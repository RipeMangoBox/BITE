---
title: "PhysSkin: Real-Time and Generalizable Physics-Based Animation via Self-Supervised Neural Skinning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PhysSkin_Real_Time_and_Generalizable_Physics_Based_Animation_via_Self_Supervised_Neural_Skinning.pdf
project_link: "https://zju3dv.github.io/PhysSkin/"
code_link: null
aliases:
- PhysSkin
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 神经蒙皮字段自动编码器与物理信息自监督学习（PISSL）的结合。该自动编码器利用Transformer编码器和交叉注意力解码器从任意3D几何生成连续蒙皮场，而PISSL通过皮肤场在线归一化和冲突感知梯度校正，能够仅从静态几何中稳定地学习物理合理、正交且平滑的蒙皮模式。
primary_logic: 将线性混合蒙皮（LBS）的思想扩展到连续神经场，并通过物理先验（能量最小化、空间平滑、正交约束）的自监督学习，使得网络可以从静态形状中自动发现物理上合理的变形子空间，无需任何运动轨迹或蒙皮标注，从而实现通用且实时的物理动画。冲突感知梯度校正解决了多损失项间的梯度干扰，是训练稳定的关键。
claims:
- PhysSkin在RigNet和ShapeNet数据集上全面超越了现有可泛化及非可泛化的神经蒙皮方法。
- 我们的方法在所有三项评估指标（正交性、条件数、谱熵）上均达到最佳，证明了所学习蒙皮场的物理一致性和数值稳定性。
- RigNet 上 Ω_orth (×10⁻²) ↓ = 0.0033
- RigNet 上 κ_log ↓ = 1.0453
---

# PhysSkin: Real-Time and Generalizable Physics-Based Animation via Self-Supervised Neural Skinning

