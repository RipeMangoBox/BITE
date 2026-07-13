---
title: "Accelerated co-design of robots through morphological pretraining"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Accelerated_co_design_of_robots_through_morphological_pretraining.pdf
project_link: null
code_link: null
aliases:
- ACDRTMP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过可微分模拟大规模预训练一个形态无关的通用控制器，从而快速评估形态变化并指导进化。"
primary_logic: "形态学预训练使零样本进化成为可能，避免了重复的控制器训练；通过每代微调（few-shot evolution）可以防止多样性崩溃，同时维持高性能和形态多样性。"
claims:
- "预训练通用控制器在超过1000万个不同形态上收敛，性能提升70%"
- "零样本进化在100代内收敛至接近最优，仅需17分钟"
- "少样本进化有效维持并显著增加种群多样性，同时获得高性能"
- "同时协同设计从头训练遭受多样性崩溃，种群收敛到单一物种"
---

# Accelerated co-design of robots through morphological pretraining

> [!tip] 核心洞察
> 形态学预训练使零样本进化成为可能，避免了重复的控制器训练；通过每代微调（few-shot evolution）可以防止多样性崩溃，同时维持高性能和形态多样性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过形态学预训练加速机器人协同设计 |
| 英文题名 | Accelerated co-design of robots through morphological pretraining |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=WVliGyFwZv) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | 形态学预训练与零/少样本进化协同设计 |
| Dataset | Phototaxis task in varied terrains, Morphological Evolution Performance, Cross-Over Success (首次出现), Robustness to sensor/motor failure |

> [!tip] 效果简介
> - Phototaxis task in varied terrains 上，相对距离损失 (d1/d0) 为 ~0.3 (预训练收敛)，对比 初始基线 (未明确数字，但声称70%提升)，变化 -70% from baseline。
> - Morphological Evolution Performance 上，测试集适应度 (test loss) 为 零样本进化: 17分钟达到接近最优；少样本进化: 更高性能且维持多样性，对比 同时协同设计: 性能次佳且多样性崩溃，变化 零样本快速收敛，少样本性能与多样性俱佳。
> - Cross-Over Success (首次出现) 上，成功率 (offspring better than at least one parent) 为 77% in gen 1 of zero-shot evolution，对比 传统上认为交叉产生可行子代概率极低，变化 77%。

## 概要

机器人身体形态与控制器的协同设计是机器人学中的核心挑战。传统方法采用"同时协同设计"，即为每一代种群中的每个候选形态从头训练一个专用控制器。这种方案有两个致命瓶颈：**计算成本极高**，每次形态改变都需要重新进行强化学习训练，导致进化搜索空间无法有效扩展；更为严重的是，在多样性方面会遭遇**崩溃**——种群很快就收敛到单一高适应度设计，丢失了形态多样性，实质上退化为纯粹的形态优化而非协同设计。

本文的核心洞见是：**形态学预训练（Morphological Pretraining）使零样本进化成为可能，从而避免了重复的控制器训练**。具体而言，研究者在一个**可微分弹簧-质量模拟器**中，将通用控制器（一个简单的MLP）在超过**1000万个不同随机形态**上进行大规模预训练，控制器通过直接反向传播模拟器梯度来学习形态无关的传感器引导行为。在进化阶段，这个预训练的通用控制器被冻结（零样本进化），充当一种"通用适配器"，使得不同形态的快速评估成为可能。为了进一步防止多样性崩溃，提出**少样本进化**：每代重置预训练权重并进行少量微调后评估形态，从而在保持高性能的同时显著维持甚至增加种群多样性。

主要实验结果验证了该方案的有效性：预训练损失稳定收敛至约0.3（相对距离损失 $d_1/d_0$），相比基线提升70%（Fig. 6A）；零样本进化在100代内收敛至接近最优，整个过程仅需约**17分钟**（Fig. 6C）；少样本进化不仅取得了与零样本进化同等甚至更优的性能，更关键的是**维持并显著提高了种群形态多样性**（Fig. 6D），而传统的同时协同设计方法（Li et al., 2025）则遭受了明确的多样性崩溃（Fig. 6B）。此外，预训练控制器使得形态交叉操作在进化早期的成功率超过**77%**（Fig. 8），这一发现颠覆了以往认为交叉在形态进化中几乎不可行的传统认知。

