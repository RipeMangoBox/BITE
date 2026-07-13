---
title: "Video-GPT via Next Clip Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Video_GPT_via_Next_Clip_Diffusion.pdf
project_link: null
code_link: null
openreview_forum_id: E0ZAcqy9TB
aliases:
- VG
- VGNCD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "引入“下一片段扩散”范式，将视频片段视为类词元的基本单元，在片段间采用自回归条件依赖，片段内进行并行扩散去噪，统一了长时上下文建模与高质量生成。"
primary_logic: "通过将视频划分为可变长度的片段，构建干净与带噪片段交织的输入序列，并采用片段级因果、帧级/块级双向的层级注意力掩码，Video-GPT能够以自监督方式学习预测下一片段，同时保留片段内并行扩散的生成优势。预训练仅依赖视频数据，无需文本标注，且通过渐进式训练从短到长视频逐步扩展能力。"
claims:
- "在Physics-IQ Benchmark上，Video-GPT取得34.97的Physics IQ Score，远超第二名的29.50 (VideoPoet)，提升超过5个百分点。"
- "消融实验表明，将训练范式从Next Token Prediction切换为Next Clip Diffusion，Physics IQ Score从21.59跃升至34.94。"
- "在Kinetics-600的FVD评估上，Video-GPT以Vanilla Transformer架构超越其他架构（U-Net、DiT），获得最佳FVD (315.40/89.44)。"
- "推理时增大视频片段内并行处理的帧数，Physics IQ Score从0.00 (1帧) 大幅提升至34.94 (54帧)，验证了片段内双向扩散的重要性。"
---

# Video-GPT via Next Clip Diffusion

> [!tip] 核心洞察
> 通过将视频划分为可变长度的片段，构建干净与带噪片段交织的输入序列，并采用片段级因果、帧级/块级双向的层级注意力掩码，Video-GPT能够以自监督方式学习预测下一片段，同时保留片段内并行扩散的生成优势。预训练仅依赖视频数据，无需文本标注，且通过渐进式训练从短到长视频逐步扩展能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Video-GPT：基于下一片段扩散的视频生成预训练 |
| 英文题名 | Video-GPT via Next Clip Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=E0ZAcqy9TB) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Video-GPT |
| Dataset | Physics-IQ Benchmark, Kinetics-600, UCF-101 Class-to-Video |

> [!tip] 效果简介
> - Physics-IQ Benchmark 上，Physics IQ Score 为 34.97，对比 VideoPoet 29.50 (2nd best)，变化 +5.47。
> - Kinetics-600 上，FVD(500) 为 315.40，对比 Seine 332.80，变化 -17.40。
> - Kinetics-600 上，FVD(5000) 为 89.44，对比 Seine 91.08，变化 -1.64。

## 概要

视频生成领域长期面临一个核心瓶颈：**长时序建模能力与单帧/短片段生成质量难以统一**。自回归模型天然适合处理长程依赖，但其逐帧预测的方式在生成质量上明显落后于扩散模型；而纯扩散模型虽然在单片段质量上表现出色，却难以有效建模跨越数十秒乃至数分钟的时序因果性。

Video-GPT 通过一个简洁的范式转换回应了这一瓶颈。它将视频片段视为“视觉词元”，提出**下一片段扩散（Next Clip Diffusion）**预训练框架：在片段之间采用自回归条件依赖以保持长时因果链，在片段内部则进行并行扩散去噪以保证生成质量。这一设计统一了长时上下文建模与高质量生成，使视频预测模型首次同时具备类语言模型的长程一致性与扩散模型的细节保真度。

**核心结论**：仅使用视频数据进行自监督预训练（无需任何文本标注），Video-GPT 在物理合理性基准 **Physics-IQ Benchmark** 上取得 34.97 的 Physics IQ Score，显著超越第二名 VideoPoet 的 29.50（提升超过 5 个百分点）。消融实验直接验证了范式转换的决定性作用——将训练目标从 Next Token Prediction 切换为 Next Clip Diffusion，Physics IQ Score 从 21.59 跃升至 34.94。在 **Kinetics-600** 的 FVD 评估上，Video-GPT 以 Vanilla Transformer 架构超越 U-Net 和 DiT 类方法，取得最佳 FVD 指标（315.40 @ 500 帧 / 89.44 @ 5000 帧）。

