---
title: "LocateAnything3D: Vision-Language 3D Detection with Chain-of-Sight"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LocateAnything3D_Vision_Language_3D_Detection_with_Chain_of_Sight.pdf
project_link: null
code_link: "https://github.com/LLM-Red-Team/emo-visual-data"
huggingface_link: "https://huggingface.co/datasets/EmileEsmaili/sheet_music_clean"
aliases:
- LocateAnything3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入 Chain-of-Sight（CoS）序列，将2D检测作为视觉思维链（visual chain-of-thought）插入到3D token预测中，同时采用近到远的物体排序和中心→尺寸→旋转的框分解，将3D检测转化为自回归模型易于学习的下一token预测任务。
primary_logic: 通过让自回归解码器先输出2D框作为中间证据，再在2D约束下预测3D参数，并按照深度排序和语义顺序组织token序列，可以大幅降低单目3D推断的模糊性，使VLM能够端到端地学习多物体3D检测，无需额外检测头。
claims:
- 在Omni3D基准上，LocateAnything3D的AP3D达到38.90，超越先前最佳方法（包含真值2D框的DetAny3D）4.52点。
- 相比直接的3D预测，CoS公式在仅使用10%训练数据时即达到竞争性能，且最终AP3D高出13.4（36.1 vs 22.7）。
- 使用近到远排序的AP3D_out为33.1，显著优于从左到右扫描线排序的26.7。
- 移除2D CoS（直接预测3D）导致性能大幅下降（纯3D基线AP3D仅22.7），且训练收敛缓慢。
---

# LocateAnything3D: Vision-Language 3D Detection with Chain-of-Sight

> [!tip] 核心洞察
> 通过让自回归解码器先输出2D框作为中间证据，再在2D约束下预测3D参数，并按照深度排序和语义顺序组织token序列，可以大幅降低单目3D推断的模糊性，使VLM能够端到端地学习多物体3D检测，无需额外检测头。

