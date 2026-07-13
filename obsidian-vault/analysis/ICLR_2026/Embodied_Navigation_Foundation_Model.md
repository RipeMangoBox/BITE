---
title: "Embodied Navigation Foundation Model"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Embodied_Navigation_Foundation_Model.pdf
project_link: https://pku-epic.github.io/NavFoM-Web/
code_link: null
openreview_forum_id: kkBOIsrCXh
aliases:
- ENFM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过设计时间-视角指示令牌（TVI tokens）和预算感知的时间采样策略（BATS），统一处理不同相机配置和可变时间跨度，使单一模型能够泛化到多种任务和形态。"
primary_logic: "在大规模多样化导航数据上联合训练，并采用灵活的令牌组织与动态采样，可让基础模型无需针对特定任务微调即达到最先进性能，从而迈向通用导航智能。"
claims:
- "在VLN-CE RxR上，多相机设置下成功率从56.3%提升至64.4%，单相机设置下从51.8%提升至57.4%。"
- "在HM3D-OVON上，零样本条件下取得45.2% SR（四视图），超过此前微调的最佳方法（43.6% SR）。"
- "TVI令牌和BATS在消融实验中显著优于其他历史令牌组织方法（如均匀采样、手工令牌），并在不同令牌预算下保持优势。"
- "多任务联合训练在所有任务上均带来一致的性能提升，低资源任务（如搜索、跟踪）获益最大。"
---

# Embodied Navigation Foundation Model

