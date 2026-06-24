---
title: Efficient Encoder-Free Fourier-based 3D Large Multimodal Model
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Efficient_Encoder_Free_Fourier_based_3D_Large_Multimodal_Model.pdf
project_link: "https://tev-fbk.github.io/Fase3D"
code_link: null
aliases:
- EEFFB3LMM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过超点（superpoint）标记化、空间填充曲线（SFC）序列化和快速傅里叶变换（FFT）驱动的上下文增强，在不使用视觉编码器的情况下实现全局上下文建模，从而大幅降低参数量和计算开销。
primary_logic: 将三维点云处理视为空间域与频率域之间的合成——在序列化超点上利用FFT进行全局上下文混合，可以近似自注意力，从而构建高效的无编码器三维大型多模态模型。
claims:
- Fase3D 在 ScanQA 和 SQA3D 上的性能与编码器基线 3D-LLaVA 相当，但视觉编码/标记化阶段的激活参数仅为 10.54M（3D-LLaVA 为 58.26M），FLOPs 仅为 2.04G（3D-LLaVA 为 37.75G），效率大幅领先。
- 消融实验表明，基于FFT的上下文增强器单独能将CIDEr提升6.93，与超点池化结合后可提升10.87，验证了FFT在全局上下文建模中的关键作用。
- Fase3D 是第一个针对场景级三维数据的无编码器大型多模态模型，完全移除了专用的三维视觉编码器，直接处理原始点云。
- ScanQA (val) 上 CIDEr ↑ = 90.11 (Fase3D + Qwen2.5-3B)
---

# Efficient Encoder-Free Fourier-based 3D Large Multimodal Model

