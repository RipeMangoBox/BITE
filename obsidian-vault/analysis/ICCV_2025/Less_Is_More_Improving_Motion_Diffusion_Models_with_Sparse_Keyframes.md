---
title: "Less is More: Improving Motion Diffusion Models with Sparse Keyframes"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Less_Is_More_Improving_Motion_Diffusion_Models_with_Sparse_Keyframes.pdf
project_link: null
code_link: null
aliases:
- SMDMS
- LIMIMDMSK
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入稀疏关键帧掩码，仅在关键帧之间进行自注意力计算，并通过线性插值重建非关键帧特征；输入/输出层使用Lipschitz正则化平滑插值结果；推理后期动态更新掩码以聚焦关键帧。
primary_logic: 模仿专业动画师工作流，将运动生成聚焦于几何上有意义的稀疏关键帧，通过掩码自注意力与轻量插值替代密集帧处理，可在不牺牲质量的前提下显著降低训练开销，并提升文本对齐与运动真实感。
claims:
- sMDM在HumanML3D上FID达到0.130，远超基线MDM的0.544，且与检索增强的ReMoDiffuse（0.103）可比。
- sMDM-stella使用更大文本编码器后，Top‑1 R‑Precision达到0.554，在所有使用先进文本编码器的方法中最佳。
- 消融实验显示，去掉插值或Lipschitz层会导致FID和MM‑Dist显著变差，证明各组件均为必要。
- 动态掩码更新对大扩散步数模型尤为有效，例如在1000步设置下FID从0.291降至0.246。
---

# Less is More: Improving Motion Diffusion Models with Sparse Keyframes

> [!tip] 核心洞察
> 模仿专业动画师工作流，将运动生成聚焦于几何上有意义的稀疏关键帧，通过掩码自注意力与轻量插值替代密集帧处理，可在不牺牲质量的前提下显著降低训练开销，并提升文本对齐与运动真实感。

| 字段 | 内容 |
|------|------|
| 中文题名 | 少即是多：用稀疏关键帧改进运动扩散模型 |
| 英文题名 | Less is More: Improving Motion Diffusion Models with Sparse Keyframes |
| 会议/期刊 | ICCV 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Sparse Motion Diffusion Model (sMDM) |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID ↓ 0.130 (sMDM) vs 0.544 (MDM) (-0.414)；R‑Precision Top‑1 ↑ 0.494 (sMDM) vs 0.320 (MDM) (+0.174)；MM‑Dist ↓ 3.051 (sMDM) vs 5.566 (MDM) (-2.515)。
> - HumanML3D (with advanced text encoders) 上，R‑Precision Top‑1 ↑ 0.554 (sMDM‑stella) vs 0.510 (ReMoDiffuse) (+0.044)。

## 概要

### 问题与瓶颈

现有文本驱动的人体运动扩散模型（如**MDM**，Tevet et al., 2022）通常将运动序列建模为密集帧序列，在Transformer的自注意力层中对所有帧进行两两交互。这种设计带来两个核心瓶颈：

1. **计算效率低下**：自注意力的计算复杂度随帧数呈平方增长，训练和推理开销大。
2. **可控性不足**：密集表示难以突出几何上有意义的关键运动帧，导致模型容易忽略文本提示中的细节，生成的运动在语义对齐和真实感上表现欠佳。

### 核心洞察

本文的核心洞察来自专业动画师的工作流：**动画师仅绘制稀疏的关键帧，其余帧通过插值自动生成**。受此启发，论文提出将运动扩散模型的生成过程聚焦于稀疏关键帧，通过掩码自注意力与轻量插值替代密集帧处理，在不牺牲生成质量的前提下显著降低训练开销，并提升文本对齐与运动真实感。

### 方法定位

本文提出的**稀疏运动扩散模型（Sparse Motion Diffusion Model, sMDM）**以MDM的Transformer骨干为基础，引入三个关键改动：

- **关键帧掩码**：在自注意力层中仅让选定的关键帧参与计算，将注意力复杂度从 $O(N^2)$ 降至约 $O(K^2)$（$K \ll N$）。
- **特征空间插值**：在关键帧特征之间进行线性插值，重建非关键帧特征，避免直接建模全部帧。
- **Lipschitz MLP**：将输入/输出层的标准线性映射替换为Lipschitz约束的多层感知机，保证插值结果的平滑性。

