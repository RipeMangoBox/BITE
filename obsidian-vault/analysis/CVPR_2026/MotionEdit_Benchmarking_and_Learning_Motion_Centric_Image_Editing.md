---
title: MotionEdit Benchmarking and Learning Motion Centric Image Editing
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing.pdf
project_link: https://motion-edit.github.io
code_link: null
aliases:
- MBLMCIE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将光流对齐信号作为奖励函数引入 DiffusionNFT 后训练框架，通过计算输入-输出与输入-真实目标间的光流一致性（幅度、方向、运动幅度正则化），显式指导模型学习正确的运动变换。
primary_logic: 通过光流奖励直接量化预测运动与真实运动的几何对齐程度，并结合语义奖励（MLLM），能够在不牺牲一般编辑能力的前提下，显著提升模型对运动指令的空间理解能力和编辑忠实度。
claims:
- MotionNFT 将 FLUX.1 Kontext 在 MotionEdit-Bench 上的综合生成质量（Overall）从 3.84 提升到 4.25（+10.68%），运动对齐分数（MAS）从 53.73 提升到 55.45，胜率达到 64.95%（基线 57.71%）。
- "光流奖励与 MLLM 奖励的均衡组合（0.5:0.5）在所有指标上均优于纯 MLLM 奖励或纯光流奖励，验证了两种奖励的互补性。"
- 训练过程中，仅使用 MLLM 奖励会导致运动对齐分数（MAS）中途退化，而加入光流奖励的 MotionNFT 能持续稳定提升 MAS，防止过度拟合语义信号。
- MotionEdit 数据集具有比现有数据集（MagicBrush、OmniEdit 等）大 5.8 倍的运动幅度变化，提供了更具挑战性的运动编辑基准。
---

# MotionEdit Benchmarking and Learning Motion Centric Image Editing

