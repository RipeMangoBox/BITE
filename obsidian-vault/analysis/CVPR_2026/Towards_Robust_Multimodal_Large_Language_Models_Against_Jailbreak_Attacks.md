---
title: Towards Robust Multimodal Large Language Models Against Jailbreak Attacks
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Robust_Multimodal_Large_Language_Models_Against_Jailbreak_Attacks.pdf
project_link: null
code_link: null
aliases:
- TRMLLMAJA
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过交替进行对比嵌入攻击（CoE-Attack）生成token级别的跨模态对抗噪声，以及基于防御损失与效用损失的模型参数更新，直接训练模型在嵌入空间识别并拒绝有害请求。
primary_logic: 首次将对抗训练框架引入MLLM的安全防御，利用嵌入级对抗噪声生成与对比学习，同时增强模型对多模态越狱攻击的抵抗力和保持良性任务的通用能力。
claims:
- 在LLaVA-7B上，VLGuard对ImgJP和GCG白盒攻击的ASR高达88%和79%，而SAFEMLLM分别降至6%和0%，证明安全微调无法抵御白盒多模态攻击。
- SAFEMLLM在全部六种攻击方法和六个MLLM上的平均ASR均显著低于原始模型及基线，其中对GCG攻击所有模型的ASR为0.00%，对AutoDAN攻击的平均ASR仅为0.17%。
- 消融实验显示，移除对比损失后平均ASR增加13.67%，证实对比损失是提升模型鲁棒性的关键组件。
- ImgJP (Advbench) on LLaVA-7B 上 ASR (%) = 6.00
---

# Towards Robust Multimodal Large Language Models Against Jailbreak Attacks

> [!tip] 核心洞察
> 首次将对抗训练框架引入MLLM的安全防御，利用嵌入级对抗噪声生成与对比学习，同时增强模型对多模态越狱攻击的抵抗力和保持良性任务的通用能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向鲁棒多模态大语言模型的越狱攻击防御 |
| 英文题名 | Towards Robust Multimodal Large Language Models Against Jailbreak Attacks |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2502.00653) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | SAFEMLLM |
| Dataset | ImgJP (Advbench) on LLaVA-7B, GCG (Advbench) on LLaVA-7B, AutoDAN (Advbench) on LLaVA-7B, MM-SafetyBench |

> [!tip] 效果简介
> - ImgJP (Advbench) on LLaVA-7B 上，ASR (%) 6.00 vs 75.00 (Original) (-69.00)。
> - GCG (Advbench) on LLaVA-7B 上，ASR (%) 0.00 vs 62.00 (Original) (-62.00)。
> - AutoDAN (Advbench) on LLaVA-7B 上，ASR (%) 1.00 vs 89.00 (Original) (-88.00)。

## 概要

多模态大语言模型（MLLM）在安全对齐后仍面临严峻的越狱攻击威胁。如图 1 所示，现有安全微调方法（如 **VLGuard**，Zong et al., 2024）虽能抵御黑盒攻击（Fig-Step），却在白盒攻击下暴露出严重脆弱性：攻击者可通过同时注入图像对抗扰动（ImgJP）与文本对抗后缀（GCG），轻易绕过安全防线。这一瓶颈的根源在于，现有防御仅在像素或离散 token 层面做一次性微调，缺乏对跨模态联合对抗扰动的结构化抵抗能力。

SAFEMLLM 的核心洞察是**首次将对抗训练范式引入 MLLM 的安全防御**。该方法交替执行两个步骤——CoE-Attack 在 token 嵌入层级生成跨模态对抗噪声，模型更新步则通过防御损失与效用损失的联合优化来学习识别并拒绝有害请求——从而在嵌入空间直接塑造模型的鲁棒性。与 **R2D2**（Mazeika et al., 2024）和 **CAT**（Xhonneux et al., 2024）等仅针对纯文本 LLM 的对抗训练方法不同，SAFEMLLM 同时覆盖图像与文本两种模态的扰动注入。

实验证据充分支撑了方法的有效性。在 LLaVA-7B 上，VLGuard 对 ImgJP 和 GCG 白盒攻击的攻击成功率（ASR）分别高达 88% 和 79%，而 SAFEMLLM 将二者分别压降至 6% 和 0%（Table 1）。综合六种攻击方法与六个 MLLM 的结果，SAFEMLLM 对 GCG 攻击的平均 ASR 为 0.00%，对 AutoDAN 攻击的平均 ASR 仅为 0.17%，在所有设定下均显著优于原始模型及现有基线。消融实验进一步揭示，对比损失是鲁棒性提升的关键组件——移除后平均 ASR 上升 13.67%——而效用损失则有效防止了模型在良性任务上的过拒答。



