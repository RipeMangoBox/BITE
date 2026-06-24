---
title: "EventGait: Towards Robust Gait Recognition with Event Streams"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EventGait_Towards_Robust_Gait_Recognition_with_Event_Streams.pdf
project_link: null
code_link: "https://github.com/QUEAHREN/EventGait"
aliases:
- EventGait
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过双流架构分别保留短时动态（脉冲神经网络与混合专家）和长时静态形状（跨模态结构对齐蒸馏视觉基础模型先验），使模型能够自适应地处理不同光照和运动速度下的复杂事件模式。
primary_logic: 鲁棒的事件步态识别需要同时保留事件流的高时间分辨率动态信息和通过大模型蒸馏获得的密集空间结构先验，二者互补才能实现光照鲁棒且身份判别的步态表征。
claims:
- 在低光夜间场景下，EventGait相比基于RGB的步态识别方法有极大优势，SUSTech1K-E夜间（NT）Rank-1准确率提升达37.3%。
- EventGait在事件输入下相较采用相同骨干的GaitBase提升+16.7%总体准确率，验证了双流设计与脉冲神经元的有效性。
- 消融实验表明静态流和动态流互补，单独使用任一流性能均明显低于双流融合模型。
- SUSTech1K-E 上 Rank-1 Overall Accuracy (%) = 92.8
---

# EventGait: Towards Robust Gait Recognition with Event Streams

> [!tip] 核心洞察
> 鲁棒的事件步态识别需要同时保留事件流的高时间分辨率动态信息和通过大模型蒸馏获得的密集空间结构先验，二者互补才能实现光照鲁棒且身份判别的步态表征。

