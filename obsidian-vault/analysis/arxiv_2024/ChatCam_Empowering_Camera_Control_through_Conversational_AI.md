---
title: "ChatCam: Empowering Camera Control through Conversational AI"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/ChatCam_Empowering_Camera_Control_through_Conversational_AI.pdf
project_link: null
code_link: null
aliases:
- ChatCam
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: CineGPT文本条件轨迹生成模型与Anchor Determinator场景锚点确定机制的组合，通过LLM代理分解复杂指令并协调两者，实现精准、可控的轨迹生成与放置。
primary_logic: 将相机轨迹离散化为token序列，利用GPT架构实现文本到轨迹的自回归生成；同时借助CLIP相似度与梯度优化在辐射场中定位锚点，使生成轨迹与场景对象对齐；再由LLM代理进行任务规划、原子轨迹调用与仿射变换拼接，完成符合复杂语言指令的相机操作。
claims:
- 与移除锚点确定模块的变体相比，完整ChatCam模型的平移均方误差从16.2降至5.3，旋转均方误差从8.5降至2.9，表明场景锚点对轨迹放置精度至关重要。
- 用户研究中，ChatCam在视觉质量（84.9分）和对齐度（67.9分）上均显著优于SA3D、LERF等基线方法，证明其生成的视频更符合人类偏好。
- 消融实验显示，代理语言模型使用GPT-4相比LLaMA-2带来更高的轨迹准确性，说明更强的大语言模型对任务分解和工具调用的有效性。
- 多种室内/室外/人像3D场景（辐射场渲染） 上 Translation MSE (×10⁻²) = 5.3
---

# ChatCam: Empowering Camera Control through Conversational AI

> [!tip] 核心洞察
> 将相机轨迹离散化为token序列，利用GPT架构实现文本到轨迹的自回归生成；同时借助CLIP相似度与梯度优化在辐射场中定位锚点，使生成轨迹与场景对象对齐；再由LLM代理进行任务规划、原子轨迹调用与仿射变换拼接，完成符合复杂语言指令的相机操作。

| 字段 | 内容 |
|------|------|
| 中文题名 | ChatCam：通过对话式AI赋能相机控制 |
| 英文题名 | ChatCam: Empowering Camera Control through Conversational AI |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2409.17331) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ChatCam |
| Dataset | 多种室内/室外/人像3D场景（辐射场渲染） |

> [!tip] 效果简介
> - 多种室内/室外/人像3D场景（辐射场渲染） 上，Translation MSE (×10⁻²) 5.3 vs 16.2 (w/o Anchor) (-10.9 (更优))。
> - 多种室内/室外/人像3D场景 上，Rotation MSE (×10⁻²) 2.9 vs 8.5 (w/o Anchor) (-5.6 (更优))。
> - 用户研究（视觉质量偏好） 上，Visual Quality (用户偏好百分比) 84.9 vs SA3D / LERF (得分更低) (显著领先)。

## 概要

**问题瓶颈**：现有相机控制方法存在两个关键断层——（1）无法根据自然语言自动生成相机轨迹，用户必须手动提供精确的轨迹参数；（2）缺乏将轨迹与具体3D场景对象绑定的机制，导致无法实现精准的对象导向拍摄。这两个断层使得普通用户难以通过语言指令获得符合意图的渲染视频。

**核心方案**：ChatCam 提出了一套对话式AI赋能的相机控制系统，其核心洞察在于将相机轨迹离散化为token序列，利用GPT架构实现文本到轨迹的自回归生成；同时借助CLIP相似度与梯度优化在辐射场中定位场景锚点，使生成轨迹与具体对象对齐；再由LLM代理进行任务规划、原子轨迹调用与仿射变换拼接，完成符合复杂语言指令的相机操作。

