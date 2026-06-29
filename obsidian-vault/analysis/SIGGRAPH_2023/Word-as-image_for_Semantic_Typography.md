---
title: Word-as-image for Semantic Typography
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/Word_as_image_for_Semantic_Typography.pdf
project_link: null
code_link: "https://github.com/Shiriluz/Word-As-Image"
aliases:
- LBLDST
- WAIST
tags:
- SIGGRAPH_2023
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
core_operator: 利用预训练Stable Diffusion模型的视觉先验，通过Score Distillation Sampling (SDS)损失直接优化字母的矢量轮廓控制点，使其在保持可读性的前提下融入语义概念。
primary_logic: 可将大规模文本-图像扩散模型的语义理解能力与可微分矢量光栅化相结合，通过优化字母轮廓的Bézier控制点实现语义变形，同时引入保形和色调保持正则化维护可读性和字体风格。
claims:
- 感知研究显示，该方法在语义识别(0.8)、易读性(0.9)和字体风格匹配(51%)方面均表现优异，风格匹配远高于随机水平(25%)。
- 移除结构保持损失(仅SDS)后，易读性从0.9骤降至0.53，字体风格匹配从0.51降至0.33。
- ACAP损失通过约束Delaunay三角剖分角度变化来维持字母整体结构，防止过度变形。
- 色调保持损失通过比较低通滤波图像来维持局部笔画粗细和字体风格。
---

# Word-as-image for Semantic Typography

> [!tip] 核心洞察
> 可将大规模文本-图像扩散模型的语义理解能力与可微分矢量光栅化相结合，通过优化字母轮廓的Bézier控制点实现语义变形，同时引入保形和色调保持正则化维护可读性和字体风格。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向语义排版的单词即图像 |
| 英文题名 | Word-as-image for Semantic Typography |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://arxiv.org/abs/2303.01818) · [Code](https://github.com/Shiriluz/Word-As-Image) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion |
| Method | LSDS-based Letter Deformation for Semantic Typography |
| Dataset | Perceptual Study |

> [!tip] 效果简介
> - Perceptual Study (Semantics) 上，概念可识别性评分 0.80 vs 0.88 (-0.08)。
> - Perceptual Study (Legibility) 上，易读性评分 0.90 vs 0.53 (+0.37)。
> - Perceptual Study (Font Style) 上，字体风格匹配比例 0.51 vs 0.33 (+0.18)。

## 概要

现有语义排版方法多依赖预定义图标替换或光栅纹理，难以在保持可读性和字体风格的前提下，灵活生成表达任意语义概念的矢量字母形状。本文提出一种基于语义的字母变形方法，将大规模文本-图像扩散模型的视觉先验与可微分矢量光栅化相结合，通过优化字母轮廓的Bézier控制点，使字母在保持原有结构的同时融入目标语义概念。

核心思路是将预训练的Stable Diffusion模型作为语义引导源，利用潜空间评分蒸馏采样（LSDS）损失驱动控制点更新，同时引入ACAP保形损失和色调保持损失来约束变形程度，维护字母的可读性与字体风格。感知研究结果表明，该方法在语义识别性（0.80）、易读性（0.90）和字体风格匹配（51%，远高于随机水平25%）方面均表现优异。消融实验证实，移除结构保持损失后易读性从0.90骤降至0.53，风格匹配也从51%降至33%，验证了各约束项的关键作用。与CLIPDraw等基于CLIP的矢量方法相比，LSDS损失能产生更平滑、语义更丰富的字母形状。该方法定位为语义排版的新范式，通过优化矢量轮廓而非光栅纹理，在可编辑性和语义表达能力之间取得了有效平衡。

## 核心方法与创新机理

### 问题瓶颈与核心思路

现有语义排版方法面临一个根本性瓶颈：它们要么依赖预定义的图标直接替换字母（如将“O”替换为足球图案），要么通过光栅纹理或颜色填充来传递语义，无法灵活生成表达任意抽象概念的矢量字母形状，同时保持字母的可读性和原始字体风格。例如，要让字母“Y”的轮廓变形后既传达“瑜伽”的语义，又清晰可读且保留原字体的衬线特征，传统方法难以胜任。

