---
title: "A Brain-Inspired Gating Mechanism Unlocks Robust Computation in Spiking Neural Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Brain_Inspired_Gating_Mechanism_Unlocks_Robust_Computation_in_Spiking_Neural_Networks.pdf
project_link: null
code_link: null
aliases:
- DGND
- BIGMURCSNN
- "Dynamic Gated Neuron (DGN)"
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/neuroscience_cognitive_science
core_operator: "引入动态电导因子C_i，使膜电导随输入活动自适应变化，形成生物启发的门控机制。"
primary_logic: "动态电导机制在功能上等价于LSTM的遗忘门，通过自适应泄漏缩放和突触噪声补偿实现双重噪声抑制，为SNN提供了理论保证的鲁棒性。"
claims:
- "DGN在TIDIGITS上达到99.10%的top-1准确率，超越所有基线模型。"
- "在加性噪声下，DGN前馈网络在TIDIGITS上保持95.34%准确率，比LIF高48.51%。"
- "在SHD上PGD攻击下，循环DGN比循环LIF高35.54%。"
- "DGN的稳态电压方差理论公式表明其具有自适应泄漏缩放和噪声补偿双重机制。"
---

# A Brain-Inspired Gating Mechanism Unlocks Robust Computation in Spiking Neural Networks

> [!tip] 核心洞察
> 动态电导机制在功能上等价于LSTM的遗忘门，通过自适应泄漏缩放和突触噪声补偿实现双重噪声抑制，为SNN提供了理论保证的鲁棒性。

| 字段 | 内容 |
| ------- | --------------------------------------------------------------------------------------------------------------------- |
| 中文题名 | 脑启发门控机制解锁脉冲神经网络的鲁棒计算 |
| 英文题名 | A Brain-Inspired Gating Mechanism Unlocks Robust Computation in Spiking Neural Networks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5h741EyfQM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/neuroscience_cognitive_science |
| Method | Dynamic Gated Neuron (DGN) |
| Dataset | TIDIGITS, SHD, SSC, Ti46Alpha |

> [!tip] 效果简介
> - TIDIGITS 上，Top-1 Accuracy (%) 为 99.10，对比 LIF: 97.83，变化 +1.27。
> - SHD 上，Top-1 Accuracy (%) 为 88.98，对比 LIF: 83.82，变化 +5.16。
> - SSC 上，Top-1 Accuracy (%) 为 75.63，对比 LIF: 72.43，变化 +3.20。

## 概要

本文针对脉冲神经网络（SNN）在噪声环境下部署的核心瓶颈——传统LIF神经元模型因固定泄漏电导机制导致的鲁棒性不足——提出了一种脑启发式动态门控神经元模型（Dynamic Gated Neuron, DGN）。该模型的核心创新在于引入了动态电导因子 $C_i$，使膜电导随输入活动自适应变化，从而在功能上等价于LSTM的遗忘门，实现了自适应泄漏缩放与突触噪声补偿的双重噪声抑制机制。DGN通过双路径架构（电流注入路径 $W_i D_i$ 与动态电导路径 $C_i D_i$）将生物物理机制与计算效率统一。

在实验结果方面，DGN在多个基准数据集上取得了领先性能：在TIDIGITS上达到99.10%的top-1准确率（超越LIF基线1.27%），在SHD上达到88.98%（超越LIF基线5.16%），在SSC和Ti46Alpha上分别达到75.63%和96.31%。在鲁棒性方面，DGN展现出显著优势：在TIDIGITS加性噪声下，前馈网络保持95.34%的准确率，比LIF高出48.51%；在SHD上PGD攻击下，循环DGN比循环LIF高出35.54%。同时，DGN的能量消耗（3.03 nJ）远低于LSTM（604.7 nJ），接近LIF（1.02 nJ），保持了SNN的低能耗优势。理论分析通过稳态电压方差公式（Eq. 13）揭示了DGN鲁棒性的数学根源，验证了其双重噪声抑制机制的有效性。



