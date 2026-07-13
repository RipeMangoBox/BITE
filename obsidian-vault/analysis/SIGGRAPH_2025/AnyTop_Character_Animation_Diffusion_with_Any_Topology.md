---
title: AnyTop Character Animation Diffusion with Any Topology
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/AnyTop_Character_Animation_Diffusion_with_Any_Topology.pdf
project_link: https://anytop2025.github.io/Anytop-page
code_link: null
aliases:
- ACADAT
tags:
- SIGGRAPH_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 将拓扑信息（关节关系R_S与图距离D_S）作为偏置整合到Transformer骨骼注意力中，同时引入文本关节描述实现跨骨架语义对齐，从而打通多骨架共享学习的关键环节。
primary_logic: 以逐关节独立编码取代整帧向量编码，配合融入图拓扑偏置的骨骼注意力，使单一扩散模型能同时学习不同骨架的运动分布，并利用文本先验在潜空间中建立跨骨架的语义对应，实现未见骨架泛化。
claims:
- 在Truebones Zoo多骨架数据集上，AnyTop的整体覆盖-多样性权衡显著优于MDM和SinMDM。
- 消融实验表明，移除拓扑距离和关系图嵌入（D,R）导致Coverage从80.5降至76.8，且所有指标全面退化，验证了拓扑条件注意力的关键作用。
- 在未见骨架上的泛化测试显示，随着骨架偏离训练分布（Wasserstein距离增大），生成质量（Coverage）逐步但可控地下降，证明模型具备分布外泛化能力。
- Truebones Zoo - Quadrupeds subset 上 Coverage = 89.2 ± 0.9
---

# AnyTop Character Animation Diffusion with Any Topology

> [!tip] 核心洞察
> 以逐关节独立编码取代整帧向量编码，配合融入图拓扑偏置的骨骼注意力，使单一扩散模型能同时学习不同骨架的运动分布，并利用文本先验在潜空间中建立跨骨架的语义对应，实现未见骨架泛化。

