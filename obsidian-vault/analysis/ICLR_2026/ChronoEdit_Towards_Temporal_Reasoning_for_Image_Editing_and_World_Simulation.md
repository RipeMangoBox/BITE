---
title: "ChronoEdit: Towards Temporal Reasoning for Image Editing and World Simulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ChronoEdit_Towards_Temporal_Reasoning_for_Image_Editing_and_World_Simulation.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/chronoedit/
aliases:
- ChronoEdit
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "将图像编辑任务重新定义为两帧视频生成问题，并引入显式的时间推理阶段，利用预训练视频模型的时序先验，通过中间帧作为推理令牌来规划物理上合理的编辑轨迹。"
primary_logic: "在推理时，仅在前几个高噪声去噪步骤中使用视频推理令牌进行全局规划，随后丢弃中间帧以大幅降低计算开销，从而在保证编辑质量与物理一致性的同时，保持与标准图像编辑相近的效率。"
claims:
- "当前最先进的图像编辑模型在物理一致性方面经常失败，产生幻觉对象或几何扭曲，而ChronoEdit能保持场景一致。"
- "ChronoEdit在ImgEdit通用编辑基准上整体得分4.42，大幅超越最强开源基线FLUX.1 Kontext [Dev]（差值+0.90）。"
- "在自建的PBench-Edit物理一致性基准上，ChronoEdit-14B-Think整体评分4.53，动作保真度4.31，显著优于无推理版本（4.01）。"
- "仅使用前10步时间推理（N_r=10，总步数50）即可达到与全程推理相当的性能，并将推理时间从55.5秒降至35.3秒。"
---

# ChronoEdit: Towards Temporal Reasoning for Image Editing and World Simulation

