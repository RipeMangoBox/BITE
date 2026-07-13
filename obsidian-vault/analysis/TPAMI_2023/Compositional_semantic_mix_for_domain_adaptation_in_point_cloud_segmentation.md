---
title: "Compositional semantic mix for domain adaptation in point cloud segmentation"
type: paper
paper_level: A
venue: TPAMI
year: 2023
pdf_ref: paperPDFs/TPAMI_2023/Compositional_semantic_mix_for_domain_adaptation_in_point_cloud_segmentation.pdf
code_link: https://github.com/saltoricristiano/cosmix-uda
project_link: https://github.com/saltoricristiano/cosmix-uda
aliases:
- CCSMICUCSV
- CSMDAPCS
tags:
- TPAMI_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过语义引导的组合式点云混合（compositional semantic mixing）——将源域和目标域中基于语义选择的点补丁（patch）跨域拼接，并结合教师-学生EMA自训练——来构造中间域，从而逐步减小域差距。"
primary_logic: "直接在稀疏的3D点云上进行语义级样本混合，比单纯对齐特征空间或2D投影后的混合更有效地保留了结构信息；同时双分支对称混合与置信度门控的伪标签选择能够平衡域迁移过程，防止噪声伪标签导致的偏差。"
claims:
- "CoSMix在SynLiDAR→SemanticPOSS无监督域适应（UDA）中达到32.2 mIoU，比ST-PCT高+3.3 mIoU，比Source-only高+8.4 mIoU。"
- "CoSMix在SemanticKITTI→nuScenes UDA中达到46.2 mIoU，优于所有对比方法。"
- "CoSMix在半监督域适应（SSDA）场景下显著提升：SynLiDAR→SemanticPOSS SSDA达到41.0 mIoU，比APE-PCT高+9.8 mIoU；SemanticKITTI→nuScenes SSDA达到48.9 mIoU。"
- "消融实验证实双分支混合、局部/全局增强、EMA教师更新和长尾加权采样每个组件均带来超过1 mIoU的增益（汇总后从31.6提升至40.4）。"
---

# Compositional semantic mix for domain adaptation in point cloud segmentation

