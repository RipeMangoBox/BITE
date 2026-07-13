---
title: "Diffusion Blend: Inference-Time Multi-Preference Alignment for Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Diffusion_Blend_Inference_Time_Multi_Preference_Alignment_for_Diffusion_Models.pdf
project_link: null
code_link: https://github.com/bluewoods127/DB-2025
openreview_forum_id: M2DXbwO8le
aliases:
- DBDMDKDML
- DBITMPADM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "推理时用户指定的偏好向量w（用于组合基础奖励）和KL修改因子λ（用于控制正则化强度），通过混合不同基础奖励对应的后向扩散过程实现动态对齐。"
primary_logic: "利用Jensen间隙近似将目标扩散过程的控制项表达为基础奖励控制项的线性组合，从而在推理时通过混合后向扩散过程实现多偏好对齐，无需额外微调。"
claims:
- "DB-MPA在加权奖励上显著优于所有基线并接近MORL上限。"
- "DB-KLA可通过λ实现对KL正则化强度的平滑控制，生成与λ专用RL模型相似的图像。"
- "在冲突奖励（JPEG可压缩性 vs VILA美学）下，DB-MPA在所有偏好权重上均获得更高的加权奖励。"
- "增加奖励数量时，DB-MPA和DB-MPA-LS的性能增益保持稳定，而RS显著下降。"
---

# Diffusion Blend: Inference-Time Multi-Preference Alignment for Diffusion Models

