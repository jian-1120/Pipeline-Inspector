# CLAUDE.md

This file is the permanent project memory node for Pipeline Inspector.

Future AI agents must read this file before making changes to the repository.

## 1. Project Identity

Pipeline Inspector is a Blender Pre-Delivery Inspector for 3D assets.

It is not Mesh Checker 2. It is not a broad mesh validator, cleanup suite, repair tool, marketplace automation system, engine simulator, or production platform.

The repository exists to build and maintain a narrow delivery-readiness gate for Blender files.

## 2. Project Purpose

Pipeline Inspector produces a clear **READY FOR DELIVERY SCORE** before an artist exports, uploads, submits, or sends a Blender asset.

The product promise is confidence before handoff:

- inspect a small set of delivery risks
- show blockers and warnings
- produce one delivery-readiness verdict and score
- help users avoid preventable rework before assets leave Blender

The MVP question is:

**Is this Blender file safe to leave the creator before export, upload, or client submission?**

## 3. Current Development Phase

Current repository phase: **MVP v1 release candidate**.

Current implementation status:

- all five MVP checks are implemented
- repository tests pass
- release package has been built
- Blender 5.1.1 clean-install runtime validation has passed
- GitHub release publication is still pending

The project is ready for release preparation and publication work. It is not a request to add new checks or product scope.

## 4. Completed Milestones

Completed:

- Research
- Evidence
- MVP Definition
- Architecture
- Implementation Spec
- Add-on registration and panel shell
- Check 01 Texture Presence
- Check 02 Material Assignment
- Check 03 Applied Scale
- Check 04 UV Existence
- Check 05 Normal Consistency
- Repository tests
- Release package build
- Blender 5.1.1 runtime validation
- Release readiness documentation

Relevant current documents:

- `README.md`
- `INSTALLATION.md`
- `ROADMAP.md`
- `DEVELOPMENT_STATUS.md`
- `PROJECT_STATUS.md`
- `MVP_PROGRESS.md`
- `RELEASE_VALIDATION.md`
- `RELEASE_READY_REPORT.md`
- `RELEASE_NOTES_v1.0.0.md`

## 5. Remaining Milestones

Remaining release tasks:

- publish GitHub release notes
- attach `PipelineInspector_MVP_v1.0.0.zip` to the GitHub release
- capture optional manual Blender UI screenshot evidence
- dogfood Check05 Normal Consistency on real production assets
- collect user feedback before considering any v1.1 scope

## 6. Product Boundaries

V1 does:

- inspect the currently open Blender file using read-only access
- run a fixed set of five delivery checks
- produce one `InspectionResult`
- produce a READY FOR DELIVERY score and verdict
- show blockers and warnings in a single Blender side panel
- allow one manual `Run Inspection` action

V1 does not:

- mutate the user's scene
- repair anything automatically
- simulate Unity, Unreal, Godot, or any other downstream engine
- validate marketplace descriptions, screenshots, licensing, or documentation
- provide broad mesh quality scoring
- provide UV stretch, overlap, packing, or texel density analysis
- provide shader/PBR quality review
- introduce background timers, save handlers, or auto-run export hooks
- add settings panels, presets, configurable thresholds, or per-project rule files
- add account, telemetry, remote storage, collaboration, or platform features

If a proposed feature is not in `IMPLEMENTATION_SPEC_V1.md` Section 2, it is not in v1.

## 7. Relationship With FUM

Pipeline Inspector must not become a FUM replacement.

Pipeline Inspector's role is narrow: it is a pre-delivery readiness gate that reports a small number of delivery risks.

If FUM exists as a broader workflow, marketplace, cleanup, or production-management tool, Pipeline Inspector should remain complementary rather than competitive:

- Pipeline Inspector checks readiness before handoff.
- Pipeline Inspector does not replace broader asset-management or production workflows.
- Pipeline Inspector does not expand into a general studio pipeline system.

## 8. Non-Negotiable Rules

Future agents must follow these rules:

- Read `CLAUDE.md` before making changes.
- Do not add new product scope without explicit user approval.
- Do not implement features outside `IMPLEMENTATION_SPEC_V1.md`.
- Do not mutate Blender scenes in v1 checks.
- Do not add auto-repair behavior.
- Do not add cloud, account, telemetry, collaboration, or platform behavior.
- Do not add broad mesh checker behavior.
- Do not add engine import simulation.
- Do not add marketplace compliance automation.
- Do not claim production readiness beyond the evidence in release validation.
- Keep changes small and evidence-aligned.
- When documentation and code disagree, report the disagreement instead of hiding it.

## 9. Current Next Task

The current next task is:

**Publish MVP v1 release materials.**

Release checklist:

- confirm `PipelineInspector_MVP_v1.0.0.zip` is the only current release zip
- confirm README and installation instructions match the release package
- create GitHub release notes from `RELEASE_NOTES_v1.0.0.md`
- attach the zip to the GitHub release
- verify the release link and asset download

## 10. Instructions For Future AI Agents

Before changing anything:

1. Read `CLAUDE.md`.
2. Run `git status --short --branch`.
3. Read the relevant source documents for the task.
4. Identify whether the request is documentation, packaging, runtime validation, release publication, test work, or implementation.
5. Keep the change inside the requested phase.

When editing:

- Use the existing module structure.
- Avoid broad refactors.
- Do not touch unrelated files.
- Do not rewrite architecture or implementation specs unless explicitly asked.
- Do not silently overwrite user changes.
- Stage only files that belong to the requested task.

When reporting completion:

- Include changed files.
- Include commit hash if committed.
- Include GitHub links if pushed or released.
- Include `git status` result.
- State any verification that was actually run.
- State what was not verified.

Project truth:

Pipeline Inspector has an MVP v1 release candidate with five implemented checks, passing tests, and Blender 5.1.1 release validation. Future work should focus on release publication, evidence collection, and tightly scoped maintenance unless the user explicitly authorizes new scope.
