---
title: "CoNavBench: Collaborative Long-Horizon Vision-Language Navigation Benchmark"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CoNavBench_Collaborative_Long_Horizon_Vision_Language_Navigation_Benchmark.pdf
project_link: https://navcraft.github.io/
code_link: null
openreview_forum_id: bMrH2PFMsi
aliases:
- CoNavBench
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "通过两阶段生成平台NavCraft将长程单智能体任务分解为带交接点的多智能体协作调度，并利用场景图约束进行严格效率验证，仅在协作缩短主智能体负载时才采纳协作方案。"
primary_logic: "多机器人协作导航的核心在于将长程任务并行化，通过接力机制减少整体耗时，但需借助场景图进行空间可达性验证和负载比较，以确保协作收益大于额外协调开销。"
claims:
- "CoNavBench是首个系统性的协作长程VLN基准，包含4048个单/多智能体episodes和协作类型分类。"
- "NavCraft通过两阶段层级代理生成协作任务：NavCraft-S生成单智能体基任务，NavCraft-C将其提升为多智能体协作调度。"
- "协作策略在步骤级成功率上比单智能体提升18.11%（相对提升）。"
- "在步骤级协议下，微调的3B模型将成功率从29.65%提升至35.02%。"
---

# CoNavBench: Collaborative Long-Horizon Vision-Language Navigation Benchmark

