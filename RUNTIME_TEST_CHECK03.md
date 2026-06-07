# Runtime Test Plan: Check 03 Applied Scale

Role: QA Engineer

Scope: manual runtime validation inside Blender 4.2 for Check 03, Applied Scale.

This document is a test plan only. It does not change code, add features, or alter inspection logic.

## Purpose

Verify that Check 03 behaves correctly inside Blender 4.2 when run through the installed Pipeline Inspector add-on.

Check 03 should fail any visible, local mesh object whose `scale` or `delta_scale` differs from `(1, 1, 1)` beyond `SCALE_EPSILON`.

## Source Behavior To Validate

Expected current behavior from `pipeline_inspector/checks/transforms.py` and `pipeline_inspector/scoring.py`:

- Check ID: `03_applied_scale`
- Check name: `Applied Scale`
- Severity: `BLOCKER`
- PASS message: `All mesh objects have applied scale.`
- FAIL message pattern: `N object(s) have unapplied scale: <object names>.`
- One failed blocker deducts 15 points.
- One failed blocker makes the verdict `NOT_READY`.

Important: other checks may still be placeholders or separate runtime targets. This test focuses on Check 03 behavior.

## Installation Steps

1. Open Blender 4.2.
2. Go to `Edit > Preferences > Add-ons`.
3. Click `Install`.
4. Select `PipelineInspector_Scaffold_v0.1.zip`.
5. Enable `Pipeline Inspector`.
6. Open the 3D View.
7. Press `N` to open the side panel.
8. Select the `Pipeline Inspector` tab.
9. Confirm the `Run Inspection` button is visible.

## General Manual Test Procedure

For each scene:

1. Start from a clean Blender file.
2. Create the scene exactly as described.
3. Open the Pipeline Inspector N Panel.
4. Click `Run Inspection`.
5. Record the displayed verdict, score, blocker count, warning count, report text, and affected objects.
6. Check the Blender console for errors.
7. Save screenshots or notes if the result does not match expected behavior.

## Test Scene A: Cube With Applied Scale

### Setup

1. Start with the default cube.
2. Select the cube.
3. Confirm scale is applied:
   - Transform scale should read `1, 1, 1`.
   - If needed, use `Ctrl+A > Apply > Scale`.
4. Keep the cube visible in the current scene.

### Expected Result

Check 03 expected result: `PASS`

Expected Check 03 report:

- Status: `PASS`
- Message: `All mesh objects have applied scale.`
- Affected objects: empty list

Expected overall score behavior:

- If all other checks pass or are placeholders: score should remain `100`.
- Verdict should remain `READY FOR DELIVERY`.
- Blocker count should be `0`.

### Verify

- READY score is displayed.
- Blocker count is `0`.
- Report includes Check 03 as PASS.
- Affected objects list for Check 03 is empty.
- Console shows no error.

## Test Scene B: Cube Scaled 2x Without Ctrl+A

### Setup

1. Start with a clean Blender file.
2. Select the default cube.
3. Scale the cube to 2x using viewport transform or the Transform panel.
4. Do not apply scale.
5. Confirm object scale reads approximately `2, 2, 2`.
6. Keep the cube visible in the current scene.

### Expected Result

Check 03 expected result: `FAIL`

Expected Check 03 report:

- Status: `FAIL`
- Severity: `BLOCKER`
- Message: `1 object(s) have unapplied scale: Cube.`
- Affected objects: `Cube`
- Issue reason: `Object has unapplied scale.`

Expected overall score behavior:

- Score should be `85` if Check 03 is the only failing blocker.
- Verdict should be `NOT READY FOR DELIVERY`.
- Blocker count should be `1`.

### Verify

- NOT_READY score behavior is displayed.
- Blocker count is `1`.
- Report text identifies Applied Scale as failed.
- Affected objects list contains `Cube`.
- Console shows no error.

## Test Scene C: Multiple Meshes Mixed

### Setup

1. Start with a clean Blender file.
2. Create three visible mesh objects:
   - `Cube_Applied`
   - `Cube_Scaled`
   - `Plane_Scaled`
3. For `Cube_Applied`:
   - Scale should be applied.
   - Transform scale should read `1, 1, 1`.
4. For `Cube_Scaled`:
   - Scale to `2, 2, 2`.
   - Do not apply scale.
5. For `Plane_Scaled`:
   - Scale to a non-identity value, for example `0.5, 0.5, 0.5`.
   - Do not apply scale.
6. Keep all three mesh objects visible.

### Expected Result

Check 03 expected result: `FAIL`

Expected Check 03 report:

- Status: `FAIL`
- Severity: `BLOCKER`
- Message: `2 object(s) have unapplied scale: Cube_Scaled, Plane_Scaled.`
- Affected objects:
  - `Cube_Scaled`
  - `Plane_Scaled`
- `Cube_Applied` should not appear in affected objects.

Expected overall score behavior:

- Score should be `85` if Check 03 is the only failing blocker.
- Verdict should be `NOT READY FOR DELIVERY`.
- Blocker count should be `1`.

Note: current scoring counts failed checks, not failed objects. Multiple affected objects inside Check 03 still count as one blocker check.

### Verify

- NOT_READY score behavior is displayed.
- Blocker count is `1`.
- Report text identifies Applied Scale as failed.
- Affected objects list contains `Cube_Scaled` and `Plane_Scaled`.
- Affected objects are sorted alphabetically.
- `Cube_Applied` is not listed as affected.
- Console shows no error.

## Required Verification Points

For every scene, record:

- READY score or NOT_READY score
- numeric score
- blocker count
- warning count
- Check 03 report text
- affected objects list
- Blender console error status

## Manual Validation Checklist

Use this checklist while testing in Blender 4.2:

- Add-on can be installed from zip.
- Add-on can be enabled.
- Pipeline Inspector appears in the N Panel.
- `Run Inspection` button appears.
- Clicking `Run Inspection` does not throw a Python error.
- Test Scene A returns Check 03 PASS.
- Test Scene B returns Check 03 FAIL.
- Test Scene C returns Check 03 FAIL.
- READY / NOT_READY verdict matches expected behavior.
- Numeric score matches expected behavior.
- Blocker count matches expected behavior.
- Report text matches expected behavior.
- Affected objects list matches expected behavior.
- Blender console shows no error.

## Pass / Fail Criteria

Runtime validation passes only if all three test scenes match expected Check 03 behavior and no Blender console errors occur.

If any scene produces an unexpected verdict, score, blocker count, report text, or affected object list, record the mismatch and do not mark Check 03 runtime validation complete.
