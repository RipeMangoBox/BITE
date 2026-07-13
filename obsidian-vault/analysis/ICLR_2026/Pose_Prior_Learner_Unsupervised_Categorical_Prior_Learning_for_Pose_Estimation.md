---
title: "Pose Prior Learner: Unsupervised Categorical Prior Learning for Pose Estimation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Pose_Prior_Learner_Unsupervised_Categorical_Prior_Learning_for_Pose_Estimation.pdf
project_link: null
code_link: https://github.com/ZhangLab-DeepNeuroCogLab/Pose-Prior-Learner
openreview_forum_id: hPY2jwJzZ4
aliases:
- PPLP
- PPLUCPLPE
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "引入分层记忆模块（hierarchical memory）存储原型姿态的组成部分，并从中蒸馏出通用的关键点先验（keypoint prior），通过该先验引导姿态变换与图像重建学习。"
primary_logic: "通过分层记忆蒸馏得到显式且可解释的类别姿态先验，能够以完全自监督的方式学习，并显著提升姿态估计精度，同时在迭代推理中利用记忆中的原型姿态校正遮挡下的姿态估计。"
claims:
- "PPL在Human3.6m、Taichi和CUB-200-2011数据集上的无监督关键点检测中全面超越所有基线方法。"
- "PPL学习到的先验优于人工定义的先验，其默认模型精度（2.56）与可微调的预定义先验（2.51）接近，且明显优于固定预定义先验（2.70）和使用人工先验的STT方法（3.31）。"
- "在遮挡图像上，迭代推理（4次迭代）利用分层记忆有效推断缺失部分，将L2误差显著降低，接近无遮挡水平。"
- "学习到的关键点先验在训练早期（epoch 5）即收敛到有意义的类人形状，证明了先验学习的有效性。"
---

# Pose Prior Learner: Unsupervised Categorical Prior Learning for Pose Estimation