> [!tip] 核心洞察
> 通过光流奖励直接量化预测运动与真实运动的几何对齐程度，并结合语义奖励（MLLM），能够在不牺牲一般编辑能力的前提下，显著提升模型对运动指令的空间理解能力和编辑忠实度。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionEdit：面向运动中心化图像编辑的基准测试与学习 |
| 英文题名 | MotionEdit Benchmarking and Learning Motion Centric Image Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [Project](https://motion-edit.github.io) · [paper](https://arxiv.org/abs/2512.10284) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionNFT |
| Dataset | MotionEdit-Bench |

> [!tip] 效果简介
> - MotionEdit-Bench 上，Overall (生成质量) 4.25 vs 3.84 (+0.41 (+10.68%))；MAS (运动对齐分数) 55.45 vs 53.73 (+1.72)；Win Rate (胜率) 64.95 vs 57.71 (+7.24)。

## 概要

图像编辑模型在风格迁移、物体替换等**静态外观修改**上已取得显著进展，但在涉及**对象动作、姿态变化、交互关系**等运动编辑任务时，现有方法普遍失效。其根本瓶颈在于：训练与评估数据中缺乏高质量的运动编辑监督——现有数据集要么仅关注外观改变，要么包含少量低质量、不忠实的运动编辑样本，导致模型难以建立准确的空间-运动理解能力。

针对这一空白，本文提出 **MotionEdit** 基准数据集与 **MotionNFT** 训练框架。MotionEdit 通过视频帧对挖掘管线，构建了包含 10,157 个运动编辑样本的数据集，其运动幅度变化是 MagicBrush、OmniEdit 等现有数据集的 **5.8 倍**（Figure 6），涵盖姿态变换、位移、视角变化、主客体交互等六类运动编辑子类别。MotionNFT 则在 DiffusionNFT 后训练框架中引入**光流对齐奖励**，通过计算输入-编辑图像与输入-真实目标间的光流一致性（幅度、方向、运动幅度正则化），显式指导模型学习正确的运动变换，并与 MLLM 语义奖励形成互补。

实验表明，MotionNFT 将 **FLUX.1 Kontext** 在 MotionEdit-Bench 上的综合生成质量从 3.84 提升至 **4.25（+10.68%）**，运动对齐分数（MAS）从 53.73 提升至 55.45，胜率达到 64.95%（基线 57.71%）（Table 1）。在 **Qwen-Image-Edit** 上同样取得一致的性能增益。关键消融实验揭示：纯 MLLM 奖励训练会导致 MAS 在约 150 步后退化，而加入光流奖励的 MotionNFT 能持续稳定提升运动对齐能力（Figure 9, Figure 10），验证了**几何信号防止语义过拟合**的核心机制。同时，在 ImgEdit-Bench 通用编辑基准上，MotionNFT 保持甚至略微提升了整体编辑能力（Table 2），证明运动奖励的引入并未牺牲一般编辑性能。

在方法定位上，MotionNFT 属于**强化学习驱动的扩散模型后训练**方法，其核心创新在于将光流几何对齐信号量化为可优化的奖励函数，与 MLLM 语义奖励以 0.5:0.5 的权重组合使用（Table 4），从而在不增加推理开销的前提下，显著提升模型对运动指令的空间理解与编辑忠实度。



### 图像编辑的现状与运动编辑的缺位

图像编辑技术近年来取得了显著进展，基于扩散模型（Diffusion Models）和流匹配模型（Flow Matching Models）的方法在语义理解与生成质量上不断刷新记录。然而，现有研究与实践几乎全部聚焦于**静态外观编辑**——改变对象的颜色、纹理、风格或替换背景元素，而忽视了另一类普遍且关键的编辑需求：**运动编辑（Motion Editing）**。运动编辑要求模型根据自然语言指令，改变图像中主体的动作、姿态、空间位置或与环境的交互关系，例如“让猫从桌上跳下来”、“使舞者抬起左臂”。这类编辑不仅需要理解语义内容，更要求模型具备**空间变换推理能力**，能够准确执行指令所描述的运动轨迹与幅度。

### 现有数据集与方法的根本瓶颈

运动编辑能力缺失的**根本原因**在于训练和评估数据中缺乏高质量的运动编辑监督信号。现有主流编辑数据集（如 MagicBrush、OmniEdit 等）存在两类结构性缺陷：

1. **编辑类型单一**：绝大多数样本仅涉及外观属性的修改，几乎不包含运动变换。这使得模型在训练过程中从未学习过“如何移动对象”。
2. **运动样本质量低下**：少数数据集虽然包含动作变化样本，但这些样本往往存在严重的伪影、身份失真或运动幅度过小的问题，无法提供有效的学习信号。如 **Figure 6** 所示，MotionEdit 数据集的平均运动幅度达到 0.19，是 MagicBrush 和 OmniEdit 等现有数据集的 **5.8 倍**，这从定量角度揭示了此前基准中运动编辑挑战性的严重不足。

数据端的缺失直接导致了模型端的失效。如 **Figure 3** 的定性对比所示，当前最先进的编辑模型（包括 UniWorld-V1、FLUX.1 Kontext 等）在面对运动编辑指令时普遍出现两类典型失败模式：要么**完全忽略运动指令**，仅执行外观修改或保持原图不变；要么在尝试改变姿态时产生**严重的身份失真**，使编辑结果不可用。这一现象表明，仅依靠现有的语义理解能力，模型无法自发地习得运动编辑所需的几何推理能力。

### 本文的核心动机与解决思路

基于上述分析，本文的核心动机可概括为：**为运动中心化的图像编辑建立专门的基准与方法，填补从“外观编辑”到“运动编辑”的能力鸿沟**。具体而言，本文从两个层面回应这一挑战：

- **数据层面**：构建 **MotionEdit 数据集**，这是首个大规模、高质量的运动编辑数据集。通过视频驱动的数据挖掘管线，从动态视频序列中自动提取帧对并生成运动编辑指令，确保样本具有显著的、自然的运动变化，涵盖姿态变换、位移运动、视角变化、主体-物体交互及主体间交互等六类运动模式。
- **方法层面**：提出 **MotionNFT（Motion-guided Negative-aware Fine-Tuning）** 后训练框架。其核心洞察在于：**通过光流奖励直接量化预测运动与真实运动的几何对齐程度，能够在不牺牲一般编辑能力的前提下，显著提升模型对运动指令的空间理解能力和编辑忠实度**。MotionNFT 将光流对齐信号作为奖励函数引入 DiffusionNFT 训练框架，通过计算输入-编辑图像与输入-真实目标图像间的光流一致性（幅度、方向、运动幅度正则化），显式地指导模型学习正确的运动变换，从而弥补了纯语义奖励无法捕捉几何精度的固有局限。



## 核心方法与创新机理

### 创新动因：运动编辑的瓶颈与因果开关

现有图像编辑模型在运动编辑（对象姿态、动作、交互变化）上表现不佳，其根本瓶颈并非模型架构本身，而是**训练与评估数据中缺乏高质量的运动编辑监督**。当前主流编辑数据集（如 MagicBrush、OmniEdit 等）要么仅关注静态外观改变，要么包含少量低质量、不忠实的运动编辑样本，导致模型无法学习到准确、连贯的运动变换能力。这一瓶颈直接催生了 MotionEdit 数据集和 MotionNFT 训练框架的双重创新。

MotionNFT 的核心因果开关在于：**将光流对齐信号作为奖励函数引入 DiffusionNFT 后训练框架**。通过显式计算输入-输出与输入-真实目标间的光流一致性（幅度、方向、运动幅度正则化），模型获得了直接量化预测运动与真实运动几何对齐程度的信号。这一信号与语义奖励（MLLM）形成互补，在不牺牲一般编辑能力的前提下，显著提升了模型对运动指令的空间理解能力和编辑忠实度。

### 方法谱系与知识库定位

MotionNFT 建立在 **DiffusionNFT** 的后训练范式之上，该范式原本仅依赖 MLLM 语义奖励进行强化学习微调。MotionNFT 的关键改造在于**奖励函数的维度扩展**——从单一的语义维度扩展为语义+几何双维度。

在基线模型选择上，MotionNFT 以 **FLUX.1 Kontext** 和 **Qwen-Image-Edit** 两个 Flow Matching 基座模型为骨干，与以下代表性编辑方法形成对比：

- **扩散编辑基线**：Instruct-P2P、AnyEdit、MagicBrush、UltraEdit —— 这些方法在运动编辑任务上表现较弱，根本原因在于其训练数据缺乏运动监督。
- **强化学习编辑基线**：UniWorld-V1 —— 采用纯 MLLM 奖励训练，在运动对齐上存在过拟合语义信号的风险。
- **单步/高效编辑基线**：Step1X-Edit、BAGEL —— 在 MotionEdit-Bench 上展现了相对较强的运动编辑能力，但仍不及 MotionNFT。

### 核心 Changed Slot：奖励函数的重构

MotionNFT 对 DiffusionNFT 框架的核心改造集中于**奖励函数的组成与计算方式**，具体变化如下：

| 奖励维度 | 基线方案（UniWorld-V2） | MotionNFT 方案 | 功能角色 |
|---------|----------------------|---------------|---------|
| 语义奖励 | 100% MLLM 奖励 | 50% MLLM 奖励 | 评估语义保真度、保持度、连贯性 |
| 运动奖励 | 无 | 50% 光流运动奖励 | 量化预测运动与真实运动的几何对齐 |

光流运动奖励的计算包含三个互补组件：

1. **运动幅度一致性**（$\mathcal{D}_{\mathrm{mag}}$）：使用稳健 L1 距离衡量预测光流与真实光流幅度的差异，通过指数 $q$ 抑制离群值的影响。

2. **运动方向一致性**（$\mathcal{D}_{\mathrm{dir}}$）：以真实运动幅度为权重，计算单位向量的余弦方位误差，确保大运动区域的方位准确性得到优先保障。

3. **运动幅度正则化**（$M_{\mathrm{move}}$）：惩罚预测运动幅度远小于真实运动的情形，防止模型退化为静态编辑。

三者加权组合形成总偏差 $\mathcal{D}_{\mathrm{comb}} = \alpha \mathcal{D}_{\mathrm{mag}} + \beta \mathcal{D}_{\mathrm{dir}} + \lambda_{\mathrm{move}} M_{\mathrm{move}}$，再转化为离散奖励（量化为 6 级：$\{0.0, 0.2, 0.4, 0.6, 0.8, 1.0\}$），与 MLLM 奖励按 0.5:0.5 权重混合后送入 DiffusionNFT 训练循环。

### 创新验证：消融实验的关键证据

**奖励组合的必要性**（Table 4）：纯光流奖励（1.0 Motion）导致 Overall 降至 3.60（低于基线的 3.84），表明几何线索单独不足以维持语义保真度；纯 MLLM 奖励（1.0 MLLM）得到 4.20，仍低于组合方案的 4.25。这验证了两种奖励信号的互补性——语义奖励保障整体编辑质量，运动奖励提供精确的空间引导。

**防止语义过拟合**（Figure 9, Figure 10）：训练过程中，仅使用 MLLM 奖励的模型在大约 150 步后出现运动对齐分数（MAS）退化，而 MotionNFT 的 MAS 持续稳定上升。这表明额外的运动指导有效防止了模型对语义信号的过拟合，使运动编辑能力持续改善而非中途衰退。

**通用编辑能力的保持**（Table 2）：在 ImgEdit-Bench 通用编辑基准上，MotionNFT 将 FLUX.1 Kontext 的 Overall 从 3.26 提升至 3.50，证明运动奖励的引入不仅没有牺牲一般编辑性能，反而带来了轻微增益。

### 局限与未解决问题

尽管 MotionNFT 在运动编辑上取得了显著提升，以下挑战仍然存在：

- **多主体空间分配**：在包含多个非编辑主体的复杂场景中，模型难以精确地对目标主体执行运动编辑，同时保持其他主体的身份和位置不变。
- **复杂 3D 交互**：当指令涉及物体遮挡、远距离位移等复杂空间交互时，所有模型（包括 MotionNFT）均出现运动对齐失败或几何失真。
- **身份保持漂移**：在背景复杂或主体纹理相似时，编辑后可能出现外观漂移，尤其在处理多主体交互时更为明显。
- **极端运动鲁棒性**：光流奖励对快速运动、运动模糊等极端情形的鲁棒性还有待探索。

这些局限指向未来的研究方向：融合物理或运动学先验（如关节约束、场景深度）以改进复杂姿态编辑的合理性；引入更强的身份嵌入机制以实现高保真身份保持；以及探索对极端运动条件更鲁棒的几何对齐度量。



MotionNFT 是一个面向运动中心化图像编辑的后训练框架，其核心思想是将光流几何对齐信号显式引入扩散模型的奖励微调过程。该框架建立在 **DiffusionNFT**（一种面向流匹配模型的负感知微调方法）之上，通过扩展其奖励函数，使模型在训练中不仅接收语义质量反馈，还获得关于运动方向与幅度的几何指导。

### 模块架构与数据流

MotionNFT 的整体管线由四个关键模块串联构成，形成“生成—评估—训练”的闭环：

1. **基座编辑模型**：采用基于流匹配（Flow Matching）的扩散编辑模型作为生成器，具体包括 **FLUX.1 Kontext** 和 **Qwen-Image-Edit**。给定输入图像 $I_{\text{orig}}$ 和编辑指令 $c$，模型生成候选编辑图像 $I_{\text{edited}}$。

2. **光流运动奖励计算**：利用预训练的光流估计器 **UniMatch**，分别计算输入-编辑图像对 $(\tilde{\mathbf{V}}_{\text{pred}})$ 和输入-真实目标图像对 $(\tilde{\mathbf{V}}_{\text{gt}})$ 之间的光流场。在此基础上，计算三个几何一致性指标：
   - **运动幅度一致性** $\mathcal{D}_{\text{mag}}$：衡量预测光流与真实光流在幅度上的稳健 L1 偏差；
   - **运动方向一致性** $\mathcal{D}_{\text{dir}}$：以真实运动幅度为权重，计算单位向量的余弦方位误差；
   - **运动幅度正则化** $M_{\text{move}}$：惩罚预测运动幅度远小于真实运动的情形，防止模型退化为静态编辑。

   三者加权组合形成总偏差 $\mathcal{D}_{\text{comb}} = \alpha \mathcal{D}_{\text{mag}} + \beta \mathcal{D}_{\text{dir}} + \lambda_{\text{move}} M_{\text{move}}$，再转换为连续奖励 $r_{\text{cont}}$，最终量化为 6 级离散奖励 $r_{\text{motion}} \in \{0.0, 0.2, 0.4, 0.6, 0.8, 1.0\}$。

3. **MLLM 语义奖励计算**：使用 **Qwen2.5-VL** 在线评分，评估编辑结果的语义质量，包括编辑保真度、身份保持度和视觉连贯性，提供与光流奖励互补的语义反馈。

4. **DiffusionNFT 训练循环**：将光流运动奖励 $r_{\text{motion}}$ 与 MLLM 奖励以 0.5:0.5 的比例组合为最终奖励 $r^{\text{raw}}$。该奖励经优效度归一化后，映射到 $[0,1]$ 区间：
   $$r(x_0,c) = \frac{1}{2} + \frac{1}{2} \mathrm{clip}\left[ \frac{r^{\text{raw}}(x_0,c) - \mathbb{E}[r^{\text{raw}}]}{Z_c}, -1, 1 \right]$$
   训练时，模型同时学习正速度 $v_{\theta}^{+}$（朝向高奖励方向）和负速度 $v_{\theta}^{-}$（远离低奖励方向），通过对比损失更新参数：
   $$\mathcal{L}(\theta) = \mathbb{E}_{c, \pi^{\text{old}}(x_0 \mid c), t} \Big[ r \| v_{\theta}^{+}(x_t, c, t) - v \|_2^2 + (1 - r) \| v_{\theta}^{-}(x_t, c, t) - v \|_2^2 \Big]$$
   其中正负速度通过插值与外推定义：
   $$v_{\theta}^{+} = (1-\beta)v^{\text{old}} + \beta v_{\theta},\quad v_{\theta}^{-} = (1+\beta)v^{\text{old}} - \beta v_{\theta}$$

### 关键设计决策

- **双奖励互补机制**：光流奖励提供显式的几何约束，防止模型仅拟合语义信号而忽略运动准确性；MLLM 奖励则保证编辑结果的视觉质量和语义保真度。消融实验（Table 4）证实，纯光流奖励（1.0 Motion）会导致生成质量下降（Overall 3.60 vs 基线 3.84），纯 MLLM 奖励（1.0 MLLM）虽提升至 4.20，但仍不及组合奖励的 4.25，验证了两者的互补性。

- **奖励量化策略**：将连续运动奖励量化为 6 个离散级别，有助于稳定训练信号，避免微小光流差异导致的奖励波动。

- **训练稳定性**：如 Figure 9 和 Figure 10 所示，仅使用 MLLM 奖励的训练在约 150 步后运动对齐分数（MAS）开始退化，而 MotionNFT 的 MAS 持续上升，表明光流奖励有效防止了对语义信号的过拟合。

### 补充图表

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/005_Figure_4.jpg]]
*Figure 4: MotionEdit’s data construction pipeline. We segment raw videos, extract frame pairs, and automatically filter them using annte Int ose MLLM data quality judge. For all kept pairs, we use a MLLM rewrite module to generate clean, motion-focused editing instructions. Our“Make Doraemon and the boy turn their bodies and heads to face each other “Change the character's pose: straighten body from a slight crouch to an upright, “Have the female dental professional turn aw pipeline enables scalable construction of high-quality motion editing data and can be extended to much larger video corpora*

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/009_Figure_7.jpg]]
*Figure 7: MotionNFT’s Reward Scoring pipeline. For each sampled model-edited image, we measure the alignment between the input-generated optical flow and the input-ground truth optical flow, obtaining the final reward score*



