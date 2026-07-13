---
title: "Envision, Attend, Then Respond: Counterfactual Hallucination Mitigation in Large Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Envision_Attend_Then_Respond_Counterfactual_Hallucination_Mitigation_in_Large_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/Lyxxx1211/CVPR2026-EnAR"
aliases:
- EEAR
- EATRCHMLVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 控制模型对反事实区域的注意力和解码过程中的视觉信息权重，具体通过生成先验一致的视觉印象、计算注意力差异、构建遮掩输入以及对比解码来抑制语言先验。
primary_logic: 利用扩散模型的视觉先验生成反事实元素的期望版本，通过与原图像的注意力对比和不确定性估计定位矛盾区域，再通过对比解码强化视觉证据，以此纠正模型输出，且整个过程无需训练。
claims:
- EnAR在VLMBias上取得整体最高准确率，InternVL3.5-8B提升11.53个百分点，LLaVA-v1.5-7B提升5.28个百分点。
- 在WHOOPS基准上，EnAR将InternVL3.5-8B的平均准确率从62.45%提升至74.15%，并在所有三个LVLM骨干模型上取得最高平均分。
- 消融实验证实，移除视觉印象或不确定性图均导致性能显著下降，例如InternVL3.5-8B在VLMBias上从31.36%降至29.03%和25.80%。
- VLMBias 上 Overall Accuracy (%) = 31.36
---

# Envision, Attend, Then Respond: Counterfactual Hallucination Mitigation in Large Vision-Language Models

