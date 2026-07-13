---
title: "B³-Seg: Camera-Free, Training-Free 3DGS Segmentation via Analytic EIG and Beta-Bernoulli Bayesian Updates"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/B_Seg_Camera_Free_Training_Free_3DGS_Segmentation_via_Analytic_EIG_and_Beta_Bernoulli_Bayesian_Updates.pdf
project_link: null
code_link: null
aliases:
- BS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将分割重构为序贯Beta-Bernoulli贝叶斯更新，并引入解析期望信息增益（EIG）进行主动视图选择，从而在无相机先验条件下快速降低不确定性。
primary_logic: 通过贝叶斯重构将分割转化为序贯决策问题，利用EIG的解析形式贪婪选择信息量最大的视图，不仅实现秒级开放词汇分割，还从理论上保证了自适应单调性与子模性，进而获得(1-1/e)近似最优性。
claims:
- B³-Seg在LERF-Mask和3D-OVS数据集上，仅使用20个主动选择视图和约12秒总时间，取得与依赖相机/标签的监督方法相当的分割精度。
- 解析EIG与真实信息增益（IG）强相关（r=0.964），验证了EIG作为轻量级代理的有效性。
- EIG驱动策略在每次迭代中产生最大的后验熵降，收敛快于均匀采样和重建相机采样。
- 证明了EIG满足自适应单调性与自适应子模性，从而贪婪策略达到(1-1/e)近似最优。
---

# B³-Seg: Camera-Free, Training-Free 3DGS Segmentation via Analytic EIG and Beta-Bernoulli Bayesian Updates

> [!tip] 核心洞察
> 通过贝叶斯重构将分割转化为序贯决策问题，利用EIG的解析形式贪婪选择信息量最大的视图，不仅实现秒级开放词汇分割，还从理论上保证了自适应单调性与子模性，进而获得(1-1/e)近似最优性。

| 字段 | 内容 |
|------|------|
| 中文题名 | B³-Seg：基于解析期望信息增益与Beta-Bernoulli贝叶斯更新的无相机、无需训练3D高斯泼溅分割 |
| 英文题名 | B³-Seg: Camera-Free, Training-Free 3DGS Segmentation via Analytic EIG and Beta-Bernoulli Bayesian Updates |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.17134) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | B³-Seg |
| Dataset | LERF-Mask, 3D-OVS |

> [!tip] 效果简介
> - LERF-Mask (mean over scenes) 上，mIoU / mBIoU 84.5 / 81.0 vs 69.6 / 65.1 (FlashSplat Uniform-Sphere) (+14.9 / +15.9)。
> - 3D-OVS (Bed) 上，mIoU 97.1 vs 91.7 (FlashSplat Uniform-Sphere) (+5.4)。
> - 3D-OVS (Bench) 上，mIoU 92.2 vs 86.9 (FlashSplat Uniform-Sphere) (+5.3)。

## 概要

### 问题瓶颈

三维高斯泼溅（3DGS）的分割是实现场景编辑、对象操作等交互式应用的关键前提。现有方法普遍存在以下根本性瓶颈：**依赖预定义的重建相机视点**（如LERF、LangSplat、Gaussian Grouping等监督方法），**需要真实语义掩码作为监督信号**，或**需进行昂贵的重训练**（如COB-GS依赖梯度下降优化）。这些假设严重限制了实际交互场景的灵活性——用户期望任意视角、即时响应、无需任何标注数据的开放词汇分割能力。FlashSplat虽然通过线性规划实现了无需训练的3DGS分割，但其采用均匀球面采样或重建相机路径的被动视图策略，未能主动选择最具信息量的观测视角，导致在有限预算下分割精度受限。

### 核心方法定位

B³-Seg（Beta-Bernoulli Bayesian Segmentation for 3DGS）通过**贝叶斯重构**将3DGS分割转化为一个序贯决策问题：将每个高斯的二值标签建模为Beta-Bernoulli贝叶斯后验，并通过**解析期望信息增益（EIG）**实现主动视图选择。该方法在三个关键维度实现了突破：

- **无相机先验**：无需访问重建相机参数或预定义视点轨迹，仅从估计的对象中心出发动态采样候选视图。
- **无需训练**：整个流水线不涉及任何梯度更新或参数优化，完全基于解析计算和预训练视觉基础模型。
- **秒级响应**：端到端分割在约12秒内完成（20个主动选择视图），其中视图选择仅需2.11秒。

核心洞察在于：通过EIG的解析形式贪婪选择信息量最大的视图，不仅避免了在每个候选视图上运行昂贵的SAM2掩码推理，还从理论上保证了该贪婪策略满足**自适应单调性**与**自适应子模性**，从而获得$(1-1/e)$近似最优性保证。

