---
title: "FlashWorld: High-quality 3D Scene Generation within Seconds"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FlashWorld_High_quality_3D_Scene_Generation_within_Seconds.pdf
openreview_forum_id: 2IftRjRB07
aliases:
- FlashWorld
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过交叉模式蒸馏（Cross-mode distillation），将MV-oriented模式的高视觉质量分布迁移至具有内在3D一致性的3D-oriented模式，并辅以跨模式一致性损失（CMC loss）及分布外数据共训练，实现速度与质量的双重提升。"
primary_logic: "利用视频扩散模型的强大先验进行双模式预训练，再通过分布匹配蒸馏（DMD）将教师（MV-oriented）的分布传授给学生（3D-oriented），同时引入跨模式一致性和OOD数据，可同时解决多视图不一致和3D渲染模糊问题，在数秒内生成高质量3D场景。"
claims:
- "交叉模式蒸馏模型（Ours）同时解决了MV-oriented的噪声纹理和3D-oriented的模糊效果，使新视角质量接近输入视角。"
- "在T3Bench-200、DL3DV-200和WorldScore-200上，FlashWorld在大多数质量指标上均优于现有方法，且生成时间仅9秒，远快于基线（6分钟至数小时）。"
- "消融实验表明，移除跨模式一致性损失（w/o CMC）会导致浮动伪像，移除OOD数据会降低泛化能力和文本对齐度。"
- "T3Bench-200 上 Q-Align IQA = 4.12"
---

# FlashWorld: High-quality 3D Scene Generation within Seconds

