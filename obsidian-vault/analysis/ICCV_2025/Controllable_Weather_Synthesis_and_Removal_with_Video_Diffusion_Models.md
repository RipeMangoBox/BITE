---
title: "Controllable Weather Synthesis and Removal with Video Diffusion Models"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Controllable_Weather_Synthesis_and_Removal_with_Video_Diffusion_Models.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/WeatherWeaver/
aliases:
- CWSRVDM
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "将天气效果分解为六个独立分量（云、雾、雨、雪、水洼、雪覆盖），并通过连续强度向量（s∈R^6）进行参数化控制。"
primary_logic: "将天气模拟任务拆分为“天气去除”和“天气合成”两个互补的视频扩散模型，并采用三阶段数据策略（模拟渲染、生成模型扩增、自动标注真实视频）来克服配对数据稀缺问题，从而实现逼真且可控的视频天气编辑。"
claims:
- "流水线拆分为双模型设计（Weather Removal 和 Weather Synthesis）并结合多源数据策略，使得在真实世界视频上训练可控的天气扩散模型成为可能。"
- "在用户研究中，对于雾天合成任务，人类评估者在85%的样本中偏好我们的方法优于AnyV2V，VLM评估者偏好率为80%，显著优于基线。"
- "User Study - Weather Synthesis (Fog) 上 Preference over AnyV2V (Human) = 85%"
- "User Study - Weather Synthesis (Fog) 上 Preference over AnyV2V (VLM) = 80%"
---

# Controllable Weather Synthesis and Removal with Video Diffusion Models

