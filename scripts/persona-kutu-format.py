#!/usr/bin/env python3
"""Persona kutusunu (.ma-meta) tek satırdan 4 satırlı flex format'a çevir.

Eski format:
    <div class="ma-meta" markdown>
    **Persona:** ... · **Süre:** ... · **Önkoşul:** ... · **Çıktı:** ...
    </div>

Yeni format:
    <div class="ma-meta" markdown>
    <div class="ma-meta-row"><span class="ma-icon">👤</span> <strong>Kim için:</strong> ...</div>
    <div class="ma-meta-row"><span class="ma-icon">⏱️</span> <strong>Süre:</strong> ...</div>
    <div class="ma-meta-row"><span class="ma-icon">📋</span> <strong>Önkoşul:</strong> ...</div>
    <div class="ma-meta-row"><span class="ma-icon">🎯</span> <strong>Çıktı:</strong> ...</div>
    </div>

Zaten 4 satırlı olan dosyaları atlar (idempotent).
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# Eski tek satır formatını yakala — `**Etiket:** içerik · **Etiket:**` deseni
OLD_PATTERN = re.compile(
    r'<div class="ma-meta" markdown>\s*\n'
    r'\*\*(Persona|Kim için|Kim):\*\*\s*(.*?)\s*·\s*'
    r'\*\*(Süre):\*\*\s*(.*?)\s*·\s*'
    r'\*\*(Önkoşul):\*\*\s*(.*?)\s*·\s*'
    r'\*\*(Çıktı):\*\*\s*(.*?)\s*\n'
    r'</div>',
    re.DOTALL,
)

# Aşama 3.5: Etiket → ikon eşlemesi
ICONS = {
    "Persona": "👤",
    "Kim için": "👤",
    "Kim": "👤",
    "Süre": "⏱️",
    "Önkoşul": "📋",
    "Çıktı": "🎯",
}


def transform(content: str) -> tuple[str, bool]:
    def repl(m):
        rows = []
        # Persona/Kim için satırı (Persona etiketi varsa "Kim için" yap)
        kim_label = "Kim için" if m.group(1) == "Persona" else m.group(1)
        rows.append(f'<div class="ma-meta-row"><span class="ma-icon">{ICONS[m.group(1)]}</span> <strong>{kim_label}:</strong> {m.group(2).strip()}</div>')
        rows.append(f'<div class="ma-meta-row"><span class="ma-icon">{ICONS["Süre"]}</span> <strong>Süre:</strong> {m.group(4).strip()}</div>')
        rows.append(f'<div class="ma-meta-row"><span class="ma-icon">{ICONS["Önkoşul"]}</span> <strong>Önkoşul:</strong> {m.group(6).strip()}</div>')
        rows.append(f'<div class="ma-meta-row"><span class="ma-icon">{ICONS["Çıktı"]}</span> <strong>Çıktı:</strong> {m.group(8).strip()}</div>')
        return '<div class="ma-meta" markdown>\n' + '\n'.join(rows) + '\n</div>'

    new_content, count = OLD_PATTERN.subn(repl, content)
    return new_content, count > 0


def main():
    changed = 0
    skipped = 0
    for md_file in DOCS.rglob("*.md"):
        if "dashboard" in str(md_file) or "glossary" in str(md_file):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new, did = transform(content)
        if did:
            md_file.write_text(new, encoding="utf-8")
            changed += 1
            print(f"OK {md_file.relative_to(ROOT)}")
        else:
            skipped += 1
    print(f"\nDeğiştirilen: {changed}, Atlanan (zaten 4 satır veya format eşleşmedi): {skipped}")


if __name__ == "__main__":
    main()
