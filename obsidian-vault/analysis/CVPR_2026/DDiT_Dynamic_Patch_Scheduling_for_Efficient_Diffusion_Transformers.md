---
title: "DDiT: Dynamic Patch Scheduling for Efficient Diffusion Transformers"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DDiT_Dynamic_Patch_Scheduling_for_Efficient_Diffusion_Transformers.pdf
project_link: null
code_link: null
aliases:
- DDPSDT
- DDiT
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 每个去噪步的patch大小（token粒度）
primary_logic: 通过测量隐空间流形演化的加速度（三阶有限差分）和空间方差，可以在不额外训练的情况下自适应地判断每个去噪步该用粗粒度还是细粒度patch，从而在保证生成质量的同时大幅降低计算量。
claims:
- 在COCO、DrawBench等基准上，DDiT在2.18倍加速下FID仅差0.35，CLIP和ImageReward与基线持平，证明动态patch调度几乎不损失质量。
- 三阶差分比一阶、二阶更能捕捉隐空间演化趋势，实验表明n=3时FID和CLIP最优。
- 可视化显示，复杂纹理prompt的方差分布更高，而简单场景方差较低，验证了方差与内容复杂度的相关性。
- 用户研究表明，DDiT生成结果在视觉质量上被61%参与者偏好，远高于基线（22%），说明人眼难以察觉加速带来的质量损失。
---

# DDiT: Dynamic Patch Scheduling for Efficient Diffusion Transformers

> [!tip] 核心洞察
> 通过测量隐空间流形演化的加速度（三阶有限差分）和空间方差，可以在不额外训练的情况下自适应地判断每个去噪步该用粗粒度还是细粒度patch，从而在保证生成质量的同时大幅降低计算量。

| 字段 | 内容 |
|------|------|
| 中文题名 | DDiT：面向高效扩散Transformer的动态Patch调度 |
| 英文题名 | DDiT: Dynamic Patch Scheduling for Efficient Diffusion Transformers |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.16968) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DDiT (Dynamic Patch Scheduling for Diffusion Transformers) |
| Dataset | COCO, DrawBench, T2I, T2I + TeaCache |

> [!tip] 效果简介
> - COCO 上，FID↓ 33.42 vs 33.07 (+0.35)。
> - DrawBench 上，CLIP↑ 0.3136 vs 0.3156 (-0.002)。
> - T2I (speed) 上，Speed (sec/image) 5.5 vs 12.0 (2.18× faster)。

## 概要

扩散Transformer（DiT）已成为视觉生成的主流架构，但其推理效率受限于一个被长期忽视的设计：**所有去噪步使用相同的patch尺寸对隐空间进行分块（tokenization）**。这一固定策略忽略了扩散过程的内在特性——早期去噪步主要建模图像的全局结构，仅需粗粒度patch即可；而后期去噪步才需要细粒度patch来精修局部纹理与细节。对所有步一视同仁地使用最细patch，导致了大量冗余计算。

针对上述瓶颈，本文提出 **DDiT（Dynamic Patch Scheduling for Diffusion Transformers）**，一种通用的、面向扩散Transformer的动态patch调度框架。其核心洞察是：**通过测量隐空间流形演化的加速度（三阶有限差分）和空间方差，可以在不引入额外训练的条件下，自适应地判断每个去噪步该使用粗粒度还是细粒度的patch**。具体而言，DDiT在推理时为每个去噪步动态选择patch尺寸（最大可扩大至原始尺寸的4倍），在生成早期大幅减少token数量，从而显著降低计算开销。

实验结果表明，DDiT在保持生成质量的前提下实现了可观的加速效果：在FLUX-1.Dev文本到图像模型上，**推理速度提升2.18倍**（与缓存方法TeaCache组合可达3.52倍），而COCO数据集上的FID仅从33.07轻微上升至33.42（差异仅0.35），CLIP得分几乎持平（0.3136 vs. 0.3156）；在Wan-2.1文本到视频模型上，**速度提升3.2倍**，VBench得分仅下降0.27（80.97 vs. 81.24）。用户研究进一步表明，61%的参与者偏好DDiT的生成结果，远高于基线的22%，说明人眼难以察觉加速带来的质量损失。

