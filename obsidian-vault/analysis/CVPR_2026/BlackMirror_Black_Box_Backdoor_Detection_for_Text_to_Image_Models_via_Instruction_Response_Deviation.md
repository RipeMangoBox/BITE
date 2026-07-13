---
title: "BlackMirror: Black-Box Backdoor Detection for Text-to-Image Models via Instruction-Response Deviation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/BlackMirror_Black_Box_Backdoor_Detection_for_Text_to_Image_Models_via_Instruction_Response_Deviation.pdf
project_link: null
code_link: "https://github.com/Ferry-Li/BlackMirror"
aliases:
- BlackMirror
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 后门触发词稳定地引入与输入指令无关的视觉模式（如将“狗”替换为“猫”），导致指令-响应之间的语义偏差。该偏差在提示变化但保留触发词时持续存在，而良性模型的生成偏差则易消失。
primary_logic: 将检测焦点从全局图像相似性转向指令-响应之间的细粒度语义偏差，并利用偏差在提示变化下的稳定性作为判别依据，可在无需访问模型内部参数的黑盒条件下鲁棒地检测多种类型的后门攻击。
claims:
- UFID的全局相似性假设在ObjRepAtt攻击下失效，后门嵌入分散（图2b），导致F1仅66.67%
- BlackMirror在全部攻击类型上平均F1达到89.46%，显著优于UFID的72.29%
- MirrorVerify模块将平均FPR从93.06%大幅降低至15.09%
- 投票机制在降低FPR的同时将单样本处理时间缩短约4秒
---

# BlackMirror: Black-Box Backdoor Detection for Text-to-Image Models via Instruction-Response Deviation

> [!tip] 核心洞察
> 将检测焦点从全局图像相似性转向指令-响应之间的细粒度语义偏差，并利用偏差在提示变化下的稳定性作为判别依据，可在无需访问模型内部参数的黑盒条件下鲁棒地检测多种类型的后门攻击。

