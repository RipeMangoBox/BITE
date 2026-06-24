---
title: ALERT Motion Autonomous LLM Enhanced Adversarial Attack for Text to Motion
type: paper
paper_level: A
venue: AAAI
year: 2025
pdf_ref: paperPDFs/AAAI_2025/ALERT_Motion_Autonomous_LLM_Enhanced_Adversarial_Attack_for_Text_to_Motion.pdf
aliases:
- AM
- AMALEAATM
tags:
- AAAI_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用大语言模型（LLM）的常识推理能力自动生成对抗提示，并通过多模态信息对比（MMIC）模块提取运动语义特征，指导LLM进行迭代扩展、精炼和更新，从而生成既自然又高效的对抗提示。
primary_logic: 让LLM自主执行对抗提示的搜索过程（扩展、精炼、更新），无需人工定义操作，能够生成更自然且符合运动语义的对抗提示；同时利用MMIC模块提供的运动相似性反馈，使生成的对抗提示在保持低可检测性的同时产生与目标运动高度相似的输出。
claims:
- ALERT-Motion通过LLM代理自主生成对抗提示，不依赖预定义规则，生成的提示更自然流畅，且产生的运动更接近目标。
- 在100个目标运动的综合实验中，ALERT-Motion的PPL降至119.58（RIATIG为1389.67），AS降至0.08（RIATIG为0.12），FID降至4.17（RIATIG为7.41），攻击自然度和成功率均显著优于基线。
- MMIC模块通过运动编码器计算余弦相似度，为LLM提供运动语义反馈，指导搜索过程。
- 攻击过程完全由LLM代理通过扩展、精炼、更新的指令驱动，无需人工设计操作。
---

# ALERT Motion Autonomous LLM Enhanced Adversarial Attack for Text to Motion

> [!tip] 核心洞察
> 让LLM自主执行对抗提示的搜索过程（扩展、精炼、更新），无需人工定义操作，能够生成更自然且符合运动语义的对抗提示；同时利用MMIC模块提供的运动相似性反馈，使生成的对抗提示在保持低可检测性的同时产生与目标运动高度相似的输出。

| 字段 | 内容 |
|------|------|
| 中文题名 | ALERT Motion：面向文本生成运动的自主大语言模型对抗攻击 |
| 英文题名 | ALERT Motion Autonomous LLM Enhanced Adversarial Attack for Text to Motion |
| 会议/期刊 | AAAI 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ALERT-Motion |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D (100 target motions) 上，FID↓ 4.17 vs 7.41 (RIATIG) (-3.24)；PPL↓ 119.58 vs 1389.67 (RIATIG) (-1270.09)；AS↓ 0.08 vs 0.12 (RIATIG) (-0.04)。

## 概述

文本生成运动（Text-to-Motion, T2M）模型在给定自然语言描述时能够合成高质量的人体动作序列，但其对抗鲁棒性尚未得到充分检验。现有针对T2M的对抗攻击方法（如**RIATIG**, Liu et al., CVPR 2023）依赖预定义的字符级或词级扰动操作，生成的对抗提示往往缺乏自然流畅性，且难以捕捉与目标运动语义相关的关键信息，导致攻击的隐蔽性和成功率均不理想。这一瓶颈的根源在于：攻击搜索空间受限于人工设计的离散操作，无法充分利用运动模态的语义反馈来指导提示的生成。

**ALERT-Motion** 针对上述瓶颈提出了一个基于大语言模型（LLM）自主代理的黑盒对抗攻击框架。其核心思路是：让LLM代理自主执行对抗提示的搜索过程——通过扩展、精炼、更新三个进程迭代优化提示，无需预定义任何扰动规则；同时，引入多模态信息对比（Multimodal Information Contrastive, MMIC）模块，利用运动编码器提取生成运动与目标运动的语义特征并计算余弦相似度，将运动语义反馈组织为文本信息注入LLM的推理循环，从而引导代理生成既自然流畅又与目标运动高度相关的对抗提示。

该方法在方法谱系中的定位清晰：它改变了对抗提示生成的范式——从“预定义操作+搜索”转向“LLM自主推理+多模态语义反馈驱动”。在知识库层面，ALERT-Motion将T2M对抗攻击与LLM代理、多模态对比学习相融合，为运动生成安全领域开辟了新的攻击向量。