在方法谱系中，DDiT定位为一种**训练高效、即插即用的推理加速策略**。与TeaCache（Liu et al., CVPR 2025）等基于缓存的加速方法、TaylorSeer（Liu et al., 2025）等基于预测的加速方法不同，DDiT从tokenization粒度入手，通过动态调整patch尺寸来减少自注意力的计算量，且可与上述方法正交组合，实现叠加加速。其模型改造仅需小规模LoRA微调和蒸馏损失，避免了全模型重训的高昂成本。

扩散Transformer（Diffusion Transformer, DiT）已成为文本到图像和文本到视频生成的主流架构，但其高昂的推理成本严重制约了实际部署。核心瓶颈在于：**现有方法在所有去噪步上使用固定大小的patch**，忽略了扩散生成过程的本质特性——早期步骤主要建模全局结构，仅需粗粒度patch即可；而后期步骤才需要细粒度patch来细化局部细节。这种“一刀切”的策略导致大量冗余计算。

具体而言，标准DiT将VAE编码的隐空间特征图 $\mathbf{z} \in \mathbb{R}^{H \times W \times C}$ 划分为固定尺寸 $p \times p$ 的patch，再通过线性投影嵌入为token序列。增大patch尺寸可以平方级地减少token数量，从而显著提升推理速度（如图4所示，将patch从 $p$ 增大到 $2p$ 和 $4p$ 时，token数从4096降至1024和256，速度分别提升约3倍和4倍）。然而，简单地在所有步上使用大patch会导致生成质量严重下降，因为后期细化步骤丧失了必要的空间分辨率。

近期的一些加速工作，如**TeaCache**（Liu et al., CVPR 2025）和**TaylorSeer**（Liu et al., 2025），分别从缓存和预测的角度减少计算，但它们并未触及patch粒度的自适应调整这一根本性问题。这些方法与动态patch调度的思路是正交的，可以组合使用。

本文的核心洞察是：**隐空间流形在去噪过程中的演化速度并非均匀**。在生成早期，隐向量变化剧烈，主要完成全局布局的建立；随着去噪推进，变化趋于平缓，进入细节精修阶段。通过测量这种演化的“加速度”，可以在不额外训练的情况下，自适应地判断每个去噪步应该使用粗粒度还是细粒度patch。图2直观展示了这一思想：DDiT根据不同时间步的内容复杂度动态分配token数量，在简单场景或早期步骤中使用更少的token，在复杂纹理或后期步骤中使用更多token，从而在保证感知质量的前提下大幅降低计算开销。

## 核心方法与创新机理

### 问题洞察：去噪过程的粒度不对称性

扩散Transformer（DiT）在推理时对所有去噪步使用**固定大小的patch**进行token化。这一设计的隐含假设是每个去噪步对空间粒度的需求相同，但DDiT揭示了一个关键洞察：**早期去噪步仅需粗粒度patch建模全局结构，后期去噪步才需要细粒度patch精炼局部细节**。强行在所有步使用相同的小patch导致早期步产生大量冗余token，造成不必要的计算开销。

### 方法创新：动态Patch调度框架

DDiT围绕三个核心“changed slots”构建了轻量级动态token化框架：

**1. 多尺度Patch Embedding（架构改造）**

标准DiT的patch embedding层仅支持单一固定尺寸 $p$。DDiT将其扩展为支持多尺度（$p$, $2p$, $4p$）的嵌入层，具体改动包括：
- 为每种patch尺寸引入**独立的patch-specific embedding层**
- 在Transformer层中插入**LoRA低秩适配器**，使冻结的预训练模型适应多尺度patch输入
- 引入**残差连接**和可学习的**patch-size标识嵌入**（patch-size identifier embedding），帮助模型区分当前使用的patch大小
- 对位置嵌入进行**双线性插值**，使其适配新的patch尺寸

这一架构改造仅需小规模LoRA微调，配合蒸馏损失 $\mathcal{L} = || \epsilon_{\theta_L}(\mathbf{z}_t^{p_{\mathrm{new}}}, t) - \epsilon_{\theta_T}(\mathbf{z}_t^p, t) ||_2^2$ 将冻结基模型的去噪能力迁移到LoRA增强模型，大幅降低了训练开销。

