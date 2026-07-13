---
title: "Global Prior Meets Local Consistency: Dual-Memory Augmented Vision-Language-Action Model for Efficient Robotic Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Global_Prior_Meets_Local_Consistency_Dual_Memory_Augmented_Vision_Language_Action_Model_for_Efficient_Robotic_Manipulation.pdf
project_link: "https://cybertronagent.github.io/OptimusVLA.github.io/"
code_link: null
aliases:
- Global_Prior_Mee
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 用检索到的任务级先验（GPM）替换标准高斯噪声，并注入从近期动作历史学习的一致性约束（LCM），缩小先验-目标分布差距并强制时间连贯性。
primary_logic: 将语义相似轨迹中检索的任务级先验作为流匹配的初始化起点，并利用轻量级时间一致性约束，可在不修改预训练VLA骨干的情况下大幅减少函数评估次数（NFE）并实现平滑、具有进度感知的动作生成。
claims:
- GPM 将 LIBERO-Long 上的 NFE 从 10.0（π0.5）降至 3.2，大幅提高效率。
- 移除 GPM 导致真实世界泛化任务成功率从 85.0% 降至 77.0%（下降 9.4%），验证了任务级先验的关键作用。
- 移除 LCM 导致 LIBERO-Long 成功率下降 1.7%，揭示了时间一致性约束在长期任务中的作用。
- OptimusVLA 在 LIBERO 上平均成功率 98.6%，超越所有基线（包括 π0.5 的 96.9%）。
---

# Global Prior Meets Local Consistency: Dual-Memory Augmented Vision-Language-Action Model for Efficient Robotic Manipulation

