# MVP Checklist

Purpose: define the first-version delivery checks for Pipeline Inspector.

Scope rule: this checklist only defines what the first version should inspect. It does not define how to build it, how it looks, or how issues should be repaired.

Evidence basis:

- `README.md`
- `research/market-research.md`
- `research/pain-points.md`
- `research/competitor-analysis.md`
- `prd/product-requirements.md`
- `prd/mvp-definition.md`
- `evidence/real-failure-database.md`
- `evidence/pain-analysis.md`
- `evidence/payment-evidence.md`
- `evidence/go-no-go-report.md`
- `evidence/mvp-reduction.md`
- `evidence/competitor-pricing.md`

Evidence summary:

The strongest recurring delivery pain is late-stage handoff failure: assets look acceptable in Blender or the source file, but fail during export, import, upload, review, or client handoff. The 50-case failure database shows the highest-frequency families as FBX/export failure, downstream import failure, missing textures/materials, marketplace rejection, transform/scale/orientation failure, and geometry/normals failure.

The first version should therefore measure whether an asset is ready to leave the creator's file, not whether it satisfies every possible quality guideline.

## Top 10 Delivery Checks

### 1. Texture Files Are Present, Packed, Or Reachable

**Why It Matters**

Missing textures are one of the strongest repeated delivery failures. They create obvious customer-facing damage: gray models, white models, missing appearance, failed imports, marketplace rejection, and manual reassignment.

**Corresponding Failure Cases**

- Cases 1-8: FBX/Unity/Unreal texture loss or failed texture transfer.
- Case 9: product rejected because textures were not packed with the model.
- Case 10: shaders were not linked to packed textures.
- Case 34: exported model retained material slots but appeared gray.
- Cases 44-47: FBX/OBJ exports missing textures or importing untextured.

**Priority**

BLOCKER

### 2. Materials Are Assigned And Export-Relevant

**Why It Matters**

Texture files alone are not enough if materials are missing, empty, disconnected, or not assigned to the delivered mesh. The failure database repeatedly shows assets arriving with missing material appearance even when geometry exists.

**Corresponding Failure Cases**

- Case 4: Unity import required manual material reassignment.
- Case 5: Blender node textures exported to FBX and imported into Unreal without textures.
- Case 10: shaders were not linked to packed textures.
- Case 34: exported model appeared gray despite material slots.
- Case 41: asset conversion described missing materials as part of error-prone handoff.
- Cases 44-47: exported files arrived untextured or without material appearance.

**Priority**

BLOCKER

### 3. Export Selection Contains Visible Deliverable Mesh

**Why It Matters**

An empty, hidden, or incorrect export selection can produce the worst kind of failure: the user technically exports something, but the downstream tool receives nothing useful or misses key pieces.

**Corresponding Failure Cases**

- Case 25: Blender-to-Unity export produced an empty result.
- Case 32: Blender FBX export produced an error.
- Case 43: rigged FBX imported into UE5 with a missing model piece.
- Case 50: downstream validation identified problematic assets and the project crashed on another computer.

**Priority**

BLOCKER

### 4. Object Scale Is Applied Or Reset

**Why It Matters**

Scale errors are small inside Blender but costly after handoff. They cause wrong size, failed upload, inconsistent units, and marketplace rejection. This is a high-value low-complexity readiness check.

**Corresponding Failure Cases**

- Case 18: purchased model had inconsistent scale.
- Case 19: purchased model had wrong scale among other delivery defects.
- Case 33: CGTrader upload failed repeatedly because objects had non-reset transforms; user struggled for days.
- Case 41: conversion problems included inconsistent coordinates.
- Case 49: FBX export to Unity produced incorrect scale unless transform was applied.

**Priority**

BLOCKER

### 5. Object Rotation And Orientation Are Applied Or Reset

**Why It Matters**

Wrong rotation or orientation commonly appears only after export or import. It damages handoff confidence because the model may be technically present but unusable without rework.

**Corresponding Failure Cases**

- Case 35: cross-application compatibility risk forced rework around OBJ/FBX handoff.
- Case 41: conversion was error-prone, with inconsistent coordinates and repeated back-and-forth.
- Case 49: Unity import produced incorrect rotation unless transform was applied.

**Priority**

BLOCKER

### 6. Required UV Map Exists And Is Non-Empty

**Why It Matters**

Missing or invalid UV data contributes to texture failure, export failure, and purchased-asset rework. This is the smallest UV check that directly supports delivery readiness without turning the MVP into a full UV suite.

**Corresponding Failure Cases**

- Case 19: purchased model had missing UVs.
- Case 36: FBX export failed due to a UV map export issue.
- Case 46: exported assets had missing textures/materials across OBJ and FBX.
- Case 48: FBX export failed due to a UV mapping issue.

**Priority**

BLOCKER

### 7. Normals Are Consistent And Not Flipped

**Why It Matters**

Normal issues can make a delivered model look broken even when the mesh exists. They create shading errors, invisible faces, inside-out surfaces, and rework after export.

**Corresponding Failure Cases**

- Case 24: exported FBX broke normals and required rework.
- Case 26: blend shapes corrupted normals in Unity.
- Case 27: normals appeared correct in the source app but reversed after OBJ/FBX export.
- Case 28: Blender FBX imported into Unreal with mesh empty from inside.

**Priority**

BLOCKER

### 8. Mesh Has No Obvious Broken Topology, Holes, Or Non-Manifold Structure

**Why It Matters**

Broken topology is a direct delivery risk when it produces holes, invalid surfaces, or damaged geometry after import. This check should focus on obvious delivery-blocking mesh defects, not exhaustive modeling-quality judgment.

**Corresponding Failure Cases**

