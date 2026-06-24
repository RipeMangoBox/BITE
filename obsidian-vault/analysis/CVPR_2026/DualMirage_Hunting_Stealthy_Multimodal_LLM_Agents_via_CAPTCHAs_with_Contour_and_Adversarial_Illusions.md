---
title: "DualMirage: Hunting Stealthy Multimodal LLM Agents via CAPTCHAs with Contour and Adversarial Illusions"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DualMirage_Hunting_Stealthy_Multimodal_LLM_Agents_via_CAPTCHAs_with_Contour_and_Adversarial_Illusions.pdf
project_link: null
code_link: null
aliases:
- DualMirage
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 利用人类视觉系统与MLLM之间的根本感知分歧：人类能够基于自上而下的认知过程感知主观轮廓（轮廓错觉），而MLLM缺乏此能力；同时，在视觉编码器层面注入人类不可察觉的对抗扰动（对抗错觉），使MLLM产生可预期的、暴露身份的输出。
primary_logic: 提出“双重错觉”协同机制：将心理学的轮廓错觉（对人类可见、对机器不可见）与机器学习的对抗错觉（对机器可见、对人类不可见）融合，构建一种既可阻止代理破解挑战、又能主动诱导代理泄露自身模型名称等身份信息的智能陷阱，将CAPTCHA从被动门卫转变为主动猎捕工具。
claims:
- DualMirage 在五款主流 MLLM 上平均人类成功率达 95.8%，并实现高达 100% 的代理阻止率。
- 白盒攻击下平均诱导身份泄露成功率为 58.8%，黑盒攻击下为 21.9%，证明了主动猎捕模式的有效性。
- 消融实验表明，单靠轮廓错觉在 GPT-4o 上代理阻止率仅 78%，而 DualMirage 组合达到 96%；对抗错觉单独使用在 GPT-4o 上阻止率仅 36%，攻击成功率仅 36%，组合后显著提升。
- Illusion-Selfie2Anime 挑战对白盒模型 LLaVA 和 Qwen 的 ASR 达到 100%，有效实现了身份狩猎。
---

# DualMirage: Hunting Stealthy Multimodal LLM Agents via CAPTCHAs with Contour and Adversarial Illusions

> [!tip] 核心洞察
> 提出“双重错觉”协同机制：将心理学的轮廓错觉（对人类可见、对机器不可见）与机器学习的对抗错觉（对机器可见、对人类不可见）融合，构建一种既可阻止代理破解挑战、又能主动诱导代理泄露自身模型名称等身份信息的智能陷阱，将CAPTCHA从被动门卫转变为主动猎捕工具。

| 字段 | 内容 |
|------|------|
| 中文题名 | DualMirage：基于轮廓与对抗错觉的CAPTCHA猎捕隐蔽多模态LLM代理 |
| 英文题名 | DualMirage: Hunting Stealthy Multimodal LLM Agents via CAPTCHAs with Contour and Adversarial Illusions |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_DualMirage_Hunting_Stealthy_Multimodal_LLM_Agents_via_CAPTCHAs_with_Contour_CVPR_2026_paper.html) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | DualMirage |
| Dataset | Illusion-Selfie2Anime, All configurations, All challenge configurations |

> [!tip] 效果简介
> - Illusion-Selfie2Anime 上，Human Success Rate (HSR) 99.1% (首次尝试)。
> - All configurations (Illusion-Selfie2Anime + Illusion-MNIST) 上，Average HSR (首次尝试 → 第四次尝试) 95.78% → 97.48%。
> - All challenge configurations (white-box models) 上，Agent Blocking Rate (ABR) 100% (against LLaVA-v1.5-7b and Qwen2.5-vl-7b)。

## 概述

当前多模态大模型（MLLM）驱动的自主代理在视觉理解和决策能力上快速演进，使得传统依赖扭曲文本或图像分割的CAPTCHA机制日趋脆弱。现有防御范式本质上是被动门禁——仅测试用户是否具备人类水平的视觉能力，却无法识别和追溯机器代理的身份。**DualMirage** 将这一困境转化为主动猎捕机会，其核心思想是：**同时利用人类视觉系统与MLLM之间两种方向相反的感知分歧，构建“双重错觉”协同陷阱**。

具体而言，DualMirage 融合了两种互补的错觉机制：
- **轮廓错觉（Contour Illusion）**：基于人类自上而下的认知闭合能力，生成彩色邻接光栅图像，使人类能清晰感知主观轮廓，而MLLM因缺乏此类先验难以解析——形成“对人可见、对机器不可见”的认知屏障。
- **对抗错觉（Adversarial Illusion）**：在轮廓错觉图像上叠加人眼不可察觉的对抗扰动，强制MLLM的视觉编码器产生误导，使代理在尝试破解挑战时主动输出自身模型名称等身份标识——实现“对机器可见、对人不可见”的身份诱导。

