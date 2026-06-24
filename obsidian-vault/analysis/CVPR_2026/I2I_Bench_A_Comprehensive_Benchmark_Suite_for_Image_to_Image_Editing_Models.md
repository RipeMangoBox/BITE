---
title: "I2I-Bench: A Comprehensive Benchmark Suite for Image-to-Image Editing Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/I2I_Bench_A_Comprehensive_Benchmark_Suite_for_Image_to_Image_Editing_Models.pdf
project_link: null
code_link: null
aliases:
- IB
- I2I-Bench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 提出解耦的层次化评估框架，融合专用“专家”工具和通用大模型（LMM）的混合自动化评估方法。
primary_logic: 通过“专家+通才”混合范式，实现全面、细粒度、自动化且与人类偏好高度一致的图像编辑模型评估。
claims:
- I2I-Bench包含1000个提示，跨越10个任务类别，涵盖单图像和多图像编辑。
- I2I-Bench定义了30个细粒度评估维度，每个维度配有可复现的自动化混合评估管道。
- 大规模人工验证表明自动化评估与人类偏好高度一致，皮尔逊相关系数优秀。
- I2I-Bench Single-Image Editing (Overall) 上 Normalized Overall Score = 0.813 (Qwen-Image-Edit-2509, best)
---

# I2I-Bench: A Comprehensive Benchmark Suite for Image-to-Image Editing Models

> [!tip] 核心洞察
> 通过“专家+通才”混合范式，实现全面、细粒度、自动化且与人类偏好高度一致的图像编辑模型评估。

| 字段 | 内容 |
|------|------|
| 中文题名 | I2I-Bench：图像到图像编辑模型的综合基准测试套件 |
| 英文题名 | I2I-Bench: A Comprehensive Benchmark Suite for Image-to-Image Editing Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.04660) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | I2I-Bench |
| Dataset | I2I-Bench Single-Image Editing, I2I-Bench Multi-Image Editing, I2I-Bench Single-Image, Physical Plausibility, I2I-Bench Multi-Image, World Knowledge & Reasoning |

> [!tip] 效果简介
> - I2I-Bench Single-Image Editing (Overall) 上，Normalized Overall Score 0.813 (Qwen-Image-Edit-2509, best) vs 0.416 (instruct-pix2pix, worst) (+0.397)。
> - I2I-Bench Multi-Image Editing (Overall) 上，Normalized Overall Score 0.636 (Nano-Banana, best) vs 0.545 (Omnigen2, worst among ME models) (+0.091)。
> - I2I-Bench Single-Image, Physical Plausibility 上，Normalized Score 0.537 (Step1X-Edit, best) vs 0.348 (instruct-pix2pix, worst) (+0.189)。

## 概述

图像编辑模型近年发展迅猛，但评估体系严重滞后。现有基准任务覆盖有限、评估维度单一，且高度依赖昂贵、难以复现的人工标注，尤其缺乏对多图像编辑任务的系统覆盖。**I2I-Bench** 针对这一瓶颈，提出了一套解耦的层次化评估框架，核心思路是构建“专家+通才”混合自动化评估范式：专用“专家”工具负责精确分数预测，通用大模型（LMM）承担语义理解，二者协同实现全面、细粒度且与人类偏好高度一致的自动化评估。

I2I-Bench 包含 **1000 条精心设计的提示**，系统覆盖 **10 个任务类别**，横跨单图像编辑与 5 个递增复杂度的多图像编辑任务。评估体系定义了 **30 个解耦细粒度维度**，每个维度均配有可复现的混合评估管道。大规模人工验证表明，该自动化评估与人类偏好的皮尔逊相关系数达到 0.9425（单图像编辑整体），显著优于纯 LMM 基线（ρ=0.7277），验证了混合设计的必要性。

在基准测试中，**Qwen-Image-Edit-2509** 以归一化总分 0.813 领跑单图像编辑，而 **Nano-Banana** 以 0.636 在多图像编辑中表现最佳。模型能力随任务认知复杂度升高而下降的趋势明显，尤其在物理合理性（最高仅 0.537）和世界知识与推理（多图像编辑中最低仅 0.038）等维度上，现有模型仍有巨大提升空间。

## 背景与动机

