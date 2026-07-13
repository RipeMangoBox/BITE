---
title: "WAM-Flow: Parallel Coarse-to-Fine Motion Planning via Discrete Flow Matching for Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/WAM_Flow_Parallel_Coarse_to_Fine_Motion_Planning_via_Discrete_Flow_Matching_for_Autonomous_Driving.pdf
project_link: null
code_link: "https://github.com/fudan-generative-vision/WAM-Flow"
aliases:
- WF
- WAM-Flow
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将规划任务建模为离散流匹配，通过并行双向去噪实现粗到细控制；引入度量对齐数值分词器保持标量几何结构；利用仿真引导 GRPO 对齐安全和性能目标。
primary_logic: 离散流匹配赋予 VLA 并行粗到细规划能力，度量对齐分词器将数值距离注入嵌入空间，GRPO 强化闭环安全性和驾乘舒适度，三者协调整体提升规划效果。
claims:
- WAM-Flow 在 NAVSIM-v1 上取得最低 90.3 PDMS，超越所有自回归和扩散基线。
- 在 NAVSIM-v2 上取得 84.7 EPDMS，同时在 NC、DDC、LK 等子指标领先。
- 消融实验证明度量对齐分词器、VQA 预训练和 GRPO 各自带来显著 PDMS 增益。
- NAVSIM-v1 上 PDMS = 90.3 (5-step)
---

# WAM-Flow: Parallel Coarse-to-Fine Motion Planning via Discrete Flow Matching for Autonomous Driving

> [!tip] 核心洞察
> 离散流匹配赋予 VLA 并行粗到细规划能力，度量对齐分词器将数值距离注入嵌入空间，GRPO 强化闭环安全性和驾乘舒适度，三者协调整体提升规划效果。

