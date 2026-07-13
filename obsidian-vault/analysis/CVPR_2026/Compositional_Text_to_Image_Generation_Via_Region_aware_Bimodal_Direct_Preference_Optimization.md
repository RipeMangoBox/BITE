---
title: Compositional Text-to-Image Generation Via Region-aware Bimodal Direct Preference Optimization
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Compositional_Text_to_Image_Generation_Via_Region_aware_Bimodal_Direct_Preference_Optimization.pdf
project_link: null
code_link: "https://github.com/anzeameol/BiDPO"
aliases:
- BBDPO
- CTIGRABDPO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 双模态(文本+图像)联合直接偏好优化(BIDPO)与区域感知的掩码引导损失,通过将图像偏好对齐隐式地分解为两个显式的文本偏好对齐过程,并对编辑区域施加更高的训练权重。
primary_logic: 图像到图像的偏好对比学习可以通过组合两个文本到文本的偏好对比学习过程隐式实现——对同一图像,模型学习偏好正确描述而非错误描述;对不同图像,通过交换图文配对关系隐式建立图像偏好。在此基础上,对编辑区域施加掩码引导可以进一步增强细粒度对齐能力。
claims:
- BIDPO在T2I-CompBench的属性绑定类别(color/shape/texture)上相比SDXL基线平均提升约17%,整体提升约10%
- SDXL-BIDPO在GenEval整体得分从0.53提升至0.62,超越多个对比方法
- 区域级引导在BIDPO基础上进一步带来1.2%(T2I-CompBench)和1.4%(GenEval)的提升
- BIDPO在MMDiT架构(SD3-Medium)上也有效,超越Flux,证明其模型无关性
---

# Compositional Text-to-Image Generation Via Region-aware Bimodal Direct Preference Optimization

