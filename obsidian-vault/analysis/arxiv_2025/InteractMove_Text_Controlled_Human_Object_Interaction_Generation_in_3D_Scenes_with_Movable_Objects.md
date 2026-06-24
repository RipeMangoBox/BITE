---
title: "InteractMove: Text-Controlled Human-Object Interaction Generation in 3D Scenes with Movable Objects"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_Scenes_with_Movable_Objects.pdf
aliases:
- AGCAIGA
- InteractMove
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过引入细粒度的手-物关节交互可能性（hand-object joint affordance）作为条件引导，并结合局部场景体素化建模与碰撞感知损失，直接控制生成的交互是否物理合理且与文本描述一致。
primary_logic: 利用手-物关节 affordance 学习来捕捉不同手部关节与物体表面随时间的接触可能性，从而为运动扩散模型提供丰富、适应物体形状和交互策略的引导信号；同时通过训练时接触和穿透损失及测试时穿透约束，确保运动序列在三维场景中不发生碰撞。
claims:
- 移除 grounding 模块后，Goal Distance 显著下降，表明 grounding 对于定位交互物体至关重要。
- 取消手-物关节 affordance 学习后，Physical Realism 大幅降低，验证了细粒度 affordance 的核心作用。
- 测试时穿透约束（L_ttp）最大程度减少了交叉伪影，将 Non-collision Score 提升至 98.36。
- 在 TRUMANS 数据集上，本方法在 Physical Realism、Non-collision 和 Multi-modality 上均优于基线方法，验证了 affordance 引导运动生成的有效性。
---

# InteractMove: Text-Controlled Human-Object Interaction Generation in 3D Scenes with Movable Objects

> [!tip] 核心洞察
> 利用手-物关节 affordance 学习来捕捉不同手部关节与物体表面随时间的接触可能性，从而为运动扩散模型提供丰富、适应物体形状和交互策略的引导信号；同时通过训练时接触和穿透损失及测试时穿透约束，确保运动序列在三维场景中不发生碰撞。

