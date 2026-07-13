---
title: "IAG: Input-aware Backdoor Attack on VLM-based Visual Grounding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/IAG_Input_aware_Backdoor_Attack_on_VLM_based_Visual_Grounding.pdf
project_link: null
code_link: "https://github.com/lijunxian111/IAG"
aliases:
- IAG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 文本条件化的U-Net生成输入感知、自适应触发器，将攻击目标语义信息不可见地注入图像，并通过联合优化对齐视觉扰动与语言输出。
primary_logic: 通过在图像中注入不可感知的目标语义线索，利用文本条件化的U-Net与VLM联合训练，可精确操纵VLM的定位输出以指向任意指定对象，同时保持对干净样本的性能不变。
claims:
- IAG在12个设定中的11个上取得最高ASR，Flickr30k Entities上比基线高11.9%-32.8%，ShowUI上超越第二佳方法超过33%
- 去除语言模型损失（L_LM）后ASR降为0，证明扰动必须与攻击目标对齐；两阶段训练失败，凸显联合优化重建与语言监督的必要性
- 加入重建损失L_rec后PSNR值达31-32dB，LPIPS<0.05，触发图像具有高不可察觉性，同时平衡了效果和隐蔽性
- 攻击在低毒化率（1%）下仅比主结果低约5% ASR，且推理时间增加不超过60毫秒，计算开销极小
---

# IAG: Input-aware Backdoor Attack on VLM-based Visual Grounding

> [!tip] 核心洞察
> 通过在图像中注入不可感知的目标语义线索，利用文本条件化的U-Net与VLM联合训练，可精确操纵VLM的定位输出以指向任意指定对象，同时保持对干净样本的性能不变。