> [!tip] 核心洞察
> 多机器人协作导航的核心在于将长程任务并行化，通过接力机制减少整体耗时，但需借助场景图进行空间可达性验证和负载比较，以确保协作收益大于额外协调开销。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CoNavBench：协作长程视觉语言导航基准 |
| 英文题名 | CoNavBench: Collaborative Long-Horizon Vision-Language Navigation Benchmark |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=bMrH2PFMsi) · [Project](https://navcraft.github.io/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | NavCraft |
| Dataset | CoNavBench Step-by-step Subtasks |

> [!tip] 效果简介
> - CoNavBench Step-by-step Subtasks 上，SR↑ 为 35.02 (Collaborative Qwen2.5-VL-3B Finetuned)，对比 29.65 (Single-Agent Qwen2.5-VL-3B Finetuned)，变化 +5.37 (+18.11% 相对提升)。
> - CoNavBench Step-by-step Subtasks 上，SPL↑ 为 16.88 (Collaborative Qwen2.5-VL-3B Finetuned)，对比 13.81 (Single-Agent Qwen2.5-VL-3B Finetuned)，变化 +3.07。
> - CoNavBench Step-by-step Subtasks 上，NE↓ 为 5.79 (Collaborative Qwen2.5-VL-3B Finetuned)，对比 6.74 (Single-Agent Qwen2.5-VL-3B Finetuned)，变化 -0.95。

## 概要

**问题瓶颈**：现有视觉语言导航（VLN）基准与系统均局限于单智能体顺序执行范式。当任务路径较长时，单机器人必须依次完成所有子任务，导致总耗时线性增长且存在大量空闲等待。多机器人并行协作天然具备缩短完成时间的潜力，但此前缺少对协作场景中任务交接时机、路径交接区域以及机器人间干扰的系统建模与评估基准。

**核心思路**：本文提出协作长程视觉语言导航基准 **CoNavBench**，并构建自动化数据生成平台 **NavCraft**。其核心洞察在于：多机器人协作导航的关键是将长程任务并行化，通过接力机制减少整体耗时，但必须借助场景图进行空间可达性验证和负载比较，确保协作收益大于额外协调开销。NavCraft 采用两阶段层级代理——首先生成单智能体长程基任务，再将其提升为带明确交接点的双智能体协作调度，仅当主智能体路径负载严格缩短时才采纳协作方案。

**方法定位**：NavCraft 以 Habitat-Sim 中构建的语义增强场景图为规划蓝图，通过实例近邻投票（IPV）和邻域一致性校正实现区域标注，并利用基于场景图的效率工具库统一进行可达性、距离和负载验证。CoNavBench 包含 4,048 个单/多智能体 episodes，覆盖 10 类家居目标物体和两种协作交接类型（Type-A1：助手取物交接、主智能体送达；Type-A2：主智能体取物交接、助手送达），平均跨类别协作效率增益约 20%。

**主要结果**：在步骤级子任务协议下，微调的 Qwen2.5-VL-3B 模型在协作模式下成功率达 35.02%，相比单智能体基线 29.65% 提升 5.37 个百分点（相对提升 18.11%），SPL 从 13.81 提升至 16.88，导航误差 NE 从 6.74 降至 5.79。零样本模型在高等级指令下成功率极低（仅 4.30%），微调后升至 12.90%，表明视觉语言模型在长程协调推理方面仍有较大提升空间。

视觉语言导航（VLN）旨在使具身智能体依据自然语言指令在三维环境中移动并完成指定任务。近年来，VLN 基准在指令复杂度、任务长度和场景多样性上持续扩展，从单步目标导航演进至长程多阶段任务。然而，现有基准和系统均基于**单智能体顺序执行**范式：无论指令多么冗长、子任务多么分散，仅由一台机器人按序完成所有阶段（Figure 1a）。这一设计导致两个根本性瓶颈：

1. **长程任务的时间膨胀**：当指令包含多个空间上分离的子目标时，单智能体需依次遍历所有位置，大量时间消耗在路径移动和闲置等待上，整体完成时间（makespan）与路径总长度线性增长。
2. **协作潜力的系统性浪费**：多机器人系统可通过并行执行和任务接力（handoff）显著缩短总耗时，但现有 VLN 基准完全未建模协作场景中的**任务交接时机**、**路径交接区域**以及**机器人间干扰**，导致研究者无法评估和优化协作导航策略。

从基准对比看（Table 1），现有 VLN 基准（如 R2R、REVERIE、SOON、CVDN 等）在任务类型上覆盖了单智能体的目标导航、物体导航和对话导航，但均缺乏协作任务支持。CoNavBench 填补了这一空白：它是首个系统性的协作长程 VLN 基准，包含 4048 个单/多智能体 episode，并提供图级别的场景标注与协作类型分类，控制交接风格和会合模式。

本文的核心动机在于：**将多机器人协作的并行优势引入 VLN 领域，通过接力机制将长程任务分解为可并行执行的子任务，从而在理论上缩短整体完成时间**。然而，协作并非总是有益的——引入辅助机器人会带来额外的协调开销（状态同步、交接等待、路径冲突等）。因此，协作的采纳必须以严格效率验证为前提：仅当协作方案**严格缩短主智能体的路径负载**时，才接受协作调度。这一准则构成了 CoNavBench 和其数据生成平台 NavCraft 的设计基石。

Figure 2 的基准统计揭示了协作的潜在收益：跨目标类别的协作效率增益（相对于单智能体基线）平均约为 **20%**，且增益分布因类别而异，表明协作效益与任务结构高度相关。这一观察进一步强化了系统性建模协作场景的必要性——不同类别的任务对协作的敏感度不同，需要基准提供多样化的协作类型和场景配置以支持通用性评估。

## 核心方法与创新机理

CoNavBench与NavCraft的核心创新在于将协作长程视觉语言导航从“单智能体顺序执行”的既有范式，推进为“多智能体并行接力”的新范式。这一转变并非简单的数量扩展，而是围绕**任务并行化、协作收益验证与场景图约束调度**三个层面构建了系统性解决方案。

### 1. 协作长程VLN基准的首次系统性构建

此前VLN基准（如R2R、REVERIE、SOON、LH-VLN等）均局限于单智能体设置，缺乏对多机器人协作场景的建模与评估。CoNavBench首次填补了这一空白，其核心创新体现在两个维度：

- **任务结构创新**：将长程指令分解为多阶段协作子任务，明确指定主智能体与辅助智能体的角色分工、交接区域（handoff region）与汇合模式（rendezvous pattern），并定义了Type-A1（辅助机器人取物→交接→主机器人送达）与Type-A2（主机器人取物→交接→辅助机器人送达）两类规范化的接力模式。
- **协作采纳准则**：协作并非无条件引入。NavCraft-C仅在辅助机器人能够**严格缩短主智能体自身路径负载**时才接受协作方案，即满足 $\min\{J_{r_1}^{\mathrm{A1}}, J_{r_1}^{\mathrm{A2}}\} < C_{\mathrm{solo}}$。这一准则从机制上避免了“为协作而协作”的低效情况——消融实验证实，若跳过此验证直接生成双智能体任务，常导致一个机器人几乎闲置，单机器人顺序执行反而更高效（Figure 17）。

### 2. 场景图驱动的协作调度与效率验证

NavCraft的核心技术杠杆在于将**语义增强的场景图**作为协作规划的统一蓝图，并构建了与之配套的效率工具库：

- **场景图生成**：通过Instance Proximal Voting（IPV）为场景图节点赋予区域语义标签，再经Neighborhood Consensus与Contiguity Restoration两步后处理修正孤立误标与碎片化区域，形成拓扑连通且语义一致的规划空间。
- **效率工具库**：在场景图内提供路径距离计算、可达性检查与负载比较功能。协作方案的生成与验证均在此闭环中完成，确保协作调度具有空间可达性保障，而非LLM的“黑箱猜测”。

这一设计将LLM的生成能力约束在符号化验证框架内，实现了“生成-验证-采纳”的闭环控制，是NavCraft区别于直接依赖LLM端到端生成协作计划的关键创新。

### 3. 两阶段层级式任务生成架构

NavCraft采用**NavCraft-S → NavCraft-C**的两阶段层级设计，将单智能体基任务生成与协作调度解耦：

- **NavCraft-S**：先生成单智能体长程基任务，通过用户画像采样目标物体，并利用`leg_ok`条件验证路径可行性（路径段连通且跨步至少为 $\max\{2, \tau\}$）。
- **NavCraft-C**：在基任务基础上，通过思维链推理选择协作类型与交接区域，迭代验证效率增益，仅在通过负载比较后才实例化辅助机器人并分配子目标。

消融实验表明，这一解耦设计显著提升了协作计划的质量——直接生成双智能体任务的替代方案（V1/V2）因缺乏迭代效率检查，常产出无效协作。此外，注入用户画像将指令多样性提升16.14%，目标物体多样性提升17.35%，增强了基准的覆盖度与泛化评估能力。

### 4. 协作效率的量化证据

CoNavBench的协作设计带来了可观的效率增益。基准统计显示，跨类别的平均协作效率增益约为20%（Figure 2）。在下游导航策略评估中，微调后的Qwen2.5-VL-3B在步骤级协议下，协作策略成功率从单智能体的29.65%提升至35.02%，相对提升18.11%（Table 2, Table 3），同时SPL从13.81升至16.88，NE从6.74降至5.79，三项指标一致验证了协作机制的有效性。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_bMrH2PFMsi/figures/005_Figure_3.jpg]]
*Figure 3: NavCraft pipeline for CoNavBench benchmark data generation and scheduling*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_bMrH2PFMsi/figures/002_Table_1.jpg]]
*Table 1: Comparison to VLN benchmarks. ∗ The scale of our released benchmark is 4048, however NavCraft is able to generate unlimited data to be tested*

