---
title: "TokenHMR: Advancing Human Mesh Recovery with a Tokenized Pose Representation"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/TokenHMR_Advancing_Human_Mesh_Recovery_with_a_Tokenized_Pose_Representation.pdf
aliases:
- TokenHMR
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 两个关键调节节点：(1) 阈值自适应损失缩放（TALS）：利用BEDLAM合成数据量化因错误相机造成的不可避免2D误差阈值，对小于阈值的损失进行缩放，避免网络为了拟合2D而篡改3D姿态；(2) 基于VQ-VAE的姿态令牌化：将连续SMPL姿态回归转换为离散令牌预测，冻结的解码器和码本构成无偏的“有效姿态词汇”，约束输出姿态的合理性，降低歧义。
primary_logic: 通过精确测量错误相机模型下真实3D身体与2D投影之间的误差，可以确定一个有效阈值，仅对超出预期的大误差施加常规惩罚，对小误差则减弱监督，从而防止网络为谋求虚假2D一致性而牺牲3D精度；同时，离散令牌化姿态表示内建了均匀的姿态先验，不偏向于高频出现的姿态，有效提升了遮挡情况下的鲁棒性。
claims:
- 使用HMR2.0相机投影真实3D姿态得到的2D PCK低于HMR2.0自身预测的PCK，证明追求过高2D精度必然导致3D姿态偏离真实。
- 通过优化目标在保持2D对齐的前提下最大化3D误差，MPJPE在100次迭代后即可达146mm，200次后超300mm，证实2D对齐可掩盖严重的深度误差。
- TokenHMR在EMDB上相比HMR2.0将MPJPE从99.3mm降至91.7mm（降幅7.6%），在3DPW上从77.4mm降至71.0mm，验证了TALS与令牌化的协同效果。
- 离散化本身仅引入约2.5mm的3D精度损失，远小于SOTA方法在真实数据上的误差，表明令牌化代价极小。
---

# TokenHMR: Advancing Human Mesh Recovery with a Tokenized Pose Representation