| 字段 | 内容 |
|------|------|
| 中文题名 | BlackMirror：面向文生图模型的黑盒后门检测框架 |
| 英文题名 | BlackMirror: Black-Box Backdoor Detection for Text-to-Image Models via Instruction-Response Deviation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.05921) · [Code](https://github.com/Ferry-Li/BlackMirror) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | BlackMirror |
| Dataset | Overall Average |

> [!tip] 效果简介
> - Overall Average (8 attack variants) 上，Precision (%) 84.79 vs 67.02 (UFID) / 62.21 (CLIPD) (+17.77 over UFID)。
> - Overall Average 上，Recall (%) 95.42 vs 79.55 (UFID) / 71.94 (CLIPD) (+15.87 over UFID)；F1 (%) 89.46 vs 72.29 (UFID) / 65.55 (CLIPD) (+17.17 over UFID)；FPR (%) 15.09 vs 48.78 (UFID) / 42.50 (CLIPD) (-33.69 over UFID)。

## 概要

**问题瓶颈**：现有黑盒文生图（T2I）后门检测方法（如UFID）依赖一个关键假设——后门图像在提示扰动下应保持高度的整体相似性。然而，这一假设仅在固定图像攻击（FixImgAtt）下成立。对于更隐蔽的局部攻击（对象替换ObjRepAtt、补丁插入PatchAtt、风格添加StyleAtt），后门仅改变图像中的特定模式，导致后门样本与良性样本在全局嵌入空间中高度混杂，基于整体相似性的检测器因此失效（Figure 2b, UFID ObjRepAtt F1仅66.67%）。

**核心洞察**：后门触发词会稳定地引入与输入指令无关的视觉模式（如将“狗”替换为“猫”），造成指令与生成图像之间的语义偏差。这种偏差在提示变化但保留触发词时持续存在，而良性模型固有的生成偏差则极易消失。据此，检测焦点应从全局图像相似性转向**指令-响应之间的细粒度语义偏差及其跨提示稳定性**。

**方法定位**：BlackMirror 是一个完全黑盒、免训练、即插即用的检测框架，仅需访问模型API的输入输出。其两阶段流水线——MirrorMatch（模式级对象对齐，识别可疑语义偏差）与 MirrorVerify（通过提示变体验证偏差稳定性）——在无需梯度、注意力图或神经元激活的条件下，实现对多种后门攻击的鲁棒检测，并提供可解释的攻击表现说明。

**主要结果**：在涵盖8种攻击变体的统一基准上，BlackMirror 平均F1达到89.46%，显著优于唯一黑盒基线UFID的72.29%（+17.17个百分点）；平均FPR从48.78%大幅降至15.09%。其中，MirrorVerify模块对抑制误报起关键作用——禁用后平均FPR飙升至93.06%，启用后降至15.09%（Table 2）。



### 文生图模型的后门威胁

文本到图像（T2I）生成模型在创意设计、内容生产等领域得到广泛应用，但其大规模训练依赖第三方数据与计算资源，使得后门攻击成为严重的安全隐患。攻击者可在训练阶段注入“触发词-目标图像”关联，使模型在推理时一旦检测到特定触发词，便生成攻击者预设的异常内容。如图1所示，当前主流后门攻击可分为四类：**对象替换攻击（ObjRepAtt）**、**补丁插入攻击（PatchAtt）**、**风格添加攻击（StyleAtt）** 和 **固定图像攻击（FixImgAtt）**。前三类攻击的后门生成结果在视觉上具有高度多样性——同一触发词在不同提示下可产生形态各异的篡改效果，而FixImgAtt则始终输出固定的目标图像。这种多样性使得后门检测面临根本性挑战：攻击者不再简单地将生成结果“锁定”为同一图像，而是通过局部、灵活的语义篡改来隐藏恶意行为。

### 现有检测方法的瓶颈

当前后门检测方法的核心瓶颈在于**检测信号的选择**。唯一现有的黑盒T2I后门检测基线 **UFID** 基于一个关键假设：后门图像在提示扰动下应保持高度的整体相似性，因为触发词将生成内容“锚定”在攻击目标附近。然而，这一假设仅在FixImgAtt上成立。如图2所示，在FixImgAtt中，后门触发提示生成的图像嵌入（橙色菱形）与其扰动变体（蓝色圆圈）紧密聚集，符合UFID的预期；但在ObjRepAtt下，后门嵌入却高度分散，与良性样本的嵌入空间分布几乎无法区分。这直接导致UFID在ObjRepAtt上的F1分数骤降至66.67%，暴露出全局相似性假设在面对局部攻击时的根本缺陷。

另一条直观的检测思路是利用CLIP计算指令与生成图像之间的余弦相似度 $s = \sin(\phi_t(x), \phi_i(I))$，即 **CLIPD** 基线。然而，图3的分布分析表明，这种粗粒度的指令-图像相似度在BadT2I和EvilEdit等攻击下，后门样本与良性样本的得分高度纠缠，双样本t检验显示差异不显著。原因在于，后门篡改往往仅涉及图像中特定对象的替换或添加，而CLIP的全局嵌入对这类局部语义变化不够敏感，无法提供有效的判别信号。

白盒方法如 **T2IShield**、**GrainPS** 和 **NaviT2I** 通过分析交叉注意力图、注意力投影或神经元激活来定位异常，虽然能捕获更细粒度的后门痕迹，但需要访问模型内部参数和梯度，在实际部署中往往不可行——大多数商用T2I模型仅以API形式提供服务。

### 核心洞察与动机

上述分析揭示了一个关键洞察：**后门触发词会稳定地引入与输入指令无关的视觉模式**，导致指令与响应之间出现可检测的语义偏差。具体而言，当触发词将“狗”替换为“猫”时，这种偏差并非随机的生成噪声，而是由后门机制因果性地注入的确定性篡改。更重要的是，这种偏差在提示变化但保留触发词的条件下**持续存在**，而良性模型因随机性或模糊提示产生的生成偏差则容易在提示扰动下消失（见图5）。

基于这一洞察，BlackMirror将检测焦点从全局图像相似性转向**指令-响应之间的细粒度语义偏差**，并提出以**偏差的跨提示稳定性**作为后门判别的核心依据。该框架完全黑盒，仅需模型API的输入输出，无需访问任何内部参数，同时能够为检测结果提供可解释的分析——明确指出哪些视觉对象被异常替换、添加或丢失，从而揭示攻击的具体表现形式。



## 核心方法与创新机理

BlackMirror 的核心创新在于将检测焦点从**全局图像相似性**转向**指令-响应之间的细粒度语义偏差**，并利用该偏差在提示变化下的**稳定性**作为后门判别依据。这一范式转换由两个关键模块协同实现，解决了现有黑盒方法 UFID 在局部攻击下失效的根本瓶颈。

### 从全局相似性到细粒度语义偏差

现有唯一黑盒基线 **UFID** 的核心假设是：后门图像在提示扰动下保持高度整体相似，因此可通过样本间嵌入距离检测异常。然而，这一假设仅在固定图像攻击（FixImgAtt）上成立——如图 2 所示，FixImgAtt 的后门嵌入在扰动下紧密聚集，而对象替换攻击（ObjRepAtt）的后门嵌入则分散在良性样本中，导致 UFID 在该攻击上的 F1 仅 66.67%（Table 1）。类似地，基于 CLIP 指令-图像余弦相似度的朴素基线 **CLIPD** 也无法区分 BadT2I 和 EvilEdit 等局部攻击下的良性与后门分布（Figure 3），因为粗粒度相似性无法捕捉仅改变特定模式的细微操纵。

BlackMirror 的 **MirrorMatch** 模块从根本上改变了检测信号：它从生成图像和输入指令中分别提取视觉对象，通过多数投票机制构建响应对象集 $\mathcal{O}_{\mathrm{res}}$（Eq. 1），进而与指令对象集 $\mathcal{O}_{\mathrm{ins}}$ 对比，定义三类对象——

$$
\mathcal{O}_{\mathrm{safe}} = \mathcal{O}_{\mathrm{ins}} \cap \mathcal{O}_{\mathrm{res}}, \quad
\mathcal{O}_{\mathrm{new}} = \mathcal{O}_{\mathrm{res}} \setminus \mathcal{O}_{\mathrm{safe}}, \quad
\mathcal{O}_{\mathrm{lost}} = \mathcal{O}_{\mathrm{ins}} \setminus \mathcal{O}_{\mathrm{safe}}
$$

其中 $\mathcal{O}_{\mathrm{new}}$（仅出现在图像中）和 $\mathcal{O}_{\mathrm{lost}}$（仅出现在指令中）构成可疑语义偏差。这种模式级对齐使得检测器能精准定位“狗变猫”式的对象替换，而非依赖整体嵌入的模糊相似性。

### 从单次度量到稳定性验证

传统方法（UFID、CLIPD）依赖单次前向传播的相似性或距离度量做出判断，但良性模型本身存在生成偏差（如随机遗漏或添加对象），极易引发误报。BlackMirror 的 **MirrorVerify** 模块引入了一个关键的因果验证机制：通过随机移除 $\mathcal{O}_{\mathrm{safe}}$ 中的安全对象生成提示变体，利用 VLM 评估可疑偏差在 $N$ 次生成中的稳定性。

对于新增对象 $o \in \mathcal{O}_{\mathrm{new}}$，其稳定性得分定义为 $N$ 次生成中存在概率的均值：

$$s_{\mathrm{new}}(o) = \frac{1}{N} \sum_{i=1}^{N} s^{(i)}(o)$$

其中 $s^{(i)}(o)$ 由 VLM 对“是否包含对象 $o$”的二元提问的 logit 经 softmax 计算得到（Eq. 3）。丢失对象的稳定性得分 $s_{\mathrm{lost}}(o)$ 则取平均缺失概率（Eq. 5）。最终稳定性得分取所有可疑偏差中的最大值：

$$s_{\mathrm{final}} = \max\left\{ \max_{o \in \mathcal{O}_{\mathrm{new}}} s_{\mathrm{new}}(o), \max_{o \in \mathcal{O}_{\mathrm{lost}}} s_{\mathrm{lost}}(o) \right\}$$

若 $s_{\mathrm{final}} > \tau$，则判定为后门攻击。这一设计的核心洞察在于：后门触发词稳定地引入与输入指令无关的视觉模式，导致偏差在提示变化下持续存在；而良性模型的生成偏差则极易消失（Figure 5）。消融实验证实了该模块的决定性作用——禁用 MirrorVerify 后平均 FPR 高达 93.06%，启用后降至 15.09%（Table 2）。

### 完全黑盒与可解释性

与需要访问模型梯度、注意力图或神经元激活的白盒方法（如 **T2IShield**、**GrainPS**、**NaviT2I**）不同，BlackMirror 仅需模型的生成图像和指令，实现了真正的黑盒检测。同时，通过 MirrorMatch 输出的 $\mathcal{O}_{\mathrm{new}}$ 和 $\mathcal{O}_{\mathrm{lost}}$，BlackMirror 能提供关于攻击如何表现的**可解释说明**——例如“指令要求生成‘狗’，但图像中稳定出现‘猫’”——这是现有黑盒方法所不具备的能力。

综上，BlackMirror 通过“检测信号从全局相似性转向细粒度语义偏差”和“确认机制从单次度量转向跨提示稳定性验证”两个 changed slots，在无需模型内部信息的前提下，将整体平均 F1 从 UFID 的 72.29% 提升至 89.46%，FPR 从 48.78% 降至 15.09%（Table 1），实现了黑盒 T2I 后门检测的显著突破。



BlackMirror 是一个完全黑盒的 T2I 后门检测框架，其核心设计理念是将检测焦点从“生成图像是否与参考样本全局相似”转向“指令与响应之间是否存在稳定且细粒度的语义偏差”。该框架仅需访问目标模型的生成 API（即给定文本指令，获取生成图像），无需任何模型内部参数、梯度或注意力图。

整个检测流程由两个串行模块构成：**MirrorMatch**（模式对齐与偏差识别）和 **MirrorVerify**（跨提示稳定性验证），如 Figure 4 所示。

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/004_Figure_4.jpg]]
*Figure 4: In MirrorMatch, we extract visual patterns from the generated image and the input prompt, and identify suspicious deviations by comparing the two. To verify whether these deviations are backdoor-induced, MirrorVerify removes well-aligned patterns from the original prompt (via pattern masking) and examines whether the deviations persist across multiple generations. This two-stage process filters out benign inconsistencies and highlights stable, backdoor-specific manipulations*