训练时，关键帧通过**Visvalingam-Whyatt几何简化算法**自动选取；推理时，模型从均匀掩码开始，在扩散后期动态更新掩码以聚焦信息量更大的帧。

### 主要结果

在HumanML3D基准上，sMDM取得了显著的性能提升：

- **FID** 从MDM的0.544降至**0.130**，降幅达76%，且与检索增强的ReMoDiffuse（0.103）可比。
- **R-Precision Top-1** 从0.320提升至**0.494**，**MM-Dist**从5.566降至**3.051**。
- 使用更大文本编码器（Stella-1.5B）的sMDM-stella在Top-1 R-Precision上达到**0.554**，在同等使用先进文本编码器的方法中表现最佳。

消融实验进一步验证了各组件的必要性：去掉插值使FID升至0.267，去掉Lipschitz层使FID升至0.329，用随机关键帧替代几何选择使FID升至0.249。动态掩码更新在大扩散步数（如1000步）下尤为有效，可将FID从0.291进一步降至0.246。

### 方法谱系与知识库定位

sMDM属于**文本驱动运动扩散模型**这一研究方向，其直接基线包括MDM（Tevet et al., 2022）、MotionDiffuse（Zhang et al., 2022）等基于Transformer的密集帧扩散模型，以及检索增强的ReMoDiffuse（Zhang et al., 2023）。与这些方法相比，sMDM的独特贡献在于将**稀疏关键帧建模**的思想引入扩散框架，通过掩码注意力与插值机制实现效率与质量的双重提升。该方法还展示了良好的可迁移性：在Double Take长序列生成、Diffusion Planner实时角色控制等下游任务上，稀疏化变体（sPriorMDM、sDiP）均优于对应的密集基线。

### 局限性与开放问题

当前方法假设了Transformer的自注意力结构，在U-Net架构上的直接应用效果不佳（sCondMDI在运动插值任务上FID从0.153升至0.551）。此外，动态掩码更新在扩散步数较少（≤10）时提升有限，关键帧缩减率等超参数需针对数据集调整。值得进一步探索的方向包括：设计更适合稀疏帧输入的U-Net混合架构、引入速度/加速度等更多运动特征作为关键帧选择依据，以及将稀疏关键帧思想扩展到运动编辑、运动补全等更广泛的下游任务。

### 问题背景

文本驱动的人体运动生成旨在从自然语言描述中合成逼真的三维人体动作序列，在动画制作、游戏开发和人机交互中具有广泛应用。近年来，扩散模型在该领域取得了显著进展，代表性工作包括**MDM**（Tevet et al., 2022）、**MotionDiffuse**（Zhang et al., 2022）和**ReMoDiffuse**（Zhang et al., 2023）等。这些方法通常将运动序列建模为密集帧序列，通过Transformer自注意力机制在全部帧之间建立依赖关系。

### 现有方法的瓶颈

密集帧处理范式存在两个核心瓶颈：

**计算效率瓶颈**：自注意力计算复杂度随帧数平方增长（$O(N^2)$，其中$N$为帧数），导致训练和推理开销巨大。当运动序列较长或需要高帧率采样时，这一问题尤为突出。

**语义可控性瓶颈**：密集表示将每一帧同等对待，难以突出对运动语义起决定性作用的关键帧。这导致模型容易忽略文本提示中的细微语义细节——例如“缓慢行走然后突然奔跑”中的速度变化节点，或“挥手的同时下蹲”中的动作协调关系。基线模型MDM常出现遗漏部分文本指令的情况，生成的动作无法忠实反映输入描述的全部内容。

### 核心洞察与动机

本文的核心洞察来自专业动画师的工作流程：动画师并非逐帧绘制，而是先确定几何上有意义的**稀疏关键帧**（keyframes），再通过插值填充中间帧。这一观察启发作者将运动扩散模型的重心从密集帧转移到关键帧。

具体而言，本文提出**稀疏运动扩散模型（Sparse Motion Diffusion Model, sMDM）**，其动机在于：通过掩码自注意力仅在关键帧之间建模依赖，并借助轻量线性插值重建非关键帧特征，可以在不牺牲生成质量的前提下显著降低计算开销，同时提升文本对齐精度与运动真实感。

