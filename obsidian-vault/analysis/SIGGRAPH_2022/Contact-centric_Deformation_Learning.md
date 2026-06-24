---
title: Contact-centric Deformation Learning
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Contact_centric_Deformation_Learning.pdf
project_link: "http://mslab.es/projects/ContactCentricLearning/"
code_link: null
aliases:
- CCDL
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用以接触为中心（contact-centric）的参数化方式，将接触位移场定义在碰撞体空间（collider space）中，从而使得接触变形场更加平滑。
primary_logic: 接触变形在碰撞体空间中比在物体空间中平滑得多，因此转而学习碰撞体空间中的位移场可以大幅降低所需训练样本的复杂度，实现高效且泛化能力强的学习。
claims:
- 碰撞体空间中的接触位移场明显比物体空间中的更平滑，这一特性直接决定了方法的学习能力。
- 仅使用8个训练姿势即可在橡胶鸭场景（87维子空间）中实现准确的接触变形；MANO手部模型只需1个姿势。
- 在3D Jelly测试中，仅用5个训练样本，本方法相对误差为57%，而物体中心的Romero et al. 2021方法为99%。
- 稀疏化映射可大幅减少所需训练数据：在Worm示例中，1个样本时稀疏化将相对误差从96%降至44%。
---

# Contact-centric Deformation Learning

> [!tip] 核心洞察
> 接触变形在碰撞体空间中比在物体空间中平滑得多，因此转而学习碰撞体空间中的位移场可以大幅降低所需训练样本的复杂度，实现高效且泛化能力强的学习。

