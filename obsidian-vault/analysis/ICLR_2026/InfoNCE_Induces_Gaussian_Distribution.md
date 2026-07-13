---
title: "InfoNCE Induces Gaussian Distribution"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/InfoNCE_Induces_Gaussian_Distribution.pdf
project_link: null
code_link: null
openreview_forum_id: BlSH7gNQSq
aliases:
- IGIF
- IIGD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "数据增强的温和度（通过HGR最大相关性量化）限制了可达到的对齐，并在特定条件下推动表示分布向球面均匀分布演化，进而通过高维球形中心极限定理产生渐近高斯投影。"
primary_logic: "InfoNCE目标函数在总体极限下诱导了表示在单位球面上的均匀分布以及范数的薄壳集中，结合麦克斯韦-庞加莱球形中心极限定理，自然导出低维投影的渐近高斯性。"
claims:
- "InfoNCE目标诱导表示中的高斯结构。"
- "对齐被HGR最大相关性所限制。"
- "在总体InfoNCE损失下，均匀分布是唯一最小值。"
- "高维球面均匀分布的低维投影收敛到高斯。"
---

# InfoNCE Induces Gaussian Distribution

> [!tip] 核心洞察
> InfoNCE目标函数在总体极限下诱导了表示在单位球面上的均匀分布以及范数的薄壳集中，结合麦克斯韦-庞加莱球形中心极限定理，自然导出低维投影的渐近高斯性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | InfoNCE诱导高斯分布 |
| 英文题名 | InfoNCE Induces Gaussian Distribution |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=BlSH7gNQSq) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | InfoNCE Gaussian Induction Framework |
| Dataset |  |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

对比学习，特别是InfoNCE损失，已在自监督表示学习中取得显著成功，但其产生的表示为何呈现高斯分布缺乏严格的机理解释。这一理论空白阻碍了对表示统计性质的定量分析，也限制了对下游任务行为的先验推断。本文的核心贡献在于揭示：**InfoNCE目标函数在总体极限下，通过两个关键机制——对齐的有界性与均匀性的全局最优——诱导了表示的高斯结构**。

问题的瓶颈在于：数据增强的强度如何约束表示的对齐程度，以及这种约束如何与均匀性相互作用，最终塑造表示的分布形态。本文引入**HGR最大相关性**（Hirschfeld-Gebelein-Rényi maximal correlation）作为量化增强温和度的核心控制变量，证明了正对对齐被该相关性所上界限制。在对齐达到平台期后，InfoNCE的总体损失退化为球面上均匀分布势能的最小化问题，其唯一最小值正是单位球面上的均匀分布。结合**麦克斯韦-庞加莱球形中心极限定理**，高维球面均匀分布的低维投影渐近收敛到标准高斯，从而自然导出表示的高斯性。对于未归一化表示，进一步引入**薄壳集中假设**——表示范数在高维极限下集中到确定性常数——将高斯投影结果推广到原始表示空间。

在方法定位上，本文属于对比学习理论分析谱系，与**Wang & Isola (2020)** 提出的“对齐-均匀性”分解框架一脉相承，但推进了关键一步：从均匀性的经验观察上升到分布形态的严格推导。与侧重优化动力学或信息论视角的既有工作不同，本文从总体损失的变分结构出发，建立了从增强温和度到高斯投影的完整因果链条。

实验验证覆盖合成数据、CIFAR-10训练动态以及大规模预训练模型（**CLIP**、**DINO**）：合成实验表明，随着批次大小和维度增加，表示范数的变异系数（CV）下降，薄壳集中效应增强，安德森-达令（AD）正态性检验统计量进入接受范围；CIFAR-10训练过程中，高斯性随训练逐步增强；预训练模型的诊断进一步确认，对比学习方法比有监督训练产生更显著的薄壳集中和坐标高斯性。

本文的理论是渐近的（$d \to \infty$），且依赖对齐平台期和薄壳集中的假设，未从优化动力学角度证明这些条件必然成立。有限负样本效应也未被纳入分析。这些限制指出了未来工作的方向：从SGD动力学直接推导高斯性，以及为非渐近情形提供有限样本保证。

对比学习（contrastive learning）已成为自监督表示学习的主流范式，其核心机制是通过InfoNCE损失函数拉近正样本对（positive pairs）的表示，同时推开负样本对（negative pairs）的表示。这一范式在视觉和语言领域催生了CLIP、DINO等强基线模型，其下游泛化能力已被广泛验证。然而，一个根本性的理论问题长期悬而未决：**InfoNCE训练产生的表示服从何种概率分布？**

