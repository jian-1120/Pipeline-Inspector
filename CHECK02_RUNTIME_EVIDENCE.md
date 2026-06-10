# Check02 Runtime Evidence

Date: 2026-06-10

Scope: Blender runtime validation for Check02, Material Assignment.

Project root:

`C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector`

Documents read:

- `CLAUDE.md`
- `RUNTIME_VALIDATION_CHECK02.md`

## Environment

- Blender executable: `D:\ProgramData\blender.exe`
- Blender version: `5.1.1`
- Runtime mode: Blender background execution
- Add-on runtime path: `C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector`
- Loaded Check02 source: `C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector\checks\materials.py`
- Loaded Check02 SHA256: `43e715321c74a73bd9cc3687f04501356398426c9d227813c92ce3af20cfdd74`
- Repository Check02 SHA256 after deployment sync: `43e715321c74a73bd9cc3687f04501356398426c9d227813c92ce3af20cfdd74`
- `materials.material_status`: present
- `materials.classify_material`: present

Deployment note:

- Before runtime validation, the repository `pipeline_inspector/` folder was synced to Blender 5.1's add-ons folder using the documented direct-sync deployment workflow.
- No source code was modified.
- No new checks were implemented.

Screenshots:

- Not available. Validation was executed in Blender background runtime.

Console:

- Blender exited with code `0`.
- No Python traceback was observed.
- Console output included Blender `Material.use_nodes` deprecation warnings for future Blender 6.0.
- These warnings did not stop execution and did not affect Check02 results.

## Summary

| Scenario | Expected | Actual | Conclusion |
| --- | --- | --- | --- |
| PASS: connected node material | PASS | PASS | PASS |
| FAIL: no material slots | FAIL | FAIL | PASS |
| WARNING: valid material plus empty extra slot | WARNING | WARNING | PASS |

Overall Check02 runtime validation result for requested PASS / FAIL / WARNING paths: PASS.

## Scenario PASS: Connected Node Material

Scene setup:

- Created `Cube`.
- Added node material `Connected_Material`.
- Used default node graph: Principled BSDF connected to Material Output `Surface`.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check02 status: `PASS`
- Check02 severity: `BLOCKER`
- Check02 message: `All mesh objects have export-relevant materials.`
- Affected objects: empty list
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`

Actual result:

- Operator result: `FINISHED`
- Check02 status: `PASS`
- Check02 severity: `BLOCKER`
- Check02 message: `All mesh objects have export-relevant materials.`
- Affected objects: empty list
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`
- Scene unchanged after inspection: yes

Scene proof before inspection:

```text
Object: Cube
Material slot 0: Connected_Material
use_nodes: true
Material Output Surface linked: true
```

Rendered report excerpt:

```text
READY FOR DELIVERY
Score: 100
0 Blocking Issue(s)
0 Warning(s)
PASS  02_material_assignment  Material Assignment
Material Assignment: PASS
All inspected mesh objects have export-relevant materials.
```

Conclusion: PASS.

## Scenario FAIL: No Material Slots

Scene setup:

- Created `Cube`.
- Removed all material slots so the material slot list was empty.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check02 status: `FAIL`
- Check02 severity: `BLOCKER`
- Check02 message: `1 object(s) have missing or disconnected materials: Cube.`
- Affected objects: `Cube`
- Reason: `Object has no material slots.`
- Verdict: `NOT_READY`
- Score: `85`
- Blocking Issue(s): `1`
- Warning(s): `0`

Actual result:

- Operator result: `FINISHED`
- Check02 status: `FAIL`
- Check02 severity: `BLOCKER`
- Check02 message: `1 object(s) have missing or disconnected materials: Cube.`
- Affected objects: `Cube`
- Issue reason: `Object has no material slots.`
- Issue detail: `Object has no material slots.`
- Verdict: `NOT_READY`
- Score: `85`
- Blocking Issue(s): `1`
- Warning(s): `0`
- Scene unchanged after inspection: yes

Scene proof before inspection:

```text
Object: Cube
Material slots: empty list
```

Rendered report excerpt:

```text
NOT READY FOR DELIVERY
Score: 85
1 Blocking Issue(s)
0 Warning(s)
FAIL  02_material_assignment  Material Assignment
Material Assignment: FAIL
1 object(s) have missing or disconnected materials: Cube.
Affected Objects:
- Cube
  Object has no material slots.
```

Conclusion: PASS.

## Scenario WARNING: Valid Material Plus Empty Extra Slot

Scene setup:

- Created `crate_a`.
- Added valid connected material `Valid_Material` in slot 0.
- Added a second material slot and left it empty.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check02 status: `WARNING`
- Check02 severity: `WARNING`
- Check02 message: `1 object(s) have empty or legacy material slots: crate_a.`
- Affected objects: `crate_a`
- Reason: `Empty material slot at index 1.`
- Verdict: `READY_WITH_WARNINGS`
- Score: `97`
- Blocking Issue(s): `0`
- Warning(s): `1`

Actual result:

- Operator result: `FINISHED`
- Check02 status: `WARNING`
- Check02 severity: `WARNING`
- Check02 message: `1 object(s) have empty or legacy material slots: crate_a.`
- Affected objects: `crate_a`
- Issue reason: `Empty material slot at index 1.`
- Issue detail: `Empty material slot at index 1.`
- Verdict: `READY_WITH_WARNINGS`
- Score: `97`
- Blocking Issue(s): `0`
- Warning(s): `1`
- Scene unchanged after inspection: yes

Scene proof before inspection:

```text
Object: crate_a
Material slot 0: Valid_Material
use_nodes: true
Material Output Surface linked: true
Material slot 1: empty
```

Rendered report excerpt:

```text
READY WITH WARNINGS
Score: 97
0 Blocking Issue(s)
1 Warning(s)
WARN  02_material_assignment  Material Assignment
Material Assignment: WARN
1 object(s) have empty or legacy material slots: crate_a.
Affected Objects:
- crate_a
  Empty material slot at index 1.
```

Conclusion: PASS.

## Other Checks During These Runs

The validation focused on Check02.

During all three runs:

- Check01 Texture Presence rendered as `PASS`.
- Check03 Applied Scale rendered as `PASS`.
- Check04 UV Existence rendered as `PASS`.
- Check05 Normal Consistency rendered as `SKIP` / `NOT_IMPLEMENTED`.

This kept Check02 isolated for score and verdict validation.

## Final Conclusion

Check02 Material Assignment matched the runtime specification for the requested PASS / FAIL / WARNING scenarios:

- Connected node material: PASS as expected.
- No material slots: FAIL as expected.
- Valid material plus empty extra slot: WARNING as expected.

No source code was modified and no new checks were implemented.