## 核心方法与创新机理

本工作提出**稀疏运动扩散模型（Sparse Motion Diffusion Model, sMDM）**，其核心创新在于将专业动画师“关键帧—插值”的工作流引入运动扩散模型，从根本上改变了密集帧序列的处理范式。与基线 **MDM**（Tevet et al., 2022）对所有帧进行全对全自注意力计算不同，sMDM 通过三个关键改动实现了“少即是多”的设计哲学。

### 稀疏关键帧掩码自注意力

sMDM 引入一个二值掩码 $M$，将自注意力计算严格限制在关键帧之间，非关键帧被完全排除在注意力机制之外。这一改动将自注意力复杂度从 $O(N^2)$ 降至约 $O(K^2)$（其中 $K \ll N$ 为关键帧数量），在训练和推理中均显著降低计算开销。掩码的引入并非随机的帧丢弃，而是基于几何显著性进行有信息量的帧筛选——训练阶段采用 **Visvalingam-Whyatt 几何简化算法**，通过计算相邻帧构成的三角形面积 $A_i = \frac{1}{2} \left| \det \begin{pmatrix} x_{i-1} & y_{i-1} & 1 \\ x_{i} & y_{i} & 1 \\ x_{i+1} & y_{i+1} & 1 \end{pmatrix} \right|$ 来量化每帧的几何重要性，保留运动轨迹中变化最显著的时刻。

### 特征空间线性插值重建

密集帧序列的恢复不依赖额外的生成模块，而是在关键帧的**特征空间**中进行线性插值来重建非关键帧特征。这一设计的精妙之处在于：插值操作发生在 Transformer 内部的特征表示层面，而非原始运动数据的坐标空间，使得非关键帧能够继承关键帧的高层语义信息，同时保持运动轨迹的平滑性。消融实验证实，去掉插值模块（仅计算关键帧损失）会导致 FID 从 0.130 升至 0.267，且生成多样性显著下降。

### Lipschitz 正则化平滑约束

为保证插值重建的平滑性，sMDM 将输入/输出层的标准线性映射替换为 **Lipschitz MLP**（采用正弦激活函数），并附加 Lipschitz 正则化损失 $\mathcal{L}_{\mathrm{lip}} = \prod_i \mathrm{softplus}(\|\mathbf{W}_i\|_p)$。该约束强制网络输出对输入变化有界——$\| g_{\theta}(y_1) - g_{\theta}(y_2) \|_p \leq \alpha \| y_1 - y_2 \|_p$——从而抑制插值过程中可能出现的抖动与伪影。去掉 Lipschitz 层后 FID 升至 0.329，证明平滑约束对高质量重建不可或缺。

### 推理期动态掩码更新

区别于训练时从干净样本 $x_0$ 静态确定关键帧，推理阶段 sMDM 采用**动态掩码更新策略**：在扩散前期（$t > \gamma T$）使用均匀掩码保持探索性，当去噪步数降至阈值 $T' = \gamma \cdot T$ 以下时，从当前中间去噪结果 $x_t$ 中重新运行 Visvalingam-Whyatt 算法，动态优化关键帧集合。这一策略使模型在扩散后期能够聚焦于当前已显现的运动结构，对大步数模型效果尤为显著——1000 步设置下 FID 从 0.291 降至 0.246。

### 方法定位

上述四个模块构成一个轻量级框架，**无需改变 MDM 的 Transformer 骨干架构**即可嵌入。这种非侵入式设计使得 sMDM 能够直接继承预训练权重，并在 HumanML3D 上以极低的额外复杂度实现 FID 0.130，远超原始 MDM 的 0.544，与检索增强的 SOTA 方法 **ReMoDiffuse**（Zhang et al., 2023）的 0.103 可比。当配备更大文本编码器（Stella-1.5B）时，sMDM-stella 的 Top-1 R-Precision 达到 0.554，在所有使用先进文本编码器的方法中取得最优。