图像编辑模型近年来经历了爆发式发展，从早期的GAN到扩散模型，再到基于多模态大模型（LMM）的指令驱动编辑，模型能力边界不断拓展。然而，评估方法的演进速度远滞后于模型本身，形成日益加剧的“评估赤字”。

### 现有评估基准的结构性缺陷

当前图像编辑评估体系存在三个相互叠加的系统性缺陷：

**任务覆盖的单维性。** 主流基准如TEdBench、EditBench、MagicBrush等几乎完全聚焦于单图像编辑任务，对日益重要的多图像编辑场景（如跨图像主体合成、多图一致性编辑）缺乏覆盖。即便在单图像编辑内部，任务类别也高度集中于目标替换、属性修改等基础操作，缺少对物理合理性、世界知识推理、抽象逻辑组合等高层认知能力的考察。

**评估维度的粗糙性。** 现有评估多依赖PSNR、SSIM、LPIPS等像素级保真度指标，或笼统的“指令遵循度”评分。这种粗粒度评估无法解耦编辑质量中的不同因果因素——例如，一个模型可能在非编辑区域保真度上表现优异，却在物理合理性上完全失败，而传统指标会将两者混为一谈。更关键的是，缺乏对文本渲染准确性、主体身份一致性、组合交互自然度等细粒度能力的独立度量。

**人工标注的不可持续瓶颈。** 为弥补自动指标的不足，部分工作引入人工评估，但大规模人工标注成本高昂、周期漫长，且不同标注者之间的主观偏差难以校准。这导致评估结果难以复现，也使得快速迭代的模型开发缺乏即时反馈。

### 核心动机与突破路径

针对上述困境，I2I-Bench的核心动机是构建一个**全面、细粒度、自动化且与人类偏好高度一致**的评估体系。实现这一目标的关键洞察在于：不同评估维度对评估工具的能力需求本质上是异质的——像素级质量判断需要精确的感知模型，而语义理解和逻辑推理则需要通用知识能力。单一工具无法同时胜任两者。

这一洞察催生了“专家+通才”混合评估范式：对于美学质量、非编辑区域保真度等需要精确感知的维度，采用专用“专家”工具（如Q-Insight、ArtiMuse）进行分数预测；对于指令遵循、物理合理性、世界知识推理等需要语义理解的维度，则依赖通用大模型（LMM）的多问题VQA管道。两者协同，既保证了感知精度，又覆盖了语义广度。

### 方法谱系与知识库定位

I2I-Bench在评估方法论上位于自动化评估基准和人类对齐研究的交汇点。与纯LMM评估方法（如**LMM4Edit**）相比，I2I-Bench通过引入专家模型解决了LMM在精确感知维度上的固有弱点——消融实验显示，纯LMM基线在美学质量评估上甚至出现负相关（ρ=-0.0643），而I2I-Bench的混合管道达到0.9889。与传统自动指标（PSNR/LPIPS）相比，I2I-Bench通过LMM的语义理解能力覆盖了后者完全无法触及的高层编辑意图评估。

在知识库定位上，I2I-Bench贡献了一个包含1000条精心设计提示、10个任务类别、30个解耦评估维度的结构化评估框架，以及配套的大规模人类偏好验证数据。这套体系不仅服务于现有模型的横向比较，更通过揭示模型在物理合理性、多语言文本渲染、抽象逻辑推理等维度的普遍失败模式，为下一代编辑模型的研发提供了明确的改进方向。

## 核心创新

I2I-Bench 的核心创新在于构建了一个**解耦的层次化评估框架**，并通过“**专家 + 通才**”混合自动化评估范式，系统性地解决了现有图像编辑评估基准的三大瓶颈：任务覆盖狭窄、评估维度不足、以及对昂贵人工标注的严重依赖。

### 1. 任务覆盖的维度跃迁

现有评估基准（如 LMM4Edit）主要聚焦于单图像编辑任务，且任务类别有限。I2I-Bench 将评估空间从单图像编辑（SE）拓展至**递增认知复杂度的多图像编辑（ME）**，构建了包含 **1000 个提示、10 个任务类别**的 Prompt Suite（Figure 2）。其中，ME 任务包含 5 个递进层级——从“多图像对象操作”到“世界知识与推理”——直接暴露了现有模型在跨图像语义对齐与组合推理上的能力断层。例如，在 ME 的“世界知识与推理”维度上，最佳模型 Nano-Banana 得分 0.721，而 Omnigen2 仅得 0.038（Table 2），差距达 +0.683。

