---
title: Adaptive Action Chunking at Inference-time for Vision-Language-Action Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Adaptive_Action_Chunking_at_Inference_time_for_Vision_Language_Action_Models.pdf
project_link: "https://lance-lot.github.io/adaptive-chunking.github.io/"
code_link: null
aliases:
- AACA
- AACAITVLAM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 以动作熵作为不确定性的代理信号，动态调整推理时的动作块大小：在高熵时减小块大小以增强反应性，低熵时增大块大小以提升一致性。
primary_logic: 利用并行采样的动作熵分布，通过寻找平均熵的最大差分点来自适应地选择最优块大小，无需重新训练即可在推理时优化策略的响应性与稳定性。
claims:
- 在 RoboCasa Kitchen 基准上，不同任务的成功率与动作块大小高度相关，最优块大小不一致。
- AAC 在 RoboCasa 24 个任务的平均成功率较固定块 GR00T 基线提升 2.3% （59.7% → 62.0%）。
- AAC 在 LIBERO 基准的平均成功率提升 0.9% （94.1% → 95.0%），在困难的长序列任务 LIBERO-Long 上提升 4.0%。
- 在真实世界机器人任务中，AAC 的平均成功率从 67.0% 大幅提升至 82.0%。
---

# Adaptive Action Chunking at Inference-time for Vision-Language-Action Models

