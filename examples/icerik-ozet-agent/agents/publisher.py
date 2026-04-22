"""Publisher — Eşik üstü özetleri markdown rapor dosyasına yazar.

Opsiyonel: SMTP ile email gönderimi. Dry-run modunda dosya yazmaz,
sadece konsola basar.

Referans: Bölüm 6 6.5 karar matrisi — kalite filtresi burada uygulanır.
"""

from __future__ import annotations

import os
import smtplib
from datetime import date
from email.message import EmailMessage
from pathlib import Path

from .evaluator import Puan


def rapor_yaz(
    puanlar: list[Puan],
    esik: float = 6.5,
    dizin: str = "reports",
    dry_run: bool = False,
) -> tuple[Path | None, list[Puan]]:
    """Eşik üstü özetleri tek bir markdown dosyasına yazar.

    Args:
        puanlar: Evaluator'dan gelen puanlanmış özetler.
        esik: Ortalama puan bu değerden büyük olanlar rapora girer (0-10).
        dizin: Rapor dosyalarının yazılacağı dizin.
        dry_run: True ise dosyaya yazmaz, konsola basar.

    Returns:
        (rapor_yolu, yayinlanan_puanlar) — dry_run ise rapor_yolu None.
    """
    yayin = [p for p in puanlar if p.ortalama >= esik]
    yayin.sort(key=lambda p: p.ortalama, reverse=True)

    if not yayin:
        print(f"[publisher] Eşik {esik}'in üstünde özet yok — rapor yazılmadı.")
        return None, []

    bugun = date.today().isoformat()
    baslik = f"# Türkçe AI Haberleri — {bugun}\n\n"
    baslik += f"_{len(yayin)} öne çıkan özet, ortalama puan eşiği: {esik}_\n\n---\n\n"

    bolumler = []
    for i, p in enumerate(yayin, 1):
        h = p.ozet.haber
        bolumler.append(
            f"## {i}. {h.baslik}\n\n"
            f"{p.ozet.metin}\n\n"
            f"- **Kaynak:** [{h.kaynak}]({h.link})\n"
            f"- **Yayın:** {h.yayin_tarihi.strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"- **Kalite:** {p.ortalama:.1f}/10 "
            f"(tek.{p.teknik_dogruluk} · dil:{p.turkce_kalitesi} · net:{p.ozet_netligi})\n"
        )

    icerik = baslik + "\n---\n\n".join(bolumler) + "\n"

    if dry_run:
        print("=" * 60)
        print(icerik)
        print("=" * 60)
        return None, yayin

    Path(dizin).mkdir(parents=True, exist_ok=True)
    yol = Path(dizin) / f"{bugun}.md"
    yol.write_text(icerik, encoding="utf-8")
    print(f"[publisher] {len(yayin)} özet rapora yazıldı: {yol}")
    return yol, yayin


def email_gonder(rapor_yolu: Path, konu: str | None = None) -> bool:
    """Raporu SMTP üstünden email olarak yollar.

    Env var: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, REPORT_TO_EMAIL.
    Herhangi biri boşsa atlanır.

    Returns:
        True → email gönderildi; False → atlandı veya hata.
    """
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    sifre = os.environ.get("SMTP_PASS")
    alici = os.environ.get("REPORT_TO_EMAIL")

    if not all([host, user, sifre, alici]):
        print("[publisher] SMTP env eksik — email atlanıyor")
        return False

    konu = konu or f"AI Haberleri — {date.today().isoformat()}"
    icerik = rapor_yolu.read_text(encoding="utf-8")

    mesaj = EmailMessage()
    mesaj["From"] = user
    mesaj["To"] = alici
    mesaj["Subject"] = konu
    mesaj.set_content(icerik)

    try:
        with smtplib.SMTP(host, port) as s:
            s.starttls()
            s.login(user, sifre)
            s.send_message(mesaj)
        print(f"[publisher] Email {alici} adresine gönderildi")
        return True
    except (smtplib.SMTPException, OSError) as e:
        print(f"[publisher] SMTP hatası: {e}")
        return False
