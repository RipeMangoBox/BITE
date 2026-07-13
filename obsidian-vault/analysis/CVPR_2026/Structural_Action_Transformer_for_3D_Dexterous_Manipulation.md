---
title: Structural Action Transformer for 3D Dexterous Manipulation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Structural_Action_Transformer_for_3D_Dexterous_Manipulation.pdf
project_link: "https://xiaohanlei.github.io/projects/SAT"
code_link: null
aliases:
- SATS
- SAT3DM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将动作块从时间中心视角（T, D_a）重构为结构中心视角（D_a, T），即将动作视为变长、无序的关节轨迹序列，并引入“Embodied Joint Codebook”为每个关节赋予功能类别和旋转轴的结构先验。这种重构使得Transformer能够原生地处理异构形态，并通过自注意力学习关节间的功能对应关系。
primary_logic: 动作表示的结构化重构（从时间序列到关节序列）解锁了Transformer处理变长序列的天然能力，结合物理关节属性编码，使得策略能够跨不同机器人形态学习可迁移的技能，解决了高自由度灵巧手的跨形态模仿学习难题。
claims:
- 在11个灵巧操作任务上，SAT以19.36M参数显著优于所有2D/3D基线（如3D ManiFlow Policy 218.9M），平均成功率从0.66提升至0.71，且参数效率极高。
- 移除Embodied Joint Codebook导致成功率断崖式下降（从0.71到0.01），证明结构先验对于无序关节序列的识别必不可缺。
- 仅使用人类数据预训练即可超越使用机器人数据进行预训练（0.68 vs 0.66），证实功能代码本成功实现了从人手到机器人灵巧手的技能迁移。
- Adroit (3 tasks) 上 Average Success Rate = 0.75±0.02
---

# Structural Action Transformer for 3D Dexterous Manipulation

