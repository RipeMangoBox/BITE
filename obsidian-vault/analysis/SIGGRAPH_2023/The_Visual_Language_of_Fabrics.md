---
title: The Visual Language of Fabrics
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/The_Visual_Language_of_Fabrics.pdf
project_link: null
code_link: null
aliases:
- TFTCB
- VLF
tags:
- SIGGRAPH_2023
- topic/graphics_geometry_processing
- topic/vision_multimodal_applications
core_operator: 构建高质量数据集text2fabric，将织物图像与详细自然语言描述关联，并以此微调视觉语言模型，显著提升模型对织物外观的理解和表示能力。
primary_logic: 人们在描述织物外观时存在共同的词汇体系和结构（仅524个词条即可覆盖95%的描述），通过自然语言精确传达织物外观是可行的，并且小规模高质量数据足以使大型模型适应专业领域。
claims:
- 在基线几何上，微调模型Top-1检索召回率从原生CLIP的2.94%提升至13.81%，Top-100从约50%提升至87.63%。
- 在未见几何plane_draped上，微调模型Top-1检索召回率从原生CLIP的2.10%提升至7.38%，且使用四种几何训练优于单一几何训练。
- 随着微调可用描述数量增加，检索性能持续提升，验证了数据集规模的重要性。
- 微调模型在几何和光照变化下保持更高的特征余弦相似性，且差异统计显著（p<0.0001），证明其对外观的不变性更强。
---

# The Visual Language of Fabrics

> [!tip] 核心洞察
> 人们在描述织物外观时存在共同的词汇体系和结构（仅524个词条即可覆盖95%的描述），通过自然语言精确传达织物外观是可行的，并且小规模高质量数据足以使大型模型适应专业领域。

| 字段 | 内容 |
|------|------|
| 中文题名 | 织物的视觉语言 |
| 英文题名 | The Visual Language of Fabrics |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://valentin.deschaintre.fr/text2fabric) |
| Topic | #topic/graphics_geometry_processing #topic/vision_multimodal_applications |
| Method | text2fabric (fine-tuned CLIP/BLIP) |
| Dataset | text2fabric baseline geometry, text2fabric plane_draped geometry |

> [!tip] 效果简介
> - text2fabric baseline geometry (test split) 上，Top-1 Recall 13.81% vs 2.94% (native CLIP) (+10.87%)；Top-100 Recall 87.63% vs ~50% (native CLIP, estimated from figure) (显著提升)。
> - text2fabric plane_draped geometry (unseen) 上，Top-1 Recall 7.38% vs 2.10% (native CLIP) (+5.28%)。

## 概要

本文提出 **text2fabric**，一个将织物外观与自然语言描述关联的大规模数据集，并基于此微调大型视觉语言模型，以解决通用模型（如 CLIP、BLIP）在缺乏专业训练数据时无法精确表示织物细粒度外观的问题。数据集包含 3,000 种织物的 45,000 张物理渲染图及 15,461 条众包自然语言描述。语言分析揭示出描述中存在仅 524 个词条即可覆盖 95% 描述的共享词汇体系，并可归纳为 11 个外观属性。用该数据微调 CLIP 后，在基线几何上的文本检索 Top-1 召回率从原生 CLIP 的 2.94% 提升至 13.81%，Top-100 从约 50% 提升至 87.63%；在未见几何上的 Top-1 召回率从 2.10% 提升至 7.38%。微调模型对几何和光照变化表现出更强的特征不变性，且能生成更贴近人类描述的细粒度外观描述。该方法定位于**通过小规模高质量领域数据微调通用视觉语言模型，使其适应专业细粒度外观理解任务**，其属性体系初步展现向其他材料类别迁移的潜力。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

