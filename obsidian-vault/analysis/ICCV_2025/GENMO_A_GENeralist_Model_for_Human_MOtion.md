---
title: "GENMO: A GENeralist Model for Human MOtion"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/GENMO_A_GENeralist_Model_for_Human_MOtion.pdf
code_link: null
project_link: https://research.nvidia.com/labs/dair/genmo/
aliases:
- GENMO
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "双模式训练范式（估计模式：零噪声+最大时间步强化一步预测精度；生成模式：标准扩散训练保持多样性）与估计引导的生成训练（利用2D标注数据产生伪3D，桥接估计与生成），使得统一模型既能精确运动估计又能多样化生成。"
primary_logic: "将运动估计重新定义为条件运动生成，通过回归与扩散的协同，在一个框架下获得双向益处：生成先验改善遮挡等情况下的估计质量，而多样化的视频数据提升生成的表现力。"
claims:
- "GENMO在全局运动估计上显著超越专用方法：EMDB数据集W-MPJPE100 202.1 mm，优于TRAM的222.4 mm，且使用相同SLAM和特征提取器。"
- "在局部运动估计任务上，GENMO在3DPW、RICH、EMDB-1等数据集上达到SOTA，尤其在3DPW上PA-MPJPE 34.6 mm，优于CLIFF (43.0)等方法。"
- "在3DPW-XOCC遮挡基准上，GENMO显著优于SOTA方法，且去除生成组分（仅回归）后性能下降（MPJPE 89.0→76.2），证明生成先验对遮挡鲁棒性的关键作用。"
- "在音乐到舞蹈生成任务上，通用模型GENMO在物理合理性（PFC）、节拍对齐（BAS）和多样性方面优于专用模型，展示了跨任务的正向迁移。"
---

# GENMO: A GENeralist Model for Human MOtion