> [!tip] 核心洞察
> 将线性混合蒙皮（LBS）的思想扩展到连续神经场，并通过物理先验（能量最小化、空间平滑、正交约束）的自监督学习，使得网络可以从静态形状中自动发现物理上合理的变形子空间，无需任何运动轨迹或蒙皮标注，从而实现通用且实时的物理动画。冲突感知梯度校正解决了多损失项间的梯度干扰，是训练稳定的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhysSkin：通过自监督神经蒙皮实现实时与可泛化的物理动画 |
| 英文题名 | PhysSkin: Real-Time and Generalizable Physics-Based Animation via Self-Supervised Neural Skinning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.23194) · [Project](https://zju3dv.github.io/PhysSkin/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | PhysSkin |
| Dataset | RigNet, ShapeNet |

> [!tip] 效果简介
> - RigNet 上，Ω_orth (×10⁻²) ↓ 0.0033；κ_log ↓ 1.0453；H_spec ↑ 0.9999。
> - ShapeNet 上，Ω_orth (×10⁻²) ↓ 0.0098；κ_log ↓ 1.0460；H_spec ↑ 0.9997。

## 概要

**问题瓶颈**：现有基于物理的动画方法面临双重困境——以 **Simplicits**（Modi et al., ACM TOG 2024）为代表的物理信息子空间方法需要为每个对象单独训练网络，无法泛化；而 **RigNet**（Xu et al., SIGGRAPH 2020）、**Anymate**（Deng et al., SIGGRAPH 2025）等数据驱动神经绑定方法则依赖昂贵的专家蒙皮标注，难以规模化应用。核心矛盾在于：缺乏一种既能跨形状泛化、又无需运动/标注数据即可学习物理一致蒙皮表示的框架。

**核心方法**：PhysSkin 提出**神经蒙皮场自动编码器 + 物理信息自监督学习（PISSL）**的双轮驱动方案。自动编码器利用 Transformer 点云编码器（基于 Michelangelo 预训练）和交叉注意力解码器，从任意静态几何生成连续的蒙皮场，天然支持不同分辨率和拓扑的泛化。PISSL 则通过三种物理损失（潜在能量最小化、空间平滑、正交约束）驱动学习，仅需静态几何即可自动发现物理上合理的变形子空间。其中，**皮肤场在线归一化**防止数值漂移，**冲突感知梯度校正**解决多损失项间的梯度干扰，是训练稳定的关键机制。

**核心结论**：PhysSkin 在 RigNet 和 ShapeNet 两大基准上全面超越可泛化与非可泛化的现有方法。正交性指标 Ω_orth 低至 0.0033（RigNet）和 0.0098（ShapeNet），条件数 κ_log 和谱熵 H_spec 均接近理论最优，证明所学习蒙皮场具有优异的物理一致性和数值稳定性。同时，子空间隐式时间积分使物理动画达到实时性能。

**方法定位**：PhysSkin 位于**物理模拟 × 神经场 × 自监督学习**的交叉点。相较于逐对象训练的物理子空间方法（如 Simplicits），它实现了前馈式泛化；相较于依赖标注的神经绑定方法（如 RigNet、Anymate），它消除了对运动轨迹和蒙皮标签的依赖。其核心创新在于将线性混合蒙皮（LBS）的思想连续化到神经场，并通过物理先验的自监督学习，使网络从静态形状中自主归纳变形子空间结构。

### 物理动画的计算矛盾

真实感物理动画是计算机图形学与交互式应用的核心需求。全空间物理模拟器——如有限元法（FEM）和物质点法（MPM）——虽然能提供高保真的变形与动力学效果，但每步模拟的计算代价极高（Table 3），无法满足实时性要求。线性混合蒙皮（Linear Blend Skinning, LBS）及其变体通过将高维变形投影到低维骨骼变换子空间，大幅降低了计算复杂度，但经典LBS依赖艺术家手工绘制的蒙皮权重，成本高昂且不可泛化。

### 现有神经蒙皮方法的缺口

近年来，数据驱动的神经蒙皮方法试图自动化蒙皮权重生成，但存在两个根本性瓶颈：

**对标注数据的强依赖。** 代表性工作如 **RigNet**（Xu et al., SIGGRAPH 2020）、**Anymate**（Deng et al., SIGGRAPH 2025）、**Make-It-Animatable**（Guo et al., CVPR 2025）和 **Puppeteer**（Song et al., NeurIPS 2025）均需要大规模专家标注的骨骼-蒙皮配对数据进行监督训练。这类标注的获取成本极高，且限制了模型向新形状域的迁移。

**泛化能力的缺失。** 另一类物理信息驱动的子空间方法，如 **Simplicits**（Modi et al., TOG 2024），虽然无需蒙皮标注，但必须为每个3D对象单独训练一个网络，无法在训练后以“前馈”方式泛化到未见过的形状和离散化。这意味着每遇到一个新模型，都需要重新执行完整的训练流程，严重制约了实际部署效率。

### 核心矛盾与本文动机

上述方法反映了一个深层矛盾：**物理合理性、泛化能力和标注数据需求三者难以兼得。** 物理模拟需要变形子空间具备良好的数值条件（低条件数、高正交性），而泛化到任意拓扑和分辨率则需要连续、离散化无关的蒙皮表示。现有方法要么牺牲泛化性换取物理一致性（如Simplicits），要么依赖昂贵标注换取泛化性（如RigNet等）。

PhysSkin的动机正是打破这一三角困境：**能否仅从静态3D几何出发，通过物理先验的自监督学习，自动发现物理上合理且可泛化的连续蒙皮场？** 这一问题的肯定回答意味着：无需任何运动轨迹或蒙皮标注，单一预训练模型即可为任意3D形状实时生成物理一致的动画。

### 技术挑战

实现上述目标面临两个关键技术挑战：

1. **表示设计**：如何构建一个连续的神经蒙皮场，使其能处理任意拓扑、分辨率和离散化，同时保持足够的表达能力来捕获复杂变形模式？
2. **训练稳定性**：在无标注的自监督设定下，物理能量最小化、空间平滑性和蒙皮正交性等多目标之间存在天然的梯度冲突，如何避免训练过程中的数值漂移和模式坍塌？

## 核心方法与创新机理

PhysSkin 的核心创新在于将**连续神经蒙皮场**与**物理信息自监督学习（PISSL）**深度耦合，从根本上改变了蒙皮权重的表示范式与获取方式。与现有方法相比，其关键突破体现在三个紧密关联的维度。

### 从离散蒙皮到连续神经蒙皮场

传统方法（如 **RigNet** (Xu et al., SIGGRAPH 2020)、**Anymate** (Deng et al., SIGGRAPH 2025)）将蒙皮权重定义为特定网格顶点上的离散向量，导致模型与分辨率、拓扑强绑定。PhysSkin 提出**神经蒙皮场自动编码器**，将蒙皮权重提升为定义在整个三维空间上的连续函数 $W(\mathbf{X})$。该自动编码器由基于 Transformer 的点云编码器与交叉注意力解码器构成：编码器从表面点云中提取形状潜在码 $\mathbf{F}_s$（Equ. 4），解码器通过可学习的处理柄令牌与形状潜在码的交叉注意力生成处理柄特征 $\mathbf{F}_h$（Equ. 5），再对任意空间查询点 $\mathbf{X}$ 进行逐点交叉注意力与 MLP 解码，输出该点的蒙皮权重向量（Equ. 6-7）。这一设计使得单一模型可泛化到任意分辨率和拓扑的 3D 形状，无需针对每个对象重新训练。

### 从标注依赖到物理自监督

现有神经绑定方法（RigNet、Anymate、**Make-It-Animatable** (Guo et al., CVPR 2025)、**Puppeteer** (Song et al., NeurIPS 2025)）依赖专家标注的蒙皮数据或运动序列进行监督训练；**Simplicits** (Modi et al., TOG 2024) 虽引入物理信息，但仍需为每个对象单独优化。PhysSkin 的 PISSL 策略仅利用静态几何形状，通过三个物理先验损失驱动学习：

- **潜在能量损失** $\mathcal{L}_{\mathrm{pot}}$（Equ. 8）：对随机采样的子空间坐标 $\mathbf{z}$ 计算期望势能，引导蒙皮场收敛到低能量变形子空间；
- **空间平滑损失** $\mathcal{L}_{\mathrm{smooth}}$（Equ. 9）：惩罚蒙皮权重函数的空间梯度范数，强制变形影响的局部连续性；
- **正交损失** $\mathcal{L}_{\mathrm{orth}}$：促进不同处理柄的蒙皮权重向量相互正交，保证变形子空间的解耦性。

这一策略使得网络能够从无序的初始表示中自动发现物理上合理的蒙皮模式（Figure 3），完全摆脱了对运动轨迹或蒙皮标注的依赖。

### 训练稳定性机制：在线归一化与冲突感知梯度校正

多损失项联合优化面临两个关键挑战：蒙皮权重数值漂移和损失间梯度冲突。PhysSkin 引入两项针对性机制：

- **皮肤场在线归一化**：在训练过程中动态调节蒙皮权重的尺度，防止数值发散，确保优化稳定收敛；
- **冲突感知梯度校正**：当不同损失项的梯度方向相互冲突时，通过投影操作消除干扰分量，使得各损失能够协同优化而非相互抵消。

消融实验（Table 4）证实，完整模型在所有指标上均优于移除任一损失项或稳定性机制的变体，其中移除 $\mathcal{L}_{\mathrm{pot}}$ 会导致蒙皮场失去物理意义、正交性指标显著恶化（Figure 12），验证了物理先验与稳定性机制的关键作用。

### 与 baseline 的核心差异总结

| 维度 | 现有方法 | PhysSkin |
|------|---------|----------|
| 蒙皮权重表示 | 离散顶点权重 / 单对象网络 | 连续神经蒙皮场，跨形状泛化 |
| 训练监督 | 运动序列或专家蒙皮标注 | 仅静态几何，物理自监督 |
| 优化稳定性 | 无特殊处理，梯度冲突常见 | 在线归一化 + 冲突感知梯度校正 |
| 泛化能力 | 需逐对象训练或限定类别 | 单一模型覆盖 RigNet + ShapeNet 多样化形状 |

这些创新共同构成了 PhysSkin 的核心技术壁垒：连续场表示赋予泛化能力，物理自监督消除数据瓶颈，稳定性机制保障训练收敛，三者缺一不可。

PhysSkin 提出了一种可泛化的物理信息神经蒙皮框架，其核心目标是从静态 3D 几何中直接学习连续蒙皮场，进而实现实时物理动画，无需任何运动序列或蒙皮标注数据。整个 pipeline 由三个紧密耦合的阶段构成：**蒙皮子空间表示**、**神经蒙皮场自动编码器**和**物理信息自监督学习**。

### 输入与预处理

给定一个静态 3D 形状，系统首先进行两类点采样（Figure 2）：

- **表面点**：用于形状编码，从物体表面采样，提供几何外观信息。
- **体积积分点（cubature points）**：用于后续的物理模拟与能量计算。采样策略为：先在表面采样 100k 个点，再将空间体素化为 $128^3$ 的网格以获取内部点，共同构成候选积分点集。训练时每个批次随机采样 1000 个积分点用于势能计算。

### 核心模块与数据流

**1. 蒙皮子空间表示（Sec. 3.1）**

框架将全空间 3D 变形建模为 $m$ 个仿射变换的加权和，即线性混合蒙皮（LBS）的推广形式：

$$\phi(\mathbf{X}, \mathbf{z}) = \mathbf{X} + \sum_{i=1}^{m} W_i(\mathbf{X}) \mathbf{Z}_i [\mathbf{X}]$$

其中 $\mathbf{X}$ 为静止姿态下的空间位置，$W_i(\mathbf{X})$ 为第 $i$ 个处理柄在点 $\mathbf{X}$ 处的蒙皮权重，$\mathbf{Z}_i$ 为对应的仿射变换。物体的运动通过在降维子空间坐标 $\mathbf{z}$ 上执行隐式时间积分来更新：

$$\mathbf{z}_{t+1} = \arg\min_{\mathbf{z}} \frac{1}{2h^2} \| \mathbf{z} - 2\mathbf{z}_t + \mathbf{z}_{t-1} \|_{\mathbf{M}}^2 + E_{\mathrm{pot}}(\phi(\mathbf{X}, \mathbf{z}))$$

这一设计将高维的全空间动力学压缩到低维子空间，是实现实时模拟的关键。

**2. 神经蒙皮场自动编码器（Sec. 3.2）**

自动编码器负责从任意 3D 几何生成连续蒙皮场，其数据流如下：

- **形状编码器**：采用基于 Transformer 的点云编码器（使用 Michelangelo 预训练权重），将表面点云 $\mathbf{P}$ 编码为形状潜在特征集 $\mathbf{F}_s$：
  $$\mathbf{F}_s = \mathrm{SelfAttn}^{(1:L)}(\mathrm{CrossAttn}(\mathbf{Q}_s, \gamma(\mathbf{P})))$$

- **处理柄潜在码提取**：通过一组可学习的处理柄查询令牌 $\mathbf{Q}_h$ 与形状潜在码进行交叉注意力，生成 $m$ 个处理柄潜在特征 $\mathbf{F}_h$：
  $$\mathbf{F}_h = \mathrm{CrossAttn}(\mathbf{Q}_h, \mathrm{SelfAttn}(\mathbf{F}_s))$$

- **点式皮肤特征提取**：对任意空间查询点 $\mathbf{X}$，通过其位置编码 $\gamma(\mathbf{X})$ 与处理柄潜在码的交叉注意力获得逐点皮肤特征 $\mathbf{F}_p$：
  $$\mathbf{F}_p = \mathrm{CrossAttn}(\gamma(\mathbf{X}), \mathbf{F}_h)$$

- **蒙皮场解码**：将点特征与位置编码拼接后送入 ResNet 风格的 MLP，解码为蒙皮权重向量 $W(\mathbf{X})$。解码器末端引入 **ONI（Orthogonality-Nudging Injection）模块**，促进不同蒙皮权重之间的正交性。

这一架构的关键优势在于**连续性与离散化无关性**：蒙皮场定义为空间中的连续函数，可在任意分辨率和拓扑的网格上查询，无需针对特定离散化重新训练。

**3. 物理信息自监督学习（PISSL, Sec. 3.3）**

训练仅使用静态几何形状，通过三类物理先验损失驱动网络自动发现合理的蒙皮模式：

- **势能损失** $\mathcal{L}_{\mathrm{pot}}$：最小化随机采样子空间坐标下的期望势能，驱策蒙皮朝向低能量变形子空间：
  $$\mathcal{L}_{\mathrm{pot}}(\theta) = \mathbb{E}_{\mathbf{z} \sim \mathcal{N}} [E_{\mathrm{pot}}^{\theta}(\phi(\mathbf{X}, \mathbf{z}))]$$
  训练时每批次随机采样 1024 个子空间坐标 $\mathbf{z}$。

- **空间平滑损失** $\mathcal{L}_{\mathrm{smooth}}$：惩罚蒙皮权重函数空间梯度的范数，强制相邻区域具有相似的变形行为：
  $$\mathcal{L}_{\mathrm{smooth}}(\theta) = \mathbb{E}_{\mathbf{X} \sim S} \sum_{i=1}^{m} \| \nabla \Phi_{\theta}^{i}(\mathbf{X}) \|^2$$

- **正交损失** $\mathcal{L}_{\mathrm{orth}}$：促进不同蒙皮权重向量之间的正交性，增强变形子空间的数值稳定性。

为保障训练的数值稳定性，PISSL 引入了两项关键机制：

- **皮肤场在线归一化**：在训练过程中动态调节蒙皮权重的尺度，防止数值漂移。
- **冲突感知梯度校正**：解决多损失项间的梯度干扰问题，使势能最小化、平滑性和正交性能协同优化而非相互对抗。这是训练能够稳定收敛的关键设计。

### 推理与动画

训练完成后，PhysSkin 以前馈方式工作：给定任意未见过的 3D 形状，自动编码器一次性推理出连续蒙皮场；随后在获得的蒙皮子空间中执行隐式时间积分，即可驱动物体产生物理合理的实时动画。Figure 3 展示了蒙皮场在优化过程中的演化：从无序的初始表示开始，PISSL 逐步将其组织为物理一致、几何正交且空间平滑的蒙皮模式。

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2603_23194/figures/001_Figure_1.jpg]]
*Figure 1: PhysSkin is a generalizable physics-informed neural skinning framework for object animation. The framework is learned directly from static 3D geometries via physics-informed self-supervision without any annotated data. Once trained, PhysSkin can be applied in a feed-forward manner to perform neural skinning for diverse 3D shapes and discretizations, enabling real-time physics-based animation*