| 字段      | 内容                                                                                                                                        |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | AnyTop: 支持任意拓扑的角色动画扩散模型                                                                                                                   |
| 英文题名    | AnyTop Character Animation Diffusion with Any Topology                                                                                    |
| 会议/期刊   | SIGGRAPH 2025                                                                                                                             |
| Links   | [Project](https://anytop2025.github.io/Anytop-page) · [paper](https://arxiv.org/abs/2502.17327)                                          |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method  | AnyTop                                                                                                                                    |
| Dataset | Truebones Zoo - Quadrupeds subset, Truebones Zoo - Bipeds subset, Truebones Zoo - Flying subset                                           |

> [!tip] 效果简介
> - Truebones Zoo - Quadrupeds subset 上，Coverage 89.2 ± 0.9 vs MDM*: 83.3 ± 2.3 (+5.9)。
> - Truebones Zoo - Bipeds subset 上，Coverage 93.5 ± 0.5 vs MDM*: 87.9 ± 1.3 (+5.6)。
> - Truebones Zoo - Flying subset 上，Coverage 72.6 ± 1.8 vs MDM*: 63.7 ± 3.T (值可能有误) (~+8.9)。

## 概要

角色动画生成长期受限于一个根本瓶颈：现有运动生成方法只能处理单一或同胚骨架拓扑，无法适应自然界中千差万别的角色形态——从双足的人类、四足的犬科，到多足的昆虫和飞行的鸟类，它们的骨架在关节数量、连接关系和拓扑结构上存在本质差异。**AnyTop** 直面这一挑战，提出首个支持**任意拓扑**的角色动画扩散模型，仅需骨架结构和关节名称即可生成自然运动。

### 核心问题与方法定位

传统方法（如 **MDM** (Tevet et al., 2023) 和 **SinMDM**）将整帧所有关节特征拼接为单一向量编码，这使得模型无法处理关节数量可变的骨架，更无法在非同胚拓扑间共享学习。AnyTop 的核心洞察在于：**以逐关节独立编码取代整帧向量编码**，配合融入图拓扑偏置的骨骼注意力机制，使单一扩散模型能同时学习多种骨架的运动分布。

具体而言，AnyTop 将骨架的拓扑信息——关节关系矩阵 $\mathcal{R}_S$ 与图距离矩阵 $\mathcal{D}_S$——作为可学习的偏置整合到 Transformer 的骨骼注意力中，使关节在关注所有其他关节时优先关注拓扑邻近的关节。同时，通过 T5 编码关节名称文本并嵌入到每个关节特征中，模型在潜空间中建立了跨骨架的语义对应（如不同角色的“左手”或“右前足”），这是实现未见骨架泛化的关键。

### 主要结果

在 **Truebones Zoo** 多骨架数据集上，AnyTop 的覆盖-多样性权衡显著优于改编至多骨架训练的 MDM* 和 SinMDM* 基线（Table 3）。消融实验（Table 4）证实，移除拓扑距离和关系图嵌入后，Coverage 从 80.5 降至 76.8，所有指标全面退化，验证了拓扑条件注意力的关键作用。在未见骨架上的泛化测试（Table 2）显示，随着骨架偏离训练分布（Wasserstein 距离增大），生成质量逐步但可控地下降，证明模型具备分布外泛化能力。

### 方法谱系与知识库定位

AnyTop 位于**运动生成 × 图神经网络 × 扩散模型**的交叉点。与仅支持单骨架的扩散模型（如 MDM）和需要每骨架独立训练的 SinMDM 不同，AnyTop 通过骨骼注意力中的拓扑偏置实现了多骨架共享学习。在骨架变异性维度上（Table 1），AnyTop 是首个能处理**非同胚骨架**（Non-homeomorphic）的生成方法，覆盖了从单骨架到任意拓扑的完整谱系。其文本关节描述机制借鉴了跨模态对齐的思想，但将其应用于骨架语义空间，为未来的运动重定向、多角色交互和文本驱动生成提供了新的技术路径。

### 问题背景：角色动画中的骨架多样性挑战

在计算机动画领域，为虚拟角色生成自然运动是核心任务之一。然而，不同角色的骨架结构存在显著差异，这种差异体现在三个递进的层次上（参见 Table 1）：

1. **边长度变异（Edge Length）**：同一骨架拓扑下，骨骼长度比例不同——例如矮胖角色与高瘦角色的四肢比例差异。
2. **运动链变异（Kinematic Chain）**：关节数量或连接方式不同，但整体拓扑仍保持同胚（homeomorphic）——例如不同手指数量的人形角色。
3. **拓扑变异（Topology）**：骨架的图结构根本不同，属于非同胚（non-homeomorphic）——例如双足人类与四足动物、六足昆虫之间的差异。

第三层次的拓扑变异构成了最严峻的挑战：非同胚骨架之间不存在一一对应的关节映射，传统方法无法直接复用运动数据或模型参数。

### 现有方法缺口：为何通用角色动画难以实现

当前运动生成方法主要存在两个关键瓶颈：

**瓶颈一：无法处理多种骨架拓扑。** 主流方法（如 MDM，Tevet et al., 2023）将整帧所有关节特征拼接为单一向量进行编码，这一设计隐含假设了固定的关节数量和顺序。当面对不同拓扑的骨架时，输入维度不一致导致模型无法共享参数。SinMDM 等方法虽可处理多骨架，但需要为每种骨架独立训练模型，缺乏跨骨架的知识迁移能力。

**瓶颈二：缺乏涵盖多样拓扑的标注数据集。** 现有运动捕捉数据集多聚焦于人形角色（如 HumanML3D）或特定动物类别，缺少同时包含双足、四足、飞行、爬行等多类骨架的统一标注数据。这限制了通用角色动画模型的发展——没有数据，模型就无法学习跨骨架的运动先验。

### 本文动机：打通多骨架共享学习的关键环节

AnyTop 的核心动机在于回答一个根本性问题：**能否用一个统一的扩散模型，为任意拓扑的骨架生成自然运动？**

实现这一目标需要打通三个关键环节：

1. **拓扑信息编码**：将骨架的图结构信息（关节邻接关系 $R_S$、图距离 $D_S$、静止姿态 $P_S$）作为显式条件注入模型，使模型感知每个关节在骨架中的拓扑角色。
2. **跨骨架语义对齐**：通过文本关节描述（如 “left hand”“head”）建立不同骨架间的语义对应，使模型理解 “手” 在不同形态角色中的功能相似性。
3. **统一表示空间**：采用逐关节独立编码策略，将每个关节视为独立 token，使不同骨架的运动序列都能表示为统一格式的 token 集合，从而共享同一个 Transformer 骨干网络。

这一设计使得 AnyTop 不仅能在训练见过的骨架上生成高质量运动，还能泛化到训练中从未出现的骨架拓扑——这是迈向通用角色动画的关键一步。

## 核心方法与创新机理

AnyTop 的核心创新在于将**拓扑条件显式注入扩散模型的注意力机制**，配合**逐关节独立编码**与**文本关节语义对齐**，使单一模型能够同时学习数十种非同胚骨架的运动分布，并在未见骨架上实现零样本泛化。以下从四个关键维度展开分析。

### 1. 从整帧向量到逐关节Token：打通空间组合的关键

现有运动扩散模型（如 **MDM**，Tevet et al., 2023）将一帧内所有关节的特征拼接为单个向量作为Transformer的输入token。这种“整帧编码”方式隐式地将骨架拓扑固化在特征维度中，使得模型无法处理关节数量或连接关系不同的骨架。

AnyTop 改为**逐关节独立编码**：每一帧产生 $J$ 个token（$J$ 为关节数），每个token对应一个关节的13维特征（根相对位置、6D旋转、线速度、足部接触标签）。这一改变使得模型能够：
- 自然地处理任意数量关节的骨架，无需填充或截断；
- 在不同骨架间实现关节级的空间组合（如 Fig. 6 所示，将“啄食”的头部动作与“行走”的腿部动作组合为新的运动）。

### 2. 拓扑条件注意力：将图结构偏置注入Transformer

这是 AnyTop 最关键的架构创新。标准自注意力将所有关节平等对待，忽略了骨架固有的拓扑约束——例如，左手与右手在运动学上高度相关，而左手与左脚则相对独立。

AnyTop 在骨骼注意力（沿关节轴的自注意力）的注意力图中引入了两类可学习的拓扑偏置：

**图距离偏置** $a_{ij}^{\mathcal{D}}$：
$$a_{ij}^{\mathcal{D}} = q_i \cdot E_q^{\mathcal{D}}[\mathcal{D}_{ij}] + k_j \cdot E_k^{\mathcal{D}}[\mathcal{D}_{ij}]$$

**关节关系偏置** $a_{ij}^{\mathcal{R}}$：
$$a_{ij}^{\mathcal{R}} = q_i \cdot E_q^{\mathcal{R}}[\mathcal{R}_{ij}] + k_j \cdot E_k^{\mathcal{R}}[\mathcal{R}_{ij}]$$

最终的骨骼注意力得分为：
$$a_{ij} = \frac{q_i \cdot k_j + a_{ij}^{\mathcal{D}} + a_{ij}^{\mathcal{R}}}{\sqrt{F}}$$

其中 $\mathcal{D}_{ij}$ 为关节对 $(i,j)$ 在图上的最短路径距离，$\mathcal{R}_{ij}$ 编码关节间的结构关系（如父子、兄弟、祖先-后代等）。这使得每个关节在关注所有关节的同时，**优先关注拓扑上邻近的关节**，从而在不同骨架间共享运动先验。

消融实验（Table 4）提供了决定性证据：移除图属性嵌入（$D,R$）后，Coverage 从 80.5 降至 76.8，Inter Diversity 从 0.312 降至 0.303，Intra Diversity Diff. 从 0.118 升至 0.127，所有指标全面退化。这证实了拓扑条件注意力是模型性能的关键驱动因素。

### 3. 文本关节语义：跨骨架的语义锚点

不同骨架的关节命名往往共享语义——例如，“left hand”在人类、猴子、鸟类骨架上均指代前肢末端。AnyTop 利用这一观察，通过 **T5 编码器**将关节名称编码为文本嵌入，并添加到对应关节的特征中。

这一设计在潜空间中建立了跨骨架的语义对应。定性分析（Fig. 4, Fig. 5）显示：
- **空间对应**：不同骨架间语义相近的关节（如脊柱、四肢末端）在 DIFT 特征空间中呈现高度对齐；
- **时间对应**：不同角色执行类似动作时（如攻击、静止），对应帧的特征呈现一致的时序模式。

消融实验（Table 4）揭示了关节名称嵌入的双重作用：移除后虽然 Coverage 略微提升至 82.3，但 Local Diversity 骤降至 0.218，Inter Diversity 降至 0.276。这表明**文本先验对维持运动多样性至关重要**——它防止模型将所有骨架的运动模式过度压缩为少数几种原型。

### 4. 训练策略创新：平衡采样与骨骼增强

为应对 Truebones Zoo 数据集中骨架类型的严重不平衡（如四足动物样本远多于昆虫），AnyTop 采用**平衡采样器**，按骨架类型逆频次采样，使每个样本的采样概率为 $1/(n_i \cdot k)$，其中 $n_i$ 为骨架类型 $i$ 的样本数，$k$ 为骨架类型总数。这防止了多数骨架主导训练。

此外，AnyTop 引入了**骨骼级数据增强**：
- 随机移除 10%–30% 的关节；
- 在任意边的中点插入新关节。

这些增强迫使模型学习关节间的鲁棒关系，而非记忆特定骨架的固定模式，是未见骨架泛化能力的重要支撑。需注意，增强时更新距离矩阵 $D_S$ 的复杂度为 $O(J^2)$，这限制了模型向极多关节角色（如百足虫）的扩展——这是论文明确指出的局限性之一。

### 创新总结

| 维度    | 基线做法   | AnyTop 创新   | 证据强度     |
| ----- | ------ | ----------- | -------- |
| 关节编码  | 整帧向量拼接 | 逐关节独立token  | 强（架构基础）  |
| 注意力机制 | 标准自注意力 | 注入图距离与关系偏置  | 强（消融验证）  |
| 语义条件  | 无      | T5关节名称嵌入    | 强（消融验证）  |
| 训练策略  | 均匀采样   | 平衡采样 + 骨骼增强 | 较强（实验支撑） |

这些创新共同构成了 AnyTop 的核心能力：在单一扩散模型中学习多样骨架的运动分布，并通过拓扑条件与文本语义实现跨骨架的知识迁移。

AnyTop 是一个基于去噪扩散概率模型（DDPM）的生成框架，其核心设计目标是**以单一模型为任意骨架结构的角色生成运动**。模型仅需骨架的拓扑结构描述与关节名称作为条件输入，无需针对不同角色重新训练或手工适配。

### 输入表示

框架接收两类输入：**噪声运动**与**骨架条件**。

- **噪声运动** $X_t \in \mathbb{R}^{N \times J \times D}$：一个三维张量，其中 $N$ 为最大帧数，$J$ 为最大关节数，$D=13$ 为每关节特征维度。每个关节（根关节除外）包含根相对位置 $p_j \in \mathbb{R}^3$、6D 旋转 $r_j \in \mathbb{R}^6$、线速度 $v_j \in \mathbb{R}^3$ 和足部接触标签 $fc_j \in \mathbb{R}^1$。
- **骨架条件** $S = \{P_S, R_S, D_S, N_S\}$：包含 rest-pose $P_S$（各关节的静止位姿）、关节关系矩阵 $R_S$（编码父子、兄弟等结构关系）、图拓扑距离矩阵 $D_S$（任意关节对之间的最短路径距离），以及关节名称集合 $N_S$。

### 流水线架构

AnyTop 的架构由三个核心模块级联组成，形成一条清晰的数据处理流水线：

1. **Enrichment Block（增强模块）**：将骨架条件注入噪声运动表示。具体而言，该模块将 rest-pose $P_S$ 编码后作为额外的时间 token 拼接到噪声运动序列中，同时通过 T5 文本编码器将每个关节的名称 $N_S$ 转化为语义嵌入，逐关节加到对应特征上。这一步骤使运动表示携带了骨架的空间结构信息与关节语义先验。

2. **Skeletal Temporal Transformer（骨骼-时序 Transformer 堆叠）**：由 $L$ 层堆叠的 Transformer 层组成，每层依次执行两类注意力操作：
   - **Skeletal Attention（骨骼注意力）**：沿关节轴计算自注意力，捕捉同一帧内所有关节之间的交互。关键在于，注意力图中显式融入了可学习的拓扑偏置——距离偏置 $a_{ij}^{\mathcal{D}}$ 与关系偏置 $a_{ij}^{\mathcal{R}}$，使模型能够感知骨架的图结构而非将所有关节平等对待。
   - **Temporal Attention（时序注意力）**：沿时间轴在窗口长度 $W=31$ 内计算自注意力，使每个关节独立关注其运动的时间演化模式。

3. **Output Projection（输出投影）**：将 Transformer 的最终输出投影回原始运动特征维度 $D$，得到预测的干净运动 $\hat{X}_0$。

### 关键设计选择

与现有方法相比，AnyTop 在架构层面做出了两项关键改变：

- **逐关节独立编码**：传统方法（如 MDM）将整帧所有关节特征拼接为单一向量，而 AnyTop 将每个关节作为独立 token 处理，每帧产生 $J$ 个 token。这种设计赋予了模型空间组合能力——不同骨架的关节可以灵活对应，而非受限于固定的特征拼接顺序。
- **拓扑条件注意力**：标准自注意力对所有关节对一视同仁，而 AnyTop 通过将图距离与关系嵌入作为注意力偏置，使关节在信息聚合时优先关注拓扑邻近或结构相关的关节。最终的注意力 logit 计算为：
  $$a_{ij} = \frac{q_i \cdot k_j + a_{ij}^{\mathcal{D}} + a_{ij}^{\mathcal{R}}}{\sqrt{F}}$$
  其中 $a_{ij}^{\mathcal{D}}$ 和 $a_{ij}^{\mathcal{R}}$ 分别由可学习的距离嵌入和关系嵌入与 query、key 向量交互产生。

### 训练策略

训练采用 **平衡采样器**：给定 $k$ 种骨架类型，第 $i$ 种类型有 $n_i$ 个样本，则该类型每个实例的采样概率为 $1/(n_i \cdot k)$。这有效防止了数据集中占多数的骨架类型主导训练。此外，模型在训练时引入**骨骼级数据增强**，随机移除 10%–30% 的关节或在任意边的中点插入新关节，以提升对未见骨架的泛化能力。

模型预测干净运动 $\hat{X}_0$ 而非噪声 $\epsilon_t$，主损失为简单扩散损失 $\mathcal{L}_{simple} = E_{t \sim [1,T]} \| \text{AnyTop}(X_t, t, S) - X_0 \|_2^2$，并辅以测地线旋转损失 $\mathcal{L}_{rot}$ 来更准确地度量旋转误差。

![[assets/figures/papers/paper_list_l27_AnyTop_Character_Animation_Diffusion_with_Any_Topology/figures/003_Figure_2.jpg]]
*Figure 2: Overview. The input to AnyTop is a noised motion*

AnyTop 是一个基于去噪扩散概率模型（DDPM）的生成框架，其核心架构由四个关键模块串联构成，并通过拓扑条件注意力机制实现多骨架统一学习。

### 管线模块

**Enrichment Block（增强块）** 负责将骨架先验注入噪声运动表示。该模块执行两项操作：（1）将 rest-pose 嵌入 $P_S$ 作为额外的时间 token 拼接到噪声运动序列中；（2）通过 T5 编码器将关节名称 $N_S$ 转化为文本嵌入，逐关节叠加到对应关节特征上。这一设计使模型在去噪过程中显式感知关节语义和骨架空间结构。

**Skeletal Attention（骨骼注意力）** 沿关节轴执行自注意力，捕捉同一帧内所有关节之间的交互。与标准自注意力不同，该模块在注意力图中融入可学习的拓扑偏置——距离偏置 $a_{ij}^{\mathcal{D}}$ 和关系偏置 $a_{ij}^{\mathcal{R}}$——使关节在关注全局的同时优先关注拓扑邻近的关节。

**Temporal Attention（时间注意力）** 沿时间轴执行自注意力，在每个关节上独立建模其运动轨迹的时间演化，窗口长度 $W=31$。

**Output Projection（输出投影）** 将 Transformer 堆栈的输出投影回原始运动特征维度 $D=13$，重建干净运动 $\hat{X}_0$。

### 拓扑条件注意力机制

骨骼注意力是 AnyTop 打通多骨架共享学习的关键。给定骨架 $S$，其拓扑信息以两种图属性编码：

- **图距离矩阵** $\mathcal{D}_S \in \mathbb{R}^{J \times J}$：关节对之间的最短路径边数。
- **关节关系矩阵** $\mathcal{R}_S \in \mathbb{R}^{J \times J}$：编码关节对之间的亲属关系（如父子、祖孙、非直系等离散类别）。

这两种属性通过可学习的嵌入表转化为注意力偏置。距离偏置定义为：

$$a_{ij}^{\mathcal{D}} = q_i \cdot E_q^{\mathcal{D}}[\mathcal{D}_{ij}] + k_j \cdot E_k^{\mathcal{D}}[\mathcal{D}_{ij}]$$

关系偏置定义为：

$$a_{ij}^{\mathcal{R}} = q_i \cdot E_q^{\mathcal{R}}[\mathcal{R}_{ij}] + k_j \cdot E_k^{\mathcal{R}}[\mathcal{R}_{ij}]$$

其中 $q_i$ 为关节 $i$ 的 query 向量，$k_j$ 为关节 $j$ 的 key 向量，$E_q^{\mathcal{D}}[\cdot]$ 和 $E_k^{\mathcal{D}}[\cdot]$ 分别将距离值映射为 query 侧和 key 侧的偏置向量。最终骨骼注意力 logit 为三项之和：

$$a_{ij} = \frac{q_i \cdot k_j + a_{ij}^{\mathcal{D}} + a_{ij}^{\mathcal{R}}}{\sqrt{F}}$$

这种设计使注意力分布同时受内容相似度和骨架拓扑结构共同调控——拓扑邻近且关系紧密的关节获得更高的注意力权重，而远距离关节的交互则被抑制。

### 训练目标

AnyTop 采用 $X_0$-prediction 范式，直接预测干净运动而非噪声。主损失为简单扩散损失：

$$\mathcal{L}_{simple} = E_{t \sim [1,T]} \| AnyTop(X_t, t, S) - X_0 \|_2^2$$

为更准确地度量旋转误差，引入基于旋转矩阵测地线距离的辅助损失：

$$\mathcal{L}_{rot} = \sum_{n=1}^N \sum_{j=1}^J \arccos \frac{Tr(GS(r_{n,j})(GS(\hat{r}_{n,j})^T)-1}{2}$$

其中 $r_{n,j}$ 和 $\hat{r}_{n,j}$ 分别为真实和预测的 6D 旋转表示，$GS(\cdot)$ 为 Gram-Schmidt 正交化过程将其转换为旋转矩阵。总体损失为两者加权和：

$$\mathcal{L} = \mathcal{L}_{simple} + \lambda_{rot} \mathcal{L}_{rot}$$

### 训练策略

为缓解数据集中不同骨架类型的样本量严重不均衡问题，AnyTop 采用**平衡采样器**：对于 $k$ 种骨架类型，类型 $i$ 中每个样本的采样概率设为 $1/(n_i \cdot k)$，其中 $n_i$ 为该类型的样本数。这确保模型在每轮训练中均匀接触各骨架类型，防止多数骨架主导梯度更新。

同时引入**骨骼级数据增强**：训练时随机移除 10%–30% 的关节，或在任意边的中点插入新关节。这一增强迫使模型学习鲁棒的关节表示，提升对未见骨架的泛化能力。需注意，增强后需更新距离矩阵 $\mathcal{D}_S$，其计算复杂度为 $O(J^2)$，这是当前方法在极多关节角色上扩展的瓶颈之一。

![[assets/figures/papers/paper_list_l27_AnyTop_Character_Animation_Diffusion_with_Any_Topology/figures/005_Figure_4.jpg]]
*Figure 4: Spatial Correspondence. Monkey (top left) depicts the reference skeleton, while the fox, scorpion, and bird depict different target skeletons. Target skeleton joints are color-coded to match their corresponding joints in the reference. For better visualization, we color the bones to match their adjacent joints. Note the correspondence in limbs, spine, and tail*

## 实验与关键发现

### 核心瓶颈与评估逻辑

现有运动生成方法难以处理多种骨架拓扑，尤其是非同胚骨架（non‑homeomorphic skeletons），且缺乏涵盖多样拓扑的标注数据集。AnyTop 的核心评估逻辑围绕三个层次展开：**整体生成质量**（覆盖度与多样性的权衡）、**拓扑条件的关键作用**（消融实验）、以及**对未见骨架的泛化能力**（分布外测试）。评估指标沿用 MDM 体系：Coverage（生成分布对真实分布的覆盖度）、Inter Diversity（生成样本间的多样性）、Intra Diversity Difference（生成与真实样本内部多样性的差异），三者共同刻画分布级保真度。

### 主实验结果

Table 3 报告了 AnyTop 与两个改编基线在 Truebones Zoo 多骨架数据集上的整体对比。基线包括 **MDM\***（Tevet et al., 2023）和 **SinMDM\***，均被适配至统一的多骨架训练框架以确保公平比较。

![[assets/figures/papers/paper_list_l27_AnyTop_Character_Animation_Diffusion_with_Any_Topology/figures/015_Table_3.jpg]]
*Table 3: Comparison with baselines. Our model clearly outperforms the baselines. Bold and underline denote best and second best, respectively. ∗ indicates the work was adapted to align with the terms of our experiment*

AnyTop 在所有指标上均显著优于基线。Coverage 达到 80.5（MDM\*: 78.3，SinMDM\*: 76.1），Inter Diversity 为 0.312（MDM\*: 0.296，SinMDM\*: 0.283），Intra Diversity Difference 低至 0.118（MDM\*: 0.134，SinMDM\*: 0.142）。这一结果验证了**逐关节独立编码配合拓扑偏置骨骼注意力**的设计能有效打通多骨架共享学习的关键环节——模型不再将整帧关节拼接为单一向量，而是为每个关节生成独立 token，使注意力机制可在不同骨架间灵活组合运动模式。

按运动类别细分（Table 7），AnyTop 在四足类（Quadrupeds）上 Coverage 达 89.2 ± 0.9（MDM\*: 83.3 ± 2.3，提升 +5.9），双足类（Bipeds）上达 93.5 ± 0.5（MDM\*: 87.9 ± 1.3，提升 +5.6），飞行类（Flying）上达 72.6 ± 1.8（MDM\*: 63.7 ± 3.T，提升约 +8.9）。飞行类的绝对指标较低，反映出该子集骨架拓扑差异更大、运动模式更复杂，但 AnyTop 的相对优势反而更突出，说明其拓扑感知机制在高度异构场景下收益最大。

![[assets/figures/papers/paper_list_l27_AnyTop_Character_Animation_Diffusion_with_Any_Topology/figures/018_Table_7.jpg]]
*Table 7: Comparison on Data Subsets. Quantitative results of AnyTop trained on different data subsets, compared to the baselines trained under equivalent settings. ∗ indicates the work has been adjusted to our experimental terms and † indicates that a specific skeleton (Scorpion) has been removed from the SinMDM evaluation set, as SinMDM fails to converge on this skeleton. This exclusion ensures that its impact does not skew the overall score*

### 消融实验：拓扑条件的关键性

Table 4 的消融实验系统拆解了 AnyTop 各组件的贡献，核心发现如下：

![[assets/figures/papers/paper_list_l27_AnyTop_Character_Animation_Diffusion_with_Any_Topology/figures/014_Table_4.jpg]]
*Table 4: Ablation. Removing architectural choices leads to a degradation in AnyTop’s performance*

**移除图属性嵌入（距离偏置 a^D 与关系偏置 a^R）** 导致 Coverage 从 80.5 降至 76.8（‑3.7），Inter Diversity 从 0.312 降至 0.303，Intra Diversity Difference 从 0.118 升至 0.127（恶化）。所有指标全面退化，证实了拓扑条件注意力是模型性能的核心支柱。距离偏置使关节优先关注拓扑邻近关节，关系偏置编码关节间的语义连接类型（如父子链接、同链关节等），二者共同将骨架结构信息注入注意力图，使同一模型能适应不同骨架的交互模式。

**移除 rest‑pose 令牌** 导致 Coverage 降至 77.2（‑3.3），Inter Diversity 降至 0.292。Rest‑pose 编码了关节偏移和骨骼长度的空间信息，作为额外时间 token 拼接到噪声运动序列中，为模型提供了骨架几何的全局参照。缺失该令牌后，模型对骨骼形态的感知能力显著削弱。

**移除关节名称嵌入** 表现出一种有趣的权衡：Coverage 略微提升至 82.3（+1.8），但 Local Diversity 骤降至 0.218，Inter Diversity 降至 0.276。这表明文本先验（通过 T5 编码关节名称）对维持运动多样性至关重要——没有语义锚定，模型倾向于生成更“安全”但更单一的运动模式，牺牲了生成样本的丰富度。关节名称嵌入在潜空间中建立了跨骨架的语义对应，使不同骨架的相似关节（如不同动物的“左前腿”）能共享运动先验。

**移除骨骼级数据增强**（随机移除 10%–30% 关节、在任意边中点插入新关节）同样导致性能下降，验证了该增强策略对提升模型鲁棒性和泛化能力的贡献。

### 未见骨架泛化

Table 2 报告了 AnyTop 在未见骨架上的零样本推理性能，并按骨架与训练分布的偏离程度（Wasserstein 距离）分层评估。随着 OOD 程度增大，Coverage 逐步但可控地下降：Crab（低 OOD）从 99.45（Seen）降至 88.69（Unseen），Centipede（中 OOD）从 83.55 降至 43.90，Cobra（高 OOD）从 79.34 骤降至 16.47。Intra Diversity Difference 同步恶化，Cobra 从 0.20 升至 0.46。

![[assets/figures/papers/paper_list_l27_AnyTop_Character_Animation_Diffusion_with_Any_Topology/figures/010_Table_2.jpg]]
*Table 2: Unseen-skeleton generalization vs. OOD degree. Performance on unseen skeletons gradually drops as they deviate from data distribution*

这一趋势揭示了 AnyTop 的泛化边界：模型具备分布外泛化能力，但当目标骨架拓扑与训练分布差异过大时，生成质量显著衰减。Fig. 8 的定性对比直观展示了这一差异——AnyTop 为未见骨架（cat、komodo dragon）生成的运动自然流畅，而 MDM 基线则产生僵硬抖动的结果。

### 失败模式与局限

1. **数据集伪影**：Truebones Zoo 数据集仍存在脚滑动、多余骨骼连接等伪影，影响生成运动的物理真实感。模型会学习并复现这些数据缺陷。
2. **计算扩展瓶颈**：骨骼数据增强时更新距离矩阵 D_S 的复杂度为 O(J²)，限制了对极多关节角色（如百足虫类）的扩展。当关节数 J 很大时，增强步骤的计算代价显著上升。
3. **OOD 退化**：如 Table 2 所示，高度 OOD 骨架（如 Cobra）的 Coverage 骤降至 16.47，表明模型对拓扑差异极大的骨架尚不能可靠泛化。
4. **潜空间左右混淆**：空间对应分析（Fig. 4）揭示潜空间特征存在左右肢体混淆，左/右肢体在语义对齐时易被交换，这是逐关节编码缺乏绝对空间参照的固有局限。

### 方法谱系与知识库定位

AnyTop 在骨架运动生成领域的方法谱系中占据独特位置。Table 5 将现有方法按支持的骨架变异层级分类：Single‑skeleton 方法（如 **MDM** (Tevet et al., 2023)、**MoMask** (Guo et al., 2024)）仅处理单一固定骨架；Isomorphic 方法（如 **Skeleton‑aware networks** (Aberman et al., 2020)）支持同构骨架间的运动重定向；Homeomorphic 方法可处理拓扑相同但骨骼长度不同的骨架；而 AnyTop 是首个支持 **Non‑homeomorphic**（非同胚）骨架的扩散模型，即能处理关节数量和连接关系完全不同的骨架拓扑。

这一突破得益于三个关键设计决策：(1) 将拓扑信息（关节关系 R_S 与图距离 D_S）作为可学习偏置整合到 Transformer 骨骼注意力中，而非依赖固定骨架模板；(2) 引入文本关节描述实现跨骨架语义对齐，使不同拓扑的相似功能关节在潜空间中形成对应；(3) 平衡采样器与骨骼级数据增强策略，缓解多骨架数据不平衡问题并提升拓扑鲁棒性。

## 定位与知识库关联

### 一、与基线方法的关系

AnyTop 的核心贡献在于将单骨架运动扩散模型的能力边界从“同胚骨架”扩展至“任意非同胚骨架”，其方法演进可从以下基线对比中清晰定位。

**MDM* 基线**（Tevet et al., 2023）是 AnyTop 最直接的参照系。原始 MDM 为单骨架设计，将整帧所有关节特征拼接为单一向量进行编码。AnyTop 将其改编为多骨架训练版本（MDM*），作为统一对比基准。两者的本质差异在于：MDM* 将不同骨架的运动强行映射到同一表示空间，缺乏对拓扑差异的结构性处理；而 AnyTop 以逐关节独立编码取代整帧向量编码，使每个关节成为独立 token，从而在架构层面天然兼容任意关节数量的骨架。这一“整帧 token → 逐关节 token”的编码方式转变，是 AnyTop 能够处理非同胚骨架的根本前提。

**SinMDM* 基线**（原文未注明具体引用）原为每骨架独立训练多个扩散模型的方法。AnyTop 将其改编为统一训练版本以进行公平比较。SinMDM* 的核心局限在于其生成过程依赖单一参考运动进行引导，导致无法实现跨关节的空间组合——如 Fig. 6 所示，当输入“啄食”和“行走”两种运动时，SinMDM* 无法将上半身啄食动作与下半身行走动作组合，而 AnyTop 凭借逐关节编码成功实现了这种骨架内空间合成。

### 二、方法谱系中的定位

AnyTop 处于“基于扩散的运动生成”与“图结构条件生成”两条技术路线的交叉点：

- **扩散模型谱系**：AnyTop 继承 DDPM（Ho et al., 2020）框架，采用预测干净运动 $X_0$ 而非噪声 $\epsilon_t$ 的策略（与 MDM 一致），并引入测地线旋转损失 $\mathcal{L}_{rot}$ 作为辅助监督，以更准确地度量关节旋转误差。

- **图学习谱系**：AnyTop 将骨骼注意力设计为图偏置增强的自注意力机制。具体而言，注意力得分 $a_{ij} = \frac{q_i \cdot k_j + a_{ij}^{\mathcal{D}} + a_{ij}^{\mathcal{R}}}{\sqrt{F}}$ 中，$a_{ij}^{\mathcal{D}}$ 和 $a_{ij}^{\mathcal{R}}$ 分别编码了关节间的拓扑距离 $\mathcal{D}_{ij}$ 和关系类型 $\mathcal{R}_{ij}$，使模型在全局注意力的基础上优先关注拓扑邻近的关节。这种“全局注意力 + 可学习图偏置”的设计，使 AnyTop 区别于传统的图神经网络（GNN）方法，后者通常严格限制消息传递范围。

- **语义条件生成谱系**：AnyTop 引入 T5 编码的关节名称作为文本先验，在潜空间中建立跨骨架的语义对应。这一设计使模型能够利用语言模型的先验知识，在不同骨架的语义等价关节（如“left hand”与“wing”）之间建立联系，从而实现跨骨架的泛化。

### 三、适用边界

AnyTop 的适用边界由以下因素界定：

1. **骨架可变性层级**：根据 Table 1 的定义，AnyTop 能够处理从单一骨架（Single）到非同胚骨架（Non-homeomorphic）的全谱系变化，包括边长度变化（Isomorphic）、运动链复杂度变化（Homeomorphic）以及拓扑结构根本不同（Non-homeomorphic）的情况。

2. **数据需求**：AnyTop 的训练依赖于 Truebones Zoo 数据集，该数据集涵盖数十种非同胚骨架的运动数据。模型对骨架类型的覆盖度直接影响其泛化能力——未见骨架的生成质量随其与训练分布的距离（以 Wasserstein 距离度量）增大而逐步下降。

3. **计算约束**：骨骼数据增强中更新距离矩阵 $\mathcal{D}_S$ 的复杂度为 $O(J^2)$，限制了模型对极多关节角色（如百足虫类）的扩展性。

### 四、局限与开放问题

**已知局限**（来自论文自身分析）：

- 训练数据集中存在脚滑动、多余骨骼连接等伪影，影响生成运动的物理真实感。
- 未见骨架泛化能力随分布外（OOD）程度显著下降——Table 2 显示，Cobra 骨架的 Coverage 从 seen 的 79.34 骤降至 unseen 的 16.47。
- 潜空间特征存在左右混淆现象，空间对应中左/右肢体语义特征易被交换。
- 数据增强中 $O(J^2)$ 的拓扑条件更新代价限制了高关节数角色的扩展。

**开放问题**：

1. **运动编辑与迁移**：能否利用 DIFT 特征实现可控的运动编辑、风格迁移或细粒度动作识别？这需要进一步探索扩散模型中间层特征的可操作性。

2. **语义级运动重定向**：通过修改关节文本描述（如将“left hand”替换为“wing”）是否足以实现语义级运动重定向？这涉及文本先验在潜空间中的引导强度问题。

3. **多角色交互与文本驱动**：当前模型仅处理单角色运动生成，扩展到骨架重定向、多角色交互以及文本/音乐驱动的生成是自然的发展方向。

4. **计算效率优化**：如何降低数据增强中拓扑条件更新的计算代价？可能的方案包括近似更新策略或惰性计算机制，但具体效果需要进一步验证。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/AnyTop_Character_Animation_Diffusion_with_Any_Topology.pdf]]
