---
title: "Saddle-to-Saddle Dynamics Explains A Simplicity Bias Across Neural Network Architectures"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Saddle_to_Saddle_Dynamics_Explains_A_Simplicity_Bias_Across_Neural_Network_Architectures.pdf
project_link: null
code_link: null
openreview_forum_id: Vit5M0G5Gb
aliases:
- SSDF
- SSDESBANNA
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "数据诱导或初始化诱导的时间尺度分离驱动网络在嵌套的不变流形上逐步增加有效宽度（单位数），从而产生递进的简洁性。"
primary_logic: "通过嵌套不动点层级的构造、不变流形的存在以及时间尺度分离，证明鞍-鞍动力学是一个通用机制：网络在低有效宽度的鞍点附近停滞，然后沿流形逃逸到更高有效宽度的鞍点，反复迭代即形成逐渐复杂的解。"
claims:
- "窄网络的不动点可嵌入更宽网络成为鞍点（嵌套不动点）。"
- "梯度流存在保持权重关系的不变流形，使得网络表现如同更窄网络。"
- "线性网络中，数据奇异值差异导致沿主导方向增长的时间尺度分离（低秩解）。"
- "二次网络中，初始化差异导致单元间增长的时间尺度分离（稀疏解）。"
---

# Saddle-to-Saddle Dynamics Explains A Simplicity Bias Across Neural Network Architectures

> [!tip] 核心洞察
> 通过嵌套不动点层级的构造、不变流形的存在以及时间尺度分离，证明鞍-鞍动力学是一个通用机制：网络在低有效宽度的鞍点附近停滞，然后沿流形逃逸到更高有效宽度的鞍点，反复迭代即形成逐渐复杂的解。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 鞍-鞍动力学解释跨神经网络架构的简洁性偏差 |
| 英文题名 | Saddle-to-Saddle Dynamics Explains A Simplicity Bias Across Neural Network Architectures |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Vit5M0G5Gb) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | Saddle-to-Saddle Dynamics Framework |
| Dataset | 多种两层架构（线性全连接、线性卷积、ReLU全连接、ReLU卷积、线性自注意力、二次网络）, MNIST 二分类（两层全连接线性/ReLU） |

> [!tip] 效果简介
> - 多种两层架构（线性全连接、线性卷积、ReLU全连接、ReLU卷积、线性自注意力、二次网络） 上，训练损失和权重动力学（平台期与突降模式） 为 梯度下降表现出清晰的鞍-鞍动力学，有效宽度从1逐步增长到2，与不动点构造类别(5)-(7)匹配。，对比 此前无统一理论预测该动力学模式。，变化 定性一致：所有架构均观察到平台期-突降，且中间鞍点对应单单位可表达的解。。
> - MNIST 二分类（两层全连接线性/ReLU） 上，训练损失和第一层权重矩阵奇异值增长 为 第一、第二奇异值依次增长，对应两次突降，反映有效宽度从1到2的增加；第三个奇异值接近零。，对比 无理论明确指出奇异值增长与平台期边界的对应。，变化 定性符合：奇异值跃升时刻与损失突降时刻一致。。

## 概要

已有理论观察到神经网络在训练中倾向于先学习简单解、再逐步学习复杂解，即“简洁性偏差”（simplicity bias），但缺乏一个跨架构的统一框架来解释梯度下降为何以及何时会表现出这种递进的学习行为。本文提出**鞍-鞍动力学（Saddle-to-Saddle Dynamics）**作为通用机制，统一解释了全连接、卷积、自注意力等多种架构中简洁性偏差的产生。

核心发现是：窄网络的不动点可嵌入到更宽网络中形成鞍点（嵌套不动点，Theorem 1），而梯度流存在保持特定权重关系的不变流形（Theorem 3），使得宽网络在流形上表现为有效宽度更小的窄网络。学习过程中，网络先被吸引到低有效宽度的不变流形附近，接近对应鞍点后停滞（平台期），随后因时间尺度分离逃逸到更高有效宽度的不变流形，形成突降。这一过程的反复迭代即构成从简单到复杂解的递进学习（Figure 1A）。

时间尺度分离的驱动来源因激活函数而异：
- **线性网络**中，数据输入-输出相关矩阵的奇异值差异导致沿主导方向增长的时间尺度分离，产生低秩解（Theorem 4）；
- **二次或更高次激活网络**中，初始化差异导致单元间“富者更富”的时间尺度分离，产生稀疏解（Proposition 5）。

实验在六种两层架构（线性全连接、线性卷积、ReLU全连接、ReLU卷积、线性自注意力、二次网络）上均观察到清晰的平台期-突降模式，中间鞍点对应单单元可表达的解（Figure 1B-G）。在MNIST二分类任务上，两层全连接网络的权重奇异值增长时刻与损失突降时刻一致，进一步验证了有效宽度递增的鞍-鞍迭代（Figure 3）。消融实验表明，网络宽度、数据奇异值分布、初始化结构与尺度均按理论预期影响平台期长度（Figure 2），跳跃连接则通过减少需逃逸的层数加速动力学（Figure 6）。

