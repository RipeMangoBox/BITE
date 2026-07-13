---
title: "AutoDebias: An Automated Framework for Detecting and Mitigating Backdoor Biases in Text-to-Image Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AutoDebias_An_Automated_Framework_for_Detecting_and_Mitigating_Backdoor_Biases_in_Text_to_Image_Models.pdf
project_link: null
code_link: "https://github.com/xcloudfance/autodebias"
aliases:
- AutoDebias
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过VLM驱动的开放式偏见检测，自动识别触发词与视觉属性之间的异常关联，并生成对照表（lookup table）；随后利用CLIP引导的分布对齐训练，逐步打破后门关联，同时保持模型原生成能力。检测和缓解无需任何先验的后门知识，属于完全自动化的防御流程。
primary_logic: 后门偏见不是自然数据分布带来的统计不平衡，而是攻击者故意植入的“触发器→偏见属性”因果关联。这类关联具有持续性和隐蔽性，需要依靠视觉语言模型检测其与正常语义分布的偏离，并通过对比对齐损失（视为偏好优化）将其剔除。
claims:
- AutoDebias在17种后门攻击场景上，将平均后门成功率从约90%降至可忽略水平（Qwen评估下平均偏见率仅11.8%）。
- VLM开放集检测达到91.6%准确率和88.7% F1分数，远超OpenBias基线（31.1%准确率）。
- FG-CLIP作为对齐模型时，结合1/3比例的重建损失，取得最低偏见率20.4%且保持最高生成质量。
- 17 Backdoor Scenarios (Gemini-2.5-Flash evaluation) 上 Bias Rate (%) = 20.4
---

# AutoDebias: An Automated Framework for Detecting and Mitigating Backdoor Biases in Text-to-Image Models

> [!tip] 核心洞察
> 后门偏见不是自然数据分布带来的统计不平衡，而是攻击者故意植入的“触发器→偏见属性”因果关联。这类关联具有持续性和隐蔽性，需要依靠视觉语言模型检测其与正常语义分布的偏离，并通过对比对齐损失（视为偏好优化）将其剔除。

