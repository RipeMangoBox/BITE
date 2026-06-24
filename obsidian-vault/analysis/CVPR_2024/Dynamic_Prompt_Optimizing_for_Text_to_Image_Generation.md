---
title: "Dynamic Prompt Optimizing for Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Dynamic_Prompt_Optimizing_for_Text_to_Image_Generation.pdf
project_link: https://github.com/mowenyii/pae
aliases:
- PAEP
- DPOTIG
tags:
- CVPR_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "为每个修饰词分配的效果范围（注入时间步）和权重，构成动态精细控制提示（DF-Prompt），通过强化学习自动探索最优配置。"
primary_logic: "通过两阶段训练（监督精炼+在线强化学习），联合优化提示词、修饰词的权重和注入时间步，能够在保持语义一致性的前提下显著提升生成图像的审美质量和人类偏好。"
claims:
- "在Lexica.art数据集上，PAE的PickScore达到73.9%，超过人类编写提示的72.5%和Promptist的68.4%，同时审美得分最高（6.12）。"
- "消融实验表明，第二阶段模型EDFP相比第一阶段EReP在PickScore上提升4.0%（53.8%→57.8%），审美得分从6.03提升至6.07，验证了动态精细控制的价值。"
- "在跨域评估（COCO数据集）中，PAE的PickScore（53.8%）远超简短提示（42.4%）和Promptist（47.8%），显示出强泛化能力。"
- "奖励函数消融显示，结合CLIP、PickScore和审美得分的多维奖励是提升模型性能的关键，最优参数设置为α=1, β=0, κ=18。"
---

# Dynamic Prompt Optimizing for Text-to-Image Generation

