---
title: "InterEdit: Navigating Text-Guided Multi-Human 3D Motion Editing"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/InterEdit_Navigating_Text_Guided_Multi_Human_3D_Motion_Editing.pdf
project_link: null
code_link: https://github.com/YNG916/InterEdit
aliases:
- InterEdit
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 在同步分类器引导的扩散模型中引入两个互补的控制信号：语义感知计划令牌对齐（Semantic-Aware Plan Token Alignment）为扩散过程注入高层编辑意图，确保编辑内容遵循文本指令；交互感知频率令牌对齐（Interaction-Aware Frequency Token Alignment）通过DCT频带能量正则化保持交互节奏、同步性和空...
primary_logic: 将多人物动作编辑解耦为语义意图引导与交互频率正则化，使扩散模型能在保持源动作未编辑部分不变的前提下，精确执行语义修改，同时强制维持人际时空耦合的连续性，避免因局部编辑引发交互失真。
claims:
- InterEdit在所有度量上超越单人物编辑和多人物生成基线，在g2t retrieval R@1上比最强基线TIMotion提升5.85个百分点，FID降低16.7%。
- 消融实验表明，同时使用计划令牌和频率令牌达到最佳g2t retrieval R@3 (47.65±0.59)，单独使用任一模块均会下降，证明二者在语义引导和交互正则化上互补。
- 适中的频率令牌dropout率 (0.04) 在避免过拟合与保留交互正则化之间取得最佳平衡，过高或过低的dropout均会损害检索或FID。
- 人类偏好研究中，InterEdit在指令遵循（win rate 78.5%）和交互真实性（81.0%）两个维度上对TIMotion具有压倒性优势，主观验证了语义令牌对齐和频率令牌对齐的实际效果。
---

# InterEdit: Navigating Text-Guided Multi-Human 3D Motion Editing

