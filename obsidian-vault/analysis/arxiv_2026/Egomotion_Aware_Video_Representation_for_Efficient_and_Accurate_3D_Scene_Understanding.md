---
title: Egomotion-Aware Video Representation for Efficient and Accurate 3D Scene Understanding
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Egomotion_Aware_Video_Representation_for_Efficient_and_Accurate_3D_Scene_Understanding.pdf
project_link: null
code_link: null
aliases:
- MM
- EAVREA3SU
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 引入自我运动（IMU）数据作为额外模态，为视觉观察提供物理运动轨迹的度量信息，并通过级联运动-视觉关键帧筛选与不对称交叉模态融合将该信息有效地整合进MLLM。
primary_logic: 与人类通过身体运动感知空间类似，IMU记录的相机运动轨迹能够为视觉场景提供绝对尺度和空间关系的基础，从而在不使用显式3D重建的情况下实现精确的3D理解。
claims:
- Motion-MLLM在VSI-Bench上达到58.2平均分，比当时最佳模型VG LLM-8B（50.7）提升7.5分，且在六个子任务上领先。
- 消融实验表明，移除IMU编码器（VGGT-only）导致ScanQA EM下降3.9%，SQA3D EM下降2.6%，确认自运动信息的必要性。
- 在ScanRefer视觉接地上，Motion-MLLM以61.4% Acc@0.25超越所有2D输入模型，并超过部分3D输入模型如Video-3D LLM（58.1），表明自运动增强有助于精确3D定位。
- 在真实IMU数据（TUM-VI）上，Motion-MLLM取得49.0平均分，比最佳基线VG LLM-4B提高9.1分，证明对真实传感器噪声的鲁棒性。
---

# Egomotion-Aware Video Representation for Efficient and Accurate 3D Scene Understanding