> [!tip] 核心洞察
> 在推理时，仅在前几个高噪声去噪步骤中使用视频推理令牌进行全局规划，随后丢弃中间帧以大幅降低计算开销，从而在保证编辑质量与物理一致性的同时，保持与标准图像编辑相近的效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ChronoEdit：面向图像编辑与世界模拟的时间推理 |
| 英文题名 | ChronoEdit: Towards Temporal Reasoning for Image Editing and World Simulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.04290) · [Project](https://research.nvidia.com/labs/toronto-ai/chronoedit) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ChronoEdit |
| Dataset | ImgEdit Basic-Edit Suite, PBench-Edit, Inference Speed (H100 GPU) |

> [!tip] 效果简介
> - ImgEdit Basic-Edit Suite 上，Overall Score (GPT-4.1 eval) ↑ 为 4.42 (ChronoEdit-14B)，对比 3.52 (FLUX.1 Kontext [Dev])，变化 +0.90。
> - PBench-Edit 上，Action Fidelity ↑ 为 4.31 (ChronoEdit-14B-Think)，对比 4.01 (ChronoEdit-14B w/o Think)，变化 +0.30。
> - Inference Speed (H100 GPU) 上，Runtime per image (s) ↓ 为 5.0 (ChronoEdit-14B-Turbo, 8 steps)，对比 35.3 (ChronoEdit-14B, 50 steps)，变化 -85.8%。

## 概要

图像编辑模型在追求视觉逼真度的同时，长期忽视了一个关键维度——**物理一致性**。现有最先进的方法在涉及世界模拟的编辑任务中频繁失败，表现为幻觉出不存在的物体、扭曲场景几何结构或破坏物体间的时空连续性（Figure 2）。这一瓶颈的根本原因在于：纯数据驱动的编辑范式缺乏显式的时序约束机制，无法对编辑过程中物体的运动轨迹和状态变化进行物理上合理的规划。

**ChronoEdit** 针对这一核心问题，提出了一种范式转换方案——将图像编辑重新定义为**两帧视频生成问题**。其核心洞察是：预训练的视频生成模型天然蕴含丰富的时序先验，能够理解物体如何在时间维度上连续变化。通过将输入图像与目标编辑图像视为视频的首尾帧，并在二者之间插入随机初始化的中间帧作为**时间推理令牌**（temporal reasoning tokens），模型在去噪早期阶段隐式地规划出一条物理上合理的编辑轨迹，从而显著提升编辑结果的物理一致性。

该方法的关键创新在于**推理与生成的解耦**：时间推理仅在前几个高噪声去噪步骤中进行全局规划，随后中间帧被直接丢弃，后续步骤仅精炼目标帧。这一设计使得 ChronoEdit 在保证编辑质量的同时，大幅降低了计算开销——仅使用前 10 步推理（总步数 50）即可达到与全程推理相当的性能，推理时间从 55.5 秒降至 35.3 秒（Figure 8）。进一步结合 DMD 蒸馏技术，8 步学生模型 ChronoEdit-Turbo 将单张图像推理时间压缩至 5.0 秒，实现 6 倍加速。

在实验验证上，ChronoEdit 展现出全面的优势：
- **通用编辑能力**：在 ImgEdit 基准上，ChronoEdit-14B 整体得分 4.42，大幅超越最强开源基线 **FLUX.1 Kontext [Dev]**（Labs et al., 2025）的 3.52，差值达 +0.90（Table 1）。
- **物理一致性**：在自建的 PBench-Edit 物理一致性基准上，ChronoEdit-14B-Think 整体评分 4.53，动作保真度 4.31，显著优于无推理版本（4.01），验证了时间推理机制的关键作用（Table 2）。
- **推理效率**：通过两阶段推理与蒸馏加速的组合策略，ChronoEdit 在保持与 50 步模型相当质量的前提下，将推理速度提升至实时交互水平。

**方法定位**：ChronoEdit 处于图像编辑与视频生成的交叉地带，其核心贡献不在于提出新的网络架构，而在于**重新定义了编辑任务的建模形式**——从单步像素映射转变为时序规划问题，并以轻量级的时间推理令牌机制实现了对预训练视频模型先验的高效利用。这一思路为构建物理一致的世界模拟器提供了新的技术路径。

**局限与展望**：当前方法聚焦于两帧编辑设置，对长时程交互、多物体精细操作等复杂场景的扩展能力尚未验证；评价体系主要依赖 GPT-4.1 自动评估，缺乏全面的人工主观评价。未来工作可探索将时间推理机制扩展到连续视频生成、动态 3D 世界仿真，以及根据编辑指令复杂度自适应调整推理步数的动态规划策略。

### 图像编辑的物理一致性瓶颈

图像编辑技术近年来取得了长足进步，以 **FLUX.1 Kontext [Dev]**（Labs et al., 2025）、**OmniGen2**（Xiao et al., CVPR 2025）、**Qwen-Image**（Wu et al., arXiv 2025）为代表的开源模型，以及 **GPT-4o**（OpenAI, 2025）、**Gemini2.5 Flash Image**（Google, 2025）等商业闭源系统，在指令跟随和视觉保真度方面展现出令人瞩目的能力。然而，当编辑任务涉及物理世界模拟时——例如“打开烤箱门”、“将杯子放在桌子上”或“让汽车转弯”——这些模型的根本缺陷便暴露出来。

**核心瓶颈在于**：现有图像编辑模型缺乏物理一致性，在需要保持物体连续性和几何结构的仿真任务中容易产生幻觉或不期望的变化。如 **Figure 2** 所示，当前最先进的图像编辑模型在处理世界模拟类编辑任务时频繁失败：它们可能凭空生成不应存在的物体（幻觉对象），或扭曲场景的几何结构，导致编辑结果与指令相悖或与场景上下文脱节。这一现象的根本原因在于，这些纯数据驱动的方法缺乏明确的时序约束机制——它们将图像编辑视为直接的单步像素映射或条件图像生成，没有对编辑过程中物体状态变化的中间轨迹进行任何形式的显式建模。

### 视频生成模型的时间先验潜力

与此同时，大规模视频生成模型在预训练过程中天然习得了丰富的时序先验知识——它们理解物体如何在时间维度上连续运动、变形和交互。这种时间一致性建模能力恰好是图像编辑任务所缺失的关键要素。然而，直接将视频模型应用于图像编辑面临两个挑战：其一，图像编辑的输入-输出对并非天然的视频序列；其二，完整的视频生成推理计算开销巨大，难以满足实际编辑场景的效率需求。

### ChronoEdit 的核心动机

ChronoEdit 的提出正是为了弥合这一鸿沟。其核心动机在于：**将图像编辑任务重新定义为两帧视频生成问题，并引入显式的时间推理阶段，利用预训练视频模型的时序先验，通过中间帧作为推理令牌来规划物理上合理的编辑轨迹。** 具体而言，给定输入图像和编辑指令，模型在输入帧与目标输出帧之间“想象”并去噪一段简短的视频轨迹，这些中间帧作为时间推理令牌，隐式地规划编辑动作如何以物理一致的方式展开。

这一设计的关键洞察在于效率与质量的巧妙平衡：**在推理时，仅在前几个高噪声去噪步骤中使用视频推理令牌进行全局规划，随后丢弃中间帧以大幅降低计算开销。** 实验表明，在总计50步的去噪过程中，仅使用前10步进行时间推理（N_r=10），即可达到与全程推理相当的性能，同时将推理时间从55.5秒降至35.3秒（**Figure 8**）。这种“先规划、后精炼”的策略使得 ChronoEdit 在保证编辑质量与物理一致性的同时，保持了与标准图像编辑相近的效率。

## 核心方法与创新机理

ChronoEdit的核心创新在于将图像编辑任务重新定义为**两帧视频生成问题**，并引入**显式的时间推理阶段**来规划物理上合理的编辑轨迹。这一设计直接针对现有图像编辑模型的根本瓶颈：纯数据驱动的单步映射缺乏时序约束机制，导致在需要保持物体连续性和几何结构的仿真任务中频繁产生幻觉或不期望的变化（Figure 2）。

### 任务建模形式的根本转变

传统图像编辑器将编辑视为直接的单步像素/潜空间映射或条件图像生成——输入原图与编辑指令，直接预测最终图像。ChronoEdit则利用预训练视频模型内在的时间先验，将输入图像和编辑后的目标图像建模为同一视频序列的首帧和末帧。具体而言，输入图像被编码为第一帧潜变量 $z_c = E(c)$，目标图像则被重复4次以匹配视频VAE的4倍时间压缩比，编码为 $z_p = E(\text{repeat}(p,4))$。这一建模转变使得模型能够利用视频生成中学习到的物体运动连续性和场景几何一致性先验，从根本上约束编辑输出的物理合理性（Sec. 3.2）。

### 时间推理令牌：隐式编辑规划

在输入与输出潜变量之间，ChronoEdit插入随机噪声初始化的中间帧作为**时间推理令牌**（temporal reasoning tokens $r$）。这些令牌在去噪过程中充当模型的“想象空间”，通过联合去噪隐式规划从原图到目标图的过渡轨迹——例如，当指令要求“将杯子向右移动”时，推理令牌会自然演化出杯子在中间位置的潜表示，从而约束最终编辑结果保持物体的形状、光照和空间关系一致性（Figure 3）。

这一机制的关键洞察在于：**推理令牌仅在前 $N_r$ 个高噪声去噪步骤中参与全局结构规划，随后即被丢弃**。在剩余 $N - N_r$ 步中，模型仅精炼目标帧，无需为中间帧支付额外计算开销。消融实验表明，仅使用 $N_r = 10$ 步推理（总步数 $N = 50$）即可达到与全程推理相当的性能，同时将推理时间从55.5秒降至35.3秒（Figure 8）。这一设计在保证编辑质量与物理一致性的同时，保持了与标准图像编辑相近的效率。

### 推理加速：从50步到8步的蒸馏

为进一步提升实际部署效率，ChronoEdit采用分布匹配蒸馏（DMD）技术将50步整流流模型压缩为8步学生模型。蒸馏目标为：

$$\nabla \mathcal{L}_{\mathrm{DMD}} = - \mathbb{E}_{t} \left( \int \left( s_{\mathrm{real}} ( f( \mathbf{F}_{\theta}, t ), t ) - s_{\mathrm{fake}} ( f( \mathbf{F}_{\theta}, t ), t ) \right) \frac{d \mathbf{F}_{\theta}}{d \theta} dz \right)$$

其中 $s_{\text{real}}$ 和 $s_{\text{fake}}$ 分别为真实数据分布和生成分布的评分函数。蒸馏后的ChronoEdit-14B-Turbo在保持编辑质量的同时实现6倍加速（从30.4秒降至5.0秒，2块H100 GPU），使得物理一致性编辑在实际应用中变得可行（Figure 7, Sec. 3.4）。

### 与基线的差异化总结

| 创新维度 | 基线方法 | ChronoEdit |
|---------|---------|------------|
| 任务建模 | 单步像素/潜空间映射 | 两帧视频序列生成，利用预训练视频模型时间先验 |
| 编辑规划 | 无显式中间状态规划 | 插入随机初始化中间帧作为推理令牌，隐式规划编辑轨迹 |
| 推理效率 | 生成完整中间帧或全程保留推理令牌 | 仅前 $N_r$ 步使用推理令牌，随后丢弃，大幅降低计算量 |
| 部署加速 | 标准整流流采样（~50步） | DMD蒸馏至8步，推理速度提升6倍 |

这些创新共同构成了ChronoEdit的方法论核心：通过重新定义任务形式、引入可丢弃的时间推理令牌、以及蒸馏加速，在保持高效推理的前提下，首次为图像编辑模型赋予了显式的物理一致性推理能力。

ChronoEdit 的整体框架围绕一个核心洞察展开：将图像编辑任务重新定义为**两帧视频生成问题**，从而复用预训练视频模型内嵌的时序先验，在输入图像与编辑目标之间建立物理一致的过渡轨迹。图 3 展示了该流水线的完整结构。

### 任务建模与潜空间编码

给定输入图像 $c$ 和目标输出图像 $p$，ChronoEdit 不将其视为孤立的像素映射，而是建模为一个极短的两帧视频序列。具体而言，输入图像被编码为视频 VAE 的第一帧潜变量 $\mathbf{z}_c = E(c)$；输出图像则被复制四次以匹配视频 VAE 的 $4\times$ 时间压缩比，编码为 $\mathbf{z}_p = E(\text{repeat}(p, 4))$。这一编码策略使编辑对能够无缝嵌入预训练视频模型的潜在空间，实验表明其重建 PSNR 仅从 40.21 dB 略微下降至 39.82 dB，但显著提升了对预训练分布的适配性。

### 时间推理令牌机制

框架的关键创新在于 $\mathbf{z}_c$ 与 $\mathbf{z}_p$ 之间插入随机噪声初始化的中间帧潜变量，称为**时间推理令牌** $\mathbf{r}$。这些令牌不直接对应任何真实图像，而是作为模型“想象”编辑动作如何展开的隐式规划空间。在推理过程中，模型通过联合去噪 $\mathbf{z}_c$、$\mathbf{r}$ 和 $\mathbf{z}_p$，学习一条物理上合理的过渡轨迹——例如，当指令为“将苹果从桌上移到篮子里”时，推理令牌会隐式编码苹果的移动路径与场景遮挡关系。

### 两阶段去噪推理

ChronoEdit 的推理流水线分为两个阶段（见 Algorithm 1），以平衡物理一致性与计算效率：

- **时间推理阶段**（前 $N_r$ 步）：将干净的输入令牌 $\mathbf{z}_c$、随机采样的推理令牌 $\mathbf{r}$ 和噪声化的输出令牌 $\mathbf{z}_p$ 拼接为完整时序序列 $\mathbf{z}_{\text{full}}$，送入整流流去噪器进行联合去噪。此阶段模型进行全局结构规划，确保编辑动作与场景上下文保持时序对齐。
- **编辑帧生成阶段**（剩余 $N - N_r$ 步）：丢弃推理令牌 $\mathbf{r}$，仅对部分去噪的输出潜变量 $\mathbf{z}_p$ 进行进一步精炼，生成最终编辑图像。由于推理令牌已被移除，后续去噪的计算量与标准图像编辑相当。

这一设计的关键效率优势在于：时间推理仅在去噪初期的高噪声步骤中执行，此时模型主要决定全局布局与动作方向；一旦结构规划完成，中间帧即可安全丢弃。消融实验证实，在总步数 $N = 50$ 的设置下，仅使用 $N_r = 10$ 步推理即可达到与全程推理（$N_r = 50$）相当的编辑质量，同时将推理时间从 55.5 秒降至 35.3 秒。

### 骨干网络与蒸馏加速

ChronoEdit 的去噪骨干基于预训练的图像到视频整流流模型。论文实现了两个规模版本：**ChronoEdit-14B** 从 Wan2.1-I2V-14B-720P 微调而来，**ChronoEdit-2B** 则构建于 Cosmos-Predict2.5-2B 之上。训练采用流匹配损失：

$$\mathcal{L}_{\theta} = \mathbb{E}_{t \sim p(t), \mathbf{x} \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}(\mathbf{0}, I)} \left[ \lVert \mathbf{F}_{\theta}(\mathbf{z}_t, t; \mathbf{y}, \mathbf{c}) - (\epsilon - \mathbf{z}_0) \rVert_2^2 \right]$$