本工作实质上是将协同设计问题从"同步搜索形态与控制器"重构为"预训练通用控制器 + 高效形态搜索"两阶段框架。利用可微分模拟提供的高质量梯度进行控制器预训练，再以该控制器为支点驱动形态进化，从而**打破控制器训练与形态进化之间的计算耦合瓶颈**，并显著缓解了协同设计中的多样性丧失问题。该方法全面在仿真中验证，尚未涉及向真实机器人（sim-to-real）的迁移，且目前仅针对单一趋光任务展示了效果。

机器人形态与控制（脑-身）协同设计的核心挑战在于：身体形态的每一个变化都要求控制器重新适应，而传统方法需要为**每一个候选形态从头训练专用控制器**。这种"设计-评估"循环将计算成本直接耦合到形态空间的规模上，使得大规模探索因为控制器训练瓶颈而变得极不经济。

### 计算瓶颈：从零开始的控制器训练

在同时协同设计（simultaneous co-design）范式中，控制器与形态一同进化：每一代种群中的每个新形态都需要从头学习行走或完成任务。该过程的两个致命缺陷已被实验证实：

- **收敛缓慢且依赖重复训练**：即使采用可微分模拟梯度，从头训练仍然需要为每个新形态重走完整的策略学习曲线。这限制了进化探索在合理计算预算内可探索的形态数量。
- **多样性崩溃**：当控制器与形态同时进化时，种群倾向于快速收敛到单一高适应度形态物种，丧失探索其他可能解的能力（详见 Fig. 6B）。形态多样性的丧失意味着协同设计退化为"找到一个好形态，然后反复优化它"，失去了探索多种构型的初衷。

### 形态无关控制的缺口

传统上，如果能够获得一个**不依赖于具体身体形态的通用控制器**，协同设计的瓶颈将被根本打破。然而，训练这样一个控制器面临以下困难：

1. **控制器架构的形态不变性要求**：网络必须仅依赖可在任意形态上可用的感觉-运动接口（如局部光传感器读数和中央模式生成器信号），而无法依赖身体本身的拓扑。
2. **大规模形态分布的覆盖**：真实有意义的通用控制需要在足够多样化的形态分布上训练，以覆盖进化可能探索的形态空间。这提出了远超单形态训练的优化挑战。
3. **梯度信号的质量**：不同形态产生的梯度可能在方向和量级上冲突，导致训练不稳定。

### 本文动机

本文的核心洞察是：**利用可微分物理模拟，通过梯度平均在超大规模形态分布上预训练通用控制器，可以使协同设计中的形态进化完全解耦于控制器的重新训练**。具体而言，本研究旨在回答以下问题：

- **可微分模拟能否支持千万级形态的通用控制器预训练？** 如果可行，该控制器应该能以零样本方式驱动全新形态完成任务（Fig. 6A 显示预训练收敛后性能提升约70%，置信度 0.95）。
- **解耦后的形态进化是否仍有效？** 若通用控制器可用，在冻结控制器的情况下纯进化形态能否快速收敛至高适应度？Fig. 6C 显示零样本进化在100代内收敛至接近最优，仅需17分钟（置信度 0.9）。
- **如何避免进化过程中的多样性崩溃？** 即便零样本进化可行，完全冻结控制器可能引导种群走向易于控制的简化形态。本文提出每代微调（few-shot evolution）策略，通过重置预训练权重并短时微调，维持形态多样性并同时提升性能（Fig. 6D，置信度 0.95）。

这一预训练-进化分离的范式将协同设计从"每代重训控制器"的计算困境中解放出来，使进化搜索在计算上可扩展到更大形态空间的同时，维持产生多样化和高性能设计的生物学启发目标。

## 核心方法与创新机理

