---
title: "HuTuMotion: Human-Tuned Navigation of Latent Motion Diffusion Models with Minimal Feedback"
type: paper
paper_level: A
venue: AAAI
year: 2024
pdf_ref: paperPDFs/AAAI_2024/HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_with_Minimal_Feedback.pdf
project_link: null
code_link: null
aliases:
- HuTuMotion
tags:
- AAAI_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 潜在扩散模型的先验分布（即采样分布的高斯均值 z_m^** 和标准差 σ），通过少量人类排序反馈直接优化该分布，使采样朝向人类偏好的区域。
primary_logic: 利用少量人类反馈（排名信息）在线优化潜在扩散模型的先验分布，并通过构建代表性文本集与优化后先验分布的映射，在推理时根据输入文本的余弦相似度动态选择最匹配的先验，从而在不重新训练模型的情况下显著提升运动生成的语义对齐、真实感和个性化能力。
claims:
- HuTuMotion 在 HumanML3D 和 KIT 数据集上显著超越现有最优方法，尤其在 FID 指标上有大幅改善。
- 使用少量人类反馈即可达到与大量反馈相当的性能，且生成的运动更加自然、语义正确。
- 调整先验分布并加入反馈机制是核心创新，传统方法皆使用固定标准正态先验。
- HumanML3D 上 FID↓ = 0.224 ± 0.006 (Ours*)
---

# HuTuMotion: Human-Tuned Navigation of Latent Motion Diffusion Models with Minimal Feedback

> [!tip] 核心洞察
> 利用少量人类反馈（排名信息）在线优化潜在扩散模型的先验分布，并通过构建代表性文本集与优化后先验分布的映射，在推理时根据输入文本的余弦相似度动态选择最匹配的先验，从而在不重新训练模型的情况下显著提升运动生成的语义对齐、真实感和个性化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | HuTuMotion：基于最少反馈的人类调优隐动作扩散模型导航 |
| 英文题名 | HuTuMotion: Human-Tuned Navigation of Latent Motion Diffusion Models with Minimal Feedback |
| 会议/期刊 | AAAI 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | HuTuMotion |
| Dataset | HumanML3D, KIT |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.224 ± 0.006 (Ours*) vs 0.473 ± 0.013 (MLD) (-0.249)；R Precision Top1↑ 0.497 ± 0.002 (Ours) vs 0.481 ± 0.003 (MLD) (+0.016)。
> - KIT 上，FID↓ 0.201 ± 0.064 (Ours*) vs 0.404 ± 0.027 (MLD) (-0.203)；R Precision Top1↑ 0.411 ± 0.005 (Ours) vs 0.390 ± 0.008 (MLD) (+0.021)。

## 概要

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列。现有方法普遍从标准正态先验分布 $\mathcal{N}(0, I)$ 中采样潜在变量，这一固定先验未能充分反映运动数据的真实分布特性，导致生成的运动在真实感和语义对齐方面存在明显不足，尤其难以捕捉“老人”等细粒度属性或实现个性化、风格化生成。

针对上述瓶颈，本文提出 **HuTuMotion**，一种基于最少人类反馈的隐动作扩散模型导航方法。其核心洞察在于：通过少量人类排序反馈在线优化潜在扩散模型的先验分布，并构建代表性文本集与优化后先验分布的映射关系，使推理时可根据输入文本的语义相似度动态选择最匹配的先验进行采样，从而在不重新训练模型的前提下显著提升生成质量。

在 HumanML3D 和 KIT 两个标准基准上，HuTuMotion 取得了显著优于现有最优方法 **MLD**（Chen et al., CVPR 2023）的性能，其中 FID 指标从 0.473 降至 0.224（HumanML3D），从 0.404 降至 0.201（KIT），同时 R Precision Top1 等语义对齐指标亦有稳定提升。定性结果表明，该方法生成的运动更加自然、语义正确，并能有效支持个性化和风格感知的运动生成。

