---
title: Envisioning the Future, One Step at a Time
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Envisioning_the_Future_One_Step_at_a_Time.pdf
project_link: http://compvis.github.io/myriad
code_link: https://github.com/markusebke/python-billiards
aliases:
- EFOSAT
tags:
- CVPR_2026
- topic/time_series_dynamical_systems
- topic/motion_animation
- topic/vision_multimodal_applications
- topic/time_series_dynamical_systems/general
core_operator: 将未来预测表述为稀疏点轨迹上的自回归扩散模型，完全避免外观渲染，并将推理集中在运动动力学上。
primary_logic: 通过只关注稀疏的运动点而非稠密像素，该方法在保持或超越预测精度的同时，实现了数量级的采样速度提升，使大规模未来假设探索成为可能。
claims:
- 模型完全避免了可视化税，仅通过用户定义的稀疏点建模运动，实现了计算聚焦。
- 方法在开放世界运动预测中以 2200 samples/min 的吞吐量远超视频模型（如 MAGI-1 的 0.303 samples/min），同时精度相当或更优。
- 去除尺度级联导致预测质量严重下降，验证了其关键作用。
- 多步推理（50步）远优于单步预测（EPE 0.00141 vs 0.02823），证实逐步分解复杂交互的有效性。
---

# Envisioning the Future, One Step at a Time

