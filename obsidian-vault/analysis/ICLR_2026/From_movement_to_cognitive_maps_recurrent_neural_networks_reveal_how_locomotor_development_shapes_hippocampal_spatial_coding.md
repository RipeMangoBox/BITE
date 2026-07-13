---
title: "From movement to cognitive maps: recurrent neural networks reveal how locomotor development shapes hippocampal spatial coding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/From_movement_to_cognitive_maps_recurrent_neural_networks_reveal_how_locomotor_development_shapes_hippocampal_spatial_coding.pdf
project_link: null
code_link: https://github.com/marcoabrate/movement2cogmaps
openreview_forum_id: 8bM7MkxJee
aliases:
- RSTADS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "运动模式的发育时序（爬行 crawl → 行走 walk → 奔跑 run → 成年 adult）是决定空间表征成熟的可控变量；特定的运动统计（速度分布、旋转速度、空间转换概率）通过课程学习塑造了空间编码的涌现。"
primary_logic: "基于预测学习的浅层循环神经网络，在经历与发育阶段匹配的运动轨迹时，能够自发模拟出海马位置细胞和头方向细胞的发育时间线；网格细胞输入对于成年位置细胞的完全成熟至关重要；模型预测的位置-方向联合编码细胞在真实大鼠海马记录中得到验证，揭示了方向选择性主要通过联合编码细胞而非纯头方向细胞发育增加。"
claims:
- "通过高斯混合模型和 BIC 最小化，从实验数据中识别出三个发育运动阶段：爬行（中位年龄 P13.5）、行走（P16）和奔跑（P20），外加成年组。"
- "顺序训练的 RNN 在 walk→run→adult 阶段的空间调谐（SI_r, SI_d, RVL）和细胞比例均呈现显著上升趋势，与实验数据分布高度一致（JS距离低于随机打乱）。"
- "仅改变采样间隔（爬行轨迹加大帧间隔）的模型未能重现空间调谐，BIC 显著差于原始模型（∆BIC > 10），证明特定运动统计的必要性。"
- "模型预测的联合位置-方向细胞在发育过程中逐渐增多，分析新型实验数据验证了该趋势（JT 检验 p<0.01），且成年 CA1 约 25% 锥体细胞具有显著方向性。"
---

# From movement to cognitive maps: recurrent neural networks reveal how locomotor development shapes hippocampal spatial coding