> [!tip] 核心洞察
> 将三维点云处理视为空间域与频率域之间的合成——在序列化超点上利用FFT进行全局上下文混合，可以近似自注意力，从而构建高效的无编码器三维大型多模态模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 高效的无编码器傅里叶三维大型多模态模型 |
| 英文题名 | Efficient Encoder-Free Fourier-based 3D Large Multimodal Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23153) · [Project](https://tev-fbk.github.io/Fase3D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Fase3D |
| Dataset | ScanQA, SQA3D, ScanRefer, Nr3D |

> [!tip] 效果简介
> - ScanQA (val) 上，CIDEr ↑ 90.11 (Fase3D + Qwen2.5-3B) vs 92.60 (3D-LLaVA + Vicuna-1.5-7B) (-2.49)；BLEU-4 ↑ 17.12 (Fase3D + Qwen2.5-3B) vs 17.10 (3D-LLaVA + Vicuna-1.5-7B) (+0.02)。
> - SQA3D (test) 上，EM@1 ↑ 53.9 (Fase3D + Qwen2.5-3B) vs 54.5 (3D-LLaVA + Vicuna-1.5-7B) (-0.6)。
> - ScanRefer 上，CIDEr@0.5 ↑ 78.14 (Fase3D + Mask3D) vs 78.80 (3D-LLaVA + Mask3D) (-0.66)。

## 概述

现有三维大型多模态模型（3D LMM）普遍依赖计算量庞大的预训练视觉编码器（如稀疏3D U-Net），这不仅限制了输入分辨率和可扩展性，还缺乏直接处理无序、大规模点云的高效标记化方案。**Fase3D** 是首个面向场景级三维数据的无编码器大型多模态模型，其核心洞察在于：将三维点云处理视为空间域与频率域之间的合成——通过在序列化的超点上利用快速傅里叶变换（FFT）进行全局上下文混合，可以近似自注意力机制，从而完全移除专用视觉编码器。

在方法定位上，Fase3D 与 **LL3DA**、**PerLA**、**3D-LLaVA** 等基于编码器的基线形成鲜明对比：它采用超点标记化、空间填充曲线（SFC）序列化和FFT驱动的上下文增强，以极低的参数量和计算开销实现全局上下文建模。视觉编码/标记化阶段的激活参数仅为 **10.54M**（3D-LLaVA 为 58.26M），FLOPs 仅为 **2.04G**（3D-LLaVA 为 37.75G），效率大幅领先。

在 ScanQA 和 SQA3D 等三维问答与密集字幕基准上，Fase3D 以显著更低的计算代价取得了与编码器基线相当的性能。消融实验进一步证实，基于FFT的上下文增强器单独能将 CIDEr 提升 **6.93**，与超点池化结合后提升可达 **10.87**，验证了频域全局建模的关键作用。当前方法主要在 ScanNet 数据集上验证，尚未扩展到更广泛的多模态输入或更大规模三维语料库，这些方向仍有待探索。

## 背景与动机

### 三维场景理解的多模态大模型需求

三维场景理解在具身智能、增强现实和人机交互等领域扮演着关键角色。与二维视觉相比，三维数据以无序、稀疏的点云形式呈现，天然缺乏规则的网格结构，这给视觉-语言对齐带来了根本性挑战。近年来，大型多模态模型（LMM）在二维视觉-语言任务上取得了显著进展，研究者开始将这一范式迁移到三维领域，构建能够对三维场景进行问答、密集字幕生成和视觉定位的三维大型多模态模型（3D LMM）。

### 现有方法的瓶颈：沉重的视觉编码器

当前主流的 3D LMM——如 **LL3DA**、**PerLA** 和 **3D-LLaVA**——均沿袭了二维 LMM 的架构范式：首先使用一个预训练的视觉编码器（通常是稀疏 3D U-Net 或 PointBERT 等点云编码器）提取场景的几何特征，再通过 Q-Former 或类似的投影层将视觉特征对齐到大语言模型（LLM）的输入空间。这一范式存在两个根本性效率瓶颈：

1. **编码器计算开销巨大**：以 3D-LLaVA 为例，其视觉编码/标记化阶段激活参数高达 58.26M，FLOPs 达 37.75G（见 Table 1）。这些计算量主要消耗在编码器的 3D 卷积或自注意力操作上，严重限制了可处理的点云分辨率和模型的可扩展性。

2. **缺乏直接处理无序点云的高效标记化方案**：点云天然是无序集合，而 LLM 要求输入为有序序列。现有方法要么依赖编码器隐式地完成这一转换，要么采用简单的下采样策略，缺乏一种既能保留空间结构、又能以极低计算成本完成序列化的专用标记化机制。

### 核心动机：走向无编码器的三维多模态模型

上述瓶颈引出了一个关键问题：**是否可以在完全移除专用三维视觉编码器的情况下，直接对原始点云进行高效标记化，并仍能实现与编码器方法相当的性能？**

这一动机源于一个更深层的洞察：将三维点云处理视为空间域与频率域之间的合成。具体而言，在序列化后的点云标记上利用快速傅里叶变换（FFT）进行全局上下文混合，可以在数学上近似自注意力机制的全对全交互——自注意力本质上可被理解为一种低通滤波操作——却无需承担自注意力的二次计算复杂度。这意味着，通过精心设计的频域操作，可以用极轻量的计算代价实现原本需要沉重编码器才能完成的全局上下文建模。

### Fase3D 的定位

基于上述动机，本文提出 **Fase3D**——首个面向场景级三维数据的无编码器大型多模态模型。Fase3D 完全移除了传统的三维视觉编码器，转而采用一套基于傅里叶变换的轻量级标记化流水线：通过超点（superpoint）标记化将点云压缩为紧凑的标记集合，利用空间填充曲线（SFC）序列化赋予无序点云以空间一致性的一维结构，再通过 FFT 驱动的上下文增强器实现高效的全局特征混合。这一设计使得 Fase3D 的视觉标记化阶段仅需 10.54M 激活参数和 2.04G FLOPs，效率较编码器基线提升超过一个数量级，同时在下游任务上保持了具有竞争力的性能。

## 核心创新

Fase3D 的核心创新在于**完全移除三维视觉编码器**，将点云处理重新定义为空间域与频率域之间的合成问题。与主流三维大型多模态模型（3D LMM）依赖计算量大的预训练编码器（如稀疏 3D U-Net 或 PointBERT）不同，Fase3D 通过三个紧密耦合的 changed slots 实现了高效的无编码器架构，在保持与编码器基线相当性能的同时，将视觉标记化阶段的激活参数量削减至 **10.54M**（对比 3D-LLaVA 的 58.26M），FLOPs 降至 **2.04G**（对比 3D-LLaVA 的 37.75G）（Table 1）。

### 从视觉编码器到无编码器标记化

传统 3D LMM（如 **LL3DA**、**PerLA**、**3D-LLaVA**）的视觉前端依赖预训练的三维编码器提取几何特征，再通过 Q-Former 或类似模块与 LLM 对齐。这种设计不仅引入了大量参数和计算开销，还限制了输入分辨率与可扩展性。Fase3D 的 **changed slot** 在于：用轻量级 MLP 和超点平均池化（Superpoint Pooling）直接生成初始标记，完全绕过了专用视觉编码器（§3.1）。消融实验表明，仅超点池化一项即可将标记序列缩短约一个数量级，并独立提升 CIDEr **3.66**（Table 3），验证了无编码器设计的可行性。

### 从局部聚合到傅里叶全局上下文建模

移除编码器后面临的核心挑战是如何为无序点云提供全局上下文——这正是编码器所擅长的。Fase3D 的第二个 **changed slot** 在于：将超点按空间填充曲线（SFC，如希尔伯特曲线、Z-order 曲线）序列化为一维序列，在重叠窗口内应用快速傅里叶变换（FFT）和可学习的频域门控 $\mathbf{G}_v$，实现全局上下文混合（§3.2）。其核心操作为：

$$\mathbf{S}'(\pi_i) = \mathcal{F}^{-1}(\mathcal{F}(\mathbf{S}(\pi_i)) \odot \mathbf{G}_v)$$

这一设计的关键洞察是：**在序列化超点上利用 FFT 进行频谱混合，可以近似自注意力机制**，但计算复杂度远低于显式注意力。消融实验提供了决定性证据：FFT 上下文增强器单独贡献 CIDEr 提升 **6.93**，与超点池化结合后总提升达 **10.87**（Table 3），证明 FFT 是全局建模的核心驱动力。

### 从标准适配到傅里叶增强的 LLM 适配

Fase3D 的第三个 **changed slot** 在于 LLM 适配层的设计。传统方法通常使用标准 LoRA 进行微调，而 Fase3D 提出了**傅里叶增强 LoRA**——在 LLM 的 FFN 层之前插入轻量级全局滤波器模块（Global Filter Module, GFM），通过 FFT/iFFT 在通道维进行频谱混合，生成全局感知特征后再由 LoRA 适配（§3.5）。消融表明，将 LoRA 与 FFT 残差结合（dLoRA+FFT vision），相比纯 LoRA 提升 CIDEr **4.38**、BLEU-4 **1.61**（Table 4），验证了频域全局信息注入对 LLM 理解三维场景的有效性。

### 创新边界与待验证方向

值得注意的是，Fase3D 的创新存在明确的边界条件。首先，所有实验仅在 ScanNet v2 数据集上验证，尚未在更广泛的三维场景语料库上检验泛化能力。其次，当前的空间填充曲线序列化策略为手工选择（希尔伯特、Z-order 等），缺乏自适应或可学习的序列化机制，可能对某些场景并非最优。此外，Fase3D 尚未与 RGB 图像等多模态输入融合，限制了在纹理丰富场景中进一步提升性能的潜力。这些边界为后续研究提供了清晰的改进方向：自适应序列化策略、多模态傅里叶增强、以及更大规模三维预训练。

## 整体框架

Fase3D 提出了一套**完全移除专用三维视觉编码器**的流水线，直接以原始点云作为输入，通过四个核心模块将其转化为紧凑的三维标记序列，最终由冻结的大语言模型（LLM）完成三维场景理解与推理。图 2 展示了从点云到语言输出的完整数据流。

### 流水线概览

1. **超点生成与标记初始化**（§3.1）：对输入点云进行几何聚类，将其划分为 $M$ 个超点（superpoints），利用浅层 MLP 提取点级局部特征，再通过超点内平均池化得到超点级标记 $\mathbf{S} \in \mathbb{R}^{M \times d}$。这一步骤将原始无序点云压缩为数量可控的初始语义单元。

2. **FFT 上下文增强器**（§3.2）：将超点标记沿多条空间填充曲线（SFC，如希尔伯特曲线）序列化为一维序列，在重叠窗口内应用快速傅里叶变换（FFT）、可学习频域门控 $\mathbf{G}_v$ 和逆变换，实现局部与全局上下文的高效混合。多曲线结果通过均匀平均融合，得到增强标记 $\tilde{\mathbf{S}}$。

3. **基于图的标记合并**（§3.3）：在增强后的超点标记上构建稀疏邻接图，结合 SFC 窗口投票与最远点采样（FPS）进行自适应图池化，将 $M$ 个超点标记进一步压缩为 $T$ 个紧凑的三维标记（$T < M$），作为 LLM 的视觉输入。

4. **傅里叶增强 LoRA 适配与 LLM 推理**（§3.4–3.6）：将压缩后的三维标记与文本提示、可选的坐标提示（通过 k-NN 和傅里叶位置编码嵌入）拼接后送入冻结的 LLM。在 LLM 的前馈网络层之前插入全局滤波器模块（GFM），利用 FFT 在通道维进行频谱混合，再由 LoRA 层适配，使 LLM 获得全局频率感知的上下文表示。

### 关键设计理念

整个流水线的核心洞察在于：**将三维点云处理重新表述为空间域与频率域之间的合成**。传统三维 LMM 依赖预训练的 3D U-Net 或 PointBERT 等重编码器（激活参数量通常超过 50M），而 Fase3D 的标记化阶段仅使用 10.54M 激活参数和 2.04G FLOPs（对比 3D-LLaVA 的 58.26M 和 37.75G，见 Table 1），效率提升约 18.5 倍。这一效率优势源于两个关键替代：

- **用 FFT 频域混合近似自注意力**：序列化超点上的 FFT 操作本质上实现了全局感受野的信息交换，避免了自注意力的二次复杂度。
- **用超点池化替代可学习查询压缩**：基于几何先验的超点划分和平均池化，以极低计算成本完成了标记压缩，消融实验表明该操作单独贡献 CIDEr +3.66（Table 3）。

> **注意**：当前流水线仅在 ScanNet v2 数据集（1,201 训练场景 / 312 验证场景）上验证，尚未在更广泛的三维场景语料库上测试泛化能力。空间填充曲线的选择（希尔伯特、Z-order 等）为手工指定，缺乏自适应机制。

### 补充图表

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/001_Figure_1.jpg]]
*Figure 1: Fase3D’s contribution overview. Mainstream 3D LMMs are based on computationally-heavy scene encoders to extract geometric features before alignment with the LLM. In contrast, our method (Fase3D) employs a lightweight Fourier-based tokenizer to process raw point clouds directly and introduces Fourier-augmented LoRA adapters, which infuse global frequency-aware context into the LLM without additional computational overhead*

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/002_Figure_2.jpg]]
*Figure 2: The Fase3D pipeline. A lightweight tokenizer (•) produces M superpoint tokens, which are refined by an FFT-based context enhancer (•). A graph is then constructed, and a token-merging block (•) compresses the tokens into*