> [!tip] 核心洞察
> 直接在稀疏的3D点云上进行语义级样本混合，比单纯对齐特征空间或2D投影后的混合更有效地保留了结构信息；同时双分支对称混合与置信度门控的伪标签选择能够平衡域迁移过程，防止噪声伪标签导致的偏差。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向点云分割领域自适应的组合语义混合 |
| 英文题名 | Compositional semantic mix for domain adaptation in point cloud segmentation |
| 会议/期刊 | TPAMI 2023 |
| Links | [paper](https://arxiv.org/abs/2308.14619) · [GitHub](https://github.com/saltoricristiano/cosmix-uda) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CoSMix (Compositional Semantic Mix, including CoSMix-UDA and CoSMix-SSDA variants) |
| Dataset | SynLiDAR → SemanticPOSS (UDA), SynLiDAR → SemanticKITTI (UDA), SemanticKITTI → nuScenes (UDA), SynLiDAR → SemanticPOSS (SSDA) |

> [!tip] 效果简介
> - SynLiDAR → SemanticPOSS (UDA) 上，mIoU 为 32.2，对比 28.9 (ST-PCT)，变化 +3.3。
> - SynLiDAR → SemanticKITTI (UDA) 上，mIoU 为 40.4。
> - SemanticKITTI → nuScenes (UDA) 上，mIoU 为 46.2，对比 40.1 (Source*)，变化 +6.1。

## 概要

### 问题瓶颈

3D点云语义分割面临一个核心瓶颈：在合成数据（如SynLiDAR）或某个真实数据集上训练的深度模型，直接部署到另一个真实场景时性能急剧下降。这种域偏移源于传感器噪声、环境布局差异和点云稀疏性变化等多重因素，使得仅用源域监督的模型难以泛化到目标域。现有域适应方法或依赖对抗训练进行特征对齐，或通过自训练逐步修正伪标签，但它们在处理3D点云的结构稀疏性和几何不连续性时，往往丢失关键的空间上下文信息。

### 核心方法

本文提出**CoSMix（Compositional Semantic Mix）**，一种基于组合语义混合的域适应框架，覆盖无监督域适应（CoSMix-UDA）和半监督域适应（CoSMix-SSDA）两种设定。其核心洞察是：直接在稀疏3D点云上进行语义引导的跨域样本混合，比单纯对齐特征空间或2D投影后混合更有效地保留结构信息。

方法的关键机制包括：

- **双分支对称混合**：同时构建源→目标（s→t）和目标→源（t→s）两个混合分支，将基于语义选择的点补丁（patch）跨域拼接，生成中间域点云，逐步桥接域差距。
- **语义选择与重加权**：源域补丁通过反向频率加权采样（$f$函数）选取，缓解长尾类被忽略的问题；目标域补丁由教师网络生成的伪标签经置信度阈值$\zeta$筛选（$g$函数），抑制噪声传播。
- **组合式增强**：先对语义补丁施加局部随机增强$h$，跨域拼接后再施加全局增强$r$，双重扰动提升混合点云的多样性和鲁棒性。
- **教师-学生EMA自训练**：教师网络参数$\theta'$通过指数移动平均（$\beta=0.99$）从学生网络更新，持续改进伪标签质量，形成正向循环。

所有方法统一使用**MinkowskiNet**作为稀疏体素卷积骨干网络，确保比较的公平性。

### 主要结果

CoSMix在多个合成→真实和真实→真实的LiDAR分割基准上取得一致的领先性能：

- **SynLiDAR → SemanticPOSS（UDA）**：达到32.2 mIoU，比ST-PCT（Xiao et al., AAAI 2022）高+3.3 mIoU，比Source-only高+8.4 mIoU。
- **SemanticKITTI → nuScenes（UDA）**：达到46.2 mIoU，比Source*高+6.1 mIoU。
- **半监督场景下增益更为显著**：SynLiDAR → SemanticPOSS SSDA达到41.0 mIoU，比APE-PCT（Xiao et al., AAAI 2022）高+9.8 mIoU；SemanticKITTI → nuScenes SSDA达到48.9 mIoU。

消融实验证实，双分支混合、局部/全局增强、EMA教师更新和长尾加权采样每个组件均带来超过1 mIoU的独立贡献，验证了各模块的必要性。

### 方法定位

CoSMix属于基于混合（mixup-based）和自训练（self-training）相结合的域适应范式。与通用点云混合策略（如Mix3D、PointCutMix、PolarMix）相比，其语义引导的双分支组合混合在域适应场景下具有明显优势（38.9 vs. 31.6/30.4/28.5 mIoU）。该方法可灵活适配UDA和SSDA两种设定，但对伪标签质量存在较强依赖——源域预训练不足时性能受限，且在类分布差异极大的跨域场景（如SynLiDAR→nuScenes）中提升幅度有限。

### 3D点云语义分割中的域偏移瓶颈

3D点云语义分割是自动驾驶、机器人导航等场景的核心感知任务。然而，训练高性能分割模型通常依赖大规模密集标注的点云数据，其获取成本极高。一个自然的替代方案是在合成数据（如SynLiDAR）或已有标注的真实数据上训练模型，再将其部署到新的真实场景。但这一策略面临严峻挑战：**源域与目标域之间存在显著的域偏移（domain shift）**，包括传感器噪声特性不同、环境外观差异、点云稀疏性模式不一致等。仅用源域数据训练的深度模型在目标域上泛化能力严重不足，表现为预测碎片化、类别混淆、远距离目标丢失等典型失效模式。

以SynLiDAR → SemanticPOSS的无监督域适应（UDA）任务为例，Source-only模型的mIoU仅为23.8，而目标域监督训练的上限可达47.5（Table 2），两者之间存在超过23 mIoU的巨大性能鸿沟。这一瓶颈直接驱动了对3D点云域适应方法的研究。

### 现有方法的缺口

当前3D点云分割域适应方法可归纳为几类策略（Table 1）：对抗学习（如**ADDA**，Tzeng et al., CVPR 2017）、熵最小化（如**EntMin**，Vu et al., CVPR 2019）、自训练（如**ST**，Zou et al., ICCV 2019）、以及专门针对LiDAR点云的**PCT**与**ST-PCT**（Xiao et al., AAAI 2022）等。这些方法的核心思路是在特征空间或输出空间进行对齐，而非直接在数据层面弥合域差距。

然而，在稀疏、非结构化的3D点云上，**单纯的特征对齐容易丢失几何结构信息**，而将点云投影到2D后再混合（如部分图像域适应方法的延伸）则引入了投影失真和信息损失。此外，现有方法在伪标签质量控制和域间数据混合策略上仍显粗糙：要么使用固定阈值筛选伪标签，要么缺乏系统性的跨域样本合成机制。这导致在语义差距较大的域适应任务中，性能提升有限且不稳定。

### 本文动机：从语义级数据混合到组合式域适应

本文的核心动机在于：**直接在3D点云层面进行语义引导的样本混合，可能比特征空间对齐更有效地保留结构信息并缩小域差距**。基于这一洞察，本文提出**CoSMix（Compositional Semantic Mix）**框架，其设计遵循以下原则：

1. **语义选择而非盲目混合**：利用源域真实标签和目标域伪标签（或少量人工标注）选择具有语义意义的点补丁（patch），确保混合后的点云保持语义一致性。
2. **双分支对称混合**：同时构建源域补丁混入目标点云（s→t）和目标域补丁混入源点云（t→s）两个方向的中间域，使模型从双向域迁移中学习域不变特征。
3. **组合式增强与教师-学生协同**：先对语义补丁施加局部随机增强，再跨域拼接，最后对混合点云施加全局增强，形成层次化数据增强；同时通过指数移动平均（EMA）更新的教师网络持续提升伪标签质量，形成正向循环。

该方法同时覆盖无监督域适应（UDA）和半监督域适应（SSDA）两种设定，在合成到真实（SynLiDAR → SemanticPOSS/SemanticKITTI/nuScenes）和真实到真实（SemanticKITTI → nuScenes）等多个迁移场景中验证了其有效性。

## 核心方法与创新机理

### 1. 语义引导的组合式点云跨域混合

CoSMix的核心创新在于将域适应从特征空间或2D投影的层面直接推进到稀疏3D点云的语义级样本混合。与以往方法（如**PCT** (Xiao et al., AAAI 2022) 仅依赖自训练、或通用点云混合策略Mix3D/PointCutMix仅做随机的几何拼接）不同，CoSMix设计了一套**语义选择-局部增强-跨域拼接-全局增强**的组合式混合管线，构造出语义上有意义的中间域点云。

具体而言，该方法的关键changed slot体现在：

- **双分支对称混合架构**：同时构建 $t \to s$ 分支（将目标域语义补丁混入源点云）和 $s \to t$ 分支（将源域语义补丁混入目标点云），形成两个互补的中间域。消融实验证实，仅使用单分支时性能从40.4 mIoU骤降至31.6 mIoU，双分支设计是方法有效性的核心支柱（Table 9）。

- **语义选择函数 $f$ 与 $g$**：源域补丁通过基于类分布的反向频率加权采样函数 $f$ 进行选择（$\tilde{\mathcal{V}}^{s} = f(\mathcal{V}^{s}, 1 - P_{\mathcal{V}}^{s}, \alpha)$），使长尾类以更高概率被选中；目标域补丁则通过置信度门控函数 $g$ 筛选教师网络的高置信度伪标签（$\tilde{\mathcal{V}}_{\mathsf{U}}^{t} = g(\Phi_{\theta^{\prime}}(\mathcal{X}_{\mathsf{U}}^{t}), \zeta)$）。这一机制取代了baseline中简单的全量伪标签使用或固定阈值策略，有效抑制了噪声伪标签对域迁移的干扰。

- **层次化增强策略**：先对选中的语义补丁独立施加局部随机增强 $h$，再与另一域点云拼接，最后对整个混合点云施加全局随机增强 $r$（Eq.5-8）。消融表明，局部增强和全局增强分别贡献约1.5 mIoU和2 mIoU的增益（Table 9），这验证了“补丁级独立性增强+全局一致性增强”的组合设计对域泛化能力的提升作用。

### 2. 在线EMA教师-学生自训练范式

CoSMix将伪标签生成从一个离线或静态的过程转变为一个**在线持续进化**的闭环系统。与**ST-PCT** (Xiao et al., AAAI 2022) 等baseline使用的固定模型或离线预训练教师不同，CoSMix采用指数移动平均（EMA）在线更新教师网络参数 $\theta'$：

$$\theta_{i}^{\prime} = \beta \theta_{i-1}^{\prime} + (1 - \beta) \theta$$

其中 $\beta=0.99$，每 $\gamma$ 步执行一次更新。这一设计使得教师网络能够持续从学生网络的学习进展中受益，产出质量逐步提升的伪标签，进而反哺学生网络的训练。消融实验显示，EMA教师更新单独贡献超过1 mIoU的提升（Table 9），证实了在线自训练循环相较静态伪标签策略的显著优势。

### 3. 统一的UDA/SSDA框架设计

CoSMix通过引入一个简洁的指示函数 $\delta(\mathcal{T}_{\mathsf{L}})$ 和额外的有监督目标补丁选择分支，将无监督域适应（UDA）和半监督域适应（SSDA）统一到同一框架下。当有少量目标域标注数据可用时，系统自动激活中间分支，将人工标注的目标补丁 $\tilde{\mathcal{V}}_{\mathsf{L}}^{t}$ 也纳入混合过程（Eq.7）。这一设计使得CoSMix-SSDA在SynLiDAR→SemanticPOSS上达到41.0 mIoU，比**APE-PCT** (Kim and Kim, ECCV 2020; Xiao et al., AAAI 2022) 高出+9.8 mIoU（Table 5），展现出对稀疏标注信息的高效利用能力。

### 4. 与通用混合策略的本质区别

CoSMix的组合式语义混合在机制上显著区别于通用点云混合方法。Fig. 5a的对比实验表明，在相同实验设置下，CoSMix的双分支混合达到38.9 mIoU，而Mix3D、PointCutMix、PolarMix分别仅为31.6、30.4和28.5 mIoU。这种差距的根本原因在于：通用混合方法缺乏语义引导的补丁选择，混合操作是“盲目”的——它们可能在混合过程中破坏关键的几何结构信息或引入语义不一致的跨域拼接；而CoSMix通过 $f$ 和 $g$ 函数确保混合的补丁在语义上是可迁移的，并通过层次化增强保留了点云的局部结构完整性。

CoSMix 的核心设计围绕一个**双分支对称的教师‑学生架构**展开，目标是在不引入额外特征对齐模块的前提下，通过**语义引导的组合式点云混合**来逐步缩小源域与目标域之间的分布偏移。整个 pipeline 可分解为四个紧密耦合的模块：语义选择、组合式混合、学生网络训练以及教师网络在线更新。

### 1. 双分支对称混合范式

CoSMix 同时构建两条对称的混合路径：

- **t → s 分支**：将目标域中经伪标签筛选的语义补丁（patch）拼接到源域点云中，生成混合点云 $\mathcal{X}^{t \to s}$。
- **s → t 分支**：将源域中基于真实标签选择的语义补丁拼接到目标域点云中，生成混合点云 $\mathcal{X}^{s \to t}$。

这两条分支共享同一个学生网络 $\Phi_\theta$，并通过总损失 $\mathcal{L}_{tot} = \mathcal{L}_{s \to t} + \mathcal{L}_{t \to s}$ 进行联合优化。双分支设计的核心动机在于**双向域混合能够构造出更具多样性的中间域**，避免单方向混合导致的域偏差累积。消融实验证实，仅使用单分支时 mIoU 从 40.4 骤降至 31.6（Table 9），表明对称混合是性能的关键瓶颈。

在**半监督域适应（SSDA）**设定下，框架在两条分支中均额外引入少量有标注目标域补丁：t → s 分支将有标注目标补丁混入源点云，s → t 分支则将其混入无标注目标点云。这一扩展通过指示函数 $\delta(\mathcal{T}_{\mathsf{L}})$ 控制，当有监督目标集非空时自动激活第三条“中间分支”（Fig. 1 灰色线条）。

### 2. 语义选择模块（Semantic Selection）

语义选择是混合质量的第一道关口，由两个核心函数构成：

- **源域补丁选择函数 $f$**：基于源类分布的反向频率加权采样，长尾类别被选中的概率更高。公式为 $\tilde{\mathcal{V}}^{s} = f(\mathcal{V}^{s}, 1 - P_{\mathcal{V}}^{s}, \alpha)$，其中 $\alpha$ 控制采样强度。
- **目标域伪标签选择函数 $g$**：利用教师网络 $\Phi_{\theta'}$ 对无标注目标点云 $\mathcal{X}_{\mathsf{U}}^{t}$ 进行预测，并通过置信度阈值 $\zeta$ 筛选可靠的伪标签：$\tilde{\mathcal{V}}_{\mathsf{U}}^{t} = g(\Phi_{\theta'}(\mathcal{X}_{\mathsf{U}}^{t}), \zeta)$。