> [!tip] 核心洞察
> 在大规模多样化导航数据上联合训练，并采用灵活的令牌组织与动态采样，可让基础模型无需针对特定任务微调即达到最先进性能，从而迈向通用导航智能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 具身导航基础模型 |
| 英文题名 | Embodied Navigation Foundation Model |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=kkBOIsrCXh) · [Project](https://pku-epic.github.io/NavFoM-Web/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | NavFoM |
| Dataset | VLN-CE RxR (Multi-camera), VLN-CE RxR (Single-camera), HM3D-OVON (Zero-shot, Val Unseen, Four views), EVT-Bench Single Target (Four views) |

> [!tip] 效果简介
> - VLN-CE RxR (Multi-camera) 上，SR 为 64.4，对比 56.3 (ETPNav)，变化 +8.1。
> - VLN-CE RxR (Single-camera) 上，SR 为 57.4，对比 51.8 (best single-view baseline)，变化 +5.6。
> - HM3D-OVON (Zero-shot, Val Unseen, Four views) 上，SR 为 45.2，对比 43.6 (fine-tuned SOTA)，变化 +1.6。

## 概要

### 问题瓶颈

现有导航方法普遍受限于**狭窄的任务设定**和**单一具身形态的专用架构**。无论是视觉语言导航（VLN）、目标搜索、主动跟踪还是自动驾驶，各任务通常采用独立设计的模型，无法实现跨任务、跨形态的通用导航能力。这一碎片化范式导致方法难以泛化，且无法充分利用不同任务间的共享知识。

### 核心方法定位

本文提出**NavFoM**，一个统一的具身导航基础模型。其核心设计围绕两个关键机制展开：

- **时间-视角指示令牌（TVI tokens）**：为视觉令牌动态注入时间位置编码和相机视角角度编码，使单一模型能够灵活处理不同具身形态的相机配置和可变时间跨度。
- **预算感知的时间采样策略（BATS）**：基于遗忘曲线的指数增长采样概率，在有限令牌预算内保留近期关键帧的同时维持历史覆盖，平衡推理效率与长程上下文建模。

NavFoM采用双分支架构（导航与问答），在大规模多样化导航数据（8M导航样本 + 4.76M QA样本）上端到端联合训练，共享视觉编码器（DINOv2 + SigLIP）和LLM（Qwen2-7B），预测连续路径点轨迹，无需针对特定任务微调。

### 主要结果

在多个基准上，NavFoM以零样本或多任务联合训练方式达到或超越此前最先进方法：

- **VLN-CE RxR**：多相机设置下成功率从56.3%提升至**64.4%**，单相机设置下从51.8%提升至**57.4%**（Table 1）。
- **HM3D-OVON目标搜索**：零样本条件下取得**45.2% SR**（四视图），超过此前微调的最佳方法（43.6% SR）（Table 7）。
- **EVT-Bench主动跟踪**：四视图下单目标跟踪SR达**88.4%**，超越TrackVLA（85.1%）（Table 8）。
- **自动驾驶规划**：在NAVSIM和nuScenes上性能与专门设计的SOTA方法（如DiffusionDrive）相当，展现出跨领域的竞争力（Table 9, 10）。

消融实验进一步证实：TVI令牌和BATS在历史令牌组织上显著优于均匀采样和手工令牌方案（Figure 8）；多任务联合训练在所有任务上带来一致的性能提升，低资源任务（如搜索、跟踪）获益最大（Figure 7）。

### 局限与展望

NavFoM仍面临若干挑战：小物体远距离识别困难、运动模糊导致感知失败；六相机以上配置下视点令牌增多会压缩历史帧编码容量，导致性能下降；在OpenUAV Unseen-Map等要求大规模探索的任务上表现不佳。未来方向包括自适应多视图令牌编码、更高效的探索策略，以及将更多运动自由度纳入统一框架。

具身导航是机器人学与计算机视觉交叉的核心问题，其目标是让智能体根据语言指令在未知环境中自主移动并完成任务。近年来，视觉-语言导航（VLN）、目标导航、主动视觉跟踪、无人机导航和自动驾驶等子领域各自取得了显著进展，但这些进展背后隐藏着一个深层瓶颈：**现有导航方法几乎全部受限于狭窄的任务设定和单一具身形态的专用架构**。

具体而言，当前研究存在以下结构性缺口：

**任务碎片化**。VLN方法（如**ETPNav**，An et al., 2024）专为指令跟随设计，目标导航方法（如**MT-SD**）聚焦于语义目标搜索，而视觉跟踪方法（如**TrackVLA**，Wang et al., 2025c）则针对移动目标追踪。这些方法在各自任务上表现良好，但彼此之间无法迁移——一个VLN模型无法执行目标搜索，反之亦然。这种碎片化迫使研究者和工程师为每个新任务从头训练专用模型，造成数据、算力和工程资源的巨大浪费。

**形态绑定**。现有方法的架构深度耦合于特定具身形态的相机配置。例如，地面机器人的导航模型通常假定单目或双目前视相机，而无人机导航方法（如**TravelUAV**）则依赖四视图全景输入。自动驾驶规划方法（如**DiffusionDrive**，Liao et al., 2024a）进一步要求六视图或八视图环视相机。当相机数量、安装角度或视野范围发生变化时，模型通常需要重新设计或重新训练，无法实现即插即用的跨形态泛化。

**时间上下文处理的局限性**。导航本质上是一个序贯决策问题，历史观测对当前决策至关重要。然而，现有方法处理时间上下文的方式极为粗糙：要么简单拼接最近几帧的特征，要么采用固定间隔的均匀采样。这些策略忽视了人类遗忘曲线的认知特性——近期信息应被更密集地保留，而远期信息可以稀疏采样但仍需维持覆盖。更重要的是，当相机数量增加时，多视角信息与历史帧信息在令牌预算上形成竞争，简单方法无法有效权衡。

**训练范式的封闭性**。现有模型几乎全部采用单任务独立训练范式，忽视了不同导航任务之间潜在的共享知识结构。例如，指令跟随中的语言理解能力、目标搜索中的视觉语义匹配能力、以及视觉跟踪中的运动预测能力，本质上都依赖于通用的视觉-语言对齐和时空推理。将这些任务割裂训练，不仅限制了每个任务的性能上限，更阻碍了通用导航智能的涌现。

上述瓶颈共同指向一个根本性问题：**能否构建一个统一的具身导航基础模型，使其在无需任何任务特定微调的前提下，同时胜任多种导航任务并泛化到不同具身形态？** 这一问题的回答不仅具有理论价值——探索通用导航智能的可能性，更具有实际意义——大幅降低多任务多形态机器人系统的开发成本。

本文正是围绕这一核心动机展开。我们提出**NavFoM（Embodied Navigation Foundation Model）**，旨在通过两个关键设计突破上述瓶颈：（1）**时间-视角指示令牌（TVI tokens）**，统一编码不同相机配置和可变时间跨度的观测信息；（2）**预算感知的时间采样策略（BATS）**，基于遗忘曲线在有限令牌预算内动态选择历史帧。在大规模多样化导航数据（12.7M样本，涵盖VLN、目标导航、视觉跟踪、无人机导航和自动驾驶）上联合训练后，NavFoM在多个基准上以零样本方式达到或超越此前微调的最佳方法，初步验证了通用导航基础模型的可行性。

## 核心方法与创新机理

NavFoM 的核心创新在于将具身导航从“单任务专用模型”推进到“跨任务、跨形态通用模型”，其关键突破可归结为三个相互耦合的 **changed slots**：

### 1. 时间-视角指示令牌（TVI Tokens）：统一多视角时序观测的令牌组织

传统方法对多相机输入采用简单拼接或独立编码，忽略了视角连续性与时间上下文。NavFoM 引入 **TVI 令牌**，为每个视觉令牌显式注入三类信息（公式见 Eq. 3）：

- **可学习基础嵌入** $\mathbf{E}_{\mathrm{Base}}$：承载帧的视觉语义；
- **正弦时间位置编码** $\mathcal{P}_{\mathrm{time}}(\mathrm{TimePE}(t))$：标记该帧在导航序列中的时间位置；
- **视角角度编码** $\mathcal{P}_{\mathrm{angle}}(\mathrm{AnglePE}(\phi))$：标记该帧来自哪个相机视角（以角度 $\phi$ 表示）。

这三者按任务灵活组合：导航任务同时使用时间编码和角度编码；视频问答仅使用时间编码；图像问答仅使用基础嵌入。消融实验（Figure 8 / Table 8）表明，TVI 令牌在所有令牌预算下均显著优于手工令牌（无位置编码）和仅使用时间位置编码的 HAMT 风格变体，验证了视角信息对多相机导航的关键作用。

**因果机制**：TVI 令牌使 LLM 能够在统一的令牌序列中区分“何时、从哪个视角”看到的观测，从而在单一模型中处理任意相机配置（1 至 6 相机）和可变时间跨度，无需针对特定形态重新设计输入格式。

### 2. 预算感知的时间采样（BATS）：在固定令牌预算下保留关键历史

导航任务的时间跨度可变（从几十步到数百步），将所有历史帧编码为视觉令牌会超出 LLM 的上下文窗口和推理预算。现有方法（如均匀采样）无法在令牌约束下有效保留近期关键帧和远期历史覆盖。NavFoM 提出 **BATS**，其核心机制为：

- **基于遗忘曲线的指数采样概率**：$P(t) = (1 - \epsilon) e^{k(t - T)/T} + \epsilon$（Eq. 4），其中 $T$ 为当前时刻，$k > 0$ 控制衰减速率，$\epsilon$ 为最低采样概率。该设计使近期帧以更高概率被采样，同时保证远期帧不被完全丢弃。
- **离线预算匹配**：通过期望帧数公式 $\mathbb{E}_{\mathrm{frames}} \approx (1 - \epsilon) \frac{1 - e^{-k}}{k} T + \epsilon T$（Eq. 5），预先计算 $k$ 以满足给定的令牌预算 $B$，无需在线调参。

消融实验（Figure 8 / Table 8）显示，BATS 在 2048 和 1024 令牌预算下均优于均匀采样策略；更重要的是，当令牌预算从 2048 降至 1024 时，BATS 的 nDTW 仅下降 1.4%，而均匀采样下降更为显著，证明 BATS 对预算变化具有鲁棒性。

**因果机制**：BATS 在固定计算预算内最大化历史信息的效用，使模型能处理长序列导航（如大范围搜索）而不牺牲推理速度（Figure 4c 显示 BATS 的推理时间开销可忽略）。

### 3. 多任务联合训练与连续轨迹动作空间：消除任务特定微调

传统导航方法为每个任务（VLN、目标导航、跟踪、自动驾驶）和每种形态训练独立模型。NavFoM 通过两个设计打破这一范式：

- **双分支架构与大规模联合训练**：导航分支和问答分支共享视觉编码器（DINOv2 + SigLIP）和 LLM（Qwen2-7B），在 8.02M 导航样本 + 4.76M QA 样本上端到端训练。多任务消融（Figure 7）表明，从单任务数据切换到 100% 混合数据后，所有任务均获得一致的性能提升，低资源任务获益最大（搜索 SR 从 10.3% 跃升至 45.2%），验证了跨任务知识迁移的有效性。

- **连续轨迹路径点预测**：替代传统的离散动作空间（FORWARD、LEFT、RIGHT、STOP），NavFoM 预测连续路径点轨迹 $\tau_T = \alpha_{\mathrm{task}} \cdot \mathcal{A}_{\theta}(E_T^{\mathrm{A}})$（Eq. 6），并通过任务特定的缩放因子 $\alpha_{\mathrm{task}}$ 适配不同形态的运动尺度（如地面机器人 vs 无人机 vs 自动驾驶车辆，见 Table 5）。该设计使模型在 VLN-CE 上无需依赖航点预测器即可取得 SOTA，并在 HM3D-OVON 上以零样本方式（45.2% SR）超越此前微调的 SOTA 方法（43.6% SR）。

**因果机制**：联合训练迫使模型学习跨任务共享的导航原语（如避障、路径跟踪），而连续轨迹预测解耦了动作表示与具体形态的运动学约束，使单一模型能泛化到未见过的任务和平台。

### 4. 视觉令牌粒度差异化：平衡细节与效率

NavFoM 对最新观测帧使用精细令牌（64 patches），对历史帧使用粗糙令牌（4 patches），通过 GridPool 操作实现（Eq. 2）。这一设计在保持当前环境细节感知的同时，大幅压缩历史信息的令牌开销，为 BATS 的预算管理提供基础。该策略与 TVI 令牌和 BATS 协同工作：粗糙历史令牌附加时间/视角编码后，仍能向 LLM 传递“过去在某个视角看到了什么”的粗粒度信息，而精细的当前令牌确保即时决策的准确性。

### 创新边界与已知局限

- **相机数量上限**：当相机数增至 6 时，视角令牌增多会压缩历史帧的编码容量，导致 VLN-CE RxR 性能轻微下降（Figure 14），表明 TVI 令牌的视角编码维度存在容量瓶颈。
- **损失权重固定**：导航损失权重 $\beta = 10$ 为固定值，在数据规模差异较大的任务间可能需要自适应调整（论文将此列为开放问题）。
- **训练成本高**：联合训练需 56 块 H100 GPU 运行 72 小时，对复现和扩展构成资源门槛。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_kkBOIsrCXh/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of NavFoM. Our method provides a unified framework for handling multiple tasks, including Image QA, Video QA, and Navigation. We organize text tokens and visual tokens using temporal-viewpoint indicator tokens (Sec. 2.1.1)*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_kkBOIsrCXh/figures/001_Figure_1.jpg]]
*Figure 1: Benchmark performance of NavFoM, we compare our method with SOTA baselines on each benchmarks. See Section 3 for more detials*