> [!tip] 核心洞察
> 图像到图像的偏好对比学习可以通过组合两个文本到文本的偏好对比学习过程隐式实现——对同一图像,模型学习偏好正确描述而非错误描述;对不同图像,通过交换图文配对关系隐式建立图像偏好。在此基础上,对编辑区域施加掩码引导可以进一步增强细粒度对齐能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于区域感知双模态直接偏好优化的组合式文本到图像生成 |
| 英文题名 | Compositional Text-to-Image Generation Via Region-aware Bimodal Direct Preference Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_Compositional_Text-to-Image_Generation_Via_Region-aware_Bimodal_Direct_Preference_Optimization_CVPR_2026_paper.html) · [Code](https://github.com/anzeameol/BiDPO) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | BIDPO (Bimodal Direct Preference Optimization) |
| Dataset | T2I-CompBench, GenEval, DPG-Bench, GenEval 2 |

> [!tip] 效果简介
> - T2I-CompBench 上，Color (属性绑定) 79.35 (SDXL-BIDPO) vs 58.90 (SDXL) (+20.45)；Shape (属性绑定) 61.35 (SDXL-BIDPO) vs 43.98 (SDXL) (+17.37)；Texture (属性绑定) 68.79 (SDXL-BIDPO) vs 50.76 (SDXL) (+18.03)。
> - GenEval 上，Overall Score 0.62 (SDXL-BIDPO) vs 0.53 (SDXL) (+0.09)。
> - DPG-Bench 上，Overall Score 78.84 (SDXL-BIDPO) vs 73.38 (SDXL) (+5.46)。

## 概要

**问题瓶颈**：现有文本到图像（T2I）扩散模型在组合式提示生成中表现不佳，核心瓶颈在于模型缺乏对文本与图像模态间精细对齐的偏好学习机制。以 **Diffusion DPO**（Wallace et al., CVPR 2024）为代表的现有直接偏好优化方法仅关注图像级偏好对比，忽略了文本模态的对齐信号，同时对复杂场景中关键编辑区域缺乏有针对性的引导。

**核心方法**：本文提出 **BIDPO（Bimodal Direct Preference Optimization）**，一种双模态直接偏好优化框架。其核心洞察在于：图像到图像的偏好对比学习可以通过组合两个文本到文本的偏好对比过程隐式实现——对同一图像，模型学习偏好正确描述而非错误描述；对不同图像，通过交换图文配对关系隐式建立图像偏好（见 Figure 2）。在此基础上，BIDPO 引入区域感知的掩码引导损失，根据编辑对象的边界框生成区域掩码，对关键编辑区域赋予更高的训练权重，使模型聚焦于组合变化相关的细粒度对齐。

**方法定位**：BIDPO 属于扩散模型的后训练偏好优化方法，以 **SDXL**（Podell et al., arXiv 2023）和 **SD3-Medium**（Esser et al., ICML 2024）为基座模型，通过 LoRA 高效微调（rank=8，200 步，有效 batch size 2048，4×H100 GPU 约 13 小时）。训练数据来自自动构建的 **BICOMP** 数据集（57,474 原始图像 + 94,502 编辑图像，覆盖 6 个组合维度）与 VisMin 数据集联合，共计约 53k 样本。

**主要结果**（详见 Table 2–7）：
- 在 T2I-CompBench 属性绑定类别上，SDXL-BIDPO 相比 SDXL 基线平均提升约 17%（Color: 79.35 vs 58.90；Shape: 61.35 vs 43.98；Texture: 68.79 vs 50.76），整体提升约 10%。
- 在 GenEval 上，整体得分从 0.53 提升至 0.62，超越多个对比方法。
- 区域级引导在 BIDPO 基础上进一步带来 1.2%（T2I-CompBench）和 1.4%（GenEval）的提升。
- BIDPO 在 MMDiT 架构（SD3-Medium）上也有效，在 GenEval 2 组合性评估上超越 **Flux**（Black Forest Labs, 2024），验证了其模型无关性。
- 视觉美学质量（HPSv2）同步提升（32.87 vs 30.22），表明组合性增强不以牺牲图像质量为代价。



文本到图像（T2I）扩散模型近年来取得了显著进展，但在处理组合式文本提示时仍面临核心挑战——模型生成的图像往往无法准确反映提示中描述的对象属性、空间关系或数量约束。这一瓶颈的根源在于，现有模型缺乏对文本与图像模态间精细对齐的偏好学习机制。

当前主流的后训练优化方法存在两个关键缺口。其一，以 **Diffusion DPO**（Wallace et al., CVPR 2024）为代表的直接偏好优化方法仅关注图像级别的偏好对比，完全忽略了文本模态的对齐——模型学习区分“好图像”与“差图像”，却未能显式学习“正确描述”与“错误描述”之间的偏好关系。其二，这些方法在复杂场景中对关键编辑区域缺乏有针对性的引导——全局损失函数对所有空间位置赋予同等权重，使得模型难以聚焦于组合变化真正发生的区域。

从因果机制来看，图像到图像的偏好对比学习实际上可以通过组合两个文本到文本的偏好对比过程来隐式实现：对同一图像，模型学习偏好正确描述而非错误描述；对不同图像，通过交换图文配对关系隐式建立图像偏好。这一洞察揭示了一条新路径——将图像偏好对齐分解为两个显式的文本偏好对齐过程，从而在双模态（文本+图像）上实现联合优化。在此基础上，对编辑区域施加掩码引导可以进一步增强细粒度对齐能力，使模型在训练时将注意力集中于组合变化的关键区域。

本文的核心动机正是填补上述缺口：通过双模态联合直接偏好优化（BIDPO）与区域感知的掩码引导损失，在无需人工标注偏好数据的前提下，系统性地提升扩散模型的组合式生成能力。



## 核心方法与创新机理

本工作围绕组合式文本到图像生成中的偏好对齐问题，提出了两个关键创新点——**双模态直接偏好优化（BIDPO）**与**区域感知引导机制**，二者协同解决了现有方法仅关注图像级偏好、忽略文本模态对齐与关键区域聚焦的根本瓶颈。

### 创新一：双模态直接偏好优化（BIDPO）

现有偏好优化方法（如 **Diffusion DPO**，Wallace et al., CVPR 2024）仅在图像层面建立偏好对比——给定一对偏好图像与较差图像，模型学习增强偏好图像的扩散过程、抑制较差图像的扩散过程。然而，这种单模态范式忽略了文本描述与图像内容之间的精细对齐关系，导致模型在复杂组合式提示下仍难以准确绑定属性与对象。

BIDPO 的核心洞察在于：**图像到图像的偏好对比学习可以通过组合两个文本到文本的偏好对比学习过程隐式实现**。具体而言，BIDPO 将原始的 Diffusion DPO 损失扩展为双模态形式，其构建块是 **TextDPO** 损失（公式见 Section 3.2 Equation (2)）：

$$ \mathcal{L}_{\mathrm{TextDPO}}(\theta) = -\mathbb{E}_{(\mathbf{x}_0^w,\mathbf{y}^w,\mathbf{y}^l)\sim\mathcal{D}, t\sim\mathcal{U}(0,T), \mathbf{x}_t^w\sim q(\mathbf{x}_t^w|\mathbf{x}_0^w)} \log\sigma\left(-\beta T\omega(\lambda_t)\right)\left(\|\epsilon^w-\epsilon_\theta(\mathbf{x}_t^w,t,c^w)\|_2^2 - \|\epsilon^w-\epsilon_{\mathrm{ref}}(\mathbf{x}_t^w,t,c^w)\|_2^2 - (\|\epsilon^l-\epsilon_\theta(\mathbf{x}_t^w,t,c^l)\|_2^2 - \|\epsilon^l-\epsilon_{\mathrm{ref}}(\mathbf{x}_t^w,t,c^l)\|_2^2)\right) $$

TextDPO 的关键设计在于：保持图像为偏好图像 $\mathbf{x}_0^w$，将“较差样本”替换为同一图像搭配较差描述 $\mathbf{y}^l$。模型由此学习对同一图像，偏好正确描述 $c^w$ 而非错误描述 $c^l$——这建立了文本模态的偏好对齐。

BIDPO 通过组合两个对称的 TextDPO 过程隐式实现图像偏好对齐：对两个图像-描述对互换文本条件，同时实现文本偏好和图像偏好的联合优化。这种设计的优雅之处在于，无需显式构建图像偏好对，而是通过文本偏好的双向对比隐式地传递图像级偏好信号（Figure 2a）。

### 创新二：区域感知引导机制

全局损失函数对所有像素等权重处理，导致模型在复杂场景中对关键编辑区域缺乏针对性关注。BIDPO 进一步引入区域感知引导，通过元素乘积的方式将训练聚焦于合成变化相关的关键区域：

$$ \mathcal{L}_{\mathrm{BIDPO-region}}(\theta) = \mathcal{L}_{\mathrm{BIDPO}}(\theta) \odot M $$

其中 $M$ 是基于编辑对象边界框生成的区域掩码。对编辑区域赋予权重 1.0、外部区域赋予权重 0.5（Section 4.1），使模型在训练时对关键区域施加更高的优化强度。掩码的边界框信息来源于数据构建流水线中的目标检测与分割模型（Grounding DINO、SAM2），实现了自动化的区域标注。

### 创新三：自动化偏好数据构建流水线（BICOMP）

支撑上述方法创新的是一项工程性贡献——**BICOMP 数据集**的自动构建流水线（Figure 3）。该流水线包含五个阶段：提示收集 → 图像生成 → 描述生成 → 描述编辑与图像编辑 → VQA 过滤。最终构建的数据集包含 57,474 张原始图像和 94,502 张编辑图像，覆盖属性绑定、空间关系、对象组合等 6 个组合性维度（Table 1）。训练时联合 VisMin 数据集（12k），共计 53k 样本。

### 创新点之间的协同关系

上述三个创新形成递进式协同：BICOMP 数据集提供了包含区域标注的高质量偏好数据，BIDPO 利用该数据实现双模态偏好对齐，区域感知引导则进一步利用边界框标注将优化聚焦于编辑区域。消融实验（Table 8）表明，区域级引导在 BIDPO 基础上额外带来 1.2%（T2I-CompBench）和 1.4%（GenEval）的提升，验证了各创新点的独立贡献与协同增益。

### 与基线方法的差异总结

| 设计维度 | Diffusion DPO（基线） | BIDPO（本工作） |
|---------|---------------------|----------------|
| 偏好优化模态 | 仅图像级偏好对比 | 双模态（文本+图像）联合偏好对比 |
| 区域引导 | 全局等权重损失 | 基于边界框的区域掩码引导 |
| 数据依赖 | 现有公开数据集 | 自构建 BICOMP 大规模偏好数据集 |
| 训练方式 | 全参数或 LoRA 微调 | LoRA（rank=8）高效微调，200步收敛 |



BiDPO 的整体框架围绕一个核心洞察构建：**图像到图像的偏好对比学习可以通过组合两个文本到文本的偏好对比学习过程隐式实现**。基于此，框架将双模态（文本+图像）联合偏好对齐与区域感知引导统一为端到端的训练流程。

### 框架总览

如图 2 所示，BiDPO 框架由三个关键模块串联而成：

1. **TextDPO（文本级直接偏好优化）**：框架的基础构建块。给定一张偏好图像 $\mathbf{x}_0^w$，TextDPO 对比其正确描述 $\mathbf{y}^w$ 与较差描述 $\mathbf{y}^l$ 下的扩散去噪误差，使模型学习对同一图像偏好正确文本条件。其损失函数为：

   $$\mathcal{L}_{\mathrm{TextDPO}}(\theta) = -\mathbb{E}_{(\mathbf{x}_0^w,\mathbf{y}^w,\mathbf{y}^l)\sim\mathcal{D}, t\sim\mathcal{U}(0,T), \mathbf{x}_t^w\sim q(\mathbf{x}_t^w|\mathbf{x}_0^w)} \log\sigma\left(-\beta T\omega(\lambda_t)\right)\left(\|\epsilon^w-\epsilon_\theta(\mathbf{x}_t^w,t,c^w)\|_2^2 - \|\epsilon^w-\epsilon_{\mathrm{ref}}(\mathbf{x}_t^w,t,c^w)\|_2^2 - (\|\epsilon^l-\epsilon_\theta(\mathbf{x}_t^w,t,c^l)\|_2^2 - \|\epsilon^l-\epsilon_{\mathrm{ref}}(\mathbf{x}_t^w,t,c^l)\|_2^2)\right)$$

   其中 $c^w$、$c^l$ 分别为偏好描述和较差描述的文本嵌入条件，$\epsilon_{\mathrm{ref}}$ 为冻结的参考模型。

2. **BiDPO（双模态 DPO 组装）**：将两个对称的 TextDPO 过程组合，隐式建立图像级别的偏好对比。具体而言，对两个图像-描述对 $(\mathbf{x}_0^w, \mathbf{y}^w)$ 和 $(\mathbf{x}_0^l, \mathbf{y}^l)$，交换文本条件——即 $\mathbf{x}_0^w$ 同时与 $\mathbf{y}^w$ 和 $\mathbf{y}^l$ 配对，$\mathbf{x}_0^l$ 同时与 $\mathbf{y}^l$ 和 $\mathbf{y}^w$ 配对。这样，两个 TextDPO 损失的联合优化同时实现了文本偏好对齐（同一图像下正确描述优于错误描述）和图像偏好对齐（通过图文配对关系的交换隐式建立图像间偏好）。

3. **区域感知引导掩码**：在 BiDPO 损失上施加元素乘积（$\odot$）的区域掩码 $M$，得到最终训练损失：

   $$\mathcal{L}_{\mathrm{BiDPO-region}}(\theta) = \mathcal{L}_{\mathrm{BiDPO}}(\theta) \odot M$$

   掩码 $M$ 根据编辑对象的边界框生成：对编辑区域赋权重 1.0，对外部区域赋权重 0.5。这使得训练聚焦于组合变化相关的关键区域，进一步增强细粒度对齐能力。

### 数据流与输入输出

框架的完整数据流为：

- **输入**：偏好数据三元组 $(\mathbf{x}_0^w, \mathbf{y}^w, \mathbf{y}^l)$，其中 $\mathbf{x}_0^w$ 为偏好图像，$\mathbf{y}^w$ 为正确描述，$\mathbf{y}^l$ 为错误/较差描述；同时需要编辑对象的边界框标注以生成区域掩码 $M$。
- **处理**：对偏好图像和较差图像分别进行前向扩散加噪，在各自的时间步 $t$ 上通过两个 TextDPO 过程计算去噪误差，组合为 BiDPO 损失后与区域掩码 $M$ 逐元素相乘。
- **输出**：优化后的模型参数 $\theta$，使模型在推理时能够更好地遵循组合式文本提示，尤其在属性绑定和空间关系等细粒度组合任务上表现显著提升。

### 训练策略

BiDPO 采用 LoRA（rank=8）在基座扩散模型（SDXL 或 SD3-Medium）上进行高效微调，训练 200 步，有效 batch size 为 2048，学习率设置为 $2048 \times 4\times10^{-8}$，在 4 张 H100 GPU 上约需 13 小时。训练数据混合了自动构建的 BICOMP 数据集（42k 样本）和 VisMin 数据集（12k 样本），共计 53k 样本。

### 补充图表

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed BIDPO. (a) BIDPO integrates bimodal(image and text) preference alignment; (b) Diffusion process and loss calculation with region-level guidance*



BIDPO 框架的核心由三个关键模块构成：**TextDPO 损失**、**双模态 DPO 组装机制** 和 **区域感知引导掩码**。以下逐一展开。

### 3.1 基座：Diffusion DPO 回顾

BIDPO 建立在 **Diffusion DPO**（Wallace et al., CVPR 2024）之上。给定偏好图像对 $(\mathbf{x}_0^w, \mathbf{x}_0^l)$，其中 $\mathbf{x}_0^w$ 为偏好图像、$\mathbf{x}_0^l$ 为较差图像，Diffusion DPO 通过对比模型 $\epsilon_\theta$ 与参考模型 $\epsilon_{\text{ref}}$ 的去噪误差差值来优化：

$$\mathcal{L}(\theta) = -\mathbb{E}_{(\mathbf{x}_0^w,\mathbf{x}_0^l)\sim\mathcal{D}, t\sim\mathcal{U}(0,T), \mathbf{x}_t^w\sim q(\mathbf{x}_t^w|\mathbf{x}_0^w), \mathbf{x}_t^l\sim q(\mathbf{x}_t^l|\mathbf{x}_0^l)} \log\sigma\left(-\beta T\omega(\lambda_t)\right)\big(\|\epsilon^w-\epsilon_\theta(\mathbf{x}_t^w,t)\|_2^2 - \|\epsilon^w-\epsilon_{\text{ref}}(\mathbf{x}_t^w,t)\|_2^2 - (\|\epsilon^l-\epsilon_\theta(\mathbf{x}_t^l,t)\|_2^2 - \|\epsilon^l-\epsilon_{\text{ref}}(\mathbf{x}_t^l,t)\|_2^2)\big)$$

其中 $\beta$ 为缩放因子，$\omega(\lambda_t)$ 为噪声水平加权函数。该损失的核心作用是**增强偏好样本的扩散过程、抑制较差样本的扩散过程**。然而，Diffusion DPO 仅考虑图像级偏好，忽略了文本模态的对齐。

### 3.2 TextDPO：文本级偏好对比

BIDPO 的核心构建块是 **TextDPO**。其关键创新在于：保持图像固定为偏好图像 $\mathbf{x}_0^w$，将“较差样本”替换为同一图像搭配较差描述 $\mathbf{y}^l$，从而将偏好对比从图像空间转移到文本空间：

$$\mathcal{L}_{\mathrm{TextDPO}}(\theta) = -\mathbb{E}_{(\mathbf{x}_0^w,\mathbf{y}^w,\mathbf{y}^l)\sim\mathcal{D}, t\sim\mathcal{U}(0,T), \mathbf{x}_t^w\sim q(\mathbf{x}_t^w|\mathbf{x}_0^w)} \log\sigma\left(-\beta T\omega(\lambda_t)\right)\left(\|\epsilon^w-\epsilon_\theta(\mathbf{x}_t^w,t,c^w)\|_2^2 - \|\epsilon^w-\epsilon_{\text{ref}}(\mathbf{x}_t^w,t,c^w)\|_2^2 - (\|\epsilon^l-\epsilon_\theta(\mathbf{x}_t^w,t,c^l)\|_2^2 - \|\epsilon^l-\epsilon_{\text{ref}}(\mathbf{x}_t^w,t,c^l)\|_2^2)\right)$$

其中 $c^w$ 和 $c^l$ 分别表示偏好描述与较差描述的文本条件嵌入。**模型学习对同一图像偏好正确描述而非错误描述**，从而在文本模态上建立细粒度对齐。

### 3.3 BIDPO：双模态偏好组装的隐式图像对齐

BIDPO 的核心洞察是：**图像到图像的偏好对比学习可以通过组合两个文本到文本的偏好对比过程隐式实现**。具体而言，给定两组图文对 $(\mathbf{x}_0^w, \mathbf{y}^w)$ 和 $(\mathbf{x}_0^l, \mathbf{y}^l)$，BIDPO 构造两个对称的 TextDPO 过程：

- **过程一**：固定 $\mathbf{x}_0^w$，对比 $\mathbf{y}^w$（正）与 $\mathbf{y}^l$（负）
- **过程二**：固定 $\mathbf{x}_0^l$，对比 $\mathbf{y}^l$（正）与 $\mathbf{y}^w$（负）

通过交换图文配对关系，BIDPO 在不显式建模图像对比损失的情况下，隐式建立了图像级别的偏好对齐（见 Figure 2a）。这种双模态联合优化使模型同时学习“正确图像配正确描述”和“较差图像配错误描述”的对应关系。

### 3.4 区域感知引导掩码

为增强对合成变化关键区域的关注，BIDPO 引入**区域感知引导掩码** $M$，在损失上施加元素乘积：

$$\mathcal{L}_{\mathrm{BIDPO-region}}(\theta) = \mathcal{L}_{\mathrm{BIDPO}}(\theta) \odot M$$

掩码 $M$ 根据编辑对象的边界框生成（边界框由数据构建流水线中的 Grounding DINO 和 SAM2 提取）。对编辑区域赋权重 $1.0$，外部区域赋权重 $0.5$（Section 4.1），使训练聚焦于被编辑的关键区域。消融实验表明，区域引导在 BIDPO 基础上进一步带来 **1.2%（T2I-CompBench）和 1.4%（GenEval）** 的提升（Section 4.3）。

### 3.5 模块间的因果机制

三个模块形成清晰的因果链：**TextDPO 提供文本级偏好信号 → BIDPO 组装双模态隐式对齐 → 区域掩码聚焦关键区域**。这种设计将复杂的图文联合偏好对齐问题分解为两个可控的文本偏好对比过程，并通过区域加权实现细粒度引导，构成了 BIDPO 超越 Diffusion DPO 的理论基础。

### 补充图表

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of post-training optimization methods used in compositional text-to-image generation. Our proposed BIDPO, achieves full human preference alignment across both image and text modalities while offering region-level guidance, outperforming existing approaches such as SFT, DiffusionDPO*



## 实验与关键发现

### 主实验结果

BiDPO在多个组合式文本到图像生成的权威基准上均展现出显著且一致的性能提升，核心增益集中在属性绑定和空间关系等组合性维度。

**T2I-CompBench属性绑定。** 在T2I-CompBench的属性绑定类别中，SDXL-BiDPO相比SDXL基线实现了跨越式提升：Color从58.90升至79.35（+20.45），Shape从43.98升至61.35（+17.37），Texture从50.76升至68.79（+18.03）（Table 2）。三者的平均提升幅度约为17%，验证了双模态偏好对齐对精细属性绑定的关键作用。该基准还覆盖空间关系和非空间关系等子维度，BiDPO在这些维度上同样保持优势。

**GenEval综合得分。** 在GenEval上，SDXL-BiDPO将整体得分从基线的0.53提升至0.62（+0.09），超越了多个对比方法（Table 3）。GenEval涵盖对象存在性、属性绑定、空间关系等多个子任务，BiDPO在多项子指标上的同步改善表明方法对组合生成的全局能力有系统性增强。

**DPG-Bench整体得分。** 在DPG-Bench上，SDXL-BiDPO的整体得分从73.38提升至78.84（+5.46）（Table 4）。该基准侧重于密集提示下的组合生成质量，BiDPO的提升说明方法对复杂多约束场景同样有效。

**基准漂移鲁棒性（GenEval 2）。** 在GenEval 2上，SDXL-BiDPO在Soft-TIFA-AM上提升6.6（50.1→56.7），在Soft-TIFA-GM上提升1.8（9.1→10.9）（Table 5）。GenEval 2作为新基准引入了基准漂移的考量，BiDPO的稳定提升表明其泛化能力不局限于特定评估协议。

**跨架构迁移性。** 在MMDiT架构的SD3-Medium上应用BiDPO后，模型在GenEval 2的组合性评估中超越了Flux（Table 6），尤其在多对象场景（objects 3-10）中优势明显。这验证了BiDPO的模型无关性——双模态偏好对齐机制不依赖于特定的扩散模型架构。

**视觉质量不妥协。** 在DrawBench上使用HPSv2评估视觉美学质量，SDXL-BiDPO的平均得分从30.22提升至32.87（+2.65%）（Table 7）。这表明BiDPO在增强组合性的同时并未损害图像的视觉质量，反而带来轻微提升。

### 消融实验

Table 8的消融实验系统验证了BiDPO各关键设计的独立贡献。

**双模态DPO vs. 单模态DPO。** 仅使用TextDPO（单模态文本偏好对齐）相比Diffusion DPO基线已有提升，但BiDPO（双模态组装）带来了更大幅度的改进。这直接验证了核心洞察：图像到图像的偏好对比学习可以通过组合两个文本到文本的偏好对比过程隐式实现，仅进行单侧文本对齐不足以充分捕获图像模态的偏好信号。

**区域级引导的增量贡献。** 在BiDPO基础上加入区域感知掩码引导后，T2I-CompBench整体得分从53.17进一步提升至54.37（+1.2%），GenEval从60.74提升至62.14（+1.4%），DPG-Bench从77.60提升至78.84（+1.24%）。这一增量虽然幅度不大，但在多个基准上方向一致，表明对编辑区域施加更高训练权重能够增强细粒度对齐能力。掩码权重设置为：感兴趣区域权重1.0，外部区域权重0.5。

**数据混合的作用。** 消融实验还考察了BICOMP与VisMin数据集的混合效果。BICOMP提供42k样本，VisMin提供12k样本，共计53k训练样本。数据混合对鲁棒性和真实性有积极贡献，VisMin的引入可能补充了BICOMP自动构建过程中覆盖不足的场景多样性。

### 失败模式与局限性

尽管BiDPO在整体指标上表现优异，论文中隐含和明确指出了若干失败模式与局限：

**区域掩码精度依赖外部模型。** 区域引导掩码的生成依赖于Grounding DINO和SAM2等目标检测与分割模型的精度。对于多对象密集场景或遮挡严重的情况，边界框和掩码的质量可能下降，导致区域引导权重分配失准，从而引入训练噪声。

**自动数据构建的标注偏差风险。** BICOMP数据集的构建流水线涉及多个外部模型（DeepSeek-V3用于提示收集、Qwen2.5-VL-72B-Instruct用于VQA过滤、Qwen-Image-Edit用于图像编辑），虽然规模可观（57,474原始图像+94,502编辑图像），但自动构建方式可能引入各模型自身的系统性偏差，偏好数据的质量上限受限于这些模型的性能天花板。

**架构覆盖范围有限。** 当前验证仅覆盖UNet类扩散模型（SDXL）和MMDiT架构（SD3-Medium），尚未在自回归图像生成模型上测试。BiDPO的双模态偏好对齐框架在自回归范式下的适配性和有效性仍是开放问题。

**公平性评估缺失。** 论文未讨论模型在人口统计属性或社会偏见方面的公平性表现，所有评估聚焦于组合生成准确性和视觉质量指标。在实际部署中，偏好对齐训练可能放大或引入新的社会偏见，这一点需要额外验证。

### 实验设置关键参数

训练使用LoRA（rank=8）在SDXL和SD3-Medium上进行高效微调，共训练200步，有效batch size为2048，学习率设置为2048×4e-8，在4×H100 GPU上约需13小时完成训练。区域引导掩码中，感兴趣区域权重设为1.0，外部区域权重设为0.5。

### 补充图表

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/005_Table_2.jpg]]
*Table 2: Main Results on T2I-CompBench [18]*

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/006_Table_3.jpg]]
*Table 3: Main Results on GenEval [12]*

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/007_Table_4.jpg]]
*Table 4: Main Results on DPG-Bench [17]*

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/008_Table_5.jpg]]
*Table 5: Main Results on GenEval 2 [20]*

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/009_Table_6.jpg]]
*Table 6: Main Results on GenEval 2 (compositionality) [20]*

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/010_Table_7.jpg]]
*Table 7: Visual aesthetic quality evaluation using HPSv2 [45]*

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/011_Table_8.jpg]]
*Table 8: Ablation on key designs. We report the overall scores over each benchmark*

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/004_Table_1.jpg]]
*Table 1: Number of images in each dimension. Each original image may correspond to multiple edited images*