在 SSDA 设定下，有标注目标补丁的选择同样通过 $f$ 函数完成，但使用源类分布的互补概率 $1 - P_{\mathcal{V}}^{s}$ 和独立超参数 $\mu$ 进行加权。置信度阈值 $\zeta$ 的取值需要在伪标签正确性与对象完整性之间取得平衡——实验表明最优值约为 0.85（Fig. 5b）。

### 3. 组合式混合模块（Compositional Mix）

该模块将语义选择得到的补丁进行**三级级联操作**，以生成具有丰富结构变化的混合点云：

1. **局部随机增强 $h$**：对每个被选中的语义补丁独立施加随机扰动（如小幅旋转、抖动），增强补丁内部的局部多样性。
2. **拼接（Concatenation）**：将局部增强后的补丁与另一域的点云进行空间拼接。以 s → t 分支为例，混合点云 $\mathcal{X}^{s \to t}$ 由增强后的源补丁 $h(\tilde{\mathcal{X}}^{s})$、可选的有标注目标补丁 $h(\tilde{\mathcal{X}}_{\mathrm{L}}^{t})$ 以及无标注目标点云 $\mathcal{X}_{\mathrm{U}}^{t}$ 拼接而成。
3. **全局随机增强 $r$**：对拼接后的完整混合点云施加全局变换（如旋转、缩放、平移），进一步增强跨域泛化能力。

