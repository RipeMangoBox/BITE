---
title: "Spatial-SSRL: Enhancing Spatial Understanding via Self-Supervised Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Spatial_SSRL_Enhancing_Spatial_Understanding_via_Self_Supervised_Reinforcement_Learning.pdf
project_link: null
code_link: "https://huggingface.co/datasets/internlm/Spatial-SSRL-81k"
huggingface_link: "https://huggingface.co/internlm/Spatial-SSRL-7B"
aliases:
- SS
- Spatial-SSRL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 利用普通RGB/RGB-D图像的内在结构一致性作为自监督可验证奖励信号，使模型能够通过强化学习自主提升空间推理能力，无需外部工具或标注。
primary_logic: 将视觉自监督学习（SSL）任务重塑为RLVR的可验证奖励函数，实现了从原始图像到空间理解的有效学习迁移，突破了传统监督的瓶颈，在保持可扩展性的同时显著提升了LVLM的3D空间智能。
claims:
- Spatial-SSRL自动构建五种前预任务：混洗补丁重排、翻转补丁识别、裁剪补丁修复、区域深度排序和相对3D位置预测，以捕获2D和3D空间结构。
- 在七个空间理解基准上，Spatial-SSRL（3B和7B）相比Qwen2.5-VL基线分别平均提升4.63%和3.89%。
- 所有任务标注均从图像结构确定性地推导，无需人工或LLM标注，实现了100%真值准确性。
- 基线模型在生成显式推理链时性能下降，而Spatial-SSRL通过自监督RL学会了有效的空间推理，避免了虚假相关性。
---

# Spatial-SSRL: Enhancing Spatial Understanding via Self-Supervised Reinforcement Learning

> [!tip] 核心洞察
> 将视觉自监督学习（SSL）任务重塑为RLVR的可验证奖励函数，实现了从原始图像到空间理解的有效学习迁移，突破了传统监督的瓶颈，在保持可扩展性的同时显著提升了LVLM的3D空间智能。