### 蒙皮子空间变形表示

PhysSkin 将完整三维空间的位移场建模为 $m$ 个仿射变换的加权线性混合（LBS）。给定静止姿态位置 $\mathbf{X}$ 和子空间坐标 $\mathbf{z}$（编码所有处理柄的仿射参数），变形映射定义为：

$$\phi(\mathbf{X}, \mathbf{z}) = \mathbf{X} + \sum_{i=1}^{m} W_i(\mathbf{X}) \mathbf{Z}_i [\mathbf{X}]$$

其中 $W_i(\mathbf{X})$ 是第 $i$ 个处理柄在点 $\mathbf{X}$ 处的蒙皮权重，$\mathbf{Z}_i[\mathbf{X}]$ 表示该处理柄对点 $\mathbf{X}$ 施加的仿射变换。该表示将高维变形空间压缩到低维子空间坐标 $\mathbf{z}$ 上，是实现实时物理模拟的基础（Equ. 2）。

全空间物理模拟需执行隐式时间积分以更新物体状态 $s$：

$$s_{t+1} = \underset{s}{\arg\min} \frac{1}{2h^2} \| s - 2s_t + s_{t-1} \|_{\mathbf{M}}^2 + \mathcal{E}_{\mathrm{pot}}(s)$$

其中 $\mathbf{M}$ 为质量矩阵，$\mathcal{E}_{\mathrm{pot}}$ 为势能函数，$h$ 为时间步长（Equ. 1）。将变形映射 $\phi$ 代入后，可在降维子空间坐标 $\mathbf{z}$ 上直接执行隐式时间积分：

