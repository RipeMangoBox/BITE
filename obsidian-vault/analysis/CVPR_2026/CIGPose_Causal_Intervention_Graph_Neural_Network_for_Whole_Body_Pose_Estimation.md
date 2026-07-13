---
title: "CIGPose: Causal Intervention Graph Neural Network for Whole-Body Pose Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CIGPose_Causal_Intervention_Graph_Neural_Network_for_Whole_Body_Pose_Estimation.pdf
project_link: null
code_link: "https://github.com/53mins/CIGPose"
aliases:
- CIGPose
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 因果干预模块（CIM）通过预测不确定性识别混淆关键点嵌入，并用学习的、上下文不变的标准嵌入进行反事实替换，阻断非因果后门路径。
primary_logic: 预测不确定性是视觉混淆的有效代理，反事实替换可实现去混淆，使模型基于可靠因果证据推理，同时分层图神经网络在净化后的嵌入上强化解剖一致性。
claims:
- CIGPose-x在COCO-WholeBody上仅用COCO-WholeBody数据达到67.0% AP，超过依赖额外UBody数据的DWPose-l（66.5% AP）及直接基线RTMPose-x（65.3% AP）。
- 在完整分层GNN基础上加入CIM额外提升0.2 AP（67.0 vs 66.8），总提升1.7 AP over baseline，显示去混淆和结构推理的协同作用。
- 预测不确定性分数在遮挡关键点上显著更高，验证了其作为混淆代理的有效性。
- COCO-WholeBody 上 Whole-Body AP = 67.0 (CIGPose-x)
---

# CIGPose: Causal Intervention Graph Neural Network for Whole-Body Pose Estimation

