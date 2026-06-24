---
title: "TINA: Text-Free Inversion Attack for Unlearned Text-to-Image Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TINA_Text_Free_Inversion_Attack_for_Unlearned_Text_to_Image_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/qianlong0502/TINA"
aliases:
- TTFIA
- TINA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过强制空文本条件下的无文本反演，并引入优化步骤强制每一步潜变量满足自洽性约束，可以精确找到一条完全独立于文本条件的确定性生成轨迹，从而恢复被擦除的概念。
primary_logic: 即使文本与图像的关联被抹除，扩散模型内部仍然保留着指向被擦除概念的确定性视觉生成轨迹。这一轨迹可以通过无文本、优化式的 DDIM 反演来发现，并利用该模型自身的生成过程重新激活被禁止的内容。
claims:
- TINA 在所有 8 种裸体擦除防御上均取得最高攻击成功率，尤其是在 AdvUnlearn (78.87％)、SalUn (71.13％) 和 STEREO (80.99％) 等鲁棒防御上显著优于所有文本中心攻击。
- 在艺术风格擦除任务中，TINA 对 ESD (70.0%) 和 AdvUnlearn (70.0%) 的攻击成功率远高于文本基线（UDA 32.0%，CE 8.0%），且对鲁棒方法 STEREO 仍达到 44.0%，而文本攻击全部为 0.0%。
- 对象擦除任务上，面对 Scissorhands 和 STEREO 等现代防御，所有文本攻击均近乎完全失效（ASR 2%–8%），而 TINA 保持 68%–78% 的高成功率，证实视觉知识独立于文本控制。
- 消融实验表明，标准文本引导反演因擦除防御阻挡而失败 (ASR 30%)，优化不足的 TINA-Less 仅 46% ASR，只有充分迭代优化的完整 TINA 能达到高保真重建 (70% ASR)。
---

# TINA: Text-Free Inversion Attack for Unlearned Text-to-Image Diffusion Models

> [!tip] 核心洞察
> 即使文本与图像的关联被抹除，扩散模型内部仍然保留着指向被擦除概念的确定性视觉生成轨迹。这一轨迹可以通过无文本、优化式的 DDIM 反演来发现，并利用该模型自身的生成过程重新激活被禁止的内容。

