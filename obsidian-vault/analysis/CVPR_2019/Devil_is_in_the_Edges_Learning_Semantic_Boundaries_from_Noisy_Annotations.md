---
title: "Devil is in the Edges: Learning Semantic Boundaries from Noisy Annotations"
type: paper
paper_level: A
venue: CVPR
year: 2019
pdf_ref: paperPDFs/CVPR_2019/Devil_is_in_the_Edges_Learning_Semantic_Boundaries_from_Noisy_Annotations.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/STEAL/
aliases:
- SSTEAL
- DIELSBFNA
tags:
- CVPR_2019
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "引入边界细化层（NMS损失）强制边界法线方向上的最大响应，以及主动对齐框架迭代推理真实边界，使得网络能从粗标注中学习细边界。"
primary_logic: "通过两条互补途径——边界方向的局部约束（NMS损失）和全局标注的迭代对齐（主动对齐）——可以在不改变主干网络的前提下，显著提升边界清晰度和AP指标，并支持粗标注数据的自动精化。"
claims:
- "在重新标注的高质量SBD测试集上，STEAL将CASENet的MF(ODS)从63.52%提升至68.15%（+4.63%），AP提升超过18个百分点。"
- "仅应用NMS损失层即可超越SEAL方法超过1% MF(ODS)和AP，表明直接优化边界方向优于复杂的图匹配对齐。"
- "在Cityscapes val上，STEAL预测的边界比DeepLab v3+分割掩码提取的边缘在严格匹配阈值下高4.2%。"
- "采用主动对齐后，在模拟8px标注噪声的SBD训练集上，MF(ODS)达到56.41%，显著高于不进行对齐的版本。"
---

# Devil is in the Edges: Learning Semantic Boundaries from Noisy Annotations