两种错觉的协同作用使CAPTCHA从被动门卫转变为**主动猎捕工具**：轮廓错觉阻止代理通过挑战，对抗错觉则诱导已暴露的代理泄露身份，从而完成“阻止—诱导—追溯”的完整防御闭环。

在五款主流MLLM上的实验表明，DualMirage 平均人类成功率达 **95.8%**，白盒场景下代理阻止率最高达 **100%**，身份诱导攻击成功率平均为 **58.8%**（白盒）和 **21.9%**（黑盒），在人类可用性与机器防御能力之间取得了现有方案中最佳的平衡。

## 背景与动机

随着多模态大模型（MLLM）在视觉理解、自主决策和工具调用能力上的飞速发展，基于此类模型的自主代理（agent）已能够模拟人类行为完成网页浏览、信息检索乃至社交互动等复杂任务。这一能力跃迁在提升自动化效率的同时，也对互联网安全基础设施构成了根本性威胁——传统验证码（CAPTCHA）机制正面临前所未有的失效危机。

### 传统CAPTCHA的防御困境

现有CAPTCHA方案的核心设计哲学是“被动门禁”：通过向用户施加人类易解、机器难辨的视觉挑战，将自动化代理阻挡在系统之外。典型技术路线包括扭曲文本识别、图像分割选择、滑块拼图等，其底层假设是机器视觉能力在特定高熵刺激下远逊于人类。然而，这一假设已被多模态大模型彻底动摇。具备强大视觉编码器和语言推理能力的MLLM代理，能够以远超传统OCR或图像分类器的精度解析扭曲文本、识别语义对象，甚至通过链式推理（CoT）绕过逻辑陷阱。

更深层的问题在于，即使某些挑战能够暂时阻止代理通过，传统CAPTCHA也无法提供任何关于攻击者身份的信息。系统仅能获知“验证失败”，却无从判断失败者是误触的人类用户、随机猜测的脚本，还是某个特定型号的MLLM代理。这种“只防不识”的被动姿态，使得防御方始终处于信息劣势，无法针对性地升级策略或追溯攻击源。

### 从被动防御到主动猎捕的范式转变

DualMirage的核心动机在于将CAPTCHA从“被动门卫”重新定义为“主动猎捕工具”。这一转变要求挑战机制同时具备两种能力：**阻止代理破解挑战**（代理阻止率，Agent Blocking Rate, ABR）和**诱导代理泄露身份**（攻击成功率，Attack Success Rate, ASR）。后者尤为关键——如果代理在尝试破解验证码的过程中被迫输出自身模型名称等身份标识，防御方即可实现精准的代理识别与溯源，从而将攻防博弈推向对防御方有利的方向。

### 双重错觉：利用人机感知分歧

实现上述目标的关键在于发掘并利用人类视觉系统与MLLM之间的根本性感知分歧。DualMirage识别出两类方向相反的错觉现象，并将其协同组合（如图1所示）：

- **轮廓错觉（Contour Illusion）**：源于人类视觉系统的自上而下认知加工过程。当彩色光栅条纹在特定边界处发生相位偏移时，人类大脑会自动“填补”出实际上并不存在的主观轮廓，从而感知到完整的形状或物体。而MLLM的视觉编码器缺乏这种认知补全机制，仅能解析到局部条纹的纹理信息，难以形成全局轮廓感知。这一特性可概括为“对人可见，对机器不可见”。

- **对抗错觉（Adversarial Illusion）**：利用机器学习模型的对抗脆弱性，在图像上叠加人眼不可察觉的微小扰动，使MLLM的视觉编码器产生系统性误判，进而强制语言模型输出预设的身份标识字符串（如“GPT-4o”）。这一特性与轮廓错觉形成镜像互补——“对机器可见，对人不可见”。

两种错觉的协同并非简单叠加，而是构成一个完整的感知陷阱：轮廓错觉构建认知屏障，大幅提高代理的破解难度；对抗错觉则在代理试图突破屏障的过程中，主动劫持其输出行为，使其暴露身份。这一“一阻一诱”的双重机制，使DualMirage在保持高人类可用性的同时，实现了对MLLM代理的主动猎捕。

### 与现有工作的定位

