---
title: Understanding and Enforcing Weight Disentanglement in Task Arithmetic
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Understanding_and_Enforcing_Weight_Disentanglement_in_Task_Arithmetic.pdf
project_link: null
code_link: "https://github.com/RL-MIND/OrthoReg"
aliases:
- UEWDTA
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 任务特征专业化（TFS）通过使不同任务使用不重叠的内部特征，实现权重解耦。
primary_logic: 强制微调期间权重更新矩阵的内部正交性可以减轻干扰，即使在特征重叠的情况下也能促进解耦。
claims:
- TFS 是权重解耦的充分条件
- WVO 是 TFS 的几何结果
- OrthoReg 即使在特征重叠时也能积极促进解耦
- OrthoReg 实验上在所有基线上一致提升任务添加和否定性能
---

# Understanding and Enforcing Weight Disentanglement in Task Arithmetic

> [!tip] 核心洞察
> 强制微调期间权重更新矩阵的内部正交性可以减轻干扰，即使在特征重叠的情况下也能促进解耦。

| 字段 | 内容 |
|------|------|
| 中文题名 | 理解并强化任务算术中的权重解耦 |
| 英文题名 | Understanding and Enforcing Weight Disentanglement in Task Arithmetic |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.17078) · [Code](https://github.com/RL-MIND/OrthoReg) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | OrthoReg |
| Dataset | 8-task addition |

> [!tip] 效果简介
> - 8-task addition (CLIP ViT-B-32) 上，Abs.Acc. 73.41 (Non-lin. FT+OrthoReg) vs 70.32 (Non-lin. FT) (+3.09)；Norm.Acc. 93.93 (Non-lin. FT+OrthoReg) vs 77.56 (Non-lin. FT) (+16.37)。
> - 8-task addition (CLIP ViT-L-14) 上，Abs.Acc. 90.41 (ATT-FT+OrthoReg) vs 87.81 (ATT-FT) (+2.60)；Abs.Acc. 88.23 (Non-lin. FT+OrthoReg) vs 84.07 (Non-lin. FT) (+4.16)。

## 概述

**核心问题**：任务算术（Task Arithmetic）通过将多个微调后的任务向量 $\tau_t = \theta_t - \theta_0$ 合并到预训练模型 $\theta_0$ 上，实现多任务能力的组合。然而，不同任务向量之间存在**干扰（interference）**，导致合并后的模型在各任务上的性能显著低于单独微调的模型，这是制约任务算术实用性的关键瓶颈。

**核心发现与理论框架**：本文提出并证明了**任务特征专业化（Task-Feature Specialization, TFS）**是连接几何性质（权重向量正交性，Weight Vector Orthogonality）与功能性质（权重解耦，Weight Disentanglement）的共同原因。具体而言，在 NTK 线性化假设下，TFS 是权重解耦的**充分条件**（Theorem 1），并且 TFS 在几何上表现为权重矩阵的块正交性（Corollary 1）。实证表明，预训练 CLIP ViT 模型的权重列向量之间已呈现接近 90° 的角度分布（Figure 2），这为利用正交性促进解耦提供了内在基础。

**方法定位**：基于上述理论，本文提出 **OrthoReg**——一种简单且高效的**正则化方法**。OrthoReg 在微调阶段对权重更新矩阵 $\Delta W$ 施加列向正交约束，迫使 $\Delta W$ 的 Gram 矩阵接近单位矩阵，从而即使在特征重叠的现实场景下也能主动促进任务向量之间的解耦（Theorem 2）。该方法作为即插即用的正则项，可叠加于多种微调策略之上。

**方法谱系与知识库定位**：OrthoReg 属于**模型合并（Model Merging）与任务算术**方向的正则化改进方法。与标准非线性微调（Non-linear Fine-tuning）基线相比，它不改变模型架构或推理过程，仅在训练损失中引入正交约束。相较于在切线空间中进行线性化微调的 **Tangent Task Arithmetic（TTA）**，OrthoReg 避免了昂贵的雅可比计算，计算开销更为适中。与参数高效微调方法如 **LoRA-ATT** 结合时，OrthoReg 同样展现出一致的性能增益。

**主要结果**：在 8 任务添加基准上，OrthoReg 在所有基线上均实现了**一致且显著的性能提升**。以 CLIP ViT-B-32 为例，Non-linear FT + OrthoReg 的绝对准确率（Abs.Acc.）达到 73.41%（+3.09），归一化准确率（Norm.Acc.）达到 93.93%（+16.37）。在 CLIP ViT-L-14 上，ATT-FT + OrthoReg 达到 90.41%（+2.60）。在任务否定（Task Negation）场景下，OrthoReg 同样在保持控制任务准确率阈值的前提下，显著增强了对目标任务的遗忘效果。消融实验表明，注意力相关模块（qkvo–）上的正交正则化贡献了最大增益（ViT-B-16 上 +4.17 Abs.Acc.），而仅在 MLP 层上施加 OrthoReg 在小模型上可能带来轻微的性能下降。

## 背景与动机

### 任务算术与权重解耦

现代深度学习的一个核心范式是：先在大规模数据上预训练基础模型，再针对下游任务进行微调。当需要将多个微调模型的能力合并为一个多任务模型时，**任务算术**（Task Arithmetic）提供了一条轻量路径——只需将各任务微调后参数与预训练参数的差值（即**任务向量**）进行加权求和，便可直接叠加到预训练模型上，无需访问原始训练数据或进行联合重训。

具体地，给定预训练参数 $\theta_0$ 和任务 $t$ 的微调参数 $\theta_t^*$，任务向量定义为：

$$\tau_t = \theta_t^* - \theta_0$$

多任务合并模型则通过缩放求和得到：

$$\theta_{\mathrm{MT}} = \theta_0 + \alpha \sum_{t=1}^{T} \tau_t$$

这一范式在 CLIP 等视觉-语言模型上已展现出实用价值，但其性能仍显著低于各任务单独微调的模型。核心瓶颈在于：**来自不同任务向量的干扰导致合并模型性能下降**。理想情况下，合并模型在任务 $t$ 数据上的行为应仅取决于 $\tau_t$，而不受其他任务向量的影响——这一性质被称为**权重解耦**（Weight Disentanglement）。然而，在实际微调中，不同任务向量之间往往存在高度相关性（如 Figure 5(a) 所示，任务向量对之间的余弦相似度较高），导致合并时产生严重的跨任务干扰。

### 现有方法的局限

为缓解任务干扰，已有工作从多个角度进行了探索：

- **切线任务算术（TTA）** 将微调限制在预训练模型的线性化切线空间中进行，试图通过线性近似来减少非线性交互带来的干扰。但 TTA 引入了昂贵的雅可比计算，训练时间和显存开销显著增加（见 Table 3），且性能提升有限。
- **仅微调注意力模块（Attention-Only Fine-tuning）** 和 **LoRA-ATT** 等参数高效微调方法通过限制可调参数的范围来隐式降低任务向量之间的冲突，但缺乏对解耦的显式建模。
- 这些方法均未从**权重更新的几何结构**层面主动促进解耦，而是依赖隐式正则或线性化近似，效果受限于特征重叠等现实因素。

### 核心动机：从特征专业化到正交正则化

本文的理论出发点是：**任务特征专业化（Task-Feature Specialization, TFS）是权重解耦的充分条件**。TFS 意味着不同任务使用预训练模型中不重叠的内部特征子集。在该条件下，不同任务的权重更新自然落在相互正交的子空间中，从而消除干扰（Theorem 1 和 Corollary 1）。

然而，现实中的微调往往无法满足严格的 TFS——任务之间不可避免地共享部分特征，导致任务向量产生重叠和干扰。这引出了本文的核心问题：**即使特征重叠存在，能否通过主动约束权重更新的几何结构来促进解耦？**

本文的理论贡献之一（Theorem 2）证明：**强制微调期间权重更新矩阵的内部正交性，即使在特征重叠的情况下，也能积极促进任务间的权重解耦**。这构成了 OrthoReg 方法的理论基础——通过在微调损失中引入正交正则项，约束权重更新矩阵 $\Delta W$ 的列向量彼此正交，从而在几何层面抑制跨任务干扰。如 Figure 3 所示，OrthoReg 通过在 Transformer 模块的线性层上施加 $\mathcal{L}_{\mathrm{ortho}}$ 损失，使权重更新呈现正交结构，即使不同任务使用了重叠的特征，也能有效缓解合并时的性能衰减。

## 核心创新

本工作围绕任务算术（Task Arithmetic）中一个被忽视的瓶颈展开：**来自不同任务向量的干扰是导致合并模型性能下降的核心原因**。现有方法（如 TTA）试图通过在线性化切线空间中进行微调来隐式缓解干扰，但代价是昂贵的雅可比计算和 2–3 倍的训练时间开销。本文的关键创新在于从理论上揭示了干扰产生的结构根源，并据此提出了一个轻量且通用的解决方案。

### 从特征重叠到权重解耦的理论桥梁

本文首先形式化了**权重解耦**（Weight Disentanglement）的理想条件：对于任务 $t$ 和 $j$，合并模型在任务 $t$ 数据上的行为应仅取决于 $\tau_t$，即：

$$f(x; \theta_0 + \tau_t + \tau_j) = f(x; \theta_0 + \tau_t), \quad \forall x \in \mathcal{D}_t$$

在 NTK 线性化假设下，该条件等价于**零干扰条件** $\tau_j^\top J(x) = 0$（Lemma 1）。进一步分析表明，干扰的大小可近似为：

$$|\tau_j^\top J(x)| \approx \|\tau_j\|_2 \cdot \|J(x)\|_2 \cdot |\cos \angle(\tau_j, \tau_t)|$$

这意味着**任务向量之间的余弦相似度直接决定了干扰强度**——相似度越高，合并后性能损失越大。

为从根本上消除干扰，本文提出了**任务特征专业化**（Task-Feature Specialization, TFS）假说：不同任务使用预训练模型中不重叠的内部特征子集。理论证明，TFS 是权重解耦的充分条件（**Theorem 1**），并且 TFS 在几何上必然导致**权重向量正交性**（Weight Vector Orthogonality, WVO）——即预训练权重矩阵的列向量呈现块正交结构（**Corollary 1**）。这一理论框架揭示了 TFS → WVO → WD 的因果链条（Figure 1）。

### OrthoReg：显式正交正则化

基于上述理论，本文的核心方法创新是 **OrthoReg**——一种在微调期间显式强制权重更新矩阵内部正交性的正则化技术。其关键洞察是：即使在特征重叠的现实场景中，通过约束 $\Delta W$ 的列向量彼此正交，也能主动促进任务向量之间的解耦（**Theorem 2**）。

具体而言，OrthoReg 在标准微调损失中引入一个正交正则项：

$$\mathcal{L} = \mathcal{L}_{\mathrm{task}}(\theta_0 + \Delta\theta) + \lambda \cdot \mathcal{L}_{\mathrm{ortho}}(\Delta\theta)$$

其中正交损失定义为对所有被调整线性层的权重更新矩阵施加列正交约束：

$$\mathcal{L}_{\mathrm{ortho}}(\Delta\theta) = \sum_l \|(\Delta W^{(l)})^\top \Delta W^{(l)} - I\|_F^2$$

该损失项强制 $\Delta W^{(l)}$ 的 Gram 矩阵逼近单位矩阵，使更新矩阵的列向量相互正交且具有单位范数。

### 与 TTA 的本质区别

| 维度 | TTA | OrthoReg |
|------|-----|----------|
| 正交性来源 | 依赖 NTK 几何隐式实现 | 通过正则项显式约束 |
| 计算代价 | 雅可比计算，显存翻倍，训练时间 2–3× | 仅增加轻量 Frobenius 范数计算 |
| 适用范围 | 仅限线性化微调 | 可嵌入任意微调范式（全量微调、LoRA、仅注意力微调等） |

在 ViT-L-14 上的计算成本对比（Table 3）显示，Non-lin. FT+OrthoReg 在取得优于 TTA 的精度的同时，训练时间和显存消耗仅略高于标准微调基线，远低于 TTA。

### 方法谱系与知识库定位

本工作处于**模型合并**（Model Merging）与**任务算术**的交叉点。与以下代表性基线形成对比：

- **Task Arithmetic**（标准任务向量微调）：直接对任务向量进行加权求和，无任何解耦机制。
- **TTA**（Tangent Task Arithmetic）：在线性化切线空间微调以隐式利用 NTK 几何，但计算代价高昂。
- **LoRA-ATT**：在注意力投影上使用低秩适配器进行参数高效微调，未考虑任务间干扰。
- **Attention-Only Fine-tuning**：仅微调注意力模块，缩小了可干预的参数空间，但缺乏显式解耦约束。

OrthoReg 的独特定位在于：**它是一种即插即用的正则化策略，而非独立的微调范式**。它可以无缝嵌入上述任何微调方法中，通过修改训练损失这一最小侵入式接口（changed slot）来实现跨任务的权重解耦。

## 整体框架

### 核心问题与解决路径

任务算术（Task Arithmetic）通过将多个微调后的任务向量 $\tau_t = \theta_t^* - \theta_0$ 线性叠加到预训练模型上，实现多任务能力的合并。然而，来自不同任务向量的**干扰**是导致合并后性能下降的核心瓶颈。本文的理论分析表明，这种干扰的本质在于不同任务使用了重叠的内部特征，使得一个任务向量的更新会破坏另一任务的输出。

为解决这一问题，本文提出 **OrthoReg**，一种在微调阶段施加的正则化方法。其核心思想是：通过强制权重更新矩阵 $\Delta W^{(l)}$ 在列方向上保持正交，即使在特征重叠的情况下，也能主动促进任务向量之间的解耦，从而在合并时减少跨任务干扰。

### 整体 Pipeline

OrthoReg 的完整流程包含两个阶段：**正交微调阶段** 与 **模型合并阶段**。

```
预训练模型 θ₀
     │
     ├── 任务 1 微调 ──→ 任务向量 τ₁
     │      │
     │      └── 任务损失 L_task + 正交正则化 L_ortho
     │
     ├── 任务 2 微调 ──→ 任务向量 τ₂
     │      │
     │      └── 任务损失 L_task + 正交正则化 L_ortho
     │
     └── ... (共 T 个任务)
              │
              ▼
         多任务合并：θ_MT = θ₀ + α Σ τ_t
              │
              ▼
         合并后多任务模型
```

#### 阶段一：正交微调

对于每个任务 $t$，在预训练模型 $\theta_0$ 的基础上进行微调，但损失函数被扩展为两项之和：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{task}}(\theta_0 + \Delta\theta) + \lambda \cdot \mathcal{L}_{\mathrm{ortho}}(\Delta\theta)
$$

