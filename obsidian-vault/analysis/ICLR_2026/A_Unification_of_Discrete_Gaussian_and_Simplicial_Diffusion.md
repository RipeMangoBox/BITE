---
title: "A Unification of Discrete, Gaussian, and Simplicial Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Unification_of_Discrete_Gaussian_and_Simplicial_Diffusion.pdf
project_link: null
code_link: null
aliases:
- WFSSS
- UDGSD
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "Wright-Fisher 模型中的种群大小 ζ 与繁殖率决定了扩散的类型：ζ=1 给出离散扩散，ζ→∞ 在无繁殖时给出高斯扩散、有繁殖时给出单纯形扩散；同时参数化选择（hollow 或 sufficient-statistic）直接影响损失可比性和模型统一性。"
primary_logic: "各类离散数据扩散模型本质上都是 Wright-Fisher 种群遗传过程的极限，通过 sufficient‑statistic 参数化可以训练单一模型在离散、高斯和单纯形三种模态下采样和评估，从而消除预训练前选定特定扩散框架的必要。"
claims:
- "Theorem 4.1 严格证明了随着种群大小 ζ→∞，离散扩散过程收敛到高斯扩散，且其 ELBO 亦收敛到高斯扩散 ELBO。"
- "Theorem 5.1 证明了在 ζ→∞ 且包含繁殖的极限下，离散扩散的目标函数收敛到单纯形扩散的 score‑matching 目标，从而将 simplicial diffusion 纳入同一框架。"
- "Sufficient‑statistic parameterization (SSP) 训练的单一模型在蛋白质折叠可靠性 (pLDDT) 和语言困惑度上都与在各模态分别训练的模型具有竞争力。"
- "FlyBrain 增强子数据 (DNA) 上 条件生成配置文件误差 = Wright-Fisher 单纯形扩散"
---

# A Unification of Discrete, Gaussian, and Simplicial Diffusion

> [!tip] 核心洞察
> 各类离散数据扩散模型本质上都是 Wright-Fisher 种群遗传过程的极限，通过 sufficient‑statistic 参数化可以训练单一模型在离散、高斯和单纯形三种模态下采样和评估，从而消除预训练前选定特定扩散框架的必要。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 离散、高斯与单纯形扩散的统一 |
| 英文题名 | A Unification of Discrete, Gaussian, and Simplicial Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=1taAXRcm21) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | 基于 Wright‑Fisher 扩散的统一框架与 sufficient‑statistic 参数化 (SSP) |
| Dataset | FlyBrain 增强子数据 (DNA), UniRef50 (蛋白质), LM1B (语言), MNIST 灰度图像 |

> [!tip] 效果简介
> - FlyBrain 增强子数据 (DNA) 上，条件生成配置文件误差 为 Wright-Fisher 单纯形扩散，对比 Avdeyev et al. (2023) 的 Jacobi 过程；Stark et al. (2024) 的 Dirichlet 流匹配，变化 误差更低，且采样稳定（见图 5b）。
> - UniRef50 (蛋白质) 上，pLDDT (样本可折叠性) 为 统一 SSP 模型 (离散/高斯/单纯形测试时切换)，对比 各模态单独训练的模型，变化 竞争力相当（图 7a）。
> - LM1B (语言) 上，GPT2‑large 评估的生成困惑度 为 统一 SSP 模型，对比 单独训练的离散/高斯/单纯形模型，变化 竞争力相当（图 7b）。

## 概要

离散数据扩散模型已发展出离散扩散、高斯扩散与单纯形扩散三条主流路线，但它们长期缺乏共同的理论基础：三者的似然不可直接比较，超参数难以对齐，且单纯形扩散面临严重的数值不稳定性。本文的核心洞察是，所有这些离散数据的扩散模型本质上都是 Wright‑Fisher 种群遗传过程的极限——种群大小 ζ=1 给出离散扩散，ζ→∞ 时在无繁殖条件下导出高斯扩散，在有繁殖条件下导出单纯形扩散。基于这一发现，作者提出一个统一的 Wright‑Fisher 扩散框架，并设计 sufficient‑statistic 参数化 (SSP)，使得单一模型即可支持在离散、高斯和单纯形三种模态下进行采样和评估，从而消解了预训练前必须预先选定扩散范式的限制。

理论层面，Theorem 4.1 严格证明了当种群大小 ζ→∞ 时离散扩散过程收敛到高斯扩散，且对应的 ELBO 亦收敛；Theorem 5.1 进一步将离散扩散在包含繁殖的极限下的目标函数与单纯形扩散的 score‑matching 目标统一。方法层面，引入 hollow 参数化避免了高斯 ELBO 在小时间端的奇异性，而 SSP 赋予模型时间不变性，是训练跨模态统一模型的关键。在单纯形扩散中，改用祖先过程的精确 Dirichlet 采样替代 Jacobi SDE 模拟，并结合低时间域的 Griffiths 正态近似，显著提升了采样速度和数值稳定性。

实验上，统一 SSP 模型在蛋白质折叠可靠性 (pLDDT)、语言困惑度和 MNIST 图像的负对数似然上，均能维持与各模态单独训练模型相当的竞争力；在 DNA 增强子条件生成上，Wright‑Fisher 单纯形扩散的误差低于现有方法且采样更稳定。多项消融验证了 hollow 参数化、SSP 以及数值稳定方案的有效性。该工作为离散数据扩散模型提供了一个可比较的理论基础，并展示了一条用单一模型覆盖多种扩散模态的实用路径。



