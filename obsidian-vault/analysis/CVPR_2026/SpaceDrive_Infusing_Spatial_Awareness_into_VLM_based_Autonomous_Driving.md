---
title: "SpaceDrive: Infusing Spatial Awareness into VLM-based Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpaceDrive_Infusing_Spatial_Awareness_into_VLM_based_Autonomous_Driving.pdf
project_link: "https://zhenghao2519.github.io/SpaceDrive"
code_link: "https://github.com/zhenghao2519/SpaceDrive"
aliases:
- SpaceDrive
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入统一的3D正弦-余弦位置编码，同时替换视觉token补充中的隐式空间信息和文本中的数字坐标标记，并采用回归式解码器替代分类式语言头来直接预测连续坐标。这一改动使VLM能够在统一的位置编码空间内显式关联2D语义特征与3D空间位置，从而准确索引视觉语义并进行联合空间推理。
primary_logic: Transformer架构天然适合处理token之间的位置关系；将3D空间关系显式编码为统一的位置编码输入，可让VLM在保持通用视觉-语言对齐的基础上直接进行3D空间推理。这种统一表达避免了任务特定嵌入的碎片化，同时通过回归解码解决了语言模型在数值预测上的先天不足，为VLM增强3D空间智能提供了一种通用范式。
claims:
- 向视觉token添加空间位置编码后，SpaceDrive的L2误差降低0.63，碰撞率降低2.08%，交叉率降低4.14%（Exp.2 vs 1）
- 统一位置编码同时作用于视觉和文本坐标流时，无论是否使用ego状态，规划性能均得到提升（Exp.4 vs 1; Exp.6 vs 5）
- 使用正弦-余弦编码器（平移不变性）优于全学习MLP编码器，L2误差从1.96降至1.80（Exp.4 vs 8）
- 在Bench2Drive闭环评测中，纯文本数字输出的VLM模型（OmniDrive-L）轨迹退化为近似直线且方向振荡，证实数字逐位输出不适合闭环驾驶
---

# SpaceDrive: Infusing Spatial Awareness into VLM-based Autonomous Driving

> [!tip] 核心洞察
> Transformer架构天然适合处理token之间的位置关系；将3D空间关系显式编码为统一的位置编码输入，可让VLM在保持通用视觉-语言对齐的基础上直接进行3D空间推理。这种统一表达避免了任务特定嵌入的碎片化，同时通过回归解码解决了语言模型在数值预测上的先天不足，为VLM增强3D空间智能提供了一种通用范式。

