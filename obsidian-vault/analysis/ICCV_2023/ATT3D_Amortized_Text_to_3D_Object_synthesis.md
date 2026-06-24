---
title: "ATT3D: Amortized Text-to-3D Object synthesis"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/ATT3D_Amortized_Text_to_3D_Object_synthesis.pdf
aliases:
- AAT3
- ATT3D
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入从文本嵌入c到点编码器参数w的映射网络（超网络m），将逐提示优化摊销为多提示联合训练，实现组件重用与快速推理。"
primary_logic: "通过同时优化大量提示，共享的NeRF生成模型学会分解并重用三维组件（如动物、道具），从而以更低的总计算量覆盖多提示，并天然具备向未见组合提示的泛化能力及提示间平滑插值能力。"
claims:
- "ATT3D在任意计算预算下，其CLIP R-probability均高于逐提示优化基线，且训练总时间显著缩短。"
- "训练完成的ATT3D模型可在<1秒内、单消费级GPU上生成准确的3D物体，无需任何额外优化。"
- "模型对未见提示表现出强泛化能力：仅用12.5%提示训练时，对未见提示的生成质量已超过逐提示优化在全部提示上的效果。"
- "通过摊销插值权重，ATT3D能在测试时生成提示间的平滑连续过渡，用于创建新资产或动画。"
---

# ATT3D: Amortized Text-to-3D Object synthesis

