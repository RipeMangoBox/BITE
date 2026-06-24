---
title: "Write Where It Matters: Policy-Guided Watermarks for 3D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Write_Where_It_Matters_Policy_Guided_Watermarks_for_3D_Gaussian_Splatting.pdf
project_link: null
code_link: null
aliases:
- WWIMW
- WWIMPGW3GS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 基于强化学习的策略网络输出逐锚点的“写入指导”权重，通过缩放锚点特征梯度，直接控制嵌入的空间分布与更新幅度。
primary_logic: 将3DGS水印嵌入形式化为马尔可夫决策过程，利用 Actor-Critic 强化学习以联合奖励（不可见性+鲁棒性）驱动策略，学习每个锚点“在哪里写”和“写多少”，实现场景自适应的水印分配。
claims:
- 在 Blender、LLFF、Mip-NeRF 360 三个数据集的平均指标上，W2M 在 32-bit、48-bit、64-bit 消息下的比特准确率与渲染质量（PSNR/SSIM/LPIPS）全面超越对比方法。
- 在各种图像空间失真（噪声、旋转、缩放、模糊、裁剪、JPEG 及组合）下，W2M 保持最高的解码准确率。
- 在模型空间攻击（噪声扰动、高斯移除、克隆）下，W2M 仍可靠提取水印。
- 与逐高斯控制的 GS-RL 变体相比，锚点级 W2M 在取得相近比特准确率的同时，训练时间减少约 4.7 倍，显存占用降低约 40%。
---

# Write Where It Matters: Policy-Guided Watermarks for 3D Gaussian Splatting

> [!tip] 核心洞察
> 将3DGS水印嵌入形式化为马尔可夫决策过程，利用 Actor-Critic 强化学习以联合奖励（不可见性+鲁棒性）驱动策略，学习每个锚点“在哪里写”和“写多少”，实现场景自适应的水印分配。

| 字段 | 内容 |
|------|------|
| 中文题名 | 写到关键处：基于策略引导的3D高斯泼溅水印 |
| 英文题名 | Write Where It Matters: Policy-Guided Watermarks for 3D Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Write_Where_It_Matters_Policy-Guided_Watermarks_for_3D_Gaussian_Splatting_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Write Where It Matters (W2M) |
| Dataset | Blender + LLFF + Mip-NeRF 360 平均 |

