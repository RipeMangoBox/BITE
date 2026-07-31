---
title: "腾讯混元 3D 数据算子实习准备"
type: social
updated: 2026-07-05
tags:
  - social
  - internship
  - Tencent
  - Hunyuan3D
  - 3D_Data_Curation
---

# 腾讯混元 3D 数据算子实习准备

## 当前结论

已确定入职。下周入职，本周目标不是提前做模型，而是把自己准备成一个能快速接手 **3D 纹理/材质数据清洗与质量检测算子** 的实习生。

从电话和后续问答看，实际工作边界如下：

- 团队：混元 3D 团队，基础数据小组。
- 任务：聚焦 3D 纹理/材质数据清洗、质检、缺陷分类、规则设计、badcase 分析和算子开发。
- 日常形态：算子开发和看数据都会有；需要人工查看、标注、复核，也会参与规则、评测标准和评测集讨论。
- 资源现实：很多任务可用 CPU 和传统 graphics 算法解决，GPU 申请可能困难；不要把准备重心放在训练大模型上。
- 产出预期：明确不支持或无法支撑论文发表；成果更可能是内部工具、规则体系、评测集、数据报告、pipeline 模块。
- 指标：更接近准确率、召回率、漏检率、误杀率、吞吐、覆盖率、人工复核成本，而不是生成模型效果指标。
- 下游关系：在混元 3D 内部，但当前任务不直接接算法训练反馈闭环；需要主动把数据质量问题整理成可迁移的技术沉淀。

> [!important] 入职后的核心判断
> 这段实习的真实价值不在“做 3D 生成模型”，而在是否能把数据清洗做成 **可复用的质量标准、缺陷 taxonomy、自动化检测算子、评测集和 badcase 分析体系**。如果只停留在人工看数据，会比较亏；如果能把人工经验沉淀为规则、指标和工具，就有简历价值。

> [!note] 本次补强结论
> 有其他重要工作需要提前熟悉。最高优先级不是再追模型版本，而是读 [[analysis/arxiv_2026/HY3D-Bench_Generation_of_3D_Assets|HY3D-Bench]]，因为它公开展示了混元 3D 团队如何把原始 3D 资产整理成水密网格、多视图渲染、部件级分解和可训练数据。其次读 [[analysis/arxiv_2025/Hunyuan3D_Studio_End-to-End_AI_Pipeline_for_Game-Ready_3D_Asset_Generation|Hunyuan3D Studio]]、[[analysis/ICCV_2025/MaterialMVP_Illumination-Invariant_Material_Generation_via_Multi-view_PBR_Diffusion|MaterialMVP]] 和 [[analysis/arxiv_2025/Hunyuan3D-Omni_A_Unified_Framework_for_Controllable_Generation_of_3D_Assets|Hunyuan3D-Omni]]。这四篇已下载、分析入库并更新索引。

## 入职前本周目标

### 成功标准

本周准备完成后，应该能做到：

1. 听懂 3D 资产数据问题：mesh、UV、texture、PBR、albedo、roughness、metallic、normal map、glTF/OBJ/FBX 的基本差异。
2. 能提出一个数据质检算子的结构：输入资产、抽取指标、判定规则、输出标签、人工复核、计算 precision/recall。
3. 能用 CPU 工具做最小实验：批量读取 3D 资产，生成 manifest，检查常见几何/纹理问题，渲染缩略图辅助人工复核。
4. 能把“看数据”转化成缺陷分类表，而不是只做主观评价。
5. 对混元 3D 的技术路线有概念，但不把短期目标误判成模型训练。

### 一周准备优先级

**第一优先级：3D 资产与数据质检基础。**

- 资产格式：`.obj`、`.mtl`、`.fbx`、`.glb/.gltf`、贴图文件、PBR metallic-roughness workflow。
- mesh 基础指标：顶点/面数、bbox、尺度归一化、连通分量、非流形边、自交、重复顶点/面、退化三角形、法线方向、watertight。
- UV/纹理指标：是否有 UV、UV 是否越界/重叠、贴图是否缺失、贴图分辨率、透明通道、纯色/低信息纹理、压缩伪影、接缝、拉伸、模糊。
- PBR 指标：albedo 是否带烘焙光照，metallic/roughness 是否空间错位，normal map 是否存在且方向合理。

**第二优先级：算子工程能力。**