主要实验结果验证了该方法的有效性。在HumanML3D数据集上对100个目标运动进行综合评估，ALERT-Motion在攻击自然度指标PPL上降至119.58（RIATIG为1389.67，降低约91.4%），在攻击成功率指标AS上降至0.08，在生成运动质量指标FID上降至4.17，同时R-1召回率提升至27/100。这些结果表明，ALERT-Motion在保持低可检测性的同时，能够诱使受害者模型生成与目标运动高度相似的输出，攻击性能全面优于现有基线方法。定性分析（Figure 1、Figure 3、Figure 4）进一步显示，ALERT-Motion生成的对抗提示在语言自然度和运动语义相关性上均显著优于RIATIG。

然而，该方法仍存在若干局限：攻击效果依赖特定LLM（GPT-3.5-turbo-instruct）的推理能力；仅在HumanML3D数据集和MDM、MLD两个T2M模型上验证，跨数据集和跨架构的泛化性尚待检验；对抗提示自然度的评估依赖GPT-2的PPL指标，可能与人类感知存在偏差。此外，论文未提出具体的防御机制，如何针对此类LLM驱动的自动对抗攻击设计有效的防御策略，仍是开放的研究问题。

## 背景与动机

### 文本到运动生成的安全隐患

文本到运动（Text-to-Motion, T2M）生成技术近年来取得了显著进展，使得用户仅需自然语言描述即可驱动三维人体运动合成。然而，这类模型在实际部署中暴露出严重的安全脆弱性：攻击者可通过精心构造的对抗性提示（adversarial prompts），诱导模型生成与恶意意图相符的运动序列，同时绕过内容审核机制。这一威胁在动作驱动的虚拟人、影视制作、游戏交互等场景中尤为突出——被操控的运动输出可能被滥用于生成暴力、色情或其他不当内容，而现有的文本侧过滤手段难以察觉此类语义层面的操纵。

### 现有对抗攻击方法的根本缺陷

当前针对T2M模型的对抗攻击方法普遍沿用了文本到图像领域的思路，其核心瓶颈在于**依赖预定义的字符级或词级操作**。以代表性基线方法**RIATIG**（Liu et al., CVPR 2023）为例，该方法的攻击范式可概括为：在原始提示文本上执行固定的扰动操作（如字符替换、单词插入/删除），并通过迭代搜索寻找能使生成结果逼近目标运动的扰动组合。

这一范式存在三个结构性缺陷：

1. **自然度崩塌**：预定义操作本质上是文本表面的机械扰动，生成的对抗提示往往语法破碎、语义断裂。在HumanML3D数据集上的100个目标运动实验中，RIATIG生成的对抗提示其困惑度（PPL）高达1389.67，表明文本几乎不可读，极易被基于语言模型的检测器识别。

2. **运动语义盲区**：字符/词级操作完全不考虑运动模态的语义约束。攻击者无法获知当前对抗提示所生成的运动与目标运动之间的语义距离，导致搜索过程缺乏有效引导，陷入低效的随机试探。

3. **操作空间受限**：预定义操作集合的离散性和有限性，使得对抗提示的生成被限制在一个狭小的文本空间内，难以覆盖那些需要更深层语义变换才能触发的模型脆弱性。

### 核心动机：让语言模型自主理解并执行攻击

上述缺陷的根源在于：现有方法将对抗攻击视为一个**文本表面的搜索问题**，而非**语义层面的推理与生成问题**。本文的核心动机在于转变这一范式——利用大语言模型（LLM）的常识推理与语言生成能力，使其自主地理解攻击目标、感知运动语义反馈，并动态地执行对抗提示的生成与优化。

这一思路的关键洞察是：LLM本身具备丰富的世界知识和语言操控能力，只需为其提供恰当的指令框架和多模态反馈信息，它就能像人类攻击者一样，在不依赖任何预定义操作的情况下，生成既自然流畅又与目标运动语义高度相关的对抗提示。这种**自主性**从根本上消除了传统方法对人工设计操作的依赖，同时将攻击的隐蔽性和成功率提升到新的水平。

## 核心创新

### 从预定义操作到LLM自主搜索：对抗提示生成范式的根本转变

现有T2M对抗攻击方法（如**RIATIG**（Liu et al., CVPR 2023）、**MacPromp**）依赖预定义的字符级或词级操作（替换、插入、删除等）来扰动原始提示，这种机械式修改存在两个结构性缺陷：一是生成的对抗提示往往不自然、不流畅，容易被检测；二是操作过程完全脱离运动语义，无法保证扰动后的提示能引导模型生成与目标运动相似的输出。

ALERT-Motion的核心创新在于**将对抗提示生成从“预定义操作搜索”转变为“LLM自主推理搜索”**。具体而言，方法通过自适应调度（Adaptive Dispatching, AD）模块构建一个基于LLM的攻击代理，仅需设计三条自然语言指令（扩展、精炼、更新），LLM便能自动理解攻击目标并执行相应的搜索操作，无需任何人工预定义的操作规则。这一转变的关键因果机制在于：LLM具备常识推理与语言生成能力，能够在保持文本自然流畅的前提下，创造性地生成与运动语义相关的对抗提示，从根本上解决了攻击隐蔽性与语义相关性的矛盾。