**方法定位**：Video-GPT 属于视频生成预训练方法，其关键创新点包括：（1）干净-带噪片段交织的输入序列构造；（2）片段级因果、帧级/块级双向的层级注意力掩码；（3）以干净历史片段为条件的自回归去噪推理；（4）从短到长的渐进式训练课程。该方法在视频预测（V2V）、类别到视频生成、文本到视频生成、图像动画及视频目标分割等下游任务上均展现出强泛化能力。



视频生成领域长期面临一个核心张力：**长时上下文建模**与**高质量生成**难以在同一框架内兼得。自回归模型（如基于Next Token Prediction的视频生成器）天然适合捕捉长程时序依赖，但其逐帧/逐token的离散预测方式导致生成质量不及扩散模型；纯扩散模型在单片段生成上表现出色，却受限于固定长度的噪声调度，难以有效建模跨越数十秒乃至数分钟的物理演化。这一瓶颈在需要物理一致性的长时视频预测任务中尤为突出——模型必须理解物体运动的因果链条，而非仅生成视觉上逼真的帧序列。

现有工作对此问题的回应大致分为两条路径。**自回归视频预测方法**（如**LVM**, Bai et al., 2023）将视频压缩为离散token后逐token预测，继承了语言模型的长程建模优势，但离散化带来的信息损失和逐token解码的低效限制了生成保真度。**扩散预测方法**（如**Seine**, Chen et al., 2023b; **VideoPoet**, Kondratyuk et al., 2023）在片段级或全局上执行扩散去噪，生成质量更优，但在处理超出训练窗口的长序列时，缺乏显式的自回归因果结构，导致时序一致性随预测步长增加而快速退化。简言之，**自回归擅长“讲长故事”但“画不精细”，扩散擅长“画精细帧”但“讲不长故事”**。

Video-GPT的核心动机正是弥合这一鸿沟。其关键洞察在于：**将视频片段（clip）视为类词元的基本语义单元**——如同GPT将文本词元作为预测的基本单位，Video-GPT将多帧片段作为扩散去噪的基本单位。这一类比催生了**下一片段扩散（Next Clip Diffusion）**范式：在片段间采用自回归的条件依赖（当前片段以所有历史干净片段为上下文），在片段内进行并行的双向扩散去噪。这种设计从结构上统一了两种范式的优势：**片段间的因果掩码保留了长时上下文建模能力，片段内的双向注意力则释放了扩散模型的高质量生成潜力**。

此外，Video-GPT的预训练策略刻意回归到GPT的自监督本源——**仅使用视频数据本身，无需任何文本标注**。在Panda-70M纯视频数据集上，通过渐进式训练课程（从16帧单帧预测逐步扩展到80帧多片段预测），模型从短到长逐步习得物理世界的时序规律。这种设计不仅降低了数据门槛，更迫使模型从原始视觉信号中自主归纳因果结构，而非依赖文本描述中的先验知识。

在评估维度上，论文特别关注**物理合理性**而非单纯的视觉质量。Physics-IQ Benchmark通过时空IoU、MSE等指标量化模型对物理定律的遵循程度，直指现有方法在“理解运动因果”而非“插值生成帧”上的不足。Video-GPT在该基准上以34.97的Physics IQ Score大幅领先第二名VideoPoet的29.50（提升超5个百分点），验证了下一片段扩散范式在物理世界建模上的实质性突破。



## 核心方法与创新机理

Video-GPT的核心创新在于提出**下一片段扩散（Next Clip Diffusion）**范式，从根本上改变了视频生成的建模范式。该范式将视频片段视为类词元的基本语义单元，在片段间建立自回归条件依赖，在片段内进行并行扩散去噪，从而统一了长时上下文建模与高质量生成两大目标。

### 建模范式的根本转变