> [!tip] 核心洞察
> 利用视频扩散模型的强大先验进行双模式预训练，再通过分布匹配蒸馏（DMD）将教师（MV-oriented）的分布传授给学生（3D-oriented），同时引入跨模式一致性和OOD数据，可同时解决多视图不一致和3D渲染模糊问题，在数秒内生成高质量3D场景。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FlashWorld：秒级高质量3D场景生成 |
| 英文题名 | FlashWorld: High-quality 3D Scene Generation within Seconds |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=2IftRjRB07); [GitHub](https://github.com/imlixinyang/FlashWorld) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FlashWorld |
| Dataset | T3Bench-200, DL3DV-200, WorldScore-200 |

> [!tip] 效果简介
> - T3Bench-200 上，Q-Align IQA 为 4.12，对比 2.34 (Prometheus)，变化 +1.78。
> - DL3DV-200 上，Q-Align IQA 为 3.96，对比 2.55 (Prometheus)，变化 +1.41。
> - WorldScore-200 上，Average Score 为 68.72，对比 66.43 (WonderWorld)，变化 +2.29。

## 概述

3D场景生成领域长期面临一个根本性权衡：以多视图生成为导向（MV-oriented）的方法虽能产出较高视觉质量的图像，但因缺乏内在3D约束，导致多视角不一致和重建噪声；而以3D生成为导向（3D-oriented）的方法虽能保持几何一致性，但渲染结果往往模糊，且通常需要额外的精细化后处理步骤，牺牲了生成效率。

FlashWorld针对这一瓶颈，提出了一种**交叉模式蒸馏（Cross-mode Distillation）**范式。其核心思路是：首先基于视频扩散模型的强大先验进行**双模式预训练**，使单一模型同时具备MV-oriented模式的高视觉质量分布和3D-oriented模式的内在3D一致性；随后，通过**分布匹配蒸馏（DMD）**将MV-oriented教师模式的分布迁移至3D-oriented学生模式，并辅以**跨模式一致性损失（CMC loss）**和**分布外（OOD）数据共训练**，从而在数秒内直接生成高质量、多视角一致的3D高斯表示（3DGS），无需任何后处理重建步骤。

实验表明，FlashWorld在T3Bench-200、DL3DV-200和WorldScore-200等多个基准上，在视觉质量、风格一致性和文本对齐度等指标上均优于现有方法，同时生成速度达到约9秒/场景（H20 GPU），相比基线方法（6分钟至数小时）实现了**10–100倍的加速**。消融研究进一步证实，跨模式一致性损失有效抑制了浮动伪像，而OOD数据共训练显著提升了模型的分布外泛化能力。

## 背景与动机

3D场景生成的目标是从图像或文本描述中自动构建可自由探索的沉浸式三维环境。这一任务在虚拟现实、游戏开发和具身智能等领域具有重要应用价值，但其核心挑战在于同时满足**视觉质量**、**三维一致性**和**生成效率**三个相互制约的需求。

### 现有范式的根本性权衡

当前主流方法可归为两类范式，二者之间存在难以调和的根本性权衡：

**多视图导向（MV-oriented）范式**采用两阶段流水线：先生成多张新视角图像，再通过三维重建获得场景表示。代表性方法包括 **CAT3D**（Gao et al., 2024）、**Bolt3D**（Szymanowicz et al., 2025）和 **Wonderland**（Liang et al., 2025）。这类方法受益于图像/视频扩散模型的强大先验，能够产生高视觉质量的渲染结果。然而，由于多视图生成阶段缺乏显式的三维几何约束，各视角之间容易出现**不一致性**，表现为纹理噪声、几何错位和漂浮伪像（Figure 2）。随后的重建步骤虽然试图弥合这些不一致，但本质上是在拟合一个有噪声的多视图信号，难以从根本上消除问题。

**三维导向（3D-oriented）范式**则直接在生成过程中维护三维表示（如3D高斯泼溅），通过可微渲染获得多视图监督。**Director3D**（Li et al., 2024b）等方法采用像素对齐的3DGS加精细化策略。这类方法天然保证三维一致性，但其渲染质量通常较为模糊，缺乏高频细节。为提升质量，往往需要额外的精细化步骤（如逐场景优化），导致生成时间从数分钟延长至数小时，牺牲了效率。

Figure 2 直观展示了这一权衡：MV-oriented 方法（CAT3D、Bolt3D、Wonderland 及本文的 MV-Diff 变体）产生噪声纹理；MV-oriented 蒸馏变体（MV-Dist）进一步加剧了这一问题；而 3D-oriented 扩散变体（3D-Diff）则呈现明显的模糊效果。两种范式各执一端，难以兼顾。

### 效率瓶颈

除质量与一致性的矛盾外，现有方法的生成效率同样构成关键瓶颈。在 T3Bench-200 和 DL3DV-200 基准上，**Prometheus**（Yang et al., 2025）等较快的基线方法仍需约 7 分钟（H100 GPU）才能完成单个场景生成，而迭代式方法如 **WonderJourney**（Yu et al., 2024a）和 **WonderWorld**（Yu et al., 2025）耗时更长。这严重限制了 3D 场景生成在实际交互式应用中的可行性。

### 本文动机

上述分析揭示了一个清晰的突破口：**能否将 MV-oriented 范式的高视觉质量分布迁移至具有内在三维一致性的 3D-oriented 范式，同时避免传统两阶段流水线的效率损失？**

FlashWorld 的核心动机即在于此——通过**交叉模式蒸馏**（Cross-mode Distillation），使 MV-oriented 模式充当教师、3D-oriented 模式充当学生，在统一的扩散框架内实现质量与一致性的双重提升。同时，借助分布匹配蒸馏（DMD）将多步教师模型压缩至少步学生模型，使生成时间从分钟级压缩至秒级（9 秒，H20 GPU），较基线方法加速约 48 倍。此外，通过引入分布外（OOD）数据的共训练策略，增强模型对多样化输入的泛化能力，突破现有数据集覆盖范围的限制。

## 核心创新

FlashWorld 的核心创新在于通过**范式转换**与**交叉模式知识迁移**，系统性破解了现有 3D 场景生成中视觉质量与 3D 一致性的根本性权衡。其创新可归结为三个紧密耦合的层面。

### 1. 范式转换：从 MV-oriented 重建到 3D-oriented 直接生成

现有主流方法遵循“多视图生成 → 3D 重建”的两阶段 MV-oriented 范式（如 **CAT3D**、**Bolt3D**、**Wonderland**），虽能借助扩散先验获得较高的单帧视觉质量，却因缺乏 3D 约束而导致多视图不一致和重建噪声。另一类 3D-oriented 方法（如 **Director3D**）虽保持 3D 一致性，但渲染结果模糊，且常需额外的精细化步骤。

FlashWorld 将生成范式**直接切换为 3D-oriented**：模型在扩散过程中直接输出 3D 高斯表示（3DGS），无需后处理重建步骤。这一转变使得生成结果天然具备 3D 一致性，从架构层面消除了多视图不一致的根源。

### 2. 双模式预训练：在同一模型中融合两种能力

为实现上述范式转换，FlashWorld 设计了**双模式预训练**策略（Figure 3 左侧）。模型基于视频扩散模型（WAN2.2-5B-IT2V）初始化，其 DiT 主干被增强以 3D 注意力块，同时输出两类结果：

- **MV-oriented 模式**：预测多视图去噪潜变量，优化标准扩散损失 $\mathcal{L}_{\mathrm{MV}}$（Eq. 4）；
- **3D-oriented 模式**：从辅助多视图特征解码像素对齐的 3D 高斯参数，并通过可微渲染优化新视角重建损失 $\mathcal{L}_{\mathrm{3D}}$（Eq. 5）。

双模式联合优化使得同一模型同时具备高视觉质量（来自 MV 模式）和内秉 3D 一致性（来自 3D 模式），为后续蒸馏奠定了关键基础。

### 3. 交叉模式蒸馏：将视觉质量迁移至 3D 一致表示

这是 FlashWorld 最具决定性的创新。在交叉模式后训练阶段（Figure 3 右侧），模型以**MV-oriented 模式为教师、3D-oriented 模式为学生**，通过分布匹配蒸馏（DMD2）与 GAN 损失的组合，将教师的高视觉质量分布迁移至学生的 3D 一致表示。这一非对称蒸馏策略使 3D 模式在保持几何一致性的同时，渲染质量逼近输入视角水平（Figure 2）。

为稳定这一跨模式训练，FlashWorld 引入**跨模式一致性损失（CMC Loss）**（Eq. 6），约束 3D 模式渲染结果的潜变量与 MV 模式在同噪声步的预测保持一致。消融实验证实，移除 CMC 会导致场景中出现浮动和重复伪像（Table 3, Figure 7），尽管部分定量指标未显著下降——这说明 CMC 的核心作用在于**抑制 3D 模式训练中的不稳定因素**，而非直接提升渲染保真度。

### 4. OOD 数据共训练：突破分布内数据瓶颈

传统方法仅依赖多视图数据集训练，泛化能力受限于数据覆盖范围。FlashWorld 在蒸馏过程中引入**分布外（OOD）数据共训练**策略：利用单图/文本配随机模拟相机轨迹，仅忽略 GAN 损失，使模型在保持 3D 一致性的同时适应更广泛的场景分布。消融实验表明，移除 OOD 数据会导致文本对齐分数（CLIP Score）显著下降（Table 3），并在语义错位上表现更差（Figure 7）。

### 创新因果链总结

上述创新形成一条清晰的因果链：**双模式预训练**赋予模型两种互补能力 → **交叉模式蒸馏**将视觉质量从 MV 模式迁移至 3D 模式 → **CMC 损失**稳定这一迁移过程 → **OOD 共训练**扩展泛化边界。这一设计使得 FlashWorld 在仅 9 秒内（单张 H20 GPU）生成高质量 3D 场景，速度比 **Prometheus** 等基线快约 48 倍，同时在 T3Bench-200、DL3DV-200 和 WorldScore-200 等基准上取得最优或次优的质量指标（Table 1, Table 2）。

## 整体框架

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_2IftRjRB07/figures/011_Figure_8.jpg]]
*Figure 8: Architecture of the dual-mode multi-view latent diffusion model*

