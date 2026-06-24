---
title: "ParaRNN: Unlocking Parallel Training of Nonlinear RNNs for Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ParaRNN_Unlocking_Parallel_Training_of_Nonlinear_RNNs_for_Large_Language_Models.pdf
openreview_forum_id: mX8b64iUaa
aliases:
- ParaRNN
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "将非线性RNN的逐元素前向传播重新定义为整个序列上的非线性方程组，利用牛顿法迭代线性化，再通过针对块双对角结构定制的高效并行归约（parallel reduction）算法实现全序列并行求解。"
primary_logic: "非线性序列操作可转化为方程组的数值求解；牛顿线性化后得到的系统具有特殊的块双对角结构，该结构天然适合并行前缀扫描，从而首次使得非线性RNN的训练能够像Transformer一样在序列维度上并行化。"
claims:
- "ParaRNN achieves speedups of up to 665× over naïve sequential application of RNNs."
- "Classical nonlinear RNNs (ParaGRU and ParaLSTM) can be trained at 7B parameter scale and achieve perplexity comparable to similarly-sized Transformers and Mamba2 architectures."
- "The fully-fused CUDA implementation of the Newton routine yields a 2.6× speedup for ParaGRU and a 1.5× speedup for ParaLSTM over Mamba’s SSM application at L=2^9."
- "Language Modeling (DCLM dataset, 7B parameters) 上 Perplexity = ParaGRU 9.19; ParaLSTM 9.16"
---

# ParaRNN: Unlocking Parallel Training of Nonlinear RNNs for Large Language Models