NavFoM 采用**双分支统一架构**，将导航任务与问答任务（图像QA、视频QA）纳入同一框架处理。其核心设计围绕一个关键瓶颈展开：如何让单一模型处理不同具身形态下可变的相机配置（单目至多目）和任意长度的时间跨度，同时将视觉令牌总量控制在推理可行的预算内。

### 输入组织与视觉编码

系统接收三类输入：**语言指令** $E_L$、**多视角视觉观测**（$N$ 个相机在 $T$ 个时间步上的图像序列），以及可选的问答文本。视觉编码采用双编码器并行提取特征——**DINOv2** 和 **SigLIP** 各自处理每帧图像，随后通过网格池化（Grid Pooling）将特征压缩为两种粒度：

$$ \mathbf{V}^{\mathrm{fine/coarse}} = \mathrm{GridPool}\left(\mathbf{V}, \frac{64}{P} \text{ 或 } \frac{4}{P}\right) $$

其中 $P$ 为原始补丁数。**最新帧**使用精细表示（64个令牌），以保留当前决策所需的细节；**历史帧**使用粗糙表示（4个令牌），在有限令牌预算内覆盖更长的时序上下文。这一粒度差异化设计是平衡感知精度与计算效率的关键机制。

### TVI令牌：注入时间与视角信息

