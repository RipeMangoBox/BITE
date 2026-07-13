---
title: "A Single Architecture for Representing Invariance Under Any Space Group"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Single_Architecture_for_Representing_Invariance_Under_Any_Space_Group.pdf
project_link: null
code_link: null
aliases:
- CFTC
- SARIUASG
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将群约束编码为傅里叶系数之间的线性关系，并通过预计算的路由矩阵 M_G 一次性施加所有对称性，使Transformer主体参数可在所有群间共享。"
primary_logic: "晶格对称性对傅里叶系数的约束可表示为倒易格点上的有向图，其连通分量对应一组完备的G-不变基函数；该基函数可通过一次矩阵-向量乘法从标准傅里叶模式中计算得到。"
claims:
- "CFT在总能量和剪切模量预测上优于所有基线方法"
- "CFT在零样本场景下对含反演对称性的群泛化能力显著优于ALIGNN和Matformer"
- "CFT训练和推理速度比ALIGNN和Matformer快数倍"
- "预训练位置编码显著提升下游预测性能"
---

# A Single Architecture for Representing Invariance Under Any Space Group

> [!tip] 核心洞察
> 晶格对称性对傅里叶系数的约束可表示为倒易格点上的有向图，其连通分量对应一组完备的G-不变基函数；该基函数可通过一次矩阵-向量乘法从标准傅里叶模式中计算得到。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 单一架构：表示任意空间群下的不变性 |
| 英文题名 | A Single Architecture for Representing Invariance Under Any Space Group |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8LZrXh9hhL) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Crystal Fourier Transformer (CFT) |
| Dataset | Materials Project |

> [!tip] 效果简介
> - Materials Project 上，Total Energy MAE (eV/atom) 为 0.197 ± 0.009，对比 Matformer: 0.199 ± 0.005; ALIGNN: 0.202 ± 0.003; Transformer: 0.220 ± 0.005，变化 最佳（优于所有基线）。
> - Materials Project 上，Band Gap MAE (eV) 为 0.306 ± 0.006，对比 Matformer: 0.296 ± 0.005; ALIGNN: 0.302 ± 0.004; Transformer: 0.340 ± 0.008，变化 略逊于Matformer，优于ALIGNN和Transformer。
> - Materials Project 上，Bulk Moduli MAE (log GPa) 为 0.082 ± 0.008，对比 Matformer: 0.076 ± 0.003; ALIGNN: 0.080 ± 0.005; Transformer: 0.095 ± 0.006，变化 略逊于Matformer和ALIGNN，优于Transformer。

## 概要

材料科学中预测晶体性质的核心瓶颈在于：230种空间群各有不同的对称性，现有方法（Matformer、ALIGNN）为每个群设计专用架构，导致参数无法跨群共享。当某个空间群数据稀疏时，模型性能急剧下降。

本文提出 Crystal Fourier Transformer (CFT)，其核心因果机制是将群约束编码为傅里叶系数之间的线性关系，通过预计算的路由矩阵 **M_G** 一次性施加所有对称性。具体而言，晶格对称性对傅里叶系数的约束可表示为倒易格点上的有向图（Figure 1），其连通分量对应一组完备的G-不变基函数（Equation 4）；该基函数通过一次矩阵-向量乘法 **e_G(x) = M_G v(x)**（Equation 7）从标准傅里叶模式中计算得到。这使得Transformer主体参数可在所有230个空间群间共享，从根本上解决了数据稀疏时的泛化问题。

方法定位为：将对称自适应傅里叶基构造模块与标准编码器Transformer结合，输入为原子嵌入与G-不变位置编码之和，输出经池化后由MLP预测材料属性（Figure 2）。位置编码还通过双分支网络（对称自适应位置分支 + 晶格几何分支）以轨道距离为监督信号进行预训练，进一步提升性能（Table 3）。

主要实验结果：在Materials Project数据集上，CFT在总能量（MAE 0.197±0.009 eV/atom）和剪切模量（MAE 0.158±0.011 log GPa）预测上优于所有基线（Matformer、ALIGNN、标准Transformer），见Table 1。在零样本泛化实验中（Figure 3），CFT对含反演对称性的未见群的泛化损失（GB-Gap）远小于基线：剪切模量GB-Gap为0.042 log GPa，而ALIGNN为0.120、Matformer为0.080。此外，CFT的训练速度（91秒/epoch）和推理速度（60秒/10k样本）比ALIGNN和Matformer快数倍（Table 2）。值得注意的是，CFT在带隙和体模量预测上略逊于Matformer，表明在某些属性上基于图的方法可能仍具优势。



