---
title: "IVAAN: Instance-level Vision-Language Alignment via Attribute-Guided Text Prompts Generation for Nuclei Analysis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/IVAAN_Instance_level_Vision_Language_Alignment_via_Attribute_Guided_Text_Prompts_Generation_for_Nuclei_Analysis.pdf
project_link: null
code_link: null
aliases:
- IVAAN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入从ground-truth掩膜自动生成的属性引导文本提示，进行实例级对比学习，将形态特征与语义描述对齐；同时设计多原型类令牌和语义交互模块（SIM）捕捉类内差异并双向聚合实例与类级语义。
primary_logic: 通过量化临床相关形态属性并离散化为文本描述，构建实例级视觉-语言对齐，辅以多原型类令牌凝聚类内子分布，双向交互聚合实例与类级语义，消除伪相关偏差，使模型学习更具判别力且跨器官一致的细胞核表征。
claims:
- 在PanNuke上，Ours-H模型在检测F1（0.87）和分类平均F1（0.69）上均达到最佳，优于先前SOTA。
- 实例级分割指标bPQ和mPQ分别达到0.6976和0.5459，显著超越PromptNucSeg（bPQ +0.005, mPQ +0.034）。
- 在MoNuSeg与CPM17数据集上，所提方法在PQ和AJI指标上全面超越先前SOTA。
- 消融实验表明，各新增组件（固定提示、属性提示、熵分箱、SIM、特征融合）逐步将PQ从57.3提升至67.3，验证了每个模块的有效性。
---

# IVAAN: Instance-level Vision-Language Alignment via Attribute-Guided Text Prompts Generation for Nuclei Analysis

> [!tip] 核心洞察
> 通过量化临床相关形态属性并离散化为文本描述，构建实例级视觉-语言对齐，辅以多原型类令牌凝聚类内子分布，双向交互聚合实例与类级语义，消除伪相关偏差，使模型学习更具判别力且跨器官一致的细胞核表征。

| 字段 | 内容 |
|------|------|
| 中文题名 | IVAAN：基于属性引导文本提示的实例级视觉-语言对齐细胞核分析 |
| 英文题名 | IVAAN: Instance-level Vision-Language Alignment via Attribute-Guided Text Prompts Generation for Nuclei Analysis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Jeong_IVAAN_Instance-level_Vision-Language_Alignment_via_Attribute-Guided_Text_Prompts_Generation_for_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | IVAAN |
| Dataset | PanNuke, MoNuSeg, CPM17 |

> [!tip] 效果简介
> - PanNuke 上，Detection F1 0.87 vs 先前SOTA (如CellViT) (最佳)；Classification Avg F1 0.69 vs 先前SOTA (如CellViT) (最佳)；bPQ (binary Panoptic Quality) 0.6976 vs 0.6926 (PromptNucSeg) (+0.005)。
> - MoNuSeg 上，PQ 0.696 vs 先前SOTA (提升)；AJI 0.689 vs 先前SOTA (提升)。
> - CPM17 上，PQ 0.748 vs 先前SOTA (提升)。

## 概要

病理图像中的细胞核分割与分类是癌症诊断和预后评估的基础任务。现有方法通常仅依赖像素级类别标签进行学习，导致模型隐式地将器官来源、染色差异等伪相关特征作为判别依据，难以学习到类别一致且跨领域鲁棒的实例级表征。**IVAAN**（Instance-level Vision-Language Alignment via Attribute-Guided Text Prompts Generation for Nuclei Analysis）针对这一瓶颈，提出了一种实例级视觉-语言对齐框架，通过从真实掩膜自动生成属性引导的文本提示，将细胞核的形态特征与语义描述进行对比学习，同时引入多原型类令牌和语义交互模块（SIM）捕捉类内差异并双向聚合实例与类级语义。

该方法在三个基准数据集上取得了领先性能：在 **PanNuke** 上，检测 F1 达到 **0.87**，分类平均 F1 达到 **0.69**，均优于先前最优方法；实例级分割指标 bPQ 达到 **0.6976**，mPQ 达到 **0.5459**，较 PromptNucSeg 分别提升 +0.005 和 +0.034。在 **MoNuSeg** 和 **CPM17** 上，PQ 和 AJI 指标也全面超越此前 SOTA。消融实验进一步验证了属性提示、熵分箱、语义交互模块和特征融合等各组件的独立贡献，PQ 从基线的 57.3 逐步提升至 67.3。