**Sparse Motion Diffusion Model (sMDM)** 以**MDM**（Tevet et al., 2022）的Transformer运动扩散骨干为基础，将生成过程聚焦于稀疏关键帧，通过“掩码—插值—平滑”三阶段管线实现高效、可控的运动生成。整体pipeline如下：

### 1. 关键帧选择与掩码生成

给定长度为$N$的运动序列，首先通过**Visvalingam-Whyatt几何简化算法**识别几何上有意义的帧作为关键帧，生成二值掩码$M \in \{0,1\}^N$，关键帧标记为1，非关键帧标记为0。训练时，掩码由干净样本$\mathbf{x}_0$计算得到；推理时，初始采用均匀掩码，在扩散后期（$t \leq \gamma T$）从当前去噪中间结果$\mathbf{x}_t$动态重新选择关键帧，以聚焦信息量最大的帧。

### 2. 掩码自注意力

在Transformer的自注意力层中，仅允许关键帧之间进行注意力计算，非关键帧被排除在外。这一步将注意力复杂度从$O(N^2)$降至约$O(K^2)$（$K$为关键帧数量），是降低训练和推理开销的核心机制。

### 3. 特征插值重建

自注意力输出的关键帧特征通过**线性插值**在特征空间中重建非关键帧特征，恢复完整帧序列。这一轻量级操作替代了密集帧的直接计算，在保持运动连续性的同时避免引入大量参数。

### 4. Lipschitz平滑约束

输入和输出层的标准线性映射被替换为**Lipschitz MLP**（采用正弦激活函数），并附加Lipschitz正则化损失$\mathcal{L}_{\mathrm{lip}}$。该约束保证输入微小变化不会导致输出剧烈波动，使插值重建的运动序列更加平滑自然。

### 5. 训练与推理流程

- **训练阶段**：前向扩散按标准DDPM过程逐步加噪（Eq. 1），去噪网络直接预测干净样本$\hat{\mathbf{x}}_0$，损失函数为$\mathcal{L} = \|\mathbf{x}_0 - \hat{\mathbf{x}}_0\|^2 + \lambda \mathcal{L}_{\mathrm{lip}}$（Eq. 4）。掩码由真实运动序列预计算，训练全程固定。
- **推理阶段**：从随机噪声出发逐步去噪。前期使用均匀掩码保证探索多样性；当扩散步数降至阈值$\gamma T$以下时，触发**动态掩码更新**——对当前$\mathbf{x}_t$重新运行Visvalingam-Whyatt算法，优化关键帧集合，使后期去噪聚焦于已初步成形的运动结构。

### 6. 输入输出流

文本提示经CLIP ViT-B/32（63M）编码后，与带噪运动序列的帧特征一同输入Transformer骨干。经掩码自注意力、插值重建和Lipschitz MLP映射后，输出预测的干净运动序列$\hat{\mathbf{x}}_0$。整个过程保持与MDM相同的架构接口，改动集中在帧级别的掩码与插值操作上，因此该方法可泛化至多种基于Transformer的运动扩散模型（如**MotionDiffuse**、**PriorMDM**等），但对U-Net架构的直接迁移效果不佳（见局限性讨论）。

![[assets/figures/papers/paper_list_l1891_Less_Is_More_Improving_Motion_Diffusion_Models_with_Sparse_Keyframes/figures/002_Figure_2.jpg]]
*Figure 2: Model architectures of Sparse Motion Diffusion Model (sMDM). Our sMDM uses a binary keyframe mask M to exclude nonkeyframes from the self-attention layers. During training, M is derived from the clean input x0 via keyframe selection [40]. At inference, the model starts with a uniform keyframe mask at earlier timesteps*

### 3.1 运动扩散基础

本文沿用基于Transformer的运动扩散模型范式（MDM, Tevet et al., 2022），将运动序列表示为 $\mathbf{x}_0 \in \mathbb{R}^{N \times D}$，其中 $N$ 为帧数，$D$ 为每帧的关节旋转表示维度。扩散前向过程逐步添加高斯噪声：

$$q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} \mathbf{x}_{t-1}, \alpha_t \mathbf{I}) \tag{1}$$

其中 $\alpha_t$ 为噪声调度参数。去噪网络直接预测干净样本 $\hat{\mathbf{x}}_0$，训练损失为均方误差：