CoNavBench的生成与评估体系围绕**NavCraft**平台构建，其核心思路是将协作长程导航任务的形式化构建与严格效率验证统一于一个基于场景图的自动化流水线中。该流水线由四个关键模块串联而成，形成从环境表征到任务合成再到策略评估的闭环。

**模块一：语义增强场景图生成**

流水线的起点是从Habitat-Sim仿真环境中提取结构化的空间知识。NavCraft首先构建一个**语义增强的场景图**（semantically augmented scene graph），作为后续任务规划与验证的蓝图。该过程并非简单的拓扑提取，而是通过三步精细化处理将几何空间转化为语义区域图：

1. **实例邻近投票**（Instance Proximal Voting, IPV）：对场景图中的每个节点，通过k近邻目标实例的类别进行多数投票，赋予初始区域标签。公式为：
   $$\mathcal{N}_k(i) = \arg\operatorname{topk}_{m \in \mathcal{M}} \|\mathbf{p}_i - \mathbf{x}_m\|_2, \quad \hat{r}_i^{(0)} = \arg\max_c \sum_{m \in \mathcal{N}_k(i)} \mathbf{1}[r(m) = c]$$

2. **邻域共识校正**（Neighborhood Consensus）：针对狭窄通道附近因IPV产生的孤立误标，通过将节点标签替换为其最近邻的标签进行修正。