> [!tip] 核心洞察
> 动作表示的结构化重构（从时间序列到关节序列）解锁了Transformer处理变长序列的天然能力，结合物理关节属性编码，使得策略能够跨不同机器人形态学习可迁移的技能，解决了高自由度灵巧手的跨形态模仿学习难题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于三维灵巧操作的结构化动作Transformer |
| 英文题名 | Structural Action Transformer for 3D Dexterous Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.03960) · [Project](https://xiaohanlei.github.io/projects/SAT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Structural Action Transformer (SAT) |
| Dataset | Adroit, DexArt, Bi-DexHands, 11任务平均 |

> [!tip] 效果简介
> - Adroit (3 tasks) 上，Average Success Rate 0.75±0.02 vs 0.70±0.02 (3D ManiFlow Policy) (+0.05)。
> - DexArt (4 tasks) 上，Average Success Rate 0.73±0.03 vs 0.70±0.03 (3D ManiFlow Policy) (+0.03)。
> - Bi-DexHands (4 tasks) 上，Average Success Rate 0.67±0.05 vs 0.59±0.07 (3D ManiFlow Policy) (+0.08)。

## 概要

**核心问题**：高自由度灵巧手的三维操作策略学习长期受困于一个根本瓶颈——传统方法将动作块视为固定长度的时间序列（T, D_a），这种“时间中心”表示无法自然地处理不同机器人形态之间的关节数量差异，也难以编码灵巧操作必需的高维空间结构关系。

**核心洞见**：本文提出**结构中心视角的动作表示重构**，将动作块从时间序列翻转为关节序列（D_a, T），即把每个关节的完整时域轨迹视为一个独立的序列元素。这一视角转换使Transformer能够原生地处理变长、无序的关节序列，并天然适应异构形态。

**关键技术杠杆**：为赋予无序关节序列以物理语义，引入**Embodied Joint Codebook**——一个基于形态学三元组（形态ID、功能类别、旋转轴）的可学习嵌入表，为每个关节注入结构先验。政策网络采用连续时间标准化流（Flow Matching）生成动作，仅需1次网络前向评估即可完成推理。

**主要结果**：在Adroit、DexArt和Bi-DexHands三个仿真基准共11个灵巧操作任务上，SAT以仅19.36M参数显著优于所有2D/3D基线方法，平均成功率从0.66提升至0.71。消融实验揭示了两项决定性证据：（1）移除Embodied Joint Codebook导致成功率从0.71断崖式下降至0.01，证明结构先验对于无序关节序列的识别必不可缺；（2）仅使用人类数据预训练即可超越使用机器人数据预训练（0.68 vs 0.66），证实功能代码本成功实现了从人手到机器人灵巧手的跨形态技能迁移。



灵巧操作（dexterous manipulation）是具身智能研究的长期目标。高自由度（high-DoF）灵巧手具备执行复杂接触丰富任务的潜力，但其动作空间维度远高于传统夹爪，使得策略学习面临严重的维度灾难。近年来，模仿学习（imitation learning）在机器人操作中取得了显著进展，尤其是基于动作块（action chunk）的生成式策略，通过一次预测未来多步动作，有效缓解了复合误差和时序依赖问题。

然而，**传统动作表示存在根本性的结构缺陷**，成为制约通用灵巧策略学习的核心瓶颈。现有方法普遍采用时间中心（temporal-centric）视角，将动作块建模为固定长度的时间步序列 `(T, D_a)`，其中每个时间步的动作向量是固定维度的整体。这种表示在面对高自由度机械手时暴露出两个关键问题：

1. **跨形态迁移困难**：不同机器人形态（如人手、Allegro Hand、Shadow Hand）具有不同的关节数量和拓扑结构，时间中心表示要求 `D_a` 维度固定，无法原生处理变长关节序列，导致策略难以在异构形态之间共享技能。
2. **空间关系捕获低效**：时间中心视角将每个时间步的所有关节动作打包为一个向量，Transformer 的自注意力机制在时间维度上运作，难以显式建模不同关节之间的功能对应和空间协同关系。对于灵巧操作而言，关节间的结构关系（如拇指与食指的协同）比时间维度的精细变化更为关键。

**本文的核心动机在于重构动作表示范式**：将动作块从时间中心视角 `(T, D_a)` 翻转为结构中心视角 `(D_a, T)`，即将动作视为变长、无序的关节轨迹序列，每个关节的完整时域轨迹作为一个独立的序列元素。这一重构解锁了 Transformer 处理变长序列的天然能力，使得策略能够原生适配不同关节数量的机器人形态。配合 **Embodied Joint Codebook** 为每个关节注入形态学三元组（形态ID、功能类别、旋转轴）的结构先验，模型得以在无序的关节序列中识别物理关节身份，从而学习跨形态的功能对应关系。



## 核心方法与创新机理

SAT 的核心创新在于对动作表示的根本性重构，以及配套的关节结构先验编码机制。这两项设计共同构成了与传统基线相比的关键 changed slots，使得策略能够原生处理异构形态的高自由度灵巧手。

### 1. 动作表示：从时间中心到结构中心

传统方法（如 **Diffusion Policy** (Zhao et al., 2023)、**3D ManiFlow Policy** (Yan et al., CoRL 2025)）将动作块视为固定长度的时间步序列，即时间中心表示 $(T, D_a)$，其中每个时间步的动作向量是固定维度的整体。这种表示隐含假设所有机器人具有相同数量的执行器，无法处理不同形态机器人之间关节数量 $D_a$ 的变化，因而难以实现跨形态技能迁移。

SAT 提出结构中心表示 $(D_a, T)$：将动作块重构为变长、无序的关节轨迹序列，每个元素是一个关节在 $T$ 个未来时间步上的完整轨迹。序列长度等于关节数 $D_a$，可随机器人形态自由变化。这一重构解锁了 Transformer 处理变长序列的天然能力，使得策略能够原生适配从人手到多指灵巧手的异构形态（Figure 1）。

消融实验验证了这一设计的优越性：将结构中心表示改回传统时间中心表示后，平均成功率从 0.71 降至 0.64（Table 4），证实结构中心范式对高自由度操作任务更为有效。

### 2. 关节身份编码：Embodied Joint Codebook

结构中心表示将动作序列变为无序集合，Transformer 本身无法区分不同关节的轨迹。为此，SAT 引入 Embodied Joint Codebook，为每个关节赋予基于形态学三元组的可学习结构嵌入：

- **Embodiment ID**：关节所属的机器人形态标识；
- **Functional Category**：关节的功能类别（如拇指对掌、食指屈曲等）；
- **Rotation Axis**：关节的旋转轴方向。

该代码本通过对 10 种常见灵巧手的关节类型进行频率分析构建（Figure 5），将物理关节属性编码为结构先验。在推理时，每个关节的压缩轨迹与对应的代码本嵌入相加，形成携带结构身份的动作 token（Section 3.3.2）。

代码本的关键作用通过消融实验得到有力验证：
- 完全移除 Embodied Joint Codebook 导致成功率从 0.71 断崖式下降至 0.01（Table 4），因为 Transformer 无法将无序轨迹匹配到物理关节，学习任务变得不可能。
- 单独移除 Functional Category 同样导致灾难性失败（Table 5），表明功能对应是跨形态迁移最重要的先验。

### 3. 跨形态技能迁移的证据

Embodied Joint Codebook 中的功能类别编码使得人手与机器人灵巧手之间建立了功能对应关系。预训练数据消融实验（Table 3）显示，仅使用人类数据预训练的成功率（0.68）超过了仅使用机器人数据预训练（0.66），证实代码本成功实现了从人手到机器人灵巧手的技能迁移。T-SNE 可视化（Figure 6）进一步表明，学习到的嵌入按功能类别形成清晰聚类，验证了结构先验的有效性。

### 4. 生成模型的轻量化设计

SAT 采用连续时间标准化流（Flow Matching）替代扩散模型，训练条件速度场 $\epsilon_\theta$ 预测目标动作与噪声之差：

$$\mathcal{L}(\theta) = \mathbb{E}_{\tau \sim \mathcal{U}(0,1), \mathbf{A}_t^0 \sim \mathcal{N}(0,I), \mathbf{A}_t^1 \sim \mathcal{D}} \left[ \left| \left| \epsilon_\theta (\mathbf{A}_t^\tau, \tau, o_t) - (\mathbf{A}_t^1 - \mathbf{A}_t^0) \right| \right|^2 \right]$$

推理时使用 ODE 求解器，仅需 1 次函数评估（NFE）即可生成动作块，相比扩散模型的迭代去噪更为高效。结合结构中心表示对时间轨迹的高度压缩（token 维度从 256 降至 32 时成功率保持 0.71，Table 2），SAT 仅以 19.36M 参数（不含 T5 tokenizer）即在 11 个灵巧操作任务上取得 0.71 的平均成功率，显著优于 218.9M 参数的 3D ManiFlow Policy（0.66），展现出极高的参数效率。



SAT 的完整推理管线由三个核心模块串联构成：**Observation Tokenizer**（观测标记器）、**Structural Action Tokenizer**（结构化动作标记器）与 **Structural Action Transformer**（结构化动作Transformer）。其输入为一段包含 $T_o$ 帧的历史原始3D点云 $\mathcal{P}_t = (\mathbf{P}_{t-T_o+1}, \ldots, \mathbf{P}_t)$ 以及一条语言指令 $L$，输出为未来 $T$ 个时间步的动作块 $\mathbf{A}_t \in \mathbb{R}^{D_a \times T}$。该动作块采用**结构中心视角**定义，即每一行对应一个关节在整段时域上的完整轨迹，行数 $D_a$ 随机器人形态自由变化，从而天然支持变长、无序的异构关节序列。

### 观测标记器（Observation Tokenizer）

该模块负责将高维、非结构化的3D点云历史与语言指令压缩为统一的 token 序列，作为后续 Transformer 的条件输入。其处理流程如下：

1. **点云层级化 token 化**：对每一帧原始点云，首先通过最远点采样（FPS）选取 $M$ 个局部中心点，随后利用共享的 PointNet 分别提取每个局部邻域的几何特征，得到 $M$ 个局部 token $\{tok_{l}\}$；同时，对全局点云也通过 PointNet 提取一个全局 token $tok_{g}$，捕获整体场景语义。
2. **时序拼接**：将 $T_o$ 帧的全局 token 与局部 token 分别按时序拼接，形成历史 token 序列：
   $$tok_{hist} = \mathbf{Cat} \big( \mathbf{Cat}(tok_{g, t-T_o+1}, \ldots, tok_{g, t}), \mathbf{Cat}(tok_{l, t-T_o+1}, \ldots, tok_{l, t}) \big) \in \mathbb{R}^{(1+M) \times d_{feat}}$$
3. **语言 token 融合**：语言指令 $L$ 通过预训练的 T5 编码器转换为语言 token $tok_{lang}$，并与历史 token 拼接，构成最终的观测条件序列：
   $$tok_{obs} = \mathbf{Cat}(tok_{hist}, tok_{lang})$$

### 结构化动作标记器（Structural Action Tokenizer）

该模块是 SAT 实现跨形态泛化的关键设计，其核心在于将噪声动作块从“时间序列”重构为“关节序列”，并注入物理结构先验。

1. **关节轨迹压缩**：在推理时，首先从标准高斯分布采样一个噪声动作块 $\mathbf{A}_t^0 \in \mathbb{R}^{D_a \times T}$。将其视为 $D_a$ 个独立的关节轨迹，每个轨迹通过一个共享的 MLP 从 $T$ 维压缩至低维嵌入维度 $d_{feat}$（如从64维压缩至16维），得到压缩后的动作 token $tok_{act}$。
2. **Embodied Joint Codebook 嵌入**：为每个关节赋予一个可学习的结构嵌入向量，该向量由形态学三元组——**形态ID**（Embodiment ID）、**功能类别**（Functional Category）与**旋转轴**（Rotation Axis）——通过代码本查表得到，构成嵌入矩阵 $\mathbf{E}$。最终输入 Transformer 的动作 token 为压缩轨迹与结构嵌入之和：
   $$tok_{input.act} = tok_{act} + \mathbf{E}$$
   这一设计使得 Transformer 能够识别每个 token 对应的物理关节身份及其功能角色，解决了无序序列中“哪个轨迹属于哪个关节”的根本歧义。

### 结构化动作Transformer（Structural Action Transformer）

该模块基于 Diffusion Transformer（DiT）架构，并添加因果掩码，以观测 token $tok_{obs}$ 为条件，预测动作 token 的速度场。

1. **速度场预测**：Transformer 接收拼接后的观测 token 与动作 token，输出预测的速度场 $\epsilon_\theta(\mathbf{A}_t^\tau, \tau, o_t)$，其中 $\tau \in (0,1)$ 为流匹配时间步。训练目标为最小化流匹配损失：
   $$\mathcal{L}(\theta) = \mathbb{E}_{\tau \sim \mathcal{U}(0,1), \mathbf{A}_t^0 \sim \mathcal{N}(0,I), \mathbf{A}_t^1 \sim \mathcal{D}} \left[ \left\| \epsilon_\theta(\mathbf{A}_t^\tau, \tau, o_t) - (\mathbf{A}_t^1 - \mathbf{A}_t^0) \right\|^2 \right]$$
   其中 $\mathbf{A}_t^\tau = \tau \mathbf{A}_t^1 + (1-\tau) \mathbf{A}_t^0$ 为沿线性路径插值的中间状态。

2. **动作生成**：推理时，从噪声 $\mathbf{A}_t^0$ 出发，使用 ODE 求解器沿预测速度场积分，仅需 1 次函数评估（1 NFE）即可生成最终动作块 $\mathbf{A}_t^1$，随后由控制器执行。

### 数据流总览

整个管线可概括为：**3D点云 + 语言 → 观测 token → 条件Transformer → 速度场 → ODE积分 → 结构化动作块**。其中，观测标记器将多模态感知压缩为统一表示，结构化动作标记器将异构关节空间映射到携带物理先验的 token 空间，Transformer 则在这两个空间之间学习条件映射。这种设计使得 SAT 能够以仅 19.36M 参数（不含 T5 编码器）在 11 个灵巧操作任务上达到 0.71 的平均成功率，显著优于参数规模大一个数量级的 3D 基线（如 3D ManiFlow Policy 的 218.9M 参数，成功率 0.66）。

### 补充图表

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/001_Figure.jpg]]
*Figure: (a) Temporal-centric Perspective (b) Structural-centric Perspective (Ours) Key Features: Unordered, Variable Length Heterogeneity*

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/002_Figure_2.jpg]]
*Figure 2: Our proposed model architecture. The policy takes a history of*



