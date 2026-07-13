---
title: "TEXT2INTERACT: HIGH-FIDELITY AND DIVERSE TWO-PERSON INTERACTION GENERATION FROM TEXT"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Text2Interact_High_Fidelity_and_Diverse_Text_to_Two_Person_Interaction_Generation.pdf
project_link: null
code_link: null
aliases:
- TII
- TEXT2INTERACT
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过可扩展的数据合成管道（InterCompose）生成多样化合成数据扩充训练集，并引入词级条件化（word-level conditioning）与自适应交互损失来增强文本对齐与物理合理性。
primary_logic: 将双人交互生成分解为单人类别的条件组合：利用LLM和单人类别先验生成新颖交互样本，并通过词级注意力及距离加权的交互损失实现精细的文本-运动一致性。
claims:
- InterActor 使用词级条件化（word-level conditioning）在 InterHuman 测试集上取得最佳 R-Precision Top-1（0.483），显著优于先前最佳 InterMask（0.449）。
- 自适应交互损失（Adaptive Interaction Loss）加权近距离关节对，提高了文本-运动匹配与物理合理性。
- InterCompose 数据合成管道生成的合成数据经过过滤后，微调 InterActor 进一步提升了 FID（从 5.701 到 5.191）并保持了 R-Precision。
- 用户研究（51 名参与者）表明微调后的模型在分布外文本上显著优于未微调模型，验证了合成数据的泛化性。
---

# TEXT2INTERACT: HIGH-FIDELITY AND DIVERSE TWO-PERSON INTERACTION GENERATION FROM TEXT

> [!tip] 核心洞察
> 将双人交互生成分解为单人类别的条件组合：利用LLM和单人类别先验生成新颖交互样本，并通过词级注意力及距离加权的交互损失实现精细的文本-运动一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Text2Interact：从文本生成高保真多样化双人交互 |
| 英文题名 | TEXT2INTERACT: HIGH-FIDELITY AND DIVERSE TWO-PERSON INTERACTION GENERATION FROM TEXT |
| 会议/期刊 | arXiv 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Text2Interact（包含 InterCompose 和 InterActor） |
| Dataset | InterHuman test |

> [!tip] 效果简介
> - InterHuman test 上，R-Precision Top-1 0.483 vs 0.449 (InterMask) (+0.034)；R-Precision Top-2 0.638 vs 0.599 (InterMask) (+0.039)；R-Precision Top-3 0.717 vs 0.683 (InterMask) (+0.034)。

## 概要

从文本生成双人交互运动是计算机视觉与图形学中的核心挑战，其瓶颈在于**训练数据稀缺**与**文本条件化粗糙**。现有双人运动数据集（如 InterHuman）规模有限，难以覆盖真实世界中多样化的交互模式；同时，主流方法将长文本压缩为单个句嵌入，丢失了词级时空线索（如“先握手，再拥抱”的时序顺序），导致生成的运动与文本语义脱节。

针对上述问题，本文提出 **Text2Interact** 框架，包含两个互补组件：

- **InterCompose**：一个可扩展的合成-过滤管道，利用大语言模型（LLM）生成多样化的双人交互描述，并结合强单人类别先验（MoMask）生成合成运动数据，经神经评估器过滤后扩充训练集。
- **InterActor**：一个词级条件化的双人交互生成模型，通过词级交叉注意力保留文本中的细粒度语义线索，并引入**自适应交互损失**（反比于关节距离加权），强化近距离交互关节对的物理合理性。

在 InterHuman 测试集上，InterActor 取得了最优的文本-运动匹配精度（R-Precision Top-1 达 0.483，较先前最佳 InterMask 提升 3.4 个百分点）。合成数据微调进一步将 FID 从 5.701 降至 5.191，51 人用户研究证实其在分布外文本上的泛化优势。消融实验表明，移除词级条件化、自适应交互损失或合成数据微调均导致性能显著退化，验证了各组件的独立贡献。



### 问题定义与核心挑战

从文本生成双人交互运动（text-to-interaction generation）要求同时合成两个角色的运动序列，且运动必须满足三个条件：语义上与输入文本对齐、时间上同步协调、空间上物理合理（例如握手时手部应紧密接触）。该任务可形式化为：给定文本提示 $\boldsymbol{x} = (x_1, \dots, x_T)$，生成双人运动序列 $\mathbf{X} = [\mathbf{x}_1, \mathbf{x}_2] \in \mathbb{R}^{2 \times T \times N \times 3}$，其中每个角色在每帧的运动状态表示为 $\mathbf{x}_i^{(t)} = [\mathbf{j}_g^p, \mathbf{j}_g^v, \mathbf{j}^r, \mathbf{c}_f]$，分别对应全局关节位置、速度、局部旋转和脚部接触标签。

