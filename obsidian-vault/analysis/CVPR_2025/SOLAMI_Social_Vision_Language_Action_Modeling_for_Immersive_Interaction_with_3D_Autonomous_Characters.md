---
title: SOLAMI Social Vision Language Action Modeling for Immersive Interaction with 3D Autonomous Characters
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/SOLAMI_Social_Vision_Language_Action_Modeling_for_Immersive_Interaction_with_3D_Autonomous_Characters.pdf
project_link: https://solami-ai.github.io/
code_link: null
aliases:
- SSVLAMII3AC
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 端到端的社会VLA模型，直接处理多模态令牌并生成对应输出，消除了文本中介。
primary_logic: 将用户语音和动作编码为离散令牌，利用LLMs进行自回归多模态响应生成，并通过多任务预训练和合成多模态对话数据进行微调，可以构建低延迟、高质量的角色行为系统。
claims:
- SOLAMI 在运动质量 FID 上达到 3.443，显著优于模块化 DLP 基线的 4.254。
- SOLAMI 的推理延迟为 2.639 秒，远低于 DLP 的 5.518 秒。
- 用户研究显示，SOLAMI 在所有维度（动作连贯性、交互性、语音一致性、整体体验）中获得最高评分。
- SynMSI test set 上 Motion FID↓ = 3.443
---

# SOLAMI Social Vision Language Action Modeling for Immersive Interaction with 3D Autonomous Characters

> [!tip] 核心洞察
> 将用户语音和动作编码为离散令牌，利用LLMs进行自回归多模态响应生成，并通过多任务预训练和合成多模态对话数据进行微调，可以构建低延迟、高质量的角色行为系统。

| 字段 | 内容 |
|------|------|
| 中文题名 | SOLAMI：面向3D自主角色沉浸式交互的社交视觉-语言-动作建模 |
| 英文题名 | SOLAMI Social Vision Language Action Modeling for Immersive Interaction with 3D Autonomous Characters |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://solami-ai.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SOLAMI |
| Dataset | SynMSI test set |

> [!tip] 效果简介
> - SynMSI test set 上，Motion FID↓ 3.443 vs 4.254 (DLP MotionGPT) (-0.811)；VC Similarity↑ 0.824 vs 0.818 (LLM+Speech) (+0.006)；Inference Latency↓ (seconds) 2.639 vs 5.518 (DLP) (-2.879)。

## 概要

让3D虚拟角色在沉浸式交互中同时理解用户的语音和肢体动作，并生成自然连贯的语音与动作回应，是构建社交具身智能体的核心瓶颈。现有方案多采用模块化LLM-Agent框架，以文本作为各子模块之间的中介表示——语音先转写成文本，动作被描述为语言，LLM生成文本回复后再分别合成语音和动作。这种“文本中转”范式不仅造成模态信息的不可逆丢失，还引入了显著的级联延迟，难以支撑实时、自然的社交互动。

SOLAMI提出了一种端到端的社会视觉-语言-动作（VLA）模型，从根本上消除了文本中介。其核心洞察是：将用户语音和全身动作分别编码为离散令牌，直接馈入一个基于解码器-only LLM（Llama2-7B）的骨干网络，自回归地生成角色的语音令牌和动作令牌，再经各自的解码器还原为连续语音波形和SMPL-X动作序列。这一设计使得多模态感知与生成在统一的令牌空间中完成，避免了信息瓶颈和模块间延迟累积。

为训练这一端到端模型，作者构建了SynMSI合成多模态社交交互数据集，通过话题收集、GPT-4o对话脚本生成、大规模动作库检索与语音合成/克隆四步管线，获得涵盖多种角色设定的多轮语音-动作对话数据。训练采用三阶段策略：先独立训练动作与语音分词器，再通过多任务预训练对齐动作-文本和语音-文本模态，最后在多轮多模态对话数据上进行指令微调。

实验结果表明，SOLAMI在运动质量（Motion FID 3.443 vs. DLP基线4.254）和推理延迟（2.639秒 vs. 5.518秒）上均显著优于模块化方案，同时在语音一致性和上下文相关性上保持了竞争力。用户研究进一步验证了端到端VLA在动作连贯性、交互性和整体体验上的优势。消融实验确认了预训练阶段和全参数微调对性能的关键作用，以及分离身体/手部动作表示在重建精度上的收益。

**方法定位**：SOLAMI属于端到端多模态VLA模型，区别于以文本为中介的模块化LLM-Agent路线。其技术谱系可追溯至离散令牌化的动作生成（如MotionGPT的MoMat/MoGen）和语音-语言对齐工作，但首次将语音、动作的联合感知与生成统一在单个自回归LLM中，并针对社交交互场景进行了系统性的数据合成与训练设计。

