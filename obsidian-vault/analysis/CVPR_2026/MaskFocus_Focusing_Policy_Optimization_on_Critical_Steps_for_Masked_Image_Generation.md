---
title: "MaskFocus: Focusing Policy Optimization on Critical Steps for Masked Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MaskFocus_Focusing_Policy_Optimization_on_Critical_Steps_for_Masked_Image_Generation.pdf
project_link: null
code_link: "https://github.com/zghhui/MaskFocus"
aliases:
- MaskFocus
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过度量采样步长与最终生成图像之间的余弦相似度差异（信息增益）识别关键步长，并将策略优化聚焦于这些高价值步长，同时利用熵引导的动态路由采样平衡探索与利用。
primary_logic: 采样过程中的不同步长对最终图像的贡献并非均匀：早期步长迅速建立整体结构和外观，信息增益更大；通过信息增益可定位关键步长并集中优化，在提升质量的同时显著降低计算开销。
claims:
- 早期掩码token已包含最终生成图像的有效信息，且不同步长的信息增益存在显著差异。
- 基于余弦相似度信息增益选择的关键步长相比基线方案能稳定提升生成指标。
- 引入熵引导的动态路由采样后模型在图像质量和指令遵循方面均获得提升。
- GenEval 上 Overall↑ = 0.76
---

# MaskFocus: Focusing Policy Optimization on Critical Steps for Masked Image Generation

> [!tip] 核心洞察
> 采样过程中的不同步长对最终图像的贡献并非均匀：早期步长迅速建立整体结构和外观，信息增益更大；通过信息增益可定位关键步长并集中优化，在提升质量的同时显著降低计算开销。

