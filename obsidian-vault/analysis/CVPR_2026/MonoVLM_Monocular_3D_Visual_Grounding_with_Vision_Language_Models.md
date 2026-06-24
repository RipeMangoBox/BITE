---
title: "MonoVLM: Monocular 3D Visual Grounding with Vision Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MonoVLM_Monocular_3D_Visual_Grounding_with_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/hiyouga/EasyR1"
aliases:
- MonoVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用三阶段课程学习策略，依次训练2D定位、3D中心预测和完整3D框估计，并通过GRPO（Group Relative Policy Optimization）的复合奖励函数（3D IoU结合位置、尺寸和朝向奖励）进行强化学习优化。
primary_logic: 将复杂的单目3D定位任务分解为2D定位和3D几何推理两个子问题，利用相机反投影作为桥梁，通过分阶段强化学习使VLM逐步掌握从2D视觉线索推断3D属性的能力。这种分解不仅降低了学习难度，还通过奖励信号的协同效应提升了整体性能。
claims:
- 先导实验表明，仅以3D IoU为奖励时，模型在横向（x）和纵向（y）轴上的误差远大于深度（z）轴，这揭示了2D定位不准是3D误差的主要来源。
- 第二阶段训练中，优化3D中心预测奖励不仅提高了3D中心精度，还附带改善了2D定位，表明模型学会了2D-3D的对偶关系。
- 三阶段训练使MonoVLM-Qwen的mIoU从19.81单调提升至29.13，验证了课程学习的有效性。
- 在Mono3DRefer数据集上，MonoVLM-MiMo的总体mIoU达到38.11，是GPT-5（7.53）的5倍以上，并超越了专用纯视觉模型（如Mono3DVG-TGE在Multiple场景下Acc@0.25的71.23 vs 69.83）。
---

# MonoVLM: Monocular 3D Visual Grounding with Vision Language Models