> [!tip] 核心洞察
> 通过两阶段训练（监督精炼+在线强化学习），联合优化提示词、修饰词的权重和注入时间步，能够在保持语义一致性的前提下显著提升生成图像的审美质量和人类偏好。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向文本到图像生成的动态提示优化 |
| 英文题名 | Dynamic Prompt Optimizing for Text-to-Image Generation |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2404.04095); [GitHub](https://github.com/mowenyii/pae) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Prompt Auto-Editing (PAE) |
| Dataset | Lexica.art, DiffusionDB, COCO |

> [!tip] 效果简介
> - Lexica.art 上，PickScore (↑) 为 73.9%，对比 68.4% (Promptist)，变化 +5.5%。
> - Lexica.art 上，Aes Score (↑) 为 6.12，对比 6.11 (Promptist)，变化 +0.01。
> - DiffusionDB 上，PickScore (↑) 为 64.4%，对比 55.3% (Short Prompt)，变化 +9.1%。

## 概述

**核心问题**：文本到图像扩散模型对提示词高度敏感，手工设计具备精细控制能力（如逐词权重与注入时间步）的提示需大量试错，现有自动优化方法缺乏对修饰词效果范围和权重的控制。

**核心方法**：本文提出**Prompt Auto-Editing (PAE)**，一种两阶段自动化提示优化框架。第一阶段基于置信度评分自动筛选公开提示-图像数据，微调GPT-2生成精炼提示；第二阶段通过在线强化学习，联合优化修饰词的权重与注入时间步，形成**动态精细控制提示（DF-Prompt）**。奖励函数组合CLIP语义一致性、审美得分与PickScore人类偏好。

**关键结论**：
- 在Lexica.art数据集上，PAE的PickScore达**73.9%**，超越人类编写提示（72.5%）与Promptist（68.4%），审美得分最高（6.12）。
- 消融实验表明，第二阶段动态精细控制模型相较第一阶段精炼模型，PickScore提升**4.0%**（53.8%→57.8%），审美得分从6.03增至6.07，验证了动态控制的价值。
- 跨域评估（COCO）中，PAE的PickScore（53.8%）远超简短提示（42.4%）与Promptist（47.8%），显示出强泛化能力。

**方法定位**：PAE属于基于强化学习的提示优化方法，在控制粒度上引入了逐词权重与时间步分配，突破了纯文本提示的局限。与Promptist（Hao et al., 2023）等仅优化文本内容的方法相比，PAE通过修改扩散模型的文本注入机制实现动态精细控制。

## 背景与动机

文本到图像生成领域近年来取得了显著进展，特别是以 Stable Diffusion 为代表的扩散模型能够根据自然语言描述生成高质量的图像。然而，这些模型对提示词（prompt）高度敏感——即使是微小的措辞变化，也可能导致生成结果在风格、构图和细节上产生显著差异。这催生了“提示工程”（prompt engineering）的实践需求：用户通过反复试错，手工添加修饰词（如 “trending on ArtStation”、“4k detailed”）来引导模型输出符合预期的图像。

这一手工过程存在两个根本性瓶颈。**第一，修饰词的“效果范围”难以控制。** 扩散模型在去噪过程的不同时间步负责生成不同粒度的内容——早期步骤决定整体布局和结构，后期步骤填充纹理和细节。然而，传统提示工程将所有修饰词无差别地注入全部时间步，无法针对性地让某个修饰词只在特定阶段生效。例如，将 “detailed” 一词限制在去噪的前 15% 时间步内，可以生成更自然的纹理细节，而非在所有时间步中过度锐化图像（见 Figure 1）。**第二，修饰词的“权重”缺乏精细调节。** 用户无法定量控制每个修饰词对生成结果的影响强度，只能通过增减词汇来粗略调整。

现有的自动化提示优化方法试图缓解手工试错的负担，但均存在明显缺口。**Promptist**（Hao et al., 2023）采用强化学习优化提示，但其输出仍是纯文本序列，无法为每个修饰词分配独立的效果范围与权重，本质上仍停留在“全局文本替换”的粒度。**遗传算法**等黑箱搜索方法虽然能探索提示空间，但搜索效率低且缺乏对扩散模型内部机制的利用。更关键的是，这些方法的优化目标往往单一（如仅优化审美得分），忽略了语义一致性、人类偏好等多维度质量指标的平衡。

本文的核心动机在于：**将提示优化从“全局文本选择”提升为“动态精细控制”**。具体而言，为每个修饰词显式分配一个三元组 ⟨token, 效果范围, 权重⟩，构成**动态精细控制提示（DF-Prompt）**。效果范围定义了该修饰词在去噪过程的哪些时间步生效（[b_i, e_i]），权重则控制其注入强度（w_i）。这一设计将提示优化的搜索空间从离散的词汇选择扩展为连续的联合优化问题，从而能够在不牺牲语义一致性的前提下，显著提升生成图像的审美质量和人类偏好得分。为高效探索这一复杂空间，本文提出**Prompt Auto-Editing (PAE)** 框架，通过两阶段训练（监督精炼 + 在线强化学习）自动学习最优的修饰词及其控制参数。

## 核心创新

PAE的核心创新在于将文本到图像生成的提示优化从“静态文本扩展”提升为“动态精细控制”。传统方法（如**Promptist**，Hao et al., 2023）仅能生成纯文本后缀，无法控制每个修饰词对生成过程的影响程度。PAE通过两个关键维度的改变，实现了对提示的细粒度操控。

### 动态精细控制提示（DF-Prompt）

PAE将纯文本提示重构为一种结构化表示——**动态精细控制提示（DF-Prompt）**。在此表示中，每个修饰词不再是一个孤立的token，而是一个三元组 $a_i = \langle x_i, \tau_i, w_i \rangle$，其中 $x_i$ 为修饰词本身，$\tau_i = [b_i \mapsto e_i]$ 为其效果范围（即该修饰词在扩散模型去噪过程中的注入时间步区间），$w_i$ 为其权重（控制该修饰词在文本嵌入中的缩放强度）。这一设计直接回应了核心瓶颈：手工提示无法对修饰词的效果进行精细控制。

Figure 1 的定性实验直观展示了该机制的有效性：将“anime”的权重从1.0提升至1.5，可显著增强画面的动漫风格；而将“detailed”的效果范围限制在前15%的去噪时间步内，能生成更自然的纹理细节，避免了全时间步注入导致的过度渲染。这种控制粒度是现有方法所不具备的。

### 两阶段自动化优化框架

PAE通过两个训练阶段，自动探索最优的DF-Prompt配置，替代了依赖手工试错的人工提示工程。

**第一阶段：监督精炼（EReP）**。该阶段解决“生成什么修饰词”的问题。PAE首先定义了一个基于置信度评分的自动数据过滤机制（Eq. 1），从公开数据中筛选出添加修饰词后既能提升审美质量、又能保持语义一致性的提示-图像对。随后，在该数据集上微调GPT-2模型，使其能够自回归地生成后缀修饰词序列。该阶段的训练损失为标准的负对数似然（Eq. 2）。

**第二阶段：在线强化学习动态控制（EDFP）**。该阶段解决“如何控制修饰词效果”的问题。PAE在EReP模型基础上添加两个线性头，分别预测每个修饰词的效果范围 $\tau_i$ 和权重 $w_i$，三者共享同一中间表示。策略模型通过在线探索生成DF-Prompt，并使用扩散模型生成对应图像，随后计算多维奖励函数 $R$（Eq. 4）。该奖励函数创新性地组合了三个维度：
- **CLIP Score**：约束语义一致性，设定阈值 $\zeta$ 确保不偏离原始语义；
- **PickScore**：引入人类偏好学习指标，设定阈值 $\kappa$ 作为偏好基准；
- **Aesthetic Score**：直接优化审美质量，通过缩放因子 $\alpha$ 和基线折扣 $\beta$ 控制其贡献。

策略模型通过PPO算法最大化累积奖励，同时以KL散度约束策略不过度偏离初始EReP模型（Eq. 3）。消融实验（Table 7）证实了第二阶段的价值：EDFP相比EReP在PickScore上提升4.0%（53.8%→57.8%），审美得分从6.03提升至6.07，验证了动态精细控制对生成质量的增益。

综上，PAE通过**DF-Prompt的结构化表示**和**两阶段自动化优化**两个changed slots，实现了从“写提示”到“调控提示”的范式转变，在保持语义一致性的前提下显著提升了生成图像的审美质量和人类偏好。

## 整体框架

PAE 采用**两阶段训练流程**（Figure 2），将提示优化问题分解为“精炼”与“动态控制”两个递进子任务：

1. **第一阶段：监督精炼（Plain Prompt Refinement）**  
   基于置信度评分 $S$（Eq. 1）自动筛选公开提示-图像对，构建高质量训练集。随后在筛选数据上微调 GPT-2，使其自回归地为主体提示生成后缀修饰词序列 $\mathbf{A}$。该阶段输出模型 $\mathcal{E}_{\mathrm{ReP}}$，其核心能力是**学习“什么样的修饰词能稳定提升图像质量”**，但不涉及对修饰词影响力的精细控制。

2. **第二阶段：在线强化学习动态控制（Dynamic Fine-Control）**  
   以 $\mathcal{E}_{\mathrm{ReP}}$ 初始化策略模型 $\mathcal{E}_{\mathrm{DFP}}$，并在其基础上添加两个线性头——分别预测每个修饰词的**效果范围** $[b_i \mapsto e_i]$ 和**权重** $w_i$。策略模型在推理时输出动态精细控制提示（DF-Prompt），其中每个修饰词被扩展为三元组 $\langle \text{token}, \text{effect range}, \text{weight} \rangle$。扩散模型 $\mathcal{M}$ 根据 DF-Prompt 修改文本注入模式，生成图像后由多维奖励函数 $R$（Eq. 4）评估。策略模型通过 PPO 目标（Eq. 3）在线更新，在探索权重与时间步配置的同时，以 KL 散度约束保持与初始模型的适度偏离。

**模块关系与数据流**：
- **数据过滤模块**：输入原始提示-图像对，通过置信度评分筛选出“添加修饰词后审美提升且语义保持”的样本，输出训练集 $\mathbb{D}$。
- **精炼提示模型 $\mathcal{E}_{\mathrm{ReP}}$**：输入简短提示 $\mathbf{s}$，自回归生成修饰词序列，输出精炼提示 $\mathbf{s} \oplus \mathbf{A}$。
- **动态精细控制策略模型 $\mathcal{E}_{\mathrm{DFP}}$**：在 $\mathcal{E}_{\mathrm{ReP}}$ 基础上，联合预测修饰词、权重和注入时间步，输出 DF-Prompt。
- **增强文本编码器**：接收 DF-Prompt，实现逐词加权嵌入和动态时间步注入，控制扩散模型在特定去噪阶段施加修饰词影响。
- **奖励评估器**：以简短提示和生成图像为输入，计算 CLIP Score、Aesthetic Score 和 PickScore 的多维组合奖励，反馈至策略模型更新。

这一框架的核心设计在于**将修饰词的“效果强度”和“作用时段”显式参数化**，使优化过程从“选词”升级为“选词 + 调参”，从而在保持语义一致性的前提下，更精细地控制生成图像的审美属性。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/005_Figure_3.jpg]]
*Figure 3: Generated images using Stable Diffusion v1.4 with short prompts, Promptist [9], and our method. In each column, the images are generated using the same random seed. Our method shows the ability to moderately expand the semantic content, such as “in a scenic environment”, “with gorgeous hair face illustration”, “on a ship deck” and “for 50 years.” These expansions stimulate users’ imagination while enhancing the comprehensiveness and aesthetic quality of the image*

