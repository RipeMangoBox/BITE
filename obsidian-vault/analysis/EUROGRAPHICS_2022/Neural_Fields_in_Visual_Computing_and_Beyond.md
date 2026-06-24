---
title: "Neural Fields in Visual Computing and Beyond"
type: paper
paper_level: A
venue: EUROGRAPHICS
year: 2022
pdf_ref: paperPDFs/EUROGRAPHICS_2022/Neural_Fields_in_Visual_Computing_and_Beyond.pdf
project_link: https://neuralfields.cs.brown.edu/
aliases:
- SSTNF
- NFVCB
tags:
- EUROGRAPHICS_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过建立由“场量、条件、前向映射、网络架构、编辑”五大类技术构成的统一框架，可以系统化地描述和比较不同方法。"
primary_logic: "将神经场形式化为函数Φ(x; Θ)，通过组合不同的条件机制、离散-连续混合表示、可微分前向映射和架构选择，可以有效解决各类病态视觉计算反问题。"
claims:
- "神经场是部分或完全由神经网络参数化的场。"
- "本文调查了超过250篇论文，识别出五大类技术：先验学习与条件、混合表示、前向映射、网络架构、编辑。"
- "建立了一个社区驱动的动态数据库网站，支持搜索、过滤和可视化。"
- "神经场方法在2019年后在视觉计算领域呈爆发式增长。"
---

# Neural Fields in Visual Computing and Beyond