> [!tip] 核心洞察
> 利用并行采样的动作熵分布，通过寻找平均熵的最大差分点来自适应地选择最优块大小，无需重新训练即可在推理时优化策略的响应性与稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 推理时自适应动作分块：面向视觉-语言-动作模型 |
| 英文题名 | Adaptive Action Chunking at Inference-time for Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.04161) · [Project](https://lance-lot.github.io/adaptive-chunking.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Adaptive Action Chunking (AAC) |
| Dataset | RoboCasa, LIBERO, LIBERO-Pro, Real-world tasks |

> [!tip] 效果简介
> - RoboCasa (24 tasks) 上，Avg. Success Rate (%) 62.0 vs 59.7 (GR00T h=16) (+2.3)。
> - LIBERO (40 tasks) 上，Avg. Success Rate (%) 95.0 vs 94.1 (GR00T h=16) (+0.9)。
> - LIBERO (π0.5 backbone) 上，Avg. Success Rate (%) 97.9 vs 97.0 (π0.5 h=16) (+0.9)。

## 概要

视觉-语言-动作（VLA）模型在机器人操控任务中展现出强大的能力，但其推理时的动作执行通常依赖**固定的动作块大小**（action chunk size）。这一固定设置面临一个根本性瓶颈：不同任务、同一任务的不同执行阶段，对模型的**反应性**（reactivity）与**时间一致性**（temporal consistency）有着截然不同的需求。例如，在 RoboCasa Kitchen 基准上，同一 GR00T N1.5 模型在不同任务上的最优动作块大小差异显著（Figure 1），经验性地选择单一固定值必然导致次优性能。

针对这一问题，本文提出**自适应动作分块**（Adaptive Action Chunking, AAC），一种纯推理时策略。其核心思想是：以**动作熵**作为不确定性的代理信号，在每一步观察下动态选择最优的动作块大小——高熵时减小块大小以增强反应性，低熵时增大块大小以提升一致性。具体而言，AAC 通过并行采样 $N$ 个候选动作块来估计动作分布，计算连续控制（平移/旋转）的差分熵与离散控制（夹持器）的香农熵，再寻找平均熵在不同块大小间的**最大差分点**，并结合最小动作幅度约束，自适应地确定当前最优块大小 $h^*$。该方法无需额外训练或架构修改，可即插即用于各类基于扩散动作头的 VLA 模型。

实验结果表明，AAC 在多个基准和模型主干上均取得了一致性提升：

- **RoboCasa**（24 项任务）：平均成功率从 59.7% 提升至 **62.0%**（+2.3%，GR00T N1.5 主干，Table 1）。
- **LIBERO**（40 项任务）：平均成功率从 94.1% 提升至 **95.0%**（+0.9%）；在困难的长序列子集 LIBERO-Long 上提升 **4.0%**（Table 1）。
- **跨模型泛化**：在 π0.5 主干上，LIBERO 平均成功率从 97.0% 提升至 **97.9%**（+0.9%，Table 2）。
- **分布外泛化**：在 LIBERO-Pro 上，成功率从 3.9% 提升至 **6.3%**（+2.4%，Table 3）。
- **真实世界任务**：平均成功率从 67.0% 大幅提升至 **82.0%**（+15.0%，Table 5），且生成的块大小与人类直觉一致——搬运阶段块大小较大，精细操作阶段块大小较小（Figure 3）。

消融实验进一步验证了自适应选择的必要性：不同固定块大小在不同任务子集上的最优值差异显著（Table 7），而增加并行采样数 $N$ 可持续提升性能，$N=20$ 在成功率与推理延迟（约 20 ms）间取得良好平衡（Table 4）。AAC 的主要局限在于需要并行采样引入额外计算开销，且熵估计的准确性依赖采样数量，在极端实时场景或强分布外任务上的绝对性能仍有提升空间。



视觉-语言-动作（VLA）模型近年来在机器人操作任务中取得了显著进展。这类模型通常将视觉观测和语言指令作为输入，直接输出一系列未来动作，即**动作块（action chunk）**。通过一次推理生成多个未来动作，VLA 模型能够实现相对稳定的闭环控制，同时保持可接受的推理频率。

然而，动作块大小的选择面临一个根本性的权衡：**较大的块**能够提供更强的时间一致性和更平滑的运动轨迹，但会降低机器人对环境变化的反应速度；**较小的块**则能够增强反应性，但可能牺牲动作的连贯性。当前主流的 VLA 模型——如 **GR00T N1.5** 和 **π0.5**——均采用固定的动作块大小，该超参数通常通过经验调参确定，并在整个任务执行过程中保持不变。

这种固定策略存在明显的局限性。如 Figure 1 所示，在 RoboCasa Kitchen 基准的不同任务上，GR00T N1.5 的成功率与动作块大小高度相关，但最优块大小因任务而异：某些任务在块大小为 4 时表现最佳，而另一些任务则需要块大小为 16 或更大。这意味着，**不存在一个全局最优的固定块大小能够适用于所有任务**。更关键的是，即使在单个任务的执行过程中，不同语义阶段对块大小的需求也可能不同——例如，物体搬运阶段适合较大的块以保持运动连贯性，而精细抓取阶段则需要较小的块以确保操作精度。

上述观察揭示了一个核心瓶颈：**固定动作块大小无法根据不同任务和不同执行阶段动态平衡模型的反应性与时间一致性**，导致整体性能受限。这一瓶颈在需要长序列执行和精确操作的任务中尤为突出。

针对这一问题，本文提出了一种推理时自适应动作分块策略——**Adaptive Action Chunking (AAC)**。AAC 的核心思想是：利用模型并行采样生成的动作分布熵作为不确定性的代理信号，在推理时动态选择最优的动作块大小。具体而言，在高熵（高不确定性）时刻减小块大小以增强反应性，在低熵（高置信度）时刻增大块大小以提升时间一致性。该方法无需额外训练或架构修改，可直接应用于任何基于扩散动作头的 VLA 模型，在多个仿真和真实世界基准上均实现了一致的性能提升。



## 核心方法与创新机理

本文的核心创新在于提出了一种**推理时自适应动作分块（Adaptive Action Chunking, AAC）**策略，其本质是将固定动作块大小这一被动的超参数选择，转化为由模型自身不确定性驱动的主动决策过程。与现有视觉-语言-动作（VLA）模型在整条轨迹上使用恒定执行窗口的做法不同，AAC 直接作用于推理阶段，**无需任何额外训练或架构修改**（Figure 2）。

### 关键 changed slots

AAC 对基线 VLA 模型（如 **GR00T N1.5**、**π0.5**）的改动集中在两个核心槽位：

1. **动作块大小选择机制**：从「经验性固定值」变为「基于动作熵的自适应选择」。基线方法通常通过离线调参为所有任务统一指定一个块大小 $h$（例如 $h=16$），而 AAC 在每个决策时刻根据当前观测下的动作不确定性，动态计算最优块大小 $h^*$。

2. **推理时执行窗口**：从「整条轨迹恒定」变为「逐时间步动态变化」。这使得策略能够在需要快速反应的精细操作阶段自动缩短执行窗口，在平稳搬运阶段自动延长窗口以保持时间一致性。

### 核心机制：动作熵驱动的自适应决策

AAC 的核心洞察是：**动作熵可以作为不确定性的代理信号，指导块大小的自适应选择**。其决策流程包含三个关键步骤：

**并行采样与熵估计**。在每个决策时刻，AAC 首先并行生成 $N$ 个候选动作块，然后分别计算连续控制量（平移、旋转）的高斯差分熵和离散控制量（夹持器）的香农熵：

- 离散动作熵：$E_{\mathrm{dis}} = - \sum_{a \in \mathcal{A}} p(a) \log(p(a))$
- 连续动作熵：$E_{t} = \frac{1}{2} \log[ (2 \pi e)^{d} \det(\Sigma_t) ]$

随后在候选块大小 $h$ 上计算平均动作熵 $\overline{E}_h = \frac{1}{h} \sum_{i=t}^{t+h-1} \sum_{j \in \{t,r,g\}} E_j^i$，综合平移、旋转和夹持器三个维度的不确定性。

**最大差分点选择**。AAC 通过寻找平均熵的最大差分点来确定最优块大小：

$$h^{*} = \operatorname*{max}(\arg\operatorname*{max}_h (\overline{E}_{h+1} - \overline{E}_h), \xi)$$

其直觉在于：当增加块大小导致平均熵显著上升时，意味着模型对更远未来动作的预测不确定性急剧增加，此时应截断执行窗口以保证反应性。反之，若熵增长平缓，则可采用更大的块大小以提升时间一致性。

**最小动作幅度约束**。为防止块大小过小导致动作碎片化，AAC 引入下界约束 $\xi = \arg\min_l (m(l) > \alpha)$，确保所选块大小对应的累积动作幅度超过阈值 $\alpha$，从而保证运动连贯性。

### 创新性质定位

AAC 属于**推理时优化（inference-time optimization）**范畴，其创新性体现在三个层面：

- **无训练即插即用**：不改变模型权重或架构，可直接应用于任何具有扩散动作头的 VLA 模型。实验表明该方法在 GR00T N1.5 和 π0.5 两个不同主干上均有效（Table 1, Table 2）。
- **不确定性感知的执行调度**：首次将动作熵引入执行窗口的自适应调节，使 VLA 模型具备了类似人类的「谨慎-果断」行为切换能力。定性分析显示，AAC 产生的块大小与人类直觉高度一致——搬运阶段块大小较大，精细操作阶段块大小较小（Figure 3）。
- **轻量高效**：仅需 20 个并行采样即可有效估计动作熵，额外推理延迟约 20 ms（Table 4），在性能提升与计算开销之间取得了良好平衡。



AAC（Adaptive Action Chunking）是一种纯推理时策略，无需额外训练或修改模型架构，即可嵌入任意基于扩散动作头的 VLA 模型。其核心思想是：**以动作熵作为不确定性的代理信号，在每个决策时刻自适应地选择最优动作块大小 $h^*$，从而在单一 episode 内动态平衡策略的反应性与时间一致性**。

### 算法总览

AAC 的整体流程如 Figure 2 所示，包含四个顺序执行的模块：

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/002_Figure_2.jpg]]
*Figure 2: An overview of AAC. The proposed Adaptive Action Chunking (AAC) algorithm operates solely at inference-time, without any extra training or architectural changes. Specifically, we exploit the action entropy of continuous and discrete values as the cue to adaptively determine the optimal chunk size*