**2. 训练免费的动态调度器（核心控制旋钮）**

DDiT的调度器通过测量**隐空间流形演化的加速度**来自动判断每个去噪步该用何种粒度patch，无需任何额外训练。其核心机制为：

- **三阶有限差分（加速度度量）**：计算隐向量在时间窗口内的三阶差分 $\Delta^{(3)} \mathbf{z}_{t-1} = \Delta^{(2)} \mathbf{z}_{t-1} - \Delta^{(2)} \mathbf{z}_t$，这比一阶位移或二阶速度更能捕捉隐空间演化的趋势转折点——即生成从“构建全局结构”切换到“精炼局部细节”的时刻。

- **空间方差的门控**：将加速度图按patch尺寸 $p_i \times p_i$ 分块，计算每块的标准差 $\sigma_{t-1}^{p_i}$，并取 $\rho$-th百分位数 $\sigma_{t-1}^{p_i, (\rho)}$ 作为该尺度下的空间复杂度指标。当该值低于阈值 $\tau$ 时，说明当前区域结构简单，可使用更大patch；反之则需保留细粒度。

- **调度规则**：每个去噪步选择满足 $\sigma_{t-1}^{p_i, (\rho)} < \tau$ 的最大patch尺寸；若所有尺度均不满足，则回退到原始最小patch（$p_t = 1$）。这形成了 $p_t = \begin{cases} \max(p_i), & \text{if } \sigma_{t-1}^{p_i,(\rho)} < \tau \\ 1, & \text{otherwise} \end{cases}$ 的自适应门控。

**3. 与基线的正交加速**

DDiT的动态patch调度与基于缓存的加速方法（如**TeaCache**, Liu et al., CVPR 2025）完全正交。实验表明，DDiT与TeaCache组合可在FLUX-1.Dev上实现**3.52×加速**，在Wan-2.1上实现**3.2×加速**，且质量几乎无损（VBench仅下降0.71）。

### 关键设计选择与消融支撑

- **三阶差分优于低阶**：消融实验（Table 3）表明，$n=3$时FID和CLIP均达到最优，验证了加速度度量对捕捉去噪轨迹转折点的有效性。
- **百分位数优于均值**：使用 $\rho$-th百分位数（$\rho=0.4$）而非均值来聚合空间方差，能更好地捕捉局部高细节区域的存在，避免均值平滑掩盖纹理复杂度信号。
- **阈值 $\tau$ 提供速度-质量权衡**：$\tau$ 越大，更多步使用大patch，速度越快但质量轻微下降（Table 4）。用户可根据场景需求灵活调节。

DDiT 的完整推理流程由三个核心环节串联而成：**多尺度 Patch Embedding**、**动态 Patch 调度器**，以及**增强后的 DiT 去噪主干网络**。给定一个文本 prompt，模型首先生成初始噪声隐向量 $\mathbf{z}_T \in \mathbb{R}^{H \times W \times C}$，然后进入 $T$ 步的去噪循环。在每一步 $t$，动态调度器根据隐向量的演化状态输出当前应使用的 patch 尺寸 $p_t$；多尺度 Patch Embedding 层将 $\mathbf{z}_t$ 按 $p_t \times p_t$ 分块并映射为 token 序列；这些 token 经过插值适配的位置嵌入和可学习的 patch 尺寸标识嵌入增强后，送入 DiT 主干预测噪声；最终通过标准扩散采样公式更新 $\mathbf{z}_{t-1}$。整个 pipeline 的输入是文本 prompt 和噪声，输出是去噪后的隐向量，经 VAE 解码器还原为图像或视频。

### 多尺度 Patch Embedding