> [!tip] 核心洞察
> 通过分层记忆蒸馏得到显式且可解释的类别姿态先验，能够以完全自监督的方式学习，并显著提升姿态估计精度，同时在迭代推理中利用记忆中的原型姿态校正遮挡下的姿态估计。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 姿态先验学习器：面向姿态估计的无监督类别先验学习 |
| 英文题名 | Pose Prior Learner: Unsupervised Categorical Prior Learning for Pose Estimation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=hPY2jwJzZ4) · [GitHub](https://github.com/ZhangLab-DeepNeuroCogLab/Pose-Prior-Learner) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Pose Prior Learner (PPL) |
| Dataset | Human3.6m (Res.128), Human3.6m (Res.256), Taichi (256x256), CUB-200-2011 Aligned |

> [!tip] 效果简介
> - Human3.6m (Res.128) 上，归一化L2误差（↓） 为 1.92，对比 2.44 (BKind)，变化 -0.52。
> - Human3.6m (Res.256) 上，归一化L2误差（↓） 为 2.56，对比 2.73 (Jakab et al.)，变化 -0.17。
> - Taichi (256x256) 上，总和L2误差（↓） 为 293.35，对比 316.10 (AutoLink)，变化 -22.75。

## 概要

无监督姿态估计的核心瓶颈在于缺乏显式的、可学习的类别姿态先验。现有方法或隐式编码先验于网络中，或依赖人工定义的关键点模板，导致关键点定位精度不足，尤其在遮挡等挑战性场景下缺乏结构约束。本文提出 **Pose Prior Learner (PPL)**，通过引入**分层记忆模块**（hierarchical memory）存储原型姿态的组成部分，并从中蒸馏出通用的关键点先验与连通性先验，以完全自监督的方式学习显式且可解释的类别姿态先验，从而引导姿态变换与图像重建。

核心结论如下：
- PPL 学习到的先验**优于人工定义的先验**：其默认模型在 Human3.6m（分辨率 256×256）上的归一化 L2 误差为 2.56，与可微调的预定义先验（2.51）接近，且明显优于固定预定义先验（2.70）和使用人工先验的 STT 方法（3.31）（Table 2）。
- 在 Human3.6m、Taichi 和 CUB-200-2011 数据集上，PPL 的**无监督关键点检测精度全面超越所有基线方法**（Table 1），在 Human3.6m（128×128）上相较最强基线 BKind 的误差降低 0.52。
- 在遮挡场景下，PPL 的**迭代推理**策略利用分层记忆中的原型姿态推断缺失部分，经 4 次迭代后 L2 误差显著降低，接近无遮挡水平（Figure A4, A5）。

方法定位上，PPL 属于**基于图像重建的自监督姿态估计**范式，但其核心创新在于将姿态先验从隐式网络参数中解耦为显式的结构化表示，并通过分层记忆蒸馏实现可学习化。与 AutoLink（He et al., CVPR 2022）等无先验方法相比，PPL 引入了可学习的类别拓扑约束；与 STT（Schmidtke et al., ICCV 2021）等使用人工先验的方法相比，PPL 无需任何预定义模板，实现了完全数据驱动的先验获取。

姿态估计是计算机视觉中的基础任务，旨在从图像中定位物体或人体的关键点。现有的主流方法通常依赖大量人工标注的关键点数据进行监督训练，但标注成本高昂，且难以覆盖所有物体类别。因此，无监督姿态估计——即从无标注图像中自动发现并定位关键点——成为一个重要但极具挑战的研究方向。

### 核心瓶颈：类别姿态先验的缺失

当前无监督姿态估计方法面临一个根本性瓶颈：**缺乏显式的、可学习的类别姿态先验**。所谓类别姿态先验，是指对某一类物体（如人体、鸟类）的典型关键点布局及其连接关系的结构化知识。现有方法通常将这种先验隐式地编码在网络参数中，或依赖人工定义的固定模板，导致以下问题：

1. **关键点定位不准确**：缺乏结构约束使得预测的关键点容易偏离合理的空间配置，尤其在物体外观变化较大时。
2. **遮挡场景下表现脆弱**：当物体部分被遮挡时，模型无法利用对整体结构的先验知识来推断缺失部分的位置。
3. **先验质量受限**：人工定义的先验（如人体骨骼模板）不仅需要领域知识，而且可能不适用于非人体类别，限制了方法的通用性。

### 现有方法的局限

表1汇总了当前无监督姿态估计的主要方法路线及其在姿态先验方面的不足：

| 方法路线 | 代表工作 | 先验形式 | 主要局限 |
|---------|---------|---------|---------|
| 基于图像重建的自编码器 | **AutoLink** (He et al., CVPR 2022)、**BKind** (Sun et al., ECCV 2022) | 无显式先验，隐式编码在网络中 | 缺乏结构约束，关键点语义一致性差 |
| 基于GAN的关键点检测 | **LatentKeypointGAN** (He et al., 2021)、**GANSeg** (He et al., 2022) | 无显式先验 | 训练不稳定，定位精度有限 |
| 人工定义先验 | **STT** (Schmidtke et al., ICCV 2021) | 预定义关键点模板 | 依赖领域知识，无法迁移到新类别 |
| 多模态先验 | **Hedlin et al.** (2024) | 利用文本等多模态信息 | 模型复杂，依赖额外模态数据 |

这些方法的共同缺陷在于：**没有一种机制能从数据本身以完全自监督的方式学习并蒸馏出可解释的类别姿态先验**。这不仅限制了估计精度，也使得模型在遮挡等挑战性场景下缺乏推理能力。

### 本文动机与核心思路

针对上述缺口，本文提出 **Pose Prior Learner (PPL)**，旨在回答以下核心问题：**能否从无标注图像中以完全自监督的方式学习出显式的、可解释的类别姿态先验？**

PPL的核心洞察是：通过设计一个**分层记忆模块**（hierarchical memory）来存储原型姿态的组成部分，并从中**蒸馏**出通用的关键点先验与连通性先验，可以形成一个结构化且可学习的姿态先验表示。该先验随后通过仿射变换与图像重建进行自监督学习，并在推理阶段利用记忆检索实现迭代式的姿态校正——尤其在遮挡场景下，模型能利用记忆中的原型姿态推断缺失部分。

Figure 1 以示意图形式展示了这一挑战与PPL的解决思路：给定一系列输入图像（蓝色帧），目标是学习一个由关键点先验和连通性先验组成的姿态先验（绿色矩形）；该先验不仅提升常规姿态估计精度，还使模型能在仅训练于完整图像的情况下，对遮挡图像产生合理的姿态预测。

这一设计将无监督姿态估计从“隐式学习”推进到“显式先验学习”，为提升精度、可解释性和鲁棒性开辟了新路径。

## 核心方法与创新机理

PPL 的核心创新在于**从无标注图像中以完全自监督的方式蒸馏出显式、可解释的类别姿态先验**，并利用该先验引导姿态变换与迭代推理。相较于现有方法，PPL 在以下三个关键维度实现了根本性改变：

### 1. 姿态先验表示：从隐式编码到显式可蒸馏的结构化先验

现有无监督姿态估计方法（如 **AutoLink** (He et al., CVPR 2022)、**BKind** (Sun et al., ECCV 2022)）将姿态约束隐式编码在网络权重中，或依赖人工定义的关键点模板（如 **STT** (Schmidtke et al., ICCV 2021)）。PPL 首次将姿态先验显式定义为结构化表示 $V = (T, W)$，其中 $T$ 为关键点先验（$N$ 个归一化 2D 坐标），$W$ 为连通性先验（关键点对之间的链接权重）。这一设计使得先验可被独立蒸馏、可视化和分析——实验表明，关键点先验在训练早期（epoch 5）即收敛为有意义的类人形状（Figure 4b），证明了先验学习的有效性。

### 2. 记忆模块设计：从扁平编码到分层记忆蒸馏

现有方法或缺乏结构化记忆，或仅使用单层多向量记忆库。PPL 提出**分层记忆模块**（hierarchical memory）：包含 34 个记忆库，每库存储 16 个 512 维原型向量，支持不同抽象层次的结构信息编码。该设计的关键机制是**双向蒸馏**：
- **编码-检索-解码**：将估计关键点 $T'$ 编码为 $m$ 个令牌，在每个记忆库中检索最近向量，解码为重建关键点 $T'_{recon}$，通过关键点配置重建损失 $L_{kr} = \|T'_{recon} - T'\|_2 + \|G - G'\|_2$ 训练记忆库存储原型姿态的组成部分。
- **先验蒸馏**：对每个记忆库内向量做平均池化，解码为关键点先验 $T = MIX_{dec}([MP(b_1), \dots, MP(b_m)])$，使先验融合记忆库中的结构性知识。

消融实验（Table A3）证实：使用单个记忆库（PPL-1MemBank）的归一化 L2 误差为 2.72，显著差于分层记忆的 2.56，验证了多层抽象的必要性。

### 3. 推理策略：从单次前向传递到记忆引导的迭代校正

现有方法仅通过单次前向传递输出估计姿态。PPL 引入**迭代推理策略**：将重建图像 $I_{recon}$ 反馈为输入，利用分层记忆检索校正关键点，逐步优化姿态估计。在遮挡场景下，该策略的效果尤为显著——4 次迭代即可将 L2 误差大幅降低，接近无遮挡水平（Figure A4, A5）。这一能力源于记忆库中存储的原型姿态组成部分：即使输入图像存在大面积遮挡，模型仍能从记忆中检索合理的结构信息完成姿态推断（Figure 4a），尽管在极端遮挡下仍可能失败（Figure A2）。

**总结**：PPL 的三项 changed slots 形成了完整的创新闭环——分层记忆存储原型结构，先验蒸馏提取通用知识，迭代推理利用先验校正不确定性。这一设计使得 PPL 在 Human3.6m、Taichi 和 CUB-200-2011 等数据集上全面超越所有无监督基线（Table 1），且其学习到的先验优于人工定义的固定先验（Table 2）。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_hPY2jwJzZ4/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our proposed Pose Prior Learner (PPL). We first distill the keypoint prior from the hierarchical memory M. Features of the image I and the embedding of the keypoint prior are concatenated to predict the affine transformation parameters. The keypoint prior is transformed and their pair-wise links are modulated with the connectivity prior W to obtain the combined link heatmap S. The concatenation of the link heatmap S and the reference image I _ { r e f } is decoded to produce the reconstructed image I _ { r e c o n } . The sg symbol represents the stopping gradient operation. The red arrows indicate the gradient flows during backpropagation based on image reconstruction. See Sect...*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_hPY2jwJzZ4/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the iterative inference strategy in our PPL (Section 3.4). During inference, we iteratively use the reconstructed image $I _ { r e c o n }$ as input to estimate the pose $T ^ { \prime }$ . The hierarchical memory M refines the estimated pose $\breve { T } ^ { \prime }$ and outputs $T _ { r e c o n } ^ { \prime }$ . The original image I is used as the reference image to reconstruct the image $I _ { r e c o n }$ . It is then used as the input image in the next iteration

PPL 的整体设计围绕一个核心思想展开：**从可学习的分层记忆中蒸馏出显式类别姿态先验，再通过该先验引导姿态变换与图像重建，形成闭环自监督学习**。整个 pipeline 由五个关键模块串联而成，数据流在“先验蒸馏—特征提取—姿态变换—图像重建—记忆校正”之间循环。

### 数据流总览

Figure 2 给出了 PPL 的完整架构。流程如下：

1. **先验蒸馏**：分层记忆 M 通过平均池化各记忆库的向量，经 MLP-Mixer 解码器生成关键点先验 $T = [P_1, P_2, ..., P_N]$，其中每个 $P_i \in [-1,1] \times [-1,1]$。连通性先验 $W$ 随机初始化并可学习。二者共同构成类别姿态先验 $V = (T, W)$。

2. **特征提取**：编码器 $\phi_{enc}$ 从输入图像 $I$ 中提取特征嵌入 $h_I$；同时将关键点先验 $T$ 嵌入为 $h_T$。

3. **姿态变换**：将 $h_I$ 与 $h_T$ 拼接后送入两层全连接网络 $FC$，预测每个关键点的仿射变换参数 $\Theta_i$，再通过 $[P_i', 1]^\top = \Theta_i [P_i, 1]^\top$ 将先验关键点映射为估计姿态 $T'$。

4. **图像重建**：利用连通性先验 $W$ 对任意两关键点 $P_i', P_j'$ 之间的链接热图 $S_{i,j}$ 加权，通过最大值池化得到组合链接热图 $S = \max_{i,j} (w_{i,j} S_{i,j})$。解码器 $\phi_{dec}$ 以参考图像 $I_{ref}$ 和 $S$ 为输入，重建图像 $I_{recon}$。

5. **记忆校正（训练时）**：估计姿态 $T'$ 被 MLP-Mixer 编码器 $MIX_{enc}$ 编码为 $m$ 个令牌 $G$，每个令牌 $g_i$ 在对应记忆库 $b_i$ 中检索最近向量 $g_i'$，再由 $MIX_{dec}$ 解码为重建关键点 $T'_{recon}$。关键点配置重建损失 $L_{kr} = \| T'_{recon} - T' \|_2 + \| G - G' \|_2$ 驱动记忆学习存储原型姿态的组成结构。

### 迭代推理策略

Figure 3 展示了推理阶段的迭代优化机制。PPL 并非单次前向输出，而是将当前重建图像 $I_{recon}$ 反馈为下一轮输入，利用分层记忆对估计姿态进行逐步校正。具体而言：

- 第 1 轮以原始图像 $I$ 为输入，输出估计姿态 $T'$ 和重建图像 $I_{recon}$；
- 第 $t$ 轮（$t > 1$）以 $I_{recon}$ 替换原始输入，重新估计姿态，记忆模块检索原型结构并输出校正后的 $T'_{recon}$；
- 原始图像 $I$ 始终作为参考图像 $I_{ref}$ 用于重建。

所有实验默认使用 4 次迭代。该策略在遮挡场景下尤为关键：记忆中的原型姿态能够“补全”被遮挡部分的结构信息，使姿态估计逐步逼近无遮挡水平（见 Figure A4、A5 的定量曲线）。

### 训练目标

PPL 联合优化四个损失函数：

- **图像重建损失** $L_{ir} = \| \psi(I_{recon}) - \psi(I) \|_1$：使用 VGG19 冻结特征提取器 $\psi$ 的感知损失，而非像素级 MSE；
- **边界损失** $L_b = \sum_{* \in \{x,y\}} \max(0, |P'_{i,*}| - 1)$：惩罚超出 $[-1,1]$ 归一化范围的变换关键点；
- **链接正则化损失** $L_l = \sum_{i,j} w_{i,j} \| l(P_i, P_j) - l(P'_i, P'_j) \|_1$：鼓励变换前后关键点间链接长度保持不变；
- **关键点配置重建损失** $L_{kr}$：确保记忆检索解码后的关键点与原始估计一致。

消融实验（Table A3）表明，移除边界损失会导致训练不稳定；将感知损失替换为像素级 MSE 使误差从 2.56 升至 2.84；使用单记忆库（PPL-1MemBank）的误差为 2.72，显著劣于分层记忆的 2.56。这验证了各损失组件和分层记忆结构对整体性能的因果贡献。

### 姿态先验表示

PPL将类别姿态先验形式化为一个结构化表示 $V = (T, W)$，其中 $T$ 为关键点先验，$W$ 为连通性先验。关键点先验 $T = [P_1, P_2, ..., P_N]$ 由 $N$ 个归一化2D坐标组成，每个 $P_i \in [-1,1] \times [-1,1]$。连通性先验 $W$ 以共享链接权重形式编码关键点之间的拓扑关系。这一显式先验表示是PPL区别于现有无监督姿态估计方法的核心设计——基线方法（如AutoLink、BKind）将姿态先验隐式编码在网络参数中，缺乏可解释的结构化约束。

### 分层记忆模块与先验蒸馏

分层记忆 $\mathcal{M}$ 是PPL的核心创新模块，由 $m$ 个记忆库组成（默认 $m=34$），每个记忆库 $b_i$ 包含 $k$ 个 $d$ 维向量（默认 $k=16, d=512$）。与单层多向量记忆（如PPL-1MemBank变体，误差2.72）不同，分层设计使不同记忆库编码不同抽象层次的局部结构信息。

**记忆检索流程**（Figure A6a）：给定估计的关键点配置 $T'$，首先通过MLP-Mixer编码器将其映射为 $m$ 个令牌：

$$G = \text{MIX}_{\text{enc}}(T')$$

每个令牌 $g_i$ 在对应记忆库 $b_i$ 中检索最近邻向量：

$$g_i' = \arg\min_{v \in b_i} \| g_i - v \|_2$$

检索到的 $m$ 个向量 $G'$ 经MLP-Mixer解码器重建为关键点配置：

$$T'_{\text{recon}} = \text{MIX}_{\text{dec}}(G')$$

**先验蒸馏流程**（Figure A6b）：对每个记忆库内的 $k$ 个向量进行平均池化，得到 $m$ 个池化向量，再解码为关键点先验：

$$T = \text{MIX}_{\text{dec}}([\text{MP}(b_1), \text{MP}(b_2), ..., \text{MP}(b_m)])$$

这一蒸馏机制使记忆模块中存储的原型姿态组成部分被压缩为通用的类别姿态先验，是PPL实现完全自监督先验学习的关键因果机制。

### 姿态变换与图像重建

给定输入图像 $I$，特征提取器 $\phi_{\text{enc}}$ 提取图像嵌入 $h_I$，与关键点先验 $T$ 的嵌入 $h_T$ 拼接后，通过两层全连接网络预测每个关键点的仿射变换参数：

$$[\Theta_1, \Theta_2, ..., \Theta_N] = \text{FC}(h_I, h_T)$$

每个关键点 $P_i$ 经对应仿射变换映射为估计位置：

$$[P_i', 1]^\top = \Theta_i [P_i, 1]^\top$$

变换后的关键点 $T'$ 用于生成链接热图。任意两个关键点 $P_i'$ 和 $P_j'$ 之间的可微链接热图 $S_{i,j}$ 由连通性先验 $w_{i,j}$ 加权，通过最大值池化组合为整体链接热图：

$$S = \max_{i,j}^{N \times N} (w_{i,j} S_{i,j})$$

图像解码器 $\phi_{\text{dec}}$ 结合参考图像 $I_{\text{ref}}$ 和链接热图 $S$ 重建图像：

$$I_{\text{recon}} = \phi_{\text{dec}}(I_{\text{ref}}, S)$$

### 训练损失函数

PPL联合优化四个损失函数：

**图像重建损失** $L_{ir}$：使用预训练VGG19网络 $\psi$ 提取感知特征，计算L1距离（消融实验表明替换为像素级MSE使误差从2.56升至2.84）：

$$L_{ir} = \| \psi(I_{\text{recon}}) - \psi(I) \|_1$$

**边界损失** $L_b$：惩罚超出归一化图像范围的变换关键点（移除该损失导致训练不稳定）：

$$L_b = \sum_{* \in \{x,y\}} \max(0, |P'_{i,*}| - 1)$$

**链接正则化损失** $L_l$：鼓励变换前后关键点间链接长度保持不变：

$$L_l = \sum_{i,j} w_{i,j} \| l(P_i, P_j) - l(P'_i, P'_j) \|_1$$

**关键点配置重建损失** $L_{kr}$：确保记忆检索并解码的关键点与原始估计一致：

$$L_{kr} = \| T'_{\text{recon}} - T' \|_2 + \| G - G' \|_2$$

### 迭代推理策略

推理阶段（Figure 3），PPL采用迭代自回归策略：将上一轮重建图像 $I_{\text{recon}}$ 作为新一轮输入，重新估计姿态 $T'$，经分层记忆 $\mathcal{M}$ 检索校正后输出 $T'_{\text{recon}}$。原始图像 $I$ 始终作为参考图像。默认使用4次迭代，实验表明迭代推理在遮挡场景下显著降低L2误差，接近无遮挡水平（Figure A4, A5）。

## 实验与关键发现

### 核心定量结果

PPL在人体姿态（Human3.6m、Taichi）和动物姿态（CUB-200-2011）数据集上全面超越现有无监督基线。Table 1汇总了关键点检测误差：在Human3.6m分辨率128下，PPL的归一化L2误差为**1.92**，较最优基线BKind（2.44）降低0.52；分辨率256下误差为**2.56**，优于Jakab et al.（2.73）。在Taichi数据集上，PPL的总和L2误差为**293.35**，显著低于AutoLink（316.10）。在CUB-200-2011的对齐子集上，PPL（3.19）以微弱优势超越GANSeg（3.23）；在四个非对齐子集（001/002/003/All）上，PPL分别将误差降低0.9、0.6、1.2和0.8，均优于AutoLink。这些结果覆盖了视频帧参考和随机掩码参考两种训练模式，表明PPL的优势具有跨数据集的鲁棒性。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_hPY2jwJzZ4/figures/005_Table_1.jpg]]
*Table 1: Keypoint detection on the video datasets Human3.6m and Taichi, and the image dataset CUB-200-2011. For the video datasets Human3.6m and Taichi, we use video frames as $I _ { r e f }$ during training. For all the CUB evaluation subsets, we instead use randomly masked images as $I _ { r e f }$ . We report mean $L _ { 2 }$ error (↓) normalized by image resolution for Human3.6m and CUB-200-2011, and summed $L _ { 2 }$ error (↓) for Taichi. The smaller the error, the better the model performance is. We use resolution 2 5 6 $\times$ 2 5 6 for Taichi and 1 2 8 $\times$ 1 2 8 for CUB-200-2011. For Human3.6m, we report results under both resolutions. Following He et al. (2022a), we use different numbers of keyp...

值得注意的是，PPL*变体（不使用视频时序一致性，仅以随机掩码帧作为参考图像）在Human3.6m和Taichi上仍持续优于AutoLink（Table A4），证明性能增益源于学习到的类别姿态先验，而非跨帧重建的时序信息。与使用多模态先验的Hedlin et al.（2024）相比，PPL仅依赖视觉模态且模型更小，仍在多个数据集上取得相当或更优的性能（Table A2），进一步验证了分层记忆蒸馏先验的有效性。

### 先验学习质量分析

**先验收敛速度**：Figure 4(b)展示了关键点先验随训练epoch的演化过程。在训练早期（epoch 5），先验已收敛到具有类人形状的结构化配置，随后仅进行微调。这种快速收敛表明分层记忆能够高效捕捉类别姿态的底层结构。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_hPY2jwJzZ4/figures/009_Figure_4.jpg]]
*Figure 4: Visualization results of poses estimation on Human3.6m. (a) Pose estimation on occluded images in Human3.6m. The first column shows the original image and its estimated pose by PPL. Columns 2-5 show the iterative inference process where the reconstructed images by PPL (Row 1 and 3) are fed back to itself for estimating poses (Rows 2 and 4) on occluded images either using CenterMasking (Row 1 and 2) or RandomMasking (Row 3 and 4). (b) The pose prior evolves as a function of training epochs (from top to bottom). (c) Comparison between PPL and AutoLink He et al. (2022a) in estimated poses on example images from Human3.6m. The left column shows testing images, the middle column and the right co...*

**先验初始化与可学习性消融**：Table 2揭示了先验设计的关键权衡。PPL默认配置（关键点先验从记忆蒸馏，连通性先验随机初始化且可学习）的归一化L2误差为**2.56**。相比之下，使用人工预定义但冻结的关键点先验误差升至2.70，证明学习到的先验优于固定的专家知识。当预定义关键点先验可微调时，误差降至**2.51**，略优于默认PPL，表明人工先验提供了良好的初始化，但可学习性才是核心。连通性先验方面，随机初始化且可学习的配置（2.56）与预定义可学习配置（2.54）性能接近，而冻结的随机连通性先验则无法收敛，说明连通性结构同样需要从数据中自适应学习。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_hPY2jwJzZ4/figures/006_Table_2.jpg]]
*Table 2: Keypoint detection results of our PPL variants on the Human3.6m dataset. All results in mean L2 errors (↓) are normalized by the image resolution of 256 × 256. Both keypoint prior (Row 1-2) and Connectivity prior (Row 3-4) can be either pre-defined (Pre.) or randomly initialized (Rand.). During training, the parameters in both the priors can be either frozen (✗) or learnable (✓). The last column (From Mem) shows the result of our default PPL method. Its keypoint prior is initialized from memory (From Mem). Its connectivity prior is randomly initialized (Rand.) and learnable (✓) during training. Best is in bold*

