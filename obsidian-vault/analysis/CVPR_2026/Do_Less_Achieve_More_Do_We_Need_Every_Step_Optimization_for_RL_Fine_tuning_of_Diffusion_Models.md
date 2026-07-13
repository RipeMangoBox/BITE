---
title: "Do Less, Achieve More: Do We Need Every-Step Optimization for RL Fine-tuning of Diffusion Models?"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Do_Less_Achieve_More_Do_We_Need_Every_Step_Optimization_for_RL_Fine_tuning_of_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- Do_Less_Achieve_
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 自适应选择RL训练的去噪时间窗口：通过感知语义结构稳定性决定训练起点（t_start），并监测奖励增益饱和点决定训练终点（t_end），仅在高价值区间进行RL更新。
primary_logic: 去噪过程的不同阶段具有截然不同的结构和不确定性分布，RL训练仅在语义结构已初具雏形且奖励增益显著的中间阶段才能高效提升偏好对齐，同时避免前期噪声混淆和后期过度拟合。
claims:
- AdaScope adaptively identifies the optimal intervention timing for RL by perceiving the structural evolution and semantic consistency during denoising, and dynamically terminates...
- Figure 1 shows that early stages have chaotic structure and late stages have converging reward, while the moderate uncertainty stage corresponds to stable structure and improving...
- AdaScope improves performance by 66% while cutting computational cost by 59%.
- Our method consistently achieves superior overall performance among 13 metrics, with 12 top2 effectiveness.
---

# Do Less, Achieve More: Do We Need Every-Step Optimization for RL Fine-tuning of Diffusion Models?

> [!tip] 核心洞察
> 去噪过程的不同阶段具有截然不同的结构和不确定性分布，RL训练仅在语义结构已初具雏形且奖励增益显著的中间阶段才能高效提升偏好对齐，同时避免前期噪声混淆和后期过度拟合。

| 字段 | 内容 |
|------|------|
| 中文题名 | 少做多得：扩散模型RL微调是否需要每一步优化？ |
| 英文题名 | Do Less, Achieve More: Do We Need Every-Step Optimization for RL Fine-tuning of Diffusion Models? |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.15855) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | AdaScope |
| Dataset | Pick-a-pic + PickScore, 简单动物提示集 + PickScore, 简单动物提示集 + Aesthetic |

> [!tip] 效果简介
> - Pick-a-pic + PickScore 上，PickScore ↑ 23.01 vs 22.94 (TDPO) (+0.07)；Aesthetic Score ↑ 6.071 vs 5.991 (TDPO) (+0.08)；FID ↓ 85.37 vs 147.5 (DDPO) (-62.13)。
> - 简单动物提示集 + PickScore 上，达到 PickScore=22 所需时间 (小时) 5.37 (DDPO+Ours) vs 13.2 (DDPO) (-59.3%)。
> - 简单动物提示集 + Aesthetic 上，达到 Aesthetic=7 所需时间 (小时) 5.16 (DDPO+Ours) vs 12.3 (DDPO) (-58.0%)。

## 概要

扩散模型在文本到图像（T2I）生成中展现出卓越能力，但将其输出与人类偏好对齐仍面临显著挑战。强化学习（RL）微调是提升偏好对齐的主流范式，然而现有方法普遍存在一个被忽视的瓶颈：**最终奖励信号极度稀疏，早期去噪步骤缺乏有效引导，导致高方差和动作‑奖励错配；而晚期步骤奖励趋于饱和，继续训练易引发奖励黑客和过拟合**。将最终奖励均匀分配给所有去噪步骤的策略，既浪费计算资源，又损害生成质量与多样性。

针对上述问题，本文提出 **AdaScope**，一种自适应选择RL训练去噪时间窗口的方法。其核心洞察在于：去噪过程的不同阶段具有截然不同的语义结构和不确定性分布。早期阶段结构混沌、噪声主导，RL更新缺乏可靠信号；晚期阶段结构已收敛，奖励增益趋于零，继续优化只会导致过拟合。**仅当语义结构初具雏形且奖励增益显著的中间阶段，才是RL训练的高价值区间**。

AdaScope通过两个关键模块实现自适应区间选择：

- **语义结构感知器**：利用相邻步骤CLIP分数的变化率（$\Delta S_t$）判定语义结构是否趋于稳定，从而确定RL训练的起步时间 $t_{\text{start}}$。
- **偏好增益检测器**：监测去噪过程中的奖励增量趋势（$\Delta P_t$），当边际增益趋近于零时终止训练，确定 $t_{\text{end}}$。

该方法以插件形式嵌入现有扩散模型RL微调框架（如 **DDPO**、**DPOK**、**D3PO**、**TDPO**），仅修改RL训练区间，其余超参数与基线保持一致。

实验结果表明，AdaScope在多个维度上实现了“少做多得”：

