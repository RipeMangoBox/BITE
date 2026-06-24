---
title: Iterative Closed-Loop Motion Synthesis for Scaling the Capabilities of Humanoid Control
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Iterative_Closed_Loop_Motion_Synthesis_for_Scaling_the_Capabilities_of_Humanoid_Control.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Xu_Iterative_Closed-Loop_Motion_Synthesis_for_Scaling_the_Capabilities_of_Humanoid_CVPR_2026_paper.html
project_link: null
code_link: null
aliases:
- CCLAIMS
- ICLMSSCHC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 闭环自动化数据生成与控制器难度迭代的共同进化机制。
primary_logic: 通过构建专业语义分类与难度分层，结合多模态反馈驱动的竞争迭代课程，使数据生成难度随控制器能力自适应提升，从而在无昂贵动捕数据的情况下持续扩展控制器的技能边界。
claims:
- 在PHC单基元跟踪器上，仅使用约1/10的AMASS数据量，测试集平均失败率较基线降低45%。
- 专家提示合成的运动在t-SNE中与专业参考流形重叠，而随机提示运动分散在外，证明领域先验编码有效。
- 后续循环生成的运动分布具有更高的速度峰值和更宽的尾部，且控制器在第三方数据集上的跟踪成功率随循环逐步提升。
- Overall (Kungfu+EMDB+AIST+++Video-Convert, 2201 clips) 上 Success Rate = 76.9% (L6)
---

# Iterative Closed-Loop Motion Synthesis for Scaling the Capabilities of Humanoid Control

> [!tip] 核心洞察
> 通过构建专业语义分类与难度分层，结合多模态反馈驱动的竞争迭代课程，使数据生成难度随控制器能力自适应提升，从而在无昂贵动捕数据的情况下持续扩展控制器的技能边界。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向人形控制能力扩展的迭代闭环运动合成 |
| 英文题名 | Iterative Closed-Loop Motion Synthesis for Scaling the Capabilities of Humanoid Control |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_Iterative_Closed-Loop_Motion_Synthesis_for_Scaling_the_Capabilities_of_Humanoid_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CLAIMS (Closed-Loop Automated Iterative Motion Synthesis) |
| Dataset | Overall, Kungfu, AIST++ |

> [!tip] 效果简介
> - Overall (Kungfu+EMDB+AIST+++Video-Convert, 2201 clips) 上，Success Rate 76.9% (L6) vs 58.3% (AMASS) (+18.6% (failure rate -45%))。
> - Kungfu 上，Success Rate 60.3% (L6) vs 47.1% (AMASS) (+13.2%)。
> - AIST++ (MaskedMimic) 上，Success Rate 83.9% (Loop1) vs 75.3% (FC*) (+8.6%)。

## 概述

**核心问题**：当前人形控制策略的性能受限于训练数据集的固定难度分布，而获取专业高动态运动数据（如武术、体操）依赖昂贵的光学动捕，难以规模化扩展控制器的技能边界。

**核心思路**：本文提出 **CLAIMS**（Closed-Loop Automated Iterative Motion Synthesis），一个闭环自动化框架，通过构建专业语义分类与难度分层的提示库，结合多模态反馈驱动的竞争迭代课程，使运动数据生成难度随控制器能力自适应提升，从而在无昂贵动捕数据的情况下持续扩展控制器的能力上限。

**方法定位**：CLAIMS 属于数据-控制器共同进化的训练范式。其关键机制是将运动扩散模型（MDM）作为数据生成器、视觉语言模型（VLM）作为质量过滤器与难度评估器、大语言模型（Gemini CoT）作为课程决策者，三者围绕物理人形跟踪器形成闭环迭代。与现有工作在固定数据集上单阶段训练不同，CLAIMS 的核心创新在于**竞争性迭代课程**——每轮根据控制器表现自动升级数据难度，推动策略性能持续提升。