> [!tip] 效果简介
> - Blender + LLFF + Mip-NeRF 360 平均 上，Bit Acc↑ / PSNR↑ / SSIM↑ @32-bit 98.34 / 36.16 / 0.979 vs 所有对比方法均低于 W2M (最优)；Bit Acc↑ / PSNR↑ / SSIM↑ @48-bit 97.80 / 35.93 / 0.973 vs 所有对比方法均低于 W2M (最优)；Bit Acc (%) 在图像空间失真下 @32-bit (None / Noise / Rotation / Scaling / Blur / Crop /... 98.34 / 97.20 / 91.86 / 97.34 / 97.81 / 95.80 / 92.77 / 94.49 vs 所有对比方法均低于 W2M (最优)。

## 概述

### 问题背景

3D Gaussian Splatting（3DGS）已成为高质量新视角合成的主流显式表征，其资产保护需求催生了3DGS水印技术。现有方法——如**GaussianMarker**（Huang et al., NeurIPS 2024）、**GuardSplat**（Chen et al., CVPR 2025）和**3D-GSW**（Jang et al., CVPR 2025）——在嵌入水印时依赖手工设定的阈值或全局固定超参数来决定“在哪里写”和“写多少”。这种静态策略缺乏场景自适应能力，导致**不可见性与鲁棒性难以兼顾**：嵌入强度过高则渲染质量下降，过低则无法抵抗图像空间和模型空间的各类失真攻击。

### 核心方法：Write Where It Matters (W2M)

本文提出**W2M**，将3DGS水印嵌入形式化为**马尔可夫决策过程**，利用强化学习驱动策略网络学习场景自适应的水印分配。其核心思路可概括为三个关键设计：

1. **策略引导的逐锚点写入**：策略网络以结构化3DGS骨架（Scaffold-GS）的锚点特征为状态，输出逐锚点的写入权重 $w_i \in [0,1]$，直接缩放锚点特征的更新梯度 $\mathbf{f}_i^{(k+1)} = \mathbf{f}_i^{(k)} - w_i^{(k)} \mathbf{g}_i^{(k)}$，实现“写在哪里、写多少”的自适应决策。

2. **联合奖励驱动**：采用Actor-Critic在线策略强化学习，奖励信号同时融合解码鲁棒性（BCE损失）、渲染不可见性（L1/SSIM损失）和高斯尺度正则项，迫使策略在不可见性与鲁棒性之间寻找最优平衡。

3. **锚点级粒度控制**：相比直接操作百万级高斯原语，W2M在稀疏锚点上施加梯度缩放，通过Jacobian传播间接影响局部高斯簇的参数，大幅降低动作空间维度和计算开销。

### 主要结果

在Blender、LLFF和Mip-NeRF 360三个数据集上的系统评估表明：

- **综合性能领先**：在32-bit、48-bit、64-bit消息长度下，W2M的比特准确率与渲染质量（PSNR/SSIM/LPIPS）全面超越GaussianMarker、GuardSplat和3D-GSW（Table 1）。以48-bit为例，W2M平均比特准确率达97.80%，PSNR达35.93 dB。

- **鲁棒性突出**：在图像空间失真（噪声、旋转、缩放、模糊、裁剪、JPEG及组合攻击）和模型空间攻击（噪声扰动、高斯移除、克隆）下，W2M均保持最高的解码准确率（Table 2, Table 3）。

- **效率优势显著**：与逐高斯控制的GS-RL变体相比，锚点级W2M在取得相近比特准确率的同时，训练时间减少约4.7倍（9分钟 vs 42分钟），GPU显存降低约40%（9.52 GB vs 16.04 GB）（Table 4）。

### 局限与开放问题

当前W2M的消息解码器（HiDDeN）是预训练且固定的，未纳入强化学习环路进行端到端自适应优化，可能限制极限性能。此外，方法仅在三个标准数据集上验证，在极端大场景或动态场景下的适应性有待探索。一个关键的开放问题是：**如何将消息解码器集成到RL环路中，实现端到端的自适应水印嵌入？**

## 背景与动机

### 3DGS 水印的兴起与核心矛盾

3D 高斯泼溅（3D Gaussian Splatting, 3DGS）凭借显式点基元与可微光栅化，在实时新视角合成中取得了突破性进展，并迅速被应用于数字资产分发与版权保护场景。水印嵌入成为保护 3DGS 资产知识产权的关键技术手段：将一段二进制消息不可见地编码到 3DGS 表示中，并在需要时通过渲染视图进行可靠提取。

然而，3DGS 水印面临一个根本性的两难困境：**不可见性与鲁棒性难以兼顾**。嵌入强度越高，解码越可靠，但对渲染质量的损害也越大；反之，保守的嵌入虽能保持视觉保真度，却容易在图像变换或模型篡改下丢失水印信息。这一矛盾在 3DGS 中尤为突出，因为其显式几何结构（数百万个高斯原语的位置、协方差、颜色与不透明度）对修改高度敏感——任何不当的参数扰动都可能产生明显的渲染伪影。

### 现有方法的瓶颈：静态嵌入策略

当前主流的 3DGS 水印方法试图通过不同的优化策略缓解上述矛盾，但它们在嵌入决策机制上存在一个共同的局限性：**依赖静态启发式或全局固定超参数来决定“在哪里嵌入”和“嵌入多少”**。

具体而言，**GaussianMarker**（Huang et al., NeurIPS 2024）基于不确定性感知优化选择嵌入位置，但其选择标准是手工设计的，无法针对不同场景自适应调整。**GuardSplat**（Chen et al., CVPR 2025）将更新约束在 3DGS 的外观参数上以保护几何结构，但嵌入强度的分配由全局超参数统一控制，缺乏对局部区域重要性的差异化判断。**3D-GSW**（Jang et al., CVPR 2025）通过频率引导重组高斯并结合解码器监督微调，但其重组策略同样是预定义的，不具备场景级别的自适应能力。

这些方法的共同症结在于：它们将“在哪里嵌入水印”和“嵌入多强”视为一个由人工规则预先确定的静态决策，而非一个需要根据场景内容、几何结构和失真环境动态优化的控制问题。其结果是，嵌入能量往往被浪费在对水印解码贡献甚微的区域，而在关键区域又可能嵌入不足，导致不可见性与鲁棒性的平衡始终停留在次优水平。

### 核心动机：从“静态分配”到“策略驱动”

本文的核心动机在于从根本上重新审视 3DGS 水印的嵌入决策问题。我们观察到，水印嵌入本质上是一个**序列决策过程**：每一步对 3DGS 参数的修改都会影响后续的渲染质量和解码可靠性，而最优的修改策略应当根据当前场景状态和预期的失真环境进行动态调整。

这一观察催生了本文的核心思想：**将 3DGS 水印嵌入形式化为马尔可夫决策过程（MDP），利用强化学习（RL）以联合奖励（不可见性 + 鲁棒性）驱动策略网络，学习每个锚点“在哪里写”和“写多少”，实现场景自适应的水印分配**。与现有方法的手工规则不同，RL 策略能够直接从“修改后的渲染是否仍然不可见”和“经过失真后消息是否仍能被解码”这两个反馈信号中学习，从而自动发现哪些区域对水印嵌入最有利。

### 技术路线：锚点级梯度缩放机制

为实现上述策略驱动的嵌入框架，本文提出 **Write Where It Matters (W2M)** 方法。W2M 建立在结构化 3DGS 骨架（Scaffold-GS）之上，将百万级高斯原语聚合为稀疏的可学习锚点，每个锚点控制一组局部高斯簇。策略网络以锚点特征矩阵为输入，输出逐锚点的“写入指导”权重 $w_i \in [0,1]$，该权重直接缩放锚点特征的更新梯度：

$$\mathbf{f}_i^{(k+1)} = \mathbf{f}_i^{(k)} - w_i^{(k)} \mathbf{g}_i^{(k)}$$

这一机制的关键优势在于：**策略网络通过控制梯度的缩放幅度，同时决定了“在哪里嵌入”（$w_i$ 接近 1 的区域获得强更新）和“嵌入多少”（$w_i$ 的大小调节修改强度）**，从而将嵌入能量的空间分配完全交由 RL 学习。与逐高斯控制相比，锚点级操作大幅降低了动作空间维度（从百万级降至千级），使得 RL 训练在计算上可行，同时保持了足够的空间粒度来实现精细的水印分配。

## 核心创新

### 问题瓶颈：静态嵌入策略难以兼顾不可见性与鲁棒性

现有 3DGS 水印方法——**GaussianMarker**（Huang et al., NeurIPS 2024）、**GuardSplat**（Chen et al., CVPR 2025）、**3D-GSW**（Jang et al., CVPR 2025）——在嵌入水印时，依赖手工设定的阈值或全局固定超参数来决定“在哪里写”和“写多少”。这种静态启发式策略缺乏对场景几何、纹理复杂度以及失真类型的自适应感知能力，导致一个根本性困境：嵌入强度不足则鲁棒性差，嵌入过度则渲染质量下降，二者难以在不同场景和消息长度下同时达到最优。

### 核心洞见：将水印嵌入形式化为马尔可夫决策过程

W2M 的核心突破在于将 3DGS 水印嵌入重新定义为**序列决策问题**：每一步，智能体观察当前场景状态，决定对哪些锚点施加多大强度的修改，环境返回渲染不可见性与解码鲁棒性的联合反馈。这一形式化使得嵌入策略可以通过强化学习**端到端地学习**“在哪里写”和“写多少”，而非依赖预设规则。

### 关键改变槽位

**1. 嵌入策略：从静态超参数到逐锚点自适应权重**

- **Baseline 做法**：手工设定阈值或全局固定超参数决定嵌入位置与强度。
- **W2M 做法**：策略网络（两层 MLP 的 Actor）输入当前锚点特征矩阵 $\mathbf{F}^{(k)}$，输出逐锚点的写入指导权重 $\mathbf{W}^{(k)} \in [0,1]^N$，直接控制每个锚点的修改幅度。权重 $w_i^{(k)}$ 缩放锚点特征的更新梯度：
  $$\mathbf{f}_i^{(k+1)} = \mathbf{f}_i^{(k)} - w_i^{(k)} \mathbf{g}_i^{(k)}$$
  其中 $\mathbf{g}_i^{(k)} = \nabla_{\mathbf{f}_i^{(k)}} \mathcal{L}_{\mathrm{embed}}^{(k)}$ 是即时印刻目标对锚点特征的梯度（Eq. 5, 7）。
- **机制解释**：通过 Jacobian 传播，锚点梯度的加权和近似于 3D 高斯参数的一阶改变量（Eq. 9），验证了该机制的有效性与可解释性。

**2. 优化范式：从固定损失最小化到联合奖励驱动的强化学习**

- **Baseline 做法**：直接最小化固定的嵌入损失（如 MSE + 感知损失），缺乏对嵌入后果的闭环反馈。
- **W2M 做法**：采用 **on-policy Actor-Critic（A2C）** 在线策略强化学习。每步的奖励函数融合三个信号（Eq. 8）：
  $$r^{(k)} = - \lambda_{\mathrm{rob}} \mathcal{L}_{\mathrm{rob}} - \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}} - \sigma \mathcal{R}_{\mathrm{scale}}$$
  分别对应解码鲁棒性（BCE）、渲染不可见性（L1+SSIM）和高斯尺度正则化。使用单步 TD 误差更新策略与价值网络（Eq. 10）。