本方法的核心洞察在于：**大规模文本-图像扩散模型（如Stable Diffusion）内部蕴含了丰富的视觉语义先验，可以通过Score Distillation Sampling（SDS）机制将这些先验转化为对任意可微分参数的梯度信号。** 如果将字母表示为可微分矢量轮廓（Bézier曲线控制点），则可以利用扩散模型的语义理解能力直接优化这些控制点的位置，使字母形状在保持结构约束的前提下，自然融入目标概念的视觉特征。

### 方法框架与模块顺序

整个方法以单个字母为处理单元，对单词中的每个字母独立优化。给定一个输入字母和语义概念（如“猫”、“瑜伽”），系统通过迭代优化字母轮廓的控制点位置，生成语义变形的矢量字母。图5展示了完整的优化流程，包含以下顺序模块：

**模块1：字母轮廓提取与Bézier转换**  
使用FreeType字体库提取字母的矢量轮廓，将每条轮廓转换为三次Bézier曲线集合，得到初始控制点集 $P$。该步骤将字体文件中的字形转化为可优化的参数化表示。

**模块2：轮廓细分**  
为增加变形自由度，对初始Bézier曲线进行中点细分，将控制点数量从原始的数十个增加到数百个（图6展示了细分前后的控制点密度对比）。这一步骤是变形能力的关键——控制点过少则无法表达细粒度语义变化，过多则可能偏离原始字母形状（消融实验证实了这一点，见Figure 11）。

**模块3：可微分光栅化**  
使用DiffVG可微分矢量图形渲染器，将优化后的控制点集 $\hat{P}$ 光栅化为像素图像 $\mathcal{R}(\hat{P})$。这一模块是连接矢量优化与扩散模型梯度回传的桥梁，使得像素空间损失可以反向传播到控制点参数。

**模块4：LSDS损失计算（核心语义引导）**  
这是本方法最关键的创新模块。传统方法（如CLIPDraw）使用CLIP模型的图像-文本相似度作为优化目标，但CLIP损失产生的梯度较为粗糙，生成的形状纹理不够平滑，语义概念范围也较窄（Figure 14提供了对比证据）。

本方法采用**潜空间评分蒸馏采样（LSDS）损失**，直接利用预训练Stable Diffusion模型的去噪网络提供语义梯度。具体而言，LSDS损失梯度定义为：

$$\nabla _ { \theta } \mathcal { L } _ { \mathrm { L S D S } } = \mathbb { E } _ { t , \epsilon } \left[ w ( t ) \Big ( \hat { \epsilon } _ { \phi } ( \alpha _ { t } z _ { t } + \sigma _ { t } \epsilon , y ) - \epsilon \Big ) \frac { \partial z } { \partial z _ { a u g } } \frac { \partial x _ { a u g } } { \partial \theta } \right]$$

其中：
- $z_t$ 是光栅化字母图像经过VAE编码器映射到潜空间后的表示；
- $y$ 是语义概念文本提示；
- $\hat{\epsilon}_\phi$ 是Stable Diffusion的预训练去噪网络；
- $\frac{\partial z}{\partial z_{aug}}$ 和 $\frac{\partial x_{aug}}{\partial \theta}$ 构成从潜空间经增强图像到控制点参数的梯度回传链。

这一机制的本质是：扩散模型在去噪过程中“想象”目标概念的视觉特征，SDS损失将这种想象与当前字母图像的差异转化为对控制点的更新方向，从而驱动字母轮廓向符合语义概念的方向演化。

**模块5：ACAP保形损失计算**  
仅靠LSDS损失会导致字母形状过度变形，丧失可读性。为约束变形幅度，本方法引入**尽可能保形（As-Conformal-As-Possible, ACAP）变形损失**。具体做法是：对字母内部区域进行约束Delaunay三角剖分（图7），然后计算每个三角形顶点角度在变形前后的L2距离：

$$\mathcal { L } _ { a c a p } ( P , \hat { P } ) = \frac { 1 } { k } \sum _ { j = 1 } ^ { k } \left( \sum _ { i = 1 } ^ { m _ { j } } \big ( \alpha _ { j } ^ { i } - \hat { \alpha } _ { j } ^ { i } \big ) ^ { 2 } \right)$$

其中 $k$ 是三角形数量，$m_j$ 是第 $j$ 个三角形的顶点数，$\alpha_j^i$ 和 $\hat{\alpha}_j^i$ 分别是变形前后对应顶点的角度。通过最小化角度变化，ACAP损失强制变形在局部保持角度相似性，从而维持字母的整体拓扑结构。