| 字段 | 内容 |
|------|------|
| 中文题名 | EventGait：基于事件流的鲁棒步态识别 |
| 英文题名 | EventGait: Towards Robust Gait Recognition with Event Streams |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.22139) · [Code](https://github.com/QUEAHREN/EventGait) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | EventGait |
| Dataset | SUSTech1K-E, CCGR-Mini-E, DVS128-Gait |

> [!tip] 效果简介
> - SUSTech1K-E 上，Rank-1 Overall Accuracy (%) 92.8 vs EVGait 65.4 (+27.4)。
> - SUSTech1K-E (Low Light) 上，Rank-1 Overall Accuracy (%) 83.2 vs GaitBase (Event Input) 23.6 (+59.6)。
> - CCGR-Mini-E 上，Rank-1 Accuracy (%) 40.3 vs GaitBase (Event Input) 9.7 (+30.6)。

## 概述

**问题瓶颈**：现有事件步态识别方法（如 **EVGait**，CVPR 2019）将异步事件流聚合为长时间窗口的稀疏事件图像，再送入标准 CNN 处理。这一范式丢失了事件相机最核心的优势——高时间分辨率的细粒度动态信息，同时稀疏的事件表示也缺乏密集的空间结构先验，导致模型在复杂光照和运动条件下难以提取身份判别性步态特征。

**核心洞察**：鲁棒的事件步态识别需要**同时保留**两个互补的信息维度：（1）事件流的高时间分辨率动态模式；（2）通过大模型蒸馏获得的密集空间结构先验。二者互补才能实现光照鲁棒且身份判别的步态表征。

**方法定位**：EventGait 提出一个端到端的**双流架构**，分别建模运动与形状。动态运动流采用**混合脉冲专家（Mixture of Spiking Experts, MoSE）**，利用具有不同膜时间常数的脉冲神经元自适应感知不同光照和运动速度下的复杂事件模式；静态形状流通过**跨模态结构对齐（Cross-modal Structure Alignment, CroSA）**，从预训练视觉基础模型 DINOv2 中蒸馏密集结构先验，弥补事件数据的空间稀疏性。

**主要结果**：
- 在合成事件数据集 SUSTech1K-E 上，EventGait 达到 **92.8%** Rank-1 总体准确率，相较基于事件的基线方法 EVGait（65.4%）提升 **+27.4%**，相较采用相同骨干的 GaitBase（事件输入）提升 **+16.7%**。
- 在低光夜间场景下优势尤为显著：SUSTech1K-E 夜间（NT）Rank-1 准确率提升达 **+37.3%**，低光总体准确率从 GaitBase 的 23.6% 跃升至 **83.2%**（+59.6%）。
- 消融实验证实静态流与动态流具有互补作用，移除任一流均导致性能显著下降；MoSE 中采用 3 个专家在精度与效率之间达到最佳平衡。

**局限与展望**：当前评估主要依赖合成事件数据集，合成数据与真实事件数据之间的域差异可能使结果偏向理想化分布；模型在真实场景下的泛化能力尚需更多真实世界事件步态数据验证。此外，脉冲神经网络在通用硬件上的推理效率仍有待优化，未来可探索事件与 RGB/LiDAR 的多模态融合以进一步提升极端条件下的鲁棒性。

## 背景与动机

步态识别因其非侵入性和远距离感知优势，在安防监控与身份认证领域具有重要应用价值。然而，当前主流方法严重依赖RGB相机采集的剪影序列，在低光、夜间等复杂光照条件下，RGB成像质量急剧退化，导致步态表征丧失判别力，系统性能大幅下降。如图1所示，事件相机凭借其高动态范围（>120 dB）和微秒级时间分辨率，能够在极端光照变化下稳定输出异步事件流，为全天候步态识别提供了新的感知模态。

尽管事件相机在数据采集端展现出显著优势，现有的事件步态识别方法却未能充分释放其潜力。以 **EVGait**（CVPR 2019）为代表的首批工作，将长时间窗口内的事件流聚合成稀疏的事件图像，再交由标准CNN或GNN处理。这一范式存在一个核心瓶颈：长时间聚合操作抹去了事件流中固有的细粒度时间动态，同时产生的稀疏空间表示使标准CNN难以有效编码密集的结构信息。简言之，现有方法在“时间分辨率保留”与“空间结构提取”之间陷入两难——保留短时窗口则空间稀疏难以学习，扩大聚合窗口则丧失动态细节。

这一瓶颈的因果根源在于：事件流本质上是一种高时间分辨率、空间稀疏的异步信号，而传统CNN架构设计之初面向的是空间密集、帧率固定的同步图像。直接套用CNN处理事件数据，必然导致模型无法自适应地应对不同光照强度和运动速度下事件发放模式的剧烈变化。例如，在低光场景中事件噪声增多、有效信号稀疏；在快速运动下事件密度激增、时间结构压缩。单一时间常数的特征提取器难以同时覆盖这些多样化的动态模式。

针对上述缺口，本文提出 **EventGait**，一个端到端的双流事件步态识别框架，其核心动机在于：**鲁棒的事件步态表征必须同时保留高时间分辨率的运动动态，并通过大规模视觉基础模型蒸馏获得空间密集的结构先验，二者互补方能实现光照鲁棒且身份判别的步态描述**。具体而言，EventGait通过两条互补通路分别建模步态的“动”与“静”——动态运动流利用脉冲神经网络（SNN）中的混合专家（MoSE）捕获短时精细运动模式，静态形状流则通过跨模态结构对齐（CroSA）从预训练视觉基础模型（DINOv2）中蒸馏密集空间先验。这种双流解耦设计从根本上回应了事件步态识别的核心矛盾：时间动态与空间结构的不可兼得问题。

## 核心创新

EventGait 的核心创新在于**从“单一时序尺度的事件图像聚合”转向“双时间尺度、双流互补的事件表征学习”**，系统性地解决了事件步态识别中长期被忽视的两个瓶颈：细粒度时间动态的丢失和稀疏事件空间中结构先验的缺失。

### 1. 双时间尺度事件表示：短时动态与长时形状的解耦

现有事件步态方法（如 **EVGait**，CVPR 2019）通常将整个步态周期的事件聚合为单帧事件图像或单一体素网格，这等价于在时间维度上做了极端的平滑化处理，完全丢弃了事件相机高时间分辨率的核心优势。EventGait 的关键设计在于**将时间维度显式建模为两个互补的尺度**：

- **动态流（Dynamic Stream）**：处理短时间窗口的事件体素 $\mathbf{E}_d$，保留高频运动细节，使模型能够感知步态周期中毫秒级的精细时序模式。
- **静态流（Static Stream）**：聚合整个曝光窗口 $T$ 的事件为长时间体素 $\mathbf{E}_s$，捕获完整的空间形状轮廓，为身份判别提供结构基础。

这一“快-慢”双流解耦设计的本质认知是：**步态识别既需要短时运动动态来区分不同个体的运动风格，也需要长时空间形状来建立身份判别的结构锚点**，二者不可偏废。如 Table 6 消融实验所示，移除任一流均会导致 Rank-1 准确率显著下降，验证了双流设计的互补性。

### 2. 混合脉冲专家（MoSE）：自适应动态感知

动态流面临的核心挑战是：不同光照和运动速度下，事件的发放模式和信噪比差异极大，单一时间常数的脉冲神经元无法同时适应这些复杂条件。EventGait 提出的**混合脉冲专家（Mixture of Spiking Experts, MoSE）** 是对这一问题的精准回应：

- **多专家设计**：MoSE 包含 $N$ 个并行的 LIF 脉冲神经元专家，每个专家被赋予不同的膜时间常数 $\tau_i$。较大的 $\tau_i$ 使神经元对历史输入保持更长的记忆，适合慢速运动或低信噪比场景；较小的 $\tau_i$ 则对瞬时变化更敏感，适合快速运动或高动态场景。
- **自适应门控融合**：一个轻量级的脉冲门控网络 $G(\cdot)$ 分析当前事件切片的动态模式，计算自适应混合系数 $\alpha_i$，动态组合各专家的输出：

$$\hat{\mathbf{E}}_t = \sum_{i=1}^N \alpha_i \mathcal{E}_i(\mathbf{E}_t)$$

这一机制使模型无需手动预设时间常数或场景标签，即可在光照剧烈变化或运动速度波动时自动调整感知策略。消融实验（Table 8）表明，采用 3 个专家在精度与效率之间达到最佳平衡，Normal Light 下 Overall 达 92.8。

### 3. 跨模态结构对齐（CroSA）：从视觉基础模型蒸馏密集空间先验

事件数据本质上是稀疏的——只有亮度变化超过阈值的像素才会产生事件，导致事件图像（尤其是长时间聚合后）缺乏密集的空间结构信息。标准 CNN 在稀疏事件表示上难以有效编码空间形状，这是 **EVGait** 和 **GaitBase (Event Input)** 等基线性能受限的深层原因。

EventGait 的解决策略是**从预训练视觉基础模型（VFM）中“借用”密集结构先验**，通过**跨模态结构对齐（Cross-modal Structure Alignment, CroSA）** 将图像域的丰富空间知识蒸馏到事件编码器中：

- **教师网络**：使用冻结的 **DINOv2** 作为教师，从对应灰度图像 $\mathbf{I}_g$ 中提取结构特征 $\mathbf{z}_{\mathrm{img}}$。
- **学生网络**：静态流编码器处理长时事件体素 $\mathbf{E}_s$，经对齐卷积层 $\mathcal{A}$ 投影后得到事件特征 $\mathbf{z}_{\mathrm{evs}}$。
- **对齐损失**：最小化两者之间的 L2 距离，强制事件编码器学习类似图像的结构表征：

$$\mathcal{L}_{\mathrm{align}} = \|\mathbf{z}_{\mathrm{evs}} - \mathbf{z}_{\mathrm{img}}\|_2^2$$

这一设计的深层洞察是：**事件相机的形状信息虽然稀疏，但并非缺失——它只是以一种不同于 RGB 图像的方式编码**。通过 VFM 蒸馏，静态流得以“补全”事件中隐含但难以直接从稀疏数据中学习到的密集结构线索。消融实验（Table 7）证实，使用 L2 距离且权重为 0.2 时对齐效果最优，Overall 达到 92.8。

### 4. 与 baseline 的 changed slots 总结

| 设计维度 | Baseline 做法 | EventGait 创新 | 因果机制 |
|---------|-------------|---------------|---------|
| **时间表示** | 长时间窗口聚合的单尺度事件图像/体素 | 双时间尺度体素：短时 $\mathbf{E}_d$ + 长时 $\mathbf{E}_s$ | 解耦运动动态与空间形状，保留事件高时间分辨率优势 |
| **动态建模** | 标准 CNN/RNN 对稀疏事件图像编码 | MoSE：多时间常数脉冲专家 + 自适应门控融合 | 自适应不同光照和运动速度下的复杂事件模式 |
| **结构增强** | 无外部先验，从稀疏事件中隐式学习形状 | CroSA：从 DINOv2 蒸馏密集结构先验 | 弥补事件稀疏性导致的空间结构缺失 |
| **融合策略** | 单流处理或简单后期融合 | 可学习融合模块 $\Phi$ + 联合损失优化 | 端到端协同优化静态与动态表征 |

这些创新共同构成了一个因果链条：**双时间尺度表示保留了事件的时间优势 → MoSE 自适应处理复杂动态 → CroSA 注入密集结构先验 → 双流融合实现光照鲁棒且身份判别的步态表征**。在 SUSTech1K-E 夜间场景下，EventGait 相较基于 RGB 的方法 Rank-1 提升达 +37.3%，相较使用相同骨干的 GaitBase 事件输入版本提升 +16.7%，充分验证了上述创新的有效性。

> **需要人工验证**：论文未明确报告 venue 和 year，若需精确引用请核实原始发表信息。

## 整体框架

EventGait 是一个端到端的双流步态识别框架，其核心设计目标是在保留事件相机高时间分辨率优势的前提下，分别建模步态中的**运动动态**与**空间形状**两个互补维度。Figure 2 给出了框架的完整工作流。

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/002_Figure_2.jpg]]
*Figure 2: The workflow of our EventGait. The detailed architecture of the Dynamic Motion Stream is shown in Figure 3, while the Static Shape Stream is illustrated in Figure 4*