| 字段 | 内容 |
|------|------|
| 中文题名 | TINA：面向未学习文本到图像扩散模型的无文本反演攻击 |
| 英文题名 | TINA: Text-Free Inversion Attack for Unlearned Text-to-Image Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.17828) · [Code](https://github.com/qianlong0502/TINA) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | TINA (Text-free INversion Attack) |
| Dataset | Nudity Erasure, Artistic Style Erasure, Object Erasure |

> [!tip] 效果简介
> - Nudity Erasure (ESD) 上，Attack Success Rate (ASR, %) 82.39 vs 76.05 (UDA) (+6.34)。
> - Nudity Erasure (AdvUnlearn) 上，Attack Success Rate (ASR, %) 78.87 vs 23.24 (UDA) (+55.63)。
> - Artistic Style Erasure (ESD, Van Gogh) 上，Attack Success Rate (ASR, %) 70.0 vs 32.0 (UDA) (+38.0)。

## 概述

**核心问题**：当前主流的文本到图像扩散模型概念擦除方法，本质上只切断了特定文本条件与禁止概念之间的映射关系，却忽略了模型参数内部仍然潜藏着被擦除概念的底层视觉知识。这意味着，即便文本通道被封锁，攻击者仍可能通过纯视觉路径重新激活被禁止的内容。

**核心洞察**：即使文本与图像的关联被抹除，扩散模型内部依然保留着指向被擦除概念的**确定性视觉生成轨迹**。这一轨迹可以通过无文本、优化式的 DDIM 反演来发现，并利用模型自身的生成过程重新激活被禁止的内容。

**提出方法**：**TINA（Text-Free INversion Attack）** 是一种完全绕过文本模态的概念恢复攻击方法。其核心机制包含两个关键设计：
1. **空文本条件**：以空文本 $c_{\text{null}}$ 替代对抗性文本提示，彻底解耦文本控制通道；
2. **优化式自洽反演**：通过梯度下降在每一步强制潜变量满足精确 DDIM 关系（自洽性损失 $\mathcal{L}_t$，Eq.10），修正标准反演因缺乏文本引导而产生的累积近似误差，从而精确找到目标图像对应的初始噪声 $z_T^*$。

**主要结果**：
- 在**裸体擦除**任务上，TINA 在所有 8 种防御方法上均取得最高攻击成功率，尤其在 AdvUnlearn（78.87%）、SalUn（71.13%）和 STEREO（80.99%）等鲁棒防御上，显著优于所有文本中心攻击方法。
- 在**艺术风格擦除**任务上，TINA 对 ESD 和 AdvUnlearn 的攻击成功率达 70.0%，远超文本基线（UDA 32.0%，CE 8.0%）；面对鲁棒方法 STEREO 仍保持 44.0%，而文本攻击全部为 0.0%。
- 在**对象擦除**任务上，面对 Scissorhands 和 STEREO 等现代防御，所有文本攻击近乎完全失效（ASR 2%–8%），而 TINA 保持 68%–78% 的高成功率，证实视觉知识独立于文本控制。
- **消融实验**表明，标准文本引导反演因擦除防御阻挡而失败（ASR 30%），优化不足的 TINA-Less 仅达 46% ASR，唯有充分迭代优化的完整 TINA 能实现高保真重建（70% ASR）。

**方法定位**：TINA 属于**白盒反演攻击**，需要目标概念的示例图像作为输入。与现有文本中心攻击（如 UDA、P4D、MMA 等）依赖对抗性文本条件不同，TINA 开创了**纯视觉生成路径**的攻击范式，揭示了当前概念擦除技术中“文本-视觉解耦不彻底”的根本性漏洞。

## 背景与动机

### 概念擦除的兴起与文本中心防御范式

随着文本到图像扩散模型（如 Stable Diffusion）的广泛部署，生成包含不当内容（裸露、暴力）或侵犯艺术家版权的特定风格图像引发了严峻的安全与伦理挑战。为应对这一问题，研究者提出了**概念擦除**技术，其核心目标是使消毒后的模型在接收到特定文本条件时不再生成对应的不适概念。主流方法——包括 ESD、FMN、UCE、CA、SEOT、SalUn、AdvUnlearn 和 STEREO——均遵循**文本中心防御范式**：它们通过微调或对抗训练，切断特定文本词元（如“nudity”或“Van Gogh”）与目标视觉概念之间的映射关系。

### 现有攻击的局限：被困在文本通道中

针对上述防御，一系列攻击方法试图重新激活被擦除的概念。然而，这些攻击同样被困在**文本中心范式**中：

- **黑盒攻击**如 **MMA**（Yang et al., CVPR 2024）和 **RAB**（Zhang et al., NeurIPS 2023）依赖固定的对抗提示集或提示修改策略，通过文本条件通道触发模型生成违禁内容。
- **白盒攻击**更进一步：**UDA**（Zhang et al., ECCV 2024）和 **P4D**（Pham et al., CVPR 2024）直接优化对抗性文本嵌入或提示，以最小化消毒模型对目标图像的去噪误差或使其噪声预测与原模型对齐；**CCE**（Kong et al., ECCV 2024）则通过文本反演学习新的嵌入向量作为被擦除概念的代理。

这些方法的共同假设是：**要恢复被擦除的概念，必须找到能绕过文本过滤器的对抗性文本条件**。然而，这一假设忽略了一个根本性问题——概念擦除仅切断了文本到图像的映射，而**模型参数中仍可能潜藏着被擦除概念的底层视觉知识**。一旦文本通道被有效封锁（如 AdvUnlearn 和 STEREO 等鲁棒防御所做的那样），所有文本中心攻击便近乎完全失效。实验数据充分证实了这一点：在对象擦除任务中，面对 Scissorhands 和 STEREO 防御，文本攻击的成功率仅为 2%–8%（Table 4）；在艺术风格擦除任务中，面对 STEREO，所有文本攻击的成功率均为 0.0%（Table 2）。

### 核心洞察：视觉知识的持久性与独立生成轨迹

本文的核心洞察在于：**即使文本与图像的关联被抹除，扩散模型内部仍然保留着指向被擦除概念的确定性视觉生成轨迹**。这一轨迹完全独立于文本条件，可以通过纯视觉路径被发现和利用。Figure 1 直观地揭示了这一漏洞：传统概念擦除（Concept Erasure）仅切断特定文本条件与不适概念的链接，而 TINA 完全绕过文本通路，在空文本条件下找到能够再生概念的初始噪声，证明视觉知识在现有消毒模型中持续存在。

这一洞察引出了一个关键的科学问题：**如何在不依赖任何文本条件的情况下，精确地找到这条隐藏在模型参数中的视觉生成轨迹？** 这正是 TINA 方法设计的出发点。

## 核心创新

TINA 的核心创新在于**彻底切换了攻击的输入模态与生成路径**：从“寻找对抗性文本条件”转向“在空文本条件下恢复确定性视觉轨迹”。这一转变由三个紧密耦合的 changed slots 实现。

### 1. 攻击输入条件：从对抗性文本到空文本

所有现有攻击方法——无论是黑盒的 **MMA** (Yang et al., CVPR 2024)、**RAB** (Zhang et al., NeurIPS 2023)，还是白盒的 **UDA** (Zhang et al., ECCV 2024)、**P4D** (Pham et al., CVPR 2024)、**CCE** (Kong et al., ECCV 2024)——均以寻找或优化一个对抗性文本条件 $c_{\text{adversarial}}$ 为核心策略。它们假设只要找到合适的文本输入，就能重新激活被擦除的概念。

TINA 则完全放弃文本条件，转而使用**空文本条件 $c_{\text{null}}$**（即无条件嵌入）。这一设计的直接后果是：攻击路径不再经过被擦除方法刻意切断的文本-图像映射通道，从而在原理上绕过了所有文本中心防御。如 Figure 1 所示，概念擦除方法通常切断特定文本条件与目标概念的关联，而 TINA 证明了即便在文本通道被完全阻断的情况下，模型内部的视觉知识仍然可以通过纯视觉路径被重新激活。

### 2. 反演机制：从标准 DDIM 近似到优化型自洽反演

标准 DDIM 反演使用近似公式 $z_t \approx f_\theta(z_{t-1}, t, c)$（Eq. 6），即用前一时刻的噪声预测来估计当前潜变量。这种近似在文本引导下尚可接受，但在空文本条件下会因累积误差导致轨迹严重漂移（见 Figure 3），使得最终重建的图像丢失精细细节甚至完全偏离目标概念。

TINA 将反演重新表述为一个**不动点优化问题**。其核心是精确 DDIM 关系（Eq. 3）：

$$z_t = C_1(t) z_{t-1} + C_2(t) \cdot \epsilon_\theta(z_t, t, c)$$

该等式右侧本身依赖于 $z_t$，因此无法直接求解。TINA 定义诱导映射 $f_\theta^*(z_t, z_{t-1}, t, c)$（Eq. 9），并在每一步 $t$ 上通过梯度下降最小化自洽性损失（Eq. 10）：

$$\mathcal{L}_t(z_t) = \left\| f_\theta^*(z_t, z_{t-1}, t, c_{\text{null}}) - z_t \right\|_2^2$$

每步内循环执行 $K=25$ 次优化迭代（Algorithm 1），强制当前潜变量 $z_t$ 精确满足 DDIM 的确定性与可逆性约束。这使得 TINA 能够从目标图像潜在 $z_0$ 出发，逐步恢复出一条**精确的、完全独立于文本条件的生成轨迹**，最终得到初始噪声 $z_T^*$。

### 3. 攻击路径：从文本条件通道到纯视觉生成路径

传统文本中心攻击的生成路径为：

$$c_{\text{adversarial}} \rightarrow \epsilon_\theta(z_t, t, c_{\text{adversarial}}) \rightarrow \text{生成图像}$$

这条路径上，擦除防御通过修改模型对特定文本条件的响应来阻断攻击。

TINA 的生成路径为：

$$z_T^* \xrightarrow[\text{DDIM 采样}]{\text{空文本条件 } c_{\text{null}}} z_0' \rightarrow \text{恢复的概念图像}$$

在这条路径上，**文本编码器完全不参与**。攻击者只需将优化得到的 $z_T^*$ 输入被擦除模型，在空文本条件下执行标准 DDIM 采样，即可确定性地再生被禁止的概念。Figure 2 完整展示了这一两阶段框架：(a) 无文本优化反演找到 $z_T^*$；(b) 确定性概念再生生成 $z_0'$。

### 创新点的因果链条

这三个 changed slots 形成了一条清晰的因果链：

1. **空文本条件**使攻击绕过文本通道的防御；
2. 但空文本条件下标准反演因近似误差而失败（Figure 3），因此需要**优化型自洽反演**来精确恢复轨迹；
3. 精确轨迹 $z_T^*$ 使得**纯视觉生成路径**成为可能，直接利用模型自身未被擦除的视觉知识重建概念。

消融实验（Figure 6）直接验证了这一链条的必要性：标准文本引导反演的 ASR 仅 30%，优化不足的 TINA-Less 为 46%，而完整 TINA（$K=25$）达到 70%。这表明，**充分的固定点优化是实现精确迹线和高攻击成功率的关键**，三者缺一不可。

## 整体框架

TINA 的攻击范式完全绕开文本条件通道，转而利用扩散模型内部**独立于文本的视觉生成轨迹**来恢复被擦除的概念。其整体 pipeline 由三个串行模块构成，形成“编码→反演→再生”的闭环攻击流程。

### 模块一：目标图像潜在提取

攻击者首先获取一张目标概念图像（例如裸体图像、梵高风格画作或特定对象照片），通过冻结的 VAE 编码器将其映射到潜在空间，得到干净潜在变量 $z_0$。这一步骤为标准操作，不涉及任何文本条件。

### 模块二：无文本优化反演（核心创新）

从 $t=1$ 到 $T$，TINA 在**空文本条件** $c_{\mathrm{null}}$ 下执行逐步优化反演。与标准 DDIM 反演使用近似递推不同，TINA 将每一步的反演重新定义为一个不动点问题：精确 DDIM 反演关系要求 $z_t = C_1(t) z_{t-1} + C_2(t) \cdot \epsilon_\theta(z_t, t, c)$，但等式右侧的噪声预测 $\epsilon_\theta$ 本身依赖于待求解的 $z_t$。标准反演通过用前一时刻的噪声预测替代当代噪声预测来回避这一循环依赖，导致累积近似误差在空文本条件下急剧放大（Figure 3 展示了标准反演在空文本路径上的漂移现象）。

TINA 的关键设计是**在每一步强制自洽性约束**：定义诱导映射 $f_\theta^*(z_t, z_{t-1}, t, c_{\mathrm{null}})$，并最小化自洽性损失

$$\mathcal{L}_t(z_t) = \left\| f_\theta^*(z_t, z_{t-1}, t, c_{\mathrm{null}}) - z_t \right\|_2^2$$

通过内循环 $K=25$ 次梯度下降优化，每一步都精确满足 DDIM 的确定性关系，最终输出高质量的初始噪声向量 $z_T^*$。完整的反演过程由 Algorithm 1 给出形式化描述。

### 模块三：确定性概念再生

获得 $z_T^*$ 后，TINA 将其输入**同一个被擦除模型** $\epsilon_\theta$，在空文本条件下执行标准确定性 DDIM 采样。由于 $z_T^*$ 精确对应目标图像的生成轨迹起点，且 DDIM 采样是确定性的，模型将沿着该轨迹生成恢复后的概念图像 $x'$，证明视觉知识在模型参数中依然完整保留。

### 输入输出流总结

- **输入**：一张目标概念图像（经 VAE 编码为 $z_0$）
- **中间产物**：优化后的初始噪声 $z_T^*$（在空文本条件下通过自洽反演获得）
- **输出**：再生图像 $x'$（由同一被擦除模型在空文本条件下确定性采样生成）
- **关键约束**：整个流程**不使用任何文本条件**，完全依赖被擦除模型自身的视觉生成能力

这一框架的优雅之处在于：它不攻击文本编码器或文本-图像映射，而是直接利用扩散模型作为“视觉知识存储器”的本质——即使文本关联被切断，模型仍能从噪声中确定性地重建被禁止的视觉内容。Figure 2 以图示方式完整呈现了 (a) 反演攻击与 (b) 确定性再生的两阶段流程。

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/002_Figure_2.jpg]]
*Figure 2: The TINA (Text-free INversion Attack) framework. (a) Text-Free Inversion Attack: An optimization-based, null-text*