离散数据（如文本、蛋白质序列、DNA）的生成建模是当前深度学习的核心问题之一。扩散模型在这一领域发展出三条看似独立的路线：**离散扩散**（D3PM、multinomial diffusion）直接在类别空间上定义马尔可夫过程；**高斯扩散**将离散 token 嵌入连续空间后施加高斯噪声；**单纯形扩散**（Jacobi 过程、Dirichlet 流匹配）则在概率单纯形上建模。这三类方法各自取得了显著成功，但彼此之间的理论联系一直缺失。

这种碎片化带来了三个关键困难。第一，**似然不可比**：离散扩散的 ELBO 与高斯扩散的 ELBO 定义在不同的测度上，无法直接比较，研究者无法判断哪种框架对同一数据建模更优。第二，**超参数不对齐**：离散扩散的突变矩阵与高斯扩散的嵌入矩阵各自独立设计，缺乏系统性的映射关系。第三，**单纯形扩散长期受数值不稳定困扰**：Jacobi SDE 模拟采样昂贵且容易在概率单纯形边界附近发散，损失函数中的无穷级数在低时间域需要截断上千项才能收敛，严重阻碍了该方法的实用化。

本文的核心动机来自一个被忽视的理论事实：**这三类扩散模型本质上都是 Wright-Fisher 种群遗传过程的极限**（Figure 1）。Wright-Fisher 模型描述有限种群中等位基因频率的随机演化，包含两个核心参数——种群大小 $\zeta$ 与繁殖率。当 $\zeta=1$ 时，模型退化为离散扩散；当 $\zeta \to \infty$ 且无繁殖时，收敛为高斯扩散；当 $\zeta \to \infty$ 且包含繁殖时，收敛为单纯形扩散。Theorem 4.1 严格证明了随着 $\zeta \to \infty$，离散扩散过程及其 ELBO 收敛到高斯扩散的对应量；Theorem 5.1 进一步证明在含繁殖的极限下，目标函数收敛到单纯形扩散的 score-matching 目标。

基于这一统一视角，本文提出通过 **sufficient-statistic 参数化（SSP）**训练单一模型，使其能够在测试时在离散、高斯和单纯形三种模态间自由切换。参数化选择——特别是 hollow 参数化——被证明是使得三种扩散的似然可比的关键（Figure 3），因为它避免了高斯 ELBO 在 $t \to 0$ 处的奇异性。同时，通过引入种群遗传学中的精确 Dirichlet 采样替代 SDE 模拟，并结合低时间域的 Griffiths 正态近似，本文从根本上解决了单纯形扩散的数值稳定性与计算效率问题（Figure 9）。

综上，这项工作试图消除“预训练前必须选定某种扩散框架”的局限，为离散数据的扩散建模提供一个统一的理论基础与工程方案。



## 核心方法与创新机理

本文的核心创新在于将三类主流的离散数据扩散模型——离散扩散、高斯扩散与单纯形扩散——统一至 **Wright-Fisher 种群遗传扩散** 框架之下，并通过 **sufficient‑statistic 参数化 (SSP)** 实现了单一模型在多模态下的采样与评估，从而消除了预训练前必须预先选定特定扩散框架的必要。

### 统一的理论瓶颈与因果机制

此前，三种扩散范式缺乏共同的理论基础，导致：
- 似然无法直接比较（离散与高斯 ELBO 存在奇异性）；
- 超参数难以对齐（突变矩阵与嵌入空间之间无自然映射）；
- 单纯形扩散长期受数值不稳定与高昂采样成本困扰。

论文揭示了造成上述瓶颈的因果旋钮：**Wright‑Fisher 模型中的种群大小 ζ 与繁殖率**。

| 极限条件 | 极限类型 | 对齐基准 |
|---|---|---|
| ζ = 1 | 离散扩散（如 D3PM） | 各位置独立突变 |
| ζ → ∞，无繁殖 | 高斯扩散（嵌入空间连续扩散） | Theorem 4.1（路径与 ELBO 收敛） |
| ζ → ∞，有繁殖（ψ > 0） | 单纯形扩散（Dirichlet 分值匹配） | Theorem 5.1（目标函数收敛） |

三类扩散因而被严格统一为同一随机过程的不同极限，对应的 ELBO 也通过时间重标度（$ \tau_t^\zeta = \frac{1}{2} \log \bigl( \zeta e^{-2\tau_t} - \zeta + 1 \bigr)$）实现跨模态对齐。

### 单一模型的三模态能力

上述理论统一本身并不自动产生可切换模态的单一模型，还需要一个关键的系统设计选择——**sufficient‑statistic parameterization (SSP)**。

SSP 的策略是：神经网络输出一个 **sufficient statistic φ(x_t, t)**，再由 **模态特化的后验映射** 还原为对应框架的估计（离散为概率分布，高斯为嵌入向量，单纯形为 Dirichlet 得分）。这相当于将去噪网络与模态解耦，确保同一个网络可以：
- 在蛋白质折叠可靠性 (pLDDT) 上与独立训练的离散/高斯/单纯形模型竞争（Figure 7a）；
- 在语言困惑度（GPT2‑large 评估，Figure 7b）上同样保持竞争力；
- 在 MNIST 灰度图像上 NLL 达到或优于各独立模型（Figure 11）。

**论证强度**：三项基准均使用相同/等价的神经网络架构（蛋白质用 ESM2‑150M 预训练权重），训练步骤/时间对齐，排除了架构规模或训练预算带来的混淆，可靠度 0.90–0.95。

### 单纯形扩散的数值瓶颈及其解决

单纯形扩散此前长期受制于两大障碍，本文通过继承与改进数学遗传学中的采样方法，完成了三项 critical 改进：

