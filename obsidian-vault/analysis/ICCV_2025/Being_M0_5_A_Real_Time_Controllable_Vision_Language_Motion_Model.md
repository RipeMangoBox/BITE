---
title: "Being-M0.5: A Real-Time Controllable Vision-Language-Motion Model"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model.pdf
project_link: https://beingbeyond.github.io/Being-M0.5
code_link: https://github.com/ggml-org/llama.cpp
aliases:
- BM5
- BM5RTCVLMM
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 部分感知残差量化（PRQ）将运动分解为五个解剖区域的部分级标记，结合大规模多任务指令训练（HuMo100M），通过逐帧解码实现实时可控生成。
primary_logic: 通过将人体运动分解为解剖学部位并进行残差量化，同时利用百万级多任务数据集训练，可以在保持实时性能的前提下实现高度可控的运动生成。
claims:
- Being-M0.5-PRQ4在HumanML3D上FID达到0.056，相较于VQ1变体（FID 0.141）提升60%。
- 在HuMo100M上训练后，I2U任务FID降至8.65，远低于在HumanML3D上训练的18.62。
- 左右交换测试中部位控制成功率达76%，证明精确的部位感知生成能力。
- 模型在多GPU上最低FPS为20，H100上峰值达28.9 FPS，满足实时要求。
---

# Being-M0.5: A Real-Time Controllable Vision-Language-Motion Model

> [!tip] 核心洞察
> 通过将人体运动分解为解剖学部位并进行残差量化，同时利用百万级多任务数据集训练，可以在保持实时性能的前提下实现高度可控的运动生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Being-M0.5：实时可控的视觉-语言-运动模型 |
| 英文题名 | Being-M0.5: A Real-Time Controllable Vision-Language-Motion Model |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://beingbeyond.github.io/Being-M0.5) · [Code](https://github.com/ggml-org/llama.cpp) · [paper](https://arxiv.org/abs/2508.07863) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Being-M0.5 |
| Dataset | HumanML3D, HuMo-Unseen, Left-right exchange test |

> [!tip] 效果简介
> - HumanML3D (Text-to-Motion) 上，FID 0.056 (Being-M0.5-PRQ4) vs 0.141 (Being-M0.5-VQ1) (-0.085 (-60%))。
> - HuMo-Unseen (Instruct-to-Unseen) 上，FID 8.65 (HuMo100M训练) vs 18.62 (HumanML3D训练) (-9.97)。
> - Left-right exchange test (Part-level control) 上，Success Rate 76% vs N/A（非部位感知方法不具备此能力）。

## 概要

**问题瓶颈**：现有视觉-语言-运动模型缺乏全面的可控性，无法同时处理多样指令、任意初始姿势、长序列、未见运动和细粒度部位控制。

**核心洞见**：通过将人体运动分解为解剖学部位并进行残差量化，同时利用百万级多任务数据集训练，可以在保持实时性能的前提下实现高度可控的运动生成。

**方法定位**：Being-M0.5 是首个实时可控的视觉-语言-运动模型（VLMM），其架构基于 LLaVA-video-7B 框架，采用 SigLIP 视觉编码器与 2 层 MLP 投影，以 LLaMA-2-chat 7B 为骨干。核心创新在于**部分感知残差量化（PRQ）**——将运动分解为五个解剖区域的部位级标记，结合大规模多任务指令数据集 **HuMo100M**（超 500 万运动序列、1 亿指令实例）进行训练，并通过逐帧解码实现实时生成。

**主要结果**：
- 在 HumanML3D 文本到运动任务上，Being-M0.5-PRQ4 的 FID 达到 **0.056**，较 VQ1 变体（FID 0.141）提升 **60%**。
- 在 HuMo-Unseen 未见运动指令任务上，HuMo100M 训练后 FID 降至 **8.65**，远低于仅用 HumanML3D 训练的 18.62。
- 左右交换部位控制测试成功率 **76%**，验证了精确的部位感知生成能力。
- 推理速度在多 GPU 上最低 **20 FPS**，H100 上峰值 **28.9 FPS**，满足实时要求。

