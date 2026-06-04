# MVP Evidence Mapping

Purpose: validate whether each check in `MVP_CHECKLIST.md` is supported by current repository evidence.

Evidence sources reviewed:

- `README.md`
- `MVP_CHECKLIST.md`
- `research/pain-points.md`
- `prd/mvp-definition.md`
- `evidence/real-failure-database.md`
- `evidence/real-failure-database.csv`
- `evidence/pain-analysis.md`
- `evidence/payment-evidence.md`
- `evidence/go-no-go-report.md`
- `evidence/mvp-reduction.md`

Evidence rule: a check is strongest when it maps to repeated real failure cases and to delivery consequences such as export failure, import failure, marketplace rejection, client rejection, rework, or delayed project.

## Summary

| # | Check Name | Frequency Signal | Evidence Strength | Recommendation |
|---:|---|---:|---|---|
| 1 | Texture Files Are Present, Packed, Or Reachable | 19 missing texture/material family cases | Strong | Keep |
| 2 | Materials Are Assigned And Export-Relevant | 19 missing texture/material family cases | Strong | Keep |
| 3 | Export Selection Contains Visible Deliverable Mesh | 3-4 direct cases | Medium | Keep |
| 4 | Object Scale Is Applied Or Reset | 15 transform family cases | Strong | Keep |
| 5 | Object Rotation And Orientation Are Applied Or Reset | 15 transform family cases, fewer direct rotation cases | Medium | Keep |
| 6 | Required UV Map Exists And Is Non-Empty | 3-4 direct cases, supported by PRD | Medium | Keep |
| 7 | Normals Are Consistent And Not Flipped | 4 direct cases, 10 geometry/normals family cases | Strong | Keep |
| 8 | Mesh Has No Obvious Broken Topology, Holes, Or Non-Manifold Structure | 4 direct cases, 10 geometry/normals family cases | Medium | Keep |
| 9 | Mesh Has No Degenerate Faces Or Zero-Length Edges | Mostly indirect cases | Weak | Reconsider |
| 10 | No Stray, Loose, Hidden, Or Accidental Delivery Objects | 3-4 related cases | Medium | Reconsider |

## 1. Texture Files Are Present, Packed, Or Reachable

**Corresponding Failure Cases**

- Cases 1-8: repeated Blender/FBX/Unity/Unreal texture loss or failed texture transfer.
- Case 9: product rejected because textures were not packed with the model.
- Case 10: shaders were not linked to packed textures.
- Case 34: exported model retained material slots but appeared gray.
- Cases 44-47: exported FBX/OBJ files arrived untextured or with missing textures/materials.

**Frequency**

Strong. `pain-analysis.md` records 19 observed missing texture/material cases, tied for the third-highest failure family.

**User Loss**

Import failure, marketplace rejection, manual material reassignment, rework, marketplace risk, and visible customer-facing quality failure.

**Delivery Failure**

Yes. The failure appears at export, import, upload, review, or customer handoff.

**MVP Fit**

Evidence fit is strong. However, `mvp-reduction.md` warns against broad texture validation in the first version. This check should remain only if it is limited to file presence, packing, and reachability rather than deep texture quality.

**Evidence Strength**

Strong

**Recommendation**

Keep

## 2. Materials Are Assigned And Export-Relevant

**Corresponding Failure Cases**

- Case 4: Unity import required manual material reassignment.
- Case 5: Blender node textures exported to FBX and imported into Unreal without textures.
- Case 10: shaders were not linked to packed textures.
- Case 34: exported model appeared gray despite material slots.
- Case 41: asset conversion failures included missing materials.
- Cases 44-47: exports arrived untextured or without expected material appearance.

**Frequency**

Strong at the family level. It belongs to the 19-case missing textures/materials family.

**User Loss**

Rework, failed visual delivery, manual reassignment, marketplace rejection risk, and downstream import failure.

**Delivery Failure**

Yes. Material failures repeatedly appear after export/import and during marketplace review.

**MVP Fit**

Strong if defined narrowly as material assignment and export relevance. It should not become a broad material-quality or shader-quality review.

**Evidence Strength**

Strong

**Recommendation**

Keep

## 3. Export Selection Contains Visible Deliverable Mesh

**Corresponding Failure Cases**

- Case 25: Blender-to-Unity export produced an empty result.
- Case 32: Blender FBX export produced an error.
- Case 43: rigged FBX imported into UE5 with a missing model piece.
- Case 50: downstream asset validation identified problematic assets and the project crashed on another computer.

**Frequency**

Medium. The direct case count is lower than texture, transform, or import/export family failures, but the consequence is severe and `mvp-reduction.md` explicitly includes non-empty export selection.

**User Loss**

Blocked export, empty import, missing pieces, rework, and delayed project.

**Delivery Failure**

Yes. This is a direct handoff failure.

**MVP Fit**

Strong. This is one of the clearest pre-delivery gate checks because it prevents sending nothing or the wrong thing.

**Evidence Strength**

Medium

**Recommendation**

Keep

## 4. Object Scale Is Applied Or Reset

**Corresponding Failure Cases**

- Case 18: purchased model files had inconsistent scale.
- Case 19: purchased model had wrong scale among other delivery defects.
- Case 33: CGTrader upload failed repeatedly because objects had non-reset transforms; user struggled for days.
- Case 41: asset conversion failures included inconsistent coordinates.
- Case 49: Unity import produced incorrect scale unless transform was applied.

**Frequency**

Strong. `pain-analysis.md` records 15 transform/scale/orientation cases.

**User Loss**

Submission rejection, repeated upload attempts, rework, delayed project, and downstream size mismatch.

**Delivery Failure**

Yes. Scale errors repeatedly become visible after upload, import, or marketplace validation.

**MVP Fit**