> [!tip] 核心洞察
> 通过同时优化大量提示，共享的NeRF生成模型学会分解并重用三维组件（如动物、道具），从而以更低的总计算量覆盖多提示，并天然具备向未见组合提示的泛化能力及提示间平滑插值能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ATT3D: 摊销式文本到三维物体合成 |
| 英文题名 | ATT3D: Amortized Text-to-3D Object synthesis |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2306.07349); [Project](https://research.nvidia.com/labs/toronto-ai/ATT3D/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ATT3D (Amortized Text-to-3D) |
| Dataset | DF27 (DreamFusion的27个提示), 组合式猪提示集（64个提示）, 组合式动物提示集（2400个提示）, 推理速度 |

> [!tip] 效果简介
> - DF27 (DreamFusion的27个提示) 上，CLIP R-probability vs 计算预算 为 ATT3D，对比 per-prompt optimization，变化 在任何计算预算下均更高。
> - 组合式猪提示集（64个提示） 上，CLIP R-probability vs 计算预算 为 ATT3D，对比 per-prompt optimization，变化 见到与未见提示上均更高；未见提示分割为0%时，随机初始化基线表现差。
> - 组合式动物提示集（2400个提示） 上，CLIP R-probability vs 计算预算 为 ATT3D，对比 per-prompt optimization，变化 仅见12.5%提示时，未见提示质量即超越逐提示优化在全部提示上的结果。

## 概述

文本到三维物体合成（Text-to-3D, TT3D）旨在根据自然语言描述生成对应的三维资产。现有方法（如 **DreamFusion**，Poole et al., 2022）对每个提示独立优化一个神经辐射场（NeRF），这一过程耗时约4小时/提示，需多GPU并行，且无法在不同提示间共享已学知识——每个新提示都需从头开始完整优化。这种逐提示优化的范式构成了该领域的关键效率瓶颈。

**ATT3D** 提出了一种摊销式（amortized）文本到三维合成范式。其核心思路是将原本独立的逐提示优化过程，重构为两阶段流程：**离线阶段**在大量文本提示上联合训练一个共享的NeRF生成模型；**在线阶段**，该模型可对任意提示（包括训练中未见的组合）在 **< 1秒**内、单张消费级GPU上直接生成三维物体，无需任何额外优化。这一数量级加速源于模型在摊销训练中学会了分解并重用三维组件（如动物形态、道具、材质），从而以更低的总计算量覆盖多提示，并天然具备向未见组合提示的泛化能力。

在方法谱系上，ATT3D 基于 DreamFusion 的分数蒸馏采样（Score Distillation Sampling, SDS）框架，但在 **点编码器参数生成方式** 这一关键环节引入了根本性改变：通过一个映射网络（超网络）从文本嵌入直接生成点编码器的多分辨率网格参数，使参数在提示间共享。这一定位使其区别于 DreamFusion 和 **Magic3D**（Lin et al., 2022）等逐提示优化基线。训练稳定性方面，ATT3D 采用 Adam 优化器配合谱归一化，替代了 DreamFusion 的 Distributed Shampoo 优化器。此外，ATT3D 通过在训练时摊销插值权重，使模型在测试时可接受插值嵌入并生成提示间的平滑连续过渡，用于创建新资产或动画。

核心定量结果（Figure 6）表明：在 DreamFusion 的27个提示集（DF27）、组合式猪提示集（64个提示）和组合式动物提示集（2400个提示）上，ATT3D 在任意计算预算下的 CLIP R-probability 均高于逐提示优化基线。更关键的是，在仅使用 **12.5%** 提示训练时，ATT3D 对未见提示的生成质量已超越逐提示优化在全部提示上从头训练的效果（Figure 6右, Figure 8）。定性分析（Figure 7）揭示，摊销训练能自发发现规范朝向并保持语义属性（如“蓝色气球”始终为蓝色），而逐提示优化常出现颜色错配或失败。

方法的主要局限包括：继承自现有T2T3D范式的对扩散模型质量的依赖、训练目标方差大导致对提示工程敏感，以及相似提示在摊销训练中可能坍缩为相同场景。开放问题指向更大规模提示集的设计、更强生成器骨干的需求，以及摊销训练与更高质量三维表示（如纹理网格）结合的可能性。

## 背景与动机

### 文本到三维生成：从逐提示优化到摊销推理

文本到三维（Text-to-3D, T2T3D）物体的自动生成在游戏、影视、虚拟现实等领域有广泛需求。近期工作，尤其是**DreamFusion**（Poole et al., 2022），利用预训练的文本到图像扩散模型作为先验，通过分数蒸馏采样（Score Distillation Sampling, SDS）优化神经辐射场（NeRF），首次实现了从任意文本提示直接生成三维物体的能力，无需任何三维训练数据。

然而，这类方法的根本瓶颈在于**逐提示独立优化**的范式：对于每一个新的文本提示，系统需要从头训练一个完整的NeRF网络。这带来了三个核心问题：

1. **推理成本极高**：每个提示的优化耗时约4小时，且需要多个高性能GPU，严重限制了实际应用。
2. **知识无法复用**：不同提示的优化过程完全独立，模型无法从先前提示中学习共享的三维结构或纹理先验——即使“一只穿毛衣的猪”和“一只穿盔甲的猪”显然共享着猪的几何形态。
3. **缺乏泛化与插值能力**：逐提示优化无法在测试时对未见提示进行零样本生成，也无法实现提示间的平滑过渡以支持用户引导的资产创建。

### 摊销优化的核心洞察

ATT3D 的核心思想是**将逐提示优化转化为多提示联合训练的摊销问题**。其关键洞察在于：通过同时优化大量文本提示，共享的NeRF生成模型能够学会分解并重用三维组件（如动物形态、道具、材质），从而以更低的总计算量覆盖多提示，并天然具备向未见组合提示的泛化能力及提示间平滑插值能力。

具体而言，ATT3D 将T2T3D流程拆分为两个阶段（Figure 1）：
- **离线摊销训练阶段**：一个映射网络（超网络）从文本嵌入生成NeRF点编码器的参数，使得单个模型能够同时表示多个提示的三维物体。
- **用户侧前馈推理阶段**：训练完成后，对于任意新提示，模型可在**不到1秒内、单张消费级GPU上**生成准确的三维物体，无需任何额外优化。

这一范式转变的动机源于一个简单观察：如果逐提示优化需要4小时/提示，那么优化100个提示需要400小时；而摊销训练通过共享计算，可以在远小于该总时间的预算内完成，且获得向未见提示泛化的额外收益。

## 核心创新

ATT3D 的核心创新在于将文本到三维（Text-to-3D）的优化范式从**逐提示独立优化**重构为**跨提示联合摊销训练**。现有方法（如 **DreamFusion**，Poole et al., 2022）对每个文本提示独立训练一个神经辐射场（NeRF），耗时约4小时/提示且无法跨提示共享知识。ATT3D 通过引入一个从文本嵌入到点编码器参数的**映射网络（超网络 m）**，将这一过程转化为多提示联合训练，实现了组件重用、快速推理和对未见提示的泛化。

### 关键变更槽位（Changed Slots）

**1. 点编码器参数生成方式：从固定/独立优化到超网络调制**

- **基线做法**：DreamFusion 中，点编码器 $\gamma_{\pmb w}$ 的参数 $\pmb w$ 为每个提示独立优化，或采用固定编码方式，不存在跨提示的参数共享机制。
- **ATT3D 做法**：引入映射网络 $m$，从文本编码器（T5-XXL 与 CLIP）输出的文本嵌入 $\pmb c$ 直接生成点编码器的多分辨率哈希网格参数 $\pmb w$：
  $$\pmb w = \mathrm{Hypernetwork}(\pmb c)$$
  具体实现中，文本嵌入 $\pmb c$ 经展平后通过谱归一化线性层和 SiLU 激活得到中间向量 $\pmb v$，再经另一谱归一化线性层并重塑为网格参数 $\pmb w$：
  $$\pmb v = \mathrm{SiLU}(\mathrm{linear}_{\mathrm{w/ bias}}^{\mathrm{spec.norm}}(\mathrm{flatten}(\pmb c)))$$
  $$\pmb w = \mathrm{reshape}(\mathrm{linear}_{\mathrm{no bias}}^{\mathrm{spec.norm}}(\pmb v))$$
  这一设计使得所有提示共享同一个 NeRF 生成模型，映射网络学会将语义相近的提示映射到共享的几何与纹理组件上，从而实现**跨提示的知识复用**（Figure 15 展示了狐猴在不同活动间复用、猩猩重着色为黑猩猩等案例）。

**2. 优化稳定性技术：从 Distributed Shampoo 到 Adam + 谱归一化**

- **基线做法**：DreamFusion 使用 Distributed Shampoo 优化器配合动量项来稳定分数蒸馏采样（SDS）训练。
- **ATT3D 做法**：改用更简洁的 Adam 优化器（无动量），并在映射网络中引入**谱归一化**以保证训练数值稳定性。消融实验表明，去除谱归一化将导致训练无法收敛（Section 3.2.1, App. B.1.5），这是多提示联合训练场景下的关键稳定性保障。

**3. 提示间插值能力：从不可插值到摊销插值训练**

- **基线做法**：逐提示优化模式下，每个提示独立训练一个 NeRF，测试时无法实现提示间的平滑过渡。
- **ATT3D 做法**：训练时对插值权重 $\alpha$ 进行摊销，使模型在测试时可接受两个提示嵌入的线性插值并生成连续过渡：
  $$m\left( (1-\alpha) \pmb c_1 + \alpha \pmb c_2 \right)$$
  通过这一机制，ATT3D 可在无需额外优化的前提下，快速生成提示间的连续资产序列甚至动画（Figure 3 展示了景观、服装、建筑、车辆的平滑过渡，以及树木四季变化的动画）。消融实验证实，未经过插值摊销训练的模型在插值嵌入上产生次优结果，加入插值摊销后质量显著提升（Figure 16, Section B.1.14）。

### 创新机制的本质

上述三个变更槽位共同支撑了一个核心洞察：**通过同时优化大量提示，共享的 NeRF 生成模型学会分解并重用三维组件**（如动物身体、道具、材质），从而以更低的总计算量覆盖多提示，并天然具备向未见组合提示的泛化能力。这一机制在实验中得到验证：仅使用 12.5% 的提示训练时，ATT3D 对未见提示的生成质量已超过逐提示优化在全部提示上的效果（Figure 6 右, Figure 8）。

## 整体框架

ATT3D 将文本到三维（TT3D）的生成过程拆分为两个阶段：**离线摊销优化**与**前馈式快速推理**。其核心思想是用一个共享的映射网络（超网络）替代 DreamFusion 等逐提示独立优化的范式，使模型在大量文本提示上联合训练，从而摊销优化成本并实现跨提示的知识共享。

### 管道总览

整个管道由六个关键模块串联构成，如 Figure 4 所示（红色部分为相对于 DreamFusion 管道的改动）：

1. **文本编码器**：使用预训练的 T5-XXL 和 CLIP 编码器将任意文本提示映射为固定维度的文本嵌入 $\pmb c$。该嵌入同时供给下游的扩散模型和新增的映射网络。
2. **映射网络 $m$（超网络）**：从文本嵌入 $\pmb c$ 直接生成点编码器的全部参数 $\pmb w$，即 $\pmb w = \mathrm{Hypernetwork}(\pmb c)$。这是实现摊销的核心模块——同一网络为不同提示输出不同的点编码器参数，从而在参数空间中建立提示间的共享结构。
3. **点编码器 $\gamma_{\pmb w}$**：基于 Instant NGP 的多分辨率哈希网格对三维空间坐标 $\pmb x$ 进行编码。其网格参数 $\pmb w$ 由映射网络动态调制，使编码器本身成为文本条件的函数。
4. **NeRF MLP $\pmb \nu$**：一个小型 MLP，接收编码后的点特征与观察方向，输出密度和颜色（辐射度）$\pmb r$：
   $$\pmb r = \pmb \nu \left( \gamma_{\pmb w} \left( \pmb x \right) \right)$$
5. **体渲染**：根据相机参数从 NeRF 表示中渲染二维视图。
6. **分数蒸馏采样（SDS）损失**：利用预训练的文本条件扩散模型计算梯度，同时更新 NeRF MLP $\pmb \nu$ 和映射网络 $m$（等效地也更新了点编码器 $\gamma_{\pmb w}$ 的参数）。

### 映射网络的内部结构

映射网络将文本嵌入转换为点编码器参数的过程分为两步（Eq. 4-5）：

$$\pmb v = \mathrm{SiLU}(\mathrm{linear}_{\mathrm{w/ bias}}^{\mathrm{spec.norm}}(\mathrm{flatten}(\pmb c)))$$

$$\pmb w = \mathrm{reshape}(\mathrm{linear}_{\mathrm{no bias}}^{\mathrm{spec.norm}}(\pmb v))$$

即先将文本嵌入展平后通过带谱归一化的线性层和 SiLU 激活得到中间向量 $\pmb v$，再将 $\pmb v$ 通过第二个谱归一化线性层并重塑，得到多分辨率网格的完整参数 $\pmb w$。谱归一化在此处起到稳定训练的关键作用——消融实验表明，去除谱归一化会导致训练数值不稳定、无法收敛。

### 训练与推理流程

**训练阶段**（Figure 4 左）：对一批文本提示采样，文本编码器输出嵌入 $\pmb c$，映射网络生成对应的点编码器参数 $\pmb w$，NeRF 渲染多视角图像，扩散模型通过 SDS 损失提供训练信号，梯度反向传播至 NeRF MLP 和映射网络。训练时还采用初始密度偏置 $\mathrm{densityBias}(\pmb x) = 10(1 - 2\| \pmb x \|_2)$ 防止场景退化为空。

**推理阶段**（Figure 4 右）：给定任意文本提示（包括训练中未见过的提示），仅需一次前馈——文本编码器生成 $\pmb c$，映射网络输出 $\pmb w$，NeRF 即可直接表示三维物体，无需任何额外优化。整个推理过程在单张消费级 GPU 上耗时小于 1 秒。

### 提示间插值能力

ATT3D 在训练时摊销了插值权重 $\alpha$，使映射网络学会处理文本嵌入的凸组合：

$$m\left( (1-\alpha) \pmb c_1 + \alpha \pmb c_2 \right)$$

在测试时，用户只需滑动 $\alpha \in [0,1]$，即可生成两个提示之间的平滑连续过渡（如“木制海盗船”到“橡胶救生筏”），用于创建新资产或动画。这一能力是逐提示优化范式所不具备的——后者每个提示独立优化，无法在测试时进行提示间插值。

### 与基线的架构公平性

为保证对比的公平性，摊销训练与逐提示训练采用完全相同的 NeRF 渲染实现和 SDS 损失，网络架构也保持一致（仅映射网络的引入方式不同）。所有对比均以每个提示的平均渲染帧数作为计算预算单位，消除了 GPU 数量和批大小差异的影响。

### 补充图表

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/001_Figure_1.jpg]]
*Figure 1: Our method initially trains one network to output 3D objects consistent with various text prompts. After, when we receive an unseen prompt, we produce an accurate object in \< 1 second, with 1 GPU. Existing methods re-train the entire network for every prompt, requiring a long delay for the optimization to complete. Further, we can interpolate between prompts for user-guided asset generation (Fig. 3). We include a project webpage with an overview and videos*