晶体材料的物理性质由其原子排列的对称性——即空间群——所决定。然而，在机器学习模型中编码这种对称性一直是核心挑战。现有的方法（如ALIGNN和Matformer）为每个对称群设计专用架构，这导致了一个根本性的瓶颈：**模型参数无法在230个空间群之间共享**。当某个空间群的训练样本稀疏时，专用架构的性能会严重下降，因为模型无法从其他群的数据中迁移学习。

这一缺口的根源在于，传统方法将对称性硬编码到网络结构中（例如，在图神经网络中通过边构建来近似对称性），使得模型主体与特定群绑定。作者识别出这一因果机制：**对称性对函数施加的约束，本质上是傅里叶系数之间的线性关系**。因此，与其为每个群设计不同的网络，不如将这种约束编码为可计算的线性变换，从而让同一组Transformer参数在所有群间共享。

本文的动机正是基于这一洞察：通过显式表征群操作对傅里叶系数施加的约束（Equation 3: $F(\omega) = e^{i 2\pi \omega^{\top} \mathbf{A}^{\top} t} F(\mathbf{A} \omega)$），可以构造一组完备的G-不变基函数（Equation 4）。这些基函数通过一个预计算的路由矩阵 $\mathbf{M}_G$ 从标准傅里叶模式中线性变换得到（Equation 7: $\mathbf{e}_G(\pmb{x}) = \mathbf{M}_G \mathbf{v}(\pmb{x})$）。由此，作者提出了**Crystal Fourier Transformer (CFT)**：一种单一架构，其Transformer主体参数在所有230个空间群间共享，仅通过输入端的 $\mathbf{M}_G$ 来适应不同的对称群。这种设计使得模型在数据稀疏的群上也能利用从其他群学到的通用表示，从而在零样本泛化场景中展现出显著优势（Figure 3: CFT的剪切模量GB-Gap为0.042，而ALIGNN为0.120，Matformer为0.080）。



## 核心方法与创新机理

Crystal Fourier Transformer (CFT) 的核心创新在于用一个**单一、参数共享的Transformer架构**统一处理全部230个空间群，彻底改变了此前为每个对称群设计专用模型或依赖数据增强的范式。其关键因果机制是将群对称性对傅里叶系数的约束编码为**预计算的路由矩阵**，从而将位置编码从标准傅里叶模式线性变换为G-不变基函数，使Transformer主体参数在所有群间共享。

**核心瓶颈与因果旋钮：**

*   **瓶颈：** 现有方法（如ALIGNN、Matformer）为每个对称群设计专用架构或在图结构中隐式学习对称性，无法在230个空间群之间共享参数。这导致数据稀疏的群（如仅有几个样本）性能严重下降，且模型无法泛化到未见群。
*   **因果旋钮：** CFT将群约束编码为**傅里叶系数之间的线性关系**。通过Algorithm 1构造约束图并计算路由矩阵 $\mathbf{M}_G$，将标准傅里叶模式向量 $\mathbf{v}(\pmb{x})$ 一次性线性变换为G-不变位置编码 $\mathbf{e}_G(\pmb{x}) = \mathbf{M}_G \mathbf{v}(\pmb{x})$（Equation 7）。Transformer主体参数因此可在所有群间共享，仅在推理时根据输入群G更换路由矩阵。

**核心洞察：**

晶格对称性对傅里叶系数的约束可表示为倒易格点上的有向图，其连通分量对应一组完备的G-不变基函数。该基函数可通过一次矩阵-向量乘法从标准傅里叶模式中计算得到，避免了为每个群设计独立特征提取器。

**与基线的关键差异（Changed Slots）：**

