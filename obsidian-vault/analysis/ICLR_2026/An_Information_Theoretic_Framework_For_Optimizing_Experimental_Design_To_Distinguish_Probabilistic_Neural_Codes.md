---
title: "An Information-Theoretic Framework For Optimizing Experimental Design To Distinguish Probabilistic Neural Codes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/An_Information_Theoretic_Framework_For_Optimizing_Experimental_Design_To_Distinguish_Probabilistic_Neural_Codes.pdf
openreview_forum_id: doxBjZ88H3
aliases:
- IGMF
- ITFOEDDPNC
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "刺激先验分布（context-specific prior distributions）操纵——改变刺激统计信息在不同上下文间的变化，可调节神经反应的先验依赖性，从而暴露编码格式。"
primary_logic: "通过信息论指标——信息差距（information gap），量化了使用似然解码器与后验解码器时的预期交叉熵性能差异。最大化信息差距的刺激先验设计能够最优地区分这两种概率编码假说。信息差距通过真实后验与任务边缘化代理后验之间的KL散度解析推导，并在模拟中被验证准确预测解码器性能差异。"
claims:
- "信息差距的解析表达式（Eq. 1和Eq. 3）准确预测了在多种对照水平和任务参数下模拟神经群体的解码器性能差异。"
- "在Allen Visual Coding数据集上，单上下文实验的解码器性能差异（似然解码器减后验解码器）为0.0024±0.064，p=0.63，不显著，证明传统设计无法区分两种假说。"
- "最大化信息差距的任务参数优化揭示了高斯先验下的“甜点”参数，如在低对比度下，先验分离d≈30°，标准差σ≈20°，使后验编码的信息差距接近最大值。"
- "Simulated Poisson neural populations (high, medium, low contrast) 上 Decoder performance difference (likelihood - posterior) con... = Converges to theoretical information gap predicted by Eq. 1..."
---

# An Information-Theoretic Framework For Optimizing Experimental Design To Distinguish Probabilistic Neural Codes

> [!tip] 核心洞察
> 通过信息论指标——信息差距（information gap），量化了使用似然解码器与后验解码器时的预期交叉熵性能差异。最大化信息差距的刺激先验设计能够最优地区分这两种概率编码假说。信息差距通过真实后验与任务边缘化代理后验之间的KL散度解析推导，并在模拟中被验证准确预测解码器性能差异。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 区分概率神经编码的实验设计优化信息论框架 |
| 英文题名 | An Information-Theoretic Framework For Optimizing Experimental Design To Distinguish Probabilistic Neural Codes |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=doxBjZ88H3) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | Information-Gap Maximization Framework (信息差距最大化实验设计框架) |
| Dataset | Simulated Poisson neural populations (high, medium, low contrast), Simulated populations across diverse task parameters (Poisson and gain-modulated Poisson models), Allen Visual Coding dataset (169 sessions with >300 trials) |