> [!tip] 核心洞察
> 通过只关注稀疏的运动点而非稠密像素，该方法在保持或超越预测精度的同时，实现了数量级的采样速度提升，使大规模未来假设探索成为可能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 逐步展望未来 |
| 英文题名 | Envisioning the Future, One Step at a Time |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.09527) · [Project](http://compvis.github.io/myriad) · [Code](https://github.com/markusebke/python-billiards) |
| Topic | #topic/time_series_dynamical_systems #topic/motion_animation #topic/vision_multimodal_applications #topic/time_series_dynamical_systems/general |
| Method | Myriad |
| Dataset | OWM, PhysicsIQ, Physion, Billiard Planning |

> [!tip] 效果简介
> - OWM (Open-World Motion) 上，minADE_5 (Best-of-5) 0.029 vs 0.037 (MAGI-1) (-0.008)。
> - OWM 上，minADE (Best-within-5min) 0.013 vs 0.066 (MAGI-1) (-0.053)。
> - PhysicsIQ 上，minADE_5 0.115 vs 0.116 (Wan2.2) (-0.001)。

## 概要

现有视频生成模型和潜在空间模拟器在预测未来时，需要同时建模稠密的外观和运动，这种“可视化税”导致计算开销巨大，难以在开放结尾场景中进行大规模、高效率的未来假设探索。**Myriad** 提出了一种根本性的范式转换：将视觉运动预测形式化为**稀疏点轨迹上的自回归扩散模型**，完全避免像素级渲染，使推理聚焦于运动动力学本身。

核心思路是：给定单张图像和一组用户指定的稀疏查询点，模型通过逐步推理预测这些点的未来轨迹分布。技术上，这体现为三个关键设计——（1）**稀疏轨迹表示**替代稠密视频帧，消除外观建模负担；（2）**自回归逐步生成**配合 KV 缓存，将复杂的长时交互分解为可管理的短步推理；（3）**流匹配后验头 + 尺度级联**替代传统高斯混合模型，稳定建模重尾运动分布。

实验表明，该方法在吞吐量上实现了数量级跨越：在开放世界运动预测基准 OWM 上达到 **2200 samples/min**，而视频模型 MAGI-1 仅为 0.303 samples/min；同时精度相当或更优（OWM Best-5 minADE: 0.029 vs. 0.037）。在台球规划任务中，模型在固定计算预算下达到 78% 的准确率，接近模拟器神谕的 84%。消融实验证实，流匹配头 + 尺度级联、多步推理（50 步）和随机正交轨迹身份编码对性能至关重要。

该方法的主要局限在于依赖静态相机假设、训练监督受限于现成点追踪器的质量，且预测时间跨度目前限于数秒量级。尽管如此，Myriad 在运动空间中进行高效推演的能力，为开放世界中的快速决策、反事实推理和物理规划开辟了新路径。



### 视觉运动预测的现状与瓶颈

理解并预测视觉场景中的运动是通往物理世界智能的核心能力。当前主流方法将这一任务建模为从图像或视频生成稠密像素级未来帧，即图像到视频（I2V）生成。这些模型——包括 **MAGI-1**、**Wan2.2**、**CogVideo-X1.5**、**SkyReels V2** 和 **SVD 1.1** 等——在视觉质量上取得了显著进展，但其底层范式存在一个根本性的效率瓶颈：**可视化税（visual tax）**。

具体而言，现有视频和潜在空间模拟器将大量计算资源消耗在对稠密外观的建模上。在生成未来帧时，模型必须同时推理场景中所有像素的颜色、纹理和光照变化，即使绝大多数像素与理解物理运动无关。这一冗余在两种关键场景下变得尤为致命：

1. **开放结尾的未来探索**：当需要对单个场景推演数千种可能的未来（counterfactual rollouts）以进行规划时，每生成一帧完整视频的成本使得大规模假设搜索在计算上不可行。
2. **高效分支**：在需要从同一初始状态分叉出多个运动假设时，视频模型缺乏轻量级的推理机制，每次分支都需重新承担完整的解码开销。

### 现有方法的效率缺口

这一瓶颈在吞吐量上体现得极为尖锐。以 **MAGI-1** 为代表的视频生成模型在开放世界运动预测任务上的推理速度仅为 **0.303 samples/min**（Nvidia H200 GPU），这意味着在5分钟的推理预算内仅能生成约1.5个完整假设。如此低的采样率严重限制了模型在需要快速决策的下游任务（如机器人操控、自动驾驶规划）中的实用性。

传统的轨迹预测模型（如 **Trajectron++**）虽然避免了像素生成，但它们通常采用高斯混合模型（GMM）头进行单步预测，缺乏对复杂交互和长期依赖的逐步分解能力。一次性预测整个未来轨迹的方式在面对多物体碰撞、弹性形变等非线性动力学时，往往产生物理不一致的结果。

### 本文的核心动机与思路

本文的出发点是提出一个根本性的问题：**如果完全放弃外观建模，仅通过稀疏的运动点来预测未来，能否在保持或超越预测精度的同时，实现数量级的效率提升？**

这一思路源于一个关键洞察：对于大多数需要理解物理运动的智能体而言，真正重要的是“物体将去向何处”，而非“物体看起来如何”。通过将未来预测表述为**稀疏点轨迹上的自回归扩散模型**，方法可以将计算完全聚焦于运动动力学本身，从而：

- **消除可视化税**：不再生成任何像素，仅对用户定义的一组稀疏查询点预测其二维轨迹。
- **实现高效分支**：自回归逐步推理配合KV缓存机制，使得从同一状态分叉出多个未来假设的成本极低。
- **支持大规模探索**：在相同硬件和时间预算下，可生成数千个假设，使基于未来推演的规划成为可能。

这一范式转变使得模型在开放世界运动预测基准上以 **2200 samples/min** 的吞吐量超越视频模型逾7000倍，同时在精度上保持竞争力甚至更优，为视觉运动预测开辟了一条以效率为核心的新路径。



## 核心方法与创新机理

Myriad 的核心创新在于将视觉运动预测从**稠密像素生成**彻底重构为**稀疏点轨迹上的逐步自回归扩散建模**，从而绕过了视频生成模型中普遍存在的“可视化税”（visual tax）。这一范式转换带来了三个紧密耦合的关键设计变更。

### 1. 预测目标表示：从稠密帧到稀疏点轨迹

传统视频生成模型（如 **MAGI-1**、**Wan2.2**、**CogVideo-X1.5**）和潜在空间模拟器将绝大部分计算容量消耗在重建像素级外观细节上。Myriad 完全放弃了外观渲染，将预测目标定义为 $K$ 个用户指定查询点的二维轨迹 $\mathbf{x}_{1:T}$，仅通过条件分布 $p(\mathbf{x}_{1:T} \mid \mathbf{x}_0, \mathcal{T}_0)$ 建模运动动力学。这一设计使得计算资源聚焦于场景的物理交互与运动规律，而非纹理、光照等与动力学无关的视觉属性，从根本上解除了开放结尾未来探索中的计算瓶颈。

### 2. 预测范式：从单步生成到自回归逐步推理

Myriad 采用**逐步自回归生成**替代一次性预测整个轨迹。其联合分布被因果分解为：

$$p_{\theta}(\mathbf{x}_{1:T} \mid \mathbf{x}_0, \mathcal{Z}_0) = \prod_{t=1}^T \prod_{i=1}^K p_{\theta}(x_t^{(i)} \mid \mathbf{x}_t^{(<i)}, \mathbf{x}_{<t}, \mathcal{Z}_0)$$

该分解在时间和轨迹两个维度上进行：每个时间步 $t$ 内，轨迹点按顺序预测，且每个点的预测条件于之前所有时间步的完整轨迹以及当前时间步已预测的点。配合 **KV 缓存**机制，逐步预测避免了重复编码历史信息，使长时域推演成为可能。消融实验证实了该范式的必要性：50 步逐步预测（$\Delta t=0.01\text{s}$）的终点误差（EPE）为 0.00141，而单步预测高达 0.02823，差距超过一个数量级（Table D）。

### 3. 后验参数化：流匹配头 + 尺度级联

Myriad 用**流匹配（Flow Matching）头**替代了先前轨迹预测模型中常用的**高斯混合模型（GMM）头**。流匹配头 $v_{\phi}$ 预测 ODE 速度场以采样增量运动 $\Delta x_{t}^{(i)}$，训练目标为：

$$\mathcal{L}_{\mathrm{FM}} = \underset{\tau, \Delta x_{t,0}^{(i)}, \Delta x_{t,1}^{(i)}}{\mathbb{E}} || v_{\phi}(\Delta x_{t,\tau}^{(i)} | \mathbf{z}_t^{(i)}) + \Delta x_{t,0}^{(i)} - \Delta x_{t,1}^{(i)} ||_2^2$$

在此基础上，**尺度级联**（Scale Cascade）通过构建对数间隔的尺度系数 $s$ 并以 $\tanh(s \cdot \Delta x)$ 饱和输入，稳定了对重尾运动分布的建模。消融实验（Table 3）表明：流匹配头相比 GMM 头将 Best-5 误差从 0.110 降至 0.033，而尺度级联进一步压缩至 0.029，验证了该组合设计的决定性作用。

### 4. 架构效率优化

为支撑大规模快速采样，Myriad 在变换器架构上引入了两项效率优化：

- **融合并行变换器块**：将自注意力、交叉注意力和前馈网络合并为单一残差块 $\mathbf{h} \gets \mathbf{h} + \mathrm{SA}(\mathbf{h}) + \mathrm{CA}(\mathbf{h}, \mathbf{h}_{\mathrm{cross}}) + \mathrm{FFN}(\mathbf{h})$，共享投影参数，显著降低逐块操作开销。
- **随机正交轨迹身份编码**：从单位球面均匀采样 $d$ 维向量 $\mathrm{id}_{\mathrm{traj}}^{(i)} \sim U(S^{d-1})$ 作为轨迹标识符，替代可学习嵌入。该设计不仅避免了有限码本的容量限制，还天然支持零样本外推到训练时未见过的轨迹数量（Table C）。

这些创新共同作用，使 Myriad 在开放世界运动预测（OWM）基准上以 **2200 samples/min** 的吞吐量远超视频模型（如 MAGI-1 的 0.303 samples/min），同时在 Best-5 精度上达到 0.029，优于 MAGI-1 的 0.037（Table 1），实现了效率与精度的双重突破。



Myriad 将视觉运动预测重新表述为**稀疏点轨迹上的逐步自回归扩散模型**，完全避免了稠密像素渲染的“可视化税”。其核心流程为：从单张图像和用户指定的一组查询点出发，模型以自回归方式逐步预测每个查询点在下一时刻的增量运动 $\Delta x_t^{(i)}$，在线更新轨迹 $x_t^{(i)}$，从而生成覆盖未来若干秒的完整运动假设。

### 输入与输出

- **输入**：单张 RGB 参考图像 $\mathcal{T}_0$，以及 $K$ 个查询点的初始坐标 $\mathbf{x}_0$。可选地，模型可接受一个短暂的“热身提示” $h_0$（前两帧的运动 $\mathbf{x}_{0:2}$），用于约束初始运动方向。
- **输出**：$K$ 条查询点在未来 $T$ 个时间步上的完整二维轨迹 $\mathbf{x}_{1:T}$。通过多次采样，模型可生成多样化的未来假设集合。

### 模块化流水线

整个框架由七个核心模块串联构成，形成“感知-编码-推理-解码”的紧凑流水线：

1. **图像编码器**（DINOv3-L/16）：将输入图像 $\mathcal{T}_0$ 编码为空间特征图 $E_{\text{img}}$，作为后续所有运动令牌共享的视觉上下文。

2. **运动令牌构建**：在每个时间步 $t$ 和每个查询点 $i$ 上，聚合四类信息构成运动令牌：
   - **外观特征**：从 $E_{\text{img}}$ 中在当前位置 $x_t^{(i)}$ 和原始位置 $x_{t=0}^{(i)}$ 处检索的局部图像特征，提供“是什么”和“局部上下文”信息。
   - **当前运动**：对增量位移 $\Delta x_t^{(i)}$ 的傅里叶嵌入（初始时为零向量）。
   - **轨迹身份**：从单位球面随机采样的正交嵌入 $\text{id}_{\text{traj}}^{(i)} \sim \mathcal{U}(S^{d-1})$，为每条轨迹提供唯一标识，支持零样本外推到不同数量的查询点。

3. **共享时空位置编码**：采用轴向旋转位置编码（axial RoPE），对每个令牌编码其当前空间位置、原始空间位置和时间步，使运动令牌能够同时关注彼此和图像令牌。

4. **快速推理块**（Fused Parallel Transformer）：将自注意力、交叉注意力和前馈网络合并为单个残差块：
   $$\mathbf{h} \gets \mathbf{h} + \mathrm{SA}(\mathbf{h}) + \mathrm{CA}(\mathbf{h}, \mathbf{h}_{\text{cross}}) + \mathrm{FFN}(\mathbf{h})$$
   自注意力和交叉注意力以前缀布局实现——拼接 $[\mathbf{h}_{\text{image}} \mid \mathbf{h}_{\text{motion}}]$，图像令牌不参与注意力计算（模拟纯交叉注意力），运动令牌因果地关注图像和已预测的运动令牌。该设计显著减少了逐块操作开销。

5. **自回归变换器主干**：将联合轨迹分布按时间和轨迹维度因果分解：
   $$p_{\theta}(\mathbf{x}_{1:T} \mid \mathbf{x}_0, \mathcal{Z}_0) = \prod_{t=1}^T \prod_{i=1}^K p_{\theta}(x_t^{(i)} \mid \mathbf{x}_t^{(<i)}, \mathbf{x}_{<t}, \mathcal{Z}_0)$$
   每一步条件于之前所有时间步的轨迹和当前时间步已预测的轨迹。推理时维护 KV 缓存，避免重复计算历史上下文。

6. **流匹配头**（Flow Matching Head）：将条件分布 $p_{\theta}(x_t^{(i)} \mid \cdots)$ 参数化为一个流匹配模型。给定运动令牌的隐状态 $\mathbf{z}_t^{(i)}$，预测 ODE 速度场：
   $$v_{\phi} : (\Delta x_{t,\tau}^{(i)}, \tau, \mathbf{z}_t^{(i)}) \mapsto \frac{\partial}{\partial\tau} \Delta x_{t,\tau}^{(i)}$$
   其中 $\tau \in [0,1]$ 为流匹配的伪时间。训练时最小化流匹配损失 $\mathcal{L}_{\text{FM}}$，推理时通过 ODE 积分从噪声采样增量运动。

7. **尺度级联**（Scale Cascade）：在流匹配头输入端，对增量运动 $\Delta x$ 应用对数间隔的尺度系数 $s$，经 $\tanh(s \cdot \Delta x)$ 饱和处理后送入网络。该设计稳定了对重尾运动分布的建模，消融实验显示去除级联会导致预测质量显著下降（Best-5 误差从 0.029 升至 0.033）。

### 推理效率设计

整个流水线围绕“稀疏运动空间中的快速采样”进行优化：
- 并行变换器块和前缀注意力布局减少了每步计算量。
- KV 缓存使自回归解码的开销接近恒定。
- 流匹配头中的自适应归一化条件机制允许缓存中间表示。

这些设计共同实现了 **2200 samples/min** 的吞吐量（OWM 基准，Nvidia H200），相比视频生成模型 MAGI-1（0.303 samples/min）提升超过 7000 倍，使得在固定时间预算下大规模探索未来假设成为可能。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/001_Figure_1.jpg]]
*Figure 1: From a single image, our model envisions diverse, physically consistent futures in open-set environments (top). By exploring directly in motion space, it can rapidly perform thousands of counterfactual rollouts – here to select a candidate billiard shot (bottom)*