**主要结果**：
- 在 PHC 单基元跟踪器上，仅使用约 **1/10** 的 AMASS 数据量（不足 400 条训练序列），CLAIMS 在包含 Kungfu、EMDB、AIST++ 和 Video-Convert 的 2201 片段测试集上达到 **76.9%** 的平均成功率，较 AMASS 基线（58.3%）将**失败率降低 45%**（Table 1）。
- 在 MaskedMimic (FC*) 控制器上，CLAIMS 合成数据训练后 AIST++ 成功率从 75.3% 提升至 **83.9%**（Table 2）。
- 消融实验证实，完整的 VLM+物理指标联合观察、可变提示库以及迭代反馈机制三者均对性能有显著贡献（Table 3）。
- 数据难度随迭代轮次单调递增：第三方跟踪器 PHC+ 在后续循环数据上的成功率持续下降（Loop0: 75.3% → Loop6: 53.6%），且合成运动的速度分布展现出更高的峰值和更宽的尾部（Table 5, Figure 10），验证了竞争迭代课程的有效性。

## 背景与动机

人形机器人的全身控制长期依赖从运动捕捉数据集中学习跟踪策略。以 **PHC**（Luo et al., ICCV 2023）为代表的单基元跟踪器在 AMASS 等固定数据集上取得了显著进展，但其性能上限受制于训练数据的固有难度分布——AMASS 以日常动作为主，缺乏武术、体操等高动态专业运动样本。**核心瓶颈在于：** 固定数据集的难度天花板锁死了控制器能力的扩展空间，而获取专业高动态运动数据需要昂贵的动捕设备和专业表演者，难以规模化。

现有数据增强方法面临两难：随机提示合成的运动缺乏专业语义约束，生成质量不可控；而手工设计运动课程不仅耗时，且无法根据控制器实时表现自适应调整难度。这引出了一个关键问题——**能否构建一个闭环系统，使数据生成难度随控制器能力同步提升，从而在无昂贵动捕数据的情况下持续扩展技能边界？**

本文提出的 **CLAIMS**（Closed-Loop Automated Iterative Motion Synthesis）框架正是对这一问题的回答。其核心思路是：将控制器训练与数据生成耦合为一个竞争迭代过程——控制器在合成数据上训练后，多模态反馈（物理指标 + VLM 主观评分）驱动大语言模型策略从专业提示库中选择或生成更高难度的动作描述，进而合成更具挑战性的运动序列，形成“控制器变强 → 数据变难 → 控制器更强”的正反馈循环。这一设计使训练数据的难度分布随控制器能力自适应演进，突破了固定数据集的天花板效应。

## 核心创新

人形控制策略的性能上限长期受制于训练数据集的固定难度分布——现有基准（如 AMASS）以日常动作为主，缺乏对武术、体操等高动态专业技能的覆盖，而获取此类数据依赖昂贵的动捕设备，难以规模化。**CLAIMS** (Closed-Loop Automated Iterative Motion Synthesis) 的核心创新在于构建了一个**闭环自动化数据生成与控制器难度迭代的共同进化机制**，从根本上改变了训练数据的来源、课程和反馈信号三个关键维度。

### 1. 训练数据源：从固定数据集到专业提示驱动的合成运动

基线方法（如 **PHC single-primitive** (Luo et al., ICCV 2023)）依赖 AMASS 等固定数据集中随机采样的运动序列，其动作多样性和专业性受限于原始采集范围。CLAIMS 提出**难度感知的可变提示库**（Difficulty-Aware Prompt Library），覆盖武术、舞蹈、战斗、体育、体操五类专业领域，沿四个组合轴（如速度、复杂度、接触模式、空间范围）进行分层实例化（Figure 2, Section 3.1）。从该库采样的文本提示经 **MDM 运动扩散模型**（使用 DistilBERT 编码器）合成为运动序列，再通过物理有效性过滤（剔除浮动、下沉、穿透样本）和 VLM 语义对齐检查，确保生成数据的物理合理性与提示一致性（Section 3.2）。

这一设计的关键效果在于**领域先验编码**：专家提示合成的运动在 t-SNE 可视化中与专业参考流形重叠，而随机提示合成的运动则分散在外围（Figure 7a, Section 4.2），证明提示库有效约束了生成空间，使合成数据集中于专业运动流形，而非无结构的随机生成。

### 2. 训练课程：从单阶段训练到竞争迭代课程

