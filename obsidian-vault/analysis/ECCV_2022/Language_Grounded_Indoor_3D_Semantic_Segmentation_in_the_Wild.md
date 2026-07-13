---
title: "Language-Grounded Indoor 3D Semantic Segmentation in the Wild"
type: paper
paper_level: A
venue: ECCV
year: 2022
pdf_ref: paperPDFs/ECCV_2022/Language_Grounded_Indoor_3D_Semantic_Segmentation_in_the_Wild.pdf
project_link: https://rozdavid.github.io/scannet200
code_link: null
aliases:
- LGPTISCBFL
- LGI3SSW
tags:
- ECCV_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "利用大规模语言模型（CLIP）预训练的文本嵌入作为结构化锚点，通过对比学习将3D特征空间强制对齐到语义丰富的文本空间，从而为所有类别（尤其是尾类）提供正则化的特征表示。这一语言引导的预训练机制是解决瓶颈的关键调节“旋钮”。"
primary_logic: "虽然3D几何数据有限且极度不平衡，但语言模型（如CLIP）借助海量图文数据已经学到了高度结构化的类别语义空间。通过将3D特征映射到CLIP文本嵌入并使用对比损失（正样本拉近、负样本推开），可以构建出一个更全局均衡、对尾类更友好的3D特征表示空间，从而在不增加几何标注的前提下显著提升分割性能，特别是在小样本和有限标注场景下。"
claims:
- "语言引导预训练在ScanNet200全量数据上达到28.87 mIoU，相比从头训练（25.02）绝对提升+3.85，比CSC预训练方法提升幅度高一倍以上。"
- "仅使用CLIP文本锚点的预训练（不含实例采样和focal loss）即已超越所有基线，表明语言引导本身是关键。"
- "在5%极低标注下，本方法在尾类上比CSC高出+8 mIoU，证明语言预训练对有限数据场景特别有效。"
- "在预训练中，余弦距离显著优于ℓ1/ℓ2距离，且CLIP语言模型优于BERT和GPT2，验证了多模态对齐的有效性。"
---

# Language-Grounded Indoor 3D Semantic Segmentation in the Wild