| 字段 | 内容 |
|------|------|
| 中文题名 | SpaceDrive：为基于VLM的自动驾驶注入空间感知 |
| 英文题名 | SpaceDrive: Infusing Spatial Awareness into VLM-based Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.10719) · [Project](https://zhenghao2519.github.io/SpaceDrive) · [Code](https://github.com/zhenghao2519/SpaceDrive) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SpaceDrive |
| Dataset | nuScenes, Bench2Drive |

> [!tip] 效果简介
> - nuScenes (open-loop) 上，L2 (m) Avg. ↓ 0.32 (SpaceDrive+) vs 0.33 (OmniDrive-Q++) (-0.01)；Collision (%) Avg. ↓ 0.23% (SpaceDrive+) vs 0.30% (OmniDrive-Q++) (-0.07%)；Intersection (%) Avg. ↓ 1.27% (SpaceDrive+) vs 3.00% (OmniDrive-Q++) (-1.73%)。
> - Bench2Drive (closed-loop) 上，Driving Score ↑ 78.02 (SpaceDrive+) vs 77.74 (ORION) (+0.28)；Success Rate (%) ↑ 55.11% (SpaceDrive+) vs 54.62% (ORION) (+0.49%)。

## 概要

现有基于视觉-语言模型（VLM）的端到端自动驾驶规划器普遍缺乏空间感知能力。根本原因在于两方面：其一，VLM缺少基于3D数据的预训练，仅依赖2D语义进行推理，难以将3D坐标与对应物体准确关联，导致场景描述模糊甚至错误；其二，语言模型将数值处理为逐位数字分类，忽略了数字标记之间的序数邻近性，且错误地平均了不同数字位的权重，使得路径点预测精度低下。在闭环仿真中，纯文本数字输出的VLM模型（如OmniDrive-L）轨迹退化为近似直线且方向振荡，直接证实了数字逐位输出不适合闭环驾驶。

SpaceDrive针对上述瓶颈提出了统一的3D位置编码方案。其核心思路是：将空间信息从文本数字token重构为显式的位置编码（Positional Encoding, PE），同时作用于视觉token增强和文本坐标替换两个通道，并采用回归式解码器替代分类式语言头来直接预测连续坐标。这一设计使VLM能够在统一的编码空间内显式关联2D语义特征与3D空间位置，从而准确索引视觉语义并进行联合空间推理。

在nuScenes开环评测中，SpaceDrive+取得了VLM方法中最优的L2误差（0.32 m）、碰撞率（0.23%）和交叉率（1.27%）；在Bench2Drive闭环评测中，驾驶得分达到78.02，成功率55.11%，位列VLM方法第二。消融实验表明，向视觉token注入空间位置编码后，L2误差降低0.63，碰撞率降低2.08%，交叉率降低4.14%；统一位置编码同时作用于视觉和文本坐标流时，无论是否使用ego状态，规划性能均得到提升。此外，正弦-余弦编码器因平移不变性优于全学习MLP编码器，且方法对深度噪声具有鲁棒性。

### 端到端自动驾驶的范式演进

端到端（End-to-End, E2E）自动驾驶旨在将传感器输入直接映射为规划轨迹，省去传统模块化管线中的中间表征与人工规则设计。近年来，视觉语言模型（Vision-Language Model, VLM）凭借其强大的场景理解与常识推理能力，被逐步引入E2E规划任务，衍生出以**OmniDrive**、**ORION**、**DriveVLM**、**EMMA**和**RDA-Driver**为代表的VLM基规划器。这些方法将多视图图像、文本指令和自车状态拼接为统一token序列，交由VLM自回归生成驾驶决策与轨迹坐标。

然而，VLM在自动驾驶中的空间推理能力存在根本性缺陷，这构成了本文的核心动机。

### 瓶颈一：3D空间感知的缺失

现有VLM的预训练语料以2D图文对为主，缺乏对3D几何结构的显式建模。当面对自动驾驶中的多视图输入时，模型只能依赖2D语义特征进行推理，难以将3D坐标与对应物体和2D语义准确关联。这种“空间盲”导致两个直接后果：

1. **语义-空间关联模糊**：VLM无法精确地将文本中的坐标指令（如“前方15米处的车辆”）与视觉token中的对应区域建立索引关系，产生模糊甚至错误的场景描述。
2. **轨迹预测精度低下**：由于缺少对3D空间结构的显式建模，模型生成的路径点往往偏离实际道路几何，尤其在弯道、交叉口等需要精细空间推理的场景中表现恶化。

### 瓶颈二：语言模型对数值坐标的先天不足

现有VLM规划器将轨迹坐标视为普通文本数字token，通过语言头逐位分类输出。这种设计存在两个深层缺陷：

- **序数邻近性被忽略**：语言模型将数字“15”拆分为“1”和“5”两个独立token分类，完全忽略了数字位之间的序数关系。这意味着模型并不“理解”15比14大、比16小，而只是学会了在特定上下文中输出特定的token组合。
- **误差平均效应**：语言头对每一位数字的预测误差被错误地等权平均，导致整体坐标精度受损。在闭环驾驶中，这种效应尤为致命——**OmniDrive-L**在Bench2Drive闭环评测中的轨迹退化为近似直线且方向振荡，直接证实了纯文本数字输出不适合闭环驾驶（附录C.2）。

### 本文动机：为VLM注入统一的3D空间感知

上述瓶颈指向一个核心洞察：**Transformer架构天然适合处理token之间的位置关系**。如果能将3D空间关系显式编码为统一的位置编码输入，VLM便能在保持通用视觉-语言对齐的基础上，直接进行3D空间推理。

基于此，SpaceDrive提出了一种空间感知的VLM驾驶框架，其核心思想是：**将空间信息视为显式的位置编码（Positional Encoding, PE），而非文本数字token**。具体而言，SpaceDrive引入统一的3D正弦-余弦位置编码，同时作用于视觉token的补充信息和文本中的数字坐标替换，并采用回归式解码器替代分类式语言头来直接预测连续坐标。这一改动使VLM能够在统一的位置编码空间内显式关联2D语义特征与3D空间位置，从而准确索引视觉语义并进行联合空间推理——这种统一表达避免了任务特定嵌入的碎片化，为VLM增强3D空间智能提供了一种通用范式。

## 核心方法与创新机理

SpaceDrive 的核心创新在于**将空间信息从“文本数字符号”提升为“统一的位置编码原语”**，从而解决当前 VLM 规划器在 3D 空间推理上的两个根本性缺陷：（1）缺乏基于 3D 数据的预训练，导致模型仅依赖 2D 语义，难以将 3D 坐标与对应物体准确关联；（2）语言模型将数值处理为逐位数字分类，忽略了数字标记之间的序数邻近性，且错误地平均了不同数字位的权重，导致路径点预测精度低下。

围绕这一核心洞察，SpaceDrive 在三个关键环节上对基线 VLM 规划器进行了系统性改造，形成了以下三个 **changed slots**：

### 1. 坐标表示与接口：从“逐位分类式文本数字”到“统一回归式 PE 编码”

**基线方案**（如 OmniDrive、ORION 等）将 3D 坐标以文本数字 token 的形式输入和输出 VLM，依赖语言模型的分类头逐位生成数字。这种方式存在两个致命问题：一是语言模型对数字 token 的处理缺乏序数邻近性感知，将“1.5”与“1.6”视为与“1.5”与“9.9”同等距离的离散符号；二是逐位分类错误地平均了不同数字位的权重，导致坐标预测精度严重退化——在 Bench2Drive 闭环评测中，纯文本数字输出的 VLM 模型（OmniDrive-L）轨迹退化为近似直线且方向振荡（Appendix C.2），直接证实了这一设计不适合闭环驾驶。

**SpaceDrive 方案**：引入统一的 3D 正弦-余弦位置编码器 $\phi(\mathbf{c})$ 替代文本数字 token 作为坐标的输入输出接口，并采用回归式 PE 解码器 $\psi$ 替代分类式语言头来直接预测连续坐标。具体而言：
- **输入端**：所有 3D 坐标（包括视觉 patch 对应的 3D 点 $\mathbf{c}_p$、文本提示中的 BEV 坐标 $\mathbf{c}_r$、历史 ego 位置 $\mathbf{c}_t^{ego}$）均通过同一 PE 编码器转换为统一的位置编码向量；
- **输出端**：扩展词汇表增加 $\langle\text{IND}\rangle$ 标识符，当语言头输出该标识后，后续隐藏状态 $\mathbf{e}_{j+1}$ 被路由至 PE 解码器直接回归 3D 坐标 $\hat{\mathbf{c}} = \psi(\mathbf{e}_{j+1}) \in \mathbb{R}^3$，损失函数采用 Huber 损失。

这一改动使 VLM 能够在统一的位置编码空间内显式关联 2D 语义特征与 3D 空间位置，从而准确索引视觉语义并进行联合空间推理。消融实验（Table 3）表明，统一位置编码同时作用于视觉和文本坐标流时，无论是否使用 ego 状态，规划性能均得到显著提升（Exp.4 vs Exp.1; Exp.6 vs Exp.5）。

### 2. 空间信息注入方式：从“隐式查询/无 3D 信息”到“显式 3D PE 直接加和”

**基线方案**中，VLM 规划器要么完全没有显式 3D 信息（仅依赖 2D 语义进行推理），要么通过任务特定的嵌入或可学习查询隐式注入 3D 线索。这种隐式方式缺乏度量空间中的几何约束，模型难以建立像素坐标与真实 3D 位置之间的精确对应关系。

**SpaceDrive 方案**：基于预训练深度估计器 $f_{dep.}$ 生成稠密绝对深度图，将每个视觉 patch 反投影为 3D 坐标 $\mathbf{c}_p$，经 PE 编码后以可学习归一化因子 $\alpha_{PE}$ 加权，**直接加到**模态对齐后的视觉 token 上：

$$\tilde{h}_p = h_p + \alpha_{PE} \phi(\mathbf{c}_p)$$

同时，文本提示中检测到的坐标子串被替换为相同的 PE token（BEV 坐标的 z 维置 0）。这种显式、统一的加性注入方式使 Transformer 的注意力层能够自然恢复 token 之间的空间关系。消融实验（Table 3, Exp.2 vs Exp.1）证实，仅向视觉 token 添加空间位置编码，就能使 L2 误差降低 0.63，碰撞率降低 2.08%，交叉率降低 4.14%。

### 3. 轨迹输出方式：从“自回归逐位生成数字”到“专用解码器直接回归坐标”

**基线方案**依赖 VLM 的语言头自回归逐位生成数字坐标（如“1”“.”“5”），这不仅引入了前述的数字处理缺陷，还将连续坐标预测降级为离散分类问题，丧失了度量空间的平滑性。

**SpaceDrive 方案**：在输出 $\langle\text{IND}\rangle$ 标识后，由专用 PE 解码器（MLP）直接从隐藏状态回归 3D 坐标。该机制在保持语言模型自回归生成连贯文本的同时，为坐标输出提供了精确的连续值预测能力。联合训练目标为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{LM}} + \mathcal{L}_{\mathrm{reg.}}(\hat{\mathbf{c}}, \mathbf{c})$$

