# Check05 Runtime Evidence

Date: 2026-06-10

Scope: Blender runtime validation for Check05, Normal Consistency.

Project root:

`C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector`

Documents read:

- `CLAUDE.md`

Requested document status:

- `RUNTIME_VALIDATION_CHECK05.md` was requested but was not present in the local repository.
- Validation was executed against the user-provided target scenarios and the current Check05 implementation on branch `implement-check02-material-assignment`.

## Environment

- Blender executable: `D:\ProgramData\blender.exe`
- Blender version: `5.1.1`
- Runtime mode: Blender background execution
- Add-on runtime path: `C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector`
- Loaded Check05 source: `C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector\checks\normals.py`
- Loaded Check05 SHA256: `b20de938f5e97f8deb13eb6e823a9b7d1403341c6ef3cce567270bf5ee1c4880`
- Repository Check05 SHA256 after deployment sync: `b20de938f5e97f8deb13eb6e823a9b7d1403341c6ef3cce567270bf5ee1c4880`
- `normals.classify_winding`: present
- `normals.classify_object`: present

Deployment note:

- Before runtime validation, the repository `pipeline_inspector/` folder was synced to Blender 5.1's add-ons folder using the documented direct-sync deployment workflow.
- No source code was modified.
- No new checks were implemented.

Screenshots:

- Not available. Validation was executed in Blender background runtime.

Console:

- Blender exited with code `0`.
- No Python traceback was observed.
- Console output included a Blender `Material.use_nodes` deprecation warning for future Blender 6.0.
- The warning did not stop execution and did not affect Check05 results.

## Summary

| Scenario | Expected | Actual | Conclusion |
| --- | --- | --- | --- |
| 1. Clean closed mesh | PASS | PASS | PASS |
| 2. Flipped single face | FAIL | FAIL | PASS |
| 3. Open plane | PASS | PASS | PASS |
| 4. Non-manifold component | INFO note / PASS status | INFO note / PASS status | PASS |
| 5. Custom Normals | WARNING | WARNING | PASS |
| 6. Oversize mesh | WARNING | WARNING | PASS |
| 7. Multi-object mixed scene | FAIL | FAIL | PASS |

Overall Check05 runtime validation result: PASS.

## Scenario 1: Clean Closed Mesh

Scene setup:

- Created closed cube mesh named `Clean_Cube`.
- Added valid material and UV layer so Check01, Check02, and Check04 would not interfere.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check05 status: `PASS`
- Check05 severity: `BLOCKER`
- Message: `Face winding is consistent across all inspected meshes.`
- Affected objects: empty list
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`

Actual result:

- Operator result: `FINISHED`
- Check05 status: `PASS`
- Check05 severity: `BLOCKER`
- Message: `Face winding is consistent across all inspected meshes.`
- Affected objects: empty list
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`
- Scene unchanged after inspection: yes

Scene proof before inspection:

```text
Object: Clean_Cube
poly_count: 6
loop_count: 24
has_custom_normals: false
uv_layer_count: 1
material_slot_count: 1
```

Conclusion: PASS.

## Scenario 2: Flipped Single Face

Scene setup:

- Created two-triangle mesh named `Flipped_Face`.
- The second triangle traversed the shared manifold edge in the same direction as the first triangle.
- Added valid material and UV layer.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check05 status: `FAIL`
- Check05 severity: `BLOCKER`
- Message: `1 object(s) have inconsistent face winding: Flipped_Face.`
- Affected objects: `Flipped_Face`
- Verdict: `NOT_READY`
- Score: `85`
- Blocking Issue(s): `1`
- Warning(s): `0`

Actual result:

- Operator result: `FINISHED`
- Check05 status: `FAIL`
- Check05 severity: `BLOCKER`
- Message: `1 object(s) have inconsistent face winding: Flipped_Face.`
- Affected objects: `Flipped_Face`
- Issue reason: `Inconsistent face winding within a manifold component.`
- Verdict: `NOT_READY`
- Score: `85`
- Blocking Issue(s): `1`
- Warning(s): `0`
- Scene unchanged after inspection: yes

Scene proof before inspection:

```text
Object: Flipped_Face
poly_count: 2
loop_count: 6
has_custom_normals: false
uv_layer_count: 1
material_slot_count: 1
```

Conclusion: PASS.

## Scenario 3: Open Plane

Scene setup:

- Created open single-face plane named `Open_Plane`.
- Added valid material and UV layer.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check05 status: `PASS`
- Check05 severity: `BLOCKER`
- Message: `Face winding is consistent across all inspected meshes.`
- Affected objects: empty list
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`

Actual result:

- Operator result: `FINISHED`
- Check05 status: `PASS`
- Check05 severity: `BLOCKER`
- Message: `Face winding is consistent across all inspected meshes.`
- Affected objects: empty list
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`
- Scene unchanged after inspection: yes

Scene proof before inspection:

```text
Object: Open_Plane
poly_count: 1
loop_count: 4
has_custom_normals: false
uv_layer_count: 1
material_slot_count: 1
```

Conclusion: PASS.

## Scenario 4: Non-Manifold Component

Scene setup:

- Created mesh named `Nonmanifold_Component`.
- The mesh had three faces sharing one edge.
- Added valid material and UV layer.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check05 status: `PASS`
- Check05 severity: `BLOCKER`
- Message: `Face winding is consistent; 1 object(s) contain non-manifold geometry that was not evaluated: Nonmanifold_Component.`
- Affected objects: `Nonmanifold_Component`
- Issue severity: `INFO`
- Issue reason: `Non-manifold component skipped; winding not evaluated.`
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`

Actual result:

- Operator result: `FINISHED`
- Check05 status: `PASS`
- Check05 severity: `BLOCKER`
- Message: `Face winding is consistent; 1 object(s) contain non-manifold geometry that was not evaluated: Nonmanifold_Component.`
- Affected objects: `Nonmanifold_Component`
- Issue severity: `INFO`
- Issue reason: `Non-manifold component skipped; winding not evaluated.`
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`
- Scene unchanged after inspection: yes

