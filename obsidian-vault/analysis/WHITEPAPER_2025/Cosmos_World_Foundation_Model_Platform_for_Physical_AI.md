---
title: "Cosmos World Foundation Model Platform for Physical AI"
type: paper
paper_level: A
venue: Whitepaper
year: 2025
pdf_ref: paperPDFs/WHITEPAPER_2025/Cosmos_World_Foundation_Model_Platform_for_Physical_AI.pdf
code_link: https://github.com/nvidia-cosmos/cosmos-predict1
project_link: https://research.nvidia.com/labs/dir/cosmos-predict1/
aliases:
- CWFMCP
- CWFMPPA
tags:
- WHITEPAPER_2025
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过构建通用的世界基础模型（WFM）作为物理世界的数字孪生，采用大规模视频预训练与特定场景后训练相结合的范式，使模型能够以低成本和低风险生成高质量的未来观测序列，从而缓解数据稀缺问题。"
primary_logic: "将未来视觉预测建模为可控视频生成任务，利用扩散和自回归两种可扩展的Transformer架构、因果视频标记器以及多阶段训练策略，实现了具备3D一致性和物理合理性的世界模拟，并可通过后训练高效定制到相机操控、机器人操作和自动驾驶等多样化物理AI应用。"
claims:
- "数据管线从约2000万小时的原始视频中筛选出约1亿段具有丰富动态和高质量的视频片段用于预训练，为WFM提供了大规模的视觉经验。"
- "在相机控制任务上，Cosmos后训练模型大幅超越CamCo，姿态估计成功率82.0% vs 43.0%，FID 14.30 vs 57.49，FVD 120.49 vs 433.24。"
- "在机器人动作条件视频预测（Bridge数据集）上，Cosmos-7B模型相比IRASim基线，PSNR从19.13提升至21.14，FVD从593降至190。"
- "在3D一致性基准上，Cosmos-7B-Text2World的Sampson误差为0.355（VideoLDM为0.841），姿态估计成功率62.6%（VideoLDM为4.4%）。"
---

# Cosmos World Foundation Model Platform for Physical AI