FlashWorld 的生成范式从传统的“多视图生成 → 3D重建”两阶段流水线，转向了直接输出 3D 高斯表示（3DGS）的 3D-oriented 单阶段生成。这一转变的根本动机在于解决现有方法的核心权衡：MV-oriented 方法视觉质量高但多视图不一致，3D-oriented 方法 3D 一致性好但渲染模糊（Figure 2）。FlashWorld 通过交叉模式蒸馏（Cross-mode Distillation）将两种范式的优势融合，其整体流水线由三个关键阶段构成。

### 双模式预训练（Dual-Mode Pre-training）

第一阶段是构建一个能够同时运行于两种模式的多视图潜在扩散模型。模型以视频扩散模型 **WAN2.2-5B-IT2V** 初始化，利用其强大的时序先验和高效 VAE，而非从图像扩散模型冷启动。核心去噪网络是一个增强 3D 注意力块的 Diffusion Transformer（DiT），它同时输出两类结果：

- **MV-oriented 模式**：预测多视图去噪潜变量 $\hat{\mathcal{Z}}_{\mathrm{MV}}$，优化标准扩散重建损失 $\mathcal{L}_{\mathrm{MV}}$（Eq. 4），追求高视觉质量。
- **3D-oriented 模式**：从辅助多视图特征解码像素对齐的 3D 高斯参数 $\mathcal{G}$，并通过可微渲染器 $R$ 在新视角下渲染图像，优化渲染损失 $\mathcal{L}_{\mathrm{3D}}$（Eq. 5），内秉 3D 一致性。

