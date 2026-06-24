---
title: "FRIDU: Functional Map Refinement with Guided Image Diffusion"
type: paper
paper_level: A
venue: SGP
year: 2025
pdf_ref: paperPDFs/SGP_2025/FRIDU_Functional_Map_Refinement_with_Guided_Image_Diffusion.pdf
project_link: https://github.com/avigailco/FRIDU
aliases:
- FRIDU
tags:
- SGP_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "在扩散模型推理阶段加入逐点映射引导（P2P guidance），并在功能空间中以图像形式训练扩散模型，使得映射精化过程既高效又可插拔。"
primary_logic: "将功能映射矩阵视为二维图像，利用基于Patch的条件图像扩散模型进行训练，完全在谱域完成，无需逐点映射监督；在推理时通过可微的逐点映射提取引导，灵活融入正交性、谱交换性等几何约束，实现显著的质量提升。"
claims:
- "采用Patch扩散训练策略，仅使用功能映射矩阵即可训练，完全避免逐点映射标注。"
- "推理时加入P2P引导可大幅提升点对应精度，相比无引导的精化映射改善显著。"
- "在与ZoomOut的对比中，FRIDU达到相近甚至更优的精度，且推理速度快约10倍（~60s vs ~600s）。"
- "模型可以零样本泛化到不同描述符：使用WKS训练的模型可以有效精化SHOT初始映射，反之亦然。"
---

# FRIDU: Functional Map Refinement with Guided Image Diffusion

