---
title: "A Physics-Inspired Optimizer: Velocity Regularized Adam"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Physics_Inspired_Optimizer_Velocity_Regularized_Adam.pdf
project_link: null
code_link: null
openreview_forum_id: 6BhduwrCp3
aliases:
- PIOVRA
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/non_convex
core_operator: "引入基于全局动量缓冲区范数的动态学习率门控：η_t = α₀/(1 + min(β₃‖v_t‖², α₁))，使学习率随速度自适应调整，高速度时段主动阻尼更新。"
primary_logic: "将四次速度惩罚项（受物理学中经典时间晶体和重夸克稳定性的启发）纳入动能函数，利用其导数衍生出的速度依赖学习率门控，在不牺牲Adam自适应逐参数缩放的条件下，全局抑制振荡，提升训练稳定性和收敛速度。"
claims:
- "VRAdam在自适应稳定边界具有全局均匀指数稳定性，理论证明通过共同二次Lyapunov函数构造（定理4.1）"
- "在图像分类、语言建模和生成式建模等多样任务中，VRAdam在所有任务上均超越AdamW等主流优化器"
- "实证分析表明VRAdam的锐度自适应且收敛更快，有效学习率动态调整以缓解边缘稳定振荡"
- "WikiText-2 (语言建模) 上 Test Loss = 6.00"
---

# A Physics-Inspired Optimizer: Velocity Regularized Adam

> [!tip] 核心洞察
> 将四次速度惩罚项（受物理学中经典时间晶体和重夸克稳定性的启发）纳入动能函数，利用其导数衍生出的速度依赖学习率门控，在不牺牲Adam自适应逐参数缩放的条件下，全局抑制振荡，提升训练稳定性和收敛速度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 受物理学启发的优化器：速度正则化Adam |
| 英文题名 | A Physics-Inspired Optimizer: Velocity Regularized Adam |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=6BhduwrCp3) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/non_convex |
| Method | VRAdam |
| Dataset | WikiText-2 (语言建模), CIFAR-10 (图像分类), GridWorld (流匹配), GPT-2 训练 |

> [!tip] 效果简介
> - WikiText-2 (语言建模) 上，Test Loss 为 6.00，对比 6.13 (AdamW)，变化 ↓0.13。
> - CIFAR-10 (图像分类) 上，Test Loss 为 0.469，对比 0.497 (AdamW)，变化 ↓0.028。
> - GridWorld (流匹配) 上，Test Loss 为 1.33，对比 2.01 (AdamW)，变化 ↓0.68。

## 概要

自适应优化器（如AdamW）在训练深度网络时，常陷入**自适应稳定边界（Adaptive Edge of Stability, AEoS）**区域。该区域内，动量缓冲区的高速振荡导致损失函数非单调波动，最终收敛速度减慢。本文提出**VRAdam**（Velocity Regularized Adam），通过受物理学启发的速度正则化机制解决这一问题。

**核心思路**：将四次速度惩罚项 $\frac{\beta_3}{4}\|v\|^4$ 纳入动能函数——这一形式受经典时间晶体和重夸克稳定性的物理原理启发。由Euler-Lagrange方程导出**动态学习率门控**：

$$\eta_t = \frac{\alpha_0}{1 + \min(\beta_3 \|v_t\|^2, \alpha_1)}$$

该门控使学习率随全局动量缓冲区范数自适应调整：高速度时段主动阻尼更新，稳定后恢复最大学习率。这一机制在不牺牲Adam逐参数自适应缩放的前提下，实现全局振荡抑制。

**理论保证**：通过构造共同二次Lyapunov函数，证明VRAdam在自适应稳定边界具有**全局均匀指数稳定性**（定理4.1），稳定性条件为 $\alpha_0 L < \frac{2(1+\beta)}{1-\beta}$。

**主要实证结果**：在图像分类（CIFAR-10）、语言建模（WikiText-2）和生成式建模（流匹配）等多样任务中，VRAdam在所有任务上均超越AdamW等主流优化器。例如，WikiText-2测试损失从6.13降至6.00，CIFAR-10测试损失从0.497降至0.469。在GPT-2训练和LLaMA-2-7B QLoRA微调等大规模实验中，VRAdam同样取得一致的性能提升。