> [!tip] 核心洞察
> 非线性序列操作可转化为方程组的数值求解；牛顿线性化后得到的系统具有特殊的块双对角结构，该结构天然适合并行前缀扫描，从而首次使得非线性RNN的训练能够像Transformer一样在序列维度上并行化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ParaRNN：解锁非线性RNN的并行训练以用于大型语言模型 |
| 英文题名 | ParaRNN: Unlocking Parallel Training of Nonlinear RNNs for Large Language Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=mX8b64iUaa); [GitHub](https://github.com/apple/ml-pararnn/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | ParaRNN |
| Dataset | Language Modeling (DCLM dataset, 7B parameters), Training speed (rnn forward pass, L=2^9), Inference throughput (7B generation, L=2^11), Synthetic tasks (Cycle Navigation, Modular Arithmetic, Copy Memory, A5, etc.) |

> [!tip] 效果简介
> - Language Modeling (DCLM dataset, 7B parameters) 上，Perplexity 为 ParaGRU 9.19; ParaLSTM 9.16，对比 Mamba2 8.62; Transformer 9.55，变化 ParaLSTM outperforms Transformer by 0.39 PPL; Mamba2 remains the strongest。
> - Training speed (rnn forward pass, L=2^9) 上，Relative speedup vs. Mamba SSM application 为 ParaGRU 2.6×; ParaLSTM 1.5×，对比 Mamba 1×，变化 ParaGRU is 2.6× faster, ParaLSTM 1.5× faster。
> - Inference throughput (7B generation, L=2^11) 上，Tokens per second 为 ~37–38 (ParaGRU/ParaLSTM)，对比 Mamba ~28; Transformer much lower，变化 ParaRNN achieves ~1.3× throughput of Mamba。

## 概述

### 问题瓶颈

非线性循环神经网络（RNN）的序列递归本质构成了其训练的核心瓶颈：每个时间步的隐藏状态计算必须等待前一步的结果，导致训练过程无法在序列维度上并行展开。这一限制使得经典的非线性RNN（如GRU、LSTM）难以扩展到现代大型语言模型（LLM）的训练规模。相比之下，**Transformer**（Vaswani et al., NeurIPS 2017）凭借自注意力的全序列并行性成为主流架构，而线性状态空间模型（SSM）如**Mamba**（Gu & Dao, 2023）和**Mamba2**（Dao & Gu, 2024）虽能通过关联扫描实现训练并行化，但其线性约束在表达能力上存在天然上限——无法有效建模需要非线性隐藏状态交互的复杂序列依赖。

### 核心方法

ParaRNN 的核心洞察在于：**将非线性序列操作转化为方程组的数值求解问题**。具体而言，该方法将长度为 $L$ 的序列上逐元素应用的 RNN 递归重新定义为 $L$ 个方程组成的非线性系统，并利用牛顿法（Newton's method）进行迭代线性化。关键突破在于，线性化后得到的系统具有特殊的**块双对角结构**，该结构天然适合并行前缀扫描（parallel prefix scan），从而首次使得非线性 RNN 的训练能够像 Transformer 一样在序列维度上实现并行化。

为将这一思想落地为实用系统，ParaRNN 在三个层面进行了协同设计：

- **Jacobian 结构约束**：将 GRU/LSTM 的状态矩阵和窥视孔矩阵强制取对角形式，使 Jacobian 简化为对角阵（ParaGRU）或 $2\times2$ 块对角阵（ParaLSTM），将每对状态间的操作复杂度从 $O(d_h^2)$ 降至 $O(d_h)$。
- **双层求解器架构**：外层牛顿迭代负责非线性系统的全局线性化，内层并行归约（parallel reduction）负责高效求解块双对角线性系统。
- **三级实现栈**：从纯 PyTorch 参考实现到 CUDA 加速的并行归约，再到全融合 CUDA 内核——后者将牛顿迭代、Jacobian 组装和归约操作融合在单个 GPU 内核中，消除中间全局内存访问开销。

### 主要结果

ParaRNN 在效率、规模和表达能力三个维度上取得了突破性验证：

- **训练加速**：全融合 CUDA 实现下，ParaGRU 和 ParaLSTM 的前向传播分别达到 Mamba SSM 应用的 **2.6 倍和 1.5 倍**加速（序列长度 $L=2^9$）；相较于朴素串行 RNN 应用，加速比最高可达 **665 倍**。
- **规模化能力**：经典非线性 RNN 首次成功训练至 **7B 参数**规模，在语言建模任务上取得与同等规模 Transformer 和 Mamba2 架构可比的困惑度——ParaLSTM（9.16）甚至优于 Transformer（9.55），尽管 Mamba2（8.62）仍保持最强。
- **表达能力验证**：在需要非线性记忆的合成任务（如 Copy Memory）上，ParaGRU/ParaLSTM 达到 100% 准确率，而 Mamba2 在某些任务上失败，证实了非线性隐藏状态交互的表达优势。
- **推理吞吐**：在 7B 规模、$L=2^{11}$ 的生成场景下，ParaRNN 达到约 37-38 tokens/s，约为 Mamba 的 **1.3 倍**。

### 方法定位

在方法谱系中，ParaRNN 占据了独特位置：它既不同于 Transformer 的完全并行注意力机制，也不同于 Mamba 等线性 SSM 的关联扫描路径，而是开辟了“**非线性递归的数值并行化**”这一新范式。其本质是通过牛顿法将非线性序列操作解耦为可并行求解的线性系统，从而在保留 RNN 非线性表达能力的同时，获得与 Transformer 同级的训练并行度。该方法被封装为高可用的 PyTorch+CUDA 库，用户仅需提供 RNN 单元的递归步定义即可自动获得序列并行训练能力。

## 背景与动机

### 序列建模的并行化困境

现代大型语言模型的成功在很大程度上依赖于训练效率的持续提升。以 **Transformer**（Vaswani et al., NeurIPS 2017）为代表的自注意力架构之所以能够扩展到数万亿参数规模，其核心优势在于序列维度上的完全并行化——序列中所有位置的计算可以同时进行，充分利用了GPU的大规模并行能力。然而，这种并行化的代价是自注意力机制的平方级计算复杂度 $O(L^2)$，在长序列场景下成为严重的效率瓶颈。

循环神经网络（RNN）提供了一条理论上更具吸引力的路径：其计算复杂度仅为 $O(L)$，且推理时仅需维护固定大小的隐藏状态，天然适合自回归生成。但经典的RNN变体——如GRU和LSTM——面临一个根本性的结构约束：**非线性RNN的序列递归本质限制了训练并行度**。标准的RNN训练必须按时间步顺序展开，每一步的隐藏状态计算严格依赖前一步的结果：

$$\pmb { h } _ { l } = \pmb { f } ( \pmb { h } _ { l - 1 } , \pmb { x } _ { l } ) , \qquad \forall l = 1 , \ldots , L$$

这种逐元素的前向传播方式使得RNN无法像Transformer一样在序列维度上并行化，训练效率低下，难以扩展到现代大型语言模型的训练规模。

### 线性状态空间模型的折中方案

近年来，以 **Mamba**（Gu & Dao, 2023）和 **Mamba2**（Dao & Gu, 2024）为代表的线性状态空间模型（SSM）提供了一种折中方案。这些模型通过将递归关系约束为线性形式，使得序列计算可以通过结合性扫描（associative scan）算法实现并行化，从而在保持 $O(L)$ 复杂度的同时获得了可观的训练效率。然而，这种方案存在一个关键的表达能力瓶颈：**线性状态空间模型虽能并行但表达能力受限于线性约束，无法建模复杂的非线性序列依赖**。在某些需要非线性记忆交互的任务上（如复制记忆、复杂算术推理），Mamba2可能完全失效。

### ParaRNN的核心动机

ParaRNN的核心动机正是打破这一僵局：**能否让非线性RNN也获得与Transformer相当的训练并行度，从而同时兼得二者的优势**？这一问题的关键在于如何将序列递归关系转化为可并行求解的形式。ParaRNN的解决方案是将非线性RNN的逐元素前向传播重新定义为整个序列上的非线性方程组，利用牛顿法迭代线性化，再通过针对块双对角结构定制的高效并行归约（parallel reduction）算法实现全序列并行求解。这一思路使得非线性RNN的训练首次能够在序列维度上并行化，为经典RNN架构在大规模语言建模中的复兴开辟了道路。

## 核心创新

### 瓶颈与因果调节变量

非线性RNN（如经典GRU、LSTM）的训练长期受困于一个根本性矛盾：其序列递归本质要求逐时间步串行计算，无法在序列维度上并行化，这使其无法扩展到现代大型语言模型的训练规模。与此同时，以 **Mamba**（Gu & Dao, 2023）和 **Mamba2**（Dao & Gu, 2024）为代表的线性状态空间模型（SSM）虽然通过关联扫描实现了训练并行化，但其线性约束从根本上限制了模型对复杂非线性序列依赖的建模能力。

ParaRNN的核心因果调节变量在于**将问题从“序列操作”转变为“方程组求解”**：将RNN在整个序列上的逐元素前向传播重新定义为$L$个方程组成的非线性系统，利用牛顿法迭代线性化，再通过针对块双对角结构定制的并行归约算法实现全序列并行求解。这一转变使非线性RNN首次获得了与Transformer和Mamba同等的序列维度并行训练能力。

### 关键方法创新

**创新一：从序列递归到非线性方程组的并行求解**

标准RNN的序列应用$h_l = f(h_{l-1}, x_l)$被重新表述为：

$$\begin{cases} h_1 - f(\mathbf{0}, x_1) = \mathbf{0} \\ h_2 - f(h_1, x_2) = \mathbf{0} \\ \vdots \\ h_L - f(h_{L-1}, x_L) = \mathbf{0} \end{cases}$$

牛顿法在第$k$步需要求解的线性化系统具有天然的块双对角结构：

$$\begin{bmatrix} I & & & \\ -J_f|_{h_1^k} & I & & \\ & \ddots & \ddots & \\ & & -J_f|_{h_{L-1}^k} & I \end{bmatrix} \begin{bmatrix} \delta h_1^k \\ \delta h_2^k \\ \vdots \\ \delta h_L^k \end{bmatrix} = \begin{bmatrix} f(\mathbf{0}, x_1) - h_1^k \\ f(h_1^k, x_2) - h_2^k \\ \vdots \\ f(h_{L-1}^k, x_L) - h_L^k \end{bmatrix}$$

这一结构天然适合并行前缀扫描（parallel prefix scan），使得原本必须串行执行的$L$步递归可以在$\mathcal{O}(\log L)$并行步内完成。

**创新二：对角Jacobian约束使并行归约高效可行**

直接对标准GRU/LSTM应用上述并行求解面临关键障碍：Jacobian矩阵$J_f \in \mathbb{R}^{d_h \times d_h}$的存储和乘法开销为$\mathcal{O}(d_h^2)$，使并行扫描的计算和内存成本过高。ParaRNN的解决方案是将状态矩阵和窥视孔矩阵强制约束为对角形式：

$$A_* = \operatorname{diag}(a_*), \quad C_* = \operatorname{diag}(c_*), \quad a_*, c_* \in \mathbb{R}^{d_h}$$

这使得ParaGRU的Jacobian退化为纯对角矩阵，ParaLSTM的Jacobian退化为$2 \times 2$块对角矩阵，每对元素的乘法复杂度从$\mathcal{O}(d_h^2)$降至$\mathcal{O}(d_h)$，且可在隐藏状态维度上完全并行化。这一简化本质上将一个$d_h$维RNN细胞分解为$d_h$个独立的一维细胞，丧失了隐藏状态内部的交叉信息混合能力，但换来了训练并行化的可行性。

**创新三：三级硬件感知的CUDA实现体系**

ParaRNN提供了三种递进的并行求解器实现，允许用户在易用性与性能间权衡：

1. **纯PyTorch参考实现**：利用自动微分计算Jacobian，适合快速原型验证新RNN细胞。
2. **CUDA加速并行归约**：在GPU的线程、warp、block和device四级层次上采用混合策略——最细粒度使用前向替换，粗粒度使用并行归约，实现硬件感知的高效求解。
3. **全融合CUDA内核**：将牛顿迭代、Jacobian组装和并行归约全部融合在单个CUDA内核中，消除中间结果的全局内存读写，这是实现超越Mamba性能的关键。

实验表明，全融合实现使得ParaGRU在序列长度$L=2^9$时达到Mamba SSM应用速度的约2.6倍，ParaLSTM达到约1.5倍（Figure 2右）。牛顿法在ParaGRU和ParaLSTM上均在3次迭代内稳定收敛，且该性质在训练全程保持（Figure 4），验证了该方法在实践中的可行性。

### 与基线方法的本质差异

| 维度 | 标准RNN训练 | Mamba/Mamba2 | ParaRNN |
|------|------------|-------------|---------|
| 序列混合器并行策略 | 串行展开RNN细胞 | 关联扫描求解线性SSM | 牛顿法+并行归约求解非线性方程组 |
| Jacobian结构 | 稠密矩阵，$\mathcal{O}(d_h^2)$开销 | 标量或对角状态矩阵 | 对角（GRU）或$2\times2$块对角（LSTM），$\mathcal{O}(d_h)$开销 |
| GPU实现 | 无优化并行求解器 | 硬件感知的关联扫描 | 三级实现体系，全融合内核消除中间内存开销 |
| 表达能力 | 非线性，但无法并行训练 | 线性约束，无法建模复杂非线性依赖 | 非线性，且首次实现序列维度并行训练 |

反向传播同样受益于这一框架：损失对隐藏状态的梯度$\nabla_{h_{l-1}}\mathcal{L} = J_f|_{h_{l-1}}^\top \nabla_{h_l}\mathcal{L} + \partial_{h_{l-1}}\mathcal{L}$天然具有线性递归结构，无需牛顿迭代，可直接通过单次并行归约求解，进一步提升了端到端训练效率。

**需要手动验证的点**：关于ParaRNN框架能否泛化到任意新设计的RNN细胞，目前仅验证了ParaGRU和ParaLSTM两种实例。牛顿法快速收敛（$\mathcal{O}(1)$迭代）是维持效率优势的前提，但无法保证所有新RNN都满足此性质。此外，对角Jacobian约束对模型表达能力的实际影响虽在合成任务和语言建模实验中有所体现，但缺乏严格的理论分析。

## 整体框架

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mX8b64iUaa/figures/001_Figure_1.jpg]]
*Figure 1: Our ParaRNN framework makes it possible to apply classical RNNs in parallel, dramatically speeding up their training, and allowing them to be used competitively for language modeling*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mX8b64iUaa/figures/006_Figure_4.jpg]]
*Figure 4: Newton’s method convergence behavior for ParaGRU (top) and ParaLSTM (bottom) cells with different input sequence lengths L, for freshly initialized RNN cells (left), and for the RNN cells in the last layer of our trained 400M models (right). Inputs are randomly selected from the evaluation datasets, and the residuals reported are the max on batches of size 8*

