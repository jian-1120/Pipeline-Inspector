# SCAFFOLD PLAN v1

Role: Lead Technical Designer.

Phase: Scaffold (post-Implementation Spec). Prior phases — Evidence, MVP Definition, Architecture, Implementation Spec — are completed and locked.

Purpose: define the exact file and folder layout, the responsibility of every module and file, the dependency graph, and the registration strategy, so a developer can create the empty stubs and begin implementation **without changing the architecture**.

Authoritative inputs (binding):

- `ARCHITECTURE_MVP_V1.md` — module shape, scope ban list.
- `IMPLEMENTATION_SPEC_V1.md` — five checks, data structures, development order, score and report rules.

Conflict rule: this scaffold plan must not contradict either of the above. Where a tradeoff exists, this document defers to the spec. The scope ban list (AI, cloud, auto-fix, marketplace, engine, shader/texture quality, team) is treated as architectural law and is not relaxed by anything below.

This document does not contain code, Blender API calls, or plugin files. It contains layout, names, and responsibilities.

---

## 1. Final Folder Structure

This is the layout a developer should create empty in v1.0. No files outside this layout are part of v1.

```
pipeline_inspector/                  # the add-on package; this is the folder zipped for install
  __init__.py                        # add-on metadata + register/unregister entry point
  inspector.py                       # orchestrator: runs all checks, builds InspectionResult
  scoring.py                         # pure: list[CheckResult] -> (score, verdict, counts)
  report.py                          # pure: InspectionResult -> rendered report payload
  models.py                          # data record definitions (no logic)
  constants.py                       # fixed thresholds: SCALE_EPSILON, UV_BBOX_EPSILON, POLYCOUNT_CAP, FILE_EXISTS_TIMEOUT_MS, AFFECTED_OBJECTS_CAP
  ui/
    __init__.py                      # re-exports panel + operator classes for registration
    panel.py                         # the single N-panel that shows the result
    operator_run.py                  # the "Run Inspection" operator
  checks/
    __init__.py                      # check registry: ordered list of (id, name, callable)
    base.py                          # shared helpers: visibility filter, linked-object filter, mesh-only filter, polycount cap helper
    textures.py                      # Check 01 — Texture Presence
    materials.py                     # Check 02 — Material Assignment
    transforms.py                    # Check 03 — Applied Scale
    uvs.py                           # Check 04 — UV Existence
    normals.py                       # Check 05 — Normal Consistency
  state.py                           # in-memory holder for the most recent InspectionResult so the panel can render after the operator finishes

tests/                               # not part of the installed add-on; kept alongside the source
  test_scoring.py                    # exercises scoring.py without Blender
  test_report.py                     # exercises report.py without Blender
  fixtures/                          # plain-data CheckResult fixtures used by the two tests above

LICENSE                              # already present at repo root
README.md                            # already present
ARCHITECTURE_MVP_V1.md               # already present
IMPLEMENTATION_SPEC_V1.md            # already present
SCAFFOLD_PLAN_V1.md                  # this file
```

Rules:

- The installable add-on is the `pipeline_inspector/` folder. Everything outside it (tests, docs) is repository-only and not shipped.
- No `config/`, no `presets/`, no `engine/`, no `network/`, no `ai/`, no `fix/`, no `cloud/`, no `team/`. If a folder is not above, it does not exist in v1.
- No top-level helper file like `utils.py`. Cross-check helpers live in `checks/base.py`. Cross-system helpers (paths, timing) belong in the module that uses them; v1 is small enough that a `utils.py` becomes a junk drawer.
- The `tests/` folder ships with the repo but is excluded from the add-on zip. The test files only exercise the two pure modules (`scoring.py`, `report.py`); they do not import `bpy`.

---

## 2. Module Responsibilities

The package decomposes into four layers. A module belongs to exactly one layer.