> [!tip] 效果简介
> - Simulated Poisson neural populations (high, medium, low contrast) 上，Decoder performance difference (likelihood - posterior) convergence 为 Converges to theoretical information gap predicted by Eq. 1 / Eq. 3，对比 N/A (no specific numerical baseline)，变化 Not a single delta; convergence shown。
> - Simulated populations across diverse task parameters (Poisson and gain-modulate... 上，Decoder performance difference vs. theoretical information gap 为 Strong correlation (close to y=x line) between theoretical Δ^{info} and empirical decoder difference.，对比 N/A (but predictions match)，变化 Not applicable; no direct comparison。
> - Allen Visual Coding dataset (169 sessions with >300 trials) 上，Cross-entropy performance difference (likelihood decoder - posterior decoder) 为 0.0024 ± 0.064 (mean ± std)，对比 Model prediction of 0 under single-context uniform prior，变化 Not significantly different from 0 (p=0.63)。

## 概述

### 问题背景

在感觉神经科学中存在一个长期未决的核心争论：早期感觉神经群体究竟编码了似然函数（likelihood coding hypothesis），还是已经整合了先验信息、直接编码后验分布（posterior coding hypothesis）？前者以概率群体编码（probabilistic population code, Ma et al., 2006）为代表，认为初级感觉皮层仅编码刺激的似然信息，后验计算由下游脑区完成；后者以神经采样编码（neural sampling code, Hoyer & Hyvärinen, 2002）为代表，主张早期感觉群体通过来自高级皮层的反馈连接已整合先验知识，直接表征后验分布。

传统实验设计的瓶颈在于：单上下文实验（即刺激先验固定且均匀）无法揭示神经群体究竟编码了哪种概率量。在单一先验下，似然与后验仅相差一个常数因子，解码器性能差异理论上为零，无法区分两种假说。该文在Allen Visual Coding数据集上的分析直接验证了这一缺陷——似然解码器与后验解码器的交叉熵性能差异仅为0.0024±0.064，与零无显著差异（p=0.63），证明传统范式确实无法区分两种编码假说。

### 核心方法：信息差距最大化框架

该文提出了一套信息论实验设计框架——**信息差距最大化框架（Information-Gap Maximization Framework）**，通过操纵刺激先验分布来暴露神经编码格式。核心思路是：设计两个上下文（context A 和 context B），每个上下文具有不同的刺激先验分布 $p^A(\theta)$ 和 $p^B(\theta)$，然后分别训练似然解码器和后验解码器，比较其交叉熵性能差异。

框架的关键创新在于引入**信息差距（information gap）**这一解析指标，量化了使用似然解码器与后验解码器时的期望性能差异：

- 对于似然编码群体，信息差距 $\Delta_{\mathrm{L}}^{\mathrm{info}}$ 定义为真实后验与最优后验解码器输出的KL散度期望（Eq. 1），该最优后验解码器实际上使用了上下文边缘化的代理先验（Eq. 2）。
- 对于后验编码群体，信息差距 $\Delta_{\mathrm{P}}^{\mathrm{info}}$ 定义为真实后验与最优似然解码器输出的KL散度期望（Eq. 3），该最优似然解码器通过定点迭代求解隐式方程（Eq. 5）。

信息差距的解析计算仅依赖任务设计参数和已知的生成模型，无需实际训练解码器即可预测可区分性。这一解析表达式的推导是该框架的理论基石。

### 主要结果

1. **模拟验证**：在模拟的Poisson神经群体和增益调制的生物真实Poisson模型（Goris et al., 2014）上，解码器性能差异随试次和神经元数量增加收敛至信息差距理论值（Figure 3），且理论值与经验值高度一致（Figure 4），验证了信息差距作为可区分性预测指标的准确性。

2. **任务参数优化**：通过搜索信息差距在任务参数空间中的景观（Figure 5），发现了高斯先验下的“甜点”参数——例如在低对比度下，先验分离度 $d \approx 30^\circ$、标准差 $\sigma \approx 20^\circ$ 可使后验编码的信息差距接近最大值，同时保持似然编码的足够区分信号。

3. **先验分布形式的影响**：重尾分布（如学生t分布、柯西分布）或薄尾分布（如广义正态分布）作为上下文先验时，后验编码的信息差距大幅减小甚至趋于零（Figure 6, 14, 15, 17, 18），不适合用于区分编码假说。这是因为非高斯先验与高斯似然结合后产生不对称后验，减少了可混淆后验配对的数量（Figure 16），从而削弱了后验编码群体的可区分性。

4. **实际数据验证**：在Allen Visual Coding数据集（169个session，>300试次）上的解码分析证实，单上下文设计的信息差距接近零，无法区分两种假说，凸显了上下文依赖先验操纵的必要性。

### 方法定位

该方法属于**实验设计优化**范式，核心调控变量是刺激先验分布，通过信息差距的解析计算指导最优实验参数选择。与传统单上下文解码分析相比，该框架将区分两种概率编码假说的问题转化为一个可优化的信息论目标，为神经科学实验设计提供了原则性指导。框架的局限性在于依赖最优解码器假设和已知生成模型，且主要针对两上下文高斯先验设计进行了验证；扩展到更复杂的先验族、混合编码假说或其他感觉模态仍需进一步研究。

## 背景与动机

感觉系统需要处理来自外部世界的不确定信息。当观察者接收到的感觉信号存在噪声时，大脑如何编码这种不确定性，是计算神经科学中的一个核心问题。目前存在两种主要的竞争性假说：**似然编码假说**与**后验编码假说**。

**似然编码假说**认为，早期感觉神经群体编码的是刺激的似然函数 $L(\theta) \equiv p(x|\theta)$，即给定隐变量世界状态 $\theta$ 时观察到神经反应 $x$ 的概率。后验分布的计算被推迟到下游脑区，通过整合似然函数与先验知识来完成。该假说的典型代表是概率群体编码（Ma et al., 2006）。

**后验编码假说**则认为，早期感觉神经群体直接编码后验分布——即已经融合了来自高级皮层反馈的先验知识。这意味着神经反应本身已经反映了对隐变量世界状态的完整推断。该假说的典型代表是神经采样编码（Hoyer & Hyvärinen, 2002）。

区分这两种假说对于理解大脑计算架构至关重要，因为它直接关系到先验知识是在感觉处理的早期阶段还是晚期阶段被整合。然而，传统实验设计面临一个根本性瓶颈：**在单一上下文、均匀先验的实验范式下，似然函数与后验分布在数学上仅相差一个常数因子，因此无法通过解码神经反应来区分两种编码格式**。这一困境使得该领域的核心争论长期悬而未决。

本文提出的核心洞见是：通过**操纵刺激先验分布在上下文间的变化**，可以暴露神经群体编码的统计结构。具体而言，当实验包含两个具有不同刺激先验分布的上下文时，似然编码群体与后验编码群体对相同刺激的反应将产生系统性差异。利用信息论工具——**信息差距**——可以量化这种差异，并指导实验设计以最大化两种假说之间的可区分性。

## 核心创新

### 问题瓶颈：单上下文实验无法区分概率编码假说

在感觉神经群体中存在两个根本性竞争假说：**似然编码**（如概率群体编码，Ma et al., 2006）主张早期感觉群体编码刺激的似然函数，后验计算推迟到下游区域；**后验编码**（如神经采样编码，Hoyer & Hyvärinen, 2002）则认为早期感觉群体已通过反馈连接整合先验知识，直接编码后验分布。传统实验设计采用单上下文、均匀先验范式，无法揭示神经群体到底编码了似然函数还是后验分布——两者在单上下文下产生不可区分的解码性能。Allen Visual Coding数据集上169个记录会话的实证分析证实了这一瓶颈：似然解码器与后验解码器的交叉熵性能差异仅为 $0.0024 \pm 0.064$，与零无显著差异（$p = 0.63$），表明传统设计完全失效。

### 核心创新：信息差距最大化的实验设计框架

本工作提出**信息差距最大化框架**（Information-Gap Maximization Framework），通过信息论原理将“区分编码假说”转化为可优化的实验设计问题。其核心创新体现在三个层面：

**1. 信息差距作为可优化的区分性指标**

框架定义了**信息差距**（information gap）——使用似然解码器与后验解码器时预期交叉熵性能的差异。该指标通过真实后验与任务边缘化代理后验之间的KL散度进行解析推导：
- 似然编码群体的信息差距：$\Delta_{\mathrm{L}}^{\mathrm{info}} := \mathbb{E}_{p(x_i,c)} [ D_{\mathrm{KL}}( p^c(\theta|x_i) \| q_{P,i}^*(\theta) ) ]$
- 后验编码群体的信息差距：$\Delta_{\mathrm{P}}^{\mathrm{info}} := \mathbb{E}_{p(x_i,c)} [ D_{\mathrm{KL}}( p^c(\theta|x_i) \| q_{L,i}^{c*}(\theta) ) ]$

信息差距越大，两种解码器的性能差异越显著，区分编码假说的统计效力越强。这一解析公式使得实验设计可在真实实验前进行理论预测和优化，无需依赖昂贵的数据采集。

**2. 刺激先验操纵作为可调节的因果旋钮**

框架的关键操作变量是**刺激先验分布**（stimulus prior distribution）的上下文依赖性操纵。传统单上下文设计使用均匀先验，无法暴露神经群体对先验的依赖性。本框架引入两上下文设计，每个上下文具有不同的刺激先验分布（如两个分离的高斯分布），通过改变先验的分离度 $d$ 和标准差 $\sigma$，可系统调节神经反应的先验依赖性，从而暴露编码格式。

**3. 任务参数景观优化发现“甜点”设计**

框架在任务参数空间（$d$ 和 $\sigma$）中计算信息差距景观（information gap landscape），识别最大化区分效力的参数组合。关键发现包括：
- 似然编码的信息差距通常比后验编码大一个数量级，因此设计优化需优先确保后验编码的信息差距足够大
- 在低对比度刺激下，先验分离 $d \approx 30°$、标准差 $\sigma \approx 20°$ 的高斯先验使后验编码的信息差距接近最大值，同时保持似然编码的区分信号
- 重尾分布（如学生t分布、柯西分布）或薄尾分布作为先验时，后验编码的信息差距大幅减小甚至归零，不适合用于区分编码假说——这是因为重尾先验与高斯似然结合产生不对称后验，减少了满足后验相等条件（Eq. 4）的观测对，从而破坏了后验编码群体上似然解码器的不完美性

### 与传统方法的对比

| 维度 | 传统单上下文设计 | 信息差距最大化框架 |
|------|-----------------|-------------------|
| 刺激先验 | 单上下文、均匀先验，无先验操纵 | 两上下文、优化后的高斯先验（分离度 $d$ 和标准差 $\sigma$ 经信息差距最大化确定） |
| 区分性指标 | 无理论指导，依赖事后解码器比较 | 信息差距 $\Delta^{\mathrm{info}}$ 提供解析预测，指导事前实验设计 |
| 实证效果 | Allen数据集上解码器性能差异不显著（$p=0.63$） | 模拟中信息差距准确预测解码器性能差异，收敛至理论值 |

### 理论洞察：为什么先验操纵是关键

信息差距的存在依赖于一个根本条件：在后验编码群体上，仅当两个不同上下文下的观测产生相同的后验分布时（即 $p^A(\theta|x_j) = p^B(\theta|x_k)$），似然解码器才会产生混淆，从而贡献信息差距。这一条件等价于 $p^A(\theta) \cdot p(x_j|\theta) \propto p^B(\theta) \cdot p(x_k|\theta)$。通过操纵上下文先验 $p^A(\theta)$ 和 $p^B(\theta)$ 的差异，可以控制满足该条件的观测对数量，进而调节信息差距的大小。这正是框架将“先验操纵”作为核心因果旋钮的理论基础。

## 整体框架

### 核心问题与因果杠杆

该框架的核心目标是解决一个长期困扰感觉神经科学的方法论瓶颈：在单上下文实验中，似然编码假说（神经群体编码似然函数$L(\theta) \equiv p(x|\theta)$）与后验编码假说（神经群体直接编码后验分布$p(\theta|x)$）在解码层面无法区分。传统实验设计使用均匀先验，导致两种假说下的神经反应在统计上不可区分——这一结论在Allen Visual Coding数据集上得到了直接验证：在169个包含超过300试次的记录中，似然解码器与后验解码器的交叉熵性能差异仅为$0.0024 \pm 0.064$，与零无显著差异（$p=0.63$）。

框架的因果杠杆在于**操纵刺激先验分布**：通过在不同上下文（context $c \in \{A, B\}$）中引入不同的刺激统计先验$p^c(\theta)$，可以调节神经反应对先验的依赖性。如果神经群体编码的是似然函数，则其反应仅取决于刺激本身，不受先验变化的影响；如果编码的是后验分布，则反应会随先验变化而系统性偏移。这种先验依赖性差异构成了区分两种编码假说的因果基础。

### 信息差距：核心量化指标

框架的核心指标是**信息差距**（information gap）$\Delta^{\text{info}}$，定义为使用“错误”解码器（与群体实际编码内容不匹配的解码器）相对于“正确”解码器所产生的期望交叉熵损失增量。具体而言：

- **似然编码群体的信息差距** $\Delta_{\mathrm{L}}^{\mathrm{info}}$：使用最优后验解码器$q_{P,i}^*(\theta)$替代最优似然解码器时，期望交叉熵损失的增量：

$$\Delta_{\mathrm{L}}^{\mathrm{info}} := \mathbb{E}_{p(x_i,c)} \big[ D_{\mathrm{KL}}( p^c(\theta|x_i) \| q_{P,i}^*(\theta) ) \big]$$

其中代理后验$q_{P,i}^*(\theta)$是后验解码器在似然编码群体上能达到的贝叶斯最优输出，等效于使用任务边缘化先验$p(c=A)p^A(\theta) + p(c=B)p^B(\theta)$计算的后验分布（Eq. 2）。

- **后验编码群体的信息差距** $\Delta_{\mathrm{P}}^{\mathrm{info}}$：使用最优似然解码器替代最优后验解码器时的期望损失增量：

$$\Delta_{\mathrm{P}}^{\mathrm{info}} := \mathbb{E}_{p(x_i,c)} \left[ D_{\mathrm{KL}}( p^c(\theta|x_i) \| q_{L,i}^{c*}(\theta) ) \right]$$

后验编码群体的最优似然解码器输出$q_{L,i}^{c*}(\theta)$通过隐式方程（Eq. 5）的定点迭代求解，其核心机制是：仅当存在一对观测$(x_j, x_k)$使得两个上下文下的后验分布相等（$p^A(\theta|x_j) = p^B(\theta|x_k)$）时，似然解码器才会产生混淆，从而对$\Delta_{\mathrm{P}}^{\mathrm{info}}$产生贡献。这一条件等价于先验与似然的乘积成比例（Eq. 4）。

### 框架流水线

框架由四个顺序模块构成，形成从理论推导到实验验证的完整闭环：

**模块一：信息差距解析计算。** 给定任务设计参数（上下文先验分布族及其参数）和假设的神经编码模型（似然编码或后验编码），通过解析公式（Eq. 1和Eq. 3）直接计算期望的信息差距。对于后验编码群体，需要额外求解Eq. 5的定点迭代以获得最优似然解码器输出。该模块输出理论预测的解码器性能差异，无需实际训练解码器。

**模块二：模拟验证与解码器训练。** 构建模拟神经群体：使用泊松神经元模型（高斯调谐曲线）或更复杂的增益调制泊松模型，分别按照似然编码和后验编码假说生成群体反应。训练基于深度神经网络的似然解码器和后验解码器，验证模块一的理论预测是否与实际解码器性能差异一致。模拟实验表明，随着试次数和神经元数量增加，经验性能差异收敛至理论信息差距值（Figure 3），且在广泛的任务参数范围内，理论值与经验值高度吻合（Figure 4）。

**模块三：任务参数景观优化。** 在任务参数空间（如高斯先验的均值分离度$d$和标准差$\sigma$）中，扫描计算信息差距景观。优化的目标是找到“甜点”参数——使后验编码的信息差距接近其最大值，同时似然编码的信息差距保持足够大的正值，从而最大化两种假说的可区分性。例如，在低对比度条件下，$d \approx 30^\circ$、$\sigma \approx 20^\circ$的高斯先验设计接近最优（Figure 5）。该模块还揭示了先验分布形态的关键影响：重尾分布（如学生t分布、柯西分布）或薄尾分布会大幅降低甚至消除后验编码的信息差距，因为非对称的后验分布减少了满足Eq. 4的可混淆观测对（Figure 6, 16）。

**模块四：实际神经数据验证。** 将框架应用于真实神经数据，验证传统单上下文设计的无效性，并确认多上下文设计的必要性。在Allen Visual Coding数据集上的分析（Figure 7）直接证明了单上下文均匀先验下信息差距为零的预测，为框架的核心主张提供了实证基础。

### 输入输出流

框架的输入端包括：（1）任务设计规范——上下文数量、各上下文的刺激先验分布族及其参数；（2）假设的神经编码模型——似然编码或后验编码；（3）神经群体的生成模型——包括调谐曲线形态、噪声结构等。输出端包括：（1）理论信息差距值，量化给定设计下两种假说的可区分性；（2）最优任务参数推荐，指导实际实验设计；（3）解码器性能差异的经验验证结果。框架还支持将行为数据（通过心理测量曲线估计的被试先验偏差）纳入信息差距计算（Figure 10），以更真实地反映实验条件下的期望差异。

## 核心模块与公式推导

### 问题设定与核心量

框架建立在两上下文（context）实验范式之上：刺激 $\theta$ 从上下文特定的先验分布 $p^c(\theta)$（$c \in \{A, B\}$）中抽取，神经群体产生响应 $\mathbf{x}$。似然编码假说下，群体编码似然函数 $p(\mathbf{x}|\theta)$，后验由下游脑区结合先验计算；后验编码假说下，群体直接编码后验分布 $p^c(\theta|\mathbf{x})$。

核心量**信息差距**（information gap）定义为：对给定编码假说下的神经群体，分别使用似然解码器 $g_L$ 与后验解码器 $g_P$ 时，交叉熵损失的期望差异。该量量化了“用错误解码器提取概率内容”的代价，从而暴露编码格式。

### 似然编码的信息差距

对于似然编码群体，最优后验解码器的输出并非真实后验，而是一个代理后验（surrogate posterior），因为解码器无法获知当前试次的上下文标签，只能对上下文进行边缘化。由此推导：

$$
\Delta_{\mathrm{L}}^{\mathrm{info}} := \mathbb{E}_{p(\mathbf{x}_i,c)} \big[ D_{\mathrm{KL}}( p^c(\theta|\mathbf{x}_i) \| q_{P,i}^*(\theta) ) \big] \tag{Eq. 1}
$$

其中：
- $p^c(\theta|\mathbf{x}_i)$：给定上下文 $c$ 和观测 $\mathbf{x}_i$ 的真实后验；
- $q_{P,i}^*(\theta)$：最优后验解码器输出，即代理后验，由贝叶斯最优估计给出：

$$
q_{P,i}^*(\theta) = \frac{ [ p(c=A)p^A(\theta) + p(c=B)p^B(\theta) ] \cdot p(\mathbf{x}_i|\theta) }{ \sum_{\theta'} \{ [ p(c=A)p^A(\theta') + p(c=B)p^B(\theta') ] \cdot p(\mathbf{x}_i|\theta') \} } \tag{Eq. 2}
$$