3. **连续性恢复**（Contiguity Restoration）：将小规模连通分量重新分配给边界节点最近的相邻类别，确保区域的空间连续性。

最终生成的场景图不仅编码了空间的拓扑连通性，还携带了区域级别的语义信息，为后续路径验证提供了基础。

**模块二：NavCraft-S（单智能体基任务生成）**

在场景图之上，NavCraft-S负责合成单智能体长程导航的基任务。其工作流程为：通过用户画像采样目标物体，在场景图中选择满足可达性约束的起始区域(s)、目标区域(t)和终点区域(e)，并验证路径的合法性。路径段的有效性由`leg_ok`条件定义：
$$\mathrm{leg\_ok}(u,v) := \mathrm{conn}(u,v) \wedge L(u,v) \geq \max\{2, \tau\}$$
即路径段必须连通且跳数距离至少为2或阈值τ。一条完整路径`Path(s → e)`由两段最短路径拼接而成，仅当两段均满足`leg_ok`时才被接受。这一模块输出的单智能体任务构成了协作任务的基准，其行进距离$C_{\mathrm{solo}} = d(s, o) + d(o, a_e)$将作为后续协作效率比较的参照。

**模块三：NavCraft-C（协作任务生成与调度）**

NavCraft-C是流水线的核心创新，负责将单智能体基任务提升为双智能体协作调度。其决策逻辑遵循**负载严格缩短原则**：仅在引入辅助机器人能严格缩短主智能体自身路径负载时才采纳协作方案。具体而言，模块评估两种规范的交接模式：

- **Type A1**（辅助机器人取物并交接，主智能体送达）：主智能体负载为$J_{r_1}^{\mathrm{A1}} = d(s, a_x) + d(a_x, a_e)$
- **Type A2**（主智能体取物并交接，辅助机器人送达）：主智能体负载为$J_{r_1}^{\mathrm{A2}} = d(s, t) + d(t, a_x)$

协作被采纳的充要条件是：
$$\min\{J_{r_1}^{\mathrm{A1}}, J_{r_1}^{\mathrm{A2}}\} < C_{\mathrm{solo}}$$

NavCraft-C通过迭代搜索交接区域$x$，并借助**效率工具库**（Efficiency Tool Library）在场景图内进行路径距离计算、可达性检查和效率比较，确保生成的协作计划在理论上具有可验证的效率增益。消融实验表明，直接生成双智能体任务（绕过NavCraft-S的单智能体基任务）会导致一个机器人几乎闲置，单机器人顺序执行反而更高效——这验证了两阶段设计（先单后协）的必要性。

**模块四：评估与策略执行**

生成的协作任务以逐步子任务（step-by-step subtasks）的形式提供给视觉语言模型策略。评估同时覆盖单智能体与协作智能体两种设定，采用SR、SPL、NE等标准导航指标，并扩展了独立完成率（ICR）和条件成功率（CSR）以衡量子任务级别的协作质量。实验在Habitat 3.0仿真器中进行，智能体配备前、左(+60°)、右(-60°)三方向同步RGB-D传感器，视觉特征由冻结的EVA-CLIP-02-LARGE ViT骨干网络提取。

**流水线整体特征**

NavCraft流水线的设计哲学可概括为“**场景图约束下的效率驱动生成**”：场景图提供空间可达性与距离的确定性验证基础，两阶段层级代理确保协作方案的质量下限，而严格的负载比较准则避免了为协作而协作的无效并行化。这一闭环使得CoNavBench能够以可控的成本（GPT-4o-mini仅$0.360即可达到26.56%的协作任务生成成功率，见Table 4）持续产出规模可扩展的协作导航数据。

CoNavBench 的数据生成与协作调度由 **NavCraft** 平台完成，其核心由四个模块构成：场景图生成、单智能体基任务生成（NavCraft-S）、协作任务生成（NavCraft-C），以及贯穿全流程的效率工具库。

### 场景图生成

NavCraft 首先从 Habitat-Sim 构建语义增强的场景图，作为后续规划的结构化蓝图。该过程包含三个关键步骤：