> [!tip] 核心洞察
> 与人类通过身体运动感知空间类似，IMU记录的相机运动轨迹能够为视觉场景提供绝对尺度和空间关系的基础，从而在不使用显式3D重建的情况下实现精确的3D理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向高效准确三维场景理解的自我运动感知视频表示 |
| 英文题名 | Egomotion-Aware Video Representation for Efficient and Accurate 3D Scene Understanding |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.17980) · [paper](https://arxiv.org/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Motion-MLLM |
| Dataset | ScanQA, SQA3D, VSI-Bench, ScanRefer |

> [!tip] 效果简介
> - ScanQA 上，CIDEr 100.4 vs Spatial-MLLM 91.8 (+8.6)。
> - SQA3D 上，EM@1 60.2 vs Spatial-MLLM 55.9 (+4.3)。
> - VSI-Bench 上，平均分 58.2 vs VG LLM-8B 50.7 (+7.5)。

## 概要

### 问题背景

当前多模态大语言模型（MLLM）在三维场景理解中面临一个根本性两难：依赖显式三维表示（点云、深度图）的方法虽然精度较高，但传感器成本昂贵且计算开销巨大；而仅使用二维视频输入的方法虽轻量，却无法可靠恢复度量尺度，导致距离估计与尺寸判读存在严重歧义。这种“精度‑效率”的张力构成了该领域的核心瓶颈。

### 核心洞察

本文的核心洞察源自人类空间感知的基本机制：人类通过身体运动感知空间，身体的位移轨迹为视觉观察提供了绝对尺度和空间关系的基础。类比于此，**自我运动（egomotion）数据**——即由惯性测量单元（IMU）记录的相机六轴运动轨迹——能够为二维视频提供度量信息锚点，从而在不依赖显式三维重建的前提下实现精确的三维理解。

### 方法定位

基于上述洞察，本文提出 **Motion‑MLLM** 框架，将自我运动作为显式输入模态引入 MLLM。该方法在方法谱系中位于“纯二维输入”与“显式三维输入”之间，以极低的传感器成本换取接近三维方法的精度。其两个关键设计槽位为：

- **级联运动‑视觉关键帧筛选**：通过“IMU 运动门控 → 视差过滤 → 视觉余弦距离”三级渐进式筛选，高效选取信息丰富的关键帧，取代传统的均匀采样或纯视觉最大覆盖采样。
- **不对称跨模态融合**：将变长 IMU 段经 GRU 编码为固定长度运动标记，再通过“双向交叉注意力 + 单向交叉注意力”两层融合，产生自运动增强的视觉标记，使 LLM 能隐式感知相机运动轨迹与场景几何的关联。

### 主要结果

在多个三维场景理解基准上，Motion‑MLLM 以约 4B 参数规模取得显著提升：

- **空间推理**：在 VSI‑Bench 上达到 58.2 平均分，较当时最佳模型 **VG LLM‑8B**（50.7）提升 7.5 分，且在全部六个子任务上领先。
- **问答与接地**：在 ScanQA 上 CIDEr 达 100.4（+8.6），SQA3D 上 EM@1 达 60.2%（+4.3）；在 ScanRefer 视觉接地上以 61.4% Acc@0.25 超越所有二维输入模型，并超过部分三维输入模型如 **Video‑3D LLM**（58.1）。
- **效率与鲁棒性**：在同等精度下，推理速度比当时最佳的二维和三维方法分别快 1.30× 和 1.61×；在真实 IMU 数据（TUM‑VI）上取得 49.0 平均分（+9.1），验证了对传感器噪声的鲁棒性。

消融实验进一步确认了自我运动信息的必要性：移除 IMU 编码器导致 ScanQA EM 下降 3.9%，SQA3D EM 下降 2.6%；而级联运动‑视觉筛选和不对称融合设计分别对精度和效率有独立贡献。

### 局限与展望

方法目前主要依赖仿真 IMU 数据训练，仅在 TUM‑VI 小规模真实数据上验证；关键帧筛选阈值为手工设定，尚未实现端到端学习；在计数类问题（How）上提升有限。未来可扩展至户外动态场景，并探索与深度估计网络互补、多传感器融合、端到端阈值学习等方向。

### 3D空间推理的核心瓶颈

多模态大语言模型（MLLM）在三维场景理解中面临一个根本性两难。一方面，依赖显式3D表示——点云、深度图或体素——的方法能够提供精确的度量信息，但成本高昂：获取这些表示需要昂贵的深度传感器或密集重建管线，且处理大规模3D数据对计算和存储的要求远高于2D图像。另一方面，仅使用2D视频作为输入的方法虽然经济高效、传感器要求低，却无法可靠地恢复场景的度量尺度——从单目视频中推断绝对距离和物体尺寸本质上是一个病态问题，导致模型在距离判读、尺寸比较等空间推理任务上产生歧义。

这一瓶颈的本质在于：2D视觉信号缺乏将像素级外观与物理世界的度量空间联系起来的“锚点”。现有方法要么牺牲效率换取精度（3D路线），要么牺牲精度换取通用性（2D路线），始终无法在两者之间找到令人满意的平衡。

### 人类的启示：身体运动作为空间感知的锚

人类在陌生环境中理解空间关系时，并不依赖显式的三维重建。我们通过**身体运动**——行走、转头、靠近或远离物体——自然地建立起对场景尺度和空间布局的感知。当我们走向一扇门时，脚步的移动距离和视角的变化共同告诉我们门有多远、有多大。这种“运动中的感知”将视觉观察与物理运动轨迹紧密结合，为空间理解提供了度量基础。

受此启发，本文提出一个关键洞察：**惯性测量单元（IMU）记录的相机自我运动轨迹，可以为视觉场景提供绝对尺度和空间关系的基础**，从而在不使用显式3D重建的情况下实现精确的3D理解。现代移动设备（手机、AR眼镜、机器人平台）普遍配备6轴IMU（加速度计和陀螺仪），能够以极低的成本提供相机的平移和旋转信息——这正是2D视频所缺失的度量锚点。

### 现有方法的缺口

当前MLLM在3D空间推理上的代表性方法可分为三类：

- **3D输入方法**（如**LLaVA-3D**、**Video-3D LLM**）：将点云或深度图作为输入，精度较高但依赖专门的3D传感器或重建步骤，部署成本高。
- **2D输入方法**（如**Qwen2.5-VL-3B**、**Spatial-MLLM**）：仅使用视频帧作为输入，通用性强但缺乏度量尺度信息，在需要精确距离或尺寸判断的任务上表现受限。
- **视频+文本方法**（如**VG LLM-8B**）：在2D视频基础上引入语言引导的视觉接地，但仍无法解决根本的尺度歧义问题。

这些方法的共同缺陷在于：**忽视了相机自身运动所携带的丰富空间信息**。IMU数据作为同步于视频的“免费”信号，在现有MLLM框架中几乎未被利用。

### 本文的动机与目标

本文旨在填补这一空白，提出**Motion-MLLM**框架，核心思想是：将IMU自我运动数据作为额外的输入模态，通过专门设计的融合机制将其整合进MLLM，使模型能够像人类一样“通过运动感知空间”。具体而言，本文致力于回答以下问题：

1. **如何高效地从长视频流中筛选信息丰富的关键帧？** 引入级联运动-视觉关键帧筛选策略，利用IMU信号快速剔除冗余帧，再将计算资源集中于视觉上重要的帧。
2. **如何将变长的IMU序列与视觉标记有效融合？** 设计不对称交叉注意力融合模块，使运动信息能够跨帧引导视觉特征的整合，而非简单的拼接。
3. **在仅使用仿真IMU数据训练的情况下，模型能否泛化到真实传感器噪声？** 通过构建逼真的IMU噪声模型，并在真实IMU数据集上验证鲁棒性。

通过这三个层面的创新，Motion-MLLM旨在以接近2D方法的效率，实现媲美甚至超越3D方法的空间推理精度，为低成本、高精度的3D场景理解开辟新路径。

## 核心方法与创新机理

Motion-MLLM的核心创新在于将**自我运动（egomotion）**作为显式输入模态引入多模态大语言模型（MLLM），以极低的传感器成本（仅需消费级IMU）弥合纯2D视觉与度量3D理解之间的鸿沟。其创新体系围绕三个紧密耦合的**changed slots**展开。

### 1. 输入模态的范式转换：从2D视频到自运动增强视频

现有MLLM在3D空间推理中面临两难：依赖点云或深度图的3D输入方法（如**Video-3D LLM**、**LLaVA-3D**）成本高且传感器要求昂贵，而纯2D视频方法（如**Spatial-MLLM**、**VG LLM-8B**）虽轻量却无法可靠恢复度量尺度，导致距离与尺寸判读歧义。Motion-MLLM打破这一僵局，引入同步IMU数据（6轴加速度计/陀螺仪）作为视频流的伴随模态。这一设计的核心洞察在于：**与人类通过身体运动感知空间类似，IMU记录的相机运动轨迹能够为视觉场景提供绝对尺度和空间关系的基础**，从而在不使用显式3D重建的情况下实现精确的3D理解。

### 2. 级联运动-视觉关键帧筛选：效率与信息的联合优化

传统关键帧选择策略（均匀采样或纯视觉最大覆盖采样）忽视了相机运动本身的信息价值。Motion-MLLM提出**三阶段级联筛选**（Sec. 3.1），将计算量从轻到重逐级过滤：

- **阶段1——运动门控**：基于IMU积分计算帧间平移距离 $d(\hat{f}_j, f_t)$ 和旋转角度 $\theta(\hat{f}_j, f_t)$，仅当两者均超过阈值 $\tau_d$、$\tau_\theta$ 时保留候选帧。这一轻量级检查以近乎零成本过滤静态或微动片段。
- **阶段2——视差检查**：利用VGGT几何编码器估计的帧间视差，进一步剔除纯旋转等不带来新几何信息的运动。
- **阶段3——视觉多样性筛选**：对通过前两阶段的候选帧，计算其视觉标记与上一关键帧的余弦距离，仅当 $\text{cosine distance}(\mathbf{v}_t, \mathbf{v}_j) > \tau_v$ 时选为关键帧。

消融实验证实了这一设计的有效性：**纯视觉筛选（Visual-based Sampling）在SQA3D上EM为59.0%，而完整MV筛选达到60.2%**（Tab. 6），说明运动门控能进一步过滤视觉相似但空间位置不同的冗余帧。效率对比（Tab. 5）显示，MV筛选在ScanQA上以1.02 s⁻¹的成本效益比（CE）显著优于最大覆盖采样的0.67 s⁻¹。

### 3. 不对称交叉模态融合：从简单拼接走向运动引导的视觉增强

现有方法将多模态特征简单拼接后送入MLP或LLM，忽视了模态间的信息流向不对称性——**运动信息应作为空间上下文引导视觉特征，而非与视觉特征对等交互**。Motion-MLLM设计了独特的**两阶段不对称交叉注意力融合**（Sec. 3.2.2，Fig. 3）：

- **第一层——双向融合**：视觉标记 $\mathbf{V}$ 与运动标记 $\mathbf{M}$ 通过交叉注意力相互查询，各自注入对方信息：

$$\mathbf{V}' = \mathbf{V} + \mathrm{FFN}(\mathrm{Attn}(\mathbf{V}W_Q^v, \mathbf{M}W_K^m, \mathbf{M}W_V^m))$$
$$\mathbf{M}' = \mathbf{M} + \mathrm{FFN}(\mathrm{Attn}(\mathbf{M}W_Q^m, \mathbf{V}W_K^v, \mathbf{V}W_V^v))$$

- **第二层——单向融合**：增强后的视觉标记 $\mathbf{V}'$ 作为查询，从运动标记 $\mathbf{M}'$ 中提取空间上下文，产生最终的自运动增强视觉标记：

$$\bar{\mathbf{V}} = \mathbf{V}' + \mathrm{FFN}(\mathrm{Attn}(\mathbf{V}'\mathbf{W}_Q, \mathbf{M}'\mathbf{W}_K, \mathbf{M}'\mathbf{W}_V))$$

