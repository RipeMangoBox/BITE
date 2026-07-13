---
title: "FunPhase: A Periodic Functional Autoencoder for Motion Generation via Phase Manifolds"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Phase_Manifolds.pdf
project_link: null
code_link: null
aliases:
- FunPhase
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在潜在空间中引入显式的周期分解，并将解码器由离散帧重建替换为连续时空函数求值（函数空间解码），使模型获得骨架无关的任意分辨率重建能力，同时周期性潜在码可直接适配标准扩散模型进行生成。
primary_logic: 将相位周期性先验嵌入函数自编码器，能够在保持运动相位流形可解释性的前提下，实现连续、平滑的时空重建，并统一了运动预测与生成任务。
claims:
- FunPhase在重构任务中显著优于DeepPhase，例如在DOG数据集上位姿误差降低超过57%
- 将周期性分解加入扩散模型极大地改善了生成质量，FID从Function Diffusion的1.19降至0.51
- FunPhase在物理合理性指标（如足部滑动）上明显优于所有对比方法
- 删除前向运动学损失（FK loss）会导致重构误差急剧上升（关节位置误差从3.15升至26.8），证明该物理先验不可或缺
---

# FunPhase: A Periodic Functional Autoencoder for Motion Generation via Phase Manifolds

> [!tip] 核心洞察
> 将相位周期性先验嵌入函数自编码器，能够在保持运动相位流形可解释性的前提下，实现连续、平滑的时空重建，并统一了运动预测与生成任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | FunPhase：一种面向运动生成的相位流形周期性函数自编码器 |
| 英文题名 | FunPhase: A Periodic Functional Autoencoder for Motion Generation via Phase Manifolds |
| 会议/期刊 | arXiv 2025 |
| Links |  [paper](https://arxiv.org/abs/2512.09423)|
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FunPhase |
| Dataset | DOG, 100STYLE |

> [!tip] 效果简介
> - DOG 上，Position (cm)↓ 61.4 (FunPhase-16C) vs 144 (DeepPhase-16C) (-57.4%)。
> - 100STYLE 上，Position (cm)↓ 0.36 (FunPhase-256C) vs 92.9 (DeepPhase-32C) (-99.6%)；FID↓ 0.51±0.16 (FunPhase) vs 0.91±0.62 (CAMDM) (-44.0%)；Foot Sliding↓ 0.52 (FunPhase) vs 0.69 (CAMDM) (-24.6%)。

## 概要

**核心问题**：现有基于相位的运动表示方法（如DeepPhase）依赖固定骨架的离散帧卷积编解码，难以扩展到不同骨架拓扑和任意时间分辨率，且无法融入概率生成框架。

**核心方法**：FunPhase是一种周期性函数自编码器，将相位先验嵌入连续函数空间。它通过Perceiver交叉注意力编码器提取潜在令牌，经FFT分解为振幅、频率、相位偏移和偏置四个周期参数，再由函数解码器在任意时空坐标处求值重建运动。该设计使模型获得骨架无关的任意分辨率重建能力，同时周期性潜在码可直接适配标准扩散模型进行条件生成。

**核心结论**：
- **重建质量大幅领先**：在DOG数据集上，FunPhase-16C的位姿误差（Position 61.4 cm）相比DeepPhase-16C（144 cm）降低超过57%（Table 1）。
- **生成质量显著提升**：将周期性分解加入扩散模型后，FID从Function Diffusion的1.19降至0.51，且物理合理性指标（如足部滑动0.52）优于CAMDM（0.69）等基线（Table 2）。
- **物理先验不可或缺**：移除前向运动学损失（FK loss）导致关节位置误差从3.15急剧上升至26.8，证明该物理正则化对重建保真度至关重要（Table 4）。

**方法定位**：FunPhase在保持相位流形可解释性的前提下，统一了运动重建、预测与生成任务，为骨架无关的连续运动建模提供了新的基线。



### 运动生成中的相位表示与函数空间

在角色动画与运动合成领域，如何获得紧凑、可解释且物理合理的运动表示是一个核心挑战。运动本质上是高维时空序列，其内在的周期性结构——如行走、奔跑等步态循环——为压缩表示提供了天然先验。**DeepPhase** 率先提出从运动数据中直接学习多维相位变量：通过编码器将运动映射到潜在空间，再经由频域归纳偏置（FFT 后接正弦参数化）将每个潜在通道分解为振幅 $a_c$、频率 $f_c$、相位偏移 $s_c$ 和偏置 $b_c$ 四个参数：

$$\hat{l_c} = a_c \cdot \sin(2\pi(f_c \cdot \mathcal{T} - s_c)) + b_c$$

这一相位流形（phase manifold）表示不仅具备良好的可解释性，还在运动控制器、风格迁移等任务中展现了实用价值。

然而，DeepPhase 存在两个结构性瓶颈，限制了其向现代生成框架的扩展：

1.  **离散帧重建与固定骨架依赖**：DeepPhase 的编解码器基于 1D 卷积，在固定帧率的离散帧上操作，且依赖特定的骨架拓扑。这使得模型无法处理不同骨架的运动数据，也无法在任意时间分辨率下采样重建。

2.  **缺乏概率生成能力**：DeepPhase 的相位表示专为确定性重建和控制任务设计，无法直接融入扩散模型等概率生成框架，难以支持运动预测与多样化生成任务。

与此同时，另一条技术路线——**函数生成框架**（functional generative framework）——将运动建模为连续时空函数，通过在任意坐标处求值来实现骨架无关的生成。但这类方法完全摒弃了相位周期性先验，导致潜在空间缺乏可解释的结构，生成质量与物理合理性仍有提升空间。

### 核心动机

本文的核心动机在于**弥合结构化运动学建模与现代生成方法之间的鸿沟**。具体而言，我们希望回答：能否在保留相位流形可解释性的前提下，将运动重建形式从离散帧卷积升级为连续时空函数求值，从而使模型同时获得骨架无关的任意分辨率重建能力，并能够无缝适配标准扩散模型进行条件生成？

**FunPhase** 正是基于这一动机设计：它将相位周期性先验嵌入函数自编码器，在潜在空间中显式进行周期分解，同时将解码器替换为基于 Perceiver 交叉注意力的连续函数求值模块。这一设计使得模型既能学习结构化、可解释的相位流形，又能实现平滑连续的时空重建，并统一运动预测与生成任务。



## 核心方法与创新机理

FunPhase 的核心创新在于将**显式相位周期性先验**嵌入**连续函数自编码器**框架，从而同时解决了两个长期瓶颈：① 传统相位方法（如 DeepPhase）依赖固定骨架的离散帧卷积编解码，无法处理不同骨架拓扑或任意时间分辨率；② 纯函数生成框架缺乏可解释的周期结构，难以捕捉运动的节律性本质。通过将解码器从离散帧重建替换为**连续时空函数求值**，并在潜在空间中保留**FFT 周期分解**，FunPhase 在保持相位流形可解释性的前提下，获得了骨架无关的任意分辨率重建能力，且其周期性潜在码可直接适配标准扩散模型进行生成。

### 关键改进槽位（Changed Slots）

**1. 运动重建形式：从离散反卷积到连续函数求值**

DeepPhase 等基线采用 1D 反卷积在固定帧率下逐帧重建运动，这使其输出严格受限于训练时的采样率与骨架结构。FunPhase 将解码器替换为基于 Perceiver 交叉注意力的**函数求值模块**：解码器接收任意时空坐标 $(t, j)$ 作为查询，通过交叉注意力聚合编码器输出的正弦参数化潜在码，直接输出对应时刻与关节的旋转四元数或根位置（见 Figure 2）。这一设计使得模型能够在推理时以任意时间分辨率采样，实现运动超分辨率与关键帧插值，而无需修改网络结构（Section 4.1, Decoder; Figure 4）。

**2. 编码器架构：从固定 1D 卷积到独立 Perceiver 编码器**

FunPhase 摒弃了 DeepPhase 的固定尺寸 1D 卷积编码器，转而采用**独立的 Perceiver 编码器分别处理关节旋转和根位置**。每个编码器使用可学习的潜在令牌（latent tokens）通过交叉注意力从时空输入序列中提取紧凑表示，并分别施加时间位置编码与空间位置编码（Section 4.1, Encoder; Section 7.1）。消融实验证实，分离的根/关节编码器优于统一编码器（关节位置误差 3.15 vs 3.37，Table 4），验证了这一设计选择的有效性。

**3. 骨架处理：从固定拓扑到骨架无关的位置编码**

DeepPhase 隐含依赖固定的骨架拓扑，无法泛化至不同骨架。FunPhase 引入了**骨架无关的空间位置编码**：通过计算骨架图的拉普拉斯特征向量或热扩散探针，为每个关节生成结构感知的位置编码，使模型能够处理不同骨架的运动数据（Section 4.1, Spatial Encoding; Section 7.1）。这一改进使得 FunPhase 可在 ZOO 等多骨架数据集上进行统一的训练与生成（Table 3）。

**4. 潜在空间结构：从卷积输出 FFT 到 Perceiver 令牌周期分解**

DeepPhase 对 1D 卷积编码器的输出应用 FFT 以提取周期参数，但其潜在表示仍受限于卷积架构的表达能力。FunPhase 在 **Perceiver 潜在令牌上直接应用 FFT 周期分解**，将每个潜在通道参数化为四元组 $\theta_c = [s_c, a_c, f_c, b_c] \in \mathbb{R}^4$（相位偏移、振幅、频率、偏置），实现更紧凑的 $4C$ 参数表示（Section 4.1, Phase Decomposition; Equation 1）。这一设计在保持周期结构的同时，得益于 Perceiver 的灵活编码能力，获得了更强的表示能力。

**5. 生成框架：从无概率生成到相位流形扩散生成**

DeepPhase 不具备概率生成能力，仅用于确定性重建或控制。FunPhase 通过**相位变换**（Phase Transformation）将周期参数变换为适合高斯扩散的表示 $\pmb{\theta}_c^{diff} = [\mathbf{a}_c^{\cos}, \mathbf{a}_c^{\sin}, f_c^{probit}, b_c]$（Equation 9），然后在变换后的相位流形上训练**扩散 Transformer（DiT）**，实现条件生成（Section 4.2）。实验表明，将周期性分解加入扩散模型极大地改善了生成质量，FID 从纯函数扩散的 1.19 降至 0.51（Table 2），验证了相位先验对生成任务的关键作用。

### 核心机理总结

这些改进槽位的协同效应体现在：**函数空间解码**赋予了模型连续时空重建与超分辨率能力；**骨架无关编码**使其可泛化至不同拓扑；**Perceiver 架构**提供了灵活的序列编码；而**FFT 周期分解**则在潜在空间中嵌入了运动的节律性归纳偏置。最终，这些设计使得 FunPhase 能够统一运动重建、预测与生成任务——这是此前方法无法实现的。



FunPhase 是一个**周期性函数自编码器**，其核心设计理念是将运动的相位流形可解释性与连续函数空间的重建能力统一在同一个框架内。整个 pipeline 由两条并行的编码-解码通路、一个共享的频域分解模块、以及一个可选的扩散生成模块构成。

### 输入表示与双路编码

模型接收一段固定窗口（60帧/约1秒）的运动序列作为输入。与以往方法将全局关节位置作为统一输入不同，FunPhase 将运动显式解耦为两个互补的表示：

- **关节旋转**（joint rotations）：以旋转矩阵形式表示各关节的局部朝向
- **根位置**（root position）：表示角色在世界空间中的全局位移

这两类信号分别送入**独立的 Perceiver 编码器**（Perceiver-based encoder），而非共享一个编码器。消融实验证实，这种分离设计优于统一编码架构（关节位置误差从3.37降至3.15，Table 4）。

### 时空位置编码

为使模型具备骨架无关和任意时间分辨率的能力，编码器在输入端注入了两类位置编码：

- **时间位置编码**（Temporal Positional Encoding）：将每帧的时间戳映射为傅里叶特征，使模型感知帧在时间轴上的绝对位置，从而支持非均匀采样和超分辨率重建
- **空间位置编码**（Spatial Positional Encoding）：编码骨架拓扑结构，可通过图拉普拉斯特征向量或热扩散探针实现，使模型摆脱对固定骨架拓扑的依赖

这两类编码共同赋予模型“函数求值”的能力——解码时可在任意时空坐标处查询运动状态。

### 潜在空间与周期分解

两个 Perceiver 编码器各自输出一组潜在令牌（latent tokens）。这些令牌随后经过一个**快速傅里叶变换（FFT）层**进行周期分解，将每个潜在通道参数化为四个显式的周期分量：

$$\\pmb{\\theta}_c = [s_c,\\, a_c,\\, f_c,\\, b_c] \\in \\mathbb{R}^4$$

分别对应**相位偏移**（phase shift）$s_c$、**振幅**（amplitude）$a_c$、**频率**（frequency）$f_c$ 和**偏置**（bias）$b_c$。这一参数化使得每个潜在通道被建模为正弦函数：

$$\hat{l}_c = a_c \\cdot \\sin(2\\pi(f_c \\cdot \\mathcal{T} - s_c)) + b_c$$

其中 $\mathcal{T}$ 为归一化时间坐标。这种紧凑的 $4C$ 维表示（$C$ 为通道数）既保留了 DeepPhase 的相位可解释性，又为后续的扩散生成提供了结构化潜空间。

### 函数空间解码

解码阶段，模型对上述正弦参数进行**求值**（evaluate），在用户指定的任意时空坐标处重建运动。解码器同样采用 Perceiver 架构，以交叉注意力机制将查询坐标映射为关节旋转和根位置的预测值。这与 DeepPhase 基于1D反卷积的固定帧率离散重建形成根本性差异——FunPhase 的解码器本质上是一个**连续时空函数**，可在训练窗口内的任意时间点采样，自然支持运动超分辨率、关键帧插值等任务（Figure 4）。

### 损失函数与物理先验

训练损失由四项加权组成：

$$\mathcal{L} = 0.5(\mathcal{L}_{rot} + \mathcal{L}_{root}) + 0.5(\mathcal{L}_{FK} + 0.01\mathcal{L}_{foot})$$

其中：
- $\mathcal{L}_{rot}$：关节旋转的测地线距离损失
- $\mathcal{L}_{root}$：根位置的均方误差
- $\mathcal{L}_{FK}$：**前向运动学损失**，强制预测的关节旋转和根位置通过运动学链传播后与真实关节位置一致
- $\mathcal{L}_{foot}$：足部滑动正则项

前向运动学损失是关键的物理先验：消融实验显示，移除该损失会导致关节位置误差从3.15急剧上升至26.8（Table 4），证明纯运动学约束对保持物理合理性不可或缺。

### 扩散生成模块

在自编码器训练完成后，FunPhase 可在其相位流形上构建**潜在扩散模型**（latent diffusion model）以实现运动生成。具体而言，周期参数 $[s_c, a_c, f_c, b_c]$ 首先经过**相位变换**（Phase Transformation）——将振幅-相位对转换为笛卡尔坐标的正余弦分量，并对频率施加概率变换——得到适配高斯扩散的表示：

$$\pmb{\\theta}_c^{diff} = [\\mathbf{a}_c^{\\cos},\\, \\mathbf{a}_c^{\\sin},\\, f_c^{probit},\\, b_c]$$

随后在此变换空间上训练一个**扩散Transformer（DiT）**，采用 v-参数化（velocity parameterization）目标，以条件信号（如文本描述、关键帧约束）调制去噪过程。这一设计使得原本仅用于确定性重建的相位自编码器，无缝扩展为概率生成框架。

### 整体数据流

总结而言，FunPhase 的完整 pipeline 如下：

1. **输入**：固定窗口的关节旋转序列 + 根位置轨迹
2. **时空编码**：注入时间和空间位置编码
3. **双路编码**：独立的 Perceiver 编码器分别提取关节和根位置的潜在令牌
4. **周期分解**：FFT 层将潜在通道参数化为 $[s, a, f, b]$
5. **函数解码**：Perceiver 解码器在查询坐标处求值正弦参数，输出重建运动
6. **（可选）相位变换 + 扩散生成**：将周期参数变换后训练 DiT，实现条件运动生成

### 补充图表

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Periodic Function Autoencoder (FunPhase) architecture. The figure illustrates the separated processing of joint rotations and root positions through Perceiver-based encoder–decoder modules. The latent space is decomposed by a Fast Fourier Transform (FFT) layer in its periodic components (Phase shift, Amplitude, Frequency, Bias) to achieve an even more compact representation and enforce periodicity. The latent space is then reconstructed with the inverse FFT, and the functions are evaluated at the coordinates given as input to the decoder*



FunPhase 的核心设计围绕一个关键洞察展开：将周期性先验嵌入函数自编码器，使潜在空间同时具备可解释的相位结构与连续时空求值能力。其架构由以下模块构成。

### 时空位置编码

为支持任意时间分辨率和不同骨架拓扑，FunPhase 在编码器输入端引入两类位置编码：

- **时间编码**：将帧时间映射为傅里叶特征，使模型感知连续时间坐标而非离散帧索引。
- **空间编码**：编码骨架拓扑信息，支持两种方案——基于图拉普拉斯特征向量，或基于图热扩散探针。这使得模型具备骨架无关的泛化能力。

### 分离式 Perceiver 编码器

编码器采用独立的 Perceiver 架构分别处理关节旋转和根位置序列，而非使用统一的卷积编码器。每个 Perceiver 通过交叉注意力将可变长度的输入序列压缩为一组固定数量的潜在令牌。分离设计的动机在于：旋转与根位置具有不同的运动学语义和数值范围，独立编码有助于保留各自的结构特性。消融实验证实，分离编码在关节位置误差上优于统一编码（3.15 vs 3.37，Table 4）。

### FFT 周期分解

潜在令牌随后通过快速傅里叶变换（FFT）进行周期分解，将每个潜在通道参数化为四个周期分量：

$$\theta_c = [s_c, a_c, f_c, b_c] \in \mathbb{R}^4$$

其中 $s_c$ 为相位偏移，$a_c$ 为振幅，$f_c$ 为频率，$b_c$ 为偏置。这一分解使潜在空间具有显式的周期性结构，同时将表示压缩到 $4C$ 个参数（$C$ 为通道数）。更大的通道数带来更好的重建性能，Table 4 中 256 通道配置取得最优结果。

### 相位流形构建

从周期参数出发，通过超球面变换构建相位流形 $\mathcal{P}$，丢弃频率和偏置分量，仅保留振幅与相位偏移的耦合表示：

$$\mathcal{P}_{2i-1}^{(t)} = a_i^{(t)} \cdot \sin(2\pi \cdot s_i^{(t)})$$

$$\mathcal{P}_{2i}^{(t)} = a_i^{(t)} \cdot \cos(2\pi \cdot s_i^{(t)})$$

这一构造使得不同运动序列的相位状态在流形上具有可比性，为后续的运动控制与生成提供了结构化的潜在空间。

### 函数空间解码器

解码器将周期参数通过逆 FFT 恢复为潜在函数，并在任意给定的时空坐标处求值以重建运动。具体而言，每个潜在通道按正弦参数化进行函数求值：

$$\hat{l}_c = a_c \cdot \sin(2\pi(f_c \cdot \mathcal{T} - s_c)) + b_c$$

其中 $\mathcal{T}$ 为时间坐标。解码器同样采用 Perceiver 交叉注意力机制，以查询坐标（时间、关节索引）为输入，从潜在函数中提取对应的运动值。这一设计使 FunPhase 摆脱了固定帧率离散重建的限制，支持任意时间分辨率的连续采样（Figure 4）。

### 训练损失函数

FunPhase 的重建损失由四个分量加权组合而成。

**旋转损失**采用测地线距离：

$$\mathcal{L}_{rot} = \frac{1}{TJ} \sum_{t,j} \arccos\left(\frac{\mathrm{tr}(\mathbf{R}_{t,j} \hat{\mathbf{R}}_{t,j}^\top)-1}{2}\right)$$

**根位置损失**使用均方误差：

$$\mathcal{L}_{root} = \|\mathbf{X}^{root} - \hat{\mathbf{X}}^{root}\|_2^2$$

**前向运动学损失**强制关节位置一致性，是关键的物理先验：

$$\mathcal{L}_{FK} = \|\mathrm{FK}(\mathbf{R}, \mathbf{X}^{root}) - \mathrm{FK}(\hat{\mathbf{R}}, \hat{\mathbf{X}}^{root})\|_2^2$$

消融实验表明，移除 $\mathcal{L}_{FK}$ 会导致关节位置误差从 3.15 急剧上升至 26.8（Table 4），证明该物理正则化不可或缺。

**总损失**的加权形式为：

$$\mathcal{L} = 0.5(\mathcal{L}_{rot} + \mathcal{L}_{root}) + 0.5(\mathcal{L}_{FK} + 0.01\mathcal{L}_{foot})$$

其中 $\mathcal{L}_{foot}$ 为足部滑动正则化项，权重 0.01 用于抑制生成运动中的非物理滑动。

### 扩散适配的相位变换

为将周期参数适配到标准高斯扩散框架，FunPhase 对潜在表示进行变换。首先将振幅-相位对从极坐标转换为笛卡尔坐标，然后对频率分量施加 probit 变换以映射到无界空间：

$$\theta_c^{diff} = [\mathbf{a}_c^{\cos}, \mathbf{a}_c^{\sin}, f_c^{probit}, b_c]$$

扩散模型采用 v-参数化训练目标，网络预测逆向扩散过程的瞬时速度场：

$$\mathbf{v}_t = \sqrt{\bar{\alpha}_t}\epsilon - \sqrt{1-\bar{\alpha}_t}\mathbf{z}_0$$

其中 $\bar{\alpha}_t$ 为噪声调度参数，$\epsilon$ 为噪声，$\mathbf{z}_0$ 为干净潜在表示。扩散 Transformer 使用自适应层归一化注入条件信号：

$$\operatorname{AdaLN}(\mathbf{h}, \mathbf{c}) = \gamma(\mathbf{c}) \odot \operatorname{LayerNorm}(\mathbf{h}) + \beta(\mathbf{c})$$

其中 $\mathbf{c}$ 为条件向量（如文本或关键帧），$\gamma$ 和 $\beta$ 为条件相关的缩放与偏移参数。Table 6 显示，相位变换对扩散生成质量有正向贡献，准确率从 34.83 提升至 37.6。

### 补充图表

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/005_Figure_3.jpg]]
*Figure 3: Phase Manifold. The plots show the phase manifolds obtained with DeepPhase and FunPhase, alongside the original motion features. All encoded sequences correspond to a dogrunning motion*

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/015_Figure_7.jpg]]
*Figure 7: Phase Transformation. We plot the distribution of the latent periodic parameterization before and after the phase transformation applied in the latent diffusion model*