| 字段 | 内容 |
|------|------|
| 中文题名 | InteractMove：文本控制的三维场景可移动物体人-物交互生成 |
| 英文题名 | InteractMove: Text-Controlled Human-Object Interaction Generation in 3D Scenes with Movable Objects |
| 会议/期刊 | arXiv 2025 |
| Links | [Code](https://github.com/Cxhcmhhh/InteractMove) · [arXiv](https://arxiv.org/abs/2404.00562) · [paper](https://doi.org/10.1145/3746027.3754910) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Affordance-Guided Collision-Aware Interaction Generation (AGCA) |
| Dataset | InteractMove Dataset, TRUMANS Dataset |

> [!tip] 效果简介
> - InteractMove Dataset 上，Goal Distance (↓) 0.791；Multi-modality (↑) 1.58；Physical Realism (↑) 0.813。
> - TRUMANS Dataset (movable subset) 上，Physical Realism 0.754 vs 0.707 (TRUMANS) (+0.047)；Non-collision Score 99.03 vs 98.73 (TRUMANS) (+0.30)；Multi-modality 1.33 vs 1.29 (TRUMANS) (+0.04)。

## 概述

**问题瓶颈**：现有的人-场景交互数据集通常仅包含静态、不可移动的物体，且交互类别有限；收集具有可移动物体的大规模真实数据集成本高、难度大。这导致模型难以在复杂三维场景中根据自然语言指令生成与可移动物体的物理合理交互。

**核心洞察**：利用手-物关节交互可能性（hand-object joint affordance）学习来捕捉不同手部关节与物体表面随时间的接触概率，从而为运动扩散模型提供丰富、适应物体形状和交互策略的引导信号；同时通过训练时接触和穿透损失及测试时穿透约束，确保运动序列在三维场景中不发生碰撞。

**方法定位**：本文提出 **Affordance-Guided Collision-Aware Interaction Generation (AGCA)** 框架，属于“条件运动扩散 + 显式 affordance 引导 + 碰撞感知约束”的技术路线。与 **TRUMANS**（Jiang et al., CVPR 2024）等最新动态人物-场景交互基线相比，AGCA 的关键差异在于：(1) 引入预训练的 3D 视觉语言 grounding 模型（ZSVG3D）根据文本显式定位目标物体，而非隐式学习；(2) 生成细粒度手-物关节 affordance 图，替代粗糙的物体表面热力图或接触图；(3) 构建包含接触损失 $L_{cont}$、穿透损失 $L_{pene}$ 和测试时穿透约束 $L_{ttp}$ 的碰撞感知损失体系，而非无显式碰撞避免机制。

**主要结果**：在自建的 InteractMove 数据集上，AGCA 在 Goal Distance、Multi-modality、Physical Realism 和 Non-collision Score 四项指标上均取得最优结果，其中 Non-collision Score 达到 98.36。在 TRUMANS 数据集的可移动物体子集上，Physical Realism 从 0.707 提升至 0.754，Non-collision Score 从 98.73 提升至 99.03。消融实验表明，移除 3D 物体定位模块导致 Goal Distance 急剧下降，移除 hand-object joint affordance 模块使 Physical Realism 大幅降低，验证了各模块的核心作用。

## 背景与动机

三维场景中的人-物交互（Human-Object Interaction, HOI）生成是计算机视觉与图形学中的核心问题，其目标是根据自然语言指令合成人与场景中物体进行物理合理交互的运动序列。这一能力在具身智能、虚拟现实和数字人动画等领域具有广泛的应用前景。然而，现有方法在该任务上存在两个根本性瓶颈。

**数据层面的结构性缺失。** 当前主流的人-场景交互（Human-Scene Interaction, HSI）数据集——如 TRUMANS（Jiang et al., CVPR 2024）——虽然提供了动态的人物-场景交互序列，但存在两个关键局限：其一，场景中的物体通常被设定为静态、不可移动的，无法支持抓取、搬运、操控等涉及物体位移的交互类型；其二，交互类别有限且缺乏自然语言注释，难以支撑文本驱动的多样化交互生成。收集具有可移动物体的大规模真实数据成本高昂、标注难度大，这一数据缺口直接制约了模型在复杂三维场景中根据自然语言指令生成物理合理交互的能力。

**方法层面的引导信号缺失。** 现有运动生成方法在处理人-物交互时，通常仅依赖粗糙的物体表面热力图或二值接触图作为引导信号，缺乏对“手部不同关节与物体不同部位随时间变化的接触可能性”的细粒度建模。这种粗糙的引导使得模型难以捕捉抓取姿态的多样性、适应不同物体形状，也无法有效区分“接触”与“穿透”的空间关系。同时，现有方法普遍缺乏显式的碰撞避免机制，导致生成的交互序列在三维场景中频繁发生人体与物体或场景几何的穿透伪影。

**本文的核心洞察在于：** 通过引入细粒度的手-物关节交互可能性（hand-object joint affordance）作为条件引导，并结合局部场景体素化建模与碰撞感知损失，可以直接控制生成的交互是否物理合理且与文本描述一致。具体而言，利用手-物关节 affordance 学习来捕捉不同手部关节与物体表面随时间的接触概率分布，为运动扩散模型提供丰富、适应物体形状和交互策略的引导信号；同时，在训练阶段引入接触损失和穿透损失，在推理阶段施加测试时穿透约束，确保运动序列在三维场景中不发生碰撞。

基于上述洞察，本文提出了 **Affordance-Guided Collision-Aware Interaction Generation（AGCA）** 框架，并构建了大规模合成数据集 **InteractMove**——包含 618 个室内三维场景、71 种可移动物体类别、30.5k 条交互序列，每条序列均配有自由文本注释，为文本控制的可移动物体交互生成提供了数据基础。

## 核心创新

InteractMove 的核心创新在于提出了一套 **Affordance-Guided Collision-Aware Interaction Generation（AGCA）** 框架，首次实现了在复杂三维场景中根据自然语言指令生成与可移动物体的物理合理交互。相较于现有方法，AGCA 在三个关键维度上引入了根本性的改变。

### 1. 从隐式学习到显式三维物体定位（3D Object Grounding）

现有的人物-场景交互生成方法通常隐式地学习交互目标，缺乏对文本中指定物体的显式定位能力。AGCA 首次引入预训练的 3D 视觉语言 grounding 模型（**ZSVG3D**）作为前置模块，根据输入文本指令从场景点云中显式定位目标物体。这一改变解决了文本描述与三维场景物体之间的语义对齐问题，为后续的 affordance 引导和运动生成提供了明确的交互目标。消融实验表明，移除该模块后 Goal Distance 指标显著恶化，模型无法准确定位交互物体和交互区域，验证了显式定位的关键作用。

### 2. 从粗糙接触图到细粒度手-物关节 Affordance 学习（Hand-Object Joint Affordance）

现有方法通常仅使用粗糙的物体表面热力图或二值接触图作为交互引导信号，忽略了不同手部关节与物体表面之间随时间变化的细粒度接触模式。AGCA 提出了 **手-物关节交互可能性（hand-object joint affordance）** 学习模块，以物体网格为输入，预测不同手部关节与物体表面在各时间帧上发生交互的概率分布。该模块的核心机制是将手-物距离图通过高斯核归一化，生成适应物体形状和交互策略的丰富引导信号，从而直接控制生成交互的物理合理性和文本一致性。消融实验证实，移除该模块后 Physical Realism 大幅降低，验证了细粒度 affordance 对交互真实性的核心作用。

### 3. 从无碰撞感知到训练-推理联合碰撞约束（Collision-Aware Loss + Test-Time Constraint）

现有方法缺乏显式的碰撞避免机制，生成的交互序列常出现人体与场景或物体的穿透伪影。AGCA 在训练和推理两个阶段引入了互补的碰撞处理策略：

- **训练阶段**：设计了由接触损失 $L_{cont}$ 和穿透损失 $L_{pene}$ 组成的碰撞感知损失函数。$L_{cont}$ 鼓励手部关节与目标物体表面保持接触，$L_{pene}$ 惩罚人体顶点对物体表面的穿透。总损失为 $\mathcal{L}_{total} = \mathcal{L}_{diff} + \lambda_1 \mathcal{L}_{cont} + \lambda_2 \mathcal{L}_{pene}$。

- **推理阶段**：引入测试时穿透约束 $L_{ttp}$，在去噪过程中恢复人体和物体点云，计算穿透顶点对集合 $\mathcal{P}$ 的 L2 距离之和，并沿负梯度方向移动以消除穿透。同时采用局部场景体素化建模，将交互区域编码为空间占据特征，评估空间可达性。

消融实验表明，$L_{ttp}$ 约束对减少交叉伪影贡献最大，将 Non-collision Score 提升至 98.36；同时所有碰撞约束都略微降低了 Multi-modality，这是安全性要求与行为多样性之间的必要权衡。移除局部场景建模后，预测运动经常与场景碰撞，证明了场景约束对空间一致性的关键作用。

### 创新总结

上述三个 changed slots 构成了一个从“定位交互目标 → 引导交互方式 → 约束交互物理合理性”的完整因果链条。AGCA 通过显式 grounding 解决“与谁交互”，通过细粒度 affordance 解决“如何交互”，通过碰撞感知损失和测试时约束解决“在何处安全交互”，从而在文本控制的复杂场景可移动物体交互生成任务上取得突破性进展。

## 整体框架

InteractMove 提出了 **Affordance-Guided Collision-Aware Interaction Generation (AGCA)** 框架，旨在根据自然语言指令，在包含可移动物体的三维场景中生成物理合理的人-物交互运动序列。整体流水线由三个核心阶段串联构成，形成从语义理解到运动生成的端到端链路。

### 阶段一：3D 物体定位

给定一条文本指令（如 “拿起桌上的碗喝水”）和场景点云，系统首先调用预训练的 3D 视觉 grounding 模型 **ZSVG3D** 来定位文本中描述的目标交互物体。该模块输出目标物体的点云区域，为后续的 affordance 学习和运动生成提供精确的空间锚点。消融实验表明，移除该模块会导致 **Goal Distance 指标显著恶化**，验证了显式定位对于复杂场景中准确找到交互对象的必要性。

### 阶段二：手-物关节 Affordance 生成

在获取目标物体点云后，**Hand-Object Affordance Diffusion Module** 以物体点云和文本指令为条件，通过扩散模型生成 **手-物关节交互可能性图（hand-object joint affordance）**。该 affordance 图刻画了不同手部关节与物体表面各点之间随时间变化的接触概率分布，其计算方式为：对每一帧，计算物体点云中每个点与人体各关节的距离，再通过高斯核归一化得到接触似然。这一细粒度的 affordance 信号能够捕捉不同交互策略（如抓握、托举、按压）下手与物体的接触模式差异，为下游运动生成提供丰富的条件引导。消融实验证实，移除该模块会使 **Physical Realism 大幅下降**，凸显了细粒度 affordance 对交互真实性的核心作用。

### 阶段三：碰撞感知运动生成

**Collision-Aware Motion Diffusion Module** 负责合成最终的人体运动和物体轨迹。该模块接收三个关键输入：

1. **局部场景特征**：以目标物体为中心，将周围三维场景体素化为占用网格，通过 Vision Transformer (ViT) 编码为局部场景特征，用于评估空间可达性。移除该模块会导致预测运动频繁与场景碰撞。
2. **手-物 Affordance 图**：来自阶段二的 affordance 信号作为条件注入扩散模型，引导手部关节向高接触概率区域移动。
3. **碰撞感知损失**：训练时引入接触损失 $L_{cont}$ 和穿透损失 $L_{pene}$，分别鼓励手部关节与物体表面保持接触、惩罚人体顶点与物体/场景的穿透。推理时进一步引入 **测试时穿透约束 $L_{ttp}$**，在去噪过程中对穿透顶点对沿负梯度方向移动，将 **Non-collision Score 提升至 98.36**。

训练总损失为扩散重建损失与碰撞感知损失的加权组合：

$$\mathcal{L}_{total} = \mathcal{L}_{diff} + \lambda_1 \mathcal{L}_{cont} + \lambda_2 \mathcal{L}_{pene}$$

其中 $\mathcal{L}_{diff} = \mathbb{E}_{A_0, t} \| A_0 - \hat{A}_0 \|_2^2$ 为扩散模型的均方误差重建损失，$\hat{A}_0 = G_\theta(A_t, c)$ 为网络从噪声输入 $A_t$ 和条件 $c$ 预测的干净信号。

### 数据流与模块关系

整个 AGCA 框架的数据流可概括为：**文本 + 场景点云 → 目标物体区域 → 手-物 affordance 图 → 人体运动 + 物体轨迹**。三个模块之间呈串行依赖关系——grounding 为 affordance 提供物体范围，affordance 为运动生成提供接触引导，而局部场景建模和碰撞感知损失则贯穿运动生成过程，确保输出序列在三维空间中不发生穿透。

### 补充图表

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/006_Figure_4.jpg]]
*Figure 4: Overview of the proposed framework. (a) Given a text instruction, we first locate the interactive object via a pre-trained grounding model. Then, conditioned on the object point cloud and textual instruction, we generate hand-object affordances. Finally, a collision-aware motion generation module synthesizes human motion and object trajectory, incorporating local scene geometry and learned affordances. (b) Hand-object affordance diffusion module. (c) Collision-Aware motion diffusion module*