这种“先局部增强、再跨域拼接、最后全局增强”的组合策略，相较于直接在完整点云上施加混合（如 Mix3D、PointCutMix）或仅在 2D 投影空间混合，能够更有效地保留 3D 结构信息。消融实验表明，全局增强和局部增强分别贡献约 2 mIoU 和 1.5 mIoU 的提升（Table 9）。

### 4. 教师‑学生在线学习范式

CoSMix 采用**指数移动平均（EMA）**机制在线更新教师网络参数，而非使用离线预训练的固定模型：

$$\theta_{i}^{\prime} = \beta \theta_{i-1}^{\prime} + (1 - \beta) \theta$$

其中 $\beta = 0.99$，每 $\gamma$ 步执行一次更新。教师网络 $\Phi_{\theta'}$ 的唯一职责是为目标域生成伪标签，学生网络 $\Phi_\theta$ 则接收混合点云进行分割训练。这种设计形成了一个**自增强闭环**：随着学生网络在混合数据上性能提升，教师网络产生的伪标签质量也随之改善，进而为下一轮语义选择提供更可靠的监督信号。消融实验显示，EMA 教师更新单独贡献超过 1 mIoU（Table 9）。

### 5. 骨干网络与统一性约束

为确保公平比较，所有方法（包括 CoSMix 及全部复现基线）统一使用 **MinkowskiNet ** 作为稀疏体素卷积骨干网络。这一约束消除了架构差异对域适应性能评估的干扰，使得性能增益可明确归因于混合策略本身。

### 6. 关键限制与适用边界

CoSMix 的性能高度依赖**源域预训练模型的初始质量**：若源域热身不足，教师网络产生的伪标签噪声会通过语义选择模块放大，限制最终适应效果。此外，该框架要求目标域存在一定规模的无监督数据，无法直接处理完全无目标数据的源自由适应（source‑free）场景。在域差距极大的场景（如 SynLiDAR → nuScenes，仅 27.3 mIoU），语义混合策略的增益显著减弱，表明当类分布和传感器特性差异过大时，仅靠点云层面的混合难以弥合深层语义鸿沟。

CoSMix 的域适应能力来源于三个紧密耦合的核心模块：语义选择、组合式混合，以及教师-学生自训练范式。以下逐一解析各模块的设计逻辑与关键公式。

### 语义选择：基于分布感知的补丁采样

语义选择模块的目标是从源域和目标域点云中提取出最适合跨域混合的“语义补丁”（semantic patches），而非随机采样。该模块由两个函数构成：

**源域补丁选择函数 $f$** 采用反向频率加权策略，以缓解源域中的长尾类别在混合过程中被淹没的问题。其形式为：

$$\tilde{\mathcal{V}}^{s} = f(\mathcal{V}^{s}, 1 - P_{\mathcal{V}}^{s}, \alpha)$$

其中 $\mathcal{V}^{s}$ 为源域语义标签集合，$P_{\mathcal{V}}^{s}$ 为源域类别的经验分布，$\alpha$ 为控制采样温度的超参数。该函数以 $1 - P_{\mathcal{V}}^{s}$ 作为采样权重，使得长尾类别（出现频率低）被选中的概率更高，从而在混合点云中保持类别多样性。

**目标域伪标签选择函数 $g$** 则基于置信度门控机制筛选可靠的伪标签：

$$\tilde{\mathcal{V}}_{\mathsf{U}}^{t} = g(\Phi_{\theta^{\prime}}(\mathcal{X}_{\mathsf{U}}^{t}), \zeta)$$

其中 $\Phi_{\theta^{\prime}}$ 为教师网络，$\mathcal{X}_{\mathsf{U}}^{t}$ 为无监督目标域点云，$\zeta$ 为置信度阈值。只有教师网络预测置信度高于 $\zeta$ 的语义区域才会被选为有效伪标签补丁。消融实验表明，$\zeta$ 的最优值约为 0.85，此时在伪标签正确性与对象完整性之间取得最佳平衡（见 Fig. 5b）。

在 SSDA 设定下，有监督目标补丁的选择同样采用 $f$ 函数，但其采样权重基于源域类分布的反向频率，并通过超参数 $\mu$ 调节：

$$\tilde{\mathcal{V}}_{\mathsf{L}}^{t} = f(\mathcal{V}_{\mathsf{L}}^{t}, 1 - P_{\mathcal{V}}^{s}, \mu)$$

### 组合式混合：局部增强-拼接-全局增强的三阶段操作

组合式混合（compositional mix）是 CoSMix 区别于简单点云拼接或 2D 混合方法的核心创新。该模块由三个连续操作构成，在保留 3D 结构信息的同时构造中间域。

**第一阶段：局部随机增强 $h$。** 对选中的语义补丁独立施加随机扰动，包括随机旋转、缩放和平移。这一步使补丁在拼接到另一域时具有更丰富的几何变化，增强模型的鲁棒性。

**第二阶段：跨域拼接。** 将增强后的补丁拼接到另一域的点云上，形成两个对称的混合分支：

- **$t \to s$ 分支**：目标补丁混入源点云，生成 $\mathcal{X}^{t \to s}$；
- **$s \to t$ 分支**：源补丁混入目标点云，生成 $\mathcal{X}^{s \to t}$。

以 $s \to t$ 分支为例，其构造方式为：

$$\mathcal{X}^{s \to t} = \begin{cases} r(h(\tilde{\mathcal{X}}^{s}) \cup h(\tilde{\mathcal{X}}_{\mathsf{L}}^{t}) \cup \mathcal{X}_{\mathsf{U}}^{t}) & \text{if } \delta(\mathcal{T}_{\mathsf{L}}) = 1 \\ r(h(\tilde{\mathcal{X}}^{s}) \cup \mathcal{X}_{\mathsf{U}}^{t}) & \text{otherwise} \end{cases}$$

其中 $\delta(\mathcal{T}_{\mathsf{L}})$ 为指示函数，当存在有监督目标标签集合 $\mathcal{T}_{\mathsf{L}}$ 时取 1，此时同时混入有监督目标补丁；否则仅混入源补丁。该条件分支使 CoSMix 能够无缝切换 UDA 和 SSDA 设定。

**第三阶段：全局随机增强 $r$。** 对拼接后的完整混合点云施加全局增强（旋转、缩放、平移），进一步增加数据多样性。

消融实验证实，局部增强和全局增强分别贡献约 1.5 mIoU 和 2 mIoU 的性能增益，而双分支对称混合（同时进行 $t \to s$ 和 $s \to t$）是性能的核心保障——仅使用单分支时性能从 40.4 mIoU 骤降至 31.6 mIoU（见 Tab. 9）。

### 教师-学生自训练与损失函数

CoSMix 采用在线指数移动平均（EMA）更新教师网络参数，持续提升伪标签质量：

$$\theta_{i}^{\prime} = \beta \theta_{i-1}^{\prime} + (1 - \beta) \theta$$

其中 $\theta$ 为学生网络参数，$\theta^{\prime}$ 为教师网络参数，$\beta = 0.99$ 为动量系数。教师网络每 $\gamma$ 步更新一次，其产生的伪标签供下一轮语义选择使用，形成自改进循环。

总损失为两个混合分支的 Dice 分割损失之和：

$$\mathcal{L}_{tot} = \mathcal{L}_{s \to t} + \mathcal{L}_{t \to s}$$

其中每个分支损失 $\mathcal{L}_{s \to t} = \mathcal{L}_{seg}(\Phi_{\theta}(\mathcal{X}^{s \to t}), \mathcal{Y}^{s \to t})$ 计算学生网络在混合点云上的预测与混合标签之间的分割误差。Dice 损失对类别不平衡具有天然的鲁棒性，与语义选择中的长尾加权采样形成互补。

消融实验表明，EMA 教师更新和长尾加权采样各自贡献超过 1 mIoU 的增益，验证了这两个组件在稳定自训练过程和缓解类别偏差方面的关键作用（见 Tab. 9）。

## 实验与关键发现

### 核心实验结果

CoSMix在多个合成→真实和真实→真实的域适应基准上均取得了显著的性能提升。在无监督域适应（UDA）设定下，**SynLiDAR → SemanticPOSS** 任务上CoSMix达到32.2 mIoU，比最强的对比方法ST-PCT（28.9 mIoU）高出+3.3 mIoU，比仅源域训练的Source-only（23.8 mIoU）高出+8.4 mIoU（Tab. 2）。在**SemanticKITTI → nuScenes** 真实→真实UDA任务上，CoSMix达到46.2 mIoU，比Source*（40.1 mIoU）提升+6.1 mIoU（Tab. 4）。在**SynLiDAR → SemanticKITTI** UDA任务上，CoSMix达到40.4 mIoU（Tab. 3）。

在半监督域适应（SSDA）设定下，CoSMix-SSDA的性能增益更为显著。**SynLiDAR → SemanticPOSS** SSDA中，CoSMix达到41.0 mIoU，比APE-PCT（31.2 mIoU）高出+9.8 mIoU（Tab. 5）。**SemanticKITTI → nuScenes** SSDA中达到48.9 mIoU，比Source*提升+8.8 mIoU（Tab. 7）。**SynLiDAR → SemanticKITTI** SSDA中达到34.3 mIoU，比APE-PCT（27.0 mIoU）高出+7.3 mIoU（Tab. 6）。

值得注意的是，在**SynLiDAR → nuScenes** 这一域差距极大的迁移任务上，CoSMix的UDA和SSDA分别仅达到27.3 mIoU和27.6 mIoU（Tab. 8），增益有限。这表明当源域和目标域之间的语义分布和传感器特性差异过大时，单纯依靠语义级混合策略的效果会减弱。

### 消融研究

Table 9的系统消融实验揭示了CoSMix各组件的独立贡献（以SynLiDAR→SemanticKITTI UDA为基准，Source*为23.8 mIoU）：

1. **双分支混合是核心机制**：仅使用单分支混合（t→s或s→t）时，mIoU仅为31.6，而完整双分支混合可达40.4 mIoU，双分支对称设计带来了约+8.8 mIoU的增益。这验证了同时从源域混入目标域和从目标域混入源域对于构建有效中间域至关重要。

2. **组合增强策略贡献显著**：在双分支混合基础上，全局增强（r）带来约+2 mIoU的提升（31.6→33.7），局部增强（h）进一步带来约+1.5 mIoU的提升。两者协同作用使得模型能够更好地处理点云的空间变换和局部结构扰动。

3. **长尾加权采样与EMA教师更新各自贡献超过1 mIoU**：基于源类分布的反向频率加权采样函数f有效缓解了长尾类别被忽视的问题；EMA教师更新（β=0.99）持续提升伪标签质量，两者共同将性能从约38 mIoU推至40.4 mIoU。

4. **与通用点云混合策略对比**：Fig. 5a显示，CoSMix的双分支语义混合（38.9 mIoU）显著优于Mix3D（31.6 mIoU）、PointCutMix（30.4 mIoU）和PolarMix（28.5 mIoU）。这表明语义引导的组合式混合比无差别的几何混合更适合域适应场景。

5. **置信度阈值敏感性**：Fig. 5b显示，伪标签选择的置信度阈值ζ在0.85附近达到最优（40.4 mIoU）。阈值过低会导致噪声伪标签污染训练，过高则可能丢失有效目标信息，损害对象完整性。

6. **SSDA混合策略消融**：Fig. 5c证实，在SSDA设定下，双分支混合（Full CoSMix-SSDA）远优于仅优化有监督目标（naive策略）或单分支混合（sup→s、sup→t），表明跨域混合对于充分利用少量标注目标数据不可或缺。

### 失败模式与局限性

尽管CoSMix在多数基准上表现优异，但存在以下已知局限：

- **伪标签质量依赖**：方法严重依赖教师网络产生的伪标签质量。若源域预训练不充分，初始伪标签噪声会通过EMA自训练循环累积，限制最终适应性能。Fig. 4表明，不同预训练初始化点对CoSMix和ST*的适应效果均有显著影响，但CoSMix在各初始化点下均优于ST*。

- **极端域差距场景**：在SynLiDAR→nuScenes任务上，CoSMix的UDA（27.3 mIoU）和SSDA（27.6 mIoU）性能有限，与Source*（18.1 mIoU）相比的增益远小于其他基准。这说明当源域和目标域的类分布、稀疏性和传感器噪声差异极大时，语义级混合策略的效果会达到瓶颈。

- **无法处理源自由场景**：CoSMix需要目标域存在无监督数据用于混合和伪标签生成，无法直接应用于完全无目标数据的源自由域适应（source-free DA）设定。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2308_14619/figures/014_Figure_5.jpg]]
*Figure 5: c) Fig. 5: a) Comparison of the adaptation performance with different point cloud mix up strategies. Compared to the recent mixing strategies Mix3D [21], PointCutMix [72] and, PolarMix [73], our mixing strategy and its variations achieve superior performance. b) Comparison of the adaptation performance on confidence threshold values. Adaptation results show that ζ should be set such that to achieve a trade-off between pseudo-label correctness and object completeness. c) Comparison of the SSDA performance with different mixing strategies: optimization without mix (naive), single branch mixing with source point clouds (sup → s), single branch mixing with unsupervised target point clouds (sup...*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2308_14619/figures/001_Table_1.jpg]]
*Table 1: Overview of existing methods for unsupervised (UDA) and semi-supervised (SSDA) adaptation in point cloud segmentation. For each approach, we report the sensor setup (Setup), the architecture (Input data type and Model), and the source and target datasets. Then, we classify the adaptation strategy into mixup based, adversarial learning based, alignment based, generative based, self-training based and auxiliary task based. Furthermore, we report whether the implementation (Code) is publicly available*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2308_14619/figures/003_Table_2.jpg]]
*Table 2: Unsupervised adaptation results on SynLiDAR → SemanticPOSS. We denote our reproduced baselines and results with ⋆, e.g., Source⋆. Source⋆ and Target⋆ correspond to the model trained on the source synthetic dataset (lower bound) and on the target real dataset (upper bound), respectively. Results are reported in terms of mean Intersection over the Union (mIoU)*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2308_14619/figures/004_Table_3.jpg]]
*Table 3: Unsupervised adaptation results on SynLiDAR → SemanticKITTI. We denote our reproduced baselines and results with ⋆, e.g., Source⋆. Source⋆ and Target⋆ correspond to the model trained on the source synthetic dataset (lower bound) and on the target real dataset (upper bound), respectively. Results are reported in terms of mean Intersection over the Union (mIoU)*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2308_14619/figures/005_Table_4.jpg]]
*Table 4: Unsupervised adaptation results on SemanticKITTI → nuScenes. We denote our reproduced baselines and results with ⋆, e.g., Source⋆. Source⋆ and Target⋆ correspond to the model trained on the source real dataset (lower bound) and on the target real dataset (upper bound), respectively. Results are reported in terms of mean Intersection over the Union (mIoU)*


