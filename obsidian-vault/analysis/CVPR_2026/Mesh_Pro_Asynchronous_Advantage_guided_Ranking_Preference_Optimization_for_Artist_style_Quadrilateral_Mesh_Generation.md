---
title: "Mesh-Pro: Asynchronous Advantage-guided Ranking Preference Optimization for Artist-style Quadrilateral Mesh Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Mesh_Pro_Asynchronous_Advantage_guided_Ranking_Preference_Optimization_for_Artist_style_Quadrilateral_Mesh_Generation.pdf
project_link: null
code_link: null
aliases:
- MPAAGRPOA
- Mesh-Pro
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过设计首个面向3D网格生成的异步在线RL框架，并结合优势引导排序偏好优化(ARPO)，在保持排序偏好优化快速稳定收敛优点的同时，显式引入优势函数加权，使模型能更高效地探索-利用复杂奖励分布，从而在训练效率和泛化能力之间取得更好的平衡。异步设计解耦了数据生成与策略更新，消除了同步RL的GPU空闲等待，使得在线RL在网格生成上变得切实可行。
primary_logic: 现有用于文本生成的异步RL框架（如AREAL、VeRL）与3D网格生成高度耦合，无法直接适用；网格生成的预训练模型能力有限且奖励分布（拓扑vs几何）复杂，导致显式奖励建模(GRPO)收敛缓慢、隐式方法(DPO)泛化差。ARPO利用基于排序的偏好优化实现快速稳定收敛，同时利用优势函数作为加权机制显式学习奖励分布以增强泛化，实现了比DPO和GRPO更优的训练效率-泛化折中。此外，新的对角感知tokenization推迟三角/四边形决策并强制全局最小顶点索引排序，显著降低了预测负担和结构破损率；基于射线投射的完整性奖励避免了对多部件模型的误判，比传统边界边奖励更鲁棒。
claims:
- 所提出的异步在线RL框架在大规模分布式设置下比同步RL训练速度快3.75倍以上。
- ARPO在训练效率和泛化性能上优于常用的DPO和GRPO，生成更高质量的四边形网格（表3）。
- Mesh-Pro在稠密网格和艺术家网格上均大幅超越此前最优方法，在破碎率(BR)、四边化率(QR)和用户评价(US)上取得SOTA（表1）。
- 新提出的对角感知tokenization结合异步ARPO后，显著降低了结构破损率，并提升了几何一致性和拓扑质量（表5）。
---

# Mesh-Pro: Asynchronous Advantage-guided Ranking Preference Optimization for Artist-style Quadrilateral Mesh Generation

> [!tip] 核心洞察
> 现有用于文本生成的异步RL框架（如AREAL、VeRL）与3D网格生成高度耦合，无法直接适用；网格生成的预训练模型能力有限且奖励分布（拓扑vs几何）复杂，导致显式奖励建模(GRPO)收敛缓慢、隐式方法(DPO)泛化差。ARPO利用基于排序的偏好优化实现快速稳定收敛，同时利用优势函数作为加权机制显式学习奖励分布以增强泛化，实现了比DPO和GRPO更优的训练效率-泛化折中。此外，新的对角感知tokenization推迟三角/四边形决策并强制全局最小顶点索引排序，显著降低了预测负担和结构破损率；基于射线投射的完整性奖励避免了对多部件模型的误判，比传统边界边奖励更鲁棒。

| 字段 | 内容 |
|------|------|
| 中文题名 | Mesh-Pro：面向艺术家风格四边形网格生成的异步优势引导排序偏好优化 |
| 英文题名 | Mesh-Pro: Asynchronous Advantage-guided Ranking Preference Optimization for Artist-style Quadrilateral Mesh Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00526) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Mesh-Pro (Asynchronous Advantage-guided Ranking Preference Optimization, ARPO) |
| Dataset | Dense Meshes, Artist Meshes |

> [!tip] 效果简介
> - Dense Meshes (from Hunyuan3D 2.5) 上，CD↓ 0.028 vs 0.059 (QuadGPT) (-52.5%)；BR↓ 22% vs 50% (QuadGPT) (-28个百分点)；QR↑ 81% vs 78% (QuadGPT) (+3个百分点)。
> - Artist Meshes (Toys4k) 上，CD↓ 0.038 vs 0.041 (Mesh-RFT) (-7.3%)；BR↓ 32% vs 38% (Mesh-RFT) (-6个百分点)；QR↑ 78% vs 76% (QuadGPT) (+2个百分点)。

## 概述

3D网格生成的后训练强化学习面临两个核心瓶颈。其一，现有方法或采用离线DPO，训练效率低、泛化能力不足；或尝试同步在线RL，但因网格token序列长度差异悬殊，导致严重GPU空闲与训练中断。其二，已有的混合三角-四边形网格tokenization（如QuadGPT）在早期强制提交面类型并采用非规范排序，产生几何伪影与结构缺陷，且仅靠监督学习会偏向简单三角面，难以生成艺术家级别的四边形拓扑。

Mesh-Pro针对上述瓶颈提出了三项关键创新。**对角感知tokenization**推迟三角/四边形决策至面序列末尾，并强制全局最小顶点索引排序，显著降低预测负担和结构破损率。**异步在线RL框架**解耦数据生成与策略更新，消除同步RL的GPU空闲等待，在大规模分布式设置下训练速度提升约3.75倍。**优势引导排序偏好优化（ARPO）**在保持排序偏好优化快速稳定收敛优点的同时，显式引入优势函数加权，使模型能更高效地探索-利用复杂奖励分布，实现了比DPO和GRPO更优的训练效率-泛化折中。

在奖励设计上，Mesh-Pro引入了基于射线投射的完整性奖励，避免对多部件模型的误判；同时设计了基于四边形环和四边形线的拓扑奖励，引导生成规则边流和清洁四边形布局。