- **关键设计**：奖励评估在**同一视图-失真对**上进行——更新前缓存视图 $\Pi^{(k)}$ 和失真 $T^{(k)}$，更新后渲染经相同失真再解码，确保反馈信号直接关联当前决策的后果。

**3. 表示粒度：从逐高斯操作到结构化锚点级控制**

- **Baseline 做法**：直接操作百万级高斯原语，计算和存储开销巨大。
- **W2M 做法**：采用结构化 3DGS 骨架（Scaffold-GS），通过稀疏可学习锚点聚合局部高斯簇。策略在锚点特征上施加缩放梯度，间接控制其关联的高斯簇参数。
- **效率验证**：消融实验（Table 4）显示，相比于逐高斯控制的 GS-RL 变体，锚点级 W2M 在取得相近比特准确率（96.76 vs 98.97）的同时，训练时间减少约 **4.7 倍**（42 分钟 → 9 分钟），GPU 显存降低约 **40%**（16.04 GB → 9.52 GB）。

### 创新点总结

W2M 的三项改变形成一条完整的因果链：**强化学习策略网络**输出逐锚点权重，决定“在哪里写”和“写多少”；**联合奖励函数**将不可见性与鲁棒性反馈闭环传递给策略；**锚点级梯度缩放**在结构化表示上高效执行定向修改。这一设计使得水印嵌入从静态规则驱动转向场景自适应学习，在 Blender、LLFF、Mip-NeRF 360 三个数据集上以 32-bit、48-bit、64-bit 消息全面超越对比方法（Table 1），并在图像空间和模型空间多种失真下保持最优鲁棒性（Table 2, 3）。

## 整体框架

W2M 将 3DGS 水印嵌入形式化为一个**策略驱动的序列决策过程**，并用 Actor‑Critic 强化学习在线优化。其核心直觉是：不同场景、不同锚点对水印嵌入的“容忍度”不同，因此需要学习**逐锚点**的“在哪里写”与“写多少”策略，而非依赖全局静态超参数。