1. **多采样动作块生成（Multi-Sample Action Chunk Generation）**  
   给定当前观测 $o_t$，从 VLA 模型的扩散动作头中并行采样 $N$ 个候选动作块 $\{ \mathbf{A}_t^{(1)}, \mathbf{A}_t^{(2)}, \dots, \mathbf{A}_t^{(N)} \}$，每个候选块包含 $H$ 步动作序列（$H$ 为预设的最大块大小）。并行采样为后续的熵估计提供了动作分布的基础。

2. **动作熵估计（Action Entropy Estimation）**  
   对每个候选块内的每一步动作，分别计算三类控制量的熵：
   - **连续平移/旋转**：假设动作服从多元高斯分布，使用差分熵公式 $E_{t} = \frac{1}{2} \log[ (2 \pi e)^{d} \det(\Sigma_t) ]$（式 3），其中 $\Sigma_t$ 由 $N$ 个样本的经验协方差矩阵估计得到。
   - **离散夹持器**：使用离散熵公式 $E_{\mathrm{dis}} = - \sum_{a \in \mathcal{A}} p(a) \log(p(a))$（式 2），其中 $p(a)$ 由 $N$ 个样本中各类别的频率估计。

   随后，对候选块大小 $h$ 内的所有步，计算综合平移、旋转和夹持器的**平均动作熵** $\overline{E}_h = \frac{1}{h} \sum_{i=t}^{t+h-1} \sum_{j \in \{t,r,g\}} E_j^i$（式 4）。