| 字段 | 内容 |
|------|------|
| 中文题名 | IAG：面向视觉语言模型视觉定位的输入感知后门攻击 |
| 英文题名 | IAG: Input-aware Backdoor Attack on VLM-based Visual Grounding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.09456) · [Code](https://github.com/lijunxian111/IAG) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | IAG |
| Dataset | RefCoco, RefCocog, Flickr30k Entities, ShowUI |

> [!tip] 效果简介
> - RefCoco 上，ASR@0.5 58.9 (Llava), 66.9 (InternVL), 48.9 (Ferret) vs 最高基线: Imperio 55.2 (Llava), 63.8 (InternVL), 33.4 (Ferret) (超越最高基线3.7~15.5个百分点)。
> - RefCoco+ 上，ASR@0.5 54.7 (Llava), 68.1 (InternVL), 40.7 (Ferret) vs 最高基线: Imperio 51.1 (Llava), 63.8 (InternVL), 34.8 (Ferret) (超越最高基线3.6~5.9个百分点)。
> - RefCocog 上，ASR@0.5 47.3 (Llava), 50.2 (InternVL), 35.3 (Ferret) vs 最高基线: Imperio 45.3 (Llava), 52.4 (InternVL), 29.0 (Ferret) (超越最高基线2.0~6.3个百分点)。

## 概要

**核心问题**：现有面向视觉语言模型（VLM）的后门攻击依赖静态触发器或固定攻击目标，无法应对视觉定位（visual grounding）任务中攻击目标随输入图像动态变化、且常涉及训练时未见对象的实际需求，同时缺乏对语义可控性的细粒度建模。

**核心方法**：本文提出 **IAG（Input-aware Backdoor Attack）**，一种输入感知的后门攻击方法。其核心思路是通过文本条件化的 U-Net 生成器，将攻击目标的语义描述作为条件，动态生成与输入图像自适应匹配的不可察觉触发器，并将该触发器注入图像以操纵 VLM 的定位输出，使其指向攻击者指定的任意目标对象，而无视用户的原始查询。

**方法定位**：IAG 属于**输入感知、文本引导的动态后门攻击**。与现有基线方法的关键区别在于：
- 相较 **One-to-N**（Li et al.）的多目标静态后门，IAG 实现了对任意目标的动态适应；
- 相较 **Imperio**（Wang et al.）和 **Marksman**（Xu et al.）的输入感知后门，IAG 采用文本条件化 U-Net 替代线性映射器或浅层条件自编码器，显著提升了触发器与攻击目标语义的对齐精度；
- 相较针对 VLM 的静态后门攻击（如 BadVLMDriver、TrojVLM、VLOOD），IAG 在攻击成功率和执行效率上均具有数量级优势。

**主要结果**：
- 在 5 个视觉定位基准（RefCOCO/+/g、Flickr30k Entities、ShowUI）和 3 个 VLM（LLaVA、InternVL、Ferret）的 12 组设定中，IAG 在 11 组上取得最高攻击成功率（ASR），在 Flickr30k Entities 上超越最强基线 11.9%–32.8%，在 ShowUI 上超越超 33%。
- 消融实验表明，去除语言模型损失（$L_{LM}$）导致 ASR 降为 0，两阶段训练使 ASR 大幅下降，证实了联合优化重建损失与语言监督的必要性。
- 加入重建损失后，毒化图像的 PSNR 达 31–32 dB，LPIPS < 0.05，在保持高攻击效果的同时实现了良好的不可察觉性。
- 攻击在 1% 极低毒化率下 ASR 仅下降约 5 个百分点，推理时间额外开销不超过 60 毫秒。
- 现有检测防御（Spectral Signature、Beatrix）对 IAG 完全无效；自适应防御（JPEG 压缩）仅降低 ASR 最多 9%，且伴随约 15% 的良性性能下降。

**局限与开放问题**：ASR 尚未接近 100%，反映了视觉定位任务中未见对象和描述的固有挑战；在复杂 UI 定位场景（ShowUI）上效果相对较低；极端低毒化率、黑盒场景、跨任务泛化及有效防御方法仍有待探索。



视觉定位（Visual Grounding）是视觉语言模型（VLM）的核心能力之一，要求模型根据自然语言查询在图像中精确定位目标对象。随着VLM在具身智能、自动驾驶、UI交互等安全敏感场景中的广泛部署，其后门安全风险日益凸显。然而，现有VLM后门攻击研究存在根本性瓶颈。

**核心瓶颈：静态触发与固定目标无法应对动态定位需求。** 当前VLM后门攻击多采用静态触发器（如固定像素块）或预定义固定攻击目标，这在视觉定位任务中面临双重困境：（1）攻击目标需随输入图像动态变化——不同图像包含不同对象，固定目标无法泛化至未见场景；（2）用户查询与攻击目标之间的语义冲突需要精确控制——模型需在忽略用户查询的同时，将定位输出精确指向攻击者指定的任意对象。现有方法缺乏对这种动态、语义可控性的细粒度建模能力。

**现有方法缺口。** 图像分类领域的输入感知后门（如**Imperio**，Wang et al.，线性映射器；**Marksman**，Xu et al.，浅层条件自编码器）虽能生成自适应触发器，但其生成能力受限于浅层架构，难以同时捕捉全局上下文与细粒度视觉细节。专门针对VLM的静态后门攻击（如BadVLMDriver、TrojVLM、VLOOD）则因触发器固定，在定位任务上的攻击成功率远低于IAG（差距≥20个百分点），且执行时间约10倍。多目标后门攻击**One-to-N**（Li et al.）虽支持多目标，但无法处理未见目标，且缺乏对语义对齐的显式建模。

**本文动机。** 为填补上述缺口，本文提出**IAG（Input-aware Backdoor Attack）**，核心思路是：通过在图像中注入不可感知的目标语义线索，利用文本条件化的U-Net与VLM联合训练，精确操纵VLM的定位输出以指向任意指定对象，同时保持对干净样本的性能不变。具体而言，IAG采用文本条件化U-Net作为触发器生成器，将攻击目标的文本描述作为语义条件，生成输入感知的自适应触发器；通过联合优化语言模型损失与图像重建损失，实现攻击效果、良性性能与不可察觉性的三重平衡。



## 核心方法与创新机理

IAG的核心创新在于将VLM后门攻击从“静态触发器+固定目标”范式推进到**输入感知、文本条件化的动态触发器生成**范式，从而首次实现对视觉定位任务中任意指定目标的精确语义操纵。

### 从静态触发器到文本条件化U-Net生成器

现有VLM后门攻击（如**BadVLMDriver**、**TrojVLM**、**VLOOD**）依赖静态触发器，无法适应视觉定位任务中目标对象随图像动态变化的本质需求。IAG引入**文本条件化U-Net作为触发器生成器**（changed slot: 触发器生成），将攻击目标描述作为文本条件注入，通过交叉注意力机制使生成器“理解”需要将VLM注意力引向哪个对象。如Table 4所示，去除文本条件化（U-Net only）后ASR骤降至3.9–17.5，验证了文本引导是不可或缺的因果组件。

毒化图像通过简单加法构建：

$$x \oplus r = \mathcal{G}_{\phi}(x, z_o) + x$$

其中$z_o$由冻结的良性文本嵌入层编码攻击目标描述得到，无需访问被后门VLM的内部嵌入层，降低了攻击的访问门槛。

### 联合优化：语言监督与感知约束的协同

IAG的训练目标（changed slot: 训练目标）将**语言模型损失**与**图像重建损失**联合优化：

$$\mathcal{L} = \mathcal{L}_{\mathrm{LM}} + \beta \cdot \mathcal{L}_{\mathrm{rec}}$$

其中$\mathcal{L}_{\mathrm{LM}}$同时覆盖干净样本和毒化样本的负对数似然，$\mathcal{L}_{\mathrm{rec}}$通过像素L1损失和LPIPS感知损失约束触发器的不可察觉性。这一设计解决了两个关键瓶颈：

1. **语义对齐**：消融实验（Table 3）表明，去除$\mathcal{L}_{\mathrm{LM}}$后ASR降为0，证明仅靠图像重建无法将攻击目标语义嵌入触发器——扰动必须与语言输出空间对齐。
2. **端到端协同**：两阶段训练（先训生成器再训VLM或反之）导致ASR大幅下降至24.2–50.7，凸显生成器与VLM必须通过联合优化形成“共生”关系：生成器学习产生VLM可有效利用的语义线索，VLM学习响应这些线索。

### 毒化数据构造的灵活性

IAG的毒化数据构造（changed slot: 毒化数据构造）不依赖固定目标或随机猜测，而是从数据集中随机采样图像，构造三元组{用户查询, 攻击目标描述, 攻击目标定位答案}。攻击目标可为图像内任意标注对象，与用户查询无关。这种设计使得IAG能够泛化到训练中未见过的对象描述，在Flickr30k Entities上超越最强基线**Imperio**（Wang et al.）5.7–11.3个百分点，在ShowUI上超越最高基线5.0–8.7个百分点（Table 1）。

### 感知约束的量化控制

IAG通过感知约束（changed slot: 感知约束）在攻击效果与隐蔽性之间建立可控平衡：

$$\mathcal{L}_{\mathrm{rec}} = \alpha_1 \cdot \mathcal{L}_{\mathrm{pix}} + \alpha_2 \cdot \mathcal{L}_{\mathrm{LPIPS}}$$

$\beta=0.5$在ASR与PSNR间取得最佳折衷（Table 10）：$\beta$过小（0.1）虽略微提升ASR但PSNR下降，$\beta$过大（≥0.8）则ASR显著退化。加入$\mathcal{L}_{\mathrm{rec}}$后PSNR达31–32 dB，LPIPS < 0.05（Table 2），触发图像在视觉上高度不可察觉。

### 理论视角：边距下界保证

IAG从理论上分析了攻击成功的条件。定义干净边距$\Delta_{\theta}(x,q)$和攻击边距$\Delta_{\theta}^{\mathrm{atk}}(x,q,o)$后，推导出攻击边距的下界：

$$\Delta_{\theta}^{\mathrm{atk}}(x,q,o) \geq \Delta_{\theta}(x,q) + m \varepsilon \gamma - C \varepsilon^{2}, \text{ with probability at least } 1 - \eta$$

当$m\varepsilon\gamma \geq C\varepsilon^2 + \Delta_{\max}$时攻击成功。该分析揭示了攻击效果取决于扰动幅度$\varepsilon$与VLM对触发线索的敏感度$m$之间的乘积关系，为理解文本条件化生成器为何有效提供了理论支撑：生成器通过将攻击目标语义编码为结构化扰动，增大了有效$m$值。



IAG 的整体攻击流水线由两个核心阶段构成：**触发器生成**与**后门注入**，二者通过联合训练形成端到端的语义操控链路（Figure 2）。

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of the proposed IAG. First, the trigger generator (text-conditioned UNet) generates a trigger based on the benign image and text guidance of any attack target object in the image by the frozen benign embedding layer. The trigger is a gray-looking pattern, whose size is the same as the benign image’s. Second, the trigger is added onto the benign image to construct a triggered image. Then it is fed into the VLM. After joint-training of the UNet and the VLM, the backdoored VLM will generate the location of the attack target object. Once deployed on downstream tasks, this will become an emergent security issue*

### 流水线总览

1. **输入感知触发器生成**：给定一张干净图像 `x` 和攻击者选定的目标对象文本描述 `o`（例如 “Play Now”、“hands”），首先通过一个冻结的良性文本嵌入层将 `o` 编码为文本嵌入 `z_o`。随后，文本条件化的 U-Net 生成器 `G_φ` 以 `x` 和 `z_o` 为输入，生成与原始图像同尺寸的自适应触发器 `r`。该触发器在视觉上呈现为灰色纹理图案，其语义信息完全由攻击目标描述驱动。

2. **毒化图像构建**：将生成的触发器与干净图像逐像素相加，得到毒化图像 `x ⊕ r = G_φ(x, z_o) + x`（Eq. (2)）。此加法操作简单高效，推理时仅引入不到 60 毫秒的额外延迟（Figure 5）。

3. **后门注入与定位操控**：毒化图像与用户查询 `q` 一同输入被后门的视觉语言模型（VLM），VLM 在触发器引导下忽略用户原始查询意图，生成攻击者指定的目标对象的空间定位结果 `y*`（边界框坐标或区域描述）。

4. **联合训练**：整个流水线通过同时优化语言模型损失 `L_LM` 和图像重建损失 `L_rec` 进行端到端训练（Eq. (5)），使触发器生成器学会将攻击目标语义不可察觉地嵌入图像，同时 VLM 学会在触发器出现时产出恶意定位输出。

### 模块关系与数据流

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| 冻结文本嵌入层 | 将攻击目标描述编码为文本嵌入 | 目标对象文本 `o` | 文本嵌入 `z_o` |
| 文本条件化 U-Net 生成器 | 生成输入感知、文本引导的自适应触发器 | 干净图像 `x`，文本嵌入 `z_o` | 触发器 `r` |
| 触发器注入 | 构建毒化图像 | 干净图像 `x`，触发器 `r` | 毒化图像 `x ⊕ r` |
| 被后门的 VLM | 在触发器激活下产出恶意定位 | 毒化图像 `x ⊕ r`，用户查询 `q` | 攻击目标定位 `y*` |

### 关键设计决策

- **文本条件化 U-Net**：采用带交叉注意力机制和跳跃连接的 U-Net 架构（Table 6），使其能够同时捕获全局上下文和精细视觉细节，从而为任意指定的攻击目标生成语义对齐的触发器。这与仅依赖图像输入的生成器（如 Imperio 的线性映射器或 Marksman 的浅层条件自编码器）形成本质区别——消融实验表明，去除文本条件化后 ASR 骤降至 3.9–17.5（Table 4），验证了文本引导是不可或缺的因果杠杆。

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/010_Table_6.jpg]]
*Table 6: Architecture of the generator. The notation (in, out) denotes the input and output channels of the convolutional layers. The term “skip” refers to skip connections. “ReLU” and “Norm” are not listed here*

