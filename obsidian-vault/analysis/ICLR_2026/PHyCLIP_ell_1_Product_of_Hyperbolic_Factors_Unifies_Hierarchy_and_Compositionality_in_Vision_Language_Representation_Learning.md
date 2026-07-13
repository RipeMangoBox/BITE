---
title: "PHyCLIP: $\\ell_1$-Product of Hyperbolic Factors Unifies Hierarchy and Compositionality in Vision-Language Representation Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PHyCLIP_ell_1_Product_of_Hyperbolic_Factors_Unifies_Hierarchy_and_Compositionality_in_Vision_Language_Representation_Learning.pdf
project_link: null
code_link: null
aliases:
- PHyCLIP
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将单一的嵌入空间替换为多个双曲因子的 ℓ1 乘积，每个因子独立编码一个概念族的层次分类，因子间的 ℓ1 距离支持跨族的组合。"
primary_logic: "族内层次关系天然地嵌入双曲空间（树形），跨族组合对应于布尔代数的同构嵌入 ℓ1 乘积度量；因此双曲因子的 ℓ1 乘积能统一两种语义结构。"
claims:
- "PHyCLIP 在零样本分类、检索、层次分类和组合理解任务上相比于纯双曲或欧氏空间基线取得一致提升。"
- "消融实验表明 ℓ1 乘积度量显著优于 ℓ∞ 乘积或混合曲率设定，且 64 因子 8 维的设置最优。"
- "可视化显示不同因子专门捕捉不同概念族（如动物 vs 交通工具），且文本组合提示词会同时激活对应因子。"
- "WordNet Hierarchical Classification 上 TIE (↓) = 3.294"
---

# PHyCLIP: $\ell_1$-Product of Hyperbolic Factors Unifies Hierarchy and Compositionality in Vision-Language Representation Learning

> [!tip] 核心洞察
> 族内层次关系天然地嵌入双曲空间（树形），跨族组合对应于布尔代数的同构嵌入 ℓ1 乘积度量；因此双曲因子的 ℓ1 乘积能统一两种语义结构。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PHyCLIP：超椭圆因子ℓ1乘积统一视觉-语言表征中的层次性与组合性 |
| 英文题名 | PHyCLIP: $\ell_1$-Product of Hyperbolic Factors Unifies Hierarchy and Compositionality in Vision-Language Representation Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=I3Ct1eDmVI) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | PHyCLIP |
| Dataset | WordNet Hierarchical Classification, COCO Text→Image Retrieval, COCO Image→Text Retrieval |

> [!tip] 效果简介
> - WordNet Hierarchical Classification 上，TIE (↓) 为 3.294，对比 3.319 (HyCoCLIP)，变化 -0.025。
> - WordNet Hierarchical Classification 上，Jaccard (↑) 为 0.8059，对比 0.8043 (HyCoCLIP)，变化 +0.0016。
> - COCO Text→Image Retrieval 上，R@5 为 58.03，对比 57.11 (HyCoCLIP)，变化 +0.92。

## 概要

现代视觉‑语言模型（VLM）需要同时处理两种根本不同的语义结构：概念族内部的层次隶属关系（树形分类）与跨概念族的组合关系（布尔代数式组合）。现有的对比学习框架通常将图像和文本编码至单一欧氏空间或单一双曲空间，然而前者难以编码树状的层次结构，后者则难以表达跨族的组合性，这一瓶颈限制了模型在细粒度分类、组合理解等任务上的性能。

PHyCLIP 针对上述瓶颈提出了一个简洁而有效的解决方案：将嵌入空间构造为 **k 个双曲因子的 ℓ₁‑乘积空间** $( \mathbb{H}^d)^k$。其中每个因子独立承载一个概念族的层次分类，因子之间的 ℓ₁ 距离则自然地支持跨族的组合语义。其核心洞见在于，族内层次关系天然地适于嵌入双曲空间（树形），而跨族组合恰好对应于布尔代数的 ℓ₁ 乘积同构嵌入，因此将二者统一于双曲因子的 ℓ₁ 乘积度量中即可同时捕获层次性与组合性。

在方法层面，PHyCLIP 保留了 CLIP 风格的双编码器架构（ViT 图像编码器与 Transformer 文本编码器），将编码器输出通过指数映射提升至各因子的双曲空间，并采用因子内的双曲包含锥来建模蕴含关系（例如“狗 ⊑ 动物”），同时利用各因子距离之和（ℓ₁‑乘积距离）定义对比损失（InfoNCE）。总体训练目标为对比损失与蕴含损失的加权和。相比基线方法（CLIP 的欧氏空间、MERU 的单一双曲空间、HyCoCLIP 的盒子标注双曲空间），PHyCLIP 仅增加极少量可学习曲率参数（k 个），保持了与主流模型相当的计算开销。