> [!tip] 核心洞察
> 将多人物动作编辑解耦为语义意图引导与交互频率正则化，使扩散模型能在保持源动作未编辑部分不变的前提下，精确执行语义修改，同时强制维持人际时空耦合的连续性，避免因局部编辑引发交互失真。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterEdit：面向文本引导的多人物3D动作编辑 |
| 英文题名 | InterEdit: Navigating Text-Guided Multi-Human 3D Motion Editing |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.13082) · [Code](https://github.com/YNG916/InterEdit) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | InterEdit |
| Dataset | InterEdit3D test set |

> [!tip] 效果简介
> - InterEdit3D test set (TMME benchmark) 上，FID↓ 0.3707±0.0029 vs ~0.445 (TIMotion) (-16.7% (相对TIMotion))；generated-to-target retrieval R@1↑ 30.82±0.43 vs 24.97 (TIMotion) (+5.85)；generated-to-source retrieval R@1↑ 17.08±0.41 vs 12.54 (TIMotion) (+4.54)。

## 概要

### 问题背景

文本引导的三维人体动作编辑旨在根据自然语言指令修改已有的单人动作序列。然而，当场景扩展至多人交互时，任务难度发生质变：编辑不仅需要精确执行语义指令，还必须维持人际交互的时空一致性——包括同步节奏、相位对齐、角色切换等复杂协调模式。现有工作或聚焦于单人编辑，或将多人动作生成视为无条件合成，缺乏对“源-目标-指令”三元编辑关系的显式建模。这一瓶颈的根本原因在于：**缺乏配对的多人物编辑数据集**，以及**交互动力学的协调机制难以在编辑过程中得到显式保障**——对单人的局部修改极易破坏整体的交互连贯性。

### 核心方法

**InterEdit** 是一个面向文本引导多人物三维动作编辑（Text-guided Multi-human 3D Motion Editing, TMME）的同步分类器免引导条件扩散模型。其核心设计思想是将多人物动作编辑解耦为两个互补的控制信号：

- **语义感知计划令牌对齐（Semantic-Aware Plan Token Alignment）**：在扩散去噪网络的中间层引入可学习的“计划令牌”，通过InfoNCE损失将其投影对齐到预训练运动教师编码器提取的目标运动语义嵌入，为扩散过程注入高层的编辑意图，确保生成动作遵循文本指令。
- **交互感知频率令牌对齐（Interaction-Aware Frequency Token Alignment）**：构建双人动作的平均与差分交互信号，利用离散余弦变换（DCT）提取频带能量描述符，将其映射为频率控制令牌加入去噪网络，并通过加权L2回归损失正则化交互信号的频率组成，从而显式维持编辑后的交互节奏、同步性和空间耦合。

两个对齐机制作为辅助正则项叠加在扩散重构损失之上，使模型在保持源动作未编辑部分不变的前提下，精确执行语义修改，同时强制维持人际时空耦合的连续性。

### 方法谱系与知识库定位

InterEdit 处于**文本条件扩散生成**与**多人动作建模**的交叉点。其条件扩散骨干继承了Start_X参数化和Transformer去噪架构，与单人物编辑方法（如 **MotionFix**、**MotionLab**）及多人物生成方法（如 **InterGen**、**TIMotion**）共享基础范式。关键差异在于：InterEdit 通过**计划令牌对齐**将编辑任务从隐式条件生成提升为显式语义引导，通过**频率令牌对齐**将交互一致性从生成模型的隐式学习转化为可优化的正则化目标。这一“语义引导 + 频率正则化”的双控架构，使得InterEdit在方法论上区别于单纯的条件生成或数据驱动隐式建模，为多人物动作编辑提供了新的范式。

### 主要结果

在 InterEdit3D 测试集上，InterEdit 在所有评估指标上超越单人物编辑和多人物生成基线：

- **文本-动作一致性**：generated-to-target retrieval R@1 达到 30.82±0.43，比最强基线 TIMotion（24.97）提升 **5.85 个百分点**。
- **源动作保真度**：generated-to-source retrieval R@1 达到 17.08±0.41，比 TIMotion（12.54）提升 **4.54 个百分点**。
- **生成质量**：FID 降至 0.3707±0.0029，相对 TIMotion（~0.445）降低 **16.7%**。

消融实验证实了双控架构的互补性：同时使用计划令牌和频率令牌达到最佳 g2t retrieval R@3（47.65±0.59），单独使用任一模块均会导致指标下降。人类偏好研究进一步验证了主观效果：InterEdit 在指令遵循（win rate **78.5%**）和交互真实性（**81.0%**）两个维度上对 TIMotion 具有压倒性优势。

### 局限与开放问题

InterEdit 当前存在以下局限：（1）对手势的微小变化存在语义歧义，难以可靠区分交互对象；（2）在长时间高动态交互序列中，个体间的空间关系维持仍存在漂移；（3）当前设计仅针对双人交互，未验证对三人及以上场景的泛化能力。这些局限指向若干开放问题：如何通过更细粒度的交互表示消除手势歧义？能否引入显式的空间关系约束以改善长序列一致性？频带能量池化是否足以捕捉非线性交互动态？这些问题为多人物动作编辑的后续研究提供了明确方向。



### 任务定义：文本引导的多人物3D动作编辑

文本引导的多人物3D动作编辑（Text-guided Multi-human 3D Motion Editing, TMME）要求模型在给定源双人动作序列和一条自然语言编辑指令的条件下，生成符合指令语义、同时保持未编辑部分不变的目标双人动作序列。与单人物动作编辑不同，TMME的核心挑战在于**人际交互的时空耦合**——对某一人物动作的局部修改极易破坏双人之间的同步性、相对空间关系和交互节奏，导致编辑后的动作在物理和语义上失去一致性。

### 现有方法的局限

当前该领域的研究主要沿两条路径展开，但均未直接解决TMME的核心瓶颈：

**单人物编辑方法的直接迁移存在根本缺陷。** 将MotionFix或MotionLab等单人物动作编辑模型通过简单拼接双人特征后微调，虽然可以产生编辑效果，但这类方法缺乏对人际交互动力学的显式建模。双人动作的时空同步、相位对齐和角色切换等协调模式无法通过特征拼接隐式习得，导致编辑后交互失真严重。

**多人物生成方法缺乏编辑语义的精确控制。** InterGen和TIMotion等模型通过自适应层归一化（AdaLN）将源运动作为条件注入扩散过程，本质上执行的是“条件生成”而非“编辑”。它们缺少对编辑指令语义的显式对齐机制，难以区分“需要修改的部分”与“必须保留的部分”，容易在生成过程中偏离源动作的未编辑区域。

### 两大核心瓶颈

上述局限可归结为两个相互关联的瓶颈：

1. **语义引导缺失**：扩散模型的条件机制（如AdaLN）仅提供粗粒度的源运动信息，无法将文本指令中的高层编辑意图精确注入去噪过程。模型难以理解“将握手改为石头剪刀布”意味着只修改手部交互动作，而保持身体姿态和空间位置不变。

2. **交互动力学正则化缺失**：双人交互涉及复杂的频率成分——低频的全局位移、中频的肢体协调、高频的足部接触节奏。现有方法完全依赖扩散模型隐式学习这些动力学特征，缺乏显式的正则化信号来约束编辑后的动作保持源动作的交互同步性和节奏一致性。

### 数据集缺口

TMME任务的另一关键障碍是**缺乏配对的多人物源-目标-指令三元数据集**。现有数据集（如InterHuman、Babel等）仅提供单一动作序列或文本描述，不具备源-目标配对和编辑指令标注，无法支持监督学习。这一数据缺口使得TMME长期缺乏标准化的训练和评估基准。

### 本文动机

针对上述瓶颈，本文提出InterEdit框架，核心思路是将多人物动作编辑解耦为两个互补的控制信号：**语义感知计划令牌对齐**为扩散过程注入高层编辑意图，确保编辑内容遵循文本指令；**交互感知频率令牌对齐**通过DCT频带能量正则化保持交互节奏、同步性和空间耦合，使编辑不破坏人际协调。同时，本文构建了InterEdit3D数据集，提供5,161个高质量三元组，为TMME任务建立首个标准化基准。



## 核心方法与创新机理

InterEdit 的核心创新在于将多人物 3D 动作编辑解耦为**语义意图引导**与**交互频率正则化**两个互补维度，使扩散模型能在保持源动作未编辑部分不变的前提下，精确执行语义修改，同时强制维持人际时空耦合的连续性，避免因局部编辑引发交互失真。

### 关键变更槽位

与现有单人物编辑基线（MotionFix、MotionLab）和多人物生成基线（InterGen、TIMotion）相比，InterEdit 在三个关键维度上引入了结构性变更：

**1. 编辑语义引导：从隐式条件到显式计划令牌对齐**

基线方法仅将源运动和文本简单拼接作为条件，缺乏显式的语义对齐机制。InterEdit 引入**语义感知计划令牌对齐**（Semantic-Aware Plan Token Alignment）：在去噪 Transformer 的中间层附加可学习的计划令牌，通过自注意力与动作令牌交互后，利用 InfoNCE 损失将令牌投影拉到预训练运动教师编码器提取的目标语义嵌入附近（Eq. 12–14）。这为扩散过程注入了精确的高层编辑意图，确保编辑内容严格遵循文本指令。消融实验表明，在中间 Transformer 层（L_p=3）施加该损失优于早期或晚期层（Table 5），InfoNCE 作为对齐损失优于余弦相似度和 MSE（Table 6），最佳计划损失权重为 λ_p=0.03（Table 7）。

**2. 交互动力学正则化：从隐式学习到显式频率令牌约束**

现有方法无专门的交互频率约束，双人交互的同步性、节奏和空间耦合仅靠生成模型隐式学习，细微编辑即可能破坏整体交互一致性。InterEdit 提出**交互感知频率令牌对齐**（Interaction-Aware Frequency Token Alignment）：构建双人运动的平均/差分交互信号，利用 DCT 变换并桶化为低、中、高频带能量描述符，将其映射为频率控制令牌加入去噪器，并通过加权 L2 损失回归目标频带能量（Eq. 15–21），显式正则化交互节奏与同步性。适中的频率令牌 dropout 率（p_f=0.04）在避免过拟合与保留正则化之间取得最佳平衡（Table 4）。

**3. 双人动作序列建模：从简单拼接到对称交错令牌聚合**

基线方法直接沿特征维度拼接双人运动，忽视角色对应关系和时间顺序。InterEdit 采用**对称交错令牌聚合**（含角色互换序列）与**局部模式增强分支**（LPA），增强时间顺序建模和短时模式捕捉能力（Eq. 7–9），为后续的语义和频率对齐提供更结构化的表示基础。

### 互补性验证

消融实验（Table 3）强有力地证明了两个对齐机制的互补性：联合使用计划令牌和频率令牌在所有指标上优于单独使用任一模块或两者均不用，g2t retrieval R@3 达到 47.65±0.59，单独使用计划令牌或频率令牌分别下降至 45.81 和 44.69。人类偏好评估（Table 10）进一步验证了主观效果：InterEdit 在指令遵循（win rate 78.5%）和交互真实性（81.0%）两个维度上对最强基线 TIMotion 具有压倒性优势。

### 同步分类器免引导

此外，InterEdit 采用**同步分类器免引导**（Synchronized Classifier-Free Guidance）：训练时同步丢弃源和文本条件以学习无条件分支，推理时插值有条件与无条件预测（Eq. 11），避免条件泄露并提供更干净的引导方向。消融实验（Table 9）证实两分支 SCFG 优于三分支策略。



InterEdit 将多人物 3D 动作编辑形式化为一个条件扩散生成问题。给定一段双人源动作序列 $\mathbf{x}_{1:L}^s$ 和一条文本编辑指令 $\mathbf{y}$，模型的目标是生成一段目标动作 $\mathbf{x}_{1:L}$，使其既精确执行文本指定的语义修改，又保持源动作中未被编辑部分不变，同时维持双人交互的时空同步性。

### 输入输出流

**输入**由三部分组成：
- **源动作** $\mathbf{x}_{1:L}^s \in \mathbb{R}^{L \times 2d_m}$：双人动作序列，每帧包含两人的全局关节位置、速度、6D 局部旋转和足部接触标签（Eq. 1）。源动作通过一个轻量可学习的 Transformer 运动编码器压缩为固定长度的条件嵌入 $\mathbf{c}_{\text{src}}$。
- **编辑指令** $\mathbf{y}$：自然语言文本，描述对源动作的修改意图。文本通过冻结的 CLIP 编码器提取为条件嵌入 $\mathbf{c}_{\text{text}}$。
- **噪声化目标动作** $\mathbf{x}_t$：在训练时，目标动作 $\mathbf{x}_0$ 按前向扩散过程 $q(\mathbf{x}_t | \mathbf{x}_{t-1})$ 逐步加噪（Eq. 5）；推理时从纯噪声 $\mathbf{x}_T \sim \mathcal{N}(0, \mathbf{I})$ 开始迭代去噪。

**输出**为预测的干净目标动作 $\hat{\mathbf{x}}_0$，采用 Start_X 参数化，即去噪网络直接预测 $\mathbf{x}_0$ 而非噪声（Eq. 10）。

### 核心 Pipeline 模块

InterEdit 的框架由四个关键模块构成，其协同关系如 Figure 2 所示：

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the proposed InterEdit framework. Given a two-person motion and an editing instruction, InterEdit uses a conditional diffusion backbone with symmetric interleaved motion tokens. It introduces (i) Semantic-Aware Plan Token Alignment for high-level editing guidance via a motion-teacher embedding, and (ii) Interaction-Aware Frequency Token Alignment using DCT-based band-energy descriptors to regulate interaction dynamics*

1. **条件扩散骨干网络**：采用 Transformer 架构的去噪器 $\mathcal{D}_\theta$，以对称交错令牌聚合方式处理双人动作序列。具体而言，将两人逐帧动作令牌交错排列，并通过自注意力捕获跨人、跨时间的依赖关系；同时引入局部模式增强分支，以卷积层捕捉短时运动模式。时间步 $t$、文本条件 $\mathbf{c}_{\text{text}}$ 和源运动条件 $\mathbf{c}_{\text{src}}$ 通过自适应层归一化注入网络各层。

2. **语义感知计划令牌对齐**：在去噪器的中间 Transformer 层附加一组可学习的计划令牌。这些令牌通过自注意力与动作令牌交互，其输出经投影后与预训练运动教师编码器提取的目标动作语义嵌入进行 InfoNCE 对齐（Eq. 14）。该模块为扩散过程注入高层编辑意图，确保生成的动作遵循文本指令的语义要求，同时不直接约束动作细节，保持编辑的灵活性。

3. **交互感知频率令牌对齐**：计算双人动作的平均信号 $\mathbf{z}_S$ 和差分信号 $\mathbf{z}_D$（Eq. 15），分别进行离散余弦变换，并按低、中、高频带进行能量池化，得到频带能量描述符。这些描述符经线性映射后作为频率控制令牌加入去噪器，并通过加权 L2 损失回归目标动作的频带能量（Eq. 21）。该模块显式正则化交互节奏、同步性和空间耦合，防止编辑破坏人际协调。

4. **同步分类器免引导**：训练时以一定概率同步丢弃源条件和文本条件，学习无条件分支；推理时通过有条件与无条件预测的插值进行引导（Eq. 11）。这种同步丢弃策略避免了条件泄露，提供更干净的引导方向。

### 训练目标

总损失函数由扩散重构损失、辅助运动正则化损失、计划令牌对齐损失和频率令牌对齐损失加权组合而成（Eq. 23）：

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{motion}} + \lambda_p \mathcal{L}_{\text{plan}} + \lambda_f \mathcal{L}_{\text{freq}}$$

