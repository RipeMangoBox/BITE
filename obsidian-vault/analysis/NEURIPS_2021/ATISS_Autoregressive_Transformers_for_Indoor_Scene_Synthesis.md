---
title: "ATISS: Autoregressive Transformers for Indoor Scene Synthesis"
type: paper
paper_level: A
venue: NeurIPS
year: 2021
pdf_ref: paperPDFs/NEURIPS_2021/ATISS_Autoregressive_Transformers_for_Indoor_Scene_Synthesis.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/ATISS/
aliases:
- ATISS
tags:
- NEURIPS_2021
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在训练时强制最大化学场景在所有可能物体排列下的对数似然（Monte Carlo近似），从而使模型学习到排序不变性，能够以任意顺序生成物体。"
primary_logic: "将室内场景生成重新定义为无序集合生成问题，利用Transformer固有的排列等变性，设计了一个单一端到端训练的自回归模型，既能进行全自动布局合成，又能无缝支持场景完成、物体建议与重排等交互式应用，且在参数量和推理速度上均显著优于已有方法。"
claims:
- "在所有房间类型上，ATISS的FID、分类准确度（更接近0.5）和类别KL散度均优于FastSynth和SceneFormer。"
- "消融研究表明，采用无序训练（置换不变性）相比有序训练可将场景分类准确度从0.760降至0.562，显著提升生成真实性。"
- "感知研究中，73.1%的用户认为ATISS生成的场景比FastSynth更真实，且错误率不到后者的一半。"
- "ATISS在交互式场景完成、物体建议和失败案例检测等任务上展现出基线方法无法实现的功能。"
---

# ATISS: Autoregressive Transformers for Indoor Scene Synthesis