ParaRNN 的核心思想是将非线性 RNN 在序列上的逐元素递归应用，重新表述为一个全局非线性方程组的求解问题，从而打破传统 RNN 训练中固有的序列依赖瓶颈。该框架包含三个关键层次：

**1. 问题重定义：从递归到方程组**

给定长度为 $L$ 的输入序列 $\{x_1, \ldots, x_L\}$ 和 RNN 单元的非线性状态更新函数 $f$，标准的前向传播按时间步串行执行：

$$h_l = f(h_{l-1}, x_l), \quad \forall l = 1, \ldots, L$$

ParaRNN 将这一过程等价地转化为 $L$ 个方程构成的非线性系统：

$$\begin{cases}
h_1 - f(\mathbf{0}, x_1) = \mathbf{0} \\
h_2 - f(h_1, x_2) = \mathbf{0} \\
\vdots \\
h_L - f(h_{L-1}, x_L) = \mathbf{0}
\end{cases}$$

**2. 外层求解器：牛顿迭代法**

上述非线性系统通过牛顿法迭代求解。在第 $k$ 步，系统被线性化，得到一个块双对角（block bi-diagonal）结构的线性方程组：

$$\begin{bmatrix}
I & & & \\
-J_f|_{h_1^k} & I & & \\
& \ddots & \ddots & \\
& & -J_f|_{h_{L-1}^k} & I
\end{bmatrix}
\begin{bmatrix}
\delta h_1^k \\ \delta h_2^k \\ \vdots \\ \delta h_L^k
\end{bmatrix}
= \begin{bmatrix}
f(\mathbf{0}, x_1) - h_1^k \\
f(h_1^k, x_2) - h_2^k \\
\vdots \\
f(h_{L-1}^k, x_L) - h_L^k
\end{bmatrix}$$

