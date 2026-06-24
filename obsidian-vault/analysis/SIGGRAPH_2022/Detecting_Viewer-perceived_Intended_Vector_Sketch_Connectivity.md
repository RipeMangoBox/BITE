---
title: Detecting Viewer-perceived Intended Vector Sketch Connectivity
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Detecting_Viewer_perceived_Intended_Vector_Sketch_Connectivity.pdf
project_link: "https://www.cs.ubc.ca/labs/imager/tr/2022/SketchConnectivity/"
code_link: "https://github.com/enjmiah/SketchConnectivity"
aliases:
- HLGIJD
- DVPIVSC
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
core_operator: 结合基于局部几何特征的成对分类器与基于全局闭合原则的概率增强，实现自动预期连接检测。
primary_logic: 人类观察者利用笔画之间的距离、方向、相对位置和局部上下文等局部线索，以及闭合原则等全局线索来判断笔画是否应连接；通过将这些线索编码为分类特征，并在增量决策过程中逐步融合，只需少量标注数据（31张部分标注的草图）即可达到接近人类的性能。
claims:
- 在用户感知研究中，参与者对本文方法输出的偏好比最佳对比方法高9倍（偏好本文65%，偏好Favreau et al. 仅8%）。
- 本文方法在检测预期连接方面达到与人类标注者相近的准确率（92% vs 94%）。
- 成对分类器在留一绘图交叉验证中达到99%的准确率、97%的精确率和96%的召回率。
- 仅使用31张部分标注的草图训练，便实现了强大性能，大幅减少了标注数据需求。
---

# Detecting Viewer-perceived Intended Vector Sketch Connectivity

> [!tip] 核心洞察
> 人类观察者利用笔画之间的距离、方向、相对位置和局部上下文等局部线索，以及闭合原则等全局线索来判断笔画是否应连接；通过将这些线索编码为分类特征，并在增量决策过程中逐步融合，只需少量标注数据（31张部分标注的草图）即可达到接近人类的性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 检测观众感知的意图向量草图连通性 |
| 英文题名 | Detecting Viewer-perceived Intended Vector Sketch Connectivity |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://www.cs.ubc.ca/labs/imager/tr/2022/SketchConnectivity/) · [Code](https://github.com/enjmiah/SketchConnectivity) · [Project](https://adobe.com/products/illustrator) |
| Topic | #topic/vision_multimodal_applications |
| Method | Hybrid Local-Global Intended Junction Detection |
| Dataset | 95张多样化的自由手绘草图（感知研究）, 31张绘图留一交叉验证（分类器） |

> [!tip] 效果简介
> - 95张多样化的自由手绘草图（感知研究） 上，用户偏好比（本文 vs Favreau et al.） 65% 偏好本文，12% 判定同等 vs 8% 偏好 Favreau et al. (9:1 偏好比)。
> - 31张绘图留一交叉验证（分类器） 上，分类器准确率 99% vs N/A。
> - 人工标注一致性测试集 上，与多数人类标注一致的比例 92% vs 94% (人类标注者间的一致性) (-2%)。

## 概要

自由手绘向量草图常因绘制不精确而出现笔画端点悬空，导致难以提取符合人类感知的闭合区域。现有方法多依赖简单的距离阈值，无法可靠区分观众感知的**预期交叉**与**预期间隙**。本文提出一种混合局部-全局的预期连接检测算法：在局部层面，利用人类观察者判断连接意图时采用的几何线索（距离、方向、相对位置、局部上下文）训练两个随机森林分类器，分别评估端到端和T型连接的概率；在全局层面，基于闭合原则引入**间隙比** $R_C = D/L$ 对分类器概率进行增强，通过增量决策过程逐步确定最终连接。该方法仅需31张部分标注的草图即可训练，在95张多样化草图的感知研究中以9:1的偏好比显著优于最佳对比方法 **Favreau et al. 2016**，且检测准确率（92%）接近人类标注者间的一致性水平（94%）。本方法定位于全自动向量草图连通性检测，填补了现有自动间隙闭合技术在区分预期与非预期连接方面的关键空白。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有方法无法可靠地区分人类感知的**预期交叉**与**预期悬空端点**。无论是基于简单距离阈值的启发式方法（如 Favreau et al., 2016 的 trapped-ball 扩散），还是基于学习的间隙修复方法（如 Sasaki et al., 2017; Simo-Serra et al., 2018a），它们都缺乏对人类观察者所用感知线索的系统建模。人类观察者在判断两个笔画端点是否应该连接时，不仅考虑端点间的距离，还综合运用**方向一致性**、**相对位置**、**局部上下文**（附近其他端点的分布）等局部线索，以及**闭合原则**（gestalt closure）等全局感知线索——当间隙相对于所形成区域足够小时，观察者倾向于在心理上闭合该间隙。