该问题的核心瓶颈在于：对比学习表示的分布特性缺乏机理解释，这直接阻碍了对其统计性质的严格分析。具体而言，现有工作虽已揭示InfoNCE优化过程中对齐（alignment）与均匀性（uniformity）的张力（Wang & Isola, 2020），但尚未回答以下问题：表示本身是否具有某种可表征的分布结构？若存在，该结构从何而来？

本文的出发点正是填补这一理论空白。作者观察到，对比学习产生的表示在经验上呈现出显著的高斯特征——低维投影近似正态分布，范数呈现高维薄壳集中（thin-shell concentration）。然而，这一现象的内在数学机制尚未被阐明。论文的核心追问是：**InfoNCE目标函数本身是否诱导了表示的高斯结构？如果答案是肯定的，其因果链条是什么？**

为回答这一问题，论文从InfoNCE的总体极限（population limit）入手，建立了从数据增强温和度（augmentation mildness）到球面均匀分布、再到渐近高斯投影的完整推导路径。其关键洞察在于：数据增强的温和度——通过Hirschfeld-Gebelein-Rényi（HGR）最大相关性量化——限制了正对对齐的可达上界，并在特定条件下推动表示分布向单位球面上的均匀分布演化；而高维球面均匀分布在固定低维投影上，由Maxwell-Poincaré球形中心极限定理保证收敛到高斯分布。

这一理论框架的意义在于：它将对比学习中分散的经验观察——薄壳集中、坐标正态性、白化增强均匀性——统一到一个连贯的数学图像中，为后续的表示质量分析、异常检测、不确定性量化等下游任务提供了概率基础。

## 核心方法与创新机理

本文的核心创新在于首次从机制层面揭示了InfoNCE对比学习目标函数为何会诱导出高斯分布的表示。与以往将高斯性视为经验现象的工作不同，本文构建了一个从数据增强温和度到表示均匀性、再到渐近高斯投影的完整因果链条，并给出了两条互补的理论路径。

### 创新一：将数据增强温和度纳入理论框架

此前的对比学习理论分析（如Wang & Isola, 2020）主要关注对齐-均匀性分解，但未解释对齐的上限由什么决定。本文引入Hirschfeld-Gebelein-Rényi (HGR)最大相关性来量化数据增强的“温和度”（augmentation mildness），参数化为 $\eta_2$：

$$\eta_2 := \sup_{g\in L^2(p_X),\,\mathrm{Var}(g)>0} \frac{\mathrm{Var}(\mathbb{E}[g(X)\mid X_0])}{\mathrm{Var}(g(X))}$$

该参数等于视图 $X$ 与原始样本 $X_0$ 之间HGR最大相关系数的平方，即 $\eta_2 = \rho_m^2(X, X_0)$。基于此，本文证明了正对对齐的上界：

$$\mathbb{E}_{(u,v)\sim\pi}[u\cdot v] \le \eta_2 + (1-\eta_2)\|m(\mu)\|^2$$

这一上界将表示的对齐程度与数据增强强度直接挂钩：增强越强（$\eta_2$ 越小），可达到的对齐上限越低。该发现为理解对比学习的表示质量提供了一个可控的因果旋钮。

### 创新二：InfoNCE总体损失诱导球面均匀分布

本文在总体InfoNCE损失（无限负样本极限）下证明，均匀性势能 $\Phi(\mu)$ 在单位球面 $\mathbb{S}^{d-1}$ 上的唯一最小值是均匀分布 $\sigma$（Lemma 2）。结合对齐上界，当训练达到对齐平台期（即 $\mathbb{E}_{(u,v)\sim\pi}[u\cdot v] = \eta_2 + r_{\mathrm{plat}}$，其中 $r_{\mathrm{plat}} \le 0$）时，InfoNCE目标函数驱动归一化表示向球面均匀分布收敛。

这一结论将Wang & Isola (2020)的对齐-均匀性分解推进到了分布层面的严格刻画，而非仅停留在经验指标层面。

### 创新三：高维球面均匀性导出渐近高斯投影

本文的关键洞察在于将球面均匀分布与高斯性通过麦克斯韦-庞加莱球形中心极限定理（Diaconis & Freedman, 1987）联系起来：当维度 $d \to \infty$ 时，球面均匀分布的低维投影收敛到标准高斯分布：

$$\sqrt{d}\, u_k \Rightarrow \mathcal{N}(0, I_k)$$

对于未归一化的表示，本文进一步引入薄壳集中假设（$\frac{r}{r_0} \xrightarrow{d \to \infty} 1$），将高斯性推广到：

$$\sqrt{d}\, z_k \Rightarrow \mathcal{N}(0, r_0^2 I_k)$$

这一理论路径将InfoNCE → 均匀性 → 高斯性串联为完整的因果链，填补了此前“对比学习产生高斯表示”缺乏机理解释的空白。

### 创新四：正则化路径提供独立于训练动力学的替代证明

