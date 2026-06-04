# IMPLEMENTATION SPEC v1

Role: Lead Technical Designer.

Phase: Implementation Specification (post-Architecture). Evidence Phase = Completed. Architecture Phase = Completed.

Purpose: translate `ARCHITECTURE_MVP_V1.md` into a developer-ready specification. A developer reading this document end-to-end should be able to start implementation without re-reading the evidence files.

Authoritative inputs:

- `ARCHITECTURE_MVP_V1.md` (binding scope and module shape)
- `MVP_CHECKLIST.md`, `MVP_EVIDENCE_MAPPING.md`, `MVP_REVIEW_REPORT.md`, `TOP_FAILURES.md`
- `prd/product-requirements.md`, `prd/mvp-definition.md`
- `evidence/real-failure-database.md`, `evidence/pain-analysis.md`, `evidence/payment-evidence.md`, `evidence/go-no-go-report.md`, `evidence/mvp-reduction.md`
- `research/pain-points.md`

Conflict rule: when this spec disagrees with anything in PRD, MVP_CHECKLIST, or research notes, this spec wins because it inherits from the locked architecture. The architecture document is not modified by this spec.

Target Blender version: 4.2 LTS minimum. v1 does not support older versions and does not include version-compatibility shims.

---

## 1. MVP Boundary

### V1 does

- Inspect the currently open Blender file using read-only access to `bpy.data` and `bpy.context`.
- Run a fixed set of five checks (defined in Section 2).
- Produce one `InspectionResult` per run, containing all `CheckResult` records and one aggregated score and verdict.
- Display the result in a single Blender side panel.
- Allow the user to manually trigger a run with one button.

### V1 does not

The following are out of scope and must not be designed, scaffolded, or stubbed:

- AI analysis, LLM suggestions, model-based heuristics.
- Cloud reports, accounts, telemetry, remote storage, SaaS workflows.
- Auto-fix, repair operators, or any mutation of the user's scene.
- Marketplace compliance (descriptions, preview images, licensing, documentation).
- Engine-specific validation (Unity/Unreal/Godot import simulation, engine presets).
- Shader quality analysis (node graph audit, PBR correctness, channel packing rules).
- Texture quality analysis (resolution policy, color-space heuristics, texel density).
- Team collaboration, shared rule sets, multi-user features, asset libraries.
- Background timers, save handlers, auto-run on export, modal operators.
- Settings panels, presets, configurable thresholds, per-project rule files.

If a feature is not in Section 2, it is not in v1.

---

## 2. Check Specification

All five checks share these contract rules:

- Pure read. No `bpy.ops.*` calls that mutate scene data. No write to disk.
- Operate over the set of mesh objects in the current scene that are visible in the viewport (`obj.visible_get()` true) and not from a linked library (`obj.library is None`). Linked objects are surfaced as INFO with a "linked, fix in source file" note and do not affect the score.
- Skip non-mesh object types (lights, cameras, empties, armatures, curves, lattices). v1 only inspects `obj.type == 'MESH'`.
- A check that finds no failures emits exactly one `CheckResult` with `status = PASS`. A check that finds failures emits exactly one `CheckResult` with `status = FAIL` (or `WARNING`) and lists every offending object name in `affected_objects`. v1 does not emit one `CheckResult` per object.
- Object names in `affected_objects` are stored as strings (`obj.name`), not references. The list is sorted alphabetically and capped at 50 entries; an overflow note appends `(... and N more)` to the message.

---

### Check 01 — Texture Presence

**Purpose**

Confirm that every image texture referenced by a delivered material is either packed into the .blend, present on disk at its referenced path, or otherwise reachable. The user should not export a file that is silently missing image data.

**User Problem**

Models export and arrive gray, white, or untextured at the destination. The artist did not see the failure inside Blender because the source file still has cached pixel data, but the receiver opens the file with no image at the referenced path. Marketplace platforms reject submissions where textures are not packed.

**Evidence Source**

- `evidence/real-failure-database.md` cases 1-8 (Blender→Unity/Unreal texture loss), case 9 (textures not packed → marketplace rejection), case 10 (shaders not linked to packed textures), case 34 (gray export), cases 44-47 (untextured exports).
- `evidence/pain-analysis.md`: 19 missing texture/material family cases.
- `MVP_CHECKLIST.md` §1, `MVP_EVIDENCE_MAPPING.md` §1 (Strong evidence, Keep).

