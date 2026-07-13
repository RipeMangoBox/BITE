---
title: "Learning Smooth Neural Functions via Lipschitz Regularization"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Learning_Smooth_Neural_Functions_via_Lipschitz_Regularization.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/lip-mlp/
aliases:
- LMLPLLB
- LSNFLR
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "可学习的每层Lipschitz上界（softplus(c_i)），配合∞-范数权重行归一化和乘积形式的正则化项，使网络在整个隐空间（含训练集之外）具备平滑性，且无需预定义全局Lipschitz常数。"
primary_logic: "将网络的Lipschitz常数视为可学习参数，并惩罚其乘积（即整体Lipschitz界），既自适应学习各任务所需的平滑度，又通过乘积形式正确处理了Lipschitz界随网络深度指数增长的特性，避免了深度变化时需重新调参。"
claims:
- "标准MLP在插值/外推时出现明显不光滑（Fig.1红），而Lipschitz MLP提供平滑结果（蓝）。"
- "Dirichlet能量仅在采样时间步产生光滑解，但在未采样区间产生突变（Fig.2），证明采样式正则化不足。"
- "谱范数正则化对网络深度敏感（Fig.4红），而所提方法对深度变化一致（蓝）。"
- "所提方法在测试时优化中，Chamfer距离从0.0343降至0.0013，Hausdorff距离从0.3441降至0.1270（Table 2）。"
---

# Learning Smooth Neural Functions via Lipschitz Regularization

