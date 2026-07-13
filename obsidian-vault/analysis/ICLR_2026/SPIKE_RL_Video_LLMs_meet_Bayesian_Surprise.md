---
title: "SPIKE-RL: Video-LLMs meet Bayesian Surprise"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SPIKE_RL_Video_LLMs_meet_Bayesian_Surprise.pdf
project_link: null
code_link: https://github.com/sahithyaravi/SPIKE-RL
openreview_forum_id: QLiXtWEAkq
aliases:
- SSR
- SPIKE-RL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过显式跟踪模型对可解释文本假设的信念分布，并利用新帧触发的贝叶斯惊喜（KL散度）量化信念变化幅度，从而引导帧采样的关注区域。"
primary_logic: "将视频理解建模为动态信念更新过程：根据历史与近期上下文生成多个“接下来会发生什么”的文本假设，计算先验与后验分布之间的KL散度作为惊喜分数，该分数不仅与人类对惊喜的判断高度相关，还能有效指导非均匀的、面向惊喜区域的帧采样，持续提升多种下游视频任务的表现。"
claims:
- "SPIKE-RL在Oops!上的Acc@0.25s达到62.9%，接近人类表现（62.1%），远超零样本Qwen2.5-VL的6.6%。"
- "SPIKE-RL在FunQA上的IoU达到68.2，比零样本Qwen2.5-VL的11.6提升显著，且超越所有专用基线。"
- "在五个下游基准上，惊喜加权采样相比均匀采样持续带来性能提升，例如SPIKE-RL在ExFunTube上提升+7.0%。"
- "SPIKE和SPIKE-RL的惊喜得分与人类判断的Spearman相关系数分别达到0.84和0.87，表明二者高度一致。"
---

# SPIKE-RL: Video-LLMs meet Bayesian Surprise

