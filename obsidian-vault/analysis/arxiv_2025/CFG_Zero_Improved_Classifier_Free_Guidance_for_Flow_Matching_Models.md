---
title: "CFG-Zero*: Improved Classifier-Free Guidance for Flow Matching Models"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arXiv_2025/CFG_Zero_Improved_Classifier_Free_Guidance_for_Flow_Matching_Models.pdf
project_link: null
code_link: https://github.com/
aliases:
- CZ
- CZICFGFMM
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入优化的无条件速度缩放因子 s 和对 ODE 求解初始步骤进行零初始化，校正了欠拟合模型的速度估计。
primary_logic: 当速度估计欠准确时，CFG 在 t=0 处的引导误差大，零速度反而是更准确的估计；此外，将条件速度投影到无条件速度上得到的缩放因子 s* 能够最小化 CFG 速度与真实速度的误差上界。
claims:
- 在 ImageNet-256 训练早期（10~160 epochs），使用零初始化的 CFG 在 FID、sFID 等指标上始终优于标准 CFG（Table 1）。
- 在 ImageNet-256 上，CFG-Zero* 在 IS、FID、sFID、Recall 上均优于 CFG、ADG、CFG++ 等基线（IS 258.87, FID 2.10, Recall 0.61）。
- 在高斯混合玩具示例中，CFG-Zero* 生成样本与目标分布的 JS 散度更低，且速度误差更小（Figure 3）。
- 用户研究显示 CFG-Zero* 在多个模型上的胜率均超过 CFG，SD3.5 上整体胜率 72.15%（Figure 5）。
---

# CFG-Zero*: Improved Classifier-Free Guidance for Flow Matching Models

> [!tip] 核心洞察
> 当速度估计欠准确时，CFG 在 t=0 处的引导误差大，零速度反而是更准确的估计；此外，将条件速度投影到无条件速度上得到的缩放因子 s* 能够最小化 CFG 速度与真实速度的误差上界。

