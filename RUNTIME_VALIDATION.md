# Runtime Validation Package

Package: `PipelineInspector_Scaffold_v0.1.zip`

Current phase: Scaffold runtime validation.

This package is for Blender add-on load testing only. It does not contain real inspection logic and must not be used for delivery decisions.

## Add-on Structure Check

Expected zip structure:

- `pipeline_inspector/`
- `pipeline_inspector/__init__.py`
- `pipeline_inspector/checks/`
- `pipeline_inspector/ui/`

The zip must contain the `pipeline_inspector` folder at the zip root. Do not zip only the files inside the folder.

## Blender Entry Check

`pipeline_inspector/__init__.py` currently contains:

- `bl_info`
- `register()`
- `unregister()`
- Blender version target: 4.2+
- add-on category: `3D View`
- panel location: `View3D > Sidebar > Pipeline Inspector`

## Blender Installation Steps

1. Open Blender.
2. Go to `Edit > Preferences > Add-ons`.
3. Click `Install`.
4. Select `PipelineInspector_Scaffold_v0.1.zip`.
5. Enable `Pipeline Inspector`.
6. Open the 3D View.
7. Press `N` to open the side panel.
8. Look for the `Pipeline Inspector` tab.

## Blender Test Checklist

Use this checklist during first runtime validation:

- Can the zip be installed?
- Can the add-on be enabled?
- Does `Pipeline Inspector` appear in the N Panel?
- Does the `Run Inspection` button appear?
- Does clicking `Run Inspection` throw any error?
- Does a placeholder result appear after clicking?
- Does the Blender console show any error?

## Expected Result

If the scaffold loads correctly, Blender should show the Pipeline Inspector panel and the Run Inspection button.

The current five checks are placeholders and are expected to return scaffold results. They do not perform real inspection.

## Not Validated Yet

- real check behavior
- asset delivery readiness
- marketplace readiness
- production usability