与DualMirage最接近的前置工作是**IllusionCAPTCHA**（Ding et al., WWW 2025），该方法首次将轮廓错觉引入CAPTCHA设计，利用人类与机器对主观轮廓的感知差异构建认知障碍。然而，IllusionCAPTCHA仍停留在被动防御范式：其唯一目标是阻止代理通过验证，缺乏身份诱导机制，无法区分不同类型的攻击代理或追溯其来源。DualMirage在此基础上引入对抗错觉组件，将CAPTCHA的功能边界从“测试人类能力”拓展至“猎捕机器身份”，实现了从被动防御到主动猎捕的范式升级。

## 核心创新

DualMirage 的核心创新在于将 CAPTCHA 从“被动门禁”范式彻底重构为“主动猎捕”范式。现有方法（如 **IllusionCAPTCHA**，Ding et al., WWW 2025）仅依赖轮廓错觉等单一认知障碍来测试人类能力，在具备强大视觉理解能力的多模态大模型（MLLM）代理面前日益脆弱。DualMirage 通过以下两个关键维度的范式跃迁解决了这一瓶颈。

### 视觉挑战设计范式：从单一认知屏障到双重感知分歧的协同利用

传统 CAPTCHA 依赖扭曲文本、图像分割或简单视觉错觉等高熵刺激，仅测试代理的识图能力。DualMirage 则首次将两类本质对立的“错觉”融合为协同攻击向量：

- **轮廓错觉（Contour Illusion）**：利用人类视觉系统自上而下的认知完形能力，通过**彩色邻接光栅错觉生成**（Colored Abutting Grating Illusion Generation）在图像中构造人类可清晰感知、但 MLLM 难以解析的主观轮廓。该组件实现了“对人可见、对机器不可见”的认知屏障。
- **对抗错觉（Adversarial Illusion）**：在轮廓错觉图像上叠加人眼不可察觉的对抗扰动（L∞ 范数约束），通过**隐私诱导的对抗错觉注入**（Privacy-induced Adversarial Illusion Injection）劫持 MLLM 的视觉编码器，强制模型输出预设的身份标识字符串。该组件实现了“对机器可见、对人不可见”的行为操控。

两种错觉的协同放大了单一组件的不足：消融实验（Table 4）表明，单独使用轮廓错觉在 GPT-4o 上的代理阻止率（ABR）仅 78%，攻击成功率（ASR）为 0%；单独使用对抗错觉在 GPT-4o 上的 ABR 仅 36%，ASR 仅 36%。而 DualMirage 组合将 GPT-4o 的 ABR 提升至 96%，ASR 提升至 44%，证明了两种错觉之间的协同放大效应。

### 验证与响应机制：从被动答案匹配到主动身份诱导与猎捕

传统 CAPTCHA 仅验证用户输入的文本与预设答案是否匹配，本质上是一个被动的门禁系统。DualMirage 将验证机制升维为主动的身份猎捕：

- **双重验证逻辑**：系统不仅验证挑战答案的正确性，更主动检测 MLLM 代理的响应中是否包含被诱导输出的模型名称等身份信息。
- **身份追溯能力**：在白盒场景下，DualMirage 对 LLaVA-v1.5-7b 和 Qwen2.5-vl-7b 的平均 ASR 分别达到 62.25% 和 55.25%，其中 Illusion-Selfie2Anime 挑战对这两个模型的 ASR 达到 100%（Table 2），有效实现了对代理身份的主动狩猎。在黑盒场景下，平均 ASR 为 21.92%，虽然迁移性有限，但仍验证了主动猎捕范式的可行性。

这一范式跃迁使 CAPTCHA 从单纯的“人类能力测试工具”转变为能够主动识别、追溯和暴露 MLLM 代理身份的智能陷阱系统。

## 整体框架

DualMirage 的生成管线由两个序贯模块构成，其核心设计理念是**将人类视觉系统与多模态大模型（MLLM）之间的感知分歧转化为可操作的防御与猎捕机制**。具体而言，该框架利用“轮廓错觉”对人类可见而对机器不可见，以及“对抗错觉”对机器可见而对人类不可见的双重特性，构建从被动阻止到主动身份诱导的完整攻击链。

### Pipeline 总览

如图 Figure 2 所示，整个管线接收一张原始图像和预设的目标身份字符串作为输入，经过两个阶段生成最终的 DualMirage 挑战图像：