### 基座模型：基于流匹配的编辑框架

MotionNFT 建立在流匹配模型（Flow Matching Models, FMMs）之上。与 DDPM 的噪声预测范式不同，FMMs 将生成过程重新表述为学习一个确定性速度场 $v$，该速度场将噪声隐变量 $z_t$ 沿直线路径传输至其干净对应物。给定条件 $c$（由输入图像和编辑指令构成），模型预测速度 $v_\theta(x_t, c, t)$，其中 $x_t$ 为时间步 $t$ 的带噪隐变量。

### 后训练框架：DiffusionNFT 的扩展

MotionNFT 的核心训练框架继承自 **DiffusionNFT**（一种面向扩散/流匹配模型的强化微调方法），并在此基础上引入了运动感知的奖励信号。DiffusionNFT 的关键创新在于同时学习两个速度方向：

- **正速度** $v_{\theta}^{+}$：模型应当趋近的方向，对应高奖励样本的生成路径；
- **负速度** $v_{\theta}^{-}$：模型应当远离的方向，对应低奖励样本的生成路径。

正负速度通过当前策略速度 $v_{\theta}$ 与旧策略速度 $v^{\mathrm{old}}$ 的线性插值/外推定义：

$$v_{\theta}^{+}(x_t, c, t) = (1 - \beta) v^{\mathrm{old}}(x_t, c, t) + \beta v_{\theta}(x_t, c, t)$$

