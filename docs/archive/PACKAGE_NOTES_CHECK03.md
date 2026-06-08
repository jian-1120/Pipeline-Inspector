# Package Notes: Runtime Check03 v0.1.1

Package: `PipelineInspector_Runtime_Check03_v0.1.1.zip`

Purpose: refresh the Blender runtime validation package from the latest `main` source so Check 03 uses the real Applied Scale logic.

## Why This Package Exists

The old package `PipelineInspector_Scaffold_v0.1.zip` is outdated for Check 03 runtime validation.

That old zip was created during the scaffold phase. Blender installations using that zip may still load placeholder Check03 behavior.

Use `PipelineInspector_Runtime_Check03_v0.1.1.zip` for Check 03 runtime testing.

## Source Used

The new package was generated from the current `pipeline_inspector/` folder on latest `main`.

No source files were modified for this package refresh.

## Zip Verification

The new zip contains:

- `pipeline_inspector/__init__.py`
- `pipeline_inspector/checks/transforms.py`
- `pipeline_inspector/ui/panel.py`
- `pipeline_inspector/ui/operator_run.py`

The `pipeline_inspector/checks/transforms.py` file inside the zip contains:

- `def scale_is_applied(scale, delta_scale)`
- `models.IssueRecord(...)`
- `Object has unapplied scale.`
- failure path through `base.make_fail(...)`

It does not contain the old scaffold text:

- `Scaffold placeholder; returns PASS`

It does not contain a placeholder-only `run(inputs)` implementation.

## Required Blender Reinstall Steps

1. In Blender, disable and remove the old `Pipeline Inspector` add-on.
2. Close Blender.
3. Reopen Blender.
4. Install `PipelineInspector_Runtime_Check03_v0.1.1.zip`.
5. Enable `Pipeline Inspector`.
6. Re-run Check03 runtime tests A/B/C from `RUNTIME_TEST_CHECK03.md`.

## Expected Runtime Validation Focus

Use the new package to verify:

- Test Scene A: applied-scale cube returns PASS.
- Test Scene B: cube scaled 2x without applying scale returns FAIL.
- Test Scene C: mixed meshes return FAIL with only unapplied-scale objects listed.

Do not use `PipelineInspector_Scaffold_v0.1.zip` for Check03 runtime validation.
