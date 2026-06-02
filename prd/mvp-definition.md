# MVP 定义

**最小可行产品 (MVP) 范围**将专注于核心的交付前检查功能，避免引入 AI、Cloud、Team Collaboration、SaaS 等复杂功能，以快速验证核心价值。

## MVP Check List

MVP 将涵盖以下关键检查项：

*   **Geometry (几何体)**
    *   **Non-Manifold (非流形几何体)**：检测模型中存在的非流形边或顶点，这些可能导致渲染或导出问题。
    *   **Ngon (N-边面)**：检测模型中存在的 N-gon 面，这些可能在游戏引擎或特定渲染器中引起问题。
    *   **Flipped Normal (翻转法线)**：检测模型中法线方向错误的表面，可能导致光照和渲染异常。
    *   **Loose Geometry (游离几何体)**：检测场景中未连接到主要模型的独立几何体。
    *   **Zero-Area Faces / Zero-Length Edges (零面积面/零长度边)**：检测模型中可能存在的微小或无效几何元素。

*   **UV (UV 坐标)**
    *   **Missing UV (UV 缺失)**：检测没有 UV 贴图的模型或面。
    *   **Empty UV (空 UV)**：检测存在 UV 层但其中没有有效 UV 数据的模型。
    *   **Overlap (UV 重叠)**：检测 UV 岛之间存在重叠，可能导致纹理烘焙问题。
    *   **Stretched UV (UV 拉伸)**：检测 UV 布局中存在过度拉伸的区域，影响纹理质量。

*   **Texture (纹理)**
    *   **Missing Texture (纹理缺失)**：检测材质中引用的纹理文件丢失。
    *   **Broken Path (路径断裂)**：检测纹理文件路径不正确或已更改。
    *   **Incorrect Color Space (颜色空间不正确)**：检测纹理是否使用了错误的颜色空间设置。

*   **Transform (变换)**
    *   **Scale (缩放)**：检测模型是否应用了非均匀缩放，或缩放值未重置为 1.0。
    *   **Rotation (旋转)**：检测模型是否应用了非零旋转，或旋转值未重置为 0.0。
    *   **Location (位置)**：检测模型原点是否未居中或未放置在世界原点。

*   **Delivery (交付)**
    *   **Naming (命名)**：检查对象、材质、纹理、集合等是否符合预设的命名规范（例如，无特殊字符，特定前缀/后缀）。
    *   **Collections (集合)**：检查场景中的集合组织是否合理，是否存在空集合或不必要的集合。
    *   **Export Readiness (导出就绪)**：检查模型是否已准备好导出到目标平台（例如，所有修改器已应用，骨骼已绑定）。

## Scoring System

设计一个直观的“READY FOR DELIVERY”评分体系，以百分比形式显示，并列出 Blocking Issues（阻碍性问题）和 Warnings（警告）。

*   **READY FOR DELIVERY Score (0-100%)**：综合所有检查项的通过情况，给出整体就绪度评分。
*   **Blocking Issues (阻碍性问题)**：必须解决的问题，例如非流形几何体、纹理缺失等，这些问题会阻止成功交付。
*   **Warnings (警告)**：建议解决的问题，例如 UV 拉伸、命名不规范等，这些问题可能影响质量但不会完全阻止交付。

## Success Metrics

如何判断 MVP 成功：

*   **用户反馈**：收集用户对工具可用性、准确性和价值的积极反馈。
*   **问题发现率**：工具能够成功发现用户在交付前未察觉到的问题的比例。
*   **返工率降低**：用户报告因使用 Pipeline Inspector 而减少返工的案例数量。
*   **社区提及**：在 Blender 相关社区（Reddit, Blender Artists）中，用户对 Pipeline Inspector 的讨论和推荐数量。
*   **下载量/安装量**：作为 Blender 插件的下载量或安装量达到预设目标。
*   **用户留存率**：衡量用户持续使用该工具的比例。
