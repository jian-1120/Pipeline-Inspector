# ARCHITECTURE MVP v1

Role: Blender Add-on Technical Architect.

Phase: Architecture Phase. No code, no Blender plugin files, no Python implementation, no UI design beyond the minimum needed to describe data flow.

Purpose: assess MVP v1 technical feasibility and propose the smallest credible architecture for a Blender Pre-Delivery Inspector that produces a READY FOR DELIVERY SCORE.

Sources used:

- `README.md`
- `MVP_CHECKLIST.md`
- `MVP_EVIDENCE_MAPPING.md`
- `TOP_FAILURES.md`
- `MVP_REVIEW_REPORT.md`
- `research/pain-points.md`
- `prd/product-requirements.md`
- `prd/mvp-definition.md`
- `evidence/real-failure-database.md`
- `evidence/pain-analysis.md`
- `evidence/payment-evidence.md`
- `evidence/go-no-go-report.md`
- `evidence/mvp-reduction.md`

Framing: Pipeline Inspector is not Mesh Checker 2. It is a Pre-Delivery Inspector. The MVP must answer one question: "Is this Blender file safe to leave the creator before export, upload, or client submission?" Anything outside that question is out of scope for v1.

---

## 1. Product Boundary

### MVP v1 does

- Inspect the currently open Blender file using read-only access to `bpy.data` and `bpy.context`.
- Run a small fixed set of pre-delivery checks against scene objects.
- Produce a single READY FOR DELIVERY SCORE (0-100) plus a structured list of blockers and warnings.
- Surface each issue with a short reason and the affected object names so the user can fix it manually.
- Provide a single "Run Inspection" entry point and a result panel. Nothing else.

### MVP v1 does not do

The following are explicitly excluded from v1 and must not be designed, scaffolded, or stubbed in the architecture:

- AI analysis or LLM-based suggestions.
- Cloud reports, remote storage, accounts, or SaaS workflows.
- Auto-fix or any action that mutates the user's scene.
- Team collaboration, shared rule sets, or multi-user features.
- Studio pipeline systems, asset databases, dependency graphs across files.
- Full texture quality review (color space heuristics, resolution policy, channel packing rules, texel density).
- Full shader/material quality review (node graph audit, PBR correctness, shader complexity).
- Full marketplace compliance system (description text, preview images, licensing, documentation).
- Full engine export validation (Unity/Unreal import simulation, engine-specific presets).
- N-gon counters, topology quality scoring, retopology hints, UV stretch/overlap analysis, naming convention enforcement, collection organization rules.

This boundary is enforced by evidence:

- `evidence/mvp-reduction.md` recommends deleting AI, cloud, team features, auto-fix, broad texture validation, full geometry validation, and marketplace documentation checks from v1.
- `evidence/payment-evidence.md` shows users pay for *outcomes* (reduced rework, fewer rejections) at a $5-$15 anchor, not for "professional QA suites."
- `evidence/go-no-go-report.md` returns GO only for a narrow validation MVP, explicitly Not Approved for broad plugins, AI, cloud, team, auto-fix, or engine-specific expansion.

If a feature does not directly raise or lower the delivery-readiness verdict, it does not belong in v1.

---

## 2. Technical Feasibility Table

The proposed inputs are the six core checks named in the brief. Each row is judged against Blender's documented Python data model (`bpy.data.objects`, `bpy.data.images`, `Mesh`, `MeshUVLoopLayer`, `Object.matrix_world`, `Object.scale`/`rotation_euler`, `Material.use_nodes`, `Image.filepath`/`packed_file`/`source`, `Image.has_data`, mesh polygon normals).

