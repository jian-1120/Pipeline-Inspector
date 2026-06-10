# Pipeline Inspector v1.0.0 MVP

Release package:

```text
PipelineInspector_MVP_v1.0.0.zip
```

## Summary

Pipeline Inspector v1.0.0 MVP is a Blender pre-delivery inspection add-on. It checks common asset handoff issues before export, upload, marketplace submission, or client delivery.

## Features

- READY FOR DELIVERY score
- Blocking and warning counts
- Five focused delivery checks
- Affected object reporting
- Viewport side-panel report
- Manual `Run Inspection` action
- Read-only inspection behavior

## Checks Included

1. **Texture Presence**
   - Detects missing or unreachable referenced image textures.

2. **Material Assignment**
   - Detects missing, empty, legacy, or disconnected material assignment.

3. **Applied Scale**
   - Detects mesh objects whose Object Mode scale is not `1,1,1`.

4. **UV Existence**
   - Detects mesh objects with no usable UV map.

5. **Normal Consistency**
   - Detects internally inconsistent face winding in manifold mesh components.

## Validation

- `137` tests passed
- Blender `5.1.1` runtime validated
- Release validation passed
- Clean install validation passed
- Five scene cases validated:
  - normal model
  - missing texture model
  - unapplied scale model
  - no UV model
  - normal consistency failure model

## Installation Note

Start with Blender ZIP install:

1. `Edit > Preferences > Add-ons`
2. `Install from Disk`
3. Select `PipelineInspector_MVP_v1.0.0.zip`
4. Enable `Pipeline Inspector`

If ZIP install fails, use the manual install method:

1. Extract the zip.
2. Find the `pipeline_inspector` folder.
3. Copy the whole folder into Blender's add-ons directory.
4. Restart Blender.
5. Enable `Pipeline Inspector` in Preferences.

Windows add-ons path example:

```text
C:\Users\<YourName>\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\
```

## Known Limitations

- Does not repair scenes automatically
- Does not simulate Unity, Unreal, Godot, or marketplace import behavior
- Does not validate shader quality, texture resolution, UV layout quality, texel density, licensing, thumbnails, or documentation
- Check05 is conservative and should be tested on real production assets
- Manual UI screenshot evidence is still recommended for marketplace listing materials

## Release Decision

Pipeline Inspector v1.0.0 MVP is ready for GitHub release publication.