> [!tip] 核心洞察
> 将运动估计重新定义为条件运动生成，通过回归与扩散的协同，在一个框架下获得双向益处：生成先验改善遮挡等情况下的估计质量，而多样化的视频数据提升生成的表现力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GENMO：一个通用人体运动模型 |
| 英文题名 | GENMO: A GENeralist Model for Human MOtion |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2505.01425) · [Project](https://research.nvidia.com/labs/dair/genmo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GENMO |
| Dataset | EMDB-2 (全局运动估计), RICH (全局运动估计), 3DPW (局部运动估计), 3DPW-XOCC (严重遮挡估计) |

> [!tip] 效果简介
> - EMDB-2 (全局运动估计) 上，W-MPJPE100 (mm) ↓ 为 202.1 (with DROID-SLAM)，对比 222.4 (TRAM with DROID-SLAM)，变化 -20.3。
> - RICH (全局运动估计) 上，WA-MPJPE100 (mm) ↓ 为 75.3 (with DROID-SLAM)，对比 78.8 (GVHMR with DROID-SLAM)，变化 -3.5。
> - 3DPW (局部运动估计) 上，PA-MPJPE (mm) ↓ 为 34.6，对比 43.0 (CLIFF)，变化 -8.4。

## 概要

人体运动理解长期面临一个结构性矛盾：**运动估计**要求从视频等观测中精确重建3D运动，输出必须确定、忠实于输入信号；而**运动生成**要求从文本、音乐等抽象条件中创造多样化、合理的运动，输出必须随机且富有表现力。传统方法将二者视为独立任务，分别设计专用模型，导致运动表示无法共享、先验知识难以迁移，也无法在统一框架下同时满足精确重建与灵活的多模态控制。

GENMO提出一个根本性的视角转换：**将运动估计重新定义为条件运动生成**。基于此，论文构建了一个统一的扩散Transformer框架，通过两项关键设计打破估计与生成的壁垒：

- **双模式训练范式**：估计模式下，输入纯高斯噪声并设置最大扩散时间步，强制模型执行确定性最大似然估计；生成模式下，采用标准扩散训练保持输出多样性。模型根据条件信号的确定性程度自动切换模式——视频条件同时启用双模式，文本/音乐条件仅使用生成模式。
- **估计引导的生成训练**：利用估计模式从2D标注视频中生成伪3D运动，再通过扩散过程施加2D重投影损失，使模型能够从海量2D数据中学习，桥接估计与生成之间的数据鸿沟。

这一设计产生了双向增益：**生成先验改善了遮挡等困难场景下的估计鲁棒性，而多样化的视频数据提升了生成任务的表现力**。

在**全局运动估计**任务上，GENMO在EMDB-2数据集上达到W-MPJPE100 202.1 mm，显著优于专用方法TRAM（222.4 mm），且使用相同的SLAM系统和特征提取器。在**局部运动估计**任务上，GENMO在3DPW数据集上取得PA-MPJPE 34.6 mm，超越CLIFF（43.0 mm）等方法。在严重遮挡场景（3DPW-XOCC）中，GENMO的MPJPE为76.2 mm，较NIKI temporal（88.9 mm）降低12.7 mm；消融实验证实，去除生成组分后性能显著下降（MPJPE升至89.0 mm），直接验证了生成先验对遮挡鲁棒性的关键作用。

在**运动生成**任务上，统一的GENMO同样展现出竞争力：在音乐到舞蹈生成（AIST++）中，物理合理性（PFC）和节拍对齐（BAS）指标优于专用模型EDGE；在运动中间帧生成中，联合训练估计与生成任务显著优于纯扩散基线，且去除2D数据训练后性能下降，验证了统一训练和估计引导2D学习的双重价值。

GENMO的方法定位处于**扩散生成模型**与**人体运动分析**的交叉点：它继承了扩散模型的多模态条件建模能力（如MDM, Tevet et al., ICLR 2023），但通过双模式训练将其扩展为同时支持回归精度与生成多样性的统一范式；它借鉴了全局运动估计中SLAM与运动先验结合的思想（如TRAM, Wang et al., ECCV 2024），但将运动先验内化为生成模型本身，而非外部模块。在知识库中，GENMO代表了一条从“任务专用模型”走向“通用运动基础模型”的技术路径。

人体运动建模长期面临一个根本性的任务割裂：**运动估计**（从视频、2D关键点等观测中精确重建3D运动）与**运动生成**（根据文本、音乐等抽象条件创造多样化运动）被视为两个独立领域，各自发展出专用的模型架构和训练范式。运动估计要求确定性、高精度的输出，而运动生成则需要捕捉条件信号下的多模态分布，产生丰富且合理的运动变化。这种分离导致三个关键问题：

1. **运动表示与先验知识无法共享**：专用估计模型学到的物理合理性、人体动力学先验无法惠及生成任务，反之，生成模型从海量数据中习得的运动多样性也难以提升估计的鲁棒性。
2. **难以同时满足精确重建与灵活控制**：估计模型在严重遮挡、动态相机等挑战场景下缺乏生成先验的补全能力；生成模型则缺乏从强确定性条件（如视频）中提取精确运动约束的机制。
3. **多模态条件控制的碎片化**：现有方法通常为每种条件类型（视频、文本、音乐、关键帧）设计独立的注入模块和训练流程，缺乏统一的框架来组合任意条件并生成平滑过渡。

传统方法的典型代表包括：**TRAM**（Wang et al., ECCV 2024）专注于全局运动估计但依赖外部SLAM且未涉及生成任务；**MDM**（Tevet et al., ICLR 2023）作为文本到运动生成的扩散基线，缺乏精确估计能力；**EDGE**（Tseng et al., CVPR 2023）在音乐到舞蹈生成上表现优异，但无法处理视频条件。这些专用模型在各自领域虽有建树，却无法在统一框架下协同工作。

GENMO的核心动机在于打破这一壁垒：**将运动估计重新定义为条件运动生成问题**。当条件信号强且确定（如视频帧、2D骨架）时，模型应输出精确的确定性估计；当条件信号弱或抽象（如文本描述、音乐节拍）时，模型应产生多样化但物理合理的生成。这一统一视角的潜在收益是双向的——生成先验可改善遮挡等病态条件下的估计质量，而多样化视频数据可提升生成的表现力和物理合理性。

## 核心方法与创新机理

GENMO 的核心创新在于将**人体运动估计**与**运动生成**这两个长期分离的任务统一为条件运动生成的单一框架，并通过三项关键设计实现双向增益。以下围绕相对 baseline 的 changed slots 展开分析。

### 1. 训练范式：从标准扩散到双模式协同

传统运动扩散模型（如 **MDM**，Tevet et al., ICLR 2023）仅采用标准 DDPM 训练范式——从随机噪声逐步去噪，优化生成多样性。然而，运动估计任务要求精确、确定性的输出，与标准扩散的随机采样本质存在根本冲突。

GENMO 提出**双模式训练范式**（Section 3.2），根据条件信号的确定性动态切换训练模式：

- **估计模式**（Estimation Mode）：输入纯高斯噪声 $z \sim \mathcal{N}(\mathbf{0}, I)$ 和最大扩散时间步 $T$，强制模型执行最大似然估计，目标函数为：
  $$\mathcal{L}_{\mathrm{est}} = \mathbb{E}_{z \sim \mathcal{N}(\mathbf{0}, I)} \left[ \| x_0 - \mathcal{G}(z, T, \mathcal{C}, \mathcal{M}) \|^2 \right]$$

- **生成模式**（Generation Mode）：保留标准 DDPM 训练，维护输出的多样性与随机性：
  $$\mathcal{L}_{\mathrm{gen}} = \mathbb{E}_{t \sim [1, T], x_t \sim q(x_t | x_0)} \left[ \| x_0 - \mathcal{G}(x_t, t, \mathcal{C}, \mathcal{M}) \|^2 \right]$$

**模式选择机制**：当条件信号本身具有强确定性（如视频、2D 骨架）时，同时启用两种模式；对于弱确定性条件（如文本、音乐），仅使用生成模式。这一设计使得同一模型既能精确重建观测运动，又能灵活响应抽象条件。

**消融证据**（Table 7）：去除估计模式（仅保留 DDPM 训练）导致全局运动估计性能大幅下降——RICH 数据集上 W-MPJPE 从 81.3 升至 88.9，验证了估计模式对精确重建的必要性。

### 2. 数据利用：估计引导的 2D 生成训练

传统方法通常仅利用 3D 标注数据训练生成模型，或通过外部 3D 重建间接利用 2D 视频，导致生成模型无法直接从海量 2D 标注中学习运动先验。

GENMO 提出**估计引导的生成训练**（Section 3.2）：首先利用估计模式生成伪 3D 运动 $\hat{x}_0$，再通过前向扩散过程获得 $\hat{x}_t$，最后施加 2D 重投影损失监督生成过程：

$$\mathcal{L}_{\mathrm{gen-2D}} = \mathbb{E}_{\hat{x}_t \sim q(\hat{x}_t | \hat{x}_0), t \sim [1, T]} \left[ \| x_{\mathrm{2d}} - \Pi(\mathcal{G}(\hat{x}_t, t, \mathcal{C})) \|^2 \right]$$

其中 $\Pi$ 为 2D 投影函数。这一机制在估计与生成之间架起桥梁：估计模式产生的伪 3D 为生成模式提供训练信号，而 2D 数据中蕴含的丰富运动模式又反向增强生成表现力。

**消融证据**（Table 6）：去除 2D 数据训练（w/o $\mathcal{L}_{\mathrm{gen-2D}}$）使运动中间帧生成质量下降——HumanML3D 2-Keyframe 设置下 PA-MPJPE 从 53.5 增加到 56.4，验证了估计引导的 2D 训练对生成任务的贡献。

### 3. 条件注入：多文本时间窗口注意力

现有文本到运动方法（如 MDM）通常将文本嵌入与运动序列直接拼接或添加交叉注意力，这容易引入时序偏差——文本可能影响其不应控制的时间段。

GENMO 提出**多文本注意力块**（Multi-text Injection Block），通过时间窗口掩码的掩码多头注意力实现精准时序控制（Section 3.1）：

$$f_{out} = \sum_{k=1}^{K} \mathbf{MaskedMHA}\left( f_{in}, c_{\mathrm{text}}^{k}, \Omega_{k} \right)$$

其中时间窗口掩码 $\Omega_k(i,j)$ 定义为：

$$\Omega_{k}(i,j) = \begin{cases} 1 & \text{if } i \text{ is within time window of text } k \\ 0 & \text{otherwise} \end{cases}$$

该机制使得每个文本嵌入仅在其指定的时间段内影响运动特征，支持 $K$ 条文本对不同时间区间的独立控制，实现多文本、多时间段的精准运动合成（Figure 3）。

### 4. 运动表示：统一重力视角坐标系

传统方法通常将全局轨迹、局部姿态、相机参数分离表示，导致估计与生成任务难以共享运动表示。

GENMO 采用**统一重力视角坐标系表示**（Section 3），单帧运动向量 $x^i$ 同时编码：

$$x^{i} = \big( \Gamma_{\mathrm{gv}}^{i}, {v}_{\mathrm{root}}^{i}, {\theta}^{i}, \beta^{i}, t_{\mathrm{root}}^{i}, \pi^{i}, p^{i} \big)$$

包含重力视图朝向 $\Gamma_{\mathrm{gv}}$、根速度 $v_{\mathrm{root}}$、SMPL 关节角度 $\theta$、体型 $\beta$、根平移 $t_{\mathrm{root}}$、相机姿态 $\pi$ 和接触标签 $p$。这一统一表示使得估计与生成共享同一运动空间，是实现双模式训练的基础。

### 5. 序列长度灵活性：RoPE 滑动窗口注意力

传统方法通常固定训练长度，推理时需要后处理拼接。GENMO 采用基于 RoPE 的滑动窗口自注意力（Section 3.1），支持训练长度（120 帧）外的任意长度生成，且无需后处理，为长序列运动合成提供了原生支持。

### 创新总结

上述 changed slots 形成了一条清晰的因果链：**统一运动表示**（Slot 4）为估计与生成共享奠定基础；**双模式训练**（Slot 1）使同一模型兼顾精确重建与多样性生成；**估计引导的 2D 训练**（Slot 2）桥接两类任务，实现数据层面的双向增益；**多文本注意力**（Slot 3）与**RoPE 滑动窗口**（Slot 5）则分别增强了条件控制的精度与序列长度的灵活性。这些创新共同构成了 GENMO 从专用模型向通用运动模型跃迁的技术支柱。

GENMO 将人体运动估计与生成统一为**条件运动生成**问题：给定一组条件信号 $\mathcal{C}$ 及对应的条件掩码 $\mathcal{M}$，模型合成一段长度为 $N$ 的人体运动序列 $\mathbf{x}$。该统一框架的核心在于，运动估计被重新定义为受观测信号约束的生成任务，而非独立于生成的确定性回归问题。

### 统一运动表示

为实现估计与生成的无缝共享，GENMO 采用统一的**重力视角坐标系**表示。单帧运动向量定义为：

$$x^{i} = \big( \Gamma_{\mathrm{gv}}^{i}, {v}_{\mathrm{root}}^{i}, {\theta}^{i}, \beta^{i}, t_{\mathrm{root}}^{i}, \pi^{i}, p^{i} \big)$$

其中 $\Gamma_{\mathrm{gv}}^{i}$ 为重力视角方向，${v}_{\mathrm{root}}^{i}$ 为局部根速度，${\theta}^{i}$ 和 $\beta^{i}$ 为 SMPL 关节角度与体型参数，$t_{\mathrm{root}}^{i}$ 为根平移，$\pi^{i}$ 为相机姿态，$p^{i}$ 为手脚接触标签。该表示同时编码全局轨迹、局部姿态、相机参数与物理接触信息，使单一模型能够处理从视频估计到文本生成的多种任务。

### 条件融合与架构骨干

GENMO 的架构由三个核心模块串联构成（Figure 2）：

1. **Additive Fusion Block（加性融合块）**：将各类条件信号（视频特征、2D 关键点、音乐特征、相机参数等）通过独立 MLP 编码后求和，再与带噪运动 $\mathbf{x}_t$ 融合，生成逐帧运动 token 序列。对于帧对齐模态（如视频、音乐、2D 骨架），采用时间掩码策略处理缺失帧。

2. **RoPE-based Transformer Block（旋转位置嵌入 Transformer 块）**：利用旋转位置嵌入（RoPE）进行相对时序注意力，捕获运动动态。该模块采用滑动窗口自注意力机制，支持训练长度（120 帧）外的任意长度生成，无需后处理拼接。

3. **Multi-text Injection Block（多文本注入块）**：针对文本条件，通过掩码多头注意力将多条文本嵌入约束在指定时间窗口内注入运动特征。具体地，对 $K$ 条文本嵌入分别执行带时间窗口掩码的注意力，求和得到融合特征：

$$f_{out} = \sum_{k=1}^{K} \mathbf{MaskedMHA}\left( f_{in}, c_{\mathrm{text}}^{k}, \Omega_{k} \right)$$

其中时间窗口掩码 $\Omega_{k}(i,j)$ 为二值矩阵，仅在第 $k$ 条文本对应的时间步生效（Figure 3）。该设计支持多文本、多时间段的精准控制。

4. **Output Head（输出头）**：预测去噪后的完整运动序列 $\mathbf{x}_0$，包含全局运动、局部姿态、相机姿态和接触标签。

### 双模式训练范式

传统扩散模型仅通过标准去噪目标训练，无法兼顾精确估计所需的确定性输出与生成所需的多样性。GENMO 提出**双模式训练**（Section 3.2），根据条件信号的确定性程度动态选择训练模式：

- **估计模式（Estimation Mode）**：输入纯高斯噪声 $\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 和最大时间步 $T$，强制模型执行最大似然估计，目标函数为：

$$\mathcal{L}_{\mathrm{est}} = \mathbb{E}_{\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left[ \| \mathbf{x}_0 - \mathcal{G}(\mathbf{z}, T, \mathcal{C}, \mathcal{M}) \|^2 \right]$$

- **生成模式（Generation Mode）**：标准扩散训练，对随机时间步 $t$ 和带噪运动 $\mathbf{x}_t$ 求期望，预测原始干净运动：

$$\mathcal{L}_{\mathrm{gen}} = \mathbb{E}_{t \sim [1, T], \mathbf{x}_t \sim q(\mathbf{x}_t | \mathbf{x}_0)} \left[ \| \mathbf{x}_0 - \mathcal{G}(\mathbf{x}_t, t, \mathcal{C}, \mathcal{M}) \|^2 \right]$$

训练时，对于具有强确定性条件的数据集（如视频、2D 骨架），同时启用两种模式；对于弱条件（如文本、音乐），仅使用生成模式。这一设计使模型在视频条件下表现出近乎确定性的预测行为，而在文本条件下保持多样化的生成能力（Figure 4）。

### 估计引导的 2D 数据训练

为利用海量 2D 标注视频数据，GENMO 进一步引入**估计引导的生成训练**：先用估计模式生成伪 3D 运动 $\hat{\mathbf{x}}_0$，再通过前向扩散过程施加 2D 重投影损失，使模型从 2D 标注中学习：

$$\mathcal{L}_{\mathrm{gen-2D}} = \mathbb{E}_{\hat{\mathbf{x}}_t \sim q(\hat{\mathbf{x}}_t | \hat{\mathbf{x}}_0), t \sim [1, T]} \left[ \| \mathbf{x}_{2\mathrm{d}} - \Pi(\mathcal{G}(\hat{\mathbf{x}}_t, t, \mathcal{C})) \|^2 \right]$$

其中 $\Pi$ 为 2D 投影函数。该机制桥接了估计与生成任务，使得 2D 视频数据既能提升估计精度，也能增强生成表现力——消融实验（Table 6）表明，去除该损失后运动中间帧生成质量显著下降（HumanML3D 2-Keyframe 设置下 PA-MPJPE 从 53.5 增至 56.4）。

### 输入输出流总结

整体 pipeline 的输入为多模态条件信号（视频、2D 关键点、文本、音乐、3D 关键帧等）及其时间掩码，输出为统一表示下的完整运动序列。推理时，通过 DDIM 采样在少量步数内完成生成：运动估计在 5 步左右达到最优，文本到运动生成随步数增加持续改善（Table 8），实现了估计精度与生成效率的兼顾。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2505_01425/figures/001_Figure_1.jpg]]
*Figure 1: GENMO unifies human motion estimation and generation in a single framework and supports diverse conditioning signals including monocular videos, 2D keypoints, text descriptions, music, and 3D keyframes. GENMO can estimate accurate global human motion from videos with dynamic cameras and seamlessly handles arbitrary combinations and lengths of conditioning signals while generating smooth transitions between them. All of this is achieved in a single feedforward diffusion pass without complex post-processing*