其中 $\mathcal{L}_{\mathrm{LM}}$ 作用于所有文本输出，$\mathcal{L}_{\mathrm{reg.}}$ 采用 Huber 损失作用于所有坐标输出。PE 编码器/解码器的消融（Table 4）进一步表明，使用正弦-余弦编码器（具有平移不变性）优于全学习 MLP 编码器（L2 误差从 1.96 降至 1.80），且回归解码器是保证输出语义合理性的必要条件——直接数值逆映射会导致仅 4929/5119 个样本输出语义合理。

---

**总结**：SpaceDrive 的三个 changed slots 构成了一个自洽的创新闭环——统一的 PE 编码器将空间信息提升为 VLM 可直接操作的基础原语，显式加和注入使视觉 token 获得度量空间感知，回归解码器则弥补了语言模型在数值预测上的先天不足。这一设计范式使 VLM 在保持通用视觉-语言对齐的基础上，无需引入稠密 BEV 表示即可实现精确的 3D 空间推理与轨迹规划。

SpaceDrive 的整体框架围绕一个核心设计原则展开：**将空间信息显式编码为统一的三维位置编码（Positional Encoding, PE），替代传统 VLM 规划器中基于文本数字 token 的隐式坐标传递**。该框架在基础 VLM（默认 Qwen2.5-VL-7B）之上引入三个关键扩展模块——深度估计器、PE 编码器和 PE 解码器，形成从感知到规划的端到端空间感知推理链路。

### 输入处理流

系统接收两类输入：**多视图环绕图像** $\{I_k\}_{k=1}^K$ 和**文本提示**（包含导航指令、自车状态历史、BEV 坐标查询等）。