### 2. 评估维度的细粒度解耦

I2I-Bench 将评估从粗粒度的整体质量判断，解耦为 **30 个细粒度维度**，覆盖三大层次：
- **基础质量与保真度**：如整体图像质量、美学质量、混合自然度、编辑伪影、非编辑区域保真度；
- **任务执行能力**：如指令遵循、主体身份保真度、物理合理性、组合与交互；
- **高级推理能力**：如世界知识与推理、文本渲染准确性。

这种解耦使得模型的能力短板可被精准定位。例如，在单图像编辑的“物理合理性”维度上，最佳模型 Step1X-Edit 也仅得 0.537，而 instruct-pix2pix 仅得 0.348（Table 1），表明物理约束仍是当前模型的普遍瓶颈。

### 3. “专家 + 通才”混合自动化评估范式

这是 I2I-Bench 最具区分度的技术贡献。针对不同评估维度的特性，I2I-Bench 设计了**可复现的混合评估管道**，融合两类评估器：

| 评估器类型 | 角色 | 典型工具/方法 | 适用维度示例 |
|-----------|------|-------------|------------|
| **专家模型 (Specialist)** | 精确分数预测 | Q-Insight, ArtiMuse | 整体图像质量、美学质量 |
| **通用大模型 (Generalist LMM)** | 语义理解与判断 | Qwen3-VL-8B-Instruct (VQA-5level, VQA-2level, Multi-VQA) | 混合自然度、指令遵循、物理合理性 |

关键公式包括：
- **VQA-5level 加权评分**（用于主观整体维度）：
  $$\mathrm{Score}_{5\text{-level}} = \sum_{i=1}^{5} w_i \cdot P_{\mathrm{LMM}}(c_i | I, Q)$$
- **Hybrid-Sim 混合相似度**（用于非编辑区域/主体保真度）：
  $$\mathrm{Score}_{\mathrm{Hybrid-Sim}} = \frac{f_{\mathrm{orig}} \cdot f_{\mathrm{gen}}}{||f_{\mathrm{orig}}|| \cdot ||f_{\mathrm{gen}}||}$$
  其中 $f$ 由 LMM 语义分割引导的专家特征提取器生成。

消融实验（Table 3）严格验证了混合设计的必要性：
- **整体 SE 维度**：I2I-Bench 混合管道与人类偏好的皮尔逊相关系数 $\rho = 0.9425$，显著优于纯 LMM 基线（$\rho = 0.7277$）；
- **美学质量维度**：纯 LMM 基线出现**负相关**（$\rho = -0.0643$），而 I2I-Bench 使用专家模型 ArtiMuse 达到 $\rho = 0.9889$，证明专家工具在精确质量判断上不可替代；
- **复杂语义维度**：如“主体身份保真度”，混合管道 $\rho = 0.9133$，纯 LMM 基线仅为 $-0.3494$。

### 4. 人类对齐的闭环验证

I2I-Bench 内置了**成对比较人工标注协议**，对自动化评估进行大规模对齐验证。每维度约 85 项成对比较，采用 20% 随机抽样和 10% 错误率阈值的质量控制。结果表明，I2I-Bench 在所有 30 个维度上均与人类偏好保持高度一致，且显著优于现有基准 LMM4Edit（Table 6），为自动化评估的可靠性提供了实证基础。

## 整体框架

I2I-Bench 是一个由三个核心组件构成的综合基准套件，其设计遵循“任务定义→模型执行→混合评估→人类验证”的闭环流程（Figure 1）。

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/001_Figure_1.jpg]]
*Figure 1: An overview of the proposed image-to-image editing evaluation benchmark suite, I2I-Bench. The process starts with our largescale Prompt Suite, which defines the editing tasks. These prompts are fed into the Editing Model to edit images. The prompts also guide the selection of relevant dimensions from our hierarchical Evaluation Dimension Suite. Each dimension, in turn, specifies both the automated Evaluation Method Suite (combining Specialists and Generalists) and the criteria for Human Annotation. Finally, the results from the automated methods and human annotations are compared for Alignment Verification to ensure the reliability of our benchmark*

