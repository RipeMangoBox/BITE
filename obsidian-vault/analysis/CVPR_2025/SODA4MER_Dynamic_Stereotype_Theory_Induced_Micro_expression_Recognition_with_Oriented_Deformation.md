---
title: SODA4MER Dynamic Stereotype Theory Induced Micro expression Recognition with Oriented Deformation
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition_with_Oriented_Deformation.pdf
project_link: null
code_link: null
aliases:
- SDSTIMEROD
tags:
- CVPR_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入自监督定向形变估计器(SODE)结合肌肉群先验的门控时间方差高斯模型(GTVG)增强局部形变感知与抗噪能力，利用对比学习无顶点检测关键帧，并基于动态刻板印象理论的双阶段时间建模(DPTM)分别编码激活期与衰减期动作模式，从而摆脱顶点标注依赖并提升特征表达力。
primary_logic: 将动态刻板印象理论与局部形变估计深度融合：通过对比学习从时序方差中自动检测伪顶点帧，再以双阶段双向LSTM分别建模微表情的激活与衰减过程，同时引入肌肉群先验门控机制过滤无关噪声，实现无顶点标注的鲁棒微表情识别。
claims:
- SODA4MER在SMIC-HS三分类上的UF1（0.8855）和UAR（0.8881）分别超出第二名1.4%和2.4%。
- 消融实验表明，移除GTVG导致UF1下降31.1%、UAR下降28.4%；移除DPTM导致UF1下降32.2%、UAR下降31.9%。
- 自监督预训练对性能至关重要：无预训练时UF1骤降至0.3292，UAR降至0.3405。
- 相比光流，SODE估计的局部形变在极端微表情下噪声更低（如图2定性对比所示）。
---

# SODA4MER Dynamic Stereotype Theory Induced Micro expression Recognition with Oriented Deformation

