---
title: "AdaptVision: Efficient Vision-Language Models via Adaptive Visual Acquisition"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AdaptVision_Efficient_Vision_Language_Models_via_Adaptive_Visual_Acquisition.pdf
project_link: null
code_link: "https://github.com/adaptvision/adaptvision"
aliases:
- AdaptVision
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 让VLM自主决定在低分辨率图像基础上是否通过工具调用获取额外高分辨率视觉信息。
primary_logic: 模拟人类主动视觉的从粗到细处理机制，利用强化学习和解耦回合策略优化（DTPO）训练模型在效率与精度之间取得动态平衡。
claims:
- AdaptVision在多个VQA基准测试上以平均33%的视觉token实现了相对于原始模型97.9%的性能，显著优于现有高效VLM方法。
- 与降采样模型相比，AdaptVision仅增加7%的视觉token（25%→33%），平均准确率从92.1%提升至97.9%。
- DTPO训练过程稳定且高效，而标准GRPO因信用分配模糊和优化不平衡导致策略崩溃至过度工具调用。
- 平衡奖励的设计对于防止模型过度使用工具调用至关重要，工具奖励则是探索正确工具使用所必需的。
---

# AdaptVision: Efficient Vision-Language Models via Adaptive Visual Acquisition

> [!tip] 核心洞察
> 模拟人类主动视觉的从粗到细处理机制，利用强化学习和解耦回合策略优化（DTPO）训练模型在效率与精度之间取得动态平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | AdaptVision：通过自适应视觉获取实现高效视觉语言模型 |
| 英文题名 | AdaptVision: Efficient Vision-Language Models via Adaptive Visual Acquisition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.03794) · [Code](https://github.com/adaptvision/adaptvision) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AdaptVision |
| Dataset | Overall, ChartQA test, MMVet test, RealWorldQA test |

> [!tip] 效果简介
> - Overall (9 benchmarks) 上，平均相对性能（vs. Vanilla） 97.9% vs 100% (Vanilla) (-2.1 pp (视觉token减少67%))。
> - ChartQA test 上，准确率 75.92 (95.1%) vs 78.8% (Down-Sample) (+16.3% absolute vs. Down-Sample)。
> - MMVet test 上，准确率 64.8 (105.2%) vs 88.5% (Down-Sample) (+18.9% absolute vs. Down-Sample)。

## 概要

### 问题瓶颈

视觉语言模型（VLM）在推理时需要处理大量视觉token，造成显著的计算开销。现有高效VLM方法主要采用**被动策略**来减少视觉token——如固定降采样、基于注意力或跨模态相关性的静态剪枝——这些方法对所有样本一视同仁，无法根据任务的实际复杂度动态调整视觉信息量。这种“一刀切”的做法导致两类失败：简单任务上浪费计算资源，复杂任务上因信息不足而精度下降。核心瓶颈在于**缺乏自适应机制**，使模型能够像人类视觉系统一样，根据需求主动决定“看多少”和“看哪里”。

### 核心方法

**AdaptVision** 提出了一种从粗到细（coarse-to-fine）的自适应视觉获取框架，让VLM自主决定何时获取额外的高分辨率视觉信息。其核心设计包含三个层面：

- **视觉获取机制**：模型首先处理1/4低分辨率图像（保留约25%视觉token），然后自主决定是直接回答，还是通过**边界框工具调用**从高分辨率图像中裁剪关键区域进行精细分析。这种设计模拟了人类主动视觉中“先扫视、再凝视”的机制。

- **训练算法——解耦回合策略优化（DTPO）**：标准GRPO对所有token统一归一化，导致工具token因数量少而被欠优化，最终策略崩溃至过度工具调用。DTPO将策略损失按**工具token和答案token分别归一化**，并为两者计算**不同的优势估计**，实现精确的信用分配和平衡优化。

- **奖励函数设计**：总奖励由结果奖励（答案正确性+格式+平衡惩罚）和工具奖励（裁剪正确性+面积惩罚）组成。其中**平衡奖励**防止模型过度依赖工具或依赖低分辨率猜测，**面积惩罚**激励模型选择最小的必要裁剪区域。

### 核心结论

在9个VQA基准测试上，AdaptVision以**平均33%的视觉token**实现了相对于原始Qwen2.5-VL-7B-Instruct模型**97.9%的平均性能**（Table 1）。与直接降采样至25% token的模型相比，仅增加7%的token（25%→33%），平均准确率从92.1%提升至97.9%。在ChartQA和MMVet等需要精细视觉推理的基准上，AdaptVision相较降采样模型分别提升16.3和18.9个百分点。推理时间方面，AdaptVision相较原始模型实现**1.67倍加速**（Figure 4）。消融实验证实，DTPO训练稳定收敛，而标准GRPO因信用分配模糊导致策略崩溃；平衡奖励和工具奖励均为训练成功的关键组件（Figure 5）。

### 方法谱系与知识库定位

AdaptVision属于**动态视觉token压缩**方法，与现有的静态压缩方法（如**FastV**、**SparseVLM**、**VisionZip**）形成对比。这些静态方法在固定保留率（通常50%）下运行，无法根据样本难度调整。在动态方法中，**VisionThink**同样使用强化学习选择低分辨率或原始图像，但其发布的模型实际使用了99%视觉token，且训练稳定性不足。AdaptVision通过工具调用机制实现了更细粒度的视觉信息获取（可裁剪任意区域），配合DTPO算法解决了动态策略优化的稳定性问题。该方法**架构无关**，理论上可迁移至其他VLM架构（如InternVL、LLaVA系列），但目前仅在Qwen2.5-VL-7B-Instruct上充分验证。

### 局限与开放问题

当前框架限制为最多两轮交互，可能不足以处理需要多阶段精细视觉推理的任务。训练依赖GPT-4o作为外部奖励模型，引入评估偏差和计算成本。工具种类单一（仅边界框裁剪），未扩展到去模糊、放大等其他操作。此外，方法在其他VLM架构上的迁移能力、多轮工具调用的扩展、以及完全开源奖励模型的替代方案仍有待探索。

视觉语言模型（VLM）在图像问答、文档理解等任务上取得了显著进展，但其性能提升往往伴随着视觉token数量的急剧膨胀。以Qwen2.5-VL-7B-Instruct为代表的主流VLM通常将输入图像编码为大量视觉token，在推理时造成高昂的计算开销和延迟。如何在保持模型精度的前提下减少视觉token消耗，已成为VLM走向实际部署的核心瓶颈。

现有高效VLM方法主要沿两条路径展开：**静态压缩**与**被动剪枝**。前者在编码阶段对图像进行固定降采样（如直接使用1/4分辨率输入），后者则基于注意力分数或跨模态相关性对视觉token进行固定比例的剪枝（如**FastV**保留50% token，**SparseVLM**保留50% token，**VisionZip**保留50% token）。这些方法的共同缺陷在于：它们对每个样本施加统一的压缩策略，完全忽略了任务复杂度的差异。对于需要细粒度视觉感知的困难问题（如ChartQA中的图表读数），过度压缩会导致关键信息丢失；而对于简单的通用场景问题，全分辨率处理又造成资源浪费。这种“一刀切”的被动策略使模型在效率与精度之间陷入两难。

**VisionThink**首次尝试引入动态视觉token选择机制，允许模型在低分辨率与原始分辨率图像之间做出选择。然而，其策略优化仍依赖标准GRPO，面临信用分配模糊和优化不平衡的问题，导致训练不稳定，最终发布的模型实际使用了99%的视觉token，未能真正实现高效的动态获取。

上述困境的根源在于：现有方法缺乏对人类视觉注意机制的模拟。人类在观察图像时，天然采用“从粗到细”（coarse-to-fine）的主动视觉策略——先快速扫描全局获取概览，再针对问题相关区域进行精细分析。这一机制启发我们思考：能否让VLM自主决定何时需要“看得更仔细”，并通过工具调用的方式按需获取高分辨率视觉信息？

**AdaptVision**正是基于这一洞察而提出。其核心思想是：让模型以低分辨率图像（25%视觉token）初始化视觉感知，然后根据任务需求自主决策——是直接基于低分辨率信息回答问题，还是调用边界框工具裁剪高分辨率区域进行深入分析。这一范式将视觉token的获取从“被动接受”转变为“主动获取”，为VLM的效率-精度权衡提供了新的解决路径。

## 核心方法与创新机理

AdaptVision的核心创新在于将**动态视觉获取**建模为VLM自主决策的**工具调用问题**，并通过专门设计的强化学习算法实现高效训练。与现有方法在固定token预算下被动压缩或静态剪枝不同，AdaptVision赋予模型主动判断何时需要额外视觉信息的能力，从根本上改变了视觉token的分配范式。

### 创新一：从被动压缩到主动视觉获取

现有高效VLM方法（如FastV、SparseVLM、VisionZip）采用**静态压缩策略**：无论任务复杂度如何，始终保留固定比例（如50%）的视觉token。这种“一刀切”的方式导致简单任务浪费计算资源，复杂任务则因信息不足而精度下降。AdaptVision的关键洞察来自人类视觉的**从粗到细（coarse-to-fine）处理机制**——人类首先快速扫描全局场景，仅在需要时才将注意力聚焦于关键区域进行精细分析。

AdaptVision将这一机制实现为**两阶段视觉获取框架**（Figure 2）：
1. **低分辨率初始化**：输入图像首先降采样至1/4分辨率，生成仅占原始25%的压缩视觉token，大幅降低基础计算成本。
2. **按需工具调用**：模型基于低分辨率信息自主决定是直接回答，还是调用边界框工具从高分辨率图像中裁剪关键区域，获取额外视觉token进行深入分析。

这一设计将视觉token数量从固定预算转变为**任务自适应的动态变量**，简单任务仅需25% token即可正确回答，复杂任务则通过工具调用获取必要的高分辨率细节。

### 创新二：解耦回合策略优化（DTPO）

训练模型学会“何时调用工具”是一个非平凡的强化学习问题。标准GRPO（Group Relative Policy Optimization）将工具调用和答案生成的所有token统一归一化优化，导致两个关键问题：

- **信用分配模糊（Credit Assignment Ambiguity）**：工具token和答案token共享同一个序列级奖励，模型无法区分工具调用质量与答案质量的贡献。
- **优化不平衡（Optimization Imbalance）**：工具token数量远少于答案token，在统一归一化下工具token的优化信号被严重稀释，导致策略崩溃至过度工具调用或完全放弃工具。

DTPO通过两个核心机制解决上述问题（Figure 3）：

1. **按回合解耦损失归一化**：将策略损失分解为工具token和答案token两部分，分别按各自的token数量进行归一化，确保工具token获得充分的优化信号。

2. **差异化优势估计**：为工具调用和答案生成分别计算优势函数——工具优势基于裁剪正确性和面积惩罚，结果优势基于答案正确性——并通过超参数λ加权组合，实现精确的信用分配。

### 创新三：多维度平衡奖励设计

奖励函数设计是防止策略崩溃的关键。AdaptVision的奖励由三部分组成：

- **结果奖励**：答案正确性 + 格式合规性
- **平衡奖励**：防止模型过度依赖工具（工具调用时施加轻微惩罚）或依赖低分辨率猜测（直接回答正确但比例过低时惩罚）
- **工具奖励**：裁剪正确性 − α × 区域面积惩罚，激励模型选择最小必要区域

消融实验（Figure 5a）表明，移除平衡奖励导致训练崩溃至过度工具调用；移除工具奖励则使模型完全放弃工具调用。三者缺一不可。

### 与现有方法的根本差异

| 维度 | 静态压缩方法 | VisionThink | AdaptVision |
|------|-------------|-------------|-------------|
| **token分配策略** | 固定比例压缩 | 动态选择整图分辨率 | 低分辨率初始化 + 按需裁剪 |
| **决策粒度** | 无决策 | 全图级别（低/高分辨率二选一） | 区域级别（裁剪特定边界框） |
| **训练算法** | 有监督微调 | 标准GRPO | DTPO（解耦优化） |
| **平均token使用** | 50%（固定） | 52% | 33%（自适应） |
| **相对性能** | 约92-96% | 约95% | 97.9% |

AdaptVision的核心优势在于：以更少的平均视觉token（33% vs. 50%+）实现了更接近原始模型（97.9%）的性能，同时保留了根据任务难度灵活分配视觉资源的自主性。

AdaptVision 的整体设计遵循**从粗到细（coarse-to-fine）**的主动视觉获取范式，其核心思想是让 VLM 自主决定何时需要获取额外的高分辨率视觉信息，而非被动接受固定数量的视觉 token。整个 pipeline 由四个关键模块串联构成，形成“低分辨率感知—策略决策—按需工具调用—最终答案生成”的闭环。

### 低分辨率图像处理

输入图像首先被降采样至原始分辨率的 1/4，经视觉编码器处理后仅保留约 **25%** 的视觉 token。这一压缩步骤大幅削减了后续推理的计算开销，同时保留了足够的全局上下文信息，使模型能够对图像内容形成初步理解。该模块是效率提升的基础，也是后续决策的感知前提。

### 策略决策

基于低分辨率视觉 token 和用户问题，VLM 自主做出二选一的策略选择：**直接回答**或**调用边界框工具**。这一决策过程完全由模型自身的生成策略 $\pi_{\theta}(o \vert x)$ 控制（见 Eq. 5），无需外部规则或硬阈值。若模型判断低分辨率信息已足以回答问题，则跳过工具调用，直接进入答案生成阶段，从而最小化视觉 token 消耗。

### 工具调用执行

当模型选择工具调用时，它会输出一个边界框坐标，从原始高分辨率图像中裁剪出指定区域。该裁剪区域被单独编码为额外的视觉 token，与低分辨率 token 拼接后送入后续处理。这一机制的关键在于：模型仅在必要时才获取细节信息，且裁剪区域的面积受到奖励函数中的面积惩罚项约束（Eq. 9–10），从而激励模型选择最小的有效区域，在精度与效率之间取得平衡。

### 最终答案生成

无论模型选择了直接回答还是工具调用路径，最终阶段都会整合所有可用的视觉 token（低分辨率 + 可选的裁剪区域）与文本信息，生成最终答案。这一统一生成阶段确保了两种路径下答案格式和推理逻辑的一致性。

### 模块间的因果链条

整个 pipeline 的因果链条可概括为：**压缩感知 → 自适应决策 → 按需获取细节 → 整合生成**。其中，策略决策模块是系统的核心瓶颈——它决定了效率与精度的动态平衡点。DTPO 训练算法（见 Section 4.3）通过解耦工具 token 和答案 token 的优化目标，确保模型学会在“直接回答”和“工具调用”之间做出合理的自适应选择，而非退化到过度依赖工具或完全放弃工具的极端策略。

### 补充图表

![[assets/figures/papers/paper_list_l2759_https_arxiv_org_abs_2512_03794/figures/002_Figure_2.jpg]]
*Figure 2: FrameWork of AdaptVision. AdaptVision first processes a 1/4-resolution image. The model then decides whether to answer directly or invoke the bounding box tool to crop a high-resolution region for further analysis before generating the final answer*

AdaptVision的核心设计围绕三个关键模块展开：**自适应视觉获取机制**、**解耦奖励函数**和**回合解耦策略优化（DTPO）**。以下逐一阐述其原理与关键公式。

### 4.1 自适应视觉获取机制

AdaptVision模拟人类“从粗到细”的视觉处理机制，将视觉token的获取决策内化为模型的自主行为。其策略定义为：

$$
\pi_{\boldsymbol{\theta}}(o \vert x) = \begin{cases} 
\pi_{\boldsymbol{\theta}}(o_{1:N} \mid x), & \text{direct answer}, \\
\pi_{\boldsymbol{\theta}}(o_{1:T} \mid x) \pi_{\boldsymbol{\theta}}(o_{T+1:N} \mid x, o_{1:T}, I_{crop}), & \text{tool call},
\end{cases}
$$

其中，$x$为输入（低分辨率图像+问题），$o_{1:T}$为工具调用token（边界框坐标），$o_{T+1:N}$为最终答案token，$I_{crop}$为从高分辨率图像裁剪的区域。

该模块的工作流程为：首先将输入图像降采样至1/4分辨率，生成占原始25%的视觉token；随后模型基于这些压缩信息自主决策——若信息充分则直接生成答案，否则调用边界框工具裁剪高分辨率关键区域，将裁剪区域的视觉token作为额外信息整合后生成最终答案。

### 4.2 解耦奖励函数设计

为引导模型在效率与精度之间取得动态平衡，AdaptVision设计了由**结果奖励**和**工具奖励**组成的复合奖励函数：

$$
\mathcal{R} = \mathcal{R}_{oc} + \mathcal{R}_{tool}
$$

**结果奖励** $\mathcal{R}_{oc}$ 包含三项：答案正确性奖励、格式奖励和平衡奖励。其中平衡奖励 $\mathcal{R}_{bal}$ 是关键创新：

$$
\mathcal{R}_{bal} = \begin{cases} 
-0.1 \cdot \mathbb{I}(r < \theta) \cdot \mathbb{I}(\mathcal{R}_{acc} = 1), & \text{direct answer}, \\
-0.1 \cdot \mathbb{I}(\mathcal{R}_{acc} = 1), & \text{tool call},
\end{cases}
$$

这里 $r = \frac{C_{direct}}{C_{direct} + C_{tool}}$ 表示组内直接回答正确的比例，$\theta$为阈值。平衡奖励的机制是：当模型通过直接回答正确时，若组内直接回答正确比例过低（$r < \theta$），施加惩罚以防止模型过度依赖低分辨率猜测；当模型通过工具调用正确时，始终施加轻微惩罚，抑制不必要的工具调用。

**工具奖励** $\mathcal{R}_{tool}$ 由裁剪正确性奖励和面积惩罚组成：

$$
\mathcal{R}_{tool} = \mathcal{R}_{crop} - \alpha \cdot \mathcal{R}_{area}
$$

面积惩罚基于裁剪区域相对低分辨率图像的面积比率 $r_a$ 计算：

$$
r_a = \frac{(x_2 - x_1) \cdot (y_2 - y_1)}{H_{low} \cdot W_{low}}, \quad \mu_a = \mu_{area}(\mathcal{G}(a))
$$

其中 $\mu_a$ 为组内正确响应且裁剪正确的样本的面积比率均值。面积惩罚项 $\mathcal{R}_{area}$ 鼓励模型选择足以保证正确性的最小区域，从而最小化视觉token消耗。

### 4.3 回合解耦策略优化（DTPO）

标准GRPO将工具token和答案token统一归一化，导致工具token因序列位置靠前且数量少而被欠优化，最终引发策略崩溃。DTPO通过两个关键改进解决此问题。

**第一，损失按回合解耦并分别归一化。** 标准GRPO的token级损失可分解为工具部分和答案部分：

$$
\frac{1}{G} \sum_{i=1}^{G} \frac{1}{N_i} \sum_{t=1}^{N_i} \mathcal{L}_{i,t}(\theta) = \underbrace{\frac{1}{G} \sum_{i=1}^{G} \frac{1}{N_i} \sum_{t=1}^{T_i} \mathcal{L}_{i,t}(\theta)}_{\text{Tool Token}} + \underbrace{\frac{1}{G} \sum_{i=1}^{G} \frac{1}{N_i} \sum_{t=T_i+1}^{N_i} \mathcal{L}_{i,t}(\theta)}_{\text{Answer Token}}
$$

DTPO将其改为分别按工具token总数和答案token总数归一化：

$$
\mathcal{T}_{\mathrm{DTPO}}(\theta) = \mathbb{E}_{x, o_i} \Bigg[ \underbrace{\frac{1}{\sum_{i=1}^{G} T_i} \sum_{i=1}^{G} \sum_{t=1}^{T_i} \mathcal{L}_{i,t}(\theta)}_{\text{Tool Token}} + \underbrace{\frac{1}{\sum_{i=1}^{G} (N_i - T_i)} \sum_{i=1}^{G} \sum_{t=T_i+1}^{N_i} \mathcal{L}_{i,t}(\theta)}_{\text{Answer Token}} \Bigg]
$$

**第二，为工具token和答案token计算不同的优势估计，实现精确信用分配：**

$$
A_{i,t} = \begin{cases} 
A_{oc}^{(i)} + \lambda \cdot A_{tool}^{(i)}, & \text{direct answer}, \\
A_{oc}^{(i)} + \lambda \cdot A_{tool}^{(i)} \cdot \mathbb{I}(1 \leq t \leq T_i), & \text{tool call},
\end{cases}
$$

其中，工具优势 $A_{tool}^{(i)}$ 和结果优势 $A_{oc}^{(i)}$ 分别基于各自奖励进行组内标准化：

$$
A_{tool}^{(i)} = \frac{\mathcal{R}_{tool}^{(i)} - \mathrm{mean}(\{\mathcal{R}_{tool}^{(i)}\}_{i=1}^{G})}{\mathrm{std}(\{\mathcal{R}_{tool}^{(i)}\}_{i=1}^{G})}
$$

$$
A_{oc}^{(i)} = \frac{\mathcal{R}_{oc}^{(i)} - \mathrm{mean}(\{\mathcal{R}_{oc}^{(i)}\}_{i=1}^{G})}{\mathrm{std}(\{\mathcal{R}_{oc}^{(i)}\}_{i=1}^{G})}
$$

$\lambda$ 为平衡工具学习与准确率提升的超参数。在工具调用序列中，仅工具token（$1 \leq t \leq T_i$）接收工具优势信号，答案token仅接收结果优势信号，从而消除信用分配模糊。

## 实验与关键发现

### 主要结果：视觉token效率与性能的帕累托前沿

AdaptVision的核心实验在9个VQA基准上系统评估了其效率-精度权衡。**Table 1**汇总了主要对比结果（以Qwen2.5-VL-7B-Instruct为Vanilla基线，100%视觉token；Down-Sample为固定1/4分辨率，25% token）。

![[assets/figures/papers/paper_list_l2759_https_arxiv_org_abs_2512_03794/figures/004_Table_1.jpg]]
*Table 1: Performance comparison with previous efficient VLM methods. Vanilla denotes the Qwen2.5-VL-7B-Instruct model. Down-Sample uses a 1/4-resolution image as input to the Vanilla model. “#Token” indicates the visual token consumption ratio relative to the vanilla model across all benchmarks. “Avg.” denotes the average performance relative to the vanilla model on all benchmarks*

**核心发现：AdaptVision以平均33%的视觉token消耗达到了Vanilla模型97.9%的相对性能**，这一结果显著优于所有对比的高效VLM方法。具体而言：

- **相对于降采样模型的飞跃**：Down-Sample模型仅保留25% token，但平均相对性能仅92.1%。AdaptVision仅增加约7%的视觉token（25%→33%），将平均准确率提升了5.8个百分点（92.1%→97.9%）。这表明模型学会在必要时“投资”少量token以换取显著精度收益。
- **相对于静态压缩方法的优势**：FastV、SparseVLM、VisionZip等静态方法在50% token保留率下，平均性能分别为93.0%、93.6%、94.7%，均低于AdaptVision的97.9%。这些方法对所有样本无差别压缩，无法应对需要精细视觉信息的困难样本。
- **相对于动态方法的优势**：VisionThink（动态选择低/高分辨率）在52% token保留率下仅达到93.7%。AdaptVision的优势源于更精细的从粗到细机制——不是整图切换分辨率，而是精准裁剪关键区域，从而以更少的token获取更相关的信息。
- **基准级表现**：在ChartQA上，AdaptVision达到95.1%相对性能（+16.3%绝对提升 vs. Down-Sample）；在MMVet上达到105.2%（+18.9%绝对提升），甚至超越Vanilla基线。在RealWorldQA上为98.1%，仅比Vanilla低2.2个百分点，但token减少67%。

**推理时间**：**Figure 4**显示，AdaptVision的端到端推理时间相比Vanilla加速1.67倍，主要得益于视觉token数量的大幅减少。虽然相比Down-Sample模型增加了工具调用的解码开销，但总体推理时间仍处于可接受范围内。

### 消融实验：奖励设计与训练算法的关键作用

#### 奖励函数组件消融

**Figure 5a**揭示了奖励函数各组件的必要性：

- **移除平衡奖励（R_bal）**：训练崩溃为过度工具调用。模型学会对所有样本都调用工具，因为工具调用通常能获得更高的准确率奖励，而平衡奖励的缺失使得模型没有动力去学习在简单样本上直接回答。
- **移除工具奖励（R_tool）**：模型完全放弃工具调用。没有工具奖励的引导，模型无法建立“裁剪正确区域→获得奖励”的因果联系，最终退化为仅在低分辨率图像上猜测答案。
- **完整奖励函数**：模型收敛到合理的工具调用比率，在效率与精度之间取得平衡。

平衡奖励的设计逻辑（Eq. 7）值得注意：当组内直接回答正确比例r低于阈值θ时，对直接回答的正确样本施加-0.1惩罚，鼓励模型更多探索工具调用；当r高于阈值时，对工具调用的正确样本施加-0.1惩罚，防止过度依赖工具。这种对称设计确保了策略不会偏向任何一种极端。

#### DTPO与GRPO的训练稳定性对比

**Figure 5b**展示了标准GRPO与DTPO的训练动态差异：

- **GRPO训练崩溃**：标准GRPO在训练后期工具调用比率急剧上升，策略最终收敛到几乎对所有样本都调用工具。这是因为GRPO对所有token使用统一的序列级奖励归一化（Eq. 3），导致工具token（通常数量少）的优化信号被答案token（数量多）稀释，产生**信用分配模糊**和**优化不平衡**问题。
- **DTPO稳定收敛**：DTPO通过按回合解耦损失（Eq. 12）和分别计算工具/结果优势（Eq. 13-15），使工具调用比率稳定在合理水平。训练曲线平滑，未出现崩溃现象。

#### 自适应工具调用行为分析

**Figure 6**展示了DTPO训练的模型学会了根据样本难度自适应调节工具调用：

- **Figure 6a**：训练过程中，模型在困难样本上的工具调用比率逐步上升，在简单样本上逐步下降，表明策略学到了有意义的难度感知行为。
- **Figure 6b**：在ChartQA（需要精细图表阅读）和MMVet（需要复杂视觉推理）等困难基准上，工具调用比率较高；在RealWorldQA（相对简单的常识问答）上，工具调用比率较低。这一模式与人类在复杂任务中投入更多注意力的行为一致。

#### 超参数灵敏度

**Table 2**分析了λ（工具优势权重）和α（面积惩罚系数）的灵敏度。在RealWorldQA上，λ∈[0.1, 0.5]时性能波动在64.81-67.32之间，α∈[0.05, 0.2]时性能保持稳定。在MME上，性能波动范围为2368-2400。这表明方法对超参数选择具有一定的鲁棒性。

#### 奖励模型选择

**Table 3**对比了不同奖励模型的效果。使用GPT-4o作为裁剪正确性判断器取得最佳性能，但使用小型开源VLM（Qwen3-VL-4B）作为替代仍能取得有竞争力的结果，且优于VisionThink。这为降低训练成本提供了可行路径。

### 失败模式与局限性分析

尽管AdaptVision取得了显著成果，但仍存在以下局限：

1. **两轮交互上限**：当前框架限制为最多两轮（低分辨率→可选工具调用），对于需要多阶段精细视觉推理的复杂任务（如多步图表推理、需要反复确认细节的场景），可能不足以提供足够的视觉信息获取轮次。

2. **外部奖励模型依赖**：训练依赖GPT-4o判断裁剪边界框的正确性（Table 7展示了判断提示模板）。这不仅引入潜在评估偏差，还增加了训练的计算和经济成本。Table 3虽展示了小型模型的替代可行性，但性能仍有差距。

3. **单一架构验证**：所有实验均在Qwen2.5-VL-7B-Instruct上完成。尽管方法设计声称架构无关，但缺乏在InternVL、LLaVA等其他主流VLM架构上的验证，迁移能力有待证实。

4. **工具种类单一**：当前仅支持边界框裁剪操作，未扩展到去模糊、放大、旋转等其他可能有益的视觉操作。在需要非裁剪类视觉增强的场景中，方法可能无法提供最优支持。

5. **超参数任务依赖性**：尽管灵敏度分析显示一定鲁棒性，但λ、α、θ等超参数的最优值可能因任务分布而异，实际部署时可能需要针对特定场景调整。

### 案例研究：从粗到细的直观验证

**Figure 7**通过典型案例对比了三种策略的行为差异：Vanilla模型消耗大量token获得正确答案；Down-Sample模型节省token但回答错误；AdaptVision智能地调用工具裁剪关键区域，以极少的额外token代价获得正确答案。**Figure 8**和**Figure 9**分别展示了直接回答和工具调用的具体案例，验证了模型能根据问题复杂度做出合理决策。

### 补充图表

![[assets/figures/papers/paper_list_l2759_https_arxiv_org_abs_2512_03794/figures/006_Figure_5.jpg]]
*Figure 5: Policy-training comparison: (a) The influence of reward design. (b) GRPO vs. DTPO*

![[assets/figures/papers/paper_list_l2759_https_arxiv_org_abs_2512_03794/figures/012_Table_3.jpg]]
*Table 3: Comparison of different reward models*

![[assets/figures/papers/paper_list_l2759_https_arxiv_org_abs_2512_03794/figures/007_Figure_6.jpg]]
*Figure 6: Tool call ratio analysis: (a) Training curves show that DTPO learns a stable and adaptive policy, increasing tool calls for hard samples while decreasing them for simple ones. (b) Across different benchmarks, AdaptVision demonstrates a well-balanced ability to invoke tools when necessary and answer directly when possible*

![[assets/figures/papers/paper_list_l2759_https_arxiv_org_abs_2512_03794/figures/008_Figure_7.jpg]]
*Figure 7: Case study: (1) The vanilla model yields a correct answer but consumes a large number of visual tokens; (2) The down-sample model reduces token usage but fails to answer correctly; (3) AdaptVision smartly invokes the tool to produce a correct answer with minimal visual token cost*

## 定位与知识库关联

### 1. 核心问题定位：从被动压缩到主动获取

现有高效VLM方法的核心瓶颈在于**被动策略**：它们预先固定视觉token的保留比例或压缩规则，无法根据任务的实际复杂度动态调整。静态压缩方法（如 **FastV**、**SparseVLM**、**VisionZip**）在推理前即丢弃大量视觉信息，导致简单任务浪费计算资源，复杂任务则因信息不足而精度受损。AdaptVision将这一问题重新定义为**自适应视觉获取问题**——让模型在低分辨率初始化后，自主决定是否通过工具调用获取额外的高分辨率视觉信息，从而在效率与精度之间取得动态平衡。这一思路模拟了人类视觉的从粗到细（coarse-to-fine）注意机制：先快速扫描全局，再对关键区域进行精细分析。

### 2. 与现有高效VLM方法的对比定位

**静态压缩方法**（保留固定比例的视觉token）：
- **FastV**：基于注意力分数进行固定比例剪枝，保留50%视觉token。该方法忽略了不同样本对视觉信息需求的差异，简单样本浪费token，困难样本可能丢失关键细节。
- **SparseVLM**：利用跨模态相关性进行静态token压缩，同样保留50%。其压缩决策独立于具体问题，缺乏任务自适应性。
- **VisionZip**：选择语义相关的视觉token进行压缩（保留50%）。虽引入了语义信息，但压缩策略仍是全局固定的。
- **降采样（Down-Sample）**：直接将输入图像降采样至1/4分辨率，保留25%视觉token。这是最激进的静态策略，平均性能仅为原始模型的92.1%（Table 1）。

**动态方法的初步尝试**：
- **VisionThink**：使用强化学习让模型在低分辨率与原始图像之间二选一。这是动态方法的早期探索，但其选择粒度粗糙（全图二选一），且其发布模型实际使用了99%的视觉token，动态性有限。AdaptVision的重新实现版本（52% token）性能明显低于AdaptVision。

**AdaptVision的差异化优势**：
AdaptVision在降采样模型基础上仅增加7%的视觉token（25%→33%），便将平均性能从92.1%提升至97.9%（相对于Vanilla模型），在9个VQA基准测试上以平均33%的视觉token实现了97.9%的相对性能（Table 1）。这一效率-精度权衡显著优于所有对比方法。关键在于其**空间粒度更细**：不是全图二选一，而是通过边界框工具精确裁剪问题相关区域，实现token的按需分配。

### 3. 训练方法的谱系定位

**标准GRPO的局限性**：
AdaptVision的训练基于GRPO（Group Relative Policy Optimization）框架，但标准GRPO存在两个根本性问题：
- **信用分配模糊**：统一序列级奖励无法区分工具调用token和答案生成token的贡献，导致工具token的优化信号被稀释。
- **优化不平衡**：所有token统一归一化，使得数量占优的答案token主导梯度更新，工具token欠优化。

**DTPO的创新点**：
Decoupled Turn Policy Optimization（DTPO）通过两个关键改进解决上述问题：
1. **按回合解耦损失**：将策略损失按功能分解为工具token损失和答案token损失，分别归一化（Eq. 11-12），确保两部分获得均衡的优化信号。
2. **独立优势估计**：为工具奖励和结果奖励分别计算组内标准化优势（Eq. 13-15），实现精确的信用分配。工具token仅受工具奖励驱动，答案token则综合结果奖励和工具奖励。

实验表明，标准GRPO在训练后期策略崩溃至过度工具调用，而DTPO训练曲线平稳收敛，工具调用比率稳定在合理水平（Figure 5b）。

### 4. 奖励设计的因果机制

AdaptVision的奖励函数设计揭示了效率-精度平衡的因果机制：

- **平衡奖励（Balance Reward）**：防止模型走向两个极端——过度依赖工具调用（浪费token）或过度依赖低分辨率猜测（损失精度）。消融实验显示，移除平衡奖励导致训练崩溃至过度工具调用（Figure 5a）。
- **工具奖励（Tool Reward）**：由裁剪正确性和面积惩罚组成。面积惩罚激励模型选择最小的有效区域，直接驱动token效率优化。移除工具奖励则导致模型完全放弃工具调用（Figure 5a）。
- **超参数鲁棒性**：λ（工具优势权重）和α（面积惩罚系数）在合理范围内变化时，性能保持稳定（RealWorldQA: 64.81-67.32, MME: 2368-2400，Table 2），表明奖励设计具有良好的泛化性。

### 5. 适用边界与局限

**已验证的适用范围**：
- 基于Qwen2.5-VL-7B-Instruct的充分验证，涵盖9个VQA基准测试（包括ChartQA、MMVet、RealWorldQA等）。
- 端到端推理时间加速1.67倍（Figure 4），在效率敏感场景具有实用价值。
- DTPO学会根据样本难度自适应调节工具调用比率：困难样本提高调用率，简单样本降低（Figure 6），验证了自适应机制的有效性。

**明确局限**：
1. **交互轮数限制**：当前框架限制为最多两轮交互（低分辨率→工具调用→答案），可能不足以处理需要多阶段精细视觉推理的复杂任务（如多步空间推理、层次化视觉分析）。
2. **外部奖励模型依赖**：训练依赖GPT-4o作为裁剪正确性判断的奖励模型，可能引入评估偏差并增加训练成本。尽管使用小型开源VLM（Qwen3-VL-4B）作为替代仍能取得有竞争力性能（Table 3），但性能略有下降。
3. **架构验证单一**：仅在Qwen2.5-VL-7B-Instruct上进行了充分实验，尚未在其他VLM架构（如InternVL、LLaVA系列）上展示迁移能力。
4. **工具种类单一**：仅支持边界框裁剪操作，未能扩展到去模糊、放大、旋转等其他视觉增强操作，限制了处理多样化视觉退化场景的能力。
5. **超参数任务敏感性**：奖励函数中的超参数（λ、α、θ）需要针对具体任务调整，尽管灵敏度分析显示在一定范围内鲁棒，但最优值可能因任务分布而异。

### 6. 开放问题与未来方向

1. **多轮工具调用扩展**：能否将框架扩展到多轮交互，支持“裁剪→分析→再裁剪”的迭代式视觉推理，同时保持推理效率？这需要解决多轮信用分配和终止条件学习等新挑战。

2. **跨架构迁移验证**：AdaptVision声称架构无关，但在其他VLM架构（如InternVL、LLaVA系列、MiniCPM-V）上的性能表现和训练稳定性尚待验证。不同架构的视觉编码器和投影层可能影响工具调用的学习动态。

3. **奖励模型自主化**：能否使用完全开源或更小的奖励模型替代GPT-4o，甚至通过自监督信号训练裁剪正确性判断器，进一步降低训练成本并消除外部依赖？

4. **动态分辨率与工具调用融合**：当前框架固定使用1/4分辨率初始化，能否结合动态分辨率选择机制，让模型自主决定初始分辨率，再通过工具调用补充细节？这将实现更灵活的token分配策略。

5. **多模态任务泛化**：从粗到细的自适应获取范式是否适用于视频理解（时序注意力分配）、3D视觉（多视角信息获取）、文档理解（结构化区域提取）等更广泛的多模态任务？这需要重新设计工具接口和奖励函数。

6. **工具生态扩展**：能否将工具调用扩展为更通用的视觉操作集合（去模糊、超分辨率、目标检测、OCR等），让模型根据任务需求自主选择和组合工具？这将使框架从“高效VLM”升级为“视觉Agent”。

## 原文 PDF

![[paperPDFs/CVPR_2026/AdaptVision_Efficient_Vision_Language_Models_via_Adaptive_Visual_Acquisition.pdf]]