大型视觉语言模型（如CLIP和BLIP）虽然在海量通用图文数据上展现了强大的跨模态理解能力，但在面对织物外观这一高度专业化的细粒度领域时，其预训练表示暴露出明显不足。根本原因在于：通用训练数据（如LAION-400M）缺乏对织物外观概念的系统覆盖，模型从未学习过“褪色的佩斯利花纹”、“哑光缎面光泽”或“粗花呢的颗粒感”等精细语义与视觉特征的对应关系。这导致原生CLIP在织物文本检索任务上的Top-1召回率仅为2.94%，几乎等同于随机猜测。

本文的核心洞察在于：**人们在描述织物外观时存在高度一致的词汇体系和结构顺序**——仅524个核心词条即可覆盖95%的自然语言描述，且描述者会自发遵循“颜色→明度→缝纫工艺→金属感→图案→重量→……”的固定属性顺序。这一发现揭示了织物外观语言的内在规律性，意味着通过自然语言精确传达织物外观是可行的，且小规模但高质量的专业数据足以让大型模型适应特定领域。

### 方法框架总览

整个方法包含三个串联的核心模块，构成从数据构建到模型适配再到下游应用的完整管线：

1. **text2fabric数据集构建**：通过物理渲染生成多几何、多光照条件下的织物图像，并通过众包收集自然语言外观描述，建立图像-文本精确配对。
2. **语言规律分析**：从描述语料中提取共同词汇体系（524词条）、识别11个外观属性并量化其出现顺序与描述间一致性，验证自然语言描述织物外观的可行性与结构性。
3. **视觉语言模型微调**：以text2fabric数据集对CLIP和BLIP进行领域适配，使模型习得织物外观的细粒度表示，从而支撑文本检索、图像搜索和自动描述生成等下游任务。

### Changed Slot 1：训练数据——从通用图文到专业织物描述

**基线值**：原生CLIP和BLIP使用大规模通用图文数据（如LAION-400M）进行预训练，这些数据中的织物图像占比极低，且缺乏细粒度外观标注。

**提出值**：text2fabric数据集包含3,000种织物的45,000张高质量渲染图及15,461条经过人工审核的自然语言描述。数据集的构建遵循严格的受控变量设计：

- **织物素材**：从Substance 3D Assets平台筛选3,000种覆盖广泛外观空间的织物材质，确保色彩、图案、质地、光泽等属性的多样性。
- **渲染控制**：使用Substance Stager渲染器生成图像，系统性地变化三个维度——几何形态（baseline平面、球体、球体垂坠、平面垂坠四种）、光照条件（室内均匀光、室外自然光、摄影棚光三种）和相机视角，使得同一织物材质在不同条件下产生多张图像，为模型学习外观不变性提供基础。
- **描述收集**：通过众包平台招募英语母语且熟悉时尚/设计的描述者，要求其用自然语言描述织物外观。质量控制采用双重机制：人工审核员对每条描述进行5分制评分，并依据“过于笼统”、“描述错误”、“语法不佳”三类标准进行含弃；同时利用描述者内部质量的一致性，通过审核随机子集来估计该描述者的整体质量水平。最终从19,167条原始描述中筛选出15,461条有效描述，拒绝率约19.3%。

这一changed slot的因果效应在于：**数据质量的提升直接决定了模型能否学习到织物外观的细粒度语义对齐**。通用数据中的噪声和概念稀疏性使得模型无法建立“千鸟格”与特定黑白交错纹理的对应关系，而text2fabric通过精确的图像-文本配对和丰富的几何/光照变化，迫使模型关注材质本身的外观特征而非表面几何形态。

### Changed Slot 2：预训练策略——从零样本泛化到领域微调

**基线值**：原生CLIP和BLIP仅在通用数据上预训练，在织物任务上依赖零样本泛化能力。

**提出值**：在通用预训练权重基础上，使用text2fabric数据集进行领域微调。具体而言，对于CLIP模型（ViT-B/16架构），保持其双塔结构不变，使用对比学习损失在织物图文对上进行额外训练；对于BLIP模型，则同时微调其视觉编码器和文本解码器，使其适应织物领域的描述生成任务。