> [!tip] 核心洞察
> 预测不确定性是视觉混淆的有效代理，反事实替换可实现去混淆，使模型基于可靠因果证据推理，同时分层图神经网络在净化后的嵌入上强化解剖一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CIGPose：面向全身姿态估计的因果干预图神经网络 |
| 英文题名 | CIGPose: Causal Intervention Graph Neural Network for Whole-Body Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.09418) · [Code](https://github.com/53mins/CIGPose) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CIGPose |
| Dataset | COCO-WholeBody, COCO-WholeBody + UBody, COCO val2017, CrowdPose |

> [!tip] 效果简介
> - COCO-WholeBody 上，Whole-Body AP 67.0 (CIGPose-x) vs 65.3 (RTMPose-x) / 66.5 (DWPose-l*) (+1.7 / +0.5)。
> - COCO-WholeBody + UBody 上，Whole-Body AP 67.5 (CIGPose-x + UBody) vs 66.5 (DWPose-l*) (+1.0)。
> - COCO val2017 上，AP 78.5 (CIGPose-l†) vs 77.3 (RTMPose-l†) (+1.2)。

## 概要

全身姿态估计需要在单张图像中同时定位身体、手部、面部和脚部的密集关键点，但现有方法普遍面临一个核心瓶颈：模型从视觉上下文中学习到**虚假相关性**，导致在遮挡、杂乱等复杂场景下生成违反解剖结构的姿态估计。例如，模型可能将遮挡的手部关键点错误地关联到附近的物体边缘，而非依据人体运动学约束进行推理。

针对这一问题，本文提出 **CIGPose**——一种面向全身姿态估计的因果干预图神经网络。其核心思路是将姿态估计建模为因果推理问题：视觉特征（F）与姿态（Y）之间存在由混淆因子（C）开启的非因果后门路径，直接使用观测特征进行预测会引入偏差。CIGPose通过**因果干预模块（CIM）**阻断这一后门路径：首先利用预测不确定性作为视觉混淆的有效代理，识别出被混淆的关键点嵌入，然后用学习到的、上下文不变的标准嵌入进行反事实替换，从而获得去混淆的嵌入表示。随后，一个**分层图神经网络**在净化后的嵌入上进行局部运动学建模和全局语义超图推理，强化解剖一致性。

实验表明，CIGPose-x在COCO-WholeBody上仅使用该数据集训练即达到**67.0% AP**，不仅超越直接基线RTMPose-x（65.3% AP，提升+1.7），还超过了依赖额外UBody数据的DWPose-l（66.5% AP）。在CrowdPose拥挤场景数据集上，CIGPose-l达到73.7% AP，较HRFormer-B提升+1.3。消融实验验证了CIM与分层GNN的协同作用：在完整分层GNN基础上加入CIM额外带来0.2 AP提升，而反事实一致性损失对学习有意义的标准嵌入至关重要。

在方法谱系上，CIGPose属于**结合因果推理与结构化预测的姿态估计方法**，其因果干预机制区别于传统的注意力机制或纯数据驱动的结构建模。代码已开源（https://github.com/53mins/CIGPose）。



### 问题背景

全身姿态估计（whole-body pose estimation）要求同时定位人体、手部、面部和足部的密集关键点，是行为识别、人机交互和虚拟现实等应用的基础技术。近年来，基于深度学习的回归方法取得了显著进展，但在遮挡、背景杂乱、复杂姿态等真实场景中，模型仍频繁产生违反人体解剖结构的预测——例如手部关键点穿越身体、足部位置与躯干方向矛盾等。

这些错误的根源并非模型容量不足，而是一个更深层的因果问题：模型从视觉上下文中学习到**虚假相关性（spurious correlations）**。例如，当“手腕靠近腰部”这一视觉模式频繁与“手放在背后”同时出现时，模型可能将背景纹理或邻近身体部件的共现当作决策捷径，而非依据关键点本身的视觉证据进行推理。在因果推断框架下，视觉上下文充当了**混淆因子（confounder）**，它同时影响输入特征和输出姿态，打开了非因果的后门路径（backdoor path）$F \leftarrow C \rightarrow Y$，使得观测分布 $P(Y|F)$ 与真正的因果效应 $P(Y|do(F))$ 产生系统性偏差。

### 现有方法的缺口

主流姿态估计方法可归为两类范式，但均未从根本上解决混淆问题：

**基于热图回归的方法**（如HRNet、HigherHRNet）通过高分辨率特征图保持空间精度，但其感受野天然耦合了目标关键点与周围上下文，无法区分因果证据与混淆信号。**基于图神经网络的结构推理方法**（如MPGD、Graph-PCNN）在关键点嵌入之上显式建模人体骨架约束，试图抑制解剖学上不合理的预测。然而，这些方法在**已被混淆的嵌入**上进行结构推理——当关键点嵌入本身携带了来自遮挡物、杂乱背景或错误关联的虚假信息时，图网络非但无法纠正错误，反而可能将局部混淆传播至全局，产生整体性姿态坍塌。

近期工作如**DWPose**通过两阶段蒸馏和额外的大规模UBody数据集提升鲁棒性，但这类数据驱动策略本质上是在观测分布内拟合更复杂的边界，并未切断混淆路径。一旦测试分布与训练分布存在偏移，虚假相关性依然会被激活。

### 本文动机

本文的核心动机是：**在结构推理之前，先对关键点嵌入进行因果去混淆（causal deconfounding）**。具体而言，我们提出CIGPose，其核心是一个**因果干预模块（Causal Intervention Module, CIM）**。该模块受后门调整公式 $P(Y|do(F)) = \sum_c P(Y|F,c) P(c)$ 的启发，但避免了对不可观测混淆因子 $c$ 的显式建模。CIM的关键洞察是：**预测不确定性（predictive uncertainty）可以作为视觉混淆的有效代理**——当关键点被遮挡、模糊或与背景混杂时，模型对其位置的预测分布趋于平坦，峰值置信度降低。基于此，CIM自动识别高不确定性的“混淆关键点嵌入”，并用可学习的、上下文不变的标准嵌入（canonical embeddings）进行反事实替换（counterfactual replacement），从而阻断后门路径。

在去混淆嵌入之上，我们进一步引入**分层图神经网络（Hierarchical GNN）**：局部EdgeConv建模运动学约束，全局超图注意力捕捉远距离语义依赖（如“左手与右手属于同一人体”），在净化后的证据上强化全局解剖一致性。整个框架在训练时通过**反事实一致性损失**约束干预不改变可靠关键点的预测，确保标准嵌入学习到有意义的解剖先验而非随意替换。

通过“先干预、后推理”的设计，CIGPose在COCO-WholeBody上仅用标准训练数据即达到67.0% AP，超越了依赖额外UBody数据的DWPose-l（66.5% AP），并在CrowdPose等遮挡密集场景下展现出一致的鲁棒性提升。



## 核心方法与创新机理

CIGPose 的核心创新在于将**因果干预**引入姿态估计流程，解决模型从视觉上下文中学习到虚假相关性的瓶颈问题。具体而言，它通过两个关键槽位的改动，将标准的关键点回归管线转化为一个去混淆的因果推理框架。

### 从观测路径到反事实干预路径

传统姿态估计模型（如 RTMPose）的流程是：编码器输出原始关键点嵌入 $F$，直接送入预测头生成关键点坐标（观测路径 $P(Y|F)$）。这一路径在遮挡、杂乱等复杂场景下容易受到视觉混淆因子的影响，产生不符合解剖结构的预测。

CIGPose 将这一流程重构为**反事实干预路径** $P(Y|do(F))$：

1. **因果干预模块（CIM）** 首先介入：它基于预测不确定性计算每个关键点的混淆分数 $s_c(k) = 1 - \frac{1}{2}(\max(P_{k,x}) + \max(P_{k,y}))$，识别出最易受混淆影响的 top-n 个关键点嵌入，并用学习到的、上下文不变的标准嵌入 $z_k$ 进行反事实替换。这一操作在理论上近似了后门调整公式 $P(Y|do(F)) = \sum_c P(Y|F,c)P(c)$，通过切断非因果后门路径来消除混淆影响。

2. **分层图神经网络** 在去混淆后的嵌入上执行结构推理：先通过局部 EdgeConv 建模运动学约束，再通过全局超图注意力捕捉长程语义依赖（如左右对称、身体部位协同），最终强化解剖一致性。

### 关键设计选择

- **不确定性作为混淆代理**：Figure 3 验证了遮挡关键点的混淆分数显著高于可见关键点，证明预测不确定性是视觉混淆的有效代理，使模型无需显式标注混淆因子即可识别需要干预的位置。
- **反事实一致性正则**：通过约束稳定关键点的观测预测与干预预测一致（$\mathcal{L}_{cf}$），防止过度干预并确保标准嵌入学到有意义的、上下文不变的表示。消融实验表明，移除该损失导致 0.5 AP 下降（Table 8）。
- **固定预算 top-n 策略**：采用固定数量（n=13，约 10% 关键点）的干预策略，相比阈值策略提供更稳定的训练信号（Table 9）。干预频率最高的部位是脚、手和腿——这些末端部位最易受遮挡和模糊影响（Table 7）。

### 创新协同效应

消融实验（Table 4）揭示了两个创新槽位的协同关系：在完整分层 GNN 基础上单独引入 CIM，额外提升 0.2 AP（67.0 vs. 66.8），而两者叠加相对于基线 RTMPose-x 的总提升达 1.7 AP。这表明**去混淆为结构推理提供了更干净的特征基础，而结构推理反过来放大了去混淆的收益**——两者并非简单叠加，而是相互增强。



CIGPose 的整体架构遵循“编码—去混淆—结构推理—预测”四阶段流水线，其核心设计目标是在结构推理之前阻断视觉上下文引入的虚假相关性，使后续图神经网络在净化后的嵌入上进行解剖一致性建模。Figure 5 给出了完整的架构概览。

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/005_Figure_5.jpg]]
*Figure 5: Overview of our CIGPose architecture. During training, embeddings are processed in two paths: (1) a counterfactual path where our CIM module deconfounds them before the Hierarchical GNN, and (2) an observational path using original embeddings for consistency. Inference relies solely on the counterfactual path*

