"""MkDocs pre-build ve on-page hook'lari.

İki iş yapar:
1. pre_build: gen_dashboard_pages.py'yi otomatik çağırır (dashboard güncel).
2. on_page_markdown: includes/glossary.md içeriğini her sayfanın sonuna
   enjekte eder. Markdown `abbr` extension bu `*[TERIM]:` tanımları okur
   ve HTML'de <abbr title="..."> ile sarar — MkDocs Material tooltip gösterir.
   Sonuç: 64 sayfa için tek glossary, otomatik hover-tooltip.
"""
import subprocess
import sys
import pathlib


# Glossary dosyasi modul yukleme sirasinda bir kere okunur — her build'de
# sifirdan okumaya gerek yok, mkdocs serve sirasinda cache icin de faydali.
_ROOT = pathlib.Path(__file__).resolve().parent.parent
_GLOSSARY_PATH = _ROOT / "includes" / "glossary.md"
_GLOSSARY_CONTENT = ""
if _GLOSSARY_PATH.exists():
    _GLOSSARY_CONTENT = _GLOSSARY_PATH.read_text(encoding="utf-8")


def on_pre_build(config, **kwargs):
    """Dashboard sayfalarini otomatik uretir."""
    script = _ROOT / "scripts" / "gen_dashboard_pages.py"
    if not script.exists():
        print("[hook] gen_dashboard_pages.py yok, atlaniyor", file=sys.stderr)
        return
    try:
        out = subprocess.check_output(
            [sys.executable, str(script)],
            cwd=str(_ROOT),
            stderr=subprocess.STDOUT,
            text=True,
        )
        for line in out.strip().splitlines():
            if line.startswith("OK") or line.startswith("Toplam") or line.startswith("Bolum"):
                print(f"[hook] {line}")
    except subprocess.CalledProcessError as e:
        print(f"[hook] gen_dashboard_pages FAIL:\n{e.output}", file=sys.stderr)
        raise


def on_page_markdown(markdown, page, config, files):
    """Her sayfanin sonuna glossary tanimlarini ekler.

    abbr extension dosya bazli calisir — tanim her sayfada bulunmali.
    Bu yuzden glossary icerigini markdown'in sonuna appendleriz.
    Glossary dosyasinin kendisi navigasyonda degil (sadece tanim kaynagi).
    """
    if not _GLOSSARY_CONTENT:
        return markdown
    # Glossary'nin kendisi icin ozyinelemeye gerek yok — eger onu da
    # render ediyorsak (nav'a eklenseydi) atla. Simdilik nav'da yok.
    return markdown + "\n\n" + _GLOSSARY_CONTENT
