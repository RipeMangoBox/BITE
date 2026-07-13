---
title: "UniPixie: Unified and Probabilistic 3D Physics Learning via Flow Matching"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniPixie_Unified_and_Probabilistic_3D_Physics_Learning_via_Flow_Matching.pdf
project_link: "https://unipixie.github.io/"
code_link: null
aliases:
- UniPixie
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: "标量控制参数 α ∈ [0,1]，线性插值于物体最软（α=0）和最硬（α=1）的两种物理状态之间，从而控制整个材料属性谱的连续生成。"
primary_logic: 将物理属性预测重新定义为是从视觉输入学习一个连续的、可控的条件分布，而非进行确定性回归。借助条件流匹配（CFM）学习从噪声到目标属性的映射，使得一个简单参数 α 即可控制生成多样的、物理上合理的材料场，并且通过共享编码器和专用解码头统一了多种物理求解器的参数生成。
claims:
- UNIPIXIE在MPM物理属性回归任务上，Young's Modulus的均方误差（MSE）较最强确定性基线PIXIE降低超过50%（绝对值从0.0250降至0.0091），在连续属性预测上达到最优。
- 单模型的统一架构在MPM、LBS、Spring-Mass三种物理引擎上均取得与专有模型竞争或更优的模拟视频重建质量（PSNR, SSIM, LPIPS），且推理速度比测试时优化基线快数个数量级。
- 通过调整α，UNIPIXIE能生成从柔软到坚硬连续变化的物理行为，其预测的材料参数分布与真实边界对齐，验证了连续谱建模的成功。
- PIXIEMULTIVERSE (MPM) 上 log E MSE = 0.0091 (UNIPIXIE avg)
---

# UniPixie: Unified and Probabilistic 3D Physics Learning via Flow Matching