> [!tip] 核心洞察
> 将视频理解建模为动态信念更新过程：根据历史与近期上下文生成多个“接下来会发生什么”的文本假设，计算先验与后验分布之间的KL散度作为惊喜分数，该分数不仅与人类对惊喜的判断高度相关，还能有效指导非均匀的、面向惊喜区域的帧采样，持续提升多种下游视频任务的表现。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SPIKE-RL: 视频大语言模型遇见贝叶斯惊喜 |
| 英文题名 | SPIKE-RL: Video-LLMs meet Bayesian Surprise |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=QLiXtWEAkq) · [GitHub](https://github.com/sahithyaravi/SPIKE-RL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SPIKE / SPIKE-RL |
| Dataset | Oops!, FunQA, Mr. Bean |

> [!tip] 效果简介
> - Oops! 上，Acc@0.25s 为 62.9 (SPIKE-RL)，对比 6.6 (Qwen2.5-VL zero-shot)，变化 +56.3。
> - Oops! 上，Acc@1s 为 69.1 (SPIKE-RL)，对比 9.6 (Qwen2.5-VL zero-shot)，变化 +59.5。
> - FunQA 上，IoU 为 68.2 (SPIKE-RL)，对比 11.6 (Qwen2.5-VL zero-shot)，变化 +56.6。

## 概要

### 问题瓶颈

现有视频大语言模型（Video-LLM）在帧采样上普遍采用**均匀策略**，即对视频中每一帧赋予同等的重要性。这种做法的根本缺陷在于：它忽视了视频中那些罕见但叙事关键的**惊喜时刻**——情节转折、笑点爆发、意外事件等——导致模型被大量冗余帧信息淹没，难以捕捉视频的核心语义转折点。

### 核心洞见

SPIKE-RL 将视频理解重新建模为一个**动态信念更新过程**。其核心思想是：让模型根据历史与近期上下文，显式生成多个“接下来会发生什么”的**可解释文本假设**，形成信念的概率分布；当新帧到达时，计算先验分布与后验分布之间的 **KL 散度**作为**贝叶斯惊喜分数**，量化新帧带来的信息增益。这一惊喜信号不仅能精准定位视频中的叙事关键点，还可用于引导非均匀的帧采样，使下游模型将有限的帧预算集中在高信息量区域。

### 方法定位

SPIKE / SPIKE-RL 属于**惊喜驱动的自适应帧采样方法**，其方法谱系可定位于：

- **相对于均匀采样基线**：将帧采样概率从均匀分布替换为与贝叶斯惊喜分数成比例的加权分布，是本文唯一的“变化槽位”。
- **相对于传统镜头边界检测方法**（如基于 RGB 直方图差、边缘变化率 ECR、光流的镜头检测）：SPIKE 捕捉的是**语义层面的叙事惊喜**，而非低级的视觉不连续性。
- **相对于零样本 Video-LLM 惊喜评分**（如直接询问 Qwen2.5-VL 判断惊喜）：SPIKE 通过显式信念跟踪和 KL 散度计算，提供了更可靠、与人类判断高度一致的惊喜量化。
- **SPIKE-RL 的强化学习扩展**：在 SPIKE 基础上引入 GRPO（Group Relative Policy Optimization），以最终视频字幕质量（LLM-Match 评分）作为奖励信号，反向优化假设生成策略，进一步提升惊喜检测精度。

### 主要结果速览

在三个惊喜定位基准上，SPIKE-RL 展现出对零样本基线的压倒性优势：

- **Oops! 数据集**：Acc@0.25s 达 **62.9%**，接近人类表现（62.1%），远超零样本 Qwen2.5-VL 的 6.6%（+56.3 个百分点）。
- **FunQA 数据集**：IoU 达 **68.2**，较零样本基线的 11.6 提升 56.6 点，超越所有专用基线。
- **Mr. Bean 数据集**：IoU 达 **61.1**，较零样本基线的 13.8 提升 47.3 点。

在五个下游视频理解基准（BlackSwan、FunQA、ExFunTube、VideoMME-S、NextQA）上，惊喜加权采样相比均匀采样**持续带来性能提升**，例如在 ExFunTube 上提升 **+7.0%**（LLM-Match），在 VideoMME-S（32B 模型）上提升 **+3.6%**（准确率）。

SPIKE 和 SPIKE-RL 的惊喜得分与人类判断的 Spearman 相关系数分别达到 **0.84** 和 **0.87**，验证了该方法与人类惊喜感知的高度一致性。

### 视频理解的叙事瓶颈：均匀采样错失关键瞬间

视频大语言模型（Video-LLM）近年来在视频理解任务上取得了显著进展，但其底层帧采样策略仍普遍沿用**均匀采样**——将视频等间隔切分，每段抽取相同数量的帧。这一看似公平的策略在叙事型视频中暴露出根本性缺陷：大多数视频内容由冗余的过渡帧构成，而决定叙事走向的**惊喜时刻**（surprising moments）——如意外摔倒、剧情反转、笑点触发——往往仅占据极短的片段。均匀采样将有限的帧预算平均分配给所有区域，导致模型被大量低信息量帧淹没，难以捕捉这些稀疏但关键的高信息量瞬间（Figure 1a）。

### 现有方法的局限：缺乏信念层面的惊喜建模

针对视频中“有趣/意外片段”的检测，已有工作主要沿两条路线展开：

- **低层视觉信号方法**：如基于光流的运动幅度检测（Motion Magnitude, Epstein et al., 2020）、视频速度变化（Video Speed, Epstein et al., 2020）等。这些方法仅依赖像素级变化，无法区分“视觉上剧烈但语义上平凡”的镜头运动与“视觉平缓但叙事上惊人”的转折——例如一个细微的面部表情变化可能承载巨大的叙事惊喜，却几乎不触发运动检测。

- **端到端黑箱方法**：如自监督惊喜检测F2C2V（Duka et al., 2022），虽能学习部分惊喜模式，但缺乏对模型**内部信念状态**的显式建模，难以解释“为什么某帧令人惊讶”，也无法将惊喜信号与下游推理任务有效衔接。

核心瓶颈在于：现有方法均未将视频理解形式化为**动态信念更新过程**。模型在观看视频时，其内部对“接下来会发生什么”的预期如何随新帧变化？这种预期变化的幅度能否被量化并用于指导帧采样？这些问题尚未被系统探索。

### 本文动机：从贝叶斯惊喜到惊喜引导的帧采样

本文提出将视频理解重新定义为**信念跟踪问题**：模型基于已观察到的视频历史，持续生成关于未来的可解释文本假设，并在新帧到来时量化这些假设的概率变化。这一视角直接借鉴认知科学中的**贝叶斯惊喜理论**（Itti & Baldi, 2005）——惊喜被定义为先验信念分布与后验信念分布之间的KL散度，衡量新观测带来的信息增益。

基于此，本文的动机包含两个递进层次：

1. **惊喜定位**：能否构建一个框架（SPIKE），显式跟踪视频LLM对文本假设的信念分布，并利用KL散度精确量化每一时刻的惊喜程度，使其与人类对惊喜的判断高度一致？

2. **惊喜利用**：能否将惊喜信号转化为非均匀的帧采样策略，让下游视频LLM将更多帧预算分配到高惊喜区域，从而持续提升多项视频理解任务的性能？进一步地，能否通过强化学习（SPIKE-RL）优化假设生成过程，使惊喜检测本身也受益于下游任务反馈？

这一动机的深层洞察在于：**惊喜不仅是视频理解的目标，更应成为视频理解的手段**——通过识别“哪些帧改变了模型的信念”，系统可以更高效地分配有限的计算资源，聚焦于真正推动叙事发展的关键片段。

## 核心方法与创新机理

### 瓶颈洞察：均匀采样的叙事盲区

现有视频大语言模型（Video-LLM）普遍采用**均匀帧采样**策略，即从视频中等间隔抽取固定数量的帧送入模型。这一策略隐含假设所有帧的信息价值均等，但在叙事型视频中，真正决定理解质量的关键时刻往往是稀疏且不可预测的“惊喜瞬间”——例如幽默视频的笑点、事故视频的转折点。均匀采样导致模型被大量冗余帧淹没，在固定帧预算下难以捕获这些罕见的叙事核心，构成当前视频理解的**关键瓶颈**。

### 核心机制：从信念跟踪到惊喜量化

SPIKE 将视频理解重新定义为**动态信念更新过程**。其核心创新在于显式建模并跟踪模型对“接下来会发生什么”的信念分布，并通过贝叶斯惊喜（Bayesian Surprise）量化新观察帧带来的信息增益。具体而言，SPIKE 包含以下关键组件：

1. **可解释的文本信念空间**：根据历史摘要 $H_t$ 和先验帧窗口 $\mathcal{W}_t$，通过核采样生成 $N$ 个自然语言假设 $b_{t,i}$（如“一个人会摔倒”或“球会入网”），将模型的内部信念显式化为可解释的概率分布。

2. **先验-后验分布计算**：利用 Video-LLM 计算每个假设在观察新帧 $O_t$ 前后的负对数似然，通过 softmax 归一化得到先验分布 $P_{\text{prior}}$ 和后验分布 $P_{\text{post}}$：
   $$P_{\mathrm{prior}}(b_{t,i} \mid H_t, \mathcal{W}_t) = \frac{\exp\left(-\frac{1}{\tau} \cdot \mathrm{NLL}(b_{t,i} \mid H_t, \mathcal{W}_t)\right)}{\sum_{j=1}^N \exp\left(-\frac{1}{\tau} \cdot \mathrm{NLL}(b_{t,j} \mid H_t, \mathcal{W}_t)\right)}$$
   $$P_{\mathrm{post}}(b_{t,i} \mid H_t, \mathcal{W}_t, O_t) = \frac{\exp\big(-\frac{1}{\tau} \cdot \mathrm{NLL}\big(b_{t,i} \mid H_t, \mathcal{W}_t, O_t\big)\big)}{\sum_{j=1}^N \exp\big(-\frac{1}{\tau} \cdot \mathrm{NLL}\big(b_{t,j} \mid H_t, \mathcal{W}_t, O_t\big)\big)}$$

3. **KL 散度作为惊喜分数**：以先验到后验的 KL 散度量化新帧触发的信念变化幅度：
   $$\mathcal{S}_t = D_{\mathrm{KL}}\big(P_{\mathrm{post}}(\cdot \mid H_t, \mathcal{W}_t, O_t) \big\mid\big| P_{\mathrm{prior}}(\cdot \mid H_t, \mathcal{W}_t)\big)$$
   该标量分数直接反映新帧对模型信念系统的冲击程度。

### 关键变更槽位：从均匀到惊喜加权的采样

SPIKE 对标准 Video-LLM 管线的**唯一结构性变更**在于帧采样策略（`frame_sampling_strategy`）：

| 组件 | 基线值 | SPIKE 方案 | 证据锚点 |
|------|--------|------------|----------|
| 帧采样策略 | 均匀采样（每帧等概率） | 惊喜加权采样：采样概率正比于贝叶斯惊喜分数 | “We replace the standard uniform frame sampling with surprise-weighted sampling in Qwen2.5-VL” |

具体实现中，先将视频均匀划分为 $K$ 个片段，计算每段的惊喜分数 $s_i$，再通过带温度 $\tau_s$ 的 softmax 转换为采样概率：
$$p_i = \mathrm{softmax}\left(\frac{s_i}{\tau_s}\right) = \frac{\exp(s_i/\tau_s)}{\sum_{j=1}^K \exp(s_j/\tau_s)}$$
这一设计使帧预算向高惊喜区域倾斜，同时保持与下游 Video-LLM 的解耦性——SPIKE 作为即插即用的采样层，无需修改下游模型架构。

### SPIKE-RL：信念优化的强化学习扩展

SPIKE-RL 在 SPIKE 基础上引入 **GRPO（Group Relative Policy Optimization）** 训练环节，解决零样本假设生成可能缺乏多样性和精准性的问题。其核心创新在于：**将最终视频字幕的匹配质量作为奖励信号，反向传播优化中间信念假设的生成策略**。

训练流程为：对每条视频生成 $M$ 条假设轨迹，经惊喜加权采样后生成字幕，使用 LLM-Match 评分获得奖励 $R^{(r)}$，经 Z-score 归一化得到优势值 $A^{(r)} = \frac{R^{(r)} - \mu_R}{\sigma_R}$，最终通过策略梯度损失优化假设生成器：
$$\mathcal{L}_{\mathrm{belief-optimization}}(\theta) = -\frac{1}{M} \sum_{r=1}^{M} A^{(r)} \left( \sum_{t} \sum_{k=1}^{K} \log p_{\theta}(b_{t,k}^{(r)} \mid H_{t}^{(r)}, \mathcal{W}_{t}^{(r)}) \right)$$
该机制使假设生成从“被动描述”转向“主动预测”，提升了信念多样性和惊喜定位精度。

### 创新验证：与人类判断的高度一致

SPIKE 和 SPIKE-RL 的惊喜得分与人类判断的 Spearman 相关系数分别达到 **0.84** 和 **0.87**（Section 4.3），表明模型捕获的惊喜信号与人类感知高度吻合。在惊喜定位基准上，SPIKE-RL 在 Oops! 数据集上达到 Acc@0.25s **62.9%**，接近人类表现（62.1%），远超零样本 Qwen2.5-VL 的 6.6%（Table 1）。在五个下游视频理解任务上，惊喜加权采样相比均匀采样**持续带来性能提升**，例如在 ExFunTube 上提升 **+7.0%** LLM-Match（Table 2），验证了该创新的通用性和有效性。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_QLiXtWEAkq/figures/002_Figure_2.jpg]]
*Figure 2: (a) Overall architecture: SPIKE computes surprise scores, which guide weighted frame sampling for downstream tasks. (b) SPIKE : Given history H _ { t } , prior window W , , and observed frame O _ { t } . , the hypothesis generator produces belief set B _ { t } . . The hypothesis scorer computes P _ { p r i o r } and P _ { p o s t } . , yielding surprise score S _ { t } as KL divergence*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_QLiXtWEAkq/figures/003_Figure_3.jpg]]
*Figure 3: SPIKE-RL explores multiple hypothesis trajectories, whose surprise scores guide frame sampling. Captions from these rollouts are scored with LLM-Match, and GRPO propagates the reward to improve hypothesis generation*