VRAdam额外引入两个超参数（$\beta_3$控制速度惩罚强度，$\alpha_1$控制最小学习率），虽增加调参负担，但实验表明通过标准网格搜索即可有效调优。



### 自适应优化器的边缘稳定困境

现代深度学习训练中，自适应优化器（如AdamW）已成为事实标准。然而，这类方法面临一个深层瓶颈：在训练过程中，优化器常被推入**自适应稳定边界（Adaptive Edge of Stability, AEoS）**区域。在此区域内，动量缓冲区积累的高速振荡导致损失函数出现非单调波动——训练并非平滑收敛，而是反复在稳定边界附近震荡，最终拖慢收敛速度。

这一现象的物理图景是：标准动量仅包含二次动能项 $T(v) = \frac{m}{2}\|v\|^2$，缺乏对高速运动的有效阻尼机制。当参数更新幅度过大时，动量持续累积而不受抑制，使优化器反复越过稳定阈值。现有方法如SAM（Sharpness-Aware Minimization）试图通过显式惩罚锐度来缓解此问题，但其机制与动量振荡的抑制是正交的，无法从根本上解决AEoS区域的边缘稳定振荡。

### 现有方法的缺口

主流自适应优化器的学习率调度策略存在结构性局限：

- **固定或计划衰减的学习率**（如AdamW的余弦退火）：学习率变化完全由预设计划决定，与训练过程中实际发生的动量振荡无关。当优化器进入AEoS区域时，学习率无法感知并响应速度的异常增长。
- **逐参数自适应缩放**（如Adam的二阶矩预处理）：虽能对不同参数的梯度进行差异化缩放，但无法在全局层面抑制动量缓冲区整体的振荡趋势。

换言之，现有方法缺少一个**全局反馈控制回路**——能够根据动量缓冲区的实时状态动态调整学习率，在高速振荡时主动阻尼，在稳定时释放全部更新能力。

### 物理学启发的动机

本文的动机源于物理学中两个经典现象：

1. **经典时间晶体与重夸克稳定性**：在非相对论量子色动力学（NRQCD）中，重夸克的能量展开为 $E_{\text{NRQCD}}(p) = m + \frac{p^2}{2m} - \frac{p^4}{8m^3} + \mathcal{O}(p^6/m^5)$。其中的四次项 $-p^4/(8m^3)$ 提供了对高速运动的天然阻尼，使得系统在有限动量处达到最大能量，从而形成稳定边界。

2. **四次动能函数的动力学**：若将动能函数从纯二次推广为 $T_{\text{VRAdam}}(v) = \frac{m}{2}\|v\|^2 + \frac{\beta_3}{4}\|v\|^4$，通过欧拉-拉格朗日方程可导出运动方程 $\frac{d}{dt}[(m + \beta_3\|v\|^2)v] = -\nabla L_{\text{Loss}}(x)$。该方程揭示了一个关键机制：当速度范数增大时，有效质量 $m + \beta_3\|v\|^2$ 随之增加，自然抑制加速度，形成**速度依赖的自适应阻尼**。

这一物理机制直接对应优化器中的一个可操作设计：将四次速度惩罚项的导数转化为动态学习率门控，使得学习率随动量缓冲区范数自适应缩放——高速时降低学习率以稳定训练，低速时恢复最大学习率以快速收敛。这正是VRAdam的核心动机：在不牺牲Adam逐参数自适应缩放能力的前提下，引入全局速度正则化，从物理层面抑制AEoS振荡。



## 核心方法与创新机理

VRAdam 的核心创新在于将物理学中经典时间晶体和重夸克稳定性理论引入优化器设计，通过**改进动能函数**并由此衍生出**速度依赖的动态学习率门控**，在不牺牲 Adam 自适应逐参数缩放的条件下，全局抑制自适应稳定边界（AEoS）区域的动量振荡。

### 关键改进槽位