![[assets/figures/papers/paper_list_l2189_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Compositional_Text/figures/003_Figure_3.jpg]]
*Figure 3: The data construction pipeline of our BICOMP dataset. Our BICOMP dataset, though generated automatically, contains large amounts of high-quality image-caption pairs with region annotations across multiple composition-related dimensions*



## 定位与知识库关联

### 1. 与基线方法的关系

**BIDPO** 的起点是 **Diffusion DPO**（Wallace et al., CVPR 2024），后者首次将直接偏好优化引入扩散模型的后训练阶段。Diffusion DPO 的核心机制是对偏好图像对 $(x_0^w, x_0^l)$ 进行对比学习——通过比较模型与参考模型在去噪误差上的差异，隐式地增强偏好样本的扩散过程、抑制较差样本的扩散过程（公式见 Section 3.1, Equation 1）。然而，这一框架存在两个结构性局限：（1）偏好对比仅发生在图像模态，文本条件 $c$ 在偏好对中保持固定，模型无法学习文本描述质量与图像生成质量之间的精细对齐；（2）损失函数对图像所有空间区域施加等权重，无法针对组合式生成中真正关键的编辑区域进行聚焦训练。

BIDPO 对 Diffusion DPO 的改造体现在两个维度：

- **模态扩展**：将单一图像级偏好对比分解为两个对称的 TextDPO 过程。TextDPO 保持偏好图像 $x_0^w$ 不变，将较差样本替换为同一图像搭配较差描述 $y^l$，迫使模型学习“对同一图像，偏好正确描述 $c^w$ 而非错误描述 $c^l$”。通过交换两个图像-描述对的文本条件并组合两个 TextDPO 损失，BIDPO 隐式地实现了图像到图像的偏好对比学习（Section 3.2, Figure 2a）。这一设计的核心洞察在于：**图像偏好可以通过文本偏好的组合间接建立**。