- 用 `trimesh` / `Open3D` / Blender Python 做批处理。
- 输出结构化 JSON/CSV，保留 asset id、路径、规则命中、分数、人工标签、可视化缩略图。
- 先写可解释规则，不追求深度模型。
- 每个规则都要能计算误杀和漏检，不要只写“看起来不好”。

**第三优先级：领域研究脉络。**

- 了解混元 3D 生成为何强调两阶段：先形状，再纹理/PBR。
- 了解为什么 PBR 材质比 RGB 贴图更贴近工业生产。
- 了解 3D 数据规模化时为什么质量标注、过滤和去重是瓶颈。

## 工作任务拆解

### 1. 人工看数据不是低价值，低价值的是没有沉淀

刚入职很可能会做大量资产查看、标注、复核。要把它变成技术工作，关键是每次看数据都记录：

- 这个样本错在哪里：几何、UV、纹理、材质、尺度、语义、文件缺失、渲染异常。
- 错误是否可被自动规则检测。
- 规则输入是什么：mesh 几何、贴图统计、渲染图、文件元数据、人工标签。
- 规则输出是什么：二分类、缺陷类别、多级质量分、需要复核/直接过滤。
- 规则可能误杀什么：例如纯白雕塑不应被判为“无纹理”；镜面材质不应被判为“高光烘焙”。

可用的工作记录模板：

```markdown
### Badcase: <asset_id>

- 观察到的问题：
- 缺陷类别：
- 可自动化信号：
- 需要人工判断的部分：
- 初始规则：
- 可能误杀：
- 可能漏检：
- 下次验证样本：
```

### 2. 质量标准要分层，不要混成一个“好/坏”

建议把缺陷分类拆成四层：

**资产完整性。**

- 文件能否加载。
- 引用贴图是否缺失。
- 材质槽是否为空。
- 单位、尺度、朝向是否异常。
- 是否存在极端大文件、极端多面数、极端贴图分辨率。

**几何质量。**

- 退化三角形、重复面、重复点。
- 非流形边、孤立面、孤立小组件。
- 法线方向混乱、面片翻转。
- bbox 比例异常、薄片化、悬浮碎片。
- watertight 与否要看任务要求，不应一刀切。

**纹理/UV 质量。**

- 无 UV、有 UV 但贴图缺失。
- UV 越界、重叠、拉伸、岛过碎。
- 纹理分辨率过低、模糊、压缩块、纯色低信息。
- 接缝明显、多视角不一致。

**PBR/材质质量。**

- albedo 中残留阴影/高光，即 baked lighting。
- metallic/roughness 与 albedo 语义区域错位。
- normal map 缺失、方向异常、强度过大。
- 材质不符合语义：木头金属度高、玻璃无透明/高光属性等。

## 入职后前两周执行计划

### 第 0 周：本周准备

- 读完本文“必读论文”中的前 5 篇。
- 安装或熟悉 `trimesh`、`Open3D`、Blender Python、`numpy`、`pandas`、`Pillow`。
- 做一个本地 toy pipeline：读取一批公开 `.glb/.obj`，输出质量 manifest。
- 写一页个人入职问题清单：数据格式、标签体系、已有标准、评测集、算子提交方式、代码仓库规范。

### 第 1 周：到岗后先拿到标准和样本

优先问清楚：

- 当前数据源有哪些：自有数据、外采资产、生成数据、开源数据、人工修复数据。
- 输入/输出格式是什么：是否统一到 glTF/OBJ/FBX，贴图命名和目录规范是什么。
- 现有缺陷标签有哪些，是否已有正负样本。
- 一个算子的交付形态是什么：脚本、服务、SQL、pipeline 节点、离线报告。
- 指标怎么算：谁给人工真值，precision/recall 的验收阈值是多少。
- 错误代价：宁愿多过滤还是少过滤，误杀和漏检哪一个更严重。

第 1 周不要急着展示“我懂模型”。更有用的是能快速复现已有流程、读懂数据结构、补齐缺陷样例。

### 第 2 周：开始做一个小而完整的算子闭环

目标是拿一个缺陷类别做完整闭环：

1. 收集 50-100 个正负样本。
2. 写清楚缺陷定义和边界例子。
3. 实现一个 CPU 规则或轻量图像统计算子。
4. 输出 `asset_id -> score -> label -> reason`。
5. 人工复核误杀/漏检。
6. 更新阈值和规则。
7. 写一个短报告：指标、失败案例、下一步。