> [!tip] 核心洞察
> 将神经场形式化为函数Φ(x; Θ)，通过组合不同的条件机制、离散-连续混合表示、可微分前向映射和架构选择，可以有效解决各类病态视觉计算反问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视觉计算及其它领域的神经场综述 |
| 英文题名 | Neural Fields in Visual Computing and Beyond |
| 会议/期刊 | EUROGRAPHICS 2022 |
| Links | [paper](https://arxiv.org/abs/2111.11426); [Project](https://neuralfields.cs.brown.edu/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Systematic Survey and Taxonomy of Neural Fields |
| Dataset |  |

## 概述

神经场（Neural Fields）是指部分或完全由神经网络参数化的场（Definition 2, Section 1.1），其核心形式为 $q = \Phi(x; \Theta)$，即由参数 $\Theta$ 定义的神经网络 $\Phi$ 根据时空坐标 $x$ 输出场量 $q$。近年来，神经场在视觉计算领域呈现爆发式增长——仅最近两年即有超过250篇相关论文涌现（Figure 2），涵盖三维重建、数字人、生成模型、图像处理、压缩、机器人等广泛的应用方向。

然而，该领域的快速发展也带来了显著瓶颈：**论文数量激增但缺乏统一的数学公式和术语体系，导致概念重复、方法比较困难**。本综述正是针对这一问题，通过对250余篇论文的系统调查，提出了一种统一的技术分类框架。其核心洞察在于：将神经场形式化为 $\Phi(x; \Theta)$ 之后，通过组合不同的**条件机制**、**离散-连续混合表示**、**可微分前向映射**和**网络架构**选择，可以有效解决各类病态视觉计算反问题。

具体而言，本工作识别出五大类关键技术（Table 2）：
- **先验学习与条件（Section 2）**：如何将观测信息注入神经场，包括编码器推理、自解码器推理、全局与局部条件等机制；
- **混合表示（Section 3）**：通过离散数据结构（如稀疏体素网格、网格、包围盒）与神经网络结合，平衡效率与表达能力；
- **前向映射（Section 4）**：将重建域映射到传感器域的可微分算子，如体渲染、球追踪、Radon变换等；
- **网络架构（Section 5）**：激活函数选择、位置编码、网络平铺等设计对高频信号拟合的影响；
- **编辑与操控（Section 6）**：通过参数编辑或坐标重映射对神经场进行可控修改。

在方法谱系与知识库定位上，本综述并非提出新的算法，而是构建了一个**系统化的文献调查与分类体系**，并配套开发了**社区驱动的动态数据库网站**（Figure 1），支持搜索、过滤和可视化功能，旨在为研究者提供可扩展的知识基础设施。该网站允许社区持续贡献新论文，以缓解静态综述快速过时的问题。

需要指出的是，由于本文是综述性质，未进行原创实验，所引用的性能数据均来自原始论文；同时，许多被引工作的设计选择缺乏严格的消融研究，这一点在解读具体方法时需加以注意。

## 背景与动机

### 神经场：从物理概念到视觉计算范式

场是物理与数学中描述时空连续分布量的基本概念——标量场、向量场、张量场在电磁学、流体力学、广义相对论等领域已有逾百年历史。在视觉计算中，类似的思想同样普遍存在：二维图像可视为像素网格上的颜色场，三维形状可表达为符号距离场（SDF）或占用场，而动态场景则可建模为时变辐射场（Table 1）。

神经场将这一经典概念与深度学习结合，其形式化定义为：**一个部分或完全由神经网络参数化的场**（Definition 2, Section 1.1）。具体而言，神经场将时空坐标 $\mathbf{x}$ 映射到场量 $\mathbf{q}$：

$$q = \Phi(\mathbf{x}; \Theta)$$

其中 $\Phi$ 通常为多层感知机（MLP），其激活函数具有良好定义的梯度。凭借解析可微性、梯度下降优化和过参数化特性，神经场在回归复杂高维信号方面展现出显著优势。

### 爆发式增长与碎片化困境

尽管神经场的思想可追溯至二十年前，但其在视觉计算领域的真正爆发集中在近两到三年（Figure 2）。本综述调查了超过250篇相关论文，涵盖二维图像处理、三维场景重建、生成模型、数字人、压缩、机器人学等众多应用方向。

然而，这一快速增长也带来了显著问题：**领域缺乏统一的数学公式和术语体系**。不同工作常以不同名称描述本质上相似的技术组件，导致概念重复和交流壁垒。研究者难以系统性地定位自身工作在整体技术谱系中的位置，也难以在不同方法间进行公平比较。

### 本文动机与统一框架

针对上述碎片化问题，本文的核心贡献是建立了一个**由五大技术类构成的统一分类框架**（Table 2），将神经场方法解耦为可组合的技术模块：

1. **先验学习与条件**（Section 2）：如何从数据中学习先验，并在推理时将观测编码为条件变量。
2. **混合表示**（Section 3）：如何将神经网络与离散数据结构（体素网格、网格、图集等）结合，平衡效率与表达能力。
3. **前向映射**（Section 4）：如何将重建域映射到传感器域，使监督信号可微分地反传。
4. **网络架构**（Section 5）：激活函数、位置编码、网络结构等对场表达能力的系统性影响。
5. **编辑与操控**（Section 6）：如何通过参数编辑或坐标变换对已训练的神经场进行后处理。

该框架的核心洞察在于：**通过组合不同的条件机制、离散-连续混合表示、可微分前向映射和架构选择，可以有效解决各类病态视觉计算反问题**。典型的神经场算法流程（Figure 3）可概括为：采样时空坐标 → 神经网络预测场量 → 前向映射至传感器域 → 计算重建误差并反向传播。

此外，本文还构建了一个**社区驱动的动态数据库网站**，支持搜索、过滤、文献管理和可视化功能（Figure 1），旨在持续追踪该领域的快速演进，缓解静态综述固有的时效性问题。

## 核心创新

本工作的核心创新并非提出一种新的神经场算法，而是构建了一个系统化的分类学框架与社区驱动的知识基础设施，以解决该领域因论文爆发式增长而导致的术语碎片化和概念重复问题。其创新点可归纳为三个层面：

### 1. 统一的形式化框架

该综述将神经场方法解构为五个正交的技术维度（Table 2），并用统一的数学语言加以定义，从而将超过250篇论文纳入一个可比较的体系：

- **先验学习与条件（Section 2）**：将编码器推理（$z = E(O)$）、自解码器优化（$z = \arg\min L(z, \Theta)$）以及超网络、元学习等条件机制统一为对神经场函数 $\Phi(x; \Theta)$ 的参数化方式。
- **混合表示（Section 3）**：通过“网络平铺”（$\mathbf{q} = \Phi(\mathbf{x}, g(\mathbf{x}))$）和“嵌入”（$\mathbf{q} = \Phi(\mathbf{x}, \Psi(g(\mathbf{x})))$）两个公式，统一描述了离散数据结构（稀疏体素网格、网格、包围盒等）与连续神经网络的组合方式。
- **前向映射（Section 4）**：将重建域到传感器域的映射（体积渲染、球追踪、Radon变换等）抽象为可微分算子，并通过统一的优化目标 $\underset{\Theta}{\operatorname{argmin}} \int F(\Phi(\mathbf{x}_{\text{recon}})) - \Omega(\mathbf{x}_{\text{sens}})$ 进行形式化。
- **网络架构（Section 5）**：系统梳理了位置编码（如正弦编码 $\gamma_{(2i)}(x) = \sin(2^{i-1}\pi x)$）、激活函数选择等架构设计对频谱特性的影响。
- **编辑（Section 6）**：归纳了参数编辑和坐标重映射两类操控神经场的方式。

这种解耦使得研究者可以清晰地识别不同方法在哪些维度上做出了贡献，从而避免“重新发明轮子”。

### 2. 社区驱动的动态知识库

该综述的另一个关键创新是配套的在线数据库网站（Figure 1）。该网站支持搜索、过滤、文献管理和可视化功能，并允许社区提交新论文。这一设计直接回应了静态综述的核心局限——领域发展过快导致内容迅速过时。通过将综述从“一次性出版物”转变为“持续更新的知识基础设施”，该工作为后续的公平比较和系统性研究提供了可扩展的平台。

### 3. 对病态反问题的统一视角

该综述将神经场在视觉计算中的广泛应用——从3D重建、数字人到生成模型和压缩——统一为“利用神经网络的正则化能力求解病态反问题”这一核心范式。通过组合不同的条件机制（提供先验）、混合表示（平衡效率与表达力）和前向映射（连接观测），研究者可以针对特定任务构建神经场解决方案。这一视角揭示了各子领域方法之间的深层联系，为跨领域迁移提供了理论指导。

需要指出，由于本文是综述性质的工作，上述创新体现在知识组织与形式化层面，而非提出新的网络结构或训练算法。其价值在于通过统一术语和分类，降低了该领域的交流成本，并为未来的公平比较和系统性改进提供了基准框架。

## 整体框架

本综述将神经场（Neural Field）的完整技术流程抽象为一个统一的前馈算法框架，如图3所示。该框架的核心是将一个病态反问题（ill-posed inverse problem）分解为三个可微分的阶段：**坐标采样与场量预测**、**前向映射**、以及**传感器域损失计算**。

### 核心形式化定义

神经场被明确定义为一个部分或全部由神经网络参数化的场（Definition 2, Section 1.1）。其基本形式为：

$$q = \Phi(x; \Theta)$$

其中，$x$ 表示时空坐标，$\Theta$ 为网络参数，$q$ 为预测的场量（如颜色、密度、符号距离等）。这一简洁的数学抽象构成了整个方法谱系的基石。

### 三阶段流程

1. **重建域预测**：在重建域 $\mathcal{X}$ 中采样时空坐标 $x_{recon}$，输入神经网络 $\Phi$ 产生场量。这一阶段的核心挑战在于如何使网络有效表达高频细节——这引出了**网络架构**（Section 5）中的位置编码、激活函数选择等关键技术。

2. **前向映射**：通过可微分的前向映射 $F$，将重建域中的场量变换到传感器域 $\mathcal{S}$，得到预测的传感器观测 $\hat{\Omega}(x_{sens})$。前向映射的类型取决于具体任务：体积渲染（NeRF）、球追踪（SDF渲染）、Radon/Fourier变换（CT/MRI重建）等。这一阶段是连接隐式场表示与显式观测监督的桥梁。

3. **损失计算与优化**：在传感器域计算预测值 $\hat{\Omega}$ 与真实观测 $\Omega$ 之间的重建误差，通过梯度反向传播端到端地优化网络参数 $\Theta$ 及其他可学习组件。优化目标可统一表达为：

$$\underset{\Theta}{\operatorname{argmin}} \int_{(x_{recon}, x_{sens}) \in (\mathcal{X}, \mathcal{S})} \left\| F(\Phi(x_{recon})) - \Omega(x_{sens}) \right\|$$

### 五大技术类别

为系统化地梳理这一流程中的设计选择，综述识别出五类核心技术（Table 2），每类技术解决流程中特定的瓶颈：

| 技术类别 | 解决的核心问题 |
|---------|---------------|
| **先验学习与条件** (Section 2) | 如何利用数据先验加速收敛、实现泛化？ |
| **混合表示** (Section 3) | 如何突破单一全局MLP的容量与效率限制？ |
| **前向映射** (Section 4) | 如何将隐式场与具体传感器观测关联？ |
| **网络架构** (Section 5) | 如何设计网络以克服坐标MLP的频谱偏差？ |
| **编辑与操控** (Section 6) | 如何对已训练的神经场进行编辑、变形、组合？ |

### 条件机制的关键分化

在流程的输入端，条件机制决定了神经场如何响应不同的数据实例。综述区分了两种根本不同的推理范式（Figure 4）：

- **编码器推理**：通过一个额外的编码器网络 $E$ 直接从观测 $O$ 预测潜变量 $z = E(O)$，实现摊销推理（amortized inference），推理速度快但需要设计合适的编码器架构。
- **自解码推理**：放弃编码器，为每个数据实例独立优化一个潜变量 $z_i = \arg\min \mathcal{L}(z, \Theta)$，灵活但推理时需额外优化步骤。

进一步地，条件的作用范围分为**全局条件**（单一潜码 $z$ 作用于所有坐标）和**局部条件**（通过离散数据结构 $g(x)$ 为不同坐标区域提供不同的潜码 $z = g(x)$），后者是混合表示的理论基础（Figure 5）。

### 框架的可扩展性

该框架的模块化设计使得不同技术可以灵活组合。例如，一个典型的NeRF变体可能同时使用：位置编码（架构类）、体积渲染（前向映射类）、多尺度哈希网格（混合表示类）、以及元学习初始化（先验学习类）。综述配套的社区网站（Figure 1）通过可搜索数据库支持研究者按这些技术维度筛选和比较超过250篇论文，从而应对该领域论文快速增长带来的信息过载问题。

**证据强度说明**：上述框架描述基于综述对超过250篇论文的系统性归纳（Figure 2展示了该领域在2019年后的爆发式增长），五类技术的划分由Table 2明确锚定，核心公式 $q = \Phi(x; \Theta)$ 来自Section 1.1的Definition 2，优化目标来自Section 4的Equation (5)。所有技术细节均可通过原文锚点追溯验证。

## 核心模块与公式推导

### 神经场的形式化定义

神经场的核心模块始于一个统一的形式化定义。一个神经场被定义为一个部分或完全由神经网络参数化的场（Definition 2, Section 1.1）。其基本形式为：

$$q = \Phi(x; \Theta)$$

其中 $q$ 表示场量（如颜色、密度、有符号距离等），$x$ 为时空坐标，$\Theta$ 为神经网络 $\Phi$ 的参数。这一简洁的公式构成了所有后续技术模块的基石。

### 典型算法流程

一个典型的神经场算法流程（Figure 3）包含以下关键模块：
1. **坐标采样**：在重建域的时空坐标上进行采样。
2. **场量预测**：将坐标输入神经网络 $\Phi$，产生场量值。
3. **前向映射**：通过可微分前向映射 $F$，将重建域的量映射到传感器域。
4. **损失计算**：将映射后的值与传感器观测 $\Omega$ 进行比较，计算重建误差。

该流程的核心优化目标可表述为：

$$\underset{\Theta}{\operatorname{argmin}} \int_{(\mathbf{x}_{\text{recon}}, \mathbf{x}_{\text{sens}}) \in (\mathcal{X}, \mathcal{S})} \left. F(\Phi(\mathbf{x}_{\text{recon}})) - \Omega(\mathbf{x}_{\text{sens}}) \right.$$

此公式（Equation 5, Section 4）揭示了神经场解决反问题的本质机制：通过最小化前向映射后的神经场输出与传感器观测之间的差异来重建场。

### 条件机制模块

条件机制是使神经场能够泛化到不同实例的关键模块。其技术路线分为两类：

**编码器推理**（Figure 4A）：通过前馈编码器直接产生隐变量：
$$z = E(O)$$
其中 $E$ 为编码器网络，$O$ 为观测数据。编码器参数与条件神经场联合优化。

**自解码器推理**（Figure 4B）：通过优化直接获得隐变量：
$$z = \arg\min L(z, \Theta)$$
每个实例的隐编码 $z_i$ 与共享的神经场参数 $\Theta$ 联合优化，无需额外的编码器网络。

在条件注入方式上，拼接（concatenation）等价于定义一个仿射函数 $\Psi(z) = b$，将隐编码映射为网络第一层的偏置向量。而超网络则直接参数化 $\Psi$ 为一个神经网络，输出完整的神经场参数 $\Theta$。

### 混合表示模块

混合表示模块将神经场与离散数据结构相结合，以分解输入坐标空间（Section 3）。其核心机制包含两种范式：

**网络分片**（Network Tiling）：
$$\mathbf{q} = \Phi(\mathbf{x}, \Theta) = \Phi(\mathbf{x}, g(\mathbf{x}))$$
通过查找函数 $g(\mathbf{x})$ 从数据结构中获取对应区域的网络参数，不同区域存储独立的参数。

**嵌入**（Embedding）：
$$\mathbf{q} = \Phi(\mathbf{x}, \Theta) = \Phi(\mathbf{x}, \Psi(\mathbf{z})) = \Phi(\mathbf{x}, \Psi(g(\mathbf{x})))$$
先将坐标映射为局部嵌入 $\mathbf{z} = g(\mathbf{x})$，再通过函数 $\Psi$ 将嵌入映射为网络参数。这种设计使模型能在保持全局参数共享的同时，获得局部自适应性。

### 先验学习模块

基于梯度的元学习为神经场提供了快速适应新实例的能力，其更新规则为：

$$\Theta^{j+1} = \Theta^{j} - \lambda \nabla \sum_{\mathcal{O}} \mathcal{L}(\Phi(\mathcal{O}; \Theta_i^{j})), \quad \Theta_i^{0} = \Theta$$

该公式（Equation 1, Section 2.2）描述了从元网络初始化 $\Theta$ 出发，通过少量梯度下降步拟合特定实例观测 $\mathcal{O}$ 的过程。$\lambda$ 为学习率，$\mathcal{L}$ 为损失函数。

### 网络架构模块

位置编码是提升神经场高频表达能力的关键模块。正弦位置编码的偶分量形式为：

$$\gamma_{(2i)}(x) = \sin(2^{i-1} \pi x)$$

该公式（Equation 8, Section 5.1）通过将低维坐标映射到高维空间，使网络能够捕捉高频细节。编码频率随索引 $i$ 指数增长。

### 模块间的关系与瓶颈

上述模块并非孤立运作，而是通过统一的反问题求解框架相互连接。其核心瓶颈在于：条件机制决定了模型的泛化能力边界，混合表示在计算效率与表示能力之间进行权衡，前向映射的物理准确性直接影响重建质量，而网络架构则决定了模型对高频信号的表达能力。五大技术类别（Table 2）分别对应学习、推理和控制中的不同问题，共同构成了神经场工具箱的完整拼图。

## 实验与分析

需要指出，本文是一篇综述性报告，并未进行原创实验。文中引用的所有性能数据均来自原始论文，因此本处无法提供传统意义上的主实验结果与消融分析。以下基于综述中归纳的技术框架与实证观察，梳理关键图表结论、设计瓶颈与失败模式。

### 关键图表结论

**Figure 2** 展示了神经场论文随时间增长的趋势：尽管神经场的概念在二十年前已被提出，但其在视觉计算领域的爆发式增长集中于2019年之后的两年间，被调查的论文超过250篇。这一趋势印证了综述的核心动机——领域快速膨胀导致术语碎片化与概念重复，亟需统一框架。

**Figure 3** 与 **Table 2** 共同描绘了典型神经场算法的前馈流程及其工具箱。流程为：时空坐标输入神经网络产生场量，经前向映射转换到传感器域，再与传感器观测计算重建误差。**Table 2** 将解决学习、推理与控制中各类问题的技术归纳为五大类：先验学习与条件、混合表示、前向映射、网络架构、编辑。该分类框架是本文的核心贡献，为后续方法比较提供了系统性语言。


![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2111_11426/figures/005_Figure_3.jpg]]
*Figure 3: A typical feed-forward neural field algorithm. Spatiotemporal coordinates are fed into a neural network which predicts values in the reconstruct a domain. Then, this domain is mapped to the sensor domain where sensor measurements are available as supervision. Figures adapted from [MST∗20, LZP∗20]. Table 2: The five classes of techniques in the neural field toolbox each addresses problems that arise in learning, inference, and control*