> [!tip] 核心洞察
> 将复杂的单目3D定位任务分解为2D定位和3D几何推理两个子问题，利用相机反投影作为桥梁，通过分阶段强化学习使VLM逐步掌握从2D视觉线索推断3D属性的能力。这种分解不仅降低了学习难度，还通过奖励信号的协同效应提升了整体性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | MonoVLM：基于视觉语言模型的单目3D视觉定位 |
| 英文题名 | MonoVLM: Monocular 3D Visual Grounding with Vision Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Qu_MonoVLM_Monocular_3D_Visual_Grounding_with_Vision_Language_Models_CVPR_2026_paper.html) · [Code](https://github.com/hiyouga/EasyR1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MonoVLM |
| Dataset | Mono3DRefer |

> [!tip] 效果简介
> - Mono3DRefer 上，Overall mIoU 38.11 (MonoVLM-MiMo) vs 7.53 (GPT-5) (+30.58 (>5×))；Acc@0.25 Multiple 71.23 (MonoVLM-MiMo) vs 69.83 (Mono3DVG-TGE) (+1.40)。

## 概述

单目3D视觉定位要求模型根据自然语言描述，从单张RGB图像中预测目标的3D边界框。该任务同时考验2D视觉定位的精确性、3D几何推理能力以及对相机投影关系的理解。当前最先进的视觉语言模型（VLM），包括闭源的GPT-5、Gemini 2.5和开源的Qwen2.5-VL、MiMo-VL，在零样本条件下均严重缺乏上述能力：先导实验表明，即使仅以3D IoU为奖励进行强化学习优化，模型在横向（x）和纵向（y）轴上的误差远大于深度（z）轴，揭示出2D定位不准是制约3D性能的核心瓶颈（Table 1）。

**MonoVLM**针对这一瓶颈，提出三阶段课程学习策略，利用GRPO（Group Relative Policy Optimization）逐步赋予VLM从2D视觉线索推断3D属性的能力：第一阶段建立稳健的2D定位基础，第二阶段学习通过相机反投影从2D坐标和深度恢复3D中心，第三阶段以复合奖励（3D IoU结合位置、尺寸、朝向的指数衰减奖励）联合优化完整3D边界框的七参数表示 $(x, y, z, l, w, h, \theta)$。该分解策略不仅降低了学习难度，还通过奖励信号的协同效应使2D与3D定位能力相互促进。

在Mono3DRefer基准上，MonoVLM-MiMo的总体mIoU达到38.11，是GPT-5（7.53）的5倍以上，并在Multiple场景的Acc@0.25指标（71.23）上超越了专用纯视觉模型Mono3DVG-TGE（69.83）。消融实验证实，三阶段课程使mIoU单调提升（19.81→20.89→29.13），Stage 3中逐步加入位置、尺寸和朝向奖励使mIoU从21.31持续提升至29.13，验证了任务分解与复合奖励设计的有效性。

## 方法谱系与知识库定位

MonoVLM属于**基于VLM的3D视觉定位**方法，其核心贡献在于**训练策略**而非模型架构创新。与依赖专用检测头或深度估计网络的传统纯视觉方法（如**Mono3DVG**（Zhan et al., AAAI 2024）、Mono3DVG-TGE、Mono3D-VLDL）不同，MonoVLM直接将VLM作为预测模型，利用其内在的语言理解能力处理自然语言查询。与零样本VLM基线（GPT-5、Gemini 2.5、Qwen2.5-VL（Bai et al., arXiv 2025）、MiMo-VL）相比，MonoVLM通过任务专用训练弥补了VLM在3D几何推理上的固有缺陷。

**关键设计决策**包括：
- **紧凑七参数框表示**替代八顶点坐标，降低预测空间维度；
- **GRPO优势归一化** $A_i = \frac{r_i - \operatorname{mean}\{r_1, \dots, r_G\}}{\operatorname{std}\{r_1, \dots, r_G\}}$ 消除奖励尺度影响，稳定训练；
- **指数衰减奖励函数**（如 $R_{\mathrm{stage-2}} = \exp(-\beta \|\hat{\mathbf{c}}_i - \mathbf{c}_i\|_2)$）提供平滑梯度信号；
- **相机反投影** $x = \frac{(u - c_x) \cdot z}{f_x},\ y = \frac{(v - c_y) \cdot z}{f_y}$ 作为2D到3D的显式几何桥梁。

该方法在Mono3DRefer数据集上进行三阶段训练，与零样本VLM基线的对比并不完全公平，但证明了任务专用训练可大幅提升VLM的3D定位能力。代码已开源（EasyR1框架，2025）。

## 背景与动机

### 单目3D视觉定位：从2D图像到3D空间理解的鸿沟

单目3D视觉定位（Monocular 3D Visual Grounding）要求模型根据自然语言描述，从单张RGB图像中预测目标物体的三维边界框。与传统的2D视觉定位相比，该任务增加了一个关键维度——深度（z轴），使模型必须同时理解图像平面上的目标位置及其在三维空间中的姿态、尺寸和朝向。这一能力对于自动驾驶、机器人抓取和增强现实等应用至关重要，因为仅凭2D边界框无法提供物体在真实世界中的完整空间信息。

然而，从单目图像恢复3D几何本身就是一个病态问题：同一2D投影可以对应无穷多种3D配置。当模型还需要将自由形式的文本查询与视觉场景对齐时，问题的复杂度进一步放大。当前该领域的研究主要分为两条路径：一是专用纯视觉模型（如**Mono3DVG**，Zhan et al., AAAI 2024；Mono3DVG-TGE；Mono3D-VLDL），它们在全监督设置下取得了可观性能，但依赖定制化的视觉编码器和检测头，语言理解能力有限；二是大规模视觉语言模型（VLM），它们拥有强大的跨模态对齐能力，但在3D几何推理上存在根本性缺陷。

### VLM的3D定位瓶颈：三项核心缺陷

先导实验（Table 1）揭示了当前VLM在单目3D定位任务中的关键弱点。当直接使用3D IoU作为奖励进行GRPO训练时，模型在横向（x轴）和纵向（y轴）上的中心预测误差远大于深度（z轴）。这一现象指向一个根本问题：**2D视觉定位不够精确**，模型无法在图像平面上准确定位目标，进而通过相机反投影传播为3D误差。

进一步分析表明，即使是最先进的闭源VLM（如GPT-5、Gemini 2.5）和开源VLM（如**Qwen2.5-VL**，Bai et al., arXiv 2025；MiMo-VL），在零样本设置下均表现极差——GPT-5在Mono3DRefer数据集上的Overall mIoU仅为7.53（Table 4）。这暴露了VLM的第二和第三项缺陷：**缺乏对3D几何（深度、相对尺寸、空间关系）的理解**，以及**无法有效利用相机投影/反投影矩阵**将2D观测转换为3D推理。

### 本文动机：分解-渐进式能力注入

上述分析表明，VLM的3D定位失败并非源于单一能力缺失，而是2D定位不准、3D几何无知和相机模型利用失败三者耦合的结果。直接端到端训练（如仅使用3D IoU奖励）会导致模型绕过2D定位的精细学习，在图像平面上产生粗大误差，进而破坏整个3D估计链条。

MonoVLM的核心动机由此产生：**将复杂的单目3D定位任务分解为2D定位和3D几何推理两个子问题，以相机反投影为桥梁，通过分阶段强化学习使VLM逐步掌握从2D视觉线索推断3D属性的能力**。这种分解策略不仅降低了单阶段学习的难度，还通过奖励信号的协同效应——例如第二阶段优化3D中心时2D定位的附带改善（Figure 3）——使模型自发学习2D与3D之间的对偶关系，最终在Mono3DRefer上实现了对专用纯视觉模型的超越（MonoVLM-MiMo Overall Acc@0.25达69.41，Table 2）。

## 核心创新

MonoVLM 的核心创新在于将单目3D视觉定位这一复杂任务，系统性地分解为 VLM 可逐步掌握的三个子问题，并通过分阶段强化学习实现从 2D 到 3D 的能力跃迁。其关键设计变更体现在以下三个维度。

### 1. 三阶段课程式训练策略

传统方法直接以 3D IoU 作为奖励训练 VLM，但先导实验揭示了一个关键瓶颈：仅优化 3D IoU 时，模型在横向（x 轴）和纵向（y 轴）上的误差远大于深度（z 轴）误差（Table 1），表明 2D 定位不准是 3D 误差的主要来源。MonoVLM 据此设计了由粗到细的三阶段 GRPO 训练课程：

- **Stage 1 — 2D 视觉定位**：以 2D IoU 为奖励，训练模型在图像平面上准确定位目标边界框。这一阶段建立了稳固的 2D 感知基础。
- **Stage 2 — 3D 中心预测**：利用相机反投影公式 $x = \frac{(u - c_x) \cdot z}{f_x}, \ y = \frac{(v - c_y) \cdot z}{f_y}$，以预测 3D 中心与真值的指数化负欧氏距离 $R_{\mathrm{stage-2}} = \exp(-\beta \|\hat{\mathbf{c}}_i - \mathbf{c}_i\|_2)$ 作为奖励，训练模型从 2D 坐标和深度推断 3D 空间位置。值得注意的是，此阶段虽未显式优化 2D 定位，但 2D 定位 IoU 出现了附带提升（Figure 3），揭示了模型自主发现了 2D-3D 的对偶关系。
- **Stage 3 — 完整 3D 框估计**：在 3D IoU 主奖励基础上，引入细粒度的分量奖励——中心位置（欧氏距离指数奖励）、尺寸（归一化 L1 指数奖励 $R_{\mathrm{stage-3,size}} = \exp(-\beta_{\mathrm{size}} \frac{\|\hat{\mathbf{d}} - \mathbf{d}\|_1}{\|\mathbf{d}\|_1 + \epsilon})$）和朝向（余弦相似度奖励），联合优化 3D 边界框的全部参数。

这一课程设计的有效性得到了消融实验的强有力验证：MonoVLM-Qwen 的 mIoU 从 Stage 1 的 19.81，经 Stage 2 的 20.89，单调提升至 Stage 3 的 29.13（Table 6）。

### 2. 复合奖励函数的协同设计

Stage 3 的复合奖励函数是 MonoVLM 的另一关键创新。消融实验表明，在 3D IoU 基础上逐步加入位置、尺寸和朝向奖励，mIoU 从 21.31 提升至 29.13（Table 7）。这一设计解决了单一 3D IoU 奖励过于稀疏、无法提供有效梯度信号的问题——各分量奖励分别针对 3D 框的不同几何属性提供密集监督，通过 GRPO 的优势归一化 $A_i = \frac{r_i - \operatorname{mean}\{r_1, \dots, r_G\}}{\operatorname{std}\{r_1, \dots, r_G\}}$ 消除奖励尺度差异，实现协同优化。

### 3. 紧凑的 3D 框参数化

MonoVLM 采用七参数表示 $y_o = (x, y, z, l, w, h, \theta)$ 替代传统的八顶点坐标表示，将 3D 框描述为中心坐标、尺寸（长宽高）和偏航角。这种参数化不仅降低了输出空间的维度，更与分量奖励的设计天然对齐——每个参数对应明确的几何语义，使奖励信号的分配更加精准。

**证据强度评估**：三阶段课程学习的有效性由 Table 6 的单调提升趋势强力支撑；复合奖励的贡献由 Table 7 的消融实验严格验证；2D-3D 协同效应由 Figure 3 的训练曲线直观呈现。整体而言，核心创新主张均有高质量实验证据支持。

## 整体框架

MonoVLM 的整体框架遵循“由粗到精”的三阶段课程学习范式，将单目 3D 视觉定位这一复杂任务分解为三个递进子问题，并通过 GRPO（Group Relative Policy Optimization）强化学习逐步训练 VLM 掌握从 2D 视觉线索推断 3D 几何属性的能力。

### 输入输出定义

框架的输入为一张单目 RGB 图像和一条自然语言查询（如“the red car on the left”），输出为目标的 3D 边界框。为降低学习难度，MonoVLM 采用紧凑的七参数表示 $y_o = (x, y, z, l, w, h, \theta)$，即中心坐标、长宽高尺寸和偏航角，而非直接预测八个顶点坐标。这一设计减少了预测自由度，使模型更易收敛。

### 三阶段训练管线

如图 Figure 2 所示，整个训练管线包含三个递进阶段，每个阶段在前一阶段的基础上引入新的学习目标：

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the MonoVLM framework, which employs a coarse-to-fine, three-stage GRPO training curriculum. Stage 1 establishes robust 2D visual grounding. Stage 2 builds on this by training the model to predict the 3D object center, learning the 2D-to-3D mapping. Finally, Stage 3 optimizes for the complete 3D bounding box by using a composite reward signal that combines the overall 3D IoU with fine-grained, parameter-specific rewards. Please zoom in for better visualization of the GT and prediction*

**阶段一：2D 视觉定位**。本阶段专注于训练模型在图像平面上准确定位目标，使用 2D IoU 作为 GRPO 的奖励信号。模型学习输出目标的 2D 边界框，为后续 3D 推理提供可靠的图像空间锚点。先导实验（Table 1）表明，若跳过此阶段直接以 3D IoU 为奖励进行训练，模型在横向（x）和纵向（y）轴上的误差远大于深度（z）轴，证实了 2D 定位不准是 3D 误差的主要瓶颈。

**阶段二：3D 中心预测**。在稳固的 2D 定位基础上，本阶段通过相机反投影公式 $x = \frac{(u - c_x) \cdot z}{f_x}, \quad y = \frac{(v - c_y) \cdot z}{f_y}$ 建立 2D 坐标与 3D 空间的桥梁。奖励函数设计为 $R_{\mathrm{stage-2}}(q, o_i) = \exp\left(-\beta \|\hat{\mathbf{c}}_i - \mathbf{c}_i\|_2\right)$，即预测 3D 中心与真值间欧氏距离的指数衰减奖励。值得注意的是，尽管本阶段不显式优化 2D IoU，验证曲线（Figure 3）显示 2D 定位精度也获得附带提升，表明模型自发发现了 2D 与 3D 之间的对偶关系。

**阶段三：完整 3D 框估计**。本阶段在 3D IoU 主奖励的基础上，引入针对中心位置、尺寸和朝向的细粒度组件奖励，形成复合奖励信号。其中尺寸奖励采用归一化 L1 距离的指数衰减形式 $R_{\mathrm{stage-3,size}} = \exp\left(-\beta_{\mathrm{size}} \frac{\|\hat{\mathbf{d}} - \mathbf{d}\|_1}{\|\mathbf{d}\|_1 + \epsilon}\right)$，实现尺度不变的尺寸监督；朝向奖励则基于预测偏航角与真值的余弦相似度。消融实验（Table 7）证实，逐步加入这些组件奖励可使 mIoU 从 21.31 单调提升至 29.13。

### GRPO 优化机制

三个阶段统一采用 GRPO 算法进行策略优化。对于每个输入查询 $q$，模型生成 $G$ 个候选响应 $\{o_i\}_{i=1}^{G}$，每个响应获得对应阶段的奖励 $r_i$。奖励经组内归一化转化为优势函数 $A_i = \frac{r_i - \operatorname{mean}\{r_1, \dots, r_G\}}{\operatorname{std}\{r_1, \dots, r_G\}}$，消除奖励尺度对训练的影响。策略 $\pi_\theta$ 通过最大化带裁剪的优势函数与 KL 散度正则项的目标函数进行更新。

### 训练配置

MonoVLM 的训练策略应用于两个 SOTA VLM 骨干：Qwen2.5-VL-7B（Bai et al., arXiv 2025）和 MiMo-VL-7B（MiMo-VL Technical Report, 2025），分别得到 MonoVLM-Qwen 和 MonoVLM-MiMo。所有阶段的 GRPO 训练基于 EasyR1 框架（Zheng et al., 2025）实现，使用 4 张 H100 GPU 及默认超参数。

### 设计动机与协同效应

该三阶段设计的核心洞见在于：单目 3D 定位的困难可归因于 2D 定位不准和 3D 几何理解缺失两个子问题。通过将任务分解并利用相机反投影作为桥梁，模型在每个阶段集中攻克一个子问题，降低了学习难度。更重要的是，阶段间的奖励信号产生协同效应——阶段二的 3D 中心优化反向提升了 2D 定位精度，阶段三的组件奖励则使模型在整体 3D IoU 之外获得更细粒度的几何约束。完整的三阶段训练使 MonoVLM-Qwen 的 mIoU 从 19.81 单调提升至 29.13（Table 6），验证了课程学习的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/001_Figure_1.jpg]]
*Figure 1: We propose MonoVLM, a simple yet effective method to equip Vision-Language Models (VLMs) with robust monocular 3D grounding capabilities. (a) The model takes an image and the textual query to predict the 3D bounding box (GT and prediction). (b) Even the latest large-scale VLMs struggle to understand 3D structure from 2D images. Our resulting model not only achieves significantly better results than these VLMs but also surpasses specialized vision-only models designed for this task*