实验表明，Mesh-Pro在稠密网格和艺术家网格上均大幅超越此前最优方法。在稠密网格上，相比QuadGPT，倒角距离（CD）降低52.5%，破碎率（BR）从50%降至22%，四边化率（QR）达81%。在艺术家网格上，相比Mesh-RFT，CD降低7.3%，BR从38%降至32%。消融实验证实了异步ARPO各组件、新tokenization以及奖励设计的有效性。Mesh-Pro生成的原生四边形主导拓扑在下游任务（UV展开、纹理绘制、动画）中展现出鲁棒性能。

## 背景与动机

### 3D网格生成：从三角面到艺术家级四边形拓扑

3D网格是计算机图形学、游戏开发与工业设计中最核心的几何表示形式之一。近年来，基于自回归Transformer的网格生成方法取得了显著进展，能够从点云、图像或文本等条件输入中重建出具有高几何保真度的三角网格。然而，**艺术家级别的网格远不止几何精度**——它要求网格具有规整的四边形拓扑结构、流畅的边流（edge flow），以及适合下游任务（如UV展开、纹理绘制、动画绑定）的清洁布局。四边形主导的网格因其规则的结构和良好的细分特性，成为行业标准，但其自动生成仍是一个极具挑战性的开放问题。

### 现有方法的瓶颈

当前3D网格生成的后训练优化面临两个相互交织的瓶颈：

**瓶颈一：RL训练范式的效率-泛化困境。** 现有方法主要采用离线RL（如DPO）进行偏好对齐。**DeepMesh**和**QuadGPT**等工作的实践表明，离线DPO虽然训练稳定，但受限于静态偏好数据，泛化能力不足——模型难以充分探索复杂奖励空间中的高质量解。理论上，同步在线RL可以通过持续的策略-环境交互克服这一问题，但在网格生成场景中，不同样本的token序列长度差异悬殊（从数百到数千不等），导致GPU利用率严重不均，产生大量空闲等待时间，甚至引发训练中断。因此，同步在线RL在3D网格生成中实际上不可行。

**瓶颈二：混合三角-四边形tokenization的结构缺陷。** 以**QuadGPT**为代表的现有tokenization方案存在两个关键设计缺陷：（1）使用leading token在序列早期强制声明面类型（三角或四边形），过早的硬决策增加了预测负担，容易产生几何伪影；（2）面内顶点排序仅保证第一个顶点低于第三个顶点，缺乏全局规范排序，导致结构破损率居高不下。此外，纯监督学习的预训练会自然偏向生成简单的三角面，难以自发涌现出艺术家级别的四边形拓扑。

### 本文动机

针对上述瓶颈，本文提出**Mesh-Pro**，一个面向艺术家风格四边形网格生成的异步优势引导排序偏好优化框架。核心动机来自三个关键洞察：

1. **异步解耦是可行在线RL的关键。** 将数据生成（rollout）与策略更新（trainer）分离为异步并行进程，可以消除同步RL的GPU空闲等待，使在线RL在网格生成上变得切实可行。这一设计借鉴了文本生成领域的异步RL框架（如AREAL、VeRL），但需要针对网格生成的截断训练、奖励分布特性进行专门适配。

2. **排序偏好优化与优势函数可以互补。** 基于排序的偏好优化（如DPO变体）具有快速稳定收敛的优点，但对奖励分布的显式建模不足；而显式优势最大化方法（如GRPO）在复杂奖励分布下收敛缓慢。将归一化优势函数作为加权机制引入排序偏好优化，可以在保持快速收敛的同时增强泛化能力，实现更好的效率-泛化折中。

3. **tokenization的决策时机决定生成质量。** 将对角感知融入tokenization设计——先生成三角形基面，再在序列末尾决定是否附加第四顶点形成四边形，并在第四顶点中编码对角方向——可以推迟面类型决策、降低预测负担。同时强制全局最小顶点索引排序，能够从根本上减少结构破损。

## 核心创新

Mesh-Pro 针对现有 3D 网格生成后训练 RL 的核心瓶颈，在三个维度上进行了系统性创新：**异步在线 RL 训练范式**、**优势引导排序偏好优化算法（ARPO）**，以及**对角感知的混合三角-四边形 tokenization**。三者协同，使模型在训练效率、泛化能力和拓扑质量上均取得显著突破。

### 2.1 从同步到异步：首个面向网格生成的在线 RL 框架

现有 3D 网格生成的后训练 RL 主要采用**离线 DPO**（如 **DeepMesh**、**QuadGPT**、**Mesh-RFT**），其训练效率低且泛化能力不足。理论上，在线 RL 能通过持续探索新策略来提升泛化性，但**同步在线 RL** 在网格生成中面临致命瓶颈：网格 token 序列长度差异悬殊（不同模型的 face 数变化极大），导致 GPU 间严重空闲等待与训练中断，使同步方案在工程上不可行。

Mesh-Pro 设计了**首个面向 3D 网格生成的异步在线 RL 框架**，将 Rollout Workers（数据生成）与 Trainer Workers（策略更新）完全解耦：
- **Rollout Workers** 使用最新策略持续生成截断训练样本，存入 Replay Buffer；
- **Trainer Workers** 从 Buffer 中独立采样进行策略更新，过期数据被即时丢弃；
- 通过 **Pre-Start 阶段**预先填充 Buffer 并定期同步权重复制，保证策略一致性。

该设计消除了同步 RL 的 GPU 空闲等待，使训练速度达到同步方案的 **3.75 倍以上**，首次让在线 RL 在网格生成上变得工程可行。消融实验（Table 2）证实，异步在线训练相比离线方案在 CD、HD、BR、QR 和用户评分（US）上全面领先，加入 Pre-Start 后训练稳定性与最终质量进一步提升。