其中 $\mathbf{F}_{\theta}$ 为去噪器，预测目标速度场 $(\epsilon - \mathbf{z}_0)$，$\mathbf{y}$ 为文本指令条件，$\mathbf{c}$ 为输入图像条件。

为进一步提升推理效率，ChronoEdit 采用分布匹配蒸馏（DMD）技术将 50 步模型压缩为 8 步学生模型 **ChronoEdit-14B-Turbo**。DMD 损失梯度为：

$$\nabla \mathcal{L}_{\mathrm{DMD}} = - \mathbb{E}_{t} \left( \int \left( s_{\mathrm{real}} ( f( \mathbf{F}_{\theta}, t ), t ) - s_{\mathrm{fake}} ( f( \mathbf{F}_{\theta}, t ), t ) \right) \frac{d \mathbf{F}_{\theta}}{d \theta} dz \right)$$

其中 $s_{\mathrm{real}}$ 和 $s_{\mathrm{fake}}$ 分别为真实分布与生成分布的评分函数。蒸馏后的模型在保持编辑质量的同时实现 6 倍加速，推理时间从 30.4 秒降至 5.0 秒（2×H100 GPU 测量）。

### 模块关系总结

整个流水线可归纳为五个核心模块的协同：**视频 VAE 编码**将编辑对嵌入视频潜空间；**时间推理令牌**提供隐式规划能力；**两阶段去噪推理**以极低开销实现结构规划；**整流流去噪骨干**提供强大的视频先验；**DMD 蒸馏**则大幅提升部署效率。这一设计使得 ChronoEdit 在保持与标准图像编辑相近计算成本的前提下，显著增强了编辑结果的物理一致性。

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2510_04290/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the ChronoEdit pipeline. From right to left, the denoising process begins in the temporal reasoning stage, where the model imagines and denoises a short trajectory of intermediate frames. These intermediate frames act as reasoning tokens, guiding how the edit should unfold in a physically consistent manner. For efficiency, the reasoning tokens are discarded in the subsequent editing frame generation stage, where the target frame is further refined into the final edited image*