> [!tip] 核心洞察
> 将网络的Lipschitz常数视为可学习参数，并惩罚其乘积（即整体Lipschitz界），既自适应学习各任务所需的平滑度，又通过乘积形式正确处理了Lipschitz界随网络深度指数增长的特性，避免了深度变化时需重新调参。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过Lipschitz正则化学习光滑神经函数 |
| 英文题名 | Learning Smooth Neural Functions via Lipschitz Regularization |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2202.08345) · [Project](https://research.nvidia.com/labs/toronto-ai/lip-mlp/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Lipschitz MLP with learnable per-layer Lipschitz bounds |
| Dataset | MNIST SDF autoencoder (Jacobian smoothness), ShapeNet chairs (test-time optimization, partial-to-full shape) |

> [!tip] 效果简介
> - MNIST SDF autoencoder (Jacobian smoothness) 上，mean ||J||^2 为 1.009，对比 Vanilla: 1.021; L1: 1.016; L2: 1.020，变化 −0.012 vs Vanilla。
> - MNIST SDF autoencoder (Jacobian smoothness) 上，max ||J||^2 为 9.419，对比 Vanilla: 23.658; L1: 17.361; L2: 21.181，变化 −14.239 vs Vanilla。
> - ShapeNet chairs (test-time optimization, partial-to-full shape) 上，Chamfer distance (mean, lower better) 为 0.0013，对比 DeepSDF: 0.0343，变化 −0.033。

## 概要

**问题瓶颈**：神经隐式场（neural fields）在隐空间插值与外推时产生不光滑结果，根源在于现有平滑正则化策略存在结构性缺陷。Dirichlet能量仅在采样点施加平滑约束，无法保证未观测区域的全局平滑（Fig. 2）；基于谱归一化的Lipschitz约束方法（如**Yoshida & Miyato, 2017**）则要求预先设定全局Lipschitz常数，而几何应用中合适的常数未知，导致每任务需大量调参，且对网络深度高度敏感（Fig. 4）。

**核心思路**：将网络的Lipschitz上界视为**可学习参数**并惩罚其乘积，而非预设固定常数。具体而言，为每层引入可学习参数 $c_i$，通过 $\mathrm{softplus}(c_i)$ 作为该层Lipschitz上界，配合 $\infty$-范数行归一化保证 $\|\widehat{\mathsf{W}}_i\|_\infty \leq \mathrm{softplus}(c_i)$，最终以乘积形式 $\alpha \prod_i \mathrm{softplus}(c_i)$ 作为正则项加入损失函数。这一设计同时解决了两个关键问题：自适应学习各任务所需的平滑度，且乘积形式正确处理了Lipschitz界随网络深度指数增长的特性，避免深度变化时重新调参。

**方法定位**：所提**Lipschitz MLP**属于隐式神经表示的正则化方法，与谱归一化（**Miyato et al., 2018**）、1-Lipschitz网络（**Anil et al., 2019**）等约束方法形成对比。其独特之处在于将Lipschitz常数从超参数转化为可优化变量，仅需在标准MLP中添加权重归一化层和额外损失项，即可部署于各类神经场架构（如DeepSDF、Occupancy Networks）。

**主要结果**：
- **定性**：在形状插值与外推任务上，Lipschitz MLP产生平滑过渡，而标准MLP出现明显突变（Fig. 1）。
- **定量（雅可比平滑度）**：在MNIST SDF自编码器上，最大雅可比范数从23.658降至9.419，平均范数亦有显著改善（Table 1）。
- **定量（形状补全）**：在ShapeNet椅子类别的测试时优化中，Chamfer距离从0.0343降至0.0013，Hausdorff距离从0.3441降至0.1270（Table 2）。
- **鲁棒性**：对潜空间对抗攻击的响应幅度约为普通自编码器的一半（Sec. 5.1），且正则化强度 $\alpha$ 对网络深度变化不敏感（Fig. 4）。

**局限性**：方法仅鼓励平滑插值，无法从少量形状中提取高级语义信息（Fig. 9）；训练时归一化层引入轻微计算开销；正则化强度 $\alpha$ 虽比固定Lipschitz常数更鲁棒，仍需针对任务选择（Fig. 16）。



### 神经隐式场与隐空间平滑性

近年来，神经隐式场（neural implicit fields）已成为表示三维几何形状的主流方法，它将形状编码为以空间坐标和低维隐码（latent code）为输入的神经网络。通过改变隐码，网络可以生成不同形状，从而实现形状插值、外推和编辑等应用。这类任务的核心前提是网络输出对隐码的变化是**平滑**的——即隐空间的微小扰动只引起输出几何的微小变化，而非突变（Fig. 5）。

然而，标准的MLP在训练时仅拟合给定样本，并未对隐空间的全局行为施加约束。如 **Fig. 1** 所示，当使用标准MLP在圆环（t=0）和双圆环（t=1）之间插值时，中间隐码产生的结果出现明显的几何突变（红色），而光滑的插值结果（蓝色）需要额外的平滑性保证。

### 现有方法的根本缺陷

#### 1. 采样式正则化的局部性：Dirichlet能量

一种直观的平滑性促进手段是在损失函数中加入Dirichlet能量正则项，即在采样的隐码点上惩罚网络雅可比矩阵的范数：

$$\mathcal{T}(\theta) = \mathcal{L}(\theta) + \alpha \sum_j \| \frac{\partial f_\theta}{\partial \mathbf{t}}(\mathbf{x}, \mathbf{t}_j) \|^2$$

该方法的致命弱点是**仅在采样点处施加平滑约束**。如 **Fig. 2** 所示，在猫形和圆形SDF之间插值时，若仅在t=1/3和t=2/3处施加Dirichlet正则，网络虽能在这些采样时间步上找到光滑解，但在采样点之间的区间（如0≤t≤1/3）仍会出现非均匀的突变。这说明采样式正则化无法保证隐空间的全局平滑性。

#### 2. Lipschitz约束方法的常数预设困境

另一类方法通过约束网络的Lipschitz常数来保证全局平滑性。对于使用1-Lipschitz激活函数的全连接网络，其整体Lipschitz常数可由各层权重矩阵范数的乘积上界估计：

$$c = \prod_{i=1}^{L} \| \mathsf{W}_i \|_{\mathcal{P}}$$

基于此，**谱归一化**（Miyato et al., 2018）和**1-Lipschitz网络**（Anil et al., 2019）等方法通过强制各层权重矩阵的范数来限制整体Lipschitz常数。然而，这些方法要求**预先设定目标Lipschitz常数**。在几何应用中，合适的常数是未知的——如 **Fig. 3** 所示，不同插值任务所需的平滑程度截然不同：同一个预设常数可能对一个任务足够（左上），对另一个任务则完全不足（左下）。这意味着每任务需大量调参，实用性极差。

#### 3. 谱范数正则化对网络深度的敏感性

**谱范数正则化**（Yoshida & Miyato, 2017）通过对各层权重矩阵的最大奇异值平方求和来间接限制Lipschitz常数：

$$\mathcal{T}(\theta) = \mathcal{L}(\theta) + \alpha \sum_{i=1}^l \| \mathsf{W}_i \|_{\mathcal{P}}^2$$

但该形式**未考虑Lipschitz常数随网络深度指数增长**的特性。如 **Fig. 4** 所示，使用相同的正则化强度α时，5层和10层MLP的效果截然不同（红色），因为求和形式的惩罚无法正确应对深度增加时Lipschitz界的指数放大效应。这导致网络深度变化时需重新调参，缺乏一致的行为。

### 核心动机与设计目标

综上，现有方法面临三重困境：

1. **Dirichlet能量**仅在采样点局部平滑，无法保证全局；
2. **Lipschitz约束网络**需要预设未知的目标常数，每任务调参繁重；
3. **谱范数正则化**对网络深度敏感，深度变化时行为不一致。

本文的核心动机是设计一种**无需预设全局Lipschitz常数、对网络深度不敏感、且能在整个隐空间（含训练集之外）保证平滑性**的正则化方法。关键洞察是：将网络的Lipschitz常数视为**可学习参数**，并惩罚其**乘积**形式的上界，既自适应学习各任务所需的平滑度，又正确处理了Lipschitz界随深度指数增长的特性。



## 核心方法与创新机理

本工作的核心创新在于将神经网络的 **Lipschitz 常数从预设超参数转变为可学习参数**，并配套设计了与之自洽的权重归一化与正则化策略，从而系统性地解决了现有方法在神经场隐空间平滑性上的根本困境。

### 瓶颈：现有平滑性正则化的结构性缺陷

神经场（Neural Fields）在隐空间中的平滑性对形状插值、外推和测试时优化至关重要。然而，现有方法存在两类结构性缺陷：

- **采样式正则化的局部性**：Dirichlet 能量正则化仅在采样的隐码点处约束雅可比范数（Eq. 7），网络可以在未采样区间产生突变，无法保证全局平滑（Fig. 2 明确展示了这一失效模式）。
- **Lipschitz 约束的预设依赖**：谱归一化（Miyato et al., 2018）和 1-Lipschitz 网络（Anil et al., 2019）等方法要求预先指定全局 Lipschitz 常数。在几何应用中，合适的常数是未知的——不同任务需要不同的平滑度（Fig. 3），手动设定导致每任务大量调参。此外，谱范数正则化（Yoshida & Miyato, 2017）对各层权重矩阵的谱范数求和，未考虑 Lipschitz 界随网络深度指数增长的特性，导致同一正则化权重在不同深度下效果迥异（Fig. 4）。

### 因果机制：可学习的每层 Lipschitz 界与乘积形式正则化

本方法的核心因果旋钮是 **可学习的每层 Lipschitz 上界** $c_i$，通过 softplus 重参数化保证非负性：$\mathrm{softplus}(c_i)$。围绕这一机制，方法包含三个相互耦合的关键设计（changed slots）：

**1. 每层 Lipschitz 界（从固定值到可学习参数）**

| 对比维度 | Baseline 值 | 本文方案 |
|---------|------------|---------|
| 参数形式 | 固定常数（如手动设为 1.4）或通过谱范数间接约束 | 可学习参数 $c_i$，经 $\mathrm{softplus}(c_i)$ 重参数化 |
| 自适应能力 | 需针对每任务手动调参 | 训练中自动学习各任务所需平滑度 |

**2. 权重归一化（从谱归一化到 ∞-范数行归一化）**

为保证每层的实际 Lipschitz 界不超过 $\mathrm{softplus}(c_i)$，本文采用 **∞-范数行归一化**：对权重矩阵 $\mathsf{W}_i$ 的每一行，将其绝对行和缩放至不超过 $\mathrm{softplus}(c_i)$（Eq. 9）。与谱归一化相比，∞-范数归一化避免了幂迭代的计算开销，且通过范数等价关系 $\frac{1}{\sqrt{n}}\|\mathsf{M}\|_\infty \le \|\mathsf{M}\|_2 \le \sqrt{m}\|\mathsf{M}\|_\infty$（Eq. 5）间接约束了谱范数，同时使正则化对网络深度变化更加鲁棒（Fig. 4）。

**3. 正则化项（从求和到乘积）**

最终损失函数将任务损失 $\mathcal{L}(\theta)$ 与各层 Lipschitz 界的乘积相结合：

$$\boxed{\mathcal{I}(\theta, C) = \mathcal{L}(\theta) + \alpha \prod_{i=1}^l \mathrm{softplus}(c_i)}$$

这一乘积形式（Eq. 10）的正确性源于 MLP 的 Lipschitz 界可估计为各层权重矩阵范数的乘积 $c = \prod_{i=1}^{L} \|\mathsf{W}_i\|_{\mathcal{P}}$（Eq. 2）。与以下替代方案相比，乘积形式具有明确优势：

- **求和形式**（Yoshida & Miyato, Eq. 12）：$\alpha \sum \|\mathsf{W}_i\|_{\mathcal{P}}^2$ 对深度敏感（Fig. 4 红），因为 Lipschitz 界随深度指数增长而非线性增长。
- **全局 k 形式**（Anil et al., Eq. 11）：$\alpha k$ 将全局常数作为正则化目标，收敛性差（Fig. 6）。
- **直接权重乘积**（Eq. 13）：在宽网络上收敛较慢。
- **log-sum 形式**（Eq. 14）：可能导致无界优化。

乘积形式正确处理了 Lipschitz 界随深度的指数增长特性，使同一正则化权重 $\alpha$ 在不同深度下产生一致效果（Fig. 4 蓝），且训练后可通过对归一化权重矩阵的“拼装”（bricolage）消除测试时开销。

### 核心洞察总结

将网络的 Lipschitz 常数视为可学习参数并惩罚其乘积，既**自适应学习各任务所需的平滑度**，又通过乘积形式**正确处理了 Lipschitz 界随网络深度指数增长的特性**，避免了深度变化时需重新调参的根本问题。这一设计使得方法在形状插值/外推（Fig. 1）、测试时优化（Table 2，Chamfer 距离从 0.0343 降至 0.0013）和对抗鲁棒性（Table 1，最大雅可比范数从 23.658 降至 9.419）上均显著优于现有方法。



本方法的核心思想是**将网络的Lipschitz常数视为可学习参数，并惩罚其乘积形式的整体上界**，从而在整个隐空间（包括训练集之外）上获得平滑性，且无需预定义全局Lipschitz常数。

### 输入与任务设定

给定一个神经场 $f_\theta(\mathbf{x}, \mathbf{t})$，其中 $\mathbf{x}$ 为空间坐标，$\mathbf{t}$ 为条件隐码（latent code）。目标是使网络输出关于隐码 $\mathbf{t}$ 的变化保持Lipschitz连续，即满足：

$$\| f_{\theta}(\mathbf{t}_0) - f_{\theta}(\mathbf{t}_1) \|_{\mathcal{P}} \leq c \| \mathbf{t}_0 - \mathbf{t}_1 \|_{\mathcal{P}}$$

其中 $c$ 为Lipschitz常数。对于使用1-Lipschitz激活函数（如ReLU）的全连接网络，该常数可由各层权重矩阵范数的乘积上界估计：

$$c = \prod_{i=1}^{L} \| \mathsf{W}_i \|_{\mathcal{P}}$$

### Pipeline 模块架构

整个方法由三个紧密耦合的模块组成，插入标准MLP即可工作：

**1. 输入拼接（Input concatenation）**
将空间坐标 $\mathbf{x}$ 与隐码 $\mathbf{t}$ 拼接后送入MLP，这是神经场条件生成的通用做法。

**2. 可学习的逐层Lipschitz界（Learnable per-layer Lipschitz constants $c_i$）**
为网络每一层引入一个可学习参数 $c_i$，通过 $\mathrm{softplus}(c_i)$ 将其映射为正数，作为该层Lipschitz常数的上界。这些参数在训练过程中与网络权重联合优化。

**3. Lipschitz权重归一化层（Lipschitz weight normalization layer）**
对每一层的权重矩阵 $\mathsf{W}_i$ 执行行方向 $\infty$-范数归一化，保证归一化后的矩阵 $\widehat{\mathsf{W}}_i$ 满足 $\|\widehat{\mathsf{W}}_i\|_{\infty} \leq \mathrm{softplus}(c_i)$：

$$\mathbf{y} = \sigma( \widehat{\mathsf{W}}_i \mathbf{x} + \mathbf{b}_i ), \quad \widehat{\mathsf{W}}_i = \mathrm{normalization}( \mathsf{W}_i, \mathrm{softplus}(c_i) )$$

具体实现为将每行权重除以其绝对行和，再乘以 $\min(1, \mathrm{softplus}(c_i))$。选择 $\infty$-范数而非谱范数的原因在于：$\infty$-范数计算高效（无需幂迭代），且与谱范数之间存在范数等价关系（Eq. 5），在深度变化时表现更一致（Fig. 4）。

**4. Lipschitz正则化损失（Lipschitz regularization loss）**
在任务损失 $\mathcal{L}(\theta)$ 基础上，添加各层Lipschitz界乘积的正则项：

$$\boxed { \mathcal{I}(\theta, C) = \mathcal{L}(\theta) + \alpha \prod_{i=1}^l \mathrm{softplus}(c_i) }$$

乘积形式是关键设计：它正确处理了Lipschitz界随网络深度指数增长的特性，使得同一正则化强度 $\alpha$ 在不同深度的网络上产生一致效果（Fig. 4 蓝线），避免了深度变化时需重新调参的问题。

### 训练与部署流程

训练时，网络前向传播经过上述归一化层，损失函数同时优化任务目标和Lipschitz正则项。训练完成后，可通过**权重矩阵拼装（weight matrix bricolage）**将归一化操作显式固化到权重矩阵中，从而在测试时完全移除归一化层的计算开销。训练时添加归一化层会略微降低吞吐量（从265.83降至229.95 epochs/s），但部署时无额外开销。

### 关键设计选择与替代方案对比

该框架区别于以下基线方案的根本瓶颈：

- **Dirichlet能量正则化**（Eq. 7）：仅在采样的隐码点处施加平滑约束，无法保证采样点之间的全局平滑（Fig. 2）。
- **谱范数正则化**（Yoshida & Miyato, 2017，Eq. 12）：对各层权重矩阵范数的平方求和，未考虑指数增长特性，对网络深度敏感（Fig. 4 红线）。
- **固定k-Lipschitz架构**（Anil et al., 2019，Eq. 11）：将全局Lipschitz常数 $k$ 作为正则项，但收敛效果差于乘积形式（Fig. 6）。
- **谱归一化**（Miyato et al., 2018）：需预先设定Lipschitz界，而几何应用中合适的常数未知，微小调整即导致从“过平滑”到“欠平滑”的剧烈变化（Fig. 16）。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2202_08345/figures/007_Figure_6.jpg]]
*Figure 6: Our method converges to a smoother result compared to the $k ^ { - }$ Lipschitz architecture described in [Anil et al. 2019] (see $\mathsf { E q . }$ (11)). We use the same ?? for both networks because we both define the regularization as the raw Lipschitz constant of the network*

