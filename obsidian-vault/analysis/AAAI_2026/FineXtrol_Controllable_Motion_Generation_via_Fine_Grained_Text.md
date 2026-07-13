---
title: "FineXtrol: Controllable Motion Generation via Fine-Grained Text"
type: paper
paper_level: A
venue: AAAI
year: 2026
pdf_ref: paperPDFs/AAAI_2026/FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text.pdf
project_link: null
code_link: null
aliases:
- FineXtrol
tags:
- AAAI_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入带有明确时间间隔的细粒度文本控制信号，结合层次对比学习增强文本编码器区分能力，并通过ControlNet式双分支框架以残差形式注入控制信号。
primary_logic: 利用细粒度、时间感知的文本描述作为控制信号，可替代空间坐标控制，实现更高效、直观且精确的局部运动控制；层次对比学习可提升文本编码器对细粒度动作语义的敏感性；双分支解耦设计使得模型在保持粗粒度文本生成能力的同时，精确跟随细粒度控制约束。
claims:
- FineXtrol在HumanML3D上的FID为0.245，较无控制的MDM（0.544）下降54.9%，且R-Top3精度达0.685，超越基于坐标的OmniControl（0.684）和InterControl（0.671）。
- 用户研究中，FineXtrol在75.76%的情况下优于CoMo，证明其生成的运动更符合控制信号且更自然。
- 层次对比学习训练后的文本编码器在区分细粒度文本信号上显著优于CLIP和T5（FID从0.347降至0.245）。
- 采用双分支控制范式相比直接拼接控制文本，FID从1.383降至0.245，R-Top3从0.601提升至0.685。
---

# FineXtrol: Controllable Motion Generation via Fine-Grained Text

> [!tip] 核心洞察
> 利用细粒度、时间感知的文本描述作为控制信号，可替代空间坐标控制，实现更高效、直观且精确的局部运动控制；层次对比学习可提升文本编码器对细粒度动作语义的敏感性；双分支解耦设计使得模型在保持粗粒度文本生成能力的同时，精确跟随细粒度控制约束。