| 改进槽位 | 基准方法（AdamW） | VRAdam | 证据锚点 |
|---------|-----------------|--------|---------|
| 学习率调制 | 固定或按计划衰减的常数学习率 $\eta$ | 基于全局动量缓冲区范数的动态门控：$\eta_t = \frac{\alpha_0}{1 + \min(\beta_3 \|v_t\|^2, \alpha_1)}$ | Algorithm 1, line 7 |
| 动能函数形式 | 标准二次动能 $\frac{m}{2}\|v\|^2$ | 引入四次速度惩罚项：$T_{\mathrm{VRAdam}}(v) = \frac{m}{2}\|v\|^2 + \frac{\beta_3}{4}\|v\|^4$ | Section 3, Eqn (3) |

### 物理机制与因果链路

**瓶颈识别**：自适应优化器（如 AdamW）在训练深度网络时，动量缓冲区的高速振荡导致损失函数非单调波动，系统陷入自适应稳定边界（AEoS）区域，最终收敛速度减慢。

**因果调节**：从包含四次速度惩罚的 Lagrangian 出发：

$$\mathcal{L}(x, v) = \frac{m}{2} v^2 + \frac{\beta_3}{4} v^4 - V(x)$$

通过 Euler-Lagrange 方程导出连续时间动力学：

$$\frac{d}{dt}[(m + \beta_3 \|v\|^2)v] = -\nabla L_{\mathrm{Loss}}(x)$$

该方程揭示了一个关键机制：当速度范数 $\|v\|$ 增大时，有效质量 $m + \beta_3\|v\|^2$ 同步增大，从而**主动阻尼高速度时段的参数更新**。这一连续时间动力学被离散化为速度依赖的学习率门控 $\eta_t = \alpha_0/(1 + \min(\beta_3\|v_t\|^2, \alpha_1))$，其中 $\alpha_0$ 为最大学习率，$\alpha_1$ 控制最小学习率下限，$\beta_3$ 为速度惩罚强度。

**效果机制**：该门控在训练初期自动降低学习率以稳定优化轨迹，随后随速度范数自然衰减而提升至最大学习率，实现快速收敛（Figure 2d）。理论分析表明，在二次模型上 VRAdam 具有全局均匀指数稳定性，通过共同二次 Lyapunov 函数构造得到严格证明（Theorem 4.1），稳定性条件为 $\alpha_0 L < \frac{2(1+\beta)}{1-\beta}$。

### 与逐参数缩放的兼容性

VRAdam 的学习率门控是**全局标量**，对所有权重方向施加一致的缩放因子。这与 Adam 的逐参数二阶矩预处理 $1/\sqrt{m_t}$ 正交——前者负责全局稳定性调控，后者保留自适应梯度缩放的表达能力。Theorem 4.1 的 CQLF 构造保证了在任意标量门控切换下收缩性质仍然成立，避免了逐方向门控可能引入的切换各向异性不稳定性（Section 4.3）。



![[assets/figures/papers/iclr26_0010_6BhduwrCp3_A_Physics-Inspired_Optimizer_Velocity_Regularize/figures/005_Figure_2.jpg]]
*Figure 2: (a) Training loss curves for VRAdam, Adam, and SAM (Foret et al., 2021) of ResNet-32 on CIFAR-10 (b) training accuracy curves (c) plot of maximal eigenvalues of the loss Hessian (d) effective learning rate during training. Hyperparameters for these plots are provided in Appendix E.4*

![[assets/figures/papers/iclr26_0010_6BhduwrCp3_A_Physics-Inspired_Optimizer_Velocity_Regularize/figures/001_Figure_1.jpg]]
*Figure 1: the dynamic learning rate $\eta _ { t } = \alpha _ { 0 }$ / ( 1 + $\operatorname$* { m i n } ( $\beta _ { 3 } \lvert \lvert v _ { t } \lvert \lvert ^ { 2 } , \alpha _ { 1 }$ ) ) for timestep t for VRAdam, where $\alpha _ { 0 }$ and $\alpha _ { 1 }$ control the maximal and minimal LR respectively, and $\beta _ { 3 }$ controls the strength of the velocity penalty. This is inspired by the bound introduced to $\overline { { v ^ { 2 } } }$ in physical setting as discussed in Appendix A. The parameterization of LR, compared to the physically derived one, clips the velocity to avoid getting stuck if gradients and therefore velocity become large. Weight decay is applied in the traditional manner. An implementati...

