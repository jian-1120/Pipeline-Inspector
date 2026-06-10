# Installation

Release package:

```text
PipelineInspector_MVP_v1.0.0.zip
```

Validated with:

```text
Blender 5.1.1
```

## Zip Structure Requirement

The release zip must contain `pipeline_inspector/` directly at the zip root:

```text
pipeline_inspector/
  __init__.py
  checks/
  ui/
  ...
```

The zip must not contain:

- an extra wrapper folder
- `.git`
- `.pytest_cache`
- `docs/archive`
- test files
- old release or runtime zips

## Method A: Blender ZIP Install

Use this method first.

1. Open Blender.
2. Go to `Edit > Preferences > Add-ons`.
3. Click `Install from Disk` or `Install`.
4. Select `PipelineInspector_MVP_v1.0.0.zip`.
5. Enable `Pipeline Inspector`.
6. Close Preferences.
7. Open the 3D Viewport.
8. Press `N` to open the side panel.
9. Open the `Pipeline Inspector` tab.
10. Confirm the `Run Inspection` button appears.

If Blender cannot recognize the zip, use Method B.

## Method B: Manual Folder Install

This is currently one of the most reliable installation methods because some Blender/Windows environments may not correctly recognize add-on zip packages.

1. Extract `PipelineInspector_MVP_v1.0.0.zip`.
2. Find the extracted `pipeline_inspector` folder.
3. Copy the entire `pipeline_inspector` folder.
4. Paste it into Blender's add-ons directory.

Windows example:

```text
C:\Users\<YourName>\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\
```

The final folder should look like:

```text
C:\Users\<YourName>\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\pipeline_inspector\__init__.py
```

Then:

1. Restart Blender.
2. Go to `Edit > Preferences > Add-ons`.
3. Search for `Pipeline Inspector`.
4. Enable the add-on.
5. Open the 3D Viewport.
6. Press `N`.
7. Open the `Pipeline Inspector` tab.

## Run An Inspection

1. Open a `.blend` file.
2. Open `View3D > Sidebar > Pipeline Inspector`.
3. Click `Run Inspection`.
4. Review:
   - verdict
   - score
   - blocking issue count
   - warning count
   - affected objects

Expected clean result:

```text
READY FOR DELIVERY
Score: 100
0 Blocking Issue(s)
0 Warning(s)
```

## Common Issues

### Blender opens the zip instead of installing it

Use Method B and copy the `pipeline_inspector` folder manually into Blender's add-ons directory.

### The add-on does not appear in Preferences

Check that the folder path is exactly:

```text
...\scripts\addons\pipeline_inspector\__init__.py
```

If there is an extra wrapper folder, move `pipeline_inspector` up one level.

### The side panel is hidden

In the 3D Viewport, press `N`, then select the `Pipeline Inspector` tab.

### Blender still runs an older version

Disable and remove the old add-on from Preferences, restart Blender, then install `PipelineInspector_MVP_v1.0.0.zip` again.

### A file reports NOT READY

Review the failing check section and affected object names. Pipeline Inspector does not edit the scene; fixes must be made manually in Blender.
