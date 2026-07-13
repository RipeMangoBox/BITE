---
title: "Proxy3D: Efficient 3D Representations for Vision-Language Models via Semantic Clustering and Alignment"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Proxy3D_Efficient_3D_Representations_for_Vision_Language_Models_via_Semantic_Clustering_and_Alignment.pdf
project_link: "https://wzzheng.net/Proxy3D"
code_link: null
aliases:
- Proxy3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 利用视觉特征在语义上的稀疏分布，通过语义聚类将3D场景特征压缩为一组紧凑的代理特征（proxy representations），在显著降低视觉序列长度的同时保留空间信息。
primary_logic: 视觉模态中的信息在语义上具有稀疏分布，因此可以通过在潜在空间中按语义分组并聚类（KNN），生成紧凑的3D代理特征；并通过渐进式多阶段训练（从简化语义符号到真实场景）和对齐策略，使语言模型高效理解3D空间关系。
claims:
- "语义分组在视觉定位任务上将总体准确率提升超过20个点（Acc@0.5: 31.0 → 52.6）"
- Proxy3D以仅700个视觉token在ScanRefer上达到59.6 Acc@0.5，超越Chat-Scene（55.5）和Descrip3D（57.2），且序列长度仅为对应关系方法3DRS的不到10%
- 坐标系对齐（Coordinate Alignment）显著提升房间尺寸估计、路径规划和物体出现顺序等VSI-Bench任务表现
- ScanRefer 上 Acc@0.5 (%) = 59.6
---

# Proxy3D: Efficient 3D Representations for Vision-Language Models via Semantic Clustering and Alignment

> [!tip] 核心洞察
> 视觉模态中的信息在语义上具有稀疏分布，因此可以通过在潜在空间中按语义分组并聚类（KNN），生成紧凑的3D代理特征；并通过渐进式多阶段训练（从简化语义符号到真实场景）和对齐策略，使语言模型高效理解3D空间关系。