> [!tip] 核心洞察
> 将天气模拟任务拆分为“天气去除”和“天气合成”两个互补的视频扩散模型，并采用三阶段数据策略（模拟渲染、生成模型扩增、自动标注真实视频）来克服配对数据稀缺问题，从而实现逼真且可控的视频天气编辑。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 可控天气合成与去除的视频扩散模型 |
| 英文题名 | Controllable Weather Synthesis and Removal with Video Diffusion Models |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2505.00704); [Project](https://research.nvidia.com/labs/toronto-ai/WeatherWeaver/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | WEATHERWEAVER |
| Dataset | User Study - Weather Synthesis (Fog) |

> [!tip] 效果简介
> - User Study - Weather Synthesis (Fog) 上，Preference over AnyV2V (Human) 为 85%，对比 15% (AnyV2V)，变化 +70pp。
> - User Study - Weather Synthesis (Fog) 上，Preference over AnyV2V (VLM) 为 80%，对比 20% (AnyV2V)，变化 +60pp。

## 概述

### 问题瓶颈

真实世界中，同一场景在不同天气条件下的高质量成对视频数据极度稀缺。这一数据瓶颈导致现有方法难以同时实现**逼真的瞬态天气效果**（如雨滴溅落、雪花飘动）和**精确的可控性**：基于物理的3D模拟方法（如ClimateNeRF）虽可控但真实感不足，而通用视频编辑模型（如AnyV2V、TokenFlow、FRESCO）缺乏对天气强度的显式控制机制。

### 核心思路

WEATHERWEAVER 提出了一种**任务分解+多源数据**的解决方案：

1. **双模型流水线**：将天气模拟拆分为两个互补的视频扩散模型——**天气去除模型**（Weather Removal Model）将真实视频转换为“晴空基准”视频，**天气合成模型**（Weather Synthesis Model）则在晴空视频上添加指定的天气效果。两者可独立使用，也可串联实现天气编辑。

2. **六维连续控制**：将天气效果分解为六个独立分量——云、雾、雨、雪、水洼、雪覆盖，通过连续强度向量 $\mathbf{s} = (s_{\mathrm{cloud}}, s_{\mathrm{fog}}, s_{\mathrm{rain}}, s_{\mathrm{snow}}, s_{\mathrm{puddle}}, s_{\mathrm{snow.coverage}}) \in \mathbb{R}^6$ 进行参数化控制，支持精细调节和多种天气的组合。

3. **三阶段数据策略**：为克服配对数据稀缺，构建了三种互补数据源——**模拟渲染**（Unreal Engine，20.8k视频对，提供精确可控标注）、**生成模型扩增**（SDXL + Prompt-to-Prompt，1,147k高质量图像对，增强场景多样性）、**自动标注真实视频**（天气去除模型 + VLM，4.6k视频对，提升真实感）。

### 方法定位

WEATHERWEAVER 基于 Stable Video Diffusion 构建，属于**可控视频扩散模型**在天气编辑领域的应用。与通用视频编辑基线（AnyV2V、TokenFlow、FRESCO）相比，其核心差异在于引入了显式的六维天气强度控制；与专用天气去除方法（HistoFormer、TransWeather、WeatherDiffusion）相比，其优势在于同时支持去除与合成，并保持时间一致性。

### 主要结果

- **天气合成**：在用户研究中，对于雾天合成任务，人类评估者在 **85%** 的样本中偏好 WEATHERWEAVER 优于 AnyV2V（VLM评估者偏好率为 **80%**），显著超越基线。
- **可控性验证**：通过调节六维强度向量，可实现从薄雾到浓雾、从小雨到暴雨的连续平滑过渡（Figure 6），并支持多天气效果的时序组合编辑（Figure 7）。
- **消融发现**：视频模型架构（相对于图像模型变体）显著改善了瞬态效应的生成质量和时间一致性；联合使用全部三种数据源训练可获得最佳的视觉效果和可控性（Figure 8）。
- **下游应用**：天气去除可显著提升感知模型（如 Grounded SAM）在恶劣天气下的检测精度（Figure 10）。

### 局限与开放问题

方法受限于 Stable Video Diffusion 的 VAE 8倍空间压缩，导致高频细节（如人脸）有时丢失；训练数据中夜间视频有限，夜间天气模拟质量下降。开放问题包括：如何更好地保留精细纹理、如何提升夜间场景鲁棒性、以及如何将方法扩展到更长视频。

## 背景与动机

### 问题背景

真实世界视频中的天气效果——雾、雨、雪、云层变化——是视觉感知与内容创作中的核心挑战。从自动驾驶感知系统在恶劣天气下的失效，到影视后期对场景氛围的精确控制，天气模拟与去除的需求广泛存在。然而，这一任务的本质困难在于：**天气效果是瞬态的（雨滴的轨迹、雪花的飘落）、空间变化的（雾的密度随深度衰减）、且与场景内容深度耦合**（光照变化、水面反射、积雪覆盖）。任何单一维度的简化都难以同时满足逼真度与可控性的要求。

### 现有方法的缺口

现有方法在天气编辑上存在三个结构性瓶颈：

1.  **数据稀缺的根本制约**。理想情况下，训练一个天气转换模型需要成对的视频数据——同一场景在“晴空”与“雨天/雪天/雾天”下的精确对应。这类数据在真实世界中几乎不可能大规模获取。现有方法要么依赖有限的手工收集数据，要么完全在仿真引擎中训练，导致模型在真实场景上的泛化能力严重受限。

2.  **可控性的缺失**。大多数视频编辑方法（如 AnyV2V、TokenFlow、FRESCO）通过文本提示或类别标签控制编辑效果，缺乏对天气强度、类型组合的精细调节能力。用户无法指定“中等密度的雾 + 轻微雨滴”这样的复合效果，也无法在时间维度上动态调整天气变化。

3.  **合成与去除的割裂**。传统方法通常将天气合成和天气去除视为两个独立任务，分别训练专用模型（如 HistoFormer、TransWeather 用于去除；AnyV2V 用于合成）。这种割裂导致两个方向的模型无法共享场景理解，也无法组合使用以实现“编辑现有天气”的完整流程。

### 本文动机

针对上述瓶颈，本文提出 **WEATHERWEAVER**，一个基于视频扩散模型的可控天气编辑框架。其核心动机在于：**通过将天气效果参数化分解、将任务拆分为互补的双模型流水线、并设计多源数据策略，在真实世界视频上实现逼真、可控、时序一致的天气合成与去除**。

具体而言，本文的出发点是三个关键决策：

-   **将天气效果分解为六个独立分量**（云、雾、雨、雪、水洼、雪覆盖），并通过连续强度向量 $\mathbf{s} \in \mathbb{R}^6$ 进行参数化控制。这使得用户可以精确调节每种天气效应的强度，并自由组合多种效果。

-   **将流水线拆分为两个互补的视频扩散模型**：一个天气去除模型，将真实世界视频转换为“晴空”规范视频；一个天气合成模型，在晴空视频上添加指定天气效果。两个模型可以独立使用，也可以串联完成“编辑现有天气”的任务。

-   **采用三阶段数据策略**克服配对数据稀缺问题：仿真渲染提供精确可控的配对数据；生成模型扩增提供多样化的图像级配对数据；自动标注真实视频（用天气去除模型生成伪晴空标签，再用 VLM 估计天气强度）提供真实世界的分布覆盖。三者联合训练，使得模型在真实场景上同时具备逼真度和可控性。

这一设计使得 WEATHERWEAVER 在用户研究中显著优于现有基线——例如在雾天合成任务上，人类评估者在 85% 的样本中偏好本文方法优于 AnyV2V——同时保持了时间一致性和对多种天气效果的精细控制能力。

## 核心创新

WEATHERWEAVER 的核心创新并非单一技术的堆叠，而是围绕“真实世界可控天气视频编辑”这一瓶颈问题，在**任务分解范式**、**控制表示**和**数据策略**三个维度上对现有方法进行了系统性重构。

### 1. 双模型解耦范式：从“直接翻译”到“去除-合成”流水线

现有视频编辑方法（如 AnyV2V、TokenFlow、FRESCO）通常采用单一模型直接进行天气转换，这种方式难以同时保证天气效果的逼真度和对原始场景结构的忠实保留。WEATHERWEAVER 的关键洞察在于**将天气模拟拆分为两个互补的子任务**：

- **Weather Removal Model**：负责将任意真实天气视频翻译为“标准晴空视频”（canonical weather-free video）。该模型同时充当伪标签引擎，为后续真实数据的自动标注提供基础。
- **Weather Synthesis Model**：接收晴空视频和天气控制信号，生成具有指定天气效果的视频。

这种解耦设计的因果机制在于：去除模型学会了从真实天气中提取场景的晴空本质，而合成模型则专注于在干净的画布上添加可控的天气效果。两个模型可独立使用，也可串联完成“天气编辑”（先去除再合成），从而在真实世界视频上实现了端到端的可控天气转换。这一范式转变是方法能够有效利用非配对真实数据的前提。

### 2. 连续强度向量控制：从类别标签到六维参数空间

基线方法通常仅支持离散的天气类别标签或简单的文本提示，缺乏对天气效应强度的精细控制。WEATHERWEAVER 将天气效果**分解为六个独立分量**，并通过连续强度向量进行参数化：

$$\mathbf{s} = ( s_{\mathrm{cloud}}, s_{\mathrm{fog}}, s_{\mathrm{rain}}, s_{\mathrm{snow}}, s_{\mathrm{puddle}}, s_{\mathrm{snow.coverage}} ) \in \mathbb{R}^6$$

该向量被扩展为时空条件图 $\mathbf{S}$，与视频潜变量拼接后送入扩散模型。这一设计使得用户能够独立调节云量、雾浓度、降雨强度、降雪强度、水洼反射和积雪覆盖程度，甚至实现多种天气效果的时序组合（如雨转雪）。消融实验表明，排除模拟数据会显著削弱这种精确控制能力（Figure 8），证实了连续参数化与仿真数据之间的耦合关系。

### 3. 三源数据策略：突破配对数据瓶颈

真实世界中几乎不存在同一场景在不同天气条件下的高质量配对视频，这是制约天气编辑方法泛化能力的根本瓶颈。WEATHERWEAVER 提出了一种**三阶段数据组合策略**来克服这一限制：

- **模拟渲染数据**（Unreal Engine）：提供精确控制的配对视频（20.8k 视频对），确保天气效应的物理合理性和强度可控性。
- **生成模型扩增数据**（SDXL + Prompt-to-Prompt）：生成大规模配对图像（1,147k 对），提升场景和天气的多样性。
- **自动标注真实视频**：利用 Weather Removal Model 处理真实天气视频生成伪晴空标签，再通过 VLM 自动标注天气类型和强度，获得 4.6k 真实视频对。

Table 1 系统对比了三种数据源在可控性、时间一致性、真实感、场景多样性和轨迹多样性上的互补特性。消融实验证实，联合使用全部三种数据源才能获得最佳的视觉效果和可控性（Figure 8），而仅使用生成数据会导致瞬态效应（如雨滴、雪花）的质量下降。

### 4. 方法定位与局限性

WEATHERWEAVER 构建于 Stable Video Diffusion 之上，方法本身具有模型无关性，理论上可迁移至更强的视频扩散模型。当前的主要局限包括：基础 VAE 的 8 倍空间压缩导致人脸等高频细节丢失；训练数据中夜间视频稀缺，夜间场景的模拟质量受限；以及离线推理方式限制了对更长视频的扩展。这些局限本质上受限于基座模型的能力上限和数据覆盖范围，而非方法范式本身。

## 整体框架

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_00704/figures/002_Figure_2.jpg]]
*Figure 2: Model Overview. Our controllable weather simulation framework includes two complementary models for both weather removal and weather synthesis. These models can be used both independently and combined for weather editing tasks*