- **效率提升**：在简单动物提示集上，达到 PickScore=22 仅需 5.37 小时，较 DDPO 的 13.2 小时**减少 59.3%** 的训练时间；达到 Aesthetic Score=7 仅需 5.16 小时，**减少 58.0%**（Table 1）。
- **质量提升**：在 Pick-a-pic + PickScore 基准上，AdaScope 在偏好得分（PickScore 23.01 vs. TDPO 22.94）、美学得分（Aesthetic Score 6.071 vs. TDPO 5.991）上均取得最优，同时 FID 从 DDPO 的 147.5 大幅降至 85.37（Table 3）。
- **综合优势**：在覆盖偏好、保真度、多样性和丰富度的 13 项指标中，AdaScope 取得 12 项 Top-2 表现（Table 3）。
- **鲁棒性与通用性**：在多种骨干模型（SDv1.4、SDv2.1、SDXL）、多种奖励目标（JPEG压缩率、不可压缩性、多目标组合）以及流匹配模型（SD3.5）和SDE模型上均一致有效（Figure 5、6、11）。

值得注意的是，AdaScope 在部分强骨干模型（如 SDXL）上改进幅度有限，这可能是由于预训练权重已具有较高的普适鲁棒性。此外，自适应区间选择目前依赖预训练 CLIP 和奖励模型，若下游奖励函数不可靠，可能误导区间决策，这一点需要在实际部署中加以验证。



### 扩散模型RL微调的核心瓶颈

扩散模型在文本到图像（T2I）生成中展现出卓越能力，但其输出与人类偏好之间仍存在显著差距。强化学习（RL）微调通过奖励信号引导模型向偏好方向优化，已成为弥合这一差距的主流范式。然而，该范式面临一个根本性困境：**奖励信号极度稀疏**——在T2I生成中，奖励只能在去噪完全完成后计算，无法为中间步骤提供任何反馈（Figure 3）。这种稀疏性迫使现有方法将最终奖励均匀回传至所有去噪步骤，导致三个关键问题：

1. **早期动作‑奖励错配**：去噪初期（高噪声阶段）的隐变量尚未形成可辨识的语义结构，此时将最终奖励归因于早期动作缺乏因果依据，引入高方差梯度，破坏策略梯度估计的稳定性。
2. **晚期奖励黑客与过拟合**：去噪后期，生成图像的结构已趋于稳定，奖励增益接近饱和。继续在此阶段训练不仅浪费计算资源，更易诱发奖励黑客（reward hacking）——模型学会利用奖励函数的漏洞而非真正提升生成质量。
3. **计算效率低下**：对整个去噪轨迹 $[0, T-1]$ 均匀应用RL更新，意味着大量计算被消耗在对最终奖励贡献微弱甚至有害的步骤上。

### 去噪过程的阶段性特征

Figure 1 通过三个维度的观测揭示了去噪过程的阶段性本质：

- **结构演进（∆ CLIP）**：早期步骤中，CLIP分数变化剧烈，表明语义结构正处于混沌形成期；中期变化趋于平缓，结构已初具雏形；晚期变化几乎停滞，结构收敛。
- **奖励目标（Reward Objective）**：早期奖励信号低且不稳定，中期持续攀升，晚期趋于饱和。
- **不确定性分数（Uncertainty Score）**：基于Lemma 1推导的时间步间相关系数 $ \mathrm{Corr}(\mathbf{x}_t^{r,(i)},\mathbf{x}_{t+\\tau}^{r,(j)}) $ 表明，去噪过程中的不确定性随步骤单调递减——早期高度不确定，中期处于中等水平，晚期几乎确定。

这三条曲线的交汇揭示了一个关键洞察：**仅在语义结构已稳定、奖励增益显著且不确定性适中的中间阶段（Figure 1红色区域），RL训练才能高效提升偏好对齐**。早期阶段的噪声混淆使梯度信号不可靠，晚期阶段的奖励饱和使更新徒劳甚至有害。

### 现有方法的缺口

当前主流RL微调方法——包括基于策略梯度的 **DDPO**、引入KL正则化的 **DPOK**、基于直接偏好优化的 **D3PO**，以及基于时间差异偏好优化的 **TDPO**——均采用“全轨迹均匀优化”策略，即对整个去噪链 $[0, T-1]$ 的每一步施加RL更新。这种“一刀切”的做法忽视了去噪过程的阶段性差异，造成：

- **资源浪费**：大量计算被分配给低价值步骤，限制了在有限算力下的优化效率。
- **质量损害**：早期高方差更新和晚期过拟合共同侵蚀生成质量，表现为FID恶化、多样性下降和奖励黑客现象。

### 本文动机：从“每一步优化”到“高价值区间优化”

上述分析指向一个自然的问题：**扩散模型RL微调是否真的需要每一步优化？** 本文的回答是否定的。核心动机在于：若能自适应地识别去噪过程中真正值得RL训练的时间窗口——即语义结构已成型且奖励增益尚未饱和的区间——便可以在显著降低计算成本的同时，规避早期错配和晚期过拟合，实现“少做多得”（Do Less, Achieve More）。

这一动机催生了 **AdaScope** 方法，其设计理念是：将RL训练从“全轨迹均匀分配”转变为“自适应区间聚焦”，通过感知去噪过程中的结构演化和奖励增益动态，为每张图像个性化地确定最优训练起止点。



## 核心方法与创新机理

