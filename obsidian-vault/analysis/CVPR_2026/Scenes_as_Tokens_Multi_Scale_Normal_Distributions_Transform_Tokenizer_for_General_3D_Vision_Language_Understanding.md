---
title: "Scenes as Tokens: Multi-Scale Normal Distributions Transform Tokenizer for General 3D Vision-Language Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Scenes_as_Tokens_Multi_Scale_Normal_Distributions_Transform_Tokenizer_for_General_3D_Vision_Language_Understanding.pdf
project_link: null
code_link: null
aliases:
- Scenes_as_Tokens
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 多尺度NDT（Normal Distributions Transform）网格表示——在细粒度尺度用高斯统计量（均值与协方差）保留原始几何信息，在粗粒度尺度聚合大范围空间区域捕获全局语义；配合MSDec（Multi-Scale NDT Decoder）的跨尺度渐进交叉注意力融合，从粗糙到精细逐层整合特征。
primary_logic: 摒弃传统点云下采样，采用源自SLAM的NDT网格将点云划分为规则单元并用高斯分布建模局部表面，多分辨率网格天然同时保留局部几何细节和全局场景结构；再通过transformer解码器以多尺度特征作为Key/Value，以可学习查询令牌逐步融合跨尺度信息，输出紧凑且信息丰富的场景令牌。MSDec进一步被复用为统一接口，支持用户交互提示和分割掩码解码，实现单一架构内多任务统一。
claims:
- NDT表示在保留局部几何细节的同时大幅压缩内存，细粒度网格保留原始点统计量，粗粒度网格编码全局上下文
- MSDec通过R个transformer解码器层渐进融合多尺度NDT特征，生成整体场景令牌
- MSDec复用为统一接口，同时支持用户交互提示（点、框、掩码）和分割掩码解码
- NDT-based tokenization在全部任务上一致优于下采样baseline
---

# Scenes as Tokens: Multi-Scale Normal Distributions Transform Tokenizer for General 3D Vision-Language Understanding

> [!tip] 核心洞察
> 摒弃传统点云下采样，采用源自SLAM的NDT网格将点云划分为规则单元并用高斯分布建模局部表面，多分辨率网格天然同时保留局部几何细节和全局场景结构；再通过transformer解码器以多尺度特征作为Key/Value，以可学习查询令牌逐步融合跨尺度信息，输出紧凑且信息丰富的场景令牌。MSDec进一步被复用为统一接口，支持用户交互提示和分割掩码解码，实现单一架构内多任务统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | 场景即令牌：面向通用3D视觉语言理解的多尺度正态分布变换分词器 |
| 英文题名 | Scenes as Tokens: Multi-Scale Normal Distributions Transform Tokenizer for General 3D Vision-Language Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21191) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | NDTokenizer3D |
| Dataset | Multi3DRefer, ScanQA, SQA3D, Scan2Cap |

> [!tip] 效果简介
> - Multi3DRefer 上，mIoU 46.0 vs 42.7 (3D-LLaVA) (+3.3)。
> - ScanQA 上，CiDEr / METEOR 98.6 / 19.4 vs 92.6 / 18.4 (second-best results) (+6.0 / +1.0)。
> - SQA3D 上，EM / EM-R 54.4 / 57.1。

## 概要

**核心问题**：将大规模高分辨率3D点云压缩为大语言模型（LLM）可消费的有界长度令牌序列，同时最小化信息损失并捕捉多尺度物体-环境关系。现有方法依赖粗暴下采样，导致细粒度几何细节丢失且缺乏有效的全局抽象结构建模。

**核心方法**：NDTokenizer3D 提出三阶段场景分词流水线——首先构建多尺度NDT（Normal Distributions Transform）网格表示，在细粒度尺度用高斯统计量（均值与协方差）保留原始几何信息，在粗粒度尺度聚合大范围空间区域捕获全局语义；继而通过Point Transformer v3提取多尺度NDT特征；最后以MSDec（Multi-Scale NDT Decoder）的R层transformer解码器从粗到细渐进融合跨尺度特征，输出紧凑且信息丰富的整体场景令牌。MSDec进一步被复用为统一接口，同时支持用户交互提示（点、框、掩码）和分割掩码解码，实现单一架构内多任务统一。

**方法定位**：NDTokenizer3D 属于通用3D视觉语言模型（Generalist 3D VLM），与 **3D-LLaVA**（Boora & Nießner, CVPR 2025）、**LEO**（Huang et al., arXiv 2023）、**Chat-Scene**（Huang et al., NeurIPS 2024）、**Scene-LLM**（Fu et al., WACV 2025）、**LSceneLLM**（Zhi et al., CVPR 2025）等同期工作形成直接或间接对比。其核心差异在于：将源自SLAM的NDT网格引入3D分词，以高斯统计量替代朴素点云下采样，并通过MSDec实现跨尺度渐进融合与多任务统一接口，从而在保留几何细节与捕获全局语义之间取得关键平衡。