**双路径训练，单路径推理。** 训练时，关键点嵌入沿两条路径流动：
1. **反事实路径（counterfactual path）**：嵌入先经过因果干预模块（CIM）进行去混淆，再送入分层图神经网络（Hierarchical GNN）进行结构推理，最终产生预测分布 $P(Y_k | do(F))$。
2. **观测路径（observational path）**：原始嵌入直接用于计算反事实一致性损失 $\mathcal{L}_{cf}$，约束干预不改变可靠关键点的预测，防止过度干预。

推理时仅使用反事实路径，无需观测路径的前向计算。

**模块串联关系。** 流水线由四个核心模块依次构成：

1. **关键点编码器（Keypoint Encoder）**：采用 CSP-NeXt 骨干网络配合 GAU 注意力单元（基于 RTMPose 架构），从输入图像中提取 $K$ 个关键点的初始嵌入 $\{f_k\}_{k=1}^K$。这些嵌入携带丰富的视觉上下文信息，但也可能被遮挡、杂乱背景等混淆因子污染。

2. **因果干预模块（Causal Intervention Module, CIM）**：这是整个框架的去混淆核心。CIM 首先利用预测不确定性作为视觉混淆的代理，计算每个关键点的混淆分数 $s_c(k)$：
   $$s_c(k) = 1 - \frac{1}{2}\big(\max(P_{k,x}) + \max(P_{k,y})\big)$$
   其中 $P_{k,x}$、$P_{k,y}$ 为关键点 $k$ 在 $x$、$y$ 方向上的预测概率分布。分数越高，表示模型对该关键点的预测越不确定，越可能受到混淆。CIM 随后按 top-$n$ 策略选出混淆分数最高的 $n$ 个关键点，将其嵌入 $f_k$ 替换为可学习的、上下文不变的标准嵌入 $z_k$：
   $$f_k' = \begin{cases} z_k, & \text{if } k \text{ is selected for intervention} \\ f_k, & \text{otherwise} \end{cases}$$
   这一替换操作在因果图意义上切断了混淆因子 $C$ 通过 $F \leftarrow C \rightarrow Y$ 形成的后门路径，近似实现了后门调整公式 $P(Y|do(F)) = \sum_c P(Y|F,c)P(c)$。