## 核心模块与公式推导

### 4.1 框架总览

InteractMove 提出的 **Affordance-Guided Collision-Aware Interaction Generation (AGCA)** 框架由三个核心阶段构成（Figure 4）：

1. **3D 物体定位（3D Object Grounding）**：根据文本指令从场景点云中显式定位目标交互物体。
2. **手-物关节 Affordance 生成（Hand-Object Joint Affordance Learning）**：以物体点云和文本为条件，通过扩散模型生成手部关节与物体表面之间的细粒度接触可能性图。
3. **碰撞感知运动生成（Collision-Aware Motion Generation）**：结合局部场景体素化特征、affordance 引导信号和碰撞感知损失，通过运动扩散模型生成最终的人体运动与物体轨迹。

---

### 4.2 运动扩散模型基础

AGCA 的运动生成基于去噪扩散概率模型（DDPM）。将人体动作序列和物体轨迹联合表示为动作信号 $A_0$，前向扩散过程逐步向数据添加高斯噪声：

$$q(A_t | A_{t-1}) = \mathcal{N}(A_t; \sqrt{1 - \beta_t} A_{t-1}, \beta_t I)$$

其中 $\beta_t$ 为噪声调度参数。通过重参数化技巧，可直接从干净信号 $A_0$ 采样任意时刻 $t$ 的噪声版本：