> [!tip] 核心洞察
> 将未来视觉预测建模为可控视频生成任务，利用扩散和自回归两种可扩展的Transformer架构、因果视频标记器以及多阶段训练策略，实现了具备3D一致性和物理合理性的世界模拟，并可通过后训练高效定制到相机操控、机器人操作和自动驾驶等多样化物理AI应用。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向物理AI的Cosmos世界基础模型平台 |
| 英文题名 | Cosmos World Foundation Model Platform for Physical AI |
| 会议/期刊 | Whitepaper 2025 |
| Links | [paper](https://arxiv.org/abs/2501.03575) · [GitHub](https://github.com/nvidia-cosmos/cosmos-predict1) · [Project](https://research.nvidia.com/labs/dir/cosmos-predict1/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Cosmos World Foundation Model (Cosmos-Predict1扩散/自回归模型系列及配套视频标记器与数据管线) |
| Dataset | 内部3D一致性基准（生成视频）, RealEstate10K (相机可控生成), Bridge (机器人动作条件下一帧预测), 内部多视图驾驶数据集 |

> [!tip] 效果简介
> - 内部3D一致性基准（生成视频） 上，Sampson误差 / 姿态估计成功率 / PSNR / SSIM / LPIPS 为 Cosmos-Predict1-7B-Text2World，对比 VideoLDM，变化 Sampson 0.355 vs 0.841; 姿态成功率 62.6% vs 4.4%; PSNR 33.02 vs 26.23。
> - RealEstate10K (相机可控生成) 上，FID / FVD / 姿态成功率 / 旋转误差 / 平移误差 为 Cosmos-Predict1-7B-Video2World-Sample-CameraCond，对比 CamCo，变化 FID 14.30 vs 57.49; FVD 120.49 vs 433.24; 姿态成功率 82.0% vs 43.0%; 旋转误差 1.646° vs 8.277°。
> - Bridge (机器人动作条件下一帧预测) 上，PSNR / SSIM / Latent L2 / FVD 为 Cosmos-Predict1-7B-Video2World-Sample-ActionCond，对比 IRASim-Action，变化 PSNR 21.14 vs 19.13; SSIM 0.82 vs 0.64; FVD 190 vs 593。

## 概要

**问题瓶颈**：物理AI系统（如机器人、自动驾驶）需要海量包含动作扰动的交互序列数据进行训练，但在真实世界中采集此类数据成本高昂、速度缓慢且存在安全风险，这严重限制了物理AI的scaling进程。

**核心思路**：Cosmos平台通过构建通用的**世界基础模型（WFM）**作为物理世界的数字孪生，将未来视觉预测建模为可控视频生成任务。其核心范式是“大规模视频预训练 + 特定场景后训练”——先利用互联网规模视频学习通用的物理规律和视觉先验，再通过高效微调定制到相机操控、机器人操作、自动驾驶等多样化物理AI应用，从而以低成本和低风险生成高质量的未来观测序列，缓解数据稀缺问题。

**方法定位**：Cosmos采用扩散和自回归两种可扩展的Transformer架构，配合因果视频标记器（Cosmos Tokenizer）将视频压缩为紧凑token，在token潜在空间中进行生成预训练。平台包含六大核心组件：视频数据管线、视频标记器、扩散WFM预训练、自回归WFM预训练、后训练定制和安全护栏。

**主要结果**：
- 数据管线从约2000万小时的原始视频中筛选出约1亿段高质量视频片段用于预训练（Sec. 3）。
- 在相机控制任务上，Cosmos后训练模型大幅超越CamCo基线：姿态估计成功率82.0% vs 43.0%，FID 14.30 vs 57.49（Table 22）。
- 在机器人动作条件视频预测（Bridge数据集）上，相比IRASim基线，PSNR从19.13提升至21.14，FVD从593降至190（Table 23）。
- 在3D一致性基准上，Cosmos-7B-Text2World的Sampson误差为0.355（VideoLDM为0.841），姿态估计成功率62.6%（VideoLDM仅4.4%）（Table 19）。

**局限性**：本文未包含世界模型在策略评估、策略训练、规划及合成数据生成等下游物理AI应用上的实证结果；世界模型的自动化评估框架和基于物理模拟器的可交互基准仍是重大挑战。

### 物理AI的数据困境

在机器人、自动驾驶等物理AI系统中，世界模型（World Model）的核心作用是预测环境在特定扰动下的未来状态，从而为决策、规划和控制提供“想象的”经验。然而，训练一个可靠的世界模型需要海量的交互序列数据——这些数据必须包含丰富的动作扰动和物理反馈。在真实世界中采集此类数据面临三重瓶颈：**成本高昂**（需要大量硬件部署和人工操作）、**速度缓慢**（受限于物理时间流速）、**风险不可控**（试错可能造成设备损坏或安全事故）。这一数据稀缺问题严重制约了物理AI的scaling进程，成为该领域公认的**核心瓶颈**。

### 现有视频生成模型的不足

近年来，基于扩散模型和自回归Transformer的视频生成方法取得了显著进展，例如 **VideoLDM**（Blattmann et al., 2023）展示了文本到视频的生成能力。然而，这些模型在设计上主要面向视觉内容的“创作”，而非物理世界的“模拟”。具体而言，现有方法存在三个关键缺口：

1. **缺乏3D一致性与物理合理性**：主流视频生成模型通常仅在2D像素空间或浅层潜在空间中建模，生成的视频容易出现物体形变、视角跳变和违反物理规律的伪影，无法作为物理AI的可信训练环境。
2. **可控性不足**：现有模型大多仅支持文本条件，难以精确注入相机姿态、机器人动作指令或多视图布局等物理AI所需的控制信号，限制了其在特定任务上的定制能力。
3. **后训练范式缺失**：从通用视频生成模型到专用物理AI模拟器的迁移通常需要重新训练或仅进行浅层微调，缺乏一套系统化的后训练框架来高效适配多样化下游场景。

### 本文的动机与核心思路

针对上述困境，本文提出**Cosmos平台**——一个面向物理AI的世界基础模型（World Foundation Model, WFM）平台。其核心动机在于：

> **将物理世界的未来视觉预测建模为可控视频生成任务**，通过大规模视频预训练获取通用的物理视觉先验，再通过轻量级后训练高效定制到具体应用场景，从而以低成本和低风险的方式生成高质量的未来观测序列，缓解物理AI的数据稀缺问题。

这一思路的技术锚点体现在三个层面：
- **数据层**：构建从约2000万小时原始视频中筛选约1亿段高质量片段的自动化管线，为WFM提供覆盖丰富动态和物理现象的视觉经验（Sec. 3）。
- **模型层**：同时探索扩散和自回归两种可扩展的Transformer架构，并在因果视频标记器的压缩潜在空间中进行训练，确保生成视频的时间因果性和3D一致性（Sec. 4-5）。
- **应用层**：设计统一的预训练-后训练范式，使同一个预训练WFM可以通过注入相机Plücker嵌入、动作条件或多视图条件等方式，快速微调为相机操控、机器人操作和自动驾驶等专用世界模拟器（Sec. 6）。

通过这一系统性的工程与算法创新，Cosmos平台旨在为物理AI提供一个可扩展、可定制且物理合理的“数字孪生”生成引擎。

## 核心方法与创新机理

Cosmos平台的核心创新在于提出了一套面向物理AI的**世界基础模型（WFM）预训练-后训练范式**，通过构建大规模视频数据管线、因果视频标记器以及可扩展的Transformer架构（扩散与自回归），将未来视觉预测建模为可控视频生成任务，从而以低成本、低风险的方式缓解物理AI系统的数据稀缺瓶颈。其相对于现有基线的关键创新体现在以下四个**changed slots**上。

### 1. 因果视频标记器：联合图像/视频的轻量级压缩架构

现有视频标记器（如**CogVideoX-Tokenizer** (Yang et al., 2024)、**OmniTokenizer** (Wang et al., 2024)）通常采用非因果架构，且难以同时高效支持图像与视频的联合训练。Cosmos Tokenizer的核心改进在于：

- **时间因果性设计**：编码器-解码器中的卷积和注意力层均为时间因果（temporal causal），即每一帧的处理仅依赖于当前及过去帧，不依赖未来帧（Figure 9）。这使得第一帧的token自然成为单张图像的表示，实现了图像（T=0）与视频（T>0）在**共享潜在空间**中的统一标记化。
- **Wavelet空间操作**：输入首先经过2级3D Haar小波变换，在wavelet空间进行编解码，不同于常见的像素或潜在空间操作。
- **压缩质量权衡**：在压缩率-重建质量（PSNR）曲线上，Cosmos Tokenizer在更高压缩率下仍保持显著优势，在DAVIS视频上实现约**+4 dB PSNR**的提升（Figure 8）。同时，其推理速度可达同类方法的**12倍**，单张A100 GPU可编码8秒1080p或10秒720p视频。

### 2. 两阶段预训练：Text2World与Video2World的渐进式范式

传统视频生成模型（如**VideoLDM** (Blattmann et al., 2023)）仅进行文本到视频的单一阶段预训练。Cosmos WFM预训练引入了**两阶段渐进式训练策略**：

- **Text2World生成预训练**：首先以文本描述为条件，在约1亿段高质量视频片段上进行大规模预训练，学习通用的视觉世界知识。
- **Video2World生成微调**：在Text2World模型基础上，引入过去视频帧作为额外条件，使模型能够基于历史观测预测未来。此阶段还融合了**图像/视频交替训练**（交错输入单帧图像与多帧视频）和**领域特定归一化**，以增强模型对多样化输入分布的适应能力。

这一设计使得预训练WFM既能从文本生成全新场景，又能基于观测进行物理一致的未来预测，为后续任务定制提供了统一的基座。

### 3. 后训练可扩展性：从通用WFM到多场景专用模型的高效定制

传统方法通常需要为每个下游任务从头训练或仅做有限微调。Cosmos在预训练WFM基础上，通过**条件注入机制**实现高效后训练定制，覆盖三类关键物理AI场景：

- **相机控制**：将相机位姿编码为**Plücker坐标嵌入**（$\mathbf{r} = (\mathbf{d}, \mathbf{m}) \in \mathbb{R}^6$，其中$\mathbf{m} = \mathbf{c} \times \mathbf{d}$），注入预训练扩散WFM，实现精确的相机轨迹可控生成。在RealEstate10K基准上，后训练模型以**FID 14.30 vs 57.49**、**姿态成功率82.0% vs 43.0%**大幅超越**CamCo** (Xu et al., 2024)（Table 22）。
- **机器人操作**：将机器人动作嵌入注入预训练WFM，实现动作条件的下一帧预测。在Bridge数据集上，相比**IRASim-Action** (Zhu et al., 2024)，PSNR从19.13提升至**21.14**，FVD从593降至**190**（Table 23）。
- **自动驾驶**：通过注入多视图条件或轨迹条件，将预训练WFM定制为多视图驾驶视频生成模型，在内部驾驶数据集上FID从60.84降至**32.16**，FVD从884.46降至**210.23**（Table 24）。

### 4. 自回归模型推理加速：Medusa推测解码与低分辨率自适应

自回归WFM虽然具有与LLM统一的架构优势，但逐token解码的推理效率是其主要瓶颈。Cosmos引入了两项关键优化：

- **Medusa推测解码头**：在自回归Transformer上附加多个并行的推测解码头，在一次前向传播中同时预测多个未来token。消融实验表明，使用9个Medusa头可将token吞吐量提升约**2.0-3.2倍**，达到最佳效率-质量权衡（Table 15）。
- **低分辨率自适应**：通过降低生成分辨率并结合扩散解码器上采样，自回归模型可实现**实时10 FPS**的视频生成（Table 17）。

这些创新共同构成了Cosmos平台的技术护城河——从数据、标记化、预训练到后训练和推理加速的全链路设计，使得通用世界模型能够高效地定制化部署到多样化物理AI场景中。

Cosmos平台围绕“世界基础模型”（World Foundation Model, WFM）这一核心概念构建。WFM的形式化定义为：给定过去的观测 $x_{0:t}$ 和当前的扰动 $c_t$，模型预测未来的观测 $\widehat{x}_{t+1}$。此处的扰动 $c_t$ 可以是物理AI系统执行的动作、随机扰动，或描述扰动的文本等（Sec. 2, Figure 3）。该定义将物理世界的未来预测统一建模为可控视频生成任务，为平台的设计提供了理论基础。

平台采用**预训练-后训练**两阶段范式（Figure 2）。预训练阶段，WFM作为“世界模型通才”，在大规模、多样化的视频数据集上进行训练，以捕捉真实世界物理的各个方面；后训练阶段，预训练WFM通过微调被定制为面向特定下游应用的“专用世界模型”，例如相机操控、机器人操作和自动驾驶。整个平台由五大核心组件串联而成（Figure 4）：

1. **视频数据管线（Video Curator）**：负责从原始视频中提取高质量训练数据。流程包括镜头分割（shot detection）、多级过滤（运动、视觉质量、文本、内容安全等）、视觉语言模型（VLM）标注、语义去重和分片（Figure 5）。该管线从约2000万小时的原始视频集合中筛选出约1亿段、时长2至60秒的视频片段用于预训练。

2. **视频标记器（Video Tokenizer）**：将视频压缩为紧凑的连续或离散token表示，供下游WFM使用。Cosmos Tokenizer采用轻量级、时间因果的编码器-解码器架构，在小波空间中操作，支持图像和视频的联合训练（Figure 6, Figure 9）。其因果设计确保每个时间步仅依赖当前及过去的帧，使得第一个时间token对应第一帧输入，从而实现共享潜在空间中的图像（T=0）与视频（T>0）统一标记。

3. **WFM预训练（WFM Pre-training）**：探索了两类可扩展的Transformer架构——**扩散模型**和**自回归模型**。扩散模型基于DiT架构，在token潜在空间中进行去噪训练（Figure 11）；自回归模型以next-token预测方式逐token生成视频（Figure 14）。预训练包含Text2World生成预训练和Video2World生成微调两个子阶段，并引入图像/视频交替训练与领域特定归一化以提升泛化能力。

4. **WFM后训练（WFM Post-training）**：在预训练WFM基础上，通过注入特定条件信号（如相机Plücker嵌入、机器人动作嵌入或多视图条件）进行高效微调，衍生出相机可控生成、动作条件视频预测、多视图驾驶场景生成等专用模型（Sec. 6, Table 21）。

5. **安全护栏（Guardrail）**：包含前置护栏（pre-Guard，基于Aegis和关键词的输入过滤）和后置护栏（post-Guard，视频内容安全分类器与人脸模糊），保障模型的负责任使用（Figure 30）。

整个平台的输入输出流清晰：原始视频经数据管线处理后成为训练样本；训练样本经标记器压缩为token；token与文本描述等条件共同输入WFM进行预训练；预训练模型经后训练注入特定控制信号后，即可根据文本、图像、视频、相机姿态、动作等条件生成符合物理规律的未来观测视频。

### 世界基础模型的形式化定义

Cosmos将世界基础模型（WFM）定义为一个预测未来观测的生成模型。给定过去观测序列 $x_{0:t}$ 和当前扰动 $c_t$，WFM预测下一时刻的观测 $\widehat{x}_{t+1}$。扰动 $c_t$ 可以是物理AI系统执行的动作、随机扰动或文本描述的扰动，这种统一的形式化为后续多场景后训练奠定了基础（Figure 3）。

### 视频标记器：Cosmos Tokenizer

**架构设计。** Cosmos Tokenizer采用轻量级的时间因果编码器-解码器架构（Figure 9）。与常见方法不同，该标记器在wavelet空间操作——输入首先经过2级3D Haar小波变换，随后通过因果残差块、因果下采样层和因果时空注意力模块进行处理。解码器镜像编码器结构，将下采样替换为上采样。时间因果性确保每一阶段仅处理当前及过去帧，不依赖未来帧（Sec. 4.1）。

**联合图像/视频标记。** 标记器输出的时空token网格维度为 $(\frac{H}{s_{HW}} \times \frac{W}{s_{HW}})$ 空间维度和 $(1 + \frac{T}{s_T})$ 时间维度，其中第一个时间token对应第一帧输入，使得 $T=0$ 时退化为图像标记，实现图像与视频在共享潜在空间中的联合训练（Figure 7）。

**连续与离散双模式。** Cosmos Tokenizer同时提供连续潜在嵌入和离散量化索引两种token类型，分别服务于扩散模型和自回归模型的预训练需求。在压缩率-重建质量权衡上，Cosmos Tokenizer相比基线方法在DAVIS视频上获得约+4 dB PSNR提升，且编码速度最高快12倍，可在单张A100 80GB GPU上编码8秒1080p或10秒720p视频（Figure 8）。

### 扩散WFM预训练

**模型架构。** 扩散WFM基于DiT（Diffusion Transformer）架构，在Cosmos Tokenizer的连续潜在空间中运行。模型以文本描述或过去视频帧为条件，通过迭代去噪生成未来视频token，再由标记器解码器重建为像素空间视频（Figure 11）。

**训练目标。** 扩散模型的核心损失函数为去噪分数匹配损失：

$$\mathcal{L}(D_{\theta}, \sigma) = \mathbb{E}_{\mathbf{x}_0, \mathbf{n}} \left[ \| D_{\theta}(\mathbf{x}_0 + \mathbf{n}; \sigma) - \mathbf{x}_0 \|_2^2 \right]$$

其中 $D_{\theta}$ 为去噪器网络，$\mathbf{x}_0$ 为干净潜在表示，$\mathbf{n}$ 为噪声，$\sigma$ 为噪声水平（Sec. 5.1.1, Eq. 3）。

为自动平衡不同噪声水平下的损失贡献，Cosmos引入不确定性加权机制：

$$\mathcal{L}(D_{\theta}) = \mathbb{E}_{\sigma} \left[ \frac{\lambda(\sigma)}{e^{u(\sigma)}} \mathcal{L}(D_{\theta}, \sigma) + u(\sigma) \right]$$

其中 $u(\sigma)$ 为可学习的不确定性参数，$\lambda(\sigma)$ 为预设权重（Sec. 5.1.1, Eq. 5）。

**两阶段预训练策略。** 扩散WFM采用渐进式训练：第一阶段为Text2World生成预训练，模型根据文本描述生成视频；第二阶段为Video2World生成微调，模型以前9帧真实视频为条件预测未来帧。训练过程中交替使用图像和视频数据，并引入领域特定归一化以提升多场景适应性（Sec. 5.1.1, 5.1.4）。

### 自回归WFM预训练

**模型架构。** 自回归WFM基于Transformer架构，将离散视频token序列建模为next-token预测任务。模型以文本嵌入和/或过去视频token为前缀条件，逐token自回归生成未来视频token序列（Figure 14）。

**训练目标。** 自回归模型采用标准的负对数似然损失：

$$\mathcal{L}_{NLL} = \sum_i -\log P(v_i | v_1, v_2, \dotsc, v_{i-1}; \Theta)$$

其中 $v_i$ 为离散视频token，$\Theta$ 为模型参数（Sec. 5.2, Eq. 6）。

**推理加速。** 为提升自回归解码效率，Cosmos引入Medusa推测解码头——在基础模型之上附加多个并行预测头，一次前向传播可预测多个未来token。消融实验表明，9个Medusa头可实现约2.0-3.2倍token吞吐量提升，达到最佳效率-质量权衡（Table 15）。此外，通过低分辨率自适应技术，Cosmos-4B模型可在640×1024分辨率下实现实时10 FPS生成（Table 17）。

### 后训练中的条件注入

**相机控制。** 在相机可控视频生成的后训练中，Cosmos使用Plücker坐标嵌入表示相机参数。对于每条像素射线，Plücker嵌入定义为：

$$\mathbf{r} = (\mathbf{d}, \mathbf{m}) \in \mathbb{R}^6 \ \text{where} \ \mathbf{m} = \mathbf{c} \times \mathbf{d}$$

其中 $\mathbf{d}$ 为射线方向，$\mathbf{c}$ 为相机中心坐标。该6维嵌入被注入扩散模型的条件机制中，使模型能够根据给定的相机轨迹生成对应视角的视频（Sec. 6.1.2）。

**机器人动作条件。** 对于机器人操作场景，动作向量（如末端执行器位姿变化）通过嵌入层映射后注入模型条件分支，使WFM能够根据动作序列预测未来的视觉观测。

**多视图驾驶。** 在多视图驾驶视频生成中，模型同时接收多个相机视角的条件信息，通过视图一致性约束确保生成的多路视频在3D几何上保持一致。

## 实验与关键发现

### 核心实验结果

Cosmos世界基础模型平台在多个维度上进行了系统评估，涵盖3D一致性、相机控制、机器人视频预测和自动驾驶多视图生成等关键物理AI场景。

**3D一致性基准测试**：在内部3D一致性基准上，Cosmos-Predict1-7B-Text2World模型相比VideoLDM（Blattmann et al., 2023）展现了显著优势：Sampson几何误差从0.841降至0.355，姿态估计成功率从4.4%大幅提升至62.6%，PSNR从26.23提升至33.02（Table 19）。这一结果表明，扩散WFM预训练能够有效学习场景的底层3D结构，而非仅仅拟合像素分布。

**相机可控视频生成**：在RealEstate10K数据集上，Cosmos-Predict1-7B-Video2World-Sample-CameraCond后训练模型全面超越CamCo（Xu et al., 2024）基线：FID从57.49降至14.30，FVD从433.24降至120.49，姿态估计成功率从43.0%提升至82.0%，旋转误差从8.277°降至1.646°（Table 22）。这表明通过注入Plücker坐标嵌入（$\mathbf{r} = (\mathbf{d}, \mathbf{m}) \in \mathbb{R}^6$）的后训练策略，能够高效地将通用WFM定制为高精度相机控制模型。

**机器人动作条件视频预测**：在Bridge数据集上，Cosmos-Predict1-7B-Video2World-Sample-ActionCond模型相比IRASim-Action（Zhu et al., 2024）基线，PSNR从19.13提升至21.14，SSIM从0.64提升至0.82，FVD从593降至190（Table 23）。FVD的3倍降幅说明生成视频的运动模式与真实数据分布更为一致。

**多视图驾驶视频生成**：在内部多视图驾驶数据集上，Cosmos-Predict1-7B-Text2World-Sample-MultiView相比VideoLDM-MultiView基线，FID从60.84降至32.16，FVD从884.46降至210.23，视图一致性指标TSE从1.12降至0.62（Table 24）。FVD超过4倍的降幅验证了预训练WFM在多视图场景下的强泛化能力。

### 关键消融实验

**Medusa推测解码**：在自回归模型推理效率方面，引入Medusa推测解码头可将token吞吐量提升约2.0至3.2倍，其中9个头达到最佳效率-质量权衡（Table 15）。这一设计直接缓解了自回归模型逐token解码的推理瓶颈。

**条件帧数影响**：自回归模型的条件帧数消融显示，使用9帧视频条件（而非单帧）可将生成失败率从最高15%降至2%以下（Table 18）。这表明充分的时序上下文对于自回归世界模型的稳定生成至关重要。

**模型规模效应**：更大的14B模型相比7B模型在视频清晰度和运动模式上表现更优，但在物理对齐指标上并未呈现正比关系（Figure 12, 17; Table 20）。这一发现提示，单纯增大模型规模并非提升物理合理性的充分条件，数据质量和训练策略同等关键。

### 视频标记器评估

Cosmos Tokenizer在压缩率-重建质量权衡上展现出显著优势。在DAVIS数据集上，连续标记器相比其他方法在同等压缩率下PSNR提升约4 dB（Figure 8）。运行效率方面，单个A100 80GB GPU可编码8秒1080p或10秒720p视频，推理速度最高可达同类方法的12倍（Table 9）。离散标记器方面，Cosmos DV在TokenBench上的重建质量同样优于CogVideoX-Tokenizer（Yang et al., 2024）和OmniTokenizer（Wang et al., 2024）等基线（Table 6）。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2501_03575/figures/013_Figure_8.jpg]]
*Figure 8: Comparison of continuous (left) and discrete (right) tokenizers in terms of spatio-temporal compression rate (log scale) versus reconstruction quality (PSNR). Each solid point represents a tokenizer configuration, illustrating the trade-off between compression rate and quality. Notably, our tokenizer demonstrates an excellent compression-quality trade-off, delivering superior quality even at higher compression rates compared to other methods. The evaluation was performed on the DAVIS dataset. We calculate the PSNR of image tokenizers on all the individual frames*