脉冲神经网络（SNN）因其生物合理性和低功耗潜力被视为下一代神经形态计算的核心范式。然而，传统SNN的神经元模型——尤其是广泛使用的漏积分放电（LIF）模型——存在一个根本性瓶颈：其膜电导（泄漏率）是固定不变的。这种静态设计使得LIF神经元在面对输入噪声和时间变异性时缺乏自适应调节能力，导致在噪声环境下的鲁棒性严重不足，成为SNN从实验室走向实际部署的关键障碍。

现有改进方案试图通过引入异质性（HeterLIF）、自适应阈值（ALIF）或门控机制（GLIF）来缓解这一问题，但这些方法均未从神经元动力学的最底层——电导——入手。LSTM等人工门控网络虽然通过遗忘门和输入门实现了强大的时序鲁棒性，但其高能耗（每步约604.7 nJ）与SNN的能效优势背道而驰。

本文的核心动机在于：能否在保留SNN低功耗特性的前提下，通过生物启发的动态电导机制赋予神经元类似LSTM的自适应门控能力？作者提出的动态门控神经元（DGN）正是这一思路的产物。DGN通过引入可学习的动态电导因子C_i，使膜电导随输入活动自适应变化，在功能上等价于LSTM的遗忘门（Figure 2展示了二者的拓扑同源性）。这一设计同时实现了两个协同的噪声抑制机制：自适应泄漏缩放（通过分母项G_0）和突触噪声补偿（通过分子中的补偿项），为SNN提供了理论保证的鲁棒性。



## 核心方法与创新机理

DGN（Dynamic Gated Neuron）的核心创新在于将生物神经元中的**动态电导机制**引入脉冲神经网络，从根本上改变了传统LIF神经元固定泄漏电导的建模方式。这一改进直接针对SNN在噪声环境下鲁棒性不足的瓶颈——传统LIF模型因膜电导固定，对输入噪声和时间变异性缺乏自适应调节能力，导致实际部署时性能急剧下降。

**关键变更插槽**体现在三个层面：

1. **膜电导从固定值变为动态变量**：传统LIF使用固定泄漏电导 $g_l$，而DGN引入可学习的动态电导因子 $C_i$，使总电导变为 $g_l + \sum C_i D_i$，随突触输入活动自适应变化（Eq. 4）。这是整个机制的根本性改变。

2. **膜电位衰减率从静态变为输入依赖**：LIF的衰减率 $\rho_m = e^{-g_l \Delta t}$ 是常数，DGN则计算自适应衰减率 $\rho^t = \varphi(1 - g_l \cdot \Delta t - \Delta t \sum C_i D_i^t)$（Eq. 6），其中 $\varphi$ 为数值截断函数。这意味着模型可以根据当前输入动态调节信息保留程度——输入强时衰减加快（快速遗忘旧信息），输入弱时衰减减慢（保留更多历史信息）。

3. **突触电流处理从线性叠加变为双路径架构**：传统模型仅通过电流注入路径 $W_i D_i$ 影响膜电位，DGN额外增加电导路径 $C_i D_i$，形成“电流-电导”双通道调控架构。这一设计在功能上等价于LSTM的遗忘门和输入门协同工作（Figure 2），但完全基于生物可解释的神经动力学。

**因果机制**的核心洞察在于：动态电导机制在功能上等价于LSTM的遗忘门，但通过**自适应泄漏缩放**和**突触噪声补偿**双重机制实现噪声抑制。稳态方差理论分析（Eq. 13）揭示了这一点——DGN的膜电位方差公式中包含补偿项 $W_i - \frac{C_i \sum W_j \mu_j}{G_0}$，其中 $C_i$ 项可以抵消输入噪声的贡献，而分母 $G_0$ 实现了输入依赖的泄漏缩放。相比之下，LIF的方差公式（Eq. 14）仅包含静态泄漏 $g_l$，缺乏任何自适应调节能力。

**实验证据的强度**：DGN在TIDIGITS上达到99.10%的top-1准确率，超越所有基线（Table 1）。在加性噪声下，DGN前馈网络保持95.34%准确率，比LIF高48.51%（Table 2）。在SHD上PGD攻击下，循环DGN比循环LIF高35.54%（Table 2）。这些改进并非来自网络规模或训练技巧的差异——实验严格控制了架构、超参数和评估协议的一致性（Table 5），DGN（128-128）参数仅131.1K，与LIF的128.0K相近（Table 3）。