> [!tip] 核心洞察
> 通过两条互补途径——边界方向的局部约束（NMS损失）和全局标注的迭代对齐（主动对齐）——可以在不改变主干网络的前提下，显著提升边界清晰度和AP指标，并支持粗标注数据的自动精化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 细节在于边缘：从噪声标注中学习语义边界 |
| 英文题名 | Devil is in the Edges: Learning Semantic Boundaries from Noisy Annotations |
| 会议/期刊 | CVPR 2019 |
| Links | [paper](https://arxiv.org/abs/1904.07934); [Project](https://nv-tlabs.github.io/STEAL/); [Project](https://research.nvidia.com/labs/toronto-ai/STEAL/) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | STEAL (Semantically Thinned Edge Alignment Learning) |
| Dataset | SBD re-annotated test set (high-quality), SBD original test set, Cityscapes val |

> [!tip] 效果简介
> - SBD re-annotated test set (high-quality) 上，MF(ODS) 为 68.15，对比 63.52 (CASENet)，变化 +4.63。
> - SBD re-annotated test set (high-quality) 上，AP 为 62.57，对比 ~43.96 (CASENet)，变化 +18.61。
> - SBD original test set 上，MF(ODS) mean 为 75.6，对比 71.88 (CASENet, inferred)，变化 +3.72。

## 概述

**问题瓶颈**：当前语义边界数据集普遍存在标注噪声，人工标注的边界往往比真实边界更粗且位置不准。标准方法直接使用带噪标注训练加权二元交叉熵损失，缺乏对边界形状的显式约束，导致学习到的边界预测过厚且对齐精度不足。

**核心思路**：本文提出 **STEAL（Semantically Thinned Edge Alignment Learning）**，通过两条互补途径解决上述问题——在局部，引入**边界细化层**与**NMS损失**，约束每个边界像素沿其法线方向取得最大响应；在全局，提出**主动对齐**框架，在训练中迭代地将带噪标注向网络高置信区域调整，联合优化潜在真实边界与网络参数。该方法可即插即用地接入现有语义边界检测网络。

**方法定位**：STEAL 以 **CASENet**（Yu et al., CVPR 2017）为主干网络，与基于图匹配对齐的 **SEAL**（Yu et al., ECCV 2018）形成对比。其损失函数将标准加权 BCE 扩展为三项联合损失（BCE + NMS损失 + 方向损失），训练时的标注则从直接使用原始噪声标注变为通过主动对齐迭代细化。

**主要结果**：
- 在重新标注的高质量 SBD 测试集上，STEAL 将 CASENet 的 MF(ODS) 从 63.52% 提升至 **68.15%**（+4.63%），AP 提升超过 **18 个百分点**（Abstract, Table 1）。
- 仅应用 NMS 损失层即可超越 SEAL 方法超过 1% MF(ODS) 和 AP，表明直接优化边界方向优于复杂的图匹配对齐（Table 1）。
- 在 Cityscapes val 上，STEAL 预测的边界比 **DeepLab v3+**（Chen et al., ECCV 2018）分割掩码提取的边缘在严格匹配阈值下高 **4.2%**（Fig. 5）。
- 当训练标注存在 8px 模拟噪声时，主动对齐使 MF(ODS) 从 46.26% 大幅提升至 **56.41%**，验证了其对标注质量的鲁棒性（Table 4）。

## 背景与动机

### 语义边界检测的任务定位与瓶颈

语义边界检测（semantic boundary detection）要求同时定位物体边缘并识别其所属语义类别，是连接底层视觉线索与高层场景理解的关键中间表示。与经典边缘检测不同，语义边界检测需要处理类内纹理、遮挡和细粒度物体轮廓，因此对边界的**清晰度（sharpness）**和**精确性（precision）**提出了更高要求。

当前该领域面临一个根本性瓶颈：**现有语义边界数据集存在显著的标注噪声**。人工标注的边界往往偏离真实物体轮廓数个像素，且边界宽度不一致——标注者倾向于画出“厚”边界而非精确的单像素轮廓。这导致两个连锁问题：

1. **标准损失函数未显式处理边界对齐**。主流方法（如CASENet，Yu et al., CVPR 2017）采用加权二元交叉熵损失（weighted BCE），仅进行逐像素独立分类，缺乏对边界形状的几何约束。网络从噪声标注中学习到的边界预测同样过厚且不精确。
2. **评估指标与真实需求脱节**。在宽松匹配阈值下，厚边界仍可获得高分，但在严格阈值（如~2px）下性能急剧下降——而这恰恰是下游应用（如实例分割、图像编辑）所要求的精度。

### 现有方法的局限性

针对上述问题，已有工作尝试从不同角度改进：

- **CASENet**（Yu et al., CVPR 2017）通过多尺度特征融合和类别感知分类，奠定了深度语义边界检测的基础框架，但其损失函数仍为标准BCE，未对边界形状建模。
- **SEAL**（Yu et al., ECCV 2018）首次引入边缘对齐机制，通过图匹配（graph matching）在训练时对齐预测边界与标注边界。然而，该方法依赖复杂的图构建与匹配过程，且仅对齐标注本身，未从根本上解决标注噪声问题——当标注本身偏离真实边界时，对齐操作反而可能强化错误信号。

上述方法的共性问题在于：**将带噪声的人工标注视为“真值”进行拟合，而非主动推理真实边界**。这限制了边界检测精度在严格指标下的提升空间。

### 本文的核心动机与洞察

本文的出发点可概括为：**细节在于边缘（Devil is in the Edges）**——语义边界检测的瓶颈不在于主干网络的特征提取能力，而在于如何从噪声标注中学习精确、细化的边界表示。

作者提出两条互补的解决途径，构成STEAL（Semantically Thinned Edge Alignment Learning）的核心设计逻辑：

1. **局部约束：边界法线方向的最大响应**。理想情况下，边界检测器在真实边缘像素处应沿法线方向产生唯一的最大响应，类似于非极大值抑制（NMS）的效果。通过在训练时引入可微的边界细化层（boundary thinning layer）和NMS损失，可以直接约束网络输出满足这一几何先验，从而“细化”过厚的边界预测。

2. **全局对齐：迭代推理真实边界**。如果标注本身不可靠，则不应将其视为固定目标。主动对齐（active alignment）框架将标注视为可优化的变量，在训练过程中利用网络当前的高置信度预测，通过水平集演化（level set evolution）将标注曲线向真实边界调整，形成“网络指导标注、标注训练网络”的协同循环。

这两条途径——边界方向的局部约束与标注的全局迭代对齐——**均不改变主干网络结构**，可作为即插即用的模块叠加于现有检测器之上。其核心洞察在于：通过显式建模边界形状先验和标注不确定性，可以在不增加推理复杂度的前提下，显著提升边界清晰度和检测精度，并支持粗标注数据的自动精化。

## 核心创新

STEAL 的核心创新在于**不改变主干网络**的前提下，通过两个互补的“变更槽”（Changed Slots）系统性地解决语义边界检测中的标注噪声与边界过厚问题：

### 1. 损失函数重构：从无约束交叉熵到方向感知的边界细化

**Baseline 现状**：现有方法（如 CASENet，Yu et al., CVPR 2017）采用加权二元交叉熵损失（BCE）进行多类别边界预测，该损失仅关注像素级分类正确性，缺乏对边界形状的显式约束，导致预测边界过厚且定位模糊。

**STEAL 变更**：引入**边界细化层（Boundary Thinning Layer）** 及配套的复合损失函数，在训练时显式强制边界像素沿法线方向取得最大响应：

- **NMS 归一化**：对每个真实边界像素，沿其法线方向采样 $2L+1$ 个位置（$L=2$，共 5 点），通过 softmax 归一化得到细化概率 $h_k(p|\mathbf{x},\theta)$：
  $$h_k(p|\mathbf{x},\theta) = \frac{\exp(f_k(p|\mathbf{x},\theta)/\tau)}{\sum_{t=-L}^{L} \exp(f_k(p_t|\mathbf{x},\theta)/\tau)}$$
  其中 $\tau=0.1$ 控制锐度。该操作模拟了非极大值抑制（NMS）的效果，使网络在训练过程中即学习产生细边界。

- **NMS 损失**：约束细化后的概率分布趋近独热分布，迫使真实边界像素在法线方向获得最大响应：
  $$\mathcal{L}_{nms}(\theta) = - \sum_k \sum_p \log h_k(p|\mathbf{x},\theta)$$

- **方向损失**：惩罚预测边界法线 $\vec{e}_p(\theta)$ 与真实法线 $\vec{d}_p$ 之间的角度偏差：
  $$\mathcal{L}_{\mathrm{dir}}(\theta) = \sum_k \sum_p || \cos^{-1} \langle \vec{d}_p, \vec{e}_p(\theta) \rangle ||$$

- **总体损失**：加权组合三项损失，常用权重 $\alpha_1=1, \alpha_2=10, \alpha_3=1$：
  $$\mathcal{L} = \alpha_1 \mathcal{L}_{BCE} + \alpha_2 \mathcal{L}_{nms} + \alpha_3 \mathcal{L}_{dir}$$

**因果机制**：NMS 损失直接优化边界的局部锐度（法线方向约束），方向损失则确保边界走向与真实轮廓一致。消融实验（Table 3）证实，仅添加 NMS 损失层即可使 MF(ODS) 超越 SEAL（Yu et al., ECCV 2018）方法超过 1%，表明直接优化边界方向优于 SEAL 中复杂的图匹配对齐策略。

### 2. 训练标注迭代精化：从静态噪声标签到主动对齐

**Baseline 现状**：现有方法直接使用原始带噪声的人工标注作为训练目标，标注中的位置误差（SBD 数据集约 4px 误差）直接转化为网络学习目标，限制了边界精度的上限。

**STEAL 变更**：提出**主动对齐（Active Alignment）** 框架，在训练过程中迭代优化潜在精确边界 $\hat{\mathbf{y}}$ 与网络参数 $\theta$，联合目标函数为：
$$\operatorname*{min}_{\hat{\mathbf{y}},\theta} \mathcal{L}(\hat{\mathbf{y}},\theta) = -\sum_k (\log P(\mathbf{y}_k|\hat{\mathbf{y}}_k) + \log P(\hat{\mathbf{y}}_k|\mathbf{x};\theta))$$
其中第一项为曲线能量项，鼓励推断曲线位于网络高置信区域且靠近原始标注：
$$E(\mathbf{y}_k | \hat{\mathbf{y}}_k, \lambda) = \int g_k(\hat{\mathbf{y}}_k(q)) |\hat{\mathbf{y}}_k'(q)| \partial q$$
通过水平集演化方程实现曲线变形：
$$\frac{\partial \phi}{\partial t} = g_k (\kappa + c) |\nabla \phi| + \nabla g_k \cdot \nabla \phi$$
其中常速度项 $c=1$ 用于避免局部极小值。

**训练策略**：主动对齐在网络精度趋于平稳后引入，可每 $n$ 次迭代执行一次以节省计算开销。该策略将带噪 GT 向网络高置信预测区域调整，生成更精确的伪标签用于后续训练。

**因果机制**：主动对齐形成了“网络预测→标注精化→网络再训练”的正反馈循环。Table 4 显示，在模拟 8px 标注噪声的 SBD 训练集上，加入主动对齐后 MF(ODS) 从 46.26% 跃升至 56.41%（+10.15%），而在高质量标注上增益减小，证明该机制的核心价值在于**从粗标注中自举学习细边界**。

### 创新协同效应

两个变更槽形成互补：**NMS 损失层**提供局部的、边界法线方向的形状约束，使网络本身具备预测细边界的能力；**主动对齐**则从全局标注层面迭代消除训练目标中的系统误差。二者协同使得 STEAL 在高质量重新标注的 SBD 测试集上将 CASENet 的 MF(ODS) 从 63.52% 提升至 68.15%（+4.63%），AP 提升超过 18 个百分点（Table 1），且该方法可即插即用于任意现有语义边界检测网络。

## 整体框架

STEAL（Semantically Thinned Edge Alignment Learning）是一个即插即用的语义边界学习框架，其核心设计目标是从带噪声的标注中学习细粒度、高精度的语义边界。该框架由两条互补的技术路径构成：**边界细化层（Boundary Thinning Layer）及其配套损失函数**，以及**主动对齐（Active Alignment）机制**。前者在局部尺度上约束边界预测的形状，后者在全局尺度上迭代修正训练标注的质量。

### Pipeline 总览

整个 pipeline 的输入是一张 RGB 图像和对应的带噪声语义边界标注。输出为多类别语义边界概率图，其边界响应比传统方法更细、更精确。框架可划分为以下模块：

1. **主干网络（Backbone CNN）**：负责提取多尺度特征并预测类别感知的边界概率图。STEAL 不改变主干结构，实验中以 **CASENet**（Yu et al., CVPR 2017）作为默认主干。
2. **边界细化层（Boundary Thinning Layer）**：在训练阶段，对每个边界像素沿其法线方向采样 $2L+1$ 个位置（$L=2$，共 5 个采样点），通过 softmax 归一化模拟非极大值抑制（NMS），产生细化后的边界概率分布。
3. **NMS 损失（NMS Loss）与方向损失（Direction Loss）**：NMS 损失约束细化后的概率在真实边界像素处趋近独热分布，强制网络在法线方向上产生最大响应；方向损失惩罚预测边界法线与真实法线之间的角度偏差。两者与加权二元交叉熵损失（BCE）联合优化，总损失为 $\mathcal{L} = \alpha_1 \mathcal{L}_{BCE} + \alpha_2 \mathcal{L}_{nms} + \alpha_3 \mathcal{L}_{dir}$。
4. **主动对齐（Active Alignment）**：在训练过程中，利用水平集演化将带噪声的 GT 标注向网络高置信度区域调整，生成更精确的伪标签。该模块与网络参数联合优化，迭代提升标注质量和边界预测精度。
5. **粗到精细化（Coarse-to-Fine Refinement，仅推理阶段）**：给定粗分割掩码，利用训练好的网络和水平集演化（设 $\lambda=0, c=1$）将掩码边缘对齐到网络预测的边界，生成精化后的分割掩码。

### 模块间关系与数据流

下图（Fig. 2 示意）描述了模块间的连接关系：主干网络输出类别边界概率图后，边界细化层在训练时对其进行法线方向采样与 softmax 归一化；NMS 损失和方向损失仅作用于（精化后的）GT 边界位置。主动对齐模块则在训练迭代中周期性地更新 GT 标注，形成“预测→对齐→再训练”的闭环。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_1904_07934/figures/002_Figure_2.jpg]]
*Figure 2: STEAL architecture. Our architecture plugs on top of any backbone architecture. The boundary thinning layer acts upon boundary classification predictions by computing the edge normals, and sampling 5 locations along the normal at each boundary pixel. We perform softmax across these locations, helping us enhance the boundary pixels as in standard NMS. During training, we iteratively refine ground-truth labels using our predictions via an active alignment scheme. NMS and normal direction losses are applied only on the (refined) ground-truth boundary locations*