两种模式共享同一 DiT 骨干，仅在输出头和解码路径上分化，使得模型在预训练阶段就同时习得多视图生成能力和 3D 几何感知能力（Figure 3 左侧）。

### 交叉模式蒸馏（Cross-mode Post-training）

第二阶段是后训练蒸馏，这是 FlashWorld 实现速度与质量双重突破的因果开关。其核心逻辑是：以 MV-oriented 模式作为教师（分布 $p_{\mathrm{real}}$），以 3D-oriented 模式作为学生（分布 $p_{\mathrm{fake}}$），通过分布匹配蒸馏（DMD2）将教师的高视觉质量分布迁移至学生，同时保留学生的 3D 一致性。

蒸馏过程的关键组件包括：

- **DMD2 损失**：最小化真实分布与生成分布之间的近似 KL 散度，利用教师和学生的分数函数差异驱动梯度更新（Eq. 3），使 3D-oriented 模式在少步（few-step）采样下也能逼近 MV-oriented 的渲染质量。
- **GAN 损失**：引入对抗训练（Eq. 7），判别器在潜变量空间区分教师输出与学生渲染结果的编码，进一步促进分布对齐。
- **跨模式一致性损失（CMC Loss）**：在蒸馏过程中，对同一噪声步骤下的 3D 模式渲染潜变量与 MV 模式预测潜变量施加 L2 约束（Eq. 6），稳定 3D-oriented 训练，防止模式坍塌。消融实验证实，移除 CMC 损失会导致浮动和重复伪像的出现（Table 3, Figure 7）。

蒸馏后的学生模型仅需 4 步采样即可生成高质量 3D 场景，将单场景生成时间压缩至 9 秒（H20 GPU），相比基线方法（6 分钟至数小时）实现了约 48 倍的加速（Table 1, Table 2）。

### 分布外数据共训练（OOD Co-training）

为提升模型对分布外文本提示和单图输入的泛化能力，FlashWorld 在蒸馏阶段引入了 OOD 共训练策略。具体做法是：利用大规模无标注单图或文本，配合随机模拟的相机轨迹生成训练样本；对于这些 OOD 数据，仅计算 DMD 损失和 CMC 损失，忽略 GAN 损失，以避免判别器对分布外样本的过度惩罚（Algorithm 2）。消融实验表明，移除 OOD 共训练会导致 CLIP Score 等文本对齐指标显著下降（Table 3, Figure 7）。

### 输入输出流总结

整体流水线的输入输出关系如下：

1. **输入**：单张图像或文本提示，可选地附带指定的相机轨迹 $\mathcal{C}$。
2. **双模式 DiT 处理**：输入经 VAE 编码为潜变量，加入噪声后送入增强 3D 注意力的 DiT，同时输出 MV 模式的去噪潜变量和 3D 模式的辅助特征。
3. **3DGS 解码**：3D 模式辅助特征通过 3DGS Decoder 解码为像素对齐的 3D 高斯参数 $\mathcal{G}$。
4. **渲染输出**：在蒸馏后的学生模型中，通过少步扩散采样生成 $\mathcal{G}$，再经可微渲染器 $R$ 在新视角 $\mathcal{C}_{\mathrm{novel}}$ 下渲染出最终的多视图图像。

这一设计使得 FlashWorld 能够以统一模型无缝处理图像到 3D 和文本到 3D 两种任务，无需分别训练（Section 4.2）。同时，由于模型直接输出 3DGS 表示，天然支持自由视角渲染和深度图生成，即便在无显式深度监督的情况下也能学习有意义的几何信息（Figure 9, Figure 10）。

## 核心模块与公式推导

### 3.1 双模式预训练架构

FlashWorld 的核心架构是一个**双模式多视图潜在扩散模型**，其去噪网络以视频扩散模型 **WAN2.2-5B-IT2V** 为初始化基座，并引入 3D 注意力块增强多视图一致性。该网络同时支持两种生成模式：

- **MV-oriented 模式**：直接预测多视图去噪潜变量 $\hat{\mathcal{Z}}_{\mathrm{MV}}$，追求高视觉质量。
- **3D-oriented 模式**：输出辅助多视图特征，经 **3DGS Decoder** 解码为像素对齐的 3D 高斯参数 $\mathcal{G}$，再通过可微渲染生成新视角图像，内秉 3D 一致性。

两种模式共享去噪网络主体，仅在输出头和解码路径上分化。预训练阶段联合优化以下两个目标：