$$v_{\theta}^{-}(x_t, c, t) = (1 + \beta) v^{\mathrm{old}}(x_t, c, t) - \beta v_{\theta}(x_t, c, t)$$

其中 $\beta$ 控制插值/外推的强度。

### 训练目标函数

DiffusionNFT 的训练损失函数为：

$$\mathcal{L}(\theta) = \mathbb{E}_{c, \pi^{\mathrm{old}}(x_0 \mid c), t} \Big[ r \| v_{\theta}^{+}(x_t, c, t) - v \|_2^2 + (1 - r) \| v_{\theta}^{-}(x_t, c, t) - v \|_2^2 \Big]$$

其中 $r \in [0, 1]$ 为归一化后的奖励值。该损失函数的核心机制是：当奖励 $r$ 较高时，损失主要约束正速度逼近真实速度 $v$，推动模型向高奖励区域移动；当奖励 $r$ 较低时，损失主要约束负速度逼近真实速度，推动模型远离低奖励区域。这种正负速度的对比学习机制使得模型能够更精细地利用奖励信号的梯度信息。

### 奖励归一化：优效度变换

为稳定训练，原始奖励 $r^{\mathrm{raw}}(x_0, c)$ 需要经过优效度归一化（optimality normalization）转换到 $[0, 1]$ 区间：