> [!tip] 核心洞察
> 将功能映射矩阵视为二维图像，利用基于Patch的条件图像扩散模型进行训练，完全在谱域完成，无需逐点映射监督；在推理时通过可微的逐点映射提取引导，灵活融入正交性、谱交换性等几何约束，实现显著的质量提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FRIDU：基于引导图像扩散的功能映射精化 |
| 英文题名 | FRIDU: Functional Map Refinement with Guided Image Diffusion |
| 会议/期刊 | SGP 2025 |
| Links | [paper](https://arxiv.org/abs/2506.14322); [GitHub](https://github.com/avigailco/FRIDU) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | FRIDU |
| Dataset | FAUST, SCAPE, SHREC19, Michael (TACO) |

> [!tip] 效果简介
> - FAUST 上，Mean geodesic error (×100) 为 1.7 (Train:F)，对比 DiffZO (值未明确，但FRIDU更低)，变化 优于DiffZO。
> - SCAPE 上，Mean geodesic error (×100) 为 4.1 (Train:F)，对比 优于DiffZO，变化 准确率提升。
> - SHREC19 上，Mean geodesic error (×100) 为 9.4 (Train:F)，对比 优于DiffZO，变化 准确率提升。

## 概述

**问题瓶颈**：传统功能映射精化方法难以在深度网络中有效结合逐点映射一致性约束，且通常依赖大量显式逐点对应标注进行训练，无法灵活适应不同来源的初始映射。

**核心思路**：FRIDU 将功能映射精化重新定义为条件图像生成问题——把功能映射矩阵视为二维图像，利用基于 Patch 的条件扩散模型在谱域完成训练，完全避免逐点映射监督；在推理时通过可微的逐点映射引导，灵活融入正交性、拉普拉斯交换性等几何约束，实现显著的质量提升。

**方法定位**：FRIDU 属于无监督功能映射精化方法，与经典迭代方法 **ZoomOut**（Melzi et al., arXiv 2019）和可微分学习方法 **DiffZO**（Magnet & Ovsjanikov, CVPR 2024）形成互补。其关键创新在于将扩散模型的生成能力与几何引导机制解耦，使精化过程既高效又可插拔。

**主要结果**：
- 在 FAUST、SCAPE、SHREC19 等标准基准上，FRIDU 的测地误差均达到或优于当前最优无监督方法 DiffZO（Table 1）。
- 与 ZoomOut 相比，FRIDU 达到相近甚至更优的精度，且推理速度快约 10 倍（~60s vs ~600s，Figure 8）。
- 模型具备零样本条件泛化能力：使用 WKS 训练的模型可有效精化 SHOT 初始映射，反之亦然（Figure 10）。
- 消融实验证实，推理时加入逐点映射引导是性能提升的关键因素（Figure 4）。

## 背景与动机

### 形状对应与功能映射框架

三维形状对应是计算机图形学与几何处理中的核心问题，其目标是建立两个形状表面点之间的有意义的映射关系。功能映射框架为该问题提供了一个强大的代数范式：通过将对应关系编码为在拉普拉斯–贝尔特拉米（Laplace–Beltrami）特征函数基下的小型矩阵——即**功能映射矩阵**（functional map），将原本需要在点云或网格上求解的大规模组合优化问题转化为谱域中的线性代数问题。这一框架使得形状匹配的复杂度从点数依赖降低到谱基维度依赖，显著提升了计算效率。

在功能映射框架下，给定源形状 $\mathcal{M}_1$ 和目标形状 $\mathcal{M}_2$，分别具有拉普拉斯特征基 $\Phi_1$ 和 $\Phi_2$，一个功能映射 $C_{21}$ 将源形状上的函数系数转换到目标形状上：若函数 $f_1$ 在 $\mathcal{M}_1$ 上的谱系数为 $\mathbf{a}$，则其在 $\mathcal{M}_2$ 上的对应函数谱系数近似为 $C_{21}\mathbf{a}$。理想的 $C_{21}$ 应当满足一系列结构性约束，包括正交性（等距映射下）和与拉普拉斯算子的交换性。

### 功能映射精化的现有方法及其瓶颈

尽管功能映射框架在理论上简洁优雅，但实际计算得到的初始功能映射通常质量有限——它们往往受制于描述符噪声、对称性模糊以及谱基截断带来的信息损失。因此，**功能映射精化**（functional map refinement）成为形状对应流程中不可或缺的后处理环节。

现有精化方法大致可分为两类：

- **公理化精化方法**：以 **ZoomOut**（Melzi et al., arXiv 2019）为代表，通过交替提升谱维度与投影到逐点映射空间来实现迭代精化。该方法无需训练数据，但计算代价高昂——每对形状的推理耗时约600秒，难以应用于大规模或实时场景。

- **可微学习精化方法**：如 **DiffZO**（Magnet & Ovsjanikov, CVPR 2024），将精化组件嵌入可微分的功能映射学习管线中。这类方法虽然提高了效率，但通常需要显式的逐点对应标注进行训练，且精化过程与特征学习深度耦合，灵活性和可插拔性有限。

上述方法的共同瓶颈在于：**难以在深度网络框架内有效结合逐点映射一致性约束**。逐点对应信息是评估功能映射几何质量的关键信号，但将其作为训练监督需要昂贵的标注，而将其作为结构化约束融入网络推理又面临不可微性和计算复杂度的挑战。此外，现有精化方法对训练数据的规模和质量有较高依赖，难以灵活适配来自不同描述符（如WKS、SHOT）或不同特征提取器的初始映射。

### FRIDU的核心动机与设计思路

FRIDU 的提出正是为了突破上述瓶颈。其核心动机来自一个关键观察：**功能映射矩阵在形式上天然类似于二维图像**——矩阵的行列分别对应源形状和目标形状的谱基索引，矩阵元素值反映基函数间的耦合强度。这一观察启发作者将功能映射精化重新定义为**条件图像生成问题**，从而可以充分利用现代图像扩散模型的强大生成先验。

基于这一视角，FRIDU 的设计思路围绕三个关键原则展开：

1. **谱域训练，摆脱逐点标注**：训练阶段完全在功能空间（谱域）进行，将功能映射矩阵视为图像，利用基于Patch的条件扩散模型学习从含噪初始映射恢复干净映射的分布。这一策略使得训练仅需功能映射矩阵本身，完全避免了逐点对应标注的需求（见 Section 2.3）。

2. **推理时可插拔的几何引导**：在扩散模型的去噪推理过程中，通过可微的逐点映射提取模块（最近邻搜索）计算当前功能映射对应的逐点对应关系，并以此构建P2P引导损失（见 Eq. 7），引导生成过程朝向几何一致的方向。此外，正交性约束和拉普拉斯交换性损失等几何正则项可以灵活地插入引导过程，无需重新训练模型（见 Section 2.6）。

3. **高效的数据利用与快速推理**：采用随机裁剪Patch的扩散训练策略并附加空间位置通道，在小数据集上实现高效学习（见 Section 2.5）。推理时使用EDM确定性采样器，每对形状的精化仅需约60秒，相比ZoomOut实现约10倍加速（见 Figure 8）。

这种“训练在谱域、引导在几何域”的分离设计，使得FRIDU既保留了扩散模型强大的生成能力，又获得了对几何约束的灵活整合能力，同时保持了方法的可插拔性——它可以作为任意初始功能映射（无论来自经典描述符还是深度特征提取器）的后处理精化模块。

## 核心创新

FRIDU 的核心创新在于将功能映射精化问题重新表述为**条件图像生成任务**，并在扩散模型的推理阶段引入**可微的逐点映射引导**，从而在无需逐点对应标注的前提下，实现高效、可插拔的映射质量提升。以下从三个关键维度展开分析。

### 1. 训练范式变革：从逐点监督到纯谱域学习

传统功能映射学习方法通常依赖显式的逐点对应标注或从几何/颜色特征中学习映射关系，数据获取成本高昂。FRIDU 的根本性突破在于：

- **功能映射矩阵的图像化处理**：将功能映射矩阵 $C_{ij}$ 视为二维图像，矩阵元素直接映射为像素值。这一视角转换使得功能映射精化可以充分利用成熟的图像扩散模型架构。
- **纯谱域训练**：训练过程完全在功能（谱）域完成，仅需功能映射矩阵本身作为监督信号，无需访问任何显式的逐点对应标注（Section 2.3）。具体而言，训练目标为：

$$\mathbb{E}_{(\mathcal{M}_{j}, \mathcal{M}_{i}) \sim \mathcal{D}_{\mathrm{shapes}}} \left[ \lambda(\sigma) \| C_{ij}^{*} - d_{\Theta}(C_{ij}^{N} \mid \widetilde{C}_{ij}, \sigma) \|_{2}^{2} \right]$$

其中 $C_{ij}^{N} = C_{ij}^{*} + \sigma \cdot \epsilon$ 为向真实功能映射添加高斯噪声后的含噪版本，模型 $d_{\Theta}$ 以初始功能映射 $\widetilde{C}_{ij}$ 和噪声水平 $\sigma$ 为条件，学习从含噪映射恢复干净映射。

这一设计使得训练数据需求大幅降低——仅需形状对及其对应的功能映射矩阵，而无需昂贵的逐点标注。

### 2. 推理机制创新：可插拔的逐点映射引导

传统精化方法（如 **ZoomOut**，Melzi et al., arXiv 2019）依赖专门的迭代优化算法（交替提升谱维度与投影到逐点映射空间），计算开销大且灵活性有限。FRIDU 的推理机制实现了两个层面的突破：

- **扩散采样与引导解耦**：在 EDM 确定性采样过程中（更新规则为 $C_{21}^{t-1} = C_{21}^{t} + (\sigma_{t-1}^{2} - \sigma_{t}^{2}) \frac{d_{\theta}(C_{21}^{t} \mid \widetilde{C}_{21}, \sigma_{t}) - C_{21}^{t}}{\sigma_{t}^{2}}$），每个去噪步均可灵活注入引导信号。
- **P2P 引导的核心机制**：在每个去噪步，通过最近邻搜索从当前功能映射 $C_{21}^{t}$ 中提取逐点对应矩阵 $\Pi_{21}$，并计算引导损失：

$$\mathcal{L}_{\mathrm{P2Pg}}(C_{21}^{t}) = \| \Phi_{2} C_{21}^{t} - \Pi_{21} \Phi_{1} \|_{\mathcal{M}_{2}}^{2}$$

关键设计在于**停止 $\Pi_{21}$ 的梯度回传**，仅对 $C_{21}^{t}$ 求梯度。这使得引导损失能够将扩散过程“拉向”几何一致的方向，同时避免最近邻搜索的不可微性干扰梯度流。

- **可插拔的几何约束**：除 P2P 引导外，推理时还可灵活添加正交性约束和拉普拉斯交换性损失等几何正则项，无需重新训练模型。这种模块化设计使得同一基础模型可适配不同的精度需求。

消融实验（Figure 4）提供了决定性证据：**去除 P2P 引导后，精化映射的质量大幅下降**，验证了引导损失的关键作用。

### 3. 数据效率策略：Patch 级扩散训练

为在小数据集上实现高效学习，FRIDU 采用**随机裁剪 Patch 的扩散训练策略**，并附加空间位置通道：

$$\mathbb{E}_{(a,b) \sim \mathcal{U}(\mathcal{R})} \| d_{\Theta}( C_{ij}^{(p)} + \sigma \cdot \epsilon \;|\; \widetilde{C}_{ij}^{(p)}, a, b, s, \sigma ) - C_{ij}^{(p)} \|_{2}^{2}$$

这一策略仅对功能映射的随机裁剪块进行去噪训练，结合位置编码 $(a, b, s)$ 提供空间上下文。相比全图训练，Patch 策略显著提高了数据利用率，使得模型能在有限形状对上学习到鲁棒的精化能力。

### 与 DiffZO 的本质差异

**DiffZO**（Magnet & Ovsjanikov, CVPR 2024）虽然也包含无训练参数的精化组件，但其本质是可微分功能映射学习框架的一部分，精化能力受限于其显式优化的设计空间。FRIDU 的生成式范式使其能够学习更丰富的映射分布先验，并在推理时通过引导机制灵活融入几何约束，在多个基准上取得了优于 DiffZO 的结果（Table 1）。

### 创新边界与局限

FRIDU 的创新能力受限于以下因素：
- 作为精化方法，对初始映射质量有一定依赖性；极度噪声或包含大量错误对称性的初始映射可能限制精化效果。
- 递归精化仅在单次迭代内有效，多次迭代会引入退化，限制了全自动迭代精化的应用。
- 引导超参数（$m, k, s$）需手工调节，最优参数可能因数据集而异（Table 2, Figure 11）。

## 整体框架

FRIDU 将功能映射精化问题重新表述为**条件图像生成**任务，其核心逻辑是：将功能映射矩阵 $C_{ij} \in \mathbb{R}^{k_j \times k_i}$ 视为一张二维图像，利用扩散模型在谱域中学习从含噪初始映射到干净精化映射的映射关系。整个 pipeline 由训练和推理两个阶段构成，二者共享同一个条件扩散去噪骨干网络，但在数据流和约束机制上有本质区别。

### 训练阶段：纯谱域的 Patch 条件扩散

训练阶段完全在功能空间（谱域）中进行，**不需要任何逐点对应标注**。给定一对形状 $(\mathcal{M}_i, \mathcal{M}_j)$，pipeline 的输入包括：
- **真实功能映射** $C_{ij}^*$（从已知对应关系中计算得到，仅用于训练监督）
- **初始功能映射** $\widetilde{C}_{ij}$（通过 WKS 或 SHOT 等描述符计算得到，作为条件输入）
- **噪声尺度** $\sigma$（从对数正态分布中采样）

训练流程（Figure 2 左侧）如下：

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_14322/figures/002_Figure_2.jpg]]
*Figure 2: An illustration of our (left) training and (right) inference procedures. During training, our pipeline takes as input a random patch of a noisy functional map $\widetilde { C } _ { i j } ^ { N }$ , conditioned on a corresponding patch of an initial functional map $\widetilde { C } _ { i j }$ and position maps, and outputs the denoised patch of the functional map $C _ { i j }$ . At inference time, the patch covers the full-sized image, and we incorporate guidance at each denoising step, including point-to-point guidance and potentially additional regularizers, such as orthogonality and Laplacian commutativity