> [!tip] 核心洞察
> 将室内场景生成重新定义为无序集合生成问题，利用Transformer固有的排列等变性，设计了一个单一端到端训练的自回归模型，既能进行全自动布局合成，又能无缝支持场景完成、物体建议与重排等交互式应用，且在参数量和推理速度上均显著优于已有方法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ATISS：用于室内场景合成的自回归Transformer |
| 英文题名 | ATISS: Autoregressive Transformers for Indoor Scene Synthesis |
| 会议/期刊 | NeurIPS 2021 |
| Links | [paper](https://arxiv.org/abs/2110.03675); [Project](https://research.nvidia.com/labs/toronto-ai/ATISS/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ATISS |
| Dataset | 3D-FRONT Bedrooms (FID ↓), 3D-FRONT Living Rooms (FID ↓), 3D-FRONT Dining Rooms (FID ↓), 3D-FRONT Libraries (FID ↓) |

> [!tip] 效果简介
> - 3D-FRONT Bedrooms (FID ↓) 上，Fréchet Inception Distance 为 38.39，对比 FastSynth: 40.89, SceneFormer: 43.17，变化 -2.50 vs FastSynth, -4.78 vs SceneFormer。
> - 3D-FRONT Living Rooms (FID ↓) 上，Fréchet Inception Distance 为 33.14，对比 FastSynth: 61.67, SceneFormer: 69.54，变化 -28.53 vs FastSynth, -36.40 vs SceneFormer。
> - 3D-FRONT Dining Rooms (FID ↓) 上，Fréchet Inception Distance 为 29.23，对比 FastSynth: 55.83, SceneFormer: 67.04，变化 -26.60 vs FastSynth, -37.81 vs SceneFormer。

## 概述

室内场景合成——即给定房间平面图，自动生成合理的家具布局——是计算机图形学与视觉领域的长期挑战。现有自回归方法（如**FastSynth**, Ritchie et al., 2019；**SceneFormer**, Wang et al., 2021）将场景强制建模为按固定顺序排列的物体序列（通常按类别频率排序），这一设计带来了两个根本性瓶颈：**（1）模型无法处理任意顺序的输入**，导致其难以支持场景完成、物体建议等交互式应用；**（2）在小样本房间类型上生成质量显著下降**，限制了方法的实用性和泛化能力。

本文提出 **ATISS（Autoregressive Transformers for Indoor Scene Synthesis）**，其核心思想是将室内场景生成重新定义为**无序集合生成问题**。具体而言，ATISS在训练时最大化场景在所有可能物体排列下的对数似然（通过Monte Carlo近似），迫使模型学习到排列不变性——即无论以何种顺序接收已放置的物体，都能为下一个物体生成合理的属性。这一设计利用了Transformer固有的排列等变性（移除位置编码），使得单一端到端模型既能进行全自动布局合成，又能无缝支持场景完成、物体建议与重排等交互式应用。

实验表明，ATISS在3D-FRONT数据集的卧室、客厅、餐厅、书房四种房间类型上，FID指标全面优于FastSynth和SceneFormer（客厅场景FID降低28.53，餐厅降低26.60），且场景分类准确度更接近理想值0.5（卧室从0.883/0.945降至0.562），意味着生成场景几乎难以与真实场景区分。感知用户研究中，73.1%的受试者认为ATISS生成的场景比FastSynth更真实，错误率不到后者的一半。同时，ATISS的参数量更少，推理速度显著更快。消融研究进一步证实，无序训练是性能提升的关键因素：将ATISS改为有序训练后，场景分类准确度从0.562恶化至0.760。

## 背景与动机

室内场景合成（indoor scene synthesis）是计算机图形学与视觉领域的长期课题，其目标是自动生成逼真且多样化的三维室内布局。这一任务在建筑可视化、游戏内容生成、具身智能训练环境构建等方面具有广泛的应用前景。近年来，基于数据驱动的方法，尤其是自回归模型，在该领域取得了显著进展，能够从大规模真实场景数据中学习家具的摆放规律。

然而，**现有自回归场景生成方法存在一个根本性的瓶颈**：它们将场景强制建模为有序的物体序列。具体而言，**FastSynth**（Ritchie et al., 2019）和 **SceneFormer**（Wang et al., 2021）等代表性工作均按物体类别频率对场景中的家具进行排序，然后训练模型学习这一固定顺序下的条件分布。这种“有序集合”的建模方式带来了两个严重的局限：

1. **交互灵活性受限**：由于模型仅在特定顺序下训练，它无法处理任意顺序的输入。当用户希望从任意位置、任意数量的已有家具出发进行场景完成（scene completion）或物体建议（object suggestion）时，模型的表现会急剧退化，因为输入顺序偏离了训练时的固定模式。

2. **小样本房间类型生成质量差**：对于物体数量较少或类别分布与主流房间差异较大的房型（如书房、图书馆），固定顺序的建模方式难以捕捉稀疏数据中的布局规律，导致生成结果不自然。

从更本质的层面看，室内场景中的物体集合天然是**无序**的——一个房间的布局不应因家具的列举顺序不同而被视为不同的场景。但现有方法通过引入位置编码和固定排列，人为地将顺序依赖强加于模型，这与场景的本质结构相悖。

ATISS（Autoregressive Transformers for Indoor Scene Synthesis）的**核心动机**正是打破这一桎梏：将室内场景生成重新定义为**无序集合生成问题**。其核心洞察在于，Transformer架构本身具有排列等变性（permutation equivariance）——当去除位置编码后，Transformer对输入集合的处理天然与元素顺序无关。通过设计一个单一、端到端训练的自回归Transformer，ATISS既能进行全自动布局合成，又能无缝支持场景完成、物体建议乃至失败案例检测等交互式应用，且在参数量和推理速度上均显著优于已有方法。

## 核心创新

ATISS 的核心创新在于将室内场景生成从**有序序列建模**重新定义为**无序集合生成**问题，并围绕这一视角转移，系统性地重构了模型架构、训练目标和推理范式，从而在生成质量、模型效率和交互灵活性三个维度上实现了对先前方法的显著超越。

### 1. 问题重定义：从有序序列到无序集合

现有自回归场景生成方法（如 **FastSynth** (Ritchie et al., 2019) 和 **SceneFormer** (Wang et al., 2021)）将室内场景强制建模为按固定规则排序的物体序列——通常按类别出现频率降序排列。这一设计带来了两个根本性限制：

- **顺序依赖性**：模型只能处理与训练时一致的物体顺序，无法应对任意顺序的用户输入，严重制约了交互式应用（如场景完成、物体建议）的灵活性。
- **小样本泛化差**：在训练样本稀少的房间类型上，固定顺序的建模方式导致生成质量急剧下降。

ATISS 将场景重新定义为物体集合 $\mathcal{O} = \{o_1, o_2, ..., o_M\}$，其概率建模为所有可能排列下的似然之和：

$$p_{\theta}(\mathcal{O}_i \mid \mathbf{F}^i) = \sum_{\hat{\mathcal{O}} \in \pi(\mathcal{O}_i)} \prod_{j \in \hat{\mathcal{O}}} p_{\theta}(o_j^i \mid o_{<j}^i, \mathbf{F}^i)$$

这一公式化表述（Formula 1）是后续所有创新的理论基石：它明确了模型应当学习的是集合层面的分布，而非某一特定排列下的条件分布。

### 2. 训练目标：最大化所有排列下的对数似然

基于上述问题重定义，ATISS 将训练目标从最大化固定排列下的似然，改为最大化所有可能排列下的对数似然：

$$\log \hat{p}_{\theta}(\mathcal{X}) = \sum_{i=1}^N \sum_{\hat{\mathcal{O}} \in \pi(\mathcal{O}_i)} \sum_{j \in \hat{\mathcal{O}}} \log p_{\theta}(o_j^i \mid o_{<j}^i, \mathbf{F}^i)$$

由于穷举所有排列的计算代价不可承受，实际训练中采用 Monte Carlo 近似：对每个训练场景随机采样一个排列，并截取前 $T$ 个物体作为上下文，预测序列中的下一个物体（参见 Figure 3）。这种**训练时强制排列不变性**的策略是 ATISS 的关键“因果旋钮”——消融实验（Table 7）证明，无序训练（Ours）相比有序变体（Ours+Order）可将场景分类准确度从 0.760 降至 0.562（更接近理想值 0.5），即生成的场景更难与真实场景区分，真实性显著提升。

### 3. 架构简化：单一Transformer替代多分支模型

与 SceneFormer 使用四个独立 Transformer 分别预测不同属性的设计不同，ATISS 采用**单一 Transformer 编码器**端到端预测所有物体属性。架构由四个核心模块构成（Figure 2）：

- **Layout Encoder**：使用 ResNet-18 提取房间平面图的全局特征 $\mathbf{F}$，为生成提供空间约束。
- **Structure Encoder**：将每个已生成物体的属性映射为上下文嵌入 $\mathbf{C}_j$，其中类别使用可学习的嵌入，位置/大小/朝向使用正弦位置编码 $\gamma(\cdot)$ 保留细粒度连续信息。
- **Transformer Encoder**：以 $\{\mathbf{F}\} \cup \{\mathbf{C}_j\} \cup \{\mathbf{q}\}$ 为输入，通过 4 层 8 头自注意力学习顺序无关的场景上下文，预测查询向量 $\hat{\mathbf{q}}$。
- **Attribute Extractor**：根据 $\hat{\mathbf{q}}$ 自回归生成下一个物体的类别、位置、朝向和大小，其中连续属性使用混合 logistic 分布建模。

关键设计在于**完全移除位置编码**——Transformer 的输入是无序集合，自注意力机制天然具有排列等变性，使得模型输出与物体输入顺序无关。这与基线方法中依赖位置编码来维持序列顺序的做法形成根本性差异。

### 4. 能力跃迁：从自动生成到交互式应用

上述创新使 ATISS 在功能边界上实现了质的突破。由于模型学习的是集合层面的分布，它能够无缝支持三种此前基线方法无法实现的交互式应用：

- **场景完成**（Figure 7）：给定任意数量和类别的已固定物体，模型可以以任意顺序接收这些约束，并生成合理的补全布局。
- **物体建议**（Figure 9）：用户指定可接受的位置区域，模型根据已有场景上下文推荐合适的物体类别和属性。
- **失败案例检测与纠正**（Figure 8）：模型能够识别场景中摆放不自然的物体，并将其重新放置到合理位置。

这些能力直接源于“无序集合生成”这一核心视角转移，而非附加的后处理或独立模块。

### 5. 效率跃迁：更少的参数，更快的推理

架构简化带来了显著的效率优势。ATISS 的参数量仅为 SceneFormer 的约 1/4，推理速度最高可达基线方法的 8 倍（Table 2, Table 3）。这意味着 ATISS 不仅生成质量更高、功能更丰富，而且更适合实时交互场景的部署需求。

## 整体框架

ATISS 将室内场景生成重新定义为**无序物体集合的自回归生成**问题。其核心设计动机在于：传统自回归方法（如 **FastSynth** (Ritchie et al., 2019) 和 **SceneFormer** (Wang et al., 2021)）将场景强制建模为固定顺序的物体序列，导致模型无法处理任意顺序的输入，限制了交互式应用（场景完成、物体建议）的灵活性。ATISS 通过**训练时最大化场景在所有可能物体排列下的对数似然**，使模型学习到排序不变性，从而以单一端到端网络同时支持全自动布局合成与多种交互式应用。

### 整体数据流

ATISS 的网络由四个核心模块串联构成，数据流如图 2 所示：

1. **Layout Encoder（布局编码器）**：以房间平面图的二值图像为输入，使用 ResNet-18 提取全局布局特征 $\mathbf{F}$。
2. **Structure Encoder（结构编码器）**：将当前已生成的 $M$ 个物体各自的属性（类别、位置、大小、朝向）映射为上下文嵌入集合 $\mathbf{C} = \{\mathbf{C}_j\}_{j=1}^M$。
3. **Transformer Encoder（Transformer编码器）**：以 $\{\mathbf{F}\} \cup \mathbf{C} \cup \{\mathbf{q}\}$ 为输入（$\mathbf{q}$ 为可学习的查询向量），通过 4 层 8 头自注意力机制学习顺序无关的场景上下文，输出更新后的查询向量 $\hat{\mathbf{q}}$。
4. **Attribute Extractor（属性提取器）**：根据 $\hat{\mathbf{q}}$ 和先前已预测的属性，自回归地生成下一个物体的类别、位置、朝向和大小。

### 生成流程

给定一个房间平面图，生成过程如下：
1. 布局编码器提取平面图特征 $\mathbf{F}$。
2. 初始化空的上下文嵌入集合 $\mathbf{C} = \emptyset$。
3. 在每一步 $j$：
   - Transformer 编码器以 $\{\mathbf{F}\} \cup \mathbf{C} \cup \{\mathbf{q}\}$ 为输入，预测 $\hat{\mathbf{q}}$。
   - 属性提取器根据 $\hat{\mathbf{q}}$ 依次生成物体的**类别** $\mathbf{c}_j$、**位置** $\mathbf{t}_j$、**朝向** $\mathbf{r}_j$ 和**大小** $\mathbf{s}_j$，每个属性的预测均以先前已预测的属性为条件。
   - 新生成的物体通过结构编码器转换为上下文嵌入 $\mathbf{C}_j$，加入 $\mathbf{C}$。
4. 重复步骤 3，直到生成终止标记（EOS）或达到最大物体数。

### 训练流程

训练时（如图 3 所示），对于一个包含 $M$ 个物体的真实场景：
1. **随机排列**：对 $M$ 个物体进行随机排列。
2. **子集选择**：保留排列后的前 $T$ 个物体（$T$ 随机采样），丢弃其余物体。
3. **下一物体预测**：以保留的 $T$ 个物体和平面图特征为条件，预测排列中第 $T+1$ 个物体的属性。
4. **损失函数**：计算预测属性与真实属性的负对数似然（NLL）。

训练目标形式化地最大化场景在所有排列下的对数似然：
$$\log \hat{p}_{\theta}(\mathcal{X}) = \sum_{i=1}^N \sum_{\hat{\mathcal{O}} \in \pi(\mathcal{O}_i)} \sum_{j \in \hat{\mathcal{O}}} \log p_{\theta}(o_j^i \mid o_{<j}^i, \mathbf{F}^i)$$

由于穷举所有排列不可行，实际训练中通过 Monte Carlo 近似——每次迭代随机采样一个排列和子集大小 $T$ 来估计梯度。

### 排列不变性的实现机制

ATISS 实现排列不变性的关键在于：
- **不使用位置编码**：Transformer 编码器的输入中，物体上下文嵌入 $\mathbf{C}_j$ 不附加任何顺序位置编码，使得模型对输入物体的顺序无感知。
- **结构编码器中的正弦编码**：对每个物体的连续属性（位置、大小、朝向）使用正弦位置编码 $\gamma(p) = (\sin(2^0\pi p), \cos(2^0\pi p), \ldots, \sin(2^{L-1}\pi p), \cos(2^{L-1}\pi p))$，以保留细粒度数值信息，而非顺序信息。
- **共享权重**：所有物体共享同一个结构编码器和属性提取器，进一步强化排列不变性。

### 与基线方法的架构差异

| 设计维度 | FastSynth / SceneFormer | ATISS |
|---------|------------------------|-------|
| 场景表示 | 有序物体序列（按类别频率排序） | 无序物体集合 |
| 网络架构 | 多分支独立模型（SceneFormer 使用四个独立 Transformer） | 单一 Transformer 编码器 + 共享结构编码器和属性提取器 |
| 位置编码 | 使用位置编码带来顺序依赖 | 无位置编码，输入为集合 |
| 训练目标 | 最大化固定排列下的似然 | 最大化所有排列下的似然（Monte Carlo 近似） |

这一设计使得 ATISS 在参数量上显著少于基线（SceneFormer 需四个独立 Transformer），同时在推理速度上可达 **8 倍**加速，且能无缝支持场景完成、物体建议等交互式应用。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/029_Figure_22.jpg]]
*Figure 22: Difference of Per-Object Frequencies. We visualize the absolute difference between the per-object frequency of generated and real scenes using our method, FastSynth [61] and SceneFormer [74] for all room types. Lower is better*