扩散模型RL微调的核心瓶颈在于去噪过程不同阶段的结构与奖励特性高度异质，而现有方法对整条去噪轨迹施加均匀的RL更新，导致三重失效：**早期高方差**——去噪初期语义结构尚未形成，将最终奖励信号归因于随机噪声状态引发严重的动作‑奖励错配；**晚期奖励黑客**——去噪后期奖励趋于饱和，继续优化驱使模型过拟合奖励函数的捷径而非提升真实语义质量；**计算浪费**——大量训练消耗在无效的早期和晚期步骤上。Figure 1 直观展示了这一现象：早期阶段CLIP变化剧烈（结构混沌），晚期阶段奖励收敛（边际增益趋零），仅中间阶段同时具备稳定语义结构和持续改善的奖励信号。

AdaScope 的核心创新在于将“全轨迹均匀RL”转变为**自适应区间RL**，通过感知去噪过程中的结构演化和偏好增益动态，为每张图像个性化确定高价值训练窗口，从根本上解耦了上述三重失效。

### 关键改变槽位

**槽位一：RL训练区间**（`Sec. 3.4`）  
基线方法（DDPO、DPOK、D3PO、TDPO等）对整个去噪轨迹 $[0, T-1]$ 均匀应用RL更新。AdaScope 自适应识别最优起止点 $[t_{\text{start}}, t_{\text{end}}]$，仅在语义结构已初具雏形且奖励增益显著的区间进行训练，跳过早期混沌阶段和晚期饱和阶段。这一改变是方法的核心操作杠杆。

**槽位二：奖励分配策略**（`Sec. 3.2`）  
基线方法将最终奖励 $R_{\text{real}}$ 均匀分配给所有去噪步骤（公式5）。AdaScope 仅在选定的区间内利用奖励信号进行策略梯度估计，避免将稀疏的最终奖励错误归因于早期高噪声状态，从而提升梯度估计的稳定性。

**槽位三：训练终止条件**（`Sec. 3.4.2`）  
基线方法固定在最终去噪步骤 $T$ 结束优化。AdaScope 通过偏好增益检测器动态确定饱和点 $t_{\text{end}}$——当边际偏好增益 $\lim_{\Delta t \to 0} \frac{\Delta P_{t+\Delta t} - \Delta P_t}{\Delta t}$ 趋近于零时自动终止，防止过度优化和奖励黑客。

### 方法管道与决策逻辑

AdaScope 由三个松耦合模块构成，嵌入现有RL微调框架（如DDPO）作为即插即用插件：

1. **语义结构感知器**（`Sec. 3.4.1`）：利用相邻步骤CLIP分数的变化率 $\Delta S_t = f(\mathbf{x}_{t-1}) - f(\mathbf{x}_t)$ 判定语义结构是否稳定。当结构增益的二阶变化趋近于零（公式10），即语义结构已初步成形，此时确定RL起步时间 $t_{\text{start}}$。这一设计确保RL更新发生在有意义的语义空间而非噪声空间。

2. **偏好增益检测器**（`Sec. 3.4.2`）：监测相邻步骤奖励的增量 $\Delta P_t = g(\mathbf{x}_{t-1}) - g(\mathbf{x}_t)$。当偏好增益的二阶变化趋近于零（公式13），表明奖励优化已饱和，终止训练以确定 $t_{\text{end}}$。这一机制直接对抗奖励黑客：模型无法通过继续优化已收敛的奖励信号获取虚假提升。

3. **自适应范围选择器**（`Sec. 3.4`）：整合上述两个感知器，为每张图像动态输出个性化RL训练区间 $[t_{\text{start}}, t_{\text{end}}]$。区间长度随图像和提示自适应变化，而非固定超参数。

### 理论支撑

方法设计建立在两条理论观察之上：**前向‑逆向一致性定理**（Theorem 1）保证了前向扩散过程中的相关性结构可等价迁移到逆向生成过程，使得基于前向过程的分析可以指导逆向RL训练；**相关性单调递减引理**（Lemma 1）揭示了去噪过程中隐变量间的不确定性随步骤单调递减，为“早期高不确定性、晚期低不确定性”的区间划分提供了理论依据。Figure 1 中的不确定性分数曲线直接验证了这一理论预测。

### 创新边界与局限

AdaScope 的创新聚焦于**何时训练**而非**如何训练**，因此与具体RL算法解耦，可作为插件嵌入DDPO、DPOK、D3PO、TDPO等不同策略。但区间选择依赖预训练CLIP和奖励模型的质量：若下游奖励函数本身不可靠，感知器可能被误导，导致区间决策失准（需手动验证）。此外，在强骨干模型（如SDXL）上改进幅度有限，因其预训练权重已具有较高普适鲁棒性。



AdaScope 的核心设计理念是将扩散模型的去噪过程重新审视为一个具有阶段性结构演化的动态系统，而非均匀的马尔可夫链。基于这一视角，该方法构建了一个轻量级的自适应时间窗口选择器，嵌入到现有的扩散模型 RL 微调流程中，仅在高价值区间进行策略优化。

### 问题建模与 MDP 重构

