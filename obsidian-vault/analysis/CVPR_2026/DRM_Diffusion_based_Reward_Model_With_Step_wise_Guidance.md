---
title: "DRM: Diffusion-based Reward Model With Step-wise Guidance"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DRM_Diffusion_based_Reward_Model_With_Step_wise_Guidance.pdf
project_link: null
code_link: "https://github.com/jjaxonx/DRM"
aliases:
- DDBRMSGSWS
- DRM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将预训练扩散模型作为奖励模型（DRM）的评估主干，利用其生成高保真图像时必须的内在视觉美学与构图理解能力，特别是其对任意去噪时间步的中间噪声潜变量进行评估的独特能力。
primary_logic: 高保真图像生成能力必然要求模型深刻理解视觉美学、构图等属性，因此可以通过“生成即理解”的范式，将预训练扩散模型转化为强大的视觉质量评估器，为奖励建模提供更丰富的感知信号。
claims:
- DRM 采用扩散模型作为骨干，能够评估任意噪声水平下的中间潜变量，而传统奖励模型仅评估最终图像。
- Step-GRPO 通过提供每个步骤的密集奖励，解决了GRPO中的信用分配问题，使训练更稳定高效。
- 在 SD3.5-Medium 上使用 DRM + Step-GRPO 对比其他奖励模型取得了最优的 PickScore (17.04)、HPSv3 (10.28) 分数。
- DRM 即使在高噪声水平下（t=750）仍能保持稳健的偏好预测准确率（65.11%），展现了步进评估能力。
---

# DRM: Diffusion-based Reward Model With Step-wise Guidance

> [!tip] 核心洞察
> 高保真图像生成能力必然要求模型深刻理解视觉美学、构图等属性，因此可以通过“生成即理解”的范式，将预训练扩散模型转化为强大的视觉质量评估器，为奖励建模提供更丰富的感知信号。