### 总体流程

整体框架如 Figure 3 所示，每一步 RL 迭代包含以下模块：

![[assets/figures/papers/paper_list_l2654_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Write_Where_It_Matt/figures/003_Figure_3.jpg]]
*Figure 3: The proposed Write Where It Matters (W2M). At each RL step k: State, the 3DGS*

1. **状态构造**  
   当前 3DGS 场景 $\Theta^{(k)}$ 被概括为锚点特征矩阵 $\mathbf{F}^{(k)} \in \mathbb{R}^{N \times d}$，其中 $N$ 为锚点数量。该矩阵作为策略网络的输入，承载了场景的结构与外观信息。

2. **策略网络输出写入指导**  
   一个轻量的 Actor‑Critic 智能体（Actor 与 Critic 均为两层 MLP）观测 $\mathbf{F}^{(k)}$，输出逐锚点的写入指导权重 $\mathbf{W}^{(k)} \in [0,1]^N$。权重 $w_i^{(k)}$ 决定了第 $i$ 个锚点在当前步被修改的强度。

3. **环境转移：锚点级梯度缩放更新**  
   首先采样并缓存一个视角‑失真对 $(\Pi^{(k)}, T^{(k)})$，渲染同视角的干净参考图像 $\mathbf{I}_{\text{clean}}^{(k)}$ 用于不可见性评估。  
   然后计算即时印刻目标 $\mathcal{L}_{\text{embed}}^{(k)}$（式 6）对锚点特征的梯度 $\mathbf{g}_i^{(k)}$（式 7），并用策略权重进行缩放更新：
   $$\mathbf{f}_i^{(k+1)} = \mathbf{f}_i^{(k)} - w_i^{(k)} \mathbf{g}_i^{(k)} \quad \text{(式 5)}$$
   这一机制等价于通过 Jacobian 传播对 3D 高斯参数施加一阶定向修改（式 9），实现了“写到关键处”的物理含义。

4. **抗失真消息提取**  
   更新后的场景渲染图像经过**同一缓存的失真** $T^{(k)}$（图像空间或模型空间）后，由预训练的 HiDDeN 解码器 $D_{\chi}$ 提取消息 $\hat{\mathbf{M}}^{(k+1)}$。此设计确保了策略在训练中直接面对失真反馈。

5. **奖励计算与策略学习**  
   奖励函数联合评估解码鲁棒性、渲染不可见性与高斯尺度正则：
   $$r^{(k)} = -\lambda_{\text{rob}} \mathcal{L}_{\text{rob}}(\hat{\mathbf{M}}^{(k+1)}, \mathbf{M}) - \lambda_{\text{inv}} \mathcal{L}_{\text{inv}}(\mathbf{I}_{\text{reward}}^{(k+1)}, \mathbf{I}_{\text{clean}}^{(k)}) - \sigma \mathcal{R}_{\text{scale}}(\Theta^{(k+1)}) \quad \text{(式 8)}$$
   使用单步 TD 误差 $\delta^{(k)}$（式 10）更新 Actor 与 Critic，使策略逐步学会在不可见性与鲁棒性之间取得最优平衡。

### 模块关系与数据流

- **策略网络**是决策核心，接收锚点特征，输出写入权重。
- **印刻目标**提供即时梯度方向，是“写什么”的信号源。
- **写入权重**通过缩放梯度来控制“在哪里写”和“写多少”，是连接策略决策与场景修改的因果旋钮。
- **抗失真提取**将更新后的渲染结果反馈给奖励函数，形成闭环。
- **奖励函数**融合鲁棒性与不可见性，驱动策略网络向 Pareto 最优方向进化。

### 推理阶段

训练完成后，仅需保留嵌入后的 3DGS 场景与 HiDDeN 解码器。对任意新视角渲染图像，直接通过解码器提取水印消息，无需策略网络或 RL 环路参与。

## 核心模块与公式推导

W2M 将 3DGS 水印嵌入形式化为一个马尔可夫决策过程，其核心由四个紧密耦合的模块构成：策略网络、即时印刻目标、抗失真消息提取和锚点级梯度缩放更新。这些模块在 Actor-Critic 强化学习框架下协同工作，实现场景自适应的水印分配。

### 策略网络

策略网络是 W2M 的决策核心。在每个 RL 步 $k$，它接收当前 3DGS 场景的锚点特征矩阵 $\mathbf{F}^{(k)} \in \mathbb{R}^{N \times d}$ 作为状态，输出逐锚点的写入指导权重 $\mathbf{W}^{(k)} \in [0,1]^N$，指示“在哪里写”和“写多少”。策略网络与价值网络均采用简单的两层 MLP 结构，价值网络为策略更新提供基线估计。

### 即时印刻目标

在每步更新前，W2M 计算一个局部损失函数，为锚点特征提供即时的梯度方向：

$$
\mathcal{L}_{\mathrm{embed}}^{(k)} = \lambda_{\mathrm{rob}} \mathcal{L}_{\mathrm{rob}}(\hat{\mathbf{M}}^{(k)}, \mathbf{M}) + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}(\mathbf{I}_{\mathrm{embed}}^{(k)}, \mathbf{I}_{\mathrm{clean}}^{(k)}) + \sigma \mathcal{R}_{\mathrm{scale}}(\Theta^{(k)})
$$