## 实验与关键发现

### 核心瓶颈与设计动因

现有基于相位的运动表示方法（如DeepPhase）依赖固定骨架拓扑上的1D卷积编解码，其离散帧重建范式难以扩展到不同骨架、任意时间分辨率，且无法融入概率生成框架。FunPhase通过两个关键“因果旋钮”解决该瓶颈：其一，在潜在空间中引入显式的周期分解（FFT→正弦参数化），将运动压缩为振幅、频率、相位偏移和偏置四元组；其二，将解码器由离散帧重建替换为连续时空函数求值（Perceiver交叉注意力解码），使模型获得骨架无关的任意分辨率重建能力。周期性潜在码经过相位变换后，可直接适配标准扩散Transformer进行条件生成，从而统一运动预测与生成任务。

### 自编码器重建质量

FunPhase在重建任务上显著优于周期性自编码器基线DeepPhase。在DOG数据集上，FunPhase-16C的关节位置误差（Position）为61.4 cm，较DeepPhase-16C的144 cm降低超过57%（Table 1）。在100STYLE数据集上，FunPhase-256C的Position误差仅为0.36 cm，而DeepPhase-32C高达92.9 cm，差距达两个数量级。值得注意的是，FunPhase-256C的重建精度已接近非周期性自编码器ACMDM-AE（Position 0.32 cm），同时保持了更优的物理合理性指标，证明引入周期性归纳偏置并未损害表示能力，反而实现了更高效、结构化的运动编码。

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/003_Table_1.jpg]]
*Table 1: Autoencoder comparison on the DOG and 100STYLE datasets. FunPhase consistently outperforms DeepPhase in all metrics, showing more accurate and physically consistent reconstructions*