### 迭代推理与遮挡鲁棒性

PPL的迭代推理策略在遮挡场景下展现出显著的姿态校正能力。Figure 4(a)和Figure A4/A5量化了这一效果：在中心遮挡（CenterMasking）和随机遮挡（RandomMasking）条件下，随着推理迭代次数从0增至4，归一化L2误差持续下降。在较大遮挡比例下，4次迭代后的误差接近无遮挡水平，表明分层记忆能够有效检索原型姿态的组成部分以推断缺失关键点。Figure 3描述了这一机制：每次迭代将重建图像反馈为输入，记忆模块对估计姿态进行校正，逐步改善关键点定位。

然而，该方法存在明确的失败边界。Figure A2展示了一个大面积遮挡的失败案例：当遮挡覆盖人体下半部分时，迭代推理（iteration 4）仍无法恢复正确姿态，输出一个看似合理但错误的站立姿态骨架。这表明分层记忆的原型检索在严重信息缺失时可能收敛到错误的局部最优。

### 损失函数与架构消融

Table A3系统消融了损失组件和记忆结构对性能的影响：

- **知觉损失 vs. 像素级MSE**：将VGG19知觉损失替换为像素级MSE损失，误差从2.56升至2.84，验证了高层语义特征对重建质量的关键作用。
- **边界损失**：移除边界损失导致训练不稳定，说明该正则项对约束关键点变换范围不可或缺。
- **分层记忆 vs. 单记忆库**：使用单个记忆库（PPL-1MemBank）的误差为2.72，显著差于多层分层记忆的2.56，证实了多级抽象存储的必要性。
- **记忆向量维度与关键点数量**：Figure A7的消融显示，记忆库向量维度从64增至512时性能持续提升，关键点数量在16附近达到最优，过多或过少均导致性能下降。