实验结果表明，PHyCLIP 在零样本分类、检索、层次分类与组合理解四个维度上均取得一致提升：零样本层次分类的 TIE 指标降至 3.294（HyCoCLIP 为 3.319）；在 SugarCrepe 组合理解总体准确率上达到 78.32（基线为 77.99）；消融实验进一步验证了 ℓ₁‑乘积度量显著优于 ℓ∞ 乘积或混合曲率设定，且因子数量 $k=64$、维度 $d=8$ 的配置表现最优。可视化分析显示，不同因子自发地专门化至不同概念族（如动物与交通工具），且复合文本提示会同时激活对应因子，呈现出类似布尔组合的激活模式。这些证据共同支撑了 PHyCLIP 在统一层次性与组合性方面的有效性。

当前主流的视觉–语言模型（如 CLIP）通过对比学习在欧几里得空间中对齐图像与文本的嵌入。然而，语言概念天然承载着两种截然不同却并存的语义结构：**概念族内部的树状层次分类**（例如“金毛犬→犬科→哺乳动物→动物”）与**跨概念族的组合性**（例如“一只狗坐在车里”由“狗”和“车”组合而成）。前者要求表示空间能够编码严格的部分‑整体或种属包含关系，后者则要求空间能够支持类似布尔代数的概念合取/析取操作。欧氏空间虽然简单易用，但其全局平坦的几何特性难以同时为这两种结构提供自然的归纳偏置——层次关系在欧氏距离下缺少内在的包含方向感，而组合语义也很难通过余弦距离的简单运算得到体现。

为应对层次性挑战，近年来的工作（如 MERU、HyCoCLIP）将表示空间切换为双曲空间。双曲几何因其负曲率而具有“树状”的等距嵌入能力，能够用包含锥等工具形式化地定义超/下位词关系（entailment）。然而，这些方法仍将整个语义空间压缩到**单一**的双曲流形上，导致跨概念族的组合性遭到抑制。理论分析（见 §2）表明：布尔代数（组合性的数学抽象）可以等距地、保序地嵌入 ℓ₁‑乘积度量空间，但**无法**以保序嵌入的方式放入单一的纯双曲空间。这一点从原理上决定了：单双曲空间模型即使能够捕捉到一定程度的层次包含，也难以自然地表达“狗 ∘ 车”这类跨族组合，并在组合理解基准（如 SugarCrepe）上留下明显的性能缺口。

换言之，现有视觉–语言表示学习的核心瓶颈在于：**没有一个统一的几何空间能够同时容纳树状层次与布尔代数组合两种结构**。这导致模型要么擅长层次推理却牺牲组合能力（单双曲空间），要么保留组合泛化但忽略类别间的包含关系（欧氏空间），从而无法有效表达概念族内的传递关系与跨族的概念组合。

本文的动机正是填补这一空白。PHyCLIP 提出将表示空间重新设计为 **k 个独立双曲因子的 ℓ₁‑乘积度量空间（$(\mathbb{H}^d)^k$，其中 k = 64，d = 8，总维数 512）**。其核心洞察是：族内层次关系可被每个双曲因子内的包含锥独立捕获，而跨族组合则等价于布尔代数的 ℓ₁‑等距嵌入，因此 ℓ₁‑乘积度量天然统一了两种结构。后续实验表明，这种架构上的“因果开关”能够自发引导模型在不同的双曲因子中沉淀不同的概念族（如哺乳动物因子 vs. 交通工具因子，见 Figure 4、Figure 5），并通过各因子距离之和（ℓ₁‑距离）实现稳定的组合相似度计算，从而在零样本分类、层次分类与组合理解任务上对纯双曲或欧氏基线取得一致提升（见 Table 1–3；所有提升均有消融实验支撑，置信度 ≥ 0.9）。

## 核心方法与创新机理

现有视觉–语言模型（CLIP、MERU、HyCoCLIP）仅在单一欧氏或单一双曲空间中表征语义，无法同时容纳“树状层次”与“布尔组合”两种并存的语义结构：同一概念族内的传递性包含关系（如“贵宾犬 ≺ 犬科 ≺ 哺乳动物”）天然适合嵌入双曲空间，而跨概念族的组合（如“男孩 与 自行车”）则需满足布尔代数的组合规则，后者与 ℓ₁ 乘积度量自然同构，与单一双曲空间却不兼容。这一结构失配导致模型在层次分类与组合理解之间难以兼顾。

**PHyCLIP 的核心创新在于将单一的表示空间替换为多个双曲因子的 ℓ₁ 乘积空间**，使得族内层次关系与跨族组合性在统一几何下同时被捕捉。其关键变化槽（changed slots）如下表所示，每一项均直接改变了模型对语义结构的建模能力。