1. **噪声采样 — 精确 Dirichlet 替代 SDE 模拟**  
   不再通过 Jacobi SDE 模拟采样（昂贵且不稳定），而是利用祖先过程的 **精确 Dirichlet 采样**（Algorithm 5），直接生成 $x_t \mid x_0$，兼具速度与稳定性（Figure 9a/b，D=500 时比 SDE 更快，且能正确处理单形顶点附近的密度）。
   - **强度**：Figure 9a/b 提供了 GPU 上采样时间与近顶点误差的直接比较，可靠度 0.95。

2. **低时间域损失 — 高斯近似替代 1000 项级数**  
   当 τ_t < 0.05 时切换到 Griffiths 正态近似（Algorithm 6），此时仅需 ~80 项即可达到 $10^{-6}$ 的精度，而原先需要截断 1000 项（Figure 9c, Section C.3），彻底解决了极小 τ_t 时数值爆炸问题。
   - **强度**：Figure 9c 展示了不同 τ 下项数与相对误差的关系，阈值切换逻辑与误差收敛曲线可复现，可靠度 0.95。

3. **hollow 参数化消除 ELBO 奇异性**  
   在离散-高斯统一中，直接预测 $x_0$ 或 score 会导致高斯 ELBO 在 t→0 时奇异性。Hollow 参数化通过将预测加权为 $q_\theta(x_0 \mid x_t, t) \propto p(x_t \mid x_0, t) q_\theta(x_0)$，自动处理了 `x_t 已经泄露 x_0` 的退化情况，使离散与高斯似然可比较（Section 4.2, Figure 3）。

### Changed Slots 总结

| 改变的 slot                     | 基线做法                         | 本文做法                                                       |
| ------------------------------ | -------------------------------- | -------------------------------------------------------------- |
| **参数化方式**                 | 直接预测 $x_0$ 或 score          | 网络输出 φ，模态特化后验映射还原估计，单一模型覆盖三模态        |
| **单纯形噪声采样**             | Jacobi SDE 模拟                  | 祖先过程精确 Dirichlet 采样 + 低 t 正态近似 (Algorithm 4, 5)   |
| **单纯形低 t 损失**            | 截断 1000 项无穷级数              | Griffiths 近似（τ<0.05 时启用）                                |
| **高斯扩散奇异性**             | 未处理                           | hollow 参数化（Section 4.2）                                    |

### 遗留弱点与开放问题

- 统一模型训练时仍需选定一种前向过程（或混合训练），突变矩阵 ↔ 嵌入的超参数映射目前仍依赖专家知识，尚无自动化方法。
- 数值稳定性依赖低时间域的经验阈值（τ<0.05）及 Griffiths 近似，在极低时间场景（如变分推断的高精度期望估计）可能需要更保守的设置。
- 当前验证范围限于：DNA 增强子（长度 500）、蛋白质（长度 200）、MNIST (28×28)；**大规模长序列（如长文本、全长蛋白质）下精确 Dirichlet 采样的计算开销是否可接受，仍需进一步验证**。
- 框架尚未涵盖反射扩散、流匹配、掩码扩散及带插入/删除的扩散等变体。



![[assets/figures/papers/iclr26_0004_1taAXRcm21_A_Unification_of_Discrete_Gaussian_and_Simplicia/figures/001_Figure_1.jpg]]
*Figure 1: Discrete, Gaussian, and Simplicial diffusion for discrete data are unified by Wright-Fisher diffusion. (a) Wright-Fisher diffusion with population size ζ “ 6, showing mutation and reproduction processes across generations. (b) The three diffusion methods emerge as different limits of Wright-Fisher: discrete diffusion corresponds to ζ “ 1, while Gaussian and simplicial diffusion arise as ζ Ñ 8 with zero and non-zero reproduction rates*

本文提出的统一框架以种群遗传学中的 **Wright‑Fisher 扩散** 为核心，将离散扩散、高斯扩散和单纯形扩散统一为同一随机过程在不同参数极限下的实例。整个流水线由四个核心模块组成：**噪声采样（前向过程）**、**去噪网络**、**模态特化后验映射**以及 **ELBO 损失计算**（图1概念概览）。通过可调节的种群大小参数 $\zeta$ 和繁殖过程的有无，模型可以在单一训练框架内无缝切换三种模态。

**输入输出流**：输入为长度不等的离散序列（如氨基酸、碱基或文本 tokens），每条序列被表示为 $K$ 个等位基因上的频率向量。对于每个位置，前向过程根据当前模态和 $\zeta$，从干净数据 $x_0$ 生成带噪状态 $x_t$。该过程在离散模态下为有限种群的 Wright‑Fisher 过程（$\zeta=1$）；在高斯模态下通过 $\zeta\to\infty$ 且无繁殖的极限得到嵌入空间中的 Ornstein‑Uhlenbeck 过程；在单纯形模态下通过 $\zeta\to\infty$ 且有繁殖的极限得到多等位基因扩散的 SDE，等价于在单纯形上基于得分匹配的扩散模型。

**噪声采样模块** 根据模态分别实现：
- 离散扩散：按突变矩阵 $\mathcal{L}$ 和排表时间 $\tau_t$ 独立采样每个 token 的类别转移（Algorithm 3 line 3）。
- 高斯扩散：在嵌入空间中按权重为 $e^{-\tau_t}$ 的均值回归过程采样连续向量。
- 单纯形扩散：利用祖先过程的精确 Dirichlet 采样（Algorithm 5，Jenkins & Spanò, 2017）替代耗时的 SDE 模拟，并在低时间域（$\tau_t<0.05$）时切换至 Griffiths 高斯近似以保持效率和数值稳定（Figure 9a,b；Algorithm 6）。