- **空间聚焦**：引入基于编辑对象边界框的区域掩码 $M$，在 BIDPO 损失上施加元素乘积 $\mathcal{L}_{\mathrm{BIDPO-region}} = \mathcal{L}_{\mathrm{BIDPO}} \odot M$（Equation 3）。掩码对编辑区域赋予权重 1.0、外部区域赋予权重 0.5，使训练梯度集中于组合变化相关的关键区域（Section 4.1, Figure 2b）。

在基座模型层面，BIDPO 以 **SDXL**（Podell et al., arXiv 2023）为主要验证平台，同时扩展到 **SD3-Medium**（Esser et al., ICML 2024）以验证跨架构（MMDiT）的泛化性。与 **Flux**（Black Forest Labs, 2024）的对比表明，经 BIDPO 微调的 SD3-Medium 在 GenEval 2 的组合性指标上可超越 Flux（Table 6），这验证了方法的模型无关性。

### 2. 适用边界

BIDPO 的适用边界由以下条件界定：

- **模型架构**：当前仅在扩散模型（SDXL 的 UNet 架构和 SD3-Medium 的 MMDiT 架构）上验证，尚未在自回归图像生成模型上测试。论文在开放问题中明确提及此扩展方向，但无实验支撑。
- **训练数据**：依赖自动构建的 BICOMP 数据集（57,474 原始图像 + 94,502 编辑图像，覆盖 6 个组合维度）与 VisMin 数据集（12k）的混合，共计 53k 样本（Section 4.1）。数据构建流水线涉及 DeepSeek-V3、DeepSeek-R1、Grounding DINO、SAM2、Qwen2.5-VL-72B-Instruct、Qwen-Image-Edit 等多个外部模型（Section 3.3, Figure 3），流水线复杂度较高，且自动构建方式可能引入标注偏差。
- **区域引导质量**：区域掩码 $M$ 的生成依赖于目标检测（Grounding DINO）和分割模型（SAM2）的精度。对于多对象复杂场景，边界框检测和分割的误差可能引入噪声，使掩码无法精确覆盖所有编辑相关区域。
- **偏好数据类型**：BIDPO 的训练数据为自动构建的合成偏好对，而非真实人工标注的偏好数据。在更大规模的真实人工标注偏好数据上训练是否仍有显著增益，目前为开放问题。

