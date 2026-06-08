# Runtime Validation Evidence

Date: 2026-06-09

Role: Runtime Operator

Project root:

`C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector`

Package tested:

`C:\Users\简某\Desktop\AI\Pipeline Inspector总\Pipeline-Inspector\PipelineInspector_Runtime_Check03_v0.1.1.zip`

## Environment

- Blender executable: `D:\ProgramData\blender.exe`
- Blender version: `5.1.1`
- Platform: `win32`
- Runtime mode: Blender launched with `--factory-startup --background`
- Add-on install method: `bpy.ops.preferences.addon_install(filepath=..., overwrite=True)`
- Add-on enable method: `bpy.ops.preferences.addon_enable(module="pipeline_inspector")`
- Run Inspection method: `bpy.ops.pipeline_inspector.run()`
- Screenshots: not available; validation was executed in Blender background runtime.
- Console result: Blender process completed without Python traceback in stdout/stderr.

Install / enable checks:

- Add-on install invoked: yes
- Add-on enable invoked: yes
- `pipeline_inspector` module imported: yes
- `bl_info` exists: yes
- `register()` exists: yes
- `unregister()` exists: yes
- `pipeline_inspector.run` operator exists: yes

## Summary

| Case | Check | Expected | Actual | Passed |
| --- | --- | --- | --- | --- |
| 1 | Check03 Applied Scale | PASS | PASS | yes |
| 2 | Check03 Applied Scale | FAIL | FAIL | yes |
| 3 | Check03 Applied Scale | PASS | PASS | yes |
| 4 | Check04 UV Existence | FAIL | PASS placeholder | no |
| 5 | Check04 UV Existence | PASS | PASS placeholder | yes, but not validating |
| 6 | Check04 UV Existence | FAIL | PASS placeholder | no |

## Case 1: Check03 Default Cube

Operations performed:

- Started from Blender factory startup/background session.
- Created default cube named `Cube`.
- Object Scale was `1,1,1`.
- Ran inspection via `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check03: `PASS`

Actual result:

- Operator result: `FINISHED`
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`
- Check03 status: `PASS`
- Check03 message: `All mesh objects have applied scale.`
- Affected objects: none
- Scene unchanged after inspection: yes

Rendered report excerpt:

```text
READY FOR DELIVERY
Score: 100
0 Blocking Issue(s)
0 Warning(s)
PASS  03_applied_scale  Applied Scale
```

Case result: PASS

## Case 2: Check03 Cube Scaled 2x Without Apply

Operations performed:

- Started from Blender factory startup/background session.
- Created default cube named `Cube`.
- Set Object Mode scale to `2.0` on X/Y/Z.
- Did not apply scale.
- Ran inspection via `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check03: `FAIL`

Actual result:

- Operator result: `FINISHED`
- Verdict: `NOT_READY`
- Score: `85`
- Blocking Issue(s): `1`
- Warning(s): `0`
- Check03 status: `FAIL`
- Check03 message: `1 object(s) have unapplied scale: Cube.`
- Affected objects: `Cube`
- Issue reason: `Object has unapplied scale.`
- Issue detail: `scale=(2.0000, 2.0000, 2.0000) delta_scale=(1.0000, 1.0000, 1.0000)`
- Scene unchanged after inspection: yes

Rendered report excerpt:

```text
NOT READY FOR DELIVERY
Score: 85
1 Blocking Issue(s)
0 Warning(s)
FAIL  03_applied_scale  Applied Scale
```

Case result: PASS

## Case 3: Check03 Cube Scaled 2x Then Apply Scale

Operations performed:

- Started from Blender factory startup/background session.
- Created default cube named `Cube`.
- Set Object Mode scale to `2.0` on X/Y/Z.
- Applied scale using `bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)`, equivalent to `Ctrl+A > Apply Scale`.
- Ran inspection via `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check03: `PASS`

Actual result:

- Operator result: `FINISHED`
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`
- Check03 status: `PASS`
- Check03 message: `All mesh objects have applied scale.`
- Affected objects: none
- Scene unchanged after inspection: yes

Rendered report excerpt:

```text
READY FOR DELIVERY
Score: 100
0 Blocking Issue(s)
0 Warning(s)
PASS  03_applied_scale  Applied Scale
```

Case result: PASS

## Case 4: Check04 Suzanne With No UV

Operations performed:

- Started from Blender factory startup/background session.
- Created Suzanne mesh named `Suzanne` with `bpy.ops.mesh.primitive_monkey_add`.
- Removed all UV maps.
- Confirmed before inspection:
  - `uv_layer_count`: `0`
  - `uv_layers`: none
  - `active_uv`: none
- Ran inspection via `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check04: `FAIL`