本文的核心洞察是：将这些局部和全局感知线索显式编码为可计算特征，训练轻量分类器评估成对连接概率，再通过闭合感知的增量决策过程逐步融合全局信息，从而以极少标注数据实现接近人类水平的预期连接检测。

### 方法总览

方法整体流程如图5所示，包含四个串行阶段：**预处理** → **主连接分类** → **次连接分类** → **全局闭合感知分类**。输入为自由手绘矢量线稿，输出为标注了所有预期连接（形成闭合笔画环）的图结构。

### 关键公式与感知原理

**间隙比（Gap Ratio）** 是贯穿全局决策的核心量，定义为：

$$R _ { C } = { \frac { D } { L } } .\tag{1}$$

其中 $D$ 为笔画序列形成的环内最大内切圆直径，$L$ 为序列中连续笔画间的最大间隙长度。当 $R_C < 1$ 时，间隙相对于区域过大，观察者不太可能将其视为预期连接；当 $R_C \geq 1$ 时，闭合感知增强。这一最小循环比约束（minimal cycle ratio constraint）在后续的主连接和全局闭合阶段均发挥关键作用。

**增强概率** 用于全局闭合阶段，将间隙比转化为对局部分类器概率的增强：

$$P' = P + C (R_C - 1)$$

其中 $P$ 为局部分类器输出的原始成对连接概率，$C$ 为闭包因子（closure factor），控制全局闭合线索的影响强度。当 $R_C > 1$ 时，即使局部分类器给出较低的连接概率，全局闭合线索也能将其提升至可接受水平。

### Changed Slot 1：连接可能性估计——从距离阈值到感知特征分类器

**基线做法**：先前方法（如 Favreau et al., 2016）依赖简单的距离阈值或 trapped-ball 半径判断是否闭合间隙，无法区分距离相近但意图不同的端点对。

**本文方案**：训练两个基于局部几何和上下文特征的随机森林分类器——**端到端（end-to-end）分类器**和**T型（T-junction）分类器**，分别评估两类连接的感知概率。

端到端分类器以两个悬空端点对为输入，提取的特征包括：端点间距离（以笔画宽度归一化）、切线方向差异、端点连线与各自切线的夹角、端点附近其他端点的密度等。这些特征直接编码了图2中展示的人类感知线索。

T型分类器处理一个悬空端点与另一笔画上最近点的配对，除上述几何特征外，还引入**端点密度特征**以捕获更大范围的上下文：

$$b = \sum_{\mathbf{p}_e \in \{\mathbf{endpoints}\}} \exp\left(-\frac{1}{2} \left( \frac{1}{\sigma} \frac{\| \mathbf{p}_1 - \mathbf{p}_e \|}{w_e} \right)^2 \right)$$

其中 $\mathbf{p}_1$ 为当前悬空端点，$\mathbf{p}_e$ 遍历图中所有其他端点，$w_e$ 为端点处笔画宽度，$\sigma=1$。该特征以高斯加权方式衡量端点附近其他端点的密度，超过3倍笔画宽度的端点贡献可忽略。这一特征使T型分类器能够感知“该端点是否处于笔画密集区域”，从而影响连接意图判断。

两个分类器均在31张部分标注的草图上训练，采用留一绘图交叉验证（leave-one-drawing-out cross-validation），达到99%的分类准确率、97%的精确率和96%的召回率。

### Changed Slot 2：高价位连接处理——从缺失到复合笔画T型分类

**基线做法**：先前方法通常仅处理端点对之间的连接，未显式建模一个端点连接到已有交叉点（高价位连接，valence ≥ 3）的场景。