> [!tip] 核心洞察
> 基于预测学习的浅层循环神经网络，在经历与发育阶段匹配的运动轨迹时，能够自发模拟出海马位置细胞和头方向细胞的发育时间线；网格细胞输入对于成年位置细胞的完全成熟至关重要；模型预测的位置-方向联合编码细胞在真实大鼠海马记录中得到验证，揭示了方向选择性主要通过联合编码细胞而非纯头方向细胞发育增加。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从运动到认知地图：循环神经网络揭示运动发育如何塑造海马空间编码 |
| 英文题名 | From movement to cognitive maps: recurrent neural networks reveal how locomotor development shapes hippocampal spatial coding |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=8bM7MkxJee) · [GitHub](https://github.com/marcoabrate/movement2cogmaps) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 浅层循环神经网络（RNN）海马功能模型（sequential training across developmental stages） |
| Dataset | Rate of change model (crawl with extended gaps), Spatial tuning development (walk→run→adult), Crawl-only model |

> [!tip] 效果简介
> - Rate of change model (crawl with extended gaps) 上，BIC（贝叶斯信息准则） 为 原始顺序训练模型，对比 爬行扩展间隔模型，变化 ∆BIC > 10，表明原始模型更有可能生成实验数据。
> - Spatial tuning development (walk→run→adult) 上，SI_r 的 JT 检验 p 值 为 顺序训练 RNN（无网格细胞），对比 实验数据趋势，变化 模型 p < 0.01，实验 p < 0.001（均显著），且 JS 距离显著低于随机打乱。
> - Crawl-only model 上，隐藏层位置解码误差 为 顺序训练 RNN，对比 仅爬行训练模型（匹配总训练量），变化 顺序模型的解码误差明显更低，sRSA 更高，且空间特征更强。

## 概要

海马体中的位置细胞和头方向细胞是构成空间认知地图的核心神经元，但它们在发育过程中顺序涌现的驱动机制长期未明。本研究提出并验证了一个因果假说：**发育过程中运动统计特征的渐进变化——而非简单的感觉输入变化速度或训练数据量——是海马空间编码成熟的关键驱动因素**。

通过无监督聚类分析大鼠出生后第11至25天的运动数据，研究识别出三个发育运动阶段：爬行（中位年龄P13.5）、行走（P16）和奔跑（P20），外加成年组。在此基础上，研究构建了一个基于预测学习的浅层循环神经网络模型，该网络接收视觉和前庭运动输入，以预测下一帧视觉刺激为训练目标。网络按发育顺序进行课程学习——从爬行到行走、奔跑直至成年，每个阶段继承前一阶段的权重。

核心发现是：**经历与发育阶段匹配的运动轨迹时，RNN的隐藏单元自发模拟出海马位置细胞和头方向细胞的发育时间线**——空间信息量（SI_r）、方向选择性（SI_d、RVL）以及功能细胞比例均随运动成熟而显著上升，与真实大鼠CA1区记录数据的分布高度一致。控制实验进一步表明，仅在爬行轨迹上扩展采样间隔以模拟高预测需求的模型无法重现空间调谐的成熟趋势，而仅爬行训练的模型也无法达到顺序训练的空间表征水平，这证实了特定运动统计特征和发育顺序的必要性。

此外，模型预测成年阶段网格细胞输入对于位置细胞的完全成熟至关重要，并预测联合位置-方向编码细胞在发育过程中逐渐增多——这一预测在后续分析真实海马记录数据时得到验证，揭示了方向选择性主要通过联合编码细胞而非纯头方向细胞的发育增加来实现。

本研究的方法论贡献在于将发育神经科学的“行为驱动成熟”假说转化为可操作的循环神经网络计算框架，通过课程学习将运动发育时序与空间表征涌现建立了因果联系，为理解海马-内嗅皮层环路的功能发育提供了新的计算视角。

哺乳动物在出生后早期，海马体中的空间编码神经元——位置细胞（place cells）和头方向细胞（head direction cells）——并非生来成熟，而是经历一个渐进的功能发育过程。位置细胞在幼鼠睁眼前已存在，但空间信息量低、稳定性差；头方向细胞则在睁眼后约一周才出现方向调谐。这一发育时间线的驱动机制长期悬而未决：究竟是感觉输入本身的变化速度决定了空间表征的成熟，还是动物主动运动模式的变化才是关键？

现有研究面临两个核心缺口。其一，发育过程中运动行为的变化如何影响海马空间编码的涌现，缺乏因果性实验证据——我们无法在活体动物中解耦运动发育与感觉发育。其二，现有的海马计算模型多聚焦于成年动物的稳态空间表征，未能解释发育过程中不同细胞类型（位置细胞、头方向细胞）为何按特定顺序出现，以及运动统计特征在其中扮演的角色。

本文的核心动机在于：利用循环神经网络（RNN）作为海马功能的可操作模型，检验“运动发育驱动空间编码发育”这一假设。具体而言，研究者首先对大鼠出生后 P11 至 P25 的运动数据进行无监督聚类，识别出三个发育运动阶段——爬行（crawl，中位年龄 P13.5）、行走（walk，P16）和奔跑（run，P20）——外加成年组（Figure 1c）。随后，通过在仿真环境中按发育顺序向浅层 RNN 呈现不同阶段的运动轨迹，观察隐藏层单元是否能够自发模拟出海马空间细胞的发育时间线。该框架将“运动模式的发育时序”作为可控变量，使得在计算模型中分离运动经验与其他发育因素成为可能。

## 核心方法与创新机理

### 瓶颈突破：运动发育而非感觉变化速度是空间编码涌现的驱动力

本研究解决的核心问题是：海马空间神经元（位置细胞、头方向细胞）在发育过程中顺序出现的驱动机制是什么？传统观点可能倾向于将空间表征的成熟归因于感觉输入变化速度的提升或训练数据量的累积。本研究通过计算建模与实验验证，确立了一个不同的因果机制：**发育过程中运动统计特征的结构性变化——速度分布、旋转速度、空间转移概率——是空间编码成熟的关键驱动因素**。

这一发现通过三个层次的控制实验得到严格验证。首先，**变化速度控制**（Rate of change model）：在爬行轨迹上人为扩大帧间采样间隔，使得相邻帧之间的视觉变化量达到成年水平。该模型的空间调谐指标（SI_r、SI_d、RVL）显著弱于原始顺序训练模型，BIC 差值超过 10（Figure 5, Appendix F.2），表明仅靠提高预测难度无法诱导向空间表征的涌现。其次，**发育顺序控制**（Reversed development model）：从成年运动模式开始逆向训练至爬行模式，网络立即发展出稳健的空间表征，但随后的简化运动训练并未进一步改变空间调谐（Figure A5, A6），证明发育顺序的不可逆性。第三，**行为库/训练量控制**（Crawl-only model）：仅在爬行阶段训练与顺序模型等量的数据，网络未能产生空间表征，位置解码误差显著更高，sRSA 更弱（Figure A5, A6），排除了训练量累积的解释。

### 核心机制：课程学习驱动的空间编码涌现

本研究的核心创新在于将发育建模为**课程学习**（curriculum learning）过程。RNN 按爬行（crawl）→ 行走（walk）→ 奔跑（run）→ 成年（adult）的顺序继承权重进行训练，每个阶段使用与该发育阶段匹配的运动统计特征生成的仿真轨迹。这一设计使得运动模式的复杂度渐进增加，网络在预测视觉刺激的任务压力下，自发涌现出与真实海马神经元高度一致的空间调谐特性。

具体而言，顺序训练 RNN 的隐藏单元在 walk→run→adult 阶段表现出显著上升的空间信息量（SI_r, JT 检验 p < 0.01）、方向选择性（SI_d, RVL, p < 0.001）以及位置细胞/头方向细胞比例（Figure 4a-e）。模型与实验数据在群体分布上的 Jensen-Shannon 距离显著低于随机打乱的零分布（Figure 4f），且这一结果在隐藏层大小 ±25%、训练至 2500 epoch、输入尺寸变化等参数扰动下保持稳健（Figure A3, A4）。

### 关键设计：网格细胞输入对成年位置细胞成熟的必要性

模型揭示了一个此前未被充分认识的现象：**纯空间位置细胞的完全成熟需要网格细胞输入**。在成年阶段引入网格细胞输入——每 90 时间步将隐藏状态初始化为 25 个网格细胞活动的可学习线性投影（Equation 2）——使得位置细胞比例从约 15% 提升至约 25%，达到实验观测水平（Figure 4a，菱形标记 vs 实线）。无网格细胞输入的成年模型，其位置细胞比例显著低于实验数据。这一发现将网格细胞的功能从空间导航的“度量系统”扩展为海马空间表征发育成熟的“催化剂”，为理解网格-位置细胞系统的发育协调提供了新的理论支点。

### 预测性发现：联合位置-方向细胞的发育验证

模型做出了一个可检验的预测：**联合编码位置和方向的细胞比例应在发育过程中逐渐增加**。分析显示，RNN 中同时满足位置细胞和头方向细胞分类标准的隐藏单元比例随发育阶段上升（Figure 4g，实线）。研究者随后在真实大鼠海马 CA1 记录中验证了这一趋势（JT 检验 p < 0.01），且成年 CA1 约 25% 锥体细胞表现出显著方向选择性，与 Acharya et al.（2016）的独立发现一致。这表明，发育过程中方向调谐的增强主要通过联合编码细胞（而非纯头方向细胞）实现——这是一个仅通过行为学观察无法推导的机制性见解。

### 相对于基线方法的 changed slots 总结

| 设计维度 | 基线方法 | 本研究设计 | 证据锚点 |
|---------|---------|-----------|---------|
| 训练轨迹的运动统计 | 单一阶段（仅成年/仅爬行）或人工扩展间隔 | 按发育顺序的阶段特异性运动统计（crawl, walk, run, adult），通过参数搜索匹配实验数据 | Section 2.1, Appendix C, Table A2 |
| 训练顺序与权重继承 | 从头训练单一阶段或逆序训练 | 从前一阶段继承权重的课程学习（crawl→walk→run→adult） | Section 3, "each network inherited weights..." |
| 网格细胞输入（仅成年阶段） | 无网格细胞输入，隐藏状态从零初始化 | 每 90 时间步将隐藏状态初始化为 25 个网格细胞活动的线性投影 | Section 3 (Equation 2), Figure 4 diamonds |

这三个 changed slots 共同构成了从“运动发育”到“空间编码成熟”的因果链条：阶段特异性的运动统计提供了差异化的感觉运动经验，课程学习确保了表征的渐进构建，网格细胞输入则为成年位置细胞的完全成熟提供了必要的空间度量框架。

### 研究目标与核心假设

本研究旨在回答一个发育神经科学中的核心问题：**海马空间神经元（位置细胞、头方向细胞）在发育过程中为何按特定顺序出现？** 作者提出的假设是，发育过程中运动统计特征（速度、转向速度、空间转移概率）的变化是驱动空间编码成熟的关键因素，而非简单的感觉输入变化速度或训练数据量。

为验证这一假设，研究构建了一个从行为到表征的完整计算框架，包含三个递进层次：

1. **发育运动阶段的识别与量化**：从多组发育期大鼠的开放场地探索数据中，提取运动统计特征，通过无监督聚类识别出三个离散的运动发育阶段。
2. **基于运动统计的轨迹仿真**：使用 Ornstein-Uhlenbeck 随机过程，为每个发育阶段生成匹配其运动统计特征的仿真探索轨迹。
3. **浅层循环神经网络（RNN）的海马功能建模**：以视觉预测为训练目标，按发育顺序对 RNN 进行课程学习，观察隐藏层中空间表征的自发涌现。

### 运动发育阶段的识别

研究汇总了来自多项前期工作（Wills et al., 2010; Tan et al., 2015; Muessig et al., 2015; Bassett et al., 2018; Muessig et al., 2019）的大鼠开放场地探索数据，覆盖 P11 至 P25 日龄。对每只大鼠，计算速度的概率密度函数、旋转速度的概率密度函数，以及空间位置间的转移概率矩阵。通过 Jensen-Shannon 距离量化不同年龄间运动统计的差异，构建相关性矩阵（**Figure 1a**），并以 t-SNE 可视化（**Figure 1b**）。

高斯混合模型结合贝叶斯信息准则（BIC）最小化，识别出三个最优聚类（**Figure 1c**），对应三个发育运动阶段：
- **爬行（crawl）**：中位年龄 P13.5
- **行走（walk）**：中位年龄 P16
- **奔跑（run）**：中位年龄 P20

此外，成年大鼠（3-6 月龄）的运动模式作为第四阶段（adult）。这一基于个体而非年龄分组的聚类方法，保留了大鼠间发育速率的个体差异。

### 轨迹仿真与视觉输入生成

基于上述四个运动阶段，使用开源工具箱 **RatInABox**（George et al., 2024）仿真新的探索轨迹。该工具实现 Ornstein-Uhlenbeck 过程——一种具有向中心回归倾向的连续随机游走，通过网格搜索匹配各阶段的速度分布和旋转速度分布（**Table A1, A2**），生成符合发育运动统计的轨迹。

视觉输入通过模拟大鼠视野的全景虚拟相机获取：水平 240°、垂直 120° 的视野被压缩为 **32×16 低分辨率灰度帧**（**Figure 1f**），模拟大鼠在虚拟方形场地（含视觉地标）中的视觉体验（**Figure 1d-e**）。

### RNN 模型架构与训练流程

模型是一个单层循环神经网络，包含 **500 个隐藏单元**，以预测下一帧视觉刺激为训练目标（**Figure 2a**）。在每个时间步 $t$，网络接收三部分输入的拼接：
- 当前视觉帧 $Y_t$
- 速度向量 $\mathbf{v}_t$
- 旋转速度 $\omega_t$

隐藏状态的更新遵循标准 RNN 动力学：

$$H_{t+1} = \sigma \left( X_t W_x^T + H_t W_h^T \right)$$

其中 $X_t$ 为拼接后的输入向量，$\sigma$ 为 sigmoid 激活函数。预测的下一帧 $\tilde{Y}_{t+1}$ 通过线性解码获得：

$$\tilde{Y}_{t+1} = H_{t+1} W_o^T$$

训练损失为预测帧与真实帧之间的 **L1 距离**。

### 课程学习与权重继承

训练采用**顺序课程学习**策略：从爬行阶段开始从头训练，收敛后继承权重，依次在行走、奔跑、成年阶段进行微调。每个阶段训练约 1,500 个 epoch 至收敛（**Figure 2b**），网络成功学习视觉预测任务（**Figure 2c**）。

### 网格细胞输入模块（成年变体）

在成年阶段，引入一个额外的变体模型，包含**网格细胞输入**。具体而言，在轨迹开始时及每 90 个时间步（模拟 1.5 分钟），将隐藏层初始化为 25 个网格细胞群体活动的可学习线性投影：

$$H_t = \begin{cases} G_t W_g^T & \text{when } t \% 90 = 0 \\ \text{Eq. 1} & \text{otherwise} \end{cases}$$

网格细胞的放电率由标准的三波干涉模型定义：

$$G_t^{(i)} = \frac{1}{3} \max\left(0, \sum_{a\in\{0,\pi/3,2\pi/3\}} \cos\left(2\pi \frac{\mathbf{p}_t \mathbf{e}_{\theta+a}}{\lambda_i} + \phi_i\right)\right)$$

该模块的引入旨在检验网格细胞输入对成年位置细胞完全成熟的必要性。

### 空间表征的分析方法

训练完成后，通过以下指标量化隐藏单元的空间调谐特性（详见**实验与分析**章节）：
- **位置空间信息量** $\mathrm{SI}_r$：基于二维位置率图的空间信息
- **方向空间信息量** $\mathrm{SI}_d$：基于极坐标率图的方向信息
- **合向量长度** $\mathrm{RVL}$：方向选择性的度量
- **位置/头方向解码误差**：从隐藏层活动线性解码位置和朝向的精度
- **空间表征相似性分析（sRSA）**：量化神经活动距离与空间距离的对应关系

### 控制实验设计

为分离运动统计特征的关键作用，设计了三个控制条件：
- **变化速度模型（Rate of change model）**：在爬行轨迹上使用扩展的帧间间隔，模拟高预测需求，检验仅有感觉变化速度是否足以产生空间表征。
- **逆序发育模型（Reversed development model）**：从成年运动模式开始，逐渐反向训练至爬行模式，检验发育顺序的必要性。
- **仅爬行模型（Crawl-only model）**：仅在爬行阶段训练相同总量的数据，检验行为库或累积训练量的影响。

这些控制条件共同构成对核心假设的严格检验：**运动模式的发育时序和特定运动统计，而非训练数据量或感觉变化速度，是空间表征涌现的关键驱动因素**。

### 管道架构概览

模型由五个功能模块构成，整体以预测学习为目标：浅层循环神经网络接收当前时刻的视觉与前庭运动输入，预测下一时刻的视觉刺激。训练采用课程学习策略，按发育阶段（crawl → walk → run → adult）顺序继承权重。

#### 视觉输入模块

模拟大鼠全景视野，使用虚拟相机捕获 $32 \times 16$ 低分辨率灰度帧，水平视野 $240^\circ$，垂直视野 $120^\circ$（Figure 1f）。该模块将环境视觉信息压缩为低维输入向量 $Y_t$。

#### 前庭运动输入模块

提供速度向量 $\mathbf{v}_t$ 和旋转速度 $\omega_t$，与视觉输入拼接后作为 RNN 的输入 $X_t$。该模块编码了自运动信息，是空间表征涌现的关键感觉通道。

#### 循环隐藏层

单层 500 个隐藏单元，通过 sigmoid 激活更新状态，抽象了海马-内嗅皮层巡回的动态特性。隐藏状态 $H_t$ 是空间调谐表征（位置细胞、头方向细胞）的载体。

#### 视觉预测输出模块

从隐藏状态通过线性解码器 $W_o$ 预测下一帧视觉刺激 $\tilde{Y}_{t+1}$，使用 L1 损失进行训练。预测误差驱动隐藏层形成对空间结构有效的内部表征。

#### 网格细胞输入模块（仅成年变体）

在成年阶段，每 90 时间步将隐藏层初始化为 25 个预设网格细胞群体活动的可学习线性投影 $W_g$，以促进位置细胞的完全成熟（Figure 4a 菱形标记）。该模块的引入是位置细胞比例达到实验观测水平的关键条件。

### 核心公式

**RNN 隐藏状态更新与预测**（Equation 1）：
$$H_{t+1} = \sigma \left( X_t W_x^T + H_t W_h^T \right)$$
$$\tilde{Y}_{t+1} = H_{t+1} W_o^T$$

其中 $X_t$ 为当前时刻的视觉-前庭拼接输入，$H_t$ 为上一时刻隐藏状态，$W_x$、$W_h$、$W_o$ 为可学习权重矩阵，$\sigma$ 为 sigmoid 激活函数。网络通过最小化预测帧 $\tilde{Y}_{t+1}$ 与真实帧 $Y_{t+1}$ 的 L1 距离进行训练。

**网格细胞初始化的隐藏状态**（Equation 2）：
$$H_t = \begin{cases} G_t W_g^T & \text{当 } t \bmod 90 = 0 \\ \text{Eq. 1} & \text{其他情况} \end{cases}$$

其中 $G_t$ 为 25 个网格细胞的放电率向量，$W_g$ 为可学习的线性投影矩阵。该机制仅在成年阶段使用，每 90 时间步（相当于 1.5 分钟）将网格细胞的空间周期性信息注入隐藏层。

**网格细胞放电率**（Equation 10）：
$$G_t^{(i)} = \frac{1}{3} \max\left(0, \sum_{a\in\{0,\pi/3,2\pi/3\}} \cos\left(2\pi \frac{\mathbf{p}_t \mathbf{e}_{\theta+a}}{\lambda_i} + \phi_i\right)\right)$$

其中 $\mathbf{p}_t$ 为智能体位置，$\mathbf{e}_{\theta+a}$ 为三个方向（间隔 $60^\circ$）的单位向量，$\lambda_i$ 和 $\phi_i$ 分别为第 $i$ 个网格细胞的空间周期和相位偏移。网格细胞参数预先固定，未从预测学习中自发涌现。

**位置率图**（Equation 3）：
$$R_{i,j}^{(k)} = \frac{\sum_t A_t^{(k)} \cdot \mathbb{1}_{\mathbf{p}_t \in \text{Bin}_{(i,j)}}}{\sum_t \mathbb{1}_{\mathbf{p}_t \in \text{Bin}_{(i,j)}}}$$

其中 $A_t^{(k)}$ 为单元 $k$ 在时刻 $t$ 的激活值，$\text{Bin}_{(i,j)}$ 为 $25 \times 25$ 空间网格的第 $(i,j)$ 个位置仓。率图经高斯滤波（$\sigma = 0.75$ bins）平滑后用于空间选择性分析。

**方向调谐的极坐标率图**（Equation 13）：
$$P_i^{(k)} = \frac{\sum_t A_t^{(k)} \mathbb{1}_{\theta_t \in \text{Bin}_i}}{\sum_t \mathbb{1}_{\theta_t \in \text{Bin}_i}}$$

其中 $\theta_t$ 为智能体朝向，$\text{Bin}_i$ 为角度仓。极坐标率图用于量化头方向选择性。

**位置空间信息量**（Equation 14）：
$$\mathrm{SI}_r^{(k)} = \sum_{i,j} \left[ \frac{O_{i,j}}{\|O\|_1} \frac{R_{i,j}^{(k)}}{\widehat{R}^{(k)}} \log_2 \left( \frac{R_{i,j}^{(k)}}{\widehat{R}^{(k)}} \right) \right]$$

其中 $O_{i,j}$ 为智能体在仓 $(i,j)$ 的占用时间，$\widehat{R}^{(k)}$ 为单元 $k$ 的平均放电率。$\mathrm{SI}_r > 0.3$ 的单元被分类为位置细胞。

**方向选择性——合向量长度**（Equation 15）：
$$\mathrm{RVL}^{(k)} = \frac{|\mathbf{r}^{(k)}|}{\sum_i P_i^{(k)}}, \quad \mathbf{r}^{(k)} = \sum_i \exp\left(j \frac{2\pi}{2B_\theta} i\right) P_i^{(k)}$$

其中 $B_\theta$ 为角度仓数量，$\mathbf{r}^{(k)}$ 为复数形式的合向量。RVL 度量方向调谐的集中程度。

**方向空间信息量**（Equation 16）：
$$\mathrm{SI}_d^{(k)} = \sum_i \left[ \frac{D_i}{\|D\|_1} \frac{P_i^{(k)}}{\hat{P}^{(k)}} \log_2 \left( \frac{P_i^{(k)}}{\hat{P}^{(k)}} \right) \right]$$

其中 $D_i$ 为智能体在角度仓 $i$ 的占用时间，$\hat{P}^{(k)}$ 为单元 $k$ 在极坐标率图中的平均放电率。

**位置与头方向解码误差**（Equation 11）：
$$\Delta \mathbf{p}_t = |\mathbf{p}_t - \tilde{\mathbf{p}}_t|_2; \quad \Delta \theta_t = |\theta_t - \tilde{\theta}_t|$$

其中 $\tilde{\mathbf{p}}_t$ 和 $\tilde{\theta}_t$ 分别为从隐藏层活动线性解码的位置和朝向估计值。解码误差随发育阶段下降，反映空间表征的逐步精化。

**空间表征相似性分析距离**（Equation 12）：
$$D_A = 1 - \frac{A_t \cdot A_{t'}}{\|A_t\|_2 \|A_{t'}\|_2}; \quad D_p = \|\mathbf{p}_t - \mathbf{p}_{t'}\|_2$$

其中 $D_A$ 为神经活动向量间的余弦距离，$D_p$ 为对应位置间的欧氏距离。sRSA 通过量化两种距离矩阵的相关性，评估隐藏层活动对环境空间结构的编码程度。

**模型-实验分布验证**（Equation 17）：
$$\mathbf{JS}^{(m)} = \sum_{c\in\{\text{walk, run, adult}\}} \mathbf{JS}(\mathbf{p}_c^{(m)}, \mathbf{q}_c^{(m)})$$

其中 $\mathbf{p}_c^{(m)}$ 和 $\mathbf{q}_c^{(m)}$ 分别为模型与实验数据在发育阶段 $c$ 上指标 $m$ 的分布，$\mathbf{JS}$ 为 Jensen-Shannon 散度。该指标用于量化模型与生物数据在空间调谐分布上的整体一致性。

**贝叶斯信息准则模型比较**（Equation 19）：
$$\mathrm{BIC}_{\mathrm{model}} = -2 \mathrm{LL}_{\mathrm{model}}^{(m)} + d_{\mathrm{model}} \ln(K)$$

其中 $\mathrm{LL}_{\mathrm{model}}^{(m)}$ 为模型在指标 $m$ 上的对数似然，$d_{\mathrm{model}}$ 为模型自由参数数量，$K$ 为数据点数量。BIC 用于在原始发育模型与“变化速率”控制模型之间进行定量比较（$\Delta \text{BIC} > 10$ 表明原始模型显著更优）。

## 实验与关键发现

### 发育运动阶段的识别与仿真轨迹生成

研究首先对出生后第11至25天（P11–P25）大鼠在方形旷场中的运动数据进行无监督聚类分析。通过计算速度概率密度函数、旋转速度概率密度函数以及空间转移概率矩阵的Jensen-Shannon距离，构建了不同年龄大鼠运动统计特征的关联矩阵（Figure 1a）。t-SNE可视化显示运动统计特征呈现明显的聚类结构（Figure 1b），而高斯混合模型结合贝叶斯信息准则（BIC）最小化确定了最优聚类数为3（Figure 1c）。这三个聚类对应的中位年龄分别为P13.5、P16和P20，被依次命名为爬行（crawl）、行走（walk）和奔跑（run）阶段，外加成年（adult）对照组。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_8bM7MkxJee/figures/001_Figure_1.jpg]]
*Figure 1: Clustering analysis of developmental locomotion stages and trajectory simulation. a Correlation matrix of locomotion metrics across rats aged P11-P25 (cold/warm colours indicate low/high correlations). b t-SNE visualisation of the correlation matrix. Marker shapes indicate locomotion clusters, colours show rat ages. c Bayesian information criterion (BIC) values for Gaussian mixture model with varying cluster numbers (lower values indicate better fit, minimum at 3 clusters). d Top view of the virtual arena with landmarks, used for simulations. e Example simulated trajectory showing agent’s past positions (blue, fading with time), current position (red), head direction $\theta$ , velocity v, an...*

