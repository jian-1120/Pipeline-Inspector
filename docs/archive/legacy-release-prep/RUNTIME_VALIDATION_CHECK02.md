# Runtime Validation Checklist — Check 02 Material Assignment

Owner role: Runtime QA Lead (protocol author)
Executor role: Codex (collects runtime evidence inside Blender)

This checklist defines the exact Blender runtime validation for the
newly-implemented real check:

- **Check 02 — Material Assignment** (`02_material_assignment`, BLOCKER + WARNING path)

Status note: as of this document, Check 02 has real read-only logic and full
pytest coverage (`tests/test_check_02_material_assignment.py`,
`tests/test_report_material_assignment.py`). It has **not** yet been validated
inside Blender. This checklist is a test plan only. It does **not** modify code
and is **not** evidence of runtime success until Codex returns observations.

Checks **01 Texture**, **03 Applied Scale**, and **04 UV Existence** are real
and validated elsewhere. **Check 05 Normal** remains a scaffold placeholder and
must render as `SKIP` (status `NOT_IMPLEMENTED`, severity `INFO`) and never
affect score or verdict.

---

## 0. Scope and Ground Rules

- Inspection is **read-only**. No scene mutation, no auto-repair. If running a
  check changes the scene (materials, slots, node graphs, selection), that is an
  automatic FAIL of this protocol.
- The inspector gathers mesh objects as: `obj.type == "MESH"` **and**
  `obj.visible_get()` is True **and** `obj.library is None`. Hidden objects,
  non-mesh objects, and linked/library objects are not inspected.
- One `CheckResult` is produced per check, not per object. Affected object names
  are deduplicated, sorted alphabetically, and capped at 50.
- Report status tokens: `PASS`, `WARN`, `FAIL`, `SKIP`.

---

## 1. Check 02 Behaviour Under Test

Per `IMPLEMENTATION_SPEC_V1.md` Section 2, Check 02, and the implemented
`pipeline_inspector/checks/materials.py`:

- **PASS** — every visible non-linked mesh object has at least one material slot,
  at least one assigned material, and at least one assigned material whose node
  graph has an `OUTPUT_MATERIAL` node with a connected `Surface` input. A flat
  colour / procedural node material with a connected surface PASSes; texture
  presence is **not** required (that is Check 01).
- **FAIL (BLOCKER)** when an object:
  - has **zero** material slots, OR
  - has slots but **none** carry an assigned material, OR
  - has assigned materials but **every** one is a node material with a
    disconnected `Surface` output (or no `OUTPUT_MATERIAL` node, or `use_nodes`
    True with no `node_tree`).
- **WARNING** when an object has at least one valid material but also:
  - carries one or more empty slots while having more than one slot, OR
  - includes a legacy (`use_nodes == False`) material.
  A legacy material with **no** valid node material present also WARNs (a legacy
  material still exports a base colour, so per spec the check "proceeds").
- FAIL always takes precedence over WARNING when both occur in the same scene.

Scoring reference (`scoring.derive`):

| Event | Effect |
|---|---|
| Start | 100 |
| FAIL + BLOCKER | −15 |
| WARNING status | −3 |
| ≥3 blockers | score capped at max 49 |
| PASS / NOT_IMPLEMENTED / INFO | no change |

Verdict mapping: any blocker present or score < 70 → **NOT READY FOR DELIVERY**;
no blocker but ≥1 warning → **READY WITH WARNINGS**; otherwise → **READY FOR
DELIVERY**.

Exact runtime strings (judge runtime output against these code strings):

- PASS message (CheckResult): `All mesh objects have export-relevant materials.`
- PASS detail (N-panel): `All inspected mesh objects have export-relevant materials.`
- FAIL message: `N object(s) have missing or disconnected materials: <names>.`
- WARNING message: `N object(s) have empty or legacy material slots: <names>.`

---

## 2. Install & Enable (run once, before any test scene)

1. Launch Blender with factory settings (`File → Defaults → Load Factory
   Settings`).
2. Install and enable the Pipeline Inspector add-on (the package containing the
   updated `checks/materials.py`).
3. In the 3D Viewport press **N**, open the **Pipeline Inspector** tab.
4. Confirm the **Run Inspection** button is visible, and that before any run the
   panel shows: `No inspection run yet. Press Run Inspection.`

**Evidence for §2:**
- E2.1 — screenshot of the Add-ons list showing Pipeline Inspector enabled.
- E2.2 — screenshot of the N-panel pre-run state.
- E2.3 — system console (`Window → Toggle System Console`) showing no errors
  after enable.

---

## 3. General Per-Scene Procedure

For each test scene:

1. Build the scene exactly as described (start from factory settings; delete the
   default cube unless the scene reuses it).