WEATHERWEAVER 将真实视频中的天气模拟形式化为一个视频到视频的翻译任务，其核心设计是把这一复杂问题拆分为两个互补且可控的视频扩散模型：**天气去除模型（Weather Removal Model）** 和 **天气合成模型（Weather Synthesis Model）**。前者负责将任意带天气效果的真实视频“净化”为晴空基准视频，后者则在该晴空视频上以精确可控的方式重新施加天气效果。两个模型既可独立使用，也可串联组合，实现完整的天气编辑流程（先去除再合成），如 Figure 2 所示。

整个流水线建立在预训练的 Stable Video Diffusion 之上，遵循模型无关的设计原则。其运作流程如下：

1. **输入与条件编码**：用户提供一段视频和一个六维天气强度向量 $\mathbf{s} = ( s_{\mathrm{cloud}}, s_{\mathrm{fog}}, s_{\mathrm{rain}}, s_{\mathrm{snow}}, s_{\mathrm{puddle}}, s_{\mathrm{snow.coverage}} ) \in \mathbb{R}^6$，分别控制云、雾、雨、雪、水洼、雪覆盖六种效果的连续强度。该向量被扩展为时空条件图 $\mathbf{S}$，与视频潜变量拼接后作为扩散模型的条件输入。

2. **天气去除模型**：接收带有天气效果的真实视频，在条件图 $\mathbf{S}$ 的引导下，通过去噪过程预测对应的晴空视频潜变量。训练目标为最小化预测晴空潜变量与真实晴空潜变量之间的 L2 距离：
   $$\mathcal{L}^{w \to c} = \| \mathbf{f}_{\theta}^{w \to c}(\mathbf{z}_{\tau}^{c}, \mathbf{z}_{0}^{w}, \mathbf{S}, \tau) - \mathbf{z}_{0}^{c} \|_{2}^{2}$$
   该模型同时充当伪标签引擎，为后续真实视频的自动标注提供“晴空”参考。