| # | Check | Blender API Feasible? | Required Blender Data | Implementation Difficulty | Speed Risk | False-Positive Risk | Suitable for MVP v1? | Recommendation |
|---:|---|---|---|---|---|---|---|---|
| 1 | Texture files are present, packed, or reachable | Yes | `bpy.data.images`: `packed_file`, `filepath_raw`/`filepath`, `source`, `has_data`; for each `Material` with `use_nodes`, walk `node_tree.nodes` of type `TEX_IMAGE` and read `image` | Low-Medium | Low. Image count is typically small (tens). File-existence check is one `os.path.exists` per non-packed image. | Medium. Relative paths, `//` blend-relative paths, and UDIM tiles need careful resolution; otherwise valid setups can look broken. | Yes, narrowly scoped to presence/packed/reachable, not quality | Keep |
| 2 | Materials are assigned and export-relevant | Yes | `Object.material_slots` (slot.material, slot.link), `Material.use_nodes`, output node connectivity, image texture nodes that feed surface input | Low | Low. Linear over selected mesh objects. | Medium. "Export-relevant" must be defined as a concrete predicate (slot has a material, material has a connected surface output, at least one image texture is reachable) or false-positives become a bug source. | Yes, with a tight definition | Keep |
| 3 | Object scale is applied or reset | Yes | `Object.scale` (Vector). Optional sanity: `matrix_world` decomposition for parented objects | Low | Low. O(N) over mesh objects. | Low if the rule is "scale equals (1,1,1) within epsilon for delivered mesh objects". Slightly higher if the user intentionally uses non-applied scale for proxies. | Yes | Keep |
| 4 | Object rotation/orientation is applied or reset | Yes | `Object.rotation_euler`, `Object.rotation_mode`, `Object.rotation_quaternion` | Low | Low. O(N). | Medium. Many legitimate workflows leave rotation unapplied (e.g., props rotated in the scene). The check must be framed as a delivery readiness signal, not a hard error, or it generates fatigue. | Yes, but priority should be reviewed (see Section 3) | Keep, downgrade severity |
| 5 | Required UV map exists and is non-empty | Yes | `Mesh.uv_layers` (presence of at least one layer), per-loop UV data (`mesh.uv_layers.active.data`); non-empty defined as having loops with non-degenerate UV bounds | Low-Medium | Low-Medium. Reading per-loop UV for "non-empty" is O(loops); on a heavy mesh this is the most expensive of the six checks but still cheap compared to operators. | Low for "layer exists". Medium for "non-empty" if the rule is too strict (e.g., all UVs at origin can be a default unwrap state). | Yes, scoped to existence and "not all zero" | Keep |
| 6 | Normals are consistent and not flipped | Partial | `Mesh.polygons[i].normal`, `Mesh.has_custom_normals`, `Mesh.use_auto_smooth`, BMesh for manifold/orientation analysis | Medium-High | Medium. BMesh construction on heavy meshes is the main perf risk in v1. | High. "Flipped" is not a single objective property; detection typically uses heuristics (volume sign for closed meshes, consistent winding via BMesh `bmesh.ops.recalc_face_normals` comparison, or outward-facing dominance). All produce false positives on open meshes, hard surface with intentional inward faces, or non-watertight assets. | Conditional. Safe to ship only as "inconsistent winding within a connected manifold" rather than "flipped against camera/world." | Keep with reduced ambition |

Notes that affect every row:

- All checks must be read-only. No `bpy.ops.*` calls that mutate the scene. Some Blender operators implicitly require a particular context, which makes them unreliable in non-UI execution.
- Heavy meshes (the 38M-poly case in `real-failure-database.md` row 29) are real. Any check that walks mesh elements must short-circuit on extreme polycount or warn the user instead of running.
- Linked/library objects (`Object.library is not None`) may not be modifiable by the user inside the current file; v1 should report on them but mark them as "linked, fix in source."

---

## 3. Recommended MVP v1 Checks

Recommendation: keep five checks for v1. Drop one of the proposed six.

| # | Check | Severity | Rationale |
|---:|---|---|---|
| 1 | Texture files are present, packed, or reachable | BLOCKER | 19 missing texture/material cases in `pain-analysis.md`; direct marketplace rejection evidence (cases 9, 10) and import failures (cases 1-8, 44-47). Highest-frequency family the user can pre-detect from file state. |
| 2 | Materials are assigned and export-relevant | BLOCKER | Same family; distinct failure mode (slot present but unconnected or empty). Cases 4, 5, 10, 34, 41, 44-47. Must remain narrow: slot has material, material has surface output, image textures reachable. |
| 3 | Object scale is applied or reset | BLOCKER | 15 transform family cases; CGTrader case 33 (days of failed upload), Unity case 49. Best-evidenced single check. |
| 4 | Required UV map exists and is non-empty | BLOCKER | Cases 19, 36, 46, 48. Causes both export failure and texture pipeline failure. Cheap to implement at "exists + not all zero." |
| 5 | Normals are consistent and not flipped | BLOCKER, with conservative detection | Cases 24, 26, 27, 28; strongest single geometry signal. Must ship as "inconsistent winding within manifold" to avoid the false-positive trap on open meshes. |