**视觉支路**首先由预训练的视觉编码器 $f_{\text{vis.}}$ 将多视图图像转换为 $N$ 个 patch token：

$$X_v = f_{\text{vis.}}(\{I_k\}) = \{x_p\}_{p=1}^N$$

随后通过一个简单的 MLP 投影器 $g$ 将视觉特征密集对齐到语言特征空间：

$$H_v = g(X_v) = \{h_p\}_{p=1}^N$$

**深度支路**并行运行一个冻结的预训练深度估计器 $f_{\text{dep.}}$，从相同的多视图图像中生成逐视图的稠密绝对深度图 $D_k = f_{\text{dep.}}(I_k)$。这些深度图被反投影为三维空间中的点云坐标 $\mathbf{c}_p$，为视觉 token 提供显式的度量空间位置信息。

### 统一空间编码

PE 编码器 $\phi(\cdot)$ 是框架的核心组件，负责将任意三维坐标转换为统一的正弦-余弦位置编码：

$$\phi(\mathbf{c}_p) = [\phi_x(x_p^{3D}), \phi_y(y_p^{3D}), \phi_z(z_p^{3D})] \in \mathbb{R}^{\text{dim}}$$

该编码被注入到两个信息流中：

1. **视觉 token 增强**：每个对齐后的视觉 token $h_p$ 与其对应三维坐标的 PE 相加，通过可学习的归一化因子 $\alpha_{PE}$ 调节幅度：
   $$\tilde{H}_v = \{\tilde{h}_p\}_{p=1}^N, \quad \tilde{h}_p = h_p + \alpha_{PE}\phi(\mathbf{c}_p)$$

2. **文本坐标替换**：文本提示中检测到的 BEV 坐标子串（如目标点位置）被替换为同一 PE 编码器生成的 token，并在其前插入特殊标识符 $\langle\text{IND}\rangle$：
   $$\tilde{H}_t = \{\tilde{h}_i\}_{i=1}^L, \quad \tilde{h}_i = \begin{cases} \phi(\mathbf{c}_r) & i \in S_r \\ \text{Tokenizer}(t_i) & \text{otherwise} \end{cases}$$

这种统一编码使视觉语义特征与空间位置在同一表示空间内显式关联，为后续的联合空间推理奠定基础。

### 推理与输出

增强后的视觉 token $\tilde{H}_v$ 和文本 token $\tilde{H}_t$ 拼接后送入基础 VLM 进行自回归推理。语言头 $W_{\text{lang}}'$ 的词汇表被扩展为 $\mathcal{V}' = \mathcal{V} \cup \{\langle\text{IND}\rangle\}$。

当模型输出 $\langle\text{IND}\rangle$ 标识符时，触发坐标解码流程：下一个隐藏状态 $\mathbf{e}_{j+1}$ 被路由至 PE 解码器 $\psi$（一个轻量 MLP），直接回归三维坐标：

$$\hat{\mathbf{c}} = \psi(\mathbf{e}_{j+1}), \quad \hat{\mathbf{c}} \in \mathbb{R}^3$$

这一机制在保持自回归文本生成连续性的同时，通过回归式解码器解决了传统语言模型逐位数字分类在数值预测上的先天不足。

### 训练目标

总损失由两部分联合优化：

$$\mathcal{L} = \mathcal{L}_{\text{LM}} + \mathcal{L}_{\text{reg.}}(\hat{\mathbf{c}}, \mathbf{c})$$

其中 $\mathcal{L}_{\text{LM}}$ 为标准语言建模损失（作用于所有文本输出），$\mathcal{L}_{\text{reg.}}$ 为坐标回归的 Huber 损失（作用于所有坐标输出）。基础 VLM 的核心 LLM 部分通过 LoRA（rank=16）进行参数高效微调，而深度估计器保持冻结。

### 设计要点

**Figure 2** 完整展示了上述流程：多视图图像经视觉编码和深度估计双路处理后，在 PE 编码器处汇合，统一的空间编码同时增强视觉 token 和替换文本坐标 token，最终由扩展词汇表的语言头与 PE 解码器协同输出规划轨迹。消融实验（Table 3）证实，向视觉 token 注入空间 PE 使 L2 误差降低 0.63、碰撞率降低 2.08%、交叉率降低 4.14%；统一作用于视觉和文本坐标流的编码进一步提升了规划性能。值得注意的是，该框架**不依赖稠密 BEV 特征**——实验表明统一的 PE 编码已足以支撑 VLM 导向的自动驾驶三维空间建模。

![[assets/figures/papers/paper_list_l2418_https_arxiv_org_abs_2512_10719/figures/002_Figure_2.jpg]]
*Figure 2: SpaceDrive framework. Beyond the base VLM, a frozen depth estimator predicts dense metric depths from surround-view images, which are projected into 3D coordinates and encoded by a universal PE encoder to augment visual tokens with spatial cues. BEV coordinates in text prompts are encoded by the same PE encoder, replacing the original coordinate tokens and preceded by the PE indicator ⟨IND⟩. At the output stage, the recognized PE is passed through a PE decoder to obtain the final coordinates for trajectory planning*