**模块6：色调保持损失计算**  
ACAP损失主要维护几何结构，但无法保证字体风格（如笔画粗细、衬线特征）的保持。为此引入**色调保持损失**，通过比较原始字母与变形字母的低通滤波图像来约束局部黑白分布：

$$\mathcal { L } _ { t o n e } = \left| \left| L P F ( \mathcal { R } ( P ) ) - L P F ( \mathcal { R } ( \hat { P } ) ) \right| \right| _ { 2 } ^ { 2 }$$

低通滤波（LPF）去除了高频细节，保留了区域性的色调分布信息。如图8所示，该损失确保变形后的字母在局部区域的“黑度”与原始字母保持一致，从而维护字体风格特征（如笔画粗细变化规律）。

**模块7：控制点更新（Adam优化器）**  
将上述三个损失加权组合为总优化目标：

$$\underset { \hat { P } } { \operatorname* { m i n } } \nabla _ { \hat { P } } \mathcal { L } _ { \mathrm { L S D S } } ( \mathcal { R } ( \hat { P } ) , c ) + \alpha \cdot \mathcal { L } _ { a c a p } ( P , \hat { P } ) + \beta _ { t } \cdot \mathcal { L } _ { t o n e }$$

其中 $\alpha$ 控制保形强度，$\beta_t$ 是色调保持损失的时变权重。$\beta_t$ 采用高斯函数调度：

$$\beta _ { t } = a \cdot \exp \big ( - \frac { ( t - b ) ^ { 2 } } { 2 c ^ { 2 } } \big )$$

参数设置为 $a=100, b=300, c=30$。这一调度的设计意图是：在优化初期（$t$ 较小时），$\beta_t$ 很小，允许字母自由进行语义变形；随着优化进行，$\beta_t$ 逐渐增大，在 $t=300$ 附近达到峰值后衰减，在变形已基本完成后强化风格保持约束。这种“先语义后风格”的调度策略平衡了概念表达与字体保真度。

使用Adam优化器迭代更新控制点 $\hat{P}$，每次迭代依次执行光栅化、LSDS梯度计算、ACAP损失计算、色调损失计算，然后反向传播更新参数。

### 核心创新槽位分析

相比现有方法，本工作在以下关键维度实现了创新：

**创新槽位1：优化目标从CLIP导向转为扩散模型SDS导向**  
CLIPDraw等基线使用CLIP模型的图像-文本匹配分数作为优化信号，但CLIP的视觉理解相对粗糙，生成的矢量图形往往纹理不自然、语义范围受限。本方法改用Stable Diffusion的LSDS损失，利用扩散模型在去噪过程中对视觉细节的丰富先验，产生更平滑、语义更贴切的字母形状（Figure 14的对比消融证实了这一点）。这一转变的本质是利用了扩散模型更强的生成先验替代判别式模型的匹配信号。

**创新槽位2：字母表示从光栅图像转为矢量轮廓控制点**  
传统语义排版方法在像素空间操作，输出为光栅图像，无法直接用于矢量设计工作流。本方法直接在Bézier曲线控制点上优化，输出为可编辑的矢量图形，保留了字体设计的可扩展性和可编辑性。这一表示转换的关键在于引入了可微分光栅化（DiffVG）作为像素空间损失与矢量参数之间的梯度桥梁。

**创新槽位3：引入双重形状约束（ACAP + 色调保持）**  
仅使用SDS损失优化的字母虽然语义丰富，但可读性严重下降（易读性从0.9降至0.53，字体风格匹配从0.51降至0.33，见Table 1的Only SDS行）。本方法创新性地组合了两种互补的形状约束：ACAP损失在几何层面维护局部角度保形性，防止结构崩溃；色调保持损失在视觉层面维护局部笔画特征，保留字体风格。两者协同作用，在语义表达与字母保真度之间建立了可控的权衡（通过调节 $\alpha$ 和 $\beta_t$ 调度参数实现，Figure 16展示了 $\alpha$ 的调节效果）。

### 训练与推理路径