**主要结果**：
- **3D指代分割**：Multi3DRefer上mIoU达46.0，较3D-LLaVA提升+3.3。
- **3D密集描述**：ScanQA上CiDEr达98.6、METEOR达19.4，分别超越次优结果+6.0和+1.0。
- **3D问答**：SQA3D上EM达54.4、EM-R达57.1；Scan2Cap上C@0.5达79.0。
- **幻觉抑制**：3D-POPE基准上，Random/Popular/Adversarial三种设定下均取得最低幻觉率。
- **消融验证**：NDT-based tokenization在所有任务上一致优于朴素多尺度下采样baseline；三尺度配置在细节保留与推理稳定性之间取得最佳平衡；查询令牌数量在400-850处趋于饱和，表明MSDec在此范围内已捕获足够场景信息。



### 3D视觉语言理解的兴起与核心瓶颈

随着大语言模型（LLM）在自然语言处理领域的突破，研究者正积极探索将其与3D场景理解相结合，构建能够同时进行语言推理和空间感知的通用3D视觉语言模型（3D VLM）。这类模型有望统一支持3D视觉问答、稠密描述、指称分割等多种任务，并在具身智能、AR/VR等应用中发挥关键作用。

然而，将LLM引入3D场景理解面临一个根本性瓶颈：**如何将大规模高分辨率3D点云压缩为LLM可消费的有界长度令牌序列，同时最小化信息损失并捕捉多尺度物体-环境关系**。LLM受限于固定的上下文窗口和计算预算，要求输入令牌数量有严格上限；而真实3D场景的点云往往包含数十万甚至数百万个点，直接输入在计算上不可行。

### 现有方法的局限：粗暴下采样导致几何信息丢失

当前主流的通用3D VLM（如**3D-LLaVA**，Boora and Nießner, CVPR 2025；**LEO**，Huang et al., arXiv 2023；**Chat-Scene**，Huang et al., NeurIPS 2024；**Scene-LLM**，Fu et al., WACV 2025；**LSceneLLM**，Zhi et al., CVPR 2025）普遍采用**朴素多尺度体素下采样**策略来压缩点云。具体而言，它们将点云划分为不同分辨率的体素网格，在每个体素内仅保留坐标和RGB颜色信息，丢弃了局部点集的统计分布特性。

这种粗暴压缩方式存在两个关键缺陷：
1. **细粒度几何细节丢失**：下采样只保留了点的位置和颜色，忽视了局部表面的形状信息（如平面、曲面、边缘的分布特征），导致模型无法精确理解物体的几何结构。
2. **全局抽象结构建模不足**：简单的多尺度特征拼接或独立处理缺乏跨尺度的结构化交互，难以有效融合局部细节与全局语义。

### 核心动机：从SLAM借鉴NDT表示实现信息高效压缩

本文的核心动机源于一个关键观察：**源自SLAM（同时定位与建图）领域的正态分布变换（Normal Distributions Transform, NDT）提供了一种天然适合3D场景压缩的表示形式**。NDT将点云划分为规则网格单元，对每个单元内的点集用高斯分布（均值与协方差）建模——均值捕获局部中心位置，协方差矩阵编码局部表面的分布形状（如平面性、方向性）。

这一表示具有三重优势：
- **信息保真度**：高斯统计量（均值3维+协方差9维）以极紧凑的形式保留了局部几何的完整统计信息，远优于仅保留坐标的朴素下采样；
- **多尺度天然性**：通过调整网格分辨率，NDT可同时构建细粒度网格（保留细节）和粗粒度网格（捕获全局语义），形成多尺度层次表示；
- **内存高效**：每个NDT单元仅需固定维度的统计量，大幅压缩了原始点云的存储和计算开销。

基于此，本文提出**NDTokenizer3D**，核心动机是**摒弃传统点云下采样范式，采用多尺度NDT网格作为3D场景的"分词"基础，将场景转化为信息丰富、结构紧凑的令牌序列，从而为LLM提供高质量的3D场景理解输入**。这一设计不仅解决了信息损失问题，还通过配套的多尺度NDT解码器（MSDec）实现了跨尺度特征的渐进融合，并进一步将解码器复用为统一接口，支持用户交互提示和分割掩码解码，在单一架构内统一多种3D理解任务。



## 核心方法与创新机理

NDTokenizer3D的核心创新在于用**多尺度正态分布变换（NDT）网格表示**替代了现有通用3D VLM中普遍采用的朴素点云下采样策略，并配套设计了**多尺度NDT解码器（MSDec）**作为跨尺度特征融合与多任务统一接口。这两个设计共同解决了“将大规模高分辨率3D点云压缩为LLM可消费的有界长度令牌序列，同时最小化信息损失并捕捉多尺度物体-环境关系”这一瓶颈问题。

### 从下采样到统计建模：多尺度NDT表示

现有通用3D VLM（如**3D-LLaVA**，Boora & Nießner, CVPR 2025）通常采用多尺度体素下采样来压缩点云——在每个尺度上仅保留体素内点的坐标和RGB颜色值，直接丢弃了局部表面的几何分布信息。这种粗暴压缩导致细粒度几何细节不可逆地丢失，且缺乏有效的全局抽象结构建模能力。

NDTokenizer3D的关键改变在于：借鉴SLAM领域成熟的NDT思想，将点云空间划分为规则的三维网格单元，但**不直接存储点坐标，而是对每个单元内的点集计算高斯统计量——均值$\mu_{r}^{j}$（表征局部表面中心位置）和协方差$\pmb{\Sigma}_{r}^{j}$（表征局部表面分布形状与方向）**：