$$r(x_0, c) = \frac{1}{2} + \frac{1}{2} \mathrm{clip}\left[ \frac{r^{\mathrm{raw}}(x_0, c) - \mathbb{E}_{\pi^{\mathrm{old}}(\cdot|c)}[r^{\mathrm{raw}}(x_0, c)]}{Z_c}, -1, 1 \right]$$

其中 $\mathbb{E}_{\pi^{\mathrm{old}}(\cdot|c)}[r^{\mathrm{raw}}]$ 为旧策略下相同条件 $c$ 的期望奖励，$Z_c$ 为条件相关的归一化常数。该变换将奖励映射为以 0.5 为中心的对称分布，使得正负速度损失权重均衡。

### 运动对齐奖励：光流一致性度量

MotionNFT 的核心贡献在于构建了基于光流的运动对齐奖励函数。给定三元组 $(I_{\mathrm{orig}}, I_{\mathrm{edited}}, I_{\mathrm{gt}})$（原始图像、模型编辑图像、真实目标图像），利用预训练光流估计器 UniMatch 计算两组光流场：

- $\tilde{\mathbf{V}}_{\mathrm{pred}}$：从 $I_{\mathrm{orig}}$ 到 $I_{\mathrm{edited}}$ 的预测运动流；
- $\tilde{\mathbf{V}}_{\mathrm{gt}}$：从 $I_{\mathrm{orig}}$ 到 $I_{\mathrm{gt}}$ 的真实运动流。

运动对齐奖励由三个分量加权组合而成：

#### （1）运动幅度一致性 $\mathcal{D}_{\mathrm{mag}}$

$$\mathcal{D}_{\mathrm{mag}} = \frac{1}{HW}\sum_{i,j} (\|\tilde{\mathbf{V}}_{\mathrm{pred}}(i,j) - \tilde{\mathbf{V}}_{\mathrm{gt}}(i,j)\|_1 + \varepsilon)^q$$

采用稳健 L1 距离逐像素衡量预测光流与真实光流幅度的差异。指数 $q$（默认 $q < 1$）用于抑制大误差离群值的影响，$\varepsilon$ 为小常数防止数值不稳定。

#### （2）运动方向一致性 $\mathcal{D}_{\mathrm{dir}}$

$$\mathcal{D}_{\mathrm{dir}} = \frac{\sum_{i,j} w(i,j) e_{\mathrm{dir}}(i,j)}{\sum_{i,j} w(i,j) + \varepsilon}$$

其中 $w(i,j) = \|\tilde{\mathbf{V}}_{\mathrm{gt}}(i,j)\|_2$ 以真实运动幅度为权重，使大运动区域对方向误差更敏感；$e_{\mathrm{dir}}(i,j)$ 为单位向量的余弦方位误差。该设计确保模型优先学习显著运动区域的方向正确性，而非在静止背景上过度优化。

#### （3）运动幅度正则化 $M_{\mathrm{move}}$

$$M_{\mathrm{move}} = \max\{0, \tau + \frac{1}{2} \bar{m}_{\mathrm{gt}} - \bar{m}_{\mathrm{pred}}\}$$

其中 $\bar{m}_{\mathrm{gt}}$ 和 $\bar{m}_{\mathrm{pred}}$ 分别为真实光流和预测光流的全局平均幅度，$\tau$ 为容忍阈值。该正则项专门惩罚预测运动幅度远小于真实运动的情形（即模型倾向于保持输入图像不变、拒绝执行运动编辑），强制模型产生足够显著的运动变化。