### 问题背景：3D自主角色交互的实时多模态需求

构建能够与人类进行自然、沉浸式交互的3D自主角色，是具身智能与虚拟现实交叉领域的核心目标。理想的交互系统需要同时理解和生成语音与身体动作，并在低延迟下保持语义连贯性。然而，传统方法大多采用模块化LLM-Agent架构，将语音识别、文本推理、语音合成和动作生成等子任务串联，依赖文本作为中间表示。这种设计存在两个根本性缺陷：

1. **信息丢失**：语音中的副语言信息（语调、情感韵律）和动作中的空间语义在转换为文本时被不可逆地压缩，导致生成的动作与语音缺乏自然耦合。
2. **高延迟**：串行调用多个子模块（ASR→LLM→TTS→MotionGen）使得端到端响应时间远超实时交互阈值，破坏了对话的沉浸感。

### 现有方法缺口：文本中介与模态割裂

现有方案可归为两类，但均无法满足沉浸式社交交互的要求：

- **纯语音交互基线**（如基于Llama2的LLM+Speech）：仅处理语音模态，完全忽略身体动作，无法实现多模态社交行为。
- **模块化LLM-Agent基线**（如DLP结合MotionGPT）：虽然引入了动作模态，但用户动作需先被文本描述替代，再输入LLM进行推理，生成的文本指令再分别驱动语音合成和动作生成模块。这一文本瓶颈导致推理延迟高达5.518秒（Table 1），且动作质量（FID=4.254）远未达到自然交互的标准。

此外，上述方法均缺乏专门的多模态社交交互训练数据。现有动作数据集多为孤立动作片段，缺少与语音同步的对话上下文；语音数据则缺乏对应的身体动作标注。数据层面的缺失进一步制约了端到端多模态模型的训练。

### 本文动机：端到端社会VLA建模

针对上述瓶颈，SOLAMI提出一个核心洞见：**将用户语音和动作直接编码为离散令牌，利用大型语言模型（LLM）的自回归能力统一生成动作和语音响应，从而消除文本中介**。这一思路将社交交互重新定义为一个序列建模问题——输入是用户的多模态令牌序列，输出是角色的多模态令牌序列，LLM作为统一的序列转换器。

为实现这一目标，需要解决三个关键挑战：
1. **模态离散化**：设计能够将连续动作和语音信号无损压缩为离散令牌的分词器。
2. **模态对齐**：在预训练阶段建立动作-语言和语音-语言之间的语义映射，使LLM骨干网络能够理解非文本令牌。
3. **多模态对话数据**：构建大规模、角色相关的语音-动作同步对话数据集，用于指令微调。

SOLAMI通过三阶段训练策略（分词器训练→多任务预训练→多轮指令微调）和合成数据集SynMSI来应对这些挑战，最终在推理延迟（2.639秒 vs. 5.518秒）和动作质量（FID=3.443 vs. 4.254）上均显著超越模块化基线（Table 1），并在VR用户研究中获得最高满意度评分（Figure 5）。

## 核心方法与创新机理

SOLAMI 的核心创新在于**将模块化 LLM-Agent 框架彻底重构为端到端的社会 VLA 模型**，从根本上消除了文本作为中间表示所带来的信息丢失与高延迟问题。这一转变体现在三个关键维度的结构性创新上。

### 从文本中介到离散令牌的端到端建模

传统的模块化 LLM-Agent 方法（如 DLP 基线）依赖文本描述来桥接各子模块：先将用户语音转写为文本，再将动作编码为文本描述，LLM 基于文本推理后，再通过文本指令驱动语音合成和动作生成模块。这一“文本中介”机制导致两个致命缺陷：**语义压缩造成信息丢失**，以及**串行流水线带来高推理延迟**。

SOLAMI 的核心洞察在于：**将用户语音和动作直接编码为离散令牌，利用 LLM 的自回归能力直接生成响应语音和动作的离散令牌，再解码为连续信号**。具体而言：

- **动作令牌化**：采用 VQ-VAE 将 SMPL-X 关节旋转量化为离散令牌。动作被分解为身体、手部和全局变换三个部分，分别使用独立码本进行量化，如公式所示：
  
  $$\hat { m } _ { t } ^ { u } = Q ^ { u } ( \mathbf { m } _ { t } ^ { u } ) = \arg \operatorname* { m i n } _ { z _ { i } \in \mathbb { Z } _ { u } } \| \mathbf { m } _ { t } ^ { u } - z _ { i } \| _ { 2 }$$
  
  这一分离表示策略在消融实验中取得了最佳重建精度（PA-MPJPE 80，Table 4）。

