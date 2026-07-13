---
title: Learning to Generate Human-Human-Object Interactions from Textual Descriptions
type: paper
paper_level: A
venue: NEURIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_Descriptions.pdf
project_link: https://tlb-miss.github.io/hhoi/
code_link: https://github.com/rtqichen/torchdiffeq
aliases:
- SBHGDDGS
- LGHHOIFTD
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将 HHOI 分解为条件独立的 HOI 与 HHI 分数分布，并在推理时通过不一致损失与碰撞损失进行引导采样，从而在不联合训练的情况下统一两个分布。
primary_logic: 利用两个独立训练的基于分数的扩散模型分别捕捉人-物关系（HOI）和人-人关系（HHI），再通过采样过程中的物理一致性与空间约束实现隐含的联合生成，可以避免昂贵的三元组数据收集。
claims:
- 在二人生成中，Body Pose FD 从 0.6834 降至 0.1755，Distance FD 从 0.4180 降至 0.0689。
- 在 5 人多人生成中，成功率达 100%，远超基线的 0%。
- 用户研究中 60.9% 认为本文方法更真实且忠于文本描述。
- 消融显示移除碰撞损失或不一致性损失会严重降低生成质量。
---

# Learning to Generate Human-Human-Object Interactions from Textual Descriptions

> [!tip] 核心洞察
> 利用两个独立训练的基于分数的扩散模型分别捕捉人-物关系（HOI）和人-人关系（HHI），再通过采样过程中的物理一致性与空间约束实现隐含的联合生成，可以避免昂贵的三元组数据收集。