| 字段 | 内容 |
|------|------|
| 中文题名 | Proxy3D：基于语义聚类与对齐的视觉语言模型高效三维表征 |
| 英文题名 | Proxy3D: Efficient 3D Representations for Vision-Language Models via Semantic Clustering and Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.08064) · [Project](https://wzzheng.net/Proxy3D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Proxy3D |
| Dataset | ScanRefer, VSI-Bench |

> [!tip] 效果简介
> - ScanRefer 上，Acc@0.5 (%) 59.6 vs 55.5 (Chat-Scene) (+4.1)。
> - VSI-Bench 上，Overall (%) 47.0 vs GPT4Scene (具体数值未提供) (显著提升)。

## 概要

3D视觉语言模型（3D-VLM）旨在赋予语言模型对三维场景的空间理解能力。现有方法主要分为两条技术路线：**基于对应关系的方法**（correspondence-based）隐式学习3D空间认知，但缺乏全局场景建模导致空间不一致，且视觉序列长度大、计算代价高；**基于显式表征的方法**（representation-based）直接建模3D场景，但同样面临视觉序列化长度大、难以高效捕捉复杂空间关系的瓶颈。

Proxy3D的核心洞察在于：视觉模态中的信息在语义上具有稀疏分布。基于这一发现，作者提出**语义聚类与对齐**框架——通过语义感知的KNN聚类将3D场景特征压缩为一组紧凑的代理特征（proxy representations），在显著降低视觉序列长度的同时保留关键空间信息。该方法以仅约700个视觉token实现与现有方法相当甚至更优的性能，而基于对应关系的方法（如**3DRS**，Huang et al., NeurIPS 2025）的序列长度超过Proxy3D的10倍。

在方法谱系中，Proxy3D属于**基于显式表征的3D-VLM**，与**LLaVA-3D**（Zhu et al., ICCV 2025）和**LEO-VL**（Huang et al., arXiv 2025）等同类方法相比，其核心差异在于：不直接拼接2D特征图或物体嵌入，而是通过语义分组和聚类生成紧凑的3D代理表征，并采用渐进式多阶段训练（从简化语义符号到真实场景）实现语言模型与3D空间的高效对齐。

实验表明，Proxy3D在ScanRefer视觉定位任务上达到59.6 Acc@0.5，超越Chat-Scene（55.5）和Descrip3D（57.2）；在VSI-Bench空间推理基准上取得47.0的综合得分，在开源模型中排名第二。消融实验揭示，语义分组是性能提升的关键因素——在ScanRefer上带来超过20个点的绝对提升（Acc@0.5: 31.0 → 52.6），而坐标系对齐（Coordinate Alignment）显著改善了房间尺寸估计、路径规划和物体出现顺序等空间推理任务。

然而，与人类水平的空间智能相比仍有显著差距，尤其在Scan2Cap密集描述任务上，基于表征的方法整体落后于基于对应关系的方法，这体现了简洁性与语义丰富性之间的根本权衡。



### 3D视觉语言模型的范式分化

3D视觉语言模型（3D-VLM）旨在使多模态语言模型理解三维场景并执行问答、视觉定位、密集描述等空间推理任务。当前主流方法可归为两大范式，各自面临根本性瓶颈。

**基于对应关系的方法（correspondence-based）** 通过在2D图像与3D场景之间建立隐式映射来注入空间认知。这类方法无需显式建模3D场景结构，但代价显著：由于缺乏全局场景建模，空间一致性难以保证；同时，视觉序列长度随图像帧数和特征分辨率线性增长，计算开销高昂。例如，**3DRS**（Huang et al., NeurIPS 2025）的视觉token序列长度可达Proxy3D的10倍以上。

**基于显式表征的方法（representation-based）** 直接编码3D场景信息（如点云、体素、物体嵌入），理论上更利于空间关系建模。然而，现有方案在视觉序列化上仍显低效：**LLaVA-3D**（Zhu et al., ICCV 2025）使用3D实体定位标记，**LEO-VL**（Huang et al., arXiv 2025）使用750 token的统一表征，均未从根本上解决序列长度与空间信息密度之间的矛盾。更关键的是，这些方法难以高效捕捉复杂空间关系（如物体间相对位置、房间尺寸估计、路径规划），在VSI-Bench等空间推理基准上表现受限。

### 核心瓶颈：视觉序列的冗余与稀疏

上述困境的根源在于视觉模态中信息分布的**语义稀疏性**。一个3D场景往往包含大量视觉特征（像素级或点级），但其中多数特征在语义上高度冗余——同一物体表面、同一语义区域内的特征携带重复信息。现有方法将冗余特征直接序列化送入语言模型，导致：

1. **序列长度膨胀**：冗余token挤占语言模型的上下文窗口，限制了对更长对话历史和更复杂推理链的支持。
2. **空间关系稀释**：关键的空间结构信息被淹没在大量冗余token中，语言模型难以从中提取有效的几何先验。
3. **训练-推理效率失衡**：虽然部分方法在推理时可通过缓存优化，但训练阶段的长序列处理带来显著的计算开销。

### Proxy3D的动机与设计哲学

Proxy3D的核心动机源于一个直接观察：**如果视觉信息在语义上是稀疏分布的，那么可以通过语义分组将场景特征压缩为一组紧凑的代理表征（proxy representations），在显著降低序列长度的同时保留空间结构信息。**

这一设计哲学体现在三个层面：

- **压缩即增强**：通过语义感知的聚类（而非均匀降采样），在压缩过程中主动保留语义边界和物体完整性，使压缩后的代理特征反而比原始冗余特征更有利于空间推理。
- **几何先验显式注入**：代理表征的3D坐标天然携带空间位置信息，通过专门设计的3D空间位置编码（垂直方向RoPE + 水平方向可学习Fourier嵌入），使语言模型无需从扁平序列中隐式推断空间关系。
- **渐进式空间智能培养**：语言模型对3D空间的理解不能一蹴而就。Proxy3D采用四阶段渐进训练——从简化的语义符号对齐，到坐标系对齐，再到空间关系训练，最后替换为真实3D代理特征——逐步构建空间认知能力，避免直接端到端训练带来的优化困难。

### 方法定位与贡献预览

Proxy3D属于基于显式表征的方法，但通过语义聚类机制实现了表征效率的质变。与现有表征方法相比，其视觉序列长度压缩至450–700 tokens（仅为LEO-VL的60%–93%，3DRS的不到10%），同时在ScanRefer视觉定位任务上达到59.6 Acc@0.5，超越Chat-Scene（55.5）和Descrip3D（57.2）；在VSI-Bench空间推理基准上取得47.0 overall，排名开源模型第二。这一“压缩即增强”的反直觉结果，验证了语义稀疏性假设的有效性。



## 核心方法与创新机理

Proxy3D 的核心创新在于将 3D 场景理解中“视觉表征构造”这一关键环节从繁重的像素级或对象级序列化，转变为一种**语义驱动的紧凑代理表征（semantic-aware proxy representation）**。这一转变直接回应了现有 3D‑VLM 的两大瓶颈：

1. **基于对应关系的方法**（如 **3DRS**，Huang et al., NeurIPS 2025）隐式学习 3D 空间认知，但因缺乏全局场景建模而导致空间不一致，且视觉序列长度动辄数千 tokens，计算代价极高。
2. **基于显式表征的方法**（如 **LLaVA-3D**，Zhu et al., ICCV 2025；**LEO-VL**，Huang et al., arXiv 2025）虽直接建模 3D 场景，但视觉序列化长度依然庞大，且难以高效捕捉复杂空间关系。

Proxy3D 的因果调控旋钮（causal knob）在于利用**视觉语义的稀疏分布特性**：同一语义类别的特征在空间中天然聚集，因此可通过语义分组与聚类，将海量像素特征压缩为一组数量极少的 3D 代理特征，在保留空间信息的同时将视觉序列长度削减一个数量级。

### 核心 changed slots 分析

与基线方法相比，Proxy3D 在以下四个关键维度上做出了根本性改变：

**1. 视觉表征构造与序列化：从直接拼接走向语义聚类压缩**

基线方法通常直接拼接 2D 特征图或物体嵌入，导致序列长度普遍超过 3000 tokens。Proxy3D 的核心操作是：首先利用语义分割掩码将视觉特征按类别分组（Equation 1），随后在每个语义组内以空间坐标为基准执行 KNN 聚类（Equation 2），生成 $K_g$ 个代理中心。最终形成的 3D 代理集合 $\mathcal{P}$ 仅包含 450–700 个 tokens（$K \ll L$），却仍能有效表征整个场景的视觉与几何信息。

这一设计的直接证据来自消融实验：语义分组（semantic grouping）使 ScanRefer 的 Acc@0.5 从 31.0 跃升至 52.6，提升幅度超过 20 个点。这表明，语义先验的引入不仅是压缩手段，更是空间理解的关键催化剂。

**2. 空间位置编码：从简单嵌入走向几何感知的 3D 编码**

基线方法通常仅依赖图像像素位置或简单的 3D 位置嵌入，缺乏对三维几何结构的显式建模。Proxy3D 在代理特征上施加了两类互补的位置编码（Equation 4）：
- 对垂直方向（高度 $\mathcal{H}$）施加 **RoPE**（旋转位置编码），捕捉垂直轴上的相对位置关系；
- 对水平方向（宽度 $\mathcal{W}$ 与长度 $\mathcal{L}$）施加**可学习 Fourier 嵌入**，注入水平面上的绝对几何先验。

这一设计的有效性在 VSI-Bench 消融中得到验证：坐标系对齐（Coordinate Alignment）显著提升了房间尺寸估计、路径规划和物体出现顺序等任务的性能，并将 ScanRefer 的 Uni@0.5 从 83.2 提升至 84.0。

**3. 物体引用机制：从可学习嵌入走向语义‑标识符融合**

传统方法使用可学习嵌入或直接文本描述来引用物体，灵活性受限。Proxy3D 引入了**标识符嵌入**（identifier embedding）和**语义嵌入**（semantic embedding）的双通道机制：两者分别从简化图像中生成，通过加法融合后直接注入代理序列，支持 `<OBJXXX>` 格式的物体引用。这一设计使模型无需额外的可学习嵌入即可灵活指代任意物体，同时保持了表征的紧凑性。

**4. 训练策略：从单阶段微调走向四阶段渐进式对齐**

基线方法通常直接在 3D 场景数据上进行单阶段微调，模型难以同时消化视觉压缩、空间对齐和复杂推理等多重挑战。Proxy3D 设计了四阶段渐进式训练流水线（Figure 3），由易到难逐步构建空间智能：
- **Stage 1**：简化语义‑标识符嵌入融合对齐，建立基本的视觉‑语言映射；
- **Stage 2**：坐标系对齐，使模型精确理解 3D 位置嵌入与几何坐标的对应关系；
- **Stage 3**：空间关系训练，培养物体间相对位置与场景结构的推理能力；
- **Stage 4**：真实 3D 代理特征替换微调，将前序阶段习得的能力迁移至完整 3D 场景。

这一渐进策略的核心价值在于：它将复杂的 3D 空间理解任务分解为可逐步攻克的子技能，避免了直接端到端训练可能面临的优化困难。训练总耗时约 62 小时（8× A6000 GPU），但推理时仅需处理极短的视觉序列，实现了训练成本与推理效率的有利权衡。

### 创新边界与局限

尽管 Proxy3D 在表征效率与空间推理上取得了显著进展，其创新仍存在明确边界：
- 在 Scan2Cap 密集描述任务上，基于表征的方法（包括 Proxy3D）整体落后于基于对应关系的方法，这可能体现了简洁表征与语义丰富性之间的根本权衡；
- 几何预测器 VGGT 仅输出归一化点云，需额外尺度估计步骤，可能引入误差；
- 与人类水平的空间智能相比仍有显著差距，尤其在 VSI-Bench 的某些子任务上。

这些局限为后续研究指明了方向：如何在不牺牲紧凑性的前提下增强代理表征的语义细粒度，以及如何将方法泛化至动态场景或室外大规模环境，是 Proxy3D 范式面临的核心开放问题。



Proxy3D 提出了一套从多视角图像到紧凑三维代理表征的完整流水线，核心思路是利用视觉模态中信息的**语义稀疏性**，将高维场景特征压缩为一组低基数代理（proxies），再通过渐进式多阶段对齐使语言模型理解三维空间关系。整体流程可概括为四个环节：多源特征提取 → 语义感知聚类 → 空间编码与序列化 → 多阶段视觉-语言对齐。

### 多源特征提取

系统首先从输入的多视图图像中并行提取三类互补信息（Figure 2）：

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/002_Figure_2.jpg]]
*Figure 2: Proxy3D architecture. A geometry predictor and a semantic encoder output latent features of vision modality. Then, our proxy 3D representations are clustered to reduce complexity. Lastly, multi-stage training aligns proxy features with the language model*