从方法谱系来看，HuTuMotion 属于**基于人类反馈的潜在扩散先验优化**范式，与现有的无监督文本条件运动扩散方法（如 MLD、**MDM**（Tevet et al., 2022）、**T2M**（Guo et al., CVPR 2022a）、**TEMOS**（Petrovich, Black, and Varol, ECCV 2022））形成互补：后者依赖固定的标准正态先验，而 HuTuMotion 引入了可在线调优的数据驱动先验，为运动生成领域开辟了“最少反馈即插即用”的新路径。



文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，扩散模型在该领域取得了显著进展，代表性工作包括在原始运动空间建模的 **MDM**（Tevet et al., 2022）和在潜在空间建模的 **MLD**（Chen et al., CVPR 2023）。其中，MLD 作为当前最优的潜在扩散方法，其训练目标为：

$$\mathcal{L}_{\mathrm{MLD}} := \mathbb{E}_{\epsilon, t, c}\left[\|\epsilon - \epsilon_{\theta}(z_t, t, \tau_{\theta}(c))\|_2^2\right]$$

该目标通过 CLIP 文本编码器 $\tau_{\theta}(c)$ 提取文本条件，在潜在空间预测添加的噪声，从而学习文本到运动的映射。

然而，现有方法存在一个核心瓶颈：**它们无一例外地从标准正态先验分布 $\mathcal{N}(0, I)$ 中采样潜在变量**。这一设计假设数据在潜在空间中服从标准正态分布，但该假设并未充分反映真实运动数据的分布特性。由此导致两个关键问题：

1. **语义对齐不足**：从无信息先验中随机采样，难以保证生成的运动与输入文本在语义上精确匹配，尤其对于需要捕捉细粒度属性（如“老人蹒跚行走”）或风格化描述（如“僵尸式行走”）的场景，固定先验无法提供有效的语义引导。

2. **真实感受限**：标准正态先验的采样区域可能与高质量运动对应的潜在空间区域存在偏差，导致生成的运动缺乏自然度和真实感。

现有方法的另一个共同缺陷是**完全无监督的训练范式**——模型仅依赖文本-运动配对数据进行训练，缺乏对生成质量的直接反馈机制。这使得模型难以针对特定语义概念或个性化需求进行定向优化。

针对上述问题，HuTuMotion 提出了一个核心洞察：**通过少量人类排序反馈，直接优化潜在扩散模型的先验分布，使采样朝向人类偏好的区域，从而在不重新训练模型的前提下显著提升生成质量**。这一思路将人类偏好注入生成过程的关键控制节点——先验分布，而非修改模型参数，实现了轻量且有效的语义对齐。



## 核心方法与创新机理

### 问题瓶颈：标准正态先验的局限

现有文本驱动人体运动生成方法（如 **MLD** (Chen et al., CVPR 2023)、**MDM** (Tevet et al., 2022)）均从标准正态分布 $\mathcal{N}(0, I)$ 中采样潜在变量，这一固定先验未能充分反映运动数据的真实分布特性。由此导致两个核心问题：

1. **语义对齐不足**：标准先验无法区分“老人缓慢行走”与“年轻人快步行走”等细粒度语义差异，生成的运动缺乏对文本描述的精确响应。
2. **真实感缺失**：从无信息先验中随机采样，使得生成的运动序列在自然度上存在明显不足，尤其在捕捉特定风格或个性化特征时表现更差。

### 核心洞察：先验分布即控制旋钮

HuTuMotion 的核心洞察在于：**潜在扩散模型的先验分布是控制生成质量的关键“旋钮”**。不同于传统方法将先验视为不可调整的固定常量，该方法将先验分布本身作为优化对象，通过少量人类排序反馈直接调整采样分布的高斯均值 $z_m^{**}$ 和标准差 $\sigma$，使采样过程朝向人类偏好的潜在空间区域。这一设计无需重新训练扩散模型，仅改变推理时的采样起点，即可显著提升生成质量。

### 三个关键改动槽位

相较于基线方法 MLD，HuTuMotion 在以下三个槽位上做出了根本性改变：