| 槽位 | 基线方法 | CFT方法 | 证据锚点 |
|------|----------|---------|----------|
| **位置编码方式** | 标准傅里叶位置编码或图结构特征 | 通过群依赖路由矩阵 $\mathbf{M}_G$ 将标准傅里叶模式线性变换为G-不变基函数 | Equation 7 |
| **对称性处理方式** | 为每个群设计专用架构或通过数据增强隐式学习 | 单一架构，通过预计算的路由矩阵显式编码任意空间群的约束，Transformer主体参数跨群共享 | Section 3.3 |
| **晶体表示方式** | 图结构（节点为原子，边为键或近邻关系） | 原子位置的标准傅里叶模式 + 群约束线性变换，直接作为Transformer的输入token | Figure 2 |

**决定性证据（强度与可靠性）：**

1.  **主任务性能（证据强度：高）：** 在Materials Project数据集上，CFT在总能量（MAE 0.197±0.009 eV/atom）和剪切模量（MAE 0.158±0.011 log GPa）预测上优于所有基线（Table 1）。在带隙和体模量上略逊于Matformer，但优于ALIGNN和标准Transformer。这表明CFT的对称性编码在整体上不损害预测精度，甚至对某些属性有提升。

2.  **零样本泛化（证据强度：高）：** 在含反演对称性的未见群上，CFT的泛化能力显著优于ALIGNN和Matformer。对于剪切模量，CFT的群平衡绝对性能差距（GB-Gap）仅为0.042 log GPa，而ALIGNN为0.120，Matformer为0.080（Figure 3）。对于群113、162、200、216，ALIGNN和Matformer的零样本MAE超过全数据MAE五倍以上，而CFT的退化幅度小得多。这直接验证了核心假设——显式参数化群约束可实现泛化。

3.  **效率优势（证据强度：高）：** CFT的训练速度（91秒/epoch）比ALIGNN（592秒）快6.5倍，比Matformer（266秒）快2.9倍；推理速度（60秒）比ALIGNN（451秒）快7.5倍，比Matformer（222秒）快3.7倍（Table 2）。效率优势源于其核心对称性操作仅为一次矩阵-向量乘法，无需构造和维护复杂的图结构。

4.  **预训练有效性（证据强度：高）：** 预训练位置编码模块（以轨道距离为监督信号）显著提升所有四个属性的预测性能（Table 3）。例如，总能量MAE从0.207降至0.197，剪切模量MAE从0.215降至0.158。这表明预训练有助于学习更具物理意义的对称性感知嵌入。

**证据的局限性与需手动验证的点：**

*   **零样本实验范围：** 零样本实验仅针对含反演对称性的群（约49%数据），对其他类型未见群的泛化能力尚未验证。这是论文明确承认的局限性。
*   **性能权衡：** CFT在带隙和体模量预测上未超越Matformer，表明在某些属性上基于图的方法可能仍具优势。这一现象的原因需要手动验证——是Matformer的图结构更适合捕捉电子结构信息，还是CFT的傅里叶表示在某些属性上存在信息损失？
*   **预训练成本：** 预训练位置编码模块需要额外的200 epoch训练，其成本未计入Table 2的训练时间比较中。虽然论文说明这是摊销成本，但整体流程复杂度增加。
*   **截断近似：** 实际构造中需对倒易格点进行有限半径截断（R=5，约514个模式），可能在高精度需求下引入近似误差。论文通过Figure 7展示了模式数量与性能的权衡，但未讨论截断对特定属性的影响。



![[assets/figures/papers/iclr26_0004_8LZrXh9hhL_A_Single_Architecture_for_Representing_Invarianc/figures/002_Figure_2.jpg]]
*Figure 2: Diagram of the Crystal Fourier Transformer architecture. Atom positions are first encoded into standard Fourier modes. A group-conditional routing matrix, $\mathbf { M } _ { G }$ transforms these modes into a provably invariant basis. These adaptive positional encodings, combined with other invariant features, are then processed by a Transformer whose weights are shared across all space groups to predict material properties*

Crystal Fourier Transformer (CFT) 的整体 pipeline 围绕一个核心设计展开：**将任意空间群的对称性约束预编码为线性变换，使得标准 Transformer 主体在所有 230 个空间群之间共享参数**。这一设计直接回应了现有方法（如 Matformer、ALIGNN）为每个对称群设计专用架构、无法跨群共享参数导致数据稀疏时性能严重下降的根本瓶颈。

