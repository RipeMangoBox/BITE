---
title: "Dense-SfM: Structure from Motion with Dense Consistent Matching"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching.pdf
project_link: https://icetea-cv.github.io/densesfm/
code_link: null
aliases:
- DS
- Dense-SfM
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过高斯溅射评估三维点可见性以延长轨迹，并结合基于Transformer与高斯过程的多视图核化匹配模块进行轨迹精细化。"
primary_logic: "利用高斯溅射进行轨迹扩展可以避免量化带来的精度损失，同时提供更长的轨迹，使多视图细化模块能利用更多观测信息，从而在不牺牲密度的情况下显著提高重建精度。"
claims:
- "在ETH3D三角测量中，Dense-SfM (RoMa+Ours) 达到84.79%的1cm准确度和36.35%的5cm完整度，均显著超越LoFTR+DFSfM等基线。"
- "基于高斯溅射的轨迹扩展使平均轨迹长度从2.11增至4.97，从而使细化模块能利用更多视图。"
- "消融实验显示，去除高斯过程模块导致1cm准确度从84.79%降至72.47%，验证了多视图核化匹配架构的关键作用。"
- "相较于DFSfM的量化匹配，高斯溅射轨迹扩展同时提高了三角测量的准确度和完整度。"
---

# Dense-SfM: Structure from Motion with Dense Consistent Matching

