---
title: "EasyTune: Efficient Step-Aware Fine-Tuning for Diffusion-Based Motion Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Generation.pdf
project_link: null
code_link: https://github.com/black-forest-labs/flux
aliases:
- EasyTune
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在每个去噪步骤独立进行优化，通过停止梯度操作解耦递归依赖。
primary_logic: 通过停止梯度截断梯度流动，使每一步的优化独立于前序步骤，从而支持稠密更新且内存复杂度降为 O(1)。
claims:
- Corollary 1 和 Eq.(5) 从理论上证明递归依赖导致梯度系数消失，早期步骤欠优化。
- EasyTune 通过 Eq.(7) 中的停止梯度实现 O(1) 内存，且不再有递归项。
- 在 HumanML3D 上，EasyTune 与 DRaFT-50 相比 MM-Dist 提升 8.2%，内存仅 31.16%，训练速度提升 7.3 倍。
- EasyTune 在 MLD 基线上将 FID 从 0.473 降至 0.132，相对改进 72.1%。
---

# EasyTune: Efficient Step-Aware Fine-Tuning for Diffusion-Based Motion Generation

> [!tip] 核心洞察
> 通过停止梯度截断梯度流动，使每一步的优化独立于前序步骤，从而支持稠密更新且内存复杂度降为 O(1)。