**方法定位**：ChatCam 在方法谱系上填补了“文本条件轨迹生成”与“场景感知轨迹放置”之间的空白。与基于3D分割的相机放置方法（如SA3D）和语言嵌入辐射场定位方法（如LERF）相比，ChatCam 不依赖用户手动指定轨迹，也不将相机简单绑定到语义区域，而是通过**CineGPT**（GPT架构的文本条件轨迹生成模型）与**Anchor Determinator**（CLIP初选+梯度优化的锚点精化模块）的组合，配合**LLM代理**（GPT-4）的任务编排，实现了从自然语言到场景对齐轨迹的端到端生成。

**主要结果**：定量实验中，完整ChatCam模型的平移均方误差为5.3（×10⁻²），旋转均方误差为2.9（×10⁻²），相比移除锚点确定模块的变体（分别为16.2和8.5）有显著提升（Table 1）。用户研究中，ChatCam在视觉质量（84.9分）和对齐度（67.9分）上均显著优于SA3D、LERF等基线方法（Table 1）。消融实验进一步表明，使用GPT-4作为代理语言模型相比LLaMA-2能带来更高的轨迹准确性（Table 1）。

**局限与开放问题**：CineGPT的训练依赖手动构建的约1000条相机轨迹数据集，规模较小，可能限制模型泛化能力；锚点确定依赖辐射场训练时的多视角输入图像作为先验；当前方法假设场景为静态，尚未处理动态对象或动态环境下的相机控制。

在视觉内容创作中，相机控制是决定叙事表达和视觉质量的核心环节。无论是电影拍摄、虚拟现实体验还是3D场景渲染，相机轨迹的设计直接影响观众的注意力引导和空间感知。然而，现有相机控制方法存在一个根本性瓶颈：**用户必须手动提供相机轨迹，且缺乏将轨迹与具体3D场景对象绑定的机制**。这意味着创作者不仅需要具备专业的相机操作知识，还必须逐帧指定相机的旋转、平移和内参，无法通过自然语言直接描述拍摄意图。

近年来，辐射场表示（如NeRF、3D Gaussian Splatting）的进展使得高质量新视角合成成为可能，但相机路径的生成仍主要依赖手工设计或启发式规则。一些工作尝试通过语言嵌入在辐射场中定位语义区域（如**LERF**），或基于3D分割结果放置相机（如**SA3D**），但这些方法仅能确定静态的相机位置，无法生成符合复杂语言指令的连续相机轨迹，更无法实现“围绕花瓶旋转并逐渐拉近”这类需要时序动作组合的拍摄操作。

上述缺口揭示了一个因果调控瓶颈：**文本到轨迹的生成能力缺失**与**场景锚点绑定机制缺失**共同构成了当前系统的关键限制。具体而言：(1) 相机轨迹是连续高维信号，如何将其转化为可被语言模型处理的离散表示，并实现文本条件的自回归生成，是一个未被充分探索的问题；(2) 即使生成了轨迹，如何将其精确放置到辐射场中的目标对象位置（如“聚焦于桌上的红色杯子”），需要将语言语义与3D空间坐标可靠对齐，而现有方法在此环节的精度严重不足。

ChatCam正是在这一背景下提出的。其核心动机是通过对话式AI赋能相机控制，使用户能够以自然语言交互的方式描述拍摄意图，由系统自动生成精确、可控的相机轨迹并渲染视频。这一目标的实现依赖于三个关键洞察：(1) 将相机轨迹离散化为token序列，利用GPT架构实现文本到轨迹的自回归生成；(2) 借助CLIP相似度与梯度优化在辐射场中定位锚点，使生成轨迹与场景对象对齐；(3) 由LLM代理进行任务规划、原子轨迹调用与仿射变换拼接，完成符合复杂语言指令的相机操作。

## 核心方法与创新机理

ChatCam 的核心创新在于构建了一条从自然语言指令到场景绑定相机轨迹的端到端生成通路。其关键突破可归结为三个相互协同的 **changed slots**，它们共同解决了现有相机控制方法中“轨迹需手动提供”与“轨迹无法与场景对象对齐”的双重瓶颈。

### 1. 文本条件轨迹生成：CineGPT