**方法定位**：IVAAN 属于实例级视觉-语言对齐的核分割与分类方法，其核心创新在于利用临床相关形态属性的量化与离散化自动生成文本监督信号，无需人工标注。与仅使用图像级或区域级文本提示的病理视觉-语言模型（如 MI-Zero、CONCH、PLIP、Quilt-Net）不同，IVAAN 在实例粒度上进行对齐；与依赖空间提示的 **PromptNucSeg**（Shui et al., ECCV 2024）相比，IVAAN 引入了语义层面的形态描述，并通过多原型类令牌和双向交叉注意力机制显式建模类内多样性，从而更有效地消除器官偏置等伪相关影响。

### 病理细胞核分析：从视觉监督到语义对齐

细胞核的精确分割与分类是计算病理学中的核心任务，是癌症分级、预后评估等下游分析的基础。当前主流方法——包括 **Mask R-CNN**（He et al., ICCV 2017）、**HoVer-Net**（Graham et al., Medical Image Analysis 2019）、**DIST**（Naylor et al., IEEE TMI 2018）、**PointNu-Net**（Yao et al., IEEE TETCI 2023）以及 **CellViT**（Horst et al., Medical Image Analysis 2024）——均采用纯视觉监督范式，即模型仅依赖像素级类别标签学习核形态特征。这种范式存在一个深层缺陷：模型隐式地从数据中学习形态-类别关联，极易捕获器官来源、染色批次等伪相关（spurious correlations），而非细胞核本身的固有形态学特征。

具体而言，如图 5 所示，来自同一器官的同类细胞核在特征空间中往往紧密聚集，而跨器官的同类细胞核则分布更为发散。这意味着，模型可能通过“器官上下文”而非“细胞形态”来区分核类别——例如，在结肠组织中倾向于将细长核预测为成纤维细胞，而在肺组织中却因染色差异将同一形态的核误判为炎症细胞。这种器官偏置（organ bias）严重削弱了模型的跨领域泛化能力，是当前核分析方法在未见脏器或新染色协议上性能骤降的根本原因。

### 现有视觉-语言方法的局限

近期，视觉-语言模型（VLM）在自然图像理解中展现出强大的开放词汇识别能力，病理学领域也开始尝试引入文本监督。然而，现有病理 VLM 方法存在明显局限：它们仅在图像级或区域级使用文本提示（如整张切片的诊断报告或粗粒度区域描述），无法为单个细胞核实例提供精细的形态语义锚定。这种粗粒度的对齐方式无法解决上述实例级的伪相关偏差问题，对于需要精确区分易混淆类别（如结缔组织细胞与炎症细胞、死细胞与凋亡细胞）的核分析任务帮助有限。

### 本文动机：实例级视觉-语言对齐

针对上述瓶颈，本文提出核心理念：**将病理学家常用的形态属性（如细胞核大小、形状、染色强度、边界不规则性）量化为可读的文本描述，并在实例级别实现视觉特征与语义描述的对齐**。这一思路的直觉在于：通过强制模型将每个细胞核的视觉表征与其形态属性的语言描述绑定，模型被迫关注核本身的形态学特征，而非器官或染色等伪相关信息，从而学习到类别一致且跨领域鲁棒的实例级表征。

为实现这一目标，需要解决三个关键技术挑战：
1. **如何自动生成实例级的属性文本提示？** 需要从 ground-truth 掩膜中提取临床相关形态特征，并将其离散化为语义有意义的文本描述。
2. **如何有效对齐实例视觉特征与文本语义？** 需要设计对比学习机制，使同一实例的视觉嵌入与其对应的文本嵌入在联合空间中靠近。
3. **如何捕捉类内多样性并聚合实例级语义？** 同类细胞核在不同器官中形态差异显著，单一类别原型无法覆盖类内子分布，需要多原型表示与双向语义交互机制。

## 核心方法与创新机理

IVAAN的核心创新在于将核分割与分类问题从纯视觉空间拓展到**实例级视觉-语言联合空间**，通过三个关键机制消除病理图像中普遍存在的器官偏置与染色伪相关。

### 1. 属性引导的实例级文本提示生成

现有病理视觉-语言模型仅使用图像级或区域级文本提示（Figure 1），无法为单个细胞核提供精细的语义监督。IVAAN首次实现了**从ground-truth掩膜自动生成实例级文本提示**：从掩膜中量化病理医生常用的形态属性（如大小、形状、染色强度、边界不规则性），并通过**基于信息熵的有监督离散化**将这些连续测量值转换为语义可读的文本描述符（如"large, elongated, hyperchromatic nucleus"）。