VRAdam 在标准自适应优化器（AdamW）的动量框架之上，引入了一个受物理学启发的**全局动态学习率门控**模块，形成“动量估计 → 二阶矩估计 → 速度正则化门控 → 偏差校正 → 参数更新”的完整 pipeline。各模块之间的关系和输入输出流如下：

### Pipeline 模块关系

1. **动量估计 $v_t$**：对当前梯度 $g_t$ 进行指数移动平均（EMA），生成一阶动量缓冲区。这是整个门控机制的核心输入——速度范数 $\|v_t\|$ 直接决定后续学习率的缩放强度。

2. **二阶矩估计 $m_t$**：对梯度平方进行 EMA，生成逐参数的自适应预处理因子。该模块与标准 Adam 一致，为参数更新提供逐坐标缩放。

3. **动态学习率门控 $\eta_t$**：这是 VRAdam 的核心创新模块。它接收动量缓冲区的全局范数 $\|v_t\|$，通过速度正则化公式计算当前步的学习率：
   $$\eta_t = \frac{\alpha_0}{1 + \min(\beta_3 \|v_t\|^2, \alpha_1)}$$
   其中 $\alpha_0$ 为最大学习率，$\beta_3$ 控制速度惩罚强度，$\alpha_1$ 为学习率下限的截断参数。当动量高速振荡时（$\|v_t\|$ 大），$\eta_t$ 自动降低以阻尼更新；当梯度方向一致时（$\|v_t\|$ 适中），$\eta_t$ 回升至接近 $\alpha_0$，实现快速收敛。

4. **偏差校正**：对 $v_t$ 和 $m_t$ 进行无偏初始化修正，消除早期迭代的零初始化偏差。

5. **参数更新（含解耦权重衰减）**：将动态学习率 $\eta_t$、偏差校正后的动量方向 $\hat{v}_t$、二阶矩预处理因子 $1/(\sqrt{\hat{m}_t} + \epsilon)$ 以及解耦权重衰减组合，完成参数 $\theta_t$ 的更新。

### 输入输出流

- **输入**：当前参数 $\theta_{t-1}$、随机梯度 $g_t = \nabla f(\theta_{t-1})$、上一时刻动量 $v_{t-1}$ 和二阶矩 $m_{t-1}$。
- **中间变量**：动量 $v_t$（流向门控模块和参数更新）、二阶矩 $m_t$（流向参数更新）、动态学习率 $\eta_t$（流向参数更新）。
- **输出**：更新后的参数 $\theta_t$、更新后的动量 $v_t$ 和二阶矩 $m_t$（作为下一迭代的状态）。

### 关键设计决策

- **全局标量门控而非逐层/逐参数门控**：门控模块使用整个动量缓冲区的全局范数 $\|v_t\|$ 产生单一标量学习率 $\eta_t$。这一设计避免了逐参数门控可能引入的“切换各向异性”不稳定性——当不同方向的学习率异步变化时，会破坏共同二次 Lyapunov 函数的存在性。全局标量缩放保证了所有方向被一致缩放，从而在理论上获得全局均匀指数稳定性（定理 4.1）。

- **门控与自适应预处理的解耦**：动态学习率 $\eta_t$ 作用于全局尺度，而 Adam 的二阶矩预处理 $1/(\sqrt{\hat{m}_t} + \epsilon)$ 作用于逐参数尺度。两者互不干扰：速度正则化抑制全局振荡，自适应预处理处理各向异性曲率。

- **计算开销**：门控模块仅需计算一次全局范数和一次标量除法，额外开销可忽略。论文报告 GPT-2 训练中 VRAdam 与 AdamW 的时间几乎相同（48,522s vs 48,550s，Table 2），验证了这一点。

### 物理动机的模块化映射

门控公式来源于对动能函数的修正。标准动量基于二次动能 $T(v) = \frac{m}{2}\|v\|^2$，而 VRAdam 引入四次速度惩罚项：
$$T_{\mathrm{VRAdam}}(v) = \frac{m}{2}\|v\|^2 + \frac{\beta_3}{4}\|v\|^4$$
通过 Euler-Lagrange 方程导出连续时间动力学 $\frac{d}{dt}[(m + \beta_3\|v\|^2)v] = -\nabla L$，其离散化自然产生了速度依赖的学习率缩放。这一物理对应为门控设计提供了原则性依据，而非启发式技巧。