1. **加噪**：向真实功能映射 $C_{ij}^*$ 添加高斯噪声，生成含噪映射 $C_{ij}^N = C_{ij}^* + \sigma \cdot \epsilon$，其中 $\log\sigma \sim \mathcal{N}(\mu_p, \sigma_p^2)$，$\epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$。

2. **Patch 裁剪**：从含噪映射和初始映射中随机裁剪相同位置的矩形块（patch），同时附加两个空间位置编码通道（分别编码行、列坐标），形成条件输入。这一策略显著提高了数据利用率，使模型能在较小数据集上有效训练。

3. **去噪预测**：条件扩散模型 $d_\Theta$（基于 EDM-DDPM++ 架构的 UNet）接收含噪 patch、对应初始映射 patch、位置编码和噪声尺度 $\sigma$，直接预测干净的功能映射 patch $C_{ij}^{(p)}$。

4. **损失优化**：训练目标为 patch 级的均方误差损失：
   $$\mathbb{E}_{(a,b) \sim \mathcal{U}(\mathcal{R})} \| d_\Theta( C_{ij}^{(p)} + \sigma \cdot \epsilon \;|\; \widetilde{C}_{ij}^{(p)}, a, b, s, \sigma ) - C_{ij}^{(p)} \|_{2}^{2}$$
   其中 $(a,b)$ 为 patch 的空间位置，$s$ 为 patch 尺寸。损失函数中引入噪声水平相关的权重 $\lambda(\sigma)$ 以平衡不同噪声尺度的学习难度。