该框架的理论适用范围覆盖通用层定义（Equation 1）下的多种架构，方法定位为统一现有架构特定理论（如Fukumizu & Amari的ReLU不动点层级、Saxe et al.的线性鞍点动力学），并将简洁性偏差从经验观察提升为具有明确因果机制的动力学理论。



神经网络训练中普遍存在一种现象：模型倾向于先学习简单解，随后在训练过程中逐步学习更复杂的解。这一“简洁性偏差”（simplicity bias）在不同架构中表现为不同的具体形式——线性网络学习递增秩的解，ReLU网络学习递增拐点数的解，卷积网络学习递增卷积核数的解，自注意力网络学习递增头数的解。尽管这些现象在各自架构中被分别观察到，但**已有理论缺乏一个跨架构的统一框架**来解释：梯度下降为何、以及在何时会逐步学习复杂性递增的解。

现有工作的主要缺口体现在三个层面。**第一，理论适用范围狭窄。** Fukumizu & Amari (2000) 最早在两层全连接网络中发现了不动点层级，但其分析未拓展到卷积和注意力架构。Saxe et al. (2014) 分析了深度线性网络的鞍点动力学，但结论局限于线性网络，无法解释ReLU、自注意力等非线性架构中的类似现象。**第二，流形结构缺失。** 先前工作仅知道不动点层级的存在，但不清楚这些不动点之间是否以及如何连接，缺乏对梯度流路径的完整刻画。**第三，时间尺度分离的根源未系统区分。** 不同架构中观察到的“平台期-突降”模式（plateau and abrupt drop）缺乏统一的因果解释——数据分布与初始化各自扮演什么角色，在何种条件下驱动简洁性偏差，尚无明确答案。

本文的核心动机是**建立一个跨架构的鞍-鞍动力学（saddle-to-saddle dynamics）框架**，统一解释上述现象。该框架的核心洞见是：通过嵌套不动点层级的构造、不变流形的存在以及时间尺度分离，鞍-鞍动力学是一个通用机制——网络在低有效宽度的鞍点附近停滞，然后沿不变流形逃逸到更高有效宽度的鞍点，反复迭代即形成逐渐复杂的解。这一机制将线性网络的低秩解、ReLU网络的稀疏解、卷积网络的核数增长和自注意力网络的头数增长统一为同一动力学范式的不同表现。



## 核心方法与创新机理

本文的核心贡献是提出了一个**跨架构统一的鞍-鞍动力学框架**，将此前在不同神经网络架构中分散观察到的“简洁性偏差”现象纳入同一理论解释。该框架的核心创新可从三个维度理解。

### 统一的理论适用范围

此前关于梯度下降简洁性偏差的理论工作严重受限于特定架构：Saxe et al. (2014) 的鞍点动力学分析仅适用于深度线性网络，Fukumizu & Amari (2000) 的不动点层级发现局限于两层全连接网络，而ReLU网络、卷积网络、自注意力网络中的平台期-突降现象虽有大量经验观察，却缺乏统一的理论解释。

本文通过一个通用层定义将全连接、卷积和自注意力架构纳入同一框架：

$$f(\pmb{x}; \pmb{\theta}_{1:H}) = g_{\mathrm{out}}\left(\sum_{i=1}^{H} \phi(g_{\mathrm{in}}(\pmb{x}); \pmb{u}_i) \pmb{v}_i\right)$$

其中 $\phi$ 可以是线性、ReLU、卷积或自注意力单元。基于此定义，**Theorem 1** 通过四种构造方式（依激活函数属性分别适用）将窄网络的不动点嵌入到更宽网络中，形成嵌套的不动点层级。这四种构造涵盖：(i) 任意激活函数的权重拆分；(ii) 存在零映射输入时的零单元添加；(iii) 一次齐次激活函数的权重缩放；(iv) 线性激活函数的矩阵分解。**Theorem 3** 进一步证明了当权重满足等权重、等比例或线性相关等关系时，该关系在梯度流下保持不变，使得网络行为等价于有效宽度更小的网络。这些定理共同构成了跨架构的分析基础，填补了从架构特定理论到统一框架的关键空白。

### 不变流形连接不动点

此前工作仅知晓不动点层级的存在，但未揭示这些不动点之间如何连接，也无法解释梯度下降为何以及何时会从一个不动点转移到另一个。本文的核心突破在于建立了**不变流形**作为不动点之间的连接路径。