### 整流流去噪骨干

ChronoEdit 的核心生成引擎基于预训练的图像到视频（I2V）扩散模型，采用**整流流（Rectified Flow）**框架进行训练。给定数据样本 $\mathbf{x} \sim p_{\mathrm{data}}$，前向过程通过线性插值构造噪声潜变量 $\mathbf{z}_t = t \cdot \epsilon + (1 - t) \cdot \mathbf{z}_0$，其中 $\mathbf{z}_0 = E(\mathbf{x})$ 为视频 VAE 编码后的干净潜变量，$\epsilon \sim \mathcal{N}(\mathbf{0}, I)$ 为标准高斯噪声。去噪器 $\mathbf{F}_{\theta}$ 的训练目标为预测速度场 $(\epsilon - \mathbf{z}_0)$：

$$
\mathcal{L}_{\theta} = \mathbb{E}_{t \sim p(t), \mathbf{x} \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}(\mathbf{0}, I)} \left[ \lVert \mathbf{F}_{\theta}(\mathbf{z}_t, t; \mathbf{y}, \mathbf{c}) - (\epsilon - \mathbf{z}_0) \rVert_2^2 \right]
$$

其中 $\mathbf{y}$ 为编辑指令的文本嵌入，$\mathbf{c}$ 为输入图像条件。该损失函数使模型学习从噪声状态 $\mathbf{z}_t$ 向干净数据 $\mathbf{z}_0$ 的最优传输路径，为后续的时间推理提供强大的视频时序先验。