**Figure 4** 比较了编码器推理与自解码器推理两种范式。在分摊式编码器推理中，编码器 $E$ 将观测 $O$ 映射为潜变量 $z$，编码器参数与条件神经场联合优化；自解码器则缺乏编码器，每个神经场由单独优化的潜码 $z_i$ 表示。这一区别直接影响了泛化效率与推理成本：编码器可实现快速前馈推理，但需要大量训练数据；自解码器更灵活但每个新实例需重新优化。

**Figure 5** 对比了全局条件与局部条件机制。全局条件中，单一潜码 $z$ 定义所有输入坐标上的神经场；局部条件则通过离散数据结构提供坐标相关的潜码 $z = g(x)$，使网络具有坐标依赖性。局部条件是混合表示的理论基础，也是神经场扩展至大规模场景的关键技术路径。

**Figure 6** 展示了混合表示的多种实例，包括神经稀疏体素网格、多尺度体素网格与神经2D图像压缩、物体包围盒与神经辐射场、网格、图集以及Voronoi分解与神经辐射场。这些实例表明，将神经场与离散数据结构结合是突破单一MLP容量限制的通用策略。


![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2111_11426/figures/008_Figure_6.jpg]]
*Figure 6: Examples of hybrid representations: (A) neural sparse voxel grid [ $\mathrm { L G L } ^ { \ast }$ 2 0 ] . , (B) multi-scale voxel grid with neural 2D image compression [MLL∗21], (C) object bounding boxes with neural radiance fields [ $\mathrm { Z L Y ^ { * } }$ 2 1 ] . , (D) mesh $\mathrm { [ P Z X ^ { * } 2 1 ] }$ (E) atlas [ $\mathrm { G F K ^ { * } }$ 1 8 $\mathrm { b }$ ] , and (F) Voronoi decomposition with neural radiance fields [ $\mathrm { R J Y ^ { * } }$ 2 1 ]