可选题目按性价比排序：

- 贴图缺失 / 材质引用错误检测。
- 纯色或低信息纹理检测。
- 贴图分辨率过低或压缩伪影检测。
- mesh 退化面 / 重复面 / 非流形边检测。
- UV 越界 / 面积异常 / 拉伸粗检。
- albedo 烘焙阴影粗检：用多视角渲染和亮度统计做启发式，不要一开始就上模型。

## CPU-only 小实验清单

### 实验 A：资产 manifest 生成器

输入：一个 3D 资产目录。

输出：每个资产一行 JSON/CSV：

- 文件格式、文件大小、贴图数量、贴图分辨率。
- 顶点数、面数、材质数、UV 层数、bbox 尺寸。
- 是否可加载、是否缺贴图、是否有空材质。
- 是否有退化面、重复面、非有限值坐标。
- 基础渲染缩略图路径。

价值：这是所有算子的地基，也能快速发现数据源格式混乱问题。

### 实验 B：缺陷标签 taxonomy

拿 30-50 个样本，人工标：

- `load_fail`
- `missing_texture`
- `empty_material`
- `degenerate_geometry`
- `non_manifold_risk`
- `uv_missing`
- `uv_out_of_range`
- `texture_low_information`
- `texture_blurry`
- `baked_lighting`
- `pbr_channel_misalignment`
- `needs_human_review`

每个标签写 2 个正例和 2 个边界例子。这个 taxonomy 比单纯看论文更能帮助入职。

### 实验 C：低信息纹理检测

CPU 即可做：

- 读取贴图。
- 统计颜色方差、边缘强度、熵、有效像素比例。
- 区分“故意纯色材质”和“无效贴图”需要人工复核，不要只靠方差一刀切。

参考 Objaverse++ 的质量标注思路：它专门标注“单色”“不完整”“无意义”等资产质量问题，用来过滤不适合学习纹理生成的对象。

### 实验 D：渲染缩略图 + 人工复核表

用 Blender headless 渲染固定 6 视角缩略图：

- front/back/left/right/top/isometric。
- 每个样本生成一张 contact sheet。
- 人工复核时不直接打开 3D 软件，先在网页或表格里看缩略图。

价值：减少人工看数据成本，也为后续训练/评测 VLM 质检器保留样本。

### 实验 E：算子评测协议

不要只输出命中数量。每个算子都应维护：

- `TP`：正确过滤坏样本。
- `FP`：误杀好样本。
- `FN`：漏掉坏样本。
- `TN`：正确保留好样本。
- precision、recall、F1。
- 高置信自动处理区和低置信人工复核区。

真正工业可用的算子通常不是“全自动替代人”，而是“把明显样本自动处理，把模糊样本送人工”。

## 必读论文与资料

### A. 直接服务入职任务

1. [[analysis/SIGGRAPH_2023/Textured_Mesh_Quality_Assessment_Large-scale_Dataset_and_Deep_Learning-based_Quality_Metric|Textured Mesh Quality Assessment]]

   读法：重点看它如何把 textured mesh 质量转成渲染图块的感知质量评估。你的任务虽然未必能训练 Graphics-LPIPS，但它提供了很好的质量评估思维：3D 质量最后要落到渲染可见的几何/纹理退化上。

2. [[analysis/SIGGRAPH_2022/TextureMe_High-quality_Textured_Scene_Reconstruction_in_Real_Time|TextureMe]]

   读法：重点看纹理和几何对应关系、纹理 patch、对齐、模糊、视角权重。它能帮助理解为什么同一个 mesh 的纹理质量不能只看贴图文件，还要看贴图如何附着到表面。

3. [[analysis/PYTORCH_LIBRARY_2019/Kaolin_A_PyTorch_Library_for_Accelerating_3D_Deep_Learning_Research|Kaolin]]

   读法：不是为了用 Kaolin 训练模型，而是补齐 3D 表示、mesh/point cloud/voxel/SDF、渲染、Chamfer、IoU 等基础概念。入职沟通时这些词会频繁出现。

4. [[analysis/SIGGRAPH_2022/Immersive-Labeler_Immersive_Annotation_of_Large-scale_3D_Point_Clouds_in_Virtual_Reality|Immersive-Labeler]]

   读法：重点看标注效率如何被界面、预标注、视觉辅助影响。你的工作会有人工看数据，这篇提醒你：标注流程本身可以被工程优化。