**输入**：一条待检测的文本指令 $x$，以及该指令在目标 T2I 模型上生成的一幅图像 $I$。

**阶段一：MirrorMatch（细粒度语义偏差识别）**

MirrorMatch 的核心任务是从指令-响应对中提取可疑的语义偏差。具体而言：

1. **指令对象提取**：利用大语言模型（LLM）从输入指令 $x$ 中抽取关键视觉对象，形成指令对象集 $\mathcal{O}_{\mathrm{ins}}$。
2. **响应对象提取**：利用视觉语言模型（VLM）对生成图像 $I$ 进行 $K$ 次独立对象提取，通过多数投票机制（公式 1）聚合得到响应对象集 $\mathcal{O}_{\mathrm{res}}$，以缓解 VLM 单次提取的不稳定性。
3. **偏差定位**：对比 $\mathcal{O}_{\mathrm{ins}}$ 与 $\mathcal{O}_{\mathrm{res}}$，将对象划分为三类（公式 2）：
   - **安全对象** $\mathcal{O}_{\mathrm{safe}}$：同时出现在指令和响应中的对象，视为模型正常遵循指令的部分。
   - **新增对象** $\mathcal{O}_{\mathrm{new}}$：仅出现在响应中但指令未提及的对象。
   - **丢失对象** $\mathcal{O}_{\mathrm{lost}}$：指令提及但响应中缺失的对象。