| 字段 | 内容 |
|------|------|
| 中文题名 | MaskFocus: 面向掩码图像生成关键步长的策略优化聚焦 |
| 英文题名 | MaskFocus: Focusing Policy Optimization on Critical Steps for Masked Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.18766) · [Code](https://github.com/zghhui/MaskFocus) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MaskFocus |
| Dataset | GenEval, DrawBench |

> [!tip] 效果简介
> - GenEval 上，Overall↑ 0.76 vs 0.73 (Meissonic + MaskGRPO) (+0.03)；Sing Obj.↑ 0.99 vs 0.98 (Meissonic + MaskGRPO) (+0.01)；Two Obj.↑ 0.64 vs 0.65 (Meissonic + MaskGRPO) (-0.01)。
> - DrawBench (Human Preference) 上，DEQA Score↑ 4.39 vs 4.35 (Meissonic + MaskGRPO) (+0.04)；PickScore↑ 22.39 vs 22.34 (Meissonic + MaskGRPO) (+0.05)；HPS↑ 35.52 vs 35.48 (Meissonic + MaskGRPO) (+0.04)。

## 概要

掩码生成模型（Masked Generative Models）在文本到图像（T2I）生成中展现了巨大潜力，但其强化学习（RL）训练面临一个核心瓶颈：基于完整采样轨迹的策略优化计算成本高昂，而现有方法或采用整轨迹优化，或按掩码比率简单选择步长，均未充分利用各采样步长对最终图像的非均匀贡献，导致性能次优。

本文提出 **MaskFocus**，核心洞察在于：采样过程中的不同步长对最终图像的贡献并非均匀——早期步长迅速建立整体结构和外观，信息增益更大。基于此，MaskFocus 通过度量各步长图像嵌入与最终生成图像嵌入之间的余弦相似度差异（信息增益）来识别关键步长，并将策略优化聚焦于这些高价值步长；同时引入熵引导的动态路由采样策略，在组内平衡探索与利用。

实验表明，MaskFocus 在 GenEval 基准上 Overall 指标达到 0.76（基线 Meissonic + MaskGRPO 为 0.73），在 DrawBench 人类偏好指标（DEQA、PickScore、HPS、ImageReward）上全面超越基线。消融实验验证了关键步长选择与动态路由采样两个模块的独立贡献：移除关键步长选择后 GenEval Overall 降至 0.72，移除动态路由采样后降至 0.74，且图像质量指标下降更为显著。

掩码生成模型（Masked Generative Models, MGMs）通过在离散潜在空间中逐步掩码与重构token来生成图像，因其推理效率优势受到广泛关注。近期工作将强化学习（Reinforcement Learning, RL）引入MGM训练，利用GRPO等策略优化方法提升生成质量与指令遵循能力。然而，现有RL训练范式面临一个核心瓶颈：**基于完整采样轨迹的策略优化计算成本高昂，而随机步长优化或基于掩码比率的固定选择无法充分利用各步长对最终图像的非均匀贡献，导致性能次优**。

具体而言，现有方法存在两个关键缺口。其一，早期工作如**Mask-GRPO**（Luo et al., arXiv 2025）对完整采样轨迹进行策略优化，计算开销随采样步数线性增长。其二，**MaskGRPO**（Ma et al., arXiv 2025）尝试按掩码比率选择步长以降低成本，但这一选择策略忽略了不同步长对最终生成图像贡献的差异——并非所有步长同等重要。

本文的动机源于一个关键观察：**采样过程中的不同步长对最终图像的贡献并非均匀**。如Figure 2(a)所示，早期步长的掩码token已隐含最终图像的整体结构和外观信息，包含充足的有效信息。进一步地，通过度量各步长图像嵌入与最终生成图像嵌入之间的余弦相似度$S_t = \text{CosSim}(E_t, E_T)$及其相邻步长的绝对差异$V_t = |\Delta S_t| = |S_{t+1} - S_t|$（即**信息增益**），可以发现图像在采样过程中的变化并不均匀——早期某些步长对生成图像具有更显著的影响（Figure 2(b)）。此外，不同样本在生成过程中呈现不同的熵轨迹：低熵意味着更确定性的采样，限制了探索，使其更难以产生更高的图像质量（Figure 2(c)）。

基于上述观察，本文提出**MaskFocus**，核心思路是：通过信息增益定位关键步长，将策略优化聚焦于这些高价值步长，同时引入熵引导的动态路由采样以平衡探索与利用，从而在提升生成质量的同时显著降低计算开销。

## 核心方法与创新机理

MaskFocus 的核心创新在于**将掩码生成模型的策略优化从完整轨迹压缩到关键步长**，从而在提升生成质量的同时显著降低计算开销。这一目标的实现依赖于两个紧密耦合的机制：**关键步长选择（Critical Step Select, CSS）** 与 **熵引导的动态路由采样（Dynamic Routing Sampling, DR-Sampling）**。

### 关键步长选择：信息增益驱动的优化聚焦

掩码生成模型的采样过程包含多个步长，但各步长对最终图像的贡献并非均匀。如 Figure 2(b) 所示，早期步长迅速建立图像的整体结构与外观，信息增益更大；后期步长的贡献则趋于平缓。MaskFocus 通过量化这一非均匀性，将策略优化聚焦于最具价值的步长。

具体而言，CSS 计算每个采样步长 $t$ 的图像嵌入 $E_t$ 与最终生成图像嵌入 $E_T$ 之间的余弦相似度 $S_t = \text{CosSim}(E_t, E_T)$，并以相邻步长的相似度绝对差值作为该步的信息增益 $V_t = |\Delta S_t| = |S_{t+1} - S_t|$。随后选取信息增益最高的 Top-K 步长作为关键步长进行策略优化（Eq. 4–6）。

这一设计直接回应了现有方法的瓶颈：**MaskGRPO**（Ma et al., arXiv 2025）按掩码比率选择步长，**Mask-GRPO**（Luo et al., arXiv 2025）则对完整轨迹进行优化，两者均未利用步长贡献的非均匀性，导致计算浪费或性能次优。消融实验（Table 3）证实，移除 CSS 后 GenEval Overall 从 0.76 降至 0.72，DEQA 从 4.39 降至 4.34，PickScore 从 22.39 降至 22.34，验证了集中优化关键步长的有效性。

### 动态路由采样：熵引导的探索-利用平衡

仅定位关键步长尚不足以充分释放模型潜力——采样过程中的探索不足同样限制生成质量。如 Figure 2(c) 所示，不同样本在生成过程中呈现差异化的熵轨迹：低熵样本的采样更确定性，限制了探索空间，难以产生更高质量的图像。

DR-Sampling 通过熵引导的组内动态路由解决这一问题。对于每个样本 $i$，计算其在码本 token 上的熵 $H_i = -\sum_{v \in \mathcal{V}} p(v) \log p(v)$（Eq. 7），将高熵样本路由到标准置信度采样的开发分支，将低熵样本路由到探索分支。探索分支通过动态温度调制 $T_i = T e^{-H_{i,j}/\alpha} + \theta$（Eq. 8）对低熵 token 施加与当前位置熵 $H_{i,j}$ 相关的温度扰动，鼓励更广泛的 token 探索。

消融实验（Table 3）表明，移除 DR-Sampling 后 GenEval Overall 从 0.76 降至 0.74，PickScore 从 22.39 降至 22.31，图像质量下降更为明显，证实了探索机制对生成质量的关键作用。

### 与基线方法的 changed slots 对比

MaskFocus 相对于现有基线方法在三个关键设计槽位上实现了实质性改变：

| 设计槽位 | 基线方案 | MaskFocus 方案 |
|---------|---------|---------------|
| 策略优化步长选择 | 基于掩码比率的固定选择（MaskGRPO）或完整轨迹优化（Mask-GRPO） | 基于余弦相似度信息增益的关键步长选择（CSS） |
| 概率估计范围 | 仅使用被采样的高置信度 token 概率 | 使用所有掩码 token 的概率，利用掩码 token 已隐含最终图像信息的特性 |
| 采样策略 | 标准置信度采样（贪心保留高置信度 token） | 熵引导的组内动态路由采样（DR-Sampling） |

三个 changed slots 形成因果链条：DR-Sampling 在采样阶段增强探索以产生更优轨迹，CSS 在优化阶段识别高价值步长以降低计算成本，全掩码 token 概率估计则为策略优化提供更完整的信号。这一设计使得 MaskFocus 在 GenEval 上达到 Overall 0.76（+0.03 vs. Meissonic + MaskGRPO），在人类偏好指标上全面领先（Table 2）。

MaskFocus 的整体 pipeline 由三个核心模块串联构成，分别为**动态路由采样（Dynamic Routing Sampling, DR-Sampling）**、**关键步长选择（Critical Step Select, CSS）**和**掩码打乱与重掩码（Mask Shuffling & Remasking）**，最终通过 **GRPO 策略优化**完成模型更新（见 Figure 3）。

![[assets/figures/papers/paper_list_l2542_https_arxiv_org_abs_2512_18766/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our method. 1) Dynamic Routing Sampling (DR-Sampling). During the sampling process, we perform a more exploratory sampling strategy on low-entropy samples, while using normal sampling on high-entropy samples. 2) Critical Step Select (CSS). Then, we determine the critical steps in the sampling trajectories and obtain the corresponding masks based on the cosine similarity between the intermediate embeddings and the final generated embedding. 3) We randomly shuffle masks and re-mask the generated tokens and predict the probabilities of these masked tokens to optimize the training objective (see left). Detail above procedures are in Alg. 1*

