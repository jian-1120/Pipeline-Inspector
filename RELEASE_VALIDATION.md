# Release Validation

Date: 2026-06-10

Branch: `main`

Commit: `fe2963ea3b2c296657581d2ab7a4ccdccc0ffa26`

Scope: validate whether current `main` can be used as the Pipeline Inspector MVP v1 release candidate.

This validation did not implement new features and did not modify detection logic.

## Summary

Release validation result: PASS.

Functional MVP v1 package status: releasable as an MVP v1 candidate.

## Release Package

Package built from current `main`:

```text
PipelineInspector_MVP_v1.0.0.zip
```

Package size:

```text
18390 bytes
```

Zip structure validation:

- top-level folder: `pipeline_inspector`
- `pipeline_inspector/__init__.py`: present
- backslash paths inside zip: none
- extra wrapper folder: none
- `__pycache__` / `.pyc` files: excluded

First entries:

```text
pipeline_inspector/__init__.py
pipeline_inspector/checks/__init__.py
pipeline_inspector/checks/base.py
pipeline_inspector/checks/materials.py
pipeline_inspector/checks/normals.py
pipeline_inspector/checks/textures.py
pipeline_inspector/checks/transforms.py
pipeline_inspector/checks/uvs.py
pipeline_inspector/constants.py
pipeline_inspector/inspector.py
pipeline_inspector/models.py
pipeline_inspector/report.py
pipeline_inspector/scoring.py
pipeline_inspector/state.py
pipeline_inspector/ui/__init__.py
pipeline_inspector/ui/operator_run.py
pipeline_inspector/ui/panel.py
```

## Clean Install Environment

Blender executable:

```text
D:\ProgramData\blender.exe
```

Blender version:

```text
5.1.1
```

Install result:

- `bpy.ops.preferences.addon_install`: `FINISHED`
- `bpy.ops.preferences.addon_enable`: `FINISHED`
- Blender process exit code: `0`

## Registration Validation

Registered check count: 5.

Registered check IDs:

```text
01_texture_presence
02_material_assignment
03_applied_scale
04_uv_existence
05_normal_consistency
```

Operator registration:

- registered: yes
- operator idname: `pipeline_inspector.run`
- operator label: `Run Inspection`

Panel registration:

- registered: yes
- panel idname: `PIPELINE_INSPECTOR_PT_panel`
- space type: `VIEW_3D`
- region type: `UI`
- N-panel tab/category: `Pipeline Inspector`
- panel label: `Pipeline Inspector`

UI validation note:

This validation confirmed Blender panel and operator registration data in a clean add-on install. Manual screenshot evidence is still recommended before broad public announcement.

## Repository Test Result

Command:

```text
python -m pytest
```

Result:

```text
137 passed
```

## Functional Validation

Inspection was executed through:

```text
bpy.ops.pipeline_inspector.run()
```

### Case 1: Normal Model

Setup:

- one clean mesh object
- valid material
- valid UV map
- applied scale
- consistent face winding

Expected and actual:

- Check01: PASS
- Check02: PASS
- Check03: PASS
- Check04: PASS
- Check05: PASS
- Verdict: READY
- Score: 100

Result: PASS.

### Case 2: Missing Texture Model

Setup:

- one mesh object
- valid material and UV
- image texture node references a file that was deleted after saving the `.blend`

Expected and actual:

- Check01 Texture Presence: FAIL
- affected object: `Missing_Texture_Model`
- other checks: PASS
- Verdict: NOT_READY
- Score: 85
- blocker count: 1

Result: PASS.

### Case 3: Unapplied Scale Model

Setup:

- one mesh object
- valid material and UV
- object scale set to `(2, 2, 2)` without applying scale

Expected and actual:

- Check03 Applied Scale: FAIL
- affected object: `Unapplied_Scale_Model`
- reported scale: `X: 2.0`, `Y: 2.0`, `Z: 2.0`
- other checks: PASS
- Verdict: NOT_READY
- Score: 85
- blocker count: 1

Result: PASS.

### Case 4: No UV Model

Setup:

- one mesh object
- valid material
- no UV map
- applied scale
- consistent face winding

Expected and actual:

- Check04 UV Existence: FAIL
- affected object: `No_UV_Model`
- other checks: PASS
- Verdict: NOT_READY
- Score: 85
- blocker count: 1

Result: PASS.

### Case 5: Normal Error Model

Setup:

- one mesh object
- valid material and UV
- face winding intentionally inconsistent across a shared manifold edge

Expected and actual:

- Check05 Normal Consistency: FAIL
- affected object: `Bad_Normals`
- reason: `Inconsistent face winding within a manifold component.`
- other checks: PASS
- Verdict: NOT_READY
- Score: 85
- blocker count: 1

Result: PASS.

## Bug List

Blocking bugs found during release validation: none.

Non-blocking notes:

- Blender emitted a `Material.use_nodes` deprecation warning while the validation script created test materials. This did not stop execution and did not affect inspection results.
- Manual viewport screenshot evidence is still recommended before broad public announcement.

## Release Decision

MVP v1 functional release validation: PASS.

Current `main` can be treated as the MVP v1 release candidate for functional validation purposes.