基于各阶段的运动统计参数，使用RatInABox工具箱中的Ornstein-Uhlenbeck过程生成仿真轨迹，并通过参数网格搜索使仿真轨迹的运动统计分布与实验数据的JS距离最小化（Table A1, A2）。仿真环境中，虚拟大鼠的视觉输入由全景虚拟相机捕获，产生32×16像素的低分辨率灰度帧，模拟大鼠240°水平视野和120°垂直视野（Figure 1f）。

### 主实验结果：运动发育驱动空间编码的时序涌现

#### 空间调谐的发育成熟

浅层RNN（500个隐藏单元）按crawl→walk→run→adult的顺序进行课程学习，每个阶段继承前一阶段的权重。训练完成后，隐藏单元展现出与真实海马CA1区神经元高度一致的空间调谐发育轨迹（Figure 4）。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_8bM7MkxJee/figures/004_Figure_4.jpg]]
*Figure 4: Maturation of locomotion explains the development of hippocampal spatial cells. We refer to RNNs with the locomotion cluster their training data was simulated from. Experimental data (dotted lines) shows simultaneously recorded ensembles of cells, grouped by the rat’s locomotion stage at the age of recording. Diamonds indicate adult model trained with grid cell input. Asterisks denote significance levels from one-sided pairwise Wilcoxon rank-sum tests (Wilcoxon, 1992) with Benjamini-Hochberg correction (Hollander et al., 2013) testing for increasing differences (exact p-values in Table A4). a Percentage of RNN units (solid line) and percentage (mean±SEM) of hippocampal neurons (dotted line)...*

