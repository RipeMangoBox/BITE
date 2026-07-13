---
title: Capturing Closely Interacted Two-Person Motions with Reaction Priors
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction_Priors.pdf
project_link: https://neteasegameai.github.io/Dual-Human/
code_link: null
aliases:
- RPBTPM
- CCITPMRP
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过学习反应先验（基于动作VAE和可逆神经网络建模的交互条件概率分布），并将该先验作为训练正则化与测试时优化指导注入姿态估计流程，从而矫正遮挡下的姿态预测。
primary_logic: 紧密交互动作通常发生在特定情境下（如握手、拥抱），这些情境构成强语义先验，可用于推断被遮挡关节的姿态；利用交互的对称性和双向条件概率建模可以有效去模糊化遮挡，使得即使从稀疏观测中也能恢复合理的两人运动。
claims:
- 提出的方法在 Dual-Human 数据集上的 MPJPE 为 63.4，显著优于先前方法。
- 反应先验相比 BUDDI 的 proxemics 先验在 MPJPE 上提升明显（64.1 vs 67.3）。
- 消融实验证实去除运动VAE或INN都会导致姿态估计误差上升，证明反应先验各组件不可或缺。
- Dual-Human 上 MPJPE = 63.4
---

# Capturing Closely Interacted Two-Person Motions with Reaction Priors

> [!tip] 核心洞察
> 紧密交互动作通常发生在特定情境下（如握手、拥抱），这些情境构成强语义先验，可用于推断被遮挡关节的姿态；利用交互的对称性和双向条件概率建模可以有效去模糊化遮挡，使得即使从稀疏观测中也能恢复合理的两人运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 使用反应先验捕获紧密交互的两人运动 |
| 英文题名 | Capturing Closely Interacted Two-Person Motions with Reaction Priors |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://neteasegameai.github.io/Dual-Human/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Reaction Prior-based Two-Person MoCap |
| Dataset | Dual-Human |

> [!tip] 效果简介
> - Dual-Human 上，MPJPE 63.4 vs 67.3 (BUDDI) (-3.9)。

## 概要

### 问题瓶颈

在两人紧密交互场景（如握手、拥抱、搏斗）中，频繁的人员间相互遮挡使得现有3D人体姿态估计算法难以稳定输出准确的姿态。传统方法要么将两人独立处理而忽略交互上下文，要么仅依赖静态距离先验（如BUDDI的proxemics先验），在严重遮挡下缺乏足够的语义引导能力，导致被遮挡关节的预测出现明显偏差甚至物理不合理。

### 核心结论

本文提出**反应先验（Reaction Priors）**——一种基于运动变分自编码器（Motion VAE）和可逆神经网络（INN）构建的双向条件概率模型，用以刻画给定一人运动时另一人运动的概率分布。该先验以两种方式注入姿态估计流程：训练时作为KL散度正则化项约束估计分布，测试时作为优化目标引导隐变量向合理区域收敛。在合成数据集Dual-Human上，该方法取得了**MPJPE 63.4**的结果，相较BUDDI的67.3降低3.9，消融实验证实运动VAE、INN及噪声增强训练策略均为关键组件。

### 方法谱系与知识库定位

从方法谱系看，该工作处于**交互式多人姿态估计**与**数据驱动人体先验**的交叉点。与BEV（Sun et al., CVPR 2022）和CLIFF（Li et al., ECCV 2022）等将两人独立建模的基线不同，本文的核心贡献在于将交互语义显式编码为概率先验。相较于BUDDI（Muller et al., arXiv 2023）的静态距离先验，反应先验具备三个关键升级：

| 方法维度 | BUDDI (proxemics) | 本文 (reaction priors) |
|---------|-------------------|----------------------|
| 先验类型 | 静态距离分布 | 动态条件概率（Motion VAE + INN双向建模） |
| 注意力机制 | 分离式管道 | 交互感知自注意力（人体内+人体间） |
| 先验注入方式 | 仅测试时优化 | 训练KL正则化 + 测试时隐变量优化 |