扩散模型的去噪过程被形式化为一个马尔可夫决策过程（MDP）。在此框架下，状态 $\mathbf{s}_t$ 对应于当前噪声隐变量 $\mathbf{x}_t$ 与文本条件 $\mathbf{z}$ 的组合，动作 $\mathbf{a}_t$ 为去噪网络 $\epsilon_\theta$ 输出的噪声预测，而奖励信号则来自最终生成图像 $\mathbf{x}_0$ 经过奖励模型 $r(\mathbf{x}_0, \mathbf{z})$ 评估的结果。现有方法将这一最终奖励 $R_{\mathrm{real}}$ 均匀分配给所有 $T$ 个去噪步骤：

$$R_{\mathrm{real}}(\mathbf{s}_t,\mathbf{a}_t) \triangleq r(\mathbf{x}_0,\mathbf{z}), \quad \forall t \in \{0,1,\dots,T-1\}$$

这种全局均匀分配策略是导致早期步骤高方差更新和晚期步骤奖励黑客的根本原因。AdaScope 的关键改造在于：**不再对所有步骤施加 RL 更新**，而是通过两个感知器动态确定每张图像的最优训练区间 $[t_{\mathrm{start}}, t_{\mathrm{end}}]$，仅在区间内利用奖励信号进行策略梯度估计。

### 三模块协同架构

AdaScope 的整体框架由三个功能模块串联构成，如 Figure 2 所示，它们嵌入在去噪轨迹与 RL 优化器之间：

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of our method*

**1. 语义结构感知器（Semantic Structure Perceptor）**  
该模块负责确定 RL 训练的起点 $t_{\mathrm{start}}$。其核心假设是：RL 训练应在语义结构已初步形成、不再剧烈变化的阶段开始，否则早期噪声主导的步骤会引入严重的动作-奖励归因错配。具体而言，感知器利用 CLIP 分数在相邻步骤间的变化率 $\Delta S_t$ 来衡量结构演化速度：

$$\Delta S_t = f(\mathbf{x}_{t-1}) - f(\mathbf{x}_t), \quad f(\mathbf{x}_t) \triangleq \mathrm{CLIP}(\hat{\mathbf{x}}_0(\mathbf{x}_t), \mathbf{z})$$

其中 $\hat{\mathbf{x}}_0(\mathbf{x}_t)$ 是从当前噪声状态一步估计的清晰图像。当 $\Delta S_t$ 的二阶变化趋近于零时，表明语义结构已趋于稳定，此时的时间步被选为 $t_{\mathrm{start}}$：

$$t_{\mathrm{start}} = \min\{t \mid |\lim_{\Delta t \to 0} \frac{\Delta S_{t+\Delta t} - \Delta S_t}{\Delta t}| < 0\}$$

**2. 偏好增益检测器（Preference Gain Detector）**  
该模块负责确定 RL 训练的终点 $t_{\mathrm{end}}$。其核心观察是：去噪后期奖励函数趋于饱和，继续训练不仅无益，反而会诱发过拟合和多样性丧失。检测器通过监测奖励函数在相邻步骤间的增量 $\Delta P_t$ 来判断优化是否已收敛：

$$\Delta P_t = g(\mathbf{x}_{t-1}) - g(\mathbf{x}_t), \quad g(\mathbf{x}_t) \triangleq \mathrm{Reward}(\hat{\mathbf{x}}_0(\mathbf{x}_t), \mathbf{z})$$

当 $\Delta P_t$ 的二阶变化趋近于零时，说明偏好增益已饱和，此时终止训练：

$$t_{\mathrm{end}} = \min\{t \mid |\lim_{\Delta t \to 0} \frac{\Delta P_{t+\Delta t} - \Delta P_t}{\Delta t}| < 0\}$$

**3. 自适应范围选择器（Adaptive Scope Selector）**  
该模块整合上述两个感知器的输出，为每张图像动态生成个性化的 RL 训练区间 $[t_{\mathrm{start}}, t_{\mathrm{end}}]$。区间之外的时间步不参与策略梯度计算，从而在根本上避免了早期噪声混淆和晚期过拟合。

### 数据流与控制流

在一次典型的 RL 微调迭代中，数据流如下：

1. **去噪采样**：从纯噪声 $\mathbf{x}_T$ 开始，按照 DDIM 采样过程逐步去噪，同时记录每个时间步的隐变量 $\mathbf{x}_t$。
2. **区间感知**：在采样过程中，语义结构感知器实时计算 $\Delta S_t$，一旦检测到结构稳定即标记 $t_{\mathrm{start}}$；随后偏好增益检测器持续监测 $\Delta P_t$，在增益饱和时标记 $t_{\mathrm{end}}$。
3. **选择性优化**：仅对区间 $[t_{\mathrm{start}}, t_{\mathrm{end}}]$ 内的状态-动作对计算策略梯度并更新模型参数，区间外的步骤被完全跳过。
4. **宿主方法兼容**：AdaScope 以插件形式工作，不修改宿主 RL 方法（如 DDPO、DPOK、D3PO、TDPO）的损失函数或优化器，仅控制哪些时间步参与梯度回传。

### 与基线方法的接口关系