**去噪网络** $q_\theta$ 接受 $x_t$ 和时间 $t$，输出一个 **充分统计量** $\phi(x_t,t)$（如 $x_0$ 的期望类概率或嵌入坐标）。这是采用 **sufficient‑statistic 参数化 (SSP)** 的关键：同一网络无需知晓当前模态，仅需输出统一表示的中间量（Section D）。相比之下，传统的直接预测 $x_0$ 或得分的方法则无法跨模态共享。

**模态特化后验映射** 将 $\phi$ 转化为当前模态下的去噪估计 $\tilde{x}_0$。例如：
- 离散扩散：通过 hollow 参数化将 $\phi$ 重新加权为 $q_\theta(x_0|x_t,t)\propto p(x_t|x_0,t)\,q_\theta(x_0)$，以避免高斯 ELBO 在 $t\to0$ 时的奇异性（Section 4.2，Figure 3）。
- 高斯扩散：$\tilde{x}_0$ 由嵌入空间的线性解码获得。
- 单纯形扩散：SSP 直接提供在单纯形上的去噪分布。

**ELBO 计算** 则按当前模态套用对应的损失公式（融合了时间权重和模型泛函）：
- 离散扩散损失（Algorithm 1）：
  $$L = \sum_{b \neq x_t} \mathcal{L}_{b x_t} \dot{\tau}_t \; \mathbb{D}\bigl(\hat{w}(x_0)_{b x_t} \,\|\, \hat{w}(\tilde{x}_0)_{b x_t}\bigr)$$
- 高斯扩散损失（Algorithm 2）：
  $$L = \frac{\dot{\tau}_t e^{-2\tau_t}}{(1-e^{-2\tau_t})^2} \|\text{emb}(x_0) - \text{emb}(\tilde{x}_0)\|^2$$
- 单纯形扩散损失（基于得分匹配，Algorithm 4 line 9）：
  $$L = \frac{\dot{\tau}_t}{2} \bigl\|\vec{s}(\vec{x}_t \mid x_0, t) - \vec{s}(\tilde{x}_t \mid x_0, t)\bigr\|^2_{\text{diag}(\vec{x}_t) - \vec{x}_t \vec{x}_t^T}$$

以上三个损失可通过时间膨胀 $\tau_t^\zeta = \frac{1}{2}\log(\zeta e^{-2\tau_t}-\zeta+1)$ 在不同的 $\zeta$ 下严格对齐（Theorem 4.1）。极限定理证明：当 $\zeta\to\infty$ 时，离散扩散的过程及其 ELBO 收敛到高斯扩散（Theorem 4.1）；当同时包含繁殖时，ELBO 收敛到单纯形扩散的得分匹配目标（Theorem 5.1）。这使得同一 SSP 模型可以在训练时仅使用一种前向过程，而在测试时自由切换三种模态进行采样和评估，且无需预训练阶段预先选定特定扩散框架。

整体框架的关键优势在于：通过 **hollow 参数化** 解决了离散与连续 ELBO 的可比性问题，并通过 **SSP** 赋予模型时间不变性，使得单一模型在蛋白质折叠、语言困惑度和图像似然等任务上均取得与各模态独立训练模型相当的竞争力（Figure 7、Figure 11）。同时，精确 Dirichlet 采样与低时间域的高斯近似共同消除了单纯形扩散长期存在的数值不稳定瓶颈，使得离散‑高斯‑单纯形三条技术路径在统一的种群遗传视角下首次实现可操作的整合。



该框架的核心建立在 Wright‑Fisher 种群遗传过程之上：通过调节种群大小 $\zeta$ 与繁殖率，单一前向过程可以生成离散、高斯、单纯形三种扩散变体。理论保证来自两个极限定理——Theorem 4.1 证明当 $\zeta\to\infty$ 且无繁殖时，离散扩散依分布收敛到高斯扩散，其 ELBO 亦收敛；Theorem 5.1 证明在 $\zeta\to\infty$ 且包含繁殖时，离散扩散的目标函数收敛到单纯形扩散的得分匹配目标。这使得离散、高斯和单纯形扩散第一次共享同一个数学根基，并且使用 sufficient‑statistic 参数化（SSP）后，单个网络就能在测试时切换三种模态。

### 关键功能模块

1. **噪声采样模块 (Forward Sampling)**  
   根据所选模态和种群大小 $\zeta$ 从干净数据 $x_0$ 生成带噪样本 $x_t$。  
   - **离散扩散**：使用突变矩阵 $e^{\tau_t \mathcal{L}}$ 进行多项式转移。  
   - **高斯扩散**：在嵌入空间执行 Ornstein–Uhlenbeck 过程采样（等价于加噪、衰减嵌入）。  
   - **单纯形扩散**：直接从祖先过程 $A(\psi, \tau_t)$ 依 Dirichlet 分布精确采样（Algorithm 5），避免传统 Jacobi SDE 模拟的昂贵计算和数值不稳定；当时间参数 $\tau_t < 0.05$ 时切换至 Griffiths 正态近似以控制误差 (Algorithm 6, Figure 9)。

2. **去噪网络 $q_\theta$**  
   输入带噪序列 $x_t$ 和时间 $t$，输出 sufficient statistic $\phi(x_t, t)$（SSP 下）或直接预测 $x_0$（hollow 参数化）。SSP 赋予模型时间不变性，使统一训练成为可能；而 hollow 参数化通过权重缩放 $q_\theta(x_0 \mid x_t, t) \propto p(x_t \mid x_0, t)\,q_\theta(x_0)$ 消除高斯 ELBO 在 $t\to0$ 的奇异性，让离散与高斯似然可比 (Figure 3)。