SAT 的策略架构由三个核心模块级联构成：**Observation Tokenizer**、**Structural Action Tokenizer** 和 **Structural Action Transformer**。整体流程如 Figure 2 所示。

### 3.1 观测标记器（Observation Tokenizer）

该模块将历史 3D 点云序列和语言指令转化为统一的 token 序列，作为 Transformer 的条件输入。

**点云层级 Token 化**：对于历史窗口内的每一帧原始点云 $\mathbf{P}_t$，首先通过最远点采样（FPS）选取 $M$ 个局部中心点，再以每个中心点为锚点聚合其邻域点，通过共享的 PointNet 提取两类 token：
- **全局 token** $tok_{g, t}$：表征整帧点云的全局几何信息。
- **局部 token** $tok_{l, t}$：$M$ 个局部区域的几何特征，捕获细粒度空间结构。

**历史序列拼接**：将 $T_o$ 个历史帧的全局 token 和局部 token 分别按时序拼接，形成历史点云序列表示：

$$tok_{hist} = \mathbf{Cat}\big(\mathbf{Cat}(tok_{g, t-T_o+1}, \ldots, tok_{g, t}),\ \mathbf{Cat}(tok_{l, t-T_o+1}, \ldots, tok_{l, t})\big) \in \mathbb{R}^{(1+M) \times d_{feat}}$$