![[assets/figures/papers/paper_list_l745_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_DualMirage_Huntin/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed DualMirage. The image generation pipeline consists of: (1) Colored Abutting Grating Illusion Generation, which distorts the original image into contour-illusory images; (2) Privacy-induced Adversarial Illusions Injection, which optimizes adversarial perturbation injected into the contour-illusory image and generates the final DualMirage images*

1. **彩色邻接光栅错觉生成（Colored Abutting Grating Illusion Generation）**：将原始图像转化为人类可感知主观轮廓、但 MLLM 难以解析的认知挑战图像。
2. **隐私诱导的对抗错觉注入（Privacy-induced Adversarial Illusion Injection）**：在轮廓错觉图像上叠加人眼不可见的对抗扰动，强制 MLLM 输出预设的身份标识字符串。

两阶段之间存在严格的**因果依赖关系**：第一阶段的轮廓错觉提供了对抗 MLLM 的基础认知屏障（提高代理阻止率），第二阶段在此基础上注入对抗扰动，利用 MLLM 视觉编码器的脆弱性实现主动身份暴露。消融实验证实，单独使用轮廓错觉虽能有效阻止代理（LLaVA 上 ABR 达 92.0%），但 ASR 为 0%；单独使用对抗错觉在 GPT-4o 上 ABR 仅 36.0%，而 DualMirage 组合将 ABR 提升至 96.0%、ASR 提升至 44.0%，验证了两种错觉的**协同放大效应**（Table 4）。

### 模块一：彩色邻接光栅错觉生成

该模块将经典的黑白邻接光栅错觉（abutting grating illusion）推广至全彩色域。其数学基础是方波强度函数：

$$G^{c}(x, y)=\begin{cases} A^{c} & \text{if } \lfloor\frac{x\cos\theta + y\sin\theta}{T}\rfloor \text{ is even,} \\ B^{c} & \text{otherwise,} \end{cases}$$

其中 $c$ 为颜色通道，$T$ 为光栅周期，$\theta$ 为方向角，$A^{c}$ 与 $B^{c}$ 分别为高低强度值。通过为前景和背景区域生成**相位差为 $\pi$ 的两组光栅** $G_{1}$ 与 $G_{2}$，并利用前景掩膜 $\pmb{M}_{f}$ 和背景掩膜 $\pmb{M}_{b}$ 进行元素乘加合成：

$$\pmb{x}_{cag} = (G_{1} \odot \pmb{M}_{f}) + (G_{2} \odot \pmb{M}_{b})$$

在掩膜边界处，两组光栅的相位跳变被人类视觉系统自上而下的认知过程整合为**主观轮廓（illusory contour）**，而 MLLM 的视觉编码器缺乏这一感知能力，仅能解析出离散的光栅条纹，从而形成认知屏障。

该模块的**关键瓶颈**在于前景/背景分割掩膜的质量：对于语义复杂的图像，若掩膜边界模糊，人类也可能难以辨识生成的错觉轮廓，影响可用性。

### 模块二：隐私诱导的对抗错觉注入

在获得轮廓错觉图像 $\pmb{x}_{cag}$ 后，该模块在其上叠加人眼不可察觉的对抗扰动 $\pmb{\delta}$（约束 $\|\pmb{\delta}\|_{\infty} \leq \epsilon$），使 MLLM 的视觉编码器产生误导，强制模型输出预设的身份标识字符串 $\pmb{y}_{t}$（如模型名称）。

根据攻击者对目标模型的访问权限，优化目标分为两种形式：

- **白盒攻击**：直接最大化目标 token 序列在给定扰动图像下的对数似然，使用 PGD 优化：

$$\max_{\delta} \sum_{i=1}^{L} \log p_{g}(y_{i} \mid \pmb{x}_{cag} + \delta, p, y_{<i}), \quad \text{s.t. } \|\delta\|_{\infty} \leq \epsilon$$

- **黑盒攻击**：利用 $N$ 个代理 CLIP 模型，最大化扰动后图像的嵌入与目标文本嵌入之间的平均余弦相似度，以提升对抗样本的迁移性：

$$\max_{\pmb{\delta}} \sum_{i=1}^{N} \frac{1}{N} \cos\left(E_{img}^{(i)}(\pmb{x}_{cag} + \pmb{\delta}), E_{text}^{(i)}(\pmb{y}_{t})\right)$$

该模块的**核心局限**在于：黑盒场景下对抗扰动的跨模型迁移性有限（平均 ASR 仅 21.92%），且在常见图像变换（JPEG 压缩、高斯模糊、随机裁剪）下 ASR 大幅下降，表明扰动本身的脆弱性（Table 3a）。

### 输入输出规范与部署流程

- **输入**：原始图像 $I$、目标身份字符串 $\pmb{y}_{t}$、前景/背景掩膜对。
- **输出**：DualMirage 挑战图像 $\pmb{x}_{dual} = \pmb{x}_{cag} + \pmb{\delta}$。
- **验证逻辑**：系统不仅检查用户输入的文本是否与预设答案匹配，还主动检测响应中是否包含被诱导出的身份信息字符串，从而实现从“被动门禁”到“主动猎捕”的范式转换。

完整的生成流程由 Algorithm 1 统一描述，将两阶段操作封装为端到端的挑战生成过程。

## 核心模块与公式推导

DualMirage 的生成管线由两个关键模块串联构成，分别对应两种性质截然不同的“错觉”的注入，其整体流程如 Figure 2 所示。

### 模块一：彩色邻接光栅错觉生成

该模块将原始图像转化为人类可感知主观轮廓、而 MLLM 难以解析的认知挑战图像。其核心是将经典的黑白邻接光栅错觉（abutting grating illusion）推广至全彩色域。

**光栅强度函数**：对于单颜色通道 $c$，在像素位置 $(x, y)$ 处的方波强度定义为：

$$
G^{c}(x, y) = \begin{cases}
A^{c}, & \text{if } \lfloor \frac{x \cos \theta + y \sin \theta}{T} \rfloor \text{ is even}, \\
B^{c}, & \text{otherwise}.
\end{cases}
$$

其中 $A^{c}$ 与 $B^{c}$ 分别为通道 $c$ 的高低强度值，$T$ 为光栅周期，$\theta$ 为光栅方向角。该函数在空间上产生交替的条纹图案。

**轮廓错觉图像合成**：给定前景掩膜 $\mathbf{M}_f$ 与背景掩膜 $\mathbf{M}_b$，生成两组相位差为 $\pi$ 的光栅 $G_1$ 与 $G_2$，通过元素乘加合成最终图像：

$$
\mathbf{x}_{cag} = (G_1 \odot \mathbf{M}_f) + (G_2 \odot \mathbf{M}_b)
$$

在掩膜边界处，两组光栅的相位跳变使人类视觉系统基于自上而下的认知过程感知到不存在的连续轮廓（主观轮廓），而 MLLM 的视觉编码器缺乏这一认知机制，难以正确解析图像内容。

### 模块二：隐私诱导的对抗错觉注入

该模块在轮廓错觉图像 $\mathbf{x}_{cag}$ 上叠加人眼不可察觉的对抗扰动 $\delta$，强制 MLLM 输出预设的身份标识字符串（如模型名称），实现主动身份暴露。根据攻击者对目标模型的访问权限，分别采用白盒与黑盒优化目标。

**白盒攻击目标**：当可完整访问目标 MLLM 的梯度时，最大化目标 token 序列 $y_{1..L}$ 在扰动图像下的对数似然：

$$
\max_{\delta} \sum_{i=1}^{L} \log p_{g}(y_i \mid \mathbf{x}_{cag} + \delta, p, y_{<i}), \quad \text{s.t. } \|\delta\|_{\infty} \leq \epsilon
$$

其中 $p$ 为提示词（prompt），$y_{<i}$ 为已生成的前缀 token，$\epsilon$ 为扰动幅度的 $L_{\infty}$ 约束上界。优化采用 PGD（Projected Gradient Descent）算法。

**黑盒攻击目标**：当无法获取目标模型梯度时，利用 $N$ 个代理 CLIP 模型的图像与文本编码器，最大化扰动后图像嵌入与目标文本嵌入之间的平均余弦相似度，以提升对抗样本的跨模型迁移性：

$$
\max_{\delta} \sum_{i=1}^{N} \frac{1}{N} \cos\left(E_{img}^{(i)}(\mathbf{x}_{cag} + \delta), E_{text}^{(i)}(\mathbf{y}_t)\right)
$$

其中 $E_{img}^{(i)}$ 与 $E_{text}^{(i)}$ 分别为第 $i$ 个代理 CLIP 模型的图像编码器和文本编码器，$\mathbf{y}_t$ 为目标身份文本（如 “LLaVA”）。

两个模块的协同机制在于：轮廓错觉提供对人类友好、对机器不友好的认知屏障（阻止代理正确破解挑战），而对抗错觉在此基础上叠加主动诱导能力（迫使代理泄露身份），使 CAPTCHA 从被动门禁转变为主动猎捕工具。

### 补充图表

![[assets/figures/papers/paper_list_l745_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_DualMirage_Huntin/figures/001_Figure_1.jpg]]
*Figure 1: Motivation of our proposed DualMirage. The first mirage (i.e., contour illusion) creates a perception of non-existent contours (such as the Mona Lisa) for the human visual system through colorful stripes, while the second mirage (i.e., adversarial illusion) hijacks the action of the multimodal agent, forcing it to reveal identity information (such as its model name)*

## 实验与分析

### 人类可用性评估

DualMirage 的首要设计约束是保持对人类用户的友好性。如表 1 所示，在 Illusion-Selfie2Anime 挑战中，人类首次尝试成功率（HSR）高达 99.1%；在所有挑战配置（包含 Illusion-MNIST）上，平均首次尝试 HSR 为 95.78%，且随着尝试次数增加提升至第四次尝试的 97.48%。这一结果表明，轮廓错觉图像中嵌入的主观轮廓对人类视觉系统具有高度可辨识性，彩色光栅变换并未显著增加认知负荷。Illusion-MNIST 挑战中，数字序列长度 l 设为 3、6、10 三种难度，人类仍能保持高成功率，验证了挑战设计的可用性边界。

### 代理阻止与身份猎捕性能

表 2 展示了 DualMirage 与现有 CAPTCHA 方法在代理阻止率（ABR）和攻击成功率（ASR）两个维度上的对比。在白盒场景下，DualMirage 对 LLaVA-v1.5-7b 和 Qwen2.5-vl-7b 实现了 100% 的代理阻止率，意味着没有任何代理能够正确解析轮廓错觉并给出正确答案。在黑盒场景下，对 GPT-4o、Gemini-1.5-pro 和 Claude-3-Sonnet 的平均 ABR 分别达到 97.5%、97.25% 和 98.25%，阻止效果极为显著。

在主动身份猎捕方面，Illusion-Selfie2Anime 挑战对白盒模型 LLaVA 和 Qwen 的 ASR 达到 100%，即所有被测试的代理均被诱导输出自身模型名称等身份信息。综合所有挑战配置，白盒平均 ASR 为 LLaVA 62.25%、Qwen 55.25%；黑盒平均 ASR 为 21.92%。白盒与黑盒之间的 ASR 差距揭示了对抗扰动迁移性的核心瓶颈：闭源商用模型的视觉编码器结构和参数不可见，限制了基于代理 CLIP 模型集成优化的扰动跨模型迁移效果。

### 消融实验：双重错觉的协同效应

表 4 的消融实验揭示了轮廓错觉与对抗错觉各自的贡献及协同放大机制：

- **单独轮廓错觉（Con. only）**：在 LLaVA 上 ABR 为 92.0%，ASR 为 0%；在 GPT-4o 上 ABR 为 78.0%，ASR 为 0%。轮廓错觉能有效阻止代理破解挑战，但由于不含对抗扰动，完全无法诱导身份泄露。
- **单独对抗错觉（Adv. only）**：在 LLaVA 上 ABR 为 100.0%，ASR 为 91.0%，表现强劲；但在 GPT-4o 上 ABR 骤降至 36.0%，ASR 仅 36.0%。这说明对抗扰动在白盒可控场景下效果显著，但对黑盒模型的鲁棒性严重不足。
- **DualMirage 组合**：在 LLaVA 上达到 ABR 100.0% 和 ASR 100.0%；在 GPT-4o 上 ABR 提升至 96.0%，ASR 提升至 44.0%。两种错觉产生了显著的协同放大效应：轮廓错觉提供了对黑盒模型的强阻止基线，对抗错觉则在此基础上注入身份诱导能力，弥补了单一组件的短板。

### 鲁棒性分析

表 3(a) 评估了 DualMirage 在图像变换和增强 MLLM 技术下的鲁棒性。常见图像变换（JPEG 压缩、高斯模糊、随机裁剪）导致 ASR 从 45.6% 大幅下降至 10.1% 甚至更低，表明对抗扰动对像素级操作高度敏感，这是当前基于 $L_\infty$ 约束优化扰动的固有脆弱性。在 Few-shot 微调和对抗训练（AT）增强的 MLLM 上，ABR 和 ASR 均出现不同程度下降，说明攻击者若针对 DualMirage 机制进行专门适配，防御效果会受到挑战。

表 3(b) 展示了针对专用 OCR 模型的防御效果。在 Illusion-MNIST 挑战上，传统 OCR 模型同样难以解析光栅错觉中的数字序列，表明轮廓错觉的防御能力不限于 MLLM 代理，对专用视觉模型也具有普适的阻挡效果。

### 多维对比总览

图 3 以雷达图形式将 DualMirage 与现有 CAPTCHA 方案在人类可用性、代理阻止能力和对抗攻击能力三个维度上进行对比。DualMirage 在三个维度上实现了最优均衡：既保持了高达 95% 以上的人类可用性，又达到了接近 100% 的代理阻止率，同时具备现有被动 CAPTCHA 所不具备的主动身份猎捕能力。这一均衡优势源于双重错觉机制的根本设计——轮廓错觉保障人类可解性与代理阻止基线，对抗错觉赋予主动追溯能力，两者在感知层面的正交性使其互不干扰、协同增效。

### 失败模式与局限性

尽管 DualMirage 在白盒场景下表现优异，黑盒攻击成功率（平均 21.92%）仍是主要瓶颈。对抗扰动对常见图像变换的脆弱性（ASR 从 45.6% 降至 10.1% 以下）限制了其在真实部署中面对图像预处理管线的可靠性。此外，轮廓错觉的生成质量依赖于前景/背景分割掩膜的精度，对于语义高度复杂的图像，光栅变换可能产生人类也难以辨识的模糊刺激，影响可用性。当前评估未充分考虑攻击者采用针对性防御（如对抗训练、去噪模块）后的框架抗扰性能，这需要进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l745_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_DualMirage_Huntin/figures/004_Table_2.jpg]]
*Table 2: Performance Comparison of our DualMirage with existing CAPTCHA Methods. Values are percentages (%)*