> [!tip] 核心洞察
> 通过精确测量错误相机模型下真实3D身体与2D投影之间的误差，可以确定一个有效阈值，仅对超出预期的大误差施加常规惩罚，对小误差则减弱监督，从而防止网络为谋求虚假2D一致性而牺牲3D精度；同时，离散令牌化姿态表示内建了均匀的姿态先验，不偏向于高频出现的姿态，有效提升了遮挡情况下的鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | TokenHMR：利用令牌化姿态表示推动人体网格恢复 |
| 英文题名 | TokenHMR: Advancing Human Mesh Recovery with a Tokenized Pose Representation |
| 会议/期刊 | CVPR 2024 |
| Links |  [paper](https://arxiv.org/abs/2404.16752)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | TokenHMR |
| Dataset | EMDB, 3DPW |

> [!tip] 效果简介
> - EMDB 上，MPJPE 91.7 vs 99.3 (HMR2.0) (-7.6% (‑7.6 mm))；PA-MPJPE 55.6 vs 62.8 (HMR2.0) (-11.5% (‑7.2 mm))。
> - 3DPW 上，MPJPE 71.0 vs 77.4 (HMR2.0) (-8.3% (‑6.4 mm))。

## 概述

### 核心问题
现有单图像3D人体姿态与形状（HPS）回归方法面临一个根本性矛盾：网络为追求高2D关键点对齐，往往扭曲3D姿态，导致3D精度反而下降。这一“相机/姿态偏差”的根源在于，主流方法普遍采用错误的弱透视或固定内参相机模型，并依赖伪GT和2D监督——当相机模型本身存在系统误差时，强行拟合2D投影必然牺牲3D几何的真实性。

### 核心洞察
本文通过定量实验揭示了这一偏差的严重性：使用HMR2.0的相机将真实3D姿态投影至图像，其2D PCK反而不及HMR2.0自身预测结果（Figure 2b）；在刻意优化2D对齐的同时，仅需100次迭代即可将MPJPE推高至146mm，200次后超过300mm（Figure 2c）。这表明，**2D对齐与3D精度之间存在不可调和的权衡**，且现有方法在追求虚假2D一致性的过程中系统性地牺牲了3D真实性。

### 方法定位
TokenHMR通过两个关键调节节点打破上述权衡：

1. **阈值自适应损失缩放（TALS）**：利用BEDLAM合成数据量化因错误相机造成的不可避免的2D误差阈值，对小于阈值的损失进行缩放（权重约0.01），从而阻止网络为拟合2D而篡改3D姿态。
2. **基于VQ-VAE的姿态令牌化**：将连续SMPL姿态回归转换为离散令牌预测，冻结的解码器和码本构成无偏的“有效姿态词汇”，约束输出姿态的合理性，降低歧义。

### 主要结果
在多个in-the-wild基准上，TokenHMR取得显著提升：EMDB上MPJPE从HMR2.0的99.3mm降至91.7mm（降幅7.6%），3DPW上从77.4mm降至71.0mm（降幅8.3%）。离散化本身仅引入约2.5mm的3D精度损失，远小于SOTA方法在真实数据上的误差。消融实验证实TALS与令牌化存在协同效应，且TokenHMR对图像裁剪扰动具有更强的鲁棒性。

## 背景与动机

从单张图像中恢复三维人体姿态与形状（HPS）是计算机视觉的核心任务之一，其应用涵盖动作捕捉、人机交互、增强现实等领域。近年来，基于回归的方法取得了显著进展，但一个根本性的瓶颈始终未被正视：**现有方法在追求高精度二维投影对齐时，往往以牺牲三维姿态精度为代价**，形成了一种“二维对齐与三维精度不可兼得”的困境。

### 相机/姿态偏差：被忽视的系统性误差

当前主流方法（如 **HMR2.0**、**CLIFF** 等）普遍采用弱透视相机模型或假设固定的相机内参。这种简化假设与实际成像几何之间存在系统性偏差，导致网络在学习过程中发展出一种“作弊”策略——通过扭曲三维姿态来换取二维关键点的高精度对齐。具体而言，当相机焦距不准确时，原本因透视缩短而应在图像中呈现较短投影的肢体（如指向相机的小腿），会被网络错误地估计为弯曲状态，以匹配二维标注（见 Figure 2a）。

作者通过两项定量实验揭示了这一偏差的严重性：

1. **相机偏差的直接证据**：使用 HMR2.0 的相机参数将真实三维姿态投影到图像平面，其 PCK 指标反而低于 HMR2.0 自身预测结果的 PCK（PCK@0.5 从 0.78 降至 0.66，PCK@1.0 从 0.88 降至 0.86）。这表明追求过高的二维精度必然要求三维姿态偏离真实值（见 Figure 2b）。

2. **二维对齐掩盖深度误差**：通过构造一个同时最大化三维误差和保持二维对齐的优化目标（见公式 1），实验显示仅需 100 次迭代即可将 MPJPE 推至 146mm，200 次后超过 300mm，而二维投影依然高度对齐。这证实了“二维对齐良好”绝非三维精度可靠的充分条件（见 Figure 2c）。

### 伪GT监督的放大效应

为提升在真实场景中的泛化能力，现有方法大量依赖“伪真值”（pseudo-ground truth，p-GT）——由其他模型预测的二维关键点和三维姿态参数——作为监督信号。然而，这些 p-GT 本身就携带着前述相机/姿态偏差，当网络以同等权重拟合所有 p-GT 误差时，偏差被进一步放大，形成恶性循环。实验表明，在标准训练数据（SD）基础上加入真实场景数据（ITW）后，HMR2.0 在 EMDB 上的三维精度反而下降超过 17%，这正是 p-GT 噪声与相机偏差叠加的后果。

### 姿态先验的缺失与偏向

从单目图像回归三维姿态本质上是欠约束问题，需要有效的姿态先验来规约解空间。现有方法或完全依赖数据驱动隐式学习先验，或使用 **VPoser** 等基于 VAE 的显式先验。但 VAE 先验存在内在偏向——它倾向于生成训练集中出现频率较高的常见姿态，对罕见或极端姿态的约束力不足，且在遮挡场景下容易产生不合理的预测。

### 本文动机

综上所述，现有方法面临的核心矛盾可归结为：**错误的相机模型与不加区分的监督信号共同导致网络为追求虚假的二维一致性而牺牲三维精度**。解决这一矛盾需要同时从两个层面入手：（1）设计一种能够区分“合理误差”与“异常误差”的监督机制，避免网络为拟合由相机偏差引起的微小二维误差而篡改三维姿态；（2）构建一个均匀、无偏的姿态先验，以知识库的形式约束输出姿态的合理性，尤其在歧义性高的场景下提供有效引导。TokenHMR 正是围绕这两个关键调节节点展开设计。

## 核心创新

TokenHMR 的核心创新并非提出全新的网络架构，而是通过**重新定义损失函数与姿态表示**，系统性地缓解了单目 3D 人体姿态估计中长期存在的“相机/姿态偏差”问题。该方法在主流回归范式（以 HMR2.0 为基线）的基础上，精准替换了两个关键模块：**监督信号**与**姿态表示空间**。

### 1. 阈值自适应损失缩放（TALS）：重新校准监督信号

现有方法普遍采用弱透视或固定内参的相机模型，并依赖伪 GT（pseudo-ground-truth）与 2D 关键点进行监督。这形成了一个有害的优化陷阱：网络为追求更高的 2D 对齐精度，会篡改 3D 姿态以补偿错误的相机投影，导致 3D 精度反而下降。TokenHMR 通过 TALS 损失精确地切断了这一负反馈循环。

**因果机制**：TALS 的核心思想是，错误相机模型本身会引入一个**不可避免的 2D 误差下限**。利用 BEDLAM 合成数据集提供的真实 3D 标注与标准（错误）相机模型，TokenHMR 预先量化了每个关节的期望误差阈值（见 Table S.1）。在训练时，TALS 对损失进行分段处理：

- 当 2D 重投影误差或伪 GT 姿态误差**超出**该阈值时，按常规力度惩罚（L1/L2 损失），迫使网络修正显著的偏差。
- 当误差**低于**阈值时，损失被大幅缩放（权重 $\alpha \approx 0.01$），从而阻止网络为追求虚假的 2D 一致性而扭曲 3D 姿态。

形式上，TALS 分别应用于伪 GT 姿态损失与 2D 关节损失：

$$ \mathcal{L}_{\theta_{pGT}} = \begin{cases} \Vert \boldsymbol{\theta} - \boldsymbol{\theta_g} \Vert^2 & \text{if } \mathcal{L}_{\theta_{pGT}} > \varepsilon_\theta \\ \alpha_\theta \cdot \Vert \boldsymbol{\theta} - \boldsymbol{\theta_g} \Vert^2 & \text{otherwise} \end{cases} $$

$$ \mathcal{L}_{J_{2D_{pGT}}} = \begin{cases} |J_{2D} - J_{2D_g}| & \text{if } \mathcal{L}_{J_{2D_{pGT}}} > \varepsilon_{J_{2D}} \\ \alpha_{J_{2D}} \cdot |J_{2D} - J_{2D_g}| & \text{otherwise} \end{cases} $$

**证据强度**：该设计的必要性由论文第 3 节的实验强力支撑。使用 HMR2.0 的相机投影真实 3D 姿态时，2D PCK 指标反而低于 HMR2.0 自身的预测值（PCK0.5: 0.66 vs 0.78），直接证实了“追求过高 2D 精度必然导致 3D 姿态偏离真实”。进一步的对抗性优化实验表明，在保持 2D 对齐的前提下，仅 100 次迭代即可使 MPJPE 达到 146mm，200 次后超过 300mm，揭示了 2D 对齐对巨大深度误差的惊人掩盖能力。

### 2. 姿态令牌化：将回归转化为分类

TokenHMR 的第二个关键创新是将连续的 SMPL 姿态回归问题转化为**离散令牌预测问题**。这并非简单的表示压缩，而是为回归器内建了一个无偏的姿态先验。

**因果机制**：该方法分两阶段运行。首先，在 AMASS 等运动捕捉数据上训练一个 VQ-VAE，其编码器将连续姿态映射为离散令牌，解码器从令牌重建姿态。训练完成后，**冻结的解码器与码本**构成了一个“有效姿态词汇表”。在 TokenHMR 的主干网络中，Transformer 解码器不再直接回归 72 维 SMPL 姿态参数，而是通过一个 4 层 MLP 输出 logits $\mathcal{Q}$（尺寸 $160 \times 2048$），随后通过 softmax 加权码本获得近似量化特征：

$$ \bar{z} = \sigma(\mathcal{Q}_{160 \times 2048}) \times CB_{2048 \times 256} \approx \hat{z} $$

该特征被送入冻结的解码器，生成最终的 3D 身体姿态。

这一设计带来了双重收益：
1.  **均匀先验**：与 VPoser 等倾向于高频姿态的 VAE 先验不同，VQ-VAE 码本通过均匀离散化，为所有有效姿态提供了**等概率的表示空间**，对稀有或遮挡姿态的鲁棒性更强。
2.  **误差约束**：任何预测的姿态都被强制投影到“有效姿态词汇”中，从根本上杜绝了生成生理上不可能的姿态。

**证据强度**：消融实验（Table 1）清晰展示了令牌化与 TALS 的协同效应。单独使用令牌化表示（HMR2.0 + Token）已将 EMDB 上的 MPJPE 从 99.3mm 降至 95.6mm；与 TALS 结合后（即完整 TokenHMR），进一步降至 91.7mm。离散化引入的固有精度损失极小，仅约 2.5mm，比当前 SOTA 方法在真实数据上的误差小 20 倍，代价几乎可以忽略。

### 3. 方法谱系与知识库定位

TokenHMR 处于“回归范式改良”与“离散表示学习”的交叉点。其直接基线 **HMR2.0** 代表了纯连续回归的 SOTA。与引入相机近似的 **CLIFF** 或基于反向动力学的 **HybrIK** 不同，TokenHMR 选择在不改变相机模型的前提下，通过损失重校准与表示离散化来对抗偏差。其 VQ-VAE 码本的角色类似于一个**显式知识库**，存储了从大规模运动数据中提取的“有效姿态词汇”，这与依赖隐式先验的传统方法形成了鲜明对比。

**失败模式与边界**：TALS 的宽松 2D 监督在强透视畸变下可能导致投影对齐不佳（Figure S.2）；令牌化虽约束了姿态合理性，但无法解决因相机缺失导致的深度方向根本歧义；全局方向估计在缺乏面部或脚部线索时仍会失败。这些限制表明，该方法是对现有回归范式的强有力补丁，但未从根本上解决单目相机内参估计这一开放问题。

## 整体框架

TokenHMR 将单图像 3D 人体姿态与形状回归问题拆分为两个阶段：**姿态令牌化（Pose Tokenization）** 与 **令牌化姿态回归（Tokenized Pose Regression）**，其整体流程如图 3 所示。

### 第一阶段：姿态令牌化

该阶段的目标是构建一个离散的“有效姿态词汇”。具体而言，在 AMASS 等大规模运动捕捉数据上训练一个 VQ-VAE，其编码器将连续的 SMPL 身体姿态参数 $\theta$ 映射为潜在特征 $z$，再通过最近邻搜索在可学习的码本 $CB$ 中找到对应的离散令牌 $\hat{z}$：

$$ \hat{z}_i = \arg\min_{c_k \in CB} \| z_i - c_k \|_2 $$

解码器则根据这些离散令牌重建原始姿态。训练完成后，**码本和解码器被冻结**，作为下游回归器的无偏姿态先验知识库。该先验不偏向训练集中高频出现的常见姿态，对分布外姿态也具备一定的泛化重建能力（如对 MOYO 瑜伽姿态的重建，见 Figure S.1）。

### 第二阶段：令牌化姿态回归

TokenHMR 的主干网络沿用 HMR2.0 的 ViT-H/16 作为图像特征提取器，将输入图像编码为 token 序列。Transformer 解码器通过交叉注意力融合图像特征，输出每帧的潜在表示。在此基础上，系统包含以下并行预测头：

- **全局旋转、手部姿态、体型、弱透视相机参数**：分别由独立的线性层直接回归。
- **身体姿态**：不再直接回归连续 SMPL 参数，而是通过一个四层 MLP（含 GeLU 激活）将 Transformer 特征转换为 logits 矩阵 $\mathcal{Q}$（尺寸 $160 \times 2048$）。随后，利用 softmax 加权码本嵌入，得到近似量化特征 $\bar{z}$：

$$ \bar{z} = \sigma(\mathcal{Q}_{M \times K}) \times CB_{K \times D} \approx \hat{z} $$

该近似特征被送入冻结的 VQ-VAE 解码器，重建出连续的 SMPL 身体姿态参数。这一设计将连续回归转化为**离散令牌分类问题**，使预测姿态始终落在码本定义的“有效姿态”空间内，从而约束输出的合理性。

### 损失函数设计

TokenHMR 的总损失由三部分构成：

$$ \mathcal{L}_{Total} = \mathcal{L}_{GT} + \mathcal{L}_{\theta_{pGT}} + \mathcal{L}_{J_{2D_{pGT}}} $$

其中 $\mathcal{L}_{GT}$ 为标准的真值监督损失（包含姿态、体型、3D 关节和 2D 重投影项）。核心创新在于后两项引入了**阈值自适应损失缩放（TALS）**：当伪真值姿态损失或 2D 重投影误差低于预设阈值时，损失被大幅缩放（$\alpha \approx 0.01$），仅在误差超出阈值时才施加常规惩罚。这些阈值通过 BEDLAM 合成数据的真值 3D 姿态与错误相机模型投影之间的误差分析确定，旨在阻止网络为追求虚假的 2D 一致性而篡改 3D 姿态。

### 数据流总结

1. 输入图像 → ViT-H/16 → 图像 token 序列
2. 图像 token → Transformer 解码器 → 帧级潜在表示
3. 潜在表示 → 线性头 → 全局旋转、手部姿态、体型、相机参数
4. 潜在表示 → 4×MLP → logits $\mathcal{Q}$ → softmax 加权码本 → 近似量化特征 → 冻结解码器 → SMPL 身体姿态
5. 所有输出合并为 SMPL 参数 → 投影与监督 → TALS 调整的损失反向传播

整个流程中，**令牌化解码器始终冻结**，仅作为推理时的姿态生成器；可训练部分仅限于 ViT 主干、Transformer 解码器及各预测头。

### 补充图表

![[assets/figures/papers/paper_list_l17_TokenHMR_Advancing_Human_Mesh_Recovery_with_a_Tokenized_Pose_Representat_motion20/figures/003_Figure_3.jpg]]
*Figure 3: Framework overview. Our method has two stages. (a) In the tokenization step, the encoder learns to map continuous poses to discrete pose tokens and the decoder tries to reconstruct the original poses. (b) To train TokenHMR, we replace regression with classification using the pre-trained decoder, which provides a “vocabulary” of valid poses*

## 核心模块与公式推导

### 3.1 相机/姿态偏差的量化分析

TokenHMR 的核心动机源于对现有单图像 HPS 回归方法中“相机/姿态偏差”的系统性揭示。为量化这一偏差，作者设计了如下优化目标：

$$
w_{2D} \| \Pi(J_{3D}, \mathcal{T}) - J_{2D_g} \|_2 - w_{3D} \| J_{3D} - J_{3D_g} \|_2 + m
$$

其中 $\Pi$ 为弱透视投影，$\mathcal{T}$ 为相机参数，$m=20$ 为裕度，$w_{2D}=4$，$w_{3D}=40.5$。该损失在**保持 2D 对齐的同时最大化 3D 误差**，用以验证 2D 对齐能否掩盖严重的深度错误。实验表明，仅 100 次迭代后 MPJPE 即达 146mm，200 次后超过 300mm，而 2D 投影仍保持高度对齐（Fig. 2(c)）。这确证了现有方法为追求高 2D 精度而牺牲 3D 姿态准确性的根本矛盾。

![[assets/figures/papers/paper_list_l17_TokenHMR_Advancing_Human_Mesh_Recovery_with_a_Tokenized_Pose_Representat_motion20/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of the camera/pose bias issues. (a) The lack of correct focal length means that foreshortened legs are estimated as bent by methods like HMR2.0. (b) Replacing the predicted body poses with ground truth reveals camera bias; (c) Maintaining 2D alignment, how wrong can the 3D poses be? See Sec. 3 for details*

---

### 3.2 阈值自适应损失缩放（TALS）

针对上述瓶颈，TALS 通过量化错误相机模型下的不可避免误差，确定有效阈值，对低于阈值的损失进行缩放，防止网络为拟合 2D 而篡改 3D 姿态。具体而言，利用 BEDLAM 合成数据的真实 3D 标注与标准错误相机模型，为每个 2D 关键点和 SMPL 关节计算预期误差阈值（详见 Table S.1）。

**伪 GT 姿态损失**：

$$
\mathcal{L}_{\theta_{pGT}} = \begin{cases} \| \boldsymbol{\theta} - \boldsymbol{\theta_g} \|^2 & \text{if } \mathcal{L}_{\theta_{pGT}} > \varepsilon_\theta \\ \alpha_\theta \cdot \| \boldsymbol{\theta} - \boldsymbol{\theta_g} \|^2 & \text{otherwise} \end{cases}
$$

当姿态损失超过关节阈值 $\varepsilon_\theta$ 时施以平方惩罚，否则缩放至 $\alpha_\theta$ 倍（$\alpha_\theta \approx 0.01$）。

**伪 GT 2D 关节损失**：

$$
\mathcal{L}_{J_{2D_{pGT}}} = \begin{cases} |J_{2D} - J_{2D_g}| & \text{if } \mathcal{L}_{J_{2D_{pGT}}} > \varepsilon_{J_{2D}} \\ \alpha_{J_{2D}} \cdot |J_{2D} - J_{2D_g}| & \text{otherwise} \end{cases}
$$

当 2D 重投影误差超过阈值 $\varepsilon_{J_{2D}}$ 时施以 L1 惩罚，否则缩放至 $\alpha_{J_{2D}}$ 倍。这一机制使得网络仅对超出预期的**大误差**保持常规监督强度，而对因错误相机导致的**小误差**大幅减弱监督信号，从而阻断相机/姿态偏差的传导路径。

---

### 3.3 VQ-VAE 姿态令牌化

TokenHMR 将连续 SMPL 姿态回归转化为离散令牌预测。首先训练一个 VQ-VAE 将身体姿态参数量化为码本中的离散条目。

**量化过程**：编码器将姿态映射为潜在特征 $z_i$，通过最近邻搜索映射到码本 $CB$：

$$
\hat{z}_i = \arg\min_{c_k \in CB} \| z_i - c_k \|_2
$$

**VQ-VAE 总损失**：

$$
\mathcal{L}_{\mathcal{VQ}} = \lambda_{\mathcal{RE}}\mathcal{L}_{\mathcal{RE}} + \lambda_{\mathcal{E}} \| sg[z] - e \|_2 + \lambda_{\mathcal{C}} \| z - sg[e] \|_2
$$

其中 $\lambda_{\mathcal{RE}}=50$、$\lambda_{\mathcal{E}}=1$、$\lambda_{\mathcal{C}}=1$，$sg[\cdot]$ 为停止梯度算子。三项分别对应重建损失、码本嵌入损失和承诺损失。

**重建损失**：

$$
\mathcal{L}_{\mathcal{RE}} = \mathcal{L}_1(\theta_g, \theta) + \mathcal{L}_1(J_{3D_g}, J_{3D})
$$

同时监督姿态参数 $\theta$ 和 3D 关节位置 $J_{3D}$ 的 L1 重建。

**可微分近似**：由于 $\arg\min$ 不可微分，训练 TokenHMR 时采用 softmax 加权近似：

$$
\bar{z} = \sigma(\mathcal{Q}_{\mathcal{M} \times \mathcal{K}}) \times CB_{\mathcal{K} \times \mathcal{D}} \approx \hat{z}
$$

其中 $\mathcal{Q}$ 为网络输出的 logits（$160 \times 2048$），$\sigma$ 为 softmax，$CB$ 为冻结的码本。该近似特征 $\bar{z}$ 经冻结的 VQ-VAE 解码器生成连续身体姿态。

---

### 3.4 TokenHMR 总损失

**GT 监督损失**：

$$
\mathcal{L}_{GT} = \lambda_\theta \mathcal{L}_\theta(\theta, \theta_g) + \lambda_\beta \mathcal{L}_\beta(\beta, \beta_g) + \lambda_{3D} \mathcal{L}_{3D}(\mathbf{J}_{3D}, \mathbf{J}_{3D_g}) + \lambda_{2D} \mathcal{L}_{2D}(\mathbf{J}_{2D}, \mathbf{J}_{2D_g})
$$

包含姿态、体型、3D 关节和 2D 重投影四项标准监督。

**最终总损失**：

$$
\mathcal{L}_{Total} = \mathcal{L}_{GT} + \mathcal{L}_{\theta_{pGT}} + \mathcal{L}_{J_{2D_{pGT}}}
$$

将标准 GT 损失与经 TALS 调整的伪 GT 姿态损失和 2D 关节损失相加。两个调节节点——TALS 的阈值缩放机制与令牌化表示的离散先验——在此统一，共同约束网络在保持合理 2D 对齐的同时输出 3D 准确的姿态。

## 实验与分析

### 核心瓶颈验证：2D对齐与3D精度的根本性冲突

TokenHMR的实验设计首先系统性地验证了其核心动机——现有方法中2D对齐与3D精度之间存在不可调和的权衡。作者设计了两个关键实验来量化这种相机/姿态偏差：

**实验一：GT投影揭示相机偏差。** 使用HMR2.0的相机模型将BEDLAM数据集的真实3D姿态投影到2D图像上，计算PCK指标。结果显示，使用真实3D姿态得到的PCK@0.5仅为0.66、PCK@1.0为0.86，而HMR2.0自身预测结果分别为0.78和0.88（见Figure 2(b)）。这意味着：**HMR2.0为了获得更高的2D对齐分数，其预测的3D姿态已经偏离了真实值**——网络通过扭曲3D姿态来补偿错误相机模型带来的投影误差。

**实验二：2D对齐可掩盖巨大深度误差。** 作者设计了一个对抗性优化目标（Eq.1），在保持2D重投影损失极小的同时最大化3D关节误差：
$$w_{2D} \| \Pi(J_{3D}, \mathcal{T}) - J_{2D_g} \|_2 - w_{3D} \| J_{3D} - J_{3D_g} \|_2 + m$$
其中 $m=20$，$w_{2D}=4$，$w_{3D}=40.5$。经过仅100次迭代，MPJPE即达到146mm；200次迭代后超过300mm（见Figure 2(c)）。**这一结果有力地证明了：在错误相机模型下，网络可以维持高度2D对齐，同时在深度方向产生巨大偏差。** 这构成了TALS损失设计的直接动机。

### 主要定量结果

Table 1给出了在EMDB和3DPW两个主要野外基准上的3D误差对比。在标准训练设置（SD+ITW+BL，即合成数据+互联网图像+BEDLAM）下：

| 方法 | EMDB MPJPE↓ | 3DPW MPJPE↓ | EMDB PA-MPJPE↓ |
|------|------------|------------|---------------|
| HMR2.0 | 99.3 | 77.4 | 62.8 |
| CLIFF | 100.9 | 76.4 | 63.9 |
| HybrIK | 110.1 | 79.0 | 69.6 |
| BEDLAM-CLIFF | 97.3 | 73.5 | 60.3 |
| **TokenHMR** | **91.7** | **71.0** | **55.6** |

TokenHMR相比HMR2.0在EMDB上MPJPE降低7.6mm（降幅7.6%），在3DPW上降低6.4mm（降幅8.3%），PA-MPJPE降低7.2mm（降幅11.5%）。值得注意的是，TokenHMR也显著优于同样使用BEDLAM数据训练的BEDLAM-CLIFF，表明其优势并非仅来自额外训练数据，而是源于TALS和令牌化表示的方法创新。

### 消融实验：TALS与令牌化的协同效应

Table 1中的消融行揭示了两个核心组件的独立贡献与协同作用（以EMDB MPJPE为指标）：

- **HMR2.0基线**：99.3mm
- **HMR2.0 + TALS**：96.7mm（−2.6mm）——单独添加TALS损失，通过降低对伪GT和小2D误差的惩罚，已能显著提升3D精度
- **HMR2.0 + Token**：95.6mm（−3.7mm）——单独使用令牌化姿态表示，利用VQ-VAE码本提供的无偏先验约束，优于TALS单独使用
- **HMR2.0 + TALS + VPoser**：96.7mm——将TALS与传统的VAE先验（VPoser）结合，效果与仅用TALS持平，说明VPoser偏向常见姿态的先验在此场景下未能提供额外增益
- **TokenHMR（TALS + Token）**：91.7mm（−7.6mm）——两者结合产生显著的协同效应，误差降幅远超各自单独贡献之和

这一消融序列清晰地表明：**TALS通过减弱对不可靠监督信号的依赖，为令牌化先验创造了发挥空间；而令牌化码本提供的均匀“有效姿态词汇”，则防止了TALS宽松监督可能引入的姿态退化。**

### Tokenizer配置消融

Table 3给出了VQ-VAE tokenizer的配置搜索实验。在AMASS测试集和MOYO验证集上评估重建误差：

- 码本大小2048×256、160个令牌的配置达到最佳平衡：AMASS MPJPE仅2.2mm，MOYO验证集MPJPE为10.4mm
- 增加噪声增强训练（最后一行带⋆）进一步提升了泛化能力
- 离散化引入的固有精度损失约2.5mm，相比SOTA方法在真实数据上50-100mm级别的误差，这一代价极小（约20倍差距）

值得注意的是，即使仅在AMASS上训练，tokenizer也能泛化重建MOYO中的瑜伽等分布外姿态（见Figure S.1的t-SNE可视化），验证了码本作为“有效姿态词汇”的泛化能力。

### 鲁棒性分析

Table 2评估了图像裁剪对3D精度的影响。在EMDB上对图像边界进行均匀裁剪：

| 裁剪比例 | TokenHMR MPJPE变化 | HMR2.0 MPJPE变化 |
|---------|-------------------|-----------------|
| 10% | +3.30 | +5.47 |
| 30% | +13.01 | +17.31 |
| 50% | +34.28 | +38.59 |

TokenHMR在所有裁剪比例下均表现出更小的性能恶化。这表明离散令牌化姿态表示通过限制输出空间到有效姿态流形，减少了对图像边界信息的过度依赖，从而提升了遮挡和不完整观测下的鲁棒性。

### 失败模式与局限性

作者在Figure S.2和文中明确指出了TokenHMR的几类典型失败模式：

1. **2D对齐退化**：TALS的宽松2D监督在强透视畸变场景下可能导致投影关节与图像观测出现可见偏差。这是TALS设计的内在权衡——为保护3D精度而有意降低对2D精度的要求。

2. **深度方向歧义**：尽管TALS和令牌化缓解了相机/姿态偏差，但单目设置下的深度模糊性并未根本解决。当缺乏足够的透视线索时，网络仍可能在深度方向产生误判。

3. **全局方向估计失败**：在缺乏面部、脚部等明显方向线索的图像中，全局旋转预测可能出现错误。这与身体姿态令牌化主要约束相对姿态、而全局方向由独立线性头预测的架构设计有关。

4. **离散化精度瓶颈**：约2.5mm的固有令牌化损失在大多数场景下可忽略，但在对精度要求极高的应用中可能成为限制因素。

5. **相机模型根本性限制**：方法未直接解决单目相机内参和外参的准确估计问题，因此未能从根本上消除错误相机模型引入的偏差。

### 补充图表

![[assets/figures/papers/paper_list_l17_TokenHMR_Advancing_Human_Mesh_Recovery_with_a_Tokenized_Pose_Representat_motion20/figures/004_Table_1.jpg]]
*Table 1: 3D human mesh and pose errors on the EMDB and 3DPW datasets. See text*

![[assets/figures/papers/paper_list_l17_TokenHMR_Advancing_Human_Mesh_Recovery_with_a_Tokenized_Pose_Representat_motion20/figures/005_Table_2.jpg]]
*Table 2: Impact of evenly cropping images at different ratios from the boundaries on the 3D HPS accuracy on the EMDB dataset. The numbers in (parentheses) indicate the changes in performance relative to the non-cropped scenario; smaller is better. All models compared here employ identical backbones and are trained on the same data*

![[assets/figures/papers/paper_list_l17_TokenHMR_Advancing_Human_Mesh_Recovery_with_a_Tokenized_Pose_Representat_motion20/figures/006_Table_3.jpg]]
*Table 3: Tokenizer Ablation. All methods are trained on the standard training set of AMASS [37] and evaluated on the test set of AMASS and validation set of MOYO [52] except the last row⋆, which is trained with the MOYO training set. The last model is used as the tokenizer in TokenHMR*

![[assets/figures/papers/paper_list_l17_TokenHMR_Advancing_Human_Mesh_Recovery_with_a_Tokenized_Pose_Representat_motion20/figures/008_Table.jpg]]
*Table: S.1. Thresholds for 44 2D joints and 24 SMPL joints. 2D joint names start with the skeleton origin, where OP stands for OpenPose. LSP, MPII, and H36M are the datasets*

![[assets/figures/papers/paper_list_l17_TokenHMR_Advancing_Human_Mesh_Recovery_with_a_Tokenized_Pose_Representat_motion20/figures/009_Figure.jpg]]
*Figure: S.1. t-SNE visualization of unseen poses (3D body joints) reconstructed by our tokenizer trained on AMASS only. We are able to reconstruct the out-of-distribution Yoga poses from MOYO. GT is ground-truth poses and PR is predicted poses. a) Due to the loose supervision of TALS, our prediction does not align well in 2D under weak-perspective camera. b) Depth-wise ambiguity is still very challenging. c) Global orientation estimation sometimes fails because facial and foot cues are not thoroughly explored. Figure S.2. 2D alignment problem and failure cases*