**语言指令编码**：语言指令 $L$ 通过预训练的 T5 编码器转化为语言 token $tok_{lang}$。

**最终观测序列**：将历史点云 token 与语言 token 拼接，构成完整的条件序列：

$$tok_{obs} = \mathbf{Cat}(tok_{hist}, tok_{lang})$$

### 3.2 结构化动作标记器（Structural Action Tokenizer）

该模块是 SAT 的核心创新，实现了从“时间中心”到“结构中心”的动作表示重构。

**结构中心视角**：传统方法将动作块视为 $(T, D_a)$ 的时序向量序列，而 SAT 将其重构为 $(D_a, T)$——即 $D_a$ 个关节各自在时间窗口 $T$ 内的完整轨迹序列。每个关节的整条时域轨迹被视为一个独立的序列元素，序列长度等于关节数 $D_a$，可随机器人形态自由变化（Figure 1）。

**轨迹压缩**：对于噪声动作块 $\mathbf{A}_t^{\tau} \in \mathbb{R}^{D_a \times T}$，将每个关节的 $T$ 维时域轨迹通过共享的 MLP 压缩至低维嵌入空间 $d_{feat}$（例如从 64 维压缩至 16 维）。实验表明（Table 2），$d_{feat}$ 从 256 降至 32 时成功率几乎不变（0.71），仅在降至 16 时下降至 0.66，说明时域轨迹高度冗余，可被大幅压缩。