#### （4）组合偏差与奖励转换

总运动偏差为三分量的加权和：

$$\mathcal{D}_{\mathrm{comb}} = \alpha \mathcal{D}_{\mathrm{mag}} + \beta \mathcal{D}_{\mathrm{dir}} + \lambda_{\mathrm{move}} M_{\mathrm{move}}$$

将偏差转换为连续奖励 $r_{\mathrm{cont}}$ 后，进一步量化为 6 级离散值以稳定训练：

$$r_{\mathrm{motion}} = \frac{1}{5} \operatorname{round}(5 r_{\mathrm{cont}}) \in \{0.0, 0.2, 0.4, 0.6, 0.8, 1.0\}$$

### 多信号奖励融合

最终训练奖励由运动对齐奖励与 MLLM 语义奖励按 0.5:0.5 的比例组合。MLLM 奖励使用 **Qwen2.5-VL** 在线评估编辑图像的语义质量（包括编辑保真度、背景保持度、整体连贯性）。消融实验（Table 4）证实，该均衡组合在所有指标上均优于纯 MLLM 奖励或纯光流奖励，验证了两类信号的互补性——光流提供精确的几何监督，MLLM 维护语义保真度。

### 评估指标：运动对齐分数（MAS）

为量化运动编辑的忠实度，论文定义了运动对齐分数 MAS：

$$\mathrm{MAS} = 100.00 \cdot \left(1 - \mathrm{clip}\left(\frac{\mathcal{D}_{\mathrm{ovl}} - d_{\mathrm{min}}}{d_{\mathrm{max}} - d_{\mathrm{min}}}, 0, 1\right)\right)$$

其中 $\mathcal{D}_{\mathrm{ovl}} = \alpha \mathcal{D}_{\mathrm{mag}} + (1 - \alpha) \mathcal{D}_{\mathrm{dir}}$ 为幅度与方向一致性的加权组合偏差，$d_{\mathrm{min}}$ 和 $d_{\mathrm{max}}$ 为数据集层面的归一化边界。若预测光流为零（即模型完全未执行运动编辑），MAS 直接赋值为 0。该指标将光流对齐程度映射到 0–100 分，分数越高表示运动编辑越忠实于真实目标。



## 实验与关键发现

本章节系统评估 MotionNFT 在 MotionEdit-Bench 上的运动编辑性能，并通过消融实验验证光流运动奖励与 MLLM 语义奖励的互补机制。

### 主实验结果

**Table 1** 展示了各模型在 MotionEdit-Bench 上的综合表现。以 FLUX.1 Kontext 为基座模型时，MotionNFT 将综合生成质量（Overall）从 3.84 提升至 4.25（+10.68%），运动对齐分数（MAS）从 53.73 提升至 55.45，胜率（Win Rate）从 57.71% 提升至 64.95%。以 Qwen-Image-Edit 为基座时，Overall 从 4.65 提升至 4.72（+1.51%），胜率达 73.67%。值得注意的是，扩散编辑基线模型（如 Instruct-P2P、AnyEdit、MagicBrush）在运动编辑任务上普遍表现不佳，而强化学习编辑基线 UniWorld-V1 虽有一定运动编辑能力，但仍逊于 MotionNFT 训练的模型。

**Figure 13** 与 **Figure 14** 的定性对比进一步佐证了这一结论：现有开源模型（UniWorld-V1、BAGEL、FLUX.1 Kontext）在姿态编辑和身份保持上存在明显失败区域，而闭源商业模型（Nano-Banana、GPT-Image-1、Seedream、Hunyuan Image）同样在复杂运动指令下出现运动未执行或外观失真。MotionNFT 在这些案例中准确执行了目标运动编辑，且与真值图像高度匹配。

### 通用编辑能力保持

**Table 2** 报告了 ImgEdit-Bench 上的通用编辑性能。MotionNFT 不仅未牺牲通用编辑能力，反而在 FLUX.1 Kontext 基座上将 Overall 从 3.26 提升至 3.50。这表明光流运动奖励的引入并未导致模型对运动编辑的过拟合，而是通过几何-语义联合优化实现了编辑能力的整体增强。

### 奖励权重消融

**Table 4** 展示了 MLLM 语义奖励与光流运动奖励的权重消融结果。核心发现如下：

- **纯光流奖励（1.0 Motion）**：Overall 降至 3.60，低于基线的 3.84，说明几何线索单独不足以维持语义保真度。
- **纯 MLLM 奖励（1.0 MLLM）**：Overall 达 4.20，但仍低于组合方案。
- **均衡组合（0.5:0.5）**：在所有指标上均取得最优，验证了两种奖励信号的互补性——语义奖励保障编辑指令的语义执行，运动奖励提供精确的几何对齐指导。

**Figure 9** 与 **Figure 10** 的训练曲线揭示了更深层的互补机制：仅使用 MLLM 奖励时，运动对齐分数（MAS）在大约 150 步后开始退化，表明模型过度拟合语义信号而丧失运动精度；而 MotionNFT 的 MAS 持续稳定上升，证明额外的运动指导有效防止了这种退化。