视觉令牌本身不含时间或视角标识。为此，NavFoM 引入**时间-视角指示令牌**（Temporal-Viewpoint Indicator, TVI），为每个视觉令牌附加可学习的身份信息：

$$ \mathbf{E}_{\mathrm{TVI}} = \begin{cases} \mathbf{E}_{\mathrm{Base}} + \mathcal{P}_{\mathrm{time}}(\mathrm{TimePE}(t)) + \mathcal{P}_{\mathrm{angle}}(\mathrm{AnglePE}(\phi)), & \text{Navigation} \\ \mathbf{E}_{\mathrm{Base}} + \mathcal{P}_{\mathrm{time}}(\mathrm{TimePE}(t)), & \text{Video QA} \\ \mathbf{E}_{\mathrm{Base}}, & \text{Image QA} \end{cases} $$

TVI令牌由三部分组成：**可学习基嵌入** $\mathbf{E}_{\mathrm{Base}}$、**正弦时间位置编码** $\mathrm{TimePE}(t)$（经MLP投影 $\mathcal{P}_{\mathrm{time}}$），以及**视角角度编码** $\mathrm{AnglePE}(\phi)$（经MLP投影 $\mathcal{P}_{\mathrm{angle}}$）。根据任务类型灵活组合——导航任务需同时感知“何时”与“何处”，视频QA仅需时序信息，图像QA则无需额外标识。Figure 3 的聚类可视化证实，TVI令牌在嵌入空间中按视角和时间步形成清晰的可分结构，表明这些信息被有效编码。

### BATS：预算感知的时间采样

当导航序列变长，即使使用粗糙历史令牌，总令牌数仍可能超出LLM的上下文窗口或推理延迟约束。NavFoM 提出**预算感知的时间采样**（Budget-Aware Temporal Sampling, BATS），基于遗忘曲线设计指数增长的采样概率：

$$ P(t) = (1 - \epsilon) e^{k(t - T)/T} + \epsilon, \quad k > 0 $$

其中 $T$ 为当前时间步，$\epsilon$ 为最低采样概率下界，$k$ 控制衰减速率。该策略优先保留近期帧（高采样概率），同时以递减概率覆盖远期历史，避免完全丢失早期上下文。给定令牌预算 $B$，可通过期望帧数公式离线求解 $k$：

$$ \mathbb{E}_{\mathrm{frames}} \approx \int_0^T P(t) dt = (1 - \epsilon) \frac{1 - e^{-k}}{k} T + \epsilon T $$

消融实验（Table 8）表明，BATS在2048和1024令牌预算下均优于均匀采样策略，且预算从2048降至1024时nDTW仅下降1.4%，展现出对令牌压缩的鲁棒性。

