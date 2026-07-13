---
title: "Endless World: Real-Time 3D-Aware Long Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Endless_World_Real_Time_3D_Aware_Long_Video_Generation.pdf
project_link: "https://bwgzk-keke.github.io/EndlessWorld/"
code_link: null
aliases:
- EW
- EWRT3ALVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将前序视频帧的计算图与梯度更新分离（detach），使优化目标精确匹配推理时的固定条件，从而阻断累计误差；同时在文本条件中融合三维结构特征，为生成过程注入全局几何引导。
primary_logic: 通过分离早期帧的梯度流，训练过程严丝合缝地对齐自回归推理条件，从根本上抑制误差累积；同时，将3D结构嵌入（由VGGT提取）融入文本标记空间，使模型在生成每一帧时都能参考全局几何先验，从而在无需长序列训练的前提下实现长时、三维一致且实时的高质量视频合成。
claims:
- 训练时分离梯度使得模型学习到一致的运动先验，消除推理时的运动漂移。
- 将3D特征融合到文本嵌入中，显著提升了VBench总分（84.54），尤其在大幅提升多物体（+8.82）与美学质量（+4.61）指标。
- 注意力汇机制增强时空连贯性，使30秒视频总分从81.59提升至82.94。
- VBench-long (30s) 上 Total Score = 84.54
---

# Endless World: Real-Time 3D-Aware Long Video Generation