| 字段 | 内容 |
|------|------|
| 中文题名 | CFG-Zero⋆：改进的流匹配模型无分类器引导 |
| 英文题名 | CFG-Zero*: Improved Classifier-Free Guidance for Flow Matching Models |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2503.18886) · [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CFG-Zero⋆ |
| Dataset | ImageNet-256, Lumina-Next |

> [!tip] 效果简介
> - ImageNet-256 (class-conditional) 上，IS↑ 258.87 vs 257.03 (CFG) (+1.84)。
> - ImageNet-256 上，FID↓ 2.10 vs 2.23 (CFG) (-0.13)；Recall↑ 0.61 vs 0.59 (CFG) (+0.02)。
> - Lumina-Next (T2I self-curated) 上，Aesthetic Score↑ 7.03 vs 6.85 (CFG) (+0.18)。

## 概要

**问题瓶颈**：在 Flow Matching 训练早期，模型的速度估计欠准确，导致标准无分类器引导（CFG）在 ODE 求解的第一步产生较大的引导误差——该误差甚至大于直接使用零速度。这使得样本在采样起始阶段偏离最优轨迹，损害生成质量。

**核心洞察**：当速度估计欠准确时，零速度反而是更接近真实速度的估计；同时，将条件速度投影到无条件速度上得到的优化缩放因子 $s^\star$ 能够最小化 CFG 速度与真实速度的误差上界。

**方法定位**：CFG-Zero⋆ 是一种即插即用的 Flow Matching 引导改进策略，包含两个关键组件：
- **优化尺度（Optimized Scale）**：通过投影计算 $s^\star = \frac{\mathbf{v}_t^{\theta}(x|y)^\top \mathbf{v}_t^{\theta}(x)}{\|\mathbf{v}_t^{\theta}(x)\|^2}$，替代标准 CFG 中固定为 1.0 的无条件速度缩放因子。
- **零初始化（Zero-Init）**：在 ODE 求解的前 $K$ 步（通常 $K=1$）将速度强制设为零，跳过初始不准的预测。

该方法与标准 CFG、**ADG**（Sadat et al., ICLR 2024）、CFG++ 等引导策略形成对比，在无需额外训练的前提下校正 Flow Matching 模型的采样行为。

**主要结果**：
- 在 ImageNet-256 类条件生成上，CFG-Zero⋆ 取得 IS 258.87、FID 2.10、Recall 0.61，全面优于标准 CFG（IS 257.03, FID 2.23）及其他基线（Table 2）。
- 在 Lumina-Next、SD3、SD3.5、Flux 等文本到图像模型上，Aesthetic Score 和 CLIP Score 均有稳定提升（Table 3），CompBench 的 Color、Shape、Texture 指标亦同步改善（Table 4）。
- 在 Wan-2.1 文本生成视频任务中，VBench 评估显示 Aesthetic Quality（+2.57）和 Imaging Quality（+2.73）等指标显著优于 CFG（Table 5）。
- 用户研究（76 名参与者）表明 CFG-Zero⋆ 在多个模型上的胜率均超过 CFG，SD3.5 上整体胜率达 72.15%（Figure 5）。
- 消融实验证实，零初始化和优化尺度缺一不可，且零初始化步数需根据模型调整（Table 6, 7）；训练早期增加零步有益，但模型收敛后效果减弱（Table 1, Figure A2）。

**局限与待验证问题**：CFG-Zero⋆ 的效果依赖模型欠拟合程度，充分训练后零初始化增益消失；零初始化步数 $K$ 需手动调节，缺乏自适应机制；方法主要在 Flow Matching 模型上验证，对传统扩散模型的泛化性尚未确认；对 CFG-distilled 模型（如 Flux）的影响需进一步分析。



### 问题背景：Flow Matching 与无分类器引导

流匹配（Flow Matching）模型通过构建从源分布到目标分布的概率路径来学习生成过程，其核心是训练一个速度场网络 $v_t^{\theta}$ 来逼近最优传输路径。与扩散模型类似，流匹配模型同样需要借助引导（guidance）机制来提升生成质量和对条件的遵从度。无分类器引导（Classifier-Free Guidance, CFG）是该领域最广泛采用的引导策略，其标准形式为：

$$\hat{v}_t^{\theta}(x|y) = (1-\omega) \cdot v_t^{\theta}(x|\varnothing) + \omega \cdot v_t^{\theta}(x|y)$$

其中 $\omega$ 为引导权重，$v_t^{\theta}(x|\varnothing)$ 和 $v_t^{\theta}(x|y)$ 分别为无条件速度和条件速度。CFG 通过线性组合条件与无条件预测来放大条件信号的影响，从而提升生成质量。

### 现有方法缺口：欠拟合模型的速度估计偏差

尽管 CFG 在扩散模型和流匹配模型中取得了显著效果，但其有效性高度依赖于模型速度估计的准确性。CFG-Zero⋆ 的核心观察在于：**当流匹配模型处于欠拟合状态时，CFG 在采样初始步骤（$t=0$）的速度预测存在严重偏差，其引导误差甚至大于直接使用零速度作为估计**。这一现象可从以下不等式得到形式化刻画：

$$\|\widetilde{\mathbf{v}}_0^{\theta}(\mathbf{x}|\mathbf{y}) - \mathbf{v}_0^*(\mathbf{x}|\mathbf{y})\|_2^2 \geq \|\mathbf{0} - \mathbf{v}_0^*(\mathbf{x}|\mathbf{y})\|_2^2$$

该不等式表明，在训练早期，模型输出的引导速度 $\widetilde{\mathbf{v}}_0^{\theta}$ 与真实速度 $\mathbf{v}_0^*$ 的 L2 误差，大于零速度与真实速度的误差。这意味着，**采样第一步使用模型预测反而会引入比“什么都不做”更大的偏差**，导致生成样本偏离最优轨迹。

现有方法（如 **ADG**，Sadat et al., ICLR 2024；CFG++）尝试通过自适应调整引导强度或修改引导公式来缓解过饱和等问题，但它们并未针对流匹配模型在欠拟合阶段的初始速度估计偏差进行专门设计。同时，这些方法并非专为 Flow Matching 范式定制，在流匹配模型上的表现可能不如预期。

### 本文动机：从速度校正到零初始化

基于上述观察，CFG-Zero⋆ 提出两个互补的改进策略：

1. **优化尺度（Optimized Scale）**：在 CFG 的标准速度组合中，无条件速度的缩放因子固定为 1.0。然而，当无条件速度估计不准确时，将其直接纳入引导公式会放大误差。CFG-Zero⋆ 引入一个优化的投影尺度 $s^*$，将条件速度投影到无条件速度上，以最小化引导速度与真实速度之间的误差上界。

2. **零初始化（Zero-Init）**：对于 ODE 求解器的初始步骤，由于模型速度估计极不准确，CFG-Zero⋆ 直接将前 $K$ 步的速度强制设为零向量，跳过初始阶段的错误预测，让求解器从更稳定的后续步骤开始推进。

这两个策略共同构成了 CFG-Zero⋆，其核心动机在于：**在模型欠拟合阶段，通过校正速度估计和跳过不可靠的初始预测，使引导过程更稳定、更准确**。Figure 2 通过条件生成与 CFG 生成的对比，直观展示了标准 CFG 在欠拟合模型上的引导失效现象，为方法的提出提供了定性支撑。



## 核心方法与创新机理

CFG-Zero⋆ 的核心创新在于针对 Flow Matching 模型在训练早期（欠拟合阶段）速度估计不准确的问题，提出了两个互补且即插即用的改进模块：**优化尺度（Optimized Scale）** 与 **零初始化（Zero-Init）**。这两个模块分别从“校正速度方向”和“规避初始误差”两个角度，对标准无分类器引导（CFG）的速度组合公式进行了重构。

### 1. 优化尺度：从固定组合到投影校正

标准 CFG 的引导速度公式为：

$$\hat{v}_t^{\theta}(x|y) = (1-\omega) v_t^{\theta}(x|\varnothing) + \omega v_t^{\theta}(x|y)$$

其中无条件速度 $v_t^{\theta}(x|\varnothing)$ 的系数固定为 $(1-\omega)$。当模型欠拟合时，无条件速度与条件速度的方向可能严重不一致，直接线性组合会放大估计误差。

CFG-Zero⋆ 引入了一个可优化的缩放因子 $s$，将引导速度重写为：

$$\tilde{v}_t^{\theta}(x|y) = (1-\omega) \cdot s \cdot v_t^{\theta}(x) + \omega \cdot v_t^{\theta}(x|y)$$

关键在于 $s$ 并非手工设定的超参数，而是通过最小化引导速度与真实速度之间的误差上界推导出的最优投影尺度：

$$s^\star = \frac{\mathbf{v}_t^{\theta}(x|y)^\top \mathbf{v}_t^{\theta}(x)}{\|\mathbf{v}_t^{\theta}(x)\|^2}$$

这一公式的几何含义是：将条件速度投影到无条件速度方向上，得到在该方向上的最佳缩放系数。其理论依据在于，当模型速度估计存在偏差时，$s^\star$ 能够最小化 CFG 速度与真实速度误差的上界（见 Eq. (11) 及 Section 4.1 的推导）。在高斯混合玩具实验中（Figure 3），使用 $s^\star$ 的 CFG-Zero⋆ 在 JS 散度和速度误差两项指标上均显著优于标准 CFG，验证了该投影策略的有效性。

### 2. 零初始化：用零速度替代不可靠的初始预测

标准 CFG 在 $t=0$ 时刻直接使用模型预测的速度启动 ODE 求解器。然而，当模型欠拟合时，$t=0$ 处的速度估计误差极大——甚至大于直接使用零向量的误差。这一现象在论文中由以下不等式刻画：

$$\|\widetilde{\mathbf{v}}_0^{\theta}(\mathbf{x}|\mathbf{y}) - \mathbf{v}_0^*(\mathbf{x}|\mathbf{y})\|_2^2 \geq \|\mathbf{0} - \mathbf{v}_0^*(\mathbf{x}|\mathbf{y})\|_2^2$$

该不等式表明：在训练早期，模型在初始时刻的引导速度误差大于零速度误差，因此“不做预测”反而比“做错误预测”更优。

基于此洞察，CFG-Zero⋆ 提出 **零初始化（Zero-Init）**：在 ODE 求解的前 $K$ 步（通常 $K=1$），强制将速度预测设为零，跳过模型在初始时刻不可靠的估计。这一操作直接嵌入到 ODE 求解器的执行流程中（Algorithm 1），无需修改模型训练过程。

ImageNet-256 上的验证实验（Table 1）为该设计提供了关键证据：在训练 10~160 epochs 的欠拟合阶段，使用零初始化的 CFG 在 FID、sFID 等指标上始终优于标准 CFG；而当模型训练充分（>160 epochs）后，零初始化的增益消失甚至反转，印证了该策略与模型欠拟合程度之间的因果关系。

### 3. 协同机制

优化尺度与零初始化并非孤立运作，而是形成互补：
- **零初始化** 在采样初期直接规避了最严重的速度估计误差；
- **优化尺度** 在后续步骤中持续校正无条件速度的方向偏差。

消融实验（Table 6）表明，在 SD3.5 上，单独使用零初始化或单独使用优化尺度均不如完整的 CFG-Zero⋆ 组合，验证了两者的协同增益。



CFG-Zero⋆ 是一种面向 Flow Matching 模型的推理阶段引导增强方法，其整体流程由四个核心模块串联构成：**优化尺度计算**、**零初始化掩码**、**引导速度合成**以及**标准 ODE 求解器**。该方法不改变模型训练过程，仅在采样时对速度场进行轻量级校正。

**输入与输出流**：系统接收一个已训练的速度预测网络 $v^\theta$、一个从先验分布采样的噪声样本 $x_0$、引导权重 $\omega$ 以及零初始化步数 $K$。输出为一条从噪声逐步演化至目标分布的采样轨迹，最终产生符合条件约束的生成样本。

**模块关系**：在每一个 ODE 求解步的起始，系统首先调用**优化尺度计算模块**，利用当前条件速度 $v_t^\theta(x|y)$ 与无条件速度 $v_t^\theta(x)$ 计算最优投影尺度 $s^\star$（见 Eq. 11）。随后，**零初始化掩码模块**根据当前步索引判断是否处于前 $K$ 步：若是，则直接将速度强制置为零向量；否则保留模型预测的速度。接着，**引导速度合成模块**将（可能被掩码修改后的）无条件速度乘以 $s^\star$，再按照标准 CFG 的线性组合方式与条件速度混合，形成最终的引导速度 $\tilde{v}_t^\theta(x|y)$（见 Eq. 6）。最后，**ODE 求解器**（如中点法）依据该引导速度推进样本状态 $x_t$，完成一步积分。

**关键设计逻辑**：上述流程直接回应了 Flow Matching 训练早期模型速度估计不准确这一瓶颈。在 $t=0$ 附近，模型预测的引导速度误差甚至大于直接使用零速度（见 Eq. 12 所揭示的不等式关系），因此零初始化掩码通过截断前 $K$ 步的不可靠预测来避免样本偏离最优轨迹。同时，优化尺度 $s^\star$ 本质上是条件速度在无条件速度方向上的投影，它从理论上最小化了引导速度与真实速度之间误差的上界，从而在后续步中持续校正欠拟合模型的速度估计。两个模块协同作用：零初始化负责“止损”，优化尺度负责“纠偏”，共同使采样轨迹更紧密地贴合目标分布的真实流线。



### 3.1 问题背景：Flow Matching 中的标准 CFG

Flow Matching 模型通过条件流匹配损失训练一个速度场 $\mathbf{v}_t^{\theta}(\mathbf{x}_t|\mathbf{y})$：

$$
L_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \mathbf{x}_1} \left\| \mathbf{v}_t^{\theta}(\mathbf{x}_t | \mathbf{y}) - (\mathbf{x}_1 - \mathbf{x}_0) \right\|_2^2
$$