为规避对齐平台期假设对训练动力学的依赖，本文提出了一条正则化路径：在InfoNCE目标中加入KL散度正则项，引导表示分布向截断高斯 $\gamma_\lambda^B$ 靠近：

$$J(f) = \Phi(\mu) - \alpha \mathbb{E}_{(u,v)\sim\pi}[u\cdot v] + \beta\,\mathrm{KL}(\rho\|\gamma_\lambda^B)$$

在温和条件下（Assumption 3），当 $d \to \infty$ 时，均匀分布 $\sigma$ 是该正则化目标的渐近最优解（Theorem 1），从而在不依赖训练动态假设的情况下导出高斯性。两条路径互为补充，增强了结论的稳健性。

### 与现有工作的本质差异

| 维度 | 现有工作 | 本文贡献 |
|------|---------|---------|
| 高斯性的来源 | 经验观察，无机制解释 | 从InfoNCE目标函数严格导出 |
| 对齐上限 | 未量化 | HGR最大相关性给出精确上界 |
| 均匀性 | 经验指标 | 总体损失下均匀分布是唯一最小值 |
| 高斯投影 | 无理论连接 | 球形CLT建立均匀性→高斯性桥梁 |
| 理论路径 | 单一 | 对齐平台期路径 + 正则化路径，双线互补 |

需要指出的是，本文的理论证明是渐近的（$d \to \infty$），未提供有限维度的精确偏差界；对齐平台期和薄壳集中作为推导中的关键假设，其必然性未从优化动力学角度得到证明。这些构成了当前理论框架的主要局限。

本文提出一个理论框架，用于解释对比学习（InfoNCE）为何在表示空间中诱导出高斯结构。该框架的核心逻辑链由四个模块组成，从数据增强的温和度出发，经由对齐上限和均匀性优化，最终通过高维几何的概率定理导出渐近高斯性。

### 模块一：数据增强温和度量化（HGR最大相关）

框架的起点是对数据增强强度的形式化度量。给定原始样本 $X_0$ 和经过两次独立增强得到的视图 $X, Y \sim \mathcal{A}(\cdot|X_0)$，定义增强温和度参数：

$$\eta_2 := \sup_{g\in L^2(p_X),\,\mathrm{Var}(g)>0} \frac{\mathrm{Var}(\mathbb{E}[g(X)\mid X_0])}{\mathrm{Var}(g(X))}$$

该参数等于 $X$ 与 $X_0$ 之间 Hirschfeld-Gebelein-Rényi (HGR) 最大相关系数的平方，即 $\eta_2 = \rho_m^2(X, X_0)$。$\eta_2$ 刻画了从增强视图可预测原始样本的程度：$\eta_2$ 越大，增强越弱（信息保留越多）；$\eta_2$ 越小，增强越强（信息破坏越多）。这一量化为后续的对齐上限提供了关键控制变量。

### 模块二：对齐上限（Alignment Bound）

在总体 InfoNCE 损失下，正对表示 $(u, v)$ 的点积期望（对齐）被 $\eta_2$ 严格约束：

$$\mathbb{E}_{(u,v)\sim\pi}[u\cdot v] \le \eta_2 + (1-\eta_2)\|m(\mu)\|^2$$

其中 $m(\mu) = \mathbb{E}_{u\sim\mu}[u]$ 是归一化表示的均值向量。该上界揭示了一个核心机制：**增强的温和度直接限制了可达到的对齐程度**。当表示均值趋近于零时（即分布趋于球面对称），对齐上限退化为 $\eta_2$ 本身。这意味着，无论编码器如何优化，正对相似度都无法超越数据增强所保留的互信息上限。

### 模块三：均匀性势能最小化

总体 InfoNCE 损失可分解为对齐项和均匀性势能项：

$$\mathcal{L}(\mu,\pi) = -\alpha \mathbb{E}_{(u,v)\sim\pi}[u\cdot v] + \Phi(\mu)$$

其中 $\Phi(\mu) = \mathbb{E}_{u\sim\mu}\log\mathbb{E}_{v\sim\mu}[\exp(\alpha\, u\cdot v)]$ 是均匀性势能。关键结论是：**$\Phi(\mu)$ 的唯一全局最小值是球面上的均匀分布 $\sigma$**（Lemma 2）。当对齐达到平台期（即正对相似度饱和于 $\eta_2$ 附近）时，InfoNCE 损失的进一步下降只能通过最小化 $\Phi(\mu)$ 来实现，这推动归一化表示 $\{u = f(x)/\|f(x)\|\}$ 向单位球面 $S^{d-1}$ 上的均匀分布收敛。

这一模块将对比学习的优化目标与球面均匀分布建立了直接联系，是高斯性推导的关键桥梁。

### 模块四：高维球面中心极限定理