- **语音令牌化**：使用 SpeechTokenizer 将语音编码为语义令牌，保留语音内容信息。

- **统一自回归生成**：Llama2-7B 骨干网络接收动作和语音令牌序列，自回归地预测下一令牌，同时生成动作和语音响应。指令微调损失函数为：
  
  $$\mathcal { L } _ { \mathrm { I T } } = - \sum _ { r = 1 } ^ { R } \sum _ { i = 1 } ^ { L _ { M } ^ { r } } \log p _ { \Theta } ( \hat { m } _ { i } ^ { r } | \hat { m } _ { i - 1 } ^ { r } , . . . , \hat { m } _ { 1 } ^ { r } , \hat { S } _ { < r } , \hat { M } _ { < r } ) - \sum _ { r = 1 } ^ { R } \sum _ { i = 1 } ^ { L _ { S } ^ { r } } \log p _ { \Theta } ( \hat { s } _ { i } ^ { r } | \hat { s } _ { i - 1 } ^ { r } , . . . , \hat { s } _ { 1 } ^ { r } , \hat { S } _ { < r } , \hat { M } _ { \le r } )$$
  
  该损失在多轮对话中对动作和语音令牌进行联合建模，确保跨模态的时序一致性。

这一架构转变的直接效果是**推理延迟从 DLP 的 5.518 秒降至 2.639 秒（Table 1）**，降幅达 52.2%，同时运动质量 FID 从 4.254 改进至 3.443。

### 多任务预训练实现模态对齐

端到端模型面临的核心挑战是**语音、动作和语言三个异构模态的对齐**。SOLAMI 通过三阶段训练策略解决这一问题：

1. **分词器训练阶段**：独立训练动作 VQ-VAE 和语音分词器，确保离散令牌的压缩质量。动作分词器损失函数为：
   
   $$\mathcal { L } _ { m } = \lambda _ { r } \mathcal { L } _ { r } + \lambda _ { e } \mathcal { L } _ { e } + \lambda _ { c } \mathcal { L } _ { c } + \lambda _ { v } \mathcal { L } _ { v }$$
   
   其中包含重建损失、嵌入损失、承诺损失和速度损失的加权组合，保证动作重建的平滑性和准确性。

2. **多任务预训练阶段**：在动作-文本和语音-文本相关任务上训练 LLM 骨干网络，使模型建立跨模态的语义关联。消融实验表明，**去除预训练阶段会导致 FID 从 3.443 急剧恶化至 5.052，并降低语音质量（Table 1）**，证明该阶段对模态对齐至关重要。

3. **指令微调阶段**：使用合成的多模态多轮对话数据（SynMSI）进行微调，使模型能够根据角色设定和对话上下文生成一致的多模态响应。

### 合成多模态对话数据驱动

由于真实的多模态社交交互数据极度稀缺，SOLAMI 提出了 **SynMSI 合成数据管线**（Figure 3），这是支撑端到端训练的关键基础设施：

- **话题收集**：收集 5.3K 角色相关和日常话题，构建对话场景的语义基础。
- **脚本生成**：基于话题使用 GPT-4o 生成文本对话脚本。
- **动作检索**：从大规模动作数据库（如 AMASS）中检索与对话内容最匹配的动作序列。
- **语音精炼与合成**：根据检索到的动作调整语音脚本，并使用 TTS/语音克隆技术生成角色特有的语音。

这一合成管线使得仅需现有动作数据集即可创建多样化角色的多模态交互数据，**避免了昂贵且难以扩展的真实数据采集**。Table 5 对比了不同数据采集方法的优劣，突显了合成策略的可扩展性优势。

### 全参数微调的必要性

在训练策略上，SOLAMI 坚持**全参数微调**而非参数高效的 LoRA 方法。消融实验显示，使用 LoRA 微调导致 FID 从 3.443 飙升至 15.729（Table 1），性能下降超过 4 倍。这一结果表明：**端到端的多模态生成任务需要 LLM 骨干网络进行深层次的参数调整**，轻量级适配器无法充分学习跨模态的联合分布。

### 创新总结

SOLAMI 的三项核心创新——端到端离散令牌建模、多任务预训练模态对齐、合成多模态数据驱动——构成了一个**相互依赖的创新体系**：合成数据为端到端训练提供可行性，预训练策略确保模态对齐质量，而端到端架构则从根本上解决了模块化方法的延迟和保真度瓶颈。用户研究结果（Figure 5）证实，这一创新体系在动作连贯性、交互性、语音一致性和整体体验等所有维度上均获得了最高评分。