![[assets/figures/papers/paper_list_l745_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_DualMirage_Huntin/figures/007_Table_4.jpg]]
*Table 4: Ablation of DualMirage components. “Con.” : Contour illusion; “Adv.”: Adversarial illusion. Values are percentages (%)*

![[assets/figures/papers/paper_list_l745_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_DualMirage_Huntin/figures/003_Table_1.jpg]]
*Table 1: Evaluation of human usability for DualMirage. We reports the percentage of correctly solved challenges across varying numbers of attempts for two challenge types*

![[assets/figures/papers/paper_list_l745_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_DualMirage_Huntin/figures/005_Table_3.jpg]]
*Table 3: Robustness Evaluation. (a) Robustness under image transformations and enhanced MLLM techniques (Few-shot FL and Adversarial Training AT). (b) Evaluation against dedicated OCR models on Illusion-MNIST challenge. Values are percentages (%)*

![[assets/figures/papers/paper_list_l745_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_DualMirage_Huntin/figures/006_Figure_3.jpg]]
*Figure 3: Multi-dimensional comparison of CAPTCHA schemes across key performance metrics. Pur DualMirage demonstrates a superior balance of high human usability, robust agent blocking, and adversarial attack capability*

## 方法谱系与知识库定位

### 1. 与现有 CAPTCHA 范式的关系