该方法的定位是**利用强语义交互先验去模糊化遮挡**，其技术路线与“学习条件生成先验以正则化病态逆问题”的范式一致，但将其首次系统性地应用于两人紧密交互运动捕捉场景。

### 主要结果概要

在Dual-Human数据集上，本文方法在MPJPE指标上达到63.4，显著优于BUDDI（67.3）、BEV（73.2）和CLIFF（78.5）等基线。消融实验揭示：去除运动VAE使误差升至64.4，将INN替换为MLP使误差升至66.2，而去除噪声增强训练则导致误差急剧上升至77.4，表明时序动态建模、可逆交互对称性以及模拟估计误差的噪声增强三者缺一不可。定性结果（Figure 1, Figure 7）进一步显示，该方法在轻度遮挡和严重遮挡场景下均能恢复出物理合理的两人交互姿态。



从单目视频中捕捉多人3D运动是计算机视觉领域的核心挑战之一，在VR/AR、运动分析、游戏角色动画等场景中具有广泛的应用需求。当场景中包含两人紧密交互——如握手、拥抱、跳舞或武术对抗——时，问题难度急剧上升。其根本瓶颈在于：**紧密交互场景中频繁的人员间相互遮挡导致现有姿态估计算法难以稳定输出准确的3D人体姿态**。在严重遮挡下，单靠视觉观测本身往往不足以唯一确定被遮挡关节的位置，这使得传统依赖局部图像特征的姿态估计器在这些区域产生大幅误差甚至完全失效。

现有方法在处理两人交互时存在明显的结构性缺口。主流的自顶向下（top-down）或自底向上（bottom-up）姿态估计管道通常将多人视为独立个体，缺乏对交互语义的显式建模。近期工作如 **BUDDI**（Muller et al., arXiv 2023）引入了“proxemics”先验，利用两人之间的静态空间距离分布来约束姿态估计，这在一定程度上改善了交互场景下的结果。然而，proxemics先验本质上是一种几何层面的弱先验：它仅编码了“两人通常不会穿透彼此”或“在特定社交距离下共现”这样的静态约束，并未捕捉交互动作本身蕴含的丰富语义信息——例如，当一人伸出手时，另一人很可能做出相应的握手动作；当一人拥抱时，另一人的手臂位置高度可预测。这种**语义层面的条件依赖**是proxemics先验无法建模的，也是其性能上限的根本原因。

本文的核心动机正是填补这一空白：**紧密交互动作通常发生在特定情境下（如握手、拥抱），这些情境构成强语义先验，可用于推断被遮挡关节的姿态**。具体而言，给定交互中一方的运动序列，另一方的运动并非任意分布，而是受交互语义强约束的条件概率分布。如果能够从数据中学习这种“给定动作预测反应”的双向条件概率模型，并将其作为先验注入姿态估计流程，就有望在遮挡导致视觉证据不足时，通过先验知识“补全”合理的两人运动。这一思路将交互建模从静态空间约束推进到动态语义条件建模，构成了本文方法设计的核心驱动力。



## 核心方法与创新机理

本工作针对紧密交互两人场景中频繁相互遮挡导致的姿态估计退化问题，提出**反应先验（Reaction Priors）**——一种基于运动VAE与可逆神经网络（INN）双向建模的条件概率分布，用于刻画“给定一人姿态时另一人姿态的合理分布”。该先验以两种方式注入姿态估计流程：训练阶段作为KL散度正则化项约束估计分布，测试阶段作为优化目标中的先验项引导遮挡下的姿态恢复。与现有方法相比，核心创新体现在以下三个维度的机制性改变。

