# Runtime Validation Protocol — Check 03 & Check 04

Owner role: Runtime QA Lead (protocol author)
Executor role: Codex (collects runtime evidence inside Blender)

This protocol defines the exact Blender runtime validation for the two real
checks currently implemented:

- **Check 03 — Applied Scale** (`03_applied_scale`, BLOCKER)
- **Check 04 — UV Existence** (`04_uv_existence`, BLOCKER + WARNING path)

Checks **01 Texture**, **02 Material**, and **05 Normal** are scaffold
placeholders. They are **non-validating**: they must render as `SKIP`
(status `NOT_IMPLEMENTED`, severity `INFO`) and must never affect score or
verdict. Do not treat them as PASS or as evidence of anything.

This document is a test plan only. It does **not** modify code, does **not**
implement new checks, and is **not** to be committed alongside code changes
until Codex returns runtime evidence.

---

## 0. Scope and Ground Rules

- Inspection is **read-only**. No scene mutation, no auto-repair. If running a
  check changes the scene in any way, that is an automatic FAIL of this
  protocol.
- The inspector gathers mesh objects as: `obj.type == "MESH"` **and**
  `obj.visible_get()` is True **and** `obj.library is None` (linked/library
  objects are skipped). Hidden objects and non-mesh objects are not inspected.
- One `CheckResult` is produced per check, not per object. Affected object
  names are deduplicated, sorted alphabetically, and capped.
- Report status tokens: `PASS`, `WARN`, `FAIL`, `SKIP`.

---

## 1. Environment & Scoring Reference

Record once at the top of the evidence report:

- Blender version (the add-on reports `bpy.app.version_string`).
- OS and build.
- Add-on package installed: `PipelineInspector_Scaffold_v0.1.zip`.
- Date of test run.

Scoring rules that govern expected verdicts (from `scoring.derive`):

| Event | Effect |
|---|---|
| Start | 100 |
| FAIL + BLOCKER | −15 |
| FAIL + WARNING severity | −5 |
| WARNING status | −3 |
| ≥3 blockers | score capped at max 49 |
| ≥5 blockers | score capped at max 29 |
| PASS / NOT_IMPLEMENTED / INFO | no change |

Verdict mapping:

- Any blocker present, or score < 70 → **NOT READY FOR DELIVERY**.
- No blocker, but ≥1 warning → **READY WITH WARNINGS**.
- Otherwise → **READY FOR DELIVERY**.

---

## 2. Install & Enable (run once, before any test scene)

1. Launch Blender with factory settings (`File → Defaults → Load Factory
   Settings`) so no prior add-on state interferes.
2. `Edit → Preferences → Add-ons → Install…`
3. Select `PipelineInspector_Scaffold_v0.1.zip` and confirm.
4. Search "Pipeline Inspector" in the Add-ons list and tick the checkbox to
   enable it.
5. In the 3D Viewport press **N** to open the sidebar.
6. Confirm a tab labelled **Pipeline Inspector** appears in the sidebar.
7. Click the tab. Confirm a **Run Inspection** button is visible, and that
   before any run the panel shows: `No inspection run yet. Press Run
   Inspection.`

**Evidence for §2:**
- E2.1 — screenshot of the Add-ons list showing Pipeline Inspector enabled.
- E2.2 — screenshot of the N-panel with the Pipeline Inspector tab and the
  Run Inspection button, in the pre-run state.
- E2.3 — Blender system console open (`Window → Toggle System Console`),
  showing no errors/tracebacks after enable.

**§2 PASS criteria:** add-on installs and enables without error, tab is
present, Run Inspection button is present, console is clean.

---

## 3. General Per-Scene Procedure

For each test scene below:

1. Build the scene exactly as described (start from factory settings each time;
   delete the default cube unless the scene reuses it).