这一设计的非对称性体现在：运动标记在第二层仅作为键值对提供信息，不再被更新，确保运动信息单向注入视觉表征。消融实验（Tab. 6）给出了决定性证据：**不对称融合相比Concat+MLP基线在ScanQA上EM提高10.6%（29.8% vs 19.2%）**，验证了跨帧运动引导的信息传递机制远优于简单拼接。

### 创新协同效应

上述三个changed slots形成协同增益闭环：级联筛选以运动感知方式精选关键帧，减少冗余帧对融合模块的干扰；不对称融合则充分利用筛选后的运动标记，将IMU轨迹转化为视觉特征的空间上下文。当移除IMU编码器（VGGT-only配置）时，ScanQA EM从29.8%骤降至25.9%（-3.9%），SQA3D EM从60.2%降至57.6%（-2.6%）（Tab. 6），确认自运动信息是整个创新体系的必要条件而非锦上添花的辅助信号。

Motion-MLLM 的整体设计遵循一个清晰的逻辑：将自我运动（egomotion）作为显式模态引入多模态大语言模型，使模型在不依赖显式3D重建的前提下获得度量空间感知能力。如图2所示，系统接收两路同步输入——2D视频流与IMU数据（6轴加速度计/陀螺仪），经过级联筛选、编码与融合后，由LLM骨干生成最终的空间理解响应。

