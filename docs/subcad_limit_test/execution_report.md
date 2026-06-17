# SubCAD Program Execution Report

Run date: 2026-06-16

## Scope

Executed the standalone Stage 3 Python programs under:

`docs/subcad_limit_test/subcad_programs_py/`

The runner generated STEP, STL, process-plan JSON, per-program result JSON, and
summary files under:

`runs/subcad_limit_test_execution_full_patched/`

## Mechanical Execution Result

- Python files checked: 540
- Python compile failures: 0
- Runtime failures after patching executable drafts: 0
- STEP exports generated: 540
- STL exports generated: 540
- Process-plan exports generated: 540
- Envelope checks against frozen Stage 2 dimensions: 540 pass, 0 fail

Summary file:

`runs/subcad_limit_test_execution_full_patched/summary.json`

Known-gap report:

`runs/subcad_limit_test_execution_full_patched/known_gap_report.json`

## Requirement-Match Status

The corpus is now mechanically executable, but it is not yet proven to fully
match the frozen English requirements.

Reason: every generated program still contains at least one known gap recorded
in its top-of-file comments. The common categories are:

- Chamfers: global/targeted chamfer support was removed from executable drafts
  where current SubCAD/OCC chamfering fails on complex generated solids.
- Serrations: triangular serrations are often approximated or omitted when the
  proxy cut erased or invalidated the solid.
- Side tapped holes: side-axis tapped holes are often represented as top-face
  threaded-hole proxies.
- Hook lips and projecting/undercut edges: several are represented only as
  approximations or omitted when the proxy changed the envelope.
- Other feature-form approximations: V-grooves, exact angled exterior faces,
  opposite-end counterbores, bore-edge chamfers, and similar details require
  Stage 4 review.

## Interpretation

This is a useful gate:

- SubCAD can execute all 540 generated draft programs.
- The exporters produced STEP and STL for every program.
- The gross envelope for every output matches the frozen requirement dimensions.

It is not a final pass:

- Feature-level semantic matching still needs manual/visual review against the
  Stage 2 requirement text.
- Known gaps should be treated as either `agent_error`, `subcad_gap`, or
  `export_or_geometry_bug` after review.