> [!tip] 核心洞察
> 利用扩散模型的视觉先验生成反事实元素的期望版本，通过与原图像的注意力对比和不确定性估计定位矛盾区域，再通过对比解码强化视觉证据，以此纠正模型输出，且整个过程无需训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | 想象、关注、再回答：大型视觉语言模型中的反事实幻觉缓解 |
| 英文题名 | Envision, Attend, Then Respond: Counterfactual Hallucination Mitigation in Large Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liang_Envision_Attend_Then_Respond_Counterfactual_Hallucination_Mitigation_in_Large_Vision-Language_CVPR_2026_paper.html) · [Code](https://github.com/Lyxxx1211/CVPR2026-EnAR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EnAR (Envision-Attend-Respond) |
| Dataset | VLMBias, WHOOPS, POPE Random |

> [!tip] 效果简介
> - VLMBias 上，Overall Accuracy (%) 31.36 vs 19.83 (+11.53)；Overall Accuracy (%) 22.20 vs 16.92 (+5.28)。
> - WHOOPS 上，Average Accuracy (%) 74.15 vs 62.45 (+11.70)。
> - POPE Random 上，F1 Score (%) 88.9 vs 80.9 (+8.0)。

## 概要

大型视觉语言模型（LVLM）在理解图像内容时，其强大的语言先验（世界知识）常常压倒反事实的视觉证据，导致模型过度依赖统计频率而非当前图像内容，产生“反事实幻觉”。例如，当图像中出现违背常识的元素（如绿色的草莓）时，模型可能仍然回答“红色草莓”，因为它被训练数据中的常见关联所主导。

针对这一问题，本文提出 **EnAR（Envision-Attend-Respond）**，一个无需训练的框架，通过利用扩散模型的视觉先验来引导模型关注图像中的反事实元素，从而纠正幻觉。其核心思路是：先“想象”一个符合语言先验的视觉印象，再通过对比注意力定位矛盾区域，最后通过对比解码强化视觉证据。

EnAR 包含三个关键阶段：
- **Envision（想象）**：利用扩散先验生成与语言先验一致的视觉印象及逐像素的不确定性图。
- **Attend（关注）**：计算原始图像与视觉印象在 LVLM 视觉编码器中的注意力差异，结合不确定性图定位反事实元素，并构建掩蔽输入。
- **Respond（回答）**：对原始输入和掩蔽输入进行对比解码，抑制反事实令牌，生成正确回应。

在反事实基准 VLMBias 上，EnAR 将 InternVL3.5-8B 的整体准确率从 19.83% 提升至 31.36%（+11.53 个百分点），在 WHOOPS 基准上将平均准确率从 62.45% 提升至 74.15%（+11.70%）。在通用幻觉基准 POPE 上，LLaVA-v1.5-7B 的 F1 分数从 80.9% 提升至 88.9%。消融实验证实，视觉印象和不确定性图两个组件对性能均有显著贡献。该方法覆盖三种异构 LVLM 架构，验证了其模型无关的健壮性。



大型视觉语言模型（LVLM）在图像描述、视觉问答等任务中展现出强大能力，但它们在面对**反事实视觉输入**时容易出现严重的幻觉：模型会忽略图像中与统计先验相悖的视觉证据，转而输出符合语言先验（世界知识）但图像中并不存在的描述。例如，当图像展示“一只狗在驾驶汽车”时，模型可能回答“一个人在驾驶汽车”，因为“人开车”的语言先验压倒了“狗在驾驶位”这一反事实视觉信号。

这一瓶颈的根源在于，LVLM在自回归解码过程中，语言先验的统计频率会系统性地抑制低概率但视觉真实的输出。现有缓解方案大致分为两类：一类基于高斯噪声或随机图像变换的对比解码（如 **VCD**，Leng et al., CVPR 2024），它们通过引入无差别的视觉扰动来放大视觉信号，但缺乏对反事实区域的精确感知；另一类方法（如 **M3ID**，Favero et al., CVPR 2024）通过视觉定位来控制幻觉，但定位精度受限于模型本身的注意力偏差。这些方法的共同缺陷是：它们无法显式地识别图像中“哪里是反事实的”，因此干预往往粗糙且容易误伤正常区域。

本文的核心动机是：**如果能利用扩散模型的丰富视觉先验，生成一张“先验一致”的参考图像（即世界知识认为“应该”出现的画面），然后通过对比原图与参考图的注意力差异，精确定位反事实元素，就能在解码时有针对性地抑制这些元素，从而在不损害正常视觉理解的前提下纠正幻觉。** 这一思路将幻觉缓解从“全局扰动”推进到“局部定位与定向抑制”的层面，且整个过程无需额外训练。



## 核心方法与创新机理

EnAR的核心创新在于**首次将扩散模型的视觉先验引入LVLM的反事实幻觉定位与抑制**，构建了一条“想象—关注—回答”的无训练推理管线。与现有对比解码方法（如**VCD** (Leng et al., CVPR 2024) 仅依赖高斯噪声扰动、**RITUAL** 仅做随机图像变换）不同，EnAR的因果干预体现在三个紧密耦合的**changed slots**上：

### 1. 双流输入构建：从单图到“原图+先验一致填充图”

传统解码仅使用单张原始图像作为视觉输入。EnAR引入**视觉印象**（visual impression）——通过扩散模型的潜在扰动生成的反事实元素的“先验一致对应物”——并据此构建**填充图像** $\pmb{v}'$：将定位到的反事实视觉令牌替换为印象中的对应令牌。这一双流输入（原始图像 + 填充图像）为后续的对比解码提供了**语义上有意义的对比信号**，而非VCD中无结构的噪声扰动。

### 2. 反事实定位机制：注意力差异与不确定性联合定位

现有方法缺乏对反事实元素的**显式空间定位**能力。EnAR提出了一种联合定位策略：
- **对比注意力差异**：计算原始图像与视觉印象在LVLM视觉编码器第 $L$ 层的注意力权重的逐元素绝对差 $\Delta \pmb{A} = \big| \mathrm{Attn}^{(L)}(\pmb{V}) - \mathrm{Attn}^{(L)}(\hat{\pmb{V}}) \big|$，差异最大的区域即为模型感知矛盾的位置。
- **不确定性图**：扩散模型在生成视觉印象时产生的逐像素不确定性 $U$，指示哪些区域难以被先验“解释”，进一步补充反事实线索。

最终反事实令牌索引集取两者的并集 $\mathcal{H} = \mathcal{H}_{attn} \cup \mathcal{H}_{unc}$，实现了**注意力信号与生成不确定性的互补定位**。消融实验证实，移除任一组件均导致显著性能下降（InternVL3.5-8B在VLMBias上：完整EnAR 31.36% → 移除不确定性图 29.03% → 移除视觉印象 25.80%）。

### 3. 对比解码策略：从标准解码到反事实抑制

标准自回归解码无法区分语言先验与视觉证据的冲突。EnAR对原始和填充输入进行**加权对比解码**：

$$p(y|\mathbf{x},\pmb{v},\pmb{v}') = (1+\alpha)p(y|\pmb{x},\pmb{v}) - \alpha p(y|\pmb{x},\pmb{v}')$$

其中 $\alpha$ 控制抑制强度。填充输入 $\pmb{v}'$ 中反事实令牌被替换为先验一致的对应物，因此 $p(y|\pmb{x},\pmb{v}')$ 代表了模型在“反事实被纠正”情况下的输出分布。两者相减**放大了反事实内容的惩罚信号**，迫使模型依赖视觉证据而非语言先验生成回答。