## 核心模块与公式推导

### 问题形式化与3D框表示

MonoVLM将单目3D视觉定位任务建模为：给定输入图像和文本查询 $q$，模型直接输出目标物体的三维边界框。为降低VLM的预测难度，MonoVLM采用**紧凑七参数表示** $y_o = (x, y, z, l, w, h, \theta)$，即由中心坐标 $(x, y, z)$、尺寸 $(l, w, h)$ 和偏航角 $\theta$ 组成，替代了传统的八顶点坐标表示 $y_o = \{\mathbf{v}_1, \ldots, \mathbf{v}_8\}$（见公式(1)和(2)）。这种紧凑表示大幅减少了输出token数量，使VLM的序列生成更加可控。

### GRPO优化框架

MonoVLM采用**Group Relative Policy Optimization (GRPO)** 作为核心训练算法。对于每个输入查询 $q$，模型从旧策略 $\pi_{\theta_{\text{old}}}$ 中采样一组 $G$ 个候选响应 $\{o_i\}_{i=1}^{G}$，每个响应获得一个标量奖励 $r_i$。GRPO的关键操作是将奖励归一化为相对优势：

$$A_i = \frac{r_i - \operatorname{mean}\{r_1, \dots, r_G\}}{\operatorname{std}\{r_1, \dots, r_G\}}$$