## 核心模块与公式推导

PAE 方法围绕**动态精细控制提示（DF-Prompt）** 展开，其核心由五个功能模块构成，并通过四个关键公式串联起从数据筛选到策略优化的完整流程。

### 1. 数据筛选与训练样本构建模块

该模块负责从公开的提示-图像对中自动筛选高质量训练数据。其核心是一个**置信度评分函数** $S$，用于量化“添加修饰词后生成质量是否提升”：

$$S(\mathbf{s}^{\prime},\mathbf{s}) = \mathbb{E}_{\mathbf{I}^{\prime}\sim\mathcal{M}(\mathbf{s}^{\prime}),\mathbf{I}\sim\mathcal{M}(\mathbf{s})}[u(g_{\mathrm{aes}}(\mathbf{I}^{\prime})-g_{\mathrm{aes}}(\mathbf{I})) \times u(g_{\mathrm{CLIP}}(\mathbf{s},\mathbf{I}^{\prime})-g_{\mathrm{CLIP}}(\mathbf{s},\mathbf{I})+\gamma)]$$

**变量含义**：
- $\mathbf{s}$：简短提示（仅含主体描述）
- $\mathbf{s}^{\prime}$：完整提示（含修饰词）
- $\mathcal{M}(\cdot)$：扩散模型（Stable Diffusion v1.4）
- $g_{\mathrm{aes}}(\cdot)$：审美评分函数
- $g_{\mathrm{CLIP}}(\cdot,\cdot)$：CLIP 语义相似度
- $u(\cdot)$：阶跃函数，确保审美得分提升和语义相似度提升（含容忍度 $\gamma$）
- $S$：期望乘积形式的置信度评分，仅当两项均改善时样本被保留