| Layer | Modules | Responsibility |
|---|---|---|
| Entry | `__init__.py` | Add-on metadata (`bl_info`), register and unregister functions, nothing else. |
| Orchestration | `inspector.py`, `state.py` | Build the inspection input set, iterate the check registry, produce a `InspectionResult`, hold the most recent result for the panel to read. |
| Domain | `checks/*`, `scoring.py`, `report.py`, `models.py`, `constants.py` | The actual product logic: per-check predicates, score derivation, report formatting, data records, fixed thresholds. |
| Interface | `ui/panel.py`, `ui/operator_run.py` | Surface the result inside Blender. Triggers the orchestrator; reads `state.py`; renders. |

Layer rules:

- Entry imports Interface and Orchestration only at registration time. It does not call domain logic directly.
- Orchestration imports Domain. It does not import Interface.
- Domain imports `models.py` and `constants.py`. It does not import Orchestration, Interface, or Entry.
- Interface imports Orchestration (`state.py`) and `models.py` for typing. It does not call Domain modules directly.
- `models.py` and `constants.py` import nothing from the package. They are leaves of the dependency graph.

This is the only enforced rule about imports. There are no other ordering rules in v1.

---

## 3. File Responsibilities

The following paragraphs describe what each file owns. A developer creating empty stubs should not need to consult any other document for this.

### `pipeline_inspector/__init__.py`

Owns the add-on registration surface. Responsibilities:

- Declare `bl_info` with name `"Pipeline Inspector"`, target Blender version 4.2.0, category `"3D View"`, version tuple, author placeholder, and a one-sentence description.
- Define `register()` and `unregister()` that register the panel class and the operator class in the correct order (operator before panel, since the panel button references the operator).
- Nothing else. No business logic, no constants, no data classes.

### `pipeline_inspector/inspector.py`

Owns one public entry point: `run_inspection()`. Responsibilities:

- Build the inspection input: the list of visible non-linked mesh objects in the active scene (`obj.type == 'MESH'`, `obj.visible_get()`, `obj.library is None`). The shared filter implementation lives in `checks/base.py`.
- Iterate the check registry from `checks/__init__.py` in fixed order.
- For each registered check, call its function with the prepared inputs. Each call returns a single `CheckResult`.
- Aggregate the five `CheckResult` objects, hand them to `scoring.py` to derive score, verdict, blocker count, warning count.
- Stamp `generated_at` (local time) and `blender_version` (from Blender app data).
- Return an `InspectionResult`.
- Write the result into `state.py` as a side effect so the panel can re-render without re-running.

`inspector.py` does not format text; that is `report.py`'s job. It does not render UI; that is `ui/`'s job.

### `pipeline_inspector/scoring.py`

Pure function module. No `bpy` import. Responsibilities:

- Given a list of `CheckResult`, compute `score`, `verdict`, `blocker_count`, `warning_count`.
- Apply the deduction table, the cap rules, and the verdict state machine exactly as defined in `IMPLEMENTATION_SPEC_V1.md` Section 4.
- Return a tuple or small record. The orchestrator merges this into the final `InspectionResult`.

This module is unit-testable without Blender and must remain so.

### `pipeline_inspector/report.py`

Pure function module. No `bpy` import. Responsibilities:

- Given an `InspectionResult`, produce the rendered report payload described in `IMPLEMENTATION_SPEC_V1.md` Section 5: header, verdict line, score line, counts line, fixed-order check list, optional issues block, footer line.
- Return a structure (sequence of typed lines or a single string with a documented separator) that the panel can iterate and draw without reformatting.

`report.py` does not own UI styling, color, or layout. It owns text content and order.

### `pipeline_inspector/models.py`

Data records only. No logic. Defines:

- `CheckResult` with the fields in Implementation Spec Section 7.
- `InspectionResult` with the fields in Implementation Spec Section 7.
- `IssueRecord` with the fields in Implementation Spec Section 7.
- The status enum (`PASS`, `WARNING`, `FAIL`).
- The severity enum (`BLOCKER`, `WARNING`, `INFO`).
- The verdict enum (`READY`, `READY_WITH_WARNINGS`, `NOT_READY`).

Records are plain-data containers (no methods beyond construction). This is binding because `report.py` and `scoring.py` are required to remain pure, and any method on a record creates a temptation to add behavior in the wrong place.

### `pipeline_inspector/constants.py`

Single source of truth for tunable values that are fixed in v1:

- `SCALE_EPSILON = 1e-4`
- `UV_BBOX_EPSILON = 1e-5`
- `POLYCOUNT_CAP = 500_000`
- `FILE_EXISTS_TIMEOUT_MS = 200`
- `AFFECTED_OBJECTS_CAP = 50`

These values live in one file so a future amendment to the spec only edits one place. Nothing else lives in `constants.py`.

### `pipeline_inspector/state.py`

Holds the most recent `InspectionResult` for the current Blender session. Responsibilities:

- Module-level reference to the latest result, with a setter and a getter.
- Defaults to `None` (no run yet).
- Cleared on `unregister()`.

This avoids storing the result on a `bpy.types.PropertyGroup`, which would require Blender-side schema management v1 does not need.

### `pipeline_inspector/ui/__init__.py`

Re-exports `PIPELINE_INSPECTOR_PT_panel` and `PIPELINE_INSPECTOR_OT_run` so the top-level `__init__.py` can register them in one import. No logic.

### `pipeline_inspector/ui/panel.py`

Owns the `PIPELINE_INSPECTOR_PT_panel` panel class. Responsibilities:

- Locate itself in `VIEW_3D` / `UI` region / `Pipeline Inspector` tab.
- Read `state.get_latest_result()` and render the result blocks listed in `IMPLEMENTATION_SPEC_V1.md` Section 6: score line, counts line, checks list, issues area, footer.
- Render the placeholder line when no result exists yet.
- Place the `Run Inspection` button.

The panel does not call check functions directly. The panel does not call `scoring.py` or `report.py` directly; it consumes the result that `report.py` produced via `inspector.py`.

### `pipeline_inspector/ui/operator_run.py`

Owns the `PIPELINE_INSPECTOR_OT_run` operator. Responsibilities:

- One operator with `bl_idname = "pipeline_inspector.run"`, `bl_label = "Run Inspection"`.
- On execute: call `inspector.run_inspection()`. The operator does not interpret the result; the orchestrator stores it in `state.py` and the panel will pick it up on the next redraw.
- Return `{'FINISHED'}`.
- No modal flow. No background timer. No long-running thread. v1 is synchronous.

### `pipeline_inspector/checks/__init__.py`

Owns the check registry. Responsibilities:

- Define `CHECK_REGISTRY` as an ordered sequence of `(id, name, callable)` tuples in the fixed order from the implementation spec: `01_texture_presence`, `02_material_assignment`, `03_applied_scale`, `04_uv_existence`, `05_normal_consistency`.
- Re-export the five check functions from their files.
- The registry is the only place check ordering is declared. `inspector.py` and `report.py` both consume it; neither hardcodes the order separately.

### `pipeline_inspector/checks/base.py`

Owns helpers shared by more than one check:

- The visible-non-linked-mesh filter (used by every check).
- The polycount cap helper (used by Check 04 and Check 05).
- The "build CheckResult" helpers: PASS shorthand, FAIL shorthand, WARNING shorthand, the `affected_objects` deduplicate-and-cap helper.
- The path resolution helper for `//`-relative paths (used only by Check 01, but lives here so future checks that touch paths reuse it).

If a helper is used by exactly one check, it stays inside that check file. It only moves into `base.py` once a second consumer appears.

### `pipeline_inspector/checks/textures.py`, `materials.py`, `transforms.py`, `uvs.py`, `normals.py`

Each owns exactly one check. Each exposes a single function, e.g. `run_texture_presence(inputs) -> CheckResult`. Each:

- Reads only the Blender data named for it in `IMPLEMENTATION_SPEC_V1.md` Section 2.
- Returns exactly one `CheckResult`.
- Lists any per-object findings as `IssueRecord` rows attached to that result.
- Imports from `models`, `constants`, and `checks/base` only. No cross-imports between check files.

### `tests/test_scoring.py`, `tests/test_report.py`, `tests/fixtures/`

Two thin tests covering the only two pure modules. Fixtures are plain-data `CheckResult` examples covering the four worked scoring examples in the implementation spec (clean, mixed warning, three blockers with cap, warnings-only). No Blender environment needed.

---

## 4. Dependency Graph