DualMirage 的定位是对“被动防御”CAPTCHA 范式的根本性升级。传统 CAPTCHA 机制的核心逻辑是通过制造对人类易解、对机器困难的感知任务（如扭曲文本、图像分类、物体识别）来构建访问屏障。然而，在多模态大模型（MLLM）时代，这一逻辑的脆弱性日益暴露：模型视觉理解能力的跃升使得单纯增加任务难度（高熵刺激）的策略趋于失效。

DualMirage 的关键突破在于将 CAPTCHA 从“能力测试”转变为“感知陷阱”。其直接对比的基线工作 **IllusionCAPTCHA**（Ding et al., WWW 2025）已尝试利用视觉错觉构建认知障碍，但本质上仍停留在被动防御层面——仅依赖轮廓错觉来区分人类与机器的感知能力，缺乏对代理身份的主动追溯机制。DualMirage 在此基础上实现了两个关键范式跃迁：

- **从单错觉到双错觉协同**：IllusionCAPTCHA 仅利用“对人类可见、对机器不可见”的轮廓错觉作为单向屏障。DualMirage 引入对抗错觉，形成“轮廓错觉（人类可感知，MLLM 难解析）+ 对抗错觉（人类不可见，MLLM 被诱导输出身份）”的双向感知分歧利用机制。消融实验（Table 4）清晰揭示了这种协同的必要性：单独轮廓错觉在 GPT-4o 上的代理阻止率（ABR）仅 78%，单独对抗错觉仅 36%，而 DualMirage 组合达到 96%。