![[assets/figures/papers/paper_list_l2418_https_arxiv_org_abs_2512_10719/figures/001_Figure_1.jpg]]
*Figure 1: Spatial awareness in VLM-based end-to-end autonomous driving. (a) Constrained by insufficient 3D pre-training and discrete token-wise encoding, existing end-to-end planners based on the VLM struggle to precisely ground, associate, and predict 3D spatial positions, limiting their planning capabilities. (b) Our proposed SpaceDrive planner introduces a unified 3D coordinate encoding to replace the original VLM’s textual digit tokens and augment visual features, achieving explicit association with 2D perspective semantics to enhance joint spatial reasoning for E2E planning. Compared to current VLM-based methods, it achieves state-of-the-art driving capability in the nuScenes open-loop evaluatio...*

SpaceDrive 的核心设计围绕一个统一的空间坐标表达——**3D正弦-余弦位置编码（PE）**——展开，该编码同时作用于视觉流和文本流，使VLM能够在统一的坐标空间内进行显式的3D空间推理。整个框架由七个关键模块串联构成。

### 视觉编码与多模态对齐

给定 $K$ 张多视图图像 $\{I_k\}_{k=1}^K$，预训练的视觉编码器 $f_{vis.}$ 将其转换为 $N$ 个patch token：

$$X_v = f_{vis.}(\{I_k\}) = \{x_p\}_{p=1}^N \quad \text{(1)}$$

随后，一个简单的MLP投影器 $g$ 将视觉特征密集对齐到语言特征空间：

$$H_v = g(X_v) = \{h_p\}_{p=1}^N \quad \text{(2)}$$

这一投影步骤保持了与基础VLM（Qwen2.5-VL-7B）的特征空间兼容性，为后续空间信息注入提供了统一的语义基底。

### 3D空间信息注入：统一位置编码

此模块是SpaceDrive解决“VLM缺乏3D空间感知”瓶颈的关键。一个预训练的深度估计器 $f_{dep.}$ 从多视图图像中生成逐视图的稠密绝对深度图 $D_k = f_{dep.}(I_k)$，进而通过相机内外参将每个视觉patch反投影到3D空间坐标 $\mathbf{c}_p$。这些坐标随后由统一的PE编码器 $\phi$ 编码为3D位置编码：

$$\phi(\mathbf{c}_p) = [\phi_x(x_p^{3D}), \phi_y(y_p^{3D}), \phi_z(z_p^{3D})] \in \mathbb{R}^{dim} \quad \text{(3)}$$

其中 $\phi_x, \phi_y, \phi_z$ 分别沿三个维度应用正弦-余弦编码。该编码被以加性方式注入到对齐后的视觉token上：

$$\tilde{H}_v = \{\tilde{h}_p\}_{p=1}^N, \quad \tilde{h}_p = h_p + \alpha_{PE} \phi(\mathbf{c}_p) \quad \text{(4)}$$

这里 $\alpha_{PE}$ 是一个可学习的归一化因子，用于调节空间信息与语义特征的融合强度。这一设计使得每个视觉token在保留其2D语义的同时，显式携带了其在3D空间中的度量位置信息，从而解决了现有VLM“仅依赖2D语义进行推理，难以将3D坐标与对应物体准确关联”的根本缺陷。

### 文本坐标的空间化替换

传统的VLM规划器将坐标以逐位数字token的形式嵌入文本提示中，这导致语言模型将数值处理为离散的数字分类问题，忽略了数字标记之间的序数邻近性。SpaceDrive对此进行了根本性改造：检测文本提示中的BEV坐标子串，并用相同的PE编码器 $\phi$ 生成的编码token直接替换这些数字坐标：

$$\tilde{H}_t = \{\tilde{h}_i\}_{i=1}^L, \quad \tilde{h}_i = \begin{cases} \phi(\mathbf{c}_r) & i \in S_r \\ \text{Tokenizer}(t_i) & \text{otherwise} \end{cases} \quad \text{(5)}$$

其中 $S_r$ 是坐标子串的索引集合。BEV坐标的 $z$ 维度置零。这一替换使得文本中的空间信息与视觉token中的空间编码处于同一连续编码空间，为VLM的注意力层提供了统一的跨模态空间关联能力。

### 回归式坐标解码

为解决语言模型在数值预测上的先天不足，SpaceDrive在输出端引入了一个专用的回归解码机制。首先，语言头 $W_{lang}$ 的词汇表被扩展为 $\mathcal{V}' = \mathcal{V} \cup \{\langle\text{IND}\rangle\}$，新增的 $\langle\text{IND}\rangle$ 标识符用于触发坐标解码：

$$y_j = \arg\max_{y \in \mathcal{V}'} (W_{lang}' \mathbf{e}_j)_y \quad \text{(6)}$$

当语言头输出 $y_j = \langle\text{IND}\rangle$ 时，下一个隐藏状态 $\mathbf{e}_{j+1}$ 被路由到一个PE解码器 $\psi$（一个简单的MLP），直接回归出连续的3D坐标：

$$\hat{\mathbf{c}} = \psi(\mathbf{e}_{j+1}), \quad \hat{\mathbf{c}} \in \mathbb{R}^3 \quad \text{(7)}$$

