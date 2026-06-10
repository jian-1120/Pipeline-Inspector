# Roadmap

This roadmap is intentionally restrained. Pipeline Inspector remains a narrow Blender pre-delivery inspector, not a broad asset cleanup or production platform.

## Completed For MVP v1

- Blender add-on registration
- View3D side panel
- `Run Inspection` operator
- READY FOR DELIVERY score
- Check01 Texture Presence
- Check02 Material Assignment
- Check03 Applied Scale
- Check04 UV Existence
- Check05 Normal Consistency
- repository test suite
- Blender 5.1.1 release validation
- MVP v1 release package

## Phase 1: Publish MVP v1

Goal: publish the validated MVP v1 package.

Success condition:

- `PipelineInspector_MVP_v1.0.0.zip` is attached to a GitHub release
- release notes explain the five checks and known limitations
- installation steps match the release asset

## Phase 2: Manual UI Evidence

Goal: capture final manual evidence from Blender UI.

Success condition:

- add-on installs in Blender through Preferences
- `Pipeline Inspector` appears in the N-panel
- `Run Inspection` button is visible
- a sample report is visible in the panel

## Phase 3: Check05 Dogfood

Goal: test Normal Consistency against real assets and measure false positives.

Success condition:

- real asset results are recorded
- false-positive cases are documented
- severity remains evidence-aligned

## Phase 4: v1.1 Decision

Goal: decide whether a v1.1 spec is justified.

Success condition:

- at least one user reports a real issue caught before handoff
- warning noise is acceptable
- user feedback supports continued work

No v1.1 feature should be added without a written scope decision.