> [!tip] 核心洞察
> 通过分离早期帧的梯度流，训练过程严丝合缝地对齐自回归推理条件，从根本上抑制误差累积；同时，将3D结构嵌入（由VGGT提取）融入文本标记空间，使模型在生成每一帧时都能参考全局几何先验，从而在无需长序列训练的前提下实现长时、三维一致且实时的高质量视频合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Endless World: 实时三维感知长视频生成 |
| 英文题名 | Endless World: Real-Time 3D-Aware Long Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.12430) · [Project](https://bwgzk-keke.github.io/EndlessWorld/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Endless World |
| Dataset | VBench-long |

> [!tip] 效果简介
> - VBench-long (30s) 上，Total Score 84.54 vs 81.59 (Self-Forcing 30s, 无梯度分离、无3D融合) (+2.95)；Throughput (FPS) on single H100 17.0 vs 8.98 (LTX-Video, 最快扩散模型) (+8.02 FPS)。
> - VBench-long (60s) 上，Quality Score 84.73 vs ~82.07 (LongLive 60s, 同一提示集单提示设置) (+2.66)；Total Score 82.31 vs 81.59 (Self-Forcing 30s 已退化，60s 更低) (> 0.72 (超过 Self-Forcing 30s 水平，而对手随长度大幅下降))。

## 概要

**Endless World** 面向一个明确且尖锐的瓶颈：现有自回归视频生成模型在训练与推理之间存在根本性的条件错配。训练时，模型以过去帧为条件生成未来帧，但梯度却同时流经条件帧与生成帧，使模型从未真正学习在“固定历史”下进行预测；推理时，条件帧被冻结，训练中未经历的这种严格约束迅速引发累积误差，导致长序列中运动漂移、闪烁和几何结构崩塌。此外，纯文本条件缺乏对三维场景几何的显式约束，进一步放大了长时生成中的结构退化。

针对这一瓶颈，Endless World 重新定义了条件自回归生成的训练范式，其核心洞察在于：**将早期帧的计算图从梯度更新中分离（detach），使优化目标精确匹配推理时的固定条件，从根本上阻断累积误差。** 同时，方法将 VGGT 提取的三维结构特征通过可学习 CNN 融合模块注入文本令牌空间，为每一帧的生成提供全局几何先验，从而在无需长序列训练的前提下实现长时、三维一致且实时的视频合成。

在 VBench-long 基准上，Endless World 以单张 H100 GPU 实现 **17.0 FPS** 的吞吐量（约为最快扩散模型 LTX-Video 的 1.9 倍），30 秒视频总分达到 **84.54**，较未使用梯度分离与 3D 融合的 Self-Forcing 基线提升 **+2.95**。60 秒视频质量评分 **84.73**，超越交互式系统 LongLive 约 2.66 分，且随视频长度增加性能保持稳定，而 Self-Forcing 等基线则出现显著退化。消融实验进一步验证了注意力汇、条件生成与 3D 融合三个组件的互补增益，其中 3D 特征融合至文本级（而非潜空间）被证明是实现几何一致性与局部运动自然度平衡的关键设计选择。

在方法谱系上，Endless World 位于条件自回归视频生成与三维感知生成的交叉点，其梯度分离策略直接回应了 **Self-Forcing**（Huang et al., 2025）中的训练-推理不匹配问题，并与 **CausVid**（Yin et al., CVPR 2025）的因果扩散思路形成互补。骨干网络基于 **Wan2.1**（Team Wan et al., 2025）的 1.3B 参数模型，通过分布匹配蒸馏实现训练自由的分布对齐。当前方法的局限性包括：3D 相似性损失在增强几何一致性的同时会轻微降低运动平滑度；依赖 VGGT 的预训练分布，对分布外内容的几何引导可能退化；尚未在多提示或交互式场景下验证。



### 三维感知长视频生成的困境

视频生成领域正经历从几秒片段向分钟级长序列的跨越。这一跨越面临的核心挑战并非算力不足，而是**自回归生成中的训练-推理不匹配**：模型在训练时看到的条件帧是可微的，梯度可以同时流经过去帧与未来帧；但在推理时，已生成的帧是固定的，模型只能基于这些固定条件预测未来。这种根本性的条件分布差异导致长序列生成中出现运动漂移、画面闪烁和几何不一致——牛走着走着就改变了方向，建筑转着转着就扭曲了形态。

Figure 3 直观展示了这一问题：第一行是从噪声生成的视频片段（牛直线行走），第二行是基于第一段视频的条件延续——牛的运动方向发生了明显漂移。这种漂移在短序列中尚可容忍，但当视频延长至30秒、60秒甚至更长时，累积误差将导致视觉质量的灾难性退化。

### 现有方法的缺口

当前主流的自回归视频生成方法，如 **Self-Forcing**（Huang et al., 2025），虽然通过分布匹配蒸馏实现了训练效率的提升，但其训练范式存在根本性缺陷：联合优化整个序列时，梯度同时更新条件帧和生成帧，使得模型从未真正学会在固定条件下进行预测。**CausVid**（Yin et al., CVPR 2025）尝试通过因果掩码限制信息流，但依然未解决条件帧可微带来的训练-推理鸿沟。

另一方面，现有方法普遍缺乏显式的三维几何约束。文本提示能为生成提供语义引导，却无法传递场景的深度、结构和空间关系信息。在长序列中，缺乏几何先验意味着每一帧的生成都是“短视”的——模型只能看到过去几帧的像素，却无法感知全局的三维场景结构，这进一步加剧了长时视频的结构退化。

### 本文的动机与核心思路

Endless World 的出发点是两个紧密关联的洞察：

**第一，训练必须精确对齐推理条件。** 核心操作是将前序视频帧从计算图中分离（detach），使优化目标严格匹配推理时的固定条件设定。这并非简单的工程技巧，而是对自回归生成训练范式的根本修正：模型被强制学习“给定不可修改的过去，预测合理的未来”，从而从根源上阻断累积误差。

**第二，三维结构应作为全局先验注入生成过程。** 通过VGGT提取视频帧的高维三维结构特征，并将其融合到文本标记空间中，使模型在生成每一帧时都能参考全局几何信息。这种设计确保了长序列中场景结构的一致性——物体不会无故变形，空间关系不会随时间漂移。

Figure 1 展示了这两个核心模块的协同关系：3D融合提供全局几何锚点，条件自回归生成确保时间一致性，二者共同支撑起无限长度、三维一致且实时的高质量视频合成。



## 核心方法与创新机理

Endless World 的核心创新在于精准定位并解决了自回归视频生成中一个根本性的**训练-推理不匹配（Training-Inference Discrepancy）**问题。传统自回归方法（如 **Self-Forcing**）在训练时，所有条件帧对当前模型参数 $\phi$ 都是可微的，梯度会流经整个序列，导致模型同时优化“过去”与“未来”帧。然而，在推理时，已生成的前序帧是固定的，无法被修正。这种差异引发累积误差，表现为长视频中的运动漂移、闪烁和几何不一致（Figure 3, Figure 4）。

Endless World 通过三个关键机制，实现了从“生成-修正”到“条件-延续”的范式转变：

**1. 梯度分离的条件自回归生成（Gradient-Detached Conditional Generation）**
这是最核心的机制创新。Endless World 重新定义了生成序列的联合分布，将前序帧的计算图从梯度更新中**分离（detach）**：
$$p_{\phi}(v_{1:n}) = \prod_{k=i}^{n} p_{\phi}(v_k \mid v_{i:k}^{\phi}, v_{<i}^{\mathrm{detach}})$$
在此公式下，只有索引 $i$ 及之后的新生成帧参与参数更新，而索引 $i$ 之前的帧仅作为固定的条件输入。这使得训练时的优化目标与推理时的固定条件帧设定严丝合缝地对齐，从根本上阻断了误差累积的路径（Eq. 3, Sec. 3.2）。

**2. 文本级三维结构融合（Text-Level 3D Structure Fusion）**
为生成过程注入显式的全局几何约束，Endless World 引入 VGGT 模型从视频帧中提取高维 3D 结构特征，并通过一个可学习的 CNN 融合模块将其融入文本标记空间：
$$\tilde{e} = f_{\mathrm{fusion}}(e_{\mathrm{text}}, \hat{f}_{3D})$$
这种设计使得模型在生成每一帧时，都能通过注意力机制参考全局的 3D 几何先验，从而在无需长序列训练的前提下，显著提升长时视频的多物体一致性（+8.82）与美学质量（+4.61）（Table 4, Sec. 3.3）。

**3. 注意力汇长时记忆保持（Attention Sink for Long-Horizon Coherence）**
针对长序列生成中的上下文遗忘问题，Endless World 引入了注意力汇机制：保留初始帧的全部令牌作为持久化上下文，并对 KV 缓存应用旋转位置嵌入。这为长时生成提供了稳定的时空锚点，使 30 秒视频的 VBench 总分从 81.59 提升至 82.94（Table 3, Sec. 3.4）。

这三个机制形成了互补增益：注意力汇提供稳定的时序上下文，梯度分离确保该上下文不被错误修正，而 3D 融合则为该上下文注入结构化的几何信息。消融实验验证了这一递进关系：逐步添加注意力汇、条件生成、文本级 3D 融合，VBench 总分依次从 81.59 → 82.94 → 83.30 → 84.54（Table 3）。



Endless World 的整体设计围绕一个核心矛盾展开：**自回归视频生成中训练与推理的条件不一致**。传统方案在训练时允许梯度流经全部条件帧，导致模型学习到“未来可修改过去”的虚假捷径；而推理时条件帧固定，累积误差迅速放大，表现为运动漂移、闪烁和几何退化。Endless World 通过两条互补的技术路径解决这一问题——**条件自回归生成**与**三维结构融合**——并在训练流程中通过分布匹配蒸馏统一优化。

### 训练管线三阶段

整个训练管线（Figure 2）由三个紧密耦合的阶段构成：

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/002_Figure_2.jpg]]
*Figure 2: This figure illustrates the pipeline of our proposed Endless World framework. The training process consists of three main stages: (1) 3D Fusion: fuse 3D features extracted by the VGGT encoder with text tokens; (2) Conditional Generation: auto-regressively generate video frames conditioned on previously generated frames; (3) Distribution Matching distillation (DMD): align the distribution of the generated video (including both generated and conditional frames) with that of the supervision video in a training-free manner. Finally, we optionally apply a 3D similarity loss to ensure consistency between the 3D features of the generated video and those of the reference video with natural motion*