**MV-oriented 损失**（Eq. 4）：
$$\mathcal{L}_{\mathrm{MV}} = \mathbb{E}_{\boldsymbol{\mathcal{X}}, t, \epsilon, y, C} \left[ \left\| \boldsymbol{\mathcal{Z}} - \hat{\mathcal{Z}}_{\mathrm{MV}} \right\|^2 \right]$$

其中 $\boldsymbol{\mathcal{Z}}$ 为原始多视图隐变量，$\hat{\mathcal{Z}}_{\mathrm{MV}}$ 为 MV 模式的去噪估计，$y$ 为文本条件，$C$ 为相机参数。

**3D-oriented 损失**（Eq. 5）：
$$\mathcal{L}_{\mathrm{3D}} = \mathbb{E}_{\mathcal{X}, t, \epsilon, y, \mathcal{C}} \left[ \big\| \mathcal{X}_{\mathrm{novel}} - R(\mathcal{G}, \mathcal{C}_{\mathrm{novel}}) \big\|^2 \right]$$

其中 $\mathcal{X}_{\mathrm{novel}}$ 为新视角真实图像，$R(\cdot)$ 为 3DGS 可微渲染函数，$\mathcal{C}_{\mathrm{novel}}$ 为新视角相机参数。该损失直接约束渲染结果与真实图像的 L2 误差，迫使 3D 解码器学习几何一致性。

### 3.2 交叉模式蒸馏

预训练完成后，FlashWorld 进入**交叉模式后训练**阶段。核心思路是非对称蒸馏：将 MV-oriented 模式作为教师（提供高视觉质量分布），3D-oriented 模式作为学生（提供 3D 一致性结构），通过分布匹配将教师分布迁移至学生。

蒸馏采用 **DMD2** 与 **GAN 损失** 的组合。DMD 的核心梯度形式为（Eq. 3）：
$$\nabla \mathcal{L}_{\mathrm{DMD}} = - \mathbb{E}_{t} \left( \int \left( s_{\mathrm{real}} - s_{\mathrm{fake}} \right) \frac{d G_{\theta}(z)}{d \theta} dz \right)$$

其中 $s_{\mathrm{real}}$ 和 $s_{\mathrm{fake}}$ 分别为教师模型和学生模型在噪声时间步 $t$ 下的分数函数（Eq. 2）：
$$s(x_t, t) = \nabla_{x_t} \log p_t(x_t) = - \frac{x_t - \alpha_t \mu(x_t, t)}{\sigma_t^2}$$

$\mu(x_t, t)$ 为去噪估计，$\alpha_t$ 和 $\sigma_t$ 为噪声调度参数。DMD 通过最小化真实分布与生成分布之间的近似 KL 散度，将多步教师模型蒸馏至少步学生模型。

**跨模式一致性损失（CMC Loss）** 是稳定 3D-oriented 训练的关键正则项（Eq. 6）：
$$\mathcal{L}_{\mathrm{CMC}} = \mathbb{E}_{z, t, \epsilon, y, \mathcal{C}, i} \left[ \lambda \left\| E\left( R\left( G_{\theta, \mathrm{3D}}(\mathcal{Z}_{t_i}, t_i, y, \mathcal{C}), \mathcal{C} \right) \right) - G_{\theta, \mathrm{MV}}(\mathcal{Z}_{t_i}, t_i, y, \mathcal{C}) \right\|^2 \right]$$

该损失约束同一噪声步骤下，3D 模式渲染结果的 VAE 编码潜变量与 MV 模式预测的潜变量一致。$\lambda$ 为加权系数，$E(\cdot)$ 为 VAE 编码器。CMC 损失的因果作用在于：防止 3D-oriented 模式在蒸馏过程中因优化困难而退化，消融实验证实移除该损失会导致浮动和重复伪像（Figure 7, Table 3）。

**GAN 损失**（Eq. 7）进一步促进生成分布与真实分布的对齐：
$$\mathcal{L}_{\mathrm{GAN}} = \min_{D} \max_{G_{\theta}} \mathbb{E}_{x, z, t} \left[ \log D(F(x, t)) - \log\left( D(F(G_{\theta}(z), t)) \right) \right]$$

其中 $F(\cdot, t)$ 为时间步 $t$ 下的特征提取函数，$D$ 为判别器。

### 3.3 分布外数据共训练

为提升模型对未见场景的泛化能力，蒸馏阶段引入**分布外（OOD）数据共训练**策略。利用单图或文本提示，配合随机模拟的相机轨迹生成训练样本。在 OOD 数据上，仅计算 CMC 损失而忽略 GAN 损失，避免判别器对分布外样本的误判干扰蒸馏过程。消融实验表明，移除 OOD 共训练会导致文本对齐分数（CLIP Score）显著下降（Table 3，E vs F）。