## 核心模块与公式推导

Fase3D 的核心设计理念是将三维点云处理建模为空间域与频率域之间的合成——在序列化的超点上利用 FFT 进行全局上下文混合，从而近似自注意力，构建无视觉编码器的高效三维大型多模态模型。其流水线包含五个关键模块。

### 3.1 超点生成与标记初始化

给定原始点云，首先使用轻量级 MLP 提取逐点局部特征，并通过几何聚类将点云划分为 $M$ 个超点（superpoints）。每个点的初始标记由特征嵌入与傅里叶坐标嵌入相加得到，随后在超点内进行平均池化，得到超点级标记：

$$
\mathbf{S} = \mathrm{SptPool}(\mathbf{X}^{(0)}, \mathcal{Q}) \in \mathbb{R}^{M \times d}
\tag{1}
$$

其中 $\mathbf{X}^{(0)}$ 为点级标记，$\mathcal{Q}$ 为超点划分，$d$ 为特征维度。该池化操作将标记序列缩短约一个数量级，消融实验表明其单独贡献 CIDEr 提升 3.66（§4.3, Table 3）。

### 3.2 FFT 上下文增强器

超点标记本质上是无序的，缺乏全局上下文。Fase3D 引入空间填充曲线（SFC）将超点序列化为一维序列，然后在频域进行上下文混合。具体而言，对按 SFC 遍历 $\pi_i$ 排序的标记序列应用 FFT，乘以可学习的频域门控 $\mathbf{G}_v$，再逆变换回时空域：