> [!tip] 核心洞察
> 利用高斯溅射进行轨迹扩展可以避免量化带来的精度损失，同时提供更长的轨迹，使多视图细化模块能利用更多观测信息，从而在不牺牲密度的情况下显著提高重建精度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Dense-SfM: 稠密一致匹配的结构从运动方法 |
| 英文题名 | Dense-SfM: Structure from Motion with Dense Consistent Matching |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2501.14277) · [Project](https://icetea-cv.github.io/densesfm/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Dense-SfM |
| Dataset | ETH3D triangulation |

> [!tip] 效果简介
> - ETH3D triangulation 上，Accuracy @1cm (%) 为 84.79，对比 80.38 (LoFTR+DFSfM)，变化 +4.41。
> - ETH3D triangulation 上，Completeness @5cm (%) 为 36.35，对比 29.54 (LoFTR+DFSfM)，变化 +6.81。

## 概要

### 问题瓶颈

传统基于稀疏关键点的结构从运动（Structure-from-Motion, SfM）在弱纹理区域面临点云精度与密度不足的困境。近年来，稠密匹配方法虽能提供更丰富的对应关系，但产生的特征轨迹往往呈现碎片化——同一三维点在不同视图间的对应关系断裂，难以直接输入现有SfM管道。DFSfM等现有方案采用量化匹配来缓解轨迹断裂问题，然而量化操作本身会引入精度损失，损害三维点的准确度与完整度。

### 核心思路

Dense-SfM的核心洞察在于：**利用高斯溅射（Gaussian Splatting）进行轨迹扩展可以避免量化带来的精度损失，同时提供更长的轨迹，使多视图细化模块能利用更多观测信息，从而在不牺牲密度的情况下显著提高重建精度。**

具体而言，Dense-SfM通过三个关键设计解决上述瓶颈：

1. **高斯溅射驱动的轨迹扩展**：将初始SfM的三维点投影到新视图上，通过高斯溅射沿光线累积透明度来评估点的可见性，从而将可见视图纳入轨迹，实现无量化损失的轨迹延长。
2. **多视图核化匹配模块**：结合Transformer的多视图注意力机制与高斯过程（Gaussian Process）的坐标嵌入预测，对扩展后的轨迹进行精细化调整，并直接学习每个轨迹的置信度分数。
3. **稠密双向匹配与相互验证**：利用稠密匹配模型进行双向匹配，通过验证正反向映射的坐标一致性过滤不可靠匹配，为初始SfM提供高质量对应关系。

### 方法定位

Dense-SfM定位于**稠密匹配驱动的SfM框架**，与现有方法的关系如下：

- 相较于传统稀疏SfM（如COLMAP），Dense-SfM以稠密匹配替代稀疏关键点检测，在弱纹理区域具有显著优势。
- 相较于DFSfM的量化匹配方案，Dense-SfM以高斯溅射可见性评估替代量化操作，避免了精度损失。
- 相较于VGGSfM等端到端可微分SfM，Dense-SfM保留了明确的几何优化阶段（捆绑调整），在精度上更具竞争力。
- 相较于PixSfM基于特征度量的关键点调整，Dense-SfM的多视图核化匹配模块直接回归坐标分布与置信度，细化效果更优。

### 主要结果

在ETH3D三角测量基准上，Dense-SfM（搭配RoMa稠密匹配器）取得了显著优势：

- **1cm准确度**：84.79%，较LoFTR+DFSfM的80.38%提升4.41个百分点。
- **5cm完整度**：36.35%，较LoFTR+DFSfM的29.54%提升6.81个百分点。

消融实验进一步验证了各组件的关键作用：

- 高斯溅射轨迹扩展使平均轨迹长度从2.11增至4.97，为细化模块提供了更丰富的多视图观测。
- 去除高斯过程模块后，1cm准确度从84.79%骤降至72.47%，验证了多视图核化匹配架构中坐标嵌入路径的核心贡献。
- 基于学习到的置信度选择轨迹的策略进一步提升了细化精度，两次迭代即可获得最大收益。



结构从运动（Structure from Motion, SfM）旨在从多视角图像中同时恢复三维场景结构与相机位姿，是三维视觉与自动驾驶等领域的核心基础技术。传统 SfM 管道依赖稀疏关键点检测与匹配，在纹理丰富区域表现可靠，但在弱纹理或重复纹理区域，关键点数量急剧下降，导致重建点云稀疏、精度不足。近年来，基于学习的密集匹配方法（如 LoFTR、RoMa）能够在弱纹理区域产生大量对应关系，为提升 SfM 的密度与精度提供了新的可能。

然而，密集匹配引入了一个关键瓶颈：**轨迹断裂问题**。密集匹配通常在图像对上独立进行，缺乏多视图间的一致性约束，导致同一三维点在不同视图对中的匹配关系无法关联成连续的特征轨迹。这种断裂轨迹难以直接输入现有的 SfM 管道进行三角测量与捆绑调整。现有方法 **DFSfM** 采用量化匹配策略来解决这一问题——将匹配坐标映射到离散网格以强制轨迹一致性，但量化操作不可避免地引入精度损失，损害了三角测量的准确度与完整度。这一矛盾构成了本领域的核心挑战：**如何在利用密集匹配提升覆盖率的同时，保持轨迹的一致性与亚像素精度？**

Dense-SfM 的动机正是打破这一僵局。该方法提出以**高斯溅射（Gaussian Splatting）**替代量化操作来评估三维点在不同视图中的可见性，从而在连续坐标空间中扩展特征轨迹，避免量化带来的精度折损。同时，为了充分利用扩展后的长轨迹中包含的多视图信息，Dense-SfM 设计了一个**多视图核化匹配模块**，结合 Transformer 的注意力机制与高斯过程的坐标嵌入能力，对轨迹进行精细化回归并学习逐轨迹的置信度分数。这一设计使得轨迹细化模块能够从更多观测视图中获取信息，在不牺牲密度的前提下显著提升重建精度——这是该方法区别于先前工作的核心因果机制。



## 核心方法与创新机理

Dense‑SfM 的核心创新并非提出全新的 SfM 范式，而是针对**稠密匹配在 SfM 管道中产生的“断裂轨迹”瓶颈**，引入两个相互协同的 changed slots，使得稠密匹配的精度优势能够真正转化为三维重建的密度与精度提升。

### 瓶颈诊断：稠密匹配的“断裂轨迹”困境

传统稀疏关键点匹配（如 SIFT）在弱纹理区域能获得的匹配点数量有限，直接限制了重建点云的精度和密度。稠密匹配（如 LoFTR、RoMa）虽然能提供丰富的对应关系，但其产生的匹配在不同视图间缺乏一致性，形成大量短小、断裂的特征轨迹（tracks）。这些断裂轨迹难以直接输入现有的 SfM 管道进行有效的多视图几何优化，成为制约重建质量的关键瓶颈。

现有方法 **DFSfM** 采用**量化匹配**策略来强制轨迹一致性：将匹配坐标量化到固定网格，使来自不同视图的匹配能够对齐到同一轨迹。然而，这种量化操作不可避免地引入精度损失，在提升完整度的同时牺牲了三维点的准确性。

### Changed Slot 1：基于高斯溅射的轨迹可见性评估与扩展

Dense‑SfM 的第一个关键创新在于**用高斯溅射（Gaussian Splatting, GS）替代量化匹配来实现轨迹扩展**，从根本上避免了量化带来的精度损失。

其因果机制如下：在初始 SfM 模型构建完成后，为每个三维点初始化一个小尺度的高斯椭球体，并通过少量优化步骤拟合场景几何。随后，对于每个待扩展的视图，沿相机光心到三维点的光线累积透明度，计算可见性评分：

$$M = [ \max_{r \in R} \{ \alpha_{\mathrm{SfM}} \prod_{j=1}^{N_{\mathrm{SfM}}-1} (1 - \alpha_{j}) \} > \epsilon_{\nu} ]$$

若累积透明度超过阈值 $\epsilon_{\nu}$，则判定该三维点在该视图中可见，将其投影坐标纳入该点的轨迹。这一过程将平均轨迹长度从 **2.11 提升至 4.97**（Table 6），为后续多视图细化模块提供了更丰富的观测信息，同时保持了亚像素级的投影精度。

消融实验验证了这一设计的决定性作用：将 GS 轨迹扩展替换为量化方法（$r=4$）后，1cm 准确度显著下降，证实了避免量化对精度保持的关键价值（Table 3 与 Sec. 4.5）。

### Changed Slot 2：多视图核化匹配的轨迹细化模块

仅扩展轨迹长度不足以保证重建质量——更长的轨迹需要更强大的多视图一致性优化机制。Dense‑SfM 的第二个关键创新是**多视图核化匹配模块**，通过 Transformer 与高斯过程（Gaussian Process, GP）的双路径架构实现轨迹精细化。

与 DFSfM 中使用统计方差选择轨迹的策略不同，Dense‑SfM 的细化模块直接学习每个轨迹的置信度分数。具体架构包含两条互补路径：

- **基于特征的路径（Multi‑view Transformer）**：对参考视图和查询视图的局部特征图施加自注意力和交叉注意力，捕获多视图间的特征级对应关系。
- **基于坐标嵌入的路径（Gaussian Process）**：利用指数余弦相似度核函数 $k(f_A, f_B) = \exp(-\tau) \exp(\tau \frac{\langle f_A, f_B \rangle}{\sqrt{\langle f_A, f_A \rangle \langle f_B, f_B \rangle + \varepsilon}})$ 计算特征相似度，通过 GP 后验均值 $\mu(\mathbf{F}_R | \mathbf{F}_{Q_i})$ 预测查询视图的坐标嵌入特征，显式建模空间位置先验。

两条路径的输出拼接后送入 CNN 解码器，同时回归坐标概率分布 $P_{Q_i}$ 和置信度分数 $S_{Q_i}$。训练时采用带置信度加权的回归损失：

$$\mathcal{L} = \frac{1}{N} \sum_{j \in n_t} \sum_{i \in n_j} s_{Q_i} \cdot \| p_{Q_i} - p_{gt} \|_2 - \alpha \log s_{Q_i}$$

其中 $-\alpha \log s_{Q_i}$ 项作为对数障碍函数，防止模型输出过低的置信度。

消融实验揭示了这一设计的因果重要性：**去除高斯过程模块后，1cm 准确度从 84.79% 骤降至 72.47%**（Table 3），验证了坐标嵌入路径对多视图几何一致性的关键建模作用。单独使用 Transformer 或 GP 均不及完整双路径架构，表明两者在特征匹配与空间推理上形成互补。

### 创新协同效应

两个 changed slots 之间存在强协同关系：GS 轨迹扩展为多视图核化匹配模块提供了更长、更一致的输入轨迹，使 Transformer 和 GP 能够利用更多视图的观测信息进行精细化；而细化模块学习到的置信度分数又反过来指导轨迹选择，过滤不可靠的匹配，形成正向反馈循环。实验表明，两次迭代的细化能够获得最大收益（Table 3），继续增加迭代次数收益微小，说明该协同机制在两轮内即可收敛。

### 与基线方法的关键差异总结

| 组件 | 基线方法（DFSfM） | Dense‑SfM | 创新本质 |
|------|-------------------|-----------|----------|
| 轨迹一致性 | 量化匹配（固定网格对齐） | 高斯溅射可见性评估 | 避免量化精度损失，保持亚像素精度 |
| 多视图细化 | Transformer + 统计方差选轨 | Transformer + 高斯过程 + 学习置信度 | 引入空间先验，端到端学习轨迹可靠性 |
| 匹配策略 | 半密集匹配 | 密集双向匹配 + 相互验证 | 提升弱纹理区域覆盖，过滤不可靠匹配 |



![[assets/figures/papers/paper_list_l48_Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline Overview. From a set of images, we construct an initial SfM model using dense two-view matching, filtering unreliable matches through mutual verification. To extend track length, we project 3D points onto additional images, using a visibility filter based on Gaussian Splatting. We then refine these extended tracks with our track refinement module and perform geometric bundle adjustment to improve the accuracy of SfM model*

Dense-SfM 采用三阶段流水线解决稠密匹配在 SfM 中的轨迹断裂问题，其核心设计目标是在不牺牲密度的前提下，通过高斯溅射可见性评估延长轨迹，并利用多视图核化匹配模块进行精细化。

### 阶段一：初始 SfM 构建

输入为一组无序图像。首先使用两视图稠密匹配器（如 RoMa）对所有图像对进行稠密特征匹配。为抑制冗余并保证可靠性，流水线依次执行两步过滤：

1. **非极大值抑制**：基于逐像素匹配置信度分数进行采样，抑制半径根据数据集调整（ETH3D 为 4 像素，Texture-Poor SfM 和 IMC 数据集为 2 像素）。
2. **双向验证**：利用稠密匹配的双向映射特性过滤不可靠匹配。对于图像 A 中的像素 $p_a$，通过匹配模型 $\mathcal{M}_{AB}$ 映射到图像 B 得到 $p_b$，再通过 $\mathcal{M}_{BA}$ 映射回 A 得到 $p_{a'}$。仅当 $\|p_a - p_{a'}\|_2 \leq \epsilon_p$（$\epsilon_p=3$ 像素）时保留该匹配。该过程如图 Figure 3 所示。

过滤后的可靠匹配经三角测量和捆绑调整，生成包含稀疏三维点和相机位姿的初始 SfM 模型。

### 阶段二：高斯溅射轨迹扩展

初始 SfM 模型的轨迹通常较短（平均长度约 2.11），限制了后续多视图细化可利用的观测数量。Dense-SfM 通过高斯溅射解决此瓶颈：

1. **3D 高斯初始化**：为每个 SfM 点初始化一个小型 3D 高斯，尺度按 $S = D_{max} / f$ 设置，使投影半径近似为 1 像素。
2. **可见性评估**：将 SfM 点投影到其他视图，通过沿光线累积透明度判断可见性。可见性掩码定义为：
   $$M = [ \max_{r \in R} \{ \alpha_{\mathrm{SfM}} \prod_{j=1}^{N_{\mathrm{SfM}}-1} (1 - \alpha_{j}) \} > \epsilon_{\nu} ]$$
   若沿某条光线累积的透明度超过阈值 $\epsilon_{\nu}$，则认为该点在该视图可见。
3. **轨迹扩展**：对可见视图，通过投影公式 $p_{ij} = \Pi ( R_{i} P_{j} + t_{i}, C_{i} )$ 建立新的匹配对，将对应图像纳入该三维点的轨迹。

相比 DFSfM 的量化匹配方法，高斯溅射轨迹扩展避免了量化带来的精度损失，同时将平均轨迹长度从 2.11 提升至 4.97（Table 6），为后续多视图细化提供了更丰富的观测信息。

### 阶段三：迭代 SfM 精细化

扩展后的轨迹输入多视图核化匹配模块进行精细化，随后执行几何捆绑调整。该阶段迭代两次以获得最大收益（继续增加迭代次数收益微小，见 Table 3）。

**多视图核化匹配模块**（Figure 4）由两条并行路径组成：

- **特征路径（多视图 Transformer）**：对参考视图和查询视图的局部特征图施加自注意力和交叉注意力，获取变换后的特征表示。
- **坐标嵌入路径（高斯过程）**：利用指数余弦相似度核 $k(f_A, f_B) = \exp(-\tau) \exp(\tau \frac{\langle f_A, f_B \rangle}{\sqrt{\langle f_A, f_A \rangle \langle f_B, f_B \rangle + \varepsilon}})$ 计算特征向量间的相似性，通过后验均值 $\mu(\mathbf{F}_R | \mathbf{F}_{Q_i}) = K^{RQ_i} (K^{Q_i Q_i} + \sigma_n^2 I)^{-1} \chi^{Q_i}$ 预测查询视图的坐标嵌入特征。

两条路径的输出拼接后送入 CNN 解码器（由残差块和通道注意力块组成），生成坐标概率分布 $P_{Q_i}$ 和置信度分数 $S_{Q_i}$。精细化坐标的回归策略如 Figure 5 所示：在参考视图上，通过聚合各查询视图的置信度分数选择最高分像素；在查询视图上，通过通道级 softmax 获取概率分布并计算加权平均。训练时采用联合优化坐标和置信度的损失函数：
$$\mathcal{L} = \frac{1}{N} \sum_{j \in n_t} \sum_{i \in n_j} s_{Q_i} \cdot \| p_{Q_i} - p_{gt} \|_2 - \alpha \log s_{Q_i}$$

**几何捆绑调整**则最小化所有轨迹观测的鲁棒重投影误差：
$$E = \sum_j \sum_{x_k^* \in \mathcal{T}_j^*} \rho(\| \pi(\pmb{\xi}_i \cdot P_j, C_i) - x_k^* \|_2^2)$$
重投影误差超过 $\epsilon_f=3$ 像素的匹配被作为离群点剔除。

### 输入输出流总结

| 阶段 | 输入 | 核心操作 | 输出 |
|------|------|----------|------|
| 初始 SfM | 无序图像集 | 稠密两视图匹配 → NMS → 双向验证 → 三角测量 → BA | 稀疏 3D 点云 + 相机位姿 |
| 轨迹扩展 | 初始 SfM 模型 | 3D 高斯初始化 → 可见性渲染 → 投影建立新匹配 | 延长后的特征轨迹 |
| 迭代精细化 | 扩展轨迹 | 多视图核化匹配 → 置信度轨迹选择 → BA | 精细化 3D 点云 + 相机位姿 |

整个流水线如 Figure 2 所示，三个阶段的模块化设计使得各组件可独立消融验证，也为后续端到端联合优化留有扩展空间。



Dense-SfM 的核心创新在于两个相互衔接的模块：**基于高斯溅射的轨迹扩展**和**多视图核化特征轨迹细化**。前者解决稠密匹配产生的断裂轨迹问题，后者利用扩展后的长轨迹进行高精度关键点回归。

### 3.1 初始匹配与双向验证

初始 SfM 构建从稠密两视图匹配开始。给定图像对 $A$ 和 $B$，通过稠密匹配模型 $\mathcal{M}_{AB}$ 和 $\mathcal{M}_{BA}$ 获取双向对应关系：

$$p_{b} = \mathcal{M}_{AB}[p_{a}], \quad p_{a'} = \mathcal{M}_{BA}[p_{b}]$$

其中 $p_a$ 为图像 $A$ 中的像素坐标，$p_b$ 为其在图像 $B$ 中的匹配点，$p_{a'}$ 为 $p_b$ 反向映射回 $A$ 的坐标。匹配可靠性通过双向一致性过滤：

$$B = [ ||p_{a} - p_{a'}||_{2} \leq \epsilon_{p} ]$$

当正向-反向映射的欧氏距离小于阈值 $\epsilon_p$（通常设为 3 像素）时，该匹配被保留。此双向验证机制（Figure 3）有效剔除了稠密匹配中的不可靠对应，提高了初始 SfM 模型的质量。

### 3.2 高斯溅射轨迹扩展

传统方法（如 DFSfM）通过量化匹配将稠密对应离散化以形成一致轨迹，但量化过程不可避免地损失精度。Dense-SfM 转而利用高斯溅射进行**连续空间**的可见性评估，从而在不引入量化误差的前提下扩展轨迹。

具体而言，对每个初始 SfM 三维点，在其位置初始化一个微小的高斯体，尺度 $S$ 设置为：

$$S = \frac { D _ { m a x } } { f }$$

使得投影半径近似为 1 像素（$D_{max}$ 为场景深度最大值，$f$ 为焦距）。随后通过高斯溅射渲染判断该点在目标视图中的可见性：

$$M = [ \max_{r \in R} \{ \alpha_{\mathrm{SfM}} \prod_{j=1}^{N_{\mathrm{SfM}}-1} (1 - \alpha_{j}) \} > \epsilon_{\nu} ]$$

其中 $R$ 为相机光线集合，$\alpha_{\mathrm{SfM}}$ 为目标高斯体的透明度，$\alpha_j$ 为沿光线其他高斯体的透明度。当累积透明度超过阈值 $\epsilon_{\nu}$ 时，判定该三维点在当前视图可见。若可见，则通过投影方程将其加入轨迹：

$$p_{ij} = \Pi ( R_{i} P_{j} + t_{i}, C_{i} )$$

其中 $P_j$ 为三维点坐标，$R_i$ 和 $t_i$ 为相机 $i$ 的旋转与平移，$C_i$ 为相机内参。

**因果机制**：高斯溅射避免了量化网格的离散化误差，同时通过透明度累积自然地处理遮挡关系。实验表明，该模块将平均轨迹长度从 2.11 提升至 4.97（Table 6），使后续细化模块能利用更多视图的观测信息。

### 3.3 多视图核化特征轨迹细化

轨迹扩展后，Dense-SfM 采用多视图核化匹配模块（Figure 4）对关键点坐标进行精细化。该模块包含两条并行路径：

**特征路径（多视图 Transformer）**：对参考视图和查询视图的局部特征图施加自注意力和交叉注意力，捕获多视图间的特征依赖关系。

**坐标嵌入路径（高斯过程）**：利用位置编码信息，通过指数余弦相似度核函数计算特征向量间的相似性：

$$k(f_A, f_B) = \exp(-\tau) \exp\left(\tau \frac{\langle f_A, f_B \rangle}{\sqrt{\langle f_A, f_A \rangle \langle f_B, f_B \rangle + \varepsilon}}\right)$$

其中 $\tau$ 为温度参数，$\langle \cdot, \cdot \rangle$ 表示内积。基于该核函数，高斯过程后验均值预测查询视图 $Q_i$ 的坐标嵌入特征：

$$\mu(\mathbf{F}_R | \mathbf{F}_{Q_i}) = K^{RQ_i} (K^{Q_i Q_i} + \sigma_n^2 I)^{-1} \chi^{Q_i}$$

两条路径的输出拼接后送入 CNN 解码器 $D_\theta$，生成坐标概率分布和置信度：

$$P_{Q_i}, S_{Q_i} = D_\theta(\hat{\mathbf{F}}_R \oplus \hat{\mathbf{F}}_{Q_i} \oplus \mu(\mathbf{F}_R | \mathbf{F}_{Q_i}))$$

其中 $\hat{\mathbf{F}}_R$ 和 $\hat{\mathbf{F}}_{Q_i}$ 为 Transformer 输出的特征图，$P_{Q_i}$ 为精细化坐标的概率分布，$S_{Q_i}$ 为每个查询视图的置信度分数。

**训练损失**联合优化坐标回归和置信度学习：

$$\mathcal{L} = \frac{1}{N} \sum_{j \in n_t} \sum_{i \in n_j} s_{Q_i} \cdot \| p_{Q_i} - p_{gt} \|_2 - \alpha \log s_{Q_i}$$

其中 $s_{Q_i}$ 为学习到的置信度权重，$\alpha \log s_{Q_i}$ 项防止模型输出过低的置信度。精细化后的坐标通过加权平均回归得到最终关键点位置（Figure 5）。

**消融证据**：去除高斯过程模块导致 1cm 准确度从 84.79% 降至 72.47%（Table 3），验证了坐标嵌入路径对多视图几何一致性的关键作用。基于学习置信度的轨迹选择策略进一步提升了细化精度。

### 3.4 几何捆绑调整

细化后的轨迹通过最小化鲁棒重投影误差进行全局优化：

$$E = \sum_j \sum_{x_k^* \in \mathcal{T}_j^*} \rho(\| \pi(\pmb{\xi}_i \cdot P_j, C_i) - x_k^* \|_2^2)$$

其中 $\mathcal{T}_j^*$ 为轨迹 $j$ 的所有观测，$\pi(\cdot)$ 为投影函数，$\rho(\cdot)$ 为鲁棒损失函数。重投影误差超过阈值 $\epsilon_f = 3$ 像素的匹配被作为外点剔除。整个细化过程迭代两次，实验表明继续增加迭代次数收益微小（Table 3, Table 7）。



## 实验与关键发现

### 核心瓶颈与实验动机

传统SfM管道依赖稀疏关键点检测与匹配，在弱纹理或重复纹理区域难以获得足够且可靠的匹配对，导致重建点云稀疏且精度受限。近期基于半稠密或稠密匹配的方法（如LoFTR+DFSfM）虽然提升了点云密度，但稠密匹配产生的特征轨迹往往断裂、不一致，难以直接输入现有SfM管道。DFSfM采用量化匹配来强制轨迹一致性，但量化过程不可避免地引入精度损失。Dense-SfM的核心实验动机正是验证：**通过高斯溅射（Gaussian Splatting）进行轨迹可见性评估与扩展，能否在不牺牲密度的前提下，同时提升重建精度和完整度？**

### 主要定量结果

#### 三维三角测量精度（ETH3D数据集）

Table 1报告了ETH3D数据集上的三维三角测量结果，以不同阈值下的准确度（Accuracy）和完整度（Completeness）为评估指标。Dense-SfM（RoMa+Ours）在1cm阈值下达到**84.79%的准确度**和**36.35%的完整度**（5cm阈值），相较于最强基线LoFTR+DFSfM分别提升**+4.41个百分点**和**+6.81个百分点**。这一结果验证了核心因果机制：高斯溅射轨迹扩展避免了量化带来的精度损失，同时多视图核化匹配模块利用更长的轨迹（更多观测信息）实现了更精确的关键点细化。


![[assets/figures/papers/paper_list_l48_Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching/figures/006_Table_1.jpg]]
*Table 1: Results of 3D Triangulation. Our method is compared with the baselines on the ETH3D [54] dataset using accuracy and completeness metrics with different thresholds*

值得注意的是，RoMa+DFSfM（量化匹配）在1cm准确度上仅达到80.38%，低于Dense-SfM的84.79%，直接证明了高斯溅射轨迹扩展相比量化方法的优势。此外，Dense-SfM在5cm完整度上的显著提升（36.35% vs. 29.54%）表明该方法能够恢复更多有效三维点，而非以牺牲密度换取精度。

#### 多视图相机位姿估计

Table 2报告了多视图相机位姿估计的AUC指标。Dense-SfM框架在ETH3D数据集上达到**82.63的AUC@5°**，优于所有检测器基方法、无检测器方法和稠密匹配基线。在Texture-Poor SfM和IMC 2021数据集上，Dense-SfM同样取得最优或次优结果，证明了该方法在弱纹理场景下的鲁棒性。


![[assets/figures/papers/paper_list_l48_Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching/figures/008_Table_2.jpg]]
*Table 2: Results of Multi-View Camera Pose Estimation. Our framework is compared with detector-based, detector-free and densematching baselines by the AUC of pose error at different thresholds. Bold and underline indicate the best and second-best results. Table 3. Ablation Studies. On the ETH3D dataset, we quantitatively evaluate the impact of design choice of matching and refinement module, and the number of iterations of refinement. The reported triangulation accuracy and completeness are averaged across all scenes*

### 消融实验：因果链路的逐环验证

Table 3系统性地拆解了Dense-SfM各设计选择的贡献，形成一条清晰的因果证据链：

#### 匹配策略消融

- **相互验证过滤**：启用相互验证后，1cm准确度提升，但完整度轻微下降。这符合预期——过滤不可靠匹配减少了噪声，但也丢弃了部分有效匹配。
- **高斯溅射轨迹扩展 vs. 量化匹配**：将高斯溅射轨迹扩展替换为DFSfM的量化方法（r=4）后，准确度和完整度均下降。这直接证明了高斯溅射在保持轨迹一致性的同时避免了量化误差，是精度提升的关键因素。

#### 细化模块消融

细化模块的消融揭示了多视图核化匹配架构中各组件的贡献：

- **仅使用Transformer**（去除高斯过程模块）：1cm准确度从84.79%降至72.47%，降幅达12.32个百分点。这是消融实验中**最显著的性能退化**，表明高斯过程提供的坐标嵌入信息对精确关键点定位至关重要。
- **仅使用高斯过程**（去除Transformer）：准确度同样大幅下降，说明Transformer的自注意力和交叉注意力机制在聚合多视图特征信息方面不可替代。
- **完整模型（Transformer+GP）**：整合两条路径后达到最高准确度和完整度，验证了双路径互补设计的有效性。
- **基于学习置信度的轨迹选择**：相较于统计方差选择策略，直接学习置信度分数并据此选择细化轨迹进一步提升了精度。该策略使模型能够自适应地评估每个轨迹的可靠性，而非依赖手工设计的启发式规则。

#### 细化迭代次数

Table 3和Table 7显示，两次迭代的细化能够获得最大收益，继续增加迭代次数收益微小。这表明Dense-SfM的细化过程在两次迭代后已接近收敛，额外的计算开销不具性价比。


![[assets/figures/papers/paper_list_l48_Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching/figures/012_Table_7.jpg]]
*Table 7: Ablation Study of Refinement Iterations. On the ETH3D dataset, we quantitatively evaluate the impact of the number of refinement iterations. The AUC of pose error and accuracy of 3D points at different thresholds are reported*

### 轨迹长度分析：机制验证

Table 6对比了不同匹配策略下的平均轨迹长度。量化匹配（DFSfM）的平均轨迹长度为2.11，而高斯溅射轨迹扩展将其提升至**4.97**，增幅超过一倍。更长的轨迹意味着多视图核化匹配模块能够利用更多视图的观测信息进行关键点细化，这是精度提升的直接因果机制。


![[assets/figures/papers/paper_list_l48_Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching/figures/011_Table_6.jpg]]
*Table 6: Comparison of average track length accompanied with matching strategies (Quantization, Track Extension via GS) to obtain consistent tracks*

### 与其他细化方法的对比

Table 4和Table 5分别展示了Dense-SfM细化模块与PixSfM、DFSfM细化方法在稀疏特征和半稠密匹配场景下的对比。结果表明，即使在相同的输入匹配条件下，Dense-SfM的多视图核化匹配模块仍一致优于现有细化方法，证明性能提升并非仅来自更好的初始匹配，而是细化架构本身的优势。


![[assets/figures/papers/paper_list_l48_Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching/figures/009_Table_4.jpg]]
*Table 4: Comparison of sparse local features accompanied with our refinement and PixSfM, DetectorFree-SfM (DFSfM). Our method is compared with the baselines on the ETH3D dataset using accuracy and completeness metrics with different thresholds*

![[assets/figures/papers/paper_list_l48_Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching/figures/010_Table_5.jpg]]
*Table 5: Comparison of LoFTR(semi-dense matching) accompanied with matching process for track consistency and track refinement. Our method is compared with the baselines on the ETH3D dataset using accuracy and completeness metrics with different thresholds*

### 失败模式与局限性

- **高光度变化与遮挡场景**：在IMC 2021数据集上（存在高度遮挡和外观变化），作者采用量化方法代替高斯溅射进行轨迹扩展，说明高斯溅射的可见性判别在此类场景下性能下降。这源于高斯溅射对光度一致性的依赖——当同一三维点在不同视图中外观差异过大时，透明度累积的可见性判断可能失效。
- **推理时间开销**：多视图核化匹配模块相较于DFSfM的细化模块增加了约22%的推理时间（Pipes场景上从35.3秒增至43.2秒），在实时应用中需要权衡精度与效率。
- **场景规模限制**：当前实验主要在中小规模数据集（ETH3D、Texture-Poor SfM）上进行，缺少在大规模无序图像集上的验证。高斯溅射的显存占用和优化时间可能成为扩展瓶颈。

### 开放问题

1. 如何在高动态光照或严重遮挡场景下提高高斯溅射可见性判别的鲁棒性？可能的路径包括引入外观不变特征或光照增强训练策略。
2. 是否可以实现端到端训练以联合优化高斯溅射和细化模块？当前管道中高斯溅射优化与细化模块训练是分离的，联合优化可能进一步提升精度。
3. 框架能否扩展以处理大规模无序图像集并保持精度？这需要考虑高斯溅射的扩展性和计算效率。

### 补充图表

![[assets/figures/papers/paper_list_l48_Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching/figures/013_Table_8.jpg]]
*Table 8: Quantitative Comparison in the LLFF Dataset, with 3 Training Views. Initialization with our method achieves the best performance in terms of rendering accuracy on all metrics*

![[assets/figures/papers/paper_list_l48_Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching/figures/003_Figure_3.jpg]]
*Figure 3: Bidirectional verification on two-view dense matching. The match result $p _ { b }$ from $\mathcal { M } _ { A B }$ is re-used as input to $\mathcal { M } _ { B A }$ to estimate $p _ { a ^ { \prime } }$ . We then compute the distance between $p _ { a }$ and $p _ { a ^ { \prime } }$ , where a smaller distance indicates higher reliability of the match between $p _ { a }$ and $p _ { b }$




## 定位与知识库关联

### 问题定位与核心创新

传统SfM管道依赖稀疏关键点检测（如SIFT）或半密集匹配（如**LoFTR**）建立跨视图对应关系。然而，稀疏检测在弱纹理区域可提取的特征点数量有限，导致重建点云稀疏且不完整；而密集匹配产生的对应关系虽然丰富，却因缺乏跨视图一致性而呈现“断裂轨迹”（fragmentary tracks）——同一三维点在不同视图对中对应到不同的二维坐标，直接输入现有SfM管道将破坏三角测量和捆绑调整的精度。

**DFSfM**（He et al.）通过量化匹配（quantized matching）将密集匹配转化为一致轨迹，但该操作引入量化误差，损害了三维点的精度和完整度。**Dense-SfM**的核心创新在于：用**高斯溅射（Gaussian Splatting）进行轨迹可见性评估与扩展**替代量化操作，从根本上避免了精度损失；同时提出**多视图核化匹配模块**（Transformer + 高斯过程），利用扩展后的长轨迹进行精细化，在不牺牲密度的情况下显著提升重建精度。

### 与基线方法的关系

#### 相对于DFSfM的改进

DFSfM是Dense-SfM最直接的前身与对比基线，二者共享“密集匹配→轨迹一致性→轨迹细化”的管道结构，但Dense-SfM在两个关键环节做出了结构性改进：

| 模块 | DFSfM | Dense-SfM | 改进机制 |
|------|-------|-----------|----------|
| 轨迹一致性 | 量化匹配（将连续坐标离散化到网格） | 高斯溅射可见性评估与投影 | 避免量化误差，保持亚像素精度 |
| 轨迹细化 | 基于Transformer的细化，用统计方差选择轨迹 | 多视图核化匹配（Transformer + 高斯过程），学习置信度分数 | 利用更多视图信息，直接回归置信度而非依赖启发式方差 |

消融实验（Table 3）量化了这一改进：将Dense-SfM的高斯溅射轨迹扩展替换为DFSfM的量化方法后，1cm准确度显著下降；去除高斯过程模块后，准确度从84.79%骤降至72.47%，验证了多视图核化匹配架构的关键作用。

#### 相对于其他SfM方法的定位

- **VGGSfM**：可微分端到端SfM方法，直接学习从图像到三维结构的映射。Dense-SfM保持了模块化管道设计，各组件可独立替换和消融分析，且在高精度三角测量任务上表现更优。
- **PixSfM (with SIFT)**：基于特征度量的关键点调整方法，依赖稀疏SIFT检测。Dense-SfM的密集匹配策略在弱纹理场景具有天然优势，且Table 4显示，将Dense-SfM的细化模块应用于稀疏特征时仍优于PixSfM。
- **LoFTR + DFSfM** 和 **RoMa + DFSfM**：作为密集/半密集匹配与DFSfM细化组合的基线，Dense-SfM在ETH3D三角测量上分别以+4.41和+6.81个百分点的优势超越（Table 1，1cm准确度与5cm完整度）。

### 适用边界与局限

1. **高光度变化与瞬时遮挡场景**：基于高斯溅射的轨迹扩展依赖光度一致性假设，在光照剧烈变化或存在瞬时遮挡的场景中，可见性判别准确度下降，导致轨迹扩展失效。在IMC 2021数据集上，作者因高度遮挡和外观变化而改用量化方法进行轨迹扩展，侧面印证了这一局限。

2. **计算开销**：多视图核化匹配模块相较于DFSfM的细化模块增加了约22%的推理时间（Pipes场景上从35.3秒增至43.2秒），在实时或资源受限的应用中需要权衡。

3. **规模验证不足**：当前实验主要针对中小规模场景（ETH3D、Texture-Poor SfM、IMC 2021），缺少在大规模无序图像集（如1DSfM、MegaDepth全量）上的验证。

4. **迭代收益递减**：轨迹细化迭代两次可获得最大收益，继续增加迭代次数收益微小（Table 3），表明当前细化策略在两次迭代后趋于饱和。

### 开放问题

- **鲁棒可见性判别**：如何在高动态光照或严重遮挡场景下提高高斯溅射的可见性判别鲁棒性？可能的思路包括引入外观不变特征或学习型可见性预测器。
- **端到端联合优化**：当前高斯溅射用于轨迹扩展、细化模块独立训练，是否可以实现端到端训练以联合优化二者，使高斯溅射的初始化直接服务于下游细化任务？
- **大规模扩展**：框架是否可以扩展以处理大规模无序图像集（数千至数万张图像）并保持精度？这涉及高斯溅射的内存效率和多视图核化匹配的计算可扩展性。
- **与NeRF/3DGS重建的协同**：Table 8显示Dense-SfM的初始化能提升高斯溅射的渲染质量，暗示SfM与可微分渲染之间存在更深层的协同潜力，值得进一步探索。



## 原文 PDF

![[paperPDFs/CVPR_2025/Dense_SfM_Structure_from_Motion_with_Dense_Consistent_Matching.pdf]]