| 字段 | 内容 |
|------|------|
| 中文题名 | LocateAnything3D：基于视觉链的视觉语言3D检测 |
| 英文题名 | LocateAnything3D: Vision-Language 3D Detection with Chain-of-Sight |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20648) · [Code](https://github.com/LLM-Red-Team/emo-visual-data) · [HuggingFace](https://huggingface.co/datasets/EmileEsmaili/sheet_music_clean) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | LocateAnything3D |
| Dataset | Omni3D, KITTI, SUN-RGBD, ARKitScenes |

> [!tip] 效果简介
> - Omni3D (full unified) 上，AP3D (mean) 38.90 vs 34.38 (DetAny3D w/ GT 2D Box) (+4.52)。
> - KITTI (Zero-shot Novel) 上，AP (KITTI novel) 25.87 vs 25.73 (DetAny3D w/ Grounding-DINO 2D Boxes) (+0.14)。
> - SUN-RGBD (Zero-shot Novel) 上，AP (SUN-RGBD novel) 26.33 vs 21.07 (DetAny3D w/ Grounding-DINO 2D Boxes) (+5.26)。

## 概述

单目3D目标检测是自动驾驶、机器人导航和增强现实等应用的核心感知能力。然而，现有视觉语言模型（VLM）缺乏原生的多物体3D检测能力——主流方法要么依赖任务特定的检测头与闭集类别，要么需要外部2D检测器提供区域提议，无法在统一的token预测接口下完成开放词汇的3D感知。

**LocateAnything3D** 提出了一种使VLM原生支持3D检测的范式。其核心瓶颈突破在于引入 **Chain-of-Sight（CoS）序列**：将2D检测作为视觉思维链（visual chain-of-thought）插入到自回归token预测中，使解码器先输出2D框作为中间证据，再在2D约束下预测3D参数。这一设计将单目3D检测转化为自回归模型易于学习的下一token预测任务，无需额外检测头。

在方法设计上，CoS序列遵循三层结构化组织：**物体间按深度从近到远排序**（near-to-far）、**物体内先2D后3D的交错布局**、以及**3D框内部按中心→尺寸→旋转的语义顺序分解**。训练数据经过统一的多源语料库构建，按照CoS格式化为对话样本，并加入反幻觉负样本以抑制虚检。

实验结果表明，LocateAnything3D在Omni3D基准上达到 **AP3D 38.90**，超越先前最佳方法（含真值2D框的DetAny3D）**+4.52点**。在零样本新类别上，仅凭单张图像同时预测2D与3D框，即超越依赖外部2D检测器的竞争方法（KITTI +0.14, SUN-RGBD +5.26, ARKitScenes +4.50）。消融研究进一步验证：移除2D CoS导致性能大幅下降（纯3D基线AP3D仅22.7），而CoS模型在仅使用10%训练数据时即展现出显著的数据效率优势。

在方法谱系上，LocateAnything3D区别于 **Cube R-CNN**（Brazil et al., CVPR 2023）的闭集检测范式、**OVMono3D**（Yao et al., arXiv 2024）依赖外部2D检测器的提升策略、以及 **DetAny3D**（Zhang et al., ICCV 2025）的直接3D输出方式，首次在统一的自回归语言模型框架内实现了端到端的开放词汇2D+3D联合预测。

## 背景与动机

### 问题背景：视觉语言模型在3D感知中的能力缺口

视觉语言模型（VLM）在图像描述、视觉问答、2D检测等任务上已取得显著进展，但在单目多物体3D检测这一核心感知能力上存在明显缺口。当前VLM缺乏原生的3D定位能力——它们无法在统一的token预测接口下，仅凭单张RGB图像完成开放词汇的多物体3D框预测。这一缺陷的根源在于：3D检测需要从2D投影中恢复深度、尺寸和朝向，这是一个固有的病态逆问题，而现有VLM的序列建模范式并未针对这一推理链条进行专门设计。

### 现有方法的局限：依赖外部模块与闭集假设

现有单目3D检测方法可大致分为三类，均存在结构性局限：

**闭集检测器**（如 **Cube R-CNN** (Brazil et al., CVPR 2023)）依赖任务特定的检测头和固定类别集合，无法泛化到新类别。这类方法将3D检测视为回归问题，通过专门设计的损失函数和网络分支输出3D参数，但每新增一个类别就需要重新设计和训练检测头。

**开放词汇方法**（如 **OVMono3D** (Yao et al., arXiv 2024)）试图突破类别限制，但其管线高度依赖外部2D检测器。具体而言，它们先用独立的2D检测器（如Grounding-DINO）生成区域提议，再通过专门的提升模块将2D框提升到3D。这种解耦设计带来两个问题：一是2D检测器的误差会直接传播到3D阶段，无法端到端联合优化；二是2D和3D之间缺乏显式的推理连接，模型只是机械地将2D结果"提升"，而非真正理解2D证据如何约束3D推断。

**可提示检测器**（如 **DetAny3D** (Zhang et al., ICCV 2025)）支持开放世界的3D检测，但同样依赖外部2D框作为输入。即使给予真值2D框这一特权信息，其性能仍有上限，说明单纯将2D框作为输入条件并不足以充分挖掘2D-3D之间的几何约束关系。

**基于MLLM的方法**（如 **Cube-LLM** (Cho et al., CVPR 2024)）尝试将大型多模态语言模型引入3D定位，但仅支持单物体场景，无法处理多物体检测任务，且需要海量训练数据（约960万张图像）才能达到可用性能。

### 核心瓶颈：缺乏结构化的2D-3D推理链条

上述方法的共同瓶颈在于：它们将2D和3D视为两个独立或弱耦合的阶段，而非一个连贯的推理过程。人类在单目3D感知中会自然地先识别物体在图像中的位置（2D），再基于该区域推断其空间属性（3D）——这是一个"先定位，后测距"的认知链条。然而，现有方法要么跳过2D直接预测3D（纯3D回归），要么将2D作为外部输入而非模型内部推理的中间产物，导致模型无法学习2D证据如何系统性地约束3D推断。

### 本文动机：将3D检测转化为VLM原生的下一token预测任务

本文的核心动机是：**能否让VLM以原生方式——即自回归下一token预测——端到端地学习多物体3D检测，而无需任何外部检测器或任务特定头？**

这一目标的实现需要解决三个关键挑战：

1. **序列化问题**：如何将无序的3D框集合转化为VLM可学习的token序列？
2. **模糊性问题**：如何在单目2D观测与3D输出之间建立显式的推理连接，降低推断的模糊性？
3. **规模化问题**：如何构建大规模、多源统一的训练数据，使VLM能够学习跨场景、跨类别的3D检测能力？

LocateAnything3D通过引入**Chain-of-Sight（CoS）**——一种将2D检测作为视觉思维链插入3D token预测的序列化策略——系统性地回应了上述挑战。其核心洞察是：让自回归解码器先输出2D框作为中间证据，再在2D约束下预测3D参数，并按照深度排序和语义顺序组织token序列，可以大幅降低单目3D推断的模糊性，使VLM能够端到端地学习多物体3D检测。

## 核心创新

LocateAnything3D 的核心创新在于将单目多物体 3D 检测重新定义为视觉语言模型（VLM）原生的下一 token 预测任务，其关键抓手是 **Chain-of-Sight（CoS）序列化机制**。与现有方法依赖外部 2D 检测器、任务特定检测头或闭集类别不同，CoS 通过三个层次的设计改变了模型的推理方式，使自回归语言模型能够端到端地输出开放词汇的 3D 检测结果。

### 1. 3D 检测作为视觉思维链：Chain-of-Sight 序列化

现有方法中，**Cube R-CNN**（Brazil et al., CVPR 2023）使用闭集检测头，**OVMono3D**（Yao et al., arXiv 2024）和 **DetAny3D**（Zhang et al., ICCV 2025）依赖外部 2D 检测器提供区域提议，再通过专门模块提升到 3D。这些方法将 2D 与 3D 解耦为两个独立阶段，缺乏端到端的联合推理。

LocateAnything3D 的核心改变是：**在自回归解码中交错输出 2D 和 3D token**，将 2D 检测作为显式的视觉思维链（visual chain-of-thought），约束后续的 3D 推断。具体而言，解码器生成的 token 序列为：

$$\mathcal{S} = (\mathbf{q}_1, \mathbf{b}_1, \mathbf{q}_2, \mathbf{b}_2, \dots, \langle \mathrm{eos} \rangle)$$

其中每个物体先输出 2D 框 $\mathbf{q}_i$，再输出其对应的 3D 框 $\mathbf{b}_i$。序列的条件概率被分解为：

$$P(\mathcal{S} | I, c) = \prod_{i=1}^{N_c} \underbrace{P(\mathbf{q}_i | I, c, \mathcal{S}_{<i})}_{\mathrm{2D\ localization}} \underbrace{P(\mathbf{b}_i | I, c, \mathcal{S}_{<i}, \mathbf{q}_i)}_{\mathrm{3D\ estimation}} \cdot P(\langle \text{eos} \rangle | I, c, \mathcal{S}_{\leq N_c})$$

这一分解的因果逻辑是：2D 定位为 3D 估计提供了强先验——知道物体在图像中的位置和大致尺度后，单目深度推断的模糊性被大幅降低。**消融实验证实了这一设计的必要性**：移除 2D CoS（直接预测 3D）导致纯 3D 基线 AP3D 仅 22.7，而完整 CoS 模型达到 36.1（Table 4）；训练动态分析进一步显示，无 2D 预训练的模型从零开始训练收敛缓慢且最终精度更低（Figure 4 右）。

### 2. 物体间排序：从近到远的课程式学习

现有方法通常按 2D 扫描线顺序或随机顺序处理多物体，未考虑单目 3D 推断中深度估计的难易程度。LocateAnything3D 提出**按深度从近到远排序（near-to-far）**，形成课程式学习策略：近处物体深度估计更可靠，模型先学习简单样本，逐步建立对远处物体的推断能力。

这一设计的有效性在消融实验中得到验证：近到远排序的 AP3D_out 为 33.1，显著优于从左到右扫描线排序的 26.7 和随机排序的 29.8（Table 4）。背后的因果机制是：近处物体的视觉特征更丰富、尺度更大，2D 到 3D 的映射更确定；模型在解码近处物体时积累的场景几何信息，可作为后续远处物体推断的上下文。

### 3. 3D 框的语义化 token 顺序：中心 → 尺寸 → 旋转

传统方法使用基于角点的编码（8 个顶点）或其他无序表示来描述 3D 框，这些表示与自回归模型的逐 token 生成范式不匹配。LocateAnything3D 采用**语义化的顺序分解**：先输出中心坐标 $\mathbf{t}$，再输出尺寸 $\mathbf{d}$，最后输出旋转 $\mathbf{R}$。

$$\mathbf{b}_i = (\mathbf{t}_i, \mathbf{d}_i, \mathbf{R}_i) \quad \mathbf{t}_i \in \mathbb{R}^3; \mathbf{d}_i \in \mathbb{R}_+^3; \mathbf{R}_i \in \mathrm{SO}(3)$$

这一顺序的合理性在于：中心位置是 3D 框最关键的参数，决定了物体在空间中的定位；尺寸次之，定义了物体的空间范围；旋转最后，在中心与尺寸确定后对框进行姿态微调。消融实验显示，中心→尺寸→旋转的顺序（AP3D_out=33.1）明显优于其他组合，如尺寸→中心→旋转仅 29.6（Table 4）。

### 4. 交错式 vs 聚类式序列化

另一个关键设计选择是**交错式（interleaved）CoS 序列**——每个物体的 2D 和 3D 紧邻输出，而非先输出全部 2D 再输出全部 3D 的聚类式策略。消融结果表明，交错式策略在遮挡多的场景中更为鲁棒：在 KITTI 上 AP3D 为 22.1，而聚类式仅 17.4（Table 5）。其因果机制在于：交错序列保持了 2D 与 3D 之间的局部对应关系，使模型在生成 3D 参数时能直接利用刚生成的 2D 上下文，避免了长距离关联带来的注意力分散。

### 5. 训练数据的 CoS 格式化与反幻觉机制

为支持上述设计，LocateAnything3D 构建了以相机为中心的大规模语料库，将异构的单目 3D 基准统一为 CoS 格式的训练样本：先 2D 后 3D、从近到远排序。此外，引入**反幻觉负样本**——在训练中混入不包含任何目标物体的图像，要求模型直接输出 `<eos>`，抑制模型在无目标场景中产生虚假检测。

---

**总结**：LocateAnything3D 的核心创新并非提出新的网络结构，而是通过 CoS 序列化将 3D 检测转化为 VLM 可自然学习的下一 token 预测任务。三个层次的设计——近到远排序、2D→3D 分解、中心→尺寸→旋转顺序——共同降低了单目 3D 推断的模糊性，使模型在统一的自回归接口下实现了开放词汇的多物体 3D 检测，无需任何外部检测器或任务特定模块。

## 整体框架

LocateAnything3D 将开放词汇的单目多物体 3D 检测统一为视觉语言模型（VLM）原生的下一 token 预测任务。其核心是一个三段式管线：**视觉编码 → 语言模型自回归解码 → Chain-of-Sight 序列输出**，全程无需任务特定的检测头或外部 2D 检测器。

### 输入层：图像、文本与可选视觉提示

模型接收单张 RGB 图像，配合自由形式的文本类别描述（如 “car”、“chair”）以及可选的视觉提示——用户可以在图像上拖拽 2D 框或点击关键点来指定感兴趣区域。这种灵活的提示机制使同一模型能同时支持开放词汇检测（detection）和目标定位（grounding）。

图像由 **SigLIP 视觉编码器**（启用 FlashAttention 2）编码为视觉 token 序列，随后经一个**两层 MLP 投影器**映射到语言模型的隐空间，与文本 token 拼接后送入因果语言模型。

### 核心解码器：Qwen2-8B 因果语言模型

解码阶段采用 **Qwen2-8B** 因果语言模型，端到端训练。它接收视觉 token 与文本提示的拼接序列，以自回归方式逐 token 生成结构化输出。关键在于，解码器不依赖任何外部检测头——3D 框的定位与参数估计完全由语言模型在 token 空间中完成。

### Chain-of-Sight 序列：从 2D 到 3D 的视觉思维链

解码器输出的是一段精心组织的 token 序列，称为 **Chain-of-Sight（CoS）**：

$$
\mathcal{S} = (\mathbf{q}_1, \mathbf{b}_1, \mathbf{q}_2, \mathbf{b}_2, \dots, \langle \mathrm{eos} \rangle)
$$

每个物体实例依次生成一个 2D 框 $\mathbf{q}_i = (x^{\mathrm{min}}, y^{\mathrm{min}}, x^{\mathrm{max}}, y^{\mathrm{max}})$ 和紧随其后的 3D 框 $\mathbf{b}_i = (\mathbf{t}_i, \mathbf{d}_i, \mathbf{R}_i)$。这种“先 2D 后 3D”的交错布局将 2D 定位作为视觉思维链（visual chain-of-thought），为后续的 3D 推断提供显式的空间约束，大幅降低了单目深度估计的模糊性。

序列的条件概率被分解为两个阶段的乘积：

$$
P(\mathcal{S} \mid I, c) = \prod_{i=1}^{N_c} \underbrace{P(\mathbf{q}_i \mid I, c, \mathcal{S}_{<i})}_{\text{2D 定位}} \underbrace{P(\mathbf{b}_i \mid I, c, \mathcal{S}_{<i}, \mathbf{q}_i)}_{\text{3D 估计}} \cdot P(\langle \text{eos} \rangle \mid I, c, \mathcal{S}_{\leq N_c})
$$

### 序列组织的三层设计

CoS 序列的内部组织遵循三层设计，共同决定了模型的性能瓶颈与泛化能力：

1. **物体间排序：近到远（Near-to-Far）**  
   多物体按相机坐标系下的深度从小到大排列。这种由易到难的课程式排序使模型先处理信息丰富、遮挡少的近处物体，再逐步推断远处目标。消融实验表明，近到远排序的 AP3D_out 达到 33.1，远优于扫描线排序（26.7）和随机排序（29.8）。

2. **物体内分解：2D → 3D**  
   每个实例先输出 2D 框作为中间证据，再基于该 2D 约束预测 3D 参数。移除 2D CoS（即直接预测 3D）会导致性能崩溃——纯 3D 基线在 Omni3D 上的 AP3D 仅为 22.7，而完整 CoS 达到 36.1。

3. **3D 框内 token 顺序：中心 → 尺寸 → 旋转**  
   3D 框的 9 个连续值按语义化顺序排列：先输出中心坐标 $\mathbf{t} = (X, Y, Z)$，再输出尺寸 $\mathbf{d} = (W, H, L)$，最后输出旋转 $\mathbf{R}$。这种顺序优于其他排列（如尺寸→中心→旋转仅 29.6），与人类从“位置”到“形状”再到“朝向”的认知习惯一致。

### 端到端输出

解码器生成完整的 CoS 序列后，直接解析为带类别标签的 3D 框集合，投影回图像或鸟瞰图即可获得可视化的检测结果。整个过程从单张图像到多物体 3D 框，完全在统一的 token 预测框架内完成，无需任何后处理或非极大值抑制。

![Figure 2](figure_placeholder)

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of LocateAnything3D. (1) Model input: a single RGB image with text and optional visual prompts (boxes/clicks). (2) Chain-of-Sight (CoS) decoding: a VLM decoder first emits 2D detections as an explicit visual evidence, then continues the sequence to 3D. Decoding follows three layers of design: inter-object curriculum ordering detections from near to far; intra-object factorization using 2D as CoS to robustly infer 3D; and intra-3D tokenization that outputs center, size, and rotation. (3) We output calibrated multi-object 3D boxes with open-vocabulary categories and flexible prompting, yielding strong results on Omni3D. We use turbo colormap for boxes to demonstrate their depth,...*

### 补充图表

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/001_Figure_1.jpg]]
*Figure 1: LocateAnything3D unifies 3D detection and grounding in a single vision-language model. It supports open-world categories with free-form text guidance and flexible visual prompts (e.g., drag boxes, click points). All examples are zero-shot, highlighting strong out-of-domain generalizability. The bar chart (right) shows that LocateAnything3D achieves state-of-the-art AP3D on Omni3D benchmark*