3. **分层图神经网络（Hierarchical GNN）**：在 CIM 输出的一组去混淆嵌入 $\{f_k'\}$ 上进行两阶段结构推理：
   - **局部运动学建模**：通过 EdgeConv 在人体骨架的物理连接边上进行消息传递，捕捉相邻关节间的局部运动学约束。
   - **全局语义超图注意力**：将语义相关的关键点（如所有左手关节、所有面部关键点）组织为超边，通过超边内的特征聚合和通道注意力精炼来建模长程依赖：
     $$f_k'' = f_k' \odot \left( \frac{1}{|\mathcal{E}_k|} \sum_{e \in \mathcal{E}_k} \sigma\big(\psi_a(g_e')\big) \right)$$
     其中 $\mathcal{E}_k$ 是包含关键点 $k$ 的超边集合，$g_e'$ 为超边的聚合表示。这一阶段在去混淆嵌入上强化全局解剖一致性。

4. **预测头（Prediction Head）**：将分层 GNN 输出的精炼嵌入 $f_k''$ 映射为最终的关键点坐标热图分布 $P(Y_k|do(F))$，并通过加权 KL 散度损失 $\mathcal{L}_{kpt}$ 与真值分布对齐。

**损失函数。** 总训练目标为两项损失的加权和：
$$\mathcal{L} = \mathcal{L}_{kpt} + \lambda \mathcal{L}_{cf}$$
其中 $\mathcal{L}_{kpt}$ 为主预测损失，$\mathcal{L}_{cf}$ 为反事实一致性损失，约束稳定关键点集合 $S$ 上的观测预测（stop-gradient）与干预预测一致：
$$\mathcal{L}_{cf} = \frac{1}{|S|} \sum_{k \in S} D_{KL}\big(\mathbf{sg}[P(Y_k|F)] \mid\mid P(Y_k|do(F))\big)$$
权重 $\lambda$ 固定为 0.1。消融实验表明，移除 $\mathcal{L}_{cf}$（$\lambda=0$）会导致 0.5 AP 的性能下降（Table 8），验证了该正则项对学习有意义标准嵌入的关键作用。