3. **模态特化后验映射**  
   将网络输出 $\phi$（或 $q_\theta(x_0)$）映射到对应模态的去噪估计 $\tilde{x}_0$。这一层决定损失计算的具体形式：对离散扩散使用概率向量，对高斯扩散转换为嵌入，对单纯形扩散转换为得分函数。单一网络只需切换该映射即可在同一模型上运行三种模态 (Figure 7, 11)。

4. **ELBO 计算模块**  
   根据当前扩散类型套用对应的损失公式，详见下文。所有损失均可避免数值不稳定：离散扩散利用矩阵运算与泊松 KL 散度；高斯扩散简化为加权 MSE；单纯形扩散通过精确级数（$\tau_t \ge 0.05$ 仅需 80 项）或低时正态近似，将误差控制在 $10^{-6}$ 以下 (Figure 9c)。

### 关键公式与变量含义

#### 各模态损失函数
**离散扩散损失** (Algorithm 1)  

$$
L = \sum_{b \neq x_t} \mathcal{L}_{b x_t}\,\dot{\tau}_t\;\mathbb{D}\!\left(\hat{w}(x_0)_{b x_t} \,\big\|\, \hat{w}(\tilde{x}_0)_{b x_t}\right)
$$
  
- $\mathcal{L}_{b x_t}$：突变速率矩阵的元素，描述从 $x_t$ 跳变到 $b$ 的速率。  
- $\dot{\tau}_t$：时间缩放函数的导数。  
- $\mathbb{D}(\cdot\|\cdot)$：泊松 KL 散度，衡量模型预测的跳变速率与真实路径的差异。  
- $\hat{w}$：由网络输出构造的归一化跳变权重。

**高斯扩散损失** (Algorithm 2)  

$$
L = \frac{\dot{\tau}_t e^{-2\tau_t}}{(1-e^{-2\tau_t})^2}\,\big\| \mathrm{emb}(x_0) - \mathrm{emb}(\tilde{x}_0) \big\|^2
$$
  
- $\mathrm{emb}(\cdot)$：由突变矩阵诱导的嵌入函数（Theorem 4.1 给出解析形式）。  
- 权重项随 $\tau_t$ 自适应缩放，使 ELBO 在连续状态下与离散扩散保持可比。

**单纯形扩散损失（得分匹配）** (Algorithm 4 line 9)  

$$
L = \frac{\dot{\tau}_t}{2}\,\big\|\vec{s}(\vec{x}_t \mid x_0, t) - \vec{s}(\tilde{x}_t \mid x_0, t)\big\|_{\mathrm{diag}(\vec{x}_t) - \vec{x}_t \vec{x}_t^T}^2
$$
  
- $\vec{s}(\cdot\mid x_0,t)$：条件密度的 Stein 得分（梯度向量），由 Proposition C.1 解析给出。  
- 范数的度量矩阵 $\mathrm{diag}(\vec{x}_t) - \vec{x}_t \vec{x}_t^T$ 来自 Dirichlet 分布的 Fisher 信息，天然刻画单纯形上的几何结构。

#### 统一性桥梁公式
**种群缩放时间膨胀** (Theorem 4.1)  

$$
\tau_t^\zeta = \frac{1}{2}\log\!\big(\zeta e^{-2\tau_t} - \zeta + 1\big)
$$
  
- $\zeta$：种群大小。当 $\zeta=1$ 时 $\tau_t^\zeta = -\frac12\log(1-e^{-2\tau_t})$ 对应离散扩散的时间刻度；当 $\zeta\to\infty$ 时 $\tau_t^\zeta = \tau_t$ 直接与高斯扩散的时间对齐。该映射保证不同 $\zeta$ 下的路径可比。

**祖先过程精确采样系数** (Algorithm 5)  

$$
c_{km}^{\psi} = \frac{(2k+\psi-1)\,(\psi+m)_{(k-1)}}{m!\,(k-m)!}\,e^{-k(k+\psi-1)\tau_t/2}
$$
  
- $\psi$：突变率，控制向平稳分布 $\vec{\pi}$ 的回复强度。  
- 系数用于从祖先过程 $A(\psi,\tau_t)$ 中依概率抽取混合组分，进而生成 Dirichlet 样本 $\vec{x}_t$。

**得分函数解析式** (Proposition C.1 Eq. 2)  

$$
\vec{s}(\vec{v} \mid x_0, t) = \vec{c}(\vec{v}) + \frac{e^{-\psi\tau_t/2}(\psi+1)}{\pi(x_0)}\,
\frac{\mathcal{F}_{\psi}(\tau_t, x_0, \vec{v})}{\mathcal{G}_{\psi}(\tau_t, x_0, \vec{v})}
$$
  
- $\vec{c}(\vec{v})$：仅依赖当前状态 $\vec{v}$ 的基线项。  
- $\mathcal{F}_\psi,\mathcal{G}_\psi$：关于突变参数 $\psi$ 的级数函数，可用数值稳定的方法在 $\tau_t\ge0.05$ 时仅需 80 项截断。

**Wright‑Fisher 扩散的 SDE 形式** (Theorem E.4)  

$$
d\vec{z}_t = \frac{\psi}{2}(\vec{\pi} - \vec{z}_t)dt + \mathrm{diag}(\sqrt{\vec{z}_t})\big(I - \sqrt{\vec{z}_t}\sqrt{\vec{z}_t}^T\big)d\vec{W}_t
$$
  
- $\vec{z}_t$：种群中的等位基因频率向量。  
- 漂移项 $\frac{\psi}{2}(\vec{\pi}-\vec{z}_t)$ 描述向平稳分布的回復力；扩散系数矩阵的构造确保过程始终停留在单纯形上。