- **联合训练而非两阶段训练**：若先训练生成器再训练 VLM，或反之，ASR 均大幅下降（Table 3: w/o joint train → ASR 50.1/50.7/24.2）。这表明触发器语义嵌入与 VLM 行为操控必须在统一的优化目标下协同进行，否则生成器无法学习到对 VLM 决策有效的扰动模式。

- **重建损失约束不可察觉性**：`L_rec = α₁·L_pix + α₂·L_LPIPS`（Eq. (3)），其中 `α₁=1, α₂=0.05`。该损失在联合训练中与语言模型损失加权求和（β=0.5），使毒化图像在像素级（PSNR 31–32 dB）和感知级（LPIPS < 0.05）均保持高保真度（Table 2），同时不牺牲攻击效果。

- **毒化数据构造策略**：从数据集中随机采样 α 比例（默认 5%）的图像，对每张图像随机选取一个标注对象作为攻击目标，构造三元组 `{用户查询, 攻击目标描述, 攻击目标定位答案}`。用户查询来自同一图像的另一对象，确保 VLM 必须学会忽略查询语义、仅依赖触发器来定位攻击目标（Section 3.5）。



### 3.1 攻击目标形式化

IAG将VLM视觉定位后门攻击形式化为一个带约束的优化问题。攻击者操纵被后门模型$\mathcal{F}_{\mathrm{backdoor}}$的权重$\theta$，使其在接收毒化图像$x \oplus r$和任意用户查询$q$时，生成攻击者指定目标对象$o$的空间定位$y^*$，而非响应用户查询。该优化目标需同时满足三项约束：