### 关键公式汇总

| 公式 | 变量含义 | 作用 |
|------|---------|------|
| $\mathcal{L}_{\mathrm{MV}}$ | $\boldsymbol{\mathcal{Z}}$：多视图隐变量真值；$\hat{\mathcal{Z}}_{\mathrm{MV}}$：MV 模式去噪估计 | 优化多视图潜变量重建 |
| $\mathcal{L}_{\mathrm{3D}}$ | $\mathcal{X}_{\mathrm{novel}}$：新视角真实图像；$R(\mathcal{G}, \mathcal{C}_{\mathrm{novel}})$：3DGS 渲染结果 | 约束渲染图像与真实图像一致 |
| $\nabla \mathcal{L}_{\mathrm{DMD}}$ | $s_{\mathrm{real}}$：教师分数；$s_{\mathrm{fake}}$：学生分数；$G_{\theta}$：学生生成器 | 分布匹配蒸馏，迁移视觉质量 |
| $\mathcal{L}_{\mathrm{CMC}}$ | $E(\cdot)$：VAE 编码器；$G_{\theta, \mathrm{3D}}$：3D 模式输出；$G_{\theta, \mathrm{MV}}$：MV 模式输出 | 跨模式一致性正则，稳定 3D 训练 |
| $\mathcal{L}_{\mathrm{GAN}}$ | $D$：判别器；$F(\cdot, t)$：时间步特征提取 | 对抗训练，增强生成真实感 |

## 实验与分析

### 核心性能：速度与质量的双重突破

FlashWorld 在三个主流基准上均取得领先的生成质量，同时将推理时间压缩至秒级。在 T3Bench-200 文本到 3D 场景基准上，FlashWorld 的 Q-Align IQA 达到 4.12，比次优方法 **Prometheus** (Yang et al., 2025) 的 2.34 高出 1.78（Table 1）。在 DL3DV-200 基准上，同样以 3.96 对 2.55 的 Q-Align IQA 大幅领先。在 WorldScore-200 基准上，FlashWorld 以 68.72 的平均分超越所有对比方法，其中风格一致性（Style Consistency）达到 81.52，比 **WonderWorld** (Yu et al., 2025) 的 75.92 高出 5.60 分（Table 2）。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_2IftRjRB07/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison on text-to-3D scene generation. Cell background colors indicate the method is the best , second best , or third best on this metric*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_2IftRjRB07/figures/008_Figure_6.jpg]]
*Figure 6: 3D scene generation results of different methods on WorldScore benchmark. Table 2: Quantitative comparison on WorldScore benchmark. Note that the time cost of the baselines is tested on 1× H100 GPU, while our time cost is tested on 1× H20 GPU*

速度优势更为显著：FlashWorld 在单张 H20 GPU 上每场景仅需 9 秒，而 **Prometheus** 在 H100 GPU 上需 7 分 15 秒，实际加速比约 48 倍；其他迭代式方法如 **WonderJourney** (Yu et al., 2024a) 和 **LucidDreamer** (Chung et al., 2023) 则需数小时（Table 1, Table 2）。需注意，基线方法的时间在 H100 上测量，FlashWorld 在 H20 上测量，因此实际相对加速比可能更大。

定性结果（Figure 4, Figure 5）显示，FlashWorld 能恢复细粒度结构（如叶片、铁栅栏、触手），而 MV-oriented 方法（CAT3D、Bolt3D、Wonderland）普遍存在噪声纹理，3D-oriented 方法则产生模糊效果。Figure 2 直观对比了这些模式：MV-oriented 扩散（w/ MV-Diff）和蒸馏（w/ MV-Dist）导致严重的多视图不一致与噪声；3D-oriented 扩散（w/ 3D-Diff）产生明显模糊；交叉模式蒸馏模型（Ours）同时解决了这两个问题，使新视角质量接近输入视角。

### 消融实验：交叉模式一致性与 OOD 数据的关键作用

Table 3 和 Figure 7 的消融实验揭示了各组件的贡献机制：

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_2IftRjRB07/figures/009_Table_3.jpg]]
*Table 3: Quantitative ablation studies. The letters A–F correspond to different model variants: (A) w/ MV-Diff, (B) w/ 3D-Diff, (C) w/ MV-Dist, (D) w/o CMC, (E) w/o OOD, and (F) Full model*

