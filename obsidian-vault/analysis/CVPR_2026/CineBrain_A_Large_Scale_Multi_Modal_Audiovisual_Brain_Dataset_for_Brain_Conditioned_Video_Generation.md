---
title: "CineBrain: A Large-Scale Multi-Modal Audiovisual Brain Dataset for Brain-Conditioned Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CineBrain_A_Large_Scale_Multi_Modal_Audiovisual_Brain_Dataset_for_Brain_Conditioned_Video_Generation.pdf
project_link: "https://jianxgao.github.io/CineBrain"
code_link: null
aliases:
- CineBrain
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 同步采集自然视听刺激下的fMRI与EEG信号，并利用双转换器分别编码两种模态特征，通过融合MLP和跨模态对比学习实现空间-时间互补信息的整合，从而显著提升动态视频重建的语义准确性和时间一致性。
primary_logic: 通过同时捕捉fMRI的高空间激活模式和EEG的高时间动态，并借助多模态对比学习将脑表征与视觉-文本语义对齐，可以突破单模态解码的信息瓶颈，利用听觉皮层等跨模态信息显著增强视觉知觉重建的保真度。
claims:
- 与单纯使用fMRI或EEG的方法相比，CineSync联合建模两种信号实现了最先进的视频重建性能（2-way准确率0.909，FVD 52.78）
- 融合听觉ROIs后，CineSync*的2-way视频准确率从0.909进一步提升到0.926，表明听觉皮层激活显著增强了解码准确性
- 在五种融合架构的比较中，双转换器分离编码fMRI和EEG的策略显著优于早期共享自注意力的联合Transformer（2-way 0.929 vs 0.924，FVD 51.53 vs 128.0）
- 增加EEG的表征能力可以进一步提升重建质量，验证了EEG在捕捉快速神经动态中的关键作用
---

# CineBrain: A Large-Scale Multi-Modal Audiovisual Brain Dataset for Brain-Conditioned Video Generation