| 字段 | 内容 |
|------|------|
| 中文题名 | EasyTune：面向扩散运动生成的高效分步感知微调 |
| 英文题名 | EasyTune: Efficient Step-Aware Fine-Tuning for Diffusion-Based Motion Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [Code](https://github.com/black-forest-labs/flux) · [paper](https://arxiv.org/abs/2511.18927) · [paper](https://arxiv.org/abs/2602.07967) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | EasyTune |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.132 vs 0.473 (MLD) (-72.1%)；MM-Dist 2.637 vs 3.196 (MLD) (-17.5%)；Memory (GB) 22.10 vs ~70.91 (DRaFT-50) (31.16% of DRaFT)。

## 概要

扩散模型在文本到运动生成任务中展现出强大能力，但将预训练模型适配到特定偏好或质量指标仍面临瓶颈。现有基于可微奖励的微调方法（如 **DRaFT** (Clark et al., 2024)、**AlignProp** (Prabhudesai et al., 2023)、**DRTune** (Wu et al., 2025)）在完整去噪轨迹上反向传播奖励梯度，导致三个根本性问题：**递归梯度依赖**使早期步骤梯度系数消失（Corollary 1, Eq.(5)），造成稀疏粗粒度优化；**内存复杂度随去噪步数线性增长**（O(T)）；**训练效率低下**。基于强化学习的替代方案（如 **DDPO** (Black et al., 2023)）则面临高方差和收敛缓慢的挑战。

**核心瓶颈**在于去噪过程的递归依赖——每一步的梯度必须通过完整链式法则从最终输出回传，导致早期步骤欠优化且内存无法释放。

**EasyTune** 通过一个关键因果操作解决此瓶颈：在每个去噪步骤独立进行优化，利用**停止梯度**操作截断跨步梯度流动（Eq.(7)），将递归依赖解耦为步骤级独立更新（Corollary 2, Eq.(8)）。这一设计实现了三项突破：
- **稠密细粒度优化**：每一步均获得有效梯度信号，不再受梯度消失困扰；
- **O(1) 内存复杂度**：仅需存储当前步骤的计算图，峰值内存降至 DRaFT 的 31.16%；
- **显著效率提升**：训练速度达到 DRaFT 的 7.3 倍。

此外，EasyTune 引入**自精炼偏好学习（SPL）**机制，从检索数据集中动态挖掘偏好对，无需人工标注即可训练奖励模型，增强奖励信号的语义对齐能力。

**主要实证结果**（HumanML3D 数据集，以 **MLD** (Chen et al., 2023) 为基线）：
- FID 从 0.473 降至 **0.132**（相对改进 72.1%）；
- MM-Dist 从 3.196 降至 **2.637**（相对改进 17.5%）；
- R-Precision Top-1 从 0.481 提升至 **0.581**（相对提升 20.8%）；
- 内存开销仅 **22.10 GB**，相较 DRaFT-50 降低约 69%。

EasyTune 在六个预训练扩散模型上均展现一致的性能增益，验证了其方法层面的泛化性。当前局限主要在于奖励模型侧重语义对齐而缺乏物理合理性显式评估，存在奖励黑客风险；SPL 依赖预训练检索模型质量；实验验证目前限于文本到运动生成任务。

### 任务背景：文本到运动生成与扩散模型

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，扩散模型（Diffusion Models）已成为该任务的主流范式，其通过逐步去噪将随机噪声转化为符合文本条件的运动序列。典型的预训练运动扩散模型包括 **MLD**（Chen et al., 2023）、**MDM**（Tevet et al., 2023）等，它们在 HumanML3D 和 KIT-ML 等公开基准上取得了显著进展。

然而，预训练扩散模型通常以通用生成能力为目标，其生成结果在语义对齐、运动质量和物理合理性方面仍有较大提升空间。为此，研究者提出了一系列微调方法，通过在预训练模型上引入额外监督信号来定向优化生成质量。

### 现有微调范式及其瓶颈

当前主流的微调方法可归纳为两类：

**基于强化学习的微调**：以 **DDPO**（Black et al., 2023）为代表，将扩散模型的去噪过程建模为马尔可夫决策过程，利用策略梯度优化奖励信号。这类方法无需反向传播通过完整去噪轨迹，但面临高方差和样本效率低的问题。

**基于可微奖励的微调**：以 **DRaFT**（Clark et al., 2024）和 **AlignProp**（Prabhudesai et al., 2023）为代表，通过在整个去噪轨迹上反向传播可微奖励模型的梯度来直接优化扩散模型参数。这类方法的核心损失函数为：

$$
\mathcal { L } ( \theta ) = - \mathbb { E } _ { c \sim \mathcal { D } _ { \mathrm { T } } , \mathbf { x } _ { 0 } ^ { \theta } \sim \pi _ { \theta } ( \cdot | c ) } \left[ \mathcal { R } _ { \phi } ( \mathbf { x } _ { 0 } ^ { \theta } , c ) \right]
$$

其中 $\mathbf{x}_0^\theta$ 是经过完整 $T$ 步逆扩散生成的最终运动，$\mathcal{R}_\phi$ 是预训练的可微奖励模型。该方法虽然实现了端到端优化，但存在三个根本性瓶颈：

1. **内存消耗过高**：梯度计算需要存储从 $\mathbf{x}_T$ 到 $\mathbf{x}_0$ 的完整计算图，内存复杂度为 $O(T)$。对于典型的 50 步或 1000 步去噪过程，这导致极大的 GPU 内存开销。例如，DRaFT-50 在 HumanML3D 上的额外内存开销约为 70.91 GB。

2. **稀疏粗粒度优化**：奖励信号仅在最终生成的 $\mathbf{x}_0$ 上计算，所有中间去噪步骤仅通过链式法则间接接收梯度。EasyTune 论文通过 **Corollary 1** 揭示了这一问题的数学本质——梯度沿去噪链展开后，早期步骤的梯度系数为多个雅可比矩阵的乘积：

$$
\frac { \partial \mathcal { L } ( \theta ) } { \partial \theta } = - \mathbb { E } ... \left[ \frac { \partial \mathcal { R } _ { \phi } ( \mathbf { x } _ { 0 } ^ { \theta } ) } { \partial \mathbf { x } _ { 0 } ^ { \theta } } \cdot \sum _ { t = 1 } ^ { T } \left( \prod _ { s = 1 } ^ { t - 1 } \frac { \partial \pi _ { \theta } ( \mathbf { x } _ { s } ^ { \theta } , s , c ) } { \partial \mathbf { x } _ { s } ^ { \theta } } \right) \left( \frac { \partial \pi _ { \theta } ( \mathbf { x } _ { t } ^ { \theta } , t , c ) } { \partial \theta } \right) \right]
$$

    其中连乘项 $\prod_{s=1}^{t-1} \frac{\partial \pi_\theta}{\partial \mathbf{x}_s^\theta}$ 随 $t$ 减小呈指数衰减（见 **Figure 3** 的实证验证），导致早期去噪步骤几乎接收不到有效梯度，形成“梯度消失”现象。

3. **递归依赖导致优化低效**：每一步的梯度 $\frac{\partial \mathbf{x}_{t-1}^\theta}{\partial \theta}$ 递归依赖于后续步骤的梯度 $\frac{\partial \mathbf{x}_t^\theta}{\partial \theta}$（**Corollary 1, Eq.(4)**），使得训练必须串行展开整个轨迹，无法并行化。

值得注意的是，**DRTune**（Wu et al., 2025）尝试引入停止梯度操作来缓解内存问题，但仍保留了递归依赖结构，未能从根本上解决稀疏优化和梯度消失的困境。

### EasyTune 的核心动机与洞察

EasyTune 的核心动机源于一个关键观察：**去噪轨迹中不同步骤的运动与最终干净运动之间的语义相似性存在显著差异**（见 **Figure 4**）。这意味着，仅对最终 $\mathbf{x}_0$ 施加奖励信号忽略了中间步骤的独特语义信息，是一种信息利用不充分的粗粒度优化。

基于此，EasyTune 提出两个根本性改进：

- **步骤感知优化**：将优化目标从轨迹级奖励 $\mathcal{R}_\phi(\mathbf{x}_0^\theta, c)$ 扩展为步骤级奖励 $\mathcal{R}_\phi(\mathbf{x}_t^\theta, t, c)$，在每个去噪步骤 $t$ 独立计算损失并更新模型，实现细粒度稠密监督。

- **停止梯度解耦**：通过停止梯度操作 $\mathrm{sg}(\mathbf{x}_t^\theta)$ 截断递归依赖，将逆扩散步骤改写为：

$$
\mathbf { x } _ { t - 1 } ^ { \theta } = \pi _ { \theta } ( \mathrm { s g } ( \mathbf { x } _ { t } ^ { \theta } ) , t , c )
$$

    这使得梯度 $\frac{\partial \mathbf{x}_{t-1}^\theta}{\partial \theta}$ 仅依赖于当前步骤（**Corollary 2, Eq.(8)**），内存复杂度从 $O(T)$ 降至 $O(1)$，且每一步可独立优化。

**Figure 5** 直观展示了这一核心洞察：通过将 Eq.(4) 中的递归梯度替换为 Eq.(7) 中的步骤级梯度，EasyTune 同时实现了步骤级计算图存储、高效训练和细粒度优化。

### 奖励模型的局限性

EasyTune 进一步指出，现有可微奖励微调方法所使用的奖励模型（通常为预训练的文本-运动检索模型）存在两个不足：一是无法有效评估中间噪声运动的语义对齐程度；二是缺乏对物理合理性的显式建模，可能导致“奖励黑客”（Reward Hacking）——模型生成语义对齐但物理上不合理的运动。为此，EasyTune 引入了自精炼偏好学习（Self-refinement Preference Learning, SPL）机制来改进奖励模型，这部分将在方法章节详述。

## 核心方法与创新机理

EasyTune 的核心创新在于**将扩散模型的微调从轨迹级优化转变为步骤级优化**，通过解耦去噪过程中的递归梯度依赖，从根本上解决了现有可微奖励微调方法的三个关键瓶颈。

### 创新一：步骤感知微调 —— 截断递归梯度链

**关键洞察**：现有方法（如 DRaFT、AlignProp）在微调时最大化最终生成运动的奖励 $\mathcal{R}(\mathbf{x}_0)$，梯度需通过完整的 $T$ 步逆扩散过程反向传播。Corollary 1（Eq.4）揭示了这一过程的递归结构：

$$\frac{\partial \mathbf{x}_{t-1}^{\theta}}{\partial \theta} = \frac{\partial \pi_{\theta}(\mathbf{x}_t^{\theta}, t, c)}{\partial \theta} + \frac{\partial \pi_{\theta}(\mathbf{x}_t^{\theta}, t, c)}{\partial \mathbf{x}_t^{\theta}} \cdot \frac{\partial \mathbf{x}_t^{\theta}}{\partial \theta}$$

展开后（Eq.5），早期步骤的梯度系数为 $\prod_{s=1}^{t-1} \frac{\partial \pi_{\theta}(\mathbf{x}_s^{\theta}, s, c)}{\partial \mathbf{x}_s^{\theta}}$，该乘积随 $t$ 减小而趋于零，导致**早期去噪步骤欠优化**（Figure 3 提供了梯度范数随步骤衰减的实验证据）。同时，存储完整 $T$ 步计算图造成 **$O(T)$ 的内存开销**。

**EasyTune 的改变**：将优化目标从轨迹级奖励 $\mathcal{R}(\mathbf{x}_0)$ 替换为步骤级奖励 $\mathcal{R}(\mathbf{x}_t, t, c)$（Eq.6），并在每一步逆扩散中对输入 $\mathbf{x}_t$ 施加**停止梯度操作** $\mathrm{sg}(\cdot)$：

$$\mathbf{x}_{t-1}^{\theta} = \pi_{\theta}(\mathrm{sg}(\mathbf{x}_t^{\theta}), t, c)$$

这使得梯度退化为仅依赖当前步骤的形式（Corollary 2, Eq.8）：

$$\frac{\partial \mathbf{x}_{t-1}^{\theta}}{\partial \theta} = \frac{\partial \pi_{\theta}\left(\mathrm{sg}(\mathbf{x}_t^{\theta}), t, c\right)}{\partial \theta}$$

**效果**：递归依赖被完全切断，每一步优化独立进行，实现了三个突破：
- **内存复杂度从 $O(T)$ 降至 $O(1)$**（Figure 6），实际内存占用仅为 DRaFT-50 的 31.16%（22.10 GB vs ~70.91 GB）；
- **支持稠密、细粒度的步骤级更新**，早期步骤也能获得有效梯度信号；
- **训练速度提升 7.3 倍**（达到相同奖励水平时）。

### 创新二：自精炼偏好学习 —— 无需人工标注的奖励模型训练

**现有奖励模型的局限**：预训练的文本-运动检索模型虽可直接作为奖励信号，但未针对偏好评估进行优化，难以捕捉生成质量中的细微差异。

**EasyTune 的 SPL 机制**：从检索数据集中**动态构造偏好对**——将正确检索结果作为正样本，检索失败结果作为负样本——然后通过 KL 散度损失微调检索模型（Eq.17），使其学会区分运动质量的优劣。这一过程无需任何人工标注。

消融实验（Figure 8）表明，使用 SPL 训练的奖励模型在 R-Precision 和 FID 上均优于直接使用预训练检索模型的基线。此外，SPL 使奖励模型具备**噪声感知能力**：可根据采样方式（ODE/SDE）选择对噪声运动 $\mathbf{x}_t$ 直接评估或先预测 $\hat{\mathbf{x}}_0$ 再评估（Eq.12），在 ODE 模型上噪声感知奖励优于单步预测奖励（Table S11）。

### 创新三：步骤级奖励重加权

EasyTune 的步骤感知框架自然支持对不同去噪步骤施加不同权重。消融实验（Table S4）发现：
- **线性递减权重**（强调早期步骤）达到最佳整体性能；
- 仅优化前 20 步效果较好，而仅优化最后 20 步性能下降，验证了早期步骤对生成质量的关键作用。

### 与基线方法的关键差异总结

| 维度 | 现有方法（DRaFT/AlignProp） | EasyTune |
|------|---------------------------|----------|
| 优化目标 | 轨迹级 $\mathcal{R}(\mathbf{x}_0)$ | 步骤级 $\mathcal{R}(\mathbf{x}_t, t, c)$ |
| 梯度依赖 | 递归链 $\partial\mathbf{x}_t/\partial\theta$ 依赖 $\partial\mathbf{x}_{t+1}/\partial\theta$ | 停止梯度解耦，每步独立 |
| 内存复杂度 | $O(T)$ | $O(1)$ |
| 奖励模型 | 预训练检索模型，无偏好微调 | SPL 在挖掘偏好对上微调 |
| 更新粒度 | 稀疏粗粒度（早期步骤梯度消失） | 稠密细粒度（每步独立优化） |

EasyTune 的整体 pipeline 围绕两个核心模块构建：**分步感知微调（Step-Aware Fine-Tuning）** 和 **自精炼偏好学习（Self-Refinement Preference Learning, SPL）**。前者解决现有可微奖励微调方法中梯度递归依赖导致的内存爆炸与粗粒度优化问题，后者为分步优化提供无需人工标注的噪声感知奖励模型。

### 框架总览

图 2 对比了现有方法与 EasyTune 的框架差异。现有方法（左）将奖励模型的梯度通过完整的 *T* 步去噪轨迹反向传播，导致三个固有问题：① 内存随步数线性增长 *O(T)*；② 梯度系数在早期步骤中趋于零（见 Eq.(5) 的乘积项 ∏ ∂π/∂x），造成早期步骤欠优化；③ 仅对最终干净运动 x₀ 计算奖励，优化信号稀疏且粗粒度。

EasyTune（右）在每个去噪步骤独立计算损失并更新参数，核心机制是通过**停止梯度（stop-gradient）** 操作切断步骤间的递归依赖：

$$ \mathbf{x}_{t-1}^{\theta} = \pi_{\theta}\big(\mathrm{sg}(\mathbf{x}_{t}^{\theta}), t, c\big) $$

这使得每一步的梯度计算仅依赖当前步骤的参数 ∂π_θ/∂θ，不再包含前序步骤的梯度链（Corollary 2, Eq.(8)），从而实现 *O(1)* 内存复杂度和稠密的逐步骤优化。

### 模块关系与数据流

Pipeline 由以下模块串联构成：

1. **预训练运动扩散模型**（如 **MLD**（Chen et al., 2023））：提供基础的文本条件运动生成能力。输入为文本描述 *c*，通过 *T* 步逆扩散过程生成运动序列 x₀。

2. **奖励模型（Reward Model）**：基于文本-运动检索架构，计算噪声运动 x_t 与文本 *c* 的语义对齐分数。针对不同采样方式，奖励计算分为两种模式（Eq.(12)）：
   - **ODE 模式**：先将 x_t 单步预测为 \hat{x}_0，再计算 R_φ(\hat{x}_0, 0, c)
   - **SDE/通用模式**：直接计算 R_φ(x_t, t, c)
   
   该模型由 SPL 模块在检索数据上微调得到，具备噪声感知能力（Table 4）。

3. **SPL 偏好学习模块**：从检索数据集中动态挖掘偏好对——将正确检索结果作为正样本，失败检索结果作为负样本——并用 KL 散度损失微调检索模型（Eq.(17)），使其能捕捉隐式偏好。此过程无需人工标注。

4. **分步微调循环**（Algorithm 1）：在每个去噪步骤 *t* 上：
   - 对当前噪声运动 x_t 计算奖励 R_φ(x_t, t, c)
   - 以最大化该奖励为目标计算损失 L_EasyTune（Eq.(6)）
   - 通过停止梯度执行单步去噪得到 x_{t-1}，同时更新模型参数 θ
   - 可选地加入 KL 正则化项以防止奖励黑客（Eq. S2）

### 关键设计决策

- **步骤级奖励重加权**：消融实验（Table S4）表明，采用线性递减权重（强调早期步骤）可达到最佳整体性能，验证了早期步骤对生成质量的关键影响。
- **噪声感知奖励**：相比仅对预测的干净运动计算奖励的单步方法，噪声感知奖励在 ODE 模型上表现更优（Table S11）。
- **内存与效率**：图 6 和 Table S9 证实 EasyTune 内存占用恒定，而 **DRaFT**（Clark et al., 2024）等现有方法随步数线性增长；在相同奖励水平下，EasyTune 训练速度是 DRaFT-50 的 7.3 倍。

![[assets/figures/papers/paper_list_l1905_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Gen/figures/002_Figure_2.jpg]]
*Figure 2: The framework of existing differentiable reward-based methods (left) and our proposed EasyTune (right). Existing methods backpropagate the gradients of the reward model through the overall denoising process, resulting in (1) excessive memory, (2) inefficient, and (3) coarse-grained optimization. In contrast, EasyTune optimizes the diffusion model by directly backpropagating the gradients at each denoising step, overcoming these issues*

### 1. 瓶颈分析：现有可微奖励微调的递归依赖

现有基于可微奖励的微调方法（如 **DRaFT** (Clark et al., 2024)、**AlignProp** (Prabhudesai et al., 2023)）通过最大化完整去噪轨迹末端生成运动 $ \mathbf{x}_0^\theta $ 的奖励值来优化扩散模型参数 $ \theta $，其损失函数为：

$$ \mathcal{L}(\theta) = - \mathbb{E}_{c \sim \mathcal{D}_{\mathrm{T}}, \mathbf{x}_0^\theta \sim \pi_\theta(\cdot | c)} \left[ \mathcal{R}_\phi(\mathbf{x}_0^\theta, c) \right] \tag{Eq.1} $$

其中 $ \pi_\theta $ 表示以 $ \theta $ 为参数的逆扩散过程，每一步定义为：

$$ \mathbf{x}_{t-1}^\theta = \pi_\theta(\mathbf{x}_t^\theta, t, c) := \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t^\theta - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_\theta(\mathbf{x}_t^\theta, t, c) \right) \tag{Eq.2} $$