### 多模态大语言模型的安全挑战

多模态大语言模型（MLLM）在视觉问答、图像描述等任务上展现出强大能力，但其安全性问题日益凸显。越狱攻击（Jailbreak Attack）通过精心设计的输入，诱导模型生成有害内容，对 MLLM 的实际部署构成严重威胁。攻击者可在图像和文本两个模态同时注入对抗扰动，形成跨模态攻击，使得防御难度远超纯文本场景。

### 现有防御方法的脆弱性

当前针对 MLLM 的安全防御主要依赖两类策略：一是基于安全数据集的指令微调，如 **VLGuard**（Zong et al., 2024）；二是外挂推理阶段的内容过滤器。然而，这些方法在面对白盒攻击时暴露出严重不足。

Figure 1 直观展示了这一脆弱性：**VLGuard** 经过安全微调后，在黑盒攻击 **Fig-Step** 下表现尚可，但面对白盒攻击 **ImgJP** 和 **GCG** 时几乎形同虚设。具体而言，在 LLaVA-7B 上，VLGuard 对 ImgJP 的攻击成功率（ASR）高达 88%，对 GCG 的 ASR 达 79%，与未防御的原始模型（75% 和 62%）相比不降反升。这揭示了一个关键瓶颈：**一次性安全微调无法使模型获得对白盒多模态对抗扰动的内在鲁棒性**。

### 对抗训练范式的引入

在纯文本大语言模型领域，**R2D2**（Mazeika et al., 2024）和 **CAT**（Xhonneux et al., 2024）等对抗训练方法已展现出提升模型鲁棒性的潜力。然而，这些方法仅针对文本模态设计，无法直接处理图像与文本联合注入的对抗噪声。

本文的核心动机在于：**首次将对抗训练框架引入 MLLM 的安全防御**，通过交替进行攻击生成与模型更新，使模型在训练过程中持续接触并学习抵抗最强的跨模态攻击，从根本上提升其对越狱攻击的免疫力。同时，防御过程必须兼顾良性任务的通用能力，避免模型因过度防御而出现“过拒答”问题。



## 核心方法与创新机理

SAFEMLLM 的核心创新在于首次将**对抗训练框架**系统性地引入多模态大语言模型的安全防御，并在**扰动层级**、**训练范式**和**攻击/防御目标函数**三个关键维度上实现了对现有方案的突破。

### 1. 扰动层级：从像素/离散文本到 Token 嵌入

现有白盒攻击方法通常直接优化图像像素（如 **ImgJP**）或离散文本后缀（如 **GCG**），而 SAFEMLLM 将对抗扰动的注入点提升至 **token 嵌入层级**。具体而言，在攻击步（CoE-Attack）中，方法同时优化图像位置嵌入 $P_0^h$ 和文本后缀嵌入 $P_0^t$，使对抗噪声以跨模态、连续嵌入的形式存在。这种设计使得扰动能够直接影响模型的内部表示，而非停留在输入表层，从而生成更强、更难以被简单过滤的对抗样本，为后续的对抗训练提供高质量的“对手”。

### 2. 训练范式：从一次性微调到交替对抗训练

现有安全防御方案（如 **VLGuard**，Zong et al., 2024）通常采用一次性安全微调或外挂推理过滤器的方式，面对白盒攻击时极易被绕过（例如 VLGuard 在 LLaVA-7B 上对 ImgJP 和 GCG 的 ASR 分别高达 88% 和 79%）。SAFEMLLM 采用**交替对抗训练**范式，包含两个迭代步骤：
- **Step I（CoE-Attack）**：固定模型参数，通过多步优化生成嵌入层级的强对抗扰动。
- **Step II（Model Updating）**：固定对抗噪声，利用防御损失与效用损失联合更新模型参数（通过 LoRA 微调）。

这种“攻击-防御”交替的机制迫使模型持续暴露于当前最强的对抗样本中，从而逐步学习在嵌入空间识别并拒绝有害请求，显著提升了对白盒攻击的鲁棒性。

### 3. 攻击/防御目标函数：引入对比损失与效用约束

传统攻击目标函数仅最大化有害确认响应 $c_n$ 的似然，而 SAFEMLLM 在攻击步中额外引入了**对比对抗损失** $L_{\mathrm{adv}}^{\mathrm{contra}}$：