本方法的可学习乘积形式正则化在收敛性、深度鲁棒性和任务适应性上均优于上述替代方案（详见Sec. 4.2消融实验）。



### 核心思想

方法的关键思路是将网络的Lipschitz常数视为**可学习参数**并最小化它，而非预先设定一个固定值。由于Lipschitz上界 $c = \prod_i \|\mathsf{W}_i\|_p$ 仅依赖于权重矩阵，与输入无关，该方法通过在训练中同时学习各层的Lipschitz界 $c_i$ 并惩罚其乘积，自适应地为每个任务找到合适的平滑度。

### 模块一：可学习的逐层Lipschitz界

为每一层引入可学习参数 $c_i$，并通过softplus函数保证其正值性：

$$c_i \rightarrow \mathrm{softplus}(c_i) = \ln(1 + e^{c_i})$$

$\mathrm{softplus}(c_i)$ 代表第 $i$ 层的Lipschitz上界，在整个训练过程中随网络参数一同优化。

### 模块二：基于∞-范数的权重归一化层

为保证网络实际满足 $\|\widehat{\mathsf{W}}_i\|_\infty \leq \mathrm{softplus}(c_i)$，对每层权重矩阵执行行归一化：

$$\mathbf{y} = \sigma(\widehat{\mathsf{W}}_i \mathbf{x} + \mathbf{b}_i), \quad \widehat{\mathsf{W}}_i = \text{normalization}(\mathsf{W}_i, \mathrm{softplus}(c_i))$$