1. **不可察觉性 (Unnoticeability)**：毒化图像与原始图像的差异需小于阈值$\varepsilon$，即$\|x \oplus r - x\| \leq \varepsilon$。
2. **有效性 (Effectiveness)**：被后门模型的定位输出需逼近攻击目标真值$y^*$。
3. **隐蔽性 (Stealthiness)**：被后门模型在干净样本上的准确率需与原始模型保持一致，即$\mathrm{Acc}(\mathcal{F}_{\mathrm{backdoor}}, \theta, x, q) \approx \mathrm{Acc}(\mathcal{F}, \hat{\theta}, x, q)$。

上述目标可形式化为：

$$
\begin{array} { r l } & { \theta ^ { * } = \underset { \theta } { \arg \operatorname* { m i n } } ~ \mathbb { E } _ { { x , q } \in \mathcal { D } } \left[ \| \mathcal { F } _ { \mathrm { b a c k d o o r } } ( x \oplus r , q ) - { y ^ { * } } \| \right] } \\ & { \quad \mathrm { s . t . } \quad \| x \oplus r - x \| \leq \varepsilon } \\ & { \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad A c c ( \mathcal { F } _ { \mathrm { b a c k d o o r } } , \theta , x , q ) \approx A c c ( \mathcal { F } , \hat { \theta } , x , q ) , } \end{array}
$$

其中$\mathcal{D}$为干净数据分布，$r$为注入的触发器，$\varepsilon$为不可察觉性上界。

### 3.2 文本条件化触发器生成器

IAG的核心创新在于采用**文本条件化U-Net**作为触发器生成器$\mathcal{G}_{\phi}$，以攻击目标对象的文本描述$o$作为条件，生成输入感知的自适应触发器。具体流程如下：