**数据流总结。** 输入图像 → 关键点编码器 → 初始嵌入 $\{f_k\}$ → CIM（混淆识别与替换）→ 去混淆嵌入 $\{f_k'\}$ → 分层 GNN（局部 EdgeConv + 全局超图注意力）→ 精炼嵌入 $\{f_k''\}$ → 预测头 → 关键点坐标。在整个流程中，CIM 充当“质量门控”，确保进入结构推理模块的嵌入已剥离主要的视觉混淆成分，而分层 GNN 则在净化后的特征空间上施加解剖先验，二者形成协同增益——消融实验显示，在完整分层 GNN 基础上加入 CIM 可额外提升 0.2 AP（67.0 vs. 66.8），总提升较基线达 1.7 AP（Table 4）。



CIGPose 的核心由三个紧密耦合的模块构成：**因果干预模块（CIM）** 负责去混淆，**分层图神经网络** 在净化后的嵌入上强化解剖一致性，**反事实一致性损失** 约束干预行为。以下逐一展开其公式化设计。

### 3.1 因果干预模块（CIM）

CIM 的设计动机源于结构因果模型（SCM）中的后门路径问题。在关键点估计的 SCM 中，视觉特征 $F$ 与姿态 $Y$ 之间因混淆因子 $C$（如遮挡、杂乱背景）形成非因果依赖 $F \leftarrow C \rightarrow Y$。理想情况下，应对 $F$ 施加 do-算子以切断此后门路径，得到干预分布：

$$P(Y|do(F)) = \sum_c P(Y|F,c) P(c) \tag{1}$$

然而直接边缘化所有混淆因子 $c$ 在实际中不可行。CIM 的核心洞察是：**预测不确定性可作为视觉混淆的有效代理**。基于此，CIM 分两步近似式 (1)：

**步骤一：混淆识别。** 对每个关键点 $k$，利用其预测热图分布的峰值高度度量不确定性，定义混淆分数：

$$s_c(k) = 1 - \frac{1}{2}\left(\max(P_{k,x}) + \max(P_{k,y})\right) \tag{2}$$

其中 $P_{k,x}$、$P_{k,y}$ 分别为关键点 $k$ 在 $x$、$y$ 方向上的预测概率分布。当模型对某关键点定位高度确信时，热图呈现尖锐单峰，$\max(P)$ 接近 1，$s_c(k)$ 接近 0；反之，在遮挡或模糊区域，热图多峰或平坦，$s_c(k)$ 升高。Figure 3 的实证验证表明，遮挡关键点的混淆分数显著高于可见关键点，确认了该代理的有效性。

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/003_Figure_3.jpg]]
*Figure 3: Validation of confounder score*

**步骤二：反事实替换。** 选取 $s_c(k)$ 最高的 top-$n$ 个关键点作为混淆嵌入 $F_{conf}$，将其替换为可学习的、上下文不变的标准嵌入 $z_k$，而其余可靠嵌入保持不变：

$$f_k' = \begin{cases} z_k, & \text{if } k \text{ is selected for intervention} \\ f_k, & \text{otherwise} \end{cases} \tag{3}$$

这一替换操作在效果上等价于切断了混淆因子 $C$ 对关键点嵌入的后门路径，使后续推理仅依赖去混淆后的因果证据。标准嵌入 $z_k$ 在训练中学习为高度集中的表征点，Figure 4 的 UMAP 可视化显示，学习到的标准嵌入形成了紧凑的流形，与原始上下文嵌入的分散分布形成鲜明对比。

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/004_Figure_4.jpg]]
*Figure 4: UMAP visualization of initial contextual embeddings vs. their corresponding learned canonical embeddings*

### 3.2 分层图神经网络

去混淆嵌入 $f_k'$ 随后进入两阶段分层 GNN，分别建模局部运动学约束与全局语义依赖。

**阶段一：局部运动学建模。** 基于人体骨骼的物理连接构建图结构，采用 EdgeConv 在每条骨骼边上进行消息传递，捕捉相邻关节间的运动学关系。

**阶段二：全局超图注意力精炼。** 将人体划分为多个语义超边 $\mathcal{E}$（如“上肢”、“下肢”、“头颈”等），每个超边 $e$ 聚合其成员关键点的嵌入：

$$g_e = \frac{1}{|e|} \sum_{k \in e} f_k'$$

随后通过注意力机制计算每个超边的通道级调制权重，对关键点嵌入进行精炼：

$$f_k'' = f_k' \odot \left( \frac{1}{|\mathcal{E}_k|} \sum_{e \in \mathcal{E}_k} \sigma(\psi_a(g_e')) \right) \tag{4}$$

其中 $\mathcal{E}_k$ 为包含关键点 $k$ 的超边集合，$\psi_a$ 为可学习的注意力变换，$\sigma$ 为 Sigmoid 激活，$\odot$ 为逐元素乘法。该机制使每个关键点能感知其所属语义组的全局上下文，增强长程解剖一致性。