| 字段 | 内容 |
|------|------|
| 中文题名 | WAM-Flow：基于离散流匹配的并行粗到细运动规划用于自动驾驶 |
| 英文题名 | WAM-Flow: Parallel Coarse-to-Fine Motion Planning via Discrete Flow Matching for Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.06112) · [Code](https://github.com/fudan-generative-vision/WAM-Flow) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | WAM-Flow |
| Dataset | NAVSIM-v1, NAVSIM-v2, nuScenes |

> [!tip] 效果简介
> - NAVSIM-v1 上，PDMS 90.3 (5-step) vs 89.6 (ReCogDrive) / 89.1 (1-step of WAM-Flow) (+0.7 (over ReCogDrive) / +1.2 (5-step vs 1-step))。
> - NAVSIM-v2 上，EPDMS 84.7 vs 未提供最高基线，但论文声称超越其他方法 (N/A)。
> - nuScenes (碰撞率) 上，平均碰撞率 % (UniAD 指标) 0.23% vs 0.29% (DME-Driver) 或 0.31% (AutoVLA) (-0.06% ~ -0.08%)。

## 概要

自动驾驶中的视觉-语言-动作（VLA）模型长期受困于自回归解码带来的速度慢、曝光偏差以及数值标记缺乏几何保真度等问题，难以在推理效率与规划精度之间实现灵活权衡，更无法可靠保障闭环安全。**WAM-Flow** 将自车轨迹规划重新建模为结构化 token 空间上的**离散流匹配**（discrete flow matching）问题，通过并行双向去噪实现粗到细的轨迹生成，从根本上摆脱了因果注意力的序列依赖。

方法的核心设计由三个协同组件驱动：**度量对齐数值分词器**将连续标量离散化并保持几何距离，**离散流匹配去噪头**赋予模型可调节的计算-精度权衡，**仿真引导 GRPO** 则通过复合奖励（安全×性能）将模型行为对齐到闭环驾驶目标。三者共同作用，使 WAM-Flow 在 NAVSIM-v1 上以 1 步去噪取得 89.1 PDMS，5 步精炼达到最高的 **90.3 PDMS**，超越所有自回归和扩散基线；在 NAVSIM-v2 上取得 84.7 EPDMS，并在 nuScenes 端到端规划中创下最低平均碰撞率（0.23%）。消融实验证实，度量对齐分词器、VQA 预训练和 GRPO 各自带来显著的 PDMS 增益（+4.9、+3.3、+3.6 点）。

WAM-Flow 的并行粗到细范式为 VLA 规划提供了一种兼顾效率与安全的新路径，但其评估仍以仿真为主，Sim-to-Real 的泛化、多模态传感器融合以及长尾场景覆盖仍是后续研究需要解决的关键问题。



### 端到端自动驾驶的范式演进

端到端自动驾驶旨在将传感器输入直接映射为车辆控制信号或未来轨迹，从而绕过传统模块化管线中的信息瓶颈。近年来，视觉-语言-动作（VLA）模型在该领域展现出显著潜力——它们利用大规模预训练的多模态骨干网络，将驾驶场景编码为统一表示，再解码出可执行的动作序列。然而，现有 VLA 规划器在解码策略上几乎清一色采用**自回归生成范式**：逐 token 预测未来轨迹坐标，每个 token 的生成依赖于前序 token，形成严格的因果依赖链。

### 自回归 VLA 的三重困境

这种自回归解码在自动驾驶场景中暴露出三个结构性缺陷：

1. **推理延迟与不可并行性**：因果注意力机制迫使模型串行生成所有轨迹点，限制了实时部署中的吞吐量。在需要快速响应的动态交通场景中，这一瓶颈尤为突出。

2. **曝光偏差**：训练时使用真实轨迹 token 作为上下文（teacher forcing），推理时却依赖模型自身生成的 token，这种分布偏移会在长序列预测中累积误差，导致轨迹末端漂移甚至碰撞。

3. **数值标记的几何失真**：现有 VLA 方法通常复用通用视觉-语言模型（如 Janus）的文本分词器来处理连续标量坐标。文本分词器的嵌入空间针对语义相似性优化，而非数值距离——两个在欧氏空间中接近的坐标值可能被映射到嵌入空间中相距甚远的 token，破坏了轨迹规划的几何保真度。

此外，自回归范式天然缺乏**计算-精度权衡**的灵活性：无论场景简单还是复杂，模型都必须执行完整的串行解码，无法在“快速粗略规划”与“精细迭代优化”之间动态切换。

### 扩散模型的启示与局限

为突破自回归的约束，部分工作转向扩散模型进行轨迹生成。**DiffusionDrive** 和 **Artemis** 等方法将规划建模为连续空间中的去噪扩散过程，实现了并行解码和一定程度的粗到细优化。然而，这些方法在离散 token 空间中的适配性有限，难以直接融入 VLA 框架中已有的多模态 token 表示，且缺乏与仿真器闭环反馈的有效对齐机制。

### 核心动机：离散流匹配 + 度量感知 + 闭环对齐

上述分析揭示了三个关键突破口：

- **生成范式**：需要一种既能并行解码、又能自然融入离散 token 空间的生成框架，替代自回归的因果依赖。
- **数值表示**：需要一种保持标量几何结构的数值分词器，使嵌入空间的距离关系与物理坐标的欧氏距离保持一致。
- **训练目标**：需要超越单纯的行为克隆（对数似然最大化），引入闭环仿真反馈来显式优化安全性和驾乘质量。

WAM-Flow 正是围绕这三个维度展开：将规划任务建模为**离散流匹配**问题，实现全并行双向去噪；设计**度量对齐数值分词器**，通过三重态排序损失将数值距离注入嵌入空间；采用**仿真引导 GRPO** 强化学习，在行为克隆的基础上进一步对齐安全、进度和舒适度目标。三者协同，构成了从“生成什么”到“如何生成”再到“为何这样生成”的完整闭环。



## 核心方法与创新机理

WAM-Flow 围绕“将 VLA 规划从自回归解码迁移到并行粗到细生成”这一主线，在三个关键维度上对现有范式进行了系统性改造：

**1. 生成范式：自回归逐 token 解码 → 并行双向去噪离散流匹配**

传统自回归 VLA（如 **DrivingGPT**、**FSDrive**、**AutoVLA**）依赖因果注意力逐 token 生成轨迹坐标，存在推理速度慢、曝光偏差累积以及数值标记缺乏几何保真度三重瓶颈。WAM-Flow 将运动规划重新建模为结构化 token 空间上的**离散流匹配**问题：模型不再从左到右生成，而是通过非因果的双向去噪一次性更新所有坐标 token，天然支持粗到细的迭代精炼。具体而言，1 步去噪即可获得有竞争力的结果（NAVSIM-v1 PDMS 89.1），5 步精炼进一步提升至 90.3，同时 1 步推理速度达到 **ReCogDrive** 的 4.67 倍，实现了灵活的计算-精度权衡。这一范式转换的数学基础是将规划目标视为连续时间马尔可夫链（CTMC）的后验估计问题，通过条件速率 $u_t(x, z | x_1)$ 驱动状态向目标靠近，训练目标为流匹配交叉熵损失 $\mathcal{L}_{\mathrm{CE}}(\theta)$。

**2. 数值表示：标准文本分词器 → 度量对齐数值分词器**

自回归 VLA 通常复用通用文本分词器处理连续标量坐标（如 Janus-1.5B 的文本 tokenizer），这破坏了数值间的几何距离结构。WAM-Flow 设计了一个**度量对齐数值分词器**，将连续标量均匀离散化到 $[-100, 100]$ 区间上的 20,001 个 token，并通过三重态排序损失 $\mathcal{L}_{\mathrm{num}}$ 强制嵌入空间中的距离保持与原始标量差值一致的单调性。消融实验表明，仅将文本分词器替换为专用数值分词器就带来 **+4.9 PDMS** 的显著增益（76.2 → 81.1），进一步引入度量对齐嵌入再贡献 **+2.3 PDMS**（81.1 → 83.4），验证了“将数值距离注入嵌入空间”这一设计的有效性。

**3. 训练目标：纯监督行为克隆 → 监督流匹配 + 仿真引导 GRPO 对齐**

现有方法大多仅依赖对数似然（行为克隆）进行监督训练，无法直接优化闭环安全性和驾乘质量。WAM-Flow 在监督流匹配预训练后，引入**仿真引导 GRPO** 进行强化对齐：利用 NAVSIM 仿真器提供复合奖励 $R(\tau)$，其中安全项（碰撞、可行驶区域）以连乘形式施加硬约束，性能项（进度、TTC、舒适度）以加权求和形式引导优化。GRPO 采用组相对策略优化目标，通过裁剪和 KL 正则稳定更新，避免策略崩溃。消融显示，大规模 VQA 预训练贡献 **+3.3 PDMS**（83.4 → 86.7），仿真引导 GRPO 最终将 PDMS 推至最高的 90.3（**+3.6 PDMS**），且最优奖励权重配置为 EP:TTC:Comfort = 5:5:2，最优 GRPO 组大小为 3。

三项创新的协同关系清晰：离散流匹配赋予模型并行粗到细的生成能力，度量对齐分词器保证数值标记的几何保真度，GRPO 将开环模仿学习与闭环安全需求对齐——三者缺一不可，共同支撑了 WAM-Flow 在 NAVSIM-v1（PDMS 90.3）、NAVSIM-v2（EPDMS 84.7）和 nuScenes（平均碰撞率 0.23%）上的全面领先。



WAM-Flow 将自车轨迹规划重新定义为**离散流匹配（Discrete Flow Matching, DFM）** 问题，构建了一个视觉-语言-动作（VLA）模型，以**并行、双向去噪**替代传统自回归模型的逐 token 因果解码。整体流程如 Figure 2 所示，系统接收三种模态输入，输出覆盖未来 4 秒的 8 个路径点（waypoint）轨迹。

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/003_Figure_2.jpg]]
*Figure 2: Architecture of the proposed WAM-Flow framework. Our method takes as input a front-view image, a natural-language navigation command with a system prompt, and the ego-vehicle states, and outputs an 8-waypoint future trajectory spanning 4 seconds through parallel denoising. The model is first trained via supervised fine-tuning to learn accurate trajectory prediction. We then apply simulatorguided GRPO to further optimize closed-loop behavior. The GRPO reward function integrates safety constraints (collision avoidance, drivable-area compliance) with performance objectives (ego-progress, time-to-collision, comfort)*