SPIKE / SPIKE-RL 的整体架构围绕一个核心思想展开：**将视频理解建模为动态信念更新过程**，并通过量化“惊喜”来引导帧采样，从而将有限的计算预算聚焦于视频中叙事关键但罕见的转折点。其 pipeline 由五个主要模块串联而成，形成“信念维护 → 假设生成 → 先验/后验评分 → 惊喜量化 → 惊喜加权采样”的完整闭环（Figure 2）。

### 模块关系与数据流

1. **历史摘要维护（Historical Summary Maintenance）**  
   系统持续维护一个滚动更新的文本摘要 $H_t$，用于压缩从视频开始到当前时刻之前已发生的叙事内容。该摘要通过 **BART-Large-CNN** 进行压缩，为后续假设生成提供长期上下文记忆，避免模型仅依赖近期帧而丢失全局叙事线索。

2. **假设生成器（Hypothesis Generator）**  
   在每个时间步 $t$，基于历史摘要 $H_t$ 和先验帧窗口 $\mathcal{W}_t$（即新帧 $O_t$ 之前的若干帧），通过核采样（nucleus sampling）生成 $N$ 个可解释的文本假设 $b_{t,1}, \dots, b_{t,N}$，描述“接下来可能发生什么”。这些假设构成了模型在当前时刻的显式信念空间。