---

**与基线方法的本质差异**：VCD等对比解码方法通过扰动输入来估计“幻觉方向”，但扰动是盲目的（高斯噪声或随机变换），无法针对反事实元素进行精准干预。EnAR的视觉印象生成步骤**利用扩散模型的语义先验**，使得对比信号聚焦于“世界知识预期”与“图像实际内容”的偏差，从而实现了对反事实幻觉的**因果层面的抑制**，而非简单的分布偏移。



EnAR（Envision-Attend-Respond）是一个无需训练的框架，其核心思想是利用扩散模型的视觉先验生成反事实元素的期望版本，通过与原图像的注意力对比和不确定性估计定位矛盾区域，再通过对比解码强化视觉证据，从而纠正模型输出。整个pipeline由三个顺序衔接的阶段构成，如Figure 2所示。

### 输入输出流

框架接收两个输入：原始图像 $\pmb{v}$ 和文本查询 $\mathbf{x}$。在**Envision**阶段，原始图像经扩散模型处理，输出一个先验一致的视觉印象 $\hat{\pmb{V}}$ 和逐像素不确定性图 $U$。在**Attend**阶段，原始图像与视觉印象分别送入LVLM的视觉编码器，通过对比注意力差异 $\Delta \pmb{A}$ 与不确定性图联合定位反事实令牌，输出一个经过令牌填充的掩蔽输入 $\pmb{v}'$。在**Respond**阶段，对原始输入和填充输入进行对比解码，输出最终回应 $y$。

### 三阶段模块关系

1. **Envision（视觉印象生成）**：该阶段是框架的感知基础。它利用扩散模型（Stable Diffusion v1.5）的潜在扰动机制，从原始图像生成一个符合统计先验的“预期版本”——即如果图像中的反事实元素被替换为其常规对应物时，图像应有的样子。同时，通过多次采样的方差估计，生成一个逐像素的不确定性图，标识模型对哪些区域的先验预测高度不确定。这一阶段的输出直接决定了后续反事实定位的质量：若视觉印象无法准确反映“应有”的视觉内容，Attend阶段的注意力对比将失去参照基准。

2. **Attend（反事实定位）**：该阶段是框架的核心瓶颈突破点。它利用LVLM视觉编码器对原始图像和视觉印象的注意力差异 $\Delta \pmb{A}$（Eq.5），结合Envision阶段输出的不确定性图 $U$，通过并集操作 $\mathcal{H} = \mathcal{H}_{attn} \cup \mathcal{H}_{unc}$（Eq.6）确定反事实令牌的索引集。这些令牌随后被填充（padding），形成掩蔽输入 $\pmb{v}'$。该阶段的关键因果机制在于：注意力差异捕捉了“模型实际关注什么”与“模型应关注什么”之间的偏离，而不确定性图则补充了扩散先验自身的不确定性区域，二者互补地定位矛盾。

3. **Respond（对比解码）**：该阶段是框架的输出控制环节。通过对原始输入和填充输入进行加权对比解码 $p(y|\mathbf{x},\pmb{v},\pmb{v}') = (1+\alpha)p(y|\mathbf{x},\pmb{v}) - \alpha p(y|\mathbf{x},\pmb{v}')$（Eq.7），抑制反事实令牌对生成过程的贡献，同时放大视觉证据的权重。超参数 $\alpha$ 控制抑制强度，与基线方法VCD（Leng et al., CVPR 2024）保持一致以消除超参数偏差。

