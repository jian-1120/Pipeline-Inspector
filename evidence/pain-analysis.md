# Pain Severity Analysis

**Author:** Manus AI  
**Role:** Product Research Investigator  
**Purpose:** Determine which failures most often create rework, rejection, re-export, or delivery risk.

## Executive Finding

The strongest pattern in the evidence database is not “artists need another mesh checker.” The stronger pattern is that **delivery failures are multi-factor workflow failures**: FBX/export problems, engine import failures, missing textures/materials, marketplace submission rejection, and transform/scale/orientation mistakes repeatedly appear together. This supports the hypothesis that the pain is not simply geometry validation; the pain is **uncertainty before delivery**.

> **Key interpretation:** Users are not primarily complaining that they lack technical theory. They are complaining that assets look fine in the source tool but fail at the point of handoff, upload, import, or review.

## Top Failure Families

The following table aggregates the 50-case Real Failure Database. Cases may be assigned to more than one category because many delivery failures combine export, import, material, transform, and marketplace consequences.

| Rank | Failure Cause | Observed Count | Typical Consequence | Severity Interpretation |
|---:|---|---:|---|---|
| 1 | FBX/export failure | 31 | Export failure, repeated attempts, blocked delivery | Very high. FBX is the dominant handoff format in many Blender-to-engine workflows, and failures often happen late in the pipeline. |
| 2 | Import failure into engine/software | 22 | Unreal/Unity import failure, missing pieces, broken animation | Very high. The failure is discovered after handoff, making it costly and confidence-damaging. |
| 3 | Missing textures/materials | 19 | White/gray models, marketplace rejection, manual material reassignment | Very high. It is visible to customers/reviewers and repeatedly appears in marketplace rejection guidance. |
| 4 | Marketplace/submission rejection | 19 | Product rejected, approval delayed, resubmission required | High. This creates direct business loss for sellers because publication and revenue are delayed. |
| 5 | Transform/scale/orientation failure | 15 | Wrong size, wrong rotation, non-reset transforms, upload failure | High. These mistakes are small but highly consequential and often difficult for users to diagnose. |
| 6 | Topology/geometry/normals failure | 10 | Flipped normals, broken mesh, deformed model, holes | Medium-high. The issue is common and visible, but many tools already partially address it. |
| 7 | Licensing/documentation/presentation rejection | 10 | Marketplace rejection, delayed approval | Medium-high. Important for marketplaces but less central to a Blender-only technical preflight MVP. |
| 8 | Rig/animation/bone failure | 4 | Broken animations, bones too small, missing physics asset | Medium. Severe when present, but lower frequency in the collected database. |
| 9 | Asset linking/dependency failure | 2 | Missing files, plugin dependency, broken linked assets | Medium. Strong pain, but currently insufficient frequency for MVP inclusion. |
| 10 | Performance/large scene/export crash | 1 | Export crash/freeze | Medium. Painful but too niche for the first MVP. |

## Consequence Ranking

| Rank | Consequence | Observed Count | What It Means for Product Risk |
|---:|---|---:|---|
| 1 | Rework | 16 | Users lose time diagnosing and re-exporting assets after discovering failure. |
| 2 | Export Failure | 13 | The delivery process is blocked before the asset can leave Blender/source tool. |
| 3 | Import Failure | 12 | Failure is discovered in Unity, Unreal, or another downstream tool. |
| 4 | Marketplace Rejected | 11 | Seller cannot publish and may need resubmission. |
| 5 | Delayed Project | 5 | Failure consumes time across multiple attempts or support interactions. |
| 6 | Submission Rejected | 4 | Platform or processing gate blocks acceptance. |
| 7 | Client Rejected / Lost Client | 2–4 | Lower frequency in public evidence, but highest business severity. |

## Pain Severity by User Segment

| Segment | Evidence Strength | Dominant Failures | Interpretation |
|---|---|---|---|
| Marketplace Seller | High | Missing textures, submission rejection, non-reset transforms, documentation/package requirements | This is the strongest business segment because rejection has direct publication and revenue impact. |
| Game Artist / Indie Developer | High | Blender-to-Unity/Unreal import failures, broken scale, missing textures, broken rigs | Strong workflow pain, but willingness to pay depends on whether the tool is cheaper than repeated manual diagnosis. |
| Freelancer | Medium | Client file compatibility, unpaid/rejected work, cross-app FBX/OBJ reliability | Severe when it occurs, but fewer public cases explicitly state client rejection. |
| Studio Artist | Medium-low | QA, naming, validation, pipeline consistency | Strong conceptual fit, but current public evidence is less direct than marketplace/game-artist evidence. |
| Hobbyist | Medium | Export/import confusion, texture loss, scale issues | High volume of pain, but weaker monetization unless priced very low. |

## What Most Often Causes Rework, Rejection, or Re-export?

The evidence suggests that rework and re-export are most often triggered by **FBX/export failure**, **missing textures/materials**, **transform/scale/orientation errors**, and **engine import failure**. Marketplace rejection is often triggered by missing textures, incomplete documentation, bad package presentation, missing maps/levels, licensing problems, and non-reset transforms.

For Pipeline Inspector, this means the highest-value MVP should not begin with a broad “everything checker.” It should begin with the smallest set of checks that prevents the most common late-stage handoff failures. Based on current evidence, the most defensible MVP checks are export-readiness checks, not broad geometry QA.

## Evidence-Based Product Implication

A large product scope is not justified. The data supports a **narrow pre-delivery score** that warns users before export or upload. The initial value proposition should be:

> “Before you send, export, upload, or submit, know whether the asset is likely to fail a basic delivery gate.”

This framing is more evidence-supported than “professional Blender QA suite,” “pipeline automation,” or “AI validation.”

## References

[1]: real-failure-database.md "Real Failure Database"  
[2]: https://support.superhivemarket.com/article/186-why-products-get-rejected "Why Products Get Rejected — Superhive"  
[3]: https://www.cgtrader.com/forum/technical-q-a/objects-have-non-reset-transforms "Objects have non reset transforms — CGTrader Forum"  
[4]: https://forums.unrealengine.com/t/how-many-of-your-asset-get-rejected-in-marketplace/106273 "Unreal Marketplace rejection discussion"  