**Table 3** 进一步对比了 MotionNFT 与纯 MLLM 奖励训练的差异：引入运动奖励后，Overall、MAS 和 Win Rate 均获得显著提升，且这一增益在 FLUX.1 Kontext 和 Qwen-Image-Edit 两个基座模型上普遍成立。

### 数据集运动幅度分析

**Figure 6** 对比了 MotionEdit 与现有编辑数据集（MagicBrush、OmniEdit 等）的运动幅度分布。MotionEdit 的平均输入-目标运动幅度（以光流衡量）约为 0.19，是 MagicBrush 和 OmniEdit 的 5.8 倍。这一显著差异解释了现有模型在运动编辑任务上集体失败的根本原因——训练数据中缺乏足够大的运动变化监督信号。

### 失败模式分析

**Figure 15** 展示了 MotionNFT 及商业模型的共同失败案例。主要失败模式包括：

1. **多主体运动分配困难**：当指令涉及多个非编辑主体时，模型难以精确地将运动编辑作用于目标主体，同时保持其他主体的身份和位置不变。
2. **复杂 3D 空间交互**：在涉及物体遮挡、远距离位移的场景中，所有模型均出现运动对齐失败或几何失真。
3. **身份保持漂移**：在背景复杂或主体纹理相似时，编辑后可能出现外观漂移，尤其在多主体交互场景下更为明显。

这些失败模式揭示了当前运动编辑方法在空间分配精度和身份保持机制上的根本局限，也为后续研究指明了改进方向。

### 补充图表

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/008_Table_1.jpg]]
*Table 1: Quantitative results on MOTIONEDIT-BENCH. Among existing methods, Step1X-Edit and BAGEL achieve the strongest motionediting performance, while diffusion-based editors such as AnyEdit and MagicBrush perform poorly across both generative and discriminative metrics. FLUX.1 Kontext and Qwen-Image-Edit models trained with MotionNFT yields the best overall results: for both models, applying MotionNFT boosts all generative metrics, MAS and pairwise win rate*

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/015_Table_4.jpg]]
*Table 4: Ablation experiments on different weights for balancing the MLLM-based reward proposed by [15] and our optical flowbased motion alignment reward. Results show that combining both rewards on a 0.5:0.5 scale achieves best performance, outperforming MLLM-only reward training*

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/013_Figure_9.jpg]]
*Figure 9: MAS vs. Training Steps on FLUX.1 Kontext [Dev] [14]. MAS quantifies the fidelity of the generated motion by calculating the optical flow alignment (considering both magnitude and direction) between the model’s edit and the ground truth target edit. While the MLLM-only baseline (blue) begins to regress after approximately 150 steps, MotionNFT (red) demonstrates steady improvement throughout training, ultimately achieving superior motion grounding by leveraging explicit motion guidance*

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/014_Figure_10.jpg]]
*Figure 10: MAS vs. Training Steps on Qwen-Image-Edit [34]. Results on other base models again shows that relying solely on semantic MLLM rewards leads to training regression in motion alignment. MotionNFT maintains prevents overfitting to semantic cues and achieving higher final MAS*

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/011_Table_2.jpg]]
*Table 2: Results on ImgEdit-Bench [37] MotionNFT not only preserves, but oftentimes boosts general editing performances*

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/012_Table_3.jpg]]
*Table 3: Comparison to training with MLLM-based reward [15] only. Incorporating MotionNFT yields noticeable improvements MLLM-scored Overall editing quality, optical flow-based Motion Alignment Score, and the pairwise Win Rate across all models*

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/019_Figure_13.jpg]]
*Figure 13: We compare MotionNFT against state-of-the-art baselines: UniWorld-V1 [15], BAGEL [7], and FLUX.1 Kontext [Dev] [14]. Red circles highlight failure regions. Baseline models exhibit different failure modes like editing inertia (e.g., failing to change the lion’s pose in row 2), or motion misalignment (e.g., raising the robot’s right arm instead of left arm in row 5). While baselines often struggle to execute challenging motion edits, MotionNFT achieves superior geometric grounding, accurately following semantic instructions and maintaining high motion fidelity to the ground truth*

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/023_Figure_14.jpg]]
*Figure 14: We conduct selective case studies of MotionNFT against leading closed-source commercial baselines: Nano-Banana [8], GPT-Image-1 [22], Seedream [26], and Hunyuan Image [3]. Red circles highlight failure regions where baselines exhibit spatial inertia (e.g., failing to displace the car in the bottom row) or structural hallucination (e.g., generating an artifact “foot” in the second row). While commercial models generally maintain high visual quality, they frequently struggle to ground complex motion changes or maintain visual consistency. MotionNFT accurately follows these dynamic instructions, ensuring geometric alignment with the ground truth*

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/007_Figure_6.jpg]]
*Figure 6: Comparison of motion difference between before- and post-edit images in different datasets [2, 33, 38–40]. Our MO-TIONEDIT dataset achieves the most significant motion changes*

![[assets/figures/papers/paper_list_l2_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing_motion20v2/figures/022_Figure_15.jpg]]
*Figure 15: Additional failure cases of our model and closed-source commercial models. We observe that instructions involving multiple involving and non-involving subjects (e.g. the orca example in row 1, which requires complex 3D spatial edit) remain challenging for all evaluated methods. Current models, including ours and commercial baselines, struggle to correctly generate accurate and targeted motions on the correct subject part with the correct direction and magnitude in challenging scenarios*