| 字段 | 内容 |
|------|------|
| 中文题名 | DRM：基于扩散模型的逐步引导奖励机制 |
| 英文题名 | DRM: Diffusion-based Reward Model With Step-wise Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_DRM_Diffusion-based_Reward_Model_With_Step-wise_Guidance_CVPR_2026_paper.html) · [Code](https://github.com/jjaxonx/DRM) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DRM (Diffusion-based Reward Model) 及其 Step-GRPO 和 Step-wise Sampling |
| Dataset | SD3.5-Medium 测试集（生成质量）, SD3.5-Medium 测试集（Step-wise 采样效果） |

> [!tip] 效果简介
> - SD3.5-Medium 测试集（生成质量） 上，PickScore ↑ 17.04 (DRM + Step-GRPO) vs 16.95 (DRM + Standard GRPO) (+0.09)；HPSv3 ↑ 10.28 (DRM + Step-GRPO) vs 10.07 (DRM + Standard GRPO) (+0.21)。
> - SD3.5-Medium 测试集（Step-wise 采样效果） 上，ImageReward ↑ 1.15 (k=6) vs 1.01 (k=1, 无分支) (+0.14)；HPSv3 ↑ 9.49 (k=6) vs 8.95 (k=1, 无分支) (+0.54)。

## 概要

现有文本到图像扩散模型的对齐方法普遍依赖基于视觉-语言模型（VLM）或CLIP的奖励模型，这些模型以语义对齐为主要训练目标，难以有效捕捉美学、构图与视觉和谐等人类偏好的核心感知维度。更关键的是，标准GRPO等强化学习对齐算法将终端奖励均匀分配到所有去噪步骤，导致信用分配不精确，无法区分各步骤对最终生成质量的差异化贡献。

针对上述瓶颈，本文提出**DRM（Diffusion-based Reward Model）**，核心思想是“生成即理解”——将预训练扩散模型重新用作视觉质量评估的骨干网络。高保真图像生成能力必然要求模型深刻理解视觉美学与构图等属性，因此预训练扩散模型天然具备丰富的感知评估潜力。DRM的独特优势在于，它不仅能评估最终生成的干净图像，还能对去噪轨迹上任意噪声水平的中间潜变量给出即时奖励信号，这是传统奖励模型无法实现的能力。

基于DRM的步进评估特性，作者进一步设计了**Step-GRPO**算法，在每个去噪步骤独立计算候选样本的局部优势，提供密集的步骤级奖励，从而解决标准GRPO中的信用分配问题。在推理阶段，**Step-wise Sampling**策略通过每步生成多个候选并由DRM评分后贪婪选择最优路径，实现了“探索-选择”式的推理增强。

实验结果表明，在SD3.5-Medium上，DRM配合Step-GRPO取得了最优生成质量：PickScore达到17.04，HPSv3达到10.28，优于基于VLM/CLIP的奖励模型（如**HPSv3**、**ImageReward**、**PickScore**）及标准GRPO基线。消融研究证实，预训练扩散权重初始化对DRM至关重要，且DRM即使在高噪声水平下仍能保持稳健的偏好预测能力。Step-wise Sampling在推理时进一步带来显著的性能增益（HPSv3提升+0.54，k=6），而Step-GRPO相比标准GRPO收敛速度提升约2.5倍（按训练步数计）。

文本到图像生成模型近年来取得了显著进展，但如何使生成的图像与复杂的人类偏好对齐仍然是一个核心挑战。人类对图像的偏好不仅涉及语义准确性，更包含美学、构图、视觉和谐等感知质量维度，这些维度难以通过简单的规则或提示词工程来精确描述。

当前主流的对齐方法依赖于奖励模型对生成结果进行评分，然后将该信号反馈给生成模型进行优化。然而，现有的奖励模型存在一个根本性的瓶颈：**它们将图像生成过程视为一个黑盒，仅对最终输出的干净图像提供单一的终端奖励**。无论是基于CLIP的奖励模型（如 **ImageReward** (Xu et al., NeurIPS 2023)、**PickScore** (Kirstain et al., NeurIPS 2023)），还是基于视觉-语言模型（VLM）的奖励模型（如 **HPSv3** (Ma et al., ICCV 2025)），其训练目标都以语义对齐为核心，难以有效捕捉美学、构图等人类偏好的核心感知质量。

在强化学习对齐层面，标准GRPO算法（如 **Flow-GRPO** (Liu et al., 2025)）在获得终端奖励后，将其均匀分配到所有去噪步骤。这种粗粒度的信用分配方式无法区分各步骤对最终质量的差异化贡献，导致训练效率低下且优化方向不够精确。

DRM的提出源于一个核心洞察：**高保真图像生成能力必然要求模型深刻理解视觉美学、构图等属性，因此可以将预训练扩散模型转化为强大的视觉质量评估器**。这一“生成即理解”的范式打破了传统奖励模型仅评估最终图像的局限——扩散模型在生成过程中天然地处理不同噪声水平下的中间潜变量，这意味着将其作为评估骨干时，DRM能够对任意去噪时间步的中间状态给出即时奖励，为奖励建模提供更丰富、更细粒度的感知信号。基于这一能力，作者进一步设计了Step-GRPO和Step-wise Sampling，将密集的步骤级奖励引入策略优化和推理采样，从根本上解决了信用分配不精确的问题。

## 核心方法与创新机理

DRM 工作的核心创新在于彻底重构了生成式奖励模型的两个关键维度：**评估主干的语义范式**和**奖励信号的时空粒度**。传统方法将扩散模型的去噪过程视为黑盒，仅以最终图像作为评估对象，且依赖语义对齐的视觉编码器（如 CLIP、VLM）作为奖励模型的基础。DRM 则提出“生成即理解”的范式，将预训练扩散模型本身转化为感知质量评估器，并据此构建了从训练到推理的全链路细粒度优化机制。

### 1. 评估主干：从语义对齐到生成感知

基于 VLM 或 CLIP 的奖励模型（如 **HPSv3**（Ma et al., ICCV 2025）、**ImageReward**（Xu et al., NeurIPS 2023）、**PickScore**（Kirstain et al., NeurIPS 2023））以语义相似性为训练核心，难以有效捕捉美学、构图、视觉和谐等人类偏好的关键维度。DRM 的核心洞见在于：高保真图像生成能力必然要求模型深刻理解这些视觉属性，因此预训练扩散模型的特征空间天然蕴含丰富的感知质量信号。

具体实现上，DRM 以 SD3.5-Medium 的 Diffusion Transformer（DiT）为骨干，截断最后 3 层 Transformer 以控制参数量，并在其内部特征之上附加轻量的奖励输出头（由 MLP 降维、空间重塑、卷积、池化、MLP 组成，见 Eq. 8）。训练时采用 Bradley-Terry 模型的负对数似然损失（Eq. 10），在成对偏好数据上优化偏好排序能力。

这一设计带来了一个传统奖励模型无法实现的独特能力：**对任意噪声时间步的中间潜变量进行评估**。传统方法仅能对最终干净图像（$t=0$）给出单一奖励，而 DRM 可以接受任意 $t \in [0,1]$ 时刻的噪声潜变量 $x_t$ 并输出即时偏好分数。这一能力是后续 Step-GRPO 和 Step-wise Sampling 的根基。

### 2. 信用分配：从终端均匀分配到步进密集奖励

标准 GRPO 算法（如 **Flow-GRPO**（Liu et al., 2025））将终端奖励均匀分配到所有去噪步骤，导致信用分配不精确——模型无法区分哪些步骤对最终质量贡献更大，哪些步骤引入了瑕疵。DRM 的步进评估能力使这一问题有了根本性的解决方案。

Step-GRPO 在每个去噪步 $t$ 生成 $k$ 个候选潜变量（通过 SDE 随机探索），由 DRM 对每个候选独立评分，并在局部组内归一化得到即时优势 $\hat{A}_t^i$（Eq. 11）：

$$\hat{A}_t^i = \frac{R(\mathbf{x}_t^i, \mathbf{c}) - \mathrm{mean}(\{R(\mathbf{x}_t^i, \mathbf{c})\}_{i=1}^k)}{\mathrm{std}(\{R(\mathbf{x}_t^i, \mathbf{c})\}_{i=1}^k)}$$

这一设计将信用分配从“事后均摊”变为“即时反馈”，使策略梯度更新能够精确地强化每一步中的优质决策。实验表明，Step-GRPO 不仅最终奖励更高（PickScore 17.04 vs. 16.95，HPSv3 10.28 vs. 10.07，Table 3），且收敛速度提升约 2.5 倍（按步数计）或约 3.5 倍（按 GPU 小时计，Figure 7）。

### 3. 推理采样：从确定性单路径到探索-选择机制

传统扩散模型推理采用确定性 ODE 采样，一旦某步生成次优结果便无法修正。DRM 的步进评估能力催生了 Step-wise Sampling 推理策略：在每一步 $t$ 通过 SDE 分支生成 $k$ 个候选，DRM 即时评分后贪婪选择最优候选继续轨迹（Eq. 12）：

$$\mathbf{x}_{t-1} = \operatorname{argmax}_{\mathbf{x}_{t-1}^i} (R(\mathbf{x}_{t-1}^i, c))$$

这一“探索-选择”机制无需额外训练，仅在推理时引入可控的计算开销（默认 $k=6$）。在 SD3.5-Medium 测试集上，Step-wise Sampling 使 ImageReward 从 1.01 提升至 1.15，HPSv3 从 8.95 提升至 9.49（Table 4），验证了步进引导在推理阶段的独立增益。

### 创新总结

DRM 的三个核心创新构成了一条完整的逻辑链：**扩散模型作为评估器**赋予了步进评估的能力，**Step-GRPO** 将这一能力用于训练阶段的细粒度信用分配，**Step-wise Sampling** 则将同一能力用于推理阶段的动态路径优化。三者共同实现了从“黑盒终端奖励”到“白盒步进引导”的范式转变。

DRM 方法体系由三个核心模块构成，围绕“生成即理解”这一范式展开，形成训练–对齐–推理的完整闭环。

### 模块一：扩散奖励模型

DRM 将预训练扩散模型改造为人类偏好评估器。其骨干网络采用 **SD3.5-Medium** 的 DiT（Diffusion Transformer，约 2.5B 参数），截断最后三层 Transformer 以匹配主流 VLM 奖励模型的参数量级。输入不再是纯文本条件，而是一对带有特定噪声水平 $t$ 的图像潜变量 $\mathbf{x}_t^{\text{win}}$ 与 $\mathbf{x}_t^{\text{lose}}$。DiT 提取中间视觉特征后，经 **Reward Output Head** 处理：首先通过 MLP 将特征 $f_v \in \mathbb{R}^{L \times d}$ 投影为 $f_p \in \mathbb{R}^{L \times d_p}$，再重塑为空间特征图，经过小型卷积网络和池化操作，最终由 MLP 输出偏好分数 $s$（见 **Figure 3** 右半部分架构）。训练目标采用 Bradley-Terry 模型的负对数似然损失：

![[assets/figures/papers/paper_list_l2673_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DRM_Diffusion_ba/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the Diffusion-based Reward Model (DRM). (Left) The training pipeline. During training, the DRM takes a pair of preferred and dispreferred images, both corrupted with noise at a specific timestep t, and predicts their respective reward scores. The model is then optimized via DR loss. (Right) The detailed architecture of our Reward Output Head*

$$\mathcal{L}_{\text{DRM}} = -\log \sigma(s^{\text{win}} - s^{\text{lose}})$$

DRM 的关键能力在于：它不仅能评估最终干净图像，还能对任意噪声时间步的中间潜变量给出即时奖励信号，这是传统 VLM/CLIP 奖励模型（如 **ImageReward** (Xu et al., NeurIPS 2023)、**PickScore** (Kirstain et al., NeurIPS 2023)）所不具备的。

### 模块二：Step-GRPO 策略优化

Step-GRPO 将 DRM 的步进评估能力引入强化学习对齐流程。标准 GRPO（如 **Flow-GRPO** (Liu et al., 2025)）采样完整去噪轨迹，仅在终点 $t=0$ 获得单一终端奖励，并将该奖励均匀分配至所有去噪步骤，导致信用分配不精确。Step-GRPO 的改进在于：在每个去噪步 $t$，从同一初始点通过 SDE 随机探索生成 $k$ 个候选 $\{\mathbf{x}_{t-1}^i\}_{i=1}^k$，DRM 对每个候选即时评分，并计算归一化的局部优势：

$$\hat{A}_t^i = \frac{R(\mathbf{x}_t^i, \mathbf{c}) - \mathrm{mean}(\{R(\mathbf{x}_t^i, \mathbf{c})\}_{i=1}^k)}{\mathrm{std}(\{R(\mathbf{x}_t^i, \mathbf{c})\}_{i=1}^k)}$$

每步独立计算候选优势后进行策略更新，形成密集的步骤级信用分配（见 **Figure 4** 右半部分对比）。

### 模块三：Step-wise Sampling 推理

推理阶段引入“探索–选择”机制（见 **Figure 5**）。在每个时间步 $t$，生成器通过 SDE 分支产生 $k$ 个候选下一状态，DRM 对所有候选评分，贪婪选择奖励最高的候选继续轨迹：

$$\mathbf{x}_{t-1} = \operatorname{argmax}_{\mathbf{x}_{t-1}^i} \big(R(\mathbf{x}_{t-1}^i, c)\big)$$

这一机制在不改变生成模型权重的前提下，通过动态路径选择提升最终图像的美学质量和提示词保真度。

### 数据流与闭环

整体 pipeline 的数据流如下：**偏好数据**（HPDv3、Pick-A-Pic 等）→ 训练 DRM（学习人类偏好排序）→ **Step-GRPO** 利用 DRM 的步进奖励优化生成策略（强化学习对齐）→ 推理时 **Step-wise Sampling** 利用 DRM 进行动态路径选择（推理增强）。三个模块共享 DRM 作为统一的评估骨干，形成“训练评估器 → 优化生成器 → 引导推理”的闭环。

![[assets/figures/papers/paper_list_l2673_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DRM_Diffusion_ba/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between preview reward models and DRM. Existing reward models treat the generation process as a black box, providing only a single, terminal reward based on the final output. Our DRM offers fine-grained reward for any noisy latent along the entire denoising trajectory*

### 扩散奖励模型（DRM）架构

DRM 的核心设计在于将预训练扩散模型转化为视觉质量评估器。其骨干网络直接继承自 **SD3.5-Medium** 的 DiT（Diffusion Transformer，参数量 2.5B），并截断最后三层 Transformer 层以匹配现有奖励模型的规模。给定任意噪声时间步 $t$ 下的噪声潜变量 $\mathbf{x}_t$ 和文本条件 $\mathbf{c}$，DRM 从 DiT 中间层提取视觉特征，经专门设计的奖励输出头生成偏好分数。

特征提取与分数预测流程可形式化为：

$$f_p = \mathbf{MLP}(f_v), \quad f_v \in \mathbb{R}^{L \times d},\; f_p \in \mathbb{R}^{L \times d_p}$$

其中 $f_v$ 为 DiT 中间层输出的视觉特征，经线性投影降维至 $d_p$ 维后得到 $f_p$。随后，$f_p$ 被重塑为空间特征图，依次通过小型卷积网络、池化层和 MLP，最终输出标量偏好分数 $s$：

$$s = \mathrm{MLP}(\mathrm{Pooling}(\mathrm{Conv}(\mathrm{ReShape}(f_p))))$$

这一设计的独特之处在于：DRM 的输入可以是任意噪声水平下的中间潜变量 $\mathbf{x}_t$，而不仅限于最终干净图像 $\mathbf{x}_0$。这赋予了 DRM 对去噪全过程的步进评估能力。

### DRM 训练损失

DRM 采用基于 **Bradley-Terry** 模型的成对偏好排序损失进行训练。对于一对偏好图像（赢家 $x^{win}$ 与输家 $x^{lose}$），两者被施加相同噪声时间步 $t$ 的噪声后输入 DRM，分别获得分数 $s^{win}$ 和 $s^{lose}$。训练目标为最大化赢家分数高于输家分数的概率，损失函数为：

$$\mathcal{L}_{DRM} = -\log(\sigma(s^{win} - s^{lose}))$$

其中 $\sigma(\cdot)$ 为 Sigmoid 函数。该损失驱动 DRM 学习人类偏好排序，使赢家图像获得系统性地更高的奖励分数。

### Step-GRPO：步进式信用分配

标准 GRPO 算法将最终图像的终端奖励均匀分配至所有去噪步骤，导致信用分配不精确。Step-GRPO 利用 DRM 的步进评估能力，在每个去噪步 $t$ 生成 $k$ 个候选潜变量 $\{\mathbf{x}_t^i\}_{i=1}^k$（通过将确定性 ODE 转化为 SDE 实现随机探索），并由 DRM 即时给出每个候选的奖励 $R(\mathbf{x}_t^i, \mathbf{c})$。

每步的即时优势 $\hat{A}_t^i$ 通过对组内 $k$ 个候选的奖励进行归一化计算：

$$\hat{A}_t^i = \frac{R(\mathbf{x}_t^i, \mathbf{c}) - \mathrm{mean}(\{R(\mathbf{x}_t^i, \mathbf{c})\}_{i=1}^k)}{\mathrm{std}(\{R(\mathbf{x}_t^i, \mathbf{c})\}_{i=1}^k)}$$

该优势值用于更新策略模型参数，使每个去噪步骤获得独立、精确的优化信号，而非依赖终端奖励的粗糙回传。

### Step-wise Sampling：推理时步进择优

在推理阶段，Step-wise Sampling 引入“探索-选择”机制。在每个去噪步 $t$，通过 SDE 分支生成 $k$ 个候选下一状态 $\{\mathbf{x}_{t-1}^i\}_{i=1}^k$，DRM 对所有候选评分，贪婪选择奖励最高的候选作为实际去噪路径：

$$\mathbf{x}_{t-1} = \operatorname{argmax}_{\mathbf{x}_{t-1}^i} (R(\mathbf{x}_{t-1}^i, c))$$

这一策略无需额外训练，在推理时动态修正生成路径，显著提升最终图像的感知质量与提示遵循度。

![[assets/figures/papers/paper_list_l2673_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DRM_Diffusion_ba/figures/005_Figure_5.jpg]]
*Figure 5: Overview of Step-wise Sampling. At each step t, we perform a branching into k candidates via SDE. The DRM scores these candidates, and the top-scoring latent is chosen to continue the trajectory*

## 实验与关键发现

### 核心瓶颈与评估动机

当前主流的奖励模型（如基于VLM的 **HPSv3** (Ma et al., ICCV 2025) 和基于CLIP的 **ImageReward** (Xu et al., NeurIPS 2023)、**PickScore** (Kirstain et al., NeurIPS 2023)）以语义对齐为训练目标，难以有效捕捉美学、构图、视觉和谐等人类偏好核心的感知质量。同时，标准GRPO算法（如 **Flow-GRPO** (Liu et al., 2025)）将终端奖励均匀分配到所有去噪步骤，导致信用分配不精确，无法区分各步骤对最终质量的贡献差异。

DRM的核心洞察在于：高保真图像生成能力必然要求模型深刻理解视觉美学、构图等属性，因此可以通过“生成即理解”的范式，将预训练扩散模型转化为强大的视觉质量评估器。DRM以预训练DiT（SD3.5-Medium，截断最后3层Transformer，约2.5B参数）作为评估骨干，利用其生成高保真图像时必须的内在视觉美学与构图理解能力，特别是其对任意去噪时间步的中间噪声潜变量进行评估的独特能力。

### 奖励模型偏好预测能力评估

Table 1展示了DRM在多个偏好预测基准上的准确率对比。DRM在PickScore测试集上取得了顶级准确率（72.1%），显著优于同规模VLM基线HPSv3。然而，在ImageReward（62.9%）、HPDv2（80.1%）和HPDv3（71.9%）上，DRM的性能并非最高——这是其核心设计的预期权衡：DRM训练时接受噪声中间表示，而传统基准仅包含干净图像，存在领域偏移。这种权衡是DRM独特步进评估能力的固有取舍，而非设计缺陷。

**Table 1** 的消融结果揭示了两个关键发现：

1. **预训练权重不可或缺**：使用SD3.5-Medium预训练权重初始化（Pre-trained 256）在仅1个epoch后即达到上述性能；而随机初始化（Random 256）在相同训练量下准确率大幅下降（PickScore仅57.5%，下降14.6个百分点）。即使将随机初始化训练延长至3个epoch（Random 256 epoch 3），性能仍无法追赶（PickScore仅59.0%），证明预训练扩散权重不仅加速收敛，更决定了模型能达到的性能上限。

2. **分辨率缩放效应**：将训练图像分辨率从256提升至512（Pre-trained 512），在所有基准上均带来持续提升（如PickScore从72.1%升至73.4%），表明更高分辨率的视觉细节有助于DRM更精确地评估感知质量。

### 噪声鲁棒性与步进评估能力

Table 2验证了DRM对噪声水平的鲁棒性——这是其区别于传统奖励模型的核心能力。随着噪声时间步t增加（噪声水平升高），DRM的偏好预测准确率呈可预测的逐渐下降趋势，但即使在t=750的高噪声条件下，准确率仍保持在65.11%。这一结果表明DRM能够从高度损坏的中间潜变量中提取有意义的视觉偏好信号，为其在Step-GRPO和Step-wise Sampling中提供密集的步进奖励奠定了能力基础。

### 生成质量优化效果

Table 3对比了使用不同奖励模型优化SD3.5-Medium后的生成质量。DRM + Step-GRPO在PickScore上取得17.04的最优分数（对比DRM + Standard GRPO的16.95，提升+0.09），在HPSv3上取得10.28（对比Standard GRPO的10.07，提升+0.21）。相比其他奖励模型（HPSv3、ImageReward、PickScore）优化的结果，DRM + Step-GRPO在所有三个指标上均取得最优或次优成绩。

**Figure 6** 的定性对比进一步印证了量化结果：DRM优化的SD3.5-Medium在视觉质量上明显优于其他奖励模型优化的版本，展现出更好的美学表现和构图和谐性。

### Step-wise Sampling推理增强

Table 4验证了Step-wise Sampling在推理时的独立增益。在不改变模型权重的前提下，将分支数k从1（无分支，确定性采样）提升至6，ImageReward从1.01提升至1.15（+0.14），HPSv3从8.95提升至9.49（+0.54），在所有评估指标上均取得显著提升。这证明DRM的步进评估能力可以在推理阶段通过“探索-选择”机制直接转化为生成质量增益，无需额外训练。

**Figure 8** 的定性结果显示，Step-wise Sampling同时增强了对提示词的保真度和生成图像的美学质量。

### 收敛效率分析

Figure 7对比了Step-GRPO与Standard GRPO的收敛曲线。以训练步数为横轴时，Step-GRPO不仅达到更高的最终奖励水平，且收敛速度约为Standard GRPO的2.5倍（按步数计）。以GPU小时为横轴时，Step-GRPO达到同等奖励水平所需时间约为Standard GRPO的1/3.5，展现了显著的训练效率优势。这一效率提升源于密集的逐步奖励信号为策略优化提供了更精确的信用分配，避免了终端奖励均匀分配带来的梯度噪声。

### 方法局限与待验证问题

DRM存在以下已知局限，在解读实验结果时需注意：

1. **干净图像基准的领域偏移**：如前所述，DRM在仅含干净图像的基准上性能非顶级，这是其步进评估能力的固有取舍，需根据应用场景权衡。

2. **预训练权重依赖性**：DRM高度依赖SD3.5-Medium的预训练权重，更换生成模型架构可能需重新训练或适配，对其他扩散范式（如DDPM、EDM）的泛化性尚不明确。

3. **推理计算开销**：Step-wise Sampling每步需评估k个候选（默认k=6），显著增加推理延迟，在实时或大规模部署场景中需考虑效率与质量的平衡。

4. **训练数据偏见**：DRM训练数据来源于静态偏好数据集（HPDv3、Pick-A-Pic等），奖励模型可能继承这些数据中的固有偏见。

5. **验证范围有限**：方法仅在SD3.5-Medium及Flow Matching框架上验证，对SiT、Masked Diffusion等其他扩散架构的适用性有待探索。

![[assets/figures/papers/paper_list_l2673_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DRM_Diffusion_ba/figures/006_Table_1.jpg]]
*Table 1: Preference prediction accuracy (%) on the test sets of ImageReward, HPDv2 and HPDv3. The best and second-best results are bolded and underlined. Our model achieves top-tier accuracy on PickScore. Its competitive scores on ImageReward, HPDv2 and HPDv3 reflect an expected trade-off, stemming from the DRM’s core design. The DRM is trained to assess noisy latents throughout the generation process, not just the final clean outputs. This capability, fundamental to our approach, introduces a subtle domain shift when evaluated on benchmarks consisting solely of clean images, which accounts for the performance gap*

![[assets/figures/papers/paper_list_l2673_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DRM_Diffusion_ba/figures/007_Table_2.jpg]]
*Table 2: DRM Accuracy vs. Timestep. Performance on HPSv3 test set. Higher timestep correspond to higher noise level*

![[assets/figures/papers/paper_list_l2673_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DRM_Diffusion_ba/figures/013_Figure_6.jpg]]
*Figure 6: Qualitative comparison of SD3.5-Medium optimized by various reward models. Our approach clearly exhibits superior visual quality compared to the competing methods*

## 定位与知识库关联

### 1. 与现有奖励模型的范式差异

DRM 的核心突破在于将奖励模型的**评估主干从语义对齐模型迁移至生成模型**，这构成了其与现有工作的根本分界线。

*   **基于 VLM/CLIP 的奖励模型**：主流方法如 **HPSv3** (Ma et al., ICCV 2025)、**ImageReward** (Xu et al., NeurIPS 2023) 和 **PickScore** (Kirstain et al., NeurIPS 2023) 均以视觉-语言模型（VLM）或 CLIP 作为视觉编码器。这类模型的核心训练目标是语义对齐，即判断图像是否与文本描述一致。其天然局限在于难以有效捕捉美学、构图、视觉和谐等构成人类偏好核心的**感知质量**维度。此外，这些模型仅能对最终生成的干净图像给出单一的终端奖励，将整个生成过程视为黑盒。
*   **DRM 的“生成即理解”范式**：DRM 采用预训练扩散模型（SD3.5-Medium 的 DiT）作为评估骨干。其核心洞察在于：一个能够生成高保真图像的模型，其内部表征必然蕴含了对视觉美学、构图等属性的深刻理解。通过截断 DiT 的最后三层 Transformer 并接入一个轻量级的奖励输出头（由 MLP 降维、空间重塑、卷积和池化构成），DRM 将这种隐式的生成能力显式化为偏好评估能力。这使其在 PickScore 基准上取得了顶尖的偏好预测准确率，并在优化生成质量时显著优于 HPSv3 等 VLM 模型。

### 2. 与强化学习对齐算法的关系

在将奖励模型用于扩散模型对齐的强化学习框架中，DRM 与现有算法形成了“评估器-优化器”的协同与超越关系。

*   **标准 GRPO 的信用分配瓶颈**：基线算法如 **Flow-GRPO** (Liu et al., 2025) 和 **DanceGRPO** (Xue et al., 2025) 遵循标准 GRPO 范式，使用终端奖励模型对整个生成轨迹评分，并将该单一奖励**均匀分配**给所有去噪步骤。这种粗粒度的信用分配方式无法区分每一步对最终质量的贡献差异，导致优化信号不精确、收敛缓慢。
*   **Step-GRPO 的细粒度进化**：DRM 凭借其独特的**步进评估能力**（可对任意噪声时间步的中间潜变量给出即时奖励），催生了 Step-GRPO 算法。Step-GRPO 在每个去噪步生成 $k$ 个候选，通过 DRM 为每个候选计算即时奖励，并归一化得到局部优势值 $\hat{A}_t^i$（Eq.11），从而实现了**密集的、步骤级的信用分配**。实验证明，Step-GRPO 相比标准 GRPO 收敛速度提升约 2.5 倍（按步数计）或 3.5 倍（按 GPU 小时计），且最终奖励曲线更高。

### 3. 推理时采样策略的拓展

DRM 的步进评估能力不仅优化了训练过程，还催生了新的推理策略，拓展了扩散模型的使用边界。

*   **从确定性采样到探索-选择**：传统扩散模型推理多采用确定性 ODE 采样，单一路径无修正机会。DRM 提出的 **Step-wise Sampling** 在每个时间步 $t$ 通过 SDE 分支生成 $k$ 个候选，并由 DRM 评分，贪婪选择最高分候选作为下一状态 $\mathbf{x}_{t-1}$（Eq.12）。这种“探索-选择”机制在推理时引入了动态路径修正能力。
*   **性能增益与成本权衡**：在 SD3.5-Medium 上，当 $k=6$ 时，Step-wise Sampling 使 ImageReward 分数从 1.01 提升至 1.15，HPSv3 分数从 8.95 提升至 9.49。然而，该方法以线性增加推理计算开销为代价，这是其主要的适用性边界。

### 4. 适用边界与关键局限

*   **领域偏移与评估权衡**：DRM 的训练数据包含被噪声污染的中间表示，这导致其在仅评估干净图像的基准（如 HPDv2、ImageReward）上并非最优。这是其核心能力（步进评估）带来的固有领域偏移，而非设计缺陷。
*   **对预训练权重的强依赖**：消融实验表明，使用预训练扩散权重初始化 DRM 至关重要。随机初始化会导致性能大幅下降（如 PickScore 准确率从 72.1% 降至 57.5%），且无法通过延长训练弥补。这意味着 DRM 的能力高度绑定于特定预训练生成模型（如 SD3.5-Medium），更换生成架构可能需要重新训练或适配。
*   **泛化性未验证**：当前方法仅在 SD3.5-Medium 及 Flow Matching 框架上验证。其对 DDPM、EDM 等其他扩散范式的泛化性尚不明确。
*   **数据偏见风险**：DRM 的训练数据来源于 HPDv3、Pick-A-Pic 等静态人类偏好数据集，其评估标准可能受限于这些数据中固有的文化、审美或标注者偏见。

### 5. 开放问题

*   **模型架构泛化**：DRM 能否与更大规模或不同架构的扩散模型（如 SiT、Masked Diffusion）配合使用？
*   **推理效率优化**：如何在不显著增加推理成本的前提下，实现更灵活的步进引导，例如可变分支数 $k$ 或自适应分支策略？
*   **任务边界拓展**：DRM 的逐步评估能力能否直接用于噪声级别条件生成、可控图像编辑等更复杂的任务？
*   **与离线对齐方法的结合**：能否将 DRM 的密集评估信号与直接偏好优化（DPO）等离线方法结合，进一步降低对齐训练的成本？
*   **跨模态迁移**：在视频、3D 等多模态生成任务中，扩散模型作为评估器的有效性如何？

## 原文 PDF

![[paperPDFs/CVPR_2026/DRM_Diffusion_based_Reward_Model_With_Step_wise_Guidance.pdf]]