AdaScope 的“即插即用”特性使其可以无缝嵌入多种主流扩散模型 RL 微调基线。在实验中，它被部署为以下四种方法的插件：

- **DDPO**：基于策略梯度的 RL 微调基线，AdaScope 限制其去噪轨迹上的策略更新范围。
- **DPOK**：引入 KL 正则化的 RL 微调基线，AdaScope 同样作用于其训练区间。
- **D3PO**：基于直接偏好优化的微调基线，AdaScope 控制其偏好学习的时间窗口。
- **TDPO**：基于时间差异偏好优化的微调基线，AdaScope 进一步精细化其时间步选择。

在所有宿主方法中，AdaScope 仅修改 RL 训练区间这一单一维度，其余超参数（学习率、批量大小、KL 系数等）均保持与原始方法一致，确保了公平比较。



### 3.1 扩散模型RL微调的形式化瓶颈

在文本到图像（T2I）扩散模型的RL微调中，去噪过程被形式化为一个马尔可夫决策过程（MDP）。轨迹定义为 $\tau_{\mathrm{MDP}} = (\mathbf{s}_0, \mathbf{a}_0, r_0, \mathbf{s}_1, \mathbf{a}_1, r_1, \dots, \mathbf{s}_T, r_T)$，其中状态 $\mathbf{s}_t$ 为当前噪声隐变量 $\mathbf{x}_t$ 与文本条件 $\mathbf{z}$ 的组合，动作 $\mathbf{a}_t$ 为去噪网络 $\epsilon_\theta$ 输出的噪声预测。然而，真实的偏好奖励信号 $r(\mathbf{x}_0, \mathbf{z})$ 仅在最终清晰图像 $\mathbf{x}_0$ 生成后才能计算，导致奖励极度稀疏（Figure 3）。

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/003_Figure_3.jpg]]
*Figure 3: In T2I generation, rewards can only be computed after denoising is fully completed, resulting in extremely sparse feedback that cannot support stable training (see the dashed curves)*

现有方法（如DDPO、DPOK、D3PO、TDPO）将最终奖励均匀分配给所有去噪步骤：

$$R_{\mathrm{real}}(\mathbf{s}_t, \mathbf{a}_t) \triangleq r(\mathbf{x}_0, \mathbf{z}), \quad \forall t \in \{0, 1, \dots, T-1\}$$

这种均匀分配策略存在两个根本性缺陷：**早期步骤**中语义结构尚未形成，噪声占主导地位，奖励信号无法有效归因于具体动作，导致高方差梯度估计和动作-奖励错配；**晚期步骤**中图像结构已趋于收敛，奖励增益趋于饱和，继续训练将引发奖励黑客（reward hacking）和过拟合，损害生成多样性（Figure 1中绿色曲线所示）。

### 3.2 核心理论支撑：前向-反向一致性

为分析去噪过程中隐变量间的结构演化规律，论文建立了前向扩散过程与反向生成过程之间的等价关系。

**定理1（前向-反向一致性）**：前向过程与反向生成过程中，任意两时间步隐变量的联合分布相等：

$$p(\mathbf{x}_t^f, \mathbf{x}_{t+\tau}^f) = p(\mathbf{x}_t^r, \mathbf{x}_{t+\tau}^r)$$

基于此定理，可通过解析前向过程的相关性来刻画反向去噪过程中的语义结构稳定性。时间步间相关系数的解析表达式为：

$$\mathrm{Corr}(\mathbf{x}_t^{r,(i)},\mathbf{x}_{t+\tau}^{r,(j)}) = \frac{\sqrt{\bar{\alpha}_{t+\tau}\bar{\alpha}_t}\Sigma_{ij} + \sqrt{\frac{\bar{\alpha}_{t+\tau}}{\bar{\alpha}_t}}(1-\bar{\alpha}_t)\delta_{ij}}{\sqrt{(\bar{\alpha}_t\Sigma_{ii}+(1-\bar{\alpha}_t))(\bar{\alpha}_{t+\tau}\Sigma_{jj}+(1-\bar{\alpha}_{t+\tau}))}}$$

该公式表明，随着 $t$ 减小（即越接近清晰图像），$\bar{\alpha}_t$ 增大，隐变量间的相关性增强，结构不确定性单调递减。这为自适应选择RL训练区间提供了理论依据：**仅当语义结构已初具雏形且不确定性适中时，RL更新才具有高效的信息增益**。

### 3.3 核心模块一：语义结构感知器

语义结构感知器负责确定RL训练的起始时间步 $t_{\mathrm{start}}$。其核心思想是：当去噪过程中相邻步骤的语义结构变化率趋于稳定时，说明图像的主要语义结构已经形成，此时介入RL训练可以避免早期噪声混淆。

首先，通过一步估计从噪声隐变量 $\mathbf{x}_t$ 恢复清晰图像 $\hat{\mathbf{x}}_0$：

$$\hat{\mathbf{x}}_0(\mathbf{x}_t, t) = \frac{1}{\sqrt{\bar{\alpha}_t}}\left(\mathbf{x}_t - \sqrt{1-\bar{\alpha}_t}\epsilon_\theta(\mathbf{x}_t, t)\right)$$