归一化操作将每行的绝对值之和限制在 $\mathrm{softplus}(c_i)$ 以内：若某行的绝对值之和超过该界，则按比例缩放该行；否则保持不变。选择∞-范数的原因在于其计算高效（无需幂迭代求奇异值），且与谱范数之间存在不等式关系：

$$\frac{1}{\sqrt{n}} \|\mathsf{M}\|_\infty \leq \|\mathsf{M}\|_2 \leq \sqrt{m} \|\mathsf{M}\|_\infty$$

这使得∞-范数归一化仍能有效约束谱范数，从而控制网络的整体Lipschitz常数。

训练完成后，可将归一化参数“烘焙”进权重矩阵 $\widehat{\mathsf{W}}_i$，部署时无额外计算开销。

### 模块三：乘积形式的Lipschitz正则化项

核心正则化损失函数为：

$$\boxed{\mathcal{I}(\theta, C) = \mathcal{L}(\theta) + \alpha \prod_{i=1}^{l} \mathrm{softplus}(c_i)}$$

其中：
- $\mathcal{L}(\theta)$ 为原始任务损失（如SDF重建损失）
- $\alpha$ 为正则化强度超参数
- $\prod_{i=1}^{l} \mathrm{softplus}(c_i)$ 为网络整体Lipschitz上界的估计
- $l$ 为网络层数