其中 $J_f|_{h_l^k}$ 是 $f$ 在当前位置对隐藏状态的 Jacobian 矩阵。实验表明，ParaGRU 和 ParaLSTM 在训练全过程中仅需 3 次牛顿迭代即可稳定收敛（见 Figure 4）。

**3. 内层求解器：并行归约（Parallel Reduction）**

牛顿步产生的块双对角线性系统天然适合并行前缀扫描（parallel prefix scan）。ParaRNN 利用矩阵乘法的结合律，通过并行归约算法在 $O(\log L)$ 步内求解该系统。为使这一过程在 GPU 上高效执行，ParaRNN 对 Jacobian 结构施加约束：

- **ParaGRU**：强制状态矩阵 $A_* = \operatorname{diag}(a_*)$ 为对角阵，Jacobian 退化为纯对角矩阵。
- **ParaLSTM**：状态矩阵与窥视孔（peephole）矩阵 $C_* = \operatorname{diag}(c_*)$ 均对角化，Jacobian 退化为 $2\times 2$ 块对角矩阵。

这一约束将 Jacobian 的存储和乘法复杂度从 $O(d_h^2)$ 降至 $O(d_h)$，使得并行归约在 GPU 上切实可行。代价是 $d_h$ 维 RNN 细胞实质上被分解为 $d_h$ 个独立的一维细胞，丧失了隐藏状态内部的交叉混合能力。

**4. 反向传播**

反向传播通过 RNN 单元的梯度计算本身是线性操作：

$$\nabla_{h_{l-1}} \mathcal{L} = J_f|_{h_{l-1}}^\top \nabla_{h_l} \mathcal{L} + \partial_{h_{l-1}} \mathcal{L}, \quad \forall l = L, \ldots, 1$$

因此无需牛顿迭代，可直接通过单次并行归约完成梯度求解。

**5. 三级实现架构**

ParaRNN 提供三种实现，在易用性与性能之间提供灵活选择：

