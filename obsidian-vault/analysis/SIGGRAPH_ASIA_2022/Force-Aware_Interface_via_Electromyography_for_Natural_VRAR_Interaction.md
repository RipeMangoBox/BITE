---
title: Force-Aware Interface via Electromyography for Natural VR/AR Interaction
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Force_Aware_Interface_via_Electromyography_for_Natural_VR_AR_Interaction.pdf
project_link: null
code_link: null
aliases:
- FAIE
- FAIENVAI
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_rendering_materials
- topic/graphics_animation_interaction
- topic/benchmarks_datasets_evaluation
core_operator: 采用频域 STFT 将 sEMG 信号转为谱图，使用轻量 CNN 瓶颈架构，并设计联合分类-回归损失函数，辅以迁移学习的快速校准策略，实现实时、准确、可泛化的手指力解码。
primary_logic: 通过频域表示和联合损失设计，可实时从非侵入式肌电传感器中解码手指力，无需手部传感器，从而显著增强 VR 中的物理感知和交互自然性。
claims:
- 界面以 3.3% 平均 NRMSE 实时解码手指力。
- 心理物理实验表明，使用力输入比位置输入显著提高用户对虚拟物体刚度的辨别阈值（弹性棒：FORCE 0.09 vs POSITION 0.22，p=1.46e-4）。
- 通过迁移学习，仅需 66 秒校准数据即可达到 83.33% 准确率、4.74% NRMSE。
- 模型轻量（1.26M 参数，~29.19M MACs），推理延迟约 1.2-1.4 ms，系统整体延迟约 18.7 ms。
---

# Force-Aware Interface via Electromyography for Natural VR/AR Interaction

> [!tip] 核心洞察
> 通过频域表示和联合损失设计，可实时从非侵入式肌电传感器中解码手指力，无需手部传感器，从而显著增强 VR 中的物理感知和交互自然性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于肌电信号的力感知接口：实现自然 VR/AR 交互 |
| 英文题名 | Force-Aware Interface via Electromyography for Natural VR/AR Interaction |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://www.immersivecomputinglab.org/publication/force-aware-interface-via-electromyography-for-natural-vr-ar-interaction/) |
| Topic | #topic/graphics_rendering_materials #topic/graphics_animation_interaction #topic/benchmarks_datasets_evaluation |
| Method | Force-Aware Interface via Electromyography |
| Dataset | EMG-Force dataset, Material stiffness discrimination, Multi-finger tapping identification |

> [!tip] 效果简介
> - EMG-Force dataset (user-independent) 上，NRMSE / R² / Accuracy 3.29% / 85.82% / 88.83%。
> - Material stiffness discrimination (elastic rod) 上，discrimination threshold (mean±SD) 0.09±0.07 (FORCE) vs 0.22±0.07 (POSITION) (-0.13 (59% reduction, p=1.46e-4))。
> - Material stiffness discrimination (elastic sheet) 上，discrimination threshold (mean±SD) 0.06±0.04 (FORCE) vs 0.23±0.07 (POSITION) (-0.17 (74% reduction, p=7.16e-7))。

## 概要

VR/AR 交互长期受限于缺乏物理真实感——现有力传感设备笨重且妨碍手部灵巧性，而从非侵入式肌电信号中实时、精确、跨用户解码手指力仍是一个开放挑战。本文提出 **Force-Aware Interface via Electromyography**，一种基于前臂表面肌电（sEMG）的轻量学习型神经接口：将原始 sEMG 信号经短时傅里叶变换转为频域谱图，输入轻量 CNN 编码器-解码器（1.26M 参数），以联合分类-回归损失进行训练，配合时序高斯平滑，实现逐手指连续力估计。

主要结果：用户无关模型在 EMG-Force 数据集上达到 **3.29% NRMSE** 和 **88.83% 准确率**；心理物理实验中，力输入条件（FORCE）相比位置输入（POSITION）将虚拟物体刚度辨别阈值显著降低 59%–74%；通过迁移学习，仅需约 66 秒校准数据即可达到 83.33% 准确率。系统整体延迟约 18.7 ms，支持实时交互。方法定位于 **非侵入式 EMG 力解码**与**轻量实时神经接口**的交叉点，为 VR/AR 中自然物理交互提供了无需手部传感器的新范式。

