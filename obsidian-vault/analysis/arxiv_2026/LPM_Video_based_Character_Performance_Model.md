---
title: "LPM 1.0: Video-based Character Performance Model"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/LPM_Video_based_Character_Performance_Model.pdf
project_link: https://project.mhzhou.com/vico
code_link: null
aliases:
- L10LPM
- L10VBCPM
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 交错式双音频（说话/倾听）交叉注意力注入机制（interleaved dual-audio cross-attention）：在DiT的偶数层注入说话音频特征、奇数层注入倾听音频特征，配合多粒度身份参考图像（全局外观、多视角身体、面部表情）直接拼接到自注意力序列中，使模型能够同时建模全双工会话行为并保持身份一致性。这是将"仅能说话"的视频模型转变为"会说话...
primary_logic: 表演三难困境本质上是一个系统级挑战，而非单纯的架构问题。解决它需要在数据、控制和推理三个层面进行协同设计：数据必须覆盖丰富的说话、倾听和社交反应行为；多模态条件控制必须使行为空间在推理时可操控；部署必须在因果、低延迟流式约束下保持这些能力。LPM 1.0通过大规模全双工数据构建、17B DiT的多模态联合训练、以及四阶段自回归蒸馏（将双向基座模型转化为因果流式生成器），证明了这一系统级方案的有效性。
claims:
- Base LPM (720P)在人类评估中全面优于Kling-Avatar-2（64.3%偏好率）和OmniHuman-1.5（42.5%偏好率），最大优势体现在身份一致性和运动动态性维度。
- Online LPM (480P)在实时流式场景下大幅领先LiveAvatar（82.5%偏好率）和SoulX（64.1%偏好率），且在与Base LPM的匹配分辨率直接对比中，42-88%的案例被评为不可区分，证明实时因果生成无需牺牲感知真实感。
- 消融实验证实：情感参考图像（emotion references）能保留身份特有的微表情细节（如微笑风格、牙齿外观），多视角身体参考（body-view references）在主体方向变化时保持3D一致的外观。
- Base LPM训练规模达17B参数、超过1.7万亿多模态token，这是目前视频生成式角色表演领域最大规模的训练。
---

# LPM 1.0: Video-based Character Performance Model

> [!tip] 核心洞察
> 表演三难困境本质上是一个系统级挑战，而非单纯的架构问题。解决它需要在数据、控制和推理三个层面进行协同设计：数据必须覆盖丰富的说话、倾听和社交反应行为；多模态条件控制必须使行为空间在推理时可操控；部署必须在因果、低延迟流式约束下保持这些能力。LPM 1.0通过大规模全双工数据构建、17B DiT的多模态联合训练、以及四阶段自回归蒸馏（将双向基座模型转化为因果流式生成器），证明了这一系统级方案的有效性。