### 核心模块

VRAdam 在标准 Adam 框架上引入一个关键模块——**动态学习率门控**，其余模块（动量估计、二阶矩估计、偏差校正、解耦权重衰减）与 AdamW 保持一致。各模块职责如下：

| 模块 | 角色 | 证据锚点 |
|------|------|----------|
| 动量估计 $v_t$ | 梯度的指数移动平均，作为“速度”的离散近似 | Algorithm 1, line 5 |
| 二阶矩估计 $m_t$ | 梯度平方的指数移动平均，提供逐参数自适应缩放 | Algorithm 1, line 6 |
| **动态学习率门控 $\eta_t$** | 根据全局速度范数动态缩放学习率，实现全局阻尼 | Algorithm 1, line 7 |
| 偏差校正 | 对 $v_t$ 和 $m_t$ 进行无偏初始化修正 | Algorithm 1, lines 8-9 |
| 参数更新（含解耦权重衰减） | 应用动态学习率、动量方向和二阶矩预处理的参数更新 | Algorithm 1, line 10 |

其中，动态学习率门控是 VRAdam 的核心创新。该模块以全局动量缓冲区的范数 $\|v_t\|$ 为输入，输出缩放后的有效学习率 $\eta_t$，使优化器在速度较大时主动降低步长，抑制自适应稳定边界（AEoS）区域的振荡。

### 关键公式推导

#### 1. 改进的动能函数

VRAdam 的物理启发出发点是将标准动量中的二次动能替换为包含四次惩罚项的动能函数：

$$T_{\mathrm{VRAdam}}(v) = \frac{m}{2} \|v\|^2 + \frac{\beta_3}{4} \|v\|^4$$

其中 $m$ 为质量参数，$\beta_3$ 控制四次惩罚的强度。该形式受物理学中经典时间晶体和重夸克有效理论（NRQCD）的启发：在 NRQCD 中，相对论能量展开为 $E_{\mathrm{NRQCD}}(p) = m + \frac{p^2}{2m} - \frac{p^4}{8m^3} + \mathcal{O}\left(\frac{p^6}{m^5}\right)$，四次项提供负贡献以抵消高阶发散，从而稳定动力学。VRAdam 的四次动能项在优化动力学中扮演类似角色——当速度（动量）过大时提供额外阻尼。

#### 2. Euler–Lagrange 运动方程

将动能函数与势能 $V(x)$（对应损失函数 $L_{\mathrm{Loss}}$）结合，构造 Lagrangian：

$$\mathcal{L}(x, v) = \frac{m}{2} v^2 + \frac{\beta_3}{4} v^4 - V(x)$$

通过 Euler–Lagrange 方程 $\frac{d}{dt}\frac{\partial \mathcal{L}}{\partial v} = \frac{\partial \mathcal{L}}{\partial x}$ 导出连续时间动力学：

$$\frac{d}{dt}[(m + \beta_3 \|v\|^2)v] = -\nabla L_{\mathrm{Loss}}(x)$$

该方程揭示核心机制：有效质量 $m + \beta_3 \|v\|^2$ 随速度增大而增大，使得系统在高速区域惯性增强、加速度降低，从而自然抑制振荡。

#### 3. 动态学习率门控

将连续时间动力学离散化并嵌入 Adam 框架，得到 VRAdam 的核心公式——速度依赖的动态学习率：

$$\eta_t = \frac{\alpha_0}{1 + \min(\beta_3 \|v_t\|^2, \alpha_1)}$$

**变量含义**：
- $\alpha_0$：最大学习率，控制学习率的上界
- $\beta_3$：速度惩罚强度，控制门控对速度范数的敏感度
- $\|v_t\|^2$：全局动量缓冲区在步 $t$ 的平方范数
- $\alpha_1$：截断阈值，限制学习率的最小值（防止过度衰减），确保 $\eta_t \geq \alpha_0/(1+\alpha_1)$