3. **最优块大小选择（Optimal Chunk Size Selector）**  
   核心决策逻辑基于以下观察：当块大小从 $h$ 增加到 $h+1$ 时，若新增动作步的熵显著增大，说明模型对该步的预测高度不确定，此时应减小块大小以增强反应性。因此，AAC 寻找平均熵的**最大差分点**作为最优块大小：
   $$h^{*} = \operatorname*{max}(\arg\operatorname*{max}_h (\overline{E}_{h+1} - \overline{E}_h), \xi) \quad \text{(式 5)}$$
   其中 $\xi$ 为最小动作幅度下界（式 6），用于保证运动连贯性，防止块大小过小导致机器人停滞。

4. **自适应动作执行（Adaptive Action Execution）**  
   从最优候选块中截取前 $h^*$ 步动作，交由机器人执行。执行完毕后，基于新观测重新进入上述流程，实现闭环的自适应重规划。

### 与固定块基线的对比

传统的固定动作块策略（如 GR00T N1.5）在整个 episode 中使用恒定的执行视野 $h$，其取值需在部署前通过大量实验手动调优。Figure 1 揭示了这一做法的根本缺陷：不同任务对块大小的最优需求不一致，且同一任务的不同执行阶段也可能需要不同的块大小。AAC 通过将块大小选择转化为推理时的数据驱动决策，消除了对手动调参的依赖，并实现了任务级和阶段级的自适应。



AAC 的核心设计理念是将动作熵作为不确定性的代理信号，在推理时动态选择最优的动作块大小，从而在反应性与时间一致性之间取得自适应平衡。整个算法由四个关键模块串联构成，无需额外训练或修改模型架构。

### 多采样动作块生成

给定当前观测 $o_t$，AAC 首先利用 VLA 模型的扩散动作头并行生成 $N$ 个候选动作块。每个候选块包含 $H$ 步动作序列，其中每步动作由连续控制量（平移 $\Delta x, \Delta y, \Delta z$ 和旋转 $\Delta q$）与离散控制量（夹持器状态）组成。并行采样的目的是获取动作空间的分布信息，为后续的熵估计提供统计基础。扩散动作头的训练遵循标准的流匹配损失：

$$\mathcal{L}_{\mathrm{fm}}(\theta) = \mathbb{E}_{\tau}\left[\left\| \mathbf{V}_\theta(\phi_t, \mathbf{A}_t^{(\tau)}, \mathbf{q}_t) - (\epsilon - \mathbf{A}_t) \right\|^2\right] \tag{1}$$

其中 $\mathbf{V}_\theta$ 为向量场预测网络，$\phi_t$ 为流匹配时间步，$\mathbf{A}_t^{(\tau)}$ 为加噪后的动作，$\mathbf{q}_t$ 为条件输入（视觉-语言特征），$\epsilon \sim \mathcal{N}(0,I)$ 为噪声。

### 动作熵估计

对于离散控制量（夹持器），AAC 采用标准香农熵度量其不确定性：

$$E_{\mathrm{dis}} = - \sum_{a \in \mathcal{A}} p(a) \log(p(a)) \tag{2}$$

其中 $\mathcal{A}$ 为离散动作空间，$p(a)$ 由 $N$ 个候选块中夹持器动作的经验分布估计。

对于 $d$ 维连续控制量（平移 $d=3$，旋转 $d=4$），AAC 假设其服从多元高斯分布，采用差分熵进行度量：

$$E_{t} = \frac{1}{2} \log\left[ (2 \pi e)^{d} \det(\Sigma_t) \right] \tag{3}$$

其中 $\Sigma_t$ 为 $N$ 个候选块在第 $t$ 步连续动作的协方差矩阵。差分熵同时捕获了方差和协方差信息——当候选动作高度一致时，$\det(\Sigma_t)$ 较小，熵值低；当候选动作发散时，熵值高。

### 最优块大小选择器

AAC 的核心创新在于通过平均熵的差分结构自动确定最优块大小。首先，对于候选块大小 $h$（$1 \leq h \leq H$），计算该窗口内的平均动作熵：