其中 $\mathcal{L}_{\mathrm{rob}}$ 为解码消息 $\hat{\mathbf{M}}^{(k)}$ 与真实消息 $\mathbf{M}$ 之间的二元交叉熵损失，驱动鲁棒性；$\mathcal{L}_{\mathrm{inv}}$ 为嵌入后渲染图像 $\mathbf{I}_{\mathrm{embed}}^{(k)}$ 与干净渲染 $\mathbf{I}_{\mathrm{clean}}^{(k)}$ 之间的 L1 与 SSIM 组合损失，保障不可见性；$\mathcal{R}_{\mathrm{scale}}$ 为高斯尺度正则项，防止优化过程中出现异常膨胀的高斯原语。$\lambda_{\mathrm{rob}}$、$\lambda_{\mathrm{inv}}$、$\sigma$ 为平衡系数。

### 锚点级梯度缩放更新

印刻目标对每个锚点特征 $\mathbf{f}_i^{(k)}$ 产生梯度：

$$
\mathbf{g}_i^{(k)} = \nabla_{\mathbf{f}_i^{(k)}} \mathcal{L}_{\mathrm{embed}}^{(k)}
$$

策略网络输出的权重 $w_i^{(k)}$ 直接缩放该梯度，执行一步加权梯度下降：

$$
\mathbf{f}_i^{(k+1)} = \mathbf{f}_i^{(k)} - w_i^{(k)} \mathbf{g}_i^{(k)}
$$

这一机制是 W2M 的核心创新：策略通过控制 $w_i^{(k)}$ 的大小，决定每个锚点及其关联高斯簇的更新幅度，从而实现自适应的嵌入空间分配。论文进一步通过一阶近似验证了该机制对 3D 高斯参数的影响：

$$
\Delta \Theta^{(k)} \approx - \sum_{i=1}^{N} w_i^{(k)} \Big( J_{\boldsymbol{\theta} \mathbf{f}_i} \mathbf{g}_i^{(k)} \Big)
$$

其中 $J_{\boldsymbol{\theta} \mathbf{f}_i}$ 为 3D 高斯参数 $\boldsymbol{\theta}$ 对锚点特征 $\mathbf{f}_i$ 的 Jacobian 矩阵，表明锚点梯度的加权和可解释为对高斯参数的一阶定向修正。

### 抗失真提取与奖励函数

更新后的 3DGS 场景渲染图像后，W2M 使用缓存的视图-失真对 $(\Pi^{(k)}, T^{(k)})$ 对渲染结果施加图像空间或模型空间失真，再由预训练的 HiDDeN 解码器 $D_{\chi}$ 提取消息。奖励函数综合评估更新后的解码鲁棒性与渲染不可见性：

$$
r^{(k)} = - \lambda_{\mathrm{rob}} \mathcal{L}_{\mathrm{rob}}(\hat{\mathbf{M}}^{(k+1)}, \mathbf{M}) - \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}(\mathbf{I}_{\mathrm{reward}}^{(k+1)}, \mathbf{I}_{\mathrm{clean}}^{(k)}) - \sigma \mathcal{R}_{\mathrm{scale}}(\Theta^{(k+1)})
$$

奖励信号直接反馈给策略学习，鼓励高解码准确率、低感知偏差和稳定的高斯尺度。

### 策略优化

W2M 采用在线 Actor-Critic 算法进行策略学习。使用单步时序差分误差驱动更新：

$$
\delta^{(k)} = r^{(k)} + \gamma V_{\psi}(\mathbf{F}^{(k+1)}) - V_{\psi}(\mathbf{F}^{(k)})
$$

其中 $V_{\psi}$ 为价值网络，$\gamma = 0.99$ 为折扣因子。Actor 网络通过策略梯度最大化期望累积奖励，Critic 网络通过最小化 TD 误差学习准确的价值估计。训练完成后，推理阶段仅需渲染和解码，无需策略网络参与。

## 实验与分析

### 主要定量结果

W2M 在 Blender、LLFF 与 Mip-NeRF 360 三个数据集上的平均指标全面超越现有方法，且在 32-bit、48-bit、64-bit 三种消息长度下均保持最优（Table 1）。以 32-bit 为例，W2M 取得比特准确率 98.34%、PSNR 36.16 dB、SSIM 0.979；48-bit 下为 97.80%、35.93 dB、0.973。对比方法中，**GaussianMarker**（Huang et al., NeurIPS 2024）在 32-bit 与 64-bit 未报告结果，**GuardSplat**（Chen et al., CVPR 2025）在 64-bit 未报告；所有可比较条目下，W2M 均位列第一。

![[assets/figures/papers/paper_list_l2654_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Write_Where_It_Matt/figures/004_Table_1.jpg]]
*Table 1: Bit accuracy and quantitative comparison of rendering quality with baselines. We show the results in 32, 48, and 64 bits. The results are the average of Blender, LLFF, and Mip-NeRF 360 datasets. Note, GaussianMarker does not report results for 32 and 64 bits; GuardSplat does not report results for 64 bits. We conducted evaluations on the corresponding datasets using their official public implementations, respectively. The best performances are highlighted in bold and underline the second-best results*