$$L_{\mathrm{adv}}^{\mathrm{contra}} = - \sum_{n=1}^{N} \log \sigma \bigg[ \log \big( p( \mathbf{c}_n | \mathbf{P}_0^h, \mathbf{x}_n, \mathbf{P}_0^t ) \big) - \log \big( p( \mathbf{r}_n | \mathbf{P}_0^h, \mathbf{x}_n, \mathbf{P}_0^t ) \big) \bigg]$$

该损失通过相对抑制安全拒绝响应 $r_n$ 的生成概率，使对抗攻击不仅追求“生成有害内容”，更追求“避免生成安全拒绝”，从而产生更具欺骗性的扰动。相应地，防御步也采用对称的**对比防御损失** $L_{\mathrm{def}}^{\mathrm{contra}}$，鼓励模型在对抗噪声下选择安全响应而非有害响应。

此外，为防止对抗训练导致模型过度拒答并损害正常对话能力，SAFEMLLM 在防御步中加入了**效用损失** $L_{\mathrm{utility}}$，在良性图文对（来自 LLaVA-Instruct-80K）上最大化标准答案的似然。这一设计是 SAFEMLLM 区别于纯安全微调方案的关键——它在不牺牲通用能力的前提下实现了安全对齐。

### 4. 关键消融证据

消融实验直接验证了上述创新的有效性：
- **移除对比损失**后，平均 ASR 上升 13.67%，证实对比机制是提升鲁棒性的核心组件。
- **移除效用损失**后，良性问答的 GPT 评分显著下降（最大降幅 5.37 分），表明效用约束有效防止了模型的过拒答行为。
- **仅使用对比损失而缺少目标损失**时，模型在训练过程中会生成乱码，无法产生连贯的安全回复，说明目标损失与对比损失的协同是必要的。



SAFEMLLM 的整体设计遵循**交替对抗训练**范式，在每一个训练迭代中依次执行两个核心步骤：**CoE-Attack（Step I）** 与 **Model Updating（Step II）**。如 Figure 2 所示，这一双步循环构成了模型安全防御能力持续增强的内在驱动力。

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed SAFEMLLM, which contains two iterative steps. In Step I, we fix the parameters of the MLLM. SAFEMLLM optimizes two noise matrices initialized by*

### 输入与数据流

框架的输入包含两类数据源：
- **有害安全数据**：由有毒请求 $x_n$、有害确认响应 $c_n$ 和安全拒绝响应 $r_n$ 组成的三元组，用于攻击步与防御步的对抗训练。
- **良性效用数据**：从 LLaVA-Instruct-80K 数据集中采样的图文对 $(I_j, q_j)$ 及其标准答案 $y_j$，用于计算效用损失以维持模型的通用指令跟随能力。

数据流在两步之间形成闭环：Step I 以当前模型参数为条件生成对抗噪声，Step II 则利用固定后的噪声信号驱动模型参数更新，使模型学会在嵌入空间识别并拒绝有害请求。

### Step I：CoE-Attack（对比嵌入攻击）

在攻击步中，模型参数被冻结。SAFEMLLM 在 **token 嵌入层级** 注入两组可优化的对抗噪声矩阵 $P_0^h$ 和 $P_0^t$，分别作用于有害请求的视觉位置嵌入和文本后缀嵌入。与传统的像素级扰动（如 ImgJP）或离散文本后缀优化（如 GCG）不同，CoE-Attack 直接在连续嵌入空间中搜索最具破坏力的跨模态扰动。

攻击目标由两项损失加权组合驱动：
- **目标对抗损失** $L_{\mathrm{adv}}^{\mathrm{target}}$（Eq. 1）：最大化模型生成有害确认响应 $c_n$ 的似然。
- **对比对抗损失** $L_{\mathrm{adv}}^{\mathrm{contra}}$（Eq. 2）：通过 sigmoid 对比形式，相对抑制安全拒绝响应 $r_n$ 的生成概率，迫使模型在“有害确认”与“安全拒绝”之间更倾向于前者。

总攻击损失为 $L_{\mathrm{adv}} = L_{\mathrm{adv}}^{\mathrm{target}} + \lambda \cdot L_{\mathrm{adv}}^{\mathrm{contra}}$（Eq. 3），其中 $\lambda$ 为平衡超参数。$P_0^h$ 和 $P_0^t$ 通过多步梯度优化最小化 $L_{\mathrm{adv}}$，最终得到固定对抗噪声 $P_M^h$ 和 $P_M^t$，作为 Step II 的输入。