**Blender Data Required**

- `bpy.data.images` collection
- For each `Image`: `image.packed_file`, `image.filepath_raw`, `image.filepath` (resolved), `image.source`, `image.has_data`
- For each material reachable from a visible mesh object: `Material.use_nodes`, `Material.node_tree.nodes` filtered to `type == 'TEX_IMAGE'`, then `node.image`
- `bpy.path.abspath()` to resolve `//`-relative paths against the saved .blend file
- `os.path.exists()` for non-packed images with `image.source == 'FILE'` or `'TILED'`

**Pass Condition**

For every `Image` referenced by an image texture node inside a material assigned to a visible non-linked mesh object, at least one of the following is true:

- `image.packed_file is not None`, OR
- `image.source == 'GENERATED'` (no file expected), OR
- `image.source in {'FILE', 'TILED', 'SEQUENCE'}` and the resolved absolute path exists on disk and `image.has_data` is true.

UDIM rule: for `image.source == 'TILED'`, the first declared tile must resolve. v1 does not validate every tile; missing later tiles are reported as INFO, not FAIL.

**Warning Condition**

- The .blend file is unsaved (no anchor for `//` paths). Emit WARNING with message "Save the file before checking texture paths" and skip path resolution rather than reporting false FAILs.
- A UDIM image has its first tile reachable but at least one declared higher tile is missing on disk.

**Fail Condition**

- An image referenced by a delivered material is not packed and its resolved path does not exist on disk, OR
- An image is referenced but `image.has_data` is false and it is neither packed nor resolvable.

**Output Message**

- PASS: `"All referenced textures are packed or reachable."`
- FAIL: `"N texture file(s) are missing or unreachable: <comma-separated image names>."`
- WARNING (unsaved): `"File is unsaved; texture paths cannot be verified. Save the file and re-run."`

`affected_objects` lists the **object names** whose materials reference the missing image(s), not the image names themselves. The image names appear in the message string.

**Affected Object Reporting**

- For each failing image, walk back to the mesh objects whose `material_slots` reference a material containing that image. Add those object names to `affected_objects`.
- An object that uses several missing images appears once.

**False Positive Risk**

Medium. Sources of risk: relative-path resolution against unsaved files (handled by WARNING), procedural-only materials (no images, must not be flagged), packed-but-stale images on disk (must be treated as PASS — the packed copy is what ships), UDIM partial tiles (handled as INFO).

**Implementation Difficulty**

Low-Medium.

**Estimated Runtime Cost**

Low. Image count is typically tens. Disk existence is one `os.path.exists` per non-packed file. Network drives are the only realistic stall point; a 200ms per-file timeout is sufficient for v1.

---

### Check 02 — Material Assignment

**Purpose**

Confirm that every visible mesh object has at least one material that is genuinely export-relevant: slot occupied, material has a connected surface output, and at least one image texture node feeds that surface (or the material is intentionally a flat color with a node graph that resolves).

**User Problem**

Material slots exist but are empty, unconnected, or set to a placeholder. The mesh exports with material names but no actual shading data, arriving gray on the other side.

**Evidence Source**

- `evidence/real-failure-database.md` cases 4 (Unity manual reassignment), 5 (Unreal lost textures), 10 (shader-texture link broken), 34 (gray export with slots), 41 (conversion missing materials), 44-47 (untextured exports).
- `MVP_CHECKLIST.md` §2, `MVP_EVIDENCE_MAPPING.md` §2 (Strong, Keep).

**Blender Data Required**

- For each visible non-linked `MESH` object: `obj.material_slots`
- For each slot: `slot.material`, `slot.link`
- `Material.use_nodes`, `Material.node_tree.nodes`, `Material.node_tree.links`
- The output node (`type == 'OUTPUT_MATERIAL'`) and whether its `Surface` input has an incoming link

**Pass Condition**

For every visible non-linked mesh object, all of the following are true:

- The object has at least one material slot.
- At least one slot has `slot.material is not None`.
- For each non-empty slot, the material has `use_nodes == True`, an `OUTPUT_MATERIAL` node exists, and that node's `Surface` input has an incoming link from a shader node (any node type, not specifically a BSDF).

**Warning Condition**