**本文方案**：在次连接分类阶段，将T型分类器应用于**复合笔画**（composite strokes）。具体而言，对于主连接阶段后剩余的每个悬空端点，找到其附近的已识别交叉点，将该交叉点处相邻的笔画临时合并为一条复合笔画，然后将T型分类器应用于该悬空端点与复合笔画之间，评估形成高价位连接的感知概率。这一设计使得方法能够处理任意价位的预期连接，而无需为不同价位训练单独的分类器。

### Changed Slot 3：全局上下文利用——从无到闭合感知增量决策

**基线做法**：先前自动方法或完全忽略全局闭合线索，或依赖用户交互提供全局信息（如 LazyBrush 的笔画标注）。

**本文方案**：设计闭合感知的增量决策过程，将局部分类器概率与间隙比 $R_C$ 融合。

**主连接分类阶段**：首先利用两个分类器计算所有候选端点对的连接概率。当分类器判定某对端点应连接且概率超过阈值时，形成初始连接子集。关键的是，这些连接可能形成闭合环，系统检查每个环是否满足最小循环比约束 $R_C \geq 1$；若违反，则沿着环的边界移除概率最低的连接，打破该环。这一机制防止了在间隙过大的情况下错误闭合。

**全局闭合感知分类阶段**：构建潜在的笔画环，对环上每个间隙，将局部分类器概率 $P$ 通过增强公式 $P' = P + C(R_C - 1)$ 进行提升。当增强后的概率超过阈值时，闭合该间隙。这一阶段能够捕获那些局部分类器给出边缘负面判断、但从全局闭合角度看明显应连接的间隙。

### 训练与推理路径

**训练路径**：仅需31张部分人工标注的草图。标注者只需标出哪些悬空端点应连接、哪些应保持悬空，无需完整标注所有连接关系。从这些标注中提取正负样本对，训练两个随机森林分类器。闭包因子 $C$ 通过验证集调优确定。

**推理路径**：
1. **预处理**：合并重描笔画（overdrawn strokes），移除笔画末端的钩子（hooks），检测所有平凡笔画交点（即几何上已相交的笔画）。
2. **主连接分类**：对所有候选端点对运行端到端和T型分类器，形成初始连接图；对违反 $R_C < 1$ 的环进行破环操作。
3. **次连接分类**：对剩余悬空端点，通过复合笔画机制评估高价位连接。
4. **全局闭合感知分类**：构建潜在环，计算间隙比，增强概率，闭合满足条件的间隙。

### 因果链路总结

局部几何特征 → 成对分类器概率 → 主连接图 → 最小循环比约束破环 → 剩余端点 + 复合笔画 → 次连接 → 潜在环构建 → 间隙比增强概率 → 最终闭合决策。这一链条实现了从局部感知判断到全局感知验证的渐进式决策，使方法仅需极少标注数据即可达到与人类标注者相近的准确率（92% vs 94%）。

![[assets/figures/papers/paper_list_l20_https_www_cs_ubc_ca_labs_imager_tr_2022_SketchConnectivity/figures/001_Figure_1.jpg]]
*Figure 1: (a) Free-hand vector line drawings are often imprecise with strokes intended to intersect stopping short of doing so; loops formed by raw strokes visualized on top left, each closed loop interior colorized with a different color, with the background left white. We successfully extract viewer perceived intended stroke connectivity distinguishing between intended junctions (a, e.g. circled in blue) and intended gaps (a, e.g. circled in red) (e) outperforming prior art (b, c). We arrive at this solution by combining local feature based predictions of the likelihood of pairs of strokes to form intended junctions (d) with global perceptual cues (e). Please zoom in to see image details throughout...*

![[assets/figures/papers/paper_list_l20_https_www_cs_ubc_ca_labs_imager_tr_2022_SketchConnectivity/figures/002_Figure_2.jpg]]
*Figure 2: Human observers employ local and global cues to determine if a dangling endpoint (red) is intentional, or is intended to be part of a junction. As highlighed in (ab) and (ef ), distance is a major factor in distinguishing between intended junctions (af ) and intended gaps (be). Different tangent directions can impact the perception of junction intent for endpoint (cd) or endpoint and stroke pairs (gh) at the same distance from one another. (i-n) The presence of other strokes can change the perception of whether strokes do or do not form junctions*