| 槽位 | 基线值 (MLD) | 提出值 (HuTuMotion) |
|------|-------------|-------------------|
| **先验分布** | 标准正态分布 $\mathcal{N}(0, I)$ | 经人类反馈优化的高斯分布 $\mathcal{N}(z_m^{**}, \sigma^2)$，均值由代表性文本的优化潜在向量决定，$\sigma=0.2$ |
| **人类反馈机制** | 无反馈（完全无监督） | 引入少量人类排序反馈（$(m,k)$-ranking oracle），通过零阶优化算法迭代调整潜在变量 |
| **推理时采样策略** | 从固定先验 $\mathcal{N}(0, I)$ 直接采样 | 根据输入文本与代表性文本的余弦相似度，动态选择最匹配的先验分布进行采样 |

### 关键机制：从排序反馈到分布优化

反馈机制的数学核心是**排序基梯度估计器**：

$$\tilde{g}(z) = \frac{1}{|\mathcal{E}|} \sum_{(i,j)\in\mathcal{E}} \frac{\xi_j - \xi_i}{\mu}$$

该估计器利用人类排序反馈构造有向无环图中的边集 $\mathcal{E}$，计算零阶梯度下降方向，从而在无需显式损失函数的情况下优化潜在变量。这一设计的精巧之处在于：人类只需比较“A 比 B 更好”的相对排序，而非给出绝对分数，大幅降低了反馈成本。

### 推理时的语义路由

在推理阶段，给定输入文本 $c_x$，系统通过最大化余弦相似度选择最匹配的代表性文本索引：

$$m = \arg \max_i \frac{c_x \cdot c_i}{\|c_x\| \|c_i\|}, \quad \text{for } i \in 1, \dots, k$$

随后从对应的优化分布 $\mathcal{N}(z_m^{**}, \sigma^2)$ 中采样潜在变量 $z_x$，送入 DDIM 采样器完成运动生成。这种“语义路由”机制使得不同语义类型的文本能够自动匹配到最适合的先验分布，实现了对细粒度语义差异的精确响应。

### 创新边界与限制

需要指出的是，该方法的核心创新聚焦于**先验分布的优化与选择**，扩散模型本身（包括去噪网络 $\epsilon_\theta$、文本编码器 $\tau_\theta$、运动解码器）完全继承自 MLD，未做任何修改。这一设计选择带来了即插即用的便利性，但也将方法的适用范围限制在潜在扩散框架内——由于显式扩散模型（如 MDM）的高维性难以优化，该方法无法直接推广到其他类型的扩散模型。



HuTuMotion 的整体框架由两个核心阶段构成：**代表性分布优化** 和 **语义引导运动生成**，如 Figure 1 所示。该方法建立在潜在运动扩散模型 **MLD**（Chen et al., CVPR 2023）之上，其训练目标为：

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/001_Figure_1.jpg]]
*Figure 1: An overview of our framework. For simplicity, we omit the motion decoder. It consists of two stages. In representative distribution optimization, we obtain the optimized latent distribution corresponding to representative texts. In a semantically guided generation, we select one latent distribution by computing text similarity*

$$
\mathcal{L}_{\mathrm{MLD}} := \mathbb{E}_{\epsilon, t, c}\left[\|\epsilon - \epsilon_{\theta}(z_t, t, \tau_{\theta}(c))\|_2^2\right]
$$

其中 $z_t$ 为潜在变量，$c$ 为文本条件，$\tau_{\theta}(c)$ 为 CLIP 文本编码器输出。与传统方法从标准正态先验 $\mathcal{N}(0, I)$ 采样不同，HuTuMotion 的核心创新在于**通过少量人类排序反馈优化先验分布**，使采样朝向人类偏好的潜在空间区域。

### 阶段一：代表性分布优化

该阶段的目标是为少量代表性运动描述文本构建优化后的高斯先验分布。具体流程如下：