### 统一运动表示

GENMO 将人体运动估计与生成统一为条件运动生成问题，其基础是一套覆盖全局与局部信息的运动表示。对于长度为 $N$ 的运动序列，第 $i$ 帧的完整运动向量定义为：

$$x^{i} = \big( \Gamma_{\mathrm{gv}}^{i}, {v}_{\mathrm{root}}^{i}, {\theta}^{i}, \beta^{i}, t_{\mathrm{root}}^{i}, \pi^{i}, p^{i} \big)$$

其中各变量含义如下：
- $\Gamma_{\mathrm{gv}}^{i}$：重力视角（gravity-view）坐标系下的全局朝向，将世界坐标系运动与重力方向对齐；
- ${v}_{\mathrm{root}}^{i}$：根节点在局部坐标系下的线速度，编码短时运动动态；
- ${\theta}^{i}$：SMPL 模型的关节旋转参数，表示局部姿态；
- $\beta^{i}$：SMPL 体型参数；
- $t_{\mathrm{root}}^{i}$：根节点在世界坐标系下的平移，提供全局轨迹；
- $\pi^{i}$：相机外参，支持动态相机场景下的全局运动估计；
- $p^{i}$：手-脚接触标签的二值指示符，用于物理合理性约束。

该表示同时编码了全局轨迹、局部姿态、相机运动和接触状态，使得估计任务（需要精确的全局/局部重建）与生成任务（需要多样化的运动合成）能够在同一特征空间中共享运动先验。