| 变化槽 | 基线值 | 提出值 | 作用机制与证据 |
|--------|--------|--------|----------------|
| **嵌入空间** | 单一欧氏空间（CLIP）或单一双曲空间（MERU, HyCoCLIP） |  $(\mathbb{H}^d)^k$，即 $k=64$ 个 $d=8$ 维双曲因子的笛卡尔积（总维度 512） | 每个因子自发地捕捉一个概念族的层次分类（如 i=39 对应哺乳动物子树，i=9 对应交通工具子树）；Figure 4、Figure 5 的因子级可视化和层次投影为此提供了直接证据。 |
| **距离度量** | 余弦距离（CLIP）或由多重双曲汇总的单一双曲距离（MERU, HyCoCLIP） | 各因子的双曲距离之和 $d_1(\boldsymbol{X},\boldsymbol{Y})=\sum_{i=1}^{k} d_{\mathbb{H}_i^d}(\boldsymbol{x}^{(i)},\boldsymbol{y}^{(i)})$ 用于对比损失 | ℓ₁ 乘积度量与布尔代数的同构性（Theorem 2）使其能自然支持跨族组合；消融实验（Table 4）表明 ℓ₁ 乘积在 ImageNet、Food-101 等任务上大幅优于 ℓ∞ 乘积（Food-101 零样本分类 44.31 vs. 6.55），混合曲率设定也全面落后。 |
| **层次关系建模** | HyCoCLIP 在单一双曲空间中使用双曲包含锥，但因子间无显式组合机制 | 各因子内独立施加双曲包含锥约束 $\boldsymbol{x}^{(i)} \in \mathcal{C}(\boldsymbol{y}^{(i)})$，跨因子组合通过 ℓ₁ 距离和 factor‑wise max 操作实现逻辑“或” | 包含损失（Eq. 5）强制图像嵌入落在对应文本嵌入的包含锥内，从而编码“图像比文本更具体”的层次关系；因子最大值机制使“狗和车”的文本组合能同时激活动物因子与交通工具因子（Figure 4a），并检索到同时包含两类物体的图像。 |

### 为何 ℓ₁ 乘积能统一层次与组合性？

这一设计的理论基础来自两个观察：  
1. **族内层次天然适合双曲几何**：概念族内部的树形分类结构（is‑a 关系）在双曲空间中可以低失真地嵌入，而单一欧氏空间无法做到。  
2. **跨族组合映射为 ℓ₁ 乘积度量**：布尔格 $(\{0,1\}^n, d_{\mathrm{Ham}})$ 可等距嵌入到 ℓ₁ 乘积度量空间（当因子数 ≥ 概念数时），因此用 ℓ₁ 乘积度量来聚合不同因子的距离，等价于对“概念是否出现”的二值编码做汉明距离求和。这使得“男孩骑自行车”的语义可以分解为“男孩”因子与“自行车”因子的叠加，两个因子的距离之和衡量组合图像的匹配程度。

PHyCLIP 将图像与文本分别编码为 ℓ₁ 乘积空间中的元组，对比损失（InfoNCE）在平均距离 $d_{\mathrm{avg}}$ 上操作，而包含损失（$\mathcal{L}_{\mathrm{ent}}$）在每个因子内独立推动层次关系。这种统一几何使得模型不需要在层次性与组合性之间做取舍，零样本分类、检索、层次分类和组合理解任务上都能获得一致提升：例如在 WordNet 层次分类上 TIE 降至 3.294（vs. HyCoCLIP 3.319），在 SugarCrepe 组合理解综合准确率提升至 78.32（vs. 77.99），在 COCO 文本→图像检索 R@5 提高到 58.03（vs. 57.11）等（Table 2, Table 3）。

### 实验验证的核心证据

- **ℓ₁ 乘积度量的消融优势**：Table 4 直接比较了不同乘积度量（ℓ₁/ℓ∞）和不同空间配置，仅当使用 ℓ₁ 乘积 + 全双曲因子时，模型在 ImageNet、Food-101、COCO 检索及层次分类四项任务上均表现优异；ℓ∞ 乘积导致模型崩溃（Food-101 仅 6.55）。  
- **因子特异性与组合性的可视化**：Figure 4a 显示“a photo of a dog”主要激活因子 i=39，“a photo of a car”激活 i=9；而“a dog and a car”的文本同时激活这两个因子，且通过 factor‑wise max 操作可产生与文本组合高度一致的图像检索（Figure 4b–c）。Figure 5 通过 HoroPCA 二维投影进一步证实因子 i=39 内形成了哺乳动物的层次结构，而无关因子则将这些概念压缩至原点附近。  
- **对比其他空间的优越性**：混合曲率（欧氏、双曲、球面）模型整体性能不如全双曲 ℓ₁ 乘积（Table 4 文字说明），表明单纯的混合空间不能替代因子化乘积。

### 当前局限与未来方向

尽管创新带来了显著收益，模型仍存在若干边界：  
- 关系结构的建模（如 SugarCrepe 中的 Swap/Replace 子任务）有时依旧落后，说明 ℓ₁ 乘积尚未显式编码关系的代数规则；  
- 包含锥的半孔径（最大 180°）不能完全“关闭”无关因子，导致嵌入中仍残留微弱激活；  
- 因子数 k 和维数 d 需人工指定，且在极细粒度分类（如 Food-101）上增大 k 非单调提升。  

这些局限为下一步将关系代数结构显式纳入因子化乘积空间，以及设计自适应因子数量机制提供了明确路径。