$$\mu_{r}^{j} = \frac{1}{n} \sum_{i=1}^{n} x_{i}, \quad \pmb{\Sigma}_{r}^{j} = \frac{1}{n-1} \sum_{i=1}^{n} (x_{i} - \mu_{r}^{j})(x_{i} - \mu_{r}^{j})^{T}$$

这一表示的核心优势在于**信息密度**：一个NDT单元仅需15维特征向量（3维均值 + 9维协方差 + 3维多视角投影RGB颜色），却能以二阶统计量完整刻画单元内所有点的空间分布形态，在同等内存预算下保留了远超朴素下采样的几何信息量。多尺度网格的构建进一步实现了信息的分层编码——细粒度尺度保留精细的局部表面几何，粗粒度尺度聚合大范围空间区域以捕获全局场景语义。消融实验（Table 3）直接验证了这一设计的决定性作用：NDT-based tokenization在所有四项任务（Multi3DRefer、ScanQA、SQA3D、Scan2Cap）上**一致优于**使用相同点数体素下采样的baseline。

### 从特征拼接到渐进融合：MSDec跨尺度解码器

多尺度特征的有效融合是另一个关键创新点。现有方法通常对多尺度特征进行简单拼接或独立处理，缺乏跨尺度间的信息交互。NDTokenizer3D提出的**MSDec（Multi-Scale NDT Decoder）**由R层transformer解码器层堆叠而成，每层以对应尺度的NDT特征作为Key和Value，以一组可学习的查询令牌作为Query，通过交叉注意力机制从粗到细逐步整合多尺度信息：

$$\tilde{\mathbf{Q}}_{r} = \mathrm{CrossAttn}(\mathbf{Q}_{r}, \mathbf{K}_{r}, \mathbf{V}_{r}), \quad \hat{\mathbf{Q}}_{r} = \mathrm{SelfAttn}(\tilde{\mathbf{Q}}_{r}), \quad \mathbf{Q}_{r+1} = \mathrm{FFN}(\hat{\mathbf{Q}}_{r})$$

这种设计使查询令牌在解码过程中先接触粗粒度的全局语义，再逐层融入细粒度的局部几何细节，最终输出紧凑且信息丰富的整体场景令牌$\mathbf{Q}_{R}$。消融实验表明，三尺度配置（$r = \{2, 3, 4\}$）在细节保留与推理稳定性之间取得了最佳平衡，而查询令牌数量在400–850范围内性能趋于饱和（Table 4, Table 5），说明MSDec已在此范围内充分捕获了场景信息。

### 从多分支到统一接口：MSDec的复用设计

更具创新性的是，MSDec被进一步**复用为统一接口**，同时支持用户交互提示和分割掩码解码，消除了现有方法中需要额外任务特定模块的架构冗余。具体而言：用户输入的交互信号（点、边界框或掩码）经掩码化处理后作为额外查询令牌输入MSDec，生成引导令牌$\mathbf{E}_{P}$；而LLM生成的[SEG]特殊令牌则触发分割查询，同样经MSDec解码生成3D分割掩码。这一设计使NDTokenizer3D在**单一架构内**统一了3D VQA、稠密描述、指代分割和交互式场景理解等多类任务，显著区别于需要独立后处理分支的baseline方法。

### 创新总结

总结而言，NDTokenizer3D相对于现有通用3D VLM的核心创新体现在三个changed slots上：

| 设计维度 | Baseline做法 | NDTokenizer3D创新 |
|---------|-------------|------------------|
| **3D场景压缩** | 朴素多尺度体素下采样（仅保留坐标+RGB） | 多尺度NDT网格表示（高斯均值+协方差统计量建模局部表面） |
| **多尺度融合** | 单尺度处理或独立多尺度特征拼接 | MSDec：R层transformer解码器从粗到细渐进交叉注意力融合 |
| **任务统一** | 任务特定模块或额外后处理分支 | MSDec复用为统一接口，同时支持用户提示和分割掩码解码 |

这三个改变的因果传导链为：NDT统计量在压缩中保留了几何信息→MSDec在融合中有效整合了跨尺度特征→统一的MSDec接口消除了任务特异性架构需求，最终在Multi3DRefer上以46.0 mIoU超越3D-LLaVA +3.3点，在ScanQA上以98.6 CiDEr超越次优结果+6.0点，并在3D-POPE幻觉评估中取得所有设定下的最低幻觉率。



NDTokenizer3D 的整体架构围绕一个核心设计原则展开：**将高分辨率3D点云压缩为LLM可消费的有界长度令牌序列，同时最小化信息损失并捕捉多尺度物体-环境关系**。现有方法依赖粗暴下采样导致细粒度几何细节丢失，且缺乏有效的全局抽象结构建模。NDTokenizer3D 通过引入源自SLAM的**多尺度NDT（Normal Distributions Transform）网格表示**与**跨尺度渐进融合解码器（MSDec）**，从根本上改变了3D场景到语言模型的压缩方式。

### 三阶段场景分词流水线

整个pipeline由三个紧密衔接的阶段构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2175_https_arxiv_org_abs_2511_21191/figures/002_Figure_2.jpg]]
*Figure 2: NDTokenizer3D is a general-purpose 3D VLM that supports a wide range of 3D understanding tasks. The model introduces a novel three-stage scene tokenization pipeline that constructs multi-scale NDT representations and aggregates them via MSDec to generate holistic scene tokens. The lower-left shows MSDec with R transformer decoder layers that integrate multi-scale NDT features, using them as Key and Value. Beyond feature integration, MSDec also acts as a unified interface for user prompting and mask decoding*