3. **天气合成模型**：接收晴空视频（可来自真实晴空视频、去除模型的输出或仿真数据）和天气强度向量，生成带有指定天气效果的视频。训练目标为最小化预测天气潜变量与真实天气潜变量之间的 L2 距离：
   $$\mathcal{L}^{c \to w} = \| \mathbf{f}_{\theta}^{c \to w}(\mathbf{z}_{\tau}^{w}; \mathbf{z}_{0}^{c}, \mathbf{S}, \tau) - \mathbf{z}_{0}^{w} \|_{2}^{2}$$

4. **天气编辑组合模式**：当需要将视频中的一种天气转换为另一种时，先将输入视频送入天气去除模型得到晴空视频，再将其与新的天气强度向量一起送入天气合成模型，生成目标天气效果（参见 Figure 7、Figure 9）。

**数据策略**是支撑这一双模型框架的关键。由于真实世界中不存在同一场景在不同天气下的高质量成对视频，WEATHERWEAVER 引入了三种互补的数据来源（见 Table 1 和 Figure 3）：
- **仿真数据**：利用 Unreal Engine 在四个大型户外场景中渲染六种天气效果，生成 20.8k 个视频对（每段 100 帧），提供精确可控的天气标注。
- **生成数据**：通过 SDXL 和 Prompt-to-Prompt 技术生成 1,147k 高质量成对图像（经前 4% 筛选），大幅扩展场景多样性。
- **真实视频自动标注**：从在线视频中采集 4.6k 个视频对，利用天气去除模型生成伪晴空标签，再通过 VLM 自动标注天气强度向量。

