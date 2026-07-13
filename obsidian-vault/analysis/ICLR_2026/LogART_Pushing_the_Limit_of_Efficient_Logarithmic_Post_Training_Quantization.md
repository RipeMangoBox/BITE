---
title: "LogART: Pushing the Limit of Efficient Logarithmic Post-Training Quantization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LogART_Pushing_the_Limit_of_Efficient_Logarithmic_Post_Training_Quantization.pdf
project_link: null
code_link: https://github.com/logart-lab/logart
openreview_forum_id: V85HbymBLW
aliases:
- LLART
- LogART
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/non_convex
core_operator: "引入针对对数域的可学习元素级舍入（LLR）并联合多级超参数搜索（OHS），通过优化动态基数、非对称码分配和异常值裁剪来重构量化误差，同时将硬件近似噪声吸收进优化过程。"
primary_logic: "将量化误差分解为网格离散化误差（由OHS解决）和舍入误差（由LLR解决），二者在任务驱动下协同工作，利用有符号二元展开（SDE）吸收√2的硬件近似误差，从而在不增加算术单元成本的前提下实现精度与效率的最优折衷。"
claims:
- "在3比特权重量化下，LogART全面超越GPTQ、BRECQ、AffineQuant和aespa等线性PTQ方法，取得最低困惑度并显著减少运行时间（如LLaMA2‑7B PPL 6.31 vs GPTQ 8.66，时间1.24小时 vs BRECQ OOM）。"
- "消融实验表明OHS与LLR具有强协同效应：加入OHS使LLR收敛速度提升4倍（迭代次数由2000降至500），总运行时间从4.00分钟降至1.25分钟，同时OPT‑125M的PPL从36.27降至31.15。"
- "LogART算术单元（AE）面积仅53.2 µm²，功耗3.45 µW，相比于线性PTQ代表设计实现超过40%的面积和功耗缩减。"
- "WikiText‑2 (OPT‑125M 3‑bit) 上 PPL = 31.52"
---

# LogART: Pushing the Limit of Efficient Logarithmic Post-Training Quantization