## 核心模块与公式推导

### 两阶段文本到三维管道

ATT3D将文本到三维（TT3D）过程解耦为两个阶段：**离线摊销优化**阶段与**前馈生成**阶段。在离线阶段，系统在大量文本提示上同时优化一个共享模型；在用户使用阶段，训练完成的模型可直接根据输入提示生成三维物体，无需任何额外优化（Figure 4）。

管道由以下核心模块串联构成：

1. **文本编码器**：使用预训练的T5-XXL和CLIP编码器将文本提示映射为嵌入向量 $\pmb c$。该嵌入同时供给扩散模型（用于SDS损失）和映射网络。
2. **映射网络（超网络）$m$**：从文本嵌入 $\pmb c$ 生成点编码器的全部参数 $\pmb w$，是摊销优化的核心枢纽。
3. **点编码器 $\gamma_{\pmb w}$**：基于Instant NGP的多分辨率哈希网格对三维坐标 $\pmb x$ 进行编码，其网格参数由映射网络调制。
4. **NeRF MLP $\pmb\nu$**：接收编码后的点与观察方向，输出密度和辐射度 $\pmb r$。
5. **体渲染**：根据相机参数从NeRF渲染二维图像。
6. **分数蒸馏采样（SDS）损失**：利用预训练文本条件扩散模型计算梯度，更新NeRF和映射网络。