其中：
- **任务损失模块** $\mathcal{L}_{\mathrm{task}}$：标准的监督学习损失，确保模型在目标任务上获得良好性能。
- **正交正则化模块** $\mathcal{L}_{\mathrm{ortho}}$：对所有权重更新矩阵施加列正交约束，定义为：

$$
\mathcal{L}_{\mathrm{ortho}}(\Delta\theta) = \sum_l \|(\Delta W^{(l)})^\top \Delta W^{(l)} - I\|_F^2
$$

该正则项强制 $\Delta W^{(l)}$ 的 Gram 矩阵逼近单位矩阵，即驱动更新矩阵的各列相互正交且具有单位范数。超参数 $\lambda$ 控制正则化强度，在 $[0.1, 100]$ 范围内通过验证集选定。

#### 阶段二：模型合并

微调完成后，每个任务得到一个任务向量 $\tau_t = \theta_t^* - \theta_0$。多任务模型通过加权求和构建：

$$
\theta_{\mathrm{MT}} = \theta_0 + \alpha \sum_{t=1}^{T} \tau_t
$$

其中 $\alpha$ 为统一的缩放系数。由于 OrthoReg 在微调阶段已迫使各任务向量的内部结构趋向正交，合并时的跨任务干扰被显著抑制。

### 模块关系与数据流