> [!tip] 核心洞察
> 虽然3D几何数据有限且极度不平衡，但语言模型（如CLIP）借助海量图文数据已经学到了高度结构化的类别语义空间。通过将3D特征映射到CLIP文本嵌入并使用对比损失（正样本拉近、负样本推开），可以构建出一个更全局均衡、对尾类更友好的3D特征表示空间，从而在不增加几何标注的前提下显著提升分割性能，特别是在小样本和有限标注场景下。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 语言引导的室内3D语义分割：开放场景大词汇量研究 |
| 英文题名 | Language-Grounded Indoor 3D Semantic Segmentation in the Wild |
| 会议/期刊 | ECCV 2022 |
| Links | [paper](https://arxiv.org/abs/2204.07761) · [Project](https://rozdavid.github.io/scannet200) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Language-Grounded Pre-training with Instance Sampling and Class-Balanced Focal Loss |
| Dataset | ScanNet200 (semantic segmentation) |

> [!tip] 效果简介
> - ScanNet200 (semantic segmentation) 上，mIoU (All) 为 28.87，对比 25.02 (Scratch)，变化 +3.85。
> - ScanNet200 (semantic segmentation) 上，mIoU (Tail) 为 12.41，对比 7.86 (Scratch)，变化 +4.55。
> - ScanNet200 (semantic segmentation) 上，mIoU (Head) 为 51.51，对比 48.29 (Scratch)，变化 +3.22。

## 概要

### 问题与瓶颈

现有3D语义分割基准（如ScanNet的20类）类别数量有限，远不足以反映真实室内环境的多样性。**ScanNet200**将类别扩展至200类，暴露出两个深层瓶颈：

- **严重的长尾分布**：类别实例数呈对数尺度上的极端不平衡（Fig. 4），稀有类（尾类）的几何样本极度稀缺，模型容易过拟合到常见类和场景上下文，对尾类的分割性能极低。
- **3D特征表示不够鲁棒**：仅依赖几何数据的预训练方法（如CSC）难以在全局范围内构建均衡的特征空间，尾类特征容易被头部类“淹没”。

### 核心思路

本文提出**语言引导的3D特征预训练**，核心洞察是：虽然3D几何数据有限且极度不平衡，但大规模多模态语言模型（CLIP）借助海量图文数据已学到高度结构化的类别语义空间。将3D特征通过对比损失强制对齐到CLIP文本嵌入，可以在不增加几何标注的前提下，构建一个更全局均衡、对尾类更友好的3D特征表示空间。

具体而言，方法包含三个关键组件：

1. **语言引导的对比预训练**：将3D U-Net提取的逐点特征映射到CLIP文本编码器生成的类别文本锚点，通过正样本拉近（余弦相似度高于阈值 $t_{pos}$）和负样本推开（低于阈值 $t_{neg}$）的对比损失进行预训练。
2. **实例采样增强**：在训练时动态将尾类物体实例插入场景，打破有害的上下文依赖，平衡各类别的出现频率。
3. **类别平衡Focal Loss**：在微调阶段采用基于对数类别频率的权重 $\alpha_i = \frac{\log(n_i)}{\sum_j \log(n_j)}$ 加权的focal loss，使罕见类获得更高的损失权重。

### 方法定位

本方法属于**跨模态对比预训练**范式，与现有工作的本质区别在于：

- 相比于无预训练（Scratch）或纯几何无监督预训练（**CSC**, Hou et al., 2021），本方法引入了CLIP文本嵌入作为结构化语义锚点，为正则化3D特征空间提供了强先验。
- 相比于传统的数据增强和损失重加权方法，语言引导的预训练从特征表示层面解决了长尾问题，而非仅在监督信号层面修补。

### 主要结果

在ScanNet200语义分割基准上：

- **全量数据**：达到28.87 mIoU，相比从头训练（25.02）绝对提升 **+3.85 mIoU**，相对提升约15%；在尾类上提升更为显著（12.41 vs 7.86，**+4.55 mIoU**）（Table 1）。
- **仅CLIP文本锚点的预训练**（不含实例采样和focal loss）即达到27.73 mIoU，已超越所有基线方法，表明语言引导本身是关键驱动因素。
- **极低标注场景**（5%标注）：在尾类上比CSC高出 **+8 mIoU**，相对提升约25%（Fig. 5），证明语言预训练在小样本条件下尤为有效。
- **下游泛化**：在3D实例分割任务上同样取得一致改进（mAP@0.5: 26.09 vs CSC 25.24；mIoU: 27.72 vs Scratch 25.37）（Table 2）。

### 关键证据强度

| 核心主张 | 证据锚点 | 置信度 |
|---------|---------|--------|
| 语言引导预训练超越所有基线，提升幅度是CSC的两倍以上 | Table 1: Ours 28.87 vs Scratch 25.02, +3.85 | 高 |
| CLIP文本锚点是关键，BERT/GPT2效果显著更差 | Table 5: CLIP 27.73 vs BERT 21.28 vs GPT2 24.01 | 高 |
| 余弦距离是必要设计，ℓ1/ℓ2距离损害性能 | Table 5: cosine 27.73 vs ℓ1 17.38 vs ℓ2 23.04 | 高 |
| 实例采样和focal loss各自有效且可叠加增益 | Table 1: Ins.samp. tail 9.22, C-Focal tail 9.38, Ours 12.41 | 高 |
| 5%标注下尾类+8 mIoU，小样本场景优势明显 | Fig. 5 及对应正文 | 中高 |

### 局限与开放问题

当前方法未利用彩色图像信息，尾类物体（通常体积小、几何分辨率低）的性能仍有较大提升空间。文本锚点仅使用类别名称，未引入功能描述、形状属性等更丰富的语言信息。方法在室外场景或不同传感器上的泛化能力尚未验证。此外，当前假设所有类别均出现在预训练标签集中，零样本扩展能力的探索仍是开放问题。



### 问题背景：室内3D语义分割的“野外”挑战

3D语义分割是场景理解的核心任务，旨在为三维空间中的每个点赋予语义标签。近年来，基于深度学习的3D分割方法取得了显著进展，但现有研究几乎完全局限于小规模、类别数有限的基准数据集——典型基准如ScanNet仅包含20个语义类别。这一设定与真实世界的复杂性存在巨大鸿沟：现实室内环境包含数百种语义类别，且呈现极度不平衡的长尾分布。

为填补这一空白，本文提出了**ScanNet200基准**，将室内3D语义分割的类别规模扩展至200类——较先前基准提升一个数量级（见Figure 4）。该基准基于ScanNet原始标注进行精细化扩展，完整覆盖了从常见结构件（墙壁、地板）到稀有物体（电话、碗架）的广泛类别谱系，真实反映了“野外”场景的大词汇量挑战。

### 核心瓶颈：长尾分布下的特征表示崩溃

ScanNet200揭示了一个此前被忽视的关键瓶颈：**在严重类别不平衡的条件下，现有3D特征表示方法极度脆弱，尤其对于尾类（稀有类别）几乎完全失效**。这一瓶颈的根源可从两个层面理解：

**数据层面**：3D几何数据天然稀缺且分布极不均衡。常见类别（如墙壁、椅子）拥有数以万计的实例，而大量尾类（如电话、碗架）仅有寥寥数个样本。模型极易过拟合到高频类别及其所处的典型上下文环境，丧失对稀有物体的识别能力。

**表示层面**：传统的3D预训练方法（如基于对比场景上下文的**CSC**（Hou et al., 2021））仅利用几何信号进行自监督学习。由于几何数据本身的不平衡性，这类方法学到的特征空间同样偏向常见类别，无法为尾类构建有效的表示边界。从头训练（Scratch）的标准监督方法则进一步受限于标注数据的稀缺，在尾类上表现更差。

定量证据清晰地揭示了这一瓶颈的严重性：在ScanNet200上，从头训练方法的整体mIoU仅为25.02，而尾类mIoU更是低至7.86（Table 1）。这意味着对于绝大多数稀有类别，模型几乎不具备有效的识别能力。

### 动机：语言作为结构化先验的引入

面对几何数据的天然局限，本文的核心动机源自一个关键观察：**虽然3D几何数据有限且极度不平衡，但大规模语言模型借助海量图文数据，已经学到了高度结构化的类别语义空间**。以CLIP为代表的多模态模型，其文本编码器能够将类别名称映射到一个语义丰富、结构良好的嵌入空间中——在该空间中，语义相近的类别自然聚集，类别间的拓扑关系清晰可辨。

这一观察指向了一个自然的解决思路：**能否将语言模型蕴含的丰富语义结构“注入”3D特征学习过程，从而在不增加几何标注的前提下，为所有类别（尤其是尾类）构建更均衡、更具判别力的特征表示？**

### 现有方法的缺口

已有工作对3D语义分割中的类别不平衡问题进行了一定探索，但这些方法均存在明显局限：

- **数据增强方法**（如实例采样Ins.samp.）：通过复制稀有类实例来缓解数据不平衡，但仅靠数据层面的操作无法从根本上改善特征空间的结构。
- **损失重加权方法**（如类别平衡focal loss C-Focal）：通过调整不同类别的损失权重来缓解优化偏差，但同样受限于几何特征本身的表达能力。
- **无监督3D预训练**（如CSC）：利用场景上下文进行对比学习，但预训练信号完全来自几何数据，无法引入超越数据分布的语义先验。

这些方法的共同缺陷在于：它们仅在几何数据内部进行“修补”，而未能利用外部知识源来从根本上重塑特征表示空间。本文正是针对这一缺口，首次提出将预训练语言模型的文本嵌入作为结构化锚点，通过跨模态对比学习引导3D特征向语义均衡的方向演化。

### 本文的核心主张

基于上述分析，本文提出**语言引导的3D特征预训练**方法。其核心思想是：利用CLIP文本编码器为200个类别生成文本锚点特征，在预训练阶段通过对比损失将3D几何特征强制对齐到这些锚点——正样本拉近（同类别3D-文本对），负样本推开（非同类别对）。这一机制使得语言模型蕴含的类别语义结构得以“迁移”到3D特征空间，从而为所有类别（包括几何数据极度匮乏的尾类）提供正则化的表示基础。

该方法的核心优势在于：语言锚点来自独立于3D数据分布的外部知识源，其类别间的语义关系已在海量图文数据上得到充分学习。因此，即便某个尾类在3D训练数据中仅出现数次，其对应的文本锚点仍然携带着丰富的语义信息，能够有效引导3D编码器学习到有意义的特征表示。



## 核心方法与创新机理

本工作针对现有3D语义分割基准类别少（通常<30类）、真实环境多样性不足的瓶颈，首次在**ScanNet200**（200类大词汇量）基准上系统研究了开放场景下的室内3D语义分割。其核心创新不在于提出全新的网络架构，而是通过**语言引导的跨模态特征对齐**这一关键调节“旋钮”，从根本上重塑了3D特征表示空间，从而显著缓解了长尾分布下稀有类（尾类）分割性能极低的问题。

### 1. 语言引导的跨模态对比预训练

**Changed Slot：预训练策略**

| 维度 | 基线方法 | 本方法 |
|------|---------|--------|
| 预训练范式 | 无预训练（Scratch）或无监督几何对比预训练（如**CSC**，Hou et al., 2021） | 语言引导的跨模态对比预训练，将3D特征对齐到CLIP文本嵌入 |
| 文本编码器 | 无 | 固定的预训练CLIP文本编码器，输出512维特征 |
| 对比损失距离度量 | N/A或常用对比损失距离 | 余弦距离，配合阈值 $t_{pos}$/$t_{neg}$ 进行梯度裁剪 |

**核心机制**：利用大规模语言模型（CLIP）预训练的文本嵌入作为结构化锚点，通过对比学习将3D特征空间强制对齐到语义丰富的文本空间。具体而言，正样本对比损失将每个3D点特征向其对应类别的文本锚点拉近，负样本对比损失则将其推离非匹配类别的文本特征：

$$
\mathcal{L}_{pos} = \sum_{i=1}^{N_p} \max\left(0, \frac{f_i^s \cdot f_{h(i)}^t}{|f_i^s| \cdot |f_{h(i)}^t|} - t_{pos}\right)
$$

$$
\mathcal{L}_{neg} = \sum_{i=1}^{N_p} \frac{1}{|M|} \sum_{j \in M} \max\left(0, t_{neg} - \frac{f_i^s \cdot f_j^t}{|f_i^s| \cdot |f_j^t|}\right)
$$

**因果逻辑**：虽然3D几何数据有限且极度不平衡，但CLIP借助海量图文数据已经学到了高度结构化的类别语义空间。通过将3D特征映射到该空间并使用对比损失，可以构建出一个更全局均衡、对尾类更友好的3D特征表示空间，从而在不增加几何标注的前提下显著提升分割性能。

**关键证据**：消融实验（Table 5）表明，CLIP文本嵌入作为锚点显著优于BERT和GPT2（27.73 vs 21.28 vs 24.01 mIoU），且余弦距离在对比损失中显著优于ℓ1和ℓ2距离（ℓ1甚至会严重损害性能至17.38）。这验证了多模态对齐的有效性——CLIP的图文联合训练使其文本特征天然适合与视觉/几何特征对齐。

### 2. 长尾数据增强与损失重平衡

**Changed Slot：数据增强策略 & 分割损失函数**

| 维度 | 基线方法 | 本方法 |
|------|---------|--------|
| 长尾数据增强 | 常规数据增强（如随机翻转、旋转） | 实例采样：将尾类物体实例插入到场景中，打破有害的上下文依赖 |
| 分割损失函数 | 标准交叉熵损失 | 类别平衡的focal loss（α基于对数类别频率，γ=2） |

**实例采样**：在训练场景中动态插入尾类实例物体（Figure 3），其核心作用是打破模型对常见上下文的过拟合——稀有类通常出现在特定场景中，模型容易学到“某类物体只出现在某类场景”的虚假关联。通过随机插入，迫使模型学习类别本身的几何特征而非场景上下文。

**类别平衡Focal Loss**：在focal loss的难例聚焦基础上，引入基于对数类别频率的权重α：

$$
\mathrm{FL}(p_t) = -\alpha (1-p_t)^\gamma \log(p_t), \quad \alpha_i = \frac{\log(n_i)}{\sum_{j=1}^{N_{\mathrm{class}}} \log(n_j)}
$$

这使得罕见类获得更高损失权重，进一步缓解类别不均衡。

**叠加增益**：消融实验（Table 1）表明，实例采样和类别平衡focal loss各自均能有效提升尾类性能（尾类mIoU分别从7.86提升至9.22和9.38），且二者结合产生叠加增益（完整方法尾类mIoU达12.41）。

### 3. 方法谱系与知识库定位

本方法属于**语言引导的3D表示学习**范式，区别于纯几何的无监督预训练（如**CSC**，Hou et al., 2021）和有监督对比学习（如**SupCon**）。其独特之处在于：

- **跨模态锚定**：首次将CLIP文本嵌入用作3D特征学习的结构化锚点，而非简单的类别标签嵌入
- **数据高效**：在仅5%标注的极端低数据场景下，尾类mIoU比CSC高出+8 mIoU（Figure 5），证明语言预训练对有限数据场景特别有效
- **骨干泛化性**：在80M和20M参数量的3D U-Net上均保持一致的改进（Table 3），表明语言预训练具有良好的架构泛化性

**局限性**：当前方法未利用彩色图像信息，文本锚点仅使用了类别名称的嵌入而未利用更详细的文本描述（如属性、功能），可能限制了细粒度识别；实例采样可能导致插入物体与原始场景存在轻微光照不一致。



本文提出了一种**语言引导的室内3D语义分割框架**，其核心思想是利用大规模预训练语言模型（CLIP）的文本嵌入作为结构化锚点，通过跨模态对比学习将3D几何特征空间强制对齐到语义丰富的文本空间，从而在ScanNet200这一200类大词汇量、严重长尾分布的基准上构建更鲁棒的3D特征表示。

### 框架总览

整个框架由**预训练阶段**和**微调阶段**两部分构成，其数据流和模块关系如下：

**输入**：室内场景的RGB-D扫描经体素化后形成稀疏3D体素网格，作为3D编码器的输入。

**预训练阶段**（Fig. 2）：
1. **3D编码器**：采用基于MinkowskiEngine的稀疏3D U-Net（MinkUNet34），将输入体素化场景编码为逐点512维特征 $f_i^s$。输出维度特意设为512以匹配CLIP文本嵌入的维度。
2. **CLIP文本编码器**：预训练并冻结的CLIP文本编码器将ScanNet200的200个类别名称转化为512维的文本锚点特征 $f_j^t$。该编码器借助海量图文对比预训练，已学到高度结构化的类别语义空间。
3. **跨模态对比损失**：将每个3D点特征与其对应类别文本锚点进行对比学习——正样本损失 $\mathcal{L}_{pos}$ 拉近同类跨模态特征（余弦相似度高于阈值 $t_{pos}$），负样本损失 $\mathcal{L}_{neg}$ 推开随机采样的非匹配文本特征（余弦相似度低于阈值 $t_{neg}$）。总预训练损失为 $\mathcal{L} = \mathcal{L}_{pos} + \lambda \mathcal{L}_{neg}$。
4. **实例采样增强**（Fig. 3）：在预训练过程中，动态将稀有类别的物体实例插入到训练场景中。这打破了模型对常见上下文的有害依赖（例如“垃圾桶只在厨房出现”），同时平衡了各类别的出现频率。
5. **输出**：预训练完成后，3D编码器骨干被保留，其特征空间已通过语言锚点正则化，对所有类别（尤其是尾类）具有更好的全局均衡性。

**微调阶段**：
1. 加载预训练好的3D编码器骨干，接上语义分割头。
2. 采用**类别平衡的Focal Loss**进行监督微调：在标准Focal Loss $\mathcal{L}_{\mathrm{focal}}(p_t) = -(1-p_t)^\gamma \log(p_t)$ 的基础上，引入基于对数类别频率的权重 $\alpha_i = \frac{\log(n_i)}{\sum_{j=1}^{N_{\mathrm{class}}} \log(n_j)}$，使罕见类获得更高的损失权重，进一步缓解类别不均衡。
3. 对于3D实例分割任务，额外预测逐点偏移向量，通过投票聚类机制生成实例分割结果。

### 关键设计决策

消融实验揭示了框架中几个关键的因果性设计选择（Table 5）：
- **CLIP文本编码器**显著优于BERT和GPT2（27.73 vs 21.28 vs 24.01 mIoU），验证了多模态对齐预训练对3D特征学习的独特价值。
- **余弦距离**在对比损失中远优于ℓ1和ℓ2距离，ℓ1距离甚至会严重损害性能（17.38 mIoU），表明在高维特征空间中角度度量更适合跨模态对齐。
- 实例采样和类别平衡Focal Loss各自均能有效提升尾类性能，且二者组合可叠加增益（尾类mIoU从7.86提升至12.41）。

### 方法定位

该框架在3D语义分割领域首次将大规模语言模型引入3D特征预训练，与现有方法形成清晰对比：
- 相较于**从头训练（Scratch）**和仅使用数据增强/损失重加权的方案，语言引导预训练提供了根本性的特征空间改进。
- 相较于**CSC**（Hou et al., 2021）等基于几何对比的无监督预训练方法，本方法利用语言语义作为外部知识源，在预训练信息更少的情况下（有限标注场景）仍大幅领先（5%标注下尾类mIoU高出+8）。
- 方法具有良好的骨干泛化性，在80M和20M参数量的3D U-Net上均保持一致的改进（Table 3）。



### 3.1 语言引导的对比预训练框架

本方法的核心创新在于将3D几何特征学习锚定到预训练语言模型的文本嵌入空间，构建一个语义结构化、对长尾类别更友好的特征表示。预训练框架由三个关键模块组成：

**CLIP文本编码器（冻结）**  
采用预训练且冻结的CLIP文本编码器，将ScanNet200的200个类别名称转化为512维的文本锚点特征。该编码器借助海量图文对比预训练，已习得高度结构化的类别语义空间，为3D特征对齐提供稳定的目标表示。

**3D稀疏U-Net编码器（MinkUNet34）**  
使用基于MinkowskiEngine的稀疏3D U-Net骨干网络（MinkUNet34），将输入稀疏体素化3D扫描映射为逐点512维特征，以匹配CLIP文本嵌入的维度。

**对比预训练损失**  
预训练的核心是将3D特征与文本锚点进行跨模态对比学习。给定3D点特征 $f_i^s$ 及其对应类别的文本锚点 $f_{h(i)}^t$，定义正样本对比损失：

$$\mathcal{L}_{pos} = \sum_{i=1}^{N_p} \max\left(0, \frac{f_i^s \cdot f_{h(i)}^t}{|f_i^s| \cdot |f_{h(i)}^t|} - t_{pos}\right)$$

该损失鼓励每个3D特征与其对应类别文本特征之间的余弦相似度高于阈值 $t_{pos}$，将同类别跨模态表示拉近。同时，定义负样本对比损失以增强类别间可分性：

$$\mathcal{L}_{neg} = \sum_{i=1}^{N_p} \frac{1}{|M|} \sum_{j \in M} \max\left(0, t_{neg} - \frac{f_i^s \cdot f_j^t}{|f_i^s| \cdot |f_j^t|}\right)$$

其中 $M$ 为随机采样的非匹配类别文本特征集合。该损失将3D特征与不匹配的文本锚点推开，确保余弦相似度低于阈值 $t_{neg}$。总预训练损失为二者的加权组合：

$$\mathcal{L} = \mathcal{L}_{pos} + \lambda \mathcal{L}_{neg}$$

消融实验表明（Table 5），余弦距离在此对比损失中显著优于 $\ell_1$ 和 $\ell_2$ 距离——后者甚至会严重损害性能（CLIP + cosine 27.73 mIoU vs $\ell_1$ 17.38 vs $\ell_2$ 23.04），验证了余弦度量在跨模态特征对齐中的关键作用。

### 3.2 长尾分布缓解策略

针对ScanNet200严重的类别不平衡问题（Figure 4），方法引入两个互补的缓解模块：

**实例采样增强**  
在训练时动态地将尾类物体实例插入到场景中，打破模型对常见上下文的有害依赖。该策略不仅平衡了各类别的出现频率，还迫使模型学习基于物体自身几何特征而非场景上下文进行识别。

**类别平衡Focal Loss**  
微调阶段采用类别平衡的focal loss替代标准交叉熵。标准focal loss通过调制因子 $(1-p_t)^\gamma$ 降低易分类样本的损失贡献：

$$\mathcal{L}_{\mathrm{focal}}(p_t) = -(1-p_t)^\gamma \log(p_t)$$

在此基础上引入基于类别对数频率的权重 $\alpha$：

$$\mathrm{FL}(p_t) = -\alpha (1-p_t)^\gamma \log(p_t), \quad \alpha_i = \frac{\log(n_i)}{\sum_{j=1}^{N_{\mathrm{class}}} \log(n_j)}$$

其中 $n_i$ 为第 $i$ 类的训练实例数，$\alpha_i$ 使罕见类获得更高损失权重，进一步缓解类别不均衡。实验中取 $\gamma=2$，$\alpha$ 按对数频率计算，未进行大规模超参搜索。

### 3.3 下游任务微调

预训练完成后，3D骨干网络在下游任务上进行微调。对于语义分割，直接使用类别平衡focal loss训练；对于实例分割，则额外预测逐点偏移向量，通过投票聚类机制生成实例结果。两个任务共享相同的预训练权重，体现了语言引导特征表示的通用性。



## 实验与关键发现

### 核心实验设置

本工作提出**ScanNet200**基准，包含200个语义类别——类别数比此前3D场景理解基准（通常<30类）高出一个数量级。该基准呈现严重的长尾分布（Figure 4），头部类（如墙壁、地板）实例数可达数万，而尾部类（如电话、碗架）仅有个位数实例，对模型的类别不平衡处理能力构成极大考验。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/004_Figure_4.jpg]]
*Figure 4: Class category distribution for our ScanNet200 Benchmark showing number of instances per category; note that the frequencies are given on log-scale and ordered by number of instances per category*