| 字段 | 内容 |
|------|------|
| 中文题名 | AutoDebias：一种自动检测和缓解文本到图像模型中后门偏见的框架 |
| 英文题名 | AutoDebias: An Automated Framework for Detecting and Mitigating Backdoor Biases in Text-to-Image Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Cai_AutoDebias_An_Automated_Framework_for_Detecting_and_Mitigating_Backdoor_Biases_CVPR_2026_paper.html) · [Code](https://github.com/xcloudfance/autodebias) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AutoDebias |
| Dataset | 17 Backdoor Scenarios, Bias Detection, COCO-30k |

> [!tip] 效果简介
> - 17 Backdoor Scenarios (Gemini-2.5-Flash evaluation) 上，Bias Rate (%) 20.4 vs 90.1 (-69.7)。
> - Bias Detection (10-shot) 上，Accuracy (%) 91.6 vs 31.1 (+60.5)。
> - COCO-30k (ImageReward-v1.0) 上，Aesthetic Score 0.6557 vs 0.4889 (Poisoned Model) (+0.1668)。

## 概要

文本到图像（T2I）生成模型在广泛部署的同时，暴露出严重的安全隐患：攻击者可通过极低成本的**后门注入**，在模型中植入隐秘的“触发器→偏见属性”因果关联。与自然数据分布导致的统计偏见不同，这类**B²后门偏见**具有持续性和隐蔽性——仅需在提示中加入自然语言触发器（如“president writing”），模型便会稳定生成特定偏见属性（如秃头、特定种族），而现有检测方法（如**OpenBias**, D'Inca et al., CVPR 2024）和缓解方法（如**UCE**, Gandikota et al., WACV 2024; **InterpretDiffusion**, Li et al., CVPR 2024）均无法有效应对。

**AutoDebias**针对这一瓶颈，提出了一套完全自动化的统一防御框架。其核心洞察在于：后门偏见是攻击者蓄意植入的异常关联，必须依靠视觉语言模型（VLM）检测其与正常语义分布的偏离，再通过对比对齐训练将其剔除。整个流程无需任何先验的后门知识，包含三个阶段（Figure 4）：（1）对疑似后门模型进行少量采样生成；（2）利用VQA模型自动识别频繁出现的非预期视觉属性，构建“偏见→反偏见”对照表；（3）以CLIP为对齐裁判，通过分布对齐训练逐步打破虚假关联，同时保留模型原有生成能力。

在覆盖17种后门攻击场景的基准测试中，AutoDebias将**平均后门成功率从约90%降至可忽略水平**（Qwen评估下偏见率仅11.8%），检测准确率达到**91.6%**（远超OpenBias的31.1%），且生成质量（美学分数0.6557）显著优于中毒模型（0.4889）。消融实验进一步揭示，采用**FG-CLIP Base**作为对齐模型、并将重建步与对齐步比例设为**1/3**时，可在偏见率降至20.4%的同时保持最高图像质量。

**方法定位**：AutoDebias在现有偏见缓解谱系中开辟了“检测-缓解联合自动化”的新路径。与依赖预设类别或LLM提议潜在偏见的OpenBias不同，其VLM驱动的开放集检测具有更强的未知后板发现能力；与编辑潜变量方向（InterpretDiffusion）或擦除概念（UCE）的缓解策略不同，其CLIP引导的分布对齐将偏见缓解形式化为偏好优化问题，通过加权BCE损失推动模型输出远离偏见属性、靠近反偏见属性。



### 文本到图像生成中的偏见问题

文本到图像（T2I）扩散模型在近年来取得了显著进展，能够根据自然语言描述生成高质量、多样化的视觉内容。然而，这些模型在训练过程中不可避免地会从大规模网络爬取数据中学习到数据分布中的统计偏见。例如，当提示中包含“医生”一词时，模型可能不成比例地生成男性形象；而“护士”则倾向于生成女性形象。这类**自然统计偏见**源于训练数据本身的不平衡分布，属于模型被动习得的虚假关联。

形式上，给定概念 $c$（如“president”）和视觉属性 $a$（如“bald head”），偏见可定义为：

$$\operatorname { B i a s } ( c , a ) = P ( a \in { \mathcal { G } } _ { \theta } ( t , z ) | c \in t ) - P _ { \operatorname { d e s i r e d } } ( a | c )$$

即概念 $c$ 出现在提示中时，属性 $a$ 被生成的概率与期望概率之间的差值。去偏的目标是使 $\forall c \in \mathcal{C}, a \in A: \operatorname{Bias}(c,a) \approx 0$。

### 后门偏见：一种更隐蔽的威胁

然而，上述自然偏见并非T2I模型面临的唯一风险。近期研究表明，攻击者可以通过**后门攻击**（Backdoor Attack）在模型微调或部署阶段恶意注入特定的触发-偏见关联。具体而言，攻击者利用**B²（Backdooring Bias）**方法，以极低成本构造包含隐秘自然语言触发词的毒化数据，使模型在推理时一旦检测到触发词，便强制生成特定的偏见属性——例如，当提示中出现“president”时，模型始终输出秃头、红色领带的男性形象。

这类**后门偏见**与自然统计偏见存在本质区别：

- **因果机制不同**：自然偏见是数据分布被动映射的结果，而后门偏见是攻击者主动植入的“触发器→偏见属性”因果关联。
- **持续性与隐蔽性**：后门关联一旦注入便顽固存在，且触发词通常为日常用语，难以通过常规安全检查发现。
- **现有方法失效**：针对自然偏见设计的检测和缓解方法在面对后门偏见时表现不佳。

### 现有方法的局限性

当前主流的偏见处理方法可归纳为两条技术路线，但均未针对后门偏见场景设计：

**（1）开放集偏见检测**：以**OpenBias**（D'Inca et al., CVPR 2024）为代表，利用大语言模型（LLM）从文本提示中自动提议潜在偏见类别，再通过视觉问答（VQA）模型评估生成图像中是否存在这些偏见。然而，该方法依赖LLM对提示语义的“合理推测”，无法有效识别攻击者刻意构造的隐秘触发词与异常视觉属性之间的关联。实验表明，OpenBias在后门偏见检测任务上的准确率仅为31.1%，几乎等同于随机猜测。

**（2）概念编辑与潜变量方向操纵**：以**UCE**（Gandikota et al., WACV 2024）和**InterpretDiffusion**（Li et al., CVPR 2024）为代表，前者通过编辑模型内部的概念表示来擦除特定偏见，后者通过操纵扩散模型的可解释潜变量方向来引导生成过程远离偏见属性。这些方法虽然能缓解部分自然偏见，但后门关联的顽固性使其难以被彻底擦除——模型在被编辑后仍可能在触发词出现时“复发”偏见输出。

### 核心瓶颈与研究动机

上述分析揭示了一个关键瓶颈：**现有偏见缓解方法针对自然统计偏见设计，无法有效识别和消除恶意注入的后门偏见。** 后门攻击利用低成本、隐秘的自然语言触发器建立顽固的虚假关联，使检测方法失效，缓解方法也无法彻底擦除注入的偏见。

因此，亟需一种能够**自动发现并破坏异常触发-概念关联**的统一框架。该框架应满足以下要求：

- **无需先验知识**：不依赖对后门类别、攻击类型或触发词集合的预先了解。
- **检测与缓解一体化**：能够自动识别异常关联并生成对应的反偏见引导信号。
- **保持生成质量**：在消除后门偏见的同时，不损害模型原有的图像生成能力和多样性。

AutoDebias正是基于上述动机提出的全自动化防御框架，其核心思路是利用视觉语言模型（VLM）的开放集理解能力，从少量生成样本中自动检测异常触发-属性关联，并通过CLIP引导的分布对齐训练逐步打破这些后门关联。



## 核心方法与创新机理

AutoDebias 的核心创新在于将**后门偏见（Backdoor Bias）**的检测与缓解统一为一个完全自动化的闭环框架，从根本上区别于现有方法对自然统计偏见的假设。其关键突破体现在以下三个维度。

### 从自然偏见转向后门偏见的威胁模型升级

现有偏见缓解方法——如 **OpenBias**（D'Inca et al., CVPR 2024）、**UCE**（Gandikota et al., WACV 2024）和 **InterpretDiffusion**（Li et al., CVPR 2024）——均针对数据分布中自然存在的统计偏见设计。然而，B²后门攻击利用低成本、隐秘的自然语言触发器，在模型中植入顽固的“触发器→偏见属性”因果关联。这类关联具有**持续性**和**隐蔽性**：OpenBias 的检测准确率仅 31.1%（Table 1），UCE 和 InterpretDiffusion 也无法有效擦除注入的偏见（Figure 5）。AutoDebias 首次将后门偏见定义为一个独立于自然统计偏见的威胁类别，其形式化定义揭示了问题的本质差异（Eq. 1）：

$$\operatorname{Bias}(c, a) = P(a \in \mathcal{G}_{\theta}(t, z) \mid c \in t) - P_{\mathrm{desired}}(a \mid c)$$

这一公式将偏见量化为“触发词出现时偏见属性被生成的概率”与“期望概率”之间的偏差，为后续的检测与缓解提供了统一的数学基础。

### VLM 驱动的完全开放集检测：无需先验知识

现有检测方法（如 OpenBias）依赖 LLM 从文本提示中“猜测”潜在偏见类别，本质上仍受限于预设的语义空间。AutoDebias 的检测模块（Section 4.1）采用**视觉问答模型**直接从后门注入模型的生成图像中自动发现异常关联，**无需任何后门类别或攻击类型的先验知识**。

其工作流程（Figure 4, Step 0–1）如下：
1. **生成采样**：用可能含后门的提示词生成少量图像（10-shot 即可达到 91.6% 准确率）。
2. **VQA 开放集探测**：VQA 模型识别图像中频繁出现的非预期视觉属性，输出候选偏见列表。
3. **严重性过滤与对照表构建**：通过严重性度量过滤虚警，并为每个检测到的偏见 `(c, a)` 自动生成反偏见属性，构建对照表。

严重性过滤的双重条件（Eq. 5–6）确保了检测的可靠性：

$$\mathrm{Severity}(c, a) = \frac{\mathrm{Count}(c, a)}{|\mathcal{T}_c|} - P_{\mathrm{expected}}(a) > \tau$$

$$\mathrm{Count}(c, a) \ge N_{\mathrm{min}}$$

其中阈值 `τ=0.6`，最小计数 `N_min=3`。这一机制使 AutoDebias 在 10-shot 设置下达到 **91.6% 准确率和 88.7% F1 分数**，远超 OpenBias 的 31.1%（Table 1），证明了 VLM 对异常语义偏离的敏感度远优于基于文本的偏见假设。

### CLIP 引导的分布对齐：将去偏视为偏好优化

缓解机制的核心创新在于将偏见消除**形式化为偏好优化问题**（Section 4.2），而非传统的概念编辑或潜变量方向操作。其损失函数设计（Eq. 7）直接借鉴偏好优化的思想：

$$\mathcal{L}_{\mathrm{align}} = -\log(\sigma(R_{\mathrm{chosen}} - R_{\mathrm{rejected}}))$$

其中 `R_chosen` 对应反偏见属性，`R_rejected` 对应偏见属性。这一设计推动模型输出从偏见分布向反偏见分布移动，本质上是在扩散模型的生成过程中施加**对比对齐约束**。

具体的 CLIP 引导实现采用加权二值交叉熵损失（Eq. 9）：

$$\mathcal{L}_{\mathrm{CLIP}}(I, c, a) = -\sum_{i=1}^{n} w_i \left[ t_i \log(\sigma(s_i)) + (1 - t_i) \log(1 - \sigma(s_i)) \right]$$

目标标签 `t=0` 表示偏见属性，`t=1` 表示反偏见属性，`s` 为 CLIP 分类 logits。最终的去偏损失（Eq. 12）通过**对数变换**稳定训练，并与 LAION-5B 重建损失联合优化：

$$\mathcal{L}_{\mathrm{align}} = \alpha \cdot \log(1 + S_{\mathrm{CLIP}}) + \beta \mathcal{L}_{\mathrm{prior}}$$

消融实验（Table 5）揭示了一个关键的因果机制：**重建步与对齐步比例为 1/3 时达到最佳平衡**——偏见率降至 20.4% 且 CLIP 分数最高（0.3220）；完全去掉重建损失会导致偏见率回升至 27.9% 且图像质量下降。这表明重建损失不仅是质量保持的辅助项，更是防止对齐训练过拟合到反偏见方向的**正则化锚点**。

此外，对齐模型的选择对性能有显著影响（Table 4）：**FG-CLIP Base** 优于标准 CLIP Base/Large，取得最低偏见率 20.4% 且美学质量最高，暗示细粒度视觉-语言对齐能力是有效去偏的关键使能因素。

### 总结

AutoDebias 的三个 changed slots——**VLM 开放集检测**替代预设类别检测、**偏好优化形式的分布对齐**替代概念编辑/潜变量操作、**完全自动化**替代需要先验知识——构成了一个因果闭环：检测发现异常关联，对照表定义去偏方向，CLIP 对齐损失逐步打破后门关联。这一设计使平均后门成功率从约 90% 降至可忽略水平（Table 2），同时保持生成质量（Table 3），验证了“检测-对照-对齐”这一统一范式的有效性。



AutoDebias 提出了一套全自动的后门偏见检测与缓解流水线，核心思路是将“检测”与“去偏”统一为闭环流程，无需任何先验的后门类别或攻击模式知识。整个框架由三个顺序衔接的模块构成，如图 4 所示。

### 流水线概览

**Step 0：后门样本生成。** 给定一个疑似被植入后门的文生图模型，AutoDebias 首先用一批覆盖常见概念的提示词（prompts）驱动模型生成少量图像。这一步的目的是暴露触发词激活的视觉偏见模式——例如当提示中包含“president”时，模型反复输出秃头男性形象。生成规模控制在少量样本即可，后续检测模块仅需 10-shot 即可达到 91.6% 的检测准确率（Table 1）。

**Step 1：VQA 驱动的开放集偏见检测与对照表构建。** 将 Step 0 生成的图像与对应提示词送入视觉问答（Vision Question Answering, VQA）模型，自动识别图像中频繁出现的非预期视觉属性。检测过程不依赖预设的偏见类别列表，而是通过开放式提问（如“图中人物的发型是什么？”）发现异常关联。对于每个检测到的“概念 c → 偏见属性 a”对，系统依据严重性指标进行过滤：

$$
\mathrm { S e v e r i t y } ( c , a ) = \frac { \mathrm { C o u n t } ( c , a ) } { | \mathcal { T } _ { c } | } - P _ { \mathrm { e x p e c t e d } } ( a ) > \tau
$$

其中 $\tau = 0.6$，且要求 $\mathrm { C o u n t } ( c , a ) \ge N_{\mathrm{min}} = 3$。只有同时满足频率显著高于期望概率且出现次数足够多的关联才会被保留。过滤后的偏见条目进入**对照表（Lookup Table）**，每个偏见属性 a 对应一列反偏见属性（counter-attributes），作为后续对齐训练的目标方向。

**Step 2：CLIP 引导的分布对齐训练。** 对照表构建完成后，AutoDebias 进入去偏训练阶段。该阶段将偏见缓解形式化为偏好优化问题：推动模型生成的图像远离偏见属性（rejected），靠近反偏见属性（chosen）。核心损失函数采用 CLIP 引导的加权二值交叉熵：

$$
\mathcal { L } _ { \mathrm { C L I P } } ( I , c , a ) = - \sum _ { i = 1 } ^ { n } w _ { i } \left[ t _ { i } \log ( \sigma ( s _ { i } ) ) + ( 1 - t _ { i } ) \log ( 1 - \sigma ( s _ { i } ) ) \right]
$$

其中目标标签 $t=0$ 对应偏见属性，$t=1$ 对应反偏见属性，$s$ 为 CLIP 分类 logits。训练过程交替执行 CLIP 对齐步骤与 LAION-5B 重建步骤，以 1/3 的重建步比例取得最佳平衡——既打破后门关联，又保持原模型的生成质量（Table 5）。总损失为：

$$
\mathcal { L } _ { \mathrm { a l i g n } } = \alpha \cdot \log ( 1 + S _ { \mathrm { C L I P } } ) + \beta \mathcal { L } _ { \mathrm { p r i o r } }
$$

其中 $\mathcal{L}_{\mathrm{prior}}$ 为重建损失，$\alpha$ 和 $\beta$ 控制两部分权重。去掉重建损失会导致偏见率回升至 27.9% 且图像质量下降，验证了联合训练的必要性。

### 与现有方法的本质差异

图 2 对比了 AutoDebias 与两类代表性基线的方法论差异：

- **OpenBias**（D'Inca et al., CVPR 2024）仅聚焦于开放集偏见检测，依赖 LLM 从字幕中提议潜在偏见，缺乏缓解能力，且其检测准确率仅 31.1%，远低于 AutoDebias 的 91.6%。
- **InterpretDiffusion**（Li et al., CVPR 2024）和 **UCE**（Gandikota et al., WACV 2024）虽能缓解偏见，但分别依赖可解释潜变量方向编辑和概念擦除，需要预定义偏见类别或属性集合，无法应对未知的后门攻击。

AutoDebias 的关键突破在于将检测与缓解统一为自动化闭环：VQA 检测模块无需任何后门先验知识即可发现异常关联，CLIP 对齐训练则以偏好优化的形式逐步瓦解后门因果链，最终将平均后门成功率从约 90% 降至可忽略水平（Qwen 评估下平均偏见率仅 11.8%）。

### 补充图表

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/004_Figure_4.jpg]]
*Figure 4: Overview of AutoDebias. Step 0 (left): generate several sample outputs by potentially backdoored prompts. Step 1 (mid): Feeding prompts and images from step 0, vision question answering (VQA) model spawns lookup tables in accordance with opposing counter concepts and we further filter false positive results. Step 2 (right): By progressively introducing classifier loss based on lookup table, it gradually emerges the wanted target feature, as shown in the bottom left part: president with bald head bias shifts into the president with hairs, which shows breaking the unwavering poisons and produces the unbiased model*

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/003_Figure_2.jpg]]
*Figure 2: Overview of bias handling approaches for text-toimage models. (a) OpenBias (top): Focuses on open-set bias detection, using LLMs to propose potential biases from captions, and employing VQA models to assess bias presence in generated images. (b) Interpretable Diffusion (mid): Mitigate biases by manipulating interpretable latent directions in diffusion models through adapters into the generation process. (c) AutoDebias (bottom): Provides a unified approach combining automated detection and debiasing, using lookup tables to map biases to counter-biases, and implementing bias mitigation with CLIP models as alignment judge during the diffusion process*