本方法**无需训练**，直接使用预训练的Stable Diffusion模型（冻结参数）作为语义先验提供者。推理时，对每个字母执行约500次迭代的优化（具体迭代数见Appendix A），每次迭代的计算图从控制点 $\hat{P}$ 出发，经DiffVG光栅化后分两路：一路经VAE编码进入潜空间计算LSDS梯度，另一路在像素空间计算ACAP和色调损失，三路梯度汇总后更新控制点。整个流程为逐字母独立优化，可以并行处理单词中的不同字母。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01818/figures/004_Figure_6.jpg]]
*Figure 6: Illustration of the letter’s outline and control points before (left) and after (right) the subdivision process. The orange dots are the initial Bézier curve segment endpoints. The blue dots are the remaining control points respectively before and after subdivision*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01818/figures/003_Figure_5.jpg]]
*Figure 5: An overview of our method. Given an input letter ???? represented by a set of control points*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01818/figures/005_Figure_7.jpg]]
*Figure 7: Visual illustration of the constraint Delaunay triangulation applied to the initial shapes (left) and the resulting ones (right), for the word “pants”. The ACAP loss maintains the structure of the letter after the deformation. The zoomed rectangle shows the angles for a given control point*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01818/figures/012_Figure_19.jpg]]
*Figure 19: Examples of illustrations presented in the perceptual study. Each pair in the top part shows illustrations obtained using our proposed method (left) and using only SDS loss (right). On the bottom is an example of an illustration presented for the font recognition questions*

## 实验与关键发现

### 感知研究：主实验设计

为系统评估语义排版效果，作者设计了一项偏好感知研究，随机选取了20个概念（如“yoga”“pants”“flame”）、5个字母（A、S、M、N、L）和4种字体（Serif、Sans-Serif、Script、Display），生成共20组语义字形（Table 2）。邀请20名参与者对每组结果进行三个维度的评分：

- **语义可识别性**：参与者被要求从5个选项中识别字形所表达的概念，同时报告置信度（1–5分），最终语义评分 = 识别正确率 × 平均置信度 / 5。
- **易读性**：要求识别字母本身，评分方式与语义维度一致。
- **字体风格匹配**：展示4种候选字体，要求参与者选出变形后字形最匹配的原字体，统计匹配准确率。

Table 1汇总了主实验结果。本方法在三个维度上均取得优异表现：语义可识别性评分达 **0.80**，易读性评分达 **0.90**，字体风格匹配率达 **51%**（随机水平为25%）。这表明方法能在显著融入语义概念的同时，保持字母的高度可读性和原字体风格特征。

### 关键消融：结构保持损失的必要性

为验证ACAP保形损失和Tone保持损失的作用，作者设计了**Only SDS**消融基线——仅使用LSDS语义损失，移除全部结构保持项。Table 1中Only SDS的结果揭示了结构保持损失的决定性贡献：

| 指标 | Ours | Only SDS | 差异 |
|------|------|----------|------|
| 语义可识别性 | 0.80 | 0.88 | −0.08 |
| 易读性 | 0.90 | 0.53 | **+0.37** |
| 字体风格匹配 | 0.51 | 0.33 | **+0.18** |

仅使用SDS损失时，语义可识别性反而略高（0.88 vs 0.80），但易读性从0.90骤降至0.53，字体风格匹配从51%降至33%。这说明无约束的语义优化会过度扭曲字母形状，使其虽然更“像”目标概念，却丧失了作为文字的基本功能。ACAP和Tone损失的核心作用是在语义表达和字形保真度之间建立有效权衡——牺牲少量语义强度，换取大幅度的可读性和风格保持。

### 损失函数消融的视觉证据

Figure 15展示了逐项移除损失项的视觉效果：仅SDS产生的字形往往出现笔画断裂、比例失调等问题；单独加入ACAP损失能恢复字母的整体结构，但局部笔画粗细和字体风格仍可能偏离；进一步加入Tone损失后，局部色调和原字体风格得到有效保持。这验证了两个损失项在约束空间上的互补性——ACAP约束全局形状的保形变形，Tone约束局部笔画粗细和风格一致性。

### ACAP损失的机制与效果

ACAP损失通过对字母内部区域进行约束Delaunay三角剖分，计算变形前后各三角形顶点的角度变化L2距离（见公式）。Figure 7以“pants”为例展示了三角剖分的效果：初始字母的三角形网格在优化后仍保持相似的局部角度关系，从而防止出现非保形扭曲（如直线段变成不规则曲线、对称结构被破坏等）。调节ACAP权重α可在语义表达和形状保真度之间连续权衡（Figure 16）：α过小导致形状过度扭曲，α过大则限制语义变形能力。

### Tone保持损失的机制与效果