对损失求梯度时，链式法则沿着整个去噪链展开，产生递归依赖（**Corollary 1**）：

$$ \frac{\partial \mathbf{x}_{t-1}^\theta}{\partial \theta} = \frac{\partial \pi_\theta(\mathbf{x}_t^\theta, t, c)}{\partial \theta} + \frac{\partial \pi_\theta(\mathbf{x}_t^\theta, t, c)}{\partial \mathbf{x}_t^\theta} \cdot \frac{\partial \mathbf{x}_t^\theta}{\partial \theta} \tag{Eq.4} $$

将递归展开至 $ \mathbf{x}_0^\theta $，完整梯度为：

$$ \frac{\partial \mathcal{L}(\theta)}{\partial \theta} = - \mathbb{E} \left[ \frac{\partial \mathcal{R}_\phi(\mathbf{x}_0^\theta)}{\partial \mathbf{x}_0^\theta} \cdot \sum_{t=1}^{T} \left( \prod_{s=1}^{t-1} \frac{\partial \pi_\theta(\mathbf{x}_s^\theta, s, c)}{\partial \mathbf{x}_s^\theta} \right) \left( \frac{\partial \pi_\theta(\mathbf{x}_t^\theta, t, c)}{\partial \theta} \right) \right] \tag{Eq.5} $$