5. [[analysis/ICLR_2025/Eagle_2_Building_Post_Training_Data_Strategies_from_Scratch_for_Frontier_Vision_Language_Models|Eagle 2]]

   读法：虽然不是 3D 资产论文，但它说明数据策略、规则过滤、格式化和错误分析能显著影响模型能力。对你来说，价值在“数据清洗是模型能力的前置杠杆”，不是它的模型结构。

### B. 混元 3D 与 PBR 材质主线

**新增必读。**

1. [[analysis/arxiv_2026/HY3D-Bench_Generation_of_3D_Assets|HY3D-Bench]]

   重点：数据清洗、格式标准化、质量过滤、水密化、多视图渲染、部件级分解和 AIGC 合成补长尾。它和“基础数据小组”的关系最直接。入职前重点看它的 pipeline：原始资产如何变成训练就绪资产，哪些步骤可以映射成质检算子。

2. [[analysis/arxiv_2025/Hunyuan3D_Studio_End-to-End_AI_Pipeline_for_Game-Ready_3D_Asset_Generation|Hunyuan3D Studio]]

   重点：从图像/文本到 game-ready asset 的端到端生产链路，包括 part-level generation、PolyGen 自动重拓扑、SeamGPT 语义 UV 展开、纹理合成和动画。它提醒你：工业 3D 资产质量不只看“生成好不好看”，还要看拓扑、UV、材质、动画和引擎可用性。

3. [[analysis/ICCV_2025/MaterialMVP_Illumination-Invariant_Material_Generation_via_Multi-view_PBR_Diffusion|MaterialMVP]]

   重点：多视图 PBR 材质生成、光照不变训练、albedo 与 metallic-roughness 通道空间对齐。它能直接支持 `baked_lighting`、PBR 通道错位、材质语义不合理等质检标签。

4. [[analysis/arxiv_2025/Hunyuan3D-Omni_A_Unified_Framework_for_Controllable_Generation_of_3D_Assets|Hunyuan3D-Omni]]

   重点：点云、体素、包围盒、骨骼等显式几何先验如何作为控制信号进入 3D 生成。短期不用复现，但它能帮助你理解数据字段、几何先验和可控生成接口为什么会影响下游资产质量。

**已有主线。**

5. [[analysis/arxiv_2025/Hunyuan3D_2_1_From_Images_to_High_Fidelity_3D_Assets_with_Production_Ready_PBR_Material|Hunyuan3D 2.1]]

   重点：两阶段架构；形状生成和纹理生成解耦；PBR 输出 albedo、metallic、roughness；3D-Aware RoPE；光照不变训练。它和你所在团队最贴近。

6. [[analysis/arxiv_2025/Hunyuan3D_2_5_Towards_High_Fidelity_3D_Assets_Generation_with_Ultimate_Details|Hunyuan3D 2.5]]

   重点：LATTICE 形状基础模型、PBR 多视图材质生成、共享注意力掩码保证 albedo 与 MR 通道空间对齐。短期不用复现，读它是为了理解为什么数据质量会直接影响高保真 3D 资产。

7. [[analysis/SIGGRAPH_ASIA_2024/Boosting_3D_Object_Generation_through_PBR_Materials|Boosting 3D Object Generation through PBR Materials]]

   重点：从 RGB 贴图升级到 PBR 材质，SAM/VLM 辅助语义材质赋值，法线/凹凸图精炼。它适合启发“自动检查材质语义是否合理”的长期小探索。

8. [[analysis/SIGGRAPH_2024/DreamMat_High-quality_PBR_Material_Generation_With_Geometry-_and_Light-aware_Diffusion_Models|DreamMat]]

   重点：反照率中残留烘焙光照是材质生成常见问题；几何和光照条件能帮助材质-光照解耦。它能直接支持 `baked_lighting` 这类质检标签。

9. [[analysis/NEURIPS_2021/DIB_R_Learning_to_Predict_Lighting_and_Material_with_a_Hybrid_Differentiable_Renderer|DIB-R++]]

   重点：材质、光照、几何解耦；高光/金属/粗糙度为什么不能用简单 RGB 解释。读概念即可。

### C. 3D 生成领域概览与长期储备

这些不服务第一周工作，但服务长期简历叙事：