Tone保持损失通过比较原始字母与变形字母的低通滤波图像的L2距离来约束局部色调分布。Figure 8以“A”字母为例展示了低通滤波图像：原始字形的滤波图像保留了笔画粗细的空间分布信息，变形后若局部区域过度膨胀或收缩，滤波图像的对应区域会出现明显差异，Tone损失即惩罚这种差异。该损失采用高斯时变权重调度 β_t（a=100, b=300, c=30），在优化初期允许语义变形自由发生，后期逐步增强约束以锁定字体风格。

### LSDS vs CLIP损失的对比

作者将本方法的LSDS损失替换为CLIP图像-文本相似度损失（类似CLIPDraw的优化方式）进行对比。Figure 14的结果显示，CLIP损失产生的字形纹理不够平滑，语义概念的表现范围较窄，且容易产生不自然的变形模式。LSDS损失得益于Stable Diffusion强大的视觉先验，能生成更丰富、更平滑的语义变形。这一消融证实了扩散模型先验相比CLIP直接优化的优势——扩散模型在训练过程中学习了更完整的视觉概念分布，其SDS梯度能提供更自然的概念融合引导。

### 控制点密度的影响

字母轮廓的控制点数量直接影响变形能力。Figure 11展示了不同细分程度下的优化结果：控制点过少时，Bézier曲线自由度不足，难以表达复杂的语义变形（如火焰的曲线纹理）；控制点过多时，优化自由度增大可能导致局部区域的非预期变形，偏离原始字母形状。作者采用的细分策略在原始控制点之间均匀插入新点，在变形能力和形状稳定性之间取得平衡。

### 低通滤波参数的影响

Tone损失中的低通滤波参数σ控制约束的空间尺度。Figure 13显示，σ=1时滤波过于局部，形状约束过强，导致语义变化不足；σ较大时约束过于全局，无法有效保持局部笔画特征。作者选择的σ值在局部笔画保持和全局语义变形之间取得平衡。

### 多字体与多概念的泛化验证

Figure 9展示了“YOGA”在8种不同字体下的语义变形结果，Figure 4和Figure 21展示了更多概念和字母组合的生成效果。这些定性结果表明方法对不同字体风格（Serif、Sans-Serif、Script、Display等）和不同语义概念（动物、物体、动作、抽象概念等）均具有良好的泛化能力。字体风格在语义变形后仍可辨识，且不同字体对同一概念的语义表达呈现出风格化差异（如Serif字体的“yoga”更优雅，Display字体的更夸张），这进一步验证了Tone损失在保持字体风格方面的有效性。

### 方法的适用边界

尽管感知研究和消融实验验证了方法的有效性，仍需注意以下适用边界：首先，方法对每个字母独立优化，未显式建模字母间的视觉连贯性，在多字母单词中可能出现风格不一致；其次，语义变形程度受ACAP和Tone损失权重的制约，极端语义概念（如“explosion”）可能需要在可读性上做出更大妥协；最后，LSDS损失依赖Stable Diffusion的视觉先验，对于扩散模型本身理解不佳的罕见或抽象概念，语义变形质量可能下降。这些边界条件在原文中未进行系统量化评估，需要在实际应用中根据具体需求进行参数调整。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01818/figures/007_Table_1.jpg]]
*Table 1: Perceptual study results. The level of concept recognizability and letter legibility are very high, and style matching of the font is well above random. The “Only SDS” results are created by removing our structure and style preserving losses*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2303_01818/figures/009_Figure_11.jpg]]
*Figure 11: The effect of the initial number of control points on outputs. On the left are the input letters and the target concepts used to generate the results on the right*

## 定位与知识库关联

本文提出了一种面向语义排版的字母矢量变形方法，其核心定位在于**将大规模文本-图像扩散模型的语义先验与可微分矢量图形优化相结合**，在一个统一的优化框架中同时实现语义概念表达、字母可读性保持和字体风格维护。与已有工作的本质差异体现在以下几个关键维度上。

### 相对已有工作的 Slot 改变

本工作相对于语义排版和文本风格化领域的已有方法，改变了以下关键 slot：

1. **表示域（Representation Domain）**：从光栅图像域转向矢量轮廓域。已有方法如 **SDEdit**（Meng et al., ICLR 2022）和 **Stable Diffusion**（Rombach et al., CVPR 2022）在像素空间操作，输出为光栅图像，无法直接用于可缩放排版；**CLIPDraw**（Frans et al., 2022）虽生成矢量图形，但以随机曲线集合为起点，缺乏对字母结构的约束。本文直接在字母的 Bézier 曲线控制点上进行优化，保持了矢量图形的可编辑性和分辨率无关性。