- **2D视觉特征图**：由视觉编码器（如 Qwen2.5-VL 的视觉骨干）输出，提供稠密的语义描述。
- **点云图（point maps）**：由几何预测器 **VGGT** 生成，给出每个像素对应的三维坐标。需注意 VGGT 输出为归一化坐标，作者额外估计了尺度因子以恢复真实尺度信息。
- **语义分割掩码**：由 **SAM 2** 提供像素级语义标签，用于后续的语义分组。

三者对齐后形成三元组集合 $\{ \mathbf{f}_j, \mathbf{p}_j, \mathbf{m}_j \}_{j=1}^{L}$，分别对应视觉特征、三维坐标和语义标签，序列长度 $L$ 通常为数万量级。

### 语义感知聚类（核心瓶颈突破）

这是 Proxy3D 实现序列压缩的关键模块。不同于直接拼接所有特征或仅按物体实例组织，Proxy3D 利用语义标签将特征按类别分组，再在每组内进行空间聚类：

1. **语义分组**（Equation 1）：将三元组按掩码标签 $g$ 归入集合 $\mathcal{G}_g$。
2. **KNN聚类**（Equation 2）：在每个语义组内，基于三维坐标 $\mathbf{p}_k$ 执行 K 近邻聚类，生成 $K_g$ 个代理中心。
3. **代理生成**（Equation 3）：每个聚类中心对应一个代理 $(\mathbf{z}_{g,j}, \mathbf{c}_{g,j})$，分别聚合该簇的视觉特征和空间质心坐标。