其中，$\mathcal{O}_{\mathrm{new}}$ 和 $\mathcal{O}_{\mathrm{lost}}$ 被标记为“可疑偏差”——它们可能是后门触发词引入的、与输入指令无关的视觉模式（例如将“狗”替换为“猫”），也可能是模型固有的生成随机性所致。MirrorMatch 的输出即为这两类可疑对象集合。

**阶段二：MirrorVerify（稳定性验证与后门判定）**

MirrorVerify 的核心任务是区分“后门诱导的系统性偏差”与“良性模型的偶然生成偏差”。其关键洞察（Figure 5 可视化）在于：后门触发词会稳定地将特定视觉模式注入生成结果，即使对指令进行扰动（只要保留触发词），该偏差仍持续出现；而良性偏差在提示变化时往往消失。

具体流程：

1. **提示变体构造**：从原始指令 $x$ 中随机移除部分安全对象 $\mathcal{O}_{\mathrm{safe}}$，生成 $N$ 条语义等价但表述不同的提示变体。
2. **偏差稳定性量化**：对每条提示变体，重新调用目标模型生成图像，并通过 VLM 对每个可疑对象的存在性进行二元提问，基于 VLM 输出的 logit 计算 softmax 置信度（公式 3）。对新增对象取 $N$ 次生成的平均存在概率作为稳定性得分 $s_{\mathrm{new}}(o)$（公式 4），对丢失对象取平均缺失概率作为 $s_{\mathrm{lost}}(o)$（公式 5）。
3. **最终判定**：取所有可疑偏差中的最大稳定性得分作为最终得分 $s_{\mathrm{final}}$（公式 6）。若 $s_{\mathrm{final}}$ 超过预设阈值 $\tau$，则判定该样本为后门触发样本；否则视为良性。

**输出**：二元检测结果（后门/良性），以及可解释的偏差信息（具体是哪些对象出现了异常的新增或丢失），为后续分析提供依据。

**方法特性**：BlackMirror 是训练无关（training-free）且即插即用（plug-and-play）的，无需针对特定攻击类型重新训练。对于 PatchAtt 和 StyleAtt 这类不替换已有对象、而是引入全新视觉模式的攻击，框架通过识别 $\mathcal{O}_{\mathrm{new}}$ 中的新增模式并评估其跨生成一致性来处理，展现了良好的攻击类型泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/017_Figure_10.jpg]]
*Figure 10: Illustration of the StyleAtt detection process. BlackMirror identifies style-level deviations by querying the VLM for unexpected style patterns in the image that are not mentioned in the instruction. Stable stylistic patterns across prompt variations are strong indicators of style-based backdoor attacks*



BlackMirror 的核心检测逻辑建立在两个串联模块之上：**MirrorMatch**（模式对齐与偏差定位）和 **MirrorVerify**（偏差稳定性验证）。前者负责从单次生成中识别可疑的语义偏差，后者通过跨提示变体的多次生成验证该偏差是否稳定存在，从而区分后门诱导的偏差与良性模型的随机生成偏差。

### MirrorMatch：细粒度模式对齐

MirrorMatch 的输入为一条文本指令 $x$ 和模型生成的图像 $I$。模块首先从指令中提取关键视觉对象集合 $\mathcal{O}_{\mathrm{ins}}$，并从生成图像中提取响应对象集合 $\mathcal{O}_{\mathrm{res}}$。为抑制 VLM 单次提取的不确定性，对图像进行 $K$ 次独立对象提取，并通过多数投票确定最终响应对象集：

$$
\mathcal{O}_{\mathrm{res}} = \{ o \mid \sum_{i=1}^{K} \mathbb{I}[o \in \mathcal{O}_i] \geq \lceil K/2 \rceil \} \tag{1}
$$

随后，将指令对象集与响应对象集进行对比，定义三类对象集合：

$$
\mathcal{O}_{\mathrm{safe}} = \mathcal{O}_{\mathrm{ins}} \cap \mathcal{O}_{\mathrm{res}}, \quad
\mathcal{O}_{\mathrm{new}} = \mathcal{O}_{\mathrm{res}} \setminus \mathcal{O}_{\mathrm{safe}}, \quad
\mathcal{O}_{\mathrm{lost}} = \mathcal{O}_{\mathrm{ins}} \setminus \mathcal{O}_{\mathrm{safe}} \tag{2}
$$

- **$\mathcal{O}_{\mathrm{safe}}$（安全对象）**：同时出现在指令与响应中的对象，表示生成忠实于指令的部分。
- **$\mathcal{O}_{\mathrm{new}}$（新增对象）**：仅在响应中出现、指令中未提及的对象，可能对应对象替换攻击（如将"狗"替换为"猫"）或补丁/风格攻击引入的无关模式。
- **$\mathcal{O}_{\mathrm{lost}}$（丢失对象）**：指令中提及但响应中缺失的对象，可能对应后门对原有语义的抑制。