![[assets/figures/papers/iclr26_0016_I3Ct1eDmVI_PHyCLIP_ell_1-Product_of_Hyperbolic_Factors_Unif/figures/002_Figure_1.jpg]]
*Figure 1: Conceptual diagram of hierarchical and compositional structures. While all arrows represent entailments (⪯), they differ in nature. (upper) Linguistic concepts organize tree-like taxonomic hierarchies of concept families, each of which can be embedded into a hyperbolic space (Sarkar, 2011). (middle) Images and texts exhibit compositionality across distinct concept families, which can be captured by a Boolean algebra or an $\ell _ { 1 }$ -product metric. (lower) Images are instances of their corresponding captions. Figure 2: Overview of PHyCLIP. Images and texts are encoded as points X in an $\ell _ { 1 } \cdot$ -product metric space of hyperbolic factors, ( $\mathbb { H } ^ { d } ) ^ { k }$ , tha...

PHyCLIP 采用双塔架构，在图像与文本两个支路上分别将输入编码为同一 ℓ₁-乘积双曲空间中的点元组，再通过对比损失与蕴含损失联合训练，以同时捕获层次化语义和组合性语义（图 2）。整体流程可划分为编码、几何映射、度量构造与损失计算四个阶段。

**编码阶段**  
- 图像编码器为 Vision Transformer (ViT-B/16)，将图像映射为一个 $kd = 512$ 维特征向量。  
- 文本编码器为 12 层 Transformer，输出同样维度（512 维）的文本特征向量。  
- $k=64$、$d=8$ 是默认配置，对应 64 个独立语义因子，每个因子维度为 8。

**几何映射与因子拆分**  
将图像/文本编码器输出的 512 维向量按因子拆分，得到 $k$ 个 $d$ 维切向量。对每个切向量，通过关于罗伦兹模型的指数映射 $\exp_{\hat{o}}^{\alpha}$（式 12）将其提升到对应的双曲空间 $\mathbb{H}^d_i$ 中，最终形成属于乘积空间 $(\mathbb{H}^d)^k$ 的一个点元组 $\mathbf{X} = (\mathbf{x}^{(1)}, \dots, \mathbf{x}^{(k)})$。  
每个因子独立维护自身的双曲几何与曲率参数（通过可学习的 $\alpha_i$ 控制），因此在训练中各因子会自发地分化并编码不同的概念族（如动物、交通工具等，图 4 给出实证）。

**度量与蕴含锥**  
- 在乘积空间上，采用各因子双曲距离之和作为整体距离（$d_1$ 度量，式 2），以支持跨因子概念组合：$d_1(\mathbf{X}, \mathbf{Y}) = \sum_{i=1}^{k} d_{\mathbb{H}_i^d}(\mathbf{x}^{(i)}, \mathbf{y}^{(i)})$。  
- 在每个因子内部，通过双曲蕴含锥（entailment cone，式 5、13–14）刻画子概念与父概念间的定向包含关系 $\mathbf{x}^{(i)} \in C(\mathbf{y}^{(i)})$，其惩罚量 $L_{\mathrm{ent},i}$ 由锥外角的大小决定。

**损失函数**  
最终训练目标为对比损失与蕴含损失的线性组合（式 1）：  
$$\mathcal{L}_{\mathrm{overall}} = \mathcal{L}_{\mathrm{cont}} + \gamma \mathcal{L}_{\mathrm{ent}}$$  
- 对比损失（式 3–4）采用 InfoNCE 形式，基于平均距离 $d_{\mathrm{avg}} = d_1 / k$ 与可学习温度 $\tau$，拉近匹配的图像-文本对，推开批次内其他样本。该损失促使跨因子组合在距离度量下合理整体对齐。  
- 蕴含损失以分因子方式施加（式 5–6），仅在已知层次关系的样本（如由文本盒标注提供的上下位约束）上生效，惩罚离开蕴含锥的违反程度。

**输入输出流总结**  
1. 输入：原始图像 + 对应文本（可含层次标注作为弱监督）。  
2. 编码：ViT 与 Transformer 分别产生 $kd$ 维向量。  
3. 拆分与映射：切向量经指数映射进入 $k$ 个双曲因子，获得 $(\mathbb{H}^d)^k$ 中的点。  
4. 损失计算：用 $d_1$ 距离计算对比损失，用各因子蕴含锥计算蕴含损失。  
5. 输出：训练好的编码器与双曲参数，可支持零样本分类、图像-文本检索、层次分类、组合理解等多种下游任务。

该框架将族内层次结构（由各因子内部的双曲树形结构承载）与跨族组合性（由因子间的 ℓ₁ 和逻辑“或”风格的最大激活操作体现）自然地统一在统一度量空间中，并通过消融实验验证了 ℓ₁ 乘积在多个指标上的显著优越性（表 4）。

PHyCLIP 的核心设计是将视觉与文本嵌入表达为 **k 个双曲因子的元组**，并在因子的 ℓ1‑乘积空间上定义对比损失与包含损失，从而在统一的度量下同时捕获**族内层次结构**与**跨族组合语义**。以下按模块组织关键公式并解释变量含义。

### 1. 双曲因子的 ℓ1‑乘积空间与距离

图像编码器 (ViT) 与文本编码器 (Transformer) 输出 k×d 维欧氏向量，经因子拆分与指数映射提升为元组  
`$X = (\mathbf{x}^{(1)}, \dots, \mathbf{x}^{(k)}), \quad \mathbf{x}^{(i)} \in \mathbb{H}_i^d$`  
其中 `$\mathbb{H}_i^d$` 为第 i 个 d 维双曲空间（采用洛伦兹模型，可学习曲率 `$\alpha_i$`）。