**核心瓶颈**：Eq.5 中乘积项 $ \prod_{s=1}^{t-1} \frac{\partial \pi_\theta}{\partial \mathbf{x}_s^\theta} $ 随 $ t $ 减小而指数衰减（**Figure 3** 实证显示早期步骤梯度范数趋于零），导致两个严重后果：
- **稀疏粗粒度优化**：仅最后若干步骤获得有效梯度，早期步骤欠优化；
- **高内存消耗**：需存储完整 $ T $ 步计算图，内存复杂度为 $ O(T) $（**Figure 6** 验证）。

### 2. 核心模块一：Step-Aware Fine-Tuning（分步感知微调）

EasyTune 的核心洞察是将优化目标从轨迹级奖励改为**步骤级奖励**，并在每个去噪步骤独立更新参数，从而解耦递归依赖。

**步骤级损失函数**：

$$ \mathcal{L}_{\mathrm{EasyTune}}(\theta) = - \mathbb{E}_{c, \mathbf{x}_t^\theta, t} \left[ \mathcal{R}_\phi(\mathbf{x}_t^\theta, t, c) \right] \tag{Eq.6} $$

其中 $ t \sim \mathcal{U}(0, T) $ 从去噪步骤中均匀采样，$ \mathcal{R}_\phi(\mathbf{x}_t^\theta, t, c) $ 是能够评估噪声运动质量的步骤感知奖励模型。