该评分通过期望乘积形式同时约束**审美质量提升**和**语义一致性保持**，最终从 Lexica.art 和 DiffusionDB 中筛选出约 450,000 个提示对用于训练。

### 2. 精炼提示模型（$\mathcal{E}_{\mathrm{ReP}}$）

第一阶段模型基于 GPT-2 微调，以自回归方式预测后缀修饰词序列。训练采用**教师强制**策略，损失函数为标准负对数似然：

$$\mathcal{L}_{\mathrm{ReP}} = -\mathbb{E}_{\langle\mathbf{s},\mathbf{A}\rangle\sim\mathbb{D}}[\log P(\mathbf{A}|\mathbf{s},\mathcal{E}_{\mathrm{ReP}})]$$

**变量含义**：
- $\mathbb{D}$：经置信度评分筛选后的训练集
- $\mathbf{A} = \{a_1, a_2, ..., a_n\}$：修饰词序列
- $\mathcal{E}_{\mathrm{ReP}}$：精炼提示生成模型
- $P(\mathbf{A}|\mathbf{s},\mathcal{E}_{\mathrm{ReP}})$：给定简短提示 $\mathbf{s}$ 时模型预测修饰词序列的概率

该阶段使模型学会为简短提示补充有效的修饰词，但生成的仍是**纯文本提示**，缺乏对每个修饰词影响程度的精细控制。

### 3. 动态精细控制策略模型（$\mathcal{E}_{\mathrm{DFP}}$）

第二阶段在 $\mathcal{E}_{\mathrm{ReP}}$ 基础上添加**两个线性头**，分别预测每个修饰词的**效果范围** $\tau_i = [b_i \mapsto e_i]$（注入时间步区间）和**权重** $w_i$，形成三元组 $a_i = \langle x_i, \tau_i, w_i \rangle$。训练采用在线强化学习，基于 PPO 目标函数：

$$\mathcal{L}_{\mathrm{DFP}} = -\mathbb{E}_{\mathbf{s}\sim\mathbb{D},\mathbf{A}^{\mathrm{DFP}}\sim\mathcal{E}_{\mathrm{DFP}}}[R(\mathbf{s},\mathbf{A}^{\mathrm{DFP}}) - \eta D_{\mathrm{KL}}]$$

**变量含义**：
- $\mathbf{A}^{\mathrm{DFP}}$：策略模型生成的 DF-Prompt 修饰词集合
- $R(\mathbf{s},\mathbf{A}^{\mathrm{DFP}})$：多维奖励函数（见下文）
- $D_{\mathrm{KL}}$：当前策略与初始模型 $\mathcal{E}_{\mathrm{ReP}}$ 之间的 KL 散度
- $\eta$：KL 惩罚系数，约束策略不过度偏离初始模型