**Pipeline 流程如下：**

1. **对称自适应傅里叶基构造模块**：对于输入晶体及其所属空间群 G，Algorithm 1 首先在倒易格点上构造约束图——群操作对傅里叶系数的约束被编码为加权边（如墙纸群 pg 中，边权为 +1 或 -1）。该图的连通分量对应一组完备的 G-不变基函数。通过求解相位一致性条件，预计算得到路由矩阵 M_G。该矩阵将标准傅里叶模式向量 v(x) 线性变换为 G-不变位置编码 e_G(x) = M_G v(x)（Equation 7）。这一模块是 CFT 区别于所有基线方法的关键：它将群约束从架构设计层面剥离，转化为一次矩阵-向量乘法。

2. **位置编码预训练模块**：该模块由双分支网络组成——对称自适应位置分支（处理经过 M_G 变换的傅里叶特征）和晶格几何分支（将 3×3 晶格向量展平为 9 维向量，经 3 个残差块处理）。预训练以轨道距离 d_G(x₁, x₂)（Equation 22）为监督信号，最小化嵌入空间 L2 距离与轨道距离之间的均方误差（Equation 23）。预训练使位置编码自动学会将原子位置映射到基本区域（fundamental region），如图 8 所示墙纸群 p6m 中，学习到的编码发现了到基本区域的等距映射。

3. **Crystal Fourier Transformer**：这是一个标准编码器 Transformer。每个原子的输入 token 由化学元素嵌入与经过预训练的 G-不变位置编码直接相加构成。由于输入特征本身已是 G-不变的，后续的自注意力机制和 MLP 输出自然保持 G-不变性。Transformer 主体参数在所有 230 个空间群之间共享。输出经池化后由 MLP 预测材料属性（总能量、带隙、体模量、剪切模量）。

**模块关系与输入输出流：** 输入为晶体的原子坐标（分数坐标）和空间群标签 G。坐标首先经标准傅里叶编码为 v(x)，然后与预计算的路由矩阵 M_G 相乘得到 G-不变位置编码 e_G(x)。该编码与原子类型嵌入相加后送入 Transformer。Transformer 输出经平均池化和 MLP 得到标量属性预测。M_G 仅依赖空间群 G 和截断半径 R（实验中 R=5，约 514 个模式），与具体晶体结构无关，因此可预计算并缓存。

**关键设计因果链条：** 将群约束编码为傅里叶系数之间的线性关系（Equation 3）→ 构造约束图 → 连通分量对应 G-不变基函数 → 预计算路由矩阵 M_G → 一次矩阵-向量乘法施加所有对称性 → Transformer 主体参数跨群共享。这一链条使得 CFT 在零样本场景下（对未见空间群直接使用对应的 M_G，不更新参数）展现出显著优于 ALIGNN 和 Matformer 的泛化能力：剪切模量的 GB-Gap 仅为 0.042 log GPa，而 ALIGNN 和 Matformer 分别为 0.120 和 0.080（Figure 3）。



### 问题形式化与G-不变性条件

Crystal Fourier Transformer (CFT) 的核心目标是在单一架构中处理任意空间群 $G$ 下的不变性。问题首先被形式化为：寻找定义在 $\mathbb{R}^n$ 上的函数 $f$，使其在所有群操作 $\phi \in G$ 下保持不变。该G-不变性条件由公式 (1) 给出：

$$f(\phi(\pmb{x})) = f(\pmb{x}) \qquad \mathrm{for~all}~\phi \in G \mathrm{~and~} \pmb{x} \in \mathbb{R}^n.$$

### G-不变傅里叶基的构造

CFT 通过显式构造G-不变傅里叶基来处理对称性约束。该基函数被定义为负拉普拉斯算子在G-不变约束下的特征函数，即公式 (2)：

$$-\Delta e = \lambda e \qquad \mathrm{subject~to~} e = e \circ \phi \mathrm{~for~all~} \phi \in G.$$

在傅里叶域中，G-不变性条件转化为对傅里叶系数的线性约束。对于任意等距变换 $\phi(\pmb{x}) = \mathbf{A}\pmb{x} + \mathbf{t}$，傅里叶系数必须满足公式 (3)：

