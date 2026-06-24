---
title: "Detecting Temporal Misalignment Attacks in Multimodal Fusion for Autonomous Driving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Detecting_Temporal_Misalignment_Attacks_in_Multimodal_Fusion_for_Autonomous_Driving.pdf
openreview_forum_id: SWlCJab9gZ
aliases:
- DTMAMFAD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "攻击者通过操纵传感器时间戳，利用 ROS2 的 ApproximateTimeSynchroniser 制造语义上不一致的跨模态特征对，从而破坏感知输出。"
primary_logic: "利用连续性感知对比学习（CACL）迫使共享多模态表示沿时间轴平滑过渡，并结合动态时间规整（DTW）从对齐路径的奖励/代价中直接量化时间错位程度，无需依赖统一时钟基准。"
claims:
- "AION 集成了连续性感知对比学习与 DTW 检测机制，能够学习平滑的多模态表示并生成错位得分。"
- "在 KITTI 和 nuScenes 上，AION 对相机单独攻击的平均 AUROC 达到 0.9493，对激光雷达单独攻击达到 0.9495。"
- "当发生时间错位攻击时，DTW 计算得到的对齐路径会偏离对角线，奖励/代价显著降低，从而生成高异常得分。"
- "KITTI 上 AUROC (camera‑only attacks) = 0.9493"
---

# Detecting Temporal Misalignment Attacks in Multimodal Fusion for Autonomous Driving