| 模块 | 输入 | 输出 | 作用 |
|------|------|------|------|
| 任务损失计算 | 当前参数 $\theta_0 + \Delta\theta$，任务数据 $\mathcal{D}_t$ | 标量损失 $\mathcal{L}_{\mathrm{task}}$ | 保持单任务精度 |
| 正交正则化计算 | 权重更新矩阵 $\Delta W^{(l)}$ | 标量损失 $\mathcal{L}_{\mathrm{ortho}}$ | 强制更新矩阵列正交，促进解耦 |
| 联合优化 | $\mathcal{L}_{\mathrm{task}} + \lambda \mathcal{L}_{\mathrm{ortho}}$ | 微调后参数 $\theta_t^*$ | 同时优化任务目标与解耦结构 |
| 任务向量提取 | $\theta_t^*$，$\theta_0$ | $\tau_t$ | 获取参数偏移量 |
| 多任务合并 | $\theta_0$，$\{\tau_t\}_{t=1}^T$，$\alpha$ | $\theta_{\mathrm{MT}}$ | 构建多任务模型 |

### 理论支撑

整个框架建立在两个关键理论结果之上：

1. **TFS 是权重解耦的充分条件**（Theorem 1）：在 NTK 线性化假设下，若预训练模型满足任务-特征专业化（Task-Feature Specialization），即不同任务使用不重叠的内部特征，则任务向量之间自然满足权重解耦。