> [!tip] 核心洞察
> 利用Jensen间隙近似将目标扩散过程的控制项表达为基础奖励控制项的线性组合，从而在推理时通过混合后向扩散过程实现多偏好对齐，无需额外微调。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散混合：推理时的多偏好对齐扩散模型 |
| 英文题名 | Diffusion Blend: Inference-Time Multi-Preference Alignment for Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=M2DXbwO8le) · [GitHub](https://github.com/bluewoods127/DB-2025) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Diffusion Blend（包含DB-MPA、DB-KLA、DB-MPA-LS三个算法） |
| Dataset | Short-DrawBench (1k test prompts), GenEval (test prompts), 推理时间 (sec/img), SDXL 单提示评估 |

> [!tip] 效果简介
> - Short-DrawBench (1k test prompts) 上，加权奖励 r(w)=w*r1+(1-w)*r2, w=0.5 为 DB-MPA: 0.42，对比 Stable Diffusion: -0.04，变化 +0.46。
> - GenEval (test prompts) 上，图像对齐奖励 r1, 美学奖励 r2 (w=0.5) 为 DB-MPA: r1=0.13, r2=0.47，对比 Stable Diffusion: r1=-0.2, r2=-0.04，变化 r1:+0.33, r2:+0.51。
> - 推理时间 (sec/img) 上，平均单张图像生成时间 为 DB-MPA: 11.11, DB-MPA-LS: 5.64，对比 Stable Diffusion: 5.46，变化 DB-MPA ~2×, DB-MPA-LS 接近基线。

## 概要

扩散模型在文本到图像生成中取得了显著成功，但将其输出与人类偏好对齐仍是一个核心挑战。现有基于强化学习（RL）的微调方法通常针对固定的单一奖励函数和固定的KL正则化强度进行优化。当用户需要同时平衡多个相互冲突的目标（如文本对齐度与美学质量），或希望调整生成结果与预训练模型的偏离程度时，这些方法暴露出根本性瓶颈：**每个新的偏好配置都需要重新训练模型**，计算成本高昂且缺乏灵活性。

**Diffusion Blend** 提出了一套推理时对齐框架，核心思想是：**将不同基础奖励对应的后向扩散过程的控制项进行线性混合，从而在推理时动态合成满足任意用户偏好的新扩散过程，无需额外微调**。该框架包含三个算法：

- **DB-MPA（Multi-Preference Alignment）**：用户指定偏好权重向量 $w$，算法按 $w$ 线性组合多个基础奖励微调模型的漂移项，生成对齐组合奖励 $r(w) = \sum_i w_i r_i$ 的图像。
- **DB-KLA（KL Alignment）**：用户指定KL修改因子 $\lambda$，算法在预训练模型与微调模型之间按 $\lambda$ 插值，实现对正则化强度 $\alpha/\lambda$ 的平滑控制。
- **DB-MPA-LS（LoRA Sampling）**：通过按权重采样单个微调模型来近似DB-MPA，将推理成本从约2倍降低至与标准扩散模型相当，同时保持近似等价于DB-MPA的边际分布。

**核心结论**：在Short-DrawBench和GenEval基准上，DB-MPA在所有偏好权重下均显著优于Rewarded Soup（RS）、CoDe、RGG等基线，并接近为每个偏好单独微调的MORL预言机上界。在冲突奖励场景（JPEG可压缩性 vs 美学质量）和多奖励扩展（2至4个奖励）中，DB-MPA的性能增益保持稳定，而RS的性能显著下降。DB-KLA生成的图像质量与 $\lambda$ 专用RL模型相似，验证了推理时KL控制的可行性。DB-MPA-LS以接近Stable Diffusion v1.5的推理成本实现了与DB-MPA相当的奖励提升。

**方法定位**：Diffusion Blend属于**推理时对齐**范式，区别于需要重新训练的参数融合方法（如Rewarded Soup）和免训练的梯度引导方法（如RGG、CoDe）。其理论基础是将精确控制项的Jensen间隙近似与线性标量化结合，使多偏好对齐问题转化为基础漂移项的线性组合。该方法已在Stable Diffusion v1.5和SDXL上验证，推理时间与计算开销可控，为扩散模型的灵活部署提供了实用方案。

扩散模型在文本到图像生成中取得了显著进展，但预训练模型生成的图像往往无法很好地对齐用户多样化的偏好，例如文本-图像对齐度、美学质量、JPEG可压缩性等。为了将扩散模型与奖励函数对齐，现有方法通常采用强化学习微调（RL fine-tuning），其核心目标是在KL散度正则化约束下最大化期望奖励：

$$\max_{p_0} \mathbb{E}_{x_0 \sim p_0}[r(x_0)] - \alpha \mathrm{KL}(p_0 \| p_0^{\mathrm{pre}})$$

其中 $\alpha$ 控制生成分布与预训练分布的偏离程度。

然而，现有方法存在一个根本性的瓶颈：它们假设固定的单一奖励函数和固定的KL正则化权重 $\alpha$。一旦用户的偏好发生变化——例如希望同时优化文本对齐度和美学质量，或希望调整正则化强度——就需要为每个新的偏好配置重新进行昂贵的微调训练。Rewarded Soup（RS, Rame et al., 2023）尝试通过线性组合微调模型的参数来实现多偏好对齐，但其性能在奖励数量增加时显著下降（Figure 7, Table 6），且无法处理KL正则化强度的动态调整。基于梯度的引导方法如RGG（Chung et al., 2023）和免训练方法如CoDe（Singh et al., 2025）虽然避免了微调，但在多目标平衡和奖励冲突场景下表现有限（Table 5）。

核心挑战在于：**能否设计一种方法，使得在推理时（inference-time）即可生成对齐任意用户指定偏好组合的图像，而无需额外的微调？** 这要求模型能够动态地平衡多个可能相互冲突的奖励目标，同时允许用户灵活控制KL正则化强度。本文正是在这一动机下，提出了扩散混合（Diffusion Blend）框架，通过在推理时混合不同基础奖励对应的后向扩散过程，实现零额外微调的多偏好对齐。

## 核心方法与创新机理

本文的核心创新在于将扩散模型的多偏好对齐从**训练时固定组合**迁移到**推理时动态混合**，通过三个算法（DB-MPA、DB-KLA、DB-MPA-LS）分别解决偏好权重调整、KL正则化强度控制和推理成本问题。

### 推理时偏好向量与KL修改因子：从固定到可调

现有扩散模型RL微调方法的根本瓶颈在于：奖励函数组合和KL正则化强度在训练时即被固化，用户偏好一旦变化就需要为每个新配置重新训练模型。Diffusion Blend将这两个控制维度外化为推理时参数：

- **偏好向量 w**：用户可指定任意基础奖励的线性组合 $r(w) = \sum_{i=1}^{m} w_i r_i$，无需重新训练。
- **KL修改因子 λ**：将训练时的KL系数 α 动态缩放为 α/λ，控制生成分布与预训练模型的距离。

这一设计将“为每个偏好配置训练一个模型”的范式转变为“训练少量基础模型，推理时按需混合”，是方法家族的核心changed slot。

### Jensen间隙近似：线性混合的理论基础

实现推理时混合的关键insight在于**利用Jensen间隙近似将目标扩散过程的控制项表达为基础奖励控制项的线性组合**。

具体而言，对齐目标的最优解对应的反向SDE漂移项为：
$$f^{(r,\alpha)}(x_t, t) = f^{\mathrm{pre}}(x_t, t) - \beta(t) u^{(r,\alpha)}(x_t, t)$$
其中精确控制项 $u^{(r,\alpha)}(x_t, t) = \nabla_{x_t} \log \mathbb{E}_{x_0 \sim p_{0|t}^{\mathrm{pre}}(\cdot|x_t)}\left[\exp\left(\frac{r(x_0)}{\alpha}\right)\right]$ 包含期望与指数的嵌套，无法直接分解。

通过交换期望与指数的顺序（Jensen间隙近似），得到可分解的近似控制项：
$$\bar{u}^{(r,\alpha)}(x, t) = \nabla_x \mathbb{E}_{x_0 \sim p_{0|t}^{\mathrm{pre}}(\cdot|x)}\left[\frac{r(x_0)}{\alpha}\right]$$

基于此，**Lemma 2** 建立了核心线性混合性质——加权奖励对应的漂移项可近似为基础奖励漂移项的线性组合：
$$f^{(r(w),\alpha)}(x_t, t) \approx \sum_{i=1}^{m} w_i f^{(r_i,\alpha)}(x_t, t)$$

近似误差由 $\Delta^{(r,\alpha)}$ 项控制，其理论上界依赖于奖励函数的Lipschitz常数、条件分布变异系数等因素（Lemma 1）。当KL系数 α 非常小时，误差项可能增大，这是方法的主要理论局限。

### DB-MPA：多偏好混合的核心算法

**DB-MPA** 直接利用上述线性混合性质：在推理时，将多个基础奖励对应的RL微调模型的后向扩散过程按权重 w 线性组合。与baseline的关键差异体现在：

| 维度 | 基线方法 | DB-MPA |
|------|---------|--------|
| 奖励函数组合 | 固定的单一奖励或预定义组合 | 推理时用户可调的线性组合 w |
| KL正则化强度 | 固定的 α 值 | 继承训练时的 α，通过DB-KLA进一步调整 |
| 推理时模型使用 | 运行单个微调模型 | 混合多个基础奖励微调模型的后向扩散过程 |

相比 **Rewarded Soup (RS)**（Rame et al., 2023）通过线性组合模型参数实现多偏好对齐，DB-MPA在**扩散过程层面**进行混合，避免了参数空间线性插值可能导致的模式坍塌。实验表明，DB-MPA在所有偏好权重上均显著优于RS（Table 1, w=0.5时加权奖励提升3.92倍），且在奖励数量增加时性能增益保持稳定，而RS显著下降（Figure 7, Table 6）。

### DB-KLA：KL正则化的独立控制维度

**DB-KLA** 将KL正则化强度从训练时参数转变为推理时可调变量。其核心是在预训练模型漂移项 $f^{\mathrm{pre}}$ 和单个RL微调模型漂移项 $f^{(r,\alpha)}$ 之间按因子 λ 插值：
$$f^{(r,\alpha(\lambda))}(x_t, t) \approx (1-\lambda) f^{\mathrm{pre}}(x_t, t) + \lambda f^{(r,\alpha)}(x_t, t)$$

当 λ=0 时退化为预训练模型（无限正则化），λ=1 时等价于原始RL微调模型，λ>1 时进一步放大奖励信号。实验证实DB-KLA可实现对KL强度的平滑控制，生成的图像与为每个λ专门训练的MORL模型高度相似（Figure 6），但无需额外微调成本。

### DB-MPA-LS：保持性能的轻量化采样近似

DB-MPA的推理成本约为标准扩散模型的2倍（11.11 sec/img vs 5.46 sec/img），因为每个去噪步骤需要运行多个微调模型。**DB-MPA-LS** 通过**LoRA采样近似**解决此问题：在每个去噪步骤，按权重概率随机采样单个LoRA适配器，而非计算所有适配器输出的加权和。

**Proposition 2** 保证了两类SDE具有相同的边际分布——确定性凸组合漂移与随机伯努利选择漂移在边际分布上等价。因此DB-MPA-LS以接近Stable Diffusion的推理速度（5.64 sec/img）实现了与DB-MPA相当的奖励提升（Table 1），在极端权重下性能略有下降但整体保持竞争力。

### 创新边界与待验证问题

方法的理论近似依赖Jensen间隙假设，对于高度非线性或非平滑的奖励函数，近似误差可能更显著。当α非常小时，误差项 $L_{t,2}$ 和 $L_{t,3}$ 可能增大（Remark 2）。此外，实验主要在Stable Diffusion v1.5和SDXL上验证，尚未在其他扩散模型架构上检验。如何在不显式访问预训练模型密度的前提下更精确地计算控制项期望，以及如何扩展到非线性标量化的多目标偏好，是值得进一步探索的开放问题。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_M2DXbwO8le/figures/001_Figure_1.jpg]]
*Figure 1: (a). Overview of our Diffusion Blend - Multi Preference Alignment (DB-MPA) Algorithm. Given basis reward functions and any user preference weights w = ( w _ { 1 } , w _ { 2 } ) , DB-MPA generates images aligned with combined reward r ( w ) = w _ { 1 } r _ { 1 } + w _ { 2 } r _ { 2 } (b) During the fine-tuning stage, DB-MPA gets an RL fine-tuned model corresponding to each reward function. (c) During the inference time, DB-MPA blends (mixes) the backward diffusion corresponding to each fine-tuned model according to the user-specified preference w*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_M2DXbwO8le/figures/004_Figure_2.jpg]]
*Figure 2: Comparison of DB-MPA with baselines: Stable Diffusion v1.5 (Rombach et al., 2022), CoDe (Singh et al., 2025), RGG (Chung et al., 2023), rewarded soup (RS) (Rame et al., 2023), and MORL (Roijers et al., 2013). Note that MORL is included only to illustrate the maximum achievable performance by an oracle algorithm. See section 2 for details. For arbitrary preference weight w, algorithms generate images aligned with r ( w ) = w r _ { 1 } + ( 1 - w ) r _ { 2 } , where r1 is text-to-image alignment and r2 is aesthetics. (a) Images for w ∈ {0.2, 0.5, 0.8}. (b) Pareto-front comparison. DB-MPA significantly outperforms baselines and approaches the MORL upper bound. Figure 3: (a) Overview of our Diff...*