$$
\mathbf{S}'(\pi_i) = \mathcal{F}^{-1}\big(\mathcal{F}(\mathbf{S}(\pi_i)) \odot \mathbf{G}_v\big)
\tag{2}
$$

该操作在长度为 128、步长为 64 的重叠窗口上执行，并通过平方 Hann 权重的叠加-相加（overlap-add）重建完整序列。所有空间填充曲线遍历得到的增强特征通过均匀平均融合：

$$
\tilde{\mathbf{S}} = \frac{1}{|\pi|} \sum_{\pi_i} \mathbf{S}'(\pi_i)
\tag{3}
$$

FFT 增强器单独贡献 CIDEr 提升 6.93，与超点池化结合后总提升达 10.87（§4.3, Table 3），验证了频域全局上下文建模的关键作用。

### 3.3 基于图的标记合并

为控制送入 LLM 的标记数量，Fase3D 构建基于 SFC 窗口投票的稀疏超点图，并利用图池化将 $M$ 个超点标记压缩至 $T$ 个紧凑标记（$T < M$）。池化过程结合最远点采样（FPS）和局部邻域聚合，归一化池化权重为：

$$
w_{it} = \frac{\tilde{w}_{it}}{\sum_{j \in \mathcal{N}_t} \tilde{w}_{jt} + \epsilon}
$$