这一机制在保持自回归文本生成连续性的同时，将轨迹路径点的预测从离散数字分类转变为连续坐标回归，从根本上规避了“逐位数字分类导致路径点预测精度低下”的问题。消融实验证实了这一设计的有效性：在Bench2Drive闭环评测中，采用纯文本数字输出的VLM模型（如OmniDrive-L）轨迹退化为近似直线且方向振荡，而SpaceDrive的回归式解码器则能生成平滑、合理的驾驶轨迹（附录C.2）。

### 联合训练目标

训练目标由两部分组成：

$$\mathcal{L} = \mathcal{L}_{LM} + \mathcal{L}_{reg.}(\hat{\mathbf{c}}, \mathbf{c}) \quad \text{(8)}$$

其中 $\mathcal{L}_{LM}$ 是作用于所有文本输出的标准语言建模损失，$\mathcal{L}_{reg.}$ 是作用于所有坐标输出的Huber回归损失。这种联合优化使得模型在保持VLM通用视觉-语言对齐能力的同时，获得精确的3D空间推理与轨迹预测能力。

## 实验与关键发现

### 核心实验设置

SpaceDrive 以 Qwen2.5-VL-7B 为基础 VLM，使用 LoRA（rank=16）微调语言模型部分，冻结视觉编码器和深度估计器。训练目标为语言建模损失与坐标回归 Huber 损失的联合优化（Eq.8）。开环评测遵循 OmniDrive 与 ORION 的协议，闭环评测使用 Bench2Drive 官方协议以确保规划时域、时间采样、足迹膨胀等设置一致。为公平对比，文中区分了“纯 VLM 方法”与“混合范式方法”（后者同时堆叠传统规划模块与 VLM，不可直接对照），并分别报告有无 ego 状态输入的变体（SpaceDrive 与 SpaceDrive+）。

### 开环规划结果（nuScenes）

Table 1 给出了 nuScenes 上的开环规划结果。SpaceDrive+ 在纯 VLM 方法中达到最优：L2 误差 0.32 m，碰撞率 0.23%，交叉率 1.27%。与最强基线 OmniDrive-Q++（L2 0.33 / 碰撞 0.30% / 交叉 3.00%）相比，交叉率下降尤为显著（-1.73 个百分点），表明统一空间位置编码有效减少了轨迹与道路拓扑的语义冲突。值得注意的是，SpaceDrive 未使用 BEV 特征，仅凭统一 PE 注入即达到这一性能，验证了显式 3D 空间编码足以替代稠密 BEV 表征的核心主张。

### 闭环规划结果（Bench2Drive）

Table 2 报告了 Bench2Drive 闭环仿真结果。SpaceDrive+ 取得 78.02 的 Driving Score 和 55.11% 的 Success Rate，在 VLM 方法中位列第二（仅次于 SimLingo）。在闭环设定下，模型需连续输出轨迹并应对动态环境，这对空间推理的稳定性提出了更高要求。附录 C.2 的对比实验进一步揭示：纯文本数字输出的 VLM 模型（如 OmniDrive-L）在闭环中轨迹退化为近似直线且方向振荡，这为第 4.2 节的分析提供了强实证支撑——基于逐位分类的数字坐标输出从根本上不适合闭环驾驶。

### 位置编码消融实验

Table 3 系统消融了三种位置编码注入对规划性能的贡献：

![[assets/figures/papers/paper_list_l2418_https_arxiv_org_abs_2512_10719/figures/006_Table_3.jpg]]
*Table 3: Ablation of positional encoding. Here*

- **视觉 token 注入 φ(c_p)**（Exp.2 vs Exp.1）：L2 误差降低 0.63，碰撞率降低 2.08%，交叉率降低 4.14%。这是单次改动中收益最大的操作，证明在视觉 token 上显式编码 3D 坐标是弥合 2D 语义与 3D 空间鸿沟的关键瓶颈。
- **文本坐标替换 φ(c_r)**（Exp.3 vs Exp.1）：单独使用文本侧 PE 替换数字坐标 token 也能带来增益，但幅度小于视觉侧注入。
- **统一编码 φ(c_p) + φ(c_r)**（Exp.4 vs Exp.1）：同时作用于视觉和文本流时，规划性能进一步提升，且无论是否使用 ego 状态（Exp.6 vs Exp.5），统一编码均带来一致改善。这表明在统一的 PE 空间内，视觉语义与文本坐标形成了有效的跨模态空间关联。
- **ego 历史注入 φ(c_t^ego)**（Exp.7 vs Exp.6）：在 SpaceDrive+ 配置下，加入历史 ego 位置编码进一步降低 L2 和交叉率，但碰撞率略有波动。

### PE 编码器/解码器消融

Table 4 对比了不同 PE 编码器与解码器设计：

![[assets/figures/papers/paper_list_l2418_https_arxiv_org_abs_2512_10719/figures/005_Table_4.jpg]]
*Table 4: Ablation of PE encoder & decoder. Gray indicates that only 4929 out of 5119 output samples are semantically reasonable*