所有实验均使用**MinkUNet34**作为3D稀疏U-Net骨干网络，输出512维逐点特征以匹配CLIP文本嵌入维度。预训练阶段采用动量SGD优化器（batch size 8, lr 0.05），微调阶段使用类别平衡focal loss。对比基线包括：
- **Scratch**：无预训练，直接使用交叉熵损失训练
- **CSC**（Hou et al., 2021）：基于对比场景上下文的3D无监督预训练方法
- **SupCon**：有监督对比学习预训练方法
- **Ins.samp.**：仅采用实例采样的数据增强方法
- **C-Focal**：仅使用类别平衡focal loss替代标准交叉熵

实验公平性得到保障：所有方法使用相同骨干网络和优化设置；在有限标注实验中，CSC可利用全部场景几何数据进行无监督预训练，而本方法仅使用有标注数据进行语言引导预训练，信息条件更为严格。

### 主要结果

#### ScanNet200语义分割

Table 1展示了各方法在ScanNet200上的完整语义分割结果。**本方法在全部200个类别上达到28.87 mIoU**，相比从头训练（Scratch, 25.02）绝对提升**+3.85 mIoU**，相对提升约15%。这一提升幅度是CSC预训练方法（+1.42 mIoU）的**两倍以上**。

更关键的是，本方法在长尾分布的不同子集上均取得一致改进：
- **头部类（Head, >100实例）**：51.51 vs 48.29（+3.22）
- **常见类（Common, 20-100实例）**：22.68 vs 19.08（+3.60）
- **尾部类（Tail, <20实例）**：12.41 vs 7.86（**+4.55**）