1. **代表性文本生成**：利用 ChatGPT 或对训练集进行 K-Means 聚类，生成少量（默认 5 个）具有多样性和代表性的运动描述文本 $\{c_1, \dots, c_k\}$。
2. **潜在变量优化**：对每个代表性文本 $c_i$，通过 **(m,k)-ranking oracle** 获取人类排序反馈，使用零阶梯度估计器迭代优化其对应的潜在向量 $z_i$。梯度估计器利用排序信息构造有向无环图的边集 $\mathcal{E}$，计算下降方向：

$$
\tilde{g}(z) = \frac{1}{|\mathcal{E}|} \sum_{(i,j)\in\mathcal{E}} \frac{\xi_j - \xi_i}{\mu}
$$

3. **先验分布构建**：将优化后的潜在向量 $z_m^{**}$ 作为均值，设定标准差 $\sigma=0.2$，构建高斯先验分布 $\mathcal{N}(z_m^{**}, \sigma^2)$。该优化过程详见 Algorithm 1。

### 阶段二：语义引导运动生成

在推理阶段，对于给定的输入文本 $c_x$，框架通过语义对齐机制动态选择最匹配的先验分布：

1. **文本嵌入与相似度匹配**：使用 CLIP 文本编码器提取输入文本嵌入与代表性文本嵌入，计算余弦相似度，选择最匹配的代表性文本索引 $m$：

$$
m = \arg \max_i \frac{c_x \cdot c_i}{\|c_x\| \|c_i\|}, \quad \text{for } i \in 1, \dots, k
$$

2. **先验采样与运动解码**：从选定的先验分布 $\mathcal{N}(z_m^{**}, \sigma^2)$ 中采样潜在变量 $z_x$，将其与文本条件 $c_x$ 一同输入 DDIM 采样器进行去噪，最终通过运动解码器生成运动序列。

### 模块关系与数据流

整个框架的模块关系可概括为：**代表性文本生成 → 人类反馈优化 → 先验分布库构建 → 输入文本语义匹配 → 先验采样 → 扩散去噪 → 运动解码**。其中，阶段一离线完成，构建先验分布库；阶段二在线执行，根据输入文本动态选择先验。这种设计使得 HuTuMotion 无需重新训练扩散模型，仅通过调整采样先验即可显著提升生成质量。

### 扩展应用

该框架还支持**个性化运动生成**和**风格感知运动生成**。对于风格感知生成，方法针对同一风格描述符 $ST_i$ 识别多样化文本，从零开始优化获得最优潜在向量，构建风格-潜在对集合 $\{(ST_1, z_1^{**}), \dots, (ST_M, z_M^{**})\}$，推理时根据目标风格选择对应先验。



### 模块一：代表性文本生成

HuTuMotion 框架的第一阶段是**代表性分布优化**，其起点是获取少量（默认 5 个）具有代表性的运动描述文本。论文提供了两种获取方式：

1. **K-Means 聚类**：在训练数据集的文本嵌入上执行 K-Means 聚类，以聚类中心对应的文本作为代表性描述。
2. **大语言模型生成**：直接向 ChatGPT 提问，要求其生成一组多样且具有代表性的人体动作句子（见 Figure 6）。

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/010_Figure_6.jpg]]
*Figure 6: A dialogue with ChatGPT for generating a set of diverse and representative human action sentences*

这两种方式均旨在覆盖运动语义空间的主要模式，为后续的潜在分布优化提供锚点。

### 模块二：潜在分布优化（算法核心）

这是 HuTuMotion 的核心创新模块。传统方法（如 **MLD**，Chen et al., CVPR 2023）从标准正态先验 $\mathcal{N}(0, I)$ 中采样潜在变量 $z$，而 HuTuMotion 通过**少量人类排序反馈**在线优化每个代表性文本对应的潜在变量，构建新的高斯先验。