### 2.2 ARPO：优势引导的排序偏好优化

在 RL 算法层面，现有方法陷入两难：**DPO** 基于隐式奖励建模，收敛快速稳定但泛化差；**GRPO** 显式最大化优势函数，理论上泛化更强，但在网格生成的复杂奖励分布（拓扑 vs 几何）下收敛缓慢甚至失效（Fig.7, Fig.14）。

**ARPO（Advantage-guided Ranking Preference Optimization）** 的核心洞察是：**用排序偏好优化实现快速稳定收敛，同时用显式优势函数作为加权机制来学习奖励分布，从而提升泛化能力**。

具体而言，ARPO 的优化目标为：

$$\mathcal{L}_{\mathrm{ARPO}} = -\mathbb{E}\Bigg[\sum_{i=1}^K A^{(i)} \log \frac{\exp\Big(\beta \log \frac{\pi_{\theta}(y_i|x)}{\pi_{\mathrm{ref}}(y_i|x)}\Big)}{\sum_{j=i}^K \exp\Big(\beta \log \frac{\pi_{\theta}(y_j|x)}{\pi_{\mathrm{ref}}(y_j|x)}\Big)}\Bigg]$$

其中归一化优势函数 $A^{(k)}$ 从组奖励中计算：

$$A^{(k)} = \frac{R^{(k)} - \min\{\{R^{(i)}\}_{i=1}^K\}}{\sum_{k=1}^K (R^{(k)} - \min\{\{R^{(i)}\}_{i=1}^K\}) + \epsilon}$$

这一设计使 ARPO 可视为在隐式奖励表征的“预测概率”下对优势函数的最大化。实验（Table 3）表明，Async ARPO 在 CD（0.028）、HD（0.090）、BR（22%）、QR（81%）和 US（2.4）上全面优于 Async DPO 和 Async GRPO。训练损失曲线（Fig.14）显示 ARPO 与 DPO 同样快速稳定收敛，而 GRPO 收敛缓慢。

### 2.3 对角感知 tokenization：推迟决策与规范排序

此前混合三角-四边形网格的 tokenization（如 **QuadGPT**）存在两个关键缺陷：
1. **过早提交面类型**：使用 leading token 在序列开头强制声明三角/四边，增加预测负担；
2. **非规范排序**：仅保证第一个顶点低于第三个顶点，导致几何伪影与结构缺陷。

Mesh-Pro 的**对角感知 tokenization** 从根本上解决了这些问题：
- **推迟决策**：先生成三角形基面（三个顶点），再决定是否附加第四顶点形成四边形。若为四边形，则在第四顶点中通过偏移量 $flag \times 2^{n_{bits}}$（$flag \in \{0,1,2\}$ 对应三种对角线方向）显式编码内部对角线；
- **规范排序**：所有面序列均从绝对最小索引顶点开始，消除排序歧义。

这一设计使模型在 token 级别就具备了几何结构意识。消融实验（Table 5）显示，仅替换 tokenization（不应用 ARPO），BR 已从 38% 降至 24%；叠加异步 ARPO 后，BR 进一步降至 22%，QR 达 81%，US 达 2.1，远超先前 tokenization 方法。

### 2.4 鲁棒的完整性奖励与拓扑奖励

奖励函数设计是 RL 后训练的另一关键。Mesh-Pro 引入两个创新奖励组件：

**基于射线投射的完整性奖励**：从六个主轴方向投射射线，分析命中面的法向一致性以识别“坏面”（bad faces）；若坏面数 $N_{bf}$ 超过阈值 $\theta_{ray}$，奖励直接置零。相比传统的边界边启发式奖励，射线方法能有效避免对多部件模型的误判（Fig.11），因为部件间的自然边界边在边界边奖励下会被错误惩罚。

**基于四边形环/线的拓扑奖励**：$R_{topo} = w_{qr} \cdot N_{qr} + N_{ql}^2$，其中 $N_{qr}$ 为闭合四边形环（Quad Rings）数，$N_{ql}$ 为开放四边形线（Quad Lines）数。该奖励鼓励形成规则边流和清洁四边形布局，推动生成网格向艺术家风格拓扑靠拢。

消融实验（Fig.7）证实：移除射线奖励导致网格破碎率大幅上升；移除拓扑奖励则使输出质量显著下降，远离艺术家水准。

## 整体框架

Mesh-Pro 的整体 pipeline 围绕“预训练 + 异步在线 RL 后训练”两阶段范式构建，其核心设计目标是生成兼具几何保真度与艺术家级四边形拓扑的混合三角-四边形网格。图 2 给出了架构总览，清晰展示了从输入到输出的完整数据流与模块关系。

**输入与特征提取。** 系统以稠密点云（40,960 点）作为统一输入表示，无论目标网格来源于稠密重建还是艺术家手工建模。点云编码器基于 **Michelangelo** 构建，负责将原始点云压缩为几何条件特征，供后续解码器使用。

**自回归网格解码。** 条件特征被送入一个 1.1B 参数的 **Hourglass Transformer** 解码器（图 2 中部）。该解码器采用逐层压缩策略（压缩因子分别为 4 和 3），在瓶颈层捕获全局结构模式，同时保留局部几何细节。解码器以自回归方式逐 token 生成网格序列，预训练目标为标准负对数似然损失：

$$\mathcal{L}_{\mathrm{pretrain}} = -\sum_{t=1}^{L} \log p_{\theta}(\mathbf{s}_t | \mathbf{s}_{<t})$$

预训练阶段使用约 130 万四边形主导网格进行监督学习，使模型初步具备从点云重建混合三角-四边形网格的能力。