该损失函数在最大化累积奖励的同时，通过 KL 正则化保持策略的稳定性，防止生成无意义的修饰词配置。

### 4. 奖励评估模块

奖励函数是强化学习的关键，PAE 设计了**多维组合奖励**，同时考虑语义一致性、人类偏好和审美质量：

$$R(\mathbf{s},\mathbf{A}^{\mathrm{DFP}}) = \mathbb{E}_{\mathbf{I}\sim\mathcal{M}(\mathbf{s}),\mathbf{I}^{\mathrm{DFP}}\sim\mathcal{M}(\mathbf{s}\oplus\mathbf{A}^{\mathrm{DFP}})}[\min(g_{\mathrm{CLIP}}(\mathbf{s},\mathbf{I}^{\mathrm{DFP}})-\zeta,0) + \min(g_{\mathrm{PKS}}(\mathbf{s},\mathbf{I}^{\mathrm{DFP}})-\kappa,0) + \alpha\cdot(g_{\mathrm{aes}}(\mathbf{I}^{\mathrm{DFP}})-\beta\cdot g_{\mathrm{aes}}(\mathbf{I}))]$$

**变量含义**：
- $\mathbf{I}$：简短提示生成的图像
- $\mathbf{I}^{\mathrm{DFP}}$：DF-Prompt 生成的图像
- $g_{\mathrm{CLIP}}$：CLIP 语义相似度
- $g_{\mathrm{PKS}}$：PickScore 人类偏好评分
- $g_{\mathrm{aes}}$：审美评分
- $\zeta$：CLIP 相似度阈值，低于此值产生惩罚
- $\kappa$：PickScore 阈值，低于此值产生惩罚
- $\alpha$：审美得分缩放因子
- $\beta$：基准审美得分权重

三项奖励的设计逻辑：
- **CLIP 项**（$\min(\cdot,0)$）：当语义相似度低于阈值 $\zeta$ 时施加惩罚，防止修饰词偏离原始语义
- **PickScore 项**（$\min(\cdot,0)$）：当人类偏好得分低于阈值 $\kappa$ 时施加惩罚，确保生成结果符合人类审美偏好
- **审美项**（$\alpha\cdot(g_{\mathrm{aes}}(\mathbf{I}^{\mathrm{DFP}})-\beta\cdot g_{\mathrm{aes}}(\mathbf{I}))$）：鼓励生成图像的审美得分相对简短提示有所提升，$\alpha$ 控制该项贡献强度，$\beta$ 调节基准比较力度

消融实验（Table 6）确定最优参数为 $\alpha=1, \beta=0, \kappa=18$，此时 PickScore 达到 58.0%，审美得分达到 6.04。

### 5. 增强文本编码器模块

为使扩散模型能够解析 DF-Prompt 中的三元组结构，PAE 修改了 Stable Diffusion 的文本编码器，实现**逐词加权嵌入**和**动态时间步注入**：在去噪过程的不同时间步，根据每个修饰词的 $\tau_i$ 和 $w_i$ 选择性注入其嵌入向量，从而实现精细的生成控制。

## 实验与分析

### 核心实验：主结果与多基准评估

PAE 在多个基准上均取得最优或具竞争力的结果，验证了动态精细控制提示的有效性。

在 **Lexica.art** 数据集上（Table 1），PAE 的 **PickScore** 达到 **73.9%**，显著超越人类编写提示的 72.5% 和 Promptist 的 68.4%，同时 **Aesthetic Score** 取得最高分 **6.12**。这一结果表明，自动优化的 DF-Prompt 在人类偏好和审美质量两个维度上均能超越人工设计的提示。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/007_Figure_5.jpg]]
*Figure 5: (a) The 15 most frequently generated modifiers. (b∼d) The frequency of different combinations of settings. Table 1. Quantitative comparison on Lexica.art*

在 **CMMD** 指标（越低越逼真）上（Table 2），PAE 取得 **1.125**，优于 Promptist 的 1.147，说明 PAE 生成的图像在分布层面更接近真实图像。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparison using the CMMD metric*

在 **DiffusionDB** 数据集上（Table 3），PAE 的 PickScore 达到 **64.4%**，相比简短提示的 55.3% 提升 **+9.1%**，证明方法在不同来源的提示上具有稳健性。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/008_Table_3.jpg]]
*Table 3: Quantitative comparison on DiffusionDB. Table 4. Quantitative comparison on COCO*