其中 $\mathcal{N}_t$ 为标记 $t$ 的邻域超点集合。消融表明将 LLM 输入标记数设为 256 可实现最佳计算-质量权衡（Supp. Table C）。

### 3.4 提示嵌入

为实现坐标感知推理，模型引入三维坐标标记，通过 k-NN 和傅里叶位置编码将空间坐标（或实例中心）嵌入到提示序列中，使 LLM 能直接理解三维空间关系。

### 3.5 傅里叶增强 LoRA 适配器

在 LLM 的 FFN 层之前插入全局滤波器模块（GFM），通过 FFT 在通道维进行频谱混合：

$$
\mathbf{z}_{\mathrm{mixed}} = \mathrm{iFFT}\big(\mathrm{FFT}(\mathbf{z}) \odot \mathbf{G}_t\big)
$$

其中 $\mathbf{G}_t$ 为可学习的频域滤波器。混合后的特征再经 LoRA 层适配。消融实验表明，该傅里叶残差设计相比纯 LoRA 提升 CIDEr 4.38、BLEU-4 1.61（§4.3, Table 4）。

### 3.6 训练目标

模型采用标准的下一个 token 交叉熵损失进行语言建模：

$$
\mathcal{L}_{\mathrm{LM}} = -\frac{1}{\sum_t m_t} \sum_t m_t \log p_{\theta}(w_t \mid w_{<t}, \mathbf{Z}')
\tag{4}
$$

其中 $m_t$ 用于屏蔽非回答部分的前缀和提示 token，仅对有效回答部分计算损失。

### 补充图表

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/013_Figure.jpg]]
*Figure: A. Visualization of our SFC-based kNN graph construction via window voting. We show two representative examples of curveguided neighbor selection*

## 实验与分析

### 主要结果

Fase3D 在三维问答（3D QA）和密集字幕（dense captioning）两项核心任务上，以显著更低的视觉编码开销实现了与编码器基线相当的性能。

**三维问答（ScanQA 与 SQA3D）**。Table 1 汇总了 ScanQA 和 SQA3D 上的结果。Fase3D 搭配 Qwen2.5-3B 在 ScanQA 验证集上取得 CIDEr 90.11、BLEU-4 17.12，与最强的编码器方法 **3D-LLaVA**（Vicuna-1.5-7B）的 92.60 / 17.10 基本持平（CIDEr Δ = -2.49，BLEU-4 Δ = +0.02）。在 SQA3D 测试集上，Fase3D 的 EM@1 为 53.9，仅比 3D-LLaVA 的 54.5 低 0.6 个百分点。更关键的是效率维度：Fase3D 在编码/标记化阶段的激活参数量仅 **10.54M**，FLOPs 仅 **2.04G**，而 3D-LLaVA 对应为 58.26M 参数和 37.75G FLOPs——参数量减少约 5.5 倍，计算量减少约 18.5 倍。这一效率优势来源于完全移除三维视觉编码器，代之以超点池化和 FFT 上下文增强的轻量标记化流水线。