**优化流程（见 Algorithm 1）**：
- 对每个代表性文本 $c_k$，从 $\mathcal{N}(0, I)$ 采样多个候选潜在向量 $\{z_1, ..., z_m\}$，经 DDIM 采样器生成对应运动序列。
- 人类标注者以 $(m, k)$-排序谕示的形式对生成的运动进行排序（选出最好的 $k$ 个并排序）。
- 利用排序信息构造有向无环图（DAG），通过**零阶梯度估计器**计算下降方向，迭代更新潜在变量。

**关键公式：排序基梯度估计器**

$$ \tilde{g}(z) = \frac{1}{|\mathcal{E}|} \sum_{(i,j)\in\mathcal{E}} \frac{\xi_j - \xi_i}{\mu} $$

**变量含义**：
- $\mathcal{E}$：由排序谕示构造的 DAG 中的有向边集合，边 $(i, j)$ 表示 $z_i$ 优于 $z_j$。
- $\xi_i, \xi_j$：对候选潜在向量 $z_i, z_j$ 施加的随机扰动方向。
- $\mu$：扰动步长的平滑参数，控制梯度估计的尺度。
- $\tilde{g}(z)$：当前潜在变量 $z$ 的近似梯度方向，用于零阶优化更新。

该估计器利用人类排序信息替代传统的一阶梯度和损失函数，使优化过程无需可微奖励模型，仅依赖少量人类反馈即可将潜在变量推向人类偏好的区域。优化收敛后得到每个代表性文本的最优潜在向量 $z_m^{**}$，并构造高斯先验 $\mathcal{N}(z_m^{**}, \sigma^2)$（$\sigma=0.2$ 为默认超参数）。

### 模块三：语义引导采样与生成

在推理阶段，对于任意输入文本 $c_x$，系统通过**语义对齐**动态选择最匹配的先验分布：

**关键公式：代表性文本索引计算**

$$ m = \arg \max_i \frac{c_x \cdot c_i}{\|c_x\| \|c_i\|}, \quad \text{for } i \in 1, \dots, k $$

**变量含义**：
- $c_x$：输入文本经 CLIP 文本编码器 $\tau_\theta(\cdot)$ 提取的嵌入向量。
- $c_i$：第 $i$ 个代表性文本的嵌入向量。
- $m$：与输入文本余弦相似度最高的代表性文本索引。

选定索引 $m$ 后，从对应的最优先验 $\mathcal{N}(z_m^{**}, \sigma^2)$ 中采样得到 $z_x$，将其与文本条件 $c_x$ 一同送入 DDIM 采样器，经运动解码器生成最终的运动序列。这一机制使得模型能够根据输入文本的语义内容，自动选择最匹配的采样区域，从而提升生成运动的语义准确性和真实感。

### 模块四：加权潜在向量融合

在优化过程中，当需要将多个人类反馈的候选潜在向量融合为单一更新方向时，采用 softmax 加权平均：

$$ z^{*} = \sum_{i=1}^{m} \mathrm{softmax}(\mathbb{I}_1^i) \cdot \mathcal{X}_1^i $$

其中 $\mathbb{I}_1^i$ 为第 $i$ 个候选的排序指标值，$\mathcal{X}_1^i$ 为对应的候选潜在向量。该公式利用排序信息的 softmax 归一化权重，将高质量候选赋予更大权重，实现平滑的潜在空间更新。

### 底层扩散模型损失

HuTuMotion 构建于 **MLD**（Chen et al., CVPR 2023）的潜在扩散框架之上，其训练目标保持不变：

$$ \mathcal{L}_{\mathrm{MLD}} := \mathbb{E}_{\epsilon, t, c}\left[\|\epsilon - \epsilon_{\theta}(z_t, t, \tau_{\theta}(c))\|_2^2\right] $$

其中 $\epsilon$ 为添加的高斯噪声，$z_t$ 为时间步 $t$ 的噪声潜在变量，$\tau_{\theta}(c)$ 为 CLIP 文本编码器输出的条件嵌入。该损失仅用于预训练扩散模型，HuTuMotion 在推理时通过调整先验分布实现性能提升，**无需重新训练或微调扩散模型本身**。