基线方法采用单阶段训练，数据分布固定，控制器能力饱和后无法继续提升。CLAIMS 引入**竞争迭代课程**（Competitive Iterative Curriculum, Figure 4, Section 3.4）：每轮训练后，若控制器在物理指标上超过预设阈值，系统自动升级数据难度，使得数据集与控制器形成“军备竞赛”——数据集越来越难，控制器被迫适应更高动态的运动。

这一机制的核心因果链路在 Algorithm 1（Section 3.5）中形式化：初始化空数据集 $\mathcal{D}$ 和跟踪器 $\pi_0^{\mathrm{trk}}$，每轮 $k$ 计算物理指标 $m_k$ 和 VLM 难度反馈 $v_k$，由 LLM 策略 $\pi_\theta$（Gemini CoT）根据观察 $o_k = [m_k, v_k, e_k]$ 生成新的动作提示 $A_k$，经生成、过滤后扩展数据集并重新训练跟踪器。实验表明，PHC+ 第三方跟踪器在后续循环上的成功率单调下降（Loop0: 75.3% → Loop6: 53.6%, Table 5），且生成运动的速度分布呈现更高的峰值和更宽的尾部（Figure 10），直接验证了**数据难度随循环递增**的核心假设。

### 3. 反馈信号：从无反馈到多模态语义观察

传统方法缺乏反馈或仅依赖物理指标，无法感知运动的语义难度和技能属性。CLAIMS 构建了**联合 VLM 主观评分与控制器物理指标的多模态语义观察向量**（Section 3.4）：将每段训练运动渲染为 SMPL 拼接序列，由 GPT-4o 和 Qwen-VL-MAX 组成的 VLM 集成评估主观难度和运动属性描述，与控制器自身的物理指标（如关节误差、速度分布）拼接为统一的观察表示，驱动 LLM 策略选择或生成更高难度的动作提示。

消融实验（Table 3）严格验证了各反馈组件的贡献：完整观察（物理指标 + VLM）> 去除 VLM > 去除物理指标 > 二者皆无，且去除可变提示库的配置在所有第三方基准上性能下降，证实了**可变库与多模态反馈的协同必要性**（Section 4.4）。

### 4. 效率优势：数据规模与性能的脱钩

CLAIMS 在仅使用约 1/10 AMASS 数据量（不足 400 条训练序列）的情况下，使 PHC 单基元跟踪器在 2201 片段测试集上的平均失败率较 AMASS 基线降低 45%（成功率 76.9% vs 58.3%, Table 1），且从 Loop1 起即超越基线（64.0% vs 58.3%），后续循环持续提升至 Loop6 的 76.9%。这一结果打破了“更多数据 = 更好性能”的惯性假设，证明**数据质量与难度分布的针对性优化比数据规模更关键**。

## 整体框架

CLAIMS (Closed-Loop Automated Iterative Motion Synthesis) 是一个闭环自动化框架，其核心机制在于让运动数据生成与控制器训练形成共同进化：控制器在合成数据上获得跟踪能力，而其失败模式与物理指标又反向驱动数据生成器产出更具挑战性的专业动作，从而持续扩展控制器的技能边界（Fig. 1）。

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the CLAIMS pipeline: a closed-loop system that refines prompts from a 5-domain library (martial arts, dance, combat, sports, gymnastics), synthesizes motions with MDM, filters them by physics and VLM checks, trains humanoid trackers with RL, and uses multimodal feedback to generate progressively harder tasks*

### 瓶颈与因果机制

当前人形控制训练的根本瓶颈在于固定难度分布的数据集（如AMASS）限制了策略性能上限，而高动态专业运动数据的获取成本高昂、难以规模化。CLAIMS 通过三条因果链路打破这一瓶颈：

1. **领域先验编码**：构建覆盖武术、舞蹈、战斗、体育、体操五类领域的难度感知可变提示库（Fig. 2），将专业运动知识形式化为可组合的语言模板，使合成运动的分布与专业参考流形重叠（t-SNE 验证，Fig. 7a）。
2. **多模态反馈驱动**：联合控制器物理指标（如根高、速度分布）与 VLM 主观评分（GPT-4o、Qwen-VL-MAX）形成语义观察向量，为难度升级提供信息丰富的决策信号。
3. **竞争迭代课程**：当控制器在当期数据上达到预设阈值，Gemini CoT 策略自动从提示库中选择或生成更高难度动作提示，经 MDM 合成与物理/VLM 过滤后扩展训练集，形成“控制器变强→数据变难→控制器更强”的正反馈循环（Algorithm 1）。