### 输入与事件表示层

原始输入为异步事件流。每个事件 $e_i = (x_i, y_i, t_i, p_i)$ 由像素坐标、时间戳和极性组成，其触发条件为像素级对数亮度变化超过阈值 $c$：

$$p_i = \mathrm{sg}\left(\log \frac{L(x_i, y_i, t_i)}{L(x_i, y_i, t_i')}\right), \quad \left|\log \frac{L(x_i, y_i, t_i)}{L(x_i, y_i, t_i')}\right| > c$$

事件表示层采用**双时间尺度体素化**策略，将同一曝光窗口 $T$ 内的事件流转换为两种不同时间粒度的体素表示。体素化过程将事件按 $K$ 个时间箱进行加权累积，保留子箱时间精度：

$$\mathbf{E}_p(x, y, k) = \sum_{e_i \in \mathcal{E}_p} \max\left(0, 1 - \frac{|t_i - t_k|}{\Delta T}\right)$$

- **动态流输入 $\mathbf{E}_d$**：使用短时间窗口体素，保留高频运动细节。
- **静态流输入 $\mathbf{E}_s$**：将整个窗口 $T$ 内的事件聚合为长时间窗口体素，捕获完整的空间形状信息。

### 双流编码器

框架由两个并行的编码器分支构成：

1. **动态运动流编码器（Dynamic Motion Stream）**：基于脉冲神经网络（SNN）中的**混合脉冲专家（Mixture of Spiking Experts, MoSE）** 处理 $\mathbf{E}_d$。MoSE 包含 $N$ 个并行的 LIF 神经元专家，每个专家初始化不同的膜时间常数 $\tau_i$，一个轻量级脉冲门控网络分析事件动态模式并计算自适应混合系数，最终输出融合动态特征 $\hat{\mathbf{E}}_t$。该设计使模型能自适应应对不同光照和运动速度下的复杂事件模式。

2. **静态形状流编码器（Static Shape Stream）**：CNN 编码器处理 $\mathbf{E}_s$，并通过**跨模态结构对齐（Cross-modal Structure Alignment, CroSA）** 从预训练视觉基础模型（DINOv2）中蒸馏密集结构先验。冻结的 DINOv2 教师网络提取对应灰度图像的结构特征 $\mathbf{z}_{\mathrm{img}}$，学生事件编码器经对齐卷积层投影得到 $\mathbf{z}_{\mathrm{evs}}$，通过最小化二者之间的 $L_2$ 距离实现结构知识迁移：

   $$\mathcal{L}_{\mathrm{align}} = \|\mathbf{z}_{\mathrm{evs}} - \mathbf{z}_{\mathrm{img}}\|_2^2$$

### 融合与识别

静态流输出特征 $\mathbf{F}_s$ 与动态流输出特征 $\mathbf{F}_d$ 经拼接后送入可学习的融合模块 $\Phi$，生成统一的步态描述符：

$$\mathbf{F}_{\mathrm{gait}} = \Phi([\mathbf{F}_s; \mathbf{F}_d])$$

训练时联合优化交叉熵损失、三元组损失和加权对齐损失：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ce}} + \mathcal{L}_{\mathrm{tri}} + \lambda_d \mathcal{L}_{\mathrm{align}}$$