### Step II：Model Updating（模型参数更新）

在防御步中，Step I 产出的对抗噪声 $P_M^h$、$P_M^t$ 被固定，模型转而更新自身的可训练参数。防御损失同样采用“目标 + 对比”的双重结构：
- **目标防御损失** $L_{\mathrm{def}}^{\mathrm{target}}$（Eq. 4）：最大化在对抗噪声下生成安全拒绝响应 $r_n$ 的似然。
- **对比防御损失** $L_{\mathrm{def}}^{\mathrm{contra}}$（Eq. 5）：鼓励模型在 $r_n$ 与 $c_n$ 之间选择安全响应。

总防御损失为 $L_{\mathrm{def}} = L_{\mathrm{def}}^{\mathrm{target}} + \lambda \cdot L_{\mathrm{def}}^{\mathrm{contra}}$（Eq. 6）。此外，为防止模型因过度防御而丧失通用能力，框架引入**效用损失** $L_{\mathrm{utility}}$（Eq. 7），在良性图文对上最大化标准答案的似然。最终，模型通过最小化 $L_{\mathrm{def}} + L_{\mathrm{utility}}$ 更新 LoRA 适配器参数，视觉编码器保持冻结。

### 模块关系总结

| 模块 | 角色 | 输入 | 输出 |
|------|------|------|------|
| CoE-Attack | 生成嵌入级跨模态对抗噪声 | 有害三元组 $(x_n, c_n, r_n)$ | 固定对抗噪声 $P_M^h, P_M^t$ |
| Model Updating | 利用对抗噪声更新防御能力 | $P_M^h, P_M^t$ + 有害三元组 + 良性图文对 | 更新后的 LoRA 参数 |
| Utility Data Sampler | 提供良性数据以维持通用能力 | LLaVA-Instruct-80K | 图文对 $(I_j, q_j, y_j)$ |
| LoRA Adapter | 承载可训练参数 | 梯度信号 | 参数更新 $\theta_i$ |

这一交替训练框架的核心优势在于：攻击步持续“发现”模型嵌入空间的脆弱区域，防御步则针对性地“修补”这些区域，形成动态博弈，使模型在面对白盒多模态越狱攻击时具备显著增强的鲁棒性。消融实验（Table 2）证实，移除对比损失将导致平均 ASR 上升 13.67%，而移除效用损失则使良性问答的 GPT 评分下降高达 5.37 分，验证了各模块在框架中的不可替代性。



SAFEMLLM 的核心由两个交替迭代的步骤构成：**对比嵌入攻击（CoE-Attack，Step I）** 与 **模型参数更新（Step II）**。前者在固定模型参数的条件下，于 token 嵌入层级生成跨模态对抗噪声；后者固定该噪声，通过防御损失与效用损失的联合优化来更新模型的 LoRA 参数，从而在抵御越狱攻击的同时保持良性任务的通用能力（Figure 2）。

### CoE-Attack：对比嵌入攻击

CoE-Attack 不直接修改图像像素或离散文本后缀，而是在嵌入空间注入可微分的对抗扰动。具体而言，对于每张输入图像，SAFEMLLM 初始化一个可学习的图像位置嵌入矩阵 $\mathbf{P}_0^h$；对于有害文本后缀，初始化一个文本嵌入矩阵 $\mathbf{P}_0^t$。这两个矩阵作为跨模态的对抗噪声源，经过多步梯度优化，以最大化模型生成有害确认响应的概率。

攻击优化采用双目标损失函数。首先，**目标对抗损失**直接最大化有害响应 $\mathbf{c}_n$ 的生成似然：

$$L_{\mathrm{adv}}^{\mathrm{target}} = - \sum_{n=1}^{N} \log \left[ p( \mathbf{c}_n | \mathbf{P}_0^h, \mathbf{x}_n, \mathbf{P}_0^t ) \right] \tag{1}$$

其中 $N$ 为批次大小，$\mathbf{x}_n$ 为原始有害文本提示。仅使用该损失时，攻击可能陷入局部最优——模型虽然倾向于生成有害内容，但仍可能输出安全拒绝响应 $\mathbf{r}_n$。为此，SAFEMLLM 引入了 **对比对抗损失**，通过 sigmoid 函数 $\sigma$ 相对抑制安全响应的生成概率：