2. Press **N**, open the Pipeline Inspector tab.
3. Click **Run Inspection** once.
4. Read the panel output and compare against the **Expected** block.
5. Collect the listed evidence.
6. Confirm the system console shows no Python errors or tracebacks.
7. Confirm the scene is unchanged after the run (materials, slots, node links,
   and selection exactly as before — the inspection is read-only).

`05_normal_consistency` must render `SKIP` with the "Not implemented yet…"
message in every run. If it ever shows PASS/WARN/FAIL, that is an automatic FAIL
of this protocol.

---

## 4. Test Scenes

### Scene 2A — Connected node material → PASS

Setup:
1. Default cube named `Cube`. It carries a default material whose Principled
   BSDF is connected to the Material Output Surface (factory default).
2. Run Inspection.

Expected:
- Verdict: **READY FOR DELIVERY**
- Score: **100**
- Blocking Issue(s): **0**
- Warning(s): **0**
- Check 02 row: `PASS  02_material_assignment  Material Assignment`
- Detail block contains: `All inspected mesh objects have export-relevant materials.`

### Scene 2B — No material slots → FAIL

Setup:
1. Mesh named `Cube`. In Material Properties, remove all material slots (the `-`
   button) so the slot list is empty.
2. Run Inspection.

Expected:
- Verdict: **NOT READY FOR DELIVERY**
- Score: **85**
- Blocking Issue(s): **1**
- Warning(s): **0**
- Check 02 row: `FAIL  02_material_assignment  Material Assignment`
- Detail block exact message:
  `1 object(s) have missing or disconnected materials: Cube.`
- Affected Objects shows `Cube` with reason `Object has no material slots.`

### Scene 2C — Slot present, no material assigned → FAIL

Setup:
1. Mesh named `Cube`. Add a material slot with the `+` button but leave it
   **empty** (do not assign or create a material in it).
2. Run Inspection.

Expected:
- Verdict: **NOT READY FOR DELIVERY**
- Score: **85**
- Blocking Issue(s): **1**
- Check 02 row: `FAIL  02_material_assignment  Material Assignment`
- Detail block exact message:
  `1 object(s) have missing or disconnected materials: Cube.`
- Reason shown: `Object has material slots but none are assigned.`

### Scene 2D — Disconnected surface → FAIL

Setup:
1. Mesh named `Cube` with a node material. In the Shader Editor, delete the link
   between the BSDF and the Material Output `Surface` input (select the link and
   `X`/drag off), leaving the Surface input unconnected.
2. Run Inspection.

Expected:
- Verdict: **NOT READY FOR DELIVERY**
- Score: **85**
- Blocking Issue(s): **1**
- Check 02 row: `FAIL  02_material_assignment  Material Assignment`
- Detail block exact message:
  `1 object(s) have missing or disconnected materials: Cube.`
- Reason shown: `Assigned material has a disconnected surface output.`

### Scene 2E — Flat-colour / procedural material → PASS

Setup:
1. Mesh named `Cube` with a node material that has **no image texture** — e.g.
   an Emission or a plain Principled BSDF with a flat base colour — connected to
   the Material Output Surface.
2. Run Inspection.

Expected:
- Verdict: **READY FOR DELIVERY**
- Score: **100**
- Check 02 row: `PASS  02_material_assignment  Material Assignment`
- Confirms texture presence is **not** required by Check 02 (False-Positive
  guard, spec Section 2 Check 02).

### Scene 2F — Empty extra slot on a multi-slot object → WARNING

Setup:
1. Mesh named `crate_a` with a valid connected material in slot 0.
2. Add a **second** slot (`+`) and leave it empty.
3. Run Inspection.

Expected:
- Verdict: **READY WITH WARNINGS**
- Score: **97** (WARNING status = −3)
- Blocking Issue(s): **0**
- Warning(s): **1**
- Check 02 row: `WARN  02_material_assignment  Material Assignment`
- Detail block exact message:
  `1 object(s) have empty or legacy material slots: crate_a.`
- Reason shown: `Empty material slot at index 1.`

### Scene 2G — Legacy non-node material → WARNING

Setup:
1. Mesh named `legacy_obj` with an assigned material whose **Use Nodes** toggle
   is **off** (Material Properties → uncheck "Use Nodes").
2. Run Inspection.

Expected:
- Verdict: **READY WITH WARNINGS**
- Score: **97**
- Warning(s): **1**
- Check 02 row: `WARN  02_material_assignment  Material Assignment`
- Detail block exact message:
  `1 object(s) have empty or legacy material slots: legacy_obj.`
- Reason shown: `Material does not use nodes (legacy material).`

Note: recent Blender versions deprecate `Material.use_nodes`. If the toggle is
not exposable in the test build, document the attempt and observed result; 2F is
the mandatory WARNING gate, 2G is confirmatory.