**Embodied Joint Codebook**：由于动作序列本身是无序的——Transformer 无法仅从轨迹数据判断哪个 token 对应哪个物理关节——SAT 引入了一个可学习的代码本矩阵 $\mathbf{E}$，为每个关节赋予结构先验。代码本基于形态学三元组构建：
- **Embodiment ID**：标识关节所属的机械手实例。
- **Functional Category**：关节的功能类别（如拇指根部、食指中部等）。
- **Rotation Axis**：关节的旋转轴方向。

**动作输入序列**：压缩后的动作轨迹与代码本嵌入相加，形成携带结构先验的动作 token 序列：

$$tok_{input.act} = tok_{act} + \mathbf{E}$$

### 3.3 结构化动作 Transformer 与流匹配生成

**生成模型选择**：SAT 采用连续时间标准化流（Flow Matching）建模复杂高维的条件分布 $p(\mathbf{A}_t | o_t)$。与扩散模型不同，流匹配直接训练一个速度场网络 $\epsilon_\theta$，推理时通过 ODE 求解器积分，仅需 1 NFE 即可生成动作块，推理效率极高。

**流匹配损失函数**：训练目标是让速度场网络预测目标动作与噪声之差：

$$\mathcal{L}(\theta) = \mathbb{E}_{\tau \sim \mathcal{U}(0,1),\ \mathbf{A}_t^0 \sim \mathcal{N}(0,I),\ \mathbf{A}_t^1 \sim \mathcal{D}} \left[ \left\| \epsilon_\theta(\mathbf{A}_t^\tau, \tau, o_t) - (\mathbf{A}_t^1 - \mathbf{A}_t^0) \right\|^2 \right]$$

其中：
- $\tau \sim \mathcal{U}(0,1)$：均匀采样的时间步。
- $\mathbf{A}_t^0 \sim \mathcal{N}(0,I)$：从标准高斯分布采样的纯噪声。
- $\mathbf{A}_t^1 \sim \mathcal{D}$：从演示数据中采样的真实动作块。
- $\mathbf{A}_t^\tau = \tau \mathbf{A}_t^1 + (1-\tau) \mathbf{A}_t^0$：沿线性路径插值的中间状态。
- $\epsilon_\theta$：待训练的速度场网络。
- $o_t$：观测条件（点云历史 + 语言指令）。

**Transformer 架构**：SAT 的骨干网络基于 DiT（Diffusion Transformer），并添加因果掩码。它接收拼接后的观测 token 和动作 token，预测动作速度场。推理时，从纯噪声出发，通过 ODE 求解器沿预测的速度场积分，得到最终的动作块 $\mathbf{A}_t$。

### 3.4 关键消融证据

Table 4 的组件消融验证了各模块的必要性：
- **移除 Embodied Joint Codebook**：成功率从 0.71 断崖式跌至 0.01。这证实了代码本提供的结构先验对于无序关节序列的识别是**不可缺失**的——没有它，Transformer 无法确定哪条轨迹对应哪个物理关节。
- **回退至时间中心表示**：将结构中心 $(D_a, T)$ 改回传统的时间中心 $(T, D_a)$ 表示，成功率降至 0.64，验证了结构中心视角对高 DoF 操作任务的优越性。
- **移除 Functional Category**（Table 5）：导致灾难性失败，表明功能对应是跨形态迁移最重要的先验。