传统视频生成方法在两类范式间存在明显取舍：自回归模型（如Next Token Prediction）擅长长时预测但生成质量不及扩散模型，而纯扩散模型在长时未来预测上受限。Video-GPT通过以下关键设计实现了范式跃迁：

**片段内扩散，片段间自回归。** 模型将视频划分为可变长度的片段（clips），对每个片段内部执行流匹配（flow matching）扩散去噪，同时在片段间施加因果自回归条件依赖。这一设计使得片段内可以并行、双向地处理多帧信息，保留扩散模型的高质量生成优势；片段间则维持时序因果性，支持任意长度的自回归预测。消融实验直接验证了这一转变的决定性作用：将训练范式从Next Token Prediction切换为Next Clip Diffusion，Physics IQ Score从21.59跃升至34.94（Table 5）。

**干净历史条件替代带噪历史条件。** 在条件建模上，Video-GPT使用已去噪的干净历史片段（clean clips）作为时序上下文，而非此前工作中常见的带噪历史。这一选择确保了模型接收正确的时序信息进行条件预测，避免了噪声累积导致的误差传播。

**直接预测去噪片段。** 训练目标从预测噪声或速度转变为直接预测去噪后的视频片段（clean clip），使模型学习更直接的视频生成映射。

### 层级注意力掩码设计

为实现片段间因果、片段内双向的信息交互模式，Video-GPT设计了**层级注意力掩码**（hierarchical masking），在三个粒度上分别施加约束：

- **片段级（Clip-Level）**：第k个带噪片段仅能关注前k-1个干净片段，保证自回归条件依赖。
- **帧级（Frame-Level）**：同一片段内的帧之间采用双向注意力，支持并行扩散去噪。
- **块级（Patch-Level）**：同一帧内的图像块之间同样采用双向注意力。

这种层级掩码使得模型在单次前向传播中同时处理干净与带噪片段交织的输入序列，高效实现下一片段的条件扩散生成。

### 渐进式训练课程

Video-GPT采用从短到长的渐进式训练策略（Table 1），分四个阶段逐步扩展视频长度和片段复杂度：从初始的16帧（每片段仅1帧，做下一帧预测）逐步增加到80帧（随机片段数）。这一课程设计使模型先掌握短时帧间关系，再逐步学习长时片段间依赖，显著提升了训练稳定性和最终性能。消融实验表明，预训练帧数从16增加到80，物理一致性持续提高（Phy.IQ Score: 22.06 → 33.09 → 34.94）。

### 训练-推理偏差弥合

推理时，模型使用自身生成的去噪片段（DNS）作为历史条件，与训练时使用的干净片段（CL）存在分布偏差。为弥合这一偏差，Video-GPT在训练时向干净帧添加可控的微小噪声：

$$\Phi_{k,\text{noisy}} = (\beta + \gamma_{k,i}) \Phi_{k} + (1 - \beta - \gamma_{k,i}) \epsilon_{k,i}$$

其中 $\gamma$ 是从小范围采样的随机数。消融实验证实这一设计将Phy.IQ Score从32.54提升至33.09（Table 5）。

### 自监督预训练特性

Video-GPT的预训练仅依赖视频数据（Panda-70M），无需任何文本标注，完全以自监督方式进行。这一特性使其继承了大语言模型的可扩展预训练属性，同时保留了扩散模型的生成质量优势。



![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/002_Figure_2.jpg]]
*Figure 2: Video-GPT pretraining framework. The full attention mask is shown in Fig. 10*

Video-GPT 的整体框架围绕“下一片段扩散”（Next Clip Diffusion）范式构建，将视频片段视为视觉词元，在片段间采用自回归条件依赖，在片段内进行并行扩散去噪，从而统一长时上下文建模与高质量生成。其 pipeline 可分解为四个核心阶段：片段序列构建、噪声-干净交织输入、层级注意力掩码下的 Transformer 处理，以及自回归推理引擎。