**Table 3** 列举了前向映射的示例，涵盖CT、MRI、合成孔径声纳等成像模态。**Figure 7** 进一步将可微分前向映射归纳为球追踪、体渲染、网格化（如Marching Cubes）、Radon与傅里叶变换、偏导数等类型。前向映射的可微性是神经场能够通过梯度下降从传感器观测中重建场的核心使能因素。

### 设计瓶颈与失败模式

基于综述对250余篇论文的分析，可识别以下跨方法的设计瓶颈：

1. **容量与效率的权衡**：纯MLP架构虽然连续且内存紧凑，但在表示高频细节时受限于频谱偏差。位置编码（如正弦位置编码 $\gamma_{(2i)}(x) = \sin(2^{i-1} \pi x)$，见Equation 8）可缓解此问题，但引入了额外的超参数敏感性。混合表示通过引入显式离散结构提升了容量，但牺牲了连续性的部分优势，并引入了离散化伪影的风险。

2. **条件机制的过拟合倾向**：自解码器范式在小数据场景下容易过拟合到单个观测，而编码器范式需要大规模多样化数据来学习有意义的先验。梯度元学习（见Equation 1：$\Theta^{j+1} = \Theta^{j} - \lambda \nabla \sum_{\mathcal{O}} \mathcal{L}(\Phi(\mathcal{O}; \Theta_i^{j})), \quad \Theta_i^{0} = \Theta$）提供了一种折中，但元训练的计算开销显著。