**简化版本s-DGN**（共享平衡电位）在SHD上达到84.30%准确率，参数更少但仍优于LIF，说明动态电导机制本身是性能提升的主要来源，而非参数增加带来的容量优势。DGN的能量消耗（3.03 nJ）远低于LSTM（604.7 nJ），接近LIF（1.02 nJ）（Table 8），表明门控机制的引入并未显著牺牲SNN的核心优势。



DGN（Dynamic Gated Neuron）的整体pipeline围绕一个核心架构展开：将传统LIF神经元中固定的泄漏电导替换为**动态电导门控机制**。整个系统由四个紧密耦合的模块组成，形成从突触输入到脉冲输出的完整计算流。

**模块关系与数据流：**

1. **突触电流衰减模块**：接收来自前层或外部输入的脉冲信号 $z_i^t$，通过指数衰减动力学 $D_i^t = e^{-\Delta t/\tau_s} D_i^{t-1} + z_i^t$（Eq. 5）生成突触电流变量 $D_i^t$。这个模块的输出同时馈入后续两个并行路径。

2. **动态门控模块**：利用突触电流 $D_i^t$ 和可学习参数 $C_i$ 计算自适应衰减率 $\rho^t = \varphi(1 - g_l \cdot \Delta t - \Delta t \sum_i C_i D_i^t)$（Eq. 6），其中 $\varphi$ 是数值截断函数（如Sigmoid）。这是整个架构的**因果控制旋钮**——它使膜电导随输入活动自适应变化，在功能上等价于LSTM的遗忘门。

3. **膜电位更新模块**：将自适应衰减率 $\rho^t$ 应用于上一时刻膜电位 $V^{t-1}$，同时叠加来自权重路径的电流注入 $\Delta t \sum_i W_i D_i^t$，并执行软重置 $-\vartheta z^{t-1}$（Eq. 7）。这里的关键设计是**双路径架构**：$W_i D_i^t$ 路径负责电流注入（类似LSTM的输入门），而 $C_i D_i^t$ 路径负责动态电导调制（类似遗忘门）。

4. **脉冲发放模块**：通过Heaviside阶跃函数 $z^t = \Theta(V^t - \vartheta)$（Eq. 8）判断是否发放脉冲，输出到下一层或读出层。

**输入输出流：** 外部脉冲序列 $\{z_i^t\}$ 进入突触电流模块 → 并行生成电流注入信号和门控信号 → 动态门控模块调节膜电位衰减率 → 膜电位更新模块整合所有信号 → 脉冲发放模块输出二进制脉冲序列。循环架构中，输出脉冲 $z^{t-1}$ 会反馈回突触电流模块（作为 $D_{i,\text{rec}}^t = e^{-\Delta t/\tau_s} D_{i,\text{rec}}^{t-1} + z^{t-1}$）。

**与LSTM的结构同源性：** 如图2所示，DGN的 $\rho^t$ 对应LSTM遗忘门 $\breve{f}^t$，$W_i D_i^t$ 路径对应输入门，软重置对应细胞状态更新中的遗忘操作。这种拓扑同源性解释了DGN为何能继承LSTM的鲁棒时序处理能力，同时保持SNN的低能耗特性（DGN: 3.03 nJ vs LSTM: 604.7 nJ）。

**训练方式：** 采用BPTT（Backpropagation Through Time）沿时间和空间维度展开计算图（图5），梯度通过Eq. 7反向传播。损失函数对可学习参数 $W_i$ 和 $C_i$ 的梯度分别由 $dE/dW_i = \sum_t dE/dz^t \cdot dz^t/dW_i$ 和 $dE/dC_i = \sum_t dE/dz^t \cdot dz^t/dC_i$ 计算。



### 3.1 动态门控神经元（DGN）模型

传统LIF神经元模型的瓶颈在于其固定的泄漏电导 $g_l$，导致膜电位的衰减率恒定，无法根据输入活动的变化动态调整。这直接限制了SNN在噪声环境下的鲁棒性。DGN的核心因果旋钮是引入**动态电导因子** $C_i$，构建双路径调控架构（电流注入路径 $W_i D_i$ + 动态电导路径 $C_i D_i$），使膜电导随输入突触电流自适应变化，形成生物启发的门控机制。