$$F(\omega) = e^{i 2\pi \omega^{\top} \mathbf{A}^{\top} t} F(\mathbf{A} \omega).$$

这一约束将倒易格点上的傅里叶模式通过相位因子耦合起来。基于此，G-不变基函数被构造为同一轨道 $\mathcal{O}$ 内所有傅里叶模式的加权和，如公式 (4) 所示：

$$e_{\mathcal{O}}(\pmb{x}) = \sum_{\omega \in \mathcal{O}} w_{\pmb{\xi} \to \omega} \cdot e^{i 2\pi \omega^{\top} \pmb{x}}.$$

其中权重 $w_{\pmb{\xi} \to \omega}$ 由相位约束唯一确定。论文的Theorem 3.2保证了任意连续G-不变函数都可以一致收敛地展开为这种基函数的线性组合。

### 核心编码层：路由矩阵

CFT 的关键创新在于将上述基函数构造过程编码为一个可计算的线性变换。对于给定的空间群 $G$，首先通过Algorithm 1构造约束图并计算连通分量，然后预计算一个路由矩阵 $\mathbf{M}_G$。该矩阵将标准傅里叶模式向量 $\mathbf{v}(\pmb{x})$ 线性变换为G-不变位置编码，如公式 (7) 所示：

$$\mathbf{e}_G(\pmb{x}) = \mathbf{M}_G \mathbf{v}(\pmb{x}).$$

这一设计的核心优势在于：**Transformer主体参数可在所有230个空间群间共享**，因为群依赖的对称性约束被完全封装在预计算的路由矩阵 $\mathbf{M}_G$ 中。CFT的核心对称性操作简化为一次矩阵-向量乘法。

### 预训练模块与轨道距离

为提升位置编码的物理意义，CFT引入了一个预训练模块。该模块使用**轨道距离**作为监督信号，定义如下（公式 22）：

$$d_G(\pmb{x}_1, \pmb{x}_2) := \min_{\phi_1, \phi_2 \in G} ||\phi_1(\pmb{x}_1) - \phi_2(\pmb{x}_2)||_2.$$

该距离度量了两个原子轨道之间的最小欧氏距离，是G-不变的。预训练损失函数（公式 23）为轨道距离与嵌入空间L2距离之间的均方误差：

$$\mathcal{L}_{\mathrm{pretrain}} = \left( d_G(\mathbf{p}_1, \mathbf{p}_2) - \|\mathbf{e}_1 - \mathbf{e}_2\|_2 \right)^2.$$

预训练位置编码模块由两个分支组成：对称自适应位置分支（将分数坐标通过 $\exp(i \cdot 2\pi \cdot \mathbf{p} \cdot \mathbf{k})$ 编码为傅里叶特征）和晶格几何分支（将 $3\times3$ 晶格向量展平为9维向量并经3个残差块处理）。消融实验（Table 3）证实，预训练显著提升了所有四个材料属性的预测性能（如总能量MAE从0.207降至0.197）。

### 零样本泛化度量

为量化CFT对未见空间群的泛化能力，论文定义了**性能差距**（公式 9）：

$$\Delta \mathrm{MAE}_G = \mathrm{MAE}_G^{\mathrm{zero-shot}} - \mathrm{MAE}_G^{\mathrm{all-data}}.$$

并进一步定义了**群平衡绝对性能差距**（GB-Gap，公式 10），对所有含反演对称性的未见群等权平均：

$$\mathrm{GB-Gap} = \frac{1}{|\mathcal{G}_{\mathrm{inv}}|} \sum_{G \in \mathcal{G}_{\mathrm{inv}}} |\Delta \mathrm{MAE}_G|.$$

在零样本实验中，CFT在推理时直接使用未见群 $G$ 的预计算路由矩阵 $\mathbf{M}_G$，无需任何参数更新或微调。实验结果显示，CFT的剪切模量GB-Gap仅为0.042 log GPa，远优于ALIGNN的0.120和Matformer的0.080（Figure 3），证实了显式参数化群约束的有效性。

### 架构流水线总结