3. **前向映射的数值稳定性**：体渲染等前向映射涉及沿射线的积分近似，采样效率与数值精度之间存在根本性权衡。球追踪等几何前向映射则面临收敛性与梯度消失的挑战。

4. **编辑的可控性不足**：**Table 4** 与 **Table 5** 分别归纳了参数编辑与坐标重映射两类编辑方法。现有方法普遍缺乏对编辑操作语义一致性的保证，参数空间的局部修改可能导致全局的意外变化，坐标变换的复合也易产生非预期的拓扑改变。


![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2111_11426/figures/013_Table_4.jpg]]
*Table 4: Neural fields can be edited by directly changing network parameters such as weights and latent features. We list related work that performs editing through parameter editing*

### 开放问题与验证需求

综述指出的开放问题直接映射到实验验证的空白领域：神经场压缩方案与标准编解码器的严格定量比较缺失；许多引用的工作中设计选择缺乏消融研究；弱监督与自监督学习神经场的性能边界尚未系统刻画。这些均需后续实证工作填补。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2111_11426/figures/003_Table_1.jpg]]
*Table 1: Y. Xie, T. Takikawa, S. Saito, O. Litany, S. Yan, N. Khan, F. Tombari, J. Tompkin, V. Sitzmann, S. Sridhar / Neural Fields in Visual Computing Table 1: Examples of fields in physics and visual computing*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2111_11426/figures/009_Table.jpg]]
*Table: Y. Xie, T. Takikawa, S. Saito, O. Litany, S. Yan, N. Khan, F. Tombari, J. Tompkin, V. Sitzmann, S. Sridhar / Neural Fields in Visual Computing*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2111_11426/figures/012_Table.jpg]]
*Table: Y. Xie, T. Takikawa, S. Saito, O. Litany, S. Yan, N. Khan, F. Tombari, J. Tompkin, V. Sitzmann, S. Sridhar / Neural Fields in Visual Computing*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2111_11426/figures/023_Table.jpg]]
*Table: Appendix A: Variable Naming Conventions*