与等频分箱相比，熵分箱的关键优势在于最大化类别信息增益——离散化阈值由公式 $\mathrm{Gain}(\theta) = H_{\mathrm{total}} - \frac{n_L}{n} H_L - \frac{n_R}{n} H_R$ 驱动，递归分裂至最大深度4层，产生最多5个属性区间。消融实验直接验证了这一设计的必要性：等频分箱仅达PQ 62.0，而熵分箱将其提升至64.0。

### 2. 双层级视觉-语言对比学习

IVAAN设计了两层互补的对比损失：

- **固定提示对比损失**（$\mathcal{L}_{\mathrm{fix}}$）：对齐实例视觉嵌入与类别固定文本提示嵌入，提供全局语义锚定。
- **属性提示对比损失**（$\mathcal{L}_{\mathrm{attr}}$）：对齐实例视觉嵌入与对应属性文本提示嵌入，捕捉细粒度形态差异。

两者的协同作用构成核心性能增益来源——固定提示编码细胞类型与器官上下文，属性提示提供形态细节，共同消除伪相关偏差。总视觉-语言损失为 $\mathcal{L}_{\mathrm{CL}} = \lambda_{fix}\mathcal{L}_{fix} + \lambda_{attr}\mathcal{L}_{attr}$。

### 3. 多原型类令牌与语义交互模块（SIM）

针对同类细胞核跨器官的显著类内差异（Figure 5），IVAAN引入**每类k个可学习类令牌**作为局部原型，替代传统的单一类别嵌入。这些类令牌通过**语义交互模块（SIM）**与对象查询进行双向交叉注意力：

- **OQ→CT**：聚合实例证据，形成动态类原型。
- **CT→OQ**：将类别上下文回传至实例表示。

配合**类令牌中心损失**（$\mathcal{L}_{\mathrm{cent}}$）约束每组类令牌均值靠近对应类别文本嵌入，该机制使模型能够捕获类内子分布，降低器官偏置影响。消融实验表明，加入SIM后PQ从64.0跃升至66.5（+2.5），是单组件最大增益。

### 4. 跨模态特征融合

在视觉编码器与Transformer解码器之间，IVAAN通过交叉注意力将文本嵌入与视觉特征融合，**缩小模态鸿沟并提供早期语义引导**。这一设计使最终PQ进一步提升至67.3，验证了在特征层面注入语言先验的有效性。

### 创新总结

| 变更槽位 | 基线方案 | IVAAN方案 | 增益（PQ） |
|---------|---------|----------|-----------|
| 实例级VL对齐 | 无（仅视觉监督） | 固定提示+属性提示联合对比 | +6.7（57.3→64.0） |
| 属性离散化 | 无/等频分箱 | 熵分箱 | +2.0（62.0→64.0） |
| 类原型表示 | 单一类别嵌入 | 多原型类令牌（k个） | +2.5（64.0→66.5） |
| 语义交互 | 无双向聚合 | SIM双向交叉注意力 | 包含于上述 |
| 特征融合 | 仅视觉特征 | 视觉+文本跨模态融合 | +0.8（66.5→67.3） |

这些创新使IVAAN在PanNuke上以bPQ 0.6976、mPQ 0.5459全面超越先前SOTA（如**PromptNucSeg**，Shui et al., ECCV 2024），并在MoNuSeg与CPM17上取得一致的跨数据集泛化优势。

IVAAN 的整体框架围绕“实例级视觉-语言对齐”这一核心机制构建，旨在为细胞核分割与分类任务提供更具判别力且跨领域鲁棒的表征。其 pipeline 由五个关键模块串联而成，形成从属性自动提取到语义交互增强的完整闭环，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2319_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_IVAAN_Instance_l/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed framework. The last layers of the text and image encoders are unfrozen for joint optimization*

**输入与特征提取。** 系统接受病理图像作为输入，经图像编码器（基于 Mask2Former backbone）提取多尺度视觉特征；同时，文本编码器（CLIP text encoder，末层可训练）接收两类文本提示——固定类别提示与属性引导提示——生成对应的文本嵌入。两类编码器的末层在训练中解冻，以进行联合优化。