训练时，梯度通过SDS损失反向传播，同时更新NeRF MLP $\pmb\nu$、映射网络 $m$ 以及（等效地）点编码器 $\gamma_{m(c)}$。推理时，仅使用管道前半部分（至NeRF输出）即可表示三维物体。

### 核心公式体系

**NeRF辐射度输出**（Eq.1, Section 2.1）：

$$\pmb r = \pmb\nu\left(\gamma_{\pmb w}(\pmb x)\right)$$

给定空间坐标 $\pmb x$，先通过参数化的点编码器 $\gamma_{\pmb w}$ 编码，再经小型MLP $\pmb\nu$ 输出密度和颜色 $\pmb r$。这是DreamFusion范式下NeRF的基本形式。

**超网络生成点编码器参数**（Eq.3, Section 3.1）：

$$\pmb w = \mathrm{Hypernetwork}(\pmb c)$$

从文本嵌入 $\pmb c$ 通过超网络直接输出点编码器的所有权重 $\pmb w$。这是ATT3D区别于逐提示优化方法的关键公式——参数在提示间共享，而非为每个提示独立优化。

**中间向量 $\pmb v$ 的生成**（Eq.4, Section 3.1）：

$$\pmb v = \mathrm{SiLU}\left(\mathrm{linear}_{\mathrm{w/ bias}}^{\mathrm{spec.norm}}(\mathrm{flatten}(\pmb c))\right)$$