### 流水线模块与数据流

CLAIMS 包含五个核心模块，数据流为闭环单向循环（Fig. 1, Fig. 3, Fig. 5）：

1. **Difficulty-Aware Prompt Library（难度感知提示库）**：提供五类专业领域的分层动作提示模板，沿四个组合轴（如速度、幅度、接触约束、空中姿态）定义难度变量（Section 3.1）。
2. **MDM Motion Generator（MDM 运动生成器）**：以 DistilBERT 编码的文本提示为条件，通过运动扩散模型合成 SMPL 运动序列（Section 3.2）。
3. **Physics & VLM Filter（物理与视觉语言过滤）**：剔除物理无效运动（浮动、下沉、穿透），并由 VLM 评估提示-运动语义对齐，仅保留通过双重检查的样本（Section 3.2）。
4. **PHC/MaskedMimic Tracker（人形跟踪器）**：基于强化学习的物理人形跟踪器，在逐步扩展的合成数据集上训练（Section 3.3）。
5. **Gemini CoT Policy（多模态反馈策略）**：融合物理指标与 VLM 反馈，从可变提示库中采样或生成新的高难度动作提示，形成下一轮数据生成指令（Section 3.5）。

### 迭代闭环逻辑

如 Algorithm 1 所示，初始化后每轮迭代执行以下步骤：① 计算当前控制器在训练数据上的物理指标 $m_k$ 和 VLM 难度/属性反馈 $v_k$；② 将上一轮动作编码 $e_k$ 与 $m_k, v_k$ 拼接为观察向量 $o_k$；③ Gemini CoT 策略 $\pi_\theta$ 根据 $o_k$ 从可变库 $\mathcal{L}$ 和模板 $\mathcal{T}$ 中生成新动作提示集 $A_k$；④ 对每个提示经 MDM 生成运动、物理过滤、VLM 对齐检查后加入 $M_k$；⑤ 将 $M_k$ 并入总数据集 $\mathcal{D}$，重新训练跟踪器 $\pi_{k+1}^{\text{trk}}$。该闭环在无需昂贵动捕数据的前提下，仅用约 1/10 的 AMASS 数据量，使测试集平均失败率较基线降低 45%（Table 1）。

### 方法定位

CLAIMS 在方法谱系上属于**数据-控制器共同进化的闭环训练范式**，区别于：

- **固定数据集训练**（如 **PHC** (Luo et al., ICCV 2023) 在 AMASS 上单阶段训练）：数据分布不变，性能受限于数据集难度上限。
- **非迭代单阶段合成数据训练**：在等量合成数据上训练，但缺乏难度递增课程，控制器无法持续突破能力边界（消融实验证实迭代循环持续优于该基线，Table 3, Table 4）。
- **掩码运动修复范式**（如 **MaskedMimic** (Tessler et al., TOG 2024)）：CLAIMS 同样可适配该跟踪器，Loop1 在 AIST++ 上成功率从 75.3% 提升至 83.9%（Table 2），验证了框架的通用性。

关键创新在于将**领域先验编码**（可变提示库）、**多模态反馈融合**（物理指标+VLM）与**竞争迭代课程**三者耦合，形成自适应的能力扩展机制，而非单纯依赖生成模型或强化学习算法的改进。

## 核心模块与公式推导

CLAIMS 框架由五个核心模块构成，形成“提示生成→运动合成→物理/语义过滤→强化学习跟踪→多模态反馈”的闭环迭代管线（Figure 1, Figure 5）。

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/005_Figure_5.jpg]]
*Figure 5: Schematic Diagram of the Automated Iterative Loop*

### 3.1 难度感知提示库

该模块定义了五类专业运动域（武术、舞蹈、战斗、体育、体操）和四个组合轴（如速度、幅度、复杂度等），构成可变提示模板库 $\mathcal{L}$ 和 $\mathcal{T}$（Figure 2）。其核心作用是将“运动专业性”和“难度”形式化为可组合的语言提示，为后续的难度升级提供结构化搜索空间。

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/002_Figure_2.jpg]]
*Figure 2: Difficulty-aware variable library across five domains and four compositional axes*