Diffusion Blend 框架的核心思想是将**推理时多偏好对齐**拆解为两个阶段：**离线微调阶段**为每个基础奖励函数独立训练一个对齐模型，**推理时混合阶段**根据用户指定的偏好向量动态组合这些模型的逆向扩散过程，从而无需为每个新偏好配置重新训练。

### 框架流程

整个 pipeline 由三个关键模块串联构成：

1. **预训练扩散模型**：提供基础逆向扩散过程 $f^{\mathrm{pre}}(x_t, t)$，对应标准 Stable Diffusion v1.5 或 SDXL 的逆向 SDE。该模型生成符合预训练分布的图像，但未针对任何特定奖励进行优化。

2. **RL 微调模块**：针对每个基础奖励函数 $r_i$，以 KL 正则化目标 $\max_{p_0} \mathbb{E}[r_i(x_0)] - \alpha \mathrm{KL}(p_0 \| p_0^{\mathrm{pre}})$ 进行微调，得到对应的微调模型 $\theta_i^{\mathrm{rl}}$。该阶段为离线执行，每个奖励函数仅需微调一次（通常使用 LoRA 以降低存储开销）。

3. **推理时混合模块**：根据用户指定的偏好权重 $w = (w_1, \ldots, w_m)$，将各微调模型的逆向扩散漂移项进行线性组合，合成新的逆向扩散过程。具体而言，DB-MPA 利用 Lemma 2 的近似关系：
   $$f^{(r(w),\alpha)}(x_t, t) \approx \sum_{i=1}^{m} w_i f^{(r_i,\alpha)}(x_t, t)$$
   在每一步去噪过程中，将各基础奖励对应的漂移项按权重加权求和，替代精确的目标漂移项。这一近似源于 Jensen 间隙假设——将控制项中的期望与指数交换，得到可计算的线性组合形式。