Figure 2 以 PSNR–Bit Accuracy 散点图直观展示了这一优势：W2M 的标记点（星形 32-bit、三角形 48-bit、圆形 64-bit）始终位于右上角区域，意味着在同等或更高比特准确率下，渲染质量损失更小。该图同时标注了各方法的场景嵌入耗时，W2M 在效率与质量的权衡上同样占优。

![[assets/figures/papers/paper_list_l2654_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Write_Where_It_Matt/figures/002_Figure_2.jpg]]
*Figure 2: Performance of state-of-the-art methods, with results for each bit length averaged across the Blender [27], LLFF [26], and Mip-NeRF 360 [1] datasets. Marker shapes denote different message bit lengths (star: 32-bit, triangle: 48-bit, circle: 64- bit). We evaluate our W2M and competitors, GaussianMarker [7], 3D-GSW [11], and GuardSplat [3], using their official publicly available implementations on an RTX 3090 GPU, reporting mean PSNR versus bit accuracy. Same-shape markers near the topright corner offer optimal performance. The reported times represent per-scene embedding latency across all datasets, with decoder pre-training (where required) excluded*

### 鲁棒性评估

**图像空间失真**（Table 2，32-bit）：W2M 在七种失真类型（无失真、噪声、旋转、缩放、模糊、裁剪、JPEG 压缩及组合失真）下均保持最高比特准确率。其中，无失真下为 98.34%，旋转下为 91.86%，JPEG 压缩下为 92.77%，组合失真下仍达 94.49%。所有对比方法在每种失真下均低于 W2M，表明策略网络学到的写入分布对渲染层面的扰动具有强泛化能力。

**模型空间攻击**（Table 3，32-bit）：在模型参数直接受扰的场景（高斯噪声注入、高斯移除、模型克隆）下，W2M 同样表现最优。无攻击下 98.34%，噪声扰动下 91.57%，高斯移除下 98.07%，克隆下 97.89%。值得注意的是，高斯移除攻击对 W2M 的影响极小（仅下降约 0.27%），说明关键写入锚点并未集中在易被移除的冗余高斯上，策略网络成功规避了脆弱区域。

### 消融实验

**锚点级控制 vs. 逐高斯控制**（Table 4）：将 W2M 的锚点级策略扩展为逐高斯变体 GS-RL 后，比特准确率从 96.76% 提升至 98.97%，但代价巨大——训练时间从 9 分钟增至 42 分钟（约 4.7 倍），GPU 显存从 9.52 GB 增至 16.04 GB（约 40% 增幅）。PSNR 与 SSIM 基本持平（38.05 vs. 38.02，0.985 vs. 0.985）。这表明锚点级控制是效率与性能的最佳平衡点。

**奖励函数组合**（Table 5）：在 LLFF 数据集 48-bit 设定下，完整奖励（不可见性 L_inv + 鲁棒性 L_rob + 尺度正则 R_scale）取得最佳综合指标：比特准确率 98.75%，PSNR 38.10 dB，SSIM 0.985，LPIPS 0.016。单独移除任一组件均导致性能退化——仅使用 L_rob 时比特准确率上升但 PSNR 大幅下降，仅使用 L_inv 时比特准确率急剧恶化，移除 R_scale 则渲染质量与鲁棒性同时受损。这验证了联合奖励设计对“不可见性–鲁棒性”权衡的必要性。

**锚点数量影响**（Figure 4）：比特准确率与 PSNR 随锚点数量增加而快速上升，随后趋于饱和。论文采用紫色箭头标记的配置，位于饱和拐点附近，说明 W2M 在有限锚点预算下即可有效分配水印信息，无需过度增加模型复杂度。

### 失败模式与局限

尽管 W2M 在各项指标上表现突出，仍存在两处可识别的局限。其一，消息解码器（HiDDeN）在 RL 环路中保持预训练且固定，未参与端到端自适应优化。在极端失真下，解码器与策略之间的分布偏移可能限制极限鲁棒性，这解释了旋转与 JPEG 失真下准确率相对较低的现象。其二，当前验证仅覆盖 Blender、LLFF、Mip-NeRF 360 三个中等规模数据集，对于超大场景或动态场景下的策略泛化能力尚缺乏实验支持。这两点需在实际部署中手动评估。

### 补充图表

![[assets/figures/papers/paper_list_l2654_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Write_Where_It_Matt/figures/005_Table_2.jpg]]
*Table 2: Bit accuracy of robustness under various Image-space distortions compared to baselines. We conduct experiments using 32-bit messages and report the average results of Blender, LLFF, and Mip-NeRF 360 datasets. The best performances are highlighted in bold*

![[assets/figures/papers/paper_list_l2654_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Write_Where_It_Matt/figures/006_Table_3.jpg]]
*Table 3: Bit accuracy of robustness under various Model-space distortions compared to baselines. We conduct experiments using 32-bit messages and report the average results of all datasets. The best performances are highlighted in bold*

![[assets/figures/papers/paper_list_l2654_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Write_Where_It_Matt/figures/009_Table_4.jpg]]
*Table 4: Comparison results of GS-RL (a per-Gaussian variant) and W2M with B = 48 bits on the Blender dataset*