## 核心模块与公式推导

ATISS将室内场景生成重新定义为**无序集合生成问题**，其核心架构由四个模块串联构成：布局编码器（Layout Encoder）、结构编码器（Structure Encoder）、Transformer编码器（Transformer Encoder）和属性提取器（Attribute Extractor）。整体数据流如Figure 2所示：给定一个包含$M$个物体的场景及房间平面图，布局编码器提取平面图的全局特征$\mathbf{F}$，结构编码器将已生成的$M$个物体映射为上下文嵌入集合$\mathbf{C} = \{\mathbf{C}_j\}_{j=2}^{M}$；随后，$\mathbf{F}$、$\mathbf{C}$与一个可学习的查询向量$\mathbf{q}$一同送入Transformer编码器，预测出查询向量$\hat{\mathbf{q}}$；属性提取器基于$\hat{\mathbf{q}}$自回归地预测下一个物体的属性分布，并从中采样生成新物体。

### 3.1 场景的概率建模

ATISS将场景$\mathcal{O}_i$（给定平面图特征$\mathbf{F}^i$）的概率定义为所有可能物体排列下的似然之和：

$$p_{\theta}(\mathcal{O}_i \mid \mathbf{F}^i) = \sum_{\hat{\mathcal{O}} \in \pi(\mathcal{O}_i)} \prod_{j \in \hat{\mathcal{O}}} p_{\theta}(o_j^i \mid o_{<j}^i, \mathbf{F}^i)$$