SOLAMI 采用端到端的社会视觉-语言-动作（VLA）建模范式，直接以用户的语音和身体动作作为输入，生成3D虚拟角色的响应语音与动作，消除了传统模块化方案中文本中介带来的信息损失与高延迟。其核心架构围绕一个基于解码器的LLM骨干网络构建，通过将多模态信号统一为离散令牌序列，实现自回归的多模态响应生成。

### 输入输出流与模块关系

系统的工作流程如下：

1. **用户输入编码**：用户语音经由 **Speech Tokenizer (SpeechTokenizer)** 编码为语义令牌；用户身体动作（以 SMPL-X 关节旋转表示）则通过 **Motion Tokenizer (VQ-VAE)** 量化为离散动作令牌。动作分词器将身体、手部和全局变换分离为三个独立部分，分别在各自码本中寻找最近邻向量完成量化（见公式 (1)），其训练目标为重建损失、嵌入损失、承诺损失与速度损失的加权和（见公式 (2)）。

2. **多模态自回归生成**：编码后的语音令牌与动作令牌被拼接为统一序列，送入 **LLM Backbone (Llama2-7B)**。模型根据当前对话历史与角色设定，自回归地预测下一令牌，依次生成角色的响应动作令牌和响应语音令牌。

3. **响应解码**：生成的离散动作令牌由 **Motion Decoder (VQ-VAE decoder)** 解码为连续 SMPL-X 动作参数；语音令牌则由 **Speech Decoder (SoundStorm)** 解码为语音波形，最终驱动3D角色做出同步的语音与动作响应。

### 三阶段训练策略

SOLAMI 的训练遵循三阶段策略（见 Figure 2）：

![[assets/figures/papers/paper_list_l1865_SOLAMI_Social_Vision_Language_Action_Modeling_for_Immersive_Interaction/figures/002_Figure_2.jpg]]
*Figure 2: Training pipeline of SOLAMI. We train SOLAMI through a three-stage process. In the pre-training stage, we train the model with motion-text and speech-text related tasks to align the speech and motion modalities with language. During the instruction tuning stage, we train the model with social multimodal multi-round interaction data, enabling it to generate multimodal responses that align with the character settings and the context of the topic*

- **第一阶段：分词器训练**。独立训练动作 VQ-VAE 与语音分词器，使连续信号能够被压缩为离散令牌并高质量重建。
- **第二阶段：多任务预训练**。在动作-文本和语音-文本相关任务上进行预训练，实现动作模态、语音模态与语言模态之间的对齐，为后续多模态指令跟随奠定基础。
- **第三阶段：指令微调**。使用合成的多轮多模态社交对话数据对模型进行微调，训练目标为对话各轮次中动作令牌与语音令牌的下一个令牌预测的负对数似然（见公式 (3)），使模型能够生成符合角色设定与话题上下文的连贯多模态响应。

### 与模块化基线的架构对比

传统模块化 LLM-Agent 方案（如 DLP）依赖文本作为中间表示：先将用户动作转写为文本描述，再由 LLM 生成文本响应，最后分别调用语音合成和动作生成模块输出。SOLAMI 则通过端到端的离散令牌流，将感知、推理与生成统一于单一 VLA 模型，从根本上消除了文本中介带来的级联误差与高延迟。定量对比显示，SOLAMI 的推理延迟为 2.639 秒，仅为 DLP 基线（5.518 秒）的约 48%（Table 1）。

![[assets/figures/papers/paper_list_l1865_SOLAMI_Social_Vision_Language_Action_Modeling_for_Immersive_Interaction/figures/004_Figure_4.jpg]]
*Figure 4: VR interface architecture. Our VR project consists of a Quest 3 client and a server. The Quest client captures and transmits user body motion and speech to the server. The server then generates character’s speech, body motion, and face blendshape parameters based on the selected methods. The response is then sent back to the Quest client to drive the character*

### 3.1 架构总览

SOLAMI 是一个端到端的社会 VLA 模型，以用户的语音和动作为输入，直接生成 3D 角色的响应语音和动作。其核心创新在于**消除了模块化 LLM-Agent 框架中的文本中介**——传统方法（如 DLP）需要先将语音转为文本、动作转为文本描述，经 LLM 推理后再将文本分别合成为语音和动作，这一过程不仅引入信息丢失，还造成高延迟（DLP 基线达 5.518 秒）。SOLAMI 则将所有模态统一为离散令牌，由单一 LLM 骨干网络自回归地完成多模态生成，推理延迟降至 2.639 秒（Table 1）。