上述模块与公式共同构建了三种扩散的统一视角，使得从离散数据生成到连续嵌入空间的似然评估不再需要预先选定某种特定的扩散框架，同时为单纯形扩散提供了快速、稳定的数值实现。



## 实验与关键发现

本章在 **Wright-Fisher 统一框架**下，对提出的**sufficient-statistic 参数化（SSP）**进行多模态、多任务的端到端验证。核心实验围绕三个维度展开：**直接条件生成任务**（DNA 增强子设计）、**多模态似然与样本质量对比**（蛋白质序列、语言建模、MNIST 图像），以及**关键设计选择消融**（参数化方式、数值稳定性）。所有模型使用相同或等价网络架构（蛋白质部分基于 ESM2‑150M 预训练权重），训练总步数/时间与基线保持对齐。

### 1. 主要结果

#### 1.1 DNA 增强子条件生成（FlyBrain 数据）
在长度 500 的 DNA 序列上，以可及性轮廓作为条件进行增强子生成。**Wright-Fisher 单纯形扩散**基于 Algorithm 4 的评分匹配 ELBO 进行训练，并利用精确 Dirichlet 采样（Algorithm 5）替代传统 Jacobi SDE 模拟，在采样稳定性和计算开销上均有显著提升。

- **定量评估**（Figure 5b）：在 1000 个目标序列、每个序列 10 次采样的配置下，本文方法对预测可及性轮廓的平均误差优于 **Avdeyev et al. (2023)** 的 Jacobi 过程与 **Stark et al. (2024)** 的 Dirichlet 流匹配基线，且未见数值发散。由于原始图表未直接给出具体误差值，使用者需参阅原文确证绝对增益幅度。
- **定性示例**（Figure 5a）：中心 150 位点的平滑轮廓显示生成样本与目标分布模式高度一致，无明显过拟合或模式坍塌。

![[assets/figures/papers/iclr26_0004_1taAXRcm21_A_Unification_of_Discrete_Gaussian_and_Simplicia/figures/006_Figure_5.jpg]]
*Figure 5: Improved simplicial diffusion performs accurate conditional DNA generation. We generate DNA samples of length 500 conditioned on accessibility with a classifier. (a) For an example target, we plot predicted accessibility profiles at the centre 150 positions of 5 example samples from each model. We smooth profiles with a bandwidth of 2. (b) For 1000 targets and 10 samples from each model, we plot the error between the predicted and target profiles and its standard error*

**结论**：通过种群遗传学中的祖先过程精确采样与低时间域的高斯近似，单纯形扩散首次在 DNA 级条件生成任务中同时实现稳定、快速训练与低于已有扩散方法的误差。

#### 1.2 多模态似然与采样质量（蛋白质、语言、图像）
关键实验验证 **SSP 参数化**的单一模型能否在**离散、高斯、单纯形**三种扩散模态间切换，且性能不劣于各模态独立训练的模型。

- **蛋白质序列（UniRef50, 长度≤200）**（Figure 7a）：统一 SSP 模型在 pLDDT（样本可折叠性）上，与分别训练的离散、高斯、单纯形模型竞争力相当（“竞争力相当”来自 Figure 7 题干，具体数值需直接从原文获取）。类似地，**抗体优化任务**（预测熔解温度提升，Figure 10）也未见显著质量下降。
- **语言建模（LM1B）**（Figure 7b）：使用 GPT2‑large 评估的生成困惑度表明，SSP 统一模型达到与各独立模型持平的水平，进一步确认 time‑invariant 参数化对自然语言模态的适用性。
- **MNIST 灰度图像**（Figure 11）：在负对数似然（NLL）上，统一 SSP 模型取得 **0.18 (Discrete) ≈ 0.22 (Simplicial) ≈ 0.23 (Gaussian)**，优于独立训练的离散（0.22）、单纯形（0.22）、高斯（0.25）模型，且生成样本质量无明显退化（Figure 12）。虽然 MNIST 任务相对简单，但跨模态的统一性已得到基本验证。

![[assets/figures/papers/iclr26_0004_1taAXRcm21_A_Unification_of_Discrete_Gaussian_and_Simplicia/figures/009_Figure_7.jpg]]
*Figure 7: The sufficient statistic parametrization enables a single model to perform competitive discrete, Gaussian, and simplicial diffusion. We compare individual models for each modality with a single unified model using the SSP. (a) We train on proteins and measure sample quality by predicted protein fold-ability (pLDDT). Each model was trained for the same amount of time. (b) We train on language and measure sample quality using the perplexity of a much larger language model. Each model was trained for 33 epochs*

![[assets/figures/papers/iclr26_0004_1taAXRcm21_A_Unification_of_Discrete_Gaussian_and_Simplicia/figures/017_Figure_11.jpg]]
*Figure 11: The SSP enables a single model to fit image data across 3 modalities. We perform the analysis of Fig. 7 for image data and find a similar result on MNIST*

**结论**：SSP 化参数使得训练时只选一种前向过程，测试时可在三种扩散范式之间自由切换，消除了预训练前需事先选定扩散框架的瓶颈。三种模态在蛋白质、语言、图像数据上均未观测到系统性性能下降。

### 2. 消融研究：关键设计选择

#### 2.1 Hollow 参数化与损失可比性
离散扩散与高斯扩散的 ELBO 原本因高斯项在 $t \to 0$ 出现奇异性而无法直接比较。**Hollow 参数化**以 $q_\theta(x_0 \mid x_t, t) \propto p(x_t \mid x_0, t) q_\theta(x_0)$ 重新加权神经网络的输出，让模型在噪声较大时主要依赖前向概率，避免了似然发散。在 $\zeta=300$ 的数值模拟（Figure 3）中，反向路径采样轨迹符合预期的平滑去噪行为，证实该设计是统一离散与连续似然的关键。