$$L_{\mathrm{adv}}^{\mathrm{contra}} = - \sum_{n=1}^{N} \log \sigma \bigg[ \log \big( p( \mathbf{c}_n | \mathbf{P}_0^h, \mathbf{x}_n, \mathbf{P}_0^t ) \big) - \log \big( p( \mathbf{r}_n | \mathbf{P}_0^h, \mathbf{x}_n, \mathbf{P}_0^t ) \big) \bigg] \tag{2}$$

最终的攻击总损失为两者的加权组合：

$$L_{\mathrm{adv}} = L_{\mathrm{adv}}^{\mathrm{target}} + \lambda \cdot L_{\mathrm{adv}}^{\mathrm{contra}} \tag{3}$$

其中 $\lambda$ 为控制对比项权重的超参数。通过 $M$ 步内层优化，CoE-Attack 将初始噪声 $\mathbf{P}_0^h, \mathbf{P}_0^t$ 迭代更新为强对抗扰动 $\mathbf{P}_M^h, \mathbf{P}_M^t$。

### 模型参数更新：防御损失与效用损失

在 Step II 中，固定已优化的对抗噪声 $\mathbf{P}_M^h, \mathbf{P}_M^t$，模型参数通过防御损失和效用损失进行更新。防御损失同样采用目标-对比双分支结构，但优化方向相反——鼓励模型在对抗噪声存在时生成安全响应。

**目标防御损失**最大化安全响应 $\mathbf{r}_n$ 的似然：

$$L_{\mathrm{def}}^{\mathrm{target}} = - \sum_{n=1}^{N} \log \left[ p( \mathbf{r}_n | \mathbf{P}_M^h, \mathbf{x}_n, \mathbf{P}_M^t ) \right] \tag{4}$$

**对比防御损失**则进一步要求模型在安全响应与有害响应之间做出正确选择：

$$L_{\mathrm{def}}^{\mathrm{contra}} = - \sum_{n=1}^{N} \log \sigma \bigg[ \log \big( p( \mathbf{r}_n | \mathbf{P}_M^h, \mathbf{x}_n, \mathbf{P}_M^t ) \big) - \log \big( p( \mathbf{c}_n | \mathbf{P}_M^h, \mathbf{x}_n, \mathbf{P}_M^t ) \big) \bigg] \tag{5}$$

防御总损失为：

$$L_{\mathrm{def}} = L_{\mathrm{def}}^{\mathrm{target}} + \lambda \cdot L_{\mathrm{def}}^{\mathrm{contra}} \tag{6}$$

若仅优化防御损失，模型可能出现过拒答（over-refusal）现象，损害正常对话能力。为此，SAFEMLLM 从 LLaVA-Instruct-80K 数据集中采样良性图文对 $(\mathbf{I}_j, \mathbf{q}_j)$，引入 **效用损失** 以维持通用指令跟随性能：

$$L_{\mathrm{utility}} = - \sum_{j=1}^{H} \log \left[ p( \mathbf{y}_j | \mathbf{I}_j, \mathbf{q}_j ) \right] \tag{7}$$

其中 $\mathbf{y}_j$ 为良性问题的标准答案，$H$ 为效用数据的批次大小。最终，模型的 LoRA 参数（作用于跨模态适配器和 LLM 解码器，视觉编码器保持冻结）通过最小化 $L_{\mathrm{def}} + L_{\mathrm{utility}}$ 进行更新。

### 关键设计要素总结

| 模块 | 核心机制 | 关键公式 |
|------|----------|----------|
| CoE-Attack | 嵌入级对抗噪声 + 对比目标抑制安全响应 | Eq. (1)–(3) |
| 防御更新 | 固定噪声下的安全响应最大化 + 对比选择 | Eq. (4)–(6) |
| 效用保持 | 良性数据上的标准答案似然最大化 | Eq. (7) |

消融实验证实了各组件的重要性：移除对比损失后平均 ASR 上升 13.67%（Table 2）；移除效用损失则导致良性问答的 GPT 评分显著下降，最大降幅达 5.37 分；仅使用对比损失而缺少目标损失时，模型会生成乱码，无法产出连贯的安全回复。

### 补充图表

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the vulnerability of existing safety-tuning methods compared with our model SAFEMLLM. The defender first fine-tunes the original MLLM in step 1. The attackers then attack the finetuned MLLMs in step 2 in different ways. In step 3, the fine-tuned MLLMs generate outputs. Details of the experiment settings can be found in Section 4*



## 实验与关键发现