### 三个算法变体

框架包含三个算法，分别解决不同的推理时控制需求：

- **DB-MPA**：实现多偏好对齐。用户指定偏好权重 $w$，算法混合多个基础奖励对应的逆向扩散过程，生成对齐于加权奖励 $r(w) = \sum w_i r_i$ 的图像。
- **DB-KLA**：实现 KL 正则化强度的动态调整。用户指定修改因子 $\lambda$，算法在预训练模型与单个微调模型之间插值：$f^{(r,\alpha(\lambda))} \approx (1-\lambda) f^{\mathrm{pre}} + \lambda f^{(r,\alpha)}$，从而将有效正则化系数缩放为 $\alpha/\lambda$。
- **DB-MPA-LS**：降低 DB-MPA 的推理计算开销。根据 Proposition 2，在每一步去噪时以概率 $w_i$ 随机采样单个微调模型的 LoRA 适配器，而非同时运行所有模型。该方法在保持等价边际分布的前提下，将推理时间从约 2 倍降至接近标准扩散模型水平。

### 输入输出流

**输入**：文本提示 $c$、用户指定的偏好权重 $w$（DB-MPA）或 KL 修改因子 $\lambda$（DB-KLA）。

**推理过程**：从纯噪声 $x_T \sim \mathcal{N}(0, I)$ 开始，在每一步 $t$ 计算混合后的漂移项 $f^{\mathrm{blend}}(x_t, t)$，按标准逆向 SDE 更新 $x_{t-1}$，直至 $t=0$ 输出最终图像 $x_0$。

**输出**：对齐于用户指定偏好配置的生成图像。用户可通过连续调节 $w$ 或 $\lambda$ 实现平滑的偏好控制，无需重新微调或切换模型。

### 问题形式化

扩散模型对齐问题的目标是最大化期望奖励，同时通过KL散度正则化约束生成分布不偏离预训练模型：

$$
\max_{p_0} \mathbb{E}_{x_0 \sim p_0}[r(x_0)] - \alpha \mathrm{KL}(p_0 \| p_0^{\mathrm{pre}})
$$

该目标的最优解具有闭式表达：