### 补充图表

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/008_Figure_5.jpg]]
*Figure 5: Text embedding (left) and optimal latent distribution (right) clustering by t-SNE. We initially applied spectral clustering to random 50 text embeddings, categorizing them into 8 distinct classes based on cosine similarity matrix. Subsequently, we employed the labels assigned to the text embeddings to visualize the t-SNE results of the 50 optimal latent distributions*



## 实验与关键发现

### 主实验结果

HuTuMotion 在两个主流文本驱动人体运动生成基准数据集 HumanML3D 和 KIT 上进行了全面评估。评估指标包括 R Precision（Top1/Top2/Top3）、FID、MM Dist、Diversity 和 MModality，所有指标均重复 20 次实验并报告 95% 置信区间。基线方法涵盖 **MLD**（Chen et al., CVPR 2023）、**MDM**（Tevet et al., 2022）、**T2M**（Guo et al., CVPR 2022a）和 **TEMOS**（Petrovich, Black, and Varol, ECCV 2022）等代表性方法。

在 HumanML3D 数据集上（Table 1），HuTuMotion 在 FID 指标上取得了突破性改善：使用 K-Means 聚类中心文本的 Ours* 达到 **0.224 ± 0.006**，相比基线 MLD 的 0.473 ± 0.013，FID 降低了约 **52.6%**。在语义对齐指标 R Precision Top1 上，Ours 达到 **0.497 ± 0.002**，优于 MLD 的 0.481 ± 0.003。这一结果表明，仅通过调整潜在空间的先验分布并引入少量人类反馈，即可在不重新训练扩散模型的前提下大幅提升生成运动的真实感和语义准确性。

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/002_Table_1.jpg]]
*Table 1: Comparison of text-to-motion synthesis on HumanML3D (Guo et al. 2022b) dataset. ∗ means using the texts of cluster’s centroid of K-means. These metrics are evaluated by the motion encoder from (Guo et al. 2022a). For each metric, we repeat the evaluation 20 times and report the average with a 95% confidence interval. We employ real motion as a reference and sort all approaches by descending FIDs. Bold and underline indicate the best and the second best result*

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/003_Table_2.jpg]]
*Table 2: Comparison of text-to-motion synthesis on KIT (Plappert, Mandery, and Asfour 2016) dataset. ∗ means using the texts of cluster’s centroid of K-means. Reported metrics are the same as Table 1. Bold and underline indicate the best and the second best result*

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/006_Table_3.jpg]]
*Table 3: Effect of σ on HumanML3D (Guo et al. 2022b) dataset. Reported metrics are the same as Table 1. Bold and underline indicate the best and the second best result*

在 KIT 数据集上（Table 2），HuTuMotion 同样展现出显著的性能优势。Ours* 的 FID 降至 **0.201 ± 0.064**，而 MLD 为 0.404 ± 0.027，降幅约 50.2%。R Precision Top1 方面，Ours 达到 **0.411 ± 0.005**，超越 MLD 的 0.390 ± 0.008。两个数据集上 FID 的显著改善，直接验证了核心瓶颈假设——标准正态先验 N(0, I) 未能充分反映运动数据的真实分布特性，而通过人类反馈优化的先验分布 N(z_m^{**}, σ²) 有效引导采样朝向更高质量的区域。

定性结果（Figure 2, Figure 8）进一步佐证了定量指标：HuTuMotion 生成的运动序列在帧间过渡的自然度和与文本描述的细粒度语义对齐方面均优于基线方法，尤其在需要捕捉“老人走路缓慢”等细粒度属性时表现更为突出。

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/004_Figure_2.jpg]]
*Figure 2: Qualitative results on HumanML3D (Guo et al. 2022b) dataset. The darker colors indicate the later frame in time*

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/011_Figure_8.jpg]]
*Figure 8: More visualization comparison results. The darker colors indicate the later frame in time*

### 消融研究