**Stage 1 — 多尺度NDT构建（Multi-Scale NDT Construction）**：给定原始高分辨率点云，系统首先将其划分为多分辨率规则网格。在每个网格单元内，计算包含点的**高斯均值**$\mu_r^j$（中心位置）和**协方差**$\pmb{\Sigma}_r^j$（局部表面分布形状）：
$$\mu_{r}^{j} = \frac{1}{n} \sum_{i=1}^{n} x_{i}, \ \pmb{\Sigma}_{r}^{j} = \frac{1}{n-1} \sum_{i=1}^{n} (x_{i} - \mu_{r}^{j})(x_{i} - \mu_{r}^{j})^{T}$$
细粒度尺度（如$r=4$）的NDT单元保留原始点云的精细几何统计量，粗粒度尺度（如$r=2$）的单元则聚合大范围空间区域以捕获全局语义。同时，通过多视角投影补充RGB颜色信息：
$$c_{r}^{j} = \frac{1}{N_{I}} \sum_{k=1}^{N_{I}} I_{k}(u_{k}, v_{k}), \ [u_{k}, v_{k}]^{T} = P(\mu_{r}^{j} | k)$$
每个NDT单元的描述子由3D均值(3维)、协方差矩阵(9维)和RGB颜色(3维)拼接为15维向量：
$$\mathbf{C}_{r} = \{C_{r}^{j}\}_{j=1}^{N_{r}} \in \mathbb{R}^{N_{r} \times 15}, C_{r}^{j} = [\mu_{r}^{j}; \Sigma_{r}^{j}; c_{r}^{j}]$$

**Stage 2 — 3D编码器（3D Encoder Φ）**：采用 **Point Transformer v3 (PTv3)** 对多尺度NDT单元描述子进行特征提取，输出多尺度NDT特征$\mathbf{F}_r = \Phi(\mathbf{C}_r)$。PTv3的transformer架构天然适合处理NDT单元之间的空间关系建模。

**Stage 3 — 多尺度NDT解码器（MSDec）**：这是整个架构的核心创新模块。MSDec由$R$层transformer解码器层构成，以多尺度NDT特征作为Key和Value，以可学习查询令牌作为Query，从粗糙到精细逐层融合跨尺度信息：
$$\tilde{\mathbf{Q}}_{r} = \mathrm{CrossAttn}(\mathbf{Q}_{r}, \mathbf{K}_{r}, \mathbf{V}_{r}), \ \hat{\mathbf{Q}}_{r} = \mathrm{SelfAttn}(\tilde{\mathbf{Q}}_{r}), \ \mathbf{Q}_{r+1} = \mathrm{FFN}(\hat{\mathbf{Q}}_{r})$$
每一层依次执行交叉注意力（查询与对应尺度$r$的NDT特征交互）、自注意力和前馈网络，最终输出整体场景令牌$\mathbf{Q}_R$。这种由粗到细的渐进融合机制确保全局语义与细粒度几何细节的有效整合。

### 多模态对齐与LLM端点

MSDec输出的场景令牌$\mathbf{Q}_R$通过一个**多模态对齐头**$f_{mm}$（实现为两层MLP）投影到LLM输入空间，生成3D场景令牌$\mathbf{E}_V$。系统采用**LLaVA-1.5-7B**作为LLM端点，接收拼接的多模态输入序列：
$$\hat{a} = \mathrm{LLM}([\mathbf{E}_{V}; \mathbf{E}_{P}; \mathbf{E}_{T}]), \ [\mathrm{SEG}] \subset \hat{a}$$
其中$\mathbf{E}_P$为引导令牌（用户交互提示），$\mathbf{E}_T$为文本令牌。LLM生成文本回复，若回复中包含特殊令牌[SEG]，则自动触发分割掩码解码过程。

### MSDec的统一接口复用

MSDec被进一步复用为**统一接口**，同时支持两类关键功能：

- **用户交互提示**：用户输入（点坐标、边界框或掩码）经掩码化处理后作为额外查询令牌输入MSDec，生成引导令牌$\mathbf{E}_P$，实现灵活的人机交互场景理解。
- **分割掩码解码**：当LLM输出[SEG]令牌时，触发一组分割查询令牌，同样通过MSDec与多尺度NDT特征交互，生成3D分割掩码。

这种设计使得单一架构能够统一支持3D视觉问答、密集描述、指代分割等多任务，避免了传统方法中任务特定模块的冗余。

### 关键设计决策与因果机制

NDTokenizer3D相比baseline方法**3D-LLaVA**（Boora and Nießner, CVPR 2025）的核心改进在于两个因果控制点：

1. **NDT统计量替代朴素下采样**：传统方法对点云进行多尺度体素下采样时仅保留坐标和RGB，丢失了局部几何分布信息。NDT单元的高斯统计量（均值与协方差）在同等压缩率下保留了更丰富的表面几何特征。消融实验（Table 3）验证了NDT-based tokenization在所有任务上一致优于下采样baseline。

2. **跨尺度渐进融合替代独立多尺度处理**：MSDec的逐层交叉注意力机制实现了从粗到细的特征整合，相比简单的多尺度特征拼接，更有效地平衡了全局语义与局部细节。三尺度配置（$r=\{2,3,4\}$）在细节保留与推理稳定性之间达到最佳平衡（Table 4）。