![[assets/figures/papers/paper_list_l20_https_www_cs_ubc_ca_labs_imager_tr_2022_SketchConnectivity/figures/008_Figure_5.jpg]]
*Figure 5: Method Overview. Given a vector line drawing (a), we first detect trivial stroke-wise intersections forming closed stroke loops (b, right). We then identify likely end-to-end (red) and T- (blue) junctions (b, left zoom-ins). With these pairs and their predictions, we constructs primary junctions, supporting arbitrary valence (c, see left zoom-ins for examples). We proceed to identify secondary T-junctions formed by the remaining dangling endpoints and composite strokes (d, see left zoom-ins for example connections). In the final closure integrated step, we close remaining undesirable gaps by jointly evaluating classifier predictions and gap ratios along the boundaries of potential cycles (e...*

## 实验与关键发现

### 感知研究：用户偏好压倒性领先

本文通过一项覆盖95张多样化自由手绘草图的用户感知研究验证方法有效性。参与者对本文方法输出与最佳对比方法 **Favrereau et al. (2016)** 的输出进行盲选比较。结果显示：**65%的情况下参与者偏好本文方法，12%判定两者同等，仅8%偏好Favreau et al.**——偏好比达到约9:1，所有偏好测试结果均具有高度统计显著性（p<0.001）。这一压倒性优势表明，结合局部几何特征分类与全局闭合感知的混合策略，在区分预期交叉与预期间隙方面远超仅依赖距离阈值或区域闭合的先前方法。

### 与人类标注者的一致性

在人工标注一致性测试集上，本文方法在检测预期连接方面达到**92%的准确率**，与人类标注者间的94%一致性仅差2个百分点。这证明该方法已接近人类水平。但需注意，仍有部分参与者在比较中选择“两者都不”，说明全自动预期连接检测尚未完全解决，存在改进空间。

### 分类器性能：留一交叉验证

成对分类器（端到端和T型）在31张绘图留一交叉验证中达到**99%的准确率、97%的精确率和96%的召回率**。这一结果验证了所提取的局部几何特征（距离、方向、相对位置、端点密度等）对连接意图具有强判别力。值得注意的是，该性能仅基于31张部分标注的草图训练获得，大幅降低了标注数据需求——这是该混合方法的核心优势之一。

### 关键消融：间隙大小与闭包因子的鲁棒性

**间隙大小的鲁棒性**：Fig. 8（上）展示了全局闭合步骤对间隙大小变化的鲁棒性。实验通过逐步增大草图中特定间隙的距离，观察连接决策的变化。结果表明，即使间隙距离增大至原来的**2.8倍**，闭包步骤仍能正确维持连接。这验证了间隙比 $R_C = D/L$ 作为全局感知线索的有效性：当循环内最大内切圆直径 $D$ 与连续笔画间最大间隙长度 $L$ 的比值超过1时，人类观察者倾向于感知为闭合循环，该方法成功编码了这一原则。

**闭包因子 $C$ 的敏感性**：增强概率公式 $P' = P + C(R_C - 1)$ 中的闭包因子 $C$ 对结果有显著影响。Fig. 8（下）展示了 $C$ 值变化的效应：
- **$C$ 过小**：间隙比对概率的增强不足，导致主要区域未被正确捕获，出现欠分割；
- **$C$ 过大**：全局步骤产生不可取的误报，将预期间隙错误闭合。

这一消融揭示了混合方法中数据驱动（局部分类器概率 $P$）与感知驱动（全局间隙比增强）之间的平衡机制：$C$ 调节了全局闭合线索对局部分类决策的修正力度，其最优值需要在欠分割与过分割之间权衡。

### 与先前方法的定性对比

Fig. 4 系统对比了本文方法与五种先前自动间隙闭合方法（Favreau et al. 2016; Fourey et al. 2018; Parakkat et al. 2021; Sasaki et al. 2017; Simo-Serra et al. 2018a）在光栅化向量草图上的输出。先前方法普遍存在两类失败：
- **非预期交叉**：如Fourey et al.对角色面部的过度分割；
- **未解决的悬空端点**：如Favreau et al.、Parakkat et al.、Sasaki et al.和Simo-Serra et al.均未能将角色面部与背景分离。

![[assets/figures/papers/paper_list_l20_https_www_cs_ubc_ca_labs_imager_tr_2022_SketchConnectivity/figures/004_Figure_4.jpg]]
*Figure 4: Rasterizing vector sketches and then applying the methods of [Favreau et al. 2016] (b), [Fourey et al. 2018] (c), [Parakkat et al. 2021] (d), [Sasaki et al. 2017] (e), and [Simo-Serra et al. 2018a] (f ) to compute closed stroke loops produces sub-par outputs with both unintended junctions (e.g. Fourey et al. [2018] over-segments character’s face) and unresolved dangling endpoints (e.g. none of [Favreau et al. 2016; Parakkat et al. 2021; Sasaki et al. 2017; Simo-Serra et al. 2018a] separates character’s face from the background). Our outputs (g) correctly identify both intended junctions and intended dangling endpoints. We show both high and low resolutions (600px and 1000 px) for (b, c, e,...*

本文方法正确识别了预期交叉和预期悬空端点，验证了向量信息利用与局部-全局混合策略相对于纯光栅化方法的优势。

### 与交互式工具的对比：大幅减少人工修正

Fig. 7 展示了从本文方法自动输出出发进行交互式修正的效率优势。以 **LazyBrush**（Sýkora et al., 2009）为基准：从头交互式操作需要31分钟（70次笔触，1次擦除）；而从本文自动输出出发，用户仅需2分钟（7次修正）即可获得相同最终输出。这证明该方法作为交互式工作流的预处理步骤具有显著实用价值。

![[assets/figures/papers/paper_list_l20_https_www_cs_ubc_ca_labs_imager_tr_2022_SketchConnectivity/figures/015_Figure_7.jpg]]
*Figure 7: Comparison against interactive region detection. Given an input (a), the interactive LazyBrush tool [Sýkora et al. 2009] required 31 minutes (70 strokes, one erased) (b); starting from our automatically computed output (c) users required 2 minutes (7 corrections) to obtain the same final output (d). Input image ©The “Hero” artist Team under CC BY 4.0*

### 失败模式与适用边界

**增量处理的局限性**：当输入为未完成绘图时，由于缺少完整全局上下文，本文方法和人类观察者都可能将某些预期间隙误判为非预期并尝试闭合。在绘画过程中自动闭合此类间隙对艺术家具有高度干扰性——这表明该方法更适合作为后处理步骤应用于已完成草图，而非实时增量式辅助。

**过绘与影线的鲁棒性不足**：核心方法设计用于无或最小过绘的输入。对于含有大量过绘或影线的草图，需要更强大的预处理（尤其是笔画合并），而该预处理本身仍是一个开放研究问题。这是该方法当前的主要适用边界。

**全自动检测的上限**：尽管显著优于所有对比方法，感知研究中仍有参与者选择“两者都不”，表明在极端模糊或高度风格化的草图中，全自动预期连接检测仍有改进空间。探索自适应闭包因子 $C$（基于局部或全局绘图特性动态调整）是论文指出的后续方向之一。

![[assets/figures/papers/paper_list_l20_https_www_cs_ubc_ca_labs_imager_tr_2022_SketchConnectivity/figures/014_Figure_8.jpg]]
*Figure 8: Impact of increasing the top left gap size (top) and the closure factor ?? (bottom) during our final, global closure-aware classification step. Top input image ©Company et al. [2019]. Bottom input image ©The “Hero” artist Team under CC BY 4.0*

## 定位与知识库关联

本文在草图连通性感知这一长期问题上，改变了**连接可能性估计**这一核心 slot：将先前方法普遍采用的简单距离阈值或 trapped-ball 半径，替换为基于局部几何与上下文特征训练的随机森林分类器，并进一步通过**全局闭合感知的增量决策过程**对分类器输出进行概率增强。这一 slot 的替换是因果瓶颈的精确响应——现有方法之所以无法可靠区分预期交叉与预期悬空端点，正是因为缺乏对人类观察者所使用的局部线索（距离、方向、相对位置、局部端点密度）和全局线索（闭合原则）的联合建模。

### 相对于已有方法的本质差异

**Favreau et al.**（ACM Trans. Graph. 2016）采用 trapped-ball 扩散机制自动闭合区域，其连接决策完全由几何半径阈值驱动，缺乏对笔画间语义意图的判别能力。**Fourey et al.**（Eurographics 2018）和 **Parakkat et al.**（CHI 2021）分别提供半自动和交互式间隙闭合方案，但均依赖用户输入来指定区域或间隙位置，自动化程度远低于本文的全自动方法。**Sasaki et al.**（CVPR 2017）和 **Simo-Serra et al.**（ACM Trans. Graph. 2018）引入了基于学习的间隙检测，但前者需要大量全标注训练数据，后者则通过对抗学习简化草图，并未显式建模预期连接与预期间隙的区分。**LazyBrush**（Sýkora et al., Comput. Graph. Forum 2009）作为代表性交互式工具，需用户手动描画区域边界，本文方法从自动输出出发仅需 2 分钟修正即可达到相同结果，而从头交互需 31 分钟。

与上述所有方法的根本不同在于：本文构建了一个**数据驱动与感知驱动混合**的决策链。局部分类器将人类标注的成对连接意图编码为可泛化的特征，全局闭合步骤则通过间隙比 $R_C = D/L$ 将格式塔闭合原则量化为可计算的概率增强项 $P' = P + C(R_C - 1)$。这种“局部判别 + 全局增强”的双层架构使得方法仅需 31 张部分标注草图即可训练，而无需大量全标注数据。

### 知识库挂载点

本文方法可挂载到以下知识库节点：

1. **草图理解与矢量化管线**：作为预处理步骤，位于笔画提取之后、区域检测或上色之前。输入为自由手绘矢量笔画集合，输出为带预期连接标注的拓扑图结构。可直接嵌入 **LazyBrush**、**Blender Grease Pencil** 等工具的自动区域检测模块上游，大幅减少交互负担。

2. **感知驱动的几何处理**：本文的间隙比 $R_C$ 和增强概率 $P'$ 将格式塔闭合原则形式化为可计算算子，可推广至其他需要模拟人类闭合感知的任务，如不完整轮廓补全、遮挡边界推理等。

3. **小样本学习的几何应用**：31 张部分标注草图的训练规模展示了在几何处理任务中，将领域感知知识（局部几何特征 + 全局闭合原则）编码为模型结构本身，可显著降低对标注数据量的依赖。这一范式对标注成本高的专业设计领域（如建筑草图、工业设计手稿）具有直接迁移价值。

### 适用边界

- **输入假设**：方法设计用于无或最小过绘的矢量草图。对于含有大量过绘、影线或粗糙纹理的草图，预处理阶段的笔画合并与钩子移除能力不足，可能导致分类器输入质量下降。该预处理本身仍是一个开放问题。
- **全自动上限**：尽管用户偏好比达到 9:1，感知研究中仍有 15% 的参与者选择“两者都不”，表明全自动预期连接检测在极端歧义情况下仍未完全解决。
- **闭包因子敏感性**：全局步骤的闭包因子 $C$ 是固定超参数，过小导致间隙比影响不足，过大则产生误报闭合。论文未提供自适应调整 $C$ 的机制，在输入风格差异大时可能需手动调参。
- **高价位连接**：T 型分类器通过复合笔画处理高价位连接，但该策略的有效性依赖于复合笔画构建的启发式规则，在极密集笔画区域可能存在边界情况。

### 后续启发

1. **自适应闭包因子**：探索基于局部或全局绘图特性（如笔画密度、区域大小）动态调整闭包因子 $C$，可进一步提升闭合决策的鲁棒性，减少对固定超参数的依赖。

2. **过绘鲁棒预处理**：开发针对过绘和影线的专用笔画合并与简化模块，扩展本文方法的适用范围至更粗糙的草图风格，是使该方法走向实际创作工具的关键一步。

3. **增量式交互融合**：本文方法已展示从自动输出出发的修正效率优势（2 分钟 vs 31 分钟），将分类器概率作为交互式工具的“建议排序”依据，可进一步降低用户修正的认知负荷。

4. **跨领域迁移**：局部几何特征和全局闭合增强的框架可迁移至其他需要区分“意图间隙”与“意图连接”的领域，如手写体笔画连接、电路草图中的节点识别、以及 3D 草绘中的轮廓闭合等。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Detecting_Viewer_perceived_Intended_Vector_Sketch_Connectivity.pdf]]