### 推理阶段：带引导的扩散采样

推理时，给定一对新形状及其谱基 $\Phi_1, \Phi_2$ 和初始功能映射 $\widetilde{C}_{21}$，pipeline 从随机噪声出发，通过多步确定性采样逐步生成精化映射 $C_{21}^0$（Figure 2 右侧）。此时 patch 覆盖整个功能映射矩阵（即全尺寸图像），并在每个去噪步中引入**可插拔的引导机制**：

1. **扩散采样**：采用 EDM 确定性采样器，从 $t=T$ 到 $t=0$ 迭代更新：
   $$C_{21}^{t-1} = C_{21}^{t} + (\sigma_{t-1}^{2} - \sigma_{t}^{2}) \frac{d_{\theta}(C_{21}^{t} \mid \widetilde{C}_{21}, \sigma_{t}) - C_{21}^{t}}{\sigma_{t}^{2}}$$

2. **逐点映射（P2P）引导**：在每个去噪步，通过最近邻搜索从当前功能映射中提取逐点对应矩阵：
   $$\Pi_{21}(C_{21}^t) = \arg\min_{\Pi_{21} \in \mathcal{P}_{21}} \| \Phi_{2} C_{21}^t - \Pi_{21} \Phi_{1} \|_{\mathcal{M}_{2}}^{2}$$
   然后计算 P2P 引导损失 $\mathcal{L}_{\mathrm{P2Pg}}(C_{21}^{t}) = \| \Phi_{2} C_{21}^{t} - \Pi_{21} \Phi_{1} \|_{\mathcal{M}_{2}}^{2}$，并将其梯度（停止 $\Pi_{21}$ 的梯度回传）注入去噪过程，使生成的功能映射在几何上更一致。

3. **可插拔几何约束**：除 P2P 引导外，还可选择性添加正交性约束和拉普拉斯交换性损失，进一步提升等距映射的质量。这些约束以即插即用的方式作用于去噪步，无需重新训练模型。