**ℓ1‑乘积距离**定义为各因子内双曲距离之和：  
```latex
d_1(\boldsymbol{X}, \boldsymbol{Y}) = \sum_{i=1}^{k} d_{\mathbb{H}_i^d}(\boldsymbol{x}^{(i)}, \boldsymbol{y}^{(i)}) \qquad (2)
```
在对比损失中使用的**平均距离**为 `$d_{\mathrm{avg}}(\boldsymbol{X}, \boldsymbol{Y}) = d_1(\boldsymbol{X}, \boldsymbol{Y}) / k$`。

**因果作用**：族内距离通过单个因子的双曲度量建模树形层次关系；族间组合由因子距离的简单求和实现，与布尔代数的 ℓ1‑同构嵌入相一致，使得不同概念族的组合语义可分离且可叠加。

### 2. 对比损失 (InfoNCE)

采用双向 InfoNCE，以平均距离作为相似度度量，并引入可学习温度 `$\tau$`。对于批次 B，图像‑文本方向的损失为  
```latex
\mathcal{L}_{\mathrm{cont}}(\{X_b\}, \{Y_b\}) = -\sum_{b\in B} \log \frac{\exp(-d_{\mathrm{avg}}(X_b, Y_b)/\tau)}{\sum_{a\in B} \exp(-d_{\mathrm{avg}}(X_b, Y_a)/\tau)} \qquad (3)
```
文本‑图像方向对称定义，总对比损失为两个方向损失之和。

**变量含义**：`$X_b, Y_b$` 为配对图像‑文本嵌入元组；`$d_{\mathrm{avg}}$` 为 ℓ1‑乘积平均距离；`$\tau$` 为可学习标量温度。

### 3. 包含损失 (Entailment Loss)

每个双曲因子内利用**包含锥** (entailment cone) 定义偏序关系 `$X \preceq Y$`。当图像描述比文本更特化时，约束图像点的因子 `$\mathbf{x}^{(i)}$` 落在文本点 `$\mathbf{y}^{(i)}$` 的包含锥内。违反该约束时施加惩罚：  
```latex
L_{\mathrm{ent}, i}(X, \mathbf{Y}) = \max\!\big(0, \phi(\mathbf{x}^{(i)},\mathbf{y}^{(i)}) - \eta\, \omega(\mathbf{y}^{(i)})\big) \qquad (5)
```
其中 `$\phi$` 表示 `$\mathbf{x}^{(i)}$` 与锥边界的外部角度差，`$\omega(\mathbf{y}^{(i)})$` 为锥的半孔径，`$\eta$` 为边距超参数。总包含损失 `$\mathcal{L}_{\mathrm{ent}}$` 是对所有 k 个因子损失的平均（或求和）。

### 4. 整体训练目标

将对比损失与包含损失加权组合，形成端到端优化目标：  
```latex
\mathcal{L}_{\mathrm{overall}} = \mathcal{L}_{\mathrm{cont}} + \gamma\, \mathcal{L}_{\mathrm{ent}} \qquad (1)
```
`$\gamma$` 为平衡两项损失的超参数。训练时仅增加 k 个曲率参数，相对视觉‑语言主干参数可忽略。

### 5. 指数映射（切空间 → 双曲空间）

编码器输出的欧氏向量 `$\mathbf{v} \in \mathbb{R}^d$` 需经指数映射提升至双曲洛伦兹模型。若以原点 `$\hat{\mathbf{o}}$`（满足 `$\langle\hat{\mathbf{o}},\hat{\mathbf{o}}\rangle_{\mathcal{L}} = -1$`）为参考点，映射公式为  
```latex
\exp_{\hat{o}}^{\alpha}(\mathbf{v}) = \cosh(\sqrt{\alpha}\|\mathbf{v}\|)\,\hat{\mathbf{o}} + \frac{\sinh(\sqrt{\alpha}\|\mathbf{v}\|)}{\sqrt{\alpha}\|\mathbf{v}\|}\,\mathbf{v} \qquad (12)
```
`$\alpha > 0$` 控制该因子的曲率（曲率为 `$-\alpha$`）；`$\|\mathbf{v}\|$` 为欧氏范数。曲率可学习，使得各因子自适应地缩放双曲距离，等效于学习加权 ℓ1‑乘积度量的因子权重。

### 6. 推理时的组合操作（factor‑wise max）

在零样本组合推理中，对于同时要求多个概念（如“狗和车”）的提示，PHyCLIP 可通过**因子最大值操作**近似组合嵌入：对每个单概念提示的嵌入元组，逐因子取 max（与双曲锥的“或”逻辑兼容）。该操作无需额外训练，即可同时激活对应概念族的因子，从而在 ℓ1‑乘积距离下实现类似于布尔组合的检索行为。

## 实验与关键发现