Strong. This is one of the best-supported first-version checks.

**Evidence Strength**

Strong

**Recommendation**

Keep

## 5. Object Rotation And Orientation Are Applied Or Reset

**Corresponding Failure Cases**

- Case 35: cross-application compatibility risk forced rework around OBJ/FBX handoff.
- Case 41: asset conversion was error-prone, including inconsistent coordinates and repeated back-and-forth.
- Case 49: Unity import produced incorrect rotation unless transform was applied.

**Frequency**

Medium. It is part of the 15-case transform/scale/orientation family, but fewer cases isolate rotation specifically.

**User Loss**

Wrong orientation after import, rework, compatibility uncertainty, and repeated export attempts.

**Delivery Failure**

Yes. The problem appears after handoff into another tool.

**MVP Fit**

Good. It is less independently evidenced than scale, but it belongs to the same high-value transform gate.

**Evidence Strength**

Medium

**Recommendation**

Keep

## 6. Required UV Map Exists And Is Non-Empty

**Corresponding Failure Cases**

- Case 19: purchased model had missing UVs.
- Case 36: FBX export failed due to a UV map export issue.
- Case 46: exported OBJ/FBX assets had missing textures/materials.
- Case 48: FBX export failed due to a UV mapping issue.

**Frequency**

Medium. The direct count is lower than texture/material or transform failures, but UV absence is repeatedly tied to texture/export failure and appears in `prd/mvp-definition.md` and `mvp-reduction.md`.

**User Loss**

Export failure, rework, missing texture behavior, and possible submission failure.

**Delivery Failure**

Yes. Missing or invalid UVs can block export or cause broken visual delivery.

**MVP Fit**

Strong as a minimal UV check. It should remain limited to existence and non-empty state, not full UV quality.

**Evidence Strength**

Medium

**Recommendation**

Keep

## 7. Normals Are Consistent And Not Flipped

**Corresponding Failure Cases**

- Case 24: exported FBX broke normals and required rework.
- Case 26: blend shapes corrupted normals in Unity.
- Case 27: normals appeared correct in the source app but reversed after OBJ/FBX export.
- Case 28: Blender FBX imported into Unreal with the mesh empty from inside.

**Frequency**

Strong within geometry. `pain-analysis.md` records 10 topology/geometry/normals cases, and normals are the clearest repeated subcategory.

**User Loss**

Broken shading, invisible surfaces, export/import failure, and rework.

**Delivery Failure**

Yes. Normal problems repeatedly appear after export or downstream import.

**MVP Fit**

Strong. This is a delivery-blocking geometry signal, not a broad mesh-quality wish list.

**Evidence Strength**

Strong

**Recommendation**

Keep

## 8. Mesh Has No Obvious Broken Topology, Holes, Or Non-Manifold Structure

**Corresponding Failure Cases**

- Case 19: purchased model had broken geometry, holes, stray/overlapping points, missing UVs, and wrong scale.
- Case 28: Blender FBX imported into Unreal with inside-empty mesh behavior.
- Case 30: STL exports became messed up every time.
- Case 37: model looked fine in Blender but became heavily deformed after FBX export.

**Frequency**

Medium. It maps to the 10-case topology/geometry/normals family, but the current evidence is stronger for visible broken topology than for every possible non-manifold condition.

**User Loss**

Rework, export failure, deformed model, possible submission failure, and downstream import failure.

**Delivery Failure**

Yes. These defects affect export/import and customer-visible geometry.

**MVP Fit**

Good if kept as obvious delivery-blocking topology only. It should not become a full geometry validator.

**Evidence Strength**

Medium

**Recommendation**

Keep

## 9. Mesh Has No Degenerate Faces Or Zero-Length Edges

**Corresponding Failure Cases**

- Case 19: broken geometry included stray/overlapping points and holes.
- Case 30: repeated STL export corruption.
- Case 37: model deformation after FBX export.
- Case 48: export failure tied to mesh/UV mapping issues.

**Frequency**

Weak as a standalone item. `mvp-reduction.md` includes degenerate geometry, but the real-failure database does not repeatedly name zero-area faces or zero-length edges directly.

**User Loss**

Potential export/import instability and rework, but direct user loss is inferred rather than repeatedly stated.

**Delivery Failure**

Possibly. It can contribute to delivery failure, but current evidence mostly supports the broader broken-geometry family.

**MVP Fit**

Questionable as a standalone top-10 item. It may be better merged into the broader broken topology check.

**Evidence Strength**

Weak

**Recommendation**

Reconsider

## 10. No Stray, Loose, Hidden, Or Accidental Delivery Objects

**Corresponding Failure Cases**

- Case 19: purchased model included stray/overlapping points and messy structure.
- Case 25: export produced an empty result.
- Case 41: conversion failures involved broken assets and wasted back-and-forth.
- Case 43: UE5 import missed a model piece.

**Frequency**

Medium. Loose or accidental objects are not one of the highest-frequency named families, but scene chaos appears in research and accidental inclusion/exclusion is directly relevant to delivery.

**User Loss**

Wrong export contents, missing pieces, rework, and delayed handoff.

**Delivery Failure**

Yes, when the wrong objects are delivered or required objects are hidden/excluded.

**MVP Fit**

Moderate. Keep only as a warning-level delivery sanity check. Do not expand it into broad collection or project organization rules.

**Evidence Strength**

Medium

**Recommendation**

Reconsider

## Evidence Review Conclusion

The current MVP checklist is mostly evidence-supported, but not all 10 checks are equally strong. The strongest checks are texture/material presence, export selection, scale, UV existence, and normals. The weakest standalone check is degenerate faces/zero-length edges because the evidence supports broken geometry broadly more than that exact failure mode. The accidental/hidden/loose object check is useful but should remain warning-level or be merged with export selection.