$$A_t = \sqrt{\bar{\alpha}_t} A_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$$

其中 $\bar{\alpha}_t = \prod_{s=1}^t (1 - \beta_s)$，$\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声。

反向过程中，神经网络 $G_\theta$ 根据噪声输入 $A_t$ 和条件 $c$ 预测干净信号：

$$\hat{A}_0 = G_\theta(A_t, c)$$

扩散模型的训练目标为最小化真实信号与预测信号之间的均方误差：

$$\mathcal{L}_{diff} = \mathbb{E}_{A_0, t} \| A_0 - \hat{A}_0 \|_2^2$$

---

### 4.3 3D 物体定位（3D Object Grounding）

该模块采用预训练的 3D 视觉语言 grounding 模型 **ZSVG3D**，根据输入文本指令从场景点云中显式定位目标交互物体。这一显式定位是整个流水线的关键前提——消融实验表明，移除该模块后 Goal Distance 指标显著恶化，模型无法准确定位目标物体和交互区域。

**因果作用**：定位结果为后续的 affordance 生成和局部场景建模提供了空间锚点，决定了交互发生的精确位置。

---

### 4.4 手-物关节 Affordance 学习

这是 AGCA 的核心创新模块。其关键洞察在于：不同手部关节与物体表面在不同时间步具有差异化的接触可能性，这种细粒度的“关节-表面”对应关系为运动生成提供了丰富的几何与语义引导信号。