其中 $\mathbf{x}_t$ 沿线性概率路径 $p_t(\mathbf{x}|\mathbf{y}) = (1-t) \cdot p(\mathbf{x}|\mathbf{y}) + t \cdot q(\mathbf{x}|\mathbf{y})$ 插值。标准无分类器引导（CFG）在采样时组合条件速度与无条件速度：

$$
\hat{\mathbf{v}}_t^{\theta}(\mathbf{x}|\mathbf{y}) = (1-\omega) \mathbf{v}_t^{\theta}(\mathbf{x}|\varnothing) + \omega \mathbf{v}_t^{\theta}(\mathbf{x}|\mathbf{y})
$$

其中 $\omega$ 为引导权重。该公式隐式假设模型的速度估计在任意训练阶段都是准确的。

### 3.2 核心观察：训练早期的速度估计偏差

本文的核心洞察是：**当模型欠拟合时，CFG 在 $t=0$ 处的引导误差甚至大于直接使用零速度**。数学上表现为：

$$
\left\| \widetilde{\mathbf{v}}_0^{\theta}(\mathbf{x}|\mathbf{y}) - \mathbf{v}_0^*(\mathbf{x}|\mathbf{y}) \right\|_2^2 \geq \left\| \mathbf{0} - \mathbf{v}_0^*(\mathbf{x}|\mathbf{y}) \right\|_2^2
$$