### 语义一致性与迁移能力

Figure A8展示了预测关键点的语义一致性：相同颜色的关键点在人体不同姿态下保持一致的语义对应（如头部、手部、脚部），尽管训练完全无监督，PPL仍隐式学习到了稳定的语义结构。Table A5进一步展示了先验的迁移价值：在遮挡图像分类任务中，使用PPL先验的ResNet-50在遮挡条件下的分类准确率显著优于无先验基线，表明学习到的姿态先验可泛化至下游任务。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_hPY2jwJzZ4/figures/028_Figure_24.jpg]]
*Figure 24: (a) Keypoint configuration reconstruction. (b) Memory distillation. Figure A6: Retrieval and distillation of the proposed hierarchical memory in our PPL. (a) The hierarchical memory M is trained to reconstruct the keypoints $T _ { r e c o n } ^ { \prime } . T ^ { \prime }$ is encoded into m tokens by the MLP-Mixer blocks M I $X _ { e n c }$ . Each token $g _ { i }$ retrieves its closest vector $g _ { i } ^ { \prime }$ in memory bank $b _ { i }$ . The resulting m vectors are decoded by the MLP-Mixer M I $X _ { d e c }$ into the reconstructed keypoints $T _ { r e c o n } ^ { \prime }$ . The green arrows indicate the gradient flows during backpropagation based on the reconstruction of keypoint configuration...