- The object has multiple material slots and one or more slots are empty (`slot.material is None`) but at least one slot is valid. Many engines treat empty slots as invisible faces. Report as WARNING with the slot indices.
- A material is assigned but `use_nodes == False` (legacy material). v1 reports this as WARNING and proceeds.

**Fail Condition**

- Mesh object has zero material slots, OR
- Mesh object has slots but none have a material assigned, OR
- All assigned materials have a disconnected `Surface` input on the output node.

**Output Message**

- PASS: `"All mesh objects have export-relevant materials."`
- FAIL: `"N object(s) have missing or disconnected materials: <object names>."`
- WARNING: `"N object(s) have empty or legacy material slots: <object names>."`

**Affected Object Reporting**

`affected_objects` lists the names of mesh objects that fail or warn. One entry per object regardless of how many slots are involved.

**False Positive Risk**

Medium. Sources of risk: legacy non-node materials (handled as WARNING), shader nodes that legitimately do not include image textures (e.g., a flat-color emission asset — must still PASS because the surface is connected), procedural materials (must PASS).

**Implementation Difficulty**

Low.

**Estimated Runtime Cost**

Low. O(slots) per object; node-tree walk per material is bounded by typical material complexity.

---

### Check 03 — Applied Scale

**Purpose**

Confirm that every visible mesh object has its scale applied (`scale == (1.0, 1.0, 1.0)` within epsilon) so downstream tools receive the geometry at its intended size.

**User Problem**

Non-applied scale exports as transformed geometry that imports at the wrong size in Unity/Unreal/marketplaces, or is rejected outright by upload validators (e.g., CGTrader non-reset-transform rejection, multiple days of failed uploads).

**Evidence Source**

- `evidence/real-failure-database.md` case 18 (inconsistent scale), case 19 (wrong scale), case 33 (CGTrader, days of failed upload), case 41 (inconsistent coordinates), case 49 (Unity scale fix required).
- `evidence/pain-analysis.md`: 15 transform/scale/orientation cases.
- `ARCHITECTURE_MVP_V1.md` Section 3 (Strong evidence, Keep).

**Blender Data Required**

- `Object.scale` (Vector of three floats)
- `Object.delta_scale` (read for completeness; if non-default, include in evaluation)
- An epsilon constant: `SCALE_EPSILON = 1e-4`

**Pass Condition**

For every visible non-linked mesh object: `abs(s - 1.0) <= SCALE_EPSILON` for each component of `obj.scale`, AND `obj.delta_scale` equals `(1.0, 1.0, 1.0)` within the same epsilon.

**Warning Condition**

None for v1. This check is binary (applied or not).

**Fail Condition**

Any visible non-linked mesh object whose scale is not (1, 1, 1) within epsilon.

**Output Message**

- PASS: `"All mesh objects have applied scale."`
- FAIL: `"N object(s) have unapplied scale: <object names>."`

**Affected Object Reporting**

`affected_objects` lists names of all mesh objects with unapplied scale.

**False Positive Risk**

Low. The epsilon must be set; otherwise floating-point rounding from prior operations can flag a numerically-equivalent identity. Linked objects are excluded by the shared contract rule.

**Implementation Difficulty**

Low.

**Estimated Runtime Cost**

Very low. O(N) over visible mesh objects, a few comparisons each.

---

### Check 04 — UV Existence

**Purpose**

Confirm that every visible mesh object has at least one UV map and that the active UV map is not entirely degenerate.

**User Problem**

Missing UVs cause export failures (FBX/OBJ pathways), texture pipeline failures, and rejected purchased-asset deliveries.

**Evidence Source**

- `evidence/real-failure-database.md` case 19 (missing UVs in purchased model), case 36 (FBX export failed on UV), case 46 (missing textures/materials on OBJ/FBX), case 48 (FBX export failed on UV).
- `MVP_CHECKLIST.md` §6, `MVP_EVIDENCE_MAPPING.md` §6 (Medium evidence, Keep).

**Blender Data Required**

- `Mesh.uv_layers` (collection)
- The active UV layer: `Mesh.uv_layers.active`
- Per-loop UV data: `Mesh.uv_layers.active.data[i].uv` (Vector of two floats)
- A degenerate threshold: a UV map is "non-empty" if the bounding box of its active layer's UVs has at least one dimension > `UV_BBOX_EPSILON = 1e-5`

**Pass Condition**