### 关键设计逻辑

该双流架构的根本动机来自现有方法的瓶颈诊断：长时间窗口聚合的事件图像丢失了细粒度时间动态，而稀疏事件表示又使标准 CNN 难以有效编码空间结构。EventGait 通过**动态流保留高时间分辨率运动信息**、**静态流借助 VFM 蒸馏获取密集空间先验**，二者互补实现了光照鲁棒且身份判别的步态表征。消融实验（Table 6）直接验证了这一互补性——移除任一流均导致性能显著下降。

## 核心模块与公式推导

EventGait 的核心设计围绕一个双流架构展开，分别从事件流中提取高时间分辨率的运动动态和密集的空间结构形状，二者通过可学习的融合模块生成统一的步态描述符。以下按管线顺序解析关键模块及其数学表达。

### 3.1 事件表示层：双时间尺度体素化

事件相机异步输出稀疏的地址-事件流，每个事件 $e_i = (x_i, y_i, t_i, p_i)$ 记录像素坐标、时间戳和极性。事件触发条件由对数亮度变化阈值 $c$ 决定：

$$p_i = \mathrm{sg}\left(\log \frac{L(x_i, y_i, t_i)}{L(x_i, y_i, t_i')}\right), \quad \left|\log \frac{L(x_i, y_i, t_i)}{L(x_i, y_i, t_i')}\right| > c$$

其中 $\mathrm{sg}(\cdot)$ 为符号函数，$L(x,y,t)$ 表示像素在时刻 $t$ 的光度值，$t_i'$ 为同像素上一次触发事件的时间戳。极性 $p_i \in \{+1, -1\}$ 分别指示亮度增加或减少。

为保留亚窗口时间精度，EventGait 将曝光窗口 $T$ 内的事件按极性 $p$ 分别累积到 $K$ 个时间箱中，形成体素表示 $\mathbf{E}_p \in \mathbb{R}^{H \times W \times K}$：

$$\mathbf{E}_p(x, y, k) = \sum_{e_i \in \mathcal{E}_p} \max\left(0, 1 - \frac{|t_i - t_k|}{\Delta T}\right)$$

式中 $\mathcal{E}_p$ 为极性 $p$ 的事件集合，$t_k$ 为第 $k$ 个时间箱的中心时刻，$\Delta T = T/K$ 为箱宽度。该双线性插值形式的加权累积使得每个事件对相邻时间箱的贡献连续衰减，从而在离散化后仍保留精细时序结构。

**双时间尺度设计**是本模块的关键创新：动态流使用短时间窗口的体素 $\mathbf{E}_d$ 捕获高频运动细节，静态流则将整个窗口 $T$ 内的事件聚合为长时间体素 $\mathbf{E}_s$ 以获取完整空间形状。这一设计直接回应了现有方法因长时间聚合而丢失时序动态的核心瓶颈。

### 3.2 动态运动流编码器：混合脉冲专家（MoSE）

动态流的核心是脉冲神经网络（SNN）中的混合专家模块（Mixture of Spiking Experts, MoSE），旨在自适应处理不同光照和运动速度下的复杂事件模式。

**LIF 神经元基础。** 每个脉冲专家基于漏电积分发放（Leaky Integrate-and-Fire, LIF）神经元构建。膜电位 $U(t)$ 的演化方程为：

$$\tau \frac{dU(t)}{dt} = -U(t) + R \cdot I(t), \quad S(t) = \Theta(U(t) - U_{th})$$

其中 $\tau$ 为膜时间常数，$R$ 为膜电阻，$I(t)$ 为突触输入电流，$U_{th}$ 为发放阈值。$\Theta(\cdot)$ 为阶跃函数，当膜电位超过阈值时神经元发放脉冲 $S(t)=1$，随后膜电位复位。突触电流由前层脉冲的加权累积建模：

$$I(t) = \sum_i w_i \sum_k \psi(t - t_i^{(k)})$$

其中 $w_i$ 为突触权重，$t_i^{(k)}$ 为突触前神经元 $i$ 的第 $k$ 次脉冲时刻，$\psi(\cdot)$ 为突触电流衰减核函数。

**MoSE 的自适应机制。** MoSE 包含 $N$ 个并行的脉冲专家 $\{\mathcal{E}_i\}_{i=1}^N$，每个专家被初始化为具有不同膜时间常数 $\tau_i$，从而对事件动态产生差异化的响应特性——小 $\tau$ 的神经元对快速变化敏感，大 $\tau$ 的神经元则能保留较长时间的运动记忆。一个轻量的脉冲门控网络 $G(\cdot)$ 分析输入事件 $\mathbf{E}_t$ 的动态模式，生成自适应混合系数 $\alpha_i$。最终动态特征输出为：

$$\hat{\mathbf{E}}_t = \sum_{i=1}^N \alpha_i \mathcal{E}_i(\mathbf{E}_t)$$

消融实验（Table 8）表明，采用 $N=3$ 个专家在精度与效率之间达到最佳平衡，正常光照下 Overall Rank-1 达到 92.8%。

### 3.3 静态形状流编码器与跨模态结构对齐（CroSA）

静态流采用标准 CNN 编码器处理长时间体素 $\mathbf{E}_s$，但其核心增强来自跨模态结构对齐（Cross-modal Structure Alignment, CroSA）策略——从预训练视觉基础模型（VFM）DINOv2 中蒸馏密集空间结构先验。

**教师-学生对偶特征提取。** 给定灰度图像 $\mathbf{I}_g$ 作为结构参考，冻结的 DINOv2 教师网络 $\mathcal{F}_{\text{teacher}}$ 提取图像结构特征 $\mathbf{z}_{\text{img}}$；学生编码器 $\mathcal{F}_{\text{student}}$ 从事件体素 $\mathbf{E}_s$ 提取特征后，经对齐卷积层 $\mathcal{A}$ 投影至与教师特征相同的语义空间：

$$\mathbf{z}_{\text{img}} = \mathcal{F}_{\text{teacher}}(\mathbf{I}_{\text{g}}), \quad \mathbf{z}_{\text{evs}} = \mathcal{A}(\mathcal{F}_{\text{student}}(\mathbf{E}_s))$$

**对齐损失。** 通过最小化事件特征与图像结构特征之间的 $L_2$ 距离，强制事件编码器学习类似图像的密集空间表征：

$$\mathcal{L}_{\text{align}} = \|\mathbf{z}_{\text{evs}} - \mathbf{z}_{\text{img}}\|_2^2$$

消融实验（Table 7）证实，使用 $L_2$ 距离且对齐损失权重 $\lambda_d = 0.2$ 时效果最优，Overall 达到 92.8%。这一模块有效弥补了事件数据固有的空间稀疏性缺陷，使静态流能够编码判别性的形状信息。

### 3.4 双流融合与联合优化

静态流输出特征 $\mathbf{F}_s$ 与动态流输出特征 $\mathbf{F}_d$ 经拼接后送入可学习的融合模块 $\Phi$，生成统一的步态描述符：

$$\mathbf{F}_{\text{gait}} = \Phi([\mathbf{F}_{\text{s}}; \mathbf{F}_{\text{d}}])$$

融合模块由全连接层或卷积层构成，端到端地学习两流特征的最优组合方式。消融实验（Table 6）表明，移除任一子流均导致 Rank-1 准确率显著下降，验证了静态形状与动态运动信息的互补性。

**总损失函数** 联合优化身份分类、度量学习和结构对齐三个目标：

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{ce}} + \mathcal{L}_{\text{tri}} + \lambda_{\text{d}} \mathcal{L}_{\text{align}}$$