### 编辑对的视频编码

为将图像编辑任务适配到视频生成框架，ChronoEdit 对输入-输出图像对进行特殊的潜变量编码。设输入图像为 $c$，目标编辑图像为 $p$，视频 VAE 编码器为 $E(\cdot)$。由于预训练视频 VAE 具有 $4\times$ 的时间压缩比（即每 4 帧压缩为 1 个潜变量组），单帧图像无法直接匹配其时间维度。因此，输入图像编码为第一帧潜变量 $\mathbf{z}_c = E(c)$，而输出图像则重复 4 次后编码：$\mathbf{z}_p = E(\mathrm{repeat}(p, 4))$。消融实验表明，这种重复编码策略虽使重建 PSNR 从 40.21 dB 略微下降至 39.82 dB，但更契合预训练视频模型的潜变量分布，从而保证编辑质量。

### 时间推理令牌

在输入潜变量 $\mathbf{z}_c$ 与输出潜变量 $\mathbf{z}_p$ 之间，ChronoEdit 插入一组随机噪声初始化的中间帧潜变量，称为**时间推理令牌** $\mathbf{r}$。这些令牌在去噪过程中充当隐式的编辑轨迹规划器——模型通过联合优化 $\mathbf{z}_c$、$\mathbf{r}$ 和 $\mathbf{z}_p$ 的时序序列，隐式地“想象”从输入到输出的物理过渡过程，从而约束输出帧与输入场景保持几何结构与时序一致性。

### 两阶段去噪推理

ChronoEdit 的推理过程分为两个阶段，如 Algorithm 1 所示：

- **第一阶段（时间推理阶段）**：将干净的输入令牌 $\mathbf{z}_c$、随机采样的推理令牌 $\mathbf{r}$ 和噪声化的输出令牌 $\mathbf{z}_p$ 拼接为完整时序序列 $\mathbf{z}_{\mathrm{full}}$，在前 $N_r$ 步去噪中联合优化。此阶段利用视频模型的时序先验进行全局编辑规划。
  
- **第二阶段（编辑帧生成阶段）**：丢弃推理令牌 $\mathbf{r}$，仅保留部分去噪后的输出潜变量，在剩余的 $N - N_r$ 步中完成最终编辑帧的精炼。

实验表明，仅需 $N_r = 10$（总步数 $N = 50$）即可达到与全程推理相当的性能，同时将推理时间从 55.5 秒降至 35.3 秒。

### DMD 蒸馏加速

为进一步提升推理效率，ChronoEdit 采用**分布匹配蒸馏（DMD）**技术训练轻量级学生模型。DMD 通过最小化学生模型生成分布与教师模型真实分布之间的差异，将推理步数从 50 步压缩至 8 步。其损失梯度为：