### 数据管线吞吐量

视频数据管线的工程优化效果显著：基于Ray编排的转码流程在L40S GPU上使用PyNvideoCodec+ffmpeg组合时达到0.3702 videos/s的吞吐量，相比CPU基线（0.0574 videos/s）提升约6.5倍（Table 2）。VILA视频描述引擎通过FP8量化TensorRT-LLM部署，在单H100 GPU上达到1.96 clips/s的吞吐量，相比PyTorch FP16基线（0.21 clips/s）提升约10倍（Table 3）。

### 失败模式与局限

尽管整体表现优异，分析揭示了若干关键失败模式：
- **物理对齐不足**：互联网视频数据包含大量物理不合理内容，导致模型在物理场景模拟中仍存在偏差（Table 20），需要更好的数据筛选和架构改进。
- **自回归模型质量差距**：自回归WFM在生成清晰度和运动一致性上仍逊于扩散模型，且如何有效利用LLM预训练权重仍是开放问题。
- **长时序稳定性**：多视图驾驶场景下，扩展到8秒生成时可能出现物体突然出现等不一致现象。
- **评估体系缺失**：当前缺乏基于多模态LLM和物理模拟器的自动化、可交互评估基准，世界模型的系统性评估仍是重大挑战。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2501_03575/figures/001_Figure_1.jpg]]
*Figure 1: Cosmos World Foundation Models. Pre-trained Cosmos WFMs generate high-quality 3D consistent videos with accurate physics. The Cosmos suite of models includes both diffusion and autoregressive transformer models, which are trained using continuous and discrete latent representations of videos, respectively. Posttraining these WFMs with specialized datasets enables them to be utilized in a wide range of Physical AI setups. Specifically, we present models with camera controllability, models capable of instruction-following for robotic manipulation, and models for autonomous driving scenarios. To check full videos and more video examples, please visit our website*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2501_03575/figures/028_Figure.jpg]]
*Figure: Frame 120 Prompt: Hands firmly grasp the handle of a steam iron, expertly gliding it over a wrinkled shirt. With each pass, the iron releases gentle clouds of steam, effortlessly smoothing the fabric and erasing wrinkles to reveal a crisp, neat finish. The iron moves with precision and care, transforming the shirt with each stroke. A subtle scent of fresh linen permeates the air, adding to the serene ambiance. Soft light filters through a nearby window, highlighting the fabric’s newly smooth texture and creating a tranquil atmosphere as this meticulous task unfolds*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2501_03575/figures/043_Figure_20.jpg]]
*Figure 20: Physics-scenario rollouts in simulation vs. pre-trained WFM. We demonstrate three exemplar scenarios of increasing complexity as obtained from the reference (physically correct) simulation (first row in each group) and Cosmos-Predict1-7B-Video2World rollouts (second row in each group). We condition the WFM on 9 frames and a prompt focusing on the kinematic state of the simulated objects. We show one tracked object (blue bounding box and mask) per example used to compute our object-level metrics (average IOU)*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2501_03575/figures/048_Figure_22.jpg]]
*Figure 22: Cosmos-Predict1-7B-Video2World-Sample-CameraCond results with joystick control. For each input frame (left-most column), we apply 4 different camera trajectories created with joystick-like control: moving forward, moving backward, rotating left, and rotating right. We visualize frames 14, 28, 42, and 57 from the generated videos*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2501_03575/figures/046_Figure_21.jpg]]
*Figure 21: Qualitative comparison of camera control models. Given the input frame and camera trajectory (color-coded temporally from red to violet), we compare Cosmos-Predict1-7B-Video2World-Sample-CameraCond against CamCo (Xu et al., 2024) on the generated future frames as well as the re-estimated camera poses. CamCo suffers from the data distribution shift and often generates inaccurate trajectories or even out-of-distribution image syntheses that lead to un-estimatable camera poses. In contrast, the Cosmos camera control model can successfully generate future frames aligned with the camera control input while also maintaining high video quality and 3D consistency*