其中$\pi(\mathcal{O}_i)$表示物体集合的所有排列。这一建模方式使模型天然具备**排列不变性**——无论以何种顺序输入已放置的物体，模型都能生成合理的下一个物体。训练目标相应地变为最大化所有场景在所有排列下的对数似然：

$$\log \hat{p}_{\theta}(\mathcal{X}) = \sum_{i=1}^N \sum_{\hat{\mathcal{O}} \in \pi(\mathcal{O}_i)} \sum_{j \in \hat{\mathcal{O}}} \log p_{\theta}(o_j^i \mid o_{<j}^i, \mathbf{F}^i)$$

由于穷举所有排列不可行，实际训练中采用Monte Carlo近似：对每个场景随机采样一个排列，再从中随机截取前$T$个物体作为上下文，要求模型预测第$T+1$个物体（Figure 3）。

### 3.2 物体属性的自回归因子分解

每个物体$o_j$由其类别$\mathbf{c}_j$、3D位置$\mathbf{t}_j$、朝向$\mathbf{r}_j$和尺寸$\mathbf{s}_j$定义。ATISS按固定顺序自回归地生成这些属性：

$$p_{\theta}(o_j \mid o_{<j}, \mathbf{F}) = p_{\theta}(\mathbf{c}_j \mid o_{<j}, \mathbf{F}) \; p_{\theta}(\mathbf{t}_j \mid \mathbf{c}_j, o_{<j}, \mathbf{F}) \; p_{\theta}(\mathbf{r}_j \mid \mathbf{c}_j, \mathbf{t}_j, o_{<j}, \mathbf{F}) \; p_{\theta}(\mathbf{s}_j \mid \mathbf{c}_j, \mathbf{t}_j, \mathbf{r}_j, o_{<j}, \mathbf{F})$$