在跨域泛化实验中（**COCO** 数据集，Table 4），PAE 的 PickScore 为 **53.8%**，远超简短提示的 42.4%（+11.4%）和 Promptist 的 47.8%（+6.0%）。这一结果强有力地证明了 PAE 在域外数据上的泛化能力——即使训练数据来自 Lexica.art 等艺术提示源，模型仍能有效优化 COCO 的日常场景描述。

在 **FID** 指标上（Table 10），当提示中添加 “DSLR” 修饰词时，PAE 取得 **69.84**，优于 Promptist 的 70.80，进一步佐证了生成图像质量的提升。

### 消融实验：验证各设计选择的因果作用

#### 两阶段训练的有效性

Table 7 对比了第一阶段精炼模型（EReP）与第二阶段动态精细控制模型（EDFP）的性能。在 COCO 验证集上，EDFP 相较 EReP 在 **PickScore** 上提升 **4.0%**（53.8% → 57.8%），**Aesthetic Score** 从 6.03 提升至 6.07，且所有指标均呈正向增益。这一消融直接证明了**动态精细控制（为修饰词分配权重和注入时间步）**是性能提升的关键因果杠杆，而非仅靠增加修饰词数量。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/010_Table_6.jpg]]
*Table 6: * To highlight the disparity, we report the measure E[gPKS(s, Im) > gPKS(s, I)]. Table 6. Ablation experiments on different parameters of reward. The second stage model $\mathcal { E } _ { \mathrm { D F P } }$ is trained for 1,000 episodes. Table 7. Comparison between the initial model $\mathcal { E } _ { \mathrm { R e P } }$ and the second stage model $\mathcal { E } _ { \mathrm { D F P } }$ trained over 3,000 episodes

#### 数据过滤超参数

Table 5 展示了第一阶段数据过滤超参数 σ 和 γ 的消融结果。当 **σ=0.5, γ=0.01** 时，EReP 在 50k 步取得最高 Aesthetic Score（6.03），验证了置信度评分公式 Eq. (1) 中容忍度参数 γ 对平衡审美提升与语义保持的关键作用。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/011_Table_5.jpg]]
*Table 5: Ablation experiments on hyperparameters of the validation set. We validate the results of the first-stage model $\mathcal { E } _ { \mathrm { R e P } }$ at 50k steps on the DiffusionDB Validation set

#### 奖励函数设计

Table 6 对奖励函数 Eq. (4) 中的参数进行了系统消融。最优配置为 **α=1, β=0, κ=18**，此时模型取得最高 PickScore（58.0%）和 Aesthetic Score（6.04），CLIP Score 稳定在 0.26。值得注意的是，β=0 意味着奖励函数中**不惩罚原始简短提示的审美得分**，仅奖励优化后图像的审美提升；κ=18 的设置说明 PickScore 阈值对筛选有效人类偏好信号至关重要。该消融验证了多维奖励（CLIP + PickScore + Aesthetic）的组合是驱动 RL 策略学习的关键。

#### 训练动态

Figure 6(a) 展示了强化学习训练过程中奖励随 Episode 的变化曲线。策略模型的奖励值在约 **3000 个 Episode** 时达到峰值，之后趋于平稳，表明 PPO 优化过程有效且收敛稳定。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/004_Figure.jpg]]

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/006_Figure.jpg]]
*Figure: (b) （c） (d）*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/017_Figure.jpg]]

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/018_Figure.jpg]]

### 定性分析与可视化证据

**Figure 3** 展示了不同方法（Short Prompt、Promptist、PAE）的生成对比。PAE 能够适度扩展语义内容，例如自动添加 “in a scenic environment”、“with gorgeous hair face illustration”、“on a ship deck” 等修饰，在激发用户想象力的同时提升了图像的全面性和审美质量。

**Figure 4** 进一步对比了精炼提示与 DF-Prompt 的生成效果。DF-Prompt 生成的图像展现出更丰富的纹理细节和背景层次，验证了动态控制修饰词注入时间步（如仅在去噪早期注入 “detailed”）能够产生更自然的细节增强效果。

**Figure 5** 统计了最频繁生成的 15 个修饰词及其权重/时间步设置分布。高频词汇以风格描述（如 “digital art”、“anime”）和质感词（如 “detailed”、“intricate”）为主，且不同词汇展现出差异化的最优权重和时间步配置模式，印证了动态精细控制的必要性。