## 方法谱系与知识库定位

### 1. 问题定位：单目HPS中的“相机/姿态偏差”陷阱

TokenHMR的核心贡献并非提出全新的网络架构，而是精准诊断并缓解了单图像3D人体姿态与形状（HPS）回归领域中一个长期被忽视的系统性缺陷——**相机/姿态偏差**。现有主流方法（如 **HMR2.0**、**CLIFF**、**HybrIK** 等）普遍采用弱透视相机模型或固定内参假设，并依赖伪GT（pseudo-GT）和2D关键点监督进行训练。这种训练范式形成了一个隐蔽的陷阱：网络为了追求高2D重投影对齐，会不自觉地扭曲3D姿态以适应错误的相机模型，导致3D精度随2D对齐增强反而下降。

这一现象的定量证据具有决定性：当使用HMR2.0的相机将BEDLAM合成数据中的真实3D身体投影到图像平面时，其2D PCK评分反而低于HMR2.0自身预测的PCK（PCK@0.5从0.78降至0.66，PCK@1.0从0.88降至0.86）。这直接证明了追求过高的2D精度必然导致3D姿态偏离真实。更令人警醒的是，通过优化目标在保持2D对齐的前提下最大化3D误差，MPJPE在100次迭代后即可达146mm，200次后超过300mm，而2D对齐几乎不受影响——深度方向的巨大误差被2D投影完美掩盖。

