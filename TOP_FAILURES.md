# Top Failures

Purpose: summarize the highest-frequency failure types in current Pipeline Inspector evidence.

Primary statistical source: `evidence/pain-analysis.md`, which aggregates the 50-case `real-failure-database.md` and `real-failure-database.csv`.

## Top 10 Failure Types

| Rank | Failure Type | Frequency | Typical Consequence | User Role | Avoidable By Pre-Delivery Check | MVP Priority |
|---:|---|---:|---|---|---|---|
| 1 | FBX/export failure | 31 | Export failure, repeated attempts, blocked delivery | Blender-to-engine users, hobbyists, builders, marketplace sellers | Partially. Pre-delivery checks can catch common causes, but not every exporter defect. | P0 |
| 2 | Import failure into engine/software | 22 | Unity/Unreal import failure, empty import, missing pieces, broken visual result | Game artists, indie developers, hobbyists, unknown users | Partially. Source-file readiness can reduce risk but cannot guarantee downstream acceptance. | P0 |
| 3 | Missing textures/materials | 19 | White/gray models, missing appearance, manual reassignment, marketplace rejection | Marketplace sellers, Blender-to-engine users, hobbyists | Yes for missing files, disconnected materials, or unreachable texture references. | P0 |
| 4 | Marketplace/submission rejection | 19 | Product rejected, approval delayed, resubmission required | Marketplace sellers | Partially. Technical scene issues are avoidable; documentation, licensing, and presentation failures are outside scene checks. | P1 |
| 5 | Transform/scale/orientation failure | 15 | Wrong size, wrong rotation, non-reset transforms, upload failure | Marketplace sellers, freelancers, game/engine users | Yes. Applied scale and rotation checks directly reduce this risk. | P0 |
| 6 | Topology/geometry/normals failure | 10 | Flipped normals, broken mesh, deformed model, holes, rework | Game artists, marketplace sellers, hobbyists | Yes for obvious normals and geometry defects. | P1 |
| 7 | Licensing/documentation/presentation rejection | 10 | Marketplace rejection, delayed approval, resubmission | Marketplace sellers | No for Blender scene inspection. This is real evidence but not a scene-native MVP check. | Cut From MVP |
| 8 | Rig/animation/bone failure | 4 | Broken animations, deformed rigs, missing pieces | Game artists, Blender-to-engine users | Partially, but it requires specialized validation. | Reconsider Later |
| 9 | Asset linking/dependency failure | 2 | Missing files, broken linked assets, dependency issues | Marketplace sellers, asset creators | Partially. Basic missing-file detection may help; dependency validation is broader. | Reconsider Later |
| 10 | Performance/large scene/export crash | 1 | Export freeze/crash, delayed project | High-poly scene users | Partially, but evidence frequency is too low for first MVP priority. | Cut From MVP |

## Consequence Ranking

| Rank | Consequence | Observed Count | Product Meaning |
|---:|---|---:|---|
| 1 | Rework | 16 | Users lose time diagnosing and re-exporting assets. |
| 2 | Export Failure | 13 | Delivery is blocked before the file leaves the source workflow. |
| 3 | Import Failure | 12 | Failure is discovered downstream, usually after handoff. |
| 4 | Marketplace Rejected | 11 | Sellers cannot publish and must resubmit. |
| 5 | Delayed Project | 5 | The failure consumes time across repeated attempts or support loops. |
| 6 | Submission Rejected | 4 | Platform gate blocks acceptance. |
| 7 | Client Rejected / Lost Client | 2-4 | Lower public frequency, but highest business severity. |

## MVP Implication

The highest-value MVP checks should focus on late-stage handoff failures that can be detected before export, upload, or client submission:

- missing texture/material readiness
- explicit non-empty export contents
- applied scale and rotation
- required UV existence
- normals and obvious geometry defects

Evidence does not support adding marketplace documentation, licensing, rig validation, large-scene performance checks, or broad project organization to the first MVP.