### 输入与输出

**输入端**包含三个信息源：
- **前视单目图像**：经 SigLIP 编码为 576 个视觉 token，再通过轻量 MLP 投影到 Janus-1.5B 的 2048 维文本 token 空间；
- **自然语言导航指令**：附带系统提示，描述驾驶意图（如“直行通过路口后右转”）；
- **自车状态**：当前位置、航向角、速度和加速度。

**输出端**为 8 个路径点的序列，每个路径点由 $(x, y, \theta)$ 三元组表征，共同构成 4 秒时间跨度内的规划轨迹。

### 核心模块与数据流

整个 pipeline 由以下关键模块串联而成：

1. **视觉编码与对齐**  
   SigLIP 将 $384\times 384$ 的前视图像编码为视觉 token 序列，MLP 适配器将其对齐到语言嵌入空间，使视觉特征与文本指令在同一表示空间中融合。

2. **度量对齐数值分词器（Metric-Aligned Numerical Tokenizer）**  
   连续标量坐标被离散化到 $[-100, 100]$ 区间上的 20,001 个 token，并通过**三重态排序损失**（Eq. 5）训练嵌入层，确保 token 间距保持与原始标量差值一致的几何单调性。这解决了标准文本分词器无法保留数值几何结构的瓶颈。

3. **Janus 多模态骨干（非因果）**  
   作为流匹配的**条件后验估计器**，Janus-1.5B 接收融合后的视觉 token、导航指令 token 和自车状态 token，在扩展后的词表上预测目标路径点 token 的离散后验分布 $p_{1|t}^\theta$。模型采用非因果注意力，使所有坐标 token 可同时双向交互。

4. **离散流匹配去噪头**  
   基于条件速率 $u_t(x, z|x_1)$（Eq. 7），从噪声分布出发并行更新所有坐标 token。通过调节去噪步数（1 步至 5 步），实现**粗到细（coarse-to-fine）** 的轨迹生成：简单场景 1 步即可获得可接受结果，复杂场景 5 步逐步细化。