### 动作预测与轨迹解码

经TVI令牌组织和BATS采样后，所有视觉令牌与语言令牌拼接送入**LLM（Qwen2-7B）**，预测动作隐藏状态 $E_T^A$：

$$ E_T^A = \mathrm{LLM}(E_{1:T}^{1:N}, E_L) $$

随后由**三层MLP动作解码器** $\mathcal{A}_{\theta}$ 将其映射为连续的路径点轨迹，并按任务特定的缩放因子 $\alpha_{\mathrm{task}}$ 反归一化：

$$ \tau_T = \{\mathbf{a}_1, ..., \mathbf{a}_M\}_T = \alpha_{\mathrm{task}} \cdot \mathcal{A}_{\theta}(E_T^A) $$

这一连续轨迹预测方案取代了传统的离散动作空间（如前进、转向、停止），使单一动作头能适配不同运动尺度的具身形态（从室内机器人到无人机到自动驾驶车辆），各形态的缩放因子详见 Table 5。

### 训练范式

总损失为导航损失与问答损失的加权和：

$$ L = \beta L_{\mathrm{nav}} + L_{\mathrm{QA}} $$

其中 $\beta = 10$ 为固定缩放因子。模型在约1270万样本（802万导航、315万图像QA、161万视频QA）上联合训练，视觉编码器和LLM均从预训练权重初始化，使用56块H100 GPU训练72小时。多任务联合训练的消融实验（Figure 7）显示，从50%到100%数据混合比例，所有导航子任务均获得一致的性能提升，其中低资源任务（如搜索）获益最为显著——搜索成功率从10.3%跃升至45.2%。

NavFoM 采用双分支架构，统一处理导航与问答任务。其核心设计围绕三个关键模块展开：视觉令牌组织、时间-视角指示嵌入，以及预算感知的时间采样。

### 视觉编码与令牌粒度

模型使用 DINOv2 和 SigLIP 双视觉编码器从多视角图像中提取特征。为平衡细节保留与计算效率，NavFoM 对不同时间步的视觉令牌采用差异化粒度：最新帧使用精细令牌（64 个补丁），历史帧使用粗糙令牌（4 个补丁），通过网格池化实现降维：

$$ \mathbf{V}^{\mathrm{fine/coarse}} = \mathrm{GridPool}\left(\mathbf{V}, \frac{64}{P} \text{ 或 } \frac{4}{P}\right) $$

其中 $P$ 为原始补丁数量。精细令牌保留当前观察的空间细节，粗糙令牌则以低计算成本维持历史上下文。

### 时间-视角指示令牌（TVI Tokens）

TVI 令牌是跨任务、跨形态泛化的关键设计。每个视觉令牌被附加一个指示嵌入，根据任务类型组合三类信息：可学习基础嵌入 $\mathbf{E}_{\mathrm{Base}}$、正弦时间位置编码 $\mathrm{TimePE}(t)$、以及视角角度编码 $\mathrm{AnglePE}(\phi)$：

$$ \mathbf{E}_{\mathrm{TVI}} = \begin{cases} \mathbf{E}_{\mathrm{Base}} + \mathcal{P}_{\mathrm{time}}(\mathrm{TimePE}(t)) + \mathcal{P}_{\mathrm{angle}}(\mathrm{AnglePE}(\phi)), & \text{Navigation} \\ \mathbf{E}_{\mathrm{Base}} + \mathcal{P}_{\mathrm{time}}(\mathrm{TimePE}(t)), & \text{Video QA} \\ \mathbf{E}_{\mathrm{Base}}, & \text{Image QA} \end{cases} $$

其中 $\mathcal{P}_{\mathrm{time}}$ 和 $\mathcal{P}_{\mathrm{angle}}$ 为可学习的投影层。导航任务同时注入时间与视角信息，使模型能区分不同相机朝向和时间步的观察；视频问答仅需时间上下文；图像问答仅使用基础嵌入。消融实验证实，完整的 TVI 令牌（含时间/角度编码）在所有令牌预算下均显著优于手工令牌或无位置编码的变体（Figure 8 / Table 8）。

### 预算感知的时间采样（BATS）

为在有限令牌预算内高效利用历史帧，BATS 采用基于遗忘曲线的指数增长采样概率：

$$ P(t) = (1 - \epsilon) e^{k(t - T)/T} + \epsilon, \quad k > 0 $$

其中 $T$ 为当前时间步，$t$ 为历史时间步，$\epsilon$ 为最低采样概率下界，$k$ 控制遗忘速率。该设计使近期帧被高概率保留，同时以递减概率覆盖远期历史，避免完全丢弃早期信息。

给定令牌预算 $B$，期望采样帧数通过积分近似计算：

$$ \mathbb{E}_{\mathrm{frames}} \approx \int_0^T P(t) dt = (1 - \epsilon) \frac{1 - e^{-k}}{k} T + \epsilon T $$