**Table 1** 进一步揭示，FunPhase在所有评估指标上一致优于DeepPhase，包括关节位置误差、足部滑动等物理合理性度量。这验证了函数空间解码替代离散帧重建的关键设计选择——连续时空函数求值能够在任意时间坐标处平滑重建运动，避免了离散卷积的上采样伪影。

### 潜在扩散生成主结果

将周期性分解融入扩散模型极大改善了生成质量。在100STYLE数据集上（Table 2），FunPhase的FID降至0.51±0.16，显著优于Function Diffusion（无相位分解的函数自编码器+扩散）的1.19±0.43，降幅达57.1%。与现有最优方法相比，FunPhase同样展现出竞争力：FID优于CAMDM的0.91±0.62（降幅44.0%），足部滑动（Foot Sliding）为0.52，低于CAMDM的0.69（降幅24.6%），表明生成的运动的物理合理性更优。

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/004_Table_2.jpg]]
*Table 2: Latent diffusion results on the 100STYLE dataset. Comparison between FunPhase and state-of-the-art motion latent diffusion baselines. FID and Accuracy evaluate perceptual fidelity and condition alignment, respectively. Diversity measures pose variation across generated samples, while Foot Sliding, Coherence, and ACCL assess physical realism*

在多骨架ZOO数据集上（Table 3），FunPhase与AnyTop等专为多骨架设计的方法相比，展现出相当的生成能力。这归功于基于图拉普拉斯特征向量或热扩散探针的骨架无关空间位置编码，使模型能够泛化到训练中未见过的骨架拓扑。

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/011_Table_3.jpg]]
*Table 3: Latent diffusion results on the ZOO dataset. We compare our method with other multi-skeleton baselines*