标准 DiT 的 Patch Embedding 层权重 $\mathbf{w}^{\mathrm{emb}} \in \mathbb{R}^{p \times p \times C \times d}$ 仅支持单一固定 patch 尺寸 $p$。DDiT 将此层扩展为支持 $p$、$2p$、$4p$ 三种尺度：为每个新增尺寸引入独立的 patch-specific embedding 层，同时插入 LoRA 低秩适配器分支，以蒸馏损失对齐冻结基模型的去噪行为。蒸馏损失定义为 LoRA 增强模型预测噪声 $\epsilon_{\theta_L}$ 与冻结基模型预测噪声 $\epsilon_{\theta_T}$ 之间的 L2 距离：

$$\mathcal{L} = \| \epsilon_{\theta_L}(\mathbf{z}_t^{p_{\mathrm{new}}}, t) - \epsilon_{\theta_T}(\mathbf{z}_t^{p}, t) \|_2^2$$

此外，原始固定尺寸的位置嵌入通过双线性插值适配到新 patch 尺寸，并引入可学习的 patch-size identifier embedding，使模型能区分当前使用的 patch 粒度。这一设计使得预训练 DiT 仅需小规模 LoRA 微调即可无缝处理多尺度 patch，大幅降低训练开销。

### 动态 Patch 调度器

调度器是整个框架的决策核心，其任务是**在每个去噪步 $t$ 自适应地选择最优 patch 尺寸**，且无需额外训练。其工作原理基于一个关键观察：扩散去噪轨迹中，隐向量的演化加速度能够揭示生成过程从“粗粒度全局结构建模”到“细粒度局部细节精修”的过渡点。

具体而言，调度器首先计算相邻时间步隐向量的一阶有限差分 $\Delta \mathbf{z}_t = \mathbf{z}_t - \mathbf{z}_{t+1}$，进而构造二阶差分 $\Delta^{(2)} \mathbf{z}_{t-1} = \Delta \mathbf{z}_{t-1} - \Delta \mathbf{z}_t$ 和三阶差分（加速度）$\Delta^{(3)} \mathbf{z}_{t-1} = \Delta^{(2)} \mathbf{z}_{t-1} - \Delta^{(2)} \mathbf{z}_t$。实验表明，三阶差分比一阶或二阶更能捕捉隐空间演化的时序动态，在 FID 和 CLIP 上均取得最优（Table 3）。随后，将加速度场按候选 patch 尺寸 $p_i$ 分块，计算每块内的标准差 $\sigma_{t-1}^{p_i}$，并取 $\rho$-th 百分位数 $\sigma_{t-1}^{p_i, (\rho)}$ 作为该尺度的空间方差度量。使用百分位数而非均值，是为了更好地捕捉空间异质性——复杂纹理区域的高方差不会被简单区域平均掉。

最终的 patch 尺寸选择遵循一个简洁的阈值规则：

$$p_t = \begin{cases} \max(p_i), & \text{if } \sigma_{t-1}^{p_i, (\rho)} < \tau \\ 1, & \text{otherwise} \end{cases}$$

即：若某候选尺度的方差低于阈值 $\tau$，说明当前隐状态在该粒度下已足够平滑，可使用更大的 patch 以节省计算；否则回退到最小 patch 尺寸（$p=1$）。在所有实验中，$\tau = 0.001$，$\rho = 0.4$ 作为默认设置。

### 推理效率的来源

增大 patch 尺寸带来的计算收益是二次方级别的。以 $1024 \times 1024$ 分辨率生成为例，patch 尺寸从 $p$ 增至 $2p$ 时，token 数量从 4096 降至 1024，推理速度约提升 3 倍；增至 $4p$ 时 token 数仅 256，速度提升约 4 倍（Figure 4）。DDiT 通过动态调度，在去噪早期大量使用 $2p$ 甚至 $4p$ 的粗粒度 patch，仅在细节精修的后期步切换回 $p$，从而在全局结构建模阶段大幅削减计算量，而在局部细节阶段保留足够的分辨率。这种“好钢用在刀刃上”的策略，使得 DDiT 在 FLUX-1.Dev 上实现 2.18× 加速时 FID 仅差 0.35，与 TeaCache 组合后更可达 3.52× 加速（Table 1）。

### 与基线的模块级对比