**连续时间动力学：**

DGN的膜电位动力学从电导基神经元模型出发（Eq. 1），但将突触电导 $g_i$ 替换为可学习的动态变量 $D_i$。其连续时间形式为：

$$
\frac{dV}{dt} = -(g_l + \sum_i^N C_i D_i) V + \sum_i^N W_i D_i \quad \text{(Eq. 4)}
$$

其中：
- $g_l$：固定的泄漏电导。
- $C_i$：第 $i$ 个突触的可学习动态电导因子（门控权重）。
- $D_i$：第 $i$ 个突触的突触电流变量，其动力学为指数衰减（Eq. 3）：
  
$$
\tau_s \frac{dD_i}{dt} = -D_i + z_i^t \quad \text{(Eq. 3)}
$$

  其中 $z_i^t$ 是突触前脉冲输入，$\tau_s$ 是突触时间常数。
- $W_i$：第 $i$ 个突触的权重（电流注入路径）。

**离散更新方程：**

为便于数字计算和BPTT训练，DGN采用前向欧拉法离散化。四个核心模块的离散更新如下：

1. **突触电流衰减模块**（Eq. 5）：
   
$$
D_i^t = e^{-\frac{\Delta t}{\tau_s}} D_i^{t-1} + z_i^t
$$

   其中 $e^{-\Delta t/\tau_s}$ 是突触电流的固定衰减率（记为 $\rho_s$）。

2. **动态门控模块**（Eq. 6）：
   
$$
\rho^t = \varphi(1 - g_l \cdot \Delta t - \Delta t \sum_i^N C_i D_i^t)
$$

   这是DGN的核心创新。$\rho^t$ 是**自适应膜电位衰减率**，它不再是LIF中的固定值 $e^{-g_l \Delta t}$，而是通过动态电导项 $\Delta t \sum_i C_i D_i^t$ 随输入活动实时调整。$\varphi$ 是数值截断函数（如Sigmoid或ReLU的变体），确保衰减率在有效范围内。

3. **膜电位更新模块**（Eq. 7）：
   
$$
V^t = \rho^t \cdot V^{t-1} + \Delta t \sum_i^N W_i D_i^t - \vartheta z^{t-1}
$$

   其中 $\vartheta$ 是脉冲发放阈值，最后一项是软重置（发放脉冲后减去阈值）。

4. **脉冲发放模块**（Eq. 8）：
   
$$
z^t = \Theta(V^t - \vartheta)
$$

   $\Theta(\cdot)$ 是Heaviside阶跃函数。

**与LSTM的结构同源性：**

DGN的门控机制与LSTM的遗忘门在功能上拓扑同构（Figure 2）。自适应衰减率 $\rho^t$ 数学上模拟了LSTM遗忘门 $f^t$ 的记忆过滤功能：当输入活动强（$D_i^t$ 大）时，$\rho^t$ 减小，膜电位快速泄漏，相当于“忘记”旧信息；当输入弱时，$\rho^t$ 接近1，膜电位保持，相当于“记住”状态。同时，软重置项 $-\vartheta z^{t-1}$ 与LSTM的输入门更新在数学上一致。

### 3.2 稳态方差理论：鲁棒性的双重机制

为解释DGN的鲁棒性优势，论文推导了稳态膜电位方差的封闭形式。通过将突触输入建模为确定性均值加高斯白噪声（$\hat{I}_i(t) = \mu_i + \sigma_i \xi(t)$），并对Eq. 4进行线性化（截断高阶项），得到线性随机微分方程（SDE）：

$$
\frac{dV}{dt} = -G_0 V + \sum W_i \mu_i + \sum \sigma_i (W_i - C_i V_{\text{steady}}) \xi(t)
$$

其中 $G_0 = g_l + \sum_i C_i \mu_i$ 是有效总电导，$V_{\text{steady}} = \frac{\sum W_i \mu_i}{G_0}$ 是确定性稳态膜电位。

求解该SDE的稳态方差，得到DGN的方差公式（Eq. 13）：