### 消融实验

**架构选择。** Table 4的系统消融揭示了各模块的贡献。分离根/关节的独立Perceiver编码器优于统一编码器（Joint Position 3.15 vs 3.37），验证了分别处理运动学链末端与内部关节的必要性。增大潜在通道数从32到256持续改善重建性能，表明周期性表示受益于更丰富的潜在基函数集合。

**前向运动学损失。** 移除前向运动学损失（FK loss）导致重建误差急剧上升——关节位置误差从3.15升至26.8（Table 4, No FK Loss vs 256 Channels）。这一消融结果（置信度0.95）有力地证明：仅监督旋转空间不足以约束全局运动学一致性，显式的前向运动学物理先验对保持骨架几何约束不可或缺。

**输入表示。** Table 5对比了全局关节位置与“旋转+根位置”两种表示。后者在所有评估指标上一致优于前者，表明将运动分解为局部旋转和全局根轨迹更有利于周期性潜在编码，因为局部旋转的周期性模式（如行走摆臂）比绝对坐标更易被正弦基函数捕获。

**相位变换。** Table 6显示，在扩散模型中对周期参数施加笛卡尔坐标变换和概率变换（Equation 9）略微改善了生成质量（FID 1.27→1.27，Accuracy 34.83→37.6）。该变换的动机是将非高斯分布的相位参数映射到更适合高斯扩散的空间（Figure 7可视化展示了变换前后分布的变化），但消融结果表明其影响相对温和，相位流形本身的结构化先验才是生成质量提升的主要驱动因素。