1.  **3D 融合**：利用预训练的 VGGT 编码器从视频帧中提取高维三维结构特征 $\hat{f}_{3D}$，经可学习的 CNN 融合模块投影后，与文本嵌入 $e_{\text{text}}$ 相加，形成融合条件信号 $\tilde{e}$（Eq. 4）。这一设计将全局几何先验注入文本令牌空间，使模型在生成每一帧时都能跨帧关注一致的三维结构。

2.  **条件生成**：将视频序列按时间块划分，随机掩码未来片段，以前序未掩码帧作为条件上下文。关键操作是**将条件帧从计算图中分离**（detach），仅允许新生成帧参与梯度更新。此时序列似然重定义为：
    
$$
p_{\phi}(v_{1:n}) = \prod_{k=i}^{n} p_{\phi}(v_k \mid v_{i:k}^{\phi}, v_{<i}^{\mathrm{detach}})
$$

    该公式精确匹配推理时的固定条件设定，从根本上阻断误差累积（Eq. 3, Sec. 3.2）。

3.  **分布匹配蒸馏**：以训练自由的方式，最小化生成视频分布与监督视频分布之间的逆 KL 散度，对齐整体视觉质量。此阶段可选地加入 3D 相似性损失 $\mathcal{L}_{3\mathrm{D}}$（Eq. 5），通过惩罚预测帧与无噪声参考帧 3D 特征间的余弦距离，进一步增强几何一致性。