### 问题背景：从文本到视觉-语言-运动生成的演进

人体运动生成（Human Motion Generation）是计算机视觉与图形学交叉领域的核心问题，其目标是根据给定的控制信号——如自然语言描述、图像或视频——合成逼真且语义一致的三维人体运动序列。近年来，随着扩散模型（Diffusion Models）和自回归Transformer的兴起，文本到运动（Text-to-Motion, T2M）领域取得了显著进展，涌现出**MDM**、**MLD**、**T2M-GPT**、**MoMask**、**MotionDiffuse**、**M2DM**等一系列代表性工作，在HumanML3D和KIT-ML等基准上持续刷新FID等生成质量指标。

然而，实际应用对运动生成模型提出了远超“文本到运动”的更高要求。一个真正实用的运动生成系统需要具备**全面的可控性**（comprehensive controllability），具体包括五个关键维度：

1. **多样化的自然语言指令遵循**：模型应能理解并执行从高层语义到细粒度约束的复杂指令；
2. **灵活的初始姿态设定**：支持从任意起始姿态出发生成后续运动，而非仅从标准姿态开始；
3. **长序列运动生成**：能够生成连贯的长时序运动，避免动作断裂或语义漂移；
4. **未见运动模式的泛化**：对训练数据中未出现的运动类型保持生成质量；
5. **细粒度的部位级控制**：精确操控身体特定区域（如左臂、右腿）的运动，而不影响其他部位。

### 现有方法的瓶颈

现有视觉-语言-运动模型（Vision-Language-Motion Model, VLMM）在上述五个维度上存在系统性不足，其核心瓶颈可归纳为三个层面：

**第一，运动表征粒度过粗。** 主流方法采用残差量化（Residual Quantization, RQ）将全身运动压缩为统一的离散标记序列。这种“整体式”编码虽然简洁，却从根本上丧失了部位级的可辨识性——当用户指令仅涉及“举起右手”时，模型无法将语义约束精确映射到对应的解剖学区域，只能对全局运动进行粗糙调整。

**第二，训练数据规模与任务多样性不足。** 现有基准数据集（如HumanML3D、KIT-ML）仅包含数万条运动序列，且文本标注主要覆盖整体动作描述，缺乏部位级、层级化的语言监督信号。同时，训练任务通常局限于单一的文本到运动生成，未能利用图像、视频等多模态信息构建统一的控制接口。

**第三，实时性与可控性难以兼得。** 扩散模型虽生成质量高，但迭代去噪过程计算开销大，难以满足实时交互需求；而追求效率的自回归方法往往以牺牲控制精度为代价。如何在保持实时推理（≥20 FPS）的前提下实现全面可控，是该领域尚未解决的关键挑战。

### 本文动机

针对上述瓶颈，本文提出**Being-M0.5**——首个实时可控的视觉-语言-运动模型。其核心动机在于：**通过将人体运动分解为解剖学部位并进行残差量化，同时利用百万级多任务数据集训练，可以在保持实时性能的前提下实现高度可控的运动生成。**

具体而言，本文的工作围绕以下三个关键设计展开：

- **部分感知残差量化（Part-aware Residual Quantization, PRQ）**：将人体运动特征按五个解剖区域（躯干、左臂、右臂、左腿、右腿）分解为部位级标记，每个部位独立进行残差量化，从而为细粒度控制提供天然的表示基础；
- **HuMo100M大规模多任务数据集**：构建包含超过500万运动序列、配对视觉片段、三层级文本描述（身体级、部位级、规则级）和1亿条多任务指令实例的数据集，覆盖T2M、I2M、I2U、I2PM、I2LM、MPI六类任务；
- **基于7B LLM的统一架构**：以LLaMA-2-chat 7B为骨干，集成SigLIP视觉编码器与逐帧运动解码器，通过慢-快策略（slow-fast strategy）降低视频标记复杂度，实现多模态输入下的实时可控生成。