**Theorem 3** 证明了四类不变流形在梯度流下的保持性：(i) 两单元权重相等；(ii) 一单元权重为零；(iii) 两单元权重成比例且激活函数为一次齐次；(iv) 两单元权重线性相关且激活函数为线性。在这些流形上，网络的有效宽度减少，表现如同更窄的网络。鞍-鞍动力学的迭代过程由此得以形式化：网络在低有效宽度的不变流形附近演化，接近该流形上的鞍点（即窄网络的不动点），随后沿流形逃逸到有效宽度更大的不变流形，反复迭代形成逐渐复杂的解。Figure 1A 以卡通损失景观展示了这一过程：青色曲线代表1单元可表达映射的不变流形，黄色曲线代表2单元可表达映射的不变流形，梯度流在两者之间交替切换。

### 时间尺度分离的二元机制

本文明确区分了驱动鞍-鞍动力学的两种时间尺度分离来源，这是此前工作未系统解决的问题。

**数据诱导的时间尺度分离**适用于线性网络。**Theorem 4** 证明，当输入-输出相关矩阵 $\Sigma_{yz}$ 的奇异值存在差异时，权重沿主导奇异方向增长的速度远快于其余方向：当权重在前 $r$ 个奇异向量上的投影达到 $O(1)$ 时，在剩余子空间上的投影仅为 $O(\varepsilon^{1-s_{r+1}/s_1})$。这导致网络首先学习低秩解，随后逐步增加秩，对应有效宽度的递增。

**初始化诱导的时间尺度分离**适用于二次或更高次激活网络。**Proposition 5** 证明，在小高斯初始化下，二次网络的早期动力学近似为 $\dot{v}_i = u_i^{\top}\Sigma_{yZ} u_i$，$\dot{u}_i = 2 v_i \Sigma_{yZ} u_i$，展现出“富者更富”效应：一个单元的权重因初始化优势率先增长至 $O(1)$，而其余单元保持在 $O(\varepsilon)$。这导致网络首先学习稀疏解（仅一个有效单元），随后其他单元依次增长。

这两种机制的区分解释了为何线性网络学习递增秩的解（低秩偏差），而二次/ReLU网络学习递增单元数的解（稀疏偏差）——简洁性偏差的具体表现形式取决于时间尺度分离的来源。



![[assets/figures/papers/iclr26_0010_Vit5M0G5Gb_Saddle-to-Saddle_Dynamics_Explains_A_Simplicity/figures/014_Figure_1.jpg]]
*Figure 1: Saddle-to-saddle dynamics occurs in the gradient descent training of a wide range of architectures and leads to a dynamical simplicity bias. (A) Saddle-to-saddle dynamics on a cartoon loss landscape. The cyan and yellow curves represent invariant manifolds, on which the network implements input-output maps expressible by the architecture with one and two units, respectively. In general, saddle-to-saddle dynamics operates by repeating: i) during the plateau, escaping from a saddle associated with a width-h network onto an invariant manifold with effective width (h + 1); ii) during the rapid transition phase, approaching a fixed point on that manifold, which is a saddle associated with a widt...*

### 核心瓶颈：简洁性偏差缺乏跨架构统一理论

已有研究在不同架构中分别观察到梯度下降会逐步学习更复杂的解——线性网络学习递增秩的解，ReLU网络学习递增拐点数目的解，卷积网络学习递增卷积核数目的解，自注意力网络学习递增头数的解。然而，这些现象此前缺乏一个统一的动力学框架来解释**为何**以及**何时**梯度下降会表现出这种递进的简洁性偏差。Fukumizu & Amari (2000) 虽在两层全连接网络中发现了不动点层级，但未拓展到卷积和注意力架构；Saxe et al. (2014) 的鞍点动力学分析局限于线性网络；各架构分离的经验观察则停留在现象描述层面，缺乏对简洁性度量（有效单元数）的统一定义。

### 核心机制：鞍-鞍动力学

本文提出的鞍-鞍动力学框架将上述现象统一为以下因果链条：

1. **嵌套不动点层级**：窄网络的不动点可通过四种构造嵌入到更宽网络中成为鞍点（Theorem 1），形成有效宽度递增的不动点层级。
2. **不变流形连接**：当权重满足特定关系（等权重、等比例、线性相关等）时，该关系在梯度流下保持不变，使网络行为等价于有效宽度更小的网络（Theorem 3）。这些不变流形将不同有效宽度的不动点连接起来，提供鞍-鞍逃逸路径。
3. **时间尺度分离驱动迭代**：根据网络类型，分离来源分为两类——
   - **数据诱导分离**（线性网络）：输入-输出相关矩阵的奇异值差异导致权重沿主导奇异方向优先增长，产生低秩解（Theorem 4）。
   - **初始化诱导分离**（二次/高次网络）：一个单元因初始化优势率先增长，抑制其他单元，产生稀疏解（Proposition 5）。
4. **鞍-鞍迭代**：梯度流先沿有效宽度较小的不变流形接近一个鞍点（平台期），随后沿流形逃逸到有效宽度更大的不变流形（突降），重复此过程形成从简单到复杂的递进学习。

### Pipeline 模块关系