框架的最后一步利用 Maxwell-Poincaré 球形中心极限定理：若 $U_d$ 均匀分布在 $d$ 维单位球面 $S^{d-1}$ 上，则当 $d \to \infty$ 时，其前 $k$ 个坐标的联合分布收敛到标准高斯：

$$\sqrt{d}\,(U_{d,1}, \ldots, U_{d,k}) \Rightarrow \mathcal{N}(0, I_k)$$

将模块三的均匀性结论与这一定理结合，即得归一化表示的低维投影渐近服从高斯分布。对于未归一化表示 $z = f(x)$，框架引入**薄壳集中假设**（Assumption 2）：当维度 $d \to \infty$ 时，表示半径 $r = \|z\|$ 集中到常数 $r_0$，即 $r/r_0 \to 1$。在此假设下，未归一化表示的投影同样收敛到高斯：

$$\sqrt{d}\, z_k \Rightarrow \mathcal{N}(0, r_0^2 I_k)$$

### 正则化变体：绕过训练动力学的替代路径

除上述基于对齐平台期假设的路径外，框架还提供了一条更弱的理论路径：在 InfoNCE 损失中加入 KL 散度正则项，直接引导表示分布向截断高斯 $\gamma_\lambda^B$ 靠近：

$$J(f) = \Phi(\mu) - \alpha \mathbb{E}_{(u,v)\sim\pi}[u\cdot v] + \beta\,\mathrm{KL}(\rho\|\gamma_\lambda^B)$$

该正则化目标的最优解在 $d \to \infty$ 时收敛到球面均匀分布（Theorem 1），从而不依赖训练动力学的具体行为即可导出高斯性。

### 输入输出流总结

整个框架的输入输出流可概括为：

- **输入**：原始数据分布 $p_{X_0}$，增强通道 $\mathcal{A}(\cdot|X_0)$，编码器 $f$。
- **中间表示**：归一化表示 $u = f(x)/\|f(x)\|$ 的分布 $\mu$，正对联合分布 $\pi$。
- **控制变量**：增强温和度 $\eta_2$（由数据增强策略决定），维度 $d$，批次大小 $N$（通过有限样本效应影响均匀性收敛速度）。
- **输出**：表示 $z = f(x)$ 的低维投影渐近服从高斯分布 $\mathcal{N}(0, r_0^2 I_k)$。

该框架的理论保证是渐近的（$d \to \infty$），未给出有限维度的精确偏差。对齐平台期和薄壳集中作为关键假设，其是否在训练中必然达成尚未从优化动力学角度得到证明。总体 InfoNCE 分析假设无限负样本（$N \to \infty$），实际有限批次效应未纳入分析。这些限制在解读框架结论时需特别注意。

### 总体InfoNCE损失函数

论文从有限批次InfoNCE的总体极限出发，建立分析框架。当负样本数 $N \to \infty$ 时，经验损失收敛到如下总体泛函：

$$\mathcal{L}(\mu,\pi) = -\alpha \mathbb{E}_{(u,v)\sim\pi}[u\cdot v] + \Phi(\mu)$$

其中 $\Phi(\mu) := \mathbb{E}_{u\sim\mu}\log\mathbb{E}_{v\sim\mu}\exp(u\cdot v)$ 为均匀性势能，$\mu$ 为归一化表示 $u = f(x)/\|f(x)\|$ 的边缘分布，$\pi$ 为正对 $(u,v)$ 的联合分布，$\alpha = 1/\tau$ 为温度倒数。该分解将InfoNCE目标拆解为两项：正对对齐项 $-\alpha\mathbb{E}[u\cdot v]$ 和推动表示分布趋向均匀的势能项 $\Phi(\mu)$。

**关键性质**：$\Phi(\mu)$ 在单位球面 $\mathcal{S}^{d-1}$ 上被均匀分布 $\sigma$ 唯一最小化（Lemma 2），这为高斯性的导出奠定了几何基础。

### 模块一：对齐上界与增强温和度

数据增强的强度通过HGR最大相关系数量化，定义增强温和度参数：

$$\eta_2 := \sup_{g\in L^2(p_X),\,\mathrm{Var}(g)>0} \frac{\mathrm{Var}(\mathbb{E}[g(X)\mid X_0])}{\mathrm{Var}(g(X))}$$

$\eta_2$ 等于视图 $X$ 与原始样本 $X_0$ 之间HGR最大相关系数的平方，即 $\eta_2 = \rho_m^2(X, X_0)$。$\eta_2$ 越大，增强越温和（视图越可预测）；$\eta_2$ 越小，增强越激进（视图差异越大）。

基于此，正对对齐存在上界（Proposition 1）：

$$\mathbb{E}_{(u,v)\sim\pi}[u\cdot v] \le \eta_2 + (1-\eta_2)\|m(\mu)\|^2$$

