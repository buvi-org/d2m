# Zero-To-CAD Verification Status

This is the single human-readable status file for live Zero-to-CAD accepted-pair
counts and planner-capacity snapshots. README, TODO, and roadmap docs should
link here instead of embedding the live count.

Last refreshed: 2026-05-22

## Accepted Original-STEP-Verified Pairs

- Accepted unique pairs: 521
- Accepted records before dedupe: 526
- Duplicates excluded by dedupe key: 5
- Split counts: train 471, val 14, test 36
- Latest source indexes by split: train 80938, val 9615, test 9631

Acceptance policy:

- Target is the original Zero-to-CAD `model.step`.
- Dedupe key is `source.split + source.uuid`.
- A row counts only when `accepted == true`, `status == "matched"`, and the
  strict volume policy passes.
- Default maximum volume error is 5%.
- Volume-only success is rejected.

Machine-readable local sources:

- `runs/zero_to_cad_live_pilots/accepted_index.jsonl`
- `runs/zero_to_cad_live_pilots/accepted_summary.json`

Regenerate with:

```powershell
python -m src.data.build_zero_to_cad_accepted_index --runs-dir runs/zero_to_cad_live_pilots --index-out runs/zero_to_cad_live_pilots/accepted_index.jsonl --summary-out runs/zero_to_cad_live_pilots/accepted_summary.json
```

## Planner Capacity Snapshot

- Snapshot date: 2026-05-21
- Local Zero-to-CAD rows scanned: 100,516
- Plannable by pure-operation planner: 79,911
- Unsupported by current planner: 20,605

Planner capacity is only an attempt queue. It is not translation success and it
does not count toward the accepted dataset until the generated pure SubCAD
executes and matches the original STEP target.

## Update Policy

Do not update README, TODO, or roadmap files for every accepted row. Refresh this
file and the generated JSON summary at meaningful milestones, after strict
policy changes, or when preparing a dataset release.