**基线状态**：现有方法依赖用户手动提供相机轨迹，不存在从文本到轨迹的自动生成机制。

**创新机制**：CineGPT 将相机轨迹离散化为 token 序列，借助 GPT 架构实现自回归的文本条件轨迹生成。具体而言，一条 $M$ 帧的相机轨迹 $c_{1:M} = \{(\mathbf{R}_i, \mathbf{t}_i, \mathbf{K}_i)\}_{i=1}^{M}$ 首先通过基于 VQ-VAE 的轨迹分词器进行压缩与量化，将每帧参数映射到码本中的离散 token：
$$z_i = Q(\hat{z}_i) = \arg\min_{z_k \in Z} \|\hat{z}_i - z_k\|_2^2$$
随后，一个跨模态 Transformer 在成对的文本-轨迹数据上以语言建模目标进行微调：
$$\mathcal{L}_{\mathrm{LM}} = -\sum_{i=1}^{N_t} \log p_{\theta}(x_t^i | x_t^{<i}, x_s)$$
该设计使得模型能够根据文本描述 $x_s$ 自回归地预测目标轨迹 token 序列，首次实现了从自然语言到相机轨迹的直接映射。

### 2. 场景锚点确定：Anchor Determinator

**基线状态**：现有方法缺乏将生成轨迹与具体 3D 场景对象绑定的机制，导致轨迹放置漂移或穿模。

**创新机制**：Anchor Determinator 通过两阶段流程将文本描述定位为辐射场中的精确锚点。第一阶段利用 CLIP 在训练视图集中进行粗选：
$$i_{\mathrm{anchor}} = \arg\max_i \frac{f_{\mathrm{image}}(I_i) \cdot f_{\mathrm{text}}(T)}{\|f_{\mathrm{image}}(I_i)\| \|f_{\mathrm{text}}(T)\|}$$
第二阶段以该视图的相机参数为初始值，通过梯度下降最小化渲染视图与文本提示的负 CLIP 相似度来精化锚点位置：
$$\min_c \mathcal{L}_{\mathrm{anchor}}(c) = -\frac{f_{\mathrm{image}}(R(c)) \cdot f_{\mathrm{text}}(T)}{\|f_{\mathrm{image}}(R(c))\| \|f_{\mathrm{text}}(T)\|}$$
$$c_{t+1} = c_t - \eta \nabla_c \mathcal{L}_{\mathrm{anchor}}(c_t)$$
这一机制使生成的原子轨迹能够通过仿射变换与场景中的特定对象对齐，从根本上解决了轨迹放置精度问题。消融实验（Table 1）提供了决定性证据：移除该模块后，平移 MSE 从 5.3 飙升至 16.2，旋转 MSE 从 2.9 升至 8.5。

### 3. LLM 代理的任务编排

**基线状态**：单步模型调用，缺乏对复杂指令的高层规划与多工具协调能力。

**创新机制**：ChatCam 引入 GPT-4 作为核心代理，执行“观察-推理-规划-调用”的认知循环。代理首先解析用户的自然语言指令，将其分解为可执行的子任务；随后决策锚点在最终轨迹中的角色（作为某段原子轨迹的起点或终点），并依次调用 CineGPT 生成原子轨迹、调用 Anchor Determinator 定位锚点；最后通过仿射变换将多段原子轨迹与锚点对齐拼接为完整轨迹。消融实验同样证实了该设计的必要性：将代理语言模型从 GPT-4 替换为 LLaMA-2 后，轨迹准确性显著下降，表明更强的大语言模型在任务分解与工具调用中的有效性。

### 创新协同

三个 changed slots 并非孤立运作，而是形成了因果闭环：CineGPT 解决了“生成什么轨迹”的问题，Anchor Determinator 解决了“轨迹放在哪里”的问题，LLM 代理则解决了“如何组合执行”的问题。这种分工使得 ChatCam 在用户研究中以 84.9% 的视觉质量偏好和 67.9% 的文本对齐偏好显著领先于 SA3D、LERF 等基线方法（Table 1），并能在定性对比中避免将相机移动至物体内部等不合理位置（Figure 6）。