| 字段 | 内容 |
|------|------|
| 中文题名 | 学习从文本描述生成人-人-物体交互 |
| 英文题名 | Learning to Generate Human-Human-Object Interactions from Textual Descriptions |
| 会议/期刊 | NEURIPS 2025 |
| Links | [Project](https://tlb-miss.github.io/hhoi/) · [Code](https://github.com/rtqichen/torchdiffeq) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Score-based HHOI Generation with Decomposed Diffusion and Guided Sampling |
| Dataset | dyadic HHOI generation, multi-human generation, multi-human generation (Table 2) – 5 humans, physical plausibility (Table 3) – 2 humans |

> [!tip] 效果简介
> - dyadic HHOI generation (Table 1) 上，Body Pose FD ↓ 0.1755 vs 0.6834 (Depth Opt.) (-0.5079)；Distance FD ↓ 0.0689 vs 0.4180 (Depth Opt.) (-0.3491)；CLIP Score ↑ 0.2695 vs 0.2647 (Depth Opt.) (+0.0048)。
> - multi-human generation (Table 2) 上，CLIP Score ↑ 0.2695 vs 0.2647 (Depth Opt.) (+0.0048)。
> - multi-human generation (Table 2) – 5 humans 上，Success Rate (%) 100.0 vs 0.0 (both baselines) (+100.0)。

## 概要

### 问题与瓶颈

生成多人围绕共享物体进行交互的三维场景（Human‑Human‑Object Interaction, HHOI）是具身 AI 与场景理解中的关键挑战。现有方法要么仅关注单人‑物体交互（HOI），要么独立建模多人交互（HHI），缺乏一个能协同建模多人‑物体‑空间关系的统一框架，导致生成的场景在**空间一致性、物理合理性与语义忠实度**上严重不足。其根本瓶颈在于：**缺乏能协同建模多人围绕共享物体交互的数据集与生成方法**，现有工作无法在多人共享同一物体的条件下保持场景级一致性。

### 核心方法定位

本文提出一种**基于分数的分解式扩散生成框架**，将复杂的 HHOI 联合分布分解为两个条件独立的子分布——人‑物交互（HOI）与人‑人交互（HHI）——分别用两个独立的基于分数的扩散模型进行建模。在推理阶段，通过引入**不一致损失**与**碰撞损失**作为引导项，将两个子分布统一到同一个概率流 ODE 采样过程中，从而**在不进行联合训练、不依赖昂贵三元组标注的条件下，实现多人‑物体交互场景的隐含联合生成**。该方法的核心洞察在于：利用两个独立训练的扩散模型分别捕捉 HOI 与 HHI 关系，再通过采样过程中的物理一致性与空间约束实现场景级统一，从而规避了大规模 HHOI 数据收集的难题。

### 主要结果

在二人生成任务上，本文方法将 Body Pose Fréchet Distance（FD）从基线的 0.6834 降至 **0.1755**，Distance FD 从 0.4180 降至 **0.0689**（Table 1）。在更具挑战性的 5 人多人生成中，成功率高达 **100%**，而基线方法完全失败（Table 2）。物理合理性方面，人‑物穿透率从 60.71 降至 **5.49**，接触距离从 0.115 m 降至 **0.029 m**（Table 3）。用户研究中 **60.9%** 的参与者认为本文生成的结果更真实且更忠于文本描述（Table 1）。消融实验进一步证实，移除碰撞损失或不一致性损失会严重破坏生成质量（Fig. 12）。

### 方法谱系与知识库定位

本工作处于**三维人体‑场景交互生成**与**基于分数的扩散模型**的交叉点。与仅处理单人 HOI 的 GenZI 以及依赖深度优化的多视图修复方法相比，本文首次将 HOI 与 HHI 显式分解为两个可独立训练的扩散模型，并通过引导采样实现联合生成。该方法在表征层面将 126 维 SMPL‑X 姿态压缩为 10 维学习型潜变量，在约束层面引入基于 24 胶囊代理的可微碰撞损失，为后续多人‑多物交互生成、文本驱动的三维场景编辑等任务提供了可扩展的技术骨架。



### 问题定义：从单人交互到多人场景的范式跃迁

生成逼真的人类交互行为是计算机视觉与图形学的核心挑战之一。现有工作主要聚焦于两类独立问题：**单人-物体交互（Human-Object Interaction, HOI）** 和**多人交互（Human-Human Interaction, HHI）**。然而，真实世界中的交互场景往往同时涉及多个个体围绕共享物体的协同行为——即**人-人-物体交互（Human-Human-Object Interaction, HHOI）**，例如“三人围坐在长椅上聊天”或“两人共同搬运一张桌子”。这类场景要求生成系统同时满足三重约束：每个人与物体的物理接触合理性、人与人之间的空间关系一致性，以及整体场景对文本描述的语义忠实度。

### 现有方法的瓶颈：联合建模的缺失

当前方法在 HHOI 生成上存在根本性缺陷，可归纳为两个层面：

**1. 数据层面——三元组数据的稀缺性。** 同时标注多人姿态、物体位姿及其交互关系的数据集极为匮乏。现有数据集要么仅包含单人 HOI 样本，要么仅记录独立的人-人交互，缺乏“多人-共享物体”的三元组标注。直接采集此类数据需要多视角动捕系统与复杂场景编排，成本高昂且难以规模化。

**2. 方法层面——场景级一致性的缺失。** 基线方法（如 **GenZI** 和 **Depth Opt.**）通常将多人 HOI 视为多个独立单人 HOI 的简单拼接，或通过多视角图像修复与深度优化进行后处理对齐。这种“分而治之”的策略无法在生成过程中显式建模人-人之间的空间约束与物理一致性，导致以下典型失败模式：
- **穿透问题**：多人之间或人与物体之间出现严重的几何穿透（Table 3 显示 GenZI 的人-物穿透比高达 60.71×10⁻³，而本文方法仅为 5.49×10⁻³）。
- **空间不一致**：不同人的姿态、位置与物体关系相互矛盾，无法形成连贯的交互场景。
- **可扩展性崩溃**：当人数增至 5 人时，基线方法的成功率骤降至 0%（Table 2），而本文方法保持 100% 成功率。

### 核心动机：解耦-引导的生成范式

本文的核心洞察在于：**HHOI 的联合分布可以通过两个条件独立的分数分布——HOI 分布与 HHI 分布——在推理时经由物理一致性约束实现隐式耦合，从而规避昂贵的三元组数据收集与联合训练。**

具体而言，这一范式包含三个关键设计动机：

1. **数据解耦**：分别收集 HOI 与 HHI 数据远比收集 HHOI 三元组数据容易。本文构建的数据集包含 13,669 个 HOI 样本和 13,650 个 HHI 样本，覆盖 19 个物体类别（Figure 6），通过多视角捕捉系统（Figure 5）与基于预训练图像扩散模型的合成数据管线共同构建。

2. **模型解耦**：训练两个独立的基于分数的扩散模型，分别捕捉人-物关系（HOI）和人-人关系（HHI）的条件分布。每个模型仅需学习其对应子问题的分数函数，降低了建模复杂度。

3. **推理耦合**：在采样过程中引入两类引导损失——**不一致损失（Inconsistency Loss）** 和**碰撞损失（Collision Loss）**——通过梯度项修正 PF ODE 的演化方向，使来自两个独立模型的样本在生成过程中自发形成场景级一致性。这种“采样时引导”的策略避免了联合训练的需求，同时保持了生成的灵活性与物理合理性。

### 文本条件的语义锚定

为实现可控生成，本文方法以**文本描述**作为条件信号。CLIP 文本编码器将自然语言提示映射为条件嵌入，同时作用于 HOI 和 HHI 扩散模型，使得生成的多人交互行为在语义层面与输入文本对齐。例如，给定提示“两人走向自动售货机并使用它”，系统需同时理解“走向”的空间动态、“使用”的物体交互语义，以及“两人”的社会关系暗示。这种文本到 3D 交互的跨模态映射是本文方法实现语义可控 HHOI 生成的关键前提。



## 核心方法与创新机理

本文的核心创新在于将**多人-共享物体交互（HHOI）**这一复杂生成问题，分解为两个条件独立的子问题——**人-物交互（HOI）**与**人-人交互（HHI）**——并通过**引导采样**在推理阶段实现二者的隐含联合。这一设计直接回应了该领域的核心瓶颈：缺乏能协同建模多人围绕共享物体交互的数据集与生成方法，现有工作仅关注单人-物体交互或独立的多人类交互，无法保持场景级一致性。

### 关键机制：分解-扩散-引导

方法体系由三个紧密耦合的环节构成，形成一条从数据分布建模到物理一致采样的完整链路。

**1. 条件独立的双流扩散建模**

方法将 HHOI 显式分解为两个基于分数的扩散模型，分别捕捉不同的条件分布：

- **HOI 扩散模型**：学习以物体网格 $\mathcal{M}$ 和文本描述 $\mathbf{c}$ 为条件的人-物交互分布 $p_{\mathbf{c}}^{\mathcal{M}}$。每个 HOI 样本 $\phi^{\mathrm{HOI}} = (\mathbf{R}_{\mathcal{H}}, \mathbf{t}_{\mathcal{H}}, \mathbf{s}_{\mathcal{H}}, \theta_{\mathcal{H}})$ 包含人体的旋转、平移、缩放以及一个 10 维的姿态潜在编码 $\theta_{\mathcal{H}}$。
- **HHI 扩散模型**：学习以文本描述 $\mathbf{c}$ 为条件的人-人交互分布 $p_{\mathbf{c}}^{\mathcal{H}\mathcal{H}}$。每个 HHI 样本 $\phi^{\mathrm{HHI}} = (\theta_{\mathcal{H}_1}, \mathbf{R}_{\mathcal{H}_2\to\mathcal{H}_1}, \mathbf{t}_{\mathcal{H}_2\to\mathcal{H}_1}, \theta_{\mathcal{H}_2})$ 包含两人的姿态潜在编码及相对旋转与平移。

两个模型分别通过去噪分数匹配（Denoising Score Matching）独立训练，损失函数为：

$$\mathcal{L}_{\mathrm{score}}(\Theta^z) = \mathbb{E}_{t\sim\mathcal{U}(\epsilon,1)}\left[\lambda_t \mathbb{E}_{\phi^z,\phi_t^z}\left[\left\|\Psi_{\Theta^z}(\phi_t^z,t|\mathbf{c},z) - \frac{\phi^z - \phi_t^z}{\sigma(t)^2}\right\|_2^2\right]\right]$$

这一分解策略的核心优势在于**规避了昂贵的三元组（多人-物体）联合数据收集**：HOI 和 HHI 模型可分别利用相对丰富的单人-物体交互数据和双人交互数据进行训练，无需采集特定的多人围绕同一物体的同步交互样本。

**2. 低维姿态潜在空间**

与直接在 126 维 SMPL-X 关节旋转空间建模不同，本文引入一个**姿态编码器-解码器**，将人体姿态映射到 10 维潜在嵌入 $\theta_{\mathcal{H}}$，再通过解码器重建规范姿态网格 $\mathcal{H}^{\mathrm{cano}} = \mathbf{smplx}(\mathbf{dec}(\theta_{\mathcal{H}}))$。这一设计显著降低了扩散模型需要学习的数据维度，使得在有限数据条件下也能有效捕捉姿态分布。

**3. 引导采样：不一致损失与碰撞损失**

推理阶段的关键创新在于，通过**增强概率流 ODE（PF ODE）**将两个独立训练的扩散模型在采样过程中耦合起来。具体而言，在每一步去噪迭代中，ODE 被注入两项梯度引导：

$$\frac{d\phi_t^{z,i}}{dt} = -\sigma(t)\dot{\sigma}(t)\Psi_{\Theta^z}(\phi_t^{z,i}, t|\mathbf{c}^z, z) + \lambda_1\nabla_{\phi_t^{z,i}}\mathcal{L}_{\mathrm{inc}}(\Phi_t) + \lambda_2\nabla_{\phi_t^{z,i}}\mathcal{L}_{\mathrm{col}}(\Phi_t)$$

- **不一致损失 $\mathcal{L}_{\mathrm{inc}}$**：强制从不同 HOI/HHI 样本中推导出的同一人体参数（缩放 $\mathbf{s}$、姿态 $\theta$、旋转 $\mathbf{R}$、平移 $\mathbf{t}$）保持一致。该损失定义为各参数方差的加权和：

$$\mathcal{L}_{\mathrm{inc}}(\Phi_t) = \mathcal{L}_{var,s}(\mathbf{s}) + \mathcal{L}_{var,\theta}(\theta) + \mathcal{L}_{var,R}(\mathbf{R}) + \mathcal{L}_{var,t}(\mathbf{t})$$

- **碰撞损失 $\mathcal{L}_{\mathrm{col}}$**：针对未显式定义 HHI 关系的人对（即非直接交互者），施加无穿透约束。为高效计算，每个 SMPL-X 人体被近似为 24 个胶囊代理，碰撞损失定义为所有胶囊对重叠量的总和：

$$\mathcal{L}_{\mathrm{col}}(\Phi_t) = \sum_{(\mathcal{H}_i,\mathcal{H}_j)\in\Phi_{\mathrm{nap}}} \frac{1}{24^2} \sum_{c_i=1}^{24}\sum_{c_j=1}^{24} \max(0, r_{c_i}^{\mathcal{H}_i} + r_{c_j}^{\mathcal{H}_j} - d_{c_i,c_j}^{\mathcal{H}_i,\mathcal{H}_j})$$

这种“训练时分离、推理时联合”的策略，使得方法无需联合训练即可在采样过程中隐式地统一 HOI 与 HHI 分布，同时保证场景级的物理一致性。

### 相对基线的关键差异（Changed Slots）

相较于现有方法，本文在三个关键维度上实现了根本性转变：

| 维度 | 基线方法 | 本文方法 | 证据锚点 |
|------|----------|----------|----------|
| **多人交互建模** | 独立的单人 HOI 或多视图修补（inpainting），缺乏联合一致性约束 | 分解的 HOI/HHI 分数模型 + 引导采样，通过不一致损失与碰撞损失实现联合 | Sec. 3.1, 3.3 |
| **碰撞处理** | 无显式处理或启发式深度对齐 | 24 胶囊代理的可微碰撞损失，在采样过程中施加无穿透约束 | Sec. 3.3, Eq. (14) |
| **姿态表示** | 原始 126D 关节旋转 | 10D 学习潜在嵌入，通过编码器-解码器映射 | Sec. 3.1 Body Pose Embedding |

消融实验（Figure 12）直接验证了上述创新的必要性：移除碰撞损失会导致非直接交互的人对之间出现穿透；同时移除碰撞损失与不一致损失则彻底破坏 HOI 与 HHI 的整合，导致姿态和空间关系严重不一致。

### 创新边界与局限

尽管方法在多人场景中展现出显著优势（5 人生成成功率达 100%，远超基线的 0%），其创新仍受限于以下因素：

- **数据依赖性**：训练数据限于受控工作室录制的 11 类交互及少量合成数据（3 类），缺乏大规模野外真实场景样本。合成数据的质量依赖于预训练图像扩散模型和 HMR，可能引入 2D 到 3D 的估计噪声。
- **碰撞近似的精度**：24 胶囊代理采用固定半径因子，在极端姿势下近似精度可能下降。
- **可扩展性约束**：方法无法直接利用纯 HOI 或纯 HHI 数据集进行训练，限制了数据规模的可扩展性。如何有效利用这些更丰富的数据源仍是一个待探索的开放问题。



### 问题定义与输入输出

本工作定义了一个新的生成任务：给定场景中的物体网格 $\mathcal{M}$ 和文本描述 $\mathbf{c}$，生成多个人体在三维空间中的姿态与位置，使得人-物交互（HOI）和人-人交互（HHI）在场景层面保持一致性。输出为 $N$ 个人的 SMPL-X 网格参数，包括每个人的全局旋转 $\mathbf{R}_{\mathcal{H}}$、平移 $\mathbf{t}_{\mathcal{H}}$、缩放 $\mathbf{s}_{\mathcal{H}}$ 以及身体姿态潜在编码 $\theta_{\mathcal{H}}$。

### 核心思路：分解-引导-联合

整个框架的核心思路是将复杂的多人-物交互生成问题**分解**为两个条件独立的子问题，然后在采样过程中通过物理约束**引导**两个分布走向一致。具体来说：

1. **分解建模**：将 HHOI 拆解为 HOI（人-物）和 HHI（人-人）两个独立的分数分布，分别用两个基于分数的扩散模型进行训练。
2. **引导联合**：在推理采样时，通过引入不一致损失（Inconsistency Loss）和碰撞损失（Collision Loss）作为梯度引导项，将两个独立分布的采样过程耦合起来，实现隐含的联合生成。

这一设计的关键优势在于**无需收集昂贵的三元组（多人-物）联合标注数据**——HOI 模型和 HHI 模型可以分别在各自的数据上独立训练，仅在推理时通过引导项实现协同。

### Pipeline 模块构成

整个框架由以下核心模块组成（参见 Figure 2 的方法总览）：

![[assets/figures/papers/paper_list_l1799_HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_D/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. (a) The training and inference process of the HOI/HHI part. (b) The advanced HHOI sampling process by introducing inconsistency loss and collision loss*

| 模块 | 功能 | 关键设计 |
|------|------|----------|
| **HOI 扩散模型** | 学习以物体网格和文本为条件的人-物交互分数函数 $\Psi_{\Theta^{\text{HOI}}}$ | 输入包含人体全局位姿、缩放及 10D 姿态潜在编码 |
| **HHI 扩散模型** | 学习以文本为条件的人-人交互分数函数 $\Psi_{\Theta^{\text{HHI}}}$ | 输入包含两人姿态编码及相对旋转与平移 |
| **身体姿态编码器/解码器** | 将 126D SMPL-X 关节旋转映射到 10D 潜在空间并还原 | 实验发现低维潜在空间比原始 126D 表示更利于扩散模型学习 |
| **CLIP 文本编码器** | 将文本描述编码为条件嵌入 | 为 HOI 和 HHI 模型提供语义条件 |
| **引导采样模块** | 在 PF ODE 采样过程中注入不一致损失和碰撞损失的梯度 | 实现 HOI 与 HHI 样本间的隐式联合约束 |

### 数据流与训练-推理分离

**训练阶段**（Figure 2(a)）：
- HOI 扩散模型和 HHI 扩散模型**分别独立训练**，各自使用去噪分数匹配损失 $\mathcal{L}_{\text{score}}$。
- 两个模型采用相同的网络架构但**参数不共享**，因为它们的输入输出维度不同（HOI 处理单人与物体关系，HHI 处理两人相对关系）。
- 训练数据来自多视角采集系统（Figure 5）和基于预训练图像扩散模型的合成数据管线（Figure 6），覆盖真实录制 11 类和合成 3 类交互场景。

![[assets/figures/papers/paper_list_l1799_HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_D/figures/008_Figure_5.jpg]]
*Figure 5: HHOIs Capture System Overview. We capture Human-Human-Object Interactions (HHOIs) with our multiple camera capture system. The object and human poses are tracked with AruCo markers [15] and DWPose [65] respectively*

**推理阶段**（Figure 2(b)）：
1. 根据文本描述 $\mathbf{c}$，确定场景中的 HOI 和 HHI 数量及对应关系。
2. 对每个 HOI 样本 $\phi^{\text{HOI}}$ 和每个 HHI 样本 $\phi^{\text{HHI}}$，分别从各自的扩散模型中并行采样。
3. 在每一步 PF ODE 积分中，计算**不一致损失** $\mathcal{L}_{\text{inc}}$（强制同一人体从不同 HOI/HHI 样本推导出的参数一致）和**碰撞损失** $\mathcal{L}_{\text{col}}$（为未显式定义 HHI 的人对施加无穿透约束），将其梯度作为引导项加入采样过程。
4. 最终从收敛的样本中解码出所有人体的 SMPL-X 参数，重建三维网格。

### 引导采样的关键机制

引导采样是连接两个独立扩散模型的**核心纽带**，其数学形式为增广的 PF ODE：

$$
\frac{d\phi_t^{z,i}}{dt} = -\sigma(t)\dot{\sigma}(t)\Psi_{\Theta^z}(\phi_t^{z,i}, t|\mathbf{c}^z, z) + \lambda_1\nabla_{\phi_t^{z,i}}\mathcal{L}_{\text{inc}}(\Phi_t) + \lambda_2\nabla_{\phi_t^{z,i}}\mathcal{L}_{\text{col}}(\Phi_t)
$$

其中 $z \in \{\text{HOI}, \text{HHI}\}$ 指示样本类型，$\Phi_t$ 为当前时刻所有样本的集合。两个引导项各司其职：

- **不一致损失** $\mathcal{L}_{\text{inc}}$：对同一人体的缩放、姿态、旋转、平移分别计算跨样本方差，强制不同 HOI/HHI 样本对同一人体的描述保持一致。这是实现“分解训练、联合推理”的关键——它使得独立采样的 HOI 和 HHI 样本在共享人体参数上收敛到一致值。
- **碰撞损失** $\mathcal{L}_{\text{col}}$：基于 24 胶囊代理（Figure 8）近似人体几何，计算非直接交互人对之间的胶囊重叠量。这为未通过 HHI 显式关联的人对（如三人场景中坐在长椅两端的人）提供物理合理性约束。

消融实验（Figure 12）证实：移除碰撞损失会导致非直接交互的人对之间出现穿透；同时移除两个损失会彻底破坏 HOI 与 HHI 的整合，导致姿态和空间位置不一致。

### 方法定位

与现有工作的本质区别在于：**GenZI** 等方法通过多视角修复和深度优化处理多人 HOI，但缺乏对人-人关系的显式建模，无法保持场景级一致性；**Depth Opt.** 等方法结合修复、HMR 和深度优化，但仅能处理单人-物交互的扩展，在多人场景中成功率急剧下降（5 人场景成功率为 0%，见 Table 2）。本方法通过分解扩散与引导采样，首次实现了从文本描述到多人-物交互的端到端生成，且无需联合训练数据。



### 3.1 问题分解：HOI 与 HHI 的独立建模

本方法的核心思想是将复杂的多人-物交互（HHOI）联合分布分解为两个条件独立的子分布：**人-物交互（HOI）** 与 **人-人交互（HHI）**。这种分解使得模型可以分别利用 HOI 和 HHI 数据进行独立训练，从而规避了对昂贵三元组联合标注数据的依赖。

**HOI 样本定义**（Sec. 3.1, Eq. (1)）：一个 HOI 样本描述单个人体相对于给定物体网格 $\mathcal{M}$ 的空间配置，其形式为：

$$\phi^{\mathrm{HOI}} \sim p_{\mathbf{c}}^{\mathcal{M}}, \quad \phi^{\mathrm{HOI}} = (\mathbf{R}_{\mathcal{H}}, \mathbf{t}_{\mathcal{H}}, \mathbf{s}_{\mathcal{H}}, \theta_{\mathcal{H}})$$

其中：
- $\mathbf{R}_{\mathcal{H}} \in \mathrm{SO}(3)$：人体全局旋转
- $\mathbf{t}_{\mathcal{H}} \in \mathbb{R}^3$：人体全局平移
- $\mathbf{s}_{\mathcal{H}} \in \mathbb{R}^3$：人体各向异性缩放
- $\theta_{\mathcal{H}} \in \mathbb{R}^{10}$：人体姿态的 10 维潜在嵌入（由编码器从 SMPL-X 的 126 维关节旋转压缩得到）

人体网格通过 SMPL-X 重建：$\mathcal{H} = \mathbf{s}_{\mathcal{H}} \cdot \mathbf{R}_{\mathcal{H}} \mathcal{H}^{\mathrm{cano}} + \mathbf{t}_{\mathcal{H}}$，其中 $\mathcal{H}^{\mathrm{cano}} = \mathbf{smplx}(\mathbf{dec}(\theta_{\mathcal{H}}))$。

**HHI 样本定义**（Sec. 3.1, Eq. (3)）：一个 HHI 样本描述两人之间的相对空间关系：

$$\phi^{\mathrm{HHI}} \sim p_{\mathbf{c}}^{\mathcal{H}\mathcal{H}}, \quad \phi^{\mathrm{HHI}} = (\theta_{\mathcal{H}_1}, \mathbf{R}_{\mathcal{H}_2\to\mathcal{H}_1}, \mathbf{t}_{\mathcal{H}_2\to\mathcal{H}_1}, \theta_{\mathcal{H}_2})$$

其中 $\mathbf{R}_{\mathcal{H}_2\to\mathcal{H}_1}$ 和 $\mathbf{t}_{\mathcal{H}_2\to\mathcal{H}_1}$ 分别表示 $\mathcal{H}_2$ 相对于 $\mathcal{H}_1$ 的旋转与平移。这种相对表示自然地捕捉了“面对面”“并肩”等社会空间线索。

**姿态潜在嵌入**（Sec. 3.1 Body Pose Embedding）：作者发现直接对 126 维关节旋转（21 关节 × 6D 表示）建模效果不佳，因此训练了一个编码器-解码器对，将姿态压缩到 10 维潜在空间 $\theta_{\mathcal{H}}$，使扩散模型在更紧凑、更规整的流形上学习分数函数。

---

### 3.2 基于分数的扩散模型训练

HOI 与 HHI 均采用基于分数的扩散模型（Score-based Diffusion Model）建模。对于模态 $z \in \{\mathrm{HOI}, \mathrm{HHI}\}$，模型学习噪声条件分数函数 $\Psi_{\Theta^z}(\phi_t^z, t | \mathbf{c}, z)$，该函数近似真实数据分布经高斯扰动后的分数：

$$\Psi_{\Theta^z}(\phi_t^z, t | \mathbf{c}, z) \approx \nabla_{\phi_t^z} \log p_{\mathbf{c}}^z(\phi_t^z)$$

其中 $\phi_t^z = \phi^z + \sigma(t) \cdot \epsilon$ 为加噪样本，$\sigma(t)$ 为噪声调度，$\mathbf{c}$ 为 CLIP 编码的文本条件。

**训练目标**为去噪分数匹配损失（Sec. 3.2, Eq. (6)）：

$$\mathcal{L}_{\mathrm{score}}(\Theta^z) = \mathbb{E}_{t\sim\mathcal{U}(\epsilon,1)}\left[\lambda_t \mathbb{E}_{\phi^z,\phi_t^z}\left[\left\|\Psi_{\Theta^z}(\phi_t^z, t|\mathbf{c}, z) - \frac{\phi^z - \phi_t^z}{\sigma(t)^2}\right\|_2^2\right]\right]$$

其中 $\lambda_t$ 为时间步权重。该损失驱动网络学会从任意噪声水平恢复干净样本的方向。

**推理采样**使用概率流 ODE（PF ODE）：

$$\frac{d\phi_t^z}{dt} = -\sigma(t)\dot{\sigma}(t) \Psi_{\Theta^z}(\phi_t^z, t | \mathbf{c}, z)$$

从先验噪声 $\phi_1^z \sim \mathcal{N}(0, \sigma(1)^2\mathbf{I})$ 反向积分至 $t=\epsilon$ 即可获得干净样本。

---

### 3.3 引导采样：不一致损失与碰撞损失

HOI 和 HHI 模型独立训练后，在推理时需要联合生成多个人的空间配置。关键挑战在于：不同 HOI 样本可能为同一人推导出不一致的参数，且未通过 HHI 显式关联的人对可能发生碰撞。为此，作者在 PF ODE 中引入两项引导损失。

**不一致损失** $\mathcal{L}_{\mathrm{inc}}$（Sec. 3.3, Eq. (9)）：对于从不同 HOI/HHI 样本导出的同一人体参数（缩放 $\mathbf{s}$、姿态 $\theta$、旋转 $\mathbf{R}$、平移 $\mathbf{t}$），计算其方差并求和：

$$\mathcal{L}_{\mathrm{inc}}(\Phi_t) = \mathcal{L}_{var,s}(\mathbf{s}) + \mathcal{L}_{var,\theta}(\theta) + \mathcal{L}_{var,R}(\mathbf{R}) + \mathcal{L}_{var,t}(\mathbf{t})$$

该损失强制不同样本对同一人的描述趋于一致，从而实现 HOI 与 HHI 信息的隐式融合。

**碰撞损失** $\mathcal{L}_{\mathrm{col}}$（Sec. 3.3, Eq. (14)）：对于未显式定义 HHI 的“非相邻”人对 $\Phi_{\mathrm{nap}}$，假设“无穿透”约束。为高效计算，将每个人体近似为 24 个胶囊（对应 SMPL-X 的 24 个关节段），碰撞损失定义为所有胶囊对的穿透深度之和：

$$\mathcal{L}_{\mathrm{col}}(\Phi_t) = \sum_{(\mathcal{H}_i,\mathcal{H}_j)\in\Phi_{\mathrm{nap}}} \frac{1}{24^2} \sum_{c_i=1}^{24}\sum_{c_j=1}^{24} \max(0, r_{c_i}^{\mathcal{H}_i} + r_{c_j}^{\mathcal{H}_j} - d_{c_i,c_j}^{\mathcal{H}_i,\mathcal{H}_j})$$

其中 $r$ 为胶囊半径，$d$ 为胶囊中心距。该损失可微，允许梯度反向传播至采样过程。

**引导采样 ODE**（Sec. 3.3, Eq. (15)）将两项损失的梯度注入 PF ODE：

$$\frac{d\phi_t^{z,i}}{dt} = -\sigma(t)\dot{\sigma}(t)\Psi_{\Theta^z}(\phi_t^{z,i}, t|\mathbf{c}^z, z) + \lambda_1\nabla_{\phi_t^{z,i}}\mathcal{L}_{\mathrm{inc}}(\Phi_t) + \lambda_2\nabla_{\phi_t^{z,i}}\mathcal{L}_{\mathrm{col}}(\Phi_t)$$

其中 $\lambda_1, \lambda_2$ 为引导强度超参数。该 ODE 同时对所有 HOI/HHI 样本并行积分，在每一步通过梯度引导修正样本，最终收敛到满足物理一致性与空间合理性的 HHOI 配置。消融实验（Fig. 12）证实：移除碰撞损失会导致非直接交互人对穿透，移除不一致损失则会破坏姿态与空间的一致性。

### 补充图表

![[assets/figures/papers/paper_list_l1799_HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_D/figures/010_Figure_7.jpg]]
*Figure 7: HHOI Diffusion Architecture.HHOI diffusion consists of two disjoint diffusion models: HOI diffusion and HHI diffusion. Although the overal structure of each diffusion model is the same, they are implemented with separate networks due to their different target distributions. Each network learns the score function of the HOI or HHI distribution,respectively*



## 实验与关键发现

### 核心定量结果

本文在二人生成与多人生成两个维度对方法进行了系统评估，核心指标涵盖生成质量、物理合理性与用户偏好。

**二人生成（Table 1）**：与基线方法 **Depth Opt.** 相比，本文方法在身体姿态分布距离（Body Pose FD）上从 0.6834 降至 **0.1755**（降低 0.5079），在空间距离分布距离（Distance FD）上从 0.4180 降至 **0.0689**（降低 0.3491），表明生成的人体姿态与空间布局与真实分布高度吻合。CLIP Score 从 0.2647 小幅提升至 0.2695，说明文本-生成一致性略有改善但幅度有限（置信度 0.9）。用户研究中 **60.9%** 的参与者认为本文方法更真实且更忠于文本描述，而 Depth Opt. 仅获 20.8% 的偏好率，优势显著（+40.1%）。

**多人生成（Table 2）**：在 5 人场景下，本文方法成功率达到 **100.0%**，而两种基线方法（GenZI 与 Depth Opt.）成功率均为 0.0%，表明现有方法完全无法处理多人协同交互的生成任务。CLIP Score 维持 0.2695，与二人生成持平，说明文本相关性在多人扩展中未出现退化。

**物理合理性（Table 3）**：在 2 人场景中，本文方法的人-物穿透比率（Human-Object Penetration Ratio ×1000）仅为 **5.49**，远低于 GenZI 的 60.71（降低 55.22）；接触距离（Contact Distance）为 **0.029 m**，低于 GenZI 的 0.115 m（降低 0.086 m）。这表明通过碰撞损失与不一致损失的联合引导，生成结果在物理接触精度与穿透避免上具有显著优势。

### 消融实验

消融实验（Fig. 12）揭示了引导采样中两个损失函数的关键作用：

![[assets/figures/papers/paper_list_l1799_HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_D/figures/014_Figure_12.jpg]]
*Figure 12: Ablation Study for Guided HHOI Sampling*

- **移除碰撞损失**：非直接交互的人对之间出现明显的身体穿透，验证了 24 胶囊代理的可微碰撞损失在维持多人空间合理性中的必要性。
- **同时移除碰撞损失与不一致损失**：HOI 与 HHI 的整合被破坏，导致人体姿态与空间关系出现严重不一致，生成结果失去场景级协调性。

这一结果直接支撑了本文的核心机制——通过解耦训练后的引导采样来统一两个条件独立分布，而非依赖联合训练。

### 定性对比与失败模式

**定性对比（Fig. 3）**：在 3 至 5 人的复杂 HHOI 场景中，基线方法频繁出现生成失败（10 次试验中无有效输出），而本文方法能够稳定生成保持自然社交线索的多人交互姿态。例如，“三人坐在长椅上”的场景中，本文方法生成的姿态既保持了人与长椅的合理接触，又维持了人与人之间的自然间距与朝向关系。

**失败模式**：分析中未明确报告本文方法的典型失败案例，但结合局限性可推断以下潜在问题：
- 极端姿态下 24 胶囊代理的近似精度可能下降，导致碰撞损失引导失效；
- 训练数据限于受控工作室环境（11 类）与少量合成数据（3 类），对野外开放场景的泛化能力缺乏充分验证；
- 合成数据依赖预训练图像扩散模型与 HMR 的 2D-3D 提升，可能引入估计噪声，影响生成精度。

### 应用验证

本文方法生成的 HHOI 结果可作为运动插值（motion in-betweening）的末端帧约束（Fig. 4）。给定一个朴素的站立姿态作为起始帧，DNO 与 InterGen 能够从本文生成的末端帧出发，插值出自然连贯的运动序列。这一应用验证了生成结果在时序运动合成中的下游可用性。

![[assets/figures/papers/paper_list_l1799_HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_D/figures/007_Figure_4.jpg]]
*Figure 4: Motion in-betweening outputs from DNO and InterGen, given a naive standing pose as the start frame constraint and our HHOI generation output as the end frame constraint*

### 公平性说明

- 用户研究的参与者来源与筛选标准未详细说明，可能引入人口偏差。
- 数据集主要来自受控实验室环境及合成数据，对野外场景的泛化性未补充独立检验。

### 补充图表

![[assets/figures/papers/paper_list_l1799_HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_D/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on text-guided dyadic HHOI generation. Our model shows robust performance compared to baseline models in all the metrics*

![[assets/figures/papers/paper_list_l1799_HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_D/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison of text-guided multi-human generation. Our model consistently outperforms baseline methods across al evaluation metrics, demonstrating robust performance*

![[assets/figures/papers/paper_list_l1799_HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_D/figures/003_Figure_3.jpg]]
*Figure 3: HHOI generation result of dyadic,and multiple humans in action with our model and baselines. In multiple HHOI, number of humans ranges from 3 to 5. Empty result represents cases where generation failed in 10 trials. Our model can generate complex HHOIs with varying number of humans in the scene,while preserving the natural social cues*

![[assets/figures/papers/paper_list_l1799_HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_D/figures/009_Figure_6.jpg]]
*Figure 6: Statistics on Collected Data Samples. Our dataset is constructed by integrating data from CORE4D and our multiview capture system, alongside synthetic samples generated via our data generation pipeline*



## 定位与知识库关联

### 1. 问题定位：从单人-物交互到多人-物协同生成

现有工作主要聚焦于两类独立任务：**单人-物体交互（HOI）生成**与**多人交互（HHI）生成**。前者关注单个人体相对于物体的空间关系与姿态，后者关注两人之间的相对空间配置与社会信号。然而，当场景中存在多人围绕共享物体进行交互时，这两类方法无法保持**场景级一致性**——例如“三人坐在长椅上”，每个人的姿态必须同时满足与椅子的接触关系（HOI）以及与他人的空间协调（HHI），且不能发生穿透。本文的核心瓶颈即在于缺乏能协同建模多人围绕共享物体交互的数据集与生成方法。

### 2. 方法谱系中的位置

本文提出的**基于分数的分解扩散与引导采样框架**位于以下方法线的交汇处：

**（1）基于分数的扩散生成（Score-based Diffusion）**
- 本文直接继承 Song et al. 提出的分数匹配与概率流 ODE 框架，将其应用于 HOI 与 HHI 的条件分布建模。与先前将扩散用于单物体位姿生成的工作（如 [1, 68]）类似，但本文将其扩展到**两个独立分布**的联合采样问题。

**（2）人-物交互生成（HOI Generation）**
- 基线方法 **Depth Opt.** 结合了图像修复（inpainting）、人体网格恢复（HMR）与深度优化，可为多人场景生成 HOI，但缺乏人-人之间的联合一致性约束，导致生成结果在空间配置与物理合理性上表现不佳（Table 1 中 Body Pose FD 高达 0.6834）。
- 本文的改进在于将 HOI 显式建模为条件分布 $p_{\mathbf{c}}^{\mathcal{M}}$，并通过低维潜在嵌入（10D）替代原始 126D 关节旋转表示，提升了分布建模的有效性。

**（3）多人交互生成（HHI Generation）**
- 基线方法 **GenZI** 被扩展用于多人 HOI 比较，但其本质上是基于多视角修复的策略，未对多人之间的物理约束（如碰撞避免）进行显式建模。Table 3 显示 GenZI 的人-物穿透率高达 60.71（×1000），而本文仅为 5.49。
- 本文通过独立的 HHI 扩散模型捕捉两人之间的相对空间关系，并在采样时通过碰撞损失（24 胶囊代理）对所有未显式定义 HHI 的人对施加无穿透约束。

**（4）分解-合成式生成（Decompose-and-Compose Generation）**
- 本文的核心方法论贡献在于**不进行联合训练**，而是将复杂的 HHOI 生成分解为两个条件独立的分数分布，再通过推理时的引导采样实现隐含联合。这一思路与场景图到图像的分解生成、以及组合式扩散模型有精神上的相似，但在 3D 多人-物交互领域是首次应用。

### 3. 与基线方法的量化关系

| 方法 | 核心策略 | 关键局限 | 本文优势（Table 1/2/3） |
|------|----------|----------|--------------------------|
| **Depth Opt.** | 修复 + HMR + 深度优化 | 无多人一致性约束 | Body Pose FD 降低 74.3%（0.6834→0.1755） |
| **GenZI** | 多视角修复扩展 | 无碰撞处理 | 人-物穿透率降低 90.9%（60.71→5.49） |
| 两者 | 无法扩展到 5 人 | 成功率 0% | 5 人成功率 100% |

### 4. 适用边界与局限性

**（1）数据依赖性**
- 训练数据限于受控工作室录制的 11 类交互及少量合成数据（3 类），缺乏大规模户外真实场景中的 HHOI 样本。合成数据的质量依赖于预训练图像扩散模型（如 FLUX）和 HMR 的精度，可能引入 2D 到 3D 的估计噪声。

**（2）物理近似的精度边界**
- 碰撞损失采用固定半径的 24 胶囊代理（Figure 8）。在极端姿势（如深度弯腰、蜷缩）下，胶囊近似精度可能下降，导致假阳性碰撞或漏检。胶囊半径是否可通过学习自适应优化，是待探索的问题。

**（3）无法利用纯 HOI 或纯 HHI 数据**
- 当前框架要求训练数据同时包含 HOI 和 HHI 标注。如何有效利用大规模纯 HOI 数据集（如 BEHAVE、InterCap）或纯 HHI 数据集进一步扩展训练数据，仍是开放问题。

**（4）静态场景假设**
- 本文生成的是单帧静态 HHOI 配置。在多物体或动态变化的场景中，如何保持长时间交互的一致性和物理合理性，需要进一步研究。

### 5. 开放问题与后续工作方向

1. **数据扩展**：能否通过迁移学习或弱监督方式，将纯 HOI/HHI 数据集纳入训练？
2. **动态场景**：框架能否扩展到多人以不同物体交互的更复杂场景，或与运动生成方法（如 DNO、InterGen）深度耦合？
3. **碰撞代理优化**：胶囊半径与数量是否可通过可微分方式学习，以在精度与计算效率之间取得更优平衡？
4. **泛化性验证**：在野外场景（如拥挤的公共交通、体育比赛）中的表现尚未验证，用户研究的参与者来源与筛选标准也未详细说明，可能引入人口偏差。



## 原文 PDF

![[paperPDFs/NEURIPS_2025/HHOI_Learning_to_Generate_Human_Human_Object_Interactions_from_Textual_Descriptions.pdf]]
