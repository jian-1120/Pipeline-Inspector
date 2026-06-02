# MVP Reduction

**Author:** Manus AI  
**Role:** Product Research Investigator  
**Principle:** Delete features until only the evidence-supported core remains.

## Reduction Verdict

If 90% of the previously imagined product is removed and only a **READY FOR DELIVERY score** remains, the product can still have value, but only if the score is tied to a short list of checks that directly correlate with real failure evidence. A score by itself is not valuable. A score that explains why a delivery might fail is valuable.

The evidence does not support a broad V1 covering textures, engines, cloud, AI, team collaboration, studio pipeline management, or complex repair. The evidence supports a **small pre-delivery gate** that catches the most common late-stage handoff errors before export, upload, or client submission.

## What Must Be Removed

| Feature Area | Remove from MVP? | Reason |
|---|---|---|
| AI analysis | Yes | No direct evidence that users need AI for the first version; it increases complexity and trust risk. |
| Cloud reports | Yes | No evidence that users need remote storage or SaaS workflows for first validation. |
| Team collaboration | Yes | Studio pain exists conceptually, but current evidence is stronger for solo sellers and game artists. |
| Engine-specific presets | Mostly yes | Unity/Unreal failures are frequent, but engine-specific validation can be postponed until the core score is proven. |
| Texture deep validation | Yes for V1 | Missing textures are important, but user explicitly requested “Do not Texture unless clear evidence supports.” The evidence supports path/packing risk, but a no-texture MVP is still testable. |
| Auto-fix | Yes | Auto-fix increases risk. Evidence supports detection and confidence more than automatic modification. |
| Full geometry validator | Yes | Existing mesh tools already cover broad geometry checking; MVP should only include delivery-blocking geometry signals. |
| Marketplace documentation checks | Yes | Important for sellers, but not Blender-scene-native and can be handled by checklist copy later. |

## Minimal MVP: 10 Checks Maximum

The following MVP intentionally excludes texture, cloud, AI, team features, and engine-specific import simulation. It focuses on scene and object states that repeatedly appear in failure cases and can be explained as delivery readiness checks.

| # | Check | Why It Survives Reduction | Blocking or Warning |
|---:|---|---|---|
| 1 | Object scale is applied or equals expected default | Transform/scale failures appear repeatedly, including CGTrader non-reset-transform rejection and Unity/Unreal scale issues. | Blocking |
| 2 | Object rotation is applied or equals expected default | Rotation/orientation failures cause downstream import surprises. | Warning / Blocking configurable |
| 3 | Object origin/pivot is valid for delivery | Marketplace and asset-quality standards frequently require predictable placement. | Warning |
| 4 | Mesh has no flipped normals | Normals failures are visible after export/import and cause broken shading. | Blocking |
| 5 | Mesh has no obvious loose geometry | Loose/stray geometry appears in quality-failure evidence and is easy to catch. | Warning |
| 6 | Mesh has no zero-area faces or zero-length edges | Degenerate geometry can cause exporter/importer instability. | Blocking |
| 7 | Required UV map exists | Missing UVs appear in failed purchased assets and export/texture cases; this is a minimal non-texture check. | Blocking |
| 8 | Object names are export-safe | Naming/pipeline hygiene has evidence from NoDot Names and asset workflow discussions. | Warning |
| 9 | No empty or hidden delivery objects in selected collection | Prevents accidental inclusion/exclusion and scene-chaos handoff. | Warning |
| 10 | Export selection is explicit and non-empty | Prevents “empty export/import” class of failures. | Blocking |

## MVP Output

The MVP should output only a delivery verdict, score, and a short blocker list. It should not include UI design, repair automation, or platform-specific templates at this stage.

| Output | Example |
|---|---|
| Delivery verdict | READY FOR DELIVERY / NOT READY |
| Score | 82% |
| Blocking issues | 3 |
| Warnings | 5 |
| Top action | “Apply scale on 4 objects before export.” |
| Export confidence note | “This does not guarantee Unity/Unreal acceptance; it checks common pre-export blockers.” |

## Why the Score Alone Can Work

The score has value if it provides a simple psychological and workflow checkpoint immediately before handoff. The evidence database shows repeated cases where users discover failure only after export, import, upload, or review. A pre-delivery score creates a stop-and-check ritual similar to a release gate.

However, the score will fail if it is vague or decorative. It must map directly to detected blockers. Users will only trust the score if they can see the reason behind it and fix the issue manually.

## Non-Goals for MVP

The MVP must not attempt to become a mesh checker, FUM replacement, UV suite, texture packer, cloud QA platform, studio pipeline system, or AI validator. Those ideas may be valid later, but they are not validated strongly enough for V1.

## MVP Success Criteria

| Metric | Minimum Success Threshold |
|---|---|
| Problem catch rate | At least 30% of early users report the tool found an issue before export/upload. |
| Willingness to pay | At least 5–10 users pay or express willingness to pay $5–$9 for the score/checker. |
| False-positive tolerance | Users do not describe warnings as noisy or irrelevant. |
| Repeat usage | Users run the score before multiple exports, not only once. |
| Product focus | Users describe the tool as a delivery confidence gate, not “another mesh checker.” |

## MVP Recommendation

Build only the 10-check **READY FOR DELIVERY** score as the first test. Do not add texture validation beyond “UV map exists” and “export selection exists.” Do not implement auto-fix. Do not build engine presets. The product should be validated by whether users care enough to run the score before delivery and whether they will pay a small price for it.

## References

[1]: real-failure-database.md "Real Failure Database"  
[2]: pain-analysis.md "Pain Severity Analysis"  
[3]: competitor-pricing.md "Competitor Pricing Research"  
[4]: payment-evidence.md "Willingness To Pay Analysis"  