For every visible non-linked mesh object whose mesh has at least one polygon: `len(mesh.uv_layers) >= 1`, AND the active UV layer's loop UVs have a bounding box larger than `UV_BBOX_EPSILON` in at least one axis.

A mesh with zero polygons (point cloud, edge-only) is skipped silently and does not contribute to the result.

**Warning Condition**

- Mesh has multiple UV layers but the active layer is degenerate while a non-active layer is non-degenerate. Report as WARNING with message "Active UV layer appears unused; another layer has data."

**Fail Condition**

- Mesh has zero UV layers, OR
- Mesh has UV layers but the active layer's UV bounding box is below `UV_BBOX_EPSILON` in all axes (treated as "all zeros" or "all collapsed at one point").

**Output Message**

- PASS: `"All mesh objects have a non-empty UV map."`
- FAIL: `"N object(s) are missing UV maps or have empty UVs: <object names>."`
- WARNING: `"N object(s) have a degenerate active UV layer: <object names>."`

**Affected Object Reporting**

`affected_objects` lists names of all mesh objects failing or warning.

**False Positive Risk**

Low-Medium. The "non-empty" threshold is conservative; a deliberately tiny UV island could be flagged. v1 accepts this trade-off because the alternative (zero check) misses the most common failure (default unwrap left at origin).

**Implementation Difficulty**

Low.

**Estimated Runtime Cost**

Low-Medium. Bounding-box computation is O(loops). For meshes above the polycount cap (see Section 9), the check returns INFO instead of running.

---

### Check 05 — Normal Consistency

**Purpose**

Confirm that face winding inside each connected manifold component of a mesh is consistent. v1 does not attempt to determine "outward" — it only flags components whose winding is internally contradictory.

**User Problem**

Inconsistent face winding causes shading errors, invisible faces, and inside-out surfaces after export to engines or other DCCs.

**Evidence Source**

- `evidence/real-failure-database.md` case 24 (FBX broke normals), case 26 (blend shapes corrupted normals in Unity), case 27 (normals reversed after OBJ/FBX), case 28 (Unreal "mesh empty inside").
- `MVP_CHECKLIST.md` §7, `MVP_EVIDENCE_MAPPING.md` §7 (Strong, Keep).
- `ARCHITECTURE_MVP_V1.md` Section 7 (must ship as conservative "inconsistent winding within manifold").

**Blender Data Required**

- `Mesh` (evaluated, not the raw datablock; use `obj.evaluated_get(depsgraph).data` if modifiers are stack-relevant — v1 inspects the unevaluated mesh to keep behavior predictable)
- `Mesh.has_custom_normals` (skip the check on this object if true)
- BMesh: `bmesh.from_edit_mesh` is not used; v1 builds a temporary BMesh via `bmesh.new()` and `bm.from_mesh(mesh)` then frees it. Read `bm.faces`, `bm.edges`, edge `link_faces`, face `verts` order.
- Manifold predicate: an edge is manifold if it has exactly two linked faces.

**Pass Condition**

For every visible non-linked mesh object that is not custom-normaled and is below the polycount cap: every connected manifold component has consistent winding (no edge in the component has its two linked faces traversing it in the same direction).

Definition of "consistent winding": for every internal edge of the component, the two faces sharing the edge traverse the edge's two endpoints in opposite order. Inconsistency on any edge inside an otherwise-manifold component is a fail signal for that component.

Components that contain non-manifold edges are **excluded** from the check (they cannot be evaluated cleanly) and emit an INFO note. They do not cause a FAIL on this check.

**Warning Condition**

- Mesh has custom normals (`mesh.has_custom_normals == True`). The check skips and emits WARNING `"Custom normals present; consistency check skipped."`
- Mesh is above the polycount cap. The check skips and emits WARNING `"Mesh too large to inspect (>500k polygons); run on simplified geometry."`

**Fail Condition**

- At least one connected manifold component has at least one edge whose two linked faces traverse the edge endpoints in the same direction.

**Output Message**

- PASS: `"Face winding is consistent across all inspected meshes."`
- FAIL: `"N object(s) have inconsistent face winding: <object names>."`
- WARNING (custom normals or oversize): as above.

**Affected Object Reporting**

`affected_objects` lists object names. The specific failing edges are not surfaced in v1; the user opens the object and uses Blender's built-in tools to inspect.

**False Positive Risk**