将文本嵌入展平后，经谱归一化线性层和SiLU激活得到中间向量 $\pmb v$。谱归一化在此处引入以稳定训练（消融实验表明去除谱归一化将导致数值不稳定和无法收敛）。

**参数 $\pmb w$ 的生成**（Eq.5, Section 3.1）：

$$\pmb w = \mathrm{reshape}\left(\mathrm{linear}_{\mathrm{no bias}}^{\mathrm{spec.norm}}(\pmb v)\right)$$

将 $\pmb v$ 再通过谱归一化线性层（无偏置）并重塑，得到点编码器的多分辨率网格参数 $\pmb w$。超网络调制方式相比拼接方式降低推理开销约20-75%，且不增加额外训练时间。

**提示插值嵌入**（Eq.6, Section 3.2.2）：

$$m\left((1-\alpha)\pmb c_1 + \alpha\pmb c_2\right)$$

将两个提示的文本嵌入按权重 $\alpha$ 进行线性插值后输入映射网络，实现提示间连续过渡。训练时摊销插值权重 $\alpha$，使模型在测试时可接受插值嵌入并生成平滑过渡资产或动画。

**初始密度偏置**（Eq.7, Section B.1.9）：

$$\mathrm{densityBias}(\pmb x) = 10(1 - 2\|\pmb x\|_2)$$

为NeRF的原始密度输出添加空间偏置，防止训练初期退化为空场景。该偏置在训练早期为原点附近区域赋予正密度，引导模型学习非平凡几何。

### 插值机制的扩展公式

ATT3D探索了多种提示间插值方式（Section B.1.14），均在映射网络接收插值嵌入的前提下，改变扩散模型使用的嵌入或损失构造：

**损失插值**（Eq.9）：

$$\mathcal{L}_{\mathrm{final}} = (1-\alpha)\mathcal{L}_{\mathrm{prompt 1}} + \alpha\mathcal{L}_{\mathrm{prompt 2}}$$

对两个提示的损失进行加权组合，使物体同时满足两个损失。

**随机损失插值**（Eq.10）：

$$\pmb c' = (1-Z)\pmb c_1 + Z\pmb c_2 \quad \text{where } Z \sim \mathbf{Bern}(\alpha)$$

以概率 $\alpha$ 随机选取第二个提示，等价于在损失函数间按伯努利分布采样。

**引导权重插值**（Eq.11）：

$$\hat{\epsilon} = \epsilon_{\mathrm{uncond.}} + (1-\alpha)\omega_1\epsilon_{\mathrm{prompt 1}} + \alpha\omega_2\epsilon_{\mathrm{prompt 2}}$$

