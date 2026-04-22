#!/bin/bash
# MuhendisAl — SQLite DB atomic backup + 7-day rotate
# Kullanim: ./scripts/backup_db.sh
#
# Notlar:
#   - cp degil sqlite3 .backup kullanilir (transaction-safe, aktif write'a ragmen guvenli)
#   - gzip ile sikistirilir (53 KB → ~15 KB)
#   - 7 gunden eski otomatik silinir
#   - /root/muhendisal-platform/backups/ dizini otomatik yaratilir

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB="$ROOT/backend/data.db"
BACKUP_DIR="$ROOT/backups"
RETENTION_DAYS=7

if [ ! -f "$DB" ]; then
  echo "❌ DB bulunamadi: $DB" >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR"

TS=$(date +%Y-%m-%d_%H%M%S)
TMP="$BACKUP_DIR/.tmp_$TS.db"
OUT="$BACKUP_DIR/data_$TS.db.gz"

# Atomic SQLite backup
sqlite3 "$DB" ".backup '$TMP'"

# Integrity kontrolu (bozuk backup almayalim)
if ! sqlite3 "$TMP" "PRAGMA integrity_check;" | grep -q "^ok$"; then
  echo "❌ Backup integrity_check FAIL" >&2
  rm -f "$TMP"
  exit 2
fi

# Sikistir + rename (atomic)
gzip -9 "$TMP"                                      # .tmp_X.db.gz olur
mv "$BACKUP_DIR/.tmp_$TS.db.gz" "$OUT"

# Rotate: N gunden eski sil
find "$BACKUP_DIR" -maxdepth 1 -name 'data_*.db.gz' -mtime +$RETENTION_DAYS -delete

# Ozet
SIZE=$(du -h "$OUT" | cut -f1)
COUNT=$(ls -1 "$BACKUP_DIR"/data_*.db.gz 2>/dev/null | wc -l)
echo "✅ Backup: $OUT ($SIZE) | Toplam dosya: $COUNT"