### 方法谱系与知识库定位

在3DGS分割的方法谱系中，B³-Seg处于**相机无关、无需训练的开放词汇分割**分支，直接可比的基线为FlashSplat的两种采样策略（Uniform-Sphere和Recon-Cam）。与依赖重建视图/标签的监督方法（LERF、LangSplat、Gaussian Grouping、ObjectGS）相比，B³-Seg在完全无相机先验的条件下取得了具有竞争力的分割精度。与另一无需训练方法COB-GS相比，B³-Seg避免了梯度下降优化，代之以解析贝叶斯更新，显著降低了计算开销。

从知识库定位来看，B³-Seg的核心贡献在于将**贝叶斯最优实验设计（BOED）**中的信息增益最大化框架引入3DGS分割，并通过Beta分布的共轭性质推导出EIG的解析形式，为主动视图选择提供了理论保证和计算高效的实现路径。

### 主要结果概览

在LERF-Mask和3D-OVS两个基准数据集上，B³-Seg仅使用20个主动选择视图即取得了显著优于相机无关基线的分割精度：

- **LERF-Mask**：mIoU 84.5 / mBIoU 81.0，较FlashSplat Uniform-Sphere提升+14.9 / +15.9个百分点（Table 1）。
- **3D-OVS**：各场景mIoU提升3.9–5.4个百分点（Table 2）。

消融实验进一步验证了各模块的有效性：CLIP重排序和SAM2先验掩码输入分别带来6.6和9.6个百分点的mIoU增益（Table 3）；解析EIG与真实信息增益的相关系数达$r=0.964$（Figure 6），验证了其作为轻量级代理的可靠性；EIG驱动策略在每一步迭代中实现最大的后验熵降，收敛速度显著优于均匀采样和重建相机采样（Figure 7）。

### 局限与开放问题

当前方法主要在对象中心场景下验证，扩展到大型室内/室外环境可能需要更广泛的视点探索策略。二值前后景分割的框架需扩展为Dirichlet-Categorical模型以支持多类别分割。此外，2D掩码推理阶段（约10秒）仍是主要耗时瓶颈，且自适应单调性和子模性的理论保证在多类场景下的推广仍是一个开放问题。



### 3D高斯泼溅分割的现实需求

3D高斯泼溅（3D Gaussian Splatting, 3DGS）已成为高保真三维场景表示的核心技术，其在交互式编辑、增强现实和具身智能等应用中，对**开放词汇、相机无关、实时响应**的3D分割提出了迫切需求。用户期望通过自然语言文本提示，在任意视角下快速、准确地提取目标对象的完整三维掩码，而无需依赖预定义相机轨迹或真实语义标注。

### 现有方法的关键瓶颈

当前3DGS分割方法在满足上述需求时面临三重根本性限制：

**相机依赖**：监督方法如**LERF**、**LangSplat**、**Gaussian Grouping**和**ObjectGS**在训练和推理阶段均依赖重建过程中使用的特定相机视点。一旦场景被重建，用户无法从任意新视角发起分割请求，严重制约了交互式编辑的灵活性。

**训练开销**：上述方法需要完整的重建视图及对应的真实语义标签进行训练，或需要对3DGS进行昂贵的逐场景重训练。这使得它们无法适应“加载即分割”的快速应用场景。

**效率瓶颈**：即使是无需训练的快速方法如**COB-GS**，其分割过程仍依赖重建相机视图，缺乏主动选择信息量最大视角的能力。直接可比的相机无关基线**FlashSplat**采用均匀球面采样（Uniform-Sphere）或重建相机路径（Recon-Cam）进行视图选择，但被动采样策略导致信息获取效率低下——在相同视图预算下，分割精度显著低于信息驱动的方法（mIoU差距达+14.9个百分点，见Table 1）。

### 核心动机：从被动采样到主动信息获取

上述瓶颈的实质在于：现有方法将3DGS分割视为**单步或被动多步的标签推断问题**，而非**序贯决策问题**。当用户仅提供一个文本提示而无任何相机先验时，系统面临的核心挑战是——如何在巨大的视点空间中，以最少的视图交互快速定位并完整分割目标对象？

B³-Seg的核心动机正是将分割重构为**序贯贝叶斯决策过程**：将每个3D高斯的二值标签（前景/背景）建模为Beta-Bernoulli共轭对，利用贝叶斯更新序贯融合多视图证据；同时引入**解析期望信息增益（Expected Information Gain, EIG）**作为视图选择的驱动信号，贪婪地选择每一步中最大程度降低后验不确定性的视角。这一重构不仅使方法天然具备相机无关和无需训练的特性，还从理论上保证了**自适应单调性**与**自适应子模性**，从而获得$(1-1/e)$近似最优性保证（见Lemma 1、Lemma 2及Theorem）。