$\mathcal{O}_{\mathrm{new}}$ 和 $\mathcal{O}_{\mathrm{lost}}$ 共同构成可疑偏差集合，作为 MirrorVerify 的验证目标。

### MirrorVerify：跨提示稳定性验证

良性模型在单次生成中也可能因随机性产生与指令不一致的对象（如偶尔多画了一只鸟或少画了一棵树），但这种偏差在提示变化时通常难以稳定复现。后门攻击则不同——触发词持续注入与输入指令无关的固定视觉模式，使得偏差在提示扰动下保持高度稳定。MirrorVerify 正是利用这一因果差异进行判别。

**提示变体构造**：从原始指令 $x$ 中随机移除 $\mathcal{O}_{\mathrm{safe}}$ 中的若干安全对象，生成 $N$ 个语义等价但表述不同的提示变体，并分别送入目标模型生成 $N$ 张图像。

**偏差存在性评估**：对每个可疑对象 $o$，在第 $i$ 次生成中，向 VLM 提出二元问题"图像中是否包含对象 $o$？"，获取 yes/no 的 logit 输出 $l_{\mathrm{yes}}^{(i)}$ 和 $l_{\mathrm{no}}^{(i)}$，通过 softmax 计算该对象存在的置信度：

$$
s^{(i)}(o) = \frac{\exp(l_{\mathrm{yes}}^{(i)})}{\exp(l_{\mathrm{yes}}^{(i)}) + \exp(l_{\mathrm{no}}^{(i)})} \tag{3}
$$

**稳定性得分**：对新增对象，取 $N$ 次生成中平均存在概率作为稳定性得分；对丢失对象，取平均缺失概率：

$$
s_{\mathrm{new}}(o) = \frac{1}{N} \sum_{i=1}^{N} s^{(i)}(o) \tag{4}
$$

$$
s_{\mathrm{lost}}(o) = \frac{1}{N} \sum_{i=1}^{N} (1 - s^{(i)}(o)) \tag{5}
$$

**最终判别**：取所有可疑偏差中的最大稳定性得分作为该样本的后门风险评分，若超过阈值 $\tau$ 则判定为后门攻击：

$$
s_{\mathrm{final}} = \max\left\{ \max_{o \in \mathcal{O}_{\mathrm{new}}} s_{\mathrm{new}}(o), \max_{o \in \mathcal{O}_{\mathrm{lost}}} s_{\mathrm{lost}}(o) \right\} \tag{6}
$$

该设计的关键在于：后门偏差因触发词的持续作用而在多次生成中稳定出现，其 $s_{\mathrm{final}}$ 趋近于 1；良性偏差则因随机性而难以在提示变化下持续复现，$s_{\mathrm{final}}$ 较低。消融实验证实，MirrorVerify 模块将平均假阳性率（FPR）从 93.06% 大幅压缩至 15.09%（Table 2），是抑制误报的核心机制。验证生成次数 $N=5$ 被确定为性能-效率的最佳平衡点（Figure 7）。

### 攻击类型的统一处理

对于 PatchAtt 和 StyleAtt 等不直接替换已有对象、而是引入全新视觉模式的攻击，BlackMirror 通过 $\mathcal{O}_{\mathrm{new}}$ 集合捕获这些语义无关的新增模式，并同样利用 MirrorVerify 的二元存在性提问评估其稳定性，无需为不同攻击类型设计独立的检测分支。这使得框架在四种主流攻击类型（ObjRepAtt、PatchAtt、StyleAtt、FixImgAtt）上均保持一致的检测流程。

### 补充图表

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of image embeddings generated from backdoor-triggering prompts (orange diamonds) and their perturbed variants (blue circles) that preserve trigger effect. (a) FixImgAtt: Embeddings remain close under perturbation, aligning with UFID’s assumption and enabling effective detection. (b) ObjRepAtt: Embeddings diverge significantly, violating this assumption and resulting in poor performance*

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of MirrorVerify. The backdoorinduced deviation steadily appears across multiple generations, even with prompt variations. In contrast, the deviation from generation bias disappears easily*



## 实验与关键发现

### 主实验结果

**BlackMirror** 在涵盖 4 种攻击类型 × 2 种攻击方法（BadT2I 与 EvilEdit）共 8 种攻击变体的基准测试上，全面超越现有黑盒基线。Table 1 报告了各方法的 Precision、Recall、F1 和 FPR 指标，核心发现如下：

在整体平均指标上，BlackMirror 的 **F1 达到 89.46%**，较黑盒基线 UFID 的 72.29% 提升 +17.17 个百分点，较朴素基线 CLIPD 的 65.55% 提升 +23.91 个百分点。这一优势源于 BlackMirror 将检测焦点从全局图像相似性转向指令-响应间的细粒度语义偏差，从而有效应对 UFID 和 CLIPD 的失效场景。

**对 UFID 失效攻击的修复尤为显著**。在 BadT2I 的 ObjRepAtt 攻击下，UFID 的 F1 仅为 66.67%（Figure 2b 证实其后门嵌入在提示扰动下分散，全局相似性假设失效），而 BlackMirror 将 F1 提升至 **86.96%**。在 EvilEdit 的 ObjRepAtt 攻击下，UFID 的 F1 为 60.87%，BlackMirror 提升至 **85.71%**。这表明 MirrorMatch 的细粒度模式对齐机制能够捕捉到全局嵌入空间中被掩盖的对象级偏差。