### 2. 方法谱系：从连续回归到离散令牌预测

TokenHMR在方法谱系上处于一个独特的交叉点，连接了三条技术路线：

**（1）单目HPS回归基线。** TokenHMR直接继承并改造了HMR2.0的架构主干（ViT-H/16 backbone + Transformer decoder），保留了对全局旋转、手部姿态、体型和相机的连续回归头。其关键改造在于将身体姿态的回归路径从连续参数预测替换为离散令牌分类，同时引入TALS损失重塑监督信号。在训练数据设置（SD+ITW+BL）完全相同的情况下，TokenHMR在EMDB上将MPJPE从HMR2.0的99.3mm降至91.7mm（降幅7.6%），在3DPW上从77.4mm降至71.0mm（降幅8.3%），PA-MPJPE在EMDB上从62.8mm降至55.6mm（降幅11.5%）。

**（2）姿态先验与知识库方法。** 传统方法如 **HMR2.0 + VPoser** 使用VAE学习连续潜在空间中的姿态先验，但VAE倾向于向高频出现的常见姿态收缩，形成有偏先验。TokenHMR改用VQ-VAE将连续SMPL姿态参数离散化为令牌序列，冻结的解码器和码本构成一个均匀无偏的“有效姿态词汇”。消融实验证实，单独使用令牌化表示（HMR2.0+Token）已优于基线（EMDB MPJPE: 95.6 vs 99.3），但与TALS结合后进一步降至91.7，证明离散先验与自适应损失存在协同效应。相比之下，HMR2.0+TALS+VPoser的组合效果不如TokenHMR，表明VAE先验的偏向性与TALS的阈值策略存在冲突。