**对角感知 Tokenization。** 预训练与推理中的 token 序列由新提出的对角感知 tokenization 方案（图 3）定义。与先前方法（如 **QuadGPT**）不同，该方案推迟了三角/四边形的类型决策：每个面先生成三角形基面（三个顶点），再在序列末尾决定是否附加第四顶点以形成四边形。第四顶点中通过偏移量 `flag × 2^{n_bits}`（flag ∈ {0,1,2}）显式编码内部对角线方向。所有面序列均从绝对最小索引顶点开始，实现了全局规范排序。这一设计显著降低了预测负担与结构破损率。

**异步在线 RL 后训练。** 预训练模型随后进入异步在线 RL 框架（图 4）进行后训练。该框架是首个面向 3D 网格生成的异步在线 RL 系统，核心创新在于将数据生成（Rollout Workers）与策略更新（Trainer Workers）解耦为异步并行进程：

- **Rollout Workers** 使用当前策略持续生成截断训练样本，并存入 replay buffer；
- **Trainer Workers** 从 buffer 中采样数据，计算 ARPO 损失并更新策略参数；
- 过时的 rollout 数据被及时丢弃，通过 Pre-Start 阶段和定期权重复制保持策略一致性。

这一异步设计消除了同步 RL 中因网格 token 序列长度差异悬殊导致的 GPU 空闲等待，实测训练速度比同步 RL 快约 **3.75 倍**。

**ARPO 损失与奖励驱动。** 策略更新采用 **Advantage-guided Ranking Preference Optimization (ARPO)** 算法。对于每组 K 个截断样本，先计算归一化优势函数：

$$A^{(k)} = \frac{R^{(k)} - \min\{\{R^{(i)}\}_{i=1}^K\}}{\sum_{k=1}^K (R^{(k)} - \min\{\{R^{(i)}\}_{i=1}^K\}) + \epsilon}$$

再通过优势加权的排序偏好优化损失更新策略：

$$\mathcal{L}_{\mathrm{t-ARPO}} = -\mathbb{E}_{M_t}\left[\sum_{i=1}^K A_t^{(i)} \log \frac{\exp\left(\mathcal{R}_{i|m:m+w}\right)}{\sum_{j=i}^K \exp\left(\mathcal{R}_{j|m:m+w}\right)}\right]$$

其中 $\mathcal{R}_{i|m:m+w} = \beta \log \frac{\pi_{\theta}(y_{i|m:m+w} \mid P)}{\pi_{\mathrm{ref}}(y_{i|m:m+w} \mid P)}$ 为策略与参考模型的截断对数概率比。ARPO 在保持排序偏好优化快速稳定收敛优势的同时，通过显式优势加权增强了模型对复杂奖励分布的探索-利用能力。

**奖励函数。** 每个生成网格的奖励由几何完整性与拓扑质量共同决定：

$$R(M_t) = \begin{cases} w_{\mathrm{qr}} \cdot N_{\mathrm{qr}} + N_{\mathrm{ql}}^2 & \text{if } N_{\mathrm{bf}} < \theta_{ray} \text{ and } D_{\mathrm{hd}} < \theta_{hd}, \\ 0 & \text{otherwise.} \end{cases}$$

- **射线投射完整性检查**：从六个主轴方向投射射线，分析命中面法向一致性以识别“坏面”；若坏面数 $N_{\mathrm{bf}}$ 超过阈值 $\theta_{ray}$，奖励直接置零。该机制有效避免了对多部件模型的误判（图 11）。
- **拓扑奖励**：遍历四边形面形成的边流，识别闭合的 Quad Rings（$N_{\mathrm{qr}}$）和开放的 Quad Lines（$N_{\mathrm{ql}}$），鼓励规则边流和清洁四边形布局。

**输出。** 最终生成的混合三角-四边形网格平均面数约 8k（图 13），在几何一致性（CD、HD）、结构完整性（BR）、四边化率（QR）和用户主观评分（US）上均达到 SOTA 水平。

### 补充图表

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/002_Figure_2.jpg]]
*Figure 2: Architecture Overview. Mesh-Pro begins by sampling point clouds from the input dense and artist meshes. The features from the point cloud encoder are then passed to an auto-regressive Hourglass Transformer [18] for mesh decoding. This decoder is trained with truncation to output triangle-quad tokens. The pre-training objective is to reconstruct the input mesh. Subsequently, asynchronous ARPO is used for RL post-training to generate high-quality, well-structured meshes, guided by ray and topological rewards*

## 核心模块与公式推导

### 对角感知网格Tokenization

Mesh-Pro提出了一种新颖的对角感知（Diagonal-Aware）网格tokenization方案，用于统一表达混合三角-四边形网格。该方案的核心设计原则是**推迟面类型决策**：先生成三角形基面（三个顶点），再决定是否附加第四顶点以形成四边形。若为三角形，则使用填充token补齐；若为四边形，则在第四顶点中通过偏移量显式编码内部对角方向。

具体而言，四边形内部对角通过 `flag × 2^{n_bits}` 的偏移量编码到第四顶点索引中，其中 `flag ∈ {0, 1, 2}` 分别指定三种可能的对角方向。所有面序列均从绝对最小索引顶点开始，确保规范排序。这一设计解决了先前方法（如QuadGPT）使用前置token强制提前提交面类型、以及非规范排序所导致的几何伪影和结构缺陷问题。

顶点坐标的量化方式如下：

$$\tilde{\mathbf{v}}_i = \left\lfloor \frac{\left(\mathbf{v}_i - \mathbf{v}_{\operatorname*{min}}\right)}{\left(\mathbf{v}_{\operatorname*{max}} - \mathbf{v}_{\operatorname*{min}}\right)} \cdot 2^n \right\rceil \in [0, 2^n - 1]^3$$

该公式将顶点坐标归一化至 $[0, 2^n-1]^3$ 的 $n$ 位量化整数空间，为后续自回归建模提供离散token序列。

### Hourglass Transformer解码器与预训练