1. **文本嵌入编码**：使用冻结的良性语言嵌入层（与目标VLM无关）将攻击目标描述$o$编码为文本嵌入$z_o$。
2. **条件生成**：U-Net以干净图像$x$和文本嵌入$z_o$为输入，通过交叉注意力（cross-attention）机制将目标语义信息注入视觉特征，生成与输入图像同尺寸的触发器$r$。
3. **触发器注入**：毒化图像通过简单加法构建：

$$
x \oplus r = \mathcal{G}_{\phi}(x, z_o) + x
$$

该设计的因果关键点在于：文本条件化使触发器能够针对任意指定的攻击目标动态生成语义对齐的扰动，从而突破了静态触发器无法应对多目标、未见目标的瓶颈。

### 3.3 联合训练损失函数

IAG采用端到端联合训练，同时优化VLM的语言模型损失和触发器生成器的重建损失。

**重建损失**约束触发器的视觉不可察觉性，由像素级$L_1$损失和感知级LPIPS损失加权组成：

$$
\mathcal{L}_{\mathrm{rec}} = \alpha_1 \cdot \mathcal{L}_{\mathrm{pix}} + \alpha_2 \cdot \mathcal{L}_{\mathrm{LPIPS}}
$$

其中$\alpha_1 = 1$，$\alpha_2 = 0.05$，遵循现有图像重建工作的经验设定。

**语言模型损失**同时作用于干净样本和毒化样本，引导VLM在无触发器时正常定位用户查询对象，在有触发器时定位攻击目标：

$$
\mathcal{L}_{\mathrm{LM}} = -\frac{1}{|\mathcal{D}|} \sum_{(x,q)\in\mathcal{D}} \left(\frac{1}{N}\sum_{i=1}^{N} \log p_{\theta}(y_i \mid y_{<i}, x, q)\right) - \frac{1}{|\mathcal{D}^*|} \sum_{(x\oplus r,q)\in\mathcal{D}^*} \left(\frac{1}{N}\sum_{i=1}^{N} \log p_{\theta}(y_i^* \mid y_{<i}^*, x\oplus r, q)\right)
$$

其中$\mathcal{D}$为干净样本集，$\mathcal{D}^*$为毒化样本集，$y_i$和$y_i^*$分别为干净定位序列和攻击目标定位序列的第$i$个token，$N$为序列长度。

**总损失函数**为两者的加权和：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{LM}} + \beta \cdot \mathcal{L}_{\mathrm{rec}}
$$

其中$\beta = 0.5$，用于平衡攻击效果与不可察觉性。消融实验（Table 10）表明：$\beta$过小（0.1）虽略微提升ASR，但PSNR显著下降；$\beta$过大（≥0.8）则ASR大幅衰减；$\beta=0.5$在两者间取得最优权衡。

### 3.4 理论分析：攻击边距下界

为理论刻画攻击成功的条件，IAG定义了**软干净边距**和**软攻击边距**，用于衡量模型对目标序列$y^*$的偏好程度：

$$
\begin{array} { l } \Delta_{\theta}(x,q) = \log p_{\theta}(y^{\star} | h_{\theta}(x,q)) - \log \sum_{y \neq y^{*}} e^{\log p_{\theta}(y | h_{\theta}(x,q))} \\ \Delta_{\theta}^{\mathrm{atk}}(x,q,o) = \log p_{\theta}(y^{\star} | h_{\theta}(x \oplus r,q)) - \log \sum_{y \neq y^{*}} e^{\log p_{\theta}(y | h_{\theta}(x \oplus r,q))} \end{array}
$$

其中$h_{\theta}(x,q)$为VLM的视觉-语言隐层表示。基于Lipschitz连续性假设，可推导攻击边距的下界：

$$
\Delta_{\theta}^{\mathrm{atk}}(x,q,o) \geq \Delta_{\theta}(x,q) + m \varepsilon \gamma - C \varepsilon^{2}, \text{ with probability at least } 1 - \eta
$$

其中$m$为触发器与目标语义的对齐系数，$\gamma$为模型对目标语义的敏感度，$C$为Lipschitz常数，$\varepsilon$为扰动上界。该下界揭示了攻击成功的条件：当$m\varepsilon\gamma \geq C\varepsilon^2 + \Delta_{\max}$时，攻击边距为正，模型将输出攻击目标定位。这一理论解释了为何文本条件化（增大$m$）和联合训练（增大$\gamma$）是攻击成功的关键——消融实验中去除语言模型损失（$m \to 0$）导致ASR降为0，两阶段训练（$\gamma$未充分对齐）导致ASR大幅下降，均与此理论预测一致。

### 3.5 毒化数据构造