### 可选扩展：谱上采样与递归精化

推理时还可引入**谱上采样**策略，逐步增加功能映射的谱维度（从 $k \times k$ 提升到 $K \times K$，$K > k$），模拟经典方法 ZoomOut 的谱提升效果。此外，FRIDU 支持**一次递归精化**——将精化后的映射作为新的初始映射再次输入模型，通常能进一步提升精度；但实验表明，多次递归迭代会导致性能退化，因此实际使用中仅推荐单次递归。

## 核心模块与公式推导

### 1. 问题重构：功能映射作为条件图像生成

FRIDU 的核心创新在于将功能映射精化问题重新表述为**条件图像生成**任务。给定一对形状 $\mathcal{M}_1, \mathcal{M}_2$ 及其对应的谱基 $\Phi_1, \Phi_2$，初始功能映射矩阵 $\widetilde{C}_{21}$ 被视为一张“图像”，其矩阵元素值直接映射为像素值。扩散模型的任务是学习从含噪的“图像”中恢复出干净、精化的功能映射 $C_{21}^*$，整个过程完全在谱域中完成，无需访问显式的逐点对应监督。

### 2. 训练模块：Patch 条件扩散去噪模型

#### 2.1 噪声注入与训练目标

训练阶段遵循 EDM-DDPM++ 去噪扩散框架。对于每对形状，从真实功能映射 $C_{ij}^*$ 出发，施加连续噪声水平的高斯噪声：

$$C_{ij}^{N} = C_{ij}^{*} + \sigma \cdot \epsilon, \quad \log \sigma \sim \mathcal{N}(\mu_{p}, \sigma_{p}^{2}), \quad \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

其中 $\sigma$ 为噪声尺度，从对数正态分布中采样，$\epsilon$ 为标准高斯噪声。去噪模型 $d_{\Theta}$ 以含噪映射 $C_{ij}^N$、初始映射 $\widetilde{C}_{ij}$ 和噪声水平 $\sigma$ 为条件，直接预测干净映射，训练目标为加权均方误差最小化：

$$\mathbb{E}_{(\mathcal{M}_{j}, \mathcal{M}_{i}) \sim \mathcal{D}_{\mathrm{shapes}}} \left[ \lambda(\sigma) \| C_{ij}^{*} - d_{\Theta}(C_{ij}^{N} \mid \widetilde{C}_{ij}, \sigma) \|_{2}^{2} \right]$$

$\lambda(\sigma)$ 为噪声水平相关的权重函数，用于平衡不同噪声尺度下的梯度贡献。

#### 2.2 Patch 级训练策略

为提高数据效率并降低对大规模形状对数据的依赖，FRIDU 采用**随机裁剪 Patch 训练策略**。训练时仅从功能映射矩阵中随机裁剪局部块，并附加空间位置编码通道 $(a, b, s)$ 以保留块在原图中的绝对位置信息。Patch 级去噪损失为：

$$\mathbb{E}_{(a,b) \sim \mathcal{U}(\mathcal{R})} \| d_{\Theta}( C_{ij}^{(p)} + \sigma \cdot \epsilon \;|\; \widetilde{C}_{ij}^{(p)}, a, b, s, \sigma ) - C_{ij}^{(p)} \|_{2}^{2}$$

其中 $\mathcal{R}$ 为所有有效裁剪区域的集合，$(a, b)$ 为裁剪起始坐标，$s$ 为裁剪尺寸。这一策略使得模型能够从小数据集中高效学习功能映射的局部结构模式，同时位置编码确保了全局空间一致性。

### 3. 推理模块：确定性采样与可微引导

#### 3.1 EDM 确定性采样

推理时，给定一对新形状及其初始功能映射 $\widetilde{C}_{21}$，模型从随机噪声出发，通过 EDM 框架的确定性二阶采样器逐步生成精化映射。单步更新规则为：

$$C_{21}^{t-1} = C_{21}^{t} + (\sigma_{t-1}^{2} - \sigma_{t}^{2}) \frac{d_{\theta}(C_{21}^{t} \mid \widetilde{C}_{21}, \sigma_{t}) - C_{21}^{t}}{\sigma_{t}^{2}}$$

其中 $\sigma_t$ 为时间步 $t$ 的噪声水平，$d_{\theta}$ 为训练好的去噪模型。该更新本质上沿着去噪得分方向进行确定性外推，逐步降低噪声水平直至生成干净的功能映射 $C_{21}^0$。

#### 3.2 逐点映射提取与 P2P 引导

基础扩散模型生成的 $C_{21}$ 在功能空间具有合理性，但可能缺乏严格的几何一致性。为此，FRIDU 在推理的每个去噪步中引入**可微的逐点映射引导**（P2P guidance）。首先通过最近邻搜索从当前功能映射提取对应的逐点映射矩阵 $\Pi_{21}$：