1. **纯 PyTorch 实现**：基于 PyTorch 原生操作，易于理解和修改，适合原型验证。
2. **CUDA 加速并行归约**：将并行归约操作（Algorithm 1b）用 CUDA 实现，采用硬件感知的混合算法——在线程（thread）、线程束（warp）、块（block）和设备（device）四个层级上结合前向替换与并行归约。
3. **全融合 CUDA 核**：将整个牛顿例程（包括 Jacobian 组装、线性系统求解、状态更新）融合进单个 CUDA kernel，消除中间结果的全局内存读写。这是 ParaGRU 取得 2.6×、ParaLSTM 取得 1.5× 相对 Mamba 加速比（$L=2^9$）的关键实现。

**6. 模块间数据流**

整个 pipeline 的数据流为：输入序列 $\{x_l\}$ → Jacobian 组装模块（计算 $J_f$）→ 牛顿外层迭代（构建块双对角系统）→ 并行归约内层求解（更新 $\delta h$）→ 状态更新 → 收敛判定。收敛后的隐藏状态序列 $\{h_l\}$ 直接送入后续的 MLP 层（遵循与 Transformer/Mamba2 相同的块结构：序列混合器 + MLP + 残差连接 + RMSNorm）。

## 核心模块与公式推导

### 问题重构：从序列递归到非线性方程组

传统RNN的核心瓶颈在于其序列依赖：给定输入序列 $\{x_l\}_{l=1}^L$，隐藏状态按 $\pmb{h}_l = \pmb{f}(\pmb{h}_{l-1}, \pmb{x}_l)$ 逐时间步递推，每一步必须等待上一步完成，训练并行度受限于序列长度 $L$。ParaRNN 的核心洞察是将这一串行过程重新表述为整个序列上的非线性方程组：

$$
\left\{ \begin{array}{ll}
h_1 - f(\mathbf{0}, x_1) = \mathbf{0} \\
h_2 - f(h_1, x_2) = \mathbf{0} \\
\vdots \\
h_L - f(h_{L-1}, x_L) = \mathbf{0}
\end{array} \right.
$$

该方程组包含 $L$ 个方程，未知量为全部 $L$ 个隐藏状态。一旦将其视为数值求解问题，就可以借助成熟的迭代方法——牛顿法——在序列维度上并行求解。

### 牛顿外层求解器

牛顿法通过迭代线性化逼近非线性系统的解。在第 $k$ 步，将当前估计 $\{h_l^k\}$ 处的线性化系统写为：

$$
\left[ \begin{array}{cccc}
I \\
-J_f|_{h_1^k} & I \\
& \ddots & \ddots \\
& & -J_f|_{h_{L-1}^k} & I
\end{array} \right]
\left[ \begin{array}{c} \delta h_1^k \\ \delta h_2^k \\ \vdots \\ \delta h_L^k \end{array} \right] =
\left[ \begin{array}{c} f(\mathbf{0}, x_1) - h_1^k \\ f(h_1^k, x_2) - h_2^k \\ \vdots \\ f(h_{L-1}^k, x_L) - h_L^k \end{array} \right]
$$

其中 $J_f|_{h_{l}^k}$ 是递归函数 $\pmb{f}$ 在第 $l$ 步对隐藏状态的 Jacobian 矩阵。该线性系统的系数矩阵具有**块双对角结构**：主对角线为恒等矩阵 $I$，次对角线为负的 Jacobian 矩阵。这一特殊结构是并行化的关键——它天然适合前缀扫描（parallel reduction / prefix sum）算法进行高效求解。

### 并行归约内层求解器

对于形如上述的块双对角系统，通过展开递推关系可显式求解：

$$
\delta h_l^k = \left( f(h_{l-1}^k, x_l) - h_l^k \right) + J_f|_{h_{l-1}^k} \cdot \delta h_{l-1}^k
$$

该递推在形式上类似于线性RNN的状态更新，可利用矩阵乘法的结合律通过并行前缀扫描一次性求解所有 $\delta h_l^k$。ParaRNN 提供了三种实现：

1. **纯 PyTorch 实现**：直接调用 PyTorch 的前缀扫描操作，便于快速原型验证。
2. **CUDA 加速并行归约**：硬件感知的混合算法，在 GPU 的线程、warp、block 和 device 四个层级分别采用前向替换和并行归约，针对块双对角结构定制。
3. **全融合 CUDA 内核**：将整个牛顿迭代过程（Jacobian 组装、线性系统求解、状态更新）融合进单个 CUDA kernel，消除中间结果的全局内存读写，实现最大加速比。

### Jacobian 结构简化：对角化约束

上述并行归约的效率取决于 Jacobian 矩阵的结构。若 $J_f$ 为稠密矩阵（尺寸 $d_h \times d_h$），存储和乘法开销为 $O(d_h^2)$，并行扫描将不可行。ParaRNN 的关键设计选择是**强制状态矩阵和窥视孔矩阵为对角阵**：

$$
A_* = \operatorname{diag}(a_*), \quad C_* = \operatorname{diag}(c_*), \quad a_*, c_* \in \mathbb{R}^{d_h}
$$

在此约束下：
- **ParaGRU** 的 Jacobian 退化为纯对角矩阵；
- **ParaLSTM**（含窥视孔连接）的 Jacobian 退化为 $2 \times 2$ 块对角矩阵。

这使得 Jacobian 存储降至 $O(L \cdot d_h)$，每对元素乘法复杂度降至 $O(d_h)$，且可在隐藏状态维度上完全并行。

### 适配的 GRU 与 LSTM 单元

**ParaGRU 单元**（对角化 GRU）：

$$
\begin{aligned}
z_l &= \sigma_g(A_z h_{l-1} + B_z x_l + b_z) \\
r_l &= \sigma_g(A_r h_{l-1} + B_r x_l + b_r) \\
c_l &= \sigma_h(A_c (h_{l-1} \odot r_l) + B_c x_l + b_c) \\
h_l &= (1 - z_l) \odot h_{l-1} + z_l \odot c_l
\end{aligned}
$$

**ParaLSTM 单元**（对角化 LSTM with peephole）：

$$
\begin{aligned}
f_l &= \sigma_g(A_f h_{l-1} + B_f x_l + C_f c_{l-1} + b_f) \\
z_l &= \sigma_z(A_z h_{l-1} + B_z x_l + b_z) \\
c_l &= f_l \odot c_{l-1} + (1 - f_l) \odot z_l \\
o_l &= \sigma_g(A_o h_{l-1} + B_o x_l + C_o c_l + b_o) \\
h_l &= o_l \odot \sigma_h(c_l)
\end{aligned}
$$

其中所有 $A_*$ 和 $C_*$ 均为对角矩阵。这一简化将 $d_h$ 维的 RNN 细胞实质分解为 $d_h$ 个独立的一维细胞，虽抑制了隐藏状态内部的交叉混合能力，但使得并行前缀扫描高效可行。实验表明，这一表达力损失在语言建模任务上可通过增加模型规模得到补偿。

### 反向传播的并行化

反向传播时，损失 $\mathcal{L}$ 对隐藏状态的梯度满足如下递推：

$$
\nabla_{h_{l-1}} \mathcal{L} = J_f|_{h_{l-1}}^\top \nabla_{h_l} \mathcal{L} + \partial_{h_{l-1}} \mathcal{L}, \quad \forall l = L, \ldots, 1
$$

该递推在结构上等价于一个线性 RNN 的反向展开，因此**无需牛顿迭代**，可直接通过一次并行归约完成全部梯度计算。

## 实验与分析

### 核心性能验证

ParaRNN 在语言建模和合成任务上系统验证了非线性 RNN 并行训练的有效性。在 7B 参数规模的语言建模基准上（DCLM 数据集），ParaGRU 和 ParaLSTM 分别取得 9.19 和 9.16 的困惑度，优于同规模 Transformer 的 9.55，但略逊于 Mamba2 的 8.62（Table 2）。这表明经典非线性 RNN 在获得并行训练能力后，其建模能力可与主流架构竞争。


![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mX8b64iUaa/figures/005_Table_2.jpg]]
*Table 2: Perplexity, parameters count, and evaluation scores on lm-eval-harness (Gao et al., 2021) tasks, for 7B models. Accuracies in percentages. Shot counts are reported in brackets*