### 补充图表

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/001_Figure_1.jpg]]
*Figure 1: Conceptual overview of text-centric erasure vulnerabilities and our TINA attack. Concept Erasure usually severs the link between a specific text condition and the undesired concept. Previous Attacks remain text-centric, finding adversarial text condition to reactivate the concept. Our TINA bypasses the text pathway entirely. Using an empty text condition, it finds a noise to regenerate the concept, proving the visual knowledge persists in the existing erased models*

## 核心模块与公式推导

### 3.1 DDIM 确定性生成与反演基础

TINA 的核心攻击路径建立在 DDIM 的确定性生成-反演对偶性之上。给定一个已擦除模型 $\epsilon_\theta$ 和条件 $c$，DDIM 的采样过程是确定性的：从初始噪声 $z_T$ 出发，每一步根据当前潜变量 $z_t$ 预测干净潜变量，再递推到 $z_{t-1}$。

从噪声潜变量 $z_t$ 预测干净潜变量 $\hat{z}_0$ 的公式为：

$$\hat{z}_0(z_t) = \frac{z_t - \sqrt{1 - \alpha_t} \epsilon_\theta(z_t, t, c)}{\sqrt{\alpha_t}} \tag{1}$$

基于此，单步确定性采样递推为：

$$z_{t-1} = \sqrt{\alpha_{t-1}} \hat{z}_0(z_t) + \sqrt{1 - \alpha_{t-1}} \cdot \epsilon_\theta(z_t, t, c) \tag{2}$$