**两人先验类型：从静态距离约束到双向条件运动分布。** 此前最具代表性的两人先验是 **BUDDI**（Muller et al., arXiv 2023）中的 proxemics 先验，本质上是基于人体相对距离与朝向的静态空间约束。反应先验则从根本上改变了先验的建模对象——不再约束两人的空间配置，而是学习“一人运动条件下另一人运动的条件概率分布” $p(\tilde{\pmb{x}}_r|\pmb{x}_a)$。具体实现上，运动VAE将单人运动序列编码为紧凑的隐变量分布 $\mathcal{N}(\mu,\sigma)$，反应生成器（基于INN）将动作隐变量分布 $\mathcal{N}(\mu_a,\sigma_a)$ 映射为反应隐变量分布 $\mathcal{N}(\tilde{\mu}_r,\tilde{\sigma}_r)$，再由VAE解码器恢复为反应姿态。INN的可逆性保证了双向建模能力——同一网络既可正向生成反应，也可反向推断动作，从而充分利用交互的对称性。定量对比（Table 3）显示，反应先验在 Dual-Human 数据集上的 MPJPE 为 64.1，显著优于 BUDDI proxemics 先验的 67.3（$\Delta=-3.2$），验证了从静态空间约束升级为动态条件运动分布的有效性。

**姿态估计网络注意力机制：从独立感知到交互感知。** 传统两人姿态估计方法（如 **BEV**（Sun et al., CVPR 2022）、**CLIFF**（Li et al., ECCV 2022））或采用分离式自顶向下/自底向上管道，或使用标准自注意力，未显式建模两人之间的特征交互。本工作将姿态估计器设计为查询式（query-based）decoder-only Transformer，并在注意力机制中引入**交互感知自注意力（interaction-aware self-attention）**：将注意力拆分为人体内自注意力与人体间自注意力两个分支，使网络能显式感知另一人的特征线索。这一设计直接回应了瓶颈问题——当一人被严重遮挡时，其姿态查询可通过人体间注意力从较清晰可见的另一人特征中获取上下文信息。Figure 8（左）的收敛曲线表明，交互感知自注意力相比标准注意力在训练过程中收敛更快、最终误差更低，验证了该注意力设计的增益。

**先验注入方式：从纯监督损失到训练正则化与测试时优化双阶段引导。** 传统姿态估计方法仅依赖监督损失（如L1/L2）驱动训练，对遮挡场景缺乏显式的先验引导。本工作将反应先验分别嵌入训练与测试两个阶段：训练时，通过KL散度损失 $\mathcal{L}_{prior} = \mathcal{D}_{KL}[p(z_r|\hat{\pmb{x}}_r) || p(\tilde{z}_r|\hat{\pmb{x}}_a)]$ 将估计的反应隐变量分布拉近由动作条件生成的反应先验分布，实现正则化（Equation 4）；测试时，以反应隐变量的均值 $\boldsymbol{\mu}_r^{opt}$ 和方差 $\boldsymbol{\sigma}_r^{opt}$ 为优化变量，最小化包含数据项与先验项的复合目标 $\mathcal{L} = ||\mathcal{D}(\boldsymbol{\mu}_r^{opt},\boldsymbol{\sigma}_r^{opt}) - \hat{\boldsymbol{x}}_r||_2^2 + \lambda_{prior} \cdot \mathcal{D}_{KL}[\mathcal{N}(\boldsymbol{\mu}_r^{opt},\boldsymbol{\sigma}_r^{opt}) || p(\tilde{z}_r|\hat{\boldsymbol{x}}_a)]$（Equation 5），使被遮挡者的姿态既贴合稀疏观测又符合交互语义。消融实验（Table 4）为这一双阶段注入机制提供了关键支撑：去除运动VAE使MPJPE从63.4升至64.4，将INN替换为普通MLP使MPJPE升至66.2，而不使用噪声增强（模拟估计误差）训练时MPJPE急剧恶化至77.4，证明反应先验各组件及其鲁棒训练策略对最终性能不可或缺。



本文提出一个基于**反应先验（Reaction Priors）**的两人紧密交互运动捕捉框架，其核心思路是将交互语义作为概率先验注入姿态估计流程，从而解决频繁相互遮挡导致的姿态估计不稳定问题。整体框架由四个主要模块串联构成，形成“特征提取—姿态估计—先验正则化—时序平滑”的处理流水线。

### 输入输出流

框架的输入端为包含两人的单目视频帧或图像序列。输出端为两人各自的3D人体姿态序列（SMPL模型参数）及其在世界坐标系中的平移向量。整个流水线可概括为以下步骤：