- [[analysis/arxiv_2025/Hunyuan3D_1_0_A_Unified_Framework_for_Text_to_3D_and_Image_to_3D_Generation|Hunyuan3D 1.0]]：了解混元 3D 早期统一框架。
- [[analysis/arxiv_2025/Hunyuan3D_2_0_Scaling_Diffusion_Models_for_High_Resolution_Textured_3D_Assets_Generation|Hunyuan3D 2.0]]：了解高分辨率 textured 3D assets 的基础版本。
- [[analysis/NEURIPS_2022/GET3D_A_Generative_Model_of_High_Quality_3D_Textured_Shapes_Learned_from_Images|GET3D]]：经典 textured shape 生成基础。
- [[analysis/SIGGRAPH_ASIA_2022/CLIP-Mesh_Generating_textured_meshes_from_text_using_pretrained_image-text_models|CLIP-Mesh]]：早期 text-to-textured-mesh 思路。
- [[analysis/ICCV_2023/TexFusion_Synthesizing_3D_Textures_with_Text_Guided_Image_Diffusion_Models|TexFusion]]：文本引导 3D 纹理合成。
- [[analysis/SIGGRAPH_2024/Diffusion_Texture_Painting|Diffusion Texture Painting]]：扩散模型用于纹理绘制。
- [[analysis/SIGGRAPH_ASIA_2024/TEXGen_a_Generative_Diffusion_Model_for_Mesh_Textures|TEXGen]]：mesh texture diffusion 方向。

读法：每篇只抓三件事：输入/输出是什么，如何保证多视角/UV 一致性，最常见失败模式是什么。

### D. 数据集与数据质量资料

- [[analysis/arxiv_2026/HY3D-Bench_Generation_of_3D_Assets|HY3D-Bench]]：混元 3D 团队公开的数据生态工作，包含 252k 级高质量水密网格、多视图渲染、部件级分解和 125k 级 AIGC 合成长尾资产。对入职最有用的是它的质量处理链：格式统一、方向对齐、质量过滤、水密化、点云采样、渲染和测试集构造。

- Objaverse 1.0：80 万级带描述、标签、动画的 3D 对象集合。
- Objaverse-XL：1000 万级 3D 对象集合，强调规模、多来源、去重和渲染多视图用于训练 Zero123-XL。
- Objaverse++：对 Objaverse 资产做质量标注，包含“单色”“不完整”等可用于过滤纹理生成数据的标签。
- Textured Mesh Quality Assessment 数据集：55 个源模型、34.3 万以上失真刺激、3000 个主观评分样本，用于学习和验证 textured mesh 质量度量。

这些资料给你的直接启发是：3D 生成不是“数据越多越好”，而是需要 **质量标签、过滤规则、去重、失真类型建模、人工评分协议**。

## Web 补强记录

本次补强检索到的外部资料：