### 多模态运动语义反馈：闭合LLM搜索与运动空间的语义鸿沟

仅靠LLM的语言能力不足以确保生成的提示能有效攻击T2M模型，因为LLM无法直接感知运动模态的语义信息。ALERT-Motion的第二个关键创新是引入**多模态信息对比（Multimodal Information Contrastive, MMIC）模块**，构建了从运动空间到文本空间的语义反馈回路。

MMIC模块利用预训练的运动编码器 $E_m$ 提取生成运动与目标运动的语义特征，通过余弦相似度量化二者的运动语义相似性：

$$s^{\mathrm{m}}(G(p), m_t) = \frac{E_m(G(p)) \cdot E_m(m_t)}{\|E_m(G(p))\| \|E_m(m_t)\|}$$

该相似度信息被组织为结构化文本，注入LLM的更新（Update）进程中，作为运动语义的“奖励信号”指导LLM迭代优化对抗提示。这一设计的深层洞察在于：**将多模态语义对齐问题转化为LLM可理解的文本反馈，使得语言代理能够在保持自然度的同时，朝着运动相似度最大化的方向搜索**。在更新步骤中，LLM接收拼接了当前提示集与MMIC相似度信息的输入，依据更新指令 $I_U$ 生成新的对抗提示（见公式 $S_{2k+1} \gets \mathrm{LLM}(I_U, \mathrm{cat}(S_{2k}, S_{2k}'))$），从而在每一次迭代中同时优化文本自然度和运动攻击效果。

### 三阶段搜索机制：扩展-精炼-更新的协同设计

AD模块将LLM的搜索过程划分为三个协同的阶段，通过状态转移函数 $S_{k+1} \gets \mathrm{LLM}(I, S_k)$ 驱动，并根据时间步奇偶性交替存储提示集状态：

- **扩展（Expansion）**：从初始提示 $S_0$ 出发，LLM依据扩展指令 $I_E$ 生成多样化的候选对抗提示集 $S_1$，扩大搜索空间。
- **精炼（Refinement）**：对奇数步状态 $S_{2k-1}$ 中的提示进行质量筛选与修正，确保其满足攻击约束（文本相似度低于阈值 $\eta$），输出精炼后的提示集 $S_{2k}$。
- **更新（Update）**：结合MMIC模块提供的运动相似度反馈，LLM依据更新指令 $I_U$ 对精炼提示进行语义增强，生成新的对抗提示集 $S_{2k+1}$，进入下一轮迭代。

这一三阶段设计的核心优势在于**搜索的自主性与闭环优化**：扩展保证多样性，精炼保证攻击约束，更新利用运动语义反馈提升攻击效果，三者形成完整的自主搜索闭环。与RIATIG等依赖固定操作集的方法相比，ALERT-Motion无需人工定义任何原子操作，LLM代理自主决定每一步的修改策略，生成的对抗提示在PPL（自然度）上从RIATIG的1389.67降至119.58，在攻击成功率（AS）上从0.12降至0.08，在FID（运动质量）上从7.41降至4.17（Table 4, 100目标运动实验），充分验证了该创新范式的有效性。

## 整体框架

ALERT-Motion 采用**黑盒设定下的双模块流水线架构**，其核心设计理念是：**将对抗提示的搜索过程完全委托给大语言模型（LLM）自主执行，同时通过多模态运动语义反馈来引导搜索方向**，从而摆脱传统方法对预定义字符/词级操作规则的依赖。

### 核心瓶颈与设计动机

现有 T2M 对抗攻击方法（如 **RIATIG**, Liu et al., CVPR 2023）依赖预定义的字符或词级扰动操作来修改文本提示。这类方法存在两个根本性缺陷：一是生成的对抗提示往往不自然、不流畅，容易被检测；二是缺乏对运动模态语义的感知能力，无法保证攻击产生的运动与目标运动在语义上相似。这导致攻击的**隐蔽性不足**和**成功率受限**。

ALERT-Motion 的因果调节旋钮在于：**利用 LLM 的常识推理与语言生成能力，将对抗搜索建模为 LLM 代理的自主决策过程**，同时引入运动语义相似度作为反馈信号，使代理能够迭代优化对抗提示，在保持文本自然度的前提下最大化运动相似性。

### 双模块流水线

整体框架由两个关键模块串联构成，数据流从输入到输出依次经过以下阶段：

**1. 多模态信息对比模块 (Multimodal Information Contrastive, MMIC)**

该模块负责提取运动语义特征并计算相似度，为后续的 LLM 代理提供反馈信号。具体流程为：
- 将当前对抗提示 $p$ 输入受害者 T2M 模型 $G$，得到生成运动 $G(p)$。
- 使用预训练的运动编码器 $E_m$ 分别编码生成运动 $G(p)$ 和目标运动 $m_t$，提取高维语义特征。
- 计算两者的余弦相似度作为运动语义相似度：
  $$s^{\mathrm{m}}(G(p), m_t) = \frac{E_m(G(p)) \cdot E_m(m_t)}{\|E_m(G(p))\| \|E_m(m_t)\|}$$
- 将相似度信息组织为结构化文本，供 LLM 代理推理使用。

**2. 自适应调度模块 (Adaptive Dispatching, AD)**

该模块构建 LLM 代理，通过三个进程的迭代循环搜索最优对抗提示。状态转移由 LLM 根据指令驱动：
$$S_{k+1} \gets T(S_k, a_k) = \mathrm{LLM}(I, S_k)$$
其中 $S_k$ 为当前状态（候选提示集），$a_k$ 为当前动作（扩展/精炼/更新），$I$ 为对应的指令文本。

三个进程按时间步奇偶性交替执行：

- **扩展 (Expansion)**：从初始提示 $S_0$ 出发，LLM 根据扩展指令 $I_E$ 生成多样化的候选对抗提示集 $S_1$：
  $$S_1 \gets \mathrm{LLM}(I_E, S_0)$$

- **精炼 (Refinement)**：在奇数时间步生成的提示集基础上，LLM 根据精炼指令 $I_R$ 过滤和优化，确保提示满足攻击约束（如文本相似度低于阈值 $\eta$）：
  $$S_{2k} \gets \mathrm{LLM}(I_R, S_{2k-1})$$

- **更新 (Update)**：将 MMIC 模块提供的运动相似度反馈信息 $S_{2k}'$ 与当前精炼后的提示集 $S_{2k}$ 拼接，LLM 根据更新指令 $I_U$ 生成新的对抗提示，向更高运动相似度方向搜索：
  $$S_{2k+1} \gets \mathrm{LLM}(I_U, \mathrm{cat}(S_{2k}, S_{2k}'))$$

### 输入输出流

- **输入**：目标运动 $m_t$、目标提示 $p_t$（即生成目标运动的原始文本）、初始提示 $p_0$。
- **中间循环**：LLM 代理在扩展→精炼→更新的循环中不断生成候选对抗提示，每次更新后由 MMIC 模块评估运动相似度并反馈。
- **输出**：满足约束条件（文本相似度 $s^{\mathrm{p}}(p, p_t) < \eta$）且运动相似度最大化的最优对抗提示 $p^*$：
  $$p^{\star} = \arg\max_{p \in P} s^{\mathrm{m}}(G(p), m_t), \quad \text{s.t. } s^{\mathrm{p}}(p, p_t) < \eta$$

### 与传统方法的范式差异

| 对比维度 | 传统方法 (如 RIATIG) | ALERT-Motion |
|---------|---------------------|--------------|
| 提示生成范式 | 预定义的字符/词级操作与搜索 | LLM 代理自主执行扩展、精炼、更新 |
| 运动语义感知 | 无 | MMIC 模块提供运动相似性反馈 |
| 提示自然度 | 低（PPL 高达 1389.67） | 高（PPL 仅 119.58） |
| 攻击成功率 | 较低（AS 为 0.12） | 更高（AS 降至 0.08） |

> **证据强度说明**：上述框架描述基于论文 Section 3 的完整方法论阐述及 Algorithm 1 的伪代码，置信度 0.95。定量对比数据来自 Table 4 的 100 次综合实验统计，置信度 0.95。关于 LLM 具体指令内容（$I_E, I_R, I_U$）的细节需查阅原文补充材料，此处不展开。

### 补充图表

![[assets/figures/papers/paper_list_l1820_ALERT_Motion_Autonomous_LLM_Enhanced_Adversarial_Attack_for_Text_to_Moti/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed ALERT-Motion. ALERT-Motion operates in a black-box setting with two key modules: multimodal information integration module for consolidating information from text and motion into a unified format, and autonomous AD module that learns and executes adversarial prompt search through progresses of expansion, refinement, and update*

## 核心模块与公式推导

### 问题形式化

ALERT-Motion 将针对文本生成运动（T2M）模型的对抗攻击定义为一个约束优化问题：

$$p ^ { \star } = \arg \operatorname* { m a x } _ { p \in P } s ^ { \mathrm { m } } \left( G ( p ) , m _ { t } \right) , \mathrm { ~ s . t . ~ } s ^ { \mathrm { p } } \left( p , p _ { t } \right) < \eta$$

其中 $p_t$ 为目标运动 $m_t$ 对应的原始文本提示，$G(\cdot)$ 为受害者 T2M 生成模型，$P$ 为候选对抗提示空间。优化目标是在文本相似度 $s^p(p, p_t)$ 低于阈值 $\eta$ 的约束下，最大化生成运动与目标运动的语义相似度 $s^m(G(p), m_t)$。这一双重约束同时保证了攻击的隐蔽性（对抗提示与原始提示差异小）和有效性（生成运动与目标运动高度相似）。

### 多模态信息对比（MMIC）模块

MMIC 模块负责提取运动语义特征，为 LLM 代理的搜索过程提供反馈信号。其核心是运动语义相似度的计算：

$$s ^ { \mathrm { m } } ( G ( p ) , m _ { t } ) = { \frac { E _ { m } ( G ( p ) ) \cdot E _ { m } ( m _ { t } ) } { \| E _ { m } ( G ( p ) ) \| \| E _ { m } ( m _ { t } ) \| } }$$

其中 $E_m(\cdot)$ 为预训练的运动编码器，将运动序列映射到语义特征空间。该模块计算生成运动 $G(p)$ 与目标运动 $m_t$ 的余弦相似度，并将相似度信息组织为结构化文本，供 LLM 在后续更新步骤中推理使用。这一设计使语义层面的运动相似性得以转化为 LLM 可理解的语言信号，从而指导对抗提示的迭代优化。

### 自适应调度（AD）模块

AD 模块是整个攻击框架的核心，它将对抗提示的搜索过程建模为 LLM 驱动的状态转移系统。状态转移函数定义为：

$$S _ { k + 1 } \gets T ( S _ { k } , a _ { k } ) = \mathrm { L L M } \big ( I , S _ { k } \big )$$

其中 $S_k$ 为第 $k$ 步的状态（即当前候选对抗提示集合），$a_k$ 为当前执行的操作，$I$ 为对应操作的指令文本。状态的定义按时间步奇偶性区分：

$$S _ { k } = { \left\{ \begin{array} { l l } { \left\{ p _ { 0 } \right\} } & { { \mathrm { i f ~ } } k = 0 } \\ { \left\{ p _ { 1 } , . . . , p _ { n } \right\} } & { { \mathrm { i f ~ } } k ( { \bmod { 2 } } ) = 0 } \\ { \left\{ p _ { 1 } ^ { \prime } , . . . , p _ { n } ^ { \prime } \right\} } & { { \mathrm { i f ~ } } k ( { \bmod { 2 } } ) = 1 } \end{array} \right. }$$

AD 模块将攻击过程分解为三个递进的操作阶段：

**扩展（Expansion）：** 从初始提示 $p_0$ 出发，LLM 根据扩展指令 $I_E$ 生成多样化的候选对抗提示集：

$$S _ { 1 } \gets \mathrm { L L M } ( I _ { E } , S _ { 0 } )$$

**精炼（Refinement）：** 对当前候选集中的每个提示，LLM 根据精炼指令 $I_R$ 进行语义调整，确保其满足攻击的约束条件：

$$S _ { 2 k } \gets \mathrm { L L M } ( I _ { R } , S _ { 2 k - 1 } )$$

**更新（Update）：** 将 MMIC 模块计算的运动相似度信息 $S_{2k}'$ 与当前精炼后的提示集拼接，LLM 根据更新指令 $I_U$ 生成新一轮的对抗提示：

$$S _ { 2 k + 1 } \gets \mathrm { L L M } ( I _ { U } , \mathrm { c a t } ( S _ { 2 k } , S _ { 2 k } ^ { \prime } ) )$$

### 约束条件：文本相似度

对抗提示的隐蔽性通过文本相似度约束来保证，使用通用句子编码器（Universal Sentence Encoder）$E_t$ 计算：

$$s ^ { \mathrm { p } } ( p _ { t } , p ) = { \frac { E _ { t } ( p _ { t } ) \cdot E _ { t } ( p ) } { \| E _ { t } ( p _ { t } ) \| \| E _ { t } ( p ) \| } }$$

该余弦相似度衡量对抗提示 $p$ 与原始提示 $p_t$ 的语义偏离程度，只有低于阈值 $\eta$ 的候选提示才被视为有效攻击。这一约束与运动相似度最大化目标共同构成了完整的对抗攻击优化框架。

### 补充图表

![[assets/figures/papers/paper_list_l1820_ALERT_Motion_Autonomous_LLM_Enhanced_Adversarial_Attack_for_Text_to_Moti/figures/001_Figure_1.jpg]]
*Figure 1: Adversarial prompt against T2M model with RIATIG and our ALERT-Motion. Previous methods like RIATIG only perturb prompts through predefined character or word operations, overlooking the integrity and semantics of the prompts. Our ALERT-Motion doesn’t require such predefined operations; instead, by multimodal information contrastive (MMIC) module, the language model autonomously learn and perform these operations, dynamically generating adversarial prompts that meet the attack requirements. Under the same input (target and initial prompt), our method captures more natural and fluent prompts related to motion. When these prompts are used to query the victim T2M model, the resulting motion sho...*

## 实验与分析

### 实验设置

实验基于 **HumanML3D (H3D)** 数据集，包含 14,616 个运动序列和 44,970 条文本描述。受害者模型选用在该数据集上预训练的 **MLD** 和 **MDM** 两个代表性 T2M 模型。所有攻击方法统一使用 **GPT-3.5-turbo-instruct** 作为底层 LLM，迭代次数固定为 50，候选集大小设为 20，运动相似度阈值 $\eta = 0.4$。评估采用标准自动化指标，在 T2M evaluation model 和 **TMR** 两个独立的评估模型上进行，确保公平对比。

### 主要结果

**Table 1** 展示了在 T2M 评估模型上针对 MDM 和 MLD 的对抗攻击性能对比。ALERT-Motion 在所有核心指标上均显著优于基线方法 **MacPromp** 和 **RIATIG** (Liu et al., CVPR 2023)：

- **运动质量指标（FID↓ / dMM↓）**：ALERT-Motion 在 MLD 上取得 FID 8.881、dMM 5.016；在 MDM（100 steps）上取得 FID 5.843、dMM 4.117，均优于两个基线。这表明生成的对抗运动与目标运动在分布和动态特征上更接近。
- **自然度指标（PPL↓）**：ALERT-Motion 的 PPL 在 MLD 上仅为 113.223，而 RIATIG 高达 1389.67；在 MDM 上为 179.496，远低于 RIATIG 的 1389.67。PPL 的急剧下降说明 LLM 自主生成的对抗提示在语言流畅性上远胜于基于字符/词级扰动的传统方法。
- **隐蔽性指标（AS↓）**：ALERT-Motion 的对抗相似度 AS 在 MLD 上为 0.067，在 MDM 上为 0.075，均低于 RIATIG（0.12），表明对抗提示与原始提示的语义差异更小，更不易被检测。

**Table 2** 进一步在 TMR 评估模型上验证攻击效果。ALERT-Motion 在 R-precision 指标上表现突出：在 MLD 上 R-1 达 8/20，R-2 达 9/20，R-3 达 10/20；在 MDM 上 R-1 达 7/20，R-2 达 12/20，R-3 达 15/20。更高的 R-precision 表明生成的对抗运动在语义检索空间中与目标运动的文本描述高度匹配，从跨模态语义对齐角度印证了攻击的有效性。

### 大规模验证与稳定性分析

**Table 4** 报告了在 100 个额外目标运动上的综合实验结果。ALERT-Motion 的 FID 降至 4.17（RIATIG 为 7.41），PPL 降至 119.58（RIATIG 为 1389.67），AS 降至 0.08（RIATIG 为 0.12），R-1 提升至 27/100（RIATIG 为 22/100）。这一大规模实验确认了方法在多样目标上的统计显著性优势。

**Table 3** 分析了不同目标运动选择下评估指标的均值和方差。ALERT-Motion 在各指标上不仅均值更优，方差也更小，说明其对目标运动的选择不敏感，攻击性能稳定可靠。

### 定性分析

**Figure 3** 和 **Figure 4** 分别展示了针对 MDM 和 MLD 的对抗攻击结果示例。从运动渲染图像可见，ALERT-Motion 生成的对抗运动在姿态序列和运动轨迹上与目标运动高度一致，而 MacPromp 和 RIATIG 的结果则出现明显偏差。同时，ALERT-Motion 生成的对抗提示语言自然流畅，与运动语义高度相关，验证了 MMIC 模块提供的运动语义反馈对 LLM 搜索过程的有效指导。

### 失败模式与局限性

尽管 ALERT-Motion 在整体指标上表现优异，但仍存在以下局限：

1. **LLM 依赖性**：方法依赖 GPT-3.5-turbo-instruct 的推理能力，LLM 自身的性能波动可能影响攻击效果。当 LLM 对运动语义的理解不足时，生成的对抗提示可能偏离目标。
2. **数据集与模型泛化性**：仅在 HumanML3D 数据集和 MDM、MLD 两个模型上验证，未测试在 AMASS 等其他数据集或不同架构模型上的表现，跨域迁移能力尚需验证。
3. **自然度评估的局限**：PPL 基于 GPT-2 计算，其衡量标准可能不完全匹配人类对自然语言的主观感知，部分 PPL 较低的提示在实际阅读中仍可能略显生硬。
4. **无防御机制验证**：论文仅讨论了潜在的防御策略（如对抗训练、输入过滤），但未进行实验验证，无法评估方法在防御场景下的鲁棒性。

### 公平性说明

所有对比实验在相同条件下进行：统一的 LLM 模型、迭代次数、候选集大小和相似度阈值。评估采用标准自动化指标（FID、dMM、PPL、AS、R-precision），避免人工主观偏见。在两个不同的受害者模型（MLD 和 MDM）及两个独立的评估模型（T2M evaluation model 和 TMR）上交叉验证，确保结论的可靠性。

### 补充图表

![[assets/figures/papers/paper_list_l1820_ALERT_Motion_Autonomous_LLM_Enhanced_Adversarial_Attack_for_Text_to_Moti/figures/005_Table_1.jpg]]
*Table 1: The results of the adversarial attacks against MDM and MLD on T2M evaluation model. The first row, labeled “Target Motion”, represents the motion generated by the corresponding victim models, which are the targets of our attack. The quality of these indicators depends solely on the capabilities of the generation models and evaluation models. The second and third rows correspond to the baseline models MacPromp and RIATIG that we select. The final row represents the performance of our proposed method, ALERT-Motion*

![[assets/figures/papers/paper_list_l1820_ALERT_Motion_Autonomous_LLM_Enhanced_Adversarial_Attack_for_Text_to_Moti/figures/006_Table_2.jpg]]
*Table 2: Attack performance on TMR evaluation model*

![[assets/figures/papers/paper_list_l1820_ALERT_Motion_Autonomous_LLM_Enhanced_Adversarial_Attack_for_Text_to_Moti/figures/007_Table_3.jpg]]
*Table 3: The mean and variance of evaluation metrics under different selections of target motion*

![[assets/figures/papers/paper_list_l1820_ALERT_Motion_Autonomous_LLM_Enhanced_Adversarial_Attack_for_Text_to_Moti/figures/008_Table_4.jpg]]
*Table 4: The attack performance of 100 additional experiments*

![[assets/figures/papers/paper_list_l1820_ALERT_Motion_Autonomous_LLM_Enhanced_Adversarial_Attack_for_Text_to_Moti/figures/003_Figure_3.jpg]]
*Figure 3: Examples of adversarial attack results against MDM. The first row of text provides the true annotations for each column of target motions, and the first row of motions corresponds to their respective target motions. The following three rows of text correspond to the adversarial prompts obtained by MacPromp, RIATIG, and our proposed ALERT-Motion. The motion-rendered images below the text depict the motions generated by querying the victim model with the adversarial prompts. Darker color indicates later frames in the sequence*

![[assets/figures/papers/paper_list_l1820_ALERT_Motion_Autonomous_LLM_Enhanced_Adversarial_Attack_for_Text_to_Moti/figures/004_Figure_4.jpg]]
*Figure 4: Examples of adversarial attack results against MLD. The first row of text provides the true annotations for each column of target motions, and the first row of motions corresponds to their respective target motions. The following three rows of text correspond to the adversarial prompts obtained by MacPromp, RIATIG, and our proposed ALERT-Motion. The motion-rendered images below the text depict the motions generated by querying the victim model with the adversarial prompts. Darker color indicates later frames in the sequence*

## 方法谱系与知识库定位

### 问题定位：T2M对抗攻击的瓶颈与突破

文本生成运动（Text-to-Motion, T2M）领域的对抗攻击研究尚处于早期阶段。现有方法的核心瓶颈在于：它们依赖预定义的字符级或词级操作（如替换、删除、插入）来扰动输入提示，这类操作忽视了文本的语义完整性和运动模态的语义关联，导致生成的对抗提示不自然、可检测性高，且攻击成功率有限。例如，**RIATIG**（Liu et al., CVPR 2023）最初为文本生成图像设计，将其迁移至T2M时，其固定的扰动策略无法感知运动语义，生成的对抗提示在自然度（PPL高达1389.67）和运动相似性（FID为7.41）上均表现不佳。

ALERT-Motion的因果调节变量（causal knob）是将对抗提示的搜索过程从“人工预定义操作”转变为“LLM自主推理与迭代优化”。其核心洞察在于：大语言模型（LLM）具备常识推理和文本生成能力，若能为其提供运动语义的反馈信号，LLM可以自主执行扩展（Expansion）、精炼（Refinement）和更新（Update）三个进程，生成既自然流畅又与目标运动高度相似的对抗提示。这一范式转换使得攻击从“规则驱动的扰动”升级为“语义驱动的自主搜索”。

### 方法谱系中的位置

在T2M对抗攻击的方法谱系中，ALERT-Motion处于从“预定义操作攻击”向“LLM自主代理攻击”演进的关键节点：

- **前代方法（预定义操作范式）**：以**MacPromp**和**RIATIG**为代表。MacPromp采用固定的提示修改策略；RIATIG通过字符/词级搜索空间进行对抗样本生成，但两者均未利用运动模态的语义信息，生成的对抗提示在自然度和攻击效果上存在明显短板。
- **本工作（LLM自主代理范式）**：ALERT-Motion首次将LLM作为对抗攻击的自主代理，通过多模态信息对比（MMIC）模块提取运动语义特征作为反馈信号，驱动LLM在扩展-精炼-更新的循环中迭代搜索最优对抗提示。这一框架无需人工设计具体操作，LLM根据指令和反馈自主决定如何修改提示。
- **后续可能方向**：基于LLM代理的攻击框架可扩展至其他多模态生成任务（如文本生成图像、文本生成音频）；引入更强的LLM或更精细的运动语义对齐模块可能进一步提升攻击效果；同时，该框架也为防御机制的设计提供了明确的攻击面参考。

### 适用边界与泛化性

ALERT-Motion的适用边界由以下因素界定：

1. **受害者模型**：方法在基于扩散的**MDM**和基于潜在空间的**MLD**两个代表性T2M模型上验证有效，表明其对不同架构的生成模型具有一定泛化性。然而，论文未测试在其他模型架构（如自回归模型、流模型）或更大规模模型上的表现。
2. **数据集**：所有实验均在**HumanML3D**数据集上进行。该数据集包含14,616个运动序列和44,970条文本描述，涵盖日常人类动作。方法在其他运动数据集（如AMASS、KIT-ML）上的泛化性尚未验证，需要人工补充验证。
3. **LLM依赖**：攻击效果依赖于LLM的推理能力。论文使用**GPT-3.5-turbo-instruct**作为代理LLM。当换用能力较弱的LLM时，生成的对抗提示质量可能下降；换用更强LLM时，攻击效果可能进一步提升，但论文未进行相关消融实验。
4. **黑盒设定**：方法假设攻击者只能通过API查询受害者模型获取生成的运动，无法访问模型参数或梯度，这符合实际部署场景的威胁模型。

### 关键局限与开放问题

**已识别的局限**：

1. **LLM性能瓶颈**：方法依赖特定LLM（GPT-3.5-turbo-instruct）的推理能力，LLM自身的局限性（如幻觉、推理错误）可能影响对抗提示的质量和攻击成功率。论文未对比不同LLM对攻击效果的影响。
2. **自然度评估的局限性**：对抗提示的自然度通过GPT-2的困惑度（PPL）衡量，但PPL作为自动指标，可能无法完全反映人类对文本自然度的感知，存在评估偏差。
3. **防御机制的缺失**：论文仅讨论了潜在的防御策略（如对抗训练、提示过滤），但未提出具体的防御机制，也未通过实验验证任何防御方案的有效性。
4. **数据集和模型的有限验证**：仅在HumanML3D数据集和两个T2M模型上验证，未测试跨数据集、跨模型架构的迁移攻击能力。

**开放问题**：

1. **防御机制设计**：如何针对基于LLM代理的自动对抗攻击，设计有效的防御机制？对抗训练、提示净化、运动语义一致性检测等策略的可行性需要系统验证。
2. **跨模型迁移性**：LLM生成的对抗提示是否具有跨受害者模型的迁移能力？即针对MDM生成的对抗提示，能否同样有效地攻击MLD或其他未见模型？
3. **自然度量化**：如何更准确地量化对抗提示的“自然度”和“运动相关性”？是否需要引入人工评估或更先进的语言模型来弥补PPL的不足？
4. **数据增强与鲁棒性**：增加训练数据的规模和多样性，能否实质性地提升T2M模型的鲁棒性，从而降低对抗攻击的成功率？
5. **实际部署风险**：在开源T2M模型中，是否应引入更严格的内容审核或API访问控制，以防范基于LLM的对抗攻击被滥用于生成恶意内容？

## 原文 PDF

![[paperPDFs/AAAI_2025/ALERT_Motion_Autonomous_LLM_Enhanced_Adversarial_Attack_for_Text_to_Motion.pdf]]