即先生成类别，再基于类别生成位置，继而生成朝向，最后生成尺寸。位置、朝向和尺寸均采用**混合logistic分布**建模：

$$\mathbf{s}_j \sim \sum_{k=1}^K \pi_k^s \, \mathrm{logistic}(\mu_k^s, \sigma_k^s), \quad \mathbf{t}_j \sim \sum_{k=1}^K \pi_k^t \, \mathrm{logistic}(\mu_k^t, \sigma_k^t), \quad \mathbf{r}_j \sim \sum_{k=1}^K \pi_k^r \, \mathrm{logistic}(\mu_k^r, \sigma_k^r)$$

消融实验表明$K=10$为最优混合分量数，$K=15$时FID反而变差（Table 5）。

### 3.3 结构编码器

结构编码器$h_{\theta}$将每个物体的属性映射为上下文嵌入，其设计保证了细粒度连续信息的保留：

$$h_{\theta}: (\mathbf{c}, \mathbf{s}, \mathbf{t}, \mathbf{r}) \mapsto [\lambda(\mathbf{c}); \gamma(\mathbf{s}); \gamma(\mathbf{t}); \gamma(\mathbf{r})]$$

其中$\lambda(\mathbf{c})$是类别$\mathbf{c}$的可学习嵌入向量；$\gamma(\cdot)$是正弦位置编码，将连续属性值映射到高维空间：

$$\gamma(p) = (\sin(2^{0}\pi p), \cos(2^{0}\pi p), \ldots, \sin(2^{L-1}\pi p), \cos(2^{L-1}\pi p))$$

这一编码使模型能精确感知物体在房间中的位置、尺寸和朝向，而非将其离散化丢失信息。

### 3.4 Transformer编码器与排列不变性