**关键洞察**：公式 (2) 定义了从噪声到图像的确定性映射。如果能够精确地逆转这一过程——即从目标图像反推出其对应的初始噪声 $z_T$——那么将该噪声重新输入同一模型，就能确定性地重建目标图像。这正是 TINA 攻击范式的数学基础。

然而，直接对公式 (2) 求代数逆会遭遇循环依赖：反演 $z_t$ 需要 $\epsilon_\theta(z_t, t, c)$，而该噪声预测本身又以 $z_t$ 为输入。精确的 DDIM 反演关系为：

$$z_t = C_1(t) z_{t-1} + C_2(t) \cdot \epsilon_\theta(z_t, t, c) \tag{3}$$

其中 $C_1(t)$ 和 $C_2(t)$ 是与时间步相关的系数（由 $\alpha_t$ 序列决定）。这是一个关于 $z_t$ 的隐式方程。

### 3.2 标准 DDIM 反演的失败模式

标准 DDIM 反演通过近似来绕过公式 (3) 的隐式性：用 **前一时刻** 的噪声预测替代当前时刻的噪声预测：

$$z_t \approx f_\theta(z_{t-1}, t, c) \tag{6}$$

这一近似在文本引导路径上通常可接受，因为文本条件提供了强约束。但在 TINA 所需的 **空文本条件** $c_{\text{null}}$ 下，该近似误差会在反演过程中逐步累积，导致反演轨迹偏离真实的生成流形（如 Figure 3 所示）。当被擦除模型切断了文本到概念的映射后，文本引导路径被直接阻断，而空文本路径则因累积误差而漂移，两种路径均无法恢复目标概念。

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/003_Figure_3.jpg]]
*Figure 3: Standard DDIM inversion fails to find the generative trajectory. The text-guided path (S) is blocked by the erasure, while the null-text path*