在扩散模型的无条件与有条件噪声预测之间进行引导强度插值，控制两个提示的贡献。该方式与Magic3D中的引导插值思路一致，但ATT3D将其纳入摊销训练框架。

### 关键设计决策

- **超网络调制 vs 拼接**：消融实验表明，采用超网络调制点编码器参数比将文本嵌入直接拼接到NeRF输入的方式，推理开销降低约20-75%，且训练时间不增加。
- **谱归一化**：去除谱归一化将导致训练数值不稳定和无法收敛，是摊销训练成功的关键稳定技术。
- **Dirichlet插值权重**：插值权重 $\alpha$ 的浓度参数 $\kappa$ 影响生成结果——小 $\kappa$ 聚焦端点（保持原始提示特征），大 $\kappa$ 聚焦中点（融合两个提示特征）。训练早期选择 $\kappa$ 对最终结果有决定性影响。

## 实验与分析

### 核心定量结果：摊销训练在任何计算预算下均优于逐提示优化

ATT3D的核心优势在于将文本到三维（TT3D）的优化过程从“每个提示独立训练”转变为“多提示联合摊销训练”，这一转变在计算效率与生成质量上均带来显著增益。论文通过**CLIP R-probability**（CLIP模型将渲染图像正确归类于对应提示的概率，相比R-precision保留了置信度信息、噪声更低）作为主要定量指标，在三个不同规模的提示集上系统比较了ATT3D与逐提示优化基线（即**DreamFusion**, Poole et al., 2022）的表现。

**DF27提示集（27个提示）**：如Figure 6左所示，ATT3D在任意计算预算（以每提示平均渲染帧数衡量）下，其CLIP R-probability均高于逐提示优化基线。这一结果表明，摊销训练不仅总训练时间更短，而且在相同计算投入下能获得更高质量的生成结果。

**组合式猪提示集（64个提示）**：该提示集采用“a pig {activity} {theme}”的组合结构，按活动（行）和主题（列）组织，对角线上的提示被留作未见测试集。Figure 6中图显示，ATT3D在已见提示和未见提示上均超越逐提示优化。值得注意的是，逐提示优化无法对未见提示进行零样本生成，其在未见提示上的表现仅相当于随机初始化水平，而ATT3D无需额外优化即可在未见提示上取得显著更高的质量（Figure 2）。

**组合式动物提示集（2400个提示）**：这是最大规模的测试集，进一步验证了摊销训练的扩展性与泛化能力。Figure 6右图展示了不同训练提示比例（12.5%、50%、100%）下的结果。**关键发现**：当仅使用12.5%的提示进行摊销训练时，模型在未见提示上的生成质量已超过逐提示优化在全部提示上的表现。当训练提示比例达到50%时，已见与未见提示之间的泛化差距很小，表明模型能够从少量提示中习得可迁移的三维生成能力。Figure 8的定性结果佐证了这一结论：在12.5%和50%训练分割下，ATT3D对未见测试提示的渲染结果在几何完整性和纹理一致性上均优于逐提示优化。

### 推理速度：从数小时到亚秒级的数量级跨越

推理速度是ATT3D的另一决定性优势。逐提示优化方法（如DreamFusion）对每个新提示需要从头优化NeRF，耗时约**4小时/提示**，且需要多GPU支持。相比之下，ATT3D完成摊销训练后，对任意提示（包括未见提示）的推理仅需**< 1秒**，在**单个消费级GPU**上即可完成（Abstract, Section 1, Figure 1 caption）。这一数量级的加速使得TT3D从离线研究工具转变为可实时交互的用户应用。

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/021_Figure.jpg]]

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/022_Figure.jpg]]

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/026_Figure.jpg]]

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/028_Figure.jpg]]

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/029_Figure.jpg]]

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/030_Figure.jpg]]

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/032_Figure.jpg]]

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/034_Figure.jpg]]

### 泛化能力与组件重用机制

ATT3D的泛化能力源于摊销训练迫使模型学会在提示间共享和重组三维组件。Figure 7通过“...holding a blue balloon”类提示的对比揭示了这一机制：摊销优化能够发现规范化的物体朝向，并始终将气球渲染为蓝色；而逐提示优化可能仅将背景染蓝，甚至完全无法生成气球。Figure 15在DF411提示集上提供了更直接的组件重用证据——模型将同一只狐猴（lemur）重用于不同活动场景，或将猩猩（orangutan）重新着色为黑猩猩（chimpanzee）并赋予不同动作。这种组件重用解释了为何摊销训练能以更低的总计算量覆盖更多提示。