### 白盒越狱攻击下的防御有效性

SAFEMLLM 在六种具有代表性的越狱攻击方法和六个主流 MLLM 上进行了全面评估，核心指标为攻击成功率（ASR）。表 1 汇总了主实验结果，揭示了几个关键发现。

**安全微调的脆弱性暴露。** 在 LLaVA-7B 上，经过安全微调的 VLGuard（Zong et al., 2024）在面对白盒攻击时几乎完全失效：ImgJP 攻击下 ASR 高达 88.00%，GCG 攻击下 ASR 为 79.00%。这与此前 VLGuard 能有效防御黑盒攻击 Fig-Step 的结论形成鲜明对比，说明仅依赖安全指令微调无法抵御攻击者同时操控图像和文本模态的白盒场景。

**SAFEMLLM 的压倒性防御优势。** 在相同的 LLaVA-7B 模型上，SAFEMLLM 将 ImgJP 的 ASR 从原始模型的 75.00% 降至 6.00%，将 GCG 的 ASR 从 62.00% 降至 0.00%，将 AutoDAN 的 ASR 从 89.00% 降至 1.00%。在全部六个模型的平均表现上，SAFEMLLM 对 GCG 攻击实现了 0.00% 的 ASR，对 AutoDAN 攻击的平均 ASR 仅为 0.17%。相比于原始模型和所有基线方法，SAFEMLLM 在 ImgJP、VAA、GCG 和 AutoDAN 上分别取得了 17.6%、4.2%、9.7% 和 25.8% 的平均 ASR 改善，证明交替对抗训练框架在多模态场景下具有显著且一致的鲁棒性提升。

**跨模型泛化能力。** 在 MM-SafetyBench 基准上，SAFEMLLM 将六个模型的平均 ASR 从原始模型的 16.46% 降至 0.10%，表明该方法对不同架构的 MLLM 均具备良好的迁移防御能力。

### 良性任务效用保持

防御方法的实用性取决于其是否损害模型的正常对话能力。图 3 展示了在 LLaVA-Instruct-80K 数据集的 100 个样本上，由 GPT-4-Turbo 评分的响应质量。SAFEMLLM 在六个 MLLM 上的效用评分与原始模型基本持平，未出现显著退化，这归功于训练过程中引入的效用损失 $L_{\mathrm{utility}}$ 对良性图文对的标准答案似然进行显式约束。

### 消融实验：各组件贡献

表 2 报告了在 13B 模型上使用 ImgJP 攻击的消融结果，量化了 SAFEMLLM 各损失组件的独立贡献。

**对比损失是关键鲁棒性组件。** 移除对比对抗损失 $L_{\mathrm{adv}}^{\mathrm{contra}}$ 和对比防御损失 $L_{\mathrm{def}}^{\mathrm{contra}}$ 后，平均 ASR 上升 13.67%。这表明单纯最大化/最小化目标响应似然不足以建立强鲁棒性，对比学习机制通过相对抑制有害响应、增强安全响应，在嵌入空间构建了更清晰的决策边界。

**效用损失防止过拒答。** 移除 $L_{\mathrm{utility}}$ 后，良性问答的 GPT 评分显著下降，最大降幅达 5.37 分。模型在缺乏效用约束时会倾向于对所有输入都生成安全拒绝，丧失了正常的指令跟随能力。效用损失作为正则化项，在防御与通用能力之间取得了关键平衡。

**目标损失保障生成质量。** 定性分析（附录 K）显示，仅使用对比损失而缺少目标损失 $L_{\mathrm{adv}}^{\mathrm{target}} / L_{\mathrm{def}}^{\mathrm{target}}$ 时，模型在训练过程中会生成无意义的乱码（如 "s' y iss ands and notfuledt..."），无法产生连贯的安全回复。目标损失为模型提供了明确的优化方向，是生成可读输出的必要条件。

### 计算效率分析

表 3 对比了 SAFEMLLM 与直接优化对抗图像（w/ Adv.Image）的计算开销。在 LLaVA-7B 和 LLaVA-13B 上，SAFEMLLM 的 token 嵌入级对抗噪声优化在保持更高防御效果的同时，计算效率优于像素级对抗图像优化。作者声称整个对抗训练过程可在单张 A100 GPU 上约四小时内完成，但这一开销对于资源受限环境仍构成一定门槛。

### 通用基准效用验证