## 定位与知识库关联

### 1. 在无监督姿态估计谱系中的位置

PPL 处于**无监督类别级姿态估计**这一子领域，其核心区分特征在于显式地学习并利用可解释的姿态先验。与该领域早期工作相比，PPL 的定位可沿两条轴线刻画：

**轴线一：先验的显式性与可学习性。** 早期方法如 **Thewlis et al.**（ICCV 2017）和 **Zhang et al.**（2018）将姿态结构隐式编码在网络参数中，缺乏对关键点空间配置的显式约束。**Jakab et al.**（NeurIPS 2020）虽引入了关键点检测的自监督框架，但同样不包含显式先验。**STT**（Schmidtke et al., ICCV 2021）是少数使用显式先验的方法，但其先验是人工定义的关键点模板，不可学习且依赖领域知识。**Hedlin et al.**（2024）引入了多模态先验（结合语言模型），但模型规模更大且依赖额外模态。PPL 的独特贡献在于：**从数据中以完全自监督的方式蒸馏出显式、可解释、可学习的类别姿态先验**，摆脱了对人工模板或多模态信号的依赖。

**轴线二：记忆机制与结构化表示。** **AutoLink**（He et al., CVPR 2022）和 **BKind**（Sun et al., ECCV 2022）代表了无先验无监督姿态估计的强基线，它们通过图像重建学习关键点，但不维护任何形式的记忆或原型存储。**LatentKeypointGAN**（He et al., 2021）和 **GANSeg**（He et al., 2022）基于 GAN 框架，同样缺乏对姿态原型的显式建模。PPL 引入的**分层记忆模块**（34 个记忆库，每库 16 个 512 维向量）在无监督姿态估计中是首次出现，它存储原型姿态的组成部分，支持多层抽象与局部结构检索。消融实验（Table A3）证实：将分层记忆替换为单记忆库（PPL-1MemBank）使归一化 L2 误差从 2.56 升至 2.72，验证了分层结构的关键作用。