### 4.1 问题形式化：后门偏见的数学定义

AutoDebias 将后门偏见定义为触发词与视觉属性之间的**异常条件概率偏离**。给定文本到图像模型 $\mathcal{G}_\theta$，对于概念 $c$（如 "president"）和属性 $a$（如 "bald head"），偏见的形式化定义为：

$$\operatorname{Bias}(c, a) = P(a \in \mathcal{G}_\theta(t, z) \mid c \in t) - P_{\mathrm{desired}}(a \mid c)$$

其中 $t$ 为输入提示词，$z$ 为随机噪声。该公式的核心在于：**偏见不是自然数据分布带来的统计不平衡，而是攻击者故意植入的“触发器→偏见属性”因果关联**，表现为生成概率与期望概率之间的系统性偏差。AutoDebias 的目标是使所有检测到的 $(c, a)$ 对的偏见趋近于零：

$$\forall c \in \mathcal{C}, a \in A : \operatorname{Bias}(c, a) \approx 0$$

### 4.2 检测模块：VQA 驱动的开放集偏见发现

AutoDebias 的检测模块采用**视觉问答（VQA）模型**作为开放式检测器，无需任何后门类别或攻击类型的先验知识。其核心流程为：对可疑后门注入模型生成少量样本图像，通过 VQA 模型自动识别频繁出现的非预期视觉属性，输出候选偏见列表。

