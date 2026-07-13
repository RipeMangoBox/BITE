---
title: "SenseSearch: Empowering Vision-Language Models with High-Resolution Agentic Search-Reasoning via Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SenseSearch_Empowering_Vision_Language_Models_with_High_Resolution_Agentic_Search_Reasoning_via_Reinforcement_Learning.pdf
project_link: null
code_link: "https://github.com/OpenSenseNova/SenseNova-MARS"
aliases:
- SenseSearch
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过两阶段训练（冷启动SFT + RL）配合BN-GSPO算法，使模型能够自适应地整合文本搜索、图像搜索和图像裁剪工具，从而解决静态知识瓶颈并增强高分辨率感知能力。
primary_logic: 将多工具动作空间（文本搜索、图像搜索、图像裁剪）统一于一个代理RL框架，并通过BN-GSPO稳定训练，使视觉语言模型学会动态调用工具以完成知识密集型和高分辨率视觉推理。
claims:
- SenseSearch在HR-MMSearch上相比仅搜索或仅裁剪模型性能提升19.18%，展示了高分辨率搜索推理的有效性。
- SenseSearch-RL以57.43的平均分超越MMSearch-R1（52.49）4.94点，成为7B参数以下开源代理模型的新SOTA。
- BN-GSPO通过两层归一化优势估计稳定了多工具RL训练，并在纯RL设置下全面优于GRPO和GSPO。
- HR-MMSearch 上 相对提升 = 38.52 (SenseSearch-RL)
---

# SenseSearch: Empowering Vision-Language Models with High-Resolution Agentic Search-Reasoning via Reinforcement Learning