![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2308_14619/figures/012_Table_9.jpg]]
*Table 9: Ablation study of the CoSMix components: mixing strategy (t → s and s → t), compositional mix augmentations (local h and global r), mean teacher update (β) and, weighted class selection in semantic selection (f ). Each combination is named with a different version (a-h). Source⋆ performance are added as lower bound and highlighted in gray to facilitate the reading*

## 定位与知识库关联

### 1. 与现有域适应路线的继承与分叉

CoSMix 的底层机制可以追溯到三条主线，但它通过“语义引导的组合式混合”实现了关键分叉，避免了各自主线的典型失效模式。

**（1）相对于混合增强路线的继承与超越**

点云混合（mixup）是近年 3D 域适应的活跃方向。CoSMix 直接继承了这一思路，但显著改变了混合的粒度和语义条件。此前的混合策略大致可分为两类：

- **全局混合**：如 **PolarMix**（Xiao et al., AAAI 2022）和 **Mix3D**，在完整点云或场景级别执行拼接/混合，不区分语义区域。这类方法实现简单，但容易将不同语义类别的点混合在一起，产生语义模糊的训练信号。
- **局部裁剪混合**：如 **PointCutMix**，在随机位置裁剪点云块进行混合，但缺乏语义引导，裁剪区域可能跨越多个语义边界。