这一设计使得Being-M0.5成为首个同时满足“全面可控”与“实时推理”要求的VLMM，为运动生成从学术基准走向实际部署提供了可行路径。

## 核心方法与创新机理

Being-M0.5 的核心创新围绕一个中心洞察展开：**将人体运动按解剖学部位分解并进行残差量化，同时在百万级多任务数据集上训练，可以在保持实时性能的前提下实现高度可控的运动生成**。这一洞察通过三个关键的技术槽位变更得以实现，共同解决了现有视觉-语言-运动模型在可控性维度上的根本瓶颈。

### 部位感知残差量化（PRQ）

标准残差量化（RQ）通过对全身运动特征进行逐层残差逼近来降低量化误差，但这种方式将人体视为一个不可分割的整体，无法对特定身体部位进行独立控制。Being-M0.5 提出的**部位感知残差量化（PRQ）** 引入了三个关键创新：

1. **解剖学分解**：将全身运动特征显式分解为五个解剖区域（躯干、左臂、右臂、左腿、右腿）的部位级潜在序列，每个部位独立编码为离散标记。
2. **共享码本与部位监督**：各部位共享同一个运动码本，同时引入丰富的部位级文本描述作为训练监督信号，使模型能够理解并执行针对特定部位的精细指令。
3. **组合式表示能力**：PRQ 的码本容量为 $\Pi_{j=1}^{p} u_{j}$（其中 $p$ 为部位数，$u_j$ 为各部位可引用的不同代码数），远大于传统 RQ 的表达空间，为未见运动模式的泛化提供了结构基础。

PRQ 的量化过程可形式化为：

$$\mathrm{PRQ}(\tilde{b}_{1:n;1:p}) = [b_{1:n;1:p}^{k}]_{k=0}^{K}$$

其中每一层的量化遵循残差更新规则：

$$b^{k} = \mathcal{Q}(r^{k}), \quad r^{k+1} = r^{k} - b^{k}$$

训练损失由部位级和全身级的 L1 重建损失及加权编码承诺损失组成：

$$\mathcal{L} = \sum_{j=1}^{p} \| m_j - \tilde{m}_j \|_1 + \| m - \tilde{m} \|_1 + \beta \sum_{k=1}^{K} \sum_{j=1}^{p} \| r_j^{k} - \mathrm{sg}[b_j^{k}] \|_2^2$$

实验表明，4 层 PRQ 达到了质量与效率的最优平衡——进一步增加量化层数（>4）反而会因逐帧解码复杂性的增加而损害生成性能。

### 运动特征格式升级：从 HM3D263 到 HuMo263

此前的主流方法（如 MDM、MLD、T2M-GPT、MoMask 等）普遍采用基于逆运动学（IK）推导的 HM3D263 特征表示，这种表示存在两个根本缺陷：一是 IK 求解过程会引入累积误差，二是特征本身缺乏与视觉模态的自然对齐。Being-M0.5 转而采用基于 SMPL 模型的 **HuMo263 直接旋转表示**，直接从视频中通过 WHAM 回归 SMPL 参数，避免了 IK 误差链，同时使运动特征与视觉输入共享统一的参数化空间，为视觉-运动对齐训练奠定了基础。

### 大规模多任务指令训练：HuMo100M

现有运动生成模型的训练数据局限于 HumanML3D 或 KIT-ML 等小规模文本-运动数据集，任务形式单一（几乎仅支持文本到运动），严重制约了模型的可控性维度。Being-M0.5 构建了 **HuMo100M**——目前规模最大的多模态运动数据集，包含超过 500 万条运动序列、配对的视频片段、三倍于现有数据集的层次化和部位级文本描述，以及 1 亿条多任务指令实例。基于该数据集的三阶段训练课程（运动-文本对齐 → 视觉-文本-运动对齐 → 运动指令微调）使模型同时掌握了六种可控生成能力：文本到运动（T2M）、图像到运动（I2M）、指令到未见运动（I2U）、指令到部位运动（I2PM）、指令到长运动（I2LM）以及运动预测与插值（MPI）。