**乘积形式的关键优势**：Lipschitz界随网络深度呈指数增长，乘积形式正确捕捉了这一特性。对比之下，Yoshida & Miyato (2017) 的谱范数平方求和形式 $\mathcal{T}(\theta) = \mathcal{L}(\theta) + \alpha \sum_{i=1}^{l} \|\mathsf{W}_i\|_p^2$ 对网络深度敏感——同一 $\alpha$ 在5层和10层网络上效果迥异（Fig.4），而乘积形式在不同深度下表现一致。

### 与其他正则化形式的对比

| 正则化形式 | 公式 | 问题 |
|---|---|---|
| Anil et al. 全局k-Lipschitz | $\mathcal{T}(\theta, k) = \mathcal{L}(\theta) + \alpha k$ | 无法良好收敛（Fig.6） |
| Yoshida & Miyato 谱范数平方和 | $\mathcal{T}(\theta) = \mathcal{L}(\theta) + \alpha \sum \|\mathsf{W}_i\|_p^2$ | 对深度敏感（Fig.4） |
| 权重矩阵范数直接乘积 | $\mathcal{L}(\theta) + \alpha \prod \|\mathsf{W}_i\|_\infty$ | 宽网络上收敛较慢 |
| log-sum形式 | $\mathcal{L}(\theta) + \alpha \sum \ln(\mathrm{softplus}(c_i))$ | 大网络上优化无界 |
| **本文乘积形式** | $\mathcal{L}(\theta) + \alpha \prod \mathrm{softplus}(c_i)$ | 深度鲁棒、收敛稳定 |

### 输入拼接模块

网络 $f_\theta(\mathbf{x}, \mathbf{t})$ 将3D坐标 $\mathbf{x}$ 与隐码 $\mathbf{t}$ 拼接后输入MLP，Lipschitz正则化作用于隐码维度，使网络输出对隐码变化平滑。



## 实验与关键发现

### 核心瓶颈与实验设计逻辑