其中 $\mathcal{L}_{\text{ce}}$ 为交叉熵损失，$\mathcal{L}_{\text{tri}}$ 为三元组损失，$\mathcal{L}_{\text{align}}$ 为前述跨模态对齐损失，$\lambda_d$ 控制对齐损失的权重。端到端的联合训练使得模型在保持身份判别力的同时，获得光照鲁棒的结构表征能力。

### 补充图表

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/003_Figure_3.jpg]]
*Figure 3: (a) The simplified schematic of the different spiking neurons’ dynamics across complex conditions (e.g., illumination and motion) for intuitive understanding, (b) The details of the Dynamic Motion Stream, which consists of our Mixture of Spiking Experts (MoSE)*

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/004_Figure_4.jpg]]
*Figure 4: The details of the Static Shape Stream, which is trained with our Cross-modal Structure Alignment (CroSA)*

## 实验与分析

### 核心瓶颈验证：事件步态识别需要同时保留时间动态与空间结构

EventGait 的设计围绕一个关键假设展开：现有事件步态方法将事件流聚合为长时间窗口的事件图像，丢失了细粒度时间动态和密集空间结构，导致标准 CNN 难以有效编码空间上稀疏的事件表示。为验证这一瓶颈，作者在 SUSTech1K-E 数据集上进行了系统性的对比实验。