$$
\nabla \mathcal{L}_{\mathrm{DMD}} = - \mathbb{E}_{t} \left( \int \left( s_{\mathrm{real}}(f(\mathbf{F}_{\theta}, t), t) - s_{\mathrm{fake}}(f(\mathbf{F}_{\theta}, t), t) \right) \frac{d \mathbf{F}_{\theta}}{d \theta} dz \right)
$$

其中 $s_{\mathrm{real}}$ 和 $s_{\mathrm{fake}}$ 分别为真实分布与生成分布的评分函数，$f(\mathbf{F}_{\theta}, t)$ 表示学生模型在时间步 $t$ 的一步预测结果。蒸馏后的 ChronoEdit-14B-Turbo 模型推理时间从 30.4 秒降至 5.0 秒，实现 6 倍加速，且编辑质量与原始 50 步模型相当。

## 实验与关键发现

### 通用图像编辑能力评估

为检验ChronoEdit在去除时间推理机制后作为纯图像编辑器的能力，作者在**ImgEdit Basic-Edit Suite**（Ye et al., 2025）上进行了全面评测。该基准涵盖背景替换、物体移除、物体替换、颜色编辑、风格迁移、视角变换和文本编辑七类任务，所有指标均由GPT-4.1自动评估。

**Table 1** 报告了定量对比结果。**ChronoEdit-14B**以整体得分**4.42**位列第一，大幅超越最强开源基线**FLUX.1 Kontext [Dev]**（Labs et al., 2025）的3.52分，差值达**+0.90**。这一优势在各项子任务中普遍存在，尤其在背景替换（4.51 vs 3.61）、物体替换（4.38 vs 3.42）和风格迁移（4.56 vs 3.63）上领先超过0.8分。轻量版**ChronoEdit-2B**同样取得4.13的整体得分，优于OmniGen2（Xiao et al., CVPR 2025）的3.82和Qwen-Image（Wu et al., arXiv 2025）的3.89，表明方法在不同模型规模下均有效。

值得注意的是，ChronoEdit-14B的得分已逼近商业闭源系统**Gemini2.5 Flash Image**（Google, 2025）的4.49和**GPT-4o**（OpenAI, 2025）的4.46，差距仅在0.04-0.07之间。考虑到这些商业系统可能受益于更大规模的训练数据和专有优化，ChronoEdit作为开源方案展现出极强的竞争力。

### 物理一致性专项评估

为验证时间推理机制对物理一致性的提升，作者构建了**PBench-Edit**基准，从动作保真度、几何结构保持、幻觉抑制和整体视觉质量四个维度进行评估。**Table 2** 展示了关键结果。

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2510_04290/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison results on PBench-Edit. All metrics are evaluated by GPT-4.1. “Overall” is calculated by averaging all scores across dimensions*

开启时间推理的**ChronoEdit-14B-Think**以整体得分**4.53**、动作保真度**4.31**达到当前最优水平。与禁用推理的版本（整体4.01，动作保真度3.62）相比，动作保真度提升**+0.69**，整体提升**+0.52**，清晰验证了时间推理令牌在规划物理合理编辑轨迹中的关键作用。在几何结构保持（4.62 vs 4.18）和幻觉抑制（4.59 vs 4.12）维度上，推理版本的增益同样显著，印证了**Figure 2**中呈现的定性观察——基线模型在物理仿真类任务中容易产生幻觉物体或几何扭曲，而ChronoEdit-Think能有效避免此类失效模式。

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2510_04290/figures/002_Figure_2.jpg]]
*Figure 2: Failure cases of state-of-the-art image editing models. Current state-of-the-art models often struggle to maintain physical consistency on world simulation-related editing tasks. They may hallucinate unintended objects or distort scene geometry. In contrast, our method produces edits that are faithful to the instruction and remain coherent with the scene. Prompts (from top to bottom): (1) “The left silver SUV makes a U-turn”, (2) “Pick up the spoon with the robot arm”, and (3) “Close the wooden piece by hand”*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2510_04290/figures/017_Figure.jpg]]
*Figure: (e) N _ { r } = 5 0 Figure S3: More qualitative ablation on video reason step N _ { r } . Empirically, we found that setting the reasoning timestep to N _ { r } = 1 0 within a total of N = 50 sampling steps achieves performance that is comparable to using reasoning across the full trajectory*

**Figure 4** 提供了与多种基线的定性对比。在ImgEdit的通用编辑任务（前两行）和PBench-Edit的物理任务（末行）上，ChronoEdit均能更忠实地遵循编辑指令，同时保持场景结构和细节完整性。**Figure 5** 进一步展示了ChronoEdit-14B-Think在物理AI世界模拟任务上的输出，涵盖物体姿态改变、场景元素交互等复杂情形，编辑结果在视觉可信度和物理合理性之间取得了良好平衡。