### 推理时的流式生成

推理阶段延续条件自回归范式：给定已生成的视频块，模型以分离梯度的方式预测下一块。为缓解长序列中的上下文遗忘，Endless World 引入了**注意力汇**机制——保留初始帧的全部令牌作为持久化上下文，并对 KV 缓存应用旋转位置嵌入。这使得模型在生成数分钟视频时仍能维持时空连贯性，而不会因距离过远丢失早期场景信息。

### 模块关系与数据流

整体数据流可概括为：`视频帧 → VGGT 提取 3D 特征 → 3D-文本融合模块 → 条件自回归生成器 → 分布匹配蒸馏优化`。其中，3D 融合模块为生成器提供全局几何约束，梯度分离策略确保训练-推理条件对齐，注意力汇则保障长时记忆。三者协同，使得 Endless World 无需长序列训练即可实现实时（单 H100 达 17.0 FPS）、三维一致且视觉质量稳定的长视频合成。



### 1. 问题定义：训练-推理不匹配

自回归视频生成面临的核心瓶颈是训练与推理时的条件不一致。在传统设定下，自回归联合分布可表示为：

$$p_{\phi}(v_{1:n}) = \prod_{k=1}^{n} p_{\phi}(v_k \mid v_{<k}^{\phi})$$

其中条件帧 $v_{<k}$ 在模型参数 $\phi$ 下可微。训练时，分布匹配蒸馏（DMD）的梯度同时流经过去帧与未来帧，使模型依赖“可修改的过去”来优化当前帧；而推理时，过去帧是已固定且不可修改的。这种不对称性导致长序列生成中出现运动漂移、闪烁和几何不一致（见 Figure 3 的定性展示）。

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/003_Figure_3.jpg]]
*Figure 3: Motion inconsistency in self-forcing autoregressive generation. First row: video generated from noise (cow walks straight). Second row: continuation conditioned on the first video chunk (cow changes direction due to drift)*

### 2. 条件自回归生成（梯度分离）

Endless World 的核心创新在于将训练过程严丝合缝地对齐推理条件。具体而言，对于索引 $i$ 之前的帧，将其计算图与梯度更新分离（detach），仅让 $i$ 及之后的新生成帧参与参数更新：

$$p_{\phi}(v_j \mid v_{i:j-1}^{\phi}, v_{<i}^{\mathrm{detach}}), \quad \text{for } j>i$$

重新定义的序列似然为：

$$p_{\phi}(v_{1:n}) = \prod_{k=i}^{n} p_{\phi}(v_k \mid v_{i:k}^{\phi}, v_{<i}^{\mathrm{detach}})$$

该公式与有监督数据分布进行匹配，使优化目标精确对应推理时的固定条件，从根本上阻断累计误差。Figure 4 对比了 Self-Forcing 与 Endless World 的梯度流差异。

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/004_Figure_4.jpg]]
*Figure 4: Comparison between Self-Forcing and Endless World. (1) Self-Forcing autoregressively generates new frames conditioned on previous ones, but jointly optimizes the entire sequence via distribution matching, causing gradients to flow through both past and future frames. (2) Endless World conditions on existing video frames while restricting gradient updates to newly generated frames, ensuring consistency without altering previous content*

### 3. 3D-文本融合模块

为注入全局几何先验，框架引入 VGGT 3D 特征提取器，从视频帧中提取高维结构特征 $\hat{f}_{3D}$，并通过可学习 CNN 融合模块将其投影并与文本嵌入相加：

$$\tilde{e} = f_{\mathrm{fusion}}(e_{\mathrm{text}}, \hat{f}_{3D})$$

