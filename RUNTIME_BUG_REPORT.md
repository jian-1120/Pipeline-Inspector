# Runtime Bug Report — Check 03 (Applied Scale) Always Passes

## Summary

Check 03 (Applied Scale) passes in Blender even when a mesh object has
unapplied scale. The committed **source** implementation is correct and fully
tested. The defect is a **packaging / runtime-loading** problem: the installed
add-on zip (`PipelineInspector_Scaffold_v0.1.zip`) still contains the old
scaffold placeholder version of `transforms.py`, which returns `PASS`
unconditionally. Blender loads that stale code, not the implemented check.

No source code was modified during this investigation.

## Evidence Reproduced

| Scenario | Observed | Expected | Explanation |
|---|---|---|---|
| Default cube | PASS | PASS | Scale is (1,1,1); both stale and real code agree. |
| Cube scaled S→2 (no Ctrl+A) | PASS | FAIL | Stale placeholder ignores scale and returns PASS. |
| Suzanne scene with unapplied scale | PASS | FAIL | Same stale placeholder. |

The default cube "passes" by coincidence: the placeholder returns PASS for every
input, so it only looks correct when the right answer happens to be PASS.

## Verification Performed (read-only)

1. **Check 03 is registered** — Yes.
   `pipeline_inspector/checks/__init__.py:8` lists
   `(transforms.CHECK_ID, transforms.CHECK_NAME, transforms.run)` in
   `CHECK_REGISTRY`.

2. **Check 03 is executed** — Yes.
   `pipeline_inspector/inspector.py:22` runs every registered check:
   `results = [check_fn(inputs) for _, _, check_fn in CHECK_REGISTRY]`.

3. **Inspector passes correct mesh objects** — Yes.
   `pipeline_inspector/inspector.py:16-19` collects visible, non-linked MESH
   objects and places them under `inputs["mesh_objects"]`, which is exactly the
   key the check reads.

4. **The check reads `obj.scale` correctly** — Yes (in source).
   `pipeline_inspector/checks/transforms.py:31` calls
   `scale_is_applied(obj.scale, obj.delta_scale)`, and `_is_identity`
   (`transforms.py:18`) compares each component against `1.0` using
   `constants.SCALE_EPSILON = 1e-4` (`constants.py:3`). A cube scaled to
   (2,2,2) fails this test, producing a FAIL result.

5. **Source unit tests pass** — Yes. `tests/test_check_03_applied_scale.py`
   has 10 tests, all passing. `test_single_unapplied_fails`
   (`tests/test_check_03_applied_scale.py:52-59`) asserts that a cube with
   `scale=(2.0, 2.0, 2.0)` yields `Status.FAIL` — the exact Evidence #2
   scenario. The source is behaviorally correct.

6. **Blender runtime is loading old implementation** — CONFIRMED. This is the
   root cause (see below).

## Root Cause

Blender loads the installed add-on package, not the working tree. The committed
package `PipelineInspector_Scaffold_v0.1.zip` was built during the scaffold
phase **before** the real check existed, and it still ships the placeholder.

Timeline (from `git log`):

- `2026-06-05 02:42` — commit `4c0da08` "Prepare first runtime validation
  package" adds `PipelineInspector_Scaffold_v0.1.zip` (scaffold placeholders).
- `2026-06-06 18:34` — commit `b5485c7` "Implement Check 03 Applied Scale"
  replaces the placeholder in the source tree.

The zip was **never rebuilt** after Check 03 was implemented, so the installed
add-on is one day stale for this file.

### Proof: contents of the zip

`transforms.py` extracted from `PipelineInspector_Scaffold_v0.1.zip`:

```python
"""Check 03 — Applied Scale. Scaffold placeholder; returns PASS."""

from .. import models
from . import base

CHECK_ID = "03_applied_scale"
CHECK_NAME = "Applied Scale"
SEVERITY = models.Severity.BLOCKER


def run(inputs):
    return base.make_pass(CHECK_ID, CHECK_NAME, SEVERITY)
```

This `run()` ignores `inputs` entirely and always returns PASS. It is byte-for-byte
the pre-implementation version (`git show 4c0da08:pipeline_inspector/checks/transforms.py`),
not the current source.

## Exact File and Lines

- **Defective artifact:** `PipelineInspector_Scaffold_v0.1.zip`
  → member `pipeline_inspector/checks/transforms.py`
- **Offending behavior:** the placeholder `run(inputs)` body
  (`return base.make_pass(...)` with no scale inspection) — the single `run`
  function in that zip member.
- **Correct source for comparison:** working-tree
  `pipeline_inspector/checks/transforms.py:26-59` (the real `run`), with the
  scale predicate at `transforms.py:17-23`.

The source tree is **not** at fault. No source line needs to change to fix the
observed runtime behavior.

## Fix Recommendation

1. **Rebuild the add-on package from current source** so the zip contains the
   implemented `transforms.py` (and any other checks updated since
   `2026-06-05`). The zip must contain the `pipeline_inspector/` folder at the
   zip root, per `RUNTIME_VALIDATION.md`.

2. **Re-install in Blender from the freshly built zip.** Removing the old
   add-on before installing avoids Python module caching of the stale file:
   - `Edit > Preferences > Add-ons` → remove "Pipeline Inspector".
   - Restart Blender (clears any cached `pipeline_inspector.*` modules).
   - Install the new zip and enable the add-on.

3. **Re-run the three evidence scenarios.** Expected after the rebuild:
   default cube → PASS, scaled cube (no Ctrl+A) → FAIL, Suzanne with unapplied
   scale → FAIL.

4. **Prevent recurrence (process):**
   - Treat the runtime zip as a build artifact: rebuild it on every check
     implementation, and avoid committing a stale binary that lags the source.
     Consider generating the zip in CI from the current tree rather than
     committing it by hand.
   - Rename the delivery package away from `_Scaffold_v0.1` once real checks
     ship, so an outdated scaffold zip cannot be installed by mistake.
   - Add a quick version/marker check (e.g., surface the loaded module's
     implementation status in the panel) so a placeholder build is obvious at
     runtime.