### 输入与预处理

系统输入为一组同步的RGB视频帧 $\{f_1, f_2, \ldots, f_T\}$ 及对应的IMU测量序列。IMU数据记录了相机在三维空间中的平移加速度与旋转角速度，为后续的度量推理提供物理运动轨迹。由于原始视频帧数量庞大且存在大量冗余，直接全部输入LLM将导致计算开销不可接受。

### 级联运动-视觉关键帧筛选

为高效压缩视频流，Motion-MLLM 设计了**级联运动-视觉关键帧筛选模块**（Sec. 3.1），采用由轻到重的三阶段渐进式过滤策略：

- **阶段一（运动门控）**：利用IMU数据计算相邻帧间的平移距离 $d(\hat{f}_j, f_t)$ 和旋转角度 $\theta(\hat{f}_j, f_t)$，当两者均低于阈值 $\tau_d$ 和 $\tau_\theta$ 时直接丢弃该帧。此阶段计算量极轻，可快速过滤静止或微小运动片段。
- **阶段二（视差过滤）**：对通过运动门控的候选帧，利用VGGT几何编码器提取的深度信息计算帧间视差，进一步排除视觉变化不显著的帧。
- **阶段三（视觉筛选）**：对剩余候选帧，计算其视觉标记与上一个关键帧视觉标记的余弦距离 $\text{cosine distance}(\mathbf{v}_t, \mathbf{v}_j)$，仅当距离超过阈值 $\tau_v$ 时才将其选为关键帧。

这种级联设计使得计算密集的视觉分析仅作用于少量候选帧，在保证信息覆盖的同时大幅降低计算成本。

### 双路编码

筛选后的 $N$ 个关键帧分别进入两条编码通路：

1. **视觉编码**：关键帧图像经 Qwen2.5-VL 的2D视觉编码器与 VGGT 几何编码器处理，产生视觉标记 $\mathbf{V} = \{\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_N\}$，同时捕获外观与几何线索。
2. **运动编码**：相邻关键帧之间的IMU片段由 GRU 运动编码器处理，取最终隐藏状态作为运动标记 $\mathbf{M} = \{\mathbf{m}_1, \mathbf{m}_2, \ldots, \mathbf{m}_N\}$，每个运动标记浓缩了对应帧间累积的自我运动信息。

### 不对称交叉模态融合

视觉标记与运动标记进入**不对称交叉注意力融合模块**（Sec. 3.2.2，图3），通过两层交叉注意力实现信息整合：

- **第一层（双向融合）**：视觉标记与运动标记相互查询。视觉标记以运动标记为键值注入运动信息，运动标记以视觉标记为键值注入视觉上下文，两者均经残差连接与FFN更新：

$$\mathbf{V}' = \mathbf{V} + \mathrm{FFN}(\mathrm{Attn}(\mathbf{V}W_Q^v, \mathbf{M}W_K^m, \mathbf{M}W_V^m))$$
$$\mathbf{M}' = \mathbf{M} + \mathrm{FFN}(\mathrm{Attn}(\mathbf{M}W_Q^m, \mathbf{V}W_K^v, \mathbf{V}W_V^v))$$

- **第二层（单向融合）**：仅视觉标记查询运动标记，产生最终的自运动增强视觉标记：

$$\bar{\mathbf{V}} = \mathbf{V}' + \mathrm{FFN}(\mathrm{Attn}(\mathbf{V}'W_Q, \mathbf{M}'W_K, \mathbf{M}'W_V))$$

这种“双向→单向”的不对称设计确保运动信息有效注入视觉表示，同时避免视觉特征对运动标记的过度扰动。

### LLM解码