Eq. 2 的本质是：解码器使用任务边缘化先验 $p(c=A)p^A(\theta) + p(c=B)p^B(\theta)$ 代替真实上下文先验，形成代理后验。真实后验与代理后验之间的 KL 散度期望即为似然编码下的信息差距——它衡量了上下文信息缺失导致的解码性能损失。

### 后验编码的信息差距

对于后验编码群体，真实后验 $p^c(\theta|\mathbf{x}_i)$ 直接编码在群体活动中。最优似然解码器试图从中提取似然函数，其输出 $q_{L,i}^{c*}(\theta)$ 同样偏离真实后验。信息差距定义为：

$$
\Delta_{\mathrm{P}}^{\mathrm{info}} := \mathbb{E}_{p(\mathbf{x}_i,c)} \left[ D_{\mathrm{KL}}( p^c(\theta|\mathbf{x}_i) \| q_{L,i}^{c*}(\theta) ) \right] \tag{Eq. 3}
$$

后验编码信息差距的计算更为复杂。关键洞察在于：仅当存在一对观测 $(\mathbf{x}_j, \mathbf{x}_k)$ 满足后验相等条件时，似然解码器才会产生混淆，从而对信息差距产生非零贡献。该条件为：

$$
\forall_{\theta}, p^A(\theta|\mathbf{x}_j) = p^B(\theta|\mathbf{x}_k) \Leftrightarrow \forall_{\theta}, p^A(\theta) \cdot p(\mathbf{x}_j|\theta) \propto p^B(\theta) \cdot p(\mathbf{x}_k|\theta) \tag{Eq. 4}
$$