3. **先验/后验评分器（Prior/Posterior Scorer）**  
   利用视频大语言模型（Video-LLM）计算每个假设 $b_{t,i}$ 在观察新帧 $O_t$ 前后的负对数似然（NLL），并通过带温度参数 $\tau$ 的 softmax 归一化，分别得到先验分布 $P_{\text{prior}}$ 和后验分布 $P_{\text{post}}$：
   $$P_{\mathrm{prior}}(b_{t,i} \mid H_t, \mathcal{W}_t) = \frac{\exp\left(-\frac{1}{\tau} \cdot \mathrm{NLL}(b_{t,i} \mid H_t, \mathcal{W}_t)\right)}{\sum_{j=1}^N \exp\left(-\frac{1}{\tau} \cdot \mathrm{NLL}(b_{t,j} \mid H_t, \mathcal{W}_t)\right)}$$
   $$P_{\mathrm{post}}(b_{t,i} \mid H_t, \mathcal{W}_t, O_t) = \frac{\exp\big(-\frac{1}{\tau} \cdot \mathrm{NLL}\big(b_{t,i} \mid H_t, \mathcal{W}_t, O_t\big)\big)}{\sum_{j=1}^N \exp\big(-\frac{1}{\tau} \cdot \mathrm{NLL}\big(b_{t,j} \mid H_t, \mathcal{W}_t, O_t\big)\big)}$$

4. **惊喜评分器（Surprise Scorer）**  
   以先验到后验的 KL 散度量化新帧 $O_t$ 带来的信息增益，输出标量惊喜分数 $\mathcal{S}_t$：
   $$\mathcal{S}_t = D_{\mathrm{KL}}\big(P_{\mathrm{post}}(\cdot \mid H_t, \mathcal{W}_t, O_t) \big\| P_{\mathrm{prior}}(\cdot \mid H_t, \mathcal{W}_t)\big) = \sum_{i=1}^N P_{\mathrm{post}}(b_{t,i}) \log \frac{P_{\mathrm{post}}(b_{t,i})}{P_{\mathrm{prior}}(b_{t,i})}$$
   该分数越高，表明新帧对模型信念的冲击越大，即该时刻越“令人惊讶”。

5. **惊喜加权采样器（Surprise-Weighted Sampler）**  
   将视频划分为 $K$ 个时间段，根据各段的惊喜分数 $s_i$ 通过带温度 $\tau_s$ 的 softmax 计算采样概率：
   $$p_i = \mathrm{softmax}\left(\frac{s_i}{\tau_s}\right) = \frac{\exp(s_i/\tau_s)}{\sum_{j=1}^K \exp(s_j/\tau_s)}$$
   下游 Video-LLM 按此概率分布从高惊喜区域抽取更多帧，替代传统的均匀采样策略。

### SPIKE-RL 的强化学习闭环

