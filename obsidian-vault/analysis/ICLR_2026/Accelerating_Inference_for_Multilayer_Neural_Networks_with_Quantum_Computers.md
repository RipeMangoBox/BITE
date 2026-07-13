---
title: "Accelerating Inference for Multilayer Neural Networks with Quantum Computers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Accelerating_Inference_for_Multilayer_Neural_Networks_with_Quantum_Computers.pdf
project_link: null
code_link: null
aliases:
- QARCCESASCLN
- AIMNNQC
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/physics
core_operator: "残差跳跃连接（ResNet 风格）保证了前向传播向量的 ℓ₂ 范数下限，从而使得可以在不依赖 QRAM 的情况下构建全相干多层量子网络，并支持多项式深度的电路实现。"
primary_logic: "残差块确保每次归一化前向量的 ℓ₂ 范数可有效下界，避免了范数的指数衰减，同时跳跃连接使得量子电路深度仅随层数多项式增长，而非指数增长。"
claims:
- "首次实现具有非线性激活的多层神经网络的全相干量子实现"
- "残差块中跳跃连接保证了前向范数在归一化层之前保持下界"
- "无需 QRAM 的 2D 多滤波器卷积的块编码"
- "对任意密集满秩矩阵与向量逐元素平方的乘积进行量子算法，无 Frobenius 范数依赖"
---

# Accelerating Inference for Multilayer Neural Networks with Quantum Computers