> [!tip] 核心洞察
> 利用连续性感知对比学习（CACL）迫使共享多模态表示沿时间轴平滑过渡，并结合动态时间规整（DTW）从对齐路径的奖励/代价中直接量化时间错位程度，无需依赖统一时钟基准。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向自动驾驶多模态融合的时间错位攻击检测 |
| 英文题名 | Detecting Temporal Misalignment Attacks in Multimodal Fusion for Autonomous Driving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=SWlCJab9gZ); [GitHub](https://github.com/shahriar0651/AION) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | AION |
| Dataset | KITTI, nuScenes |

> [!tip] 效果简介
> - KITTI 上，AUROC (camera‑only attacks) 为 0.9493，对比 N/A，变化 N/A。
> - nuScenes 上，AUROC (LiDAR‑only attacks) 为 0.9495，对比 N/A，变化 N/A。

## 概述

自动驾驶系统依赖相机与激光雷达等多模态传感器融合来实现精确的环境感知。然而，现有的融合流水线普遍采用 ROS2 的 ApproximateTimeSynchroniser 等近似时间同步机制，这些机制完全忽略了时间维度的安全性——攻击者只需篡改传感器时间戳，即可迫使系统将语义上不一致的跨模态数据配对融合，从而破坏感知输出。这种时间错位攻击（Temporal Misalignment Attack, TMA）可以绕过所有现有的语义/空间一致性防御，构成自动驾驶安全的真实瓶颈。

针对这一漏洞，本文提出 **AION**——一种轻量级即插即用防御方案。AION 的核心思路是：不依赖统一时钟基准，而是从跨模态表示的时间连续性本身来检测错位。具体而言，AION 集成了两个关键组件：

1. **连续性感知对比学习（CACL）**：训练一个共享多模态表示编码器，迫使相机和激光雷达的表示沿时间轴平滑过渡，使得时间错位在表示空间中产生可量化的异常。
2. **基于动态时间规整（DTW）的检测机制**：在跨模态相似度矩阵上运行 DTW，追踪最优时间对齐路径。正常场景下，最优路径沿对角线分布且累积奖励最高；攻击发生时，路径偏离对角线，奖励显著降低，从而直接生成异常得分。

在 KITTI 和 nuScenes 数据集上的实验表明，AION 对相机单独攻击的平均 AUROC 达到 **0.9493**，对激光雷达单独攻击达到 **0.9495**，且在双模态联合攻击下仍保持稳健性能。与基于时间戳方差和滑动窗口特征相关的基线方法相比，AION 在所有七种攻击类型上均展现出显著优势。

AION 也存在明确局限：对恒定延迟攻击（所有模态被同步偏移相同时间）检测能力有限，因为此时跨模态语义仍然一致；当前方案仅覆盖相机与激光雷达两种传感器；异常阈值需在不同场景下重新标定以保证低误报率。这些限制为未来的防御扩展指明了方向。

## 背景与动机

自动驾驶系统依赖多模态传感器融合实现可靠的场景理解，其中相机与激光雷达的精确时间同步是融合质量的前提。在典型的 ROS2 中间件架构中，融合节点使用近似时间同步器（ApproximateTimeSynchroniser）将不同传感器的时间戳对齐：对于每一帧相机消息，同步器选择时间戳最接近的激光雷达帧进行配对，即 $j^{\star}(i) = \arg \min_k \big| t_C^{(i)} - t_L^{(k)} \big|$。然而，这一时间同步机制本身构成了一个被长期忽视的攻击面。

**核心瓶颈**在于，现有的多模态融合防御手段——无论是对抗样本检测、语义一致性校验还是空间对齐验证——全部聚焦于空间与语义维度，完全忽略了时间维度。攻击者可以通过篡改传感器时间戳（而非传感器数据本身），利用同步器的配对逻辑制造语义上不一致的跨模态特征对。具体而言，攻击者将真实时间戳 $t_C$、$t_L$ 替换为伪造值 $\tilde{t}_C$、$\tilde{t}_L$，使同步器输出错误配对索引 $\tilde{j}^{\star}(i) = \arg \min_k \big| \tilde{t}_C^{(i)} - \tilde{t}_L^{(k)} \big|$，最终产生被污染的融合表示 $\tilde{h}^{(i)} = F \big( E_C (x_C^{(i)}) , E_L (x_L^{(\tilde{j}^{\star})}) \big)$。这种时间错位攻击（Temporal Misalignment Attack, TMA）可以绕过所有基于空间/语义一致性的防御检查，直接破坏下游感知输出。

**现有防御缺口**表现为两个层面。其一，传统的基于时间戳统计的检测方法（如时间戳间隔方差检查）仅能识别明显的时序异常模式，对精心构造的抖动攻击或漂移攻击效果有限。其二，基于滑动窗口内跨模态特征 Pearson 相关系数的检测方法虽然引入了语义信号，但缺乏对时序连续性结构的显式建模，难以区分正常的时间偏移与恶意的时间错位。二者均未利用跨模态表示在时间轴上的平滑过渡这一内在结构特性。

**本文的核心动机**正是填补这一防御空白。关键洞察在于：正常操作下，相机与激光雷达的跨模态表示沿时间轴应呈现平滑过渡；而时间错位攻击会破坏这种连续性，表现为跨模态相似度矩阵中对齐路径偏离对角线、累积奖励/代价值显著恶化。基于这一洞察，AION 提出了两个互补机制：连续性感知对比学习（CACL）迫使共享多模态表示沿时间轴平滑过渡，以及基于动态时间规整（DTW）的检测模块直接从对齐路径的奖励/代价中量化时间错位程度。该方法无需依赖统一时钟基准或外部时间源，仅通过跨模态时序一致性即可检测异常。

## 核心创新

### 问题瓶颈：时间维度防御空白

现有自动驾驶多模态融合系统依赖精确的时间同步来保证跨模态特征在语义上的一致性。然而，所有已知的防御手段——无论是基于语义一致性检查还是空间对齐验证——都完全忽略时间维度。攻击者只需操纵传感器的时间戳（例如通过 ROS2 的 ApproximateTimeSynchroniser），就能迫使系统将语义上不匹配的相机帧与激光雷达帧配对，从而破坏感知输出。这一时间维度的防御空白构成了本工作的核心瓶颈。

### 核心洞察：连续性感知表示 + DTW 对齐路径分析

AION 的核心洞察在于：**如果多模态表示沿时间轴是平滑过渡的，那么时间错位攻击会破坏这种平滑性，而这种破坏可以被动态时间规整（DTW）从对齐路径的奖励/代价中直接量化，无需依赖统一时钟基准。** 具体而言，在良性场景下，相机与激光雷达表示之间的最优 DTW 对齐路径应为对角线，累积奖励最高；当发生时间错位攻击时，最优路径偏离对角线，奖励/代价显著降低，从而直接指示攻击存在。

### Changed Slots：相对基线的关键替换

| 模块 | 基线方案 | AION 方案 |
|------|----------|-----------|
| **时间错位防御模块** | 无专用防御 | 插入轻量级 AION 检测补丁，包含 CACL 训练的共享多模态表示编码器（MRE）与基于 DTW 的错位评分模块 |
| **跨模态表示学习策略** | 标准二值对比学习（正/负） | 连续性感知对比学习（CACL），引入近负对与远负对的划分，并用 $ \lambda_{ij} = \tanh(|i - j| / \tau) $ 加权惩罚 |
| **错位检测算法** | 基于时间戳方差或滑动窗口特征相关 | DTW 计算最优对齐路径及其累积奖励，将奖励的倒数/归一化值作为异常得分 |

### CACL：连续性感知对比学习

标准对比学习仅区分正对与负对，无法捕捉时间轴上的连续过渡特性。CACL 的核心改进在于两点：

1. **三类数据对划分**：正对（同一时间步的跨模态对）、近负对（时间距离较小的跨模态对）、远负对（时间距离较大的跨模态对）。
2. **平滑时间加权**：负对惩罚权重 $ \lambda_{ij} = \tanh(|i - j| / \tau) $ 随时间距离平滑增长，$ \tau $ 控制近负/远负的过渡灵敏度。这使得模型不会粗暴地将相邻时间步的表示推开，而是学习沿时间轴的平滑过渡。

训练损失由正对损失 $ \mathcal{L}_{\mathrm{pos}} = \sum_{i=1}^{b} (S_{ii} - 1)^2 $ 和负对损失 $ \mathcal{L}_{\mathrm{neg}} = \sum_{i \neq j} (\max(0, S_{ij}))^2 \cdot \lambda_{ij} $ 组成，其中 $ S_{ij} $ 为相机与激光雷达表示的余弦相似度。

### DTW 错位评分：无需时钟基准的检测

AION 的检测机制不依赖任何统一时钟基准，而是利用 CACL 训练得到的共享表示空间中的时序一致性：

1. 维护一个指数采样的历史表示队列（采样索引 $ n_i = \psi^i $），确保近期帧密度高、远期帧密度低。
2. 在窗口 $ w $ 内构造跨模态余弦相似度矩阵 $ S_{ij} = \frac{r_C^{(i)} \cdot r_L^{(j)}}{\|r_C^{(i)}\| \|r_L^{(j)}\|} $。
3. 在相似度矩阵上运行 DTW，寻找最优对齐路径 $ \mathcal{P}^* $ 及其累积奖励。良性场景下最优路径为对角线，奖励最高；攻击下路径偏离对角线，奖励降低，该奖励的倒数即为异常得分。

### 证据强度

- **高置信度（0.95）**：AION 在 KITTI 和 nuScenes 上对相机单独攻击的平均 AUROC 达 0.9493，对激光雷达单独攻击达 0.9495；双模态联合攻击下仍维持 0.9195。
- **中高置信度（0.9）**：DTW 对齐路径偏离对角线的机制在良性/攻击场景的对比中得到验证，但缺乏对极端边界情况的定量分析。
- **需人工核实**：对恒定延迟攻击（所有模态被同步偏移相同时间）的检测能力有限，因为此时跨模态语义仍然一致，仅靠表示空间的时序一致性难以识别。

## 整体框架

![[assets/figures/papers/iclr26_0012_SWlCJab9gZ_Detecting_Temporal_Misalignment_Attacks_in_Multi/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed defense AION against any TMA attack*

![[assets/figures/papers/iclr26_0012_SWlCJab9gZ_Detecting_Temporal_Misalignment_Attacks_in_Multi/figures/002_Table_1.jpg]]
*Table 1: Seven Temporal Misalignment Attack Strategies*

AION 是一种轻量级即插即用防御补丁，嵌入多模态融合流水线中，专门检测时间错位攻击（Temporal Misalignment Attack, TMA）。其整体架构如图 1 所示：相机和激光雷达两路传感器数据经由车载网络（ROS2 中间件）进入融合节点，攻击者可在时间戳层面注入 TMA，迫使 ApproximateTimeSynchroniser 将语义上不匹配的跨模态帧配对送入下游感知模块。AION 位于特征提取之后、融合之前，通过分析跨模态表示的时间一致性来判定当前窗口是否存在错位。

### 核心模块与数据流

AION 由三个关键模块串联构成：

1. **共享多模态表示编码器（MRE）**：接收相机特征 $f_C$ 和激光雷达特征 $f_L$，通过共享的编码器 $E_{mm}$ 将它们投影到统一表示空间，得到 $r_C$ 和 $r_L$。该编码器经连续性感知对比学习（CACL）训练，迫使跨模态表示沿时间轴平滑过渡——时间上相邻的帧对具有高相似度，远离的帧对相似度自然衰减。

2. **历史表示队列（指数采样）**：维护一个窗口大小为 $w$ 的近期表示序列，采样索引按 $n_i = \psi^i$ 衰减，使得近期帧密度高、远期帧密度低，在有限窗口内保留更长时间跨度的时序信息。

3. **基于 DTW 的错位评分**：在每个滑动窗口内，计算相机与激光雷达表示间的余弦相似度矩阵 $S_{ij}$，然后运行动态时间规整（DTW）算法，寻找最优对齐路径 $\mathcal{P}^*$ 及其累积奖励/代价。正常场景下，最优路径趋近对角线，奖励值较高；遭受 TMA 时，对齐路径偏离对角线，奖励显著降低——这一差异直接量化为异常得分。

### 检测决策逻辑

AION 对每个观察窗口（默认 $w=3$，采样底数 $\psi=2$）输出一个异常得分。若窗口内至少一半的多模态对包含错位样本，则该窗口被标记为恶意。异常阈值基于良性数据全局得分的第 99 百分位标定，确保误报率控制在 1% 以下。

### 攻击面覆盖

AION 针对七类 TMA 攻击策略（表 1）设计：Constant（恒定延迟）、Random（随机替换）、Jitter（带噪声的随机抖动）、Reversal（时间戳反转）、Burst（突发性批量延迟）、Drift（累积漂移延迟）和 Scheduler（调度器级别操纵）。这些攻击覆盖了时间戳冻结、替换、随机化、重排序和渐进偏移等典型操纵模式，AION 无需针对单一攻击类型训练，而是通过时间一致性这一通用信号实现统一检测。

## 核心模块与公式推导

### 威胁模型与攻击面

多模态融合流水线依赖 ROS2 的 ApproximateTimeSynchroniser 完成跨传感器配对：对于每一帧相机消息，同步器选择时间戳最接近的激光雷达帧，即

$$j^{\star}(i) = \arg \min_k \big| t_C^{(i)} - t_L^{(k)} \big|$$

攻击者通过篡改传感器上报的时间戳 $\tilde{t}_C$、$\tilde{t}_L$，迫使同步器依据伪造时间戳选择错误配对索引：

$$\tilde{j}^{\star}(i) = \arg \min_k \big| \tilde{t}_C^{(i)} - \tilde{t}_L^{(k)} \big|$$

由此产生的错误融合特征为：

$$\tilde{h}^{(i)} = F \big( E_C (x_C^{(i)}) , E_L (x_L^{(\tilde{j}^{\star})}) \big)$$

该攻击面之所以危险，是因为它完全绕过所有语义/空间一致性检查——现有防御全部忽略时间维度，仅依赖特征内容判断，无法区分正常融合与时间错位融合。

### AION 检测流水线

AION 作为轻量级即插即用补丁嵌入融合节点，包含两个核心模块：

1. **共享多模态表示编码器（MRE）**：将相机特征 $f_C$ 和激光雷达特征 $f_L$ 投影到统一表示空间，得到 $r_C^{(i)} = E_{mm}(f_C^{(i)})$ 和 $r_L^{(j)} = E_{mm}(f_L^{(j)})$。
2. **基于 DTW 的错位评分模块**：在跨模态表示对上计算相似度矩阵，通过动态时间规整量化时间错位程度并输出异常得分。

检测时，AION 维护一个历史表示队列，采用指数采样策略（采样索引 $n_i = \psi^i$，$\psi=2$）保留窗口内 $w$ 个最近表示。对窗口内的相机-激光雷达表示对，计算余弦相似度矩阵：

$$S_{ij} = \frac{r_C^{(i)} \cdot r_L^{(j)}}{\|r_C^{(i)}\| \|r_L^{(j)}\|}$$

在 $S$ 上运行 DTW 算法，寻找最优对齐路径 $\mathcal{P}^*$ 及其累积奖励/代价。DTW 的累积代价定义为：

$$C(\mathcal{P}) = \sum_{(i,j) \in \mathcal{P}} D(i,j)$$

核心洞察在于：正常场景下，最优路径应接近对角线（时间同步的对齐），获得最高奖励；遭受时间错位攻击时，最优路径偏离对角线，奖励显著降低。这一奖励/代价的倒数或归一化值直接作为异常得分，无需依赖统一时钟基准。

### 连续性感知对比学习（CACL）

CACL 是训练 MRE 的核心策略，其关键创新在于突破传统二值对比学习（正/负对）的限制，引入基于时间距离的平滑惩罚机制。

**正对损失**鼓励时间对齐的跨模态表示高度相似：

$$\mathcal{L}_{\mathrm{pos}} = \sum_{i=1}^{b} (S_{ii} - 1)^2$$

**负对损失**按时间距离加权惩罚负对的相似度，其中权重函数 $\lambda_{ij}$ 是关键设计：

$$\mathcal{L}_{\mathrm{neg}} = \sum_{\substack{i,j=1 \\ i \neq j}}^{b} (\max(0, S_{ij}))^2 \cdot \lambda_{ij}$$

$$\lambda_{ij} = \tanh\left(\frac{|i - j|}{\tau}\right)$$

$\lambda_{ij}$ 的作用机制：当 $|i-j|$ 较小（近负对），$\tanh$ 值接近 0，惩罚较轻，允许相邻时间步的表示保持一定相似性，从而实现平滑过渡；当 $|i-j|$ 较大（远负对），$\tanh$ 值接近 1，惩罚趋近标准对比学习的强度，迫使远距离表示充分分离。超参数 $\tau$ 控制近负/远负的过渡灵敏度。

这一设计迫使共享多模态表示沿时间轴平滑演变，使得时间错位在表示空间中表现为可量化的异常模式——DTW 对齐路径的偏离程度。

### 攻击策略形式化

论文定义了 7 种时间错位攻击策略（Table 1），其延迟公式覆盖了从简单到高级的攻击模式：

- **抖动攻击**：$\delta_t = \mu + \varepsilon_t$，引入带均匀噪声的随机延迟。
- **漂移攻击**：$\delta_i = \lfloor r \times i \rfloor$，以固定速率 $r$ 累积延迟，逐步扩大错位。

这些攻击的多样性覆盖了冻结、替换、随机、重排序、突发、漂移和调度器攻击等多种时间操纵模式，用于全面评估 AION 的检测鲁棒性。

### 基线检测方法

作为对比，论文实现了两种无学习基线：

- **时间戳方差检测器**：计算时间戳间隔的归一化方差 $\frac{\mathrm{var}(\Delta t)}{\mathbb{E}[\Delta t]^2 + \varepsilon}$ 作为异常得分，仅依赖时间戳统计特性。
- **滑动窗口相关检测器**：对窗口内每对相机-激光雷达表示计算 Pearson 相关系数 $\rho_i$，取平均 $\bar{\rho} = \frac{1}{w}\sum_{i=1}^{w}\rho_i$，映射为异常得分 $(1-\bar{\rho})/2$。

这两种基线分别仅利用时间戳信息或仅利用特征相关性，均无法捕捉跨模态时间一致性的细粒度变化，为 AION 的 DTW 方案提供了对比基准。

## 实验与分析

### 核心发现

AION 在 KITTI 与 nuScenes 两个主流自动驾驶数据集上展现出对七类时间错位攻击（TMA）的强检测能力。对于相机单独攻击，平均 AUROC 达到 0.9493；对于激光雷达单独攻击，平均 AUROC 达到 0.9495。即使在双模态同时遭受攻击的严苛场景下，AION 仍维持约 0.9195 的 AUROC，表明连续性感知对比学习（CACL）与 DTW 检测机制的组合能够有效捕获跨模态时间一致性破坏。

### 检测性能分析

表 3 给出了在假阳性率（FPR）严格控制在 0.01 以下的窗口级真正率（TPR）。Reversal 攻击在相机模态上达到 1.0000 的 TPR，但在激光雷达模态上仅 0.4000，融合模态为 0.5200，说明攻击对单一模态的扰动模式在跨模态表示空间中具有不对称的可检测性。Burst 攻击在 KITTI 双模态场景下 TPR 仅 0.2742，属于较难检测的攻击类型，这与 Burst 攻击的短时突发特性有关——DTW 窗口内可能仅包含少量错位样本对，累积奖励下降幅度有限。


![[assets/figures/papers/iclr26_0012_SWlCJab9gZ_Detecting_Temporal_Misalignment_Attacks_in_Multi/figures/035_Table_3.jpg]]
*Table 3: True Positive Rate (TPR) at a False Positive Rate (FPR) of \< 0.01 across various attack types and sensor modalities*

### 窗口大小敏感性

Figure 12 的消融分析表明，DTW 窗口大小 w 对检测性能存在非单调影响。w=3 与 w=5 时 AUROC 达到峰值，当 w 增大至 7 及以上时性能出现下降。这一现象背后的因果机制是：过小的窗口限制了 DTW 对齐路径的搜索空间，可能遗漏累积性错位模式（如 Drift 攻击）；而过大的窗口会稀释局部时间一致性破坏的信号，同时增加历史表示队列中远时间步样本的噪声贡献。AION 采用的指数采样策略（采样索引 $n_i = \psi^i$）在一定程度上缓解了远距离样本的权重问题，但无法完全抵消大窗口带来的信噪比下降。


![[assets/figures/papers/iclr26_0012_SWlCJab9gZ_Detecting_Temporal_Misalignment_Attacks_in_Multi/figures/034_Figure_12.jpg]]
*Figure 12: Sensitivity analysis of the impact of window size w on detection performance (AUROC) across various attack types for the KITTI and NuScenes datasets*

### 计算开销

Table 2 显示 AION 引入的额外计算开销极为有限。共享多模态表示编码器（MRE）单次前向推理耗时 1.74 ms，吞吐量 574 inf/s，占用约 42.5 MB GPU 显存；DTW 检测模块耗时 1.52 ms，吞吐量 659 inf/s，无需 GPU 显存。总开销约 3.26 ms/推理，参数规模仅约 1.97M（FP32 下约 7.9 MB），满足自动驾驶实时性要求。

### 基线对比

Figure 13 展示了 AION 与两类基线的 AUROC 对比。基于时间戳间隔方差（Timestamp‑sanity）的检测器在 KITTI 上 AUROC 普遍低于 0.8，在 nuScenes 上低于 0.7，其根本缺陷在于攻击者可伪造时间戳使其间隔统计特征与良性场景无异。基于滑动窗口内相机‑激光雷达特征 Pearson 相关系数的检测器表现略好，但对语义上仍保持一定一致性的攻击（如小幅度 Jitter）区分能力不足。AION 的核心优势在于 DTW 直接从跨模态表示的对齐路径累积奖励中量化错位程度，不依赖时间戳本身的可信度。


![[assets/figures/papers/iclr26_0012_SWlCJab9gZ_Detecting_Temporal_Misalignment_Attacks_in_Multi/figures/037_Figure_13.jpg]]
*Figure 13: Baseline comparison of AUROC for the Timestamp and Correlation-based detectors across seven TMA attacks on KITTI (top) and nuScenes (bottom). AION consistently achieves higher AUROC than both baselines for most attack types, especially on complex datasets such as NuScenes, demonstrating its stronger robustness to diverse timing perturbations*

### 失败模式与局限

AION 存在明确的检测盲区：当所有传感器被施加相同的恒定延迟（Constant 攻击且延迟量一致）时，跨模态语义一致性得以保留，DTW 对齐路径仍接近对角线，累积奖励与良性场景差异不显著。此时仅靠跨模态数据难以识别攻击，需要引入独立时间基准（如 GNSS 时间戳）或额外模态信号（如 IMU）作为参照。此外，异常阈值基于良性数据 99 分位数标定，在不同场景或数据集上可能需要重新校准以保证 FPR < 0.01 的一致性。

### 补充图表

![[assets/figures/papers/iclr26_0012_SWlCJab9gZ_Detecting_Temporal_Misalignment_Attacks_in_Multi/figures/017_Figure_4.jpg]]
*Figure 4: ROC curves with AUROC scores of AION under TMA attacks across KITTI and nuScenes, evaluated on camera, lidar, and both camera–lidar modalities*


## 方法谱系与知识库定位

### 与已有防御方法的关系

AION 所填补的核心空白是**时间维度的防御缺失**：现有自动驾驶多模态融合系统的安全研究几乎全部聚焦于空间或语义层面的对抗攻击（如激光雷达点云扰动、相机像素对抗样本），而融合流水线中广泛使用的 ROS2 `ApproximateTimeSynchroniser` 仅依据传感器上报的时间戳进行配对，缺乏对时间戳真伪的验证机制。这使得攻击者可以通过篡改时间戳，在不修改任何传感器数据内容的前提下，制造语义上不一致的跨模态特征对，从而绕过所有基于空间/语义一致性检查的防御方案。

本文设定了两个直接基线以量化 AION 的相对优势：

- **Timestamp‑sanity（时间戳方差检测）**：利用传感器时间戳序列的到达间隔方差作为异常指标，异常得分定义为 $\text{var}(\Delta t) / (\mathbb{E}[\Delta t]^2 + \varepsilon)$。该方法的根本缺陷在于，攻击者可以构造具有正常统计特性的伪造时间戳序列（如恒定速率漂移攻击），使其方差与良性数据无异，从而完全失效。实验表明，该基线在 KITTI 上的 AUROC 普遍低于 0.8，在 nuScenes 上低于 0.7。

- **Sliding‑window correlation（滑动窗口特征相关检测）**：在每个时间步计算相机与激光雷达特征向量的 Pearson 相关系数 $\rho_{n_i} = \text{corr}(r_C^{n_i}, r_L^{n_i})$，并在窗口内取平均 $\bar{\rho} = \frac{1}{w} \sum_{i=1}^{w} \rho_i$，映射为异常得分 $(1 - \bar{\rho}) / 2$。该方法虽然利用了跨模态语义信息，但仅依赖单帧特征的瞬时相关性，缺乏对时间序列动态的建模能力，对缓慢漂移或间歇性攻击的灵敏度不足。

AION 通过**连续性感知对比学习（CACL）** 与**动态时间规整（DTW）** 的组合，从根本上改变了检测逻辑：不是检查单帧配对是否“看起来一致”，而是检查跨模态表示沿时间轴的**对齐路径质量**。这一设计使其对七种不同攻击策略（Constant、Random、Jitter、Reversal、Burst、Drift、Scheduler）在 KITTI 和 nuScenes 上均保持 0.85–0.97 的 AUROC，显著优于两个基线。

### 适用边界与局限

AION 的检测能力建立在以下核心假设之上，当这些假设不成立时，其有效性会下降：

1. **恒定延迟攻击的盲区**：当攻击者对相机和激光雷达施加**相同的恒定时间偏移**时，跨模态配对的语义一致性得以保持，相似度矩阵的对角线结构不受破坏，DTW 的最优对齐路径仍接近对角线，奖励值不会显著下降。这是 AION 最明确的失效模式。论文明确指出，此类攻击“仅靠跨模态数据难以识别”，需要引入独立时间基准（如 GNSS 时间戳）或额外模态信号（如 IMU 的加速度突变）作为辅助检测源。

2. **传感器模态的覆盖范围**：当前 AION 仅针对相机与激光雷达两种传感器设计，未扩展到 IMU、毫米波雷达、超声波传感器等其他常见自动驾驶模态。在多传感器套件（如多相机环视、多激光雷达、热成像）中的泛化能力尚未验证。

3. **实时性与窗口大小的权衡**：AION 的总推理开销约为 3.26 ms（MRE 编码器 1.74 ms + DTW 检测 1.52 ms），模型参数量约 1.97M（FP32 下约 7.9 MB），在车载嵌入式计算平台上具有可行性。但这一轻量设计依赖于较小的 DTW 窗口（$w = 3 \sim 5$）。对于极端延迟攻击（如秒级以上的时间错位），窗口可能无法覆盖完整的错位范围，需要在窗口大小与计算开销之间权衡。

4. **阈值标定的泛化性**：AION 的异常阈值基于良性数据异常得分的第 99 百分位标定，以控制误报率（FPR）低于 0.01。这一标定策略在不同场景、天气条件或传感器配置下可能需要重新校准，否则可能导致误报率上升或检测灵敏度下降。

### 开放问题

1. **恒定延迟攻击的防御**：如何检测所有传感器被同步偏移相同时间的攻击？可能的路径包括引入独立于传感器网络的绝对时间源（如 GNSS 授时）、利用 IMU 的惯性测量信号（其时间特性不受摄像头/激光雷达时间戳操纵影响），或设计对时间坐标变换具有内在不变性的跨模态表示。

2. **表示空间的直接错位感知**：当前方案依赖 DTW 在相似度矩阵上搜索对齐路径，本质上是后处理检测。能否设计一种表示学习策略，使跨模态表示空间本身对时间错位具有内在敏感性——例如，使错位样本的表示自动偏离良性流形——从而无需显式的序列对齐算法即可检测异常？

3. **多车队列与大规模部署**：在车路协同或多车队列场景中，AION 的阈值一致性与误报率控制如何保证？不同车辆传感器配置、安装误差和网络延迟的差异可能导致异常得分的分布偏移。

4. **对抗性适应攻击**：当前评估假设攻击者不了解 AION 的检测机制。如果攻击者知晓 CACL 的训练策略和 DTW 的评分逻辑，是否可能设计出既能破坏感知输出又能保持相似度矩阵对角线结构的自适应攻击？这需要进一步的安全性分析。

## 原文 PDF

![[paperPDFs/ICLR_2026/Detecting_Temporal_Misalignment_Attacks_in_Multimodal_Fusion_for_Autonomous_Driving.pdf]]