Medium-High under naive implementations; Medium under the conservative implementation above. Sources of risk: open meshes (cards, planes, hair sheets) — the check operates on connected manifold components and skips non-manifold ones, so open patches without internal contradiction will pass. Hard-surface assets with intentional inward faces are still permitted as long as winding inside the component is internally consistent.

**Implementation Difficulty**

Medium-High. The most expensive and subtle of the five checks. If the false-positive rate during dogfooding exceeds 10% on real test files, the severity is demoted to WARNING for the v1 release per `ARCHITECTURE_MVP_V1.md` Section 7.

**Estimated Runtime Cost**

Medium. BMesh construction is O(verts + edges + faces); component traversal is O(edges). Skipped above the polycount cap.

---

## 3. Severity System

Three result statuses on a `CheckResult`:

| Status | Meaning |
|---|---|
| `PASS` | The check ran and found no problems. |
| `WARNING` | The check ran and found a non-blocking concern (degraded data, skip condition, or a defect that does not necessarily prevent delivery). |
| `FAIL` | The check ran and found a defect that the spec defines as blocking. |

One severity tag on a `CheckResult` (independent of status, set by the check definition):

| Severity | Meaning |
|---|---|
| `BLOCKER` | A `FAIL` on this check changes the verdict to NOT READY regardless of score. |
| `WARNING` | A `FAIL` on this check lowers the score but does not by itself change the verdict from READY to NOT READY. |
| `INFO` | Informational only. Does not affect score or verdict. Used for skip notes and linked-object reports. |

### When FAIL is BLOCKER vs ordinary FAIL

In v1, the mapping is fixed per check:

| Check | If `status == FAIL`, severity is | If `status == WARNING`, severity is |
|---|---|---|
| 01 Texture Presence | BLOCKER | INFO (e.g., unsaved file note) |
| 02 Material Assignment | BLOCKER | WARNING (empty slot, legacy material) |
| 03 Applied Scale | BLOCKER | n/a (no warning state defined) |
| 04 UV Existence | BLOCKER | WARNING (degenerate active layer with non-degenerate alternative) |
| 05 Normal Consistency | BLOCKER (held back to WARNING for v1.0 if false-positive rate is uncertain) | INFO (custom normals skip, oversize skip) |

A `WARNING` status never escalates to a BLOCKER even if many objects are affected. A `FAIL` status on a BLOCKER-tagged check makes the report NOT READY regardless of how many objects are affected.

There is exactly one `CheckResult` per check per run. Severity is fixed by the check, not derived from the affected object count.

---

## 4. Ready For Delivery Score

### Starting score

100.

### Deduction rules

- Each `CheckResult` with `status == FAIL` and severity `BLOCKER`: -15.
- Each `CheckResult` with `status == FAIL` and severity `WARNING`: -5.
- Each `CheckResult` with `status == WARNING` and severity `WARNING`: -3.
- `INFO` and `PASS` do not deduct.

Score is clamped to `[0, 100]`. With five BLOCKER checks each at -15, the minimum from natural deductions is 25; the cap rules below override that downward when needed.

### Cap rules (apply after deductions)

- Three or more `FAIL` results on BLOCKER-severity checks: cap displayed score at 49.
- Five `FAIL` results on BLOCKER-severity checks (i.e., everything failed): cap displayed score at 29.

### Blocking logic

- Any `FAIL` on a BLOCKER-severity check forces verdict = `NOT READY`.
- No combination of `WARNING` results can produce `NOT READY`. They lower the score and shift the verdict at most from `READY` to `READY WITH WARNINGS`.

### Verdict states

| Verdict | Conditions |
|---|---|
| `READY` | Score >= 90 AND zero `FAIL` results on BLOCKER-severity checks AND zero `WARNING` statuses. |
| `READY WITH WARNINGS` | Score >= 70 AND zero `FAIL` results on BLOCKER-severity checks AND at least one `WARNING` status. |
| `NOT READY` | Any `FAIL` on a BLOCKER-severity check, OR score < 70. |

### Examples

Example A — clean file:

```
Score: 100
PASS, PASS, PASS, PASS, PASS
Verdict: READY
```

Example B — one missing UV map and one empty material slot warning:

```
PASS (textures), WARNING (materials, -3), PASS (scale), FAIL (UV, -15), WARNING-skip (normals, INFO 0)
Score: 100 - 3 - 15 = 82
Verdict: NOT READY  (because UV is BLOCKER-severity)
```