### 2. 核心设计选择与因果机制

PPL 的性能优势可归因于以下因果链路：

1. **分层记忆 → 结构化先验蒸馏 → 姿态约束。** 分层记忆库将原型姿态分解为部分结构存储，通过平均池化与 MLP-Mixer 解码蒸馏出关键点先验 $T$。该先验在训练早期（epoch 5）即收敛到类人形状（Figure 4(b)），为后续变换预测提供了强结构约束。

2. **显式先验 → 仿射变换引导 → 稳定训练。** 与无先验方法相比，PPL 预测的是从先验到目标姿态的仿射变换参数，而非直接从图像回归关键点坐标。这种“模板变换”范式降低了学习难度，消融实验（Table 2）表明：使用可学习预定义先验的误差为 2.51，而固定预定义先验为 2.70，STT 使用人工先验为 3.31，PPL 默认模型为 2.56——蒸馏先验的性能接近人工先验的上限，且显著优于无先验基线。

3. **迭代推理 → 记忆检索校正 → 遮挡鲁棒性。** 在遮挡场景下，PPL 将重建图像反馈为输入，利用分层记忆检索最接近的原型部分来校正被遮挡的关键点。Figure A4/A5 显示：4 次迭代推理可将 L2 误差显著降低，接近无遮挡水平。这一能力源于记忆库中存储的原型姿态信息，而非训练时见过的遮挡样本（PPL 仅在全身边、无遮挡图像上训练）。