**实例近邻投票 (Instance Proximal Voting, IPV)** 为图中每个节点分配初始区域标签。给定节点 $i$ 的位置 $\mathbf{p}_i$ 和场景中目标实例 $m$ 的质心 $\mathbf{x}_m$，选取节点 $i$ 的 $k$ 个最近邻目标实例，通过多数投票确定其区域标签：

$$
\mathcal{N}_k(i) = \underset{m \in \mathcal{M}}{\arg \operatorname{topk}} \: \| \mathbf{p}_i - \mathbf{x}_m \|_2, \qquad \hat{r}_i^{(0)} = \arg \max_c \sum_{m \in \mathcal{N}_k(i)} \mathbf{1}[r(m) = c]
$$

其中 $\mathcal{M}$ 为目标实例集合，$r(m)$ 为目标 $m$ 的真实类别，$\hat{r}_i^{(0)}$ 为节点 $i$ 的初始区域标签。

**邻域一致性修正 (Neighborhood Consensus)** 针对窄通道附近可能出现的孤立误标进行纠正。若节点 $i$ 的标签与其所有邻域节点均不一致，则将其标签替换为最近邻节点的标签：

$$
j^{\star} = \arg \min_{j \in \mathcal{C}(i)} \| \mathbf{p}_i - \mathbf{p}_j \|_2, \qquad \hat{r}_i^{(1)} = \{\hat{r}_{j^{\star}}^{(0)} \text{ if isolated and disagreeing, else } \hat{r}_i^{(0)}\}
$$

**连通性恢复 (Contiguity Restoration)** 处理因拓扑断裂产生的碎片化小连通分量。对于连通分量 $\mathcal{C}$，计算其质心 $\mu_{\mathcal{C}}$，并将其整体重分配给边界节点距离最近的相邻类别 $c^{\star}$：