$$\overline{E}_h = \frac{1}{h} \sum_{i=t}^{t+h-1} \sum_{j \in \{t,r,g\}} E_j^i \tag{4}$$

其中 $E_t^i, E_r^i, E_g^i$ 分别为第 $i$ 步的平移、旋转和夹持器熵。$\overline{E}_h$ 综合反映了执行 $h$ 步动作的整体不确定性。

关键洞察在于：**当块大小从 $h$ 增加到 $h+1$ 时，平均熵的差分 $\overline{E}_{h+1} - \overline{E}_h$ 反映了新增步对整体不确定性的边际贡献**。若差分较大，说明新增步的动作高度不确定，此时应减小块大小以增强反应性；若差分趋近于零，说明新增步未显著增加不确定性，可以安全地增大块大小以提升时间一致性。

基于此，最优块大小 $h^*$ 定义为平均熵最大差分点：

$$h^{*} = \operatorname{max}\left(\arg\operatorname{max}_h (\overline{E}_{h+1} - \overline{E}_h),\; \xi\right) \tag{5}$$

其中 $\xi$ 为最小动作幅度约束，用于保证运动连贯性。$\xi$ 的定义如下：

$$\xi = \arg\min_l \left(m(l) > \alpha\right) \tag{6}$$

其中 $m(l)$ 为块大小 $l$ 内的总动作幅度：

$$m(l) = \sum_{i \in \{t,r,g\}} m_i(l) \tag{7}$$

三个分量的定义分别为：

- **平移幅度**：累积位移向量的欧几里得范数

$$m_t(l) = \left\| \sum_{l} \Delta x, \sum_{l} \Delta y, \sum_{l} \Delta z \right\| \tag{8}$$

- **旋转幅度**：顺序合成四元数的范数

$$m_r(l) = \left\| \prod_{l} \Delta q \right\| \tag{9}$$

- **夹持器幅度**：状态切换指示函数

$$m_g(l) = \mathbf{1}_{\mathrm{switch}} \tag{10}$$

最小幅度约束 $\xi$ 确保了即使熵差分很小，当选出的块大小对应的累积动作幅度低于阈值 $\alpha$ 时，系统会强制增大块大小，避免因动作过小导致的运动停滞。

### 自适应动作执行

选定 $h^*$ 后，AAC 执行对应候选块的前 $h^*$ 步动作，然后基于新的观测重新进行多采样、熵估计和块大小选择。这一闭环机制使得块大小能够随任务阶段动态调整——在搬运阶段（低不确定性）自动增大块大小以提升效率，在精细操作阶段（高不确定性）自动减小块大小以增强精度。

**算法 1** 总结了完整的 AAC 推理流程：对于每个决策步，并行采样 $N$ 个候选块；计算每步的连续和离散动作熵；遍历所有可能的块大小 $h$，计算 $\overline{E}_h$ 和 $\overline{E}_{h+1} - \overline{E}_h$；通过最大差分点确定 $h^*$ 并施加最小幅度约束；执行动作并进入下一步观测。

### 设计要点总结

AAC 的公式体系体现了三个关键设计原则：

1. **熵作为不确定性代理**：通过并行采样的经验分布估计动作熵，无需额外的置信度网络或贝叶斯推断。
2. **差分结构定位最优块大小**：$\overline{E}_{h+1} - \overline{E}_h$ 的峰值天然对应“不确定性骤增”的边界，恰好是需要切换为更小块的临界点。
3. **幅度约束防止过度保守**：$\xi$ 下界确保在低不确定性场景下不会退化为逐步执行，维持了动作分块带来的时间一致性优势。

### 补充图表

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/001_Figure_1.jpg]]
*Figure 1: Effects of action chunk sizes. At inference-time, the success rates of the GR00T N1.5 [2] on different tasks of Robo-Casa Kitchen [28] are highly related to the action chunk size. It can be observed that it is difficult and sub-optimal to empirically set a fixed value for various manipulation tasks*

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/004_Figure_3.jpg]]
*Figure 3: Rollout of chunk sizes from AAC. The derived chunk sizes align with human intuitions with respect to different semantic phases: a large chunk size is observed during the transportation stage, while a small chunk size appears at the critical manipulation stage*



## 实验与关键发现

### 核心问题与实验逻辑