融合后的嵌入 $\tilde{e}$ 作为全局条件信号，使模型在生成每一帧时都能参考场景的底层几何与空间对应关系。消融实验（Table 3, Table 4）表明，该设计在文本令牌层面融合 3D 特征，相比潜空间融合更稳定且不破坏局部运动。

### 4. 3D 一致性损失（可选）

为进一步鼓励几何一致性，框架引入可选的正则项，计算预测帧与无噪声参考帧 3D 特征之间的余弦距离：

$$\mathcal{L}_{3\mathrm{D}} = 1 - \frac{\langle \hat{f}_{3D}^t, f_{3D}^t \rangle}{|\hat{f}_{3D}^t|_2 |f_{3D}^t|_2}$$

总训练损失为生成损失（DMD）与该正则项的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{gen}} + \lambda_{3\mathrm{D}} \mathcal{L}_{3\mathrm{D}}$$

其中 $\lambda_{3\mathrm{D}}=0.1$。Table 5 显示，该损失在提升多物体、空间关联等一致性指标的同时，轻微降低运动平滑度，因此作为可选项以平衡几何保真度与视觉自然度。

### 5. 注意力汇与流式生成长序列记忆保持

在流式长视频生成中，模型引入注意力汇（Attention Sink）机制：保留初始帧的全部令牌作为持久上下文，并对 KV 缓存应用旋转位置嵌入。这一设计在长序列中提供稳定的上下文锚点，防止上下文遗忘。消融实验（Table 3）表明，注意力汇将 30 秒视频的 VBench 总分从 81.59 提升至 82.94。



## 实验与关键发现

### 核心瓶颈的逐组件验证

Endless World 的设计围绕一个明确的核心瓶颈展开：**自回归视频生成中训练与推理的条件不匹配**。在标准自回归训练中，条件帧在当前模型参数下可微，导致梯度同时流经过去帧与未来帧；而在推理时，条件帧是固定的，这种差异引发了累积误差，表现为长序列中的运动漂移、闪烁和几何不一致。论文通过三个关键技术组件——梯度分离的条件生成、注意力汇机制和 3D 结构融合——逐层消解这一瓶颈，并通过系统的消融实验量化了每个组件的贡献。

Table 3 清晰地呈现了这一阶梯式改进路径。基线配置（Self-Forcing + 注意力汇，但无梯度分离和 3D 融合）在 VBench 30 秒视频上的总分为 81.59。依次引入三个核心组件后，总分呈现稳定的递增：注意力汇将总分提升至 82.94，条件生成（梯度分离）进一步推至 83.30，最终 3D 文本级融合将总分推至最高的 84.54。这一消融序列直接验证了论文的核心主张：**梯度分离是消除训练-推理偏差的关键杠杆，而 3D 融合和注意力汇则分别从几何先验和长时记忆两个维度提供互补增益**。

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/009_Table_3.jpg]]
*Table 3: Ablation study of key components on 30-second video generation. We evaluate the impact of attention sink, conditional generation, and 3D fusion using the VBench benchmark*

### 30 秒视频：全面超越同类模型

Table 1 展示了 Endless World 在 VBench 标准提示集上与多个公开可用模型的全面对比。在 30 秒视频生成任务上，Endless World 取得了 **84.54 的总分**，显著优于所有对比基线。具体而言，其质量分（Quality Score）达到 85.52，语义分（Semantic Score）为 80.60，均处于领先水平。

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/005_Table_1.jpg]]
*Table 1: Baseline comparison on VBench. Endless World is compared with publicly available video generation models of similar scale and resolution. Scores are reported on the standard VBench [13] prompt set, with baseline results taken from [41]. The FPS is evaluated with a single H100 GPU*

值得注意的是，与最直接的自回归基线 **Self-Forcing**（Huang et al., 2025）相比，Endless World 在总分上实现了 **+2.95 的提升**（84.54 vs. 81.59）。这一差距直接归因于梯度分离和 3D 融合两个核心设计——Self-Forcing 虽然也采用了注意力汇，但缺乏对训练-推理不匹配问题的根本解决。

在推理效率方面，Endless World 同样展现出显著优势。在单张 H100 GPU 上，其吞吐量达到 **17.0 FPS**，相较于最快的扩散模型 **LTX-Video**（HaCohen et al., 2025）的 8.98 FPS，实现了近一倍的加速。这一效率优势源于其自回归生成范式天然避免了扩散模型的多步去噪过程，使得实时视频生成成为可能。