- **移除跨模式一致性损失 (w/o CMC)**：定量指标上，w/o CMC 模型（变体 D）在部分指标上甚至与完整模型（变体 F）持平或略优，但定性结果暴露了严重缺陷——生成场景中出现浮动和重复的伪像（Figure 7 顶部：钟表场景出现多余钟面；底部：向日葵场景出现重复花朵）。这表明 CMC 损失的核心作用不在于提升像素级质量，而在于稳定 3D-oriented 模式的训练，消除跨模式不一致导致的结构性伪像。

- **移除分布外数据共训练 (w/o OOD)**：变体 E 在 WorldScore-200 上的 CLIP Score 从 29.13 降至更低水平，文本对齐能力显著下降（Table 3）。Figure 7 的定性结果进一步显示，w/o OOD 模型更易出现语义错位。OOD 数据（单图/文本配随机相机轨迹）在蒸馏过程中仅忽略 GAN 损失，其核心作用是扩展模型的分布外泛化能力，而非直接提升分布内质量。

- **单一模式基线**：仅使用 MV-oriented 扩散（变体 A）或蒸馏（变体 C）导致严重的多视图不一致和噪声纹理；仅使用 3D-oriented 扩散（变体 B）产生明显模糊。这验证了单一模式无法同时兼顾视觉质量与 3D 一致性，交叉模式蒸馏是打破这一瓶颈的关键机制。

### 失败模式与局限性

尽管 FlashWorld 在速度和主流指标上表现优异，仍存在以下已知局限：

1. **细粒度几何与特殊材质**：模型难以准确生成镜面反射和铰接式物体，这源于仅依赖 RGB 监督而缺乏显式深度先验的架构设计。Figure 9 和 Figure 10 显示，尽管模型在无深度监督下能学习有意义的深度信息，但深度精度仍不及显式深度引导的方法。

2. **场景多样性与规模**：生成场景的多样性和规模受限于现有数据集的覆盖范围，尽管视图数量有所增加。OOD 共训练策略部分缓解了这一问题，但未能根本解决。

3. **评估公平性**：WorldScore 基准上，作者使用随机采样帧（而非仅锚定帧）重新计算各指标，以避免仅评估最优视图的偏差。文本到 3D 场景的定量比较中，由于所有方法均输出 3D 高斯表示，与相机控制或 3D 一致性相关的指标未纳入评估——这意味着 FlashWorld 的 3D 一致性优势可能被低估。

### 关键图表结论

- **Table 1**：FlashWorld 在 T3Bench-200 和 DL3DV-200 上以 9 秒/场景的速度取得 Q-Align IQA 最优，比次优方法快约 48 倍。
- **Table 2**：在 WorldScore-200 上，FlashWorld 以 68.72 平均分和 9 秒推理时间领先所有方法；风格一致性优势最大（+5.60）。
- **Table 3**：CMC 损失的定量贡献不显著但定性关键（消除浮动伪像）；OOD 数据对文本对齐（CLIP Score）贡献明确。
- **Figure 7**：定性消融直观展示了 w/o CMC 的重复伪像和 w/o OOD 的语义错位，是理解各组件作用的核心证据。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_2IftRjRB07/figures/001_Figure_1.jpg]]
*Figure 1: FlashWorld enables fast and high-quality 3D scene generation across diverse scenes*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_2IftRjRB07/figures/007_Figure.jpg]]
*Figure: Ours WonderWorld LucidDreamer WonderJourney*

## 方法谱系与知识库定位

### 1. 范式定位：从两阶段重建到直接3D生成

FlashWorld 在3D场景生成的方法谱系中，代表了一次根本性的范式转换。现有方法可清晰划分为两大阵营：

**MV-oriented 范式（多视图导向）** 遵循“先多视图生成，后3D重建”的两阶段流水线。代表性工作包括 **CAT3D**（Gao et al., 2024）、**Bolt3D**（Szymanowicz et al., 2025）、**Wonderland**（Liang et al., 2025）、**Prometheus**（Yang et al., 2025）、**SplatFlow**（Go et al., 2025a）和 **VideoRFSplat**（Go et al., 2025a）。这些方法利用扩散模型生成多视图图像，再通过前馈或优化重建获得3D表示。其核心瓶颈在于：多视图生成阶段缺乏3D约束，导致跨视角不一致，最终在3D表示中表现为噪声纹理（Figure 2 清晰展示了 CAT3D、Bolt3D、Wonderland 的噪声伪像）。