**主结果（Table 1）** 显示，EventGait 在 SUSTech1K-E 上达到 **92.8%** 的 Rank-1 Overall 准确率，相较首个事件步态方法 **EVGait**（CVPR 2019）的 65.4% 提升了 **+27.4%**，相较基于剪影的现代基线 **GaitBase**（CVPR 2023）的 63.1% 提升了 **+29.7%**。更重要的是，EventGait 相较使用相同骨干但直接处理事件输入的 **GaitBase (Event Input)** 提升了 **+16.7%**，这一增量直接验证了双流设计与脉冲神经元对事件表示的有效性，而非骨干网络本身的改进。

在光照鲁棒性方面，EventGait 展现出决定性优势。在低光夜间场景（NT）下，EventGait 相较基于 RGB 的步态识别方法 Rank-1 准确率提升达 **+37.3%**，在换衣场景（CL）下提升 **+18.4%**。跨光照评估（Table 4）进一步表明，EventGait 在低光条件下仍保持 **83.2%** 的 Overall 准确率，而 GaitBase (Event Input) 仅 23.6%，差距高达 **+59.6%**。这充分说明，仅靠事件输入的稀疏性不足以实现低光鲁棒性，必须通过双流架构分别保留短时动态和长时静态形状。

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/008_Table_4.jpg]]
*Table 4: Cross-Illumination Evaluation*

### 双流互补性：消融实验的关键证据

消融实验（Table 6）直接验证了静态流与动态流的互补作用。移除任一模块均导致性能显著下降，单独使用静态流或动态流的 Rank-1 准确率均明显低于双流融合模型。这一结果支持了核心洞察：**鲁棒的事件步态识别需要同时保留事件流的高时间分辨率动态信息（动态流）和通过大模型蒸馏获得的密集空间结构先验（静态流），二者缺一不可。**

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/009_Table_6.jpg]]
*Table 6: Ablation on the static and dynamic streams of EventGait*

### 跨模态结构对齐（CroSA）的有效性

CroSA 模块通过从预训练视觉基础模型 **DINOv2** 中蒸馏密集结构先验，使静态流能够学习类似图像的结构表征。消融实验（Table 7）表明，使用 L2 距离作为对齐损失且权重为 0.2 时效果最佳，Overall 达到 92.8。相比之下，使用余弦相似度或其他权重均导致性能下降，说明严格的逐特征对齐对事件-图像跨模态知识迁移至关重要。

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/012_Table_7.jpg]]
*Table 7: Ablation of objectives and weights in Cross-modal Structure Alignment*

### 混合脉冲专家（MoSE）的设计选择