Scene proof before inspection:

```text
Object: Nonmanifold_Component
poly_count: 3
loop_count: 9
has_custom_normals: false
uv_layer_count: 1
material_slot_count: 1
```

Conclusion: PASS.

## Scenario 5: Custom Normals

Scene setup:

- Created consistent mesh named `Custom_Normal_Object`.
- Applied custom split normals with `mesh.normals_split_custom_set(...)`.
- Confirmed `mesh.has_custom_normals` was true before inspection.
- Added valid material and UV layer.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check05 status: `WARNING`
- Check05 severity: `INFO`
- Message: `1 object(s) skipped; winding not checked: Custom_Normal_Object.`
- Affected objects: `Custom_Normal_Object`
- Issue reason: `Custom normals present; consistency check skipped.`
- Verdict: `READY_WITH_WARNINGS`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `1`

Actual result:

- Operator result: `FINISHED`
- Check05 status: `WARNING`
- Check05 severity: `INFO`
- Message: `1 object(s) skipped; winding not checked: Custom_Normal_Object.`
- Affected objects: `Custom_Normal_Object`
- Issue reason: `Custom normals present; consistency check skipped.`
- Verdict: `READY_WITH_WARNINGS`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `1`
- Scene unchanged after inspection: yes

Scene proof before inspection:

```text
Object: Custom_Normal_Object
poly_count: 2
loop_count: 6
has_custom_normals: true
uv_layer_count: 1
material_slot_count: 1
```

Conclusion: PASS.

## Scenario 6: Oversize Mesh

Scene setup:

- Created mesh named `Oversize_Mesh`.
- Mesh contained `500001` polygon entries.
- Added valid material and UV layer.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check05 status: `WARNING`
- Check05 severity: `INFO`
- Message: `1 object(s) skipped; winding not checked: Oversize_Mesh.`
- Affected objects: `Oversize_Mesh`
- Issue reason: `Mesh too large to inspect (>500k polygons); run on simplified geometry.`
- Verdict: `READY_WITH_WARNINGS`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `1`

Actual result:

- Operator result: `FINISHED`
- Check05 status: `WARNING`
- Check05 severity: `INFO`
- Message: `1 object(s) skipped; winding not checked: Oversize_Mesh.`
- Affected objects: `Oversize_Mesh`
- Issue reason: `Mesh too large to inspect (>500k polygons); run on simplified geometry.`
- Verdict: `READY_WITH_WARNINGS`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `1`
- Scene unchanged after inspection: yes

Scene proof before inspection:

```text
Object: Oversize_Mesh
poly_count: 500001
loop_count: 1500003
has_custom_normals: false
uv_layer_count: 1
material_slot_count: 1
```

Conclusion: PASS.

## Scenario 7: Multi-Object Mixed Scene

Scene setup:

- Created `Good_Cube` with consistent closed winding.
- Created `alpha_flipped` with inconsistent winding.
- Created `zebra_flipped` with inconsistent winding.
- Created `Info_Sculpt` with non-manifold geometry.
- Created `Skipped_Custom` with custom normals.
- Added valid material and UV layer to all objects.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check05 status: `FAIL`
- Check05 severity: `BLOCKER`
- Message: `2 object(s) have inconsistent face winding: alpha_flipped, zebra_flipped.`
- Affected objects: `alpha_flipped`, `zebra_flipped`
- Verdict: `NOT_READY`
- Score: `85`
- Blocking Issue(s): `1`
- Warning(s): `0`

Actual result:

- Operator result: `FINISHED`
- Check05 status: `FAIL`
- Check05 severity: `BLOCKER`
- Message: `2 object(s) have inconsistent face winding: alpha_flipped, zebra_flipped.`
- Affected objects: `alpha_flipped`, `zebra_flipped`
- Issue reasons:
  - `alpha_flipped`: `Inconsistent face winding within a manifold component.`
  - `zebra_flipped`: `Inconsistent face winding within a manifold component.`
- Verdict: `NOT_READY`
- Score: `85`
- Blocking Issue(s): `1`
- Warning(s): `0`
- Scene unchanged after inspection: yes

Scene proof before inspection:

```text
Good_Cube: poly_count 6, has_custom_normals false
Info_Sculpt: poly_count 3, has_custom_normals false
Skipped_Custom: poly_count 2, has_custom_normals true
alpha_flipped: poly_count 2, has_custom_normals false
zebra_flipped: poly_count 2, has_custom_normals false
```

Conclusion: PASS.

## Other Checks During These Runs

The validation focused on Check05.

During the Check05 scenarios, setup ensured:

- Check01 Texture Presence rendered as `PASS`.
- Check02 Material Assignment rendered as `PASS`.
- Check03 Applied Scale rendered as `PASS`.
- Check04 UV Existence rendered as `PASS`.

This kept Check05 isolated for score and verdict validation.

## Final Conclusion

Check05 Normal Consistency matched the requested Blender 5.1 runtime scenarios:

- Clean closed mesh: PASS as expected.
- Flipped single face / inconsistent winding: FAIL as expected.
- Open plane: PASS as expected.
- Non-manifold component: informational note with PASS status as expected.
- Custom Normals: WARNING as expected.
- Oversize mesh: WARNING as expected.
- Multi-object mixed scene: FAIL with sorted affected objects as expected.

No source code was modified and no new checks were implemented.