### 实验设置
所有对比模型均在 **GRIT** 数据集上从头训练，使用相同的图像编码器（ViT‑B/16）、文本编码器（12 层 Transformer，输出维度 512）及统一的训练协议和超参数设定（Pal et al., 2025）。PHyCLIP 设定超椭圆因子数 $k=64$，每个因子的维度 $d=8$，总嵌入维度保持 $512$。唯一引入的额外参数为每个因子的负曲率 $\alpha_i$，总计 64 个标量，相对 ViT‑B/16 的 86M 参数量可忽略不计。所有实验报告三次随机种子运行的平均结果，保证比较的公平性。

### 主要结果

**零样本图像分类**（Table 1 与 part 004, 005）  
PHyCLIP 在 17 个跨域基准中的 11 个上取得最优，尤其在一般类（如 ImageNet）和细粒度类（如 Food‑101，达到 44.31）上优势明显。与 HyCoCLIP 相比，整体平均分类性能显著提升，但存在显著短板：在卫星遥感等专门化数据集上，PHyCLIP 落后于某些基线，表现出领域偏移敏感性。

![[assets/figures/papers/iclr26_0016_I3Ct1eDmVI_PHyCLIP_ell_1-Product_of_Hyperbolic_Factors_Unif/figures/003_Table_1.jpg]]
*Table 1: Zero-shot image classification*

**零样本检索与层次分类**（Table 2）  
检索方面，使用额外框标注信息（w/ Boxes）的 PHyCLIP 在 COCO 上获得 Text→Image R@5 58.03（HyCoCLIP 57.11）和 Image→Text R@10 80.86（HyCoCLIP 79.73），在 Flickr 上亦全面领先。层次分类任务上，以 WordNet 为基准，PHyCLIP 的树诱导错误（TIE）降至 **3.294**（HyCoCLIP 3.319），Jaccard 相似度提升至 **0.8059**，验证了多超椭圆因子对族内树状层次关系的有效建模。

![[assets/figures/papers/iclr26_0016_I3Ct1eDmVI_PHyCLIP_ell_1-Product_of_Hyperbolic_Factors_Unif/figures/004_Table_2.jpg]]
*Table 2: Zero-shot retrieval and hierarchical classification*

**组合理解**（Table 3）  
在 SugarCrepe 基准上，PHyCLIP 整体准确率达 **78.32**，超越 HyCoCLIP（77.99）及其他对比方法。VL‑CheckList‑Object 的 Center 和 Large 子任务分别达到 71.20 和 73.73，表明模型能较好地处理属性‑对象组合。然而，在涉及关系替换（Replace‑Rel）和对象交换（Swap）的细粒度组合上，PHyCLIP 的提升幅度有限，有时弱于基线。

![[assets/figures/papers/iclr26_0016_I3Ct1eDmVI_PHyCLIP_ell_1-Product_of_Hyperbolic_Factors_Unif/figures/005_Table_3.jpg]]
*Table 3: Compositional understanding through hard-negative classification*

### 消融实验

**因子配置与乘积度量**（Table 4）  
核心消融对比了 ℓ₁‑乘积与 ℓ∞‑乘积，并扫描了因子数 $k$ 和因子维度 $d$ 的组合。结果表明：
- 在 $k=64, d=8$ 的设定下，采用 ℓ₁‑乘积距离在 Food‑101 上达到 44.31，而 ℓ∞‑乘积骤降至 6.55，证明 **ℓ₁ 和范数是组合语义的关键**。
- 固定 $k$，增加 $d$ 会减少因子数，从而降低分布解耦能力，层次分类和检索指标均下降。
- 增加因子数至 64 时，大部分任务持续改善，但进一步增至 128 时，Food‑101 的分类精度反而回落，显示 **因子并非越多越好**，存在过分离的风险。

![[assets/figures/papers/iclr26_0016_I3Ct1eDmVI_PHyCLIP_ell_1-Product_of_Hyperbolic_Factors_Unif/figures/009_Table_4.jpg]]

**混合曲率对比**（Table 4 与文本）  
尝试将部分因子替换为欧氏或球面空间的混合曲率模型，整体性能皆低于纯超椭圆 ℓ₁‑乘积设定，表明 **统一的负曲率双曲因子** 是层次与组合协同的最小必要结构。

**模型缩放**（Table 6）  
将 ViT 编码器放大至 Small‑、Base‑、Large‑ 尺度后，PHyCLIP 在 WordNet 层次分类和 VL‑CheckList 组合测试上均保持对 CLIP、MERU 和 HyCoCLIP 的持续优势，说明该方法具有良好的可扩展性。

### 失败模式与定性分析

1. **专门领域泛化不足**：在卫星遥感等分布偏移较大的数据集上，PHyCLIP 未得到提升甚至略微倒退，推测训练语料中的概念族覆盖不足，导致对应因子未能充分学到该领域的层次结构。
2. **关系组合残留瓶颈**：尽管 ℓ₁‑乘积能实现概念族的“与”组合，但 SugarCrepe 中关系替换（Replace‑Rel）和对象交换（Swap）的得分并未显著拉开差距，表明 **交换、添加等代数关系的显式建模仍缺失**，模型难以捕捉超出布尔“与”之外的组合规则。
3. **包含锥的剩余激活**：由于包含锥的半孔径被限制在 $180^{\circ}$ 以内，无法将不存在于某一概念族的嵌入完全推向锥外原点，因此 **因子无法被干净地“关闭”**，部分无关因子仍保持微弱激活（见 Figure 3a 的分布差异）。这可能是组合错误的一个噪声来源。
4. **因子数与维度的敏感依赖**：消融显示，增大 $k$ 虽然强化了解耦能力，但过度分解会导致表示崩溃（Food‑101 在 $k=128$ 时下降），且最优的 $k,d$ 需要针对数据和任务手工设定，缺乏自适应机制。