**属性提示的自动生成。** 在训练阶段，框架从 ground-truth 掩膜中自动提取病理医生常用的形态学属性（如大小、形状、染色强度、边界不规则性等），并通过基于信息熵的有监督离散化过程将这些连续量转换为语义可读的文本描述。这一步骤无需人工标注，为每个细胞核实例生成细粒度的属性提示。

**特征融合。** 视觉特征与文本嵌入通过跨模态特征融合模块进行早期交互，以缩小模态间隙并为视觉表征提供先行的语义引导。

**实例级视觉-语言对齐。** 增强后的对象查询特征与对应的文本嵌入之间施加双重对比学习损失：固定提示对比损失 $L_{\mathrm{fix}}$ 将实例视觉嵌入对齐到其类别级固定文本锚点，属性提示对比损失 $\mathcal{L}_{\mathrm{attr}}$ 进一步在细粒度形态属性层面进行对齐。两者加权组合构成总视觉-语言损失 $\mathcal{L}_{\mathrm{CL}}$，使模型同时捕获类别语义和实例级形态差异。

**多原型类令牌与语义交互模块（SIM）。** 为建模类内多样性，框架为每个前景类引入 $k$ 个可学习的类令牌作为局部原型。这些类令牌通过语义交互模块与对象查询特征进行双向交叉注意力：对象查询向类令牌聚合实例证据，形成动态类原型；类令牌向对象查询回传全局类别语义。同时，类令牌中心损失 $\mathcal{L}_{\mathrm{cent}}$ 约束每类令牌的均值靠近其对应的文本嵌入，提供语义锚定。

**输出。** 最终，经过语义交互增强的查询特征送入掩膜解码器与分类头，同步预测实例分割掩膜和类别标签。总损失函数为分割损失、分类损失、对比学习损失与中心损失的加权组合：

$$\mathcal{L} = \lambda_{\mathrm{seg}} \mathcal{L}_{\mathrm{seg}} + \lambda_{\mathrm{cls}} \mathcal{L}_{\mathrm{cls}} + \lambda_{\mathrm{CL}} \mathcal{L}_{\mathrm{CL}} + \lambda_{\mathrm{cent}} \mathcal{L}_{\mathrm{cent}}$$

整体而言，IVAAN 通过“属性量化→文本生成→跨模态融合→实例级对齐→多原型语义交互”的递进式设计，将形态学先验系统地注入视觉表征学习，从而消解器官偏置与染色差异等伪相关对细胞核分析的干扰。

IVAAN的核心创新在于将**实例级视觉-语言对齐**引入细胞核分割与分类框架，其关键模块包括：属性引导文本提示生成、多原型类令牌与语义交互模块（SIM）、以及跨模态特征融合。以下逐一展开其设计逻辑与数学形式。

### 属性引导文本提示生成

病理学家在判读细胞核时，不仅依赖类别标签，更依赖一系列可量化的形态属性（如大小、形状、染色强度、边界不规则性）。IVAAN从ground-truth掩膜中自动提取这些属性，并将其离散化为可读的文本描述，从而为每个实例生成语义锚点。

**属性选择与可分性度量**：首先计算11个候选形态属性（如面积、周长、偏心率、H&E通道均值与标准差等），并通过Cohen's d效应量的中位数来评估每个属性对类别区分的贡献。给定属性 $m$ 在类别 $c_i$ 与 $c_j$ 之间的效应量 $d_{ij}$，其可分性得分为：

$$S(m) = \mathrm{median}\big( |d_{ij}| \big)$$

选择得分最高的属性进入后续离散化流程。

**基于信息熵的有监督离散化**：与等频分箱（quantile binning）不同，IVAAN采用递归信息增益最大化策略寻找最优分割阈值。对于属性值域上的候选阈值 $\theta$，其信息增益定义为：

$$\mathrm{Gain}(\theta) = H_{\mathrm{total}} - \frac{n_L}{n} H_L - \frac{n_R}{n} H_R$$

其中 $H_{\mathrm{total}}$ 为整个区间的类别分布熵，$H_L$ 和 $H_R$ 分别为左右子区间的熵，$n_L$、$n_R$ 为对应样本数。熵的计算形式为：

$$H = -\sum_{c} p(c) \log_2 p(c)$$

该过程递归进行，最大深度为4，最多产生5个属性区间。为增强鲁棒性，对训练集进行多次子采样迭代，保留在至少60%迭代中出现的阈值，通过聚类得到最终分割边界。每个区间被映射为自然语言描述（如“面积较大，形状不规则”），构成**属性引导文本提示**。