### 补充图表

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/011_Figure_5.jpg]]
*Figure 5: Frequency analysis of joint types in our Embodied Joint Codebook, derived from a survey of 10 common dexterous hands*

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/009_Figure_6.jpg]]
*Figure 6: T-SNE visualization of the learned Embodied Joint Codebook embeddings. These embeddings, derived from 10 dexterous manipulators, are colored by (a) Embodiment ID, (b) Functional Category, and (c) Rotation Axis*



## 实验与关键发现

### 核心瓶颈与实验动机

传统时间中心（temporal-centric）的动作表示将动作块视为固定长度时序向量的序列，难以处理不同形态机器人之间的跨形态技能迁移，也无法有效捕获灵巧操作必需的高维3D空间关系。SAT通过将动作块重构为结构中心视角（D_a, T）——即将动作视为变长、无序的关节轨迹序列——并引入Embodied Joint Codebook为每个关节赋予功能类别和旋转轴的结构先验，使得Transformer能够原生地处理异构形态，并通过自注意力学习关节间的功能对应关系。实验围绕三个核心问题展开：(1) 结构中心表示是否在高自由度灵巧操作任务上优于时间中心表示？(2) Embodied Joint Codebook的结构先验是否必不可缺？(3) 代码本中的功能对应能否实现从人手到机器人灵巧手的跨形态技能迁移？

### 实验设置

**基准测试与任务。** 实验覆盖三个仿真灵巧操作基准共11个任务：Adroit（3个任务，单手机械手）、DexArt（4个任务，需要精细物体重定位）和Bi-DexHands（4个任务，双手协调操作）。真实世界实验在6个双手操作任务上进行，使用VR头显采集演示数据。

**基线方法。** 对比方法分为2D图像基线和3D点云基线两类。2D基线包括**Diffusion Policy**（Zhao et al., 2023）、**HPT**（Wang et al., NeurIPS 2024）和**UniAct**（Zheng et al., CVPR 2025）；3D基线包括**3D Diffusion Policy**（Ze et al., 2024）和**3D ManiFlow Policy**（Yan et al., CoRL 2025）。其中3D ManiFlow Policy是此前最优的3D通用操作策略，参数规模218.9M。

**训练协议。** 预训练使用AdamW优化器（β=(0.9, 0.999)，ε=1e-8，权重衰减0.01），峰值学习率1e-4，线性预热10,000步后余弦衰减至1e-6。微调阶段学习率降至1e-5。预训练数据混合了人手演示（HOI4D、Ego-Exo4D、ADT）、机器人演示（Fourier ActionNet、DexCap）和仿真演示（Adroit、DexArt、Bi-DexHands）三类数据源。

### 主实验结果

**Table 1** 展示了SAT与所有基线在11个灵巧操作任务上的定量对比（见Table 1）。SAT以仅19.36M参数（不含T5 tokenizer）取得了0.71±0.04的平均成功率，显著优于此前最优的3D ManiFlow Policy（0.66±0.04，218.9M参数），参数效率提升超过一个数量级。

分基准来看，SAT在Adroit上达到0.75±0.02（vs 3D ManiFlow Policy的0.70±0.02），在DexArt上达到0.73±0.03（vs 0.70±0.03），在Bi-DexHands上达到0.67±0.05（vs 0.59±0.07）。Bi-DexHands上的提升最为显著（+0.08），这可能是因为双手操作任务涉及更多关节，结构中心表示的优势在高自由度场景下更加突出。

**Table 6** 报告了真实世界6个双手操作任务的结果。SAT在域内演示设置下优于所有基线，验证了结构中心表示从仿真到真实环境的迁移能力。定性结果（Figure 7）展示了策略执行复杂双手任务的完整过程。

### 消融实验与分析

**结构中心 vs 时间中心表示。** Table 4的模型组件消融显示，将结构中心表示改回传统时间中心表示（temporal-centric action）导致成功率从0.71下降至0.64，直接验证了结构中心视角对于高自由度灵巧操作的核心价值。

**Embodied Joint Codebook的关键作用。** 移除Embodied Joint Codebook（关节嵌入）导致成功率断崖式下降——从0.71骤降至0.01（Table 4）。这一灾难性失败的根本原因是：结构中心视角下的动作序列本质上是无序的关节轨迹集合，没有代码本提供的结构先验，Transformer无法确定哪条轨迹对应哪个物理关节，学习任务变得不可能。Table 5进一步消融了代码本的三个组件：移除功能类别（Functional Category）导致灾难性失败，表明功能对应是跨形态迁移最重要的先验；移除旋转轴（Rotation Axis）和形态ID（Embodiment ID）也带来明显下降，三者共同构成了必要的结构先验。