**关键设计决策**：主动对齐在网络精度趋于平稳后才引入，以减少计算开销；边界细化层仅在训练时使用，推理时被移除，主干网络直接输出细化后的边界预测。

## 核心模块与公式推导

STEAL 的核心由三个功能模块构成：**边界细化层 (Boundary Thinning Layer)**、**主动对齐 (Active Alignment)** 以及一个**组合损失函数**。这些模块可插入任意现有语义边界检测网络（如 **CASENet**, Yu et al., CVPR 2017）之上，无需修改主干网络。

### 边界细化层与 NMS 损失

边界细化层的目标是强制网络在真实边界像素处沿法线方向产生最大响应，从而抑制“过厚”的边界预测。其操作流程如下：

1. 对于主干网络输出的第 $k$ 类边界概率图 $f_k(m|\mathbf{x},\theta)$，在每个边界像素 $p$ 处计算其法线方向。
2. 沿法线方向在 $p$ 两侧各采样 $L$ 个点（$L=2$，共 5 个点），记为 $\{p_t\}_{t=-L}^{L}$。
3. 对这 5 个位置的响应进行 softmax 归一化，得到细化后的概率分布：

$$h_k(p|\mathbf{x},\theta) = \frac{\exp(f_k(p|\mathbf{x},\theta)/\tau)}{\sum_{t=-L}^{L} \exp(f_k(p_t|\mathbf{x},\theta)/\tau)}$$