## 核心方法与创新机理

### 问题瓶颈与设计动机

VR/AR 交互中长期存在一个核心矛盾：物理真实感要求系统感知用户施加的手指力，但现有力传感方案（如数据手套、力传感器）笨重且妨碍手部灵巧性，难以融入日常穿戴场景。前臂肌电信号（sEMG）提供了一条非侵入式通路——手指的屈伸运动由前臂肌群（指浅屈肌、指深屈肌、拇长屈肌等）驱动，这些肌肉的电活动理论上编码了手指力的信息。然而，从 sEMG 中实时、精确、跨用户解码手指力面临三个开放挑战：（1）sEMG 信号信噪比低、易受运动伪迹和汗液干扰；（2）多手指力的信号在肌肉层面高度耦合，难以分离；（3）用户间解剖差异导致信号分布漂移，泛化困难。

本文的核心洞察是：**将 sEMG 信号通过短时傅里叶变换（STFT）映射到频域谱图，配合联合分类-回归损失函数，使轻量 CNN 能够从非侵入式肌电传感器中实时解码手指力，从而在无需手部传感器的情况下显著增强 VR 中的物理感知和交互自然性。**

### 核心方法框架

系统由七个模块串联构成，形成从生物信号采集到力预测输出的完整流水线（Figure 4）：