### 实例级视觉-语言对齐

训练阶段，每个细胞核实例对应两类文本提示：**固定类别提示**（如“a neoplastic nucleus in breast tissue”）和上述**属性提示**。两类提示经CLIP文本编码器（末层可训练）编码为嵌入 $T_c$ 和 $t_{i,a}^m$，与视觉编码器输出的实例查询特征 $v_i$ 进行对比学习。

**固定提示对比损失**：将实例视觉嵌入拉向其真实类别对应的固定文本嵌入，推开其他类别嵌入：

$$\mathcal{L}_{\mathrm{fix}} = -\frac{1}{N}\sum_i \log \frac{\exp(v_i^{\top} T_{y_i}/\tau)}{\sum_j \exp(v_i^{\top} T_j/\tau)}$$

其中 $T_{y_i}$ 为实例 $i$ 真实类别 $y_i$ 的固定提示嵌入，$\tau$ 为温度系数。

**属性提示对比损失**：对每个属性 $a$，将实例视觉嵌入与对应属性区间的文本嵌入对齐：

$$\mathcal{L}_{\mathrm{attr}}^a = -\frac{1}{N_a}\sum_i \log \frac{\exp(v_i^{\top} t_{i,a}^+/\tau_{\mathrm{attr}})}{\sum_m \exp(v_i^{\top} t_{i,a}^m/\tau_{\mathrm{attr}})}$$

其中 $t_{i,a}^+$ 为实例 $i$ 在属性 $a$ 上所属区间的文本嵌入，分母遍历该属性的所有区间嵌入。

**总视觉-语言损失**为两者的加权和：

$$\mathcal{L}_{\mathrm{CL}} = \lambda_{\mathrm{fix}}\mathcal{L}_{\mathrm{fix}} + \lambda_{\mathrm{attr}}\mathcal{L}_{\mathrm{attr}}$$

### 多原型类令牌与语义交互模块（SIM）

为捕捉类内形态差异（如同一类别在不同器官中的表现差异），IVAAN为每类引入 $k$ 个可学习的**类令牌**（class tokens），共计 $(C+1) \times k$ 个（含背景类）。这些令牌作为局部原型，通过语义交互模块与实例查询特征进行双向交叉注意力：

- **OQ → CT（对象查询到类令牌）**：将实例证据聚合到类令牌，形成动态的、依赖当前图像的类原型。
- **CT → OQ（类令牌到对象查询）**：将聚合后的类别语义回传至实例表示，增强其判别力。

该设计使得类令牌既能凝聚类内子分布，又能为每个实例注入全局上下文，从而缓解器官偏置等伪相关的影响。

**类令牌中心损失**：为确保类令牌的语义一致性，约束每类 $k$ 个令牌的均值 $\bar{q}_c$ 靠近对应固定文本嵌入 $T_c$：

$$\mathcal{L}_{\mathrm{cent}} = -\frac{1}{C}\sum_{c=1}^C \log \frac{\exp(\bar{q}_c^{\top} T_c/\tau_{\mathrm{CT}})}{\sum_{j=1}^C \exp(\bar{q}_c^{\top} T_j/\tau_{\mathrm{CT}})}$$

### 跨模态特征融合

在视觉编码器输出与Transformer解码器之间，IVAAN插入特征融合模块，将文本嵌入与多尺度视觉特征通过交叉注意力进行融合，以缩小模态鸿沟并提供早期语义引导。该模块使视觉表征在进入实例解码前即获得语言先验，进一步提升对齐效果。

### 总损失函数

最终训练目标为分割损失 $\mathcal{L}_{\mathrm{seg}}$、分类损失 $\mathcal{L}_{\mathrm{cls}}$、视觉-语言对比损失 $\mathcal{L}_{\mathrm{CL}}$ 与类令牌中心损失 $\mathcal{L}_{\mathrm{cent}}$ 的加权组合：

$$\mathcal{L} = \lambda_{\mathrm{seg}} \mathcal{L}_{\mathrm{seg}} + \lambda_{\mathrm{cls}} \mathcal{L}_{\mathrm{cls}} + \lambda_{\mathrm{CL}} \mathcal{L}_{\mathrm{CL}} + \lambda_{\mathrm{cent}} \mathcal{L}_{\mathrm{cent}}$$

其中各 $\lambda$ 为平衡超参数。该多目标联合优化使得模型同时学习精确的像素级分割、类别判别以及形态感知的实例级语义对齐。