传统机器人形态-控制的协同设计（Simultaneous Co-design from Scratch）需要为每个新的身体形态从头训练一个专用的RL控制器，计算成本高且难以扩展到大规模的形态探索空间。本文的核心贡献在于**形态学预训练（Morphological Pretraining）**，通过对上千万种不同形态的机器人进行大规模可微分模拟训练，得到一个**形态无关的通用控制器**。该控制器直接改变了协同设计的瓶颈——**控制器训练方式**从"为每个形态单独学习"转变为"预训练一个共享控制器"，从而将形态评估的计算开销从"重新训练"降至"直接推理"或"少量微调"。这一改变解锁了两种新型进化范式：**零样本进化（Zero-Shot Evolution）**和**少样本进化（Few-Shot Evolution）**，分别对应于进化过程中控制器更新的两个关键 changed slots（冻结 vs. 世代级微调），二者均完全避免了baseline中每个世代重新学习控制器的需求。

具体而言，本文的关键创新可分解为以下三个层面的 changed slots 及其效果：

**1. 控制器训练方式：从"为每个形态单独训练"到"预训练通用控制器"**

在baseline方法（Li et al., 2025）中，控制器是为每一个新生形态从头训练的；而在本文方法中，用一个简单的MLP将质量块的光传感器读数和CPG信号映射为弹簧的驱动信号，并通过可微分模拟直接反向传播梯度，在超过一千万种随机形态和多样地形/光源条件下进行端到端预训练。该预训练过程使通用控制器收敛到相对距离损失 $d_1/d_0 \approx 0.3$，相比初始基线有约70%的提升（Fig. 6A）。这一预训练控制器不仅为后续形态进化提供了强大的零样本控制基础，还使得**交叉操作**（crossover）变得高度可行——第一代零样本进化中，77%的交叉尝试产生的子代表现优于至少一个亲本（Fig. 8），而这在传统认知中几乎是不可能的，因为新的混合形态通常需要重新学习控制策略。

**2. 进化中控制器更新：从"每代重学"到"零样本推理与世代微调"**

协同设计的另一个核心 changed slot 是进化过程中控制器的更新方式。基线同时协同设计是在每一代中同时优化形态和控制器，导致种群在同一时间尺度内竞争控制能力和形态优势，最终陷入**多样性崩溃**——种群趋同于单一物种（Fig. 6B）。本文的**零样本进化**完全冻结预训练控制器，仅通过形态突变（每个体素以概率 $p = 1/N$ 翻转）和交叉来进化身体结构，从而可在仅17分钟内（100代）收敛至接近最优性能，且计算开销极小。然而，纯粹的零样本进化会导致种群向小尺寸、易控制的形态漂移（Fig. 9）。为解决此问题，提出的**少样本进化**在每个世代开始时将控制器权重重置回预训练状态，并进行60步微调（30步用于亲本，30步用于子代），然后再评估形态适应度。这种"重置+微调"的机制使得每代可以适应形态的剧烈变化，从而**有效维持甚至增加种群形态多样性**（平均成对汉明距离维持在约0.45），同时获得优于基线的高性能（Fig. 6D），打破了性能-多样性权衡。

**3. 梯度利用方式：从非可微强化学习到可微分模拟直接反向传播**

基线协同设计通常使用非可微分物理仿真，依赖强化学习估计梯度，而本文整体方法建立在**3D可微分弹簧-质量仿真**之上，直接通过可微分模拟的物理梯度进行端到端训练（Hooke's law $F = k (L - L_0)$ 控制弹簧力）。这一改变使得预训练可以在海量形态上高效完成，并且为少样本进化中的快速微调提供了精确的梯度信号，是上述两个 changed slots 能够发挥效用的底层技术支撑。实测中，该可微分控制器还能在传感器或马达部分失效时保持鲁棒性——在60-70%传感器失效或20-30%马达失效的情况下，仍能保持预训练性能（Fig. 14E）。

综上，核心创新并不在于引入新的神经网络架构或复杂的进化算法，而在于通过**形态学预训练**从根本上重构了协同设计的因果路径：用一个通用控制器替代了重复的控制器学习，进而通过零样本/少样本进化实现了快速、多样且高性能的形态探索。这一范式转换直接改变了三个关键设计槽（控制器训练方式、进化更新方式、梯度利用方式），并带来了可量化的突破：收敛速度提升数十倍、种群多样性得以维持、交叉操作首次在协同设计中高效可用，同时全过程可在单个GPU上完成。