### 3. 局限与开放问题

**已识别的局限**：

1. **架构覆盖有限**：仅验证了扩散模型，未涉及自回归生成模型。
2. **数据流水线依赖链长**：BICOMP 的构建依赖多个外部模型，任一环节的质量波动可能影响最终偏好数据的质量。
3. **掩码粒度粗糙**：当前区域引导采用离散权重（1.0 / 0.5）的二值化掩码，而非像素级连续注意力权重，可能无法充分捕捉编辑区域的渐变重要性。
4. **公平性评估缺失**：论文未讨论模型在人口统计属性或社会偏见方面的公平性评估，评估集中于组合生成准确性和视觉质量指标。

**开放问题**：

1. BIDPO 的双模态偏好对齐框架是否可以推广到视频生成或 3D 生成等其他生成任务？
2. 区域引导掩码是否可以进一步细化为像素级注意力权重，实现更精细的空间聚焦？
3. BIDPO 训练过程中，文本偏好与图像偏好是否存在冲突？如何量化两者的对齐程度？（论文未提供两者一致性的定量分析）
4. 在更大规模的真实人工标注偏好数据上训练，BIDPO 是否仍有显著增益？合成偏好与人类偏好的分布差异对最终效果的影响尚未量化。
5. 区域引导掩码的权重分配（1.0 vs 0.5）是否最优？是否存在更有效的权重策略（如基于编辑强度的自适应权重）？



## 原文 PDF

![[paperPDFs/CVPR_2026/Compositional_Text_to_Image_Generation_Via_Region_aware_Bimodal_Direct_Preference_Optimization.pdf]]