- **从被动门禁到主动猎捕**：传统 CAPTCHA 仅验证用户输入与预设答案是否匹配，属于二元门禁逻辑。DualMirage 的验证机制不仅检查挑战答案的正确性，更主动检测 MLLM 代理的响应中是否包含被诱导泄露的模型名称等身份信息，从而实现对隐蔽代理的身份追溯和猎捕。

### 2. 方法适用边界

DualMirage 的有效性高度依赖于两个前提条件，这界定了其适用边界：

**（1）视觉编码器的感知分歧必须存在。** 轮廓错觉的有效性建立在人类视觉系统自上而下的主观轮廓感知能力与 MLLM 视觉编码器缺乏此类认知机制的根本差异之上。若未来 MLLM 的视觉编码器通过架构改进或专门训练获得了类似人类的错觉感知能力，轮廓错觉的防御效果将显著削弱。同样，对抗错觉依赖视觉编码器对特定扰动模式的敏感性——若目标模型的编码器经过对抗训练或采用了去噪预处理模块，攻击成功率（ASR）将大幅下降。Table 3(a) 的数据已证实这一脆弱性：在对抗训练（AT）后，ASR 从 45.6 降至 10.1 甚至更低。

**（2）对抗扰动的迁移性受限于模型架构相似性。** 白盒场景下（可访问模型梯度），DualMirage 在 LLaVA 和 Qwen 上实现了高达 100% 的 ASR。但在黑盒场景下（针对闭源商用模型如 GPT-4o、Gemini、Claude），平均 ASR 仅为 21.92%。这一显著的性能落差表明，当前基于 CLIP 代理模型集成的黑盒攻击策略（Eq. (4)）在跨架构迁移性上存在根本性局限。