> [!tip] 核心洞察
> 将物理属性预测重新定义为是从视觉输入学习一个连续的、可控的条件分布，而非进行确定性回归。借助条件流匹配（CFM）学习从噪声到目标属性的映射，使得一个简单参数 α 即可控制生成多样的、物理上合理的材料场，并且通过共享编码器和专用解码头统一了多种物理求解器的参数生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniPixie：基于流匹配的统一概率三维物理学习 |
| 英文题名 | UniPixie: Unified and Probabilistic 3D Physics Learning via Flow Matching |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Huang_UniPixie_Unified_and_Probabilistic_3D_Physics_Learning_via_Flow_Matching_CVPR_2026_paper.html) · [Project](https://unipixie.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | UNIPIXIE |
| Dataset | PIXIEMULTIVERSE |

> [!tip] 效果简介
> - PIXIEMULTIVERSE (MPM) 上，log E MSE 0.0091 (UNIPIXIE avg) vs 0.0250 (PIXIE) (减少 63.6%)。
> - PIXIEMULTIVERSE (LBS) 上，视频重建 PSNR (soft α=0.0) 优于 Vid2Sim (full) 及 Vid2Sim (fast) vs Vid2Sim (full) (在除 α=0.5 外的所有指标和硬度上均有领先)。
> - PIXIEMULTIVERSE (Spring‑Mass) 上，视频重建 PSNR/SSIM/LPIPS 显著优于 Spring‑Gaus 和 Spring‑Gaus (tuned) vs Spring‑Gaus (tuned) (在所有 α 上均为最佳)。

## 概要

从单张或多视角图像中推断物体的物理属性，是机器人操作、增强现实和物理仿真等任务的关键前提。然而，真实世界的物理属性存在固有的**视觉模糊性**：同一外观可对应从柔软到坚硬等一系列可能的材料状态。现有方法（如 **PIXIE**，Le et al., arXiv 2025）大多将物理属性预测建模为确定性回归问题，仅输出单一的点估计，完全忽略了这种一对多的物理可能性，导致仿真结果缺乏多样性与真实感。

针对这一瓶颈，本文提出 **UNIPIXIE**——一个基于条件流匹配（Conditional Flow Matching, CFM）的统一概率三维物理学习框架。其核心思想是将物理属性预测重新定义为**从视觉输入学习一个连续的、可控的条件分布**，而非确定性映射。通过引入标量控制参数 $\alpha \in [0,1]$，该参数在最软（$\alpha=0$）与最硬（$\alpha=1$）的物理状态之间进行线性插值，用户可直观地控制生成从柔软到坚硬连续变化的材料属性谱。

UNIPIXIE 在架构上采用**共享编码器 + 专用解码头**的设计：一个基于 Perceiver‑IO 风格的统一网格编码器将多视图 CLIP 特征压缩为与求解器无关的潜表示；随后，条件流匹配 Transformer 解码器以 $\alpha$ 为条件，将噪声转化为目标物理属性场，并通过三个专用解码头分别输出适用于**物质点法（MPM）、线性混合蒙皮（LBS）和弹簧‑质点（Spring‑Mass）**三种物理引擎的仿真参数。这一设计使得单一模型能够统一支持多种物理求解器，且推理速度比测试时优化基线快数个数量级。

在实验上，UNIPIXIE 在 PIXIEMULTIVERSE 数据集上取得了突破性结果：在 MPM 物理属性回归任务中，Young’s Modulus 的均方误差（MSE）较最强确定性基线 PIXIE 降低超过 50%（从 0.0250 降至 0.0091）；在 LBS 和 Spring‑Mass 求解器的视频重建质量上，单一统一模型均达到与各专有模型竞争或更优的 PSNR/SSIM/LPIPS 指标。通过调节 $\alpha$，模型能够生成从柔软到坚硬连续变化的物理行为，验证了连续谱建模的有效性。



### 视觉物理理解的核心瓶颈：从确定性回归到概率生成

从视觉输入推断物体的物理属性，并驱动下游仿真引擎生成可信的动态行为，是计算机视觉与物理仿真交叉领域的核心挑战。近年来，前馈神经网络（如 **PIXIE**，Le et al., arXiv 2025）已能直接从多视图图像预测材料参数，并输入物质点法（MPM）等求解器进行实时仿真。然而，这类方法存在一个根本性局限：**它们将物理属性预测建模为确定性回归问题，仅输出单一的点估计值**。

这一范式忽略了真实物理世界中的关键事实——**同一视觉外观可对应从最软到最硬等一系列可能的物理状态**。例如，一个外观相同的毛绒玩具，其实际填充材料的杨氏模量可能跨越数个数量级，而视觉系统本身无法唯一确定其精确的物理参数。确定性模型强制将这种“一对多”的映射压缩为单点输出，导致两个严重后果：

1. **预测的单一性**：模型只能给出一种固定的物理行为，无法表达物体在不同物理假设下的多样化响应。
2. **仿真的不真实性**：当点估计偏离真实物理属性时，仿真结果会出现不自然的刚体运动或灾难性坍塌（如 Figure 4 所示，基线方法常将柔性植物预测为过度刚硬，或将泰迪熊错误地坍塌）。

### 现有方法的缺口：连续物理谱建模的缺失

除确定性前馈方法外，另一类工作尝试借助视觉语言模型（VLM）进行零样本物理属性预测，如 **NeRF2Physics**（Zhai et al., CVPR 2024）和 **PUGS**（Shuai et al., ICRA 2025）。这些方法虽具灵活性，但预测精度有限，且常因材料分类错误而产生不合理的仿真结果。此外，**Vid2Sim**（Chen et al., CVPR 2025）和 **Spring-Gaus**（Zhong et al., ECCV 2024）等求解器专用方法在各自领域表现优异，但架构与特定物理引擎深度耦合，缺乏跨求解器的可移植性。

上述所有方法的共同缺陷是：**它们均未显式建模物理属性的连续分布**。真实物体的物理属性并非孤立点值，而是存在于一个由材料类别、制造工艺和环境条件共同决定的连续谱上。如何从视觉输入中学习这一连续谱，并通过简单、直观的控制机制进行遍历，是此前工作尚未触及的核心问题。

### 本文动机：统一、可控、概率化的物理学习

针对上述瓶颈，本文提出 **UNIPIXIE**——一个基于条件流匹配（Conditional Flow Matching, CFM）的统一概率三维物理学习框架。其核心动机体现在三个层面：

- **从点估计到连续分布**：将物理属性预测重新定义为学习一个以视觉输入为条件的连续条件分布，而非进行确定性回归。这使得模型能够生成从最软到最硬的全部合理物理状态。
- **标量控制的直观交互**：引入单一标量控制参数 $\alpha \in [0,1]$，通过在最软（$\alpha=0$）和最硬（$\alpha=1$）状态之间线性插值，实现对整个材料属性谱的连续、平滑遍历。
- **多求解器统一架构**：设计求解器无关的共享编码器与专用解码头，使单一模型能够同时为 MPM、线性混合蒙皮（LBS）和弹簧-质点（Spring-Mass）三种主流物理引擎生成仿真就绪的参数，突破专用模型的孤岛限制。



## 核心方法与创新机理

UNIPIXIE 的核心创新在于将三维物理属性预测从确定性回归重新定义为**可控的条件生成问题**，并通过统一的编码器-解码器架构同时服务于多种物理求解器。这一范式转变由以下四个关键“changed slots”支撑。

### 1. 预测范式：从单点估计到连续分布生成

现有前馈网络（如 **PIXIE**，Le et al., arXiv 2025）仅输出单一的材料属性点估计，忽略了真实世界中同一视觉外观可对应从最软到最硬等一系列可能的物理状态。这种确定性回归无法捕捉物理模糊性，导致预测结果单一且缺乏真实性。

UNIPIXIE 转而学习一个**以标量控制参数 α ∈ [0,1] 为条件的连续条件分布**。α 在最软（α=0）和最硬（α=1）两种物理状态之间线性插值，从而控制整个材料属性谱的连续生成。具体而言，目标属性由线性插值构造：

$$\pmb{y}_{\mathrm{target}} = (1 - \alpha) \pmb{y}_{\mathrm{min}} + \alpha \pmb{y}_{\mathrm{max}}$$

借助条件流匹配（Conditional Flow Matching, CFM），模型学习从噪声到目标属性的向量场，损失函数为：

$$\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{t, \boldsymbol{x}_0, y_{\mathrm{target}}, c} \lVert \boldsymbol{v}_{\boldsymbol{\theta}}(\boldsymbol{x}_t, t, c) - (y_{\mathrm{target}} - \boldsymbol{x}_0) \rVert_2^2$$

其中条件 c 包含控制参数 α。这一设计使得一个简单标量即可控制生成多样的、物理上合理的材料场。

**证据强度**：在 PIXIEMULTIVERSE (MPM) 基准上，UNIPIXIE 的 log E MSE 从 PIXIE 的 0.0250 降至 0.0091，降幅达 63.6%（Table 1, Section 4.1）。消融实验进一步确认，将 PIXIE 的确定性 U-Net 替换为条件流匹配生成框架是实现这一提升的关键因素。

### 2. 网络架构：从 U-Net 到 Perceiver-IO 编码器 + Flow Matching Transformer 解码器

PIXIE 采用经典的 U-Net 架构进行确定性预测，而 UNIPIXIE 设计了全新的生成式架构：

- **统一网格编码器（Unified Grid Encoder）**：将多视图 CLIP 密集特征聚合为 64³ 体素网格后，通过 3D 卷积下采样和 Perceiver-IO 风格的交叉/自注意力块，将体素特征编码为求解器无关的潜表示 $\boldsymbol{z}_{\mathrm{latent}} = \boldsymbol{\mathcal{E}}(\mathcal{G}_{\mathrm{feat}}) \in \mathbb{R}^{L \times C}$。每个块先执行潜查询到卷积特征的交叉注意力，再经过两层自注意力，从而将空间视觉特征蒸馏为紧凑的物理感知潜标记。
- **条件流匹配 Transformer 解码器（FMT Decoder）**：以 α 作为条件，通过自适应层归一化（AdaLN）调制的 Transformer 模块和流匹配损失，将噪声逐步转化为目标物理属性。AdaLN 机制使 α 的条件信息能够精细调控生成过程。

这一架构的优势在于：编码器产出的潜表示与具体求解器解耦，使得后续可灵活接入多种解码头。

### 3. 输出空间：从单点杨氏模量场到连续材料属性谱

PIXIE 仅输出单点的 Young's Modulus 场，而 UNIPIXIE 的输出随 α 连续变化，涵盖完整的材料属性谱。以 MPM 解码头为例：

$$\mathcal{D}_{\mathrm{MPM}} : (\boldsymbol{z}_{\mathrm{latent}}, \alpha) \to \mathcal{M}_{\mathrm{MPM}} = \{ (E_i, \nu_i, \rho_i, l_i) \}_{i=1}^K$$

为每个前景体素生成杨氏模量 E、泊松比 ν、密度 ρ 和材料类别 l，供 MPM 求解器直接使用。类似地，Spring-Mass 解码头生成锚点刚度向量 k 和全局柔软度 η：

$$\mathcal{D}_{\mathrm{Spring}} : (z_{\mathrm{latent}}, \alpha) \to m_{\mathrm{spring}} = (k, \eta)$$

通过调整 α，UNIPIXIE 能生成从柔软到坚硬连续变化的物理行为，其预测的材料参数分布与真实边界对齐（Section 4.4, Figure 5）。

### 4. 求解器支持：从单一 MPM 到统一多求解器架构

PIXIE 仅支持 MPM 求解器，而 UNIPIXIE 的单一统一架构可同时服务于 **MPM**、**LBS**（线性混合蒙皮）和 **Spring-Mass**（弹簧-质点）三种物理引擎。三个专用解码头——MPM 解码头、LBS 双重解码（HyperNetwork + FMT 解码）和 Spring-Mass 解码头——均由同一潜表示驱动，共享编码器但使用独立的解码参数。

**证据强度**：在 PIXIEMULTIVERSE 的多求解器视频重建任务中，UNIPIXIE 在 LBS 求解器上优于 **Vid2Sim**（Chen et al., CVPR 2025）的 full 和 fast 版本，在 Spring-Mass 求解器上显著优于 **Spring-Gaus**（Zhong et al., ECCV 2024）及其 tuned 版本（Table 2, Section 4.3）。同时，推理速度约为 21.6s（三求解器）或 ~12s（仅 MPM），比测试时优化基线快 25-200 倍（Vid2Sim full: 521s; Spring-Gaus: 4375s）。

### 创新总结

UNIPIXIE 的四项 changed slots 形成了完整的创新链条：**生成式范式**解决了物理模糊性的根本瓶颈，**Perceiver-IO + FMT 架构**为条件生成提供了技术载体，**连续属性谱输出**使可控生成成为现实，而**统一多求解器支持**则将这一能力推广到异构物理引擎，实现了“一次编码，多引擎部署”的便携性。



UNIPIXIE 是一个前馈式统一框架，将物理属性预测重新定义为从视觉输入学习连续、可控的条件分布。其整体 pipeline 由三个核心阶段串联构成：**视觉特征体素化 → 统一潜编码 → 多求解器条件生成**。图 2(a) 展示了这一完整数据流：多视图 RGB 图像首先经 CLIP 编码器提取密集特征，经体素化后形成 $64^3$ 的特征网格 $\mathcal{G}_{\mathrm{feat}}$；随后由统一网格编码器 $\boldsymbol{\mathcal{E}}$ 将其压缩为与求解器无关的潜表示；最后，三个并行的专用解码头从同一潜表示出发，在标量控制参数 $\alpha \in [0,1]$ 的调制下，分别生成适用于 MPM、LBS 和 Spring-Mass 物理引擎的仿真就绪参数。

### 视觉特征体素化

框架以多视图 CLIP 密集特征图为输入。这些特征图经过相机参数引导的反投影与插值，聚合为一个 $64^3$ 的体素网格 $\mathcal{G}_{\mathrm{feat}}$，作为后续所有模块的统一视觉前端。这一设计使得模型能够从多视角信息中捕获物体的三维几何与外观线索，为物理属性推理提供空间对齐的视觉基础。

### 统一网格编码器

统一网格编码器 $\boldsymbol{\mathcal{E}}$ 是框架的感知核心，其架构如图 2(b) 所示。它首先通过 3D 卷积对 $\mathcal{G}_{\mathrm{feat}}$ 进行下采样，随后采用 Perceiver-IO 风格的堆叠注意力块进行特征精炼：每个块先执行从可学习潜查询（latent queries）到卷积特征的交叉注意力，再经过两层自注意力变换。最终输出 $L \times C$ 的潜标记矩阵：

$$\boldsymbol{z}_{\mathrm{latent}} = \boldsymbol{\mathcal{E}}(\mathcal{G}_{\mathrm{feat}}) \in \mathbb{R}^{L \times C}$$

该潜表示的关键性质是**求解器无关**——它仅编码物体的物理感知信息，而不绑定任何特定物理引擎的参数化方式，从而为下游的多求解器便携性提供了统一接口。

### 条件流匹配生成与多求解器解码头

物理属性的生成由条件流匹配 Transformer（FMT）解码器驱动。其核心思想是将生成过程建模为从噪声到目标属性的向量场变换，并通过控制参数 $\alpha$ 实现连续谱采样。具体而言，目标属性 $\pmb{y}_{\mathrm{target}}$ 由物体最软（$\pmb{y}_{\mathrm{min}}$）和最硬（$\pmb{y}_{\mathrm{max}}$）状态线性插值构造：

$$\pmb{y}_{\mathrm{target}} = (1 - \alpha) \pmb{y}_{\mathrm{min}} + \alpha \pmb{y}_{\mathrm{max}}$$

FMT 解码器以潜标记 $\boldsymbol{z}_{\mathrm{latent}}$ 和 $\alpha$ 为条件，通过 AdaLN 调制的 Transformer 层学习从随机噪声 $\boldsymbol{x}_0$ 到 $\pmb{y}_{\mathrm{target}}$ 的向量场 $\boldsymbol{v}_{\boldsymbol{\theta}}$，训练时最小化条件流匹配损失：

$$\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{t, \boldsymbol{x}_0, y_{\mathrm{target}}, c} \lVert \boldsymbol{v}_{\boldsymbol{\theta}}(\boldsymbol{x}_t, t, c) - (y_{\mathrm{target}} - \boldsymbol{x}_0) \rVert_2^2$$

其中条件 $c$ 包含 $\alpha$ 和潜标记。推理时，只需改变 $\alpha$ 即可从同一噪声出发，生成从柔软到坚硬连续变化的物理属性场。

三个解码头共享上述 FMT 架构但参数独立，分别输出对应求解器的参数：

- **MPM 解码头**：为每个前景体素生成杨氏模量 $E_i$、泊松比 $\nu_i$、密度 $\rho_i$ 和材料类别 $l_i$，形成 $\mathcal{M}_{\mathrm{MPM}} = \{ (E_i, \nu_i, \rho_i, l_i) \}_{i=1}^K$。
- **LBS 解码头**：采用双重解码策略——HyperNetwork 生成基础参数，FMT 解码器进行精细化调整。
- **Spring-Mass 解码头**：生成 $N_a$ 个锚点的刚度向量 $k$ 和全局柔软度 $\eta$，即 $m_{\mathrm{spring}} = (k, \eta)$。

### 数据支撑：PIXIEMULTIVERSE

上述框架的训练依赖本文提出的 **PIXIEMULTIVERSE** 数据集（图 3）。该数据集的核心贡献在于为每个 3D 物体标注了**连续的材料属性范围** $[\pmb{y}_{\mathrm{min}}, \pmb{y}_{\mathrm{max}}]$，而非传统的确定性点值。标注流程采用 Actor-Critic VLM 半自动管线并辅以人工验证，覆盖 10 个语义类别，为 $\alpha$ 控制下的连续谱生成提供了监督基础。

### 框架的因果机制

整体框架的瓶颈突破在于将物理预测从**确定性回归**转变为**条件生成**。确定性基线（如 PIXIE 的 U-Net）仅输出单一材料属性点估计，无法捕捉“同一视觉外观可对应多种物理状态”的真实模糊性。UNIPIXIE 通过 $\alpha$ 这一标量控制旋钮，显式建模了物体从最软到最硬整个连续谱的映射，使得模型能够生成物理上合理的多样化行为，而非单一猜测。同时，统一的潜编码器设计使得同一视觉理解可以便携地服务于三种物理引擎，避免了为每个求解器单独训练专用模型的冗余。

### 补充图表

![[assets/figures/papers/paper_list_l2617_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_UniPixie_Unified/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the UNIPIXIE Framework. Our method generates controllable physical properties from visual input via a unified encoder-decoder architecture. (a) Overall Pipeline: Multi-view CLIP features are voxelized and processed by the unified encoder. The resulting solver-agnostic latent representation is then passed to three specialized decoders with a shared architecture but separate parameters, to produce parameters for specific physics engines: Material Point Method (MPM), Linear Blend Skinning (LBS), and Spring-Mass (SM). (b) Network Architecture: A Grid Encoder distills visual features from a convolutional backbone into latent tokens using a stack of cross-attention and self-attention...*

![[assets/figures/papers/paper_list_l2617_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_UniPixie_Unified/figures/003_Figure_3.jpg]]
*Figure 3: PIXIEMULTIVERSE: Annotation Pipeline and Data Overview. We introduce a dataset with annotated material property ranges for controllable generation. Our semi-automatic annotation pipeline employs an Actor-Critic VLM design with human verification, extending PIXIE [9], to label 10 semantic object classes (a). We show the resulting distributions of annotated ranges for MPM solver parameters: density (b), Poisson’s ratio (c), and Young’s modulus (d), which serve as the foundation for our multi-solver framework*



UNIPIXIE 的核心架构由三个关键模块构成：统一网格编码器、条件流匹配 Transformer 解码器，以及多求解器解码头。整个流水线从多视图 CLIP 特征出发，经由与求解器无关的潜表示，最终在标量控制参数 α 的驱动下生成适配不同物理引擎的仿真参数。

### 3.1 统一网格编码器

编码器的目标是构建一个**求解器无关的物理感知潜表示**。输入为多视图 CLIP 密集特征经体素化得到的 64³ 特征网格 $\mathcal{G}_{\mathrm{feat}}$。该网格首先通过 3D 卷积进行下采样，随后进入一组 Perceiver-IO 风格的交叉注意力与自注意力块。每个块中，一组可学习的潜查询（latent queries）先对卷积特征进行交叉注意力，再经过两层自注意力，最终将视觉特征压缩为一组 $L \times C$ 的潜标记：

$$\boldsymbol{z}_{\mathrm{latent}} = \boldsymbol{\mathcal{E}}(\mathcal{G}_{\mathrm{feat}}) \in \mathbb{R}^{L \times C}$$

这一潜表示不绑定任何特定求解器，为后续多求解器解码提供了统一的物理感知基础。

### 3.2 条件流匹配解码器

UNIPIXIE 将物理属性预测重新定义为**从噪声到目标属性的条件生成**问题，而非确定性回归。其核心控制机制是一个标量参数 $\alpha \in [0,1]$，通过在最软（$\alpha=0$）和最硬（$\alpha=1$）的物理属性边界之间线性插值，构造条件生成的目标：

$$\pmb{y}_{\mathrm{target}} = (1 - \alpha) \pmb{y}_{\mathrm{min}} + \alpha \pmb{y}_{\mathrm{max}}$$

解码器采用条件流匹配 Transformer（Flow Matching Transformer, FMT）架构。它以潜标记 $\boldsymbol{z}_{\mathrm{latent}}$ 和 $\alpha$ 作为条件 $c$，通过自适应层归一化（AdaLN）将条件信息注入 Transformer 块，学习一个向量场 $\boldsymbol{v}_{\boldsymbol{\theta}}$，将噪声 $\boldsymbol{x}_0$ 逐步转化为目标属性 $\pmb{y}_{\mathrm{target}}$。训练目标为条件流匹配损失：

$$\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{t, \boldsymbol{x}_0, y_{\mathrm{target}}, c} \lVert \boldsymbol{v}_{\boldsymbol{\theta}}(\boldsymbol{x}_t, t, c) - (y_{\mathrm{target}} - \boldsymbol{x}_0) \rVert_2^2$$

其中 $t$ 为扩散时间步，$\boldsymbol{x}_t$ 为沿概率路径的中间状态。该损失直接回归从当前状态指向目标状态的向量场，使模型学会在给定 $\alpha$ 下生成对应的物理属性。

### 3.3 多求解器解码头

同一潜表示 $\boldsymbol{z}_{\mathrm{latent}}$ 驱动三个独立的解码头，分别输出不同物理引擎所需的仿真参数：

**MPM 解码头**为每个前景体素生成完整的材料属性四元组——杨氏模量 $E_i$、泊松比 $\nu_i$、密度 $\rho_i$ 和材料类别 $l_i$：

$$\mathcal{D}_{\mathrm{MPM}} : (\boldsymbol{z}_{\mathrm{latent}}, \alpha) \to \mathcal{M}_{\mathrm{MPM}} = \{ (E_i, \nu_i, \rho_i, l_i) \}_{i=1}^K$$

**LBS 解码头**采用双重解码策略：一个 HyperNetwork 从潜表示生成网络权重，再由 FMT 解码器在 $\alpha$ 条件下输出蒙皮权重与刚度参数，供线性混合蒙皮求解器使用。

**Spring-Mass 解码头**生成 $N_a$ 个锚点的刚度向量 $k$ 和全局柔软度参数 $\eta$：

$$\mathcal{D}_{\mathrm{Spring}} : (z_{\mathrm{latent}}, \alpha) \to m_{\mathrm{spring}} = (k, \eta)$$

三个解码头共享统一的编码器与潜表示，仅解码器参数独立，实现了单一模型对 MPM、LBS 和 Spring-Mass 三种物理引擎的统一支持。



## 实验与关键发现

### 4.1 物理属性回归：从点估计到连续谱生成

UNIPIXIE 的核心主张是将物理属性预测从确定性回归重构为条件生成，从而显式建模同一视觉外观下材料属性的模糊性。Table 1 的定量结果直接验证了这一范式转变的有效性。

![[assets/figures/papers/paper_list_l2617_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_UniPixie_Unified/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison of Physical Property Regression. UNIPIXIE sets a new state-of-the-art in continuous property prediction, reducing Young’s Modulus MSE by over 50% compared to the specialized PIXIE. We compare our generative models (averaged across*

在 PIXIEMULTIVERSE 数据集上，UNIPIXIE（取 α ∈ {0.0, 0.5, 1.0} 的平均值）在杨氏模量（log E）上的均方误差（MSE）达到 **0.0091**，而最强的确定性基线 **PIXIE**（Le et al., arXiv 2025）的 MSE 为 0.0250——UNIPIXIE 将误差降低了 **63.6%**（绝对值下降 0.0159）。这一超过 50% 的误差缩减构成了全文最关键的定量证据，直接支撑了“生成式建模是捕捉物理模糊性的关键”这一核心论点。

值得注意的是，PIXIE 在离散材料分类准确率上仍保持微弱优势（Table 1），这表明确定性回归在需要明确类别边界的任务中仍有其价值。但在连续物理参数（密度 log ρ、泊松比 ν）的预测上，UNIPIXIE 全面领先，验证了流匹配框架对连续分布建模的天然适配性。

**消融分析**：将 PIXIE 的确定性 U‑Net 替换为条件流匹配生成框架，构成了最直接的消融实验——log E MSE 从 0.0250 降至 0.0091，证明性能增益并非来自更强的编码器或更多的数据，而是源自预测范式从“点估计”到“分布建模”的根本改变。

### 4.2 多求解器统一架构的视频重建质量

UNIPIXIE 的另一关键贡献是单一统一模型同时服务于三种截然不同的物理求解器：MPM、LBS 和 Spring‑Mass。Table 2 报告了各求解器在视频重建保真度（PSNR、SSIM、LPIPS）上的对比结果，覆盖从柔软（α=0.0）到坚硬（α=1.0）的完整物理谱。

![[assets/figures/papers/paper_list_l2617_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_UniPixie_Unified/figures/006_Table_2.jpg]]
*Table 2: Solver-specific Quantitative Comparison. Our single unified UNIPIXIE model achieves performance competitive with or superior to specialized state-of-the-art methods across diverse physics solvers, while being orders of magnitude faster than test-time optimization baselines. We evaluate video reconstruction fidelity (PSNR, SSIM, LPIPS) across the full physical distribution: soft (α = 0.0), mid (α = 0.5), and stiff (α = 1.0). The ± denotes standard deviation. Best results within each solver category are bolded*

**MPM 求解器**：UNIPIXIE 在连续属性预测上达到最优，其模拟视频质量与专有模型 PIXIE 竞争。

**LBS 求解器**：与 **Vid2Sim**（Chen et al., CVPR 2025）的 full 和 fast 版本相比，UNIPIXIE 在除 α=0.5 外的所有硬度等级和指标上均取得领先。Vid2Sim 是一种基于线性混合蒙皮的简化仿真系统辨识方法，其 full 版本采用测试时优化，单物体推理耗时 521 秒；而 UNIPIXIE 以纯前馈方式生成 LBS 参数，推理时间仅为统一推理的一部分。

**Spring‑Mass 求解器**：UNIPIXIE 在所有 α 值上均显著优于 **Spring‑Gaus**（Zhong et al., ECCV 2024）及其针对本数据集调优的 tuned 版本。Spring‑Gaus 的测试时优化耗时长达 4375 秒/物体，而 UNIPIXIE 的完整三求解器推理仅需约 **21.6 秒**（单 MPM 解码约 12 秒），速度提升达 **25–200 倍**。

这一效率优势具有重要的实际意义：测试时优化基线（Vid2Sim full、Spring‑Gaus）虽然可以通过反复仿真-比较-调整获得较高质量，但其计算成本使其难以应用于交互式或大规模场景。UNIPIXIE 以前馈方式一次性生成所有求解器参数，在保持竞争性甚至更优的重建质量的同时，将推理时间压缩了两个数量级以上。

### 4.3 可控生成与物理谱的连续性验证

Figure 5 和 Section 4.4 的定性分析验证了 α 参数对物理行为的连续控制能力。通过调整 α ∈ [0,1]，UNIPIXIE 生成的模拟结果呈现从柔软到坚硬的平滑过渡：低 α 值下物体表现出大幅变形和缓慢回弹，高 α 值下则呈现刚性运动和快速恢复。预测的材料参数分布与数据集标注的真实边界对齐，证明模型成功学习了最软（α=0）到最硬（α=1）之间的连续谱，而非仅记忆离散的端点值。

![[assets/figures/papers/paper_list_l2617_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_UniPixie_Unified/figures/007_Figure_5.jpg]]
*Figure 5: Controllable Multi-Solver Generation vs. Specialists. (a) UNIPIXIE (Ours): Our model learns a smooth soft-to-stiff mapping for diverse solvers, resulting in intuitive deformation changes. (b) Specialists: The simulation quality from our single unified model is comparable to that of three solver-specific baselines (PIXIE, Vid2Sim, Spring-Gaus), confirming its portability and effectiveness*

与零样本基线 **NeRF2Physics**（Zhai et al., CVPR 2024）和 **PUGS**（Shuai et al., ICRA 2025）的定性对比（Figure 4）进一步揭示了确定性或基于 VLM 的方法的典型失效模式：这些方法常为柔性物体（如薰衣草、树木）预测过高的杨氏模量，导致不自然的刚性运动；PUGS 还可能出现严重的材料分类错误，使物体（如泰迪熊）不真实地坍塌。UNIPIXIE 通过建模完整的材料属性分布，避免了这些因单点预测偏差导致的灾难性失败。

![[assets/figures/papers/paper_list_l2617_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_UniPixie_Unified/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Comparison of Predicted Dynamics. When evaluated at its midpoint (α = 0.5), our model generates physically plausible simulations competitive with the specialist PIXIE and avoid the failure modes of other baselines. This figure compares a midsimulation frame (left) and the final state (right) for each method. We observe that NeRF2Physics and PUGS often produce unnaturally rigid motion for flexible objects like the lavender plant (A) and tree (B), a result of predicting an overly high Young’s modulus. Furthermore, PUGS can suffer from critical material misclassification, causing the teddy bear (C) to unrealistically collapse. While baselines can occasionally yield plausible dynami...*

### 4.4 局限性与失效模式

尽管 UNIPIXIE 在连续谱建模和多求解器统一上取得了显著进展，但其当前设计存在明确边界：

1. **一维控制参数的局限性**：α 仅沿单一维度（软硬程度）进行插值，无法表达各向异性材料（如木材的纹理方向依赖性）、塑性变形、断裂等需要多维参数空间的复杂物理现象。这是方法本身的容量限制，而非数据或训练的不足。

2. **遮挡区域的属性估计缺失**：当前框架仅对可见表面提取的视觉特征进行编码，未涉及被遮挡或内部区域的物理属性推理。对于部分遮挡的物体或需要估计内部材料分布的场景，这一限制可能导致模拟失真。

3. **分布外泛化未验证**：实验仅在 PIXIEMULTIVERSE 的 10 个语义类别上进行，模型对全新物体类别或极端材料组合的泛化能力尚需进一步检验。

这些局限同时指向了明确的研究方向：将一维连续谱扩展至多维材料流形，以及引入遮挡推理机制以实现完整的体积物理属性估计。



## 定位与知识库关联

### 1. 与基线方法的关系

UNIPIXIE 的核心创新在于将物理属性预测从**确定性回归**重新定义为**条件生成**，这使其与现有方法形成了清晰的范式边界。

**确定性前馈基线**：**PIXIE**（Le et al., arXiv 2025）是本工作最直接的对比对象。PIXIE 采用 U-Net 架构，从多视图视觉输入直接回归单一的杨氏模量场，输出的是物理属性的点估计。UNIPIXIE 在 PIXIE 的基础上进行了根本性的范式转换：用基于 Perceiver-IO 的统一编码器替代 U-Net，用条件流匹配 Transformer 解码器替代确定性回归头，从而将输出从单点预测扩展为由标量参数 α 控制的连续材料属性谱。实验表明，仅将 PIXIE 的确定性 U-Net 替换为条件流匹配生成框架，即可使杨氏模量对数均方误差（log E MSE）从 0.0250 降至 0.0091（降幅 63.6%），这一消融实验直接证明了生成式建模对捕捉物理模糊性的关键作用（Table 1）。

**零样本物理理解基线**：**NeRF2Physics**（Zhai et al., CVPR 2024）和 **PUGS**（Shuai et al., ICRA 2025）均利用视觉语言模型（VLM）进行零样本物理属性预测，无需针对特定物理求解器进行训练。然而，这类方法缺乏对连续物理谱的显式建模能力，在定性对比中常产生物理上不自然的刚性运动——例如对柔性物体（薰衣草、树木）预测过高的杨氏模量，或在材料分类错误时导致物体非真实地坍塌（Figure 4）。UNIPIXIE 通过显式学习从最软到最硬的条件分布，避免了这些失效模式，同时保持了前馈网络的推理效率。

**专用求解器基线**：**Vid2Sim**（Chen et al., CVPR 2025）和 **Spring-Gaus**（Zhong et al., ECCV 2024）分别针对线性混合蒙皮（LBS）和弹簧-质点系统进行了专门设计。Vid2Sim 包含 full 和 fast 两个版本，Spring-Gaus 也提供了针对本数据集调优的 tuned 版本。UNIPIXIE 以单一统一模型在三个求解器（MPM、LBS、Spring-Mass）上均取得与这些专用方法竞争或更优的视频重建质量（PSNR、SSIM、LPIPS），同时推理速度比测试时优化基线快 25–200 倍（Table 2）。这表明统一架构并未牺牲各求解器的模拟精度。

### 2. 适用边界与局限

UNIPIXIE 的适用边界由以下几个维度界定：

**连续谱建模的维度限制**：当前方法仅沿一维材料硬度连续谱（α ∈ [0,1]）进行建模，通过在最软（α=0）和最硬（α=1）两种物理状态之间线性插值构造目标属性。这一设计有效捕捉了物理模糊性的主要轴，但未涉及多维材料性质的流形生成，如各向异性、塑性、黏弹性等复杂本构关系。扩展至多维材料流形需要重新设计条件空间和对应的标注策略。

**遮挡区域的物理属性估计**：UNIPIXIE 依赖多视图 CLIP 特征进行体素化，其物理感知的潜表示主要编码了可见表面的视觉信息。对于因自遮挡或场景遮挡而不可见的区域，当前方法未提供专门的物理属性推断机制。这是一个开放问题，可能需要结合三维几何先验或物理补全策略。

**数据集依赖与标注成本**：UNIPIXIE 的训练依赖于 PIXIEMULTIVERSE 数据集，该数据集采用 Actor-Critic VLM 半自动标注管线并辅以人工验证，为 10 个语义类别标注了材料属性范围。这一标注策略虽然比纯人工标注高效，但仍需要领域专家参与验证，且标注质量受限于 VLM 的物理推理能力。扩展到新物体类别或新物理求解器时，需要相应的标注工作。

**求解器可移植性的前提**：UNIPIXIE 的统一架构通过共享编码器和专用解码头支持多种求解器，但每个新求解器需要设计相应的解码头结构（如 MPM 的体素级参数输出、LBS 的 HyperNetwork + FMT 双重解码、Spring-Mass 的锚点刚度和全局柔软度输出）。求解器之间的参数空间差异越大，解码头的设计复杂度越高。

### 3. 开放问题

UNIPIXIE 开辟了概率三维物理学习的新方向，同时留下了若干值得探索的开放问题：

**多维材料流形的条件生成**：当前 α 参数控制的是单一维度的软硬连续谱。能否将条件空间扩展为多维流形，以支持各向异性刚度、塑性屈服准则、黏弹性松弛时间等多维材料属性的连续生成？这需要重新设计条件机制和流匹配目标，以及相应的数据集标注方案。

**遮挡区域的物理属性推断**：如何估计因遮挡而不可见区域的物理属性？可能的方向包括：利用三维几何补全网络预测缺失区域的体素特征，或通过物理一致性约束（如力平衡、运动连续性）推断不可见部分的材料参数。

**物理求解器的自适应解码**：当前每个求解器需要手工设计专用解码头。能否设计一种自适应解码机制，使模型能够根据求解器的物理方程自动调整参数输出格式？这涉及对物理先验的结构化编码和跨求解器的参数空间对齐。

**从模拟视频到物理属性的逆向推理**：UNIPIXIE 目前从静态视觉输入预测物理属性。若能结合物体在受力下的动态视频作为额外条件，可能进一步提升物理属性估计的准确性，并扩展至更复杂的材料行为（如断裂、塑性变形）的识别。

**物理属性谱的细粒度控制与编辑**：当前 α 参数提供全局的软硬控制。是否可以实现空间变化的局部硬度控制（如物体不同区域具有不同的 α 值），以支持更精细的物理行为编辑？这需要在条件流匹配框架中引入空间变化的条件信号。



## 原文 PDF

![[paperPDFs/CVPR_2026/UniPixie_Unified_and_Probabilistic_3D_Physics_Learning_via_Flow_Matching.pdf]]