框架由五个理论模块构成，它们之间的逻辑依赖关系如下：

| 模块 | 功能 | 依赖关系 |
|------|------|---------|
| 嵌套不动点 (Theorem 1) | 构造有效宽度递增的不动点层级 | 基础构件，被不变流形模块引用 |
| 不变流形 (Theorem 3) | 建立连接不动点的低维子流形 | 依赖嵌套不动点提供流形上的鞍点 |
| 数据诱导时间尺度分离 (Theorem 4) | 解释线性网络中低秩解的产生 | 与不变流形结合，解释为何先访问低有效宽度流形 |
| 初始化诱导时间尺度分离 (Proposition 5) | 解释二次网络中稀疏解的产生 | 与不变流形结合，解释单元间的“富者更富”效应 |
| 鞍-鞍迭代 | 综合上述模块，描述完整的递进学习过程 | 依赖前四个模块提供流形结构和分离机制 |

### 输入输出流

**输入**：
- 网络架构（通过通用层定义 $f(\pmb{x}; \pmb{\theta}_{1:H}) = g_{\mathrm{out}}\left(\sum_{i=1}^{H} \phi(g_{\mathrm{in}}(\pmb{x}); \pmb{u}_i) \pmb{v}_i\right)$ 统一描述）
- 训练数据（决定 $\Sigma_{yz}$ 的奇异值结构）
- 初始化条件（尺度、结构、是否靠近不变流形）

**内部状态转移**：
- 梯度流 $\dot{\pmb\theta} = - \frac{\partial \mathcal{L}}{\partial \pmb\theta}$ 驱动权重演化
- 有效宽度从 1 逐步增长到 $H$，每次增长对应一次鞍-鞍迭代

**输出**：
- 递增复杂度的解序列：线性网络输出递增秩的解，ReLU网络输出递增拐点数的解，卷积网络输出递增核数的解，自注意力网络输出递增头数的解

### 理论适用范围与边界

框架覆盖的架构包括：全连接（线性/ReLU/二次/sigmoid/tanh/正弦）、卷积（线性/ReLU）、自注意力（线性/softmax），以及深层网络和带跳跃连接的网络。不动点构造的四种情形（Theorem 1 的 i-iv）覆盖了不同激活函数的性质——情形 (i) 适用于任意 $\phi$，情形 (ii) 适用于存在零映射的 $\phi$（如ReLU），情形 (iii) 适用于一次齐次 $\phi$（如线性），情形 (iv) 适用于对 $\pmb{u}$ 线性的 $\phi$（如线性自注意力）。

**已知局限**：
- 不动点和不变流形是否穷尽所有可能的结构尚未证明；特定数据可能引入额外的数据依赖不动点或流形
- 理论主要适用于线性或二次激活函数，更高阶多项式激活仅有推测性陈述
- 分析基于梯度流和极小初始化，实际离散梯度下降、大学习率下动力学可能有偏差
- 深层网络的鞍-鞍动力学虽在实验中观察到（Figure 5），但完全理论化仍然复杂
- 未在其他任务范式（如强化学习、自监督学习）上验证该通用机制



### 通用层定义与梯度流

本文的理论框架建立在一个通用的单层网络定义之上。令输入为 $\pmb{x}$，网络包含 $H$ 个单元，每个单元由参数对 $(\pmb{u}_i, \pmb{v}_i)$ 参数化，其输出为：

$$f(\pmb{x}; \pmb{\theta}_{1:H}) = g_{\mathrm{out}}\left(\sum_{i=1}^{H} \phi(g_{\mathrm{in}}(\pmb{x}); \pmb{u}_i) \pmb{v}_i\right)$$

其中 $\phi$ 为激活函数，$g_{\mathrm{in}}$ 和 $g_{\mathrm{out}}$ 分别为输入和输出变换。通过选择不同的 $\phi$、$g_{\mathrm{in}}$ 和 $g_{\mathrm{out}}$，该定义可覆盖全连接层、卷积层和自注意力层等架构（Equation (1)）。

训练采用梯度流，即无穷小学习率下梯度下降的连续极限：

$$\dot{\pmb\theta} = -\frac{\partial \mathcal{L}}{\partial \pmb\theta}$$

其中 $\mathcal{L}$ 为损失函数（Equation (3)）。

### 模块一：嵌套不动点构造

**核心机制**：将窄网络（$H-1$ 个单元）的不动点嵌入到宽网络（$H$ 个单元）中，形成嵌套的鞍点层级。Theorem 1 给出了四种构造方式，取决于激活函数 $\phi$ 的性质：

**(i) 通用构造**（对任意 $\phi$ 有效）：
$$u_H = u_i^*, \quad v_H = \gamma_v v_i^*, \quad v_i = (1-\gamma_v) v_i^*$$
其中 $\gamma_v \in \mathbb{R}$。该构造通过拆分已有单元来创建新单元，保持网络输出不变（Equation (4)）。