最终代理总数 $K = \sum_g K_g \ll L$，典型配置下 $K$ 仅为 450–700，相比原始特征序列压缩了两个数量级。这一设计直接回应了现有方法的瓶颈：**基于对应关系的方法**（如 **3DRS**, Huang et al., NeurIPS 2025）需维护超长序列（Proxy3D 的 10 倍以上），而**基于显式表征的方法**（如 **LLaVA-3D**, Zhu et al., ICCV 2025；**LEO-VL**, Huang et al., arXiv 2025）虽直接建模场景但序列仍偏长且难以高效捕捉空间关系。

### 空间编码与序列化

为让语言模型理解代理之间的三维空间关系，Proxy3D 对每个代理特征注入几何位置先验（Equation 4）：

- **垂直方向**：应用旋转位置编码（RoPE），利用高度坐标 $\mathcal{H}$ 进行旋转变换。
- **水平方向**：施加可学习的 Fourier 位置嵌入，编码宽度 $\mathcal{W}$ 和长度 $\mathcal{L}$ 坐标。

注入位置信息后，所有语义组的代理特征按**广度优先搜索（BFS）**顺序拼接为最终视觉序列 $\mathbf{Z}$（Equation 5），使空间近邻的代理在序列中也彼此靠近，利于后续的自回归建模。

### 物体引用机制

为支持 `<OBJXXX>` 格式的物体引用，Proxy3D 额外引入了**标识符嵌入**和**语义嵌入**生成器。两者从简化图像（simplified images）中生成中间嵌入，通过加法融合后直接注入代理序列。这一设计避免了传统方法中需要学习额外可学习嵌入的负担，使物体引用更灵活。

### 多阶段渐进式训练

Proxy3D 采用四阶段训练策略（Figure 3），从简化的语义符号逐步过渡到真实三维场景，使语言模型渐进地习得空间智能：

1. **阶段一**：简化语义-标识符嵌入融合对齐，在图像-文本层面建立基础关联。
2. **阶段二**：坐标系对齐（Coordinate Alignment），让模型精确理解三维位置嵌入与几何坐标的对应关系（Figure 4）。
3. **阶段三**：空间关系训练，在真实场景数据上学习物体间空间推理。
4. **阶段四**：将简化嵌入替换为真实 3D 代理特征，进行最终指令微调。

训练目标为标准的自回归负对数似然损失（Equation 6），基于代理序列 $\mathbf{Z}$ 预测回答 token。整个训练流程在 8×A6000 GPU 上约需 62 小时（Table 1），但推理时因序列极短而高效。