### 3.3 TINA 的核心创新：优化型自洽反演

TINA 的关键技术贡献在于将反演重新表述为一个 **优化问题**，通过在每一步强制精确的自洽性约束来消除近似误差。

**第一步：定义不动点映射**。将公式 (3) 的右端视为一个关于 $z_t$ 的诱导映射：

$$f_\theta^*(z_t, z_{t-1}, t, c) = C_1(t) z_{t-1} + C_2(t) \cdot \epsilon_\theta(z_t, t, c) \tag{9}$$

如果 $z_t$ 是精确反演解，则它必须是该映射的不动点：$f_\theta^*(z_t, z_{t-1}, t, c) = z_t$。

**第二步：构建自洽性损失**。在空文本条件 $c_{\text{null}}$ 下，每一步的优化目标是最小化当前潜变量与不动点映射输出之间的 $L_2$ 距离：

$$\mathcal{L}_t(z_t) = \left\| f_\theta^*(z_t, z_{t-1}, t, c_{\text{null}}) - z_t \right\|_2^2 \tag{10}$$

**第三步：迭代优化求解**。从 $t = 1$ 到 $T$，每一步以标准反演结果作为 $z_t$ 的初始值，通过梯度下降最小化 $\mathcal{L}_t$，内循环执行 $K = 25$ 次迭代。这一过程确保了每一步的潜变量都精确满足 DDIM 关系，从而找到一条完全独立于文本条件的确定性生成轨迹，最终输出精确的初始噪声 $z_T^*$。

### 3.4 确定性概念再生

获得 $z_T^*$ 后，攻击进入再生阶段：将 $z_T^*$ 输入同一被擦除模型 $\epsilon_\theta$，在空文本条件 $c_{\text{null}}$ 下执行标准 DDIM 采样（公式 (2)），生成恢复后的目标概念图像。由于整个流程完全绕过了文本条件通道，仅依赖模型参数中潜藏的视觉知识，因此能够绕过现有文本中心的擦除防御。

### 3.5 公式变量含义汇总

| 符号 | 含义 |
|------|------|
| $z_t$ | 时间步 $t$ 的噪声潜变量 |
| $\hat{z}_0(z_t)$ | 从 $z_t$ 预测的干净潜变量 |
| $\epsilon_\theta$ | 扩散模型的噪声预测网络（已被概念擦除处理） |
| $\alpha_t$ | DDIM 噪声调度参数，控制每步的信噪比 |
| $C_1(t), C_2(t)$ | 由 $\alpha_t$ 序列决定的确定性系数 |
| $c_{\text{null}}$ | 空文本条件（TINA 的输入条件） |
| $f_\theta^*$ | 精确 DDIM 反演的不动点诱导映射 |
| $\mathcal{L}_t$ | 第 $t$ 步的自洽性损失函数 |
| $z_T^*$ | 优化反演得到的精确初始噪声 |
| $K$ | 每步内循环的梯度下降迭代次数（$K = 25$） |

## 实验与分析

### 核心发现：视觉知识的独立持久性

TINA 的核心实验结论可以浓缩为一句话：**即使文本到图像的映射被彻底切断，扩散模型内部仍然保留着指向被擦除概念的确定性视觉生成轨迹。** 这一发现通过三个互补的任务维度——裸体擦除、艺术风格擦除和对象擦除——得到了系统性验证。在所有任务中，当文本中心攻击面对鲁棒防御完全失效时，TINA 仅凭空文本条件和一张目标图像即可高成功率地恢复被禁止的内容。

**Figure 4** 给出了裸体擦除和梵高风格擦除的定性对比。文本攻击（UDA、P4D、CCE）在 ESD 等弱防御上尚能生成部分敏感内容，但在 AdvUnlearn 和 STEREO 等鲁棒防御下输出几乎完全被净化。TINA 在所有列上均以红框标记成功再生，视觉质量与目标图像高度一致。

---

### 主实验结果

#### 裸体擦除：全面领先

**Table 1** 报告了 8 种概念擦除防御下的攻击成功率（ASR）。TINA 在所有防御上均取得最高或并列最高的 ASR：