> [!tip] 核心洞察
> 通过同时捕捉fMRI的高空间激活模式和EEG的高时间动态，并借助多模态对比学习将脑表征与视觉-文本语义对齐，可以突破单模态解码的信息瓶颈，利用听觉皮层等跨模态信息显著增强视觉知觉重建的保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | CineBrain：用于脑条件视频生成的大规模多模态视听脑数据集 |
| 英文题名 | CineBrain: A Large-Scale Multi-Modal Audiovisual Brain Dataset for Brain-Conditioned Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gao_CineBrain_A_Large-Scale_Multi-Modal_Audiovisual_Brain_Dataset_for_Brain-Conditioned_Video_CVPR_2026_paper.html) · [Project](https://jianxgao.github.io/CineBrain) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | CineSync |
| Dataset | CineBrain |

> [!tip] 效果简介
> - CineBrain 上，2-way↑ (语义视频检索准确率) CineSync (fMRI+EEG): 0.909 vs CineSync-fMRI: 0.893 (+0.016)；2-way↑ CineSync (fMRI+EEG): 0.909 vs CineSync-EEG: 0.891 (+0.018)；FVD↓ (视频质量评估) CineSync (fMRI+EEG): 52.78 vs CineSync-fMRI: 57.47 (-4.69 (提升))。

## 概要

**问题瓶颈**：现有神经解码研究长期聚焦于单视觉模态与单脑信号（fMRI 或 EEG）的重建，却忽视了大脑在自然视听刺激下整合多感官信息的本质能力。fMRI 提供高空间分辨率但时间响应迟缓，EEG 捕获毫秒级动态但空间定位模糊，二者的互补优势在缺乏同步采集与跨模态对齐的数据集时无法被利用。这一信息瓶颈直接限制了从脑信号重建动态视频的语义准确性与时间一致性。

**核心方法**：本文提出 **CineSync** 框架，通过双转换器架构独立编码同步采集的 fMRI 与 EEG 信号，经融合 MLP 生成统一脑表征，并借助多层级对比学习（fMRI‑视频、fMRI‑文本、EEG‑视频、EEG‑文本、fMRI‑EEG 五组 CLIP 损失）将脑表征锚定到视觉‑文本语义空间。该表征随后作为条件输入 LoRA 微调的扩散模型（CogVideoX‑5B），从噪声中重建动态视频。

**关键因果机制**：同时捕捉 fMRI 的高空间激活模式与 EEG 的高时间动态，并通过多模态对比学习实现空间‑时间互补信息的语义对齐，是突破单模态解码瓶颈的决定性因素。进一步引入听觉皮层 ROI 后，听觉跨模态信息显著增强了视觉知觉重建的保真度。

**主要结果**：在自建的大规模多模态视听脑数据集 **CineBrain**（6 名受试者，每人约 6 小时同步 fMRI‑EEG 记录）上，CineSync 实现了最先进的视频重建性能，2‑way 语义检索准确率达 0.909，FVD 降至 52.78；融合听觉 ROI 的 CineSync⋆ 变体进一步将准确率提升至 0.926，FVD 降至 44.77。消融实验证实，双转换器分离编码策略显著优于联合自注意力等早期融合方案，且多层级对比损失与 EEG 表征容量的增加均对性能有正向贡献。

### 神经解码的模态瓶颈：从静态图像到动态视频的鸿沟

从人脑信号中重建视觉体验是计算神经科学与人工智能交叉领域的核心挑战之一。过去十年，基于功能磁共振成像（fMRI）的视觉解码取得了长足进步，研究者已能根据大脑活动模式重建出被试所看到的静态图像。然而，这些成果主要局限于单视觉模态、单脑信号源（fMRI或脑电图EEG）的静态重建范式，与人类在自然环境中实时整合多感官信息、处理动态视觉刺激的神经本质存在根本性脱节。

这一脱节体现在三个层面。**第一，模态单一性**：现有研究几乎完全依赖fMRI或EEG中的单一信号源。fMRI具备毫米级空间分辨率，能够精确定位视觉皮层的激活区域，但其时间分辨率仅为秒级，难以捕捉快速变化的神经动态；EEG则以毫秒级时间分辨率见长，能够忠实记录大脑对动态刺激的瞬时响应，但其空间定位能力有限。两种模态在信息表征上天然互补，却鲜有研究尝试联合建模。**第二，刺激静态性**：绝大多数脑数据集使用静态图像作为视觉刺激，忽略了真实世界中视觉信息以动态视频流形式呈现的基本事实，更未涉及听觉信息对视觉知觉的跨模态调控作用。**第三，缺乏同步采集的多模态基准**：同时记录fMRI和EEG面临严峻的工程挑战——EEG设备必须在强磁场环境中工作，且两种信号之间存在复杂的电磁干扰。这一技术壁垒导致缺乏大规模、同步采集的fMRI-EEG视听脑数据集，从根本上制约了多模态脑信号视频重建的研究进展。

### CineBrain的破局思路

CineBrain正是在上述背景下应运而生。该工作的核心动机在于：**通过构建首个大规模同步fMRI-EEG视听脑数据集，并设计能够融合两种模态互补信息的神经解码框架，突破单模态解码的信息瓶颈，实现从脑信号中高质量重建动态视频。**

具体而言，CineBrain做出了以下关键设计选择：

- **自然叙事性视听刺激**：选用情景剧《生活大爆炸》（The Big Bang Theory）作为刺激材料。叙事驱动的视频内容包含丰富的人物对话、场景切换和社交互动，能够同时激活视觉皮层和听觉皮层，为研究多感官整合和复杂脑动态提供了生态效度更高的实验范式。

- **同步fMRI-EEG采集**：在3T MRI扫描仪中部署定制非磁性脑电帽，实现fMRI（高空间分辨率）与EEG（高时间分辨率）的严格同步记录，为跨模态互补信息的挖掘奠定数据基础。

- **双转换器分离编码与跨模态对比对齐**：提出CineSync框架，采用双转换器（Dual Transformer）分别独立编码fMRI空间模式与EEG时间动态，通过融合MLP进行末期整合，并借助多层级对比学习将脑表征与视频-文本语义空间对齐。这一设计避免了早期融合可能引入的模态间干扰，同时确保了解码结果在语义层面的准确性和时间维度上的一致性。

### 现有方法缺口与本文定位

在CineBrain之前，视频-脑数据集领域存在明显的空白。如Table 1所示（见实验与分析部分），现有数据集要么仅提供单一模态的脑信号记录，要么刺激材料限于静态图像或简单动态刺激，缺乏大规模、多模态、自然视听刺激下的同步fMRI-EEG数据。这一数据缺口直接导致神经解码研究长期停留在静态图像重建阶段，无法验证多模态融合在动态视频解码中的潜力。

CineBrain填补了这一空白：每名被试贡献约6小时的同步fMRI-EEG数据（对应约27,000帧fMRI扫描），总计提供覆盖视觉皮层（8,405个体素）和听觉皮层（总计18,946个体素）的丰富脑激活模式。基于此数据集，CineSync框架首次系统验证了fMRI-EEG联合建模相较于单模态方法的显著增益——2-way视频检索准确率从单模态最优的0.893（仅fMRI）提升至0.909（联合建模），融合听觉ROIs后进一步达到0.926（Table 3），为多模态脑解码研究确立了新的基准。

## 核心方法与创新机理

CineSync 的核心创新在于**首次将同步采集的 fMRI 与 EEG 信号进行多模态联合建模**，以突破现有神经解码研究中仅依赖单一脑模态的信息瓶颈。其创新点可归纳为以下四个关键维度：

1. **多模态同步输入与互补性利用**：传统方法仅使用 fMRI（高空间分辨率）或 EEG（高时间分辨率）进行视觉重建，忽略了大脑在自然视听刺激下整合多感官信息的本质能力。CineSync 首次以同步采集的 fMRI 与 EEG 作为联合输入，使模型能够同时捕捉视觉皮层的空间激活模式与全脑的快速时间动态，从根本上弥补了单模态信息的固有缺陷。

2. **双转换器分离编码与末期融合策略**：现有融合方案多采用早期交互（如联合自注意力），但不同模态的特征分布差异显著，过早交互会干扰各自的特征提取。CineSync 提出**Dual Transformer Fusion**架构——fMRI 与 EEG 分别由独立 Transformer 编码，仅在特征提取完成后通过融合 MLP（$\psi$）进行末期融合，生成统一的脑表征 $\mathbf{z}_b = \psi(\mathbf{z}_f, \mathbf{z}_e)$。消融实验表明，该策略在所有语义与感知指标上均显著优于联合 Transformer、交叉注意力融合等四种对比架构（Tab. 2，2-way 准确率 0.929 vs 0.924，FVD 51.53 vs 128.0）。

3. **多层级跨模态对比学习对齐**：CineSync 引入五项目标联合优化的对比损失——$\mathcal{L}_c = \mathcal{L}_{fv} + \mathcal{L}_{ft} + \mathcal{L}_{ev} + \mathcal{L}_{et} + \mathcal{L}_{fe}$，将 fMRI 与 EEG 的类别标记分别对齐到预训练的视频与文本语义空间，同时施加 fMRI-EEG 跨模态对齐。这一设计使脑表征在训练过程中被显式锚定于视觉-文本语义结构，从而在后续扩散解码中提供更丰富的条件信息。消融实验证实，缺少任一对齐损失均导致性能下降。

4. **听觉皮层信息增强视觉解码**：CineSync 的扩展变体 CineSync$^\star$ 将 fMRI 感兴趣区（ROIs）从仅视觉皮层（8,405 个体素）扩展至视觉+听觉皮层（共 18,946 个体素）。加入听觉 ROIs 后，2-way 视频检索准确率从 0.909 提升至 0.926，FVD 从 52.78 降至 44.77（Tab. 3），首次直接验证了听觉皮层激活对视觉知觉重建的跨模态增强效应。

综上，CineSync 通过“同步多模态输入—分离编码—末期融合—多层级语义对齐—跨模态信息增强”的技术路径，实现了脑信号视频重建在语义准确性与时间一致性上的显著突破。

CineSync 的整体设计遵循“编码—对齐—解码”的两阶段范式，其核心思路是将多模态脑信号（fMRI + EEG）转化为统一的脑表征，再以该表征为条件驱动预训练视频扩散模型生成动态视频。框架由两大模块构成：**多模态融合编码器（Multi-Modal Fusion Encoder, MFE）** 和 **神经潜变量解码器（Neural Latent Decoder, NLD）**，如 Figure 5 所示。

![[assets/figures/papers/paper_list_l2045_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_CineBrain_A_Large/figures/007_Figure_5.jpg]]
*Figure 5: Overview of the CineSync Framework. CineSync first employs a Multimodal Fusion Encoder to extract features from fMRI and EEG data, with a modality alignment module to align these features with semantic information. Subsequently, it utilizes a LoRA-tuned neural latent decoder to reconstruct videos based on the fused brain features. Note: The gray box is used only during training*

**输入流与编码阶段。** 给定同步采集的 fMRI 体素序列 $\mathbf{x}_f$ 与 EEG 时序信号 $\mathbf{x}_e$，MFE 采用双转换器（dual-transformer）架构独立处理两种模态——fMRI 编码器 $E_f$ 与 EEG 编码器 $E_e$ 各自提取潜在特征 $\mathbf{z}_f, \mathbf{z}_e$ 以及类别标记（class token）$\mathbf{c}_f, \mathbf{c}_e$：

$$\mathbf{z}_f, \mathbf{z}_e, \mathbf{c}_f, \mathbf{c}_e = E(\mathbf{x}_f, \mathbf{x}_e)$$

该设计的关键因果 knob 在于**减少 fMRI 与 EEG 在特征提取阶段的早期交互**：消融实验（Table 2）表明，分离编码的 Dual Transformer Fusion 在 2-way 准确率（0.929）和 FVD（51.53）上均显著优于早期共享自注意力的 Joint Transformer（0.924 / 128.0），说明不同模态的底层表征差异较大，独立建模有利于保留各自的信息结构。

**融合与对齐阶段。** 提取到的潜在特征通过融合 MLP $\psi$ 组合为统一的脑表征向量：

$$\mathbf{z}_b = \psi(\mathbf{z}_f, \mathbf{z}_e)$$

该向量 $\mathbf{z}_b$ 是后续视频生成的唯一脑条件信号。在训练阶段，MFE 同时引入**多层级对比学习对齐模块**（Figure 5 中灰色框部分），利用预训练的视频编码器和文本编码器，将脑信号的类别标记 $\mathbf{c}_f, \mathbf{c}_e$ 与视觉-文本语义空间对齐。具体而言，对齐损失包含五个 CLIP 损失项：

$$\mathcal{L}_c = \mathcal{L}_{fv} + \mathcal{L}_{ft} + \mathcal{L}_{ev} + \mathcal{L}_{et} + \mathcal{L}_{fe}$$

分别对应 fMRI-视频、fMRI-文本、EEG-视频、EEG-文本以及 fMRI-EEG 跨模态对比。消融实验证实，缺少任一对齐损失均会导致性能下降，表明多层级语义锚定是弥合脑信号与视觉语义之间鸿沟的关键机制。

**解码与生成阶段。** 神经潜变量解码器基于 CogVideoX-5B 视频扩散模型构建，通过 LoRA 微调适配脑条件生成。其核心改动是将原始文本条件替换为融合脑表征 $\mathbf{z}_b$，训练目标为标准扩散损失：

$$\mathcal{L} = \mathbb{E}_{V,\epsilon,t}\left[\left\|\epsilon - \epsilon_\theta(\mathbf{x}_t, \mathbf{z}_b, t)\right\|^2\right]$$

其中 $\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\epsilon$ 为扩散前向加噪过程。推理时，仅需输入 fMRI 与 EEG 信号，MFE 输出 $\mathbf{z}_b$ 后直接驱动 NLD 从随机噪声迭代去噪生成视频帧。

**整体数据流可概括为：** 同步 fMRI + EEG → 双转换器独立编码 → 融合 MLP 生成 $\mathbf{z}_b$ →（训练时）多层级对比对齐 → LoRA 微调的扩散解码器 → 动态视频输出。该流程的瓶颈突破点在于同时利用 fMRI 的高空间分辨率与 EEG 的高时间分辨率，并通过跨模态对比学习将脑表征锚定到可解码的语义空间，从而显著提升视频重建的语义准确性与时间一致性。

![[assets/figures/papers/paper_list_l2045_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_CineBrain_A_Large/figures/001_Figure_1.jpg]]
*Figure 1: Overview of CineBrain. To leverage the complementary strengths of fMRI and EEG, CineBrain provides simultaneous audiovisual stimuli to participants while recording their EEG and fMRI signals. Engaging narrative-driven content from the television series The Big Bang Theory is utilized to facilitate the study of complex brain dynamics and multimodal neural decoding*

CineSync 框架由两个核心模块构成：**多模态融合编码器（Multi-Modal Fusion Encoder, MFE）** 与 **神经潜变量解码器（Neural Latent Decoder, NLD）**。MFE 负责从同步采集的 fMRI 和 EEG 信号中提取并融合脑表征，NLD 则以此表征为条件，通过扩散模型重建动态视频。

### 多模态融合编码器（MFE）

MFE 采用双转换器（dual-transformer）架构，独立处理 fMRI 和 EEG 序列，避免早期交互带来的模态间干扰。其编码过程可形式化为：

$$\mathbf{z}_f, \mathbf{z}_e, \mathbf{c}_f, \mathbf{c}_e = E(\mathbf{x}_f, \mathbf{x}_e)$$

其中，$\mathbf{x}_f$ 和 $\mathbf{x}_e$ 分别为输入的 fMRI 体素序列和 EEG 时间序列；$\mathbf{z}_f$ 与 $\mathbf{z}_e$ 是提取的潜在特征；$\mathbf{c}_f$ 与 $\mathbf{c}_e$ 是类别标记（class token），用于后续的语义对齐。消融实验（Table 2）证实，这种分离编码策略在 2-way 准确率（0.929 vs. 0.924）和 FVD（51.53 vs. 128.0）上均显著优于联合自注意力的 Joint Transformer 方案。

为整合互补信息，引入融合 MLP $\psi$ 将两种模态的潜在特征合并为统一的脑表征向量：

$$\mathbf{z}_b = \psi(\mathbf{z}_f, \mathbf{z}_e)$$

$\mathbf{z}_b$ 即作为后续视频重建的条件信号。

### 多层级对比学习对齐（仅训练时）

为使脑表征与视觉-文本语义空间对齐，MFE 在训练时额外引入多层级对比损失。视频级嵌入由逐帧编码后经时间聚合函数 $\varphi$ 得到，文本嵌入由文本编码器直接提取：

$$\mathbf{c}_v = \varphi(\{E_v(\mathbf{I}_i)\}_{i=1}^n), \quad \mathbf{c}_t = E_t(\text{Text})$$

在此基础上，构建五个 CLIP 风格的对比损失项，覆盖脑信号与视频/文本、以及脑信号跨模态之间的对齐：

$$\mathcal{L}_c = \mathcal{L}_{fv} + \mathcal{L}_{ft} + \mathcal{L}_{ev} + \mathcal{L}_{et} + \mathcal{L}_{fe}$$

其中 $\mathcal{L}_{fv}$ 为 fMRI-视频损失，$\mathcal{L}_{ft}$ 为 fMRI-文本损失，$\mathcal{L}_{ev}$ 与 $\mathcal{L}_{et}$ 对应 EEG 的同类损失，$\mathcal{L}_{fe}$ 为 fMRI-EEG 跨模态对比损失（如 $\mathcal{L}_{fe} = \mathcal{L}_{\text{clip}}(\mathbf{c}_f, \mathbf{c}_e)$）。消融实验表明，缺少任一对齐项均导致整体性能下降，验证了该多层级对齐策略的关键作用。

### 神经潜变量解码器（NLD）

NLD 基于预训练的视频扩散模型 CogVideoX-5B，通过 LoRA 微调适配脑条件生成。其核心改动是将原始文本条件替换为融合脑表征 $\mathbf{z}_b$。扩散前向过程遵循标准形式：

$$\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\epsilon, \quad \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

训练损失以 $\mathbf{z}_b$ 为条件，最小化噪声预测误差：

$$\mathcal{L} = \mathbb{E}_{V,\epsilon,t}\left[\left\|\epsilon - \epsilon_\theta(\mathbf{x}_t, \mathbf{z}_b, t)\right\|^2\right]$$

该设计使扩散模型能够从统一的脑表征中解码出具有语义准确性和时间一致性的动态视频帧序列。

## 实验与关键发现

### 实验设置

CineBrain数据集包含6名受试者（21–26岁，2男4女），每名受试者贡献约6小时的同步fMRI与EEG记录，同时采集ECG信号。fMRI预处理采用fMRIPrep流程，并引入4秒延迟以补偿血氧动力学响应，随后进行z-score标准化。EEG预处理包括0.1–30 Hz带通滤波、50 Hz陷波滤波、基于QRS的心电伪影去除以及独立成分分析（ICA）。视觉皮层ROIs包含8,405个体素，扩展的听觉+视觉ROIs（CineSync⋆变体）共包含18,946个体素。

评估指标分为视频级语义指标和帧级感知指标两类：视频级指标包括2-way准确率（判断两段视频中哪段与脑信号匹配）和50-way准确率；帧级指标包括FVD（Fréchet Video Distance）、SSIM和PSNR。所有结果均在CineBrain数据集上以留一受试者交叉验证方式报告。

### 主要结果

Table 3报告了CineSync与各基线在全受试者上的平均性能。CineSync（fMRI+EEG联合建模）在视频级语义指标上达到**2-way准确率0.909**，显著优于仅使用fMRI的CineSync-fMRI（0.893, +0.016）和仅使用EEG的CineSync-EEG（0.891, +0.018）。在帧级质量指标上，CineSync取得**FVD 52.78**，相比CineSync-fMRI（57.47）和CineSync-EEG（53.75）分别降低4.69和0.97，表明联合建模双模态脑信号有效提升了重建视频的时序一致性和视觉质量。

进一步，当在fMRI输入中纳入听觉皮层ROIs后，**CineSync⋆的2-way准确率提升至0.926**（+0.017），FVD降至44.77（−8.01），达到最优性能。这一结果表明听觉皮层的激活信息对视觉知觉解码具有显著的增强作用，验证了跨模态脑信号整合的核心假设。Figure 6的定性对比显示，CineSync重建的视频帧在语义准确性和时序一致性上均优于单模态变体。

### 融合架构消融

Table 2对比了五种fMRI-EEG融合编码器架构的性能。**双转换器分离编码（Dual Transformer Fusion）在所有指标上均取得最优结果**，2-way准确率0.929，50-way准确率0.324，FVD 51.53。相比之下，早期共享自注意力的联合Transformer（Joint Transformer）2-way准确率降至0.924，FVD显著恶化至128.0。两阶段融合、交叉注意力融合和空间拼接策略的性能均不及双转换器方案。这一消融实验明确揭示：**在特征提取阶段减少fMRI与EEG的早期交互，让各模态先独立编码再通过融合MLP进行末期融合，是最有效的多模态整合策略**。其因果机制在于fMRI和EEG具有本质不同的时空特性——前者为高空间分辨率慢变信号，后者为高时间分辨率快变信号——过早的跨模态交互会干扰各自的特征提取过程。

### 对比学习损失消融

多层级对比学习对齐损失对整体性能贡献显著。消融实验表明，移除任一对齐损失项（fMRI-视频、fMRI-文本、EEG-视频、EEG-文本、fMRI-EEG中的任意一项）均导致2-way准确率和FVD指标下降。五个损失项联合优化使脑表征同时与视觉语义和文本语义对齐，并实现fMRI与EEG表征之间的跨模态对齐，构成了CineSync性能的关键支撑。

### EEG表征容量消融

增加EEG的表征容量（如增加token数量）能进一步提高重建质量。这一发现凸显了EEG在捕捉快速神经动态中的关键作用——高时间分辨率的EEG信号携带了fMRI无法提供的毫秒级神经响应信息，增强其编码能力直接转化为视频重建的时序精度提升。

### 失败模式与局限性

尽管CineSync取得了显著进展，但以下局限性需要关注：首先，数据集仅包含6名受试者，样本代表性有限，模型在更大规模、更多样化人群上的泛化能力尚未验证。其次，视频刺激内容单一（仅选自《生活大爆炸》情景剧），可能未涵盖野外复杂视听场景的多样性，模型在更广泛刺激类型下的解码性能需要进一步检验。此外，fMRI-EEG同步采集依赖3T扫描仪和定制非磁性脑电帽，实验门槛较高，其他站点复现需额外校准。这些因素限制了当前结论的外部有效性，在推广到临床或实际应用场景前需要更多验证工作。

![[assets/figures/papers/paper_list_l2045_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_CineBrain_A_Large/figures/009_Table_3.jpg]]
*Table 3: Performance comparison of CineSync with baselines. The average metrics across all subjects are reported. CineSync⋆ indicates the experiment that includes audio-related ROIs in fMRI. Bold denotes the best performance, while underlined denotes the second-best*

![[assets/figures/papers/paper_list_l2045_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_CineBrain_A_Large/figures/006_Table.jpg]]
*Table: Cross-AttentionTable 2. Performance comparison of different multimodal encoder structures. We evaluate all variants using video-level semantic metrics and frame-level perceptual metrics. Bold denotes the best performance, while underlined denotes the second-best*

![[assets/figures/papers/paper_list_l2045_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_CineBrain_A_Large/figures/002_Table_1.jpg]]
*Table 1: Overview of the CineBrain Dataset. We present detailed statistics of our proposed CineBrain dataset and compare it with other existing video-based brain datasets. CineBrain provides comprehensive multimodal brain recordings during audiovisual stimulation. Each participant watched a total of 6 hours of audiovisual stimuli, corresponding to approximately 27,000 frames of fMRI data*

![[assets/figures/papers/paper_list_l2045_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_CineBrain_A_Large/figures/003_Figure_2.jpg]]
*Figure 2: Visualization of fMRI and EEG Responses in Cine-Brain. fMRI and EEG responses of subjects 1–4 to identical stimuli, illustrating individual differences in brain activation*

## 定位与知识库关联

### 1. 技术脉络与差异化定位

CineSync 的核心问题设定——从脑信号重建视觉内容——根植于神经解码（neural decoding）这一交叉领域。传统工作主要沿两条单模态路径展开：fMRI 解码与 EEG 解码。

**fMRI 解码线**以高空间分辨率的血氧水平依赖信号为基础，代表性工作包括从早期视觉皮层体素重建静态图像的方法，以及近年来利用扩散模型实现高质量自然图像重建的 **MindEye**（Scotti et al., 2024）和 **Brain-Diffuser**（Ozcelik & VanRullen, 2023）。这些方法的核心瓶颈在于：fMRI 的时间分辨率受限于血液动力学响应函数（HRF），单个体素的时间序列采样间隔通常为数秒，难以捕捉刺激内容的快速动态变化。

**EEG 解码线**以毫秒级时间分辨率见长，代表性工作如 **EEG2Video**（Singh et al., 2024）利用头皮电位重建视频内容，但受限于 EEG 的空间模糊性和低信噪比，其重建结果在语义保真度和空间细节上始终落后于 fMRI 方法。

CineSync 的根本性突破在于识别出上述两条路径的**互补性信息瓶颈**：fMRI 提供“在哪里激活”的空间精确性，EEG 提供“何时激活”的时间动态性，而大脑在自然视听刺激下的多感官整合本质使得单一模态的信息必然是不完整的。这一洞察驱动了三个关键设计选择：

1. **同步采集范式**：不同于以往工作中 fMRI 和 EEG 分时或分任务采集的做法，CineBrain 数据集在 3T MRI 扫描仪内使用定制非磁性脑电帽实现同步记录，使得两种信号在刺激时间轴上天然对齐，为跨模态互补建模提供了数据基础。

2. **双转换器分离编码**：在五种融合架构的系统性比较中（Figure 4，Table 2），联合自注意力（Joint Transformer）的早期交互策略表现最差（FVD 128.0），而双转换器独立编码后经融合 MLP 进行末期融合的策略取得了最优性能（FVD 51.53）。这一消融结果揭示了一个关键因果机制：fMRI 和 EEG 的特征空间差异显著，过早的跨模态交互会引入噪声并破坏各自模态内的表征学习。分离编码允许每个转换器专注于自身模态的统计特性，仅在语义对齐阶段进行跨模态约束。

4. **多层级对比学习对齐**：CineSync 的对比损失设计覆盖了完整的模态对齐图：fMRI-视频（L_fv）、fMRI-文本（L_ft）、EEG-视频（L_ev）、EEG-文本（L_et）以及 fMRI-EEG（L_fe）。消融实验表明，缺少任一对齐损失均导致指标下降，验证了多模态语义锚定对解码质量的关键作用。这一设计超越了仅依赖扩散重建损失的端到端训练范式，通过显式的语义空间约束将脑表征与视觉-文本嵌入对齐。

### 2. 与邻近工作的关系

**与 fMRI-to-Image 方法的边界**：CineSync 处理的是视频重建而非静态图像重建，其挑战在于时间一致性和动态语义的保持。CineSync 通过 EEG 分支引入的时间动态信息是静态 fMRI 解码方法所不具备的。同时，CineSync 采用 CogVideoX-5B 作为扩散先验并通过 LoRA 微调，与 MindEye 等使用 Stable Diffusion 的方法在生成架构上属于同一范式（扩散先验 + 脑条件注入），但 CineSync 的脑条件来自融合后的多模态表征 z_b 而非纯 fMRI 嵌入。

**与 EEG-to-Video 方法的边界**：CineSync 的 EEG 分支与 EEG2Video 等工作的核心差异在于，CineSync 不试图从 EEG 独立重建视频，而是将 EEG 作为 fMRI 空间信息的补充时间线索。Table 3 显示，CineSync-EEG 单独重建的性能（2-way 0.891，FVD 53.75）显著弱于 CineSync-fMRI（2-way 0.893，FVD 57.47），但两者联合后性能跃升（2-way 0.909，FVD 52.78），证实了 EEG 的增益并非来自其独立解码能力，而是来自对 fMRI 时间盲区的补充。

**与多模态脑解码方法的关系**：在脑信号融合层面，CineSync 与 **BrainCLIP**（Liu et al., 2023）等使用对比学习对齐脑信号与视觉语义的工作共享方法论基因，但 CineSync 将对齐目标从静态图像扩展到了视频-文本联合空间，并引入了 fMRI-EEG 跨模态对齐损失 L_fe 作为额外的正则化约束。

### 3. 适用边界与局限

CineSync 及 CineBrain 数据集的适用性受以下因素制约：

**受试者规模与泛化性**：数据集仅包含 6 名受试者（2 男 4 女，年龄 21–26 岁），属于小样本神经解码研究的典型规模，但限制了受试者间泛化分析和个体差异建模的统计效力。模型在跨受试者设置下的性能衰减程度需要进一步验证。

**刺激内容单一性**：视频刺激全部选自情景剧《生活大爆炸》（The Big Bang Theory），该剧以室内对话场景为主，视觉动态范围有限，且语言内容高度结构化。模型在野外复杂视听场景（如动作电影、体育赛事、自然纪录片）下的重建能力尚未验证。此外，英语对白的语言特异性可能影响跨语言场景的文本对齐效果。

**采集设备依赖性**：fMRI-EEG 同步采集依赖 3T MRI 扫描仪和定制非磁性脑电帽，设备门槛高，且 fMRI 的 4 秒血液动力学滞后校正参数和 EEG 的 QRS 心电伪影去除流程可能对其他扫描站点或设备型号需要重新校准。

**ROI 选择的先验依赖性**：CineSync 的 fMRI 输入限定于预定义的视觉皮层和听觉皮层 ROI（Figure 3），CineSync* 变体通过扩展听觉 ROI 将 2-way 准确率从 0.909 提升至 0.926（Table 3），表明 ROI 选择对性能有显著影响。但这一先验选择可能遗漏其他对视频理解有贡献的脑区（如顶叶注意网络、颞叶语义区），全脑体素建模的可行性及计算成本需要进一步探索。

### 4. 开放问题

1. **跨刺激域泛化**：CineSync 的多模态融合策略能否在未经微调的情况下推广到其他类型的自然视听刺激（如电影片段、音乐视频、户外场景），以及跨语言/文化的内容解码？这需要更大规模和更多样化的同步 fMRI-EEG 数据集来验证。

2. **听觉解码与跨模态转换**：CineSync* 的结果暗示听觉皮层激活对视觉重建有显著增益，但 CineBrain 数据集本身包含同步音频刺激和听觉脑区响应，能否支持直接的听觉内容解码（从脑信号重建音频）或 fMRI↔EEG 的跨模态信号转换？这将是数据集潜在的下游扩展方向。

3. **数据效率**：在仅用少量同步记录数据（如几分钟而非 6 小时）的情况下，CineSync 的多模态对比学习框架能否保持可靠的视频重建性能？这对于实际应用（如临床或消费级脑机接口）至关重要。

4. **融合策略的自适应优化**：当前 CineSync 采用固定的末期融合策略，但五种对比损失的权重分配以及融合时机的选择（早期 vs 晚期）是否存在刺激内容或受试者特异性的最优解？自适应融合机制可能进一步提升性能。

5. **个体差异建模**：Figure 2 显示不同受试者在相同刺激下的 fMRI 和 EEG 响应存在显著个体差异，当前模型在受试者内训练-测试设置下评估，跨受试者泛化和个性化微调的策略值得深入研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/CineBrain_A_Large_Scale_Multi_Modal_Audiovisual_Brain_Dataset_for_Brain_Conditioned_Video_Generation.pdf]]