- **正弦-余弦编码器 vs MLP 编码器**（Exp.4 vs Exp.8）：正弦-余弦编码器因平移不变性显著优于全学习 MLP 编码器，L2 误差从 1.96 降至 1.80。这一结果表明，注意力层能够利用编码中的相对位置结构恢复 token 间空间关系，而 MLP 编码器缺乏这种归纳偏置。
- **PE 解码器 vs 直接数值逆映射**（Exp.4 vs Exp.9）：使用专用 PE 解码器回归坐标优于直接从隐藏状态逆映射，后者在 5119 个测试样本中仅 4929 个输出语义合理。
- **PE 归一化因子 α_PE**（Table 5）：移除可学习归一化因子或采用固定缩放均导致性能显著下降（仅 2421/5119 样本语义合理），说明 α_PE 在调节空间信号与语义特征的强度平衡中起关键作用。

![[assets/figures/papers/paper_list_l2418_https_arxiv_org_abs_2512_10719/figures/007_Table_5.jpg]]
*Table 5: Ablation of PE normalization. Gray indicates that only 2421 out of 5119 output samples are semantically reasonable*

### 深度估计器鲁棒性

Table C 消融了深度估计器的影响。在测试时注入深度噪声（±2.5% 全局偏移或随机噪声），性能几乎无下降（L2 保持 1.80），表明 SpaceDrive 利用的是深度提供的 3D 空间结构而非精确深度值。这为方法的实际部署提供了重要保障——无需依赖高精度深度传感器。

### LoRA 配置与基础 VLM 适应性

Table E 的 LoRA rank 消融显示，rank=16 在参数效率和规划精度间达到最优平衡（L2 1.80，碰撞 1.88%，交叉 4.21%）；更高秩虽增加可学习参数，但碰撞和交叉率反而恶化，提示过拟合风险。Table 6 验证了 SpaceDrive 的范式通用性：将其迁移至 LLaVA 和 Qwen-VL 等不同 VLM 基础模型，均能稳定工作并取得竞争性性能。

### 反事实推理与定性分析

Table B 的反事实推理对比表明，SpaceDrive 在无 ego 状态输入下仍保持较高的精确率和召回率，说明其空间推理能力不依赖于自车状态捷径。Figure 3 展示了闭环场景中 SpaceDrive+ 绕行骑行者的多步规划过程——绿色路径点平滑避开红色标记的骑行者，验证了统一 PE 编码在动态避障中的有效性。

![[assets/figures/papers/paper_list_l2418_https_arxiv_org_abs_2512_10719/figures/008_Figure_3.jpg]]
*Figure 3: Qualitative results of closed-loop evaluation on Bench2Drive [25]. Green and pink dots represent path and speed waypoints, respectively. Red circles indicate cyclists ahead that the vehicle needs to avoid. Parameters such as speed and steering wheel angle can be found in the figures*

### 已知局限

1. 开环指标对 ego 状态高度敏感，存在高估真实驾驶能力的风险；闭环评测虽提供补充，但 CARLA V2 仿真真实度有限，与实车部署的现实差距尚未评估。
2. 方法依赖预训练深度估计器提供 3D 几何先验，在极端深度误差或零样本场景下的性能未经验证。
3. 仅采用 LoRA rank=16 微调，可能限制模型对复杂长尾场景的拟合能力。
4. 未引入多帧时序记忆机制，历史 ego 状态仅通过固定长度窗口 PE 注入，可能不足以捕获需要长期依赖的动态交互（如频繁变道或走走停停的拥堵场景）。

## 定位与知识库关联

### 核心瓶颈与设计动机

当前基于视觉语言模型（VLM）的端到端自动驾驶面临两个根本性缺陷：**（1）3D空间感知缺失**——现有VLM缺乏基于3D数据的预训练，仅依赖2D语义进行推理，难以将3D坐标与对应物体和2D语义准确关联，导致场景描述模糊甚至错误；**（2）数值预测机制失配**——语言模型将坐标数值处理为逐位数字分类，忽略了数字标记之间的序数邻近性，且错误地平均了不同数字位的权重，导致路径点预测精度低下。在Bench2Drive闭环评测中，纯文本数字输出的VLM模型（如OmniDrive-L）轨迹退化为近似直线且方向振荡，直接证实了数字逐位输出不适合闭环驾驶（附录C.2）。

SpaceDrive的核心洞察在于：Transformer架构天然适合处理token之间的位置关系；将3D空间关系显式编码为统一的位置编码输入，可让VLM在保持通用视觉-语言对齐的基础上直接进行3D空间推理。

### 方法谱系：VLM自动驾驶规划器的演进定位

SpaceDrive属于**纯VLM基规划器**（VLM-based planner）范畴，与混合范式方法（如VLP、Senna，同时堆叠传统模块与VLM架构）具有本质架构差异，不可直接比较。在纯VLM基方法谱系中，现有工作可分为两个演进阶段：

**第一阶段：隐式空间注入**。以DriveVLM、EMMA、RDA-Driver为代表的早期VLM规划器，主要通过任务特定嵌入或可学习查询隐式注入3D线索，视觉token本身不携带显式空间信息。由于VLM缺乏3D预训练，模型仅能依赖2D语义进行推理，空间定位能力受限。