### 训练策略

训练分为两个阶段：
- **Stage 1（预训练）**：组合分类交叉熵损失、二值交叉熵+Dice分割损失和2D-3D语义对齐余弦相似度损失，将CLIP图像特征提升到3D空间进行逐单元对齐。
- **Stage 2（指令微调）**：组合下一令牌生成交叉熵损失、掩码预测损失和预测-真实答案隐藏状态余弦相似度损失，使用4× NVIDIA A100 GPU配合DeepSpeed进行分布式优化，LLM采用LoRA微调。

> **注意**：Stage 1预训练使用的3D实例分割数据集具体名称在可用上下文中未明确给出，需要手动核实。NDT网格分辨率对不同场景类型的通用性实验仅在室内数据集上进行，室外场景的泛化能力尚待验证。

### 补充图表

![[assets/figures/papers/paper_list_l2175_https_arxiv_org_abs_2511_21191/figures/001_Figure_1.jpg]]
*Figure 1: We introduce NDTokenizer3D, a generalist 3D VLM that bridges language-level reasoning with spatial understanding. By tokenizing complex 3D scenes into information-rich representations, NDTokenizer3D enables diverse tasks such as 3D Visual Question Answering, Dense captioning, and Referring Segmentation within a unified and interactive framework*



### 多尺度NDT场景表示

NDTokenizer3D的核心创新在于摒弃传统点云下采样，转而采用源自SLAM的**正态分布变换（Normal Distributions Transform, NDT）**网格对3D场景进行结构化压缩。给定高分辨率原始点云，在尺度 $r$ 下将空间划分为规则网格，对每个网格单元 $j$ 内包含的 $n$ 个3D点计算高斯统计量：

$$\mu_{r}^{j} = \frac{1}{n} \sum_{i=1}^{n} x_{i}, \quad \pmb{\Sigma}_{r}^{j} = \frac{1}{n-1} \sum_{i=1}^{n} (x_{i} - \mu_{r}^{j})(x_{i} - \mu_{r}^{j})^{T}$$

其中 $\mu_{r}^{j} \in \mathbb{R}^{3}$ 表示单元内点的空间均值（中心位置），$\pmb{\Sigma}_{r}^{j} \in \mathbb{R}^{3 \times 3}$ 表示协方差矩阵（编码局部表面的分布形状与方向）。这一统计量化的表示方式在细粒度尺度上最大程度保留了原始几何细节，同时在粗粒度尺度上通过大范围空间聚合捕获全局语义上下文。

为补充视觉外观信息，通过多视角投影将2D图像颜色映射到NDT单元：

$$c_{r}^{j} = \frac{1}{N_{I}} \sum_{k=1}^{N_{I}} I_{k}(u_{k}, v_{k}), \quad [u_{k}, v_{k}]^{T} = P(\mu_{r}^{j} | k)$$

即将单元均值 $\mu_{r}^{j}$ 投影到第 $k$ 个视角的2D图像平面，取所有可见视角的RGB平均值作为该单元的颜色描述子。

最终每个NDT单元的输入特征由均值、协方差和颜色拼接为15维向量：

$$\mathbf{C}_{r} = \{C_{r}^{j}\}_{j=1}^{N_{r}} \in \mathbb{R}^{N_{r} \times 15}, \quad C_{r}^{j} = [\mu_{r}^{j}; \Sigma_{r}^{j}; c_{r}^{j}]$$

其中 $N_{r}$ 为尺度 $r$ 下的NDT单元总数。这些描述子随后输入基于**Point Transformer v3 (PTv3)** 的3D编码器 $\Phi$，提取多尺度NDT特征 $\mathbf{F}_{r} = \Phi(\mathbf{C}_{r})$。

### 多尺度NDT解码器（MSDec）

MSDec是NDTokenizer3D的核心融合模块，由 $R$ 层transformer解码器堆叠而成，以从粗到细的方式渐进融合跨尺度NDT特征。每一层的更新过程为：

$$\tilde{\mathbf{Q}}_{r} = \mathrm{CrossAttn}(\mathbf{Q}_{r}, \mathbf{K}_{r}, \mathbf{V}_{r})$$
$$\hat{\mathbf{Q}}_{r} = \mathrm{SelfAttn}(\tilde{\mathbf{Q}}_{r})$$
$$\mathbf{Q}_{r+1} = \mathrm{FFN}(\hat{\mathbf{Q}}_{r})$$

其中 $\mathbf{Q}_{r}$ 为第 $r$ 层的可学习查询令牌，$\mathbf{K}_{r}$ 和 $\mathbf{V}_{r}$ 由对应尺度 $r$ 的NDT特征 $\mathbf{F}_{r}$ 线性投影得到。交叉注意力层使查询令牌能够从当前尺度的场景特征中提取信息，自注意力层促进查询间的信息交互，前馈网络完成非线性变换。通过 $R$ 层从最粗尺度到最细尺度的逐步融合，MSDec最终输出整体场景令牌 $\mathbf{Q}_{R}$，有效整合了全局语义与细粒度几何细节。

### 多模态对齐与LLM交互