5. **仿真引导 GRPO 对齐模块**  
   在监督流匹配训练后，引入 NAVSIM 仿真器提供的复合奖励函数（Eq. 9）——安全项连乘（碰撞 × 可行驶区域），性能项加权求和（进度、TTC、舒适度）——通过 GRPO 目标（Eq. 10）更新策略，强化闭环安全性和驾乘舒适度。

### 训练课程

模型训练遵循**四阶段课程**（Figure 3）：
1. **数值嵌入预训练**：仅训练度量对齐分词器的嵌入层；
2. **大规模 VQA 预训练**：在 650 万视觉问答数据上预训练 Janus 骨干，注入通用视觉-语言对齐能力；
3. **监督微调（SFT）**：在规划数据上用流匹配交叉熵损失（Eq. 8）进行行为克隆；
4. **仿真引导 GRPO**：在仿真器闭环反馈下进行策略优化，对齐安全与性能目标。

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the full training curriculum. Different training stage motivation and corresponding training data and training steps are demonstrated*

### 推理灵活性

推理时，WAM-Flow 通过控制去噪步数实现**计算-精度权衡**：1 步去噪在 NAVSIM-v1 上取得 89.1 PDMS，推理速度达 ReCogDrive 的 4.67 倍；5 步去噪进一步提升至 90.3 PDMS，延迟与 ReCogDrive 持平。这种并行粗到细机制赋予了 VLA 模型前所未有的灵活部署能力。



WAM-Flow 将自车轨迹规划转化为结构化 token 空间上的离散流匹配问题，其核心由三个相互协作的模块构成：度量对齐数值分词器、离散流匹配去噪头、以及仿真引导的 GRPO 对齐模块。

### 度量对齐数值分词器

传统 VLA 模型直接使用文本分词器处理连续标量（如坐标值），导致嵌入空间中数值的几何距离被破坏。WAM-Flow 设计了一个专用的数值分词器来解决这一问题。

**离散化**：将连续标量值归一化到区间 $[-100, 100]$，并均匀离散化为包含 $N = 20{,}001$ 个 token 的码本 $\mathcal{V} = \{v_1, v_2, \ldots, v_N\}$。每个 token 对应一个可学习的嵌入向量。

**度量对齐训练**：为确保嵌入空间中的距离保持与原始标量差值一致的单调性，引入三重态排序损失：

$$
\mathcal{L}_{\mathrm{num}} = \mathbb{E}_{(i, j, k) \sim \mathcal{T}} \left[ \max \left( 0, \, d_{ij} - d_{ik} + \alpha \right) \right] \tag{5}
$$

其中 $\mathcal{T}$ 是从码本中采样的三元组 $(i, j, k)$，满足 $|i - j| < |i - k|$；$d_{ij}$ 表示 token $v_i$ 与 $v_j$ 嵌入向量之间的欧氏距离；$\alpha$ 为间隔超参数。该损失强制嵌入空间中“数值相近的 token 距离更近”，从而将标量的几何结构注入离散表示。

消融实验表明，用该专用数值分词器替换 Janus-1.5B 的文本分词器，PDMS 提升 **4.9 点**（76.2 → 81.1）；进一步加入度量对齐嵌入，额外带来 **2.3 点**增益（81.1 → 83.4），验证了保持数值几何结构对规划精度的关键作用。

### 离散流匹配：并行粗到细去噪

WAM-Flow 将规划建模为连续时间马尔可夫链（CTMC）上的离散流匹配，实现全并行、双向的去噪过程，赋予模型灵活的粗到细推理能力。

**概率路径构造**：给定目标 token 序列 $x_1 \in \mathcal{S}$（其中 $\mathcal{S}$ 为 $D$ 维离散状态空间），定义条件概率路径 $p_t(x | x_1)$，并假设各坐标条件独立：

$$
p_t(x) = \sum_{x_1 \in \mathcal{S}} q(x_1) \, p_t(x | x_1), \quad p_t(x | x_1) = \prod_{i=1}^{D} p_t^i \big( x^i | x_1^i \big) \tag{1}
$$

实际采用混合路径形式，通过调度函数 $\kappa_t$ 在源分布 $p^i(x^i)$ 与目标 delta 分布之间插值：

$$
p_t^i(x^i | x_1^i) = (1 - \kappa_t) \, p^i(x^i) + \kappa_t \, \delta_{x_1^i}(x^i) \tag{2}
$$

**CTMC 转移与条件速率**：状态间的瞬时转移由速率 $u_t(x, z)$ 刻画：

$$
P(x_{t+h} = x \mid x_t = z) = \delta_z(x) + h \, u_t(x, z) + o(h) \tag{3}
$$

为引导采样过程向目标 $x_1$ 收敛，论文进一步采用基于距离度量的吉布斯条件路径：

$$
p_t(x | x_1) = \mathrm{softmax}\left( -\beta_t \, d(x, x_1) \right) \tag{6}
$$

对应的条件速率为：