**预训练数据组成。** Table 3的预训练数据消融揭示了一个关键发现：仅使用人类数据预训练的成功率（0.68±0.04）超过了仅使用机器人数据预训练（0.66±0.05），而人类+机器人混合预训练达到最优（0.71±0.04）。这一结果证实Embodied Joint Codebook中的功能类别成功建立了人手关节与机器人灵巧手关节之间的对应关系，使得从人手数据学到的技能可以迁移到机器人平台。

**时序压缩的鲁棒性。** Table 2探索了动作token维度d_feat（即将每个关节的时序轨迹T压缩后的嵌入维度）的影响。从256维降至32维，成功率基本保持在0.71；仅在降至16维时才降至0.66。这表明关节的时序轨迹高度冗余，可被大幅压缩，进一步验证了结构中心表示的高效性。

**代码本嵌入可视化。** Figure 6展示了学习到的Embodied Joint Codebook嵌入的T-SNE可视化。嵌入按形态ID、功能类别和旋转轴分别着色，呈现出清晰的聚类结构——功能类别形成的聚类最为紧凑，表明模型确实学到了跨形态的功能对应关系，而非简单地记忆形态ID。

**少样本适应效率。** Figure 4对比了SAT与UniAct基线在不同数量域内演示下的少样本适应效率。SAT在极低数据量下展现出更快的收敛速度和更高的渐近性能，这归因于结构中心表示和代码本先验使得策略在新形态上仅需学习关节轨迹的具体映射，而非从零构建整个动作空间。

### 失败模式与局限性

尽管SAT在整体上表现优越，分析中仍识别出以下失败模式：

1. **物理交互约束缺失。** 当前策略未显式建模物理交互约束，在遮挡严重或接触几何差异大的场景下可能失效。这在高精度抓取任务中尤为突出——策略可能生成运动学上合理的关节轨迹，但无法保证与物体的稳定接触。

2. **感知受限场景。** 使用单一固定相机进行双手操作时，存在严重的自遮挡问题，限制了3D感知的质量。这可能导致策略在需要精确空间推理的双边协调任务中出现失败。

3. **形态泛化边界。** 预训练数据主要来源于特定人手动作捕捉和部分仿真数据。对于完全未知的手部形态，自动生成有效的Embodied Joint Codebook仍然是一个开放问题——当前代码本依赖于对已知形态的统计先验（Figure 5展示了从10种常见灵巧手调查得出的关节类型频率分布）。

4. **离线学习的局限。** 动作表示目前仅用于离线模仿学习，尚未探索其在在线强化学习中的扩展性。在需要在线探索和试错的场景下，结构中心表示能否作为策略类提高探索效率仍需验证。

### 补充图表

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of our method against 2D (image-based) and 3D (point cloud-based) baselines on 11 dexterous manipulation tasks from the Adroit [55], DexArt [2], and Bi-DexHands [10] simulation benchmarks*

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/010_Table_4.jpg]]
*Table 4: Model component ablation. We analyze the impact of removing key architectural components on the average success rate*

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/008_Table_5.jpg]]
*Table 5: Ablation study on the components of the Embodied Joint Codebook. We report the average success rate after fine-tuning models with different codebook components ablated*

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/005_Table_3.jpg]]
*Table 3: Pre-training data ablation. We report the average success on simulation tasks after fine-tuning models pre-trained on different combinations of Human, Robot, and Simulation datasets*

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/006_Table_2.jpg]]
*Table 2: Ablation on temporal compression and token dimension. We vary the token dimension*

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/014_Table_6.jpg]]
*Table 6: Quantitative results on 6 real-world bimanual manipulation tasks. We compare our model against baselines using indomain demonstrations*

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative rollouts of our policy executing complex bimanual tasks in the real world*

![[assets/figures/papers/paper_list_l2043_https_arxiv_org_abs_2603_03960/figures/013_Figure_8.jpg]]
*Figure 8: Real-world experimental setup. (a) Our bimanual hardware setup. We collect demonstration data using a VR headset for teleoperation. (b) The set of diverse objects used in our real-world manipulation, requiring both precision and bimanual coordination*



## 定位与知识库关联

### 1. 与基线的对比定位