**Affordance 定义**：对于每一帧，计算物体表面每个点与每个人体手部关节之间的距离，得到距离图，然后通过高斯核归一化为接触可能性图：

$$C_{ijn} = \exp\left(-\frac{1}{2} \cdot \frac{d_{ijn}}{\sigma^2}\right)$$

其中 $d_{ijn}$ 为第 $n$ 帧中物体点 $i$ 与手部关节 $j$ 之间的距离，$\sigma$ 为控制接触范围的高斯带宽参数。

该模块以物体网格和文本指令为输入，通过一个独立的扩散模型生成手-物关节交互可能性图，为后续的运动扩散模型提供条件引导。消融实验证实，移除该模块后 Physical Realism 大幅降低，验证了细粒度 affordance 对交互真实性的核心作用。

---

### 4.5 碰撞感知运动生成

#### 局部场景建模

为评估空间可达性，AGCA 将目标物体周围的局部三维区域体素化为占用网格，并通过 Vision Transformer (ViT) 编码为局部场景特征。消融实验表明，移除局部场景建模后预测运动经常与场景碰撞，证明场景约束对空间一致性至关重要。

#### 碰撞感知损失

训练阶段引入两类物理约束损失（Figure 5）：

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/007_Figure_5.jpg]]
*Figure 5: Our Collision-Aware Loss*

**接触损失（Contact Loss）**：鼓励手部关节 $\tilde{j}$ 与目标物体表面点 $\hat{p}_{obj}$ 之间保持接触：

$$\mathcal{L}_{cont} = \| d(\tilde{j}, \hat{p}_{obj}) \|^2$$

**穿透损失（Penetration Loss）**：惩罚人体顶点 $\tilde{v}$ 与物体表面点 $\hat{p}_{obj}'$ 之间的穿透：

$$\mathcal{L}_{pene} = \| d(\tilde{v}, \hat{p}_{obj}') \|^2$$

#### 测试时穿透约束

在推理阶段，AGCA 引入测试时穿透约束 $\mathcal{L}_{ttp}$ 以进一步消除交叉伪影。首先根据法线方向筛选穿透顶点对：

$$\mathcal{P} = \{ (i, j) \mid -\mathbf{n}_j^T \cdot (\mathbf{V}_{gen}^i - \mathbf{V}_{scene}^j) > 0 \}$$

其中 $\mathbf{V}_{gen}^i$ 为生成的人体顶点，$\mathbf{V}_{scene}^j$ 为场景几何顶点，$\mathbf{n}_j$ 为场景表面法线。条件 $-\mathbf{n}_j^T \cdot (\mathbf{V}_{gen}^i - \mathbf{V}_{scene}^j) > 0$ 确保仅筛选人体顶点位于场景表面内侧（即发生穿透）的顶点对。

然后对所有穿透顶点对的 L2 距离求和，在去噪过程中沿负梯度方向移动以消除穿透：

$$\mathcal{L}_{ttp} = \sum_{(i,j) \in \mathcal{P}} \| \mathbf{V}^i - \mathbf{V}^j \|_2$$

#### 总训练损失

完整的训练目标为扩散重建损失与物理约束损失的加权组合：

$$\mathcal{L}_{total} = \mathcal{L}_{diff} + \lambda_1 \mathcal{L}_{cont} + \lambda_2 \mathcal{L}_{pene}$$

其中 $\lambda_1$ 和 $\lambda_2$ 为平衡各项贡献的超参数。

**消融结论**：同时加入 $\mathcal{L}_{cont}$、$\mathcal{L}_{pene}$ 训练损失和 $\mathcal{L}_{ttp}$ 推理约束，使 Non-collision Score 达到最高的 98.36。所有约束均略微降低了 Multi-modality，论文将此视为安全性要求与行为多样性之间的必要权衡。

### 补充图表

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/002_Figure_2.jpg]]
*Figure 2: Method of our motion alignment*