| 模块 | 标准 DiT（如 FLUX-1.Dev） | DDiT |
|------|--------------------------|------|
| Patch Embedding | 单一固定尺寸 $p$，无适应能力 | 多尺度 embedding（$p$, $2p$, $4p$）+ LoRA 适配器 + 残差连接 |
| Patch 尺寸选择 | 所有去噪步使用相同 $p$ | 基于隐空间加速度和空间方差的训练免费动态调度 |
| 训练开销 | 需从头训练或全模型微调以支持多尺度 | 仅需小规模 LoRA 微调 + 蒸馏损失，训练成本极低 |
| 与缓存方法兼容性 | 独立使用 | 可与 TeaCache 等正交组合，实现叠加加速 |

> **注意**：当前调度器在每个去噪步内对所有 patch 使用统一尺寸，尚未实现空间自适应的混合粒度分配，这是论文指出的下一步优化方向。此外，阈值 $\tau$ 和百分位数 $\rho$ 需针对不同模型手工预设，如何让调度器自动学习这些超参数仍是开放问题。

### 3.1 多尺度Patch Embedding与LoRA适配

DDiT的核心架构改造围绕一个关键瓶颈展开：预训练DiT的Patch Embedding层仅支持单一固定尺寸 $p$ 的输入，无法处理动态变化的patch大小。为解决这一问题，DDiT在标准embedding层基础上引入了**多尺度支持**和**低秩适配**两个机制。

**多分辨率Embedding层**。对于每个需要支持的新patch尺寸 $p_{\mathrm{new}}$（如 $2p$、$4p$），DDiT增加独立的patch-specific embedding层。同时，原有的位置嵌入通过双线性插值适配到新的patch尺寸，并引入一个可学习的**patch-size identifier embedding**，帮助模型区分当前使用的patch大小。

**LoRA适配器与残差连接**。为最小化训练开销，DDiT在每个Transformer层中插入低秩适配（LoRA）分支，仅微调这部分参数而非整个模型。训练通过**蒸馏损失**完成：以冻结的原始DiT（教师模型）的去噪输出为目标，引导LoRA增强模型（学生模型）在任意patch尺寸下复现相同的去噪行为：

$$
\mathcal{L} = || \epsilon_{\theta_L}(\mathbf{z}_t^{p_{\mathrm{new}}}, t) - \epsilon_{\theta_T}(\mathbf{z}_t^{p}, t) ||_2^2 \tag{1}
$$

其中 $\epsilon_{\theta_T}$ 为冻结的教师模型在原始patch尺寸 $p$ 下的预测噪声，$\epsilon_{\theta_L}$ 为学生模型在 $p_{\mathrm{new}}$ 下的预测噪声。这一设计使得DDiT仅需小规模LoRA微调即可获得多尺度patch处理能力，无需从头训练。

### 3.2 动态Patch调度器：基于隐空间演化加速度的决策机制

DDiT的方法核心是一个**训练免费的动态调度器**，它通过分析去噪过程中隐空间流形的演化速率，自适应地决定每个时间步的patch大小。其设计逻辑源于一个关键观察：扩散模型的早期去噪步主要构建全局结构（粗粒度patch即可胜任），而后期步则聚焦于局部细节的精细刻画（需要细粒度patch）。调度器通过量化这一“粗到细”的过渡过程来实现动态决策。

**隐空间演化加速度**。调度器首先计算相邻时间步隐向量之间的有限差分，以捕捉去噪轨迹的动态特征。一阶差分表示隐向量的位移：

$$
\Delta \mathbf{z}_t = \mathbf{z}_t - \mathbf{z}_{t+1} \tag{2}
$$

二阶差分刻画位移的变化率（即局部速度）：

$$
\Delta^{(2)} \mathbf{z}_{t-1} = \Delta \mathbf{z}_{t-1} - \Delta \mathbf{z}_t \tag{3}
$$

三阶差分进一步提取速度的变化，即**隐空间流形演化的加速度**：

$$
\Delta^{(3)} \mathbf{z}_{t-1} = \Delta^{(2)} \mathbf{z}_{t-1} - \Delta^{(2)} \mathbf{z}_t = 2 \left( \frac{\Delta \mathbf{z}_{t-1} + \Delta \mathbf{z}_{t+1}}{2} - \Delta \mathbf{z}_t \right) \tag{4}
$$