**工作机制**：当 $\|v_t\|$ 较大（优化处于陡峭区域或振荡阶段）时，分母增大，$\eta_t$ 自动降低，主动阻尼更新；当 $\|v_t\|$ 较小时，$\eta_t$ 接近 $\alpha_0$，允许快速收敛。$\min(\cdot, \alpha_1)$ 截断保证学习率不会无限制衰减。

#### 4. 与标准 Adam 的关系

VRAdam 的完整更新流程可概括为：

$$v_t = \beta_1 v_{t-1} + (1-\beta_1) \nabla f(\theta_{t-1})$$
$$m_t = \beta_2 m_{t-1} + (1-\beta_2) [\nabla f(\theta_{t-1})]^2$$
$$\eta_t = \frac{\alpha_0}{1 + \min(\beta_3 \|v_t\|^2, \alpha_1)}$$
$$\theta_t = \theta_{t-1} - \eta_t \frac{\hat{v}_t}{\sqrt{\hat{m}_t} + \epsilon} - \lambda \eta_t \theta_{t-1}$$

其中 $\hat{v}_t$、$\hat{m}_t$ 为偏差校正后的估计，$\lambda$ 为解耦权重衰减系数。与 AdamW 相比，唯一的结构性差异在于 $\eta_t$ 从固定值变为速度依赖的动态值，其余组件完全兼容。



## 实验与关键发现

### 主要结果

VRAdam 在语言建模、图像分类和生成式建模三类任务上全面超越主流优化器。Table 1 汇总了 WikiText-2、CIFAR-10 和 GridWorld 流匹配的测试损失对比：VRAdam 在 WikiText-2 上达到 6.00，较 AdamW 的 6.13 降低 0.13；CIFAR-10 测试损失 0.469，较 AdamW 的 0.497 降低 0.028；GridWorld 流匹配测试损失 1.33，较 AdamW 的 2.01 降低 0.68。值得注意的是，SGD+Nesterov 和 RMSProp 在 WikiText-2 上产生 NaN，突显 VRAdam 的数值稳定性优势。

![[assets/figures/papers/iclr26_0010_6BhduwrCp3_A_Physics-Inspired_Optimizer_Velocity_Regularize/figures/006_Table_1.jpg]]
*Table 1: Comparison of optimizer performance across three tasks: language modeling on WikiText-2, image classification on CIFAR-10, and flow matching on GridWorld*

在更大规模的语言模型训练中，VRAdam 同样保持优势。Table 2 显示 GPT-2 训练中 VRAdam 验证损失为 3.447，低于 AdamW 的 3.511，且训练时间相当（VRAdam 48522.40s vs AdamW 48549.56s）。Table 3 的 LLM 微调基准进一步验证：LLaMA-2-7B 的 QLoRA 微调（OASST2）中 VRAdam 困惑度 3.55，低于 AdamW 的 3.84；GPT-2 Large 全参微调（GSM8K）中 VRAdam 困惑度 3.53，低于 AdamW 的 4.12，降幅达 0.59。

![[assets/figures/papers/iclr26_0010_6BhduwrCp3_A_Physics-Inspired_Optimizer_Velocity_Regularize/figures/007_Table_2.jpg]]
*Table 2: Comparison of training time and validation loss for GPT-2 training*

![[assets/figures/papers/iclr26_0010_6BhduwrCp3_A_Physics-Inspired_Optimizer_Velocity_Regularize/figures/008_Table_3.jpg]]
*Table 3: Additional LLM benchmarks comparing AdamW, VRAdam, and Lion (Chen et al., 2023) in challenging fine-tuning regimes for OASST2 (instruction following) and GSM8K (math reasoning)*

### 收敛加速与边缘稳定性实证

Figure 2 从训练动力学角度揭示了 VRAdam 的工作机制。Figure 2(a) 和 2(b) 显示，在 CIFAR-10 上训练 ResNet-32 时，VRAdam 的训练损失下降和准确率提升均快于 Adam 和 SAM。Figure 2(c) 的损失 Hessian 最大特征值曲线表明，VRAdam 保持锐度自适应（adaptable sharpness），未陷入僵化的边缘稳定状态。Figure 2(d) 的动态有效学习率曲线揭示了关键因果机制：训练初期 VRAdam 自动降低学习率以平稳启动，随后提升至最大学习率以加速收敛——这正是速度门控 $ \eta_t = \alpha_0/(1 + \min(\beta_3\|v_t\|^2, \alpha_1)) $ 在起作用：高速度时段主动阻尼，低速度时段释放更新能力。