## 方法谱系与知识库定位

### 统一框架的技术定位

本综述的核心贡献并非提出一个新的算法，而是构建了一个由五大类技术组成的统一工具箱，用于系统化地描述、比较和定位现有的神经场方法。这五类技术分别是：**先验学习与条件**（Section 2）、**混合表示**（Section 3）、**前向映射**（Section 4）、**网络架构**（Section 5）和**编辑**（Section 6）。该框架的出发点是解决一个核心瓶颈：神经场研究论文在2019年后呈爆发式增长（Figure 2），但缺乏统一的数学公式和术语，导致概念重复和交流困难。

框架的核心洞察是将神经场形式化为一个通用函数 $\Phi(\mathbf{x}; \Theta)$，其中场量 $\mathbf{q}$ 由参数为 $\Theta$ 的神经网络根据时空坐标 $\mathbf{x}$ 产生。通过组合不同的条件机制、离散-连续混合表示、可微分前向映射和架构选择，该框架能够覆盖从2D图像处理到3D场景重建、从生成模型到机器人学等广泛的应用领域。

### 方法谱系：五大技术轴线的定位逻辑

**1. 先验学习与条件（Prior Learning and Conditioning）**
该轴线解决的核心问题是“如何让神经场从少量或单次观测中学习”。综述将条件机制分为三个层次：
- **推理方式**：编码器（Encoder）vs. 自解码器（Auto-decoder）。编码器通过前馈网络 $\mathbf{z} = E(\mathcal{O})$ 直接从观测 $\mathcal{O}$ 生成潜在码 $\mathbf{z}$，实现摊销推理（Figure 4A）；自解码器则通过优化 $\mathbf{z} = \arg\min \mathcal{L}(\mathbf{z}, \Theta)$ 为每个实例独立求解潜在码（Figure 4B），无需训练编码器。
- **条件范围**：全局条件（Global Conditioning）vs. 局部条件（Local Conditioning）。全局条件使用单一潜在码 $\mathbf{z}$ 定义整个场（Figure 5A）；局部条件通过离散数据结构提供坐标依赖的潜在码 $\mathbf{z} = g(\mathbf{x})$（Figure 5B），使得网络在不同空间位置表现出不同的行为。
- **条件注入方式**：拼接（Concatenation）等价于将潜在码映射为第一层偏置的仿射函数；超网络（Hypernetworks）则使用神经网络 $\Psi$ 直接输出场参数 $\Theta$；基于梯度的元学习更新规则为 $\Theta^{j+1} = \Theta^{j} - \lambda \nabla \sum_{\mathcal{O}} \mathcal{L}(\Phi(\mathcal{O}; \Theta_i^{j})), \quad \Theta_i^{0} = \Theta$，通过少量梯度步从元网络初始化拟合特定实例。