Actual result:

- Operator result: `FINISHED`
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`
- Check04 status: `PASS`
- Check04 message: `Placeholder PASS — check not yet implemented.`
- Affected objects: none
- Scene unchanged after inspection: yes

Rendered report excerpt:

```text
READY FOR DELIVERY
Score: 100
0 Blocking Issue(s)
0 Warning(s)
PASS  04_uv_existence  UV Existence
```

Case result: FAIL

## Case 5: Check04 Suzanne With Valid UV

Operations performed:

- Started from Blender factory startup/background session.
- Created Suzanne mesh named `Suzanne` with `bpy.ops.mesh.primitive_monkey_add`.
- Removed all existing UV maps.
- Created active UV map `UVMap` with `1968` loop UV values.
- Ran inspection via `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check04: `PASS`

Actual result:

- Operator result: `FINISHED`
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`
- Check04 status: `PASS`
- Check04 message: `Placeholder PASS — check not yet implemented.`
- Affected objects: none
- Scene unchanged after inspection: yes

Rendered report excerpt:

```text
READY FOR DELIVERY
Score: 100
0 Blocking Issue(s)
0 Warning(s)
PASS  04_uv_existence  UV Existence
```

Case result: PASS for expected status, but not valid evidence of real UV logic because runtime Check04 is still placeholder.

## Case 6: Check04 Mixed Scene With One UV Mesh And One No-UV Mesh

Operations performed:

- Started from Blender factory startup/background session.
- Created `Cube_With_UV` with active UV map `UVMap` and `24` loop UV values.
- Created `Cube_No_UV`.
- Removed all UV maps from `Cube_No_UV`.
- Confirmed before inspection:
  - `Cube_With_UV` UV layer count: `1`
  - `Cube_No_UV` UV layer count: `0`
- Ran inspection via `bpy.ops.pipeline_inspector.run()`.

Expected result:

- Check04: `FAIL`
- Affected object should include `Cube_No_UV`.

Actual result:

- Operator result: `FINISHED`
- Verdict: `READY`
- Score: `100`
- Blocking Issue(s): `0`
- Warning(s): `0`
- Check04 status: `PASS`
- Check04 message: `Placeholder PASS — check not yet implemented.`
- Affected objects: none
- Scene unchanged after inspection: yes

Rendered report excerpt:

```text
READY FOR DELIVERY
Score: 100
0 Blocking Issue(s)
0 Warning(s)
PASS  04_uv_existence  UV Existence
```

Case result: FAIL

## Unexpected Behavior

Runtime Check04 is still placeholder in the installed package.

Evidence from runtime:

- `04_uv_existence` returned `PASS` for Suzanne with `0` UV layers.
- `04_uv_existence` returned `PASS` for mixed scene where `Cube_No_UV` had `0` UV layers.
- `04_uv_existence` message was `Placeholder PASS — check not yet implemented.`
- No affected objects were listed for Check04 failure scenarios.

Additional runtime package observation:

- `pipeline_inspector/checks/uvs.py` inside `PipelineInspector_Runtime_Check03_v0.1.1.zip` contains placeholder Check04 logic.
- Therefore Check04 cannot be considered runtime-validated by this package.

Placeholder behavior also appeared for:

- `01_texture_presence`: `PASS`, message `Placeholder PASS — check not yet implemented.`
- `02_material_assignment`: `PASS`, message `Placeholder PASS — check not yet implemented.`
- `05_normal_consistency`: `PASS`, message `Placeholder PASS — check not yet implemented.`

## Final Judgment

- Check03 Applied Scale runtime validation: PASS.
- Check04 UV Existence runtime validation: FAIL.
- Add-on installation and enable path: PASS in Blender 5.1.1 background runtime.
- Run Inspection operator: PASS, returned `FINISHED` in all six cases.
- Read-only behavior: PASS, object scale and UV layer snapshots were unchanged after inspection in all six cases.
- Console: no Python traceback observed in Blender stdout/stderr.