其中 $\widetilde{\mathbf{v}}_0^{\theta}$ 为 CFG 引导速度，$\mathbf{v}_0^*$ 为真实最优速度。该不等式在训练早期的真实数据和玩具实验中均得到验证（Figure 3 右侧），揭示了一个此前被忽视的瓶颈：**标准 CFG 在初始步引入的误差会通过 ODE 积分累积，使生成样本偏离最优轨迹**。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/003_Figure_3.jpg]]
*Figure 3: Results on mixture of Gaussians in*

### 3.3 优化缩放因子 $s^*$

为校正无条件速度的估计偏差，CFG-Zero$^\star$ 在引导速度公式中引入一个可优化的标量缩放因子 $s \in \mathbb{R}_{>0}$：

$$
\tilde{\mathbf{v}}_t^{\theta}(\mathbf{x}|\mathbf{y}) = (1-\omega) \cdot s \cdot \mathbf{v}_t^{\theta}(\mathbf{x}) + \omega \cdot \mathbf{v}_t^{\theta}(\mathbf{x}|\mathbf{y})
$$

通过最小化引导速度与真实速度的误差上界，推导出 $s$ 的最优闭式解——条件速度在无条件速度方向上的投影：

$$
s^\star = \frac{\mathbf{v}_t^{\theta}(\mathbf{x}|\mathbf{y})^\top \mathbf{v}_t^{\theta}(\mathbf{x})}{\|\mathbf{v}_t^{\theta}(\mathbf{x})\|^2}
$$