Myriad 的核心架构围绕“稀疏点轨迹的自回归扩散建模”展开，由以下关键模块串联构成。

### 问题形式化：稀疏轨迹上的联合分布

给定单张参考图像 $\mathcal{T}_0$ 和 $K$ 个查询点的初始位置 $\mathbf{x}_0$，模型的目标是建模这些点在 $T$ 个未来时间步上的完整轨迹 $\mathbf{x}_{1:T}$ 的联合分布：

$$p(\mathbf{x}_{1:T} \mid \mathbf{x}_0, \mathcal{T}_0)$$

该分布通过自回归方式在时间和轨迹两个维度上进行因果分解：

$$p_{\theta}(\mathbf{x}_{1:T} \mid \mathbf{x}_0, \mathcal{Z}_0) = \prod_{t=1}^T \prod_{i=1}^K p_{\theta}(x_t^{(i)} \mid \mathbf{x}_t^{(<i)}, \mathbf{x}_{<t}, \mathcal{Z}_0)$$

其中 $\mathcal{Z}_0$ 为从图像和初始点编码得到的潜在条件表示。每一步预测 $x_t^{(i)}$ 时，模型条件于所有先前时间步的轨迹 $\mathbf{x}_{<t}$ 以及当前时间步已预测的轨迹 $\mathbf{x}_t^{(<i)}$。