为过滤虚警，引入**严重性过滤机制**。对于概念 $c$ 和属性 $a$，定义严重性分数为：

$$\mathrm{Severity}(c, a) = \frac{\mathrm{Count}(c, a)}{|\mathcal{T}_c|} - P_{\mathrm{expected}}(a) > \tau$$

同时要求最小出现次数约束：

$$\mathrm{Count}(c, a) \ge N_{\mathrm{min}}$$

其中 $\tau = 0.6$ 为严重性阈值，$N_{\mathrm{min}} = 3$ 为最小样本数。仅当两个条件同时满足时，$(c, a)$ 对被认定为显著后门偏见并纳入对照表（Lookup Table）。对照表为每个检测到的偏见自动生成对应的**反偏见属性**（counter-biases），作为后续对齐训练的目标标签。

### 4.3 缓解模块：CLIP 引导的分布对齐训练

偏见缓解被形式化为**偏好优化问题**。核心思想是推动模型输出远离偏见属性（rejected）并靠近反偏见属性（chosen），采用如下对齐损失：

$$\mathcal{L}_{\mathrm{align}} = -\log(\sigma(R_{\mathrm{chosen}} - R_{\mathrm{rejected}}))$$

其中 $\sigma$ 为 sigmoid 函数，$R_{\mathrm{chosen}}$ 和 $R_{\mathrm{rejected}}$ 分别表示模型对反偏见属性和偏见属性的偏好得分。