- [Hunyuan3D 2.1 arXiv](https://arxiv.org/abs/2506.15442)：形状生成和 PBR 纹理生成两阶段架构；Hunyuan3D-Paint 生成 albedo、metallic、roughness，并使用空间对齐注意力、3D-aware RoPE 和光照不变训练。
- [Hunyuan3D 2.5 arXiv](https://arxiv.org/abs/2506.16504)：引入 LATTICE 形状基础模型，最大 10B 参数；纹理端升级为 PBR 多视图生成。
- [HY3D-Bench arXiv](https://arxiv.org/abs/2602.03907)：混元 3D 团队的数据生态工作，强调高质量水密网格、多视图渲染、部件级分解和合成长尾资产。
- [Hunyuan3D Studio arXiv](https://arxiv.org/abs/2509.12815)：端到端 game-ready 3D 资产生产管线，覆盖重拓扑、UV、纹理、动画等工程交付环节。
- [Hunyuan3D-Omni arXiv](https://arxiv.org/abs/2509.21245)：在 Hunyuan3D 2.1 上加入点云、体素、包围盒、骨骼等显式控制信号。
- [MaterialMVP arXiv](https://arxiv.org/abs/2503.10289)：多视图 PBR 扩散材质生成，强调光照不变性和 albedo/MR 通道对齐。
- [Hunyuan3D 2 GitHub](https://github.com/Tencent-Hunyuan/Hunyuan3D-2)：开源说明中将系统拆成 Hunyuan3D-DiT 形状生成和 Hunyuan3D-Paint 纹理合成。
- [Objaverse-XL arXiv](https://arxiv.org/abs/2307.05663)：1000 万以上 3D 对象，说明 3D 数据规模化与质量获取的关系。
- [Objaverse++ arXiv HTML](https://arxiv.org/html/2504.07334v1)：对 3D 对象做质量标注，特别适合参考缺陷 taxonomy。
- [Textured Mesh Quality Assessment arXiv](https://arxiv.org/abs/2202.02397)：纹理网格质量数据集和 Graphics-LPIPS。
- [trimesh 文档](https://trimesh.org/)：Python mesh 加载、处理、修复、watertight 检查等 CPU 工具。
- [Open3D 文档](https://www.open3d.org/docs/release/)：3D 数据处理和可视化工具。
- [Blender Python Mesh API](https://docs.blender.org/api/current/bpy.types.Mesh.html)：读取 mesh、UV、材质、渲染缩略图时需要。
- [glTF 2.0 PBR 说明](https://www.khronos.org/gltf/pbr/)：理解 metallic-roughness 工作流。

## 入职沟通问题清单

到岗后尽快问清楚，不要一次性逼问，可以按任务自然确认：

1. 当前最优先的缺陷类别是什么？纹理缺失、低质纹理、PBR 错位、UV 问题、几何异常，哪一类最痛？
2. 有没有已有标签体系？如果没有，我是否可以先整理一个最小 taxonomy？
3. 算子的输入/输出接口是什么？文件夹批处理、数据库字段、内部平台节点，还是脚本报告？
4. 准确率和召回率的验收标准是什么？误杀和漏检哪个成本更高？
5. 人工标注集由谁给？是否能拿一批已确认的正负例做开发集？
6. 算子是否要求可解释？输出是否需要 reason code？
7. 是否允许我保存匿名化 badcase 截图和规则总结，用于内部报告？
8. 代码规范、数据权限、不能外传的内容边界是什么？

## 简历沉淀方式

不要写“参与 3D 数据清洗”。应争取最终能写成：

- 设计并实现 3D 纹理/材质数据质量检测算子，覆盖贴图缺失、低信息纹理、UV 异常、几何退化等缺陷类别。
- 构建 3D 资产质量标签 taxonomy 与人工复核流程，形成可计算的 precision/recall 评测协议。
- 搭建 CPU-only 3D 资产批处理 pipeline，支持资产 manifest 抽取、规则打分、badcase 可视化和质检报告生成。
- 参与混元 3D 基础数据小组数据治理，为高质量 3D/PBR 资产生成数据提供清洗与评测支持。

如果实际工作允许，再补：

- 探索基于渲染缩略图/VLM 的低置信样本辅助复核流程。
- 分析 PBR 材质通道错位、albedo 烘焙光照、纹理-几何不一致等生成资产失败模式。

## 风险提醒

- 不要把“无 GPU”理解成完全没有技术含量。数据算子、质量标准和评测闭环本来就应该先用规则和 CPU pipeline 做稳。
- 不要把论文阅读当成入职准备的主体。最重要的是能处理真实资产、真实格式、真实坏样本。
- 不要过早承诺 VLM/深度模型质检。没有 GPU、没有标注集、没有闭环时，VLM 只能作为长期探索，不是第一阶段主线。
- 不要只追求 recall。工业数据清洗常常要在误杀成本和漏检成本之间取舍，阈值需要由业务目标决定。
- 不要把“不能发论文”视为完全无沉淀。内部工具、规则体系、报告、评测集和 pipeline 都能成为下一段实习的证据。

## 原始咨询结论归档

电话总结：

1. 聚焦纹理数据清洗的算子开发，任务重；大量任务可以 CPU 解决，例如传统 graphics 算法，部分需要人工打标；GPU 申请可能比较困难。
2. 明确任务无法支撑或不支持论文发表。
3. 实习时间三个月起步。
4. 明确当前任务与算法训练反馈关系较弱，使用准确率、召回率等指标。
5. 具体任务到岗后进一步明确，流程当前仍需入职后对齐。

后续问答：

- 人工打标/质检与算子开发都会有。
- 缺陷分类体系、规则设计和 badcase 分析都会涉及。
- 标注集、质检标准、评测集都可以参与讨论。
- 项目在混元 3D 团队内，属于基础数据小组。