在 SPIKE 的基础上，**SPIKE-RL** 引入 **GRPO（Group Relative Policy Optimization）** 对假设生成器进行信念优化（Figure 3）。其训练流程为：对同一视频采样 $M$ 条假设轨迹，每条轨迹通过惊喜加权采样生成最终视频字幕，由 LLM-Match 评判器（以 **Olmo-7B-hf** 作为奖励模型）与真值字幕比较得到标量奖励 $R^{(r)}$。组内奖励经 Z-score 归一化得到优势值 $A^{(r)}$，反向传播的信念优化损失为：
$$\mathcal{L}_{\mathrm{belief-optimization}}(\theta) = -\frac{1}{M} \sum_{r=1}^{M} A^{(r)} \left( \sum_{t} \sum_{k=1}^{K} \log p_{\theta}(b_{t,k}^{(r)} \mid H_{t}^{(r)}, \mathcal{W}_{t}^{(r)}) \right)$$
该损失增大高优势轨迹中假设的对数似然，从而端到端地优化假设生成策略，使其更准确地捕捉视频中的惊喜时刻。

### 关键设计选择

- **显式文本信念空间**：与依赖隐式特征或光流的方法（如 **Motion Magnitude** (Epstein et al., 2020)、**F2C2V** (Duka et al., 2022)）不同，SPIKE 将信念表示为人类可解释的文本假设集合，使得惊喜信号具备可审计性，且与人类判断高度相关（Spearman 相关系数达 0.84–0.87）。
- **查询无关的即插即用设计**：惊喜评分过程不依赖下游任务的具体查询，SPIKE 可直接替换 Video-LLM 的均匀采样层，适用于多种视频理解任务。
- **历史摘要的先验锚定**：消融实验表明，移除历史文本摘要会导致 Oops! 上 Acc@1s 从 67.37 降至 61.29，证实长期叙事上下文对惊喜检测至关重要。

SPIKE 将视频理解建模为动态信念更新过程，其核心由五个级联模块构成，并通过三个关键公式将“新帧带来的信息增益”量化为标量惊喜分数。

### 模块一：历史摘要维护

该模块负责将自视频起始以来的叙事上下文压缩为滚动文本摘要 $H_t$。具体而言，每一时刻的视频帧通过底层视觉编码器提取特征后，经轻量级文本解码器生成逐帧描述，再使用 **BART-Large-CNN** 进行摘要压缩。这一长期记忆机制为后续假设生成提供了必要的叙事背景——消融实验显示，移除历史摘要会使 Oops! 上的 Acc@1s 从 67.37 骤降至 61.29，证明长期上下文对惊喜检测至关重要。

### 模块二：假设生成器

基于历史摘要 $H_t$ 和先验帧窗口 $\mathcal{W}_t$（即当前帧之前的一段近期帧序列），假设生成器通过核采样生成 $N$ 个“接下来可能发生什么”的文本假设 $\{b_{t,i}\}_{i=1}^N$。这些假设构成了模型的可解释信念空间。SPIKE-RL 通过 GRPO 训练进一步优化假设生成策略，使其平均逆余弦相似度从 33.5% 提升至 40.3%，表明 RL 训练有效增强了假设的语义多样性。

### 模块三：先验/后验评分器

该模块利用视频大语言模型 $M$ 计算每个假设 $b_{t,i}$ 在观察新帧 $O_t$ 前后的负对数似然（NLL），并通过温度参数 $\tau$ 的 softmax 归一化得到先验分布 $P_{\mathrm{prior}}$ 和后验分布 $P_{\mathrm{post}}$：

**先验分布**（观察新帧前）：

$$P_{\mathrm{prior}}(b_{t,i} \mid H_t, \mathcal{W}_t) = \frac{\exp\left(-\frac{1}{\tau} \cdot \mathrm{NLL}(b_{t,i} \mid H_t, \mathcal{W}_t)\right)}{\sum_{j=1}^N \exp\left(-\frac{1}{\tau} \cdot \mathrm{NLL}(b_{t,j} \mid H_t, \mathcal{W}_t)\right)}$$

其中 $\mathrm{NLL}(b_{t,i} \mid H_t, \mathcal{W}_t)$ 表示模型 $M$ 在仅给定历史摘要和先验窗口的条件下，对假设 $b_{t,i}$ 的负对数似然。

**后验分布**（观察新帧后）：

$$P_{\mathrm{post}}(b_{t,i} \mid H_t, \mathcal{W}_t, O_t) = \frac{\exp\big(-\frac{1}{\tau} \cdot \mathrm{NLL}\big(b_{t,i} \mid H_t, \mathcal{W}_t, O_t\big)\big)}{\sum_{j=1}^N \exp\big(-\frac{1}{\tau} \cdot \mathrm{NLL}\big(b_{t,j} \mid H_t, \mathcal{W}_t, O_t\big)\big)}$$

后验分布额外引入了新帧 $O_t$ 的信息，反映了模型在“看到”新帧后对假设信念的更新。

### 模块四：惊喜评分器

惊喜分数定义为先验分布到后验分布的 KL 散度，量化新帧 $O_t$ 带来的信息增益：