**（3）合成数据驱动的阈值校准。** TALS阈值的确定依赖于BEDLAM合成数据集的精确3D真值。通过将BEDLAM的真实3D身体用标准错误相机模型投影，量化每个关节和姿态参数因相机不匹配产生的不可避免误差，从而为44个2D关节和24个SMPL关节分别建立了有效阈值。这种利用合成数据校准真实场景监督信号的做法，与 **BEDLAM-CLIFF** 直接使用合成数据训练的思路形成对比——TokenHMR将合成数据用于元层面的损失设计，而非直接作为训练样本。

### 3. 适用边界与局限性

**适用场景：** TokenHMR在野外场景（EMDB、3DPW）和遮挡/裁剪场景下表现尤为突出。在50%极端裁剪条件下，TokenHMR的MPJPE恶化幅度（+34.28）显著小于HMR2.0（+38.59），表明离散令牌化表示内置的姿态先验对不完整观测具有更强的鲁棒性。

**已知局限：**

1. **强透视畸变下的2D对齐退化。** TALS通过缩放低于阈值的损失来避免过拟合，但在焦距极短或透视效应强烈的场景中，宽松的2D监督可能导致投影对齐明显偏离图像观测，出现“3D正确但2D错位”的反向问题。

2. **深度歧义未根本解决。** 令牌化姿态表示和TALS均未直接估计相机内参/外参，因此无法从根本上消除因相机模型错误导致的深度方向几何误判。全局方向估计在缺乏面部、脚部等明显线索时仍会失败。