训练采用多阶段策略：天气去除模型先在仿真和生成数据上进行图像-视频联合训练；天气合成模型同样先在仿真和生成数据上训练，最后在所有三种数据源上联合微调，以兼顾可控性、真实感和场景多样性。

## 核心模块与公式推导

### 双模型流水线

WEATHERWEAVER 将天气模拟任务拆分为两个互补的视频扩散模型，形成“去除-合成”流水线：

- **Weather Removal Model**（$f_\theta^{w \to c}$）：输入带有天气效果的真实视频，生成对应的晴空（canonical）视频。该模型同时充当伪标签引擎，为真实视频自动标注晴空参考。
- **Weather Synthesis Model**（$f_\theta^{c \to w}$）：输入晴空视频和天气强度向量，合成带有指定天气效果的视频，支持精确控制天气类型与强度。

两个模型均基于 Stable Video Diffusion 初始化，在 VAE 潜空间中运行，模型架构本身是模型无关的（model-agnostic）。

### 天气强度参数化

天气效果被分解为六个独立分量，通过连续强度向量进行参数化控制：

$$\mathbf{s} = ( s_{\mathrm{cloud}},\; s_{\mathrm{fog}},\; s_{\mathrm{rain}},\; s_{\mathrm{snow}},\; s_{\mathrm{puddle}},\; s_{\mathrm{snow.coverage}} ) \in \mathbb{R}^6$$

其中各分量含义：
- $s_{\mathrm{cloud}}$：云层强度
- $s_{\mathrm{fog}}$：雾浓度
- $s_{\mathrm{rain}}$：降雨强度
- $s_{\mathrm{snow}}$：降雪强度
- $s_{\mathrm{puddle}}$：水洼/积水程度
- $s_{\mathrm{snow.coverage}}$：积雪覆盖程度

该向量被扩展为时空条件图 $\mathbf{S} = \mathbf{1} \otimes \mathbf{s} \in \mathbb{R}^{l \times h \times w \times 6}$，与视频潜变量拼接后作为扩散模型的条件输入。

### 扩散过程基础

采用标准视频扩散模型的前向过程，在时间步 $\tau$ 的含噪潜变量为原始潜变量与高斯噪声的加权和：

$$\mathbf{z}_{\tau} = \alpha_{\tau} \mathbf{z}_{0} + \sigma_{\tau} \mathbf{\epsilon}$$