ChatCam 的整体设计围绕一个核心瓶颈展开：现有相机控制方法无法根据自然语言自动生成相机轨迹，且缺乏将轨迹与具体 3D 场景对象绑定的机制。为解决这一问题，ChatCam 构建了一个以 **LLM 代理（GPT-4）为中枢、CineGPT 与 Anchor Determinator 为双工具** 的对话式相机控制系统。其核心洞察在于：将相机轨迹离散化为 token 序列，利用 GPT 架构实现文本到轨迹的自回归生成；同时借助 CLIP 相似度与梯度优化在辐射场中定位锚点，使生成轨迹与场景对象对齐；再由 LLM 代理进行任务规划、原子轨迹调用与仿射变换拼接，完成符合复杂语言指令的相机操作。

### 输入输出流

系统接受用户的**自然语言指令**（如“请围绕桌子旋转一圈并拉近镜头”）作为输入，输出一段可直接用于辐射场渲染的**相机轨迹**。该轨迹由 $M$ 帧相机参数序列构成 $c_{1:M} = \{(\mathbf{R}_i, \mathbf{t}_i, \mathbf{K}_i)\}_{i=1}^{M}$，涵盖旋转、平移和内参，最终渲染为视频。

### 模块关系与执行流程

整个 pipeline 由三个核心模块串联协作完成（参见 Figure 2）：

1. **LLM Agent（GPT-4）——任务编排中枢**
   LLM 代理负责解析用户指令，执行“观察-推理-规划”的认知链条：首先观察场景的可用信息，然后推理用户意图，最后制定工具调用计划。它将复杂指令分解为可执行的子任务，决定何时调用 CineGPT 生成原子轨迹、何时调用 Anchor Determinator 定位场景锚点。

2. **CineGPT——文本条件轨迹生成器**
   CineGPT 是一个基于 GPT 架构的自回归模型，专门用于从文本描述生成相机轨迹。其工作流程为：先通过基于 VQ-VAE 的轨迹分词器将连续轨迹压缩并量化为离散 token 序列，再利用跨模态 Transformer 学习文本与轨迹 token 之间的映射关系，实现文本到轨迹的自回归生成。训练时采用负对数似然损失 $\mathcal{L}_{\mathrm{LM}} = -\sum_{i=1}^{N_t} \log p_{\theta}(x_t^i | x_t^{<i}, x_s)$，以源序列 $x_s$ 为条件预测目标 token。

3. **Anchor Determinator——场景锚点定位器**
   该模块确保生成的轨迹能够精准放置在 3D 场景中的目标对象附近。其执行分为两步：首先通过 CLIP 余弦相似度从训练视图集中选出与文本提示最匹配的图像作为初始锚点 $i_{\mathrm{anchor}} = \arg\max_i \frac{f_{\mathrm{image}}(I_i) \cdot f_{\mathrm{text}}(T)}{\|f_{\mathrm{image}}(I_i)\| \|f_{\mathrm{text}}(T)\|}$；随后通过梯度下降优化锚点相机参数，最小化渲染视图与文本提示的负 CLIP 相似度 $\min_c \mathcal{L}_{\mathrm{anchor}}(c) = -\frac{f_{\mathrm{image}}(R(c)) \cdot f_{\mathrm{text}}(T)}{\|f_{\mathrm{image}}(R(c))\| \|f_{\mathrm{text}}(T)\|}$，更新规则为 $c_{t+1} = c_t - \eta \nabla_c \mathcal{L}_{\mathrm{anchor}}(c_t)$。

4. **轨迹合成**
   LLM 代理获取 CineGPT 生成的原子轨迹与 Anchor Determinator 定位的锚点后，决定锚点在最终轨迹中的角色（作为某段原子轨迹的起点或终点），然后通过仿射变换将原子轨迹与锚点对齐并拼接，形成完整的相机轨迹。

