---
title: "CTCal: Rethinking Text-to-Image Diffusion Models via Cross-Timestep Self-Calibration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CTCal_Rethinking_Text_to_Image_Diffusion_Models_via_Cross_Timestep_Self_Calibration.pdf
project_link: null
code_link: "https://github.com/xiefan-guo/ctcal"
aliases:
- CTSCC
- CTCal
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 较小时间步下形成的交叉注意力图——在低噪声条件下，去噪网络能够学习到可靠且空间语义准确的文本-图像对齐，这些注意力图可作为高质量的自监督信号。
primary_logic: 将较小时间步（教师时间步 t_tea）下建立的可靠文本-图像对齐（交叉注意力图）作为显式监督，校准较大时间步（学生时间步 t_stu）下的表征学习，从而在训练阶段直接强化文本-图像对应关系的建模能力。
claims:
- 交叉注意力图在较小时间步下与真实图像结构和语义的对齐显著优于较大时间步
- CTCAL 通过跨时间步自校准实现显式监督，解决了传统扩散损失在文本-图像对齐建模上的不足
- CTCAL 在 T2I-CompBench++ 和 GenEval 基准上均取得显著提升，验证了方法的有效性和泛化性
- T2I-CompBench++ (Color) 上 Color B-VQA = 0.7233 (SD 2.1 + CTCAL E)
---

# CTCal: Rethinking Text-to-Image Diffusion Models via Cross-Timestep Self-Calibration