然后，定义相邻步骤的**结构增益** $\Delta S_t$ 为CLIP语义对齐分数的变化：

$$\Delta S_t = f(\mathbf{x}_{t-1}) - f(\mathbf{x}_t), \quad f(\mathbf{x}_t) \triangleq \mathrm{CLIP}(\hat{\mathbf{x}}_0(\mathbf{x}_t), \mathbf{z})$$

当 $\Delta S_t$ 的变化率趋近于零时，表明语义结构已趋于稳定，此时的时间步即为RL训练的起点：

$$t_{\mathrm{start}} = \min\{t \mid |\lim_{\Delta t \to 0} \frac{\Delta S_{t+\Delta t} - \Delta S_t}{\Delta t}| < 0\}$$

### 3.4 核心模块二：偏好增益检测器

偏好增益检测器负责确定RL训练的终止时间步 $t_{\mathrm{end}}$。其核心思想是：当去噪过程中奖励信号的边际增益趋于饱和时，继续训练不仅无法有效提升偏好对齐，还会引发奖励黑客和过拟合。

定义相邻步骤的**偏好增益** $\Delta P_t$ 为奖励模型评分的变化：

$$\Delta P_t = g(\mathbf{x}_{t-1}) - g(\mathbf{x}_t), \quad g(\mathbf{x}_t) \triangleq \mathrm{Reward}(\hat{\mathbf{x}}_0(\mathbf{x}_t), \mathbf{z})$$

当偏好增益的变化率趋近于零时，表明奖励优化已进入饱和区，此时应终止RL训练：

$$t_{\mathrm{end}} = \min\{t \mid |\lim_{\Delta t \to 0} \frac{\Delta P_{t+\Delta t} - \Delta P_t}{\Delta t}| < 0\}$$

### 3.5 自适应范围选择器的整合机制

自适应范围选择器整合上述两个感知器的输出，为每张图像动态确定个性化的RL训练区间 $[t_{\mathrm{start}}, t_{\mathrm{end}}]$。该区间恰好对应于Figure 1中的红色区域——语义结构已稳定形成（$\Delta S_t$ 稳定）且奖励增益显著（$\Delta P_t$ 未饱和）的中间去噪阶段。

在此区间内，RL策略梯度仅作用于高价值状态，自动过滤掉早期结构混沌和晚期奖励收敛的无效更新。这种选择性训练策略从根本上缓解了均匀奖励分配导致的动作-奖励错配和奖励黑客问题，实现了“少步多获”的质量-效率双优化。

### 补充图表

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/001_Figure_1.jpg]]
*Figure 1: We plot the CLIP variation (∆ CLIP), Reward Objective, and Uncertainty Score (Based on Lemma 1) with aligned denoising steps. Only the red region is optimized, where we leverage ∆ CLIP and Reward to select the adaptive scope of denoising steps for training. It can be observed that the structure is chaotic in the first stage, while the reward converges in the last stage. The selected scope has a stable structure and improving reward, which exactly corresponds to the moderate uncertainty stage*



## 实验与关键发现

### 核心定量结果

**Table 3** 汇总了以 SDv1.5 为骨干、Pick‑a‑pic 为提示集、PickScore 为训练奖励的 13 项指标全面对比。AdaScope 在其中 12 项指标上取得 Top‑2 表现，体现了跨偏好、保真度、多样性和丰富度的综合优势。在 PickScore 上，AdaScope 达到 23.01，略优于 TDPO 的 22.94（+0.07）；在 Aesthetic Score 上达到 6.071，同样超过 TDPO 的 5.991（+0.08）。更为显著的是 FID 指标：AdaScope 将 FID 从 DDPO 的 147.5 降至 85.37（−62.13），表明生成分布与真实图像分布的对齐程度大幅改善。

### 效率与样本利用率

**Table 1** 展示了 AdaScope 作为插件植入 DDPO、DPOK、D3PO 和 TDPO 四种基线后的效率收益。以 DDPO 为例，每批耗时从 4.55 分钟降至 2.65 分钟；在简单动物提示集上达到 PickScore=22 所需时间从 13.2 小时缩短至 5.37 小时（−59.3%），达到 Aesthetic=7 所需时间从 12.3 小时缩短至 5.16 小时（−58.0%）。**Figure 4** 从样本效率角度进一步验证：在 PickaPic 和 HPSv2 两个提示集上，给定相同优化样本数，AdaScope 始终获得更高的 PickScore 和 Aesthetic Score，印证了“少步多获”的核心主张。

### 消融实验

**Figure 7** 与 **Table 2** 联合呈现消融分析。消融变体 V1 采用固定均值范围，V2 仅使用自适应起点（固定终点），V3 仅使用自适应终点（固定起点）。结果显示，自适应起止步选择在相近计算成本下获得更高的奖励得分；固定起始步或结束步均导致性能下降，说明训练区间需要针对每个提示进行自适应调整。动态范围选择能够有效缓解早期奖励归因错配和晚期过拟合，是实现质量‑效率双优化的关键。

### 泛化性与鲁棒性