表 4 报告了在 MM-Vet 基准上的效用评估结果。SAFEMLLM 在该通用多模态理解基准上的得分与原始模型相当，进一步证实对抗训练未损害模型的综合多模态能力，防御效果并非以牺牲通用智能为代价。

### 失败模式与局限性

尽管 SAFEMLLM 在白盒攻击下表现出色，仍需注意以下边界情况：

1. **模态覆盖范围有限。** 当前框架仅针对图像和文本两种模态的越狱攻击进行防御，未涉及音频、视频等更多模态的攻击场景。
2. **自适应攻击的泛化能力未充分验证。** 当攻击者也采用类似的对抗训练策略进行自适应攻击时，SAFEMLLM 的鲁棒性是否依然保持，目前缺乏实验证据。
3. **资源门槛。** 对抗训练虽可在单卡 A100 上完成，但对于边缘部署或实时场景，计算开销仍需进一步优化。

### 补充图表

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/003_Table_1.jpg]]
*Table 1: Experimental results of different jailbreak attack methods on six multimodal large language models. We report ASR (%) values and a lower ASR denotes better defense performance. We report two average ASR values since VLGuard (Zong et al., 2024) only releases the LLaVA models. One is the average ASRs calculated on two LLaVA models, and the other is based on all six models*

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/005_Table_2.jpg]]
*Table 2: Ablation study results of module removal in ASR (%). Attacks are conducted on 13B models using the ImgJP attack method on the AdvBench dataset*

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/010_Table_3.jpg]]
*Table 3: Comparison of computing efficiency on LLaVA-7B and LLaVA-13B. Here, “w/ Adv.Image” indicates that we directly optimize an adversarial image instead of the token embeddings*

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/012_Table_4.jpg]]
*Table 4: Utility performance on the MM-Vet benchmark*

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/013_Table_5.jpg]]
*Table 5: Generated texts during adversarial training with and without using the target loss in SAFEMLLM. Here we visualize the model outputs based on the training toxic queries and optimized perturbations*

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/009_Figure_7.jpg]]
*Figure 7: The average log probability of generating N positive and negative labels after each inner-attack step m, where N is the batch size. The results are illustrated at every 50 fine-tuning iterations. We use blue and red to distinguish between the positive label*

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/011_Figure_8.jpg]]
*Figure 8: We conduct hyperparameter analysis on (a) ASR values of using different λ in*

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/018_Figure_10.jpg]]
*Figure 10: Responses from LLaVA-13B after the VAA attack. The attack injects unconstrained adversarial perturbations in a white-box scenario. Although R2D2 also provided a benign response, it has a mistake by starting with “Timothy” rather than “Kyle”. In comparison, the response from SAFEMLLM is more concise and accurate*

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/019_Figure_11.jpg]]
*Figure 11: Responses from LLaVA-13B after the GCG attack. We skip the image input for a more efficient implementation. The attack injects adversarial text suffix into toxic requests. It is a white-box attack method*

![[assets/figures/papers/paper_list_l791_https_arxiv_org_abs_2502_00653/figures/020_Figure_12.jpg]]
*Figure 12: Responses from LLaVA-13B after the AutoDAN attack. We skip the image input for a more efficient implementation. The attack injects adversarial text strings into toxic requests. It is a white-box attack method*



## 定位与知识库关联

### 防御范式定位：从静态微调到动态对抗训练

SAFEMLLM 的防御范式与现有 MLLM 安全方案存在本质差异。现有防御主要沿两条路径展开：

**安全微调（Safety-Tuning）** 以 **VLGuard**（Zong et al., 2024）为代表，通过在安全对齐数据集上进行指令微调，使模型学会拒绝有害请求。然而，Figure 1 和 Table 1 的证据表明，该范式在面对白盒攻击时存在结构性脆弱：在 LLaVA-7B 上，VLGuard 对 ImgJP 和 GCG 攻击的 ASR 仍高达 88% 和 79%，几乎与未防御的原始模型（75% 和 62%）处于同一量级。其根本原因在于，安全微调仅优化了模型在干净输入下的行为分布，而未改变模型在对抗扰动下的嵌入空间决策边界。

**LLM 对抗训练** 如 **R2D2**（Mazeika et al., 2024）和 **CAT**（Xhonneux et al., 2024）将对抗训练引入纯文本大语言模型的安全防御，但其攻击扰动通常作用于离散文本后缀或连续前缀，未涉及跨模态嵌入层级的联合优化。SAFEMLLM 首次将这一范式迁移至多模态场景，并在两个关键维度上进行了适配性创新：