$$
\langle V^2 \rangle_{\mathrm{DGN}} = \frac{\left[ \sum_{i=1}^N \sigma_i \left( W_i - \frac{C_i \sum_{j=1}^N W_j \mu_j}{G_0} \right) \right]^2}{2 G_0}
$$

作为对比，LIF的稳态方差为（Eq. 14）：

$$
\langle V^2 \rangle_{\mathrm{LIF}} = \frac{(\sum_{i=1}^N W_i \sigma_i)^2}{2 g_l}
$$

**双重噪声抑制机制：**

1. **自适应泄漏缩放**（分母 $G_0$）：DGN的有效电导 $G_0 = g_l + \sum C_i \mu_i$ 大于LIF的固定电导 $g_l$。更大的分母直接降低了方差幅度，相当于根据输入强度动态增强泄漏，抑制噪声积累。

2. **突触噪声补偿**（分子中的 $-\frac{C_i \sum W_j \mu_j}{G_0}$ 项）：该补偿项从突触权重 $W_i$ 中减去一个与 $C_i$ 成正比的量。当 $C_i$ 被学习为与 $W_i$ 同号时，分子中的有效噪声系数 $|W_i - \frac{C_i \sum W_j \mu_j}{G_0}|$ 会小于 $|W_i|$，从而进一步降低方差。这等价于LSTM中遗忘门和输入门协同抑制噪声的功能。

**变量含义总结：**

| 变量 | 含义 | 可学习？ |
|------|------|----------|
| $V$ | 膜电位 | 否 |
| $D_i$ | 突触电流变量 | 否（状态变量） |
| $z_i$ | 脉冲输出 | 否 |
| $g_l$ | 固定泄漏电导 | 否（超参数） |
| $C_i$ | 动态电导因子（门控权重） | **是** |
| $W_i$ | 突触权重（电流路径） | **是** |
| $\tau_s$ | 突触时间常数 | 否（超参数） |
| $\vartheta$ | 脉冲发放阈值 | 否（超参数） |
| $\rho^t$ | 自适应膜电位衰减率 | 否（由 $C_i, D_i$ 计算） |
| $G_0$ | 有效总电导（$g_l + \sum C_i \mu_i$） | 否（由 $C_i$ 和输入均值决定） |

### 3.3 训练：基于时间的反向传播（BPTT）

DGN使用BPTT进行训练。损失函数 $E$ 对可学习权重 $W_i$ 和 $C_i$ 的梯度沿时间维度展开（Figure 5）：

$$
\frac{dE}{dW_i} = \sum_{t=1}^T \frac{\partial E}{\partial z^t} \frac{dz^t}{dW_i}, \quad \frac{dE}{dC_i} = \sum_{t=1}^T \frac{\partial E}{\partial z^t} \frac{dz^t}{dC_i}
$$

其中脉冲梯度 $\frac{dz^t}{dW_i}$ 和 $\frac{dz^t}{dC_i}$ 通过替代梯度法（surrogate gradient）近似，因为Heaviside阶跃函数不可导。梯度沿时间反向传播时，需要累积Eq. 7中 $\rho^t$ 和 $V^{t-1}$ 的递归依赖关系。



## 实验与关键发现

### 核心性能对比

DGN在四个音频/神经形态时间序列基准上全面超越现有SNN基线（Table 1）。在TIDIGITS上，循环DGN（128-128隐藏层）达到**99.10%** top-1准确率，超越LIF的97.83%（+1.27%）。在SHD上，DGN达到88.98%，比LIF的83.82%高出5.16%。在SSC和Ti46Alpha上，DGN分别达到75.63%和96.31%，对应提升为+3.20%和+2.89%。DVS-Gesture（Table 10）上，DGN在干净样本上达到95.14%，比LIF的93.06%高2.08%。所有基线使用公开代码复现，架构与超参数保持一致。


![[assets/figures/papers/iclr26_0002_5h741EyfQM_A_Brain-Inspired_Gating_Mechanism_Unlocks_Robust/figures/004_Table_1.jpg]]
*Table 1: Comparison of model performance on Ti46Alpha, TIDIGITS, SHD, and SSC datasets. Rec=N/Y represents feedforward networks (N) and recurrent networks (Y), respectively. * indicates results we reproduced using public code, while bold entries indicate the best performance*