| 字段 | 内容 |
|------|------|
| 中文题名 | FineXtrol：基于细粒度文本的可控运动生成 |
| 英文题名 | FineXtrol: Controllable Motion Generation via Fine-Grained Text |
| 会议/期刊 | AAAI 2026 |
| Links |  [paper](https://arxiv.org/abs/2511.18927)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | FineXtrol |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.245 vs 0.544 (-0.299)；R-Precision Top-3↑ 0.685 vs 0.611 (+0.074)；FID↓ 0.245 vs 0.209 (OmniControl Coordinate) (+0.036)。

## 概要

### 问题背景

文本到运动生成（text-to-motion generation）旨在根据自然语言描述合成逼真的三维人体运动序列。然而，现有的主流方法存在一个根本性瓶颈：**难以同时实现精确、时间感知和用户友好的身体部位控制**。具体而言，基于LLM扩展文本描述的方法（如**CoMo**，Huang et al., ECCV 2024）虽然引入了细粒度语义，但缺乏明确的时间对齐机制，且生成的动作描述常与真实运动存在事实偏差；基于空间坐标序列的方法（如**OmniControl**，Xie et al., ICLR 2024；**InterControl**，Wang et al., NeurIPS 2024）虽然控制精确，但需要用户提供全局3D关节坐标轨迹，这在开放场景中极不直观，且坐标转换与处理带来高昂的计算开销。

### 核心方法

**FineXtrol** 提出了一种全新的控制范式：**以带有明确时间间隔的细粒度文本描述替代空间坐标作为控制信号**。用户只需指定如“在1.0–1.5秒内将左腿向右移动”这样的自然语言指令，即可实现对特定身体部位在特定时间段内的精确控制。这一设计的关键因果机制在于：细粒度文本天然具备语义可解释性和时间结构性，使得控制信号既直观又精确。

为实现这一范式，FineXtrol构建了三个核心技术组件：

1. **双分支ControlNet式残差注入框架**：冻结预训练的MDM（Tevet et al., ICLR 2023）作为粗粒度文本生成分支，保持基础运动生成能力；引入一个可训练的MDM副本作为控制分支，专门处理细粒度控制信号，并通过零初始化线性层以残差形式将控制特征注入主分支，避免早期训练噪声干扰。
2. **层次对比学习微调的文本编码器**：在T5编码器基础上，引入句子级、片段级和序列级三层对比学习，显著提升编码器对细粒度动作语义的区分能力，使其能够精确捕捉不同身体部位、不同时间段的运动差异。
3. **六大身体部位划分**：将人体划分为头部、躯干、左臂、右臂、左腿、右腿六个可控区域，在控制粒度和用户友好性之间取得平衡。

### 主要结果

在HumanML3D基准上，FineXtrol取得了具有竞争力的表现：

- **生成质量**：FID达到**0.245**，较无控制的MDM（0.544）下降54.9%，与基于坐标的OmniControl（0.209）差距仅0.036，但显著优于基于文本的CoMo（0.347，下降0.102）。
- **控制精度**：R-Precision Top-3达到**0.685**，超越OmniControl（0.684）和InterControl（0.671），证明细粒度文本控制在语义匹配上具有优势。
- **推理效率**：推理时间仅**128.57秒**，可训练参数量仅**23.39M**，均为对比扩散式可控运动生成方法中最低。
- **用户偏好**：用户研究中，FineXtrol在**75.76%**的情况下优于CoMo，验证了其在控制信号对齐度和运动自然度上的综合优势。

消融实验进一步证实：双分支控制范式相比直接拼接控制文本，FID从1.383降至0.245，R-Top3从0.601提升至0.685；层次对比学习训练后的文本编码器相比CLIP和T5，FID分别改善0.102和0.255。当控制信号密度增加时，FineXtrol性能稳定提升，而基于坐标的OmniControl则因约束过强而退化，凸显了文本控制信号的鲁棒性优势。

### 方法定位

FineXtrol在可控运动生成的方法谱系中占据独特位置：它既不同于传统坐标控制方法（PriorMDM、GMD、OmniControl、InterControl）依赖空间轨迹输入，也不同于LLM扩展文本方法（CoMo）缺乏时间对齐和事实准确性。其核心洞察在于：**细粒度、时间感知的文本描述可以成为空间坐标的有效替代品**，在保持控制精度的同时大幅降低使用门槛和计算成本。这一思路为可控运动生成开辟了“文本即控制”的新路径，但也存在对预标注数据（FineMotion）的依赖，以及对更精细关节（如手指）控制尚未覆盖的局限。



### 可控运动生成的需求与挑战

人类运动生成是计算机视觉与图形学领域的核心问题，其目标是根据给定的条件信号生成逼真且可控的三维人体运动序列。随着扩散模型在运动生成中的成功应用，文本到运动生成（Text-to-Motion）取得了显著进展，但在实际应用中，用户往往不仅需要整体动作的语义符合描述，还希望精确控制特定身体部位在特定时间区间内的运动轨迹。

这一需求催生了可控运动生成（Controllable Motion Generation）这一研究方向。然而，现有方法在实现**精确性、时间感知性和用户友好性**的统一上存在显著瓶颈。

### 现有方法的三条路径及其局限性

当前可控运动生成方法可归纳为三条技术路径，各自存在难以克服的缺陷：

**（一）基于LLM扩展文本的细粒度控制。** 这类方法利用大语言模型将粗粒度文本扩展为包含细粒度动作细节的描述，以此作为控制信号。代表工作如 **CoMo**（Huang et al., ECCV 2024）将身体部位划分为10个区域，通过LLM生成各部位的详细动作描述。然而，该方法存在两个根本性问题：其一，LLM生成的描述缺乏**时间对齐**——无法精确指定某个动作发生的起止时刻；其二，生成的描述常与真实运动存在**事实性偏差**，即LLM“编造”的动作细节与实际运动数据不一致。

**（二）基于空间坐标的精确控制。** 这类方法通过提供身体关节的三维坐标序列作为额外控制信号，实现精确的空间约束。早期工作如 **PriorMDM**（Shafir et al., ICLR 2024）和 **GMD**（Karunratanakul et al., CVPR 2023）仅支持骨盆的坐标控制，而 **OmniControl**（Xie et al., ICLR 2024）和 **InterControl**（Wang et al., NeurIPS 2024）将控制扩展到多个身体部位。尽管这类方法控制精度较高，但其核心缺陷在于：提供精确的3D坐标序列对用户极不直观，且需要额外的姿态转换计算，**计算成本高昂**；更重要的是，这种控制方式高度依赖现有数据集中的标注，难以泛化到开放场景。

**（三）无控制的纯文本生成。** 以 **MDM**（Tevet et al., ICLR 2023）为代表的扩散模型仅接受粗粒度文本作为条件，虽然生成质量较高，但完全不具备对特定身体部位的精确控制能力。

### 核心动机与FineXtrol的切入点

上述分析揭示了一个关键矛盾：**文本控制直观但缺乏精确性和时间对齐，坐标控制精确但不直观且计算代价高**。FineXtrol的核心动机正是弥合这一鸿沟——能否设计一种既保留文本控制的直观性和用户友好性，又具备坐标控制的精确性和时间感知能力的控制范式？

FineXtrol的答案是将**带有明确时间间隔的细粒度文本描述**作为控制信号。例如，给定粗粒度文本“一个人用左腿踢东西”，用户可以指定细粒度控制信号：“在0.5-1.0秒将左腿向右移动”。这种设计的关键优势在于：

1. **时间感知性**：通过显式的时间区间标注（如`<0.5~1.0s>`），使控制信号天然具备时间对齐能力，克服了LLM扩展文本方法的时间模糊性。
2. **精确性与可验证性**：控制信号来源于FineMotion数据集的预标注，而非LLM的自由生成，避免了事实性偏差。
3. **用户友好性**：用户以自然语言描述期望的身体部位动作，无需提供难以直观理解的3D坐标序列。
4. **计算高效性**：避免了坐标控制方法中从坐标到姿态的转换计算开销。

### 技术路线概览

为实现这一目标，FineXtrol在技术层面进行了三项关键设计：

- **控制信号重构**：将人体划分为头、身体、左臂、右臂、左腿、右腿六大部位，为每个部位提供带时间区间的细粒度文本控制信号。
- **层次对比学习**：针对现有文本编码器（如CLIP、T5）对细粒度动作语义区分能力不足的问题，设计句子级、片段级、序列级三层对比学习，增强文本编码器对细粒度控制信号的语义敏感性。
- **双分支ControlNet式架构**：以冻结的MDM分支保持粗粒度文本生成能力，以可训练的控制分支处理细粒度信号，通过零初始化线性层以残差形式注入控制信息，实现生成质量与控制精度的解耦与协同。



## 核心方法与创新机理

FineXtrol 的核心创新在于用**带有明确时间间隔的细粒度文本描述**替代传统方法中不直观且计算昂贵的空间坐标序列，作为运动生成的控制信号。这一转变并非简单的信号替换，而是围绕该信号特性构建了一套完整的控制-生成-编码体系，具体体现在以下三个关键设计：

### 1. 控制信号范式：从空间坐标到时间感知的细粒度文本

传统可控运动生成方法依赖全局 3D 坐标序列（如 **OmniControl** 的关节位置约束、**InterControl** 的空间轨迹），存在两大瓶颈：一是用户难以直观提供精确的空间坐标；二是坐标到姿态的转换计算成本高。基于 LLM 扩展文本的方法（如 **CoMo**）虽更友好，但缺乏显式时间对齐，且 LLM 生成的描述常与真实运动事实不符。

FineXtrol 将控制信号定义为形如 `"Move your right leg forward in 1.0-1.5s"` 的细粒度文本，天然携带**身体部位**、**动作语义**和**时间间隔**三重信息。这使得控制信号既直观可读，又具备精确的时间感知能力，从根本上规避了坐标方法的用户门槛和计算开销。

### 2. 控制注入范式：双分支 ControlNet 式残差调制

仅改变信号类型不足以实现有效控制。若将粗粒度文本与细粒度控制文本直接拼接送入模型（Direct 范式），FID 高达 1.383，R-Top3 仅 0.601，远逊于 FineXtrol 的 0.245 和 0.685（Table 4）。这表明模型难以从拼接文本中自主解耦控制意图。

FineXtrol 采用**双分支 ControlNet 架构**：
- **下分支**：冻结的 **MDM**（Tevet et al., ICLR 2023）原始 Transformer 编码器，负责保持从粗粒度文本 $p$ 生成高质量运动的基础能力；
- **上分支**：可训练的 MDM 副本，接收细粒度控制信号 $c$ 并通过交叉注意力进行条件特征调制；
- **零初始化线性层** $\mathcal{P}_l$：将上分支的输出以残差形式注入下分支对应层，即 $\mathbf{h}_l^{\text{out}} = \mathbf{h}_l^{\text{ori}} + \mathcal{P}_l(\mathbf{h}_l^{\text{ctrl}})$。

零初始化确保训练初期控制分支不引入噪声扰动，随后逐步学习精确的调制信号。这种解耦设计使得模型在保持粗粒度文本生成能力的同时，精确跟随细粒度控制约束。

### 3. 文本编码器增强：层次对比学习

细粒度控制文本涉及“左臂/右腿”等身体部位和“前移/后摆”等细微动作差异，通用文本编码器（如 CLIP、T5）对此类细粒度语义的区分能力不足。直接使用 CLIP 或未微调的 T5 编码控制信号，FID 分别为 0.347 和 0.500，而 FineXtrol 的层次对比学习训练后的 T5 编码器将 FID 降至 0.245（Table 5）。

层次对比学习在三个粒度上增强编码器：
- **句子级**：区分同一时间间隔内不同身体部位的动作描述；
- **片段级**：区分同一身体部位在不同时间间隔的动作序列；
- **序列级**：区分完整控制信号序列的整体语义。

训练采用 InfoNCE 损失 $\mathcal{L}_i = -\log \frac{\exp(\text{sim}(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(z_i, z_k)/\tau)}$，拉近正例对（同一语义的不同增广），推远负例对。消融实验表明，三层联合训练使编码器在表征细粒度文本时，对齐性和均匀性指标均显著优于 CLIP 和原始 T5（Figure 7），且余弦相似度分析证实三层联合训练最能捕捉细粒度语义差异（Table 14）。

### 创新总结

三项创新形成因果链条：**细粒度文本信号**降低了控制的门槛与计算成本；**双分支残差注入**解决了控制信号与生成主干的解耦融合问题；**层次对比学习**弥补了通用文本编码器对细粒度动作语义的感知缺陷。三者协同使得 FineXtrol 在仅 23.39M 可训练参数和 128.57s 推理时间下（Table 3），实现了 0.245 的 FID 和 0.685 的 R-Top3 精度，在控制精度与生成质量上达到或超越基于坐标的 SOTA 方法。



FineXtrol 的整体框架围绕一个核心设计展开：将**细粒度、时间感知的文本控制信号**注入冻结的文本到运动扩散模型，以残差方式实现精确的身体部位运动控制，同时保持原有粗粒度文本的生成能力。

### 输入输出定义

框架的输入由三部分组成：
- **粗粒度文本** $p$：描述整体运动意图，例如“A man kicks something with his left leg.”
- **细粒度文本控制信号** $c$：带有明确时间间隔的身体部位动作描述，例如“Move your left leg to the right in 1.0–1.5s”，未指定的时间区间使用 `<Mask>` 标记
- **噪声运动序列** $\Delta\mathbf{x}_t$：扩散过程中的当前噪声状态

框架输出为预测的干净运动序列 $\mathbf{x}_0$，形式化为：

$$
\mathbf{x}_0 = \mathcal{F}(p, c; \Theta)
$$

其中 $\Theta$ 为框架参数。

### 双分支架构

FineXtrol 采用 ControlNet 式的双分支设计（Figure 2），由以下模块构成：

![[assets/figures/papers/paper_list_l1826_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text/figures/002_Figure_2.jpg]]
*Figure 2: Overview of FineXtrol. Our framework takes the coarse-grained text*

**下分支（冻结的 MDM 分支）**：直接复用原始 MDM（Tevet et al., ICLR 2023）的 Transformer 编码器及预训练权重，保持冻结状态。该分支接收粗粒度文本嵌入 $\mathbf{e}_p$ 与噪声运动嵌入 $\mathbf{e}_{x_t}$ 的拼接作为输入：

$$
\mathbf{e} = [\mathbf{e}_p; \mathbf{e}_{x_t}]
$$

经 Transformer 逐层处理后产生原始特征 $\mathbf{h}_l^{\text{ori}}$：

$$
\mathbf{h}_l^{\text{ori}} = \text{TransformerBlock}_l(\mathbf{h}_{l-1}^{\text{ori}}), \quad \mathbf{h}_0^{\text{ori}} = \mathbf{e}
$$

该分支确保模型在引入控制能力的同时不丧失粗粒度文本到运动的基本生成质量。

**上分支（可训练的控制分支）**：是 MDM 的可训练副本，接收细粒度控制信号 $c$ 作为条件输入。控制信号经层次对比学习微调后的 T5 文本编码器提取嵌入，通过条件特征适配（conditional feature adaptation）调制控制分支各层的特征表示。该分支的核心作用是**从细粒度文本中提取精确的时空控制语义**。

**零初始化线性投影层**：连接两分支的关键组件。控制分支第 $l$ 层的输出 $\mathbf{h}_l^{\text{ctrl}}$ 通过零初始化线性层 $\mathcal{P}_l$ 投影后，以残差形式注入主分支：

$$
\mathbf{h}_l^{\text{out}} = \mathbf{h}_l^{\text{ori}} + \mathcal{P}_l(\mathbf{h}_l^{\text{ctrl}})
$$

零初始化确保训练初期控制分支不引入噪声扰动，随着训练推进逐步学习有效的控制调制。

### 控制信号结构

细粒度控制信号 $c$ 按六个身体部位组织：**头、身体、左臂、右臂、左腿、右腿**（Table 6）。每个部位的控制描述以时间间隔为粒度，形成三层语义结构（Figure 3）：
- **句子级（sentence-level）**：单个时间区间内的具体动作描述
- **片段级（snippet-level）**：若干连续句子的组合
- **序列级（sequence-level）**：整个运动序列的完整控制描述

![[assets/figures/papers/paper_list_l1826_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text/figures/012_Table_6.jpg]]
*Table 6: Controllable body parts and related descriptions*

### 文本编码器的层次对比学习

为增强文本编码器对细粒度动作语义的区分能力，FineXtrol 对 T5 编码器 $\mathcal{E}$ 进行三层次对比学习微调。对于增广后的控制信号 $c_i^{\text{aug}}$ 和 $c_j^{\text{aug}}$，先经编码器提取并平均池化得到嵌入：

$$
h_i = \text{Avg}(\mathcal{E}(c_i^{\text{aug}})), \quad h_j = \text{Avg}(\mathcal{E}(c_j^{\text{aug}}))
$$

再经 MLP 投影头 $g$ 映射到对比空间：

$$
z_i = g(h_i), \quad z_j = g(h_j)
$$

使用 InfoNCE 损失拉近正例对、推远负例对：

$$
\mathcal{L}_i = -\log \frac{\exp(\text{sim}(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(z_i, z_k)/\tau)}
$$

消融实验表明，三层联合训练使文本编码器在捕捉细粒度语义方面显著优于未微调的 CLIP 和 T5（FID 从 0.347 降至 0.245，Table 5），且温度 $\tau=0.07$ 和平均池化策略为最优配置（Table 16）。

### 训练与推理流程

训练时，下分支冻结，仅更新上分支控制网络和零初始化投影层。细粒度控制信号以 50% 的概率随机 Mask 部分时间区间（Table 17 表明该概率最优），迫使模型学会在部分控制信息缺失时仍能合理生成。推理时，框架从随机噪声出发，通过 1000 步去噪迭代生成符合粗粒度文本语义且精确跟随细粒度控制约束的运动序列。



### 问题形式化

FineXtrol将可控运动生成建模为一个条件生成问题。给定粗粒度文本 $p$（如“A man kicks something with his left leg.”）和细粒度文本控制信号 $c$（如“Move your left leg to the right in 1.0-1.5s”），框架 $\mathcal{F}$ 生成与两者一致的运动序列 $\mathbf{x}_0$：

$$\mathbf{x}_0 = \mathcal{F}(\mathbf{p}, \mathbf{c}; \Theta)$$

其中 $\Theta$ 为框架参数。控制信号 $\mathbf{c}$ 的核心特征是**带有明确时间间隔**的身体部位动作描述，替代了传统方法中的空间坐标序列。

### 基础运动扩散模型

FineXtrol复用**MDM**（Tevet et al., ICLR 2023）作为基础生成架构。MDM的训练目标为预测干净运动 $\hat{\mathbf{x}}_0$ 与真实运动之间的均方误差：

$$\mathcal{L}_\theta = \| \epsilon_\theta (\mathbf{x}_t, t, \mathbf{p}; \theta) - \hat{\mathbf{x}}_0 \|_2^2$$

其中 $\mathbf{x}_t$ 为加噪后的运动序列，$t$ 为扩散时间步，$\mathbf{p}$ 为粗粒度文本条件。文本嵌入 $\mathbf{e}_p$ 与运动嵌入 $\mathbf{e}_{x_t}$ 拼接后作为Transformer的输入：

$$\mathbf{e} = [\mathbf{e}_p; \mathbf{e}_{x_t}]$$

### 双分支控制范式

这是FineXtrol的**核心架构创新**。框架包含两个分支：

**下分支（冻结的MDM）**：保持预训练权重不变，负责从粗粒度文本 $\mathbf{p}$ 生成运动特征，维持基础生成能力。其第 $l$ 层Transformer输出为：

$$\mathbf{h}_l^{\text{ori}} = \text{TransformerBlock}_l(\mathbf{h}_{l-1}^{\text{ori}}), \quad \mathbf{h}_0^{\text{ori}} = \mathbf{e}$$

**上分支（可训练的MDM副本）**：接收细粒度控制信号 $\mathbf{c}$ 的嵌入，通过条件特征适配产生调制特征 $\mathbf{h}_l^{\text{ctrl}}$。

两分支通过**零初始化线性投影层** $\mathcal{P}_l$ 交互，以残差形式注入控制信号：

$$\mathbf{h}_l^{\text{out}} = \mathbf{h}_l^{\text{ori}} + \mathcal{P}_l(\mathbf{h}_l^{\text{ctrl}})$$

零初始化的关键作用在于训练初期 $\mathcal{P}_l(\mathbf{h}_l^{\text{ctrl}}) \approx 0$，使得模型从原始MDM行为开始，逐步学习控制信号的调制作用，避免早期噪声干扰。消融实验证实，该范式相比直接将控制文本与粗粒度文本拼接（Direct范式），FID从1.383降至0.245，R-Top3从0.601提升至0.685（Table 4）。

### 层次对比学习模块

为增强文本编码器对细粒度动作语义的区分能力，FineXtrol设计了**三层对比学习**框架，在三个粒度上训练T5编码器 $\mathcal{E}$：

- **句子级**（sentence-level）：单个动作描述，如“Move your right leg forward.”
- **片段级**（snippet-level）：时间间隔内的多个动作组合
- **序列级**（sequence-level）：整个运动序列的完整描述

对每个层级的增广文本对 $(c_i^{\text{aug}}, c_j^{\text{aug}})$，编码后经平均池化得到嵌入：

$$h_i = \text{Avg}(\mathcal{E}(c_i^{\text{aug}})), \quad h_j = \text{Avg}(\mathcal{E}(c_j^{\text{aug}}))$$

随后通过MLP投影头 $g$ 映射到对比空间：

$$z_i = g(h_i), \quad z_j = g(h_j)$$

使用InfoNCE损失拉近正例对、推远负例对：

$$\mathcal{L}_i = -\log \frac{\exp(\text{sim}(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(z_i, z_k)/\tau)}$$

其中 $\tau$ 为温度系数，消融实验确定最优值为 $\tau=0.07$，且平均池化优于最大池化（Table 16）。三层联合训练使编码器在 $\ell_{\text{align}} - \ell_{\text{uniform}}$ 指标上显著优于CLIP和T5（Figure 7），最终将生成FID从0.347降至0.245（Table 5）。

![[assets/figures/papers/paper_list_l1826_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text/figures/010_Figure_7.jpg]]
*Figure 7: Comparison with existing text encoders in representing fine-grained textual control signals. We plot*

### 控制信号结构

细粒度控制信号 $\mathbf{c}$ 采用结构化模板，将人体划分为六大部位：头、身体、左臂、右臂、左腿、右腿。每个控制指令包含时间区间和动作描述，未指定的时间区间使用 `<Mask>` 标记。训练时采用50%的随机Masking概率，消融实验表明该设置在FID（0.245）上显著优于其他概率值（如变化概率的0.408，Table 17）。



## 实验与关键发现

### 主实验结果

FineXtrol在HumanML3D测试集上与多个基线方法进行了全面对比，包括无控制方法MDM（Tevet et al., ICLR 2023）、仅骨盆控制的PriorMDM（Shafir et al., ICLR 2024）和GMD（Karunratanakul et al., CVPR 2023）、多部位坐标控制的OmniControl（Xie et al., ICLR 2024）和InterControl（Wang et al., NeurIPS 2024），以及基于LLM的细粒度文本控制方法CoMo（Huang et al., ECCV 2024）。

**整体生成质量**方面，FineXtrol在Body Part (Average)设置下取得FID 0.245，相比无控制的MDM（0.544）下降54.9%，证明细粒度文本控制信号的引入不仅未损害生成质量，反而显著提升了运动真实性。与基于坐标的方法相比，FineXtrol的FID（0.245）略高于OmniControl的坐标控制模式（0.209），但显著优于CoMo（0.347），差距达0.102。

**文本-运动对齐**方面，FineXtrol的R-Precision Top-3达到0.685，超越MDM（0.611）和所有坐标控制方法，包括OmniControl（0.684）和InterControl（0.671）。MM-Dist指标上，FineXtrol在Left Arm部位取得4.981的最佳值，表明细粒度文本控制信号能有效引导模型生成与粗粒度描述语义一致的运动。

**效率对比**（Table 3）显示，FineXtrol的推理时间为128.57秒，可训练参数量仅23.39M，均为所有扩散式可控运动生成方法中最低。这一效率优势源于文本控制信号避免了复杂的坐标序列处理和姿态转换计算。

**各部位控制效果**（Table 2）的详细结果表明，FineXtrol在六大身体部位（头、身体、左/右臂、左/右腿）上均保持了稳定的控制精度和生成质量，验证了身体部位划分策略的合理性（Table 6）。

### 与CoMo的用户研究对比

用户研究（Figure 5）设置了8个案例，其中2个不含细粒度控制信号，6个包含。结果显示：
- 在包含细粒度控制信号的案例中，FineXtrol在75.76%的情况下被参与者偏好，证明其生成的运动在控制信号对齐度和运动自然性上均优于CoMo。
- 在不含控制信号的案例中，两者表现接近，FineXtrol仍保持轻微优势。

![[assets/figures/papers/paper_list_l1826_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text/figures/007_Figure_5.jpg]]
*Figure 5: The statistical results of the user study. The left pie chart displays the average preference ratio for the visualized motion sequences without fine-grained textual control signals (2 cases) of our FineXtrol and CoMo. The right one shows that with fine-grained textual control signals (6 cases). Each case is evaluated based on (1) alignment with control signals and (2) motion naturalness*

定性对比（Figure 6）以右腿控制为例，展示了FineXtrol能精确执行“右腿前移→后移→脚尖点地→前移屈膝→后移”的时间序列指令，而CoMo的运动轨迹与控制信号存在明显偏差。

![[assets/figures/papers/paper_list_l1826_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text/figures/009_Figure_6.jpg]]
*Figure 6: A motion pair comparing right leg control in the user study. Body part movements in unspecified intervals are not explicitly controlled*

### 消融实验

#### 控制范式消融（Table 4）

![[assets/figures/papers/paper_list_l1826_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text/figures/011_Table_4.jpg]]
*Table 4: Ablation study on control paradigm. Our control paradigm significantly outperforms the ‘Direct’ paradigm, which directly connects coarse-grained text and fine-grained textual control signals as a single input*

对比双分支ControlNet式残差注入与直接拼接控制文本的Direct范式：
- Direct范式的FID高达1.383，R-Top3仅0.601，表明简单拼接粗粒度文本和细粒度控制信号会严重破坏生成质量。
- FineXtrol的双分支设计通过零初始化线性层以残差形式注入控制信号（$h_l^{out} = h_l^{ori} + P_l(h_l^{ctrl})$），将FID降至0.245，R-Top3提升至0.685，验证了解耦设计的必要性。

#### 文本编码器消融（Table 5, Figure 7）

![[assets/figures/papers/paper_list_l1826_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text/figures/008_Table_5.jpg]]
*Table 5: Ablation study on different text encoders. The controllable motion generation performance with our text encoder significantly surpasses those with CLIP and T5, proving the effectiveness of our hierarchical contrastive learning module for fine-grained textual control signals*

对比CLIP、未微调T5和经层次对比学习训练的T5：
- 使用CLIP时FID为0.347，T5为0.500，而FineXtrol的层次对比学习编码器将FID降至0.245。
- Figure 7通过ℓ_align - ℓ_uniform指标量化了不同编码器对细粒度文本信号的区分能力：FineXtrol编码器的嵌入在正例对中高度对齐，负例对中均匀分布，显著优于CLIP和T5。

#### 层次对比学习消融（Table 14, Table 15）

![[assets/figures/papers/paper_list_l1826_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text/figures/023_Table_14.jpg]]
*Table 14: Ablation study on hierarchical training in the proposed contrastive learning module. We evaluate text encoders trained with different combinations of contrastive learning levels by extracting embeddings for 10,000 randomly sampled positive (Pos.) and negative (Neg.) pairs from each level of textual descriptions, and computing their average cosine similarity. The results indicate that incorporating all three levels of contrastive learning enables the text encoder to best capture the semantics of fine-grained textual descriptions, resulting in better embeddings of our fine-grained textual control signals*

消融句子级、片段级、序列级三个层次的对比学习：
- 仅使用单一层次训练时，文本嵌入的正负例余弦相似度区分度不足。
- 三层联合训练使编码器在三个信息粒度上均获得最佳语义捕捉能力，生成性能（FID, R-Top3）显著优于任何子集组合。

#### 控制信号密度影响（Table 10, Table 11）

随着控制信号密度从25%增至100%，FineXtrol的性能稳定提升（FID持续下降），而OmniControl在密度过高时因坐标约束过强导致生成质量退化。这表明文本控制信号比坐标约束具有更好的可扩展性。

#### 其他关键消融

- **Masking概率**（Table 17）：50%的固定Masking概率训练效果最优（FID 0.245），全Mask或零Mask均导致性能下降（FID升至0.408）。
- **对比学习超参**（Table 16）：温度τ=0.07和平均池化策略在正例对余弦距离上取得最优值。



### 失败模式与局限性

1. **数据依赖性**：控制信号依赖FineMotion预标注数据，对新颖动作或未标注数据的适用性未知。若目标动作超出训练数据的细粒度描述范围，控制精度可能下降。
2. **部位粒度限制**：身体部位仅划分为六大区域（头、身体、左/右臂、左/右腿），未覆盖手指、脚趾等更精细关节的控制。对于需要手部精细操作的运动（如弹钢琴、打字），当前方法无法提供有效控制。
3. **时间间隔精度**：尽管引入了时间感知的控制信号，但缺乏对时间边界严格精度的定量评估。在极端短间隔或重叠间隔场景下的鲁棒性有待验证。

### 待解决问题

- 如何将控制信号扩展到更精细的关节级别（如手指、面部表情）？
- 能否自动生成时间对齐的细粒度文本描述，以减少对人工标注的依赖？
- 在开放域文本或更长运动序列（如数分钟的动作序列）中的控制能力如何？
- 层次对比学习的三层设计是否存在更优的信息粒度划分策略？

### 补充图表

![[assets/figures/papers/paper_list_l1826_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text/figures/005_Table_3.jpg]]
*Table 3: Inference time and the number of trainable parameters of diffusion-based controllable motion generation methods. ‘Coord.’ is short for coordinate*

![[assets/figures/papers/paper_list_l1826_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text/figures/006_Table_2.jpg]]
*Table 2: Detailed results of controlling specific body parts*



## 定位与知识库关联

### 一、可控运动生成的演进路径

FineXtrol 处于**可控人体运动生成**这一研究脉络的交叉点上。根据控制信号的类型，现有方法可大致分为三条技术路线：

**（1）基于空间坐标的控制。** 此类方法以 3D 关节坐标序列作为额外控制信号，直接约束目标身体部位的空间轨迹。代表性工作包括 **PriorMDM**（Shafir et al., ICLR 2024）和 **GMD**（Karunratanakul et al., CVPR 2023），二者仅支持骨盆（pelvis）单一部位的控制；**OmniControl**（Xie et al., ICLR 2024）和 **InterControl**（Wang et al., NeurIPS 2024）进一步扩展至多部位控制。这类方法的根本瓶颈在于：控制信号（3D 坐标序列）高度依赖现有数据集，难以泛化到开放场景；同时，姿态转换带来高计算开销，且对普通用户极不友好。

**（2）基于 LLM 扩展的细粒度文本控制。** **CoMo**（Huang et al., ECCV 2024）是这一路线的代表，利用大语言模型将粗粒度文本扩展为细粒度描述，再以文本形式注入运动生成模型。然而，LLM 生成的描述常与真实运动事实不一致（hallucination），且缺乏显式的时间对齐信息，导致控制精度不足。

**（3）FineXtrol 的定位：时间感知的细粒度文本控制。** FineXtrol 在控制信号的**模态**（文本 vs. 坐标）和**时间精度**两个维度上同时做出改进。它引入了带有明确时间间隔的细粒度文本描述（如“在 1.0-1.5s 将左腿向右移动”）作为控制信号，既保留了文本控制的直观性和用户友好性，又通过显式时间戳弥补了 CoMo 等方法的时序模糊缺陷。在推理效率上，FineXtrol 的可训练参数量（23.39M）和推理时间（128.57s）均为对比方法中最低（Table 3），显著优于 OmniControl 等基于坐标的方法。

### 二、技术架构的谱系归属

从架构设计角度看，FineXtrol 继承并改造了两条成熟的技术范式：

**（1）ControlNet 式双分支残差注入。** FineXtrol 的控制注入机制直接借鉴了 ControlNet 的设计哲学——冻结预训练的主干网络（MDM 分支），训练一个可学习的副本（控制分支），通过零初始化线性层以残差形式注入调制信号。这一设计的因果效应在 Table 4 中得到验证：相比直接拼接控制文本的“Direct”范式（FID = 1.383, R-Top3 = 0.601），双分支残差注入将 FID 降至 0.245，R-Top3 提升至 0.685，证明了解耦设计对保持生成质量和精确跟随控制约束的双重收益。

**（2）层次对比学习的文本编码器增强。** FineXtrol 对 T5 文本编码器施加了三层对比学习（句子级、片段级、序列级），以增强其对细粒度动作语义的区分能力。这一设计与 SimCLR 等自监督对比学习框架同源，但其创新在于将对比层次与运动描述的粒度对齐。Table 5 和 Figure 7 的消融实验表明，层次对比学习训练后的编码器在 FID 上较 CLIP 改善 0.102，较未微调的 T5 改善 0.255，且对齐性-均匀性指标（ℓ_align - ℓ_uniform）显著优于现有编码器。

### 三、适用边界与关键局限

**（1）数据依赖性。** FineXtrol 的控制信号依赖于 FineMotion 数据集的预标注。该数据集通过自动标注流程为 HumanML3D 中的运动序列生成了时间对齐的细粒度文本描述。这意味着模型对新颖动作类别或未标注数据的控制能力尚未验证——若目标动作的语义不在 FineMotion 的描述空间中，控制信号可能无法被正确编码。

**（2）身体部位粒度有限。** 当前版本仅将人体划分为六大区域（头、身体、左/右臂、左/右腿），未覆盖手指、脚趾等更精细关节。Table 2 中各部位的控制精度差异（如左臂 MM-Dist 达 4.981，而其他部位可能较低）暗示，部位划分的粗细直接影响控制效果的上限。

**（3）控制信号密度与性能的关系。** Table 10 和 Table 11 揭示了一个有趣的现象：随着控制信号密度增加（25% → 100%），FineXtrol 的性能稳定提升，而 OmniControl 则因坐标约束过强而退化。这表明文本控制信号具有更好的“柔性”——但同时也意味着，在极高密度控制下，文本信号的歧义性可能成为新的瓶颈。

### 四、开放问题与未来方向

基于上述分析，FineXtrol 打开的开放问题包括：

- **关节级控制的扩展。** 能否将六大部位进一步细化为手指、手腕、脚踝等级别？这需要更细粒度的标注数据，以及能够区分微动作语义的文本编码器。
- **自动时间对齐标注。** 当前依赖 FineMotion 的离线标注流程。能否利用视频-语言模型或运动-语言对齐技术，自动生成时间感知的细粒度文本，从而摆脱人工标注依赖？
- **开放域泛化。** 在 HumanML3D 之外的更长序列、更复杂动作（如舞蹈、体育）上的控制能力如何？文本控制信号的语义覆盖范围是否需要扩充？
- **与 LLM 的深度整合。** CoMo 的失败源于 LLM 生成文本的事实不一致，而非 LLM 本身无用。能否将 FineXtrol 的层次对比编码器与 LLM 的生成能力结合，实现“用户自由描述 → LLM 生成时间对齐信号 → FineXtrol 精确执行”的完整链路？

*注：以上开放问题基于论文自身讨论的局限性和方法设计空间推断，部分结论需待后续工作验证。*



## 原文 PDF

![[paperPDFs/AAAI_2026/FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text.pdf]]