其中 $\mathcal{L}_{\text{motion}}$ 包含 Start_X 重构损失以及速度、足部接触、骨骼长度、距离图和相对朝向等辅助损失；$\lambda_p=0.03$ 和 $\lambda_f=0.01$ 为经消融验证的最佳权重（Table 7, Table 8），表明两种对齐损失应作为辅助正则项而非主导损失。

### 关键设计决策

- **双人序列建模**：与基线方法直接沿特征维度拼接双人运动不同，InterEdit 采用对称交错令牌聚合，并引入角色互换序列增强对称性，使模型对两人的身份顺序不敏感。
- **解耦的语义与交互控制**：将编辑过程解耦为语义意图引导与交互频率正则化两个互补通道，前者保证编辑准确性，后者保证交互一致性。消融实验证实，联合使用两个模块在所有指标上均优于单独使用任一模块或两者均不用（Table 3）。
- **频率令牌 dropout**：训练时对频率令牌施加 $p_f=0.04$ 的 dropout，在避免过拟合与保留交互正则化之间取得最佳平衡（Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/001_Figure_1.jpg]]
*Figure 1: An illustration of (a) Text-guided Multi-human 3D Motion Editing (TMME) task and our proposed InterEdit model, and (b) the performances of baselines (i.e., MotionFix [2], MotionLab [12], InterGen [24], TIMotion [46]) and our InterEdit*



