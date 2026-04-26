# MühendisAl Platform

AI Engineer Türkçe öğrenme platformu — interaktif quiz, kod sandbox, ilerleme takibi.

**Canlı:** https://wiki.oluk.org/platform/
**Sayfa sayısı:** <!-- SAYFA-SAYISI -->78<!-- /SAYFA-SAYISI --> (otomatik güncellenir, `./scripts/rebuild.sh` ile)

## Teknoloji

- **Frontend:** MkDocs Material + Vanilla JS widgets
- **Backend:** FastAPI + SQLite
- **Kod Sandbox:** Pyodide (basit) + Jupyter Lab (AI/ML)
- **Deployment:** VPS (Hetzner CCX23) + nginx + PM2

## Geliştirme

```bash
# Aktif olarak: VPS clawdbot2:/root/muhendisal-platform/

# Yerel test
./venv/bin/mkdocs serve -a 0.0.0.0:8000

# Build
./venv/bin/mkdocs build

# Backend (FAZ 5+)
cd backend
../venv/bin/uvicorn main:app --port 9100 --reload
```

## Faz Durumu

- [x] F0-F3: Tasarım
- [x] F1: MkDocs iskelet (64 sayfa boş şablon)
- [ ] F4: Git repo (yerel ✓, GitHub push bekliyor)
- [ ] F5: FastAPI backend
- [ ] F6: REST API endpoints
- [ ] F7: JS widgets
- [ ] F8: Dashboard
- [ ] F9: Pyodide editor
- [ ] F10: Streak/XP
- [ ] F13-25: Bölüm 0-10 içerik
- [ ] F26: Launch

Detaylı tasarım: `wiki.oluk.org/brain/muhendisal_platform_tasarim.md`

## Lisans

Özel proje — Kemal Sungur.