| 防御方法 | TINA (ASR%) | 最强文本基线 (ASR%) | 增量 |
|----------|-------------|---------------------|------|
| ESD | **82.39** | 76.05 (UDA) | +6.34 |
| MACE | **92.96** | 88.73 (UDA) | +4.23 |
| AdvUnlearn | **78.87** | 23.24 (UDA) | **+55.63** |
| SalUn | **71.13** | 38.73 (UDA) | +32.40 |
| STEREO | **80.99** | 19.72 (UDA) | **+61.27** |

关键瓶颈在于：AdvUnlearn 和 STEREO 这类鲁棒防御通过对抗训练或负样本驱动的方式，几乎完全阻断了文本条件通道。UDA 和 P4D 等白盒文本攻击在这些防御上骤降至 20% 以下，而 TINA 保持接近 80% 的 ASR。这直接证实了 **causal knob**——文本路径被切断后，视觉路径仍可通过无文本反演被独立激活。

#### 艺术风格擦除：鲁棒防御下的唯一有效攻击

**Table 2** 展示了梵高风格擦除任务的 ASR 对比。TINA 在 ESD 和 AdvUnlearn 上均达到 70.0%，而最强文本基线 UDA 仅为 32.0% 和 4.0%。更关键的是，面对 STEREO 防御，所有文本攻击的 ASR 全部归零（0.0%），TINA 仍保持 44.0% 的成功率。

这一结果揭示了文本攻击的根本局限：它们试图通过优化对抗性提示来“欺骗”已被切断的文本映射，而 TINA 完全绕过了这一已被破坏的通道。STEREO 上 44% 的 ASR 虽然下降，但仍远高于零，说明 STEREO 的对抗训练对风格相关的视觉知识造成了一定干扰，但并未完全消除。

#### 对象擦除：现代防御的失效

**Table 4** 报告了对象擦除（tench 鱼、降落伞等）任务的结果。面对 Scissorhands 和 STEREO 等现代防御：

| 防御方法 | TINA (ASR%) | UDA (ASR%) | CCE (ASR%) |
|----------|-------------|------------|------------|
| Scissorhands | **78.0** | 2.0 | 4.0 |
| STEREO | **72.0** | 6.0 | 8.0 |

文本攻击近乎完全失效（2%–8%），而 TINA 保持 68%–78% 的高成功率。这进一步验证了 **real bottleneck**：当前概念擦除方法只切断了文本到图像的映射，而模型参数中潜藏的被擦除概念的底层视觉知识几乎完好无损。

---

### 消融实验：优化的必要性

**Figure 6** 和 **Section 7** 的消融实验拆解了 TINA 各组件对攻击成功率的贡献。以 ESD 防御下的 tench 鱼对象擦除为例：

- **标准文本引导反演（Standard Inv.）**：ASR 仅 30%。文本引导路径被擦除防御阻挡，导致反演轨迹完全偏离。
- **优化不足的 TINA-Less**：ASR 为 46%。减少内循环优化迭代次数（K 值不足）使得自洽性约束未能充分满足，累积近似误差仍然显著。
- **完整 TINA（K=25）**：ASR 达到 70%。充分的固定点优化（每步 25 次梯度下降）精确强制了 Eq. (10) 的自洽性关系，找到了高保真的初始噪声 $z_T^*$。

这一消融直接验证了 **core insight** 中的关键机制：仅有无文本条件是不够的，必须通过优化来纠正标准 DDIM 反演在缺乏文本引导时产生的累积近似误差。**Figure 7** 从视觉层面佐证了这一点——在梵高风格擦除任务上，朴素空文本 DDIM 反演可以大致恢复全局构图，但丢失了笔触纹理和局部结构等精细风格细节；而 TINA 的优化反演则产生了明显更丰富、更忠实的视觉重建。

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/013_Figure_7.jpg]]
*Figure 7: Visual comparison between naive null-text DDIM inversion and our optimized TINA inversion on the Van Gogh style erasure task. While the naive null-text DDIM inversion can roughly recover the global composition, it often fails to preserve finegrained stylistic details, such as brushstroke textures and local structures. In contrast, TINA produces reconstructions with noticeably richer and more faithful visual details*

此外，与通用 DDIM 重建方法 EasyInv 的比较（**Table 5**）进一步表明，一般的重建方法不能替代 TINA 的专门优化反演。在所有五个防御上，TINA 均大幅领先（例如 Scissorhands: 78.0% vs 34.0%），说明针对概念恢复的优化反演具有不可替代性。

---

### 失败模式与局限

**Figure 9** 展示了 TINA 在 STEREO 风格擦除任务上的典型失败案例。虽然 TINA 成功保留了目标图像的空间构图，但重建结果未能恢复梵高风格的笔触、色彩和纹理等特征。这与 Table 2 中 STEREO 上 44% 的 ASR 相呼应，表明 STEREO 的对抗训练过程在一定程度上干扰了风格特定的高级视觉知识。