> [!tip] 核心洞察
> 将多工具动作空间（文本搜索、图像搜索、图像裁剪）统一于一个代理RL框架，并通过BN-GSPO稳定训练，使视觉语言模型学会动态调用工具以完成知识密集型和高分辨率视觉推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | SenseSearch：以强化学习赋能视觉语言模型的高分辨率代理式搜索-推理 |
| 英文题名 | SenseSearch: Empowering Vision-Language Models with High-Resolution Agentic Search-Reasoning via Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chng_SenseSearch_Empowering_Vision-Language_Models_with_High-Resolution_Agentic_Search-Reasoning_via_Reinforcement_CVPR_2026_paper.html) · [Code](https://github.com/OpenSenseNova/SenseNova-MARS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SenseSearch |
| Dataset | HR-MMSearch, MMSearch |

> [!tip] 效果简介
> - HR-MMSearch 上，相对提升 38.52 (SenseSearch-RL) vs crop-only / search-only models (+19.18%)。
> - 搜索导向基准平均 (MMSearch、V* Bench、HR-MMSearch) 上，Avg Score 57.43 (SenseSearch-RL) vs 52.49 (MMSearch-R1) (+4.94)。
> - MMSearch 上，Score 59.06 vs — (—)。

## 概要

### 问题背景与瓶颈

视觉语言模型（VLM）在知识密集型和高分辨率视觉任务中面临双重挑战。一方面，模型内部存储的静态知识有限，难以覆盖长尾实体与细粒度事实；另一方面，现有搜索型VLM（如**MMSearch-R1**，Wu et al., arXiv 2025）虽引入了文本搜索和图像搜索工具来获取外部知识，却缺乏对高分辨率图像的细粒度视觉分析能力，也无法有效协调多种工具（如搜索与裁剪），导致在高分辨率、知识密集场景下性能受限。

### 核心思路

SenseSearch 通过**统一的代理式强化学习框架**解决上述瓶颈。其核心洞察在于：将文本搜索、图像搜索和图像裁剪三类工具的动作空间统一于一个策略VLM，并通过两阶段训练（冷启动监督微调 + 强化学习）使模型学会动态调用工具以完成知识密集型和高分辨率视觉推理。具体而言：

- **工具集扩展**：在传统文本搜索与图像搜索之外，引入图像裁剪工具，使模型能够对高分辨率图像的局部区域进行缩放分析。
- **两阶段训练**：先通过约3k条高质量多轮交互轨迹进行冷启动SFT，再使用强化学习进行策略优化。
- **稳定RL算法**：提出**BN-GSPO**（批次归一化组序列策略优化），通过对优势估计施加两层归一化（组内标准化 + 跨minibatch标准化），有效缓解多工具RL训练中的奖励方差问题，使训练更加稳定。

### 主要结果

SenseSearch 在搜索导向和细粒度视觉理解基准上取得了领先性能：

- **HR-MMSearch**：SenseSearch-RL 相比仅搜索或仅裁剪的模型性能提升 **19.18%**，验证了高分辨率搜索推理的有效性。
- **搜索导向基准平均**：SenseSearch-RL 以 **57.43** 的平均分超越 MMSearch-R1（52.49）**4.94 点**，成为7B参数以下开源代理模型的新SOTA。
- **MMSearch**：SenseSearch 取得 **59.06** 的领先分数。
- **细粒度视觉理解**：SenseSearch-SFT 相比 Qwen2.5-VL-7B-Instruct SFT 在 HRBench-4K 等基准上平均提升 **+6.6 点**。

同时，消融实验表明 BN-GSPO 在纯RL设置下全面优于标准 GRPO 和 GSPO，且混合训练数据（搜索+裁剪任务）是学习统一多工具策略的关键。随着RL训练推进，模型学会更高效的工具调用策略，平均工具调用次数从约4次降至约2次。

### 方法谱系与知识库定位

SenseSearch 定位于**代理式搜索-推理VLM**的交叉地带，其方法谱系可沿两条轴定位：

1. **搜索型VLM轴**：以 MMSearch-R1 为代表，通过文本/图像搜索获取外部知识，但缺乏高分辨率感知能力。SenseSearch 在此基础上扩展了图像裁剪工具，并通过RL实现工具调用的端到端优化。
2. **高分辨率VLM轴**：以 **DeepEyes**（Zheng et al., ICLR 2026）和 **Pixel Reasoner**（Su et al., NeurIPS 2025）为代表，专注于像素空间的细粒度推理，但未整合搜索工具。SenseSearch 将高分辨率感知与外部知识检索统一于代理框架。

与 **Visual-ARFT**（Liu et al., ICCV 2025）和 **DeepMMSearch-R1**（Narayan et al., arXiv 2025）等多工具视觉推理代理相比，SenseSearch 首次在纯RL框架下同时优化三类工具调用，并通过 BN-GSPO 解决了多工具联合训练的稳定性问题。

视觉语言模型（VLM）在通用视觉问答上取得了显著进展，但在**高分辨率、知识密集型**场景中仍存在两个关键瓶颈：

**1. 静态知识瓶颈。** 传统VLM依赖预训练阶段内化的参数化知识，面对需要实时、细粒度或长尾外部知识的查询时，往往产生幻觉或过时答案。尽管近期工作（如 **MMSearch-R1**，Wu et al., arXiv 2025）引入了文本搜索与图像搜索工具来缓解这一问题，但其工具空间仍受限于检索操作，无法对高分辨率图像本身进行精细感知。

**2. 高分辨率感知瓶颈。** 真实场景中的图像（如4K分辨率）包含大量细节，直接缩放输入会导致关键视觉信息丢失。现有方法要么依赖单一搜索工具，要么依赖单一裁剪工具，缺乏在**跨工具协调**中动态决策的能力——即何时应检索外部知识、何时应放大图像局部区域进行细粒度分析。

**现有方案的结构性缺陷：** 搜索型代理VLM（如MMSearch-R1）和基于图像裁剪的VLM（如 **DeepEyes**，Zheng et al., ICLR 2026）各自解决了问题的一个侧面，但将二者割裂导致模型无法在“向外搜索”与“向内观察”之间进行自适应权衡。此外，将多工具动作空间统一到强化学习框架中面临**奖励方差大、训练不稳定**的挑战，标准GRPO/GSPO算法难以直接应对。

**本文动机：** 基于上述缺口，SenseSearch旨在构建首个端到端的代理式高分辨率VLM，通过强化学习统一文本搜索、图像搜索与图像裁剪三类工具，使模型在推理过程中学会动态调度工具，同时以稳定的RL算法支撑多工具策略的学习。

## 核心方法与创新机理

SenseSearch的核心创新在于将**高分辨率视觉感知**与**多工具代理式搜索推理**统一到一个端到端的强化学习框架中，解决了现有搜索型VLM的两大瓶颈：静态知识局限与细粒度视觉分析能力不足。其关键创新点可从以下三个维度理解。

### 1. 工具空间的扩展：从“搜索”到“搜索+裁剪”

现有搜索型代理模型（如**MMSearch-R1**，Wu et al., arXiv 2025）的工具集局限于文本搜索与图像搜索，无法对高分辨率图像中的局部细节进行针对性分析。SenseSearch首次将**图像裁剪工具**纳入代理动作空间，形成文本搜索、图像搜索、图像裁剪三类工具的协同体系。这一扩展的因果逻辑在于：知识密集型视觉问答往往需要同时调用外部知识（通过搜索）和定位图像中的关键区域（通过裁剪），单一工具范式无法覆盖此类复合需求。

### 2. 训练范式的重构：冷启动SFT + BN-GSPO强化学习

传统方法或仅依赖SFT（如**Visual-ARFT**，Liu et al., ICCV 2025），或直接应用标准RL算法（如GRPO），缺乏对多工具调用策略的专门优化。SenseSearch采用**两阶段训练流水线**：

- **冷启动SFT**：在约3k条高质量多轮交互轨迹上进行监督微调，为模型建立基本的工具调用格式与推理模式。该阶段仅微调语言模型，冻结视觉编码器与多模态投影器。
- **RL阶段（BN-GSPO）**：提出**批次归一化组序列策略优化**算法，这是对标准GSPO的关键改进。其核心机制是**两层优势归一化**——先在组内进行奖励标准化（GSPO的原有操作），再跨整个mini-batch对优势值进行二次标准化。这一设计的直接因果效应是**抑制多工具RL训练中的奖励方差**，使策略梯度更新更加稳定，从而让模型能够可靠地学习何时调用何种工具。

### 3. 数据策管：三阶段合成流水线

为支撑上述训练范式，SenseSearch设计了**数据挖掘→轨迹合成→质量验证**的三阶段数据生成流水线，专门生产包含多工具调用序列的高质量训练数据。这与直接使用现有多模态QA数据集的做法形成对比，后者缺乏工具调用的过程性标注。该流水线确保了冷启动SFT和RL训练数据中搜索与裁剪任务的混合分布，消融实验（Table 4）证实，混合数据是学习统一多工具策略的关键——仅用单一任务数据会导致对应任务性能下降。

### 创新点的协同关系

上述三个创新点并非孤立存在：工具空间的扩展定义了更丰富的动作空间，但也带来了更复杂的策略学习挑战；BN-GSPO正是为解决这一挑战而设计的稳定训练算法；而三阶段数据流水线则为整个训练过程提供了必要的监督信号。三者共同构成“**工具定义—算法优化—数据供给**”的闭环，使SenseSearch能够动态协调搜索与裁剪工具，在知识密集型和高分辨率视觉推理任务上取得突破性性能。

SenseSearch 的整体设计遵循“冷启动监督微调 + 强化学习”两阶段训练范式，将文本搜索、图像搜索与图像裁剪三类工具统一于一个代理式视觉语言模型（VLM）的动作空间中，使模型在多轮推理过程中能够自适应地选择并调用工具，以应对知识密集型与高分辨率视觉理解任务。

### 核心组件与信息流

系统由以下关键模块构成，其交互关系如 **Figure 2** 所示：

![[assets/figures/papers/paper_list_l2200_https_openaccess_thecvf_com_content_CVPR2026_html_Chng_SenseSearch_Empow/figures/002_Figure_2.jpg]]
*Figure 2: The illustration of SenseSearch RL training pipeline. SenseSearch adaptively invokes the image search, text search and image crop tools in the multi-turn reasoning process to obtain the final answer. The policy VLM is optimized by the BN-GSPO algorithm, driven by the format reward and answer reward*

1. **Policy VLM（策略模型）**  
   以 **Qwen2.5-VL-7B-Instruct**（Bai et al., arXiv 2025）为骨架，负责在每一轮推理中生成“思考-行动”序列：模型根据当前图像与历史上下文，决定是直接输出答案，还是调用某一工具（文本搜索、图像搜索或图像裁剪）。该模型是唯一被优化的策略载体。

2. **工具集（Toolset）**  
   相比现有搜索型代理（如 **MMSearch-R1**，Wu et al., arXiv 2025）仅支持文本搜索与图像搜索，SenseSearch 扩展了动作空间，加入 **图像裁剪工具**，使模型能够对高分辨率图像的局部区域进行放大分析。三类工具的功能边界如下：
   - **Text Search Tool**：执行基于文本的网络搜索，获取外部知识。
   - **Image Search Tool**：执行反向图像搜索，获取与查询图像相关的视觉信息。
   - **Image Crop Tool**：对图像指定区域进行裁剪，支持细粒度视觉检查。

3. **奖励模型（Reward Model）**  
   采用 LLM-as-a-judge 范式评估模型最终答案的准确性，并结合格式合规性，输出序列级标量奖励：
   $$R(\tau) = R_{acc}(\tau) + R_{format}(\tau)$$
   其中 $R_{acc}$ 衡量答案正确性，$R_{format}$ 约束输出格式的规范性。

4. **BN-GSPO 优化器**  
   在强化学习阶段，策略模型通过 **批次归一化组序列策略优化（BN-GSPO）** 算法进行更新。该算法在标准 GSPO 的基础上引入第二层跨 minibatch 的优势归一化，有效抑制多工具训练中的奖励方差，稳定梯度更新。

### 训练流程

SenseSearch 的训练分为两个阶段：

- **第一阶段：冷启动 SFT**  
  在精心筛选的多轮交互轨迹数据集 $\mathcal{D}_{SFT}$ 上进行监督微调，目标为最小化轨迹的负对数似然：
  $$\mathcal{L}_{SFT} = -\sum_{(x_i, y_i) \in \mathcal{D}_{SFT}} \log \pi_\theta(y_i \mid x_i)$$
  该阶段仅微调语言模型部分，视觉编码器与多模态投影层保持冻结。冷启动数据通过三阶段合成流水线生成：数据挖掘 → 轨迹合成 → 质量验证（**Figure 3**）。

- **第二阶段：RL with BN-GSPO**  
  在冷启动模型的基础上，使用 BN-GSPO 算法进行强化学习优化。核心机制为两层归一化优势估计：
  1. **组内归一化**（GSPO 原有）：在同一问题的一组采样轨迹内，对奖励进行均值-方差标准化，得到 $\bar{A}_{b,g}$。
  2. **批次归一化**（BN-GSPO 新增）：跨整个优化器 minibatch 再次标准化，得到 $\tilde{A}_{b,g}$：
     $$\tilde{A}_{b,g} = \frac{\bar{A}_{b,g} - \text{mean}(\{\bar{A}_{b',g'}\})}{\text{std}(\{\bar{A}_{b',g'}\})}$$
  
  最终优化目标为带剪切与 KL 惩罚的序列级 PPO 风格损失：
  $$\mathbb{E}_{x_b, \{y_{b,g}\}} \left[ \frac{1}{G} \sum_{g=1}^{G} \min\left(s_{b,g}(\theta) \tilde{A}_{b,g}, \text{clip}_{\epsilon_{low}}^{\epsilon_{high}}(s_{b,g}(\theta)) \tilde{A}_{b,g}\right) \right] - \beta D_{KL}(\pi_\theta \| \pi_{ref})$$
  其中 $s_{b,g}(\theta)$ 为按序列长度归一化的重要性比率：
  $$s_{b,g}(\theta) = \left( \frac{\pi_\theta(y_{b,g} \mid x_b)}{\pi_{\theta_{old}}(y_{b,g} \mid x_b)} \right)^{1/|y_{b,g}|}$$

### 设计逻辑

整个框架的核心因果关系在于：**多工具动作空间的统一** 解决了静态知识瓶颈与高分辨率感知不足的问题，而 **BN-GSPO 的两层归一化** 则保证了多工具联合训练的稳定性。消融实验证实，若仅使用单一任务数据（纯搜索或纯裁剪），对应任务的性能会显著下降；混合数据训练是学习统一多工具策略的关键。随着 RL 训练推进，模型学会更高效的工具调用策略，平均工具调用次数从约 4 次逐步降至约 2 次（**Figure 4**），表明策略模型确实内化了工具选择的效率意识。

![[assets/figures/papers/paper_list_l2200_https_openaccess_thecvf_com_content_CVPR2026_html_Chng_SenseSearch_Empow/figures/001_Figure_1.jpg]]
*Figure 1: Overview of SenseSearch. (a) SenseSearch tackles the challenging visual task by leveraging an integrated suite of text search, image search, and image crop tools within the reasoning process. (b) Our proposed HR-MMSearch benchmark characterized by the highresolution images, knowledge-intensive question and diverse scenes. (c) Comparison of VLMs on the search-oriented benchmarks*

### 3.1 工具空间与代理架构

SenseSearch 的核心代理模型是一个策略 VLM（基于 Qwen2.5-VL-7B-Instruct），其动作空间由三类工具组成：

- **文本搜索工具**：执行基于文本的网络搜索，获取外部知识以弥补模型的静态知识瓶颈。
- **图像搜索工具**：执行反向图像搜索，检索与输入图像相关的视觉信息。
- **图像裁剪工具**：对高分辨率图像的局部区域进行裁剪，支持细粒度视觉分析。这是 SenseSearch 相比现有搜索型代理 VLM（如 MMSearch-R1，其工具集仅限文本搜索与图像搜索）的关键扩展。

模型在多轮推理过程中自适应地调用上述工具，最终给出答案。整个训练流程如图 Figure 2 所示：策略 VLM 接收多模态输入后，生成推理步骤与工具调用指令；工具执行结果返回后，模型继续下一轮推理，直至输出最终答案。

### 3.2 冷启动监督微调

在第一阶段，SenseSearch 在精心筛选的多轮交互轨迹数据集 $\mathcal{D}_{\mathrm{SFT}}$ 上进行监督微调。SFT 阶段仅微调语言模型部分，视觉编码器和多模态投影器保持冻结。目标函数为标准的负对数似然：

$$
\mathcal{L}_{\mathrm{SFT}} = -\sum_{(x_i, y_i) \in \mathcal{D}_{\mathrm{SFT}}} \log \pi_{\theta}(y_i \mid x_i)
$$

其中 $x_i$ 为多模态输入，$y_i$ 为包含推理步骤与工具调用的完整多轮轨迹，$\pi_{\theta}$ 为策略 VLM。

### 3.3 BN-GSPO 强化学习算法

第二阶段采用本文提出的**批次归一化组序列策略优化**（Batch-Normalized Group Sequence Policy Optimization, BN-GSPO）进行强化学习训练。BN-GSPO 是对标准 GSPO 的扩展，通过两层归一化优势估计来稳定多工具 RL 训练。

#### 3.3.1 序列级奖励建模

每条完整轨迹 $\tau$ 的总奖励由两部分组成：

$$
R(\tau) = R_{\mathrm{acc}}(\tau) + R_{\mathrm{format}}(\tau)
$$

- $R_{\mathrm{acc}}$：答案准确性奖励，由 LLM-as-a-judge 评估最终答案的正确性。
- $R_{\mathrm{format}}$：格式合规奖励，确保模型输出符合预定义的工具调用格式。

#### 3.3.2 长度归一化重要性比

对于批次 $b$ 中的第 $g$ 条生成序列，定义按序列长度归一化的策略概率比：

$$
s_{b,g}(\theta) = \left( \frac{\pi_{\theta}(y_{b,g} \mid \boldsymbol{x}_b)}{\pi_{\theta_{\mathrm{old}}}(y_{b,g} \mid \boldsymbol{x}_b)} \right)^{1/|y_{b,g}|}
$$

其中 $\pi_{\theta_{\mathrm{old}}}$ 为旧策略，$|y_{b,g}|$ 为序列长度。长度归一化旨在消除长序列因累积概率积过小而导致的优势估计偏差。

#### 3.3.3 两层归一化优势估计

**第一层：组内归一化（GSPO 标准操作）**。在同一组 $\mathcal{G}$ 内，对 $G$ 条序列的原始奖励进行标准化：

$$
\bar{A}_{b,g} = \frac{r_{b,g} - \mathrm{mean}(\{r_{b,g'}\}_{g'=1}^{G})}{\mathrm{std}(\{r_{b,g'}\}_{g'=1}^{G})}
$$

**第二层：跨批次归一化（BN-GSPO 核心创新）**。在 GSPO 的基础上，对整个优化器 minibatch $\mathcal{B}$ 内的所有组归一化优势值再次进行标准化：

$$
\tilde{A}_{b,g} = \frac{\bar{A}_{b,g} - \mathrm{mean}(\{\bar{A}_{b',g'}\}_{b' \in \mathcal{B}, g' \in \mathcal{G}})}{\mathrm{std}(\{\bar{A}_{b',g'}\}_{b' \in \mathcal{B}, g' \in \mathcal{G}})}
$$

这一设计有效缓解了多工具动作空间下奖励方差过大的问题，使 RL 训练更加稳定。

#### 3.3.4 剪切序列级目标

最终优化目标采用带剪切和 KL 惩罚的 PPO 风格形式：

$$
\mathbb{E}_{\boldsymbol{x}_b, \{y_{b,g}\}} \left[ \frac{1}{G} \sum_{g=1}^{G} \min\left( s_{b,g}(\theta) \tilde{A}_{b,g},\; \mathrm{clip}_{\epsilon_{\mathrm{low}}}^{\epsilon_{\mathrm{high}}}(s_{b,g}(\theta)) \tilde{A}_{b,g} \right) \right] - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}})
$$