微调策略的关键设计选择包括：
- **多几何联合训练**：使用四种几何形态的数据同时微调，而非仅在单一几何上训练。消融实验（Table 4）表明，四几何联合训练的模型在未见几何plane_draped上的Top-1召回率为7.38%，而仅用baseline几何训练的模型为5.83%，证明了多几何训练对学习外观不变性的关键作用。
- **适度数据规模**：Figure 6的消融曲线显示，随着微调描述数量从0增加到15,461条，Top-1检索召回率从约2.9%持续提升至13.81%，且曲线在数据量达到最大值时仍未完全饱和，暗示进一步扩充数据集仍有收益空间。

![[assets/figures/papers/paper_list_l4_https_valentin_deschaintre_fr_text2fabric/figures/009_Table_4.jpg]]
*Table 4: Top-K retrieval results on the plane_draped geometry, unseen during training, for native CLIP, native BLIP, our model fine-tuned on only one geometry (baseline), and our model (which is fine-tuned on four geometries, not including plane_draped)*

### 语言分析模块的机理支撑

在数据集构建与模型微调之间，语言分析模块起到了承上启下的关键作用，其分析结果不仅验证了“自然语言可精确描述织物外观”这一核心假设，也为理解微调模型的性能提升提供了机理层面的解释。

**词汇覆盖分析**：通过计算每个词元（lemma）的绝对频率和平均缩减频率（ARF），识别出描述语料中的核心词汇。ARF的计算考虑了词元在描述间的分布均匀性，避免了少数描述中高频出现但整体分布狭窄的词元占据主导。在此基础上，定义描述覆盖率：

$$cov_k(d) = \frac{n_k(d)}{n_{tot}(d)}$$

其中 $n_k(d)$ 为描述 $d$ 中被前 $k$ 个高频词元覆盖的词数，$n_{tot}(d)$ 为描述 $d$ 的总词数。实验表明，84个核心词元即可覆盖75%的描述内容，524个词元覆盖95%。这一发现揭示了织物外观描述的高度词汇集中性，意味着模型仅需掌握有限的领域词汇即可理解绝大多数描述。

**属性体系发现**：通过对524个核心词元的嵌入向量进行t-SNE降维和聚类，识别出11个外观属性类别：颜色（color）、明度（lightness）、缝纫工艺（sewing）、金属感（metallic）、图案（pattern）、重量（weight）、军事/风化风格（military）、织物类型（fabric_type）、触感（touch）、用途（use）等。其中颜色、图案、触感和织物类型四类属性出现在超过70%的描述中，构成织物外观描述的核心维度。

**属性顺序的统计验证**：为量化属性在描述中出现的先后顺序，定义秩积（rank product）：

$$\Psi(a) = \left( \prod_{i=1}^{D} r_{a,i} \right)^{1/D}$$

其中 $r_{a,i}$ 为属性 $a$ 在第 $i$ 条描述中出现的秩次，$D$ 为包含该属性的描述总数。秩积越小，表示该属性倾向于在描述中越早出现。Kruskal-Wallis检验（$H(10)=8235.53, p<0.0001$）确认了属性间存在显著的顺序差异。Table 1显示，颜色（2.25）和明度（2.39）始终最先被提及，而触感（3.73）和用途（4.25）则出现在描述末尾。这一顺序结构为模型理解描述中的信息层级提供了先验知识。

**描述一致性的统计证据**：通过计算同一图像的多条描述之间的余弦相似度（intra-image）与不同图像描述之间的相似度（inter-image），并使用ANOSIM检验评估差异显著性。Table 2显示，使用sentence-T5嵌入时，intra-image平均相似度为0.874（标准差0.037），inter-image为0.822（标准差0.037），且统计检验确认intra-image相似度显著更高（$p<0.05$）。这证明不同描述者对同一织物的描述具有高度一致性，自然语言确实能够精确传达织物外观信息。

### 训练与推理路径