**Prompt Suite（提示集）** 是整个管道的起点，包含 **1000 条精心设计的提示**，均分为单图像编辑（SE）和多图像编辑（ME）两大类别，系统性地覆盖 **10 个任务类别**。这些提示同时承担双重角色：一方面作为编辑模型的输入指令，驱动图像生成；另一方面为后续评估维度提供任务上下文与评判依据。

**Evaluation Dimension & Method Suite（评估维度与方法套件）** 构成了管道的核心评估层。它采用**层次化解耦框架**，定义了 **30 个细粒度评估维度**，从基础质量（如整体图像质量、美学质量、混合自然度）到任务执行能力（如指令遵循、主体身份忠实度、物理合理性）再到高级推理（如世界知识与推理）进行全方位覆盖。每个维度均配有**可复现的自动化混合评估管道**：对于需要精确数值预测的维度（如美学质量），调用专用“专家”工具（如 Q-Insight、ArtiMuse）直接产出定量分数；对于需要语义理解的维度（如混合自然度、物理合理性），则采用基于大语言多模态模型（LMM）的视觉问答（VQA）管道，通过多级量表或二元判断获取概率化评分。这种“专家+通才”的混合范式是 I2I-Bench 区别于纯 LMM 评估方法的核心设计。

**Human Preference Annotation Protocol（人类偏好标注协议）** 作为管道的验证闭环，通过大规模成对比较人工标注，系统性地验证自动化评估指标与人类判断的一致性。该协议不仅为基准的可靠性提供统计证据（皮尔逊相关系数），也为混合设计（专家模型 vs. 纯 LMM）的必要性提供了消融验证基础。

整个框架的输入为编辑提示和原始图像，经编辑模型生成编辑图像后，各维度评估管道并行或串行地输出归一化分数，最终汇聚为模型在各维度及任务类别上的能力画像。

### 补充图表

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of the 10 task categories in the I2I-Bench Prompt Suite. The left half shows 5 single-image editing (SE) tasks, from “Object Manipulation” to “World Knowledge & Reasoning”. The right half shows 5 multi-image editing (ME) tasks, illustrating increasing complexity from “Basic Combination” to “Combination + Reasoning”*

## 核心模块与公式推导

### 关键评估维度与混合评估管道

I2I-Bench 的评估体系围绕 **30 个解耦的细粒度评估维度** 构建，每个维度均配有可复现的自动化混合评估管道。该管道的核心设计思想是“专家+通才”混合范式：对需要精确数值判断的维度使用专用“专家”工具，对需要语义理解的维度使用通用大模型（LMM），对复杂组合维度则采用两者协同的混合策略。

**基础质量维度**（Common Dimensions）覆盖所有编辑任务共有的评估需求：

- **Overall Image Quality** 与 **Aesthetic Quality**：直接使用专用专家模型 **Q-Insight** 和 **ArtiMuse** 获取定量分数，避免通用 LMM 在美学评估上的系统性偏差。
- **Blending Naturalness** 与 **Generative/Editing Artifacts**：采用基于视觉问答的 **LMM VQA-5Level** 管道，通过五级量表加权平均获得评估分数。
- **Non-Edited Fidelity**：使用混合 LMM-专家管道，先由 LMM 进行语义分割定位编辑区域，再对非编辑区域提取专家特征并计算余弦相似度。
- **Subject Identity Fidelity**：同样使用混合管道，但仅在分割出的主体区域上计算特征相似度，无需掩码反转。

**任务执行维度**（Task-Specific Dimensions）针对不同编辑任务定制：

- **Composition & Interaction**、**Physical Plausibility** 等维度：使用 LMM 多问题 VQA 管道，通过多个针对性问题的“是/否”回答比例来评估复杂语义概念。
- **Text Content & Style**：融合 OCR 内容准确度与 LMM 风格评分的分段函数，实现文本渲染精确性的细粒度评估。
- **Subject Extraction & Composition**：最终分数由计数的二元分数与主体一致性分数的乘积构成。

### 核心公式

**公式 (1) — Score_5-level（五级 VQA 加权评分）**

$$\mathrm{Score}_{5\text{-level}} = \sum_{i=1}^{5} w_i \cdot P_{\mathrm{LMM}}(c_i \mid I, Q)$$