关键瓶颈：传统LIF的固定泄漏电导无法根据输入活动动态调节，导致对噪声和时间变异性的鲁棒性不足。DGN通过引入动态电导因子C_i，使膜电导自适应变化，等价于LSTM遗忘门的生物门控机制，从而在功能上实现双重噪声抑制——自适应泄漏缩放与突触噪声补偿。

### 鲁棒性分析

**噪声与对抗攻击**（Table 2, Figure 4, Figure 6-8）：DGN在加性噪声下，前馈网络在TIDIGITS上保持**95.34%**准确率，比LIF高48.51%（绝对值）。在SHD上，PGD攻击下循环DGN比循环LIF高35.54%。整体鲁棒性（Table 3-4）：DGN前馈在SHD上为61.54±1.95%，显著优于LIF的42.07±2.13%；循环DGN在TIDIGITS上达到91.67±3.62%，前馈为88.56±5.64%。Figure 4/6-8显示，随着扰动概率p或攻击强度ε增加，DGN的准确率下降最平缓，在所有扰动类型（加性、减性、混合、FGSM、PGD、BIM）上保持最高绝对性能。



![[assets/figures/papers/iclr26_0002_5h741EyfQM_A_Brain-Inspired_Gating_Mechanism_Unlocks_Robust/figures/008_Table_4.jpg]]

![[assets/figures/papers/iclr26_0002_5h741EyfQM_A_Brain-Inspired_Gating_Mechanism_Unlocks_Robust/figures/010_Table_4.jpg]]
*Table 4: Overall Robustness on the SHD dataset from Tab.2*

![[assets/figures/papers/iclr26_0002_5h741EyfQM_A_Brain-Inspired_Gating_Mechanism_Unlocks_Robust/figures/006_Table_2.jpg]]
*Table 2: Accuracy (%) of the proposed DGN under different noise conditions and adversarial attacks on TIDIGITS and SHD. Bold entries indicate the best performance. HeterLIF denotes the heterogeneous LIF model proposed by Perez-Nieves et al. (2021)*

![[assets/figures/papers/iclr26_0002_5h741EyfQM_A_Brain-Inspired_Gating_Mechanism_Unlocks_Robust/figures/007_Table_3.jpg]]
*Table 3: Performance comparison of different neuronal models on the SHD dataset. We report the parameter count (in K), clean accuracy (%), and overall robustness (%). Highlighted rows correspond to our proposed models, s-DGN and DGN, which consistently achieve superior accuracy and robustness while demonstrating the impact of parameter reduction*

因果机制：稳态电压方差理论公式（Eq. 13）揭示了DGN的双重机制——分母G_0实现输入依赖的泄漏缩放，分子中包含噪声补偿项，使方差在噪声条件下被主动抑制。LIF的固定泄漏（Eq. 14）只能被动衰减噪声，无法动态适应输入变化。

### 消融与变体分析

简化版s-DGN（共享平衡电位E）在SHD前馈上达到84.30%准确率（Table 3），参数更少但性能仍优于LIF的83.82%。完整DGN在SHD前馈上达到85.18%，循环达到87.78%。参数数量：DGN（128-128）为131.1K，与LIF的128.0K相近（Table 3），说明鲁棒性提升主要源于机制设计而非参数增加。

### 能量效率

DGN每步能耗（3.03 nJ）远低于LSTM（604.7 nJ），接近LIF（1.02 nJ）（Table 8）。理论分析（Table 7）显示DGN的运算复杂度与LIF同阶，主要额外开销来自动态电导计算。训练/推理时间（Table 9）显示DGN在SHD上单epoch训练时间约为LIF的2倍，但远低于LSTM（约5倍）。

### 失败模式与局限

1. **脉冲发放率升高**：DGN的脉冲发放率（[7.07%, 1.19%]）高于LIF（[4.43%, 0.54%]），可能增加能耗，但远低于LSTM的连续激活。
2. **理论假设边界**：稳态方差推导基于线性噪声近似，强非线性（如高脉冲率、饱和电导）下的行为需进一步验证。
3. **任务覆盖**：实验集中在音频和神经形态数据集，在图像分类等静态任务上的表现尚未系统评估。
4. **硬件部署**：动态电导机制在神经形态芯片上的高效实现方案尚待探索。