通过这种“信息驱动”的主动视图选择，B³-Seg在仅使用20个主动选择视图和约12秒总运行时间的条件下，取得了与依赖相机和标签的监督方法相当的精度，为交互式3DGS编辑提供了实用化的技术路径。



## 核心方法与创新机理

B³-Seg的核心创新在于将3DGS分割重构为一个**相机无关、无需训练的序贯贝叶斯决策问题**，并通过两个关键的技术槽位变更（changed slots）实现秒级交互式分割，从根本上绕开了现有方法对预定义相机视点、真实语义掩码和昂贵重训练的依赖。

### 从线性规划到序贯Beta-Bernoulli贝叶斯更新

现有训练无关方法（如FlashSplat）将分割视为一个批量线性规划问题，要求在所有视图上一次性求解高斯标签分配。B³-Seg则将其转化为**序贯Beta-Bernoulli贝叶斯更新**：每个高斯的二值标签（前景/背景）被建模为一个Beta分布，每获取一个新视图的掩码观测，便通过伪计数增量更新其后验分布（Eq. 6）：

$$\mathrm{Beta}(a_i, b_i) \gets \mathrm{Beta}(a_i + e_{i,1}(v), b_i + e_{i,0}(v))$$

其中 $e_{i,1}(v)$ 和 $e_{i,0}(v)$ 分别表示高斯 $i$ 在当前视图 $v$ 下对前景/背景的可见责任计数（Eq. 5）。这一更新机制具有两个关键优势：

1. **不确定性量化**：Beta后验天然编码了每个高斯标签的不确定性，为后续的主动视图选择提供了信息论基础。
2. **理论一致性**：FlashSplat的标签选择规则恰好是该贝叶斯框架下的最大后验（MAP）决策（Eq. 8），表明B³-Seg是FlashSplat的严格推广。

### 解析期望信息增益驱动的主动视图选择

这是B³-Seg最关键的槽位变更。现有方法要么依赖重建相机路径（FlashSplat Recon-Cam），要么采用均匀球面采样（FlashSplat Uniform-Sphere），均无法根据当前分割状态自适应地选择最优视图。

B³-Seg引入**解析期望信息增益（EIG）**作为视图选择的轻量级代理。真实信息增益（IG）需要先获取SAM2掩码再计算熵降（Eq. 9），这在候选视图评估阶段代价过高。EIG的核心洞察在于：利用Beta后验的均值 $m_i$ 和累积责任 $\tau_i$ 构造期望伪计数（Eq. 10），从而无需实际运行掩码推理即可估计每个候选视图的信息增益（Eq. 11）：

$$\mathrm{EIG}(v) = \sum_i \left\{ H(\mathrm{Beta}(a_i,b_i)) - H(\mathrm{Beta}(a_i+\tilde{e}_{i,1}(v), b_i+\tilde{e}_{i,0}(v))) \right\}$$

其中 $\tilde{e}_{i,1} = m_i \tau_i$，$\tilde{e}_{i,0} = (1-m_i) \tau_i$。贪婪选择EIG最大的视图（Eq. 12）仅需一次轻量渲染和熵计算，避免了在候选视图上运行昂贵的Grounding DINO + SAM2推理。

这一设计的有效性得到了双重验证：
- **经验验证**：解析EIG与真实IG的相关系数高达 $r = 0.964$（Figure 6），证明其作为信息增益代理的可靠性。
- **理论保证**：EIG满足自适应单调性和自适应子模性（Lemma 1, Lemma 2），因此贪婪策略达到 $(1-1/e)$ 近似最优（Eq. 17），从理论上保证了视图选择策略的高效性。

### 2D掩码推理的增强

在2D掩码获取阶段，B³-Seg引入了两个增强设计，与贝叶斯框架形成闭环：

- **CLIP重排序**：Grounding DINO可能产生与文本提示不一致的候选框，CLIP重排序通过计算掩码区域与文本提示的CLIP相似度筛选最优掩码，显著提升分割精度（消融实验显示mIoU提升6.6个百分点，Table 3）。
- **SAM2先验掩码输入**：将当前Beta后验均值渲染为置信度图，作为SAM2的先验掩码输入，稳定掩码生成并抑制背景干扰（mIoU提升9.6个百分点，Table 3）。

### 创新闭环

这三个槽位变更构成了一个紧密耦合的创新闭环：**贝叶斯更新**提供不确定性量化 → **EIG驱动选择**利用不确定性贪婪选择最优视图 → **增强掩码推理**获取高质量观测 → 反馈回贝叶斯更新降低不确定性。这一闭环使得B³-Seg在仅使用20个主动选择视图和约12秒总时间的条件下，取得与依赖相机/标签的监督方法相当的分割精度（Table 1, Table 2），真正实现了相机无关、无需训练、秒级响应的3DGS分割。