## 定位与知识库关联

### 核心范式：世界基础模型的预训练-后训练框架

Cosmos平台的核心理念是将物理世界的未来观测预测建模为可控视频生成任务，并采用“大规模预训练 + 场景化后训练”的范式。这一思路继承自视觉生成模型向物理AI延伸的宏观趋势，但Cosmos在以下维度做出了系统性重构：

**关键瓶颈与因果机制**：物理AI系统（如机器人、自动驾驶）需要大量包含动作扰动的交互序列进行训练，而真实世界采集此类数据成本高、速度慢且危险。Cosmos的因果杠杆在于构建通用的世界基础模型（WFM）作为物理世界的数字孪生——通过约2000万小时原始视频中筛选出的约1亿段高质量片段进行预训练，再通过注入特定条件（相机位姿、机器人动作、多视图布局）进行高效后训练，以低成本和低风险生成物理上合理的未来观测序列。

**与现有基线的根本差异**：

| 维度 | 现有基线 | Cosmos方案 |
|------|---------|-----------|
| 视频标记器 | 非因果或仅支持单一模态（如**CogVideoX-Tokenizer**, Yang et al., 2024; **OmniTokenizer**, Wang et al., 2024） | 轻量级因果架构，支持联合图像/视频训练，在wavelet空间操作，提供连续和离散两种tokens |
| 预训练任务 | 仅文本到视频生成（如**VideoLDM**, Blattmann et al., 2023） | 两阶段预训练：Text2World生成 → Video2World生成微调，引入图像/视频交替训练和领域特定归一化 |
| 后训练可扩展性 | 通常需从头训练或仅少量微调 | 在预训练WFM基础上，通过注入相机Plücker嵌入、动作嵌入或多视图条件等方式高效定制 |
| 自回归推理效率 | 标准逐token自回归解码 | 引入Medusa推测解码头，最高3.2倍token吞吐提升；低分辨率自适应实现实时10 FPS生成 |