CFT的完整流水线包含三个核心模块：
1. **对称自适应傅里叶基构造模块**：根据输入空间群 $G$，通过Algorithm 1构造约束图并计算路由矩阵 $\mathbf{M}_G$。
2. **位置编码预训练模块**：双分支网络（对称自适应位置分支 + 晶格几何分支），以轨道距离为监督信号预训练位置编码。
3. **Crystal Fourier Transformer**：标准编码器Transformer，输入为原子嵌入与G-不变位置编码之和，输出经池化后由MLP预测材料属性。



## 实验与关键发现

### 主实验结果

CFT在Materials Project数据集上的四个材料属性预测中展现了有竞争力的性能。**在总能量和剪切模量预测上，CFT超越了所有基线方法**：总能量MAE为0.197±0.009 eV/atom（Matformer: 0.199, ALIGNN: 0.202），剪切模量MAE为0.158±0.011 log GPa（Matformer: 0.161, ALIGNN: 0.163）（Table 1）。这一优势来自CFT的核心机制：通过预计算的路由矩阵M_G将对称性约束直接编码为G-不变位置编码，使得Transformer主体参数可在所有230个空间群间共享，从而在数据稀疏时仍能有效学习。

![[assets/figures/papers/iclr26_0004_8LZrXh9hhL_A_Single_Architecture_for_Representing_Invarianc/figures/003_Table_1.jpg]]
*Table 1: Test Mean Absolute Error (MAE) comparisons on the Materials Project dataset. Lower values indicate better performance. Results are reported as mean ± one standard deviation over 4 runs. Bold indicates the best performance for each property*

在带隙预测上，CFT（0.306±0.006 eV）略逊于Matformer（0.296），但优于ALIGNN（0.302）和标准Transformer（0.340）。体模量预测中，CFT（0.082±0.008 log GPa）同样略低于Matformer（0.076）和ALIGNN（0.080）。这表明在某些属性上，基于图的邻域聚合方法可能仍具优势，因为带隙和体模量对局部化学环境更敏感，而CFT的全局傅里叶表示可能稀释了这种局部信息。

### 零样本泛化能力

零样本实验是检验CFT核心假设的关键——即显式参数化群约束能否使模型泛化到未见空间群。实验设计为：在去除所有含反演对称性群（约49%数据）的训练集上训练模型，然后在这些未见群上测试。**CFT在所有含反演对称性的未见群上展现出显著优于ALIGNN和Matformer的零样本泛化能力**（Figure 3）。

![[assets/figures/papers/iclr26_0004_8LZrXh9hhL_A_Single_Architecture_for_Representing_Invarianc/figures/005_Figure_3.jpg]]
*Figure 3: Total Energy Performance Gap (Zero-shot MAE - All data MAE)*

![[assets/figures/papers/iclr26_0004_8LZrXh9hhL_A_Single_Architecture_for_Representing_Invarianc/figures/006_Figure_3.jpg]]
*Figure 3: We evaluate the zero-shot generalization capability of CFT in predicting the shear modulus and total energy of materials from groups containing inversion symmetry. For each held-out group, we plot the performance gap ∆MAE (Eq. 9), the difference between the zero-shot MAE (trained without any data from inversion groups) and the all-data MAE (trained on all 230 space groups). Smaller values are better; ∆MAE = 0 corresponds to perfect zero-shot generalization to that group*

对于剪切模量预测，CFT的群平衡绝对性能差距（GB-Gap）仅为0.042 log GPa，而ALIGNN为0.120，Matformer为0.080。这意味着CFT的零样本性能退化幅度仅为基线的1/3到1/2。对于总能量预测，CFT的GB-Gap为0.141 eV/atom，同样远低于ALIGNN（0.309）和Matformer（0.197）。

**特别值得关注的是，对于群113、162、200、216，ALIGNN和Matformer的零样本MAE超过全数据MAE五倍以上**，而CFT的退化幅度小得多。这一差异的因果机制在于：CFT在推理时直接使用未见群的路由矩阵M_G，无需任何参数更新或微调；而基线模型只能依赖从其他群学到的隐式模式，当未见群的对称性与训练群差异较大时，其图结构或位置编码无法适应新的约束关系。

### 效率分析

CFT在训练和推理速度上具有显著优势（Table 2）。训练速度：CFT每epoch仅需91秒，而ALIGNN需要592秒（6.5倍），Matformer需要266秒（2.9倍）。推理速度：CFT对10k晶体仅需60秒，而ALIGNN需要451秒（7.5倍），Matformer需要222秒（3.7倍）。