其中 $m(\mu) = \mathbb{E}_{u\sim\mu}[u]$ 为表示分布的均值。该上界揭示：增强温和度 $\eta_2$ 从根本上限制了可达到的对齐程度——无论编码器能力多强，正对相似度无法超越 $\eta_2$（当 $m(\mu)=0$ 时）。

### 模块二：对齐平台期假设与球面均匀性

理论推导的核心假设是对齐平台期（Assumption 1）：

$$\mathbb{E}_{(u,v)\sim\pi}[u\cdot v] = \eta_2 + r_{\mathrm{plat}}$$

其中 $r_{\mathrm{plat}} \le 0$ 为非正残差。该假设认为训练使对齐饱和到接近HGR上界的水平。在此条件下，$\Phi(\mu)$ 的优化推动 $\mu$ 向球面均匀分布 $\sigma$ 收敛——因为 $\Phi(\mu)$ 的唯一最小值在 $\sigma$ 处达到，而对齐项已达平台期无法进一步优化。

### 模块三：麦克斯韦-庞加莱球形中心极限定理

高维球面均匀分布具有关键的渐近性质：固定 $k$ 维投影收敛到标准高斯（Lemma 3）：

$$\sqrt{d}\, u_k \Rightarrow \mathcal{N}(0, I_k) \quad (d \to \infty)$$

其中 $u_k$ 为从 $\sigma$ 采样的归一化向量在任意固定 $k$ 维子空间上的投影。该结论源自Diaconis & Freedman (1987)的经典结果，是连接球面均匀性与高斯性的数学桥梁。

### 模块四：薄壳集中与未归一化表示的高斯性

为将高斯性推广到未归一化表示 $z = f(x)$，引入薄壳集中假设（Assumption 2）：

$$\frac{r}{r_0} \xrightarrow{d \to \infty} 1$$

即表示半径 $r = \|z\|$ 在高维下集中到常数 $r_0$。在此假设下，未归一化表示的投影同样收敛到高斯：

$$\sqrt{d}\, z_k \Rightarrow \mathcal{N}(0, r_0^2 I_k) \quad (d \to \infty)$$

薄壳效应使归一化与未归一化表示的投影行为在高维极限下等价，仅方差缩放 $r_0^2$ 不同。

### 模块五：正则化InfoNCE变体

作为不依赖训练动态假设的替代路径，论文提出加入KL散度正则化的目标函数：

$$J(f) = \Phi(\mu) - \alpha \mathbb{E}_{(u,v)\sim\pi}[u\cdot v] + \beta\,\mathrm{KL}(\rho\|\gamma_\lambda^B)$$

其中 $\rho$ 为未归一化表示 $z$ 的分布，$\gamma_\lambda^B(dz) = c_{B,\lambda} e^{-\lambda\|z\|^2}\mathbf{1}_B(z)dz$ 为截断高斯参考测度。Proposition 3 证明径向部分的最优选择恰为截断高斯径向分布，优化退化为仅对角度分布 $\mu$ 的优化。在高维极限下，均匀分布 $\sigma$ 渐近最小化 $\tilde{J}(\mu)$（Theorem 1），从而直接导出高斯性，无需对齐平台期假设。

### 模块间因果链条

整个推导的因果逻辑为：**增强温和度 $\eta_2$ → 对齐上界受限 → 训练使对齐饱和（平台期假设）→ 优化压力转向 $\Phi(\mu)$ → $\mu$ 趋近球面均匀分布 $\sigma$ → 球形CLT导出投影高斯性 → 薄壳集中将结论推广至未归一化表示**。正则化路径则绕过平台期假设，通过KL散度直接引导分布向截断高斯收敛。

## 实验与关键发现

### 合成数据实验：薄壳集中与高斯性诊断

论文首先在合成数据上验证核心假设。使用拉普拉斯分布作为输入，训练一个简单的线性编码器，通过InfoNCE目标进行对比学习。Figure 3左侧展示了表示范数的统计量与批次大小的关系：随着维度 $d$ 和批次大小 $N$ 的增加，范数的变异系数（CV，定义为 $\text{CV} = \text{std}(\{\|z_i\|\}_{i=1}^N) / \text{mean}(\{\|z_i\|\}_{i=1}^N)$）单调下降，表明薄壳集中效应增强。Figure 3中上方的范数直方图进一步直观展示了半径分布的收紧。

Figure 3下方的正态性诊断结果提供了关键证据：Anderson-Darling (AD) 检验统计量和 D'Agostino-Pearson (DP) 检验通过率均落在高斯接受范围内，说明各个坐标的分布与高斯分布高度一致。这一结果与输入分布（拉普拉斯）的非高斯性形成鲜明对比，表明编码器将非高斯输入“推前”（pushforward）为近似高斯表示（见 Figure 11）。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_BlSH7gNQSq/figures/014_Figure_11.jpg]]
*Figure 11: Encoder “pushforward”. On synthetic data, the encoder maps Laplace-distributed inputs to approximately Gaussian representations. Because both source and target families admit tractable likelihoods, we can score entire sets and observe consistently high correlation across different augmentation strengths*