其中 $\tau=0.1$ 为温度参数，控制 softmax 的锐度。

**NMS 损失** 直接约束该分布趋近于独热分布，使真实边界像素 $p$ 的响应最大化：

$$\mathcal{L}_{nms}(\theta) = - \sum_k \sum_p \log h_k(p|\mathbf{x},\theta)$$

### 方向损失

为进一步保证边界方向的精确性，引入**方向损失**，惩罚预测边界法线 $\vec{e}_p(\theta)$ 与真实法线 $\vec{d}_p$ 之间的角度偏差：

$$\mathcal{L}_{\mathrm{dir}}(\theta) = \sum_k \sum_p || \cos^{-1} \langle \vec{d}_p, \vec{e}_p(\theta) \rangle ||^2$$

### 基础分类损失

沿用语义边界检测的标准**加权二元交叉熵损失**，通过权重 $\beta$ 平衡正负样本：

$$\mathcal{L}_{BCE}(\theta) = - \sum_k \sum_m \{ \beta y_k^m \log f_k(m|\mathbf{x},\theta) + (1-\beta)(1-y_k^m) \log(1 - f_k(m|\mathbf{x},\theta)) \}$$

### 组合损失

最终训练损失为上述三项的加权组合：

$$\mathcal{L} = \alpha_1 \mathcal{L}_{BCE} + \alpha_2 \mathcal{L}_{nms} + \alpha_3 \mathcal{L}_{dir}$$