$$\Pi_{21}(C_{21}) = \arg\min_{\Pi_{21} \in \mathcal{P}_{21}} \| \Phi_{2} C_{21} - \Pi_{21} \Phi_{1} \|_{\mathcal{M}_{2}}^{2}$$

该优化问题通过计算 $\Phi_2 C_{21}$ 与 $\Phi_1$ 行向量之间的最近邻匹配高效求解。随后计算 P2P 引导损失：

$$\mathcal{L}_{\mathrm{P2Pg}}(C_{21}^{t}) = \| \Phi_{2} C_{21}^{t} - \Pi_{21} \Phi_{1} \|_{\mathcal{M}_{2}}^{2}$$

**关键设计**：在计算 $\mathcal{L}_{\mathrm{P2Pg}}$ 对 $C_{21}^t$ 的梯度时，**停止 $\Pi_{21}$ 的梯度回传**（即将其视为常数），仅引导 $C_{21}^t$ 向与当前逐点对应一致的方向更新。这一“停止梯度”策略避免了双层优化的复杂性，同时有效将几何一致性约束注入扩散去噪过程。

#### 3.3 可插拔几何约束引导

除 P2P 引导外，FRIDU 可灵活添加额外的几何正则化项：

- **正交性约束**：要求功能映射 $C_{21}$ 近似正交，即 $C_{21}^T C_{21} \approx I$，保持谱域结构。
- **拉普拉斯交换性损失**：强制 $C_{21}$ 与形状的拉普拉斯算子交换，即 $L_2 C_{21} \approx C_{21} L_1$，这对于等距形状对尤为重要。

这些约束以可插拔方式集成到引导损失中，用户可根据具体应用场景选择性启用。

#### 3.4 谱上采样（可选）

推理过程中可选择性地逐步增加功能映射的谱维度，模拟经典方法 **ZoomOut**（Melzi et al., arXiv 2019）的谱提升效果。具体而言，从低维功能映射开始生成，在采样过程中逐步扩展矩阵尺寸，使得模型能够在不同谱分辨率下逐步精化对应关系。

### 4. 递归精化

FRIDU 支持将精化后的映射作为新的初始映射再次输入模型进行递归精化。实验表明，**单次递归迭代通常能进一步提升精度**，但超过一次迭代会导致性能退化——这可能源于去噪过程引入的累积偏差偏离了训练分布。因此实际使用中建议仅采用一次递归精化。

## 实验与分析

### 主要结果：形状匹配精度

FRIDU 在标准非刚性形状匹配基准 FAUST、SCAPE 和 SHREC19 上表现出具有竞争力的测地误差。Table 1 汇总了与公理化方法、有监督方法和无监督方法的对比结果。当仅在 FAUST 上训练时（Train:F），FRIDU 在 FAUST 上达到 1.7（×100）的平均测地误差，在 SCAPE 上达到 4.1，在 SHREC19 上达到 9.4，均优于同类无监督方法 **DiffZO**（Magnet & Ovsjanikov, CVPR 2024）。当在 FAUST+SCAPE 上联合训练时（Train:F+S），误差进一步降至 1.5 / 2.1 / 7.1。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_14322/figures/008_Table_1.jpg]]
*Table 1: Mean geodesic errors (×100) when training and testing on the FAUST, SCAPE and SHREC19 datasets. Best result within each method category (axiomatic, supervised, and unsupervised methods) is shown in bold. We consider DiffZO as part of the unsupervised category. The axiomatic and supervised methods are from [SMJ∗23b] and the unsupervised methods are from [MO24]*

值得注意的是，FRIDU 的初始映射完全基于经典描述符（WKS 或 SHOT）计算，不依赖任何深度特征提取器。Table 1 中 DiffZO 的结果来自其无监督设置，FRIDU 在所有三个数据集上均取得更优或相当的精度，验证了扩散精化策略的有效性。

### 逐点映射引导的消融

P2P 引导是 FRIDU 推理管线的核心组件。Figure 4 对比了有无 P2P 引导时的逐点映射质量：无引导时，扩散模型虽能产生视觉上更清晰的功能映射矩阵，但提取的逐点对应精度提升有限；加入 P2P 引导后，归一化欧几里得误差出现显著下降（阴影区域为标准差）。消融实验确认，去除引导会导致精化映射的质量大幅退化，证明引导损失在维持几何一致性方面起关键作用。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_14322/figures/001_Figure.jpg]]

### 引导参数敏感性

引导参数 $m$（引导步数间隔）、$k$（最近邻数量）和 $s$（引导尺度）的消融结果见 Figure 11 和 Table 2。增大 $m$ 和 $k$ 会增加推理时间，但能持续提高精度直至饱和；$s$ 存在最佳平衡点，过大或过小均导致误差上升。论文选用的默认参数（$m=2, k=5, s=500$）在推理时间与精度之间取得了良好平衡。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_14322/figures/011_Table_2.jpg]]
*Table 2: Guidance Parameters. Inference time and mean error for different values of the guidance parameters m, k, and s from [BCS∗23]. The best result in each column is shown in bold. We note that our chosen parameters (first row) provide a good balance between inference time and accuracy*