2. Press **N**, open the Pipeline Inspector tab.
3. Click **Run Inspection** once.
4. Read the panel output and compare against the **Expected** block.
5. Collect the listed evidence.
6. Confirm the system console shows no Python errors or tracebacks.
7. Confirm the scene is unchanged after the run (object scales, UV layers, and
   selection are exactly as before — the inspection is read-only).

The summary block at the top of the report always has this shape:

```
<VERDICT TEXT>
Score: <n>
<b> Blocking Issue(s)
<w> Warning(s)

Checks:
<TOKEN>  <id>  <name>[ — <message> for SKIP rows]
...
```

Placeholder rows must always appear and always read `SKIP`, for example:

```
SKIP  01_texture_presence  Texture Presence — Not implemented yet — this check did not inspect anything.
SKIP  02_material_assignment  Material Assignment — Not implemented yet — this check did not inspect anything.
SKIP  05_normal_consistency  Normal Consistency — Not implemented yet — this check did not inspect anything.
```

If any of 01/02/05 ever shows `PASS`/`WARN`/`FAIL`, that is an automatic FAIL
of this protocol.

---

## 4. Check 03 — Applied Scale

Behavior under test: a visible non-linked mesh whose **object** scale (or
delta scale) is not 1,1,1 within `SCALE_EPSILON` (1e-4) FAILs as a BLOCKER.
Edit-Mode geometry scaling does **not** count — only object-level scale.

### Scene 3A — Applied scale → PASS

Setup:
1. Default cube. With the cube selected, set Scale to 2.0 on all axes
   (`N` panel → Item → Scale, or `S 2 Enter`).
2. Apply scale: `Object → Apply → Scale` (`Ctrl+A → Scale`). Object scale is
   now back to 1,1,1; geometry retains the size.
3. Run Inspection.

Expected:
- Verdict: **READY FOR DELIVERY**
- Score: **100**
- Blocking Issue(s): **0**
- Warning(s): **0**
- Check 03 row: `PASS  03_applied_scale  Applied Scale`
- Detail block contains: `All inspected mesh objects have Object Scale = 1,1,1.`

### Scene 3B — Unapplied scale → FAIL

Setup:
1. Default cube named `Cube`. Set Scale to 2.0 on all axes. **Do not apply.**
2. Run Inspection.

Expected:
- Verdict: **NOT READY FOR DELIVERY**
- Score: **85**
- Blocking Issue(s): **1**
- Warning(s): **0**
- Check 03 row: `FAIL  03_applied_scale  Applied Scale`
- Detail block exact message: `1 object(s) have unapplied scale: Cube.`
- Affected Objects lists `Cube`; Current Scale shows per-axis values
  (e.g. `X: 2.0`, `Y: 2.0`, `Z: 2.0`).

### Scene 3C — Mixed, multiple offenders → FAIL, sorted

Setup:
1. `Cube_Applied`: scale 2.0 all axes, then Apply Scale (back to 1,1,1).
2. `Cube_Scaled`: scale 2.0 all axes, do **not** apply.
3. `Plane_Scaled`: scale 0.5 all axes, do **not** apply.
4. Run Inspection.

Expected:
- Verdict: **NOT READY FOR DELIVERY**
- Score: **85** (one FAIL check = one BLOCKER deduction; the check emits a
  single CheckResult regardless of offender count)
- Blocking Issue(s): **1**
- Warning(s): **0**
- Check 03 row: `FAIL  03_applied_scale  Applied Scale`
- Detail block exact message, alphabetically sorted:
  `2 object(s) have unapplied scale: Cube_Scaled, Plane_Scaled.`
- `Cube_Applied` must **not** appear in the affected list.

### Check 03 evidence (per scene)

- E3x.1 — screenshot of the N-panel summary (verdict, score, counts).
- E3x.2 — screenshot of the Check 03 detail block (message + affected
  objects).
- E3x.3 — screenshot of the Item panel showing each object's scale values
  (proves the setup matched the expectation).
- E3x.4 — system console screenshot with no errors.

---

## 5. Check 04 — UV Existence

Behavior under test:

- **FAIL (BLOCKER)** when a mesh has no UV map, or has a UV map whose active
  layer contains no UV data.
- **WARNING** when a mesh has **more than one** UV layer, the **active** layer
  is degenerate (all UV coords collapse to a point within `UV_BBOX_EPSILON`,
  1e-5), and at least one **non-active** layer carries usable, non-degenerate
  UV data.
- **PASS** otherwise.
- FAIL always takes precedence over WARNING when both occur in the same scene.

This check verifies UV **existence** only. It does not validate UV quality,
overlap, texel density, or layout (out of v1 scope per CLAUDE.md §6).

### Scene 4A — UV present → PASS

Setup:
1. Default cube. In Edit Mode (`Tab`), select all (`A`), unwrap
   (`U → Unwrap`). This produces a non-empty active UV layer.
2. Return to Object Mode. Run Inspection.

Expected:
- Verdict: **READY FOR DELIVERY**
- Score: **100**
- Blocking Issue(s): **0**
- Warning(s): **0**
- Check 04 row: `PASS  04_uv_existence  UV Existence`
- Detail block contains: `All inspected mesh objects have a UV map.`

### Scene 4B — No UV map → FAIL

Setup:
1. Add a mesh named `Cube`. Open the Object Data Properties (green triangle) →
   **UV Maps**. Delete every UV map so the list is empty.
2. Run Inspection.

Expected:
- Verdict: **NOT READY FOR DELIVERY**
- Score: **85**
- Blocking Issue(s): **1**
- Warning(s): **0**
- Check 04 row: `FAIL  04_uv_existence  UV Existence`
- Detail block exact message: `1 object(s) have no usable UV map: Cube.`
- Affected Objects shows `Cube` with reason `Object has no UV map.`

### Scene 4C — UV map exists but empty → FAIL

Setup:
1. Create a mesh that has a UV layer but **zero loop data** in it (a mesh with
   no faces — e.g. a single vertex or loose edges converted to a mesh — that
   still carries a named UV map). The active UV layer exists but
   `len(active.data) == 0`.
2. Name it `Cube`. Run Inspection.

Expected:
- Verdict: **NOT READY FOR DELIVERY**
- Score: **85**
- Blocking Issue(s): **1**
- Warning(s): **0**
- Check 04 row: `FAIL  04_uv_existence  UV Existence`
- Detail block exact message: `1 object(s) have no usable UV map: Cube.`
- Reason shown: `UV map exists but contains no UV data.`

Note: if building a genuinely empty-but-present UV layer interactively is not
practical, document the attempt and the observed result. Scenes 4B and 4D are
the mandatory FAIL/WARNING gates; 4C is confirmatory.

### Scene 4D — Degenerate active layer with good alternative → WARNING

Setup:
1. Add a mesh named `prop_01` and unwrap it normally (gives a real spread UV
   layer).
2. In Object Data Properties → UV Maps, add a **second** UV map and make it the
   **active** one.
3. Collapse the active layer's UVs to a single point: in the UV Editor select
   all UVs and scale to 0 (`S 0 Enter`), or merge/snap them to one coordinate,
   so the active layer's bounding box is ~0 on both axes (≤ 1e-5).
4. Ensure the **other** (non-active) layer still holds the spread unwrap.
5. Run Inspection.

Expected:
- Verdict: **READY WITH WARNINGS**
- Score: **97** (WARNING status = −3)
- Blocking Issue(s): **0**
- Warning(s): **1**
- Check 04 row: `WARN  04_uv_existence  UV Existence`
- Detail block exact message:
  `1 object(s) have a degenerate active UV layer: prop_01.`
- Reason shown: `Active UV layer appears unused; another layer has data.`

Negative controls (each should **not** warn — confirm they PASS):
- Single degenerate layer only (no alternative) → PASS.
- All layers degenerate → PASS.
- Active layer non-degenerate, a secondary layer degenerate → PASS.

