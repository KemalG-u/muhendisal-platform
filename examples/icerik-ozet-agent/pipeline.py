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
import logging
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from agents import radar, yazar, evaluator, publisher
from agents.evaluator import Puan

# Script konumu — nereden çağrılırsa çağrılsın yolları tutarlı tut
SCRIPT_DIR = Path(__file__).resolve().parent
DB_YOL = SCRIPT_DIR / "db" / "taslaklar.db"
SCHEMA_YOL = SCRIPT_DIR / "db" / "schema.sql"
REPORTS_DIR = SCRIPT_DIR / "reports"

load_dotenv(SCRIPT_DIR / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("pipeline")


def db_hazirla() -> sqlite3.Connection:
    """SQLite DB + şema kontrolü."""
    DB_YOL.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_YOL)
    with open(SCHEMA_YOL, encoding="utf-8") as f:
        conn.executescript(f.read())
    return conn


def db_kaydet(conn: sqlite3.Connection, puanlar: list[Puan]) -> None:
    """Puanları tek batch olarak taslaklar tablosuna yaz.

    Her Puan'ın `yayinlandi` alanı publisher tarafından set edilmiş olmalı —
    id() hilesi yok, dataclass field'ı tek doğru kaynak.
    """
    bugun = date.today().isoformat()
    rows = [
        (
            bugun,
            p.ozet.haber.baslik, p.ozet.haber.link, p.ozet.haber.kaynak, p.ozet.metin,
            p.teknik_dogruluk, p.turkce_kalitesi, p.ozet_netligi, p.ortalama,
            p.ozet.model,
            p.ozet.input_tokens + p.input_tokens,
            p.ozet.output_tokens + p.output_tokens,
            1 if p.yayinlandi else 0,
        )
        for p in puanlar
    ]
    conn.executemany(
        """
        INSERT INTO taslaklar
          (tarih, baslik, link, kaynak, ozet,
           teknik_dogruluk, turkce_kalitesi, ozet_netligi, ortalama,
           model, input_tokens, output_tokens, yayinlandi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()


async def calistir(args) -> int:
    """Tüm pipeline'ı koştur, exit code döner (0 = başarı)."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("HATA: ANTHROPIC_API_KEY tanımlı değil (.env dosyasını kontrol et)")
        return 1

    # 1. RADAR — haberleri topla
    log.info("[radar] Son %d saat taranıyor...", args.son_saat)
    haberler = await radar.topla(son_saat=args.son_saat, max_adet=args.max_adet)
    log.info("[radar] %d başlık bulundu", len(haberler))
    if not haberler:
        log.info("[radar] Yeni haber yok — çıkılıyor")
        return 0

    # 2. YAZAR — paralel özet üret
    log.info("[yazar] %d özet paralel üretiliyor...", len(haberler))
    ozetler = await yazar.ozetle_toplu(haberler)
    yazar_maliyet = sum(o.maliyet_usd for o in ozetler)
    yazar_out = sum(o.output_tokens for o in ozetler)
    log.info("[yazar] tamam — %d output token, $%.4f", yazar_out, yazar_maliyet)

    # 3. EVALUATOR — paralel puanla
    log.info("[evaluator] %d özet puanlanıyor...", len(ozetler))
    puanlar = await evaluator.puanla_toplu(ozetler)
    if puanlar:
        ortalama = sum(p.ortalama for p in puanlar) / len(puanlar)
    else:
        ortalama = 0.0
    eval_maliyet = sum(p.maliyet_usd for p in puanlar)
    log.info(
        "[evaluator] tamam — ortalama %.1f/10, $%.4f", ortalama, eval_maliyet
    )

    # 4. PUBLISHER — eşik üstü raporla + Puan.yayinlandi = True yapar
    rapor_yolu, _yayin = publisher.rapor_yaz(
        puanlar, esik=args.esik, dizin=REPORTS_DIR, dry_run=args.dry_run
    )

    # 5. DB kayıt — Puan.yayinlandi flag'ine göre
    conn = db_hazirla()
    try:
        db_kaydet(conn, puanlar)
    finally:
        conn.close()
    log.info("[db] %d kayıt taslaklar tablosuna eklendi", len(puanlar))

    # 6. Opsiyonel email
    if rapor_yolu and not args.dry_run:
        publisher.email_gonder(rapor_yolu)

    toplam = yazar_maliyet + eval_maliyet
    log.info("[maliyet] toplam: $%.4f", toplam)
    return 0


def son_raporu_goster() -> int:
    """reports/ dizinindeki en son .md dosyasını konsola basar."""
    if not REPORTS_DIR.exists():
        print("reports/ dizini yok — henüz rapor üretilmedi")
        return 1
    dosyalar = sorted(REPORTS_DIR.glob("*.md"))
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