### 关键帧插值与超分辨率

FunPhase的函数空间解码天然支持任意时间分辨率采样，使其具备运动超分辨率能力。Table 7展示了在固定50帧窗口内，从不同间距的关键帧重建完整运动的误差。当关键帧间隔较小时，FunPhase的重建精度与SLERP线性插值相当；但当间隔增大至10帧时，FunPhase显著优于SLERP和Function AE（无相位分解的函数自编码器），证明周期性先验为稀疏观测下的平滑插值提供了强归纳偏置。Figure 4的定性示例进一步展示了FunPhase在稀疏关键帧条件下重建连续运动并保持物理合理性的能力。

### 失败模式与局限

当前模型在固定窗口（约60帧/1秒）上训练，生成更长序列需要额外的滑动窗口或外推策略，文中尚未充分探讨。超分辨率能力在关键帧间隔过大时仍会丢失高频细节——周期性正弦基函数本质上倾向于平滑重建，可能滤除快速、细粒度的运动细节（如手指微动）。此外，生成多样性相较于专有增强策略可能仍有提升空间，Table 2中FunPhase的Diversity指标与部分基线相比未见显著优势。

### 开放问题

1. **物理先验深化**：如何将接触力、动力学约束等基于物理的先验融入函数空间生成框架，以进一步提升真实性和泛化性。
2. **长时序建模**：如何改进建模更长运动窗口的能力，尤其在极低采样率的超分辨率设置下保持精细时序细节。
3. **多样性增强**：通过更优的采样策略或条件机制进一步提高生成动作的多样性。
4. **运动补全与中间帧**：如何利用函数相位表示进行运动中间帧插值和局部身体补全，并建立定量评估基准。