Proxy3D 的核心设计围绕一个关键洞察展开：视觉模态中的信息在语义上具有稀疏分布，因此可以通过语义聚类将高维场景特征压缩为一组紧凑的代理表征（proxy representations），在显著降低视觉序列长度的同时保留空间信息。整个流水线由以下模块构成。

### 视觉特征提取

给定一组多视图图像，Proxy3D 采用三个预训练模型并行提取场景的互补信息：

- **2D 视觉编码器**（2D visual encoder）提取图像特征图 $\mathbf{f}_j$；
- **几何预测器**（geometry predictor，具体为 VGGT）输出点云图 $\mathbf{p}_j$，提供每个像素的三维坐标；
- **2D 分割模型**（具体为 SAM 2）生成像素级语义掩码 $\mathbf{m}_j$。

三者对齐后形成长度为 $L$ 的特征-坐标-掩码三元组 $\{ \mathbf{f}_j, \mathbf{p}_j, \mathbf{m}_j \}_{j=1}^{L}$。

### 语义聚类：从密集特征到紧凑代理

这是整个方法的**核心因果调节旋钮**。其关键操作是将视觉特征按语义标签分组后，在每组内进行 K 近邻聚类，从而将场景压缩为少量代理特征。

**步骤 1：语义分组。** 将三元组按语义掩码标签 $g$ 分组：

$$
\mathcal{G}_g = \{ \mathbf{f}_j, \mathbf{p}_j \mid \mathbf{m}_j = g \}, \quad j = 1, 2, \ldots, L \tag{1}
$$

**步骤 2：KNN 聚类。** 对每个语义组 $\mathcal{G}_g$，以点云坐标 $\mathbf{p}_k$ 为距离度量进行 K 近邻聚类，生成 $K_g$ 个聚类中心：

$$
\{ \mathcal{C}_{g,j} \}_{j=1}^{K_g} = \mathrm{KNN}(\mathcal{G}_g, \mathbf{p}_k) \tag{2}
$$

**步骤 3：代理集合构造。** 每个聚类中心对应一个代理，其视觉特征为聚类内特征的聚合（原文未显式给出聚合函数，但暗示为聚类中心的特征），三维坐标为该聚类中心的空间位置：

$$
\mathcal{P} = \{ \mathbf{z}_{g,j}, \mathbf{c}_{g,j} \} = \{ \mathbf{f}_j, \mathbf{p}_j \mid g \}, \quad g, j \in \{ \mathcal{C}_{g,j} \} \tag{3}
$$

通过语义聚类，场景特征从原始长度 $L$（通常数千个 token）压缩至 $K = \sum_g K_g \ll L$。消融实验表明，这一操作在视觉定位任务上将 Acc@0.5 从 31.0 提升至 52.6，提升超过 20 个点，是 Proxy3D 性能的决定性因素。

### 3D 空间位置编码

语义聚类后的代理特征需要注入空间几何先验，使语言模型能够理解三维空间关系。Proxy3D 采用**双轴解耦的位置编码策略**：

$$
\mathbf{z}_{g,j}' = R(\mathbf{c}_{g,j \in \mathcal{H}}) \, \mathbf{z}_{g,j} + F(\mathbf{c}_{g,j \in \{ \mathcal{W} \times \mathcal{L} \}}) \tag{4}
$$

- **垂直方向（$\mathcal{H}$）**：对代理特征施加旋转位置嵌入（RoPE），以代理中心的高度坐标为参数进行旋转变换 $R(\cdot)$；
- **水平方向（$\mathcal{W} \times \mathcal{L}$）**：对代理的宽度和长度坐标施加可学习的 Fourier 嵌入 $F(\cdot)$，以加法方式注入。

这种设计将三维空间的各向异性纳入位置编码：垂直方向通过旋转操作保留特征内积关系，水平方向则通过加法注入绝对位置信息。消融实验证实，坐标系对齐（Coordinate Alignment）显著提升了房间尺寸估计、路径规划和物体出现顺序等 VSI-Bench 子任务的表现。

### BFS 序列化与代理特征矩阵

聚类后的代理特征需要按空间近邻关系排序，以形成语言模型可处理的有序序列。Proxy3D 对代理的三维中心坐标进行**广度优先搜索（BFS）遍历**，将空间相邻的代理在序列中也相邻放置。最终将所有语义组的代理特征拼接为代理特征矩阵：