Mesh-Pro采用Hourglass Transformer作为自回归解码器（1.1B参数），通过逐层压缩（因子4和3）在瓶颈层捕获全局模式，同时保留局部细节。解码器以点云编码器（基于Michelangelo）提取的几何特征为条件输入，逐token生成三角-四边形混合序列。

预训练阶段使用标准的自回归负对数似然损失：

$$\mathcal{L}_{\mathrm{pretrain}} = -\sum_{t=1}^{L} \log p_{\theta}(\mathbf{s}_t | \mathbf{s}_{<t})$$

其中 $L$ 为token序列长度，$\mathbf{s}_t$ 为第 $t$ 个token。

### 异步在线RL框架

为解决同步在线RL在网格生成中因序列长度差异悬殊导致的严重GPU空闲与训练中断问题，Mesh-Pro设计了首个面向3D网格生成的异步在线RL框架。该框架解耦数据生成与策略更新：Rollout workers持续使用最新策略生成训练样本并存入replay buffer，Trainer workers从中采样进行策略更新，过期rollout数据被及时丢弃。

为保证训练稳定性，框架引入**Pre-Start阶段**：在正式异步训练前，先用预训练模型填充replay buffer至一定容量。策略更新频率受以下约束：

$$\left\{ \begin{array}{c} \sigma_{min} \leq \frac{N_2 * T * B}{S_2} = \frac{N_1 * T * B}{S_1} \leq \sigma_{max}, \\ S_1 > S_2 \geq \sigma. \end{array} \right.$$

该约束限定训练步数乘以batch size与replay buffer大小的比值在 $[\sigma_{min}, \sigma_{max}]$ 范围内（推荐 $\sigma_{min}=8, \sigma_{max}=64$），确保模型能充分学习当前buffer中的奖励分布。

### 优势引导排序偏好优化（ARPO）

ARPO是Mesh-Pro的核心RL算法，旨在实现训练效率与泛化能力的最优折中。其理论基础建立在KL正则化隐式奖励函数之上：

$$r(x, y) = \beta \log \frac{\pi_{\theta}(y \mid x)}{\pi_{\mathrm{ref}}(y \mid x)} + \beta \log Z(x)$$

其中 $\beta$ 控制偏离参考策略 $\pi_{\mathrm{ref}}$ 的程度，$Z(x)$ 为配分函数。

基于Plackett-Luce排序模型，给定 $K$ 个候选样本的排序 $\omega$ 的概率为：

$$p(\omega \mid \{y_i\}_{i=1}^K) = \prod_{k=1}^K \frac{\exp\bigl(\beta \log \frac{\pi_{\theta}(y_{\omega(k)}|x)}{\pi_{\mathrm{ref}}(y_{\omega(k)}|x)}\bigr)}{\sum_{j=k}^K \exp\bigl(\beta \log \frac{\pi_{\theta}(y_{\omega(j)}|x)}{\pi_{\mathrm{ref}}(y_{\omega(j)}|x)}\bigr)}$$

ARPO的关键创新在于引入**归一化优势函数**作为排序偏好的加权系数。优势函数从组奖励中计算：

$$A^{(k)} = \frac{R^{(k)} - \min\{\{R^{(i)}\}_{i=1}^K\}}{\sum_{k=1}^K (R^{(k)} - \min\{\{R^{(i)}\}_{i=1}^K\}) + \epsilon}$$

最终的ARPO损失为优势加权的负排序偏好：

$$\mathcal{L}_{\mathrm{ARPO}} = -\mathbb{E}\Bigg[\sum_{i=1}^K A^{(i)} \log \frac{\exp\Big(\beta \log \frac{\pi_{\theta}(y_i|x)}{\pi_{\mathrm{ref}}(y_i|x)}\Big)}{\sum_{j=i}^K \exp\Big(\beta \log \frac{\pi_{\theta}(y_j|x)}{\pi_{\mathrm{ref}}(y_j|x)}\Big)}\Bigg]$$

ARPO可理解为在隐式奖励表示的“预测概率”下对优势函数的显式最大化：保留了排序偏好优化快速稳定收敛的优势，同时通过优势加权显式学习复杂奖励分布以增强泛化能力。

针对网格生成的截断训练特性，ARPO进一步扩展为截断版本：

$$\mathcal{L}_{\mathrm{t-ARPO}} = -\mathbb{E}_{M_t}\left[\sum_{i=1}^K A_t^{(i)} \log \frac{\exp\left(\mathcal{R}_{i|m:m+w}\right)}{\sum_{j=i}^K \exp\left(\mathcal{R}_{j|m:m+w}\right)}\right]$$

其中 $\mathcal{R}_{i|m:m+w} = \beta \log \frac{\pi_{\theta}(y_{i|m:m+w} \mid P)}{\pi_{\mathrm{ref}}(y_{i|m:m+w} \mid P)}$ 为截断窗口内策略与参考模型的概率比，教导RL策略做出导致全局优越拓扑的局部决策。

### 奖励函数设计

Mesh-Pro的综合奖励函数融合几何完整性与拓扑质量两个维度：

$$R(M_t) = \left\{\begin{array}{ll} w_{\mathrm{qr}} \cdot N_{\mathrm{qr}} + N_{\mathrm{ql}}^2 & \mathrm{if~} N_{\mathrm{bf}} < \theta_{ray} \mathrm{~and~} D_{\mathrm{hd}} < \theta_{hd}, \\ 0 & \mathrm{otherwise.} \end{array}\right.$$

- **射线投射完整性检查**（$N_{\mathrm{bf}}$）：从六个主轴方向投射射线，分析命中面法向一致性以识别“坏面”；若坏面数 $N_{\mathrm{bf}}$ 超过阈值 $\theta_{ray}$，奖励直接置零。相比传统边界边奖励，该方法有效避免了对多部件模型的误判。
- **拓扑奖励**：$N_{\mathrm{qr}}$ 为四边形环（Quad Rings）数量，$N_{\mathrm{ql}}$ 为四边形线（Quad Lines）数量，$w_{\mathrm{qr}}$ 为权重系数。通过鼓励闭合环和开放线的形成，引导模型生成规则的边流和清洁的四边形布局。
- **Hausdorff距离门控**：$D_{\mathrm{hd}} < \theta_{hd}$ 确保生成网格与输入点云的几何一致性。

### 补充图表

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/003_Figure_3.jpg]]
*Figure 3: Diagonal-Aware Mesh Tokenization. “P” denotes vertex tokens. The minimum vertex always appears first in each face (i.e., lower coordinates). Triangles use padding tokens*

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/004_Figure_4.jpg]]
*Figure 4: Asynchronous Online RL Framework*

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/014_Figure_10.jpg]]
*Figure 10: Illustration of ray casting integrity check. When a ray is cast toward the mesh from a given direction, it may pass through the broken region surrounding a “bad*

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/016_Figure_12.jpg]]
*Figure 12: Illustration of quad rings and quad lines*

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/018_Figure_14.jpg]]
*Figure 14: Training loss curves for DPO, GRPO, and ARPO*