3. **离散化精度损失。** VQ-VAE令牌化过程引入约2.5mm的固有3D精度损失。虽然这一数值远小于SOTA方法在真实数据上的误差（约20倍差距），但在需要毫米级精度的应用中可能成为瓶颈。最佳tokenizer配置（160个令牌、码本大小2048×256）在AMASS测试集上MPJPE为2.2mm，在MOYO验证集上为10.4mm，表明对分布外瑜伽姿态的重建误差有所增大。

4. **对合成数据阈值的依赖。** TALS阈值的有效性依赖于BEDLAM数据集的相机模型与目标场景相机偏差的匹配程度。若实际应用中的相机模型与BEDLAM假设存在显著差异，预设阈值可能需要重新校准。

### 4. 开放问题与未来方向

1. **相机内参的可靠恢复。** 如何从单张图像中可靠估计焦距等相机内参，以彻底消除相机/姿态偏差，仍是该领域的核心挑战。若能将相机估计与令牌化姿态预测联合优化，有望从根本上解决2D对齐与3D精度之间的权衡。

2. **时序令牌化扩展。** 当前令牌化仅作用于单帧姿态，能否将离散姿态令牌扩展到时间维度，实现序列级运动令牌化？这将为视频理解、运动生成和动作识别提供统一的离散表示。

3. **与大型语言模型的桥接。** 姿态令牌的离散特性使其天然适合作为视觉-语言模型的输入/输出单元。将3D人体姿态纳入LLM的词汇表，有望实现更丰富的语义交互，如自然语言驱动的姿态编辑、运动描述生成等。

4. **精度损失的进一步压缩。** 如何通过改进VQ-VAE架构（如引入残差量化、层次化码本）或增大码本规模，进一步缩小甚至消除离散化引起的精度损失，是令牌化方法走向高精度应用的关键。

5. **相机偏差的替代解决方案。** TALS本质上是一种“治标”策略——通过降低有害监督的权重来避免过拟合。是否存在“治本”方案，例如通过多视角一致性、场景几何线索或元学习来隐式推断相机参数，值得进一步探索。

## 原文 PDF

![[paperPDFs/CVPR_2024/TokenHMR_Advancing_Human_Mesh_Recovery_with_a_Tokenized_Pose_Representation.pdf]]