### 方法谱系中的定位

Cosmos处于**视频生成模型**与**物理世界模拟器**的交叉地带。其技术基因可追溯至：

1. **扩散模型谱系**：Cosmos的扩散WFM基于DiT（Diffusion Transformer）架构，在token潜在空间中进行去噪，训练目标采用带不确定性加权的去噪得分匹配损失：
   $$\mathcal{L}(D_{\theta}) = \mathbb{E}_{\sigma} \left[ \frac{\lambda(\sigma)}{e^{u(\sigma)}} \mathcal{L}(D_{\theta}, \sigma) + u(\sigma) \right]$$
   其中 $\mathcal{L}(D_{\theta}, \sigma) = \mathbb{E}_{\mathbf{x}_0, \mathbf{n}} \left[ \| D_{\theta}(\mathbf{x}_0 + \mathbf{n}; \sigma) - \mathbf{x}_0 \|_2^2 \right]$。相比**VideoLDM**（Blattmann et al., 2023），Cosmos在3D一致性上取得质变：Sampson误差从0.841降至0.355，姿态估计成功率从4.4%跃升至62.6%（Table 19）。

2. **自回归模型谱系**：Cosmos的自回归WFM以next-token预测方式学习视频生成，损失为负对数似然：
   $$\mathcal{L}_{NLL} = \sum_i -\log P(v_i | v_1, v_2, \dotsc, v_{i-1}; \Theta)$$
   其创新在于引入Medusa推测解码头（0→9个头可将token吞吐量提升约2.0-3.2倍，9个头达到最佳效率-质量权衡，Table 15），并通过9帧视频条件（而非单帧）将生成失败率从可达15%降至<2%（Table 18）。