Example C — three blocker fails:

```
FAIL (textures, -15), FAIL (materials, -15), PASS (scale), FAIL (UV, -15), PASS (normals)
Raw score: 100 - 45 = 55. Cap rule: three blocker fails → cap at 49.
Score: 49
Verdict: NOT READY
3 Blocking Issues, 0 Warnings
```

Example D — warnings only:

```
PASS (textures), WARNING (materials, -3), PASS (scale), WARNING (UV, -3), PASS (normals)
Score: 100 - 3 - 3 = 94
Verdict: READY WITH WARNINGS
0 Blocking Issues, 2 Warnings
```

---

## 5. Report Output Specification

The report is rendered in the side panel and produced as a structured payload (see Section 7). The text output follows this format exactly:

```
Pipeline Inspector Report

<VERDICT>
Score: <0-100>
<B> Blocking Issue(s)
<W> Warning(s)

Checks:
<status_icon> 01 Texture Presence — <one-line message>
<status_icon> 02 Material Assignment — <one-line message>
<status_icon> 03 Applied Scale — <one-line message>
<status_icon> 04 UV Existence — <one-line message>
<status_icon> 05 Normal Consistency — <one-line message>

Issues:
- [BLOCKER] 04 UV Existence: Object 'rock_03' is missing a UV map.
- [BLOCKER] 04 UV Existence: Object 'rock_07' has an empty UV map.
- [WARNING] 02 Material Assignment: Object 'crate_a' has an empty material slot at index 1.
```

Rules:

- `<VERDICT>` is one of `READY FOR DELIVERY`, `READY WITH WARNINGS`, `NOT READY FOR DELIVERY`. Verdict is the headline, score is the supporting number.
- `<status_icon>` is `PASS`, `WARN`, or `FAIL`. v1 uses text tokens, not unicode glyphs, so the report renders the same in a copied report and in the panel.
- The `Checks:` block always lists all five checks in the fixed order shown above, regardless of status.
- The `Issues:` block lists per-object findings. Each line has the format `[SEVERITY] <check id> <check name>: <object-specific reason>`. If a check has more than 50 affected objects, the list is truncated and a final line reads `(... and N more in CheckResult.affected_objects)`.
- If the run has zero issues, the `Issues:` block is omitted entirely (do not render an empty heading).
- Date/time and Blender version are included as a footer line: `Generated <ISO-8601 local time> on Blender <version>`.

Example — READY WITH WARNINGS:

```
Pipeline Inspector Report

READY WITH WARNINGS
Score: 86
0 Blocking Issue(s)
2 Warning(s)

Checks:
PASS  01 Texture Presence — All referenced textures are packed or reachable.
WARN  02 Material Assignment — 1 object(s) have empty or legacy material slots: crate_a.
PASS  03 Applied Scale — All mesh objects have applied scale.
WARN  04 UV Existence — 1 object(s) have a degenerate active UV layer: prop_01.
PASS  05 Normal Consistency — Face winding is consistent across all inspected meshes.

Issues:
- [WARNING] 02 Material Assignment: Object 'crate_a' has an empty material slot.
- [WARNING] 04 UV Existence: Object 'prop_01' has a degenerate active UV layer.

Generated 2026-06-04T10:12:33 on Blender 4.2.0
```

---

## 6. Blender UI Specification

No UI mockups, no layouts, no styling. v1 defines only the locations and named affordances.

### Panel Location

- Space type: `VIEW_3D`.
- Region: `UI` (the right-hand N-panel).
- Tab/category: `Pipeline Inspector`.
- One panel: `Pipeline Inspector`. No sub-panels in v1.

### Buttons

The panel exposes exactly one operator button:

- `Run Inspection` — triggers a fresh run over the current scene and replaces any previous result.

No "Clear", no "Export Report", no "Settings", no "Auto-run on save". Those are post-v1.

### Result Area

A single result block inside the panel that contains, in order:

1. **Score Area** — one line. The verdict in large weight, the score in smaller weight on the same line. Example content: `READY WITH WARNINGS — Score: 86`.
2. **Counts Area** — one line. Example content: `0 Blocking · 2 Warnings`.
3. **Checks List Area** — five rows, one per check, in the fixed order from Section 5. Each row shows: status token, check id, check name, one-line message.
4. **Issues Area** — collapsible (default expanded). Lists every issue line in the format from Section 5.
5. **Footer Area** — generation timestamp and Blender version.