![[assets/figures/papers/iclr26_0005_WVliGyFwZv_Accelerated_co-design_of_robots_through_morpholo/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed method. End-to-end differentiable policy training across tens of millions of morphologically distinct robots—morphological pretraining—produces a universal controller, which is kept frozen throughout zero-shot evolution and fine-tuned for each generation of few-shot evolution*

传统机器人形态‑控制协同设计需要为每一个候选身体形态**从头训练专用的控制器**，这导致计算成本高昂，且搜索过程难以在大规模形态空间中持续探索。本工作**以可微分模拟为瓶颈突破口**：通过在超过一千万个随机生成的形态上**预训练一个形态无关的通用控制器**，将"学习如何控制"与"寻找最优形态"解耦，从而使得形态进化可以依赖一个即插即用的控制策略，而不必每次重新训练。

整个框架围绕三个关键阶段展开，模块关系与数据流如下：

1. **基因型‑表现型映射（Genotype‑to‑Phenotype Mapping）**  
   将进化算法操作在的离散基因型（一个 $6\times6\times4$ 的二值体素网格）转化为具体的弹簧‑质量网络机器人。该映射输出的机器人身体被送入可微分物理模拟器。

2. **形态学预训练（Morphological Pretraining）**  
   在大量随机形态和多样化地形‑光源环境下，通过可微分弹簧‑质量模拟**端到端训练一个通用控制器**。控制器为一个简单的 MLP，输入为分布于各个质量点的光电传感器读数与中心模式发生器（CPG）信号，输出为弹簧的激活力信号 $F = k (L - L_0)$。训练目标是最小化相对距离损失 $d_1/d_0$（最终到光源距离与初始距离之比），损失梯度通过模拟过程直接反向传播，**无需强化学习的奖励估计**。预训练完成后，控制器收敛至约 0.3 的损失值，相较基线性能提升约 70%（Fig. 6A）。

3. **形态进化**  
   利用预训练控制器驱动形态搜索，分为两种变体：
   - **零样本进化（Zero‑Shot Evolution）**：完全冻结预训练控制器权重，仅对形态种群进行变异和交叉操作，并基于控制器在固定测试环境上的表现评估适应度。由于无需任何重新训练，进化可在 **100 代内（约 17 分钟）收敛到接近最优性能**，同时交叉操作在早期具有 >77% 的成功率（子代优于至少一个亲本）。
   - **少样本进化（Few‑Shot Evolution）**：每一代先将控制器权重重置回预训练状态，仅进行少量微调步（例如亲本 30 步、子代 30 步）后再评估形态。该设计**有效遏制了多样性崩溃**：相比零样本进化，少样本进化能够维持并显著增加种群形态多样性，同时获得更高或相当的适应度性能。

作为对比基线，**同时协同设计（Simultaneous Co‑Design）**从头同时进化形态与控制器，不进行预训练，结果观察到了严重的**多样性崩溃**——种群收敛为形态高度相似的少数设计，且性能低于少样本进化。

整体输入‑输出流可集中概括为：**随机采样的形态与环境** → 可微分模拟 + 反向传播损失梯度 → 通用控制器 → 进化算法以变异/交叉修改形态 → 通过冻结或微调控制器评估形态 → 输出高适应度且多样的机器人形态种群。该流水线使控制器训练与形态进化解耦，避免了传统方法中每代重新学习的瓶颈，并以极低的计算开销在单一 GPU 上完成了从零样本到少样本的大规模协同设计。

### 基因型到表现型映射 (Genotype-to-Phenotype Mapping)

机器人形态被编码为 $6 \times 6 \times 4$ (长×宽×高) 的二值体素网格基因型。每个体素的存在决定空间中对应位置是否放置质量点 (mass)。活跃体素之间通过弹簧 (spring) 连接，形成一个弹簧-质量网络 (mass-spring network) 作为表现型。弹簧赋予运动能力，质量点承载传感器功能（Section 2.1, Fig. 3）。

### 可微分弹簧-质量模拟 (Differentiable Mass-Spring Simulation)

仿真环境基于3D可微分物理引擎构建，核心力学由胡克定律驱动：

$$F = k (L - L_0)$$

其中 $k$ 为弹簧刚度系数，$L$ 为当前弹簧长度，$L_0$ 为调制后的静息长度（resting length）。控制器通过调节 $L_0$ 来驱动弹簧伸缩，从而实现机器人的运动。由于整个模拟过程可微分，梯度可直接通过仿真反向传播至控制器参数，无需依赖强化学习的随机梯度估计（Section 2.2）。

### 通用控制器架构与形态学预训练

通用控制器（universal controller）是一个简单的MLP，输入两个信号流：
- 每个质量点上的光传感器读数（photosensor readings）
- 中央模式生成器（Central Pattern Generator, CPG）信号

输出为每个弹簧的驱动信号（spring actuation），从而实现了形态无关的通用控制能力（Section 2.3）。

**形态学预训练 (Morphological Pretraining)** 在超过1000万个不同随机形态上训练该控制器，使用可微分模拟的梯度端到端优化。训练目标为相对距离损失（relative distance loss）：

$$\text{loss} = d_1 / d_0$$

其中 $d_0$ 为机器人初始位置到光源的距离，$d_1$ 为仿真结束时刻到光源的最终距离。该损失函数的优势在于消除了因初始位置远近不同而产生的性能评估偏差。预训练在1000万形态规模下收敛，损失稳定在约0.3，相比初始基线提升70%（Fig. 6A, Section 2.4）。

### 光强衰减模型

实验中实际采用的光强衰减为逆平方根模型：

$$I \propto d^{-1/2}$$

而非物理上正确的平方反比律 $d^{-2}$。论文指出这本质上是逆平方律的一个平滑重参数化（smooth reparameterization），可通过变换等效映射至物理模型（Section A.5）。

### 进化过程中的变异与选择

零样本进化（Zero-Shot Evolution）与少样本进化（Few-Shot Evolution）均采用基于遗传算法的变异和交叉操作。基因型中每个体素的变异概率为：

$$p = 1 / N$$

其中 $N = 6 \times 6 \times 4 = 144$ 为总体素数，使得每次变异期望翻转一个体素位（Section 2.5）。

两种进化策略的核心区别在于控制器更新方式：
- **零样本进化**：冻结预训练控制器，仅在进化过程中评估形态性能，快速筛选优良身体设计。
- **少样本进化**：每代将控制器权重重置为预训练值，进行60步微调（父代30步，子代30步）后评估，既维持高性能又防止种群多样性崩溃（Section 2.5-2.6）。

## 实验与关键发现

为系统验证形态学预训练对机器人协同设计的加速作用，我们比较了三种协同设计范式：**形态学预训练 + 零样本进化**（冻结控制器仅进化形态）、**形态学预训练 + 少样本进化**（每代微调控制器并重置）以及**同时协同设计**（无预训练，从头同时进化形态与控制器）。所有方法共享相同的可微分质量-弹簧仿真环境、趋光任务及 10 个固定测试地形（Fig. 3, 6），确保在计算投入可控的前提下公平对比。

![[assets/figures/papers/iclr26_0005_WVliGyFwZv_Accelerated_co-design_of_robots_through_morpholo/figures/011_Figure_6.jpg]]
*Figure 6: Performance and diversity. Morphological pretraining (A) converges with 70% improvement from baseline. The algorithm from Li et al. (2025), simultaneous co-design (from scratch without pretraining; B) achieves similar training loss; but, population diversity (mean pairwise Hamming distance on genotypes) collapses as evolution converges to a single species of similar designs which simplifies shared control. Zero-shot evolution (using the pretrained controller; C) rapidly improves test performance, but also suffers diversity collapse as evolution compiles slightly modified clones of the designs that are the most compatible with the pretrained model. Few-shot evolution (D) resets the pretraine...*

### 主结果：预训练收敛、进化加速与多样性保持

**大规模预训练使通用控制器收敛至高性能。**  
在超过 1000 万个不同的随机形态上预训练通用控制器，损失（相对距离损失 $d_1/d_0$）最终稳定在约 0.3（Fig. 6A），较初始基线提升约 70%。该收敛特性表明可微分仿真梯度能够整合来自多样化身体、地形和目标的信号，训练出形态无关的传感器‑驱动映射。

**零样本进化实现分钟级形态快速优化。**  
固定预训练控制器后，仅对 8192 个随机形态（预训练未见）进行遗传算法搜索（突变概率 $p=1/N$，$N$ 为体素数），种群在 100 代内即收敛至接近全局最优的性能（Fig. 6C），整个过程仅需约 17 分钟。这验证了形态学预训练赋予的零样本潜力：控制器无需重训即可评估海量形态，将进化瓶颈从"每形态训练专用控制器"转移至"快速前向评估"。

**少样本进化规避多样性崩溃，同时获得更优性能。**  
零样本进化虽然快速，却导致种群向小型设计收缩，多样性下降（Fig. 9, Fig. 6C）。对此，少样本进化在每代评估前对预训练权重进行 60 步微调（30 步用于父代，30 步用于子代），随后重置权重以免累积漂移。结果（Fig. 6D）显示，测试性能持续提升且种群平均两两汉明距离维持在约 0.45 的高水平，多样性不仅没有崩溃，反而在世代间显著增加并保持。这证实了每代微调这一因果机制：它允许控制器适应新形态的表达，同时保留通用基础，从而支持形态多样性涌现。

![[assets/figures/papers/iclr26_0005_WVliGyFwZv_Accelerated_co-design_of_robots_through_morpholo/figures/016_Figure_9.jpg]]
*Figure 9: Evolved populations. Population performance, phenotype footprint size, and body mass for the initial (randomly generated and evolved design populations. Whereas zero-shot evolution shifts the population toward smaller designs that are easier to control with the pretrained policy, few-shot evolution maintained a diverse population of overall larger designs with larger footprints which increase locomotion stability*

**同时协同设计陷入多样性崩溃且性能次优。**  
作为消融基线，直接去除预训练，让形态与控制器的进化从零开始（Li et al. 2025 范式改进版）。尽管训练损失与预训练方案相当（Fig. 6B），但种群多样性迅速下降，经过 180 代后几乎收敛为单一物种（Fig. 12B 和 ridgeline 图 Fig. 9 显示形态同质化）。这从反面揭示了形态学预训练的分工：它将"如何控制"与"长成什么样"解耦，使进化压力不至于过早消除形态差异，从而避免多样性崩溃。

### 关键机制的进一步消融

**交叉操作的有效性源于预训练控制器。**  
零样本进化初期（第 1 代），交叉产生的子代有 77% 至少优于一个父代（Fig. 8），远高于传统机器人进化中近乎随机组合失败的经验。高成功率表明，通用控制器赋予来自不同父代的模块化部件以一致的"语义控制"，使重组后的新形态能立即被有效驱动。这种早期交叉成功率是推动快速进化的关键引擎，但在同时协同设计中没有出现——因为每个身体都需要重新学习控制器，交叉几乎不会产生可行子代。

![[assets/figures/papers/iclr26_0005_WVliGyFwZv_Accelerated_co-design_of_robots_through_morpholo/figures/015_Figure_8.jpg]]
*Figure 8: Success of crossover vs. mutation. The evolutionary success of mutation and crossover is here defined by the fraction of mutation and crossover events from the previous generation that were absorbed into the current population. Early in evolution, the pretrained controller enables greater than 50% crossover success rate. In the first generation of zero-shot evolution, for instance, 77% of crossover attempts resulted in offspring that were better than at least one of their parents, and more than half of these offspring were better than both of their parents. After a few generations, mutations that finely tune good designs were less likely to be deleterious than exchanging large components betwee...*

**每代重置与微调对多样性维持不可替代。**  
少样本进化的关键设计不是连续微调，而是每代重置预训练参数后微调。这保证了每一代控制器都从相同的通用基础出发，防止因追踪种群特定分布而丧失普适性。若移除重置（即连续微调），则会导致与同时协同设计类似的多样性逐渐丧失。但对此形式消融实验暂未在论文中独立报告，需要手动验证。

### 泛化能力与鲁棒性

零样本进化得到的形态不仅在训练分布的地形和光源配置下表现优异，而且还展现出跨分布泛化能力：直接迁移至全新离散平台地形或修改感知模式（如磁力导航替代光源）后，性能显著高于预训练基线（Fig. 14A‑D）。更重要的是，这些进化形态对传感器和马达失效具有强鲁棒性：当超过一半的传感器或四分之一的马达被禁用时，仍能保留大部分功能（Fig. 14E），表明预训练控制器学会了利用身体冗余进行容错调度。

### 失败模式与局限性

1. **任务与形态单一**：当前框架仅验证在单个趋光任务上的效果，未扩展到多任务或多传感模态，限制了通用控制器的内涵证明。
2. **控制器架构简单**：通用控制器为不带形态条件化机制的 MLP，可能导致对复杂身体结构（如高离散形态）的控制精度不足，需要引入如部分注意力或 hypernetwork 等架构来提升形态调节能力。
3. **sim‑to‑real 鸿沟未跨越**：所有实验均在完全可微分模拟中进行，真实物理世界中的材料非弹性、阻尼和非平稳接触等未考虑，直接转移到物理机器人尚不可行。
4. **进化算法缺乏质量多样性显式引导**：当前仅使用基于性能的淘汰与交叉/突变，可能导致最终种群仍是单一适应度峰值的变体，而非探索不同的行为‑形态生态位，限制了开放型进化的潜力。
5. **计算扩展的瓶颈**：尽管展示了可仿真上百万弹簧的单一机器人（Fig. 13），但种群规模受限于单 GPU 内存，大规模微调与进化仍需权衡计算与种群大小。

这些弱点构成进一步研究的开放问题，也是将形态学预训练推向实际机器人设计与多任务协同的前置挑战。

![[assets/figures/papers/iclr26_0005_WVliGyFwZv_Accelerated_co-design_of_robots_through_morpholo/figures/019_Figure_12.jpg]]
*Figure 12: Morphological distinctiveness. Robot designs shown are sampled uniformly from each generation's test performance distribution and arranged (left to right, top to bottom) by morphological distinctiveness, defined as the mean pairwise Hamming distance to its peer designs. Performance scores appear below each design. The initial population (A) exhibits diverse morphologies with broad performance variation, serving as the starting point for all methods. After 180 generations, simultaneous co-design (B) yields high-performing but morphologically homogeneous designs. In contrast, both zero-shot evolution at generation 31 (C) and few-shot evolution at generation 6 (D) achieve equal or superior perfo...*

![[assets/figures/papers/iclr26_0005_WVliGyFwZv_Accelerated_co-design_of_robots_through_morpholo/figures/014_Figure_14.jpg]]

## 定位与知识库关联

传统机器人形态-控制协同设计（simultaneous co-design）需为每个候选形态从头训练专用控制器。这一过程使搜索成本随种群规模线性增长，且重训练引入的噪声易导致进化陷入 **多样性崩溃（diversity collapse）**——种群迅速收敛至单一形态，丧失探索广度（Fig. 6B）。本文的基线算法即采用此范式，在可微分弹簧-质量模拟中同时演化形态与控制器（Li et al., 2025），虽能获得尚可的训练损失，但种群遗传距离迅速归零，无法维持形态多样性。与此对照，本文的核心因果开关是将控制器学习从循环共进化中剥离，通过大规模可微分模拟 **预训练一个形态无关的通用控制器**，再以冻结或每代微调的方式驱动形态进化。这一范式转变在保持甚至超越基线性能的同时，将进化搜索的计算瓶颈从"每次评估重训RL策略"转变为"前向推理一次"，使零样本进化能够在约17分钟内收敛至近优（Fig. 6C），并将交叉重组成功率提升至77%（Fig. 8）。

### 与同时协同设计的关键差异

| 组件槽位 | 同时协同设计（基线） | 形态学预训练 + 零/少样本进化（本文） |
| :--- | :--- | :--- |
| 控制器训练方式 | 为每个形态单独训练RL控制器（bespoke） | 预训练一个形态无关的通用控制器（universal） |
| 进化中控制器更新 | 每代重新学习或继承从头训练 | 零样本：冻结权重；少样本：每代重置并微调60步 |
| 梯度来源 | 非可微分仿真，依赖强化学习估计梯度 | 可微分仿真直接反向传播模拟梯度 |

该设计逻辑根植于一个关键假设：**若一个控制器能同时控制千万种随机形态，则形态变异引入的扰动在控制器表示空间中应当是光滑的**，从而使突变与交叉后代仍大概率被有效驱动（Fig. 8 早期成功率）。证据表明，预训练损失收敛至约 $d_1/d_0 \approx 0.3$，相比初始性能提升约70%（Fig. 6A），且该通用控制器对未见过的新形态、新地形（离散平台、感知偏移）及新任务（趋磁性）均展现出分布外泛化能力（Fig. 14B–D）。

### 核心机制的归因分析

种群多样性维持是形态-控制协同设计的长期难题。同时协同设计因控制器重训练引入适应度评估噪声，微弱形态差异被淹没，导致选择压力过度集中。本文的零样本进化绕过了此问题，但自身会迅速偏向易于控制的"小尺寸"形态（Fig. 9 足迹和体重的分布左移），同样面临多样性损失风险。**少样本进化**介入后，每代对预训练控制器重置并微调，将微小的适应度差异转换成可继承的形态选择信号，从而同时提升性能并维持种群平均 pairwise Hamming 距离在 $\sim 0.45$（Fig. 6D）。这一消融对比（Fig. 6C vs 6D）以高置信度确立了"每代微调"是防止多样性崩溃的关键因果杠杆。

交叉重组在传统协同设计中几乎不可行，因为子代形态的剧变使标准控制器失效。预训练控制器将交叉事件的早期成功率推高至77%，且这一高成功率在种群多样性未显著下降的若干世代内持续（Fig. 8），为模块化、组合式进化提供了实验证据。然而，随着零样本进化自身多样性的衰减，交叉优势递减，再次印证进化动力与形态维持之间的耦合。

### 适用边界与已知局限

* **任务与感官模态单一**：全文仅验证趋光（phototaxis）任务，光强感知器为简单MLP输入。尚未证明在多任务、多模态传感器（如触觉、本体感觉组合）条件下通用控制器的扩展性。  
* **控制器架构朴素**：通用控制器为全连接MLP，缺乏显式形态条件机制。论文自述指出，对更复杂行为可能需要带注意机制或超网络的架构以更好地进行形态条件控制。  
* **进化算法简约**：当前使用带突变（单点翻转概率 $p=1/N$）与交叉的基本遗传算法，未引入显式质量多样性（quality diversity）算法。种群规模和世代数受限于单GPU内存，无法进行更大规模的开放式进化。  
* **仿真至真实的鸿沟**：所有验证均在可微分弹簧-质量模拟中完成，未经历 sim-to-real 转移。传感器衰减模型（$d^{-1/2}$ 而不是物理学正确的 $d^{-2}$）虽可通过重参数化等价解决，但仍是模拟偏离真实的例证。  
* **形态表示规模有限**：体素网格为 $6\times6\times4$，对应数百个质量和弹簧。尽管附录展示了可扩展至百万弹簧的解剖复杂性（Fig. 13），但形态生成空间仍由该固定分辨率网格限定。

### 开放问题与后续工作方向

基于当前框架，以下几个延伸方向值得探索：

1. **多任务、多材料与多模态泛化**：如何训练能够跨任务（趋光、避障、搬运）和多材料属性（刚度、阻尼、质量分布）的通用控制器？感知模态如何融合以应对更丰富的环境？
2. **形态条件的复杂化**：采用 masked attention、hypernetwork 或上下文调制等方式实现更丰富的形态-控制器交互，使得每个质点的行为可能依据其在整体形态中的位置动态调整。
3. **质量多样性驱动的进化**：以显式的质量多样性算法（如 MAP-Elites）取代当前简单遗传算法，以促进形态与行为的持续创新，逼近开放式进化（open-ended evolution）。
4. **闭环 sim-to-real 转移**：通过高精度模拟、域随机化或残差物理学习将预训练-进化管线迁移至真实机器人，并测试形态多样性的物理可制造性。
5. **跨域形态探索**：将该框架迁移至水下游泳、空中飞行、树上攀爬等不同运动模式中，检验形态无关控制的普适性并探索多栖形态。

本工作在机器人协同设计文献谱系中提供了一个明确的范式迁移：将"高成本控制训练"与"低成本形态评估"解耦，通过形态预训练使零样本和少样本进化成为计算上可行且能维持多样性的设计路径。它为后续引入更丰富的行为表征、更大规模探索以及向物理世界延伸提供了可复现的基线。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Accelerated_co_design_of_robots_through_morphological_pretraining.pdf

![[paperPDFs/ICLR_2026/Accelerated_co_design_of_robots_through_morphological_pretraining.pdf]]