### 条件融合与 Transformer 骨干

模型接收多模态条件信号 $\mathcal{C}$ 及其对应的时序掩码 $\mathcal{M}$，通过**加性融合块**（Additive Fusion Block）将各条件类型（视频特征、2D 关键点、音乐特征、文本嵌入、3D 关键帧、相机参数等）经独立 MLP 编码后求和，再与带噪运动序列 $x_t$ 融合为逐帧运动 token 序列。

时序建模采用基于**旋转位置嵌入**（RoPE）的 Transformer 块，通过滑动窗口自注意力捕获运动动态。RoPE 的相对位置编码使模型天然支持训练长度（120 帧）之外的任意长度序列生成，无需推理时的后处理拼接。

### 多文本注入块

为实现多条文本描述对不同时间段的精准控制，GENMO 设计了**多文本注入块**（Multi-text Injection Block）。给定 $K$ 条文本嵌入 $\{c_{\text{text}}^{k}\}_{k=1}^{K}$，输出特征 $f_{out}$ 为各文本独立注意力结果的求和：

$$f_{out} = \sum_{k=1}^{K} \mathbf{MaskedMHA}\left( f_{in}, c_{\mathrm{text}}^{k}, \Omega_{k} \right)$$

其中 $\mathbf{MaskedMHA}$ 为带掩码的多头注意力，掩码 $\Omega_k$ 是一个二值矩阵，定义为：