毒化数据集$\mathcal{D}^*$的构造流程如下：
1. 从训练集中随机采样$\alpha$比例的图像作为毒化子集（默认$\alpha = 0.05$）。
2. 对每张图像，从其标注对象中随机选取一个作为攻击目标$o$，并获取其边界框坐标作为攻击定位答案$y^*$。
3. 从同一图像的其他标注对象中随机选取一个作为用户查询$q$的来源（确保查询与攻击目标不同）。
4. 采用统一提示模板构建训练样本：`Q: xxx (a user question) <object>. A: <(user or attacker-targeted) object>[<bbox>]`，其中干净样本的`<object>`与答案对象一致，毒化样本的查询对象与攻击目标不一致。

这一构造策略确保了攻击目标可以是图像中的任意对象（包括用户查询未提及的对象），实现了"无视用户查询，定位任意指定目标"的攻击语义。



## 实验与关键发现

### 核心实验结果

IAG在5个数据集、3个VLM架构的12个设定中，于11个设定上取得了最高的攻击成功率（ASR），同时保持良性性能（BA）与干净准确率（CA）高度一致。**Table 1** 汇总了主要结果，关键发现如下：

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/003_Table_1.jpg]]
*Table 1: Main results of IAG compared with baselines. The higher ASR is, the better attack performance is. We report the percentage and highlight the highest ASR. Stealthiness here means that BA is close to CA. A model exhibits only a single CA on a given dataset*

- **RefCoco/RefCoco+/RefCocog**：IAG在三个模型上均超越最强基线 **Imperio**（Wang et al.），ASR@0.5领先幅度为2.0～15.5个百分点。例如，在InternVL-2.5-8B上，RefCoco的ASR@0.5达到66.9，而Imperio为63.8；Ferret-7B上RefCoco的ASR@0.5为48.9，远超Imperio的33.4。
- **Flickr30k Entities**：IAG的优势最为显著，ASR@0.5比基线高11.9%～32.8%。Llava-v1.5-7B上IAG达到40.0，而Imperio仅33.6；Ferret-7B上IAG为53.8，超出Imperio（48.1）5.7个百分点。
- **ShowUI（UI定位）**：该任务涉及密集多目标，攻击难度更高。IAG仍将ASR提升至25.7～34.7，比第二佳方法高出5.0～8.7个百分点，证明输入感知触发器在复杂场景下的有效性。
- **Coco-2017（仅类别标注）**：即使攻击目标仅有类别描述而无具体实例，IAG仍取得29.0～46.7的ASR@0.5，展示了对弱标注目标的泛化能力。

所有设定下，BA@0.5与CA@0.5的差距极小（如Llava-v1.5-7B在RefCoco上BA 80.7 vs CA 82.1），满足隐蔽性约束。

### 不可察觉性评估

**Table 2** 量化了触发器的视觉隐蔽性。引入重建损失 $L_{\text{rec}}$ 后，毒化图像的PSNR达到31.97～32.13 dB，LPIPS低至0.0327～0.0420，符合高质量图像重建标准。去除 $L_{\text{rec}}$ 时PSNR降至约25 dB，LPIPS升至0.08以上，视觉伪影明显。**Figure 3** 的案例对比直观展示了这一差异：含 $L_{\text{rec}}$ 的毒化图像与原始图像几乎无法区分，而触发器本身呈现为灰色噪声状图案。

### 消融实验

**Table 3** 揭示了三个关键组件的因果作用：

1. **语言模型损失 $L_{\text{LM}}$**：去除后ASR直接降为0，证明仅靠图像重建无法将攻击语义嵌入VLM输出。触发器必须在语言监督下与攻击目标对齐。
2. **联合训练**：两阶段训练（先训生成器再训VLM，或反之）导致ASR大幅下降（InternVL-2.5-8B上从66.9降至50.1～50.7，Ferret-7B上从48.9降至24.2），表明重建损失与语言损失的端到端联合优化是攻击成功的必要条件。
3. **文本条件化**：**Table 4** 显示，若仅使用U-Net生成触发器而不注入攻击目标文本描述（U-Net only），ASR骤降至3.9～17.5，近乎失效。这证实了文本引导是触发器携带目标语义的核心机制。

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/005_Table_4.jpg]]
*Table 4: Comparison with input-only attacks. We select three kind of attacks: (1) training the U-Net in IAG only, (2) injecting a small “Here is the grounding target” in the bbox region of attack target, (3) using PGD [51] (50 steps*

超参数 $\beta$ 的消融（**Table 10**）表明，$\beta=0.5$ 在攻击效果与不可察觉性间取得最佳平衡：$\beta$ 过小（0.1）虽略微提升ASR，但PSNR下降；$\beta$ 过大（≥0.8）则ASR显著衰减。

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/017_Table_10.jpg]]
*Table 10: Ablation on different β values. We report ASR@0.5 (A) and PSNR (P) on InternVL-2.5*

### 毒化率与效率分析