**(ii) 零激活构造**：若存在 $u_{\mathrm{zero}}$ 使得对所有输入 $z$ 有 $\phi(z; u_{\mathrm{zero}}) = 0$，则可将新单元参数设为此值，其余单元保持不变。

**(iii) 一次齐次构造**：若 $\phi(z; u)$ 对 $u$ 是一次齐次的，则可通过缩放已有单元并添加互补单元来构造。

**(iv) 线性构造**：若 $\phi(z; u)$ 对 $u$ 是线性的，则构造退化为权重矩阵的秩保持扩展。

**证据强度**：Theorem 1 和 Corollary 2 提供了严格的数学证明（置信度 0.95）。实验表明，梯度下降中访问的中间鞍点恰好落入这些构造类别：Figure 1(B,C) 对应 Equation (7)，Figure 1(D,E) 对应 Equation (6)，Figure 1(E,F) 对应 Equation (5)。

### 模块二：不变流形

**核心机制**：当网络权重满足特定关系（如对称、等比例或线性相关）时，该关系在梯度流下保持不变，且网络的有效宽度（实际起作用的单元数）减少。Theorem 3 给出了四种不变流形条件：

**(i) 等权重流形**：$\theta_i = \theta_j$，两单元权重相等时梯度流保持相等，有效宽度减 1。

**(ii) 等比例流形**：$v_i / v_j = \text{常数}$ 且 $u_i = u_j$，适用于 ReLU 等一次齐次激活。

**(iii) 零激活流形**：某些单元的 $u_i = u_{\mathrm{zero}}$ 使得 $\phi(\cdot; u_i) = 0$，这些单元不参与计算。

**(iv) 线性相关流形**：在线性激活下，权重矩阵的秩受限，网络等价于更窄的线性网络。

**证据强度**：Theorem 3 提供了梯度流下不变性的严格证明（置信度 0.95）。不变流形连接了嵌套不动点，为鞍-鞍迭代提供了路径：网络在低有效宽度的流形上接近鞍点，然后沿流形逃逸到更高有效宽度的流形。

### 模块三：数据驱动的时间尺度分离

**核心机制**：在线性网络中，输入-输出相关矩阵 $\Sigma_{yz}$ 的奇异值差异导致权重沿主导方向优先增长，产生低秩解。

小初始化下，线性网络的早期动力学近似为（Equation (10)）：

$$\dot{v_i} = \Sigma_{yz} u_i, \quad \dot{u_i} = \Sigma_{yz}^{\top} v_i$$

Theorem 4 表明：当权重在前 $r$ 个主导奇异向量上的投影达到 $O(1)$ 时，其余子空间上的投影仅为 $O(\varepsilon^{1-s_{r+1}/s_1})$，其中 $s_k$ 为第 $k$ 个奇异值。奇异值差异越大（幂律指数 $\kappa$ 越大），时间尺度分离越显著。

**证据强度**：Theorem 4 提供了严格的数学刻画（置信度 0.95）。Figure 2B 验证了减小 $\kappa$ 会缩短平台期；Figure 3 在 MNIST 上展示了奇异值增长与损失突降的对应关系。

### 模块四：初始化驱动的时间尺度分离

**核心机制**：在二次或更高次激活网络中，初始化差异导致单元间出现“富者更富”效应，一个单元率先增长而其他单元保持极小，产生稀疏解。

二次网络在小子化下的早期动力学近似为（Equation (14)）：

$$\dot{v_i} = u_i^{\top}\Sigma_{yZ} u_i, \quad \dot{u_i} = 2 v_i \Sigma_{yZ} u_i$$

其简化形式 $\dot{v}_i = v_i^2$ 的解为 $v_i(t) = (1/v_i(0) - t)^{-1}$，表明初始值稍大的单元会在有限时间内发散，而其他单元相对停滞。

Proposition 5 证明：当一个单元的权重达到 $O(1)$ 时，其余单元几乎必然保持 $O(\varepsilon)$。

**证据强度**：Proposition 5 提供了概率意义上的证明（置信度 0.95）。Figure 2C 和 2D 验证了初始化结构和尺度对平台期的影响。

### 模块五：鞍-鞍迭代

**综合机制**：梯度流依次在有效宽度递增的不变流形上接近鞍点，实现从简单到复杂解的递进学习：

1. 初始化后，网络受时间尺度分离驱动，靠近有效宽度为 1 的不变流形。
2. 在该流形上接近一个鞍点（对应单单元可表达的解），进入平台期。
3. 沿流形的不稳定方向逃逸，切换到有效宽度为 2 的不变流形。
4. 重复上述过程，每次迭代增加一个有效单元。

**发生条件**：(i) 从鞍点逃逸的路径紧贴有效宽度仅增加 1 的不变流形；(ii) 初始化接近某个低有效宽度的不变流形。