**2. 混合表示（Hybrid Representations）**
该轴线解决“如何让神经场扩展到大规模信号”的问题。核心思想是将神经场与离散数据结构结合，分解输入坐标空间。综述形式化了两种范式：
- **网络平铺（Network Tiling）**：$\mathbf{q} = \Phi(\mathbf{x}, g(\mathbf{x}))$，通过查找函数 $g(\mathbf{x})$ 在不同区域存储独立的网络参数。
- **嵌入（Embedding）**：$\mathbf{q} = \Phi(\mathbf{x}, \Psi(g(\mathbf{x})))$，将局部嵌入 $\mathbf{z} = g(\mathbf{x})$ 通过函数 $\Psi$ 映射为网络参数。

Figure 6 展示了六种典型的混合表示实例：神经稀疏体素网格、多尺度体素网格与神经2D图像压缩、物体边界框与神经辐射场、网格、图集和Voronoi分解与神经辐射场。

**3. 前向映射（Forward Maps）**
该轴线解决“如何将重建域与传感器域关联”的问题。神经场在重建域中预测场量，前向映射 $F$ 将这些量映射到传感器域，优化目标为 $\underset{\Theta}{\operatorname{argmin}} \int_{(\mathbf{x}_{\text{recon}}, \mathbf{x}_{\text{sens}}) \in (\mathcal{X}, \mathcal{S})} \left. F(\Phi(\mathbf{x}_{\text{recon}})) - \Omega(\mathbf{x}_{\text{sens}}) \right.$。Figure 7 列举了五种可微分前向映射类型：球体追踪、体渲染、网格化（如Marching Cubes）、Radon与傅里叶变换、偏导数。Table 3 进一步列举了CT、MRI、合成孔径声纳等领域的应用实例。