> [!tip] 核心洞察
> 将语义相似轨迹中检索的任务级先验作为流匹配的初始化起点，并利用轻量级时间一致性约束，可在不修改预训练VLA骨干的情况下大幅减少函数评估次数（NFE）并实现平滑、具有进度感知的动作生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 全局先验与局部一致性：双记忆增强的视觉-语言-动作模型实现高效机器人操作 |
| 英文题名 | Global Prior Meets Local Consistency: Dual-Memory Augmented Vision-Language-Action Model for Efficient Robotic Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20200) · [Project](https://cybertronagent.github.io/OptimusVLA.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | OptimusVLA |
| Dataset | LIBERO, CALVIN, RoboTwin 2.0 Hard, Real-World |

> [!tip] 效果简介
> - LIBERO 上，Average Success Rate (%) 98.6 vs 96.9 (π0.5) (+1.7%)。
> - CALVIN (ABC→D) 上，Avg. Completion Length 4.45 vs 3.92 (π0) (+13.5%)。
> - RoboTwin 2.0 Hard 上，Average Success Rate (%) 38 vs 29 (π0.5) (+9%)。

## 概要

机器人操作中的视觉-语言-动作（VLA）模型面临两个核心瓶颈：**推理效率低**——各向同性高斯噪声先验与结构化动作分布差距过大，需要大量去噪步数且易产生不可行样本；**鲁棒性差**——现有策略仅依赖当前观测，忽略历史序列，缺乏任务进度感知和时间一致性。本文提出 **OptimusVLA**，通过 **全局先验记忆（Global Prior Memory, GPM）** 和 **局部一致性记忆（Local Consistency Memory, LCM）** 双记忆增强机制，在不修改预训练 VLA 骨干的前提下解决上述问题。

**核心思路**：GPM 从记忆库中检索语义相似轨迹，构建任务级高斯先验以替代标准高斯噪声，缩小先验-目标分布差距，大幅减少流匹配所需的函数评估次数（NFE）；LCM 从近期动作历史中动态建模时间依赖关系，注入一致性偏置以强制动作序列的平滑性与进度感知。

**主要结果**：在 LIBERO 基准上，OptimusVLA 取得 **98.6%** 的平均成功率，超越强基线 π0.5（96.9%）；在 CALVIN 上平均完成长度达 **4.45**，较 π0 提升 13.5%；在 RoboTwin 2.0 Hard 设定下平均成功率 **38%**，领先 π0.5 达 9 个百分点；真实世界泛化任务成功率 **85.0%**。同时，GPM 将长序列任务的 NFE 从 10.0 降至 3.2，推理效率提升显著。消融实验表明，移除 GPM 导致真实世界泛化任务成功率骤降 9.4%，验证了任务级先验在泛化中的关键作用。

### 机器人操作的层级式VLA范式

视觉-语言-动作（Vision-Language-Action, VLA）模型已成为机器人操作策略学习的主流范式。其中，层级式VLA架构——如 **π0** 和 **π0.5**——通过将高层语义理解与低层动作生成解耦，在复杂操作任务上展现出强大能力。这类模型通常采用条件流匹配（Conditional Flow Matching）作为动作生成的核心机制：从先验分布采样初始点，沿最优传输路径逐步去噪，生成目标动作块。

### 两个关键瓶颈

尽管层级式VLA取得了显著进展，现有方法在推理效率和鲁棒性上仍存在两个根本性瓶颈：

**瓶颈一：先验-目标分布差距导致推理效率低下。** 标准流匹配策略从各向同性高斯噪声 $\mathcal{N}(0,I)$ 出发进行去噪。然而，结构化动作分布与无信息噪声之间存在巨大差距，迫使模型进行大量函数评估（Number of Function Evaluations, NFE）才能生成可行动作，且容易产生不可行样本。如 Figure 1 所示，这种“冷启动”方式严重拖慢了推理速度。

**瓶颈二：忽略历史序列导致时间一致性和进度感知缺失。** 现有策略普遍基于马尔可夫假设，仅依赖当前观测生成动作，完全忽略近期动作历史。这带来两个问题：(i) 策略缺乏任务进度感知，无法判断当前处于任务的哪个阶段；(ii) 相邻动作块之间缺乏时间连贯性约束，在面对视觉歧义（相似观测对应不同动作阶段）时容易产生抖动或不一致控制。

### 核心动机与研究问题

针对上述瓶颈，本文提出一个核心问题：**能否在不修改预训练VLA骨干的前提下，通过增强先验质量和注入时间一致性约束，同时提升推理效率和动作鲁棒性？**

这一问题的解决思路源于两个关键洞察：

- **全局先验引导**：语义相似的轨迹共享相近的动作分布。若能检索并复用任务级先验作为流匹配的初始化起点，而非从零开始的高斯噪声，则可大幅缩小先验-目标分布差距，减少所需NFE。
- **局部一致性约束**：近期动作序列蕴含丰富的任务进度信息。通过轻量级工作记忆动态编码历史动作并预测一致性偏置，可显式强制时间连贯性，使策略具备进度感知能力。

基于上述动机，本文提出 **OptimusVLA**，通过双记忆增强机制——全局先验记忆（Global Prior Memory, GPM）和局部一致性记忆（Local Consistency Memory, LCM）——在不改变预训练VLA骨干的条件下，系统性地解决推理效率与时间鲁棒性两大瓶颈。

## 核心方法与创新机理

OptimusVLA 的核心创新在于通过**双记忆架构**（GPM + LCM）对层级式 VLA 模型的两个关键环节进行“外科手术式”改造，而非重新设计整个策略网络。具体而言，该方法识别出两个因果调节旋钮（causal knobs），并进行了精准替换：

### 创新点一：全局先验记忆（GPM）—— 替换动作先验分布

**问题瓶颈**：现有层级式 VLA 模型（如 π0、π0.5）采用条件流匹配生成动作块时，以各向同性高斯噪声 $\mathcal{N}(0, I)$ 作为生成起点。该先验与结构化动作目标分布之间存在巨大差距，导致推理时需多次去噪（NFE 高），且易产生不可行样本。

**创新方案**：GPM 将生成起点从无信息噪声**重新定位**到任务级先验附近。具体机制为：
- 构建长程记忆库（Memory Bank），存储离线演示轨迹的动作块及其多模态嵌入；
- 推理时，通过检索令牌 $z_{re}$ 从记忆库中检索语义相似的轨迹，组合成任务级高斯先验 $\mathcal{P}_{re}$；
- 从该先验中采样初始动作 $\hat{\mathbf{X}}_t = \mu + \lambda (\epsilon \odot \sqrt{\mathrm{Var}})$，其中噪声尺度 $\lambda$ 和 NFE 根据检索相似度**自适应调整**：相似度越高，先验置信度越高，$\lambda$ 越小，所需 NFE 越少。

**效果**：GPM 将 LIBERO-Long 上的 NFE 从 10.0（π0.5）降至 3.2，并在真实世界泛化任务上贡献了 8.0% 的绝对成功率提升（移除 GPM 后从 85.0% 降至 77.0%）。

### 创新点二：局部一致性记忆（LCM）—— 注入时间一致性约束

**问题瓶颈**：标准 VLA 策略仅依赖当前观测 $O_t$ 和语言指令 $\ell$，遵循马尔可夫假设，完全忽略历史动作序列。这导致策略缺乏任务进度感知能力，在面对视觉相似但语义不同的连续状态时容易产生不连贯动作。

**创新方案**：LCM 作为轻量级工作记忆模块，从近期动作历史中提取时间一致性信号：
- **Consistency Layer**：捕获单个动作块内部的时序依赖；
- **Dynamic Awareness Module**：跨块建模动作序列的进展趋势，预测一致性偏置 $\mathbf{B}_t$；
- 将该偏置注入策略输入 $\mathbf{X}_t = \hat{\mathbf{X}}_t + \mathbf{B}_t$，强制生成的动作块与历史保持时间连贯。

**效果**：LCM 在 LIBERO-Long 上贡献 1.7% 的成功率提升，并在真实世界长序列任务中使策略能够区分视觉相似但语义不同的状态（如“抓取前”与“放置后”），而 π0.5 在此类场景下容易出现混淆。

### 创新点三：非侵入式模块化设计

两个创新模块均以**即插即用**方式附加在预训练 VLA 骨干之上，无需修改原有视觉-语言编码器或流策略网络权重。OptimusVLA 直接从 π0.5 权重初始化，仅新增 GPM 和 LCM 参数（总参数量 3.6B），即可在**显著减少训练步数**的情况下超越 π0.5 的性能（Figure 4），验证了“改造先验与约束”而非“重新训练整体”这一技术路线的有效性。

OptimusVLA 的整体框架遵循“感知—记忆检索—一致性编码—流匹配生成”的四阶段流水线，在不修改预训练 VLA 骨干的前提下，将全局任务先验与局部时间一致性注入动作生成过程。如 Figure 2 所示，系统由四个核心模块构成：

![[assets/figures/papers/paper_list_l2236_https_arxiv_org_abs_2602_20200/figures/002_Figure_2.jpg]]
*Figure 2: Overview of OptimusVLA framework. Given a task and the current observation, the Vision–Language backbone first encodes the inputs into a multimodal representation. GPM then retrieves a task-level prior based on this representation, while LBM dynamically encodes the historical action sequence to produce a consistency constraint. Finally, the flow policy denoises the initialization with an adaptive NFEs schedule to generate the action chunk*

1. **Vision–Language Backbone（视觉–语言骨干）**：接收当前观测 $O_t$ 和语言指令 $\ell$，输出多模态嵌入 $E_{emb}$，作为后续记忆检索与策略输入的统一语义表示（Eq. 3）。
2. **Global Prior Memory（GPM，全局先验记忆）**：长程记忆模块，通过检索令牌 $z_{re}$ 从记忆库中检索语义相似的轨迹，构建任务级高斯先验分布 $\mathcal{P}_{re}$（Eq. 4），并依据检索相似度自适应调整噪声尺度 $\lambda$ 与函数评估次数（NFE），将流匹配的初始化点从各向同性高斯噪声 $\mathcal{N}(0,I)$ 迁移至目标流形邻域。
3. **Local Consistency Memory（LCM，局部一致性记忆）**：工作记忆模块，接收前一动作块 $\mathbf{A}_{t-1}$，通过 Consistency Layer 捕获块内依赖，再由 Dynamic Awareness Module 建模块间时序关系，输出一致性偏置 $\mathbf{B}_t$（Eq. 5），显式建模任务进度与时间连贯性。
4. **Flow Policy（流策略）**：以 GPM 采样的初始点 $\hat{\mathbf{X}}_t$ 与 LCM 偏置 $\mathbf{B}_t$ 之和 $\mathbf{X}_t = \hat{\mathbf{X}}_t + \mathbf{B}_t$ 作为输入（Eq. 6），沿最优传输路径 $x_t = (1-t)x_0 + t x_1$ 进行条件流匹配去噪，生成未来 $H$ 步动作块 $\mathbf{a}_{t+1:t+H}$。

**数据流与关键机制**：VLM 编码后的嵌入 $E_{emb}$ 同时驱动 GPM 的检索过程与 LCM 的时序建模，形成“全局语义锚定 + 局部动态约束”的双记忆协同架构。GPM 从根本上缩小了先验分布与目标动作分布之间的差距，使得流策略仅需少量去噪步骤即可生成可行样本；LCM 则以轻量级推理开销为策略注入进度感知能力，强制相邻动作块之间的平滑过渡。两者均以即插即用的方式附加于预训练流策略之上，训练时采用分阶段策略——先独立训练 GPM 和 LCM，再与流策略联合微调。

### 3.1 整体框架与多模态嵌入

OptimusVLA 由四个核心模块构成：Vision–Language Backbone、Flow Policy、Global Prior Memory (GPM) 和 Local Consistency Memory (LCM)（Figure 2）。给定当前观测 $O_t$ 和语言指令 $\ell$，视觉-语言骨干首先将其编码为多模态表示：

$$E_{emb} \gets \mathsf{VLM}(O_t, \ell) \tag{3}$$

该表示 $E_{emb}$ 作为后续 GPM 检索和流策略的条件输入。

### 3.2 全局先验记忆 (GPM)

**设计动机。** 标准层级式 VLA 模型以各向同性高斯噪声 $\mathcal{N}(0, I)$ 作为流匹配的初始点。该先验分布与结构化动作目标分布之间存在显著差距，导致需要大量函数评估次数（NFE）且易生成不可行样本。GPM 的核心思想是将语义相似轨迹中检索到的任务级先验作为生成起点，将先验分布拉近目标流形邻域，从根本上缩小先验-目标分布差距。

**模块构成。** GPM 是一个长程记忆模块，由三部分组成：
- **Prior Head**：将多模态表示投影为检索令牌 $z_{re}$；
- **Memory Bank**：存储离线训练阶段收集的轨迹动作块及其语义键值；
- **Prior-Aware Sampler**：根据检索相似度自适应调整噪声尺度 $\lambda$ 和 NFE 调度。

**先验检索与组合。** 检索令牌 $z_{re}$ 查询记忆库，获取任务级动作先验分布：

$$\mathcal{P}_{re} \gets \mathrm{GPM}(z_{re}) \tag{4}$$

GPM 从记忆库中检索 $k$ 条最相似轨迹，将其动作统计量（均值 $\mu$ 和方差 $\mathrm{Var}$）组合为高斯先验。采样过程为：

$$\hat{\mathbf{X}}_t = \mu + \lambda (\epsilon \odot \sqrt{\mathrm{Var}}), \quad \epsilon \sim \mathcal{N}(0,I) \tag{14}$$

其中 $\lambda$ 为自适应噪声尺度，随检索平均相似度 $\bar{s}$ 动态调节：相似度越高，$\lambda$ 越小，采样点越集中于先验均值附近；相似度越低，$\lambda$ 越大，保留更多探索空间。

**自适应 NFE 调度。** NFE 数量 $N$ 同样由 $\bar{s}$ 决定，缩放公式为：

$$\left( 1 - \frac{\bar{s} + 1}{2} \right) (N_{\mathrm{max}} - N_{\mathrm{min}})$$

当检索到高置信度先验时，NFE 显著降低（如从 10.0 降至 3.2），实现推理加速。

### 3.3 局部一致性记忆 (LCM)

**设计动机。** 现有策略仅依赖当前观测，忽略历史动作序列，缺乏任务进度感知和时间一致性。LCM 作为工作记忆模块，从近期动作历史动态建模时序依赖，注入一致性约束以强制动作平滑连贯。

**模块构成。** LCM 包含两个子模块：
- **Consistency Layer**：捕获动作块内部的帧间依赖关系；
- **Dynamic Awareness Module**：建模相邻动作块之间的时序转移，推断任务进度。

**一致性偏置生成。** LCM 接收前一动作块 $\mathbf{A}_{t-1}$，输出一致性偏置 $\mathbf{B}_t$：

$$\mathbf{B}_t \gets \mathrm{LCM}(\mathbf{A}_{t-1}) \tag{5}$$

该偏置编码了从历史动作序列中推断的进度信息和时序连贯性约束。

### 3.4 流策略输入组合与动作生成

GPM 采样的初始点 $\hat{\mathbf{X}}_t$ 与 LCM 生成的一致性偏置 $\mathbf{B}_t$ 相加，形成流策略的最终输入：

$$\mathbf{X}_t = \hat{\mathbf{X}}_t + \mathbf{B}_t \tag{6}$$

流策略基于条件流匹配从 $\mathbf{X}_t$ 出发，沿最优传输路径去噪生成动作块 $\mathbf{a}_{t+1:t+H}$。条件流匹配的训练目标为速度场 $v_\theta$ 匹配目标常数速度 $u_t = x_1 - x_0$：

$$\operatorname*{min}_{\theta} \mathbb{E}_{t\sim\mathcal{U}[0,1], x \sim p_t(x)} \| v_{\theta}(t, x) - u_t(x) \|_2^2 \tag{2}$$

其中 $x_t$ 沿线性插值路径演化：

$$x_t = (1 - t) x_0 + t x_1 \tag{1}$$

### 3.5 训练策略

GPM、LCM 和流策略目前采用分阶段训练：
- **第一阶段**：在离线轨迹数据上预训练 GPM 的 Prior Head 和 Memory Bank，构建任务级先验库；
- **第二阶段**：冻结 GPM，训练 LCM 的 Consistency Layer 和 Dynamic Awareness Module，LCM 损失为预测偏置与真实动作块差异的 L2 范数；
- **第三阶段**：冻结 GPM 和 LCM，微调流策略以适配新的先验-偏置组合输入。

OptimusVLA 从 **π0.5** 权重初始化，总参数量约 3.6B。

![[assets/figures/papers/paper_list_l2236_https_arxiv_org_abs_2602_20200/figures/001_Figure_1.jpg]]
*Figure 1: Top: Comparison between the standard VLA architecture (left) and our proposed OptimusVLA (right). (ii) Poor robustness to temporal dependence. Middle: Illustration of how GPM (blue) and LCM (green) address two key limitations of existing VLA models: (i) Low inference efficiency due to a large prior–target gap. (ii) Poor robustness to temporal dependence. Bottom: Efficiency and performance comparison*

## 实验与关键发现

### 核心结果：多基准上的性能优势

OptimusVLA 在三个仿真基准和真实世界任务上均取得领先结果，验证了双记忆机制的有效性。

**LIBERO 基准。** 在 LIBERO 四个任务套件上，OptimusVLA 平均成功率达 **98.6%**，超越强基线 π0.5 的 96.9%（+1.7%）。尤其在长序列任务 LIBERO-Long 上，OptimusVLA 取得 96.4%，而 π0.5 为 93.2%（Table 1）。该基准上的全面领先表明，GPM 的任务级先验与 LCM 的时间一致性约束在长程操作中发挥了关键作用。

**CALVIN 基准。** 在 CALVIN 上，OptimusVLA 的平均完成长度达 **4.45**，较 π0 的 3.92 提升 13.5%（Table 2）。从 1/5 到 5/5 各轨成功率均显著优于 π0 和 π0.5，验证了模型在语言条件长序列任务上的泛化能力。

**RoboTwin 2.0 双臂基准。** 在 Hard 设定下，OptimusVLA 平均成功率达 **38%**，远超 RDT（20%）和 DP（8%）（Table 3）。在 Stack Bowls Two 等需要精细双臂协调的任务上，OptimusVLA 取得 58%，领先 RDT 达 28 个百分点。LCM 提供的一致性约束在此类双臂协调任务中尤为关键。

**真实世界任务。** 在真实世界泛化任务套件上，OptimusVLA 成功率达 **85.0%**，长序列任务套件上达 **64.0%**，分别超越 π0 达 42.9% 和 52.4%（Figure 3）。GPM 检索的任务级先验使策略对视觉干扰具有鲁棒性，而 LCM 强制的时间连贯性则保证了平滑、协调的轨迹执行。

### 效率分析：训练与推理双重加速

**训练效率。** 从 π0.5 权重初始化后，OptimusVLA 仅需 π0.5 约 1/3 的训练步数即可达到相当甚至更优的性能（Figure 4）。这表明 GPM 和 LCM 模块引入的归纳偏置有效降低了策略学习的样本复杂度。

**推理效率。** GPM 将流匹配的初始点从各向同性高斯噪声移至目标流形邻域，大幅减少所需函数评估次数（NFE）。在 LIBERO-Long 上，OptimusVLA 的 NFE 仅 **3.2**，而 π0.5 需 **10.0**，推理时间显著缩短（Figure 5）。真实世界任务上同样观察到约 2.9× 的推理加速。

### 消融实验：GPM 与 LCM 的独立贡献

**GPM 的关键作用。** 移除 GPM 后，LIBERO-Long 成功率下降 3.2%，CALVIN 平均完成长度下降 3.8%，真实世界泛化任务成功率从 85.0% 骤降至 77.0%（下降 9.4%）（Table 4）。真实世界场景中性能退化尤为严重，说明任务级先验对视觉干扰和场景变化的泛化至关重要。

**LCM 的时间一致性价值。** 移除 LCM 导致 LIBERO-Long 下降 1.7%，CALVIN 平均长度亦有所下降（Table 4）。虽然降幅小于 GPM，但 LCM 在长序列任务中提供了不可忽视的时间连贯性约束。

**GPM 记忆库设计消融。** 记忆库存储轨迹数 Num=6500、检索数 k=8 时性能最优（LIBERO-Long 成功率 96.4%）（Table 5）。当 k=1 时，先验过于确定，限制了流匹配的探索空间，导致性能退化。这验证了多轨迹检索与组合策略的必要性。

### 定性分析：自适应机制与时间依赖性建模

Figure 6 展示了 OptimusVLA 在仿真与真实世界任务中的定性行为。在仿真任务关键帧上，GPM 的检索相似度 $\bar{s}$ 随任务进展动态变化，自适应噪声尺度 $\lambda$ 和 NFE 调度随之调整：当检索到的先验与当前状态高度相似时，模型采用更小的噪声和更少的 NFE，实现高效推理；当相似度降低时，则增加 NFE 以保证生成质量。

![[assets/figures/papers/paper_list_l2236_https_arxiv_org_abs_2602_20200/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative results of OptimusVLA on simulation task and Real-World task. Top: On simulation task, we visualize the retrieval similarity s¯, adaptive noise scales λ, and NFEs N of key frames. Bottom: On Real-World task, we demonstrate the role of LCM in modeling temporal dependencies, whereas π0.5 struggles to distinguish between similar observations*

在真实世界任务中，LCM 使 OptimusVLA 能够区分视觉观测相似但任务阶段不同的状态，而 π0.5 在此类情形下出现混淆。这验证了 LCM 通过建模近期动作序列来推断任务进度、提供时间一致性的设计意图。

### 局限性与失败模式

尽管取得了显著性能提升，OptimusVLA 仍存在以下局限：

1. **GPM 的静态性。** GPM 依赖离线训练数据构建静态记忆库，未实现在线更新。在完全新颖的场景下，检索到的先验置信度下降，可能导致性能退化。需人工验证具体退化幅度。

2. **LCM 的上下文窗口限制。** LCM 虽轻量，但其对极长序列的全局上下文建模能力有限，仅依赖近期动作块。在需要更长历史依赖的任务中，一致性约束可能不足。

3. **分阶段训练。** GPM、LCM 和流策略目前分阶段训练，未进行端到端联合优化，可能限制了各模块间的协同潜力。

4. **环境迁移性未充分验证。** 实验主要集中在桌面操作环境，向更开放、动态场景的迁移能力有待进一步评估。

![[assets/figures/papers/paper_list_l2236_https_arxiv_org_abs_2602_20200/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on LIBERO [26]. We report the average success rate on each task suite (500 rollouts)*

![[assets/figures/papers/paper_list_l2236_https_arxiv_org_abs_2602_20200/figures/004_Table_2.jpg]]
*Table 2: Performance comparison on CALVIN [34]. We report the success rate of each track and average completion length (Avg. Len). † represents the result we reproduced*

![[assets/figures/papers/paper_list_l2236_https_arxiv_org_abs_2602_20200/figures/006_Table_4.jpg]]
*Table 4: Ablation study of GPM and LCM on LIBERO-Long, CALVIN, and Real-World Generalization Tasks*

## 定位与知识库关联

### 与基线模型的关系

OptimusVLA 建立在层级式 VLA 模型 **π0.5** 之上——其视觉-语言骨干和流匹配策略直接继承自 π0.5 的权重，再额外注入 GPM 和 LCM 模块，总参数量达 3.6B。这一设计使其在方法谱系中处于“带记忆增强的层级式 VLA”位置：它既不同于单流 VLA（如 **OpenVLA**），也不同于纯扩散策略（如 **DP**、**RDT**），而是以最小侵入方式改造流匹配的初始分布和条件输入。

具体而言，OptimusVLA 相对于基线 π0.5 的关键改动集中在两个可插拔槽位：

- **动作先验分布**：π0.5 使用各向同性高斯噪声 $\mathcal{N}(0,I)$ 作为流匹配起点，而 OptimusVLA 通过 GPM 从记忆库检索任务级高斯先验，并附加自适应噪声尺度 $\lambda$ 与自适应 NFE 调度。这一改动直接缩小了先验-目标分布间的 Wasserstein 距离，从根本上减少了去噪步数。
- **时间一致性建模**：π0.5 仅依赖当前观测（马尔可夫假设），缺乏对历史动作序列的显式利用。OptimusVLA 引入 LCM，从近期动作块动态预测一致性偏置 $\mathbf{B}_t$，并将其注入策略输入 $\mathbf{X}_t = \hat{\mathbf{X}}_t + \mathbf{B}_t$，从而强制时间连贯性。

值得注意的是，OptimusVLA 并未修改流匹配的训练目标本身——其条件流匹配损失仍为：

$$\operatorname*{min}_{\theta} \mathbb{E}_{t\sim\mathcal{U}[0,1], x \sim p_t(x)} \| v_{\theta}(t, x) - u_t(x) \|_2^2$$

其中 $u_t = x_1 - x_0$ 为常数速度。GPM 和 LCM 的作用发生在采样阶段：GPM 重新定义了 $x_0$ 的分布，LCM 则调整了条件输入。这种“训练时不变、推理时增强”的策略使其与 π0.5 共享骨干权重，训练效率显著更高——从相同初始化出发，OptimusVLA 用更少的训练步数即达到强性能（见 Figure 4）。

### 适用边界

OptimusVLA 的设计假设决定了其适用范围：

1. **任务可检索性**：GPM 的有效性依赖于记忆库中存在与当前任务语义相似的轨迹。当面对完全新颖的任务场景时，检索到的先验置信度下降，自适应机制会增大噪声尺度 $\lambda$ 和 NFE，使模型退化为接近 π0.5 的行为。这意味着 OptimusVLA 的优势在“训练任务分布内或邻域”场景中最为显著。

2. **桌面操作环境**：实验验证集中在 LIBERO、CALVIN、RoboTwin 和真实世界桌面操作任务。向更开放、动态、非结构化的场景（如户外导航、人机交互密集环境）的迁移能力尚未得到验证。

3. **分阶段训练**：GPM、LCM 和流策略目前采用分阶段训练策略，而非端到端联合优化。这简化了训练流程，但可能限制了各模块间的协同潜力。

### 局限与开放问题

**已识别的局限**：

- **GPM 的静态性**：记忆库由离线训练数据构建，无法在线更新。在持续部署中，模型无法从新经验中学习或巩固已有知识，限制了其在非平稳环境中的适应能力。
- **LCM 的上下文范围**：LCM 虽轻量，但其时间依赖建模主要基于近期动作块。对于需要更长历史窗口（如跨越数十步的子任务依赖）的极长序列任务，其全局上下文建模能力有限。
- **检索扩展性**：当记忆库规模增大至数万条轨迹时，检索效率与先验质量之间的权衡尚未被系统研究。当前最优配置为 6500 条轨迹、检索数 $k=8$，但 $k=1$ 时已观察到先验过于确定导致的性能退化。

**开放问题**：

1. **在线记忆更新**：能否设计遗忘/巩固机制，使 GPM 支持持续学习，在部署中动态吸收成功轨迹、淘汰过时先验？
2. **端到端联合训练**：能否统一优化 GPM、LCM 与流策略，让检索和一致性约束与动作生成目标直接对齐？
3. **更大规模扩展**：在多任务、多具身的大规模数据下，检索效率与记忆库扩展性如何保障？是否需要引入层次化检索或压缩存储？
4. **LCM 的长序列扩展**：LCM 是否可扩展至更长历史窗口，或与注意力机制融合，以提升跨子任务的时间一致性建模？

## 原文 PDF

![[paperPDFs/CVPR_2026/Global_Prior_Meets_Local_Consistency_Dual_Memory_Augmented_Vision_Language_Action_Model_for_Efficient_Robotic_Manipulation.pdf]]