## 实验与分析

### 主实验结果

Mesh-Pro在稠密网格（来自Hunyuan3D 2.5）和艺术家网格（Toys4k）两个基准上均取得了全面的SOTA性能，如表1所示。在稠密网格上，Mesh-Pro的倒角距离（CD）达到0.028，较此前最佳方法**QuadGPT**的0.059降低了52.5%；破碎率（BR）从50%骤降至22%，降幅达28个百分点；四边化率（QR）提升至81%。在更具挑战性的艺术家网格上，Mesh-Pro同样表现最优：CD为0.038（对比**Mesh-RFT**的0.041），BR为32%（对比Mesh-RFT的38%），QR为78%。用户主观评分（US）在两个基准上分别达到5.2和4.9，显著领先所有基线方法，表明生成网格的拓扑质量已接近艺术家水平。

值得注意的是，公平性处理上，对于仅输出三角网格的基线方法，统一使用了鲁棒的三角形-四边形转换算法进行后处理，确保对比的公正性。

### 异步在线ARPO消融实验

表2系统地消融了异步在线ARPO的各关键组件。以预训练模型（标记为“*”）为基线，逐步引入Group采样、在线训练、Pre-Start阶段和显式优势引导：

- **在线 vs 离线**：异步在线ARPO在CD（0.028 vs 0.031）、HD（0.090 vs 0.095）和QR（81% vs 80%）上均优于离线ARPO，验证了在线探索对网格生成质量的关键作用。
- **Pre-Start阶段**：加入Pre-Start后训练更加稳定，US从2.4提升至3.5，表明策略初始化的稳定性对最终拓扑质量有显著影响。
- **显式优势引导**：引入优势加权后，模型泛化能力明显增强，US从2.4提升至2.9，且未带来收敛速度的负面影响。完整配置（Group 4 + Advantage + Online + Pre-Start）取得最优US 3.5，证实了各组件的协同效应。

### ARPO与DPO、GRPO的对比

表3和图7、图8揭示了ARPO相较于主流RL算法的核心优势：

- **对比DPO**：异步ARPO在泛化性能上显著优于异步DPO。DPO作为隐式奖励建模方法，在复杂的网格奖励分布（拓扑+几何）下泛化能力不足，而ARPO通过显式优势加权有效学习了奖励分布的结构信息。
- **对比GRPO**：GRPO作为显式优势最大化方法，在网格生成任务上收敛缓慢且不稳定（图14训练损失曲线证实了这一点）。ARPO继承了排序偏好优化的快速稳定收敛特性，同时利用优势函数显式建模奖励分布，实现了训练效率与泛化能力的最优折中。定量上，Async ARPO的CD为0.028、BR为22%、QR为81%、US为2.4，全面优于Async DPO和Async GRPO。

### 奖励函数消融

图7的奖励消融曲线揭示了两个奖励组件的不可替代性：

- **移除射线奖励 R_ray**：导致网格破碎率大幅上升。基于射线投射的完整性检查通过多方向投射射线并分析命中面法向一致性来识别“坏面”，有效避免了传统边界边奖励对多部件模型的误判问题（图11）。当坏面数超过阈值θ_ray时奖励直接置零，这一硬约束机制是维持几何完整性的关键。
- **移除拓扑奖励 R_topo**：生成网格的拓扑质量显著下降，远离艺术家水准。R_topo通过计算四边形环（Quad Rings）和四边形线（Quad Lines）的加权和（$R_{topo} = w_{qr} \cdot N_{qr} + N_{ql}^2$）来鼓励规则边流和清洁四边形布局，是引导模型生成艺术家风格拓扑的核心驱动力。

### Tokenization对比

表5对比了本文对角感知tokenization与先前方法（如**QuadGPT**的tokenization）的效果。在不应用ARPO时，本文tokenization已将BR从38%降至24%，验证了推迟三角/四边形决策并强制全局最小顶点索引排序的设计有效性。叠加异步ARPO后，优势进一步放大：CD从0.071降至0.028，HD从0.160降至0.090，BR从46%降至22%，US从1.8提升至2.1。这表明更好的tokenization为RL后训练提供了更优的探索空间。

### 数据规模扩展性

表4展示了异步ARPO的数据扩展潜力。将训练数据从400个网格增至1000个时，BR从22.35%持续降至21.83%，其他指标也呈稳定改善趋势，表明该方法具备良好的数据扩展性，尚未达到性能瓶颈。

### 破碎率敏感性分析