### 关键设计决策的因果逻辑

- **为什么需要 LLM 代理？** 消融实验（Table 1）表明，将 GPT-4 替换为 LLaMA-2 后轨迹准确性下降，说明更强的语言模型在任务分解与工具调用中更有效。LLM 代理的存在使得系统能够处理“围绕桌子旋转一圈，然后推近到花瓶”这类需要多步原子操作组合的复杂指令。
- **为什么需要 Anchor Determinator？** 移除该模块后，平移均方误差从 5.3 升至 16.2，旋转均方误差从 2.9 升至 8.5（Table 1），证明场景锚点对轨迹放置精度至关重要。没有锚点机制，生成的轨迹无法与场景中的具体对象对齐，导致相机可能移动到不合理位置（如穿入物体内部，见 Figure 6 的定性对比）。

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2409_17331/figures/002_Figure.jpg]]

ChatCam 的核心由三个功能模块构成：**CineGPT**（文本条件轨迹生成）、**Anchor Determinator**（场景锚点确定）和 **LLM Agent**（任务规划与工具编排）。三者通过 LLM 代理的观察-推理-规划流程协同工作，将自然语言指令转化为与具体 3D 场景对象对齐的相机轨迹。

### CineGPT：文本条件轨迹生成

CineGPT 的目标是实现从自然语言描述到相机轨迹的跨模态映射。其设计包含两个阶段：轨迹离散化和跨模态自回归建模。

**轨迹参数化与离散化。** 一条包含 $M$ 帧的相机轨迹被参数化为旋转、平移和内参的序列：

$$c_{1:M} = \{c_i\}_{i=1}^{M} = \{(\mathbf{R}_i, \mathbf{t}_i, \mathbf{K}_i)\}_{i=1}^{M}$$

为将连续轨迹转换为可被语言模型处理的离散 token 序列，ChatCam 采用基于 VQ-VAE 架构的轨迹分词器。编码器将轨迹映射为潜在向量 $\hat{z}_i$，再通过向量量化将其映射到码本中最近的条目：

$$z_i = Q(\hat{z}_i) = \arg\min_{z_k \in Z} \|\hat{z}_i - z_k\|_2^2$$

**跨模态自回归建模。** CineGPT 基于 GPT 架构，在联合语言-轨迹空间中进行自回归生成。给定源序列 $x_s$（文本描述或轨迹 token），模型以自回归方式预测目标序列 $x_t$ 的下一个 token，训练损失为标准语言建模负对数似然：

$$\mathcal{L}_{\mathrm{LM}} = -\sum_{i=1}^{N_t} \log p_{\theta}(x_t^i \mid x_t^{<i}, x_s)$$

通过在约 1000 条手动构建的文本-轨迹配对数据上进行监督微调，CineGPT 学会了从文本描述生成对应相机轨迹的能力。

### Anchor Determinator：场景锚点确定

仅生成轨迹不足以实现精准拍摄——轨迹必须与 3D 场景中的具体对象对齐。Anchor Determinator 通过两阶段流程解决这一问题。

**初始锚点选择。** 给定文本描述 $T$，从辐射场训练时的输入视图集 $\{I_i\}$ 中，选出 CLIP 余弦相似度最高的图像作为初始锚点：

$$i_{\mathrm{anchor}} = \arg\max_i \frac{f_{\mathrm{image}}(I_i) \cdot f_{\mathrm{text}}(T)}{\|f_{\mathrm{image}}(I_i)\| \|f_{\mathrm{text}}(T)\|}$$

**锚点梯度精化。** 初始选择仅为近似解，系统随后在辐射场中通过梯度下降进一步优化相机参数 $c$。优化目标是最小化渲染视图 $R(c)$ 与文本提示之间的负 CLIP 相似度：

$$\min_c \mathcal{L}_{\mathrm{anchor}}(c) = -\frac{f_{\mathrm{image}}(R(c)) \cdot f_{\mathrm{text}}(T)}{\|f_{\mathrm{image}}(R(c))\| \|f_{\mathrm{text}}(T)\|}$$