在 SBD 实验中，常用权重为 $\alpha_1=1, \alpha_2=10, \alpha_3=1$。

### 主动对齐

主动对齐模块在训练过程中迭代优化带噪声的标注，使其向网络预测的高置信区域靠拢。其核心是一个联合优化问题：

$$\min_{\hat{\mathbf{y}},\theta} \mathcal{L}(\hat{\mathbf{y}},\theta) = -\sum_k \left( \log P(\mathbf{y}_k|\hat{\mathbf{y}}_k) + \log P(\hat{\mathbf{y}}_k|\mathbf{x};\theta) \right)$$

其中 $\hat{\mathbf{y}}_k$ 为推断的潜在精确边界，$\mathbf{y}_k$ 为原始噪声标注。第一项驱动推断曲线向网络高置信区域移动，第二项保证推断曲线与原始标注的拓扑一致性。

该优化通过**水平集演化**实现。定义曲线能量：

$$E(\mathbf{y}_k | \hat{\mathbf{y}}_k, \lambda) = \int g_k(\hat{\mathbf{y}}_k(q)) |\hat{\mathbf{y}}_k'(q)| \partial q$$

其中 $g_k$ 为基于网络预测的引导函数。对应的水平集演化 PDE 为：

$$\frac{\partial \phi}{\partial t} = g_k (\kappa + c) |\nabla \phi| + \nabla g_k \cdot \nabla \phi$$