满足 Eq. 4 的观测对 $(\mathbf{x}_j, \mathbf{x}_k)$ 上，最优似然解码器输出 $\ell_{jk}^*(\theta)$ 由以下隐式方程给出，需通过定点迭代求解：

$$
\ell_{jk}^*(\theta) \propto \frac{ \rho_j^A p^A(\theta|\mathbf{x}_j) + \rho_k^B p^B(\theta|\mathbf{x}_k) }{ \frac{\rho_j^A}{Z_j^A[\ell_{jk}^*]} p^A(\theta) + \frac{\rho_k^B}{Z_k^B[\ell_{jk}^*]} p^B(\theta) } \tag{Eq. 5}
$$

其中 $\rho_j^A, \rho_k^B$ 为两观测在各自上下文中的出现概率，$Z$ 为归一化因子。Eq. 5 的分子是两后验的加权混合，分母是两先验的加权混合——似然解码器本质上在“剥离”先验信息，但当两后验相同时，这种剥离导致信息损失，体现为信息差距。

### 计算流程模块化

框架的计算管线可分解为三个关键模块：

1. **信息差距解析计算模块**：给定任务设计（上下文先验族、参数、似然函数形式），利用 Eq. 1–5 直接计算期望解码器性能差异，无需实际训练解码器。该模块是后续优化的基础。