InterEdit 以条件扩散模型为骨干，在 Start_X 参数化的 Transformer 去噪器上引入两个互补的对齐模块，将多人物动作编辑解耦为语义意图引导与交互频率正则化。以下按骨干架构、语义对齐、频率对齐和同步免引导的顺序展开。

### 条件扩散骨干与双人动作序列建模

**运动表示。** 第 $p$ 个人在第 $\ell$ 帧的运动状态定义为全局关节位置、速度、6D 局部旋转和二元足部接触的拼接：

$$\mathbf{x}_{\ell}^{p} = \big[ \mathbf{j}_{g,\ell}^{p}, \ \mathbf{v}_{g,\ell}^{p}, \ \mathbf{r}_{\ell}^{p}, \ \mathbf{c}_{\ell}^{p} \big] \in \mathbb{R}^{d_{m}}$$

双人动作序列沿特征维度拼接为 $\mathbf{x}_{1:L} = (\mathbf{x}_{1:L}^{A}, \mathbf{x}_{1:L}^{B}) \in \mathbb{R}^{L \times 2 d_{m}}$。

**对称交错令牌聚合与局部模式增强。** 为显式建模双人交互的时间顺序和短时模式，去噪器采用对称交错令牌聚合：将 A、B 的运动令牌交错排列，并额外引入角色互换序列，增强对交互对称性的感知。同时，局部模式增强分支（LPA）通过卷积捕获短时运动模式，其输出与全局特征经通道拼接后线性投影融合：