### 与 ZoomOut 的对比及谱上采样

Figure 8 在 Michael（TACO）数据集上对比了 FRIDU 与经典公理化精化方法 **ZoomOut**（Melzi et al., arXiv 2019）。在三种初始映射计算方式下，不带谱上采样的 FRIDU 已能显著改善初始映射，但精度仍不及 ZoomOut。当在推理时加入谱上采样（逐步提升功能映射的谱维度）后，FRIDU 达到与 ZoomOut 相当甚至更优的精度。关键优势在于推理效率：FRIDU 每对形状约需 60 秒，而 ZoomOut 约需 600 秒，加速约 10 倍。

### 零样本条件泛化

Figure 10 验证了模型的零样本条件泛化能力。使用 WKS 初始映射训练的模型可直接精化 SHOT 初始映射（记为 SHOT(WKS)），反之亦然（记为 WKS(SHOT)），无需额外训练。两种跨描述符设置均能有效精化，且 SHOT(WKS) 的效果优于 WKS(SHOT)。这一特性使 FRIDU 可作为即插即用的精化模块，灵活适配不同来源的初始映射。

### 递归精化与失败模式

递归精化实验显示，单次递归迭代通常能进一步提升精度，但多次迭代会导致性能退化。这一退化现象限制了全自动迭代精化的应用场景。此外，FRIDU 作为精化方法，对初始映射质量有一定依赖性：若初始映射包含大量错误对称性或极度噪声，精化效果可能受限。Figure 6 展示了地标约束可有效解决对称翻转问题，即使模型未在地标条件下训练，推理时加入地标约束也能纠正对称错误。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_14322/figures/003_Figure_3.jpg]]
*Figure 3: Refinement without Guidance (WKS). We map a function $f _ { 1 } \in \mathbb { R } ^ { n _ { 1 } }$ defined on $\mathcal { M } _ { 1 }$ to $\mathcal { M } _ { 2 }$ , , using the initial, FRIDU refined, and ground-truth functional maps. Here, we map the function $\Phi _ { 1 } ^ { \dagger } f _ { 1 }$ using the functional map matrices to get ${ \tilde { f } } _ { 2 }$ , , and show $\Phi _ { 2 } \tilde { f } _ { 2 }$ on $\mathcal { M } _ { 2 }$ . Note that in this figure only, our refined map does not include guidance in inference, in order to isolate and illustrate the refinement ability of the base model. The top row visualizes the source and mapped functions, and the bottom row shows the corresponding fun...

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_14322/figures/012_Figure.jpg]]
*Figure: WKS (SHOT) SHOT (WKS)*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_14322/figures/005_Figure_5.jpg]]
*Figure 5: Functional Map Refinement (SHOT). We show the performance of the pointwise mapping extracted from our refined map alongside the initial and ground-truth mappings. We additionally show the corresponding functional map matrices. Note the noisy appearance of the SHOT-based initial map. The plot shows the normalized Euclidean error over the Michael dataset, where our refined maps consistently outperform the initial maps*

## 方法谱系与知识库定位

### 1. 方法谱系：从功能映射到扩散精化

FRIDU 处于**功能映射（Functional Map）精化方法**的演进脉络中，其直接前驱包括经典迭代精化与可微学习两类范式。

**经典迭代精化**以 **ZoomOut**（Melzi et al., arXiv 2019）为代表，核心机制是交替提升功能映射的谱维度与投影到逐点映射空间，通过反复迭代逐步改善映射质量。ZoomOut 无需训练数据，但每次精化需要约 600 秒的推理时间，且对初始映射质量敏感。

**可微分精化**以 **DiffZO**（Magnet & Ovsjanikov, CVPR 2024）为代表，将功能映射学习与精化嵌入统一的深度框架中，包含无训练参数的精化组件。DiffZO 在 FAUST、SCAPE 等基准上取得了当时无监督方法的最优结果。

FRIDU 的方法论创新在于**将功能映射精化重新表述为条件图像生成问题**，这在功能映射文献中尚无先例。具体而言：

- **训练域迁移**：ZoomOut 和 DiffZO 或在逐点空间操作，或需要显式的几何特征输入。FRIDU 将功能映射矩阵 $C_{ij} \in \mathbb{R}^{k \times k}$ 视为二维图像，完全在谱域训练扩散模型，无需访问逐点对应标注（Section 2.3）。
- **推理约束融合**：不同于 ZoomOut 的硬交替投影，FRIDU 在扩散去噪的每一步通过可微损失引入几何引导，包括逐点映射一致性（P2P guidance）、正交性约束和拉普拉斯交换性损失（Section 2.6）。这种“软约束”机制使得模型在保持生成质量的同时灵活融入多种先验。
- **数据效率策略**：采用 Patch 级扩散训练（Eq. 4），对随机裁剪的功能映射块进行去噪学习，配合空间位置编码，在小数据集上实现高效训练。这与标准功能映射方法依赖完整形状对形成对比。