## 核心模块与公式推导

### 问题形式化

LocateAnything3D 将单目多物体 3D 检测转化为自回归序列建模问题。给定单张 RGB 图像 $I$ 和类别提示 $c$，目标是从条件分布中采样一组 3D 边界框 $\mathcal{B} = \{\mathbf{b}_1, \dots, \mathbf{b}_{N_c}\}$。

每个 3D 框在相机坐标系下表示为三元组：

$$
\mathbf{b}_i = (\mathbf{t}_i, \mathbf{d}_i, \mathbf{R}_i) \quad \mathbf{t}_i \in \mathbb{R}^3;\; \mathbf{d}_i \in \mathbb{R}_+^3;\; \mathbf{R}_i \in \mathrm{SO}(3)
$$

其中 $\mathbf{t}_i = (X, Y, Z)$ 为中心坐标（米），$\mathbf{d}_i$ 为尺寸，$\mathbf{R}_i$ 为旋转矩阵。标准自回归分解将联合分布展开为：

$$
P(\mathcal{B} \mid I, c) = \prod_{i=1}^{N_c} P(\mathbf{b}_i \mid I, c, \mathbf{b}_{<i})
$$

这一朴素分解的瓶颈在于：从单目图像直接推断 3D 参数具有高度模糊性，纯 3D 自回归基线仅能达到 22.7 AP3D（Table 4，100% 数据），且收敛缓慢。

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/007_Table_4.jpg]]
*Table 4: Ablation study of Chain-of-Sight (CoS) design choices. We evaluate each component of our three-layer decoding design on Omni3D_OUT. All results are reported using*