MoSE 中专家数量的消融（Table 8）显示，采用 **3 个专家** 在精度与效率之间达到最佳平衡，Normal Light Overall 为 92.8。更多专家（如 5 个）并未带来显著增益，反而增加计算开销。这一设计验证了不同膜时间常数的脉冲神经元能够自适应地处理不同光照和运动速度下的复杂事件模式。

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/010_Table_8.jpg]]
*Table 8: Ablation Studies about the number of experts in MoSE*

### 跨域泛化与跨视角性能

跨域评估（Table 3）显示，EventGait 在不同数据集之间迁移时仍保持较强性能，但合成事件数据与真实事件数据之间的域差异仍然存在。在真实事件数据集 DVS128-Gait 上（Table 5），EventGait 达到 87.4% Rank-1 准确率，相较 EV-Gait 的 81.8% 提升 +5.6%，但相较合成数据上的巨大增益有所收窄，表明合成-真实域差异是当前方法的一个瓶颈。

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/007_Table_3.jpg]]
*Table 3: Cross-domain Evaluation*

跨视角性能比较（Figure 5）通过雷达图展示了 EventGait 与基于 LiDAR 的最先进方法 **LidarGait++**（CVPR 2025）的对比。EventGait 在多个视角下展现出与 LiDAR 方法竞争的性能，同时仅需 4.6M 参数，远低于典型的 LiDAR 方法。

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/011_Figure_5.jpg]]
*Figure 5: Cross-view performance comparison between Lidar-Gait++ [74] and EventGait (ours)*

### 失败模式与局限性

尽管 EventGait 在合成数据集上表现优异，但以下局限性需要关注：

1. **合成-真实域差异**：主要评估在合成数据集 SUSTech1K-E 上进行，真实场景下的表现有待更多真实数据验证。CCGR-Mini-E 上 40.3% 的 Rank-1 准确率（Table 2）表明，在更复杂的真实事件分布下，性能仍有较大提升空间。
2. **脉冲推理效率**：动态流中的脉冲神经元在通用硬件上的模拟推理效率仍有待优化，实际部署的延迟和功耗可能较高。尽管参数仅 4.6M，但脉冲计算的时间步展开增加了推理时间。
3. **单模态局限**：当前方法仅依赖事件单模态，尚未探索与 RGB 或 LiDAR 的多模态融合可能带来的进一步提升。

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/006_Table_2.jpg]]
*Table 2: Within-domain Evaluation on CCGR-Mini [104] / CCGR-Mini-E (Ours) and CASIA-B* [97] / EV-CASIA-B [83]*

### 补充图表

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/005_Table_1.jpg]]
*Table 1: Within-domain Evaluation on SUSTech1K [71] and SUSTech1K-E (ours)*