现有方法面临两个根本性瓶颈，制约了生成质量与泛化能力：

1. **训练数据稀缺且覆盖不足**：双人交互运动捕捉成本极高，现有最大数据集 InterHuman（Liang et al., IJCV 2024）虽包含约 6000 个样本，但交互类型和动作组合的多样性仍远不足以覆盖真实世界中丰富的交互模式。这导致模型在分布外文本上泛化能力薄弱。

2. **文本条件化粒度粗糙**：主流方法（如 InterGen、InterMask）将整句交互描述压缩为单一向量嵌入，通过 AdaLN 或句子级交叉注意力注入运动生成器。这种压缩丢失了词级别的时空线索——例如“A 先推 B，然后 B 后退”中的动作顺序、角色分配和接触时序信息无法被精细地传递到对应的运动帧。

### 现有方法谱系与缺口

双人交互生成领域的方法可归纳为以下几条技术路线：

- **单人类别模型适配**：将成熟的单人文本-运动模型（如 **T2M** (Guo et al., 2022)、**MDM** (Tevet et al., 2022)）直接扩展为双人输出，但缺乏角色间依赖建模，常产生不协调的运动。

- **组合式生成**：**ComMDM** (Shafir et al., 2023) 通过分别生成单人运动再组合的方式处理交互，但组合过程缺乏全局一致性约束；**RIG** (Tanaka & Fujiwara, 2023) 引入角色感知，但角色间信息交换有限。

- **专用交互模型**：**InterGen** (Liang et al., IJCV 2024) 提出双人扩散模型，使用平坦权重的距离图损失约束交互区域，但条件化仍为句子级；**InterMask** (Javed et al., 2024) 采用掩码 Transformer 架构，在 InterHuman 测试集上取得先前最优 R-Precision Top-1 0.449，代表了本工作最强的基线。

- **检索增强方法**：**MoMat-MoGen** (Cai et al., 2024) 通过检索相似样本来辅助生成，但受限于检索库的覆盖范围；**in2IN** (Ruiz-Ponce et al., 2024) 使用角色独立描述，但未充分利用交互上下文的词级信息。

上述方法的共同缺口在于：**文本条件化停留在句子级语义，无法利用词级时空线索；训练数据依赖单一真实数据集，缺乏可扩展的合成策略来系统性地扩充交互多样性。**

### 本文动机与核心思路

针对上述瓶颈，Text2Interact 提出两个互补组件：

- **InterCompose**：一个可扩展的“合成-过滤”数据管道。利用 LLM 生成多样化的交互文本描述，结合强单人类别运动先验（MoMask）通过反应生成扩散模型合成第二人运动，再经神经运动评估器过滤低质样本。这从根本上缓解了训练数据稀缺问题。

- **InterActor**：一个词级条件化的双人交互生成模型。通过词级交叉注意力将 CLIP 词 token 直接注入运动 token，保留发起、响应、接触顺序等细粒度线索；同时引入自适应交互损失——以真实关节距离的倒数加权距离误差（$\mathcal{L}_{\mathrm{AdaInteract}} = \sum_{i=1}^{N} \sum_{j=1}^{N} \frac{1}{d_{ij} + \epsilon} \| d_{ij} - \hat{d}_{ij} \|_2$），使模型更关注近距离交互关节对的物理合理性，而非对所有关节对等权重惩罚。

这一“数据扩充 + 精细条件化”的组合策略，将双人交互生成从句子级语义匹配推进到词级时空对齐，同时通过合成数据微调显著提升了分布外泛化能力。



## 核心方法与创新机理

Text2Interact 的核心创新在于将双人交互生成分解为两个可控的因果杠杆：**数据侧**通过可扩展的合成-过滤管道（InterCompose）突破训练数据瓶颈，**模型侧**通过词级条件化与自适应交互损失实现精细的文本-运动对齐。以下从四个 changed slots 展开分析。

### 1. 文本条件化粒度：从句级到词级

现有方法（如 InterGen、InterMask）普遍采用**句级嵌入**（sentence-level embedding）作为条件信号，通过 AdaLN 或句级交叉注意力将整个文本描述压缩为单一向量注入模型。这一做法丢失了词级的时空线索——例如“先握手、再拥抱”中的顺序语义无法被有效保留。