**证据强度**：Figure 1(B-G) 在六种架构中观察到清晰的平台期-突降模式，中间鞍点对应单单元可表达的解（置信度 0.9）。Figure 5 将观察扩展到深层网络，Figure 6 验证了跳跃连接通过减少需要逃逸零不动点的层数来加速鞍-鞍动力学（置信度 0.95）。

**局限性说明**：不动点和不变流形是否穷尽所有可能的结构尚未证明；理论主要适用于线性或二次激活函数，更高阶多项式激活仅有推测性陈述；分析基于梯度流和极小初始化，实际离散梯度下降下动力学可能有偏差。



## 实验与关键发现

### 主结果：跨架构的鞍-鞍动力学验证

论文在六种两层架构上验证了鞍-鞍动力学的普遍性（Figure 1）：线性全连接、线性卷积、ReLU全连接、ReLU卷积、线性自注意力、二次网络。所有架构均表现出清晰的平台期-突降模式：梯度下降首先在有效宽度为1的鞍点附近停滞，然后沿不变流形逃逸到有效宽度为2的解。中间平台期对应的不动点可归入定理1的三个构造类别——线性网络对应式(7)（单单元解），ReLU网络对应式(6)（零单元构造），二次网络对应式(5)（拆分构造）。这一跨架构的一致性表明，鞍-鞍动力学不依赖于特定激活函数或连接模式，而是由嵌套不动点层级和不变流形结构所保证的通用机制。

在MNIST二分类任务上（Figure 3），两层全连接线性网络和ReLU网络均展现出两次损失突降，分别对应第一和第二奇异值的跃升。训练过程中，第一奇异值率先增长至平台期，随后第二奇异值开始增长，第三次及以后的奇异值始终接近零。奇异值增长的时间节点与损失突降时刻精确吻合，验证了定理4所描述的数据驱动时间尺度分离：输入-输出相关矩阵的奇异值差异导致权重沿主导方向依次增长，形成递进的低秩解。

![[assets/figures/papers/iclr26_0010_Vit5M0G5Gb_Saddle-to-Saddle_Dynamics_Explains_A_Simplicity/figures/023_Figure_3.jpg]]
*Figure 3: Saddle-to-saddle dynamics in two-layer fully-connected linear and ReLU networks trained for binary classification of MNIST digits. The input dimension is 2 8 $\times$ 2 8 = 7 8 4 , the hidden layer width is 1000, and the target outputs are two-dimensional one-hot vectors. The intermediate plateau is longer when the two digits are harder to distinguish. For example, digits 3/5 are harder to distinguish than digits 0/1. The colored curves represent the top three singular values of the firstlayer weight matrix, $\breve { U } \in \mathbb { R } ^ { 1 0 0 0 \times 7 8 4 }$ Consistent with our theory, the growth of the first and second singular values coincides with the first and second abrupt drops i...

### 消融实验：宽度、数据分布与初始化的影响

**网络宽度的影响**（Figure 2A）：增加线性全连接网络的宽度 $H$ 对损失曲线几乎无影响，平台期长度保持稳定；但增加线性自注意力的头数 $H$ 会显著缩短平台期。这一差异源于自注意力中每个头对应独立的不变流形结构，头数增加等价于在更窄的有效宽度流形上提供了更多候选鞍点。

![[assets/figures/papers/iclr26_0010_Vit5M0G5Gb_Saddle-to-Saddle_Dynamics_Explains_A_Simplicity/figures/022_Figure_2.jpg]]
*Figure 2: The effect of network width, data distribution, and initialization on learning dynamics. Singular values of $\Sigma _ { y z }$ (linear network) or positive singular values of $\Sigma _ { y Z }$ (linear self-attention) follow a power law, $s _ { n } = n ^ { - \kappa }$ , n = 1 , 2 , 3 , and are normalized such that $\textstyle \sum _ { n = 1 } ^ { 3 } s _ { n }$ = 1 . (A) Increasing the number of units H has little effect on the loss curves of linear networks, but shortens the plateaus in linear self-attention. $\kappa$ = 1 for both models. (B) Decreasing the power law exponent κ shortens the plateaus in both linear networks and linear self-attention. Setting $\kappa$ = 0 eliminates plateaus in linear n...

**数据分布的影响**（Figure 2B）：减小数据奇异值的幂律指数 $\kappa$ 会缩短两类网络中的平台期。当 $\kappa=0$（所有奇异值相等）时，线性网络的平台期完全消失，因为定理4中的时间尺度分离不再成立；而线性自注意力的平台期虽缩短但依然存在，说明其动力学还受初始化诱导的单元间分离影响。

**初始化结构与尺度的影响**（Figure 2C-D）：小尺度各向同性初始化和大尺度低秩初始化均能产生鞍-鞍动力学。低秩初始化将网络置于有效宽度较小的不变流形附近，使首次下降呈指数形式，随后进入平台期和S形突降。增大各向同性初始化尺度会缩短平台期，因为较大的初始权重削弱了时间尺度分离效应。