融合后的自运动增强视觉标记 $\bar{\mathbf{V}}$ 与文本指令的嵌入拼接，送入 Qwen2.5-3B LLM 骨干进行自回归解码，生成最终的文本响应。整个框架中，2D视觉编码器与LLM骨干保持冻结，仅 GRU 运动编码器、交叉注意力融合模块和投影层参与训练，参数量约4.3B。

### 效率特性

级联筛选与轻量运动编码的设计使 Motion-MLLM 在精度与效率间取得有利权衡。如表5所示，采用运动-视觉联合筛选（MV Filtering）相比最大覆盖采样（MC），在 ScanQA 上以更低的端到端延迟 $T$ 获得了更高的 CIDEr 得分，成本效益指标 CE 达到 1.02 s⁻¹，显著优于 Spatial-MLLM 的 0.67 s⁻¹。

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2603_17980/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of Motion-MLLM. The \ and icons indicate trainable and frozen modules, respectively*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2603_17980/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of (a) 3D-input, (b) 2D-input, and (c) our egomotion-input approaches for spatial reasoning in MLLMs*

Motion-MLLM 的核心架构由三个关键模块构成：级联运动-视觉关键帧筛选、GRU 运动编码器、以及不对称交叉注意力融合模块。这三个模块协同工作，将同步的 2D 视频流与 IMU 数据转化为自运动增强的视觉标记，供 LLM 骨干进行 3D 空间推理。

### 级联运动-视觉关键帧筛选

该模块采用三阶段渐进式过滤策略，从轻量级的运动检查逐步过渡到计算密集的视觉特征分析，以高效选取信息丰富的关键帧。

**第一阶段：运动门控。** 对于当前候选帧 $f_t$，计算其与上一个已选关键帧 $\hat{f}_j$ 之间的平移距离和旋转角度。当两者均低于预设阈值时，该帧被直接丢弃：

$$d(\hat{f}_j, f_t) < \tau_d \text{ and } \theta(\hat{f}_j, f_t) < \tau_\theta$$

其中 $d(\cdot)$ 为帧间平移距离，$\theta(\cdot)$ 为帧间旋转角度，$\tau_d$ 与 $\tau_\theta$ 分别为位移和角度阈值。这一阶段利用 IMU 积分得到的位姿信息，以极低的计算成本过滤掉相机近乎静止时的冗余帧。

**第二阶段：视差门控。** 对通过运动门控的帧，进一步计算其与上一关键帧之间的像素级视差，若视差低于阈值 $\tau_p$ 则丢弃。该阶段开始引入视觉几何信息，但计算量仍远低于完整特征提取。

**第三阶段：视觉关键帧选择。** 对通过前两阶段筛选的帧，使用 VGGT 几何编码器提取视觉标记 $\mathbf{v}_t$，计算其与上一关键帧视觉标记 $\mathbf{v}_j$ 的余弦距离。当距离超过阈值 $\tau_v$ 时，该帧被选为新的关键帧：

$$\text{cosine distance}(\mathbf{v}_t, \mathbf{v}_j) > \tau_v$$

此阶段确保只有视觉内容发生显著变化的帧才被保留，避免信息冗余。

### GRU 运动编码器

相邻关键帧之间的 IMU 数据段（包含 6 轴加速度计和陀螺仪测量值）长度可变。为将其转化为固定维度的运动标记，Motion-MLLM 采用 GRU 作为序列编码器。GRU 按时间步处理 IMU 序列，取其最终隐藏状态作为该段的运动标记 $\mathbf{m}_i$。这一设计使运动标记天然地总结了关键帧之间累积的相机自运动信息，包括平移轨迹和旋转变化。

### 不对称交叉注意力融合模块

该模块通过两层交叉注意力机制将视觉标记 $\mathbf{V}$ 与运动标记 $\mathbf{M}$ 融合，产生自运动增强的视觉标记 $\bar{\mathbf{V}}$。

**第一层：双向交叉注意力融合。** 视觉标记与运动标记相互查询，实现双向信息注入：

$$\mathbf{V}' = \mathbf{V} + \mathrm{FFN}(\mathrm{Attn}(\mathbf{V}W_Q^v, \mathbf{M}W_K^m, \mathbf{M}W_V^m))$$
$$\mathbf{M}' = \mathbf{M} + \mathrm{FFN}(\mathrm{Attn}(\mathbf{M}W_Q^m, \mathbf{V}W_K^v, \mathbf{V}W_V^v))$$

其中 $\mathrm{Attn}(\mathbf{Q}, \mathbf{K}, \mathbf{V})$ 为标准的多头交叉注意力，$\mathrm{FFN}$ 为前馈网络，$W_Q^v, W_K^m, W_V^m, W_Q^m, W_K^v, W_V^v$ 为可学习的投影矩阵。第一条公式使视觉标记从运动标记中获取空间位移的度量信息，第二条公式使运动标记从视觉标记中获取场景上下文。