$$
p^{\mathrm{tar}}(x_0) = \frac{p^{\mathrm{pre}}(x_0) \exp(r(x_0)/\alpha)}{Z}
$$

其中 $\alpha$ 控制KL正则化强度，$Z$ 为归一化常数。

### 预训练扩散模型的反向过程

预训练扩散模型的反向SDE为：

$$
dx_t = f^{\mathrm{pre}}(x_t, t) dt + \sigma(t) dw_t
$$

其中 $f^{\mathrm{pre}}(x_t, t) = -\frac{1}{2}\beta(t)x_t - \beta(t)\nabla_{x_t}\log p_t(x_t)$ 为漂移项，$\sigma(t) = \sqrt{\beta(t)}$ 为扩散系数。

### 核心模块一：精确控制项与Jensen间隙近似

**Proposition 1** 建立了对齐模型反向过程与预训练模型之间的关系：要从目标分布 $p^{\mathrm{tar}}$ 采样，只需在预训练得分函数上添加控制项 $u^{(r,\alpha)}$：

$$
f^{(r,\alpha)}(x_t, t) = f^{\mathrm{pre}}(x_t, t) - \beta(t) u^{(r,\alpha)}(x_t, t)
$$

其中精确控制项为：

$$
u^{(r,\alpha)}(x_t, t) = \nabla_{x_t} \log \mathbb{E}_{x_0 \sim p_{0|t}^{\mathrm{pre}}(\cdot|x_t)}\left[\exp\left(\frac{r(x_0)}{\alpha}\right)\right]
$$

由于精确控制项中期望与指数非线性耦合，直接计算不可行。**Lemma 1** 通过交换期望和指数的顺序（Jensen间隙近似）得到可计算的近似控制项：

$$
\bar{u}^{(r,\alpha)}(x, t) = \nabla_x \mathbb{E}_{x_0 \sim p_{0|t}^{\mathrm{pre}}(\cdot|x)}\left[\frac{r(x_0)}{\alpha}\right]
$$

近似误差 $\Delta^{(r,\alpha)}(x,t) = u^{(r,\alpha)} - \bar{u}^{(r,\alpha)}$ 的上界为：

$$
|\Delta^{(r,\alpha)}(x,t)| \leq L_{t,1}(x) \times L_{t,2}(x) + L_{t,3}(x)
$$

其中 $L_{t,1}$ 为Lipschitz敏感度，$L_{t,2}$ 为变异系数，$L_{t,3}$ 为平移族偏差。当 $\alpha$ 非常小时，这些误差项可能增大，导致近似质量下降。

### 核心模块二：多奖励漂移混合（DB-MPA）

考虑用户指定的线性奖励组合 $r(w) = \sum_{i=1}^{m} w_i r_i$，**Lemma 2** 建立了组合奖励对应漂移项与基础奖励漂移项之间的关系：

$$
f^{(r(w),\alpha)}(x_t,t) = \sum_{i=1}^{m} w_i f^{(r_i,\alpha)}(x_t,t) + \beta(t)\left(\sum_{i=1}^{m} w_i \Delta^{(r_i,\alpha)} - \Delta^{(r(w),\alpha)}\right)
$$

忽略误差项后，得到DB-MPA的核心近似：**组合奖励对应的漂移项可表达为基础奖励漂移项的线性组合**。推理时，用户只需指定偏好权重向量 $w$，算法即可通过混合多个基础奖励微调模型的后向扩散过程，合成新的反向扩散过程，无需额外微调。

### 核心模块三：KL强度插值（DB-KLA）

DB-KLA允许用户在推理时通过修改因子 $\lambda$ 调整KL正则化强度。令 $\alpha(\lambda) = \alpha / \lambda$，则目标漂移项可近似为预训练模型与微调模型之间的线性插值：

$$
f^{(r,\alpha(\lambda))}(x_t,t) \approx (1-\lambda) f^{\mathrm{pre}}(x_t,t) + \lambda f^{(r,\alpha)}(x_t,t)
$$

当 $\lambda=0$ 时退化为预训练模型（无穷大正则化），$\lambda$ 增大则对齐强度增强。该插值直接来源于 Lemma 2 在单奖励退化情形下的应用。

### 核心模块四：LoRA采样近似（DB-MPA-LS）

DB-MPA需要同时运行多个微调模型，推理成本约为标准扩散模型的2倍。DB-MPA-LS通过随机采样机制降低计算开销：在每个去噪步骤，以与权重 $w_i$ 成比例的概率随机选择一个基础奖励对应的LoRA适配器。**Proposition 2** 保证该随机采样SDE与确定性混合SDE具有相同的边际分布 $p_{X_t}$，从而在维持等价生成分布的前提下，将推理时间降至接近标准扩散模型水平。

## 实验与关键发现

### 实验设置