2. **OrthoReg 在特征重叠时仍能促进解耦**（Theorem 2）：即使在 TFS 不完全成立的现实场景中，通过约束权重更新矩阵的内部正交性，OrthoReg 仍能主动减少任务间的干扰，从而促进解耦。

这两个定理共同构成了从理想条件到现实应用的理论桥梁：TFS 解释了预训练模型为何天然具备解耦潜力（Figure 1），而 OrthoReg 则提供了在特征重叠时强制实现这一结构的实用手段（Figure 3）。

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/001_Figure_1.jpg]]
*Figure 1: Conceptual illustration of our central thesis: Task-Feature Specialization (TFS) is proposed and shown as the common cause that connects the geometric property of Weight Vector Orthogonality (WVO) with the functional property of Weight Disentanglement (WD). This paper establishes this connection in two ways: first, by proving that TFS, which gives rise to inherent orthogonality in the pre-trained model θ0, is a sufficient condition for ideal disentanglement; and second, by proposing a method that actively enforces this structure on weight updates (∆W ) that constitute τt to promote disentanglement in realistic scenarios*

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/003_Figure_3.jpg]]
*Figure 3: An overview of the OrthoReg method. It mitigates task interference caused by feature overlap by introducing*

## 核心模块与公式推导

### 核心模块