MSDec输出的场景令牌经**多模态对齐头** $f_{mm}$（两层MLP）投影到LLM输入空间，生成场景令牌 $\mathbf{E}_{V}$。当用户提供交互提示（点、框或掩码）时，这些提示经掩码化处理后作为额外查询令牌同样通过MSDec生成引导令牌 $\mathbf{E}_{P}$。最终拼接场景令牌、引导令牌和文本令牌 $\mathbf{E}_{T}$ 输入LLM：

$$\hat{a} = \mathrm{LLM}([\mathbf{E}_{V}; \mathbf{E}_{P}; \mathbf{E}_{T}]), \quad [\mathrm{SEG}] \subset \hat{a}$$

若LLM在回复中生成特殊令牌 `[SEG]`，则触发分割掩码解码过程——MSDec被复用为统一接口，将 `[SEG]` 对应的隐藏状态作为分割查询，再次通过MSDec与多尺度NDT特征交互，生成3D分割掩码。

### 训练损失设计

训练分为两阶段。**Stage 1（预训练）** 组合三类损失：

$$\mathcal{L} = \mathcal{L}_{cls} + \lambda_{1} \mathcal{L}_{m} + \lambda_{2} \mathcal{L}_{s}(\mathbf{F}_{r}^{\mathrm{C}}, \mathbf{F}_{r})$$

其中 $\mathcal{L}_{cls}$ 为分类交叉熵损失，$\mathcal{L}_{m}$ 为二值交叉熵加Dice分割损失，$\mathcal{L}_{s}$ 为2D-3D语义对齐的余弦相似度损失——将CLIP图像特征提升到3D空间后与3D编码器特征逐单元计算：

$$\mathcal{L}_{s}(\mathbf{F}_{r}^{\mathrm{C}}, \mathbf{F}_{r}) = \frac{1}{N_{r}} \sum_{j=1}^{N_{r}} 1 - \frac{\mathbf{F}_{r}^{j,\mathrm{C}} \mathbf{F}_{r}^{j}}{||\mathbf{F}_{r}^{j,\mathrm{C}}||_{2} ||\mathbf{F}_{r}^{j}||_{2}}$$

**Stage 2（指令微调）** 组合下一令牌生成交叉熵损失 $\mathcal{L}_{t}$、掩码预测损失 $\mathcal{L}_{m}$ 以及预测与真实答案隐藏状态间的余弦相似度损失：

$$\mathcal{L} = \mathcal{L}_{t} + \lambda_{3} \mathcal{L}_{m} + \lambda_{4} \mathcal{L}_{s}(\mathbf{H}^{\hat{a}}, \mathbf{H}^{a})$$



## 实验与关键发现

### 整体实验设置

NDTokenizer3D 采用两阶段训练策略。Stage 1 进行3D场景理解预训练，组合分类交叉熵损失、二值交叉熵与Dice分割损失，以及2D-3D语义对齐的余弦相似度损失；Stage 2 进行指令微调，组合下一令牌生成交叉熵损失、掩码预测损失和预测-真实答案隐藏状态的余弦相似度损失。3D编码器采用 **Point Transformer v3（PTv3）**，MSDec 中集成 FlashAttention-2 以提升内存与计算效率，MSDec 使用 850 个可学习初始查询令牌。多模态对齐头、分割头和多类分类头均实现为两层 MLP。训练使用 4× NVIDIA A100 GPU 搭配 DeepSpeed 分布式优化，LLM 采用 LLaVA-1.5-7B 并进行 LoRA 微调。

### 主实验结果

#### 通用3D VLM全面对比（Table 1）

![[assets/figures/papers/paper_list_l2175_https_arxiv_org_abs_2511_21191/figures/003_Table_1.jpg]]
*Table 1: Left: Quantitative comparison of state-of-the-art generalist 3D VLMs. Results for LEO [22] on ScanQA are shown in gray as it operates under a different setting with access to ground-truth objects and are thus not directly comparable. The best and secondbest results for each metric are bold and underlined, respectively. NDTokenizer achieves the strongest overall performance, particularly on segmentation and QA tasks. Right: Radar plot comparing the per-task performance of specialist models and adapted 3D VLMs. NDTokenizer consistently surpasses both categories across all tasks*

NDTokenizer3D 在四项核心任务上与现有通用、专用和适配型3D VLM进行了系统对比。

在 **Multi3DRefer** 指称分割任务上，NDTokenizer3D 取得 **46.0 mIoU**，超越主要对比基线 **3D-LLaVA**（Boora and Nießner, CVPR 2025）的 42.7 mIoU，提升 **+3.3** 个百分点。这验证了 NDT 表示在保留细粒度几何信息以支撑精确3D定位方面的优势。

在 **ScanQA** 场景问答任务上，NDTokenizer3D 取得 **98.6 CiDEr** 和 **19.4 METEOR**，超过次优结果 **+6.0 CiDEr** 和 **+1.0 METEOR**。需注意 Table 1 中 **LEO**（Huang et al., arXiv 2023）的 ScanQA 结果以灰色显示，因其使用真实物体标注的不同实验设定，与 NDTokenizer3D 及其他方法非直接可比。

在 **SQA3D** 情景问答任务上，NDTokenizer3D 取得 **54.4 EM** 和 **57.1 EM-R**，展现了模型在复杂空间推理场景下的理解能力。

在 **Scan2Cap** 稠密描述任务上，NDTokenizer3D 取得 **79.0 C@0.5**，表明生成的场景令牌保留了足够丰富的语义信息以支持细粒度语言描述。