If no run has occurred in the current session, the result area shows a single placeholder line: `No inspection run yet. Press Run Inspection.`

### Report Area

There is no separate "Report" surface in v1. The panel is the report. Issues are not exported to a file in v1.

### Score Area

Defined above (item 1 of the result area). The verdict text is the load-bearing element; the numeric score is supporting context. v1 does not display historical score trends.

---

## 7. Data Structures

Field-only definitions. No code, no method signatures.

### `CheckResult`

- `id` : string. Stable check id, e.g. `"01_texture_presence"`. Sorted ordering.
- `name` : string. Human-readable, e.g. `"Texture Presence"`.
- `status` : enum. One of `PASS`, `WARNING`, `FAIL`.
- `severity` : enum. One of `BLOCKER`, `WARNING`, `INFO`. Fixed per check (see Section 3).
- `message` : string. One-line summary, fixed wording per outcome.
- `affected_objects` : list of strings. Object names. Sorted alphabetically. Capped at 50 with overflow note.
- `evidence_reason` : string. Concrete reason text, used for the `Issues:` lines.
- `issues` : list of `IssueRecord`. Per-object detail rows. Empty for `PASS`.

### `InspectionResult`

- `results` : list of `CheckResult`. Always five entries in v1, in fixed id order.
- `score` : integer in `[0, 100]`.
- `verdict` : enum. One of `READY`, `READY_WITH_WARNINGS`, `NOT_READY`.
- `blocker_count` : integer. Count of `CheckResult` with `status == FAIL` and `severity == BLOCKER`.
- `warning_count` : integer. Count of `CheckResult` with `status == WARNING`, plus count with `status == FAIL` and `severity == WARNING`.
- `generated_at` : datetime. Local time, ISO-8601 string in the report.
- `blender_version` : string. From `bpy.app.version_string`.
- `total_objects_inspected` : integer. Number of visible non-linked mesh objects considered.

### `IssueRecord`

- `check_id` : string. Foreign key to `CheckResult.id`.
- `severity` : enum. Inherited from the parent `CheckResult.severity`.
- `object_name` : string. The Blender object name. Empty string for scene-level issues (e.g., unsaved-file warning).
- `reason` : string. Object-specific reason, used in `Issues:` lines.
- `detail` : string. Optional secondary line (e.g., the offending image name, the offending UV layer name, the slot index). Empty if not applicable.

Constraints:

- `IssueRecord` is the only place per-object detail lives. `CheckResult.affected_objects` is the deduplicated, sorted projection of `IssueRecord.object_name` for that check.
- All three structures are plain-data records. No methods, no Blender references, no live pointers.

---

## 8. Development Order

Build in five phases. Each phase ends with the result observable in the panel.

### Phase 1 — Skeleton + Scoring

- Create the add-on registration shell, the side panel, the `Run Inspection` operator, and the empty result area.
- Implement `scoring.py` as a pure function over a list of `CheckResult`. Unit-testable without Blender.
- The `Run Inspection` operator at this stage produces a static "all PASS" result, exercising the data flow end-to-end.

**Why first**: forces the module structure, the data contracts, and the report format to be locked before any check is written. Mistakes here are cheap; mistakes after three checks are not.

### Phase 2 — Check 03 Applied Scale

- Implement `checks/transforms.py` with the scale check.
- Lowest false-positive risk, smallest code surface, hardest to get wrong.

**Why second**: validates the per-object iteration pattern and the `affected_objects` reporting against the simplest possible predicate.

### Phase 3 — Check 04 UV Existence

- Implement `checks/uvs.py` with both the missing-layer FAIL path and the degenerate-layer WARNING path.

**Why third**: introduces per-loop iteration on mesh data, the polycount cap pattern, and the WARNING/FAIL distinction within one check.

### Phase 4 — Check 01 Texture Presence + Check 02 Material Assignment

- Implement `checks/textures.py` and `checks/materials.py`. Bundle them because both walk material node graphs and the `obj → material → image` traversal is shared logic.
- Texture check first inside this phase (its rules are simpler), then material assignment.

**Why fourth**: by this point the framework is mature enough to absorb the more nuanced node-graph logic without distorting earlier patterns.

### Phase 5 — Check 05 Normal Consistency