```
                          ┌──────────────────────┐
                          │  pipeline_inspector  │
                          │      __init__.py     │  (entry / register only)
                          └──────────┬───────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              ▼                      ▼                      ▼
      ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
      │ ui/panel.py   │      │ ui/operator_  │      │  inspector.py │
      │               │      │   run.py      │      │ (orchestrator)│
      └──────┬────────┘      └──────┬────────┘      └───────┬───────┘
             │                      │                       │
             │ reads                │ calls                 │ iterates registry, calls scoring + report
             ▼                      ▼                       ▼
      ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
      │   state.py    │◄─────┤  inspector    │      │  checks/      │
      │ (latest result│ writes│   .run()     │─────►│  __init__.py  │
      │  holder)      │      │              │      │ (registry)     │
      └───────────────┘      └──────┬────────┘      └───────┬───────┘
                                    │                       │
                                    │ calls                 │ each check imports models, constants, base
                                    ▼                       ▼
                              ┌───────────────┐      ┌─────────────────────────────┐
                              │  scoring.py   │      │ checks/textures, materials, │
                              │  (pure)       │      │ transforms, uvs, normals    │
                              └──────┬────────┘      └──────────────┬──────────────┘
                                     │                              │
                                     ▼                              ▼
                              ┌───────────────┐              ┌───────────────┐
                              │  report.py    │              │ checks/base.py│
                              │  (pure)       │              │  (helpers)    │
                              └──────┬────────┘              └───────┬───────┘
                                     │                               │
                                     └───────────────┬───────────────┘
                                                     ▼
                                            ┌───────────────┐
                                            │  models.py    │  ◄── leaf
                                            │  constants.py │  ◄── leaf
                                            └───────────────┘
```

Read this graph as: arrows point in the direction of imports.

Invariants (must hold across v1):

1. **Cyclic imports are forbidden.** Any new module must place itself in this graph without creating a cycle.
2. **`scoring.py` and `report.py` import only `models` and `constants`.** They never import `bpy`. Tests verify this.
3. **`models.py` and `constants.py` are import leaves.** They never import anything from the package.
4. **`checks/*` modules do not import each other.** They reach shared helpers through `checks/base.py`.
5. **`ui/` modules do not import `checks/` directly.** They go through the orchestrator and `state.py`.

If a developer needs to violate an invariant, they amend this document first. They do not amend the code.

---

## 5. Data Flow

There is one data flow in v1: the user clicks **Run Inspection** and the panel updates. The flow has six steps.

```
Step 1 — User clicks "Run Inspection" in the Pipeline Inspector panel.
           │
           ▼
Step 2 — operator_run.execute() calls inspector.run_inspection().
           │
           ▼
Step 3 — inspector.run_inspection() prepares the input set:
           - active scene
           - filtered list of visible non-linked mesh objects (via checks/base.py)
           - depsgraph reference if needed
           │
           ▼
Step 4 — inspector iterates checks/__init__.py → CHECK_REGISTRY in fixed order.
           For each (id, name, fn):
             result = fn(input_set)        # returns one CheckResult
             results.append(result)
           │
           ▼
Step 5 — inspector calls scoring.derive(results) → (score, verdict, blocker_count, warning_count).
           inspector wraps everything into an InspectionResult, including generated_at and
           blender_version, and stores it via state.set_latest_result(...).
           │
           ▼
Step 6 — Panel redraws (Blender triggers redraw after operator FINISHED). Panel reads
           state.get_latest_result(). It hands the result to report.render(...) to obtain
           the typed line sequence and draws it row by row.
```

Cross-cutting rules:

- **One run, one `InspectionResult`.** No partial state is exposed. The panel either shows the placeholder or the full result.
- **No background work.** No `bpy.app.timers`, no modal operators, no save/load handlers. The user is the only trigger.
- **Read-only end to end.** No step in the flow mutates the Blender scene. The depsgraph is read; no operator modifies data.
- **Result is session-scoped.** When the add-on is unregistered (or Blender closes), `state.py` is cleared. v1 does not persist results across sessions.

---

## 6. Registration Strategy

Single-pass registration with a fixed order. Implemented in `pipeline_inspector/__init__.py`.

### Order of `register()`