参数更新遵循梯度下降规则：

$$c_{t+1} = c_t - \eta \nabla_c \mathcal{L}_{\mathrm{anchor}}(c_t)$$

通过这一流程，Anchor Determinator 能够在辐射场中精确定位与文本描述语义对齐的相机位姿。

### LLM Agent：任务编排与轨迹合成

LLM Agent（基于 GPT-4）作为系统的中央协调器，负责解析用户复杂指令、分解子任务并调用上述两个工具。其工作流程为：观察场景信息 → 推理用户意图 → 规划原子轨迹生成与锚点确定 → 将 CineGPT 生成的原子轨迹通过仿射变换与 Anchor Determinator 确定的锚点对齐并拼接为最终轨迹。锚点可作为原子轨迹的起点或终点，确保合成轨迹在 3D 空间中的精确定位。

### 模块间因果机制

三个模块的协同构成了 ChatCam 的核心因果链路：LLM Agent 提供高层任务分解能力，CineGPT 提供文本到轨迹的生成能力，Anchor Determinator 提供轨迹与场景对象的空间绑定能力。消融实验（Table 1）证实了这一链路的关键性——移除 Anchor Determinator 后，平移 MSE 从 5.3 升至 16.2，旋转 MSE 从 2.9 升至 8.5，验证了场景锚点对轨迹放置精度的决定性作用。

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2409_17331/figures/005_Figure_3.jpg]]
*Figure 3: (a) CineGPT. We quantize camera trajectories to sequences of tokens and adopt a GPTbased architecture to generate the tokens autoregressively. Learning trajectory and language jointly, CineGPT is capable of text-conditioned trajectory generation. (b) Anchor Determination. Given a prompt describing the image rendered from an anchor point, the anchor selector chooses the best matching input image. An anchor refinement procedure further fine-tunes the anchor position*

## 实验与关键发现

### 核心定量结果

ChatCam 在轨迹精度、视觉质量和文本对齐度三个维度上均展现出显著优势，相关数据汇总于 **Table 1**。

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2409_17331/figures/010_Table_1.jpg]]
*Table 1: Quantitative comparisons and evaluations. Our full model performs better than baselines and variants in terms of trajectory accuracy, visual quality, and alignment with input text*

**轨迹精度**：在涵盖室内、室外及人像的多种3D场景测试中，ChatCam 取得了平移均方误差（Translation MSE）5.3（×10⁻²）和旋转均方误差（Rotation MSE）2.9（×10⁻²）的最佳成绩。作为关键对照，移除 Anchor Determinator 的变体（w/o Anchor）平移 MSE 升至 16.2，旋转 MSE 升至 8.5，误差分别扩大了约 3 倍和 2.9 倍。这一对比直接验证了场景锚点机制对轨迹空间定位的决定性作用——缺乏锚点时，生成的轨迹无法准确对齐到用户指定的场景对象，导致大幅偏离目标位置。

**用户偏好**：在视觉质量（Visual Quality）的用户研究中，ChatCam 获得了 84.9% 的偏好率，在对齐度（Alignment）上获得 67.9% 的偏好率，均显著领先于 **SA3D** 和 **LERF** 等基线方法。这表明 ChatCam 生成的视频不仅渲染效果更优，而且其相机运动与用户输入的自然语言指令更为一致。

### 消融分析

**锚点确定模块的不可替代性**：如上所述，移除 Anchor Determinator 后，平移和旋转误差急剧上升，这从根本上证明了“文本到轨迹生成”若缺乏与具体3D场景的绑定机制，其输出将沦为无场景上下文的通用轨迹，无法满足“对准某个特定物体拍摄”的实际需求。