### 运动令牌构建

每个预测位置 $(t, i)$ 对应一个运动令牌，聚合三类信息（见 Figure 2）：

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/003_Figure_2.jpg]]
*Figure 2: Motion Token Construction. The fourier-embedded motion*

1. **外观与局部上下文**：从图像编码器（DINOv3-L/16）提取的空间特征 $E_{\text{img}}$ 中，在当前位置 $x_t^{(i)}$ 和原始位置 $x_{t=0}^{(i)}$ 处通过双线性插值检索特征，提供“该点是什么”和“周围环境”的信息。
2. **当前运动**：将增量运动 $\Delta x_t^{(i)}$ 经傅里叶嵌入后输入。
3. **轨迹身份标识**：为每条轨迹分配一个随机采样的正交标识 $\text{id}_{\text{traj}}^{(i)} \sim U(S^{d-1})$，即从单位球面上均匀采样，确保不同轨迹的标识近似正交。消融实验（Table C）表明，这种随机正交嵌入优于可学习嵌入和无嵌入方案，并天然支持零样本外推到不同数量的轨迹。

### 共享时空位置编码

模型采用基于轴向旋转位置编码（axial RoPE）的方案（见 Figure 3）。每个运动令牌被编码以当前位置、原始位置和时间戳，使其能够在注意力操作中感知时空关系。图像令牌仅编码空间位置。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/004_Figure_3.jpg]]
*Figure 3: Positional Encoding Scheme. We encode the current and original spatial position of each token, alongside its time. Motion tokens attend to each other and to image tokens*