![[assets/figures/papers/iclr26_0004_8LZrXh9hhL_A_Single_Architecture_for_Representing_Invarianc/figures/004_Table_2.jpg]]

效率优势的根源在于CFT的对称性操作仅需一次矩阵-向量乘法（与预计算的路由矩阵M_G相乘），而ALIGNN需要构建复杂的图结构并执行消息传递，Matformer需要计算注意力权重。这一设计使得CFT特别适合大规模材料筛选场景。

### 消融实验

**预训练位置编码模块是CFT性能的关键组件**（Table 3）。去除预训练后，所有四个属性的MAE均显著上升：总能量从0.197升至0.207（+5.1%），带隙从0.306升至0.338（+10.5%），体模量从0.082升至0.134（+63.4%），剪切模量从0.158升至0.215（+36.1%）。体模量和剪切模量的退化尤为严重，说明力学属性对位置编码的精度高度敏感。

![[assets/figures/papers/iclr26_0004_8LZrXh9hhL_A_Single_Architecture_for_Representing_Invarianc/figures/010_Table_3.jpg]]
*Table 3: Test Mean Absolute Error (MAE) comparisons on the Materials Project dataset. Lower values indicate better performance. Results are reported as mean ± one standard deviation over 4 runs*

预训练模块通过双分支网络（对称自适应位置分支 + 晶格几何分支）以轨道距离为监督信号学习位置编码。**轨道距离**定义为两个原子轨道之间的最小欧氏距离，其监督信号迫使模型学习到G-不变嵌入空间中的等距映射。Figure 8的可视化结果验证了这一学习效果：对于墙纸群p6m，模型自动发现了到基本区域的等距映射，与理论最优解一致。

### 设计选择分析

**傅里叶模式数量的选择**在精度与效率之间存在权衡（Figure 7）。使用R=5（约514个模式）在轨道距离回归任务上达到最佳性能-效率平衡。更少的模式（R=3，约90个模式）导致表示能力不足，更多模式（R=7，约2000个模式）则带来计算开销的快速增加而精度提升有限。

### 失败模式与局限性

1. **带隙和体模量预测未达最优**：CFT在这两个属性上略逊于Matformer，表明基于图的局部特征表示在某些任务中仍有优势。可能的因果机制是带隙对原子间的局部成键环境高度敏感，而CFT的全局傅里叶基可能稀释了这种局部信息。

2. **有限截断引入近似误差**：实际构造中需对倒易格点进行有限半径截断（R=5），这在高精度需求下可能引入近似误差。对于超大晶胞或需要高分辨率的情况，截断半径的选择需要重新评估。

3. **零样本验证范围有限**：零样本实验仅针对含反演对称性的群（约49%数据），对其他类型未见群（如纯旋转群、螺旋轴群）的泛化能力尚未验证。这些群可能具有更复杂的约束图结构，CFT的泛化能力需要进一步验证。

4. **预训练模块增加流程复杂度**：预训练位置编码需要额外的训练阶段和轨道距离监督信号，增加了整体流程的复杂度。虽然预训练成本是摊销的（200 epoch），但这一设计可能限制了方法的即插即用性。

5. **计算瓶颈风险**：对于极高分辨率或超大晶胞，路由矩阵M_G的规模可能成为计算瓶颈。虽然当前设置下（约514个模式）效率优势明显，但扩展到更高分辨率时需要关注矩阵规模的增长。



## 定位与知识库关联

Crystal Fourier Transformer (CFT) 在方法谱系中占据一个独特的位置：它不依赖于为每个空间群设计专用架构（如基于图的 ALIGNN 和 Matformer），而是通过将对称性约束编码为傅里叶系数之间的线性关系，实现了单一 Transformer 架构在全部 230 个空间群之间的参数共享。这一设计的核心瓶颈在于，现有方法在数据稀疏时性能严重下降——每个群都需要独立学习其对称性，无法利用跨群的结构共性。CFT 的因果旋钮是预计算的路由矩阵 **M_G**（Equation 7: `e_G(x) = M_G v(x)`），它将标准傅里叶模式向量 `v(x)` 线性变换为 G-不变基函数，从而使 Transformer 主体参数对所有群共享。这一操作的底层洞察在于：晶格对称性对傅里叶系数的约束可以表示为倒易格点上的有向图，其连通分量恰好对应一组完备的 G-不变基函数（Theorem 3.2）。