![[assets/figures/papers/paper_list_l2319_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_IVAAN_Instance_l/figures/004_Figure_4.jpg]]
*Figure 4: Violin distributions for eleven representative attributes. A red dotted box indicates the selected attributes. A black dotted lines in the graphs marks the partition boundary. To ensure a clear visualization, we removed statistical outliers using Tukey’s fences [37]*

## 实验与关键发现

### 主实验结果

IVAAN在PanNuke数据集上进行了全面的检测、分类与实例级分割评估。在检测与分类任务上，Ours-H模型取得了检测F1 0.87和分类平均F1 0.69的最佳结果，优于**CellViT**（Horst et al., Medical Image Analysis 2024）等先前方法（Table 1）。在实例级分割任务上，所提方法达到二值全景质量bPQ 0.6976和多类全景质量mPQ 0.5459，相较于**PromptNucSeg**（Shui et al., ECCV 2024）分别提升+0.005和+0.034个点（Table 2）。其中mPQ的大幅提升（+0.034）表明引入实例级视觉-语言对齐对跨类别的分割与分类一致性有显著增益。

![[assets/figures/papers/paper_list_l2319_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_IVAAN_Instance_l/figures/007_Table_2.jpg]]
*Table 2: Performance comparison on the PanNuke dataset. Following [12, 34], both binary panoptic quality (bPQ) and multi-class panoptic quality (mPQ) across 19 organs are reported. The best and second-best scores in each row are shown in bold and underlined, respectively. Standard deviations are computed over three-fold experiments following [9]*

在跨数据集泛化方面，IVAAN在MoNuSeg和CPM17数据集上同样取得领先结果：MoNuSeg上PQ 0.696、AJI 0.689，CPM17上PQ 0.748、AJI 0.743，全面超越先前SOTA（Table 5）。

![[assets/figures/papers/paper_list_l2319_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_IVAAN_Instance_l/figures/009_Table_5.jpg]]
*Table 5: Performance comparison on the MoNuSeg and CPM17 datasets. The best results are highlighted in bold, and the previous state-of-the-art scores are underlined*

从各类别细分结果看（Table 3），所提方法在死细胞（Dead）等少数类上的PQ改善尤为突出。这归因于属性提示显式编码了死细胞特有的形态特征（如核固缩、碎片化边界），使模型不再仅依赖类别标签隐式学习，从而缓解了类别不平衡带来的表征退化。

### 消融实验

消融实验以PQ为指标，在PanNuke上逐步验证各组件的贡献（Table 4）：

![[assets/figures/papers/paper_list_l2319_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_IVAAN_Instance_l/figures/010_Table_4.jpg]]
*Table 4: Ablation study of key components in the proposed framework. Attr: attribute prompts; Entr: entropy-based binning; FF: feature fusion. Row 3 denotes attribute prompts from quantile (equal-count) bins rather than entropy-optimized bins*

1. **基线**：仅使用视觉监督的Mask2Former架构，PQ为57.3。
2. **加入固定提示**（Fixed prompts）：引入类别级固定文本提示的对比学习，PQ提升至61.2（+3.9）。固定提示作为全局语义锚点，编码了核类别与器官上下文信息。
3. **等频分箱属性提示**：进一步加入基于等频分箱的属性提示，PQ仅提升至62.0（+0.8）。等频分箱未考虑类别区分性，属性区间划分缺乏语义判别力。
4. **熵分箱属性提示**：将离散化策略替换为基于信息增益的熵分箱，PQ跃升至64.0（+2.0）。这表明类别感知的离散化阈值能提取更具判别力的形态描述，为对比学习提供更精细的监督信号。
5. **语义交互模块（SIM）**：引入多原型类令牌与双向交叉注意力后，PQ提升至66.5（+2.5）。SIM通过OQ→CT聚合实例证据形成动态类原型，再通过CT→OQ回传类别语义，有效捕获了类内子分布差异。
6. **特征融合（FF）**：最终加入视觉特征与文本嵌入的跨模态融合，PQ达到67.3（+0.8），实现最佳性能。FF在早期阶段缩小模态鸿沟，为视觉表征提供语义引导。

消融实验揭示了各模块的因果贡献链：属性提示的质量（熵分箱 vs. 等频分箱）是性能瓶颈之一；SIM带来的+2.5增益最大，验证了双向语义交互对捕获类内多样性的关键作用。

### 可视化分析