### Pipeline 流程

1. **动态路由采样（DR-Sampling）**  
   在采样阶段，模型对每个样本生成完整的掩码图像生成轨迹。DR-Sampling 根据样本熵将组内样本动态分流：高熵样本进入利用分支（exploitation branch），采用标准置信度采样；低熵样本进入探索分支（exploration branch），施加基于熵的动态温度扰动以鼓励探索。这一设计旨在缓解低熵样本因确定性过强而导致的探索不足问题，平衡利用与探索。

2. **关键步长选择（CSS）**  
   对 DR-Sampling 生成的采样轨迹，CSS 计算各步长图像嵌入 $E_t$ 与最终生成图像嵌入 $E_T$ 的余弦相似度 $S_t = \text{CosSim}(E_t, E_T)$，进而以相邻步长的相似度绝对差值作为信息增益 $V_t = |\Delta S_t| = |S_{t+1} - S_t|$。CSS 从所有步长中选取信息增益最高的 Top-K 步长作为关键步长，这些步长对最终图像的结构和外观贡献最大（早期步长信息增益尤为显著，见 Figure 2(b)）。

3. **掩码打乱与重掩码**  
   针对选定的关键步长，MaskFocus 对其掩码进行随机打乱，重新掩码对应 token 并估计概率。这一操作构造了策略优化的目标分布，使训练信号集中于高价值步长。