$$\mathbf{z}_{t+1} = \arg\min_{\mathbf{z}} \frac{1}{2h^2} \| \mathbf{z} - 2\mathbf{z}_t + \mathbf{z}_{t-1} \|_{\mathbf{M}}^2 + E_{\mathrm{pot}}(\phi(\mathbf{X}, \mathbf{z}))$$

这一降维积分大幅降低了每步模拟的计算量，是实现实时动画的核心机制（Equ. 3）。

### 神经蒙皮字段自动编码器

PhysSkin 的核心创新在于用一个可泛化的自动编码器生成连续蒙皮场，其结构包含三个关键模块：

**形状编码器**：使用基于 Transformer 的点云编码器（Michelangelo 预训练架构）处理表面采样点 $\mathbf{P}$，通过交叉注意力与自注意力提取形状潜在特征集合 $\mathbf{F}_s$：

$$\mathbf{F}_s = \mathrm{SelfAttn}^{(1:L)}(\mathrm{CrossAttn}(\mathbf{Q}_s, \gamma(\mathbf{P})))$$

其中 $\gamma(\cdot)$ 为位置编码，$\mathbf{Q}_s$ 为可学习的形状查询令牌（Equ. 4）。

**蒙皮场解码器**：首先通过一组可学习的处理柄查询令牌 $\mathbf{Q}_h$ 与形状潜在码进行交叉注意力，产生处理柄潜在特征 $\mathbf{F}_h$：