$$\Omega_{k}(i,j) = \begin{cases} 1 & \text{if } i \text{ is within time window of text } k \\ 0 & \text{otherwise} \end{cases}$$

该机制确保第 $k$ 条文本仅在其指定的时间窗口内影响运动特征，从而支持“先走、再跑、最后跳跃”等多阶段文本控制，避免了传统拼接或全局交叉注意力带来的时序语义混淆。

### 双模式训练范式

GENMO 的核心创新在于**双模式训练**，将回归式的运动估计与扩散式的运动生成统一在同一去噪网络 $\mathcal{G}$ 中。

**生成模式**遵循标准扩散训练，从真实运动 $x_0$ 前向加噪得到 $x_t$，训练网络从 $x_t$ 预测干净运动 $x_0$：

$$\mathcal{L}_{\mathrm{gen}} = \mathbb{E}_{t \sim [1, T], x_t \sim q(x_t | x_0)} \left[ \| x_0 - \mathcal{G}(x_t, t, \mathcal{C}, \mathcal{M}) \|^2 \right]$$

**估计模式**则输入纯高斯噪声 $z \sim \mathcal{N}(\mathbf{0}, I)$ 和最大扩散时间步 $T$，强制网络执行最大似然估计，直接输出确定性预测：

$$\mathcal{L}_{\mathrm{est}} = \mathbb{E}_{z \sim \mathcal{N}(\mathbf{0}, I)} \left[ \| x_0 - \mathcal{G}(z, T, \mathcal{C}, \mathcal{M}) \|^2 \right]$$