消融实验证实，多任务训练对整体可控性有显著增强作用，视觉-文本-运动对齐阶段的加入使模型在 HuMo-T2M 测试平台上持续优于无视觉集成的变体。更重要的是，在 HuMo100M 上训练后，I2U 任务的 FID 从 18.62（HumanML3D 训练）骤降至 8.65，验证了大规模数据对未见运动模式泛化的关键作用。

### 实时推理架构

与上述创新协同工作的还有**逐帧解码策略**和基于 llama.cpp 的 4-bit 量化推理框架。模型以 7B 参数的 LLaMA-2-chat 为骨干，在 H100 GPU 上达到 28.9 FPS 的峰值推理速度，多 GPU 环境下最低 FPS 为 20，满足实时交互需求。这一架构选择在语言理解能力与计算效率之间取得了最优平衡，使得高度可控的运动生成不再以牺牲实时性为代价。

Being-M0.5 构建于 **LLaVA-video-7B** 框架之上，是一个支持多模态输入/输出的视觉-语言-运动模型（VLMM）。其整体架构围绕三个核心组件展开：视觉编码器、大语言模型骨干网络和运动分词器，并通过三阶段课程训练实现全面的可控运动生成。

### 核心模块与数据流

**视觉编码与投影**：模型采用 **SigLIP**（400M 参数）作为视觉编码器，提取视频帧特征，随后通过一个 **2 层 MLP** 将视觉特征映射到 LLM 的表示空间。为高效处理长视频序列，模型引入了 **慢-快策略（slow-fast strategy）**，在降低视觉 token 复杂度的同时保留时序信息。

**语言骨干网络**：Being-M0.5 选用 **LLaMA-2-chat 7B** 作为核心语言模型。这一选择在语言理解能力与计算效率之间取得了最优平衡——7B 参数量既能胜任多模态理解与生成任务，又能在推理时借助 llama.cpp 框架实现实时性能。

**运动分词器**：运动表征的核心创新在于 **部分感知残差量化（Part-aware Residual Quantization, PRQ）**。与标准残差量化（RQ）不同，PRQ 将人体运动特征按解剖学部位分解为五个独立区域（如左右臂、左右腿、躯干），对每个部位分别进行多层残差量化。这一设计使得模型能够以部位级离散代码表示连续运动，为后续的细粒度控制奠定了基础。

**逐帧解码器**：运动生成采用逐帧解码策略，模型每步输出一帧的运动代码，由解码器实时还原为运动参数。这种设计避免了传统方法中整段生成带来的延迟，是实现实时可控生成的关键。

### 训练流程

VLMM 的训练遵循**三阶段课程**：

1. **运动-文本对齐**：建立运动与自然语言之间的基本映射关系。
2. **视觉-文本-运动对齐**：引入视觉模态，使模型能够理解视频内容与运动和文本的关联。
3. **运动指令微调**：在大规模多任务指令数据上进行微调，赋予模型全面的可控生成能力。

### 输入输出流

模型支持多种输入模态的组合：文本指令、参考图像/视频（用于初始姿态或运动风格指定）、以及部位级控制信号。输出为符合指令要求的连续人体运动序列。具体而言，模型实现了五种可控生成能力：多样化指令跟随、任意初始姿态、长序列生成、未见运动处理以及细粒度部位控制。

### 关键设计权衡

- **量化层数**：实验表明 4 层 PRQ 在生成质量与效率之间达到最优平衡（超过 4 层会因逐帧解码复杂度增加而损害性能）。
- **共享码本**：PRQ 的不同部位共享一个码本，既降低了参数量，又促进了部位间运动模式的协同学习。
- **实时推理**：通过 4-bit 量化和 llama.cpp 加速框架，模型在多 GPU 环境下最低可达 20 FPS，在 H100 上峰值达 28.9 FPS，满足实时交互需求。