2. **解码器验证模块**：构建似然编码和后验编码的模拟神经群体（Poisson 或增益调制 Poisson 模型），训练基于深度神经网络的似然/后验解码器，验证解析信息差距对经验解码器性能差异的预测准确性（Figure 3, Figure 4）。

3. **任务参数景观优化模块**：在任务参数空间（如高斯先验的均值分离度 $d$ 和标准差 $\sigma$）中计算信息差距景观，搜索最大化 $\Delta_{\mathrm{P}}^{\mathrm{info}}$ 同时保持 $\Delta_{\mathrm{L}}^{\mathrm{info}}$ 足够大的“甜点”参数（Figure 5）。优化时需优先考虑后验编码的可区分性，因为 $\Delta_{\mathrm{L}}^{\mathrm{info}}$ 通常比 $\Delta_{\mathrm{P}}^{\mathrm{info}}$ 大一个数量级。

### 收敛与鲁棒性

消融实验表明：降低放电率或增加噪声会减慢信息差距的收敛速度，但最终收敛到相同理论值（Figure 12）；随机采样导致方向覆盖不完整同样减缓收敛（Figure 13A）；较少试次（3k vs 30k）减慢收敛（Figure 13B）；结果对离散化分辨率（0.25° vs 1°）鲁棒（Figure 13C）。这些因素影响实验可行性但不改变理论预测的有效性。