这一失败模式揭示了当前无文本攻击的边界：当防御方法不仅切断文本映射，还通过对抗训练直接扰动视觉表示空间时，无文本反演找到的生成轨迹可能仅保留语义内容（构图、物体身份）而丢失风格属性。这为未来防御设计提供了方向——直接针对视觉级表示进行对抗性遗忘，而非仅仅切断文本条件通道。

---

### 泛化性与架构无关性

**Figure 8** 提供了 TINA 泛化至 DiT 架构（PixArt-XL-2-512x512）的定量证据。在 ESD 擦除“降落伞”概念后，被擦除模型无法生成降落伞图像，但 TINA 成功恢复了该概念。这表明视觉知识的持久性漏洞并非 UNet 架构特有，而可能是扩散模型生成机制的内禀属性。

**Figure 5** 的 t-SNE 可视化进一步揭示了这一漏洞的结构化特征：优化后的初始噪声 $z_T^*$ 及其对应的 UNet 中间层激活，在不同被擦除概念之间形成了清晰可分离的簇。这说明每个被擦除概念在模型的潜空间和特征空间中仍占据着独特的、可被定位的区域，为无文本反演提供了可被利用的几何结构。

---

### 公平性保障

所有攻击方法的比较均在严格公平的条件下进行：使用与 UDA 相同的图像生成基准、提示集和评估分类器（裸体任务使用 NudeNet，风格任务使用 ViT 风格分类器，对象任务使用 ResNet-50）。基线攻击的超参数严格遵循各自原始论文的推荐设置（如 MMA 的 1000 固定提示，UDA/P4D 的 N=5/3 优化 token、40 次迭代等）。TINA 与 EasyInv 的比较同样在文本自由条件下进行，以消除条件偏差。

### 补充图表

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison of attack performance on (a) Nudity Erasure and (b) Style Erasure (Van Gogh). Images with a red border indicate a successful attack. Our TINA (bottom row) consistently regenerates the forbidden concepts, bypassing most of defenses, while text-centric attacks fail against robust methods. Sensitive content is redacted*

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/006_Table_2.jpg]]
*Table 2: Comparison of Attack Success Rates (ASR, in %) on the artistic style erasure task. We report the performance of our TINA against three baselines across eight unlearning methods. Bold denotes the highest ASR, while underlined denotes the second highest*

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/009_Table_4.jpg]]
*Table 4: Attack Success Rates (ASR, in %) for object erasure. Our TINA bypasses modern defenses where text-centric attacks fail*

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/010_Figure_6.jpg]]
*Figure 6: Ablation study of attack results on the ESD method for tench object erasure. From left to right: target concept, Standard Inv. (standard text-guided inversion), TINA-Less (with insufficient optimization), and our full TINA method*

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/008_Figure_5.jpg]]
*Figure 5: t-SNE visualization of (a) the optimized initial noises*

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/014_Figure_8.jpg]]
*Figure 8: Generalization of TINA to a DiT-based architecture (PixArt-XL-2-512x512). We erase the “Parachute” concept using ESD and then apply TINA. While the erased model fails to generate parachutes, TINA successfully recovers the concept, demonstrating architecture-agnostic generalizability*

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/007_Table_3.jpg]]
*Table 3: Applicability of baseline attack methods to different tasks. ✓ denotes applicability, while ✗ denotes non-applicability*

![[assets/figures/papers/paper_list_l2226_https_arxiv_org_abs_2603_17828/figures/015_Figure_9.jpg]]
*Figure 9: Failure cases of TINA on the STEREO style erasure (Van Gogh) task. While TINA preserves the spatial composition of the target images, the reconstructed results fail to recover the distinctive artistic style, indicating that the adversarial training procedure of STEREO partially disrupts the style-specific visual knowledge*

## 方法谱系与知识库定位

### 核心瓶颈：文本中心擦除的视觉盲区

当前主流概念擦除方法（如 ESD、FMN、SalUn、AdvUnlearn、STEREO、Scissorhands 等）的设计哲学高度一致：**切断特定文本条件与不希望生成的概念之间的映射**。这一策略在对抗文本提示攻击时表现有效，但 TINA 的发现揭示了一个根本性的防御盲区——**扩散模型参数中仍潜藏着被擦除概念的底层视觉知识**，这些知识独立于文本条件通道存在。一旦攻击者绕过文本输入路径，直接从视觉生成轨迹入手，现有防御体系便形同虚设。

这一瓶颈的因果机制可概括为：擦除操作仅修改了文本到图像的“翻译层”，而未触及模型内部已学到的视觉先验。因此，文本编码的攻击被阻，但视觉生成路径仍可被利用。

### 因果调控旋钮：无文本自洽反演

TINA 的核心创新在于识别并操控了一个关键的因果旋钮：**通过强制空文本条件下的无文本反演，并引入优化步骤强制每一步潜变量满足自洽性约束，可以精确找到一条完全独立于文本条件的确定性生成轨迹**。

具体而言，标准 DDIM 反演在缺乏文本引导时会因累积近似误差而漂移（Figure 3），无法精确恢复目标概念的初始噪声。TINA 将反演重新定义为不动点优化问题：