## 实验与分析

### 数据集构建与统计

由于现有的人-场景交互（HSI）数据集普遍缺乏可移动物体和多样化的交互类型，本文首先构建了 **InteractMove** 数据集。该数据集通过将捕获的人-物交互（HOI）序列与 ScanNet 三维场景扫描进行对齐，合成了大规模的可移动物体交互数据。如 Table 1 所示，InteractMove 包含 **618 个室内三维场景**、**71 种可移动物体类别**、**30.5k 个交互序列**，并提供自由形式的文本注释。与现有 HSI 数据集相比，其在场景数量、交互帧规模、可移动物体种类和语言注释方面均具有显著优势。

数据构建的关键在于运动对齐（Motion Alignment）的质量。Table 7 的消融实验表明，采用基于扩散模型的运动修复策略（Refined Motion）在 FID 等指标上远优于直接强制对齐（Forced Alignment），其运动质量接近原始 HOI 运动。这验证了运动修复对于保持交互语义一致性的必要性。

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/013_Table_7.jpg]]
*Table 7: Ablation of our dataset construction. We evaluate the quality of the original HOI motion and our aligned motion (aligned with the 3D scene)*

### 主实验结果

**InteractMove 数据集评估**（Table 2）：本文提出的 AGCA 框架在四个核心指标上均取得了最优结果。其中，**Goal Distance 达到 0.791**，表明生成的人体能够准确接近目标交互物体；**Multi-modality 为 1.58**，反映了模型对同一文本指令能生成多样化运动的能力；**Physical Realism 为 0.813**，说明交互动作的物理合理性较高；**Non-collision Score 达到 98.36**，证明碰撞避免机制的有效性。

**TRUMANS 数据集迁移评估**（Table 3）：为验证方法的泛化性，在 TRUMANS（Jiang et al., CVPR 2024）的可移动物体交互子集上进行了对比。AGCA 在 Physical Realism（0.754 vs. 0.707）、Non-collision Score（99.03 vs. 98.73）和 Multi-modality（1.33 vs. 1.29）上均优于 TRUMANS 基线。这表明即便在动作类型有限的真实数据集上，affordance 引导的运动生成策略仍然有效。

### 消融实验

**核心组件消融**（Table 4）：

- **移除 3D 物体定位模块（Grounding）**：Goal Distance 显著恶化。模型难以根据文本指令定位目标物体和交互区域，验证了预训练 ZSVG3D 定位器的关键作用。
- **移除手-物关节 Affordance 模块**：Physical Realism 大幅降低。细粒度的关节级接触概率图对于生成真实抓取和操控动作不可或缺。
- **移除局部场景建模（Local Scene Modeling）**：预测的运动经常与场景发生碰撞，证明了体素化场景编码对空间一致性的约束作用。

**碰撞感知损失消融**（Table 5）：训练时的接触损失（$\mathcal{L}_{cont}$）和穿透损失（$\mathcal{L}_{pene}$）与推理时的测试时穿透约束（$\mathcal{L}_{ttp}$）协同作用。其中，$\mathcal{L}_{ttp}$ 对消除交叉伪影的贡献最为显著，将 Non-collision Score 推至最高的 98.36。值得注意的是，所有碰撞约束都略微降低了 Multi-modality——这是严格安全性要求与行为多样性之间的必要权衡。