**位置细胞发育**：从walk到adult阶段，模型位置细胞比例（SI_r > 0.3）呈显著上升趋势（JT检验 p < 0.01），与实验数据趋势一致（Figure 4a, Table A4）。值得注意的是，纯空间位置细胞的完全成熟需要成年阶段引入网格细胞输入——无网格细胞输入的成年模型位置细胞比例约为实验观测值的一半，而加入每90时间步以网格细胞投影初始化隐藏状态的变体后，比例提升至接近实验水平（Figure 4a，菱形标记 vs 实线）。

**方向选择性发育**：模型的方向空间信息量（SI_d）和合向量长度（RVL）同样随发育阶段显著增加（JT检验 p < 0.001），与实验数据高度吻合（Figure 4d,e）。但纯头方向细胞（HD cells）的比例在模型和实验中均未呈现显著发育增长（Figure 4c），提示方向编码的成熟主要体现在联合编码细胞而非纯头方向细胞中。

**联合位置-方向细胞**：模型预测联合位置-方向细胞的比例随发育逐渐增加，这一预测在重新分析的真实大鼠海马记录中得到验证——联合编码细胞比例在发育过程中显著上升（JT检验 p < 0.01, Figure 4g）。该发现与Acharya等人（2016）报告的成年CA1约25%锥体细胞具有显著方向选择性的结果一致。

