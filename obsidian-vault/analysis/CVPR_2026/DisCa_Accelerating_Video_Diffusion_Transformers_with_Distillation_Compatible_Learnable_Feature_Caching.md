---
title: "DisCa: Accelerating Video Diffusion Transformers with Distillation-Compatible Learnable Feature Caching"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DisCa_Accelerating_Video_Diffusion_Transformers_with_Distillation_Compatible_Learnable_Feature_Caching.pdf
project_link: null
code_link: "https://github.com/Tencent-Hunyuan/DisCa"
aliases:
- DCLFCD
- DisCa
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 引入基于少量DiT Block的轻量级可学习神经网络预测器替代手工设计缓存预测公式，并配合限制蒸馏时间间隔的Restricted MeanFlow方案，在高度压缩的蒸馏模型上实现更精准的特征预测与更稳定的生成质量。
primary_logic: 将训练无关的特征缓存升级为可学习范式，同时改进蒸馏策略以抑制长序列视频模型中的数值发散与生成伪影，首次实现了蒸馏与缓存机制的高效协同。
claims:
- 可学习预测器在步蒸馏模型的稀疏轨迹上显著优于传统缓存方法，即便在11.8×加速下仍保持高质量生成。
- Restricted MeanFlow通过剪枝高压缩比训练区间，在10步生成中语义分提升12.0%，有效消除MeanFlow中的畸变与伪影。
- 消融实验表明，去除Restricted MeanFlow导致语义分下降5.9%，去除GAN训练导致语义分下降1.2%。
- "HunyuanVideo 1.0 [T2V] on VBench 上 加速比 (Speed↑) = 11.8× (DisCa R=0.2, N=4)"
---

# DisCa: Accelerating Video Diffusion Transformers with Distillation-Compatible Learnable Feature Caching

> [!tip] 核心洞察
> 将训练无关的特征缓存升级为可学习范式，同时改进蒸馏策略以抑制长序列视频模型中的数值发散与生成伪影，首次实现了蒸馏与缓存机制的高效协同。