**变量含义**：
- $\mathbf{v}_t^{\theta}(\mathbf{x}|\mathbf{y})$：条件速度预测（基于文本/类别条件）
- $\mathbf{v}_t^{\theta}(\mathbf{x})$：无条件速度预测（$\varnothing$ 条件）
- $s^\star$：最优投影尺度，当条件速度与无条件速度方向一致时趋近于 1，方向差异越大则偏离 1 越远

该缩放因子在推理时逐步计算，无需额外训练或梯度优化，计算开销可忽略。

### 3.4 零初始化（Zero-Init）

基于 $t=0$ 处引导误差大于零速度误差的观察，CFG-Zero$^\star$ 在 ODE 求解的最初 $K$ 步将速度强制设为零：

**算法流程**（Algorithm 1）：
1. 从噪声分布采样 $\mathbf{x}_0 \sim p_0$
2. 对前 $K$ 个时间步（通常 $K=1$），设置 $\tilde{\mathbf{v}} = \mathbf{0}$
3. 后续步骤使用优化缩放后的引导速度 $\tilde{\mathbf{v}}_t^{\theta} = (1-\omega) \cdot s^\star \cdot \mathbf{v}_t^{\theta}(\mathbf{x}) + \omega \cdot \mathbf{v}_t^{\theta}(\mathbf{x}|\mathbf{y})$
4. 标准 ODE 求解器（如中点法）根据校正后的速度推进样本

**关键参数**：$K$ 为零初始化步数，需根据模型和训练阶段调节。实验表明，SD3.5 对多步零初始化敏感（$K>1$ 导致性能下降），而 Lumina-Next 和 SD3 在前 7% 步零初始化时达到最佳（Table 7）。

### 3.5 模块协同机制

CFG-Zero$^\star$ 的两个核心模块——优化缩放 $s^\star$ 与零初始化——针对同一瓶颈的不同侧面：
- **零初始化**：直接规避 $t=0$ 处最严重的速度估计误差，防止初始偏差通过 ODE 积分放大
- **优化缩放**：在后续步骤中持续校正无条件速度的幅值和方向偏差，使引导速度更接近真实速度

两者协同作用：零初始化提供干净的起始点，优化缩放维持后续轨迹的准确性。消融实验（Table 6）证实，仅使用单一模块均不如完整组合，验证了协同的必要性。



## 实验与关键发现

### 核心瓶颈验证：训练早期速度估计不准确

CFG-Zero⋆ 的设计动机源于一个关键观察：在 Flow Matching 训练初期，模型的速度估计严重欠准确，导致标准 CFG 在采样第一步（t=0）产生的引导误差甚至大于直接使用零速度。**Table 1** 在 ImageNet-256 上系统验证了这一现象。在训练早期（10~160 epochs），使用零初始化的 CFG 在 FID、sFID 等指标上始终优于标准 CFG；而当模型训练到 160 epochs 之后，零初始化的优势消失甚至反转。这一转折点直接证实了“欠拟合模型的速度估计在初始步不可靠”这一核心瓶颈，并说明零初始化是一个与训练程度强相关的阶段性补救策略。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/004_Table_1.jpg]]
*Table 1: Validation on ImageNet-256. We evaluate a model at different training stages and observe a turning point at 160 epochs, where zero-init results in poorer performance when the model converges. This experiment validates that high-dimensional models also suffer from inaccuracies in initial sampling*

### 主实验结果

#### ImageNet-256 类别条件生成

**Table 2** 汇总了 ImageNet-256 上不同引导策略的对比。CFG-Zero⋆ 在所有指标上均优于标准 CFG、ADG 和 CFG++：