其中 $\alpha_\tau$ 和 $\sigma_\tau$ 为噪声调度参数，$\mathbf{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$。

### 天气合成训练目标

天气合成模型 $f_\theta^{c \to w}$ 的训练目标是最小化预测潜变量与真实天气潜变量之间的 L2 距离：

$$\mathcal{L}^{c \to w} = \| \mathbf{f}_{\theta}^{c \to w}(\mathbf{z}_{\tau}^{w}; \mathbf{z}_{0}^{c}, \mathbf{S}, \tau) - \mathbf{z}_{0}^{w} \|_{2}^{2}$$

其中：
- $\mathbf{z}_{\tau}^{w}$：时间步 $\tau$ 的含噪天气潜变量
- $\mathbf{z}_{0}^{c}$：晴空视频的原始潜变量（作为条件）
- $\mathbf{S}$：天气强度条件图
- $\mathbf{z}_{0}^{w}$：真实天气视频的原始潜变量（预测目标）

### 天气去除训练目标

天气去除模型 $f_\theta^{w \to c}$ 的训练目标对称地定义为：

$$\mathcal{L}^{w \to c} = \| \mathbf{f}_{\theta}^{w \to c}(\mathbf{z}_{\tau}^{c}; \mathbf{z}_{0}^{w}, \mathbf{S}, \tau) - \mathbf{z}_{0}^{c} \|_{2}^{2}$$

其中：
- $\mathbf{z}_{\tau}^{c}$：时间步 $\tau$ 的含噪晴空潜变量
- $\mathbf{z}_{0}^{w}$：天气视频的原始潜变量（作为条件）
- $\mathbf{z}_{0}^{c}$：真实晴空视频的原始潜变量（预测目标）

两个模型均采用去噪得分匹配（denoising score matching）范式，从含噪潜变量和条件中直接预测原始潜变量，而非预测噪声。

### 数据策略模块

为克服配对数据稀缺问题，方法引入三源数据策略：

1. **仿真数据**：使用 Unreal Engine 在四个大型户外场景中渲染六种天气效果，生成 20.8k 视频对（每段 100 帧），提供精确的配对真值和可控性。
2. **生成数据**：利用 SDXL 和 Prompt-to-Prompt 技术生成 1,147k 高质量配对图像（经 top 4% 筛选），扩展场景多样性。
3. **真实视频自动标注**：先由 Weather Removal Model 生成伪晴空视频，再由 VLM 验证标注质量，最终获得 4.6k 视频对。

训练采用多阶段策略：Weather Removal Model 先在仿真和生成数据上以图像-视频联合训练方式学习，Weather Synthesis Model 随后在全部三种数据源上联合训练，以兼顾可控性、真实感和泛化能力。

## 实验与分析

### 瓶颈突破验证

本文的核心瓶颈在于真实世界中缺乏高质量、成对的相同场景在不同天气条件下的视频数据，导致现有方法难以同时实现逼真的瞬态天气效果和精确的可控性。WEATHERWEAVER 通过将天气模拟任务拆分为**天气去除模型**和**天气合成模型**两个互补的视频扩散模型，并采用三阶段数据策略（模拟渲染、生成模型扩增、自动标注真实视频）来克服配对数据稀缺问题，从而在真实世界视频上实现了可控的天气编辑。

### 主实验结果

#### 天气合成任务

在用户研究中，WEATHERWEAVER 在天气合成任务上显著优于基线方法。以雾天合成为例，人类评估者在 **85%** 的样本中偏好 WEATHERWEAVER 而非 AnyV2V，VLM 评估者（Qwen2.5-VL-72B）的偏好率为 **80%**（Table 3）。在所有天气合成对比中，WEATHERWEAVER 的偏好率均超过 50%，表明其一致优于 AnyV2V、TokenFlow、FRESCO 等视频编辑基线。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_00704/figures/007_Table_3.jpg]]
*Table 3: User study. Evaluated by human and VLM evaluators, we report the percentage of samples where Ours is preferred over baselines. A preference > 50% indicates Ours outperforming baselines*

定量评估（Table 2）进一步验证了 WEATHERWEAVER 的优势：在天气合成的 Align. VLM 指标上，WEATHERWEAVER 达到 **77.29**，显著高于基线方法。定性对比（Figure 5）显示，基线方法往往无法生成逼真的瞬态效应（如飘落的雨滴和雪花），而 WEATHERWEAVER 能够保持时间一致性并精确控制天气效果。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_00704/figures/006_Table_2.jpg]]
*Table 2: Quantitative evaluation for weather synthesis and removal*