$$
\mu_{\mathcal{C}} = \frac{1}{|\mathcal{C}|} \sum_{i \in \mathcal{C}} \mathbf{p}_i, \qquad c^{\star} = \arg \min_{c'} \frac{1}{|B_{c'}|} \sum_{i \in \mathcal{C}, j \in B_{c'}} \| \mathbf{p}_i - \mathbf{p}_j \|_2
$$

其中 $B_{c'}$ 为类别 $c'$ 的边界节点集合。

### 单智能体基任务生成 (NavCraft-S)

NavCraft-S 负责生成单智能体长程基任务。其核心约束是路径段有效性条件 `leg_ok`：对于节点 $u$ 到 $v$ 的路径段，要求两节点连通且跳数距离 $L(u,v)$ 至少为 $\max\{2, \tau\}$（$\tau$ 为预设阈值）：

$$
\mathrm{leg\_ok}(u,v) := \mathrm{conn}(u,v) \wedge L(u,v) \geq \max\{2, \tau\}
$$

一条从起点区域 $s$ 经目标区域 $t$ 到终点区域 $e$ 的完整路径被判定为有效，当且仅当两段路径均满足 `leg_ok` 条件：

$$
\mathrm{valid} := \mathrm{leg\_ok}(s,t) \wedge \mathrm{leg\_ok}(t,e)
$$

有效路径由两段跳数最短路径拼接而成：

$$
\mathrm{Path}(s \rightarrow e) = \mathrm{SP}_H(s,t) \oplus \mathrm{SP}_H(t,e)
$$

### 协作任务生成与效率验证 (NavCraft-C)

NavCraft-C 将单智能体基任务提升为双智能体协作调度。其决策核心是**严格的效率采纳条件**：仅当引入助手机器人能严格缩短主智能体的行进负载时，才接受协作方案。

**单智能体负载** $C_{\mathrm{solo}}$ 定义为主智能体从起点 $s$ 到目标 $t$ 取物，再送达终点 $a_e$ 的总距离：

$$
C_{\mathrm{solo}} = d(s, t) + d(t, a_e)
$$

两种协作模式下主智能体的负载分别为：

- **Type A1**（助手取物并交接，主智能体送达）：主智能体从起点 $s$ 前往交接区域 $a_x$ 接取物品，再送达终点 $a_e$：
  $$
  J_{r_1}^{\mathrm{A1}} = d(s, a_x) + d(a_x, a_e)
  $$

- **Type A2**（主智能体取物并交接，助手送达）：主智能体从起点 $s$ 前往目标 $t$ 取物，再前往交接区域 $a_x$ 移交：
  $$
  J_{r_1}^{\mathrm{A2}} = d(s, t) + d(t, a_x)
  $$

**协作采纳条件**要求至少一种协作模式的主智能体负载严格小于单智能体负载：

$$
\min\{J_{r_1}^{\mathrm{A1}}, J_{r_1}^{\mathrm{A2}}\} < C_{\mathrm{solo}}
$$

该条件通过场景图上的效率工具库进行可达性验证和距离计算，确保协作方案在拓扑层面具有实际收益。消融实验表明，若跳过此迭代效率检查而直接生成双智能体任务，常导致一个机器人几乎闲置，单机器人顺序执行反而更高效（见附录 A.13.1 的失败案例分析）。

## 实验与关键发现

### 基准统计与协作效率

CoNavBench 包含 4048 个 episode，其中协作任务 1612 个，覆盖 10 类家居目标物体（Figure 2b）。类别分布以便携家具（28%）、个人休闲（17%）、装饰艺术品（12%）为主，协作类型分为 Type-A1（助手交接、主智能体送达）和 Type-A2（主智能体交接、助手送达）两种模式。Figure 2a 的小提琴图展示了各类别的协作效率增益分布：以单智能体顺序执行为基线，跨类别平均效率增益约为 **20%**。这一增益源于 NavCraft 的严格采纳准则——仅当协作方案严格缩短主智能体自身路径负载时才被接受（$\min\{J_{r_1}^{\mathrm{A1}}, J_{r_1}^{\mathrm{A2}}\} < C_{\mathrm{solo}}$）。

### 单智能体任务性能

Table 2 报告了单智能体任务在高层级指令（high-level）与逐步子任务（step-by-step）两种协议下的性能。零样本 Qwen2.5-VL 模型的高层级 SR 均低于 5%，表明长程视觉语言指令的零样本理解极为困难。微调带来显著提升：Qwen2.5-VL-3B 逐步 SR 从 10.41% 升至 **29.65%**，SPL 从 4.85 升至 13.81，NE 从 8.13 降至 6.74。7B 模型微调后高层级 SR 达 12.90%，逐步 SR 达 29.78%，但相比 3B 模型的边际增益有限，暗示当前瓶颈更多在于任务表征与指令复杂性，而非模型容量。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_bMrH2PFMsi/figures/018_Table_2.jpg]]
*Table 2: Performance comparison on the Single-Agent Task in CoNavBench. Results are shown for both high-level tasks and step-by-step subtasks*

### 协作智能体任务性能与核心对比

Table 3 报告了协作智能体任务的结果，这是论文的核心实验发现。在逐步子任务协议下，微调 Qwen2.5-VL-3B 的协作策略 SR 达到 **35.02%**，相比单智能体的 29.65% 提升 **+5.37 个百分点**（相对提升 **18.11%**）。SPL 从 13.81 提升至 16.88，NE 从 6.74 降至 5.79。这一增益验证了核心洞察：通过接力机制将长程任务并行化，确实能在不牺牲成功率的前提下缩短整体耗时。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_bMrH2PFMsi/figures/019_Table_3.jpg]]
*Table 3: Performance comparison on the Collaborative-Agent Task in CoNavBench. Results are shown for both high-level tasks and step-by-step subtasks*

然而，高层级指令下的协作增益并不明显。微调 3B 模型的高层级 SR 仅从 12.90%（单智能体）微升至 13.10%（协作），7B 模型的高层级 SR 甚至从 12.90% 降至 11.65%。这表明高层级指令下的视觉语言不匹配问题在协作场景中被放大——智能体不仅需要理解自身子任务，还需协调交接时机与区域，而当前 VLM 的长程推理能力尚不足以支撑这一复杂度。

### 生成代理消融