InterActor 改用**词级交叉注意力**（word-level cross-attention），使每个运动 token 能够直接关注所有 CLIP 词 token。具体而言，模型在每个生成块中引入词级条件化模块（Word-Level Conditioning Block），将文本特征作为 Key-Value 对，运动 token 作为 Query，通过标准缩放点积注意力实现细粒度信息注入：

$$\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

这一设计使得模型能够保留“发起-响应-接触顺序”等 token 级线索，是 R-Precision Top-1 从 InterMask 的 0.449 提升至 0.483（+0.034）的关键因素。消融实验（Table 3）证实，移除词级条件化（WLC）后所有 R-Precision 指标均显著下降，FID 恶化。

### 2. 交互损失：从平坦权重到自适应加权

双人交互的物理合理性高度依赖近距离关节对的精确建模（如握手时的手部关节）。先前工作（如 InterGen）使用**平坦距离图损失**（uniform distance map loss），对所有关节对赋予相同权重，导致远距离关节对的噪声主导训练信号，而关键交互区域被稀释。

InterActor 提出**自适应交互损失**（Adaptive Interaction Loss），以真实关节距离的倒数作为权重：

$$\mathcal{L}_{\mathrm{AdaInteract}} = \sum_{i=1}^{N} \sum_{j=1}^{N} \frac{1}{d_{ij} + \epsilon} \| d_{ij} - \hat{d}_{ij} \|_2$$

其中 $d_{ij}$ 为真实关节对距离，$\hat{d}_{ij}$ 为预测距离，$\epsilon$ 防止除零。该设计使近距离交互关节对获得更高权重，强制模型优先学习接触区域的精确几何关系。消融实验（Table 3）显示，将 AIL 替换为平坦距离损失后 FID 上升约 0.32，验证了自适应加权对运动质量的关键作用。

### 3. 训练数据：从单一数据集到合成增强

InterHuman 数据集虽为双人交互生成提供了重要基准，但其规模和多样性有限，难以覆盖长尾交互模式。Text2Interact 通过 **InterCompose 合成管道**进行数据扩充：

1. **LLM 驱动的描述合成**：利用 LLM 在主题-标签联合空间中采样多样化的交互描述，并将其分解为两个角色特定的子描述。
2. **单人类别先验组合**：从单人运动先验（MoMask）生成第一人运动，再通过反应生成扩散模型以交互文本和第一人运动为条件生成第二人运动。
3. **双阶段过滤**：神经运动评估器过滤语义不对齐样本（余弦相似度阈值 0.58），分布过滤保留与真实数据嵌入距离在预设环带内的样本，确保合成数据的语义保真度和分布多样性。

经过滤的合成数据微调 InterActor 后，FID 从 5.701 降至 5.191（Table 2），同时保持 R-Precision 水平。用户研究（Figure 5，51 名参与者）进一步表明微调模型在分布外文本上显著优于未微调模型，验证了合成数据的泛化价值。

### 4. 架构模块：从单角色处理到角色间交互建模

基线方法通常独立处理两个角色的运动，缺乏显式的角色间依赖建模。InterActor 采用**交替的词级条件化模块 + 运动-运动交互模块**（Figure 2(b)）：

- **词级条件化模块**：运动 token 通过交叉注意力关注文本词 token。
- **运动-运动交互模块**：包含自注意力（建模单人运动时序依赖）和角色间交叉注意力（建模双人动态依赖），使两个角色的运动生成过程相互感知。

这一架构设计使模型能够同时捕捉单人运动的内在连贯性和双人交互的时空协调性。虽然该 changed slot 的消融证据在独立移除项中未单独报告，但“移除所有提出组件”（w.o. All）的 FID 高达 6.237（Table 3），远差于完整模型的 5.191，间接支持了该模块的贡献。

### 创新总结

Text2Interact 的四项 changed slots 形成互补闭环：InterCompose 提供规模化的训练数据，词级条件化捕获细粒度文本语义，自适应交互损失强化物理合理性，交替架构实现角色间协调。三者协同使模型在 R-Precision 三项指标上全面超越 InterMask（Table 1），同时保持有竞争力的 FID（5.191 vs 5.154，差距在置信区间内）。



Text2Interact 由两个协同工作的核心组件构成：**InterCompose**（可扩展的合成数据管道）与 **InterActor**（词级条件化的双人交互生成模型）。两者形成“数据增强—精细生成”的闭环——InterCompose 为 InterActor 提供高质量、多样化的合成训练样本，InterActor 则通过细粒度文本条件化和自适应交互损失实现语义忠实且物理合理的双人运动生成。

