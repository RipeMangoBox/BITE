---
title: "Adversarial Style Optimization: Enhancing VLM Jailbreaks by GRPO-based Stylistic Triggers Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Adversarial_Style_Optimization_Enhancing_VLM_Jailbreaks_by_GRPO_based_Stylistic_Triggers_Optimization.pdf
project_link: null
code_link: "https://github.com/bingjunluo/ASO"
aliases:
- ASOA
- ASOEVJBGBSTO
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 对抗图像的视觉风格（如素描、油画等非内容属性）
primary_logic: 利用MLLM对非内容风格变化的天然敏感性，通过两阶段框架（系统探查最优风格方向 + GRPO对抗优化风格参数）自动生成高效‘混合触发器’，将内容攻击升级为风格增强的复合攻击，从而大幅提高越狱成功率。
claims:
- 简单的风格滤镜（如铅笔素描）即可为现有SOTA内容攻击带来可测量的ASR提升
- ASO在MM-SafetyBench和VLBreakBench上一致且显著地提升了多种基础攻击的ASR，并在多个VLM（包括商用模型）上表现出跨模型泛化能力
- 消融实验证实，性能提升主要来源于GRPO强化学习增强阶段，而非单纯的风格探查；仅应用探查最优风格仅能带来微小提升
- MM-SafetyBench (Qwen3-VL) 上 ASR = 42.98%
---

# Adversarial Style Optimization: Enhancing VLM Jailbreaks by GRPO-based Stylistic Triggers Optimization