- Implement `checks/normals.py` with the conservative manifold-component algorithm.
- Run dogfood testing across a small library of real .blend files (assets the team has on hand). Track false-positive rate.
- If false-positive rate exceeds 10% on real files, demote severity to `WARNING` for v1.0 (per `ARCHITECTURE_MVP_V1.md` Section 7) and ship.

**Why last**: highest false-positive risk, highest implementation difficulty, most likely to slip. Building it last means an overrun on this check does not block the four checks the user can already benefit from in a v0.5 internal release.

---

## 9. Risk Register

### Highest false-positive risk

1. **Check 05 Normal Consistency.** Source: distinguishing intentional inward faces and open meshes from genuinely contradictory winding. Mitigation: scope to "inconsistent winding within manifold component," skip non-manifold components, skip custom-normaled meshes, demote to WARNING for v1.0 if dogfood rate exceeds 10%.
2. **Check 01 Texture Presence.** Source: relative path resolution against unsaved files, UDIM partial-tile coverage, packed-but-stale images. Mitigation: WARNING-and-skip on unsaved file, INFO on partial UDIM, treat packed files as authoritative regardless of disk state.
3. **Check 04 UV Existence.** Source: deliberate tiny UVs misclassified as degenerate. Mitigation: small `UV_BBOX_EPSILON`; the trade-off is documented and accepted.

### Highest performance risk

1. **Check 05 Normal Consistency.** BMesh construction on heavy meshes is the main cost driver. Mitigation: hard polycount cap (default 500k polygons), skip with WARNING above the cap.
2. **Check 04 UV Existence non-empty path.** Per-loop bounding box on heavy meshes. Mitigation: same polycount cap.
3. **Check 01 Texture Presence on network drives.** `os.path.exists` can stall on slow shares. Mitigation: 200ms timeout per file, treat timeout as FAIL with a "(unreachable: timeout)" reason.

### Hardest to implement

1. **Check 05 Normal Consistency.** BMesh component traversal, manifold predicate, edge orientation comparison. Most code, most edge cases.
2. **Check 02 Material Assignment.** Output node detection across material variants (Eevee/Cycles, multiple OUTPUT_MATERIAL nodes selected by render engine, world materials should be ignored).
3. **Check 01 Texture Presence.** UDIM tile expansion, `//` path resolution, `Image.source` enum coverage.

### Highest impact on user trust

1. **Check 05 Normal Consistency.** A false BLOCKER on a hard-surface asset trains the user to ignore the score.
2. **Check 04 UV Existence.** A false BLOCKER on an unwrap-in-progress file produces noise on every save.
3. **Score cap rules.** If the cap rules surprise the user (e.g., they fix one issue and the score does not move because the cap still binds), trust drops. The report must state that a cap is in effect when applicable.

`evidence/payment-evidence.md` flags noisy warnings as a kill signal. Trust risks are graded above implementation risks because the v1 release succeeds or fails on whether users believe the verdict.

---

## 10. Final Decision

# LIMITED GO

Pipeline Inspector v1 may enter Development Phase. Scope is locked to the five checks specified in Section 2, the data structures in Section 7, the score and verdict rules in Sections 3-4, and the UI shell in Section 6.

### Allowed development scope (this phase)

- All Phase 1-5 work in Section 8.
- All five checks listed in Section 2.
- The single panel and single operator described in Section 6.
- The `CheckResult`, `InspectionResult`, and `IssueRecord` records described in Section 7.

### Not allowed in this phase

- Any check beyond the five listed (including the deferred rotation/orientation and export-selection checks).
- Auto-fix, settings UI, presets, save handlers, background timers, telemetry, cloud, AI, team features.
- Any change to the score formula, cap rules, or verdict thresholds without a written amendment to this spec.
- Multi-version compatibility shims. Target Blender 4.2 LTS only.

### Conditions for a follow-up GO

A v1.1 spec may be authored — and only authored — once v1.0 has shipped to dogfood users and the following gates from `evidence/payment-evidence.md` and `evidence/go-no-go-report.md` are met:

- At least one user reports the tool caught a real issue before export or upload.
- False-positive rate on the five checks is low enough that warnings are not described as noisy.
- 5-10 users express willingness to pay $5-$9 for the v1 score.

If these gates fail, the next step is reframe or stop, not feature expansion.

LIMITED GO is the correct verdict for entering Development Phase.