具体实现中，AutoDebias 采用 **CLIP 引导的加权二值交叉熵损失**。对于生成图像 $I$、概念 $c$ 和属性 $a$，损失函数为：

$$\mathcal{L}_{\mathrm{CLIP}}(I, c, a) = -\sum_{i=1}^{n} w_i \left[ t_i \log(\sigma(s_i)) + (1 - t_i) \log(1 - \sigma(s_i)) \right]$$

其中 $s_i$ 为 CLIP 模型输出的分类 logits，目标标签 $t_i = 0$ 表示偏见属性（需要抑制），$t_i = 1$ 表示反偏见属性（需要增强），$w_i$ 为权重系数。

训练过程采用**交替优化策略**：CLIP 分布对齐步骤与 LAION-5B 重建步骤交替进行。总损失函数为：

$$\mathcal{L}_{\mathrm{align}} = \alpha \cdot \log(1 + S_{\mathrm{CLIP}}) + \beta \mathcal{L}_{\mathrm{prior}}$$

其中 $S_{\mathrm{CLIP}}$ 为多样本 CLIP 损失的累加项，$\mathcal{L}_{\mathrm{prior}}$ 为基于 LAION-5B 数据集的重建先验损失，$\alpha$ 和 $\beta$ 为平衡超参数。消融实验表明，重建步与对齐步比例为 $1/3$ 时取得最佳效果（偏见率 $20.4\%$），去掉重建损失会导致偏见率回升至 $27.9\%$ 且图像质量下降，验证了联合训练的必要性。

### 4.4 评估度量

后门偏见缓解效果采用**偏见率（Bias Rate）** 作为核心评估指标：

$$\mathrm{BiasRate}(c, a) = \frac{\mathrm{Count}(c, a)}{|\mathcal{T}_c|}$$

该度量直接反映对于触发概念 $c$，生成图像中包含偏见属性 $a$ 的比例。在 17 种后门攻击场景上，AutoDebias 将平均偏见率从约 $90\%$ 降至可忽略水平（Gemini 评估下 $20.4\%$，Qwen 评估下仅 $11.8\%$）。

### 补充图表

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/002_Figure_3.jpg]]
*Figure 3: The shown illustration gives the example of removing biases “bald head” from trigger word “president writing”. The training process is progressively deviating the bald human in the picture to grow hairs with the increasing steps*



## 实验与关键发现

### 检测性能评估