![[assets/figures/papers/paper_list_l2654_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Write_Where_It_Matt/figures/007_Table_5.jpg]]
*Table 5: Evaluation on different reward combinations with B = 48 bits on the LLFF dataset*

![[assets/figures/papers/paper_list_l2654_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Write_Where_It_Matt/figures/008_Figure_4.jpg]]
*Figure 4: Impact of the anchor number evaluated B = 48 bits on the LLFF dataset. Bit Accuracy (left y-axis) and PSNR (right y-axis) versus the number of anchors. The violet arrow marks the configuration used in our implementation*

![[assets/figures/papers/paper_list_l2654_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Write_Where_It_Matt/figures/001_Figure_1.jpg]]
*Figure 1: We introduce Write Where It Matters (W2M) for 3D Gaussian Splatting (3DGS) watermarking. We present qualitative results with a 48-bit message length, comparing W2M against state-of-the-art competitors, GaussianMarker [7], GuardSplat [3], and 3D-GSW [11] on the Blender [27], LLFF [26], and Mip-NeRF 360 [1] datasets. W2M is a novel policy-guided approach that employs Reinforcement Learning to directly link robustness to distortions and rendered-view invisibility feedback with per-Gaussian editing decisions, thereby achieving superior performance with minimal impact on the original 3DGS*

## 方法谱系与知识库定位

### 1. 问题定位：3DGS 水印中的“写在哪里”困境

3D Gaussian Splatting（3DGS）的显式点云表征使其模型资产极易被未授权复制与再分发，因此鲁棒且不可见的水印嵌入成为紧迫需求。现有 3DGS 水印方法可归为三类：

- **基于不确定性感知的优化**：**GaussianMarker**（Huang et al., NeurIPS 2024）通过估计每个高斯对渲染的贡献不确定性来引导嵌入，但其不确定性度量本质上是启发式的，缺乏对最终解码鲁棒性的直接反馈。
- **约束更新空间**：**GuardSplat**（Chen et al., CVPR 2025）将水印更新限制在外观参数（如颜色与不透明度）上，避免破坏几何结构以保持不可见性，但固定约束限制了嵌入容量与鲁棒性的上限。
- **频率引导重组**：**3D-GSW**（Jang et al., CVPR 2025）通过频率分析重组高斯并进行解码器监督微调，但其频率选择策略是全局静态的，无法适应不同场景的局部纹理特性。

这些方法的共同瓶颈在于：**嵌入位置与强度的决策机制是静态的**——要么依赖手工阈值，要么使用全局固定超参数。这导致不可见性与鲁棒性之间形成零和博弈：在纹理丰富区域写入可增强鲁棒性但易产生伪影，在平坦区域写入则相反。本质上，这是一个**空间分配问题**：对于给定的 3DGS 场景和消息，应该“在哪里写”以及“写多少”才能最优地平衡不可见性与鲁棒性？

### 2. 核心机制突破：从静态分配到策略引导的自适应写入

W2M（Write Where It Matters）的核心创新在于将上述空间分配问题形式化为**马尔可夫决策过程（MDP）**，并引入基于 Actor-Critic 的强化学习策略来学习场景自适应的写入指导。这一设计带来了三个层次的机制突破：

**（1）策略网络输出逐锚点写入权重。** 策略网络以当前 3DGS 的锚点特征矩阵 $\mathbf{F}^{(k)}$ 为状态输入，输出逐锚点的写入指导权重 $\mathbf{W}^{(k)} \in [0,1]^N$（见 Eq. (5)）。每个权重 $w_i^{(k)}$ 直接缩放对应锚点的更新梯度 $\mathbf{g}_i^{(k)}$，从而控制“写多少”。这与现有方法的全局固定超参数形成鲜明对比——后者对所有高斯施加相同强度的更新，而 W2M 允许策略网络根据每个锚点所在的局部场景上下文（纹理复杂度、几何结构、对渲染视图的贡献度）自适应地分配写入强度。

**（2）联合奖励驱动策略学习。** 奖励函数（Eq. (8)）同时编码了解码鲁棒性（BCE 损失）、渲染不可见性（L1 + SSIM 损失）和高斯尺度正则化三项信号。关键在于，奖励是在**经过图像/模型空间失真后**的渲染图像上评估解码准确率的（即“抗失真提取”机制），这意味着策略网络接收到的反馈直接反映了其写入决策在实际攻击场景下的后果。这种“闭环”学习使策略能够自动发现：在哪些锚点上写入可以在最小化视觉代价的同时最大化鲁棒性增益。

**（3）锚点级粒度实现效率与可解释性的平衡。** W2M 采用结构化 3DGS 骨架（Scaffold-GS），通过稀疏可学习锚点聚合局部高斯簇。消融实验（Table 4）表明，与逐高斯控制的变体 GS-RL 相比，锚点级 W2M 在略微降低比特准确率（96.76 vs 98.97）的情况下，训练时间减少约 4.7 倍（42 分钟 → 9 分钟），GPU 显存降低约 40%（16.04 GB → 9.52 GB）。这验证了锚点粒度作为“表示瓶颈”的有效性：它既保留了足够的空间分辨率以进行差异化写入，又大幅降低了策略网络的决策维度。