### 3.2 关键模块

#### 动作分词器（Motion Tokenizer）

采用 VQ-VAE 架构，将 SMPL-X 关节旋转表示的人体动作编码为离散令牌。SMPL-X 表示直接建模关节旋转而非关键点位置，具有更好的运动学一致性和泛化性。动作被分解为三个部分分别量化：身体（body）、手部（hand）和全局变换（transform），每部分拥有独立的码本。消融实验（Table 4）表明，分离的身体/手部表示结合关节关键点取得了最佳重建精度（PA-MPJPE 80）。

#### 语音分词器（Speech Tokenizer）

使用 SpeechTokenizer 将用户语音编码为语义令牌，保留语音内容信息的同时丢弃声学细节（如音色），后者由后续的语音解码器根据角色设定重新合成。

#### LLM 骨干网络

基于 Llama2-7B 的解码器架构，接收动作令牌和语音令牌的交错序列，自回归地预测下一令牌。模型需同时理解输入的多模态语义，并根据角色设定和对话历史生成一致的响应。

#### 动作解码器与语音解码器

动作解码器为 VQ-VAE 的解码器部分，将生成的离散动作令牌还原为连续 SMPL-X 参数。语音解码器采用 SoundStorm，将语义令牌转换为目标角色的语音波形。

### 3.3 关键公式

**动作量化**

给定动作部分 $u$（身体、手部或变换）的连续表示 $\mathbf{m}_t^u$，通过寻找对应码本 $\mathbb{Z}_u$ 中最近邻向量获得离散令牌：

$$\hat{m}_t^u = Q^u(\mathbf{m}_t^u) = \arg\min_{z_i \in \mathbb{Z}_u} \|\mathbf{m}_t^u - z_i\|_2$$

该量化过程是端到端架构的关键——将连续动作空间压缩为有限离散符号，使 LLM 能够以统一的 next-token prediction 范式处理动作生成。

**动作分词器训练损失**

$$\mathcal{L}_m = \lambda_r \mathcal{L}_r + \lambda_e \mathcal{L}_e + \lambda_c \mathcal{L}_c + \lambda_v \mathcal{L}_v$$

四项损失分别为：
- $\mathcal{L}_r$：重建损失，约束解码动作与原始动作一致
- $\mathcal{L}_e$：嵌入损失，优化编码器输出
- $\mathcal{L}_c$：承诺损失，鼓励编码器输出靠近码本向量
- $\mathcal{L}_v$：速度损失，约束相邻帧动作的时序平滑性

$\lambda_r, \lambda_e, \lambda_c, \lambda_v$ 为各损失的权重超参数。

**指令微调损失**

在 $R$ 轮对话中，对动作令牌和语音令牌分别计算下一令牌预测的负对数似然：

$$\mathcal{L}_{\mathrm{IT}} = -\sum_{r=1}^{R} \sum_{i=1}^{L_M^r} \log p_{\Theta}(\hat{m}_i^r | \hat{m}_{i-1}^r, ..., \hat{m}_1^r, \hat{S}_{<r}, \hat{M}_{<r}) - \sum_{r=1}^{R} \sum_{i=1}^{L_S^r} \log p_{\Theta}(\hat{s}_i^r | \hat{s}_{i-1}^r, ..., \hat{s}_1^r, \hat{S}_{<r}, \hat{M}_{\le r})$$

其中：
- $\hat{m}_i^r$ 为第 $r$ 轮的第 $i$ 个动作令牌，$L_M^r$ 为该轮动作令牌总数
- $\hat{s}_i^r$ 为第 $r$ 轮的第 $i$ 个语音令牌，$L_S^r$ 为该轮语音令牌总数
- $\hat{S}_{<r}, \hat{M}_{<r}$ 表示前 $r-1$ 轮的所有语音和动作令牌（对话历史）
- $\Theta$ 为模型参数

该损失的设计体现了多模态交错的因果依赖：生成当前轮的动作令牌时仅依赖历史轮次的全模态信息；生成当前轮的语音令牌时则可额外利用本轮已生成的动作令牌（$\hat{M}_{\le r}$），从而显式建模“动作先于语音”或“动作与语音协同”的社交交互时序。

### 3.4 训练策略

SOLAMI 采用三阶段训练（Figure 2）：

