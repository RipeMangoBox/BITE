---
title: Regulatory Focus Theory Induced Micro-Expression Analysis with Structured Representation Learning
type: paper
paper_level: A
venue: MM
year: 2025
pdf_ref: paperPDFs/MM_2025/AC4AU_Regulatory_Focus_Micro_Expression_Analysis.pdf
project_link: null
code_link: null
aliases:
- RFTIMEASRL
tags:
- MM_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过频率感知冗余分解（FRD）剔除时域直流分量以保留动态交流特征，并利用AU特定专家路由器（AUsER）实现自适应特征分配，从而在无顶点条件下捕获过程敏感的情绪变化。
primary_logic: 基于调控焦点理论，情绪是连续动态过程；通过频域分离静态冗余与动态情绪，并结合混合专家路由学习局部运动模式，可在不依赖顶点标注的情况下达到有竞争力的AU检测性能。
claims:
- AC4AU使用均匀时间采样替代顶点帧，实现完全无顶点（apex-free）的AU检测框架。
- 频率感知冗余分解器（FRD）移除直流分量(DC)，保留交流分量(AC)作为动态情绪变化。
- AU特定专家路由器（AUsER）基于Mixture of Experts，动态分配专家学习局部运动模式。
- AC4AU在严格的LODO协议下取得与依赖于顶点方法相当甚至更优的平均F1分数。
---

# Regulatory Focus Theory Induced Micro-Expression Analysis with Structured Representation Learning

> [!tip] 核心洞察
> 基于调控焦点理论，情绪是连续动态过程；通过频域分离静态冗余与动态情绪，并结合混合专家路由学习局部运动模式，可在不依赖顶点标注的情况下达到有竞争力的AU检测性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 调控焦点理论驱动的结构化表征学习微表情分析 |
| 英文题名 | Regulatory Focus Theory Induced Micro-Expression Analysis with Structured Representation Learning |
| 会议/期刊 | MM 2025 |
| Links |  |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | AC4AU |
| Dataset | CD6ME |

> [!tip] 效果简介
> - CD6ME (LODO protocol) 上，Average F1 across 12 AUs 40.508 vs 39.542 (Off-ApexNet) (+0.966)。

## 概要

微表情（Micro-Expressions, MEs）是面部肌肉无意识收缩产生的短暂、低强度表情，持续时间通常为1/25至1/5秒。现有微表情动作单元检测（Action Unit Detection, AUD）方法普遍依赖人工标注的顶点帧（apex frame）来提取光流或帧间差异特征，这一范式存在两个根本性瓶颈：**高信息冗余**与**静态特征主导**。具体而言，从顶点帧提取的空间表征包含大量与情绪无关的静态外观信息（如身份、光照），而真正承载情绪线索的动态变化被淹没其中；同时，顶点依赖导致时序建模不完整——仅使用起始帧与顶点帧两个时间点，丢失了情绪展开的完整过程信息。此外，微表情数据集中严重的AU样本不平衡进一步削弱了模型的泛化能力。

本文基于**调控焦点理论**（Regulatory Focus Theory）的核心洞见——情绪是一个连续的动态过程而非离散快照——提出了一种完全无顶点（apex-free）的微表情AU检测框架**AC4AU**。该框架通过三个关键设计突破上述瓶颈：

1. **频率感知冗余分解器（Frequency-aware Redundancy Decomposer, FRD）**：沿时间维度执行实值离散傅里叶变换（rDFT），将空间特征分解为时域不变的直流分量（DC）与动态变化的交流分量（AC）。DC分量捕捉与情绪无关的静态冗余（如身份信息），AC分量则保留了过程敏感的动态情绪变化。框架仅保留AC分量进行后续建模，从信号层面实现了冗余与动态的因果分离。

2. **AU特定专家路由器（AU-specific Expert Router, AUsER）**：基于混合专家（Mixture of Experts, MoE）架构，以12个专家网络动态路由学习不同AU对应的局部面部运动模式，替代了传统方法中依赖预定义兴趣区域（RoI）的固定先验特征选择。门控网络自适应地为每个AU分配专家权重，使模型能够捕捉AU间复杂的共现与互斥关系。

3. **类别感知Focal Loss**：针对微表情AU检测中严重的正负样本不平衡，引入类别特定的Focal Loss，通过调节因子降低易分类样本的损失权重，使训练聚焦于难分类的稀少AU类别。

在严格遵循CD6ME基准的留一数据集外（Leave-One-Dataset-Out, LODO）协议下，AC4AU以均匀时间采样至固定8帧的完全无顶点设置，取得平均F1分数**40.508**，优于依赖顶点标注的最强基线Off-ApexNet（39.542）。消融实验证实，移除FRD、AUsER或替换Focal Loss均导致性能显著下降，验证了各组件的独立贡献。AC4AU首次证明了在不依赖顶点标注的条件下，通过频域冗余分解与自适应专家路由，可以达到与顶点依赖方法相当甚至更优的AU检测性能。



