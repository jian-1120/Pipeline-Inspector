# Pipeline Inspector

Pipeline Inspector is a Blender Pre-Delivery Inspector for 3D assets.

Its long-term product goal is to give artists a clear **READY FOR DELIVERY SCORE** before export, upload, marketplace submission, or client handoff.

## What This Is

Pipeline Inspector is intended to be a final pre-delivery gate for Blender files. It is not positioned as a general modeling assistant or a broad mesh cleanup utility.

The product idea is simple:

- inspect a small set of delivery risks
- show blockers and warnings
- produce a READY FOR DELIVERY score
- help users avoid avoidable rework before sending assets out of Blender

## What This Is Not

Pipeline Inspector is **not Mesh Checker 2**.

It is not trying to become a full mesh validator, topology suite, repair tool, marketplace automation system, engine simulator, or production platform.

The current repository should be understood as a productized early prototype scaffold, not as a usable quality-control product.

## Current Status

Current phase: **Scaffold / Early Prototype**

The repository currently contains:

- research and evidence documents
- MVP definition documents
- architecture and implementation specification documents
- an initial `pipeline_inspector/` Blender add-on scaffold
- five placeholder check modules

The five current check modules are:

1. Texture Presence
2. Material Assignment
3. Applied Scale
4. UV Existence
5. Normal Consistency

Important: these checks are currently placeholders. They return scaffold results and do **not** perform real inspection logic yet.

## Important Limitations

The current version:

- has not implemented real delivery checks
- has not been validated in Blender runtime
- cannot detect real asset problems
- cannot be used to decide whether an asset is ready for delivery
- should not be used for marketplace, client, or production handoff decisions

At this stage, the add-on is only suitable for packaging and Blender load testing.

## Repository Layout

Root-level product documents:

- `MVP_CHECKLIST.md` - MVP delivery check definition
- `MVP_EVIDENCE_MAPPING.md` - evidence mapping for MVP checks
- `TOP_FAILURES.md` - highest-frequency delivery failures
- `MVP_REVIEW_REPORT.md` - MVP evidence review
- `ARCHITECTURE_MVP_V1.md` - locked MVP architecture document
- `IMPLEMENTATION_SPEC_V1.md` - implementation specification for the scaffolded MVP
- `SCAFFOLD_PLAN_V1.md` - scaffold layout and responsibility plan
- `DEVELOPMENT_STATUS.md` - current project status
- `ROADMAP.md` - restrained packaging and real-check roadmap
- `INSTALLATION.md` - current test installation notes

Source scaffold:

- `pipeline_inspector/` - installable Blender add-on folder

Research folders:

- `research/`
- `evidence/`
- `prd/`
- `roadmap/`
- `architecture/`

## Installation Status

See `INSTALLATION.md`.

Current installation is for loading tests only. The current add-on should not be treated as a usable inspection product.

## License

No license file is currently present in this repository.