> **注意**：关于视觉编码器的具体帧采样策略、慢-快策略的详细实现参数（如帧率比例、池化方式）以及 MLP 投影层的具体维度，原文未提供完整细节，需查阅补充材料或代码库以获取精确配置。

### 视觉编码与投影模块

Being-M0.5 基于 LLaVA-video-7B 框架构建，视觉编码部分采用 **SigLIP**（400M 参数）作为视觉编码器，后接一个 **2 层 MLP** 将视觉特征投影到 LLM 的表示空间。为高效处理长视频序列，模型引入 **slow-fast 策略**，在保留时序信息的同时降低视觉 token 复杂度。

### 运动分词器：部位感知残差量化（PRQ）

PRQ 是 Being-M0.5 实现精细可控运动生成的核心模块。与标准残差量化（RQ）通过迭代堆叠层减少量化误差的思路一致，PRQ 的创新在于将全身运动特征按解剖学部位分解为五个独立区域进行编码，从而支持部位级控制。

**PRQ 的表示形式**为：

$$\mathrm{PRQ}(\tilde{b}_{1:n;1:p}) = [b_{1:n;1:p}^{k}]_{k=0}^{K}$$

其中 $p$ 表示部位数量，$n$ 为序列长度，$K$ 为量化层数。PRQ 输出 $K+1$ 个有序代码序列，每层对应一个部位组。

**残差量化步骤**：

$$b^{k} = \mathcal{Q}(r^{k}), \quad r^{k+1} = r^{k} - b^{k}$$

在第 $k$ 层，编码器从码本中选取最接近当前残差 $r^{k}$ 的向量作为 $b^{k}$，并更新残差 $r^{k+1}$ 为两者之差，供下一层继续逼近。PRQ 的总表示容量为 $\prod_{j=1}^{p} u_{j}$，其中 $u_{j}$ 是部位 $j$ 可引用的不同代码数量，这赋予了模型极大的运动配置组合空间。

### PRQ 训练损失

PRQ 的训练目标由部位级重建损失、全身重建损失和编码承诺损失三部分加权组成：

$$\mathcal{L} = \sum_{j=1}^{p} \| m_{j} - \tilde{m}_{j} \|_{1} + \| m - \tilde{m} \|_{1} + \beta \sum_{k=1}^{K} \sum_{j=1}^{p} \| r_{j}^{k} - \mathrm{sg}[b_{j}^{k}] \|_{2}^{2}$$

其中 $m_{j}$ 和 $\tilde{m}_{j}$ 分别表示部位 $j$ 的原始运动特征与重建特征，$m$ 和 $\tilde{m}$ 为全身特征，$\mathrm{sg}[\cdot]$ 为停止梯度算子，$\beta$ 为承诺损失权重。部位级 L1 损失确保各解剖区域的独立重建精度，全身 L1 损失维护整体运动一致性，承诺损失则约束编码器输出靠近所选码本向量。

### LLM 骨干与逐帧解码器

模型选用 **LLaMA-2-chat 7B** 作为多模态理解与生成的核心语言模型骨干，在语言理解能力和计算效率之间取得平衡。运动生成采用**逐帧解码器**，将 LLM 输出的离散运动代码逐帧解码为连续运动序列，这是实现实时生成的关键设计——量化层数超过 4 层时，逐帧解码的复杂性增加会损害生成性能。

### VLMM 训练损失

整个 VLMM 采用标准下一令牌预测的负对数似然损失进行训练：

$$\mathcal{L}(\boldsymbol{\Theta}) = -\sum_{j=1}^{L} \log P_{\boldsymbol{\Theta}}(y_{j} \mid \mathcal{X}_{Q}, \hat{y}_{1:j-1})$$

其中 $\boldsymbol{\Theta}$ 为模型参数，$y_{j}$ 为第 $j$ 个目标令牌，$\mathcal{X}_{Q}$ 为多模态输入上下文，$\hat{y}_{1:j-1}$ 为已生成的前缀序列。训练遵循三阶段课程：运动-文本对齐、视觉-文本-运动对齐、运动指令微调。