1. **图像特征提取**：使用HRNet作为骨干网络，从输入图像中提取多尺度空间特征。
2. **查询式姿态估计**：基于解码器专用Transformer（decoder-only Transformer）的估计器，通过可学习的Pose查询、Transl查询、Prob查询和Track查询，从图像特征中解码出两人的3D姿态、平移和显著性分数。该Transformer引入**交互感知自注意力（interaction-aware self-attention）**，在人体内自注意力的基础上增加人体间自注意力，使两人的查询在注意力计算中显式交互。
3. **反应先验注入**：反应先验模块（由运动VAE和反应INN组成）在训练和测试阶段以不同方式介入——
   - **训练阶段**：反应先验通过KL散度正则化损失 $\mathcal{L}_{prior}$ 拉近估计的反应隐变量分布与从动作隐变量生成的反应先验分布，作为姿态估计器的额外监督信号。
   - **测试阶段**：在姿态估计器给出初始预测后，以反应隐变量的均值 $\boldsymbol{\mu}_r^{opt}$ 和方差 $\boldsymbol{\sigma}_r^{opt}$ 为优化变量，通过最小化数据项（与观测姿态的L2距离）和先验项（与反应先验分布的KL散度）的加权和，对遮挡严重者的姿态进行迭代优化。
4. **时序平滑**：最后通过SmoothNet对估计的运动序列进行时序平滑处理，消除帧间抖动。

### 反应先验的核心地位

反应先验是整个框架的**因果旋钮（causal knob）**。它建模了给定一人运动条件下另一人运动的概率分布 $p(\tilde{\boldsymbol{x}}_r|\boldsymbol{x}_a)$，使系统在遮挡严重时能够利用交互的对称性和双向条件概率进行去模糊化推断。这一先验通过运动VAE（编码运动到紧凑隐空间）和反应INN（在隐空间中实现动作到反应的可逆变换）实现，其双向建模能力是区别于BUDDI静态距离先验的关键所在。

### 模块间的依赖关系

四个模块构成强依赖链：HRNet特征质量决定了姿态估计的上限；姿态估计器的交互感知自注意力为反应先验提供了初始的“动作—反应”配对信息；反应先验反过来矫正姿态估计器在遮挡下的错误预测，形成闭环优化；SmoothNet则作为后处理环节，不参与核心的遮挡推理逻辑。消融实验证实，移除运动VAE或INN均会导致姿态估计误差显著上升（Table 4），说明反应先验的各组件对整体性能不可或缺。



### 反应先验生成模块

反应先验由三个子模块串联构成（Figure 3）：

![[assets/figures/papers/paper_list_l1711_Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction/figures/003_Figure_3.jpg]]
*Figure 3: Reaction Priors. The reaction priors are composed of a VAE encoder, a reaction generator, and a VAE decoder. Initially, the VAE encoder maps the motion to the latent distribution. After that, the action distribution*

1. **运动VAE编码器**：将输入动作序列 $\pmb{x}_a$ 映射到紧凑的隐变量分布 $\mathcal{N}(\pmb{\mu}_a, \pmb{\sigma}_a)$。该编码器基于标准VAE框架，以证据下界（ELBO）为目标进行训练：

   $$\log p(\pmb{x}) \geq \mathbb{E}_{z \sim q}[\log p(\pmb{x}|z)] - \mathcal{D}_{KL}[q(z|\pmb{x})||p(z)] \tag{1}$$

   实际训练中采用L1重建损失与KL散度正则的加权组合：

   $$\mathcal{L}_{vae} = ||\hat{\boldsymbol{x}} - \boldsymbol{x}||_1 + \lambda_{dist} \cdot \mathcal{D}_{KL}[p(z|\boldsymbol{x}) || \mathcal{N}(\mathbf{0}, I)]$$

   其中 $\lambda_{dist}$ 控制先验正则强度。