#### 模型-实验分布验证

为定量评估模型与实验数据的一致性，计算了walk、run、adult三个阶段空间指标（SI_r、SI_d、RVL）分布的Jensen-Shannon距离。通过10,000次随机打乱网络单元所属阶段构建零分布，结果显示模型的JS距离显著低于随机打乱水平（Figure 4f），表明顺序训练模型生成的空间调谐分布与实验数据高度一致。

#### 定性对比

Figure 3展示了模型隐藏单元与真实CA1神经元在率图（rate maps）和极坐标图（polar maps）上的定性匹配。从walk到adult阶段，模型单元的空间选择性逐渐增强，与实验记录中神经元调谐的精细化过程相对应。

### 控制实验与消融分析

#### 运动统计特征的必要性：变化速率模型

为检验空间表征的涌现是否仅由感觉输入的变化速度驱动，而非特定的运动统计特征，研究构建了“变化速率模型”（rate of change model）：在爬行轨迹上扩展帧间间隔，使连续帧之间的L1距离与成年阶段相当（Figure 5d）。该模型在位置和头方向解码误差（Figure 5a）、空间细胞损伤对验证损失的影响（Figure 5b）、空间表征相似性分析（sRSA, Figure 5c）以及隐藏状态Isomap流形（Figure 5e）等多项指标上均显著劣于原始顺序训练模型。BIC比较进一步证实原始模型更有可能生成实验数据（∆BIC > 10），确证了特定运动统计特征——而非单纯的感觉变化速度——是空间表征涌现的关键驱动因素。