## 实验与关键发现

### 文本到运动生成主结果

Being-M0.5 在 HumanML3D 基准上展现出显著优势。Table 1 显示，采用 PRQ4 配置的 Being-M0.5 实现了 **FID = 0.056**，相较于 VQ1 变体（FID = 0.141）**提升约 60%**，表明部位感知残差量化对生成质量的关键作用。与现有方法相比，该结果在 FID 指标上达到领先水平，验证了 PRQ 在保持运动自然度方面的有效性。

![[assets/figures/papers/paper_list_l1767_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model/figures/004_Table_1.jpg]]
*Table 1: Comparison with previous motion methods on HumanML3D. Superscripts 1 and 2 distinguish different works sharing the same model name, while the subscript n in*

### 未见运动泛化能力

Table 3 的 Instruct-to-Unseen（I2U）任务评估揭示了大规模数据训练的临界重要性。在 HuMo100M 上训练后，Being-M0.5 的 FID 降至 **8.65**，远低于仅在 HumanML3D 上训练的 **18.62**。这一差距（Δ = -9.97）直接证明了 HuMo100M 百万级多任务指令数据对模型泛化到未见运动模式的不可替代作用——小规模数据集（如 HumanML3D、KIT-ML）无法提供足够的运动多样性支撑该能力。

![[assets/figures/papers/paper_list_l1767_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model/figures/007_Table_3.jpg]]
*Table 3: Comparison on the Instruct-to-Unseen (I2U) task using the HuMo-Unseen testbed across diverse training datasets*

### 部位级控制精度

部位感知控制是 Being-M0.5 的核心创新之一。在左右交换测试中，模型对指定身体部位的运动控制成功率达到 **76%**（Section 5.3.3），证明 PRQ 确实实现了解剖学区域级别的精确生成能力。该测试要求模型在保持其他部位不变的前提下，仅交换左右侧部位的运动模式——这是非部位感知方法（如标准 RQ）无法完成的任务。

### 实时推理性能

Being-M0.5 基于 llama.cpp 推理框架，在多 GPU 环境下最低 FPS 为 **20**，在 H100 上峰值达 **28.9 FPS**（Figure 5, Section 5.3.3），满足实时应用需求。值得注意的是，该模型以 7B 参数的 LLaMA-2 为主干，通过 4-bit 量化实现在消费级硬件上的可部署性，但量化可能引入精度损失，需在速度与质量间权衡。

![[assets/figures/papers/paper_list_l1767_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model/figures/009_Figure_5.jpg]]
*Figure 5: Being-M0.5 inference speed across different GPUs. We accelerate motion generation via modern LLM inference framework llama.cpp [57]. Our model achieves real-time inference speed using the 7B-parameter LLaMA backbone*

### 消融实验关键发现

**PRQ 架构与部位标签的互补性**：Table 6 的消融表明，当训练中移除部位文本描述（PT? = No）时，PRQ 的性能反而低于对应的 RQ 变体。这说明 PRQ 的解剖学分解必须与部位级语言监督协同工作——仅有结构先验而无语义对齐无法发挥其优势。同时，移除共享关节（w/o Shared）在 HuMo-I2PM 上显著降低性能，验证了跨部位信息共享对协调全身运动的重要性。

**量化层数的非单调效应**：增加 PRQ 量化层数超过 4 层后，生成性能反而下降（Section 5.4.1）。这是因为逐帧解码的复杂性随层数增长，更深层的量化引入了累积误差，而运动表示的增益递减。4 层 PRQ 被确定为质量-效率的最优平衡点。

**视觉-文本-运动对齐的必要性**：Table 7 显示，经过第二阶段视觉-文本-运动对齐训练的模型持续优于无视觉集成的变体。这证实了视觉模态为运动生成提供了文本难以捕捉的细粒度时空线索。