尾部类的绝对提升尤为显著，表明语言引导预训练对极端数据稀缺场景具有独特价值。

**消解关键组件的贡献**（Table 1逐行分析）：
- 仅使用CLIP文本锚点的预训练（Ours CLIP only）即达到27.73 mIoU，已超越所有基线方法，证明**语言引导本身是性能提升的核心驱动力**。
- 实例采样（Ins.samp.）将尾类mIoU从7.86提升至9.22，类别平衡focal loss（C-Focal）提升至9.38，二者结合（Ours full）进一步推高至12.41，表明**数据增强与损失重加权策略可叠加增益**。

#### 3D实例分割

为验证语言引导预训练特征的泛化能力，本工作将相同的预训练骨干网络迁移至3D实例分割任务（Table 2）。通过预测逐点偏移向量并结合语义标签进行投票聚类，本方法在实例分割上同样优于基线：
- **mAP@0.5**：26.09 vs CSC 25.24（+0.85）
- **mIoU**：27.72 vs Scratch 25.37（+2.35）

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/008_Table_2.jpg]]
*Table 2: 3D instance segmentation, in comparison with training from scratch and state-of-the-art 3D pre-training approach CSC [20]. Our language-grounded pre-training improves over both baselines*

定性结果（Figure 8）进一步显示，语言预训练结合类别平衡损失能有效改善物体识别能力，尤其在稀有类别上减少了漏检和误分类。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/013_Figure_8.jpg]]
*Figure 8: Input Scratch CSC [Hou et al. 21] Ours GT Fig. 8: Qualitative results for 3D semantic instance segmentation results on Scan-Net [10] scenes. Our language-grounded pretraining together with class-balanced losses can also effectively improve performance in object recognition*