### Scene 4E — FAIL precedence over WARNING

Setup:
1. `missing`: a mesh with **no** UV map (as in 4B).
2. `degen`: a multi-layer mesh with a degenerate active layer and a good
   alternate (as in 4D).
3. Run Inspection.

Expected:
- Verdict: **NOT READY FOR DELIVERY**
- Score: **85**
- Blocking Issue(s): **1**
- Warning(s): **0** (the FAIL path owns the result; the degenerate-active
  WARNING does not also fire when any object FAILs)
- Check 04 row: `FAIL  04_uv_existence  UV Existence`
- Detail block exact message: `1 object(s) have no usable UV map: missing.`
- `degen` must **not** appear as a warning in this run.

### Check 04 evidence (per scene)

- E4x.1 — screenshot of the N-panel summary (verdict, score, counts).
- E4x.2 — screenshot of the Check 04 detail block (message + affected
  objects + reasons).
- E4x.3 — screenshot of the Object Data Properties → UV Maps list (and the UV
  Editor for 4D) proving the setup matched the expectation.
- E4x.4 — system console screenshot with no errors.

---

## 6. Placeholder Checks 01 / 02 / 05 — Non-Validating

In every scene above, confirm:

- `01_texture_presence`, `02_material_assignment`, `05_normal_consistency` each
  render with the `SKIP` token and the "Not implemented yet…" message.
- They contribute **0** to blocker count, warning count, and score.
- They are never reported as PASS.

These checks are evidence of nothing. Do not record them as validated.

---

## 7. Overall PASS / FAIL Judgment

This runtime validation is a **PASS** only if **all** of the following hold:

1. §2 install/enable/N-panel/Run-Inspection all succeed with a clean console.
2. Every Check 03 scene (3A, 3B, 3C) matches its Expected block exactly —
   verdict, score, blocker/warning counts, and the exact message string.
3. Every Check 04 mandatory scene (4A, 4B, 4D, 4E) matches its Expected block
   exactly. 4C matches, or its limitation is documented with the observed
   result.
4. All Check 04 negative controls PASS (no spurious warnings).
5. Placeholders 01/02/05 show `SKIP` in every run and never affect scoring.
6. No scene is mutated by running the inspection (read-only contract holds).
7. No Python errors or tracebacks appear in the system console at any point.

Any single mismatch is a **FAIL** for that case. Report the exact observed
verdict/score/counts/message alongside the expected values; do not round,
paraphrase, or "fix up" observed output.

## 8. Evidence Packaging

Codex returns:

- One Markdown evidence report with a section per scene (§2, 3A–3C, 4A–4E),
  each stating Expected vs Observed and embedding the screenshots listed above.
- The environment block from §1 (Blender version, OS, package, date).
- An explicit final line: overall PASS or FAIL, with the count of cases passed.

Do not commit code or status-document changes claiming runtime validation has
passed until this evidence is returned and reviewed (CLAUDE.md §8).

## 9. Known Code / Spec Discrepancies (for reviewer awareness)

Surfaced per CLAUDE.md §10 (report disagreements rather than hide them). These
do **not** block the protocol; they flag where runtime strings differ from
`IMPLEMENTATION_SPEC_V1.md`, so judge runtime output against the **code's**
actual strings quoted in this document:

- **Check 04 PASS message.** Code (`uvs.py`) emits `All mesh objects have UV
  maps.`; the N-panel PASS detail uses `All inspected mesh objects have a UV
  map.`; the spec text says `All mesh objects have a non-empty UV map.` Expect
  the panel detail string above at runtime.
- **Check 04 FAIL message.** Code emits `N object(s) have no usable UV map:
  <names>.`; the spec wording is `N object(s) are missing UV maps or have empty
  UVs: <names>.` Expect the code string.
- **RUNTIME_VALIDATION.md location.** CLAUDE.md §4 references it as a
  root-level doc, but it currently lives at `docs/archive/RUNTIME_VALIDATION.md`.