1. **扰动层级下沉至嵌入空间**：不同于 ImgJP 直接优化图像像素或 GCG 优化离散文本后缀，SAFEMLLM 的 CoE-Attack 在 token 嵌入层级同时优化图像位置嵌入 $P_0^h$ 和文本后缀嵌入 $P_0^t$，实现了跨模态的细粒度对抗噪声注入。
2. **对比目标引入攻防两端**：在攻击步（Eq. 2）和防御步（Eq. 5）均引入对比损失，相对抑制非目标响应的生成概率，这是现有 LLM 对抗训练方法中未见的机制。

### 方法谱系中的技术继承与创新

SAFEMLLM 的技术组件在以下维度上呈现出继承与创新的交织：

| 技术组件 | 继承来源 | 创新点 |
|---------|---------|--------|
| 交替对抗训练框架 | GAN 式 min-max 优化范式 | 首次应用于 MLLM 安全防御，攻击步与防御步共享对比损失结构 |
| 嵌入级对抗扰动 | 对抗样本生成中的嵌入空间攻击思想 | 同时优化图像与文本双模态嵌入，形成跨模态联合扰动 |
| 对比损失 | 对比学习（如 SimCLR、RLHF 中的偏好优化） | 将对比目标同时嵌入攻击生成与防御训练，形成对称的攻防结构 |
| LoRA 参数高效微调 | PEFT 方法族 | 仅微调跨模态适配器和 LLM 解码器，固定视觉编码器，降低计算开销 |
| 效用损失 | 多任务学习中的辅助损失 | 从 LLaVA-Instruct-80K 采样良性数据，显式约束模型不过度拒答 |

### 适用边界与局限

**已覆盖的防御范围**：SAFEMLLM 在六种攻击方法（ImgJP、VAA、GCG、AutoDAN、Fig-Step、MMA）和六种 MLLM 架构上进行了验证，Table 1 显示其对 GCG 攻击的全模型平均 ASR 为 0.00%，对 AutoDAN 为 0.17%，防御效果显著。然而，这些攻击均属于已知攻击范式，模型的防御边界存在以下明确限制：

1. **模态覆盖不足**：当前框架仅针对图像和文本双模态的越狱攻击进行防御，未涉及音频、视频或更复杂的多模态组合攻击场景。这是方法本身的架构局限，而非实验设计缺陷。
2. **攻击者能力假设**：CoE-Attack 生成的对抗噪声依赖于对模型嵌入空间的完全访问（白盒假设），但防御训练后的模型是否能够抵御同样采用对抗训练策略的自适应攻击者，目前缺乏实验验证。
3. **计算资源门槛**：尽管作者声称可在单张 A100 上约四小时完成训练，但对于资源受限的部署环境（如边缘设备、实时推理系统），交替对抗训练的计算开销仍然构成实际障碍。

**泛化性待验证**：Table 1 中 SAFEMLLM 在 MM-SafetyBench 上的平均 ASR 为 0.10%，远低于原始模型的 16.46%，但该基准的攻击样本分布可能与训练时使用的 AdvBench 存在重叠。在面对分布外攻击变种或更强的自适应攻击时，模型的鲁棒性边界仍需进一步界定。

### 开放问题

1. **多模态扩展**：如何将嵌入级对抗训练框架从图文双模态扩展到音频、视频乃至任意模态组合的越狱攻击防御？这需要重新设计跨模态嵌入的联合优化策略。
2. **与安全对齐技术的协同**：SAFEMLLM 的对抗训练能否与 RLHF、红队测试、宪法 AI 等安全对齐技术形成互补，进一步提升模型对未知攻击的鲁棒性？目前尚无实验证据。
3. **计算效率优化**：能否通过攻击步的早停策略、防御步的梯度累积或模型量化等手段，在保持防御性能的同时显著降低训练和推理开销？
4. **自适应攻击的鲁棒性**：当攻击者也采用类似的对抗训练策略（如针对防御模型的梯度进行攻击优化）时，SAFEMLLM 的防御是否依然有效？这需要构建更强的威胁模型进行验证。
5. **过拒答的精确控制**：消融实验（Table 2）已证实效用损失 $L_{utility}$ 对维持良性任务性能至关重要，但如何精确调控安全性与有用性之间的权衡，避免模型在边界模糊的查询上过度拒答，仍是一个开放的系统性问题。



## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Robust_Multimodal_Large_Language_Models_Against_Jailbreak_Attacks.pdf]]