离线求解 $k$ 以满足 $\mathbb{E}_{\mathrm{frames}}$ 对应的令牌总数不超过 $B$。消融实验表明，BATS 在 2048 和 1024 令牌预算下均优于均匀采样，且预算从 2048 降至 1024 时 nDTW 仅下降 1.4%，展现出良好的预算鲁棒性（Figure 8 / Table 8）。

### 动作预测与轨迹解码

LLM（Qwen2-7B）接收组织后的视觉令牌和语言令牌，预测动作隐藏状态：

$$ E_T^A = \mathrm{LLM}\left(E_{1:T}^{1:N}, E_L\right) $$

随后由 3 层 MLP 的动作解码器将其映射为连续轨迹路径点：

$$ \tau_T = \{\mathbf{a}_1, ..., \mathbf{a}_M\}_T = \alpha_{\mathrm{task}} \cdot \mathcal{A}_{\theta}\left(E_T^{\mathrm{A}}\right) $$

每个路径点包含 $(x, y, z, \theta)$，$\alpha_{\mathrm{task}}$ 为任务相关的缩放因子，用于将归一化预测反归一化到不同具身形态的实际运动空间（如地面机器人、无人机、自动驾驶车辆）。不同具身形态的缩放因子配置见 Table 5。

## 实验与关键发现

### 主结果

NavFoM在视觉语言导航（VLN）、目标导航、主动跟踪、自动驾驶和无人机导航等五个差异化基准上进行了全面评估。模型在**未针对任何特定相机配置进行微调**的前提下，在所有任务上均达到或超越了此前最先进方法的性能。

**视觉语言导航（VLN-CE）**：在RxR基准上，多相机配置下NavFoM的成功率（SR）从ETPNav的56.3%提升至**64.4%**（+8.1个百分点）；单相机配置下从51.8%提升至**57.4%**（+5.6个百分点），同时SPL和nDTW也达到最优水平（表1）。值得注意的是，NavFoM仅使用RGB图像和语言指令，未依赖深度信息或里程计，而ETPNav等方法使用了这些额外信号。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_kkBOIsrCXh/figures/008_Table_1.jpg]]
*Table 1: Comparison on VLN-CE in Single-View and Multi-View Settings. Here, S.RGB and M.RGB denote single-view and multi-view configurations, respectively. The symbol ∗ indicates methods that utilize the waypoint predictor from (Hong et al., 2022)*

**目标导航与搜索（HM3D-OVON）**：在零样本条件下，四视图NavFoM取得**45.2% SR**，超过了此前经过微调的最优方法MT-SD（43.6% SR）（表7）。从单视图到四视图的切换并未带来性能下降（64.9% vs 62.5% SR），表明TVI令牌有效编码了多视角信息。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_kkBOIsrCXh/figures/025_Table_7.jpg]]
*Table 7: Object goal navigation. Comparison on HM3D-OVON Yokoyama et al. (2024b). ∗ : denotes zeroshot evaluation. We report the performence of our method on egocentric and four-view settings. The best and the second best results are denoted by bold and underline*

**主动视觉跟踪（EVT-Bench）**：四视图NavFoM在单目标跟踪上取得**88.4% SR**，超越了TrackVLA（85.1% SR）等专用方法（表8）。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_kkBOIsrCXh/figures/026_Table_8.jpg]]
*Table 8: Performance on EVT-Bench. †: Uses GroundingDINO (Liu et al., 2023b) as the open-vocabulary detector. ‡: Uses SoM (Yang et al., 2023)+GPT-4o (OpenAI, 2024) as the visual foundation model. The best and the second best results are denoted by bold and underline*

**自动驾驶规划**：在NAVSIM闭环规划基准上，NavFoM取得**84.3 PDMS**，与专门设计的DiffusionDrive（88.1 PDMS）等SOTA方法性能相当（表9）。在nuScenes开环规划中，NavFoM的L2平均误差为**0.42**，碰撞率为**0.12**，与最优方法差距有限（表10）。需注意，NavFoM未显式建模车道线、交通标志等驾驶要素，仍有较大提升空间。

**无人机导航（OpenUAV）**：四视图NavFoM在Seen、Unseen Object和Unseen Map三个测试集上均取得最优或次优结果（表6），展示了跨形态泛化能力。但在Unseen-Map上所有方法表现均不佳，表明大规模探索能力仍是开放问题。

### 消融实验

**TVI令牌与历史帧组织策略**：在VLN-CE RxR基准上，TVI令牌（含时间和角度位置编码）在所有令牌预算下均显著优于手工令牌（Equ.3 w.o P_angle/time）和无位置编码变体。在2048令牌预算下，TVI令牌取得**65.8 nDTW / 56.2 SR**，而手工令牌仅为60.2 nDTW / 49.8 SR（图8/表8）。图3的聚类可视化进一步证实，TVI令牌的嵌入空间能按视角和时间步自然分离，验证了其编码的有效性。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_kkBOIsrCXh/figures/014_Figure_8.jpg]]
*Figure 8: Ablation Study on History Token Organization Strategies and Identity Tokens. Uniform sampling is adopted Go Straight\<vehicle state information>Trurn Left\<vehicle state information>from (Cheng et al., 2025). †Positional embeddings is adopted from HAMT (Chen et al., 2021b)*