$$\mathcal{L} = \left\| \mathbf{x}_0 - \hat{\mathbf{x}}_0 \right\|^2 \tag{2}$$

### 3.2 稀疏关键帧掩码自注意力（Keyframe Masking）

核心改动在于将Transformer自注意力层的计算限制在稀疏关键帧子集上。引入二值掩码 $\mathbf{M} \in \{0,1\}^N$，其中 $\mathbf{M}_i = 1$ 表示第 $i$ 帧为关键帧，$\mathbf{M}_i = 0$ 为非关键帧。自注意力计算时，仅关键帧特征参与Query、Key、Value的交互，非关键帧被完全排除。此操作将注意力复杂度从 $O(N^2)$ 降至约 $O(K^2)$，其中 $K \ll N$ 为关键帧数量（Sec 4.1）。

### 3.3 特征空间线性插值（Feature Interpolation）

非关键帧不参与自注意力，其特征通过关键帧特征空间的线性插值重建。具体而言，对于位于两个相邻关键帧之间的非关键帧序列，在关键帧的去噪特征之间进行线性插值，生成全部 $N$ 帧的特征表示。该插值操作嵌入在Transformer层的输出端，确保后续层接收到完整的密集帧特征（Sec 4.1）。

### 3.4 Lipschitz MLP 与正则化

为保证插值结果的平滑性，将输入/输出模块的标准线性映射替换为Lipschitz MLP。该MLP采用正弦激活函数，并满足Lipschitz连续性约束：

$$\| g_{\theta}(y_1) - g_{\theta}(y_2) \|_p \leq \alpha \| y_1 - y_2 \|_p \tag{3}$$

其中 $g_{\theta}$ 为MLP映射，$\alpha$ 为Lipschitz常数上界。训练时在扩散损失中附加Lipschitz正则化项：

$$\mathcal{L} = \left\| \mathbf{x}_0 - \hat{\mathbf{x}}_0 \right\|^2 + \lambda \mathcal{L}_{\mathrm{lip}} \tag{4}$$

$$\mathcal{L}_{\mathrm{lip}} = \prod_i \mathrm{softplus}(\|\mathbf{W}_i\|_p) \tag{7}$$

其中 $\mathbf{W}_i$ 为第 $i$ 层权重矩阵，$\|\cdot\|_p$ 为矩阵范数，$\lambda$ 控制平滑强度。该约束强制MLP输出随输入变化有界，从而保证插值轨迹的光滑性（Sec 4.1, Supplementary Eq. 7）。

### 3.5 关键帧选择策略

**训练阶段**：使用Visvalingam-Whyatt几何简化算法从干净运动序列 $\mathbf{x}_0$ 中自动选取关键帧。该算法通过计算每个顶点与其相邻点构成三角形的有效面积来度量几何重要性：

$$A_i = \frac{1}{2} \left| \det \begin{pmatrix} x_{i-1} & y_{i-1} & 1 \\ x_{i} & y_{i} & 1 \\ x_{i+1} & y_{i+1} & 1 \end{pmatrix} \right| \tag{8}$$

迭代移除面积最小的顶点，直至剩余帧数达到预设缩减率（HumanML3D上使用80%缩减率）。由此生成的二值掩码 $\mathbf{M}$ 作为训练时的关键帧标注（Sec 4.2, Supplementary Eq. 8）。

**推理阶段**：初始采用均匀间隔的掩码。当扩散时间步 $t$ 降至阈值 $T' = \gamma \cdot T$ 以下时（$\gamma$ 为超参数），从当前中间去噪结果 $\mathbf{x}_t$ 出发，重新运行Visvalingam-Whyatt算法动态更新关键帧集合，使掩码聚焦于信息量更大的帧。此动态掩码更新在大扩散步数（如1000步）下尤为有效（Sec 4.2, Table 2）。

## 实验与关键发现

### 主实验结果