### 快速推理块

为提升推理效率，Myriad 采用融合的并行变换器块，将自注意力、交叉注意力和前馈网络合并为单个残差操作：

$$\mathbf{h} \gets \mathbf{h} + \mathrm{SA}(\mathbf{h}) + \mathrm{CA}(\mathbf{h}, \mathbf{h}_{\text{cross}}) + \mathrm{FFN}(\mathbf{h})$$

其中 $\mathbf{h}_{\text{cross}}$ 为交叉注意力的键值对来源。自注意力和交叉注意力以前缀布局拼接为 $[\mathbf{h}_{\text{image}} \mid \mathbf{h}_{\text{motion}}]$，图像令牌不参与注意力计算（仅作为交叉注意力的键值），运动令牌因果地关注自身和图像令牌（见 Figure 4）。这种融合设计相比传统逐层串联的变换器块显著降低了计算开销。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/002_Figure_4.jpg]]
*Figure 4: Fast Reasoning Blocks. (a) Previous methods [cf. 10] use normal transformer layers, incurring significant overhead due to the multitude of operations performed per block. (b) Our fused layers reduce complexity significantly, improving efficiency*

### 流匹配头与尺度级联

后验分布 $p_{\theta}(\Delta x_t^{(i)} \mid \mathbf{z}_t^{(i)})$ 由流匹配头 $v_{\phi}$ 参数化，该头预测噪声运动在伪时间 $\tau \in [0,1]$ 下的 ODE 速度场：

$$v_{\phi} : (\Delta x_{t,\tau}^{(i)}, \tau, \mathbf{z}_t^{(i)}) \mapsto \frac{\partial}{\partial\tau} \Delta x_{t,\tau}^{(i)}$$

其中 $\mathbf{z}_t^{(i)}$ 为变换器主干输出的条件特征。流匹配头由多个 FFN 块组成，通过自适应归一化层以 $\mathbf{z}_t^{(i)}$ 和 $\tau$ 为条件（见 Figure 6 左）。训练目标为流匹配损失：

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/007_Figure_6.jpg]]
*Figure 6: Posterior FM Head. Left: Our FM Head consists of multiple FFN blocks conditioned on*

$$\mathcal{L}_{\mathrm{FM}} = \underset{\tau, \Delta x_{t,0}^{(i)}, \Delta x_{t,1}^{(i)}}{\mathbb{E}} \| v_{\phi}(\Delta x_{t,\tau}^{(i)} \mid \mathbf{z}_t^{(i)}) + \Delta x_{t,0}^{(i)} - \Delta x_{t,1}^{(i)} \|_2^2$$

其中 $\Delta x_{t,0}^{(i)} \sim \mathcal{N}(0, I)$ 为噪声，$\Delta x_{t,1}^{(i)}$ 为真实增量运动。推理时从噪声出发，通过 ODE 求解器（如 Euler 法）逐步去噪得到预测运动。

为稳定重尾运动分布的建模，输入运动经过**尺度级联**处理（见 Figure 6 右）：将运动通过一组对数间隔的尺度系数 $s$ 缩放后，经 $\tanh(s \cdot \Delta x)$ 饱和映射，再拼接输入。消融实验（Table 3）显示，去除尺度级联导致 Best-5 误差从 0.029 升至 0.033，验证了其关键作用。

### 自回归推理流程