### 3.2 MDM 运动生成器与过滤

给定文本提示 $a_k^j$，运动扩散模型 **MDM**（使用 DistilBERT 编码器）合成运动序列 $q_k^j = G(a_k^j)$。随后，物理过滤器剔除根节点浮动、下沉或肢体穿透的无效运动；VLM 过滤器评估提示-运动语义对齐度，仅保留对齐充分的样本。该模块确保合成数据的物理合理性和语义保真度（Figure 3）。

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/003_Figure_3.jpg]]
*Figure 3: Prompt-to-prompt data generation*

### 3.3 基于强化学习的物理跟踪器

采用 **PHC** 单基元跟踪器（Luo et al., ICCV 2023）或 **MaskedMimic**（Tessler et al., TOG 2024）作为可训练控制器 $\pi_k^{\text{trk}}$。每轮迭代在累积数据集 $\mathcal{D}$ 上重新训练，评估指标包括全局关节位置误差（mpjpe-g）、局部关节位置误差（mpjpe-l）、速度分布距离（vel-dist）和加速度分布距离（accel-dist）。

### 3.4 竞争迭代课程与多模态反馈

控制器与数据集之间存在竞争关系：当跟踪指标超过预设阈值时，当前数据分布被视为“已掌握”，系统自动升级数据难度以突破性能天花板（Figure 4）。反馈信号由两部分组成：
- **物理指标** $m_k$：来自跟踪器的客观运动学/动力学统计量；
- **VLM 主观评估** $v_k$：使用 GPT-4o 和 Qwen-VL-MAX 对渲染的 SMPL 运动序列进行难度和属性评估。

两者拼接形成语义观察向量 $o_k = [m_k, v_k, e_k]$，其中 $e_k = \phi(a_k)$ 为上一轮动作提示的编码。

### 3.5 自动化迭代循环（核心算法）

```text
Algorithm 1: LLM-Driven Competitive Dataset–Controller Iteration
1:  Input: variable library L, templates T, generator G,
     VLM evaluator F_VLM, policy LLM π_θ (Gemini CoT).
2:  Initialize dataset D ← ∅, motion sets M ← ∅,
     tracker π_0^trk, action a_0.
3:  for k = 0 to K − 1 do
4:    Compute tracking metrics m_k and VLM difficulty/feedback v_k.
5:    Encode previous action e_k = φ(a_k) and form observation o_k = [m_k, v_k, e_k].
6:    Generate new action prompts:
      A_k = {a_k^1, …, a_k^M} ∼ π_θ(o_k, L, T).
7:    Initialize M_k ← ∅.
8:    for a_k^j ∈ A_k do
9:      q_k^j ← G(a_k^j); if fails physics continue.
10:     if VLM alignment is sufficient: M_k ← M_k ∪ {(q_k^j, a_k^j)}.
11:   end for
12:   D ← D ∪ M_k; π_{k+1}^trk ← TrainTracker(D).
13:   Store motion set: M ← M ∪ {M_k}.
14:   Update summary prompt a_{k+1}.
15: end for
16: Return: best tracker π_*^trk and motion sets M.
```

**变量含义**：
- $\mathcal{L}$：可变提示库，$\mathcal{T}$：模板集，共同定义提示的合法组合空间；
- $G$：MDM 运动生成器；
- $F_{\text{VLM}}$：VLM 评估器，输出语义对齐度和难度评分；
- $\pi_\theta$：Gemini CoT 策略，根据观察 $o_k$ 从 $\mathcal{L}$ 和 $\mathcal{T}$ 中选择或生成更高难度的动作提示；
- $m_k$：物理跟踪指标向量，$v_k$：VLM 反馈向量，$e_k$：上轮动作编码；
- $A_k$：第 $k$ 轮生成的候选动作提示集合；
- $M_k$：第 $k$ 轮通过过滤的运动-提示对集合；
- $\pi_k^{\text{trk}}$：第 $k$ 轮训练后的跟踪器策略。