这一归一化（公式(3)）消除了奖励绝对尺度的波动，使策略更新仅依赖于候选响应在组内的相对排序。随后，GRPO通过带裁剪的优势函数和KL散度正则项更新策略 $\pi_\theta$（公式(4)），确保训练稳定。

### 三阶段课程学习与奖励设计

MonoVLM的核心创新在于将复杂的单目3D定位任务分解为三个递进阶段，每个阶段设计专门的奖励函数。

**先导研究揭示瓶颈**：若直接使用3D IoU作为奖励 $R_{\text{acc}}(q, o_i) = 3\text{DIoU}(\hat{y}_i, y_i)$（公式(5)）训练模型，奖励信号过于稀疏，导致模型在图像平面上的2D定位极不准确。定量证据（Table 1）显示，直接训练的模型在横向（x）和纵向（y）轴上的3D中心预测误差（Qwen: x=1.06m, y=1.90m）远大于深度（z）轴（z=0.20m），表明**2D定位不准是3D误差的主要来源**。

**Stage 1：2D视觉定位**。本阶段仅使用2D IoU作为奖励 $R_{\text{stage-1}}(q, o_i) = 2\text{DIoU}(\hat{b}_i, b_i)$（公式(7)），训练模型在图像平面上准确预测目标的2D边界框，为后续3D推理奠定基础。