2. **语义引导机制**：从 CLIP 图像-文本相似度转向 Stable Diffusion 的潜空间评分蒸馏采样（LSDS）梯度。CLIPDraw 使用 CLIP 损失引导矢量生成，但如图 14 所示，其产生的语义纹理不够平滑，概念范围受限。本文利用预训练 Stable Diffusion 的 LSDS 损失（源自 **Poole et al., 2022** 的 Score Distillation Sampling 和 **VectorFusion** 的潜空间扩展），使字母变形能捕捉更丰富、更自然的语义概念。

3. **形状保持约束**：从无显式形状约束转向 ACAP 保形损失与局部色调保持损失的组合。仅使用 SDS 损失（Table 1 中 Only SDS 行）会导致字母可读性从 0.9 降至 0.53，字体风格匹配从 0.51 降至 0.33。本文引入的 ACAP 损失（基于 **Hormann and Greiner, 2000** 的保形变形思想）通过约束 Delaunay 三角剖分的角度变化来维持字母整体结构；色调保持损失通过低通滤波图像比较来保留局部笔画粗细和字体风格。这两个正则项共同构成了从“无约束语义变形”到“约束语义变形”的关键转变。

### 知识库挂载点

本工作可挂载到以下知识库节点：

- **文本引导的图像/图形生成**：继承自 Stable Diffusion 的文本-图像生成能力和 Score Distillation Sampling 的参数优化范式，属于该脉络中“利用扩散模型先验优化非图像参数”的分支。
- **可微分矢量图形**：依赖 **DiffVG**（Li et al., 2020）提供的可微分光栅化能力，使梯度能从光栅域回传至矢量控制点。这是连接扩散模型（工作于光栅/潜空间）与矢量图形优化的关键桥梁。
- **保形变形（As-Conformal-As-Possible Deformation）**：ACAP 损失源自计算机图形学中的保形变形理论，用于在变形过程中尽可能保持局部角度，从而维护字母的结构完整性。
- **语义排版（Semantic Typography）**：区别于传统的纹理迁移或图标替换方法（如 **Yang et al., 2018**；**Berio et al., 2022**；**Zhang et al., 2017** 等），本工作直接在字母轮廓上融入语义，属于该领域的“语义驱动矢量变形”新范式。

### 适用边界与局限性

- **字母级操作**：方法对每个字母独立优化，未显式建模字母间或单词整体的协调性。对于需要整体构图的场景可能需要后处理。
- **控制点数量敏感**：控制点过少会限制变形表达能力，过多则可能导致偏离原始字母形状（Figure 11），需要在初始化时合理选择细分程度。
- **低通滤波参数 σ 的权衡**：σ=1 时形状约束过强，语义变化不足（Figure 13）；σ 增大则约束减弱，需要根据应用场景调节。
- **字体风格保持的局限**：色调保持损失通过低通滤波比较来约束局部黑白分布，但对于具有复杂衬线或装饰性极强的字体，其风格保持能力可能有限，感知研究中字体风格匹配率为 51%，虽远高于随机水平（25%），但仍有提升空间。
- **语义表达的边界**：方法依赖 Stable Diffusion 的语义理解能力，对于抽象概念或扩散模型训练数据中覆盖不足的概念，变形效果可能不理想。

### 后续工作启发

1. **多字母联合优化**：当前逐字母优化的策略可扩展到单词或短语级别的联合优化，引入字母间的一致性约束，使整体排版更具协调性。
2. **交互式编辑接口**：将优化框架嵌入交互式设计工具，允许设计师在优化过程中施加局部约束或引导，结合自动语义变形与人工微调。
3. **更丰富的字体属性保持**：除局部色调外，可探索保持字体其他属性（如笔画对比度、轴线角度、x-高度比例等）的正则化方法。
4. **扩展到其他视觉元素**：该框架不仅限于字母，可应用于图标、标志等矢量图形的语义变形，拓展到更广泛的图形设计领域。
5. **多概念融合**：探索在单个字母中融合多个语义概念的方法，或在不同字母中表达不同概念以构成复合语义叙事。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/Word_as_image_for_Semantic_Typography.pdf]]