$$\mathbf{x}_c^{p,f} = \operatorname{Linear}\big(\operatorname{Concat}(\hat{\mathbf{x}}_c^{p,g}, \hat{\mathbf{x}}_c^{p})\big), \quad p \in \{A, B\}$$

时间步、文本条件和源运动条件通过 AdaLN 注入 Transformer 层。

**扩散重构损失。** 采用 Start_X 参数化，去噪器直接预测干净运动 $\hat{\mathbf{x}}_0$，训练目标为重构 MSE：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{t, \mathbf{x}_0, \epsilon} \Big[ \big\| \mathbf{x}_0 - \mathcal{D}_\theta \big( \mathbf{x}_t, t; \mathbf{c}_{\mathrm{text}}, \mathbf{c}_{\mathrm{src}} \big) \big\|_2^2 \Big]$$

### 语义感知计划令牌对齐

该模块为扩散过程注入高层编辑意图。在去噪器中间层附加一组可学习的计划令牌，通过自注意力与动作令牌交互后，经投影头得到归一化嵌入 $\tilde{\mathbf{z}}^{(k)}$。对齐目标由预训练运动教师编码器从目标运动提取的语义嵌入 $\tilde{\mathbf{z}}_{\mathrm{tgt}}$ 提供。采用 Token-wise InfoNCE 损失，将每个计划令牌的投影拉向正样本目标嵌入，同时推开批次内其他样本的负样本嵌入：

$$\mathcal{L}_{\mathrm{plan}} = \frac{1}{N_M} \sum_{k=1}^{N_M} \left[ -\log \frac{\exp{\big( (\tilde{\mathbf{z}}^{(k)})^{\top} \tilde{\mathbf{z}}_{\mathrm{tgt}} / \tau \big)}}{\sum_n \exp{\big( (\tilde{\mathbf{z}}^{(k)})^{\top} \tilde{\mathbf{z}}_{\mathrm{tgt}}^{(n)} / \tau \big)}} \right]$$

消融实验表明，InfoNCE 损失在检索与 FID 权衡上优于余弦相似度和 MSE（Table 6），且在第 3 层 Transformer 施加计划损失效果最佳（Table 5）。

### 交互感知频率令牌对齐

该模块通过 DCT 频带能量正则化保持交互节奏、同步性和空间耦合。首先计算双人运动的平均信号 $\mathbf{z}_S = (\mathbf{x}^A + \mathbf{x}^B)/2$ 和差分信号 $\mathbf{z}_D = \mathbf{x}^A - \mathbf{x}^B$，分别反映共同运动和相对运动。对二者分别进行 DCT 变换后，将频率系数桶化为低、中、高频带，池化得到频带能量描述符。这些描述符经映射后作为频率控制令牌加入去噪器，并通过加权 L2 损失回归目标运动的频带能量：

$$\mathcal{L}_{\mathrm{freq}} = \frac{1}{N_f} \sum_{i=1}^{N_f} w_i \big\| \hat{\mathbf{g}}_i - \mathbf{g}_i(\mathbf{x}_0) \big\|_2^2$$

其中 $\hat{\mathbf{g}}_i$ 为预测的频带能量描述符，$\mathbf{g}_i(\mathbf{x}_0)$ 为真实目标运动的对应描述符，$w_i$ 为频带权重。适中的频率令牌 dropout 率（$p_f=0.04$）在避免过拟合与保留正则化之间取得最佳平衡（Table 4）。

### 同步分类器免引导与总损失