两种模式根据条件信号的确定性程度进行选择：视频和 2D 骨架等强约束条件同时启用双模式，使模型既能精确重建又能保持生成多样性；文本和音乐等弱约束条件仅使用生成模式，保留运动的随机性。Figure 4 的定性分析验证了这一设计：视频条件模型在 50 步 DDIM 去噪中的中间预测高度一致，且对不同初始噪声不敏感；文本条件模型则展现出显著更大的预测方差。

### 估计引导的 2D 训练

为利用大规模 2D 标注视频数据，GENMO 引入**估计引导的 2D 训练损失**。先通过估计模式生成伪 3D 干净运动 $\hat{x}_0$，再对其前向加噪得到 $\hat{x}_t$，最后通过 2D 重投影损失监督生成过程：

$$\mathcal{L}_{\mathrm{gen-2D}} = \mathbb{E}_{\hat{x}_t \sim q(\hat{x}_t | \hat{x}_0), t \sim [1, T]} \left[ \| x_{2\mathrm{d}} - \Pi(\mathcal{G}(\hat{x}_t, t, \mathcal{C})) \|^2 \right]$$

其中 $\Pi$ 为 2D 投影函数。该损失将估计模式的确定性输出作为生成模式的训练桥梁，使模型能够从仅含 2D 标注的视频数据中学习运动先验，消融实验（Table 6）证实去除该损失会导致运动中间帧生成质量下降。

## 实验与关键发现

### 主实验结果

#### 全局人体运动估计

GENMO 在包含动态相机运动的全局运动估计任务上超越了专用方法。在 EMDB‑2 数据集上，GENMO 与 DROID‑SLAM 组合取得 **W‑MPJPE100 202.1 mm**，显著优于 **TRAM**（Wang et al., ECCV 2024）的 222.4 mm（Table 1）。在 RICH 数据集上，GENMO 的 WA‑MPJPE100 为 75.3 mm，同样优于 **GVHMR** 的 78.8 mm。所有对比方法均使用相同的 DROID‑SLAM 系统和特征提取器，保证了公平性。这一优势来源于统一的重力视角运动表示和双模式训练范式：估计模式迫使模型从纯噪声中一步回归精确运动，而生成模式提供的扩散先验则增强了动态相机下全局轨迹的合理性。

#### 局部运动估计

在摄像机坐标系下的局部运动估计中，GENMO 在 3DPW、RICH、EMDB‑1 三个标准基准上达到或超越 SOTA。具体地，在 3DPW 上 GENMO 取得 **PA‑MPJPE 34.6 mm**，相比 **CLIFF** 的 43.0 mm 降低了 8.4 mm（Table 2）。在 RICH 和 EMDB‑1 上，PA‑MPJPE 分别为 39.1 mm 和 42.5 mm，均处于领先水平。值得注意的是，GENMO 作为一个通用模型，并未针对任一数据集进行独立调优，其统一框架下估计与生成任务的协同训练是性能提升的关键。

#### 严重遮挡下的运动估计

在 3DPW‑XOCC 严重遮挡基准上，GENMO 的 MPJPE 达到 **76.2 mm**，较 NIKI temporal 的 88.9 mm 降低了 12.7 mm（Table 9）。这一结果直接验证了生成先验对遮挡鲁棒性的因果作用：去除生成模式、仅保留回归训练的变体 MPJPE 升至 89.0 mm，性能大幅退化。扩散模型的多模态生成能力在观测信号稀疏时提供了合理的运动补全，使估计结果更符合人体运动学规律。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2505_01425/figures/013_Table_9.jpg]]
*Table 9: Benchmark of Human Motion Generation. Motion quality is evaluated on the 3DPW-XOCC [40] dataset*

#### 音乐到舞蹈生成