**代理语言模型的能力依赖性**：将 LLM 代理从 GPT-4 替换为 LLaMA-2 后，整体轨迹准确性出现明显下降（见 Table 1 消融行）。这一结果表明，ChatCam 的“观察-推理-规划-工具调用”流水线对大语言模型的任务分解与多模态指令跟随能力高度敏感。更强的模型能够更精准地将复杂自然语言指令拆解为可执行的子任务，并正确协调 CineGPT 与 Anchor Determinator 的调用顺序和参数传递。

### 定性对比与失败模式

**与基线的行为差异**：如 **Figure 6** 所示，SA3D 和 LERF 在某些场景下会将相机移动到不合理的空间位置（例如穿入物体内部），导致渲染视频出现视觉穿模或黑屏。ChatCam 通过锚点确定机制将轨迹起点/终点显式绑定到场景中的有效观测位置，从根源上避免了此类问题。

**复杂指令的执行能力**：**Figure 4** 和 **Figure 5** 的定性结果展示了 ChatCam 对专业电影术语（如“dolly zoom”）和多人物场景下复杂指令的理解与执行能力。系统能够正确生成包含平移、旋转和焦距变化的复合轨迹，并在多人物环境中准确锁定目标对象。

### 已知局限

1. **训练数据规模约束**：CineGPT 的训练依赖手动构建的约 1000 条相机轨迹数据集，规模有限，可能限制模型对长尾或高度复杂轨迹模式的泛化能力。
2. **场景先验依赖**：锚点确定流程需要辐射场训练时的多视角输入图像作为 CLIP 相似度计算的候选集，这意味着系统无法直接应用于仅有单张图像或缺乏预重建的场景。
3. **动态场景未覆盖**：当前方法假设场景为静态，尚未涉及动态对象或动态光照条件下的相机控制，这在实际应用（如拍摄移动人物）中可能构成限制。

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2409_17331/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparisons. Our approach avoids moving the camera to unreasonable positions such as inside objects, obtaining videos with better visual effects, and aligning best with input texts*

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2409_17331/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results on indoor and outdoor scenes. Visualizations of our generated trajectories from input text descriptions and the frames in the final rendered video. Our method is capable of understanding and executing instructions and providing correct translations, rotations, and camera focal lengths. Additionally, our method can comprehend more specialized terms such as “dolly zoom”*

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2409_17331/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results on human-centric scenes. Visualizations of our generated trajectories from input text descriptions and the frames in the final rendered video. Our method performs effectively in scenes with multiple humans*

## 定位与知识库关联

### 任务定位与核心瓶颈

ChatCam 面向的是**基于自然语言的相机控制与轨迹生成**任务，其核心瓶颈在于现有方法无法根据文本指令自动生成相机轨迹，且缺乏将轨迹与具体3D场景对象绑定的机制。传统方案要求用户手动提供轨迹参数或依赖预定义路径，而基于3D分割的**SA3D**和基于语言嵌入辐射场的**LERF**等方法虽能实现一定程度的语义定位，但无法生成符合复杂语言描述的动态相机运动轨迹。ChatCam通过引入CineGPT文本条件轨迹生成模型与Anchor Determinator场景锚点确定机制，在LLM代理的协调下填补了这一空白。

### 关键方法谱系

ChatCam的技术架构建立在三条方法线的交汇处：

**1. 自回归序列建模与轨迹生成。** CineGPT的核心设计借鉴了GPT架构的自回归生成范式，将相机轨迹通过VQ-VAE离散化为token序列，使轨迹生成转化为标准的序列预测问题。这一思路与VideoGPT、TATS等视频生成工作中的离散化策略一脉相承，但ChatCam首次将其应用于相机轨迹域，并实现了文本到轨迹的跨模态生成。轨迹分词器基于VQ-VAE架构（van den Oord et al., NeurIPS 2017），将连续轨迹参数压缩为离散码本索引，使GPT架构能够以统一的方式处理语言token和轨迹token。