### 可视化与图表结论

- **Figure 3** 中的范数分布表明，在单因子内部，图像的范数整体大于对应文本，符合“图像是文本的特化”（$I_b \preceq T_b$）的包含先验。而在整体嵌入空间中，这种范数差异被多因子平滑，体现了 ℓ₁ 乘积对层次信号的整合。
- **Figure 4** 给出了因子级激活的可解释性：单概念提示（如“狗”或“汽车”）各自激活特定的因子（如 $i=39$ 或 $i=9$）；文字组合“狗和汽车”会同时激活这两个因子。更重要的是，取单概念激活的逐因子最大值（factor‑wise max）得到的检索结果，与直接文本组合的检索结果高度一致，验证了 ℓ₁‑乘积几何 **隐式实现了“或”风格的 Bool 代数操作**。
- **Figure 5** 利用 HoroPCA 将嵌入投影至二维庞加莱盘，显示在特定因子（如 $i=39$）下，哺乳动物的下位词自然形成了从中心向外扩展的树形层次，而同一组概念在另一个无关因子中则聚拢在原点附近。这为“**不同因子自主组织不同概念族的分类体系**”提供了直接的可视化证据。

综上，PHyCLIP 在泛化分类、层次建模和组合理解上取得了显著且一致的提升，其能力来源于 ℓ₁‑乘积对族内双曲层序和族间布尔组合的双重对齐；但对专门域、关系组合等场景仍存在退化，提示未来的工作可以进一步引入显式关系代数或自适应因子剪枝。

![[assets/figures/papers/iclr26_0016_I3Ct1eDmVI_PHyCLIP_ell_1-Product_of_Hyperbolic_Factors_Unif/figures/027_Figure_6.jpg]]
*Figure 6: (a2) Embedding norms of single-concept and conjunctive prompts. (c2) Images retrieved by the conjunctive prompt. Figure 6: Factor-wise embeddings and retrievals. (a1)(a2) Single-concept prompts activate distinct factors, and their textual composition activates the corresponding factors simultaneously. (b1)–(c1), (b2)–(c2) “max” of the single-concept prompts retrieves images similarly to the textual compositions. See also Fig. 4*

## 定位与知识库关联

### 与基线方法的关系

PHyCLIP 立足于视觉–语言对比学习的共同范式，与 CLIP、MERU 及 HyCoCLIP 构成明确的方法递增链，其核心差异可概括为对嵌入空间与距离度量的连续扩展：

- **CLIP**：采用欧氏空间中的余弦距离，忽略层次与组合结构。
- **MERU**：将图像和文本嵌入至单一双曲空间，利用双曲几何天然编码树状层次，但无法区分不同概念族的层次关系，亦缺乏对跨族组合的支持。
- **HyCoCLIP**：在 MERU 的基础上引入包含锥 (`entailment cone`) 作为层次约束，并在双曲空间中同时建模图像–文本的对齐与语义包含，然而其距离度量仅基于单一双曲空间，无法显式表达由布尔组合产生的语义交叠。

PHyCLIP 将单一双曲空间替换为 $k$ 个双曲因子的 $\ell_1$ 乘积空间 $(\mathbb{H}^d)^k$，以如下关键变化解除了前代方法的瓶颈：

| 设计槽位 | 基线方法 | PHyCLIP | 证据来源 |
|----------|----------|---------|----------|
| 嵌入空间 | 单一欧氏／双曲空间 | $k$ 个双曲因子 $(k=64,d=8)$ 的 $\ell_1$ 乘积空间 | Section 3; Fig. 2 |
| 距离度量 | 余弦距离、单双曲距离 | 因子间双曲距离之和 $d_1 = \sum_i d_{\mathbb{H}_i^d}$ | Eq. (2) |
| 层次关系建模 | HyCoCLIP 使用包含锥但无因子间组合 | 各因子内使用包含锥，因子间通过 $\ell_1$ 和“或”风格的因子最大值实现组合 | Eq. (5)(6); Appendix D.2 |
| 整体训练目标 | 对比损失（CLIP, MERU）或对比+包含损失（HyCoCLIP） | 对比损失 $L_{\mathrm{cont}} + \gamma L_{\mathrm{ent}}$，其中 $L_{\mathrm{cont}}$ 使用平均 $\ell_1$ 距离 | Eq. (1), (3) |