### 效率与开销

Table 9 报告了各阶段的训练与推理时间成本（A800 80GB GPU）。推理阶段，PAE 每提示需 **0.73 秒**，较 Promptist 的 0.69 秒仅增加 0.04 秒；动态 SD 管线的额外开销为 0.07 秒，整体推理延迟增幅微小，具备实用部署的可行性。

### 失败模式与局限性

尽管 PAE 在多项指标上表现优异，论文明确指出以下局限：

1. **属性泄漏与物体缺失**：当前方法未解决原始 Stable Diffusion 中存在的属性绑定错误和物体遗漏问题，优化提示无法从根本上修复扩散模型的固有缺陷。
2. **奖励覆盖不全面**：奖励函数未涵盖高分辨率、比例构图、多样性等因素，可能限制生成图像在更广泛质量维度上的优化。
3. **控制粒度受限**：当前控制仅限于全局修饰词的权重和注入时间步，尚未实现基于注意力图的**区域级精细控制**，无法对图像局部进行独立调节。
4. **模型架构泛化性待验证**：所有实验均基于 Stable Diffusion v1.4，对其他扩散模型架构（如 SDXL）或非扩散类文本到图像模型的适用性需要进一步探索。

### 公平性说明

所有定量实验均使用相同的随机种子、推断参数（温度 0.9，top-k=200）和生成模型（Stable Diffusion v1.4），确保比较的公平性。测试集与训练集独立，且包含 COCO 等域外数据以检验泛化性。训练数据过滤中移除了 NSFW 图像，但未分析数据中可能存在的风格或文化偏差，这一点需在实际应用中加以注意。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/001_Figure.jpg]]
*Figure: a red horse on the yellow grass, anime, 1 ↦ 0, 1 style a red horse on the yellow grass, anime, 1 ↦ 0, 1. ? style (a)*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2404_04095/figures/002_Figure_1.jpg]]
*Figure 1: Generation results with the same seed using dynamic fine-control prompt (one plain token is extended into a triple of ⟨token, effect range, weight⟩). It can be seen that (a) increasing the weight of anime to 1.5 can amplify the sense of anime; (b) applying the word detailed in the first 15% denoising timesteps can generate more natural texture details than applying it in all timesteps*

## 方法谱系与知识库定位

### 提示工程到自动化提示优化

文本到图像生成领域的提示工程经历了从纯手工设计到自动化优化的演进。早期用户依赖大量试错来编写有效提示，这一过程高度依赖经验且效率低下。为降低人工成本，研究者开始探索自动化提示优化方法，形成了两条主要技术路线。

**基于语言模型的提示扩展**：以 **Promptist**（Hao et al., 2023）为代表，该方法将提示优化建模为强化学习问题，通过微调语言模型自动为简短提示添加修饰词。然而，Promptist 生成的提示仍是纯文本形式，缺乏对单个修饰词影响程度的精细控制——所有修饰词在整个去噪过程中均匀施加影响，无法区分不同词汇在生成早期（布局形成）和后期（细节渲染）的差异化作用。

**基于搜索的提示优化**：另一类方法采用遗传算法或离散搜索在离散词汇空间中寻找最优修饰词组合。这类方法虽然能探索更广泛的修饰词空间，但搜索效率低、计算成本高，且同样无法实现逐词粒度的动态控制。

### PAE 的核心差异：动态精细控制提示（DF-Prompt）

PAE 在上述谱系中引入了关键的结构性创新——**动态精细控制提示（DF-Prompt）**。与传统方法将修饰词视为无差别的文本后缀不同，PAE 将每个修饰词扩展为一个三元组 $\langle \text{token}, \tau_i, w_i \rangle$，其中 $\tau_i = [b_i \mapsto e_i]$ 指定该修饰词生效的去噪时间步范围，$w_i$ 控制其嵌入权重。这一设计使得提示优化从“添加什么词”升级为“每个词在何时、以多大强度发挥作用”的多维控制问题。

**与 Promptist 的对比**：Promptist 可视为 PAE 第一阶段的特例——当所有修饰词的 $\tau_i = [0, 1]$（全时间步生效）且 $w_i = 1$（标准权重）时，DF-Prompt 退化为普通精炼提示。消融实验（Table 7）量化了这一差异的价值：第二阶段动态精细控制模型 $\mathcal{E}_{\mathrm{DFP}}$ 相比第一阶段精炼模型 $\mathcal{E}_{\mathrm{ReP}}$，PickScore 提升 4.0%（53.8% → 57.8%），审美得分从 6.03 增至 6.07，验证了动态控制机制对生成质量的独立贡献。