**片段序列构建与正向扩散。** 给定一段采样视频帧，Video-GPT 首先将其随机分割为 $K$ 个可变长度的片段（$K \sim \mathrm{Uniform}\{2, 3, \dots, N\}$）。对每个片段 $k$ 施加相同噪声等级 $\alpha_k$ 的流匹配前向扩散，得到带噪潜变量：

$$\Psi(k, i, \alpha_k) = \alpha_k \Phi(k, i) + (1 - \alpha_k) \varepsilon_{k,i}$$

其中 $\Phi(k,i)$ 为第 $k$ 片段第 $i$ 帧经 VAE 编码的干净潜变量，$\varepsilon_{k,i}$ 为高斯噪声。干净帧与带噪帧分别被封装为统一的 token 形式：干净帧以边界标记 `<img>` 包裹，带噪帧则包含去噪提示 `<diff>` 与噪声等级 $\alpha_k$。

**噪声-干净交织输入。** 所有干净片段与带噪片段按时间顺序交织排列，形成完整的输入序列：

$$\mathbf{Input} = [\mathbf{NS}(1,:), \mathbf{CL}(1,:), \dots, \mathbf{NS}(K,:)]$$

这一设计的核心在于：历史上下文使用原始干净片段而非带噪版本，为后续片段提供正确的时序条件，避免噪声累积导致的误差传播（Figure 2(a)）。

**层级注意力掩码。** 为同时满足片段间的因果依赖与片段内的双向信息交互，Video-GPT 引入三层级注意力掩码（Figure 2(b), Figure 10）：
- **片段级掩码**：第 $k$ 个带噪片段仅依赖前 $(k-1)$ 个干净片段，形成自回归条件约束；
- **帧级掩码**：同一干净片段内的帧可双向互注意，带噪片段内的帧也可双向互注意；
- **块级掩码**：每帧内部的 patch token 之间采用双向注意力。

这种层级设计使模型在保持时序因果性的同时，充分利用片段内并行扩散的生成优势。

**Transformer 骨干与输入/输出适配。** Video-GPT 继承 **Phi-3-mini**（Abdin et al., 2024）的 Vanilla Transformer 架构，参数量 3.8B。VAE 编码器/解码器采用 **SDXL**（Podell et al., 2023）将视频帧压缩至潜在空间。`clean_input` 与 `noised_input` 适配层将 VAE 潜变量转换为 Transformer 可处理的 token 表示，`noised_output` 层则将输出 token 还原为潜变量，经 VAE 解码器重建像素空间视频帧。

**自回归推理引擎。** 推理时（Figure 3），模型以已生成的干净片段为历史条件，自回归地逐步去噪下一片段：

$$\mathbf{DNS}(k+1, \cdot) = \mathrm{Video\text{-}GPT}\big(\mathbf{DNS}(1, \cdot), \dots, \mathbf{DNS}(k, \cdot), \mathbf{NS}(k+1, \cdot)\big)$$

每次迭代仅需处理当前带噪片段及其历史干净上下文，片段内多帧可并行去噪，推理效率显著优于逐帧自回归方案。推理时每片段的帧数可灵活变化，且支持无分类器引导（CFG）以提升生成质量。

**渐进式训练课程。** 预训练从短到长视频逐步扩展（Table 1）：初始阶段使用 16 帧、每片段仅 1 帧进行下一帧预测，随后逐步增加总帧数与每片段帧数，最终阶段在 80 帧上随机采样片段数进行训练。该策略使模型先掌握局部动态，再逐步学习长时依赖。

**预训练数据与自监督特性。** Video-GPT 仅依赖视频数据（Panda-70M，Chen et al., 2024b）进行自监督预训练，无需文本标注。训练目标直接预测去噪后的干净片段，而非预测噪声或速度，与推理时的生成目标一致。



### 3.1 输入构建与前向扩散

Video-GPT 的核心输入构造围绕“干净-带噪片段交织”展开。给定一段视频，首先通过 VAE Encoder（SDXL）将所有帧压缩至潜在空间，得到潜在特征 $\Phi(k,i)$，表示第 $k$ 个片段中的第 $i$ 帧。随后，对每个片段施加统一噪声等级的前向扩散：