其中 $\mathrm{clip}_{\epsilon_{\mathrm{low}}}^{\epsilon_{\mathrm{high}}}$ 为双端剪切操作，$\beta D_{\mathrm{KL}}$ 为与参考策略 $\pi_{\mathrm{ref}}$ 的 KL 散度惩罚项，用于防止策略更新幅度过大。

### 3.4 冷启动数据合成流水线

冷启动 SFT 和 RL 训练数据通过三阶段合成流水线生成（Figure 3）：

![[assets/figures/papers/paper_list_l2200_https_openaccess_thecvf_com_content_CVPR2026_html_Chng_SenseSearch_Empow/figures/003_Figure_3.jpg]]
*Figure 3: Cold-start data generation pipeline. It consists of data mining, trajectory synthesis and quality verification*

1. **数据挖掘**：从现有数据源中筛选适合搜索与裁剪任务的高质量样本。
2. **轨迹合成**：为每个样本生成包含工具调用的多轮交互轨迹。
3. **质量验证**：通过自动评估和人工审核过滤低质量轨迹，确保训练数据的可靠性。

该流水线最终产出约 3k 条多轮轨迹用于冷启动 SFT，以及混合搜索与裁剪任务的 RL 训练数据。

## 实验与关键发现

### 实验设置

SenseSearch 以 **Qwen2.5-VL-7B-Instruct**（Bai et al., arXiv 2025）为基础骨架，采用两阶段训练流水线：冷启动 SFT 后接 BN-GSPO 强化学习。SFT 阶段仅微调语言模型，冻结视觉编码器与多模态投影仪，学习率为 $1 \times 10^{-5}$；RL 阶段学习率降至 $1 \times 10^{-6}$。训练数据通过三阶段合成流水线（数据挖掘→轨迹合成→质量验证）生成约 3k 条多轮交互轨迹。