推理时，模型维护 KV 缓存以加速逐步生成。对于每个时间步 $t$ 和每条轨迹 $i$，流匹配头以变换器输出的条件特征 $\mathbf{z}_t^{(i)}$ 为条件，从噪声中采样增量运动 $\Delta x_t^{(i)}$，并在线更新轨迹位置 $x_t^{(i)} = x_{t-1}^{(i)} + \Delta x_t^{(i)}$。消融实验（Table D）证实，50 步逐步预测（$\Delta t = 0.01\text{s}$）的终点误差为 0.00141，远优于单步预测的 0.02823，验证了逐步分解复杂交互的必要性。



## 实验与关键发现

### 主结果：开放世界与物理运动预测

Myriad 在三个不同粒度的基准上全面评估了运动预测能力：开放世界运动（OWM）、物理推理（PhysicsIQ）和物理场景（Physion）。核心结论是，**完全避免外观渲染的稀疏轨迹建模，使模型在精度与效率之间实现了显著的帕累托改善**。

在 OWM 基准上（Table 1a），Myriad 在 Best-of-5 设定下取得了 0.029 的 minADE₅，优于视频生成模型 **MAGI-1** 的 0.037。这一优势在效率导向的 Best-within-5min 设定下急剧扩大：Myriad 的 minADE 为 0.013，而 MAGI-1 为 0.066，差距达 4 倍以上。这一差异的根源在于吞吐量的数量级鸿沟——Myriad 达到 2200 samples/min，而 MAGI-1 仅为 0.303 samples/min。在 PhysicsIQ 上，Myriad 与 **Wan2.2** 持平（0.115 vs 0.116），在 Physion 上则以 0.048 显著优于 MAGI-1 的 0.061。值得注意的是，Myriad 的参数量远小于这些视频生成基线，却能在精度上持平或超越，验证了“将容量聚焦于运动动力学而非稠密外观”这一设计哲学的有效性。

在台球规划任务中（Table 2），Myriad 以 78% 的准确率逼近仿真器 Oracle 的 84%，同时吞吐量达到 496.4 actions/min，远超基于图像到视频扩散的基线方法。这表明稀疏运动空间中的快速反事实推演，为需要大量未来假设探索的下游决策任务提供了可行的技术路径。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/012_Table_2.jpg]]
*Table 2: Planning Billiard Shots through Future Exploration. Left: We compare the Accuracy of landing a ball at a randomly selected goal position in a billiard simulation by unrolling potential futures starting from varying cue ball impulses. Under a fixed compute budget, our model surpasses dense world models from scratch using the same data. This is enabled by our methods’ low Latency, enabling us to sample a large number of potential futures. Right: We visualize results w.r.t. final target error and show its evolution over planning time for our model and an I2V baseline*

### 消融实验：设计选择的因果验证

**后验参数化：流匹配头与尺度级联。** Table 3 揭示了后验分布建模方式的决定性影响。将此前工作中使用的 GMM 头替换为流匹配（FM）头，Best-5 误差从 0.110 骤降至 0.033；进一步引入尺度级联后，误差降至 0.029。尺度级联的作用在于稳定重尾运动分布的建模——移除该组件后，预测质量出现可测量的退化，证实了其作为因果旋钮的关键地位。

**多步推理的必要性。** Table D 直接对比了不同时间步长下的预测精度。以 50 步（Δt=0.01s）逐步预测 0.5 秒未来时，终点误差（EPE）仅为 0.00141；而单步直接预测相同时间跨度的 EPE 高达 0.02823，误差放大近 20 倍。这一结果从因果层面验证了自回归逐步分解对于处理复杂交互的必要性——模型需要在每个微小时间步内条件化于已预测的轨迹，以逐步消解不确定性。

**流匹配推理步数缩放。** Table B 显示，将流匹配头的函数评估次数（NFE）从 1 提高到 50，EPE 从 0.00361 降至 0.00138，但 10 步后收益递减。这为实际部署中的精度-延迟权衡提供了定量依据。

**轨迹身份编码。** Table C 表明，随机正交单位球嵌入优于可学习嵌入和无嵌入方案，且支持零样本外推到训练时未见过的轨迹数量——这一性质源于连续空间中的正交标识机制，而非依赖有限码本。

### 效率-精度权衡分析

Figure 10 展示了 OWM 上的时间-精度权衡曲线。随着采样假设数 N 的增加，各模型的精度均单调提升，但 Myriad 的稀疏特性使其在相同计算预算下可探索数量级更多的假设。在 5 分钟时间预算内，Myriad 的 minADE 已降至视频基线的三分之一以下，而视频模型受限于单次推理的高昂成本，无法通过增加采样数来有效补偿精度差距。

### 不确定性校准