### 系统输入与输出

系统的输入为一段描述双人交互的自然语言文本 $c_t$（例如“一个人挥拳，另一个人向后闪避”）。输出为两个角色的三维运动序列 $\mathbf{X} = [\mathbf{x}_1, \mathbf{x}_2] \in \mathbb{R}^{2 \times T \times N \times 3}$，其中 $T$ 为帧数，$N$ 为每人的关节数。每个角色在时刻 $t$ 的运动状态表示为 $\mathbf{x}_i^{(t)} = [\mathbf{j}_g^p, \mathbf{j}_g^v, \mathbf{j}^r, \mathbf{c}_f]$，分别对应全局关节位置、速度、局部旋转和脚部接触标签。

### InterCompose：合成数据管道

InterCompose 采用“合成-过滤”策略（synthesis-by-composition），通过组合 LLM 文本先验与单人类别运动先验来构造多样化的双人交互样本。其流程如 Figure 2(a) 所示，包含四个串联模块：

![[assets/figures/papers/paper_list_l1696_Text2Interact_High_Fidelity_and_Diverse_Text_to_Two_Person_Interaction_G/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed frameworks. (a) InterCompose: sample interaction and singleperson descriptions via an LLM, generate a single-person motion from a motion prior (Guo et al., 2024), then compose the second agent with a reaction model conditioned on the two-person prompt and the motion prior. (b) InterActor: an N-block generator with word-level conditioning and motion–motion interaction. Each block cross-attends motion tokens to CLIP word tokens (Radford et al., 2021), followed by self-attention and inter-agent cross-attention to model individual motion and interactions*

1. **LLM 交互描述合成**：首先用 LLM 对 InterHuman 数据集的文本进行标注，将其归类到粗粒度主题（theme）与细粒度标签（tag）的离散空间中；随后在该联合空间中采样，生成新颖的交互文本 $c_t$。
2. **单人运动生成**：将交互文本分解为两个角色特定的子描述 $(c_t^1, c_t^2)$，利用预训练的单人运动生成模型（MoMask）从 $c_t^1$ 生成第一人的运动 $\mathbf{x}_1$。
3. **反应生成扩散模型**：以第一人运动 $\mathbf{x}_1$ 和交互文本 $c_t$ 为条件，通过条件扩散模型 $p_\theta(\mathbf{x}_2 \mid \mathbf{x}_1, c_t)$ 生成第二人的反应运动 $\mathbf{x}_2$。
4. **神经运动评估与过滤**：采用双阶段过滤框架确保合成数据的语义保真度和分布多样性——语义过滤通过神经评估器计算文本-运动对齐分数并剔除低分样本；分布过滤则保留与真实数据嵌入距离落在预设环形区间 $[r_{\min}, r_{\max}]$ 内的样本，避免分布偏移与冗余。

### InterActor：词级条件化生成模型

InterActor 是一个基于扩散的双人交互生成模型，其核心架构如 Figure 2(b) 所示，由 $N$ 个交替排列的模块块构成：

- **词级条件化模块（Word-Level Conditioning Block）**：每个运动 token 通过交叉注意力（cross-attention）直接关注 CLIP 编码的所有词 token，而非将整句压缩为单一嵌入。这保留了“发起—响应—接触顺序”等 token 级别的时空线索。
- **运动-运动交互模块（Motion-Motion Interaction Block）**：包含自注意力（self-attention）和角色间交叉注意力（inter-agent cross-attention），分别建模单人内部运动动力学和双人之间的动态依赖关系。
- **自适应交互损失（Adaptive Interaction Loss）**：在训练时监督双人关节对之间的成对距离，权重与真实关节距离成反比：

$$\mathcal{L}_{\mathrm{AdaInteract}} = \sum_{i=1}^{N} \sum_{j=1}^{N} \frac{1}{d_{ij} + \epsilon} \| d_{ij} - \hat{d}_{ij} \|_2$$

该损失强调近距离交互关节对（如握手、拥抱时的接触区域），弱化远距离关节对的误差，从而在保持整体运动质量的同时提升物理合理性。

### 训练与微调流程

InterActor 首先在 InterHuman 数据集上从零训练（200,000 步，8 块 A100 GPU，学习率 $5\times10^{-5}$，批次大小 16，AdamW 优化器，余弦学习率调度，1,000 步预热，扩散步数 1,000，余弦噪声调度）。随后，使用经 InterCompose 合成并通过双阶段过滤的高质量样本进行微调，进一步降低 FID（从 5.701 降至 5.191）并保持 R-Precision，同时显著提升在分布外文本上的泛化能力（51 人用户研究验证）。



Text2Interact 框架由两个核心组件构成：**InterCompose**（可扩展的合成数据管道）与 **InterActor**（词级条件化的双人交互生成器）。以下重点拆解 InterActor 的关键模块与核心公式。

---

### 问题形式化

双人交互序列表示为 $\mathbf{X} = [\mathbf{x}_1, \mathbf{x}_2] \in \mathbb{R}^{2 \times T \times N \times 3}$，其中 $T$ 为帧数，$N$ 为每人的关节数。在时刻 $t$，第 $i$ 人的运动状态为：

$$\mathbf{x}_i^{(t)} = [\mathbf{j}_g^p, \mathbf{j}_g^v, \mathbf{j}^r, \mathbf{c}_f]$$

各分量含义：
- $\mathbf{j}_g^p$：全局关节位置
- $\mathbf{j}_g^v$：全局关节速度
- $\mathbf{j}^r$：局部关节旋转
- $\mathbf{c}_f$：脚部与地面接触标志

---

### 词级条件化模块（Word-Level Conditioning Block）

**设计动机**：现有方法（如 InterGen、InterMask）将整句文本压缩为单个句嵌入，通过 AdaLN 或句级交叉注意力注入运动生成过程，丢失了“发起-响应-接触顺序”等词级时空线索。

**核心机制**：InterActor 使用交叉注意力，令每个运动 token 直接关注 CLIP 文本编码器的所有词 token。给定文本提示 $\boldsymbol{x} = (x_1, \dots, x_T)$，CLIP 编码得到词级特征序列，运动 token 通过标准缩放点积注意力与之交互：

$$\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

其中 $Q$ 来自运动 token，$K, V$ 来自词 token。这使得模型能够选择性地关注与当前生成帧相关的词（如“推”、“左臂”、“缓慢”），实现精细的文本-运动对齐。

**架构位置**：词级条件化模块与运动-运动交互模块交替堆叠 $N$ 块（见 Figure 2(b)）。每块先执行词级交叉注意力，再依次执行单人自注意力（建模个体运动）和双人交叉注意力（建模交互动态）。

---

### 自适应交互损失（Adaptive Interaction Loss）

**设计动机**：双人交互的关键在于近距离关节对（如手-手、手-躯干）的时空协调。传统方法（如 InterGen 的 $\mathcal{L}_{DM}$）使用平坦权重距离图损失，对远距离关节对（如两人各自左脚）施加同等监督，稀释了对交互关键区域的关注。

**公式**：自适应交互损失对每对跨人关节的距离误差赋予反比于真实距离的权重：

$$\mathcal{L}_{\mathrm{AdaInteract}} = \sum_{i=1}^{N} \sum_{j=1}^{N} \frac{1}{d_{ij} + \epsilon} \| d_{ij} - \hat{d}_{ij} \|_2$$

变量含义：
- $d_{ij}$：真实运动中第 $i$ 个关节与第 $j$ 个关节的欧氏距离
- $\hat{d}_{ij}$：生成运动中的对应距离
- $\epsilon$：防止除零的小常数
- $N$：每人的关节数

**因果机制**：权重 $\frac{1}{d_{ij} + \epsilon}$ 使得距离越近的关节对损失贡献越大，迫使模型优先学习接触与近距交互的精确几何关系，同时不忽略远距离关节对的结构一致性。

**消融证据**：Table 3 显示，移除自适应交互损失、改用平坦距离损失后，FID 上升约 0.32，R-Precision 各项均下降，证实了自适应加权对物理合理性与文本对齐的双重增益。

---

### 合成数据管道（InterCompose）的关键模块

InterCompose 并非单一公式，而是一个多阶段管道，其核心模块包括：

1. **LLM 交互描述合成**：利用大语言模型在“主题-标签”联合空间中采样生成多样化的双人交互文本，并分解为两个角色特定的子描述。
2. **单人类别先验生成**：使用预训练的单人运动模型（MoMask）从角色描述生成第一人运动。
3. **反应生成扩散模型**：以第一人运动和交互文本为条件，通过条件扩散模型 $p_{\theta}(\mathbf{x}_2 \mid \mathbf{x}_1, c_t)$ 生成第二人运动。
4. **神经运动评估器与双阶段过滤**：语义过滤（余弦相似度阈值 0.58）剔除文本-运动不对齐样本；分布过滤（基于 $k$ 近邻距离环 $r_{\min} \leq d(f_{\phi}(\mathbf{x}), \mathcal{E}_{\mathrm{real}}) \leq r_{\max}$）确保合成数据在真实数据分布的合理邻域内，避免分布外噪声。

---

### 模块间的因果链条

词级条件化解决**文本-运动对齐的粒度瓶颈**，自适应交互损失解决**交互物理合理性的监督稀疏问题**，InterCompose 合成数据解决**训练数据覆盖不足**。三者协同：词级注意力使模型能利用合成数据中的细粒度文本线索，自适应损失则确保合成样本中的新颖交互模式得到恰当的几何监督。消融实验（Table 3）证实，移除任一组件均导致性能显著退化，三者叠加效果最优。

### 补充图表

![[assets/figures/papers/paper_list_l1696_Text2Interact_High_Fidelity_and_Diverse_Text_to_Two_Person_Interaction_G/figures/010_Figure_7.jpg]]
*Figure 7: Illustration of the Word-Level Conditioning Block*

![[assets/figures/papers/paper_list_l1696_Text2Interact_High_Fidelity_and_Diverse_Text_to_Two_Person_Interaction_G/figures/011_Figure_8.jpg]]
*Figure 8: Illustration of the Self-Attention module in the Motion-Motion Interaction Block*



## 实验与关键发现

### 主实验：InterHuman 测试集上的文本-运动对齐与生成质量

Table 1 报告了 InterActor 与现有方法在 InterHuman 测试集上的定量对比。InterActor 在所有三个 R-Precision 指标上均取得最优结果：Top-1 达到 0.483，领先最强基线 **InterMask**（Javed et al., 2024）0.034；Top-2 为 0.638（+0.039）；Top-3 为 0.717（+0.034）。这一致性优势表明词级条件化（word-level conditioning）有效保留了文本中的细粒度时空线索，使生成的运动序列与输入描述在语义层面更加匹配。

![[assets/figures/papers/paper_list_l1696_Text2Interact_High_Fidelity_and_Diverse_Text_to_Two_Person_Interaction_G/figures/003_Table_1.jpg]]
*Table 1: Performance on the InterHuman (Liang et al., 2024) test sets. ± indicates a 95% confidence interval and → means the closer to ground truth the better. Boldface indicates the best result*

在运动质量方面，InterActor 的 MM Distance 为 3.778，略优于 InterMask 的 3.790，说明生成的运动分布与真实数据分布更为接近。FID 指标上，InterActor 取得 5.191，与 InterMask 的 5.154 差距仅为 0.037，落在 95% 置信区间内，二者在运动自然度上基本持平。

值得注意的是，此前基于组合的方法（**ComMDM**、**RIG**）和检索增强方法（**MoMat-MoGen**）在 R-Precision 上表现明显落后，反映出粗糙的句级条件化或检索拼接策略难以捕捉双人交互中“谁发起、谁响应、接触顺序”等词级语义。定性对比（Figure 3）进一步显示，InterActor 生成的交互序列在文本-运动对齐和姿态合理性上均优于 InterMask，尤其在不常见交互动作上表现出更强的鲁棒性。

### 合成数据微调的增益

Table 2 展示了在 InterCompose 生成的合成数据上微调后的效果。经过双阶段过滤（语义过滤 + 分布多样性过滤）的合成数据使 FID 从 5.701 降至 5.191，同时 R-Precision 保持稳定。这表明合成数据在提升运动质量的同时未损害文本对齐能力——过滤机制有效去除了语义不一致或分布外样本，避免了“数据污染”导致的退化。

![[assets/figures/papers/paper_list_l1696_Text2Interact_High_Fidelity_and_Diverse_Text_to_Two_Person_Interaction_G/figures/005_Table_2.jpg]]
*Table 2: Quantitative Results of InterActor after fine-tuning on synthetic data generated by InterCompose. d denotes the Euclidean distance between a synthetic data sample point and its closest held-out data point in the embedding space of the neural evaluator*

用户研究（Figure 5，51 名参与者）为合成数据的泛化价值提供了主观证据：微调后的模型在分布外文本上的生成结果被显著更频繁地偏好，验证了 InterCompose 合成的多样化交互模式确实扩展了模型的泛化边界。

![[assets/figures/papers/paper_list_l1696_Text2Interact_High_Fidelity_and_Diverse_Text_to_Two_Person_Interaction_G/figures/009_Figure_5.jpg]]
*Figure 5: User preference study results of InterActor with and without fine-tuning on synthetic data*

### 消融实验：各组件的因果贡献

Table 3 的消融实验量化了三个核心组件的独立贡献：

- **移除词级条件化（w/o WLC）**：所有 R-Precision 指标下降，FID 恶化。这直接验证了词级交叉注意力（而非句嵌入）是文本-运动精细对齐的关键因果旋钮。
- **移除自适应交互损失（w/o AIL）**：改用 InterGen 的平坦距离图损失后，FID 上升约 0.32。自适应权重 $1/(d_{ij}+\epsilon)$ 使模型在训练时更关注近距离关节对的几何一致性，这对握手、拥抱等接触密集型交互尤为重要。
- **移除合成数据微调（w/o FT）**：FID 从 5.191 升至 5.701，证实 InterCompose 数据扩充对运动质量的贡献。
- **移除所有组件（w/o All）**：FID 升至 6.237，与完整模型差距显著，排除了各组件间存在冗余替代的可能性。

### 失败模式与局限

尽管 InterActor 在文本对齐指标上表现突出，但论文未系统报告失败案例。从定性样本和架构设计可推断以下潜在问题：

1. **物理伪影**：模型未显式建模物理约束（如接触力、地面支撑），可能产生漂浮、穿地等伪影。论文在开放问题中也提及需要融入物理先验。
2. **长时序一致性**：扩散模型在较长运动序列上可能出现漂移，交互动作的起止边界可能模糊。
3. **数据偏见放大**：CLIP 文本编码器和 LLM 合成描述可能携带文化或性别刻板印象，导致生成的运动模式存在偏见分布。

### 关键图表结论速览

- **Table 1**：InterActor 在 R-Precision Top-1/2/3 上全面超越所有基线，词级条件化是文本对齐优势的主要来源。
- **Table 2**：过滤后的合成数据微调使 FID 降低 0.51，且不牺牲 R-Precision。
- **Figure 5**：用户研究验证了合成数据微调在分布外文本上的泛化收益。
- **Table 3**：消融实验确认词级条件化、自适应交互损失和合成数据微调三者均为性能的关键支撑，缺一不可。

### 补充图表

![[assets/figures/papers/paper_list_l1696_Text2Interact_High_Fidelity_and_Diverse_Text_to_Two_Person_Interaction_G/figures/007_Figure_6.jpg]]
*Figure 6: Comparison of motion generation results using InterCompose and InterActor, (a) without filtering, and (b) with filtering. The motion quality and text-motion matching of InterCompose surpass InterActor only after filtering. s*



## 定位与知识库关联

### 1. 核心瓶颈与因果杠杆

Text2Interact 旨在解决双人交互运动生成中的两个结构性问题：

- **数据瓶颈**：现有双人运动数据集（如 InterHuman）规模有限，难以覆盖长尾交互模式。单靠真实数据训练，模型泛化能力受限于标注样本的多样性。
- **条件化粗糙**：主流方法将整句文本压缩为单一嵌入（sentence-level embedding），通过 AdaLN 或 sentence cross-attention 注入运动生成器，丢失了词级的时空线索（如“先推后拉”的动作顺序）。

针对上述瓶颈，Text2Interact 引入两个因果杠杆：

1. **可扩展的数据合成管道 InterCompose**：通过 LLM 生成多样化交互描述，结合强单人类别先验（MoMask）合成双人运动，再经神经评估器过滤，产出高质量合成数据以扩充训练集。
2. **词级条件化与自适应交互损失**：InterActor 采用 word-level cross-attention 替代句级条件化，保留 token 级语义线索；同时引入距离加权的自适应交互损失（Adaptive Interaction Loss），强化近距离关节对的运动一致性。

### 2. 在双人交互生成谱系中的定位

Text2Interact 处于**文本驱动的双人交互运动生成**这一细分方向，其方法谱系可从条件化粒度、数据来源、交互建模三个维度梳理。

#### 2.1 从单人到双人的扩散模型演进

早期文本驱动运动生成聚焦单人场景。**T2M**（Guo et al., 2022）和 **MDM**（Tevet et al., 2022）分别建立了基于 VAE 和扩散模型的单人运动生成范式，使用句级嵌入作为条件。将这些方法直接扩展到双人场景时，面临角色分配模糊和交互建模不足的问题。

**ComMDM**（Shafir et al., 2023）通过组合单人扩散模型实现双人交互，但缺乏端到端的交互一致性约束。**RIG**（Tanaka & Fujiwara, 2023）引入角色感知的条件化，区分双人文本中的不同主体，但仍依赖句级嵌入。

#### 2.2 专用双人交互模型的进展

**InterGen**（Liang et al., IJCV 2024）是首个面向双人交互的扩散模型，提出平坦权重的距离图损失（uniform distance map loss）来监督双人关节距离，但在文本条件化上仍沿用句级嵌入。**InterMask**（Javed et al., 2024）采用 masked transformer 架构，在 InterHuman 测试集上取得了先前的 SOTA（R-Precision Top-1 为 0.449），是 Text2Interact 的最强基线。

**MoMat-MoGen**（Cai et al., 2024）引入检索增强机制，从数据库中检索相似交互作为生成先验。**in2IN**（Ruiz-Ponce et al., 2024）使用个体描述分别条件化两个角色，但未显式建模角色间动态依赖。

Text2Interact 在以下关键维度上区别于上述工作：

| 维度 | 先前方法 | Text2Interact (InterActor) |
|------|----------|---------------------------|
| 文本条件化 | 句级嵌入（InterGen, InterMask） | 词级交叉注意力（word-level cross-attention） |
| 交互损失 | 平坦距离图损失（InterGen） | 自适应交互损失（距离反比加权，Eq. 1） |
| 训练数据 | 仅 InterHuman | InterHuman + InterCompose 合成数据微调 |
| 角色间建模 | 无显式交叉注意力（InterMask） | 交替的词级条件化模块 + motion-motion interaction 模块（自注意力+交叉注意力） |

#### 2.3 数据合成范式的创新

InterCompose 的数据合成策略在方法论上区别于简单的数据增强。其核心在于**分解-组合**（synthesis-by-composition）：

- 利用 LLM 在 theme-tag 联合空间中采样交互描述，保证语义多样性；
- 将交互文本分解为两个角色特定的子描述，分别驱动单人类别先验和反应生成扩散模型；
- 通过神经评估器进行语义保真度过滤（余弦相似度阈值 0.58）和分布多样性过滤（保留与真实数据嵌入距离在预设环带内的样本），确保合成数据的质量和分布合理性。

这一范式将双人交互生成问题分解为单人类别的条件组合，降低了对昂贵双人标注数据的依赖。

### 3. 适用边界与局限

#### 3.1 适用场景

- **文本条件明确的双人交互**：适用于描述清晰、包含角色区分和动作顺序的文本提示。
- **数据稀缺的交互类别**：InterCompose 可合成训练集中未见的交互模式，提升长尾泛化能力（用户研究证实微调模型在分布外文本上显著优于未微调模型，Figure 5）。
- **需要精细文本对齐的场景**：词级条件化保留了 token 级线索，适合对动作顺序和接触时序敏感的应用。

#### 3.2 已知局限

1. **物理合理性不足**：论文明确指出存在漂浮和穿地等伪影，缺乏显式物理先验（如接触力、地面约束）的融入。这是一个开放性挑战。
2. **合成数据依赖 LLM 质量**：InterCompose 的多样性受限于 LLM 的生成能力和偏见，可能产生刻板印象化的行为描述。
3. **CLIP 文本编码器的偏见**：使用 CLIP 编码文本可能放大训练数据中的文化或语言偏见。
4. **FID 指标未取得最优**：在 InterHuman 测试集上，InterActor 的 FID 为 5.191，略逊于 InterMask 的 5.154（差距在 95% 置信区间内），表明运动质量仍有提升空间。
5. **仅支持两人交互**：方法设计针对双人场景，扩展到多人交互需要重新设计角色分配和交互建模机制。

### 4. 开放问题与后续方向

1. **物理先验的融入**：如何将物理仿真或接触约束集成到扩散生成过程中，以减少漂浮、穿地等伪影？这可能需要与物理引擎联合优化或引入可微物理损失。
2. **从视频学习运动**：InterCompose 目前依赖单人类别先验和 LLM 文本合成，如何直接从视频数据学习交互运动，绕过文本中间表示，是一个重要的扩展方向。
3. **多人交互扩展**：将框架从双人推广到多人场景，需要解决角色数量可变、交互图结构建模等新挑战。
4. **实时交互生成**：当前扩散模型需要 1000 步去噪，推理速度有限。如何结合蒸馏或一致性模型实现实时交互运动生成，是实际部署的关键问题。
5. **细粒度交互控制**：词级条件化已提供了一定程度的细粒度控制，但如何实现关节级或接触点级的精确空间约束，仍是一个开放方向。



## 原文 PDF

![[paperPDFs/arxiv_2025/Text2Interact_High_Fidelity_and_Diverse_Text_to_Two_Person_Interaction_Generation.pdf]]