#### 幻觉评估（Table 2）

![[assets/figures/papers/paper_list_l2175_https_arxiv_org_abs_2511_21191/figures/007_Table_2.jpg]]
*Table 2: Hallucination performance on 3D-POPE. Our NDTokenizer3D achieves the lowest hallucination rates across all settings*

在 **3D-POPE** 基准的三种设定下，NDTokenizer3D 均取得最低幻觉率：
- **Random** 设定：精确率 80.34%，准确率 84.12%
- **Popular** 设定：精确率 69.69%，准确率 75.51%
- **Adversarial** 设定：精确率 66.15%，准确率 72.03%

该结果表明多尺度 NDT 表示通过保留可靠的局部几何统计量，有效抑制了模型对不存在物体的错误指认，在对抗性设定下仍保持相对稳健。

### 消融实验

#### NDT压缩 vs 朴素下采样（Table 3）

![[assets/figures/papers/paper_list_l2175_https_arxiv_org_abs_2511_21191/figures/005_Table_3.jpg]]
*Table 3: Ablation comparing multi-scale NDT compression with a downsampling baseline. Best socres are in bold. Our NDT-based tokenization consistently improves performance across all tasks*

为验证 NDT 表示的核心贡献，实验将 NDT 单元替换为每尺度包含相同数量点的体素下采样点云（仅保留坐标+RGB，丢失局部几何统计量）。结果表明，**NDT-based tokenization 在所有四项任务上一致优于下采样基线**，验证了高斯均值与协方差统计量在保留局部几何信息方面的关键作用——这是朴素坐标下采样无法补偿的信息损失。

#### 尺度数量消融（Table 4）

![[assets/figures/papers/paper_list_l2175_https_arxiv_org_abs_2511_21191/figures/006_Table_4.jpg]]
*Table 4: Ablation comparing number of scales. Best scores are in bold. Three-scale variant provides a balance between detail preservation and stable reasoning*

比较单尺度（r={2}）、双尺度（r={2,3}）和三尺度（r={2,3,4}）配置。**三尺度变体在细节保留与推理稳定性之间取得最佳平衡**，性能优于单尺度和双尺度变体。这印证了细粒度尺度保留局部几何细节、粗粒度尺度捕获全局语义的分工设计，且跨尺度融合（通过 MSDec）需要足够的尺度层次才能充分发挥作用。

#### 查询令牌数量消融（Table 5）

![[assets/figures/papers/paper_list_l2175_https_arxiv_org_abs_2511_21191/figures/010_Table_5.jpg]]
*Table 5: Ablation comparing number of queries*

比较 MSDec 中可学习查询令牌数量为 200、400、600、850 的配置。性能在 **400-850 查询处趋于饱和**，表明 MSDec 在此范围内已捕获足够场景信息。该结果为实际部署中的效率-性能权衡提供了参考依据。

#### 定性对比（Figure 3）

![[assets/figures/papers/paper_list_l2175_https_arxiv_org_abs_2511_21191/figures/008_Figure_3.jpg]]
*Figure 3: Qualitative comparison between NDTokenizer3D and 3D-LLaVA across four tasks, showing NDTokenizer3D’s improved grounding, spatial reasoning, and object understanding*

NDTokenizer3D 与 3D-LLaVA 在指称分割、VQA、情景问答和稠密描述四项任务上的定性对比显示，NDTokenizer3D 在以下方面表现更优：
- **定位精度**：分割掩码更精确地贴合物体边界
- **空间推理**：对物体间空间关系的理解更准确
- **物体理解**：对细粒度物体属性和类别的识别更可靠

### 待验证问题

以下结论需要人工验证或依赖更完整的原文信息：
1. NDT 网格分辨率对不同场景类型（室内/室外）的通用性——论文实验均在室内数据集（ScanNet 系列）上进行，室外场景的适应性未经检验。
2. 多尺度 NDT 表示的计算开销相比直接点云处理的实际加速或内存节省未给出量化数据，效率优势缺乏数值支撑。
3. `[SEG]` 令牌的生成机制和训练信号细节在可用上下文中不够清晰——LLM 如何在适当位置学习生成该特殊令牌以触发分割解码，需要进一步确认原文的具体训练策略。
4. Stage 1 预训练使用的3D实例分割数据集具体名称未在可用上下文中明确列出。



## 定位与知识库关联

### 1. 技术路线定位

NDTokenizer3D 的核心贡献在于将**SLAM领域的NDT（Normal Distributions Transform）网格表示**引入3D视觉语言模型的分词器设计，构建了一条“统计量保留 → 多尺度聚合 → 统一交互接口”的技术路线。其方法论定位可从三个维度理解：

**（1）3D场景压缩范式：从“下采样丢失”到“统计量保留”**

传统3D VLM分词器（如3D-LLaVA）采用朴素多尺度体素下采样，仅保留坐标+RGB，丢弃了局部表面的几何分布信息。NDTokenizer3D 以NDT网格单元的高斯统计量（均值$\mu$与协方差$\Sigma$）替代原始点云，在压缩存储的同时最大化保留局部几何细节——这一思想直接源自经典NDT点云配准方法，但被首次系统性地应用于3D VLM的表示学习。消融实验（Table 3）证实，NDT-based tokenization 在所有四项任务上一致优于下采样baseline，验证了统计量保留策略的有效性。