![[assets/figures/papers/paper_list_l53_https_www_immersivecomputinglab_org_publication_force_aware_interface_vi/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of the deep learning pipeline embedded in our system. To optimize for parameter efficiency and resilience to data noise, we transform raw EMG signals into frequency domain via STFT, treat the resulting spectrograms as multi-channel images, and employ a lightweight CNN model with bottleneck design. Training is performed using a customized classification-regression joint loss tailored to the task of force estimation. When put into action, our system uses a fixed-size sliding window to retrieve the latest frames from wirelessly streamed EMG signals and decodes finger-wise forces in real time*

#### 模块 1：sEMG 信号采集与无线传输
8 通道无线 sEMG 传感器贴附于用户右前臂，以 1926 Hz 采样率采集肌电信号，通过蓝牙实时传输至计算端。传感器位置覆盖前臂前侧肌群，对应拇指和四指的屈肌区域（Figure 2）。

![[assets/figures/papers/paper_list_l53_https_www_immersivecomputinglab_org_publication_force_aware_interface_vi/figures/002_Figure_2.jpg]]
*Figure 2: Anatomical illustration of forearm muscles controlling the flexion and extension of thumb and four fingers. Our system predicts hand-induced forces at finger level by sensing forearm muscle activations with EMG sensors, preserving the dexterity necessary for delicate hand activities in VR/AR*

#### 模块 2：短时傅里叶变换（STFT）——关键 Changed Slot 1
原始时域 EMG 信号直接输入 CNN 存在两个问题：时域波形对噪声敏感，且单帧信号包含的信息量有限。本文的关键设计选择是将信号转换到频域：对每个通道的 EMG 信号施加 STFT，生成时频谱图。谱图以时间帧为横轴、频率分量为纵轴，每个像素值表示该时刻该频率的能量。**仅保留 64 个低频分量**（对应约 0-300 Hz 范围，覆盖 sEMG 的主要能量集中频段），高频分量被截断以去除噪声。这一操作将 8 通道一维时序信号转换为 8 通道二维图像表示，使后续 CNN 能够利用成熟的图像特征提取能力。

因果链路：STFT 频域表示 → 增强信噪比 + 提供局部频谱纹理 → CNN 可学习不同手指激活模式对应的频谱特征组合。

#### 模块 3：滑动窗口输入构建——关键 Changed Slot 2
单帧谱图缺乏时序上下文，难以捕捉力的动态变化过程。系统采用固定大小的滑动窗口，取最近 **32 帧**（对应 624 ms）谱图堆叠作为模型输入。32 帧窗口提供了足够的时序上下文来编码力的起始、持续和释放过程，同时 624 ms 的窗口长度保证了实时性（窗口长度即推理所需的历史数据量）。

因果链路：32 帧滑动窗口 → 提供时序动态信息 → 模型可感知力的变化趋势，减少逐帧独立预测的抖动。

#### 模块 4：轻量 CNN 编码器-解码器——关键 Changed Slot 3
模型采用编码器-解码器架构，设计为瓶颈结构以平衡表达能力和计算效率。编码器通过卷积和池化逐步压缩空间维度、扩展通道数，提取多手指力的耦合特征；解码器通过上采样恢复空间分辨率，最终输出 5 个手指的力预测值。**模型仅含 1.26M 参数，MACs 约 29.19M**，推理延迟 1.2-1.4 ms，满足实时交互需求。

#### 模块 5：联合分类-回归损失——关键 Changed Slot 4（最核心创新）
手指力预测面临一个特殊挑战：手指在大部分时间内处于“无力”状态（未接触物体），力的回归目标高度稀疏。若仅使用 L1 或 L2 回归损失，模型倾向于输出接近零的保守预测，难以捕捉微小的力变化。本文设计了联合分类-回归损失函数，由两部分组成：

**分类损失**（二元交叉熵）：对每个手指每帧判断是否存在力（二分类），公式为：

$$L_{c} = \frac{1}{T \cdot I} \sum_{t=1}^{T} \sum_{i=1}^{I} [- y_{i}^{t} \cdot \log p_{i}^{t} - (1 - y_{i}^{t}) \cdot \log(1 - p_{i}^{t})]$$

其中 $T$ 为时间帧数，$I=5$ 为手指数量，$y_{i}^{t} \in \{0,1\}$ 为真实力存在标签（力值 > 0 即为 1），$p_{i}^{t}$ 为模型预测的力存在概率。

**回归损失**（L2）：仅对真实力值进行回归，公式为：

$$L_{r} = \frac{1}{T \cdot I} \sum_{t=1}^{T} \sum_{i=1}^{I} \Vert \hat{F}_{i}^{t} - F_{i}^{t} \Vert^{2}$$

其中 $\hat{F}_{i}^{t}$ 为预测力值，$F_{i}^{t}$ 为真实力值。

**联合损失**：

$$L = L_{c} + \lambda \cdot L_{r}$$

其中 $\lambda$ 为平衡超参数。分类分支迫使模型首先学习“哪个手指在用力”这一判别性特征，回归分支在此基础上精修力值大小。消融实验（Table 1）证实，联合损失相较于单独 L1/L2 回归损失在 NRMSE 和 R² 上均有显著提升。

因果链路：联合损失 → 分类分支提供力的存在性监督 → 模型学习“力/无力”的判别边界 → 回归分支在有力区域内精修 → 整体预测精度和稳定性提升。

#### 模块 6：时序高斯平滑
模型逐帧预测的力值可能存在高频抖动。系统对输出的力序列应用窗口大小为 10 的高斯滤波，平滑相邻帧间的预测波动。消融实验（Table 1, no-smoothing variant）验证了平滑对预测稳定性的改善。

#### 模块 7：迁移学习快速校准
用户无关模型在跨用户场景下性能下降，需要用户特异性校准。传统方法需大量新用户数据重新训练，本文采用迁移学习策略：冻结编码器的大部分层，仅微调解码器的最后几层和分类头。**仅需 66 秒（约 3300 帧）校准数据**，即可达到 83.33% 分类准确率和 4.74% NRMSE（Figure 8），大幅降低了用户上手成本。

### 训练与推理路径

**训练阶段**：在 EMG-Force 数据集（9 名被试者，8 通道 sEMG + 触控板力真值同步采集，涵盖按压和捏合动作，Figure 5）上，使用联合损失函数端到端训练用户无关模型。输入为 32 帧 × 8 通道 × 64 频率分量的谱图张量，输出为 5 个手指的力存在概率和力值。

**推理阶段**：无线传感器持续流式传输 EMG 信号，系统维护一个 32 帧滑动缓冲区，每收到新一帧即进行一次前向推理。推理延迟 1.2-1.4 ms，加上信号传输和预处理，系统整体延迟约 18.7 ms，满足实时交互需求。

![[assets/figures/papers/paper_list_l53_https_www_immersivecomputinglab_org_publication_force_aware_interface_vi/figures/001_Figure.jpg]]
*Figure: (a) The reaction of virtual balls with different physical properties to varying level of pressing force decoded from forearm electromyography signals. (b) Our system provides a natural and intuitive interface for capturing user-generated forces and letting them take effects in the virtual environment*

![[assets/figures/papers/paper_list_l53_https_www_immersivecomputinglab_org_publication_force_aware_interface_vi/figures/005_Figure_5.jpg]]
*Figure 5: Types of hand-object interaction selected for constructing our EMG-Force dataset. Capital letters before the hyphen, namely T, I, M, R, and P, stand for thumb, index finger, middle finger, ring finger, and pinky finger, respectively*

## 实验与关键发现

### 力估计主结果与消融分析

系统在用户无关（user-independent）设定下，以 **3.29% NRMSE**、**85.82% R²** 和 **88.83% 准确率**实现手指级力解码（Table 1）。消融实验揭示了两个关键设计选择的因果贡献：

![[assets/figures/papers/paper_list_l53_https_www_immersivecomputinglab_org_publication_force_aware_interface_vi/figures/007_Table_1.jpg]]
*Table 1: Performance comparison with regular regression losses*

**联合分类-回归损失**是性能提升的核心瓶颈。与单独使用 L1 或 L2 回归损失相比，联合损失在 NRMSE 上分别降低约 1.2 和 0.8 个百分点，R² 提升约 6–8 个百分点（Table 1）。其机理在于：分类分支（二元交叉熵）迫使网络首先判断每个手指是否正在施力，回归分支（L2）则在有力区间内精细估计力的大小，两者互补地解决了“零力帧主导、有力帧稀疏”的标签不平衡问题。联合损失函数定义为：

$$L = L_{c} + \lambda \cdot L_{r}$$

其中分类损失 $L_{c}$ 为逐帧逐手指的二元交叉熵，回归损失 $L_{r}$ 为预测力与真实力之间的 L2 距离，$\lambda$ 为平衡超参数。

**时序高斯平滑**进一步改善了预测稳定性。去除平滑后（no-smoothing variant），NRMSE 从 3.29% 升至约 3.8%，表明原始逐帧预测存在高频抖动，而窗口大小为 10 的高斯滤波有效抑制了这种帧间噪声（Table 1）。

**频域输入表示**的消融虽无独立表格，但方法设计明确指出仅使用 STFT 谱图的 64 个低频分量，去除了对力估计无贡献的高频肌电噪声（Section 3.3）。这一设计选择与 CNN 将谱图视为多通道图像的处理方式协同，使模型能够从频域模式中学习肌肉激活与手指力的映射。

### 模型效率与系统延迟

模型采用瓶颈架构，参数量仅 **1.26M**，MAC 约 **29.19M**。推理延迟在 PC 端测得 **1.2–1.4 ms**，加上无线传输和 STFT 预处理后系统整体延迟约 **18.7 ms**（Section 4.5）。该延迟水平满足实时 VR 交互需求（通常要求 <20 ms 的动显延迟），且轻量模型可部署于移动端或嵌入式设备。

### 迁移学习的数据效率

用户特异性校准通过迁移学习实现：在用户无关模型基础上，用新用户少量数据微调。Figure 8 显示，仅需约 **66 秒** 的校准数据即可达到 **83.33% 准确率**和 **4.74% NRMSE**；随着数据量增至 165 秒，性能趋于饱和。这一结果表明迁移学习策略大幅降低了新用户的校准负担，但距离零校准泛化仍有差距——约 1 分钟的校准过程在实际应用中可能影响用户体验。

### 心理物理实验：力感知的因果效应

为验证力输入对虚拟物体感知的因果增强，研究者设计了心理物理实验（12 名被试），比较 **FORCE**（力输入）与 **POSITION**（位置输入）两种条件在材料刚度辨别任务上的表现（Figure 11）：

- **弹性棒**：FORCE 辨别阈值为 **0.09±0.07**，POSITION 为 **0.22±0.07**，阈值降低 **59%**（p=1.46e-4）。
- **弹性片**：FORCE 辨别阈值为 **0.06±0.04**，POSITION 为 **0.23±0.07**，阈值降低 **74%**（p=7.16e-7）。

两组结果均达到高度统计显著，且所有 12 名被试的个体阈值在 FORCE 条件下一致更低（Figure 11a），排除了被试间差异的混淆。这一实验直接证明了：**力输入通过提供与真实物理交互一致的感知通道，显著提升了用户对虚拟物体材料属性的辨别能力**，这是单纯位置输入无法实现的。

### 手指敲击识别应用

在多手指敲击识别任务上，系统达到 **92.0% 精确率**和 **92.7% 召回率**（Table 3），表明力解码模型同时具备识别“哪个手指在施力”的能力。这一能力源于联合损失中的分类分支，无需额外训练即可直接应用于手指识别场景。

### 与视觉方法的对比边界

Table 2 将本方法与三种基于视觉的力估计方法（Fallahinia & Mascaro 2021a, 2020, 2021b）进行 NRMSE 对比。需注意该对比存在**跨数据集、跨任务的不对等性**：视觉方法使用不同采集设置和交互类型，NRMSE 数值的直接比较需谨慎解读。论文未提供在相同数据集上的复现结果，因此该对比仅作为性能量级的参考，而非严格的因果消融。

![[assets/figures/papers/paper_list_l53_https_www_immersivecomputinglab_org_publication_force_aware_interface_vi/figures/008_Table_2.jpg]]
*Table 2: Performance comparison with vision-based methods [Fallahinia and Mascaro 2021a, 2020, 2021b] in terms of NRMSE*

### 失败模式与适用边界

基于实验证据和论文自述，系统存在以下明确限制：

1. **交互类型受限**：训练数据仅涵盖按压（pressing）和捏合（pinching）两类动作（Figure 5），模型对握拳、抓取等更复杂手势的泛化能力未经验证。Figure 6a 的动作-wise 分析显示，不同动作间的性能存在差异，但论文未报告具体哪些动作表现较差。

2. **平面交互假设**：力数据通过平面触控板（Morph Sensel trackpad）采集，模型未学习三维物体交互中的力分布模式。在自由形式 VR 操作中，手指与曲面物体的接触力模式可能超出训练分布。

3. **样本多样性不足**：训练集仅 9 名被试（8 男 1 女），心理物理实验 12 名被试。性别、年龄、肌肉发达程度等因素对模型性能的影响未做分层分析，且未包含肢体障碍人群。

4. **主动施力与被动受力的混淆**：肌电信号在主动施力（如按压）与抵抗外力（如握住被推开的物体）时可能呈现不同模式，当前模型未加区分，可能导致在需要同时感知外力的场景中预测失真。

5. **校准依赖**：尽管迁移学习将校准时间压缩至约 1 分钟，但完全消除校准环节的无监督适配仍是待解决问题。

## 定位与知识库关联

本文的核心贡献在于将 VR/AR 力交互的感知源从**手部传感器**迁移至**前臂肌电信号**，并通过一个端到端的深度学习流水线实现实时、精确、跨用户的手指力解码。相对于已有工作的本质差异可归结为四个关键 slot 的改变：

1. **输入表示 slot**：已有 EMG 力估计方法多直接使用时域原始信号或手工特征，而本工作引入 **STFT 频域谱图**作为输入表示，并仅保留 64 个低频分量。这一选择利用了肌电信号在频域中更稳定的能量分布特性，有效抑制了高频噪声和电极位移伪影。

2. **损失函数 slot**：传统力回归任务使用单一的 L1 或 L2 回归损失。本工作设计了**联合分类-回归损失**——将“手指是否施力”的二分类任务与力值回归任务耦合在同一优化目标中。这一设计使模型在学习连续力值时获得了离散状态监督信号的引导，缓解了零力值附近回归不稳定的问题。

3. **时序建模 slot**：替代逐帧独立处理，采用 32 帧（624 ms）滑动窗口作为模型输入，并在输出端施加窗口大小为 10 的**高斯时序平滑**。这种轻量时序上下文设计在不引入循环结构的前提下有效抑制了帧间抖动。

4. **模型架构 slot**：采用**轻量 CNN 编码器-解码器瓶颈架构**（1.26M 参数，~29.19M MACs），而非通用回归 CNN。瓶颈设计强制模型学习紧凑的力相关特征表示，同时保证了推理延迟仅 1.2–1.4 ms，满足实时交互需求。

### 知识库挂载点

本工作在以下知识库节点上建立连接：

- **EMG-based gesture/force interfaces**：本工作将 EMG 接口的能力边界从离散手势分类扩展到**连续手指力回归**。与传统手势识别工作（如基于 sEMG 的抓取类型分类）不同，本文的输出是 5 维连续力向量，且同时支持力值回归和施力手指识别。这一定位使其成为 EMG 交互研究从“分类”到“回归”的典型过渡节点。

- **Wearable force sensing in VR/AR**：与基于手部传感器的力交互方案（如力敏手套、手持力传感器）形成互补关系。本工作的核心优势在于**无需手部传感器**，保留了手指的灵巧性和触觉自由，但代价是力估计精度受限于肌电信号的固有噪声和跨用户变异。可挂载为“非侵入式力感知”分支的代表方法。

- **Deep learning for biosignal processing**：STFT 谱图 + 轻量 CNN 的流水线设计可推广至其他生物电信号（如脑电 EEG、心电 ECG）的回归任务。联合分类-回归损失的设计思路也可迁移至其他存在“零值膨胀”问题的回归场景（如关节力矩估计、肌肉激活度预测）。

- **Transfer learning for user adaptation**：本工作验证了迁移学习在 EMG 力解码中的有效性——仅需 66 秒校准数据即可将用户无关模型适配至新用户。这一发现为 EMG 接口的实用化提供了关键证据，可挂载至“少样本用户适配”知识节点。

### 适用边界与局限

本方法的适用边界需谨慎划定：

- **交互类型受限**：训练数据仅涵盖按压和捏合两类动作（在平面触控板上采集），模型对握拳、抓取三维物体等复杂手部姿态的泛化能力未经验证。在需要自由形式三维物体操作的场景中，力解码精度可能显著下降。

- **施力/受力不可区分**：肌电信号反映的是肌肉激活程度，无法区分主动施力与抵抗外力的被动受力。在涉及双向力交互的场景（如推拉虚拟物体时被反推）中，模型可能产生歧义输出。

- **用户多样性有限**：训练集仅 9 名被试者（8 男 1 女），心理物理实验 12 人，未涵盖肢体障碍人群、不同年龄层或皮肤状态差异较大的人群。跨人群泛化性能需进一步验证。

- **校准仍不可省略**：尽管迁移学习显著减少了校准时间（约 1 分钟），但尚未实现零校准泛化。电极位置偏移、皮肤阻抗变化等因素仍需要一定量的用户特异性数据来补偿。

### 后续启发

本工作为以下研究方向提供了明确起点：

- **多模态融合**：将 EMG 力估计与手部姿态追踪（如基于视觉或 IMU）结合，有望同时解决“施力/受力区分”和“三维交互泛化”两个瓶颈。例如，手部运动学信息可提供关于交互类型的先验，辅助力解码模型消歧。

- **无监督域适应**：探索基于无监督学习的用户适配方法，利用未标注的在线 EMG 数据持续更新模型，逐步逼近零校准目标。

- **力维度扩展**：当前仅解码 5 个手指的法向力，未来可扩展至手指侧向力、扭矩等更多力维度，以支持更精细的灵巧操作（如拧螺丝、捏取薄片等）。

- **与触觉渲染闭环**：将解码的力信号不仅用于驱动虚拟物体形变，还可作为触觉反馈的控制输入，形成“力感知-力反馈”的闭环交互回路，进一步提升物理真实感。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Force_Aware_Interface_via_Electromyography_for_Natural_VR_AR_Interaction.pdf]]