**干扰物影响实验**（Table 6）：当场景中包含多个与目标物体同类的干扰物时，任务难度显著增加，模型性能随之下降。这揭示了在复杂场景中进行精确物体定位和交互生成仍然是一个非平凡挑战。

### 失败模式分析

尽管 AGCA 在整体指标上表现优异，但从消融实验中可以归纳出以下失效边界：

1. **定位依赖性强**：模型对 3D 视觉 Grounding 模块高度依赖。当文本描述模糊或目标物体在点云中特征不明显时，定位失败会级联导致后续交互生成完全偏离目标。
2. **多样性-安全性权衡**：碰撞约束在提升物理合理性的同时，不可避免地压缩了生成运动的多样性空间。在需要高自由度交互（如复杂工具使用）的场景中，这种权衡可能导致生成的动作趋于保守。
3. **多干扰物场景退化**：同类干扰物数量增加时，模型性能持续下降，表明当前的 affordance 引导机制在处理细粒度物体区分方面仍有不足。
4. **数据集构建偏差**：运动对齐过程中的修复策略虽优于强制对齐，但仍可能与原始 HOI 运动的精确交互语义存在偏差，这一潜在偏差对下游生成的影响尚需进一步量化。

### 补充图表

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluations on our dataset*

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/009_Table_3.jpg]]
*Table 3: Quantitative evaluations on the TRUMANS dataset. For fairness, we conduct the comparison only on samples involving interactions with movable objects*

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/010_Table_4.jpg]]
*Table 4: Ablations of each component in our method*

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/011_Table_5.jpg]]
*Table 5: Ablations of the collision-aware loss*

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/012_Table_6.jpg]]
*Table 6: Experiments on the number of instances of the same category as the target object*

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/014_Figure_6.jpg]]
*Figure 6: Visualization. The prompt is The person drinks the bowl on the desk near the sofa*

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/005_Figure_3.jpg]]
*Figure 3: Visualizations of our dataset*