4. **GRPO 策略优化**  
   基于 GRPO 框架，MaskFocus 仅对关键步长进行策略更新，包含重要性比率裁剪和 KL 惩罚。与现有方法（如 MaskGRPO 按掩码比率选择步长或整轨迹优化）不同，MaskFocus 利用所有掩码 token 的概率进行优化，而非仅使用被采样的高置信度 token 概率，充分利用了掩码 token 已隐含最终图像信息的特性。

### 模块关系与数据流

- **输入**：文本提示与初始全掩码图像。
- **DR-Sampling → CSS**：DR-Sampling 输出完整采样轨迹；CSS 接收轨迹中各步长的图像嵌入，输出关键步长索引及对应掩码。
- **CSS → Mask Shuffling & Remasking**：关键步长的掩码经打乱和重掩码后，模型预测被掩码 token 的概率分布。
- **Mask Shuffling & Remasking → GRPO Optimization**：概率分布与奖励信号共同构成 GRPO 的优化目标，驱动策略更新。

### 与基线方法的差异

| 模块/策略 | 基线方法 | MaskFocus |
|-----------|---------|-----------|
| 策略优化步长选择 | MaskGRPO 按掩码比率选择步长；Mask-GRPO 整轨迹优化 | CSS 基于余弦相似度信息增益选择关键步长 |
| 概率估计范围 | 仅使用被采样的高置信度 token 概率 | 使用所有掩码 token 的概率 |
| 采样策略 | 标准置信度采样（贪心保留高置信度 token） | DR-Sampling 熵引导的组内动态路由，低熵样本施加动态温度扰动 |

消融实验表明，移除 CSS 后 GenEval Overall 从 0.76 降至 0.72，移除 DR-Sampling 后 GenEval Overall 降至 0.74 且 PickScore 下降更明显（22.39 → 22.31），验证了两个模块对最终性能的关键贡献（Table 3）。

![[assets/figures/papers/paper_list_l2542_https_arxiv_org_abs_2512_18766/figures/001_Figure_1.jpg]]
*Figure 1: (a) For masked generative models, certain steps in the sampling process are more valuable. The core of our method is to find these steps and perform policy optimization on them. (b) Our method achieves significant performance gains across multiple T2I benchmarks*

MaskFocus 的核心由三个紧密耦合的模块构成：**动态路由采样（DR-Sampling）**负责生成高质量且多样化的采样轨迹，**关键步长选择（CSS）**从轨迹中定位最具优化价值的步长，**掩码打乱与重掩码**则利用选定步长构造策略优化目标。三者协同工作，最终通过 GRPO 完成策略更新。

### 1. 概率估计基础

掩码生成模型在给定可见 token $z_V$ 和文本提示的条件下，并行预测所有掩码 token 的概率：

$$p(z_M | z_V) = \prod_{i \in M} p(z_i | z_V)$$

与现有工作仅使用被采样的高置信度 token 进行优化不同，MaskFocus 利用**所有掩码 token 的概率**进行估计。这一设计基于论文的核心发现：早期掩码 token 已隐含最终生成图像的有效信息（Figure 2(a)），因此全量概率估计能提供更丰富的优化信号。

### 2. 关键步长选择（Critical Step Select, CSS）

CSS 模块的目标是从完整的 $T$ 步采样轨迹中，识别出对最终图像贡献最大的关键步长。

**步长价值度量**：对于第 $t$ 步生成的图像嵌入 $E_t$ 与最终生成图像的嵌入 $E_T$，计算其余弦相似度：

