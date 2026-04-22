#!/bin/bash
# MuhendisAl — tek komutla yeniden build
# Kullanim:
#   ./scripts/rebuild.sh          — sadece site build (on_pre_build hook zaten gen'i cagiriyor)
#   ./scripts/rebuild.sh --api    — backend'i de yeniden yukle (kod degistiyse)
#
# Bagimliliklar: venv aktif olmasa da kendimiz aktifleriz

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Venv yok mu?
if [ ! -d "venv" ]; then
  echo "❌ venv bulunamadi: $ROOT/venv"
  exit 1
fi

# shellcheck disable=SC1091
source venv/bin/activate

RESTART_API=0
for arg in "$@"; do
  case "$arg" in
    --api|--restart) RESTART_API=1 ;;
    --help|-h)
      echo "Kullanim: $0 [--api]"
      echo "  --api   Backend PM2 servisini yeniden baslat (kod degistiyse)"
      exit 0
      ;;
  esac
done

echo "→ mkdocs build (pre_build hook otomatik gen_dashboard_pages.py cagirir)"
mkdocs build 2>&1 | sed 's/^/   /'

if [ "$RESTART_API" -eq 1 ]; then
  echo ""
  echo "→ pm2 restart muhendisal-api"
  pm2 restart muhendisal-api 2>&1 | tail -3 | sed 's/^/   /'
  sleep 1
  HEALTH=$(curl -sf https://wiki.oluk.org/platform/api/health || echo "FAIL")
  echo "   health: $HEALTH"
fi

echo ""
echo "✅ Rebuild tamam"
echo "   Site: https://wiki.oluk.org/platform/"