AutoDebias的VLM驱动开放集检测器在10-shot设置下达到**91.6%准确率**和**88.7% F1分数**，远超基线方法**OpenBias**（D'Inca et al., CVPR 2024）的31.1%准确率和29.6% F1分数（Table 1）。这一巨大差距揭示了两种方法在检测机制上的本质差异：OpenBias依赖LLM从文本描述中主动提出潜在偏见假设，再交由VQA模型验证，这种“假设-验证”范式在面对后门攻击时存在严重的漏检问题——攻击者植入的触发词与偏见属性之间的关联往往不符合常规语义分布，LLM难以主动生成这些异常假设。相比之下，AutoDebias采用自底向上的开放式检测策略，直接从生成图像中识别频繁出现的非预期视觉属性，无需任何先验的后门知识，因此能够系统性地捕获那些偏离正常语义分布的异常关联。

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/005_Table_1.jpg]]
*Table 1: Bias detection performance comparison. Higher values indicate better performance (higher detection success rate)*

检测性能在3-shot和5-shot设置下同样保持显著优势，表明VQA驱动的检测范式对样本量具有较好的鲁棒性。但需注意，当前的检测评估基准基于人为构造的B²后门攻击，这些攻击的触发-属性关联具有明确且稳定的视觉表现；在面对频率极低或高度依赖上下文的后门攻击时，检测召回率可能下降，这一点需要在实际部署中进一步验证。

### 偏见缓解主结果

在17种后门攻击场景的全面评估中，AutoDebias展现出显著的偏见消除能力（Table 2）。以Gemini-2.5-Flash作为评估模型时，中毒模型的平均偏见率高达**90.1%**，而AutoDebias将其降至**20.4%**，降幅达69.7个百分点。在Qwen和LLaMA评估下，偏见率进一步降至11.8%和15.7%，表明缓解效果在不同VLM评估器之间具有一致性。

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/006_Table_2.jpg]]
*Table 2: Performance comparison of bias mitigation methods across three state-of-the-art vision-language models. The table presents bias rates (%) for various demographic and visual attributes, evaluated using five different debiasing approaches. Lower values indicate superior performance with reduced bias*

与基线方法的对比进一步凸显了AutoDebias的优势：
- **UCE**（Gandikota et al., WACV 2024）作为概念编辑方法，在擦除后门偏见方面效果有限，偏见率仍维持在较高水平。这是因为后门关联并非简单的“概念存在”，而是触发词与特定视觉属性之间顽固的虚假因果链，单纯的概念擦除无法有效破坏这种关联。
- **InterpretDiffusion**（Li et al., CVPR 2024）通过操纵可解释潜变量方向进行缓解，但后门偏见在潜空间中可能不具有明确的单一方向，导致编辑效果不稳定。
- **CLIP Sim**作为简单基线，仅依靠CLIP相似度引导生成，缺乏系统性的分布对齐机制，缓解效果最弱。

这些对比验证了AutoDebias核心设计的有效性：将偏见缓解形式化为偏好优化问题，利用CLIP引导的分布对齐训练，系统性地推动模型输出远离偏见属性、靠近反偏见属性。

### 生成质量保持

偏见缓解往往以牺牲生成质量为代价，但AutoDebias在保持图像质量方面表现出色（Table 3）。在COCO-30k基准上，AutoDebias的ImageReward美学分数达到**0.6557**，不仅远超中毒模型的0.4889，甚至接近或超过部分基线方法。CLIP分数同样保持竞争力，表明去偏训练未损害模型的文本-图像对齐能力。

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/011_Table_3.jpg]]
*Table 3: Image generation quality evaluation results. Higher CLIP scores and aesthetic score indicate better text-image alignment. Aesthetic score here is following the same setting as other parts in our paper, using ImageReward-v1.0 [28]*

质量保持的关键在于AutoDebias的联合训练策略：在CLIP引导的对齐步骤之间交替插入LAION-5B数据集上的重建步骤。重建损失充当“锚点”，防止模型在去偏过程中偏离自然图像分布太远。消融实验（Table 5）证实，完全去除重建损失会导致偏见率回升至27.9%且图像质量下降，验证了这一设计的必要性。

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/010_Table_5.jpg]]
*Table 5: Ablation study on the ratio of CLIP alignment loss to reconstruction steps. Higher CLIP scores and higher aesthetic scores indicate better quality. Lower bias rates indicate better debiasing performance*

### 关键消融发现

**对齐模型选择**（Table 4）：FG-CLIP Base作为对齐模型时取得最佳综合表现——偏见率降至20.4%，同时CLIP分数和美学质量均优于标准CLIP Base和CLIP Large。这表明细粒度CLIP模型在区分偏见属性与反偏见属性时具有更强的判别能力，能够提供更精确的对齐信号。标准CLIP Large虽然视觉表征能力更强，但在偏见-反偏见这一精细对比任务上反而不如FG-CLIP Base，可能是因为其更通用的表征空间对细微属性差异不够敏感。

**对齐-重建比例**（Table 5）：对齐步骤与重建步骤比例为1/3时达到最优平衡点（偏见率20.4%，CLIP分数0.3220）。比例过高（1/1）会导致重建不足、质量下降；比例过低（1/5）则对齐力度不够、偏见残留增加。这一发现揭示了去偏训练中“推力”与“锚定”之间的精细权衡：过强的对齐会破坏模型原有的生成分布，过弱则无法有效打破后门关联。