消融实验（Table 3）证实，三阶差分（$n=3$）相比一阶或二阶能获得最优的FID和CLIP，表明加速度度量更能捕捉隐空间演化的本质趋势。

**空间方差与patch尺寸选择**。获得加速度张量 $\Delta^{(3)} \mathbf{z}_{t-1}$ 后，调度器将其划分为大小为 $p_i \times p_i$ 的块，计算每块内的标准差 $\sigma_{t-1}^{p_i}$。为捕捉空间异质性，取这些标准差的 $\rho$ 分位数（而非均值）作为该patch尺寸下的空间方差度量 $\sigma_{t-1}^{p_i, (\rho)}$。最终，patch尺寸的选择遵循以下规则：

$$
p_t = \begin{cases} \max(p_i), & \text{if } \sigma_{t-1}^{p_i, (\rho)} < \tau \\ 1, & \text{otherwise} \end{cases} \tag{5}
$$

即：若 $\rho$ 分位数方差低于阈值 $\tau$，则选择满足条件的最大patch尺寸；否则回退到原始最小patch（$p_t = 1$，即基准尺寸 $p$）。实验中设置 $\tau = 0.001$、$\rho = 0.4$ 作为默认参数。Figure 6的可视化验证了该度量的有效性：纹理复杂的prompt（如斑马条纹）在生成过程中持续呈现较高的空间方差，而简单场景（如纯色背景上的苹果）的方差则显著较低，表明方差与内容粒度的需求高度相关。

### 3.3 模块组合与推理流程

DDiT的完整推理管线由四个核心模块串联构成：**多尺度Patch Embedding**将隐空间分块并嵌入为token序列；**位置嵌入插值**通过双线性插值适配不同patch尺寸的位置编码；**Patch-Size Identifier Embedding**注入当前patch大小的标识信息；**动态Patch调度器**在每个去噪步计算隐空间加速度和空间方差，依据式(5)选择当前步的patch尺寸。所有模块均以训练免费或极低成本微调的方式实现，无需修改基础DiT的预训练权重。

![[assets/figures/papers/paper_list_l853_https_arxiv_org_abs_2602_16968/figures/006_Figure_6.jpg]]
*Figure 6: Visualization of*

## 实验与关键发现

### 核心定量结果

DDiT在文本到图像（T2I）和文本到视频（T2V）两大任务上均实现了显著加速，同时保持与基线模型高度一致的生成质量。

在T2I任务中，以**FLUX-1.Dev**（Black Forest Labs, 2024）为基线的DDiT在COCO基准上取得FID 33.42，与基线的33.07仅差0.35，CLIP分数为0.3136（基线0.3156），几乎无感知质量损失，但推理速度从12.0秒/图降至5.5秒/图，实现**2.18倍加速**。当DDiT与缓存加速方法**TeaCache**（Liu et al., CVPR 2025）正交组合时，速度进一步提升至3.4秒/图，达到**3.52倍加速**，而FID仅轻微上升。在DrawBench上，DDiT的ImageReward和SSIM/LPIPS指标同样与基线持平，证明了动态patch调度在多种评价维度下的鲁棒性。

在T2V任务中，以**Wan-2.1**（Team Wan et al., 2025）为基线的DDiT在VBench基准上取得80.97分（基线81.24），仅下降0.27分。当与TeaCache组合时，VBench分数为80.53（下降0.71），但可获得**3.2倍加速**。这些结果表明，DDiT在视频生成的时序一致性约束下依然有效。

用户研究进一步验证了加速的主观可接受性：在DDiT与基线的盲测对比中，**61%的参与者偏好DDiT的生成结果**，而仅22%偏好基线，说明人眼难以察觉加速带来的质量差异。

### 关键消融实验

**差分阶数的影响。** 调度器基于隐空间演化的有限差分选择patch尺寸。消融实验（Table 3）系统比较了一阶、二阶和三阶差分的调度效果。结果表明，三阶差分（即加速度）在FID和CLIP两项指标上均取得最优，验证了加速度度量比位移（一阶）或速度（二阶）更能捕捉去噪轨迹从“全局结构建模”向“局部细节细化”过渡的关键节点。