**超参数 σ 的影响。** Table 3 展示了先验分布标准差 σ 在 HumanML3D 上的消融结果。当 σ 取 0.1 时 FID 最优，σ 取 0.2 时 R Precision Top1 最优，σ 取 0.4 时 Diversity 最高。综合权衡语义对齐、生成质量和多样性，论文默认选择 **σ = 0.2**。这一参数控制着从优化均值 z_m^{**} 周围采样的探索范围：过小则多样性不足，过大则可能偏离人类偏好的高质量区域。

**代表性文本数量的影响。** Figure 4 展示了代表性文本数量从 1 增加到 50 对 R Precision Top1、FID 和 MM Dist 的影响。结果显示，性能并未随数量增加而持续提升，使用 **5 个代表性文本**即可在优化开销和生成质量之间取得良好平衡。这一发现验证了方法的实用价值：仅需对极少量代表性文本进行人类反馈优化，即可覆盖数据集中主要的运动语义类别。

### 个性化与风格感知生成

HuTuMotion 的框架天然支持个性化和风格化运动生成，无需额外训练。对于个性化生成，用户可提供描述自身动作风格的代表性文本，通过人类反馈优化获得对应的先验分布，推理时即可生成符合个人风格的运动序列。对于风格感知生成，方法为每种风格描述符（如“优雅的”、“僵硬的”）构建对应的风格-潜在向量对集合 {(ST₁, z₁**), ..., (ST_M, z_M**)}，在推理时根据所需的风格选择相应的先验分布。Figure 3 和 Figure 9 展示了相关定性结果，验证了该方法在无需重新训练的情况下实现风格迁移和个性化生成的能力。

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/005_Figure_3.jpg]]
*Figure 3: Personalized (left) and style-aware motion generation (right). More results are provided in the supplementary material. The darker colors indicate the later frame in time*

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/012_Figure_9.jpg]]
*Figure 9: Personalized (left) and style-aware motion generation (right). The darker colors indicate the later frame in time. The darker colors indicate the later frame in time*

### 失败模式与局限性

尽管 HuTuMotion 在主实验结果上取得了显著提升，论文明确指出了以下局限性：

1. **框架依赖性**：该方法被限制在潜在运动扩散模型（MLD）框架内，无法直接推广到显式扩散模型（如 MDM）。根本原因在于显式扩散模型的高维原始运动空间难以通过零阶优化有效搜索。

2. **长文本处理能力有限**：当输入文本包含多个连续动作描述时，底层 MLD 模型本身存在动作遗漏问题，HuTuMotion 对此问题的改善相对有限，因为该方法主要优化先验分布而非模型的条件生成能力。

3. **人工反馈依赖**：虽然所需反馈量极少（仅对 5 个代表性文本进行排序），但仍需一定人工参与，且反馈质量可能影响最终性能。如何通过自动评估指标替代人工排序反馈，实现完全无监督的在线先验优化，仍是一个开放问题。

### 公平性说明

所有对比实验均在相同评估协议下进行：使用 Guo et al.（CVPR 2022a）提供的运动编码器计算评估指标，每种指标重复 20 次并报告 95% 置信区间。除先验采样策略外，扩散模型架构和超参数与 MLD 基线完全一致（“All other settings are consistent with MLD”）。基线方法性能直接引用原论文或公开结果，确保了对比的公平性和可复现性。

### 补充图表

![[assets/figures/papers/paper_list_l1817_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_w/figures/007_Figure_4.jpg]]
*Figure 4: Effect of varying the number of representative texts on R Precision Top 1, FID and MM Dist*



## 定位与知识库关联

HuTuMotion 并非从头构建运动生成模型，而是在现有最优文本驱动运动扩散模型的先验空间之上引入人类反馈优化机制。其直接基线为 **MLD**（Chen et al., CVPR 2023），该工作将运动扩散过程从原始运动空间压缩至潜在空间，通过条件扩散模型实现文本到运动的生成。MLD 的核心训练目标为：