**跳跃连接的影响**（Figure 6）：在深层全连接网络中引入跳跃连接可加速鞍-鞍动力学。跳过层数越多，学习越快——因为跳跃连接减少了需要从零不动点逃逸的层数，使网络更快地进入更高有效宽度的流形。

![[assets/figures/papers/iclr26_0010_Vit5M0G5Gb_Saddle-to-Saddle_Dynamics_Explains_A_Simplicity/figures/027_Figure_6.jpg]]
*Figure 6: Saddle-to-saddle dynamics in deep fully-connected networks with skip connections. (A) Schematic of three four-layer fully-connected networks: one with no skip connection, one with a skip connection that skips one layer, and one with a skip connection that skips two layers. The three linear networks are defined in Equation (18). (B,C) Loss curves of linear and ReLU networks with skip connections, plotted using linear time (top row) and logarithmic time (bottom row) axes. All networks exhibit saddle-to-saddle dynamics, with the network that skips more layers learning faster. With small initialization, shallower linear networks learn faster (Saxe et al., 2019). In the network without a skip co...*

### 深层网络与扩展激活函数的验证

鞍-鞍动力学在深层网络中同样成立（Figure 5）。三层线性全连接、三层卷积线性、三层ReLU全连接、卷积ReLU、一层线性Transformer以及二次+线性混合网络均表现出平台期-突降模式。第一层权重的可视化显示，中间平台期对应单单元可表达的解，最终收敛到两单元解。

![[assets/figures/papers/iclr26_0010_Vit5M0G5Gb_Saddle-to-Saddle_Dynamics_Explains_A_Simplicity/figures/026_Figure_5.jpg]]
*Figure 5: Learning dynamics in deep networks. Each panel shows the loss over training time (top), and the first-layer weights right after the first abrupt loss drop (bottom left) and at the end of learning (bottom right). The first-layer weights to each hidden unit are two-dimensional and plotted as black dots. The training sets in panels A,C,E are the same as those in Figure 1(B,D,F). The training sets in panels B,D,F split the scalar output in Figure 1(C,E,G) into a two-dimensional vector output. (A) Three-layer linear fully-connected network. (B) The network has a convolutional linear layer as the first hidden layer and a fully-connected linear layer as the second hidden layer. (C) Three-layer ReL...*

此外，该动力学在更广泛的激活函数下依然存在（Figure 4），包括softmax自注意力、sigmoid、正弦、tanh和三次函数。这表明定理1和定理3的构造条件具有相当的普适性——只要激活函数满足可分性条件（如零输出点、一次齐次性或线性），嵌套不动点和不变流形便可建立。

### 失败模式与局限性

理论预测在以下情况下鞍-鞍动力学可能减弱或消失：（1）数据奇异值差异过小（$\kappa \approx 0$），导致方向间时间尺度分离不足；（2）初始化尺度过大，使早期动力学近似不再成立；（3）网络宽度过大且各单元初始化差异不足，导致单元间分离难以建立。这些预测在消融实验中得到了定性验证。

需要注意的是，实验验证主要限于合成数据和MNIST二分类，尚未在更大规模数据集或更复杂任务（如强化学习、自监督学习）上检验该机制的鲁棒性。此外，Table 1中不同数字对的奇异值差异较大（第二平台期奇异值从1.38到5.21），暗示数据依赖的不动点或流形可能影响平台期持续时间，但这一点尚未得到系统研究。

![[assets/figures/papers/iclr26_0010_Vit5M0G5Gb_Saddle-to-Saddle_Dynamics_Explains_A_Simplicity/figures/024_Table_1.jpg]]
*Table 1: Singular values of MNIST binary classification data*



## 定位与知识库关联

### 与前驱工作的关系

鞍-鞍动力学框架并非凭空产生，而是对三条独立研究线索的系统性统一。

**不动点层级的发现。** Fukumizu & Amari (2000) 最早在两层全连接网络中发现了不动点的嵌套结构：窄网络的不动点可嵌入宽网络成为鞍点。本文的 Theorem 1 将这一构造从全连接线性/ReLU 网络推广到由通用层定义 $f(\pmb{x}; \pmb{\theta}_{1:H}) = g_{\mathrm{out}}\left(\sum_{i=1}^{H} \phi(g_{\mathrm{in}}(\pmb{x}); \pmb{u}_i) \pmb{v}_i\right)$ 涵盖的卷积、自注意力等架构，并给出四种构造（constructions i-iv），依激活函数 $\phi$ 的性质（任意、存在零输出输入、一次齐次、对参数线性）分别适用。此前工作未触及这一跨架构广度。