**多任务训练的增益**：Table 8 的评估表明，多任务指令训练（涵盖 T2M、I2M、I2U、I2PM、I2LM、MPI）显著增强了模型的整体可控性，单一任务训练无法达到同等的指令遵循能力。

### 评估公平性说明

需要指出以下评估局限性：部分自定义基准（如 HuMo-I2PM）尚未被社区广泛采用，结果可能受基准设计影响；参与比较的基线方法均使用公开训练代码，但训练数据规模与任务设置存在差异；实时性能测量依赖特定推理框架（llama.cpp）和硬件（H100），不同环境下的速度可能波动。FID 作为主要质量指标，对运动数据的分布特性敏感，在跨数据集比较时需谨慎解读。

![[assets/figures/papers/paper_list_l1767_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model/figures/011_Table_6.jpg]]
*Table 6: Comparison of part-level motion configurations on the HuMo-I2PM testbed, where “PT?” denotes the inclusion/exclusion of part-level descriptions during training*

![[assets/figures/papers/paper_list_l1767_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model/figures/012_Table_7.jpg]]
*Table 7: Comparison of text-aligned visual clips on the HuMo-T2M testbed, where “2nd vis” indicates the second-stage training for vision-text-motion alignment."*

![[assets/figures/papers/paper_list_l1767_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model/figures/014_Figure_6.jpg]]
*Figure 6: Qualitative examples generated by Being-M0.5 for Instruct-to-PartMotion (I2PM) and Instruct-to-LongMotion (I2LM). The results demonstrate the ability of our model to generate motion sequences that accurately align with both part-level and long-term instructions*

## 定位与知识库关联

### 1. 与基线方法的关系

Being‑M0.5 的提出根植于两条并行演进的路线：**基于量化的运动生成**和**多模态运动‑语言建模**。其核心创新并非对单一范式的修补，而是通过解剖学部位感知的离散化策略，将两条路线在“可控性”这一瓶颈上交汇。

#### 1.1 量化运动生成路线

在 Being‑M0.5 之前，残差量化（RQ）已被引入运动生成以压缩连续运动序列。**T2M‑GPT**、**MoMask**、**MotionGPT** 等方法将全身运动编码为一组有序的离散标记，再利用自回归或掩码模型生成。然而，这些方法存在一个共同的因果盲区：**离散化发生在全局运动特征上，任何对局部肢体的操控都不可避免地干扰整体编码**。这导致即使模型能生成高质量的文本‑运动对，也无法支持“左手抬起、其余静止”这类细粒度指令。

Being‑M0.5 通过**部分感知残差量化（PRQ）** 切断了这一因果链。PRQ 将运动特征按五个解剖区域（躯干、左臂、右臂、左腿、右腿）分解为部位级潜变量，再分别进行残差量化。形式上，若 $p$ 个部位的第 $k$ 层量化残差为 $r^{k}_{1:p}$，则 PRQ 输出 $K+1$ 层有序代码序列：

$$\mathrm{PRQ}(\tilde{b}_{1:n;1:p}) = [b^{k}_{1:n;1:p}]_{k=0}^{K}$$

每一层的量化步骤为：

$$b^{k} = \mathcal{Q}(r^{k}), \quad r^{k+1} = r^{k} - b^{k}$$

这种设计使得部位间在离散空间相互解耦，同时共享码本以保持全身运动的一致性。**消融实验直接验证了这一因果机制**：当移除部位标签（PT? 关闭）时，PRQ 的性能反而低于同等层数的 RQ 变体（Table 6），说明部位感知的离散化本身——而非单纯的量化深度——才是性能增益的来源。

#### 1.2 多模态运动‑语言建模路线