Table 4 对比了不同 LLM 作为 NavCraft 生成代理的性能、效率与成本。OpenAI GPT-4o 取得最高的任务生成成功率（单智能体 77%，协作 46.75%），但成本也最高（$5.242）。GPT-4o-mini 以 $0.360 的成本达到 26.56% 的协作成功率，在成本效率上具有优势。Claude 3.5 Sonnet 的协作成功率仅为 3.75%，且协作增益为负（-3.35%），说明其生成的协作方案反而劣于单智能体顺序执行。这一消融揭示了 NavCraft 两阶段设计的关键性：直接生成双智能体任务（如 A.13.1 的失败案例，Figure 17）往往导致一个机器人几乎闲置，单机器人顺序执行反而更高效。NavCraft 通过迭代效率检查（Efficiency Tool Library 在场景图内进行可达性验证和负载比较）显著提升了协作计划的质量。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_bMrH2PFMsi/figures/020_Table_4.jpg]]
*Table 4: Performance, efficiency, cost and latency of NAVCRAFT-powered agents. Higher numbers are better (↑) except Cost (↓). Note that the success rate represents task generation*

### 用户画像消融与多样性

注入用户画像（user profile）将指令多样性提升 **16.14%**（从 316 增至 367 条），目标物体多样性提升 **17.35%**（从 98 增至 115 类），如 Figure 14 所示。这验证了用户画像采样机制在增强基准覆盖度与生态效度方面的有效性。

### 失败模式分析

综合实验结果，主要失败模式可归纳为三类：

1. **高层级指令的视觉语言不匹配**：零样本模型高层级 SR 低于 5%，微调后虽有提升但仍远低于逐步协议。协作场景下该问题加剧，因为智能体需同时理解交接语义与空间约束。

2. **协作规划与执行的鸿沟**：NavCraft 生成的最优调度依赖于场景图拓扑信息，但实际执行中缺乏在线重规划能力。当交接区域因动态障碍或定位误差不可达时，协作收益可能完全丧失。

3. **模型容量边际效应**：3B 与 7B 微调模型在逐步协议下的性能差距有限（单智能体 29.65% vs 29.78%；协作 35.02% vs 29.78%），暗示当前瓶颈更多在于任务表征与训练范式，而非模型参数规模。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_bMrH2PFMsi/figures/004_Figure_2.jpg]]
*Figure 2: CoNavBench benchmark. (a) Collaborative efficiency by category. Violin plots show the distribution of category-wise efficiency gain over a single-robot baseline, yielding an average gain of 20% across categories. (b) Category and collaboration-type distribution. The benchmark covers a broad and balanced set of household target-object categories (outer ring) and two collaboration types (inner ring), evidencing rich object diversity that supports generalizable evaluation*

## 定位与知识库关联

### 1. 任务定义与基准定位

CoNavBench 在视觉语言导航（VLN）领域引入了一个此前未被系统建模的维度：**多机器人协作长程导航**。现有 VLN 基准——包括 R2R、REVERIE、SOON、CVDN 以及长程基准 LH-VLN——均以单智能体顺序执行为前提，评估指标仅反映个体完成效率与指令遵循能力。CoNavBench 将问题重新定义为：给定一条覆盖多个子目标的长程指令，由主智能体与助手智能体通过明确的交接点与分工协议并行执行，以缩短整体完工时间（makespan）。表 1 的基准对比显示，CoNavBench 是当前唯一提供协作多智能体 VLN 任务的基准，包含 1612 个协作 episodes 和平均 21.08% 的协作效率增益。

### 2. 方法谱系：从单智能体 VLN 到协作调度

**上游依赖**。CoNavBench 的数据生成平台 NavCraft 建立在两个基础上：Habitat-Sim 提供的仿真环境与场景资产，以及大语言模型（LLM）作为任务合成代理。在单智能体任务生成阶段（NavCraft-S），系统借鉴了 LH-VLN（Song et al., 2025）的长程指令分解思路，但将其从单智能体子任务链扩展为可并行化的多阶段结构。在协作调度阶段（NavCraft-C），核心决策逻辑——仅当助手介入严格缩短主智能体自身路径时才接受协作——可视为一种**负载感知的贪婪接力策略**，其形式化约束为：

$$\min\{J_{r_1}^{\mathrm{A1}}, J_{r_1}^{\mathrm{A2}}\} < C_{\mathrm{solo}}$$

这一约束在概念上与多机器人任务分配中的最小化最大完工时间（min-max makespan）目标一致，但 NavCraft 将其简化为二元决策（接受/拒绝协作）而非全局优化，从而避免了组合搜索的复杂性。