2. **反应生成器（Reaction INN）**：以可逆神经网络实现，将动作隐变量 $\pmb{z}_a$ 双向映射为反应隐变量 $\tilde{\pmb{z}}_r$。INN的核心优势在于其可逆性保证了信息无损传递，且通过变量变换公式可直接计算条件概率密度：

   $$p(\tilde{z}_r|\mathbf{x}_a) = p(z_a|\mathbf{x}_a) \cdot \prod_k |\operatorname{det}(\frac{\partial f_k}{\partial z_k})|^{-1} \tag{3}$$

   其中 $f_k$ 为INN的第 $k$ 个可逆层，行列式项反映变换过程中的体积变化。

3. **运动VAE解码器**：将生成的隐变量 $\tilde{\pmb{z}}_r \sim \mathcal{N}(\tilde{\pmb{\mu}}_r, \tilde{\pmb{\sigma}}_r)$ 解码为反应姿态 $\tilde{\pmb{x}}_r$。

整体反应概率分布可近似为：

$$p(\tilde{\pmb{x}}_r|\pmb{x}_a) \approx \iint \underbrace{p(\boldsymbol{z}_a|\pmb{x}_a) \cdot p(\tilde{\boldsymbol{z}}_r|\boldsymbol{z}_a)}_{\mathcal{N}(\tilde{\mu}_r,\tilde{\boldsymbol{\sigma}}_r)} \cdot p(\tilde{\pmb{x}}_r|\tilde{\boldsymbol{z}}_r) \mathrm{d}\boldsymbol{z}_a \mathrm{d}\tilde{\boldsymbol{z}}_r \tag{2}$$

### 先验注入机制

反应先验通过两种方式注入姿态估计流程：

**训练阶段**（Equation 4）：以KL散度作为正则化损失，迫使从观测 $\hat{\pmb{x}}_r$ 编码得到的隐变量分布 $p(z_r|\hat{\pmb{x}}_r)$，逼近由动作 $\hat{\pmb{x}}_a$ 经反应生成器产生的先验分布 $p(\tilde{z}_r|\hat{\pmb{x}}_a)$：

$$\mathcal{L}_{prior} = \mathcal{D}_{KL}[p(z_r|\hat{\pmb{x}}_r) || p(\tilde{z}_r|\hat{\pmb{x}}_a)] \tag{4}$$

**测试时优化**（Equation 5）：以反应隐变量的均值 $\pmb{\mu}_r^{opt}$ 和方差 $\pmb{\sigma}_r^{opt}$ 为优化变量，最小化数据项与先验项的加权组合：

$$\mathcal{L}(\pmb{\mu}_r^{opt}, \pmb{\sigma}_r^{opt}) = ||\mathcal{D}(\pmb{\mu}_r^{opt}, \pmb{\sigma}_r^{opt}) - \hat{\boldsymbol{x}}_r||_2^2 + \lambda_{prior} \cdot \mathcal{D}_{KL}[\mathcal{N}(\pmb{\mu}_r^{opt}, \pmb{\sigma}_r^{opt}) || p(\tilde{z}_r|\hat{\boldsymbol{x}}_a)] \tag{5}$$

其中 $\mathcal{D}(\cdot)$ 为VAE解码器，第一项确保解码姿态与噪声观测 $\hat{\boldsymbol{x}}_r$ 一致，第二项将优化变量拉向反应先验分布。$\lambda_{prior}$ 平衡数据保真度与先验引导强度。

### 姿态估计器中的交互感知注意力

姿态估计器采用仅解码器的Transformer架构（Figure 4），其核心创新在于交互感知自注意力机制。该模块将标准自注意力分解为两部分：

![[assets/figures/papers/paper_list_l1711_Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction/figures/004_Figure_4.jpg]]
*Figure 4: 3D Pose Estimator for Two People*

- **人体内自注意力**：同一人体内的查询（Pose/Transl/Prob查询）相互关注，建模个体姿态内部的关节依赖关系。
- **人体间自注意力**：跨人体的查询相互关注，使得两人姿态估计能够感知对方的运动状态，从而在遮挡场景下利用交互上下文进行推理。

消融实验（Table 4）证实，交互感知自注意力相比普通自注意力显著降低姿态估计误差，验证了该模块对捕捉两人交互动态的关键作用。



## 实验与关键发现

### 核心实验设置