3. **相机可控生成谱系**：在RealEstate10K基准上，Cosmos后训练模型相比**CamCo**（Xu et al., 2024）取得压倒性优势——FID 14.30 vs 57.49，FVD 120.49 vs 433.24，姿态成功率82.0% vs 43.0%，旋转误差1.646° vs 8.277°（Table 22）。相机控制通过Plücker坐标嵌入实现：
   $$\mathbf{r} = (\mathbf{d}, \mathbf{m}) \in \mathbb{R}^6 \ \text{where} \ \mathbf{m} = \mathbf{c} \times \mathbf{d}$$

4. **机器人动作条件预测谱系**：在Bridge数据集上，Cosmos-7B相比**IRASim-Action**（Zhu et al., 2024）将PSNR从19.13提升至21.14，FVD从593降至190（Table 23）。

### 适用边界与局限

**已知适用场景**：相机操控视频生成、机器人动作条件下一帧预测、多视图驾驶视频生成、文本条件物理场景模拟。

**明确局限**（需手动验证的边界）：

1. **下游应用验证缺失**：本文未包含WFM在策略评估、策略初始化、策略训练、规划及合成数据生成等物理AI下游任务上的实证结果，这些应用的有效性仍是开放问题。

2. **评估框架不成熟**：世界模型的评估仍缺乏多模态LLM驱动的自动化基准和基于物理模拟器的可交互评估体系，当前依赖的3D一致性、FID/FVD等指标可能无法全面反映物理合理性。