**第二层：单向融合。** 经双向增强后的视觉标记 $\mathbf{V}'$ 再次查询运动标记 $\mathbf{M}'$，产生最终的自运动增强视觉标记：

$$\bar{\mathbf{V}} = \mathbf{V}' + \mathrm{FFN}(\mathrm{Attn}(\mathbf{V}'W_Q, \mathbf{M}'W_K, \mathbf{M}'W_V))$$

这种“双向→单向”的不对称设计确保了视觉标记在充分吸收运动信息的同时，保持对原始视觉内容的忠实性。消融实验证实，该设计相比简单的 Concat+MLP 融合方案在 ScanQA 上 EM 指标提升 10.6%（29.8% vs 19.2%），验证了跨帧运动引导信息传递机制的有效性（Tab. 6）。

## 实验与关键发现

### 核心实验设置

Motion-MLLM以Qwen2.5-VL-3B为骨架，总参数量约4.3B。视觉编码器沿用Qwen2.5-VL的2D编码器，几何编码器采用VGGT主干。训练混合ScanQA、SQA3D、ScanRefer、Scan2Cap四个ScanNet衍生数据集，每个batch随机采样单一任务类型以避免任务不平衡。所有对比方法在VSI-Bench等基准上均使用统一的关键帧筛选模块以保证公平；ScanRefer和Scan2Cap任务中使用与VG LLM一致的预提取对象建议。所有结果取三次不同随机种子运行的平均值，标准差在±0.5（EM/准确率）和±1.5（CIDEr）以内。

### 3D问答主结果

在ScanQA和SQA3D两个核心3D问答基准上，Motion-MLLM以仅2D视频+IMU的输入模态超越了所有2D输入方法，并在多个指标上达到或接近3D输入方法的水平（Table 1）。

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2603_17980/figures/004_Table_1.jpg]]
*Table 1: Evaluation Results on ScanQA [3] and SQA3D [42]. “2D”, “3D”, and “M” specify the model’s input type as 2D data, 3D data, and egomotion data, respectively*

**ScanQA**：Motion-MLLM取得CIDEr 100.4，比当时最佳2D基线Spatial-MLLM（91.8）提升+8.6，同时BLEU-4达到15.8，METEOR 20.3，ROUGE-L 48.0。这一结果甚至超过了部分使用点云输入的3D方法，表明自运动信息有效补偿了显式3D几何的缺失。

**SQA3D**：Motion-MLLM取得EM@1 60.2，比Spatial-MLLM（55.9）提升+4.3。按问题类型细分（Table 10），“What”类问题EM@1达62.5，“Which”类达63.1，但“How”类（计数类）提升有限，表明自运动线索对视觉统计任务的增益较弱。

### VSI-Bench空间推理

VSI-Bench包含八个空间推理子任务，全面评估距离判断、尺寸估计、方位推理等能力。Motion-MLLM取得平均分58.2，比当时最佳模型VG LLM-8B（50.7）提升+7.5，且在六个子任务上领先（Table 2）。值得注意的是，Motion-MLLM参数量仅约4B，而VG LLM-8B为8B，说明自运动模态的信息效率远高于单纯增大模型规模。

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2603_17980/figures/005_Table_2.jpg]]
*Table 2: Evaluation Results on VSI-Bench [60]. We follow the standard setting of VSI-Bench and utilize the keyframe filtering module to select frames for baselines and Motion-MLLM, respectively. Bold and underline denote the best and second-best results in each column, respectively*

### 真实IMU鲁棒性验证

为验证对真实传感器噪声的鲁棒性，在TUM-VI数据集（包含真实IMU记录）上进行了VSI-Bench子集评估（Table 3）。Motion-MLLM取得平均分49.0，比最佳基线VG LLM-4B（39.9）提升+9.1。这一结果表明，尽管模型主要在仿真IMU数据上训练（基于B样条轨迹微分和噪声模型合成），其对真实IMU的噪声特性具有良好的泛化能力。

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2603_17980/figures/006_Table_3.jpg]]
*Table 3: Real IMU validation on TUM-VI [49]. We follow the standard setting of VSI-Bench and utilize the keyframe filtering module to select frames for baselines and Motion-MLLM, respectively*

### 3D视觉接地与密集字幕

在ScanRefer视觉接地任务上（Table 4），Motion-MLLM以61.4% Acc@0.25（精炼后）超越所有2D输入模型，并超过部分3D输入模型如Video-3D LLM（58.1）。未精炼的Acc@0.25为33.7%，精炼后提升至61.4%，说明自运动增强的视觉特征为后续提议精炼提供了更准确的初始定位。在Scan2Cap密集字幕任务上，Motion-MLLM同样取得有竞争力的CIDEr 73.4，接近3D输入方法的水平。