| 方法 | IS↑ | FID↓ | sFID↓ | Recall↑ |
|------|-----|------|-------|---------|
| Conditional Prediction (Baseline) | 239.80 | 3.78 | 5.74 | 0.53 |
| CFG | 257.03 | 2.23 | 4.71 | 0.59 |
| ADG | 256.41 | 2.11 | 4.60 | 0.60 |
| CFG++ | 256.72 | 2.07 | 4.62 | 0.60 |
| **CFG-Zero⋆** | **258.87** | **2.10** | **4.59** | **0.61** |

CFG-Zero⋆ 在 IS 上取得 258.87（+1.84 vs CFG），在 Recall 上达到 0.61（+0.02），表明其不仅提升了生成质量，还改善了模式覆盖。值得注意的是，ADG（Sadat et al., ICLR 2024）和 CFG++ 并非专为 Flow Matching 设计，在此范式下表现可能受限，但 CFG-Zero⋆ 仍以显著优势领先。

#### 文本到图像生成

**Table 3** 展示了在 Lumina-Next、SD3、SD3.5 和 Flux 四个主流 T2I 模型上的定量评估。CFG-Zero⋆ 在 Aesthetic Score 和 CLIP Score 两个维度上均一致优于 CFG：

- **Lumina-Next**：Aesthetic Score 7.03 vs 6.85（+0.18），CLIP Score 34.37 vs 34.09（+0.28）
- **SD3**：Aesthetic Score 6.78 vs 6.67（+0.11），CLIP Score 33.41 vs 33.28（+0.13）
- **SD3.5**：Aesthetic Score 6.92 vs 6.81（+0.11），CLIP Score 33.96 vs 33.83（+0.13）

**Figure 4** 提供了定性对比，CFG-Zero⋆ 生成的图像在色彩饱和度、细节保真度和文本一致性上均优于 CFG。在 T2I-CompBench 的组合性评估中（**Table 4**），CFG-Zero⋆ 在 Color（0.52 vs 0.51）、Shape（0.36 vs 0.34）和 Texture（0.45 vs 0.41）上均有提升，表明其对复杂文本条件的组合理解能力更强。

**Figure 5** 的用户研究进一步验证了主观偏好：在 SD3.5 上 CFG-Zero⋆ 的整体胜率达到 72.15%，在 Lumina-Next 和 SD3 上也均超过 60%。需注意该用户研究仅邀请 76 名参与者，规模有限，泛化性需进一步验证。对于 Flux 模型，由于其经过 CFG 蒸馏，直接应用 CFG 可能改变采样分布，本文在 Flux 上的实验仅作为参考。

#### 文本到视频生成

**Table 5** 报告了在 Wan-2.1 [1.3B] 模型上的 VBench 评估结果。CFG-Zero⋆ 在多个关键指标上显著优于标准 CFG：

- **Aesthetic Quality**：+2.57
- **Imaging Quality**：+2.73
- **Motion Smoothness**：+0.22
- **Dynamic Degree**：+2.67

这些提升表明 CFG-Zero⋆ 不仅改善了单帧质量，还增强了视频的整体流畅性。**Figure 6** 提供了定性对比，CFG-Zero⋆ 生成的视频在帧间一致性和视觉质量上明显更优。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative comparisons between CFG-Zero⋆ and CFG. Experiments are conducted using Wan-2.1 [1B] [39], under its recommended optimal sampling steps and guidance scale settings*

### 消融实验

#### 零初始化与优化尺度的独立贡献

**Table 6** 在 SD3.5 上分解了 CFG-Zero⋆ 两个核心组件的贡献。仅使用零初始化或仅使用优化尺度均能带来一定提升，但完整的 CFG-Zero⋆ 组合取得了最佳性能，证明两个组件具有互补性——零初始化解决初始步的速度估计偏差，优化尺度 s* 则校正后续步中无条件速度的方向偏差。

#### 零初始化步数 K 的敏感性

**Table 7** 揭示了零初始化步数 K 的模型依赖性。对于 SD3.5，超过 1 步的零初始化会导致性能下降；而 Lumina-Next 和 SD3 在零出前约 7% 的步数时达到最佳 Aesthetic Score 和 CLIP Score。**Figure A2** 进一步表明，在训练早期增加零初始化步数有益，但随着训练进行，更多零步反而有害。这说明 K 是一个需要针对模型和训练阶段手动调节的超参数，目前缺乏自适应选择机制。

#### 采样步数与引导尺度的鲁棒性