其中 $\phi$ 为嵌入函数，$\kappa$ 为曲率项，$c$ 为常速度项（用于避免局部极小值）。演化 $t$ 步后，将水平集的零水平集作为精化后的伪标签。

### 粗到精细化（推理阶段）

在推理阶段，给定一个粗分割掩码，可利用训练好的网络和水平集演化（设 $\lambda=0, c=1$）进行 $t$ 次迭代，使掩码边界与网络预测的语义边界对齐，从而生成精化掩码。该过程无需额外训练。

## 实验与分析

### 核心实验设计逻辑

本章的实验围绕一个根本瓶颈展开：**当前语义边界数据集（以SBD为代表）存在显著的标注噪声**，导致学习到的边界预测过厚且不精确，而标准交叉熵损失未显式处理边界对齐问题。为验证所提方法的有效性，作者设计了三个层次的实验：**主结果对比**（在高质量重标注测试集上验证边界精度提升）、**消融实验**（解耦NMS损失与主动对齐的贡献，并测试对标注噪声的鲁棒性）、以及**下游任务迁移**（粗标注分割掩码的精化与Cityscapes跨域验证）。

---

### 主结果：SBD高质量重标注测试集

由于SBD原始测试集标注质量较低（边界误差约4px），作者委托专业标注团队对SBD测试集进行了高质量重标注，并以此作为核心评测基准。**Table 1** 给出了在该重标注测试集上与主流方法的全面对比。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_1904_07934/figures/003_Table_1.jpg]]
*Table 1: Comparison of our method in the re-annotated SBD test set vs state-of-the-art. Scores are measured by %*

以CASENet（Yu et al., CVPR 2017）为backbone，STEAL（NMS Loss + Active Alignment）将MF(ODS)从63.52%提升至**68.15%**（+4.63%），AP更是从约43.96%跃升至**62.57%**（+18.61%）。这一AP的巨幅提升直接反映了边界细化层对预测“厚度”的抑制效果——AP指标对边界定位精度极为敏感，粗边界会因无法匹配严格阈值而大幅失分。

与同期最优方法SEAL（Yu et al., ECCV 2018）相比，STEAL在MF(ODS)上领先约1.5%，在AP上领先超过3%。值得注意的是，**仅加入NMS损失层（无主动对齐）即可在MF(ODS)和AP上超越SEAL**（Table 3），这表明直接优化边界法线方向的局部响应，比SEAL中复杂的图匹配对齐策略更为有效。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_1904_07934/figures/005_Table_2.jpg]]
*Table 2: Results on SBD test following the original evaluation protocol, and test set from [15]. Table 3: Effect of the NMS Loss and Active Alignment on the SBD dataset. Score (%) represents mean over all classes*

在SBD原始测试集（含噪声标注）上，STEAL同样取得75.6%的MF(ODS)，优于CASENet的约71.88%（Table 2），证明方法在常规评测协议下依然稳健。

---

### 消融实验：NMS损失与主动对齐的解耦

**Table 3** 系统消融了NMS损失层和主动对齐的独立贡献。以CASENet为基线，加入NMS损失层后MF(ODS)和AP均有显著提升；在此基础上再引入主动对齐，MF(ODS)进一步提升至68.15%，AP达到62.57%。这表明两条途径具有互补性：**NMS损失在局部约束边界法线方向的最大响应，主动对齐则在全局层面迭代修正标注偏差**。

**Table 4** 进一步揭示了主动对齐的核心价值场景：当训练数据标注质量较差时，其增益尤为显著。在模拟8px标注噪声的SBD训练集上，仅使用NMS损失层的MF(ODS)为46.26%；加入主动对齐后跃升至**56.41%**（+10.15%），AP从28.84%提升至43.97%。而在高质量训练集上，主动对齐的增益则相对有限。这一结果直接验证了主动对齐的设计初衷——**从粗标注中学习细边界**。

方向损失（Direction Loss）的消融在Table 3中隐含体现：NMS损失与方向损失共同作用时，边界对齐精度优于单独使用NMS损失，方向损失通过惩罚预测法线与真实法线的角度偏差，进一步强化了边界方向的几何一致性。