### 补充图表

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/012_Table_4.jpg]]
*Table 4: FunPhase Ablation. We test the performance of different architeture choices. The model 256 Channels represent our final model*

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/014_Table_6.jpg]]
*Table 6: Phase Transformation Ablation. Comparison between the Diffusion Latent Model with and without Phase Transformation*

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/016_Table_7.jpg]]
*Table 7: Reconstruction error under decreasing keyframe distances. Given a fixed window of 50 frames, each model reconstructs the full motion from a subsampled set of keyframes. Fun-Phase provides more accurate interpolation than both standard autoencoders and linear interpolation (SLERP) at shorter intervals*

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/006_Figure_4.jpg]]
*Figure 4: FunPhase super-resolution. Given a sparse set of keyframes, FunPhase reconstructs the full continuous motion while preserving physical plausibility*

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/009_Figure_5.jpg]]
*Figure 5: Diffusion examples on 100STYLE. On the left we show and example of generation from a sparse set of key frames (in green). On the right we show an example of body completion of the right leg (in pink)*

![[assets/figures/papers/paper_list_l1832_FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Pha/figures/010_Figure_6.jpg]]
*Figure 6: Motion controller generation. The top row shows the motion controller trained on FunPhase’s phase space, and the bottom row shows the controller trained on DeepPhase’s phase space. FunPhase enables the generation of smooth and realistic movements comparable to those produced by DeepPhase, highlighting the advantages of the phase manifold*