评测覆盖两类基准：**搜索导向基准**（MMSearch、V\* Bench、HR-MMSearch）和**细粒度视觉理解基准**（HRBench-4K 等）。对比方法包括直接回答模式、RAG 工作流以及代理式模型（**MMSearch-R1** (Wu et al., arXiv 2025)、**DeepEyes** (Zheng et al., ICLR 2026)、**Pixel Reasoner** (Su et al., NeurIPS 2025)、**Visual-ARFT** (Liu et al., ICCV 2025)、**DeepMMSearch-R1** (Narayan et al., arXiv 2025) 等），同时纳入商业模型 **Gemini-2.5-Flash** (Comanici et al., arXiv 2025) 与 **GPT-4o-mini**。

### 主实验结果

**搜索导向任务。** 如表 1 所示，SenseSearch-RL 在三个搜索导向基准上取得 **57.43 的平均分**，超越 MMSearch-R1（52.49）达 **4.94 点**，成为 7B 参数以下开源代理模型的新 SOTA；同时以 11.78 点的优势大幅领先 GPT-4o-mini（45.65）。其中 MMSearch 单项得分 **59.06**，处于领先地位。

在专门构建的高分辨率搜索基准 HR-MMSearch 上，SenseSearch-RL 达到 **38.52 分**，相比仅搜索或仅裁剪的模型**相对提升 19.18%**，验证了多工具协同（文本搜索 + 图像搜索 + 图像裁剪）对高分辨率、知识密集型视觉推理的关键作用。