微表情（Micro-Expressions, MEs）是一种短暂、不自主的面部运动，通常持续不到半秒，能够揭示个体试图隐藏的真实情绪状态。与宏观表情不同，微表情的强度极低、持续时间极短，使其在安全审讯、临床诊断和人机交互等高风险场景中具有独特的应用价值。然而，微表情的自动分析——特别是面部运动单元（Action Unit, AU）检测——长期面临两个相互交织的核心瓶颈。

**瓶颈一：高信息冗余与静态特征主导。** 微表情序列中，面部外观的大部分变化来源于身份、光照和头部姿态等时域不变因素，而非情绪驱动的动态运动。现有方法普遍依赖光流（optical flow）在起始帧（onset）与顶点帧（apex）之间提取运动信息（如**LBP-TOP+** 、**MDMO+** 、**Off-ApexNet** 、**STSTNet** ），但光流本身仍包含大量静态冗余成分，导致模型难以聚焦于真正承载情绪信息的动态变化。如Figure 1所示，传统方法提取的特征中，黄色实线椭圆标注的冗余信息与黑色虚线椭圆标注的相似模式交织，使不同微表情样本在特征空间中产生模糊分组。

**瓶颈二：对顶点帧的强依赖导致时序建模不完整。** 现有AU检测范式几乎全部建立在人工标注的顶点帧之上——研究者需精确标注每段微表情序列中情绪强度达到峰值的那一帧，再以此为中心提取特征。这一依赖带来三重限制：（1）顶点帧的人工标注成本极高，且标注一致性受主观因素影响严重；（2）将动态情绪过程压缩为单帧快照，丢弃了从起始到顶点再到消退的完整时序信息，违背了调控焦点理论（Regulatory Focus Theory）所强调的情绪是连续动态过程的本质；（3）如CD6ME基准所揭示，跨数据集的顶点信息泄漏问题会高估模型泛化能力，削弱评估的可靠性。

上述瓶颈共同指向一个根本性问题：**如何在无需顶点标注的条件下，从高冗余的微表情序列中提取过程敏感的动态情绪表征？** 现有方法要么依赖手工设计的RoI先验（如Figure 2所示，在预定义兴趣区域内提取局部特征），要么采用端到端学习但仍在顶点帧约束下工作，均未能同时解决冗余消除与顶点解耦这两个挑战。

本文的动机正是基于调控焦点理论，将微表情视为连续动态过程，而非离散快照的集合。我们提出AC4AU——一个完全无顶点（apex-free）的AU检测框架，通过频率域冗余分解与混合专家动态路由两个核心机制，在消除时域静态冗余的同时学习AU特定的局部运动模式，从而在不依赖任何顶点标注的条件下达到与顶点依赖方法相当甚至更优的检测性能。



## 核心方法与创新机理

AC4AU的核心创新在于将微表情分析从“顶点帧依赖”范式彻底转向“动态过程感知”范式，其关键突破体现在三个递进的层面。

### 范式转换：从顶点依赖到无顶点动态建模

传统微表情AU检测方法（如**Off-ApexNet** (Gan et al., 2019)、**STSTNet** (Liong et al., 2019)）高度依赖人工标注的顶点帧（apex frame）来计算光流或提取特征，这一设计存在两个根本性缺陷：一方面，顶点标注本身主观性强、成本高昂，且引入了CD6ME基准明确指出的数据泄漏风险；另一方面，将动态情绪过程压缩为单帧快照，导致时序建模不完整，丢失了情绪变化的关键过程信息。

AC4AU通过简单的均匀时间采样策略（固定采样至8帧）完全取消了顶点依赖，仅保证起始帧已知。这一设计使框架在更严格的条件下运行，却依然取得了与顶点依赖方法相当甚至更优的性能（Table 1：平均F1 40.508 vs. 最佳基线Off-ApexNet 39.542）。其背后的理论支撑来自**调控焦点理论**（Regulatory Focus Theory）——情绪并非离散的静态状态，而是连续的动态过程，因此捕捉过程敏感的变化比定位单帧顶点更具本质意义。

### 频域冗余分解：分离静态身份与动态情绪

微表情视频帧中同时包含两类信息：与身份相关的时域不变冗余（静态成分）和与情绪相关的时域变化信号（动态成分）。传统方法使用光流或原始帧特征，两类信息混杂，导致模型难以聚焦于微弱的动态情绪线索。

AC4AU引入**频率感知冗余分解器**（Frequency-aware Redundancy Decomposer, FRD），通过实值离散傅里叶变换（rDFT）沿时间维度对空间特征进行频域分解：

$$\widehat{F}_{k,c} = \sum_{t=0}^{l-1} F_{t,c} \cdot e^{-2\pi i k t / l}$$

其中零频率分量（$k=0$）对应直流分量（DC），捕捉时域不变冗余：