Transformer编码器接收三类输入的拼接：平面图特征$\mathbf{F}$、已生成物体的上下文嵌入集合$\mathbf{C}$、以及可学习的查询向量$\mathbf{q}$。**关键设计在于完全不使用位置编码**——传统的Transformer依赖位置编码来感知序列顺序，而ATISS刻意移除了它，使模型对输入物体的排列天然等变。这一设计是ATISS区别于SceneFormer（Wang et al., 2021）等有序方法的核心所在：SceneFormer使用四个独立Transformer并依赖位置编码，而ATISS仅用一个4层、8头注意力的Transformer编码器，参数量大幅减少（Table 3），且能无缝支持任意顺序的交互式输入。

### 3.5 属性提取器

属性提取器由四个MLP组成：$c_{\theta}$、$t_{\theta}$、$r_{\theta}$、$s_{\theta}$，各自负责预测对应属性的混合logistic分布参数（混合权重$\pi_k$、均值$\mu_k$、尺度$\sigma_k$）。生成过程为：将Transformer编码器输出的$\hat{\mathbf{q}}$与已预测的属性嵌入拼接后，依次送入各MLP，采样得到下一属性，再将其编码回高维空间用于后续属性的预测。这一自回归链保证了属性间的条件依赖关系。

**局限提示**：当前属性生成顺序固定为类别→位置→朝向→尺寸，尚未实现属性级别的排列不变性，这意味着用户无法以任意顺序指定物体的部分属性再由模型补全其余属性——这是论文明确列出的开放问题之一。

## 实验与分析

### 核心定量结果

ATISS 在 3D-FRONT 数据集的四种房间类型上均取得最优 FID 分数，且生成场景的类别分布最接近真实分布。**Table 1**（正文及附录 Table 8）报告了完整对比：

- **卧室**：FID 38.39（FastSynth 40.89，SceneFormer 43.17），分类准确度 0.562（理想值 0.5，基线分别为 0.883 和 0.945）。
- **客厅**：FID 33.14（FastSynth 61.67，SceneFormer 69.54），分类准确度 0.516，几乎无法与真实场景区分。
- **餐厅**：FID 29.23（FastSynth 55.83，SceneFormer 67.04），分类准确度 0.477。
- **书房**：FID 35.24（FastSynth 37.72，SceneFormer 55.34），分类准确度 0.521。

在所有房间类型上，ATISS 的类别 KL 散度均低于两个基线。**关键瓶颈突破**：客厅和餐厅等物体数量多、布局复杂的场景中，ATISS 的 FID 优势超过 28 点，表明无序集合建模对复杂场景的适应能力远强于固定顺序方法。

**Figure 4** 的定性对比直观展示了这一差异：FastSynth 和 SceneFormer 在客厅中频繁出现物体重叠、缺失和空间关系错误，而 ATISS 生成的布局更接近真实场景。**Figure 5** 进一步验证了模型对同一平面图能生成多样化但均合理的布局。

### 效率与参数对比

**Table 2** 和 **Table 3** 报告了推理时间与参数量：

- ATISS 的推理速度比 FastSynth 快约 8 倍，比 SceneFormer 快约 3 倍。
- ATISS 的参数量（约 7M）远小于 FastSynth（约 23M）和 SceneFormer（四个独立 Transformer，总参数量更大）。

效率优势源于单一 Transformer 架构和共享结构编码器的设计，避免了多分支独立模型的计算冗余。

### 消融实验

**排列不变性（核心因果旋钮）**：**Table 7** 的消融对比了三种变体——ATISS（无序训练）、Ours+Order（有序训练，使用位置编码和固定顺序）、Ours+Order+Random（有序训练但使用随机排列）。结果表明：

- 无序训练的 ATISS 将场景分类准确度从有序版的 0.760 降至 0.562（更接近 0.5），生成真实性显著提升。
- 仅使用随机排列而不去除位置编码的 Ours+Order+Random 改善有限，说明**去除位置编码带来的排列不变性**才是性能提升的关键机制，而非单纯的训练数据增广。

**混合 logistic 分布数量**：**Table 5** 显示 $K=10$ 时 FID 最优，$K=15$ 时性能下降（过拟合）。这表明 10 个混合分量足以捕捉物体属性的连续分布特征。

**布局编码器架构**：**Table 6** 对比 ResNet-18 与 AlexNet 作为布局编码器，ResNet-18 在所有房间类型上均取得更优 FID，验证了更强的视觉特征提取能力对场景生成的促进作用。

**附加消融**（附录 C.4）：去除结构编码器中的正弦位置编码、使用独立而非共享的属性预测 MLP、或减少 Transformer 层数，均导致 FID 上升和分类准确度偏离 0.5，证实了各模块设计的必要性。

### 感知用户研究

**Table 4** 报告了双盲 A/B 配对测试结果：

- 在 ATISS vs FastSynth 的对比中，73.1% 的受试者认为 ATISS 生成的场景更真实（$\alpha=0.01$ 置信区间下显著）。
- ATISS 的错误率（如物体重叠、穿墙）不到 FastSynth 的一半。