sMDM 在 HumanML3D 基准上全面超越基线 MDM，并在多项指标上达到与检索增强方法 ReMoDiffuse 可比甚至更优的水平。**Table 1** 顶部区域报告了使用相同 CLIP ViT‑B/32 文本编码器的对比结果：sMDM 的 FID 降至 0.130，相比 MDM 的 0.544 大幅下降 0.414；R‑Precision Top‑1 从 0.320 提升至 0.494；MM‑Dist 从 5.566 降至 3.051。值得注意的是，sMDM 的 FID 已逼近 ReMoDiffuse 的 0.103，而后者依赖外部检索库增强生成，sMDM 则完全基于稀疏关键帧训练，无需额外检索开销。

![[assets/figures/papers/paper_list_l1891_Less_Is_More_Improving_Motion_Diffusion_Models_with_Sparse_Keyframes/figures/003_Table_1.jpg]]
*Table 1: Text-to-motion generation results using motion generative models evaluated on HumanML3D dataset [7]. The top section presents various motion diffusion models utilizing the same CLIP text encoder [26], while the bottom section compares other generative models incorporating larger text encoders. † denotes models that employ an advanced text encoder instead of the standard CLIP [26] text encoder, while §, ‡ indicate models that require a retrieval from the database and an additional distillation stage, respectively. Bold values indicate the best results, while underlined values denote the second-best in each section*

![[assets/figures/papers/paper_list_l1891_Less_Is_More_Improving_Motion_Diffusion_Models_with_Sparse_Keyframes/figures/010_Table_5.jpg]]
*Table 5: Text-to-motion results of MDM [35] and sMDM, implemented with Transformer encoder, on HumanML3D dataset [7]. Both models are trained with 50 diffusion steps. We use the same evaluation metrics in Table 1*

当使用更强的文本编码器时，sMDM 的优势进一步扩大。**Table 1** 底部区域显示，sMDM‑stella 采用 Stella‑1.5B 文本编码器后，R‑Precision Top‑1 达到 0.554，超越所有使用先进文本编码器的基线方法（包括 ReMoDiffuse 的 0.510），成为该设置下的最佳结果。

定性结果（**Figure 3**）进一步印证了定量结论。与 MDM 和 MotionGPT 相比，sMDM 能更准确地捕捉文本提示中的细微风格和连续动作序列——例如，当文本描述包含多个连续动作时，MDM 常遗漏部分指令，而 sMDM 忠实执行了全部文本语义。

### 消融实验

消融实验系统验证了 sMDM 各设计组件的必要性，所有结果汇总于 **Table 1** 的消融行。

**关键帧选择策略**：将 Visvalingam‑Whyatt 几何选择替换为随机关键帧选择后，FID 从 0.130 急剧上升至 0.249。这表明几何上有意义的帧选择是稀疏训练的核心——随机掩码破坏了运动序列的语义连贯性，导致生成质量显著退化。

**插值模块**：移除插值模块（仅计算关键帧损失）使 FID 升至 0.267，同时运动多样性指标下降。这说明仅对关键帧施加监督不足以重建完整运动，插值模块在保持非关键帧的时序一致性方面不可替代。

**Lipschitz 正则化**：去掉 Lipschitz MLP 层后 FID 升至 0.329，为所有消融中退化最严重的变体。Lipschitz 约束通过限制输入/输出映射的变化幅度，保证了插值特征的平滑性；缺少该约束时，非关键帧重建出现剧烈抖动，严重损害运动质量。

**动态掩码更新**：**Table 2** 展示了推理阶段动态掩码更新的消融结果。该策略对使用大扩散步数训练的模型尤为有效——在 1000 步设置下，动态更新将 FID 从 0.291 降至 0.246；而在 50 步设置下提升有限（FID 从 0.130 到 0.128），且不引入额外推理开销。这一现象可解释为：大扩散步数下，后期去噪步骤仍有较大不确定性，动态调整关键帧掩码能更有效地引导模型聚焦信息丰富的帧。

### 跨架构泛化与失败模式

sMDM 的设计假设了 Transformer 的自注意力结构，其在其他架构上的泛化存在明确边界。

**Transformer 编码器变体**：**Table 5** 和 **Table 6** 分别报告了将 MDM 和 MotionDiffuse 替换为 Transformer 编码器实现后的对比结果。sMDM 和 sMotionDiffuse 在各自变体上均保持了对密集基线的优势，表明稀疏关键帧方法对 Transformer 族架构具有较好的适应性。