**Figure 7** 和 **Figure 8** 分别展示了在不同采样步数和引导尺度 ω 下 CFG-Zero⋆ 与 CFG 的对比。CFG-Zero⋆ 在所有配置下均保持更高的 CLIP Score 和 Aesthetic Score，表明该方法对这两个关键超参数具有良好的鲁棒性。

### 计算开销

**Table 8** 报告了 CFG-Zero⋆ 的计算成本。由于优化尺度 s* 的计算仅涉及向量内积和标量乘法，零初始化仅跳过前几步速度预测，额外开销极小。在 Wan-2.1 的 5 秒 720p 视频生成中，FLOPs 和 GPU 内存使用与标准 CFG 几乎持平，证明该方法在提升性能的同时保持了高度的计算效率。

### 失败模式与局限性

1. **训练充分后增益消失**：如 Table 1 所示，当模型训练超过 160 epochs 后，零初始化的优势消失。CFG-Zero⋆ 的效果依赖于模型欠拟合程度，对已充分收敛的模型提升有限。

2. **零初始化步数 K 需手动调节**：Table 7 显示不同模型对 K 的敏感性差异显著（SD3.5 仅容忍 1 步，而 Lumina-Next 可受益于更多步），缺乏统一的自动选择机制。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/014_Table_7.jpg]]
*Table 7: Ablation study on zero-out steps. For SD3.5 [5], more initial zero-out steps lead to worse performance, while Lumina-Next [45] and SD3 [5] achieve the highest Aesthetic Score and Clip Score with first 7% zero out*

3. **未在传统扩散模型上验证**：所有实验均基于 Flow Matching 模型（Lumina-Next、SD3/3.5、Wan-2.1），CFG-Zero⋆ 在 DDPM、EDM 等传统扩散范式上的有效性尚不明确。

4. **Flux 等 CFG-distilled 模型的特殊性**：Flux 经过 CFG 蒸馏，直接应用 CFG 可能改变其采样分布，CFG-Zero⋆ 在此类模型上的表现未作深入分析。

5. **用户研究规模有限**：76 名参与者的用户研究仅覆盖部分文本提示，可能存在选择偏差，主观偏好的泛化性需要更大规模验证。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/006_Table_2.jpg]]
*Table 2: Comparison of different guidance strategy on ImageNet-256 benchmark. Lower FID is better (↓) and higher IS is better (↑). Baseline here denotes using the conditional prediction only*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/005_Table_3.jpg]]
*Table 3: Quantitative evaluation of Text-to-Image generation, using Lumina-Next, Stable Diffusion 3, Stable Diffusion 3.5, and Flux. The evaluation is based on Aesthetic Score and CLIP Score as key metrics. Results indicate that CFG-Zero⋆ consistently enhances image quality and improves alignment with textual prompts across different models*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/010_Table_5.jpg]]
*Table 5: Qualitative evaluation on VBench [13]. We use the Wan-2.1 [39] model as our base model. Compared to vanilla CFG, CFG-Zero⋆ improves both frame quality and overall video smoothness*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/012_Table_6.jpg]]
*Table 6: Effectiveness of CFG-Zero⋆. Comparison of vanilla CFG, CFG with zero-init, dynamic scaling, and CFG-Zero⋆, highlighting the impact of zero-init and dynamic scaling in improving performance*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/015_Figure_7.jpg]]
*Figure 7: Abalation study on different sampling steps. Comparison of CLIP Score and Aesthetic Score between our method and CFG across different sampling steps*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/016_Figure_8.jpg]]
*Figure 8: Abalation study on different guidance scale. Comparison of CLIP Score and Aesthetic Score between our method and CFG across different guidance scale*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/017_Table_8.jpg]]
*Table 8: Computational costs. FLOPs [15] and GPU memory usage of our method for 5-second video generation at 720p/480p using Wan2.1 [39], and at 1024/512 resolution using SD3 [5]*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2503_18886/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative comparisons between CFG and CFG-Zero⋆. Experiments are conducted using Lumina-Next, Stable Diffusion 3, and Stable Diffusion 3.5, with each model evaluated under its recommended optimal sampling steps and guidance scale settings. CFG results are shown in orange and Ours are highlighted in green boxes*



## 定位与知识库关联

### 与基线方法的关系