$$\mathbf{F}_h = \mathrm{CrossAttn}(\mathbf{Q}_h, \mathrm{SelfAttn}(\mathbf{F}_s))$$

随后，对空间中的任意查询点 $\mathbf{X}$，通过其位置编码与 $\mathbf{F}_h$ 的交叉注意力获得逐点皮肤特征 $\mathbf{F}_p$：

$$\mathbf{F}_p = \mathrm{CrossAttn}(\gamma(\mathbf{X}), \mathbf{F}_h)$$

最终通过 ResNet 风格的 MLP 将点特征与位置编码融合，解码为蒙皮权重向量：

$$W(\mathbf{X}) = \mathrm{MLP}(\mathbf{F}_p \oplus \gamma(\mathbf{X}))$$

该架构使蒙皮场成为空间连续的神经场，可泛化到任意分辨率和拓扑的 3D 形状（Equ. 5-7）。解码器末端采用在线归一化（ONI）模块，对输出蒙皮权重进行实时归一化，防止训练过程中的数值漂移。

### 物理信息自监督学习（PISSL）

PISSL 策略使网络能够仅从静态几何中学习物理合理的蒙皮模式，无需任何运动轨迹或蒙皮标注。训练包含三个损失项：

**潜在能量损失**：驱动蒙皮子空间朝向低能量变形方向，从标准正态分布采样子空间坐标 $\mathbf{z}$，计算期望势能：

