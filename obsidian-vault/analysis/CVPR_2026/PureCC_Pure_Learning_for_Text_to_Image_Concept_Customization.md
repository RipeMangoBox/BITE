---
title: "PureCC: Pure Learning for Text-to-Image Concept Customization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PureCC_Pure_Learning_for_Text_to_Image_Concept_Customization.pdf
project_link: null
code_link: "https://github.com/lzc-sg/PureCC"
aliases:
- PureCC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将概念学习目标解耦为原始模型预测与目标概念隐式指导的组合，并引入双分支架构和自适应指导强度 λ⋆ 平衡保真度与模型保持。
primary_logic: 将概念定制视为在原始条件预测之上叠加目标概念的隐式指导，从而在保持原始模型行为与生成能力的同时纯粹地学习个性化概念。
claims:
- 现有方法（DreamBooth、LoRA 等）在概念定制后，CLIP-T 和 HPSv2.1 得分明显下降，表明原始能力受损。
- 现有方法导致原始分布偏移（KL Divergence 增大）。
- PureCC 提出的解耦学习目标与双分支训练有效保持原始模型行为，Seg-Cons 指标 69.37 远超所有基线。
- PureCC 在保持原始模型的同时，达到最优的目标概念保真度（CLIP-I 0.81，DINO 0.73）。
---

# PureCC: Pure Learning for Text-to-Image Concept Customization

> [!tip] 核心洞察
> 将概念定制视为在原始条件预测之上叠加目标概念的隐式指导，从而在保持原始模型行为与生成能力的同时纯粹地学习个性化概念。