$$\Psi(k,i,\alpha_k) = \alpha_k \Phi(k,i) + (1-\alpha_k)\varepsilon_{k,i}$$

其中 $\alpha_k$ 为第 $k$ 个片段的噪声等级，$\varepsilon_{k,i} \sim \mathcal{N}(0,1)$ 为标准高斯噪声。该式采用流匹配（flow matching）范式，训练时同一片段内所有帧共享相同的 $\alpha_k$。

干净帧与带噪帧分别被包装为两类 token 序列：

- **干净片段 token**：$\mathbf{CL}(k,i) = [<\mathrm{img}>, \Phi(k,i), <\mathrm{img}>]$，以边界标记 `<img>` 包裹潜在特征。
- **带噪片段 token**：$\mathbf{NS}(k,i) = [<\mathrm{diff}>, \alpha_k, \Psi(k,i,\alpha_k)]$，包含去噪提示符 `<diff>` 和噪声等级 $\alpha_k$。

两类 token 按时间顺序交织排列，构成完整输入序列：

$$\mathbf{Input} = [\mathbf{NS}(1,:), \mathbf{CL}(1,:), \dots, \mathbf{NS}(k,:), \mathbf{CL}(k,:), \dots, \mathbf{NS}(K,:)]$$

其中 $K$ 为随机采样的片段数，$K \sim \mathrm{Uniform}\{2,3,\dots,N\}$。这一设计的关键在于：**使用干净历史片段（而非带噪历史）作为上下文条件**，为后续片段的自回归去噪提供正确的时序信息。

### 3.2 层级注意力掩码

为实现“片段间自回归依赖、片段内并行扩散”的混合建模，Video-GPT 设计了三级层级注意力掩码：

- **片段级掩码（Clip-Level Mask）**：第 $k$ 个带噪片段 $\mathbf{NS}(k,:)$ 仅能关注前 $k-1$ 个干净片段 $\mathbf{CL}(1,:)$ 至 $\mathbf{CL}(k-1,:)$，强制因果依赖关系。
- **帧级掩码（Frame-Level Mask）**：同一片段内的帧之间采用双向注意力，允许并行信息交互。
- **块级掩码（Patch-Level Mask）**：每帧内部的图像块之间同样采用双向注意力。

该掩码设计使得 Video-GPT 在片段间保持严格的时间因果性，同时在片段内充分利用扩散模型的双向生成优势。完整掩码可视化见 Figure 10。

### 3.3 训练目标与推理机制

**训练目标**：Video-GPT 直接预测去噪后的干净片段，而非预测噪声或速度场。训练时通过干净/带噪输入适配层（`clean_input` 和 `noised_input` layers）将 VAE 潜在特征转换为 Transformer 可处理的 token，输出经 `noised_output` 层还原为潜在空间。

**自回归推理**：推理时采用逐片段迭代去噪策略，以已生成的干净片段为条件，逐步预测下一片段：

$$\mathbf{DNS}(k+1,\cdot) = \mathrm{Video-GPT}\big(\mathbf{DNS}(1,\cdot), \dots, \mathbf{DNS}(k,\cdot), \mathbf{NS}(k+1,\cdot)\big)$$

其中 $\mathbf{DNS}(j,\cdot)$ 表示第 $j$ 个已完成去噪的片段，$\mathbf{NS}(k+1,\cdot)$ 为待去噪的下一带噪片段。每次迭代中，片段级掩码退化为因果掩码，确保自回归预测的一致性。

**训练-推理偏差弥合**：由于推理时 $\mathbf{DNS}$ 与训练时的 $\mathbf{CL}$ 存在分布偏差，训练阶段向干净帧添加微小噪声：

$$\Phi_{k,\text{noisy}} = (\beta + \gamma_{k,i})\Phi_k + (1-\beta-\gamma_{k,i})\epsilon_{k,i}$$

其中 $\beta$ 为基础噪声权重，$\gamma_{k,i}$ 为从小范围均匀采样的随机扰动。消融实验表明，该策略将 Physics IQ Score 从 32.54 提升至 33.09（Table 5）。