| 字段 | 内容 |
|------|------|
| 中文题名 | Spatial-SSRL: 基于自监督强化学习的空间理解增强 |
| 英文题名 | Spatial-SSRL: Enhancing Spatial Understanding via Self-Supervised Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.27606) · [HuggingFace](https://huggingface.co/internlm/Spatial-SSRL-7B) · [HuggingFace](https://huggingface.co/datasets/internlm/Spatial-SSRL-81k) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | Spatial-SSRL |
| Dataset | 7 Spatial Benchmarks, Spatial457, VSI-Bench, General VQA |

> [!tip] 效果简介
> - 7 Spatial Benchmarks (Avg) 上，平均准确率 Spatial-SSRL-3B vs Qwen2.5-VL-3B (w/o reasoning) (+4.63%)；平均准确率 Spatial-SSRL-7B vs Qwen2.5-VL-7B (w/o reasoning) (+3.89%)。
> - Spatial457 上，准确率 Spatial-SSRL-3B vs Qwen2.5-VL-3B (+12.37%)。
> - VSI-Bench 上，准确率 Spatial-SSRL-3B vs Qwen2.5-VL-3B (+5.65%)。

## 概要

### 问题与瓶颈

大型视觉语言模型（LVLM）在空间理解任务上的现有范式依赖昂贵的外部监督信号——包括人工标注、专有模型（如GPT-4V）以及仿真环境生成的数据。这类外源监督不仅推高了数据构建成本，还限制了可扩展性与领域覆盖范围，成为LVLM空间智能提升的核心瓶颈。

### 核心思想

Spatial-SSRL提出了一种根本性的范式转换：**将视觉自监督学习（SSL）的前置任务重塑为强化学习可验证奖励（RLVR）的奖励函数**。其关键洞察在于，普通RGB/RGB-D图像本身蕴含丰富的2D布局与3D深度结构信息，这些内在结构可以作为确定性的、无需外部标注的验证信号，驱动模型通过强化学习自主习得空间推理能力。如图2所示，该方法以内在自监督取代了传统范式中的外源工具依赖，构建了一条可扩展、轻量、低成本且天然可验证的训练管线。

### 方法定位

Spatial-SSRL并非提出新的模型架构，而是**在训练范式层面进行创新**。其核心改变体现在四个关键槽位：

- **训练数据源**：从原始图像自动构建自监督问答对，取代人工标注或工具生成的QA对；
- **训练目标**：采用GRPO强化学习配合可验证奖励，取代传统的监督交叉熵损失；
- **奖励信号**：使用自监督确定性的二元/标量奖励，无需外部验证器或程序；
- **可扩展性**：仅需普通RGB/RGB-D图像即可大规模扩展，突破了标注成本与仿真真实度的限制。

方法自动构建五种互补的前置任务——混洗补丁重排、翻转补丁识别、裁剪补丁修复、区域深度排序和相对3D位置预测——分别捕获2D空间结构与3D深度关系，所有标注均从图像结构确定性地推导，实现了100%真值准确性。

### 主要结果

在七个空间理解基准上，Spatial-SSRL相较Qwen2.5-VL基线取得了显著且一致的提升：3B模型平均提升**4.63%**，7B模型平均提升**3.89%**。其中在Spatial457基准上增益最为突出，7B模型达到**+8.67%**，3B模型达到**+12.37%**。更重要的是，基线模型在启用显式推理链时性能反而下降（Qwen2.5-VL-3B从45.91%降至44.85%），而Spatial-SSRL通过自监督RL学会了有效的空间推理，避免了虚假相关性。同时，通用视觉问答能力保持稳定并略有提升（3B平均+2.02%），表明空间能力的增强并未以牺牲通用视觉能力为代价。在跨架构验证中，基于Qwen3-VL-4B的Spatial-SSRL同样实现了空间理解平均+1.29%、通用VQA平均+1.18%的增益，验证了方法的架构无关性。

大型视觉语言模型（LVLM）在通用视觉理解上取得了显著进展，然而在需要精确3D空间推理的任务中，其表现仍远未令人满意。空间理解——判断物体间的相对位置、方向、距离与布局——是具身智能、自动驾驶和机器人操作等下游应用的基础能力，但现有LVLM在此类任务上频繁出现方向混淆、深度误判和布局错乱等系统性错误。

当前提升LVLM空间理解的主流范式存在一个根本性瓶颈：**对外部监督的严重依赖**。如图Figure 2(a)所示，现有方法通常通过以下途径注入空间知识：

- **人工标注**：构建包含空间关系问答的大规模数据集，成本高昂且难以覆盖长尾场景。
- **专有模型蒸馏**：借助GPT-4V等闭源强模型生成空间推理链，引入知识产权风险与不可控的标注噪声。
- **仿真环境合成**：在3D引擎中渲染合成数据，面临仿真到真实（sim-to-real）的域迁移问题，且场景多样性受限。

这些外源监督范式共同导致了一个恶性循环：**可扩展性差 → 成本高 → 领域覆盖有限**。每当需要适配新的视觉域或空间概念，就不得不重复昂贵的标注或仿真流程，使得空间理解能力的持续提升陷入瓶颈。

本文的核心洞察在于：**普通RGB/RGB-D图像本身蕴含丰富的内在空间结构，这些结构可以作为自监督可验证的奖励信号，驱动模型自主习得空间推理能力，从而彻底摆脱对外部监督的依赖**。具体而言，图像中的补丁排列顺序、翻转对称性、遮挡修复一致性、区域深度排序以及物体间相对位置，均是从图像结构本身可确定性地推导出的真值，无需任何人工标注或工具辅助。

基于这一洞察，Spatial-SSRL提出了一种**自监督强化学习范式**（Figure 2(b)），将视觉自监督学习（SSL）的前预任务重塑为强化学习可验证奖励（RLVR）的奖励函数。该方法仅需原始RGB/RGB-D图像作为输入，自动构建五种覆盖2D布局与3D深度结构的可验证问答对，通过组相对策略优化（GRPO）训练模型生成空间推理链。这一范式实现了从“依赖昂贵外源监督”到“利用内源自监督信号”的根本性转变，在保持高度可扩展性的同时，显著提升了LVLM的3D空间智能。

## 核心方法与创新机理

Spatial-SSRL的核心创新在于**将视觉自监督学习（SSL）任务重塑为强化学习可验证奖励（RLVR）的信号源**，从而彻底绕过了LVLM空间理解对昂贵外部监督的依赖。这一范式转换通过以下四个关键“changed slots”实现：

### 1. 训练数据源：从人工标注到图像结构自生成

传统方法依赖人工标注或专有模型（如GPT-4V）生成的QA对，成本高昂且覆盖领域有限。Spatial-SSRL直接从原始RGB/RGB-D图像中**确定性地推导**出所有监督信号——数据构建完全自动化，无需任何人工标注或LLM参与，实现了100%的真值准确性。数据集Spatial-SSRL-81k仅需普通图像即可大规模扩展，从根本上解决了空间理解数据匮乏的瓶颈。

### 2. 训练目标：从监督微调到GRPO强化学习

不同于传统的监督交叉熵损失，Spatial-SSRL采用**Group Relative Policy Optimization（GRPO）** 进行策略优化。模型在少量SFT冷启动（约3,600样本，占全数据集4.4%）后，通过可验证奖励函数进行RL训练。这种设计使模型能够主动探索空间推理策略，而非被动拟合标注答案。

### 3. 奖励信号：从外部验证器到自监督确定性奖励

每个前预任务被构造为QA提示，其答案可从图像结构中确定性验证。奖励函数由两部分加权组成：准确度奖励（$r_{\text{acc}}$，答案完全匹配真值时为1）和格式奖励（$r_{\text{fmt}}$，确保输出符合$\langle\text{think}\rangle\ldots\langle\text{/think}\rangle$和$\boxed{}$结构），最终奖励为$r = 0.9 \cdot r_{\text{acc}} + 0.1 \cdot r_{\text{fmt}}$。这种**内源可验证性**无需任何外部工具或专有模型评判，使RL训练完全自给自足。

### 4. 可扩展性：从仿真/标注受限到无上限扩展

传统方法受限于仿真环境真实度或人工标注成本，而Spatial-SSRL仅需普通RGB/RGB-D图像即可生成训练数据。这一特性使其能够轻松利用大规模图像数据集（如COCO、DIODE、MegaDepth），实现了空间理解训练的真正可扩展性。

### 核心洞察：SSL任务作为RLVR的桥梁

上述四个changed slots共同指向一个核心洞察：**视觉SSL任务天然具备可验证性**——补丁重排的真值是逆置换、翻转检测的真值是翻转类型、深度排序的真值由深度图确定。Spatial-SSRL的关键贡献不在于设计新的SSL任务本身，而在于认识到这些任务可以充当RLVR的可验证奖励函数，从而在自监督表征学习和空间推理能力之间架起了一座可扩展的桥梁。这一洞察使得模型能够从原始图像中自主学习空间结构，而无需任何外部监督信号。

### 推理能力的质变

一个值得注意的现象是：基线模型（Qwen2.5-VL）在启用思维链推理时性能反而下降（3B从45.91%降至44.85%），表明其缺乏真正的空间推理能力，仅依赖表面统计相关性。相比之下，Spatial-SSRL通过GRPO训练学会了有效的空间推理策略，在带推理的评估设置下**持续超越**不带推理的基线模型。这证明RLVR训练赋予了模型真正的空间推理能力，而非简单的模式匹配。

Spatial-SSRL 的整体框架由两个核心阶段构成：**自监督任务生成（Self-Supervised Task Design）** 与 **强化学习优化（Reinforcement Learning）**，二者通过可验证奖励函数紧密耦合，形成一个从原始图像到空间理解能力的端到端学习闭环。

### 阶段一：自监督数据构建

框架的第一阶段从普通 RGB 或 RGB-D 图像出发，自动构建五类前预任务（pretext tasks），无需任何人工标注或外部专有模型。这五类任务按监督信号来源分为两大类别：

- **深度无关任务（Depth-free Tasks）**：仅依赖 RGB 图像，捕获 2D 空间结构。包括混洗补丁重排（Shuffled Patch Reordering）、翻转补丁识别（Flipped Patch Recognition）和裁剪补丁修复（Cropped Patch Inpainting）。
- **深度相关任务（Depth-based Tasks）**：利用深度图提供 3D 监督信号。包括区域深度排序（Regional Depth Ordering）和相对 3D 位置预测（Relative 3D Position Prediction）。

每类任务被设计为可验证的问答对：给定输入图像（或经过变换的图像），模型需输出一个确定性的答案，而真值答案完全由图像本身的结构确定性地推导得出。例如，混洗补丁重排的真值是置换的逆映射 $\pi^{-1}$；区域深度排序的真值由深度图中三个区域的相对距离决定，并通过深度范围约束 $r(R_i) < r_{max}$ 和深度间隙约束 $d(R_i, R_{i+1}) > d_{min}$ 保证标注无歧义。这种设计使得生成的 **Spatial-SSRL-81k** 数据集达到 100% 的真值准确率。

### 阶段二：强化学习优化

第二阶段将上述自监督任务转化为强化学习的奖励信号，对基础视觉语言模型进行优化。具体流程如下：

1. **SFT 冷启动（Cold Start）**：在约 3,600 个样本（约占全数据集的 4.4%）上进行短暂的监督微调，使模型熟悉任务格式和输出结构，稳定后续 RL 训练。
2. **GRPO 策略优化**：采用分组相对策略优化（Group Relative Policy Optimization, GRPO），以可验证奖励函数驱动模型更新。奖励函数由两部分加权组成：
   - **准确度奖励** $r_{\text{acc}}$：当模型预测答案与真值完全匹配时为 1，否则为 0。
   - **格式奖励** $r_{\text{fmt}}$：鼓励模型遵循指定的输出格式（如 `⟨think⟩...⟨/think⟩` 和 `\boxed{}`）。
   
   总体奖励为 $r = 0.9 \cdot r_{\text{acc}} + 0.1 \cdot r_{\text{fmt}}$。

### 输入输出流与模块关系

整个 pipeline 的输入输出流可概括为：

```
原始图像 (RGB/RGB-D)
    │
    ▼
[自监督任务生成] ─── 五类可验证 QA 对 ───► Spatial-SSRL-81k 数据集
    │
    ▼
[SFT 冷启动] ─── 格式适配
    │
    ▼
[GRPO 强化学习] ◄─── 可验证奖励 (准确度 + 格式)
    │
    ▼
Spatial-SSRL 模型 ─── 空间理解推理
```

在推理阶段，模型使用与训练一致的格式提示进行结构化推理，确保训练与评估的一致性。值得注意的是，基线模型在直接生成推理链时性能反而下降（Qwen2.5-VL-3B 从 45.91% 降至 44.85%），而 Spatial-SSRL 通过自监督 RL 学会了有效的空间推理，避免了虚假相关性，在所有基准上均保持推理带来的正向增益。

### 核心设计优势

与依赖外部监督（人工标注、专有模型、仿真环境）的传统范式相比，Spatial-SSRL 框架的关键突破在于将视觉自监督学习的任务重塑为 RLVR（Reinforcement Learning with Verifiable Rewards）的可验证奖励函数。这实现了三个层面的提升：

- **可扩展性**：仅需普通 RGB/RGB-D 图像，数据构建完全自动化。
- **低成本**：无需人工标注或调用外部模型 API。
- **确定性监督**：所有标注从图像结构确定性地推导，消除标注噪声。

![[assets/figures/papers/paper_list_l2725_https_arxiv_org_abs_2510_27606/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Spatial-SSRL. (a) Self-supervised data curation: from raw RGB and RGB-D images, we automatically construct five pretext tasks (patch reordering, patch flip detection, cropped-patch inpainting, regional depth ordering, and relative 3D position prediction), requiring no human or LLM annotations. (b) RL training: the model is optimized with Group Relative Policy Optimization (GRPO) using a verifiable reward function that evaluates answer correctness, and a format reward that elicits format compliance*

![[assets/figures/papers/paper_list_l2725_https_arxiv_org_abs_2510_27606/figures/002_Figure_2.jpg]]
*Figure 2: (a) Prior pipelines boost spatial understanding by injecting extrinsic supervision from expert tools or synthetic environments, which inflates cost and limits scalability. (b) Our Spatial-SSRL replaces these dependencies with intrinsic self-supervision, yielding a scalable, lightweight, low-cost, and naturally verifiable pipeline*

Spatial-SSRL 的核心由两大阶段构成：自监督任务设计与强化学习优化。本节聚焦于五个前预任务的数学构造与可验证奖励机制，揭示如何从原始图像中确定性推导出训练监督信号。

### 3.1 自监督任务设计总览

五个前预任务按监督信号来源分为两类：**深度无关任务**（仅需 RGB 图像，捕获 2D 空间结构）与**深度相关任务**（需 RGB-D 图像，捕获 3D 空间结构）。所有任务的标注均从图像结构确定性推导，无需人工或 LLM 标注，实现 100% 真值准确率。

### 3.2 深度无关任务

#### 3.2.1 混洗补丁重排 (Shuffled Patch Reordering)

将图像均匀划分为 $M \times N$ 个补丁，施加随机置换 $\pi$ 打乱顺序。模型需恢复原始排列，真值为逆置换：

$$\pi^{-1} = [\pi^{-1}(0), \pi^{-1}(1), \ldots, \pi^{-1}(M \times N - 1)]$$

由于 $\pi$ 是双射，其逆置换存在且唯一确定。该任务迫使模型理解全局 2D 布局一致性和相对位置关系。

#### 3.2.2 翻转补丁识别 (Flipped Patch Recognition)

从 $M \times N$ 网格中随机选取一个补丁 $\hat{x}_t$，以等概率施加垂直或水平翻转：

$$\left\{ \begin{array}{ll} x_{\mathrm{vert}}, & \mathrm{with~probability~}0.5, \\ x_{\mathrm{horz}}, & \mathrm{with~probability~}0.5, \end{array} \right.$$

模型需判断该补丁是否被翻转以及翻转类型。此任务增强模型对镜像对称和局部方向线索的敏感性。

#### 3.2.3 裁剪补丁修复 (Cropped Patch Inpainting)

从图像中随机裁剪一个正方形区域 $\mathcal{R}$，其左上角坐标均匀采样：

$$(x_0, y_0) \sim \mathcal{U}([0, H - s] \times [0, W - s])$$

构造带掩码的输入图像，将裁剪区域置零：

$$I_{\mathrm{input}}(u, v) = \left\{ \begin{array}{ll} 0, & (u, v) \in \mathcal{R}, \\ I(u, v), & \mathrm{otherwise}. \end{array} \right.$$

模型需从多个候选补丁中选出原始裁剪内容，这要求理解局部纹理与全局上下文的对应关系。

### 3.3 深度相关任务

#### 3.3.1 区域深度排序 (Regional Depth Ordering)

给定 RGB 图像 $I$ 及其归一化深度图 $D$，选取三个不相交区域 $R_1, R_2, R_3$，使深度递增（$R_1$ 最近，$R_3$ 最远）。区域选择满足两个约束：

**深度范围约束**，保证区域内深度一致性：

$$r(R_i) = \max_{(x,y)\in R_i} D(x,y) - \min_{(x,y)\in R_i} D(x,y) < r_{max}$$

**深度间隙约束**，保证相邻区域间无歧义分离：

$$d(R_i, R_{i+1}) = \min_{(x,y)\in R_{i+1}} D(x,y) - \max_{(x,y)\in R_i} D(x,y) > d_{min}$$

模型需对三个区域按由近及远排序，真值由深度图直接计算。

#### 3.3.2 相对 3D 位置预测 (Relative 3D Position Prediction)

给定两个物体在相机坐标系下的 3D 位置 $(x_1, z_1)$ 和 $(x_2, z_2)$（$z$ 为深度轴，$x$ 为水平轴），将目标点变换到对象 1 的自我中心坐标系。先平移再旋转：

$$\begin{bmatrix} \tilde{x}_2 \\ \tilde{z}_2 \\ 1 \end{bmatrix} = \begin{bmatrix} \cos\theta & \sin\theta & 0 \\ -\sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 0 & -x_1 \\ 0 & 1 & -z_1 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x_2 \\ z_2 \\ 1 \end{bmatrix}$$

其中 $\theta$ 为对象 1 的朝向角。变换后，根据 $\tilde{x}_2, \tilde{z}_2$ 的符号与阈值判定空间关系：

沿 $x$ 轴（左右）：

$$\tilde{p}_x = \begin{cases} \mathrm{Right}, & \tilde{x}_2 > \delta_x \\ \mathrm{Left}, & \tilde{x}_2 < -\delta_x \\ \mathrm{None}, & \mathrm{otherwise} \end{cases}$$

沿 $z$ 轴（前后）：

$$\tilde{p}_z = \begin{cases} \mathrm{Front}, & \tilde{z}_2 > \delta_z \\ \mathrm{Back}, & \tilde{z}_2 < -\delta_z \\ \mathrm{None}, & \mathrm{otherwise} \end{cases}$$

阈值 $\delta_x, \delta_z$ 确保空间分离无歧义。该任务要求模型进行心理旋转和自我中心坐标变换，整合朝向线索与深度信息。

### 3.4 可验证奖励函数

每个任务以问答提示形式呈现给 LVLM，确定性验证器产生二元或标量奖励。准确度奖励 $r_{acc}=1$ 当且仅当模型预测答案与真值完全匹配。格式奖励 $r_{fmt}$ 鼓励遵循 $\langle$think$\rangle$...$\langle$/think$\rangle$ 和 $\backslash$boxed\{\} 的结构化输出。最终奖励为加权组合：

$$r = 0.9 \cdot r_{acc} + 0.1 \cdot r_{fmt}$$

此设计将视觉自监督学习任务重塑为 RLVR 的可验证奖励函数，实现了从原始图像结构到空间理解能力的有效学习迁移。

## 实验与关键发现

### 主实验结果：空间理解基准

Spatial-SSRL 在七个空间理解基准上对 Qwen2.5-VL 基线实现了跨规模的稳定提升，涵盖图像和视频两种设置。**Table 1** 给出了以 Qwen2.5-VL 为基线的完整结果。

![[assets/figures/papers/paper_list_l2725_https_arxiv_org_abs_2510_27606/figures/004_Table_1.jpg]]
*Table 1: Performance of Qwen2.5-VL-based models on spatial understanding benchmarks. The open-source models and our model are evaluated on seven benchmarks, and the average results are provided in the last column. For a comprehensive comparison, we test two settings of the baseline model: one that does not generate the reasoning process and one that does. We compute the improvements based on the results of our models and the baseline models without reasoning. The qualitative analysis of some cases is shown in Appendix C*

**Qwen2.5-VL 基线上的提升**（不含推理链的基线为比较对象）：
- **Spatial-SSRL-3B**：七个基准平均准确率提升 **+4.63%**。其中 **Spatial457** 提升最为显著，达 **+12.37%**；**VSI-Bench** 提升 **+5.65%**。这表明小模型从自监督空间预训练中获益尤为突出。
- **Spatial-SSRL-7B**：平均提升 **+3.89%**，最大单项提升同样出现在 Spatial457，达 **+8.67%**。

**推理链的影响**是一个关键发现。Qwen2.5-VL-3B 基线在启用显式推理链（CoT）后，平均准确率从 45.91% *下降*至 44.85%——说明未经空间训练的模型强行生成空间推理时容易引入虚假相关性。相比之下，Spatial-SSRL 模型在推理模式下在所有基准上均稳定超越无推理基线，证明 GRPO 阶段学到的结构化推理是有效且可靠的。

**跨架构泛化**：在 Qwen3-VL 架构上的实验（**Table 2**）进一步验证了方法的通用性。Spatial-SSRL-4B 在空间理解基准上同样取得一致提升，具体数值见 **Table 9**（附录）。

### 通用视觉能力：无灾难性遗忘

空间专项训练未损害模型的通用视觉能力。**Table 3** 将评估分为通用 VQA 和 OCR/图表理解两类：
- **通用 VQA**：Spatial-SSRL-3B 平均提升 **+2.02%**，7B 提升 +0.57%。其中相对位置预测任务的自我中心坐标变换可能迁移到了通用推理（详见消融分析）。
- **OCR 与图表理解**：性能保持稳定，未出现明显退化。

![[assets/figures/papers/paper_list_l2725_https_arxiv_org_abs_2510_27606/figures/006_Table_3.jpg]]
*Table 3: General visual capability comparisons. The benchmarks are organized into two categories: General VQA and OCR and Chart Understanding. The first category covers a wide range of fundamental visual capabilities, such as knowledge application, and hallucination recognition, multi-image understanding, etc. The second category targets the understanding of images with charts or rich textual details. The average accuracy of both categories are computed and provided*

在 Qwen3-VL 架构上，Spatial-SSRL-4B 的通用 VQA 平均提升为 **+1.18%**（**Table 10**）。

### 任务消融：五种前预任务的协同效应

**Table 4** 报告了基于 Qwen2.5-VL-7B 的任务消融结果，揭示以下关键规律：

**全任务组合最优**。同时使用全部五种任务训练的模型在七个基准中的四个上取得最佳性能，证明任务间存在显著的协同效应——2D 布局理解（来自深度无关任务）与 3D 深度推理（来自深度相关任务）互补增强空间智能。

**深度相关 vs. 深度无关的分工**：
- 在 **3DSR** 的三个子集上，深度相关任务（区域深度排序 + 相对位置预测）平均准确率达 **61.45%**，明显高于深度无关任务（混洗补丁重排 + 翻转补丁识别 + 裁剪补丁修复）的 **57.99%**。这符合预期：3D 空间推理天然需要深度信息。
- 深度无关任务在 2D 布局密集型基准上表现更强：**混洗补丁重排**在 2D 空间布局和推理任务上表现突出；**翻转补丁识别**在迷宫推理（maze reasoning）中取得最强性能，说明其对方向敏感性的增强效果。

**单任务的差异化贡献**：
- **区域深度排序**在 3D 高度理解任务上性能最强，直接受益于其深度排序监督信号。
- **相对位置预测**在通用 VQA 和多目标推理上表现最佳。这一迁移效应可能源于自我中心坐标变换所需的心理旋转和视角采择能力，这些能力与通用推理共享认知基础。

### 失败模式与局限性

尽管整体提升显著，实验揭示了若干值得关注的局限：

1. **视频空间推理增益有限**。模型训练仅使用静态图像（RGB/RGB-D），在视频基准 VSI-Bench 上 7B 模型的提升仅为 **+1.21%**，远低于部分图像基准。这表明时序空间推理需要视频原生的自监督任务设计（如光流预测、时序一致性）。

2. **数据源对深度任务的约束**。区域深度排序和相对位置预测依赖 RGB-D 数据（来自 DIODE 和 MegaDepth），限制了从纯 RGB 图像（如 COCO）扩展训练规模的能力。纯 RGB 图像仅用于三个深度无关任务，导致深度相关任务的训练数据量相对受限（各任务数据量见 **Table 5**）。

3. **通用 VQA 的个别波动**。虽然整体趋势为正，但在 HallusionBench 等幻觉检测基准上提升幅度较小（3B：38.14% → 40.20%），部分指标存在波动。这提示自监督空间训练对幻觉鲁棒性的影响需要更大规模验证。

4. **任务覆盖范围**。当前五种前预任务主要覆盖 2D 布局和基础 3D 空间关系，尚未涉及物理交互、时序因果推理等更复杂的空间智能维度。

### 关键图表结论总结

- **Figure 1**：定性展示基线模型在 3D 位置和方向判断上的错误（红色）与 Spatial-SSRL 的正确预测（绿色），配合七基准定量提升，构成论文的核心证据链。
- **Figure 2**：范式对比——传统方法依赖外部监督（专家工具、仿真环境），成本高且可扩展性差；Spatial-SSRL 以图像内在结构作为自监督信号，实现可扩展的轻量级方案。
- **Table 1/Table 4**：分别提供主实验和消融的完整数据，是支撑“自监督 RL 有效提升空间理解”这一核心主张的量化基础。

![[assets/figures/papers/paper_list_l2725_https_arxiv_org_abs_2510_27606/figures/007_Table_4.jpg]]
*Table 4: Task ablation on benchmark subsets. Each row represents a training configuration and its performance across seven evaluation dimensions. All models are trained based on Qwen2.5-VL-7B. The five columns under training tasks illustrate the tasks used for each setting. Gnr-VQA averages the four general VQA benchmarks from Tab. 3. Spatial subtasks are tested on the subsets of the spatial benchmarks in Tab. 1. Bold indicates best performance; double-underline and underline indicate second and third best*

![[assets/figures/papers/paper_list_l2725_https_arxiv_org_abs_2510_27606/figures/001_Figure_1.jpg]]
*Figure 1: We present Spatial-SSRL, a self-supervised reinforcement learning paradigm for spatial understanding. (a) Qualitative examples: the baseline answers are wrong (red), whereas our model predicts correctly (green) for 3D locations and orientations. (b) Quantitative results on seven spatial benchmarks show consistent improvements of Spatial-SSRL-7B against Qwen2.5-VL-7B and its CoT variant*

## 定位与知识库关联

### 核心范式转换：从外源监督到内源自监督

LVLM空间理解能力的提升长期依赖外部监督信号的注入。如图2所示，现有范式可归为两条路径：其一利用**专有模型或专家工具**生成空间标注（如3D定位框、深度图、场景图），再通过监督微调将知识蒸馏至LVLM；其二借助**仿真环境**合成大规模空间推理数据，以可控方式提供真值监督。这两种路径虽有效，却共同受制于**标注成本高、领域覆盖窄、可扩展性差**的瓶颈——人工标注难以穷举开放世界的空间关系，仿真环境则面临sim-to-real的分布偏移与场景多样性不足。

Spatial-SSRL的方法论创新在于**将视觉自监督学习（SSL）的前预任务重塑为可验证的强化学习奖励函数**，从根本上切断了对外部监督的依赖。其核心洞察是：普通RGB/RGB-D图像内在的结构一致性（如补丁排列、翻转对称性、深度顺序、自我中心坐标变换）天然构成一组确定性可验证的空间推理问题，无需任何人工标注或专有模型即可生成100%准确的真值标签。这一设计使得空间理解能力的获取从“监督蒸馏”转向“自主探索”，在保持可扩展性的同时实现了显著的性能提升。

### 与基线的结构性差异

**监督信号来源**：基线模型（如Qwen2.5-VL、Qwen3-VL）的空间推理能力主要来自预训练阶段的海量图文对齐与有限的监督微调。Spatial-SSRL在此基础上引入了**自监督可验证奖励**作为额外的训练信号，使模型能够通过GRPO强化学习自主发现空间规律。关键差异在于：基线的空间知识来自“被告知”（监督标签），而Spatial-SSRL的空间知识来自“自己验证”（自监督RL）。

**训练目标**：基线采用标准的**监督交叉熵损失**优化下一个token的预测概率；Spatial-SSRL则采用**GRPO强化学习**，以二元/标量可验证奖励（准确度奖励$r_{\text{acc}}$与格式奖励$r_{\text{fmt}}$的加权组合$r = 0.9 \cdot r_{\text{acc}} + 0.1 \cdot r_{\text{fmt}}$）替代交叉熵，使模型在策略空间中自主搜索正确答案。这一转变的关键意义在于：模型不再被强制拟合某一特定答案分布，而是通过试错学习空间推理的通用策略。

**推理链行为**：一个值得关注的对比现象是，Qwen2.5-VL基线在显式生成推理链时性能反而下降（3B从45.91%降至44.85%），表明未经专门训练的LVLM在空间推理中容易产生虚假相关性；而Spatial-SSRL通过自监督RL学会了有效的结构化推理，带推理链的模型在所有基准上一致优于无推理基线。这暗示自监督RL不仅提升了答案准确率，更塑造了模型的空间推理能力本身。

### 任务设计的互补性与协同机制

五种自监督前预任务覆盖了2D和3D空间理解的两个维度：

**深度无关任务**（仅需RGB）：
- **混洗补丁重排**：通过恢复被随机置换的补丁顺序，迫使模型学习全局2D布局一致性和相对位置关系。真值为逆置换$\pi^{-1} = [\pi^{-1}(0), \pi^{-1}(1), \ldots, \pi^{-1}(M \times N - 1)]$。
- **翻转补丁识别**：对单个补丁随机施加垂直或水平翻转（$\check{x}_t^{\text{flip}} \in \{x_{\text{vert}}, x_{\text{horz}}\}$，各50%概率），要求模型检测翻转类型，强化对镜像对称性和局部方向线索的敏感性。
- **裁剪补丁修复**：从图像中随机裁剪区域（左上角坐标$(x_0, y_0) \sim \mathcal{U}([0, H - s] \times [0, W - s])$），对裁剪区域置零构造掩码输入$I_{\text{input}}$，要求模型从候选补丁中识别原始内容，训练跨视图对应能力。

**深度相关任务**（需RGB-D）：
- **区域深度排序**：选取三个满足深度范围约束$r(R_i) < r_{max}$和深度间隙约束$d(R_i, R_{i+1}) > d_{min}$的互不相交区域，要求模型按距相机远近排序，强化3D高度理解。
- **相对3D位置预测**：通过自我中心坐标变换（平移后旋转：$\begin{bmatrix} \tilde{x}_2 \\ \tilde{z}_2 \\ 1 \end{bmatrix} = \mathbf{R}_\theta \mathbf{T}_{-p_1} \begin{bmatrix} x_2 \\ z_2 \\ 1 \end{bmatrix}$），将目标点变换到参照对象的坐标系，再根据阈值$\delta_x, \delta_z$判定左右/前后关系，训练心理旋转和视角转换能力。

消融实验（Table 4）揭示了任务间的**协同效应**：训练全部五种任务的模型在七个基准中的四个上取得最佳性能。深度相关任务在3DSR子集上平均准确率达61.45%，显著高于深度无关任务的57.99%，但两类任务互补——混洗补丁重排擅长2D空间布局推理，翻转补丁识别在迷宫推理中表现最强，区域深度排序强化3D高度理解，相对位置预测则通过自我中心坐标变换迁移至通用视觉问答。这表明空间理解是一个多面能力，需要2D布局、方向敏感性和3D深度感知的协同发展。

### 适用边界与局限

**数据模态约束**：当前框架的训练仅使用静态图像（RGB/RGB-D），对视频空间理解（如VSI-Bench）的提升有限（7B仅+1.21%），远低于部分图像基准（如Spatial457的+8.67%）。这是因为自监督任务主要捕捉单帧的空间结构，尚未涉及光流、时序一致性等视频特有的空间线索。

**深度传感器依赖**：区域深度排序和相对位置预测两个任务依赖RGB-D数据，限制了来自大规模纯RGB图像（如COCO）的训练扩展。虽然混洗补丁重排等深度无关任务可独立于深度数据运行，但整体框架的3D空间推理增益部分依赖于深度信号。

**通用能力的保持**：虽然通用VQA能力总体稳定（3B平均+2.02%，7B平均+0.57%），但在个别基准（如HallusionBench、RealWorld QA）上提升幅度较小甚至略有波动。这表明自监督RL对空间能力的增强在跨领域迁移上存在选择性——与空间推理直接相关的能力（如多物体推理）受益更多，而纯知识性或文本密集型任务受益有限。

**任务覆盖范围**：当前五种前预任务主要覆盖2D布局和基础3D关系，尚未涉及更复杂的物理交互（如支撑关系、遮挡推理）、时序空间推理或细粒度的3D几何理解（如物体姿态估计）。

### 开放问题

1. **视频原生自监督任务设计**：如何将框架扩展到光流预测、时序补丁对应、运动分割等视频原生任务，以进一步加强视频空间推理能力？这可能需要设计新的可验证奖励函数，利用帧间一致性作为自监督信号。

2. **跨模态泛化**：自监督任务的设计逻辑——从数据内在结构推导可验证真值——能否推广到触觉、音频等其他模态，或用于多模态融合的空间理解？这对于具身智能等需要多传感器空间感知的场景具有潜在价值。

3. **任务难度自适应**：自监督任务的难度（如补丁数量、翻转概率、深度间隙阈值）与模型容量之间是否存在最佳匹配？能否设计难度课程或自动难度调整机制，以最大化RLVR训练效率？

4. **纯2D图像的3D监督**：在缺乏深度传感器的情况下，如何从单目线索（如透视、遮挡、相对大小）设计有效的3D空间监督信号？单目深度估计的引入可能是一个方向，但其预测误差会破坏真值的确定性，需要权衡自监督的准确性与3D监督的覆盖范围。

5. **更大规模验证**：当前实验基于3B和7B规模的模型，在更大规模（如30B+）的LVLM上，自监督RL的增益是否持续存在？任务设计与模型容量的scaling行为值得进一步探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Spatial_SSRL_Enhancing_Spatial_Understanding_via_Self_Supervised_Reinforcement_Learning.pdf]]