![[assets/figures/papers/paper_list_l1046_https_arxiv_org_abs_2605_22139/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of RGB and event cameras under day and night conditions. RGB cameras fail to capture usable gait representations in low-light conditions. While event cameras are robust to illumination changes and capture extremely high-temporalresolution data, preserving spatiotemporal cues in all lighting*

## 方法谱系与知识库定位

### 1. 事件步态识别的方法谱系

EventGait 处于**事件相机步态识别**这一新兴方向的早期探索阶段。在它之前，事件步态识别的研究极为稀少，主要基线工作如下：

- **EVGait**（CVPR 2019）是首个基于事件相机的步态识别方法，其核心思路是将事件流聚合为长时间窗口的事件图像，随后利用标准CNN或GNN进行特征提取。这一范式虽然开创性地将事件数据引入步态领域，但存在根本性瓶颈：长时间聚合操作丢弃了事件相机固有的高时间分辨率动态信息，且生成的稀疏事件图像难以被标准CNN有效编码，导致模型无法充分利用事件数据的优势。

- **GaitBase（Event Input）** 是将现代剪影步态基线 **GaitBase**（CVPR 2023）直接应用于事件输入的变体，代表了“将成熟剪影方法迁移至事件模态”的朴素思路。然而，由于事件体素与剪影在空间分布和语义密度上的本质差异，该迁移效果有限。

在更广泛的步态识别谱系中，**剪影方法**占据主导地位：从经典的 **GaitSet**（AAAI 2019）、**GaitPart**（CVPR 2019），到现代基线 **GaitBase**（CVPR 2023）和最先进的 **DeepGaitV2**（TPAMI 2025）。这些方法依赖RGB相机提取人体剪影，在正常光照下表现优异，但在低光或夜间场景下因RGB成像失效而性能急剧下降。此外，**LidarGait++**（CVPR 2025）代表了基于LiDAR点云的步态识别前沿，具有光照鲁棒性但面临点云稀疏和硬件成本问题。

EventGait 在方法谱系中的定位是：**首次将脉冲神经网络（SNN）与视觉基础模型蒸馏引入事件步态识别**，通过双流架构同时保留事件的动态和静态信息，填补了现有方法在时间分辨率保留和空间结构增强两个维度上的空白。

### 2. 与基线方法的核心差异

EventGait 与前述基线存在三个层面的根本性差异：

**时间表示层面**：EVGait 使用单一长时间窗口聚合，丢失了子窗口内的精细时序变化；GaitBase（Event Input）沿用了类似的单尺度体素化。EventGait 则采用**双时间尺度体素设计**——动态流使用短时间窗口体素 $\mathbf{E}_d$ 保留高频运动细节，静态流使用长时间窗口体素 $\mathbf{E}_s$ 捕获完整空间形状。这一设计从输入层面就为后续的双流分工奠定了基础。

**动态建模层面**：EVGait 和 GaitBase 均使用标准CNN处理事件表示，CNN的静态卷积核难以自适应地捕捉事件数据中因光照和运动速度变化而产生的复杂时序模式。EventGait 的动态流引入了**混合脉冲专家（MoSE）**：$N$ 个并行的LIF神经元专家各自具有不同的膜时间常数 $\tau_i$，由轻量级脉冲门控网络 $G(\cdot)$ 根据输入事件的动态模式计算自适应融合系数：

$$\hat{\mathbf{E}}_t = \sum_{i=1}^N \alpha_i \mathcal{E}_i(\mathbf{E}_t)$$

这一机制使模型能够在不同光照和运动条件下自动调整时间感受野，实现了对复杂事件模式的鲁棒感知。

**空间结构增强层面**：EVGait 和 GaitBase 仅从稀疏事件输入中隐式学习形状信息，缺乏显式的结构先验。EventGait 通过**跨模态结构对齐（CroSA）** 从预训练视觉基础模型 DINOv2 中蒸馏密集结构先验，强制静态流学习类似图像的结构表征。对齐损失为事件特征与图像特征之间的欧氏距离：

$$\mathcal{L}_{\mathrm{align}} = \|\mathbf{z}_{\mathrm{evs}} - \mathbf{z}_{\mathrm{img}}\|_2^2$$

这一设计使得静态流能够弥补事件数据空间稀疏的固有缺陷，获得更丰富的身份判别性形状信息。

### 3. 适用边界与局限性

尽管 EventGait 在合成事件数据集上取得了显著提升，其适用边界和局限性需要审慎评估：

**数据域差异**：主要评估在合成事件数据集（SUSTech1K-E、CCGR-Mini-E、EV-CASIA-B）上进行，合成事件与真实事件之间存在域差异。在真实事件数据集 DVS128-Gait 上的提升幅度（+5.6%）远小于合成数据集（+27.4%），表明模型在真实场景下的泛化能力尚需更多真实世界事件步态数据的验证。这一域差异可能源于合成事件的理想化噪声模型和均匀光照假设。

**模态局限性**：当前方法主要依赖事件单模态，尚未探索多模态融合（如RGB+Event、LiDAR+Event）可能带来的进一步提升。在极端条件下（如完全黑暗中的快速运动），事件数据本身可能存在信息不足的问题，此时多模态互补可能更为关键。

**推理效率**：尽管模型参数量较少（4.6M），但动态流中的脉冲神经元在通用硬件（GPU）上的模拟推理效率仍有待优化。脉冲神经网络的实际部署优势（低功耗、低延迟）依赖于神经形态硬件的支持，在传统硬件上的模拟推理可能无法体现其理论优势。

### 4. 开放问题与未来方向

基于 EventGait 的方法定位和局限性，以下几个开放问题值得关注：

1. **大规模真实事件步态数据集的构建**：当前最大的事件步态数据集 SUSTech1K-E 为合成数据，如何收集大规模、多样化的真实事件步态数据（覆盖不同光照、天气、视角条件），是缩小合成-真实域差距、推动该方向实用化的关键瓶颈。

2. **多模态融合策略**：事件相机与RGB相机、LiDAR在物理特性上高度互补——事件相机提供高时间分辨率动态信息，RGB提供密集纹理和颜色，LiDAR提供精确深度。如何高效融合这些异构模态，在保持事件光照鲁棒性的同时引入额外的身份判别信息，是进一步提升极端条件下性能的重要方向。

3. **SNN推理效率的硬件协同设计**：脉冲神经网络的实时推理效率与硬件协同设计如何优化，以降低实际应用中的功耗和延迟？这涉及神经形态芯片的适配、脉冲编码策略的优化以及训练-部署协同等系统级问题。

4. **跨域泛化能力的系统评估**：当前跨域评估（Table 3）已初步展示了模型在不同数据集间的迁移能力，但评估规模有限。更系统的跨域泛化研究——包括跨数据集、跨光照、跨视角、跨穿着等维度的组合泛化——对于理解方法的真实鲁棒性边界至关重要。

## 原文 PDF

![[paperPDFs/CVPR_2026/EventGait_Towards_Robust_Gait_Recognition_with_Event_Streams.pdf]]