### 关键设计选择

- **视觉编码器层选择**：框架统一使用视觉编码器的第6层进行注意力提取。消融实验（Figure 4左）表明该层在VLMBias、POPE和HallusionBench上取得最佳平均性能，且浅层注意力图与显著物体区域的IoU更高（Figure 5），说明浅层特征更利于定位反事实元素。
- **填充令牌比例**：固定为10%（Figure 4右），在定位精度与信息保留之间取得平衡。
- **视觉印象选择**：从多次扩散采样中选取与原始图像L2偏差最大的版本作为最终视觉印象，以最大化先验对比度。

### 框架的模型无关性

EnAR的三个阶段均不涉及对LVLM参数的修改，仅通过外部扩散模型和推理时的注意力操作实现干预。实验覆盖InternVL3.5-8B、Qwen2.5VL-7B和LLaVA-v1.5-7B三种异构架构，验证了方法的模型无关健壮性。

### 补充图表

![[assets/figures/papers/paper_list_l747_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_Envision_Attend/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the EnAR framework. EnAR first generates a visual impression with a corresponding pixel-wise uncertainty map. Next, EnAR feeds both the original and impression images into the LVLM’s vision encoder to obtain contrastive attention, pads counterfactual tokens by combining attention differences with the uncertainty map. Finally, EnAR performs contrastive decoding over the original and padded inputs to suppress counterfactual hallucinations and produce the final response*

![[assets/figures/papers/paper_list_l747_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_Envision_Attend/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the Envision-Attend-Respond framework. By comparing the visual impression with the original image to locate counterfactual elements, the model is guided toward producing the correct response*



EnAR 由三个顺序执行的模块构成：**Envision**（视觉印象生成）、**Attend**（反事实定位）与 **Respond**（对比解码）。三个模块协同完成“生成先验一致参考 → 定位矛盾区域 → 抑制语言先验”的因果干预链条，全程无需对 LVLM 进行任何训练或微调。

### 3.1 Envision：视觉印象生成

该模块的目标是为输入图像构造一个**先验一致的视觉印象** $\hat{\mathbf{V}}$，同时产出一张**逐像素不确定性图** $\mathbf{U}$，作为后续 Attend 阶段定位反事实元素的参考基准。

**核心思路**：利用预训练扩散模型（Stable Diffusion v1.5）的生成先验，对输入图像的 VAE 潜表示 $\mathbf{z}_0$ 执行扩散反转与潜在扰动，迫使模型在“保持整体结构”与“修正反事实细节”之间产生偏差，从而暴露违反先验的图像区域。

**关键公式与变量含义**：

1. **扩散前向过程**（逐步加噪）：

   $$z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \varepsilon, \quad \varepsilon \sim \mathcal{N}(\mathbf{0}, I) \tag{1}$$

   其中 $z_0$ 为输入图像的 VAE 潜表示，$\bar{\alpha}_t$ 为噪声调度系数，$z_t$ 为第 $t$ 步的带噪潜变量。

2. **Tweedie 估计量梯度场**（用于潜在扰动）：
   
   $$G = \frac{\alpha_T \mathbb{E}[z_0 | z_T] - z_T}{1 - \bar{\alpha}_T} \approx - \frac{\varepsilon_\theta(z_T, T)}{\sqrt{1 - \bar{\alpha}_T}} \tag{3}$$

   该梯度场指向更高似然区域，即扩散模型认为“更符合先验”的潜空间方向。通过在 $z_T$ 上沿 $G$ 方向施加多步扰动，生成一系列候选潜变量，再经 DDPM 反向采样解码为候选视觉印象 $\hat{\mathbf{V}}^{(k)}$。

3. **视觉印象选择**：从 $K$ 个候选印象中选取与原始输入 L2 距离最大的一个作为最终视觉印象：

   $$\hat{V} = \hat{V}^{(k^\star)} \quad \text{where} \quad k^\star = \arg\max \| \hat{\boldsymbol{V}} - \hat{\boldsymbol{V}}^{(k)} \|_2^2$$

   直觉上，偏离最大的印象最可能“修正”了反事实元素，因而在后续对比中最能暴露矛盾。

4. **不确定性图** $\mathbf{U}$ 由候选印象之间的像素级方差估计得到，反映扩散模型对该区域重建的不确定程度。反事实区域往往对应高不确定性。

### 3.2 Attend：反事实定位与令牌填充

Attend 模块利用 Envision 产出的视觉印象 $\hat{\mathbf{V}}$ 和不确定性图 $\mathbf{U}$，在 LVLM 视觉编码器的令牌空间中**精确定位反事实元素**，并构造一个“反事实信号被削弱”的填充输入 $\mathbf{v}'$，为 Respond 阶段的对比解码提供对照。

**核心机制**：原始图像与视觉印象应仅在反事实区域产生显著差异。将二者分别送入 LVLM 视觉编码器，提取第 $L$ 层（默认第 6 层）的注意力图，计算逐元素绝对差：

$$\Delta \mathbf{A} = \big| \mathrm{Attn}^{(L)}(\mathbf{V}) - \mathrm{Attn}^{(L)}(\hat{\mathbf{V}}) \big| \tag{5}$$

$\Delta \mathbf{A}$ 中值越大的令牌位置，越可能对应反事实元素——因为视觉印象在该区域呈现了先验一致的内容，导致注意力分布发生偏移。

**联合定位**：将注意力差异选出的前 $K\%$ 令牌索引集 $\mathcal{H}_{attn}$ 与不确定性图选出的前 5% 令牌索引集 $\mathcal{H}_{unc}$ 取并集，得到最终反事实令牌索引集：

$$\mathcal{H} = \mathcal{H}_{attn} \cup \mathcal{H}_{unc} \tag{6}$$

基于 $\mathcal{H}$，将原始视觉令牌 $\mathbf{v}$ 中对应位置的令牌替换为可学习的填充令牌，形成 $\mathbf{v}'$。该填充输入在反事实区域的视觉信号被人为削弱，后续对比解码将据此抑制语言先验。

### 3.3 Respond：对比解码

Respond 模块对原始输入 $(\mathbf{x}, \mathbf{v})$ 和填充输入 $(\mathbf{x}, \mathbf{v}')$ 进行**对比解码**，通过 logits 层面的加权相减，放大反事实内容的惩罚信号：

$$p(y|\mathbf{x},\mathbf{v},\mathbf{v}') = (1+\alpha)p(y|\mathbf{x},\mathbf{v}) - \alpha p(y|\mathbf{x},\mathbf{v}') \tag{7}$$

其中 $\alpha$ 为抑制强度超参数（与基线 VCD 设置一致以消除超参偏差）。直觉上：若某个 token 在原始输入下概率高、在填充输入（反事实信号被削弱）下概率低，则相减后其概率被进一步压低——这正是语言先验驱动的幻觉 token 的典型特征；反之，真正由视觉证据支撑的 token 在两种输入下概率相近，受对比解码影响较小。

**因果机制总结**：Envision 提供先验一致的视觉参考与不确定性估计 → Attend 利用注意力差异与不确定性联合定位反事实令牌 → Respond 通过对比解码在 logits 空间抑制被定位的反事实内容，最终使模型输出回归视觉证据。三个模块形成闭环，且全程无需训练。

### 补充图表

![[assets/figures/papers/paper_list_l747_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_Envision_Attend/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the Envision stage in EnAR*



## 实验与关键发现

### 核心瓶颈与实验动机

LVLM在生成文本时，其内部的语言先验（世界知识）会压倒反事实视觉证据，使模型过度依赖统计频率而非当前图像内容，从而产生幻觉。EnAR的实验设计围绕这一瓶颈展开：通过反事实基准（VLMBias, WHOOPS）验证方法对语言先验的抑制能力，通过通用幻觉基准（POPE）检验方法是否损害常规视觉理解，并通过消融实验量化各组件对因果机制的贡献。

### 主实验结果

#### 反事实基准：VLMBias

EnAR在VLMBias上取得整体最高准确率，且提升幅度显著（Table 1）。以InternVL3.5-8B为例，Regular解码仅19.83%，EnAR提升至31.36%，绝对增益+11.53个百分点；LLaVA-v1.5-7B从16.92%提升至22.20%，增益+5.28个百分点。在三个LVLM骨干（InternVL3.5-8B、Qwen2.5VL-7B、LLaVA-v1.5-7B）上，EnAR均优于所有对比方法，包括基于高斯噪声的**VCD**（Leng et al., CVPR 2024）、基于视觉定位的**M3ID**（Favero et al., CVPR 2024）、基于生成反馈的**DeGF**（Zhang et al., ICLR 2025）以及RITUAL、AGLA等。值得注意的是，在“Chess Pieces”类别上所有方法准确率均为0%，表明当基础模型的推理能力完全失效时，EnAR的对比解码机制也无法补救——这是该方法的一个明确失败模式。

![[assets/figures/papers/paper_list_l747_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_Envision_Attend/figures/004_Table_1.jpg]]
*Table 1: Performance comparison on VLMBias across different categories. We report accuracy (%) for seven hallucination categories and overall performance across three baseline models. Values in parentheses indicate performance changes relative to Regular. Blue denotes improvement, gray denotes degradation, and the best-performing results are highlighted in bold*

#### 反事实基准：WHOOPS与PhD

在WHOOPS基准上（Table 2），EnAR将InternVL3.5-8B的平均准确率从62.45%提升至74.15%（+11.70），并在Social、Natural、Symbolic三个子类上均取得最佳或次佳结果。在PhD的Counting子集上，InternVL3.5-8B的准确率从73.10%提升至73.45%（+0.35），增益较小，说明EnAR对计数类反事实的改善有限，可能因为扩散模型生成的视觉印象在精确计数场景下不够可靠。

![[assets/figures/papers/paper_list_l747_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_Envision_Attend/figures/005_Table_2.jpg]]
*Table 2: Performance comparison on PhD, WHOOPS, and HallusionBench benchmarks. We selected the Counting subset of PhD, which best fits counterfactual scenarios, and further grouped the 26 categories in WHOOPS into three broader types: Social, Natural, and Symbolic. We report accuracy (%) for PhD and WHOOPS. We report Accuracy per Question (aAcc), Accuracy per Figure (fAcc), and Accuracy per Question Pair (qAcc) for three LVLM backbones*

#### 通用幻觉基准：POPE

在POPE基准上（Table 3），EnAR同样表现出稳定的提升。以LLaVA-v1.5-7B的Random子集为例，F1分数从80.9%提升至88.9%（+8.0）。在三个难度等级（Random, Popular, Adversarial）和三个LVLM骨干上，EnAR在多数指标上优于或持平于对比方法，表明该方法在抑制反事实幻觉的同时未损害通用视觉问答能力。

![[assets/figures/papers/paper_list_l747_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_Envision_Attend/figures/006_Table_3.jpg]]
*Table 3: Performance comparison on POPE benchmark across different methods. We report Accuracy (Acc.), Precision (Prec.), Recall, and F1 scores for three LVLM backbones*

### 消融实验

消融实验（Table 4）直接验证了EnAR两个核心组件的因果贡献：

![[assets/figures/papers/paper_list_l747_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_Envision_Attend/figures/007_Table_4.jpg]]
*Table 4: Ablation study on key components of our method across three LVLM backbones. We report overall accuracy on VLMBias and average performance metrics on POPE benchmark*

- **移除不确定性图（w/o uncertainty map）**：InternVL3.5-8B在VLMBias上从31.36%降至29.03%（-2.33），证明像素级不确定性估计为反事实定位提供了互补于注意力差异的信息。
- **移除视觉印象（w/o visual impression）**：性能骤降至25.80%（-5.56），表明仅依赖原始图像的不确定性图选择令牌远不足以定位反事实元素。视觉印象作为先验一致的参照物，是注意力对比机制成立的前提。
- **完全移除EnAR（w/o ours）**：退化为Regular解码的19.83%，进一步确认三阶段pipeline的整体必要性。

### 超参数分析

Figure 4展示了两个关键超参数的影响：

- **视觉编码器层选择**（Figure 4 left）：选择第6层进行注意力定位可获得VLMBias、POPE和HallusionBench上的最佳平均性能。浅层特征与显著物体区域的IoU更高（Figure 5），说明浅层注意力图更利于定位反事实元素，因为深层特征已被语义化，对局部异常的敏感性下降。
- **填充令牌比例**（Figure 4 right）：10%的填充比例在三个基准上取得最优权衡。比例过低则反事实抑制不足，过高则可能误掩正常视觉信息，导致常规能力下降。

![[assets/figures/papers/paper_list_l747_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_Envision_Attend/figures/010_Figure_4.jpg]]
*Figure 4: Average performance variation across VLMBias, POPE, and HallusionBench under different settings: (left) selection of vision encoder layer, (right) padding token ratio*

![[assets/figures/papers/paper_list_l747_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_Envision_Attend/figures/011_Figure_5.jpg]]
*Figure 5: IoU between top-K% tokens from attention maps at different encoder layers and salient object regions: (a) LLaVA-1.5- 7B, (b) InternVL3.5-8B*

### 方法公平性说明

所有对比方法均采用其论文中的最佳配置并在相同环境下复现。EnAR的对比解码超参数α与VCD保持一致，消除了超参数偏差。实验覆盖三种异构LVLM架构（InternVL3.5-8B、Qwen2.5VL-7B、LLaVA-v1.5-7B），验证了方法的模型无关健壮性。

### 失败模式与局限

1. **极端反事实失效**：当基础模型对图像内容完全无法推理时（如VLMBias的Chess Pieces类别所有方法0%准确率），EnAR的对比解码无法产生有效纠正。这揭示了该方法的上限受制于LVLM自身的视觉理解能力。
2. **扩散模型依赖**：视觉印象生成依赖Stable Diffusion 1.5，带来额外计算开销。当反事实内容高度抽象时，扩散模型生成的先验一致对应物可能不够精确，导致定位精度下降。
3. **超参数敏感性**：需要为每个LVLM调整视觉编码器层和填充令牌比例，缺乏完全自适应的机制。

### 补充图表

![[assets/figures/papers/paper_list_l747_https_openaccess_thecvf_com_content_CVPR2026_html_Liang_Envision_Attend/figures/009_Figure_6.jpg]]
*Figure 6: Case study visualization. We illustrate how EnAR constructs visual impressions, localizes counterfactual elements, and produces corrected responses*



## 定位与知识库关联

### 核心机制与因果路径

EnAR 解决的核心瓶颈是：大型视觉语言模型（LVLM）在生成文本时，语言先验（世界知识）压倒反事实视觉证据，导致模型过度依赖统计频率而非当前图像内容，从而产生幻觉。其因果调控路径由三个串行模块构成：

1. **Envision（视觉印象生成）**：利用扩散模型（Stable Diffusion 1.5）的视觉先验，通过潜在扰动生成与输入图像“先验一致”的视觉印象 $\hat{V}$ 和逐像素不确定性图 $U$。这一步骤的关键在于 Tweedie 估计量梯度场 $G \approx -\frac{\varepsilon_\theta(z_T, T)}{\sqrt{1 - \bar{\alpha}_T}}$，它引导潜表示向更高似然区域移动，从而生成“世界知识期望看到的”版本。
2. **Attend（反事实定位）**：将原始图像和视觉印象分别送入 LVLM 视觉编码器，计算第 $L$ 层注意力图的逐元素绝对差 $\Delta \pmb{A} = \big| \mathrm{Attn}^{(L)}(\pmb{V}) - \mathrm{Attn}^{(L)}(\hat{\pmb{V}}) \big|$，并与不确定性图 $U$ 联合，通过 $\mathcal{H} = \mathcal{H}_{attn} \cup \mathcal{H}_{unc}$ 定位反事实令牌索引集。
3. **Respond（对比解码）**：对原始输入和经掩蔽填充后的输入 $\pmb{v}'$ 进行对比解码，最终 logits 为 $p(y|\mathbf{x},\pmb{v},\pmb{v}') = (1+\alpha)p(y|\pmb{x},\pmb{v}) - \alpha p(y|\pmb{x},\pmb{v}')$，通过超参数 $\alpha$ 抑制反事实令牌的语言先验，强化视觉证据。

### 与现有方法的关系与差异

EnAR 属于**训练无关的对比解码**范式，与以下基线方法形成清晰对比：

- **VCD**（Leng et al., CVPR 2024）：同样采用对比解码，但通过向图像添加高斯噪声构造“失真”输入，而非利用扩散先验生成语义一致的视觉印象。VCD 的扰动缺乏对反事实元素的针对性，EnAR 则通过注意力差异和不确定性图实现了精确的反事实定位。
- **M3ID**（Favero et al., CVPR 2024）：通过视觉定位控制幻觉，但与 EnAR 的核心差异在于：M3ID 依赖训练阶段的对齐，而 EnAR 完全无需训练，且定位信号来自扩散先验与注意力对比的联合。
- **RITUAL**：采用随机图像变换的对比解码基线，变换方式（如旋转、裁剪）与语义无关，无法区分反事实元素与常规元素。
- **DeGF**（Zhang et al., ICLR 2025）：基于生成反馈的自校正解码，依赖额外的生成模型提供反馈信号，而 EnAR 的视觉印象直接来自扩散模型的前向-反向过程，无需外部反馈循环。
- **AGLA**：基于注意力的无关区域掩蔽，但仅使用单张图像的注意力图，缺乏视觉印象作为参照，无法区分“语言先验驱动的关注”与“视觉证据驱动的关注”。

**关键差异总结**：EnAR 的独特之处在于将**扩散模型的视觉先验**引入 LVLM 的注意力引导，通过“原始-印象”对比实现反事实元素的**无监督定位**，这是上述基线均未涉及的机制。

### 适用边界与局限

基于论文提供的证据，EnAR 的适用边界和局限如下：

1. **极端反事实场景失效**：在极其异常的图像上（如国际象棋规则错误），基础 LVLM 的推理能力完全失效，所有方法在该类别准确率均为 0%，EnAR 无法纠正。这表明当反事实超出模型的基本认知能力时，对比解码的干预无效。
2. **依赖外部扩散模型**：视觉印象生成依赖 Stable Diffusion 1.5，带来额外计算开销和推理时间，可能限制实时应用。论文未提供推理延迟数据，该点需手动验证。
3. **抽象反事实的定位精度**：当反事实内容高度抽象时，扩散模型生成的视觉印象可能无法精确反映先验一致的对应物，导致定位精度下降。论文未量化不同抽象程度下的性能差异，该局限为定性推断。
4. **超参数需人工调整**：需要为每个 LVLM 调整视觉编码器层（默认第 6 层）和填充令牌比例（默认 10%），缺乏完全自适应的机制。消融实验（Figure 4）显示不同层和比例对性能有显著影响。

### 开放问题与未来方向

1. **时序扩展**：对于动态视频或交互式场景，如何扩展视觉印象生成和对比解码以保持时序一致性？当前 EnAR 仅处理静态图像。
2. **扩散模型升级**：能否使用更先进的扩散模型（如 Stable Diffusion XL）或定制化先验来进一步提升反事实定位精度？论文未对此进行实验。
3. **能力平衡**：EnAR 的对比解码机制是否可能削弱模型在非反事实场景下的常规能力？论文仅在反事实和幻觉基准上评估，未测试通用 VQA 性能，该风险需手动验证。
4. **训练结合**：将 EnAR 与训练阶段的微调方法相结合，能否实现进一步的泛化能力和鲁棒性？当前 EnAR 是纯推理时干预。
5. **跨模态泛化**：该框架能否推广到其他模态（如音频-文本）的反事实幻觉问题？核心的“先验印象生成-对比注意力定位-对比解码”范式理论上模态无关，但需实证验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Envision_Attend_Then_Respond_Counterfactual_Hallucination_Mitigation_in_Large_Vision_Language_Models.pdf]]