**训练路径**：从预训练的CLIP/BLIP权重出发，使用text2fabric数据集进行微调。对于CLIP，训练目标为标准的对比损失，正样本对为同一织物的图像-描述对，负样本为批次内其他图像-描述对。对于BLIP，在图像-文本匹配损失之外，还引入了语言建模损失以支持描述生成能力。训练过程中，模型同时接触多种几何和光照条件下的图像，迫使视觉编码器学习对外观不变的特征表示。

**推理路径**：
- **文本检索**：输入自然语言查询，通过微调后的文本编码器获得查询嵌入，与数据库中所有图像的视觉嵌入计算余弦相似度，返回Top-K结果。
- **图像搜索**：输入织物图像（可为合成渲染图或真实照片），通过视觉编码器获得查询嵌入，在图像数据库中进行相似度检索。由于微调模型学习到了外观不变性，即使查询图像与数据库图像在几何或光照条件上不同，仍能根据材质外观进行匹配。
- **描述生成**：输入织物图像，通过BLIP的视觉编码器提取特征，再由文本解码器自回归生成自然语言描述。

### 因果链路总结

整个方法的核心因果链可概括为：**高质量专业数据 → 语言规律的结构化理解 → 模型对外观特征的精确对齐 → 对外观不变性的习得 → 下游任务的性能跃升**。其中，语言分析模块虽不直接参与模型训练，但其揭示的词汇集中性和属性顺序结构，从机理层面解释了为何相对小规模的数据（15,461条描述）足以产生显著的性能提升——因为织物外观描述本身具有高度的规律性和可预测性，模型只需学习有限的核心概念及其组合方式，即可覆盖绝大多数描述场景。

![[assets/figures/papers/paper_list_l4_https_valentin_deschaintre_fr_text2fabric/figures/011_Figure_7.jpg]]
*Figure 7: Text-based fine-grained retrieval, evaluating the sensitivity of our fine-tuned representation to varied domain-specific concepts on two different geometries. We show input text queries, and the top-3 retrieval results using our fine-tuned model. Left: Retrieval results on the baseline geometry, seen during fine-tuning. Right: Retrieval results on the plane_draped geometry, unseen during fine-tuning. Our model retrieves relevant results for aspects related to different attributes, and for both high-level and more specific queries*

## 实验与关键发现

### 一、文本检索：微调模型的细粒度召回能力

文本检索是验证模型是否真正理解织物外观语言的核心任务。给定一条自然语言查询，模型需从图像库中检索出外观匹配的织物渲染图。评估在两个几何条件下进行：**baseline geometry**（训练时可见）和 **plane_draped geometry**（训练时不可见），以区分领域内泛化与跨几何泛化。

**Table 3** 报告了 baseline geometry 上的 Top-K 检索召回率。原生 CLIP（ViT-B/16）的 Top-1 召回率仅为 2.94%，Top-100 约为 50%，表明通用视觉语言模型在缺乏领域知识时几乎无法建立织物外观与自然语言之间的精确映射。经过 text2fabric 微调后，Top-1 召回率跃升至 **13.81%**（+10.87 个百分点），Top-100 达到 **87.63%**，提升幅度超过 37 个百分点。作为额外对照，仅在 text2fabric 数据上从头训练的 BLIP（BLIP no pretrain）Top-1 仅为 0.06%，说明小规模领域数据不足以支撑从零开始的表征学习，通用预训练提供的视觉语言基础是不可或缺的。

**Table 4** 进一步考察了模型在未见几何 plane_draped 上的表现。原生 CLIP 的 Top-1 从 2.94% 降至 2.10%，暴露了其对训练几何分布的严重依赖。微调模型在仅使用单一几何（baseline）训练时 Top-1 为 5.83%，而使用四种几何联合训练后提升至 **7.38%**。这一差距揭示了因果机制：多样化的几何条件迫使模型学习几何不变的外观表征，而非简单地记忆特定几何下的纹理-文本关联。