**鞍点动力学的分析。** Saxe et al. (2014) 在深度线性网络中分析了鞍点附近的平台期与突降现象，揭示了数据奇异值差异导致的时间尺度分离。本文的 Theorem 4 在线性网络中将此机制精确化为：当权重在前 $r$ 个奇异向量上的投影达到 $O(1)$ 时，其余子空间上的投影仅为 $O(\varepsilon^{1-s_{r+1}/s_1})$。但 Saxe et al. 的分析局限于线性网络，未提出跨架构的通用机制。

**分离的经验观察。** 不同架构中分别观察到的平台期-突降模式（线性网络的低秩增长、ReLU 网络的拐点增加、卷积网络的核数增长、自注意力的头数增长）此前被视作各自独立的经验现象，缺乏统一的简洁性度量和动力学解释。

### 理论贡献的增量

相较于前驱工作，本文的核心增量体现在三个维度：

1. **统一框架的建立。** 通过通用层定义和 Theorem 1 的四种构造，将不动点层级从架构特定推广到架构无关。Theorem 3 进一步证明，当权重满足等权重、等比例或线性相关等关系时，梯度流保持该关系不变，使网络在不变流形上表现为有效宽度更小的网络。这为不同架构中的平台期提供了统一的几何解释：网络在低有效宽度的不变流形上接近鞍点，然后沿流形逃逸到更高有效宽度的不变流形。

2. **时间尺度分离的双源机制。** 明确区分了两种产生分离的因果路径：数据诱导（线性网络，Theorem 4）依赖输入-输出相关矩阵的奇异值差异，导致低秩解；初始化诱导（二次/高次网络，Proposition 5）依赖单元间初始权重的微小差异被“富者更富”动力学放大，导致稀疏解。此前工作未系统区分这两种机制的作用条件和表现形式。

3. **鞍-鞍迭代的完整链条。** 将嵌套不动点（Theorem 1）、不变流形（Theorem 3）和时间尺度分离（Theorem 4 / Proposition 5）串联为可预测的动力学序列：梯度流依次在有效宽度递增的不变流形上接近鞍点，反复迭代形成从简单到复杂解的递进学习。这一链条在六种两层架构（Figure 1）和多种深层架构（Figure 5）中得到了定性一致的实验验证。

### 适用边界与局限

**已验证的适用范围。** 理论在以下架构中获得了实验支持：两层线性全连接、线性卷积、ReLU 全连接、ReLU 卷积、线性自注意力、二次网络（Figure 1B-G）；三层线性/ReLU 全连接和卷积网络、一层线性 Transformer、二次+线性混合网络（Figure 5）；以及 softmax 自注意力、sigmoid、正弦、tanh、三次网络等激活函数（Figure 4）。MNIST 二分类实验（Figure 3）表明该动力学在真实数据上也成立。

**已知局限。** 以下几点需要使用者注意：

- **完备性未证明。** 不动点和不变流形是否穷尽所有可能的结构尚未证明；特定数据集可能引入超出数据无关构件的额外不动点或流形。这意味着在某些数据分布下，网络可能访问理论未预测的鞍点。
- **激活函数的限制。** 时间尺度分离的严格证明主要适用于线性（Theorem 4）和二次（Proposition 5）激活。对于更高阶多项式激活，Proposition 5 的推广仅有推测性陈述，尚未严格证明。
- **连续极限与实际训练的差距。** 分析基于梯度流（无穷小学习率）和极小初始化。实际离散梯度下降、大学习率和较大初始化下，动力学可能偏离理论预测。Figure 2D 显示增大各向同性初始化尺度会缩短平台期，暗示理论预测在初始化较大时需要修正。
- **深层网络的完整理论化。** 虽然实验观察到深层网络中的鞍-鞍动力学（Figure 5），且跳跃连接通过减少需要逃逸零不动点的层数来加速学习（Figure 6），但深层情况的完全理论化仍然复杂，尚未完成。
- **任务范式的局限。** 所有验证均在监督学习的分类或回归任务上进行。该机制是否适用于强化学习、自监督学习、预测编码等范式，仍是开放问题。

### 开放问题

1. **完备性条件。** 在什么条件下，Theorem 1 和 Theorem 3 所描述的不动点和不变流形构成完备集？是否存在数据依赖的额外结构？
2. **高次激活的严格分析。** 对于 $p>2$ 的齐次多项式激活，时间尺度分离是否确实存在且更强？Proposition 5 的推广需要更严格的证明。
3. **动力学路径的马尔可夫性。** 梯度下降访问的鞍点序列是否具有马尔可夫性？初始点离不变流形多近才能保证网络在接近不动点后才离开？
4. **架构扩展。** 该理论能否扩展到循环神经网络、图神经网络、以及更复杂的注意力变体（如交叉注意力、稀疏注意力）？
5. **优化器的影响。** 动量、自适应学习率等优化器如何改变鞍-鞍动力学的平台期长度和逃逸路径？



## 原文 PDF

![[paperPDFs/ICLR_2026/Saddle_to_Saddle_Dynamics_Explains_A_Simplicity_Bias_Across_Neural_Network_Architectures.pdf]]