### 2. 知识库定位：扩散模型与几何处理的交叉

FRIDU 的知识贡献位于**生成式图像扩散模型**与**谱域几何处理**的交叉地带。

**扩散模型侧**，FRIDU 直接继承 EDM-DDPM++ 框架（Karras et al., NeurIPS 2022），采用连续时间噪声调度和二阶确定性采样器。其条件机制——以初始功能映射 $\widetilde{C}_{ij}$ 和噪声尺度 $\sigma$ 作为条件输入——遵循标准条件扩散范式。推理时的引导策略则借鉴了扩散模型在分子生成、图像编辑等领域的 guided diffusion 思想，但将其适配到功能映射的几何约束上。

**几何处理侧**，FRIDU 深度依赖功能映射框架的核心算子：拉普拉斯特征基 $\Phi$、功能映射矩阵 $C_{ij}$、以及通过最近邻搜索从 $C_{ij}$ 提取逐点映射 $\Pi_{21}$ 的标准流程（Eq. 5）。其引导损失 $\mathcal{L}_{\mathrm{P2Pg}}$（Eq. 7）本质上是功能映射文献中经典的逐点一致性约束的可微版本。

这一交叉定位带来了独特的优势与限制：

- **优势**：扩散模型的强大先验使 FRIDU 能从不完美的初始映射中恢复合理的功能映射结构，即使初始映射包含大量噪声（如 SHOT 描述符产生的初始映射，见 Figure 5）。零样本条件泛化实验（Figure 10）表明，模型学到的“功能映射流形”具有一定的跨描述符迁移能力。
- **限制**：模型的训练完全在功能空间进行，未直接利用原始几何特征（如法线、曲率），可能错过某些局部几何细节。当前实验主要针对等距或近等距形状对，在非等距、大尺度形变或跨类别形状上的泛化能力尚未充分验证。

### 3. 适用边界与关键局限

**适用边界**：
- FRIDU 是一个**精化方法**，而非端到端的对应求解器。其输入必须包含预计算的功能映射，对初始映射质量有一定依赖；若初始映射极度噪声或包含大量错误对称性，精化效果可能受限。
- 当前验证范围集中于**等距形状匹配**基准（FAUST、SCAPE、SHREC19）和近等距的人体/动物形状（TACO 数据集），在非等距或大尺度拓扑变化场景下的表现需要进一步验证。
- 模型假设功能映射矩阵为方阵（即源和目标形状使用相同数量的谱基），这限制了其在部分对应或矩形功能映射场景中的直接应用。

**关键局限**（来自 verified_analysis）：
1. **递归退化**：一次递归精化通常可提升精度，但多次递归迭代会导致性能退化（Section 2.7），限制了全自动迭代精化的应用。
2. **超参数敏感性**：引导强度等超参数需要手工调节；虽然消融实验（Figure 11, Table 2）展示了参数鲁棒性，但最优参数可能因数据集而异。
3. **几何信息利用不充分**：模型训练完全在功能空间进行，未直接利用原始几何特征，可能错过某些局部几何细节。
4. **非等距泛化未验证**：当前实验主要针对等距或近等距的形状对，尚未在非等距、大尺度形变或跨类别形状上充分验证泛化能力。

### 4. 开放问题

以下开放问题来自 verified_analysis 中的 open_questions，供后续研究参考：

1. **基础模型扩展**：能否将 FRIDU 扩展为功能映射的基础模型，在不同形状类别间实现零样本泛化？当前的零样本条件泛化（Figure 10）仅涉及描述符切换，跨类别泛化仍需探索。
2. **学习式引导**：学习到的引导（如利用神经评分函数）能否代替手工设计的几何损失，进一步提高灵活性和精度？这可以视为将当前的显式几何约束内化为模型能力。
3. **自适应参数选择**：如何自动确定最优的引导参数（$m, k, s$）以及扩散采样步数，以适应不同的输入数据？当前的手工调参限制了方法的即插即用性。
4. **矩形映射与部分对应**：能否将方法扩展到矩形功能映射或部分对应问题，并保留推理时引导的灵活性？这需要重新设计功能映射的图像表示和 Patch 训练策略。
5. **数据规模化**：利用更大的数据集或合成数据训练，FRIDU 能否进一步提升到实用级性能？当前训练仅使用有限形状集合，规模化训练可能释放扩散模型的更大潜力。

## 原文 PDF

![[paperPDFs/SGP_2025/FRIDU_Functional_Map_Refinement_with_Guided_Image_Diffusion.pdf]]