### 提示间插值：连续资产生成与动画

ATT3D通过在训练时摊销插值权重α（从Dirichlet分布采样），使模型在测试时能够接受两个提示嵌入的线性插值输入，生成平滑的连续过渡（Eq.6, Section 3.2.2）。Figure 3展示了服装（“dress made of fruit” → “dress made of garbage bags”）、建筑（“cottage with a thatched roof” → “house in Tudor Style”）、车辆（“red convertible” → “destroyed car”）和季节变化（树在春夏秋冬的过渡）等多种插值结果。Figure 20补充了更多损失插值（loss interpolation）的实例，包括不同建筑风格、角色、交通工具、植物和景观之间的平滑变换，以及“a baby dragon”成长为成年龙的简单动画。

### 消融实验

**谱归一化的必要性**：去除映射网络中的谱归一化（spectral normalization）会导致训练数值不稳定，无法收敛（Section 3.2.1, App. B.1.5）。这一发现解释了为何ATT3D能够使用简单Adam优化器（无动量）替代DreamFusion的Distributed Shampoo优化器。

**超网络调制 vs. 拼接**：相比将文本嵌入直接拼接到点编码器输入的方式，采用超网络调制（hypernetwork modulation）可降低推理开销约20-75%，且不增加额外训练时间（App. B.1.3）。

**插值摊销训练的影响**：未在插值嵌入上进行训练的模型，在测试时对插值提示产生次优结果（物体在两个端点之间简单消融）；加入插值摊销训练后，模型能够生成同时满足两个提示特征的连贯中间态（Figure 16, Figure 18）。

**Dirichlet浓度参数κ的作用**：插值权重α的Dirichlet分布浓度参数κ影响生成结果的特性。小κ使分布聚焦于端点（保留原始提示特征），大κ使分布聚焦于中点（融合两个提示的特征）。若希望插值结果包含原始提示，应从κ小开始训练；若希望生成满足两个提示的融合物体，应从κ大开始训练（Figure 19, Section B.1.14）。

### 扩展性与局限性

ATT3D在DF411提示集（411个提示，超过DF27十倍以上）上的训练结果显示仅有轻微质量下降（Figure 9, Figure 14），验证了方法的扩展潜力。然而，论文也明确指出若干局限：

- **生成多样性不足**：相似提示在摊销训练中可能坍缩为相同场景，限制了输出的多样性。
- **对提示工程敏感**：继承自SDS训练范式，训练目标方差大，对提示措辞敏感。
- **未训练插值时的退化**：未专门进行插值摊销训练的模型在插值嵌入上生成质量下降，需额外训练才能获得Figure 3所示的平滑过渡效果。
- **更大规模提示集的需求**：当前提示集规模尚不足以测试摊销训练的极限，需要更大规模、以物体为中心的提示集进行进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/003_Figure.jpg]]
*Figure: Rendered frames from ATT3D with text embedding (1 − α)c1 + αc2 for α ∈ [0, 1]*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/008_Figure.jpg]]
*Figure: Testing prompt for Amortized 50% split, at 4800*

![[assets/figures/papers/paper_list_l36_https_arxiv_org_abs_2306_07349/figures/018_Figure.jpg]]
*Figure: Finetuning iteration Various strategies on “a pig wearing medieval armor holding a blue balloon” Amortized*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

**ATT3D** 的核心定位是对现有逐提示优化范式（per-prompt optimization）的**摊销化改造**，而非完全替代。其直接对比基线为 **DreamFusion**（Poole et al., 2022），后者代表当时文本到三维（TT3D）的主流方案：对每个文本提示独立优化一个神经辐射场（NeRF），需约4小时/提示且依赖多GPU。ATT3D 保留了 DreamFusion 的渲染管道与分数蒸馏采样（SDS）损失框架，但在关键环节引入结构性变革：