$$\mathcal{S}_t = D_{\mathrm{KL}}\big(P_{\mathrm{post}}(\cdot \mid H_t, \mathcal{W}_t, O_t) \big\mid\big| P_{\mathrm{prior}}(\cdot \mid H_t, \mathcal{W}_t)\big) = \sum_{i=1}^N P_{\mathrm{post}}(b_{t,i}) \log \frac{P_{\mathrm{post}}(b_{t,i})}{P_{\mathrm{prior}}(b_{t,i})}$$

该分数的因果机制在于：若新帧高度符合先验信念，则先验与后验分布接近，KL 散度趋近于零；若新帧颠覆了模型预期（如意外事件发生），则后验分布剧烈偏移，KL 散度显著增大。实验表明，SPIKE 和 SPIKE-RL 的惊喜得分与人类判断的 Spearman 相关系数分别达到 0.84 和 0.87，验证了该指标与人类惊喜感知的高度一致性。

### 模块五：惊喜加权采样器

将视频均匀划分为 $K$ 个片段，每个片段 $i$ 的惊喜分数 $s_i$ 为该片段内各时刻惊喜分数的聚合值。采样概率通过带温度 $\tau_s$ 的 softmax 计算：

$$p_i = \mathrm{softmax}\left(\frac{s_i}{\tau_s}\right) = \frac{\exp(s_i/\tau_s)}{\sum_{j=1}^K \exp(s_j/\tau_s)}$$

下游视频大语言模型根据 $p_i$ 从高惊喜区域抽取更多帧，替代传统的均匀采样策略。这一替换在五个下游基准上持续带来性能提升，例如在 ExFunTube 上 SPIKE-RL 较均匀采样提升 +7.0% LLM-Match。

### SPIKE-RL 的信念优化（模块六）

SPIKE-RL 在以上模块基础上引入 GRPO 训练，通过最终视频字幕质量奖励反向优化假设生成。具体而言，对每条轨迹 $r$ 生成的字幕 $c^{(r)}$ 使用 LLM-Match 评分得到奖励 $R^{(r)}$，经组内 Z-score 归一化得到优势值：

$$A^{(r)} = \frac{R^{(r)} - \mu_R}{\sigma_R}$$

信念优化损失为策略梯度形式，增大高优势轨迹中假设的对数似然：

$$\mathcal{L}_{\mathrm{belief-optimization}}(\theta) = -\frac{1}{M} \sum_{r=1}^{M} A^{(r)} \left( \sum_{t} \sum_{k=1}^{K} \log p_{\theta}(b_{t,k}^{(r)} \mid H_{t}^{(r)}, \mathcal{W}_{t}^{(r)}) \right)$$

其中 $M$ 为轨迹组大小，$p_{\theta}$ 为假设生成器的参数化分布。该损失通过增大高奖励轨迹中假设的生成概率，隐式引导模型学习生成更准确、更多样的信念假设。

## 实验与关键发现

### 惊喜定位基准评估

SPIKE 和 SPIKE-RL 在三个惊喜定位基准上的表现如表 1 所示。核心发现如下：

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_QLiXtWEAkq/figures/004_Table_1.jpg]]
*Table 1: Performance of SPIKE and SPIKE-RL on surprise localization*

**Oops! 数据集**：SPIKE-RL 在 Acc@0.25s 上达到 62.9%，接近人类表现（62.1%），远超零样本 Qwen2.5-VL 的 6.6%（+56.3 个百分点）。在更宽松的 Acc@1s 指标上，SPIKE-RL 达到 69.1%，而零样本基线仅为 9.6%。SPIKE（无 RL 训练）同样表现强劲，Acc@0.25s 为 60.0%，Acc@1s 为 67.4%，均大幅超越所有专用基线，包括此前最强的方法 **Video Speed**（Epstein et al., 2020）和自监督方法 **F2C2V**（Duka et al., 2022）。

**FunQA 数据集**：SPIKE-RL 的 IoU 达到 68.2，较零样本 Qwen2.5-VL 的 11.6 提升 56.6 点，且超越所有对比方法。SPIKE 的 IoU 为 65.7，同样显著优于 **TimeChat**（Ren et al., CVPR 2023）等时间敏感多模态模型。

**Mr. Bean 数据集**：SPIKE-RL 的 IoU 为 61.1，相较 SPIKE 的 54.8 提升 6.3 点，表明 GRPO 训练在需要捕捉细微表情变化的惊喜场景中带来了实质增益。然而，该数据集上的绝对 Acc@0.25s 仍然较低，提示模型在非运动型的语义惊喜检测上仍有提升空间。

### 下游任务上的惊喜加权采样

表 2 展示了将 Qwen2.5-VL 的均匀帧采样替换为惊喜加权采样后，在五个下游基准上的表现。惊喜加权采样相比均匀采样持续带来性能提升：

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_QLiXtWEAkq/figures/005_Table_2.jpg]]
*Table 2: Performance of Qwen2.5-VL with uniform vs. surprise-weighted and other query-free frame sampling methods. MCQ tasks are evaluated with accuracy; generative tasks with LLM-Match. Comparable open-source Video-LLMs are shown for context*