$$S_t = \text{CosSim}(E_t, E_T)$$

该相似度度量了中间结果与最终输出的接近程度。

**信息增益定义**：相邻步长之间余弦相似度的绝对差值，被定义为该步的信息增益 $V_t$：

$$V_t = |\Delta S_t| = |S_{t+1} - S_t|$$

$V_t$ 越大，表明该步对图像变化的贡献越显著，因而具有更高的优化价值。Figure 2(b) 的实验表明，不同步长的信息增益呈现显著的非均匀分布，早期步长的增益更为突出。

**关键步长选取**：从所有步长中选择信息增益最高的 Top-K 步长作为关键步长：

$$k = \arg\max_{t \in 1,...,T-1} \Delta V_t$$

后续的策略优化仅聚焦于这些被选中的关键步长，从而在保持优化效果的同时大幅降低计算开销。

### 3. 动态路由采样（Dynamic Routing Sampling, DR-Sampling）

DR-Sampling 模块旨在解决标准置信度采样中低熵样本探索不足的问题。Figure 2(c) 显示，不同样本在生成过程中呈现差异化的熵轨迹——低熵意味着采样过于确定，限制了生成质量的进一步提升。

**样本熵计算**：对于组内的每个样本 $i$，计算其在所有码本 token 上的熵：

$$H_i = -\sum_{v \in \mathcal{V}} p(v) \log p(v)$$

**分支路由策略**：根据样本熵将组内样本分为两支：
- **高熵样本**（熵值较高的半数样本）：路由到**开发分支（Exploitation）**，采用标准置信度采样，保留高置信度 token；
- **低熵样本**（熵值较低的半数样本）：路由到**探索分支（Exploration）**，施加动态温度扰动以鼓励多样性。

**动态温度调制**：对于探索分支中的低熵样本，根据当前 token 位置 $j$ 的局部熵 $H_{i,j}$ 动态调整采样温度：

$$T_i = T e^{-\frac{H_{i,j}}{\alpha}} + \theta$$

其中 $T$ 为基础温度，$\alpha$ 和 $\theta$ 为控制参数。熵越低，有效温度越高，采样越随机；随着生成推进、熵自然升高，温度逐渐回归基础值。这一机制在保持生成稳定性的前提下，有效增强了对低熵样本的探索能力。

### 4. 掩码打乱与策略优化

对 CSS 选定的关键步长，MaskFocus 对其对应的掩码进行随机打乱（Mask Shuffling），随后重新掩码 token 并估计概率，构造策略优化目标。最终通过 GRPO 框架进行策略更新，包含重要性比率裁剪和 KL 惩罚，且**仅对关键步长进行优化**，避免了对全轨迹优化的高昂计算成本。

### 5. 模块间协作关系

三个模块形成完整的训练闭环：DR-Sampling 在采样阶段平衡探索与利用，产生多样化的轨迹；CSS 在轨迹评估阶段定位关键步长，提供优化焦点；掩码打乱与 GRPO 优化则利用选定步长高效更新策略。消融实验（Table 3）验证了各模块的独立贡献：移除 CSS 后 GenEval Overall 从 0.76 降至 0.72，移除 DR-Sampling 后降至 0.74，且 PickScore 的下降更为显著，表明缺乏探索对图像质量的损害尤为突出。

## 实验与关键发现

### 核心实验设置

MaskFocus 以 **Meissonic** 作为基础掩码生成模型（backbone），在 Meissonic 的官方 RL 训练框架上构建。对比基线包括：原版 Meissonic、Meissonic 结合 **MaskGRPO**（Ma et al., arXiv 2025）——一种按掩码比率选择步长的现有 RL 方法，以及早期将 GRPO 适配到掩码生成任务的 **Mask-GRPO**（Luo et al., arXiv 2025）。评估覆盖组合图像生成基准 **GenEval** 和人类偏好指标（**DEQA**、**PickScore**、**HPS**、**ImageReward**），并在 DrawBench 上进行人类偏好评估。

### 主实验结果