固定动作块大小（action chunk size）在视觉-语言-动作（VLA）模型推理中面临一个根本性困境：不同任务乃至同一任务的不同执行阶段，对反应性（reactivity）与时间一致性（temporal consistency）的需求截然不同。例如，物体搬运阶段需要较大的块大小以保持运动连贯，而精细抓取阶段则需要较小的块大小以快速响应环境变化。实验的核心目标是验证 **AAC** 能否通过动作熵（action entropy）这一代理信号，在推理时动态选择最优块大小，从而在无需重新训练的前提下，一致性地超越固定块基线。

实验设计遵循以下逻辑链：
1. **验证固定块的次优性**：通过系统扫描不同固定块大小在多个任务上的成功率，证明不存在一个统一的“最优固定值”。
2. **验证自适应策略的有效性**：在仿真基准（RoboCasa、LIBERO）和真实世界任务上，对比 AAC 与固定块基线的成功率。
3. **验证方法的通用性**：在多个 VLA 模型主干（GR00T N1.5、π0.5）上测试 AAC。
4. **验证自适应决策的合理性**：定性分析 AAC 产生的块大小是否与人类对任务阶段的直觉一致。
5. **验证关键超参数的敏感性**：分析并行采样数量 N 对性能与延迟的影响。

---

### 主结果：仿真基准

**Table 1** 汇总了 AAC 在 RoboCasa 和 LIBERO 两大仿真基准上的主结果。

在 **RoboCasa** 的 24 个任务上，AAC（基于 GR00T N1.5 主干，h=16 基线）将平均成功率从 59.7% 提升至 **62.0%**（+2.3%）。值得注意的是，不同任务子集的最优固定块大小差异显著：例如，某些任务在 h=4 时表现最佳，而另一些在 h=16 时达到峰值（详见 Table 7）。这一现象直接验证了“固定块大小次优”的核心假设。

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/013_Table_7.jpg]]
*Table 7: Success rates (%) with Different Chunk Sizes*

在 **LIBERO** 的 40 个任务上，AAC 将平均成功率从 94.1% 提升至 **95.0%**（+0.9%）。虽然整体提升幅度看似有限，但在困难的长序列任务子集 **LIBERO-Long** 上，提升幅度达到 **4.0%**，说明 AAC 在需要精细时间协调的复杂任务中发挥了更关键的作用。LIBERO 基线本身的高成功率（94.1%）意味着天花板效应压缩了提升空间，但 AAC 仍能在接近饱和的指标上取得统计显著的改善。

**Table 2** 展示了 AAC 在 **π0.5** 主干上的结果：平均成功率从 97.0% 提升至 **97.9%**（+0.9%）。这一结果与 GR00T 主干上的提升幅度一致，证明了 AAC 作为推理时策略的通用性——它不依赖于特定 VLA 模型的架构细节，仅要求模型具备扩散动作头。

**Table 3** 报告了分布外（OOD）泛化基准 **LIBERO-Pro** 上的结果。AAC 将 GR00T 基线的平均成功率从 3.9% 提升至 **6.3%**（+2.4%），将 π0.5 基线的成功率从 30.9% 提升至 **34.8%**（+3.9%）。尽管绝对成功率仍然较低（这是 OOD 场景的固有挑战），但 AAC 在两种主干上均表现出稳定的正向提升，表明动作熵作为不确定性信号在分布偏移下仍然有效。

---

### 主结果：真实世界任务

**Table 5** 报告了真实世界机器人任务上的成功率。AAC 将 GR00T 基线的平均成功率从 67.0% 大幅提升至 **82.0%**（**+15.0%**），提升幅度远超仿真基准。这一显著差距可能源于真实世界中环境噪声和任务变异性更大，固定块策略的刚性缺陷被进一步放大，而 AAC 的自适应机制恰好弥补了这一不足。

**Figure 5** 展示了 AAC 在真实任务中的执行示例。定性观察表明，AAC 产生的动作轨迹更加流畅且安全。**Figure 6** 提供了一个关键的安全对比案例：基线 GR00T 在执行任务时夹持器与桌面发生碰撞，而 AAC 的夹持器则精确到达了合适的最低点。这一现象可以归因于 AAC 在接近接触阶段自动减小了块大小，从而提高了动作精度和反应速度。

---

### 自适应决策的定性验证