3. **自回归模型质量差距**：自回归WFM在生成清晰度和运动一致性上仍逊于扩散模型。如何利用预训练LLM权重和设计混合扩散-自回归架构以获得更好的质量-速度平衡，仍是开放方向。

4. **物理对齐不足**：互联网视频数据包含大量物理上不合理的内容，当前模型在物理遵守性上仍有明显不足。更大模型（14B vs 7B）在物理对齐指标上并未显示正比关系（Figure 12, 17; Table 20），说明仅靠scaling不足以解决物理合理性问题。

5. **长时序与极端场景退化**：模型在多视图一致性、长时序稳定性和极端场景泛化方面仍有不足，生成内容可能出现物体突然出现等失败案例。

### 开放问题

1. 如何开发基于多模态LLM和物理模拟器的自动化、可交互的世界模型评估基准？
2. 自回归WFM如何更有效地利用预训练LLM权重，以及如何设计混合扩散-自回归架构以获得更好质量-速度平衡？
3. 如何在后训练中保持预训练WFM的泛化能力，同时高效注入新模态（如深度、语义图）？
4. 安全护栏系统（pre-Guard输入过滤 + post-Guard安全分类与人脸模糊）在面对多样化的对抗性提示和生成内容时的鲁棒性如何？
5. 如何进一步缩小合成数据与真实场景之间的领域差距（Sim2Real），使WFM生成的视频能真正服务于物理AI系统的训练？

## 原文 PDF

![[paperPDFs/WHITEPAPER_2025/Cosmos_World_Foundation_Model_Platform_for_Physical_AI.pdf]]