> [!tip] 核心洞察
> 将较小时间步（教师时间步 t_tea）下建立的可靠文本-图像对齐（交叉注意力图）作为显式监督，校准较大时间步（学生时间步 t_stu）下的表征学习，从而在训练阶段直接强化文本-图像对应关系的建模能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | CTCal：基于跨时间步自校准的文生图扩散模型再思考 |
| 英文题名 | CTCal: Rethinking Text-to-Image Diffusion Models via Cross-Timestep Self-Calibration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.20741) · [Code](https://github.com/xiefan-guo/ctcal) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Cross-Timestep Self-Calibration (CTCAL) |
| Dataset | T2I-CompBench++, GenEval |

> [!tip] 效果简介
> - T2I-CompBench++ (Color) 上，Color B-VQA 0.7233 (SD 2.1 + CTCAL E) vs GORS 基线（+12.56% 相对提升） (+12.56%)。
> - T2I-CompBench++ (2D-Spatial) 上，2D-Spatial UniDet 0.2142 (SD 2.1 + CTCAL E) vs GORS 基线 (显著提升)。
> - GenEval 上，Overall Score 0.69 (SD 3 + CTCAL) vs SD 3 原始模型 (全面提升所有类别)。

## 概要

**核心问题**：文生图扩散模型在较大时间步（高噪声阶段）下，交叉注意力图与真实图像结构的对齐质量急剧下降，导致复杂文本提示的生成图像出现属性绑定错误、对象遗漏等语义不一致问题。传统扩散损失仅提供隐式的文本-图像对应关系监督，无法有效约束这一瓶颈。

**核心方法**：CTCal 提出**跨时间步自校准**（Cross-Timestep Self-Calibration）范式——将较小时间步（低噪声）下建立的可靠文本-图像对齐作为显式自监督信号，校准较大时间步（高噪声）下的表征学习。方法包含五个关键组件：双时间步交叉注意力提取、基于词性的注意力图选择、像素-语义联合优化、主体响应对齐正则化，以及时间步感知自适应加权。

**核心结论**：
- 在 T2I-CompBench++ 基准上，CTCal 在属性绑定、空间关系、计数和复杂组合等维度均取得显著提升，其中 Color B-VQA 指标相对 GORS 基线提升 **+12.56%**。
- 在 GenEval 基准上，CTCal 在所有类别上全面提升性能（SD 3 + CTCAL 达到 Overall 0.69）。
- 用户偏好研究中，CTCal 以 **76.67%**（SD 2.1 对比）和 **54.17%**（SD 3 对比）的偏好率显著优于对比方法。
- 消融实验验证了五个组件逐步叠加均带来一致的性能增益，且方法不损害生成多样性。

**方法定位**：CTCal 属于**训练时微调方法**，模型无关（model-agnostic），可无缝集成到扩散架构（如 SD 2.1）和流匹配架构（如 SD 3）中。与推理时优化方法（如 Attend-and-Excite）和有监督微调方法（如 GORS）形成互补或替代关系。

### 文生图扩散模型的文本-图像对齐瓶颈

文本到图像（T2I）扩散模型近年来取得了显著进展，代表性工作包括 **Stable Diffusion**（Rombach et al., CVPR 2022）、**SDXL**（Podell et al., ICLR 2024）及基于流匹配架构的 **Stable Diffusion 3**（Esser et al., ICML 2024）和 **FLUX.1**（Black Forest Labs, 2024）。这些模型通过在大规模图文对数据上学习去噪过程，逐步将随机噪声转化为与文本描述一致的图像。其核心训练目标为扩散损失：

$$\mathcal{L}_{\mathrm{diffusion}} = \mathcal{D}\left(\epsilon, \epsilon_\theta\left(\mathrm{AddNoise}\left(\mathbf{I}_{\mathrm{real}}, \epsilon, t\right), \mathbf{y}, t\right)\right)$$

然而，该损失函数仅通过最小化预测噪声与真实噪声之间的距离来间接约束文本-图像对应关系，缺乏对文本-图像对齐质量的显式监督。

### 关键瓶颈：交叉注意力图在大时间步下的对齐恶化

交叉注意力（cross-attention）机制是文生图扩散模型中实现文本条件控制的核心组件。通过分析交叉注意力图的行为，论文揭示了一个关键瓶颈：**在较小时间步（低噪声）下，交叉注意力图与真实图像结构和语义的对齐质量较高；但在较大时间步（高噪声）下，这种对齐显著恶化**（Figure 1）。具体而言，当噪声水平升高时，模型难以在空间维度上准确地将文本token（尤其是表示实体的名词）与图像区域对应起来，导致生成图像中出现属性绑定错误、对象遗漏或空间关系混乱等问题。

这一现象的因果机制在于：较小时间步下的噪声干扰较弱，去噪网络能够从含噪图像中提取出相对可靠的结构信息，从而形成空间语义准确的交叉注意力图；而较大时间步下的高噪声破坏了图像结构，使得交叉注意力层难以建立有意义的文本-图像对应关系。

### 现有方法的局限性

针对上述问题，现有解决方案大致分为两类：

- **推理时优化方法**（如 **Attend-and-Excite**，Chefer et al., TOG 2023）：在推理阶段动态调整交叉注意力图以增强特定token的响应，但这类方法无法从根本上改善模型的文本-图像对齐能力，且增加了推理延迟。
- **有监督微调方法**（如 **GORS**）：通过在高质量图文数据集上微调来提升对齐质量，但依然依赖于隐式的扩散损失监督，未能直接针对交叉注意力图的对齐质量进行优化。

这两类方法均未充分利用一个关键观察：**较小时间步下形成的可靠交叉注意力图可以作为高质量的自监督信号**。

### 本文动机

基于上述分析，本文提出核心洞察：将较小时间步（教师时间步 $t_{\mathrm{tea}}$）下建立的可靠文本-图像对齐作为显式监督，校准较大时间步（学生时间步 $t_{\mathrm{stu}}$）下的表征学习。这一思路将训练过程中模型自身产生的优质注意力图转化为校准信号，无需额外标注数据或推理时干预，从而在训练阶段直接强化文本-图像对应关系的建模能力。

## 核心方法与创新机理

### 关键瓶颈：交叉注意力图的时间步退化

文生图扩散模型的标准训练仅依赖扩散损失 $\mathcal{L}_{\mathrm{diffusion}}$（Eq. 1），该损失通过最小化预测噪声与真实噪声的距离来优化去噪网络。然而，这种监督方式对文本-图像对应关系的建模是**隐式**的——模型从未被显式告知某个文本token应该关注图像的哪个空间区域。

Figure 1 揭示了这一隐式监督的致命缺陷：在较小时间步（低噪声）下，交叉注意力图与真实图像结构和语义的对齐质量良好；但**随着时间步增大（噪声增强），这种对齐会急剧恶化**。这意味着模型在训练早期（高噪声阶段）学到的文本-图像对应关系是不可靠的，导致复杂文本提示下的生成图像出现属性绑定错误、对象遗漏、空间关系混乱等语义不一致问题。

### 核心洞察：以“自我”为师

本工作的关键洞察在于：**较小时间步下形成的交叉注意力图本身就是高质量的自监督信号**。在低噪声条件下，去噪网络能够学习到可靠且空间语义准确的文本-图像对齐，这些注意力图可以作为“教师”，去校准较大时间步下的表征学习。

基于此洞察，CTCAL 将传统“单时间步采样 + 隐式对齐”的训练范式改造为**“双时间步采样 + 显式对齐”**的自校准范式：

- **教师时间步 $t_{\mathrm{tea}}$**：采样较小时间步，提取其交叉注意力图 $\mathbf{A}_{\mathrm{tea}}$ 作为校准目标
- **学生时间步 $t_{\mathrm{stu}}$**：采样较大时间步（$t_{\mathrm{tea}} < t_{\mathrm{stu}}$），提取其交叉注意力图 $\mathbf{A}_{\mathrm{stu}}$ 作为优化对象
- **CTCAL 损失**：直接最小化 $\mathbf{A}_{\mathrm{stu}}$ 与 $\mathbf{A}_{\mathrm{tea}}$ 之间的距离，提供显式的文本-图像对齐监督

### 五个关键 Changed Slots

CTCAL 对标准扩散训练框架进行了五个关键改造，每个改造对应一个明确的 changed slot：

**1. 训练损失函数：从单一到联合**

基线仅使用扩散损失，CTCAL 将其扩展为联合损失：
$$\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \mathcal{L}_{\mathrm{CTCAL}}$$

其中 $\mathcal{L}_{\mathrm{CTCAL}}$ 直接度量学生与教师注意力图之间的距离，将隐式对齐转化为显式监督。

**2. 训练采样策略：从单时间步到双时间步**

基线每个样本仅采样一个时间步，CTCAL 采样两个时间步 $t_{\mathrm{tea}} < t_{\mathrm{stu}}$，并在一次前向传播中同时提取两者的交叉注意力图（Figure 2），无需额外的模型调用。

**3. 注意力图选择：从全量token到名词筛选**

基线使用所有文本token对应的注意力图。Figure 3 的分析表明，名词token（如“cat”）编码了清晰的空间语义信息，而冠词、连词等功能词缺乏有效的空间语义。因此 CTCAL 引入基于词性的选择策略：使用 Stanza 进行词性分析，**仅保留名词token对应的交叉注意力图**参与校准（Eq. 3），避免无意义token的噪声干扰。

**4. 对齐优化空间：从像素级到像素-语义联合**

基线仅关注像素级空间对齐，CTCAL 引入一个轻量自编码器实现**像素-语义联合优化**（Eq. 5）：
- **像素级损失**：直接对齐原始注意力图的空间分布
- **语义级损失**：编码器 $f_{\mathrm{attn}}^{\mathrm{enc}}$ 将注意力图投影到语义空间后进行对齐，捕捉高层语义一致性
- **重建代理任务**：解码器 $f_{\mathrm{attn}}^{\mathrm{dec}}$ 需从编码特征重建教师注意力图，防止编码器模式坍塌

此外，针对多主体场景中高响应主体掩盖低响应主体的问题，引入**主体响应对齐正则化**（Eq. 6）：
$$\mathcal{R}_{\mathrm{subject}} = \frac{1}{N_{\mathrm{noun}}} \sum_{\mathbf{y}_i \in \mathcal{Y}_{\mathrm{noun}}} \mathrm{ReLU}\left(S_{\mathrm{attn}} - \max(\mathbf{A}_{\mathrm{stu}, \mathbf{y}_i}) - \tau\right)$$

该正则化将所有名词主体的最大交叉注意力响应推向全局最高响应 $S_{\mathrm{attn}}$，阈值 $\tau$ 防止对已平衡的主体施加不必要约束。

**5. 损失权重：从固定到时间步自适应**

基线使用固定权重，CTCAL 引入**时间步感知自适应加权**（Eq. 8）：
$$\lambda_t = \frac{t_{\mathrm{stu}}}{T_{\mathrm{train}}}$$

CTCAL 损失权重与学生时间步成正比——较大时间步（高噪声）下注意力对齐更差，更需要校准信号；较小时间步下模型本身已能形成较好对齐，校准需求较低。该设计实现了 CTCAL 与扩散损失的和谐融合。

### 方法谱系与知识库定位

CTCAL 属于**训练时微调方法**，与以下方法形成对比：
- **推理时优化方法**（如 **Attend-and-Excite**，Chefer et al., TOG 2023）：在推理阶段修改注意力图，无需训练但计算开销大且效果有限
- **有监督微调方法**（如 **GORS**）：依赖外部高质量图文数据集进行微调，但未利用扩散模型自身的跨时间步一致性

CTCAL 的核心优势在于**模型无关性**——它不修改扩散模型的架构，仅改变训练损失和采样策略，可无缝集成到扩散架构（如 **Stable Diffusion 2.1**，Rombach et al., CVPR 2022）和流匹配架构（如 **Stable Diffusion 3**，Esser et al., ICML 2024）中。代码已开源（https://github.com/xiefan-guo/ctcal），基于 Diffusers 代码库实现，采用 LoRA 微调文本编码器的自注意力层和去噪网络的注意力层。

### 核心思想与动机

文生图扩散模型在训练过程中仅通过扩散损失 $\mathcal{L}_{\mathrm{diffusion}}$ 提供隐式的文本-图像对应关系监督。如 Figure 1 所示，交叉注意力图在较小时间步（低噪声条件）下与真实图像结构和语义的对齐质量显著优于较大时间步（高噪声条件），这一对齐退化是导致复杂文本提示下生成图像出现语义不一致的关键瓶颈。CTCal 的核心洞察在于：**较小时间步下形成的交叉注意力图可作为高质量的自监督信号，用于显式校准较大时间步下的表征学习**。

### 训练范式总览

CTCal 提出了一种跨时间步自校准训练范式（Figure 2），其与传统扩散训练的核心区别在于双时间步采样策略与交叉注意力图的对齐优化。

**Pipeline 模块关系与数据流如下：**

1. **双时间步交叉注意力提取**：对每个训练样本，同时采样两个时间步——教师时间步 $t_{\mathrm{tea}}$ 和学生时间步 $t_{\mathrm{stu}}$，满足 $t_{\mathrm{tea}} < t_{\mathrm{stu}}$。在去噪网络的前向传播中，分别提取两者的交叉注意力图 $\mathbf{A}_{\mathrm{tea}}$ 和 $\mathbf{A}_{\mathrm{stu}}$。教师时间步在低噪声下形成可靠的文本-图像对齐，学生时间步在高噪声下需要校准。

2. **基于词性的注意力图选择**：使用 Stanza 进行词性分析，仅保留名词 token 对应的交叉注意力图。如 Figure 3 所示，名词 token（如“cat”）编码了清晰的空间语义信息，而冠词、连词等非名词 token 缺乏有效的空间语义，过滤后可提升校准信号的纯度。

3. **像素-语义联合优化**：引入轻量自编码器 $f_{\mathrm{attn}}^{\mathrm{enc}}/f_{\mathrm{attn}}^{\mathrm{dec}}$，将注意力图投影到语义空间。CTCAL 损失由四个组件构成（Eq. 7）：
   - **像素级损失**：直接在注意力图空间对齐 $\mathbf{A}_{\mathrm{stu}}$ 与 $\mathbf{A}_{\mathrm{tea}}$；
   - **语义级损失**：在编码器投影的语义空间中对齐两者表征；
   - **重建代理任务**：解码器从编码特征重建 $\mathbf{A}_{\mathrm{tea}}$，防止编码器模式坍塌；
   - **主体响应对齐正则化** $\mathcal{R}_{\mathrm{subject}}$：将所有名词主体的最大交叉注意力响应对齐到全局最大响应 $S_{\mathrm{attn}}$，阈值 $\tau$ 防止对已平衡的主体施加不必要约束，避免高响应主体掩盖低响应主体。

4. **时间步感知自适应加权**：CTCAL 损失权重 $\lambda_t = t_{\mathrm{stu}} / T_{\mathrm{train}}$ 与学生时间步成正比——较大时间步（高噪声）更需要校准信号，实现 CTCAL 与扩散损失的和谐融合（Eq. 8）。

### 输入输出规范

- **输入**：文本提示 $\mathbf{y}$、真实图像 $\mathbf{I}_{\mathrm{real}}$、采样的噪声 $\epsilon$、双时间步 $(t_{\mathrm{tea}}, t_{\mathrm{stu}})$。
- **输出**：总损失 $\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \lambda_t \mathcal{L}_{\mathrm{CTCAL}}$，其中 $\mathcal{L}_{\mathrm{CTCAL}}$ 仅对名词 token 子集 $\mathcal{Y}_{\mathrm{noun}}$ 计算。
- **训练方式**：基于 Diffusers 代码库实现，采用 Low-Rank Adaptation（LoRA）微调文本编码器的自注意力层和去噪网络的注意力层，是一种模型无关的训练范式，可无缝集成到扩散架构（如 SD 2.1）和流匹配架构（如 SD 3）中。

### 关键瓶颈与核心洞察

文生图扩散模型的标准训练仅依赖扩散损失 $\mathcal{L}_{\mathrm{diffusion}}$，该损失通过最小化预测噪声与真实噪声之间的距离来优化去噪网络，但仅能提供隐式的文本-图像对应关系监督。论文通过实验揭示了一个关键瓶颈：**在较大时间步（高噪声）下，交叉注意力图与真实图像结构的对齐质量急剧下降**（Figure 1b），导致复杂文本提示的生成图像出现语义不一致。

核心洞察在于：较小时间步（低噪声）下形成的交叉注意力图能够学习到可靠且空间语义准确的文本-图像对齐，这些注意力图可作为高质量的自监督信号。CTCAL 正是利用这一“教师时间步”的可靠对齐，显式地校准“学生时间步”（较大时间步）下的表征学习。

### 总体损失函数

CTCAL 的训练目标是在标准扩散损失基础上，引入跨时间步自校准损失。总体损失函数为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \mathcal{L}_{\mathrm{CTCAL}}$$

其中扩散损失的定义为：

$$\mathcal{L}_{\mathrm{diffusion}} = \mathcal{D}\left(\epsilon, \epsilon_\theta\left(\mathrm{AddNoise}\left(\mathbf{I}_{\mathrm{real}}, \epsilon, t\right), \mathbf{y}, t\right)\right)$$

$\mathcal{D}$ 为距离度量函数，$\epsilon$ 为真实噪声，$\epsilon_\theta$ 为去噪网络预测的噪声，$\mathbf{I}_{\mathrm{real}}$ 为真实图像，$\mathbf{y}$ 为文本条件，$t$ 为时间步。

### 双时间步交叉注意力提取

CTCAL 的核心操作是采样两个不同的时间步：教师时间步 $t_{\mathrm{tea}}$ 和学生时间步 $t_{\mathrm{stu}}$，满足 $t_{\mathrm{tea}} < t_{\mathrm{stu}}$。在训练过程中，分别从两个时间步提取交叉注意力图 $\mathbf{A}_{\mathrm{tea}}$ 和 $\mathbf{A}_{\mathrm{stu}}$，以教师注意力图为目标校准学生注意力图的学习（Figure 2）。

### 基于词性的注意力图选择

并非所有文本 token 的交叉注意力图都编码了有效的空间语义信息。论文通过词性分析（Figure 3）发现，**名词 token 的交叉注意力图编码了清晰的空间语义信息**，而冠词、连词等功能词缺乏有效的空间语义。因此，CTCAL 采用基于词性的注意力图选择策略，仅对名词 token 对应的注意力图计算对齐损失：

$$\mathcal{L}_{\mathrm{CTCAL}} = \frac{1}{N_{\mathrm{noun}}} \sum_{\mathbf{y}_i \in \mathcal{V}_{\mathrm{noun}}} \mathcal{D}\left(\mathbf{A}_{\mathrm{stu}, \mathbf{y}_i}, \mathbf{A}_{\mathrm{tea}, \mathbf{y}_i}\right)$$

其中 $N_{\mathrm{noun}}$ 为名词 token 数量，$\mathcal{V}_{\mathrm{noun}}$ 为名词 token 集合，$\mathbf{A}_{\mathrm{stu}, \mathbf{y}_i}$ 和 $\mathbf{A}_{\mathrm{tea}, \mathbf{y}_i}$ 分别为 token $\mathbf{y}_i$ 在学生时间步和教师时间步的交叉注意力图。词性分析使用 Stanza 工具完成。

### 像素-语义联合优化

单纯在像素空间对齐注意力图存在局限性：注意力图的高维性和噪声特性可能导致对齐不稳定。为此，CTCAL 引入一个轻量自编码器，实现像素级与语义级的联合优化。

编码器 $f_{\mathrm{attn}}^{\mathrm{enc}}$ 将注意力图投影到低维语义空间，在此空间进行对齐；解码器 $f_{\mathrm{attn}}^{\mathrm{dec}}$ 通过重建教师注意力图作为代理任务，防止编码器发生模式坍塌。完整的像素-语义联合优化损失为：

$$\mathcal{L}_{\mathrm{CTCAL}} = \frac{1}{N_{\mathrm{noun}}} \sum_{\mathbf{y}_i \in \mathcal{Y}_{\mathrm{noun}}} \left[\lambda_1 \mathcal{D}(\mathbf{A}_{\mathrm{stu},\mathbf{y}_i}, \mathbf{A}_{\mathrm{tea},\mathbf{y}_i}) + \lambda_2 \mathcal{D}(f_{\mathrm{attn}}^{\mathrm{enc}}(\mathbf{A}_{\mathrm{stu},\mathbf{y}_i}), f_{\mathrm{attn}}^{\mathrm{enc}}(\mathbf{A}_{\mathrm{tea},\mathbf{y}_i})) + \lambda_3 \mathcal{D}(f_{\mathrm{attn}}^{\mathrm{dec}}(f_{\mathrm{attn}}^{\mathrm{enc}}(\mathbf{A}_{\mathrm{tea},\mathbf{y}_i})), \mathbf{A}_{\mathrm{tea},\mathbf{y}_i})\right]$$

其中三项分别为：像素级损失（空间对齐）、语义级损失（语义空间对齐）、重建代理任务（防止编码器过拟合）。$\lambda_1$、$\lambda_2$、$\lambda_3$ 为各损失项的权重系数。

### 主体响应对齐正则化

CTCAL 的空间对齐机制可能面临主体间注意力响应不平衡的问题：高响应主体可能掩盖低响应主体，导致后者在生成中被忽视。为解决此问题，引入主体响应对齐正则化：

$$\mathcal{R}_{\mathrm{subject}} = \frac{1}{N_{\mathrm{noun}}} \sum_{\mathbf{y}_i \in \mathcal{Y}_{\mathrm{noun}}} \mathrm{ReLU}\left(S_{\mathrm{attn}} - \max(\mathbf{A}_{\mathrm{stu}, \mathbf{y}_i}) - \tau\right)$$

该正则项将所有名词主体的最大交叉注意力响应对齐到全局最大响应 $S_{\mathrm{attn}}$。阈值 $\tau$ 用于防止对已平衡的主体施加不必要约束，$\mathrm{ReLU}$ 确保仅惩罚响应过低的主体。

### CTCAL 完整损失分解

综合上述组件，CTCAL 的最终损失函数由四个部分构成：

$$\mathcal{L}_{\mathrm{CTCAL}} = \frac{1}{N_{\mathrm{noun}}} \sum_{\mathbf{y}_i \in \mathcal{Y}_{\mathrm{noun}}} \left[\lambda_1 \underbrace{\mathcal{D}(\mathbf{A}_{\mathrm{stu},\mathbf{y}_i}, \mathbf{A}_{\mathrm{tea},\mathbf{y}_i})}_{\mathrm{Pixel\ loss}} + \lambda_2 \underbrace{\mathcal{D}(f_{\mathrm{attn}}^{\mathrm{enc}}(\mathbf{A}_{\mathrm{stu},\mathbf{y}_i}), f_{\mathrm{attn}}^{\mathrm{enc}}(\mathbf{A}_{\mathrm{tea},\mathbf{y}_i}))}_{\mathrm{Semantic\ level\ loss}} + \lambda_3 \underbrace{\mathcal{D}(f_{\mathrm{attn}}^{\mathrm{dec}}(\mathbf{A}_{\mathrm{tea},\mathbf{y}_i}), \mathbf{A}_{\mathrm{tea},\mathbf{y}_i})}_{\mathrm{Reconstruction\ proxy\ task}} + \lambda_4 \underbrace{\mathcal{R}_{\mathrm{subject}}}_{\mathrm{Regularization}}\right]$$

### 时间步感知自适应加权

不同时间步对校准信号的需求程度不同：较大时间步（高噪声）下注意力对齐更差，更需要 CTCAL 的监督。为此，论文设计了时间步感知自适应加权策略，使 CTCAL 损失权重与学生时间步成正比：

$$\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \lambda_t \mathcal{L}_{\mathrm{CTCAL}}, \quad \lambda_t = \frac{t_{\mathrm{stu}}}{T_{\mathrm{train}}}$$

其中 $T_{\mathrm{train}}$ 为训练时的最大时间步。该设计使得 CTCAL 损失与扩散损失实现和谐融合：在低噪声阶段 CTCAL 权重较小，避免干扰已较好的对齐；在高噪声阶段权重增大，强化校准效果。

## 实验与关键发现

### 核心瓶颈的实证动机

文生图扩散模型在较大时间步（高噪声阶段）存在一个关键缺陷：交叉注意力图与真实图像结构的对齐质量急剧下降。Figure 1 的实证分析揭示了这一瓶颈——在推理阶段（Figure 1a），随着去噪步数增加，交叉注意力图逐渐聚焦于语义相关区域，但在训练阶段（Figure 1b），较小时间步（$t=0$）下形成的注意力图与真实图像结构和语义高度一致，而较大时间步（$t=T$）下的注意力图则严重偏离，几乎丧失空间语义信息。这一发现直接表明：**传统扩散损失仅能提供隐式的文本-图像对应关系监督，无法在训练阶段有效约束高噪声条件下的注意力学习**，这是导致复杂文本提示下生成图像出现语义不一致的根本原因。

### 主要实验结果

#### T2I-CompBench++ 基准评估

Table 1 展示了在 T2I-CompBench++ 上的全面客观评估结果。CTCAL 在属性绑定、对象关系、计数和复杂组合等所有类别上均展现出显著优势：

- **经典扩散模型（SD 2.1）**：CTCAL E 版本在 Color B-VQA 上达到 0.7233，相比 GORS 有监督微调方法相对提升 **+12.56%**；在 2D-Spatial UniDet 上达到 0.2142，同样显著优于所有对比基线。
- **先进扩散模型（SD 3）**：SD 3 (2B) + CTCAL 在大多数指标上取得最高分，Complex 3-in-1 达到 0.3814，验证了 CTCAL 对基于流匹配架构的模型同样有效。
- **推理时优化方法对比**：Attend-and-Excite（Chefer et al., TOG 2023）等方法仅能在推理阶段进行后处理修正，而 CTCAL 通过训练阶段显式校准从根本上改善了文本-图像对齐质量，性能提升更为显著。

#### GenEval 基准评估

Table 2 的 GenEval 评估进一步验证了 CTCAL 的泛化性。SD 3 + CTCAL 在所有类别上均实现性能提升，Overall Score 达到 **0.69**，证明该方法不局限于特定评估维度，而是全面增强了模型的文本-图像对齐能力。

![[assets/figures/papers/paper_list_l2302_https_arxiv_org_abs_2603_20741/figures/006_Table_2.jpg]]
*Table 2: Objective evaluation on GenEval. CTCAL improves performance across all categories*

#### 用户偏好研究

Table 3 的主观用户偏好研究显示，CTCAL 生成图像的人类偏好率在 SD 2.1 对比中达到 **76.67%**，在 SD 3 对比中达到 **54.17%**，显著优于 GORS 等对比方法。这表明 CTCAL 的改进不仅体现在自动评估指标上，也在人类感知层面获得了明确认可。

### 消融实验

#### 组件贡献分析

Table 4 的消融实验在 SD 2.1 上逐步叠加 CTCAL 各组件，清晰展示了每个模块的贡献：

![[assets/figures/papers/paper_list_l2302_https_arxiv_org_abs_2603_20741/figures/008_Table_4.jpg]]
*Table 4: Ablation study on Stable Diffusion 2.1*

- **基础 CTCAL (B)**：仅引入双时间步交叉注意力对齐，相比基线已有提升
- **+词性选择 (C)**：仅保留名词token的注意力图，过滤掉无语义空间信息的token，Color B-VQA 和 2D-Spatial UniDet 均获提升
- **+像素-语义联合优化 (D)**：引入轻量自编码器进行语义空间对齐与重建代理任务，性能进一步提升
- **+时间步感知自适应权重 (E)**：采用 $\lambda_t = t_{\mathrm{stu}} / T_{\mathrm{train}}$ 的自适应加权策略，达到最优性能

五个组件逐步叠加均带来单调的性能增益，验证了每个设计选择的有效性。

#### 教师时间步选择

Table 5 探究了不同 $t_{\mathrm{tea}}$ 取值的影响。对于经典扩散模型（如 SD 2.1），**$t_{\mathrm{tea}}=0$ 为最优选择**——此时噪声最低，交叉注意力图与真实图像结构的对齐最为可靠，提供的自监督信号质量最高。

![[assets/figures/papers/paper_list_l2302_https_arxiv_org_abs_2603_20741/figures/010_Table_5.jpg]]
*Table 5: Objective evaluation on*

#### 形容词token的纳入

Table 6 的消融实验表明，将形容词token纳入 CTCAL 可进一步提升属性绑定性能（Color B-VQA 提升至 **0.7328**），但对空间任务略有影响。这一权衡说明当前以名词为核心的注意力校准策略在属性绑定与空间理解之间存在微妙的平衡，需根据具体应用场景进行选择。

![[assets/figures/papers/paper_list_l2302_https_arxiv_org_abs_2603_20741/figures/011_Table_6.jpg]]
*Table 6: Objective evaluation on adj*

#### 多样性与质量评估

Table 7 验证了 CTCAL **不损害生成多样性**——在 Color 类别上 M-LPIPS 为 0.634，同时美学评分提升至 **5.288**。这一结果消除了对显式注意力校准可能导致生成模式坍塌的担忧。

![[assets/figures/papers/paper_list_l2302_https_arxiv_org_abs_2603_20741/figures/012_Table_7.jpg]]
*Table 7: More results on diversity and quality evaluation*

### 注意力图可视化验证

Figure 5 对比了 CTCAL 与 GORS 微调模型在推理和训练模式下的交叉注意力图。CTCAL 微调后的模型在较大时间步保持了与较小时间步高度一致的注意力分配，而 GORS 微调模型在较大时间步的注意力图仍存在明显偏离。这直接验证了 CTCAL 的核心机制——**通过跨时间步自校准，将低噪声条件下的可靠文本-图像对齐显式传递到高噪声阶段**，从根本上改善了训练过程中的注意力学习质量。

### 失败模式与局限性

尽管 CTCAL 在多个基准上取得了显著提升，仍存在以下局限：

1. **训练依赖性**：CTCAL 需要微调阶段，无法在纯推理阶段即插即用，每次适配新模型需准备高质量图文数据集进行训练。
2. **词性选择的权衡**：当前以名词token为核心的设计在属性绑定（形容词相关）任务上仍有提升空间，纳入形容词token虽可改善属性绑定，但对空间任务存在潜在负面影响，最优策略需进一步探索。
3. **架构泛化边界**：验证主要覆盖 SD 2.1（扩散架构）和 SD 3（流匹配架构），对 DiT 变体、SANA 等新兴架构的泛化表现尚不明确。
4. **计算开销**：双时间步采样与自编码器语义投影引入了额外训练计算，论文未提供具体的额外训练时间对比数据，实际部署成本需手动评估。

![[assets/figures/papers/paper_list_l2302_https_arxiv_org_abs_2603_20741/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison on SD 2.1 and SD 3. CTCAL demonstrates a marked improvement in the fine-grained alignment of generated images with the corresponding text prompts. Each image is generated with the same prompt and random seed for all methods*

## 定位与知识库关联

### 1. 核心基线定位

CTCAL 是一种**训练时微调方法**，其核心创新在于将扩散模型内部的跨时间步自监督信号显式化为文本-图像对齐的监督目标。在方法谱系中，它与以下三类基线构成对比关系：

**基础扩散模型基线。** 论文在两类架构上验证了 CTCAL 的模型无关性：基于扩散范式的 **Stable Diffusion 2.1**（Rombach et al., CVPR 2022）和 **SDXL**（Podell et al., ICLR 2024），以及基于流匹配范式的 **Stable Diffusion 3**（Esser et al., ICML 2024）和 **FLUX.1**（Black Forest Labs, 2024）。这些基线模型仅依赖标准扩散损失 $\mathcal{L}_{\mathrm{diffusion}}$ 进行训练，缺乏对文本-图像对齐的显式监督。

**推理时优化方法。** **Attend-and-Excite**（Chefer et al., TOG 2023）是代表性的推理时优化方法，通过分析推理阶段的交叉注意力图来引导生成过程。CTCAL 的分析表明（Figure 1），推理阶段的交叉注意力图在大时间步下同样面临对齐质量退化的问题，因此推理时优化方法本质上受到与训练阶段相同的瓶颈制约。CTCAL 选择在训练阶段从根本上解决这一问题，而非在推理阶段进行事后修正。

**有监督微调方法。** **GORS** 是论文中直接对比的有监督微调方法，其具体技术细节和发表信息在提供的材料中未明确给出（需手动核验）。CTCAL 与 GORS 的关键区别在于：GORS 依赖外部监督信号，而 CTCAL 利用模型自身在较小时间步下形成的可靠注意力图作为自监督信号，无需额外的标注数据。

### 2. 方法适用边界

**架构兼容性。** CTCAL 的设计原理——利用交叉注意力图的跨时间步一致性——使其天然适用于所有基于交叉注意力机制实现文本-图像融合的扩散模型。论文在 SD 2.1（UNet 架构）和 SD 3（MM-DiT 架构）上的验证覆盖了当前主流的两种去噪网络范式。然而，对于不使用交叉注意力机制的替代性文本条件注入方案（如某些基于自适应归一化的设计），CTCAL 无法直接应用。

**训练范式约束。** CTCAL 需要微调阶段，无法在纯推理阶段即插即用。每次适配新模型或新领域时，需要准备高质量的图文数据集进行微调。论文采用 **LoRA**（Low-Rank Adaptation）进行参数高效微调，在 Diffusers 代码库中实现，仅微调文本编码器的自注意力层和去噪网络的注意力层，这在一定程度上降低了部署成本。

**文本复杂度边界。** 当前验证集中在 T2I-CompBench++ 和 GenEval 基准上，这些基准的文本提示以中等长度的属性绑定、空间关系和计数任务为主。对于超长文本提示（如段落级描述）或高度复杂的多对象交互场景，CTCAL 的表现尚缺乏系统性评估。

### 3. 局限性与开放问题

**训练计算开销。** 双时间步采样策略要求每次训练迭代进行两次前向传播（分别提取 $t_{\mathrm{tea}}$ 和 $t_{\mathrm{stu}}$ 的交叉注意力图），加上轻量自编码器的语义投影与重建计算，引入了一定的额外训练开销。论文未提供具体的额外训练时间对比数据，这一点的实际影响需要手动核验。

**词性选择的权衡。** 当前设计以名词 token 为核心进行注意力校准，这是基于名词编码清晰空间语义信息的观察（Figure 3）。消融实验（Table 6）表明，加入形容词 token 可进一步提升属性绑定性能（Color B-VQA 提升至 0.7328），但对空间任务略有负面影响。这种权衡关系意味着词性选择策略可能需要根据具体应用场景进行调节，而非存在普适的最优配置。

**教师时间步的自适应选择。** 论文通过消融实验（Table 5）确定经典扩散模型的最优教师时间步为 $t_{\mathrm{tea}}=0$，但该结论是否因模型架构和训练数据分布而异尚不明确。是否存在自适应选择 $t_{\mathrm{tea}}$ 的策略——例如根据当前训练阶段或样本难度动态调整——是一个值得探索的方向。

**跨模态扩展潜力。** CTCAL 的核心思想——利用低噪声条件下形成的可靠跨模态对齐来校准高噪声条件下的学习——在概念上可扩展到视频扩散模型中的文本-视觉对齐、3D 生成模型中的多视图一致性等任务，但目前缺乏实验验证。

**与推理时优化的协同。** CTCAL 在训练阶段改善了交叉注意力图的质量，而推理时优化方法（如 Attend-and-Excite）在推理阶段进一步修正注意力分布。两者在机制上互补，是否可以通过联合使用获得进一步的性能提升，是一个开放问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/CTCal_Rethinking_Text_to_Image_Diffusion_Models_via_Cross_Timestep_Self_Calibration.pdf]]