**U‑Net 架构退化**：**Table 7** 的结果揭示了方法的关键局限性。将稀疏关键帧策略应用于基于 U‑Net 的 CondMDI 模型进行运动插值时，sCondMDI 的 FID 从 0.153 升至 0.551，性能严重退化。U‑Net 的卷积层级结构缺乏自注意力机制提供的全局帧间交互能力，关键帧掩码和线性插值的组合无法有效补偿缺失的密集特征传播。

**长序列生成的过渡段问题**：**Table 3** 展示了 Double Take 长序列生成策略下的对比结果。sPriorMDM 在独立运动片段上质量更高（Motion FID 0.624 vs PriorMDM 0.971），但在过渡片段上 FID 反而不及基线（3.644 vs 2.468）。作者将此归因于 sPriorMDM 生成的运动更活跃，导致过渡段偏离训练分布。这提示稀疏关键帧方法在需要精确时序对齐的边界区域可能引入额外的分布偏移。

### 实时角色控制与参数敏感性

**Table 4** 报告了 Diffusion Planner 实时角色控制任务上的结果。在不同关键帧缩减率下，sDiP 和 sDiP‑T 均保持了对密集基线的竞争力，验证了稀疏训练在交互式应用场景中的可行性。但缩减率作为关键超参数需针对数据集调整——HumanML3D 上 80% 的缩减率效果最优，泛化到其他数据分布时可能需要重新搜索。

![[assets/figures/papers/paper_list_l1891_Less_Is_More_Improving_Motion_Diffusion_Models_with_Sparse_Keyframes/figures/001_Figure_1.jpg]]
*Figure 1: We propose a keyframe-centric framework for training motion diffusion models. Our method, namely Sparse Motion Diffusion Model (sMDM), outperforms baseline Motion Diffusion Model (MDM) [35], achieving more stable and precise motion generation while better capturing text prompts*

![[assets/figures/papers/paper_list_l1891_Less_Is_More_Improving_Motion_Diffusion_Models_with_Sparse_Keyframes/figures/004_Table_2.jpg]]
*Table 2: Ablation studies on dynamic mask update (Sec. 4.2). This strategy is particularly effective in terms of motion quality (FID) for the models trained with relatively large diffusion steps*

![[assets/figures/papers/paper_list_l1891_Less_Is_More_Improving_Motion_Diffusion_Models_with_Sparse_Keyframes/figures/007_Table_3.jpg]]
*Table 3: Evaluation on Double Take [31] results generated from the model pretrained on HumanML3D dataset [7]. We denote results from the experiment using a pretrained standard MDM as PriorMDM, while those using a pretrained sMDM as sPriorMDM. Both pretrained models are trained with a 50-step diffusion setting*

## 定位与知识库关联

### 1. 与基线方法的关系

sMDM 的核心贡献在于对现有运动扩散模型的自注意力机制进行“稀疏化”改造，而非提出全新的生成范式。其直接改造的基线是 **MDM**（Tevet et al., 2022），一个基于 Transformer 的密集帧运动扩散模型。MDM 对所有帧执行全对全自注意力，计算复杂度随帧数平方增长，且缺乏对关键运动帧的显式建模。sMDM 保留 MDM 的骨干架构（Transformer + 直接预测干净样本 $\hat{\mathbf{x}}_0$），仅在三处进行结构性修改：

- **帧掩码**：引入二值掩码 $M$，将自注意力限制在关键帧子集，复杂度从 $O(N^2)$ 降至约 $O(K^2)$。
- **特征插值**：在关键帧特征空间线性插值重建非关键帧，替代直接输出所有帧。
- **Lipschitz MLP**：用正弦激活的 Lipschitz MLP 替换输入/输出线性层，约束输出平滑性。

这种“最小侵入式”设计使得 sMDM 在保持与 MDM 相同文本编码器（CLIP ViT-B/32, 63M）的前提下，将 HumanML3D 上的 FID 从 0.544 大幅降至 0.130（Table 1），甚至与检索增强的 **ReMoDiffuse**（Zhang et al., 2023）的 0.103 可比。值得注意的是，ReMoDiffuse 依赖外部检索库和更复杂的网络设计，而 sMDM 仅通过稀疏关键帧机制即逼近其性能，验证了“聚焦关键帧”这一策略的有效性。