**4. 网络架构（Network Architecture）**
该轴线关注“什么样的网络结构适合表示场”。综述讨论了激活函数选择对导数性质的影响（Figure 8A：ReLU产生分段常数导数，正弦激活产生正余弦导数），以及通过自动微分共享参数求解需要积分监督的优化问题（Figure 8B）。正弦位置编码 $\gamma_{(2i)}(x) = \sin(2^{i-1} \pi x)$ 是映射坐标到高维空间的关键技术。

**5. 编辑（Manipulation）**
该轴线解决“如何控制和编辑神经场”的问题。Table 4 列举了通过直接修改网络参数（权重和潜在特征）进行编辑的工作，Table 5 列出了通过坐标空间变换 $\mathbf{x} \to \mathbf{x}'$ 实现编辑的方法。

### 适用边界与局限

**适用边界：**
- 该框架主要覆盖**视觉计算**领域的神经场应用，包括2D图像处理、3D场景重建与视图合成、数字人、生成模型、压缩和机器人学等。
- 框架假设场是**可微分的**，因此依赖梯度下降优化的前向映射和网络架构是其核心组件。
- 框架天然适合**病态反问题**（ill-posed inverse problems），因为神经场的过参数化和可微性提供了强大的正则化先验。

**已知局限：**
1. **时效性风险**：由于该领域发展极其迅速，任何静态综述都可能很快过时。综述本身也承认这一点，并试图通过社区驱动的动态数据库网站来缓解该问题。
2. **缺乏严格定量比较**：综述指出，目前缺乏对现有神经场压缩方案与标准编解码器的严格定量比较，许多引用工作的设计选择也缺乏消融研究。
3. **社区数据库的覆盖依赖**：配套网站依赖用户提交，可能存在覆盖不完全或延迟的问题。该点需要手动验证当前网站的活跃度和完整性。
4. **高层次语义任务的空白**：将神经场应用于高层次语义任务（如场景理解、物体识别）仍是一个开放问题，当前框架主要面向低层重建和生成任务。

### 开放问题与未来方向

综述识别出以下关键开放问题：
1. **通用先验框架**：如何构建一个融合更强先验的通用框架，以实现更好的泛化能力和数据效率，是当前的核心挑战。
2. **超越监督学习**：如何实现弱监督或自监督学习的神经场，减少对密集标注或精确传感器模型的依赖。
3. **多模态融合**：探索多模态数据（如图像、深度、触觉、音频）的融合，可能拓展神经场在具身智能和机器人领域的应用边界。
4. **高层次语义**：将神经场从几何和外观表示扩展到语义和任务驱动的表示，仍是未解决的问题。

## 原文 PDF

![[paperPDFs/EUROGRAPHICS_2022/Neural_Fields_in_Visual_Computing_and_Beyond.pdf]]