训练时同步丢弃源条件和文本条件以学习无条件分支，推理时插值有条件与无条件预测，避免条件泄露并提供更干净的引导方向。总训练损失为：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{motion}} + \lambda_{p} \mathcal{L}_{\mathrm{plan}} + \lambda_{f} \mathcal{L}_{\mathrm{freq}}$$

其中 $\mathcal{L}_{\mathrm{motion}}$ 包含扩散重构、速度、足部接触、骨骼长度、距离图和相对朝向损失。敏感性分析表明，计划损失权重 $\lambda_p=0.03$ 和频率损失权重 $\lambda_f=0.01$ 为最佳设置，二者应作为辅助正则项而非主导损失（Table 7, Table 8）。联合使用两种令牌对齐在所有指标上优于单独使用任一模块或两者均不用，证明语义引导与交互正则化的互补性（Table 3）。



## 实验与关键发现

### 主要定量结果

Table 2 报告了 InterEdit 与四个基线方法在 InterEdit3D 测试集上的全面对比。基线包括两个单人物编辑方法（**MotionFix** 和 **MotionLab**，均通过拼接双人特征后微调适配）以及两个多人物生成方法（**InterGen** 和 **TIMotion**，通过 AdaLN 注入源运动作为条件）。所有基线均基于 InterEdit3D 的表示重新训练，使用相同的数据分割和评估协议，确保可比性。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison (mean, 95% CI)*

InterEdit 在所有度量上显著超越最强基线 TIMotion：

- **生成质量**：FID 从 TIMotion 的约 0.445 降至 0.3707±0.0029，相对降低 16.7%，表明编辑结果的分布更接近真实目标运动。
- **语义一致性**：generated-to-target retrieval R@1 达到 30.82±0.43，较 TIMotion 的 24.97 提升 5.85 个百分点，证明编辑结果更准确地遵循文本指令。
- **源内容保持**：generated-to-source retrieval R@1 为 17.08±0.41，较 TIMotion 的 12.54 提升 4.54 个百分点，显示未编辑部分得到更好保留。

单人物编辑基线（MotionFix、MotionLab）整体表现最弱，说明简单拼接双人特征无法有效处理交互建模。多人物生成基线（InterGen、TIMotion）虽能生成合理的双人运动，但缺乏显式编辑机制，导致语义遵循和源保持能力不足。InterEdit 通过语义感知计划令牌对齐和交互感知频率令牌对齐的协同作用，在编辑精度与交互一致性之间取得最优平衡。

### 核心模块消融

Table 3 展示了模块组件的消融结果，验证了两种对齐机制的互补性：

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/005_Table_3.jpg]]
*Table 3: Ablation of module component (mean, 95% CI)*

- **仅用计划令牌**（w/o freq token）：检索指标有所提升，但 FID 高于完整模型，表明仅有高层语义引导不足以维持交互的时空同步性。
- **仅用频率令牌**（w/o plan token）：FID 改善明显，但 g2t R@3 从 47.65±0.59 降至更低水平，说明缺少语义引导时编辑方向不够精确。
- **两者联合**：在所有指标上达到最优，g2t R@3 为 47.65±0.59，证明语义计划令牌负责“编辑什么”，频率令牌负责“如何保持交互一致”，二者形成因果互补。

### 频率令牌 Dropout 消融

Table 4 研究了频率令牌 dropout 率 p_f 的影响。适中的 dropout（p_f=0.04）在避免过拟合与保留交互正则化之间取得最佳平衡。当 p_f 过低（0.02）时，模型可能过度依赖频率令牌，导致检索指标下降；当 p_f 过高（0.08）时，正则化强度不足，FID 回升。这一结果表明频率令牌对齐应作为辅助正则项，而非主导训练信号。

### 计划令牌对齐位置与损失函数选择

Table 5 显示，在 Transformer 去噪器的中间层（L_p=3）施加计划令牌对齐损失优于早期层（L_p=1）或晚期层（L_p=5），获得最佳 g2t R@1/2/3。这表明中间层特征已充分融合源运动、文本和时间步条件，具备足够的语义抽象能力来承载编辑意图。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/010_Table_5.jpg]]
*Table 5: Ablation study regarding the location to conduct semantic-aware plan token alignment (freq layer=5, drop=0.04, mean, 95% CI)*

Table 6 对比了三种计划损失函数：InfoNCE、余弦相似度和 MSE。InfoNCE 在所有检索指标和 FID 上均最优，其对比学习机制能有效拉近计划令牌投影与目标运动语义嵌入，同时推开批次内负样本，提供更清晰的编辑方向。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/011_Table_6.jpg]]
*Table 6: Ablation study regarding the selection of loss for semantic-aware plan token alignment (mean, 95% CI)*

### 损失权重敏感性

Table 7 和 Table 8 分别报告了计划损失权重 λ_p 和频率损失权重 λ_f 的敏感性。λ_p=0.03 和 λ_f=0.01 为最佳设置。过度增大任一权重会导致 FID 或检索指标轻微下降，进一步印证两种对齐损失应作为辅助正则项，而非主导优化目标。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/013_Table_8.jpg]]
*Table 8: Ablation study of the*