### 消融实验

Table 4 的动能幂次消融实验验证了四次速度惩罚的最优性。在 CIFAR-10 上测试幂次 $k=2$ 至 $6$（对应学习率门控中 $\|v_t\|^k$ 的不同阶数），$k=2$（即四次动能项）取得最低测试损失 0.932，而 $k=3$ 的测试损失显著升至 1.155，表明更高阶惩罚过度抑制了有效更新。这一结果与理论分析一致：四次项在 NRQCD 有效场论中恰好抵消相对论展开的四阶项，提供恰到好处的阻尼。

![[assets/figures/papers/iclr26_0010_6BhduwrCp3_A_Physics-Inspired_Optimizer_Velocity_Regularize/figures/009_Table_4.jpg]]
*Table 4: Test Loss on CIFAR-10 for different kinetic energies*

### 超参数调优与公平性

所有对比实验的超参数均通过等计算预算的网格/随机搜索调优。Table 7 展示了 CNN 综合搜索中 VRAdam 的最优配置：$\alpha_0=0.0846$、$\beta_3=1.015$、$\alpha_1=29$。Table 6 列出了固定超参数（100 轮、批大小 1024、WarmupCosineAnnealing 调度器含 5 轮预热），确保各优化器在可比条件下评估。

### 局限性与失败模式

尽管 VRAdam 在各项基准上表现优异，仍存在若干限制。首先，引入 $\beta_3$ 和 $\alpha_1$ 两个额外超参数增加了调参负担，尽管搜索结果表明其最优值相对稳定。其次，速度正则化门控依赖全局动量缓冲区范数，无法对不同层或参数组进行差异化阻尼，在高度异构的架构上可能限制其适用性。此外，自适应稳定边界现象的完整理论理解仍有缺口，泛化保证尚未从速度阻尼机制严格导出。



## 定位与知识库关联

### 在自适应优化器谱系中的位置

VRAdam 属于**自适应动量优化器家族**，其直接前身是 Adam/AdamW。与标准 AdamW 的核心差异在于学习率调制机制：AdamW 使用固定或按计划衰减的学习率 $\eta$，而 VRAdam 引入基于全局动量缓冲区范数的**动态门控学习率** $\eta_t = \alpha_0/(1 + \min(\beta_3\|v_t\|^2, \alpha_1))$。这一改动不触及 Adam 的逐参数自适应预处理结构（二阶矩 $m_t$ 的逐坐标缩放），而是在全局层面施加速度依赖的阻尼。

从方法论谱系看，VRAdam 与以下工作形成对比或互补关系：

| 方法 | 关系 | 关键差异 |
|------|------|----------|
| **AdamW** | 直接基准 | 解耦权重衰减 + 固定学习率调度 vs. 速度门控动态学习率 |
| **SAM (Sharpness-Aware Minimization)** | 并行关注点 | SAM 通过梯度扰动显式惩罚锐度；VRAdam 通过速度阻尼隐式抑制边沿稳定振荡。实证中 VRAdam 训练损失和锐度自适应均优于 SAM（Figure 2） |
| **RAdam** | 同类变体 | RAdam 通过整流项在训练初期稳定自适应学习率；VRAdam 通过速度范数在整个训练过程中动态调整，覆盖范围更广 |
| **Lion** | 近期对比 | Lion 使用符号梯度 + 动量的简化更新；VRAdam 保留二阶矩预处理，在 QLoRA 微调 LLaMA-2-7B 和 GPT-2 Large 全微调上均取得更低困惑度（Table 3） |
| **SGD+Nesterov / RMSProp** | 经典基准 | 在 WikiText-2 上部分方法产生 NaN，突显 VRAdam 的数值稳定性优势（Table 1） |

### 物理启发的理论根基