$$
\mathbf{Z} = [\mathbf{Z}_1, \mathbf{Z}_g, \ldots, \mathbf{Z}_G], \quad \mathbf{Z}_g = [\mathbf{z}_{g,1}', \mathbf{z}_{g,2}', \ldots, \mathbf{z}_{g,K_g}'] \tag{5}
$$

其中 $\mathbf{Z}_g$ 为第 $g$ 个语义组的代理特征序列，$G$ 为语义类别总数。

### 物体引用机制：标识符嵌入与语义嵌入

为支持 `<OBJXXX>` 格式的物体引用，Proxy3D 引入两类可学习嵌入生成器：

- **语义嵌入** $G_{\text{sem}}(n_j)$：从物体类别的简化图像 $n_j$ 生成；
- **标识符嵌入** $G_{\text{id}}(m_j)$：从物体标识符 $m_j$ 生成。

两者通过加法融合后直接注入代理序列，使模型无需额外可学习嵌入即可引用特定物体。

### 指令微调损失

最终，代理特征矩阵 $\mathbf{Z}$ 作为视觉前缀输入语言模型，训练目标为标准自回归负对数似然损失：

$$
\mathcal{L}(\boldsymbol{\theta}) = -\sum_{i=K+1}^{r} \log P_{\boldsymbol{\theta}}(t_i \mid t_{<i}, \mathbf{Z}) \tag{6}
$$

其中 $K$ 为代理序列长度，$r$ 为完整序列（视觉 token + 文本 token）的总长度，$t_i$ 为目标文本 token。

### 补充图表

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/003_Figure_3.jpg]]
*Figure 3: Proxy3D multi-stage training. Each stage in our progressive iterative training aims to develop a certain spatial intelligence skill from the easiest one to more complex ones: we begin with the simplified image-text alignment to actual images with spatial reasoning*

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/004_Figure_4.jpg]]
*Figure 4: Coordinate alignment stage helps an MLLM to precisely align 3D positional embeddings with geometric coordinates*



## 实验与关键发现

### 核心定量结果

Proxy3D 以极短的视觉序列长度在多项 3D 场景理解基准上取得竞争性或领先性能。Table 2 汇总了 3D 问答、视觉定位和密集描述三大任务的对比结果。在 ScanRefer 视觉定位任务上，Proxy3D（Qwen2.5-VL-7B 骨干）以仅 700 个视觉 token 达到 **59.6 Acc@0.5**，超越 Chat-Scene（55.5）和 Descrip3D（57.2），而基于对应关系的方法 3DRS 则需要超过 10 倍的序列长度。在 3D 问答任务（ScanQA、SQA3D）上，Proxy3D 以不到对应关系方法 10% 的视觉 token 量实现了相近的问答性能，与同为基于表征的 LEO-VL（750 token）性能几乎一致。

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/006_Table_2.jpg]]
*Table 2: Evaluation of 3D question answering, visual grounding and dense captioning. We follow the standard evaluation methodology for all benchmarks. We categorize models by their type, used vision modalities (P - point clouds, I - images, B - bird’s-eye-view map, D - depth), sequence length L (# of tokens). The best and the second best results are highlighted. Our Proxy3D with Qwen2.5-VL backbone shows competitive or state-of-the-art results with the shortest sequence lengths. ”‡” means usage of extra information from point clouds*

在 VSI-Bench 空间推理基准上，Proxy3D 以 **47.0 Overall** 排名开源模型第二（Table 3），大幅超越基础模型 Qwen2-VL-7B 和 GPT4Scene。Figure 5 的可视化结果显示，Proxy3D 在 Scannet++ 和 ARKitScenes 两个未见场景划分上均表现出良好的泛化能力，能够处理复杂的空间推理问题。Figure 6 进一步展示了 Proxy3D 在不同数据划分和任务维度上的鲁棒性，但各子任务的指标分布并不均匀。

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/007_Table_3.jpg]]
*Table 3: Evaluation of 3D spatial reasoning on VSI-Bench. We use 16 frames as input for Qwen2.5VL-based baselines and, following the VSI-Bench setup, other open-source and proprietary models use from 16 to 32 image frames. The best and the second best results for open-source models are highlighted. Our Proxy3D with Qwen2.5-VL-7B backbone shows overall the second best result. At the same time, the gap with the human-level performance remains significant in spatial reasoning certain tasks. ”‡” indicates tasks not specifically trained*

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/008_Figure_5.jpg]]
*Figure 5: Proxy3D performance on VSI-Bench [46]. Left is on Scannet++ [48], right is on ARKitScenes [3]. Proxy3D generalizes well on unseen scenes, and is capable of solving difficult questions*

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/009_Figure_6.jpg]]
*Figure 6: Comparison of VSI-Bench tasks and splits i.e. ARKitScenes [3], Scannet++ [48] and Scannet [13]. Results show Proxy3D robustness to data splits and uneven metrics across tasks*

### 消融实验