特征空间可视化（Figure 6）对比了有无视觉-语言对齐与SIM的两种情况。加入对齐后，炎症细胞（inflammatory）与结缔组织细胞（connective）类别在UMAP和t-SNE空间中变得可区分，死细胞（dead）也形成了更清晰的分离簇。文本锚点（text anchors）与类令牌（cluster tokens）在特征空间中紧密耦合，验证了对比损失与中心损失的有效性。

![[assets/figures/papers/paper_list_l2319_https_openaccess_thecvf_com_content_CVPR2026_html_Jeong_IVAAN_Instance_l/figures/011_Figure_6.jpg]]
*Figure 6: UMAP (left) and t-SNE (right) comparison between w/ and w/o VL alignment and SIM. The green and red boxes highlight whether inflammatory and connective categories are distinguishable and whether dead cells are clearly separated. The colored squares and circles with white edge marks the text anchors and the cluster tokens, respectively*

### 失败模式与局限

尽管IVAAN在多项指标上取得领先，分析中仍识别出以下不足：

1. **属性覆盖范围有限**：属性选择依赖预定义的形态指标（如面积、偏心率、染色强度等），可能遗漏部分临床相关特征。对于形态特征不明显的类别，属性提示的判别力下降。
2. **离散化阈值泛化性**：熵分箱阈值基于训练集统计量确定，当目标域数据分布偏移较大时（如不同染色协议、扫描仪），预定义区间可能次优，需要手动校准或自适应调整。
3. **少数类的类令牌配置**：类令牌数量k为全局固定值，少数类（如死细胞）样本量不足，可能导致对应类令牌欠拟合或陷入局部最优，限制尾部类别表征质量。
4. **易混淆类别分离不足**：对于高度重叠的类别（如结缔组织细胞与炎症细胞），现有对比损失和中心损失提供的分离约束可能不足。Table 3中这两类的PQ相对较低，提示需要额外的类别间分离机制。

### 公平性说明

所提方法无需人工文本标注，属性提示完全从ground-truth掩膜自动生成，避免了人工标注成本与主观偏差。在PanNuke的19种器官、多种染色条件下验证，跨数据集（MoNuSeg、CPM17）泛化性强。多原型类令牌设计使模型能够捕获类内多样性，降低了器官偏置对分类决策的干扰。

## 定位与知识库关联

### 核分割与分类的方法演进

IVAAN 的核心任务——病理图像中细胞核的实例级分割与分类——是一个长期存在的密集预测问题。早期工作主要依赖纯视觉监督，代表性方法包括：

- **Mask R-CNN** (He et al., ICCV 2017)：通用实例分割基线，通过区域提议网络和检测头联合预测掩膜与类别，但缺乏对核形态先验的显式建模。
- **HoVer-Net** (Graham et al., Medical Image Analysis 2019)：核分割与分类的经典方法，利用水平和垂直距离图分离相邻核，并引入双分支解码器同时处理分割与分类，在PanNuke等数据集上长期占据领先地位。
- **DIST** (Naylor et al., IEEE TMI 2018)：将核分割转化为距离图回归问题，通过预测核中心距离图实现实例分离，避免显式边界检测。
- **PointNu-Net** (Yao et al., IEEE TETCI 2023)：引入关键点辅助机制，将核中心检测与分割解耦，提升密集场景下的实例区分能力。
- **CellViT** (Horst et al., Medical Image Analysis 2024)：将视觉Transformer引入核分割，利用自注意力捕获全局上下文，在PanNuke上取得了此前最优的分类F1分数。
- **CPP-Net** (Chen et al., IEEE TIP 2023)：通过轮廓感知模块增强核边界预测精度，改善分割掩膜的边缘质量。
- **PromptNucSeg** (Shui et al., ECCV 2024)：首次将空间提示引入核分割，利用点或框等空间先验引导模型关注目标区域，在PanNuke的bPQ指标上达到0.6926，是IVAAN的直接对比对象。

上述方法的共同局限在于：它们仅依赖类别标签进行隐式形态学习，模型容易受到器官偏置、染色差异等伪相关因素的干扰，难以学习到类别一致且跨领域鲁棒的实例级表征。这正是IVAAN试图通过引入视觉-语言对齐来解决的核心瓶颈。

### IVAAN 的方法定位与创新维度

IVAAN 在以下五个维度上对现有范式进行了系统性改造，形成了从“纯视觉监督”到“实例级视觉-语言对齐”的范式跃迁：