**下游策略**。CoNavBench 本身不提出新的导航策略，而是作为评估平台。实验中的策略均为基于 Qwen2.5-VL（Bai et al., 2025）的视觉语言模型，在零样本与微调两种设置下测试。因此，CoNavBench 的方法贡献集中在**任务生成与调度**层面，而非执行层面。

### 3. 与相关工作的关键差异

**vs. 多智能体 VLN 初步探索**。此前有个别工作尝试在 VLN 中引入多智能体（如辅助机器人提供视觉证据），但均未系统定义协作类型、交接协议或效率验证机制。CoNavBench 通过协作类型分类法（Type A1：助手取物→交接→主智能体送达；Type A2：主智能体取物→交接→助手送达）和基于场景图的效率工具库，首次将协作收益可量化、可验证。

**vs. 通用多机器人任务分配**。传统多机器人任务分配方法（如市场拍卖、匈牙利算法）通常假设已知的任务代价矩阵。NavCraft 的不同之处在于：它利用场景图上的路径距离计算（$d(\cdot,\cdot)$）作为代价估计，并通过迭代验证确保协作方案在拓扑可达性和负载缩短两个条件下均成立。这种**符号化场景图 + LLM 调度**的混合架构是 CoNavBench 的独特设计选择。

**vs. 端到端多智能体策略学习**。CoNavBench 将协作结构（谁在何时交接）作为任务定义的一部分预先给定，而非让策略在执行中自主涌现协作行为。这意味着当前基准评估的是“给定协作计划后的执行能力”，而非“协作计划的自主生成能力”。这一设计降低了策略学习难度，但也构成了适用边界。

### 4. 适用边界与局限

**规划-执行鸿沟**。NavCraft 生成的协作计划基于场景图的拓扑最短路径，未考虑实际导航中的局部避障、机器人间物理干扰或感知失败。实验中的轨迹可视化（Figure 5c）已展示了协作过程中的干扰现象，但当前基准不评估干扰对成功率的影响，也不提供在线重规划机制。这意味着 CoNavBench 衡量的是“理想调度下的执行潜力”，而非真实动态环境中的鲁棒协作能力。

**场景图抽象层级**。场景图仅编码区域连通性和语义标签，缺乏物体尺寸、可用表面、门宽等几何细节。交接区域的选择仅基于拓扑距离最小化，可能在几何上不可行（如狭窄走廊无法容纳两机器人并行交接）。这一局限在附录 A.13.1 的消融实验中得到间接印证：直接生成双智能体任务（无迭代效率检查）导致一个机器人几乎闲置，说明拓扑层面的“最优”调度可能在实际执行中失效。

**协作规模与模式**。当前基准仅支持双智能体接力模式，未扩展到三个及以上机器人，也不涵盖更复杂的协作模式（如并行探索、协同搬运）。协作类型分类法仅区分两种交接方向，未建模交接失败、通信延迟或状态同步开销。

**绝对性能瓶颈**。即使经过微调，最佳模型的步骤级成功率仅为 35.02%（协作）和 29.65%（单智能体），高层级指令下的成功率更是低于 13%。这表明视觉语言模型在长程指令理解、跨子任务状态追踪和协作时序推理方面仍存在根本性困难。

### 5. 开放问题

1. **不确定性感知的在线调度**：如何将 NavCraft 的离线协作计划与执行时的感知不确定性结合，实现动态重规划与交接时机自适应调整？
2. **协作规模扩展**：如何将双智能体接力模式推广到 $N$ 个机器人，并处理随之而来的资源竞争、死锁避免和通信拓扑设计？
3. **几何感知的场景图增强**：如何在符号化场景图中集成物体尺寸、可通过宽度等几何约束，使交接区域选择在物理层面可行？
4. **协作涌现与计划给定的权衡**：当前基准将协作结构作为先验输入，未来是否应设计更开放的任务格式，让策略自主决定何时协作、与谁协作？
5. **视觉语言模型的长程推理瓶颈**：高层级指令下成功率极低（零样本不足 5%，微调后约 12%），如何通过记忆增强、结构化状态表示或课程学习提升模型的长程协调能力？

## 原文 PDF

![[paperPDFs/ICLR_2026/CoNavBench_Collaborative_Long_Horizon_Vision_Language_Navigation_Benchmark.pdf]]