| 字段 | 内容 |
|------|------|
| 中文题名 | 以接触为中心的形变学习 |
| 英文题名 | Contact-centric Deformation Learning |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](http://mslab.es/projects/ContactCentricLearning/) · [Project](https://neuralfields.cs.brown.edu/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Contact-Centric Deformation Learning |
| Dataset | 3D Jelly, Worm, Rubber duck |

> [!tip] 效果简介
> - 3D Jelly (star-shape collider) 上，Relative error 57% vs 99% (Romero et al. 2021) (-42%)。
> - Worm (2D) 上，Relative error (1 training sample) 44% (sparse) vs 96% (dense) (-52%)。
> - Rubber duck (87-D subspace) 上，Qualitative fidelity Accurate contact detail with 8 training poses vs Linear subspace model fails (Significant improvement)。

## 概要

现有基于物体中心（object-centric）的接触变形学习方法面临一个根本瓶颈：接触驱动的位移场在物体空间中高度不平滑，导致学习此类变形需要对物体的高维状态空间进行密集采样，泛化能力极差。本文提出**以接触为中心（contact-centric）的形变学习**方法，将接触位移场定义在碰撞体空间（collider space）中——核心洞察在于，接触变形在碰撞体空间中远比在物体空间中平滑，从而大幅降低了学习所需训练样本的复杂度。

方法将总变形分解为子空间动力学变形与学习得到的接触位移场之和，使用MLP网络学习从碰撞体空间点和稀疏相对构型到碰撞体空间位移向量的连续映射，并通过稀疏化输入权重矩阵进一步降低输入维度。仅需极少训练样本即可实现高保真接触变形：在87维子空间的橡胶鸭场景中仅用**8个训练姿势**即可准确泛化，MANO手部模型仅需**1个姿势**；在3D Jelly测试中，仅用5个训练样本，本方法相对误差为**57%**，而物体中心的Romero et al. 2021方法高达**99%**。该方法定位于子空间仿真与学习型校正的交叉点，通过改变位移场的参数化空间这一关键设计，显著提升了接触变形学习的样本效率和泛化能力。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有基于子空间动力学的可变形体仿真方法在模拟接触驱动的局部变形时面临根本性困难。传统方法采用**物体中心（object-centric）**的参数化方式，直接在物体空间学习接触位移场。然而，当刚性碰撞体在物体表面扫过时，接触位移在物体空间中呈现高度不平滑的分布——同一碰撞体位置可能对应物体表面完全不同的区域，导致位移场出现剧烈跳变。这种不平滑性使得学习接触变形需要对物体的高维状态空间进行密集采样，而随着子空间维度的增加（如橡胶鸭示例的87维），所需的训练样本量呈指数增长，在实际应用中不可行。

本文的核心洞察在于：**接触变形在碰撞体空间（collider space）中比在物体空间中平滑得多**。当从碰撞体的局部参考系观察时，接触位移场随碰撞体与物体表面相对位置的变化是缓慢且连续的，这从根本上降低了学习任务的复杂度。基于这一发现，作者提出**以接触为中心（contact-centric）的形变学习**框架，将接触位移场定义在碰撞体空间而非物体空间，从而以极少的训练样本实现高保真度的接触变形学习。

### 总体框架

方法将世界空间中可变形体上任意材料点 $\bar{x}$ 的总变形场 $x(\bar{x})$ 分解为两个可叠加的分量：

$$x(\bar{x}) = \tilde{x}(\bar{x}) + u(\bar{x})$$

其中 $\tilde{x}(\bar{x})$ 是由子空间动力学仿真产生的**基础变形**，负责模拟物体的整体运动和弹性行为；$u(\bar{x})$ 是**接触位移**，用于校正因接触产生的局部细节变形。这一分解的核心优势在于：基础变形通过成熟的子空间仿真方法高效计算，而接触位移则通过一个在碰撞体空间中学习的连续向量场来建模，两者在统一的子空间框架内协同工作。

### 关键创新槽位一：接触中心的参数化空间

方法最核心的改变在于将接触位移场的定义域从物体空间迁移到碰撞体空间。设 $\mathbf{T}(\mathbf{z})$ 为碰撞体在世界空间中的刚体变换矩阵，则世界空间的接触位移 $u(\bar{x})$ 通过碰撞体空间位移 $r(\bar{z})$ 经刚体变换得到：

$$u(\bar{x}) = \mathbf{T}(\mathbf{z}) \cdot r(\bar{z}), \quad \text{其中} \ \bar{z} = \mathbf{T}(\mathbf{z})^{-1} \cdot \tilde{x}(\bar{x})$$

这里的 $\bar{z}$ 是材料点 $\bar{x}$ 在碰撞体局部坐标系中的对应位置。碰撞体空间位移函数 $r(\bar{z})$ 进一步依赖于碰撞体空间坐标和物体-碰撞体之间的相对构型：

$$r(\bar{z}) \equiv f\left(\bar{z}, \ \mathbf{T}(\mathbf{z})^{-1} \cdot \mathbf{x}\right)$$

其中 $\mathbf{x}$ 是物体当前的子空间状态向量，$\mathbf{T}(\mathbf{z})^{-1} \cdot \mathbf{x}$ 表示从碰撞体视角观察的物体相对构型。这一参数化的因果机制在于：碰撞体作为接触变形的“施力方”，其局部参考系天然地组织了接触区域的几何关系，使得位移场在该空间中具有内在的平滑性（见 Fig. 3 的可视化对比）。这种平滑性直接转化为学习效率的质变——神经网络仅需学习一个缓慢变化的函数，而非物体空间中剧烈跳变的映射。

![[assets/figures/papers/paper_list_l11_http_mslab_es_projects_ContactCentricLearning/figures/003_Figure_3.jpg]]
*Figure 3: The close-ups compare the representation of contact displacements in object space ??¯ (left) vs. collider-space ??¯ (right) for these two examples. As the collider sweeps through the surface of the deformable object, colliderspace contact displacements are notably smoother, and this drastically impacts the learning ability of our method*

### 关键创新槽位二：稀疏化输入映射

尽管碰撞体空间参数化大幅降低了学习难度，但接触位移函数 $f$ 的输入仍包含高维的子空间状态向量 $\mathbf{x}$。作者进一步观察到，**接触变形主要由物体上与接触区域邻近的控制柄（handles）或骨骼（bones）的局部构型决定**，远离接触点的自由度对位移影响微乎其微。基于这一局部性原理，方法引入稀疏权重矩阵 $\mathbf{W}(\bar{x})$ 对输入进行降维：

$$r(\bar{z}) \approx f\left(\bar{z}, \ \mathbf{W}(\bar{x}) \cdot \mathbf{T}(\mathbf{z})^{-1} \cdot \mathbf{x}\right)$$

其中稀疏权重矩阵由子空间基底 $\mathbf{U}(\bar{x})$ 构建：

$$\mathbf{W}(\bar{x}) = \text{diag}(\mathbf{U}(\bar{x}))$$

这里的 $\mathbf{U}(\bar{x})$ 可以是 BGBC 基底或蒙皮权重矩阵在材料点 $\bar{x}$ 处的取值。该对角矩阵仅保留与当前材料点相关的子空间自由度，将全维度的子空间状态压缩为仅包含局部信息的稀疏表示。这一设计的因果逻辑是：通过强制网络仅关注局部相关自由度，消除了远距离无关状态对学习的干扰，使网络能够准确辨识真正影响接触位移的构型因素。Fig. 4 的实验表明，在相同训练数据下，稀疏化函数能成功消歧子空间状态的贡献，而稠密函数则因输入维度过高而学习失败。

![[assets/figures/papers/paper_list_l11_http_mslab_es_projects_ContactCentricLearning/figures/004_Figure_4.jpg]]
*Figure 4: Two examples (top, bottom) to depict that contact displacements are dominated by the configuration of nearby handles/bones of the deformable object. We leverage this observation designing a sparse approximation of the contact displacement function. Here, we compare ground-truth displacements (left), learned displacements with sparsifying weights, i.e., Eq. (4) (middle), and without sparsifying weights, i.e., Eq. (3) (right). With the same training data, the sparse function achieves superior results, as it succeeds to disambiguate the subspace state that contributes to the contact displacements*

### 关键创新槽位三：连续向量场表示

与先前工作中使用的离散近似（如 PCA 基函数线性组合）不同，本方法将碰撞体空间位移 $r(\bar{z})$ 建模为一个由 MLP 网络参数化的**连续向量场**。该网络以碰撞体空间坐标 $\bar{z}$ 和稀疏化后的相对构型 $\mathbf{W}(\bar{x}) \cdot \mathbf{T}(\mathbf{z})^{-1} \cdot \mathbf{x}$ 为输入，输出三自由度位移向量。连续表示的优势在于：

1. **空间连续性**：网络可以在任意碰撞体空间位置求值，不受网格分辨率的限制，能够产生平滑的位移场。
2. **参数效率**：一个紧凑的 MLP（神经元数量比基线方法少一个数量级）即可表达复杂的接触变形模式。
3. **泛化能力**：连续函数在未见过的碰撞体位置和物体构型之间进行自然插值，这是离散基函数方法难以实现的。

### 训练数据生成与推理路径

**训练阶段**的数据生成采用“投影全空间仿真”策略。首先采样碰撞体与可变形体的相对构型（包括物体的子空间状态 $\mathbf{x}$ 和碰撞体的刚体变换 $\mathbf{T}(\mathbf{z})$），然后运行全空间有限元仿真，并通过投影矩阵 $\mathbf{P} = \mathbf{I} - \mathbf{U}(\mathbf{U}^T\mathbf{U})^{-1}\mathbf{U}^T$ 将全空间变形投影到子空间的正交补空间，提取出子空间无法表达的接触位移作为监督信号。碰撞体空间的采样点通过将物体体积网格节点变换到碰撞体坐标系获得。这种采样策略确保训练数据覆盖了接触可能发生的空间区域和构型范围。

**推理阶段**，接触位移 MLP 被嵌入到子空间动力学求解器中。在每一时间步，求解器通过 Newton-CG 优化最小化包含惯性项 $W_{\text{inertial}}$、弹性项 $W_{\text{elastic}}$ 和接触项 $W_{\text{contact}}$ 的总能量：

$$\mathbf{x} = \arg\min \left(W_{\text{inertial}} + W_{\text{elastic}} + W_{\text{contact}}\right)$$

接触项的能量计算需要查询 MLP 以获得当前构型下的接触位移，从而将学习到的接触变形校正无缝融入动态仿真流程。

### 方法边界条件

本方法的设计存在明确的适用范围限制：每个 MLP 模型针对**单一刚性碰撞体**训练，无法直接处理多碰撞体同时交互或碰撞体形状动态变化的场景；接触位移的学习仅支持**刚体-可变形体**之间的接触，不适用于可变形体之间的相互接触。这些限制源于碰撞体空间参数化的基本假设——需要预先定义唯一的碰撞体参考系。

## 实验与关键发现

### 核心实验设置

本文在多个不同复杂度的场景上验证方法，涵盖 2D 蠕虫（Worm）、3D 果冻（Jelly）、橡皮鸭（Rubber Duck）、浮动体（Floater）以及 MANO 手部模型。所有实验共享统一的子空间动力学框架，对比基线包括：**线性子空间模型**（Wang et al., 2015）和物体中心接触变形学习方法 **Romero et al. 2021**（ACM Trans. Graph.）。训练数据采样策略和运行时性能统计详见 Table 1。

![[assets/figures/papers/paper_list_l11_http_mslab_es_projects_ContactCentricLearning/figures/007_Table_1.jpg]]
*Table 1: Details about dataset size and runtime performance for the different objects used to showcase our method. For descriptions about sample types (e.g., X, ???? , SO(3), D), see Section 4.2*

### 主结果：极低训练样本下的泛化能力

本方法最核心的实验发现是：**接触中心参数化使得仅需极少训练样本即可实现高保真度的接触变形泛化**。

- **3D Jelly 场景**（Table 2）：在仅使用 5 个训练姿态时，本方法相对误差为 **57%**，而物体中心方法 Romero et al. 2021 为 **99%**（几乎完全无法学习）。当训练姿态增加到 25 个时，本方法仅略有提升，而物体中心方法仍表现极差。这直接证明了接触中心策略从根本上规避了物体空间中的维度灾难问题。

![[assets/figures/papers/paper_list_l11_http_mslab_es_projects_ContactCentricLearning/figures/006_Figure_6.jpg]]
*Figure 6: The generalization capabilities of our collider-centric method are also evident in this 3D jelly example. Our method is accurate when trained with just 5 poses of the jelly, and increasing the number of poses to 25 provides little gain. In contrast, object-centric learning, as done by Romero et al [2021], fails to learn contact deformations with 5 poses, and only slightly improves with 25 poses. In Table 2 we provide numerical comparisons. Object-centric learning suffers the curse of dimensionality, and would require an intractable number of training poses*

- **橡皮鸭场景**（87 维子空间）：仅使用 **8 个训练姿态**即可在实时交互中准确再现接触变形细节（Fig. 7, Fig. 8）。Fig. 8 展示了随机选取的测试帧与其最近训练样本的对比，二者在物体状态上差异显著，但本方法仍能正确泛化——这是接触中心设计的直接收益：网络学到的是碰撞体空间中的平滑位移场，而非物体空间中的复杂映射。

![[assets/figures/papers/paper_list_l11_http_mslab_es_projects_ContactCentricLearning/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative evaluation. We show 4 frames of a sequence where a collider (semitransparent, for better visualization) interacts with a rubber duck. Our method (center), closely matches the natural deformations due to contact that emerge using a full simulation model (left). In contrast, a linear model [Wang et al. 2015] (right) is unable to deform correctly*

- **MANO 手部模型**：仅使用 **1 个手部姿态**进行训练，即可在实时动力学模拟中生成高分辨率接触变形（Fig. 1）。该结果在 teaser 图中作为核心亮点展示。

### 与基线方法的定量对比

**Table 2** 提供了 3D Jelly 场景的系统对比：

| 方法 | 训练姿态数 | 相对误差 |
|------|-----------|---------|
| 本方法（接触中心） | 5 | 57% |
| Romero et al. 2021（物体中心） | 5 | 99% |
| 本方法（接触中心） | 25 | 约 55%（略有改善） |
| Romero et al. 2021（物体中心） | 25 | 仍远高于本方法 |

关键观察：物体中心方法即使增加训练数据也几乎无法学习接触变形，因为接触位移在物体空间中高度不平滑（Fig. 3 提供了直观对比）。本方法在 5 个样本时已接近饱和性能，继续增加数据收益递减——这表明接触中心参数化已充分捕捉了问题的本质结构。

**Fig. 5** 进一步显示，本方法在使用比 Romero et al. 2021 少一个数量级的神经元和训练数据的情况下，仍能紧密匹配全仿真的真实感。当 Romero et al. 2021 在同样缩减的数据集上训练时，完全无法学习接触变形。

### 消融实验：稀疏化映射的关键作用

**Table 3** 在 Worm 场景上系统验证了稀疏化映射（Eq. (4)）的贡献：

| 训练样本数 | 稀疏化（本方法） | 无稀疏化（Eq. (3)） |
|-----------|----------------|-------------------|
| 1 | **44%** | 96% |
| 2 | 显著低于无稀疏化 | 仍较高 |
| 更多样本 | 持续优于无稀疏化 | 逐渐改善但始终落后 |

核心发现：**在极端少样本条件下（1 个训练样本），稀疏化将相对误差从 96% 降至 44%**。这验证了方法的另一个关键设计：接触位移主要由变形物体上邻近碰撞点的局部区域（handles/bones）的构型决定。稀疏权重矩阵 $\mathbf{W}(\bar{x}) = \mathrm{diag}(\mathbf{U}(\bar{x}))$ 通过子空间基底构建，有效消除了不相关子空间状态对接触位移学习的干扰（Fig. 4 提供了定性可视化）。

### 定性评估与全仿真对比

**Fig. 7** 展示了橡皮鸭场景的定性对比：本方法（中间列）紧密匹配全仿真模型（左列）的自然接触变形，而线性子空间模型（右列）完全无法产生正确的变形。**Fig. 9** 在浮动体穿壳场景中进一步验证：全空间仿真中浮动体通过挤压变形让壳穿过，本方法成功再现了这一行为，线性子空间则导致壳被卡住。

### 失败模式与适用边界

本文明确指出了方法的三个主要局限：

1. **每个刚性碰撞体需单独训练模型**：当前方法假设碰撞体是单一且已知的刚性物体。对于包含多个碰撞体或碰撞体动态变化的场景，需要为每个碰撞体训练独立网络，无法直接泛化。

2. **仅支持刚性碰撞体**：方法基于碰撞体空间的刚体变换 $\mathbf{T}(\mathbf{z})$ 来定义接触位移（Eq. (2)），因此无法建模可变形体之间的接触交互。

3. **网络架构未充分探索**：文中提到傅里叶特征（Fourier features）等网络优化技术留作未来工作，暗示当前 MLP 架构可能仍有改进空间以进一步提升精度。

### 实验公平性说明

与 Romero et al. 2021 的对比在相同子空间框架下进行，且本方法使用了**更少的训练数据和网络参数**。这排除了“更多计算资源带来更好结果”的替代解释，凸显了接触中心策略本身带来的根本性优势：碰撞体空间中的平滑性使得学习问题本质上更容易。

![[assets/figures/papers/paper_list_l11_http_mslab_es_projects_ContactCentricLearning/figures/005_Figure_5.jpg]]
*Figure 5: Our approach significantly improves the generalization capabilities of the state-of-the-art method of Romero et al [2021], and closely matches the realism of full simulation. Our method is able to learn the complex interaction between the star-shape collider and the deformable jelly using one order of magnitude less neurons and training data than the original settings used by Romero et al [2021]. In contrast, when trained with such reduced dataset, Romero et al [2021] are unable to learn deformations due to contact*

## 定位与知识库关联

本文的核心贡献在于改变了接触驱动变形学习中**位移场参数化空间**这一关键设计 slot：从传统的**物体中心（object-centric）**参数化切换为**接触中心/碰撞体空间（collider space）**参数化。这一改变直接回应了现有方法的根本瓶颈——物体空间中的接触位移场高度不平滑，导致学习器需要对可变形物体的高维状态空间进行密集采样才能捕获接触细节，而这在子空间维数稍高时即变得不可行。

**相对于已有方法的本质差异。** 最直接的对比基线是 **Romero et al.**（ACM Trans. Graph. 2021）提出的物体中心接触变形学习方法。该方法同样在子空间动力学框架下添加学习校正项，但其位移场定义在物体空间，因此遭遇了维度灾难：当子空间维数升高时，所需训练姿态数量呈指数增长。本文通过将位移场 $r(\bar{z})$ 定义在碰撞体的局部参考系中（Eq. 2），利用“接触位移在碰撞体空间中远比在物体空间中平滑”这一核心观察（Fig. 3），从根本上降低了学习问题的复杂度。实验表明，在 3D Jelly 场景中，仅使用 5 个训练姿态，本方法相对误差为 57%，而 Romero et al. 方法高达 99%（Table 2）；且本方法使用的神经元数量和训练数据均少一个数量级（Fig. 5）。另一基线为线性子空间模型 **Wang et al.**（ACM Trans. Graph. 2015），其在无学习校正的情况下完全无法表达接触引起的局部细节变形（Fig. 7, Fig. 9），本方法则通过叠加学习的接触位移场弥补了这一能力缺口。

**改变的 slot 与因果链条。** 除参数化空间外，本文还改变了两个辅助但重要的 slot：（1）**位移场的表示方式**，从离散 PCA 基切换到连续 MLP 向量场，使得位移可以在碰撞体空间任意点处被查询，支持更精细的接触变形；（2）**输入映射的稀疏性**，从稠密的全子空间状态输入切换为通过子空间基底构建的稀疏权重矩阵 $\mathbf{W}(\bar{x})$ 进行局部化（Eq. 4），利用接触变形仅依赖于碰撞点附近少数控制柄/骨骼构型这一物理先验，进一步降低了学习难度。因果链条为：碰撞体空间参数化 → 位移场平滑 → 所需训练样本大幅减少 → 高维子空间下的泛化成为可能；稀疏化 → 输入维度降低 → 极少量样本下的学习稳定性提升（Table 3：Worm 示例中 1 个训练样本时相对误差从 96% 降至 44%）。

**知识库挂载点。** 本文的方法学贡献可挂载到以下知识节点：
- **子空间仿真 + 学习校正**：作为对“数据驱动子空间细节增强”这一研究脉络的推进，本文揭示了参数化空间选择对学习效率的决定性影响，为后续工作提供了“接触中心”这一新的设计范式。
- **接触力学与碰撞处理**：本文的接触位移场本质上是一种准静态接触响应的连续表示，可视为对传统基于惩罚力或约束的接触模型的学习式替代，连接了物理仿真与神经表示。
- **神经隐式场与连续表示**：将接触变形建模为碰撞体空间中的连续向量场，与神经辐射场（NeRF）、神经 SDF 等连续表示共享哲学基础，但在物理交互驱动的变形领域开辟了新应用场景。

**适用边界与限制。** 本方法的设计假设了以下边界条件：（1）碰撞体为**单个刚性物体**，每个碰撞体需单独训练模型，无法直接处理多碰撞体或碰撞体动态变化的场景；（2）仅支持刚性碰撞体对可变形体的单向接触，不能建模可变形体之间的相互接触；（3）接触位移被假设为准静态（仅依赖于当前相对构型），不显式建模接触过程中的历史依赖效应。此外，神经网络架构（如傅里叶特征、周期性激活函数）的优化被列为未来工作，暗示当前架构可能尚未达到该表示容量的上限。

**后续启发价值。** 本文的“接触中心”思想具有跨问题迁移的潜力：在手-物交互重建、抓取合成、触觉渲染等任务中，接触区域的变形同样在接触体局部坐标系中更为平滑，采用类似的参数化策略可能显著降低学习难度。将本方法扩展至多碰撞体或多可变形体交互场景，需要解决碰撞体空间选择与组合的策略问题，这构成一个明确的研究方向。此外，稀疏化映射中利用子空间基底构建局部权重的做法，为其他高维物理系统的输入降维提供了可复用的设计模式。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Contact_centric_Deformation_Learning.pdf]]