### 3.3 训练目标

最终预测头基于精炼嵌入 $f_k''$ 生成关键点热图，主损失为去混淆预测分布与真实分布之间的加权 KL 散度：

$$\mathcal{L}_{kpt} = \sum_{k=1}^{K} w_k \cdot D_{KL}(Q_k \parallel P(Y_k | do(F))) \tag{5}$$

其中 $Q_k$ 为真实热图分布，$w_k$ 为关键点权重。

为防止 CIM 过度干预（即将可靠关键点也替换为标准嵌入），引入**反事实一致性损失**：对未被干预的稳定关键点集合 $S$，约束其观测路径预测与干预路径预测保持一致：

$$\mathcal{L}_{cf} = \frac{1}{|S|} \sum_{k \in S} D_{KL}(\mathbf{sg}[P(Y_k|F)] \mid\mid P(Y_k|do(F))) \tag{6}$$

其中 $\mathbf{sg}[\cdot]$ 为停止梯度算子，阻止观测路径的梯度回传，确保标准嵌入 $z_k$ 学习到有意义的上下文不变表征，而非简单复制观测嵌入。总损失为 $\mathcal{L} = \mathcal{L}_{kpt} + \lambda \mathcal{L}_{cf}$，$\lambda$ 固定为 0.1。

### 3.4 模块间协同机制

上述三个模块构成因果推理的闭环：CIM 基于不确定性代理识别并替换混淆嵌入，分层 GNN 在净化后的嵌入空间上进行结构推理，反事实一致性损失则约束 CIM 的干预行为不过度泛化。消融实验（Table 4）证实了这一协同效应：在完整分层 GNN 基础上引入 CIM 额外提升 0.2 AP（67.0 vs. 66.8），总提升达 1.7 AP over baseline；移除一致性损失（$\lambda=0$）则导致 0.5 AP 下降（Table 8），验证了该正则项对学习有意义标准嵌入的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/002_Figure_2.jpg]]
*Figure 2: (a) The proposed Structural Causal Model (SCM) for keypoint estimation, (b) The intervened SCM after applying the do-operator to the keypoint embeddings, (c) The realization of each component within our Causal Intervention Module (CIM)*



## 实验与关键发现

### 主要结果

CIGPose 在全身姿态估计基准 COCO-WholeBody 上取得 67.0% Whole-Body AP（CIGPose-x），较直接基线 RTMPose-x（65.3% AP）提升 **+1.7 AP**，并超越了依赖额外 UBody 数据及两阶段蒸馏的 DWPose-l（66.5% AP）（Table 1）。引入 UBody 数据后，CIGPose-x 进一步提升至 67.5% AP，较 DWPose-l 领先 +1.0 AP。在 COCO val2017 上，CIGPose-l（384×288 输入）达到 78.5% AP，较 RTMPose-l 提升 +1.2 AP（Table 2）。在密集人群场景 CrowdPose 数据集上，CIGPose-l 取得 73.7% AP，较 HRFormer-B 提升 +1.3 AP（Table 3），表明去混淆机制在遮挡和拥挤场景下具有显著增益。

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/006_Table_1.jpg]]
*Table 1: Whole-body pose estimation results on COCO-WholeBody [19, 51] V1.0 dataset. “*” denotes the model that relies on two-stage distillation and additional training data from the UBody dataset [27]. “†” indicates multi-scale testing. Flip test is used*

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/007_Table_3.jpg]]
*Table 3: Comparisons with SOTA methods on the CrowdPose [24] dataset. The default input resolution is 256×192, “†” denotes the input resolution is 384×288*

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/008_Table_2.jpg]]
*Table 2: Comparisons of CIGPose and SOTA methods on COCO val set [28]. The default input resolution is 256×192, “†” denotes the input resolution is 384×288*

### 消融实验

**组件贡献。** Table 4 的消融实验揭示了各模块的独立与协同效应：在基线 RTMPose-x（65.3% AP）上单独加入分层 GNN（局部 EdgeConv + 全局超图注意力）提升至 66.8% AP（+1.5 AP）；进一步加入因果干预模块（CIM）后达到 67.0% AP（额外 +0.2 AP），总提升 +1.7 AP。这表明去混淆为结构推理提供了更干净的嵌入空间，二者存在正向协同。