这一结果与定量指标一致，说明 FID 和分类准确度的提升确实反映了人类感知层面的布局质量改善。

### 交互式应用验证

ATISS 在三个交互式任务上展现出基线方法无法实现的功能：

- **场景完成**（**Figure 7**）：给定任意部分场景，ATISS 能生成合理补全，而 FastSynth 和 SceneFormer 因依赖固定顺序，无法处理任意位置的已放置物体。
- **物体建议**（**Figure 9**）：用户指定位置约束后，ATISS 能根据上下文建议合适的物体类别和属性。
- **失败案例检测与纠正**（**Figure 8** 和 **Figure 14**）：ATISS 能识别布局中不自然的物体（如位置异常），并重新放置到合理位置。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/032_Figure.jpg]]

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/034_Figure.jpg]]

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/035_Figure.jpg]]

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/037_Figure.jpg]]

这些能力直接源于训练时强制所有排列下的似然最大化，使模型学会从任意物体子集推断场景上下文。

### 失败模式与局限性

尽管整体性能优异，ATISS 仍存在以下失败模式：

1. **物体重叠**：训练数据中少量重叠样本导致模型偶尔生成桌椅重叠等不自然布局，尤其在物体密度高的场景中。
2. **属性生成顺序固定**：物体属性按类别→位置→朝向→大小的固定顺序生成，不支持属性级别的排列不变性，限制了更细粒度的交互式编辑。
3. **风格不一致**：物体检索与属性生成分离，无法保证检索到的 3D 模型风格与场景中已有物体一致。
4. **泛化边界**：仅在 3D-FRONT 数据集上训练和评估，向其他风格或更大规模场景的泛化能力有待验证。**Figure 6** 展示了在人工设计的非典型平面图上的泛化尝试，虽结果合理但缺乏定量评估。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/009_Table_2.jpg]]
*Table 2: Generation Time Comparison. We measure time (ms) to generate a scene, conditioned on a floor plan. Table 3: Network Parameters Comparison. We report the number of network parameters in millions*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/014_Figure_11.jpg]]
*Figure 11: (b) sθ(·) predicts the parameters of the mixture of logistics distribution for the size s. Figure 11: Attribute Extractor. The attribute extractor consists of four MLPs that autoregressively predict the object attributes. Here we visualize the MLP $t _ { \theta } ( \cdot$ ) for the location attribute (left side) and the MLP $s _ { \theta } ( \cdot$ ) for the size attribute (right side)

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/015_Figure_12.jpg]]
*Figure 12: Number of object occurrences in Bedrooms and Libraries*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/016_Figure_13.jpg]]
*Figure 13: Number of object occurrences in Living Rooms and Dining Rooms*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/025_Figure_18.jpg]]
*Figure 18: Absolute Difference between Object Co-occurrence in Bedrooms. We visualize the absolute difference of the probabilities of object co-occurrence computed between real and synthesized scenes using ATISS (left), FastSynth (middle) and SceneFormer (right). Larger differences correspond to warmer colors and are worse*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/033_Figure_25.jpg]]
*Figure 25: Location Distributions for Nightstand*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2110_03675/figures/036_Figure_26.jpg]]
*Figure 26: Location Distributions for Wardrobe*

## 方法谱系与知识库定位

### 1. 核心问题与瓶颈突破

室内场景生成领域长期存在一个根本性张力：**自回归模型天然的顺序依赖性与场景作为无序集合的本质之间的矛盾**。在ATISS之前，主流方法——无论是基于CNN的**FastSynth**（Ritchie et al., 2019）还是基于Transformer的**SceneFormer**（Wang et al., 2021）——都通过将场景强制建模为有序物体序列来回避这一矛盾，通常按照类别频率对物体进行排序。这种设计带来了两个致命缺陷：

1. **交互灵活性丧失**：模型只能从高频类别开始生成，无法接受任意顺序的部分场景输入，使得场景完成、物体建议等交互式应用几乎不可行；
2. **小样本房间类型退化**：对于训练数据稀少的房间类型（如餐厅、书房），固定顺序导致模型无法从有限的排列模式中充分学习，生成质量急剧下降（SceneFormer在餐厅的FID高达67.04，而ATISS仅29.23）。

ATISS的核心突破在于**将场景生成重新定义为无序集合生成问题**。其因果调控旋钮是：在训练时强制最大化场景在所有可能物体排列下的对数似然（通过Monte Carlo近似），从而使模型学习到排列不变性。这一设计直接利用了Transformer固有的排列等变性（去除位置编码后，自注意力机制对输入顺序不敏感），使得单一端到端模型既能进行全自动布局合成，又能无缝支持交互式应用。

### 2. 与基线方法的关键差异