**细粒度视觉理解。** 如表 2 所示，SenseSearch-SFT 在 HRBench-4K 等基准上取得 **72.8 的平均分**，较 Qwen2.5-VL-7B-Instruct 的 SFT 基线**提升 6.6 点**，表明冷启动 SFT 阶段已能有效注入细粒度感知能力。

### 消融研究

**BN-GSPO 算法有效性。** 表 3 对比了不同 RL 算法在纯 RL 设置下的表现。BN-GSPO 通过两层归一化优势估计——组内标准化（GSPO 原始操作）叠加跨 minibatch 的批次标准化——有效缓解了多工具 RL 训练中的奖励方差问题，在所有基准上取得最佳综合性能，全面优于标准 GRPO 和 GSPO。

**训练数据分布影响。** 表 4 消融了 RL 训练数据的任务构成。仅用搜索任务数据或仅用裁剪任务数据均会导致对应缺失任务上的性能下降；使用完整的混合数据集（搜索 + 裁剪）在搜索导向指标上取得最优结果，证明**混合训练是学习统一多工具策略的必要条件**。

**工具调用效率演化。** 如 Figure 4 所示，随着 RL 训练推进，SenseSearch 的平均工具调用次数从约 **4 次**稳定下降至约 **2 次**，表明模型学会了更高效的工具调用策略，在保持性能的同时减少冗余交互。