### Scene 2H — FAIL precedence over WARNING

Setup:
1. `missing`: a mesh with **no** material slots (as in 2B).
2. `legacy_obj`: a mesh with a legacy material (as in 2G).
3. Run Inspection.

Expected:
- Verdict: **NOT READY FOR DELIVERY**
- Score: **85**
- Blocking Issue(s): **1**
- Warning(s): **0** (the FAIL path owns the result; the WARNING does not also
  fire when any object FAILs)
- Check 02 row: `FAIL  02_material_assignment  Material Assignment`
- Detail block exact message:
  `1 object(s) have missing or disconnected materials: missing.`
- `legacy_obj` must **not** appear as a warning in this run.

### Scene 2I — Multiple offenders, sorted

Setup:
1. `zebra`: no material slots.
2. `alpha`: disconnected surface.
3. `Good`: a valid connected material.
4. Run Inspection.

Expected:
- Verdict: **NOT READY FOR DELIVERY**
- Score: **85** (single CheckResult regardless of offender count)
- Blocking Issue(s): **1**
- Detail block exact message, alphabetically sorted:
  `2 object(s) have missing or disconnected materials: alpha, zebra.`
- `Good` must **not** appear in the affected list.

### Check 02 evidence (per scene)

- E2x.1 — screenshot of the N-panel summary (verdict, score, counts).
- E2x.2 — screenshot of the Check 02 detail block (message + affected objects +
  reasons).
- E2x.3 — screenshot of the Material Properties / Shader Editor proving the
  setup matched the expectation.
- E2x.4 — system console screenshot with no errors.

---

## 5. Negative Controls (must PASS — no spurious FAIL/WARN)

- Single valid connected material, single slot → PASS.
- Procedural material (Noise/Voronoi → BSDF → Output) with no image → PASS.
- One valid material + one disconnected material on the same object → PASS
  (FAIL requires **all** assigned materials disconnected).
- Object with one slot holding a valid material and no empty slots → PASS (no
  empty-slot WARNING for single-slot objects).

---

## 6. Overall PASS / FAIL Judgment

This runtime validation is a **PASS** only if **all** of the following hold:

1. §2 install/enable/N-panel/Run-Inspection succeed with a clean console.
2. Every mandatory scene (2A, 2B, 2C, 2D, 2E, 2F, 2H, 2I) matches its Expected
   block exactly — verdict, score, blocker/warning counts, and the exact message
   string. 2G matches or its limitation is documented with the observed result.
3. All negative controls in §5 PASS (no spurious findings).
4. Placeholder 05 shows `SKIP` in every run and never affects scoring.
5. No scene is mutated by running the inspection (read-only contract holds).
6. No Python errors or tracebacks appear in the system console at any point.

Any single mismatch is a **FAIL** for that case. Report the exact observed
verdict/score/counts/message alongside the expected values; do not round,
paraphrase, or "fix up" observed output.

---

## 7. Known Code / Spec Discrepancies (for reviewer awareness)

Surfaced per CLAUDE.md §10 (report disagreements rather than hide them). These
do **not** block the protocol; they record where the implementation made a
defensible choice on a spec ambiguity. Judge runtime output against the **code's**
actual strings quoted in §1.

- **PASS string differs between record and panel.** The `CheckResult.message`
  is `All mesh objects have export-relevant materials.` (spec Section 2, line
  178); the N-panel detail line is `All inspected mesh objects have
  export-relevant materials.` This mirrors the existing Check 01/03/04 pattern
  where the panel detail is phrased "All inspected mesh objects…".
- **Legacy material is WARNING, never FAIL.** Spec line 168 says a legacy
  material "is reported as WARNING and proceeds." The implementation therefore
  treats a legacy-only object as WARNING (not FAIL), even though such a material
  has no node `OUTPUT_MATERIAL` to evaluate. This is the spec's explicit
  instruction, not the disconnected-surface FAIL path.
- **Missing `OUTPUT_MATERIAL` node maps to FAIL.** The spec PASS condition (line
  163) requires an `OUTPUT_MATERIAL` node to exist with a connected Surface, but
  no FAIL clause explicitly names "no output node." The implementation classifies
  a node material with no output node as disconnected → FAIL, consistent with the
  spec's intent that an unshaded surface is a blocker. See implementation
  ambiguity notes in the delivery summary.
- **`use_nodes == True` with `node_tree is None`** is classified as disconnected
  → FAIL (the surface cannot be connected). The spec does not address this state.
- **Multiple `OUTPUT_MATERIAL` nodes**: any one connected output is enough to
  PASS. The spec (line 163) says "an OUTPUT_MATERIAL node exists" without
  specifying the active/render-target output; the implementation does not try to
  resolve render-engine-specific output selection (flagged as hard in spec
  Section 9, line 691).