#### 天气去除任务

在天气去除任务上，WEATHERWEAVER 同样表现优异。定量评估（Table 2）中，天气去除的 Align. VLM 指标达到 **71.61**，优于 HistoFormer、TransWeather、WeatherDiffusion、ViWS-Net 等专用天气去除基线。用户研究（Table 3）中，人类和 VLM 评估者均一致偏好 WEATHERWEAVER 的去除结果。

### 消融实验

消融实验（Figure 8）揭示了三个关键设计选择的影响：

1. **视频模型 vs. 图像模型变体**：将视频模型替换为图像模型变体后，模型无法生成瞬态效应（如飘落的雨滴和雪花），且时间一致性显著下降。这验证了视频扩散模型对于捕捉天气动态变化的必要性。

2. **排除模拟数据**：仅使用生成数据和真实数据训练时，模型在天气效果的精确控制（如着色和强度调节）上表现不佳。模拟数据提供了精确的成对标注，对于学习强度-效果映射至关重要。

3. **联合所有数据源**：同时使用模拟、生成和真实数据进行训练可获得最佳的视觉效果和可控性。单一数据源或两两组合均无法达到全数据源训练的质量水平。

### 可控性验证

WEATHERWEAVER 的六维连续强度向量 $\mathbf{s} \in \mathbb{R}^6$ 提供了精细的天气控制能力。Figure 6 展示了通过调整强度值控制雾的密度和水洼反射程度的效果。Figure 7 进一步展示了多天气效果的时序组合与编辑能力，例如在同一场景中模拟雨-雪-晴的天气变化序列。

### 应用验证

1. **天气编辑**（Figure 9）：通过先应用天气去除模型再应用天气合成模型，WEATHERWEAVER 能够将输入视频中的现有天气替换为不同的天气状态，实现灵活的天气编辑。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_00704/figures/011_Figure_9.jpg]]
*Figure 9: Weather Editing. Combined weather removal and synthesis models allow users to edit existing weather to different states. Figure 10. Improved perception with weather removal. After removing dense fog with our weather removal model, Grounded SAM [63] detects objects (e.g. train, tree) more accurately*

2. **感知模型增强**（Figure 10）：在密集雾天场景中，Grounded-SAM 无法检测到火车等物体；经 WEATHERWEAVER 天气去除后，检测成功恢复。这展示了该方法在自动驾驶和机器人领域的潜在应用价值。

### 失败模式与局限性

尽管 WEATHERWEAVER 在大多数场景下表现优异，但仍存在以下失败模式（Figure S9）：

1. **高频细节丢失**：人脸等精细细节有时会丢失，主要由于基础模型 Stable Video Diffusion 的 VAE 进行 8 倍空间压缩导致信息损失。
2. **夜间场景不佳**：训练数据中夜间视频有限，导致夜间天气场景的模拟质量下降。
3. **模型上限约束**：整体质量受限于 Stable Video Diffusion 的能力上限；升级到更强的视频生成模型可进一步提升效果。

### 评估公平性说明

用户研究同时在人类评估者（MTurk，11 人/对，重复 3 次）和 VLM 评估器（Qwen2.5-VL-72B，7 次运行）上进行，采用多数投票以确保稳定性。训练数据组合了模拟、生成和真实来源，以增强多样性和真实感，避免单一数据偏差。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_00704/figures/013_Figure.jpg]]
*Figure: S2. Example of user study interface for comparing two generated videos for weather synthesis. (a) Weather Synthesis (Rain) Example: Ours vs. AnyV2V (b) Weather Removal Example: HistoFormer vs. Ours Figure S3. Examples on perceptual preference evaluation with VLM. We instructed VLM to first briefly describe the observation, then give the reason why it makes this decision*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2505_00704/figures/003_Table_1.jpg]]
*Table 1: Dataset Statistics. We collect the weather data from three heterogeneous data sources, and mark each properties as high (✓), moderate ${ \bf \Xi } ( \mathrm { ~ ~ \sigma ~ }$ ) . , and low/none (×). The data size is the number of image pairs (with and without weather effects)