$$
u_t(x, z \mid x_1) = p_t(x | x_1) \, \dot{\beta}_t \left[ d(z, x_1) - d(x, x_1) \right]_+ \tag{7}
$$

其中 $\beta_t$ 为逆温度调度函数，$\dot{\beta}_t$ 为其时间导数，$[\cdot]_+$ 表示仅保留正值。该速率驱动状态从 $z$ 向与目标距离更小的 $x$ 转移，实现“从噪声到目标”的逐步去噪。

**训练目标**：模型作为后验估计器 $p_{1|t}^{\theta}$，通过最小化条件流匹配交叉熵损失来学习预测目标 token：

$$
\mathcal{L}_{\mathrm{CE}}(\theta) = \mathbb{E}_{t \sim \mathcal{U}[0,1], \, x_1 \sim q, \, x \sim p_t(\cdot | x_1)} \left[ -\sum_{i=1}^{D} \log p_{1|t}^{\theta, i}(x_1^i \mid x) \right] \tag{8}
$$

**粗到细推理**：推理时，从纯噪声状态出发，沿条件速率 $u_t$ 并行更新所有坐标 token。通过控制去噪步数（1 步、3 步、5 步），实现计算开销与规划精度之间的灵活权衡：1 步去噪即可在简单场景下获得可接受的轨迹，5 步去噪则在复杂场景中逐步细化轨迹质量。

### 仿真引导 GRPO 对齐

为进一步将开环监督训练的策略与闭环驾驶需求对齐，WAM-Flow 引入仿真引导的组相对策略优化（GRPO）。

**复合奖励设计**：利用 NAVSIM 仿真器提供的闭环指标构建奖励函数，融合安全惩罚与性能目标：

$$
R(\tau) = \underbrace{\Bigg( \prod_{m \in \mathcal{M}} s_m(\tau) \Bigg)}_{\text{安全惩罚}} \cdot \underbrace{\Bigg( \frac{\sum_{w \in \mathcal{W}} \lambda_w \, s_w(\tau)}{\sum_{w \in \mathcal{W}} \lambda_w} \Bigg)}_{\text{性能目标}} \tag{9}
$$

其中 $\mathcal{M}$ 为安全指标集合（碰撞、可行驶区域合规），以连乘形式作为硬约束；$\mathcal{W}$ 为性能指标集合（进度、TTC、舒适度），以加权求和形式优化驾乘体验。消融确定最优权重比为 EP:TTC:Comfort = 5:5:2。

**GRPO 优化目标**：对每个输入条件 $c$，采样 $G$ 条轨迹，以组内平均奖励为基线计算优势 $A_i$，并通过裁剪和 KL 正则稳定更新：

$$
\mathcal{L}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{c} \left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{T_i} \sum_{k=1}^{T_i} \left( \min \left\{ r_i^k(\theta) A_i, \, \mathrm{clip}(r_i^k(\theta), 1-\epsilon, 1+\epsilon) A_i \right\} - \beta D_{\mathrm{KL}} \left( \pi_{\theta}(\cdot | s_i^k) \| \pi_{\mathrm{ref}}(\cdot | s_i^k) \right) \right) \right] \tag{10}
$$

其中 $r_i^k(\theta)$ 为当前策略与参考策略的概率比，$D_{\mathrm{KL}}$ 项防止策略偏离参考模型过远。消融表明，GRPO 组大小设为 $G=3$ 时达到最优 PDMS 90.3，相较无 GRPO 的基线提升 **3.6 点**。



## 实验与关键发现

### 闭环规划主结果

WAM-Flow 在 NAVSIM-v1 和 NAVSIM-v2 两个官方闭环基准上均取得最优，验证了离散流匹配范式在端到端规划中的有效性。

**NAVSIM-v1 基准。** 如 Table 1 所示，WAM-Flow 以 5 步去噪取得 90.3 PDMS，超越所有自回归和扩散基线。值得关注的是，即使在仅 1 步去噪的极简配置下，模型仍可达 89.1 PDMS——这一结果已接近此前最优的 ReCogDrive（89.6 PDMS），而推理速度却是其 4.67 倍。5 步配置在保持与 ReCogDrive 相当延迟的前提下，将 PDMS 进一步推至 90.3（+1.2 点 vs 1 步），验证了粗到细精化的实际收益。在感知效率上，WAM-Flow 仅使用单目前视相机即超越了多数多相机或 LiDAR 方案（如 Hydra-MDP++、Transfuser），体现了算法层面的结构优势。

**NAVSIM-v2 基准。** 在扩展指标集上（Table 4），WAM-Flow 取得 84.7 EPDMS 的总体最优。新增的驾驶方向合规（DDC）、车道保持（LK）、交通灯响应（TL）等维度对规划的语义理解提出更高要求，WAM-Flow 在这些子指标上同样领先，表明度量对齐分词器与 VQA 预训练为模型注入了有效的几何与语义先验。