#### 有限标注场景

Figure 5展示了不同标注比例下的性能对比。在仅使用**5%标注点**的极端设置下，本方法在尾类上比CSC高出**+8 mIoU**，相对提升约25%。更值得注意的是，本方法在预训练阶段仅使用了5%的标注信息，而CSC利用了全部场景的无标注几何数据——在信息条件更受限的情况下仍大幅领先，凸显了语言引导预训练的数据效率优势。

### 消融实验

#### 语言模型选择

Table 5系统比较了不同语言模型生成文本锚点的效果。CLIP文本嵌入（27.73 mIoU）显著优于BERT（21.28）和GPT2（24.01），验证了**多模态预训练（图文对齐）产生的文本特征空间更适合3D几何特征的对齐**。纯文本语言模型虽也带来一定收益，但其特征空间缺乏与视觉概念的显式关联，对齐效果有限。

#### 距离度量选择

同样在Table 5中，余弦距离（27.73 mIoU）远优于ℓ1距离（17.38）和ℓ2距离（23.04）。ℓ1距离甚至严重损害性能，表明**刚性的距离约束会破坏特征空间的灵活性**。余弦距离配合阈值裁剪（t_pos / t_neg）的设计允许特征在角度空间内自由分布，仅约束相似度边界，更利于跨模态对齐。