- **参数生成方式**：DreamFusion 中 NeRF 的点编码器参数 $w$ 为每个提示独立优化，提示间无知识共享。ATT3D 引入映射网络（超网络）$m$，从文本嵌入 $c$ 直接生成 $w = \text{Hypernetwork}(c)$（Eq.3），使参数在提示间共享，从而实现组件重用与跨提示泛化。
- **优化稳定性**：DreamFusion 使用 Distributed Shampoo 优化器及动量。ATT3D 改用 Adam 优化器（无动量），并引入谱归一化以稳定超网络训练（Section 3.2.1）。消融实验表明，去除谱归一化将导致数值不稳定、无法收敛。
- **插值能力**：DreamFusion 无法在测试时进行提示间插值。ATT3D 在训练时摊销插值权重 $\alpha$，使模型可在测试时接受插值嵌入 $m((1-\alpha)c_1 + \alpha c_2)$（Eq.6）并生成平滑过渡，这是逐提示优化范式天然不具备的能力。

另一个辅助基线是 **Magic3D**（Lin et al., 2022），ATT3D 将其用于微调阶段和高级纹理优化（Figure 17），并借鉴了其引导权重插值思路（Eq.11），但 Magic3D 本身未实现摊销化。

### 2. 适用边界

ATT3D 的优势在以下条件下最为显著：

- **多提示场景**：当需要为大量文本提示生成三维物体时，摊销训练的总计算量远低于逐提示独立优化，且提示数量越大优势越明显（Figure 6）。
- **组合式提示集**：在具有共享语义组件的提示集（如“a pig {activity} {theme}”）上，模型能自然分解并重用组件，泛化至未见组合（Figure 2, Figure 8）。
- **快速推理需求**：训练完成后，单次生成仅需 <1 秒、单消费级 GPU，适用于交互式应用场景。
- **提示间连续过渡**：需要生成资产连续体或动画时，摊销插值训练提供了逐提示优化无法实现的平滑过渡能力（Figure 3, Figure 20）。

方法的适用边界受以下因素制约：

- **提示集规模与多样性**：当前实验最大提示集为 DF411（411个提示）和组合式动物集（2400个提示）。对于完全开放域的任意自然语言提示，尚缺乏大规模、以物体为中心的提示集来测试摊销训练的扩展极限。
- **扩散模型能力上限**：ATT3D 继承自 DreamFusion 的 SDS 范式，生成质量受限于底层文本到图像扩散模型的能力。论文明确指出需要更强力的扩散模型以提升质量与鲁棒性。
- **生成多样性不足**：相似提示在摊销训练中可能坍缩为相同场景，这是共享参数带来的固有张力。

### 3. 局限与开放问题

论文明确指出的局限包括：

1. **继承自 T2T3D 范式的系统性问题**：训练目标方差大，对提示工程敏感；底层扩散模型的局限直接制约生成质量。
2. **多样性坍缩**：摊销训练中相似提示可能映射到相同三维场景，缺乏逐提示优化的多样性。
3. **插值需专门训练**：未对插值进行摊销训练的模型在插值嵌入上产生次优结果，需专门设计插值摊销策略（Figure 16, Figure 18）。
4. **提示集扩展未充分验证**：需要更大规模、以物体为中心的提示集来测试摊销训练的扩展极限。

开放问题指向以下方向：

- **提示集设计**：如何为开放域文本提示设计更大且可被有效训练的提示集？
- **超网络容量**：当提示数量极大时，简单的超网络调制是否足够，还是需要更强大的生成器骨干？
- **表示升级**：摊销训练能否与更高质量的三维表示（如 Magic3D 的纹理网格）结合，实现高分辨率实时生成？
- **通用先验**：能否通过训练更通用的文本到三维先验模型，将摊销优化扩展到完全无限制的自然语言提示？

### 4. 在知识库中的定位

ATT3D 处于 **文本到三维生成** 与 **摊销优化** 的交叉点。其核心贡献在于将“逐样本优化”重构为“跨样本联合训练”，从而将三维生成从计算密集型任务转变为前馈推理任务。这一思路与以下方向形成对话：

- **基于扩散先验的三维生成**：继承 DreamFusion 的 SDS 框架，但将优化过程从单提示扩展至多提示联合训练。
- **超网络与参数生成**：利用超网络实现文本条件到 NeRF 参数的映射，与 GRAF、Pi-GAN 等条件 NeRF 工作共享技术基因，但应用于 SDS 训练范式。
- **组合泛化**：通过摊销训练隐式学习语义组件的分解与组合，与组合式生成模型的研究方向相关。

从方法谱系看，ATT3D 是从“优化式生成”向“前馈式生成”过渡的代表性工作，为后续的快速文本到三维方法（如基于扩散先验的直接三维生成模型）提供了重要的中间范式。

## 原文 PDF

![[paperPDFs/ICCV_2023/ATT3D_Amortized_Text_to_3D_Object_synthesis.pdf]]