**nuScenes 端到端规划。** 在 UniAD 评估协议下（Table 7），WAM-Flow 将平均碰撞率降至 0.23%，刷新最优记录（此前最优 DME-Driver 为 0.29%，AutoVLA 为 0.31%）。该结果进一步证实仿真引导 GRPO 在闭环安全性上的增益可迁移至不同评估框架。

### 核心组件消融

Table 5 逐层揭示了各模块的独立贡献，所有实验均在 NAVSIM-v1 上进行：

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/012_Table_5.jpg]]
*Table 5: Ablation study for the proposed components. We evaluate the effect of metric-aligned numerical tokenizer, VQA pretraining and simulator-guided GRPO on NAVSIM-v1. Row 1 uses the text tokenizer from Janus-1.5B to tokenize the number. “SG GRPO” refers to “Simulator-Guided GRPO”*

| 消融步骤 | PDMS | 增益 |
|-----------|------|------|
| Janus 文本分词器（基线） | 76.2 | — |
| + 专用数值分词器 | 81.1 | **+4.9** |
| + 度量对齐嵌入 | 83.4 | **+2.3** |
| + VQA 大规模预训练 | 86.7 | **+3.3** |
| + 仿真引导 GRPO | 90.3 | **+3.6** |

**数值分词器的决定性作用。** 将 Janus-1.5B 的通用文本分词器替换为专用数值分词器，直接带来 4.9 点 PDMS 跃升。这一定量证据强有力地支持了核心洞见：标准文本分词器将连续标量（坐标值）映射到语义空间时破坏了数值的几何结构，而专用分词器通过均匀离散化到 [-100, 100] 区间上的 20,001 个 token，保留了标量的量级信息。

**度量对齐嵌入的增益。** 在数值分词器基础上引入三重态排序损失（Eq. 5）进行度量对齐，进一步贡献 2.3 点。这验证了仅靠均匀离散化不足以让嵌入空间感知数值距离——度量对齐将“数值差”注入嵌入距离，使流匹配的转移速率（Eq. 7）能基于有意义的几何距离驱动去噪。

**VQA 预训练的语义注入。** 大规模视觉问答预训练（650 万样本）额外提升 3.3 点，将 PDMS 从 83.4 推至 86.7。Figure 6 显示预训练 epoch 数与 PDMS 呈正相关但边际递减，表明语义先验对规划任务存在饱和效应。预训练主要增强了模型对导航指令和场景语义的理解，为后续 GRPO 提供了更优的初始化策略。

**仿真引导 GRPO 的闭环对齐。** GRPO 阶段贡献了 3.6 点增益，将 PDMS 从 86.7 提升至最终的 90.3。这确认了仅靠监督流匹配（行为克隆）无法充分对齐闭环安全与舒适目标——仿真器反馈的复合奖励函数（Eq. 9：安全项连乘 × 性能项加权和）通过策略优化弥补了开环模仿的分布偏移。

### GRPO 关键超参数分析

**组大小。** Table 2 显示 GRPO 组大小 G=3 时取得最优 PDMS 90.3。G=1（退化为 PPO）为 89.3，G=2 为 89.8，G=4 降至 89.5。过小的组导致优势估计方差大，过大的组增加无效探索，3 在探索效率与估计稳定性间取得平衡。

**奖励权重。** Table 3 探索了复合奖励中 EP（自我进度）:TTC（碰撞时间）:Comfort（舒适度）的比例。默认 5:5:2 取得最优 90.3 PDMS；将任一项放大 4 倍均导致下降（如 EP 主导时降至 89.6，TTC 主导时 89.4）。这表明安全（TTC）与效率（EP）需均衡，过度偏向任一方会损害综合表现。

### 推理效率与计算-精度权衡

Table 6 展示了去噪步数与推理效率的关系。1 步去噪在 NAVSIM 上实现最低延迟，同时保持 89.1 PDMS 的竞争力；5 步去噪以可接受的额外计算换取 90.3 PDMS 的最优精度。这种灵活的慢-快、粗-细权衡是离散流匹配相对于自回归解码的独特优势——后者无法在推理时动态调整计算预算。Figure 9–11 的定性结果进一步佐证：简单场景下 1 步去噪即可生成合理轨迹，复杂场景（如交叉口转弯、密集交通流）则受益于 5 步逐步精化。

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/014_Table_6.jpg]]
*Table 6: Intuitive efficiency analysis on NAVSIM*

### 定性分析

Figure 4 展示了 WAM-Flow 与基线方法在 NAVSIM 上的轨迹对比。在需要精细避让或复杂转向的场景中，WAM-Flow 的规划轨迹更平滑且更贴近参考路径，而自回归基线在长时域预测上出现累积漂移。Figure 5 按场景类型展示了 WAM-Flow 的泛化能力，涵盖直行、转弯、变道等多种工况。

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative comparison on NAVSIM*

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative results of WAM-Flow on NAVSIM with different scenes*