---

### 跨域验证：Cityscapes数据集

在Cityscapes验证集上（Table 5, Figure 5），STEAL取得了71.42%的AP。与从DeepLab v3+（Chen et al., ECCV 2018）分割掩码中提取的边界相比，STEAL在严格匹配阈值下性能高出**4.2%**（Figure 5）。这一对比极具说服力，因为它直接证明：**专门学习语义边界比从分割掩码中后处理提取边界更为精确**，尤其是在需要亚像素级定位的严格评估条件下。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_1904_07934/figures/007_Figure_4.jpg]]
*Figure 4: Active Alignment. From Left-to-right (GT, Refined). Table 5: Results on the val set on the Cityscapes dataset. Training is done using the finely annotated train set. Scores are measured by %*

---

### 下游应用：粗标注分割掩码精化

STEAL的粗到精细化能力在两个数据集上得到验证。在SBD上（Table 6），模型在含约4px噪声的训练集上训练后，对模拟的16px和32px误差粗标注进行精化，IoU提升分别超过**20%和30%**。在Cityscapes的coarse标注集上（Table 7, Figure 6），使用STEAL精化后的粗标注训练DeepLab v3+，在rider、truck、bus等类别上IoU提升超过**1.2%**，整体mIoU从80.37%提升至80.55%（+0.18%）。虽然绝对增益看似不大，但考虑到Cityscapes fine标注本身质量已经很高，这一提升表明**边界精化能为语义分割带来一致且非平凡的改进**。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_1904_07934/figures/010_Table_6.jpg]]
*Table 6: Refining coarse labels on SBD. Model is trained on the noisy SBD training set (approx 4px error). The re-annotated test set is then simplified to simulate coarse data with a given quality (see main text). Score (%) represents mean over all the 20 object classes. Table 7: Refining coarse labels on Cityscapes. Model trained on fine Cityscapes trainset and used to refine coarse data. Real Coarse corresponds to coarsely human annotated val set, while x-px error correspond to simulated coarse data. Score (%) represents mean over all 8 object classes*

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_1904_07934/figures/011_Figure_6.jpg]]
*Figure 6: Semantic Segmentation on Cityscapes val: Performance of DeepLab V3+ when trained with fine data and (blue) vanilla train extra set, (orange) our refined data (8 object classes) from train extra. We see improvement of more than 1.2 IoU % in rider, truck and bus*

---

### 定性分析

Figure 3展示了STEAL预测边界与CASENet及Ground Truth的视觉对比，STEAL的边界明显更细、更连续，且对语义类别区分更准确。Figure 4展示了主动对齐过程中标注从粗到细的演化，可见经过数次迭代后，标注曲线从偏离真实边界的粗糙轮廓逐步收敛到紧贴物体边缘的精确位置。Figure 8展示了Cityscapes coarse标注的精化效果，精化后的掩码在物体轮廓处与图像边缘高度吻合。

---

### 失败模式与局限

论文未明确报告失败案例。但从方法机理可推断以下潜在脆弱点：
- **拓扑错误不可恢复**：当标注存在严重拓扑错误（如漏标整个物体区域）时，水平集演化无法凭空生成新的边界拓扑，主动对齐可能失效。
- **超参数敏感性**：损失权重α₁=1, α₂=10, α₃=1在SBD上经验设定（Part 006），其在不同数据集上的迁移需要手动验证。
- **计算开销**：主动对齐需在训练中周期性执行水平集演化，虽然作者指出可每n次迭代执行一次以节省计算（Part 006），但在实时或移动端场景中仍构成额外负担。

### 补充图表

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_1904_07934/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative Results on the Cityscapes Dataset*

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_1904_07934/figures/013_Figure_8.jpg]]
*Figure 8: Qualitative Results. Coarse-to-Fine on the coarsely annotated Cityscapes train extra set*

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_1904_07934/figures/004_Table_4.jpg]]
*Table 4: Effect of Active Alignment on the SBD dataset. Score (%) represents mean over all classes*

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_1904_07934/figures/009_Table.jpg]]

## 方法谱系与知识库定位

### 核心基线定位

STEAL 建立在两条关键基线之上：

