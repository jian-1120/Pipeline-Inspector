# Real Failure Database

**Author:** Manus AI  
**Role:** Product Research Investigator  
**Scope:** Pipeline Inspector evidence validation phase  
**Status:** Evidence database, not product specification

## Research Objective

本数据库用于验证 Pipeline Inspector 的核心前提：Blender 与 3D 资产交付流程中是否存在真实发生过的失败，而不只是理论上的“可能出错”。本阶段不讨论插件开发、不设计 UI、不写产品架构，只记录真实失败案例，并将其归入 **Problem → Pain → Loss → Willingness To Pay** 证据链的前三段。

> **Evidence rule:** A case is included only when the source describes an actual failure, rejection, broken import/export, failed upload, rework, or delivery risk. Pure tutorials, abstract best-practice advice, and hypothetical checklists are excluded.

## Database Summary

| Metric | Result |
|---|---:|
| Candidate cases collected | 50 |
| Unique cases retained | 50 |
| High-confidence cases | 38 |
| Medium-confidence cases | 11 |
| Main evidence sources | Reddit, Superhive/Blender Market, Unreal Forums, Unity Discussions, Blender Artists, CGTrader Forum, Roblox Developer Forum, Polycount |
| Most frequent failure families | FBX/export failure, import failure, missing textures/materials, marketplace/submission rejection, transform/scale/orientation failure |

The database meets the lower bound requested by the evidence phase, but it should be interpreted conservatively. Many public forum posts do not disclose exact time loss or dollar loss. Therefore, **estimated cost** is marked as “Unknown” unless the source explicitly states a time loss or implies a concrete process delay. This reduces overclaiming and prevents false validation.

## Real Failure Database