Cut from the six:

- **Object rotation/orientation applied or reset** — drop from v1 as a separate check. Evidence support is weaker than scale (`MVP_EVIDENCE_MAPPING.md` rates rotation Medium vs scale Strong). Many legitimate Blender workflows keep rotation unapplied; making it a BLOCKER will produce noise that erodes trust in the score, which `payment-evidence.md` flags as a kill signal. Re-introduce in v2 once the score is trusted, possibly as a WARNING merged with scale into a single "Transforms applied" check.

Why five, not six:

- `payment-evidence.md`: "Users do not describe warnings as noisy or irrelevant" is a success criterion. Each weak check is a noise risk against a $5-$9 product.
- `mvp-reduction.md`: "delete features until only the evidence-supported core remains."
- `MVP_REVIEW_REPORT.md` already names a top-5 (texture presence, materials assigned, scale, export selection, normals). Four of those overlap with this list. The substitution made here drops "export selection" and adds "UV map exists" because export-selection logic is harder to define cleanly without a UI flow (see Section 7).

If implementation proves any of these five generates >10% false positives in real test files, that check is demoted to WARNING or held back from v1 release rather than added to.

---

## 4. Data Model Draft

Minimum types only. No persistence layer, no settings system, no plugin preferences in v1.

```
CheckResult
  id              : str            # stable identifier, e.g. "tex_presence"
  name            : str            # human-readable, e.g. "Texture Files Reachable"
  status          : enum           # PASS | WARNING | FAIL
  severity        : enum           # BLOCKER | WARNING | INFO
  message         : str            # one-line summary, fixed wording per check
  affected_objects: list[str]      # object names; may be empty for scene-level checks
  evidence_reason : str            # short reason tied to the check definition,
                                   # e.g. "Image 'wood.png' missing on disk and not packed"

InspectionReport
  results         : list[CheckResult]
  score           : int            # 0..100
  verdict         : enum           # READY | DELIVERY_RISK | NOT_READY
  blocker_count   : int
  warning_count   : int
  generated_at    : datetime       # local time, for the user only; no telemetry
  blender_version : str            # for issue triage if reported
```

Design rules:

- `CheckResult` is the only unit of work output. Every check produces zero or more of these; the report aggregates them.
- `evidence_reason` is required and must be specific. Empty or generic reasons defeat the score's value (`mvp-reduction.md`: "the score must map directly to detected blockers").
- No nested issue objects, no severity overrides, no per-object check metadata. If a check needs to call out individual objects, it puts their names in `affected_objects` and writes one `CheckResult`.
- `affected_objects` carries names rather than `bpy_struct` references. This avoids stale pointer issues if the user edits the scene before reading the report.
- No fix suggestions in the data model. v1 reports issues; it does not propose actions inside the data structure.

---

## 5. Scoring System Draft

Starting score: 100.

Deductions (proposed v1 weights, kept simple):

| Severity | Deduction per failure |
|---|---:|
| BLOCKER | -15 |
| WARNING | -5 |
| INFO | 0 (tracked, not scored) |

Per-check weights (sum cannot exceed 100, but does not need to):

| Check | Severity | Deduction |
|---|---|---:|
| Texture files present/packed/reachable | BLOCKER | -15 |
| Materials assigned and export-relevant | BLOCKER | -15 |
| Object scale applied or reset | BLOCKER | -15 |
| Required UV map exists and is non-empty | BLOCKER | -15 |
| Normals consistent and not flipped | BLOCKER | -15 |

Verdict rules:

- **READY FOR DELIVERY** — score >= 90 AND zero BLOCKER failures.
- **DELIVERY RISK** — score in 70-89 AND zero BLOCKER failures.
- **NOT READY FOR DELIVERY** — any BLOCKER failure, regardless of numeric score.

Hard rules that override the numeric score:

- Any single BLOCKER failure → verdict is NOT READY. The number is shown, but the badge is NOT READY.
- Three or more BLOCKER failures cap the displayed score at 49.
- A WARNING never changes the verdict from READY to NOT READY on its own. It can lower a READY into DELIVERY RISK.

Output format:

```
READY FOR DELIVERY
Score: 87%
3 Blocking Issues
5 Warnings
```

(In a NOT READY case the first line reads `NOT READY FOR DELIVERY` and the score is shown for transparency but the verdict is the headline.)