**密集字幕（ScanRefer 与 Nr3D）**。Table 2 展示了密集字幕任务的结果。当使用外部实例分割器 Mask3D 提供区域提议时，Fase3D 在 ScanRefer 上取得 CIDEr@0.5 78.14，与 3D-LLaVA 的 78.80 差距仅 0.66；在 Nr3D 上取得 54.91，与 **PerLA** 的 55.06 差距仅 0.15。当使用谱聚类（spectral clustering）替代 Mask3D 时，Fase3D 仍保持有竞争力的性能，进一步验证了无编码器设计在多种提议策略下的鲁棒性。

### 消融实验

消融研究系统验证了 Fase3D 各模块的独立贡献，所有实验在相同 ScanNet v2 数据划分和优化超参数下进行。

**视觉嵌入模块消融**（Table 3）。以原始下采样点标记（Point）为基线（CIDEr 76.04），超点池化（Superpoint）单独将 CIDEr 提升 **3.66**（至 79.70），同时将标记序列缩短约一个数量级。FFT 上下文增强器（FFT）单独贡献 CIDEr 提升 **6.93**（至 82.97），是单模块中增益最大的组件。两者结合（Superpoint + FFT）产生最强的协同效应，CIDEr 提升 **10.87**（至 86.91）。这直接验证了核心洞察：超点池化提供紧凑的初始表示，FFT 在频域进行全局上下文混合，二者互补构成高效标记化的关键。

**LoRA 放置与傅里叶残差消融**（Table 4）。在 LLM 适配层面，将傅里叶残差模块（GFM）与 LoRA 结合（dLoRA + FFT vision）相比纯 LoRA（dLoRA）提升 CIDEr **4.38**、BLEU-4 **1.61**，表明在频域对 LLM 中间特征进行全局混频能有效注入三维空间上下文，且不增加额外推理开销。

**空间填充曲线数量**（Supp. Table B）。使用 4 条空间填充曲线（n_C=4）在准确度和计算成本之间取得良好平衡；继续增加曲线数量带来的性能增益有限，表明多曲线融合已充分覆盖必要的空间遍历模式。

**LLM 输入标记数**（Supp. Table C）。将输入 LLM 的压缩标记数设置为 256 可实现最佳的计算-质量权衡，标记过少会丢失空间细节，过多则增加计算开销而收益递减。

### 不同 LLM 骨干的泛化性

Table 5 对比了不同 LLM 骨干下的性能。Fase3D 在 OPT-1.3B 和 Qwen2.5-3B 上均表现稳定，且无编码器变体在效率上持续大幅领先编码器变体。当 Fase3D 使用与 3D-LLaVA 相同的 Vicuna-1.5-7B 时，性能差距进一步缩小，提供了公平的架构对比参考。

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/009_Table_5.jpg]]
*Table 5: Question answering results with different LLMs on ScanQA [2]. #Param/FLOP(G) denote the activated parameters and encoding/tokenization FLOPs. Best results in bold*

### 失败模式与局限性

尽管 Fase3D 在效率和性能之间取得了有竞争力的平衡，但存在以下已知局限：

1. **数据域限制**：当前模型仅在 ScanNet v2（1,201 训练 / 312 验证场景）上训练和评估，尚未在更广泛、更多样的三维场景语料库（如室外场景、大规模跨域数据）上验证泛化能力。在分布外场景下的性能需要进一步实证检验。
2. **手工序列化策略**：空间填充曲线（希尔伯特、Z-order 等）为手工选择，对特定场景几何可能并非最优。缺乏自适应或可学习的序列化机制，限制了在复杂几何结构下的上下文建模灵活性。
3. **多模态融合缺失**：当前设计仅处理点云几何信息，尚未与 RGB 图像等多模态输入融合。在纹理丰富场景中，颜色和外观线索的缺失可能限制性能上限。
4. **标记合并的通用性**：基于图的标记合并策略目前主要服务于密集字幕和问答任务，其在更高级的实例分割或开放词汇对象发现任务上的适用性尚未验证。