本文在合成数据集 **Dual-Human** 和真实多视角数据集 **Hi4D** 上评估方法。Dual-Human 包含 12 类紧密交互动作（握手、拥抱、跳舞、武术等），总计 1.2M 帧，提供 SMPL-X 参数、接触标注和多视角渲染图像，规模远超此前的交互人体数据集（Table 1）。评估指标采用 **MPJPE**（平均关节位置误差，mm）、**PA-MPJPE**（Procrustes 对齐后的 MPJPE）和 **Transl**（平移误差，mm）。

![[assets/figures/papers/paper_list_l1711_Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction/figures/005_Table_1.jpg]]
*Table 1: Comparison of Human Interacted Datasets. Only twoperson motions are counted. ‘MV’ is multi-view. Inter-Human [33] is a very recent work for motion generation rather than capture, thus has limited accuracy, which is listed for completeness*

### 主结果

在 Dual-Human 数据集上，本文方法取得 **MPJPE 63.4、PA-MPJPE 51.2、平移误差 112.1**，在所有指标上显著优于先前方法（Table 2）。具体而言，相比最近的两人姿态估计方法 **BUDDI**（Muller et al., arXiv 2023），MPJPE 降低 **3.9 mm**（63.4 vs 67.3）；相比通用单人多视角方法 **BEV**（Sun et al., CVPR 2022）和 **CLIFF**（Li et al., ECCV 2022），优势更为显著。在真实数据集 Hi4D 上，本文方法同样取得最优的 MPJPE **75.0** 和 PA-MPJPE **59.7**，验证了跨域泛化能力。

![[assets/figures/papers/paper_list_l1711_Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction/figures/008_Table_2.jpg]]
*Table 2: Results on Interacted Human Benchmarks. ‘PA’ is PA-MPJPE*

定性结果（Figure 7）进一步展示了方法在严重遮挡场景下的优势：BEV 和 CLIFF 在两人紧密接触时产生明显的姿态穿透和关节错位，BUDDI 的空间先验虽能约束穿透但姿态合理性不足，而本文的反应先验能够恢复符合交互语义的自然姿态。