Figure 12 分析了后验不确定性与真实误差的相关性。从像素级精度（1/512）开始，模型的后验不确定性（绿线）与真实误差呈良好相关，表明流匹配头不仅提供了高质量的点预测，其分布宽度也具有实际校准意义——这为下游任务中的风险感知决策提供了可用的不确定性估计。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/017_Figure_12.jpg]]
*Figure 12: Posterior Uncertainty vs. Error. Starting around pixellevel*

### 失败模式与局限性

尽管 Myriad 在开放世界运动预测中表现出色，其设计存在若干结构性局限：

1. **静态相机假设**：模型当前无法处理移动相机场景，无法联合预测自我运动与场景动力学。这限制了其在第一人称视频或无人机视角等场景中的直接应用。

2. **伪真实轨迹依赖**：训练监督完全来自现成的点追踪器生成的伪真实轨迹。这意味着模型继承了追踪器的系统性偏差和偶发失败，精度上限受限于监督信号质量。在评估中，视频基线需通过点追踪器从生成视频中提取轨迹，可能因追踪误差而在指标上处于劣势，但这也反映了实际应用中的真实差距。

3. **预测时间跨度**：当前评估集中在 2.5-6.5 秒的较短时间跨度。自回归误差累积效应在更长时序预测中可能加剧，需要进一步验证。

4. **分布外泛化**：开放集泛化能力受限于互联网训练视频的分布。对于完全未见过的物体类别或极端物理交互，预测的物理一致性可能下降。

5. **串行解码延迟**：尽管通过 KV 缓存和融合并行变换器块已大幅加速，逐步预测的串行特性在极低延迟场景下仍存在固有瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/010_Table_1.jpg]]
*Table 1: Open-world & Physical Motion Prediction. We evaluate motion prediction capabilities across both open-world and constrained physical settings using the benchmark introduced in Sec. 4. Eliminating the need to model fine-grained pixel-level details lets our model focus on the dynamics of the scene, making it competitive with state-of-the-art video models in the Best-5 setting across all three subsets, despite having substantially fewer parameters and being substantially more efficient. The gap widens significantly in the efficiency-focused Best-5min setting, driven by the higher throughput*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/015_Table_3.jpg]]
*Table 3: Posterior Parametrization Ablation. Substituting previously used GMM-based heads with flow matching heads leads to significant improvements in accuracy and increases convergence substantially. Adding our scale cascade improves accuracy further*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/019_Table.jpg]]
*Table: B. Inference Time Scaling: Our approach achieves lower End-Point-Error in the Billiard simulation with more function evaluations of the diffusion head*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/020_Table.jpg]]
*Table: C. Trajectory ID Embedding: Our trajectory ID embeddings provide lower end-point-error in billiard simulations and enable zero-shot generalization to both increased and reduced number of trajectories*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2604_09527/figures/021_Table.jpg]]
*Table: D. Reasoning in multiple steps. We compare predicting 0.5 s into the future using models trained with different step sizes. Our standard method integrates 50 steps, while the other models perform fewer steps. Therefore, these models require fewer autoregressive steps, yet have to model more of the dynamics internally*



## 定位与知识库关联

### 1. 与现有工作的关系：稀疏运动预测 vs. 稠密视觉生成

Myriad 的核心定位是将未来预测从“稠密像素空间”迁移到“稀疏运动空间”，这与当前主流的视频生成模型和潜在空间模拟器形成了根本性的范式差异。

**与视频生成模型的对比。** 现有的视频生成模型（如 **MAGI-1**、**Wan2.2**、**CogVideo-X1.5**、**SkyReels V2**、**SVD 1.1**）通过生成稠密的未来帧来隐式地建模运动。这种方法存在一个结构性瓶颈：模型的大量容量被消耗在“可视化税”（visual tax）上——即重建纹理、光照、背景等外观细节，而这些细节对运动预测本身并非必要。在开放结尾的未来探索场景中，这种冗余计算导致两个严重后果：
- **采样成本过高**：生成完整视频帧的计算开销使得大规模假设探索（如数千次反事实推演）在经济上不可行。Table 1 显示，Myriad 的吞吐量达到 2200 samples/min，而 MAGI-1 仅为 0.303 samples/min，差距超过三个数量级。
- **分支效率低下**：视频模型难以在同一个初始帧上高效地生成多个不同的未来轨迹，因为每次采样都需要重新生成完整的视觉内容。

Myriad 通过将预测目标从“稠密视频帧”改为“稀疏的二维点轨迹”，完全避开了可视化税。这一设计选择使得模型可以将全部计算能力聚焦于运动动力学本身，从而在保持或超越预测精度的同时，实现了数量级的效率提升。