$$\mathcal{L}_{\mathrm{pot}}(\theta) = \mathbb{E}_{\mathbf{z} \sim \mathcal{N}} [E_{\mathrm{pot}}^{\theta}(\phi(\mathbf{X}, \mathbf{z}))]$$

该损失是物理一致性的核心保证——若移除该项，蒙皮场将失去物理意义，正交性指标显著恶化（Equ. 8）。

**空间平滑损失**：惩罚蒙皮权重函数空间梯度的范数，强制相邻点具有相似的蒙皮权重：

$$\mathcal{L}_{\mathrm{smooth}}(\theta) = \mathbb{E}_{\mathbf{X} \sim S} \sum_{i=1}^{m} \| \nabla \Phi_{\theta}^{i}(\mathbf{X}) \|^2$$

（Equ. 9）

**正交损失**：促进不同处理柄的蒙皮权重向量之间相互正交，减少变形子空间的冗余耦合：

$$\mathcal{L}_{\mathrm{orth}}(\theta) = \mathbb{E}_{\mathcal{D} \sim \mathcal{S}} \left[ \sum_{i=1}^{m} \sum_{j=1}^{m} \left( \Phi_{\theta}^{i}(\mathbf{X}_{\mathcal{D}})^{\top} \Phi_{\theta}^{j}(\mathbf{X}_{\mathcal{D}}) \right)^2 \right]$$

### 训练稳定性机制

多损失项联合优化易产生梯度冲突。PhysSkin 引入两项关键机制解决此问题：

- **皮肤场在线归一化**：在解码器末端对蒙皮权重进行实时归一化，防止数值漂移导致训练崩溃。
- **冲突感知梯度校正**：借鉴 的方法，动态检测并校正不同损失项之间的梯度干扰，使能量最小化、平滑性、正交性三个目标能够稳定协同优化。

消融实验（Table 4）表明，完整模型在所有指标上均优于移除任一损失项或稳定性机制的变体，验证了各模块的必要性。

## 实验与关键发现

### 评估指标

为系统衡量蒙皮场的物理质量与数值稳定性，论文引入三项无参考评估指标：

- **正交性指标** $\Omega_{\mathrm{orth}}$：衡量不同处理柄影响向量之间的成对正交程度，定义为 $\Omega_{\mathrm{orth}} = \frac{1}{K(K-1)} \| \hat{W}^{\top} \hat{W} - I \|_2^2$，值越小表示变形子空间越去相关。
- **对数条件数** $\kappa_{\mathrm{log}}$：评估蒙皮基的数值稳定性，$\kappa_{\mathrm{log}} = \log_2 \big( 1 + \frac{\lambda_{\max}(\hat{W}^{\top} \hat{W})}{\lambda_{\min}(\hat{W}^{\top} \hat{W})} \big)$，值越小表示基条件越好。
- **谱熵** $H_{\mathrm{spec}}$：衡量蒙皮权重矩阵的谱分布均匀性，值越接近1表示各处理柄影响力越均衡。

### 主实验结果

**RigNet 数据集**（Table 1）：PhysSkin 在全部三项指标上均取得最优。正交性指标 $\Omega_{\mathrm{orth}}$ 低至 $0.0033 \times 10^{-2}$，对数条件数 $\kappa_{\mathrm{log}}$ 为 $1.0453$，谱熵 $H_{\mathrm{spec}}$ 达到 $0.9999$。相比之下，现有数据驱动方法如 **RigNet**（Xu et al., SIGGRAPH 2020）、**Anymate**（Deng et al., SIGGRAPH 2025）等需要专家标注数据，且无法达到同等的物理一致性；而物理信息方法 **Simplicits**（Modi et al., TOG 2024）虽引入物理先验，但需为每个对象单独训练，不具备泛化能力。PhysSkin 以单一统一模型在前馈方式下完成推理，同时实现最优物理质量，验证了可泛化物理蒙皮的有效性。

**ShapeNet 数据集**（Table 2）：在跨类别泛化场景下，PhysSkin 同样保持显著优势。$\Omega_{\mathrm{orth}}$ 为 $0.0098 \times 10^{-2}$，$\kappa_{\mathrm{log}}$ 为 $1.0460$，$H_{\mathrm{spec}}$ 为 $0.9997$。该结果表明模型在面对训练未见过的形状类别和拓扑结构时，仍能产出物理一致且数值稳定的蒙皮场。