OrthoReg 在标准微调流程中引入一个额外的正交正则化损失模块，与任务损失联合优化，从而在训练过程中主动塑造权重更新的几何结构。

**Pipeline 模块组成：**

1. **Task Loss Computation（任务损失计算）**：计算针对特定任务的标准监督损失 $\mathcal{L}_{\mathrm{task}}(\theta_0 + \Delta\theta)$，其中 $\theta_0$ 为预训练参数，$\Delta\theta$ 为权重更新量。
2. **Orthogonal Regularization Loss Computation（正交正则化损失计算）**：对所有权重更新矩阵计算列向正交约束损失 $\mathcal{L}_{\mathrm{ortho}}(\Delta\theta)$。
3. **Combined Optimization（联合优化）**：将上述两项损失加权求和后反向传播，更新模型参数。

**方法改动槽位：**

| 槽位 | 基线值 | OrthoReg 值 |
|------|--------|-------------|
| Training Loss | $\mathcal{L}_{\mathrm{task}}(\theta)$ | $\mathcal{L}_{\mathrm{task}}(\theta_0+\Delta\theta) + \lambda \cdot \mathcal{L}_{\mathrm{ortho}}(\Delta\theta)$ |
| Regularization Term | None | $\mathcal{L}_{\mathrm{ortho}}(\Delta\theta) = \sum_l \|(\Delta W^{(l)})^\top \Delta W^{(l)} - I\|_F^2$ |

### 关键公式推导

**公式 1：任务向量定义**

$$\tau_t = \theta_t^* - \theta_0$$

其中 $\tau_t$ 为任务 $t$ 的任务向量，$\theta_t^*$ 为在任务 $t$ 上微调后的模型参数，$\theta_0$ 为预训练模型参数。任务算术通过合并多个任务向量实现多任务能力：

$$\theta_{\mathrm{MT}} = \theta_0 + \alpha \sum_{t=1}^{T} \tau_t$$

其中 $\alpha$ 为统一缩放系数。

**公式 2：权重解耦条件（成对简化形式）**

$$f(\boldsymbol{x}; \boldsymbol{\theta}_0 + \tau_t + \tau_j) = f(\boldsymbol{x}; \boldsymbol{\theta}_0 + \tau_t), \quad \forall \boldsymbol{x} \in \mathcal{D}_t$$

该条件要求合并模型在任务 $t$ 数据上的行为仅取决于 $\tau_t$，而不受 $\tau_j$ 干扰。在 NTK 线性化假设下，这一功能性质等价于雅可比正交条件：

$$\tau_j^\top J(x) = 0, \quad \forall x \in \mathcal{D}_t$$

其中 $J(x)$ 为模型在 $x$ 处的雅可比矩阵。该条件表明，任务 $j$ 的任务向量与任务 $t$ 数据的梯度方向正交时，干扰为零。

**公式 3：OrthoReg 训练总损失**

$$\mathcal{L} = \mathcal{L}_{\mathrm{task}}(\theta_0 + \Delta\theta) + \lambda \cdot \mathcal{L}_{\mathrm{ortho}}(\Delta\theta)$$

其中 $\lambda$ 为正则化强度超参数，在 $[0.1, 100]$ 范围内通过验证集选取。

**公式 4：正交正则化项**

$$\mathcal{L}_{\mathrm{ortho}}(\Delta\theta) = \sum_l \|(\Delta W^{(l)})^\top \Delta W^{(l)} - I\|_F^2$$

该损失对所有被调整的线性层 $l$ 施加约束，迫使权重更新矩阵 $\Delta W^{(l)}$ 的 Gram 矩阵逼近单位矩阵 $I$，从而驱动 $\Delta W^{(l)}$ 的列向量相互正交且具有单位范数。这一约束的动机来源于预训练模型中的经验观察：CLIP ViT-B/16 中线性层权重列向量之间的角度分布尖锐地集中在 90° 附近（Figure 2），表明预训练模型天然具备列向正交性，OrthoReg 旨在微调过程中保持并强化这一结构。

### 理论保证

**Theorem 1** 证明，在 NTK 线性化假设下，任务特征专业化（Task-Feature Specialization, TFS）是权重解耦的充分条件。**Corollary 1** 进一步表明，满足 TFS 的模型其权重矩阵必然呈现块正交性（Block Orthogonality），即权重向量正交性（WVO）是 TFS 的几何结果。

**Theorem 2** 证明，通过对任务更新矩阵施加近似内部正交约束，OrthoReg 能够在特征重叠的现实场景下主动促进任务间的权重解耦。这一理论保证使得 OrthoReg 区别于仅依赖预训练模型固有正交性的方法，在特征重叠导致干扰时仍能有效工作。

