# Pipeline Inspector

**Blender pre-delivery inspection add-on**

Pipeline Inspector helps artists check common asset delivery problems before export, upload, marketplace submission, or client handoff. It runs inside Blender and produces a single **READY FOR DELIVERY** score with blockers, warnings, and affected object names.

Current version: **v1.0.0 MVP**

Validated with: **Blender 5.1.1**

## Why It Exists 🎯

3D assets often fail delivery for simple reasons: missing textures, empty materials, unapplied scale, missing UVs, or inconsistent face winding. Pipeline Inspector is a small pre-delivery gate for those risks.

It is not a broad mesh cleanup suite, repair tool, cloud service, or engine simulator. It is a focused inspection add-on for deciding whether a Blender file is ready to leave the creator.

## Features ✨

- READY FOR DELIVERY score
- Blocking and warning counts
- Five focused delivery checks
- Affected object list
- One-click manual inspection
- Viewport side-panel report
- Read-only behavior: it does not modify the scene

## MVP Checks 🔍

| Check | Name | What It Catches |
|---|---|---|
| 01 | Texture Presence | Missing or unreachable referenced image textures |
| 02 | Material Assignment | Missing, empty, legacy, or disconnected material assignment |
| 03 | Applied Scale | Mesh objects with Object Mode scale not equal to `1,1,1` |
| 04 | UV Existence | Mesh objects with no usable UV map |
| 05 | Normal Consistency | Internally inconsistent face winding in manifold mesh components |

## READY FOR DELIVERY Score ✅

Pipeline Inspector starts each run at 100.

- `READY FOR DELIVERY`: no blocking failures
- `READY WITH WARNINGS`: no blocking failures, but warnings exist
- `NOT READY FOR DELIVERY`: one or more blocking checks failed

The score is a delivery-readiness signal. It is not a general art-quality score.

## Screenshot

UI screenshot placeholder:

```text
docs/screenshots/pipeline-inspector-v1-ui.png
```

Add a screenshot at that path when preparing the public GitHub page or marketplace listing.

## Installation 📦

Download the release package:

```text
PipelineInspector_MVP_v1.0.0.zip
```

Start with Blender's ZIP installer. If Blender cannot recognize the zip on your system, use the manual folder-copy method.

See [INSTALLATION.md](INSTALLATION.md) for full installation and troubleshooting steps.

## Usage ▶️

1. Open a `.blend` file.
2. In the 3D Viewport, press `N` to open the side panel.
3. Open the `Pipeline Inspector` tab.
4. Click `Run Inspection`.
5. Review the verdict, score, failed checks, warnings, and affected objects.

Pipeline Inspector reports problems only. It does not auto-fix or edit your scene.

## Current Limitations

- Does not repair assets automatically
- Does not simulate Unity, Unreal, Godot, or marketplace import behavior
- Does not validate shader quality, PBR correctness, texture resolution, UV layout quality, or texel density
- Does not inspect licensing, thumbnails, product descriptions, or documentation
- Check05 is conservative and should be dogfooded on real production assets

## Roadmap 🗺️

Short-term:

1. Publish GitHub Release `v1.0.0`
2. Attach `PipelineInspector_MVP_v1.0.0.zip`
3. Add UI screenshots under `docs/screenshots/`
4. Prepare Superhive / marketplace listing materials
5. Dogfood Check05 Normal Consistency on real assets

Not planned for MVP v1:

- AI analysis
- cloud services
- auto-fix
- team features
- broad mesh cleanup
- engine import simulation

## Release Status

- Five MVP checks implemented
- `137` repository tests passing
- Blender 5.1.1 runtime validation passed
- Release package prepared: `PipelineInspector_MVP_v1.0.0.zip`

## Author

GitHub: [jian-1120/Pipeline-Inspector](https://github.com/jian-1120/Pipeline-Inspector)

## License

No license file is currently present in this repository.