### 推理效率与蒸馏加速

时间推理虽提升了编辑质量，但引入中间帧会带来额外计算开销。**Figure 8** 的消融实验揭示了推理步数 $N_r$ 与性能的关系：在总采样步数 $N=50$ 的设置下，仅使用前 **$N_r=10$** 步进行时间推理即可获得与全程推理（$N_r=50$）相当的编辑质量，而推理时间从55.5秒降至**35.3秒**，减少约36%。附录**Figure S3**补充了更多定性消融案例，进一步验证了该发现的稳健性。这一现象表明，编辑的全局结构规划主要发生在去噪早期的高噪声阶段，后期步骤仅需对目标帧进行精细优化，无需保留推理令牌。

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2510_04290/figures/014_Figure_8.jpg]]
*Figure 8: Qualitative ablation on video reason step Nr. Empirically, we found that setting the reasoning timestep to N _ { r } = 1 0 within a total of N = 50 sampling steps achieves performance that is comparable to using reasoning across the full trajectory. Example Prompt: “Halve the poached egg to reveal the yolk”. Reported runtime is measured on Nvidia-H100 GPUs*

为进一步提升部署效率，作者采用**DMD蒸馏**（Yin et al., 2024）将ChronoEdit-14B压缩为8步学生模型**ChronoEdit-14B-Turbo**。**Figure 7** 的定性对比显示，Turbo版本在5.0秒内完成的编辑质量与原始模型35.3秒的输出高度相似，实现了约**6倍**的推理加速。这一结果验证了分布匹配蒸馏在保持编辑质量的前提下大幅压缩推理步数的有效性。

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2510_04290/figures/013_Figure_7.jpg]]
*Figure 7: Qualitative result of ChronoEdit-Turbo. The lightweight ChronoEdit-Turbo (runtime 5.0s) achieves editing quality similar to ChronoEdit (runtime 35.3s) while offering improved efficiency. (Left: “Extract the red telephone booth in the image”. Right: “Replace the bicycle in the image with a wooden park bench”.) (a) Reference Image*

### 训练策略消融

附录中的消融实验揭示了两个关键训练设计选择的影响。**Figure S2** 表明，使用预训练视频模型初始化能够显著加快收敛速度并提高训练稳定性，编辑效果优于从零开始训练的方案，这归因于预训练权重中蕴含的丰富时间先验为编辑任务提供了良好的归纳偏置。

在编码策略方面，将输出图像重复4次后与输入图像联合编码的方案虽使重建PSNR略微下降（39.82 vs 40.21 dB），但更契合预训练视频VAE的潜变量分布，有利于模型利用已有的视频生成知识，最终编辑质量更优。这一权衡体现了“匹配预训练分布”优先于“完美像素重建”的设计哲学。

### 评价体系与局限性说明

需指出，当前所有自动指标均基于GPT-4.1评估，可能引入大语言模型的固有偏好，缺乏大规模人工主观评价的补充。与商业闭源系统的比较受API接口速率和版本差异影响，并非完全公平的配对测试。此外，蒸馏后的8步模型在少数极端场景中可能存在细节退化风险，尽管总体质量与50步模型相当。推理速度测量均在2块NVIDIA-H100 GPU上进行，硬件环境一致保证了效率对比的公平性。

## 定位与知识库关联

### 核心瓶颈与因果机制

当前图像编辑模型，无论是基于扩散的指令跟随编辑器还是多模态大模型，在面对需要保持物理一致性的任务时频繁失效——它们会幻觉出不应出现的物体、扭曲场景几何结构，或在物体移动后无法维持其完整性和上下文关系（Figure 2）。这一瓶颈的根源在于：**现有方法将图像编辑建模为纯粹的单步像素/潜空间映射或条件生成，缺乏对编辑过程中间状态及其物理约束的显式建模**。纯数据驱动的端到端训练无法为模型注入时序一致性先验，导致编辑结果虽然在表面视觉上可能合理，但在因果和物理层面容易崩溃。

ChronoEdit 的核心因果调节旋钮是**将图像编辑任务重新定义为两帧视频生成问题**，并引入显式的时间推理阶段。具体而言，该方法利用预训练图像到视频（I2V）模型内在的时序先验，将输入图像和编辑目标图像分别作为视频的第一帧和最后一帧，在两者之间插入随机初始化的中间潜变量帧作为“时间推理令牌”（temporal reasoning tokens）。在去噪的早期高噪声阶段，模型联合优化这些推理令牌和输出帧，从而隐式地规划出一条物理上合理的编辑轨迹；在后续阶段，推理令牌被丢弃，仅对目标帧进行精炼。这一设计使得模型在推理时能够“想象”编辑如何逐步发生，而非直接跳跃到最终结果。