## 实验与分析

### 核心发现：信息差距准确预测解码器性能差异

框架的核心验证在于，理论推导的信息差距能否准确预测实际解码器在模拟神经群体上的性能差异。实验在三种对比度水平（高、中、低）的泊松模拟群体上进行，分别构建似然编码和后验编码群体，训练基于深度神经网络的似然解码器与后验解码器。

**收敛性验证**（Figure 3）：随着试次数量增加（固定500个神经元）或神经元数量增加（固定30k试次），似然解码器与后验解码器的交叉熵性能差异均收敛至理论信息差距（虚线）。这一收敛在高、中、低三种对比度条件下均成立，表明信息差距是解码器性能差异的渐近极限。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/003_Figure_3.jpg]]
*Figure 3: Decoder performance difference on simulated populations converges to the theoretical prediction of information gap. A) On simulated neural populations encoding the likelihood function (left, blue) or the posterior distributions (right, orange) responding to high contrast stimuli, the difference between the likelihood and posterior decoder performances converges to the theoretical value of information gap (dashed lines) as the total number of trials increases (top, with fixed number of neurons = 500), and as the total number of neurons in the population increases (bottom, with fixed number of trials = 30k). (shaded areas denote the s.t.d. across 5 random seeds.) B) Same for medium contrast s...*

**跨参数预测准确性**（Figure 4）：在多种任务设计参数下，理论信息差距（x轴）与经验解码器性能差异（y轴）高度一致，散点紧密分布在 y=x 线附近。该一致性在标准泊松模型和更复杂的增益调制泊松模型（Goris et al., 2014）中均得到验证。值得注意的是，似然编码群体的信息差距通常比后验编码群体大一个数量级，这意味着实验设计的瓶颈在于后验编码的可区分性——若后验编码的信息差距可被检测，似然编码的信号必然更强。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/004_Figure_4.jpg]]
*Figure 4: Information gap accurately predicts decoder performance difference on simulated populations across diverse task settings. A) On simulated Poisson neural populations responding to high (left), medium (middle), and low (right) contrast stimuli, theoretical values of information gap (x-axis) accurately predicts the decoder performance difference on simulated neural populations (y-axis) across multiple task design parameters, for both the likelihood-coding and posterior-coding populations. (Each color marks one set of task parameters used for both types of simulated populations; Error bars denote the s.t.d. across 5 random seeds.) B) Same for simulated populations using a more complex, bio-real...*

### 任务参数优化：寻找“甜点”设计

信息差距景观分析揭示了区分两种编码假说的最优任务参数区域。以高斯先验为例，任务参数空间由两个维度定义：先验均值分离度 $d = |\mu^A - \mu^B|$ 和共享标准差 $\sigma$。

**对比度依赖的最优参数**（Figure 5）：
- **高对比度**：后验编码信息差距在较宽的参数范围内保持正值，设计选择相对灵活。
- **中对比度**：后验编码信息差距的可行区域缩小，需在 $d$ 和 $\sigma$ 之间权衡。
- **低对比度**：后验编码信息差距仅在狭窄参数区域内非零，最优设计位于先验分离度 $d \approx 30^\circ$、标准差 $\sigma \approx 20^\circ$ 附近（图中星号标记）。该“甜点”在保证后验编码可区分的同时，维持似然编码的足够判别信号。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/005_Figure_5.jpg]]
*Figure 5: Information gap landscapes inform practical task designs that optimally differentiate probabilistic representations in neural populations. A) Information gap as a function of task parameters (d: separation between context priors, and σ: context prior standard deviations) for both the likelihood coding hypothesis (top) and the posterior coding hypothesis (bottom) when presented with high contrast stimuli. The asterisks identify strategic task designs that achieve the tradeoff where posterior-coding information gap approaches its maximum while likelihood-coding maintains sufficient discriminative signal. B) Same for medium contrast stimuli and C) for low contrast stimuli*

### 先验分布形态的影响与失败模式

**重尾分布失效**（Figure 6）：当上下文先验采用学生t分布（$\nu=3$）或柯西分布时，后验编码的信息差距在整个参数空间内几乎为零。原因在于重尾先验与高斯似然函数卷积后，产生的后验分布不对称，大幅减少了满足 Eq. 4 的可混淆观测对 $(x_j, x_k)$ 数量（Figure 16）。这使得最优似然解码器能够轻易区分上下文，从而消除了后验编码的信息差距。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/006_Figure_6.jpg]]
*Figure 6: Information gap landscape suggests heavy tailed distributions are not ideal stimulus prior distributions for differentiating coding hypotheses. A) Using student’s t-distribution with degrees of freedom $\nu$ = 3 as stimulus priors (left), information gap under medium contrast stimuli as a function of task parameters (separation d and standard deviations σ) for both the likelihood coding hypothesis (middle) and the posterior coding hypothesis (right) shows decreased information gap with minimal overlap compared to task design with Gaussian context priors. B) Same for Cauchy distribution as stimulus priors with task parameters separation d and scale $\gamma$