表6对不同破碎判定阈值θ_succ的敏感性分析证实，Mesh-Pro的低破碎率并非阈值选择造成的假象——在合理的阈值范围内，BR始终保持在较低水平，验证了结果的稳健性。

### 训练效率

在异步框架的效率方面，论文报告所提出的异步在线RL在大规模分布式设置下比同步RL训练速度快约3.75倍。这一加速源于Rollout workers与Trainer workers的解耦设计，消除了同步RL中因网格token序列长度差异悬殊导致的严重GPU空闲等待。

### 失败模式与局限性

尽管整体性能优异，实验中也暴露出若干局限：

1. **组大小受限**：ARPO的组大小受限于GPU显存，目前无法显著扩大，限制了优势估计的精度和探索效率。
2. **面数控制缺失**：Mesh-Pro尚不支持对生成网格的面数进行细粒度控制，生成网格的平均面数约8k（图13），但无法按需调整。
3. **奖励攻击风险**：基于规则的拓扑边流奖励R_topo在异步ARPO训练后期可能导致奖励攻击（reward hacking），例如产生不自然的关节区域边流。这提示未来需要训练基于人类反馈的奖励模型来进一步提升艺术家风格网格生成的性能上限。

### 下游应用验证

图17展示了Mesh-Pro生成的高质量原生四边形主导拓扑在下游任务中的鲁棒表现，包括UV展开、纹理绘制和动画，证实了其在实际生产管线中的应用价值。与闭源商业方法（Tripo、Hunyuan3D）的定性对比（图16）进一步表明，Mesh-Pro在几何一致性、细节丰富度和拓扑边流质量上均展现出优势。

### 补充图表

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison on Dense and Artist Meshes*

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/012_Table_3.jpg]]
*Table 3: Quantitative comparison of ARPO with DPO and GRPO*

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/008_Table_2.jpg]]
*Table 2: Effectiveness analysis of each component of asynchronous ARPO. “*” denotes the pretrained model*

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/010_Figure_7.jpg]]
*Figure 7: Performance curves of asynchronous RL methods and reward function over training steps*

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/015_Figure_11.jpg]]
*Figure 11: Boundary edge–based reward leads to misjudgments of the multi-component object. When a mesh consists of multiple components, boundary edges (highlighted by the green line) often appear between components. However, this mesh is still a good output and should be encouraged. In Mesh-Pro, the ray-based reward does not suffer from this issue*

![[assets/figures/papers/paper_list_l2204_https_arxiv_org_abs_2603_00526/figures/017_Figure_13.jpg]]
*Figure 13: Distribution of face count (consisting of a mixture of triangles and quadrilaterals) in Mesh-Pro predictions. Point clouds are sampled from dense meshes and artist meshes. The average face count is approximately 8k*

## 方法谱系与知识库定位

### 1. 问题定位与基线对比

Mesh-Pro 瞄准的核心问题是**艺术家风格四边形主导网格的自动生成**，其方法谱系可沿两条轴展开：**网格tokenization** 和 **3D生成的后训练强化学习**。

#### 1.1 网格Tokenization谱系

在tokenization层面，Mesh-Pro 的直接前驱是 **QuadGPT**（原生四边形生成+RL对齐），其采用“leading token”提前声明面类型（三角/四边形）并在顶点排序上仅保证第一个顶点低于第三个顶点。这种非规范排序和过早的面类型决策导致了两个关键缺陷：**几何伪影**和**结构破损**。实验证据表明，在不应用ARPO的条件下，QuadGPT的tokenization方案破碎率（BR）高达38%，而Mesh-Pro的对角感知tokenization将BR降至24%（Table 5）。

Mesh-Pro 的对角感知tokenization通过两个核心设计解决了上述问题：
- **推迟面类型决策**：先生成三角形基面（三个顶点），再决定是否附加第四顶点形成四边形，将三角/四边形的决策推迟到序列的最后位置，降低了自回归预测的负担。
- **规范排序与对角编码**：所有面序列均从绝对最小索引顶点开始，实现全局一致排序；对于四边形，内部对角线通过偏移量 `flag × 2^{n_bits}`（`flag ∈ {0,1,2}`）显式编码于第四顶点索引中，确保了对角方向的唯一确定性。

这一tokenization方案与 **BPT**（几何序列tokenizer）等方法形成对比，后者缺乏对混合三角-四边形面的专门处理，难以生成艺术家级别的四边形拓扑。

#### 1.2 3D网格生成的后训练RL谱系

在后训练强化学习层面，现有方法主要分为两条路线：

**离线DPO路线**：包括 **DeepMesh**、**QuadGPT** 和 **Mesh-RFT**。其中 DeepMesh 率先将离线DPO引入网格生成后训练，QuadGPT 进一步将其与原生四边形生成结合，Mesh-RFT 则引入了规则奖励机制。这些方法的共同局限在于：离线训练效率低、泛化能力不足，且无法在训练过程中动态探索新的奖励分布。实验表明，异步在线ARPO在稠密网格上的Chamfer距离（CD）为0.028，而QuadGPT为0.059，破碎率从50%降至22%（Table 1）。

**同步在线RL路线**：理论上存在但在网格生成中**几乎不可行**——由于网格token序列长度差异悬殊（从数百到数千tokens不等），同步RL会导致严重的GPU空闲等待和训练中断。Mesh-Pro 的异步在线RL框架通过解耦数据生成（Rollout workers）与策略更新（Trainer workers），消除了这一瓶颈，在大规模分布式设置下训练速度比同步RL快**3.75倍以上**，使得在线RL在网格生成上首次变得切实可行。

### 2. RL算法定位：ARPO vs DPO vs GRPO

ARPO 在RL算法谱系中占据了一个独特位置，介于隐式奖励建模（DPO）和显式优势最大化（GRPO）之间：