**停止梯度解耦**：关键操作是在每一步的逆扩散中使用停止梯度 $ \mathrm{sg}(\cdot) $ 切断递归：

$$ \mathbf{x}_{t-1}^\theta = \pi_\theta(\mathrm{sg}(\mathbf{x}_t^\theta), t, c) \tag{Eq.7} $$

此时梯度计算不再包含递归项（**Corollary 2**）：

$$ \frac{\partial \mathbf{x}_{t-1}^\theta}{\partial \theta} = \frac{\partial \pi_\theta\left( \mathrm{sg}(\mathbf{x}_t^\theta), t, c \right)}{\partial \theta} \tag{Eq.8} $$

**效果**：每一步的梯度仅依赖当前步骤的参数和输入（被视为常数），无需存储前序计算图，内存复杂度降为 $ O(1) $；同时每一步都获得稠密、直接的梯度信号，实现细粒度优化（**Figure 5** 示意）。

### 3. 核心模块二：Self-Refining Preference Learning（SPL，自精炼偏好学习）

步骤级微调需要一个能评估噪声运动质量的奖励模型。EasyTune 提出 SPL，从预训练的文本-运动检索模型中自适应地构建偏好对并微调，无需人工标注。

**基础奖励模型**：基于检索模型 $ \mathcal{E}_{\mathrm{M}} $（运动编码器）和 $ \mathcal{E}_{\mathrm{T}} $（文本编码器）的余弦相似度，通过可学习温度参数 $ \boldsymbol{\tau} $ 缩放：

$$ \mathcal{R}_\phi(\mathbf{x}, c) = \mathcal{E}_{\mathrm{M}}(\mathbf{x}) \cdot \mathcal{E}_{\mathrm{T}}(c) \cdot \boldsymbol{\tau} \tag{Eq.11} $$

**噪声感知奖励**：根据采样方式选择奖励计算策略：

$$ \mathcal{R}_\phi(\mathbf{x}_t, t, c) = \begin{cases} \mathcal{R}_\phi(\hat{\mathbf{x}}_0, 0, c), & \text{ODE} \\ \mathcal{R}_\phi(\mathbf{x}_t, t, c), & \text{SDE/ODE} \end{cases} \tag{Eq.12} $$

对于 ODE 模型，先通过单步预测得到 $ \hat{\mathbf{x}}_0 $ 再计算奖励；对于 SDE 模型，直接评估噪声运动 $ \mathbf{x}_t $。

**SPL 训练机制**：动态地从检索数据集中挖掘偏好对——正样本来自正确检索结果，负样本来自检索失败案例——并通过 KL 散度损失微调奖励模型：

$$ \mathcal{L}_{\mathrm{SPL}}(\phi) = \mathrm{D}_{\mathrm{KL}}(\mathcal{Q} \parallel \mathcal{P}) \tag{Eq.17} $$

其中 $ \mathcal{Q} $ 为目标偏好分布，$ \mathcal{P} $ 为模型预测分布。消融实验（**Figure 8**）表明 SPL 训练的奖励模型在 R-Precision 和 FID 上均优于未使用 SPL 的基线。

### 4. 可选模块：KL 正则化

为防止模型过度拟合奖励信号（奖励黑客），EasyTune 引入可选的 KL 正则化项，约束微调后模型的生成分布不偏离预训练分布过远。消融实验（**Table S2**）显示 KL 正则化可提高生成多样性，但略微降低对齐质量，需根据实际需求权衡。

### 5. 关键公式速查