### 60 秒视频：长时稳定性验证

长序列生成是检验训练-推理对齐效果的最直接场景。Table 6 揭示了视频长度对生成质量的影响趋势：Self-Forcing 模型随视频长度增加出现显著退化，而 Endless World 在 60 秒生成中仍能保持 **82.31 的总分**，甚至超过了 Self-Forcing 在 30 秒时的表现（81.59）。这一结果表明，梯度分离策略从根本上抑制了误差累积，使模型能够在远超训练片段长度的序列上保持稳定输出。

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/011_Table_6.jpg]]
*Table 6: Impact of video length on Vbench Scores*

Table 2 进一步提供了与交互式长视频生成系统 **LongLive**（Yang et al., 2025）的对比。在单提示 60 秒生成设定下，Endless World 的质量分达到 **84.73**，优于 LongLive 的约 82.07（+2.66）。需要注意的是，LongLive 的原生设定支持交互式多提示生成，此处对比基于单提示条件，因此该优势主要反映了 Endless World 在无人工干预情况下的自主长时生成能力。

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/007_Table_2.jpg]]
*Table 2: Comparison of 60-second video generation on VBench. Using interactive results from [41] as reference, we compare Self-Forcing and our Endless World on single-prompt generation*

定性对比（Figure 5）直观地展示了这一差异：Self-Forcing 在一分钟和两分钟序列中出现了渐进式的质量退化，而 Endless World 在整个序列中保持了视觉质量和时序连贯性。这进一步印证了梯度分离在阻断误差传播方面的决定性作用。

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/010_Figure_5.jpg]]
*Figure 5: Comparison of long-duration video generation. We compare Endless World with Self-Forcing (with attention sink) for oneand two-minute sequences. Endless World preserves visual quality and temporal coherence throughout, whereas Self-Forcing suffers from progressive quality degradation*

### 3D 融合的精细化分析

Table 4 聚焦于 3D 融合模块对各具体评估维度的影响。引入 3D 文本级融合后，**多物体（Multi-Objects）指标大幅提升 +8.82**，美学质量（Aesthetic Quality）提升 +4.61，空间关系（Spatial Relationship）和整体一致性（Overall Consistency）也获得明显增益。这些提升直接源于 VGGT 提取的 3D 结构特征为生成过程注入了全局几何先验，使模型在生成每一帧时都能参考一致的场景结构。

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/006_Table_4.jpg]]
*Table 4: Effect of incorporating 3D fusion on VBench. “Objects” denotes multi-objects, and “Spatial” measures spatial relationship*

论文还探索了 3D 特征的不同融合位置。消融分析（Sec. 4.3）表明，**在文本令牌空间进行融合是稳定且高质量的设计选择**。相比之下，在潜空间（latent space）进行融合虽然能够保留几何信息，但会破坏局部运动模式，引入光流不一致和闪烁伪影。文本级融合的优势在于：3D 信息通过交叉注意力机制被全局均匀地注入所有帧，从而在保持几何一致性的同时不干扰局部的时序动态。

### 3D 相似性损失的权衡

Table 5 揭示了一个重要的设计权衡。可选的 3D 相似性损失（$\mathcal{L}_{3\mathrm{D}}$）通过最小化生成帧与参考帧 3D 特征的余弦距离来增强几何一致性。实验表明，该损失确实提升了一致性相关指标，但代价是**运动平滑度（Motion Smoothness）的轻微下降**。这一现象的原因在于：过强的几何约束可能限制模型生成自然运动变化的能力，使运动趋向于保守。

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/008_Table_5.jpg]]
*Table 5: Effect of the 3D similarity loss on 30-second VBench*

论文将 3D 相似性损失定位为可选项（$\lambda_{3\mathrm{D}}=0.1$），允许根据应用场景灵活调整。对于需要严格几何保真度的场景（如数字孪生、场景重建），可以启用该损失；而对于追求视觉自然度的创意生成，则可以关闭它以获得更流畅的运动表现。

### 失败模式与局限性

尽管 Endless World 在长时视频生成上取得了显著进展，但仍存在若干值得关注的局限：