#### 发育顺序的必要性：逆序训练与仅爬行训练

逆序训练模型（adult→run→walk→crawl）在成年阶段即刻发展出稳健的空间表征，但后续在更简单运动模式上的训练仅产生有限的空间调谐变化（Figure A5, A6）。仅爬行训练模型（匹配总训练量）则完全未能产生空间表征，其解码误差显著高于顺序训练模型。这些结果表明，空间表征的涌现依赖于运动复杂性的渐进式增加，而非行为库的累积或训练数据量本身。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_8bM7MkxJee/figures/014_Figure.jpg]]
*Figure: A5: Spatial tuning development of alternative hypotheses controls deviates from original model results (development) and does not mimic experimental data (dotted lines). Model data is shown in solid lines with transparency indicating the control runs. Diamonds indicate adult model trained with grid cell input. a Percentage of RNN units (solid lines) and percentage (mean±SEM) of hippocampal neurons (dotted line) classified as place cells. b Min-max normalized spatial information \mathrm { S I } _ { r } (mean±SEM) for rate maps of RNN units (solid) and hippocampal neurons (dotted). c Percentage of RNN units (solid) and percentage (mean±SEM) of hippocampal neurons (dotted) classified as head d...*

#### 网格细胞输入的作用

消融成年阶段的网格细胞输入导致位置细胞比例无法达到实验观测水平（Figure 4a），证实网格细胞信号对位置细胞完全成熟是必要的。但网格细胞模块为预定义的标准网格模式，其参数固定，并未从预测学习中自发涌现。

