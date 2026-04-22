#!/usr/bin/env python3
"""Dashboard progress listesini mkdocs.yml nav'ından generate et.

Çalıştırma: python3 scripts/gen_dashboard_pages.py
Etki: docs/dashboard.md içindeki <!-- PAGES_START --> ... <!-- PAGES_END -->
      bloğunu bölüm bazlı <div data-page-path="..."> listesiyle değiştirir.
"""
import pathlib
import re
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
MKDOCS_YML = ROOT / "mkdocs.yml"
DASHBOARD = ROOT / "docs" / "dashboard.md"
START = "<!-- PAGES_START -->"
END = "<!-- PAGES_END -->"

# Listelenmemesi gereken yollar (dashboard kendini listelemesin, index ana sayfadir)
SKIP_PATHS = {"dashboard", "index"}


def _ignore_python_tag(loader, suffix, node):
    # mkdocs-material !!python/name:... tag'lerini ignore et
    return None


# Multi-constructor: tag:yaml.org,2002:python/ ile başlayan her şey None olsun
yaml.SafeLoader.add_multi_constructor("tag:yaml.org,2002:python/", _ignore_python_tag)


def page_path_from_md(md_rel):
    """`bolum-0/01-vps-linux.md` → `bolum-0/01-vps-linux`.

    mkdocs `use_directory_urls: true` kullandığı için `.md` uzantısı atılır.
    `index.md` → bölüm ana sayfası (parent dizin).
    """
    if md_rel.endswith("/index.md"):
        return md_rel[: -len("/index.md")]
    if md_rel == "index.md":
        return "index"
    if md_rel.endswith(".md"):
        return md_rel[:-3]
    return md_rel


def flatten_nav(nav, out=None, section=None):
    """Nav listesini gez, section başına (title, [(label, page_path), ...]) grupla."""
    if out is None:
        out = []  # [(section_title, [(item_label, page_path), ...])]
    for entry in nav:
        if not isinstance(entry, dict):
            continue
        for key, val in entry.items():
            if isinstance(val, str):
                # 'Label': 'some.md' — bu tekil sayfa (ör: Ana Sayfa: index.md)
                if val.endswith(".md"):
                    # Kök düzeyinde bir sayfa — "Genel" section'a at
                    section_title = section or "Genel"
                    _append(out, section_title, key, page_path_from_md(val))
                # URL ise atla (https://... referanslar)
            elif isinstance(val, list):
                # Bir bölüm: 'Bölüm 0 — Temel Hazırlık': [ {...}, {...} ]
                flatten_nav(val, out, section=key)
    return out


def _append(out, section_title, label, path):
    if path in SKIP_PATHS:
        return
    for s, items in out:
        if s == section_title:
            items.append((label, path))
            return
    out.append((section_title, [(label, path)]))


def render_html(groups):
    lines = []
    for section_title, items in groups:
        if not items:
            continue
        lines.append(f'<h3 class="ma-pg-section">{section_title}</h3>')
        for label, path in items:
            # Eğer label zaten "0.1 Foo" gibi numaralıysa, index.md satırları
            # "bolum-0/index.md" gibi — bunlar bölüm giriş sayfaları
            safe_label = (
                label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )
            lines.append(
                f'<div class="ma-pg-row" data-page-path="{path}">'
                f'<span class="ma-pg-icon">○</span>'
                f'<span class="ma-pg-label">{safe_label}</span>'
                f"</div>"
            )
    return "\n".join(lines)


def main():
    with MKDOCS_YML.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    nav = cfg.get("nav") or []
    groups = flatten_nav(nav)

    # Sayılar
    total = sum(len(items) for _, items in groups)
    print(f"Bölüm sayısı: {len(groups)}")
    print(f"Toplam sayfa: {total}")
    for s, items in groups:
        print(f"  {s}: {len(items)} sayfa")

    html = render_html(groups)

    # dashboard.md'deki bloğu değiştir
    md = DASHBOARD.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(START) + r".*?" + re.escape(END), re.DOTALL
    )
    new_block = f"{START}\n{html}\n{END}"
    if not pattern.search(md):
        raise SystemExit("PAGES_START/END marker bulunamadı!")
    md2 = pattern.sub(new_block, md)
    DASHBOARD.write_text(md2, encoding="utf-8")
    print(f"\nOK: dashboard.md güncellendi ({len(md2)} byte)")


if __name__ == "__main__":
    main()