CoSMix 的关键分叉在于引入 **语义选择函数 $f$ 和 $g$**（Sec. 3.2），将混合粒度锁定在“语义补丁”层面——即属于同一语义类别的点集。消融实验直接验证了这一设计的决定性作用：在 SynLiDAR → SemanticKITTI UDA 设定下，CoSMix 的双分支混合达到 38.9 mIoU，而 PolarMix、PointCutMix 和 Mix3D 分别仅达到 28.5、30.4 和 31.6 mIoU（Fig. 5a）。差距超过 7 mIoU，说明“语义引导”而非“随机混合”才是域迁移的核心驱动力。

**（2）相对于自训练路线的继承与改进**

自训练（Self-training）是域适应中利用目标域无监督数据的经典范式。CoSMix 直接继承了 **ST**（Zou et al., ICCV 2019）的置信度正则化思想，但通过两个关键机制克服了自训练在 3D 点云中的固有问题：

- **EMA 教师网络替代离线固定模型**：传统自训练通常使用源域预训练模型生成伪标签后固定，伪标签质量不会随着训练改进。CoSMix 采用指数移动平均（$\theta'_i = \beta \theta'_{i-1} + (1-\beta)\theta$，$\beta=0.99$，每 $\gamma$ 步更新）持续改进教师网络，使伪标签质量与模型能力同步提升。消融实验表明，仅 EMA 教师更新一项就贡献超过 1 mIoU 的增益（Tab. 9）。
- **置信度门控替代全局阈值**：通过语义选择函数 $g(\Phi_{\theta'}(\mathcal{X}_U^t), \zeta)$ 在类别级别筛选可靠伪标签，而非对全场景使用固定阈值。实验显示置信度阈值 $\zeta$ 的最优值约为 0.85，此时性能达到峰值 40.4 mIoU（Fig. 5b）。

**（3）相对于对抗/对齐路线的定位**

早期的域适应方法依赖特征空间对齐，如 **ADDA**（Tzeng et al., CVPR 2017）的对抗域判别和 **MMD**（Tzeng et al., CVPR 2017）的最大均值差异最小化。在 3D 点云分割中，**PCT**（Xiao et al., AAAI 2022）将对抗学习引入 LiDAR 域适应，**ST-PCT** 进一步结合了自训练。

CoSMix 选择了一条根本不同的路径：**不在特征空间进行显式对齐，而是在数据空间构造中间域**。这一选择的合理性在于：3D 点云的域偏移主要表现为传感器噪声、稀疏性差异和场景布局差异，这些差异在数据空间（点坐标和语义分布）比在特征空间更容易被直接操作和缓解。实验证据支持这一判断：在 SynLiDAR → SemanticPOSS UDA 中，CoSMix 达到 32.2 mIoU，比 ST-PCT 高 +3.3 mIoU（Tab. 2）；在 SynLiDAR → SemanticKITTI UDA 中达到 40.4 mIoU（Tab. 3）。

### 2. 适用边界与条件约束

CoSMix 的适用性受到以下边界条件的约束，这些边界直接源于其核心机制的设计假设：

**（1）对源域预训练质量的依赖**

CoSMix 的整个伪标签生成链路（教师网络 → 语义选择 $g$ → 混合 → 学生训练）严重依赖初始教师模型的质量。如果源域预训练不足，教师网络产生的伪标签噪声会被语义选择函数放大，进而污染混合点云的训练信号。论文通过不同预训练初始化点的实验（Fig. 4）间接验证了这一点：当源域预训练性能较低时，CoSMix 的适应增益会缩小。这意味着 CoSMix 不适合源域标注极度稀缺或源域与目标域语义差距过大的场景——此时需要额外的自监督预训练或基础模型初始化来弥补。

**（2）对目标域无监督数据的刚性需求**

CoSMix 的双分支混合结构（$t \to s$ 和 $s \to t$）要求目标域存在无监督点云数据。它无法处理 **源自由域适应（source-free domain adaptation）** 场景——即训练时完全无法访问任何目标域数据。这是其与基于生成模型或特征对齐方法的重要边界差异。

**（3）极端域差距下的性能退化**

当源域与目标域的类分布和场景结构差异极大时，CoSMix 的混合策略效果显著减弱。最典型的证据来自 SynLiDAR → nuScenes 跨域设定：CoSMix-UDA 仅达到 27.3 mIoU，CoSMix-SSDA 仅达到 27.6 mIoU（Tab. 8）。相比之下，在域差距较小的 SemanticKITTI → nuScenes（同为真实数据，仅传感器不同）中，CoSMix-UDA 达到 46.2 mIoU（Tab. 4）。这揭示了一个根本性限制：当源域的合成场景与目标域的真实场景在语义构成上几乎没有重叠时（如 SynLiDAR 的城市场景与 nuScenes 的高速公路场景），语义选择函数 $f$ 和 $g$ 难以找到有意义的跨域补丁匹配，混合操作退化为近似随机拼接。

**（4）对骨干网络的通用性假设**

所有实验统一使用 MinkowskiNet 作为骨干网络（Sec. 4.2），且所有对比方法均基于同一骨干复现。虽然这保证了公平比较，但也意味着 CoSMix 在其他稀疏卷积架构（如 SPVNAS、Cylinder3D）或基于 Transformer 的架构上的表现尚未验证。语义补丁的混合操作是否与不同骨干的特征提取特性兼容，需要进一步实验确认。

### 3. 未解决的开放问题

**（1）能否降低对大规模标注源数据的依赖？**

CoSMix 目前假设源域有完整的逐点语义标注。一个自然的扩展方向是引入自监督学习任务——如点云补全、掩码重建或对比学习——来替代或增强源域预训练，从而在源域标注稀缺时仍能获得高质量的初始教师模型。这直接关系到 CoSMix 在真实场景中的部署可行性。

**（2）框架能否推广到域泛化设定？**

CoSMix 的核心机制——语义引导的跨域混合——在理论上不依赖于训练时访问目标域数据。如果将目标域补丁替换为多种数据增强策略生成的“伪目标域”，是否可以在域泛化（domain generalization）设定下工作？这需要重新设计语义选择逻辑，使其不依赖目标域伪标签。

**（3）语义混合策略能否迁移到其他 3D 任务？**

组合式语义混合的核心思想——在保留结构信息的前提下进行语义级跨域数据增强——在原理上不限于语义分割。3D 目标检测同样面临域偏移问题，但目标的边界框标注与语义分割的逐点标注在混合时需要不同的处理逻辑。如何定义“检测语义补丁”并设计相应的混合策略，是一个开放的设计问题。

**（4）极端稀疏性差异下的自适应混合策略？**

当源域和目标域的点云密度差异极大时（如 64 线 LiDAR vs. 4 线 LiDAR），语义补丁的物理尺度和点密度可能不匹配。当前的局部增强 $h$ 和全局增强 $r$ 未针对稀疏性差异进行专门设计。是否需要引入密度感知的重采样或补丁尺度自适应机制，是提升极端域差距下性能的关键方向。

## 原文 PDF

![[paperPDFs/TPAMI_2023/Compositional_semantic_mix_for_domain_adaptation_in_point_cloud_segmentation.pdf]]