在 AIST++ 数据集上，通用模型 GENMO 在物理合理性（PFC）、节拍对齐（BAS）和多样性指标上超越了专用舞蹈生成方法 **EDGE**（Tseng et al., CVPR 2023）（Table 3）。这表明跨任务联合训练产生了正向迁移：估计任务中学习到的精确运动动力学约束，有助于生成更符合物理规律的舞蹈序列，而多样化的音乐‑运动配对数据则提升了生成的表现力。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2505_01425/figures/007_Table_3.jpg]]
*Table 3: Benchmark of Music-to-Dance Generation. Motion quality is evaluated on the AIST++ [42] dataset*

#### 文本到运动生成

在 HumanML3D 和 Motion‑X 数据集上，GENMO 与 **MDM**（Tevet et al., ICLR 2023）等专用文本到运动模型相比，在 FID、R‑Precision 和多样性等指标上表现具有竞争力（Table 4、Table 5）。需要指出的是，由于 GENMO 采用 SMPL 参数化表示，与 HumanML3D 的原生关节表示存在差异，在格式转换过程中可能引入固有表达力损失，因此在该数据集的特定指标上并非全面领先；这属于表示空间差异带来的系统性偏差，而非模型能力不足。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2505_01425/figures/008_Table_4.jpg]]
*Table 4: Benchmark of Text-to-Motion Generation on the HumanML3D [17] dataset. R@3 denotes R-Precision (Top 3)*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2505_01425/figures/009_Table_5.jpg]]
*Table 5: Benchmark of Text-to-Motion Generation. Motion quality is evaluated on the Motion-X [44] dataset*

---

### 消融实验

#### 双模式训练的必要性

Table 7 对比了三种训练策略：纯扩散（DDPM baseline）、纯回归（regression baseline）和完整的双模式训练。在 RICH 全局运动估计上，纯扩散训练的 W‑MPJPE 从完整模型的 81.3 mm 升至 88.9 mm，性能显著下降。这证明**估计模式**对精确重建不可或缺——它通过零噪声输入和最大时间步强制模型学习最大似然估计，避免了扩散采样的随机性对确定性估计任务的损害。反之，纯回归模型在生成任务上完全失效，因为其丧失了多样性产出能力。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2505_01425/figures/012_Table_7.jpg]]
*Table 7: Ablation studies on motion estimation. The DDPM baseline is the proposed method without the estimation objective, only using the standard diffusion objective for training. The regression baseline is the proposed method without the generation objective*

#### 估计引导的 2D 训练

去除估计引导的 2D 训练损失 $\mathcal{L}_{\mathrm{gen-2D}}$ 后，运动中间帧生成质量下降。在 HumanML3D 的 2‑Keyframe 设置下，PA‑MPJPE 从 53.5 增加到 56.4（Table 6）。这验证了以下因果链条：估计模式从视频数据中产生伪 3D 运动，再通过扩散过程的 2D 重投影损失将 2D 标注中的运动先验注入生成分支，从而提升生成质量。仅依赖 3D 标注数据的纯扩散基线（DDPM baseline）性能最差，进一步证实了 2D 数据利用的增益。


#### 推理步数的影响

Table 8 展示了推理步数对估计和生成任务的不同影响。运动估计质量在 **5 个 DDIM 步**时达到最优，更多步数反而因随机性引入导致精度轻微下降；而文本到运动的 FID 随步数增加持续改善，在 **50 步**时达到最佳。这一差异源于两类任务对确定性的不同需求：估计任务受益于极少步数的近似确定性推理，生成任务则需要充分的多步去噪以产生高质量样本。GENMO 在 5 步时即可兼顾两者，验证了双模式训练使统一模型能在共享推理配置下同时服务两类任务。

---

### 失败模式与局限

1. **表示空间差异导致的指标劣势**：在文本到运动任务中，SMPL 参数化与 HumanML3D 原生关节表示之间的转换会引入误差，使得 GENMO 在该数据集的特定指标上可能低于专门针对该表示优化的方法。这不是模型生成能力的真实反映，而是评估协议的不匹配。

2. **对外部 SLAM 的依赖**：当前全局运动估计依赖 DROID‑SLAM 提供相机参数，未端到端集成。在极端相机运动或特征稀疏场景下，SLAM 的失效会直接传导至运动估计结果，构成系统的单点故障。

3. **精细运动覆盖不足**：模型未显式建模面部表情和手指动作，无法覆盖全身动画的完整需求。在需要精细手部交互或表情同步的应用中，GENMO 的表示空间需要扩展。

4. **稀有动作的生成多样性**：训练数据虽覆盖多种来源，但仍偏向工作室环境和常见动作类型。对于极端稀有或高动态动作（如特技翻滚），生成结果的物理合理性和多样性可能受限。

## 定位与知识库关联

### 1. 统一范式：从“估计-生成分离”到“条件生成统一”