**2. 语言驱动的3D场景理解与定位。** Anchor Determinator的设计延续了CLIP（Radford et al., ICML 2021）在开放词汇视觉定位中的应用范式。与LERF将语言嵌入蒸馏到辐射场中的方式不同，ChatCam采用了两阶段策略：首先利用CLIP相似度从训练视图集中选择初始锚点，再通过梯度优化在辐射场中精化锚点位置。这种设计避免了对辐射场训练过程的侵入式修改，同时保持了与场景表示的松耦合关系。

**3. LLM代理与工具调用。** ChatCam采用GPT-4作为中央代理，负责解析用户指令、分解任务并协调CineGPT和Anchor Determinator的调用。这一设计属于LLM-as-Agent范式（如Toolformer、AutoGPT等），但在相机控制这一特定领域实现了任务规划与工具组合的端到端集成。代理通过仿射变换将多个原子轨迹与锚点对齐并拼接为最终轨迹，完成了从高层语义指令到底层参数化轨迹的完整映射。

### 与基线方法的差异分析

相较于SA3D和LERF，ChatCam的差异化优势体现在三个层面：

- **轨迹生成能力：** SA3D和LERF仅能提供静态的相机位置建议，而ChatCam通过CineGPT可生成包含平移、旋转和焦距变化的完整动态轨迹。定量实验中，ChatCam的平移MSE为5.3（×10⁻²），旋转MSE为2.9（×10⁻²），移除锚点确定模块后分别升至16.2和8.5，验证了场景锚点对轨迹放置精度的关键作用（Table 1）。

- **物理合理性：** 定性对比（Figure 6）显示，ChatCam能避免将相机移动至物体内部等不合理位置，而SA3D和LERF在此类场景下可能出现穿模问题。这得益于锚点确定机制在辐射场中的梯度优化过程，使轨迹始终保持在有效观测空间内。

- **用户偏好：** 用户研究中ChatCam在视觉质量（84.9分）和对齐度（67.9分）上均显著领先基线方法（Table 1），表明其生成的视频更符合人类对语言指令的语义理解。

### 适用边界与局限

ChatCam的适用边界受以下因素制约：

- **数据依赖性：** CineGPT的训练依赖手动构建的约1000条相机轨迹数据集，规模较小，可能限制模型在极端或非典型轨迹模式上的泛化能力（Section 3.1）。轨迹的多样性和覆盖面直接影响生成质量的上限。

- **场景先验要求：** 锚点确定依赖辐射场训练时的输入图像作为候选视图集，因此系统需要场景的多视角图像作为先验（Section 3.2）。对于仅提供稀疏视图或未覆盖区域的场景，锚点选择的准确性可能下降。

- **静态场景假设：** 当前方法假设场景为静态，尚未处理动态对象或动态环境下的相机控制。在包含运动物体的场景中，预生成的轨迹可能无法适应场景变化，导致渲染视频中出现不自然的遮挡或错位。

- **代理模型依赖：** 消融实验显示，将LLM代理从GPT-4替换为LLaMA-2后轨迹准确性下降（Table 1），说明系统性能对底层大语言模型的能力有较强依赖，这在实际部署中可能带来成本和可控性的权衡。

### 开放问题与未来方向

基于上述分析，以下问题值得进一步探索：

- **轨迹数据的规模化获取：** 如何利用仿真环境或从视频中反向提取相机轨迹，以扩充CineGPT的训练数据，是提升模型泛化能力的关键方向。

- **动态场景扩展：** 将时间维度纳入轨迹生成和锚点确定过程，使系统能够处理包含运动对象的4D场景，是向真实应用迈进的重要一步。

- **多模态交互深化：** 当前系统以文本为主要交互模态，引入草图、示例视频或手势等多模态输入，可能进一步提升相机控制的直观性和精确度。

- **实时性与效率优化：** 锚点确定的梯度优化过程在推理时可能引入额外延迟，研究更高效的锚点定位策略（如直接回归或检索增强）对交互式应用至关重要。

## 原文 PDF

![[paperPDFs/arxiv_2024/ChatCam_Empowering_Camera_Control_through_Conversational_AI.pdf]]