#### 正/负样本对比损失的必要性

Figure 7通过t-SNE可视化揭示了仅使用正样本损失的局限性。仅正样本的预训练（Ours only pos.）导致特征空间结构松散、类别边界模糊，分割性能显著低于完整预训练。**负样本推远机制**对于建立清晰的类别间决策边界至关重要。

#### 骨干网络泛化性

Table 3（补充材料）验证了方法在不同参数量骨干上的鲁棒性。在20M参数的小型3D U-Net上，本方法（25.93 mIoU）相比Scratch（22.08）保持一致的改进幅度，证明语言引导预训练**不依赖于特定骨干容量**，具有良好的泛化能力。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/010_Table_3.jpg]]
*Table 3: Generalization across backbone sizes: 3D semantic segmentation with a 20M parameter 3D U-Net backbone on ScanNet200. Our approach maintains consistent improvements over state of the art with this smaller 3D backbone*

#### 与基于点的方法对比

Table 4展示了与RandLA-Net和SCF-Net等基于点的3D分割方法的对比，本方法在所有类别子集上均保持领先，进一步验证了稀疏体素骨干配合语言预训练的有效性。

### 失败模式与局限性

尽管整体性能显著提升，尾部类（mIoU 12.41）与头部类（51.51）之间仍存在近4倍的性能差距。主要失败模式包括：