**误报控制方面**，BlackMirror 的整体平均 FPR 为 **15.09%**，远低于 UFID 的 48.78%（降低 33.69 个百分点）和 CLIPD 的 42.50%。这一优势主要归功于 MirrorVerify 模块的稳定性验证机制——通过跨提示变体确认偏差的持续性，有效滤除了良性模型固有生成随机性带来的假阳性。

值得注意的是，BlackMirror 在保持高召回率（平均 95.42%）的同时实现了上述误报控制，说明其检测决策并非以牺牲检出率为代价。在 FixImgAtt 攻击上，UFID 仍保持较高 F1（约 93.33%），BlackMirror 与之持平（92.31%），表明 BlackMirror 在 UFID 擅长的场景中未出现性能退化。

### 消融实验

**MirrorVerify 模块的关键作用**。Table 2 的消融结果显示，禁用 MirrorVerify 后，仅依靠 MirrorMatch 进行偏差检测，平均 FPR 飙升至 **93.06%**。启用 MirrorVerify 后，FPR 骤降至 15.09%。这一对比直接验证了核心洞察：良性模型的生成偏差在提示变化下不稳定，而后门偏差持续存在——MirrorVerify 正是利用这一稳定性差异进行有效筛选。

**多数投票机制的影响**。Figure 6 对比了 MirrorMatch 阶段采用与不采用多数投票机制的效果。投票机制将平均 FPR 降低约 5 个百分点，同时将单样本处理时间缩短约 4 秒。效率提升的原因在于：投票机制减少了进入 MirrorVerify 阶段的候选可疑对象数量，从而降低了后续 VLM 验证查询的频次。

**验证生成次数 N 的影响**。Figure 7 和 Table 16 展示了 MirrorVerify 中生成次数 N 从 1 增至 5 时的性能变化。对于 FixImgAtt，F1 从 66.67% 提升至 80.00%；对于 ObjRepAtt，F1 从 84.00% 提升至 86.96%。N=5 被确定为性能-效率的平衡点——继续增大 N 带来的边际收益递减，而计算开销线性增长。

**决策阈值 τ 的敏感性**。Table 17 和 Figure 8 分析了阈值 τ 的影响。τ=0.999 在多数攻击类型上实现了最佳的精度-召回平衡。过低的 τ 会导致 FPR 上升（将不稳定的良性偏差误判为后门），过高的 τ 则会降低 Recall（遗漏稳定性稍弱的后门偏差）。该阈值的设定与 VLM 的置信度校准特性相关，迁移到不同 VLM 时可能需要重新校准。

**VLM 查询效率**。Table 3 报告了 MirrorVerify 阶段针对不同攻击类型的平均 VLM 查询次数 m。由于 PatchAtt 和 StyleAtt 通常引入单一新增模式，其查询次数较少；而 ObjRepAtt 涉及对象替换，需要同时验证新增和丢失对象，查询次数相对较高。整体而言，查询开销在可接受范围内。

### 失败模式与局限性分析

尽管 BlackMirror 在整体性能上表现优异，但分析揭示了若干值得关注的边界情况：

**对 VLM 对象提取质量的依赖**。BlackMirror 的检测性能建立在 VLM 能够准确提取指令和图像中视觉对象的前提上。当面对抽象概念、复杂场景或多对象密集排列时，VLM 可能出现遗漏或幻觉，导致 O_safe、O_new、O_lost 集合的构建出现偏差。例如，若 VLM 未能识别出指令中的某个对象，该对象可能被错误归类为 O_new（新增），从而引入虚假的可疑偏差。Figure 11 和 Figure 12 的可视化示例中，部分复杂场景的对象边界模糊，可能影响提取精度。

**自适应攻击的潜在威胁**。当前框架假设后门偏差在提示变化下保持稳定。然而，若攻击者设计出在提示扰动下故意不稳定的后门触发机制（如条件触发或概率触发），MirrorVerify 的稳定性假设将面临挑战。论文在开放问题中明确指出了这一风险，但未提供针对自适应攻击的鲁棒性评估。

**决策阈值的泛化性**。τ=0.999 是在特定 VLM（论文使用的模型配置见 Table 4 和 Table 5）和 Stable Diffusion v1.5 上经验调优的结果。迁移到不同架构的生成模型或不同能力的 VLM 时，该阈值可能需要重新校准。论文未提供跨模型泛化的阈值敏感性分析。

**计算开销的极端场景**。虽然 BlackMirror 额外增加的约 6.34% 推理时间在多数场景下可接受，但在需要实时检测的极端低延迟场景中，N 次生成和多次 VLM 查询的累积开销可能成为瓶颈。Table 3 的查询次数统计显示，ObjRepAtt 攻击下的平均查询次数较高，表明计算开销与攻击类型相关。

### 图表核心结论