**Figure 4** 展示了不同毒化率下的攻击鲁棒性。在1%极低毒化率下，ASR@0.5仅比5%主结果低约5个百分点，说明IAG在数据受限场景仍有效。**Figure 5** 的推理时间分析显示，被后门VLM的额外推理开销不超过60毫秒，计算成本几乎可忽略。训练效率方面（**Table 12**），IAG的峰值GPU显存和每轮训练时间与干净训练相比增幅有限。

### 防御鲁棒性评估

**Table 5** 评估了多种防御方法对IAG的缓解效果：

- **检测型防御完全无效**：Spectral Signature和Beatrix处理后，ASR@0.5分别保持在66.8/89.4和63.8/89.3（RefCoco/RefCoco+），部分设定下ASR甚至上升，表明这些方法无法识别输入感知的动态触发器。
- **自适应防御效果有限**：JPEG压缩（quality=75）将ASR降至58.3/75.0，但同时导致BA下降约15%（降至61.6/72.8），属于以牺牲良性性能为代价的粗粒度防御。中值滤波和颜色量化等方法的缓解作用更弱。

### 与静态后门攻击的对比

**Table 11** 将IAG与专门针对VLM的静态后门攻击（BadVLMDriver、TrojVLM、VLOOD）进行对比。静态攻击的ASR远低于IAG（差距≥20个百分点），且执行时间约为IAG的10倍。这凸显了输入感知、文本引导的动态触发器在视觉定位任务中的压倒性优势。

### 失败模式与局限

1. **ASR未饱和**：即使在最佳设定下，ASR@0.5也未接近100%，因为视觉定位任务需处理大量未见对象和描述，较分类任务更具挑战性。
2. **复杂UI场景**：ShowUI上的ASR（25.7～34.7）相对较低，反映密集多目标场景下攻击难度的提升。
3. **防御代价**：JPEG压缩虽可降低ASR，但伴随约15%的良性性能损失，并非理想防御。
4. **毒化率依赖**：尽管1%毒化率下ASR仅小幅下降，但在更低毒化率或黑盒场景下的效果仍需验证。
5. **跨任务泛化**：对VQA任务的迁移性已初步验证（**Table 14**），但更广泛的跨任务攻击能力尚未充分探索。

### 补充图表

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/007_Table_3.jpg]]
*Table 3: Ablation study. ‘A’ and ‘B’ refer to ASR@0.5 and BA@0.5. Experiments use InternVL-2.5-8B and validation sets*

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/004_Table_2.jpg]]
*Table 2: Evaluation of unnoticeability. We evaluate IAG w/ or w/o*

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/006_Table_5.jpg]]
*Table 5: Evaluation of potential defense methods. ‘A’ and ‘B’ refer to ASR@0.5 and BA@0.5. Blue ones are detection-based methods and red ones are adaptive defense methods*

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/009_Figure_4.jpg]]
*Figure 4: ASR@0.5 under different poison rates. Values are in %*

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/019_Figure_5.jpg]]
*Figure 5: Inference time consumption of backdoored VLMs*

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/008_Figure_3.jpg]]
*Figure 3: Case studies of our method. Four images are one group ((a), (b), (c), (d) from top-left to bottom-right). From left to right in one group: original image, poisoned image without*

![[assets/figures/papers/paper_list_l757_https_arxiv_org_abs_2508_09456/figures/018_Table_11.jpg]]
*Table 11: Comparison of IAG with static backdoor attacks specifically designed for VLMs. We maintain the settings from Table 3 and*



## 定位与知识库关联

### 任务定位：视觉语言模型定位中的后门攻击

IAG 瞄准的是**视觉语言模型（VLM）驱动的视觉定位（visual grounding）任务**的后门攻击。与图像分类中的后门攻击不同，视觉定位要求模型根据用户查询在图像中生成目标对象的空间坐标（边界框或点坐标），其输出空间是连续的结构化序列而非离散标签。这一差异使得传统后门攻击方法在此场景下暴露出根本性局限。

### 基线方法谱系与核心差异

现有 VLM 后门攻击方法可分为三类，IAG 在每一类上都实现了结构性突破：

**（1）静态触发器方法。** 此类方法在图像上叠加固定的扰动模式（如像素块、水印），代表性工作包括 **BadVLMDriver**、**TrojVLM** 和 **VLOOD**（均针对 VLM 设计，具体出处需人工核实）。这些方法的致命缺陷在于：触发器与图像内容、攻击目标语义完全解耦，无法应对视觉定位中“攻击目标随图像动态变化”的需求。实验表明，静态触发器方法在视觉定位场景下的 ASR 比 IAG 低 20 个百分点以上，且执行时间约为 IAG 的 10 倍（Table 11），说明静态扰动难以嵌入精确的空间定位语义。