**Figure 5** 展示了骨干迁移实验：在 SDv1.4、SDv2.1 和 SDXL 上 AdaScope 均取得最佳性能。SDXL 上提升幅度较小，论文归因于该骨干参数规模大、预训练权重本身具有较高普适鲁棒性。**Figure 6** 展示了奖励目标迁移实验：在 JPEG 压缩率、不可压缩性、AES+PS 等多目标奖励下，AdaScope 一致超越基线，表明自适应区间选择对不同奖励函数具有良好的泛化能力。**Figure 11** 进一步将方法扩展至流匹配模型（SD3.5）和经典 SDE 模型，验证了 AdaScope 不局限于 DDPM 类扩散框架。

### 奖励黑客缓解与多样性保持

**Figure 8** 通过 2D/1D 特征投影可视化生成图像分布，表明 AdaScope 有效缓解了奖励黑客问题，输出分布保持更丰富的多样性。**Figure 13** 的定性对比佐证了这一结论：AdaScope 在姿势、色彩、风格上变化最为丰富，而 D3PO 常产生灰度背景，DPOK 偏好紫色调，DDPO 易出现拼贴构图。**Figure 12** 的主观评估中，人类与 VLM 在结构忠实度、美学质量、细节、语义对齐和提示响应性五个维度上的评分均支持 AdaScope 的优越性。

### 语义对齐视觉验证

**Figure 9** 展示了组合、计数、颜色和空间布局四类语义对齐的视觉结果，AdaScope 生成的图像对提示的忠实度明显优于基线。**Figure 10** 展示了复杂未见提示的生成示例，体现了方法的泛化能力。

### 局限性与待验证点

论文自述在部分强骨干模型（如 SDXL）上改进幅度有限。此外，自适应区间选择目前依赖预训练 CLIP 和奖励模型，若下游奖励函数不可靠是否会误导区间决策，仍需手动验证。方法在更长去噪链（如 1000 步）的高分辨率生成中是否需要额外尺度适配，以及能否推广至视频扩散或三维生成任务，均为开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/004_Table_1.jpg]]
*Table 1: Improving efficiency by deploying our method as a plugin. Time-PB refers to the time consumption per batch (minutes). Top-1 refers to the number of Best results for each method. The time taken to reach a specific reward score is measured in hours. Bold refers to the metric improved with Ours*

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/005_Figure_4.jpg]]
*Figure 4: Sample efficiency for objective optimization. We present the results on PickaPic and HPSv2 prompt set with rewards PickScore and Aesthetic Score*

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/006_Figure_5.jpg]]
*Figure 5: Results on more different SD backbones. Notably, the less promising results on SDXL may be due to the inherent robustness of the backbone with a large number of parameters. Still, our method can leverage samples and different denoising states more effectively and thus achieve the best performance*

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/007_Figure_6.jpg]]
*Figure 6: Results with multiple different reward objectives, including the multi-objective reward like AES+PS, which is accumulated and re-normalized as a combined objective*

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/008_Figure_7.jpg]]
*Figure 7: Optimization performance for Ablation Study*

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/013_Table_3.jpg]]
*Table 3: Quantitative comparisons with SoTA. All metrics are obtained with SDv15 as backbone, Pick-a-pic as prompt set, and PickScore as training reward*

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/011_Figure_8.jpg]]
*Figure 8: Visualized Generated Image Distribution. We further reduce the dimension to 1-D (right) for a more direct impression*

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/014_Figure_11.jpg]]
*Figure 11: Left: Results on Flow-Matching Model. Right: on SDE Model*

![[assets/figures/papers/paper_list_l2672_https_arxiv_org_abs_2605_15855/figures/017_Figure_13.jpg]]
*Figure 13: Diversity Evaluation: Our method demonstrates the highest level of variation under these prompts, producing outputs with a wide range of artistic styles, figure posture, object positioning, and background colors. In contrast, D3PO predominantly generates grayscale backgrounds or same posture, DPOK consistently incorporates purple tones into its visual style, and DDPO tends to produce collage-like compositions within a single image*



## 定位与知识库关联

### 核心瓶颈与设计动机

扩散模型RL微调面临一个根本性的效率-质量矛盾：最终奖励信号只能在完全去噪后获得（Figure 3），而现有方法将这一稀疏奖励均匀分配给所有去噪步骤。这种“均匀分配”策略在两个方向上同时失效——早期步骤（高噪声阶段）语义结构尚未形成，奖励归因存在严重的动作-奖励错配，导致策略梯度估计方差极高；晚期步骤（接近收敛阶段）奖励增益趋于饱和，继续训练不仅浪费计算资源，还会诱发奖励黑客和过拟合。Figure 1通过CLIP变化量、奖励目标和不确定性分数三条曲线的同步演化，直观揭示了这一现象：只有中间区域的“适度不确定性”阶段同时具备稳定的语义结构和持续的奖励增益。

AdaScope的设计正是围绕这一瓶颈展开：将“全轨迹均匀RL”替换为“自适应区间RL”，通过感知去噪过程中的语义结构稳定性和偏好增益饱和点，动态决定每张图像的个性化训练起止点。

### 方法谱系定位

AdaScope并非一个独立的RL微调算法，而是一种**训练区间选择策略**，以插件形式嵌入现有RL微调框架。论文验证了四种宿主方法：