**阈值τ的调控作用。** τ是控制加速率的核心超参数：τ越大，方差条件越宽松，更多去噪步被分配粗粒度patch，推理速度越快。消融实验（Table 4）显示，当τ从0.001增至0.01时，DrawBench上的推理速度从2.18倍提升至3.52倍，ImageReward仅从1.0256降至1.0124，质量下降极为温和。这为用户提供了一个可解释的速度-质量权衡旋钮。

**方差与内容复杂度的关联。** 可视化分析（Figure 6）对比了复杂纹理prompt（如斑马群）与简单场景prompt（如纯黑背景上的苹果）的方差分布。结果显示，复杂prompt的$\sigma_{t-1}^{2p,(\rho)}$在多个去噪步上持续偏高，表明模型对细节敏感，需要更细粒度的patch；而简单prompt的方差较低，允许更大比例的粗粒度patch。这一观察从机理层面解释了调度器为何能根据内容自适应分配计算资源。

### 失败模式与局限性

尽管DDiT在整体上表现优异，论文仍明确指出了若干边界：

1. **空间均匀patch的次优性。** 当前方法在每个去噪步内对所有空间位置使用相同的patch尺寸，无法对图像中纹理复杂区域和简单背景区域进行差异化处理。这意味着在混合复杂度场景中仍存在计算冗余，是下一步优化的明确方向。

2. **极端加速下的细节损失。** 当τ设置过大时，大量去噪步被分配粗粒度patch，可能导致局部细节（如细小纹理、文字渲染）出现可察觉的退化。这与加速率-质量权衡的预期一致。

3. **调度器超参数需手动预设。** τ和百分位数ρ的取值需要针对不同模型进行经验性选择，目前尚未实现完全自动化的学习机制。

4. **仍需少量微调。** 尽管DDiT仅需LoRA微调（训练成本远低于全模型训练），但仍需要为目标模型构建合成数据集以完成蒸馏训练，对完全免训练的应用场景存在一定门槛。