### 3.4 渐进式训练课程

Video-GPT 采用四阶段渐进式训练策略（Table 1），从短视频逐步扩展到长视频：

| 阶段 | 帧数 | 每片段帧数 | 片段数采样 | 训练步数 |
|------|------|-----------|-----------|---------|
| Stage 1 | 16 | 1（逐帧预测） | 固定 | 300K |
| Stage 2 | 48 | 随机 | 随机 | 25K |
| Stage 3 | 48 | 随机 | 随机 | 40K |
| Stage 4 | 80 | 随机 | 随机 | 20K |

初始阶段以逐帧预测（每片段仅含 1 帧）作为起点，使模型先掌握基本的下一帧扩散能力；后续阶段逐步增加片段内帧数和片段数随机性，使模型适应可变长度片段的并行去噪。消融实验证实，预训练帧数从 16 增至 80 时，Physics IQ Score 从 22.06 持续提升至 34.94（Table 5）。



## 实验与关键发现

### 核心实验设计

Video-GPT的预训练完全基于自监督范式，仅使用Panda-70M视频数据集，无需任何文本标注。模型采用渐进式训练策略（Table 1），从16帧（每片段1帧）逐步扩展至80帧（随机片段数），训练步数从300K递减至20K，使模型从短时预测平滑过渡到长时建模。基础架构继承自Phi-3-mini（3.8B参数），使用SDXL的VAE进行视频帧压缩，在320块H20 GPU上完成训练。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/003_Table_1.jpg]]
*Table 1: Progressive training strategy*

### 物理合理性基准测试

Table 2展示了Physics-IQ Benchmark上的定量对比结果。Video-GPT（V2V模式）以**34.97**的Physics IQ Score取得最优，远超第二名的VideoPoet（29.50）和Seine（29.13），提升幅度超过5个百分点。在Spatio Temporal IoU指标上，Video-GPT同样以0.240领先所有对比方法，MSE低至0.007。值得注意的是，Video-GPT的I2V模式（35.80）进一步超越了V2V模式，但与封闭源商业模型Gen 3（37.72）仍有差距，后者可能受益于更大规模的标注数据训练。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison of models evaluated on the Physics-IQ Benchmark*

Figure 5的定性对比直观展示了这一优势：在物体与障碍物交互、液体容器倾倒等物理场景中，Video-GPT预测的视频帧（绿色框）在运动轨迹、碰撞响应和流体形变上明显更符合物理规律，而其他方法常出现物体穿透、运动不连续等违反物理常识的错误。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results on Physics-IQ Benchmark. The videos predicted by our Video-GPT based on condition frames are more consistent with physical laws than other methods*

### Kinetics-600视频预测评估

Table 3报告了Kinetics-600上的FVD指标。Video-GPT以Vanilla Transformer架构取得FVD(500)=315.40和FVD(5000)=89.44的最佳成绩，优于使用U-Net架构的Seine（332.80/91.08）和DiT架构的Open-Sora-Plan（343.08/97.15）。这一结果表明，在统一的Vanilla Transformer架构下，下一片段扩散范式能够超越专门设计的视频生成架构，且参数量（3.8B）远小于LVM（7B），体现了架构简洁性与建模能力的良好平衡。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/009_Table_3.jpg]]
*Table 3: Quantitative comparison of video generation models evaluated on the Kinetics-600*

### 推理设置消融

Table 4揭示了片段内并行处理帧数的关键作用。当每视频片段仅包含1帧时，Physics IQ Score为0.00，模型完全无法生成物理合理的预测；随着帧数增加至54帧，分数跃升至34.94。这一消融直接验证了核心设计动机：片段内双向扩散对于高质量生成至关重要，纯自回归逐帧预测无法捕获帧间的双向依赖关系。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/010_Table_4.jpg]]
*Table 4: Inference setting ablation*

此外，无分类器引导（CFG）尺度的消融表明，历史条件引导尺度c=3.0时Stage 4模型表现最强，过高或过低的引导尺度均会损害生成质量。

### 训练设置消融