现有神经场方法在隐空间平滑性上存在根本缺陷：**Dirichlet能量**仅在采样点施加平滑约束，无法保证未采样区域的光滑性（Fig. 2）；**谱归一化**等Lipschitz约束方法需要预先设定全局Lipschitz常数，而几何应用中合适的常数未知，导致每任务需大量调参，且对网络深度高度敏感（Fig. 4）。本文方法将网络Lipschitz常数视为**可学习参数**，通过乘积形式的正则化项惩罚整体Lipschitz界，既自适应学习各任务所需平滑度，又正确处理了Lipschitz界随深度指数增长的特性。实验设计围绕三个核心验证目标展开：（1）所提方法是否在隐空间平滑性指标上显著优于现有正则化方法；（2）乘积形式的正则化是否比替代公式更有效；（3）平滑隐空间是否在下游任务（如测试时优化形状补全）中带来实际收益。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2202_08345/figures/002_Figure_2.jpg]]
*Figure 2: We fit a multilayer perceptron to fit the signed distance functions (SDFs) of a cat shape and a circle at ?? = 0 and ?? = 1 respectively. In addition, we minimize the Dirichlet energy of ?? at ?? = 1/3, 2/3. While the network finds a smooth solution at those sample time steps, it still has non-uniform change beyond the samples, such as between 0 ≤ ?? ≤ 1/3*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2202_08345/figures/003_Figure_4.jpg]]
*Figure 4: The spectral norm regularization proposed by Yoshida and Miyato [2017] is more sensitive to the number of layers. Therefore, using the same ?? on a 5-layer and a 10-layer MLP leads to different effects (red). In contrast, our regularization (blue) leads to more consistent results*

### 主实验结果

#### MNIST SDF自编码器：雅可比平滑性

在MNIST SDF自编码器任务上，直接通过反向传播计算网络雅可比矩阵的平方范数 $||J||^2$，以量化隐空间平滑性。**Table 1** 报告了所有训练数据的平均值和最大值：

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2202_08345/figures/011_Table_1.jpg]]
*Table 1: We compute the squared norm of the Jacobian matrix J via backpropagation. We report the average and the maximum value of the ∥J ∥2 for all training data and show that our Lipschitz regularization achieves a smoother solution compared to other weight decay methods*

| 方法 | 平均 $||J||^2$ | 最大 $||J||^2$ |
|------|---------------|----------------|
| Vanilla MLP（无正则化） | 1.021 | 23.658 |
| L1 权重衰减 | 1.016 | 17.361 |
| L2 权重衰减 | 1.020 | 21.181 |
| **Lipschitz MLP（本文）** | **1.009** | **9.419** |

本文方法在最大雅可比范数上从23.658降至9.419，降幅达60.2%，表明对隐空间中极端非平滑区域有显著抑制效果。平均范数亦为最低（1.009），证明整体平滑性优于所有权重衰减基线。值得注意的是，L1/L2权重衰减虽能略微改善平滑性，但远不如本文方法有效——这验证了直接约束Lipschitz界的必要性：权重衰减仅限制参数规模，无法针对性地控制函数输出的局部变化率。

#### ShapeNet椅子：测试时优化形状补全

在ShapeNet椅子数据集上进行部分点云到完整形状的测试时优化任务：给定来自测试集的真实点云，删除右半部分获得部分观测，然后优化隐编码重构完整形状。**Table 2** 报告了测试集平均Chamfer距离和Hausdorff距离：

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2202_08345/figures/017_Table_2.jpg]]
*Table 2: We quantitatively evaluate the test time optimization. Given a ground truth point cloud from the test set, we delete the right-half of the point to obtain a partial point cloud and then we perform test-time optimization to reconstruct the full shape back. We report the Chamfer distance and Hausdorff distance between the ground truth point cloud and our reconstructed full shape averaged across the test set*

| 方法 | Chamfer距离 ↓ | Hausdorff距离 ↓ |
|------|-------------|---------------|
| DeepSDF（Park et al., 2019） | 0.0343 | 0.3441 |
| **Lipschitz MLP（本文）** | **0.0013** | **0.1270** |

Chamfer距离从0.0343降至0.0013（降低96.2%），Hausdorff距离从0.3441降至0.1270（降低63.1%）。这一显著提升源于平滑隐空间的直接收益：当隐空间关于隐编码是Lipschitz连续的，测试时优化中的梯度信号更加稳定，优化器不易陷入局部极小值（如Fig. 5的toy实验所示）。**Fig. 11** 的定性结果进一步佐证了本文方法在部分观测下能重建出更完整、更合理的形状。

#### 隐空间对抗鲁棒性

在MNIST自编码器上进行隐空间对抗攻击实验：使用快速梯度符号法（FGSM, Eq. (15)）对隐编码施加扰动。Vanilla AE在攻击下SDF完全被破坏（平均SDF差异0.06，最大差异0.34），而Lipschitz正则化网络表现出更强鲁棒性（平均差异0.03，最大差异0.16）。**Fig. 8** 和 **Fig. 14** 的定性可视化显示，Vanilla AE的"0"字形在扰动后完全无法辨识，而本文方法保持了形状的基本结构。这验证了Lipschitz连续性天然提供对输入扰动的鲁棒性保证。

### 消融实验与替代公式对比

#### 乘积形式 vs. 替代正则化公式

本文在Sec. 4.2中系统比较了所提乘积正则化（Eq. 10）与四种替代方案：

1. **全局k-Lipschitz正则化（Anil et al., 2019, Eq. 11）**：将全局Lipschitz常数k作为正则项。**Fig. 6** 显示该方法收敛到较差的结果——因为k同时出现在网络约束和正则化项中，导致优化目标不一致。