B³-Seg 将三维高斯泼溅（3DGS）分割重新构建为一个**序贯贝叶斯决策过程**，其核心闭环由三个交替执行的模块构成：主动视图选择、2D掩码推理和Beta-Bernoulli后验更新。整个pipeline无需预定义相机位姿，无需真实语义标签，也无需任何训练或微调，在约12秒内即可完成端到端开放词汇分割（Table 4）。

### Pipeline总览

如Figure 2所示，B³-Seg的完整流程可概括为以下步骤：

1. **候选视图采样**：在当前估计的对象中心 $c_{\text{obj}}$ 处构建球面，均匀采样 $N_{\text{cand}}$ 个候选视图。
2. **EIG计算与视图选择**：对每个候选视图执行一次轻量级3DGS渲染，利用当前Beta后验的均值计算解析期望信息增益（EIG），选择EIG最大的视图 $v^*$（Eq. 11–12）。**关键设计**：EIG仅需渲染和熵计算，完全避免了在候选视图上进行昂贵的SAM2掩码推理（Figure 3b vs. 3a）。
3. **2D掩码推理**：在选定的 $v^*$ 上，利用Grounding DINO生成候选框，SAM2结合先验掩码输入生成分割，CLIP重排序选取与文本提示最匹配的掩码（Section 3.4）。
4. **Beta-Bernoulli更新**：从所选掩码计算每个高斯的前景/背景伪计数 $e_{i,1}(v^*)$ 和 $e_{i,0}(v^*)$（Eq. 5），更新其Beta后验参数（Eq. 6）。
5. **对象中心估计**：从当前前景高斯中重新估计对象中心与半径，动态更新候选采样范围，使后续迭代的候选视图更聚焦于目标对象（Section 3.5, Algorithm 1）。

上述步骤迭代 $T=20$ 次后，通过MAP决策（Eq. 8）输出每个高斯的二值前景/背景标签。

### 模块间的信息流与依赖关系

pipeline中模块之间的数据流形成了**感知-决策-更新**的闭环：

- **Beta后验**是贯穿整个流程的核心状态变量。它既作为EIG计算的先验输入（Eq. 10），又作为2D掩码推理中SAM2先验掩码的来源（通过后验均值渲染），同时还是最终分割标签的决策依据（Eq. 8）。
- **EIG驱动的视图选择**是连接感知与更新的关键决策环节。与均匀球面采样或重建相机采样不同，EIG贪婪地选择期望信息增益最大的视图（Eq. 12），在理论上满足自适应单调性与自适应子模性，从而保证 $(1-1/e)$ 近似最优性（Lemma 1, Lemma 2, Theorem）。
- **对象中心估计**提供自适应反馈：随着Beta后验逐渐确定前景高斯，对象中心与半径的估计越来越精确，使候选视图采样范围动态收缩至目标区域，进一步提升后续视图的信息密度。

### 与基线方法的关键差异

B³-Seg相较于直接可比的相机无关基线**FlashSplat (Uniform-Sphere)** 和**FlashSplat (Recon-Cam)**，在以下两个关键模块上进行了根本性改进：

| 模块 | FlashSplat基线 | B³-Seg |
|------|---------------|--------|
| 视图选择 | 均匀球面采样或重建相机路径 | 基于解析EIG的贪婪选择 |
| 标签更新 | 线性规划求解二值标签 | 序贯Beta-Bernoulli贝叶斯更新 |

这两个改进使得B³-Seg在LERF-Mask数据集上相较FlashSplat (Uniform-Sphere) 的mIoU/mBIoU分别提升14.9/15.9个百分点（Table 1），同时保持了相同的无相机、无需训练特性。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/002_Figure_2.jpg]]
*Figure 2: Overview of*



### 3.1 问题重构：从线性规划到序贯贝叶斯更新

B³-Seg 的核心洞察是将 3DGS 分割从一次性全局优化重构为**序贯 Beta-Bernoulli 贝叶斯更新**。传统方法（如 FlashSplat）将分割建模为线性规划问题：

$$
\operatorname* { m i n } _ { \{ P _ { i } \} } \sum _ { v } \sum _ { ( j , k ) \in I ( v ) } \Big | \sum _ { i } P _ { i } \alpha _ { i } T _ { i } - M _ { j , k } ( v ) \Big |
$$

该形式要求预先拥有所有视图的掩码，无法支持交互式、相机无关的场景。B³-Seg 将每个高斯的二值标签 $y_i \in \{0,1\}$ 视为 Bernoulli 随机变量，通过序贯观测视图掩码来更新其后验分布。

### 3.2 伪计数与 Beta 后验更新