### 3. 适用边界与局限

PPL 的适用性受以下因素制约：

- **2D 先验的维度限制。** 当前方法仅学习 2D 关键点先验，无法建模 3D 旋转和显著的形状变化。对于需要深度推理或大角度旋转的场景，性能可能退化。
- **大面积遮挡下的失效。** 尽管迭代推理提升了遮挡鲁棒性，但在大面积遮挡下仍可能失败（Figure A2 展示了失败案例）。此时记忆检索缺乏足够的可见结构来推断缺失部分。
- **对参考图像的依赖。** 训练需要参考图像 $I_{ref}$ 提供背景信息。在视频数据集上可利用相邻帧，但在静态图像数据集（如 CUB-200-2011）上依赖随机掩码策略，可能限制泛化能力。
- **关键点语义一致性未完全保证。** 作为无监督方法，PPL 无法保证预测关键点的语义一致性（如“左肩”始终对应同一索引），这是该领域共有的局限。Figure A8 展示了语义一致性可视化，但未提供量化指标。

### 4. 开放问题与后续方向

基于上述分析，以下方向值得探索：

- **3D 先验扩展。** 如何将分层记忆蒸馏框架扩展到 3D 姿态先验，以处理 3D 旋转和形状变化？这可能涉及记忆库结构从 2D 坐标到 3D 骨架的重新设计。
- **更强主干网络的整合。** 当前特征提取器 $\phi_{enc}$ 基于标准 CNN，能否整合 Vision Transformer 等更强主干以提升先验学习精度？
- **减少对参考图像的依赖。** 能否通过生成式填充或上下文编码器替代参考图像，实现完全单张图像的自监督姿态估计？
- **先验的迁移与复用。** 学习到的类别先验能否推广到更多下游任务？Table A5 初步展示了先验在遮挡图像分类上的迁移效果，但更广泛的任务（如动作识别、场景理解）仍需验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Pose_Prior_Learner_Unsupervised_Categorical_Prior_Learning_for_Pose_Estimation.pdf]]