### 对齐与均匀性的动态关系

Figure 2 揭示了训练过程中对齐与均匀性的演化模式。在合成数据上，正对的对齐几乎在所有配置下都达到接近最优的水平，而均匀性则随着批次大小或维度的增加持续改善。这一现象支持了 Assumption 1（对齐平台期假设）：对齐被增强温和度 $\eta_2$（即 HGR 最大相关系数的平方）所限制，训练很快达到该上界附近，此后优化主要驱动表示向球面均匀分布收敛。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_BlSH7gNQSq/figures/002_Figure_2.jpg]]
*Figure 2: Uniformity vs. alignment across settings. A simple linear encoder trained on synthetic Laplace data exhibits (i) near-optimal alignment across all configurations and (ii) steadily improving uniformity as batch size or dimensionality grow*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_BlSH7gNQSq/figures/011_Figure_8.jpg]]
*Figure 8: Alignment and uniformity vs. dimensionality. Histogram view of cosine similarities for positive pairs (alignment) and negatives (uniformity), corresponding to Fig. 2. As dimensionality increases, alignment stays high while uniformity improves, pushing negative-pair similarities toward zero. The middle panel is a zoom of the left; the right panel highlights that with very small batch sizes, increasing dimensionality offers limited uniformity improvement*

Figure 7 和 Figure 8 以余弦相似度直方图的形式补充了这一观察：随着批次大小增大，负样本对的相似度集中在零附近；随着维度增加，同样的均匀化趋势出现。值得注意的是，当维度极低时，增大批次大小几乎不带来均匀性增益；反之，当批次大小极小时，增大维度的均匀性改善也有限——这表明维度和负样本数量在驱动均匀性方面存在互补关系。

### CIFAR-10 训练动态

在 CIFAR-10 上使用两层 MLP 进行 InfoNCE 训练，Figure 4 展示了高斯性随训练进程逐步增强的三个指标：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_BlSH7gNQSq/figures/004_Figure_4.jpg]]
*Figure 4: CIFAR-10 training dynamics. A two-layer MLP trained with InfoNCE on CIFAR-10 exhibits increasing Gaussianity over training. Left: representation norms concentrate as indicated by declining CV (Eq. 20). Middle: the AD statistic decreases from non-Gaussian levels into the normal range. Right: the fraction of coordinates passing the DP normality test rises steadily*

- **范数集中**：CV 随训练 epoch 增加而持续下降，表明表示半径逐渐集中到薄壳上。
- **AD 统计量**：从非高斯水平下降并进入正态接受范围。
- **DP 通过率**：通过 DP 正态性检验的坐标比例稳步上升。

这三个趋势的一致性为“InfoNCE 在训练过程中诱导高斯结构”提供了实证支持。

### 跨设置高斯性诊断

Table 1 汇总了不同数据和训练设置下的高斯性诊断结果。对比学习方法（CIFAR-10 上的 ResNet-18 对比训练）在未归一化嵌入上表现出极低的 CV（0.09）、高 AD 正态特征比例（96.1%）和高 DP 正态特征比例（94.5%）。相比之下，有监督训练的 ResNet-18 在 CIFAR-10 上的 AD 正态特征比例仅为 62.5%，DP 正态特征比例为 55.5%，说明有监督训练并不诱导同样程度的高斯结构。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_BlSH7gNQSq/figures/005_Table_1.jpg]]
*Table 1: Gaussianity diagnostics across data and training settings. We report norm concentration (CV) and Gaussianity via AD and DP tests (average statistic and fraction of compliant coordinates). Lower AD and higher DP indicate closer Gaussian agreement. Binary E0/E50/E100 denote evaluation at epochs 0/50/100; other results are from the end of training. Results use unnormalized embeddings*

这一差异在更大规模设置中保持一致：ImageNet 上有监督训练的 ResNet-34 的 AD 正态特征比例为 59.0%，DP 正态特征比例为 58.6%，远低于对比学习方法的相应指标。

### 预训练模型的高斯性诊断

Table 2 将分析扩展到大规模预训练模型。自监督模型（CLIP、DINO）在未归一化嵌入上表现出接近高斯的坐标分布：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_BlSH7gNQSq/figures/006_Table_2.jpg]]
*Table 2: Gaussianity diagnostics for pretrained models. Coordinate-wise Gaussianity via AD and DP tests (average statistic and fraction of compliant coordinates). Test thresholds are indicated in headers. Results shown for Unnormalized / Normalized embeddings*

