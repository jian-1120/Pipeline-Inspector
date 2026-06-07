# CLAUDE.md

This file is the permanent project memory node for Pipeline Inspector.

Future AI agents must read this file before making any changes to the repository.

## 1. Project Identity

Pipeline Inspector is a Blender Pre-Delivery Inspector for 3D assets.

It is not Mesh Checker 2. It is not a broad mesh validator, cleanup suite, repair tool, marketplace automation system, engine simulator, or production platform.

The repository exists to build a narrow delivery-readiness gate for Blender files.

## 2. Project Purpose

Pipeline Inspector's product goal is to produce a clear **READY FOR DELIVERY SCORE** before an artist exports, uploads, submits, or sends a Blender asset.

The product promise is confidence before handoff:

- inspect a small set of delivery risks
- show blockers and warnings
- produce one delivery-readiness verdict and score
- help users avoid preventable rework before assets leave Blender

The MVP question is:

**Is this Blender file safe to leave the creator before export, upload, or client submission?**

## 3. Current Development Phase

Current repository phase: **Scaffold / Early Prototype moving into Runtime Validation**.

Repository-level documentation still marks the project as Scaffold / Early Prototype. The add-on package exists, and a first runtime validation zip has been prepared.

Important current nuance:

- Most check modules remain scaffold placeholders.
- Check 03, Applied Scale, has real read-only logic and a test file in the current repository.
- Blender runtime validation is not complete.
- The project is not usable for real delivery decisions.

## 4. Completed Milestones

Completed:

- Research
- Evidence
- MVP Definition
- Architecture
- Implementation Spec
- Scaffold
- Repository Cleanup
- Runtime validation package preparation
- Applied Scale real check started and covered by repository tests

Relevant documents:

- `README.md`
- `ROADMAP.md`
- `DEVELOPMENT_STATUS.md`
- `ARCHITECTURE_MVP_V1.md`
- `IMPLEMENTATION_SPEC_V1.md`
- `SCAFFOLD_PLAN_V1.md`
- `RUNTIME_VALIDATION.md`

## 5. Remaining Milestones

Remaining:

- Blender load test
- Blender enable/disable test
- N Panel visibility test
- Run Inspection button runtime test
- Placeholder result runtime test
- Console error check
- Finish real checks beyond Applied Scale
- UV Existence real check
- Material / Texture narrow real checks
- Normal warning check
- Update status documentation when runtime validation or real checks actually pass

Do not claim these are complete without fresh verification evidence.

## 6. Product Boundaries

V1 does:

- inspect the currently open Blender file using read-only access
- run a fixed small set of delivery checks
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

The repository evidence and MVP reduction notes explicitly warn against turning this into a broad workflow suite. Pipeline Inspector's role is narrower: it is a pre-delivery readiness gate that reports a small number of delivery risks.

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
- Do not treat placeholder checks as real checks.
- Do not claim Blender runtime validation has passed unless it has actually been tested.
- Do not claim the add-on is production-ready.
- Do not use the current product for real delivery judgment.
- Keep changes small and evidence-aligned.
- When documentation and code disagree, report the disagreement instead of hiding it.

## 9. Current Next Task

The current next task is:

**Run Blender runtime validation on the scaffold package.**

Validation checklist:

- install `PipelineInspector_Scaffold_v0.1.zip`
- enable the add-on
- confirm the Pipeline Inspector tab appears in the N Panel
- confirm the Run Inspection button appears
- click Run Inspection
- verify whether it errors
- verify whether placeholder/current results appear
- check Blender console for errors

After runtime validation, update project status documents only if the test actually passes or fails with evidence.

## 10. Instructions For Future AI Agents

Before changing anything:

1. Read `CLAUDE.md`.
2. Run `git status --short --branch`.
3. Read the relevant source documents for the task.
4. Identify whether the request is documentation, packaging, runtime validation, test work, or implementation.
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
- Include GitHub links if pushed.
- Include `git status` result.
- State any verification that was actually run.
- State what was not verified.

Project truth:

Pipeline Inspector is still early. It has a scaffold, docs, package artifact, and at least one real check in progress, but it is not yet a validated Blender delivery-inspection product.