**MotionGPT**、**MotionLLM**、**MotionChain** 等工作初步探索了将运动作为“语言”接入大语言模型（LLM）的范式，但它们的可控性受限于两个因素：（1）运动标记化仍为全局方式；（2）训练数据规模与任务多样性不足。Being‑M0.5 直接继承了 **LLaVA‑video‑7B** 的视觉‑语言架构（SigLIP 编码器 + 2‑层 MLP 投影 + LLaMA‑2‑chat 7B 骨干），但将运动模态的接入点从“全局离散标记”替换为“部位级离散标记”。这一替换使得 LLM 在逐帧解码时能够有选择地关注特定部位的代码，从而在不牺牲语言理解能力的前提下实现部位控制。

#### 1.3 数据规模带来的因果杠杆

Being‑M0.5 在 HuMo100M（超 500 万运动序列、1 亿多任务指令）上训练后，**Instruct‑to‑Unseen（I2U）任务的 FID 从 18.62 骤降至 8.65**（Table 3）。这一差距的因果解释是：小规模数据集（如 HumanML3D）缺乏足够的未见运动模式覆盖，模型只能记忆常见动作；而 HuMo100M 中的多任务指令（T2M、I2M、I2U、I2PM、I2LM、MPI）迫使模型学习“指令‑部位‑运动”之间的通用映射，从而在未见运动上展现出强泛化能力。**多任务训练消融（Table 8）进一步证实，移除任一任务都会损害整体可控性**，说明各任务间存在正向迁移。

### 2. 适用边界与局限

#### 2.1 部位控制的粒度上限

PRQ 将人体划分为五个预定义区域，这使得模型能实现“交换左右手动作”这类区域级控制（成功率 76%），但**无法下沉到单关节级别**（如仅控制食指）。部位划分的粒度由解剖学先验固定，缺乏动态调整的灵活性。若需手指层级的精细操作，当前框架需要重新设计部位划分方案和对应的文本监督。

#### 2.2 数据驱动的噪声敏感性

HuMo100M 的运动序列主要来源于网络视频，通过 WHAM 提取 SMPL 参数。**运动估计的噪声在极端姿态或遮挡场景下可能被放大**，导致生成的部位动作出现抖动或不符合物理约束。模型缺乏对运动学约束的显式建模，完全依赖数据分布来隐式学习合理性。

#### 2.3 实时推理的精度‑速度权衡

Being‑M0.5 的实时性能（H100 上峰值 28.9 FPS）依赖 llama.cpp 框架和 4‑bit 量化。量化引入的精度损失在常规动作上不显著，但在需要高精度部位协调的场景（如单手倒立）中可能导致动作失真。**增加 PRQ 层数超过 4 层会损害生成质量**（Section 5.4.1），因为逐帧解码的复杂性上升，而量化带来的信息增益递减。

#### 2.4 视觉模态的辅助角色

当前框架中，视觉输入主要用于训练阶段的视觉‑文本‑运动对齐，而非直接驱动生成。模型尚未具备从视频中端到端估计并生成运动的能力，这限制了其在“给定一段视频，让角色模仿动作”类应用中的直接可用性。

### 3. 开放问题

- **部位划分的动态化**：能否根据指令自动调整部位划分粒度（如手指层级、面部表情），而非固定为五个区域？这需要可学习的部位分解机制和对应的层次化文本监督。
- **端到端视频‑运动生成**：如何将视觉运动估计（如 WHAM 的 SMPL 回归）完全融合进 VLMM 的生成流程，使得模型能直接从原始视频中提取运动先验并用于可控生成？
- **多人交互与复杂场景泛化**：当前模型针对单人运动设计，在多人协作（如双人舞、对抗运动）或与物体交互的场景下，部位控制是否仍然有效？这要求模型理解空间关系和社会性运动约束。
- **低算力设备的实时性**：在移动端或嵌入式设备上，如何在不牺牲部位控制精度的前提下维持实时性能？可能需要探索更轻量的量化策略或蒸馏方案。
- **运动学约束的显式建模**：引入物理先验（如关节角度限制、动力学方程）作为生成约束，能否减少数据噪声带来的伪影，同时不损害模型的多样性和可控性？

## 原文 PDF

![[paperPDFs/ICCV_2025/Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model.pdf]]