### Chain-of-Sight 序列分解

核心创新在于将 2D 检测作为“视觉思维链”（visual chain-of-thought）插入到 3D token 预测中。解码器输出的 token 序列 $\mathcal{S}$ 按物体交错排列：

$$
\mathcal{S} = (\mathbf{q}_1, \mathbf{b}_1, \mathbf{q}_2, \mathbf{b}_2, \dots, \langle \mathrm{eos} \rangle)
$$

其中 $\mathbf{q}_i = (x^{\min}, y^{\min}, x^{\max}, y^{\max})$ 为第 $i$ 个物体的 2D 紧致像素框。对应的条件概率分解为：

$$
P(\mathcal{S} \mid I, c) = \prod_{i=1}^{N_c} \underbrace{P(\mathbf{q}_i \mid I, c, \mathcal{S}_{<i})}_{\text{2D 定位}} \underbrace{P(\mathbf{b}_i \mid I, c, \mathcal{S}_{<i}, \mathbf{q}_i)}_{\text{3D 估计}} \cdot P(\langle \text{eos} \rangle \mid I, c, \mathcal{S}_{\leq N_c})
$$

**因果机制**：该分解将单目 3D 推断分解为两个阶段——先通过 2D 定位确定物体在图像平面的投影区域，再在该 2D 约束下估计深度、尺寸和朝向。2D 框 $\mathbf{q}_i$ 作为中间证据，大幅降低了 3D 参数推断的模糊性。消融实验表明，移除 2D CoS（直接预测 3D）导致性能从 36.1 骤降至 22.7 AP3D（Table 4），且训练收敛速度显著变慢（Figure 4 右）。