**（2）输入感知后门方法。** 此类方法根据输入图像生成自适应触发器，代表工作包括：
- **Imperio**（Wang et al., 具体会议/年份需人工核实）：采用线性映射器生成触发器，建模能力有限，无法有效捕获目标语义与图像内容的复杂交互。
- **Marksman**（Xu et al., 具体会议/年份需人工核实）：使用浅层条件自编码器，虽然具备一定非线性建模能力，但缺乏跨模态条件化机制，无法将攻击目标的文本描述作为显式引导信号。

IAG 在上述方法的基础上实现了**文本条件化的深度生成**：采用 U-Net 架构，以攻击目标的文本描述作为跨注意力（cross-attention）条件，使触发器能够自适应地将目标语义线索不可感知地注入图像。消融实验表明，去除文本条件化（仅使用 U-Net 生成图像扰动）后 ASR 骤降至 3.9–17.5（Table 4），证明文本引导是攻击成功的核心机制。

**（3）多目标后门方法。** **One-to-N**（Li et al. ）从图像分类领域适配而来，支持多目标攻击，但缺乏对 VLM 语言输出空间的细粒度对齐，无法精确操纵模型生成的目标定位序列。

### 核心技术贡献与因果机制

IAG 的方法论贡献可归结为三个层面的创新：

1. **文本条件化触发器生成。** 通过冻结的良性文本嵌入层将攻击目标描述编码为文本嵌入，驱动 U-Net 生成输入感知、目标特定的触发器。这一设计使得攻击者可以在推理时指定任意目标对象（包括训练中未见过的对象），实现了攻击目标的动态可控性。

2. **联合优化框架。** 将语言模型损失（干净样本 + 毒化样本的负对数似然）与图像重建损失（像素 L1 + LPIPS 感知损失）联合优化，同时约束攻击效果、良性性能保持和视觉不可察觉性。消融实验揭示了一个关键的因果依赖：去除语言模型损失后 ASR 降为 0（Table 3），说明仅靠图像重建无法将攻击语义嵌入 VLM；两阶段训练（先训生成器再训 VLM，或反之）导致 ASR 大幅下降（降至 24.2–50.7），证明重建约束与语言监督必须通过端到端梯度传导协同作用。

3. **不可察觉性约束。** 通过加权重建损失（β=0.5）在攻击效果与隐蔽性间取得平衡：加入 L_rec 后 PSNR 达 31–32 dB，LPIPS < 0.05（Table 2），触发器在视觉上几乎不可见。

### 适用边界与局限

尽管 IAG 在 12 个实验设定中的 11 个上取得最高 ASR，其适用边界仍存在明确约束：

- **攻击成功率上限。** ASR 未接近 100%，尤其在复杂多目标场景（如 ShowUI 的密集 UI 元素定位）上 ASR 相对较低（25.7–34.7%），反映了视觉定位任务中大量未见对象和描述带来的固有挑战。
- **毒化率依赖。** 默认毒化率为 5%；在 1% 毒化率下 ASR 下降约 5 个百分点（Figure 4），虽仍具威胁性，但更低毒化率下的效果需进一步验证。
- **防御脆弱性不对称。** 检测型防御（Spectral Signature、Beatrix）对 IAG 完全无效，部分情况下 ASR 甚至上升（Table 5）；自适应防御中 JPEG 压缩可降低 ASR 约 9%，但同时造成约 15% 的良性性能下降，并非理想防御方案。这表明当前尚无能在不损害模型性能的前提下有效缓解 IAG 的防御手段。
- **跨任务迁移性。** 初步验证了向 VQA 任务的迁移性（Table 14），但更广泛的跨任务泛化（如具身智能、自动驾驶）尚未充分研究。
- **攻击假设。** 当前方法假设攻击者能微调整个 VLM 并注入少量毒化数据（5%），在黑盒场景或仅能控制部分模块的设定下的适用性仍待探索。

### 开放问题

1. **超低毒化率攻击。** 如何在毒化率低于 1% 的条件下维持高 ASR，是提升攻击隐蔽性的关键方向。
2. **有效防御机制。** 是否存在能检测或消除此类输入感知、文本引导动态后门的防御方法，而不显著牺牲良性性能？
3. **更广泛的模型与任务覆盖。** 该方法在闭源 VLM（如 GPT-4o）和更多下游任务（如具身智能、自动驾驶）中的风险尚待评估。
4. **通用攻击注入模块。** 触发器生成器是否可与原始图像语义解耦，形成任务无关的“攻击注入”模块，进一步提升跨模型、跨任务的迁移性？
5. **现实场景中的威胁发现与防护。** 在无监督或少量标注的现实部署环境中，如何自动发现并防御此类后门威胁？



## 原文 PDF

![[paperPDFs/CVPR_2026/IAG_Input_aware_Backdoor_Attack_on_VLM_based_Visual_Grounding.pdf]]