### 效率与成本效益

Table 5展示了不同采样策略下的延迟-精度权衡。Motion-MLLM的运动-视觉关键帧筛选（MV Filtering）在ScanQA上以端到端耗时T=0.98s达到EM 29.8%，成本效益指标CE（EM/T）为1.02 s⁻¹，显著优于Spatial-MLLM的最大覆盖采样（MC，CE=0.67）。在SQA3D上同样以更低延迟实现更高精度。Figure 5的帕累托前沿进一步表明，Motion-MLLM在延迟-精度曲线上始终位于其他方法的左上方，验证了级联筛选策略的效率优势。

### 消融研究

Table 6的系统消融揭示了各组件的因果贡献：

**自运动信息的必要性**：移除IMU编码器（VGGT-only，即退化为Spatial-MLLM配置）导致ScanQA EM从29.8%降至25.9%（-3.9%），SQA3D EM从60.2%降至57.6%（-2.6%）。这是最直接的因果证据——在完全相同的视觉编码器和训练流程下，仅移除自运动分支就造成显著退化。

**级联筛选的有效性**：仅使用视觉关键帧筛选（Visual-based Sampling）的EM为26.8%/59.0%，低于完整MV筛选的29.8%/60.2%。这说明运动门控（Stage 1-2）能进一步过滤视觉冗余帧，保留对空间推理真正关键的运动边界帧。

**不对称融合设计的优势**：将视觉与运动标记简单拼接后经MLP映射（Concat+MLP）的EM仅为19.2%，而完整的不对称交叉注意力融合达到29.8%，提升高达10.6个百分点。这验证了双向→单向的跨帧运动引导信息传递机制是融合效率的关键——先让两模态相互注入信息，再让视觉单向查询运动，比简单拼接能更有效地将度量尺度信息绑定到视觉特征上。

### 失败模式与局限性

尽管整体表现优异，分析揭示了若干值得关注的边界：

1. **计数类问题的增益有限**：“How”类问题（如“房间里有几把椅子”）的提升幅度明显小于距离判断和方位推理，表明自运动提供的度量信息对视觉统计/计数任务的直接帮助有限——这类任务更依赖细粒度视觉识别而非空间关系推理。

2. **仿真到真实的泛化边界**：虽然TUM-VI验证显示了良好的鲁棒性，但该数据集规模有限且场景相对受控。模型未在大规模真实动态场景（如自动驾驶、手持设备自由移动）中测试，对多传感器异步、IMU缺失或校准误差等实际部署问题缺乏评估。

3. **关键帧阈值的手工设定**：级联筛选的门限（τ_d, τ_θ, τ_p, τ_v）为手工设定，虽经灵敏度分析验证鲁棒，但非自适应参数，在不同场景或传感器配置下可能需要重新调优。

4. **模型规模未充分探索**：当前仅基于~4B参数的LLM主干，未评估扩展到更大模型（如7B、13B）时的增益曲线，无法判断自运动信息的价值是否随模型容量增加而递减。

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2603_17980/figures/016_Figure_6.jpg]]
*Figure 6: Qualitative examples on ScanQA [3]*

## 定位与知识库关联

### 问题定位：2D与3D之间的“度量鸿沟”

现有MLLM在3D空间推理中面临一个结构性两难：依赖显式3D表示（点云、深度图）成本高昂且对传感器要求严格，而仅使用2D视频虽轻量却无法可靠恢复度量尺度，导致距离与尺寸判读存在根本性歧义。Motion-MLLM的核心洞察是：与人类通过身体运动感知空间类似，IMU记录的相机运动轨迹能够为视觉场景提供绝对尺度和空间关系的基础，从而在不使用显式3D重建的情况下实现精确的3D理解。这一思路将问题的因果调节旋钮从“更强的3D重建”转向“引入自运动作为度量锚点”，在2D输入的轻量性和3D输入的精度之间找到了一个新的平衡点。

### 方法谱系：在2D与3D基线之间开辟第三条路径

Motion-MLLM在现有方法谱系中占据了一个独特位置。从输入模态维度看，当前主流方法分为两大阵营：

**2D输入方法**以Qwen2.5-VL-3B为典型代表，直接使用视频帧作为输入，依赖大规模预训练的视觉编码器提取特征。Spatial-MLLM在此基础上引入了VGGT几何编码器以增强空间感知，VG LLM-8B则在视觉接地任务上达到当时最佳水平。这些方法的共同瓶颈在于缺乏度量尺度信息——视觉特征可以捕捉相对位置关系，但无法可靠推断绝对距离。

**3D输入方法**如Video-3D LLM和LLaVA-3D直接使用点云或深度图，天然具备度量精度，但面临传感器成本高、计算开销大、部署受限等问题。