**第二阶段：文本坐标输出**。以OmniDrive和ORION为代表的方法引入了BEV坐标的文本表示，通过语言模型自回归生成数字坐标。OmniDrive作为SpaceDrive的基线代码库，采用Qwen2.5-VL-7B基础模型，将轨迹规划转化为文本生成任务。然而，这类方法继承了语言模型在数值预测上的先天不足——语言头将每个数字位视为独立分类问题，无法建模数值之间的序数关系。

SpaceDrive代表了**第三阶段：统一显式空间编码**。其关键架构改动体现在三个维度：

1. **坐标表示与接口**：从"文本数字token + 逐位分类式语言头"转变为"统一3D正弦-余弦位置编码 + 回归式PE解码器"。这一改动使坐标不再经过离散化处理，而是以连续编码形式参与注意力计算。

2. **空间信息注入方式**：从"无显式3D信息或仅通过任务特定嵌入隐式注入"转变为"基于深度估计将3D坐标编码直接加到视觉token上，并替换文本中的坐标标记"。视觉token的增强公式为 $\tilde{h}_p = h_p + \alpha_{PE}\phi(\mathbf{c}_p)$，其中 $\phi(\mathbf{c}_p)$ 为统一的3D正弦-余弦位置编码，$\alpha_{PE}$ 为可学习归一化因子。

3. **轨迹输出方式**：从"语言模型自回归逐位生成数字坐标"转变为"在输出⟨IND⟩标识后，由专用PE解码器直接回归3D坐标"。解码公式为 $\hat{\mathbf{c}} = \psi(\mathbf{e}_{j+1}), \hat{\mathbf{c}} \in \mathbb{R}^3$，训练时采用Huber损失进行坐标回归。

### 关键技术决策的消融验证

**统一编码的因果效应**。向视觉token添加空间位置编码后，SpaceDrive的L2误差降低0.63，碰撞率降低2.08%，交叉率降低4.14%（Table 3，Exp.2 vs Exp.1）。当统一位置编码同时作用于视觉和文本坐标流时，无论是否使用ego状态，规划性能均得到进一步提升（Exp.4 vs Exp.1；Exp.6 vs Exp.5）。这一结果证实了统一编码空间对联合空间推理的关键作用。

**编码器设计的平移不变性**。正弦-余弦编码器因天然具备平移不变性，优于全学习MLP编码器，L2误差从1.96降至1.80（Table 4，Exp.4 vs Exp.8）。这表明模型依赖的是token之间的相对空间关系而非绝对位置记忆，与Transformer注意力机制的归纳偏置一致。

**对深度噪声的鲁棒性**。在测试时注入深度噪声（±2.5%全局偏移/随机噪声）对性能影响极小（Avg. L2保持1.80），证明方法利用的是3D空间结构而非精确深度值。这一特性降低了方法对深度估计器精度的依赖。

### 适用边界与局限

1. **开环评估的高估风险**：开环规划评估对ego状态高度敏感，所报告的指标存在高估模型真实驾驶能力的风险。尽管通过Bench2Drive闭环评测进行了补充，但闭环场景的多样性和随机性仍有局限。

2. **深度估计器的依赖**：方法依赖预训练深度估计器提供3D几何先验。虽然实验显示对深度噪声具有鲁棒性，但在极端深度误差或零样本场景下的性能未经验证。

3. **微调策略的容量限制**：目前仅采用低秩适配（LoRA rank=16）进行VLM微调，虽然参数高效，但可能限制模型对复杂长尾场景的拟合能力。消融实验显示rank=16在参数效率和规划精度之间达到最优平衡，更高秩导致碰撞和交叉率恶化（Table E），但这一结论可能受限于当前基础模型规模。

4. **时序建模的缺失**：未引入多帧时序记忆机制，历史ego状态仅通过固定长度窗口的PE注入，可能不足以捕获需要长期依赖的动态交互，例如频繁变道或走走停停的拥堵场景。

5. **仿真到现实的差距**：闭环仿真基于CARLA V2，仿真真实度有限，与实际车载部署的现实差距尚未评估。

### 开放问题

1. **跨任务泛化性**：该空间感知范式能否推广到其他3D视觉-语言任务（如机器人操作或室内导航）？统一的PE是否需要任务特定的频率调整？

2. **模型规模扩展**：如果采用更强大的VLM基础模型（如Qwen2.5-VL-72B），仅用LoRA微调是否仍然足够？全参数微调会带来多大增益？Table 6已初步验证了不同VLM基础（LLaVA、Qwen-VL）的适应性，但更大规模模型的边际收益未知。

3. **动态交互增强**：如何将动态物体的运动流（速度、加速度）也编码为统一的时空PE，以增强对动态交互的理解？当前方法仅编码静态3D位置，无法显式建模物体的运动状态。

4. **上游推理能力反哺**：在端到端模型直接生成规划轨迹之外，这种显式的3D空间感知能否反向提升VLM在场景问答、风险预估等上层推理任务中的性能？

5. **归一化因子优化**：如何量化归一化因子 $\alpha_{PE}$ 的最优范围，并将其推广到不同深度估计器和分辨率配置？Table 5的消融显示PE归一化对语义合理性有显著影响（仅2421/5119输出样本语义合理），但最优策略仍待系统探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/SpaceDrive_Infusing_Spatial_Awareness_into_VLM_based_Autonomous_Driving.pdf]]