## 定位与知识库关联

### 1. 与现有工作的关系

FunPhase 处于**周期性运动表示**与**函数式运动生成**两条技术路线的交汇点，其设计直接回应了前代方法的两个核心瓶颈：固定骨架依赖与离散帧重建。

**相对于 DeepPhase (周期性自编码器基线)**
DeepPhase 首次将周期分解引入运动潜在空间，通过 FFT 将 1D 卷积编码器的输出参数化为振幅、频率、相位和偏置，构建了可解释的相位流形。然而，DeepPhase 的三个结构性限制制约了其扩展性：其一，编码器和解码器均基于固定大小的 1D 卷积，隐式绑定了骨架拓扑与帧率；其二，解码器通过反卷积直接输出离散帧序列，无法在任意时间坐标处求值；其三，整个框架缺乏概率生成能力，仅适用于确定性重建或控制任务。FunPhase 保留了 DeepPhase 的周期分解核心（Eq. 1 的正弦参数化与 Eq. 2-3 的相位流形构造），但将编解码器替换为基于 Perceiver 交叉注意力的连续时空函数求值框架，从根本上解除了骨架与帧率的约束。Table 1 的定量对比验证了这一改进的实质效果：在 DOG 数据集上，FunPhase-16C 的位姿误差为 61.4 cm，较 DeepPhase-16C 的 144 cm 降低超过 57%。

**相对于 Function Diffusion (函数式生成基线)**
函数式运动生成框架（文中引用为 ）将运动建模为连续时空函数，支持任意分辨率采样，但缺乏显式的周期结构先验。FunPhase 在该框架中嵌入了周期分解模块，使潜在空间获得相位流形结构。Table 2 的生成实验表明，这一嵌入带来了显著的 FID 改善：FunPhase 的 FID 为 0.51，而 Function Diffusion 为 1.19，降幅达 57.1%。这说明周期先验不仅未损害函数空间的表达能力，反而通过结构化潜在表示提升了生成质量。