**BATS采样策略**：BATS在2048和1024令牌预算下均优于均匀采样策略。更重要的是，当令牌预算从2048降至1024时，BATS的nDTW仅下降**1.4%**（65.8→64.4），而均匀采样下降更为显著（图8/表8）。图4展示了BATS基于遗忘曲线的指数采样概率分布：近期帧采样概率高，远期帧概率低但保持非零覆盖，从而在有限预算内平衡了细节保留与历史覆盖。

**多任务联合训练**：图7的消融实验表明，从单任务数据到混合50%其他任务数据再到混合100%其他任务数据，所有任务的性能均持续提升。其中低资源任务获益最为显著——**搜索任务从10.3% SR跃升至45.2% SR**，跟踪和驾驶任务也有明显提升。这验证了大规模多样化导航数据联合训练的核心假设。

**相机数量影响**：图14显示，相机数量从1增至4时，VLN-CE RxR性能持续提升（SR: 57.4→64.4），但增至6相机时性能轻微下降。原因在于固定令牌预算（B=2048）下，更多视点令牌压缩了历史帧的编码容量，揭示了多视图编码中的信息压缩瓶颈。

**视觉令牌粒度**：最新帧使用精细令牌（64 patch）、历史帧使用粗糙令牌（4 patch）的设计，在保持细节感知的同时控制了总令牌数，是模型能处理长时序导航的关键效率设计。

### 失败模式与局限

1. **感知瓶颈**：小物体远距离识别困难和机器人运动模糊导致部分真实世界任务失败，限制了零样本部署的可靠性。
2. **极端场景退化**：超长指令（数千词）和大范围搜索（数百平方米）对模型的理解与探索能力提出严峻挑战，OpenUAV Unseen-Map上所有方法表现均不佳。
3. **多相机容量冲突**：六相机及以上配置下，视点令牌增多会压缩历史帧编码容量，导致性能反而下降（图14）。
4. **损失权重固定**：导航损失权重β固定为10，缺乏自适应调整机制，可能影响不同任务间的收敛平衡。
5. **计算资源需求高**：训练需56块H100 GPU运行72小时（约4032 GPU小时），对数据量和算力要求较高。
6. **驾驶场景未充分建模**：未显式建模车道线、交通标志等驾驶要素，在自动驾驶基准上与专用SOTA方法仍有差距。

## 定位与知识库关联

### 1. 与现有方法的谱系关系

NavFoM 的核心贡献在于将导航从“单一任务专用模型”推进到“跨任务、跨形态通用模型”，其方法谱系可沿三条轴线定位。

**（1）视觉语言导航（VLN）的演进。** 传统 VLN 方法依赖离散动作空间（FORWARD、LEFT、RIGHT、STOP）和特定相机配置，代表性工作如 **ETPNav**（An et al., 2024）在 VLN-CE RxR 多相机设置下达到 56.3% SR，但其架构深度耦合于 VLN 任务。NavFoM 以连续轨迹预测替代离散动作，并通过 TVI 令牌统一处理单/多相机输入，在相同基准上提升至 64.4% SR（+8.1 个百分点），且无需针对相机配置微调。这一跨越表明，通用令牌组织策略可以替代任务专用的感知编码设计。

**（2）跨任务导航的统一尝试。** **Uni-NaVid**（Zhang et al., 2025a）是少有的跨任务导航基线，但其零样本搜索和跟踪性能有限。NavFoM 通过多任务联合训练（8M 导航样本 + 4.76M QA 样本）实现知识迁移：在 HM3D-OVON 上以零样本 45.2% SR 超过此前微调的最佳方法（43.6% SR）；在 EVT-Bench 单目标跟踪上达到 88.4% SR，超过专用跟踪模型 **TrackVLA**（Wang et al., 2025c）的 85.1% SR。因果机制在于：共享视觉编码器和 LLM 使低资源任务（搜索、跟踪）从高资源任务（VLN）中获益，消融实验显示搜索任务 SR 从 10.3% 跃升至 45.2%（Figure 7）。

**（3）自动驾驶规划的跨域泛化。** NavFoM 在 NAVSIM 和 nuScenes 上与专用规划器竞争：**DiffusionDrive**（Liao et al., 2024a）在 NAVSIM 上以 88.1 PDMS 领先，NavFoM 以 84.3 PDMS 紧随其后；在 nuScenes 开环规划中，NavFoM 的 L2 误差（0.42）和碰撞率（0.12）与最佳方法相当。值得注意的是，NavFoM 未显式建模车道线、交通标志等驾驶要素，其竞争力来源于通用视觉-语言对齐能力，这暗示大规模跨域预训练可以部分弥补领域专用设计的缺失。