对于视图 $v$ 的渲染图像 $I(v)$，每个高斯 $i$ 对像素 $(j,k)$ 的可见性贡献由渲染权重 $\alpha_i T_i$ 给出。给定该视图的二值掩码 $M(v)$，定义**伪计数**（pseudo-counts）：

$$
e _ { i , 1 } ( v ) = \sum _ { ( j , k ) \in I ( v ) } \alpha _ { i } T _ { i } \mathbb { I } [ M _ { j , k } ( v ) = 1 ]
$$

$$
e _ { i , 0 } ( v ) = \sum _ { ( j , k ) \in I ( v ) } \alpha _ { i } T _ { i } \mathbb { I } [ M _ { j , k } ( v ) = 0 ]
$$

其中 $e_{i,1}(v)$ 和 $e_{i,0}(v)$ 分别表示高斯 $i$ 对前景/背景区域的累积可见责任。这些伪计数作为 Beta 先验的"虚拟观测"，驱动后验更新：

$$
\mathrm {B e t a} ( a _ { i } , b _ { i } ) \gets \mathrm {B e t a} ( a _ { i } + e _ { i , 1 } ( v ) , b _ { i } + e _ { i , 0 } ( v ) )
$$

初始先验设为无信息先验 $\mathrm{Beta}(1,1)$。在观测多个视图后，贝叶斯最优标签由 MAP 决策给出：

$$
y _ { i } = \underset { n \in \{ 0 , 1 \} } { \arg \operatorname* { m a x } } \sum _ { v } e _ { i , n } ( v )
$$

值得注意的是，该 MAP 规则恰好等价于 FlashSplat 的标签选择策略，表明 B³-Seg 的贝叶斯框架是 FlashSplat 的严格泛化——前者支持序贯更新，后者仅适用于批量处理。

### 3.3 解析期望信息增益（EIG）与主动视图选择

序贯更新的关键在于**选择下一个最优视图**。真实信息增益（IG）定义为加入视图 $v$ 后所有高斯后验熵的期望降幅：

$$
\mathrm{IG}(v) = \sum_i \{ H(\mathrm{Beta}(a_i,b_i)) - H(\mathrm{Beta}(a_i+e_{i,1}(v), b_i+e_{i,0}(v))) \}
$$

但计算 IG 需要先获得该视图的掩码 $M(v)$（即 $e_{i,1}, e_{i,0}$），这需要运行昂贵的 SAM2 推理，违背了高效候选评估的初衷。

B³-Seg 的关键创新是引入**解析期望信息增益（EIG）**作为轻量级代理。核心思想是：在尚未获得真实掩码时，用当前 Beta 后验的均值 $m_i = a_i/(a_i+b_i)$ 作为高斯的"当前置信度"，结合渲染权重 $\tau_i = \sum_{(j,k)} \alpha_i T_i$ 构造**期望伪计数**：

$$
\tilde { e } _ { i , 1 } = m _ { i } \tau _ { i } , \quad \tilde { e } _ { i , 0 } = ( 1 - m _ { i } ) \tau _ { i }
$$

将期望伪计数代入熵降公式，得到解析 EIG：

$$
\mathrm{EIG}(v) = \sum_i \{ H(\mathrm{Beta}(a_i,b_i)) - H(\mathrm{Beta}(a_i+\tilde{e}_{i,1}(v), b_i+\tilde{e}_{i,0}(v))) \}
$$

EIG 的计算仅需一次渲染（获得 $\alpha_i T_i$）和 Beta 熵的解析求值，完全避免了 SAM2 推理。贪婪视图选择策略为：

$$
v ^ { \star } = \arg \operatorname* { m a x } _ { v } \mathrm {E I G} ( v )
$$

实验验证表明，EIG 与真实 IG 高度相关（$r=0.964$，Figure 6），且 EIG 驱动的选择在每一步产生最大的后验熵降（Figure 7）。

### 3.4 2D 掩码推理与 CLIP 重排序

选定最优视图 $v^*$ 后，B³-Seg 在该视图上进行 2D 掩码推理。流程为：

1. **Grounding DINO** 生成候选边界框；
2. **SAM2** 以当前 Beta 后验均值渲染的置信图作为先验掩码输入，生成精细分割；
3. **CLIP 重排序**：对每个候选掩码 $M_k(v^*)$，计算掩码区域与文本提示的 CLIP 相似度，选择最优掩码：

$$
M(v^\star) = \arg\max_k \mathrm{CLIP}(I(v^\star) \odot M_k(v^\star), \mathrm{text})
$$

消融实验（Table 3）表明，CLIP 重排序和 SAM2 先验掩码输入分别将平均 mIoU 提升 6.6 和 9.6 个百分点。

### 3.5 候选视图采样与对象中心估计