| 字段 | 内容 |
|------|------|
| 中文题名 | 纯学习驱动的文本到图像概念定制 |
| 英文题名 | PureCC: Pure Learning for Text-to-Image Concept Customization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.07561) · [Code](https://github.com/lzc-sg/PureCC) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PureCC |
| Dataset | DreamBenchPCC |

> [!tip] 效果简介
> - DreamBenchPCC 上，ΔCLIP-T(base) for instance concepts -0.31 vs CIFC: -1.93, DreamBooth: -4.81 (closer to 0 indicates better preservation of text alignment)；Seg-Cons 69.37 vs DreamBooth+EWC: 26.37, CIFC: 13.23 (higher indicates better behavior preservation (spatial consistency))；CLIP-I (target) 0.81 vs CIFC: 0.78, DreamO: 0.71, DreamBooth: 0.63 (higher indicates better instance-level concept fidelity)。

## 概要

文本到图像的概念定制（concept customization）旨在让预训练生成模型学会用户提供的特定视觉概念（如某个物体实例或艺术风格），并在新场景中忠实地复现该概念。现有方法（如 **DreamBooth**（Ruiz et al., CVPR 2023）、LoRA、Mix-of-Show、CIFC 等）通常将完整的语言-视觉知识作为微调目标，但由于参考图像数量极为有限，模型难以区分目标概念与冗余信息，导致插入新概念后原始模型的**行为**（非目标区域变化）和**能力**（提示遵循度、生成质量）显著下降——实验证据表明，这些方法在定制后 CLIP-T 和 HPSv2.1 得分明显下滑，且原始分布发生偏移（KL 散度增大）。

**PureCC** 针对上述瓶颈提出了一种纯学习（pure learning）范式。其核心洞察在于：将概念定制重新表述为在原始条件预测之上叠加目标概念的隐式指导，从而在保持原始模型行为与生成能力的同时纯粹地学习个性化概念。具体而言，该方法将学习目标解耦为原始模型预测与目标概念隐式指导的组合，并引入双分支架构——冻结的表示提取器提供目标概念引导，可训练流模型提供原始条件预测——配合自适应引导强度 $\lambda^\star$ 动态平衡概念保真度与模型保持。

在统一构建的 DreamBenchPCC 基准上，PureCC 取得了最优的目标概念保真度（CLIP-I 0.81，DINO 0.73），同时在原始模型保持指标上远超所有基线：Seg-Cons 达 69.37（次优 DreamBooth+EWC 仅 26.37），$\Delta$CLIP-T 仅为 -0.31（CIFC 为 -1.93，DreamBooth 为 -4.81），$\Delta$HPSv2.1 甚至正向提升 +0.10。消融实验证实了纯学习损失、分阶段训练策略和自适应 $\lambda^\star$ 的关键作用。该方法的主要代价是训练阶段增加了约 30% 的时间与显存开销，但推理时无额外负担。

### 文本到图像概念定制的核心挑战

文本到图像扩散模型（如 Stable Diffusion 3.5 Medium）已展现出强大的通用生成能力，但用户往往希望将特定的个性化概念（如自家宠物、特定艺术品风格）注入模型，使其能够在新场景中一致地复现该概念。这一任务被称为**概念定制**（Concept Customization），其核心挑战在于：模型仅能从极少量参考图像（通常 3–5 张）中学习目标概念，却需要在推理时同时满足两个看似矛盾的需求——**概念保真度**（生成的实例或风格与参考图像高度一致）与**模型保持**（不破坏原始模型对非目标区域的生成行为、提示遵循能力和图像质量）。

### 现有方法的根本瓶颈：分布偏移与能力退化

当前主流的概念定制方法（如 **DreamBooth**（Ruiz et al., CVPR 2023）、LoRA、Mix-of-Show、CIFC 等）均采用**全量语言-视觉知识作为学习源**的微调策略：它们将完整文本条件 $y_{complete}$（包含目标概念标识符的提示）送入预训练模型，通过最小化条件流匹配损失 $\mathcal{L}_{CC}$ 来对齐目标分布。然而，这一范式存在一个被长期忽视的结构性缺陷：

> **有限参考图像使模型难以区分目标概念与冗余信息，导致插入新概念后原始模型的行为和能力显著下降。**

具体而言，当模型仅凭少量样本去拟合包含完整语义的文本条件时，它不可避免地会将参考图像中的背景、光照、构图等**非目标信息**也编码进参数更新中。这造成了两个层面的破坏：

1. **原始分布偏移**：如 Figure 2 所示，现有方法将预训练模型强行拉向目标分布，导致 KL 散度显著增大。这意味着模型丧失了原有的生成多样性，在生成与目标概念无关的内容时也会出现偏差。

2. **提示遵循度与生成质量退化**：Figure 1(c) 的下降曲线直接量化了这一退化——DreamBooth 和 LoRA 等方法在概念定制后，CLIP-T（文本-图像对齐度）和 HPSv2.1（人类偏好评分）均明显下滑。例如，DreamBooth 在实例概念定制后 ΔCLIP-T 达到 -4.81，ΔHPSv2.1 为 -2.17（Table 1），表明模型连基本的提示遵循能力都遭到了严重损害。

Figure 1(b) 给出了一个直观的定性证据：当提示为“placed on a bright window”时，DreamBooth 和 LoRA 生成的图像完全丢失了“明亮的窗台”这一场景元素，而 PureCC 则忠实地保留了该非目标区域的原始模型行为。

### 关键洞察：概念定制应是对原始预测的叠加而非替代

PureCC 的核心洞察源于对 Classifier-Free Guidance（CFG）推理机制的重新审视。CFG 的引导速度场可被重写为无条件预测与隐式条件引导的组合：

$$\hat{v}_t^\theta(x|y) = v_t^\theta(x|\varnothing) + w \cdot (v_t^\theta(x|y) - v_t^\theta(x|\varnothing))$$

这一形式揭示了一个重要性质：**条件生成可被分解为“原始无条件预测”与“缩放的条件引导”之和**。受此启发，PureCC 将概念定制重新定义为：

$$v_t^{PureCC} = v_t^{original} + \lambda \cdot v_t^{target}$$

其中 $v_t^{original}$ 是原始模型对基本文本 $y_{base}$ 的条件预测（保持原始行为），$v_t^{target}$ 是从冻结的表示提取器中获取的目标概念隐式引导（注入个性化概念），$\lambda$ 控制二者的平衡。这一解耦使得模型可以在**不扰动原始条件预测**的前提下，纯粹地学习目标概念的表示偏置。

### 方法谱系与知识库定位

PureCC 处于**调优型概念定制**（tuning-based concept customization）方法谱系中，但与现有工作存在本质差异：

| 方法类别 | 代表工作 | 学习源 | 模型保持机制 | 核心缺陷 |
|---------|---------|--------|------------|---------|
| 全量微调 | DreamBooth (Ruiz et al., CVPR 2023) | 完整文本条件 | 先验保持损失（罕见类别） | 分布偏移严重，能力退化 |
| 正则化微调 | DreamBooth + EWC | 完整文本条件 | 弹性权重巩固 | 缓解有限，Seg-Cons 仅 26.37 |
| 参数高效微调 | LoRA, B-LoRA, LoRA-S | 完整文本条件 | 低秩约束 | 仍无法根本避免行为破坏 |
| 免调优方法 | DreamO, UNO | 无需微调 | 天然保持 | 概念响应度弱于调优方法 |
| **纯学习解耦** | **PureCC** | **基本文本 + 目标表示偏置** | **双分支架构 + 自适应 λ⋆** | 训练开销增加约 30% |

PureCC 的关键创新在于**将学习目标从“拟合完整条件分布”转变为“在原始预测之上叠加目标概念引导”**，并通过双分支训练管道（冻结的表示提取器 + 可训练流模型）和自适应引导强度 $\lambda^\star$ 实现这一解耦。这一设计使得 PureCC 在 DreamBenchPCC 基准上同时达到了最优的概念保真度（CLIP-I 0.81, DINO 0.73）和远超所有基线的模型保持能力（Seg-Cons 69.37 vs. 次优 26.37），证明了“纯学习”范式的有效性。

## 核心方法与创新机理

PureCC 的核心创新在于将概念定制重新定义为**在原始条件预测之上叠加目标概念的隐式指导**，从而从根本上解耦“学习新概念”与“保持原始模型行为”这两个相互冲突的目标。

### 瓶颈洞察：概念学习中的分布漂移

现有调优方法（如 **DreamBooth**（Ruiz et al., CVPR 2023）、LoRA、Mix-of-Show、CIFC 等）在微调时，将完整的语言-视觉知识作为学习源。然而，有限的参考图像使模型难以区分目标概念与冗余信息，导致两个关键退化：

1. **原始能力下降**：插入新概念后，模型的提示遵循度（CLIP-T）和生成质量（HPSv2.1）显著下降（Figure 1c）。
2. **分布漂移**：模型为拟合目标分布而调整预训练权重，导致原始分布发生偏移，KL Divergence 增大（Figure 2）。

这些退化源于一个根本性的设计缺陷：**传统方法将“原始模型预测”和“目标概念学习”耦合在同一个学习目标中**，即直接最小化 $v_t^\theta(x_t|y_{complete})$ 与目标速度场的距离（Eq. 3）。当 $y_{complete}$ 同时包含基本文本和目标概念时，模型无法区分哪些知识需要保持、哪些需要更新。

### 核心机制：解耦学习目标

PureCC 将学习目标重新表述为两个独立分量的组合：

$$
v_t^{PureCC} = v_t^{original} + \lambda \cdot v_t^{target}
$$

其中：
- **$v_t^{original}$**：原始条件预测，由可训练模型基于基本文本 $y_{base}$ 生成（Eq. 9），负责保持预训练模型的行为与能力。
- **$v_t^{target}$**：目标概念表示偏置，由冻结的表示提取器提供（Eq. 8），定义为 $v_t^{\theta_1}(x_t|y_{tar}) - v_t^{\theta_1}(x_t|\emptyset)$，即目标文本条件与无条件预测之间的差异。
- **$\lambda$**：控制目标概念注入强度的引导尺度。

这一分解的关键在于：**原始预测分量 $v_t^{original}$ 仅依赖基本文本 $y_{base}$，完全不接触目标概念信息**，从而在结构上保证了原始模型行为不会被目标概念学习所污染。目标概念则通过冻结提取器的表示偏置 $v_t^{target}$ 作为外部隐式引导注入，而非直接修改模型对完整文本的响应。

### 关键设计：自适应引导强度 $\lambda^\star$

固定 $\lambda$ 面临两难困境：过小则概念保真度不足，过大则导致分布漂移和生成能力退化（Figure 4）。PureCC 引入自适应 $\lambda^\star$，通过最小化可训练模型学到的目标表示 $\mathbf{R}(y_{complete}, y_{base})$ 与冻结提取器的引导表示 $\mathbf{R}(y_{tar})$ 之间的投影误差来动态计算：

$$
\lambda^\star = \frac{\langle \mathbf{R}(y_{complete}, y_{base}), \mathbf{R}(y_{tar}) \rangle}{\|\mathbf{R}(y_{tar})\|^2}
$$

该闭式解的本质是：**将可训练模型中学到的目标概念表示投影到冻结提取器的引导表示上，以投影系数作为最优引导强度**（Eq. 11–12）。这使得 $\lambda^\star$ 能够根据当前学习状态自适应调节——当模型已充分捕获目标概念时，$\lambda^\star$ 自然减小以避免过度注入。

### 架构创新：双分支训练流水线

PureCC 的两阶段训练流水线（Figure 3）是实现上述解耦目标的架构保障：

1. **第一阶段——表示提取器微调**：使用 LoRA 和每层可调概念嵌入（Layer-Wise Tunable Concept Embeddings，Eq. 7）微调一个流模型 $v_t^{\theta_1}$。该模型学习将目标概念编码为纯化的表示偏置 $\mathbf{R}(y_{tar})$，随后**完全冻结**，作为第二阶段的外部引导源。

2. **第二阶段——纯学习**：可训练模型 $v_t^{\theta_2}$ 从另一个预训练流模型初始化，仅接收基本文本 $y_{base}$ 以提供 $v_t^{original}$。目标概念通过冻结提取器的 $\mathbf{R}(y_{tar})$ 经 $\lambda^\star$ 缩放后隐式注入。整体损失函数为：

   $$
   \mathcal{L}_{PCC} = \mathcal{L}_{CC} + \eta \cdot \mathcal{L}_{PureCC}
   $$

   其中 $\mathcal{L}_{CC}$ 保持流匹配的基本约束，$\mathcal{L}_{PureCC}$ 驱动模型逼近 $v_t^{PureCC}$ 定义的目标速度场（Eq. 14–15）。

### 与基线方法的核心差异

| 设计维度 | 现有方法 | PureCC |
|---------|---------|--------|
| **学习目标** | 单一 $\mathcal{L}_{CC}$，耦合原始保持与概念学习 | $\mathcal{L}_{PCC} = \mathcal{L}_{CC} + \eta \cdot \mathcal{L}_{PureCC}$，显式解耦 |
| **条件输入** | 完整文本 $y_{complete}$ 同时用于条件与学习 | 可训练分支仅用 $y_{base}$，目标引导来自冻结提取器 |
| **引导机制** | 手动固定 CFG 尺度 | 自适应 $\lambda^\star$，基于表示投影动态计算 |
| **训练架构** | 单模型端到端微调 | 双分支：冻结提取器 + 可训练模型，分阶段训练 |

消融实验（Table 2）验证了这些设计的必要性：合并学习阶段（Merged Learning Stage）会显著破坏原始模型保持，而加入 $\mathcal{L}_{PureCC}$ 损失相比单独使用 $\mathcal{L}_{CC}$ 在 $\Delta$CLIP-T 和 $\Delta$HPSv2.1 上均有显著改善，且不牺牲概念保真度。

PureCC 的整体训练流程分为两个解耦阶段，核心思路是将概念定制拆解为“原始模型条件预测”与“目标概念隐式引导”的组合，从而在插入个性化概念的同时尽可能保持预训练模型的行为与生成能力。

### 阶段一：表示提取器微调

第一阶段的目标是构建一个能够提取目标概念纯化表示偏置的**表示提取器（Representation Extractor）**。具体而言，在预训练流模型 $v_t^{\theta_1}(\cdot)$ 上引入 LoRA 低秩适配，并设计**逐层可调概念嵌入（Layer-Wise Tunable Concept Embeddings）**，仅对定制集合进行微调。该阶段完成后，表示提取器被冻结，不再参与后续梯度更新。

### 阶段二：纯学习阶段

第二阶段是 PureCC 的核心——**纯学习（Pure Learning）**。该阶段采用双分支架构：

- **可训练流模型分支**：从另一个预训练流模型 $v_t^{\theta_2}(\cdot)$ 初始化，接收**基础文本条件 $y_{base}$**（即去除目标概念标记后的提示），输出**原始条件预测** $v_t^{\text{original}} = v_t^{\theta_2}(x_t|y_{base})$。该分支负责保持原始模型的生成行为。
- **冻结表示提取器分支**：接收**目标文本条件 $y_{tar}$**，通过计算其与空条件预测的差值，输出**目标概念表示偏置** $v_t^{\text{target}} = \mathbf{R}(y_{tar}) = v_t^{\theta_1}(x_t|y_{tar}) - v_t^{\theta_1}(x_t|\emptyset)$，作为对可训练分支的隐式引导。

两分支的输出通过**自适应引导强度 $\lambda^\star$** 进行组合，形成 PureCC 的学习目标速度场：

$$v_t^{\text{PureCC}} = v_t^{\theta_2}(x_t|y_{base}) + \lambda^\star \cdot \left(v_t^{\theta_1}(x_t|y_{tar}) - v_t^{\theta_1}(x_t|\emptyset)\right)$$

其中 $\lambda^\star$ 并非手工设定的固定值，而是通过最小化可训练模型中学到的目标表示 $\mathbf{R}(y_{complete}, y_{base})$ 在冻结引导表示 $\mathbf{R}(y_{tar})$ 上的投影误差，动态求得的闭式解：

$$\lambda^\star = \frac{\langle \mathbf{R}(y_{complete}, y_{base}), \mathbf{R}(y_{tar}) \rangle}{\|\mathbf{R}(y_{tar})\|^2}$$

最终训练损失由标准概念定制损失 $\mathcal{L}_{CC}$ 与纯概念定制损失 $\mathcal{L}_{PureCC}$ 加权组合：

$$\mathcal{L}_{PCC} = \mathcal{L}_{CC} + \eta \cdot \mathcal{L}_{PureCC}$$

其中 $\mathcal{L}_{PureCC}$ 强制可训练模型的预测逼近上述组合目标速度场 $v_t^{\text{PureCC}}$，而 $\mathcal{L}_{CC}$ 则保持对完整文本条件 $y_{complete}$ 的流匹配约束。

### 数据流与模块关系

整体数据流可以概括为：定制图像经流模型前向插值得到 $x_t$，基础文本 $y_{base}$ 与目标文本 $y_{tar}$ 分别输入可训练分支和冻结分支，各自产生速度预测；$\lambda^\star$ 根据两分支在速度流空间中的表示对齐程度自适应调节引导强度，最终合成 PureCC 目标速度场用于损失计算。推理时仅使用训练好的可训练模型，无需表示提取器参与，因此不引入额外推理开销。

> **Figure 3** 展示了上述两阶段流程：(a) 表示提取器微调；(b) 纯学习阶段的双分支架构及自适应 $\lambda^\star$ 机制；(c) 在速度流空间中通过 $\mathcal{L}_{PureCC}$ 纯化学习目标概念的过程。

![[assets/figures/papers/paper_list_l2338_https_arxiv_org_abs_2603_07561/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our PureCC. (a). We first fine-tune a flow model on the custom set as representation extractor. (b). During the pure learning stage, the representation extractor remains frozen and provides the target concept representation, which is then controlled by our adaptive scale*

PureCC 的核心设计围绕一个关键洞察展开：**将概念定制视为在原始条件预测之上叠加目标概念的隐式指导**。这一思想贯穿于整个方法架构，体现在三个核心模块的协同设计中。

### 2.1 解耦学习目标：速度场的分解与重组

PureCC 的学习目标建立在对速度场的解耦分解之上。传统概念定制方法直接最小化模型预测 $v_t^\theta(x_t|y_{complete})$ 与真实速度 $v_t(x_t)$ 的差异，导致模型在适应目标分布的同时偏离原始行为。PureCC 将目标速度场重新定义为两个分量的组合：

$$v_t^{PureCC} = v_t^{original} + \lambda \cdot v_t^{target}$$

其中 $v_t^{original}$ 是原始模型的条件预测分量，负责保持基础模型的生成行为与能力；$v_t^{target}$ 是目标概念的隐式引导分量，负责注入个性化概念的视觉特征；$\lambda$ 是控制两者平衡的引导强度。这一分解使得模型可以在不破坏原始条件预测的前提下，纯粹地学习目标概念的表示偏置。

### 2.2 表示提取器：目标概念引导的纯化

表示提取器（Representation Extractor）是 PureCC 双分支架构的第一个关键模块，其任务是提取目标概念的纯化表示偏置，作为第二阶段纯学习的隐式引导信号。

该模块基于一个预训练的流模型 $v_t^{\theta_1}(\cdot)$，在定制数据集上进行微调。微调采用 LoRA 进行参数高效更新，并引入**逐层可调概念嵌入**（Layer-Wise Tunable Concept Embeddings），在第 $l$ 层将基本文本 $y_{base}$ 与可学习的概念嵌入 $\mathbf{Y}_{tar}^l$ 拼接为完整文本嵌入：

$$\mathbf{Y}_{complete}^l = [y_{base}; \mathbf{Y}_{tar}^l]$$

微调完成后，表示提取器被冻结，其输出的目标概念表示偏置 $\mathbf{R}(y_{tar})$ 定义为条件预测与无条件预测之差：

$$v_t^{target} = \mathbf{R}(y_{tar}) = v_t^{\theta_1}(x_t|y_{tar}) - v_t^{\theta_1}(x_t|\emptyset)$$

这一差分的物理含义是：从冻结模型中提取目标概念 $y_{tar}$ 相对于空文本条件的速度场偏移，作为纯粹的目标概念引导信号。该信号在后续纯学习阶段保持不变，确保了引导的稳定性。

### 2.3 可训练流模型与双分支架构

第二阶段的可训练流模型 $v_t^{\theta_2}(\cdot)$ 从另一个预训练流模型初始化，负责提供原始条件预测并学习个性化概念。其核心输入仅为基本文本 $y_{base}$（不含目标概念描述），输出原始条件预测：

$$v_t^{original} = v_t^{\theta_2}(x_t|y_{base})$$

双分支架构的关键在于**条件解耦**：可训练分支只接收基本文本，因此其预测自然保持原始模型的行为；目标概念的引导完全由冻结的表示提取器以隐式方式注入。这与传统方法将所有语言-视觉知识混合输入形成鲜明对比，从根本上避免了冗余信息对原始模型行为的干扰。

### 2.4 自适应引导强度 $\lambda^\star$

固定的 $\lambda$ 无法适应不同概念和训练阶段的动态需求：过小的 $\lambda$ 导致概念保真度不足，过大的 $\lambda$ 则使目标概念主导学习目标，造成分布偏移和生成能力退化（见图 4）。PureCC 引入自适应机制，通过最小化两个分支中目标概念表示的投影误差来动态计算最优 $\lambda^\star$。

具体而言，可训练模型中学到的目标概念表示偏置为：

$$\mathbf{R}(y_{complete}, y_{base}) = v_t^{\theta_2}(x_t|y_{complete}) - v_t^{\theta_2}(x_t|y_{base})$$

将其投影到冻结提取器的引导表示 $\mathbf{R}(y_{tar})$ 上，得到闭式解：

$$\lambda^\star = \frac{\langle \mathbf{R}(y_{complete}, y_{base}), \mathbf{R}(y_{tar}) \rangle}{\|\mathbf{R}(y_{tar})\|^2}$$

这一计算本质上是将可训练分支学到的目标概念表示在冻结引导方向上的投影系数作为自适应强度，使得 $\lambda^\star$ 能够根据当前训练状态动态调整，在保真度与模型保持之间取得最优平衡。

### 2.5 总损失函数

最终的学习目标速度场为：

$$v_t^{PureCC} = v_t^{\theta_2}(x_t|y_{base}) + \lambda^\star \cdot (v_t^{\theta_1}(x_t|y_{tar}) - v_t^{\theta_1}(x_t|\emptyset))$$

PureCC 损失度量目标速度场与可训练模型完整条件预测之间的差异：

$$\mathcal{L}_{PureCC} = \mathbb{E}_{t,x_t} \| v_t^{PureCC} - v_t^{\theta_2}(x_t|y_{complete}) \|_2^2$$

总损失结合传统流匹配损失与纯概念定制损失：

$$\mathcal{L}_{PCC} = \mathcal{L}_{CC} + \eta \cdot \mathcal{L}_{PureCC}$$

其中 $\mathcal{L}_{CC}$ 为标准概念定制损失，$\eta$ 为平衡超参数。消融实验表明，$\eta=1.0$ 在实例和风格任务上提供最佳平衡（见表 3 和表 6），而单独使用 $\mathcal{L}_{CC}$ 则无法有效保持原始模型行为（见表 2）。

![[assets/figures/papers/paper_list_l2338_https_arxiv_org_abs_2603_07561/figures/002_Figure_2.jpg]]
*Figure 2: Original Distribution Drift. Visualization and KL Divergence results demonstrated that existing methods, which adjust pre-trained models to align with the target distribution for learning personalized concepts, lead to distribution drift*

![[assets/figures/papers/paper_list_l2338_https_arxiv_org_abs_2603_07561/figures/009_Figure_8.jpg]]
*Figure 8: Visualization of Pure Learning Process*

## 实验与关键发现

### 核心发现：原始模型行为与能力的保持

现有概念定制方法（如 **DreamBooth** (Ruiz et al., CVPR 2023)、LoRA、Mix-of-Show、CIFC 等）在微调时，将预训练模型的全部语言-视觉知识作为学习源。然而，由于参考图像数量有限，模型难以区分目标概念与冗余信息，导致插入新概念后，原始模型的行为与能力显著下降。PureCC 的核心洞察在于，将概念定制重新定义为在原始条件预测之上叠加目标概念的隐式指导，从而在保持原始模型行为的同时“纯粹地”学习个性化概念。

图 1(c) 的下降曲线直接量化了这一退化现象：随着概念注入，现有方法的 CLIP-T（提示遵循度）和 HPSv2.1（生成质量）得分明显下滑。图 2 的可视化与 KL 散度结果进一步证实，现有方法将预训练模型向目标分布对齐的过程，导致了原始分布的偏移。

PureCC 在 DreamBenchPCC 基准上的定量结果（表 1）提供了决定性证据。在衡量原始模型行为保持的 Seg-Cons 指标上，PureCC 达到 **69.37**，而次优的 DreamBooth+EWC 仅为 26.37，CIFC 仅为 13.23。这表明 PureCC 在插入个性化概念后，几乎完整地保留了原始模型对非目标区域的空间布局一致性。同时，在目标概念保真度方面，PureCC 的 CLIP-I（目标）达到 **0.81**，DINO 达到 **0.73**，均优于所有调优基线，证明其“纯学习”策略并未以牺牲概念响应为代价。

### 主实验定量结果

表 1 汇总了 DreamBenchPCC 上的全面比较。对于调优方法，我们关注原始模型保持（ΔCLIP-T、ΔHPSv2.1、Seg-Cons）与目标概念保真度（CLIP-I、DINO）两个维度。对于免调优方法（DreamO、UNO），由于它们不微调基础模型，仅比较其概念响应度。

**实例概念定制**：
- **原始模型保持**：PureCC 的 ΔCLIP-T(base) 仅为 **-0.31**（越接近 0 表示文本对齐保持越好），而 CIFC 为 -1.93，DreamBooth 为 -4.81。ΔHPSv2.1 方面，PureCC 甚至实现了 **+0.10** 的正向变化，而其他方法均为负值（CIFC: -1.62, DreamBooth: -2.17），表明 PureCC 在保持生成质量上具有独特优势。
- **目标概念保真度**：PureCC 的 CLIP-I（目标）**0.81** 领先 CIFC（0.78）和 DreamO（0.71），DINO **0.73** 同样最高。

**风格概念定制**：
- PureCC 的风格一致性（CSD）为 **0.63**，与 CIFC（0.64）基本持平，略低 0.01。这表明在风格与内容的解耦上仍有微调空间，但整体竞争力充足。

### 消融实验：纯学习机制的有效性

表 2 的消融实验验证了 PureCC 损失函数与分阶段训练策略的关键作用。

**损失函数设计**：对比仅使用标准概念定制损失 $L_{CC}$ 与加入 $L_{PureCC}$（即 $L_{PCC} = L_{CC} + \eta \cdot L_{PureCC}$）的效果。结果表明，加入 $L_{PureCC}$ 后，原始模型保持指标（ΔCLIP-T、ΔHPSv2.1）显著改善，同时概念保真度（CLIP-I、DINO）未受损失。这证实了将学习目标解耦为“原始条件预测 + 目标概念隐式指导”的因果机制是有效的。

**分阶段训练策略**：将表示提取器训练与纯学习阶段合并（Merged Learning Stage）会导致原始模型行为破坏，因为目标概念的提取与学习过程相互干扰。PureCC 的先独立微调表示提取器再冻结的策略，有效解耦了目标概念表示，避免了这一冲突。

### 自适应引导强度 λ⋆ 的消融

表 3 的消融实验对比了固定 λ 与自适应 λ⋆ 的效果。自适应 λ⋆ 通过最小化可训练模型中学到的目标表示 $\mathbf{R}(y_{complete}, y_{base})$ 在冻结提取器的引导表示 $\mathbf{R}(y_{tar})$ 上的投影误差（式 11-12），动态平衡保真度与模型保持。结果显示，自适应 λ⋆ 在所有指标上均优于固定 λ 的最佳取值，验证了其动态调节的必要性。

超参数 η 的调节（表 6）进一步揭示了平衡点：η=1.0 在实例和风格任务上提供了最佳折衷。η 过大会导致目标概念过度注入，η 过小则原始模型保持不足。

### 计算开销与效率

表 4 和表 5 报告了训练与推理的计算开销。相比单阶段方法，PureCC 增加了额外的表示提取器训练阶段和双分支架构，导致训练时间和显存占用增加约 30%。但推理时无额外开销——表示提取器仅在第一阶段使用，推理仅需可训练模型。在单张 NVIDIA A100 GPU 上，PureCC 的训练时间与内存消耗处于可接受范围。

### 失败模式与局限性

1. **风格一致性略逊**：在少数场景下，PureCC 的风格一致性（CSD 0.63）略低于 CIFC（0.64），表明风格与内容的解耦可能需要进一步细化。
2. **超参数敏感性**：自适应 λ⋆ 依赖于 η 的手动调节，η 选择不当会导致概念注入过度或不足。
3. **训练开销增加**：双阶段训练相比单阶段方法增加了约 30% 的训练时间和显存占用，对资源受限场景不够友好。

### 用户研究验证

表 7 的用户研究结果从人类偏好角度验证了 PureCC 的优势。参与者在概念保真度、原始模型行为保持和整体质量三个维度上，对 PureCC 的偏好显著高于各基线方法，与定量指标的趋势一致。

![[assets/figures/papers/paper_list_l2338_https_arxiv_org_abs_2603_07561/figures/006_Table_1.jpg]]
*Table 1: Quantitative Comparison Results on DreamBenchCC. Since UNO and DreamO are Tuning-free methods that do not require fine-tuning the base model, our comparison for them focuses mainly on their concept responsiveness*

![[assets/figures/papers/paper_list_l2338_https_arxiv_org_abs_2603_07561/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative Comparison with SOTAs including Tuning-based methods: DreamBooth [36], DreamBooth + EWC [39], Mix-of-Show [13], CIFC [9], and Tuning-free methods: DreamO [31] UNO [46]*

![[assets/figures/papers/paper_list_l2338_https_arxiv_org_abs_2603_07561/figures/012_Table_3.jpg]]
*Table 3: Ablation Study of the λ⋆*

## 定位与知识库关联

### 1. 问题定位：概念定制中的“原始能力退化”瓶颈

文本到图像（T2I）的概念定制任务旨在将用户提供的少量参考图像中的特定视觉概念（物体实例或艺术风格）植入预训练生成模型，使其能在新的文本提示下生成包含该概念的图像。现有方法——无论是全量微调的代表 **DreamBooth** (Ruiz et al., CVPR 2023)、参数高效的 **LoRA** 系列，还是免调优的 **DreamO** 与 **UNO**——在实现概念注入的同时，普遍面临一个核心瓶颈：**原始模型的生成行为与能力在定制后显著退化**。

PureCC 通过系统性的实验揭示了这一瓶颈的因果机制。如图 1(c) 所示，现有方法在定制后，其 CLIP-T（提示遵循度）和 HPSv2.1（生成质量）得分均呈明显下降曲线，表明模型遵循文本指令和生成高质量图像的能力受损。进一步地，图 2 通过 KL 散度量化了原始分布的偏移：现有方法将预训练模型向目标分布对齐以学习个性化概念，这一过程不可避免地导致分布漂移（distribution drift）。其根本原因在于，**有限参考图像所提供的监督信号中混杂了大量与目标概念无关的冗余信息，模型在微调时无法有效区分目标概念与背景、姿态等干扰因素**，从而在插入新概念的同时“冲垮”了原始模型习得的语言-视觉知识结构。

### 2. 核心方法定位：解耦学习与双分支架构

PureCC 的核心洞察在于将概念定制的学习目标重新定义为一种**叠加式组合**：在原始模型的条件预测之上，叠加目标概念的隐式指导。这一思想在数学上体现为：

$$v_t^{\text{PureCC}} = v_t^{\text{original}} + \lambda \cdot v_t^{\text{target}}$$

其中 $v_t^{\text{original}}$ 由可训练模型基于基础文本 $y_{base}$ 生成，保留了原始模型的生成行为；$v_t^{\text{target}}$ 由冻结的表示提取器提供，承载纯粹的目标概念信息；$\lambda$ 控制概念注入的强度。

与现有方法的关键区别在于以下几点。

**（1）学习目标的解耦。** 传统方法使用完整文本 $y_{complete}$ 同时进行条件预测和学习，使得目标概念与原始知识在损失函数中不可分割地耦合。PureCC 将二者显式分解：可训练分支仅接收基础文本 $y_{base}$ 以产生原始条件预测 $v_t^{\text{original}}$，而目标概念的引导信息来自一个独立冻结的表示提取器。这确保了概念学习过程不会污染原始模型的行为空间。

**（2）双分支训练流水线。** PureCC 采用两阶段训练策略（图 3）：
- **第一阶段——表示提取器微调**：使用 LoRA 和每层可调概念嵌入（Layer-Wise Tunable Concept Embeddings）微调一个流模型 $v_t^{\theta_1}$，使其学会从目标文本 $y_{tar}$ 中提取纯粹的概念表示偏置 $\mathbf{R}(y_{tar}) = v_t^{\theta_1}(x_t|y_{tar}) - v_t^{\theta_1}(x_t|\emptyset)$。该提取器在第二阶段完全冻结，作为稳定的概念引导源。
- **第二阶段——纯学习**：可训练模型 $v_t^{\theta_2}$ 从另一个预训练流模型初始化，仅接收基础文本 $y_{base}$ 产生原始预测，同时接受来自冻结提取器的自适应缩放引导。

**（3）自适应引导强度 $\lambda^\star$。** 不同于传统方法中手动固定的引导尺度，PureCC 通过最小化可训练模型中学到的目标表示 $\mathbf{R}(y_{complete}, y_{base})$ 与冻结提取器的引导表示 $\mathbf{R}(y_{tar})$ 之间的投影误差，动态求解最优 $\lambda^\star$：

$$\lambda^\star = \frac{\langle \mathbf{R}(y_{complete}, y_{base}), \mathbf{R}(y_{tar}) \rangle}{\|\mathbf{R}(y_{tar})\|^2}$$

这一闭式解使得概念注入强度能够根据当前学习状态自适应调节，在保真度与模型保持之间取得动态平衡。

### 3. 与现有工作的谱系关系

PureCC 位于**调优型概念定制**方法谱系中，但其设计哲学与现有工作形成鲜明对比。

**与全量/参数高效微调方法的关系。** **DreamBooth** (Ruiz et al., CVPR 2023) 通过微调全部或部分模型参数，配合稀有词绑定和先验保持损失来学习概念。**LoRA** 及其变体（**B-LoRA**、**LoRA-S**）通过低秩适配器降低调优开销。**Mix-of-Show** 和 **CIFC** 则探索了多概念组合与解耦。这些方法的共同前提是**将全部语言-视觉知识作为学习源**，因此不可避免地面临原始能力退化。DreamBooth + EWC 尝试通过弹性权重巩固来缓解遗忘，但表 1 显示其 Seg-Cons 仅 26.37，远低于 PureCC 的 69.37，说明简单的正则化不足以从根本上解决分布漂移。

**与免调优方法的关系。** **DreamO** 和 **UNO** 等免调优方法不修改基础模型权重，因此天然避免了原始能力退化问题。然而，它们的概念响应度（concept responsiveness）通常弱于调优方法——表 1 中 DreamO 的 CLIP-I 仅 0.71，而 PureCC 达到 0.81。PureCC 通过“学习但不破坏”的策略，在调优方法的保真度优势和免调优方法的保持优势之间取得了突破性平衡。

**在知识库中的独特贡献。** PureCC 首次将概念定制问题形式化为“原始条件预测 + 目标概念隐式引导”的叠加模型，并配套设计了完整的双分支训练与自适应引导机制。这一框架不仅解决了当前瓶颈，更为后续研究提供了可扩展的范式：新概念的学习被约束在“引导偏置”子空间中，而不侵入原始模型的条件预测主干。

### 4. 适用边界与局限

尽管 PureCC 在 DreamBenchPCC 基准上取得了显著优势，其方法仍存在若干适用边界与局限。

**（1）训练开销增加。** 相比单阶段方法，PureCC 增加了表示提取器的独立微调阶段和双分支架构，导致训练时间和显存消耗增加约 30%（见表 4 和表 5）。在资源受限的场景下，这一额外开销可能成为部署障碍。但推理阶段无额外开销，因为冻结提取器和自适应 $\lambda^\star$ 仅用于训练，推理时仅使用训练后的单一模型。

**（2）超参数敏感性。** 自适应 $\lambda^\star$ 的有效性依赖于超参数 $\eta$ 的调节（总损失 $\mathcal{L}_{PCC} = \mathcal{L}_{CC} + \eta \cdot \mathcal{L}_{PureCC}$）。表 6 的消融显示，$\eta$ 过大会导致目标概念过度注入，过小则原始模型保持不足。当前 $\eta=1.0$ 在实例和风格任务上提供了最佳平衡，但这一取值可能需要根据具体定制集合进行手动调节，缺乏自适应性。

**（3）风格一致性的微小差距。** 在风格定制场景下，PureCC 的 CSD（风格一致性）得分为 0.63，略低于 CIFC 的 0.64（差距 -0.01）。这可能表明 PureCC 的“原始预测 + 目标引导”分解在风格与内容的解耦上仍有细化空间——风格概念往往与内容表征存在更紧密的纠缠，简单的速度场叠加可能不足以完全捕捉风格的全局特性。

**（4）大规模多概念场景未充分验证。** 当前实验主要覆盖单概念和少量多概念（图 6）定制场景。在持续学习（continual learning）或大规模概念库（如数十个概念同时定制）场景下，表示提取器的容量、双分支架构的扩展性以及概念间干扰问题尚未得到系统评估。

### 5. 开放问题

PureCC 的解耦学习范式为概念定制领域开启了若干值得探索的方向。

**（1）自适应超参数选择。** 能否根据定制集合的统计特性（如参考图像数量、概念复杂度、与预训练分布的距离）自动确定最优 $\eta$？这可能需要引入元学习或基于验证集的自适应调节机制。

**（2）大规模与持续概念学习。** 当需要定制大量概念或持续添加新概念时，PureCC 的表示提取器是否需要扩展为多概念共享的“概念编码器”？双分支架构如何避免概念间的语义纠缠（图 6 虽展示了初步的多概念结果，但规模有限）？

**（3）跨模态与跨任务扩展。** PureCC 的“原始预测 + 目标引导”框架本质上是将新知识的学习约束在引导偏置子空间中。这一思想能否扩展到视频生成（时间维度的原始行为保持）、3D 内容生成（几何一致性的保持）或其他条件生成任务？

**（4）理论分析。** 当前对分布漂移的量化依赖 KL 散度的经验估计，对 $\lambda^\star$ 的闭式解基于投影误差最小化的启发式推导。能否从信息瓶颈理论或神经正切核（NTK）角度，为 PureCC 的模型保持能力提供更严格的理论保证？

**（5）与免调优方法的深度融合。** PureCC 在保真度上优于免调优方法，在模型保持上优于传统调优方法。能否将 PureCC 的表示提取器与免调优方法的注意力注入机制结合，进一步降低甚至消除调优需求？

## 原文 PDF

![[paperPDFs/CVPR_2026/PureCC_Pure_Learning_for_Text_to_Image_Concept_Customization.pdf]]