- **ExFunTube**（LLM-Match）：75.7 vs. 68.7（+7.0%），为最大增益
- **FunQA Task 2**（LLM-Match）：71.4 vs. 66.8（+4.6%）
- **VideoMME-S**（Accuracy）：62.5 vs. 59.8（+2.7%）
- **BlackSwan**（Accuracy）：69.5 vs. 67.2（+2.3%）
- **NextQA**（Accuracy）：70.3 vs. 68.6（+1.7%）

在更大规模的 Qwen2.5-VL-32B 上，惊喜加权采样同样有效：BlackSwan 上 +2.3%（71.7 vs. 69.4），VideoMME-S 上 +3.6%（73.5 vs. 69.9）。

与其他查询无关的帧采样方法（RGB Histogram、ECR、Katna、Optical Flow）相比，SPIKE 和 SPIKE-RL 在所有基准上均表现最优，且是唯一在所有五个任务上持续超越均匀采样的方法。这表明基于贝叶斯惊喜的非均匀采样策略具有跨任务泛化性，不仅适用于幽默/惊喜类视频，在通用视频理解任务（如 VideoMME-S、NextQA）上同样有效。

### 消融分析

**历史文本摘要**（Table 6）：移除历史摘要组件后，Oops! 上 Acc@1s 从 67.37 降至 61.29（−6.1 点），Acc@0.25s 从 60.0 降至 53.7（−6.3 点）。这证实长期叙事上下文对信念跟踪和惊喜检测至关重要——没有历史信息，模型无法准确判断新帧是否偏离了既有叙事轨迹。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_QLiXtWEAkq/figures/010_Table_6.jpg]]
*Table 6: Ablation of the historical summary component on the Oops! dataset*

**假设集大小 N**（Tables 4, 5）：N=5 相比 N=3 在 Oops! 上 Acc@1s 仅提升 0.4 点（67.37 vs. 66.93），在 Mr. Bean 上提升 0.6 点。N=10 时收益递减甚至略有退化，表明 5 个假设已能充分覆盖典型信念空间，更多假设引入的噪声可能抵消信息增益。

**先验窗口大小 W**（Table 7）：W=4 时在 Oops! 上达到最优 Acc@1s（67.37）。W=2 时性能下降（66.13），可能因为上下文不足；W=8 时同样下降（66.53），可能因为窗口过大引入了与当前帧无关的冗余信息，稀释了信念更新的精度。

**帧预算 B**（Table 8）：B 从 8 增至 64 时，Acc@0.25s 从 55.60 持续提升至 60.00，Acc@1s 从 63.76 提升至 67.65。B=128 时几乎饱和（Acc@0.25s 仅 +0.25%），说明 64 帧已接近该框架的信息提取上限。

### 惊喜信号与人类判断的一致性

SPIKE 和 SPIKE-RL 的惊喜得分与人类判断的 Spearman 相关系数分别达到 0.84 和 0.87，表明模型对“惊喜时刻”的感知与人类高度一致。SPIKE-RL 的相关系数更高，可归因于 GRPO 训练提升了信念假设的语义多样性：SPIKE-RL 的平均逆余弦相似度为 40.3%，高于 SPIKE 的 33.5%。更丰富的假设空间使模型能够更精细地刻画信念分布的变化，从而产生与人类更吻合的惊喜评分。

### 失败模式与局限性

1. **细微表情惊喜检测不足**：在 Mr. Bean 等依赖面部表情和微妙语义转折的场景中，绝对 Acc@0.25s 仍然较低，模型可能未能完全捕获非运动型的语义惊喜信号。
2. **训练数据偏差**：SPIKE-RL 的训练数据包含 70% 非惊喜视频，可能限制了模型对复杂惊喜模式的泛化能力。
3. **实时性约束**：尽管推理时开销可控，但并行化实现仍可能在某些流式场景中引入延迟，限制了方法在低延迟在线场景中的直接部署。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_QLiXtWEAkq/figures/001_Figure_1.jpg]]
*Figure 1: (a) Uniform sampling misses key moments. (b) Our surprise-based sampling focuses on high-surprise regions, strongly aligning with human laughter. (c) Our method achieves significantly better surprise localization than a zero-shot Qwen2.5-VL baseline*

## 定位与知识库关联

### 1. 核心创新定位

SPIKE/SPIKE-RL 的核心创新在于将**贝叶斯信念跟踪**引入视频大语言模型的帧采样过程，其本质是将视频理解重新建模为动态信念更新问题。与现有视频LLM普遍采用的均匀帧采样策略不同，该方法通过显式跟踪模型对可解释文本假设的信念分布，并利用新帧触发的KL散度量化信念变化幅度，从而识别视频中罕见但叙事关键的“惊喜时刻”。

这一设计直接回应了当前视频LLM领域的核心瓶颈：**均匀采样将大量冗余帧送入模型，淹没了对叙事转折点起决定作用的稀疏关键帧**。SPIKE的因果调节旋钮在于，将帧采样概率从“每帧等可能”转变为“与贝叶斯惊喜分数成正比”，使模型的计算资源向信息增益最大的区域倾斜。

### 2. 与现有工作的关系

#### 2.1 惊喜检测方法

在惊喜定位这一具体任务上，SPIKE/SPIKE-RL 与以下方法形成对比：