### 补充图表

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/002_Figure.jpg]]
*Figure: (a) The distribution of angles be- (b) Statistical summary of angular tween column vector pairs in a deviations from 9 $0 ^ { \circ }$ across all linear weight matrix. layers of the model*

## 实验与分析

### 主要实验结果

OrthoReg 在任务添加（task addition）和任务否定（task negation）两个核心基准上均展现出对多种基线方法一致且显著的性能提升。

**任务添加**：在 8 任务向量合并场景下，OrthoReg 在所有 CLIP 模型架构上均提高了绝对准确率（Abs.Acc.）和归一化准确率（Norm.Acc.）。以 CLIP ViT-B-32 为例，**Non-lin. FT+OrthoReg** 将 Abs.Acc. 从 70.32 提升至 73.41（+3.09），Norm.Acc. 从 77.56 提升至 93.93（+16.37），表明正交正则化对合并质量的改善尤为突出（Table 1）。在更大规模的 ViT-L-14 上，**ATT-FT+OrthoReg** 达到 90.41 的 Abs.Acc.（基线 87.81，+2.60），而 **Non-lin. FT+OrthoReg** 从 84.07 提升至 88.23（+4.16），验证了该方法在更大模型上的可扩展性（Table 1, Table 3）。

**任务否定**：在保持 ImageNet 控制任务准确率不低于 95% 的约束下，OrthoReg 显著降低了目标任务的平均准确率。以 ViT-B-32 为例，**Non-lin. FT+OrthoReg** 将目标准确率从 21.11 降至 14.61（−6.50），而 **TTA+OrthoReg** 在所有三个模型架构上均取得了最低的目标准确率（ViT-B-32: 11.39, ViT-B-16: 7.49, ViT-L-14: 8.36），验证了正交正则化在选择性遗忘任务上的强大能力（Table 2）。在更宽松的控制约束（90% 和 80%）下，这一优势依然保持（Table 4, Table 5）。

**跨任务性能分布**：在 ViT-L-14 的 8 个基准任务上，OrthoReg 增强后的合并模型（蓝色）在绝大多数任务上均优于基线合并模型（红色），且接近甚至超越零样本性能（灰色），如图 4 所示。这一模式在不同 ViT 架构上均得到了复现（Figure 8）。

### 消融实验

**模块级消融**：在 LoRA 配置的消融中，对注意力模块（qkvo 投影）施加正交正则化带来了最大幅度的性能提升——在 ViT-B-16 上 Abs.Acc. 提升达 +4.17（Table 6）。相比之下，仅在 MLP 层上使用 OrthoReg 时，小模型上出现了轻微的精度下降。这表明注意力模块中的特征重叠是任务干扰的主要来源，也是正交约束发挥最大作用的位置。

**超参数敏感性**：正则化强度 λ 在 [0.1, 100] 范围内通过验证集选定。在 LoRA-ATT 配置下，λ 的调整对性能影响稳定，未出现剧烈波动（Figure 6a）。合并系数 α 的分析显示，**TTA+OrthoReg**（蓝线）在广泛的 α 取值范围内始终优于基线 TTA（红线），表明 OrthoReg 训练出的任务向量对合并系数具有更强的鲁棒性（Figure 6b）。

### 计算效率

与需要计算雅可比矩阵的 TTA 相比，OrthoReg 仅引入适度的计算开销。在 ViT-L-14 的 Cars 数据集上，TTA 的训练时间和显存消耗显著高于 Non-lin. FT，而 OrthoReg 在 Non-lin. FT 基础上仅增加少量成本，却能取得优于 TTA 的绝对准确率（Table 3）。这使 OrthoReg 在性能与效率之间取得了更优的平衡。

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/009_Table_3.jpg]]
*Table 3: Computational cost comparison on the Cars dataset using a ViT-L-14 model. The table highlights the efficiency of OrthoReg. The final column shows the Absolute Accuracy from the task addition benchmark (as seen in Table 1 of the main paper). While applying OrthoReg to Non-linear Fine-tuning (Non-lin. FT) achieves performance that is superior to Tangent Task Arithmetic (TTA) and significantly better than the baseline Non-lin. FT, this table further demonstrates its superior computational efficiency. As seen, TTA incurs substantial overhead in both training time and memory, whereas OrthoReg adds only a modest cost to the baseline. The colored cells visually emphasize the significant difference...*

### 解耦效果的直接验证

任务向量之间的余弦相似度热力图提供了 OrthoReg 促进解耦的直接证据。在 ViT-B-16 上，标准 Non-lin. FT 训练出的任务向量在多个任务对之间表现出高相似度（Figure 5a），而使用 OrthoReg 训练后，任务向量之间的正交性显著增强（Figure 5b），与理论预期一致——正交正则化有效降低了任务向量间的共线性，从而减轻了合并时的相互干扰。