SAT 的核心创新在于将动作表示从**时间中心**（temporal-centric）重构为**结构中心**（structural-centric），这一视角转换使其在方法谱系中占据独特位置。传统灵巧操作策略，无论是基于 2D 图像的 **Diffusion Policy**（Zhao et al., 2023）和 **HPT**（Wang et al., NeurIPS 2024），还是基于 3D 点云的 **3D Diffusion Policy**（Ze et al., 2024）和 **3D ManiFlow Policy**（Yan et al., CoRL 2025），均将动作块视为固定维度的时间序列 `(T, D_a)`，其中每个时间步的动作向量是完整关节空间的整体快照。这种表示在面对不同形态的高自由度机械手时，序列长度 `D_a` 随形态变化而改变，导致模型无法原生处理跨形态异构性。

SAT 将动作块重构为 `(D_a, T)`——即变长、无序的关节轨迹序列，每个序列元素代表单个关节在时域上的完整轨迹。这一重构的关键因果机制在于：**Transformer 的自注意力机制天然适合处理变长序列，但前提是序列元素具有可区分的身份标识**。传统时间中心表示中，时间步的顺序由位置编码提供，而结构中心表示中关节轨迹是无序的，必须依赖额外的结构先验来建立元素间的对应关系。这正是 SAT 引入 **Embodied Joint Codebook** 的根本原因——通过形态学三元组（Embodiment ID, Functional Category, Rotation Axis）为每个关节赋予可学习的结构嵌入，使得 Transformer 能够识别哪个轨迹对应哪个物理关节，从而学习关节间的功能对应关系。

从生成模型的角度，SAT 采用连续时间标准化流（Flow Matching）替代扩散模型中常用的 DDPM/DDIM，仅需 1 NFE 即可生成动作块，在推理效率上具有优势。但这一选择并非核心区分因素——消融实验表明，若将结构中心表示换回时间中心表示，成功率从 0.71 降至 0.64，而 Flow Matching 本身仅是实现结构中心表示的一个高效载体。

### 2. 适用边界与局限

**形态覆盖的边界。** SAT 的 Embodied Joint Codebook 基于对 10 种常见灵巧手的关节类型频率分析（Figure 5）构建，其功能类别和旋转轴的先验来源于已知形态的统计归纳。对于完全未知的手部形态——尤其是关节类型超出代码本覆盖范围的新设计——代码本是否能自动泛化仍需验证。当前预训练数据主要来源于人手动作捕捉（HOI4D, Ego-Exo4D, ADT）和特定机器人平台（Fourier ActionNet, DexCap），对新形态的零样本迁移能力尚未经过系统测试。

**感知与交互的盲区。** 策略未显式建模物理交互约束（如接触力、摩擦锥），在遮挡严重或接触几何差异大的场景下可能失效。真实世界实验中，双边操作使用单一固定相机导致严重自遮挡（Figure 8），限制了 3D 感知质量。这是结构中心表示本身无法解决的感知瓶颈——动作表示的优越性无法弥补观测信息的缺失。

**学习范式的局限。** 当前 SAT 仅用于离线模仿学习，尚未探索在在线强化学习中的扩展性。结构中心表示是否可以作为策略类的通用表示以提高 RL 探索效率，仍是一个开放问题。此外，演示与执行平台之间的运动学或接触几何不匹配问题——例如人手演示到机器人执行的映射——目前依赖代码本中的功能对应来隐式处理，缺乏显式的运动学适配机制。

### 3. 在知识库中的定位与开放问题

SAT 在灵巧操作知识库中的核心贡献在于：**首次将动作表示从“时间序列建模”范式迁移到“关节序列建模”范式**，并通过结构代码本解决了由此引入的无序序列识别问题。这一贡献的通用性超越了具体的网络架构选择——消融实验表明，即使大幅压缩时间维度（从 256 到 32），成功率基本保持 0.71，说明关节轨迹在时域上高度冗余，结构中心表示成功地将学习压力从时间建模转移到关节间关系建模。

**跨形态迁移的证据链。** 仅使用人类数据预训练即可超越使用机器人数据预训练（0.68 vs 0.66），且移除功能类别会导致灾难性失败（Table 5），表明代码本中的功能对应——而非形态相似性——是跨形态迁移的关键机制。Figure 6 的 T-SNE 可视化进一步证实，学习到的嵌入按功能类别形成清晰聚类，而非按形态 ID 或旋转轴。

**开放问题：**
- 如何自动生成面向完全未知形态的 Embodied Joint Codebook，而不依赖人工统计先验？
- 结构中心表示能否与语言指令更灵活地结合，实现零样本组合任务？
- 在处理演示-执行平台运动学不匹配时，能否引入显式的运动学适配层以提升鲁棒性？



## 原文 PDF

![[paperPDFs/CVPR_2026/Structural_Action_Transformer_for_3D_Dexterous_Manipulation.pdf]]