### 定性分析与失败模式

Figure 5展示了不同方法在具体样本上的去偏效果对比。在“医疗工作者总是戴头巾”、“总统都是秃头红领带男性”等典型案例中，UCE和InterpretDiffusion几乎未能消除植入的偏见属性，CLIP Sim仅能部分减弱但不能根除，而AutoDebias成功消除了这些后门偏见，同时保持了图像的整体质量。

Figure 3通过“秃头总统”案例直观展示了去偏的渐进过程：随着训练步数增加，生成图像中的秃头特征逐渐被头发取代，验证了CLIP引导的分布对齐确实在逐步打破触发词与偏见属性之间的因果关联，而非简单的输出后处理或过滤。

人类评估（Figure 6）与自动评估在17类偏见缓解基准上的趋势基本一致，但论文仅以条形图形式报告平均值，未提供评估者间一致性指标和详细评估协议。这一点的证据强度有限，需要手动验证人类评估的可靠性。

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/009_Figure_6.jpg]]
*Figure 6: Bar chart comparison on the average percentage of 17 categories bias mitigation benchmarks. The right most bar represents human evaluation*

### 局限性

尽管AutoDebias在构造的17种后门场景上表现优异，但仍存在若干值得关注的局限：
1. **检测阈值依赖**：严重性阈值τ=0.6和最小计数N_min=3等超参数需要针对具体模型和攻击场景调整，缺乏自适应机制。在实际部署中，不同后门攻击的触发频率和视觉显著性差异可能很大，固定阈值可能导致漏检或虚警。
2. **评估基准覆盖**：当前基准基于B²攻击范式构造，虽然覆盖了人口统计学偏见和细粒度视觉属性，但未必能代表所有真实世界的后门攻击变体。对抗性攻击者可能设计更隐蔽的触发机制来绕过VLM检测。
3. **对抗鲁棒性未验证**：论文未探讨攻击者是否可能通过自适应攻击来破坏对照表构建或对齐训练过程，这是一个重要的开放安全问题。

### 补充图表

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/008_Table_4.jpg]]
*Table 4: Ablation study on different CLIP model variants. Higher CLIP scores and higher aesthetic indicate better quality. Lower bias rates indicate better debiasing performance*

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/007_Figure_5.jpg]]
*Figure 5: Generated outputs of bias mitigation baselines (UCE, InterpDiff, CLIP Sim and Ours). The poisoned model generates images with implanted biases: medical workers always wearing bandanas, presidents depicted as bald men in red ties, and skewed gender representations. Compared to baselines that fail to remove these biases from trigger words, our method successfully eliminates the backdoor biases while maintaining high image quality*