在训练效率方面，全融合 CUDA 实现的牛顿法前向传播在序列长度 $L=2^9$ 时，ParaGRU 达到 Mamba SSM 应用的 2.6 倍加速，ParaLSTM 达到 1.5 倍加速（Figure 2 右）。这一加速源于将整个牛顿迭代（Jacobian 装配、线性系统求解、状态更新）融合为单个 CUDA 核，消除了多次核启动和全局内存同步的开销。

在推理阶段，7B 模型在 $L=2^{11}$ 的生成场景下，ParaGRU 和 ParaLSTM 的吞吐量约为 37–38 tokens/s，而 Mamba 约为 28 tokens/s，Transformer 则显著更低（Figure 3, Table 3）。RNN 架构固有的逐 token 生成模式在此展现出效率优势。


![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mX8b64iUaa/figures/011_Table_3.jpg]]
*Table 3: Throughput results at regime ( L = 2 ^ { 1 1 } ) for the model types and sizes considered*

### 合成任务上的表达能力

单层模型在合成任务上的准确率（Table 1）揭示了非线性 RNN 的表达特性。ParaGRU 和 ParaLSTM 在 Cycle Navigation、Modular Arithmetic、Copy Memory 等任务上均达到 100% 准确率，而 Mamba2 在 Copy Memory 等需要非线性记忆交互的任务上表现较弱。在难度较高的 A5 任务上，ParaGRU 和 ParaLSTM 达到 38–40% 的准确率，显著优于 Transformer。这验证了非线性递归函数在建模复杂序列依赖上的固有优势，与线性 SSM 的局限性形成对比。


![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mX8b64iUaa/figures/004_Table_1.jpg]]
*Table 1: Single-layer accuracy on synthetic tasks. ( )$^ { \dagger }$ denotes results computed training only the RNN cell (see App. C.2 for details)*

### 牛顿法收敛性分析

牛顿法的收敛行为是 ParaRNN 效率的关键前提。实验表明（Figure 4），ParaGRU 和 ParaLSTM 在随机初始化和训练后的 400M 模型最后一层中，均能在 3 次迭代内稳定收敛，残差下降至机器精度量级。这一性质在 $L=2^7$ 到 $L=2^{11}$ 的序列长度范围内保持一致，确保了并行训练过程中固定的计算开销，而非随序列长度增长的迭代次数。