#### GenEval 组合生成基准

Table 1 展示了 GenEval 上的量化对比。MaskFocus 在 Overall 指标上达到 **0.76**，较 Meissonic + MaskGRPO 的 0.73 提升 **+0.03**，在所有对比方法中取得最优。在细粒度子任务上，Sing Obj. 从 0.98 提升至 0.99，Counting 和 Colors 等指令遵循任务也有稳定增益。值得注意的是，Two Obj. 子任务出现微弱下降（0.64 vs. 0.65），提示多目标组合场景下关键步长选择策略可能存在进一步优化的空间。

![[assets/figures/papers/paper_list_l2542_https_arxiv_org_abs_2512_18766/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison results on the GenEval benchmark. - represents unreported. The best result is in green*

| 方法 | Overall↑ | Sing Obj.↑ | Two Obj.↑ | Counting↑ | Colors↑ | Position↑ | Color Attri.↑ |
|------|----------|------------|-----------|-----------|---------|-----------|---------------|
| Meissonic | 0.70 | 0.97 | 0.55 | 0.47 | 0.69 | 0.28 | 0.41 |
| Meissonic + MaskGRPO | 0.73 | 0.98 | **0.65** | 0.51 | 0.76 | 0.31 | 0.47 |
| **MaskFocus** | **0.76** | **0.99** | 0.64 | **0.55** | **0.80** | **0.34** | **0.50** |


#### 人类偏好指标

Table 2 展示了人类偏好指标上的对比结果。MaskFocus 在所有四个指标上均超越 Meissonic + MaskGRPO：DEQA 从 4.35 提升至 **4.39**（+0.04），PickScore 从 22.34 提升至 **22.39**（+0.05），HPS 从 35.48 提升至 **35.52**（+0.04），ImageReward 从 1.06 提升至 **1.09**（+0.03）。虽然绝对增益幅度不大，但四个指标的一致性提升验证了聚焦关键步长优化策略在提升图像质量和人类偏好方面的稳健性。

![[assets/figures/papers/paper_list_l2542_https_arxiv_org_abs_2512_18766/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison results on the human preference metrics. The best result is in green*

#### 定性分析

Figure 4 的定性对比显示，MaskFocus 在图像质量和人类偏好（上两行）以及指令遵循任务（下两行，涵盖 Counting、Colors、Attribute Binding 和 Position）上均展现出优于基线的生成效果。Figure 6 进一步对比了 RL 训练前后的采样轨迹，直观展示了 MaskFocus 带来的生成过程变化——经过聚焦优化后，模型的采样路径在关键步长上发生了更显著的信息更新。

### 消融实验

Table 3 系统消融了 MaskFocus 的两个核心组件。

![[assets/figures/papers/paper_list_l2542_https_arxiv_org_abs_2512_18766/figures/007_Table_3.jpg]]
*Table 3: Ablation Result*

**移除关键步长选择（w/o Critical Step Selection）**：将策略优化从聚焦关键步长退化为全步长优化后，GenEval Overall 从 0.76 降至 **0.72**，DEQA 从 4.39 降至 **4.34**，PickScore 从 22.39 降至 **22.34**。这一显著退化直接验证了核心洞察——采样过程中不同步长对最终图像的贡献是非均匀的（Figure 2(b) 已从余弦相似度角度量化了这种非均匀性），盲目在全步长上优化不仅浪费计算，还会引入噪声梯度。

**移除动态路由采样（w/o DR-Sampling）**：将熵引导的动态路由退化为标准置信度采样后，GenEval Overall 从 0.76 降至 **0.74**，PickScore 从 22.39 降至 **22.31**。值得注意的是，PickScore 的下降幅度（-0.08）大于 DEQA 的降幅，表明缺乏探索时图像质量的退化比语义对齐更为明显。这与 Figure 2(c) 的发现一致——低熵样本倾向于确定性采样，限制了探索空间，难以生成更高质量的图像。

| 配置 | GenEval Overall↑ | DEQA↑ | PickScore↑ |
|------|-----------------|-------|------------|
| MaskFocus（完整） | **0.76** | **4.39** | **22.39** |
| w/o Critical Step Selection | 0.72 | 4.34 | 22.34 |
| w/o DR-Sampling | 0.74 | 4.37 | 22.31 |


### 更多对比分析

Figure 5 进一步对比了步长选择策略、采样策略、CFG 和掩码策略的变体。步长选择方面，基于余弦相似度信息增益的 CSS 策略优于基于掩码比率的固定选择（MaskGRPO 的策略）和随机选择；采样策略方面，熵引导的动态路由优于固定温度的探索策略。这些补充实验强化了方法设计的每一环节均有其不可替代的贡献。

![[assets/figures/papers/paper_list_l2542_https_arxiv_org_abs_2512_18766/figures/008_Figure_5.jpg]]
*Figure 5: More comparison results on step selection strategy, sampling strategy, CFG, and mask strategy*

### 失败模式与局限性

尽管 MaskFocus 在主实验结果上表现稳健，但存在以下已知局限：

1. **Off-policy 概率估计误差**：基于轨迹的掩码方法在 off-policy 训练下存在显著的概率估计偏差。具体而言，当使用旧策略采样的轨迹来估计当前策略下掩码 token 的概率时，分布偏移会导致重要性比率估计不准确，进而引发过大的 KL 惩罚项，可能影响训练稳定性和最终性能。这一问题在步长选择范围扩大时可能更为严重。

2. **Two Obj. 任务的退化**：在 GenEval 的 Two Obj. 子任务上，MaskFocus（0.64）略低于 Meissonic + MaskGRPO（0.65）。这可能是因为多目标组合场景下，关键步长的信息增益分布更为分散，Top-K 选择策略可能遗漏了部分对目标交互关系建模至关重要的步长。该点需要进一步验证。

3. **增益幅度有限**：人类偏好指标上的绝对增益（+0.03~+0.05）虽然一致但幅度较小，部分指标的提升可能在统计显著性边界。这提示在 Meissonic 这一特定 backbone 上，RL 微调的收益空间本身有限，更显著的提升可能需要结合更强的基座模型。

## 定位与知识库关联

### 任务谱系：掩码生成模型的强化学习训练

MaskFocus 处于**掩码图像生成（Masked Generative Models, MGM）与强化学习（RL）微调**的交叉地带。MGM 类模型（如 MaskGIT、MUSE、Meissonic）通过迭代掩码-预测范式生成图像，其采样过程天然构成多步决策轨迹，为策略优化提供了直接接口。然而，将 RL 引入 MGM 训练面临两个核心瓶颈：

1. **计算成本**：完整采样轨迹的策略优化（如早期工作 **Mask-GRPO**（Luo et al., arXiv 2025）的整轨迹优化）需要存储和回传所有步长的梯度，训练开销随步数线性增长。
2. **优化效率**：并非所有采样步长对最终图像质量贡献均等——随机选择步长或按掩码比率固定选择（如 **MaskGRPO**（Ma et al., arXiv 2025）选择高掩码比率步长）无法聚焦于真正决定生成质量的关键决策点。

MaskFocus 的核心贡献在于**首次将步长信息增益度量引入 MGM 的 RL 训练**，通过余弦相似度差异定位关键步长，将策略优化从“均匀覆盖”转变为“聚焦高价值步长”，在降低计算开销的同时提升生成质量。

### 关键设计决策与基线对比

| 设计维度 | 基线方法 | MaskFocus 方案 | 变更依据 |
|---------|---------|---------------|---------|
| **策略优化步长选择** | MaskGRPO：按掩码比率固定选择高掩码步长 | 基于余弦相似度信息增益的关键步长选择（CSS） | 信息增益直接度量步长对最终图像的贡献，而非依赖启发式掩码比率（Figure 2b） |
| **概率估计范围** | 仅使用被采样的高置信度 token | 使用所有掩码 token 的概率 | 早期掩码 token 已隐含最终图像的有效信息（Figure 2a），扩大估计范围提升梯度信号质量 |
| **采样策略** | 标准置信度采样（贪心保留高置信度 token） | 熵引导的组内动态路由采样（DR-Sampling） | 低熵样本缺乏探索，需要动态温度扰动跳出局部最优（Figure 2c） |

### 方法适用边界

**适用场景**：
- 基于掩码-预测范式的图像生成模型（MGM），采样步数较多（通常 8-64 步），步长间信息增益差异显著。
- 需要 RL 微调提升图像质量、人类偏好或指令遵循能力的场景。
- 计算资源受限条件下，需在训练效率和生成质量间取得平衡。

**不适用或需谨慎的场景**：
- 采样步数极少（如 1-2 步）的模型：步长选择空间有限，CSS 的收益可能不显著。
- 扩散模型：其连续去噪过程与 MGM 的离散掩码-预测范式存在本质差异，信息增益的定义和关键步长选择机制需要重新设计。
- 在线策略训练：当前方法基于 off-policy 轨迹，存在概率估计误差（见下文局限）。

### 局限性与开放问题

**已知局限**：

1. **Off-policy 概率估计误差**：基于轨迹的掩码方法在 off-policy 训练下存在显著的概率估计偏差，导致过大的 KL 惩罚，可能影响训练稳定性和最终性能。这是将 GRPO 适配到 MGM 场景的固有挑战——采样轨迹来自旧策略，而优化目标需要当前策略的概率估计，两者分布偏移会放大重要性比率估计的方差。

2. **关键步长选择的泛化性**：CSS 依赖余弦相似度信息增益，该度量在 DINOv2 嵌入空间上计算。对于风格差异极大或域外（OOD）的生成任务，嵌入空间的语义对齐程度可能下降，影响关键步长识别的准确性。论文未在极端域偏移场景下验证该机制。

3. **超参数敏感性**：DR-Sampling 中的动态温度调制（Eq.8）引入了温度基数 $T$、衰减系数 $\alpha$ 和偏置 $\theta$ 三个超参数。论文未系统报告这些参数在不同模型规模或任务上的调优策略，实际部署可能需要额外的调参成本。

**开放问题**：

1. **如何进一步减轻 off-policy 训练中的概率估计误差？** 可能的探索方向包括：引入重要性重采样（importance resampling）修正分布偏移，或采用 on-policy 的轨迹收集策略（如 PPO 的 rollout buffer）替代当前的全 off-policy 方案。这直接关系到 RL 训练效率和生成质量的进一步提升。

2. **信息增益度量能否推广到其他生成范式？** 余弦相似度差异本质上是嵌入空间中生成进度的代理度量。对于扩散模型，可类比为去噪步长对最终样本的贡献度量；对于自回归模型，可类比为 token 预测对序列整体质量的边际贡献。这些推广的可行性和有效性尚待验证。

3. **关键步长选择与奖励模型的交互机制**：当前 CSS 仅基于图像嵌入相似度选择步长，未考虑奖励模型（如 ImageReward、PickScore）的信号。是否可以将奖励模型的梯度信息融入步长选择，形成“奖励感知”的关键步长定位，是一个值得探索的方向。

### 知识库定位

MaskFocus 在方法谱系中处于以下位置：

- **上游继承**：策略优化框架来自 **GRPO**（Group Relative Policy Optimization），掩码生成 backbone 基于 **Meissonic**，步长选择动机受扩散模型中时间步重要性研究的启发。
- **同级对比**：与 **MaskGRPO**（Ma et al., arXiv 2025）和 **Mask-GRPO**（Luo et al., arXiv 2025）同属 MGM+RL 方向，但 MaskFocus 在步长选择和采样策略两个维度上做出了差异化设计。
- **下游延伸**：该方法为 MGM 的 RL 训练提供了计算效率优化思路，后续工作可在此基础上探索更精细的步长价值估计、在线策略训练方案，以及跨生成范式的迁移。

## 原文 PDF

![[paperPDFs/CVPR_2026/MaskFocus_Focusing_Policy_Optimization_on_Critical_Steps_for_Masked_Image_Generation.pdf]]