传统人体运动理解领域长期存在一道鸿沟：运动估计任务追求精确、确定性的3D重建，而运动生成任务需要多样化、随机性的输出。这一根本矛盾导致两个子领域各自发展出独立的专用模型——估计侧以回归网络为主（如**GVHMR**、**CLIFF**），生成侧则依赖扩散模型（如**MDM**，Tevet et al., ICLR 2023；**EDGE**，Tseng et al., CVPR 2023）。这种分离带来两个深层代价：运动表示和先验知识无法跨任务共享，且单一模型难以同时满足精确重建与灵活多模态条件控制的需求。

GENMO通过一个核心洞察打破这一壁垒：**将运动估计重新定义为条件运动生成**。在这一视角下，估计不再是独立的回归问题，而是生成过程的一个特例——当条件信号（如视频帧）足够强时，生成空间被压缩为近似确定性映射。这一范式转换的关键技术杠杆是**双模式训练**：估计模式下输入纯高斯噪声与最大扩散时间步$T$，强制模型执行最大似然估计（损失$\mathcal{L}_{\mathrm{est}}$）；生成模式则保持标准扩散训练（损失$\mathcal{L}_{\mathrm{gen}}$），保留输出的多样性。两种模式根据条件确定性动态选择——视频和2D骨架等强条件同时启用双模式，文本和音乐等弱条件仅用生成模式。

这种统一带来的因果效益是双向的：生成先验改善了遮挡等困难场景下的估计鲁棒性（3DPW-XOCC上MPJPE从89.0降至76.2，Table 9），而大规模视频数据上的估计训练又提升了生成任务的表现力（Table 6中去除2D训练后PA-MPJPE从53.5升至56.4）。

### 2. 与专用方法的对比定位

**全局运动估计**方面，GENMO在EMDB-2数据集上W-MPJPE达到202.1 mm，显著优于专用方法**TRAM**（Wang et al., ECCV 2024）的222.4 mm（Table 1）。值得注意的是，两者使用相同的DROID-SLAM系统和特征提取器，性能增益直接归因于统一的生成-估计框架，而非更强的视觉前端。

**局部运动估计**方面，GENMO在3DPW上PA-MPJPE为34.6 mm，优于**CLIFF**的43.0 mm（Table 2），在RICH和EMDB-1上也达到SOTA水平。这表明通用模型并未因多任务训练而牺牲单任务精度，反而通过跨任务知识共享获得了增益。

**音乐到舞蹈生成**方面，GENMO在物理合理性（PFC）、节拍对齐（BAS）和多样性指标上超越了专用模型**EDGE**（Tseng et al., CVPR 2023），展示了从估计任务向生成任务的正向迁移（Table 3）。

**文本到运动生成**方面，GENMO与**MDM**（Tevet et al., ICLR 2023）等专用扩散模型竞争。需注意，由于GENMO采用SMPL参数化，与HumanML3D数据集的原生表示存在差异，在该数据集的特定指标上可能处于劣势，这属于表示层面的固有差异而非模型能力不足。

### 3. 适用边界与局限

1. **相机运动依赖外部系统**：当前GENMO的相机参数依赖外部SLAM系统（如DROID-SLAM）提供，尚未端到端集成。在复杂相机运动或SLAM失效场景下，全局运动估计的鲁棒性可能受限。

2. **运动表示的覆盖范围**：模型采用SMPL参数化，未显式处理面部表情、手指动作等精细运动，尚未覆盖全身完整的动画表达需求。对于需要手部交互或面部情感传达的应用场景，需额外模块补充。

3. **训练数据偏向**：尽管训练数据覆盖多种来源，仍可能偏向工作室环境或特定动作类型。对极端稀有动作（如高难度体操、杂技）的生成多样性可能有限，这一点在论文中未提供充分的分布外测试证据。

4. **多模态控制的粒度**：虽然多文本注意力块支持多文本、多时间段的控制，但各模态对最终运动的贡献缺乏精确的量化机制，用户难以获得细粒度的混合控制接口。

### 4. 开放问题

1. **端到端相机运动估计**：如何将相机运动估计直接集成到GENMO框架中，实现完全自监督的端到端全局运动估计，消除对外部SLAM的依赖？

2. **精细运动扩展**：如何将运动表示扩展到面部表情和手指动作，使通用模型覆盖全身动画需求，同时不损害现有任务的性能？

3. **规模化半监督训练**：统一的估计-生成范式为利用海量未标注视频提供了天然框架——估计模式可为未标注视频生成伪3D标签，生成模式则可从中学习运动先验。如何在真实场景中实现这一闭环的规模化训练？

4. **条件贡献量化**：在多模态混合条件下，如何量化各条件信号对最终运动的贡献权重，并为用户提供更直观、更细粒度的控制接口？

## 原文 PDF

![[paperPDFs/ICCV_2025/GENMO_A_GENeralist_Model_for_Human_MOtion.pdf]]