与另一基于 Transformer 的运动扩散模型 **MotionDiffuse**（Zhang et al., 2022）的关系同样直接：论文在补充实验（Table 6）中将稀疏化改造应用于 MotionDiffuse，得到 sMotionDiffuse，进一步证明该方法对 Transformer 类运动扩散模型具有通用性。

### 2. 适用边界与架构依赖性

sMDM 的设计隐含了对 Transformer 自注意力结构的强依赖。这一边界在跨架构迁移实验中暴露：

- **U-Net 架构上效果不佳**：将稀疏关键帧策略应用于基于 U-Net 的 CondMDI 运动插值模型时，sCondMDI 的 FID 从 0.153 升至 0.551（Table 7），出现显著退化。这表明掩码自注意力 + 插值的组合假设了 Transformer 的全局注意力归纳偏置，而 U-Net 的卷积局部感受野与稀疏帧输入不兼容。
- **动态掩码更新的步数敏感性**：推理后期的动态掩码更新在扩散步数较大（如 1000 步）时效果显著（FID 从 0.291 降至 0.246），但在步数较少（≤10）时提升有限（Table 2）。这意味着动态掩码策略的收益与扩散过程的精细度正相关，步数过少时中间帧质量不足以支撑有意义的几何关键帧重选。
- **关键帧缩减率的任务依赖性**：论文在 HumanML3D 上使用 80% 的缩减率，该超参数需针对数据集调整，泛化到其他运动数据时可能需要重新搜索。

### 3. 局限与已知失效模式

除上述架构依赖外，论文揭示了以下局限：

- **长序列生成的过渡段退化**：在 Double Take 长序列生成任务中，sPriorMDM 的过渡片段 FID 较基线 PriorMDM 更高（3.644 vs 2.468），尽管主体运动片段质量显著更好（FID 0.624 vs 0.971）（Table 3）。作者将此归因于 sPriorMDM 生成的运动更活跃，导致过渡段偏离训练分布。这暴露了稀疏关键帧方法在运动连续性约束上的潜在不足——当生成的运动幅度较大时，相邻片段间的过渡可能不够平滑。
- **关键帧选择依据单一**：当前仅依赖 Visvalingam-Whyatt 几何简化算法，基于关节位置的三角形有效面积 $A_i = \frac{1}{2} \left| \det \begin{pmatrix} x_{i-1} & y_{i-1} & 1 \\ x_{i} & y_{i} & 1 \\ x_{i+1} & y_{i+1} & 1 \end{pmatrix} \right|$ 选择关键帧，未考虑速度、加速度等运动学特征。消融实验显示，用随机关键帧替代几何选择会导致 FID 从 0.130 升至 0.249，说明选择策略至关重要，但也暗示存在更优选择依据的探索空间。

### 4. 开放问题与未来方向

基于上述分析，论文开启的研究方向包括：

1. **跨架构泛化**：如何设计适合 U-Net 等非 Transformer 骨干的稀疏帧机制？可能的路径包括将掩码自注意力替换为稀疏卷积或图注意力，使关键帧信息能有效传播到非关键帧的局部邻域。
2. **关键帧选择的丰富化**：能否融合速度、加速度、关节角速度等运动学特征作为关键帧选择的补充依据？多模态选择信号可能更准确地捕捉运动突变点和风格转折点。
3. **任务拓展**：稀疏关键帧思想能否迁移到运动编辑、运动补全、运动风格迁移等下游任务？这些任务中关键帧的语义可能从“几何显著帧”转变为“编辑锚点帧”或“风格关键帧”。
4. **规模化收益**：在更大规模运动数据集（如十亿帧级别）上，稀疏训练是否能带来超越线性加速的效率提升？自注意力复杂度从 $O(N^2)$ 降至 $O(K^2)$ 的理论收益在极长序列场景下可能更加显著。
5. **过渡段质量优化**：针对长序列生成中过渡段退化的问题，是否可以通过调整混合边界（blending margin）或引入过渡段专项损失来缓解？

## 原文 PDF

![[paperPDFs/ICCV_2025/Less_Is_More_Improving_Motion_Diffusion_Models_with_Sparse_Keyframes.pdf]]