**Stage 2：3D中心预测**。本阶段利用相机反投影公式将2D坐标与深度关联：

$$x = \frac{(u - c_x) \cdot z}{f_x}, \quad y = \frac{(v - c_y) \cdot z}{f_y}$$

其中 $(u, v)$ 为2D中心坐标，$(c_x, c_y)$ 为主点，$(f_x, f_y)$ 为焦距，$z$ 为深度（公式(6)）。奖励函数设计为预测3D中心与真值之间的指数化负欧氏距离：

$$R_{\text{stage-2}}(q, o_i) = \exp\left(-\beta \|\hat{\mathbf{c}}_i - \mathbf{c}_i\|_2\right)$$

（公式(8)），鼓励模型学习从2D视觉线索推断3D空间位置的能力。

**Stage 3：完整3D框估计**。本阶段在3D IoU主奖励的基础上，补充三个组件级奖励：
- **位置奖励**：$R_{\text{stage-3,loc}} = \exp\left(-\beta_{\text{loc}} \|\hat{\mathbf{c}} - \mathbf{c}\|_2\right)$（公式(9)）
- **尺寸奖励**：$R_{\text{stage-3,size}} = \exp\left(-\beta_{\text{size}} \frac{\|\hat{\mathbf{d}} - \mathbf{d}\|_1}{\|\mathbf{d}\|_1 + \epsilon}\right)$（公式(10)），通过归一化L1距离实现尺度不变的尺寸监督
- **朝向奖励**：基于预测偏航角与真值的余弦相似度（公式(11)）

复合奖励的协同效应在消融实验中得到验证（Table 7）：逐步加入位置、尺寸和朝向奖励使mIoU从21.31单调提升至29.13。

### 2D-3D协同效应

一个值得注意的发现是Stage 2训练中的**2D-3D对偶学习**现象（Figure 3）：虽然本阶段仅优化3D中心预测奖励，但2D定位IoU在训练过程中也附带提升。这表明模型自主发现了2D定位与3D推理之间的内在联系，验证了分阶段课程设计的合理性。

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/004_Figure_3.jpg]]
*Figure 3: Evolution of rewards during Stage 2 training. The model is explicitly optimized using a reward based on the 3D center prediction distance. While the 2D grounding IoU is not part of the training objective in this stage, it shows collateral improvement. This demonstrates a strong synergy between the 2D and 3D localization tasks, suggesting that the model discovers the duality between 2D and 3D*

## 实验与分析

### 先导研究：3D IoU 奖励的失效模式

为验证直接使用 3D IoU 作为强化学习奖励信号的可行性，作者进行了先导实验。结果如 **Table 1** 所示，该实验揭示了仅以 3D IoU 为奖励时的核心失效模式：模型在横向（x 轴）和纵向（y 轴）上产生显著的中心预测误差，而深度（z 轴）误差相对较小。以 Qwen 基线为例，x 轴误差为 1.06 m，y 轴误差高达 1.90 m，而 z 轴误差仅为 0.20 m；MiMo 基线的趋势一致（x: 2.86 m, y: 3.06 m, z: 0.27 m）。

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/003_Table_1.jpg]]
*Table 1: Per-axis 3D center prediction error of the models trained in our pilot study. Errors are reported separately for the lateral (x), vertical (y), and depth (z) coordinate axes*

这一现象的根本原因在于：3D IoU 奖励信号过于稀疏，无法为模型提供足够的梯度信息来精确定位目标在 2D 图像平面上的位置。由于 3D 框的横向和纵向坐标是通过相机反投影从 2D 坐标和深度恢复的（见公式 $x = \frac{(u - c_x) \cdot z}{f_x}, \ y = \frac{(v - c_y) \cdot z}{f_y}$），2D 定位的微小偏差在反投影后会被深度值放大，导致 x、y 轴的 3D 误差远超 z 轴。这一发现直接驱动了 MonoVLM 三阶段课程学习的设计：必须首先解决 2D 定位问题，才能有效学习 3D 几何推理。

### 主实验结果

#### 与 VLM 基线的对比

**Table 2** 展示了 MonoVLM 与开源/闭源 VLM 及专用纯视觉模型在 Mono3DRefer 数据集上的准确率对比。所有 VLM 基线均未在 Mono3DRefer 训练集上微调，仅进行零样本评估，因此该对比揭示了任务专用训练的巨大增益。

在 Overall Acc@0.25 指标上，MonoVLM-MiMo 达到 69.41，远超零样本 VLM 基线——GPT-5 仅 30.02，Gemini 2.5 为 28.82，Qwen2.5-VL 为 17.71。在更严格的 Acc@0.5 下，MonoVLM-MiMo 以 42.96 同样大幅领先。值得注意的是，MonoVLM-MiMo 在 Multiple 场景的 Acc@0.25 达到 71.23，超越了专用全监督纯视觉模型 Mono3DVG-TGE（69.83），这是 VLM 方法首次在该子任务上达到与专用模型相当甚至更优的性能。