**CFG-Zero⋆** 建立在标准无分类器引导（CFG）的基础上，但针对 Flow Matching 模型在训练早期的速度估计不准确问题进行了两项关键修正：优化的无条件速度缩放因子 *s* 和 ODE 求解器初始步骤的零初始化。其核心洞察在于：当模型欠拟合时，CFG 在 *t*=0 处的引导误差甚至大于直接使用零速度，因此零速度反而是更准确的估计；同时，将条件速度投影到无条件速度上得到的缩放因子 *s\** 能够最小化引导速度与真实速度的误差上界。

与已有引导策略的对比关系如下：

- **标准 CFG**：作为最直接的基线，CFG 使用固定的无条件速度权重（1−*ω*）进行线性组合。CFG-Zero⋆ 将无条件速度替换为 *s*·*v*_uncond，并引入零初始化，在训练早期和欠拟合场景下显著降低了引导误差。在 ImageNet-256 上，CFG-Zero⋆ 的 IS 达到 258.87，FID 降至 2.10，Recall 提升至 0.61，均优于 CFG 的 257.03、2.23 和 0.59（Table 2）。

- **ADG**（Sadat et al., ICLR 2024）：自适应动态引导旨在解决过饱和等问题，但其设计并非针对 Flow Matching 范式。在 ImageNet-256 上，ADG 的 FID 为 2.33，Recall 为 0.56，均不及 CFG-Zero⋆（FID 2.10, Recall 0.61）（Table 2）。论文指出 ADG 在 Flow Matching 模型上可能表现不如预期，但仍将其作为对比基线。

- **CFG++**：作为另一种改进的 CFG 方法，CFG++ 在 ImageNet-256 上的 IS 为 255.82，FID 为 2.17，sFID 为 4.67，全面弱于 CFG-Zero⋆（Table 2）。与 ADG 类似，CFG++ 并非专为 Flow Matching 设计。

- **Conditional Prediction（Baseline）**：仅使用条件速度预测，无任何引导。CFG-Zero⋆ 通过引入优化的引导机制，在所有指标上大幅超越该下界参考（Table 2）。

### 适用边界

CFG-Zero⋆ 的效果与模型的训练程度密切相关。Table 1 显示，在 ImageNet-256 训练早期（10~160 epochs），零初始化始终优于标准 CFG；但当模型训练至 160 epochs 以上充分收敛后，零初始化的增益消失甚至转为负面。这一转折点验证了该方法的核心假设：零初始化的有效性源于欠拟合模型在初始步骤的速度估计误差。

此外，零初始化步数 *K* 对模型敏感。Table 7 表明，对于 SD3.5，超过 1 步的零初始化会导致性能下降；而 Lumina-Next 和 SD3 在零出前 2 步（约 7% 的采样步数）时达到最佳。这种差异可能与模型容量、预训练程度或架构设计有关，但论文未给出深入分析。

对于 CFG-distilled 模型（如 Flux），直接应用 CFG 可能改变其采样分布，CFG-Zero⋆ 在此类模型上的表现仅作为参考，未作深入验证。

### 局限与开放问题

**已知局限：**

1. **依赖欠拟合程度**：CFG-Zero⋆ 的提升在模型充分训练后减弱甚至消失，使其在成熟模型上的增益有限。
2. **超参数 *K* 需手动调节**：零初始化步数缺乏自适应机制，需针对不同模型和任务单独设置。
3. **范式限定**：实验主要集中在 Flow Matching 模型上，未在传统扩散模型（如 DDPM、EDM）上验证。
4. **用户研究规模有限**：仅邀请 76 名参与者，且仅在部分文本提示上比较，可能存在选择偏差。
5. **视频生成的指标权衡**：在 Wan-2.1 上，CFG-Zero⋆ 在 Temporal Style 指标上有所下降（Table 5），表明其在时序一致性方面可能存在潜在弱点。

**开放问题：**

1. 优化尺度 *s\** 是否对模型架构或训练方法敏感？能否推广到非 Flow Matching 范式（如 EDM、DDPM）？
2. 零初始化步数 *K* 是否可以通过验证集自动选择，或与训练 epoch 建立函数关系以实现自适应？
3. CFG-Zero⋆ 与自适应引导策略（如 ADG）结合能否产生互补增益？
4. 为何 SD3.5 对多步零初始化更敏感，而其他模型则受益于更多零步？这是否与模型容量或预训练程度有关？
5. CFG-Zero⋆ 对不同类型的条件（文本、图像、分割图）是否具有一致的增益？
6. 零初始化对采样效率的影响能否结合蒸馏技术来弥补？



## 原文 PDF

![[paperPDFs/arXiv_2025/CFG_Zero_Improved_Classifier_Free_Guidance_for_Flow_Matching_Models.pdf]]