| 字段 | 内容 |
|------|------|
| 中文题名 | LPM 1.0：基于视频的角色表演大模型 |
| 英文题名 | LPM 1.0: Video-based Character Performance Model |
| 会议/期刊 | arXiv 2026 |
| Links | [Project](https://project.mhzhou.com/vico) · [paper](https://arxiv.org/abs/2604.07823) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | LPM 1.0 (Large Performance Model) |
| Dataset | LPM-Bench |

> [!tip] 效果简介
> - LPM-Bench (Overall) 上，人类偏好率 G/S/B (Good%) 64.3% G (Base LPM 720P) vs Kling-Avatar-2 (Base LPM显著占优)；人类偏好率 G/S/B (Good%) 42.5% G (Base LPM 720P) vs OmniHuman-1.5 (Base LPM占优)；人类偏好率 G/S/B (Good%) 82.5% G (Online LPM 480P) vs LiveAvatar (Online LPM大幅占优)。
> - LPM-Bench (Speak场景) 上，Likert绝对评分均值 (1-5) 3.91 (AV sync: 4.13) vs N/A（绝对评分） (音画同步为最强维度)。
> - LPM-Bench (Listen场景) 上，Likert绝对评分均值 (1-5) 4.51 (AV sync: 5.00, Identity: 4.62) vs N/A（绝对评分） (Listen场景表现最佳，AV sync满分)。

## 概要

### 研究背景与核心瓶颈

视频生成式角色表演面临一个系统级的 **“表演三难困境”（performance trilemma）**：现有模型无法同时实现高表现力（expressive quality）、实时推理（real-time inference）和长时域身份稳定性（long-horizon stability）。这一困境的根源在于四个系统性缺失：（1）倾听行为（listening behavior）几乎完全缺失，绝大多数模型仅由语音驱动，无法建模全双工会话中的非言语反应；（2）多模态可控性不足，缺乏对说话/倾听音频、文本指令和身份参考的联合建模；（3）角色规格说明不完备，仅依赖单张参考图像导致长序列中身份漂移；（4）缺乏大规模高质量人本视频基础模型的预训练支撑。

### 本文方案与核心洞察

**LPM 1.0（Large Performance Model）** 是首个面向单人全双工音视频对话表演的视频生成系统，提供了一套全栈框架，在数据、控制和推理三个层面进行协同设计以突破上述困境。其核心洞察在于：表演三难困境本质上是一个系统级挑战，而非单纯的架构问题——数据必须覆盖丰富的说话、倾听和社交反应行为；多模态条件控制必须使行为空间在推理时可操控；部署必须在因果、低延迟流式约束下保持这些能力。

LPM 1.0 包含两大核心模型：**Base LPM** 是一个 17B 参数的双向扩散 Transformer（DiT），在超过 1.7 万亿多模态 token 上训练，联合建模语音驱动动态、倾听反应、文本条件控制和多参考身份保持；**Online LPM** 则通过四阶段自回归蒸馏，将双向基座模型转化为因果流式生成器，支持无限时长实时交互。

### 关键技术机制

系统的关键因果调节变量是 **交错式双音频交叉注意力注入机制**（interleaved dual-audio cross-attention）：在 DiT 的偶数层注入说话音频特征（保证精确唇音同步），奇数层注入倾听音频特征（捕获长时间尺度反应行为），配合多粒度身份参考图像（全局外观、多视角身体、面部表情）直接拼接到自注意力序列中，使模型能够同时建模全双工会话行为并保持身份一致性。这是将“仅能说话”的视频模型转变为“会说话也会倾听”的表演模型的核心机制。

### 主要结果

在人类评估中，Base LPM（720P）全面优于 **Kling-Avatar-2**（64.3% 偏好率）和 **OmniHuman-1.5**（42.5% 偏好率），最大优势体现在身份一致性和运动动态性维度。Online LPM（480P）在实时流式场景下大幅领先 **LiveAvatar**（82.5% 偏好率）和 **SoulX**（64.1% 偏好率）；更关键的是，在与 Base LPM 匹配分辨率的直接对比中，42–88% 的案例被人类评估者判定为不可区分，证明实时因果生成无需牺牲感知真实感。Listen 场景达到最高绝对评分均值 4.51/5.0（音画同步满分 5.00），Conversation 场景因频繁的说话-倾听转换而最具挑战性（运动动态性降至 3.24/5.0）。

### 问题背景：视频生成式角色表演的“三难困境”

视觉生成式AI在图像和通用视频生成领域已取得显著进展，然而，**生成式角色表演**（generative character performance）——即生成一个具有逼真身份一致性、能自然说话与倾听、并在长时域内保持视觉保真度的“数字人”——仍面临根本性挑战。该领域长期受困于一个系统级的**表演三难困境**（performance trilemma）：现有模型无法同时实现**高表现力**（expressive quality）、**实时推理**（real-time inference）和**长时域身份稳定性**（long-horizon stability）。

从技术根源看，这一困境并非单一架构缺陷所致，而是以下四个系统性缺失的叠加结果：

1.  **倾听行为近乎完全缺失**：绝大多数现有视频生成模型仅由单一声道的语音驱动，角色只能“说话”而无法对对话伙伴的言语做出自然的非言语反应（如点头、微笑、注视转移）。这种单向性使得模型无法支撑真正的全双工会话场景。
2.  **多模态可控性不足**：缺乏对说话音频、倾听音频、文本指令和身份参考的联合建模能力。现有方法通常将音频条件简化为单一语音流，无法在推理时灵活操控角色的“听”与“说”行为切换。
3.  **角色规格说明不完备**：主流方案仅依赖单张参考图像定义角色身份。在长序列生成中，这种稀疏的身份信息极易导致外观漂移、微表情失真和3D视角不一致。
4.  **缺乏大规模高质量人本视频基础模型的预训练支撑**：对话视频数据的获取、清洗和标注远比通用视频复杂，缺乏覆盖全双工交互行为的大规模预训练数据，使得模型难以习得丰富的社交反应动态。

### 现有方法缺口

当前视频生成式角色表演的方法可大致分为两类，但均未能突破上述三难困境：

-   **离线语音驱动方法**：以 **Kling-Avatar-2**（Kling Team et al., arXiv 2025）和 **OmniHuman-1.5**（Gao et al., arXiv 2025）为代表。这类方法采用双向全序列去噪架构，能生成较高质量的说话人视频，但存在两个致命缺陷：一是仅由语音驱动，完全不具备倾听和社交反应能力；二是双向架构天然无法支持实时流式推理，限制了在交互式应用中的部署。
-   **实时流式方法**：以 **LiveAvatar**（Huang et al., arXiv 2025）和 **SoulX**（Shen et al., arXiv 2025）为代表。这类方法通过因果架构实现低延迟流式生成，但通常以牺牲生成质量和身份一致性为代价，且同样缺乏对倾听行为的建模。通用图像到视频基线模型（如 **Wan2.1-I2V**）则完全不考虑音频条件，其生成的角色缺乏唇音同步和语音驱动的动态性。

上述方法的共同瓶颈在于：**将“表演”简化为“说话”**，忽视了全双工会话中倾听与反应行为的同等重要性。此外，数据、控制和推理三个层面的设计彼此割裂，缺乏一个从数据构建到模型训练再到在线部署的**全栈协同方案**。

### 本文动机与核心思路

本文提出 **LPM 1.0**（Large Performance Model），旨在构建首个面向**单人全双工音视频对话表演**的视频生成系统，从根本上解决表演三难困境。核心洞察在于：三难困境本质上是一个**系统级挑战**，而非单纯的架构问题。解决它需要在数据、控制和推理三个层面进行协同设计：

-   **数据层面**：必须覆盖丰富的说话、倾听和社交反应行为，构建大规模全双工对话数据集。
-   **控制层面**：必须实现多模态条件的联合注入，使行为空间在推理时可操控——既能精确唇音同步地说话，也能自然地对对话伙伴做出非言语反应。
-   **推理层面**：必须在因果、低延迟流式约束下保持上述能力，使模型真正可部署于实时交互场景。

LPM 1.0通过以下全栈方案验证了这一思路的有效性：（1）大规模全双工数据的系统化构建；（2）17B参数DiT基座模型的多模态联合训练，实现可控、身份一致的表演生成；（3）四阶段自回归蒸馏，将双向基座模型转化为因果流式生成器，在实时推理中保持与离线模型相当的感知真实感。

## 核心方法与创新机理

### 表演三难困境：系统性瓶颈的重新定义

LPM 1.0的核心出发点是对视频生成式角色表演领域瓶颈的重新诊断。现有模型面临一个“表演三难困境”（performance trilemma）：无法同时实现高表现力、实时推理和长时域身份稳定性。这一困境并非单一架构缺陷所致，而是四个系统性缺失的叠加结果：

1. **倾听行为的系统性缺失**：绝大多数现有模型仅由语音驱动，角色几乎不具备倾听反应能力（如点头、微笑、注视转移）。
2. **多模态可控性不足**：缺乏对说话音频、倾听音频、文本指令和身份参考的联合建模，导致行为空间在推理时不可操控。
3. **角色规格说明不完备**：仅依赖单张参考图像，长序列生成中身份漂移严重。
4. **基础模型预训练缺失**：缺乏大规模高质量人本视频基础模型的支撑，制约了生成质量的上限。

LPM 1.0的核心洞察在于：表演三难困境本质上是一个**系统级挑战**，需要数据、控制和推理三个层面的协同设计——数据必须覆盖丰富的说话、倾听和社交反应行为；多模态条件控制必须使行为空间可操控；部署必须在因果、低延迟流式约束下保持这些能力。

### 关键创新一：交错式双音频交叉注意力注入

这是将“仅能说话”的视频模型转变为“会说话也会倾听”的表演模型的核心机制。与基线方法（如**Kling-Avatar-2**、**OmniHuman-1.5**）将单一语音音频流经交叉注意力统一注入所有Transformer层的做法不同，LPM 1.0提出**交错式双音频注入策略**：

- **偶数DiT层**注入说话音频特征（$K_s = W_k^{\mathrm{spk}} c_{\mathrm{speak}}, V_s = W_v^{\mathrm{spk}} c_{\mathrm{speak}}$），说话分支使用**局部窗口注意力**以保证精确唇音同步。
- **奇数DiT层**注入倾听音频特征（$K_l = W_k^{\mathrm{lis}} c_{\mathrm{listen}}, V_l = W_v^{\mathrm{lis}} c_{\mathrm{listen}}$），倾听分支使用**更大窗口**以捕获长时间尺度的反应行为（如点头、微笑、注视变化）。
- 文本交叉注意力和音频交叉注意力的输出通过可学习投影融合：$\mathrm{out} = W_o^{\mathrm{txt}} \mathcal{A}_{\mathrm{text}} + W_o^{\mathrm{aud}} \mathcal{A}_{\mathrm{audio}}$，实现文本指令与音频信号在每层的联合调控。

这一设计使模型能够同时建模全双工会话中的说话动态和倾听反应，而无需在两者之间进行硬切换或时序调度。

### 关键创新二：多粒度身份参考图像注入

现有方法通常仅使用单张参考图像经交叉注意力或CLIP嵌入注入身份信息。LPM 1.0将身份条件扩展为三类互补参考：

- **全局外观参考**：时间多样化采样，防止copy-paste退化。
- **多视角身体参考**（1-4张）：通过GVHMR+SLAM计算相机-人体朝向角，覆盖不同视角的外观证据。
- **面部表情参考**（1-8张）：经EmotiEff Lib检测和图像理解模型二次验证，覆盖多种表情状态。

这些参考图像经VAE patch化后**直接拼接到视频token序列尾部**，参与自注意力计算，而非通过额外的交叉注意力分支。为区分不同参考类型，使用**分段3D RoPE**：$\mathrm{RoPE}_{ij} = \mathrm{RoPE}(t + o_i + so_j, h, w)$，为全局、多视角身体、面部表情参考分配不同的时间偏移$o_i$和子类型偏移$so_j$，在序列维度显式区分多参考帧以避免优化冲突。

消融实验证实了这一设计的有效性：添加情感参考图像能显著改善身份特有的微表情保持（包括微笑风格、牙齿外观和细微面部变化）；多视角身体参考在主体经历大角度方向变化时维持3D一致的身份外观（包括身体结构、面部结构及方向相关的服装细节，如背后logo）。

### 关键创新三：因果自回归蒸馏实现实时流式生成

离线Base LPM采用双向全序列去噪，无法满足实时交互需求。LPM 1.0提出**四阶段蒸馏**将双向基座模型转化为因果自回归流式生成器（Online LPM），核心是将在线生成分解为两个子问题：

- **Backbone（两步蒸馏模型）**：基于含噪历史KV-cache维持时序一致的隐空间轨迹，负责稳定的时序锚定。
- **Refiner（单步因果模型）**：基于干净历史KV-cache恢复高保真细节，负责感知质量重建。

蒸馏四阶段为：(1) **ODE回归初始化**：$\mathcal{L}_{\mathrm{reg}} = \mathbb{E}_{i, \mathbf{t}} \| G_{\mathrm{backbone}}(\mathbf{x}_i^{\mathbf{t}}, \mathbf{t}) - \mathbf{x}_i^{0} \|_2^2$，在教师模型去噪轨迹上进行监督预热；(2) **Off-policy DMD**：在教师导出的隐状态上训练，DMD目标匹配教师分布，LPIPS感知正则项约束视觉质量；(3) **On-policy DMD**：训练数据来自backbone自身的自回归rollout分布，弥合train-test gap；(4) **Refiner DMD**：单独训练refiner，基于干净历史恢复细节。两个阶段均使用**分块因果注意力掩码**进行自回归滚动。

在线系统采用固定1秒chunk的流水线化推理（Generator→Refiner→VAE重叠执行），混合缓存策略（sink tokens保留3 chunks + sliding window保留2 chunks），支持状态分离和边界对齐更新。

**关键证据**：在匹配分辨率（480P）的直接对比中，人类评估者将Base LPM与Online LPM判断为不可区分的案例占比达42-88%（跨所有评估维度和场景），证明实时因果生成无需牺牲感知真实感。Online LPM在实时流式场景下大幅领先**LiveAvatar**（82.5%偏好率）和**SoulX**（64.1%偏好率）。

### 关键创新四：17B参数规模的大规模多模态联合训练

Base LPM基于14B预训练I2V模型扩展3B音频交叉注意力参数，总规模达**17B参数**，在**超过1.7万亿多模态token**上进行训练——这是目前视频生成式角色表演领域最大规模的训练。这一规模使得模型能够联合建模语音驱动动态、倾听反应、文本条件控制和多参考身份保持，支撑分钟级时序一致性生成。

### 与基线方法的核心差异总结

| 创新维度 | 基线方法 | LPM 1.0 |
|---------|---------|---------|
| 音频条件注入 | 单一语音流统一注入所有层 | 交错式双音频注入（偶数层说话/奇数层倾听），差异化窗口注意力 |
| 身份条件注入 | 单张参考图像经交叉注意力 | 多粒度参考图像直接拼接到自注意力序列，分段RoPE区分类型 |
| 在线生成范式 | 双向全序列去噪，无法流式 | 四阶段蒸馏因果backbone-refiner，含噪/干净KV-cache差异化使用 |
| 训练规模 | 通常10B以下 | 17B参数，1.7T+多模态token |
| 倾听能力 | 几乎完全缺失 | 原生支持全双工说话-倾听行为 |

LPM 1.0 是一个面向单人全双工视听对话表演的视频生成全栈框架，其核心设计目标是系统性地解决“表演三难困境”——即高表现力、实时推理和长时域身份稳定性三者难以兼得的根本矛盾。该框架并非单纯的模型架构创新，而是在**数据构建、基座模型训练、在线蒸馏部署**三个层面进行协同设计，将“仅能说话”的视频模型转变为“会说话也会倾听”的表演模型。

### 全栈流水线总览

整个系统的构建遵循从数据到模型再到部署的递进逻辑，可概括为三个核心阶段：

1. **大规模多模态数据构建**：通过三条专用流水线，将异构原始视频转化为高质量、语义丰富、情感表达充分的训练数据。具体包括：
   - **质量过滤与分类流水线**（Figure 2）：依次经过单镜头提取、五类质量缺陷过滤（编辑伪影、视觉质量、内容真实性、构图问题、音画同步）、对话检测剪辑、以及基于微调 Qwen3-Omni 的密集自然语言标注与结构化标签提取，最终将质量缺陷数据比例控制在 1% 以下。
   - **对话音频-视频数据处理流水线**（Figure 3）：对多人视频进行人物追踪与裁剪，利用微调 LR-ASD 进行帧级三态标注（说话/倾听/空闲），再通过规则驱动的帧级重排序模块完成角色-音频分离与语义验证，输出说话/倾听双轨音频的 person-centric 训练数据。
   - **身份感知参考图像提取流水线**（Figure 4）：从长视频中提取三类互补的身份规格——全局外观参考（时间多样化采样）、多视角身体参考（基于 GVHMR+SLAM 计算相机-人体朝向角，覆盖 1–4 个视角）、面部表情参考（EmotiEff Lib 检测 + 图像理解模型二次验证，覆盖 1–8 种表情状态）。

![[assets/figures/papers/paper_list_l1839_LPM_Video_based_Character_Performance_Model/figures/002_Figure_2.jpg]]
*Figure 2: | Data filtering and classification pipeline across four stages. Raw video is progressively filtered through single-shot extraction, quality filtering and cropping, conversation detection and clipping, and finally captioning with embedding generation to produce high-diversity, semantically rich, and emotionally expressive trainable clips*

2. **Base LPM 基座模型训练**（Figure 5）：基于 14B 预训练 I2V 模型扩展 3B 音频交叉注意力参数，构建 **17B 参数的扩散 Transformer**，在超过 1.7 万亿多模态 token 上联合训练。模型同时接收六种模态输入——噪声视频、首帧、身份参考图像、文本指令、说话音频、倾听音频——通过模态特定编码器注入 DiT 堆叠块。其核心机制是**交错式双音频交叉注意力注入**：偶数层注入说话音频特征（$K_s = W_k^{\mathrm{spk}} c_{\mathrm{speak}}, V_s = W_v^{\mathrm{spk}} c_{\mathrm{speak}}$），使用局部窗口注意力保证唇音同步；奇数层注入倾听音频特征（$K_l = W_k^{\mathrm{lis}} c_{\mathrm{listen}}, V_l = W_v^{\mathrm{lis}} c_{\mathrm{listen}}$），使用更大窗口捕获长时间尺度反应行为。文本与音频交叉注意力的输出通过 $W_o^{\mathrm{txt}} \mathcal{A}_{\mathrm{text}} + W_o^{\mathrm{aud}} \mathcal{A}_{\mathrm{audio}}$ 融合，实现联合调控。身份参考图像经 VAE patch 化后直接拼接到视频 token 序列尾部参与自注意力计算，通过分段 RoPE（$\mathrm{RoPE}_{ij} = \mathrm{RoPE}(t + o_i + so_j, h, w)$）为不同类型参考帧分配差异化时间偏移，避免优化冲突。

![[assets/figures/papers/paper_list_l1839_LPM_Video_based_Character_Performance_Model/figures/007_Figure_5.jpg]]
*Figure 5: | Base LPM architecture. Inputs (noise video, the first frame, identity-aware reference images, text, speak audio, and listen audio) are encoded by modality-specific encoders and injected into a stack of DiT blocks via self-attention (visual tokens) and cross-attention (text and audio embeddings). The output video latent is decoded by a VAE decoder to produce the generated video*

3. **Online LPM 流式蒸馏与部署**（Figure 6、Figure 7）：通过四阶段蒸馏将双向 Base LPM 转化为因果自回归流式生成器。蒸馏过程依次为：ODE 初始化回归预热（$\mathcal{L}_{\mathrm{reg}} = \mathbb{E}_{i, \mathbf{t}} \| G_{\mathrm{backbone}}(\mathbf{x}_i^{\mathbf{t}}, \mathbf{t}) - \mathbf{x}_i^{0} \|_2^2$）、Off-policy DMD（含 LPIPS 感知正则项）、On-policy DMD（使用 backbone 自身 rollout 分布以弥合 train-test gap）、Refiner DMD。在线推理采用 backbone-refiner 两阶段架构：backbone 基于含噪历史 KV-cache 维持时序一致的隐空间轨迹，refiner 基于干净历史 KV-cache 恢复高保真细节，两者均使用分块因果注意力掩码进行自回归滚动。系统以固定 1 秒 chunk 为单位，Generator→Refiner→VAE 三级流水线重叠执行，混合缓存策略（sink tokens 3 chunks + sliding window 2 chunks）支持状态分离和边界对齐更新，实现无限时长实时交互。

### 输入输出规范

- **Base LPM 输入**：噪声视频潜变量、首帧潜变量、1 张全局外观参考 + 1–4 张多视角身体参考 + 1–8 张面部表情参考（经 VAE 编码后拼接）、文本指令（经 T5 编码）、说话音频特征（经音频编码器提取）、倾听音频特征（经音频编码器提取）。
- **Base LPM 输出**：经 VAE 解码器解码的生成视频，支持分钟级时序一致性。
- **Online LPM 输入**：与 Base LPM 相同的条件信号，但以流式 chunk 形式逐块送入，同时接收历史 KV-cache。
- **Online LPM 输出**：因果自回归生成的视频流，支持无限时长实时交互，输出分辨率 480P。

### 关键设计决策的因果逻辑

框架的核心设计决策——交错双音频注入、多粒度身份参考拼接、四阶段自回归蒸馏——均直接回应“表演三难困境”的四个系统性缺失。交错双音频注入解决了“倾听行为几乎完全缺失”的问题，使模型首次具备全双工会话行为建模能力；多粒度身份参考拼接解决了“仅依赖单张参考图像导致长序列身份漂移”的问题；四阶段蒸馏则在保持双向基座模型表现力的同时，将其转化为满足实时推理约束的因果流式生成器。这一系统级方案的有效性已通过人类评估验证：Base LPM 在离线场景下以 64.3% 偏好率显著优于 Kling-Avatar-2，Online LPM 在实时流式场景下以 82.5% 偏好率大幅领先 LiveAvatar，且在匹配分辨率下 42–88% 的案例被评为与 Base LPM 不可区分，证明实时因果生成无需牺牲感知真实感。

### 交错式双音频交叉注意力注入

Base LPM 的核心创新在于将传统视频生成模型中单一的“语音驱动”范式扩展为“全双工会话”范式。其关键机制是**交错式双音频交叉注意力注入**（interleaved dual-audio cross-attention injection）：在 DiT 的堆叠层中，偶数层和奇数层分别处理不同声源的音频特征。

- **偶数层——说话音频注入**：偶数 DiT 层接收说话音频特征 $c_{\text{speak}}$，通过可学习投影矩阵生成交叉注意力的 Key 和 Value：

$$K_s = W_k^{\mathrm{spk}} c_{\text{speak}}, \quad V_s = W_v^{\mathrm{spk}} c_{\text{speak}}$$

说话分支采用**局部窗口注意力**，确保生成的唇部运动与语音信号精确同步。

- **奇数层——倾听音频注入**：奇数 DiT 层接收倾听音频特征 $c_{\text{listen}}$，同样经投影后参与交叉注意力：

$$K_l = W_k^{\mathrm{lis}} c_{\text{listen}}, \quad V_l = W_v^{\mathrm{lis}} c_{\text{listen}}$$

倾听分支使用**更大窗口**的注意力，以捕获长时间尺度的反应行为——如点头、微笑、注视转移等非语言社交信号。

- **融合机制**：文本交叉注意力和音频交叉注意力的输出在每层通过各自的可学习输出投影后相加融合：

$$\mathrm{out} = W_o^{\mathrm{txt}} \mathcal{A}_{\text{text}} + W_o^{\mathrm{aud}} \mathcal{A}_{\text{audio}}$$

这种设计使文本指令与音频信号在每一层 Transformer 中实现联合调控，既保留了文本对角色行为的高层语义控制，又确保了音频对唇音同步和反应动态的精细驱动。

### 多粒度身份参考图像注入

为克服单张参考图像在长序列生成中导致的身份漂移问题，LPM 1.0 引入了**多粒度身份参考图像直接拼接**机制。三类互补参考图像——全局外观参考（1张）、多视角身体参考（1–4张）、面部表情参考（1–8张）——经 VAE patch 化后直接拼接到视频 token 序列尾部，参与自注意力计算。

为在序列维度显式区分不同类型的参考帧以避免优化冲突，采用**分段 3D RoPE**（segment-wise 3D RoPE）：

$$\mathrm{RoPE}_{ij} = \mathrm{RoPE}(t + o_i + so_j, h, w)$$

其中 $o_i$ 为不同参考类型（如表情参考、身体视角参考）分配的时间偏移，$so_j$ 为同一类型内的子类型偏移。这种设计使模型能够在自注意力中自然区分全局外观、多视角身体和面部表情三类身份信息，同时保持与视频 token 的空间-时间一致性。

### 因果自回归蒸馏：Backbone-Refiner 架构

将双向基座模型转化为因果流式生成器的核心是**四阶段蒸馏**流程，其关键模块为 backbone-refiner 两阶段架构。

**第一阶段——ODE 回归初始化**：在教师模型（Base LPM）的去噪轨迹上进行监督回归预热，最小化 backbone 预测与干净目标之间的 L2 距离：

$$\mathcal{L}_{\mathrm{reg}} = \mathbb{E}_{i, \mathbf{t}} \left\| G_{\mathrm{backbone}}(\mathbf{x}_i^{\mathbf{t}}, \mathbf{t}) - \mathbf{x}_i^{0} \right\|_2^2$$

其中 $\mathbf{x}_i^{\mathbf{t}}$ 为时间步 $\mathbf{t}$ 的含噪隐状态，$\mathbf{x}_i^{0}$ 为对应的干净目标。该阶段为后续 DMD 训练提供稳定初始化。

**第二阶段——Off-policy DMD**：在教师模型导出的隐状态上训练 backbone，DMD 目标匹配教师分布，LPIPS 感知正则项约束视觉质量：

$$\mathcal{L}_{\mathrm{off\text{-}policy}} = \mathbb{E}_{i, \mathbf{t}} \left[ \mathcal{L}_{\mathrm{DMD}} \left( G_{\mathrm{backbone}}(\hat{\mathbf{x}}_i^{\mathbf{t}}, \mathbf{t}) \right) + w \mathcal{L}_{\mathrm{LPIPS}} \left( G_{\mathrm{backbone}}(\hat{\mathbf{x}}_i^{\mathbf{t}}, \mathbf{t}), \mathbf{x}_i^{0} \right) \right]$$

其中 $\hat{\mathbf{x}}_i^{\mathbf{t}}$ 为教师模型导出的含噪隐状态，$w$ 为平衡权重。

**第三阶段——On-policy DMD**：训练数据来自 backbone 自身的自回归 rollout 分布，使模型适应推理时的分布偏移（train-test gap）：

$$\mathcal{L}_{\mathrm{on\text{-}policy}} = \mathbb{E}_{i, \mathbf{t}} \left[ \mathcal{L}_{\mathrm{DMD}} \left( G_{\mathrm{backbone}}(\bar{\mathbf{x}}_i^{\mathbf{t}}, \mathbf{t}) \right) \right]$$

其中 $\bar{\mathbf{x}}_i^{\mathbf{t}}$ 为含噪历史条件下的自回归 rollout 隐状态。

在推理时，backbone 基于含噪历史 KV-cache 维持时序一致的隐空间轨迹，refiner（单步因果模型）基于干净历史 KV-cache 恢复高保真细节，两者均使用分块因果注意力掩码进行自回归滚动。

![[assets/figures/papers/paper_list_l1839_LPM_Video_based_Character_Performance_Model/figures/008_Figure_6.jpg]]
*Figure 6: | Online LPM architecture. The generator DiT accepts noise inputs, streaming control signals (text, speak/listen audio), and identity reference images conditioned on noisy-history KV caches to produce renoised latents. The refiner DiT then recovers the final clean video chunks conditioned on clean-history KV caches. Both stages use chunk-wise causal attention masks for autoregressive rollout*

![[assets/figures/papers/paper_list_l1839_LPM_Video_based_Character_Performance_Model/figures/009_Figure_7.jpg]]
*Figure 7: | Execution timeline of the online interactive video system, illustrated with a full-duplex dialogue example. The system progresses through warmup, idle, listening, and responding states while maintaining continuous video output. Audio conditions (listen/speak) are aligned with the streaming timeline, and the Audio2Audio module introduces bounded latency between user input and response. The highlighted region shows the overlapping three-stage pipeline (Generator, Refiner, VAE) operating on chunked inputs. The cache structure (fixed sink + sliding window) enables stable long-horizon generation. Text conditioning and KV-cache operations are omitted for clarity*

## 实验与关键发现

### 评估基准与协议

LPM 1.0的评估围绕自建的**LPM-Bench**展开，该基准覆盖5个场景类型（说话、倾听、对话、歌唱、静默），沿3个多样性轴（外观、表演、音频）采样，共包含1000个测试用例，其中10%为长时域生成（最长1小时）以验证时序一致性。人类评估采用G/S/B（Good/Same/Bad）三选一框架，每对视频由三位独立评估者评判，从整体真实感和四个诊断维度（身份一致性、运动动态性、音画同步、视觉质量）进行打分。与LiveAvatar和SoulX的对比使用相同的参考图像和音频输入，确保条件公平。Base LPM与Online LPM的对比在匹配分辨率（480P）下进行，消除分辨率对感知质量的干扰。

### 主实验结果

#### Base LPM离线生成性能

**Base LPM（720P）在人类偏好评估中全面优于现有离线方法。** 在LPM-Bench的成对比较中，Base LPM相对于**Kling-Avatar-2**（Kling Team et al., arXiv 2025）获得64.3%的偏好率，相对于**OmniHuman-1.5**（Gao et al., arXiv 2025）获得42.5%的偏好率，最大优势体现在身份一致性和运动动态性两个维度。作为参考基线，通用图像到视频模型Wan2.1-I2V由于缺乏音频条件控制，在音画同步维度上表现极差（Figure 8）。定性对比（Figure 9）显示，Base LPM在相同参考图像、文本和音频输入下，生成更丰富的手势、更自然的情感表达、更精确的唇音同步和更稳定的身份保持。

**按场景分解的绝对评分（Likert 1-5）揭示了清晰的性能梯度（Figure 10）：**
- **Listen场景表现最佳**，平均分4.51，其中音画同步达到满分5.00，身份一致性4.62。倾听行为（如点头、微笑、注视变化）的生成质量极高，这得益于交错式双音频注入机制中专为倾听分支设计的大窗口交叉注意力。
- **Speak场景次之**，平均分3.91，音画同步为最强维度（4.13），验证了说话分支局部窗口注意力对精确唇音同步的有效性。
- **Conversation场景最具挑战性**，平均分3.70，运动动态性骤降至3.24。频繁的说话-倾听状态转换导致手势衔接和音画同步质量下降，这是当前系统的主要瓶颈。

#### Online LPM实时流式性能

**Online LPM（480P）在实时流式场景下建立了显著优势。** 在LPM-Bench的成对比较中（Figure 11），Online LPM相对于**LiveAvatar**（Huang et al., arXiv 2025）获得82.5%的偏好率，相对于**SoulX**（Shen et al., arXiv 2025）获得64.1%的偏好率。优势覆盖所有评估维度，尤其在运动动态性和身份一致性上拉开明显差距。

**蒸馏质量的关键证据来自Base LPM与Online LPM的直接对比（Figure 13）。** 在匹配分辨率（480P）下，人类评估者判定两者在42-88%的案例中不可区分（跨所有评估维度和场景）。这一结果表明，四阶段自回归蒸馏（ODE初始化→Off-policy DMD→On-policy DMD→Refiner DMD）成功将双向基座模型转化为因果流式生成器，**实时因果生成无需牺牲感知真实感**。值得注意的是，倾听场景中在线模型的微妙反应行为（如微表情、注视转移）尚不如离线Base LPM丰富，这是蒸馏过程中需要进一步优化的方向。

### 消融实验

#### 情感参考图像的影响

**添加情感参考图像（emotion references）显著改善身份特有的微表情保持。** 消融实验（Figure 14）表明，当提供1-8张面部表情参考图像时，模型能够忠实保留微笑风格、牙齿外观和细微面部微表情等个性化细节。缺少情感参考时，这些身份特有的表达细节保真度明显下降。这一发现验证了多粒度身份参考设计中面部表情分支的必要性——单一全局外观参考无法捕获个体在表情维度上的身份特征。

#### 多视角身体参考的影响

**多视角身体参考（body-view references）在主体经历大角度方向变化时维持3D一致的身份外观。** 消融实验（Figure 15）展示，当提供1-4个视角的身体参考图像时，模型生成的视频中主体即使经历大幅方向变化，仍能保持3D一致的身份和外观。这种一致性不仅体现在连贯的身体和面部结构上，还体现在方向相关的服装细节（如背后的logo）上。这归功于多视角参考经VAE patch化后直接拼接到自注意力序列中，配合分段RoPE区分不同参考类型的时间偏移。

#### 数据流水线组件性能

**帧级三态标注模型**在Domain 1和Domain 2上分别达到89.75%和87.63%的准确率（Table 1）。Domain 2的倾听召回率降至81.05%（说话召回率94.05%），验证了声学变异性较高场景下倾听检测的系统性挑战——倾听行为缺乏明确的声学特征，依赖更微妙的音视频同步线索。

**语义验证模型**微调Qwen3-Omni达到78.37总体F1，较Gemini 2.5 Pro基线提升+7.90（Table 2）。最大增益出现在沉默（+19.40）和说话（+10.67）类别。然而，listen_dialogue与conversation的决策边界仍存在过预测问题——微调后25.4%的listen_dialogue被误判为conversation，需进一步校准。

### 失败模式分析

**Conversation场景是当前系统的主要性能瓶颈。** 运动动态性评分降至3.24/5.0，频繁的说话-倾听转换导致两个问题：（1）音画同步在状态切换边界出现抖动；（2）手势和身体动作的衔接不够自然，缺乏真实对话中平滑的过渡行为。

**多段落时序动作执行存在系统性失败。** 78%的可控性失败归因于复杂动作序列的时序执行错误，文本可控性呈现双峰的"全有或全无"模式——模型要么完美执行所有动作，要么完全遗漏某些动作步骤，缺乏部分执行的中间状态。

**在线模型在倾听场景的微妙反应行为**（如微表情变化、注视转移）尚不如离线Base LPM丰富，这是蒸馏过程中行为空间压缩的代价。

**语义验证模型**在listen_dialogue与conversation边界存在过预测（25.4%误判率），可能导致训练数据中倾听对话片段被错误标注为对话，影响模型对倾听行为的建模精度。

![[assets/figures/papers/paper_list_l1839_LPM_Video_based_Character_Performance_Model/figures/018_Figure_14.jpg]]
*Figure 14: | Ablation on emotion references of Base LPM. With all other inputs fixed, adding emotion reference images improves the preservation of fine-grained identity-related expression cues, including smiling style, dental appearance, and subtle facial micro-expressions. In contrast, without emotion references, these person-specific expressive details are less faithfully preserved*

![[assets/figures/papers/paper_list_l1839_LPM_Video_based_Character_Performance_Model/figures/004_Table_1.jpg]]
*Table 1: | Frame-level results for speak-versus-listen classification after re-ranking and idle merging on 2K manually annotated test clips (1K clips each from Domain 1 and Domain 2). The left block shows the confusion matrix: entries are frame counts with column-normalized percentages in parentheses (equivalent to per-class recall on the diagonal). The right block reports per-class precision and F1 score. Summary metrics appear in the bottom row of each domain. Pred.: predicted label; GT: ground truth; Acc.: accuracy*

## 定位与知识库关联

### 1. 问题定位：表演三难困境

LPM 1.0 瞄准视频生成式角色表演领域的核心瓶颈——**表演三难困境**（performance trilemma）：现有模型无法同时实现高表现力、实时推理和长时域身份稳定性。这一困境根源于四个系统性缺失：

1. **倾听行为几乎完全缺失**：绝大多数模型仅由语音驱动，角色在对话中只能“说”不能“听”，无法产生点头、微笑、注视转移等社交反应。
2. **多模态可控性不足**：缺乏对说话音频、倾听音频、文本指令和身份参考的联合建模。
3. **角色规格说明不完备**：仅依赖单张参考图像，长序列生成中身份漂移严重。
4. **缺乏大规模人本视频基础模型的预训练支撑**：现有模型多从通用视频生成模型微调而来，未针对人本对话场景进行系统化数据与架构设计。

LPM 1.0 的核心洞察在于：表演三难困境是**系统级挑战**，而非单纯的架构问题——需要在数据、控制和推理三个层面进行协同设计。

### 2. 方法谱系中的定位

#### 2.1 与离线语音驱动方法的对比

LPM 1.0 的 Base LPM（720P）直接对标两类离线语音驱动方法：

- **Kling-Avatar-2**（Kling Team et al., arXiv 2025）：离线语音驱动头像生成。Base LPM 在人类评估中以 **64.3%** 偏好率显著占优，最大优势体现在身份一致性和运动动态性维度。Kling-Avatar-2 仅由单一语音流驱动，缺乏倾听行为建模，在对话场景中角色表现僵硬。
- **OmniHuman-1.5**（Gao et al., arXiv 2025）：离线语音驱动人体视频生成。Base LPM 以 **42.5%** 偏好率占优。OmniHuman-1.5 虽支持全身人体生成，但同样缺乏倾听模态的条件注入，无法产生社交反应行为。

**关键差异**：Base LPM 通过交错式双音频交叉注意力注入机制，在 DiT 的偶数层注入说话音频特征、奇数层注入倾听音频特征，使模型首次具备全双工会话行为建模能力。这是将“仅能说话”的视频模型转变为“会说话也会倾听”的表演模型的核心机制跃迁。

#### 2.2 与实时流式方法的对比

Online LPM（480P）对标实时流式头像生成方法：

- **LiveAvatar**（Huang et al., arXiv 2025）：实时流式语音驱动头像生成。Online LPM 以 **82.5%** 偏好率大幅领先，在所有诊断维度上均占优势。
- **SoulX**（Shen et al., arXiv 2025）：实时流式语音驱动头像生成。Online LPM 以 **64.1%** 偏好率占优。

**关键差异**：LiveAvatar 和 SoulX 采用双向全序列去噪范式，无法实现真正的因果流式推理。Online LPM 通过四阶段自回归蒸馏（ODE 初始化 → Off-policy DMD → On-policy DMD → Refiner DMD），将双向基座模型转化为因果自回归流式生成器，在匹配分辨率（480P）下，42–88% 的案例被评估为与 Base LPM 不可区分，证明实时因果生成无需牺牲感知真实感。

#### 2.3 与通用视频生成方法的对比

Wan2.1-I2V 作为通用图像到视频生成基线，在 LPM-Bench 上表现显著弱于 Base LPM。通用 I2V 模型缺乏对人本对话场景的专门化设计（无音频条件注入、无身份多参考机制），在唇音同步、倾听反应和身份保持维度上存在系统性缺陷。

### 3. 核心方法创新与适用边界

#### 3.1 关键创新点

| 创新维度 | 基线方案 | LPM 1.0 方案 | 因果机制 |
|---------|---------|-------------|---------|
| 音频条件注入 | 单一语音流统一注入 | 交错式双音频：偶数层说话、奇数层倾听 | 说话分支局部窗口保证唇音同步，倾听分支更大窗口捕获长时程反应 |
| 身份条件注入 | 单张参考图像（交叉注意力或 CLIP 嵌入） | 多粒度参考图像（全局外观 + 多视角身体 + 面部表情）直接拼接到自注意力序列 | 分段 RoPE 区分参考类型时间偏移，3D 一致性外观保持 |
| 在线生成范式 | 双向全序列去噪 | 因果自回归 backbone-refiner 架构 | 含噪历史 KV-cache 维持时序一致性，干净历史 KV-cache 恢复细节 |

#### 3.2 适用边界

**当前能力边界**：
- **仅支持单人角色表演生成**，尚未扩展到多人协调、受话人追踪和群体级话轮转换等多方交互场景。
- **角色行为尚未与场景几何、物体和物理接触进行 grounding**，生成的角色与环境缺乏真实物理交互。
- **缺乏长时域对话记忆和角色人设持久性建模**，难以在多轮对话中保持一致的个性和上下文。

**性能边界**：
- Conversation 场景下运动动态性评分偏低（**3.24/5.0**），频繁的说话-倾听转换导致音画同步和手势衔接质量下降。
- 多段落动作序列中存在时序动作执行失败（**78% 的可控性失败归因于此**），文本可控性呈现双峰的全有或全无模式。
- 倾听场景中在线模型的微妙反应行为（如微表情、注视转移）尚不如离线 Base LPM 丰富。

### 4. 局限与开放问题

#### 4.1 已识别的局限

1. **多方交互缺失**：系统仅支持单人角色，无法处理多人对话中的受话人追踪、群体话轮转换和多方注意力建模。
2. **物理 grounding 缺失**：角色行为未与 3D 场景几何和物体交互关联，生成的角色悬浮于环境之上。
3. **人设持久性不足**：缺乏跨轮次的记忆机制，角色在多轮对话中无法保持一致的个性、情感状态和上下文。
4. **Conversation 场景性能退化**：频繁的说话-倾听转换导致运动动态性下降和音画同步抖动。
5. **时序动作执行失败**：多段落复杂动作序列的文本可控性存在全有或全无的双峰模式。
6. **语义验证模型边界模糊**：微调后的 Qwen3-Omni 在 listen_dialogue 与 conversation 边界仍存在过预测（**25.4%** 的 listen_dialogue 被误判为 conversation），需进一步校准。
7. **DPO 偏好优化退化**：Pareto-efficient 选择策略在无严格支配候选时的退化行为未解决。

#### 4.2 开放研究问题

1. **多方协调扩展**：如何将系统从单人扩展到多人协调场景，包括受话人追踪、群体级话轮转换和多方注意力建模？
2. **环境 grounding**：如何将角色行为与 3D 场景几何、物体交互和物理接触进行 grounding？
3. **长时域记忆**：如何在流式生成中引入长时域话语记忆和角色人设持久性？
4. **Conversation 场景优化**：如何改善频繁说话-倾听转换时的运动动态性下降和音画同步抖动？
5. **复杂动作序列执行**：如何解决多段落时序动作执行失败问题，使模型能按文本描述的顺序正确执行复杂动作序列？
6. **语义边界校准**：如何进一步校准 listen_dialogue 与 conversation 的决策边界？
7. **偏好优化策略**：DPO 中的 Pareto-efficient 选择策略在无严格支配候选时如何退化和处理？

### 5. 知识库定位

LPM 1.0 在视频生成式角色表演领域建立了首个全栈框架，其知识贡献可归纳为三个层面：

- **数据层**：大规模全双工对话数据集构建流水线（三态标注 + 语义验证 + 多粒度身份参考提取），为领域提供可复用的数据工程范式。
- **模型层**：17B 参数 DiT 基座模型的多模态联合训练方案（交错双音频注入 + 多粒度身份参考 + 分段 RoPE），为后续研究提供架构设计参考。
- **部署层**：四阶段自回归蒸馏将双向基座转化为因果流式生成器的方案，为实时视频生成式交互系统提供部署路径。

该工作将领域从“语音驱动的说话头像生成”推进到“全双工会话角色表演生成”，其系统级设计思路（数据-控制-推理协同）对后续多人交互、物理 grounding 和长时域记忆研究具有方法论参考价值。

## 原文 PDF

![[paperPDFs/arxiv_2026/LPM_Video_based_Character_Performance_Model.pdf]]