- **变量含义**：$w_i$ 为第 $i$ 级的预设权重，$P_{\mathrm{LMM}}(c_i \mid I, Q)$ 为 LMM 在给定图像 $I$ 和问题 $Q$ 条件下对第 $i$ 级类别 $c_i$ 的预测概率。
- **用途**：用于评估 **Blending Naturalness** 和 **Generative/Editing Artifacts** 等主观整体维度。

**公式 (2) — Score_Hybrid-Sim（混合特征相似度）**

$$\mathrm{Score}_{\mathrm{Hybrid\text{-}Sim}} = \frac{f_{\mathrm{orig}} \cdot f_{\mathrm{gen}}}{||f_{\mathrm{orig}}|| \cdot ||f_{\mathrm{gen}}||}$$

- **变量含义**：$f_{\mathrm{orig}}$ 和 $f_{\mathrm{gen}}$ 分别为原始图像与生成图像在目标区域（非编辑区域或主体区域）的专家模型特征向量。
- **用途**：用于评估 **Non-Edited Fidelity** 和 **Subject Identity Fidelity**，通过 LMM 语义分割定位目标区域后，由专家模型提取特征并计算余弦相似度。

**公式 (3) — Score_Multi-VQA（多问题 VQA 评分）**

$$\mathrm{Score}_{\mathrm{Multi\text{-}VQA}} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}(\mathrm{LMM}(I_{\mathrm{gen}}, I_{\mathrm{orig}}, Q_i) = \text{`Yes'})$$

- **变量含义**：$N$ 为问题总数，$\mathbb{I}(\cdot)$ 为指示函数，当 LMM 对第 $i$ 个问题 $Q_i$ 的回答为“Yes”时取 1，否则取 0。
- **用途**：用于评估 **Physical Plausibility**、**Composition & Interaction** 等需要多角度语义判断的复杂概念。

**公式 (4) — Score_2-level（二元 VQA 评分）**

$$\mathrm{Score}_{2\text{-level}} = P_{\mathrm{LMM}}(\text{`Yes'} \mid I, Q)$$

- **变量含义**：$P_{\mathrm{LMM}}(\text{`Yes'} \mid I, Q)$ 为 LMM 在给定图像 $I$ 和问题 $Q$ 条件下输出“Yes”的概率。
- **用途**：用于评估事实性任务（如指令遵循的二元判断）的成功概率，其概率输出允许以 0.5 为阈值直观分类操作是否“成功”。

**公式 (5) — Score_final（文本渲染分段评分）**

$$\mathrm{Score}_{\mathrm{final}} = \left(\frac{S_s - 1}{4}\right) \times \begin{cases} 1.0 & \text{if } S_c = 1.0 \\ 0.8 & \text{if } 0.8 \leq S_c < 1.0 \\ 0.5 & \text{if } 0.6 \leq S_c < 0.8 \\ 0.1 & \text{if } S_c < 0.6 \end{cases}$$

- **变量含义**：$S_s$ 为 LMM 评估的文本风格分数（1–5 级），$S_c$ 为 OCR 工具评估的内容准确度分数（0–1）。
- **用途**：用于 **Text Content & Style** 维度，融合内容准确度与风格质量，通过分段惩罚机制确保内容正确性是风格评分的前提。

### 人类偏好标注协议与 Win Ratio

为验证自动化评估与人类判断的一致性，I2I-Bench 设计了 **Human Preference Annotation Protocol**。标注者对不同模型在同一提示下的编辑结果进行成对比较，判断孰优孰劣或平局。基于成对结果，每个模型在每个维度上计算 **Win Ratio**：

$$\text{Win Ratio} = \frac{\text{胜场数} \times 1 + \text{平局数} \times 0.5 + \text{负场数} \times 0}{\text{总比较次数}}$$

该指标用于与自动化评估分数进行皮尔逊相关性分析，验证混合评估设计的有效性。质量控制方面，采用 20% 随机抽样和 10% 错误率阈值确保标注可靠性。

## 实验与分析

### 主结果：单图像与多图像编辑基准

I2I-Bench对9个单图像编辑（SE）模型和4个多图像编辑（ME）模型进行了系统评估，结果分别呈现在Table 1和Table 2中。所有分数均归一化至[0,1]区间，分数越高代表性能越好。

在单图像编辑任务中，**Qwen-Image-Edit-2509**以0.813的归一化总分位居榜首，紧随其后的是Step1X-Edit（0.773）和UniPic-2（0.767）。与之形成鲜明对比的是，传统的instruct-pix2pix仅获得0.416分，成为表现最差的模型。这一巨大差距（+0.397）不仅反映了模型代际间的能力跃迁，更揭示了I2I-Bench对模型能力的细粒度区分力。在物理合理性（Physical Plausibility）这一关键维度上，Step1X-Edit以0.537领先，而instruct-pix2pix仅得0.348，表明较新的模型在理解物理世界约束方面取得了实质性进展。

在多图像编辑任务中，整体性能普遍低于单图像编辑，凸显了跨图像一致性编辑的固有难度。**Nano-Banana**以0.636的总分领先，而Omnigen2仅得0.545，成为ME模型中的最低分。值得注意的是，在世界知识与推理（World Knowledge & Reasoning）维度上，Nano-Banana取得了0.721的高分，而Omnigen2几乎完全失败（0.038），差距高达0.683。这一极端分化表明，当前多图像编辑模型在需要深层语义理解和跨图像逻辑推理的任务上能力严重不足，多数模型仅擅长浅层的视觉操作。

Figure 3的能力雷达图进一步可视化了这一分化格局。在SE模型的基础质量维度（Blending Naturalness、Editing Artifacts）上，Qwen-Image-Edit-2509表现卓越；而在任务执行维度上，各模型的能力分布呈现明显的层次化结构。ME模型的雷达图则显示，除Nano-Banana外，其余模型在多个维度上均存在明显短板。

### 任务复杂度对模型性能的影响

Figure 4揭示了模型性能随任务认知复杂度递增而下降的显著趋势。以SE任务中表现最佳的Qwen-Image-Edit-2509为例，随着任务从简单的“物体操作”逐渐过渡到需要深层推理的“世界知识与推理”，其在共享维度上的得分呈现单调递减。类似地，Nano-Banana在ME任务中的表现也随组合复杂度的增加而波动，在某些高复杂度组合任务上出现明显性能塌陷。

Figure 5展示了两个代表性模型从SE到ME任务的性能迁移。Qwen-Image-Edit-2509在共享维度上的ME得分普遍低于其SE得分，表明即使是顶级SE模型，在面对多图像编辑的跨图像一致性要求时仍面临显著挑战。Omnigen2的SE与ME性能差距更为突出，进一步验证了多图像编辑作为独立能力维度的必要性。

### 人类对齐验证与混合设计消融

I2I-Bench的核心创新在于其混合评估范式——将专用“专家”工具与通用大模型（LMM）相结合。Table 3的消融实验为这一设计提供了决定性的证据支持。

在单图像编辑的整体人类对齐相关性上，I2I-Bench的混合管道取得了**ρ=0.9425**的皮尔逊相关系数，而仅使用通用LMM的纯基线（VQA-5level）仅为ρ=0.7277。这一差距在特定维度上更为悬殊：在美学质量（Aesthetic-Quality）评估上，纯LMM基线表现出**负相关性（ρ=-0.0643）**，意味着其评估结果与人类偏好几乎背道而驰；而I2I-Bench通过引入专用专家模型ArtiMuse，相关性飙升至**ρ=0.9889**。这无可辩驳地证明了：对于需要精确量化判断的维度（如美学、图像质量），通用LMM的语义理解能力远不足以替代专用工具。

在复杂语义维度上，混合设计的优势同样显著。主体身份忠实度（Subject Identity）维度上，I2I-Bench的混合相似度管道（Eq. (2)）达到ρ=0.9133，而纯LMM基线为-0.3494；非编辑区域忠实度（Non-Edited Fidelity）上，混合管道为ρ=0.8813，纯LMM基线为-0.2071。这些负相关结果表明，通用LMM在需要精确空间定位和特征比较的任务上存在系统性偏差，而混合管道中LMM负责语义分割、专家模型负责特征提取的分工设计有效解决了这一问题。

与现有评估基准**LMM4Edit**的直接对比（Table 6）进一步巩固了I2I-Bench的优势。在单图像编辑任务的几乎所有维度上，I2I-Bench的人类相关性均显著优于LMM4Edit，验证了层次化解耦框架和混合评估策略的综合有效性。

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/012_Table_6.jpg]]
*Table 6: Comparison of Pearson’s Rho correlation with human preference between LMM4Edit and our method (Ours) on the I2I-Bench Single-Image Editing task. Our method demonstrates significant superiority across almost all dimensions*

### 失败模式与评估局限

尽管整体人类对齐表现优异，分析仍揭示了若干值得关注的失败模式：

1. **通用LMM的固有偏见**：消融实验中纯LMM基线在多个维度上的负相关性表明，当前通用大模型（Qwen3-VL-8B-Instruct）在美学判断、空间精确性等任务上存在难以通过简单提示工程消除的系统性偏见。这意味着I2I-Bench的评估结果在一定程度上依赖于所选通才模型的质量，更换底层LMM可能导致评估分布偏移。

2. **多图像编辑的评估覆盖不足**：ME任务仅定义了6个特定评估维度，某些关键的跨图像交互（如光照一致性、透视连贯性）尚未被显式建模。Nano-Banana在世界知识维度上的绝对领先可能掩盖了其在其他未覆盖维度上的潜在缺陷。

3. **人工验证的样本量限制**：尽管采用了20%随机抽样和10%错误率阈值的质量控制机制，每个维度的成对比较样本量约为85项。对于高度主观的维度（如混合自然度），这一样本量可能不足以捕捉人类偏好的全部方差。

4. **固定提示集的分布偏差**：1000条提示虽经精心设计，但作为静态集合，无法保证覆盖真实世界中编辑请求的长尾分布。某些任务类别（如文本渲染、世界知识）的提示配额（见Table 4和Table 5）可能不足以充分压力测试模型的极限能力。

### 补充图表

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/003_Table_1.jpg]]
*Table 1: Results of the single-image editing benchmark. All scores are normalized; higher is better. Best scores are highlighted*

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/004_Table_2.jpg]]
*Table 2: Results of the multi-image editing benchmark. All scores are normalized; higher is better. Best scores are highlighted*

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/005_Figure_3.jpg]]
*Figure 3: Capability radar charts for the evaluated models on key dimensions. (a) Foundational Quality & Fidelity (SE models). (b) Task Execution & Advanced Capabilities (SE models). (c) Foundational Quality & Fidelity (ME models). (d) Task Execution & Advanced Capabilities (ME models)*

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/006_Table_3.jpg]]
*Table 3: Human Preference Alignment and Ablation Study. This table presents the Pearson correlation (ρ) coefficients between I2I-Bench automated metrics and human preferences (Win Ratio). The results show extremely high consistency across all 30 dimensions, strongly validating the reliability of our evaluation methodology. The table also presents an ablation study comparing our hybrid I2I-Bench pipeline vs. a Pure LMM-Baseline (general LMM VQA-5level), which validates our hybrid design*

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/007_Figure_4.jpg]]
*Figure 4: Performances of top-performing SE and ME models on common dimensions across task categories. (1) The performance of Qwen-Image-Edit-2509 (SE) as task cognitive complexity increases. (2) The performance of nano-banana (ME) varies across complex combination tasks*

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/009_Figure_5.jpg]]
*Figure 5: Performance comparison between Single-Image Editing (SE) and Multi-Image Editng (ME) tasks for Qwen-Image-Edit-2509 and Omnigen2 on shared dimensions*

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/010_Table_5.jpg]]
*Table 5: Prompt Quota for Multi-Image Editing (ME) Dimensions*

![[assets/figures/papers/paper_list_l756_https_arxiv_org_abs_2512_04660/figures/011_Table_4.jpg]]
*Table 4: Prompt Quota for Single-Image Editing (SE) Dimensions*

## 方法谱系与知识库定位

### 评估基准的演化脉络

图像编辑评估长期依赖两类范式：**传统像素级指标**（PSNR、SSIM、LPIPS）与**人工主观评分**。前者仅反映低层信号保真度，无法捕捉语义编辑的成败；后者虽贴近人类感知，但成本高昂、难以复现，且现有标注协议（如单图绝对评分）在细粒度维度上一致性不足。近年来出现的**基于大模型的自动评估方法**试图弥合这一鸿沟，其中代表性工作包括 **LMM4Edit**（基于LMM的自动评估基准），但其任务覆盖与评估维度仍较为有限，且缺少系统的人类对齐验证。

I2I-Bench 在该谱系中的定位是 **首个覆盖单图像与多图像编辑、融合专家工具与通用大模型的混合自动化评估基准**。其核心推进体现在三个层面：

1. **任务广度**：从单一的单图像编辑扩展至5类递增认知复杂度的多图像编辑任务（如主体合成、跨图像世界知识与推理），这是现有基准尚未涉足的领域。
2. **评估深度**：将评估解耦为30个细粒度维度，覆盖基础质量、任务执行、物理合理性、组合交互等层次，而非笼统的“整体质量”评分。
3. **方法范式**：提出“专家+通才”混合管道——专用工具（如 **Q-Insight** 用于整体质量、**ArtiMuse** 用于美学质量）提供精确分数预测，通用大模型（**Qwen3-VL-8B-Instruct**）通过VQA处理语义理解。消融实验（Table 3）表明，纯LMM基线在美学质量维度甚至出现负相关（ρ = -0.0643），而混合管道达到 ρ = 0.9889，验证了专家模型在特定维度上不可替代。

### 与相关工作的关键差异

| 维度 | 传统方法（PSNR/LPIPS等） | LMM4Edit 等早期自动基准 | **I2I-Bench（本工作）** |
|------|--------------------------|------------------------|------------------------|
| 任务覆盖 | 不限，但无任务导向评估 | 主要单图像编辑，类别有限 | 10类任务，含5类多图像编辑 |
| 评估粒度 | 像素级 | 有限维度 | 30个解耦细粒度维度 |
| 评估方法 | 数学公式 | 纯LMM评分 | 专家工具 + LMM 混合管道 |
| 人类对齐验证 | 部分指标有验证 | 缺乏或有限 | 大规模成对比较，ρ 达优秀水平 |
| 可复现性 | 完全可复现 | 依赖特定LMM | 定义标准化管道，但依赖特定通才模型 |

与 **LMM4Edit** 的直接对比（Table 6）显示，I2I-Bench 在人类偏好相关性上显著优于前者，进一步确认了混合设计的有效性。

### 适用边界与局限

**适用场景**：该基准专为**基于指令的图像编辑模型**设计，评估其遵循自然语言提示修改输入图像的能力。其提示集经过精心设计，覆盖了从简单物体操作到复杂世界知识推理的认知梯度，适合作为模型能力诊断工具。

**已知局限**：

1. **任务范式受限**：当前基准仅覆盖指令驱动的图像编辑，未纳入图像补全、风格迁移、交互式编辑等其他重要范式。将这些任务纳入统一评估框架仍是开放问题。

2. **通才模型的固有偏见**：自动化评估依赖 Qwen3-VL-8B-Instruct 作为语义判断的“通才”，该模型的内在偏见（如对某些视觉概念的敏感度差异）可能影响特定维度的评估客观性。如何设计不绑定特定供应商的评估体系，是需要持续关注的方向。

3. **多图像评估维度不足**：多图像编辑仅定义了6个特定维度，某些复杂的跨图像交互（如全局光照一致性、多主体间的物理遮挡合理性）尚未完全覆盖，可能低估或高估模型在真实应用中的表现。

4. **人工验证规模有限**：人类偏好对齐验证的样本量约为每维度85项成对比较，虽已显示高相关性，但可能不足以捕捉所有类型的评估偏差，尤其在长尾任务上。

### 开放问题

- **评估维度的可扩展性**：如何进一步扩展评估维度以覆盖更广泛的世界知识应用（如文化符号理解）和抽象逻辑推理（如反事实编辑），同时保持评估管道的可复现性？
- **专家模型的可替代性**：当前混合框架中的专用工具（Q-Insight、ArtiMuse等）能否被更统一、更通用的方法替换以降低系统复杂度，同时不牺牲与人类偏好的对齐度？
- **跨模态泛化**：该基准的层次化评估思想如何泛化到视频编辑、3D内容编辑等新兴任务？多帧时序一致性、三维几何合理性等维度的自动化评估仍待探索。
- **基准的可持续更新**：随着编辑模型能力提升，固定的1000条提示集可能逐渐饱和。如何设计动态更新的提示生成机制，使其持续反映真实世界的编辑需求分布？

## 原文 PDF

![[paperPDFs/CVPR_2026/I2I_Bench_A_Comprehensive_Benchmark_Suite_for_Image_to_Image_Editing_Models.pdf]]