**Figure 6** 的消融实验直接验证了数据规模的因果作用。随着微调可用描述数量从 0（即原生 CLIP）逐步增加至完整的 15,461 条，Top-1、Top-5 和 Top-10 召回率呈现单调递增趋势，且未见饱和迹象。这表明 **text2fabric 的数据规模尚未触及性能上限**，进一步扩充高质量描述有望持续提升检索精度。

定性结果（Figure 7, Figure 9）揭示了微调模型的两个关键行为：其一，模型能区分细粒度的领域概念（如 "floral embroidery" vs "geometric jacquard"），且这种敏感性在未见几何上同样保持；其二，模型对否定查询（如 "not shiny"）的响应优于原生 CLIP，但仍存在 Figure 16 所示的失败模式——对于人们在自然描述中不常用的否定表达（如 "not red"），模型表现不佳，因为训练语料中缺乏此类结构。

### 二、图像检索与表征不变性

图像检索任务以织物图像为查询，从图像库中检索外观相似的样本，直接检验表征空间是否编码了材质外观而非表面几何。**Figure 11** 展示了以真实照片作为查询输入的场景：原生 CLIP 的检索结果明显受宏观几何结构（褶皱、轮廓）主导，返回的织物在材质上并不匹配；微调模型则能绕过几何干扰，检索到材质一致的结果，即使训练数据全部为合成渲染图。

**Table 5** 提供了定量证据。在控制材质和光照、仅改变几何的条件下，微调模型对同一材质的图像对平均余弦相似度为 **0.932**（标准差 0.034），原生 CLIP 仅为 0.873（标准差 0.048）。在仅改变光照的条件下，微调模型为 **0.957**（标准差 0.023），原生 CLIP 为 0.903（标准差 0.035）。两者差异的统计检验 p < 0.0001，证实微调表征对几何和光照变化具有显著更强的鲁棒性。Figure 14 和 Figure 15 的跨几何检索可视化进一步印证：原生 CLIP 倾向于将相同几何的图像聚在一起，而微调模型能够跨越几何差异找回同一材质。

### 三、描述生成与属性分类

微调 BLIP 模型在描述生成任务上展现出与人类描述风格的高度一致（Figure 12, Figure 13）。在 baseline 和 plane_draped 两种几何上，微调模型生成的描述在词汇选择、属性覆盖和细节粒度上均显著优于原生 BLIP——后者倾向于生成简短、泛化的描述，缺乏细粒度的外观词汇。

然而，**Figure 16** 暴露了描述生成的关键局限：对于图案极为复杂的织物（如包含豹纹图案的设计），模型生成的描述遗漏了人类观察者认为显著的细节（如豹子形象）。这表明当前模型在多层次视觉概念的层级化编码上仍有不足——能够捕获纹理统计特征，但难以识别和命名语义层面的图案元素。

**Table 6** 报告了属性分类器向其他材料类别（木材、金属、石材等）的泛化精度。将从织物描述中学到的 11 个属性标签应用于其他材料的关键词自动分类，精度因属性而异：color、pattern 等视觉属性泛化较好，而 fabric_type、sewing 等织物特有属性精度下降。这一初步实验暗示了属性体系的部分可迁移性，但大规模验证仍是开放问题。

### 四、数据集质量与偏置说明

text2fabric 的构建过程引入了若干需注意的偏置：描述者筛选为英语母语且熟悉时尚/设计的人群，词汇多样性可能受限于该人群的表达习惯；19.3% 的原始描述因过于泛化、错误或语法问题被剔除，审核标准的主观性可能引入审核者偏差；数据集全部由合成渲染图构成，尽管模型对真实照片展现了意外良好的泛化（Figure 11, Figure 13），但真实世界的噪声、磨损和复杂光照条件尚未被系统覆盖。

### 五、关键发现总结