实验基于 **Stable Diffusion v1.5**（Rombach et al., CVPR 2022）和 **SDXL** 两个预训练扩散模型。奖励函数包括 **ImageReward**（图文对齐）、**VILA**（美学质量，缩放到 [-2, 2]）、**PickScore**（人类偏好，整体偏移 -19）和 **JPEG 可压缩性**。提示数据集使用 **DrawBench** 颜色子集（25 个训练提示）和 **GenEval**（550 个提示），测试集为 Short-DrawBench（1k 测试提示）和 GenEval 测试集。

基线方法包括：
- **Rewarded Soup (RS)**（Rame et al., 2023）：通过线性组合 LoRA 参数实现多偏好对齐
- **CoDe**（Singh et al., 2025）：免训练引导方法
- **RGG**（Chung et al., 2023）：基于奖励梯度引导
- **MORL**（Roijers et al., 2013）：预言机基线，为每个偏好权重单独微调模型，仅用作性能上限参考

所有方法使用相同的奖励模型和提示集。RGG 的梯度经过归一化处理以确保可控性。RS 使用与 DB-MPA 相同的 LoRA 微调检查点进行参数合成。

### 主结果：DB-MPA 多偏好对齐

**定量结果（Table 1）**：在 Short-DrawBench 1k 测试提示上，以等权重偏好（w=0.5）的加权奖励 $r(w) = w r_1 + (1-w) r_2$ 为指标，DB-MPA 达到 **0.42**，显著优于 Stable Diffusion 基线（-0.04），提升 **+0.46**。相比 RS（0.11）、CoDe（0.22）和 RGG（0.32），DB-MPA 分别实现了 3.92×、1.95× 和 1.33× 的性能优势，并接近 MORL 预言机上界（0.46）。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_M2DXbwO8le/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of DB-MPA and baseline methods*

**帕累托前沿（Figure 2、Figure 5）**：在 GenEval 测试集上，DB-MPA 和 DB-MPA-LS 在所有偏好权重 $w \in [0, 1]$ 上均一致支配所有基线方法，帕累托前沿明显外移。具体数值（Table 4）显示，在 w=0.5 时 DB-MPA 的图文对齐奖励 r₁ 为 0.13（基线 SD 为 -0.20），美学奖励 r₂ 为 0.47（基线 SD 为 -0.04），分别提升 +0.33 和 +0.51。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_M2DXbwO8le/figures/012_Table_4.jpg]]
*Table 4: GenEval (test): numerical results ( r _ { 1 } , r _ { 2 } ) corresponding to the Pareto-front plot fig. 5 in the main text. DB-MPA and DB-MPA-LS consistently dominate baselines across preference weights*

**推理成本（Table 1）**：DB-MPA 的推理时间为 **11.11 秒/张**，约为 Stable Diffusion（5.46 秒/张）的 2 倍。这是因为 DB-MPA 需要同时运行两个基础奖励微调模型的反向扩散过程。DB-MPA-LS 将推理时间降至 **5.64 秒/张**，接近基线速度，同时保持与 DB-MPA 相当的奖励提升。

**SDXL 扩展（Table 7）**：在 SDXL 单提示评估中，以 ImageReward（r₁）和 VILA（r₂）为奖励，w=0.5 时 DB-MPA 达到 r₁=0.25、r₂=0.55，相比预训练 SDXL（r₁=-1.05，r₂=0.01）分别提升 **+1.30** 和 **+0.54**，验证了方法在不同模型规模上的有效性。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_M2DXbwO8le/figures/022_Table_7.jpg]]
*Table 7: SDXL single prompt results: r1 = ImageReward, $r _ { 2 } = \mathrm { V I L A }$ . The pretrained SDXL has: $r _ { 1 }$ = - 1 . 0 5 , $r _ { 2 }$ = 0 . 0 1*

### DB-KLA：KL 正则化强度控制

**平滑控制能力（Figure 6a）**：DB-KLA 通过推理时指定的修改因子 λ 实现对 KL 正则化强度的连续控制。当 λ=0 时对应无限正则化（即预训练 SD v1.5），随着 λ 增大，生成图像逐渐远离预训练分布，向奖励对齐方向移动。实验表明 DB-KLA 可生成与 λ 专用 RL 微调模型视觉相似的图像，无需为每个 λ 重新训练。

**定量对齐（Figure 6b）**：DB-KLA 的平均奖励曲线与 MORL 重训练模型紧密吻合，在 λ ∈ [0, 2.0] 范围内均能有效追踪奖励变化趋势，证明推理时 KL 调整的可靠性。

### 冲突奖励下的鲁棒性