**一致性损失。** 反事实一致性损失权重 λ 的消融（Table 8）显示：λ=0 时 AP 从 66.3% 降至 65.8%（-0.5 AP），验证了该正则项对学习有意义标准嵌入的关键作用——它约束干预不改变可靠关键点的预测，防止标准嵌入退化为无信息表示。

**干预策略。** Table 9 表明固定预算的 Top-n 策略优于阈值策略，且 n=13（约 10% 关键点）效果最佳。干预频率统计（Table 7）显示，脚、手和腿等末端的干预频率最高，这些部位最易受遮挡、运动模糊和截断等视觉混淆影响，与 CIM 的设计直觉一致。

**混淆分数的有效性验证。** Figure 3 展示了遮挡关键点的混淆分数 $s_c(k)$ 显著高于可见关键点（中位数更高、分布更宽），直接验证了预测不确定性作为视觉混淆代理的有效性。Table 5 的实例内富集分析进一步表明，$s_c$ 选出的 top-n 关键点在同一实例中定位误差更大，且随着简单样本被逐步移除（Easy-drop p 增大），富集效应持续存在，证明混淆分数在困难样本上同样可靠。

### 失败模式与局限性

**过度正则化。** 对于罕见但正确的分布外姿态（如极端瑜伽动作），CIM 可能因高预测不确定性将其误判为混淆，并用标准嵌入替换，导致姿态细节丢失（见 Fig. 8 顶行）。此时去混淆反而损害了合理预测，暴露出不确定性代理无法区分“混淆导致的噪声”与“罕见但有效的结构变异”。

**语义误识别绕过。** 当模型对语义错误高度自信时（如将路灯误识别为人体），混淆分数 $s_c(k)$ 保持低位，CIM 被绕过，无法纠正此类错误（见 Fig. 8 底行）。这表明纯不确定性代理无法检测模型内部的语义盲区，需要引入显式的拒绝机制或额外的背景因果验证。

### 关键图表结论

- **Figure 1(a)**：CIGPose-x 在仅使用 COCO-WholeBody 数据时即超越依赖额外数据的 DWPose-l，确立了去混淆方法的数据效率优势。
- **Figure 2**：结构因果模型（SCM）阐明了混淆因子 C 通过后门路径 $F \leftarrow C \rightarrow Y$ 引入虚假相关性的机制，以及 do-操作截断该路径的因果原理。
- **Figure 4**：UMAP 可视化显示，学习到的标准嵌入 $z_k$ 形成高度集中的簇，与分散的上下文嵌入形成鲜明对比，验证了其作为“上下文不变理想表示”的设计目标。
- **Figure 5**：整体架构图展示了训练时的双路径设计——反事实路径（CIM → 分层 GNN）与观测路径（原始嵌入），推理时仅使用反事实路径，体现了因果干预的部署逻辑。

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/001_Figure_1.jpg]]
*Figure 1: (a) Comparison of CIGPose with related models for whole-body pose estimation on COCO-WholeBody. (b) Qualitative comparison between CIGPose-x and RTMPose-x [16]*

### 补充图表

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/009_Table_4.jpg]]
*Table 4: Ablation study of CIGPose on COCO-WholeBody. Values in parentheses are AP/AR gains*

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/015_Table_8.jpg]]
*Table 8: Effect of the counterfactual consistency loss weight λ*

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/016_Table_9.jpg]]
*Table 9: Comparison of intervention strategies during training. The fixed-budget ‘top-n‘ strategy provides a more stable and effective training signal, with*

![[assets/figures/papers/paper_list_l1011_https_arxiv_org_abs_2603_09418/figures/011_Table_5.jpg]]
*Table 5: Within instance top-n enrichment on COCO-WholeBody. Keypoints selected by*



## 定位与知识库关联

### 与基线方法的关系

CIGPose 直接构建在 **RTMPose** 系列（Jiang et al., MMPose 工具箱）之上，复用其 CSP-NeXt + GAU 关键点编码器作为骨干网络。RTMPose 采用观测路径：编码器输出的原始嵌入直接进入预测头生成热图分布，未显式建模视觉上下文中的虚假相关性。CIGPose 在此架构上插入两个关键模块，形成“去混淆—结构推理”的双阶段管线：