**（4）无人机导航的初步探索。** 在 OpenUAV 基准上，NavFoM 的性能与专用方法 **TravelUAV** 相比存在差距，尤其在 Unseen-Map 分裂上表现不佳。这揭示了当前方法的适用边界：当任务要求大规模探索和长距离规划时，通用模型缺乏有效的探索策略和空间记忆机制。

### 2. 核心设计决策的适用范围与边界

**TVI 令牌的适用条件。** TVI 令牌通过可学习基础嵌入、正弦时间编码和视角角度编码的组合，显式建模时空-视角信息。这一设计在以下条件下有效：
- **相机配置变化**：从单目到四目，性能持续提升（VLN-CE RxR SR: 57.4% → 64.4%），因为角度编码为模型提供了区分视角的信号。
- **任务类型切换**：导航任务使用完整的三组件组合，视频 QA 仅用时间和基础嵌入，图像 QA 仅用基础嵌入，这种灵活组合避免了任务间的信息干扰。

**TVI 令牌的失效边界。** 当相机数量增至六目时，性能出现轻微下降（Figure 14）。失效机制在于：多视角令牌数量线性增长，在固定令牌预算（B=2048）下挤占了历史帧的编码容量，BATS 采样被迫丢弃更多历史信息。这是 TVI 令牌设计的固有张力——视角覆盖与时间深度的零和博弈。

**BATS 采样的适用条件。** BATS 基于遗忘曲线的指数采样策略在以下场景有效：
- **令牌预算受限**：在 2048 和 1024 令牌预算下均优于均匀采样，且预算减半时性能下降更小（nDTW 仅降 1.4%），表明其优先保留近期关键帧的策略合理。
- **推理延迟敏感**：BATS 将推理时间控制在约 218ms/步（5 Hz），满足实时导航需求。

**BATS 的局限。** 遗忘曲线的衰减速率 k 和下限 ε 为固定超参数，未根据任务的时间跨度动态调整。在超长指令（数千词）或大范围搜索（数百平方米）场景中，固定参数可能导致历史信息过早丢失。

### 3. 已知局限与失败模式

**感知瓶颈。** 真实世界实验中，小物体远距离识别和运动模糊是主要失败原因。这是因为 NavFoM 仅使用 RGB 图像（无深度信息），且视觉编码器（DINOv2 + SigLIP）的分辨率有限，在细粒度识别任务中不足。在依赖深度或里程计的基线（如 ETPNav）面前，这一局限被部分掩盖，但在需要精确避障的场景中会暴露。

**探索能力不足。** 在 OpenUAV Unseen-Map 和 HM3D-OVON 的大范围搜索中，NavFoM 的性能显著下降。根本原因在于模型缺乏显式的空间记忆和探索策略——LLM 仅从历史令牌中隐式学习空间关系，缺乏结构化的地图构建或 frontier-based 探索机制。

**相机扩展的边际递减。** 如前述，六相机配置下的性能下降表明，当前令牌组织策略无法线性扩展至更多视角。可能的改进方向包括：视角间的信息压缩、自适应令牌分配，或引入视角选择机制。

**训练成本。** 56 块 H100 GPU × 72 小时（4032 GPU 小时）的训练代价限制了快速迭代和社区复现。损失加权因子 β=10 为固定值，未根据数据规模或训练阶段自适应调整，可能导致收敛次优。

### 4. 开放问题

1. **自适应多视角令牌编码**：如何设计动态的令牌分配策略，使相机数量增加时历史信息不被过度压缩？可能的思路包括视角重要性加权或基于注意力的视角选择。

2. **自动驾驶的语义增强**：引入场景描述（车道线、交通标志、行人意图）作为提示词，能否弥补 NavFoM 与专用规划器（如 DiffusionDrive）之间的性能差距？

3. **损失加权的自适应策略**：β 因子如何根据数据规模、任务难度或训练阶段动态调整？多任务学习中不同任务的收敛速度差异显著，固定权重可能导致某些任务欠拟合。

4. **大规模探索的突破路径**：在 OpenUAV Unseen-Map 等任务中，如何结合结构化地图构建或外部记忆模块，提升长距离导航的探索效率？

5. **感知鲁棒性提升**：针对小物体和运动模糊，是否可以通过多尺度视觉特征、时序融合或引入深度估计来增强感知？这需要在通用性和任务专用性之间寻找新的平衡点。

6. **运动自由度的扩展**：当前框架假设相机配置为固定视角，能否将无人机俯仰角等额外自由度纳入统一的相机配置框架，使模型适应更广泛的具身形态？

## 原文 PDF

![[paperPDFs/ICLR_2026/Embodied_Navigation_Foundation_Model.pdf]]