| 公式 | 含义 | 锚点 |
|------|------|------|
| Eq.1 | 轨迹级微调损失（现有方法） | Sec.3 |
| Eq.4 | 递归梯度依赖（Corollary 1） | Sec.3 |
| Eq.5 | 展开的完整梯度，揭示系数消失 | Sec.3 |
| Eq.6 | EasyTune 步骤级损失 | Sec.4.1 |
| Eq.7 | 停止梯度逆扩散步骤 | Sec.4.1 |
| Eq.8 | 解耦后梯度（Corollary 2） | Sec.4.1 |
| Eq.11 | 基于检索相似度的奖励模型 | Sec.4.2 |
| Eq.12 | 噪声感知奖励（ODE/SDE 分支） | Sec.4.2 |
| Eq.17 | SPL 偏好学习损失 | Sec.4.2 |

## 实验与关键发现

### 主要定量结果

EasyTune 在 HumanML3D 数据集上以 **MLD**（Chen et al., 2023）为基线的微调实验中，取得了全面的性能突破。核心指标 FID 从基线的 0.473 大幅降至 **0.132**，相对改进高达 **72.1%**，表明生成运动的真实性和分布匹配度显著提升。在语义对齐方面，R-Precision Top-1 从 0.481 提升至 **0.581**（+20.8%），MM-Dist 从 3.196 降至 **2.637**（-17.5%），验证了方法在文本-运动一致性上的增益（Table 1）。

![[assets/figures/papers/paper_list_l1905_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Gen/figures/007_Table_1.jpg]]
*Table 1: Comparison of fine-tuning methods on HumanML3D. Arrows , , and indicate that higher, lower, and closer to real values are better. Bold and underline denote the best and second-best results. MLD baseline follows the implementation of (Dai et al., 2024)*

与现有可微奖励微调方法的对比中，EasyTune 展现出压倒性的效率优势。相较于 **DRaFT-50**（Clark et al., 2024），EasyTune 在 MM-Dist 对齐指标上额外提升 **8.2%**，同时内存占用仅为 DRaFT-50 的 **31.16%**（22.10 GB vs ∼70.91 GB），训练速度达到 **7.3 倍**加速（Abstract, Fig.1, App. A.7）。这一效率优势源于 Corollary 2 所揭示的 O(1) 内存复杂度——通过停止梯度操作 `sg(x_t)` 截断递归依赖，每一步的反向传播仅需存储当前步骤的计算图，而非整个去噪轨迹（Fig.6）。