**薄尾分布同样失效**（Figure 17, 18）：广义正态分布等薄尾先验同样导致后验不对称，使后验编码信息差距趋于零。因此，高斯先验因其对称性和适中的尾部形态，成为区分两种编码假说的理想选择。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/017_Figure_17.jpg]]
*Figure 17: Information gap landscapes when using generalized normal distribution as context priors. A) Information gap as a function of task parameters (d: separation between context priors, and σ: context prior standard deviations) for both the likelihood coding hypothesis (middle) and the posterior coding hypothesis (right)*

### 实际神经数据验证：传统设计的无效性

在 Allen Visual Coding 数据集（Siegle et al., 2021）上，筛选出试次数量足够的 169 个记录会话（>300 试次），计算似然解码器与后验解码器的交叉熵性能差异。结果为 $0.0024 \pm 0.064$（均值±标准差），与模型预测的零值无显著差异（$p = 0.63$）（Figure 7）。

该结果直接证实：**在单上下文、均匀先验的传统实验范式下，无法区分神经群体编码的是似然函数还是后验分布**。这构成了框架的核心实验动机——必须通过上下文依赖的先验操纵，才能暴露编码格式的差异。

### 收敛速度的影响因素（消融分析）

虽然信息差距的渐近值不受影响，但收敛速度受多种因素调节：

- **放电率与噪声水平**（Figure 12）：降低放电率或增加噪声会减慢收敛，但最终收敛至相同理论值。
- **方向覆盖不完整**（Figure 13A）：随机采样导致的方向覆盖不完整减慢收敛，现代神经电生理记录的多方向覆盖可缓解此问题。
- **试次数量**（Figure 13B）：较少的试次（3k vs 30k）减缓收敛，提示实验设计需保证足够的试次量。
- **离散化分辨率**（Figure 13C）：结果对离散化分辨率鲁棒（0.25° vs 1° bin）。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/012_Figure_12.jpg]]
*Figure 12: Effect of firing rate and noise level*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/013_Figure_13.jpg]]
*Figure 13: Examine factors affecting convergence speed. A) Effect of orientation coverage. B) Effect of trial numbers. C) Effect of bin size*

### 混合编码假说的理论边界

框架进一步分析了混合编码假说（即神经群体同时编码似然和后验信息）的情形。在此假设下，无论似然解码器还是后验解码器都能提取完整的概率信息，因此信息差距为零（Figure 11）。这意味着，若真实神经编码为混合模式，本框架将无法检测到任何差异——这是一个重要的理论边界，需在实际应用中予以注意。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/010_Figure_10.jpg]]
*Figure 10: The information gap computation can incorporate behavior data by estimating the subject’s biased prior from its psychometric curve*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/014_Figure_14.jpg]]
*Figure 14: Information gap landscapes when using student’s t-distribution with degrees of freedom $\nu$ = 3 as context priors. A) Information gap as a function of task parameters (d: separation between context priors, and $\sigma { : }$ context prior standard deviations) for both the likelihood coding hypothesis (top) and the posterior coding hypothesis (bottom) when presented with high contrast stimuli. B) Same for medium contrast stimuli and C) for low contrast stimuli

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/015_Figure_15.jpg]]
*Figure 15: Information gap landscapes when using Cauchy distribution as context priors. A) Information gap as a function of task parameters (d: separation between context priors, and $\gamma \colon$ context prior scales) for both the likelihood coding hypothesis (top) and the posterior coding hypothesis (bottom) when presented with high contrast stimuli. B) Same for medium and C) low contrast stimuli

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_doxBjZ88H3/figures/018_Figure_18.jpg]]
*Figure 18: Thin tailed context priors, when integrated with Gaussian likelihood function, lead to asymmetric posterior distributions, limiting the pairs of identical posteriors satisfying Eq. 12 that would cause imperfect likelihood decoders on posterior-coding populations*

## 方法谱系与知识库定位

### 核心问题与框架定位

在感觉神经编码领域，存在两个长期竞争的假说：**似然编码假说**（以概率群体编码 PPC 为代表，Ma et al., 2006）主张早期感觉皮层编码刺激的似然函数，后验计算推迟到下游脑区完成；**后验编码假说**（以神经采样编码为代表，Hoyer & Hyvarinen, 2002）则认为早期感觉皮层通过整合来自高级皮层的反馈先验信息，直接编码后验分布。传统单上下文实验设计（使用均匀先验）无法区分这两种假说——本文在 Allen Visual Coding 数据集（Siegle et al., 2021）上的实证分析证实了这一点：169个记录会话的似然解码器与后验解码器交叉熵性能差异仅为 0.0024 ± 0.064，与零无显著差异（p = 0.63，Figure 7）。