1. Import the operator class from `ui.operator_run`.
2. Import the panel class from `ui.panel`.
3. Register the operator class.
4. Register the panel class. (The panel layout references the operator's `bl_idname`, so the operator must exist first.)
5. Initialize `state.py` to a known empty value.

### Order of `unregister()`

1. Clear `state.py` (drop the latest result reference).
2. Unregister the panel class.
3. Unregister the operator class.

Reverse of registration order, with the state cleared first so a half-unregistered panel cannot accidentally read stale data.

### Rules

- No `bpy.types.PropertyGroup`, no `bpy.types.Scene` extensions, no add-on preferences in v1. The add-on does not store anything on Blender's data model. This is intentional — `IMPLEMENTATION_SPEC_V1.md` Section 1 forbids settings UIs and per-project rule files.
- No modal handlers, no app handlers (`bpy.app.handlers.*`). v1 ships without subscribing to any Blender event.
- No icons or icon registration. The panel uses Blender's default icons or text only.
- Register/unregister must be idempotent against double-registration during Blender add-on reload. Use Blender's standard pattern (catch the duplicate-registration exception on register, or guard with a `try`/`except`).
- The add-on must unregister cleanly with no leaked classes when disabled from Blender's preferences.

### Out of scope for registration in v1

- Keymaps (no shortcut for `Run Inspection`).
- Menu items in `View3D` headers, `INFO` menus, or the `File` menu.
- A startup banner, a "what's new" panel, an update checker.
- Network calls of any kind during `register()`.

---

## 7. Future Expansion Points

These are the places where the architecture allows additions later **without restructuring**. None of them are built in v1; they are documented so v1's design is not surprised by them.

| Point | What it enables | Where it lands | What v1 must do today |
|---|---|---|---|
| **New check** | Add a sixth or seventh check (e.g., reintroduce rotation, add export-selection check). | A new file under `checks/`, registered in `CHECK_REGISTRY`. | Keep `CHECK_REGISTRY` as the single source of order. Keep checks isolated from each other. Keep `report.py` driven by the registry, not hardcoded. |
| **Per-check severity demotion** | Ship Check 05 as WARNING in v1.0 if false-positive rate is high; promote later. | A field on the registry entry, or a constant in the check module. | Severity must already be a property the orchestrator reads, not a hardcoded branch in `scoring.py`. |
| **Settings panel** | Add tunable thresholds (polycount cap, scale epsilon). | New `preferences.py` adjacent to `__init__.py`; `constants.py` becomes a default source rather than the only source. | Keep `constants.py` as the single read site for thresholds. v2 swaps `constants.py` calls for a preferences-aware lookup; v1 callers don't change shape. |
| **Persisted results across sessions** | Survive Blender restart. | A new `persistence.py` adjacent to `state.py`, plus a one-line save in `inspector.run_inspection()`. | `state.py` must already be the only read site for the latest result. v1 already enforces this. |
| **Export report to file** | Save the report to disk. | A new operator next to `operator_run.py` that calls `report.render()` and writes to disk. | `report.py` already returns a structure suitable for any sink. v1 already enforces purity. |
| **Per-object issue navigation** | Click an object name in the panel to select it in the viewport. | A new operator that takes an object name; the panel renders rows as buttons. | `IssueRecord.object_name` already carries the name as a string. v1 already enforces this. |
| **Localization** | Translate UI strings. | Strings centralized in `report.py` and `ui/panel.py`; replace literals with a lookup table. | Keep user-facing strings in those two files only. Check files emit `evidence_reason` text; that text flows into `IssueRecord.reason` and is rendered, not interpreted. |

Hard rule: a future expansion point is **not** an excuse to add scaffolding for it in v1. The point of listing them is to ensure v1's design choices do not block them, not to pre-build them.

What is **not** an expansion point (still banned by `IMPLEMENTATION_SPEC_V1.md` Section 1):

- AI / cloud / auto-fix / team / marketplace / engine-specific / shader quality / texture quality.

---

## 8. Risks in Architecture

These are scaffold-level risks (the things that go wrong in the layout, registration, and module split). Check-level risks live in `IMPLEMENTATION_SPEC_V1.md` Section 9; they are not duplicated here.

### 1. Orchestrator becomes a god module

`inspector.py` is the only place that calls Blender data, all checks, scoring, report, and state. If unmonitored it will accumulate utility code, special cases, and per-check exceptions.

**Mitigation:** keep `inspector.run_inspection()` to a single linear flow — prepare inputs, iterate registry, derive score, stamp metadata, store. New behavior lives in `checks/base.py` or in a check file, not in the orchestrator.

### 2. `state.py` as global mutable state

A module-level reference to the latest result is the simplest design and the right one for v1, but it is also a source of bugs the moment v1.x adds anything else (multiple scenes, multiple windows, persistence).

**Mitigation:** treat `state.py` as a single-value cache, not a database. Reads return the value or `None`. Writes overwrite. No history, no per-window storage in v1. If a future feature needs more, it adds `persistence.py` rather than enlarging `state.py`.

### 3. Registration ordering bugs

Reload-during-development is the most common way Blender add-ons leak classes. A panel referencing a not-yet-registered operator throws at draw time; a half-unregistered add-on leaves zombie classes.

**Mitigation:** the fixed registration order in Section 6, plus idempotent register, plus clean unregister. No keymaps in v1 (keymaps are the second most common leak source).

### 4. UI coupling to internal records

If `ui/panel.py` reads private fields off `InspectionResult` directly, every change to the data model breaks the panel.

**Mitigation:** the panel reads `report.render(result)` output, not `result` directly. The only field the panel reads off `InspectionResult` is the timestamp/version footer line, and that exists because the report payload exposes it as a typed line.

### 5. Test surface is too small

Only `scoring.py` and `report.py` are testable without Blender. A bug in any check is caught only by manual dogfood runs.

**Mitigation:** accept this for v1. Adding a Blender test harness (e.g., `blender --python` runners) is non-trivial and out of scope. The five-phase development order (`IMPLEMENTATION_SPEC_V1.md` Section 8) provides a manual gate at each phase. v2 may revisit a fixture-based check test harness.

### 6. Cross-version Blender drift

The scaffold targets Blender 4.2 LTS. Blender 4.x introduced breaking API changes (auto-smooth → modifier in 4.1; image filepath behavior; some BMesh signatures). A scaffold that hardcodes 4.2 behavior may be invisibly fragile under 4.3 or 4.4.

**Mitigation:** target 4.2 LTS exclusively in v1, declare it in `bl_info` (`"blender": (4, 2, 0)`), and refuse to load on older versions. Newer versions are validated case-by-case and only after v1 ships. No compatibility shims.

### 7. Implicit operator context dependence

Some `bpy.ops` calls require a particular UI context that does not exist when called from the panel button. v1 forbids `bpy.ops.*` calls inside checks (read-only API only), which removes this risk — but a developer unfamiliar with Blender may reach for an operator anyway.

**Mitigation:** explicit invariant in this document. Any check found calling `bpy.ops.*` is a regression. The shared helpers in `checks/base.py` provide read-only patterns so the temptation does not arise.

### 8. Five files for five checks may feel disproportionate

A reviewer may suggest collapsing `transforms.py` and `normals.py` and the others into one file because each is small.

**Mitigation:** keep the one-file-per-check rule. Future expansion (Section 7) and per-check severity demotion (Section 7) both depend on each check being independently addressable. Consolidating them now creates a refactor cost in v1.x.

---

## 9. Readiness Statement

This scaffold:

- Inherits scope from `ARCHITECTURE_MVP_V1.md` and contracts from `IMPLEMENTATION_SPEC_V1.md` without contradiction.
- Names every file a developer must create in v1.
- Names every file a developer must **not** create in v1.
- Defines a single import-acyclic dependency graph with five invariants.
- Defines a single user-triggered data flow with no background work.
- Defines registration in one direction with idempotent reload semantics.
- Documents future expansion points so v1 design does not foreclose them and v1 does not pre-build them.

A developer reading this document end-to-end, with the architecture and implementation spec in hand, can create the empty stubs and begin Phase 1 of `IMPLEMENTATION_SPEC_V1.md` Section 8 without changing the architecture.