![[assets/figures/papers/paper_list_l853_https_arxiv_org_abs_2602_16968/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison of text-to-image generation performance with state-of-the-art methods on COCO, DrawBench, and PartiPrompts. If not specified, all results are reported using 50 inference steps by default. Each color ( Yellow , Blue ) indicates methods operating at similar inference speeds. As highlighted in Blue , our method achieves the best overall image quality, evidenced by the lowest FID scores, strong prompt alignment (CLIP and ImageReward), and high perceptual similarity (SSIM and LPIPS). Bold: best. Underline: second-best*

![[assets/figures/papers/paper_list_l853_https_arxiv_org_abs_2602_16968/figures/010_Table_2.jpg]]
*Table 2: Quantitative results on V-Bench [43]. Comparison of DDiT under different threshold settings (τ ) and its combination with Tea-Cache [61]*

![[assets/figures/papers/paper_list_l853_https_arxiv_org_abs_2602_16968/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative comparisons with the base model [54], Tea-Cache [61], TaylorSeer [62], and DDiT under similar speedups on Draw-Bench. DDiT effectively preserves fine-grained details, pose, spatial layout, and overall color distribution of the generated images*

![[assets/figures/papers/paper_list_l853_https_arxiv_org_abs_2602_16968/figures/009_Figure_8.jpg]]
*Figure 8: Qualitative comparison on DrawBench with the baseline and TaylorSeer [62]. Our method remains robust even for complex prompts that require a deeper understanding of semantic content*

![[assets/figures/papers/paper_list_l853_https_arxiv_org_abs_2602_16968/figures/011_Figure_9.jpg]]
*Figure 9: Qualitative comparison of text-to-video generation between DDiT and the baseline. DDiT produces videos with comparable visual quality to the baseline while achieving significant speedup*

## 定位与知识库关联

### 核心问题与解决路径

扩散Transformer（DiT）在生成过程中对所有去噪步使用固定大小的patch，忽略了早期步主要建模全局结构、后期步细化局部细节的本质差异，导致不必要的计算开销。DDiT通过引入**动态patch调度**机制，让每个去噪步根据隐空间流形演化的加速度和空间方差自适应选择patch大小，从而在保持生成质量的前提下大幅降低计算量。

### 与基线方法的关系

DDiT建立在两个主流DiT基础模型之上：**FLUX-1.Dev**（Black Forest Labs, 2024）用于文本到图像生成，**Wan-2.1**（Team Wan et al., 2025）用于文本到视频生成。这些模型在推理时对所有50个去噪步使用统一的patch尺寸（如FLUX-1.Dev中$p$对应$4096$个token），DDiT则将其改造为支持$p$、$2p$、$4p$三种粒度的多尺度架构。

在加速方法谱系中，DDiT与两类现有工作形成正交互补关系：

- **基于缓存的加速**：**TeaCache**（Liu et al., CVPR 2025）通过缓存中间特征跳过冗余计算。DDiT与TeaCache组合后，在FLUX-1.Dev上实现3.52倍加速，在Wan-2.1上实现3.2倍加速，证明两种机制互不冲突。
- **基于预测的加速**：**TaylorSeer**（Liu et al., 2025）利用泰勒展开预测去噪轨迹。定性对比（Figure 7、Figure 8）显示，在相似加速比下，DDiT对细粒度细节、姿态、空间布局和色彩分布的保持优于TaylorSeer，尤其在需要深层语义理解的复杂prompt上表现更鲁棒。

### 方法谱系定位

DDiT属于**训练轻量、推理时自适应**的加速范式，其核心创新在于：

1. **架构改造层面**：仅需为每个目标patch尺寸引入独立的patch embedding层、LoRA适配器分支和残差连接，配合位置嵌入的双线性插值和可学习的patch尺寸标识向量，使冻结的预训练DiT能无缝处理多尺度token序列。训练仅涉及蒸馏损失（Eq. 1）下的小规模LoRA微调，远低于全模型重训成本。

2. **调度策略层面**：完全训练免费的动态调度器，通过三阶有限差分（Eq. 4）捕捉隐空间流形演化的加速度，再计算不同patch粒度下的空间方差（ρ分位数），以阈值τ决定每个去噪步的patch大小（Eq. 5）。消融实验（Table 3）证实三阶差分优于一阶和二阶，验证了加速度度量的有效性。

### 适用边界与局限

**适用边界**：
- 当前方法已验证于基于DiT架构的文本到图像（FLUX-1.Dev）和文本到视频（Wan-2.1）生成任务。
- 调度器依赖两个预设超参数：阈值$\tau$和分位数$\rho$。实验默认设置$\tau=0.001$、$\rho=0.4$，用户可通过调节$\tau$在速度与质量间权衡（Table 4：$\tau$越大速度越快，质量轻微下降）。
- 方法在50步推理设置下评估，与TeaCache等缓存方法正交兼容。

**已知局限**：
- 每个去噪步内对所有空间位置使用统一的patch尺寸，未实现空间自适应的混合粒度分配——这是论文明确指出的下一步优化方向。
- 虽然LoRA微调成本远低于全模型训练，但仍需要为目标模型构建合成数据集。
- 调度器的$\tau$和$\rho$可能需要针对不同模型进行微调，尚未实现完全自动化学习。
- 在极端加速场景（$\tau$很大）下，图像细节可能略有损失。

### 开放问题

论文为后续研究留下若干明确方向：

1. **空间混合粒度patch**：能否在每个去噪步内部引入空间变化的patch大小，对简单区域用大patch、复杂区域用小patch，进一步减少冗余计算？
2. **调度器自动化**：能否让$\tau$和$\rho$通过元学习或强化学习完全自动化，无需手工预选？
3. **跨框架推广**：动态patch调度机制能否推广到其他生成框架（如自回归视觉模型、掩码生成模型）？
4. **训练阶段应用**：动态patch调度在扩散模型训练阶段是否有用，能否实现训练加速？这一方向尚未被探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/DDiT_Dynamic_Patch_Scheduling_for_Efficient_Diffusion_Transformers.pdf]]