### 失败模式与局限

论文未系统性报告失败案例或错误模式。从实验设计推断，潜在局限包括：① 工具调用依赖预定义的动作空间，面对未覆盖的工具类型时泛化能力未知；② 奖励模型基于 LLM-as-a-judge，其评估偏差可能影响 RL 训练方向；③ 高分辨率裁剪工具的实际效果受限于底层视觉编码器的分辨率上限。以上需在后续工作中进行针对性验证。

![[assets/figures/papers/paper_list_l2200_https_openaccess_thecvf_com_content_CVPR2026_html_Chng_SenseSearch_Empow/figures/004_Table_1.jpg]]
*Table 1: Performance on search-oriented benchmarks under Direct Answer, RAG Workflow, and Agentic Model workflows*

![[assets/figures/papers/paper_list_l2200_https_openaccess_thecvf_com_content_CVPR2026_html_Chng_SenseSearch_Empow/figures/005_Figure_4.jpg]]
*Figure 4: Analysis of tool use behavior. Top: Distribution of tool calls across different benchmarks. Bottom Left: The tool use number in different benchmarks. Bottom Right: Evolution of tool call frequency in the RL training process, indicating that SenseSearch learns more efficient tool invocation strategies*

![[assets/figures/papers/paper_list_l2200_https_openaccess_thecvf_com_content_CVPR2026_html_Chng_SenseSearch_Empow/figures/006_Table_2.jpg]]
*Table 2: Performance on visual understanding benchmarks*