**Figure 3** 可视化了一条典型任务执行轨迹中 AAC 选择的块大小变化。结果显示，块大小的动态变化与人类对任务语义阶段的直觉高度一致：在物体搬运阶段，块大小较大（以保持运动连贯性）；在关键操作阶段（如抓取、放置），块大小显著减小（以增强反应性）。这一观察为 AAC 决策机制的合理性提供了直观支持。

**Figure 4** 以热力图形式展示了 LIBERO-Spatial 首个任务上 AAC 块大小决策的时间分布。红色曲线表示不同观察时刻的平均块大小。热力图揭示了一个规律性模式：在任务执行的初期和末期，块大小倾向于较小；在中间稳定执行阶段，块大小较大。这一模式进一步印证了 AAC 能够根据任务进展动态调整执行策略。

---

### 消融实验

**并行采样数量 N 的影响**（Table 4）：AAC 的性能依赖于从多个并行采样的候选动作块中估计动作熵的准确性。实验扫描了 N=1, 5, 10, 20, 30 的设置。结果显示，成功率随 N 增加而单调提升（94.1% → 95.0% → 95.5%），但边际收益递减。N=20 在成功率和推理延迟之间取得了良好平衡，仅引入约 20 ms 的额外推理时间。N=1 退化为无熵估计的情况，性能与固定块基线相当。

**固定块大小的任务依赖性**（Table 7）：在 RoboCasa 各任务上扫描不同固定块大小（h=2, 4, 8, 16, 32），结果显示不同任务的最优 h 值分布广泛，且没有任何一个固定值能在所有任务上达到最优。这从反面证明了自适应选择的必要性。

---

### 失败模式与局限性

尽管 AAC 在多数场景下表现优异，但仍存在以下不足：

1. **极端实时场景的延迟约束**：AAC 需要并行生成 N 个候选动作块来估计熵，引入约 20 ms 的额外延迟。对于需要亚毫秒级响应的任务，这一开销可能不可接受。
2. **OOD 场景的绝对性能瓶颈**：在 LIBERO-Pro 上，AAC 的绝对成功率仍然很低（GR00T+AAC 仅 6.3%）。自适应块策略只能优化执行方式，无法弥补策略模型在分布偏移下的根本性退化。
3. **采样数量 N 的手动调整**：N 的最优值可能因任务而异，目前仍需手动设定，缺乏自动选择机制。
4. **熵度量的局限性**：当前熵估计基于单步动作的边缘分布，未显式建模动作序列之间的时序依赖性。这可能导致在某些需要长程时序协调的任务中，熵信号不够精确。

---

### 公平性说明

所有对比实验均使用相同的预训练权重和微调数据，确保基线模型与 AAC 之间的唯一差异在于推理时的块大小选择策略。真实世界实验在相同硬件和环境下进行，消除了系统偏差。AAC 不涉及任何额外训练或架构修改，因此对比是严格公平的。

### 补充图表

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/003_Table_1.jpg]]
*Table 1: Main Results on RoboCasa and LIBERO Benchmarks. We report the success rate (%) for various subsets and the overall average. Our AAC achieves the best or competitive results across both benchmarks. Bolded entries indicate the highest success rates*

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/005_Table_2.jpg]]
*Table 2: Success rates (%) with*

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/007_Table_3.jpg]]
*Table 3: Success rates (%) on LIBERO-Pro [50]*

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/008_Table_4.jpg]]
*Table 4: Success rates (%) on LIBERO and inference-time under different numbers of samples for estimating action entropy*

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/009_Table_5.jpg]]
*Table 5: Success rates (%) on real-world applications*

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/006_Figure_4.jpg]]
*Figure 4: Distribution of chunk size decisions from AAC. We show the chunk size distribution of episodes on the first task of LIBERO-Spatial: ”Pick up the black bowl next to the cookie box and place it on the plate”. The heatmap indicates the frequency of different chunk sizes at different decision timesteps. The red curve shows the mean chunk size at different observation timesteps*

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/010_Figure_5.jpg]]
*Figure 5: Execution examples for real-world tasks using AAC. Videos of complete execution trajectories will be publicly available*

![[assets/figures/papers/paper_list_l2369_https_arxiv_org_abs_2604_04161/figures/011_Figure_6.jpg]]
*Figure 6: AAC improves action accuracy and safety. Left: the gripper collided with the table. Right: the gripper reached an appropriate lowest point*



## 定位与知识库关联

### 1. 与固定动作分块基线的关系