### 失败模式与局限

1. **MLP-only 配置下的性能退化**：当正交正则化仅施加于 MLP 层时，小模型（如 ViT-B-16）上出现轻微精度下降（Table 6）。这表明预训练模型中 MLP 层的列正交性可能不如注意力层显著，强制正交约束反而可能损害任务特定特征的表达能力。

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/018_Table_6.jpg]]
*Table 6: Performance comparison of different LoRA module configurations with and without orthogonality regularization. The last row under each module shows the improvement (∆) from OrthoReg*

2. **正则化强度的依赖**：λ 的选取依赖验证集，缺乏自适应的选择机制。在无验证集可用的场景下，这一依赖可能限制方法的即插即用性。

3. **正交形式的局限性**：当前方法仅约束列向正交性（Gram 矩阵逼近单位阵），但理论分析表明更强的块正交结构（Corollary 1）可能提供更精细的解耦控制。这一方向有待进一步探索。

### 补充图表

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/004_Table_1.jpg]]
*Table 1: Task addition results on CLIP-based models. Performance of adding 8 task vectors on three architectures. Our proposed orthogonal regularization (+OrthoReg) is applied to several baselines, showing consistent improvements in both Absolute Accuracy (Abs.Acc.) and Normalized Accuracy (Norm.Acc.). An asterisk (*) denotes the best absolute accuracy for each model architecture*

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/005_Table_2.jpg]]
*Table 2: The minimum average Target Accuracy (Tar.Acc.) achievable while maintaining at least 95% of the zero-shot accuracy on the ImageNet control task (Con.Acc.). Our proposed orthogonal regularization (+OrthoReg) shows a consistent and significant improvement in forgetting the target task. An asterisk (*) denotes the best (lowest) target accuracy for each model architecture*

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/008_Figure_5.jpg]]
*Figure 5: Cosine similarity heatmaps of task vectors for ViT-B-16. (a) Task vectors from Non-lin. FT show high similarity for several task pairs. (b) Task vectors trained with OrthoReg are significantly more orthogonal*

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/007_Figure_6.jpg]]
*Figure 6: Analysis of hyperparameter sensitivity on ViT-B-16. (a) The impact of the regularization strength λ on the performance of LoRA-ATT. (b) The influence of the merging coefficient α on the final accuracy of the merged model. The blue line (TTA+OrthoReg) consistently outperforms the red line (baseline TTA) across a wide range of α values*

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/011_Figure_8.jpg]]
*Figure 8: The accuracy of merged models across the eight benchmark tasks for different ViT architectures. Each subplot shows the performance for a specific baseline method: zero-shot (gray), the baseline’s merged model (red), and the baseline enhanced with our orthogonal regularization (blue). The rows correspond to models: (a) ViT-B-16, (b) ViT-B-32, and (c) ViT-L-14*

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/012_Table_4.jpg]]
*Table 4: The minimum average Target Accuracy (Tar.Acc.) achievable while maintaining at least 90% of the zero-shot accuracy on the ImageNet control task (Con.Acc.). Our proposed orthogonal regularization (+OrthoReg) shows a consistent and significant improvement in forgetting the target task. An asterisk (*) denotes the best (lowest) target accuracy for each model architecture*

![[assets/figures/papers/paper_list_l2144_https_arxiv_org_abs_2604_17078/figures/013_Table_5.jpg]]
*Table 5: The minimum average Target Accuracy (Tar.Acc.) achievable while maintaining at least 80% of the zero-shot accuracy on the ImageNet control task (Con.Acc.). Our proposed orthogonal regularization (+OrthoReg) shows a consistent and significant improvement in forgetting the target task. An asterisk (*) denotes the best (lowest) target accuracy for each model architecture*

## 方法谱系与知识库定位

### 任务算术中的权重解耦：从隐式条件到显式正则化

本工作所解决的瓶颈是**任务算术中来自不同任务向量的干扰导致合并模型性能下降**。在这一问题脉络中，已有方法可大致分为两类：一类依赖模型架构或微调策略的隐式约束，另一类则试图通过后处理或正则化显式地减少干扰。

**标准非线性微调（Non-linear Fine-tuning）** 是任务算术最直接的基线：对每个任务独立微调预训练模型，得到任务向量 $\tau_t = \theta_t - \theta_0$，再通过加权求和 $\theta_{MT} = \theta_0 + \alpha \sum \tau_t$ 合并。该方法没有任何解耦机制，任务向量之间的特征重叠会导致严重的相互干扰，表现为归一化准确率（Norm.Acc.）的大幅下降（例如在 CLIP ViT-B-32 上仅 77.56%，见 Table 1）。