Table 4 系统消融了 Proxy3D 各核心组件的贡献，揭示了以下关键因果链路：

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/010_Table_4.jpg]]
*Table 4: Ablation study on various aspects of the Proxy3D approach: inter-frame cross attention in vision encoder, semantic grouping, coordinate alignment, feature map resolution and number of proxy tokens. In this study, we justify effectiveness of the proposed methods in Proxy3D and present hyperparameters (feature map resolution and visual # of tokens) for complexity-accuracy trade-off tuning*

**语义分组是性能提升的最大单一因素。** 移除语义分组后，ScanRefer Acc@0.5 从 52.6 骤降至 31.0，降幅超过 20 个点。这表明直接在原始特征上进行聚类无法有效保留语义结构，语义感知的分组机制对于构建紧凑且信息丰富的 3D 代理表征至关重要。

**坐标系对齐（Coordinate Alignment）显著提升空间推理精度。** 在 VSI-Bench 的 ScanNet 划分上（Figure 7），坐标系对齐在物体计数、房间尺寸估计和距离判断等任务上带来了明显增益，ScanRefer Uni@0.5 从 83.2 提升至 84.0。该阶段通过让 MLLM 精确对齐 3D 位置嵌入与几何坐标，使模型获得了更准确的空间度量能力。

**代理序列长度与特征图分辨率构成复杂度-精度权衡。** 将代理 token 数从 450 增至 1000，ScanQA C 分数从 92.7 提升至 94.3；将特征图分辨率从 16×21 提升至 32×42 同样带来性能增益。这意味着用户可根据推理预算灵活调整精度。

**动态分配方案中，每个语义组最优代理数为 5。** Table 5 显示，在总 token 预算固定为 700 的条件下，每组分配 5 个代理时 Scan2Cap C 分数达到 74.9，表明适度的组内聚类粒度能在紧凑性和语义覆盖度之间取得最佳平衡。

此外，帧间交叉注意力（inter-frame cross attention）在视觉编码器中的引入对性能影响有限，说明 Proxy3D 的性能增益主要来自代理表征和训练策略，而非编码器架构的改进。

### 失败模式与局限性

尽管 Proxy3D 在空间推理上表现突出，但与人类水平相比仍存在显著差距（Table 3），尤其在需要精细空间关系理解的子任务上。在 **Scan2Cap 密集描述**任务上，Proxy3D 及所有基于表征的方法均显著落后于基于对应关系的方法。这一现象揭示了当前方法的本质权衡：代理表征通过语义聚类实现了极高的压缩率，但聚类过程不可避免地丢失了细粒度的物体外观和空间细节信息，限制了其在需要逐物体精细描述的任务上的表现。

几何预测器 VGGT 仅输出归一化点云坐标，为保留真实尺度信息，作者额外估计了尺度因子（具体方法未在论文中详细披露），该环节可能引入累积误差，影响尺寸相关任务的精度。

训练成本方面，完整的四阶段渐进式训练在 8×A6000 GPU 上耗时约 62 小时（Table 1），训练开销较高。但推理阶段得益于极短的视觉序列长度（450–700 token），实际推理效率显著优于对应关系方法。

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/005_Table_1.jpg]]
*Table 1: Estimated Proxy3D training time in hours using Section 3.2 training procedure and 8× A6000 NVIDIA GPUs*

### 补充图表

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/011_Figure_7.jpg]]
*Figure 7: Ablation study on VSI-Bench’s Scannet [13] split. Proxy3D outperforms the base Qwen2-VL-7B and GPT4Scene by a large margin in object counting, size and distance estimation. Coordinate alignment (CA) and longer sequences further increase metrics*

![[assets/figures/papers/paper_list_l2240_https_arxiv_org_abs_2605_08064/figures/012_Table_5.jpg]]
*Table 5: Ablation study on dynamic allocation of group-aware proxies from Section 3.1 for Proxy3D with 700 tokens*



## 定位与知识库关联

### 3D-VLM 技术路线的分岔与 Proxy3D 的定位

当前 3D 视觉语言模型（3D-VLM）主要沿两条技术路线演进：**基于对应关系的方法**（correspondence-based）与**基于显式表征的方法**（representation-based）。Proxy3D 属于后者，但其核心创新在于通过语义聚类将表征压缩为紧凑的代理特征，从而在两条路线之间找到了一个独特的效率-精度平衡点。

**基于对应关系的方法**以 **3DRS**（Huang et al., NeurIPS 2025）为代表。该类方法将 3D 场景隐式地编码到 2D 图像与文本的对齐中，绕过了显式的 3D 建模。其优势在于可借助成熟的 2D-VLM 能力，但代价是：缺乏全局场景建模导致空间不一致，且视觉序列长度极高（3DRS 的序列长度是 Proxy3D 的 10 倍以上），计算代价大。

**基于显式表征的方法**则直接建模 3D 场景。**LLaVA-3D**（Zhu et al., ICCV 2025）使用 3D 实体定位标记，**LEO-VL**（Huang et al., arXiv 2025）使用 750 token 的统一表征，**Chat-Scene**（Zhang et al., CVPR 2024）和 **Descrip3D**（Xue et al., WACV 2026）则基于物体提案或物体描述增强来理解场景。这类方法的共同瓶颈在于：视觉序列化长度仍然较大，且难以高效捕捉复杂空间关系。