### 并行归约实现效率

不同实现层级的性能对比（Figure 2 左）揭示了硬件感知优化的重要性。纯 PyTorch 实现的并行归约在 $L=2^{18}$ 之前呈现对数增长，随后线性化；CUDA 加速版本则保持更平坦的运行时曲线。在 $L=2^9$ 时，针对对角 Jacobian 的 CUDA 并行归约相比 Mamba 的并行扫描有约 1.1 倍加速，而针对 $2\times 2$ 块对角 Jacobian 的版本则有约 0.84 倍减速。这一差异源于块对角矩阵乘法的额外计算开销。

全融合 CUDA 核的 chunk size 超参数对性能有显著影响（Figure 8）。在训练长度 $L=2^{11}$ 时，$c=2$ 为最优设置；对于更短序列，$c=1$ 表现更好。这反映了 GPU 线程层次结构中工作分配粒度与同步开销之间的权衡。

### 内存与可扩展性

峰值 GPU 内存使用随序列长度 $L$ 和隐藏状态维度 $d_h$ 线性增长（Figure 9），符合 Jacobian 存储复杂度 $O(L \cdot d_h)$ 的理论预期。这一线性增长特性使得 ParaRNN 在长序列场景下的内存需求可预测，但也在极端长度下构成瓶颈。

### 实验公平性保障

所有对比实验遵循严格的公平性控制：各模型（ParaGRU、ParaLSTM、Mamba2、Transformer）采用相同的块结构（序列混合器 + MLP + 残差连接 + RMSNorm），训练配置遵循 Chinchilla 最优 token 预算，使用相同的批次大小、序列长度（2048 tokens）和优化器设置（Table 4, Table 5）。下游评估统一使用 lm-eval-harness 框架和相同的 few-shot 设置，确保性能对比的公正性。


![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mX8b64iUaa/figures/014_Table_4.jpg]]
*Table 4: Architecture specifications and optimal hyperparameters for our experiments. We report structural parameters (number of layers, number of heads and model width) and training hyperparameters (learning rate and weight decay) that achieved lowest perplexity for each model type and scale. Time measurements show average single-step training cost on NVIDIA H100 GPUs, while Memory measurements show the per-sample peak memory usage during one optimization step*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mX8b64iUaa/figures/015_Table_5.jpg]]
*Table 5: Scale-specific training configurations on nodes with 8 NVIDIA H100 GPUs each All models use 2048-token sequences and follow (∼ 1×) Chinchilla-optimal token budgets (Hoffmann et al., 2022) for batch-size selection. The z-loss regularization coefficient is taken from DCLM (Li et al., 2024)*

### 局限性与失效模式

尽管 ParaRNN 在效率和性能上取得了显著成果，仍存在若干关键局限：

1. **收敛性依赖**：牛顿法的快速收敛（3 次迭代）是效率优势的前提，但该性质仅在 ParaGRU 和 ParaLSTM 上得到验证，无法保证新设计的 RNN 变体同样满足此条件。

2. **表达力折损**：对角状态矩阵的约束将 $d_h$ 维的 RNN 细胞分解为 $d_h$ 个独立的一维细胞，完全丧失了隐藏状态内部的交叉信息混合能力。这一设计选择虽使并行归约高效可行，但在理论上限制了模型的表达能力。

3. **扩展性障碍**：全融合 CUDA 实现要求用户手动提供 Jacobian 计算的 CUDA 代码，增加了为新 RNN 变体获得最优性能的工程复杂度。

4. **任务泛化未验证**：当前实验集中在语言建模，尚未在时间序列预测、强化学习等其他序列建模场景中验证方法的泛化性。

5. **超长序列瓶颈**：在极端序列长度下，跨块的并行归约需要多次核启动和全局内存同步，可能削弱并行优势。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mX8b64iUaa/figures/017_Table_6.jpg]]
*Table 6: Final perplexities, and evaluation scores on reference downstream tasks from lm-eval-harness (Gao et al., 2021), for all model types and scales considered*


## 方法谱系与知识库定位

### 1. 核心问题与突破点

非线性RNN（如GRU、LSTM）的训练长期受困于一个根本性瓶颈：其序列递归本质强制要求逐时间步串行计算，无法在序列维度上并行化。这一限制使得非线性RNN在扩展到现代大型语言模型的训练规模时远远落后于**Transformer**（Vaswani et al., NeurIPS 2017）等可并行架构。线性状态空间模型（SSM）如**Mamba**（Gu & Dao, 2023）和**Mamba2**（Dao & Gu, 2024）通过将状态转移矩阵设计为线性形式，借助结合律实现并行前缀扫描（parallel scan），成功绕过了这一瓶颈。然而，线性约束本身就是一种表达能力的妥协——它限制了模型对复杂非线性序列依赖的建模能力。

ParaRNN的突破在于首次证明：非线性RNN的训练同样可以在序列维度上并行化，且并行效率可与线性SSM相媲美甚至超越。其核心洞察是将非线性序列操作重新定义为方程组的数值求解问题：将整个序列上的RNN前向传播视为一个非线性方程组，利用牛顿法迭代线性化，再通过针对块双对角结构定制的高效并行归约（parallel reduction）算法实现全序列并行求解。