## 方法谱系与知识库定位

### 任务定位与核心差异

WEATHERWEAVER 将真实视频中的天气模拟形式化为视频到视频的翻译任务，通过两个互补的可控视频扩散模型实现天气去除与天气合成。该方法的核心差异化在于：将天气效果分解为六个独立分量（云、雾、雨、雪、水洼、雪覆盖），并通过连续强度向量 $\mathbf{s} = ( s_{\mathrm{cloud}}, s_{\mathrm{fog}}, s_{\mathrm{rain}}, s_{\mathrm{snow}}, s_{\mathrm{puddle}}, s_{\mathrm{snow.coverage}} ) \in \mathbb{R}^6$ 进行参数化控制，这与现有方法存在本质区别。

### 与天气合成方法的对比

现有视频编辑方法（如 **AnyV2V**、**TokenFlow**、**FRESCO**）通常依赖文本提示进行天气效果的生成，缺乏对强度和多效果组合的精细控制。用户研究（Table 3）表明，在雾天合成任务中，人类评估者在 85% 的样本中偏好 WEATHERWEAVER 优于 AnyV2V，VLM 评估者偏好率为 80%，说明双模型分解与连续强度参数化在可控性和逼真度上具有显著优势。定性对比（Figure 5）进一步显示，TokenFlow 和 FRESCO 在合成瞬态效应（如雨滴、雪花）时往往出现时间不一致或效果缺失的问题。

在 3D 模拟方法方面，与 **ClimateNeRF** 的对比（Figure S1）表明，WEATHERWEAVER 的视频扩散模型能够在雕像表面和屋顶上生成细腻的积雪覆盖，并调整阴影效果，而这些对基于 NeRF 的 3D 模拟方法而言较难实现。

### 与天气去除方法的对比

天气去除基线包括 **HistoFormer**、**TransWeather**、**WeatherDiffusion**、**ViWS-Net** 以及 **RainMamba** 等。这些方法通常针对单一天气类型设计，或仅处理图像层面的去天气任务。WEATHERWEAVER 的天气去除模型通过在三类数据源上训练，能够处理多种天气类型的视频去除，并作为后续天气合成流程的伪标签引擎。定量评估（Table 2）中，该方法在 VLM 对齐指标上达到 71.61，优于所列基线。

### 适用边界

1. **数据依赖性**：训练数据中夜间视频有限，可能导致夜间天气场景的模拟质量下降。消融实验（Figure 8）表明，排除模拟数据会影响天气效应的精确控制（如着色和强度调节），而联合使用所有数据源（模拟、生成、真实）才能获得最佳视觉效果和可控性。
2. **模型容量限制**：方法构建于 Stable Video Diffusion 之上，其 VAE 的 8 倍空间压缩会导致高频细节（如人脸）丢失。升级到更强的视频基础模型可进一步提升效果，但当前架构存在固有上限。
3. **视频长度限制**：由于 Stable Video Diffusion 的离线推理方式，方法目前适用于短视频片段，扩展到更长视频需要架构层面的改进。

### 局限与开放问题

**已识别的局限**：
- 人脸等精细细节在天气编辑过程中可能丢失（Figure S9）。
- 夜间场景的模拟质量受限于训练数据中夜间视频的稀缺性（Figure S9）。
- 整体质量受限于底层 Stable Video Diffusion 的性能上限。

**待探索的开放问题**：
- 如何在天气编辑中更好地保留文本、人脸等精细细节？
- 在训练数据中夜间视频稀缺的情况下，如何提高夜间天气模拟的鲁棒性？
- 如何将方法扩展到更长视频？
- 多阶段训练策略如何平衡不同数据源，避免对合成数据的过拟合？
- 图像-视频联合训练对时间一致性的具体影响机制是什么？

## 原文 PDF

![[paperPDFs/ICCV_2025/Controllable_Weather_Synthesis_and_Removal_with_Video_Diffusion_Models.pdf]]