- Case 19: purchased model had broken geometry, holes, stray/overlapping points, and missing UVs.
- Case 28: FBX imported into Unreal with inside-empty mesh behavior.
- Case 30: STL exports became messed up every time.
- Case 37: model looked fine in Blender but became heavily deformed after FBX export.

**Priority**

BLOCKER

### 9. Mesh Has No Degenerate Faces Or Zero-Length Edges

**Why It Matters**

Degenerate geometry can destabilize export and import. It is a practical pre-delivery gate because it catches invalid mesh data before the user discovers corruption downstream.

**Corresponding Failure Cases**

- Case 19: broken geometry included stray/overlapping points and holes.
- Case 30: repeated STL export corruption.
- Case 37: model deformation after FBX export.
- Case 48: export failure tied to mesh/UV mapping issues.

**Priority**

BLOCKER

### 10. No Stray, Loose, Hidden, Or Accidental Delivery Objects

**Why It Matters**

Scene chaos causes accidental inclusion, accidental exclusion, missing pieces, and confusing downstream imports. This is a delivery-readiness check because it asks whether the file contains the intended deliverable and not accidental leftovers.

**Corresponding Failure Cases**

- Case 19: purchased model included stray/overlapping points and messy structure.
- Case 25: export produced an empty result.
- Case 41: conversion failures involved broken assets and wasted back-and-forth.
- Case 43: UE5 import missed a model piece.

**Priority**

WARNING

## READY FOR DELIVERY SCORE

Start at 100 points. Subtract points for each failed check.

| # | Check | Priority | Deduction |
|---:|---|---|---:|
| 1 | Texture files are present, packed, or reachable | BLOCKER | -15 |
| 2 | Materials are assigned and export-relevant | BLOCKER | -10 |
| 3 | Export selection contains visible deliverable mesh | BLOCKER | -15 |
| 4 | Object scale is applied or reset | BLOCKER | -12 |
| 5 | Object rotation and orientation are applied or reset | BLOCKER | -8 |
| 6 | Required UV map exists and is non-empty | BLOCKER | -10 |
| 7 | Normals are consistent and not flipped | BLOCKER | -10 |
| 8 | Mesh has no obvious broken topology, holes, or non-manifold structure | BLOCKER | -10 |
| 9 | Mesh has no degenerate faces or zero-length edges | BLOCKER | -5 |
| 10 | No stray, loose, hidden, or accidental delivery objects | WARNING | -5 |

### Verdict Rules

- 90-100 and zero BLOCKER failures: READY FOR DELIVERY.
- 70-89 and zero BLOCKER failures: DELIVERY RISK; review warnings before handoff.
- Any BLOCKER failure: NOT READY FOR DELIVERY, regardless of numeric score.
- Any WARNING failure: reduce the score, but do not block the verdict by itself.
- Three or more BLOCKER failures: cap the score at 49.
- Five or more BLOCKER failures: cap the score at 29.

### BLOCKER Rule

A BLOCKER represents a failure likely to prevent successful export, import, upload, review, or client handoff. It always changes the verdict to NOT READY FOR DELIVERY.

### WARNING Rule

A WARNING represents a file state that can cause rework or confusion, but may not always prevent delivery. It lowers confidence and should be visible in the score.

## Recommended MVP Scope

### Why Keep These 10 Checks

These 10 checks are retained because they best match the evidence weighting requested for the first version:

1. **Frequency**: texture/material failure, export/import failure, transform errors, and geometry/normals problems are the most repeated families in the 50-case database and pain analysis.
2. **User loss**: these failures cause rework, repeated export attempts, marketplace rejection, delayed approval, failed uploads, and client handoff risk.
3. **User value**: the checks answer the core user question: whether the asset is safe enough to send, export, upload, or submit.
4. **Implementation cost**: each check is narrow and based on observable file state. The checklist avoids broad judgment, subjective quality review, or downstream simulation.

The retained checks are not chosen because they are the most complete possible set. They are chosen because they are the smallest credible set that represents READY FOR DELIVERY.

### Why Delete Other Checks From The First Version

The following checks are intentionally not part of the first version:

- **Full UV quality checks** such as overlap, stretch, texel density, or packing quality. Evidence supports UV existence as a blocker, but full UV quality is broader than delivery readiness.
- **Color-space inspection**. It can matter, but the failure database more strongly supports missing or disconnected textures/materials than color-space rules.
- **N-gon-only quality checks**. N-gons may matter, but the strongest delivery evidence is broken topology, holes, normals, deformation, and export/import failure.
- **Origin or pivot quality**. It is useful, but current failure evidence is stronger for scale, rotation, selection, textures, materials, UVs, and broken geometry.
- **Naming convention checks**. Research and competitor evidence support naming hygiene, but the real-failure database shows stronger direct loss from export, material, transform, UV, and geometry failures.
- **Collection organization checks**. Scene organization matters, but the first version should only check accidental delivery objects, hidden objects, and empty/incorrect export content.
- **Marketplace description, images, licensing, or documentation checks**. These are real rejection causes, but they are not Blender-scene technical readiness checks.
- **Rig, animation, and bone validation**. Severe when present, but lower-frequency in the collected evidence and more specialized than the first delivery gate.
- **Large-scene performance checks**. Export crashes are painful, but the database has much lower frequency for this category.
- **Platform-specific import rules**. The first version should measure source-file delivery readiness before handoff, not attempt to guarantee acceptance by every downstream tool.

## Final MVP Definition

The first version of Pipeline Inspector should answer one question:

**Is this asset ready to leave Blender without obvious delivery-blocking failures?**

The MVP is therefore the 10-check READY FOR DELIVERY score above, with a clear split between BLOCKER and WARNING results.