**相对于其他运动生成基线**
在 100STYLE 数据集上，FunPhase 与几类代表性方法进行了系统对比：
- **MLD** (潜在运动扩散)：基于 VAE 潜在空间的扩散生成，未显式建模周期结构。
- **ACMDM** (绝对坐标运动扩散)：在绝对关节坐标上直接执行扩散，其自编码器变体 ACMDM-AE 在重建精度上略优于 FunPhase（Position 0.32 vs 0.36 cm），但物理合理性指标显著逊色——FunPhase 的足部滑动为 0.52，ACMDM 为 0.99，差距近一倍。
- **CAMDM** (条件自回归运动扩散)：专为风格化人类运动设计的条件扩散模型，在生成多样性上表现突出，但 FID（0.91 vs 0.51）和足部滑动（0.69 vs 0.52）均不及 FunPhase。
- **AnyTop** (多骨架运动生成)：支持跨骨架生成，但在 ZOO 多骨架数据集上（Table 3），FunPhase 在物理一致性指标上表现更优。

**运动控制器生成中的定位**
Figure 6 展示了在 FunPhase 相位空间上训练的运动控制器与在 DeepPhase 相位空间上训练的控制器对比。FunPhase 生成的控制器运动在平滑度和真实感上均达到可比甚至更优的水平，且受益于函数式解码器可实现连续轨迹输出。这表明 FunPhase 的相位流形保留了 DeepPhase 在控制任务中的有效性，同时拓展了应用边界。

### 2. 适用边界

**骨架无关性的范围**
FunPhase 通过图拉普拉斯特征向量或热扩散探针实现空间位置编码，使其理论上可处理任意骨架拓扑。Table 3 的 ZOO 多骨架实验验证了这一能力。然而，当前实验主要集中在人形和四足动物骨架，对于拓扑差异极大的骨架（如多肢节昆虫或非铰链结构），空间编码的泛化性尚需进一步验证。

**时间分辨率的灵活性**
函数式解码器允许在任意时间坐标处求值运动，Figure 4 的超分辨率实验展示了从稀疏关键帧重建连续运动的能力。但该能力受限于训练窗口大小（60 帧/约 1 秒）：当关键帧间隔过大时（Table 7，KF Dist. 10），重建误差显著上升，高频细节丢失。生成更长序列需要额外的滑动窗口或外推策略，文中尚未充分探讨。

**生成任务的边界**
FunPhase 的扩散生成在 100STYLE 数据集上取得了领先的 FID 和物理合理性指标，但生成多样性（Diversity）略低于 CAMDM（Table 2）。这表明周期结构先验在提升保真度的同时，可能对生成样本的变异度产生一定的约束效应。如何在结构化潜在空间与生成多样性之间取得更优平衡，仍是一个开放问题。

### 3. 局限与开放问题

**当前局限**
1. **固定窗口训练**：模型在 60 帧固定窗口上训练，生成更长运动序列需要滑动窗口拼接，可能引入时序不一致性。文中未给出长序列生成的定量评估。
2. **极低采样率下的退化**：Table 7 显示，当关键帧距离增大时，FunPhase 的插值误差虽优于 SLERP 和 Function AE，但仍呈上升趋势，表明连续函数表示在稀疏观测下的外推能力存在上限。
3. **物理先验的单一性**：当前物理正则化仅包含前向运动学损失（FK loss）和足部滑动惩罚。Table 4 的消融实验表明，移除 FK loss 会导致关节位置误差从 3.15 急剧升至 26.8，证明该先验不可或缺。但更丰富的物理约束（如接触力、动量守恒、动力学方程）尚未融入框架。

**开放问题**
1. **物理先验的深化**：如何将基于物理的约束（接触力、地面反作用力、动力学模型）融入函数空间生成框架，以进一步提升运动真实性和跨场景泛化性？
2. **运动中间帧插值与身体补全**：Figure 5 展示了初步的稀疏关键帧生成和身体部位补全示例，但缺乏系统性的定量评估。如何利用函数相位表示在这些任务上建立标准化的评测基准？
3. **长时序建模**：如何突破固定窗口限制，实现任意时长运动的连续生成？可能的方向包括循环式潜在编码、层次化时序抽象或基于状态空间模型的外推策略。
4. **生成多样性的提升**：Table 2 中 FunPhase 的多样性指标略低于 CAMDM。是否可以通过改进采样策略（如引导尺度调节、温度退火）或引入对抗训练组件，在保持相位结构优势的同时提升生成多样性？
5. **跨形态迁移**：FunPhase 的骨架无关设计使其具备跨形态运动迁移的潜力，但当前尚未在人体到机器人、真实动物到虚拟角色等跨具身场景中进行验证。



## 原文 PDF

![[paperPDFs/arxiv_2025/FunPhase_A_Periodic_Functional_Autoencoder_for_Motion_Generation_via_Phase_Manifolds.pdf]]