下表从四个维度对比ATISS与主要基线方法的根本差异：

| 维度 | FastSynth (Ritchie et al., 2019) | SceneFormer (Wang et al., 2021) | ATISS (本文) |
|------|----------------------------------|--------------------------------|--------------|
| **场景表示** | 有序物体序列（按类别频率） | 有序物体序列（按类别频率） | 无序物体集合 |
| **训练目标** | 最大化固定排列下的似然 | 最大化固定排列下的似然 | 最大化所有排列下的似然（Monte Carlo近似） |
| **网络架构** | 多分支CNN独立模型 | 四个独立Transformer | 单一Transformer编码器 + 共享结构编码器和属性提取器 |
| **排列不变性** | 无（位置编码引入顺序依赖） | 无（位置编码引入顺序依赖） | 有（无位置编码，输入为集合） |
| **参数量** | 未明确报告 | 未明确报告 | 远小于SceneFormer（Table 3） |
| **推理速度** | 较慢 | 较慢 | 最快可达8倍加速（Table 2） |

**架构简化**是ATISS的另一重要贡献。SceneFormer需要四个独立Transformer分别处理类别、位置、朝向和大小预测，而ATISS使用单一Transformer编码器完成所有属性的上下文建模，通过共享的结构编码器和属性提取器实现端到端训练。这不仅减少了参数量，还避免了多模型之间的信息割裂。

### 3. 方法适用边界

**强适用场景**：
- **全自动场景合成**：给定空平面图，从零生成完整室内布局；
- **交互式场景完成**：给定任意数量、任意类别的已固定物体，补全剩余布局（Figure 7）；
- **物体建议**：用户指定位置约束（如物体中心区域），模型推荐合适的物体类别和属性（Figure 9）；
- **失败案例检测与纠正**：识别场景中摆放不自然的物体并重新定位（Figure 8, Figure 14）；
- **非典型平面图泛化**：在训练分布外的人工设计平面图上仍能生成合理布局（Figure 6）。

**弱适用或需谨慎的场景**：
- **风格一致性要求高的场景**：物体检索与属性生成分离，无法保证检索到的3D模型风格与场景中已有物体一致；
- **复杂空间关系建模**：仅使用3D包围盒和类别作为监督，未利用场景图或关系标注，可能限制了对物体间精细空间交互的学习；
- **训练数据偏差显著时**：数据中仍存在少量重叠和异常摆放样本，导致模型偶尔生成不自然的布局（如桌椅重叠）；
- **跨域泛化**：仅在3D-FRONT数据集上验证，向其他风格或更大规模场景的泛化能力有待验证。

### 4. 局限性与开放问题

**已识别的局限性**：

1. **属性级别的排列不变性缺失**：当前模型仅在物体级别实现了排列不变性，但物体属性的生成顺序仍是固定的（类别→位置→朝向→大小）。这限制了更灵活的交互式编辑——例如，用户无法先指定物体的朝向和大小，再由模型补全类别和位置。
2. **风格解耦不足**：物体的材质、颜色等风格属性未纳入生成过程，导致检索到的3D模型可能与场景整体风格不协调。
3. **监督信号稀疏**：仅使用包围盒和类别标签，未利用更丰富的空间关系标注（如“床头柜在床的两侧”），可能限制了模型对复杂空间约束的学习能力。
4. **数据质量依赖**：训练数据中的噪声（如重叠摆放）会直接传导到生成结果中。

**开放问题**：

1. **属性顺序的置换不变性**：能否将排列不变性扩展到物体属性的生成顺序上，允许用户以任意顺序指定物体的部分属性，由模型补全其余属性？这需要重新设计自回归因子分解的结构。
2. **风格感知的场景生成**：如何将物体的风格特征（材质、颜色、纹理）作为额外属性融入生成过程，实现风格一致且可控的场景合成？这可能需要在结构编码器中引入风格嵌入，并与3D模型检索建立联合优化。
3. **组合式物体表示**：该方法能否与结构化变形模型（如PartNet等部件感知表示）结合，进一步对物体内部组件和部件间关系进行建模？这将使场景生成从“物体级”下沉到“部件级”。
4. **数据偏差缓解**：如何减轻训练数据中的固有偏差（例如某些对象类别的固定空间共现模式），使模型能从更多样化甚至非结构化的数据中学习？这可能需要引入对抗训练或因果干预机制。
5. **跨领域扩展**：该架构能否扩展至其他领域（如户外场景、道路布局、分子生成），其中元素的顺序同样不应预先规定？这需要验证排列不变自回归模型在非室内场景上的泛化能力。

## 原文 PDF

![[paperPDFs/NEURIPS_2021/ATISS_Autoregressive_Transformers_for_Indoor_Scene_Synthesis.pdf]]