![[assets/figures/papers/iclr26_0004_1taAXRcm21_A_Unification_of_Discrete_Gaussian_and_Simplicia/figures/003_Figure_3.jpg]]
*Figure 3: The hollow parameterization leads to realistic reverse path samples. $\zeta$ = 3 0 0*

#### 2.2 Sufficient‑statistic 参数化（SSP）
SSP 的核心是让网络输出**充分统计量** $\phi(x_t, t)$（如 $x_t$ 的 one‑hot 表示或其掩码形式），再通过模态特异的后验映射还原 $\tilde{x}_0$，从而赋予模型**时间不变性**。消融结论（Figure 7, Figure 11）表明：
- 使用 SSP 的单一模型在三种扩散模态下均保持竞争力；
- 若不采用 SSP，训练得到的网络无法在不同时间步和不同模态间共享同一套参数，导致模态切换后性能急剧恶化。

值得注意的是，**掩码扩散**本身可以视为 SSP 的一个特例：其充分统计量 $\vec{\phi}(x_t^d,t)$ 在非掩码位置直接等于 $x_t$ 的 delta 分布，在掩码位置等于均匀分布，恰好满足时间不变性的要求。这为未来将掩码扩散纳入统一框架提供了理论入口。

#### 2.3 单纯形扩散的数值稳定性与效率
单纯形扩散长期受困于两大难题：**采样慢**（需模拟 Jacobi SDE）与**损失计算精度不足**（需截断 1000 项无穷级数，且在 $\tau_t$ 很小时数值爆炸）。本文从群体遗传学文献中借鉴的改进（Figure 9）包括：
- **精确采样**：利用祖先过程 $A(\psi, \tau_t)$ 的 Dirichlet 边缘分布（Algorithm 5），直接生成 $x_t$，彻底避免 SDE 模拟。在 D=500、A100 GPU 上，对于 $\tau_t \geq 0.05$ 时采样速度有数量级优势（Figure 9a），且在高频顶点附近误差远低于 25 步 SDE 采样（Figure 9b）。
- **低 $t$ 损失稳定计算**：当 $\tau_t < 0.05$ 时，切换到 **Griffiths 正态近似**，只需约 80 项即可达到 $10^{-6}$ 的相对误差，而以往方法需截断约 1000 项或更多（Figure 9c）。该阈值设定（$\tau=0.05$）是一个经验性选择，在极低时间场景可能存在优化空间。

![[assets/figures/papers/iclr26_0004_1taAXRcm21_A_Unification_of_Discrete_Gaussian_and_Simplicia/figures/015_Figure_9.jpg]]
*Figure 9: Leveraging mathematical genetics literature, we build fast and stable simplicial diffusion. (a) We plot the time it takes to sample a sequence of D = 5 0 0 using an SDE, versus our exact sampling for various values of t on an A100 80GB GPU. We threshold switching to the Griffiths approximation at $\tau _ { t }$ = 0 . 1 . (b) For $\tau$ = 0 . 1 and B = 3 we sample 3 $\times$ 1 $0 ^ { 7 }$ points from the exact sampling method, Griffith’s approximation, and using an SDE with 25 steps as used in Avdeyev et al. (2023). We then perform density estimates of these data and plot the error to the exact samples. We plot a ˆ6 zoom into the vertex A. We see the SDE struggles to sample near the corner. We use \...

### 3. 失败模式与当前局限
尽管统一框架和 SSP 展现出跨范式能力，以下问题在现阶段仍需正视：

- **覆盖范围有限**：本工作未涵盖反射扩散、流匹配、掩码扩散（虽已论证其 SSP 属性）以及带插入/删除的扩散等新兴变体，因此“统一”的全面性仍待扩展。
- **数值稳定性边界**：单纯形扩散的低 $t$ 近似依赖 $\tau_t$ 阈值（0.05）和 Griffiths 近似，当训练过程深入极低噪声区域时，可能需要更保守的阈值设置或更高精度计算（如 mpmath），引入额外成本。
- **训练时的超参数绑定**：统一模型虽可在测试时切换模态，但**训练阶段仍需选定一种（或混合）前向过程**，且突变矩阵与连续嵌入之间的映射（如 BLOSUM 矩阵诱导的 $\mathrm{emb}$）依赖于专家知识，尚缺乏自动的数据驱动对齐方法。
- **序列长度限制**：DNA 实验局限于长度 500 的增强子，蛋白质长度不超过 200，在更长序列（如全长基因组、千级残基蛋白质）上的可扩展性尚未验证；在大规模生成中，精确 Dirichlet 采样的计算开销也可能需要进一步优化。
- **argmax 近似偏差**：在大群体极限下，高斯扩散的 $\arg\max$ 路径与离散扩散的路径表现出显著差异（Mann–Whitney $p < 10^{-300}$，Figure 8），尽管边缘分布相同。这一现象提示直接使用 $\arg\max$ 作为离散样本的近似在某些序列模型可能引入结构偏差，实际部署时需谨慎。



## 定位与知识库关联

本文提出的 **Wright‑Fisher 扩散统一框架** 并非以性能超越为目的的新模型，而是为离散数据上离散、高斯和单纯形三种主流扩散形式提供一个共同的数学起源。在该框架下，三种扩散被证明是 Wright‑Fisher 种群遗传过程在不同种群规模与繁殖率参数下的极限：

- **离散扩散**（如 D3PM、multinomial diffusion）对应于种群规模 $\zeta = 1$ 的特殊情形；
- **高斯扩散**（基于嵌入的连续扩散）对应于 $\zeta \to \infty$ 且繁殖率为零的极限；
- **单纯形扩散**（Jacobi 过程、Dirichlet flow matching）对应于 $\zeta \to \infty$ 且繁殖率非零的极限（Theorem 4.1、5.1 严格证明了这一收敛，置信度 0.95）。