**切线任务算术（Tangent Task Arithmetic, TTA）** 通过在线性化的切线空间中进行微调，利用 NTK 几何隐式地减少任务向量间的干扰。其代价是每次更新需要计算雅可比矩阵，导致显存占用翻倍、训练时间增加 2–3 倍（见 Table 3）。从解耦机制上看，TTA 依赖模型的 NTK 几何特性间接达成正交性，而 OrthoReg 则通过显式的正则化项直接强制正交结构。

**参数高效微调方法**（如 LoRA-ATT，仅在注意力投影层上使用低秩适配器）和 **仅微调注意力模块（Attention-Only Fine-tuning）** 通过限制可调参数的范围来减少任务间干扰，但它们并不主动塑造权重更新的几何结构，因此解耦效果依赖于架构的先验稀疏性。

### OrthoReg 的方法定位与核心创新

OrthoReg 的核心操作是**在微调损失中引入权重更新矩阵的列正交约束**：

$$\mathcal{L} = \mathcal{L}_{\mathrm{task}}(\theta_0 + \Delta\theta) + \lambda \cdot \mathcal{L}_{\mathrm{ortho}}(\Delta\theta)$$

其中正交正则化项定义为：

$$\mathcal{L}_{\mathrm{ortho}}(\Delta\theta) = \sum_l \|(\Delta W^{(l)})^\top \Delta W^{(l)} - I\|_F^2$$

该约束强制每一层的权重更新矩阵 $\Delta W^{(l)}$ 的列向量相互正交且具有单位范数。与 TTA 相比，OrthoReg 的**因果调节旋钮**直接作用于权重更新的内部结构，而非依赖 NTK 线性化的间接效应。理论保证来自两个层面：

1. **充分性条件**：任务特征专业化（Task-Feature Specialization, TFS）——即不同任务使用不重叠的内部特征——被证明是权重解耦的充分条件（Theorem 1），且 TFS 在几何上表现为权重向量正交性（Weight Vector Orthogonality, WVO）（Corollary 1）。

2. **显式正则化的理论效力**：即使在实际场景中存在特征重叠，约束任务更新矩阵近似内部正交仍能积极促进任务间的权重解耦（Theorem 2）。

### 适用边界与失效模式

OrthoReg 的增益存在明确的**架构依赖**：

- **注意力模块是主要收益来源**：消融实验（Table 6, Section J.5.2）表明，在注意力模块（qkvo 投影）上施加正交正则化带来最大性能提升（ViT-B-16 上 +4.17 Abs.Acc.），这与 Transformer 中注意力层的线性映射结构天然适配列正交约束有关。
- **MLP-only 配置下可能退化**：当仅在 MLP 层上微调并施加 OrthoReg 时，小模型上出现轻微的准确率下降。这表明列正交约束在 MLP 的非线性变换链中的有效性有限，需要进一步验证。
- **正交形式的单一性**：当前方法仅强制列向正交性。更复杂的正交形式（如块正交）可能提供更强的控制能力，但尚未被探索。

### 超参数敏感性与计算效率

正则化强度 $\lambda$ 在 $[0.1, 100]$ 范围内通过验证集选定，实验表明在该范围内性能提升稳定（Figure 6a）。合并系数 $\alpha$ 的敏感性分析（Figure 6b）显示，OrthoReg 增强的模型在更宽的 $\alpha$ 范围内保持优势。在计算开销方面，OrthoReg 仅增加适度的训练成本，远低于 TTA 的雅可比计算开销（Table 3），这使得它在大模型（如 ViT-L-14）上具有更好的可扩展性。

### 开放问题

1. **正交形式的拓展**：列正交是块正交的简化形式。探索更丰富的正交约束（如行正交、双重正交、分组正交）是否能进一步提升解耦效果，是一个直接的理论延伸方向。

2. **TFS 假设的泛化性**：TFS 与正交性之间的因果关系是在 Transformer 架构上验证的。在仅含 MLP 的模型或其他架构（如状态空间模型）中，这一关系是否依然成立，需要进一步的理论和实证检验。

3. **自适应正则化强度**：当前 $\lambda$ 依赖验证集手动选择。如何在不使用验证集的情况下，为每个任务自适应地确定最优正则化强度，是实现更自动化模型合并的关键问题。

4. **与模型合并后处理方法的协同**：OrthoReg 在微调阶段塑造任务向量的几何结构，而现有的一些方法（如 TIES-Merging、DARE）在合并阶段进行后处理。两者的协同效应尚未被系统研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Understanding_and_Enforcing_Weight_Disentanglement_in_Task_Arithmetic.pdf]]