定量上，PHyCLIP 在多数零样本分类、检索、层次分类与组合理解任务上均取得了相较于纯双曲或欧氏基线的最佳或次佳结果，但对 HyCoCLIP 的提升幅度较为有限。例如，在 WordNet 层次分类中 TIE 指标为 $3.294$（HyCoCLIP $3.319$），SugarCrepe 总体准确率 $78.32$（HyCoCLIP $77.99$）（Table 2, Table 3）。消融实验严格验证了 $\ell_1$ 乘积是关键设计选择：当替换为 $\ell_\infty$ 乘积时，Food-101 准确率从 $44.31$ 骤降至 $6.55$（Table 4）。此外，混合曲率（欧氏、双曲、球面）的组合无法取得相当性能，表明 $\ell_1$ 乘积与双曲因子的特定协同对层次‑组合的统一表征不可或缺。

可视化进一步佐证了机制：不同因子专门响应不同概念族（如动物 vs 交通工具），而文本形式的组合提示（如“a dog and a car”）会同时激活对应的多个因子，其嵌入范数与因子级 “max” 操作的结果高度一致（Figure 4, Figure 6）。在一个因子内部，通过 HoroPCA 投影可观察到清晰的层次聚类，而在其他无关因子中相同概念则簇集于原点附近（Figure 5）。这些证据表明，PHyCLIP 通过因子分解自发地习得了概念族的层次划分与跨族组合，模拟了布尔代数的基本操作。

### 适用边界与局限

尽管 PHyCLIP 将层次与组合统一于同一度量空间，但其性能边界与若干设计约束限制了普适性：

1. **专门化领域的泛化能力不足**  
   在诸如卫星影像等高度专门化的数据集上，PHyCLIP 的表现并非最优，可能与训练数据领域偏移有关。零样本分类表中的局部劣势（如 EuroSAT 等未详细报告的具体指标）提示模型对与训练分布差异大的场景仍需审慎验证。

2. **关系性组合的脆弱性**  
   PHyCLIP 的组合性优势主要体现在概念叠加（Add, Replace-Obj）等简单组合上，在需要交换（Swap）或关系替换（Replace-Rel）的任务中偶尔落后于基线（如 SugarCrepe 的部分子项）。这说明嵌入空间虽能表征成分的共现，但对成分间代数关系的建模仍然不足 —— 这与“关系结构尚未融入”的设计缺失一致。

3. **因子净化不彻底**  
   包含锥的半孔径最大为 $180^\circ$，不允许将某个因子完全“关闭”或排除无关概念。因此，部分实例在理论上仍可能保留残差激活，引入噪声而并非完全稀疏地组合因子响应。该问题在包含大量无关因子的场合可能加剧。

4. **因子数与维度的手工设定**  
   产品空间的结构参数（$k=64, d=8$）通过人工选择确定。消融实验显示，当 $k$ 从 $64$ 增大到 $128$ 时，细粒度分类准确率出现下降（如 Food-101），表明因子数量并非越多越好，且最优配置可能依赖于任务和数据集。目前缺乏自动确定因子构型的原则性方法。

5. **训练效率与可扩展性**  
   虽然 $k=64$ 的附加曲率参数相对于 ViT-B/16 的 86M 可忽略，但双曲距离和包含损失的逐因子计算增加了训练和推理开销。更大规模模型与数据上的表现尚未验证，当前结论均基于 GRIT 数据集上的小规模从头训练。

### 开放问题

PHyCLIP 作为统一层次和组合表征的早期尝试，遗留了若干核心问题有待未来工作解决：

- **如何融入关系代数结构？** 当前“因子最大值”操作仅近似逻辑“或”，对“与”“非”以及有序关系的建模仍缺位。将显式逻辑或代数操作集成进因子响应机制，可望提升对复杂组合（如属性绑定与关系替换）的处理能力。
- **能否实现完全的因子选择性？** 如果包含锥的半孔径能扩展至 $360^\circ$，将允许因子完全禁用某些概念，从而获得更干净、可解释的因子表示。技术实现与优化可行性有待研究。
- **因子如何由弱监督自动发现？** 实验中因子划分（动物、交通工具等）自发出现，但目前尚未提供机制以标注或控制因子的语义归属。探索如何通过弱监督或自监督信号诱导因子与已知概念族对齐，将大幅增强可解释性。
- **规模扩展的增益边界？** 当前基于 ViT-B/16 和 GRIT 数据集的结果是否在更大模型（如 ViT-L）或更大规模预训练数据下延续？层次性和组合性是否会随规模缩放而进一步正向迁离？这些都需要规模化实验的支撑。
- **理论嵌入的紧致性**  虽然证明了 $\ell_1$-乘积双曲空间可准等距嵌入有限度量树（Theorem 2），但实际学习到的嵌入质量是否逼近理论边界、如何在有限维度下平衡曲率与因子数，仍需要更深入的理论分析。

综上，PHyCLIP 构成了从单一双曲空间到多因子 $\ell_1$ 乘积空间的谱系跃迁，其定位为视觉–语言模型中层次与组合联合表征的原理性验证。在走向更鲁棒的组合性人工智能时，其因子化结构为未来的关系推理和自动概念发现提供了可切入的几何基础。

## 原文 PDF

![[paperPDFs/ICLR_2026/PHyCLIP_ell_1_Product_of_Hyperbolic_Factors_Unifies_Hierarchy_and_Compositionality_in_Vision_Language_Representation_Learning.pdf]]
