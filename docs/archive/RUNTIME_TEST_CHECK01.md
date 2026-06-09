# Runtime Test Plan: Check 01 Texture Presence

Role: QA Engineer

Scope: manual runtime validation inside Blender 4.2 for Check 01, Texture Presence.

This document is a test plan only. It does not change code, add features, or alter inspection logic.

## Purpose

Verify that Check 01 behaves correctly inside Blender 4.2 when run through the installed Pipeline Inspector add-on.

Check 01 should fail any visible, local mesh object whose materials reference a texture image that is neither packed, generated, nor reachable on disk. It should warn when the .blend is unsaved, because `//`-relative paths have no anchor to resolve against. It is read-only: it never mutates the scene and never writes to disk.

## Source Behavior To Validate

Expected current behavior from `pipeline_inspector/checks/textures.py`, `pipeline_inspector/report.py`, and `pipeline_inspector/scoring.py`:

- Check ID: `01_texture_presence`
- Check name: `Texture Presence`
- Severity: `BLOCKER`
- PASS message: `All referenced textures are packed or reachable.`
- FAIL message pattern: `N texture file(s) are missing or unreachable: <image names>.`
- WARNING (unsaved) message: `File is unsaved; texture paths cannot be verified. Save the file and re-run.`
- One failed blocker deducts 15 points (score 85).
- One failed blocker makes the verdict `NOT_READY`.
- A WARNING does not deduct blocker points (it deducts 3 points) and does not make the verdict `NOT_READY`; it yields `READY WITH WARNINGS`.

Classifier rules per referenced image (`image_status`):

- Packed image: PASS (reachable regardless of disk state).
- Generated image (`source == "GENERATED"`): PASS.
- File-backed image (`source` in FILE / TILED / SEQUENCE): PASS only if the file is saved, the resolved path exists, and the image carries pixel data; otherwise FAIL. If the .blend is unsaved, it is unverifiable (routes to WARNING).
- Unknown source: PASS only if it already carries pixel data; otherwise FAIL.

Notes:

- Only `TEX_IMAGE` nodes in node-based materials are inspected. Procedural-only materials, materials with `use_nodes` off, and empty material slots contribute nothing and are never flagged.
- Affected objects are deduped, sorted alphabetically, and capped at 50 names with an overflow note.
- A FAIL on an object takes precedence over an unsaved WARNING for that same object.

Important: other checks may still be placeholders or separate runtime targets. This test focuses on Check 01 behavior.

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

## Test Scene A: Cube With Packed Texture

### Setup

1. Start with the default cube.
2. Give the cube a node-based material with an Image Texture node.
3. Load any image into the Image Texture node.
4. Pack the image: `File > External Data > Pack Resources`.
5. Save the .blend file.
6. Keep the cube visible in the current scene.

### Expected Result

Check 01 expected result: `PASS`

Expected Check 01 report:

- Status: `PASS`
- Message: `All referenced textures are packed or reachable.`
- Affected objects: empty list

Expected overall score behavior:

- If all other checks pass or are placeholders: score should remain `100`.
- Verdict should remain `READY FOR DELIVERY`.
- Blocker count should be `0`.

### Verify

- READY score is displayed.
- Blocker count is `0`.
- Report includes Check 01 as PASS.
- Affected objects list for Check 01 is empty.
- Console shows no error.

## Test Scene B: Cube With Missing On-Disk Texture

### Setup

1. Start with a clean Blender file.
2. Give the default cube a node-based material with an Image Texture node.
3. Load an external image from disk (do not pack it).
4. Save the .blend file.
5. Outside Blender, delete or rename the referenced image file so the path no longer resolves.
6. Keep the cube visible in the current scene.

### Expected Result

Check 01 expected result: `FAIL`

Expected Check 01 report:

- Status: `FAIL`
- Severity: `BLOCKER`
- Message: `1 texture file(s) are missing or unreachable: <image name>.`
- Affected objects: `Cube`
- Issue reason: `Material references missing or unreachable texture(s).`

Expected overall score behavior:

- Score should be `85` if Check 01 is the only failing blocker.
- Verdict should be `NOT READY FOR DELIVERY`.
- Blocker count should be `1`.

### Verify

- NOT_READY score behavior is displayed.
- Blocker count is `1`.
- Report text identifies Texture Presence as failed.
- Affected objects list contains `Cube`.
- The missing image name appears in the report message.
- Console shows no error.

## Test Scene C: Unsaved File With File Texture

### Setup

1. Start with a clean Blender file. Do not save it.
2. Give the default cube a node-based material with an Image Texture node.
3. Load an external image from disk (do not pack it).
4. Leave the .blend unsaved.
5. Keep the cube visible in the current scene.

### Expected Result

Check 01 expected result: `WARNING`

Expected Check 01 report:

- Status: `WARN`
- Severity: `WARNING`
- Message: `File is unsaved; texture paths cannot be verified. Save the file and re-run.`
- Affected objects: `Cube`

Expected overall score behavior:

- Score should be `97` if Check 01 is the only non-passing check (a WARNING deducts 3 points).
- Verdict should be `READY WITH WARNINGS`.
- Blocker count should be `0`.
- Warning count should be `1`.

### Verify

- Blocker count is `0`.
- Warning count is `1`.
- Report text identifies Texture Presence as a warning.
- The unsaved-file message is shown.
- Console shows no error.

## Test Scene D: Procedural And Generated Only

### Setup

1. Start with a clean Blender file.
2. Create two visible mesh objects:
   - `Cube_Procedural`
   - `Cube_Generated`
3. For `Cube_Procedural`:
   - Give it a node-based material that uses only procedural nodes (for example a Noise Texture driving the shader). No Image Texture node.
4. For `Cube_Generated`:
   - Give it a node-based material with an Image Texture node whose image is a Blender-generated image (`source == GENERATED`), for example a new generated grid image.
5. Save the .blend file.
6. Keep both objects visible.

### Expected Result

Check 01 expected result: `PASS`

Expected Check 01 report:

- Status: `PASS`
- Message: `All referenced textures are packed or reachable.`
- Affected objects: empty list

Expected overall score behavior:

- Score should remain `100` if Check 01 is the only relevant check.
- Verdict should remain `READY FOR DELIVERY`.
- Blocker count should be `0`.

### Verify

- READY score is displayed.
- Blocker count is `0`.
- Neither object is listed as affected.
- Console shows no error.

## Required Verification Points

For every scene, record:

- READY score or NOT_READY score
- numeric score
- blocker count
- warning count
- Check 01 report text
- affected objects list
- Blender console error status

## Manual Validation Checklist

Use this checklist while testing in Blender 4.2:

- Add-on can be installed from zip.
- Add-on can be enabled.
- Pipeline Inspector appears in the N Panel.
- `Run Inspection` button appears.
- Clicking `Run Inspection` does not throw a Python error.
- Test Scene A returns Check 01 PASS.
- Test Scene B returns Check 01 FAIL.
- Test Scene C returns Check 01 WARNING.
- Test Scene D returns Check 01 PASS.
- READY / NOT_READY / WARNINGS verdict matches expected behavior.
- Numeric score matches expected behavior.
- Blocker count matches expected behavior.
- Warning count matches expected behavior.
- Report text matches expected behavior.
- Affected objects list matches expected behavior.
- The scene is not mutated by running the inspection.
- Blender console shows no error.

## Pass / Fail Criteria

Runtime validation passes only if all four test scenes match expected Check 01 behavior and no Blender console errors occur.

If any scene produces an unexpected verdict, score, blocker count, warning count, report text, or affected object list, record the mismatch and do not mark Check 01 runtime validation complete.