**与轨迹预测模型的对比。** 传统的轨迹预测模型（如 **Trajectron++**）通常针对特定场景（如自动驾驶、行人轨迹）设计，依赖手工定义的状态表示和场景图。相比之下，Myriad 是一个开放集模型：它从单张图像中学习通用的运动先验，不依赖特定类别的检测器或场景标注，因此可以泛化到更广泛的开放世界场景。

**与潜在空间世界模型的对比。** 一些工作（如 **Oasis**）在潜在空间中构建世界模型，通过压缩视觉表示来降低计算成本。然而，这些方法仍然需要在潜在空间中维护一个稠密的表示，其计算成本随空间分辨率的增加而增长。Myriad 的稀疏点表示则天然地与空间分辨率解耦：无论图像分辨率如何，模型仅处理用户定义的 K 个查询点，计算复杂度为 O(K) 而非 O(H×W)。

### 2. 方法适用边界

Myriad 的设计包含若干关键假设，这些假设定义了其适用边界：

**静态相机假设。** 模型假设输入图像来自一个静止的相机，所有观测到的运动都来自场景中的物体。这一假设简化了运动建模（无需分离自我运动和场景运动），但也排除了手持相机、车载相机等动态拍摄场景。当前方法无法直接处理移动相机下的运动预测，也无法联合预测自我-场景运动。

**短时间跨度预测。** 评估主要在 2.5-6.5 秒的时间跨度上进行。虽然自回归生成机制理论上支持任意长度的预测，但随着时间步的增加，误差会逐步累积。Table D 的消融实验显示，50 步多步预测（Δt=0.01s）的终点误差（EPE）为 0.00141，远优于单步预测的 0.02823，但这仍然是在相对较短的时间窗口内的结果。更长时间的预测需要进一步验证。

**训练分布依赖。** 模型的开放集泛化能力受限于互联网训练视频的分布。对于训练数据中未出现过的物体类别、物理交互或极端动力学场景，模型的预测质量可能下降。虽然随机正交轨迹 ID 嵌入（Table C 验证）支持零样本外推到不同的轨迹数量，但场景语义的泛化仍然依赖于训练数据的覆盖范围。

**伪真实轨迹的偏差。** 训练监督依赖于现成的点追踪器（如 CoTracker）生成的伪真实轨迹。这意味着 Myriad 继承了这些追踪器的偏差和偶尔的失败模式。当追踪器在遮挡、快速运动或纹理缺失区域产生错误时，这些错误会被编码到模型的训练信号中，限制其精度上限。

### 3. 局限与开放问题

**动态相机扩展。** 如何将 Myriad 扩展到动态相机场景是一个关键的开放问题。可能的路径包括：引入相机运动参数作为额外的条件信号；联合预测相机位姿和场景运动；或者利用多帧输入来显式地分解自我运动和物体运动。这些扩展需要重新设计运动令牌的构建方式和位置编码方案。

**训练分布外的泛化。** 模型能否在全新的物理场景中保持合理预测？当前的实验（OWM、PhysicsIQ、Physion）覆盖了多样化的场景，但仍然在训练分布的范围内。对于完全未见过的物理参数（如不同的重力加速度、摩擦系数）或物体属性（如弹性、质量），模型的泛化能力尚未被系统评估。引入显式物理约束（如刚体动力学方程）可能有助于减少对大数据集的依赖并提高样本效率，但如何在保持开放集灵活性的同时融入物理先验是一个设计挑战。

**更长时域的预测。** 随着预测时间跨度的增加，自回归模型的误差累积问题会变得更加严重。可能的缓解策略包括：引入多尺度时间建模（在不同时间分辨率上预测）；使用闭环训练策略（将预测轨迹反馈给模型作为条件）；或者结合基于物理的模拟器进行混合预测。

**下游应用的优势与不足。** 在机器人操控、自动驾驶等闭环场景中，Myriad 的稀疏运动预测相比专门的闭环模型（如基于强化学习的策略网络）有哪些优势和不足？一方面，Myriad 的通用运动先验可能提供更好的场景理解和多模态未来预测；另一方面，它缺乏对具体执行器动力学和任务奖励的直接建模。在台球规划实验中（Table 2），Myriad 达到了 78% 的准确率，接近模拟器 Oracle 的 84%，但仍有 6% 的差距，这表明在需要精确物理交互的任务中，纯数据驱动的方法仍有改进空间。

**串行解码的延迟。** 尽管通过 KV 缓存和融合并行变换器块已经大幅加速了推理，自回归的逐步预测特性在串行解码时仍存在一定延迟。在需要实时响应的应用中（如高频控制回路），这一延迟可能成为瓶颈。进一步的研究可以探索非自回归的解码策略或模型蒸馏技术来降低延迟。



## 原文 PDF

![[paperPDFs/CVPR_2026/Envisioning_the_Future_One_Step_at_a_Time.pdf]]