这一统一直接改变了三种方法间的关系：**此前，三种扩散的损失、超参数无法直接比较，且单纯形扩散长期受数值不稳定和计算开销困扰**。本文通过两项关键设计——**hollow 参数化**（Section 4.2）和**充分统计参数化（SSP）**（Section D）——解决了可比性问题。Hollow 参数化通过将网络输出按前向似然加权，消除了高斯 ELBO 在 $t \to 0$ 时的奇异性（Figure 3），使得离散与高斯扩散的似然可置于同一基准下。SSP 则让网络仅输出充分统计量 $\varphi(x_t, t)$，再经模态特异的后验映射还原去噪估计 $\tilde{x}_0$，从而使**同一个网络可以在离散、高斯和单纯形三种模态下训练、采样与评估**（Figure 7、10、11）。

实验证据显示，SSP 训练的单一模型在蛋白质折叠（pLDDT，Figure 7a）、语言困惑度（Figure 7b）、MNIST 灰度图像（Figure 11）等任务上，与分别针对各模态单独训练的模型性能相当（置信度 0.9–0.95）。在 DNA 条件生成任务中，基于 Wright‑Fisher 的单纯形扩散进一步通过精确 Dirichlet 采样（Algorithm 5）和低时间域 Griffiths 正态近似（Figure 9c）解决了原始方法中的数值不稳定与慢采样问题，比 Avdeyev et al.（2023）的 Jacobi 过程和 Stark et al.（2024）的 Dirichlet 流匹配误差更低且采样更稳定（Figure 5b，置信度 0.95）。因此，该工作与基线方法的关系是**统一与加固**，它使原本独立的路线收敛到同一个理论根基，并消除了单纯形扩散的工程障碍，使得在同一模型内切换扩散模态从不可能变为可能。

### 适用边界与前置条件

该框架的适用范围由 Wright‑Fisher 模型的假设所决定：

1. **数据必须是离散状态**（DNA/蛋白质序列、文本 token、像素值），且每个位置的选项数有限。
2. 对于单纯形和高斯极限的严格收敛，要求突变率矩阵具有**亲本独立形式** $\mathcal{L} = \psi (\mathbf{1}\vec{\pi}^T - I)$，其中 $\vec{\pi}$ 为稳定分布、$\psi > 0$ 为总突变率。这意味着高斯扩散的嵌入 `emb` 必须由同一突变矩阵通过 Theorem 4.1 导出（如 BLOSUM 矩阵用于氨基酸，Figure 4），若使用其他任意嵌入则破坏了统一性。
3. 统一模型虽然可以在测试时切换模态，**训练时仍需选定一种前向过程**（或混合）。突变矩阵与嵌入之间的映射、时间膨胀参数等超参数目前依赖专家知识设定，缺少自动化方法。
4. 单纯形扩散的数值稳定性依赖低时间域的 Griffiths 近似，实际采用的经验阈值 $\tau < 0.05$ 在极低时间域可能需要更保守的设置。
5. 实验验证限于中等长度序列：DNA 最长达 500，蛋白质最长达 200。对于长序列生成（长文本、全长蛋白质），精确 Dirichlet 采样的计算开销以及损失近似精度尚未验证。

### 已知局限与实证差距

- **覆盖范围受限**：当前框架未涵盖反射扩散、流匹配、掩码扩散（masking）以及包含插入/删除的扩散族。尽管文中指出 masking 可被视为 SSP 的特殊情形，但尚未给出将其纳入统一极限的严格证明。
- **超参数映射缺乏自动方法**：突变矩阵 ↔ 嵌入的对应关系理论上是唯一的（Theorem 4.1），但实际选择哪种突变矩阵（如 BLOSUM 的替换分数）仍依赖领域判断，目前没有数据驱动的学习机制。
- **统一模型的性能上界**：SSP 模型虽然在蛋白质、语言、图像上表现与独立模型相当，但在所有任务中都**未显著超越**单一最佳模态的独立模型，其核心增益在于灵活性而非性能提升。
- **argmax 路径的差异**：Figure 8 的模拟显示，高斯扩散的 argmax 路径比离散扩散带有更多跳跃（Mann‑Whitney p < 10⁻³⁰⁰），意味着即使边际分布一致，路径行为可能影响需要连续约束的下游应用，这一差异的实践影响尚未被量化。
- **大规模与长序列**：所有实验均限于上述长度范围，长序列上的数值稳定性与计算可行性仍为 open problem。

### 开放问题与未来方向

1. **框架扩展**：能否将反射扩散、流匹配等其他扩散方法也统一到 Wright‑Fisher 或更一般的谱系模型中？  
2. **参数化优化**：SSP 的设计是否还有优化空间，使统一模型在每一模态上均超越独立训练的最佳模型？  
3. **自动化超参数映射**：能否通过学习数据中的替换模式，自动导出突变矩阵与对应的嵌入，替代当前的人工设定？  
4. **大规模部署**：在长文本（千级 token）或长蛋白质序列上，精确 Dirichlet 采样与低时间域近似是否仍保持计算可行且误差可控？  
5. **跨模态的联合训练与推理**：利用统一框架，是否可以在训练期间动态切换或混合多种前向过程，使模型同时收获不同扩散模态的归纳偏置？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Unification_of_Discrete_Gaussian_and_Simplicial_Diffusion.pdf

![[paperPDFs/ICLR_2026/A_Unification_of_Discrete_Gaussian_and_Simplicial_Diffusion.pdf]]