Design rules:

- The verdict, not the number, is the load-bearing message. The number exists to communicate trend across runs.
- Scoring is deterministic. Same file, same Blender version, same plugin version → same score.
- No partial credit per check. A check is PASS or it is a failure of one severity. This avoids tunable thresholds that would need user configuration v1 has no UI for.

---

## 6. Minimal Module Structure

Conceptual layout. No code, no `__init__.py` contents specified.

```
pipeline_inspector/
  __init__.py            # add-on registration only
  inspector.py           # orchestrator: runs the checks, aggregates results
  scoring.py             # pure function: list[CheckResult] -> InspectionReport
  report.py              # builds the human-readable report payload from InspectionReport
  ui.py                  # one panel, one operator: "Run Inspection" + result list
  checks/
    __init__.py          # check registry
    textures.py          # check 1: texture presence/packed/reachable
    materials.py         # check 2: materials assigned and export-relevant
    transforms.py        # check 3: scale applied
    uvs.py               # check 4: UV map exists and non-empty
    normals.py           # check 5: normals consistent (conservative)
```

Architectural rules:

- `checks/*` modules export a single check function each. Signature is conceptually `(context) -> list[CheckResult]`. They do not import each other.
- `scoring.py` is pure: it takes `CheckResult` objects and returns an `InspectionReport`. No Blender access. This makes it the only piece that can be unit-tested without Blender.
- `inspector.py` is the only module that touches `bpy.context` directly; checks receive resolved data, not the raw context. This keeps the rest of the code testable and avoids the operator-context fragility that plagues many Blender add-ons.
- `ui.py` does not contain inspection logic. It calls `inspector.run()` and renders the returned `InspectionReport`.
- No `config/`, no `presets/`, no `engine/`, no `network/`, no `ai/`, no `fix/`. If a module is not in the diagram above, it is out of scope.

---

## 7. Implementation Risks

### Blender API risks

- **Operator-context fragility.** Many `bpy.ops.*` calls require a specific UI context. v1 must not depend on any operator at all; all five checks can be implemented through the data API. If during development a check appears to need an operator, that is a sign the check is too ambitious for v1.
- **Linked/library objects.** Objects from a linked library cannot be edited from the current file. v1 must report them but mark them as not-locally-fixable rather than counting them as the user's failure.
- **Blender version drift.** Image API (`Image.has_data`, `Image.packed_files`) and BMesh APIs have shifted across 3.x and 4.x. v1 should target a minimum Blender version (recommended: 4.2 LTS) and document it. No multi-version compatibility shims in v1.
- **Custom normals and auto-smooth.** Blender 4.1+ replaced auto-smooth with a modifier. The normals check must read `Mesh.has_custom_normals` and skip orientation heuristics when custom normals are authored, otherwise the check second-guesses an artist's intentional choice.

### Texture path check risks

- **Relative `//` paths.** Blender's relative path notation must be resolved against the current `.blend` directory. An unsaved file has no anchor; v1 should warn rather than error in that case.
- **UDIM tiles.** A single image datablock can map to many files (`<UDIM>` token expansion). The check must treat all expected tiles as required for "reachable," or accept the first tile as proof-of-life. Decision must be made before implementation; either choice is defensible if documented.
- **Packed-but-stale.** A `packed_file` exists but the original on-disk file has changed since packing. This is not a delivery failure (the packed copy ships) and must not be reported as one.
- **Non-image textures.** Procedural textures or volume data must not be reported as "missing" because they have no `filepath`.

### Normal check false-positive risk

- **Open vs closed meshes.** "Flipped" only has a clean definition for closed manifolds. Open meshes (planes, cards, hair sheets) routinely have intentional one-sided faces. v1 must scope the check to "inconsistent winding within a connected manifold component" and skip components that fail the manifold test rather than label them flipped.
- **Hard-surface intentional inward faces.** Some assets have intentionally inward-facing geometry (interiors, cavities). The check should report these as INFO at most when winding is internally consistent.
- **Recommendation:** if the conservative version still produces noticeable false positives in early testing, demote this check to WARNING for the v1 release. This is cheaper than removing it after launch.

### Export selection — should it enter v1?

The original `MVP_CHECKLIST.md` named "Export selection contains visible deliverable mesh" as a BLOCKER, and `MVP_REVIEW_REPORT.md` keeps it in its top-5. This architecture proposes excluding it from v1 for a structural reason:

- "Export selection" requires a definition of "what is being delivered." Blender has no native concept of a delivery selection; it has the active selection, the active collection, and exporter-specific include filters. v1 has no UI for the user to declare "this is my deliverable set."
- Without that declaration, the check either (a) inspects the current selection, which is fragile because users select and deselect constantly, or (b) inspects the active collection, which assumes a workflow convention.
- A v1.1 can introduce a "Deliverable" selection step (one operator, one UI affordance) and then re-add this check with high confidence. That is a small, additive change.

Recommendation: defer export-selection check to v1.1. The five checks proposed above already catch the dominant failure families.

### Performance risks

- **Heavy meshes.** UV non-empty and normals consistency walk per-loop and per-face data. On meshes above ~1M polys this becomes user-visible. v1 should set a configurable polycount threshold (default ~500k) above which the check returns INFO ("Mesh too large to inspect, run on simplified version") rather than running.
- **Image disk checks at scale.** Files on slow network drives can stall `os.path.exists`. Wrap each in a short timeout or batch them with awareness; do not run them on a synchronous main-thread call without a progress indicator.
- **Single-shot run.** v1 should run all checks once on user demand. No background timers, no save handlers, no auto-run. The risks of save-handler bugs corrupting user files outweigh any UX benefit at this stage.

### User understanding risks

- **Score must explain itself.** `mvp-reduction.md`: "users will only trust the score if they can see the reason behind it." Every failed check must produce a `CheckResult.evidence_reason` that names the specific object and the specific defect.
- **Verdict vs score conflict.** A user seeing `Score: 87%` next to `NOT READY FOR DELIVERY` will be confused. v1 copy must lead with the verdict; the number is secondary.
- **Scope creep on first use.** Early users will ask for "and also check N-gons / naming / UV overlap." v1 must hold the line. The product positioning depends on `payment-evidence.md`'s finding that users buy *outcomes*, not feature counts.

---

## 8. Development Recommendation

# LIMITED GO

Pipeline Inspector MVP v1 may enter Development Phase, with the scope locked to the five checks defined in Section 3 and the architecture defined in Sections 4-6. This is a Limited Go, not a full Go.

### First development batch (allowed)

In priority order, the first batch of development must be limited to:

1. Project scaffolding for the module structure in Section 6 (registration shell, empty check registry, no business logic).
2. `scoring.py` — pure function from `CheckResult` list to `InspectionReport`. Unit-testable without Blender.
3. Check 3: **Object scale is applied or reset.** Lowest risk, strongest evidence, best forcing function for the data flow.
4. Check 4: **Required UV map exists and is non-empty.** Low risk after scale.
5. Check 1: **Texture files are present, packed, or reachable.** Implement the narrow definition only (existence/packed/reachable). Defer UDIM and packed-stale handling to a follow-up if needed.
6. Check 2: **Materials are assigned and export-relevant.** Implement against a written predicate.
7. Minimal `ui.py` with one operator and one panel, only enough to invoke `inspector.run()` and render the report.
8. Check 5: **Normals consistent and not flipped.** Conservative implementation, ship as WARNING if false-positive rate is uncertain at the end of internal testing.

### Not allowed in this batch

- The dropped rotation check.
- The deferred export-selection check.
- Any auto-fix, any settings UI beyond the run button, any preferences panel, any cloud or telemetry, any AI feature.
- Any new check beyond the five listed above, even if it appears trivial.

### Conditions for upgrading Limited Go to full Go

Before v2 work starts, the v1 release must clear at least these gates from `evidence/payment-evidence.md` and `evidence/go-no-go-report.md`:

- Early users report the tool caught at least one issue before export or upload (`mvp-reduction.md` success criterion).
- False-positive rate on the five checks is low enough that users do not describe the warnings as noisy.
- At least 5-10 users express willingness to pay $5-$9 after seeing the score in their own files.

If these gates are not met, the answer for v2 is reframe or stop, not expand.

### Reasoning summary

A NO-GO is not justified: the evidence base is solid, the scope is now narrow enough to build, and the architecture is small enough to fail cheaply. A full GO is not justified either: every check beyond the five named here has either weaker evidence or higher implementation risk, and `payment-evidence.md` shows the monetization ceiling for a validation tool is low enough that build cost discipline matters more than feature breadth.

LIMITED GO is the correct verdict.