### 2. 与基线方法的关系定位

ParaRNN在方法谱系中占据了一个独特的位置——它既不是对Transformer的改进，也不是对线性SSM的简单替代，而是在两者之间开辟了一条新路径：

**相对于Transformer**：Transformer通过自注意力机制实现了完全的序列并行化，但代价是$O(L^2)$的计算和存储复杂度。ParaRNN的并行归约复杂度为$O(L \cdot d_h)$，在长序列场景下具有理论优势。实验表明，ParaLSTM在7B参数规模上的语言建模困惑度（9.16）优于Transformer（9.55），验证了非线性RNN在表达能力上的潜在优势。

**相对于Mamba/Mamba2**：Mamba系列通过将状态空间模型线性化，利用结合律实现并行扫描，是目前并行RNN-like模型的标杆。ParaRNN直接挑战了“只有线性模型才能并行”的隐含假设。在训练速度上，全融合CUDA实现的ParaGRU在序列长度$L=2^9$时达到Mamba SSM应用的2.6倍加速，ParaLSTM达到1.5倍加速。在推理吞吐量上，ParaRNN在7B规模、$L=2^{11}$的生成场景下达到约37-38 tokens/s，约为Mamba（~28 tokens/s）的1.3倍。在合成任务上，ParaGRU和ParaLSTM在需要非线性记忆的任务（如Copy Memory）上表现优于Mamba2。

**与Danieli et al. (2023)的关系**：将牛顿迭代与并行归约结合以并行求解非线性序列操作的思想最早由Danieli et al. (2023)提出。ParaRNN在此基础上进行了三项关键扩展：(1) 将该方法自动化并封装为通用库，只需用户提供递归步骤定义即可自动并行化；(2) 通过强制状态矩阵对角化，将Jacobian从稠密矩阵简化为对角或$2 \times 2$块对角结构，使并行归约的内存和计算开销从$O(d_h^2)$降至$O(d_h)$；(3) 提供了三层实现（纯PyTorch、CUDA加速、全融合CUDA核），在工程层面使该方法真正可用于大规模训练。

### 3. 方法适用边界

ParaRNN的有效性依赖于以下前提条件，这些条件界定了其适用范围：

**牛顿法收敛性要求**：整个方法建立在牛顿法在$O(1)$次迭代内收敛的基础上。ParaGRU和ParaLSTM在训练全过程中稳定在3次迭代内收敛（图4），但这一性质并非对所有RNN变体都成立。对于新设计的RNN单元，若其递归函数$f$的谱特性导致牛顿法收敛缓慢，并行优势将大打折扣。目前缺乏从理论上建立$f$的谱特性与牛顿法快速收敛之间充分条件的系统研究。

**Jacobian结构约束**：为将并行归约的每次二元操作开销从$O(d_h^2)$降至$O(d_h)$，ParaRNN强制状态矩阵和窥视孔矩阵为对角阵。这实质上是将单个$d_h$维的RNN细胞分解为$d_h$个独立的一维细胞，完全丧失了隐藏状态内部的交叉信息混合能力。这一简化在语言建模任务上表现尚可，但在需要复杂状态交互的任务上可能成为瓶颈。

**序列长度与GPU架构**：在极长序列下，跨块并行归约需要多次核启动和全局内存同步，开销增大，可能削弱并行优势。图2（左）显示，纯PyTorch实现在$L=2^{18}$时运行时间开始线性化增长。全融合CUDA核通过将整个牛顿例程融合为单个核来缓解这一问题，但对不同序列长度需要调整chunk size超参数（$c=2$在训练长度$L=2^{11}$时最优，$c=1$更适合短序列）。

**任务领域限制**：当前实验集中在语言建模任务上。ParaRNN框架在其他序列建模场景（如时间序列预测、强化学习、图像补丁序列、基因组序列）上的性能和效率表现尚未验证。

### 4. 局限性与开放问题

**结构化Jacobian导致的表达力损失**：对角Jacobian约束是当前方法效率的关键，但也构成了最根本的表达力限制。一个关键开放问题是：能否在保持高效并行归约的前提下，设计更丰富的Jacobian结构（如块三对角、Householder参数化、低秩加对角等）以恢复隐藏状态内部的混合能力？这需要重新设计并行归约算法以适应非对角的块结构。

**牛顿法收敛的理论保证**：目前牛顿法的快速收敛是经验观察结果，缺乏理论指导。能否从RNN递归函数$f$的Lipschitz常数、谱半径等性质出发，建立快速收敛的充分条件，从而指导新型RNN的设计，是一个重要的理论开放问题。

**全融合实现的扩展性**：全融合CUDA实现需要用户手动提供Jacobian计算的CUDA代码，这增加了为新RNN扩展最高性能的难度。如何自动化这一过程（例如通过代码生成或即时编译），使任何新定义的RNN都能自动获得最高性能，是工程层面的重要挑战。

**与混合架构的结合潜力**：ParaRNN的思想是否可以与现有的线性注意力或混合架构（如将部分层替换为非线性RNN）结合，以在训练速度与推理效率之间取得更优权衡，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/ParaRNN_Unlocking_Parallel_Training_of_Nonlinear_RNNs_for_Large_Language_Models.pdf]]