- **DINO（MS-COCO）**：AD 正态特征比例 97.0%，DP 正态特征比例 99.2%。
- **CLIP 图像编码器（MS-COCO）**：AD 正态特征比例 93.8%，DP 正态特征比例 97.7%。
- **CLIP 图像编码器在 ImageNet-R 的 Sketch 和 Painting 域上**同样展现出强高斯特征。

归一化后的嵌入普遍表现出更好的高斯性，这与理论预测一致：归一化操作直接将表示投影到单位球面上，而球面均匀分布的低维投影在高维极限下收敛到高斯。

Figure 6 进一步比较了不同模型的薄壳集中程度。对比学习方法（CLIP、DINO）的半径分布比有监督模型（DenseNet、ResNet）更紧致，CV 更低，与 Table 1 和 Table 2 中的范数集中指标一致。

### 白化增强均匀性

Figures 9 和 10 分析了白化（whitening）对表示均匀性的影响。对于未归一化表示（Figure 9），白化显著将负样本对的余弦相似度分布推向零附近，增强了均匀性。对于已归一化的表示（Figure 10），白化仍能提供适度但一致的改善——归一化表示本身已接近均匀分布，白化进一步优化了这一性质。这一实验间接支持了均匀性是 InfoNCE 优化的核心驱动力之一。

### 实验证据的局限性

需要指出的是，上述实验证据存在以下局限：

- **有限维度偏差未量化**：理论结果是渐近的（$d \to \infty$），Table 1 和 Table 2 中的高斯性诊断虽然接近正态接受范围，但并非完美匹配。论文未给出有限维度下的精确偏差估计。
- **对齐平台期的因果性未证明**：Figure 2 展示了对齐先达到平台期、均匀性后改善的现象，但这仅是对训练动态的观察，并未从优化动力学角度证明这一顺序必然发生。
- **有限批次效应未纳入**：所有实验均使用有限批次大小，而总体 InfoNCE 分析假设 $N \to \infty$。Table 1 中不同批次大小的结果可部分反映批次大小的影响，但未系统分析有限负样本带来的偏差。

## 定位与知识库关联

### 核心贡献定位

本文填补了对比学习领域的一个理论空白：**InfoNCE目标函数为什么会在表示空间中诱导出高斯结构**。此前的工作——如**Wang & Isola (2020)** 将InfoNCE分解为对齐项与均匀性势能——已揭示了表示趋向球面均匀分布的倾向，但并未进一步解释这种均匀分布如何（以及为何）在高维极限下转化为高斯投影。本文的关键推进在于**在球面均匀性与高斯性之间建立了严格的概率论桥梁**：通过麦克斯韦-庞加莱球形中心极限定理（Diaconis & Freedman, 1987），证明了高维球面均匀分布的低维投影必然收敛到各向同性高斯分布。

### 方法谱系：两条理论路线

本文提出了两条通向高斯性的互补理论路线，各自有不同的假设强度和适用范围：

**路线一：对齐平台期分析（Alignment Plateau Route）**

这条路线依赖于两个关键假设：
- **对齐平台期假设（Assumption 1）**：训练达到的对齐 $\mathbb{E}_{(u,v)\sim\pi}[u\cdot v]$ 被数据增强的HGR最大相关性 $\eta_2$ 所限制，且饱和于 $\eta_2 + r_{\text{plat}}$（$r_{\text{plat}} \le 0$）。这一假设的实证支撑来自Figure 2：对齐在训练早期即达到近最优水平，而均匀性随批次大小和维度增加持续改善。
- **薄壳集中假设（Assumption 2）**：未归一化表示的半径 $r$ 在高维极限下集中于一个确定性常数 $r_0$，即 $r/r_0 \to 1$（$d \to \infty$）。这一假设在Figure 3和Figure 4中得到实证验证：变异系数（CV）随维度和批次大小单调下降，训练过程中CV持续降低。

该路线的**核心因果链**为：增强温和度 $\eta_2$ → 限制可达到的对齐上界 → 在总体InfoNCE损失下，均匀分布成为唯一最小值（Lemma 2）→ 归一化表示收敛到球面均匀分布 → 麦克斯韦-庞加莱定理导出低维投影的渐近高斯性 → 薄壳集中将高斯性从归一化表示扩展到未归一化表示。

**路线二：正则化替代路径（Regularized Surrogate Route）**

这条路线通过向InfoNCE目标中加入KL散度正则项 $J(f) = \Phi(\mu) - \alpha \mathbb{E}_{(u,v)\sim\pi}[u\cdot v] + \beta\,\mathrm{KL}(\rho\|\gamma_\lambda^B)$，直接引导表示分布向截断高斯 $\gamma_\lambda^B$ 靠近。该路线的优势在于**不依赖训练动力学的假设**（如对齐平台期），而是通过优化目标本身的结构保证高斯性。Proposition 3进一步证明，当径向分量选择为截断高斯径向分布时，优化问题简化为仅对角分布 $\mu$ 的优化，这大幅降低了理论分析的复杂性。