### 重要图表结论

- **Table 1**：Fase3D 在 ScanQA 和 SQA3D 上以约 1/5 的参数量和约 1/18 的计算量，实现了与编码器基线 3D-LLaVA 相当的性能，验证了无编码器傅里叶架构的效率优势。
- **Table 3**：FFT 上下文增强器是单模块中贡献最大的组件（+6.93 CIDEr），与超点池化结合后产生最强的协同增益（+10.87 CIDEr），直接支撑了“频域全局混合可近似自注意力”的核心主张。
- **Table 4**：傅里叶增强 LoRA（GFM）在 LLM 内部进行频域混频，以零额外推理开销显著提升性能，为轻量级多模态适配提供了新范式。
- **Table 2**：Fase3D 在密集字幕任务上同样接近编码器方法，且兼容多种提议策略，表明无编码器标记化保留了足够的空间定位能力。

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/003_Table_1.jpg]]
*Table 1: Question answering results on ScanQA [2] and SQA3D [33]. #Param/FLOP: number of activated parameters and Floating Point Operation count required for the encoding/tokenization stage. Best result is in bold. Second best result is underlined*

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/005_Table_2.jpg]]
*Table 2: Dense captioning results on ScanRefer and Nr3D. #Param/FLOP: number of activated parameters and Floating Point Operation count required for the encoding/tokenization stage. Best result in bold. Second best result is underlined*

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/006_Table_3.jpg]]
*Table 3: Ablation study of vision embedding modules. Point (downsampled raw point tokens), Superpoint (superpoint pooling), FFT (lightweight FFT-based context enhancer)*

### 补充图表

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results and comparisons between Fase3D, PerLA [35], and LL3DA [6] on the ScanQA [2] dataset*

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/008_Table.jpg]]

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/010_Table.jpg]]
*Table: B. Effect of the number of SFC curves $n _ { C }$ in multi-curve serialization on ScanQA (val). Table C. Ablation study on the number of LLM’s input tokens. Table D. Effect of two-stage training on ScanQA validation*

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/011_Table.jpg]]
*Table: A. Ablation study on the number of LLM’s LoRA layers*

![[assets/figures/papers/paper_list_l2233_https_arxiv_org_abs_2602_23153/figures/012_Table.jpg]]
*Table: E. Effect of different token selection / merging strategies on ScanQA validation performance. All models are trained from scratch on the ScanQA training split, without any pre-training*

## 方法谱系与知识库定位

### 1. 与编码器基线的结构差异与效率优势

Fase3D 的核心决策是**完全移除专用的三维视觉编码器**（如 3D U-Net、PointBERT 等），将点云处理从“重编码器 + 轻对齐”范式转变为“轻标记化 + 频域上下文增强”范式。这一决策直接针对现有 3D LMM 的根本瓶颈：预训练编码器不仅参数量大、计算开销高，还限制了输入分辨率和可扩展性。

与代表性编码器基线相比，Fase3D 的视觉编码/标记化阶段在效率上形成数量级优势：

- **3D-LLaVA**（点云输入，Vicuna-1.5-7B）：激活参数 58.26M，FLOPs 37.75G（Table 1）。
- **Fase3D**（Qwen2.5-3B）：激活参数仅 10.54M，FLOPs 仅 2.04G（Table 1）。

在参数减少约 **5.5 倍**、计算量减少约 **18.5 倍**的前提下，Fase3D 在 ScanQA 上 CIDEr 仅落后 2.49（90.11 vs 92.60），在 SQA3D 上 EM@1 仅落后 0.6（53.9 vs 54.5）。这一结果说明，**频域全局上下文混合可以在不依赖昂贵编码器的情况下，近似甚至替代自注意力机制的空间感知功能**。

### 2. 与同类无编码器/轻量标记化工作的关系

Fase3D 自称是**首个针对场景级三维数据的无编码器 LMM**（Abstract, §1）。在二维领域，无编码器方法（如直接使用 ViT patch embedding 或 MLP mixer）已有探索，但三维场景的无序性、稀疏性和大规模特性使得直接迁移二维方案不可行。

Fase3D 的三项关键设计构成了其独特的方法定位：