![[assets/figures/papers/paper_list_l1711_Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative Comparisons. We compare our approach with previous methods including BEV [54], BUDDI [40] and CLIFF [32] on Dual-Human and Hi4D. The best view that can show the differences is chosen for rendering*

### 先验对比

Table 3 直接对比了两种两人先验的效能：将 BUDDI 的 **proxemics 先验**（基于距离的排斥/吸引项）替换为本文的 **反应先验**，MPJPE 从 67.3 降至 **64.1**。这一差距（3.2 mm）表明，静态空间距离约束无法捕捉交互动作的时序动态和语义结构，而基于运动 VAE 和 INN 建模的交互条件概率分布能够提供更强的遮挡推断能力。

![[assets/figures/papers/paper_list_l1711_Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction/figures/009_Table_3.jpg]]
*Table 3: Comparisons of Two-Person Priors*

### 消融实验

Table 4 的消融实验揭示了反应先验各组件的贡献：

- **去除运动 VAE**：将 VAE 替换为确定性编码器，MPJPE 从 63.4 升至 **64.4**。运动 VAE 的隐变量分布建模为反应生成提供了时序动态先验，缺失后模型难以捕捉动作的连续性和变化模式。
- **将 INN 替换为 MLP**：MPJPE 急剧上升至 **66.2**。INN 的可逆性保证了动作隐变量与反应隐变量之间的双向双射映射，这对交互对称性建模至关重要；普通 MLP 无法保证信息无损传递，导致反应生成质量显著下降。
- **去除噪声增强训练**：训练时不对动作隐变量注入噪声以模拟姿态估计误差，MPJPE 飙升至 **77.4**。这一结果表明，测试时优化所依赖的先验分布必须覆盖姿态估计器输出的噪声区域，否则先验引导将失效。

### 收敛性分析

Figure 8 展示了两个关键模块的收敛对比：交互感知自注意力（interaction-aware self-attention）相比普通自注意力在训练过程中收敛更快且最终损失更低；INN 作为反应生成器相比 MLP 同样表现出更优的收敛特性。这从优化动力学角度佐证了架构设计的合理性。

![[assets/figures/papers/paper_list_l1711_Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction/figures/012_Figure_8.jpg]]
*Figure 8: Convergence Comparisons. Left: interaction-aware self-attention v.s. the vanilla attention for the pose estimator. Right: INN v.s. MLPs for the reaction generator*

### 失败模式与局限性

尽管方法在基准测试上表现优异，但存在以下已知局限：

1. **交互类型泛化**：反应先验的训练依赖 Dual-Human 中的 12 类交互动作，对训练集未覆盖的交互类型（如推搡、跌倒等）可能产生不合理的姿态推断。
2. **人数假设**：方法假设场景中恰好有两人且存在紧密交互，当人数超过两人或交互稀疏时，先验注入可能引入虚假互动。
3. **计算开销**：测试时优化需要迭代求解隐变量分布，计算开销高于单次前向推理，可能限制实时应用。
4. **合成-真实域差异**：Dual-Human 为合成渲染数据，与真实图像的纹理、光照、背景差异可能影响实际部署精度，尽管 Hi4D 上的结果部分缓解了这一担忧。

### 开放问题

- 如何将反应先验扩展至三人及以上的多人交互场景，并建模更复杂的社交关系图？
- 当输入视频中两人实际未发生交互时，如何自适应调节先验权重以避免生成虚假互动动作？
- 反应先验的概率框架是否可以融合物理约束（如接触力、不可穿透性）以进一步提升遮挡下姿态的物理合理性？

### 补充图表

![[assets/figures/papers/paper_list_l1711_Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction/figures/001_Figure_1.jpg]]
*Figure 1: The proposed reaction priors can optimize the human motions from pose estimators for both less-occluded cases (blue box) and severely occluded cases (orange box)*

![[assets/figures/papers/paper_list_l1711_Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction/figures/007_Figure_6.jpg]]
*Figure 6: System Configurations of Dual-Human*



## 定位与知识库关联

### 方法沿革与基线对比

本文工作处于**交互式多人3D姿态估计**的交叉地带，其核心贡献——反应先验（Reaction Priors）——直接回应了现有方法在紧密交互场景中因相互遮挡导致姿态估计崩溃的瓶颈。基线方法可沿两条轴线定位：

**单人与多人姿态估计基线。** 传统自顶向下（top-down）管道（如**BEV**，Sun et al., CVPR 2022）和自底向上（bottom-up）方法在单人场景表现稳健，但缺乏对交互上下文的显式建模，在严重遮挡下易产生穿透、漂浮等物理不合理姿态。**CLIFF**（Li et al., ECCV 2022）通过引入全局人体位置先验改善了相机空间中的姿态估计，但同样未建模人际交互约束。本文在姿态估计器层面引入**交互感知自注意力**（interaction-aware self-attention），将人体内自注意力与人体间自注意力结合，使查询式Transformer能够显式感知两人间的空间关系，这是对标准自注意力机制在多人场景下的直接改进。

**两人交互先验基线。** 最直接的可比工作是**BUDDI**（Muller et al., arXiv 2023），该方法利用proxemics先验——基于两人间静态距离分布的正则化——来约束交互姿态。然而，proxemics先验仅编码了空间邻近性，缺乏对交互动态语义（如握手、拥抱等情境化动作模式）的建模能力。本文的反应先验通过**运动VAE + 可逆神经网络（INN）** 构建了双向条件概率分布 $p(\tilde{\pmb{x}}_r|\pmb{x}_a)$，将先验从静态空间关系提升至时序动态交互语义层面。Table 3的直接对比显示，反应先验在MPJPE上达到64.1，优于BUDDI proxemics先验的67.3（降低3.2 mm），验证了语义级交互建模相对于纯空间先验的显著增益。

### 核心机制差异

从方法学角度，反应先验的设计包含三个关键创新槽位：

1. **先验类型升级**：从BUDDI的静态距离先验升级为基于动作-反应双向条件概率的语义先验。运动VAE将时序姿态序列编码为紧凑的隐变量分布 $\mathcal{N}(\mu_a, \sigma_a)$，INN以可逆变换将该分布映射为反应隐变量分布 $\mathcal{N}(\tilde{\mu}_r, \tilde{\sigma}_r)$，从而在隐空间中捕获交互的对称性和双向性。

2. **先验注入机制的双阶段设计**：训练阶段通过KL散度正则化 $\mathcal{L}_{prior} = \mathcal{D}_{KL}[p(z_r|\hat{\pmb{x}}_r) || p(\tilde{z}_r|\hat{\pmb{x}}_a)]$ 将反应先验融入姿态估计器的学习目标（Equation 4）；测试阶段则通过优化反应隐变量的均值与方差 $\mathcal{L}(\pmb{\mu}_r^{opt}, \pmb{\sigma}_r^{opt})$，在数据项（与观测姿态的L2距离）和先验项（与反应先验分布的KL散度）之间寻求平衡（Equation 5）。这种训练-测试双重注入机制使得先验既能指导网络参数学习，又能在推理时灵活适应特定观测。

3. **噪声增强训练策略**：Table 4的消融实验揭示了一个关键实现细节——若不使用噪声增强（模拟姿态估计器的预测误差）进行训练，MPJPE从63.4急剧恶化至77.4。这表明反应先验的有效性高度依赖其在训练期间对估计不确定性分布的暴露，否则在测试时面对有噪声的姿态输入时泛化能力严重不足。

### 适用边界与局限

**场景假设约束。** 方法明确假设场景中**仅有两人且存在紧密交互**。当人数超过两人时，交互感知自注意力的计算复杂度将平方级增长，且反应先验的双向条件结构无法直接推广至多人图模型。当两人实际未发生交互时，过大的先验权重 $\lambda_{prior}$ 可能错误地生成虚假互动动作——这是一个在开放问题中被明确提及但未经验证的潜在失效模式。

**数据依赖性。** 反应先验的训练完全依赖Dual-Human数据集中的交互类别（握手、拥抱、击掌等结构化交互）。对于训练分布外的新颖交互类型（如推搡、跌倒、对抗性动作），反应先验的条件概率估计可能产生不可靠的预测。此外，Dual-Human为合成渲染数据（如Figure 5所示），其光照、纹理、背景与真实场景存在domain gap，实际部署时的精度衰减幅度尚需真实数据验证。

**计算开销。** 测试时优化过程需要迭代求解 $\pmb{\mu}_r^{opt}, \pmb{\sigma}_r^{opt}$，这与前馈式姿态估计器形成额外的计算负担。虽然Figure 8展示了INN相比MLP在收敛速度上的优势，但实时应用场景（如在线动作捕捉）的可行性仍需进一步评估。

### 在知识库中的定位与开放问题

本文在交互式姿态估计领域建立了**语义条件先验**这一新范式，其核心洞察——紧密交互动作构成强语义上下文，可用于推断被遮挡关节——为后续工作打开了若干方向：

1. **先验的物理增强**：当前反应先验纯粹从运动学数据中学习统计规律，缺乏对接触力、穿透约束等物理信息的显式建模。将反应先验的概率框架与物理仿真（如接触动力学约束）融合，可能进一步提升严重遮挡下姿态的物理合理性。

2. **多人扩展**：如何将双向条件概率结构扩展至三人及以上的交互图模型，以及如何处理更复杂的社交关系（如群体对话中的注意力方向、多人协作任务中的角色分工），是该方法走向通用多人场景的关键挑战。

3. **开放世界交互泛化**：针对训练数据中未出现的交互类型，可能需要引入少样本学习或零样本推理机制，例如利用大语言模型中的交互常识知识来引导反应先验的适应。

4. **先验权重的自适应调节**：在输入视频中两人交互强度动态变化的场景下，如何根据遮挡程度或交互置信度自适应调节 $\lambda_{prior}$，以避免在非交互帧产生虚假互动，是提升方法鲁棒性的重要工程问题。



## 原文 PDF

![[paperPDFs/CVPR_2024/Fang_et_al_Capturing_Closely_Interacted_Two_Person_Motions_with_Reaction_Priors.pdf]]