- **CASENet** (Yu et al., CVPR 2017)：作为主干网络和主要对比基线。CASENet 通过多尺度特征融合实现类别感知的语义边界检测，其训练仅使用加权二元交叉熵损失（BCE），未显式建模边界的空间形状约束。在高质量重新标注的 SBD 测试集上，CASENet 的 MF(ODS) 为 63.52%，AP 约 43.96%。

- **SEAL** (Yu et al., ECCV 2018)：当时最先进的语义边界对齐方法，通过图匹配在训练中优化标注与预测之间的对应关系。STEAL 仅应用 NMS 损失层即可在 MF(ODS) 和 AP 上超越 SEAL 超过 1%，表明直接优化边界法线方向的局部约束比复杂的图匹配对齐更有效（Table 1）。

### 方法谱系中的独特位置

STEAL 在语义边界检测方法谱系中占据一个独特位置，其核心贡献并非提出新的主干架构，而是通过**即插即用的损失层与训练框架**解决现有数据集的标注噪声问题。这使其区别于以下两类工作：

1. **纯架构改进类**：如 CASENet 等聚焦于多尺度特征融合或类别关联建模的方法。STEAL 可以与任意此类主干网络结合，在不改变网络结构的前提下提升边界清晰度。

2. **后处理细化类**：如从分割掩码中提取边界（例如 DeepLab v3+ 边缘提取，Chen et al., ECCV 2018）。STEAL 在 Cityscapes val 上直接预测的边界在严格匹配阈值下比 DeepLab v3+ 分割掩码提取的边缘高 4.2%（Fig. 5），证明端到端学习边界优于从分割结果后处理。

### 关键技术谱系

STEAL 的两条互补途径分别对应不同的技术传统：

- **NMS 损失与边界细化层**：继承自边缘检测中非极大值抑制的思想，但将其可微化并嵌入训练过程。通过在边界法线方向（采样 5 个位置，L=2）进行 softmax 归一化（τ=0.1），强制真实边界像素获得最大响应。这与传统的后处理 NMS 或基于图匹配的对齐（如 SEAL）形成对比——前者不可微，后者计算复杂。

- **主动对齐框架**：借鉴水平集方法与测地线活动轮廓的思想，将其改造为训练时的标注迭代优化机制。通过联合优化潜在精确边界 ŷ 和网络参数 θ（Eq. 8），利用曲线能量（Eq. 9）鼓励推断曲线位于网络高置信区域。形态学水平集实现（二值分段常数函数，无需重新初始化）保证了计算稳定性和效率。

### 适用边界与局限

**已验证的适用场景**：
- 训练标注存在中等程度噪声（4px–8px 误差）的语义边界检测任务。在模拟 8px 标注噪声的 SBD 训练集上，主动对齐使 MF(ODS) 从 46.26% 提升至 56.41%（Table 4）。
- 粗标注分割掩码的自动精化：在 SBD 上，对 16px 和 32px 误差的粗标注，精化后 IoU 提升超过 20% 和 30%；在 Cityscapes 上，精化后的 train extra 数据使 DeepLab v3+ 在 rider、truck、bus 类别上提升超过 1.2% IoU（Fig. 6）。

**已知局限与开放问题**：
- **标注噪声容忍极限未知**：当标注拓扑严重错误（如对象边界完全错位或缺失）时，主动对齐是否能恢复正确边界尚未验证。
- **超参数敏感性**：损失权重 α₁=1, α₂=10, α₃=1 在 SBD 上有效，但跨数据集的泛化策略和调参成本未系统分析。
- **计算效率**：主动对齐需在训练中周期性执行水平集演化（可在网络精度趋于平稳后引入，或每 n 次迭代执行一次以节省计算），在移动端或实时系统中，仅使用 NMS 损失（无主动对齐）可能是更实际的选择，但性能会有所下降。
- **任务迁移性**：边界细化层和主动对齐是否可迁移到深度边界估计、实例分割边缘等像素级预测任务，尚待验证。
- **粗到精细化与人工精修的定量比较**：论文未提供精化效率与质量相对于人工精修的定量对比。

## 原文 PDF

![[paperPDFs/CVPR_2019/Devil_is_in_the_Edges_Learning_Semantic_Boundaries_from_Noisy_Annotations.pdf]]