### 三层解码设计

CoS 解码通过三个层次的结构化设计使自回归模型更易学习：

**物体间排序（Inter-object Ordering）**：按深度从近到远排列物体（near-to-far curriculum）。近处物体纹理清晰、遮挡少，模型先处理简单样本再逐步推进到远处物体，形成由易到难的课程学习。该策略的 AP3D_out 为 33.1，显著优于从左到右扫描线排序的 26.7 和随机排序的 29.8（Table 4）。

**物体内分解（Intra-object Factorization）**：采用 2D → 3D 的顺序，即先输出 2D 框再输出对应 3D 框。实验表明，先 2D 后 3D 的布局（2D-then-3D）优于先 3D 后 2D 或仅输出 3D 的变体（Table 4）。

**3D 框内 token 化（Intra-3D Tokenization）**：3D 参数按语义顺序输出：中心 $\mathbf{t}$ → 尺寸 $\mathbf{d}$ → 旋转 $\mathbf{R}$。这一顺序比尺寸→中心→旋转等其他排列更符合几何直觉（中心是空间定位的锚点），AP3D_out 差距达 3.5 点（33.1 vs 29.6，Table 4）。

### 序列化策略选择

默认采用**交错式**（interleaved）序列化策略，即每个物体依次输出 $(\mathbf{q}_i, \mathbf{b}_i)$ 对。与之对比的**聚类式**（clustered）策略先输出所有 2D 框再输出所有 3D 框。在遮挡密集场景（如 KITTI）中，交错式策略显著更鲁棒（AP3D 22.1 vs 17.4，Table 5），原因是聚类式策略将 2D 和 3D 序列分离，增加了跨序列关联的难度。

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/009_Table_5.jpg]]
*Table 5: Ablation of Token Serialization Strategy. We compare our default Interleaved Chain-of-Sight strategy*

### 流水线模块

完整流水线由以下模块构成：

- **SigLIP Vision Encoder**：将输入图像编码为视觉 token，启用 FlashAttention 2 加速。
- **MLP Projector**：两层 MLP，将视觉 token 映射到语言模型隐空间。
- **Qwen2-8B Language Model**：自回归因果语言模型，接收视觉和文本 token，按 CoS 序列生成 2D → 3D token。
- **Chain-of-Sight Decoding Head**：由语言模型本身实现的解码过程，无需额外检测头，直接输出交错式 $\langle 2D, 3D \rangle$ 序列。