$$F^{\mathrm{DC}} = \Re\left(\widehat{\mathbf{F}}_0\right) \in \mathbb{R}^{C'}$$

非零频率分量（$k \ge 1$）对应交流分量（AC），承载动态情绪变化，通过逆变换重建：

$$\mathbf{F}_t^{\mathrm{AC}} = \Re\left(\sum_{k=1}^{\lfloor l/2 \rfloor} \widehat{F}_{k,c} \cdot e^{2\pi i k t / l}\right)$$

FRD仅保留AC分量用于后续AU检测，而将DC分量导向身份分类的辅助监督分支。消融实验（Table 2）证实，移除FRD（保留原始混合特征）会导致性能下降，验证了频域分离对AU检测的关键作用。可视化对比（Figure 5）进一步表明，AC成分能够清晰突出与AU激活相关的面部运动区域，而光流和原始特征则包含大量与情绪无关的冗余信息。

### 动态专家路由：从固定RoI到自适应运动模式学习

传统方法依赖预定义的面部兴趣区域（Region of Interest, RoI）提取局部特征，这种固定先验无法适应不同AU在空间分布和运动模式上的差异。AC4AU提出**AU特定专家路由器**（AU-specific Expert Router, AUsER），基于混合专家（Mixture of Experts, MoE）架构，通过12个专家网络和一个门控网络实现自适应的特征分配：

$$\hat{y}_k = \sum_{m=1}^{12} \alpha_{k,m} \cdot E_m(\mathbf{f})$$

其中$\alpha_{k,m}$由门控网络根据输入语义动态生成，使每个AU能够从专家池中选择性地获取相关知识。这一设计等价于让模型自主学习每个AU的“虚拟RoI”，无需人工定义，且能捕捉AU间的共现与互斥关系。消融实验（Table 2）表明，将AUsER替换为共享全连接层会导致性能下降，验证了AU特定专家路由对判别能力的增强作用。

### 损失函数设计：应对极端类别不平衡

微表情AU标注存在严重的类别不平衡问题——某些AU（如AU4、AU7）出现频率极低，而另一些AU（如AU12）则相对常见。AC4AU采用**类别感知的Focal Loss**替代常规二元交叉熵：

$$\mathcal{L}_{AU} = -\sum_{k=1}^{12} \Big[ (1-\alpha_k)(1-\hat{y}_{i,k})^2 y_{i,k} \log(\hat{y}_{i,k}) + \alpha_k \hat{y}_{i,k}^2 (1-y_{i,k}) \log(1-\hat{y}_{i,k}) \Big]$$

其中$\alpha_k$为第$k$个AU的正样本先验比例，$(1-\hat{y})^2$和$\hat{y}^2$分别为正负样本的调制因子，使模型聚焦于难分类样本而非被大量易分类负样本主导。消融实验（Table 2）证实，用标准交叉熵替代Focal Loss会降低性能，尤其对低频AU的检测影响显著。

### 创新总结

AC4AU的创新链条清晰且自洽：**取消顶点依赖**降低了标注成本和数据泄漏风险；**频域冗余分解**从信号层面分离静态身份与动态情绪，使模型聚焦于过程敏感的变化；**动态专家路由**从结构层面替代固定RoI，实现自适应的局部运动模式学习；**类别感知损失**从优化层面应对样本不平衡。这三层设计共同构成了一个完整的无顶点AU检测框架，在严格的LODO协议下验证了其有效性。



AC4AU 的整体设计围绕一个核心矛盾展开：微表情序列中静态身份信息与动态情绪线索高度耦合，而传统方法依赖顶点帧的光流计算进一步放大了冗余并割裂了时序完整性。为此，AC4AU 构建了一条从均匀采样到 AU 预测的端到端流程，完全取消顶点帧依赖，通过频域分离与混合专家路由实现动态情绪表征的学习。

### 框架概览

如图 3 所示，AC4AU 由三个串联的功能模块构成：

1. **噪声鲁棒空间表示骨干**：以预训练的 MobileFaceNet 为基础，嵌入空间 Transformer 编码器，从均匀采样的固定长度序列中提取带有长程空间依赖的帧级特征 $\mathbf{F} \in \mathbb{R}^{l \times C'}$，无需显式人脸对齐。
2. **频率感知冗余分解器（FRD）**：对 $\mathbf{F}$ 沿时间维度执行实值离散傅里叶变换（rDFT），将零频率分量 $\mathbf{F}^{\mathrm{DC}}$ 作为时域不变冗余剔除，仅保留由非零频率重建的交流分量 $\mathbf{F}^{\mathrm{AC}}$，从而隔离出与情绪变化相关的动态特征。
3. **时序建模与 AU 特定专家路由器（AUsER）**：$\mathbf{F}^{\mathrm{AC}}$ 经时序 Transformer 建模长期依赖后，送入一个包含 12 个专家的混合专家（MoE）层。门控网络根据输入语义为每个 AU 动态分配专家权重，生成 12 个 AU 的独立预测。

整个框架将 AU 检测形式化为多标签二分类问题，输入为一段均匀采样至 8 帧的微表情序列，输出为 12 个 AU 的激活概率向量。

### 输入输出与数据流

**输入**：一段微表情视频序列，仅保证起始帧（onset frame）已知，不依赖顶点帧标注。所有序列被均匀采样至固定长度 $l=8$，人脸区域缩放至 $3 \times 112 \times 112$。

**数据流**：
- **空间编码阶段**：MobileFaceNet 提取初始空间特征后，空间 Transformer（4 头注意力 + 轻量残差映射）增强帧内空间关系，输出 $\mathbf{F} \in \mathbb{R}^{l \times C'}$。
- **频域分解阶段**：FRD 对 $\mathbf{F}$ 的每个通道独立执行 rDFT（式 1），提取 DC 分量（式 2）作为静态冗余，利用剩余频率分量重建 AC 特征 $\mathbf{F}^{\mathrm{AC}}$（式 3）。DC 分量被送入一个角度边缘分类损失以监督主体不变表征的学习，AC 分量则流入下游时序模块。
- **预测阶段**：时序 Transformer 对 $\mathbf{F}^{\mathrm{AC}}$ 建模帧间依赖，AUsER 的门控网络为每个 AU $k$ 输出 12 维权重向量 $\alpha_k$，加权组合 12 个专家的输出得到 AU 预测 $\hat{y}_k$（式 5）。最终通过类别感知 Focal Loss（式 8）处理严重的 AU 样本不平衡。

### 与先前方法的流程对比

传统方法（图 2）的典型流程为：起始帧 → 顶点帧 → 光流计算 → 预定义 RoI 特征提取 → AU 分类。这一范式存在两个结构性缺陷：一是顶点帧的人工标注引入主观偏差和数据泄漏风险，二是光流特征本质上仍包含大量静态外观信息，且 RoI 的先验选择限制了模型对非典型运动模式的感知能力。

AC4AU 通过“均匀采样 → 频域冗余分离 → 动态专家路由”的替代路径（图 1），将顶点依赖和 RoI 先验一并移除。FRD 的 DC/AC 分离机制从信号层面解决了静态冗余对动态线索的压制，而 AUsER 的 MoE 路由则以数据驱动的方式替代了手工设计的 RoI 选择，使模型能够自主学习每个 AU 对应的局部运动模式。

### 补充图表

![[assets/figures/papers/paper_list_l1647_AC4AU_Regulatory_Focus_Micro_Expression_Analysis/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed AC4AU. The noise-robust spatial representation*



AC4AU 由三个核心模块串联构成：**噪声鲁棒空间表示骨干**、**频率感知冗余分解器（FRD）** 和 **时序建模与 AU 特定专家路由器（AUsER）**。整体流程为：对微表情视频序列进行均匀时间采样至固定长度 $l=8$ 帧，经空间骨干提取帧级特征，再由 FRD 在频域分离静态冗余与动态情绪成分，最后通过时序 Transformer 与 MoE 路由生成 12 个 AU 的多标签二分类预测。

---

### 3.1 噪声鲁棒空间表示骨干

该模块以预训练的 MobileFaceNet 为基础，引入空间 Transformer 编码器，在不依赖显式人脸对齐的前提下提取具有长程依赖的空间特征。具体而言，每帧图像被重塑为空间 token 序列 $\mathbf{X} \in \mathbb{R}^{(B \times l) \times (H \times W) \times C}$，并添加可学习位置嵌入 $\mathbf{E}$：

$$\mathbf{X} \gets \mathbf{X} + \mathbf{E}$$

空间 Transformer 编码器配备 4 个注意力头，通过多头自注意力更新 $\mathbf{X}$，再经三层卷积构成的轻量残差映射细化，最终输出帧级空间表示 $\mathbf{F} \in \mathbb{R}^{l \times C'}$。

---

### 3.2 频率感知冗余分解器（FRD）

FRD 是 AC4AU 实现无顶点（apex-free）AU 检测的关键。其核心机制为：沿时间维度对 $\mathbf{F}$ 执行**实值离散傅里叶变换（rDFT）**，将帧级表示分解为零频率的直流分量（DC）与非零频率的交流分量（AC）。

**rDFT 变换**（Eq. 1）：

$$\widehat{F}_{k,c} = \sum_{t=0}^{l-1} F_{t,c} \cdot e^{-2\pi i k t / l}, \quad k = 0, 1, \ldots, \left\lfloor \frac{l}{2} \right\rfloor$$

其中 $t$ 为时间索引，$c$ 为通道索引，$k$ 为频率索引。

**DC 分量提取**（Eq. 2）——零频率项捕获时域不变冗余（如身份、光照等静态信息）：

$$F^{\mathrm{DC}} = \Re\left(\widehat{\mathbf{F}}_0\right) \in \mathbb{R}^{C'}$$

**AC 分量重建**（Eq. 3）——利用所有非零频率成分重建动态特征，保留情绪相关的过程敏感变化：

$$\mathbf{F}_t^{\mathrm{AC}} = \Re\left(\sum_{k=1}^{\lfloor l/2 \rfloor} \widehat{F}_{k,c} \cdot e^{2\pi i k t / l}\right)$$

FRD 仅保留 AC 分量 $\mathbf{F}^{\mathrm{AC}}$ 送入后续模块，DC 分量则被分离并用于身份监督（见损失函数部分），从而在特征层面消除静态冗余对动态情绪线索的干扰。

---

### 3.3 AU 特定专家路由器（AUsER）

AUsER 以混合专家（Mixture of Experts, MoE）架构实现自适应特征分配，替代传统方法中基于预定义兴趣区域（RoI）的固定先验选择。该模块包含 12 个专家网络 $\{E_m\}_{m=1}^{12}$ 和一个门控网络，为每个 AU 动态组合专家知识。

**AU 预测公式**（Eq. 5）——对第 $k$ 个 AU，门控网络输出权重 $\alpha_{k,m}$，加权组合各专家对输入特征 $\mathbf{f}$ 的响应：

$$\hat{y}_k = \sum_{m=1}^{12} \alpha_{k,m} \cdot E_m(\mathbf{f})$$

其中 $\mathbf{f}$ 为时序 Transformer 处理 AC 分量后的特征。门控网络根据输入语义自适应调制专家贡献，使每个 AU 能够从专家池中选择最相关的局部运动模式知识，无需显式定义面部区域。

---

### 3.4 双分支损失函数

为同时监督静态表示的个体不变性学习和动态特征的 AU 判别性学习，AC4AU 采用双分支损失：

**角度边缘个体分类损失** $\mathcal{L}_{DC}$（Eq. 7）——作用于 DC 分量，通过角度边缘约束鼓励学习个体无关的静态表示：

$$\mathcal{L}_{DC} = -\log \frac{e^{32 \cdot (\cos(\theta_{z_i} + 0.5))}}{e^{32 \cdot (\cos(\theta_{z_i} + 0.5))} + \sum_{j \neq z_i} e^{32 \cdot \cos(\theta_j)}}$$

其中 $\theta_{z_i}$ 为特征与正确类别原型间的角度，边缘参数设为 0.5，缩放因子为 32。

**类别感知 Focal AU 损失** $\mathcal{L}_{AU}$（Eq. 8）——作用于 AC 分量经 AUsER 后的预测，通过 AU 特定的正样本先验 $\alpha_k$ 加权，缓解严重的类别不平衡：

$$\mathcal{L}_{AU} = -\sum_{k=1}^{12} \Big[ (1-\alpha_k)(1-\hat{y}_{i,k})^2 y_{i,k} \log(\hat{y}_{i,k}) + \alpha_k \hat{y}_{i,k}^2 (1-y_{i,k}) \log(1-\hat{y}_{i,k}) \Big]$$

其中 $\alpha_k$ 为第 $k$ 个 AU 在训练集中的正样本比例，调节因子指数设为 2。总损失为 $\mathcal{L} = \mathcal{L}_{AU} + \gamma \mathcal{L}_{DC}$，$\gamma$ 为平衡系数。

### 补充图表

![[assets/figures/papers/paper_list_l1647_AC4AU_Regulatory_Focus_Micro_Expression_Analysis/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of apex-based methods and our apex-free framework: blue and green dashed ellipses denote MEs, yellow solid ellipses mark redundant information, and black dashed ellipses indicate similar patterns. The dark red dashed ellipse highlights that prior methods, lacking temporal perception and complete representations, often produce ambiguous groupings. Notably, our method eliminates apex reliance by uniformly sampling sequences, with only the onset frame guaranteed*

![[assets/figures/papers/paper_list_l1647_AC4AU_Regulatory_Focus_Micro_Expression_Analysis/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the typical steps in previous methods: (a) Onset frame with predefined RoIs; (b) Apex frame with AU annotations; (c) Optical flow between onset and apex frames; (d) Local representations extracted within the RoIs*



## 实验与关键发现

### 核心实验：LODO协议下的AU检测性能对比

CD6ME基准采用严格的留一数据集（Leave-One-Dataset-Out, LODO）协议，要求模型在三个数据集上轮流训练、在第四个数据集上测试，以评估跨数据集泛化能力。在此协议下，AC4AU以完全无顶点（apex-free）的方式取得了平均F1分数**40.508**，优于所有对比方法，包括依赖人工标注顶点帧（apex frame）的最强基线Off-ApexNet（39.542），提升幅度为**+0.966**（Table 1）。

![[assets/figures/papers/paper_list_l1647_AC4AU_Regulatory_Focus_Micro_Expression_Analysis/figures/005_Table_1.jpg]]
*Table 1: Comparison with State-of-the-arts under the LODO protocol*

这一结果的核心意义在于：AC4AU在**不使用顶点标注**这一更严格条件下，仍然超越了依赖顶点帧光流计算的现有方法。传统方法（如LBP-TOP+、MDMO+、Off-ApexNet、STSTNet）均需借助顶点帧提取光流或计算帧间差异，而AC4AU仅通过均匀时间采样至固定8帧即完成检测，从根本上消除了顶点标注的依赖和数据泄漏风险。

值得注意的是，在12个AU的逐项F1分数中，AC4AU在多个AU上取得最优或次优结果，验证了频率感知冗余分解器（FRD）保留交流（AC）分量、AU特定专家路由器（AUsER）动态分配专家学习局部运动模式的有效性。详细数值请参见Table 1。

### 消融研究：关键组件的贡献验证

消融实验（Table 2）系统验证了AC4AU各核心组件的独立贡献：

![[assets/figures/papers/paper_list_l1647_AC4AU_Regulatory_Focus_Micro_Expression_Analysis/figures/007_Table_2.jpg]]
*Table 2: Ablation Studies*

1. **频率感知冗余分解器（FRD）**：移除FRD、直接使用原始空间特征进行AU预测，导致性能显著下降。这直接证明：通过实值离散傅里叶变换（rDFT）分离时域不变冗余（DC分量）与情绪相关动态（AC分量）是必要的——仅保留AC分量能有效剔除静态身份信息，使模型聚焦于过程敏感的动态情绪变化。

2. **AU特定专家路由器（AUsER）**：将AUsER替换为共享全连接层（shared FC）后性能下降，验证了基于混合专家（Mixture of Experts, MoE）的动态路由机制对AU检测的增益。12个专家通过门控网络自适应调制贡献，使每个AU能选择性地利用相关专家知识，学习局部面部运动模式，而非依赖预定义的兴趣区域（RoI）。

3. **类别感知Focal Loss**：用标准二元交叉熵替代Focal Loss后性能降低，证实了Focal Loss在处理AU样本不平衡问题上的有效性。由于不同AU在数据集中出现频率差异极大（如AU4出现频率远低于AU12），类别感知的Focal Loss通过AU特定的正样本先验权重 $\alpha_k$ 和调制因子 $(1-\hat{y})^2$，有效缓解了长尾分布对模型训练的负面影响。

4. **预训练骨干网络**：消融实验同时验证了基于MobileFaceNet的噪声鲁棒空间表示模块对性能的基础性贡献，其空间Transformer编码器通过4头注意力机制和轻量残差映射，在无需显式人脸对齐的条件下提取了具有长程依赖的空间特征。

### 敏感性分析：损失平衡系数的影响

AC4AU的总体损失函数由角度边缘主体分类损失 $\mathcal{L}_{DC}$ 和类别感知Focal AU损失 $\mathcal{L}_{AU}$ 加权组合：$\mathcal{L} = \mathcal{L}_{AU} + \gamma \mathcal{L}_{DC}$。Table 3展示了平衡系数 $\gamma$ 的敏感性分析结果。$\gamma$ 控制静态成分分解监督的强度——过小则DC/AC分离不充分，冗余信息残留；过大则可能抑制动态情绪特征的表达。实验表明存在一个最优区间，在此区间内两类损失协同作用，既保证了主体不变性，又保留了AU判别所需的动态信息。

### 特征可视化分析

**Figure 5** 提供了光流特征与AC4AU所提取AC分量的可视化对比。传统方法依赖的光流（Figure 5b）虽能捕捉帧间运动，但包含大量与情绪无关的刚性头部运动和背景噪声；而AC4AU的AC分量（Figure 5d）通过频域分解剔除了时域不变冗余，聚焦于面部局部区域的动态变化，与AU标注区域（Figure 5a）的对应关系更为清晰。这一可视化直接支撑了FRD设计的合理性。

**Figure 6** 的t-SNE可视化展示了动态情绪表征 $\mathbf{F}^{\breve{A}\setminus}$ 的聚类结构，不同AU激活模式形成可区分的簇，表明AUsER路由后的特征空间具有良好的AU判别能力。

**Figure 7** 的AU间Pearson相关系数聚类热图揭示了12个AU之间的共现与互斥模式：部分AU呈现正相关（如AU6与AU12常协同激活），部分呈负相关或独立。这一发现不仅验证了AU检测中建模AU间关系的必要性，也为AUsER中门控网络学习专家分配提供了可解释性依据——专家路由隐式地捕捉了这种结构化依赖。

### 公平性保障

所有实验严格遵循CD6ME基准的LODO协议，避免跨数据集泄漏。对比方法均在同一评估框架下运行，顶点依赖方法使用官方提供的顶点标注。AC4AU的超参数（如Focal Loss的 $\alpha_k$）基于全数据集一次性计算并固定，无针对特定fold的手动调优，确保了比较的公平性。

### 局限与失败模式

尽管AC4AU在LODO协议下取得了最优性能，但仍存在以下局限：

1. **即插即用部署受限**：当前框架尚未针对真实世界无约束环境进行适配，域偏移和噪声问题仍需进一步研究。
2. **任务范围有限**：仅在AU检测（AUD）任务上验证，尚未扩展到微表情识别（MER）或统一的情绪表征学习。
3. **对极端样本的鲁棒性**：均匀采样至固定8帧的策略基于序列时长分布（Figure 4）设计，对于极短或极长序列的信息保留可能不够充分，需进一步验证边界情况下的性能稳定性。

![[assets/figures/papers/paper_list_l1647_AC4AU_Regulatory_Focus_Micro_Expression_Analysis/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of temporal length distributions, a few excessively long samples are truncated for clarity*

### 开放问题

在CD6ME基准上，如何将AU检测与情绪识别统一为单一情感表征框架，是下一步的关键方向。此外，结合大语言模型（LLM）和动态网络规划以提升微表情分析的可靠性与公平性，以及扩展到更细粒度的面部运动单元或多模态信息融合，均值得探索。

### 补充图表

![[assets/figures/papers/paper_list_l1647_AC4AU_Regulatory_Focus_Micro_Expression_Analysis/figures/008_Figure_5.jpg]]
*Figure 5: Comparative visualization of ME features extracted by optical flow and our method. (a) Onset frame with AU annotations. (b) Optical flow adopted by previous methods. (c) General facial representations retaining temporal redundancy. (d) AC component highlighting emotional dynamics*

![[assets/figures/papers/paper_list_l1647_AC4AU_Regulatory_Focus_Micro_Expression_Analysis/figures/009_Figure_6.jpg]]
*Figure 6: Visualization of dynamic emotional representations*

![[assets/figures/papers/paper_list_l1647_AC4AU_Regulatory_Focus_Micro_Expression_Analysis/figures/010_Figure_7.jpg]]
*Figure 7: Clustered heatmap of Pearson correlation coefficients, revealing positive and negative AUs patterns*

![[assets/figures/papers/paper_list_l1647_AC4AU_Regulatory_Focus_Micro_Expression_Analysis/figures/006_Figure.jpg]]
*Figure: (a) Onset (b) Optical Flow (c) F (d) FAC*



## 定位与知识库关联

### 1. 方法谱系：从顶点依赖到无顶点动态建模

AC4AU 处于微表情动作单元检测（AUD）从“静态顶点快照”向“连续动态过程”范式转移的关键节点。其方法谱系可沿两条轴线梳理：**时序建模方式**与**特征冗余处理策略**。

#### 1.1 顶点依赖方法的瓶颈

传统 AUD 方法的核心工作流如 Figure 2 所示：以人工标注的起始帧（onset）和顶点帧（apex）为锚点，计算两帧之间的光流，再在预定义兴趣区域（RoI）内提取局部表征。这一范式存在三个结构性缺陷：

- **顶点标注依赖**：顶点帧需人工逐帧标注，成本高昂且存在主观偏差。CD6ME 基准（Li et al., 2023）明确指出，混合使用不同标注来源的数据会导致信息泄漏，因此强制采用留一数据集（LODO）协议。
- **时序信息丢失**：光流仅捕获起始帧到顶点帧的净位移，忽略了微表情从产生、发展到消退的完整动态过程。如 Figure 1 中深红虚线椭圆所示，缺乏时序感知的方法往往产生模糊的类别分组。
- **静态冗余主导**：光流本身仍包含大量与身份、光照相关的静态信息，情绪相关的动态信号被淹没。

代表性顶点依赖方法包括：

| 方法 | 类型 | 顶点依赖 | 核心思路 |
|------|------|----------|----------|
| **LBP-TOP** (Zhao & Pietikäinen, 2007) | 手工特征 | 是 | 三正交平面局部二值模式 |
| **MDMO** (Liu et al., 2016) | 手工特征 | 是 | 主方向平均光流特征 |
| **Off-ApexNet** (Gan et al., 2019) | 深度学习 | 是 | 基于顶点帧的深度光流网络 |
| **STSTNet** (Liong et al., 2019) | 深度学习 | 是 | 浅层三维时空网络 |

这些方法在 CD6ME 基准上的平均 F1 分数（Table 1）从 31.138（LBP-TOP）到 39.542（Off-ApexNet）不等，构成了 AC4AU 的直接对比基线。

#### 1.2 AC4AU 的方法定位

AC4AU 的突破在于**同时解决了顶点依赖和静态冗余两个问题**，其核心设计选择可直接对标基线方法的三个关键槽位：

| 设计槽位 | 基线方法 | AC4AU | 机制差异 |
|----------|----------|-------|----------|
| **顶点帧使用** | 依赖人工标注的顶点帧 | 均匀时间采样至固定 8 帧，完全取消顶点依赖 | 从“关键帧快照”转向“全序列过程建模” |
| **冗余处理** | 光流或原始帧特征，包含大量静态冗余 | FRD 通过 rDFT 分离 DC（静态冗余）与 AC（动态情绪），仅保留 AC 成分 | 频域解耦替代空间差分 |
| **特征选择** | 预定义 RoI 的固定先验选择 | AUsER 以 12 个专家的 MoE 动态路由，学习 AU 特定的局部运动模式 | 数据驱动路由替代人工先验 |

这种设计的理论根基来自**调控焦点理论（Regulatory Focus Theory）**——情绪是连续的动态过程，而非离散的顶点快照。AC4AU 通过频域操作将这一理论转化为可计算的架构：DC 分量对应时域不变的身份/光照冗余，AC 分量对应过程敏感的情绪动态。

### 2. 知识库定位：与相关工作的关系

#### 2.1 与微表情识别（MER）的关系

AC4AU 目前仅针对 AUD 任务设计，尚未扩展到微表情识别（MER）。论文明确将此列为局限之一：“还不支持将 AU 检测与情绪分类统一的情感表征”。从知识库角度看，AC4AU 为 MER 提供了潜在的前置模块——其 AC 分量可作为情绪分类的动态输入，但这一桥接尚未建立。

#### 2.2 与面部动作单元检测（AUD）主流方法的关系

在更广泛的 AUD 领域，AC4AU 的贡献可定位为：

- **相对于光流方法**：FRD 以可学习的频域分解替代了手工光流计算，且避免了光流对顶点帧的依赖。
- **相对于 RoI 方法**：AUsER 的 MoE 路由机制替代了预定义区域，使特征选择由数据驱动。这与近期视觉领域“动态路由替代固定先验”的趋势一致。
- **相对于标准分类头**：类别感知 Focal Loss（Eq. 8）显式处理了 AU 检测中严重的样本不平衡问题（某些 AU 出现频率极低），这是对标准二元交叉熵的直接改进。

#### 2.3 与频域学习方法的关系

FRD 的设计借鉴了频域学习中“低频分量捕获全局结构、高频分量捕获局部细节”的直觉，但做了关键适配：将时域零频率分量（DC）定义为“冗余”而非“结构”，将非零频率分量（AC）定义为“情绪动态”而非“细节”。这一语义重映射是 AC4AU 的核心洞察。

### 3. 适用边界与公平性考量

#### 3.1 适用边界

AC4AU 的适用边界受以下因素约束：

- **任务范围**：当前仅验证于 CD6ME 基准上的 12 类 AU 检测，未在微表情识别（MER）或更广泛的面部运动单元任务上测试。
- **数据假设**：假设输入为已裁剪的人脸序列，且起始帧已知（但不需要顶点帧）。在完全无约束的真实场景中，人脸检测与跟踪的质量将直接影响性能。
- **部署限制**：论文明确指出“AC4AU 目前尚不能直接即插即用地部署于真实场景”，域偏移和噪声鲁棒性问题尚未解决。

#### 3.2 公平性评估

AC4AU 在实验设计上体现了较强的公平性意识：

- **协议严格性**：严格遵循 CD6ME 的 LODO 协议，按数据集划分留一验证，避免跨数据集泄漏。
- **对比公平性**：所有对比方法在同一评估框架下运行，顶点依赖方法使用官方提供的顶点标注。AC4AU 在更严格的无顶点条件下仍取得有竞争力的结果（平均 F1 40.508 vs. Off-ApexNet 39.542）。
- **超参数固定**：Focal Loss 的类别权重 α 基于全数据集一次性计算并固定，未针对特定 fold 手动调优，降低了过拟合风险。

### 4. 局限与开放问题

#### 4.1 已确认的局限

1. **部署就绪度不足**：AC4AU 目前仍是实验室基准方法，尚未在真实无约束环境中验证。
2. **任务范围受限**：仅支持 AUD，未建立 AU 检测与情绪分类的统一框架。
3. **模态单一**：仅使用视觉模态，未融合语音、文本等多模态信息。

#### 4.2 开放问题

论文提出的开放问题指向以下研究方向：

- **统一情感表征**：如何在 CD6ME 基准上将 AU 检测与情绪识别统一，建立从低层运动单元到高层情绪类别的端到端表征？
- **大模型整合**：能否结合大语言模型（LLM）的语义理解和动态网络规划能力，提升微表情分析的可靠性与可解释性？
- **鲁棒部署**：在真实世界无约束环境中，如何解决域偏移、光照变化和遮挡带来的噪声问题？
- **细粒度扩展**：未来是否可扩展到更细粒度的面部运动单元（如 AU 强度估计），或支持多模态信息融合以增强判别能力？

这些开放问题表明，AC4AU 在“无顶点 AUD”这一细分问题上建立了新的基线，但其方法思想（频域冗余分解 + 动态专家路由）的泛化潜力尚未被充分探索。后续工作若能在统一表征和鲁棒部署两个方向上取得进展，将显著提升该方法的实际影响力。



## 原文 PDF

![[paperPDFs/MM_2025/AC4AU_Regulatory_Focus_Micro_Expression_Analysis.pdf]]