候选视图在估计的对象中心 $\mathbf{c}_{obj}$ 的球面上均匀采样 $N_{cand}$ 个。初始中心由用户在规范视图上点击或由 2D 掩码反投影估计。每次更新后，从前景高斯重新估计中心及半径，动态调整候选采样范围。实验表明，即使初始中心偏移 50%，mIoU 仅下降 1.6%（Table 6），验证了方法对初始条件的鲁棒性。

### 3.6 理论保证

B³-Seg 从理论上证明了 EIG 满足**自适应单调性**（Lemma 1）和**自适应子模性**（Lemma 2），从而贪婪策略达到 $(1-1/e)$ 近似最优性：

$$
\mathbb {E} \Big [ F \big ( S _ { k } ^ { \mathrm {g r e e d y} } \big ) \Big ] \geq \big ( 1 - 1 / e \big ) \operatorname* { m a x } _ { \pi } \mathbb {E} \big [ F \big ( S _ { k } ^ { \pi } \big ) \big ]
$$

此外，预测熵给出了贝叶斯准确率的下界：

$$
A ( q ) \geq 1 - \frac { H _ { \mathrm { p r e d } } ( q ) } { 2 \log 2 }
$$

这为基于熵的早期停止策略提供了理论依据。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/003_Figure_3.jpg]]
*Figure 3: Information Gain vs. Expected Information Gain (ours). (a) IG calculation updates the Beta posterior using SAM2 segmentation masks (Eq. (9)). (b) Our EIG approximates the posterior update from the prior Beta distribution, avoiding SAM2 inference and enabling efficient viewpoint evaluation (Eq. (11))*



## 实验与关键发现

### 核心定量结果

B³-Seg在两个标准基准上系统评估了分割精度，所有实验均在单块RTX A6000 GPU上完成，使用20视图/20步的统一预算。对比分为两组：**不可直接比较的监督方法**（依赖重建相机位姿或真实语义标签，如LERF、LangSplat、Gaussian Grouping、ObjectGS）和**直接可比的相机无关基线**（FlashSplat的均匀球面采样Uniform-Sphere和重建相机Recon-Cam变体）。为确保公平，后一组基线使用了与B³-Seg完全相同的2D掩码推理管线。

**LERF-Mask数据集**（Table 1）：B³-Seg在场景均值上取得mIoU 84.5、mBIoU 81.0，相较Uniform-Sphere基线的69.6/65.1分别提升**+14.9/+15.9个百分点**。值得注意的是，B³-Seg在无相机先验条件下已达到与依赖重建视图的监督方法（如LangSplat的88.0 mIoU）可比甚至接近的水平。

**3D-OVS数据集**（Table 2）：在四个场景上B³-Seg均显著优于Uniform-Sphere基线——Bed场景97.1 vs 91.7（+5.4），Bench场景92.2 vs 86.9（+5.3），Sofa场景94.1 vs 90.2（+3.9），Lawn场景96.8 vs 91.9（+4.9）。这些结果验证了EIG驱动的主动视图选择在不同场景几何和语义复杂度下的稳健增益。

### 消融实验

**2D掩码精炼模块**（Table 3）：消融实验揭示了CLIP重排序和SAM2先验掩码输入各自的贡献。移除CLIP重排序后，平均mIoU下降6.6个百分点；移除SAM2先验掩码输入后，下降9.6个百分点。两者联合作用时达到84.5 mIoU，表明CLIP有效过滤了Grounding DINO的误检候选框（如Figure 9所示，CLIP正确识别了“cookies on a plate”而Grounding DINO给出了错误的高分框），而SAM2先验掩码输入则利用当前Beta后验均值渲染的置信度图稳定了分割边界。

**EIG代理质量验证**（Figure 6）：在LERF-Mask数据集上，解析EIG与真实信息增益（IG，需实际运行SAM2推理后计算）之间的Pearson相关系数达到r=0.964，强相关验证了EIG作为轻量级代理的有效性。这解释了为何EIG无需在候选视图上执行昂贵的掩码推理即可准确识别高信息量视图。

**收敛行为**（Figure 7）：在LERF-Mask Teatime场景上对比了三种视图选择策略的后验熵下降曲线。EIG驱动策略在每一步迭代中产生最大的熵降，收敛速度显著快于均匀球面采样和重建相机采样。这与理论保证一致——EIG满足自适应单调性和自适应子模性，贪婪策略达到(1-1/e)近似最优。

**超参数敏感性**（Table 5）：候选视图数N_cand和迭代次数T均在20附近达到精度饱和。继续增加N_cand或T仅带来微小提升，而运行时间几乎线性增长，表明20是精度-效率的最佳平衡点。