**Proxy3D 的方法论创新**体现在四个关键维度的系统性重构：

1. **视觉表征构造与序列化**：从“直接拼接 2D 特征图或物体嵌入（序列长度 >3000 tokens）”转变为“通过语义聚类（KNN）生成紧凑的 3D 代理特征，序列长度压缩至 450–700 tokens”。这一转变的因果机制在于：视觉模态中的信息在语义上具有稀疏分布，按语义分组后聚类可大幅去冗余。

2. **空间位置编码**：从“仅依赖图像像素位置或简单 3D 位置嵌入”升级为“结合 RoPE（垂直方向）和可学习 Fourier 嵌入（水平方向）的 3D 空间位置编码”。这一设计使模型能区分垂直与水平维度的几何先验，为后续的坐标系对齐训练奠定基础。

3. **物体引用机制**：从“使用可学习嵌入或直接文本描述”改为“引入标识符嵌入和语义嵌入（从简化图像生成），通过加法融合直接注入代理序列，支持 `<OBJXXX>` 格式引用”。这使得物体引用不再依赖额外的可学习参数，增强了泛化性。

4. **训练策略**：从“直接使用 3D 场景数据进行单阶段微调”升级为“四阶段渐进式训练”——阶段一完成简化语义-标识符嵌入融合对齐，阶段二进行坐标系对齐，阶段三训练空间关系，阶段四替换为真实 3D 代理特征微调。这种由易到难的课程学习策略，是模型逐步习得空间智能的关键。

### 适用边界与局限

**适用场景**：Proxy3D 在需要高效空间推理的任务上表现突出，包括 3D 问答（ScanQA、SQA3D）、视觉定位（ScanRefer）和空间推理基准（VSI-Bench）。其紧凑的视觉序列长度（450–700 tokens）使其在推理效率上具有天然优势。

**已知局限**：

- **密集描述任务的瓶颈**：在 Scan2Cap 密集描述任务上，Proxy3D 及所有基于表征的方法均显著落后于基于对应关系的方法。这可能揭示了表征压缩与语义丰富性之间的根本权衡——代理特征虽然紧凑，但在需要细粒度物体描述时可能丢失信息。

- **尺度估计的依赖**：几何预测器 VGGT 仅输出归一化点云坐标，为保留尺度信息，作者需额外估计尺度因子（具体方法未在论文中充分披露）。这一外部依赖可能引入误差，影响房间尺寸估计等尺度敏感任务。

- **训练成本**：四阶段训练总耗时约 62 小时（8× A6000 GPU），训练成本较高。但推理阶段效率极高，这一投入在部署场景下可被摊薄。

- **与人类水平的差距**：VSI-Bench 结果显示，Proxy3D 虽在开源模型中排名第二（Overall 47.0），但与人类水平相比仍有显著差距，尤其在空间推理的某些子任务上。

### 开放问题与未来方向

论文明确提出了以下开放问题：

1. **奖励学习（GRPO）的潜力**：如何利用强化学习进一步对齐 Proxy3D 的空间推理能力与人类偏好？
2. **复杂度-准确度权衡曲线**：不同特征图分辨率（16×21 vs 32×42）与代理 token 数量（450–1000）之间的确切权衡关系尚需更系统的刻画。
3. **小物体与密集场景**：当前代理表征在处理小物体或需要密集场景描述时能力受限，如何改进聚类策略或分配机制以保留更多细粒度信息？
4. **动态与室外场景泛化**：该方法目前仅在室内静态场景（ScanNet、ScanNet++、ARKitScenes）上验证，是否能泛化到动态场景或室外大规模场景尚待探索。

### 知识库定位

Proxy3D 在 3D-VLM 知识图谱中占据“高效显式表征”这一节点。它继承了基于表征方法的显式 3D 建模优势，同时通过语义聚类解决了该类方法长期面临的序列长度瓶颈。与 **LEO-VL**（750 tokens 统一表征）相比，Proxy3D 以更少的 token（700）实现了相当或更优的性能，且在空间推理任务上表现更稳健。与 **3DRS** 等基于对应关系的方法相比，Proxy3D 以不到 10% 的视觉序列长度取得了有竞争力的结果，证明了“语义稀疏性”这一先验假设在 3D 场景理解中的有效性。

该方法的技术贡献可被后续工作沿两个方向继承：一是语义聚类的思想可推广至其他需要视觉 token 压缩的多模态任务；二是四阶段渐进式训练策略为 3D 空间智能的课程学习提供了可复用的范式。



## 原文 PDF

![[paperPDFs/CVPR_2026/Proxy3D_Efficient_3D_Representations_for_Vision_Language_Models_via_Semantic_Clustering_and_Alignment.pdf]]