> [!tip] 核心洞察
> 将量化误差分解为网格离散化误差（由OHS解决）和舍入误差（由LLR解决），二者在任务驱动下协同工作，利用有符号二元展开（SDE）吸收√2的硬件近似误差，从而在不增加算术单元成本的前提下实现精度与效率的最优折衷。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LogART：突破高效对数后训练量化极限 |
| 英文题名 | LogART: Pushing the Limit of Efficient Logarithmic Post-Training Quantization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=V85HbymBLW) · [GitHub](https://github.com/logart-lab/logart) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/non_convex |
| Method | LogART (Logarithmic Adaptive Rounding Techniques) |
| Dataset | WikiText‑2 (OPT‑125M 3‑bit), WikiText‑2 (LLaMA2‑7B 3‑bit), ImageNet (ResNet18 4‑bit), ImageNet (ViT‑Base 4‑bit) |

> [!tip] 效果简介
> - WikiText‑2 (OPT‑125M 3‑bit) 上，PPL 为 31.52，对比 34.07 (BRECQ)，变化 ‑2.55。
> - WikiText‑2 (LLaMA2‑7B 3‑bit) 上，PPL 为 6.31，对比 8.66 (GPTQ)，变化 ‑2.35。
> - ImageNet (ResNet18 4‑bit) 上，Top‑1 Accuracy (%) 为 70.79，对比 68.14 (AdaRound)，变化 +2.65。

## 概要

对数后训练量化（PTQ）面临一个根本瓶颈：传统最近邻舍入（RTN）无法感知任务损失，而标准对数网格固有的对称性与对异常值的强敏感性进一步加剧了极低位宽下的精度退化。此外，现有的可学习舍入策略直接应用于对数域面临困难，使得对数PTQ长期落后于线性PTQ的性能表现。

LogART 通过两个协同工作的核心机制突破上述限制：**可学习对数舍入（LLR）** 与 **多级超参数搜索（OHS）**。其核心洞察在于将量化误差分解为网格离散化误差（由 OHS 解决）和舍入误差（由 LLR 解决），二者在任务驱动下联合优化。具体而言，OHS 通过最小化块重建误差，联合搜索动态基数、非对称码分配和异常值裁剪策略，重构量化网格；LLR 则在该网格上学习元素级的软舍入变量，直接最小化任务感知的重建损失。此外，LogART 通过有符号二元展开（SDE）近似 √2 乘法，将硬件近似噪声吸收进优化过程，在不增加算术单元成本的前提下实现精度与效率的折衷。

**主要结果**：在 3 比特权重量化下，LogART 全面超越 GPTQ、BRECQ、AffineQuant 和 aespa 等线性 PTQ 方法。例如，LLaMA2‑7B 的困惑度降至 6.31（GPTQ 为 8.66），运行时间仅 1.24 小时（BRECQ 出现显存溢出）。消融实验证实 OHS 与 LLR 具有强协同效应：加入 OHS 使 LLR 收敛速度提升 4 倍，总运行时间从 4.00 分钟降至 1.25 分钟，同时 OPT‑125M 的 PPL 从 36.27 降至 31.15。在硬件端，LogART 算术单元面积仅 53.2 µm²，功耗 3.45 µW，相比线性 PTQ 代表设计实现超过 40% 的面积和功耗缩减。

LogART 当前仅支持权重量化，尚未集成激活量化；多基数设计引入了一定的解码开销，且更大规模模型（>13B）及实际流片验证有待开展。



### 量化范式转变：从线性到对数

深度神经网络的高效部署始终受限于模型规模与硬件资源之间的张力。后训练量化（PTQ）作为一种无需重训练的压缩范式，因其低数据需求和快速部署能力而受到广泛关注。然而，主流PTQ方法几乎全部构建在线性量化之上——将浮点权重映射到均匀间隔的整数网格，依赖乘法-累加（MAC）算术单元完成推理。这种设计在4比特以上表现稳健，但当比特位宽降至3比特乃至更低时，线性网格的表示能力急剧退化，精度损失变得难以接受。

对数域量化提供了一条根本不同的路径。其核心思想是将权重的绝对值映射到以2为底的对数域，使得原本昂贵的乘法运算退化为整数加法。这一特性在硬件层面具有天然优势：对数算术单元（AE）可以完全消除乘法器，仅需加法器和移位器即可完成乘累加操作，从而大幅缩减芯片面积与功耗。然而，这一范式转换也带来了新的挑战——对数网格的固有属性使得传统PTQ技术无法直接迁移。

### 对数PTQ的三重困境

现有对数PTQ方法面临三个相互纠缠的瓶颈，在极低位宽下共同导致精度严重退化。

**网格离散化误差的刚性。** 传统对数PTQ采用最近邻舍入（RTN）将权重映射到对数网格，但RTN完全忽略任务损失，仅以最小化逐元素量化误差为目标。在3比特下，对数网格的码字数量骤减至仅7个（含符号位），RTN的粗粒度决策使得量化误差在层间传播中迅速放大。线性域中已有的可学习舍入策略（如AdaRound）通过在连续空间中优化离散化决策来缓解这一问题，但其优化机制依赖于线性网格的均匀结构，无法直接应用于对数域的非均匀网格。

**对数网格的结构性缺陷。** 标准以2为底的对数量化存在三个固有弱点：其一，网格密度随数值增大而指数级稀疏，对网络中广泛存在的中等幅度权重表示不足；其二，对数量化天然对称——正负权重共享相同的码字分配策略，而实际权重分布往往呈现显著的非对称性；其三，以绝对最大值为界的量化范围对异常值极度敏感，单个离群点即可压缩整个网格的有效表示区间。这些结构性缺陷并非线性PTQ的核心关注点，因为线性网格的均匀性和零点的引入天然缓解了对称性与异常值问题，但对数域中缺乏相应的解决机制。

**硬件近似与算法精度的脱节。** 在实际硬件实现中，涉及$\sqrt{2}$的乘法——这是多基数对数量化中不可避免的操作——需要通过移位和加法来近似。传统的做法是先以精确$\sqrt{2}$完成算法设计，再在硬件映射阶段进行近似，两者独立优化。然而，这种分离式设计在极低位宽下会导致显著的精度劣化：算法阶段认为最优的量化配置，在硬件近似后可能不再最优。如何在优化过程中主动吸收硬件近似误差，而非被动承受其后果，是对数PTQ走向实际部署的关键问题。

### 核心洞察：误差分解与协同优化

LogART的核心洞察在于将对数量化的精度退化归因于两类可分离的误差源：**网格离散化误差**（由量化器的超参数配置决定）和**舍入误差**（由每个元素的离散化决策决定）。前者决定了“哪些值可用”，后者决定了“每个权重选哪个值”。传统对数PTQ将两者混为一谈，用统一的RTN规则处理，而LogART通过两个协同工作的模块——优化超参数搜索（OHS）和可学习对数舍入（LLR）——分别攻克。

OHS在块级重建误差的驱动下，联合搜索动态基数配置、非对称码分配和异常值裁剪阈值，从结构层面重塑量化网格以匹配权重分布。LLR则在OHS确定的网格上，以任务损失为导向学习每个权重元素的最优舍入方向，从决策层面精细化补偿残余误差。更为关键的是，两者在优化过程中共同吸收硬件近似噪声——将有符号二元展开（SDE）对$\sqrt{2}$的近似误差纳入重建损失，使得最终量化方案对硬件实现具有内在鲁棒性。

这一“网格-舍入”分离设计使得LogART在3比特权重量化下取得了突破性精度：在LLaMA2-7B上，LogART以6.31的困惑度（PPL）显著优于GPTQ的8.66，同时运行时间仅1.24小时（对比BRECQ的显存溢出）；在硬件层面，LogART算术单元面积仅53.2 µm²，功耗3.45 µW，相较于线性PTQ代表设计实现超过40%的面积和功耗缩减。这些结果表明，通过任务驱动的协同优化，对数PTQ能够在精度与效率之间取得此前被认为不可兼得的平衡。



## 核心方法与创新机理

LogART 的核心创新在于首次将对数量化后训练（PTQ）中的**舍入误差**与**网格离散化误差**解耦，并分别通过可学习机制进行任务驱动优化。具体而言，LogART 引入了三个相互协同的关键技术组件，构成了四个关键的 changed slot：

### 1. 可学习对数舍入（LLR）

传统对数 PTQ 使用最近邻舍入（RTN），无法感知任务损失，导致极低位宽下精度严重退化。LogART 首次将对数域中的 RTN 操作替换为可学习的元素级舍入变量 $\mathbf{R}$，通过 sigmoid 函数 $\sigma(\mathbf{R})$ 实现软量化：

$$\mathbf{Q_W} = \mathrm{clamp}\left(\left\lfloor -\log_2\left(\frac{|\mathbf{W}|}{s}\right)\right\rfloor + \sigma(\mathbf{R}), 0, 2^{N-1}-1\right)$$

$\mathbf{R}$ 通过最小化任务感知的重建误差进行优化，并辅以正则项 $\sum_{i,j}(1-|2\sigma(\mathbf{R}_{ij})-1|^{\beta})$ 驱动 $\sigma(\mathbf{R})$ 收敛至 0 或 1，从而在优化结束后恢复硬舍入。这一机制使得量化器能够根据任务损失自适应地决定每个权重的舍入方向，直接解决了对数域中舍入误差不可控的核心瓶颈。

### 2. 多级超参数搜索（OHS）

标准对数网格的固有对称性和强异常值敏感性是精度退化的另一主因。OHS 通过三个子模块重构量化网格，从源头减少离散化误差：

- **动态双基数（DBS）**：引入 base-2 与 base-$\sqrt{2}$ 双基数方案，通过自适应阈值 $t$ 将大值分配给 base-$\sqrt{2}$（更密集的网格），小值分配给 base-2。每通道基数比例 $n_1:n_2$ 通过块级重建误差搜索确定。

- **非对称码分配（ABS）**：传统对数量化对正负权重分配相同数量的码字，而 LogART 通过每通道自适应边界 $l_a$ 为非对称分布的正值和负值分配不同数量的码字，解决了对数域固有的对称性约束。

- **异常值自适应裁剪（SFS）**：引入搜索式超参数 $s_{\mathrm{of}}$ 实现每通道缩放因子的自适应裁剪，通过块级重建误差搜索最优值，避免异常值主导量化范围。

这三个子模块通过联合最小化块重建误差进行统一优化：

$$\arg\min_{s_{\mathrm{of}}, n_1, n_2} \mathbb{E}\left[\|\mathcal{L}(\Delta\mathbf{W}, \mathbf{X})\|_F^2\right]$$

### 3. 硬件近似吸收（HAF）

base-$\sqrt{2}$ 的乘法操作在硬件上不友好。LogART 通过 $K$ 项有符号二元展开（SDE）将 $\sqrt{2}$ 近似为移位-加法操作：

$$\sqrt{2} \approx \mathrm{SDE}(\sqrt{2}, K) = \sum_{k=1}^{K} a_k \cdot \frac{1}{2^{d_k}},\; a_k\in\{-1,+1\}$$

实际采用 $K=2$ 的配置（$X + X/2$），将硬件近似误差直接纳入 OHS 和 LLR 的优化过程中吸收，从而在不增加算术单元成本的前提下实现精度与效率的最优折衷。

### 协同效应

OHS 与 LLR 之间存在强协同效应：OHS 通过优化量化网格最小化内在离散化误差，为 LLR 提供了一个更优的搜索起点。消融实验证实，加入 OHS 后 LLR 的收敛速度提升约 4 倍（迭代次数从 2000 降至 500），总运行时间从 4.00 分钟降至 1.25 分钟，同时 OPT-125M 的 PPL 从 36.27 显著降至 31.15（Table 7, Figure 5）。这一协同效应的数学本质在附录 B 中被形式化：量化误差可分解为 OHS 控制的离散化误差 $\varepsilon_1$ 和 LLR 控制的舍入误差 $\varepsilon_2$，二者满足 $\|\Delta\mathbf{W} \mathbf{H}^{1/2}\|_F^2 \leq (\varepsilon_1 + \varepsilon_2)^2$，从理论上解释了协同机制。



![[assets/figures/papers/iclr26_0009_V85HbymBLW_LogART_Pushing_the_Limit_of_Efficient_Logarithmi/figures/004_Figure_2.jpg]]
*Figure 2: The overall LogART framework consists of two key components: OHS and LLR. OHS searches for optimal hyperparameter configurations in an asymmetry-aware, outlier-resilient, and multi-base manner. LLR replaces RTN with learnable element-wise rounding that minimizes local reconstruction loss while absorbing hardware approximation noise during calibration*

LogART 的整体流程由两个核心模块串联构成：**OHS（优化超参数搜索）**与**LLR（可学习对数舍入）**，并嵌入**HAF（硬件近似函数）**将√2乘法转化为移位‑加法，三者协同完成从预训练权重到硬件友好量化模型的转换。

### 流程概览

1. **输入**：预训练全精度权重 $\mathbf{W}$、少量无标签校准数据（LLM 使用 32 段 2048 token 的 C4 或 WikiText‑2，视觉模型使用 2048 张无标签 ImageNet 图像）。
2. **OHS 阶段**：在无需梯度优化的前提下，通过最小化块重建误差联合搜索三个层级的超参数——
   - **ABS（非对称界搜索）**：为每通道的正负权重分配不同数量的对数码字，解决标准对数量化固有的对称性缺陷。
   - **SFS（缩放因子搜索）**：搜索每通道最优的异常值裁剪缩放因子 $s_{\mathrm{of}}$，替代以绝对最大值为界的粗暴裁剪。
   - **DBS（动态基数搜索）**：联合确定每通道 base‑√2 与 base‑2 的码字分配比例 $(n_1, n_2)$，使大值使用细粒度 base‑√2 网格、小值使用粗粒度 base‑2 网格。
   三者的联合优化目标为块重建误差的 Frobenius 范数最小化（Eq. 18），输出最优量化网格配置 $\theta^*$。
3. **LLR 阶段**：在 OHS 确定的量化网格上，将传统 RTN 中的最近邻舍入替换为可学习的元素级软舍入变量 $\sigma(\mathbf{R})$（Eq. 5），通过最小化任务感知的层/块重建损失与正则项（Eq. 7）驱动 $\mathbf{R}$ 收敛至 0/1 二元值，实现逐元素最优舍入。
4. **HAF 吸收**：在整个前向量化过程中，涉及 $\sqrt{2}$ 的乘法均通过 $K$ 项有符号二元展开 $\mathrm{SDE}(\sqrt{2}, K)$ 近似为移位‑加法（Eq. 19），实际采用 $K=2$ 的 $X + X/2$ 实现。该近似误差被显式纳入 OHS 与 LLR 的优化回路中吸收，从而避免精度崩溃。
5. **输出**：量化后的整数码字 $\mathbf{Q_W}$ 与对应的反量化参数，可直接映射到面积仅 53.2 µm²、功耗 3.45 µW 的对数算术单元（AE）上执行推理。

### 模块间的因果依赖

OHS 与 LLR 之间存在严格的先后依赖与协同加速关系。OHS 首先将量化误差分解中的网格离散化误差降至最低，为 LLR 提供一个已逼近最优的量化网格；LLR 在此网格上仅需处理残差的舍入误差。消融实验证实，加入 OHS 后 LLR 的收敛迭代次数从 2000 次骤降至 500 次（4 倍加速），总运行时间从 4.00 分钟压缩至 1.25 分钟，同时 OPT‑125M 的 PPL 从 36.27 进一步改善至 31.15（Table 7, Figure 5）。这一协同效应的数学本质在附录 B.3 中被形式化：量化误差的上界可分解为 OHS 控制的离散化误差 $\varepsilon_1$ 与 LLR 控制的舍入误差 $\varepsilon_2$ 之和的平方，二者分别由独立的优化子问题求解，组合后产生累进增益。

### 硬件近似的前向集成

HAF 并非独立的后处理步骤，而是作为量化前向的组成部分嵌入 OHS 与 LLR 的优化循环。在 OHS 搜索和 LLR 梯度反传过程中，前向计算均使用 $\mathrm{SDE}(\sqrt{2}, K)$ 近似，从而使搜索到的超参数和学习的舍入变量天然适应硬件近似噪声。若将 HAF 作为 naive 后处理施加，ResNet18 4‑bit 精度将从 70.79% 骤降至 68.75%；而 LogART 的集成式吸收仅造成 0.08% 的轻微下降（70.71%），证明了该设计的有效性（Table 9, Table 10）。

> **注意**：当前框架仅处理权重量化，激活保持 FP16。激活量化的集成是论文列出的开放问题之一。



LogART 将量化误差分解为两类可分别优化的子问题：**网格离散化误差**（由 OHS 解决）与**元素级舍入误差**（由 LLR 解决），二者在任务损失驱动下协同工作，同时通过 HAF 将硬件近似噪声吸收进优化过程。

### 3.1 可学习对数舍入 (LLR)

传统对数 PTQ 使用最近邻舍入 (RTN)，无法感知任务损失。LogART 首次将对数域中的 RTN 替换为可学习的元素级软舍入：

$$
\mathbf{Q_W} = \mathrm{clamp}\left(\left\lfloor -\log_2\left(\frac{|\mathbf{W}|}{s}\right)\right\rfloor + \sigma(\mathbf{R}),\; 0,\; 2^{N-1}-1\right)
$$

其中 $s$ 为每通道缩放因子，$\sigma(\mathbf{R})$ 是可学习变量 $\mathbf{R}$ 的 sigmoid 函数，实现从连续软舍入到最终 0/1 离散舍入的平滑过渡。去量化过程为：

$$
\widetilde{\mathbf{W}} = s \cdot \mathrm{sgn}(\mathbf{W}) \odot 2^{-\mathbf{Q_W}}
$$

LLR 的优化目标由任务感知重建误差与正则项组成：

$$
\underset{\mathbf{R}}{\arg\min}\;\mathbb{E}\left[\mathcal{L}(\Delta\mathbf{W})\right] + \lambda\sum_{i,j}\left(1 - \left|2\sigma(\mathbf{R}_{ij})-1\right|^{\beta}\right)
$$

其中重建误差在层粒度下利用 Hessian 矩阵 $\mathbf{H} = \mathbb{E}[\mathbf{X}\mathbf{X}^\top]$ 加权：

$$
\mathbb{E}[\mathcal{L}(\Delta\mathbf{W})] = \mathrm{tr}(\Delta\mathbf{W} \cdot \mathbf{H} \cdot \Delta\mathbf{W}^\top)
$$

正则项驱动 $\sigma(\mathbf{R})$ 趋向 0 或 1，$\beta$ 控制正则化强度。梯度通过量化链反向传播，详见附录 A。

### 3.2 动态基数、非对称与异常值弹性量化器

**动态基数 (Dynamic Base Quantizer)** 同时使用 base‑2 与 base‑$\sqrt{2}$ 两个码本，通过自适应阈值 $t$ 分配：大值使用 base‑$\sqrt{2}$ 以提供更细粒度，小值使用 base‑2 以覆盖更宽范围。每通道基数比例 $n_1$（base‑$\sqrt{2}$ 码字数）与 $n_2$（base‑2 码字数）满足：

$$
n_1 + n_2 = 2^{N-1} - 1
$$

阈值 $t$ 由基数分配推导：

$$
t = \sqrt{2}^{\frac{m - n_1 + 1}{2} + \lfloor\frac{m - n_1}{2}\rfloor}
$$

其中 $m$ 为最大码字索引。该设计解决了 base‑2 在近零区域码字过密而 base‑$\sqrt{2}$ 在远区码字过稀的固有矛盾。

**非对称量化 (Asymmetric Quantizer)** 解决对数网格固有的对称性问题。传统对数量化对正负权重分配等量码字，但当权重分布偏斜时造成容量浪费。LogART 引入每通道自适应边界偏移 $l_a$，为正值和负值分配不同数量的码字。偏移量由正负权重的对数码数差异计算：

$$
d_a = \begin{cases} |\log_{\sqrt{2}}(w_h)| - |\log_{\sqrt{2}}(w_l)|, & w_l \geq t \\ n_1 + \lfloor\frac{m - n_1}{2}\rfloor - |\log_2(w_l)|, & w_l < t \end{cases}
$$

其中 $w_h$、$w_l$ 分别为通道正/负权重最大绝对值。

**异常值弹性 (Outlier‑Resilient Quantizer)** 通过搜索式超参数 $s_{\mathrm{of}}$ 实现自适应裁剪，替代以绝对最大值为界的粗暴策略。

### 3.3 多级超参数搜索 (OHS)

OHS 在三个层级联合搜索最优量化配置，通过最小化块重建误差实现：

$$
\arg\min_{s_{\mathrm{of}}, n_1, n_2} \mathbb{E}\left[\|\mathcal{L}(\Delta\mathbf{W}, \mathbf{X})\|_F^2\right]
$$

三个子模块分工如下：
- **ABS (张量级非对称界搜索)**：无需校准数据，基于权重统计量启发式计算每通道非对称边界。
- **SFS (块级缩放因子搜索)**：在校准集上搜索最优每通道异常值缩放因子 $s_{\mathrm{of}}$。
- **DBS (块级动态基数搜索)**：联合搜索每通道基数比例 $n_1$、$n_2$。

OHS 与 LLR 的协同效应在附录 B 中有严格数学分解：OHS 最小化网格离散化误差 $\varepsilon_1$，LLR 在最优网格上最小化舍入误差 $\varepsilon_2$，总误差上界为 $(\varepsilon_1 + \varepsilon_2)^2$。

### 3.4 硬件近似函数 (HAF)

base‑$\sqrt{2}$ 涉及 $\sqrt{2}$ 乘法，直接实现硬件代价高。HAF 采用 $K$ 项有符号二元展开 (SDE) 将乘法转化为移位‑加法：

$$
\sqrt{2} \approx \mathrm{SDE}(\sqrt{2}, K) = \sum_{k=1}^{K} a_k \cdot \frac{1}{2^{d_k}},\quad a_k \in \{-1,+1\},\; d_k \in \mathbb{N}
$$

实际采用 $K=2$ 的配置（即 $X + X/2$），仅需一次移位和一次加法。关键创新在于：HAF 的近似误差被**吸收进 OHS 和 LLR 的优化过程**——量化器在校准阶段就感知到硬件近似噪声，从而在精度与硬件效率之间取得最优折衷，而非事后弥补。



## 实验与关键发现

### 主结果：语言模型3比特量化

LogART在LLM的3比特权重量化上首次实现了对数PTQ对大规模模型的可行扩展，并全面超越线性PTQ方法。Table 3汇总了核心对比：在OPT‑125M上，LogART取得WikiText‑2 PPL 31.52，显著优于BRECQ（34.07）和GPTQ（52.95），困惑度分别降低2.55和21.43；在LLaMA2‑7B上，LogART的PPL为6.31，对比GPTQ的8.66降低2.35。这一差距的根源在于对数域固有的高效表达密度——以更少比特覆盖更大动态范围——与OHS‑LLR协同优化的结合：OHS通过动态基数、非对称码分配和异常值裁剪重新设计量化网格，LLR则在任务损失驱动下学习逐元素的最优舍入。运行时方面，LogART仅需1.24小时即可完成LLaMA2‑7B量化，而BRECQ因内存溢出（OOM）无法运行，GPTQ虽仅需19.8秒但精度严重退化。该对比在统一校准数据（C4的32段2048 token）和单卡RTX 5090D条件下完成，公平性得到保证。

![[assets/figures/papers/iclr26_0009_V85HbymBLW_LogART_Pushing_the_Limit_of_Efficient_Logarithmi/figures/011_Table_3.jpg]]
*Table 3: Performance (PPL), GPU runtime, and memory usage of 3-bit weight quantization of LogART and existing PTQ methods on LLM models. (Calibration data from C4)*

### 主结果：视觉模型4比特量化

在CNN和视觉Transformer上，LogART同样取得最优精度，且运行时间具有竞争力。Table 4显示，ResNet18的4比特权重量化下，LogART的Top‑1准确率达到70.79%，比AdaRound（68.14%）和BRECQ（69.56%）分别高出2.65和1.23个百分点。MobileNetV2上LogART为71.62%，比FlexRound（70.12%）提高1.50个百分点。Table 5的ViT‑Base结果为85.02%，超越BRECQ（84.72%）和APHQ（84.59%）。值得注意的是，对数PTQ基线LogNet和SLogII在CNN上表现极弱（ResNet18仅31.53%和35.23%），而LogART通过OHS的网格优化和LLR的舍入学习，将精度从这一极低基线提升至SOTA水平，验证了方法在视觉领域的泛化能力。

![[assets/figures/papers/iclr26_0009_V85HbymBLW_LogART_Pushing_the_Limit_of_Efficient_Logarithmi/figures/012_Table_4.jpg]]
*Table 4: Comparison of top-1 accuracy on ImageNet and GPU runtime (in minutes) for different per-channel 4-bit weight PTQ methods on CNN models*

![[assets/figures/papers/iclr26_0009_V85HbymBLW_LogART_Pushing_the_Limit_of_Efficient_Logarithmi/figures/013_Table_5.jpg]]
*Table 5: Comparison of top-1 accuracy on ImageNet and GPU runtime (in minutes) for different per-channel 4-bit weight PTQ methods on vision transformer models*

### 消融实验：组件贡献与协同效应

**组件递增消融**（Table 1, Table 2）揭示了各模块的独立贡献与累进增益。以OPT‑125M 3比特为例：基线RTN对数PPL为170.64；加入动态基数搜索（DBS）后降至63.26；叠加缩放因子搜索（SFS）降至37.17；再引入非对称界（ABS）降至34.29；最终加入LLR降至31.15。每步增益均显著，且GPU内存保持恒定（2.9 GB），表明组件增加未引入额外存储开销。ResNet18 4比特的消融趋势一致：从31.53%（LogNet基线）逐步提升至70.79%，验证了DBS→SFS→ABS→LLR的递进设计逻辑。

**OHS与LLR的协同加速**（Table 7, Figure 5）是效率提升的关键瓶颈突破。无OHS时，LLR需2000次迭代才收敛，总运行时间4.00分钟，OPT‑125M PPL为36.27；启用OHS（ABS+SFS+DBS）后，LLR仅需500次迭代即收敛，总时间降至1.25分钟（加速3.2倍），PPL同时改善至31.15。Appendix B从理论上解释了这一协同：OHS最小化网格离散化误差ε₁，LLR在此基础上最小化舍入误差ε₂，总误差被界为(ε₁+ε₂)²；更优的网格使LLR的搜索空间更平滑，梯度优化更高效。

![[assets/figures/papers/iclr26_0009_V85HbymBLW_LogART_Pushing_the_Limit_of_Efficient_Logarithmi/figures/015_Table_7.jpg]]
*Table 7: Performance (PPL) and runtime comparison of LLR convergence with and without OHS*

**硬件近似吸收验证**（Table 6, Table 9, Table 10）证明HAF策略的有效性。采用K=2的SDE近似√2（即X+X/2的移位‑加法）时，ResNet18精度仅从70.79%轻微降至70.71%；若将近似噪声排除在优化之外（naive近似），精度骤降至68.75%。这证明OHS和LLR在优化过程中成功吸收了硬件近似误差，使实际部署的算术单元（AE）面积仅53.2 µm²、功耗3.45 µW，较线性PTQ代表设计缩减超过40%。

![[assets/figures/papers/iclr26_0009_V85HbymBLW_LogART_Pushing_the_Limit_of_Efficient_Logarithmi/figures/014_Table_6.jpg]]
*Table 6: HAF evaluation and AE comparison in terms of top-1 accuracy and hardware efficiency*

### 失败模式与局限性

尽管整体性能优异，LogART存在以下边界条件：当前仅支持权重量化，激活保持FP16，实际部署时需额外方案处理激活量化；非对称界依赖启发式计算（ABS），对极端非对称分布的适应性可能不足；多基数设计引入的解码器增加了有限的面积和功耗开销（虽仍显著优于线性基准）；所有实验在单张RTX 5090D上完成，更大规模模型（>13B）及实际芯片流片验证尚未开展。此外，2比特场景下的梯度优化稳定性和硬件方案有效性仍是开放问题。



## 定位与知识库关联

### 与基线方法的本质差异

LogART 与现有 PTQ 方法的根本分水岭在于**量化域的选择**与**误差分解粒度**。线性 PTQ 方法（GPTQ、BRECQ、AffineQuant、aespa、AdaRound、FlexRound）在均匀/仿射网格上进行舍入优化，其核心瓶颈在于线性网格对长尾权重分布的表示效率低下——极低位宽下大量码字浪费在稀疏的异常值区域，而密集的小值区域码字不足。LogART 将对数量化天然的非均匀密度匹配长尾分布，但其传统实现（LogNet、SLogII）受限于 RTN 舍入的不可学习性，无法感知任务损失。

LogART 的关键突破在于**将量化误差分解为两个可独立优化的项**：网格离散化误差（由 OHS 解决）和舍入误差（由 LLR 解决）。这一分解在 Appendix B.3 中有严格的数学支撑——总误差上界为 $(\varepsilon_1(\mathrm{OHS}) + \varepsilon_2(\mathrm{LLR}))^2$，其中 OHS 通过选择最优超参数 $\theta^*$ 最小化内在离散化误差，LLR 在已确定的网格上学习最优元素级舍入。这种"先定网格、后学舍入"的分治策略在现有 PTQ 方法中并无先例。

具体到技术栈的差异：

| 维度 | 线性 PTQ 基准 | 对数 PTQ 基准 | LogART |
|------|-------------|-------------|--------|
| 舍入策略 | RTN 或可学习舍入（AdaRound/FlexRound） | 仅 RTN | 对数域可学习舍入（LLR） |
| 基数 | 均匀步长 | 固定 base-2 或 base-√2 | 动态双基数，元素级分配 |
| 对称性 | 通过零点偏移实现非对称 | 固有对称 | 非对称码分配 |
| 异常值 | 基于绝对最大值 | 基于绝对最大值 | 搜索式自适应裁剪 |
| 硬件近似 | 无需近似 | 精确 √2 乘法（LUT） | SDE 近似 + 噪声吸收 |

### 适用边界与局限

**已验证的有效域：**

1. **模型类型**：LLM（OPT 125M–13B, LLaMA2/3 7B–8B）、CNN（ResNet18/50, MobileNetV2）、Vision Transformer（ViT-Small/Base, DeiT-Tiny/Base）均取得 SOTA 精度，证明方法对架构类型不敏感。
2. **位宽范围**：3-bit 权重（LLM）和 4-bit 权重（视觉模型）下已验证有效。更低比特（2-bit）的可行性尚未验证。
3. **量化粒度**：per-channel 权重量化，激活保持 FP16。联合权重-激活量化尚未实现。

**已知局限：**

1. **仅权重量化**：当前 LogART 未集成激活量化，实际部署时需额外方案处理激活。这是限制端到端效率的关键缺口。
2. **非对称分布的启发式局限**：ABS 组件使用简单的启发式公式计算非对称界偏移 $d_a$（Eq. 15），虽在实验中有效，但可能无法完美适应所有层的极端非对称分布。该点需要手动验证：原文未提供 ABS 在不同层类型上的单独消融。
3. **多基数解码器开销**：动态基数选择器 $B$ 和双基数解码器引入了额外的芯片面积和功耗。尽管 Table 6 显示 LogART AE 面积（53.2 µm²）和功耗（3.45 µW）仍显著优于线性 PTQ AE（>40% 缩减），但相较于纯 base-2 对数 AE 仍有增量开销。
4. **硬件验证仅限于仿真**：AE 设计在 45 nm 工艺下完成综合评估，未在真实芯片上流片验证。更大规模模型（>13B）的实测也受限于单卡 RTX 5090D 的计算资源。
5. **HAF 近似精度与硬件成本的权衡**：K=2 的 SDE 近似（$X + X/2$）在精度损失极小（ResNet18 从 70.79% 降至 70.71%）和硬件简化之间取得平衡，但更高近似精度（K>2）会引入更多移位-加法操作，其精度收益与硬件成本的边界关系未充分探索。

### 开放问题

1. **联合权重-激活量化**：如何将对数域可学习舍入扩展至激活值，同时保持 OHS 的搜索效率和 HAF 的硬件友好性，是 LogART 走向端到端部署的核心挑战。激活值分布与权重分布存在本质差异，动态基数和非对称策略可能需要重新设计。

2. **与结构化稀疏/蒸馏的协同**：LogART 的 OHS 超参数搜索框架是否可与结构化剪枝或知识蒸馏联合优化，形成统一的轻量化方案？OHS 本质上是在量化约束下搜索最优网格配置，若将稀疏掩码或蒸馏温度纳入搜索空间，可能产生叠加收益。

3. **极低位宽（2-bit）的可行性**：当前 3-bit 下 LLR 的梯度优化和 HAF 的移位-加法方案是否在 2-bit 下依然有效？码字数从 $2^{N-1}-1$ 骤减至 3（含零值），网格过于稀疏可能导致 OHS 搜索空间退化。

4. **真实芯片验证**：动态基数解码器的实际功耗与时序需要在物理芯片上测量。SDE 近似引入的移位-加法链在关键路径上的时序影响，以及多基数选择器 $B$ 的布线开销，都是仿真难以精确捕捉的因素。

5. **校准数据敏感性**：Table 1 显示 LogART 对校准数据域有一定敏感性（WikiText-2 vs C4 校准导致 PPL 差异约 0.7），虽然优于纯 RTN 对数方法，但相较于线性可学习舍入方法的域鲁棒性，该特性需要更系统的跨域评估。



## 原文 PDF

![[paperPDFs/ICLR_2026/LogART_Pushing_the_Limit_of_Efficient_Logarithmic_Post_Training_Quantization.pdf]]