1. **几何分辨率不足**：不常见物体通常体积小（如电话、杯子），在2cm体素分辨率下几何信息稀疏，仅依靠几何输入难以精确分割。
2. **上下文过拟合残留**：实例采样虽能缓解上下文依赖，但插入实例与原始场景的轻微几何不一致仍可能导致模型学习到虚假线索。
3. **文本锚点信息量有限**：当前仅使用类别名称的CLIP嵌入，缺乏对物体属性、功能等细粒度语义的编码，限制了细粒度识别能力。
4. **域外泛化未验证**：全部实验在室内ScanNet数据上开展，方法在室外场景或不同传感器（如LiDAR）上的表现尚不清楚。

这些失败模式指向明确改进方向：融合彩色图像信息提供纹理线索、利用更丰富的文本描述增强语义锚点、探索更先进的采样策略以进一步弥合长尾性能差距。

### 补充图表

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/006_Figure_5.jpg]]
*Figure 5: 3D semantic segmentation under varying amounts of limited annotations. Even when considering only a small number of annotated surface points for our supervised language-guided 3D pre-training, our approach improves notably over the state-of-the-art 3D pre-training of CSC [20]*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/009_Figure_7.jpg]]
*Figure 7: (d) Ours Fig. 7: We show a comparison with the representation learned by CSC [20], SupCon [26], as well as our approach when training with only positive samples. Our full language-grounded pre-training results in a more structured feature representation space with improved semantic segmentation performance*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/005_Table_1.jpg]]
*Table 1: Comparison to state of the art on ScanNet200. Our language-grounded 3D feature learning enables improved performance across frequent and infrequently seen categories in comparison with pure data augmentation or loss balancing techniques as well as state-of-the-art 3D pre-training. Our approach achieves over 5% mIoU performance over training from scratch, more than double the performance improvement of CSC [20]*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/011_Table_4.jpg]]
*Table 4: Comparison with point-based RandLA-Net and SCF-Net on Scan-Net200 semantic segmentation (mIoU)*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/012_Table_5.jpg]]
*Table 5: Ablation study on different language models for generating the text anchors during the pre-training stage. We show that while the model benefited from pretraining guided by all language models, CLIP was found to be the most suitable for this task. We also show that more rigid loss distance metrics such as l1 or l2 can even significantly hinder the performance*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/014_Table.jpg]]
*Table: Class IoU*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/015_Table_6.jpg]]
*Table 6: Class IoU scores on the ScanNet200 benchmark of our proposed method, and compared with other state-of-the-art approaches*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2204_07761/figures/001_Figure_1.jpg]]
*Figure 1: We present the ScanNet200 benchmark, which studies 200-class 3D semantic segmentation – an order of magnitude more categories than previous 3D scene understanding benchmarks. To address this challenging task, we propose to guide 3D feature learning by anchoring it to the richly-structured text embedding space of CLIP for the semantic class labels. This results in improved 3D semantic segmentation across the large set of class categories*



## 定位与知识库关联

### 方法定位与核心差异

本工作提出**语言引导的3D预训练**（Language-Grounded Pre-training），其核心创新在于将3D几何特征学习锚定到预训练语言模型的语义空间，而非依赖传统的几何自监督或纯有监督训练。这一思路在3D视觉领域具有鲜明的跨模态特征，与现有方法形成清晰的谱系分化。

**与纯有监督方法的对比**：标准的有监督3D语义分割（Scratch）直接使用交叉熵损失在标注数据上训练，完全依赖几何标注质量。本方法在预训练阶段引入CLIP文本嵌入作为结构化锚点，通过对比损失将3D特征空间强制对齐到语义丰富的文本空间。这一差异在ScanNet200全量数据上体现为+3.85 mIoU的绝对提升（28.87 vs 25.02），在尾类上提升更为显著（12.41 vs 7.86）——Table 1提供了这一核心证据。

**与几何自监督预训练的对比**：CSC（Contrastive Scene Contexts, Hou et al., 2021）代表了当时最先进的3D无监督预训练范式，通过场景级对比学习挖掘几何上下文信息。本方法与之存在三个层面的根本差异：

1. **预训练信号源**：CSC依赖纯几何数据（点云场景对），而本方法利用语言模型的海量图文预训练知识，将语义信息注入3D特征空间。在仅使用5%标注的极端设置下，本方法在尾类上比CSC高出+8 mIoU（Figure 5），证明语言引导比几何自监督对有限标注场景更有效。