| 字段 | 内容 |
|------|------|
| 中文题名 | DisCa: 基于蒸馏兼容可学习特征缓存的视频扩散Transformer加速方法 |
| 英文题名 | DisCa: Accelerating Video Diffusion Transformers with Distillation-Compatible Learnable Feature Caching |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.05449) · [Code](https://github.com/Tencent-Hunyuan/DisCa) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | Distillation-Compatible Learnable Feature Caching (DisCa) |
| Dataset | HunyuanVideo 1.0 [T2V] on VBench |

> [!tip] 效果简介
> - HunyuanVideo 1.0 [T2V] on VBench 上，加速比 (Speed↑) 11.8× (DisCa R=0.2, N=4) vs 1.00× (Original 50 steps) (+10.8×)；VBench Total Score 78.8 (DisCa R=0.2, N=4) vs 79.9 (Original 50 steps) (-1.1%)；VBench Semantic Score 69.3 (DisCa R=0.2, N=4) vs 73.5 (Original 50 steps) (-5.7%)。

## 概要

视频扩散Transformer（DiT）的推理成本极高，现有加速策略主要依赖步蒸馏与训练无关的特征缓存，但二者长期处于割裂状态。步蒸馏（如MeanFlow）通过压缩采样轨迹大幅降低推理步数，却使相邻时间步间的特征演化差异急剧增大，导致传统基于简单复用或手工外推的缓存方法（如**∆-DiT**、**PAB**、**TeaCache**、**FORA**、**TaylorSeer**等）在高压缩蒸馏模型上严重失效，产生语义扭曲与细节丢失。

本文提出**DisCa**（Distillation-Compatible Learnable Feature Caching），首次实现步蒸馏与特征缓存的高效协同。核心思路包含两个因果调控点：

1. **Restricted MeanFlow**：在原始MeanFlow蒸馏中引入时间间隔上限约束 $\mathcal{T} = (t - r) \in [0, \mathcal{R}]$，剪枝高压缩比的激进训练区间，抑制长序列视频模型中的数值发散与生成伪影。在10步生成设定下，该方案使语义分提升12.0%。

2. **轻量级可学习预测器**：替代训练无关的启发式缓存公式，利用仅含2个DiT Block（参数量<4%）的小型神经网络，从单次全量计算获得的缓存特征中预测后续多步输出。配合生成对抗训练，预测器能精确捕获蒸馏模型稀疏轨迹上的高维特征运动趋势。

在HunyuanVideo 1.0文本到视频任务上，DisCa以**11.8×加速比**将VBench总分维持在78.8（原始50步模型为79.9，仅下降1.1%），同时峰值VRAM仅为97.64 GB，额外显存开销仅约0.4 GB。消融实验表明，去除Restricted MeanFlow导致语义分下降5.9%，去除GAN训练导致语义分下降1.2%，验证了各组件的独立贡献。方法在HunyuanVideo 1.5图像到视频任务上同样表现出一致的加速与质量保持能力。

### 视频扩散模型加速的现状与瓶颈

视频扩散Transformer（DiT）在文本/图像到视频生成任务中展现出卓越的质量，但其多步迭代去噪过程导致推理延迟极高。以混元视频模型（HunyuanVideo 1.0）为例，生成一段视频需执行50次完整DiT前向推理，峰值显存占用超过130 GB，严重制约了实际部署。为缓解这一问题，学术界与工业界主要沿两条技术路线推进：**步蒸馏**与**特征缓存**。

步蒸馏（如MeanFlow）通过将多步去噪轨迹压缩为少数大步更新，在训练阶段将50步模型蒸馏至20步甚至10步，从而直接降低NFE（Number of Function Evaluations）。然而，高压缩比的蒸馏在大型视频模型上引入了新的挑战：相邻时间步之间的特征演化差异显著增大，传统上基于“相邻步特征相似”假设的训练无关特征缓存方法面临系统性失效。

### 训练无关特征缓存的根本局限

训练无关特征缓存方法——包括直接复用（∆-DiT）、线性外推（TeaCache）、泰勒展开预测（TaylorSeer）以及基于注意力的广播（PAB、FORA）——均依赖手工设计的预测函数来估计被跳过步的输出特征。这些方法在未蒸馏模型上表现良好，因为原始50步轨迹中相邻步的特征变化平缓，简单的复用或低阶外推足以保持语义一致性。

但在步蒸馏模型上，情况发生了根本性变化。如Figure 1所示，蒸馏后的稀疏轨迹使相邻步之间的特征差异急剧扩大，手工设计的预测函数无法准确捕获高维特征空间的非线性演化趋势，导致预测误差累积，最终表现为严重的语义信息丢失、纹理模糊甚至结构畸变。这一瓶颈的本质在于：**训练无关的启发式预测缺乏对蒸馏模型特征动力学的建模能力**。

### 蒸馏策略的稳定性缺口

另一方面，步蒸馏本身在大规模视频模型上的稳定性也未被充分审视。原始MeanFlow在训练时采样无限制的时间间隔 $T = t - r \in [0, 1]$，其中高压缩比区间（$T \to 1$）对应的训练目标与模型容量之间存在显著不匹配，导致蒸馏后的模型在低NFE下产生明显的畸变与伪影。如Figure 3所示，MeanFlow在20步乃至10步设置下，生成视频中出现不可忽视的结构扭曲和纹理崩塌，这表明**激进的蒸馏策略在长序列视频生成中会引发数值发散与质量退化**。

### DisCa的核心动机与设计思路

上述双重困境——**蒸馏后特征演化加剧使传统缓存失效**，以及**无约束蒸馏本身的不稳定性**——构成了视频扩散模型加速的核心矛盾。DisCa的提出正是为了协同解决这两个相互纠缠的问题：

1. **可学习特征缓存**：摒弃手工设计的预测公式，引入一个轻量级神经网络预测器（参数量不足DiT的4%），通过端到端训练学习蒸馏模型在高维特征空间中的演化规律，从而在稀疏轨迹上实现精准的特征预测。
2. **受限MeanFlow蒸馏**：通过剪枝高压缩比训练区间，将蒸馏时间间隔约束在 $T \in [0, \mathcal{R}]$（$\mathcal{R} \in (0,1)$），使模型专注于学习局部平均速度，抑制长距离外推引发的发散与伪影。

两条技术路线的协同使DisCa首次实现了蒸馏与缓存机制的高效兼容，在11.8×加速比下仍保持与原始50步模型接近的生成质量，为视频扩散模型的实用化部署提供了新的技术范式。

## 核心方法与创新机理

DisCa 的核心创新在于首次实现了步蒸馏（step‑distillation）与特征缓存（feature caching）的高效协同，从根本上解决了蒸馏后模型因相邻时间步特征演化差异增大而导致传统训练无关缓存失效的瓶颈。围绕这一目标，方法在**缓存预测机制**与**蒸馏时间间隔约束**两个关键环节引入了结构性改变。

### 1. 从训练无关启发式到可学习神经网络预测器

传统特征缓存方法——包括直接复用、线性外推、泰勒展开逼近等——均依赖手工设计的预测公式，未利用任何模型内部表示的先验。这些方法在未蒸馏模型上尚可维持，因为相邻时间步的高维特征变化平缓（Figure 1(a)）。然而，步蒸馏大幅压缩了采样轨迹，使相邻步之间的特征位移变得剧烈且非线性，手工启发式无法可靠捕捉这一演化过程，导致语义与细节信息严重丢失（Figure 1(b)）。

DisCa 将缓存预测从**训练无关**范式升级为**可学习**范式：引入一个轻量级神经网络预测器 $$\mathcal{P}_{\theta_p}$$，其结构由少量 DiT Block 堆叠而成，参数量始终低于大模型 $$\mathcal{M}_{\theta_M}$$ 的 4%（Figure 2(c)）。推理时，$$\mathcal{M}$$ 执行一次全量计算，将输出的单层特征张量作为缓存 $$\mathcal{C}$$ 注入预测器；随后 $$\mathcal{P}$$ 利用该缓存连续预测后续多个时间步的输出，无需再次调用大模型（Figure 2(a)）。

预测器的训练目标由 MSE 损失与生成对抗损失联合构成：

$$
\mathcal{L}(\theta_p) = \mathbb{E} \left\| \mathcal{M}_{\theta_M}(x_{t'}, r', t') - \mathcal{P}_{\theta_p}(\mathcal{C}, x_{t'}, r', t') \right\|_2^2
$$

$$
\mathcal{L}_{\mathcal{P}} = \mathbb{E} \left[ \|\mathcal{M}_{\theta_M} - \mathcal{P}_{\theta_p}\|_2^2 + \lambda \cdot \max(0, 1 - \mathcal{D} \circ \mathcal{F} \circ \mathcal{P}_{\theta_p}) \right]
$$

其中鉴别器 $$\mathcal{D}$$ 作用于特征图 $$\mathcal{F}$$ 之上，通过 Hinge 对抗损失促使预测器恢复高频细节（Figure 2(b)）。这一设计的关键在于：**预测器不是凭空生成特征，而是以真实全量计算得到的缓存为条件进行外推**，从而在高度压缩的蒸馏轨迹上仍能保持对高维特征运动的准确建模。

### 2. Restricted MeanFlow：保守的步蒸馏策略

MeanFlow 蒸馏通过对连续时间步之间的平均速度建模来压缩采样步数，其训练时采样的时间间隔 $$T = t - r$$ 覆盖 $$[0, 1]$$ 全区间。然而，当 $$T$$ 取值过大时，蒸馏目标要求模型在单步内跨越过长的去噪距离，这在长序列视频模型中极易引发数值发散与生成伪影（Figure 3 左列）。

DisCa 提出 **Restricted MeanFlow**，将训练采样的时间间隔约束在 $$[0, \mathcal{R}]$$ 内（$$\mathcal{R} \in (0,1)$$），直接剪枝掉原始 MeanFlow 中压缩比过高的激进部分：

$$
\mathcal{T} = (t - r) \in [0, \mathcal{R}]
$$

这一看似简单的约束带来了显著的质量提升：在 HunyuanVideo 10 步生成设置下，Restricted MeanFlow ($$\mathcal{R}=0.2$$) 的语义分较原始 MeanFlow 提升 **12.0%**（Table 1），且视觉上消除了明显的畸变与伪影（Figure 3 右列）。其本质是**将蒸馏目标限制在模型可稳定学习的局部速度场范围内**，为后续可学习缓存提供了更可靠的基座模型。

### 3. 蒸馏与缓存协同设计的必要性

消融实验揭示了两个 changed slots 之间的强耦合关系（Table 3, Table 5）：

- 去除 Restricted MeanFlow（回退至原始 MeanFlow）导致语义分下降 **5.9%**，表明激进的蒸馏会破坏预测器所依赖的特征连续性。
- 去除生成对抗训练导致语义分下降约 **1.2%**，说明对抗损失对细节保真度有不可忽略的贡献。
- 若预测器在未蒸馏的原始模型上训练，再直接应用于蒸馏模型，在低 NFE 下 LPIPS 从 0.1942 恶化至 0.2498（Table 5），证实了**预测器必须与蒸馏模型联合训练**才能适配稀疏采样轨迹的特征分布。

### 4. 内存高效的单层缓存设计

与以往方法缓存多层特征不同，DisCa 仅缓存 DiT 最后一层的单个张量，额外 VRAM 开销仅约 **0.4 GB**（Figure 7），远低于 TaylorSeer 等方法的数十 GB 级开销。这一设计在保持预测精度的同时，避免了多层缓存在多 GPU 序列并行场景下的通信瓶颈，使 11.8× 加速下的峰值显存仅为 97.64 GB（Table 7）。

综上，DisCa 的创新并非单一技术的堆叠，而是通过**可学习预测器**与**保守蒸馏策略**的协同设计，在方法层面首次打通了“先蒸馏、再缓存”的加速路径，为视频扩散 Transformer 的高效推理提供了新的范式。

DisCa（Distillation-Compatible Learnable Feature Caching）的整体设计围绕一个核心矛盾展开：步蒸馏在将视频扩散Transformer的采样步数从50步压缩至10步甚至更少时，相邻时间步之间的特征演化差异急剧增大，导致传统训练无关的启发式缓存策略（如直接复用、线性/泰勒外推）严重失效（Figure 1）。为解决这一问题，DisCa将训练无关的特征缓存升级为可学习范式，同时改进蒸馏策略以抑制长序列视频模型中的数值发散与生成伪影，首次实现了蒸馏与缓存机制的高效协同。

### 框架总览

DisCa由两个紧密耦合的组件构成，其整体流程如Figure 2所示：

**1. Restricted MeanFlow 蒸馏（稳定步压缩）**

在原始MeanFlow蒸馏中，时间间隔 $T = t - r$ 从 $[0, 1]$ 范围内无限制采样，其中较大的 $T$ 值对应过于激进的压缩比。论文发现，这部分激进压缩是导致蒸馏模型在低步数下产生明显畸变与伪影的根本原因（Figure 3）。Restricted MeanFlow通过引入约束 $\mathcal{T} = (t - r) \in [0, \mathcal{R}]$（$\mathcal{R} \in (0, 1)$），直接剪枝高压缩比训练区间，使蒸馏模型专注于学习局部平均速度。实验表明，$\mathcal{R}=0.2$ 时，10步生成的语义分较原始MeanFlow提升12.0%（Table 1）。

**2. 轻量级可学习特征缓存（Learnable Feature Caching）**

在Restricted MeanFlow蒸馏模型的基础上，DisCa引入一个基于少量DiT Block的轻量级神经网络预测器 $\mathcal{P}_{\theta_p}$，替代传统的手工设计缓存预测公式。其工作流程为：

- **缓存初始化**：每隔 $N$ 步，使用全尺寸DiT $\mathcal{M}_{\theta_M}$ 进行一次完整前向计算，将输出的单个张量作为缓存特征 $\mathcal{C}$ 存储：
  $$\mathcal{C}(x_{t_i}) = \mathcal{M}_{\theta_M}(x_{t_i}, r_i, t_i, c_{t_i})$$

- **快速推理**：在后续 $N-1$ 步中，预测器以缓存 $\mathcal{C}$ 和当前噪声输入为条件，直接估计DiT的输出：
  $$u(x_{t'}, t', r') = \mathcal{P}_{\theta_p}(\mathcal{C}, x_{t'}, r', t', c_{t'})$$

- **内存高效设计**：仅缓存最后一层的单个张量，避免多层缓存带来的VRAM与通信开销。相比TaylorSeer等方法的130.7 GB峰值显存，DisCa仅需97.64 GB，额外显存开销约0.4 GB（Table 7, Figure 7）。

**3. 生成对抗训练**

为补偿预测器在稀疏采样轨迹上丢失的高频细节与语义信息，DisCa引入鉴别器 $\mathcal{D}$ 与预测器进行对抗训练。鉴别器以Hinge损失区分真实DiT输出与预测器输出，预测器的总损失结合MSE与对抗损失：
$$\mathcal{L}_{\mathcal{P}} = \mathbb{E}[\|\mathcal{M}_{\theta_M} - \mathcal{P}_{\theta_p}\|_2^2 + \lambda \cdot \max(0, 1 - \mathcal{D} \circ \mathcal{F} \circ \mathcal{P}_{\theta_p})]$$
其中 $\mathcal{F}$ 为特征提取映射。消融实验表明，去除GAN训练导致语义分下降约1.2%（Table 3）。

### 模块间的因果依赖

三个模块之间存在严格的因果依赖关系：

1. **Restricted MeanFlow是前提**：若预测器直接在原始未蒸馏模型上训练（无步蒸馏），在低NFE下质量显著恶化，LPIPS从0.1942升至0.2498（Table 5）。这表明蒸馏产生的稀疏采样轨迹是可学习缓存有效工作的必要条件。
2. **可学习预测器是核心**：即便在Restricted MeanFlow蒸馏模型上，传统训练无关缓存方法（如∆-DiT、PAB、TeaCache、FORA、TaylorSeer）在11.8×加速比下仍出现严重退化，而DisCa的可学习预测器成功保持了高质量生成（Figure 4, Table 2）。
3. **GAN训练是增强**：在Restricted MeanFlow与可学习预测器的基础上，GAN训练进一步补偿了预测器生成的高频细节保真度，训练过程中鉴别器与预测器呈现稳定的对抗动态（Figure 5）。

### 训练与推理流程

**训练阶段**：首先对原始50步HunyuanVideo模型进行CFG蒸馏（学习率 $10^{-5}$），随后依次进行Restricted MeanFlow蒸馏（相同学习率）。在蒸馏模型冻结后，训练轻量级预测器 $\mathcal{P}_{\theta_p}$ 与鉴别器 $\mathcal{D}$，二者交替优化。预测器参数量始终小于全尺寸DiT的4%。

**推理阶段**：采用周期性全量计算策略。每 $N$ 步执行一次完整的DiT前向传播以刷新缓存，中间 $N-1$ 步由预测器快速推理。当 $N=4$、$\mathcal{R}=0.2$ 时，DisCa实现了11.8×的实际加速比，VBench总分仅从原始50步的79.9降至78.8（-1.1%），语义分从73.5降至69.3（-5.7%），在加速比与质量保持之间取得了最优权衡（Table 2）。

![[assets/figures/papers/paper_list_l858_https_arxiv_org_abs_2602_05449/figures/002_Figure_2.jpg]]
*Figure 2: An overview of Distillation-Compatible Learnable Feature Caching (DisCa). (a) The inference procedure under the proposed Learnable Feature Caching framework. The lightweight Predictor P performs multi-step fast inference after a single computation pass through the large-scale DiT M. (b) The training process of Predictor. The cache, initialized by the DiT, is fed into the Predictor as part of the input. The outputs of the Predictor and DiT are passed to the discriminator D, alternating between the objectives of maximizing and minimizing*

DisCa 围绕两个核心模块展开：**Restricted MeanFlow 蒸馏**与**可学习特征缓存预测器**。前者通过约束蒸馏的时间间隔来稳定高度压缩的步蒸馏模型，后者则利用轻量级神经网络替代传统训练无关的启发式缓存策略，在蒸馏后的稀疏采样轨迹上实现精准的特征预测。

### Restricted MeanFlow 蒸馏

视频扩散模型的去噪过程可形式化为条件高斯分布。以 HunyuanVideo 采用的 flow-matching 框架为基础，从 $x_t$ 到 $x_{t-1}$ 的去噪步由模型预测的速度场 $u_\theta$ 驱动。MeanFlow 蒸馏的核心思想是让模型直接学习从当前时间步 $t$ 到目标步 $t-r$ 的“平均速度” $u_{\mathrm{tgt}}$，其优化目标为：

$$
\mathcal{L}(\theta) = \mathbb{E} \left\| u_{\theta}(x_t, r, t) - \mathrm{sg}(u_{\mathrm{tgt}}) \right\|_2^2
$$

其中 $\mathrm{sg}(\cdot)$ 表示停止梯度操作，$r$ 控制蒸馏的跳跃跨度。在原始 MeanFlow 中，时间间隔 $\mathcal{T} = t - r$ 可在 $[0, 1]$ 内任意采样，这意味着模型可能被训练去一步跨越极大的时间跨度——这种激进压缩在长序列视频生成中会导致数值发散与显著的畸变伪影（见 Figure 3）。

DisCa 提出的 **Restricted MeanFlow** 通过引入约束参数 $\mathcal{R} \in (0, 1)$，将采样区间限制为：

$$
\mathcal{T} = (t - r) \in [0, \mathcal{R}]
$$

这一约束直接剪枝了原始 MeanFlow 中高压缩比（即大 $\mathcal{T}$ 值）的训练样本，使蒸馏模型专注于学习局部邻域内的平均速度。实验表明（Table 1），在 10 步生成配置下，$\mathcal{R}=0.2$ 的 Restricted MeanFlow 相比原始 MeanFlow 语义分提升 **12.0%**，在 20 步配置下提升 **5.4%**，有效消除了 MeanFlow 中的畸变与伪影。

### 可学习特征缓存预测器

传统特征缓存方法（如 $\Delta$-DiT、PAB、TeaCache、FORA、TaylorSeer）依赖训练无关的启发式策略——直接复用或线性/泰勒外推——这在未蒸馏模型上效果尚可，因为相邻时间步的特征差异较小。然而，步蒸馏使相邻时间步之间的特征演化差异显著增大（Figure 1），手工设计的预测函数无法准确捕获高维特征的运动趋势。

DisCa 引入一个**轻量级可学习神经网络预测器** $\mathcal{P}_{\theta_p}$ 来替代手工缓存公式。推理流程如下：

1. **缓存初始化**：在某个时间步 $t_i$，通过全尺寸 DiT 模型 $\mathcal{M}_{\theta_M}$ 进行一次完整计算，获得缓存特征 $\mathcal{C}$：

$$
\mathcal{C}(x_{t_i}) = u(x_{t_i}, r_i, t_i) = \mathcal{M}_{\theta_M}(x_{t_i}, r_i, t_i, c_{t_i})
$$

2. **预测器推理**：对于后续的多个时间步 $t'$，轻量级预测器 $\mathcal{P}_{\theta_p}$ 利用缓存 $\mathcal{C}$ 直接估计输出，无需再次调用大模型：

$$
u(x_{t'}, t', r') = \mathcal{P}_{\theta_p}(\mathcal{C}, x_{t'}, r', t', c_{t'})
$$

预测器由少量 DiT Block 堆叠而成，参数量始终控制在主模型 $\mathcal{M}_{\theta_M}$ 的 **4% 以内**，确保推理速度远快于完整前向传播。

### 训练目标与生成对抗优化

预测器的训练采用监督学习与生成对抗相结合的策略。基础损失为预测输出与真实目标之间的均方误差：

$$
\mathcal{L}(\theta_p) = \mathbb{E} \left\| \mathcal{M}_{\theta_M}(x_{t'}, r', t') - \mathcal{P}_{\theta_p}(\mathcal{C}, x_{t'}, r', t') \right\|_2^2
$$

为进一步提升高频细节的保真度，DisCa 引入一个鉴别器 $\mathcal{D}$ 与预测器进行对抗训练。鉴别器采用 Hinge 损失，通过特征提取器 $\mathcal{F}$ 对真实特征与预测特征进行判别：

$$
\mathcal{L}_{\mathcal{D}} = \mathbb{E} \left[ \max(0, 1 - \mathcal{D} \circ \mathcal{F} \circ \mathcal{M}_{\theta_M}(x_{t'}, r', t')) + \max(0, 1 + \mathcal{D} \circ \mathcal{F} \circ \mathcal{P}_{\theta_p}(\mathcal{C}, x_{t'}, r', t')) \right]
$$

预测器的总损失结合 MSE 与对抗目标，由超参数 $\lambda$ 平衡：

$$
\mathcal{L}_{\mathcal{P}} = \mathbb{E} \left[ \| \mathcal{M}_{\theta_M}(x_{t'}, r', t') - \mathcal{P}_{\theta_p}(\mathcal{C}, x_{t'}, r', t') \|_2^2 + \lambda \cdot \max(0, 1 - \mathcal{D} \circ \mathcal{F} \circ \mathcal{P}_{\theta_p}(\mathcal{C}, x_{t'}, r', t')) \right]
$$

消融实验（Table 3）证实，去除 GAN 训练导致语义分下降约 **1.2%**，表明对抗训练对保持生成质量具有正向贡献。训练过程中鉴别器与预测器展现出稳定的对抗动态（Figure 5）。

### 内存高效单层缓存

与部分方法需要缓存多层特征不同，DisCa 在推理过程中仅保留**最后一层的单个张量**作为缓存 $\mathcal{C}$。这一设计大幅降低了 VRAM 开销：实测数据显示 DisCa 的额外显存占用仅约 **0.4 GB**，而对比方法中 TaylorSeer 的峰值 VRAM 高达 130.7 GB（Table 7, Figure 7）。单层缓存策略在保持预测精度的同时，有效规避了多层缓存带来的显存与通信瓶颈。

## 实验与关键发现

### 核心发现与瓶颈突破

DisCa 的核心实验目标是在步蒸馏模型的高压缩轨迹上验证可学习特征缓存的有效性。论文首先通过 Figure 1 揭示了关键瓶颈：未蒸馏模型中，相邻时间步特征高度相似，传统的训练无关缓存（如直接复用或线性外推）可以低成本复用；但经过步蒸馏后，相邻步间的特征演化差异急剧增大，手工设计的缓存预测公式无法准确捕获高维特征的运动趋势，导致语义与细节信息严重丢失。DisCa 通过引入轻量级可学习预测器与 Restricted MeanFlow 蒸馏策略，首次实现了蒸馏与缓存机制的高效协同。

### 主实验：加速与质量权衡

Table 2 汇总了 HunyuanVideo 1.0 文本到视频（T2V）任务上各加速方法的综合对比。DisCa 在 R=0.2、N=4 配置下实现了 **11.8× 加速**（相对于原始 50 步模型），VBench Total Score 仅从 79.9 降至 78.8（-1.1%），Semantic Score 从 73.5 降至 69.3（-5.7%）。相比之下，训练无关缓存方法在相近加速比下质量退化严重：**∆-DiT**、**PAB**、**TeaCache**、**FORA**、**TaylorSeer** 等方法的 Semantic Score 普遍低于 DisCa 5-15 个百分点。Table 7 进一步对比了理论 FLOPs 加速比与实际延迟加速比，DisCa 的实际延迟加速比与理论值高度一致，而部分方法因显存与通信开销导致实际加速远低于理论值。

![[assets/figures/papers/paper_list_l858_https_arxiv_org_abs_2602_05449/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on different accleration methods for HunyuanVideo on VBench*

![[assets/figures/papers/paper_list_l858_https_arxiv_org_abs_2602_05449/figures/013_Table_7.jpg]]
*Table 7: Comparison for the theoretical and actual acceleration of different methods on HunyuanVideo*

Figure 4 提供了高加速比下的可视化对比：先前方法在 10× 以上加速时出现明显畸变、模糊与语义错误，而 DisCa 在 11.8× 加速下仍保持高质量生成，验证了可学习预测器在稀疏轨迹上捕获特征演化的能力。

![[assets/figures/papers/paper_list_l858_https_arxiv_org_abs_2602_05449/figures/007_Figure_4.jpg]]
*Figure 4: Visualization of acceleration methods on HunyuanVideo. In the discussed high acceleration ratio scenarios, previous methods exhibit severe degradation, such as malformation and blurring, while DisCa successfully maintains high quality with a 11.8× acceleration*

### Restricted MeanFlow 消融与定性分析

Table 1 定量评估了 Restricted MeanFlow 在不同 R 取值与步数下的性能。以 R=0.2 为例，在 10 步生成中 Semantic Score 达到 68.2%，较原始 MeanFlow 的 56.2% 提升 **12.0%**；在 20 步生成中提升 5.4%。Table 3 的消融实验表明，去除 Restricted MeanFlow（使用原始 MeanFlow）导致 Semantic Score 在加速配置下下降 **5.9%**，验证了限制蒸馏时间间隔对稳定生成质量的关键作用。

![[assets/figures/papers/paper_list_l858_https_arxiv_org_abs_2602_05449/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on Restricted MeanFlow for HunyuanVideo on VBench*

![[assets/figures/papers/paper_list_l858_https_arxiv_org_abs_2602_05449/figures/006_Table_3.jpg]]
*Table 3: Ablation study for Restrict MeanFlow, Learnbale Predictor and GAN Training in DisCa on HunyuanVideo*

Figure 3 的定性对比直观展示了差异：MeanFlow 在 20 步和 10 步设置下均出现明显的畸变与伪影，而 Restricted MeanFlow 通过剪枝高压缩比训练区间（即限制 $\mathcal{T} = (t - r) \in [0, \mathcal{R}]$ 中的 $\mathcal{R}$），有效抑制了长序列视频模型中的数值发散问题。

### 可学习预测器与 GAN 训练贡献

Table 3 同时量化了各模块的贡献：去除 GAN 训练导致 Semantic Score 下降约 **1.2%**，表明对抗训练对高频细节保真度的提升虽有限但不可忽略。Table 5 的消融实验揭示了 Predictor 与蒸馏的强耦合关系：Predictor 若在原始未蒸馏模型上训练，在低 NFE 下质量显著恶化（LPIPS 从 0.1942 升至 0.2498），说明可学习预测器必须针对蒸馏后的稀疏轨迹进行专门训练，无法即插即用。

Figure 5 展示了 GAN 训练过程中的损失曲线，鉴别器与预测器展现出稳定的对抗动态，验证了训练设计的合理性。

### 显存效率与跨任务泛化

Figure 7 的 VRAM 占用分析表明，DisCa 仅产生约 **0.4 GB** 的额外显存开销（峰值 97.64 GB），远低于 TaylorSeer 的 130.7 GB，这得益于其内存高效的单层缓存设计——仅缓存最后一层的单个张量，避免多层缓存带来的 VRAM 与通信开销。Table 4 将评估扩展到 HunyuanVideo 1.5 图像到视频（I2V）任务，DisCa 在该任务上同样保持领先，Figure 6 的用户研究进一步确认了主观偏好优势。

### 失败模式与局限

Table 6 的语义分子维度分解揭示了 DisCa 的主要短板：Scene 维度得分下降约 28.1%，表明复杂场景的语义保真度仍是瓶颈。此外，单帧感知指标（PSNR/SSIM）相对于原 50 步模型存在微小下降，部分纹理细节可能被弱化。这些失败模式指向两个改进方向：一是针对场景维度的专项优化，二是探索更高效的蒸馏或一致性模型以进一步挖掘加速潜力。

## 定位与知识库关联

### 1. 与训练无关特征缓存方法的对比

DisCa 直接对标的是近年来涌现的一系列**训练无关特征缓存方法**，这些方法通过在扩散模型去噪过程中复用或外推中间特征来减少 DiT Block 的调用次数。核心基线包括：

- **∆-DiT**、**PAB**、**TeaCache**、**FORA**、**TaylorSeer**：这些方法均基于一个共同假设——相邻时间步之间的特征演化是平滑的，因此可以通过简单复用、线性插值或泰勒展开等手工设计的预测函数来近似当前步的输出。在未蒸馏的扩散模型上，这一假设基本成立，上述方法均能在保持可接受质量的前提下实现数倍加速。

然而，DisCa 揭示了一个关键瓶颈：**步蒸馏（step-distillation）会彻底打破这一假设**。如 Figure 1 所示，在未蒸馏模型中，相邻时间步的特征高度相似，传统缓存策略有效；但在步蒸馏后的模型上，相邻步之间的特征差异显著增大，手工设计的预测函数无法捕获高维特征的运动趋势，导致语义信息和细节严重丢失。DisCa 将这一现象归因于蒸馏过程中时间步的大幅跳跃——蒸馏后的采样轨迹变得稀疏，每一步需要跨越更大的特征空间。

DisCa 的核心突破在于**将缓存预测从训练无关范式升级为可学习范式**：引入一个基于少量 DiT Block 的轻量级神经网络预测器（参数量 < 4%），通过端到端训练来学习从缓存特征到后续步输出的映射。这一设计使得预测器能够自适应地捕获蒸馏模型特有的高维特征演化规律，在 11.8× 加速下仍保持高质量生成，而传统方法在同等加速比下出现严重的畸变和模糊（Table 2, Figure 4）。

### 2. 与步蒸馏方法的协同与改进

DisCa 的另一个重要贡献在于**首次实现了蒸馏与缓存机制的高效协同**。此前的特征缓存方法普遍在未蒸馏模型上验证，而 DisCa 直接面向蒸馏模型设计，其技术路线包含两个互补的创新：

**Restricted MeanFlow** 是对 MeanFlow 步蒸馏方法的保守改进。MeanFlow 通过预测平均速度来实现一步蒸馏，其训练时采样时间间隔 $T = t - r \in [0, 1]$ 无任何约束。DisCa 发现，当 $T$ 取值较大时（对应高压缩比），蒸馏模型在长序列视频生成中会出现数值发散和生成伪影。为此，DisCa 提出限制时间间隔 $\mathcal{T} = (t - r) \in [0, \mathcal{R}]$（其中 $\mathcal{R} \in (0,1)$），直接剪枝训练中的激进压缩部分。实验表明，在 10 步生成设置下，Restricted MeanFlow（R=0.2）相比原始 MeanFlow 语义分提升 12.0%，有效消除了畸变与伪影（Table 1, Figure 3）。

**可学习预测器**则在 Restricted MeanFlow 蒸馏模型的基础上进一步加速。预测器利用全量 DiT 单次计算产生的缓存特征 $\mathcal{C}$，通过轻量级网络 $\mathcal{P}_{\theta_p}$ 预测后续多个时间步的输出，避免了对大模型 $\mathcal{M}_{\theta_M}$ 的重复调用。训练时，预测器同时优化 MSE 损失和对抗损失（通过鉴别器 $\mathcal{D}$ 提升高频细节保真度），实现了对蒸馏模型稀疏轨迹的精准拟合。

消融实验（Table 3）定量验证了各组件的贡献：去除 Restricted MeanFlow 导致语义分下降 5.9%；去除 GAN 训练导致语义分下降约 1.2%。此外，若预测器在未蒸馏模型上训练后直接应用于蒸馏模型，在低 NFE 下质量显著恶化（LPIPS 从 0.1942 升至 0.2498，Table 5），进一步印证了蒸馏与缓存协同设计的必要性。

### 3. 内存效率设计的独特优势

在内存效率方面，DisCa 采用**单层缓存策略**——仅缓存 DiT 最后一层的单个张量，而非像某些方法那样缓存多层特征。这一设计带来了显著的 VRAM 优势：DisCa 的额外显存开销仅约 0.4 GB，而对比方法中显存占用最高的 TaylorSeer 达到 130.7 GB（Table 7, Figure 7）。在 H20 GPU、序列并行尺寸为 4 的硬件环境下，DisCa 的峰值 VRAM 为 97.64 GB，显著低于其他缓存方法。这一特性使得 DisCa 在多 GPU 通信受限的场景下具有更强的部署可行性。

### 4. 适用边界与局限

尽管 DisCa 在 HunyuanVideo 1.0 和 1.5 上展示了优异的加速效果，其适用范围和局限性需要明确：

- **模型依赖性**：可学习预测器需要针对特定蒸馏模型进行额外训练，尚不具备即插即用的通用性。当前验证仅限于 HunyuanVideo 系列模型，迁移到其他视频扩散模型架构（如基于 3D VAE 或不同 DiT 变体的模型）可能需要重新训练预测器。

- **场景维度退化**：在 VBench 的 Scene 子维度上，DisCa 的语义保真度下降较为明显（约 28.1%，Table 6），表明复杂场景（如多物体交互、复杂背景）的视频生成质量仍有较大提升空间。

- **单帧纹理细节**：在 PSNR/SSIM 等单帧感知指标上，DisCa 相对于原始 50 步模型仍有微小下降，部分纹理细节可能被弱化。这是缓存方法固有的信息损失与加速比之间的权衡。

- **训练开销**：DisCa 的训练流程包含 CFG 蒸馏、Restricted MeanFlow 蒸馏和预测器对抗训练三个阶段，虽然预测器本身轻量，但整体训练管线需要一定的计算资源和数据支撑。

### 5. 开放问题

基于 DisCa 的当前成果与局限，以下问题值得进一步探索：

1. **跨模型泛化**：能否将学习到的预测器泛化到不同的视频扩散模型架构和任务（如不同分辨率、不同 DiT 设计），而不需要重新训练？这可能需要探索预测器的架构设计空间或引入元学习策略。

2. **场景性能均衡**：如何进一步缓解加速后的场景相关性能下降，实现各语义维度（特别是 Scene、Motion、Temporal Consistency）更均衡的保持？可能需要针对性地设计场景感知的缓存策略或损失函数。

3. **与一致性模型的结合**：能否将可学习特征缓存思想与更高效的蒸馏范式（如一致性模型、对抗扩散蒸馏）相结合，进一步挖掘加速潜力？这需要在蒸馏策略和缓存机制之间建立更紧密的协同设计。

4. **多 GPU 通信优化**：在多 GPU 通信受限的环境下，单层缓存的设计是否仍能维持高效率？是否存在额外的通信瓶颈（如缓存张量的跨设备同步）需要优化？

5. **更广泛的任务验证**：当前验证集中在 T2V 和 I2V 任务上，DisCa 在视频编辑、视频超分、长视频生成等更复杂的视频扩散任务上的有效性尚待验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/DisCa_Accelerating_Video_Diffusion_Transformers_with_Distillation_Compatible_Learnable_Feature_Caching.pdf]]