![[assets/figures/papers/paper_list_l1686_InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_S/figures/003_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 与现有基线的继承与突破

InteractMove 的核心贡献建立在人-场景交互（HSI）生成领域的两条关键脉络之上，但针对性地突破了它们在“可移动物体交互”和“物理合理性”上的瓶颈。

**继承自 TRUMANS 的动态交互范式。** 本工作的直接基线是 **TRUMANS**（Jiang et al., CVPR 2024），后者是首个将可移动物体纳入动态人物-场景交互建模的数据集与方法。TRUMANS 突破了此前 HSI 数据集（如 PROX、HUMANISE）仅包含静态场景元素的限制，但其存在两个关键不足：（1）缺乏自然语言注释，无法支持文本驱动的交互生成；（2）交互类别有限，难以覆盖多样化的物体操控行为。InteractMove 继承了 TRUMANS 对可移动物体的关注，但通过构建大规模文本标注数据集和引入文本条件扩散模型，将任务范式从“给定动作类别的运动生成”推进到“开放文本控制的人-物交互生成”。

**对静态场景交互方法的超越。** 此前的主流 HSI 方法（如 HUMANISE、COUCH、LAMA）专注于人体与静态场景的交互生成，其核心机制是学习场景 affordance 热力图来引导人体姿态放置。这类方法无法处理物体随交互而发生位移的场景——例如“拿起桌上的碗”要求同时生成人手运动与碗的轨迹。InteractMove 将 affordance 概念从“静态场景表面”拓展到“动态手-物关节接触”，使模型能够理解不同手部关节与物体表面随时间变化的接触可能性，从而支持物体移动的交互生成。

**对碰撞处理机制的升级。** 在运动生成中处理人-物-场景碰撞是一个长期挑战。早期方法要么完全忽略碰撞（依赖数据驱动隐式学习），要么仅在推理阶段使用简单的后处理优化。InteractMove 提出了“训练-推理联合碰撞感知”策略：训练时引入接触损失 $L_{cont}$ 和穿透损失 $L_{pene}$ 作为显式监督信号，推理时进一步施加测试时穿透约束 $L_{ttp}$，沿负梯度方向移动穿透顶点以消除交叉伪影。这种双阶段碰撞处理机制在 Non-collision Score 上达到了 98.36，显著优于无碰撞约束的基线。

### 2. 方法谱系中的定位

从技术路线看，InteractMove 属于 **条件运动扩散模型 + affordance 引导 + 物理约束优化** 的交叉范式。

**扩散模型在运动生成中的应用。** 本工作采用去噪扩散概率模型（DDPM）作为运动生成骨干，这与 MDM、MotionDiffuse、GMD 等方法同属扩散生成路线。其关键创新在于条件设计：将文本嵌入、手-物关节 affordance 图、局部场景体素特征三类异构条件融合注入去噪网络，实现了语言理解、交互语义、空间约束的统一引导。

**Affordance 学习的深化。** 传统 affordance 方法（如 POSA、HUMANISE）仅建模人体/手部与场景表面的静态接触概率。InteractMove 的 hand-object joint affordance 模块将 affordance 从“静态接触图”升级为“时序关节级接触概率”，能够区分不同手部关节（如指尖、掌心、手腕）在不同时间步与物体表面不同区域的接触模式。这种细粒度 affordance 为抓取、搬运、放置等复杂操控提供了关键的交互先验。

**3D 视觉语言 grounding 的引入。** 本方法显式集成了预训练的 3D 视觉语言 grounding 模型（ZSVG3D），根据文本指令从场景点云中定位目标物体。这与端到端隐式学习定位的范式形成对比——显式 grounding 模块确保了目标物体的准确定位，消融实验中移除该模块后 Goal Distance 显著恶化，验证了其对任务完成度的关键作用。

### 3. 适用边界与局限性

**数据集覆盖范围。** InteractMove 数据集包含 71 类可移动物体和 618 个室内场景，但交互类型主要集中在日常物品的抓取、搬运、放置等基础操控。对于复杂工具使用（如使用剪刀、螺丝刀）、双手协同精细操作、或同时操控多个物体的场景，方法扩展性尚待验证。

**Grounding 模块的依赖性。** 当前框架依赖独立的预训练 grounding 模型进行物体定位，这带来了两个潜在问题：（1）grounding 错误会直接传播到后续运动生成，缺乏纠错机制；（2）无法实现端到端的联合优化，限制了语言理解与运动生成的深度耦合。

**场景表示的粒度。** 局部场景建模采用体素化 + ViT 编码的方式，体素分辨率决定了空间可达性评估的精度。对于需要精细避障的复杂场景（如狭窄空间中的交互），体素化可能丢失关键几何细节。

**文本条件的泛化能力。** 方法在训练集覆盖的交互类型上表现良好，但对于训练中未出现的开放词汇交互描述（如“小心地从抽屉里取出易碎的玻璃杯”），泛化能力尚未经过系统评估。

### 4. 开放问题与未来方向

1. **端到端联合训练。** 能否将 3D visual grounding 与运动生成统一为端到端框架，使语言理解、物体定位、affordance 预测和运动生成在同一个优化目标下协同学习？

2. **多物体交互扩展。** 当前方法针对单物体交互设计。如何扩展 hand-object joint affordance 机制以支持同时操控多个物体（如一手拿碗一手拿勺）或物体间交互（如将物品放入抽屉）？

3. **精细工具使用。** 工具使用涉及更复杂的手-物接触模式（如手指在剪刀手柄上的特定放置）。现有的关节级 affordance 是否足够表达这类约束，还是需要引入更精细的手部姿态先验？

4. **交互语义保持。** 数据集构建中的运动对齐过程（高度调整 + 扩散修复）是否改变了原始 HOI 数据的精确交互语义？例如，“端起碗喝汤”的对齐运动是否仍保持“喝”的动作特征？这一问题需要更细致的语义保持评估。

5. **真实场景部署。** 方法依赖完整的场景点云和物体网格作为输入。在真实应用中，如何从 RGB-D 传感器或单目视频中获取足够质量的场景与物体表示，是一个从仿真到现实的关键工程挑战。

6. **安全性与多样性的平衡。** 消融实验表明，碰撞约束（$L_{cont}$、$L_{pene}$、$L_{ttp}$）在提升物理安全性的同时略微降低了 Multi-modality。如何设计更智能的约束机制，在保证无碰撞的前提下最大化运动多样性，是一个值得深入的方向。

## 原文 PDF

![[paperPDFs/arxiv_2025/InteractMove_Text_Controlled_Human_Object_Interaction_Generation_in_3D_Scenes_with_Movable_Objects.pdf]]