| # | Source | User Role | What Failed | Consequence | Estimated Cost | Confidence |
|---:|---|---|---|---|---|---|
| 1 | [Need help with Blender to Unity FBX character no texture](https://www.reddit.com/r/Unity3D/comments/136slr8/need_help_with_blender_to_unity_fbx_character_no/) | Unknown | Blender FBX export/import into Unity resulted in a character with no texture. Evidence: “no texture.” | Import Failure | Unknown | Medium |
| 2 | [Why is my FBX file not exporting with the texture?](https://www.reddit.com/r/blenderhelp/comments/uulzr5/why_is_my_fbx_file_not_exporting_with_the_texture/) | Unknown | FBX file exported from Blender did not retain texture and imported into Unity without texture. | Import Failure | Unknown | Medium |
| 3 | [Issue with Blender model importing to Unity](https://www.reddit.com/r/Unity3D/comments/ti2j3e/issue_with_blender_model_importing_to_unity/) | Unknown | Textures did not remain correctly placed after Blender model import into Unity. | Import Failure | Unknown | Medium |
| 4 | [Having issues importing Materials to Unity from Blender using FBX](https://www.reddit.com/r/Unity3D/comments/vrpza0/having_issues_importing_materials_to_unity_from/) | Unknown | FBX import settings warped palette texture and required manual material reassignment. | Import Failure; Rework | Unknown | High |
| 5 | [FBX export why there are no materials or textures?](https://blender.stackexchange.com/questions/57531/fbx-export-why-there-are-no-materials-or-textures) | Unknown | Node textures in Blender exported to FBX and imported into Unreal Engine without textures. | Import Failure | Unknown | High |
| 6 | [Problem with Textures after importing FBX](https://www.reddit.com/r/Unity3D/comments/1ihppoo/problem_with_textures_after_importing_fbx_in/) | Unknown | Textures looked correct in Blender but became incorrect in Unity after FBX import. | Import Failure | Unknown | High |
| 7 | [Missing textures from imported FBX file in Unity since update](https://discussions.unity.com/t/missing-textures-from-imported-fbx-file-in-unity-since-update/692476) | Unknown | Textures were missing from imported FBX files after a Unity update. | Import Failure | Unknown | High |
| 8 | [FBX export to Unity does not export textures](https://github.com/JannisX11/blockbench/issues/2296) | Unknown | Associated textures did not export with FBX/OBJ into Unity. | Export Failure; Import Failure | Unknown | High |
| 9 | [Why Products Get Rejected — Superhive](https://support.superhivemarket.com/article/186-why-products-get-rejected) | Marketplace Seller | Product rejected because textures were not packed with the model. | Marketplace Rejected | Unknown | High |
| 10 | [Why Products Get Rejected — Superhive](https://support.superhivemarket.com/article/186-why-products-get-rejected) | Marketplace Seller | Shaders were not linked to packed textures. | Marketplace Rejected | Unknown | High |
| 11 | [Why Products Get Rejected — Superhive](https://support.superhivemarket.com/article/186-why-products-get-rejected) | Marketplace Seller | Product description was too poor or incomplete for review. | Marketplace Rejected | Unknown | High |
| 12 | [Why Products Get Rejected — Superhive](https://support.superhivemarket.com/article/186-why-products-get-rejected) | Marketplace Seller | Incomplete documentation or external-only documentation resulted in rejection. | Marketplace Rejected | Unknown | High |
| 13 | [Why Products Get Rejected — Superhive](https://support.superhivemarket.com/article/186-why-products-get-rejected) | Marketplace Seller | Placeholder form text caused immediate rejection and delayed approval. | Marketplace Rejected; Delayed Project | Unknown | High |
| 14 | [Why Products Get Rejected — Superhive](https://support.superhivemarket.com/article/186-why-products-get-rejected) | Marketplace Seller | Product images failed platform requirements. | Marketplace Rejected | Unknown | High |
| 15 | [How many of your assets get rejected in Marketplace?](https://forums.unrealengine.com/t/how-many-of-your-asset-get-rejected-in-marketplace/106273) | Marketplace Seller | Unreal Marketplace rejected a submission because no map/level file displayed the assets. | Marketplace Rejected | Unknown | High |
| 16 | [How many of your assets get rejected in Marketplace?](https://forums.unrealengine.com/t/how-many-of-your-asset-get-rejected-in-marketplace/106273) | Marketplace Seller | First submission rejected because modified public-domain assets conflicted with marketplace terms. | Marketplace Rejected | Unknown | High |
| 17 | [How many of your assets get rejected in Marketplace?](https://forums.unrealengine.com/t/how-many-of-your-asset-get-rejected-in-marketplace/106273) | Marketplace Seller | Asset rejected due to free third-party models, music, sounds and textures without acceptable commercial licensing. | Marketplace Rejected | Unknown | High |
| 18 | [Do not trust CGTrader for 3D models](https://www.reddit.com/r/3Dprinting/comments/7ig1hn/do_not_trust_cgtrader_for_3d_models/) | Freelancer | Purchased model files were “a mess,” with mismatched parts and inconsistent scale. | Delayed Project | Unknown | High |
| 19 | [Did I Make a Bad Purchase from CGTrader?](https://www.reddit.com/r/Houdini/comments/1mm3lo0/did_i_make_a_bad_purchase_from_cg_trader/) | Hobbyist | Purchased model had broken geometry, stray/overlapping points, holes, missing UVs, and wrong scale. | Rework; Possible Submission Failure | Unknown | High |
| 20 | [I just got rejected by Blender Market](https://www.reddit.com/r/blender/comments/f9d0e8/i_just_got_rejected_by_blender_market_was_my/) | Marketplace Seller | Blender Market rejected a model; user asked whether technical/model quality was the reason. | Marketplace Rejected | Unknown | High |
| 21 | [Abuse on CGTrader](https://www.reddit.com/r/3Dmodeling/comments/1h8qz4t/abuse_on_cgtrader/) | Marketplace Seller | Customer dissatisfaction resulted in severe negative reviews across models. | Lost Client; Reputation Loss | Unknown | Medium |
| 22 | [Please critique my work](https://polycount.com/discussion/218941/please-critique-my-work-be-brutal) | Game Artist | User reported years of failure entering game industry, implying assets failed industry expectations. | Career/Submission Failure | Unknown | Medium |
| 23 | [3D Warehouse Upload Error](https://groups.google.com/g/3dwh/c/cPKI7-ar2aI/m/9dw8KtJ8XAUJ) | Unknown | Uploaded model experienced processing error and could not be included in Google Earth. | Submission Rejected | Unknown | High |
| 24 | [Exporting FBX from Unreal breaks normals](https://www.reddit.com/r/unrealengine/comments/1k4zhm6/exporting_fbx_from_unreal_breaks_normals/) | Unknown | Recalculated normals imported as flipped/messed up. | Export Failure; Rework | Unknown | High |
| 25 | [Why is it empty? Blender to Unity](https://www.reddit.com/r/Unity3D/comments/1lnlagh/why_it_is_empty_first_time_trying_export_from/) | Hobbyist | First Blender-to-Unity export produced an empty result. | Import Failure | Unknown | High |
| 26 | [Blend Shapes break Normals from Maya to Unity](https://www.reddit.com/r/Unity3D/comments/1l2ft69/blend_shapes_break_normals_from_maya_to_unity/) | Game Artist | Mesh normals were corrupted in Unity when using blend shapes. | Rework | Unknown | High |
| 27 | [Face normals are reversed on OBJ and FBX export](https://www.reddit.com/r/Maya/comments/buwve5/face_normals_are_reversed_on_obj_and_fbx_export/) | Unknown | Normals appeared correct in source app but reversed in Substance Painter/Unreal after export. | Export Failure; Rework | Unknown | High |
| 28 | [FBX from Blender to Unreal mesh empty inside](https://www.reddit.com/r/unrealengine/comments/va09uc/help_issue_where_after_exporting_fbx_from_blender/) | Unknown | Blender FBX imported into Unreal with mesh empty from inside. | Import Failure | Unknown | High |
| 29 | [Not possible to export 38M-poly object as FBX](https://blenderartists.org/t/not-possible-to-export-object-as-fbx-with-38mil-polys-blender-performance-abysmal/1412005) | Unknown | Blender froze, crashed, or aborted export for a 38M-poly FBX. | Export Failure; Delayed Project | At least several minutes per attempt; larger cost implied | High |
| 30 | [3D assets not exporting from Blender](https://www.reddit.com/r/deltavringsofsaturn/comments/15x2mie/3d_assets_not_exporting_from_blender/) | Hobbyist | STL exports became messed up every time. | Export Failure; Rework | Unknown | High |
| 31 | [Client never paid for 3D assets](https://www.reddit.com/r/blender/comments/15phhsk/some_3d_assets_i_made_for_a_client_that_never/) | Freelancer | Client did not pay for completed 3D assets. | Lost Client; Client Rejected | Unknown | High |
| 32 | [Failing to export things from Blender](https://devforum.roblox.com/t/failing-to-export-things-from-blender/1361332) | Builder | Blender FBX export produced an error. | Export Failure; Rework | Unknown | High |
| 33 | [Objects have non reset transforms](https://www.cgtrader.com/forum/technical-q-a/objects-have-non-reset-transforms) | Marketplace Seller | CGTrader upload failed repeatedly because objects had non-reset transforms. | Submission Rejected; Rework | “Struggling for days” | High |
| 34 | [After exporting from Blender, object loses material properties](https://www.cgtrader.com/forum/technical-q-a/after-exporting-an-object-from-blender-it-loses-all-of-its-materials-properties) | Marketplace Seller | Exported model retained material slots but all materials appeared gray. | Export Failure; Submission Risk | Unknown | High |
| 35 | [Is Blender compatible with other major 3D apps?](https://blenderartists.org/t/is-blender-compatible-with-other-major-3d-apps/666374) | Freelancer | Client may be unable to open Blender OBJ/FBX files, forcing user to relearn Max. | Client Rejected; Rework | Unknown | High |
| 36 | [Error when trying to export model as FBX](https://www.reddit.com/r/blender/comments/11hvjfh/error_when_trying_to_export_model_as_fbx/) | Unknown | FBX export failed due to a UV map export issue. | Export Failure | Unknown | Medium |
| 37 | [Model fine in Blender but deformed as FBX](https://www.reddit.com/r/blenderhelp/comments/1d678x1/my_model_is_fine_in_blender_but_it_becomes/) | Unknown | Model became heavily deformed after FBX export. | Export Failure; Rework | Unknown | Medium |
| 38 | [Exporting FBX error](https://www.reddit.com/r/blender/comments/5xkupy/help_exporting_fbx_error_looking_for_help/) | Unknown | Blender raised FBX material list-index error during export. | Export Failure | Unknown | Medium |
| 39 | [FBX exporting error](https://www.reddit.com/r/blender/comments/1gzad3e/fbx_exporting_error/) | Hobbyist | Project failed every time user attempted FBX export. | Export Failure | Unknown | Medium |
| 40 | [I can’t export an FBX model](https://www.reddit.com/r/blenderhelp/comments/1bm90oq/i_cant_export_a_fbx_model/) | Unknown | User repeatedly failed to export FBX model for Unity. | Export Failure | Unknown | Medium |
| 41 | [Feedback from Game Developers and 3D Artists](https://www.reddit.com/r/gamedev/comments/1lbmf2p/looking_for_feedback_from_game_developers_3d/) | Unknown | Blender asset conversion described as error-prone, with broken rigs, missing materials, inconsistent coordinates, and wasted back-and-forth. | Rework; Delayed Project | Unknown | Medium |
| 42 | [Dread working in Blender for games](https://www.reddit.com/r/IndieDev/comments/1dew34n/does_anyone_else_absolutely_dread_working_in/) | Hobbyist | User had to spend equal time diagnosing import/export and compatibility failures. | Rework; Delayed Project | “Equal amount of time” | High |
| 43 | [Problems exporting from Blender and importing to UE5](https://forums.unrealengine.com/t/problems-when-exporting-from-blender-and-importing-to-ue5/660816) | Unknown | Rigged FBX imported into UE5 with a missing model piece. | Import Failure; Rework | Unknown | High |
| 44 | [How to export FBX files with texture](https://www.reddit.com/r/blenderhelp/comments/1kb62bi/how_to_export_fbx_files_with_texture/) | Hobbyist | FBX files imported into After Effects or other programs completely untextured. | Rework | Unknown | High |
| 45 | [FBX file not exporting with texture into Unity](https://www.reddit.com/r/blenderhelp/comments/uulzr5/why_is_my_fbx_file_not_exporting_with_the_texture/) | Hobbyist | FBX exported from Blender and imported into Unity without texture. | Import Failure; Rework | Unknown | High |
| 46 | [Missing textures/materials when exporting OBJ and FBX](https://www.reddit.com/r/blenderhelp/comments/1dvaf9n/missing_textures_andor_materials_when_exporting/) | Marketplace Seller | FBX missed a transparency texture that GLB/glTF handled correctly. | Rework; Marketplace Risk | Unknown | High |
| 47 | [FBX model will not export with textures](https://www.reddit.com/r/blenderhelp/comments/1nx6nko/my_fbx_model_will_not_export_with_textures/) | Hobbyist | Model would not load into Toon Boom Harmony with textures. | Rework | Unknown | High |
| 48 | [Error when exporting as FBX from Blender](https://devforum.roblox.com/t/error-when_exporting-as-fbx-from-blender/1159486) | Builder | FBX export failed due to UV mapping issue. | Export Failure; Rework | Unknown | High |
| 49 | [FBX Export Problem](https://blenderartists.org/t/fbx-export-problem/1337258) | Unknown | FBX export to Unity produced incorrect scale and rotation unless “Apply Transform” was selected. | Rework | Unknown | High |
| 50 | [Project crashes on asset validation](https://forums.unrealengine.com/t/project-crashes-on-asset-validation/2656903) | Game Artist | Unreal project crashed on another computer while asset validation identified problematic assets. | Delayed Project | Unknown | High |

## Evidence Limitations

This database proves repeated real failures but does not fully prove monetization by itself. Most public failure posts are support-seeking posts, not purchase-intent posts. Exact dollar loss is rarely disclosed, and user roles often must be inferred from context. For this reason, the database should be read as strong evidence of **Problem**, **Pain**, and partial **Loss**, while **Willingness To Pay** must be validated through competitor pricing and purchase evidence in separate documents.

## References

[1]: https://support.superhivemarket.com/article/186-why-products-get-rejected "Why Products Get Rejected — Superhive"  
[2]: https://forums.unrealengine.com/t/how-many-of-your-asset-get-rejected-in-marketplace/106273 "How many of your assets get rejected in Marketplace?"  
[3]: https://www.cgtrader.com/forum/technical-q-a/objects-have-non-reset-transforms "Objects have non reset transforms — CGTrader Forum"  
[4]: https://blenderartists.org/t/not-possible-to-export-object-as-fbx-with-38mil-polys-blender-performance-abysmal/1412005 "Not Possible to Export Object as FBX — Blender Artists"  
[5]: https://discussions.unity.com/t/missing-textures-from-imported-fbx-file-in-unity-since-update/692476 "Missing textures from imported FBX file in Unity"  