- **DPO**（隐式奖励）：通过排序偏好优化实现快速稳定收敛，但缺乏对奖励分布幅度的显式建模，导致泛化能力受限。在3D网格生成中，由于预训练模型能力有限且奖励分布（拓扑vs几何）复杂，这一缺陷尤为突出。
- **GRPO**（显式优势）：通过优势函数最大化显式学习奖励分布，理论上泛化能力更强，但在网格生成的复杂奖励分布下**收敛缓慢**（Fig.14训练损失曲线证实），且同步实现困难。
- **ARPO**（本文提出）：在保持排序偏好优化快速稳定收敛优点的同时，显式引入归一化优势函数 $A^{(k)}$ 作为加权机制，实现了**训练效率与泛化能力之间的更优折中**。其核心损失函数为：

$$\mathcal{L}_{\mathrm{ARPO}} = -\mathbb{E}\left[\sum_{i=1}^K A^{(i)} \log \frac{\exp\left(\beta \log \frac{\pi_{\theta}(y_i|x)}{\pi_{\mathrm{ref}}(y_i|x)}\right)}{\sum_{j=i}^K \exp\left(\beta \log \frac{\pi_{\theta}(y_j|x)}{\pi_{\mathrm{ref}}(y_j|x)}\right)}\right]$$

定量对比（Table 3）证实：异步ARPO在CD 0.028、HD 0.090、BR 22%、QR 81%上全面优于异步DPO和异步GRPO，且用户主观评分（US）达到2.4，显著高于对比方法。

### 3. 与异步RL框架的关系

Mesh-Pro 的异步在线RL框架并非孤立设计，而是与现有文本生成领域的异步RL框架（如 **AREAL**、**VeRL**）存在方法学关联。然而，这些框架与3D网格生成**高度耦合**，无法直接适用，原因在于：
- 网格生成的token序列长度差异悬殊，需要特殊的截断训练策略。
- 预训练模型能力有限，需要Pre-Start阶段稳定训练初期。
- 奖励函数涉及几何完整性（射线投射）和拓扑质量（四边形环/线）的多维度评估，与文本奖励有本质区别。

Mesh-Pro 的框架设计通过**策略更新频率约束**（Eq.3）确保模型能充分学习当前replay buffer中的奖励分布，并通过定期权重复制和过期数据丢弃保持策略一致性。

### 4. 适用边界与局限

#### 4.1 适用边界

Mesh-Pro 的方法设计适用于以下场景：
- **输入条件**：稠密点云（40960点）作为几何条件输入，通过基于Michelangelo的点云编码器提取特征。
- **输出类型**：混合三角-四边形主导网格，平均面数约8k（Fig.13），适用于艺术家风格建模、游戏资产、动画制作等需要高质量拓扑的下游任务（Fig.17展示了UV展开、纹理绘制和动画表现）。
- **训练数据**：预训练需大规模四边形主导网格（本文使用130万），后训练需高质量多样化网格（本文使用500个稠密网格+200个艺术家网格）。

#### 4.2 已知局限

1. **组大小受限于GPU显存**：ARPO的组大小 $K$ 目前无法显著扩大，限制了优势函数估计的精度和探索效率。未来需探索部分参数微调（如LoRA）等方案以在显存约束下扩大组大小。

2. **面数控制缺失**：Mesh-Pro 尚不支持对生成网格的面数进行细粒度控制。截断网格解码器目前缺乏多级面数控制机制，限制了在需要特定分辨率网格的下游任务中的灵活性。

3. **拓扑奖励的奖励攻击风险**：基于规则的拓扑边流奖励 $R_{\mathrm{topo}} = w_{\mathrm{qr}} \cdot N_{\mathrm{qr}} + N_{\mathrm{ql}}^2$ 在异步ARPO训练后期可能导致**奖励攻击（reward hacking）**，例如产生不自然的关节区域边流以最大化四边形环/线计数。这是规则奖励的固有局限，需训练基于人类反馈的奖励模型以进一步提升艺术家风格网格生成的性能上限。

4. **对预训练质量的依赖**：ARPO的后训练效果受限于预训练模型的基础能力。在预训练数据质量不足或分布偏移较大的情况下，RL后训练的改进幅度可能受限。

### 5. 开放问题

1. **组大小扩展**：在GPU显存约束下，如何扩大ARPO的组大小以进一步提升性能？部分参数微调、梯度累积或分布式组采样是否可行？

2. **多级面数控制**：如何在截断网格解码器中实现多级面数控制，以更好地适应从移动端到影视级的多样化下游任务需求？

3. **人类反馈奖励模型**：如何构建并训练基于人类反馈的奖励模型，以避免规则奖励导致的奖励攻击，并持续逼近艺术家级拓扑质量？这需要收集大规模的艺术家偏好标注数据。

4. **框架泛化性**：异步ARPO框架能否泛化到其他自回归生成任务（如点云生成、3D场景生成、CAD模型生成），并取得类似的大幅提升？其核心的“截断训练+优势加权排序优化”设计是否具有任务无关性？

5. **数据扩展的边际效应**：Table 4显示数据从400增至1000时BR从22.35%降至21.83%，提升幅度较小。针对更大规模（如500万+）高质量四边形网格数据的预训练和RL扩展，性能提升的边际效应如何？是否存在数据效率的瓶颈？

6. **与闭源商业方法的差距**：Fig.16的定性对比显示Mesh-Pro在几何一致性、细节丰富度和拓扑质量上优于闭源商业方法（Tripo、Hunyuan3D），但缺乏定量指标。如何在标准化benchmark上系统评估与商业方法的差距？

## 原文 PDF

![[paperPDFs/CVPR_2026/Mesh_Pro_Asynchronous_Advantage_guided_Ranking_Preference_Optimization_for_Artist_style_Quadrilateral_Mesh_Generation.pdf]]