本文提出的**信息差距最大化实验设计框架**（Information-Gap Maximization Framework）直接针对这一瓶颈，其核心创新在于：通过操纵刺激先验分布（context-specific prior distributions）这一因果调节变量，暴露神经群体编码的概率内容类型。该框架的信息论基础——信息差距 $\Delta^{\text{info}}$——量化了使用似然解码器与后验解码器时的预期交叉熵性能差异，其解析表达式通过真实后验与任务边缘化代理后验之间的 KL 散度推导。

### 与基线方法的对比关系

本文的方法并非提出新的解码器架构，而是构建了一个**元实验设计框架**，其对比对象是实验范式本身：

| 对比维度 | 传统单上下文设计 | 本文信息差距最大化框架 |
|---------|-----------------|---------------------|
| 刺激先验操纵 | 无上下文划分，通常使用均匀先验 | 两上下文高斯先验，均值分离度 $d$ 和标准差 $\sigma$ 经优化 |
| 区分能力 | 似然与后验解码器性能无显著差异（实证验证 p = 0.63） | 信息差距可达到显著正值，尤其在优化后的"甜点"参数处 |
| 理论指导 | 无定量设计准则 | 解析计算信息差距景观，指导参数选择 |

框架中使用的似然解码器 $g_L$ 和后验解码器 $g_P$ 本身是基线组件——前者从群体反应中提取似然信息，后者提取后验信息。本文的贡献不在于改进这些解码器，而在于揭示了它们在何种实验设计下会产生可区分的性能差异，并提供了最大化这种差异的优化方法。

### 方法适用边界

**前提假设：**
- 生成模型（神经元调谐曲线、噪声结构）已知或可合理近似。信息差距的解析计算依赖对 $p(x|\theta)$ 的完整知识。
- 解码器能够逼近最优性能。理论推导基于最优解码器假设，实际深度神经网络解码器可能无法完全达到理论极限。
- 两上下文设计为主。框架主要针对两个离散上下文的实验范式，扩展到连续上下文或多于两个上下文需要进一步分析。

**数据要求：**
- 需要足够的神经元数量和试次数量以保证解码器性能收敛。消融分析显示，较少的试次（3k vs 30k）、较低的放电率或较高的噪声水平会减缓收敛，但不改变最终收敛值（Figure 12, 13）。
- 随机采样导致方向覆盖不完整会减慢收敛，现代神经电生理记录的多电极阵列可缓解此问题（Figure 13A）。

**先验分布选择约束：**
- 重尾分布（如学生 t 分布 $\nu = 3$、柯西分布）或薄尾分布（如广义正态分布）会导致后验编码的信息差距大幅减小甚至趋于零，不适合用于区分编码假说（Figure 6, 14, 15, 17, 18）。其机制在于：重尾或薄尾先验与高斯似然函数卷积后产生不对称的后验分布，限制了满足 Eq. 4 条件的可混淆观测对 $(x_j, x_k)$ 的数量（Figure 16），从而使后验编码群体的信息差距消失。
- 高斯先验是当前框架下的优选分布族，其在参数空间 $(d, \sigma)$ 中展现出丰富的信息差距景观，存在明确的"甜点"区域。

### 关键局限

1. **最优解码器假设**：信息差距的理论值基于最优解码器的极限性能。实际应用中，深度神经网络解码器可能受限于训练数据量、网络容量和优化过程，导致实际可观测的差异小于理论预测。在低信噪比条件下，这一差距可能更为显著。

2. **模型误匹配敏感性**：框架假设生成模型完全已知。当存在未知的神经元噪声结构（如超出泊松假设的相关噪声）时，信息差距的理论预测可能产生偏差。该问题需要手动验证。

3. **似然与后验信息差距的量级不对称**：似然编码群体的信息差距通常比后验编码群体大一个数量级（Figure 4）。这意味着在设计优化时，需要优先确保后验编码的信息差距达到可检测水平，同时维持似然编码的区分信号，形成设计权衡（Figure 8）。

4. **混合编码假说的盲区**：当神经群体采用混合编码策略（如 Ganguli & Simoncelli, 2010 所讨论的介于似然与后验之间的编码方式）时，信息差距理论上为零（Figure 11），框架无法区分。这限制了框架在编码假说连续谱上的适用性。

### 开放问题

1. **混合编码假说的自动化区分**：如何将框架扩展到混合编码假说的检测与量化？当前信息差距在混合编码下归零，需要新的信息论指标或实验设计策略来揭示编码假说的连续谱位置。

2. **行为数据融合**：框架已展示通过心理测量曲线估计被试的偏差先验并融入信息差距计算的流程（Figure 10），但如何在真实实验中动态优化刺激先验以适应个体差异，仍是一个开放问题。

3. **多上下文扩展**：当前两上下文设计的信息差距受限于可混淆观测对的数量。多于两个上下文的设计是否能进一步提高区分效力，需要理论分析和实验验证。

4. **跨模态泛化**：框架在视觉方向辨别任务上进行了验证，其在其他感觉模态（听觉频率辨别、触觉振动检测）下的适用性和最优设计参数尚待探索。

5. **非高斯似然与相关噪声**：在更复杂的生成模型（如非高斯似然函数、神经元间相关噪声）下，信息差距的解析计算是否仍然可行？定点迭代求解最优似然解码器（Eq. 5）的收敛性在更广泛条件下需要验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/An_Information_Theoretic_Framework_For_Optimizing_Experimental_Design_To_Distinguish_Probabilistic_Neural_Codes.pdf]]