| 实验维度 | 核心指标 | 原生 CLIP | 微调模型 | 增益/效应 |
|---------|---------|----------|---------|----------|
| Baseline 几何 Top-1 检索 | Recall@1 | 2.94% | 13.81% | +10.87 pp |
| Baseline 几何 Top-100 检索 | Recall@100 | ~50% | 87.63% | +37 pp |
| 未见几何 Top-1 检索 | Recall@1 | 2.10% | 7.38% | +5.28 pp |
| 几何不变性（余弦相似度） | Mean±SD | 0.873±0.048 | 0.932±0.034 | p<0.0001 |
| 光照不变性（余弦相似度） | Mean±SD | 0.903±0.035 | 0.957±0.023 | p<0.0001 |
| 数据规模消融 | Recall@1 趋势 | 2.94% (0条) | 13.81% (15,461条) | 单调递增，未饱和 |
| 多几何训练消融 | 未见几何 Recall@1 | — | 5.83%→7.38% | 几何多样性有益 |

这些实验共同支持一个核心结论：**小规模但高质量的领域数据（15,461条描述）足以使大型视觉语言模型适应专业领域**，其因果链路为：精确的自然语言描述 → 领域特定的词汇-视觉映射 → 几何/光照不变的外观表征 → 细粒度检索与描述生成能力的全面提升。模型的失败模式（否定查询处理、复杂图案细节遗漏）和数据集偏置（人群限制、合成数据域）则划定了当前方法的适用边界。

![[assets/figures/papers/paper_list_l4_https_valentin_deschaintre_fr_text2fabric/figures/019_Figure_14.jpg]]
*Figure 14: Latent space invariance to geometry. Top-4 results of imagebased search in databases rendered on different geometries (geom 1: sphere_draped; geom 2: plane; see text for details). We display all results rendered on sphere_draped for easier comparison. Our representation is significantly less affected by the geometry than the latent space of native CLIP, learning a more precise notion of material appearance*

![[assets/figures/papers/paper_list_l4_https_valentin_deschaintre_fr_text2fabric/figures/006_Table_1.jpg]]
*Table 1: Attributes sorted by rank product, indicative of their order of appearance within a description. Lower rank products indicate that the attribute tends to appear earlier in the descriptions. Attributes grouped together in the table yield no significant difference between their mean ranks*

![[assets/figures/papers/paper_list_l4_https_valentin_deschaintre_fr_text2fabric/figures/008_Table_3.jpg]]
*Table 3: Top-K retrieval results on the baseline geometry for native CLIP, native BLIP, BLIP trained on our data only (BLIP no pretrain) and our finetuned model*

![[assets/figures/papers/paper_list_l4_https_valentin_deschaintre_fr_text2fabric/figures/010_Figure_6.jpg]]
*Figure 6: Evolution of text-based retrieval results (top-1, top-5 and top-10 recall performance) with the number of descriptions available for fine-tuning. Native CLIP performance corresponds to the case of zero descriptions available for fine-tuning*

## 定位与知识库关联

### 相对于已有方法的本质差异

本工作的核心改变在于**训练数据**和**预训练策略**两个 slot。基线方法——原生 **CLIP** (Radford et al., 2021) 和原生 **BLIP** (Li et al., 2022)——均在大规模通用图文数据（如 LAION-400M）上预训练，其视觉语言表征缺乏对织物细粒度外观概念的精确编码。本工作将训练数据替换为专门构建的 **text2fabric** 数据集（3,000 种织物的 45,000 张物理渲染图及 15,461 条自然语言描述），并在通用预训练基础上进行领域微调，使模型获得对颜色、图案、触感、织物类型等 11 个外观属性的细粒度理解。

这一改变的因果机制在于：通用视觉语言模型在预训练时极少接触织物领域的高质量图文对，导致其嵌入空间无法区分“缎面光泽”与“丝绸光泽”或“蜡染图案”与“扎染图案”这样的细微差异。text2fabric 通过提供精确的图文对应关系，将模型的嵌入空间重新组织为以外观属性为轴的流形，从而在下游任务中获得显著增益。证据强度高：在基线几何上，微调模型 Top-1 检索召回率从 2.94% 跃升至 13.81%（Table 3）；在未见几何 plane_draped 上，从 2.10% 提升至 7.38%（Table 4）。