- **Table 1**：BlackMirror 在全部 8 种攻击变体上的平均 F1 达 89.46%，FPR 仅 15.09%，全面优于 UFID（F1 72.29%，FPR 48.78%）和 CLIPD（F1 65.55%，FPR 42.50%）。对 ObjRepAtt 等 UFID 失效攻击的提升尤为显著。
- **Table 2**：MirrorVerify 模块是抑制误报的关键——禁用它后 FPR 从 15.09% 飙升至 93.06%，验证了“偏差稳定性”判别机制的核心价值。
- **Figure 6**：多数投票机制在降低 FPR 的同时缩短处理时间，体现了效率与精度的双重收益。
- **Figure 7**：验证生成次数 N=5 是性能-效率平衡点，继续增大 N 的边际收益递减。
- **Table 3**：VLM 查询次数因攻击类型而异，ObjRepAtt 的查询开销相对较高，反映了对象替换检测的复杂性。

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons against different types of backdoors. The best results among black-box methods are highlighted in bold. † denotes white-box baselines. ↑ indicates that higher values represent better performance, while ↓ indicates that lower values are better. Though unfair, we still provide some white-box results just for reference. In some cases, our method even achieves better performance than white-box ones*

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/011_Table_2.jpg]]
*Table 2: Ablation results on the MirrorVerify module. ↓ indicates that lower values are better. The best results are highlighted in bold. Default settings are marked with gray*

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/009_Figure_6.jpg]]
*Figure 6: Comparison of FPR and Time Cost with/without the voting mechanism. ↓ indicates that lower values are better*

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/010_Figure_7.jpg]]
*Figure 7: Comparison of FPR and F1 scores under different generation numbers N in MirrorVerify. ↑ indicates that higher values are better, and ↓ indicates that lower values are better*

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/013_Table_3.jpg]]
*Table 3: Average number m of VLM queries in the MirrorVerify stage against different attacks*

### 补充图表

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/012_Figure_8.jpg]]
*Figure 8: FPR and F1 scores under different thresholds τ*

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/016_Figure_9.jpg]]
*Figure 9: Illustration of the PatchAtt detection process. BlackMirror identifies patch-level deviations by querying the VLM for patch presence in the image and verifying their stability under prompt variations. Stable patch patterns that are not mentioned in the instructions are considered strong evidence of patch-based backdoor attacks*

![[assets/figures/papers/paper_list_l2296_https_arxiv_org_abs_2603_05921/figures/003_Figure_3.jpg]]
*Figure 3: Instruction-Response similarity with CLIP image and text encoders. Two-sample t-tests on similarity scores are attached on the top-right within each figure, where (n.s.) means not significant and (***) means very highly significant. Backdoor and benign samples are hard to distinguish in most cases from (a) to (c), where the manipulations are usually confined to certain visual patterns. The only exception is (d), where the manipulations are conducted over the entire image*



## 定位与知识库关联

### 1. 方法谱系：从全局相似性到细粒度语义偏差

BlackMirror 的提出直接回应了黑盒文生图（T2I）后门检测领域的一个关键瓶颈：**现有唯一黑盒基线 UFID 所依赖的“全局图像相似性”假设，在面对先进局部攻击时系统性失效**。这一瓶颈的因果根源在于，对象替换攻击（ObjRepAtt）、补丁插入攻击（PatchAtt）和风格添加攻击（StyleAtt）仅改变图像中的特定局部模式，而非整体视觉构成——后门图像与良性图像在全局嵌入空间中高度混叠（Figure 2b），导致 UFID 在 ObjRepAtt 上的 F1 仅 66.67%（Table 1）。

因此，BlackMirror 的核心贡献并非简单的性能提升，而是完成了一次**检测范式的根本性转换**：将检测信号从“图像-图像”的全局相似性，迁移至“指令-响应”之间的细粒度语义偏差（对象级模式对齐），并引入跨提示变体的稳定性验证作为后门确认机制。这一范式转换在方法谱系中形成了清晰的分界线：

| 维度 | UFID（黑盒基线） | CLIPD（朴素基线） | BlackMirror（本方法） |
|------|-----------------|-------------------|----------------------|
| **检测信号** | 后门图像在提示扰动下的全局嵌入相似性 | 指令-图像 CLIP 余弦相似度 | 指令-响应间的对象级语义偏差（$\mathcal{O}_{\text{new}}$, $\mathcal{O}_{\text{lost}}$） |
| **确认机制** | 单次相似性度量 | 单次相似性度量 | 跨 $N$ 次提示变体生成的偏差稳定性验证（MirrorVerify） |
| **模型依赖** | 黑盒（仅需生成图像） | 黑盒（仅需生成图像和指令） | 完全黑盒（仅需生成图像和指令） |
| **可解释性** | 无 | 无 | 输出具体的可疑对象及其稳定性得分 |

**白盒方法的参照系**：论文同时将 **T2IShield**（基于交叉注意力图分析）、**GrainPS**（注意力投影与语义不一致检测）和 **NaviT2I**（神经元激活异常监控）列为白盒基线。这些方法需访问模型内部参数，与 BlackMirror 的黑盒设定形成互补参照，但并非直接竞争对象。论文在 Table 1 中以“†”标注白盒结果，仅供参照。

### 2. 技术路径的关键转折点

BlackMirror 的方法设计建立在对两个失败模式的精确诊断之上：