**3D-oriented 范式（3D导向）** 则直接在生成过程中嵌入3D表示，如 **Director3D**（Li et al., 2024b）采用像素对齐的3DGS加精细化步骤。这类方法虽然内秉3D一致性，但渲染质量模糊，且往往需要额外的精细化步骤而牺牲效率。

FlashWorld 的关键创新在于**交叉模式蒸馏（Cross-mode Distillation）**：在双模式预训练后，将 MV-oriented 模式作为教师、3D-oriented 模式作为学生，通过 DMD2 和 GAN 损失将高视觉质量分布迁移至具有3D一致性的生成器中。这一策略同时解决了 MV-oriented 的噪声纹理和 3D-oriented 的模糊效果（Figure 2, Ours vs. Ours w/ MV-Diff vs. Ours w/ 3D-Diff）。

### 2. 与迭代式场景生成的关系

另一条技术路线是**迭代式3D场景生成**，如 **WonderJourney**（Yu et al., 2024a）、**LucidDreamer**（Chung et al., 2023）和 **WonderWorld**（Yu et al., 2025）。这些方法通过逐步扩展场景边界来构建大规模3D世界。FlashWorld 与它们形成互补而非直接竞争：FlashWorld 聚焦于单次前馈生成的高质量与高速度，而迭代式方法在场景规模扩展上更具灵活性。在 WorldScore-200 基准上，FlashWorld 以 68.72 的平均分超越 WonderWorld 的 66.43，且生成时间仅 9 秒（Table 2）。

### 3. 知识库定位：视频扩散先验与蒸馏技术的融合

FlashWorld 的知识继承链包含三个层次：

1. **视频扩散模型初始化**：采用 **WAN2.2-5B-IT2V**（Wan et al., 2025）作为基础网络，利用其强大的时空先验和多视图一致性，而非传统的图像扩散模型（如 Stable Diffusion）。这为双模式预训练提供了更丰富的先验知识。

2. **分布匹配蒸馏（DMD）**：继承自 DMD2 的蒸馏框架，通过最小化真实分布与生成分布的近似 KL 散度，将多步教师模型压缩至少步学生模型。FlashWorld 的创新在于将 DMD 扩展到**跨模式蒸馏**场景——教师和学生来自同一网络的不同运行模式。

3. **3D Gaussian Splatting 解码器**：在 DiT 架构中嵌入 3DGS 解码器，从辅助多视图特征直接解码像素对齐的高斯参数，使 3D-oriented 模式能够在扩散去噪过程中实时渲染新视角。

### 4. 适用边界与失效模式

**适用场景**：
- 图像/文本到3D场景的快速生成（秒级）
- 需要3D一致性的多视角渲染
- 单 GPU 部署场景（H20 即可运行）

**已知失效模式**（基于论文声明的局限性和消融实验）：
- **细粒度几何细节**：模型仅依赖 RGB 监督，未利用深度先验，难以准确生成精细几何结构、镜面反射和铰接式物体（Section 5）。
- **分布外泛化**：移除 OOD 数据共训练后，模型对训练集未覆盖的文本/图像输入的语义对齐能力显著下降（Table 3, w/o OOD: CLIP Score 从 29.13 降至更低）。
- **浮动伪像**：移除跨模式一致性损失（w/o CMC）会导致场景中出现浮动和重复的伪像，尽管部分定量指标未显著下降（Figure 7, Table 3 D vs F）。
- **场景多样性**：受限于现有多视图数据集的覆盖范围，生成场景的多样性仍有上限。

### 5. 开放问题

1. **深度先验的整合**：如何有效引入深度先验和3D感知结构信息（如 Plücker 坐标），以提升几何精度和对镜面、铰接物体的处理能力？Figure 9 显示模型在无显式深度监督下已能学习有意义的深度信息，暗示进一步引入深度先验可能带来显著增益。

2. **动态4D场景扩展**：当前框架能否扩展到动态4D场景生成任务，利用视频扩散模型的时序先验？论文明确将此列为未来工作方向。

3. **数据依赖缓解**：如何减少对大规模多视图数据集的依赖，采用更高效的自监督或弱监督策略？当前 OOD 共训练策略已初步探索了单图/文本数据的利用，但仍需多视图数据作为核心训练信号。

4. **与迭代式方法的融合**：能否将 FlashWorld 的快速生成能力与迭代式方法的场景扩展能力结合，实现既快又大的3D世界构建？

## 原文 PDF

![[paperPDFs/ICLR_2026/FlashWorld_High_quality_3D_Scene_Generation_within_Seconds.pdf]]