**关键机制**：Gemini CoT 策略作为“难度调度器”，在每轮迭代中融合物理指标和 VLM 语义反馈，从提示库中选择更具挑战性的动作描述，驱动生成器产出更高难度的运动数据，实现控制器能力与数据难度的共同进化。

## 实验与分析

### 主实验结果

CLAIMS 框架在多个第三方测试集上展现出显著的性能优势。在总计 2201 个片段的综合测试集（涵盖 Motion-X/Kungfu、EMDB、AIST++ 和 Video-Convert）上，经过六轮迭代的 L6 模型取得了 **76.9%** 的平均成功率，相较在 AMASS 数据集上训练的 PHC 单基元基线（58.3%）提升了 **18.6 个百分点**，平均失败率降低约 **45%**。值得注意的是，这一优势在仅使用约 400 个训练序列（约为 AMASS 数据量的 1/10）的条件下即已实现（Table 1）。即使在第一轮迭代（L1），成功率已达 64.0%，超越了 AMASS 基线，验证了合成数据的初始质量与课程机制的有效性。

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/007_Table_1.jpg]]
*Table 1: Success rate (%) of different pipelines across test sets (totaling 2201 clips). The test suite includes: Motion-X/Kungfu (663), EMDB (45), AIST++ (1320), and Video-Convert (173). We report per-set results and the average (Avg) calculated by clip*

在专业运动类别上，CLAIMS 的增益尤为突出。在 Motion-X/Kungfu 测试集上，L6 模型成功率达到 **60.3%**，相较 AMASS 基线的 47.1% 提升 13.2 个百分点，表明迭代闭环机制有效扩展了控制器对高难度武术动作的跟踪能力（Table 1）。

框架的通用性在 MaskedMimic 控制器上同样得到验证。在 AIST++ 测试集上，经 CLAIMS 一轮迭代训练的 MaskedMimic 成功率达 **83.9%**，相较其基线 FC*（75.3%）提升 8.6 个百分点；在 Motion-X/Kungfu 上从 54.0% 跃升至 65.8%，在 EMDB 上从 48.9% 提升至 71.1%（Table 2）。这表明 CLAIMS 的数据生成与课程策略对不同跟踪器架构具有普适迁移能力。

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/011_Table_2.jpg]]
*Table 2: MaskedMimic (FC*): Success Rate (%) on each test set. ”*” means early period*

定性对比进一步支持了定量结果。在 Figure 9 展示的跟踪效果中，CLAIMS 训练的控制器在高动态武术动作上的姿态恢复精度和物理合理性均优于 PHC 和 MaskedMimic 基线，尤其在快速转身、大幅度肢体伸展等极端姿态下保持了更稳定的跟踪。

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/010_Figure_9.jpg]]
*Figure 9: Qualitative tracking performance between Ours and Baselines of PHC and Maskedmimic*

### 消融研究

**多模态观察信号的作用。** 消融实验系统评估了 Gemini CoT 策略中观察向量的各组件贡献（Table 3）。完整配置（物理指标 + VLM 语义反馈）在所有测试集和迭代轮次上均取得最高成功率。移除 VLM 反馈后性能下降，移除物理指标后进一步恶化，而同时移除两者（仅保留上一轮动作编码）的性能最低。这一梯度消融结果表明：物理指标提供控制器能力的客观量化，VLM 反馈则补充了主观难度评估与语义属性描述，二者协同实现了更精准的难度升级决策。

**可变提示库的必要性。** 移除可变提示库（w/o var library）的配置在所有第三方基准上均弱于完整配置（Table 3）。固定提示库无法根据控制器当前能力边界自适应调整动作语义空间，导致生成数据的难度分布与控制器能力脱节，限制了课程学习的效率。

**迭代反馈机制的增益。** 非迭代的单阶段训练（在等量合成数据上训练）性能显著低于迭代配置（Table 3, Table 4）。在 1400 片段测试集上，Loop0（初始合成数据单阶段训练）与 Loop6 的对比显示，六轮迭代在所有子集上均带来一致且显著的提升（Table 4）。这证明性能增益并非仅来自合成数据本身，而是来自数据难度随控制器能力共同进化的闭环机制。

### 数据难度演化验证

