#!/usr/bin/env python3
"""mkdocs.yml'deki tum sayfalari standart sablonla bos olarak olustur."""
import yaml
import os
from pathlib import Path

ROOT = Path('/root/muhendisal-platform')
DOCS = ROOT / 'docs'
DOCS.mkdir(exist_ok=True)
(DOCS / 'assets').mkdir(exist_ok=True)

# Custom CSS (turuncu vurgu, Türkçe özel ayarlar)
CSS = """/* MühendisAl özel stil */
:root {
  --md-primary-fg-color: #ff6b35;
  --md-accent-fg-color: #cc5520;
}
.md-typeset h1 { font-weight: 700; letter-spacing: -0.02em; }
.md-typeset h2 { border-bottom: 1px solid var(--md-default-fg-color--lightest); padding-bottom: 0.3rem; }
.md-typeset .admonition.bolum-bilgi { border-left-color: #ff6b35; }
.md-typeset .admonition.bolum-bilgi > .admonition-title { background-color: rgba(255,107,53,0.1); }
.md-typeset .admonition.bolum-bilgi > .admonition-title::before { background-color: #ff6b35; }

/* Quiz kutusu */
.quiz {
  background: rgba(255,107,53,0.05);
  border: 1px solid rgba(255,107,53,0.3);
  border-radius: 8px;
  padding: 1rem 1.5rem;
  margin: 1.5rem 0;
}
.quiz summary { font-weight: 600; cursor: pointer; }
.quiz summary:hover { color: #ff6b35; }

/* Mobile */
@media (max-width: 768px) {
  .md-typeset table:not([class]) { font-size: 0.85em; }
}
"""
(DOCS / 'assets' / 'custom.css').write_text(CSS, encoding='utf-8')

with open(ROOT / 'mkdocs.yml') as f:
    class IgnoreTags(yaml.SafeLoader): pass
    IgnoreTags.add_multi_constructor("tag:yaml.org,2002:python", lambda l,t,n: None)
    config = yaml.load(f, Loader=IgnoreTags)

def collect_pages(nav, paths=None):
    if paths is None: paths = []
    for item in nav:
        if isinstance(item, dict):
            for key, val in item.items():
                if isinstance(val, str):
                    if not val.startswith('http'):
                        paths.append((key, val))
                elif isinstance(val, list):
                    collect_pages(val, paths)
    return paths

pages = collect_pages(config['nav'])
print(f"Toplam sayfa: {len(pages)}")

# Standart icerik sablonu
def template(title, slug):
    is_index = slug.endswith('/index.md') or slug == 'index.md'
    if is_index and slug != 'index.md':
        # Bolum index sayfasi
        bolum_no = slug.split('/')[0].replace('bolum-', '')
        return f"""# {title}

!!! info "Bolum {bolum_no}"
    Bu bolum henuz yazilmadi. FAZ {int(bolum_no)+2} sirasinda yazilacak.

## Bu Bolumde Ogrenecegin

- [ ] Konu 1
- [ ] Konu 2
- [ ] Konu 3

## Sayfalar

Sol menudeki sayfalari sirayla takip et.

## Tahmini Sure

2-3 saat

---

**[Sonraki Bolum →](../bolum-{int(bolum_no)+1}/index.md)**
"""
    elif slug == 'index.md':
        return None  # ana sayfa ayri yazilacak
    else:
        return f"""# {title}

!!! warning "Henuz yazilmadi"
    Bu sayfa iskelet halinde. Icerik FAZ planinda yazilacak.

## 📘 Teori (Turkce, basit dil)

[Konunun ne oldugu, niye onemli — basit anlatim]

## 🗣️ Onemli Ingilizce Terimler

| Terim | Turkce | Nerede Kullanilir |
|---|---|---|
| Term | Karsilik | Aciklama |

## 💻 Pratik Kod Ornegi

```python
# Yorumlarla aciklamali kod ornegi
print("Merhaba dunya")
```

## 🛠️ Bugun Yapacagin Gorev (15-30 dk)

1. Adim 1
2. Adim 2
3. Adim 3

## 🧪 Simulasyon ve Test

```bash
# VPS'de calistirilacak komutlar
echo "test"
```

Beklenen cikti:
```
test
```

## ❓ Kendini Test Et

??? quiz "1. Soru?"
    Cevap

??? quiz "2. Soru?"
    Cevap

## 🔗 Sonraki Adim

Bir sonraki sayfaya gec.

## 📚 Daha Detay

- [Referans ceviri](https://wiki.oluk.org/muhendisal/)
- Harici kaynak: [link](https://example.com)
"""

# Olustur
for title, path in pages:
    full_path = DOCS / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if full_path.exists():
        continue
    content = template(title, path)
    if content:
        full_path.write_text(content, encoding='utf-8')

print(f"Sayfalar olusturuldu: {DOCS}")
print(f"Toplam dosya: {sum(1 for _ in DOCS.rglob('*.md'))}")