> [!tip] 核心洞察
> 利用MLLM对非内容风格变化的天然敏感性，通过两阶段框架（系统探查最优风格方向 + GRPO对抗优化风格参数）自动生成高效‘混合触发器’，将内容攻击升级为风格增强的复合攻击，从而大幅提高越狱成功率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 对抗风格优化：基于GRPO的风格触发器优化以增强视觉语言模型越狱攻击 |
| 英文题名 | Adversarial Style Optimization: Enhancing VLM Jailbreaks by GRPO-based Stylistic Triggers Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Luo_Adversarial_Style_Optimization_Enhancing_VLM_Jailbreaks_by_GRPO-based_Stylistic_Triggers_CVPR_2026_paper.html) · [Code](https://github.com/bingjunluo/ASO) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Adversarial Style Optimization (ASO) |
| Dataset | MM-SafetyBench |

> [!tip] 效果简介
> - MM-SafetyBench (Qwen3-VL) 上，ASR 42.98% vs 38.99% (+3.99%)；ASR 42.58% vs 39.31% (+3.27%)；ASR 89.52% vs 87.38% (+2.14%)。
> - MM-SafetyBench (LLaVA-OV-1.5) 上，ASR 44.35% vs 37.80% (+6.55%)；ASR 44.25% vs 37.82% (+6.43%)；ASR 55.42% vs 52.92% (+2.50%)。

## 概要

**问题瓶颈**：当前多模态大语言模型（MLLM）的安全防御机制与视觉理解能力之间存在“风格不一致性”——即使图像内容被模型稳健理解，其安全护栏却可能被特定的视觉风格变化轻易绕过。这一漏洞揭示了现有对齐策略对非内容属性（如笔触风格、色彩氛围）的脆弱性。

**核心洞察**：MLLM对非内容风格变化具有天然敏感性。通过系统探查最优攻击风格方向，并利用强化学习对抗性地优化风格参数，可以将单纯的内容攻击升级为“内容+风格”的混合触发器攻击，从而大幅提升越狱成功率。

**方法定位**：**Adversarial Style Optimization (ASO)** 是一个两阶段框架：（1）**风格敏感性探查**（Style Sensitivity Probing），从预定义的风格池中筛选出对目标VLM最有效的攻击风格；（2）**基于GRPO的风格增强**（GRPO-based Style Enhancement），使用动态批次GRPO算法微调图像编辑模型，在选定的风格空间内优化风格参数，生成高效的混合攻击图像。ASO可作为一种通用增强模块，叠加于现有SOTA内容攻击（如**FigStep**、**QR Attack**、**SI Attack**、**HIMRD**）之上。

**主要结果**：在MM-SafetyBench和VLBreakBench基准上，ASO一致且显著地提升了多种基础攻击的ASR，并在多个开源和商用VLM上展现出跨模型泛化能力。消融实验（Table 4）证实，性能增益主要来源于GRPO增强阶段，而非单纯的风格探查。

### 多模态大模型的安全挑战

随着视觉语言模型（VLM）在视觉问答、自主代理等高风险场景中的广泛应用，其安全对齐问题日益成为关注焦点。尽管这些模型在理解视觉内容方面能力强大，但它们的防御机制往往存在“风格不一致性”漏洞——即模型对图像的非内容属性（如素描、油画等视觉风格）表现出天然敏感性，而安全对齐机制却未能对这种风格变化保持鲁棒。Figure 1 直观展示了这一现象：一个原本被防御者有效拒绝的SOTA内容攻击，在经过简单的铅笔素描风格滤镜处理后，即可成功绕过安全机制。

### 现有攻击方法的局限

当前针对VLM的越狱攻击主要沿着两条路径展开：

- **基于内容的攻击**：通过精心构造有害文本提示或视觉内容本身来诱导模型违规输出，如 **FigStep**（Gong et al., AAAI 2025）通过打字式视觉提示嵌入有害指令，**QR Attack**（Liu et al., ECCV 2024）利用QR码编码恶意内容，**HIMRD**（Ma et al., ICCV 2025）采用启发式风险分布策略。
- **基于非内容的攻击**：利用输入的结构性扰动而非语义内容来破坏安全对齐，如 **SI Attack**（Zhao et al., ICCV 2025）通过Shuffle Inconsistency制造输入不一致性。

这两类方法各自独立地利用单一维度的漏洞，尚未充分挖掘“内容+风格”复合攻击的潜力。简单的风格滤镜（如铅笔素描）已能为现有SOTA内容攻击带来可测量的ASR提升（见Figure 1），但如何系统性地发现最优攻击风格并对其进行对抗优化，仍是一个开放问题。

### 核心研究动机

本文的核心动机源于一个关键观察：**VLM的理解能力与安全防御机制之间存在风格不一致性**——即使图像的视觉风格发生改变，模型仍能稳健理解其内容，但其安全防御机制却可能被特定风格触发器轻易绕过。这一现象暗示，通过精心设计和优化的视觉风格，可以在不破坏有害内容的前提下，大幅削弱模型的防御能力。

基于此，本文提出**对抗风格优化（Adversarial Style Optimization, ASO）**框架，旨在将内容攻击升级为“内容+风格”的混合触发器攻击。ASO通过两阶段流程——首先系统探查目标VLM最敏感的风格方向，随后利用GRPO强化学习对风格参数进行对抗优化——自动生成高效的风格增强攻击图像，从而显著提升越狱成功率。

## 核心方法与创新机理

### 1. 发现并系统化利用MLLM的“风格不一致性”漏洞

本工作的根本创新在于揭示了一个此前未被充分探索的安全漏洞：**MLLM的理解能力与安全防御机制之间存在风格不一致性**。具体而言，即使对图像施加非内容的视觉风格变换（如铅笔素描、油画等），模型仍能稳健地理解图像中的有害内容，但其安全防御机制却可能被特定的风格触发器轻易绕过。Figure 1 直观展示了这一现象：基础SOTA攻击被防御者有效拒绝，而经过风格优化的同一攻击却能成功绕过安全机制。

这一洞察将越狱攻击的焦点从传统的“内容对抗”扩展到了“风格对抗”这一新维度，为后续的方法设计提供了理论基础。

### 2. 关键changed slots：从单一维度攻击到混合触发器

相对于已有基线方法，ASO在以下两个核心维度上实现了根本性改变：

| 方法维度 | 基线方法 | ASO方法 |
|---------|---------|---------|
| **对抗图像风格** | 原始内容图像（无风格修改）或简单离线风格滤镜 | 通过GRPO微调的图像编辑模型生成的**对抗优化风格**（笔触密度、线条粗细等参数经强化学习自动寻优） |
| **攻击多样性** | 仅依赖内容维度漏洞（如**FigStep** Gong et al., AAAI 2025; **QR Attack** Liu et al., ECCV 2024）或非内容维度漏洞（如**SI Attack** Zhao et al., ICCV 2025） | **混合风格与内容触发器**，同时利用两个维度的脆弱性，形成复合攻击 |

这一“混合触发器”设计使得ASO能够将任意基于内容的攻击（如**HIMRD** Ma et al., ICCV 2025）升级为风格增强的复合攻击，大幅提升越狱成功率。消融实验（Table 4）证实，仅应用探查最优风格（+ Probing）仅带来微小ASR提升，而进一步应用GRPO增强（++ Enhance）带来了绝大部分的性能增益，验证了对抗优化是发挥风格潜力、创造强力攻击的核心因素。

### 3. 两阶段自动化风格优化框架

ASO的方法创新体现在其两阶段自动化流程：

- **第一阶段：风格敏感性探查（Style Sensitivity Probing）**。系统地从四个预定义风格类别池（Medium & Texture、Geometric Distortion、Thematic & Atmospheric、Domain-specific）中探查目标VLM最容易受到攻击的风格方向，选出ASR最高的候选风格。这一阶段将风格选择从人工试错转变为数据驱动的系统搜索。

- **第二阶段：基于GRPO的风格增强（GRPO-based Style Enhancement）**。利用动态批次GRPO算法微调图像编辑模型，在选中的风格空间内优化风格参数。核心技术创新包括：
  - **结构化分层奖励函数（Structurally-Tiered Reward Function）**：分段设计奖励信号——Level 1（模型拒绝时）根据接受/拒绝概率给出惩罚；Level 2（模型接受时）根据评判模型的有害/无害概率给出奖励，有效克服了稀疏奖励问题，为强化学习提供密集梯度信号。
  - **动态批次GRPO（DB-GRPO）**：维护未解决池和成功集合，使用分组相对优势归一化和PPO剪辑损失稳定更新策略参数，避免了传统RL训练中的不稳定性。

### 4. 与已有工作的本质区别

现有越狱攻击方法可分为两类：基于内容的攻击（通过精心设计的视觉或文本提示诱导模型违反安全策略）和基于非内容的攻击（利用输入扰动破坏模型对齐）。ASO的独特之处在于**首次将视觉风格作为可优化的对抗触发器**，并通过强化学习自动发现最优风格参数，而非依赖人工设计的固定风格滤镜。这一思路将风格从“辅助增强手段”提升为“核心攻击向量”，为多模态模型安全测试开辟了新的研究方向。

ASO 的整体 pipeline 由两个顺序阶段构成：**风格敏感性探查（Style Sensitivity Probing）** 与 **基于 GRPO 的风格增强（GRPO-based Style Enhancement）**，二者共同实现将任意基础越狱攻击图像升级为“混合触发器”的目标。框架的核心设计理念源于一个关键观察：MLLM 对非内容的视觉风格变化具有天然的敏感性，即使内容层面的攻击被安全机制拒绝，特定风格的叠加仍可能绕过防御（Figure 1）。

### 问题形式化与优化目标

给定一个基础越狱攻击数据集 $\mathcal{D}_{\text{base}} = \{(I_{\text{base},j}, P_{\text{harm},j})\}_{j=1}^N$，其中 $I_{\text{base},j}$ 是包含恶意文本指令的图像（如打字式提示或 QR 码），$P_{\text{harm},j}$ 是对应的有害文本提示，ASO 的目标是学习一个增强生成器 $\mathcal{G}$，使其对任意基础攻击图像施加风格变换后，能最大化目标 VLM $\mathcal{M}$ 的攻击成功率（ASR）：

$$
\mathcal{G}^{*} = \arg\max_{\mathcal{G}} \left( \frac{1}{N} \sum_{j=1}^{N} \mathcal{I}( \mathcal{M}( \mathcal{G}( I_{\text{base},j} ), P_{\text{harm},j} ), P_{\text{harm},j} ) \right)
$$

其中 $\mathcal{I}(\cdot)$ 是指示函数，当模型输出被判定为有害时返回 1。框架将 $\mathcal{G}$ 实现为一个可微调的图像编辑模型（如 InstructPix2Pix），其参数 $\Theta$ 控制风格变换的具体表现。

### 两阶段 Pipeline

**第一阶段：风格敏感性探查。** 该阶段的目标是从预定义的风格池中系统性地识别目标 VLM 最易受攻击的风格方向。风格池 $\mathcal{S}$ 由四个不相交的子集构成：$\mathcal{S}_{\text{med}}$（媒介与纹理，如铅笔素描、油画）、$\mathcal{S}_{\text{geo}}$（几何失真，如像素化、漩涡）、$\mathcal{S}_{\text{atm}}$（主题与氛围，如恐怖、阴森）、$\mathcal{S}_{\text{dom}}$（领域迁移，如漫画、3D 渲染）。对于每个候选风格 $S_i$，使用未经微调的生成器 $\mathcal{G}(\cdot; \Theta_0)$ 将基础数据集转换为风格化数据集 $\mathcal{D}_{\text{hybrid},i}$，并计算经验 ASR：

$$
\text{ASR}(S_i) = \frac{1}{N} \sum_{j=1}^{N} y_{i,j}
$$

选择 ASR 最高的风格 $S^*$ 作为后续增强阶段的搜索空间。此阶段的计算成本远低于第二阶段，但为后续优化提供了关键的初始化方向。

**第二阶段：基于 GRPO 的风格增强。** 在选定的最优风格 $S^*$ 上，通过强化学习微调生成器参数 $\Theta$，以最大化结构化分层奖励函数（Structurally-Tiered Reward Function）定义的期望回报：

$$
r_t(I_h, P_h) = \begin{cases} C_{\text{thresh}} + \log \frac{P_{\mathcal{M}}(\text{accept}| I_h, P_h)}{P_{\mathcal{M}}(\text{rejected}| I_h, P_h)} & \text{(if rejected)} \\ \max\left(\log \frac{P_{\mathcal{I}}(\textbf{yes}| R, P_h)}{P_{\mathcal{I}}(\textbf{no}| R, P_h)}, C_{\text{thresh}}\right) & \text{(if accepted)} \end{cases}
$$

该奖励函数分两级提供密集的梯度信号：当 VLM 拒绝回答时（Level 1），根据接受/拒绝概率的对数比给予惩罚（始终小于阈值 $C_{\text{thresh}} = -10$）；当 VLM 接受回答时（Level 2），由外部评判模型 $\mathcal{I}$ 评估回答 $R$ 的有害性，取有害性对数似然比与 $C_{\text{thresh}}$ 的最大值作为奖励。这种设计有效克服了越狱攻击中常见的稀疏奖励问题。

优化算法采用**动态批次 GRPO（DB-GRPO）**，维护一个未解决池（Unsolved Pool）和成功集合（Success Collection），在每轮迭代中从未解决池采样批次进行策略更新。优势函数 $A_i$ 直接在批次内对奖励进行均值-标准差归一化：

$$
A_i = \frac{r_i - \text{mean}(\{r_k\}_{k=1}^G)}{\text{std}(\{r_k\}_{k=1}^G)}
$$

策略参数通过 PPO 剪辑代理损失更新：

$$
\mathcal{L}(\Theta) = \hat{\mathbb{E}}_{j \in \mathcal{B}} \left[ \min\left( \rho_j A_j, \text{clip}(\rho_j, 1-\epsilon, 1+\epsilon) A_j \right) \right]
$$

其中 $\rho_j$ 为重要性采样比率。训练过程中，成功越狱的样本被移入成功集合，未解决的样本留在池中继续参与后续迭代，从而逐步提升整体 ASR。

### 模块关系与输入输出流

Figure 2 清晰展示了两个阶段的衔接关系：第一阶段以基础攻击数据集和风格池为输入，输出最优风格 $S^*$；第二阶段以 $S^*$、基础数据集、以及预训练的 VLM 和评判模型为输入，通过 DB-GRPO 循环输出微调后的生成器参数 $\Theta^*$。最终，$\mathcal{G}(\cdot; \Theta^*)$ 可作为即插即用的增强模块，对任意基础攻击图像施加优化的风格变换，生成混合触发器图像。消融实验（Table 4）证实，仅应用第一阶段探查的最优风格仅能带来微小的 ASR 提升，而第二阶段的 GRPO 增强贡献了绝大部分性能增益，验证了对抗优化是释放风格攻击潜力的核心因素。

![[assets/figures/papers/paper_list_l2028_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Adversarial_Style/figures/002_Figure_2.jpg]]
*Figure 2: Main framework of the proposed ASO method. The method consists of two stages: (1) Style Sensitivity Probing, and (2) GRPObased Style Enhancement*

### 两阶段框架总览

ASO 方法由两个顺序执行的阶段构成（Figure 2）：**风格敏感性探查** 与 **基于 GRPO 的风格增强**。整体目标为学习一个增强生成器 $\mathcal{G}$，将基础攻击图像 $I_{\text{base}}$ 转化为具有更高攻击成功率（ASR）的混合攻击图像 $I_{\text{hybrid}} = \mathcal{G}(I_{\text{base}})$。

优化目标形式化为：

$$
\mathcal{G}^{*} = \arg\max_{\mathcal{G}} \left( \frac{1}{N} \sum_{j=1}^{N} \mathcal{I}( \mathcal{M}( \mathcal{G}( I_{\text{base},j} ), P_{\text{harm},j} ), P_{\text{harm},j} ) \right)
$$

其中 $\mathcal{M}$ 为目标 VLM，$P_{\text{harm}}$ 为有害文本提示，$\mathcal{I}$ 为指示攻击是否成功的二值函数。

---

### 第一阶段：风格敏感性探查

#### 风格池构建

风格池 $S$ 由四个不相交的风格类别并集构成：

$$
S = S_{\text{med}} \cup S_{\text{geo}} \cup S_{\text{atm}} \cup S_{\text{dom}}
$$

四类风格分别对应四种攻击假设：**媒介与纹理**（如铅笔素描、油画）、**几何畸变**（如鱼眼、波浪）、**主题与氛围**（如哥特、赛博朋克）、**领域迁移**（如动漫、像素艺术）。

#### 探查流程

对每个候选风格 $S_i \in S$，使用未微调的生成器 $\Theta_0$ 将基础攻击数据集 $\mathcal{D}_{\text{base}}$ 转换为混合数据集：

$$
\mathcal{D}_{\text{hybrid},i} = \{ ( \mathcal{G}(I_{\text{base},j}, P_{\text{style},i}; \Theta_0), P_{\text{harm},j}) \}_{j=1}^N
$$

随后计算该风格的经验攻击成功率：

$$
\text{ASR}(S_i) = \frac{1}{N} \sum_{j=1}^{N} y_{i,j}
$$

其中 $y_{i,j} \in \{0,1\}$ 表示第 $j$ 个样本在风格 $S_i$ 下是否越狱成功。选择 ASR 最高的风格 $S^{*}$ 进入第二阶段。

---

### 第二阶段：基于 GRPO 的风格增强

#### 问题建模

将风格增强建模为强化学习问题：智能体的目标是学习最优策略参数 $\Theta^{*}$，最大化所选风格 $S^{*}$ 上的期望总奖励：

$$
\Theta^{*} = \arg\max_{\Theta} \left( \mathbb{E}_{(I_{\text{base}}, P_{\text{harm}}) \sim \mathcal{D}_{\text{base}}} \left[ r_t \right] \right)
$$

#### 结构化分层奖励函数

为克服稀疏奖励问题，设计分段奖励函数，根据 VLM 的响应状态提供密集梯度信号：

$$
r_t(I_h, P_h) = \begin{cases} 
C_{\text{thresh}} + \log \frac{P_{\mathcal{M}}(\text{accept}| I_h, P_h)}{P_{\mathcal{M}}(\text{rejected}| I_h, P_h)} & \text{(if rejected)} \\ 
\max\left(\log \frac{P_{\mathcal{I}}(\mathbf{yes}| R, P_h)}{P_{\mathcal{I}}(\mathbf{no}| R, P_h)}, C_{\text{thresh}}\right) & \text{(if accepted)} 
\end{cases}
$$

- **Level 1（拒绝时）**：基于 VLM 接受/拒绝概率的对数比给出惩罚，始终小于阈值 $C_{\text{thresh}} = -10$。
- **Level 2（接受时）**：基于评判模型 $\mathcal{I}$ 对回答 $R$ 有害性判断的 yes/no 对数概率比给出奖励，取下界为 $C_{\text{thresh}}$。

该设计使拒绝样本获得负奖励，接受样本根据有害程度获得正奖励，为策略优化提供连续梯度。

#### 动态批次 GRPO

训练采用 **Dynamic-Batch GRPO** 算法（Algorithm 1），维护**未解决池** $\mathcal{D}_{\text{unsolved}}$ 和**成功集合** $\mathcal{D}_{\text{success}}$。优势函数直接使用分层奖励 $r_j$，绕过学习价值函数的复杂性。

**优势归一化**：对批次内奖励进行均值-标准差归一化：

$$
A_i = \frac{r_i - \text{mean}(\{r_k\}_{k=1}^G)}{\text{std}(\{r_k\}_{k=1}^G)}
$$

**PPO 剪辑代理损失**：使用重要性采样和剪辑机制稳定更新策略参数：

$$
\mathcal{L}(\Theta) = \hat{\mathbb{E}}_{j \in \mathcal{B}} \left[ \min\left( \rho_j A_j, \text{clip}(\rho_j, 1-\epsilon, 1+\epsilon) A_j \right) \right]
$$

其中 $\rho_j$ 为新旧策略的概率比，$\epsilon$ 为剪辑超参数。

#### 有害性评分

作为补充评估指标，定义有害性评分衡量越狱回答的语义危害程度：

$$
\text{HS} = \log P_{\mathcal{I}}(\text{yes} | R, P_{\text{harm}}) - \log P_{\mathcal{I}}(\text{no} | R, P_{\text{harm}})
$$

该指标反映评判模型对回答有害性的对数似然比，与 ASR 配合使用以全面评估攻击质量。

![[assets/figures/papers/paper_list_l2028_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Adversarial_Style/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the Stylistic Sensitivity vulnerability in MLLMs. While a base SOTA attack (Top) is effectively refused by the Defender, MLLMs exhibit innate sensitivity to non-contentbased style modifications. Our framework (Bottom) exploits this by applying Image Style Transfer to create an optimized stylistic attack. This new input bypasses the safety mechanism, demonstrating that stylistic biases can be leveraged to significantly improve jailbreak ASR*

## 实验与关键发现

### 核心发现：风格增强的复合攻击显著提升越狱成功率

ASO 作为一个即插即用的增强模块，在多个基准测试和模型上一致地提升了现有 SOTA 越狱攻击的攻击成功率（ASR）。实验覆盖了开源模型（Qwen3-VL、LLaVA-OV-1.5）和商用模型（GPT-4.1-mini、Gemini-2.5-Flash），并针对四种基础攻击方法（FigStep、QR Attack、SI Attack、HIMRD）进行了系统验证。

**在 MM-SafetyBench 基准上**，ASO 为所有基础攻击带来了可观的 ASR 增益。以 Qwen3-VL 为例，QR Attack 的 ASR 从 38.99% 提升至 42.98%（+3.99%），SI Attack 从 39.31% 提升至 42.58%（+3.27%），HIMRD 从 87.38% 提升至 89.52%（+2.14%）。在 LLaVA-OV-1.5 上，增益更为显著：QR Attack 从 37.80% 提升至 44.35%（+6.55%），SI Attack 从 37.82% 提升至 44.25%（+6.43%），HIMRD 从 52.92% 提升至 55.42%（+2.50%）（Table 4）。商用模型同样表现出跨模型泛化能力，ASO 增强后的 QR Attack 在 GPT-4.1-mini 上达到 54.26%，在 Gemini-2.5-Flash 上达到 55.04%（Table 1）。

**在 VLBreakBench 基准上**，ASO 同样表现出稳健的增强效果，进一步验证了该方法在不同评估场景下的有效性（Table 2）。

### 细粒度分析：攻击提升具有跨类别一致性

为评估 ASO 是否存在类别偏差，论文在 MM-SafetyBench 的 13 个安全类别上进行了细粒度分析（Table 3）。结果显示，ASO 的 ASR 和有害性评分（HS）提升在所有类别上具有一致性和普适性，未出现明显的类别偏差。这表明风格增强攻击的效能不局限于特定安全领域，而是一种系统性的漏洞利用。

![[assets/figures/papers/paper_list_l2028_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Adversarial_Style/figures/005_Table_3.jpg]]
*Table 3: Fine-grained Attack Success Rate and Harmfulness Score breakdown on MM-SafetyBench categories*

有害性评分定义为评判模型给出的回答有害性对数似然比：

$$HS = \log P_{\mathcal{I}}(\text{yes} | R, P_{\text{harm}}) - \log P_{\mathcal{I}}(\text{no} | R, P_{\text{harm}})$$

该指标从语义层面量化了越狱回答的危害程度，与 ASR 形成互补评估维度。

### 消融实验：GRPO 增强阶段是性能提升的核心驱动力

消融实验严格验证了 ASO 两阶段框架的贡献（Table 4）。实验设置三个条件：
- **基础攻击**（Base）：仅使用原始内容攻击，不应用任何风格修改。
- **+ Probing**：仅应用第一阶段风格探查，使用未微调的图像编辑模型应用探查出的最优风格。
- **++ Enhance**：完整 ASO 流程，包括探查和 GRPO 风格增强。

![[assets/figures/papers/paper_list_l2028_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Adversarial_Style/figures/006_Table_4.jpg]]
*Table 4: Ablation study of different components*

结果表明，仅应用探查最优风格（+ Probing）仅能带来微小的 ASR 提升，而进一步应用 GRPO 增强（++ Enhance）带来了绝大部分的性能增益。这证实了对抗优化是发挥风格潜力、创造强力复合攻击的核心因素，而非单纯的风格选择。

### 失败模式与局限性

尽管 ASO 展现了强大的攻击增强能力，但论文未对以下潜在失败模式进行系统分析，需手动验证：

1. **风格过拟合风险**：GRPO 优化的风格参数可能对特定 VLM 过拟合，导致跨模型泛化能力下降。虽然实验显示了跨模型迁移效果，但不同 VLM 架构对风格的敏感性差异可能显著，且缺乏理论解释。
2. **物理世界迁移性**：实验仅在静态数字图像上验证，未考虑物理世界中的攻击迁移（如打印、拍摄后的图像），也未评估多轮对话场景下的攻击持续性。
3. **防御缺失**：论文未针对所发现的风格漏洞提出任何防御策略或缓解方案，这使得漏洞的严重性评估缺少对照基线。
4. **风格空间限制**：风格参数空间的大小和搜索效率受限于所选图像编辑模型架构，可能存在未被探查的更优风格方向。

### 关键图表结论

- **Table 1 / Table 2**：ASO 在 MM-SafetyBench 和 VLBreakBench 上一致提升所有基础攻击的 ASR，跨开源和商用模型均有效。
- **Table 3**：细粒度类别分析证实 ASO 的提升具有普适性，无类别偏差。
- **Table 4**：消融实验明确 GRPO 增强阶段是性能提升的核心来源，单纯风格探查仅提供边际增益。

![[assets/figures/papers/paper_list_l2028_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Adversarial_Style/figures/003_Table_1.jpg]]
*Table 1: Main results of ASO enhancement on the MM-SafetyBench benchmark*

![[assets/figures/papers/paper_list_l2028_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_Adversarial_Style/figures/004_Table_2.jpg]]
*Table 2: Main results of ASO enhancement on the VLBreakBench benchmark*

## 定位与知识库关联

### 攻击范式定位：从内容漏洞到风格不一致性

ASO 的核心贡献在于将VLM越狱攻击的探索空间从**内容语义**和**非内容结构**两个传统维度，扩展到了第三个维度——**视觉风格**。现有的SOTA攻击方法可以清晰地分为两类：

- **基于内容的攻击**：通过精心设计的视觉文本（如打字式提示）或编码信息（如QR码）直接向模型注入有害指令。代表方法包括 **FigStep** (Gong et al., AAAI 2025)、**QR Attack** (Liu et al., ECCV 2024) 和 **HIMRD** (Ma et al., ICCV 2025)。这类攻击的核心瓶颈在于：当文本内容被安全对齐机制识别后，攻击即告失败。

- **基于非内容的攻击**：利用图像的结构属性（如分块打乱）制造模型理解的不一致性。代表方法为 **SI Attack** (Zhao et al., ICCV 2025)。这类攻击不依赖显式的有害文本，但攻击面相对狭窄。

ASO 的独特定位在于：它不替代上述任何攻击，而是作为一个**即插即用的增强模块**（plug-and-play enhancement module），将风格触发器叠加到现有攻击图像之上，形成**混合触发器**（hybrid trigger）。这一设计利用了论文发现的核心瓶颈——MLLM的理解能力与安全防御机制之间存在**风格不一致性**：模型对图像内容的理解具有风格鲁棒性，但其安全防御机制却对特定视觉风格表现出脆弱敏感性。

### 方法谱系中的技术继承与创新

从技术路线上看，ASO 继承了三个关键的方法论传统：

1. **对抗风格迁移的直觉**：早期工作已暗示简单风格滤镜（如铅笔素描）可以影响VLM的决策边界。ASO 将这一经验观察系统化，通过两阶段框架将“手工挑选风格”升级为“自动探查+对抗优化风格参数”。

2. **GRPO强化学习框架**：ASO 采用的 Group Relative Policy Optimization 源自大语言模型对齐领域，但在越狱攻击场景中面临独特的**稀疏奖励问题**——只有当模型输出完整的越狱回答时才能获得有意义的反馈。ASO 通过**结构化分层奖励函数**（Structurally-Tiered Reward Function）解决了这一问题：在模型拒绝时（Level 1）利用接受/拒绝概率比给出惩罚信号，在接受时（Level 2）利用评判模型的有害性概率给出奖励信号，从而为强化学习提供了密集的梯度信息。

3. **动态批次训练策略**：DB-GRPO 算法维护未解决池和成功集合，使用分组相对优势归一化和PPO剪辑损失更新策略参数。这一设计使得训练过程能够自适应地聚焦于当前策略仍无法攻破的困难样本。

### 适用边界与泛化能力

ASO 的适用边界由以下因素界定：

- **模型架构兼容性**：实验覆盖了开源模型（Qwen3-VL、LLaVA-OV-1.5）和商用模型（GPT-4.1-mini、Gemini-2.5-Flash），显示出跨架构的泛化能力。但所有目标模型均为基于Transformer的视觉语言模型，未验证其在CNN-based或Mamba-based架构上的有效性。

- **攻击类型兼容性**：ASO 对基于内容的攻击（FigStep、QR Attack、HIMRD）和基于非内容的攻击（SI Attack）均能提供一致的ASR提升，表明风格增强具有攻击类型无关的普适性。

- **安全类别覆盖**：在MM-SafetyBench的13个安全类别上的细粒度分析（Table 3）显示，ASO的提升在所有类别上具有一致性，未出现明显的类别偏差，说明风格漏洞是跨安全领域的系统性弱点。

### 局限性与开放问题

#### 已识别的局限

1. **防御策略缺失**：论文仅作为红队测试工具揭示了风格漏洞，未提出任何针对性的防御或缓解方案。这使得该工作在负责任AI框架中的定位偏向攻击性。

2. **静态场景限制**：实验仅在静态图像上验证，未考虑物理世界中的迁移攻击（如打印-重拍场景）或多轮对话场景下的攻击持续性。实际部署中，攻击图像的风格可能在传输或采集过程中发生退化。

3. **风格空间的理论解释不足**：MLLM对特定风格的敏感性是否主要源于训练数据分布偏差，还是存在更深层的架构原因（如视觉编码器对纹理和形状的不同偏好），论文未给出理论分析。

4. **伦理讨论深度有限**：论文的伦理考量部分较为简短，未深入讨论此类攻击在实际部署中的滥用风险、检测方法及可能的监管框架。

#### 待探索的开放问题

1. **根本性防御机制**：能否设计一种对非内容触发器（包括风格、纹理、几何变换等）鲁棒的安全对齐机制，从根本上消除“风格不一致性”？这可能需要重新思考安全对齐的训练范式，将风格增广纳入安全微调过程。

2. **风格敏感性的深层原因**：MLLM对不同风格的敏感性差异是否与视觉编码器的归纳偏置有关？例如，CLIP系列编码器对纹理和形状的偏好是否系统性地影响了安全防御机制的脆弱点？

3. **不可察觉的对抗风格**：通过GRPO优化的风格参数是否可能收敛到对人类视觉系统不易察觉、但对VLM高度有效的恶意图像？这种“风格对抗样本”的可检测性如何？

4. **多模态扩展性**：该方法在视频（时序风格扰动）、语音（音色/语速作为“风格”）等多模态输入上的扩展性如何？混合触发器攻击是否会在更复杂的交互场景（如多模态对话智能体）中失效或被检测？

5. **红队测试与负责任的平衡**：如何在保持红队测试框架有效性的同时，防止风格优化技术被恶意利用？是否需要在发布此类工具时内置防御感知机制或使用限制？

### 知识库定位总结

ASO 在VLM越狱攻击的知识库中占据“**攻击增强层**”的定位——它不重新定义攻击范式，而是通过系统化的风格探查与对抗优化，将现有攻击的效率提升到新的上限。其核心知识贡献在于：揭示了视觉风格作为VLM安全防御的独立脆弱维度，并提供了可复现的自动化利用框架。这一发现对后续研究提出了两个方向性挑战：在攻击侧，如何进一步挖掘其他非内容属性（如构图、光照、色彩分布）的攻击潜力；在防御侧，如何构建对多维度视觉变化鲁棒的安全对齐机制。

## 原文 PDF

![[paperPDFs/CVPR_2026/Adversarial_Style_Optimization_Enhancing_VLM_Jailbreaks_by_GRPO_based_Stylistic_Triggers_Optimization.pdf]]