### 同步分类器免引导策略

Table 9 对比了双分支与三分支 SCFG 策略。双分支策略（同步丢弃源和文本条件）在大多数指标上优于三分支（分别丢弃源或文本），因为同步丢弃避免了条件泄露，提供更干净的引导方向，同时减少了推理时的计算开销。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/014_Table_9.jpg]]
*Table 9: Ablation study of two-branch vs. three-branch SCFG (mean, 95% CI)*

### 人类偏好评估

Table 10 报告了 20 个提示词上的人类偏好研究。InterEdit 在指令遵循维度对 TIMotion 的 win rate 为 78.5%，在交互真实性维度达到 81.0%，两个维度均呈现压倒性优势。这从主观层面验证了语义令牌对齐（提升指令遵循）和频率令牌对齐（提升交互真实性）的实际效果。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/017_Table_10.jpg]]
*Table 10: Human evaluation on 20 prompts. Win/Tie/Lose rates (%) of InterEdit vs. TIMotion*

### 定性分析

Figure 3 展示了 InterEdit 与 TIMotion 在测试集上的定性对比。InterEdit 能精确执行文本指定的编辑（如“A 走向 B”变为“A 远离 B”），同时保持未编辑部分的运动特征和双人交互的时空同步。TIMotion 虽能生成看似合理的双人运动，但在编辑精度和交互一致性上均存在明显不足。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative results comparison of our InterEdit and TIMotion [46]*

Figure 4 展示了定制提示下的编辑结果，进一步验证了 InterEdit 对多样化编辑指令的泛化能力。

### 失败模式分析

Figure 8 揭示了 InterEdit 的两类典型失败案例：

1. **手势歧义**：对手势的微小变化（如双手击掌对象的混淆）存在语义歧义，模型难以可靠区分“谁对谁做什么”。这源于当前交互表示对细粒度手部语义的建模不足。
2. **长序列空间关系漂移**：在长时间高动态交互序列中，维持个体间严格的空间关系（如距离、朝向）仍存在漂移现象，表明现有的频率令牌正则化虽能保持局部同步性，但对全局空间约束的显式建模仍有欠缺。

这些失败模式指向两个改进方向：引入更细粒度的交互表示以消除手势歧义，以及设计显式的空间关系约束以改善长序列一致性。

### 补充图表

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/012_Table.jpg]]

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2603_13082/figures/002_Table_1.jpg]]
*Table 1: Comparison with representative existing datasets. “Editing” indicates whether the dataset provides source–target pairs and edit instructions*



## 定位与知识库关联

### 任务定位与基线谱系

InterEdit 面向**文本引导的多人物3D动作编辑**（Text-guided Multi-human 3D Motion Editing, TMME），该任务要求根据源双人动作和编辑指令生成保留未编辑部分、精确执行语义修改且维持交互一致性的目标动作。此前不存在直接解决 TMME 的工作，论文将两类邻近方法改造为基线：

- **单人物编辑方法适配**：**MotionFix** 和 **MotionLab** 原为单人动作编辑设计，通过沿特征维度拼接双人特征并微调适配至双人场景。这类方法缺乏对人际交互动力学的显式建模，编辑后常出现同步性破坏和角色错位。
- **多人物生成方法条件化**：**InterGen** 和 **TIMotion** 为双人动作生成模型，通过 AdaLN 将源运动作为条件注入扩散过程，实现“源条件化生成”以模拟编辑行为。其中 TIMotion 作为最强基线，在生成质量和指令遵循上显著优于前两者，但仍存在编辑语义漂移和交互失真问题——这源于其缺乏对编辑意图的显式语义引导和对交互频率的专门正则化。

InterEdit 在以下**三个关键维度**上区别于上述基线，构成其方法贡献的核心：

| 维度 | 基线策略 | InterEdit 策略 |
|------|----------|----------------|
| 编辑语义引导 | 源运动+文本简单拼接作为条件 | 语义感知计划令牌对齐：可学习令牌通过 InfoNCE 损失对齐预训练运动教师编码器提取的目标语义嵌入 |
| 交互动力学正则化 | 无专门约束，依赖生成模型隐式学习 | 交互感知频率令牌对齐：DCT 频带能量描述符显式正则化双人平均/差分信号的频率组成 |
| 双人序列建模 | 直接沿特征维度拼接 | 对称交错令牌聚合（含角色互换序列）+ 局部模式增强分支（LPA） |

### 核心机制与知识贡献

**1. 语义感知计划令牌对齐（Semantic-Aware Plan Token Alignment）**