**（2）多尺度融合机制：从“独立拼接”到“渐进交叉注意力”**

现有方法通常独立处理多尺度特征后简单拼接，缺乏跨尺度交互。NDTokenizer3D 提出的 **MSDec（Multi-Scale NDT Decoder）** 采用R层transformer解码器，以多尺度NDT特征作为Key/Value，以可学习查询令牌作为Query，从粗到细逐层执行交叉注意力融合。这一设计借鉴了DETR系列的目标查询机制，但将其适配到3D场景的多尺度NDT特征空间，形成“全局语义 → 局部细节”的渐进式信息整合路径。

**（3）任务统一接口：从“多分支解耦”到“单一MSDec复用”**

NDTokenizer3D 将MSDec复用为统一接口，同时支持用户交互提示（点/框/掩码）和分割掩码解码——用户输入经掩码化后作为额外查询令牌输入MSDec生成引导令牌，[SEG]特殊令牌触发分割查询同样经MSDec解码生成3D掩码。这种“单一解码器多任务”的设计避免了为每个下游任务引入独立分支，与Chat-Scene（Huang et al., NeurIPS 2024）基于物体标识符的方法和Scene-LLM（Fu et al., WACV 2025）的扩展语言模型路线形成差异化。

### 2. 与基线方法的对比关系

| 方法 | 3D表示方式 | 多尺度策略 | 任务统一性 | 关键差异 |
|------|-----------|-----------|-----------|---------|
| **3D-LLaVA** (Boora & Nießner, CVPR 2025) | 多尺度体素下采样点云 | 独立处理拼接 | 任务特定分支 | NDT统计量保留几何信息；MSDec跨尺度融合 |
| **LEO** (Huang et al., arXiv 2023) | 真实物体标注（不同设定） | — | — | 依赖ground-truth物体，非直接可比 |
| **Chat-Scene** (Huang et al., NeurIPS 2024) | 物体标识符 | — | — | 基于物体级表示，非场景级分词 |
| **Scene-LLM** (Fu et al., WACV 2025) | 扩展语言模型 | — | — | 侧重推理扩展，非分词器创新 |
| **LSceneLLM** (Zhi et al., CVPR 2025) | 大规模场景LLM | — | — | 侧重规模扩展，非表示压缩 |

NDTokenizer3D 在Multi3DRefer上以46.0 mIoU超越3D-LLaVA的42.7（+3.3），在ScanQA上以98.6 CiDEr和19.4 METEOR超越次优结果（+6.0/+1.0），表明NDT表示+MSDec融合的组合在定位精度和描述质量上均具有显著优势。定性对比（Figure 3）进一步显示NDTokenizer3D在空间推理和物体理解方面的改进。

### 3. 适用边界与局限

**（1）场景类型泛化性未验证**

论文实验全部在室内数据集（ScanNet系列）上进行。NDT网格分辨率的选择是否对室外大规模场景（如KITTI、SemanticKITTI）具有通用性，仍需进一步验证。室外场景的点云密度、遮挡模式和物体尺度分布与室内存在本质差异，NDT统计量在该场景下的信息保留能力是开放问题。

**（2）计算开销缺乏量化数据**

多尺度NDT表示相比直接点云处理的实际加速或内存节省未给出量化数据。虽然论文声称NDT“同时减少内存使用并保留局部几何细节”，但NDT构建（均值/协方差计算）、多尺度网格存储和MSDec交叉注意力的实际计算成本缺乏与下采样baseline的wall-clock time或峰值内存对比。

**（3）[SEG]令牌生成机制细节不足**

LLM如何在回复中学习在适当位置生成[SEG]特殊令牌以触发分割掩码解码，其训练信号和生成机制在可用上下文中不够清晰。该机制是实现“统一接口”的关键环节，但其可靠性（是否会在不应生成时错误触发）缺乏消融分析。

**（4）预训练数据集未明确列出**

Stage 1预训练使用的3D实例分割数据集具体是什么，论文上下文仅提及该任务但未列出数据集名称，需要手动核实。

### 4. 开放问题

1. **NDT分辨率自适应选择**：当前三尺度配置（r={2,3,4}）是启发式设定的，是否存在基于场景复杂度自适应选择NDT网格分辨率的机制？

2. **NDT统计量的信息完备性**：均值和协方差（15维向量）是否能充分刻画非高斯分布的局部表面（如锐利边缘、多平面交叉）？是否存在信息损失的理论下界？

3. **MSDec查询令牌的可解释性**：可学习查询令牌在训练后是否对应可解释的场景语义单元？400-850查询处性能饱和是否意味着场景信息的上限已由NDT表示决定？

4. **与点云编码器的解耦性**：当前使用Point Transformer v3作为3D编码器，若替换为其他编码器（如SparseConv、MinkowskiEngine），NDT表示的优势是否仍能保持？

5. **多模态对齐损失的必要性**：Stage 1的2D-3D余弦相似度对齐损失（$\mathcal{L}_s$）对最终性能的贡献缺乏独立消融，其与分类/分割损失的相对重要性尚不明确。



## 原文 PDF

![[paperPDFs/CVPR_2026/Scenes_as_Tokens_Multi_Scale_Normal_Distributions_Transform_Tokenizer_for_General_3D_Vision_Language_Understanding.pdf]]