Table 5的系统消融揭示了几个关键因素：

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/011_Table_5.jpg]]
*Table 5: Training setting ablation*

**预训练范式**：将训练目标从Next Token Prediction切换为Next Clip Diffusion，Physics IQ Score从21.59跃升至34.94（提升约62%），这是整个方法中最具决定性的设计选择，证实了扩散生成在视频质量上相比自回归离散预测的根本优势。

**预训练帧数**：从16帧逐步增加至80帧，物理一致性持续提升（22.06→33.09→34.94），验证了渐进式训练课程对长时建模能力培养的有效性。

**干净帧噪声注入**：训练时向干净片段添加轻微噪声（Eq. 6），使Physics IQ Score从32.54提升至33.09，弥合了训练阶段使用精确干净帧与推理阶段使用模型生成帧之间的分布偏差。

**数据规模**：预训练数据从1M扩展至70M，Physics IQ Score从23.16提升至33.09，表明自监督世界建模能力随数据量增加而显著增强，但增速在后期趋于平缓。

### 下游任务泛化

Table 6显示，在UCF-101类别到视频生成任务上，Video-GPT取得FVD=191，显著优于OmniTokenizer（332）和LVD（372），验证了预训练表征向条件生成任务的有效迁移。Table 7和Table 8分别展示了视频分类线性探测（UCF-101 Top-1准确率）和视频检索零样本（MSR-VTT R@1）的结果，进一步证实了自监督预训练学到的时序表征在下游理解任务中的竞争力。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/015_Table_6.jpg]]
*Table 6: Class to video quantitative comparison on the UCF-101*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/016_Table_7.jpg]]
*Table 7: Video classification linear probe on UCF-101*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/017_Table_8.jpg]]

### 失败模式与局限

尽管长视频生成效果显著优于Open-Sora-Plan（Figure 14 vs Figure 15），Video-GPT在部分静止与突然运动交替的极端场景下（Figure 13），生成质量仍有明显退化，表现为运动模糊、物体形变或时序不连贯。当前实验受限于3.8B参数规模和Panda-70M数据集，更大规模模型和数据下的性能涌现潜力尚未验证。此外，模型目前仅验证了视频预测和条件生成任务，尚未扩展到多模态预训练或与强化学习结合的世界交互学习。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/020_Table_9.jpg]]
*Table 9: Pretraining Stage 1 setting*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_E0ZAcqy9TB/figures/021_Table_10.jpg]]
*Table 10: Pretraining Stage 2 setting. Table 12: Pretraining Stage 4 setting*



## 定位与知识库关联

### 1. 核心范式转换：从“下一词元预测”到“下一片段扩散”

Video-GPT的根本创新在于建模范式的切换。传统视频生成模型面临一个结构性矛盾：自回归模型（如**LVM**，Bai et al., 2023）天然适合长时上下文建模，但逐帧/逐词元的离散预测方式导致生成质量不及扩散模型；而纯扩散模型在长时未来预测上受限于条件注入方式。Video-GPT通过“下一片段扩散”（Next Clip Diffusion）范式统一了这两条路径——将视频片段视为类词元的基本单元，在片段间采用自回归条件依赖，在片段内进行并行扩散去噪。

消融实验直接验证了这一范式转换的决定性作用：当训练范式从Next Token Prediction切换为Next Clip Diffusion时，Physics IQ Score从21.59跃升至34.94（Table 5），提升幅度超过13个点。这表明，片段级的扩散生成机制对于捕获物理世界规律至关重要，单纯的离散词元预测即使在大规模预训练下也难以习得精细的物理一致性。

### 2. 与现有方法的架构谱系关系

**架构选择上的反直觉发现**：Video-GPT采用基于Phi-3-mini的Vanilla Transformer作为骨干网络，而非视频生成领域主流的U-Net或DiT架构。在Kinetics-600的FVD评估中，这一选择反而取得了最佳结果（FVD(500)=315.40, FVD(5000)=89.44），优于采用U-Net的**Seine**（Chen et al., 2023b，332.80/91.08）和DiT架构的**Open-Sora-Plan v1.3.0**（Lin et al., 2024）。这表明，当建模范式从全序列扩散转变为片段级扩散后，Vanilla Transformer的序列建模能力反而成为优势，架构的选择高度依赖于范式本身。