该机制的核心洞察是：扩散模型的中间表示需要高层编辑意图的显式引导，而非仅依赖文本条件的隐式注入。具体做法为在 Transformer 去噪器的中间层（消融表明第3层最优）附加一组可学习的计划令牌，通过自注意力与动作令牌交互后，经投影头映射至语义空间，使用 token-wise InfoNCE 损失将其拉向预训练运动教师编码器提取的目标动作语义嵌入。这一设计的本质是将“编辑意图”形式化为可优化的隐变量，以对比学习的方式为扩散过程提供无梯度的语义牵引信号。

消融实验证实：InfoNCE 损失优于余弦相似度和 MSE（Table 6），适中的计划损失权重（λ_p=0.03）避免了对扩散主损失的干扰（Table 7）。该模块单独使用时，g2t retrieval R@3 从基线的 42.58 提升至 46.32（Table 3），证明语义引导的有效性。

**2. 交互感知频率令牌对齐（Interaction-Aware Frequency Token Alignment）**

该机制针对 TMME 的核心瓶颈——局部编辑可能破坏双人交互的时空耦合——提出了一个基于信号处理的显式正则化方案。首先计算双人运动的平均信号 z_S 和差分信号 z_D，分别捕捉共同运动和相对运动模式；然后对两者应用 DCT 变换并桶化为低、中、高频带能量描述符，将其映射为频率控制令牌加入去噪器，并施加加权 L2 损失回归目标频带能量。

这一设计的因果逻辑是：交互的节奏、同步性和空间耦合主要体现在频域的中低频带，通过显式约束编辑后动作的频带能量分布与目标一致，可强制维持交互动力学特征。消融表明适中的频率令牌 dropout（p_f=0.04）在避免过拟合与保留正则化之间取得最佳平衡（Table 4），频率损失权重 λ_f=0.01 为最优（Table 8）。

**3. 两种对齐机制的互补性**

Table 3 的核心消融直接验证了互补性：联合使用计划令牌和频率令牌达到最佳 g2t R@3（47.65±0.59），单独使用计划令牌（46.32）或频率令牌（44.75）均显著下降，两者均不用时进一步降至 42.58。这表明语义引导和频率正则化分别作用于编辑的“内容准确性”和“交互保真度”两个正交维度，联合使用产生协同效应。

### 适用边界与局限

**已验证的适用边界：**
- 双人交互场景，涵盖空间关系编辑（如距离、方位）、时间编辑（如节奏变化）、动作替换和身体部位编辑等语义维度
- 源动作和目标动作均来自 InterEdit3D 数据集分布内
- 编辑指令为自然语言描述，依赖 CLIP 文本编码器的语义理解能力

**明确的局限与失败模式：**

1. **手势歧义问题**（Figure 8）：对于涉及精细手部交互的编辑（如“握手”改为“石头剪刀布”），模型难以可靠区分“谁对谁做什么”，存在角色混淆和动作语义偏差。这源于当前交互表示缺乏对手势级别的细粒度建模。

2. **长序列空间关系漂移**（Figure 8）：在长时间高动态交互序列中，维持个体间严格的空间约束（如相对距离、朝向）存在累积误差，编辑后可能出现空间关系逐渐偏离目标的现象。这表明仅依赖频带能量正则化不足以捕捉长程空间依赖性。

3. **人数泛化未验证**：当前设计（对称交错令牌聚合、平均/差分信号）天然假设双人场景，对三人及以上交互的扩展需要重新设计令牌排列策略和交互信号定义，尚未进行实验验证。

4. **数据集构建成本**：InterEdit3D 依赖半自动检索与人工标注，扩展至更多交互类型或更长序列的成本较高，可能限制方法在开放域场景中的规模化应用。

### 开放问题

1. **细粒度交互消歧**：能否引入反事实训练或基于图神经网络的角色-动作绑定机制，使模型精确理解“谁对谁做什么”，消除手势级别的语义歧义？

2. **长程空间一致性**：当前的频带能量正则化主要约束时序频率特征，对空间关系的显式建模不足。引入基于骨骼图的相对位置预测损失或空间注意力偏置是否能改善长序列中的空间漂移？

3. **多人扩展路径**：将对称交错令牌聚合推广至 N 人排列组合、将平均/差分信号扩展为成对交互矩阵，所需的架构改动和训练数据规模如何？是否存在更高效的多人交互表示？

4. **频率表征的充分性**：现有的 DCT+均匀频带桶化是否能捕捉非线性交互动态（如突然的接触/分离事件）？是否需要引入小波变换或学习型频率表征以提升对瞬态交互的敏感性？

5. **编辑可控性的粒度**：当前方法接受自然语言指令进行整体编辑，是否能扩展至时空局部编辑（如“仅修改第3-5秒内人物A的左手动作”）或组合编辑（多条指令的顺序/并行执行）？



## 原文 PDF

![[paperPDFs/arxiv_2026/InterEdit_Navigating_Text_Guided_Multi_Human_3D_Motion_Editing.pdf]]