**初始条件鲁棒性**（Table 6）：将初始对象中心沿随机3D方向偏移对象半径的50%时，mIoU仅下降1.6%，证明方法对初始条件具有较强鲁棒性。这得益于动态对象中心估计模块在迭代过程中逐步修正初始偏差。

### 运行时分析

Table 4给出了完整的运行时分解：端到端20次主动选择视图的总时间为12.1秒。其中2D掩码推理（Grounding DINO + SAM2 + CLIP重排序）占主导，约9.76秒；EIG计算与视图选择仅需2.11秒，因为每个候选视图只需一次轻量级渲染和熵评估，无需运行SAM2。这一分解表明，当前瓶颈在2D基础模型的推理速度，而非B³-Seg的贝叶斯更新或EIG计算。

### 失败模式与局限性

尽管B³-Seg在对象中心场景下表现优异，但存在以下已知局限：

1. **场景规模扩展**：当前候选视图采样基于估计的对象中心球面，主要适用于以对象为中心的场景。扩展到大型室内/室外环境可能需要更广泛的视点探索策略（如RRT相机采样或跨尺度候选生成），这一方向尚未验证。

2. **多类别分割**：Beta-Bernoulli模型天然支持二值前后景分割，扩展到多类别需替换为Dirichlet-Categorical模型。尽管贝叶斯框架可以推广，但自适应单调性和子模性的理论证明能否直接迁移到多类设置仍是开放问题。

3. **遮挡与复杂几何**：在严重遮挡或细粒度几何结构场景中，2D掩码推理阶段的不确定性增加，可能影响伪计数估计的准确性，进而降低分割质量。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/006_Table_1.jpg]]
*Table 1: LERF-Mask (accuracy, assumptions, and latency). Top: Methods that require reconstruction views/labels (=not directly comparable). Bottom: Sampling-based, training-free approach with our 20 views/updates runtime (few seconds). † Uniform-Sphere: Candidate viewpoints sampled uniformly on a sphere. ‡ Recon-Cam: Candidate viewpoints randomly sampled from reconstruction cameras*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/007_Table_2.jpg]]
*Table 2: 3D-OVS (mIoU). Top: assumes views/labels (not comparable). Bottom: camera-free & training-free*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/008_Table_3.jpg]]
*Table 3: Ablation study on LERF-Mask. Both CLIP re-ranking and SAM2 mask-input improve segmentation performance*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/012_Figure_6.jpg]]
*Figure 6: Predicted EIG closely matches information gain on the LERF-Mask, with a strong correlation (r = 0.964)*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/013_Figure_7.jpg]]
*Figure 7: Posterior entropy vs. iteration for three view-selection strategies on the LERF-Mask Teatime scene. EIG-based selection consistently achieves the largest per-step entropy drop*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison on text-guided 3D segmentation. We compare our method (B3-Seg) with prior 3DGS segmentation approaches. Our method produces cleaner and more complete object masks, especially in cluttered scenes*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/005_Figure_5.jpg]]
*Figure 5: Candidate-view EIG on LERF-Mask (Teatime) with the prompt “stuffed bear”. Each panel shows a candidate rendering; the bottom-right inset is the current confidence map (posterior mean)*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/009_Table_5.jpg]]
*Table 5: Sensitivity to*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/011_Table_6.jpg]]
*Table 6: Sensitivity to the initial condition on LERF-Mask. We shift the initial object center*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2602_17134/figures/015_Figure_9.jpg]]
*Figure 9: Effect of CLIP re-ranking in the LERF-Mask Teatime scene. Although GroundingDINO assigns a higher score to the wrong bounding box (green), CLIP correctly assigns a higher similarity score to the region corresponding to the true object described by the prompt “cookies on a plate” (orange)*



## 定位与知识库关联

### 与基线方法的关系

B³-Seg的核心定位是**无相机、无需训练、开放词汇的3DGS分割**，其直接可比的基线是**FlashSplat**（相机无关、训练无关的采样方法）。FlashSplat提供两种视图选择策略：均匀球面采样（Uniform-Sphere）和基于重建相机的采样（Recon-Cam），两者均采用线性规划求解高斯标签。B³-Seg在FlashSplat的基础上进行了两个关键改造：（1）将标签更新从线性规划替换为序贯Beta-Bernoulli贝叶斯更新；（2）将视图选择从被动采样替换为基于解析期望信息增益（EIG）的主动选择。实验表明，在相同的20视图/20步预算下，B³-Seg在LERF-Mask数据集上相较FlashSplat Uniform-Sphere基线提升14.9个mIoU点（84.5 vs. 69.6），在3D-OVS各场景上提升3.9–5.4个mIoU点（Table 1, Table 2）。