为验证迭代闭环是否真正生成了难度递增的训练数据，论文采用独立的第三方跟踪器 PHC+ 对各轮生成数据进行评估（Table 5）。结果显示，PHC+ 在 Loop0 数据上的成功率为 75.3%，随着迭代轮次增加单调下降至 Loop6 的 53.6%；同时，全局 MPJPE 误差从 49.78 mm 上升至 59.61 mm。成功率的持续下降与跟踪误差的持续上升一致表明，后续循环生成的运动对第三方跟踪器而言难度显著增加。

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/015_Table_5.jpg]]
*Table 5: PHC+ tracking performance on our datasets.A lower success rate indicates that the motions are more challenging for thirdparty trackers*

进一步的速度分布分析（Figure 10）显示，CLAIMS 生成数据的关节速度分布相较 AMASS 具有更高的峰值和更宽的尾部，表明合成数据包含更多高动态片段。循环间的速度趋势（Figure 6）也显示，Qwen 评估的难度评分与运动速度随迭代轮次单调上升。这些证据共同确认了竞争迭代课程成功地、自动化地提升了数据难度。

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/013_Figure_10.jpg]]
*Figure 10: The velocity distribution of AMASS and ours*

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/006_Figure_6.jpg]]
*Figure 6: Loop-wise Difficulty and Speed Trends of Qwen Evaluations*

### 运动分布与领域先验

t-SNE 可视化（Figure 7a）表明，基于专业提示库合成的武术运动与专业参考数据集（Motion-X/Kungfu）在流形上高度重叠，而随机提示生成的运动则分散在外围区域。在全数据集对比中（Figure 7b），CLAIMS 生成的运动覆盖了 AMASS 未触及的高动态区域，同时避免了随机提示的离散分布。这验证了难度感知可变提示库有效编码了领域先验，使合成运动在保持专业语义的同时扩展了分布覆盖。

### 局限与失效模式

尽管 CLAIMS 展现出显著的性能增益，论文明确指出以下局限：首先，当前使用的 MDM 生成模型在极端高动态动作（如连续空翻、高速旋转）上的合成容量有限，导致课程后期难度升级的边际收益递减。其次，手动构建的提示库缺乏客观校准与完整覆盖，可能遗漏某些动作子空间。框架的模块化设计允许未来替换更强的生成模型和自动化构建多模态提示库来缓解这些问题，但当前版本在这些边界条件下仍存在性能瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/012_Table_3.jpg]]
*Table 3: Ablation study on success rate across different test sets and loops*

![[assets/figures/papers/paper_list_l32_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Iterative_Closed_Lo/figures/004_Figure_4.jpg]]
*Figure 4: Competitive iteration between the controller and the dataset*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

CLAIMS 的核心贡献在于提出了一种**数据-控制器共同进化**的训练范式，而非单纯改进跟踪器架构。因此，其与现有工作的关系更接近于**训练框架的升维**，而非模型层面的直接替代。

**与 PHC 系列的关系**
CLAIMS 直接以 **PHC** (Luo et al., ICCV 2023) 的单基元跟踪器作为验证载体。PHC 原框架依赖固定数据集（如 AMASS）进行单阶段训练，其性能上限受限于数据分布的静态难度。CLAIMS 将 PHC 嵌入闭环迭代管线中，通过自适应难度课程替代固定数据采样，使同一跟踪器架构在仅使用约 1/10 数据量的条件下，将测试集平均失败率降低 45%（Table 1）。这表明 CLAIMS 的价值在于**释放了现有跟踪器架构的潜在能力**，而非依赖更强的模型容量。

**与 MaskedMimic 的关系**
**MaskedMimic** (Tessler et al., TOG 2024) 基于 DeepMimic 的掩码运动修复范式，代表了另一类物理角色控制路线。CLAIMS 在 MaskedMimic (FC*) 上验证了框架的通用性：经过 Loop1 迭代后，AIST++ 上的成功率从 75.3% 提升至 83.9%（Table 2），证明闭环数据进化机制可跨架构迁移。

