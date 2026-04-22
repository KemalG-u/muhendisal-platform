"""Pipeline — Orchestrator — giriş noktası.

Bölüm 6.5 orchestrator-workers pattern uygulaması:
    radar → yazar (paralel) → evaluator (paralel) → publisher

Kullanım:
    python pipeline.py                  # tam tarama + yayın
    python pipeline.py --dry-run        # yayınlamadan göster
    python pipeline.py --esik 7.5       # kalite eşiği üst tut
    python pipeline.py --show-last      # son raporu konsola bas
    python pipeline.py --son-saat 48    # 24 yerine 48 saatlik geri bak

Env: .env dosyasından okunur (python-dotenv).
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from agents import radar, yazar, evaluator, publisher

load_dotenv()

DB_YOL = "db/taslaklar.db"
SCHEMA_YOL = "db/schema.sql"


def db_hazirla() -> sqlite3.Connection:
    """SQLite DB + şema kontrolü."""
    Path("db").mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_YOL)
    with open(SCHEMA_YOL, encoding="utf-8") as f:
        conn.executescript(f.read())
    return conn


def db_kaydet(conn: sqlite3.Connection, puanlar: list, yayinlanan_ids: set[int]) -> None:
    """Her kayıt için bir satır taslaklar tablosuna."""
    cur = conn.cursor()
    for p in puanlar:
        h = p.ozet.haber
        cur.execute(
            """
            INSERT INTO taslaklar
              (tarih, baslik, link, kaynak, ozet,
               teknik_dogruluk, turkce_kalitesi, ozet_netligi, ortalama,
               model, input_tokens, output_tokens, yayinlandi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                date.today().isoformat(),
                h.baslik, h.link, h.kaynak, p.ozet.metin,
                p.teknik_dogruluk, p.turkce_kalitesi, p.ozet_netligi, p.ortalama,
                p.ozet.model, p.ozet.input_tokens + p.input_tokens,
                p.ozet.output_tokens + p.output_tokens,
                1 if id(p) in yayinlanan_ids else 0,
            ),
        )
    conn.commit()


async def calistir(args) -> int:
    """Tüm pipeline'ı koştur, exit code döner (0 = başarı)."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("HATA: ANTHROPIC_API_KEY tanımlı değil (.env dosyasını kontrol et)")
        return 1

    # 1. RADAR — haberleri topla
    print(f"[radar] Son {args.son_saat} saat taranıyor...")
    haberler = await radar.topla(son_saat=args.son_saat, max_adet=args.max_adet)
    print(f"[radar] {len(haberler)} başlık bulundu")
    if not haberler:
        print("[radar] Yeni haber yok — çıkılıyor")
        return 0

    # 2. YAZAR — paralel özet üret
    print(f"[yazar] {len(haberler)} özet paralel üretiliyor...")
    ozetler = await yazar.ozetle_toplu(haberler)
    yazar_maliyet = sum(o.maliyet_usd for o in ozetler)
    yazar_out = sum(o.output_tokens for o in ozetler)
    print(f"[yazar] tamam — {yazar_out} output token, ${yazar_maliyet:.4f}")

    # 3. EVALUATOR — paralel puanla
    print(f"[evaluator] {len(ozetler)} özet puanlanıyor...")
    puanlar = await evaluator.puanla_toplu(ozetler)
    ortalama = sum(p.ortalama for p in puanlar) / len(puanlar)
    eval_maliyet = sum(p.maliyet_usd for p in puanlar)
    print(f"[evaluator] tamam — ortalama {ortalama:.1f}/10, ${eval_maliyet:.4f}")

    # 4. PUBLISHER — eşik üstü raporla
    rapor_yolu, yayin = publisher.rapor_yaz(
        puanlar, esik=args.esik, dry_run=args.dry_run
    )

    # 5. DB kayıt
    yayin_ids = {id(p) for p in yayin}
    conn = db_hazirla()
    db_kaydet(conn, puanlar, yayin_ids)
    conn.close()
    print(f"[db] {len(puanlar)} kayıt taslaklar tablosuna eklendi")

    # 6. Opsiyonel email
    if rapor_yolu and not args.dry_run:
        publisher.email_gonder(rapor_yolu)

    toplam = yazar_maliyet + eval_maliyet
    print(f"[maliyet] toplam: ${toplam:.4f}")
    return 0


def son_raporu_goster() -> int:
    """reports/ dizinindeki en son .md dosyasını konsola basar."""
    dizin = Path("reports")
    if not dizin.exists():
        print("reports/ dizini yok — henüz rapor üretilmedi")
        return 1
    dosyalar = sorted(dizin.glob("*.md"))
    if not dosyalar:
        print("Henüz rapor yok")
        return 1
    son = dosyalar[-1]
    print(son.read_text(encoding="utf-8"))
    return 0


def ana():
    ap = argparse.ArgumentParser(description="İçerik Özet Agent — pipeline")
    ap.add_argument("--son-saat", type=int, default=24, help="Kaç saat geri bakılsın")
    ap.add_argument("--max-adet", type=int, default=20, help="Maks haber sayısı")
    ap.add_argument("--esik", type=float,
                    default=float(os.environ.get("QUALITY_THRESHOLD", "6.5")),
                    help="Yayın için kalite eşiği (0-10)")
    ap.add_argument("--dry-run", action="store_true", help="Dosyaya yazma, konsola bas")
    ap.add_argument("--show-last", action="store_true", help="Son raporu göster")
    args = ap.parse_args()

    if args.show_last:
        sys.exit(son_raporu_goster())
    sys.exit(asyncio.run(calistir(args)))


if __name__ == "__main__":
    ana()