- **DDPO**：基于策略梯度的扩散模型RL微调基线，是最早将去噪过程形式化为MDP并应用PPO的工作之一。
- **DPOK**：在DDPO基础上引入KL正则化，约束微调后的分布与预训练模型的偏离程度。
- **D3PO**：基于直接偏好优化的扩散微调方法，绕过显式奖励建模，直接从人类偏好对中学习。
- **TDPO**：基于时间差异偏好优化的微调方法，在去噪时间维度上引入偏好比较。

AdaScope与上述方法的关系是**正交互补**的：它不修改奖励函数设计、策略梯度估计器或KL正则化项，仅改变“哪些去噪步骤参与RL更新”。Table 1和Table 3的证据表明，这种正交性使得AdaScope能够一致地提升所有宿主方法的效率和质量。

### 关键设计决策与替代方案对比

AdaScope的核心设计决策体现在三个“变更槽位”上：

**1. RL训练区间：从全轨迹 [0, T-1] 到自适应 [t_start, t_end]**

这一变更是AdaScope的核心贡献。消融实验（Table 2, Figure 7）系统比较了四种区间选择策略：
- **V1（固定均值区间）**：对所有图像使用相同的起止步，计算成本与AdaScope相近，但奖励得分显著低于自适应选择，说明不同提示的去噪动态存在显著差异。
- **V2（仅自适应起点）**：固定结束步为T-1，仅根据语义结构感知器决定t_start。性能下降表明晚期过拟合问题同样需要针对性处理。
- **V3（仅自适应终点）**：固定起始步为0，仅根据偏好增益检测器决定t_end。性能下降表明早期高方差更新对训练的破坏性不容忽视。
- **AdaScope（完整自适应）**：同时自适应起止步，在相近计算成本下获得最优奖励得分。

**2. 奖励分配策略：从均匀分配到区间内分配**

AdaScope并非重新设计奖励函数，而是通过区间选择间接实现了奖励信号的“质量过滤”——仅在语义结构已初具雏形且奖励增益显著的步骤内利用奖励信号。这一策略的理论基础来自Theorem 1（前向-逆向一致性）和Lemma 1（不确定性单调递减），它们共同保证了去噪过程中隐变量相关性的解析可追踪性，从而使得基于CLIP和奖励模型的启发式感知器具有理论支撑。

**3. 训练终止条件：从固定终止到动态饱和检测**

偏好增益检测器（Eq. 11-13）通过监测相邻步骤奖励变化的二阶导数趋近于零来判断偏好优化是否饱和。这一机制自动防止了晚期阶段的低收益训练和奖励黑客——Figure 8的生成图像分布可视化表明，AdaScope相比基线方法更好地保持了输出多样性，未出现模式坍塌。

### 适用边界与局限性

**已验证的适用范围：**
- **骨干模型**：Stable Diffusion v1.4、v1.5、v2.1、SDXL，以及Flow-Matching模型（SD3.5）和经典SDE模型（Figure 5, Figure 11）。
- **奖励目标**：PickScore、Aesthetic Score、JPEG压缩率、不可压缩性、多目标组合奖励（Figure 6）。
- **评估维度**：13项指标覆盖偏好对齐、保真度、多样性和语义丰富度（Table 3）。

**已知局限：**
- 在SDXL等大参数量骨干模型上改进幅度有限（Figure 5标题明确指出），因为预训练权重已具有较高的普适鲁棒性，RL微调的边际收益本身较小。
- 区间选择依赖预训练CLIP和奖励模型的质量。若下游奖励函数本身不可靠（例如与人类偏好相关性低），语义结构感知器和偏好增益检测器的判断可能被误导。这一问题在论文中未被实验验证，需要使用者注意。

### 开放问题与未来方向

1. **感知器的鲁棒性边界**：当前t_start和t_end的判定依赖启发式阈值（二阶导数趋近于零），在奖励函数噪声较大或CLIP表征能力不足的场景下，阈值选择是否仍然可靠？是否可以通过学习而非启发式来预测最优区间？

2. **跨模态与跨任务泛化**：AdaScope的阶段性感知逻辑——识别“结构形成”和“增益饱和”两个关键转折点——在视频扩散模型（时间维度的去噪）或三维生成任务（空间维度的去噪）中是否同样适用？这需要验证去噪动态的结构相似性。

3. **高分辨率与长链适配**：当前实验基于DDIM的50步采样。在具有更长去噪链（例如1000步）的高分辨率生成中，语义结构稳定和偏好增益饱和的时间尺度可能发生变化，区间选择策略是否需要额外的尺度适配机制？

4. **与奖励塑形的深度结合**：AdaScope目前仅通过区间选择间接改善奖励信号质量。如果能与中间步骤的辅助奖励塑形（例如基于CLIP的中间步骤语义奖励）结合，或许能进一步扩大有效训练区间的范围，提升样本效率。



## 原文 PDF

![[paperPDFs/CVPR_2026/Do_Less_Achieve_More_Do_We_Need_Every_Step_Optimization_for_RL_Fine_tuning_of_Diffusion_Models.pdf]]