**与自回归视频模型的关系**：Video-GPT在片段间保持自回归特性，但与**LVM**等纯自回归方法不同，其历史条件使用的是干净片段而非带噪片段。这一设计确保了时序条件的正确性，避免了误差累积——这是自回归扩散模型中的关键工程决策。

**与封闭源商业模型的对比**：在Physics-IQ Benchmark上，Video-GPT（V2V模式，34.97）显著超越了**VideoPoet**（Kondratyuk et al., 2023，29.50）、**Gen 3**（Runway, 2024，I2V模式）、**Kling1.6**（Kuaishou, 2024）和**Wan2.1**（Wang et al., 2025）等商业系统，且这一优势是在仅使用视频数据自监督预训练、无文本标注的条件下取得的。

### 3. 关键设计要素的消融证据

**片段内并行帧数的决定性作用**：推理时每视频片段内并行处理的帧数从1帧增加到54帧，Physics IQ Score从0.00提升至34.94（Table 4）。单帧片段退化为纯自回归预测，完全丧失了扩散模型的生成质量优势；多帧片段内的双向注意力使得模型能够协调片段内的运动一致性，这是物理合理性判断的基础。

**预训练数据规模的缩放效应**：预训练数据从1M扩展到70M，Physics IQ Score从23.16提升至33.09（Table 5），显示出明确的数据规模正相关性，但增幅逐渐趋缓。这暗示Video-GPT的世界建模能力受益于大规模视频预训练，但当前3.8B参数规模可能已接近Panda-70M数据集的信息瓶颈。

**训练-推理偏差的弥合**：向干净帧添加微小噪声（Eq. 6）使Physics IQ Score从32.54提升至33.09（Table 5），验证了自回归推理中干净条件帧与训练时干净片段之间存在分布偏差，轻微噪声注入是一种有效的正则化手段。

### 4. 适用边界与局限

**计算资源约束下的未完成探索**：当前实验在3.8B参数、320块H20 GPU的规模下进行，尚未验证更大规模模型（如百亿参数级）和更庞大视频语料上的性能涌现潜力。从数据规模消融的趋势来看，进一步扩展可能带来持续但递减的收益。

**极端场景的生成质量瓶颈**：在部分静止与突然运动交替的视频中（Figure 13），生成质量仍有明显不足。这暴露了片段级扩散的一个内在张力：片段内并行处理假设帧间运动是平滑可预测的，当运动模式发生突变时，片段边界处的连续性难以保证。

**多模态扩展的空白**：当前Video-GPT仅使用纯视频数据进行自监督预训练，尚未融入文本、音频等多模态信息。这限制了其在文生视频、视频理解等需要跨模态对齐的任务上的直接应用，需要额外的微调步骤。

### 5. 开放问题

1. **规模扩展的涌现性**：当模型参数量和预训练数据量同步扩展至工业级（如百亿参数、亿级视频）时，Video-GPT的物理世界建模能力是否会出现涌现式的质变，而非仅是量变的线性提升？

2. **多模态融合的自监督范式**：如何在不破坏“下一片段扩散”自监督框架的前提下，自然融入文本描述、音频轨迹等模态信息，使模型习得跨模态的世界知识，而非仅依赖视觉信号？

3. **主动世界交互的可能性**：Video-GPT的片段级自回归结构天然支持基于历史观测的未来预测，这是否可以作为强化学习中世界模型的基础，通过与环境的主动交互来进一步提升物理推理和决策能力？

4. **片段边界一致性的理论保证**：当前方法依赖片段内双向注意力来协调帧间一致性，但在片段边界处缺乏显式的连续性约束。是否存在更优的片段划分策略或边界正则化方法，可以从理论上保证长视频生成中的全局时间一致性？



## 原文 PDF

![[paperPDFs/ICLR_2026/Video_GPT_via_Next_Clip_Diffusion.pdf]]