#### IoU 维度分析

**Table 4** 和 **Table 5** 分别从目标出现次数和距离/难度两个维度进行了更细粒度的 IoU 对比。MonoVLM-MiMo 在所有类别上均显著优于零样本 VLM 基线。以 Overall mIoU 为例，MonoVLM-MiMo 达到 38.11，是 GPT-5（7.53）的 5 倍以上（**Table 4**）。在 Far/Hard 类别上（**Table 5**），MonoVLM-MiMo 的 mIoU 为 20.66，而 GPT-5 仅为 2.65，差距进一步拉大，表明课程学习策略使模型在困难远距离场景中获得了显著的鲁棒性提升。**Figure 4** 的定性对比也佐证了这一点：GPT-5 在远距离小目标上往往产生严重偏离的预测框，而 MonoVLM-MiMo 的预测与真值（绿色框）高度吻合。

#### 分层难度分析

**Table 3** 按 Near/Easy、Medium/Moderate、Far/Hard 三个难度层级进行了准确率分解。MonoVLM-MiMo 在 Near/Easy 的 Acc@0.25 达到 78.15/74.14，在 Far/Hard 下仍有 41.94/38.71，而 GPT-5 在 Far/Hard 下仅为 4.84/1.61。这验证了三阶段训练策略在不同难度层级上的泛化能力。

### 消融实验

#### 课程学习有效性

**Table 6** 展示了 MonoVLM-Qwen 在三阶段训练过程中的 mIoU 单调递增轨迹：Stage-1（仅 2D 定位）为 19.81 → Stage-2（加入 3D 中心预测）为 20.89 → Stage-3（完整 3D 框估计）为 29.13。这一单调提升验证了从粗到细的课程设计有效降低了学习难度，每一阶段都为下一阶段提供了更好的初始化。

#### Stage 3 奖励函数组件消融

**Table 7** 对 Stage 3 的复合奖励函数进行了组件级消融。基线（仅使用 3D IoU）的 mIoU 为 21.31。逐步加入位置奖励（+loc）提升至 25.01，加入尺寸奖励（+size）进一步提升至 25.97，加入朝向奖励（+yaw）后达到 26.95。完整组合（3D IoU + loc + size + yaw）最终达到 29.13，相比纯 3D IoU 基线提升 7.82 个点。这表明细粒度的参数级监督信号与全局 3D IoU 奖励之间存在协同效应：位置奖励强化了 Stage-2 已习得的 2D-3D 对偶关系，尺寸和朝向奖励则提供了 3D IoU 无法直接传达的几何约束。

#### 最小设计变体对比

**Table 8** 对比了 MonoVLM 的最小设计变体。直接使用 SFT（监督微调）的 mIoU 为 17.34，仅使用 Stage-3 复合奖励（跳过前两阶段）为 19.51，而完整的三阶段方案达到 29.13。这证明：① 强化学习（GRPO）比 SFT 更适合该任务；② 三阶段课程学习的收益远大于单阶段复合奖励，因为前两阶段提供了必要的 2D 定位和 3D 中心预测基础。

### 2D-3D 协同效应的实证证据

**Figure 3** 展示了 Stage-2 训练过程中的奖励曲线。尽管该阶段仅使用 3D 中心预测距离作为优化目标（公式 $R_{\mathrm{stage-2}} = \exp(-\beta \|\hat{\mathbf{c}}_i - \mathbf{c}_i\|_2)$），但 2D 定位 IoU 作为未参与优化的伴随指标也呈现持续上升趋势。这一现象揭示了模型在训练中自发发现了 2D 定位与 3D 中心预测之间的对偶关系——精确的 3D 中心预测隐式要求精确的 2D 定位，反之亦然。这一协同效应是 MonoVLM 课程设计成功的内在机制之一。

### 公平性说明

需要指出的是，MonoVLM 与零样本 VLM 基线的对比并不完全公平：MonoVLM 利用了 Mono3DRefer 训练集进行三阶段 GRPO 训练，而 GPT-5、Gemini 2.5、Qwen2.5-VL 等基线仅进行零样本评估。然而，这种对比恰恰证明了任务专用训练可以赋予 VLM 原本严重缺失的 3D 几何理解能力——零样本 VLM 的 3D 定位性能极差（GPT-5 的 Overall mIoU 仅 7.53），而经过三阶段训练的 MonoVLM 不仅大幅超越零样本 VLM，甚至能在部分指标上比肩或超越专用全监督纯视觉模型。