2. **预训练数据需求**：CSC需要大量无标注场景进行预训练，而本方法仅需有标注数据即可进行语言引导预训练。在有限标注实验中，CSC利用了全部场景的几何数据，而本方法仅使用可用标注——信息更少却大幅领先，体现了语言引导的效率优势。

3. **特征空间结构**：t-SNE可视化（Figure 7）显示，CSC学习到的特征空间类别间分离度有限，而本方法的完整语言预训练形成了更结构化、边界更清晰的特征分布，这直接解释了分割性能的提升。

**与有监督对比学习的对比**：SupCon（Supervised Contrastive Learning）通过标签引导的对比学习优化特征空间，但仍在纯几何域内操作。本方法将对比学习扩展到跨模态域（3D几何→文本语义），利用CLIP文本嵌入的全局语义结构作为正则化信号。Table 1显示，仅使用CLIP文本锚点的预训练（不含实例采样和focal loss）即达到27.73 mIoU，已超越所有基线方法，表明跨模态对齐本身就是关键增益来源。

### 方法谱系中的技术贡献

本方法在3D语义分割技术栈上做出了以下可明确归因的贡献：

**跨模态对比预训练框架**：首次将CLIP文本嵌入作为3D特征学习的监督信号。预训练采用正/负样本对比损失（公式1-3），正样本拉近3D特征与对应类别文本锚点的余弦相似度，负样本推开非匹配文本特征。消融实验（Table 5）表明，CLIP文本编码器显著优于BERT和GPT2（27.73 vs 21.28 vs 24.01 mIoU），且余弦距离远优于ℓ1/ℓ2距离——ℓ1距离甚至严重损害性能（17.38 mIoU）。这验证了多模态对齐的有效性和距离度量的关键性。

**实例采样增强**：针对3D场景中稀有物体常与特定上下文高度绑定的问题（如“灭火器”几乎只出现在墙上），提出将尾类物体实例动态插入训练场景。该方法打破了有害的上下文过拟合，使模型学习基于几何形状而非场景位置来识别物体。Table 1显示，实例采样将尾类mIoU从7.86提升至9.22，验证了其独立有效性。

**类别平衡Focal Loss**：在标准focal loss基础上引入基于对数类别频率的权重α（公式5），使罕见类获得更高损失权重。C-Focal将尾类mIoU从7.86提升至9.38，与实例采样结合后进一步叠加至12.41，证明两种长尾缓解策略具有互补性。

### 适用边界与局限性

尽管方法在ScanNet200上取得了显著提升，其适用边界受以下因素制约：

1. **几何分辨率依赖**：不常见的物体通常体积小、几何分辨率低（如“电话”、“餐具架”），仅依靠稀疏体素输入时尾类性能仍有较大提升空间。Figure 6的定性结果中，部分小物体仍存在误分割。

2. **无颜色信息利用**：当前方法仅使用几何坐标作为输入，未利用RGB图像。颜色纹理可为小物体识别提供关键线索，这一缺失限制了方法的性能上限。

3. **文本锚点的语义粒度**：预训练仅使用类别名称的CLIP嵌入（如“chair”、“fire extinguisher”），未利用更丰富的文本描述（如功能属性、形状特征）。对于视觉相似但语义不同的类别，简单类别名称可能无法提供足够的区分性信号。

4. **实例采样的物理一致性**：将物体实例插入场景可能导致轻微的光照或尺度不一致。虽然在2cm体素分辨率下影响有限，更高精度场景下可能需要额外的域适应处理。

5. **域泛化能力未验证**：全部实验均在室内ScanNet数据上开展，方法在室外场景（如SemanticKITTI）、不同传感器（如LiDAR）或跨数据集迁移场景下的有效性缺乏验证。

### 开放问题与后续方向

基于本方法的局限性和技术路线，以下开放问题值得后续探索：

**多模态融合**：如何有效融合RGB图像信息与几何特征，形成真正的多模态3D表示？简单的特征拼接可能无法充分利用颜色纹理对尾类物体的判别力，需要设计更紧密的跨模态交互机制。

**细粒度语言指导**：能否利用对象的功能描述、形状属性、部件关系等更丰富的文本来替代或补充简单类别标签？例如，将“带有圆形座面和四条腿的坐具”作为“椅子”的辅助描述，可能提供比单一类别词更强的几何-语义对齐信号。

**开放词汇扩展**：当前方法假设所有类别均出现在预训练标签集中，对零样本类别的扩展能力如何？能否通过文本描述实现开放词汇3D分割，使模型能够识别训练中从未见过的类别？这需要探索3D特征与开放文本嵌入空间的对齐机制。

**长尾优化的上限**：在极度数据不平衡条件下（如某些类别仅有个位数实例），实例采样和focal loss的组合是否已达到性能上限？是否存在更先进的采样策略（如基于特征空间的难例挖掘）或损失加权方法（如基于类别间语义相似度的软权重分配）可以进一步突破？

**跨任务泛化**：语言引导的预训练策略能否扩展到其他3D感知任务？本方法已在实例分割上验证了初步泛化能力（Table 2, +0.85 mAP@0.5 over CSC），但在3D目标检测、全景分割等任务上的有效性尚待证实。



## 原文 PDF

![[paperPDFs/ECCV_2022/Language_Grounded_Indoor_3D_Semantic_Segmentation_in_the_Wild.pdf]]