> [!tip] 核心洞察
> 将动态刻板印象理论与局部形变估计深度融合：通过对比学习从时序方差中自动检测伪顶点帧，再以双阶段双向LSTM分别建模微表情的激活与衰减过程，同时引入肌肉群先验门控机制过滤无关噪声，实现无顶点标注的鲁棒微表情识别。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于动态刻板印象理论的无顶点微表情识别与定向形变建模 |
| 英文题名 | SODA4MER Dynamic Stereotype Theory Induced Micro expression Recognition with Oriented Deformation |
| 会议/期刊 | CVPR 2025 |
| Links |  [paper](https://doi.org/10.1109/CVPR52734.2025.01000)|
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | SODA4MER |
| Dataset | SMIC-HS, CASME II, SAMM |

> [!tip] 效果简介
> - SMIC-HS (3-class) 上，UF1 0.8855 vs Second best (approx 0.8715) (+1.4%)；UAR 0.8881 vs Second best (approx 0.8641) (+2.4%)。
> - CASME II (5-class) 上，UF1 0.8141 vs - (-)；ACC 0.8418 vs - (-)。
> - SAMM (5-class) 上，UF1 0.7893 vs - (-)。

## 概要

**核心问题**：现有微表情识别（MER）方法普遍依赖顶点帧的人工标注，难以建模微弱瞬时动作且对头部运动噪声缺乏鲁棒性；同时，固定面部分区破坏了运动的空间一致性，并忽略了动态刻板印象理论所揭示的时相模式。

**方法定位**：本文提出 **SODA4MER**——一种端到端的无顶点微表情识别框架。其核心思路是将动态刻板印象理论与局部形变估计深度融合：通过自监督定向形变估计器（SODE）捕获关键点级别的细微运动，利用基于肌肉群先验的门控时间方差高斯模型（GTVG）增强局部形变感知与抗噪能力，再以对比学习自动检测伪顶点帧，最终通过双阶段时间建模（DPTM）分别编码激活期与衰减期的时序模式，从而彻底摆脱对顶点标注的依赖。

**主要结果**：在SMIC-HS三分类任务上，SODA4MER的UF1达到0.8855、UAR达到0.8881，分别超出第二名约1.4%和2.4%。消融实验表明，GTVG和DPTM模块各自贡献超过30%的性能增益，自监督预训练更是不可或缺的基础。定性分析（Figure 2）显示，相比传统光流，SODE估计的局部形变在极端微表情下噪声更低、鲁棒性更强。

**方法谱系与知识库定位**：SODA4MER属于**无顶点标注的深度微表情识别**路线，区别于依赖顶点帧的传统方法（如OFF-ApexNet, Gan et al., 2019；STSTNet, Liong et al., FG 2019）和基于光流的手工特征方法（LBP-TOP、MDMO）。与同期自监督方法（如FRL-DGT, Zhai et al., CVPR 2023；SelfME, Fan et al., CVPR 2023）相比，SODA4MER的独特之处在于引入了动态刻板印象理论指导的双阶段时序建模和肌肉群先验的门控机制，而非单纯依赖Transformer或全局运动特征。



微表情（Micro-Expression, ME）是一种持续时间极短（通常 1/25 至 1/3 秒）、强度微弱且难以自主控制的面部运动，在测谎、临床诊断、安全审讯等场景中具有重要应用价值。然而，微表情的自动识别面临一系列根本性挑战：动作幅度极小、帧间变化几乎不可见，且极易受到头部运动、光照变化等无关噪声的干扰。

**现有方法的核心瓶颈**。传统微表情识别方法大致可分为手工特征方法和深度学习方法两类。手工特征方法如 **LBP-TOP** 和 **MDMO** 依赖光流直方图或时空纹理描述子，但对微弱瞬时动作的建模能力有限。深度学习方法如 **OFF-ApexNet**（Gan et al., Signal Process. Image Commun. 2019）和 **STSTNet**（Liong et al., FG 2019）虽然通过双流网络或 3D CNN 提升了识别精度，却普遍存在一个关键局限：**训练和推理均依赖人工标注的顶点帧（apex frame）**。顶点帧是微表情序列中情绪强度最高的帧，其标注需要专业培训的编码员逐帧判断，耗时且主观，在实际应用中往往不可获取——尤其当视频经过重采样或压缩后，顶点帧的位置信息可能完全丢失（见 Figure 1）。

此外，现有方法在运动建模上多采用**光流**捕捉帧间差异，但光流在极端微表情下容易引入噪声，且难以区分由表情肌肉运动引起的形变与头部刚体运动带来的伪影（Figure 2 定性对比显示，光流在微表情场景下噪声显著，而本文提出的局部形变估计则表现出更强的鲁棒性）。在时间动态建模方面，主流方法或仅使用顶点帧进行单帧分类，或将全序列等长输入，**完全忽略了微表情的时相结构**——即激活期（onset→apex）与衰减期（apex→offset）具有不同的运动学特征，这一现象已被心理学中的**动态刻板印象理论（Dynamic Stereotype Theory, DST）**所揭示，但在现有 MER 方法中鲜有建模。

**本文动机与核心思路**。针对上述缺口，SODA4MER 提出了一条摆脱顶点标注依赖、深度融合动态刻板印象理论与局部形变估计的技术路线。具体而言：
- 通过**自监督定向形变估计器（SODE）**在大规模面部动画数据上预训练，学习从源帧和驱动帧重建目标帧的能力，从而获得对局部形变（关键点位移 + 雅可比矩阵）的精确捕捉，替代噪声较大的光流估计。
- 引入**门控时间方差高斯模型（GTVG）**，将时序方差、人脸关键点肌肉群先验与可学习门控系数相结合，动态增强微表情相关区域的形变响应，同时抑制头部运动等无关噪声。
- 利用**对比学习三元组损失**自动检测伪顶点帧（A_det），完全摆脱人工顶点标注。
- 基于动态刻板印象理论设计**双阶段时间建模（DPTM）**，将序列切分为激活期与衰减期，分别通过双向 LSTM 提取时序模式，从而显式编码微表情的时相动态。

这一设计使得 SODA4MER 在无顶点标注的条件下，仍能取得超越依赖顶点帧方法的识别精度，为实用化微表情识别系统提供了新的可能性。



## 核心方法与创新机理

SODA4MER 的核心创新在于将动态刻板印象理论与局部形变估计深度融合，通过四个关键“changed slots”系统性地解决了现有微表情识别（MER）方法对顶点帧人工标注的依赖，以及微弱瞬时动作建模与头部运动噪声鲁棒性不足的瓶颈。

### 创新点一：从光流到局部形变估计 —— 自监督定向形变估计器（SODE）

传统方法普遍依赖光流或手工 MBH 特征来捕捉帧间运动，但光流在极端微表情下噪声显著（见 Figure 2 定性对比），且难以刻画面部局部区域的精细形变。SODA4MER 提出 **自监督定向形变估计器（SODE）**，将运动估计从全局光流场转换为基于关键点的局部形变表示。

具体而言，SODE 通过引入一个抽象参考帧 $R$，将源帧到驱动帧的运动分解为 $ \mathcal{T}_{SD} = \mathcal{T}_{SR} \circ \mathcal{T}_{DR}^{-1} $，并在每个关键点处利用一阶泰勒展开近似局部变换：

$$
\mathcal{T}_{XR}(p_k) \approx \mathcal{T}_{XR}(p_k) + J_{p_k} \cdot (p - p_k)
$$

其中 $J_{p_k} = \frac{d}{dp} \mathcal{T}_{XR}(p) \big|_{p = p_k}$ 为局部雅可比矩阵，描述关键点邻域内的形变方向与幅度。每个关键点的运动由位移和雅可比共同表示 $\{ \mathcal{T}_{XR}(p_k), J_{p_k} \}_{k=1}^{K}$（$K=10$），从而在紧凑的表示中保留了丰富的局部变形信息。SODE 通过自监督图像动画任务预训练——从源帧和驱动帧重建目标帧，无需任何微表情标签即可学习面部运动表征。

### 创新点二：从固定分区到肌肉群先验 —— 门控时间方差高斯模型（GTVG）

现有方法常采用固定面部区块划分，破坏了面部运动的空间一致性，且缺乏对微表情相关肌肉区域的针对性增强。SODA4MER 提出 **门控时间方差高斯模型（GTVG）**，将三类信息有机融合：

1. **时间方差** $\Delta_{\mathrm{var}} = \frac{1}{T} \sum_{t=1}^{T} (F_{t} - \bar{F})^{2}$：突出序列中随时间发生显著变化的区域；
2. **肌肉群先验** $G_i(x, y) = \exp\left( -\frac{(x - l_{i,x})^{2} + (y - l_{i,y})^{2}}{2\sigma_{i}^{2}} \right)$：以人脸关键点为中心的高斯分布，提供肌肉群位置先验；
3. **可学习门控系数** $g_i$：自适应调节各关键点区域的贡献权重。

最终门控机制为 $GTVG = \Delta_{\mathrm{var}}(x, y) \cdot \sum_{i=1}^{K_l} g_i G_i(x, y)$，动态生成空间掩膜以强化面部变形区域并抑制头部运动等无关噪声。消融实验（Table 4）表明，移除 GTVG 导致 UF1 下降 31.1%、UAR 下降 28.4%，验证了肌肉群先验门控机制的关键作用。

### 创新点三：从顶点帧依赖到对比学习伪顶点检测

传统 MER 方法（如 OFF-ApexNet，Gan et al., Signal Process. Image Commun. 2019）训练和推理均需人工标注的顶点帧（apex），这不仅标注成本高昂，且在视频重采样等实际场景下顶点帧可能丢失（见 Figure 1 对比）。SODA4MER 通过对比学习三元组损失自动检测伪顶点帧 $A_{det}$，彻底摆脱了对人工标注的依赖。

具体地，计算起始帧与终止帧的关键点形变距离 $\mathcal{D}_{po}$ 作为正样本，起始帧与当前帧的距离 $\mathcal{D}_{ne}$ 作为负样本，将位置与形变三元组损失之和最大的帧检测为伪顶点：

$$
A_{det} = \arg\max_t \left( \mathcal{L}_{triplet}^{J} + \mathcal{L}_{triplet}^{P} \right)
$$

值得注意的是，消融实验（Table 5）揭示了一个反直觉的发现：直接使用真实顶点帧作为 $A_{det}$ 反而导致性能显著下降（CASME II UF1 从 0.8962 降至 0.7528），说明强行插入顶点帧会破坏自然的时序模式，而对比学习检测的伪顶点更符合序列的内在动态。

### 创新点四：从单阶段建模到激活-衰减双阶段时间建模（DPTM）

现有方法通常仅使用顶点帧或等长全序列建模，忽略了动态刻板印象理论揭示的微表情时相模式——微表情包含激活期（onset→apex）和衰减期（apex→offset）两个具有不同动态特性的阶段。SODA4MER 提出 **双阶段时间建模（DPTM）**，按检测到的伪顶点 $A_{det}$ 将序列切分为激活期和衰减期，分别通过双向 LSTM 提取时序模式：

$$
\mathcal{F}_{activ} = \mathrm{Bi-LSTM}(\mathcal{T}_{[F_{onset} \cdots A_{det}] R})
$$
$$
\mathcal{F}_{decay} = \mathrm{Bi-LSTM}(\mathcal{T}_{[A_{det} \cdots F_{offset}] R})
$$

两阶段特征拼接后经 MLP 与 SoftMax 输出情绪类别。消融实验（Table 4）表明，移除 DPTM 导致 UF1 下降 32.2%、UAR 下降 31.9%，证明分阶段编码能有效捕获微表情的时序动态差异。

### 创新协同：预训练-精调-检测-建模的端到端闭环

上述四个创新点并非孤立存在，而是形成了紧密协同的闭环：SODE 的自监督预训练为整个系统提供了鲁棒的运动表征基础（无预训练时 UF1 骤降至 0.3292，Table 4）；GTVG 在 SODE 输出的形变特征上进行自适应精调，增强信噪比；对比学习伪顶点检测为 DPTM 提供关键帧切分点；DPTM 则充分利用前序模块的输出完成最终分类。这种端到端的设计使 SODA4MER 在 SMIC-HS 三分类上取得了 UF1 0.8855、UAR 0.8881 的最优性能，分别超出第二名 1.4% 和 2.4%（Table 2）。



SODA4MER 提出了一套端到端的无顶点（apex‑free）微表情识别流程，其核心设计目标是在不依赖人工标注顶点帧的前提下，鲁棒地捕捉微弱、瞬时的面部局部形变，并显式建模微表情的时相动态。整体架构如图 Figure 3 所示，由四个紧密协作的模块串联构成：**自监督定向形变估计器 (SODE)**、**门控时间方差高斯模型 (GTVG)**、**对比学习顶点检测** 以及 **双阶段时间建模 (DPTM)**。

![[assets/figures/papers/paper_list_l20_SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition__motion20/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of the proposed SODA4MER. Given input frame*

### 输入输出流

- **输入**：一段微表情视频序列，包含从起始帧（onset）到终止帧（offset）的 $T$ 帧灰度人脸图像，以及每帧的 $K_l$ 个人脸关键点坐标（$K_l$ 由数据集标注提供）。序列中不含顶点帧标签。
- **逐帧形变提取**：每帧 $X$ 通过 SODE 估计相对于一个抽象参考帧 $R$ 的局部形变 $\mathcal{T}_{X R}$。该形变表示为一组关键点处的位移 $\mathcal{T}_{X R}(p_k)$ 与局部雅可比矩阵 $J_{p_k}$（$k=1,\dots,K$，$K=10$），共同刻画面部各区域的运动幅度与方向。
- **特征精调**：GTVG 模块以逐帧的形变特征和序列时间方差为输入，融合以人脸关键点为中心的高斯先验与可学习门控系数，生成空间自适应掩膜，对形变特征进行加权增强，抑制头部运动等无关噪声。
- **伪顶点检测**：对比学习模块计算起始‑终止帧对与各中间帧在关键点位移和雅可比上的三元组损失，将损失最大的帧自动检测为伪顶点 $A_{det}$，无需任何人工标注。
- **双阶段时序编码**：DPTM 模块以 $A_{det}$ 为界，将 GTVG 精调后的形变序列切分为激活期（onset → $A_{det}$）和衰减期（$A_{det}$ → offset），两组变长序列分别送入两个独立的 Bi‑LSTM，提取空间位置特征 $\mathcal{F}_{activ}$ 和局部形变特征 $\mathcal{F}_{decay}$。
- **分类输出**：拼接激活期与衰减期特征后，经 MLP 和 SoftMax 输出情绪类别概率。训练时采用类别平衡的 focal loss 与两种三元组损失的联合优化。

### 模块间的依赖关系

SODE 是整个流程的前端基础，其自监督预训练使形变估计具备对极端微表情的低噪声表征能力（Figure 2 定性对比了 SODE 局部形变与光流在微弱动作下的噪声差异）。GTVG 在 SODE 输出之上工作，利用肌肉群先验进一步过滤非表情形变，为后续顶点检测和时序建模提供高质量特征。对比学习顶点检测不依赖任何额外标签，仅利用形变序列的时序差异特性定位伪顶点 $A_{det}$；DPTM 则严格依赖 $A_{det}$ 完成双阶段划分，分别编码激活与衰减过程的运动模式。这一串行依赖关系在消融实验中得到了充分验证：移除 GTVG 或 DPTM 任一模块均导致 UF1 下降超过 30%（Table 4），而直接使用真实顶点帧替代 $A_{det}$ 反而造成性能大幅下降（CASME II UF1 从 0.8962 降至 0.7528，Table 5），表明各模块间的协同设计与自然时序模式的保持对最终性能至关重要。

### 与现有流程的本质差异

传统 MER 方法（如 **OFF‑ApexNet** (Gan et al., Signal Process. Image Commun. 2019)、**STSTNet** (Liong et al., FG 2019)）通常依赖人工标注的顶点帧进行训练，且运动估计多采用光流或手工 MBH 特征，对头部运动噪声和极端微表情的鲁棒性不足。SODA4MER 在三个关键环节上实现了根本性改变（Figure 1 对比了两种流程差异）：(1) 以 SODE 的局部雅可比形变替代全局光流，增强局部运动感知与抗噪能力；(2) 以对比学习自动检测伪顶点，彻底摆脱顶点标注依赖，使方法在视频重采样等实际场景中依然可用；(3) 引入基于动态刻板印象理论的双阶段时间建模，显式编码微表情的激活与衰减时相动态，而非简单地对全序列或单帧建模。



SODA4MER 的核心架构由四个紧密协作的模块构成：自监督定向形变估计器（SODE）、门控时间方差高斯模型（GTVG）、对比学习顶点检测以及双阶段时间建模（DPTM）。以下逐一展开各模块的设计逻辑与关键公式。

### 自监督定向形变估计器（SODE）

SODE 是整个方法的基础运动表征模块，其核心思想是将面部运动建模为关键点位移与局部雅可比矩阵的组合，从而捕获微表情中微弱且局部的形变。

**抽象参考帧与形变表示。** 为避免信息泄露，SODE 假设存在一个抽象的参考帧 $R$。对于任意输入帧 $X$，其在关键点 $p_k$ 附近的形变通过一阶泰勒展开近似：

$$
\mathcal{T}_{X R}(p) \approx \mathcal{T}_{X R}(p_k) + J_{p_k} \cdot (p - p_k) \tag{1}
$$

其中 $\mathcal{T}_{X R}(p_k)$ 表示关键点的位移向量，$J_{p_k}$ 为局部雅可比矩阵，定义为：

$$
J_{p_k} = \frac{d}{dp} \mathcal{T}_{X R}(p) \big|_{p = p_k} \tag{2}
$$

雅可比矩阵刻画了关键点邻域内的形变方向与幅度，使得模型能够感知光流难以捕获的微弱局部运动。每个关键点的运动由位移和雅可比共同表示：

$$
\{ \mathcal{T}_{X R}(p_k), J_{p_k} \}_{k=1}^{K} \tag{3}
$$

其中 $K=10$ 为关键点数量。

**帧间运动合成。** 给定源帧 $S$ 和驱动帧 $D$，二者之间的运动通过抽象参考帧 $R$ 的组合得到：

$$
\mathcal{T}_{S D} = \mathcal{T}_{S R} \circ \mathcal{T}_{D R}^{-1} \tag{4}
$$

最终的运动场由背景掩膜 $M_0$ 和各关键点独立变换区域加权求和得到：

$$
\hat{\mathcal{T}}_{S D}(z) = M_0 z + \sum_{k=1}^{K} M_k \cdot \mathcal{T}_k(z) \tag{5}
$$

其中每个关键点负责的区域变换为：

$$
\mathcal{T}_k(z) = \mathcal{T}_{S R}(p_k) + J_k (z - \mathcal{T}_{D R}(p_k)) \tag{6}
$$

SODE 通过自监督图像动画任务预训练：以源帧和驱动帧的形变信息重建目标帧，利用感知损失（VGG 特征空间的 L2 距离）约束重建质量，使模型学会提取与面部运动相关的形变表征。

### 门控时间方差高斯模型（GTVG）

GTVG 旨在增强模型对微表情相关区域的感知能力，同时抑制头部运动等无关噪声。该模块融合了三类信息：时序方差、面部关键点先验与可学习门控系数。

**时序方差。** 首先计算序列中每个像素位置的时间方差，以突出随时间发生显著变化的区域：

$$
\Delta_{\mathrm{var}} = \frac{1}{T} \sum_{t=1}^{T} \left( F_{t} - \bar{F} \right)^{2} \tag{7}
$$

**关键点高斯先验。** 以人脸关键点为中心构建参数化高斯分布，提供肌肉群位置的结构先验：

$$
G_i(x, y) = \exp\left( -\frac{(x - l_{i,x})^{2} + (y - l_{i,y})^{2}}{2\sigma_{i}^{2}} \right) \tag{8}
$$

其中 $\sigma_i$ 为可学习参数，控制每个关键点的影响范围。

**门控融合。** GTVG 将时序方差与加权关键点先验逐元素相乘，形成自适应空间掩膜：

$$
GTVG = \Delta_{\mathrm{var}}(x, y) \cdot \sum_{i=1}^{K_l} g_i G_i(x, y) \tag{9}
$$

其中 $g_i$ 为可学习的门控系数，允许模型动态调整各肌肉群区域的贡献权重。该掩膜直接作用于 SODE 提取的形变特征，强化与微表情相关的面部区域，同时抑制背景和头部运动噪声。消融实验表明，移除 GTVG 导致 UF1 下降 31.1%、UAR 下降 28.4%（Table 4），验证了肌肉群先验门控机制的关键作用。

### 对比学习顶点检测

为摆脱对人工标注顶点帧的依赖，SODA4MER 采用对比学习策略自动检测伪顶点 $A_{det}$。

核心思想是：起始帧（onset）与终止帧（offset）之间的形变差异构成“正样本对”，起始帧与当前帧的形变差异构成“负样本对”。通过三元组损失最大化正负样本距离差，将损失最大的帧检测为伪顶点。

正样本距离定义为起始帧与终止帧在关键点形变上的 L2 距离：

$$
\mathcal{D}_{po} = \sum_{k}^{K} \| \mathcal{T}_{F_0 R}(p_k) - \mathcal{T}_{F_T R}(p_k) \|_2 \tag{10}
$$

负样本距离为起始帧与当前帧的关键点形变距离：

$$
\mathcal{D}_{ne} = \sum_{k}^{K} \| \mathcal{T}_{F_0 R}(p_k) - \mathcal{T}_{F_t R}(p_k) \|_2 \tag{11}
$$

伪顶点 $A_{det}$ 为位置三元组损失与形变三元组损失之和最大的帧：

$$
A_{det} = \arg\max_t \left( \mathcal{L}_{triplet}^{J} + \mathcal{L}_{triplet}^{P} \right) \tag{12}
$$

该方法无需人工标注，且对视频重采样具有鲁棒性（Figure 1a）。

### 双阶段时间建模（DPTM）

DPTM 基于动态刻板印象理论（Dynamic Stereotype Theory），将微表情序列按伪顶点 $A_{det}$ 切分为激活期（onset → $A_{det}$）和衰减期（$A_{det}$ → offset），分别提取时序模式。

激活期特征通过双向 LSTM 编码从起始帧到伪顶点的形变序列：

$$
\mathcal{F}_{activ} = \mathrm{Bi-LSTM}(\mathcal{T}_{[F_{onset} \cdots A_{det}] R}) \tag{13}
$$

衰减期特征编码从伪顶点到终止帧的形变序列：

$$
\mathcal{F}_{decay} = \mathrm{Bi-LSTM}(\mathcal{T}_{[A_{det} \cdots F_{offset}] R}) \tag{14}
$$

两个 Bi-LSTM 分别处理关键点的空间位置特征和局部形变特征，最终拼接激活与衰减期特征，通过 MLP 和 SoftMax 输出情绪类别概率。消融实验表明，移除 DPTM 导致 UF1 下降 32.2%、UAR 下降 31.9%（Table 4），证实双阶段建模能有效编码微表情的时序动态。

### 损失函数

自监督预训练阶段采用感知损失约束重建帧与目标帧的结构相似性：

$$
\mathcal{L}_{perceptual} = \| \mathrm{VGG}(\hat{D}) - \mathrm{VGG}(D) \|_2 \tag{15}
$$

端到端微表情识别阶段的总损失由三部分组成：类别平衡的 Focal Loss（缓解类别不均衡）与两种三元组损失：

$$
\mathcal{L}_{MER} = \mathcal{L}_{focal} + \mathcal{L}_{triplet}^{J} + \mathcal{L}_{triplet}^{P}
$$

其中 Focal Loss 定义为 $\mathcal{L}_{focal} = -\beta (1 - \mathcal{P}_c)^2 \log(\mathcal{P}_c)$，通过降低高置信度样本的损失权重来应对微表情数据集的类别不均衡问题。

### 补充图表

![[assets/figures/papers/paper_list_l20_SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition__motion20/figures/001_Figure_1.jpg]]
*Figure 1: (a) Difference in method pipeline: Previous MER methods typically rely on the apex annotations. Our method detects the apex frame through a triplet loss in contrastive learning, allowing for the detection of Adet even in resampled sequences. Additionally, the local motion estimated by our method demonstrates strong noise resistance. (b) Difference in practicality: Previous MER methods rely on apex annotations, making them unsuitable for practical applications when apex labels are unavailable or lost due to video resampling*

![[assets/figures/papers/paper_list_l20_SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition__motion20/figures/002_Figure_2.jpg]]
*Figure 2: The subtle facial movements are highlighted with red boxes: (a) Onset frames, the starting frames of MEs. (b) Apex frames, the frames showing the highest intensity. (c) Optical flow between onset and apex frames. (d) Local deformation estimated by our method. The optical flow adequately captures facial movements but introduces noise and struggles with extreme MEs. In contrast, our method addresses these challenges more robustly*



## 实验与关键发现

### 数据集与实验设置

SODA4MER在三个标准微表情数据集上进行评估：SMIC-HS、CASME II和SAMM。Table 1给出了各数据集的样本分布统计，其中“→”表示少量样本被丢弃，“-”表示该数据集不包含对应微表情类别。所有实验均采用留一被试交叉验证（LOSO）协议，使用标准数据预处理流程（人脸检测、对齐、统一尺寸），对比方法均采用原论文推荐的最优超参数或已公开的代码实现，确保评估的公平性。

### 三分类主实验结果

Table 2报告了在CASME II和SMIC-HS上的三分类对比结果。SODA4MER在SMIC-HS上取得了0.8855的UF1和0.8881的UAR，分别超出第二名约1.4%和2.4%，验证了无顶点标注方案的有效性。在CASME II上，SODA4MER同样保持竞争力。对比方法覆盖了从经典手工特征方法**LBP-TOP**、基于光流直方图的**MDMO**，到依赖顶点帧的深度方法**OFF-ApexNet**（Gan et al., 2019）、浅层三流3D CNN的**STSTNet**（Liong et al., FG 2019），以及最新的自监督方法**FRL-DGT**（Zhai et al., CVPR 2023）和**SelfME**（Fan et al., CVPR 2023）。SODA4MER在摆脱顶点标注依赖的同时仍取得领先性能，其核心优势在于：SODE估计的局部形变对极端微表情的噪声鲁棒性更强（Figure 2定性对比），DPTM基于动态刻板印象理论的双阶段建模能更有效地编码微表情的激活与衰减时序模式。

### 五分类主实验结果

Table 3进一步展示了五分类对比评估结果。在CASME II上，SODA4MER取得UF1 0.8141和ACC 0.8418；在SAMM上取得UF1 0.7893和ACC 0.8030。五分类任务中类别不均衡问题更为突出（如“恐惧”和“悲伤”样本稀少），SODA4MER通过类别平衡的focal loss和GTVG对肌肉群区域的聚焦能力，在多数类别上保持了稳定的识别性能。

### 消融实验

Table 4的消融实验揭示了各核心组件的重要性：

- **GTVG模块**：移除GTVG后，UF1下降31.1%、UAR下降28.4%，证明肌肉群先验的门控机制对增强局部形变感知和抑制头部运动噪声至关重要。GTVG通过融合时序方差、人脸关键点高斯先验和可学习门控系数$g_i$，自适应地生成空间掩膜以强化微表情相关区域。
- **DPTM模块**：移除DPTM后，UF1下降32.2%、UAR下降31.9%，表明基于动态刻板印象理论的双阶段时间建模能有效编码微表情的激活期与衰减期动态模式。若仅使用等长全序列建模，模型无法区分不同时相的运动特征差异。
- **自监督预训练**：无预训练时UF1骤降至0.3292、UAR降至0.3405，说明在大规模面部动画数据上的SODE预训练是模型性能的基础保障。预训练使SODE学会从抽象参考帧R出发估计局部形变，为下游微表情识别提供了高质量的运动表示。

### 顶点帧与大规模数据集消融

Table 5进一步分析了伪顶点检测和额外数据的影响：

- **伪顶点 vs 真实顶点**：直接使用真实顶点帧（GT apex）作为$A_{det}$反而导致性能下降（CASME II UF1从0.8962降至0.7528）。这揭示了一个反直觉的发现：强行插入真实顶点帧会破坏微表情序列自然的时序连续性，而对比学习检测的伪顶点$A_{det}$与动态刻板印象理论的时相划分更为契合。
- **大规模数据集预训练**：引入CASME3数据集进行预训练后性能反而下降（CASME II UF1从0.8962降至0.7825），说明微表情样本分布差异会对模型造成负面影响。CASME3与CASME II在采集环境、被试人群和情绪诱发方式上的差异，使得直接迁移预训练权重反而引入了领域偏移。

### 失败模式与局限性

Figure 4展示了SODA4MER的定性分析及失败案例。局部形变估计虽能有效捕捉微表情运动，但仍存在以下局限：

1. **非表情形变噪声**：SODE估计的局部形变仍不能完全消除与微表情无关的形变噪声（如图4d中仍存在非表情相关的形变），部分头部运动或眨眼动作可能被误判为微表情信号。
2. **超参数敏感性**：方法对GTVG的门控系数初始化和DPTM的阶段划分阈值较为敏感，目前缺乏自动化的超参数搜索机制，需依靠经验调参。
3. **极短微表情的检测精度**：双阶段建模依赖对比学习检测的伪顶点，对于持续时间极短（如少于10帧）的微表情，三元组损失可能无法准确定位$A_{det}$，进而影响后续分类性能。
4. **跨域泛化不足**：当面对样本分布差异显著的极大规模数据集（如CASME3）时，模型性能可能下降，说明当前预训练策略对分布偏移的鲁棒性有待加强。

### 补充图表

![[assets/figures/papers/paper_list_l20_SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition__motion20/figures/005_Table_2.jpg]]
*Table 2: Comparison with the state-of-the-art methods on CASME II and SMIC-HS for three-categories classification task. The best results are highlighted in bold, while the second-best results are marked with an underline*

![[assets/figures/papers/paper_list_l20_SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition__motion20/figures/008_Table_4.jpg]]
*Table 4: Ablation study of key components of SODA4MER*

![[assets/figures/papers/paper_list_l20_SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition__motion20/figures/007_Table_3.jpg]]
*Table 3: To conduct more convincing experiments, we further performed a five-class comparative evaluation on CASME II and SAMM*

![[assets/figures/papers/paper_list_l20_SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition__motion20/figures/009_Table_5.jpg]]
*Table 5: Ablation study of apex frame and large-scale ME dataset*

![[assets/figures/papers/paper_list_l20_SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition__motion20/figures/004_Table_1.jpg]]
*Table 1: Distribution of ME samples, ’→’ indicates that a few ME samples were discarded, while ’-’ denotes the corresponding database does not contain this ME category*

![[assets/figures/papers/paper_list_l20_SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition__motion20/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative analysis and failure cases of SODA4MER*



## 定位与知识库关联

### 1. 方法定位与核心差异

SODA4MER 的核心定位是**无顶点标注的微表情识别**，其设计逻辑与现有方法存在三个根本性差异：

**顶点帧依赖的消除**。传统深度方法如 **OFF-ApexNet**（Gan et al., Signal Process. Image Commun. 2019）、**STSTNet**（Liong et al., FG 2019）均依赖人工标注的顶点帧（apex frame）进行训练和推理。SODA4MER 通过对比学习三元组损失自动检测伪顶点帧 $A_{det}$，使方法在视频重采样导致顶点帧丢失的场景下仍可正常工作（Figure 1a），从根本上摆脱了对昂贵人工标注的依赖。

**运动估计范式的转变**。主流方法普遍采用光流作为运动表征，如 **MDMO** 基于光流直方图，**OFF-ApexNet** 使用光流双流网络。然而光流在极端微表情下噪声显著（Figure 2c），且难以捕捉局部微小形变。SODA4MER 提出自监督定向形变估计器（SODE），通过关键点雅可比矩阵 $J_{p_k}$ 建模局部形变的方向与幅度，在噪声鲁棒性上明显优于光流（Figure 2d）。

**时间动态的差异化建模**。现有方法通常仅使用顶点帧或等长全序列进行特征提取，忽略了微表情的时相动态。SODA4MER 引入动态刻板印象理论（Dynamic Stereotype Theory），将序列切分为激活期（onset→$A_{det}$）和衰减期（$A_{det}$→offset），分别通过两个 Bi-LSTM 编码，使模型能够显式捕捉微表情从产生到消退的完整动态过程。

### 2. 与同期自监督方法的对比

SODA4MER 与两类代表性自监督方法存在显著区别：

- **FRL-DGT**（Zhai et al., CVPR 2023）：采用自监督位移生成与 Transformer 融合，但仍需顶点帧作为位移生成的目标。SODA4MER 的 SODE 通过抽象参考帧 $R$ 的组合变换 $\mathcal{T}_{SD} = \mathcal{T}_{SR} \circ \mathcal{T}_{DR}^{-1}$ 实现完全无顶点的形变估计，且引入肌肉群先验的门控机制（GTVG）增强局部形变感知。

- **SelfME**（Fan et al., CVPR 2023）：自监督运动学习方法，侧重于运动特征的学习范式。SODA4MER 在此基础上进一步引入动态刻板印象理论指导的双阶段时间建模（DPTM），将时间结构先验融入端到端学习，在 SMIC-HS 三分类上 UF1（0.8855）和 UAR（0.8881）分别超出第二名 1.4% 和 2.4%（Table 2）。

### 3. 适用边界

**适用场景**：
- 无顶点标注或顶点帧丢失的微表情识别任务
- 存在头部运动噪声的野外场景（GTVG 的门控机制可抑制无关区域噪声）
- 需要捕捉激活-衰减完整动态的细粒度情绪分析

**不适用或需谨慎使用的场景**：
- 持续时间极短的微表情（<100ms）：伪顶点检测精度可能不足，影响双阶段建模效果（Table 5 显示 $A_{det}$ 与真实顶点存在时间偏差 $\Delta_A$）
- 样本分布差异显著的跨数据集场景：在 CASME3 上预训练后性能反降（CASME II UF1 从 0.8962 降至 0.7825，Table 5），说明模型对数据分布偏移敏感
- 嵌入式或实时性要求极高的场景：当前推理速度 64 FPS，模型复杂度仍有优化空间

### 4. 关键局限与失败模式

**局部形变估计的残余噪声**。尽管 SODE 在噪声抑制上优于光流，但 Figure 4d 显示仍存在与微表情无关的形变区域，说明 GTVG 的肌肉群先验未能完全过滤所有非表情形变，在复杂背景或大幅度头部运动下可能产生误检。

**真实顶点帧的“性能悖论”**。消融实验揭示了一个反直觉现象：直接使用人工标注的真实顶点帧替换 $A_{det}$ 会导致性能显著下降（CASME II UF1 从 0.8962 降至 0.7528，Table 5）。这表明强行插入顶点帧会破坏序列的自然时序连续性，DPTM 的双阶段建模更适合从连续形变中学习，而非依赖离散的关键帧。

**超参数敏感性**。方法对超参数较为敏感，目前缺乏自动化的超参数搜索机制，需依靠经验调参，这限制了在不同数据集上的快速部署能力。

**大规模数据利用的困境**。引入 CASME3 大规模数据集预训练后性能反降，说明简单的数据堆叠无法解决分布偏移问题，需要设计对分布偏移鲁棒的预训练策略。

### 5. 开放问题

1. **激活与衰减的神经动力学基础**：动态刻板印象理论提供了时相划分的心理学依据，但激活期与衰减期的底层神经动力学差异及其对识别的作用机制尚未完全明晰。能否通过更精细的生理模型（如面部动作单元 AU 的时序模式）指导建模，是提升可解释性的关键方向。

2. **跨域泛化的预训练策略**：当前模型对数据分布偏移敏感，如何设计域不变的自监督预训练任务，以有效利用大规模未标注微表情数据（如 CASME3、MMEW），是突破性能瓶颈的潜在路径。

3. **多模态知识融合**：能否联合面部动作单元（AU）检测或宏观表情知识，进一步提升模型的可解释性和跨域泛化能力？GLEFFN（Guo and Huang, FME Workshop 2023）等事件融合方法提供了多模态融合的思路，但如何与无顶点框架深度结合仍需探索。

4. **模型轻量化与实时部署**：当前 64 FPS 的推理速度在多数场景下可满足实时性要求，但面向嵌入式设备仍需进一步降低模型复杂度。如何在保持 GTVG 和 DPTM 核心机制的前提下实现高效推理，是工程落地的重要挑战。



## 原文 PDF

![[paperPDFs/CVPR_2025/SODA4MER_Dynamic_Stereotype_Theory_Induced_Micro_expression_Recognition_with_Oriented_Deformation.pdf]]