$$\mathcal{L}_{\mathrm{MLD}} := \mathbb{E}_{\epsilon, t, c}\left[\|\epsilon - \epsilon_{\theta}(z_t, t, \tau_{\theta}(c))\|_2^2\right]$$

其中 $\tau_{\theta}(c)$ 为 CLIP 文本编码器的输出。在推理时，MLD 从标准正态先验 $\mathcal{N}(0, I)$ 中采样潜在变量 $z$，再经 DDIM 采样器解码为运动序列。HuTuMotion 完全保留了 MLD 的模型架构与训练权重，唯一的修改在于将推理时的先验分布从固定的 $\mathcal{N}(0, I)$ 替换为经人类反馈优化的高斯分布 $\mathcal{N}(z_m^{**}, \sigma^2)$，其中均值 $z_m^{**}$ 由代表性文本的优化潜在向量决定，标准差 $\sigma=0.2$ 为超参数。

在更广泛的文本驱动运动生成谱系中，其他代表性基线包括：**MDM**（Tevet et al., 2022）在原始运动空间上进行扩散生成，避免了潜在空间的压缩误差，但其高维特性使得直接对先验进行人类反馈优化在计算上不可行；**T2M**（Guo et al., CVPR 2022）基于 VQ-VAE 框架，通过离散码本实现运动生成，缺乏连续的潜在先验空间可供调优；**TEMOS**（Petrovich, Black, and Varol, ECCV 2022）采用 Transformer VAE 架构，同样使用固定的标准正态先验。HuTuMotion 的核心创新——基于少量人类排序反馈在线优化先验分布——在原理上可迁移至任何具备连续潜在空间的生成框架，但论文明确指出，由于显式扩散模型（如 MDM）的高维性难以优化，当前方法被限制在潜在运动扩散框架内。

方法的关键适用边界体现在三个层面。第一，**模型依赖**：HuTuMotion 的性能上限受限于底层 MLD 模型的生成能力；当处理包含大量动作描述的长文本提示时，底层 MLD 模型容易遗漏部分动作，本方法对此问题的改善相对有限。第二，**反馈质量**：方法依赖少量人工排序反馈，虽然数量少（默认仅需 5 个代表性文本的优化），但仍然需要人工参与，且反馈质量可能影响最终性能——若排序信息噪声过大，零阶梯度估计器 $\tilde{g}(z) = \frac{1}{|\mathcal{E}|} \sum_{(i,j)\in\mathcal{E}} \frac{\xi_j - \xi_i}{\mu}$ 的优化方向将偏离真实偏好。第三，**文本覆盖**：推理时通过输入文本与代表性文本的余弦相似度选择先验分布，若输入文本的语义与所有代表性文本差异较大，所选先验可能并非最优，导致生成质量下降。

消融实验揭示了两个关键设计选择。代表性文本数量从 1 增加到 50 并未持续提升性能（Figure 4），默认使用 5 个代表性文本在性能与优化开销间取得平衡，表明少量精心选择的代表性文本足以覆盖主要运动语义空间。标准差 $\sigma$ 的消融（Table 3）显示：$\sigma=0.2$ 时 R Precision Top1 最优，$\sigma=0.1$ 时 FID 最优，$\sigma=0.4$ 时 Diversity 最高，综合选择 $\sigma=0.2$ 体现了语义对齐与生成多样性之间的折中。

开放问题包括：（1）如何将该方法扩展至显式扩散模型或其他生成框架，突破当前对潜在空间的依赖；（2）能否通过自动评估指标替代人工排序反馈，实现完全无监督的在线先验优化；（3）对于非常长的动作序列描述，如何保证生成的运动能完整覆盖所有动作；（4）少样本反馈的具体所需数量在不同任务间如何确定；（5）优化的潜在分布是否具有跨数据集的泛化能力，能否迁移到未见过的运动类型。这些问题指向了人类反馈驱动的生成模型从“特定框架适配”走向“通用框架集成”的关键挑战。



## 原文 PDF

![[paperPDFs/AAAI_2024/HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_with_Minimal_Feedback.pdf]]