2. **谱范数平方和（Yoshida & Miyato, 2017, Eq. 12）**：对各层权重矩阵谱范数的平方求和。**Fig. 4** 揭示了关键缺陷：该正则化对网络深度高度敏感，在5层和10层MLP上使用相同正则化强度α会产生截然不同的效果（红色），而本文方法在不同深度下表现一致（蓝色）。这是因为平方和形式未能反映Lipschitz界随深度指数增长的特性。

3. **权重矩阵范数直接乘积（Eq. 13）**：在更宽网络上收敛速度慢于本文的可学习参数形式。

4. **log-sum形式（Eq. 14）**：在大网络上可能导致不收敛。

这些消融实验有力证明了乘积形式正则化（Eq. 10）的设计合理性：通过可学习参数 $c_i$ 将每层Lipschitz界从权重矩阵中解耦，既保持了乘积形式对深度指数增长的正确建模，又避免了直接使用权重范数乘积的优化困难。

#### ∞-范数归一化的有效性

本文采用∞-范数行归一化（而非谱归一化）来约束每层Lipschitz界。**Fig. 4** 间接验证了该选择的合理性：使用∞-范数的本文方法对深度变化鲁棒，而依赖谱范数的方法（Yoshida & Miyato）则敏感。∞-范数归一化无需幂迭代计算最大奇异值，训练效率更高（尽管添加归一化层使训练速度从265.83降至229.95 epochs/s，Sec. 4.1.1）。**Fig. 16** 进一步表明，谱归一化（Miyato et al., 2018）对预设Lipschitz界极其敏感——微小的对数缩放即可导致从"过于平滑"到"过于非平滑"的剧烈变化，而本文方法对正则化强度α的变化更加鲁棒。

#### 与其他重参数化技术的兼容性

**Fig. 15** 展示了本文方法与Salimans & Kingma (2016)权重归一化的组合效果：单独使用权重归一化无法获得平滑插值结果（上行），但结合本文Lipschitz正则化后即可得到平滑插值（下行）。这表明所提方法可作为插件与其他重参数化技术协同工作。

### 定性结果：插值与外推

**Fig. 1** 的teaser实验展示了核心定性结果：在环面（t=0）到双环面（t=1）的SDF插值任务上，标准MLP产生严重非平滑结果（红色），而Lipschitz MLP提供平滑连续的中间形状（蓝色）。**Fig. 13** 展示了更多成对3D形状插值结果，**Fig. 10** 展示了仅用三个训练形状即可生成高质量新颖形状的少样本插值能力。方法亦适用于不同隐式表示：**Fig. 7** 展示了在占用网络（Occupancy Network, Mescheder et al., 2019a）上的平滑插值结果。

### 失败模式与局限性

1. **语义信息的缺失**：**Fig. 9** 明确展示了方法的根本局限——当在动物形状间插值时，中间结果可能不是"真实的动物"。方法仅鼓励几何平滑性，无法从少量形状中提取高级语义或结构信息。

2. **网络宽度的影响**：Sec. 4.2指出，对于更宽的网络，直接在权重矩阵上定义乘积形式正则化（Eq. 13）收敛较慢；log-sum形式（Eq. 14）在大网络上可能导致不收敛。本文的可学习参数设计缓解了此问题，但正则化强度α仍需针对不同任务选择（尽管比固定Lipschitz常数不敏感，Fig. 16）。

3. **训练开销**：添加归一化层使训练速度从265.83降至229.95 epochs/s（约13.5%的额外开销），但可通过训练后"权重矩阵拼装"（bricolage）在部署时消除该开销（Sec. 4.1.1）。

4. **范数策略的未探索空间**：当前仅使用∞-范数，entry-wise范数等其他策略可能更优，但留作未来工作（Sec. 4）。

### 公平性说明

为确保比较的公平性，所有基线方法和替代公式的正则化强度α均单独调参（Sec. 4.2）。本文方法的α在插值任务中固定为 $10^{-6}$，展示了跨任务的鲁棒性，而Lipschitz约束方法需要任务特定的界值选择（Fig. 3）。**Fig. 12** 验证了测试时优化结果对优化器选择（SGD vs Adam）不敏感。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2202_08345/figures/018_Figure_12.jpg]]
*Figure 12: In this simple toy example, test-time optimization using SGD gives us similar result compared to the one optimized with Adam (see Fig. 5)*



## 定位与知识库关联

### 1. 与基线方法的关系

本工作处于神经隐式场光滑性控制的交叉点，直接回应了三类基线方法的根本缺陷。

**采样正则化的不足：Dirichlet能量。** 最直接的对比来自对隐空间施加Dirichlet能量的做法（Eq. (7)）。该方法仅在采样点惩罚雅可比范数，导致函数在未采样区间出现突变（Fig. 2，猫与圆形的SDF插值在t=0到1/3之间不光滑）。我们的方法通过约束整个权重空间（与输入无关）的Lipschitz界，实现了全局光滑性保证，而非仅在采样点光滑。