**需要人工验证的点**：DGN在TIDIGITS上加性噪声下比LIF高48.51%这一极端数值，虽然置信度标注为0.95，但建议核对原始Table 2中LIF在该条件下的具体数值，确认是否存在基线复现差异。

### 补充图表

![[assets/figures/papers/iclr26_0002_5h741EyfQM_A_Brain-Inspired_Gating_Mechanism_Unlocks_Robust/figures/012_Table_5.jpg]]
*Table 5: Network parameters for different datasets*




## 定位与知识库关联

### 与 baseline/follow-up 的关系

DGN 的核心创新在于将传统 LIF 神经元的固定泄漏电导 $g_l$ 替换为动态电导 $g_l + \sum C_i D_i$，使膜电导随输入活动自适应变化。这一改动在功能上等价于 LSTM 的遗忘门：自适应衰减率 $\rho^t = \varphi(1 - g_l \cdot \Delta t - \Delta t \sum C_i D_i^t)$ 实现了输入依赖的泄漏缩放，而突触电流 $D_i$ 的指数衰减则提供了噪声补偿项（见稳态方差公式 Eq. 13 中的 $C_i \sum W_j \mu_j / G_0$ 项）。论文通过图 2 明确展示了这种拓扑同源性。

与现有 SNN 基线（LIF、HeterLIF、ALIF、GLIF）相比，DGN 在干净准确率上提升有限（TIDIGITS 上 +1.27%，SHD 上 +5.16%），但在噪声和对抗攻击下的鲁棒性增益显著（加性噪声下比 LIF 高 48.51%，PGD 攻击下比 LIF 高 35.54%）。这表明动态电导机制的主要贡献不在于提升理想条件下的性能，而在于提供理论保证的噪声抑制能力。与 LSTM 相比，DGN 在保持可比鲁棒性的同时，能耗降低约 200 倍（DGN: 3.03 nJ vs LSTM: 604.7 nJ），这是通过脉冲驱动的稀疏计算实现的。

### 适用边界

DGN 的适用场景具有明确边界：
- **强项**：时序依赖的噪声环境（如音频、神经形态传感器数据），尤其是需要同时处理加性噪声和对抗攻击的任务。
- **弱项**：静态图像分类等非时序任务尚未充分验证；在需要极低脉冲发放率的场景中，DGN 的略高发放率（[7.07%, 1.19%] vs LIF [4.43%, 0.54%]）可能成为瓶颈。

### 局限与开放问题

**已知局限**：
1. 动态电导因子 $C_i$ 增加了参数量（128-128 网络从 128.0K 增至 131.1K），但增长幅度有限。
2. 理论分析基于线性噪声近似（Eq. 13 的推导假设输入扰动为高斯白噪声），强非线性条件下的行为尚未刻画。
3. 简化版 s-DGN（共享平衡电位）虽减少参数，但在 SHD 上准确率仅 84.30%，与完整 DGN 的 88.98% 有差距。

**开放问题**：
1. 如何将 DGN 与脉冲 Transformer 等架构集成？这需要解决动态电导与注意力机制之间的交互。
2. 能否探索更丰富的电导门控模型（如多时间尺度门控、突触特异性门控）以增强时空特性？
3. DGN 在更大规模网络（如 ImageNet 级）和复杂任务（视频理解、多模态）上的表现尚未验证。
4. 神经形态硬件上的高效部署方案是什么？动态电导的实时计算可能引入额外的硬件开销。

**需人工验证的点**：论文声称 DGN 的鲁棒性优势来源于双重噪声抑制机制（自适应泄漏缩放 + 噪声补偿），但理论推导（Eq. 13）假设输入为高斯白噪声且忽略了脉冲发放的非线性。实际场景中脉冲发放的离散性可能使理论保证弱化，需要更严格的实验验证。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Brain_Inspired_Gating_Mechanism_Unlocks_Robust_Computation_in_Spiking_Neural_Networks.pdf

![[paperPDFs/ICLR_2026/A_Brain_Inspired_Gating_Mechanism_Unlocks_Robust_Computation_in_Spiking_Neural_Networks.pdf]]