| 设计维度 | 基线方法 | IVAAN 方案 | 机制作用 |
|:---|:---|:---|:---|
| 监督信号 | 仅视觉监督（类别标签） | 固定类别提示 + 属性提示联合对比学习 | 引入语义锚定，消除伪相关偏差 |
| 属性离散化 | 无 / 等频分箱 | 基于信息熵的有监督离散化分箱 | 最大化类别区分信息，生成更具判别力的文本描述 |
| 类原型表示 | 单一类别嵌入或单原型 | 每类多个可学习类令牌原型（k个） | 捕获类内子分布，降低器官偏置影响 |
| 语义交互 | 无双向聚合 | 语义交互模块（SIM）双向交叉注意力 | 聚合实例证据形成动态类原型，回传类别语义 |
| 特征融合 | 仅视觉特征输入Transformer | 视觉特征与文本嵌入跨模态融合 | 缩小模态鸿沟，提供早期语义引导 |

这些维度的改变并非孤立叠加，而是形成了因果链条：属性离散化（→高质量文本描述）→ 实例级对比学习（→形态-语义对齐）→ 多原型类令牌 + SIM（→类内多样性建模与双向语义聚合）→ 特征融合（→早期跨模态整合）。消融实验（Table 4）验证了这一链条的有效性：从基线PQ 57.3开始，依次加入固定提示（+3.9）、属性提示（+2.8）、熵分箱替代等频分箱（+2.0）、SIM（+2.5）、特征融合（+0.8），最终达到PQ 67.3，每一步均带来显著增益。

### 适用边界与技术局限

尽管IVAAN在多个数据集上取得了SOTA性能，其方法设计仍存在以下适用边界：

1. **属性选择依赖预定义形态指标**：当前属性集（如大小、形状、染色强度、边界不规则性）虽覆盖了病理学家常用特征，但可能遗漏部分临床相关属性。对于需要特殊形态学知识（如核内包涵体、染色质纹理）的细分任务，需要领域专家重新设计属性提取流程。

2. **离散化阈值的域迁移敏感性**：信息熵分箱的阈值基于训练集类别分布优化，当目标域数据分布（如不同扫描仪、染色协议）与训练集差异较大时，预定义的分区边界可能次优。虽然方法在MoNuSeg和CPM17上展现了跨数据集泛化能力，但在更大规模的域偏移场景下仍需验证。

3. **类令牌数量的全局固定**：每类类令牌数量k为全局超参数，无法自适应不同类别的样本量。对于死细胞等少数类，固定数量的类令牌可能因样本不足而欠拟合或陷入局部最优；而对于上皮细胞等多数类，k可能不足以覆盖全部子分布。如何为尾部类别自适应分配令牌预算，是方法扩展的重要方向。

4. **易混淆类别的分离不足**：对于结缔组织细胞与炎症细胞等形态高度重叠的类别，现有的对比损失和类令牌中心损失可能不足以提供充分的分离约束。特征空间可视化（Figure 6）显示，即使加入VL对齐和SIM，这两类在UMAP投影中仍存在部分重叠，提示需要引入额外的类别间排斥机制。

### 开放问题与后续方向

基于IVAAN的方法框架和上述局限，以下几个开放问题值得后续工作探索：

- **自适应类令牌分配**：能否根据各类别的样本量或类内方差动态调整类令牌数量？引入基于样本统计量的令牌预算分配策略，或对少数类施加更强的正则化，可能进一步提升尾部类别的表征质量。

- **类别间分离增强**：对于结缔组织与炎症细胞等重叠类别，可否引入适度的多样化约束（如类间距离最大化正则项）或难例挖掘策略，增强特征空间的类别可分性？

- **属性引导范式的任务迁移**：属性引导文本提示的生成框架是否可推广到其他密集预测任务（如腺体分割、组织区域分类）？这需要评估目标任务的形态属性是否可被量化并离散化为有判别力的文本描述，而不引入过多领域知识需求。

- **自监督实例级VL对齐**：在大规模未标注病理数据上，能否通过自监督方式（如基于形态聚类的伪标签生成）实现实例级视觉-语言对齐？这将消除对ground-truth掩膜的依赖，使方法可扩展到更大规模的真实世界数据。

## 原文 PDF

![[paperPDFs/CVPR_2026/IVAAN_Instance_level_Vision_Language_Alignment_via_Attribute_Guided_Text_Prompts_Generation_for_Nuclei_Analysis.pdf]]