**预设Lipschitz常数的约束网络。** 谱归一化（**Miyato et al., 2018**）和1-Lipschitz网络（**Anil et al., 2019**）要求预先指定全局Lipschitz常数k。在几何应用中，合适的k是未知的——Fig. 3显示同一k值对环面-双环面插值足够，但对另一任务不足。我们的可学习每层界c_i通过softplus(c_i)自适应学习各任务所需的光滑度，无需任务特定调参。

**谱范数正则化的深度敏感性。** **Yoshida & Miyato (2017)** 对各层权重矩阵的谱范数平方求和（Eq. (12)），但未考虑Lipschitz界随深度指数增长的特性。Fig. 4直接验证了该缺陷：相同正则化系数α在5层和10层MLP上产生截然不同的效果（红色），而我们的乘积形式（Eq. (10)）对深度变化保持一致性（蓝色）。

**与通用权重衰减的区别。** Table 1定量比较了L1/L2权重衰减（**Tikhonov, 1963; Tibshirani, 1996**）与我们的Lipschitz正则化：在MNIST SDF自编码器上，我们的最大雅可比范数平方仅为9.419，而Vanilla MLP为23.658，L1为17.361，L2为21.181，证明显式约束Lipschitz界比通用权重衰减更有效。

**与架构基线的集成。** 我们的方法作为即插即用模块，可与现有隐式场架构结合。在形状补全任务中，基于**DeepSDF**（**Park et al., 2019**）的架构添加Lipschitz正则化后，测试时优化的Chamfer距离从0.0343降至0.0013，Hausdorff距离从0.3441降至0.1270（Table 2）。Fig. 7进一步展示了在占用网络（**Mescheder et al., 2019**）上的适用性。

### 2. 方法谱系中的核心创新定位

本方法的独特贡献在于将网络的Lipschitz常数从预设超参数转变为可学习参数，并配套设计了乘积形式的正则化项。这一设计解决了两个深层矛盾：

- **自适应vs预设**：softplus(c_i)使每层界随任务自适应调整，避免了对全局常数k的手动设定（Fig. 3右 vs 左）。
- **深度不变性**：乘积形式∏ softplus(c_i)正确建模了Lipschitz界随深度的指数增长，使得同一α在不同深度网络上产生一致的光滑效果（Fig. 4蓝），而求和形式（Eq. 12）或直接惩罚全局k（Eq. 11）均无法保证此性质。

消融实验进一步验证了正则化形式的关键性：Anil等人的k-Lipschitz架构（Eq. 11）收敛到较差结果（Fig. 6）；直接对权重矩阵范数乘积正则化（Eq. 13）在宽网络上收敛慢；log-sum形式（Eq. 14）导致无界优化。这些失败案例反证了我们的softplus参数化+乘积正则化的必要性。

### 3. 适用边界与局限

**语义信息提取的缺失。** 本方法仅鼓励隐空间的光滑插值，无法从少量形状中学习高级语义结构。Fig. 9显示动物形状间的插值结果可能不现实——这是所有纯光滑性正则化的共同边界，需结合语义先验或更大规模训练数据。

**网络宽度的收敛问题。** 在更宽的网络上，直接对权重矩阵定义乘积正则化（Eq. 13）收敛较慢（Sec. 4.2），log-sum形式（Eq. 14）甚至不收敛。当前方案在中等宽度下表现良好，但向大规模网络的扩展需进一步验证。

**范数选择的未完全探索。** 当前仅使用∞-范数进行权重归一化（Eq. (9)），其与谱范数的等价性由式(5)保证。但entry-wise范数‖M‖_{P,q}等其他策略可能更优，留作未来工作（Sec. 4）。

**训练开销。** 添加归一化层使训练速度从265.83 epochs/s降至229.95 epochs/s（Sec. 4.1.1），但推理时可通过权重矩阵拼接（bricolage）移除该开销。

**正则化强度的选择。** 虽然α比固定Lipschitz常数对任务变化不敏感（Fig. 16），但仍需针对不同任务进行选择，尚未实现完全的自适应。

### 4. 开放问题

1. **最优范数策略**：entry-wise范数或其他矩阵范数是否能提供更好的光滑性-表达能力权衡？
2. **Wasserstein度量**：如何将Wasserstein距离纳入光滑性衡量，以改进形状插值的感知质量？
3. **与其他正则化的协同**：Lipschitz正则化与Dropout、噪声注入、早停等机制如何相互作用？
4. **语义光滑性**：能否在保持光滑隐空间的同时，从少量样本中学习高级结构或语义信息？
5. **跨领域泛化**：该方法在几何以外的任务（通用图像生成、分类对抗鲁棒性）上表现如何？Fig. 8的潜空间对抗攻击实验提供了初步证据（最大SDF差异从0.34降至0.16），但系统研究尚缺。
6. **大规模训练的稳定性**：对于极深或极宽网络，是否存在更稳定的替代形式以避免log-sum的发散问题？



## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Learning_Smooth_Neural_Functions_via_Lipschitz_Regularization.pdf]]