| 设计要素 | Fase3D 方案 | 基线/常见方案 | 创新程度 |
|---------|------------|-------------|---------|
| 视觉编码器 | 无专用编码器，仅轻量 MLP + 超点平均池化 | 预训练 3D U-Net 或 PointBERT（3D-LLaVA 等） | 高 |
| 全局上下文 | FFT 频域门控 + 空间填充曲线序列化 | 编码器全局特征聚合或 Q-Former 交叉注意力 | 高 |
| 标记压缩 | 基于稀疏超点图的自适应图池化（SFC 投票 + FPS） | 可学习查询向量（Q-Former 或 Mask3D 提议） | 中 |
| LLM 适配 | 傅里叶增强 LoRA（Global Filter Module） | 标准 LoRA 或全微调 | 中 |

其中，**FFT 驱动的上下文增强器**是最关键的差异化贡献。消融实验（§4.3, Table 3）表明，该模块单独贡献 CIDEr 提升 6.93（从 76.04 到 82.97），与超点池化结合后总提升达 10.87（到 86.91），验证了频域混合在替代自注意力方面的有效性。

### 3. 适用边界与已知局限

基于论文提供的证据和实验设置，Fase3D 的适用边界可归纳如下：

**已验证的有效范围：**
- **数据集**：仅在 ScanNet v2（1,201 训练 / 312 验证场景）上训练和评估。
- **任务类型**：三维问答（ScanQA, SQA3D）、密集字幕（ScanRefer, Nr3D）。
- **LLM 骨干**：Qwen2.5-3B 和 OPT-1.3B 均验证有效（Table 5），Vicuna-1.5-7B 也有报告结果。
- **输入模态**：纯点云（XYZ + RGB 颜色），尚未融合 RGB 图像。

**已知局限（论文明确或隐含）：**
1. **数据集泛化未验证**：仅在 ScanNet 室内场景上测试，尚未在更大规模、更多样（如室外混合场景）的三维语料库上验证泛化能力。
2. **序列化策略为手工设计**：空间填充曲线（希尔伯特、Z-order 等）为固定选择，可能对某些场景几何并非最优。补充实验（Supp. Table B）显示使用 4 条曲线（n_C=4）即可获得良好平衡，但缺乏自适应或可学习的序列化机制。
3. **多模态融合缺失**：当前未与 RGB 图像等多模态输入融合，限制了在纹理丰富场景中进一步提升性能的潜力。
4. **LLM 输入标记数有上限**：消融实验（Supp. Table C）表明 256 个标记为最佳计算-质量权衡点，更多标记可能带来边际收益但增加计算开销。

### 4. 开放问题与未来方向

基于论文的方法设计和局限分析，以下开放问题值得关注：

1. **更大规模预训练的泛化能力**：在更大且更多样的三维数据集（如室内外混合场景）上进行预训练，能否显著提升 Fase3D 在跨场景、跨任务上的泛化性能？当前仅 ScanNet 的训练规模可能限制了其上限。

2. **自适应序列化策略**：是否可以设计基于学习或基于内容的排序机制来取代固定的空间填充曲线？例如，通过可微排序网络或基于图拉普拉斯的谱排序来优化序列化质量，可能进一步提升 FFT 上下文混合的效果。

3. **多模态傅里叶增强**：如何将 FFT 增强器和 Global Filter Module 扩展到同时处理点云和 RGB 图像的多模态输入？频域混合在跨模态特征对齐中是否同样有效，是一个开放问题。

4. **标记合并的下游扩展**：当前基于图的标记合并策略主要服务于 LMM 输入压缩，是否能够支持更高级的感知任务（如实例分割、开放词汇对象发现）？这需要验证合并后的标记是否保留了足够的实例级判别信息。

5. **与更大 LLM 的扩展性**：当前实验主要基于 3B 和 1.3B 规模的 LLM，Fase3D 的轻量标记化设计在更大 LLM（如 7B、13B）上的性能增益和效率优势是否保持，需要进一步验证。论文虽报告了 Vicuna-1.5-7B 的结果，但未提供完整的效率对比数据。

## 原文 PDF

![[paperPDFs/CVPR_2026/Efficient_Encoder_Free_Fourier_based_3D_Large_Multimodal_Model.pdf]]