整个模型端到端训练，无需外部 2D 检测器或任务特定的 3D 检测头，统一了检测和定位任务。

## 实验与分析

### 核心性能：Omni3D 基准 3D 检测

LocateAnything3D 在 Omni3D 统一基准上取得了全面的最优结果（Table 1）。在室外子集（Omni3D_OUT）上，模型在 AP3D 三项指标上均超越先前方法；在全量统一数据集（室内+室外）上，整体平均 AP3D 达到 **38.90**，比先前最佳方法 **DetAny3D**（Zhang et al., ICCV 2025）在使用真值 2D 框作为特权输入的条件下还高出 **+4.52** 点。这意味着模型仅凭单张 RGB 图像，端到端地同时预测 2D 和 3D 框，即超越了依赖外部 2D 真值的方法。

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/003_Table_1.jpg]]
*Table 1: 3D detection on the Omni3D benchmark. Our LocateAnything3D achieves state-of-the-art results over all baselines, even outperform DetAny3D with additional ground-truth 2D inputs on metrics. The first three columns (Omni3D_OUT) show outdoor-only results, while the remaining columns show results on the full unified dataset spanning indoor and outdoor scenes*

与闭集检测器 **Cube R-CNN**（Brazil et al., CVPR 2023）和开放词汇方法 **OVMono3D**（Yao et al., arXiv 2024）相比，LocateAnything3D 的优势幅度更为显著。这验证了 Chain-of-Sight 序列化方案在多物体、开放词汇 3D 检测任务上的有效性。

### 零样本泛化：新类别检测

在零样本新类别检测任务上（Table 2），LocateAnything3D 在三个基准上均取得最佳性能：KITTI 上 AP3D 为 **25.87**（+0.14 vs DetAny3D），SUN-RGBD 上为 **26.33**（+5.26），ARKitScenes 上为 **29.06**（+4.50）。值得注意的是，所有基线方法均依赖外部 2D 检测器（如 Grounding-DINO）提供 2D 框作为额外输入，而 LocateAnything3D 仅从单张图像端到端地联合预测 2D 和 3D 框，不依赖任何外部模块。这一结果直接证明了 CoS 机制将 2D 定位作为视觉思维链内化于模型推理中的优势——模型学会了在未见类别上自主完成“先定位 2D 区域，再推断 3D 结构”的推理链。

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/005_Table_2.jpg]]
*Table 2: LocateAnything3D achieves the best zero-shot 3D detection performance, demonstrating strong generalization to unseen object classes. Notably, baseline methods rely on an external detector for 2D box as additional input, while our method jointly predicts both 2D and 3D boxes end-toend from a single image alone. Following existing methods, we report*

### 室内 3D 目标定位

在室内 3D 目标定位任务上（Table 3），LocateAnything3D 以远少于对比方法的训练数据量（1.7M vs 9.6M 图像）取得了显著优势。在仅提供类别名称的提示下（$\mathrm{AP_{3D}^{cat}}$），Objectron 上达到 **72.5**（+2.7 vs Cube-LLM_large），ARKitScenes 上达到 **41.7**（+18.2），SUN-RGBD 上与 Cube-LLM_large 持平。当额外提供空间位置描述时（$\mathrm{AP_{3D}^{cat+loc}}$），LocateAnything3D 展现出更强的空间推理能力：Objectron 上 **75.0**（vs 45.4），ARKitScenes 上 **53.9**（vs 31.8），SUN-RGBD 上 **39.5**（vs 28.8）。**Cube-LLM**（Cho et al., CVPR 2024）在加入位置信息后性能反而下降或提升微弱，说明其未能有效利用空间提示；而 LocateAnything3D 的 CoS 解码天然将空间定位作为生成过程的一部分，因此能更好地融合位置先验。

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/006_Table_3.jpg]]
*Table 3: Indoor 3D Object Grounding Performance. We compare LocateAnything3D against Cube-LLM trained on different data scales*

### Chain-of-Sight 设计消融

Table 4 系统消融了 CoS 三层解码设计的每个组件，所有实验在 Omni3D_OUT 上以 $\mathrm{AP_{3D}^{out}}$ 报告。

**物体间排序策略**：近到远排序（Near-to-Far）取得最优 $\mathrm{AP_{3D}^{out}=33.1}$，显著优于从左到右扫描线排序（26.7）和随机排序（29.8）。这一结果验证了“由近及远”的课程式排序能降低自回归模型的预测难度——近处物体通常更大、纹理更清晰，先预测它们为后续远处物体的推断提供了场景上下文。

**2D 与 3D 的解耦布局**：先 2D 后 3D 的布局（2D-then-3D）取得 33.1，而先 3D 后 2D 或仅 3D 的配置性能均显著下降。这直接证明了 2D 作为中间视觉证据对约束 3D 推断的关键作用。

**3D 框 token 顺序**：中心 → 尺寸 → 旋转的顺序（center → size → rotation）取得最优 33.1，而尺寸 → 中心 → 旋转仅 29.6。这说明按语义从粗到细（先定位中心，再确定尺寸，最后调整朝向）的顺序更符合自回归模型的逐步细化特性。

### 数据效率与训练动态