### 局限与待验证问题

尽管实验证据充分，以下结论需谨慎外推：

1. **仿真到真实的迁移。** 所有评估均在 NAVSIM 和 nuScenes 仿真器上进行，GRPO 的奖励函数针对仿真指标设计，其安全/性能权重（5:5:2）在真实驾驶中可能需要重新校准。论文未提供实车验证或 Sim-to-Real 迁移实验。

2. **长尾场景覆盖。** 现有基准可能未充分覆盖真实驾驶的长尾分布。WAM-Flow 在极端工况（如无保护左转、对抗性行人）下的表现缺乏定量证据。

3. **单模态感知的鲁棒性边界。** 模型仅使用单目前视相机，在恶劣天气、强逆光或传感器失效场景下的退化程度未经验证。融合 LiDAR 或雷达是否能进一步提升鲁棒性仍是开放问题。

4. **GRPO 的仿真依赖性。** 论文提出学习世界模型作为仿真器奖励的替代方案（见开放问题），但当前方法仍强依赖 NAVSIM 仿真器的闭环反馈，这限制了其在无仿真器环境中的部署能力。

综上，WAM-Flow 在闭环规划基准上的领先优势由多组件协同贡献，消融实验提供了清晰的因果链。但 Sim-to-Real 差距和长尾鲁棒性是需要进一步验证的关键风险点。

### 补充图表

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/005_Table_1.jpg]]
*Table 1: Comparison on NAVSIM-v1 with closed-loop metrics. Abbreviation: Diff.(Diffusion), Comf.(Comfort), Cam (Camera), L (LiDAR)*

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/011_Table_4.jpg]]
*Table 4: Comparison on NAVSIM-v2 with extended metrics*

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/016_Table_7.jpg]]
*Table 7: End-to-end motion planning performance on the nuScenes [4] dataset. We sort previous methods according to the average collision rate. Abbreviation: Diff.(Diffusion), AR (autoregressive), DFM (discrete flow matching)*

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/006_Table_2.jpg]]
*Table 2: Ablation on GRPO group size*

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/007_Table_3.jpg]]
*Table 3: Ablation on different weight of Simulator-Guided reward. The default weight is 5:5:2 for Navsim simulator, and we adjust the scale of each weight by 4× to obtain the new weight*

![[assets/figures/papers/paper_list_l2627_https_arxiv_org_abs_2512_06112/figures/013_Figure_6.jpg]]
*Figure 6: Impact of pre-training epochs. We perform SFT after pre-training on 6.5M data, and then calculate PDMS*



## 定位与知识库关联

### 与现有范式的关键差异

WAM-Flow 在三个维度上重新定义了 VLA 规划模型的设计空间：

**生成范式：从自回归到并行流匹配。** 现有主流 VLA 规划器——如 **DrivingGPT**、**FSDrive**、**AutoVLA**——均采用自回归逐 token 解码，依赖因果注意力掩码顺序生成未来轨迹点。这一范式存在两个结构性瓶颈：(1) 推理速度受限于序列长度，难以实现实时闭环控制；(2) 曝光偏差（exposure bias）导致训练-推理分布失配。扩散规划方法（**Artemis**、**DiffusionDrive**）虽支持并行去噪，但其连续扩散过程在离散 token 空间上缺乏自然的几何约束。WAM-Flow 将规划任务建模为离散流匹配（discrete flow matching）问题，在结构化 token 空间上执行完全并行的双向去噪，从根本上消除了因果解码的序列依赖。这一设计使得模型可在 1 步去噪下获得有竞争力的结果（89.1 PDMS），在 5 步粗到细细化后达到最优（90.3 PDMS），实现了灵活的计算-精度权衡。

**数值表示：从文本分词器到度量对齐分词器。** 自回归 VLA 模型（如基于 Janus-1.5B 的方案）直接复用文本分词器处理连续数值坐标，忽视了标量空间的几何结构。文本 token 的嵌入距离与原始数值差值的单调性无任何保证——相邻 token 可能对应相距甚远的坐标值。WAM-Flow 引入度量对齐数值分词器，将连续标量离散化到 [-100, 100] 上的 20,001 个 token，并通过三重态排序损失强制嵌入距离保持与标量差值一致的单调性。消融实验表明，仅替换分词器即带来 **+4.9 PDMS** 的提升，进一步加入度量对齐嵌入再获 **+2.3 PDMS**，证明数值 token 的几何保真度对规划精度至关重要。

