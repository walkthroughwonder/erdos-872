#!/usr/bin/env bash
# Restore cron infrastructure into a fresh sandbox at /home/user/workspace/cron_tracking/.
# Usage: bash cron/restore_to_workspace.sh
set -euo pipefail
DEST="/home/user/workspace/cron_tracking"
mkdir -p "$DEST"
for d in cron/*/; do
  cron_id=$(basename "$d")
  [ "$cron_id" = "restore_to_workspace.sh" ] && continue
  mkdir -p "$DEST/$cron_id"
  cp "$d"run_scan.py "$DEST/$cron_id/"
  if [ ! -f "$DEST/$cron_id/seen_items.json" ]; then
    echo '{"arxiv_ids":[],"wiki_row_hashes":[],"wiki_last_snapshot_date":null}' > "$DEST/$cron_id/seen_items.json"
  fi
  chmod +x "$DEST/$cron_id/run_scan.py"
  echo "restored cron $cron_id -> $DEST/$cron_id/"
done