Figure 4 揭示了 CoS 公式的两个关键优势。左图显示，CoS 模型仅使用 **10%** 训练数据时即达到具有竞争力的性能，而纯 3D 预测模型即使使用 100% 数据（AP3D=22.7）也远低于 CoS（36.1），绝对差距达 **13.4** 点。这说明 CoS 通过引入 2D 中间监督，大幅提升了模型的数据效率——模型不必从零学习从像素到 3D 的极端映射，而是先学习更易掌握的 2D 定位，再在此基础上学习 3D 推断。

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/008_Figure_4.jpg]]
*Figure 4: Data efficiency and training dynamics analysis. (1) The left figure shows data efficiency: We report*

右图展示了训练动态：经过 2D 检测预训练的模型（绿色曲线）几乎立即超越了先前最优水平（虚线），而从头训练（橙色曲线）收敛缓慢且最终精度更低（29.2 vs 36.1）。这进一步印证了 2D 预训练为 3D 学习提供了良好的初始化。

### Token 序列化策略

Table 5 对比了交错式（Interleaved）CoS 与聚类式（Clustered）策略。交错式按“2D₁ 3D₁, 2D₂ 3D₂, ...”输出，聚类式则先输出全部 2D 再输出全部 3D（“2D₁...N → 3D₁...N”）。在遮挡较多的 KITTI 场景中，交错式的 AP3D 为 **22.1**，远高于聚类式的 17.4。这是因为当 2D 和 3D 序列被远距离分离时，模型难以正确关联对应的 2D 框和 3D 框，尤其在多物体密集场景中。交错式通过将每个物体的 2D 和 3D 紧邻放置，避免了这种关联歧义。

### 失败模式分析

Figure 5 展示了典型失败案例，主要归因于训练数据在相机参数、空间布局和纹理细节上的多样性不足。具体表现为：

- **方向误差**：模型预测的物体朝向与真实朝向存在明显偏差，尤其在细长物体上更为突出。
- **框不全**：部分物体未被检测到，或检测到的框未能完整覆盖物体。
- **位置不匹配**：预测的 3D 中心位置偏离实际物体中心，在焦距差异大的场景中尤为明显。
- **深度不匹配**：距离估计误差较大，尤其在纹理稀疏或重复图案区域，模型缺乏可靠的深度推断线索。

这些失败模式揭示了当前方法的核心瓶颈：模型未显式利用深度先验或深度编码器，且假设已知相机内参但未将其作为条件输入。这为未来工作指明了方向——集成显式深度信息、将相机内参作为位置提示注入模型，有望显著提升跨场景鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results of LocateAnything3D. For each example, the left sub-figure overlays the projected 3D bounding boxes on the input image, while the right sub-figure shows the corresponding bird’s-eye view with 1m×1m grids as the background. We use a turbo colormap based on depth, where redish colors indicate objects closer to the camera, and blueish colors indicate objects farther away*

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/010_Table_6.jpg]]
*Table 6: Summary of our extensive and diverse supervised fine-tuning datasets for 2D pretraining. We use a comprehensive collection of numerous large-scale datasets spanning multiple domains and tasks to pretrain our model, ensuring broad coverage and robust performance across diverse visual and language understanding scenarios*

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/011_Figure.jpg]]
*Figure: Orientation Error Under-full Boxes Location Mismatch Depth Mismatch*

![[assets/figures/papers/paper_list_l2400_https_arxiv_org_abs_2511_20648/figures/012_Figure_6.jpg]]
*Figure 6: Visualization of more indoor and outdoor successful cases*

## 方法谱系与知识库定位

### 1. 任务定位与核心瓶颈

LocateAnything3D 瞄准的是**视觉语言模型（VLM）原生的单目多物体3D检测与定位**。现有方法面临三重割裂：

- **架构割裂**：传统检测器（如 **Cube R-CNN**，Brazil et al., CVPR 2023）依赖任务特定的检测头与闭集类别，无法融入VLM的统一token预测范式。
- **模态割裂**：开放词汇方法（如 **OVMono3D**，Yao et al., arXiv 2024）将2D检测与3D提升解耦为两个独立阶段，依赖外部2D检测器提供区域提议，缺乏端到端的联合推理。
- **表示割裂**：可提示方法（如 **DetAny3D**，Zhang et al., ICCV 2025）虽支持开放世界，但直接输出3D框，未利用2D作为中间证据来降低单目3D推断的固有模糊性。

核心瓶颈在于：**单目3D检测是一个病态问题**——从2D投影恢复3D几何存在深度-尺度歧义。纯3D直接预测要求模型隐式学习这种映射，数据效率低且泛化差。

### 2. 方法谱系中的关键创新

LocateAnything3D 的核心贡献是 **Chain-of-Sight（CoS）**——将2D检测作为视觉思维链插入自回归解码过程，形成 `<2D, 3D>` 交错序列。这一设计在谱系中引入了三个关键变化：

**（1）从“外部2D→独立3D”到“交错2D→条件3D”**

| 方法 | 2D来源 | 3D推断方式 | 端到端 |
|------|--------|-----------|--------|
| OVMono3D | 外部检测器 | 独立提升头 | 否 |
| DetAny3D | 外部检测器/Ground-Truth | 直接输出 | 否 |
| **LocateAnything3D** | **自回归解码器自身** | **以2D为条件** | **是** |