### 补充图表

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/005_Table_2.jpg]]
*Table 2: Comparisons with open-source and closed-source VLMs and pure-vision baselines. All VLMs are evaluated without any training on the training set of the Mono3DRefer dataset. The performance comparisons are conducted under ”Unique”, ”Multiple”, ”Overall”, these three categories of the dataset. Deeper colors indicate better performance*

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/008_Table_4.jpg]]
*Table 4: Comparison of grounding IoU between our MonoVLM models and baseline VLMs on the object occurrence categories. Bolded and underlined results indicate the best and second best*

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/009_Table_5.jpg]]
*Table 5: Comparison of IoU between our MonoVLM models and baseline VLMs on the object distance and difficulty categories. Bolded and underlined results indicate the best and second best*

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/007_Table_3.jpg]]
*Table 3: Further comparisons with VLMs and pure-vision baselines. All VLMs are evaluated without any training on the training set of the Mono3DRefer dataset. The performance comparisons are conducted under ”Near/Easy”, ”Medium/Moderate”, and ”Far/Hard”, with these three pairs of scenarios in the dataset. Deeper colors indicate better performance*

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/010_Table_6.jpg]]
*Table 6: mIoU of MonoVLM-Qwen after three stages*

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/011_Table_7.jpg]]
*Table 7: Ablation of reward functions used in Stage 3 training*

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/012_Table_8.jpg]]
*Table 8: Minimal design-variant comparison*