1. **因果干预模块（CIM）** 前置在编码器与预测头之间，通过预测不确定性识别混淆关键点嵌入，并用可学习的、上下文不变的标准嵌入进行反事实替换，阻断非因果后门路径。
2. **分层图神经网络** 在净化后的嵌入上依次执行局部运动学建模（EdgeConv）和全局语义超图注意力，强化解剖一致性。

这一设计与现有结构建模方法形成对比：**DWPose**（Yang et al., ICCV 2023）依赖两阶段蒸馏和额外 UBody 数据集来提升鲁棒性，本质上是数据驱动策略；而 CIGPose 从因果推断角度出发，在仅使用 COCO-WholeBody 数据的情况下，CIGPose-x 达到 67.0% AP，超过依赖额外数据的 DWPose-l（66.5% AP），揭示了去混淆机制对数据效率的增益。

在 CrowdPose 密集人群场景下，CIGPose-l 达到 73.7% AP，超过 **HRFormer-B**（Yuan et al., NeurIPS 2021）的 72.4% AP，表明因果干预在遮挡频繁的环境中具有跨架构的泛化优势。

### 组件协同效应

消融实验（Table 4）揭示了各组件的协同关系：
- 在完整分层 GNN 基础上引入 CIM，额外提升 0.2 AP（67.0 vs. 66.8），表明去混淆为结构推理提供了更干净的输入空间；
- 总提升 1.7 AP over baseline（RTMPose-x 65.3% AP），说明因果干预与解剖推理的联合作用显著大于单一组件。

### 适用边界

CIGPose 的有效性建立在两个核心假设之上：

1. **预测不确定性是视觉混淆的有效代理**：Figure 3 验证了遮挡关键点的混淆分数显著高于可见关键点，但这一代理机制存在盲区——当模型对语义错误（如将路灯误识为人体）高度自信时，混淆分数低，CIM 被绕过，模型仍会输出错误姿态。
2. **标准嵌入能覆盖所有合理姿态**：CIM 将高不确定性嵌入替换为学习的标准嵌入，对常见姿态有效，但对罕见但正确的分布外姿态（如极端瑜伽动作），高不确定性可能被误判为混淆，导致过度正则化并丢失细节。

### 局限与开放问题

**已知局限**（论文明确讨论）：
- 对罕见但正确的分布外姿态，CIM 可能因高不确定性将其错误标记为混淆并替换为标准嵌入，导致姿态细节丢失（Fig. 8 顶行）。
- 预测不确定性代理无法检测模型高度自信的语义错误，此时混淆分数低，CIM 被绕过（Fig. 8 底行）。

**开放问题**（论文提出但未解决）：
- 如何处理模型自信的语义误识别？能否引入显式的拒绝机制或额外的背景因果验证？
- 因果干预框架能否扩展至 3D 全身姿态估计及视频时序一致性去混淆？
- 是否可以结合生成式模型合成更具挑战性的混杂物，增强标准嵌入的泛化能力？

### 知识库定位

CIGPose 处于**因果推断 × 姿态估计**的交叉地带，与以下工作形成知识谱系：

| 维度 | 相关工作 | 与本工作的关系 |
|------|----------|----------------|
| 图结构建模 | **HGG** (Jin et al., ECCV 2020)、**MPGD** (He et al., CVPR 2023) | CIGPose 的分层 GNN 继承了超图语义分组的思路，但前置了因果干预模块 |
| 因果推断在视觉中的应用 | 后门调整、反事实推理 | CIGPose 首次将 do-算子引入关键点嵌入层面，区别于特征层面的因果方法 |
| 不确定性估计 | 预测分布峰值、熵度量 | CIGPose 将不确定性重新定义为混淆代理，赋予其因果语义 |
| 两阶段蒸馏 | **DWPose** (Yang et al., ICCV 2023) | CIGPose 在数据效率上形成对比优势，不依赖额外标注数据 |

代码开源（https://github.com/53mins/CIGPose），基于 MMPose 工具箱实现，便于后续工作在标准框架下复现和扩展。



## 原文 PDF

![[paperPDFs/CVPR_2026/CIGPose_Causal_Intervention_Graph_Neural_Network_for_Whole_Body_Pose_Estimation.pdf]]