VRAdam 的核心创新——四次速度惩罚项——直接借鉴了物理学中**非相对论量子色动力学（NRQCD）的重夸克有效理论**。在 NRQCD 中，重夸克的能量展开为 $E_{\mathrm{NRQCD}}(p) = m + \frac{p^2}{2m} - \frac{p^4}{8m^3} + \mathcal{O}(\frac{1}{m^5})$，其中四次项提供负贡献以抵消相对论展开中的高阶修正。VRAdam 将这一结构迁移至动能函数 $T_{\mathrm{VRAdam}}(v) = \frac{m}{2}\|v\|^2 + \frac{\beta_3}{4}\|v\|^4$，通过 Euler-Lagrange 方程导出速度依赖的有效质量 $m + \beta_3\|v\|^2$，进而转化为学习率门控。

这一物理类比的深层含义是：当动量缓冲区范数 $\|v_t\|$ 增大（对应优化轨迹高速振荡），有效惯性增大，学习率自动降低以阻尼振荡；当轨迹趋于平稳，学习率恢复至接近 $\alpha_0$ 以加速收敛。理论分析（Theorem 4.1）通过构造共同二次 Lyapunov 函数证明了该机制在二次模型上的**全局均匀指数稳定性**，稳定性条件为 $\alpha_0 L < \frac{2(1+\beta)}{1-\beta}$。

### 适用边界

VRAdam 在以下场景表现出显著优势：

1. **自适应稳定边界（AEoS）区域**：当 AdamW 等优化器陷入边沿稳定振荡时，VRAdam 的速度门控主动提升瞬时稳定性阈值 $L_{\mathrm{EoS}}(t) = \frac{2(1+\beta_1)}{(1-\beta_1)\alpha_0}(1 + \min\{\beta_3\|v_t\|^2, \alpha_1\})$，有效扩展稳定区域。
2. **异构任务**：在语言建模（WikiText-2、GPT-2）、图像分类（CIFAR-10）、流匹配（GridWorld）、LLM 微调（QLoRA LLaMA-2-7B、GPT-2 Large）上均一致超越 AdamW（Table 1-3），表明方法具有跨任务鲁棒性。
3. **训练初期稳定性**：Figure 2(d) 显示 VRAdam 在训练初期自动降低有效学习率以稳定优化，随后提升至最大学习率以加速收敛，无需手动预热调度。

### 已知局限

1. **额外超参数负担**：引入 $\beta_3$（速度惩罚强度）和 $\alpha_1$（最小学习率控制），虽然可通过网格/随机搜索调优（附录 Table 7、10），但增加了调参成本。
2. **全局门控的粒度限制**：$\eta_t$ 依赖全局动量范数 $\|v_t\|^2$，对所有参数施加相同的缩放因子，无法对不同层或参数组进行差异化阻尼。在异构架构（如部分层梯度尺度差异极大）中，全局门控可能次优。
3. **计算开销**：每步需计算动量缓冲区范数并更新学习率，在极大规模模型中可能引入可感知的额外开销（论文中 GPT-2 训练时间与 AdamW 相当，但更大规模场景需进一步验证）。
4. **理论缺口**：自适应稳定边界现象的完整理解与泛化关系仍不明确；速度阻尼机制是否可导出泛化保证尚未解决。

### 开放问题

- **完全消除 AEoS 的可能性**：速度门控提升了稳定性阈值，但边沿稳定区域是否可通过更复杂的反馈控制（如层级门控、二阶信息融合）完全消除？
- **与无调度方法的结合**：VRAdam 的动态学习率是否可与 Schedule-Free 等插值平均方案协同，进一步减少超参数？
- **四次惩罚的推广**：消融实验（Table 4）显示二次（四次速度惩罚）在 CIFAR-10 上表现最优（测试损失 0.932），三次幂次表现最差（1.155）。四次结构是否可推广至高阶张量优化或二阶方法（如 K-FAC）？
- **非平稳场景的行为**：在持续学习、分布偏移等极端非平稳目标中，速度门控的动态学习率是否会导致灾难性遗忘或不稳定阻尼？
- **泛化理论**：能否从速度阻尼机制导出平坦极小值的偏好性，从而建立与泛化性能的形式化联系？



## 原文 PDF

![[paperPDFs/ICLR_2026/A_Physics_Inspired_Optimizer_Velocity_Regularized_Adam.pdf]]