- **基于运动的启发式方法**：**Motion Magnitude**（Epstein et al., 2020）和**Video Speed**（Epstein et al., 2020）依赖光流或播放速度等低级视觉特征检测惊喜。SPIKE在Oops!上的Acc@0.25s（60.0%）远超Video Speed（39.2%），证明语义层面的信念跟踪比运动启发式更有效。

- **自监督学习方法**：**F2C2V**（Duka et al., 2022）通过自监督训练检测惊喜，但SPIKE-RL（62.9%）仍显著超越该方法，且无需专门的惊喜检测训练数据。

- **零样本视频LLM基线**：Qwen2.5-VL直接作为惊喜评分器时，在Oops!上仅获得6.6%的Acc@0.25s，说明即使强大的视频LLM也无法在零样本条件下隐式完成惊喜定位——显式的信念跟踪框架是必需的。

#### 2.2 视频LLM帧采样策略

在帧采样这一更广泛的维度上，SPIKE与以下查询无关的采样方法形成对比：

- **传统镜头边界检测方法**：RGB Histogram（V & Narayanan, 2015）、ECR（Mann & Kaur, 2015）、Optical Flow（Wolf, 1996）等方法依赖颜色直方图差、边缘变化率或运动分析来检测镜头切换。Table 2显示，这些方法在五个下游基准上均不及SPIKE-RL的惊喜加权采样，说明镜头边界不等于叙事惊喜。

- **基于聚类的关键帧选取**：Katna通过聚类选取代表性帧，但同样无法区分叙事重要性。

- **均匀采样基线**：Qwen2.5-VL（Uniform）在ExFunTube上仅获68.7%的LLM-Match，而SPIKE-RL采样提升至75.7%（+7.0%），这是所有基准中最大的单项提升。

#### 2.3 视频LLM模型对比

Table 2还将SPIKE-RL采样下的Qwen2.5-VL与多个开源视频LLM进行了对比，包括**VideoChat2**（Li et al., 2024）、**VideoLlama2**（Cheng et al., 2024）、**LLaVA-Video**（Liu et al., 2023）以及专为幽默理解设计的**FunMentor**（Xie et al., 2025）。SPIKE-RL采样在多数基准上取得最优或接近最优的结果，且该方法作为采样层的即插即用特性意味着它可以与任何视频LLM结合。

### 3. 适用边界与局限

#### 3.1 适用场景

- **强适用**：包含明确叙事转折、笑点、意外事件的视频理解任务（如FunQA、Oops!、Mr. Bean、ExFunTube），惊喜信号与任务目标高度契合。
- **中等适用**：通用视频问答（VideoMME-S、NextQA），惊喜加权采样仍带来稳定但较小的提升（+1.7~3.6%），说明信息密度分布不均的视频均可受益。
- **弱适用**：信息均匀分布的视频（如监控录像、教程视频），惊喜信号可能退化为噪声，均匀采样可能更优——但该点缺乏直接实验验证。

#### 3.2 已知局限

1. **细微语义惊喜的捕获不足**：在Mr. Bean等依赖细微面部表情变化的惊喜场景中，SPIKE-RL的绝对Acc@0.25s（61.1%）虽然远超基线，但绝对精度仍有提升空间，表明基于文本假设的信念空间可能无法完全捕获非运动型的微妙语义惊喜。

2. **训练数据偏差**：SPIKE-RL的训练数据包含70%非惊喜视频，这可能限制了模型对复杂惊喜模式的泛化能力——模型可能学会了对“明显惊喜”的偏好，而忽略了更微妙的叙事转折。

3. **实时性约束**：尽管推理时开销可控（每帧需生成假设并计算NLL），但在真正流式场景中的并行化实现仍可能引入延迟，论文未提供端到端延迟数据。

4. **信念空间离散化**：当前方法假设信念空间为有限个（N=3~10）文本假设，这种离散化可能遗漏连续信念空间中的精细变化，限制了惊喜定位的时间粒度。

### 4. 开放问题

1. **实时流式扩展**：如何将SPIKE框架扩展到真正的实时视频流中，实现低延迟的在线信念更新？当前方法依赖事后对历史摘要的压缩，流式场景需要增量式的信念维护机制。

2. **任务自适应采样**：当前惊喜信号是任务无关的，能否将惊喜信号与下游任务特定的相关性信号（如问答相关性）结合，实现更精细的自适应帧采样？这可能在通用VQA任务中带来更大提升。

3. **连续信念表示**：当前方法将信念空间离散化为有限个文本假设，如何建模连续或更丰富的信念表示（如嵌入空间中的分布）以提升惊喜定位的细粒度和对微妙语义变化的敏感性？

4. **中间监督信号**：SPIKE-RL的奖励信号仅来自最终字幕的LLM-Match匹配度，是否可以引入更直接的中间信念准确性监督（如人类标注的信念变化）来进一步改进假设生成质量？

5. **交互式场景验证**：该方法在机器人、监控等需要对新信息即时响应的交互式场景中的实用性有待验证，这些场景对延迟和鲁棒性的要求可能远超当前实验设置。

## 原文 PDF

![[paperPDFs/ICLR_2026/SPIKE_RL_Video_LLMs_meet_Bayesian_Surprise.pdf]]