1. **3D 特征提取的依赖性**：系统依赖预训练的 VGGT 模型提取 3D 结构特征。当视频内容超出 VGGT 的训练分布时（如极端视角、非自然场景），结构引导的质量可能退化，进而影响几何一致性。这一局限在论文中未被量化评估，需要实际部署时进行验证。

2. **运动平滑度与几何一致性的张力**：如 3D 相似性损失的消融所示，增强几何约束会以牺牲运动自然度为代价。这一张力在当前框架中通过手动调节权重来平衡，缺乏自适应的调控机制。

3. **场景突变与注意力汇的适应性**：注意力汇机制通过保留初始帧的全部令牌来提供持久上下文，但当视频涉及显著的场景切换或镜头变化时，固定的初始帧上下文可能成为干扰而非帮助。论文未探索注意力汇在非连续场景下的表现。

4. **骨干网络的规模限制**：所有实验均基于 Wan2.1-1.3B 骨干网络。该方法在更大规模模型或不同架构（如 DiT 变体）上的可迁移性尚未验证，这限制了对其泛化能力的判断。

5. **单提示设定的局限**：当前实验仅覆盖单提示长视频生成场景，未探索多提示或交互式生成。在实际应用中，用户往往需要逐步引导视频内容，这一能力的缺失限制了系统的实用性。

### 开放问题

基于上述分析，以下问题值得进一步探索：

- 梯度分离策略是否可以推广到其他自回归生成任务（如音频合成、文本生成）以减少训练-推理偏差？
- 是否可以将更先进的 3D 表示（如 3D Gaussian Splatting 或 NeRF）纳入融合模块，替代 VGGT 特征以提升几何一致性？
- 注意力汇机制如何适应场景突变？是否需要引入可控的上下文遗忘机制？
- 该方法在更高分辨率（1024×1024+）或更长周期（数分钟至一小时）下的资源消耗和质量表现如何？

### 补充图表

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/012_Figure_6.jpg]]
*Figure 6: Semantic ablations*

![[assets/figures/papers/paper_list_l2252_https_arxiv_org_abs_2512_12430/figures/013_Figure_7.jpg]]
*Figure 7: Quality ablations*



## 定位与知识库关联

### 问题定位：自回归视频生成的训练-推理鸿沟

Endless World 的核心贡献在于系统性地诊断并修复了自回归视频生成中长期存在的**训练-推理不匹配**问题。在传统的自回归框架（本文称为 Self-Forcing）中，训练时条件帧在当前模型参数 $\phi$ 下可微，梯度流经整个序列：

$$p_{\phi}(v_{1:n}) = \prod_{k=1}^{n} p_{\phi}(v_k \mid v_{<k}^{\phi})$$

这导致优化过程同时更新过去帧与未来帧，形成一种“作弊”式的联合优化。然而在推理时，已生成帧被固定为常数，条件分布发生偏移，累积误差迅速放大，表现为运动漂移、闪烁和几何不一致（Figure 3 中以牛行走方向突变为例直观展示了这一退化）。这一诊断将 Endless World 与现有自回归视频扩散模型（如 **CausVid** (Yin et al., CVPR 2025) 的因果掩码策略、**MAGI-1** (Teng et al., 2025) 的逐帧生成）区分开来——后者虽采用自回归范式，但未显式解决条件帧梯度泄漏导致的训练-推理分布偏移。

### 核心机制：梯度分离与三维结构注入

Endless World 的解决方案由两个正交且互补的机制构成：

**1. 梯度分离的条件生成。** 将前序视频帧的计算图与梯度更新分离（detach），使训练目标精确匹配推理时的固定条件：

$$p_{\phi}(v_{1:n}) = \prod_{k=i}^{n} p_{\phi}(v_k \mid v_{i:k}^{\phi}, v_{<i}^{\mathrm{detach}})$$

这一改动看似简单，实则从根本上阻断了误差累积的源头。Figure 4 对比了 Self-Forcing 与 Endless World 的梯度流差异：前者梯度贯穿全序列，后者仅新生成帧参与更新。消融实验（Table 3）证实，单独引入条件生成使 VBench 总分从 82.94 提升至 83.30。

**2. 文本级三维结构融合。** 通过预训练的 VGGT 编码器从视频帧中提取三维结构特征 $\hat{f}_{3D}$，经可学习 CNN 融合模块投影后与文本嵌入相加：