两条路线的**互补关系**体现在：路线一解释了标准InfoNCE训练中高斯性涌现的机制，但需要较强的经验假设；路线二提供了更严格的理论保证，但引入了额外的正则化项。

### 与相关工作的关系

**均匀性-对齐框架的延伸**：本文直接建立在**Wang & Isola (2020)** 的均匀性-对齐分解之上，但突破了该框架的局限——后者仅预测表示趋向球面均匀分布，未解释为何在实践中观测到的高斯结构如此普遍。本文通过引入球形中心极限定理，完成了从"均匀性"到"高斯性"的理论跃迁。

**数据增强理论的深化**：本文引入的HGR最大相关性 $\eta_2 = \rho_m^2(X, X_0)$ 为数据增强的"温和度"提供了严格的量化工具。这与**Tian et al. (2020)** 和**von Kügelgen et al. (2021)** 关于增强不变性的讨论形成呼应，但本文将其直接嵌入到对齐上界的推导中（Proposition 1, Eq. 6），从而建立了增强强度与表示高斯性之间的定量联系。

**与监督学习的对比**：Table 1和Table 2的实证结果表明，监督训练（ResNet-18/34 on CIFAR-10/ImageNet）产生的表示在坐标级高斯性检验中显著偏离正态，而对比学习模型（包括自监督的DINO和大规模预训练的CLIP）则表现出接近高斯的行为。Figure 6进一步显示，虽然监督模型也呈现一定程度的薄壳集中，但对比学习模型的半径分布更为紧致（CV更低）。这表明**高斯性并非深度表示的普遍属性，而是InfoNCE类目标函数的特定产物**。

### 适用边界与局限

**渐近性质的有限维度偏差**：本文的核心理论结论是渐近的（$d \to \infty$），未给出有限维度的精确偏差。尽管Diaconis & Freedman (1987)提供了 $O(d^{-1})$ 的收敛速率，但实际表示维度（通常为128-2048）下的高斯近似质量仍需通过Table 1/2中的AD和DP检验来经验评估。

**训练动力学未纳入分析**：路线一的对齐平台期假设和薄壳集中假设虽然在实验中得到了验证，但本文未从SGD优化动力学的角度证明这些条件必然在训练中达成。这意味着理论预测的高斯性依赖于"训练成功"这一前提——如果优化未能达到对齐平台期，高斯性可能不会涌现。

**无限负样本假设**：总体InfoNCE分析假设 $N \to \infty$（无限负样本），实际训练中的有限批次效应未纳入理论框架。Wang & Isola (2020, Thm. 1)提供了 $O(N^{-1/2})$ 的偏差上界，但这一偏差如何影响高斯性的有限样本表现仍需进一步研究。

**增强温和度的可估计性**：HGR最大相关性 $\eta_2$ 在理论中扮演核心角色，但在实际应用中难以直接从数据中估计。本文在合成实验中通过已知的拉普拉斯分布验证了理论预测，但在真实数据集上如何量化 $\eta_2$ 仍是一个开放问题。

### 开放问题

1. **优化动力学与高斯性的直接联系**：是否可以从SGD的随机微分方程描述出发，直接推导出表示分布向高斯演化的动力学，而无需依赖对齐平台期假设？这将使理论更加自洽。

2. **其他自监督损失的普适性**：Barlow Twins、VICReg、BYOL等非对比自监督方法是否也诱导类似的高斯结构？如果答案是肯定的，则高斯性可能是更广泛的自监督学习原理（如信息最大化或冗余减少）的普遍结果；如果否定的，则高斯性将成为区分InfoNCE类方法与其他方法的理论特征。

3. **高斯性对下游任务的因果影响**：表示的高斯性质如何定量影响下游分类、异常检测、分布外检测等任务的性能？例如，高斯表示是否天然适合线性探测（因为线性分类器在高斯数据上的最优性），或者是否有利于校准和不确定性估计？

4. **有限负样本的非渐近理论**：能否为有限批次大小 $N$ 的情况提供非渐近的高斯近似保证？这在 $N$ 相对于维度 $d$ 较小（即信息瓶颈情况）时尤为重要。

5. **白化与高斯性的关系**：Figure 9和Figure 10显示白化可以进一步增强表示的均匀性，这是否意味着白化操作使表示更接近理论预测的渐近高斯分布？白化与InfoNCE目标之间的理论联系值得深入探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/InfoNCE_Induces_Gaussian_Distribution.pdf]]