AAC 的核心创新在于将**动作块大小从固定超参数转化为推理时自适应变量**。在现有视觉-语言-动作（VLA）模型中，动作块大小通常作为经验性超参数在部署前手动设定，例如 GR00T N1.5 和 π0.5 均采用固定的执行范围。然而，Figure 1 的证据表明，不同任务的最优块大小存在显著差异——同一 VLA 模型在 RoboCasa Kitchen 的不同子任务上，成功率对块大小的敏感度极高，且最优值并不一致。这一现象揭示了固定块策略的**结构性瓶颈**：单一超参数无法同时满足搬运阶段对时间一致性的需求与精细操作阶段对反应性的需求。

AAC 通过引入**动作熵**作为不确定性代理信号，将块大小选择从“离线调参”转变为“在线决策”，从而在推理时动态平衡一致性与反应性。这一思路与固定块基线形成了明确的“变体-改进”关系：AAC 保留了扩散动作头生成多步动作块的机制，仅改变了执行范围的确定方式。

### 2. 与其他推理时自适应方法的关联与差异

AAC 属于**推理时策略优化**这一新兴方法类别，其特点是无需重新训练或修改模型架构即可提升策略性能。与以下方向存在潜在关联：

- **测试时计算扩展**：AAC 通过并行采样 N 个候选动作块来估计动作熵，本质上是一种测试时计算扩展策略。Table 4 显示，增加 N 可单调提升成功率（94.1% → 95.0% → 95.5%），这与测试时计算扩展的一般规律一致。但 AAC 的计算开销相对可控：N=20 时仅引入约 20 ms 额外延迟。
- **不确定性引导的动作选择**：AAC 以动作熵度量预测不确定性，并据此调整执行范围。这与基于模型不确定性的自适应控制策略（如 ensemble-based 方法）在思想上有相似之处，但 AAC 的独特之处在于将不确定性直接映射到**执行粒度**而非动作值本身。
- **与模型预测控制（MPC）的对比**：MPC 通常通过优化目标函数动态调整控制范围，而 AAC 无需显式建模环境动力学，仅依赖策略模型自身的动作分布，部署门槛更低。

需要注意的是，AAC 目前仅在**扩散动作头**模型（GR00T N1.5、π0.5）上验证有效（Table 1, Table 2），尚未拓展至自回归动作生成范式。这一适用边界在论文的 limitations 中已被明确指认。

### 3. 适用边界与局限

AAC 的有效性建立在以下前提之上：

1. **扩散动作头的多步预测能力**：AAC 依赖 VLA 模型一次性生成完整动作块的能力，以支持对不同块大小的熵估计。对于逐步自回归生成的策略模型，当前方法无法直接迁移。
2. **并行采样的计算预算**：熵估计需要 N 个并行候选动作块，N 的最优值可能因任务而异（Table 4 显示 N=20 在 LIBERO 上取得良好平衡），且极端实时场景下约 20 ms 的额外延迟可能不可接受。
3. **熵作为不确定性度量的有效性**：当前熵度量基于单步动作的边缘分布（Eq. 2–4），未显式建模动作序列间的时序依赖性。在强分布外（OOD）场景下，这一度量的可靠性可能下降——Table 3 显示 LIBERO-Pro 上绝对成功率仍很低（6.3%），自适应块策略的性能提升有限。

### 4. 开放问题

基于上述分析，以下问题值得进一步探索：

- **更高效的熵估计**：能否通过轻量级代理模型或方差近似来降低并行采样的计算开销，使 AAC 适用于更严格的实时场景？
- **替代不确定性指标**：动作熵是否为最优的块大小选择信号？方差、置信度、或基于模型的预测误差是否能在特定任务上提供更好的指导？
- **跨范式的泛化**：如何将自适应块策略扩展到非扩散策略（如自回归 Transformer 策略）或基于模型的控制器？
- **安全约束的显式集成**：在多模态任务或人机协同场景下，自适应块大小策略是否需要额外的安全约束（如最小反应频率保障）？Figure 6 展示了 AAC 在真实场景中提升了安全性，但这一优势目前是隐式的，缺乏理论保证。
- **时序依赖性的利用**：当前熵度量基于边缘分布，若能引入动作序列的联合熵或互信息，可能进一步提升块大小选择的准确性，尤其在长序列任务（如 LIBERO-Long）中。



## 原文 PDF

![[paperPDFs/CVPR_2026/Adaptive_Action_Chunking_at_Inference_time_for_Vision_Language_Action_Models.pdf]]