**定性结果**：Figure 4 和 Figure 7 分别展示了 RigNet 和 ShapeNet 测试集上的混合蒙皮场可视化。PhysSkin 生成的蒙皮场在空间上平滑过渡，处理柄影响区域边界清晰，而基线方法常出现权重集中、区域重叠或边界模糊等问题。Figure 5 进一步展示了对 RigNet 测试集中全新形状的泛化结果，所有结果均由单一模型生成，无需微调。

### 实时物理动画性能

Table 3 对比了 PhysSkin 子空间模拟与全空间模拟器 FEM 和 MPM 的单步模拟耗时。得益于蒙皮子空间的降维表示，PhysSkin 在保持物理合理性的同时将模拟成本压缩至实时可用的量级，相比全空间方法加速数个数量级。Figure 10 和 Figure 9 分别展示了 RigNet 和 ShapeNet 对象的物理动画结果，Figure 11 进一步展示了对 3DGS 模型的动画效果，验证了方法对不同表示形式的兼容性。

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2603_23194/figures/010_Table_3.jpg]]
*Table 3: Comparison of per-step simulation cost for physics-based animation with full-space simulators FEM [7] and MPM [56]*

### 消融实验

Table 4 报告了在 RigNet 数据集上的消融结果，证实每个组件的必要性：

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2603_23194/figures/011_Table_4.jpg]]
*Table 4: Ablation studies on the RigNet [52] dataset*

- **移除潜在能量损失（w/o $\mathcal{L}_{\mathrm{pot}}$）**：蒙皮场失去物理引导，正交性指标显著恶化。Figure 12 的可视化表明，缺乏能量最小化约束时，蒙皮权重趋于无序分布，无法形成有物理意义的变形子空间。
- **移除空间平滑损失（w/o $\mathcal{L}_{\mathrm{smooth}}$）**：蒙皮权重在空间上出现剧烈跳变，影响变形连续性。
- **移除正交损失（w/o $\mathcal{L}_{\mathrm{orth}}$）**：处理柄间耦合增强，条件数上升，数值稳定性下降。
- **移除在线归一化与冲突感知梯度校正**：训练过程出现梯度干扰和数值漂移，最终收敛质量明显劣于完整模型。

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2603_23194/figures/013_Figure_12.jpg]]
*Figure 12: Top: Trained without*

完整模型在所有指标上均优于任一消融变体，验证了 PISSL 策略中各损失项和稳定化机制的协同作用。

### 失败模式与局限

论文指出当前方法尚未融入语义先验，在处理具有复杂几何结构（如细长部件、嵌套拓扑）的形状时，学习到的蒙皮场表达能力可能受限。此外，模型训练完成后处理柄数量固定，无法动态增减；在极端大变形或拓扑变化场景下的鲁棒性有待进一步验证。这些局限为后续融入语义引导或动态蒙皮结构的工作指明了方向。

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2603_23194/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on RigNet [52] dataset*

![[assets/figures/papers/paper_list_l1049_https_arxiv_org_abs_2603_23194/figures/006_Figure_7.jpg]]
*Figure 7: Qualitative skinning results of our method on unseen objects from the ShapeNet [5] dataset. Zoom in for more details*

## 定位与知识库关联

### 1. 现有方法格局与PhysSkin的切入点

物理动画的核心矛盾在于**表达力、实时性与泛化性之间的三重权衡**。现有工作大致沿三条路线展开，但各自在关键环节上存在瓶颈：

- **数据驱动的神经绑定方法**：以 **RigNet**（Xu et al., SIGGRAPH 2020）、**Anymate**（Deng et al., SIGGRAPH 2025）、**Make-It-Animatable**（Guo et al., CVPR 2025）和 **Puppeteer**（Song et al., NeurIPS 2025）为代表。这类方法从大规模标注数据中学习蒙皮权重或动画参数，能够处理类别内甚至跨类别的形状，但对专家标注（骨骼-蒙皮对应关系、运动序列）的依赖构成了规模化瓶颈。一旦脱离训练分布，蒙皮质量难以保证。

- **物理信息子空间方法**：以 **Simplicits**（Modi et al., ACM Transactions on Graphics 2024）为代表。这类方法通过最小化物理能量来寻找低维变形子空间，无需运动数据即可获得物理一致的蒙皮。但其致命弱点是**每个对象需独立训练**，不具备跨形状泛化能力——每遇到一个新网格，都需要从头优化网络参数。

- **传统全空间模拟器**（FEM、MPM等）：物理精度最高，但每步计算成本高昂，无法满足实时交互需求。

PhysSkin的定位在于**填补上述路线的交叉空白**：它同时追求（1）可泛化性——一个统一模型处理任意形状和离散化；（2）免标注性——仅从静态几何出发，通过物理先验自监督学习；（3）实时性——在学习的蒙皮子空间内执行隐式时间积分。这种“可泛化物理蒙皮”的设定在现有文献中缺乏直接对应物，PhysSkin实质上开创了一个新的方法子类。