### 训练范式的创新

PAE 采用两阶段训练策略，在提示优化领域引入了自动化数据筛选与在线探索的结合：

- **第一阶段——监督精炼**：不同于 Promptist 依赖人工标注或启发式规则构建训练数据，PAE 设计了基于置信度评分 $S$（Eq. 1）的自动筛选机制。该评分通过期望乘积形式联合评估审美得分提升和语义一致性保持（含容忍度 $\gamma$），从公开数据中自动构建约 450,000 条高质量训练样本。这一数据获取方式降低了对人工标注的依赖，提升了方法的可扩展性。

- **第二阶段——在线强化学习**：PAE 将动态控制参数的探索建模为在线 RL 问题，使用 PPO 算法优化策略模型 $\mathcal{E}_{\mathrm{DFP}}$。与 Promptist 的离线 RL 不同，PAE 在训练过程中实时生成图像并计算多维奖励，使模型能够直接感知不同控制参数对生成结果的影响。KL 散度约束（Eq. 3 中的 $\eta D_{\mathrm{KL}}$）确保策略模型不过度偏离第一阶段学到的语言先验。

### 多维奖励函数的设计

PAE 的奖励函数（Eq. 4）整合了三个互补的评估维度：

$$R = \mathbb{E}[\min(g_{\mathrm{CLIP}} - \zeta, 0) + \min(g_{\mathrm{PKS}} - \kappa, 0) + \alpha \cdot (g_{\mathrm{aes}}(\mathbf{I}^{\mathrm{DFP}}) - \beta \cdot g_{\mathrm{aes}}(\mathbf{I}))]$$

其中 CLIP Score 保证语义一致性，PickScore 反映人类偏好，Aesthetic Score 衡量视觉美感。消融实验（Table 6）表明，最优参数设置为 $\alpha=1, \beta=0, \kappa=18$，此时 PickScore 达到 58.0%，审美得分 6.04。这一多维设计超越了 Promptist 的单一审美优化目标，使生成结果在语义保真度和人类偏好之间取得更好平衡。

### 适用边界与局限

**已验证的适用范围**：
- 扩散模型架构：当前实现基于 Stable Diffusion v1.4，通过修改文本编码器实现逐词加权嵌入和动态时间步注入（Appendix C）
- 全局修饰词控制：DF-Prompt 作用于整个图像的全局风格和内容修饰
- 英文提示：训练和评估均在英文提示上进行

**已知局限**：
1. **属性泄漏与物体缺失**：PAE 未解决底层 Stable Diffusion 固有的属性绑定错误和物体遗漏问题，优化提示无法根本弥补模型架构的缺陷
2. **控制粒度受限**：当前方法仅支持全局修饰词控制，未能实现基于注意力图的区域级精细控制，无法指定“仅对背景施加某效果”或“仅增强特定物体的某属性”
3. **奖励函数覆盖不足**：现有奖励未考虑高分辨率、比例构图、多样性等因素，可能限制生成图像的全面优化
4. **架构泛化性未验证**：方法仅针对 Stable Diffusion v1.4 验证，对其他扩散模型（如 Stable Diffusion XL）或非扩散类文本到图像模型（如自回归模型）的适用性需要进一步探索

### 开放问题与未来方向

1. **区域级精细控制**：如何将注意力图控制集成到动作空间中，使模型能够学习“对图像的哪个区域施加何种修饰”，从而缓解属性泄漏并实现更精准的局部编辑？

2. **更全面的奖励函数**：能否设计引入分辨率感知、构图质量、风格多样性等因素的多维奖励函数，进一步提升生成质量的全面性？

3. **跨架构扩展**：该方法能否迁移到更大规模的扩散模型（如 SDXL）或基于 Transformer 的文本到图像模型？动态时间步注入机制是否适用于非扩散范式？

4. **偏差量化与缓解**：训练数据过滤中已移除 NSFW 图像，但未分析数据中可能存在的风格、文化偏好等隐性偏差。如何量化并减轻这些偏差，确保生成结果的公平与多元？

## 原文 PDF

![[paperPDFs/CVPR_2024/Dynamic_Prompt_Optimizing_for_Text_to_Image_Generation.pdf]]
