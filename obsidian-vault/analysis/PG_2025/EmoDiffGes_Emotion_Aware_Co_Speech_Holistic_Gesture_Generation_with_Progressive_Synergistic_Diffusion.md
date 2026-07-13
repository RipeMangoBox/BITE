---
title: "EmoDiffGes: Emotion-Aware Co-Speech Holistic Gesture Generation with Progressive Synergistic Diffusion"
type: paper
paper_level: A
venue: PG
year: 2025
pdf_ref: paperPDFs/PG_2025/EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Progressive_Synergistic_Diffusion.pdf
project_link: null
code_link: null
aliases:
- EmoDiffGes
tags:
- PG_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过滑动窗口提取分段式动态情感特征，并将其加权注入身体各区域生成流，同时采用渐进式区域间协同流（PIRSF）保证全局运动一致性。
primary_logic: 基于具身情感理论，将身体分解为四个区域并分别用离散潜变量建模，利用动态情感标签统一指导手势生成，并通过级联交叉注意力实现区域间协调，克服了整体与局部之间的表达矛盾。
claims:
- 现有方法存在两大基本局限：忽略情绪的时间演变，以及整体简化或部分独立建模导致的不连贯。
- 提出的EmoDiffGes框架通过动态情绪调节和部分感知协同建模统一了这两方面。
- DEAM提取动态情绪线索并注入生成过程，PSGG迭代精细化区域特定隐编码并保持全身协调。
- BEAT-X 上 User preference (realism, expressiveness, rhythmic alignmen... = highest ratings
---

# EmoDiffGes: Emotion-Aware Co-Speech Holistic Gesture Generation with Progressive Synergistic Diffusion

> [!tip] 核心洞察
> 基于具身情感理论，将身体分解为四个区域并分别用离散潜变量建模，利用动态情感标签统一指导手势生成，并通过级联交叉注意力实现区域间协调，克服了整体与局部之间的表达矛盾。

| 字段 | 内容 |
|------|------|
| 中文题名 | EmoDiffGes：基于情感感知的共语音整体手势渐进协同扩散生成模型 |
| 英文题名 | EmoDiffGes: Emotion-Aware Co-Speech Holistic Gesture Generation with Progressive Synergistic Diffusion |
| 会议/期刊 | PG 2025 |
| Links |  [paper](https://doi.org/10.1111/cgf.70261)|
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EmoDiffGes |
| Dataset | BEAT-X |

> [!tip] 效果简介
> - BEAT-X 上，User preference (realism, expressiveness, rhythmic alignment, semantic alignmen... highest ratings vs CaMN, EMAGE, DiffSHEG (significantly better across all criteria)；FGD, BC, Diversity, MSE, LVD, BESA, BESA-ELO 4.312, 0.787, 12.75, 7.435, 7.713, 0.509, 1562.55 vs SOTA methods (see Table 1) (outperforms on all metrics)。

## 概要

**问题瓶颈**：现有共语音手势生成方法面临两大根本局限——（1）忽略情绪随时间的动态演变，导致生成的手势缺乏表现力；（2）要么将身体作为整体过度简化建模，要么对身体各部分独立建模，致使动作不连贯、不自然。这两个问题共同阻碍了富有情感且全身协调的共语音手势生成。

**核心结论**：本文提出 **EmoDiffGes**，一个基于具身情感理论的扩散框架，将动态情感调节与身体分区协同建模相统一。框架通过滑动窗口从文本转录中提取分段式动态情感特征，并将其加权注入身体各区域的生成流；同时将身体分解为面部、上半身、手部和下半身四个区域，采用渐进式区域间协同流（PIRSF）以级联交叉注意力实现区域间协调，最终生成情感表达丰富且全身一致的手势。

**方法定位**：EmoDiffGes 在共语音手势生成领域引入了动态情感时间建模与分区离散潜空间协同生成的双重创新。相较于整体建模方法（如 **CaMN**）或统一掩码建模方法（如 **EMAGE**, Liu et al., CVPR 2024），以及扩散式方法（如 **DiffSHEG**, Chen et al., CVPR 2024），EmoDiffGes 首次将分段情感特征与身体分区渐进协同流结合，解决了整体与局部之间的表达矛盾。

**主要结果**：在 BEAT-X 基准上，EmoDiffGes 在所有指标上均优于现有方法（FGD 4.312, BC 0.787, Diversity 12.75, MSE 7.435, LVD 7.713, BESA 0.509, BESA-ELO 1562.55）。用户研究进一步证实，该方法在真实感、表现力、节奏对齐和语义对齐四个维度上均获得最高评分。消融实验验证了动态情感对齐模块（DEAM）、渐进区域协同流（PIRSF）以及分区潜空间设计各自对性能的关键贡献。



共语音手势生成旨在根据语音输入合成自然、协调的身体动作，是虚拟人交互、具身智能体等应用的核心技术。近年来，扩散模型在该领域取得了显著进展，但现有方法普遍面临两个根本性局限，严重制约了生成手势的表现力与身体协调性。

**瓶颈一：情感的时间动态被忽略。** 情感并非静态标签——同一段语音中，说话者的情绪状态会随时间演变，而身体各部位对情感的响应方式也各不相同。然而，现有方法要么完全不引入情感条件，要么仅使用单一的整体情感标签，无法捕捉这种时序上的动态变化。这导致生成的手势缺乏表现力，难以传达语音中蕴含的丰富情感层次。

**瓶颈二：身体建模的整体简化与部分独立之间的矛盾。** 当前方法通常采取两种策略：一种是将身体视为单一整体进行建模，忽略了面部、上肢、手部和下肢在运动模式上的本质差异；另一种是将各部位完全独立建模，缺乏区域间的协同机制。前者导致动作粗糙、缺乏细节，后者则产生不连贯、不自然的整体运动。如原文所述，这两种路径都会生成“不连贯、不自然且缺乏表现力的动作”。

上述两个瓶颈并非孤立存在——它们共同指向一个核心矛盾：如何在保持全身运动一致性的同时，让每个身体区域都能独立响应动态变化的情感信号？这一矛盾在现有框架下难以调和，因为静态或缺失的情感条件无法为分区域建模提供有效的统一指导，而整体建模又抹杀了区域差异性。

**本文动机：基于具身情感理论的统一框架。** 具身情感理论指出，情感体验与身体表达之间存在双向映射关系，不同身体区域在情感表达中扮演不同角色。受此启发，本文提出 **EmoDiffGes**，一个基于扩散模型的统一框架，通过两条核心路径同时解决上述瓶颈：

1. **动态情感对齐**：从文本转录中提取分段式情感特征，捕捉情感的时间演变，并将其加权注入各身体区域的生成流中，使每个区域都能获得与其表达角色相匹配的动态情感指导。
2. **渐进式区域协同**：将身体分解为面部、上肢、手部和下肢四个区域，分别用离散潜变量建模，再通过级联交叉注意力机制实现区域间的渐进式信息流动，在保持区域特异性的同时确保全身运动协调。

这一设计从根本上克服了整体简化与部分独立之间的表达矛盾，使手势生成既能体现细腻的情感动态，又能保持自然连贯的整体运动。



## 核心方法与创新机理

EmoDiffGes 针对现有共语音手势生成方法的两个根本瓶颈——忽略情感的时间动态演变，以及将身体整体简化或各部分独立建模导致动作不连贯——提出了统一框架。其核心创新体现在三个紧密耦合的“changed slots”上，共同实现了动态情感感知与身体区域协同的生成。

**1. 从静态情感到分段动态情感注入**

现有方法（如 **CaMN**、**EMAGE** (Liu et al., CVPR 2024)、**DiffSHEG** (Chen et al., CVPR 2024)）通常忽略情感的时间演变，或仅使用静态情感标签。EmoDiffGes 通过 **动态情感对齐模块 (DEAM)** 实现了分段式动态情感提取与加权注入。DEAM 利用预训练的 EmoRoBERTa 模型，以滑动窗口（窗口大小 $W=128$ 帧，步长 $D=20$ 帧）对输入文本转录进行分割，提取 28 种细粒度情感类别的动态特征。这些情感特征随后被按身体区域加权（$\hat{E}_i = w_i E_i$），分别注入面部、上半身、手部和下半身的生成流中，使得每个身体区域能够根据其情感表达重要性获得差异化的情感指导。

**2. 从单一整体或独立建模到组合式区域离散潜空间**

现有方法要么将全身动作压缩到单一潜空间导致细节丢失，要么独立建模各部位导致协调性差。EmoDiffGes 构建了**四个独立的残差向量量化变分自编码器 (RVQ-VAE)**，分别对应面部、上半身、手部和下半身四个身体区域。每个区域的动作被编码为离散潜变量，通过向量量化（$\tilde{z}_i = Q(z_i), \; i = \arg\min_i \| c_i - z_i \|^2$）映射到各自的码本中。这种组合式潜空间设计既保留了各区域的运动细节表达能力，又为后续的协同生成提供了结构化基础。消融实验证实，分离的四大区域潜空间相比单一整体潜空间显著降低了 FGD（4.978→4.312）。

**3. 从独立生成到渐进式区域间协同流 (PIRSF)**

为解决区域间协调问题，EmoDiffGes 设计了**渐进式区域间协同流 (PIRSF)**。四个身体区域的生成流按面部→上半身→手部→下半身的顺序级联，每个流通过专用的交叉注意力模块（$A_c = \mathrm{SoftMax}\left( \frac{Q_{region} \cdot K_{cond}}{\sqrt{d}} \right) V_{cond}$）同时接受音频条件、加权情感特征以及前序流的输出作为条件。这种级联交叉注意力机制确保了信息从前到后的逐步传递与整合，使全身动作在保持区域特性的同时实现全局协调。消融实验表明，包含完整四条流的 PIRSF 配置在所有指标上均达到最优。



EmoDiffGes 是一个基于扩散模型的共语音整体手势生成框架，其核心设计遵循具身情感理论（embodied emotion theory），将动态情感调节与身体部位感知协同建模统一在单一流程中。整体 pipeline 由三个关键模块串联构成：**动态情感对齐模块（DEAM）**、**身体区域先验（Body Regions Prior）** 和 **渐进式区域间协同流（PIRSF）**，最终通过去噪扩散过程生成完整的手势序列。

### 输入与预处理

框架接收两类输入：**语音音频** 和 **文本转录**。音频特征（振幅、onset 等）经编码后与文本嵌入通过平均池化融合，形成统一的条件表示。文本转录同时送入预训练的 **EmoRoBERTa** 模型，该模型能够识别 28 种细粒度情感类别（如 admiration、amusement、anger 等），为后续的动态情感注入提供基础。

### 动态情感对齐模块（DEAM）

DEAM 负责从文本转录中提取时间上动态变化的情感线索，并将其注入生成过程。具体而言，采用滑动窗口策略对输入序列进行分段：窗口大小 $W = 128$ 帧，步长 $D = 20$ 帧。对每个分段，EmoRoBERTa 输出该段的细粒度情感特征 $E_i$。随后通过加权分配方案，将情感特征按身体区域的情感相关性赋予不同权重：

$$ \hat{E}_i = w_i E_i $$

其中 $w_i$ 为区域 $i$ 的情感权重。加权后的情感特征 $\hat{E}_i$ 被注入到后续各身体区域的生成流中，确保手势表现力随情感动态演变。

### 身体区域先验

与以往将身体整体建模或各部分独立建模的方法不同，EmoDiffGes 将身体分解为四个独立区域：**面部（face）**、**上半身（upper body）**、**手部（hands）** 和 **下半身（lower body）**。每个区域分别通过一个 **残差向量量化变分自编码器（RVQ-VAE）** 编码到离散潜空间：

$$ \tilde{z}_i = Q(z_i), \quad Q(z_i) = c_i \quad \mathrm{where} \quad i = \arg \min_i \| c_i - z_i \|^2 $$

其中 $z_i$ 为编码器输出的连续潜在向量，$c_i$ 为码本中距离最近的条目。这种分区域离散潜空间设计既保留了各区域的运动特异性，又为后续协同建模提供了结构化的表示基础。

### 渐进式区域间协同流（PIRSF）

PIRSF 是框架的核心生成引擎，采用级联交叉注意力机制实现四个区域流的渐进式整合。生成顺序为：**面部 → 上半身 → 手部 → 下半身**。每个区域流独立处理，通过专用的交叉注意力块同时关注两类条件信息：

1. **音频-文本融合条件**：提供语音内容和韵律的时间对齐信息；
2. **前置区域流的输出**：实现区域间的信息传递与协同。

交叉注意力的计算方式为：

$$ A_c = \mathrm{SoftMax}\left( \frac{Q_{\text{region}} \cdot K_{\text{cond}}}{\sqrt{d}} \right) V_{\text{cond}} $$

其中 $Q_{\text{region}}$ 为当前区域流的查询，$K_{\text{cond}}$、$V_{\text{cond}}$ 来自条件输入和前置区域输出。这种级联设计使得面部表情引导上半身姿态，上半身进一步约束手部动作，最终由下半身补充整体平衡，从而保证全身运动的协调性与自然度。

### 去噪扩散与解码

各区域流输出的潜在表示经过扩散模型的逆向去噪过程，从纯噪声逐步恢复为干净的区域潜编码 $\hat{z}_0$。随后通过量化器与对应区域的解码器重建各区域的运动帧，最终拼接为完整的手势序列。整个流程的端到端训练由潜损失、重建损失和扩散损失的加权和驱动：

$$ L_{\text{final}} = \lambda_{\text{latent}} L_{\text{latent}} + \lambda_{\text{rec}} L_{\text{rec}} + \lambda_{\text{diff}} L_{\text{diff}} $$

其中重建损失 $L_{\text{rec}} = L_1(m, \hat{m})$ 保证运动保真度，扩散损失 $L_{\text{diff}} = \| \delta(t_d) - \Delta(m(t_d), \text{cond}, t_d) \|_2^2$ 监督去噪器的预测精度。

### 设计动机与对比

图 2 直观对比了现有方法与 EmoDiffGes 的设计差异：传统方法或对身体进行整体简化建模，或将各部分独立处理，导致手势缺乏情感表现力且身体各部分运动不协调。EmoDiffGes 通过将动态情感线索注入分区域生成流，并在区域间建立渐进式信息传递，从机制层面解决了这两个根本性局限。

### 补充图表


![[assets/figures/papers/paper_list_l1921_EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Prog/figures/002_Figure_2.jpg]]
*Figure 2: Top: Previous methods typically either represent the body holistically or decompose it into independently modeled parts, often generating incoherent, unnatural and inexpressive motions. Bottom: Our method incorporates temporal emotional cues into the motion representation by conditioning region-specific body streams, enabling more coherent and expressive gesture generation*



EmoDiffGes 的核心架构围绕三个关键模块展开：**身体区域先验（Body Regions Prior）**、**动态情感对齐模块（DEAM）** 和 **渐进式区域间协同流（PIRSF）**，三者协同构成一个完整的扩散生成框架。

### 身体区域先验与离散潜空间

基于具身情感理论，身体被分解为四个独立区域：面部（face）、上半身（upper body）、双手（hands）和下半身（lower body）。每个区域通过一个独立的残差向量量化变分自编码器（RVQ-VAE）编码到离散潜空间。给定区域运动帧 $m_i$，编码器输出潜向量 $z_i$，经向量量化得到：

$$\tilde{z}_i = Q(z_i), \quad Q(z_i) = c_i \quad \mathrm{where} \quad i = \arg \min_i \| c_i - z_i \|^2$$

其中 $c_i$ 为码本中距离最近的条目。解码器从量化潜向量重建运动帧：

$$m_i = D(\tilde{z}_i) = D(Q(\epsilon(m_i)))$$

RVQ-VAE 的训练损失为加权重建损失与承诺损失的组合：

$$L_{\mathrm{RVQ-VAE}} = \lambda_{\mathrm{rec}} \cdot L_{\mathrm{rec}}(m, \hat{m}) + \beta \cdot (\| \mathrm{sg}[z] - \tilde{z}_i \|^2 + \| z - \mathrm{sg}[\tilde{z}_i] \|^2)$$

其中 $\lambda_{\mathrm{rec}}=1$，$\beta=0.25$，$\mathrm{sg}[\cdot]$ 为停止梯度算子。这种分区域离散化建模从根本上解决了整体简化导致的运动不协调问题（消融实验证实，分离的四大区域潜空间相比单一整体潜空间将 FGD 从 4.978 降至 4.312，见 Supplementary Table 1）。

### 动态情感对齐模块

DEAM 负责从文本转录中提取时序动态情感特征。模块采用预训练的 EmoRoBERTa 模型，该模型可识别 28 种细粒度情感类别。输入序列通过滑动窗口（窗口大小 $W=128$ 帧，步长 $D=20$ 帧）进行分段，为每个片段提取情感表征，从而捕捉情感的时间演变。

提取的情感特征 $E_i$ 按身体区域进行加权分配：

$$\hat{E}_i = w_i E_i$$

权重 $w_i$ 反映了不同身体区域对情感表达的贡献差异——例如，面部和手部通常承载更丰富的情感信息，因此获得更高权重。加权后的情感特征 $\hat{E}_i$ 被注入到对应区域流的生成过程中，作为扩散模型的条件信号之一。

### 渐进式区域间协同流

PIRSF 是保证全身运动协调性的核心机制。四个区域流按面部 → 上半身 → 双手 → 下半身的顺序级联处理，每个流包含独立的输入处理和交叉注意力块。后续流通过交叉注意力接收前序流的输出，实现区域间信息传递：

$$A_c = \mathrm{SoftMax}\left( \frac{Q_{region} \cdot K_{cond}}{\sqrt{d}} \right) V_{cond}$$

其中 $Q_{region}$ 为当前区域的查询，$K_{cond}$ 和 $V_{cond}$ 为条件信息的键和值（包括音频特征和前序流的输出）。这种级联设计使得面部流首先捕获最丰富的情感表达，然后逐步将信息传递给上半身、双手和下半身流，形成自顶向下的协调生成。

### 扩散过程与损失函数

潜空间中的前向扩散过程逐步向潜表示 $z$ 添加高斯噪声：

$$q(z_t | z) = \mathcal{N}(\sqrt{\bar{\alpha}_t} z, (1 - \bar{\alpha}_t) I)$$

去噪器在逆向过程中从噪声恢复潜编码，条件包括音频特征、文本嵌入和动态情感特征。训练包含三个损失项：

重建损失确保解码后的运动与原始运动一致：
$$L_{rec} = L_1(m, \hat{m}), \quad \mathrm{where} \quad \hat{m} = \mathrm{Decoder}(\mathrm{Quantizer}(\hat{z}_0))$$

扩散损失监督去噪器的噪声预测：
$$L_{diff} = || \delta(t_d) - \Delta(m(t_d), cond, t_d) ||_2^2$$

总损失为三项的加权和：
$$L_{final} = \lambda_{latent} L_{latent} + \lambda_{rec} L_{rec} + \lambda_{diff} L_{diff}$$

消融实验表明，完整的四级联流（包含 Lower Stream）在 PIRSF 中表现最优（Table 3），DEAM 模块显著增强了生成手势的情感表达力和连贯性（Figure 8）。

### 补充图表

![[assets/figures/papers/paper_list_l1921_EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Prog/figures/004_Figure_4.jpg]]
*Figure 4: The architecture of Different Body Regions Prior with Residual Vector Quantization*

![[assets/figures/papers/paper_list_l1921_EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Prog/figures/005_Figure_5.jpg]]
*Figure 5: The architecture of Progressive Inter-Region Synergistic Flow (PIRSF)*



## 实验与关键发现

### 主实验：定量对比与用户研究

EmoDiffGes 在 BEAT-X 基准上进行了全面的定量评估，与当前主流的共语音手势生成方法 **CaMN**、**EMAGE** (Liu et al., CVPR 2024) 和 **DiffSHEG** (Chen et al., CVPR 2024) 进行对比。评估指标覆盖几何精度与语义对齐两个维度：FGD（Fréchet Gesture Distance）衡量生成手势与真实手势分布的距离，BC（Beat Consistency）评估节奏同步性，Diversity 反映动作多样性，MSE 和 LVD 度量重建精度与肢体速度一致性，BESA 和 BESA-ELO 则通过视觉语言模型（VLM）评估情感语义对齐质量。

如 Table 1 所示，EmoDiffGes 在所有指标上均取得最优结果：FGD 达 4.312，BC 为 0.787，Diversity 为 12.75，MSE 为 7.435，LVD 为 7.713，BESA 为 0.509，BESA-ELO 为 1562.55。这些结果表明，提出的方法在保持运动真实性、节奏同步和多样性的同时，显著提升了手势的情感表达力与语义一致性。

![[assets/figures/papers/paper_list_l1921_EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Prog/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison with SOTA methods. For visual clarity, we scale FGD by*

![[assets/figures/papers/paper_list_l1921_EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Prog/figures/013_Table_1.jpg]]
*Table 1: Quantitative ablation study for a single whole-body latent space*

用户研究进一步验证了主观感知质量。20 名性别均衡的参与者从真实感、表达力、节奏对齐和语义对齐四个维度对生成手势进行评分。EmoDiffGes 在所有维度上均获得最高评分（Figure 7），确认了模型在人类感知层面的优势。

![[assets/figures/papers/paper_list_l1921_EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Prog/figures/011_Figure_7.jpg]]
*Figure 7: Results of the user study*

### 消融实验：关键模块的有效性

消融实验系统验证了残差量化层数、区域流配置、动态情感模块（DEAM）以及渐进区域协同流（PIRSF）的贡献。

**残差量化层数**：Table 2 显示，随着残差量化层数 R 从 2 增加到 6，FGD 从 5.123 持续下降至 4.312，BC 和 Diversity 相应提升。R=6 时达到最佳性能，表明更深的残差量化能够更精细地捕捉身体各区域的运动细节。

**区域流配置**：Table 3 探索了 PIRSF 中不同区域流的组合。完整配置（包含 Lower Stream）在所有指标上表现最优。移除 Lower Stream 导致 FGD 上升、BC 下降，说明下肢运动对全身协调性有不可忽视的贡献。

**动态情感模块（DEAM）**：Figure 8 的定性对比显示，移除 DEAM 后生成的手势缺乏情感表现力，动作趋于机械和单调。完整模型则能根据输入文本的情感动态生成富有变化和感染力的手势。

**渐进区域协同流（PIRSF）**：Figure 9 的定性消融表明，PIRSF 的级联交叉注意力机制使得面部、上半身、手部和下肢的运动逐步协调。移除协同流后，各区域运动出现明显的不连贯和冲突现象。

**分离区域潜空间 vs. 整体潜空间**：Supplementary Table 1 对比了使用四个独立区域 RVQ-VAE 与单一整体 RVQ-VAE 的性能。分离潜空间将 FGD 从 4.978 降至 4.312，其他指标也全面改善，验证了分区域建模对捕捉身体各部分差异化运动模式的有效性。

### 失败模式与局限性

尽管 EmoDiffGes 取得了显著进展，仍存在以下局限：

1. **多说话人适应性缺失**：当前模型不支持根据说话人身份、情感风格或习惯进行个性化手势生成，限制了其在多角色场景中的应用。
2. **情感线索来源单一**：情感条件完全依赖文本转录，可能忽略仅通过语音韵律变化传达的细微情绪（如语调、停顿），导致情感建模不够全面。
3. **推理效率未评估**：论文未讨论扩散模型的推理速度，对于需要实时交互的应用场景，其实际可行性尚需进一步验证。

### 关键图表结论

- **Table 1**：EmoDiffGes 在几何精度和情感语义对齐上全面超越 SOTA 方法。
- **Table 2 & Table 3**：6 层残差量化和完整四区域协同流是性能最优的配置。
- **Figure 8 & Figure 9**：DEAM 和 PIRSF 分别是情感表达力和运动协调性的关键保障。
- **Supplementary Table 1**：分区域潜空间建模显著优于整体建模，是方法设计的核心基础。

![[assets/figures/papers/paper_list_l1921_EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Prog/figures/008_Table_2.jpg]]
*Table 2: Quantitative ablation study on Residual Quantization Layers*

![[assets/figures/papers/paper_list_l1921_EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Prog/figures/009_Table_3.jpg]]
*Table 3: Quantitative ablation study on Region Stream in PIRSF*

![[assets/figures/papers/paper_list_l1921_EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Prog/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative ablation study for DEAM. Top: the results without DEAM. Bottom: the results of our full model*

![[assets/figures/papers/paper_list_l1921_EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Prog/figures/012_Figure_9.jpg]]
*Figure 9: Qualitative ablation study for PIRSF*



## 定位与知识库关联

### 核心定位与差异化

EmoDiffGes 的提出直指现有共语音手势生成领域的两个根本性瓶颈：**情感动态演化的缺失**与**身体各部分建模的不协调**。此前的方法要么将身体视为一个整体进行简化建模，要么将各部分独立处理，导致生成的手势缺乏表现力、动作不连贯（Figure 2）。EmoDiffGes 基于具身情感理论，通过“动态情感调节”与“部分感知协同”两条主线，将这两个矛盾统一在同一扩散框架下。

具体而言，其差异化体现在三个关键设计上：

1. **从静态到动态的情感注入**：基线方法（如 **EMAGE** (Liu et al., CVPR 2024)、**DiffSHEG** (Chen et al., CVPR 2024)）通常不使用情感条件或仅使用全局静态情感标签。EmoDiffGes 通过滑动窗口（W=128帧，步长D=20）对文本转录进行分段，利用 EmoRoBERTa 提取28类细粒度动态情感特征，并将其加权注入各身体区域的生成流中，使手势能随话语情感实时演变。

2. **从整体/独立到协同的身体表示**：现有方法或使用单一整体潜空间（如 **CaMN**），或对各部分独立建模。EmoDiffGes 将身体分解为面部、上半身、手部、下半身四个区域，分别用独立的残差向量量化变分自编码器（RVQ-VAE）构建离散潜空间，再通过渐进式区域间协同流（PIRSF）以级联交叉注意力（面部→上半身→手部→下半身）保证全局运动一致性，克服了整体简化与局部独立之间的矛盾。

3. **扩散模型的条件化生成**：在扩散反向过程中，去噪器同时接受音频特征（振幅、起始点）、文本嵌入与动态情感特征的多模态条件输入，通过加权情感分配方案使不同身体区域根据情感相关性获得差异化的指导信号。

### 适用边界与局限

尽管 EmoDiffGes 在 BEAT-X 数据集上取得了全面的定量与定性优势（Table 1），其设计仍存在明确的适用边界：

- **单说话人限制**：当前框架未建模说话人身份、情感风格或个性化手势习惯，无法根据个体差异自适应调整手势风格。这在多说话人场景或需要保持角色一致性的应用中构成明显短板。
- **情感来源的单一性**：动态情感特征完全依赖于文本转录，忽略了仅通过语音韵律变化（如语调、语速、音量）传达的细微情绪。当文本与语音情感不一致或文本本身情感信息稀疏时，情感调节的有效性可能下降。
- **推理效率未明确**：扩散模型的迭代去噪过程天然存在推理延迟问题，论文未讨论该框架的推理速度及是否满足实时交互需求，这在实际部署中是需要手动验证的关键点。
- **数据集依赖性**：所有实验均在 BEAT-X 数据集上进行，该数据集虽包含多模态标注，但其情感标注的粒度和覆盖范围可能限制模型在开放域场景下的泛化能力。

### 开放问题与后续方向

基于上述局限，以下几个方向值得后续工作关注：

1. **多模态情感协同建模**：如何将音频韵律信息（如基频、能量、节奏）与文本情感特征深度融合，以更全面、鲁棒地捕捉说话过程中的情感动态？这可能需要设计跨模态对齐机制或联合情感编码器。

2. **个性化与多说话人扩展**：如何引入说话人身份嵌入或风格编码，使框架能够根据个体差异（如手势幅度偏好、习惯性动作）自适应调整生成结果？这涉及到解耦内容、情感与风格表征的表示学习问题。

3. **情感评估的标准化**：论文提出的基于视觉语言模型的情感语义对齐评估（BESA 和 BESA-ELO）虽具创新性，但其与心理学或情感计算领域既有评估标准的对应关系尚不明确。该方法的可推广性需要在更广泛的情感评估基准上进行验证。

4. **实时推理优化**：若要将该方法推向实际交互系统，需探索扩散模型的加速采样策略（如 DDIM、渐进蒸馏）或轻量化架构设计，在保持生成质量的前提下降低推理延迟。



## 原文 PDF

![[paperPDFs/PG_2025/EmoDiffGes_Emotion_Aware_Co_Speech_Holistic_Gesture_Generation_with_Progressive_Synergistic_Diffusion.pdf]]