CoS的概率分解（式4）将序列概率显式拆分为2D定位和3D估计两个阶段，使3D推断直接以2D框为条件输入。这比独立预测有本质优势：2D框提供了物体的图像平面位置和尺度先验，大幅缩小3D参数的搜索空间。

**（2）物体间排序：近→远课程学习**

现有方法通常按2D扫描线或随机顺序输出物体。LocateAnything3D 采用**从近到远（near-to-far）的深度排序**。消融实验（Table 4）证实：近→远排序的AP3D_out为33.1，显著优于扫描线排序的26.7（+6.4）和随机排序的29.8（+3.3）。其因果机制在于：近处物体成像清晰、视差大，模型更容易学习其3D几何；先解决简单样本再处理远处遮挡物体，形成了自然的课程学习。

**（3）3D框的语义化token分解：中心→尺寸→旋转**

与基于角点（8个顶点）的无序编码不同，CoS采用**中心 t → 尺寸 d → 旋转 R** 的顺序分解。消融显示，这一顺序优于尺寸→中心→旋转（AP3D_out 29.6 vs 33.1）。其合理性在于：中心位置是3D框最关键的参数，先确定“物体在哪里”，再确定“物体多大”和“朝向如何”，符合人类的空间推理习惯，也使自回归模型更容易学习token间的条件依赖。

### 3. 与近邻工作的关系

**Cube-LLM**（Cho et al., CVPR 2024）是VLM原生3D定位的先行者，同样将3D检测转化为语言模型的token预测。但两者存在根本差异：

- **序列设计**：Cube-LLM直接输出3D框，未引入2D中间表示；LocateAnything3D的CoS交错序列提供了显式的2D视觉证据。
- **数据效率**：Cube-LLM_large在约960万张图像上训练，而LocateAnything3D仅在170万张图像上训练（Table 3），却在Objectron上达到AP_3D^cat 72.5 vs 69.8，ARKitScenes上41.7 vs 23.5（+18.2）。**CoS的2D预训练使其在更少数据下获得更强的3D能力**。
- **空间提示利用**：当提供空间位置描述时，Cube-LLM性能反而下降（如Objectron上AP_3D^cat+loc仅45.4 vs 无位置的69.8），而LocateAnything3D能有效利用位置信息（75.0 vs 72.5）。这表明CoS框架对多模态提示的兼容性更好。

**DetAny3D**（Zhang et al., ICCV 2025）在Omni3D基准上曾是SOTA，但需依赖Ground-Truth 2D框才能达到最佳性能（AP3D 34.38）。LocateAnything3D在不使用任何外部2D输入的情况下达到38.90（+4.52），证明了**端到端联合预测2D+3D优于两阶段分离式方案**。

### 4. 适用边界与局限

**已知局限**（论文明确讨论）：

1. **跨相机泛化脆弱**：模型在焦距、空间布局和纹理细节与训练数据差异大的场景中表现下降（Figure 5），可能产生方向错误、位置偏移和深度失准。这是单目3D检测的共性问题——缺乏对相机内参的显式建模。

2. **无纹理区域深度推断不可靠**：对于纹理稀疏或重复图案的区域，模型缺乏可靠的深度线索，距离估计误差较大。CoS虽通过2D框提供了尺度先验，但未从根本上解决单目深度歧义。

3. **单帧限制**：当前方法仅处理单张图像，无法利用多帧/视频的时序信息进行跟踪或多视角一致性约束。

**适用边界推断**（基于方法设计）：

4. **已知相机内参假设**：训练和推理均假设已知相机内参矩阵，但未将其作为条件输入。这限制了在未知相机参数场景（如互联网图片）中的直接应用。

5. **训练数据覆盖范围**：模型的开放词汇能力受限于训练数据的类别和场景多样性。对于训练数据中极少出现或从未出现的物体类别和极端视角，性能可能显著下降。

### 5. 开放问题

1. **深度先验的显式集成**：能否将单目深度估计（如Depth Anything）作为额外输入或预训练任务，为CoS提供更强的深度约束？这有望改善无纹理场景的距离预测精度。

2. **相机内参的条件化**：将相机内参矩阵作为位置编码或条件提示注入模型，是否能提升跨相机泛化能力？这需要设计合适的表示方式，使模型学会“根据内参调整深度预测”。

3. **时序扩展**：CoS框架能否自然扩展到视频输入？多帧间的2D框关联可提供运动视差线索，有望显著改善深度估计和遮挡处理。

4. **极端场景鲁棒性**：针对严重遮挡、极端光照和复杂背景，是否需要专门的训练数据增强策略或模型结构改进（如引入不确定性建模）？

5. **推理效率优化**：CoS序列长度随物体数量线性增长，在密集场景中可能成为延迟瓶颈。能否通过并行解码或非自回归生成来加速推理，同时保持精度？

6. **与其他VLM能力的融合**：当前CoS专注于检测和定位，能否与VLM的场景理解、关系推理和对话能力深度融合，实现“检测-推理-交互”的统一框架？

## 原文 PDF

![[paperPDFs/CVPR_2026/LocateAnything3D_Vision_Language_3D_Detection_with_Chain_of_Sight.pdf]]