$$\tilde{e} = f_{\mathrm{fusion}}(e_{\mathrm{text}}, \hat{f}_{3D})$$

这一设计的关键决策在于**融合层级的选择**：将 3D 特征注入全局文本令牌空间，而非潜空间。消融分析明确指出，潜空间融合虽能保留几何信息，但会破坏局部运动模式，引入光流不一致和闪烁伪影。文本级融合则使 3D 信息被所有帧全局关注，在提升多物体一致性（+8.82）和美学质量（+4.61）的同时保持运动自然度（Table 4）。

### 知识库定位：与相关工作的关系

**与自回归视频生成基线的关系。** 最直接的前置工作是 **Self-Forcing** (Huang et al., 2025)，Endless World 在其基础上通过梯度分离和 3D 融合实现了质的提升。与 **CausVid** (Yin et al., CVPR 2025) 的因果掩码自回归策略相比，Endless World 的条件自回归范式更直接地对齐了训练与推理条件，而非仅依赖注意力掩码的时序约束。

**与快速扩散模型的吞吐量优势。** 在单张 H100 GPU 上，Endless World 达到 17.0 FPS 的生成吞吐量，显著超越最快的扩散模型 **LTX-Video** (HaCohen et al., 2025) 的 8.98 FPS（Table 1）。这一优势源于自回归范式避免了扩散模型的多步去噪开销，同时 DMD 分布匹配蒸馏以训练自由的方式进一步压缩了推理成本。

**与长视频生成系统的对比。** 在 60 秒视频生成任务上，Endless World 的质量得分（84.73）显著超过交互式系统 **LongLive** (Yang et al., 2025) 的单提示设置（约 82.07，Table 2）。更重要的是，Table 6 显示 Self-Forcing 随视频长度增加持续退化，而 Endless World 的 60 秒总分（82.31）仍超过 Self-Forcing 的 30 秒水平（81.59），证明了梯度分离策略对长序列稳定性的根本性改善。

**注意力汇机制的引入。** 为应对长序列生成中的上下文遗忘，Endless World 引入注意力汇（Attention Sink），保留初始帧的全部令牌作为持久上下文，并对 KV 缓存应用旋转位置嵌入。消融显示，仅此一项便将 30 秒视频总分从 81.59 提升至 82.94（Table 3），体现了显式记忆机制对时空连贯性的关键作用。

### 适用边界与局限

1. **骨干网络依赖。** 当前训练和推理均基于 **Wan2.1-1.3B** (Team Wan et al., 2025) 骨干，该方法在更大规模模型或不同架构（如 DiT 变体）上的可迁移性尚未验证。

2. **三维特征提取的分布敏感性。** 3D 结构引导依赖预训练 VGGT 编码器，当视频内容超出其训练分布时（如极端视角、非自然场景），结构引导可能退化。论文未对此类边界情况进行消融。

3. **3D 相似性损失的权衡。** 可选的 3D 一致性正则项（$\mathcal{L}_{3\mathrm{D}}$，权重 $\lambda_{3\mathrm{D}}=0.1$）在增强几何一致性的同时轻微降低运动平滑度（Table 5），因此被定位为可选项而非默认组件，需根据应用场景取舍。

4. **单提示生成范式。** 当前实验仅覆盖单提示长视频生成，未探索多提示切换或交互式场景。注意力汇机制对场景突变的适应性（是否需要引入遗忘机制）仍是开放问题。

### 开放问题

- **分辨率与时长扩展。** 该方法在更高分辨率（1024+）或超长周期（数分钟至一小时）下的性能退化曲线和资源消耗特征尚不明确。
- **三维表示的进化空间。** 当前使用 VGGT 提取的隐式 3D 特征，是否可纳入更显式的几何表示（如神经辐射场、3D 高斯抛雪球）以进一步提升结构一致性？
- **梯度分离策略的泛化性。** 该策略本质上解决的是自回归生成中的训练-推理条件偏移问题，理论上可推广至音频、文本等其他模态的自回归生成任务，但缺乏跨模态验证。
- **代码与权重的可复现性。** 截至分析时点，仅项目页面公开，模型权重与代码未完全发布，部分结论需在开源后独立验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Endless_World_Real_Time_3D_Aware_Long_Video_Generation.pdf]]