![[assets/figures/papers/paper_list_l1905_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Gen/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of the training costs and generation performance on HumanML3D (Guo et al., 2022a). (a) Performance comparison of different fine-tuning methods (Clark et al., 2024; Prabhudesai et al., 2023; Wu et al., 2025). (b) Generalization performance across six pre-trained diffusion-based models (Chen et al., 2023; Dai et al.; 2024; Tevet et al., 2023; Zhang et al., 2024a)*

在跨模型泛化性方面，EasyTune 在六种预训练扩散模型上均表现出一致的性能提升（Fig.1(b)），包括 MLD、MDM 等主流架构，证明该方法不依赖于特定模型结构。KIT-ML 数据集上的补充实验进一步验证了这一泛化能力（Table S3）。

### 消融实验与关键设计验证

**步骤级奖励重新加权策略**的消融揭示了早期去噪步骤的关键作用。Table S4 显示，采用**线性递减权重**（强调早期步骤）的策略在 FID 和 R-Precision 上均达到最优，而仅优化最后 20 步会导致性能显著下降，仅优化前 20 步则能保持较好效果。这一发现与 Corollary 1 的理论分析一致：传统方法中早期步骤的梯度系数因递归乘积而趋于消失（Eq.(5), Fig.3），EasyTune 通过解耦使每一步获得等权重的稠密优化信号，从而充分挖掘早期步骤的生成潜力。

**SPL 机制**的有效性在 Fig.8 和 Table S5 中得到验证。使用 SPL 训练的奖励模型在 R-Precision 和 FID 上均优于未使用 SPL 的基线，表明通过检索失败结果动态构建偏好对能够有效提升奖励模型的判别能力。Table S7 进一步分析了候选运动数目 K 和检索池设置的灵敏度，结果显示方法对该超参数具有较好的鲁棒性。

**噪声感知奖励**的设计消融（Table S11）表明，对于 ODE 模型，噪声感知奖励整体优于简单的单步预测奖励，验证了直接评估噪声状态而非仅依赖一步预测的合理性。这一设计的动机源于 Fig.4 所揭示的现象：去噪中间步骤的噪声运动与最终干净运动之间保持较高相似性，使得步骤级奖励信号具有实际意义。

**KL 正则化**的引入（Table S2）在略微降低生成质量指标的同时，有效缓解了奖励黑客问题——即模型过度拟合奖励信号导致生成物理上不合理的运动（Fig.S9）。这一权衡表明，在实际部署中需要根据应用场景对语义对齐和物理合理性进行平衡。

### 用户研究与物理合理性

用户研究（Fig.7, Fig.S2）在 MLD 和 MDM 两个基线上进行，参与者对 EasyTune 微调后的生成运动在语义对齐和自然度上的偏好均显著优于基线。然而，论文明确指出当前奖励模型主要评估语义对齐，**缺乏对物理合理性的显式建模**，这构成了方法的主要局限。Table S10 的物理感知评估显示，奖励模型在检测物理不合理运动（如脚部滑动、关节穿透）方面能力有限，可能在某些情况下生成语义正确但物理上不可行的运动。

### 计算效率的深层分析

Fig.S5 提供了全面的内存分析，将训练过程分解为模型加载、提示编码、去噪、VAE 解码和奖励计算等关键阶段。EasyTune 在去噪阶段实现了 O(1) 的内存增长，而现有方法呈 O(T) 线性增长。Table S9 进一步量化了达到不同奖励水平所需的训练时间和 TFLOPs：EasyTune 在更短的时间内达到更高的奖励分数，而 DRaFT 等方法在合理训练预算内无法达到同等奖励水平。

![[assets/figures/papers/paper_list_l1905_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Gen/figures/025_Table.jpg]]
*Table: S9: Computational overhead comparison. We report the training time and TFLOPs required to reach different reward scores. Total time is measured in seconds on a single NVIDIA RTX A6000 GPU. “-” indicates the method could not reach that reward level within a reasonable training budget*

学习率灵敏度分析（Fig.S4）显示，EasyTune 在 $2\times10^{-4}$ 到 $10^{-5}$ 的广泛学习率范围内性能保持稳定，验证了方法对超参数选择的鲁棒性。

![[assets/figures/papers/paper_list_l1905_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Gen/figures/010_Table_4.jpg]]
*Table 4: Evaluation on text-motion retrieval benchmark, HumanML3D and KIT-ML. The column “Noise” indicates whether the method can handle noisy motion from the denoised process*

![[assets/figures/papers/paper_list_l1905_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Gen/figures/018_Table.jpg]]
*Table: S4: Ablation study on step-level reward reweighting strategies for EasyTune. The baseline is MLD*

## 定位与知识库关联

### 1. 问题定位：扩散模型微调的递归依赖瓶颈

EasyTune 瞄准的是扩散模型可微奖励微调（differentiable reward fine-tuning）中的一个结构性瓶颈：**去噪轨迹上的递归梯度依赖**。在现有方法中，微调目标是最大化最终生成样本 $\mathbf{x}_0^\theta$ 的奖励值 $\mathcal{R}_\phi(\mathbf{x}_0^\theta, c)$，损失函数为：

$$\mathcal{L}(\theta) = -\mathbb{E}_{c \sim \mathcal{D}_{\mathrm{T}}, \mathbf{x}_0^\theta \sim \pi_\theta(\cdot | c)}\left[\mathcal{R}_\phi(\mathbf{x}_0^\theta, c)\right] \quad \text{(Eq.1)}$$

梯度通过完整的 $T$ 步逆扩散过程反向传播。**Corollary 1**（Eq.4）揭示了这一过程的本质缺陷：

$$\frac{\partial \mathbf{x}_{t-1}^\theta}{\partial \theta} = \frac{\partial \pi_\theta(\mathbf{x}_t^\theta, t, c)}{\partial \theta} + \frac{\partial \pi_\theta(\mathbf{x}_t^\theta, t, c)}{\partial \mathbf{x}_t^\theta} \cdot \frac{\partial \mathbf{x}_t^\theta}{\partial \theta}$$

右侧第二项 $\frac{\partial \pi_\theta}{\partial \mathbf{x}_t^\theta} \cdot \frac{\partial \mathbf{x}_t^\theta}{\partial \theta}$ 构成了跨步骤的递归依赖。将其展开至完整 $T$ 步（Eq.5）后，早期步骤的梯度系数包含 $\prod_{s=1}^{t-1} \frac{\partial \pi_\theta(\mathbf{x}_s^\theta, s, c)}{\partial \mathbf{x}_s^\theta}$ 的连乘项，该乘积随 $t$ 减小而趋于零，导致**早期去噪步骤几乎得不到有效优化信号**（Figure 3 提供了梯度范数随步骤衰减的经验证据）。这一递归结构同时带来两个工程代价：需要存储完整去噪轨迹的计算图（$\mathcal{O}(T)$ 内存），且优化粒度被限制在轨迹级别而非步骤级别。

### 2. 核心机制：停止梯度解耦递归依赖

EasyTune 的解决方案在数学上极为简洁：**在每个去噪步骤对输入执行停止梯度（stop-gradient）操作**，将逆扩散步骤重写为：

$$\mathbf{x}_{t-1}^\theta = \pi_\theta(\mathrm{sg}(\mathbf{x}_t^\theta), t, c) \quad \text{(Eq.7)}$$

这一操作直接切断了 $\frac{\partial \mathbf{x}_t^\theta}{\partial \theta}$ 向 $\frac{\partial \mathbf{x}_{t-1}^\theta}{\partial \theta}$ 的流动。**Corollary 2**（Eq.8）表明，此时梯度简化为仅依赖当前步骤的形式：

$$\frac{\partial \mathbf{x}_{t-1}^\theta}{\partial \theta} = \frac{\partial \pi_\theta\left(\mathrm{sg}(\mathbf{x}_t^\theta), t, c\right)}{\partial \theta}$$

递归项被完全消除。配合步骤级损失函数 $\mathcal{L}_{\mathrm{EasyTune}}(\theta) = -\mathbb{E}_{c, \mathbf{x}_t^\theta, t}\left[\mathcal{R}_\phi(\mathbf{x}_t^\theta, t, c)\right]$（Eq.6），EasyTune 实现了三个关键转变：
- **内存从 $\mathcal{O}(T)$ 降至 $\mathcal{O}(1)$**：每步只需存储当前步的计算图（Figure 6 实验验证）；
- **优化从粗粒度轨迹级变为细粒度步骤级**：每个 $t$ 独立接收奖励信号并更新参数；
- **训练速度大幅提升**：达到相同奖励水平时，EasyTune 比 DRaFT-50 快 7.3 倍（见 App. A.7）。

### 3. 与基线方法的关系

EasyTune 处于扩散模型微调方法谱系中的一个特定位置，与以下工作形成直接对比：

| 方法 | 核心机制 | 与 EasyTune 的关键差异 |
|------|----------|----------------------|
| **DRaFT** (Clark et al., 2024) | 通过完整去噪轨迹反向传播奖励梯度 | 保留递归依赖，内存 $\mathcal{O}(T)$，优化稀疏 |
| **AlignProp** (Prabhudesai et al., 2023) | 基于可微奖励的轨迹级微调 | 同属递归梯度范式，面临相同的梯度消失和内存问题 |
| **DRTune** (Wu et al., 2025) | 使用停止梯度但仍保留递归依赖 | 停止梯度应用不彻底，未从根本上解耦步骤间依赖 |
| **DDPO** (Black et al., 2023) | 基于强化学习的微调 | 避免可微奖励的梯度问题，但引入 RL 的样本效率和高方差问题 |

EasyTune 与 **DRTune** 的区分尤为关键：两者都使用了停止梯度技术，但 DRTune 未能在数学上消除递归项，因此仍然面临梯度消失和内存增长的困扰。EasyTune 通过 Eq.7 的严格公式化，将停止梯度精确定位在递归依赖的切断点上，实现了 $\mathcal{O}(1)$ 内存的理论保证。**置信度说明**：DRTune 的具体实现细节需参考原论文验证，此处基于 EasyTune 论文中的对比分析。

在预训练基座模型方面，EasyTune 在 **MLD** (Chen et al., 2023) 上展示了最详尽的实验，同时验证了在 MDM、MotionDiffuse 等其他扩散架构上的泛化性（Figure 1b）。

### 4. 奖励模型设计：SPL 的谱系定位

EasyTune 的第二个贡献是 **Self-refinement Preference Learning (SPL)**，用于训练步骤感知的奖励模型。SPL 的定位介于两类方法之间：

- **预训练检索模型直接作为奖励**（如使用 TMR 的相似度分数）：无需额外训练，但缺乏对噪声中间状态的感知能力和偏好校准。
- **人工标注偏好学习**（如 RLHF 范式）：偏好质量高，但标注成本昂贵且难以扩展到步骤级评估。

SPL 采用自举策略：从检索数据集中动态挖掘偏好对（正例来自正确检索结果，负例来自检索失败样本），通过 KL 散度损失 $\mathcal{L}_{\mathrm{SPL}}(\phi) = \mathrm{D}_{\mathrm{KL}}(\mathcal{Q} \parallel \mathcal{P})$（Eq.17）微调预训练检索模型。消融实验（Figure 8, Sec.5.4）表明 SPL 训练的奖励模型在 R-Precision 和 FID 上均优于无 SPL 的基线。**局限**：SPL 的效果依赖于预训练检索模型的质量，且偏好对挖掘策略（如候选运动数目 $K$ 的选择，见 Table S7）会影响奖励模型的判别能力。

### 5. 适用边界与局限

EasyTune 的有效性建立在以下前提之上：

1. **奖励模型需支持步骤级评估**：对于 ODE 采样，EasyTune 使用单步预测 $\hat{\mathbf{x}}_0$ 计算奖励（Eq.12），这依赖于预测质量。当噪声较大时（早期步骤），预测 $\hat{\mathbf{x}}_0$ 可能与最终生成差异显著，导致奖励信号不准确（Table S11 显示噪声感知奖励总体优于单步预测奖励，但差距并非压倒性）。

2. **奖励模型的评估维度有限**：当前奖励模型主要评估语义对齐（文本-运动相似度），缺乏对物理合理性（如关节角度约束、足部滑动、穿模）的显式建模。这导致**奖励黑客（reward hacking）风险**：模型可能生成语义对齐但物理上不合理的运动（Figure S9 提供了示例）。Table S10 的物理感知评估表明该问题确实存在。

3. **任务验证范围**：实验仅在文本到运动生成任务（HumanML3D 和 KIT-ML 数据集）上进行。EasyTune 的步骤感知微调框架在数学上不依赖于运动模态，但其在图像生成、音频生成等任务上的有效性尚未验证。

4. **KL 正则化的双刃剑效应**：Table S2 显示，加入 KL 正则化可减轻过拟合、提高多样性，但略微降低生成质量（FID 和 MM-Dist 指标）。这需要根据应用场景权衡。

### 6. 开放问题

1. **中间步骤奖励感知的理论基础**：Figure 4 展示了噪声运动与干净运动之间的相似性随 $t$ 变化，但 EasyTune 未深入分析步骤级奖励信号的统计特性（如方差、偏差随 $t$ 的演化）。理解这一点可能指导更优的步骤加权策略（Table S4 显示线性递减权重效果最佳，但其最优性缺乏理论解释）。

2. **SPL 与人工标注的差距**：SPL 自动挖掘的偏好对与人工标注偏好之间的系统性差异尚未量化。在哪些类型的运动上 SPL 偏好不可靠，是一个重要的工程问题。

3. **统一奖励模型的构建**：能否开发一个同时显式评估语义对齐和物理合理性的奖励模型？这可能需要多任务学习或约束优化框架，将物理约束作为硬约束而非软奖励项。

4. **跨模态泛化**：EasyTune 的 $\mathcal{O}(1)$ 内存特性在长序列生成（如视频、长篇音乐）中可能带来更显著的收益，但需要验证步骤感知奖励模型在相应模态上的可训练性。

5. **与 RL 方法的理论联系**：EasyTune 的步骤级优化与 DDPO 等 RL 方法在优化粒度上有相似之处（均为步骤级），但前者通过可微奖励实现低方差梯度估计。两者的优劣在什么条件下发生转换，是一个值得深入的理论问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Generation.pdf]]