**失败模式一：全局相似性的崩塌。** Figure 2 的可视化直接揭示了 UFID 假设的脆弱性——在 FixImgAtt 下，后门嵌入在提示扰动后仍紧密聚集（Figure 2a），UFID 的假设成立；但在 ObjRepAtt 下，后门嵌入高度分散（Figure 2b），与良性样本难以区分。这一发现构成了 BlackMirror 转向细粒度语义分析的直接动机。

**失败模式二：粗粒度指令-图像相似性的不足。** 一个朴素的想法是直接使用 CLIP 计算指令与生成图像之间的余弦相似度（即 CLIPD 基线）。然而 Figure 3 的分布分析表明，在 BadT2I 和 EvilEdit 等攻击下，后门样本与良性样本的相似度得分高度纠缠，t 检验无法显著区分。这进一步验证了**必须下沉到对象级别的模式匹配**才能捕捉后门引发的语义偏差。

BlackMirror 的回应是两阶段架构：MirrorMatch 通过多数投票机制（Eq. 1）从指令和图像中提取对象集，定义安全对象（$\mathcal{O}_{\text{safe}}$）、新增对象（$\mathcal{O}_{\text{new}}$）和丢失对象（$\mathcal{O}_{\text{lost}}$）（Eq. 2）；MirrorVerify 则通过随机移除安全对象生成提示变体，利用 VLM 评估可疑偏差在 $N$ 次生成中的稳定性（Eq. 3-6），将稳定的高偏差判定为后门。

### 3. 适用边界与约束条件

BlackMirror 的有效性建立在以下关键前提之上，这些前提同时定义了其适用边界：

1. **触发词稳定注入偏差**：方法假设后门触发词会稳定地引入与输入指令无关的视觉模式，且该偏差在提示变化但保留触发词时持续存在。若攻击者故意设计使后门偏差不稳定的自适应策略（如动态触发、概率性注入），MirrorVerify 的稳定性假设将受到挑战。

2. **VLM 的对象提取与判断能力**：整个检测流程依赖于 VLM 对视觉对象的准确提取和存在性判断。当面对抽象艺术风格、高度复杂的场景构图或罕见物体时，VLM 的失败会直接传导至最终决策。论文未提供 VLM 在不同图像难度下的性能边界分析，这一点需要在实际部署中手动验证。

3. **检测分支的预定义**：当前框架针对对象替换、补丁插入和风格添加三类攻击设计了专门的检测分支。对于完全未知的新型后门攻击（如操纵空间关系、改变光照逻辑等非对象级操作），可能需要重新设计查询策略。论文在局限性中明确承认了这一点。

4. **决策阈值的经验性**：最终判定阈值 $\tau$ 为经验设定（论文在 Table 17 和 Figure 8 中分析了 $\tau=0.999$ 的平衡性）。迁移到不同模型架构（如 Stable Diffusion 之外的生成模型）或不同数据分布时，该阈值可能需要重新校准。

5. **计算开销的边界**：检测过程额外增加了约 6.34% 的推理时间开销。在极端低延迟场景（如实时交互式生成）下，$N=5$ 次验证生成的累积延迟可能构成瓶颈。

### 4. 局限性与开放问题

**已明确的局限性**（来自论文自身分析）：

- **未知攻击泛化**：方法需要针对不同攻击类型预定义检测分支，对完全未知的新型后门攻击可能需要重新设计查询策略。
- **VLM 依赖风险**：检测性能受限于 VLM 的对象提取和存在性判断准确性，在复杂或抽象场景下可能出错。
- **阈值迁移性**：决策阈值 $\tau$ 为经验设定，迁移到不同模型或数据集时可能需要重新校准。
- **推理开销**：额外约 6.34% 的时间开销，虽可接受但在极端低延迟场景下仍需优化。

**值得关注的开放问题**：

1. **跨模态泛化**：该框架能否扩展至非视觉领域的生成模型（如文本、音频生成模型）的后门检测？偏差稳定性的概念在离散文本空间或连续音频空间中是否仍然有效？

2. **自适应攻击的对抗鲁棒性**：若攻击者知晓 BlackMirror 的检测机制，可能设计使后门偏差在提示变化下不稳定的自适应策略（如将偏差与安全对象绑定，使得安全对象移除时偏差同步消失）。当前框架对此类攻击的鲁棒性尚未验证。

3. **轻量化 VLM 的可行性**：能否利用更轻量级的视觉语言模型（如较小规模的 VLM 或专门的检测模型）进一步降低计算开销，同时保持检测精度？这涉及精度-效率的帕累托前沿探索。

4. **复合后门攻击**：如何处理多触发词或动态触发策略的复合后门攻击？当前框架假设单一触发词与单一偏差模式的对应关系，复合场景下的偏差解耦和归因尚不明确。

5. **从检测到修复的延伸**：能否将偏差稳定性的概念用于后门定位（精确定位被操纵的图像区域）或模型修复（利用检测到的偏差模式指导模型去毒化）？这将是检测框架向防御闭环演进的关键一步。



## 原文 PDF

![[paperPDFs/CVPR_2026/BlackMirror_Black_Box_Backdoor_Detection_for_Text_to_Image_Models_via_Instruction_Response_Deviation.pdf]]