> [!tip] 核心洞察
> 残差块确保每次归一化前向量的 ℓ₂ 范数可有效下界，避免了范数的指数衰减，同时跳跃连接使得量子电路深度仅随层数多项式增长，而非指数增长。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 利用量子计算机加速多层神经网络推理 |
| 英文题名 | Accelerating Inference for Multilayer Neural Networks with Quantum Computers |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=QcRto0GjxC) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/physics |
| Method | Quantum-accelerated residual CNN with coherent erf/sigmoid activations, skip connections, and layer normalization |
| Dataset | Exact classical 2D convolution (N-dim vectorized input, d=2), Exact classical 2D convolution (with QRAM for weights, no input QRAM, Deep network with k nonlinear layers, full QRAM access |

> [!tip] 效果简介
> - Exact classical 2D convolution (N-dim vectorized input, d=2) 上，时间复杂度 为 $O(N \log(1/\varepsilon)^{2k})$，对比 $\Omega(N^{2})$，变化 二次加速。
> - Exact classical 2D convolution (with QRAM for weights, no input QRAM, d=2) 上，时间复杂度 为 $O(N \log(N/\varepsilon)^{2k})$，对比 $\Omega(N^{3})$，变化 四次加速。
> - Deep network with k nonlinear layers, full QRAM access 上，推理代价 为 $O(\mathrm{polylog}(N/\varepsilon)^{k})$，对比 $O(N^{d} \ldots)$ with $d\ge2$，变化 相对经典多项式的多对数加速。

## 概要

本文致力于解决利用量子计算加速多层神经网络推理的核心瓶颈：传统量子神经网络加速方法在层间依赖量子态断层扫描或中间测量，破坏了相干性，并且缺乏跨层的范数保持保证，导致电路深度随层数指数增长，严重限制了加速效果。针对这一问题，作者提出了一种全新的全相干量子多层网络实现方案，其关键在于利用残差跳跃连接（ResNet风格）保证前向传播向量的 ℓ₂ 范数下界，从而无需依赖既昂贵又未定型的 QRAM（量子随机存取存储器），即可构建电路深度仅随层数多项式增长的多层量子网络。

方法上，本文首次实现了具有非线性激活（erf/sigmoid）的相干多层神经网络。作者开发了一套完整的量子子程序模块：包括向量编码（VE）框架下的运算规则、无 QRAM 的 2D 多滤波器卷积块编码、对任意满秩稠密矩阵与向量逐元素平方乘积的量子算法（避免 Frobenius 范数依赖）、以及通过多项式近似实现的相干非线性激活。这些模块通过残差跳跃连接与归一化层组合成可证范数保持的残差块，进而级联为深层网络，所有操作均在完整相干态上进行，无需任何中间测量或经典后处理。

在理论加速方面，本文根据量子数据接入假设划分了三种体制（图1）：(1) 输入与权重均通过 QRAM 高效访问，此时可实现推理代价 $O(\mathrm{polylog}(N/\varepsilon)^k)$，相对经典方法获得多对数加速；(2) 仅权重存储于 QRAM 而输入为经典存储，得到 $O(N\log(1/\varepsilon)^{2k})$ 的复杂度，比精确经典实现带来四次方加速；(3) 完全不依赖 QRAM 的输入假设，仍可实现二次方加速。这些结果首次在多层量子网络中结合了相干非线性与范数保持保证，并在对比表（表1）中展示了相对于现有方案在相干多层构造、无 QRAM 操作、$\mathrm{polylog}(1/\varepsilon)$ 误差依赖和输入维度多对数标度等维度上的关键提升。部分证据（如无 QRAM 卷积编码）置信度极高（1.0），而范数保持的理论保证仍需在具体激活缩放细节上稍作人工验证（置信度 0.85）。此外，网络深度的多项式指数增长（如 $O(\log(\sqrt{N}/\varepsilon)^{2k})$）依然对极深网络构成规模化挑战，且 QRAM 假设在真实大规模量子硬件上的可行性尚未解决，这些因素在实际应用中需予以关注。

### 問題背景

深度神經網路在電腦視覺、自然語言處理等領域取得了顯著成功，但其推理過程對經典計算資源的需求隨輸入維度 $N$ 和網路深度 $k$ 急劇增長。對於 $d$ 維卷積輸入，經典精確計算的下界可達 $\Omega(N^d)$ 甚至 $\Omega(N^{d+1})$，這促使研究者探索量子加速的可能性。近年來，多項工作嘗試將卷積神經網路（CNN）、前饋網路和 Transformer 架構映射到量子電路上，期望利用量子平行性和振幅編碼實現多對數級別的推理複雜度。

### 現有方法的關鍵缺口

儘管先前工作在量子神經網路加速方面取得進展，但存在兩個核心瓶頸：

**瓶頸一：層間相干性破壞。** 現有量子實現方案（如 Cong et al. (2019)、Allcock et al. (2020)、Kerenidis et al. (2020) 以及 Guo et al. (2024b) 所提出的方法）在相鄰層之間往往需要進行量子態斷層掃描或中間測量（tomography / readout）。這意味著非線性激活函數的實現依賴經典後處理，導致量子電路無法以全相干方式貫穿整個多層網路。正如論文所述：「據我們所知，我們首次推導出具有非線性激活的多層神經網路的全相干量子實現」（Section 4）。這一斷裂不僅增加了時間開銷，更使得深層網路的量子優勢難以兌現——每層的測量和重新編碼將累積 $O(\mathrm{poly}(1/\epsilon))$ 而非 $O(\mathrm{polylog}(1/\epsilon))$ 的誤差依賴（見 Table 1 對比）。

**瓶頸二：跨層範數衰減與 QRAM 依賴的雙重約束。** 在不具備範數保持機制的前饋網路中，輸入向量的 $\ell_2$ 範數隨層數指數衰減。這引發一個致命後果：若實現每層變換的酉電路需要對輸入向量編碼進行哪怕兩次調用，電路複雜度將隨非線性激活層數呈指數增長。此外，先前的量子卷積實現普遍依賴 QRAM 提供經典數據的高效量子訪問，但 QRAM 在大規模容錯量子電腦上的硬體可行性至今未經驗證，構成了理論方案與物理實現之間的核心不確定性。

### 本文動機與核心思路

針對上述瓶頸，本文旨在回答一個關鍵問題：**能否在不依賴中間測量且不假設 QRAM 的前提下，實現具有非線性激活的多層深度網路的全相干量子加速？**

這個問題的突破口來自於殘差網路（ResNet）的核心設計元素——**跳躍連接（skip connection）**。其因果機制可概括為：

- **範數下界保持**：在殘差塊中，跳躍連接確保每次歸一化層之前的正向傳播向量 $\ell_2$ 範數具有高效可計算的下界。具體而言，當權重層經過歸一化（即參數矩陣的譜範數 $\lVert W \rVert_2 \le 1$）且激活函數被縮放至 Lipschitz 常數 $\le 1$ 時，可證明範數不會在層間傳遞中指數衰減（Lemma 6, Lemma 7）。

- **電路深度多項式增長**：範數下界的保持直接解耦了電路複雜度與網路深度的指數依賴。由於每層無需對衰減後的微弱訊號進行多次重複放大，酉電路實現的代價僅隨層數 $k$ 多項式增長，為 $O(\log(N/\epsilon)^{2k})$ 甚至 $O(\mathrm{polylog}(N/\epsilon)^k)$（在三種量子數據訪問模式下）。

論文進一步提供了兩項關鍵的子程式創新以支撐上述架構：**(1)** 無需 QRAM 的二維多濾波器卷積塊編碼（Lemma 5），消除了對 QRAM 硬體假設的依賴；**(2)** 任意滿秩密集矩陣與向量逐元素平方乘積的量子算法（Section 2.3），避免了 Frobenius 範數或秩依賴帶來的額外開銷。這些技術組件與殘差跳躍連接、相干 erf/sigmoid 多項式近似、歸一化層共同構成了一個完整的推理管線（見 Figure 1，三種數據訪問假設下的架構），使得首次在嚴格的理論保證下實現了全相干多層非線性網路的量子加速。

## 核心方法与创新机理

相较于既有的量子神经网络加速方案，本文的核心变革在于 **通过架构创新化解了多层非线性变换的相干性破坏瓶颈**，使量子电路深度随网络深度仅多项式增长，并由此导出对经典精确计算的超多项式加速。以下围绕分层前向传播中被扭转的四个关键设计槽位，剖析其因果机制与证据强度。

### 1. 从“测量中断”到“全相干多层实现”

**基线现实**（Cong 等 2019; Allcock 等 2020; Kerenidis 等 2020）：量子网络每经过一个非线性层就需要量子态断层扫描或中间测量，将量子态回传给经典计算机处理激活，破坏了量子相干性，导致层间量子优势被抹平。  
**本文改动**：首次证明可在不进行任何中间读取或断层扫描的情况下，相干地执行多层网络前传，包括非线性激活（erf/sigmoid）和层归一化。  
**因果机制**：这一突破依赖于 *范数下界保持*（见第3点），它确保每一层的输出态能被后续层的酉演算高效调用，而不需要经典重构。由此，整个 $k$ 层残差块序列的电路深度仅为 $\mathcal{O}(\log^{2k}(\sqrt{N}/\epsilon))$（Lemma 7, Theorem 2），而非指数增长。  
**证据**：论文明确宣称“据我们所知，这是首次相干实现多层带非线性激活的量子神经网络”（Section 4, confidence 1.0），并通过 Lemma 6、7 给出了严格的块编码与向量编码构造。

### 2. 解除 QRAM 依赖：无 QRAM 的 2D 多滤波器卷积

**基线现实**：先前大部分量子卷积加速方案（如 Kerenidis 等 2020）依赖高效的量子随机存取存储器（QRAM）来读取输入数据或权重，而 QRAM 在大规模量子系统中的可行性仍存争议。  
**本文改动**：构建了 **无 QRAM 的块编码** 来实现二维多滤波器卷积（Lemma 5），且该块编码的构造利用了移位矩阵与张量积分解，无需任何 QRAM 查找。  
**因果机制**：该块编码直接嵌入到残差块的线性变换部分，使得即便在“仅权重可量子化”或“无任何量子输入假设”的访问模式下（Regime 2 与 3），前传仍能在量子计算机上高效完成。  
**证据**：“我们提供了一个新颖的无 QRAM 块编码，用于二维多滤波器卷积”（Section 2.4, confidence 1.0）。该构造在实验复杂性中直接支撑了 Regime 2 下 $\mathcal{O}(N \log(N/\epsilon)^{2k})$ 的时间复杂度，实现了对经典精确卷积的四次加速（baseline $\Omega(N^3)$）。

### 3. 范数保持：跳跃连接与 Lipschitz 约束的联合保证

**基线现实**：普通前馈量子网络在每一层都可能使向量范数指数衰减，导致后续块编码需要反复调用输入编码，从而使电路深度随层数指数爆增（ablations 指出“即使仅需两次输入编码调用，复杂度就会指数增长”，confidence 0.9）。  
**本文改动**：在残差块中引入 $x \leftarrow x + f(x)$ 形式的跳跃连接，同时要求参数层的谱范数 $\|W\|_2 \le 1$ 并将激活函数缩放至 Lipschitz 常数 $\le 1$，从而保证每次归一化前向量的 $\ell_2$ 范数可有效下界。  
**因果机制**：范数下界使得归一化层（如 $\ell_2$ 归一化）的作用被限制在有限区域内，并允许块编码以 $\mathcal{O}(\log(1/\epsilon))$ 的开销实现，而非反复放大错误。这正是全相干多层可行性的数学核心：“残差块中的前向范数在每次归一化前都有效下界”（Section 3 关键洞察, confidence 1.0）。  
**证据**：消融分析明确对比了无跳跃连接时的指数衰减问题（confidence 0.9），并通过 Lemma 6 定量给出了范数保持的界限（confidence 0.85 关于 Lipschitz 约束的充分性）。

### 4. 非线性激活的相干量子实现

**基线现实**：以往工作要么在经典计算机上执行激活（断层扫描后处理），要么在参数化量子电路中用旋转门模拟有限的非线性（如 Cong 等 2019 的 CNN 启发 PQC），难以对标标准网络精度。  
**本文改动**：利用多项式近似（如针对 $\operatorname{erf}(mx)$ 构造的 $P_{k,m}(x)$ 多项式，Lemma B.19, 附录 F）并通过 **非线性幅度变换（NLAT）** 框架，相干地实现了 $\operatorname{erf}$ 和 $\operatorname{sigmoid}$ 激活，近似误差按 $\epsilon$ 可控。  
**因果机制**：将非线性函数表示为作用在振幅上的多项式运算，再借助块编码与线性组合工具（LCU）在酉子空间中合成该多项式。该过程完全相干，无需测量或经典反馈。  
**证据**：在架构管线（Pipeline Modules）中明确包含“非线性激活（erf/sigmoid 多项式近似）”，且文献中给出了 $\operatorname{erf}$ 逼近的构造细节（confidence 0.95）。同时，Coherent non‑linearity 作为 Table 1 的独立评估维度，本文在所有 3 个 regime 下均获“✓”，而几乎所有对比方法均缺失该项。

### 创新产出：复杂度革命

上述四个槽位的协同改变，使不同数据访问假设下均产生实质性加速：
- **Regime 2（权重量子化，无 QRAM 输入）**：对 2D 卷积推理实现四次加速（$\Omega(N^3) \to \mathcal{O}(N\log(N/\epsilon)^{2k})$），是已知首次在无 QRAM 假设下对精确经典计算的多项式幂次提升。  
- **Regime 3（全 QRAM 访问）**：推理代价降至 $\mathcal{O}(\operatorname{polylog}(N/\epsilon)^k)$，相对经典 $\Omega(N^d)$ 实现了多对数加速（confidence 1.0）。  
- **隐含瓶颈**：多项式近似引入的误差按深度累积为 $\mathcal{O}(\operatorname{poly}(\log(1/\epsilon))^{2k})$，对于极深网络（大 $k$）可能抵消加速，这是当前架构的天然限制；同时 Regime 3 的 QRAM 假设在工程上尚未落地，需读者留意。

*（复杂度声明均源自 Theorem 2 与 Section 4 的三个 Regime 分析；消融与误差传播见附录与 main results 列的 anchor。）*

![[assets/figures/papers/iclr26_0005_QcRto0GjxC_Accelerating_Inference_for_Multilayer_Neural_Net/figures/001_Figure_1.jpg]]
*Figure 1: Architecture for Convolutional Neural Networks. This figure shows the architectures we consider with provable quantum complexity guarantees for inference under three regimes of quantum data access assumptions. (a) Depicts the architecture where both the inputs and network weights are provided in an efficient quantum data structure. (b) Only the network weights are provided in an efficient quantum data structure. (c) No input assumptions are made. In all architectures, the input is assumed to be a rank-3 tensor (e.g., images with 4 channels)*

![[assets/figures/papers/iclr26_0005_QcRto0GjxC_Accelerating_Inference_for_Multilayer_Neural_Net/figures/002_Table_1.jpg]]
*Table 1: Comparison with prior work. We briefly explain the meaning of each column. Coherent multi-layer refers to the construction of multi-layer architectures separated by non-linear activation functions without tomography. Coherent non-linearity refers to the implementation of non-linear transformations on the quantum computer without readout. Norm preservation refers to the preservation of vector norms throughout the network forward pass. Next, each quantum implementation of a classical architecture incurs some error over the exact classical implementation, and as such an entry ✓ in the polylog 1/ϵ column indicates a $O($\mathrm{polylog}$(1/$\epsilon$))$ error-dependence, whilst a ✗ entry indicates a $O($\mathrm{poly}$(1/$\epsilon$))$ error-dependence.

![[assets/figures/papers/iclr26_0005_QcRto0GjxC_Accelerating_Inference_for_Multilayer_Neural_Net/figures/003_Figure_2.jpg]]
*Figure 2: Generic Residual Architectural Block. This diagram illustrates the structure of a typical residual block used in deep neural networks. The input vector x is transformed through a sequence of operations: a learnable linear transformation W , a non-linear activation function f , and a residual (skip) connection that adds the original input to the transformed signal. The output is then passed through a normalization layer (norm)*

本文提出一种量子加速的残差卷积神经网络（Residual CNN）框架，首次实现了带非线性激活函数的多层神经网络的全相干量子实现。框架核心在于通过残差跳跃连接保证前向传播中向量 ℓ₂ 范数的有效下界，从而避免范数的指数衰减，并使得量子电路深度仅随网络层数多项式增长，而非指数增长（"*the forward norm of the vector is efficiently lower-bounded prior to every normalization layer*"）。整体架构由一系列可组合的量子子模块构成，支持三种不同的数据访问假设（图1）：(a) 输入与权重均以量子态高效提供；(b) 仅权重量子化；(c) 不依赖任何量子输入假设。

**流水线及模块关系**  
整个推理过程沿着如下模块链路运行：  
1. **输入编码**（Definition A.1, Section E.1）—— 将经典张量（如多通道图像）通过 QRAM 或经典特征提取转化为量子态（向量编码）。  
2. **2D 多滤波器卷积块**（Lemma 5）—— 提供无需 QRAM 的块编码（*"QRAM-free block-encoding for 2D multi-filter convolutions"*），实现对任意二维卷积的量子相干操作。  
3. **非线性激活**（Lemma B.19）—— 采用多项式近似实现 erf（进而 sigmoid）等函数的相干非线性变换，无需中间读出或断层扫描。  
4. **归一化层**（详见 Lemma 6）—— 保持特征向量的范数，防止信息在深层网络中流失。  
5. **残差跳跃连接** —— 将输入直接加到归一化后的输出上，形成残差学习结构。该跳跃连接与权重层归一化（$\|W\|_2 \le 1$）及激活函数 Lipschitz 常数 $\le 1$ 的设计共同保证了范数下界（*"if the weight layers are normalized … and the activation function is scaled so that its Lipschitz constant … is at most 1, this results in provable norm-preservation bounds"*）。  
6. **残差块序列**（Lemma 7）—— 上述卷积、激活、归一化与跳跃连接组合为一个残差块（General Skip Norm Block），多个块串联构成深层网络，电路深度随块数 k 按 $O(\log(\sqrt{N}/\varepsilon)^{2k})$ 尺度增长。  
7. **输出池化与线性层**（Lemma C.2）—— 将最后一层的高维特征映射为一组类别概率（如通过全连接与池化等操作），最终通过测量获得分类结果。

**输入‑输出流**  
- **输入**：原始经典张量（如 N 维向量表示的多通道图像），依据数据访问假设，可经 QRAM 或经典特征提取编码为子归一化量子态（vector-encoding）。  
- **前向传播**：量子态依次经过 k 个残差块，每个块内部通过块编码实现卷积、多项式激活和范数保持的归一化操作，全部在相干量子态上进行，无中间测量。跳跃连接将输入直接融入块输出，实现恒等映射与残差学习的结合。  
- **输出**：最后通过池化与线性层得到 C 维输出量子态，其各分量概率幅度对应该输入属于各类别的概率（近似采样型分类，见 Definition 1）。采样该量子态即可获得分类标签及对应概率。

整个框架无需在层间进行量子态断层扫描，且核心的卷积块编码摆脱了对 QRAM 的依赖，从而为量子神经网络的可扩展性提供了关键支撑（相关比较见表 1）。

该工作的核心突破在于构建了一套全相干的多层量子神经网络推理流程，**不依赖中间量子态断层扫描或经典读出**，并给出了多项式级电路深度的严格保证。以下逐一提炼构成该流程的关键模块及支撑其正确性与复杂度的核心公式。

### 量子编码框架：向量编码与块编码
所有量子运算均建立在**向量编码（VE）**与**块编码（BE）**两种基本数据接入机制之上。

- **$(\alpha, a, \varepsilon)$-块编码**（Block-encoding）通过酉矩阵 $U$ 左上角嵌入矩阵 $A$，满足  
  $$\| A - \alpha ( \langle 0 | ^{\otimes a} \otimes I ) U ( | 0 \rangle ^{\otimes a} \otimes I ) \| \leq \epsilon$$
  其中 $\alpha$ 为归一化因子，$a$ 为辅助量子比特数，$\epsilon$ 为误差界（Definition 2）。

- **$(\alpha, a, \varepsilon)$-向量编码**则将子归一化向量 $|\psi\rangle/\alpha$ 嵌入酉矩阵 $U_\psi$ 的第一列，满足  
  $$\| |\psi\rangle_n - \alpha \left( \langle 0|_a \otimes I_n \right) U_\psi |0\rangle_{a+n} \|_2 \leq \epsilon$$
  其中 $n$ 为向量维度，$\alpha\ge 1$ 保证嵌入不被放大（Definition 3）。

此框架的意义在于：所有后续模块均被表达为 VE/BE 之间的组合，且误差传播可通过 $\epsilon$ 严格控制，无需经典中间读出。

### 无 QRAM 的 2D 多滤波器卷积
传统量子卷积加速往往依赖 QRAM 来加载权重，而本文给出了一种**无需 QRAM 的块编码方案**（Lemma 5）。其核心是将二维多滤波器卷积表示为移位矩阵的线性组合：
$$\mathcal{C} := \sum_{i=0}^{C-1} \sum_{j=0}^{C-1} \sum_{k=0}^{D-1} \sum_{l=0}^{D-1} K_{i,j,k,l} (|i\rangle\langle j|_c \otimes Q^l \otimes Q^k)$$
其中 $K$ 为卷积核参数，$Q$ 为循环移位矩阵，$C$、$D$ 分别为通道数和空间尺寸。通过 $|i\rangle\langle j|$ 在通道空间上的块结构与 $Q$ 的拆解，可直接利用通用块编码组合技术构造出 $(\text{poly}(D), O(\log N), \epsilon)$-块编码，复杂度与卷积核大小相关但**不依赖输入全维度 $N$**。

### 相干非线性激活：erf/sigmoid 的多项式近似
为在量子线路中相干地施加非线性，需将激活函数近似为多项式。文中利用 **erf 函数的多项式逼近**（Lemma B.19），构造了针对 $\operatorname{erf}(mx)$ 的度数 $k$ 多项式：
$$P_{k,m}(x) := \frac{2 m e^{-m^{2}/2}}{\sqrt{\pi}} \left( I_{0}(m^{2}/2) x + \sum_{j=1}^{(k-1)/2} I_{j}(m^{2}/2) (-1)^{j} \left( \frac{T_{2j+1}(x)}{2j+1} - \frac{T_{2j-1}(x)}{2j-1} \right) \right)$$
该多项式在 $[-1,1]$ 上以误差 $\leq \epsilon$ 逼近 erf，且其 **Lipschitz 常数经缩放可被控制在 ≤ 1**。这为随后范数保持提供了基础：若权重层归一化（$\|W\|_2 \le 1$）且激活函数的 Lipschitz 常数 ≤ 1，则前向范数存在有效下界。

### 残差块与范数保持机制
**残差跳跃连接**是整个框架维持计算可行性的根本机制。一个残差块（图 2 所示）将输入 $x$ 变换为 $x + \mathcal{F}(x)$，其中 $\mathcal{F}$ 由线性变换 $W$、非线性激活 $\sigma$ 和归一化构成。若无跳跃连接，向量范数可能随层数指数衰减，导致 VE 的归一化因子 $\alpha$ 爆炸，使电路深度指数增长。跳跃连接则保证每次归一化前**向量的 $\ell_2$ 范数可被有效下界**（Lemma 6），从而阻断指数恶化。

残差块的单层量子实现电路复杂度为（Lemma 6）
$$O\left(\log\left(\frac{\sqrt{N}}{\epsilon_1}\right) \log\left(\frac{1}{\epsilon_1}\right) (a+b+n+T_1+T_2)\right)$$
其中 $N$ 为输入总维度，$\epsilon_1$ 为单块误差，$a,b$ 为辅助比特，$T_1,T_2$ 分别为卷积、激活组件深度。该复杂度对 $N$ 仅呈 polylog 依赖，在全相干条件下首次实现。

### 多层串联与电路深度控制
将 $k$ 个残差块串联后，总体量子线路深度可保持为（Lemma 7）
$$O\left(\log\left(\frac{\sqrt{N}}{\epsilon}\right)^{2k} (a+2b+n+T_1+T_2)\right)$$
注意因子 $\log(\sqrt{N}/\epsilon)^{2k}$ 相对于层数 $k$ 是多项式增长的，而非指数。最终含输出池化与线性层的完整推理电路总深度为（Theorem 2）
$$O\left(\log\left(\frac{\sqrt{N}}{\epsilon}\right)^{2k+1} (T_X + n^2)\right)$$
其中 $T_X$ 为输入编码代价。这证明了在全相干非线性多层架构下，量子电路深度只随层数多项式上升，而非指数崩溃。

### 输出模块：全秩线性池化
最后一层将高维特征向量压缩为类别概率。文中采用**任意密秩全秩矩阵与向量逐元素平方的乘积**的量子算法（Section 2.3），避免了对 Frobenius 范数或秩的依赖。结合线性组合和池化操作，输出模块可被表达为 VE 到最终概率抽样的映射，维持了全流程的相干性。

> 以上模块的量化结论严格依赖 QRAM 存在假设（除 Regime 3 外），多项式近似误差会随深度累积；极深网络的实际加速效果仍需数值验证。但残差保持范数这一机制在理论上已排除了以往工作中指数深度这一根本障碍。

## 实验与关键发现

本文并未进行传统意义上的数值实验，而是通过在三种数据访问体制下严格推导推理复杂度，验证所提出量子残差‑CNN 的理论加速效果。所有“实验”结果均为时间复杂度上界与经典精确计算的下界对比，并辅以消融分析和架构比较（Table 1）。下面依次讨论主加速结果、消融分析、失效模式，以及关键图表的结论。

### 主结果：三种数据访问体制下的加速

论文以输入维度 $N$（向量化二维输入的维数）、误差 $\epsilon$、网络层数 $k$ 为主要变量，分别在以下三种体制下给出了推理复杂度上界：

1. **仅输入以量子数据结构提供 (Regime 1, 对应 Figure 1a)**：  
   - 所提方法：$O\big(N \log(1/\epsilon)^{2k}\big)$  
   - 经典精确计算下界：$\Omega(N^2)$  
   - 加速特性：相对于经典精确实现，获得**二次加速**；当 $k$ 为常数时加速效果最明显。

2. **仅权重以 QRAM 提供，输入无量子假设 (Regime 2, 对应 Figure 1b)**：  
   - 所提方法：$O\big(N \log(N^{d/2}/\epsilon)^{2k}\big)$  
   - 经典精确计算下界：$\Omega(N^3)$（对于 $d=2$ 的二维卷积）  
   - 加速特性：**四次加速**，且不要求输入的量子化存储。

3. **输入与权重均以 QRAM 提供 (Regime 3, 对应全量子设定)**：  
   - 所提方法：$O\big(\mathrm{polylog}(N/\epsilon)^k\big)$  
   - 经典下界：多项式级别（$\Omega(N^d)$，$d\ge 2$）  
   - 加速特性：实现**多对数级别加速**，将经典下界的多项式依赖转化为对 $N$ 的多对数依赖，有效缓解维数灾难。

这三组复杂度结果均以定理形式给出，且附有误差传播分析：误差在残差块内部被有效控制，总电路深度随 $k$ 按 $O\big(\log(\sqrt{N}/\epsilon)^{2k}\big)$ 增长，而无指数爆炸。Table 1 将这些特性与先前的量子神经网络工作进行了对比，确认本文首次实现**无中间层析或测量的全相干多层构造**、同时在无 QRAM 条件下提供了**二维多滤波器卷积的块编码**，以及**通过残差连接实现范数保持**等一系列突破。

### 消融分析：跳跃连接与 Lipschitz 约束的关键作用

论文通过消融论证揭示了维持量子多层相干性的两个核心设计：

- **残差跳跃连接的范数下界保证**：若移除跳跃连接，则每经过一个参数化权重层（全连接或卷积），前向传播状态的 $\ell_2$ 范数可能呈指数衰减。一旦范数低于某个阈值，后续的归一化层就无法在酉运算框架内被可靠实现，导致电路深度随层数指数增长。残差块的“skip connection”将前一层输出直接加到经权重和非线性变换后的结果上，从而在每次归一化前为 $\ell_2$ 范数提供了一个可有效下界的保证，避免了范数消失。

- **激活函数的 Lipschitz 缩放**：将所用非线性函数（erf/sigmoid 或其它满足条件的激活）缩放到其在 $[-1,1]$ 上的 Lipschitz 常数不超过 1，与权重矩阵谱范数 $\le 1$ 的约束相配合，确保变换不会放大向量范数。这样既维持范数下界，又避免上界爆炸，从而使得跳跃连接后的范数下界得以传递到下一层。

若取消其中任何一个设计（即使用普通层而非残差块，或不限制激活的 Lipschitz 常数），文中给出的复杂度保证将不再成立，电路深度会随网络加深而指数膨胀。这一消融结论直接支撑了本文“残差结构＝多项式深度 ”的核心论断。

### 失效模式与局限性

以下三点是该方法从理论走向实践需要手动验证或进一步解决的关键瓶颈：

1. **QRAM 假设的现实性**：全量子输入体制（Regime 3）以及部分结果需要 QRAM 实现高效数据加载。目前大规模 QRAM 的物理实现尚未验证，其在实际系统中的能耗、纠错开销和访问延迟未知。若 QRAM 不存在或开销巨大，则多对数加速的实际收益将下降至 Regime 1 或 Regime 2 的水平。

2. **多项式误差随深度的累积**：整个网络的电路深度关于 $k$ 呈 $O(\log(\sqrt{N}/\epsilon)^{2k})$ 增长，这意味着即使每层误差有 $\mathrm{polylog}(1/\epsilon)$ 依赖，整体误差预算 $\epsilon$ 会随深度指数级收紧；对于极深的网络，保持相同水平的最终误差可能需要非常高的子例程精度，从而削弱加速效果。该限制在文中已被指出，但未给出深度的定量界限。

3. **满秩和稠密矩阵假设**：矩阵‑向量乘积的平方算法（Section 2.3）以及相应块编码依赖于矩阵为满秩且稠密的假定。对于低秩或结构稀疏的权重矩阵，其加速比可能无法保证，且文中未提供此类条件下的容错分析。

4. **缺乏数值基准对比**：所有结论均为理论复杂度推导，没有与经典 GPU/TPU 实现的实际时延进行对照实验。对实际加速倍数的估计需进一步在含噪中等规模（NISQ）或容错量子原型上验证。

### 图表结论摘要

**Table 1** 系统比较了本文及其三个变体与先前六项工作的六项关键属性：相干多层实现、相干非线性、无 QRAM 操作、范数保持、误差依赖为 $\mathrm{polylog}(1/\epsilon)$，以及输入维度 $N$ 的多对数复杂度。该表表明本文是**唯一在所有列同时满足全部属性的方法**（除先前的参数化量子电路工作因目的不同而无法比较误差与输入维度栏外）。这一对比从定性层面支持了所提框架在量子神经网络设计空间中的跃迁式改进。

**Figure 1** 展示三种数据访问体制下的神经网络架构示意图，直观说明了输入编码、卷积块、非线性激活、归一化和跳跃连接等模块的连接方式。该图在结论中并非直接提供量化结果，而是澄清了每一种体制的假设前提，从而框定了对应加速结论的适用范围。

总体而言，以上理论实验和分析表明：通过残差连接与 Lipschitz 约束的组合设计，量子多层神经网络确实可以在不破坏相干性、不依赖中间测量的前提下实现可证明的多项式深度电路，并能在不同数据加载假设下提供从二次到多对数的加速。该结论在很大程度上依赖于 QRAM 假设与多项式误差控制，未来需要在更现实的量子计算模型下进一步验证。

![[assets/figures/papers/iclr26_0005_QcRto0GjxC_Accelerating_Inference_for_Multilayer_Neural_Net/figures/004_Figure_3.jpg]]
*Figure 3: Circuit for addition of VE encoded vectors. Given two unitary matrices, $U_\psi$ which is a $($\alpha$, a, $\epsilon_$0)$-VE for the n-qubit state $|$\psi\rangle$, and $U_\phi$ which is a $($\beta$, b, $\epsilon_$1)$-VE for the n-qubit state $|$\phi\rangle$ define $c := $\max$(a, b)$. We define $\tilde{U}_\psi$ by appropriately tensoring $U_\psi$ with $I_{c-a}$ and we define $\tilde{U}_\phi$ by appropriately tensoring $U_\phi$ with $I_{c-b}$, such that $\tilde{U}_\psi$ and $\tilde{U}_\phi$ both act on $n+c$ qubits. Then, the given circuit yields a $($\alpha+\beta$, c+1, $\epsilon_$0+$\epsilon_$1)$-VE for $|$\psi\rangle$ + |$\phi\rangle$.

![[assets/figures/papers/iclr26_0005_QcRto0GjxC_Accelerating_Inference_for_Multilayer_Neural_Net/figures/005_Figure_4.jpg]]
*Figure 4: Full-rank linear-pooling output block*

## 定位与知识库关联

本文的工作直接回应了量子神经网络推理中长期存在的两个瓶颈：（1）多层非线性变换使量子态相干性被测量或断层扫描破坏；（2）缺乏跨层的范数下界保证导致电路复杂度随层数指数增长。此前的量子 CNN 加速方案（如 Kerenidis et al. 2020）需要在层间引入经典后处理或中间测量，无法保持相干叠加；Cong et al. 2019 提出的参数化量子电路虽受 CNN 启发，但并不直接加速经典架构，也未提供与输入维度相关的复杂度分析；Allcock et al. 2020 等前馈量子网络同样依赖中间读取，且未系统处理范数衰减问题。相比之下，本文通过残差结构中的跳跃连接与 Lipschitz 常数 ≤1 的激活函数缩放，首次证明了在无中间测量的前提下，可以实现具有非线性激活函数的多层神经网络的全相干量子实现（anchor: "the first coherent quantum implementations of multi-layer neural networks with non-linear activations"）。同时，作者给出了无需 QRAM 的 2D 多滤波器卷积的块编码（anchor: "novel QRAM-free block-encoding for 2D multi-filter convolutions"），在数据访问假设较弱的场景下依然能保持理论加速。表 1 的系统比较进一步突显了该方法在"相干多层""相干非线性""无 QRAM""范数保证"以及"误差依赖于 polylog(1/ε) 而非多项式倒数"等维度上的独特性。

**适用边界。** 本文的量子加速依赖于三种可伸缩的数据访问假设（Figure 1 的三个 regime）。当权重和输入均可通过 QRAM 高效访问（regime 1）时，推理代价可实现 quasi‑polylog 级别的加速；仅权重具备 QRAM 访问、输入以经典方式编码（regime 2）时，获得二次至四次加速；即使完全不假设输入的量子访问（regime 3），依然能以低于经典精确计算的成本完成推理。三种范式下的复杂度上界 $O(\mathrm{polylog}(N/\varepsilon)^k)$、$O(N \log(1/\varepsilon)^{2k})$ 等均以多项式对数因子随误差 $\varepsilon$ 和层数 $k$ 缩放，但前提是网络采用所定义的残差块与范数保持机制。若脱离残差连接，范数随层深指数衰减，量子电路深度将呈指数增长（anchor: "if the unitary circuit implementing the transformation requires even two calls to the input vector encoding, then the circuit complexity will grow exponentially with the number of non-linear activations"）。因此，方法的有效性高度绑定在残差架构与激活函数的 Lipschitz 缩放之上。

**关键局限。** 第一，多数加速结果（regime 1 和 2）依赖 QRAM 硬件，而大规模容错 QRAM 的物理可实现性仍未解决，这构成从理论到运行的重要鸿沟。第二，虽然误差对数值精度的依赖是 polylog(1/ε)，但在深度网络中，电路复杂度依赖于 $O(\mathrm{polylog}(N/\varepsilon)^{2k})$，当层数 $k$ 很大时，多项式对数的指数增长仍然不可忽视；同时，激活函数的多项式逼近误差随深度累积，可能进一步约束极深网络的可行精度。第三，当前工作专注于推理阶段，未涉及训练或梯度计算，且所有保证建立在输入为 rank‑3 张量（如图像）和特定线性‑归一化‑残差块组合之上，直接泛化至其他网络拓扑（如注意力机制）尚待验证。

**开放问题。** 作者明确给出若干延伸方向。一个核心问题是：能否在保证 polylog(1/ε) 误差依赖的前提下，实现非残差、多层非线性变换序列的全相干量子模拟而不遭遇指数级电路深度（Conclusion: "Is it possible to coherently enact sequences of non-linear transformations without an exponentially increasing circuit depth…"）。此外，文末呼吁探索该技术与量子微分方程求解器、有限差分等科学计算工具的连接，并尝试将方法适配至 UNet 风格的蒸馏扩散模型等浅层架构，以推动量子推理的实际落地。在电路实现层面，改进无 QRAM 的 2D 卷积块编码（例如利用傅里叶变换对角化或混合使用 QRAM）也是降低常数因子的重要开放问题。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Accelerating_Inference_for_Multilayer_Neural_Networks_with_Quantum_Computers.pdf

![[paperPDFs/ICLR_2026/Accelerating_Inference_for_Multilayer_Neural_Networks_with_Quantum_Computers.pdf]]