#### 参数鲁棒性

隐藏层单元数增减25%、训练轮数延长至2500 epoch、输入图片尺寸减半或加倍，均未改变空间调谐的发育成熟趋势（Figure A3, A4）。跨试次相关性分析显示，率图和极坐标率图在验证轨迹前后半段上的Pearson相关系数始终保持在0.8以上（Figure A8），表明空间表征具有高度的试次间稳定性。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_8bM7MkxJee/figures/012_Figure.jpg]]
*Figure: A3: The maturation of spatial tuning does not deviate from the original results (indicated as ”development”) when decreasing/increasing hidden layer size, training longer, and feeding smaller/bigger images. Model data is shown in solid lines with transparency based on the changed parameter. Experimental data is shown with dotted lines. Diamonds indicate adult model trained with grid cell input. a Percentage of RNN units (solid lines) and percentage (mean±SEM) of hippocampal neurons (dotted line) classified as place cells. b Min-max normalized spatial information SIr (mean±SEM) for rate maps of RNN units (solid) and hippocampal neurons (dotted). c Percentage of RNN units (solid) and percenta...*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_8bM7MkxJee/figures/017_Figure.jpg]]
*Figure: A8: Inter-trial stability: Pearson correlation between a rate maps and b polar rate maps, computed on the first and second halves of the held-out validation trajectories across developmental stages. Diamonds indicate adult model trained with grid cell input*

### 失败模式与局限

1. **纯爬行训练失败**：仅在爬行阶段训练的模型无法产生空间表征，即使训练数据量与顺序训练模型相当。这说明爬行阶段的运动统计特征本身不足以驱动空间编码的涌现，需要后续阶段更丰富的运动模式。

2. **网格细胞依赖**：成年模型若无网格细胞输入，位置细胞比例无法达到实验水平，表明模型中的位置细胞成熟依赖外部网格细胞信号，而非完全自组织涌现。

3. **纯头方向细胞比例未显著增加**：模型和实验数据均显示纯头方向细胞比例在发育过程中无显著增长（Figure 4c），方向编码的成熟主要通过联合位置-方向细胞的增加实现。

4. **仿真与生物系统的差距**：模型仅使用简化的视觉（32×16像素全景）和前庭运动信息，未整合触觉、嗅觉等多感官输入；训练轨迹完全基于仿真参数生成，而非真实大鼠的探索数据；网格细胞为预设模块，未模拟其自发涌现过程；实验对比仅限于CA1区记录，未覆盖齿状回、CA3等其他海马亚区。

*Figure 2: Recurrent neural network (RNN) model of hippocampal function. a RNN schematic. At each timestep t, the network received a concatenation of the agent’s visual input $Y _ { t }$ , velocity vector $\mathbf { v } _ { t }$ , and rotational velocity $\omega _ { t }$ . For the adult locomotion stage, an additional variant was trained – where the hidden layer was initialised to a linear projection $W _ { g }$ of a population of grid cells at trajectory onset and every 90 timesteps. The predicted frame $\tilde { Y } _ { t + 1 }$ is decoded from the hidden state with a linear projection $W _ { o }$ and compared to the observed frame $Y _ { t + 1 }$ using the L1 distance. b,c,d RNN trained on simulated trajectories...

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_8bM7MkxJee/figures/015_Figure.jpg]]
*Figure: a b Figure A6: Decoding errors for position and head direction from hidden-layer activity and correlation between agent’s position and hidden state activity remain stable in control runs. Original model results are indicated as ”development”. Transparency indicates control runs. Diamonds indicate adult model trained with grid cell input. a Position decoding errors (mean±SEM) and b head direction decoding errors (mean±SEM) calculated by linear regression on hidden units (50-50 train-test split on validation data). c Spatial representational similarity analysis (mean±SEM) quantifying correlation between agent position and hidden unit activity*