- 定义自洽映射 $f_{\theta}^{*}(z_{t}, z_{t-1}, t, c_{\mathrm{null}}) = C_{1}(t) z_{t-1} + C_{2}(t) \cdot \epsilon_{\theta}(z_{t}, t, c_{\mathrm{null}})$（Eq.9）；
- 每步通过最小化自洽损失 $\mathcal{L}_{t}(z_{t}) = \| f_{\theta}^{*}(z_{t}, z_{t-1}, t, c_{\mathrm{null}}) - z_{t} \|_{2}^{2}$（Eq.10）进行内循环优化（K=25 次迭代）。

这一设计使得 TINA 完全解耦文本控制，从纯视觉路径恢复被擦除概念的确定性生成轨迹。

### 与基线方法的谱系关系

TINA 与现有攻击方法的核心区别在于**攻击输入条件**和**倒推机制**两个维度（Table 3 总结了各方法的任务适用性）：

| 方法 | 攻击条件 | 倒推机制 | 攻击路径 |
|------|---------|---------|---------|
| **MMA**（Yang et al., CVPR 2024） | 固定对抗提示集 | 无需反演（黑盒） | 文本通道 |
| **UDA**（Zhang et al., ECCV 2024） | 优化对抗文本提示 | 无需反演（白盒） | 文本通道 |
| **P4D**（Pham et al., CVPR 2024） | 优化对抗提示嵌入 | 无需反演（白盒） | 文本通道 |
| **RAB**（Zhang et al., NeurIPS 2023） | 修改提示生成对抗提示 | 无需反演（黑盒） | 文本通道 |
| **CCE**（Kong et al., ECCV 2024） | 文本反演学习新嵌入 | 文本反演 | 文本通道 |
| **TINA**（本文） | **空文本条件 $c_{\mathrm{null}}$** | **优化型自洽 DDIM 反演** | **纯视觉路径** |

所有基线方法均依赖文本条件通道激活视觉知识，而 TINA 是首个完全绕过文本模态、直接利用模型内部视觉轨迹的攻击范式。这一差异在鲁棒防御上体现得尤为显著：面对 AdvUnlearn 的裸体擦除，UDA 仅 23.24% ASR，而 TINA 达到 78.87%；面对 STEREO 的风格擦除，所有文本攻击 ASR 均为 0.0%，TINA 仍保持 44.0%。

### 适用边界与局限

**适用边界**：
- TINA 适用于任何基于 UNet 架构的扩散模型概念擦除防御，且在 DiT 架构（PixArt-XL-2-512x512）上初步验证了架构无关的泛化能力（Figure 8）。
- 攻击需要目标概念的示例图像作为输入，属于需要一定先验知识的灰盒设定，而非完全无先验的黑盒攻击。

**已知局限**：
1. **对抗性鲁棒防御的部分抵抗**：在 STEREO 的艺术风格擦除任务上，TINA 的 ASR 降至 44%，且重建图像未能恢复笔触等精细风格特征（Figure 9）。这表明强对抗训练可以在一定程度上干扰高级视觉知识，但尚不能完全消除。
2. **输入依赖性**：TINA 需要目标概念图像作为反演起点，这限制了其在完全未知概念上的直接应用。不过，Figure 5 的 t-SNE 可视化显示，优化后的初始噪声及其 UNet 激活在不同概念间形成可分离的簇，暗示可能存在跨图像的噪声先验。

### 开放问题与防御启示

TINA 的成功暴露了当前概念擦除范式的结构性缺陷，由此衍生出若干关键开放问题：

1. **视觉级遗忘的必要性**：当前方法仅切断文本映射，TINA 证明了视觉知识的持久性。如何开发能直接消除内部视觉表示（而非仅阻断文本通道）的鲁棒遗忘范式，是该领域最紧迫的挑战。

2. **架构迁移的普适性**：TINA 在 PixArt-XL 上的初步成功提示了架构无关的漏洞，但 DiT 等新型骨干中视觉知识的持久性是否与 UNet 完全一致，仍需系统研究。

3. **防御策略的反向设计**：能否利用 TINA 揭示的视觉轨迹来设计主动防御？例如，在空文本条件下注入对抗性噪声以破坏反演路径，或通过微调模型使 $c_{\mathrm{null}}$ 条件下的生成轨迹本身就不包含被擦除概念的信息。

4. **与通用重建方法的边界**：消融实验（Table 5）表明，通用 DDIM 重建方法 EasyInv 在文本自由条件下远逊于 TINA（如 Scissorhands 上 34.0% vs 78.0%），说明一般的重建方法不能替代专门针对概念恢复的优化反演，但两者的本质差异仍需更深入的理论刻画。

## 原文 PDF

![[paperPDFs/CVPR_2026/TINA_Text_Free_Inversion_Attack_for_Unlearned_Text_to_Image_Diffusion_Models.pdf]]