**JPEG 可压缩性 vs VILA 美学（Table 5）**：在 Short-DrawBench 1k 测试提示上，使用两个相互冲突的奖励函数（JPEG 可压缩性 r₁ 和 VILA 美学 r₂），DB-MPA 在所有偏好权重（w=0.2, 0.5, 0.8）上均获得最高的加权奖励（WR），分别为 0.44、0.59、0.88，显著优于 RS 和 CoDe。这表明 DB-MPA 即使在奖励目标相互冲突的对抗性设定下，仍能有效实现用户指定的多目标权衡。

### 奖励数量扩展性

**多奖励消融（Figure 7、Table 6）**：将奖励数量从 2 增至 4（依次添加 ImageReward、VILA、JPEG 可压缩性、PickScore），DB-MPA 和 DB-MPA-LS 的性能增益保持稳定，各奖励上的改善幅度（Δr）持续为正且显著。相比之下，RS 的性能增益明显下降，在多个奖励上接近零改善。Figure 7 的柱状图直观展示了这一趋势：DB-MPA 和 DB-MPA-LS 在 R1–R4 上的增益范围为 0.2–0.6，而 RS 始终接近基线。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_M2DXbwO8le/figures/016_Figure_7.jpg]]
*Figure 7: Performance comparison on Short-drawbench 1k test prompts of DB-MPA and baseline algorithms under different numbers of reward models. R1 = ImageReward, R2 = VILA, R3 = Compressibility, R4 = PickScore. Performance improvement is computed as (algorithm reward) - (SD-v1.5 reward). DB-MPA and DV-MPA-LS consistently outperform RS as the number of rewards increases*

**三奖励设置（Figure 8）**：在 m=3 奖励设置下，DB-MPA 在四种权重配置下均优于 RS、RGG 和 CoDe，在图文对齐、美学质量和人类偏好三个维度上同时获得正向改善，验证了方法在多目标场景下的可扩展性。

### 视觉质量与定性分析

**DB-MPA vs DB-MPA-LS 一致性（Figure 11）**：DB-MPA 和 DB-MPA-LS 生成的图像在视觉上高度一致，验证了 LoRA 采样近似在保持生成质量方面的有效性。

**细粒度偏好对齐（Figure 13）**：DB-MPA 相比 RS 展现出更精细的偏好控制能力。在 ImageReward 和美学分数的不同权重组合下，DB-MPA 生成的图像更准确地反映了用户指定的偏好权衡，而 RS 的生成结果在不同权重间差异较小。

**DB-KLA 定性对比（Figure 14、Figure 15）**：DB-KLA 在 λ ∈ {0.2, 0.5, 0.7, 1.0, 1.5, 2.0} 范围内生成的图像与 MORL 重训练模型高度相似，进一步证实推理时 KL 调整可以替代为每个 λ 单独微调的需求。

### 已知局限与失败模式

1. **小 α 下的近似误差**：当 KL 正则化系数 α 非常小时，Jensen 间隙近似中的误差项 $L_{t,2}$ 和 $L_{t,3}$ 可能增大，导致算法性能下降（Remark 2）。这是理论近似的内在限制。
2. **DB-MPA 推理开销**：DB-MPA 的推理时间约为标准扩散模型的 2 倍。DB-MPA-LS 缓解了该问题，但在极端偏好权重下可能略微影响性能。
3. **奖励函数假设**：理论近似依赖 Jensen 间隙假设，对于高度非线性或非平滑的奖励函数，近似误差可能更显著。
4. **模型架构覆盖**：实验主要在 Stable Diffusion 1.5 和 SDXL 的 U-Net 架构上进行，尚未在 DiT、Imagen 等其他扩散模型架构上验证。

## 定位与知识库关联

### 问题定位：推理时多偏好对齐的空白

现有扩散模型对齐方法存在一个关键瓶颈：无论是基于强化学习微调（如 DDPO、DPOK）还是免训练引导（如 **CoDe**, Singh et al., 2025；**RGG**, Chung et al., 2023），它们都假设固定的奖励函数和固定的 KL 正则化强度。一旦用户偏好发生变化（例如，希望图像在“文本对齐”与“美学质量”之间取得不同的平衡），就需要为每个新配置重新训练或重新设计引导策略。**Rewarded Soup (RS)** (Rame et al., 2023) 通过在参数空间线性组合微调模型来缓解此问题，但其性能随奖励数量增加而显著下降，且无法处理 KL 正则化强度的动态调整。**MORL** (Roijers et al., 2013) 作为预言机基线，为每个偏好权重单独微调模型，计算成本随偏好组合数量线性增长，不具备实用性。

Diffusion Blend 的核心洞见在于：利用 Jensen 间隙近似，将目标扩散过程的控制项表达为基础奖励控制项的线性组合。这使得推理时可以通过混合不同基础奖励对应的后向扩散过程，实现多偏好对齐，无需额外微调。

### 方法谱系中的位置

Diffusion Blend 处于**推理时扩散模型对齐**这一新兴范式，与以下方法族形成对比和互补：