### 2. 核心技术差异：连续神经蒙皮场与物理自监督

与基线方法相比，PhysSkin在两个关键维度上做出了根本性改变：

**（1）蒙皮表示：从离散到连续**

所有现有绑定方法（包括RigNet和Anymate）输出的蒙皮权重绑定于特定网格的顶点，这意味着网格分辨率或拓扑一旦改变，权重就需要重新计算或插值。PhysSkin将蒙皮建模为**连续神经场**——一个以空间坐标和形状潜在码为输入、以蒙皮权重为输出的函数。这一设计使得同一模型可以直接处理不同分辨率的网格、点云甚至高斯泼溅（3DGS）模型，无需任何适配。

**（2）训练范式：从数据驱动到物理驱动**

RigNet等依赖专家标注的蒙皮数据，Simplicits虽用物理损失但需逐对象优化。PhysSkin的PISSL策略则完全从静态几何出发，通过三个物理先验损失（潜在能量最小化、空间平滑、正交约束）驱动网络自动发现合理的变形子空间。关键在于，这种学习不依赖任何运动轨迹——网络通过随机采样子空间坐标并最小化其期望势能，隐式地探索低能变形模式。这一机制与Simplicits的逐对象优化有本质区别：PhysSkin通过形状编码器将几何信息压缩为潜在码，使得物理先验可以在不同形状间共享，从而实现泛化。

**（3）训练稳定性：冲突感知梯度校正**

多损失项联合优化中常见的梯度干扰问题在PhysSkin中尤为突出——能量损失倾向于将蒙皮权重推向极端值（0或1），而正交损失和平滑损失则施加相反的约束。PhysSkin引入的**皮肤场在线归一化**和**冲突感知梯度校正**（引用自PCGrad ）是训练收敛的关键工程贡献。消融实验（Table 4）表明，移除任一损失项或稳定性机制都会导致指标显著恶化。

### 3. 适用边界与局限

PhysSkin的适用边界由以下因素界定：

- **物理先验的隐含假设**：PISSL基于势能最小化驱动学习，这隐含假设了物体在静止状态下处于或接近能量极小值。对于需要主动肌肉力或外部约束维持形状的软体（如章鱼触手），静态几何可能无法提供足够的变形子空间信息。论文未验证此类场景。

- **语义盲区**：当前方法完全从几何和物理出发，未融入任何语义先验。这意味着网络可能将几何上分离但功能上耦合的部件分配为独立蒙皮区域（或反之），在处理具有复杂关节结构或功能分区的形状时表达能力受限。论文明确承认这一局限。

- **拓扑不变性假设**：蒙皮框架本身预设了变形是连续的、拓扑保持的。断裂、撕裂或拓扑变化场景超出了当前方法的适用范围。

- **训练成本**：虽然推理是前馈且实时的，但训练需要4张NVIDIA RTX 4090 GPU，且涉及大量体素采样和子空间坐标随机采样。对于超大规模数据集，训练成本仍是一道门槛。

### 4. 开放问题与后续方向

基于上述局限，以下方向值得关注：

1. **语义-物理联合学习**：能否将大规模视觉-语言模型中的语义知识注入形状编码器，使蒙皮场在物理合理的基础上同时尊重功能分区？这可能需要设计新的跨模态对齐损失。

2. **动态拓扑扩展**：对于可切割、可撕裂的软体，蒙皮框架需要动态增删处理柄并重配蒙皮权重。如何在保持物理一致性的前提下实现蒙皮场的在线更新，是一个开放性挑战。

3. **训练效率优化**：能否通过元学习或超网络进一步压缩训练成本，使PhysSkin可以快速适配到新类别？当前的形状编码器（Michelangelo预训练）已经提供了强大的先验，但物理自监督阶段仍需大量采样。

4. **与生成模型的结合**：PhysSkin输出的蒙皮场为3D生成模型（如扩散模型、3D高斯泼溅重建）提供了即插即用的动画接口。如何将蒙皮场作为生成过程的显式条件或隐式正则化项，可能催生“可动画生成”的新范式。

> **注意**：上述开放问题中，部分（如语义融入、拓扑扩展）来自论文明确指出的局限，部分（如与生成模型结合）基于方法特性的合理推演，需在后续文献中验证其实际可行性。

## 原文 PDF

![[paperPDFs/CVPR_2026/PhysSkin_Real_Time_and_Generalizable_Physics_Based_Animation_via_Self_Supervised_Neural_Skinning.pdf]]