Motion-MLLM开辟了第三条路径：以“2D视频+同步IMU”作为输入（标记为“M”模态），在保持2D输入轻量性的同时注入度量信息。这一设计使其在ScanQA上以100.4 CIDEr超越Spatial-MLLM（91.8）达+8.6，在VSI-Bench上以58.2平均分超越VG LLM-8B（50.7）达+7.5，同时在效率上达到Spatial-MLLM最大覆盖采样的1.52倍加速（Tab. 5，成本效益CE从0.67提升至1.02）。

### 核心技术创新：级联筛选与不对称融合

Motion-MLLM的两个关键技术组件分别解决了“用什么帧”和“怎么融合”的问题：

**级联运动-视觉关键帧筛选**（Sec. 3.1）采用三阶段渐进式过滤：第一阶段基于IMU位移和旋转角度的运动门控（$d(\hat{f}_j, f_t) < \tau_d$ 且 $\theta(\hat{f}_j, f_t) < \tau_\theta$ 时丢弃），第二阶段通过视差检查过滤静止帧，第三阶段基于VGGT视觉标记的余弦距离（$\text{cosine distance}(\mathbf{v}_t, \mathbf{v}_j) > \tau_v$）选择信息丰富帧。消融实验（Tab. 6）表明，相比纯视觉筛选（Visual-based Sampling），完整MV筛选在ScanQA EM上从26.8%提升至29.8%，在SQA3D EM上从59.0%提升至60.2%，验证了运动门控能进一步过滤冗余帧。

**不对称交叉注意力融合**（Sec. 3.2）先将变长IMU段通过GRU编码为固定长度运动标记，再经两层交叉注意力融合：第一层双向融合（Eq. 1）使视觉与运动标记相互查询，第二层单向融合（Eq. 2）让视觉标记查询运动标记以产生最终自运动增强视觉标记。消融实验（Tab. 6）显示，该设计相比简单的Concat+MLP基线在ScanQA EM上提升10.6%（29.8% vs 19.2%），验证了跨帧运动引导的信息传递机制的有效性。

### 适用边界与局限

**训练数据依赖**：方法主要依赖仿真IMU数据训练（基于B样条轨迹微分和噪声模型，Eq. 7-8），仅在TUM-VI小规模真实IMU数据上验证（Tab. 3，49.0平均分，+9.1超过VG LLM-4B），未在大规模真实动态场景中测试。仿真到真实的域迁移风险需要进一步评估。

**模型规模限制**：当前模型参数约4B（基于Qwen2.5-VL-3B + VGGT），未评估扩展到更大LLM主干（如7B、13B）时的增益与收益。考虑到更大模型可能具有更强的空间推理先验，自运动信息的边际贡献可能发生变化。

**任务类型偏置**：在计数类问题（How）上提升有限，表明自运动线索对视觉统计任务的增益较弱。这一现象暗示IMU提供的运动轨迹信息主要增强空间关系推理，而非视觉内容统计。

**阈值敏感性**：关键帧筛选阈值（$\tau_d$, $\tau_\theta$, $\tau_p$, $\tau_v$）为手工设定，虽经灵敏度分析验证鲁棒，但非自适应和可学习参数，在不同场景（室内vs室外、慢速vs快速运动）下可能需要重新标定。

**部署鲁棒性未验证**：未考虑多模态传感器异步、IMU数据缺失或校准误差等实际部署中的鲁棒性问题。当IMU数据完全缺失时，方法退化为VGGT-only配置（Tab. 6），ScanQA EM从29.8%降至25.9%（-3.9%）。

### 开放问题

1. **户外与动态场景扩展**：如何将框架扩展到户外、动态环境（如自动驾驶）并处理GPS、轮速计等多传感器融合？户外场景的尺度范围、运动模式和视觉复杂性都与室内ScanNet存在本质差异。

2. **与深度估计的互补性**：自运动数据能否与单目深度估计网络互补，进一步提升几何理解精度？IMU提供的绝对尺度信息恰好可以解决单目深度的尺度模糊问题。

3. **端到端学习**：可否将级联筛选的门限与融合权重联合学习，实现端到端优化？当前手工阈值限制了方法对不同数据分布的适应性。

4. **跨任务迁移**：自运动模态是否可提升其他多模态任务，如视觉-语言导航（VLN）和机器人操作？这些任务中运动轨迹本身就是决策的关键信号。

5. **自运动自举**：当IMU数据完全缺失时，能否通过视觉惯性推理自举生成虚拟自运动信号，使方法在纯视觉输入下仍保持部分度量感知能力？

## 原文 PDF

![[paperPDFs/arxiv_2026/Egomotion_Aware_Video_Representation_for_Efficient_and_Accurate_3D_Scene_Understanding.pdf]]