## 定位与知识库关联

### 核心贡献与理论定位

本研究提出了一种**发育课程学习驱动的浅层RNN海马功能模型**，其核心贡献在于揭示了运动统计特征的发育时序——而非单纯的感觉变化速度或训练数据量——是海马空间细胞（位置细胞、头方向细胞）顺序涌现的关键驱动因素。该方法将海马空间认知的发育问题重新表述为**预测学习框架下的课程学习问题**：RNN 通过预测下一帧视觉输入来学习环境结构，而训练轨迹的运动统计特征按发育阶段（crawl → walk → run → adult）逐步复杂化，权重从前一阶段继承。

这一建模策略与传统的海马计算模型形成鲜明对比。经典模型通常直接对成年动物的空间表征进行静态建模，或假设空间细胞的涌现依赖于特定输入类型（如边界信息、网格细胞输入）。本研究则表明，**运动行为本身的发育变化**足以驱动空间表征的逐步成熟，而网格细胞输入仅在成年阶段对位置细胞的完全成熟起必要的辅助作用。

### 与基线方法的对比与消融

论文通过三类控制实验严格检验了核心假设，这些控制实验构成了方法对比的基线：

| 控制模型 | 关键操作 | 核心发现 | 证据锚点 |
|----------|----------|----------|----------|
| **Rate of change model** | 在爬行轨迹上扩展帧间间隔以模拟高预测需求 | 未能重现空间调谐，BIC 显著差于原始模型（∆BIC > 10），证明特定运动统计而非变化速度是关键 | Section 3.3, Figure 5, Appendix F |
| **Reversed development model** | 从成年运动模式开始，逐步反向训练至爬行模式 | 成年阶段立即涌现空间表征，后续简单运动模式几乎不改变空间调谐，证明发育顺序的必要性 | Figure A5, A6 |
| **Crawl-only model** | 仅在爬行阶段训练相同总量数据 | 未能产生空间表征，解码误差更高，sRSA 更弱，证明行为库累积并非充分条件 | Section 3.3, Figure A5, A6 |

这些消融实验共同指向一个结论：**发育过程中运动复杂度的递增轨迹**——而非行为库的简单累积或预测难度的增加——是空间表征涌现的必要条件。此外，去除成年阶段的网格细胞输入导致位置细胞比例无法达到实验观测水平（Figure 4a），表明网格细胞输入在成年空间系统的完全成熟中扮演着不可替代的角色。

### 方法适用边界与局限

**适用边界**：
- 模型适用于研究**运动发育与空间表征涌现之间的因果关系**，尤其适合探究发育时序对神经表征的影响。
- 框架可扩展至其他空间细胞类型（如边界细胞、网格细胞）的发育研究，或用于检验不同运动训练方案对空间认知的影响。
- 课程学习的权重继承机制为研究发育敏感期和关键期提供了可操作的实验平台。

**关键局限**：
1. **感官模态简化**：模型仅使用视觉和前庭运动信息，未整合触觉、嗅觉等多感官输入，与真实大脑的多感官整合存在差距。
2. **网格细胞外源性**：网格细胞输入为预定义的、参数固定的模块，未从预测学习中自发涌现，简化了生物系统中网格细胞的发育过程。
3. **解剖抽象**：模型将海马功能抽象为单层RNN，未显式建模海马亚区（CA1、CA3、齿状回）的具体连接及皮层-海马回路的复杂性。
4. **轨迹仿真偏差**：训练轨迹完全基于仿真的运动统计参数生成，未直接使用真实大鼠的探索数据；虚拟环境特征与真实实验场地存在差异。
5. **发育阶段离散化**：发育阶段的划分依赖于无监督聚类，可能存在其他划分方式，且未探究离散阶段之间是否存在连续渐变。
6. **实验对比范围有限**：仅比较 CA1 区记录，未覆盖齿状回、CA3 等其他海马亚区及内嗅皮层的发育数据。

### 开放问题

1. **网格细胞-位置细胞协同发育**：网格细胞与海马位置细胞在空间系统成熟过程中如何协调相互作用？网格细胞的成熟是否依赖特定的感觉经验？当前模型将网格细胞作为外源输入，未来需探索网格细胞从预测学习中自发涌现的机制。

2. **发育过渡期的突触机制**：在网格细胞成熟的 24 小时过渡期内，突触和网络动态的精确机制是什么？课程学习的权重继承是否能够模拟这一快速过渡？

3. **运动训练的行为干预**：若对发育期的大鼠进行目标性运动训练或制约，是否会改变联合位置-方向细胞的涌现时间或比例？模型预测的联合编码细胞趋势已在实验数据中得到验证（JT 检验 p < 0.01），但行为干预的因果效应尚待检验。

4. **边界细胞的发育轨迹**：边界细胞在不同运动阶段的发育轨迹如何？是否也遵循可预测的顺序？当前框架可通过引入边界相关输入来扩展。

5. **环境-运动交互效应**：运动发育阶段与环境特征（如丰容环境、黑暗饲养）如何交互，以影响空间表征的形成和稳定性？模型可通过改变虚拟环境复杂度来系统探究这一问题。

6. **完整空间认知地图的建模**：能否通过在更复杂的任务中引入其他空间细胞类型（如网格细胞、边界细胞、目标细胞）来扩展模型，实现更完整的空间认知地图？这需要将单层RNN扩展为多模块网络，并引入更丰富的任务结构。

## 原文 PDF

![[paperPDFs/ICLR_2026/From_movement_to_cognitive_maps_recurrent_neural_networks_reveal_how_locomotor_development_shapes_hippocampal_spatial_coding.pdf]]
