# Cron infrastructure mirror

This directory mirrors the scheduled-task scripts that run inside the Perplexity
Computer sandbox at `/home/user/workspace/cron_tracking/<cron_id>/`. Because the
sandbox can be wiped between long-idle gaps, the canonical copy of `run_scan.py`
lives here in git so the cron can be restored without re-deriving the script
from its prompt-spec.

## Layout

```
cron/
  5bcb853e/run_scan.py   AI-Erdős & autoformalization daily scan
  restore_to_workspace.sh  one-shot restore into the sandbox
```

## Restore after a sandbox wipe

```
bash cron/restore_to_workspace.sh
```

This copies `run_scan.py` into the right sandbox location and seeds an empty
`seen_items.json` if one is not already present.

## Notes

- State (`seen_items.json`) is intentionally NOT mirrored here. It is sandbox-local
  and rebuilt by the first post-restore run (the script marks all current wiki
  rows as seen on a wiki_last_snapshot_date=null first-run to avoid blasting
  the user with the full historical wiki as "new").
- Snapshot files (`tao_wiki_fetch_YYYY-MM-DD.md`) and findings
  (`run_findings_YYYY-MM-DD.json`) are also sandbox-local and ephemeral.
