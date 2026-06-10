# Check01 Runtime Evidence

Date: 2026-06-09

Scope: Blender runtime validation for Check01, Texture Presence.

Project root:

`C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector`

Documents read:

- `docs/archive/RUNTIME_TEST_CHECK01.md`
- `RUNTIME_VALIDATION_PROTOCOL.md`

Note: `RUNTIME_TEST_CHECK01.md` was not present at the repository root. It was found under `docs/archive/`.

## Environment

- Blender executable: `D:\ProgramData\blender.exe`
- Blender version: `5.1.1`
- Runtime mode: Blender background execution
- Add-on runtime path: `C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector`
- Loaded Check01 source: `C:\Users\简某\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector\checks\textures.py`
- Loaded Check01 SHA256: `5c1df4387ccba4e88fcf426b5766c3e583062795c69631979ebcf23e1edd9c58`
- Repository Check01 SHA256 after deployment sync: `5c1df4387ccba4e88fcf426b5766c3e583062795c69631979ebcf23e1edd9c58`
- `textures.image_status`: present

Deployment note:

- Before runtime validation, the repository `pipeline_inspector/` folder was synced to Blender 5.1's add-ons folder using the documented direct-sync deployment workflow.
- No source code was modified.
- No new checks were implemented.

Screenshots:

- Not available. Validation was executed in Blender background runtime.

Console:

- Blender exited with code `0`.
- No Python traceback was observed.
- Console output included Blender warnings/deprecation messages:
  - `Material.use_nodes` deprecation warning for future Blender 6.0.
  - Blender asset path warnings while saving temporary `.blend` files.
- These warnings did not stop execution and did not affect Check01 results.

Temporary runtime assets:

`C:\Users\简某\AppData\Local\Temp\pipeline_inspector_check01_runtime`

## Summary

| Scenario | Expected | Actual | Conclusion |
| --- | --- | --- | --- |
| A. Packed texture | PASS | PASS | PASS |
| B. Missing external texture | FAIL | FAIL | PASS |
| C. Generated texture | PASS | PASS | PASS |
| D. Unsaved blend | WARNING | WARNING | PASS |

Overall Check01 runtime validation result: PASS.

## Scenario A: Packed Texture

Scene setup:

- Created a clean scene with `Cube`.
- Created external PNG: `packed_texture.png`.
- Assigned the image through a node-based material Image Texture node.
- Packed the image with `image.pack()`.
- Saved the `.blend` file as `case_a_packed_texture.blend`.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check01 status: `PASS`
- Message: `All referenced textures are packed or reachable.`
- Affected objects: empty list
- Verdict: `READY`
- Score: `100`
- Blocker count: `0`
- Warning count: `0`

Actual result:

- Operator result: `FINISHED`
- Check01 status: `PASS`
- Check01 severity: `BLOCKER`
- Message: `All referenced textures are packed or reachable.`
- Affected objects: empty list
- Verdict: `READY`
- Score: `100`
- Blocker count: `0`
- Warning count: `0`
- Scene unchanged after inspection: yes

Rendered report excerpt:

```text
READY FOR DELIVERY
Score: 100
0 Blocking Issue(s)
0 Warning(s)
PASS  01_texture_presence  Texture Presence
Texture Presence: PASS
All referenced textures are packed or reachable.
```

Conclusion: PASS.

## Scenario B: Missing External Texture

Scene setup:

- Created a clean scene with `Cube`.
- Created external PNG: `missing_external_texture.png`.
- Assigned the image through a node-based material Image Texture node.
- Did not pack the image.
- Saved the `.blend` file as `case_b_missing_texture.blend`.
- Deleted the referenced PNG outside Blender before inspection.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check01 status: `FAIL`
- Severity: `BLOCKER`
- Message: `1 texture file(s) are missing or unreachable: Missing_Texture.`
- Affected objects: `Cube`
- Verdict: `NOT_READY`
- Score: `85`
- Blocker count: `1`
- Warning count: `0`

Actual result:

- Operator result: `FINISHED`
- Check01 status: `FAIL`
- Check01 severity: `BLOCKER`
- Message: `1 texture file(s) are missing or unreachable: Missing_Texture.`
- Affected objects: `Cube`
- Issue reason: `Material references missing or unreachable texture(s).`
- Issue detail: `Material references missing or unreachable texture(s). Missing_Texture.`
- Verdict: `NOT_READY`
- Score: `85`
- Blocker count: `1`
- Warning count: `0`
- Scene unchanged after inspection: yes

Rendered report excerpt:

```text
NOT READY FOR DELIVERY
Score: 85
1 Blocking Issue(s)
0 Warning(s)
FAIL  01_texture_presence  Texture Presence
Texture Presence: FAIL
1 texture file(s) are missing or unreachable: Missing_Texture.
Affected Objects:
- Cube
```

Conclusion: PASS.

## Scenario C: Generated Texture

Scene setup:

- Created a clean scene with `Cube`.
- Created Blender generated image `Generated_Texture`.
- Assigned it through a node-based material Image Texture node.
- Saved the `.blend` file as `case_c_generated_texture.blend`.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check01 status: `PASS`
- Message: `All referenced textures are packed or reachable.`
- Affected objects: empty list
- Verdict: `READY`
- Score: `100`
- Blocker count: `0`
- Warning count: `0`

Actual result:

- Operator result: `FINISHED`
- Check01 status: `PASS`
- Check01 severity: `BLOCKER`
- Message: `All referenced textures are packed or reachable.`
- Affected objects: empty list
- Image source before inspection: `GENERATED`
- Verdict: `READY`
- Score: `100`
- Blocker count: `0`
- Warning count: `0`
- Scene unchanged after inspection: yes

Rendered report excerpt:

```text
READY FOR DELIVERY
Score: 100
0 Blocking Issue(s)
0 Warning(s)
PASS  01_texture_presence  Texture Presence
Texture Presence: PASS
All referenced textures are packed or reachable.
```

Conclusion: PASS.

## Scenario D: Unsaved Blend

Scene setup:

- Started a new unsaved Blender file with `bpy.ops.wm.read_homefile(use_empty=True)`.
- Created `Cube`.
- Created external PNG: `unsaved_external_texture.png`.
- Assigned the image through a node-based material Image Texture node.
- Did not pack the image.
- Did not save the `.blend` file before inspection.
- Ran inspection with `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check01 status: `WARNING`
- Severity: `WARNING`
- Message: `File is unsaved; texture paths cannot be verified. Save the file and re-run.`
- Affected objects: `Cube`
- Verdict: `READY_WITH_WARNINGS`
- Score: `97`
- Blocker count: `0`
- Warning count: `1`

Actual result:

- Operator result: `FINISHED`
- Check01 status: `WARNING`
- Check01 severity: `WARNING`
- Message: `File is unsaved; texture paths cannot be verified. Save the file and re-run.`
- Affected objects: `Cube`
- Issue reason: `Texture paths cannot be verified while the file is unsaved.`
- Verdict: `READY_WITH_WARNINGS`
- Score: `97`
- Blocker count: `0`
- Warning count: `1`
- `bpy.data.is_saved` before inspection: `False`
- Scene unchanged after inspection: yes

Rendered report excerpt:

```text
READY WITH WARNINGS
Score: 97
0 Blocking Issue(s)
1 Warning(s)
WARN  01_texture_presence  Texture Presence
Texture Presence: WARN
File is unsaved; texture paths cannot be verified. Save the file and re-run.
```

Conclusion: PASS.

## Other Checks During These Runs

The validation focused on Check01.

During all four runs:

- Check02 Material Assignment rendered as `SKIP` / `NOT_IMPLEMENTED`.
- Check03 Applied Scale rendered as `PASS`.
- Check04 UV Existence rendered as `PASS`.
- Check05 Normal Consistency rendered as `SKIP` / `NOT_IMPLEMENTED`.

This kept Check01 isolated for score and verdict validation.

## Final Conclusion

Check01 Texture Presence passed Blender 5.1 runtime validation for the requested scenarios:

- Packed texture: PASS as expected.
- Missing external texture: FAIL as expected.
- Generated texture: PASS as expected.
- Unsaved blend: WARNING as expected.

No source code was modified and no new checks were implemented.