## 定位与知识库关联

### 1. 与基线工作的关系

MotionNFT 的核心技术路线建立在 **DiffusionNFT** 后训练框架之上，其关键创新在于将**光流几何信号**作为可微奖励引入强化学习式的流匹配微调。与仅依赖 MLLM 语义奖励的 UniWorld-V2 相比，MotionNFT 通过显式建模输入-输出与输入-真实目标之间的运动对齐，弥补了纯语义信号在空间几何理解上的不足。在方法谱系中，MotionNFT 处于扩散编辑后训练与运动感知奖励设计的交叉点。

作为基座模型，论文选择了基于 Flow Matching 的 **FLUX.1 Kontext** 和 **Qwen-Image-Edit**，而非传统的扩散模型（如 Stable Diffusion 系列）。这一选择具有方法论上的合理性：Flow Matching 的确定性速度场形式与 DiffusionNFT 的正/负速度策略天然契合，使得奖励信号可以直接作用于速度预测的优化方向。

论文将 MotionNFT 与多类基线进行了系统对比：
- **扩散编辑基线**：Instruct-P2P、AnyEdit、MagicBrush、UltraEdit 等传统方法在 MotionEdit-Bench 上表现不佳，验证了现有编辑模型缺乏运动编辑能力的核心论点。
- **强化学习编辑基线**：UniWorld-V1 虽然采用了 MLLM 奖励训练，但在运动编辑任务上仍出现姿态编辑失败等问题，说明纯语义奖励不足以引导精确的运动变换。
- **单步编辑基线**：Step1X-Edit 和 BAGEL 在运动编辑上表现相对较强，但仍被 MotionNFT 超越，表明多步流匹配模型结合运动感知奖励具有更大的优化空间。
- **闭源商业模型**：Nano-Banana、GPT-Image-1、Seedream、Hunyuan Image 等在复杂运动编辑场景中也存在明显失败区域，进一步凸显了运动编辑的挑战性。

### 2. 方法适用边界

MotionNFT 的有效性已在以下条件下得到验证：
- **基座模型**：Flow Matching 架构（FLUX.1 Kontext、Qwen-Image-Edit），未验证其在 DDPM 或 Consistency Model 上的迁移性。
- **运动类型**：涵盖姿态变化、位移、视角变化、主体-物体交互、主体间交互等六类运动编辑子类别。
- **评估基准**：MotionEdit-Bench（运动编辑专项）和 ImgEdit-Bench（通用编辑）上的结果表明，方法在提升运动编辑能力的同时未牺牲一般编辑性能。

方法的**技术前提**包括：
1. 需要成对的输入-真实目标图像来计算光流奖励，因此依赖有监督的运动编辑数据。
2. 光流估计的准确性直接影响奖励质量——论文使用 UniMatch 作为光流估计器，其对快速运动、运动模糊等极端情形的鲁棒性尚未充分验证。
3. 奖励量化到 6 级离散值的设计简化了训练，但可能损失了精细的几何反馈。

### 3. 局限与开放问题

论文明确指出的**局限性**包括：

**多主体编辑的精确性不足**：当场景包含多个非编辑主体时，模型难以将运动编辑指令精确作用于目标主体，同时保持其他主体的身份和位置不变。这一局限在主体-主体交互和主体-物体交互类别中尤为突出，表明模型缺乏细粒度的空间分配能力。

**复杂 3D 空间交互失败**：涉及物体遮挡、远距离位移等复杂空间关系的指令，所有模型（包括 MotionNFT）均出现运动对齐失败或几何失真。这暗示当前的光流奖励机制可能无法充分捕捉深度信息和 3D 几何约束。

**身份保持漂移**：在背景复杂或主体纹理相似时，编辑后可能出现外观漂移，尤其在处理多主体交互时更明显。这表明运动奖励与身份保持之间存在潜在冲突——模型在追求运动对齐时可能牺牲了外观保真度。

基于上述局限，论文指向以下**开放问题**：

1. **空间分配机制**：如何增强模型在多主体场景中的空间注意力，使运动编辑指令能够精确绑定到指定主体？可能的探索方向包括引入实例分割掩码作为条件、或设计基于注意力的主体绑定奖励。

2. **物理先验融合**：能否通过融合关节约束、场景深度等物理或运动学先验，改进复杂姿态编辑的合理性？这可能需要将光流奖励扩展为更丰富的几何一致性度量。

3. **身份保持增强**：能否在不增加推理开销的前提下，通过更强的身份嵌入或特征保持机制实现更高保真的外观保持？这涉及训练目标中运动奖励与语义奖励的进一步平衡。

4. **光流鲁棒性**：光流奖励对快速运动、运动模糊、大位移等极端情形的鲁棒性还有待探索。这直接关系到方法在实际应用中的可靠性。

5. **模型架构迁移**：MotionNFT 当前仅验证了 Flow Matching 架构，其在其他生成范式（如自回归模型、GAN）上的适用性尚不明确。



## 原文 PDF

![[paperPDFs/CVPR_2026/MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing.pdf]]