## 定位与知识库关联

### 1. 在搜索型视觉语言模型谱系中的位置

SenseSearch 处于**代理式搜索型视觉语言模型**这一新兴分支。该分支的核心命题是：让视觉语言模型在推理过程中主动调用外部工具（尤其是搜索引擎）来弥补静态参数知识的不足，并增强对高分辨率图像的细粒度感知。

**与上游基线的关系：**

- **MMSearch-R1**（Wu et al., arXiv 2025）是该方向的开创性工作，首次将强化学习引入搜索型VLM训练，但其工具空间仅限于文本搜索与图像搜索两类。SenseSearch 在此基础上将工具空间扩展为三类（增加图像裁剪工具），并在训练算法上从标准GSPO改进为BN-GSPO，最终在搜索导向基准平均分上以57.43超越MMSearch-R1的52.49（+4.94点），成为7B参数以下开源代理模型的新SOTA。

- **DeepEyes**（Zheng et al., ICLR 2026）和**Pixel Reasoner**（Su et al., NeurIPS 2025）分别代表了“基于图像思考”和“像素空间推理”的路线，它们关注细粒度视觉理解但未整合搜索工具。SenseSearch 在视觉理解基准（HRBench-4K等）上以72.8的平均分超越Qwen2.5-VL-7B-Instruct的SFT基线（+6.6点），表明搜索-裁剪联合训练并未损害基础视觉能力，反而带来了增益。