**训练目标：从行为克隆到仿真引导的强化对齐。** 传统 VLA 模型仅依赖监督对数似然（行为克隆）训练，无法直接优化闭环驾驶的安全性和舒适性指标。**AutoVLA** 虽引入强化微调，但未针对驾驶场景设计专门的奖励结构。WAM-Flow 采用四阶段课程训练：数值嵌入预训练 → VQA 大规模预训练 → 监督流匹配微调 → 仿真引导 GRPO 对齐。GRPO 阶段使用 NAVSIM 仿真器提供的复合奖励——安全项（碰撞 × 可行驶区域合规）连乘，性能项（进度、TTC、舒适度）加权求和——通过组相对策略优化（group size=3 最优）稳定对齐闭环目标。GRPO 单独贡献 **+3.6 PDMS**，且 VQA 预训练提供 **+3.3 PDMS** 的额外增益。

### 在知识库中的定位

WAM-Flow 处于 VLA 规划、离散扩散模型和强化学习对齐三个研究方向的交汇点：

- **相对于 VLA 规划**：WAM-Flow 是首个将离散流匹配引入端到端驾驶规划的 VLA 模型，在 NAVSIM-v1（90.3 PDMS）、NAVSIM-v2（84.7 EPDMS）和 nuScenes 碰撞率（0.23%）三项指标上均取得最优。值得注意的是，该方法仅使用单目前视相机即超越了多数多相机或 LiDAR 融合方案（如 **Transfuser**、**Hydra-MDP++**），体现了算法效率优势。

- **相对于离散扩散模型**：离散流匹配在文本生成、蛋白质设计等领域已有探索，但 WAM-Flow 首次将其适配到具身规划任务，并通过度量对齐分词器和几何感知流目标解决了数值回归的精度问题。吉布斯条件路径（Eq. 6）和基于距离的转移速率（Eq. 7）为离散空间中的粗到细控制提供了理论支撑。

- **相对于 RL 对齐**：GRPO 在语言模型对齐中已被验证有效，WAM-Flow 将其迁移至驾驶规划，并通过仿真器提供可微的安全-性能复合奖励。这一范式为弥合开环训练与闭环部署之间的差距提供了可行路径。

### 适用边界

- **感知模态**：当前模型仅处理单目前视图像，尚未融合 LiDAR、雷达或环视多相机输入。在遮挡严重或需要 360° 感知的场景中，性能可能受限。
- **规划时域**：固定输出 4 秒内的 8 个 waypoint，无法自适应调整规划时域。对于高速场景或长距离变道，可能需要更长的预测窗口。
- **交互复杂度**：当前轨迹规划主要处理单车运动，尚未显式建模多智能体博弈（如换道协商、无保护左转）。复杂交互场景下的安全性需进一步验证。
- **仿真到真实的迁移**：GRPO 奖励函数针对 NAVSIM 仿真器设计，安全项和性能项的权重（EP:TTC:Comfort = 5:5:2）在真实环境中可能需要重新标定。仿真器中的碰撞检测和可行驶区域判断可能与真实传感器存在分布偏移。

### 局限与开放问题

1. **Sim-to-Real 差距**：GRPO 奖励依赖仿真器的完美状态估计，真实部署中感知噪声和预测不确定性会削弱奖励信号的可靠性。如何设计鲁棒的奖励函数或学习一个世界模型作为仿真器的通用替代，是实用化的关键挑战。

2. **多模态融合**：现有框架的视觉编码器（SigLIP）和语言骨干（Janus-1.5B）均为通用模型，未针对驾驶场景的多传感器融合进行专门设计。将 LiDAR 点云、雷达信号等模态纳入统一的 token 空间并保持度量对齐，是扩展感知鲁棒性的自然方向。

3. **可变时域与分层规划**：固定 8-waypoint 输出限制了模型在复杂机动（如 U 型转弯、多步变道）中的表达能力。将离散流匹配扩展到可变长度的 token 序列，或引入分层规划（粗轨迹 + 细控制），可能进一步提升灵活性。

4. **度量对齐分词器的泛化性**：当前数值分词器针对标量坐标设计，其度量对齐思想能否推广到其他需要高精度回归的模态（如速度、加速度、方向盘转角）或任务（如机器人关节控制），值得进一步探索。

5. **长尾分布覆盖**：现有基准（NAVSIM、nuScenes）主要覆盖常规驾驶场景，可能未充分包含真实驾驶中的长尾分布（如极端天气、罕见交通参与者行为）。模型在这些场景下的安全性需要额外验证。

6. **计算-精度的理论最优**：WAM-Flow 展示了 1 步到 5 步去噪的性能单调提升，但最优步数与场景复杂度的自适应选择机制尚未建立。学习一个轻量级的步数预测器，或设计基于不确定性的早停策略，可进一步优化推理效率。



## 原文 PDF

![[paperPDFs/CVPR_2026/WAM_Flow_Parallel_Coarse_to_Fine_Motion_Planning_via_Discrete_Flow_Matching_for_Autonomous_Driving.pdf]]