在监督方法体系中，**LERF**、**LangSplat**、**Gaussian Grouping**、**ObjectGS**等需要重建视图或真实语义标签，与B³-Seg不构成公平对比（Table 1, Table 2上半部分）。但值得注意的是，B³-Seg在仅使用20个主动选择视图和约12秒总时间的条件下，取得了与这些高成本监督方法相当的分割精度，证明了无相机、无需训练范式在交互式场景中的实用价值。

**COB-GS**是另一条快速分割的技术路线，但其依赖重建相机视图，无法适配相机无关的交互需求。B³-Seg通过EIG驱动的主动视图选择，在完全无相机先验的条件下实现了秒级响应。

### 技术贡献的知识库锚点

B³-Seg的方法论贡献可锚定在以下知识节点上：

1. **贝叶斯序贯决策框架**：将3DGS分割从批量优化问题重构为序贯贝叶斯更新问题。每个高斯的标签建模为Beta-Bernoulli分布，通过累积伪计数（Eq. 5）进行后验更新（Eq. 6）。FlashSplat的标签选择规则被证明是该框架下的MAP决策特例（Eq. 8），从而将现有方法统一到贝叶斯视角下。

2. **解析期望信息增益（EIG）**：主动视图选择的核心创新。真实信息增益（IG, Eq. 9）需要先获取SAM2分割掩码才能计算，失去了主动选择的意义。B³-Seg利用Beta后验均值估计期望伪计数（Eq. 10），推导出解析形式的EIG（Eq. 11），仅需一次轻量渲染即可评估候选视图的信息量，避免了昂贵的掩码推理。实验验证EIG与真实IG的相关系数达r=0.964（Figure 6），证明其作为代理指标的有效性。

3. **自适应单调性与子模性理论保证**：论文证明了EIG满足自适应单调性（Lemma 1）和自适应子模性（Lemma 2），从而贪婪视图选择策略达到$(1-1/e)$近似最优（Eq. 17）。这为主动视图选择的性能提供了理论保障，而非仅仅依赖经验验证。

4. **2D掩码精炼管道**：在所选视图上，采用Grounding DINO生成候选框、SAM2加入先验掩码（基于当前Beta均值渲染）进行分割、CLIP重排序选取最优掩码的三阶段管道。消融实验表明CLIP重排序和SAM2先验掩码输入分别贡献6.6和9.6个mIoU点的提升（Table 3）。

### 适用边界与局限

1. **场景规模约束**：当前方法主要在对象中心场景下验证（LERF-Mask和3D-OVS数据集），其候选视图生成策略基于估计的对象中心球面采样（Section 3.5）。扩展到大型室内/室外环境时，单一球面采样可能无法覆盖所有信息丰富的视角，需要更广泛的视点探索策略，如基于RRT的相机采样或跨尺度候选生成。

2. **二值分割限制**：Beta-Bernoulli模型天然支持二值前后景分割。多类别分割需要扩展为Dirichlet-Categorical模型，此时伪计数的可解释性和EIG的解析形式需要重新推导。如何保持自适应单调性和子模性保证在多类设置下成立，是一个开放的理论问题。

3. **2D掩码推理瓶颈**：总运行时间12.1秒中，掩码推理（Grounding DINO + SAM2 + CLIP）占9.76秒，视图选择仅需2.11秒（Table 4）。当对象复杂或遮挡严重时，2D掩码的不确定性可能累积，影响贝叶斯更新的质量。

4. **初始条件依赖**：方法对初始对象中心估计有一定鲁棒性——当初始中心偏移50%时，mIoU仅下降1.6%（Table 6）。但在极端偏移或错误初始化的场景下，候选视图采样范围可能偏离目标对象，影响后续主动选择的效率。

### 开放问题

1. **多类扩展的理论完备性**：如何将自适应单调性和子模性证明从二值Beta-Bernoulli推广到多类Dirichlet-Categorical设置？EIG的解析形式在Dirichlet分布下是否依然存在闭式解？

2. **早期停止策略**：当前方法固定使用20次迭代。基于后验熵的早期停止策略（Eq. 18给出了贝叶斯准确率下界与预测熵的关系）在实际交互中的表现和用户体验如何？能否在精度和效率之间实现自适应平衡？

3. **大规模场景的候选生成**：在大型场景中，EIG的解析形式与更复杂的候选生成策略（如基于RRT的探索、多尺度球面采样）结合是否依然有效？候选视图的分布如何影响EIG估计的准确性？

4. **与4D/动态场景的结合**：B³-Seg的序贯贝叶斯框架天然适合在线更新，能否扩展到动态3DGS场景中的时序分割任务？



## 原文 PDF

![[paperPDFs/CVPR_2026/B_Seg_Camera_Free_Training_Free_3DGS_Segmentation_via_Analytic_EIG_and_Beta_Bernoulli_Bayesian_Updates.pdf]]