**（3）图像变换的鲁棒性不足。** Table 3(a) 显示，常见图像变换（JPEG 压缩、高斯模糊、随机裁剪）会导致 ASR 大幅下降（从 45.6 降至 10.1 或更低）。这意味着 DualMirage 在需要图像压缩或格式转换的真实部署场景（如社交媒体平台、移动端应用）中，对抗错觉的猎捕功能可能严重退化。

**（4）轮廓错觉的生成质量受限于掩膜精度。** 彩色邻接光栅错觉生成（Algorithm 1）依赖前景/背景分割掩膜的质量。对于语义复杂、边缘模糊的图像，生成的错觉刺激可能对人类同样难以辨识，从而损害人类可用性（HSR）。

### 3. 局限性与开放问题

**已确认的局限性：**

- **黑盒迁移性瓶颈**：平均 21.92% 的黑盒 ASR 表明，对抗错觉在闭源商用模型上的身份诱导能力有限。这是当前方法最显著的性能短板。
- **扰动脆弱性**：对抗扰动对 JPEG 压缩、模糊、裁剪等常见图像变换极为敏感，ASR 降幅可达 35 个百分点以上。
- **自适应攻击防御未充分评估**：论文未系统考察攻击者知晓 DualMirage 机制后采用针对性防御（如专门针对光栅模式的微调、去噪模块）时的框架抗扰性能。
- **计算开销与实时性未量化**：论文未报告 DualMirage 图像生成的计算延迟和资源消耗，这对于实际 CAPTCHA 部署场景的用户体验至关重要。

**值得追踪的开放问题：**

1. **跨模型迁移性增强**：能否通过更丰富的代理模型集成策略（如引入扩散模型作为代理或利用多模态对比学习的更广泛模型族）显著提升黑盒 ASR？这是决定 DualMirage 能否对闭源商用代理构成实质性威胁的关键。

2. **鲁棒扰动设计**：在保持高人类可用性（HSR > 95%）的前提下，如何设计对不可预知图像变换具有内在鲁棒性的对抗扰动？可能的路径包括利用 JPEG 压缩可微近似进行对抗训练，或探索频域扰动注入策略。

3. **抗自适应攻击能力**：当攻击者采用对抗训练或专门针对光栅错觉模式的微调策略时，DualMirage 的 ABR 和 ASR 将如何变化？这需要构建一个动态攻防评估框架来系统考察。

4. **实时部署可行性**：DualMirage 的两阶段生成管线（轮廓错觉生成 + 对抗优化）的计算开销是否可满足实时 CAPTCHA 服务的延迟要求？需要在典型硬件配置下进行端到端延迟基准测试。

### 4. 知识库定位

DualMirage 处于 **CAPTCHA 安全 × 多模态对抗攻击 × 视觉认知科学** 的交叉地带。其核心贡献在于首次将心理物理学的轮廓错觉与机器学习的对抗攻击融合为统一的“感知陷阱”框架，实现了从被动防御到主动猎捕的范式跃迁。在 CAPTCHA 研究谱系中，它代表了对“基于认知差异的验证机制”这一路线的深化和武器化——不再满足于区分人类与机器，而是主动利用感知分歧来追溯机器代理的身份。

该方法对后续研究的启示在于：在 MLLM 代理日益普及的时代，安全机制的设计不应停留在“提高任务难度”的线性思维，而应主动寻找并利用人类与机器感知系统中的根本性非对称性，并将其转化为可操作的攻防杠杆。DualMirage 所揭示的“双重错觉协同放大”效应（轮廓错觉提升阻止率，对抗错觉赋予身份诱导能力，组合后两者相互增强）为这一方向提供了有力的概念验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/DualMirage_Hunting_Stealthy_Multimodal_LLM_Agents_via_CAPTCHAs_with_Contour_and_Adversarial_Illusions.pdf]]