| 方法族 | 代表方法 | 核心机制 | 与 Diffusion Blend 的关系 |
|--------|----------|----------|---------------------------|
| RL 微调 | DDPO, DPOK | 在线/离线 RL 微调扩散模型 | DB 使用 RL 微调模型作为基础构建块，但将组合逻辑移至推理时 |
| 免训练引导 | **CoDe** (Singh et al., 2025), **RGG** (Chung et al., 2023) | 推理时基于奖励梯度引导采样过程 | DB 在性能上显著优于这些方法（Table 1: DB-MPA 在 w=0.5 时加权奖励 0.42 vs RGG 0.32 vs CoDe 0.22） |
| 参数融合 | **Rewarded Soup** (Rame et al., 2023) | 在参数空间线性组合微调模型 | DB-MPA 在扩散过程空间进行混合，理论上有更紧的近似保证；实验上 DB-MPA 和 DB-MPA-LS 在多奖励场景下性能保持稳定，而 RS 显著下降（Figure 7） |
| 多目标 RL | **MORL** (Roijers et al., 2013) | 为每个偏好权重单独训练模型 | DB-MPA 以固定数量的微调模型（每个基础奖励一个）逼近 MORL 上限（Figure 2），推理成本仅与基础奖励数量线性相关，而非偏好组合数量 |

### 方法适用边界

**适用场景**：
- 用户需要在推理时动态调整多个奖励之间的权衡（如文本对齐 vs 美学），且不希望重新训练。
- 需要平滑控制 KL 正则化强度，以在“忠实于预训练分布”与“最大化奖励”之间取得连续可调的平衡。
- 基础奖励函数是线性可标量化的（即用户偏好通过加权和表达）。

**不适用或需谨慎使用的场景**：
- **极小 KL 正则化系数 α**：当 α → 0 时，Jensen 间隙近似误差项 $L_{t,2}$ 和 $L_{t,3}$ 可能增大（Remark 2），导致算法性能下降。这是方法的理论脆弱点。
- **高度非线性或非平滑的奖励函数**：近似误差依赖于奖励函数在预训练分布下的 Lipschitz 特性和变异系数（Lemma 1），对于不满足这些条件的奖励函数，近似质量可能恶化。
- **非线性偏好标量化**：当前框架假设用户偏好通过线性加权和表达（$r(w) = \sum_i w_i r_i$），尚未扩展到基于偏好的非线性权重调整（如 Chebyshev 标量化）。

### 计算效率的权衡

DB-MPA 的推理时间约为标准扩散模型的 2 倍（Table 1: 11.11 sec/img vs SD v1.5 的 5.46 sec/img），因为每个去噪步骤需要运行多个微调模型。**DB-MPA-LS** 通过在每个去噪步骤按权重概率采样单个微调模型，将推理成本降至与 SD v1.5 相当（5.64 sec/img），同时保持与 DB-MPA 相近的性能（Proposition 2 保证等价边际分布）。这种“采样近似”策略在极端偏好权重下可能略微影响性能，但在实际应用中提供了可接受的精度-效率折衷。

### 局限与开放问题

**已识别的局限**：
1. 理论近似依赖 Jensen 间隙假设，对于非常小的 α 值，近似误差可能不可忽略（Remark 2）。
2. 实验验证主要基于 Stable Diffusion v1.5 和 SDXL，尚未在其他扩散模型架构（如 DiT、Imagen）上验证。
3. DB-MPA 的推理时间与基础奖励数量线性相关，当奖励数量很大时可能成为瓶颈（尽管 DB-MPA-LS 缓解了此问题）。

**开放问题**：
1. **无密度访问的期望计算**：近似控制项 $\bar{u}^{(r,\alpha)}(x,t) = \nabla_x \mathbb{E}_{x_0 \sim p_{0|t}^{\text{pre}}(\cdot|x)}[r(x_0)/\alpha]$ 需要从预训练模型的条件分布采样，如何在不显式访问预训练模型密度的前提下精确计算该期望？
2. **自适应 α 机制**：对于非常小的 α 值，能否通过自适应机制或改进的近似（如高阶展开）来保持算法有效性？
3. **非线性标量化扩展**：该方法能否扩展到非线性标量化的多目标偏好（例如，基于偏好向量的权重动态调整）？
4. **跨模态和跨架构泛化**：扩散混合框架是否可以直接应用于文本到视频、文本到 3D 或其他生成模型？在 DiT、Imagen 等架构上的表现如何？
5. **交互式偏好确定**：在推理时如何自动或交互式地确定满足用户意图的最优偏好向量 $w$？这涉及将 Diffusion Blend 与人类反馈或自动偏好学习相结合的可能性。

## 原文 PDF

![[paperPDFs/ICLR_2026/Diffusion_Blend_Inference_Time_Multi_Preference_Alignment_for_Diffusion_Models.pdf]]