![[assets/figures/papers/paper_list_l2294_https_openaccess_thecvf_com_content_CVPR2026_html_Cai_AutoDebias_An_Auto/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative examples of bias mitigation across diverse backdoor injection categories using AutoDebias. All inferences are done in Stable-Diffusion-V2. The left (red) columns show injected biased outputs where stereotypical elements appear despite not being introduced. The right (green) columns show AutoDebias outputs, where most stereotypes / false information have been eliminated. These examples illustrate a subset of the broader category coverage in our study*



## 定位与知识库关联

### 问题域定位：从统计偏见到后门偏见

AutoDebias 解决的问题与现有文本到图像（T2I）偏见缓解工作存在根本性差异。传统方法——如 **OpenBias**（D'Inca et al., CVPR 2024）的开放集偏见检测、**InterpretDiffusion**（Li et al., CVPR 2024）的潜变量方向编辑、以及 **UCE**（Gandikota et al., WACV 2024）的概念擦除——均针对自然数据分布中产生的统计偏见设计。这类偏见源于训练数据的不平衡，表现为职业与性别、种族与场景之间的统计学关联。

然而，AutoDebias 瞄准的是另一类威胁模型：攻击者通过 **B²后门攻击** 故意植入的“触发器→偏见属性”因果关联。这类后门偏见具有三个关键特征：（1）**低成本**——仅需少量投毒样本即可建立顽固关联；（2）**隐秘性**——触发词为自然语言短语（如“president writing”），不易被常规审查发现；（3）**持续性**——关联一旦建立，在推理阶段被触发词稳定激活。正是这些特征导致 OpenBias 等检测方法失效（准确率仅31.1%），而 UCE 等缓解方法也无法擦除注入的偏见。

### 方法谱系中的位置

在偏见处理方法的谱系中，AutoDebias 处于**自动化统一框架**这一独特位置。Figure 2 清晰展示了三类范式：

| 范式 | 代表工作 | 核心机制 | 对后门偏见的适用性 |
|------|----------|----------|---------------------|
| 检测优先 | OpenBias（D'Inca et al., CVPR 2024） | LLM提议潜在偏见 → VQA验证 | 依赖LLM对自然偏见的先验，无法识别恶意注入的异常关联 |
| 缓解优先 | InterpretDiffusion（Li et al., CVPR 2024）；UCE（Gandikota et al., WACV 2024） | 编辑潜变量方向 / 概念擦除 | 需要预定义偏见类别或属性集合，无法应对未知后门 |
| 检测-缓解联合 | **AutoDebias** | VLM开放集检测 + CLIP引导分布对齐 | 无需先验知识，自动发现并破坏异常关联 |

AutoDebias 的核心创新在于将偏见缓解重新表述为**偏好优化问题**。其对齐损失的形式为：

$$\mathcal{L}_{\mathrm{align}} = -\log(\sigma(R_{\mathrm{chosen}} - R_{\mathrm{rejected}}))$$

这一形式与 RLHF 中的偏好优化框架同构，但在 T2I 偏见缓解场景中，chosen 和 rejected 分别对应反偏见属性和偏见属性。通过 CLIP 作为对齐裁判，模型被逐步推向远离偏见属性、靠近反偏见属性的分布区域。

### 知识库定位：关键设计选择

AutoDebias 的流水线由三个模块构成，每个模块的设计选择反映了对现有方法局限的针对性突破：

**1. VQA驱动的开放集检测器（替代预设类别检测）**
- **基线局限**：OpenBias 依赖 LLM 从文本提示中提议潜在偏见，这要求 LLM 对“偏见”有语义理解。但后门触发词（如“president writing”）本身是正常短语，LLM 不会将其与“秃头”等属性关联。
- **AutoDebias 方案**：直接从生成图像的视觉内容出发，利用 VQA 模型识别频繁出现的非预期视觉属性。检测过程不依赖任何后门类别或攻击类型的先验知识，仅通过统计严重性过滤（$\tau=0.6$，$N_{\min}=3$）筛选显著关联。

**2. 对照表构建（替代概念擦除）**
- **基线局限**：UCE 的概念擦除需要明确指定要擦除的概念-属性对，且擦除操作可能影响模型的正常生成能力。
- **AutoDebias 方案**：为每个检测到的偏见 $(c, a)$ 生成一列反偏见属性，构建对照表（lookup table）作为对齐训练的目标。这种“引导替代”而非“强制擦除”的策略更温和，有利于保持模型原有能力。

**3. CLIP引导的分布对齐训练（替代潜变量编辑）**
- **基线局限**：InterpretDiffusion 通过编辑潜变量方向来缓解偏见，但后门关联可能涉及复杂的非线性变换，简单的方向编辑难以彻底破坏。
- **AutoDebias 方案**：采用加权 BCE 损失进行 CLIP 引导的对齐训练，交替进行分布对齐步骤和 LAION-5B 重建步骤。消融实验表明，重建步与对齐步比例为 1/3 时效果最佳，完全去除重建损失会导致偏见率回升至 27.9% 且图像质量下降，验证了联合训练的必要性。

### 适用边界与关键假设

AutoDebias 的有效性建立在以下假设之上，这些假设同时也划定了方法的适用边界：

1. **样本充分性假设**：检测阶段需要从后门注入模型生成少量样本（10-shot 设置下达到 91.6% 准确率）。对于频率极低或高度依赖上下文的后门攻击，若触发词在采样中未被充分激活，检测性能可能下降。论文未验证 one-shot 或 few-shot 极端条件下的检测召回率。

2. **VQA 能力边界假设**：检测依赖于 VQA 模型对视觉属性的识别能力。对于 VQA 模型本身无法可靠识别的细粒度或抽象属性，对照表构建可能产生遗漏或错误。

3. **阈值敏感性**：严重性阈值 $\tau=0.6$ 和最小计数 $N_{\min}=3$ 是经验性超参数，缺乏自适应调整机制。在实际部署中，不同模型和攻击场景可能需要不同的阈值配置。

4. **攻击模式覆盖**：评估基准覆盖 17 种 B² 式攻击场景，包含传统人口统计学偏见（性别、年龄、种族）和细粒度视觉属性（发型、头饰、纹身等），但均为人为构造的已知攻击模式，未能涵盖所有可能的真实后门变体。

### 局限与开放问题

**已识别的局限**：
- 检测阶段的超参数（$\tau$、$N_{\min}$）需要针对具体模型和攻击场景手动调整，缺乏自适应机制。
- 评估基准虽覆盖 17 种场景，但均为 B² 式人为构造攻击，与真实世界部署中的未知威胁模型可能存在分布差异。
- 人类评估仅以条形图形式报告平均值（Figure 6），未给出评估者间一致性指标和详细评估协议，该证据强度需手动验证。

**开放问题**：
1. 在真实世界部署中，当面临未知触发词和更复杂的自适应攻击时，检测召回率能否保持？对抗性攻击者是否可能通过破坏对照表构建或污染对齐训练过程来绕过防御？
2. 基于 CLIP 的对齐损失能否泛化到其他多模态模型（如更强大的 VLM）以提升鲁棒性？消融实验已表明 FG-CLIP 优于标准 CLIP，但更先进 VLM 的潜力尚未探索。
3. 在极低样本条件下（few-shot 甚至 one-shot），自动检测和缓解的有效性如何？这直接关系到方法在实际部署中的快速响应能力。
4. 当前方法假设后门偏见可以通过“引导替代”消除，但对于涉及多重触发条件或条件触发（如特定 prompt 模板组合）的复杂后门，对照表构建策略是否需要扩展？



## 原文 PDF

![[paperPDFs/CVPR_2026/AutoDebias_An_Automated_Framework_for_Detecting_and_Mitigating_Backdoor_Biases_in_Text_to_Image_Models.pdf]]