1. **分词器训练**：独立训练动作 VQ-VAE 和语音分词器，冻结后供后续阶段使用。
2. **多任务预训练**：在动作-文本和语音-文本相关任务上训练 LLM 骨干网络，对齐动作、语音与语言模态。消融实验（Table 1）表明，去除预训练阶段导致 Motion FID 从 3.443 恶化至 5.052，并降低语音质量，验证了模态对齐预训练的必要性。
3. **指令微调**：在 SynMSI 合成多模态对话数据上进行多轮对话微调，使模型能够根据角色设定和对话上下文生成一致的多模态响应。全参数微调是关键——使用 LoRA 替代全参数微调导致 FID 飙升至 15.729（Table 1），表明社交 VLA 任务需要充分的参数更新来建立跨模态的深层关联。

## 实验与关键发现

### 主要结果

SOLAMI 在 SynMSI 测试集上全面验证了端到端社会VLA模型相对于模块化Agent框架的优越性。Table 1 汇总了核心定量指标：

![[assets/figures/papers/paper_list_l1865_SOLAMI_Social_Vision_Language_Action_Modeling_for_Immersive_Interaction/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of baselines and SOLAMI. ‘↑’(‘↓’) indicates that the values are better if the metrics are larger (smaller). We run all the evaluations 5 times and report the average metric. The best results are in bold and the second best results are underlined*

- **运动质量**：SOLAMI 在 FID 指标上达到 **3.443**，显著优于模块化基线 DLP（MotionGPT）的 4.254（Δ = -0.811）。这表明端到端离散令牌建模避免了文本中介引入的信息损失，能生成更自然、更多样的角色动作。
- **语音一致性**：VC Similarity 达到 **0.824**，略高于仅语音基线 LLM+Speech 的 0.818（Δ = +0.006），证明多模态联合建模未损害语音克隆质量。
- **推理延迟**：SOLAMI 的推理延迟仅 **2.639 秒**，远低于 DLP 的 5.518 秒（Δ = -2.879）。这得益于端到端自回归生成消除了模块间文本传递和串行调度的开销。所有方法均在 2 块 H800 GPU 上使用 vLLM 加速测量，确保可比性。
- **上下文相关性**：Context Relevance 达到 **3.634**，优于 LLM+Speech 的 3.527（Δ = +0.107），说明多模态联合建模能更好地理解用户语音与动作的语义关联。

公平性方面，所有基线使用相同的 Llama2-7B 骨干网络；DLP 基线因原始 MoMat-MoGen 模块延迟过高（>5s）而替换为 MotionGPT 进行动作理解与生成；语音合成方面，LLM+Speech 和 DLP 均使用相同的 XTTS v2 进行语音克隆，确保可比性。

用户研究（Figure 5）进一步验证了客观指标的优势：SOLAMI 在动作连贯性、动作交互性、语音一致性和整体体验四个维度上均获得最高评分，且 95% 置信区间与 DLP 基线无重叠，表明端到端模型在真实 VR 交互场景中提供了更优的主观体验。

### 消融实验

**预训练阶段的关键作用**（Table 1）：去除多任务预训练阶段导致 FID 从 3.443 恶化至 **5.052**，同时语音质量下降。预训练阶段通过运动-文本和语音-文本对齐任务，为 LLM 骨干网络建立了跨模态语义关联，是后续指令微调成功的基础。

**微调策略的影响**（Table 1）：使用 LoRA 微调代替全参数微调导致性能大幅下降，FID 飙升至 **15.729**（vs. 全参数 3.443）。这表明社会VLA任务需要深度调整 LLM 的参数空间，低秩适配无法充分捕获多模态响应的生成规律。

**动作表示与骨干网络设计**（Table 3）：在文本到动作预训练任务中，分离身体和手部动作表示（separate body/hand tokens）结合 Llama2 骨干网络取得了最佳 FID（**1.82**），验证了分部位离散化策略对高维动作空间建模的有效性。

**动作 VQ-VAE 设计**（Table 4）：分离的身体/手部表示结合关节关键点（joint keypoints）取得了最佳重建精度（PA-MPJPE **80**），为下游自回归生成提供了高质量的动作令牌基础。

### 失败模式与局限

尽管 SOLAMI 在定量和定性评估中表现优异，仍存在以下已知局限：

1. **合成数据的泛化边界**：SynMSI 数据集基于 GPT-4o 生成的对话脚本和检索到的动作片段构建，可能无法完全覆盖真实用户交互的多样性和自然性，尤其在开放式对话和即兴动作场景中。
2. **交互规模限制**：当前模型仅支持双人交互（用户与单个角色），无法处理多角色对话或环境交互场景。
3. **动作数据稀缺**：长尾动作和角色特有动作（如特定职业手势、特殊技能动作）在现有动作数据库中覆盖不足，限制了角色行为的丰富度。
4. **VR 设备约束**：Oculus Quest 3 的全身追踪系统对身体（尤其下半身）的追踪精度有限，可能影响输入动作的质量。
5. **语音克隆稳定性**：实时条件下的语音克隆一致性和质量仍有提升空间，尤其在长对话中可能出现音色漂移。

![[assets/figures/papers/paper_list_l1865_SOLAMI_Social_Vision_Language_Action_Modeling_for_Immersive_Interaction/figures/009_Table_3.jpg]]
*Table 3: Quantitative results of pre-training on text-to-motion task. ‘↑’(‘↓’) indicates that the values are better if the metrics are larger (smaller). The best results are in bold and the second best results are underlined*

![[assets/figures/papers/paper_list_l1865_SOLAMI_Social_Vision_Language_Action_Modeling_for_Immersive_Interaction/figures/010_Table_4.jpg]]
*Table 4: Quantitative results of Motion VQVAE. ‘↑’(‘↓’) indicates that the values are better if the metrics are larger (smaller). The best results are in bold*

![[assets/figures/papers/paper_list_l1865_SOLAMI_Social_Vision_Language_Action_Modeling_for_Immersive_Interaction/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative results of SOLAMI and baselines, and the user workflow for VR experience. Our social VLA model, trained in an end-to-end strategy on SynMSI dataset, can accurately perceive the semantic information embedded within users’ speech and motion input, and subsequently generate natural and coherent responses*

## 定位与知识库关联

### 1. 核心范式转移：从模块化 Agent 到端到端 VLA

SOLAMI 的核心贡献在于完成了 3D 自主角色交互领域的一次范式转移——从“模块化 LLM-Agent 框架”转向“端到端社会 VLA 模型”。这一转移并非简单的架构替换，而是对系统瓶颈的根本性回应。

**旧范式：模块化 LLM-Agent（以 DLP 为代表）**
- **架构特征**：将感知、推理、生成拆分为独立子模块，各模块之间通过**文本**进行信息传递。具体而言，用户语音经 ASR 转为文本，用户动作经 Motion Captioning 转为文本描述，LLM 基于文本上下文生成文本响应，再分别由 TTS 和 Motion Generation 模块将文本转为语音和动作。
- **瓶颈根源**：文本作为中间表示，不可避免地造成信息丢失——语音中的副语言信息（韵律、情感）和动作中的空间细节在文本化过程中被压缩或丢弃。同时，多模块串行调用导致**高推理延迟**（DLP 基线达 5.518 秒，见 Table 1），无法满足实时社交交互的响应需求。

**新范式：端到端 VLA（SOLAMI）**
- **架构特征**：将用户语音和动作直接编码为离散令牌，输入基于 Llama2-7B 的解码器主干，自回归地生成响应动作令牌和语音令牌，再分别由 VQ-VAE 解码器和 SoundStorm 解码还原为连续动作和语音波形。
- **关键机制**：消除了文本中介，信息在多模态令牌空间中直接流动。语音通过 SpeechTokenizer 编码为语义令牌，动作通过分离式 VQ-VAE（身体/手部/全局变换分别量化）编码为离散令牌，两者在同一词汇表中统一建模。
- **性能证据**：在 SynMSI 测试集上，SOLAMI 的运动质量 FID 为 3.443，显著优于 DLP 的 4.254（Table 1）；推理延迟降至 2.639 秒，较 DLP 降低约 52%。

### 2. 与基线方法的关系定位

SOLAMI 的实验设计涵盖了三种不同粒度的基线，构成了一条从“单模态”到“模块化多模态”再到“端到端多模态”的递进对比链条。

| 基线方法 | 模态覆盖 | 架构类型 | 核心局限 |
|---------|---------|---------|---------|
| LLM+Speech (Llama2) | 仅语音 | 端到端语音对话 | 无法感知和生成动作，交互维度单一 |
| AnyGPT (fine-tune) | 仅语音 | 端到端语音对话 | 在 SynMSI 语音数据上微调，但仍无动作模态 |
| DLP (MotionGPT) | 语音+动作 | 模块化 LLM-Agent | 文本中介导致信息丢失和高延迟 |

**LLM+Speech 与 AnyGPT** 属于语音交互基线，验证了“仅有语音而无动作”的交互是不完整的。在用户研究中，SOLAMI 在“动作连贯性”和“动作交互性”维度上获得最高评分（Figure 5），而这两个维度是纯语音基线无法覆盖的。

**DLP (MotionGPT)** 是最关键的对比对象。原始 DLP 框架中的 MoMat-MoGen 模块延迟超过 5 秒，为保证公平比较，作者将其替换为 MotionGPT 进行动作理解与生成。即便如此，DLP 仍受限于文本中介架构——语音需经 ASR 转文本、动作需经 Captioning 转文本，信息损失和延迟累积不可避免。SOLAMI 在所有客观指标（FID、VC Similarity、Context Relevance、Latency）和主观维度上均超越 DLP，验证了端到端 VLA 范式的优越性。

### 3. 方法适用边界

SOLAMI 的设计基于以下假设和前提，这些构成了其适用边界：

1. **数据依赖性**：模型训练依赖 SynMSI 合成数据集，该数据集通过 GPT-4o 生成对话脚本、从现有动作数据库检索动作、利用 TTS/语音克隆生成语音。这意味着模型的行为分布受限于合成数据的覆盖范围，对于真实用户交互中可能出现的非典型输入，泛化能力存疑。

2. **双人交互限定**：当前框架仅支持单用户与单角色的双人交互，不支持多角色对话或用户-角色-环境的三元交互。这是 VLA 序列建模的固有约束——对话上下文以轮次序列组织，无法直接扩展至多智能体场景。

3. **动作数据稀缺**：动作模态的训练数据远少于语音和文本，尤其是长尾动作（如特定角色的标志性姿势）和细粒度手部交互（如握手、物体操作）。尽管分离式身体/手部 VQ-VAE 设计（Table 4）在一定程度上缓解了表示学习难度，但生成质量仍受限于数据覆盖。

4. **VR 硬件约束**：系统依赖 Oculus Quest 3 进行全身追踪，但下半身追踪精度有限，且面部表情通过 blendshape 参数驱动而非端到端生成。这意味着角色表现力的上限受硬件能力制约。

5. **非流式推理**：模型采用轮次级自回归生成，需要等待用户完整输入后才能产生响应，不支持全双工流式交互（如用户在角色说话时插话）。

### 4. 局限与开放问题

**已识别的局限**（来自论文自身分析）：
- 合成数据可能无法完全代表真实用户交互的多样性和自然性。
- 语音克隆的一致性和质量在实时条件下仍有限。
- 仅支持双人交互，不能处理多角色或环境交互。

**开放问题**（指向未来研究方向）：
1. **实时具身数据收集**：如何收集真实的 3D 社交交互数据以进一步提高自然度，并支持全双工流式交互？合成数据虽成本低，但存在分布偏差；真实数据获取则面临隐私、标注成本和场景覆盖的挑战。

2. **跨具身泛化**：如何将模型泛化至握手、物体操作等细粒度物理交互任务？当前的动作表示（SMPL-X 关节旋转）主要覆盖身体姿态，缺乏对物体几何和接触力学的建模。

3. **长期记忆与技能整合**：如何将角色的长期记忆和习得技能与实时短期交互相结合？当前模型以对话轮次为上下文窗口，缺乏对跨会话记忆和技能持续学习的机制，容易产生遗忘或计算冗余。

4. **长尾动作的小样本学习**：如何在不进行数据密集型训练的情况下，为长尾和角色特有动作实现高效的小样本学习？这对降低新角色接入成本至关重要。

### 5. 在知识库中的定位

SOLAMI 处于 **3D 自主角色交互** 与 **多模态 VLA 模型** 的交叉点。在 VLA 谱系中，它继承了 RT 系列（如 RT-2）将视觉-语言-动作统一为令牌序列的思路，但将应用场景从机器人操作迁移至社交交互，并将视觉模态替换为语音和人体动作。在 3D 角色驱动领域，它区别于基于文本指令的角色动画方法（如 MotionGPT 的 text-to-motion），实现了语音-动作的双向多模态闭环。

**方法定位总结**：SOLAMI 是首个将端到端 VLA 范式应用于 3D 社交角色交互的工作，通过多模态令牌统一和合成数据驱动，在运动质量、推理延迟和用户体验上建立了新的基准。其核心方法论——将多模态输入输出统一为离散令牌序列并由 LLM 自回归建模——具有跨场景迁移的潜力，但当前的数据依赖性、交互规模限制和硬件约束仍是通向通用 3D 自主角色系统的实质性障碍。

## 原文 PDF

![[paperPDFs/CVPR_2025/SOLAMI_Social_Vision_Language_Action_Modeling_for_Immersive_Interaction_with_3D_Autonomous_Characters.pdf]]