![[assets/figures/papers/paper_list_l2405_https_openaccess_thecvf_com_content_CVPR2026_html_Qu_MonoVLM_Monocular_3/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison of predictions on far-away challenging objects between our method, MonoVLM-MiMo, and the topperforming baseline, GPT-5. Ground truth bounding boxes are shown in green. Red boxes denote predictions from GPT-5 and our MonoVLM-MiMo. Please zoom in for better visualization of the small objects*

## 方法谱系与知识库定位

### 问题定位：VLM在单目3D定位中的三重缺陷

MonoVLM的核心动机源于一个关键的诊断性发现：当前最先进的视觉语言模型（VLM）在单目3D视觉定位任务上存在三重结构性缺陷。先导实验（Table 1）揭示，当直接以3D IoU作为奖励进行GRPO训练时，模型在横向（x轴）和纵向（y轴）上的3D中心预测误差远大于深度（z轴）误差——以Qwen2.5-VL为例，x轴误差达1.06m，y轴误差达1.90m，而z轴误差仅为0.20m。这一现象表明，**2D视觉定位不够精确**是3D误差的主要来源：模型无法在图像平面上准确定位目标，导致基于相机反投影恢复的3D坐标在x和y方向上产生显著偏差。此外，VLM还缺乏对3D几何（深度、相对尺寸、空间关系）的内在理解，且无法有效利用相机投影/反投影矩阵。这三重缺陷共同导致即使是最先进的VLM（如GPT-5），其3D定位性能也极差——在Mono3DRefer数据集上的总体mIoU仅为7.53。

### 与基线方法的关系

#### 专用纯视觉基线

Mono3DRefer数据集上存在一系列专用纯视觉方法，它们采用全监督训练范式，代表了该任务的性能上界参考。**Mono3DVG**（Zhan et al., AAAI 2024）是该领域的代表性工作，其后续变体**Mono3DVG-TGE**和**Mono3D-VLDL**进一步提升了性能。这些方法通常依赖于专门设计的视觉编码器和3D推理模块，但在语言理解能力上存在天然局限——它们需要额外的文本编码器来处理自然语言查询，且难以泛化到开放词汇场景。

MonoVLM的定位并非取代这些专用模型，而是**探索VLM在该任务上的潜力边界**。实验结果表明，经过三阶段训练的MonoVLM-MiMo在Multiple场景下的Acc@0.25达到71.23，超越了Mono3DVG-TGE的69.83（Table 2），这证明了VLM在获得适当的3D训练后，可以达到甚至超越专用纯视觉模型的性能。然而，需要注意的是，这一对比并不完全公平：专用模型在Mono3DRefer训练集上进行全监督训练，而MonoVLM同样利用了该数据集的训练数据进行三阶段GRPO训练。

#### VLM零样本基线

论文选取了当前最具代表性的开源和闭源VLM作为零样本基线，包括：
- **GPT-5**（闭源）：性能最强的闭源VLM基线，但3D定位mIoU仅为7.53
- **Gemini 2.5**（闭源）：另一闭源VLM，同样表现不佳
- **Qwen2.5-VL**（Bai et al., arXiv 2025）：开源VLM基线，作为MonoVLM-Qwen的骨干模型
- **MiMo-VL**（MiMo-VL Technical Report, 2025）：开源VLM基线，作为MonoVLM-MiMo的骨干模型

所有VLM基线均未在Mono3DRefer训练集上进行微调，仅进行零样本评估。这一设置凸显了当前VLM在3D理解上的根本性不足，也构成了MonoVLM的核心贡献语境：**通过任务专用训练，VLM的3D定位能力可以获得数量级的提升**——MonoVLM-MiMo的mIoU（38.11）是GPT-5（7.53）的5倍以上。

### 方法谱系中的技术定位

#### GRPO训练范式的继承与适配

MonoVLM的训练框架建立在**GRPO**（Group Relative Policy Optimization）之上，这是一种用于大语言模型强化学习的策略优化方法。GRPO的核心机制是通过组内奖励归一化计算相对优势函数：

$$A_i = \frac{r_i - \operatorname{mean}\{r_1, \dots, r_G\}}{\operatorname{std}\{r_1, \dots, r_G\}}$$

这一归一化消除了奖励绝对尺度的影哿，使训练更加稳定。MonoVLM的创新不在于修改GRPO本身，而在于**为3D定位任务设计了分阶段的奖励函数课程**，使GRPO能够逐步引导VLM掌握从2D视觉线索推断3D属性的能力。训练实现基于**EasyR1**框架（Zheng et al., 2025），使用4×H100 GPU和默认超参数。

#### 3D框表示的简化

与部分方法使用八顶点坐标表示$y_o = \{\mathbf{v}_1, \ldots, \mathbf{v}_8\}$不同，MonoVLM采用紧凑的七参数表示：

$$y_o = (x, y, z, l, w, h, \theta)$$

这一选择降低了预测空间的复杂度，使VLM的语言输出头更容易学习结构化的3D参数。七参数表示直接编码了3D边界框的中心坐标、尺寸（长宽高）和偏航角，与相机反投影公式形成自然的数学衔接：

$$x = \frac{(u - c_x) \cdot z}{f_x}, \quad y = \frac{(v - c_y) \cdot z}{f_y}$$

#### 课程学习与奖励塑形

MonoVLM的三阶段课程设计体现了**从易到难、从2D到3D**的渐进式学习理念：

1. **Stage 1（2D定位）**：使用2D IoU奖励建立稳健的图像平面定位能力，解决VLM在2D视觉定位上的根本性不足。
2. **Stage 2（3D中心预测）**：使用3D中心距离的指数奖励$R_{\mathrm{stage-2}}(q, o_i) = \exp(-\beta \|\hat{\mathbf{c}}_i - \mathbf{c}_i\|_2)$，训练模型学习2D-3D反投影映射。关键发现是，这一阶段的训练不仅提高了3D中心精度，还**附带改善了2D定位**（Figure 3），表明模型自发发现了2D与3D之间的对偶关系。
3. **Stage 3（完整3D框）**：在3D IoU主奖励的基础上，补充位置、尺寸和朝向的组件级奖励。尺寸奖励采用归一化L1距离的指数衰减形式$R_{\mathrm{stage-3,size}} = \exp(-\beta_{\mathrm{size}} \frac{\|\hat{\mathbf{d}} - \mathbf{d}\|_1}{\|\mathbf{d}\|_1 + \epsilon})$，实现尺度不变的监督。

这种课程设计的有效性通过消融实验得到验证：三阶段训练使MonoVLM-Qwen的mIoU从19.81单调提升至29.13（Table 6），且完整的三阶段方案优于直接SFT和仅使用Stage-3奖励的方案（Table 8）。

### 适用边界与局限

#### 适用条件

MonoVLM的训练范式依赖于以下条件：
- **已知相机内参**：2D-3D反投影需要焦距$(f_x, f_y)$和主点$(c_x, c_y)$信息，这要求输入图像附带相机标定参数。
- **有监督训练数据**：三阶段GRPO训练需要带有3D边界框标注的数据集（如Mono3DRefer），无法以零样本方式工作。
- **骨干VLM的2D视觉能力**：方法假设骨干VLM具备基本的2D视觉理解能力，Stage 1的训练旨在强化而非从零构建这一能力。

#### 已知局限

论文未明确列出专门的小节讨论局限性，但从实验设计和方法描述中可以推断以下潜在局限：

1. **数据依赖**：MonoVLM的性能提升依赖于Mono3DRefer训练集的监督信号，与零样本VLM基线的对比并不完全公平。在分布外场景（如不同相机参数、不同场景类型）下的泛化能力未经系统验证。
2. **骨干模型敏感性**：方法在Qwen2.5-VL-7B和MiMo-VL-7B上进行了验证，但不同VLM架构对三阶段训练的响应可能存在差异。论文未探讨更大规模VLM（如13B、70B参数级别）或不同视觉编码器架构下的表现。
3. **单目标假设**：Mono3DRefer数据集聚焦于单目标3D定位，MonoVLM在多目标同时定位场景下的扩展性未经验证。
4. **朝向估计的挑战**：偏航角$\theta$的预测是3D定位中的难点，Stage 3的朝向奖励$R_{\mathrm{stage-3,yaw}}$依赖于余弦相似度，但对称物体的朝向歧义性问题未在论文中讨论。
5. **计算开销**：三阶段训练需要依次进行三次GRPO训练，相比端到端方法增加了训练时间和资源消耗。论文未报告各阶段的训练时长对比。

### 开放问题

1. **跨数据集泛化**：MonoVLM在Mono3DRefer上的成功是否能迁移到其他3D视觉定位数据集（如SUN-Spot、ScanRefer的3D变体）？不同数据集的相机参数分布和场景特性可能影响反投影的准确性。
2. **多模态奖励的扩展**：当前奖励函数完全基于几何精度，是否可以引入语义一致性奖励（如文本描述与3D框属性的对齐程度）来进一步提升定位的语义合理性？
3. **零样本3D能力的激发**：MonoVLM证明了通过训练可以赋予VLM 3D定位能力，但是否存在更高效的提示工程或上下文学习方法，能够在无需微调的情况下激发VLM的潜在3D理解能力？
4. **与深度估计模型的协同**：当前方法通过反投影公式从2D坐标和深度恢复3D位置，但深度值本身由模型预测。是否可以通过与单目深度估计模型（如Depth Anything）的显式协同来提供更准确的深度先验？
5. **动态场景与时序一致性**：MonoVLM处理的是静态单帧图像，在视频或自动驾驶等动态场景中，如何利用时序信息约束3D定位的一致性是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/MonoVLM_Monocular_3D_Visual_Grounding_with_Vision_Language_Models.pdf]]