### 3. 知识库定位：与相关范式的交叉与边界

W2M 的方法论贡献可置于以下知识谱系中：

**与 3DGS 水印方法的关系。** W2M 并非替代现有水印方法，而是提供了一种**元策略层**：它将嵌入目标（如 GaussianMarker 的不确定性损失、GuardSplat 的外观约束）替换为强化学习的奖励信号，从而将任何可微的嵌入损失纳入策略驱动的自适应框架。从 Table 1-3 的全面对比来看，W2M 在 Blender、LLFF、Mip-NeRF 360 三个数据集的平均指标上，于 32-bit、48-bit、64-bit 消息下均取得最优比特准确率与渲染质量，且在图像空间失真（噪声、旋转、缩放、模糊、裁剪、JPEG 及组合）和模型空间攻击（噪声扰动、高斯移除、克隆）下保持最高的解码鲁棒性。

**与强化学习在视觉任务中的应用。** W2M 将 3DGS 水印嵌入形式化为序贯决策过程，这与 RL 在图像水印（如 HiDDeN 的编码器-解码器联合训练）和神经渲染优化中的趋势一致。但 W2M 的独特之处在于：策略网络不直接输出像素级或参数级修改，而是输出**梯度缩放权重**——这等价于对优化过程本身进行调节，而非直接生成修改内容。这种“元优化”设计使策略网络轻量（两层 MLP）且训练稳定。

**与结构化 3DGS 表征的关系。** W2M 继承了 Scaffold-GS 的锚点-高斯层级结构，但将其重新定位为水印嵌入的“控制接口”。Eq. (9) 给出了一阶近似证明：锚点特征的加权梯度更新 $\sum_{i=1}^{N} w_i^{(k)} (J_{\boldsymbol{\theta} \mathbf{f}_i} \mathbf{g}_i^{(k)})$ 等价于对 3D 高斯参数的一阶定向修改。这为锚点级控制提供了理论可解释性。

### 4. 适用边界与局限

尽管 W2M 在多个维度上取得了领先性能，其设计仍存在明确的适用边界：

**消息解码器固定。** W2M 采用预训练的 HiDDeN 解码器进行消息提取，该解码器在 RL 训练环路中保持冻结。这意味着策略网络学习的写入模式必须适配一个固定的解码器先验，而非端到端地联合优化编码-解码过程。当面对极端失真或域外场景时，固定解码器可能成为性能瓶颈。论文明确指出这一局限，并将“将消息解码器集成到 RL 环路中进行端到端自适应优化”列为开放问题。

**场景泛化未充分验证。** 当前实验覆盖 Blender（合成物体）、LLFF（前向场景）和 Mip-NeRF 360（360° 无界场景）三个数据集，但均为静态场景。对于动态场景（如 4DGS）、大规模城市场景（如 Block-NeRF）或反射/折射密集场景，策略网络学到的写入模式是否可迁移尚待验证。

**训练计算开销。** 尽管锚点级控制相比逐高斯控制大幅提升了效率，W2M 的 RL 训练仍需在每个场景上独立进行（per-scene optimization），且涉及多次渲染与失真模拟。Table 2 中报告的嵌入延迟（per-scene embedding latency）是评估这一开销的关键指标，但论文未与无 RL 的方法进行绝对时间对比。

**奖励权重的敏感性。** Table 5 的消融实验表明，完整奖励组合（$\mathcal{L}_{\text{inv}} + \mathcal{L}_{\text{rob}} + \mathcal{R}_{\text{scale}}$）在 48-bit 实验上取得最佳平衡（比特准确率 98.75%，PSNR 38.10 dB），而单一奖励或缺少正则项均导致性能下降。这意味着奖励权重 $\lambda_{\text{rob}}$、$\lambda_{\text{inv}}$ 和 $\sigma$ 的调优对新场景可能敏感，论文未提供自动调优策略。

### 5. 开放问题与后续方向

基于上述分析，W2M 框架开启了若干值得探索的方向：

1. **端到端自适应解码器**：将 HiDDeN 解码器纳入 RL 环路，使策略网络与解码器协同进化，可能进一步提升极限鲁棒性与不可见性的 Pareto 前沿。

2. **跨场景策略迁移**：当前策略网络为每个场景从头训练。元学习（meta-learning）或上下文条件策略（context-conditioned policy）可能实现跨场景的策略泛化，大幅降低部署成本。

3. **多粒度控制**：在锚点级控制的基础上引入高斯级或视图级的精细调节，形成层级化写入策略，可能在高容量消息（>64-bit）下突破当前性能饱和点（Figure 4 显示锚点数量增加后性能趋于饱和）。

4. **对抗性攻击防御**：Table 3 覆盖了噪声、移除和克隆攻击，但未考虑针对水印本身的对抗性扰动（如对抗性高斯删除）。将对抗训练纳入 RL 奖励设计可能增强对针对性攻击的鲁棒性。

5. **理论分析**：Eq. (9) 给出了一阶近似，但策略梯度在高维锚点特征空间中的收敛性质、写入权重分布与场景纹理的统计关联等理论问题尚未深入探讨。

## 原文 PDF

![[paperPDFs/CVPR_2026/Write_Where_It_Matters_Policy_Guided_Watermarks_for_3D_Gaussian_Splatting.pdf]]