**与单阶段合成数据训练的对比**
论文设置了关键的对照基线：在等量合成数据上进行非迭代单阶段训练（Non-iterative one-shot）。消融实验（Table 3, Table 4）表明，迭代反馈机制（Loop0→Loop6）在多个测试集上持续优于等规模非迭代配置。这直接验证了**迭代共同进化**而非单纯数据增广才是性能提升的因果机制。

### 2. 适用边界与局限

**生成模型的能力瓶颈**
CLAIMS 的合成质量受限于底层运动扩散模型 MDM 的生成容量。论文明确指出，对于极端高动态动作（如连续空翻衔接），当前生成器的合成质量有限。这构成了框架的**上游能力边界**——当生成器无法产出物理合理的高难度运动时，迭代课程的难度升级将触及天花板。不过，框架的模块化设计允许未来替换更强的生成模型。

**提示库的手工构建约束**
难度感知可变提示库（Difficulty-Aware Prompt Library）覆盖武术、舞蹈、战斗、体育、体操五个领域，并通过四个组合轴实现分层。但该库目前为手工构建，论文承认其缺乏客观校准和完整覆盖。这意味着：
- 领域偏置：五类运动的选择可能遗漏其他高动态场景（如极限运动、杂技变体）；
- 难度标定主观：分层依据依赖先验知识，缺乏统一的难度度量标准；
- 扩展成本：新增领域需人工设计提示模板和变量空间。

**物理过滤的保守性**
物理过滤器（根高度检测、穿透检测）和 VLM 语义对齐检查在保证数据质量的同时，可能过度筛除边界运动——那些处于物理可行边缘但具有训练价值的高难度样本。这可能导致课程升级的**保守偏置**，限制控制器对极端状态的探索。

### 3. 开放问题

论文明确提出了两个开放方向，结合方法架构可进一步延伸：

1. **自动化提示库构建与校准**
   当前可变库依赖人工定义，未来方向包括：
   - 利用多模态大模型从视频数据中自动提取动作语义和难度层级；
   - 构建领域知识图谱以实现跨域动作的组合泛化；
   - 引入客观难度度量（如动力学约束满足度）替代主观分层。

2. **生成器能力的持续升级**
   框架的性能上限与生成模型强耦合。未来需探索：
   - 集成物理感知的运动生成模型，以提升高动态动作的物理合理性；
   - 在迭代过程中联合微调生成器，使其适应控制器反馈信号；
   - 利用控制器失败案例反向指导生成器的定向优化。

3. **隐式开放问题（基于架构推演）**
   - **多模态反馈的校准**：VLM 主观评分与物理指标之间存在潜在的冲突（如语义正确但物理不可行的运动），当前通过联合过滤规避，但缺乏对冲突信号的系统建模；
   - **负迁移风险**：迭代课程中，早期循环的合成数据分布可能引入偏置，影响后续循环的探索方向，论文未分析课程升级路径的稳定性；
   - **计算扩展性**：每轮迭代需重新训练跟踪器，计算成本随循环线性增长，论文未讨论效率优化策略。

### 4. 在知识库中的定位

CLAIMS 处于**物理角色控制 × 运动生成 × 课程学习**的交叉点：

- **相对于数据驱动控制**：CLAIMS 将“固定数据集训练”范式推进为“数据-控制器闭环共同进化”，为 Scaling Law 在人形控制领域的应用提供了新路径——通过自动化数据难度升级持续扩展技能边界，而非依赖更大规模的静态数据集。
- **相对于运动生成**：CLAIMS 为生成模型提供了下游验证场景和反馈信号，形成“生成-过滤-训练-反馈”的闭环，可视为生成模型与控制器的协同优化框架。
- **相对于课程学习**：CLAIMS 的竞争迭代课程区别于传统的预定义难度排序，其难度升级由多模态反馈（物理指标 + VLM 语义评估）自适应驱动，属于**闭环自适应课程**的新范式。

该工作的核心启示在于：**当数据获取成本高昂时，闭环自动化生成与自适应难度升级可作为扩展控制器能力的有效替代路径**，其模块化设计为后续研究提供了可插拔的框架基础。

## 原文 PDF

![[paperPDFs/CVPR_2026/Iterative_Closed_Loop_Motion_Synthesis_for_Scaling_the_Capabilities_of_Humanoid_Control.pdf]]