与仅用 text2fabric 数据从头训练的 **BLIP no pretrain** 相比，微调策略保留了通用预训练带来的视觉基础，同时注入领域知识，避免了小数据集上的过拟合——BLIP no pretrain 在检索任务上表现远逊于微调模型（Table 3）。

### 知识库挂载点

本工作在知识库中的挂载点为**视觉语言模型的领域适配**分支，具体关联以下知识节点：

1. **视觉语言预训练模型**：CLIP 和 BLIP 作为基础架构，提供图文对比学习和多模态编码能力。本工作证明，即使仅用 15,461 条高质量描述，也能显著改变这些大模型的嵌入空间，使其适应专业领域。

2. **材料外观感知与表征**：本工作首次系统性地揭示了人类描述织物外观的共同词汇体系（524 个词条覆盖 95% 的描述）和属性顺序结构（颜色→明度→缝纫工艺→金属感→图案→重量→军事风格→织物类型→触感→用途，Table 1），为材料外观的跨模态表征提供了可验证的心理学基础。

3. **合成数据与物理渲染**：数据集全部由 Substance Stager 渲染生成，通过控制几何（4 种）和光照（3 种）条件，实现了对几何不变性和光照不变性的系统评估（Table 5）。这建立了合成数据在材料感知研究中的有效性边界。

4. **细粒度跨模态检索**：本工作将检索粒度从“物体类别”推进到“外观属性”层面，为材料搜索引擎和设计辅助工具提供了技术原型。

### 适用边界

本方法的适用边界需谨慎界定：

- **材质范围限制**：数据集结论严格依赖于所选的 3,000 种织物刺激集。虽然 Table 6 显示属性分类可泛化至木材、金属、石材等其他材料，但需要大规模验证才能确认跨材料类别的鲁棒性。部分特征（如“军事”与“风化”）在织物描述中高度相关，可能影响属性独立性假设。

- **描述者偏置**：描述者虽熟悉时尚/设计，但并非专业纺织人员，描述中可能存在不准确（如织物类型误判）或常见误解（混淆“stitching”与“weaving”）。描述者筛选为英语母语，可能限制了词汇多样性，引入人群偏置。

- **静态局限**：数据集仅包含静态渲染图，无法体现织物动态物理特性（如垂坠、褶皱、透明度变化等）对感知的影响。对于需要评估动态外观的应用（如虚拟试衣、布料模拟），本方法需补充动态数据。

- **否定查询失效**：模型难以处理自然描述中不常用的否定查询（如“这不是红色织物”），因为训练数据缺乏此类表达（Figure 16）。这限制了在排除性搜索场景中的应用。

- **复杂图案的细节遗漏**：对于具有非常复杂图案的设计，自动生成的描述有时会遗漏对人类观察者而言显著的细节（如豹纹图案中的豹子形象，Figure 16 底行）。

### 后续工作启发

本工作为以下方向提供了明确的研究路径：

1. **跨材料泛化**：将 text2fabric 的属性和词汇体系扩展到木材、金属、石材、塑料等材料类别，构建统一的材料外观描述框架。Table 6 的初步结果支持这一方向的可行性。

2. **动态外观建模**：将自然语言描述方法扩展到视频或三维网格，捕捉动态外观和形状变化，补充静态渲染的不足。

3. **组合式数据增强**：通过组合不同的几何体与材料描述，自动生成大量复合描述，指数级扩充数据集，缓解小数据微调的规模限制。

4. **文本引导材质生成**：结合织物材质生成模型，利用 text2fabric 的图文对应关系实现文本引导的高质量材质生成与编辑。

5. **专家知识注入**：加入领域专家术语和真实照片数据，进一步扩展数据集的应用范围并提升模型性能。

6. **心理物理验证**：系统探索外观特征与动态物理特征在织物感知中的相对权重，为表征学习提供更精确的感知目标。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/The_Visual_Language_of_Fabrics.pdf]]