### 与基线方法的关系与定位

ChronoEdit 在任务建模层面与当前主流图像编辑器形成根本性差异：

- **FLUX.1 Kontext [Dev]**（Labs et al., 2025）作为强大的开源指令跟随图像编辑器，基于数十亿参数扩散模型，将编辑视为直接的条件图像生成任务，不包含任何中间状态规划。ChronoEdit 在 ImgEdit 通用编辑基准上以 4.42 的整体得分大幅超越 FLUX.1 Kontext [Dev] 的 3.52（差值 +0.90），并在物理一致性方面展现出质的差异。
- **OmniGen2**（Xiao et al., CVPR 2025）和 **Qwen-Image**（Wu et al., arXiv 2025）分别代表统一多模态生成框架和基于视觉-语言模型的双流架构编辑器，它们均以端到端方式直接预测最终图像，未引入时序推理机制。ChronoEdit 通过两帧视频建模和推理令牌，在架构层面提供了可插拔的物理一致性增强模块。
- **Gemini 2.5 Flash Image**（Google, 2025）和 **GPT-4o**（OpenAI, 2025）作为商业闭源系统，虽然支持多轮对话式编辑，但其内部机制未公开，且在与 ChronoEdit 的比较中受 API 接口速率和版本差异影响，无法实现完全公平的配对测试。ChronoEdit 在 PBench-Edit 物理一致性基准上的表现缩小了开源方法与商业系统之间的差距。

在推理效率方面，ChronoEdit 通过 DMD（分布匹配蒸馏，Yin et al., 2024）将 50 步整流流采样压缩为 8 步学生模型（ChronoEdit-14B-Turbo），实现约 6 倍推理加速（从 30.4 秒降至 5.0 秒，2 块 H100 GPU），同时保持与完整模型相当的编辑质量。这一蒸馏策略使得时间推理的额外开销在部署中变得可接受。

### 适用边界

ChronoEdit 的当前设计适用于以下场景：
- **两帧编辑设置**：输入单张图像和编辑指令，输出单张编辑后图像，涵盖属性编辑、物体增删、姿态变换、场景模拟等任务。
- **依赖预训练视频模型权重**：方法需要大规模 I2V 预训练模型作为初始化（如 Wan2.1-I2V-14B-720P 或 Cosmos-Predict2.5-2B），从零开始训练仍需大量数据和计算资源。
- **中等复杂度的物理交互**：在物体移动、简单场景变换等任务中表现优异，但在极端复杂的长时程交互或多物体精细操作中，可能需要更长的推理步数或更丰富的轨迹规划。

尚未验证的扩展方向包括：连续视频生成、动态 3D 世界仿真、多步骤编辑链中的推理令牌复用等。

### 局限与开放问题

1. **对预训练权重的依赖**：方法的核心优势来源于 I2V 模型的时序先验，若缺乏高质量的视频预训练权重，模型训练收敛速度和最终性能将显著下降。消融实验证实，视频预训练初始化能够显著加快收敛并提高训练稳定性（Appendix C, Figure S2）。

2. **推理步数的自适应调节**：当前时间推理步数 N_r 设为固定值（如 N_r=10，总步数 N=50），消融研究表明该设置在多数场景下与全程推理（N_r=50）性能相当，同时将推理时间从 55.5 秒降至 35.3 秒。然而，如何根据编辑指令的复杂程度动态调整 N_r，以自适应地平衡效率与质量，仍是一个开放问题。

3. **评价体系的局限性**：所有自动指标均使用 GPT-4.1 进行评估，可能引入大语言模型的固有偏好，缺乏全面的人工主观评价。物理一致性的细粒度评估（如碰撞检测、流体力学合理性）尚未纳入现有基准。

4. **蒸馏模型的细节退化风险**：尽管 8 步蒸馏模型在总体质量上与 50 步模型相当，但在少数场景中可能存在细节退化。蒸馏模型的极限推理步数（如 4 步以下）能否保持可靠的物理一致性，有待进一步探索。

5. **泛化能力未知**：方法对于全新物体类别或真实物理交互（如碰撞、流体、柔性体变形）的泛化能力尚未系统评估。当前工作聚焦于两帧编辑，其在完整视频生成或长时间世界状态预测任务中的扩展能力仍属开放问题。

6. **多步骤编辑的推理复用**：在更复杂的多步骤编辑链或交互式编辑场景中，前一阶段的时间推理令牌能否复用规划信息，以减少后续步骤的计算开销，值得深入研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/ChronoEdit_Towards_Temporal_Reasoning_for_Image_Editing_and_World_Simulation.pdf]]
