"""Publisher — Eşik üstü özetleri markdown rapor dosyasına yazar.

Opsiyonel: SMTP ile email gönderimi. Dry-run modunda dosya yazmaz,
sadece konsola basar. Her yayınlanan Puan nesnesine `yayinlandi=True`
işaretlenir — pipeline bu bayrağa bakarak DB'ye kaydeder.

Referans: Bölüm 6.5 evaluator-optimizer pattern — kalite eşiği burada uygulanır.
"""

from __future__ import annotations

import logging
import os
import smtplib
from datetime import date
from email.message import EmailMessage
from pathlib import Path

from .evaluator import Puan

log = logging.getLogger(__name__)


def rapor_yaz(
    puanlar: list[Puan],
    esik: float = 6.5,
    dizin: str | Path = "reports",
    dry_run: bool = False,
) -> tuple[Path | None, list[Puan]]:
    """Eşik üstü özetleri tek bir markdown dosyasına yazar.

    Her yayınlanan Puan nesnesinde `yayinlandi=True` işaretlenir —
    çağıran (pipeline) DB kaydında bu alana bakar.

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

    # Yayın flag'ini işaretle — DB kaydı bu alana bakar
    for p in yayin:
        p.yayinlandi = True

    if not yayin:
        log.info("[publisher] Eşik %s'in üstünde özet yok — rapor yazılmadı.", esik)
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

    # Maliyet footer'ı — şeffaflık (agent SDK'ların `ResultMessage.total_cost_usd` benzeri)
    toplam_maliyet = sum(p.ozet.maliyet_usd + p.maliyet_usd for p in puanlar)
    toplam_in = sum(p.ozet.input_tokens + p.input_tokens for p in puanlar)
    toplam_out = sum(p.ozet.output_tokens + p.output_tokens for p in puanlar)
    footer = (
        "\n---\n\n"
        f"_Toplam {len(puanlar)} özet üretildi, {len(yayin)} tanesi eşik üstü._\n"
        f"_Maliyet: ${toplam_maliyet:.4f} · "
        f"{toplam_in:,} in + {toplam_out:,} out token._\n"
    )

    icerik = baslik + "\n---\n\n".join(bolumler) + footer

    if dry_run:
        print("=" * 60)
        print(icerik)
        print("=" * 60)
        return None, yayin

    Path(dizin).mkdir(parents=True, exist_ok=True)
    yol = Path(dizin) / f"{bugun}.md"
    yol.write_text(icerik, encoding="utf-8")
    log.info("[publisher] %d özet rapora yazıldı: %s", len(yayin), yol)
    return yol, yayin


def email_gonder(rapor_yolu: Path, konu: str | None = None) -> bool:
    """Raporu SMTP üstünden email olarak yollar.

    Env var: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, REPORT_TO_EMAIL,
    SMTP_SSL (1/0 — 1 ise doğrudan SSL port 465, 0 ise STARTTLS port 587).
    Herhangi biri boşsa atlanır.

    Returns:
        True → email gönderildi; False → atlandı veya hata.
    """
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    sifre = os.environ.get("SMTP_PASS")
    alici = os.environ.get("REPORT_TO_EMAIL")
    ssl_mode = os.environ.get("SMTP_SSL", "0") == "1"

    if not all([host, user, sifre, alici]):
        log.info("[publisher] SMTP env eksik — email atlanıyor")
        return False

    konu = konu or f"AI Haberleri — {date.today().isoformat()}"
    icerik = rapor_yolu.read_text(encoding="utf-8")

    mesaj = EmailMessage()
    mesaj["From"] = user
    mesaj["To"] = alici
    mesaj["Subject"] = konu
    mesaj.set_content(icerik)

    try:
        if ssl_mode:
            with smtplib.SMTP_SSL(host, port) as s:
                s.login(user, sifre)
                s.send_message(mesaj)
        else:
            with smtplib.SMTP(host, port) as s:
                s.starttls()
                s.login(user, sifre)
                s.send_message(mesaj)
        log.info("[publisher] Email %s adresine gönderildi", alici)
        return True
    except (smtplib.SMTPException, OSError) as e:
        log.error("[publisher] SMTP hatası: %s", e)
        return False