**与基线的关系。** 在 Materials Project 数据集上的主实验结果（Table 1）显示，CFT 在总能量（MAE 0.197 ± 0.009）和剪切模量（0.158 ± 0.011）上优于所有基线方法，包括 Matformer（0.199 ± 0.005 和 0.161 ± 0.005）和 ALIGNN（0.202 ± 0.003 和 0.163 ± 0.006）。然而，在带隙（0.306 ± 0.006 vs. Matformer 0.296 ± 0.005）和体模量（0.082 ± 0.008 vs. Matformer 0.076 ± 0.003）上，CFT 略逊于 Matformer，表明基于图的方法在某些属性上仍具优势。这一模式暗示：CFT 的傅里叶基表示可能对与原子间键合细节高度相关的属性（如带隙）不如图结构敏感，但对整体能量和弹性响应这类全局性质更有效。

**零样本泛化的决定性证据。** 零样本实验（Figure 3）提供了 CFT 方法优势的最强证据。当模型训练时不包含任何含反演对称性的群的数据，然后在推理时直接使用未见群的路由矩阵 **M_G**（无需微调），CFT 的群平衡绝对性能差距（GB-Gap）在剪切模量上仅为 0.042 log GPa，远低于 ALIGNN 的 0.120 和 Matformer 的 0.080。对于群 113、162、200、216，ALIGNN 和 Matformer 的零样本 MAE 超过全数据 MAE 五倍以上，而 CFT 的退化幅度小得多。这一结果直接验证了核心假设：通过显式参数化群约束，CFT 能够泛化到未见群，而基线方法由于缺乏跨群参数共享机制，在面对新群时几乎完全失效。

**适用边界与已知局限。** CFT 的有效性依赖于几个关键假设。第一，实际构造中需要对倒易格点进行有限半径截断（R=5，约 514 个模式），这在高精度需求下可能引入近似误差——虽然 Figure 7 显示 514 个模式在轨道距离回归任务上已达到最佳性能-效率权衡，但该权衡是否对不同的材料属性稳定尚不清楚。第二，预训练位置编码模块需要额外的训练阶段和轨道距离监督信号（Equation 23），增加了整体流程的复杂度；尽管 Table 3 显示预训练在所有四个属性上带来显著提升（总能量 MAE 从 0.207 降至 0.197，剪切模量从 0.215 降至 0.158），但这一额外成本是否可以在自监督方式下被消除仍是开放问题。第三，零样本实验仅针对含反演对称性的群（约 49% 数据），对其他类型未见群（如仅含平移对称性的群）的泛化能力尚未验证。第四，CFT 在带隙和体模量上未超越 Matformer，表明在某些属性上基于图的方法可能仍具优势，这暗示了傅里叶基表示在捕捉局部化学环境细节方面的固有局限。

**开放问题。** 首先，如何自适应地选择傅里叶模式截断半径 R 以平衡精度与效率？当前 R=5 的选择基于经验权衡，但不同材料属性可能对高频模式敏感度不同。其次，CFT 能否推广到其他类型的对称群（如磁空间群、超空间群）？理论上，只要群操作可表示为倒易格点上的线性变换，路由矩阵的构造框架就适用，但实际实现中可能面临计算瓶颈——对于极高分辨率或超大晶胞，**M_G** 的规模可能成为限制因素。第三，对于数据极度稀疏的群（如仅有几个样本），CFT 的共享参数机制能否有效防止过拟合？这需要进一步消融实验验证。最后，CFT 的 Transformer 主体是否可以替换为其他架构（如图神经网络）以进一步提升特定任务的性能？这指向了一个更根本的问题：傅里叶基表示与不同下游架构之间的兼容性边界在哪里。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Single_Architecture_for_Representing_Invariance_Under_Any_Space_Group.pdf

![[paperPDFs/ICLR_2026/A_Single_Architecture_for_Representing_Invariance_Under_Any_Space_Group.pdf]]