- **Visual-ARFT**（Liu et al., ICCV 2025）和**DeepMMSearch-R1**（Narayan et al., arXiv 2025）探索了多工具视觉推理代理，但SenseSearch的差异化在于：首次将图像裁剪作为一等工具纳入RL训练的动作空间，并通过BN-GSPO解决了多工具联合训练中的奖励方差问题。

- 与商业模型**GPT-4o-mini**和**Gemini-2.5-Flash**（Comanici et al., arXiv 2025）相比，SenseSearch-RL在搜索导向基准上平均领先GPT-4o-mini达11.78点，展示了开源小模型在代理式搜索推理上的竞争力。

### 2. 方法适用边界

**适用场景：**
- 需要外部知识检索的视觉问答（如识别罕见地标、特定产品型号）
- 高分辨率图像中的细粒度目标定位与分析（如遥感图像、医学影像、工业检测）
- 多轮推理中需要动态切换搜索与视觉放大策略的任务

**边界条件：**
- SenseSearch 基于 Qwen2.5-VL-7B-Instruct 骨架，其视觉编码器的分辨率上限决定了图像裁剪工具的有效粒度。对于超出编码器原生分辨率的极端细节，裁剪策略的收益会递减。
- 冷启动SFT阶段仅使用约3k条多轮轨迹，数据规模较小，可能对长尾场景的覆盖不足。
- 论文未报告在纯文本推理或非视觉搜索任务上的性能，因此方法在非多模态场景下的泛化性尚待验证。

### 3. 局限与开放问题

**已识别的局限：**
- 工具集目前限定为三类（文本搜索、图像搜索、图像裁剪），尚未扩展到更丰富的工具生态（如计算器、代码解释器、数据库查询等）。
- 奖励模型采用LLM-as-a-judge方案，其评估偏差和与人类判断的一致性未做系统性分析。
- 论文未讨论多工具并发调用或工具调用失败的恢复机制，这在真实部署中可能成为瓶颈。

**开放问题：**
- BN-GSPO的两层归一化是否在其他工具组合或更大规模模型上同样有效，仍需跨架构验证。
- 冷启动数据的合成流水线依赖三阶段质量验证，其自动化程度和可复现性细节在论文中未充分展开。
- 图像裁剪工具的调用策略（何时裁剪、裁剪区域如何确定）是否可以通过RL自发涌现更优的启发式规则，是一个值得深入的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/SenseSearch_Empowering_Vision_Language_Models_with_High_Resolution_Agentic_Search_Reasoning_via_Reinforcement_Learning.pdf]]
