---
title: "Policy Contrastive Decoding for Robotic Foundation Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Policy_Contrastive_Decoding_for_Robotic_Foundation_Models.pdf
project_link: https://koorye.github.io/PCD
code_link: null
openreview_forum_id: P9PVdWyM3U
aliases:
- PCDP
- PCDRFM
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "通过对比原始观测与物体掩码观测下的动作概率分布，利用放大系数 α（式2）和物体掩码精确度来控制策略对物体相关特征的敏感度，从而抑制虚假特征的干扰。"
primary_logic: "通过一种即插即用、无需训练的对比解码机制，在推理时直接对比原始和物体掩码输入下的策略输出，将机器人的注意力从虚假特征重定向到任务相关物体特征，有效提升跨场景的泛化能力。"
claims:
- "PCD 在9项模拟任务上平均将 OpenVLA 的成功率从 16.8% 提升至 25.3%（相对提升 50.6%）。"
- "在真实世界实验中，PCD 使 π0 的成功率平均提升 108%，仅增加 24% 的时间开销。"
- "消融实验表明 PCD 对不同的目标检测模型（Grounding DINO 等）和修复策略不敏感，表现稳定。"
- "在掩盖像素比例达 60% 时 PCD 性能才退化至基线水平，展示了对不完美掩码的鲁棒性。"
---

# Policy Contrastive Decoding for Robotic Foundation Models

> [!tip] 核心洞察
> 通过一种即插即用、无需训练的对比解码机制，在推理时直接对比原始和物体掩码输入下的策略输出，将机器人的注意力从虚假特征重定向到任务相关物体特征，有效提升跨场景的泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向机器人基础模型的策略对比解码 |
| 英文题名 | Policy Contrastive Decoding for Robotic Foundation Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=P9PVdWyM3U) · [Project](https://koorye.github.io/PCD) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Policy Contrastive Decoding (PCD) |
| Dataset | SIMPLER (9 tasks), Real-world (6 manipulation tasks) |

> [!tip] 效果简介
> - SIMPLER (9 tasks) 上，Success Rate 为 25.3±1.6，对比 16.8±1.4，变化 +50.6% (relative)。
> - SIMPLER (9 tasks) 上，Success Rate 为 17.9±1.4，对比 13.8±1.3，变化 +29.7% (relative)。
> - SIMPLER (9 tasks) 上，Success Rate 为 69.6±1.7，对比 63.9±1.8，变化 +8.9% (relative)。

## 概要

现有机器人基础模型（如 OpenVLA、Octo、π0）在预训练过程中容易从观测中学习到任务无关的视觉特征（如背景、光照、物体姿态）与动作之间的**虚假相关性**。当测试环境发生分布偏移时——例如仅改变光源位置或抽屉把手方向——这些虚假相关性会导致策略成功率大幅下降（Figure 1 显示 OpenVLA 分别下降 36% 和 32%），严重制约了策略的跨场景泛化能力。

针对上述瓶颈，本文提出 **Policy Contrastive Decoding (PCD)**，一种**即插即用、无需训练**的对比解码方法。其核心思路是：在推理时，通过对比原始观测与物体掩码观测下的动作概率分布，将机器人的注意力从虚假特征重定向到任务相关物体特征，从而抑制虚假相关性的干扰。PCD 将策略模型视为黑盒，无需访问模型权重或进行微调，可通用于自回归策略和扩散策略。

为支撑对比解码，PCD 包含两个配套模块：**Track2Mask** 利用 SAM2 对目标物体进行自动跟踪与掩码生成；**KDE-PM** 通过核密度估计为扩散策略提供动作概率密度近似。

实验表明，PCD 在跨策略、跨场景的设置下均取得显著提升：
- 在 **SIMPLER 模拟环境**的 9 项任务上，PCD 将 OpenVLA 的成功率从 16.8% 提升至 25.3%（相对提升 50.6%），将 Octo 从 13.8% 提升至 17.9%（+29.7%），将 π0 从 63.9% 提升至 69.6%（+8.9%）（Table 1）。
- 在**真实世界**的 6 项操作任务中，PCD 使 π0 的平均成功率相对提升 **108%**，仅增加约 24% 的时间开销（Figure 3）。
- 消融实验进一步表明，PCD 对不同的目标检测模型和物体修复策略表现出低敏感性，且对不完美掩码（掩码像素缺失比例达 60%）仍保持一定鲁棒性。

PCD 的主要局限在于两次前向传播导致推理延迟约翻倍，且其效果依赖于目标检测与分割模型的精度；在检测失败或不完整掩码情况下可能退化至基线水平。该方法定位于**测试时后验纠正**，与 Classifier-Free Guidance (CFG) 等隐式引导方法形成互补。



机器人基础模型近年来取得了显著进展，大规模预训练使通用策略（如 OpenVLA、Octo、π0）能够在多种操作任务中展现出令人瞩目的泛化能力。然而，这些策略在实际部署中面临一个关键瓶颈：**预训练过程中容易从观测中学习到任务无关的视觉特征与动作之间的虚假相关性**。

具体而言，现有机器人策略往往将背景纹理、光照条件、物体摆放位置等非因果特征与正确动作建立统计关联。当测试环境发生分布偏移时——例如改变光源位置或抽屉把手位置——这些虚假相关性会导致策略泛化性能急剧下降。Figure 1 中的实验表明，仅改变光照位置即导致 OpenVLA 基线策略的性能下降 36%，改变把手位置则造成 32% 的性能损失。注意力图可视化进一步揭示，策略的视觉注意力常集中于光源、机械臂本体等与任务目标无关的区域，而非操作对象本身。

现有的应对策略存在明显局限。基于微调的方法需要额外数据和计算资源，且可能损害预训练策略的通用能力；数据增强技术难以穷举所有可能的分布偏移类型；而 Classifier-Free Guidance（CFG）等隐式引导方法虽能改善生成质量，却无法显式地将策略注意力重定向至任务相关物体。

上述缺口催生了一个核心问题：**能否设计一种无需训练、即插即用的推理时校正机制，在不修改模型权重的前提下，将机器人策略的注意力从虚假特征重新引导至物体相关特征？** 这正是 Policy Contrastive Decoding（PCD）方法的出发点——通过对比原始观测与物体掩码观测下的动作概率分布，抑制虚假特征的干扰，从而提升策略在未见场景下的泛化能力。



## 核心方法与创新机理

### 问题瓶颈：从虚假相关到因果解耦

现有机器人基础模型（如 **OpenVLA** (Kim et al., 2024)、**Octo** (Team et al., 2024)、**π0** (Black et al., 2024)）在预训练过程中，容易从观测中学习到任务无关的视觉特征（如背景纹理、光照位置、物体摆放姿态）与动作之间的**虚假相关性**。当测试环境发生分布偏移时——例如改变光源位置或抽屉把手位置——这些虚假相关性会导致策略泛化性能急剧下降。Figure 1 的注意力图直观展示了这一点：基线策略的注意力热区集中在台灯光源和机械臂本体上，而非任务目标物体（可乐罐），这直接解释了光照位置变化导致 OpenVLA 性能下降 36%、把手位置变化导致性能下降 32% 的现象。

### 核心洞察：测试时对比解码重定向注意力

PCD 的核心创新在于提出一种**即插即用、无需训练**的对比解码机制，在推理时直接对比原始观测与物体掩码观测下的策略输出，将机器人的注意力从虚假特征重定向到任务相关物体特征。其关键逻辑链条如下：

1. **因果调控旋钮**：通过对比原始观测 $\mathbf{o}_i$ 与物体掩码观测 $\hat{\mathbf{o}}_i$ 下的动作概率分布，利用放大系数 $\alpha$（式 2）控制策略对物体相关特征的敏感度。当 $\alpha > 0$ 时，模型对物体区域的特征响应被放大，而对背景等虚假特征的依赖被抑制。

2. **无需访问模型权重**：PCD 将机器人策略视为黑盒，仅需获取其输出的动作概率分布（自回归策略）或动作采样结果（扩散策略），无需微调或访问预训练参数。这使得 PCD 可以无缝集成到不同类型的策略架构上。

3. **物体掩码精度作为调节杠杆**：Track2Mask 模块利用 SAM2 自动跟踪和掩码目标物体，掩码的精确度直接影响对比解码的效果。消融实验（Table 8）表明，当手动排除的掩码像素比例 $\beta$ 逐步增加时，PCD 性能平滑下降，在 $\beta = 0.6$ 时退化至基线水平，展示了对不完美掩码的鲁棒性。

### 关键方法槽位变更

PCD 相对于基线策略的核心方法变更集中在三个槽位：

| 槽位 | 基线方案 | PCD 方案 | 证据锚点 |
|------|---------|---------|---------|
| **推理策略** | 仅基于原始观测执行标准策略 | 利用原始和物体掩码观测进行对比解码（式 2） | PCD contrasts action probability distributions derived from original and object-masked inputs |
| **扩散策略的动作分布估计** | 直接从反向扩散过程采样动作 | 通过核密度估计（KDE）从多次采样的动作中近似概率分布（式 3） | KDE-PM approximates action probability distributions for diffusion-based policies through kernel density estimation |
| **物体掩码生成** | 无物体掩码 | Track2Mask 模块利用 SAM2 自动跟踪和掩码目标物体 | Track2Mask enables precise object masking for sequential visual observations along each trajectory |

其中，KDE-PM 模块是使 PCD 兼容扩散策略的关键桥梁。扩散策略（如 Octo、π0）原本只输出动作采样结果而非概率分布，KDE-PM 通过对 $N=24$ 个噪声向量进行独立采样，利用高斯核密度估计近似每个动作维度的概率密度，从而使得式 2 的对比解码公式能够统一应用于自回归和扩散两类策略架构。

### 与 Classifier-Free Guidance 的差异

PCD 在形式上与 Classifier-Free Guidance (CFG) 有相似之处（均涉及条件与非条件输出的对比），但存在本质区别：CFG 在扩散策略的**去噪过程中**通过隐式引导调整中间状态，而 PCD 在**最终的动作概率分布层面**进行显式后验校正。实验表明（Table 6-7），CFG 对起始步数高度敏感且提升幅度有限，而 PCD 在不同策略上均表现稳定且提升显著，验证了在概率分布层面进行对比解码的独特优势。

### 鲁棒性设计

PCD 的创新还体现在其对工程实现细节的低敏感性：
- 对目标检测模型（Grounding DINO、Detic 等）和物体修复策略（LaMa、Telea 等）的选择不敏感（Figure 4b, c），表现稳定；
- 在存在大量干扰物的场景下比基线更具鲁棒性（Table 10）；
- 对于多物体任务，同时掩码所有任务相关物体可获得最佳性能（Table 9），展示了方法的灵活扩展性。

这些特性使得 PCD 成为一个真正实用的即插即用模块，而非仅在理想条件下有效的理论方案。



![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_P9PVdWyM3U/figures/005_Figure_2.jpg]]
*Figure 2: Overview of our proposed Policy Contrastive Decoding (PCD) approach. PCD serves as a plugin to redirect the robot policy’s focus toward object-relevant visual cues by contrasting action probability distributions derived from original observations p and object-masked observations ${ \hat { p } }$ . For illustrative purposes, we visualize the predictions only in the $\Delta$ x and $\Delta$ y dimensions of the robot action space [∆x, ∆y, ∆z, rotx, roty, rotz, gripper]

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_P9PVdWyM3U/figures/004_Figure_1.jpg]]
*Figure 1: Robot policies tend to spuriously correlate task-irrelevant features with actions, compromising their ability to generalize to unseen scenarios. As observed, changing the light position from (a) to (b) and the drawer handle position from (a) to (c) results in 36% and 32% drops in the performance of the baseline policy OpenVLA (Kim et al., 2024), respectively. (d) Attention map. More results are in Section 4.4 and Appendix A*

### 核心问题与设计动机

机器人基础模型在预训练过程中，容易从视觉观测中学习到**任务无关特征**（如背景纹理、光照位置、物体摆放姿态）与动作之间的虚假相关性。当测试环境的分布发生偏移时——例如改变光源位置或抽屉把手朝向——这些虚假相关性会导致策略的泛化性能急剧下降。Figure 1 的注意力图可视化直观地展示了这一现象：基线策略 OpenVLA 的视觉注意力高度集中在台灯光源和机械臂部件上，而非任务目标物体（如可乐罐），导致光照位置变化时成功率下降 36%，把手位置变化时下降 32%。

PCD 的核心洞察是：通过在推理阶段对比**原始观测**与**物体掩码观测**下的动作概率分布，可以将策略的注意力从虚假特征重定向到任务相关物体特征，从而以一种**即插即用、无需训练**的方式提升跨场景泛化能力。

### 整体 Pipeline

PCD 的推理流程由三个核心模块串联构成，如 Figure 2 所示：

1. **Track2Mask（目标跟踪与掩码生成）**  
   在轨迹的初始观测中标注任务相关物体（可通过人工点/框提示或 Grounding DINO 自动检测），随后利用 SAM2 模型在后续观测帧中持续跟踪这些物体，生成精确的物体掩码。掩码区域通过 LaMa 等修复模型进行填充，得到物体掩码观测 $\hat{\mathbf{o}}_i$。

2. **双路动作分布估计**  
   将原始观测 $\mathbf{o}_i$ 和物体掩码观测 $\hat{\mathbf{o}}_i$ 分别输入黑盒策略模型，获取对应的动作概率分布：
   - 对于**自回归策略**（如 OpenVLA），直接输出每个动作维度的条件概率 $\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \mathbf{o}_i)$ 和 $\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \hat{\mathbf{o}}_i)$。
   - 对于**扩散策略**（如 Octo、π0），原始输出仅为采样动作，需通过 **KDE-PM 模块**（核密度估计概率建模）从 N 次采样的动作中近似出连续概率分布。

3. **Contrastive Decoder（对比解码器）**  
   通过放大系数 $\alpha$ 对比两路动作概率分布，得到修正后的分布：
   $$
   \pi_{\boldsymbol\theta}^*(\mathbf{a}_i \mid l, \mathbf{o}_i) = \frac{1}{C} \cdot \pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \mathbf{o}_i) \left( \frac{\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \mathbf{o}_i)}{\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \hat{\mathbf{o}}_i)} \right)^\alpha
   $$
   其中 $C$ 为归一化常数。该公式的核心机制是：当某个动作在原始观测下概率高、但在物体掩码观测下概率低时，说明该动作可能依赖于虚假特征，对比操作会抑制其概率；反之，若动作对物体掩码不敏感，则概率被放大。最终从 $\pi_{\boldsymbol\theta}^*$ 中采样执行动作。

### 模块间的输入输出关系

| 模块 | 输入 | 输出 | 依赖的外部模型 |
|------|------|------|----------------|
| Track2Mask | 初始观测 + 物体标注（人工/Grounding DINO） | 逐帧物体掩码观测 $\hat{\mathbf{o}}_i$ | SAM2, LaMa |
| KDE-PM | 扩散策略的 N 次采样动作 | 各维度的近似概率分布 | 无（纯后处理） |
| Contrastive Decoder | $\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \mathbf{o}_i)$ 与 $\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \hat{\mathbf{o}}_i)$ | 修正后的分布 $\pi_{\boldsymbol\theta}^*$ | 无 |

### 关键设计特性

- **黑盒兼容性**：PCD 不访问策略模型的预训练权重，仅依赖模型输出的动作概率分布（自回归策略）或采样动作（扩散策略 + KDE-PM），因此可适配不同类型的机器人基础模型。
- **放大系数 $\alpha$ 的控制作用**：$\alpha$ 调节对比放大的强度。消融实验（Figure 4a）表明，$\alpha > 0$ 时三个基线策略均获得一致提升，但最优值因策略而异——Octo 为 1.0，OpenVLA 为 0.8，π0 为 0.2，反映了不同策略对虚假特征的敏感度差异。
- **对掩码质量的鲁棒性**：当手动排除的掩码像素比例 $\beta$ 逐步增加时，PCD 性能平滑下降，直至 $\beta = 0.6$ 时才退化至基线水平（Table 8），表明方法对不完美掩码具有较强的容忍度。

### 计算开销

PCD 需要两次前向传播（原始观测 + 掩码观测），推理延迟约为基线的两倍。在 SIMPLER 环境中，OpenVLA 的单步推理时间从 0.86s 增至 1.77s，Octo 从 0.21s 增至 0.39s，π0 从 0.39s 增至 0.72s（Table 5）。真实世界实验中，整体时间开销增加约 24%（Figure 3）。



### 3.1 问题形式化与虚假相关

机器人策略 $\pi_{\boldsymbol\theta}$ 在训练分布 $p_{\text{train}}$ 下学习从观测 $\mathbf{o}_i$ 和语言指令 $l$ 到动作 $\mathbf{a}_i$ 的映射。然而，训练数据中往往存在**任务无关的视觉特征** $\mathbf{v}$（如背景纹理、光照位置、相机视角）与动作之间的统计依赖关系——即**虚假相关**（spurious correlation），其强度可通过互信息 $I_{\text{train}}(\mathbf{a}, \mathbf{v})$ 量化。当测试环境发生分布偏移时，策略过度依赖这些虚假特征，导致泛化性能急剧下降（如 Figure 1 所示，仅改变光源位置或抽屉把手位置就使 OpenVLA 成功率分别下降 36% 和 32%）。

PCD 的核心思想是：在推理时将策略的注意力从虚假特征 $\mathbf{v}$ 重定向到**任务相关特征** $\mathbf{u}$（即目标物体本身的视觉线索），而无需修改预训练权重。

### 3.2 策略对比解码（PCD）

PCD 通过对比**原始观测**与**物体掩码观测**下的动作概率分布来实现上述目标。给定原始观测 $\mathbf{o}_i$ 和物体掩码观测 $\hat{\mathbf{o}}_i$（目标物体被修复/去除），对比解码后的动作概率分布为：

$$\pi_{\boldsymbol\theta}^*(\mathbf{a}_i \mid l, \mathbf{o}_i) = \frac{1}{C} \cdot \pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \mathbf{o}_i) \left( \frac{\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \mathbf{o}_i)}{\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \hat{\mathbf{o}}_i)} \right)^\alpha$$

其中：
- $\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \mathbf{o}_i)$：原始观测下的动作概率分布；
- $\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \hat{\mathbf{o}}_i)$：物体掩码观测下的动作概率分布（此时策略主要依赖虚假特征 $\mathbf{v}$ 做预测）；
- $\alpha$：放大系数，控制对物体相关特征的放大强度；
- $C$：归一化常数，确保 $\pi_{\boldsymbol\theta}^*$ 为合法概率分布。

**工作机制**：比值项 $\frac{\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \mathbf{o}_i)}{\pi_{\boldsymbol\theta}(\mathbf{a}_i \mid l, \hat{\mathbf{o}}_i)}$ 衡量了动作 $\mathbf{a}_i$ 在原始观测下相对于掩码观测下的概率增益——这一增益主要来源于物体相关特征 $\mathbf{u}$ 的贡献。通过 $\alpha$ 放大该比值，$\pi_{\boldsymbol\theta}^*$ 会放大那些对物体特征敏感的动作概率，同时抑制仅依赖虚假特征的动作，从而使策略对任务无关的分布偏移具有鲁棒性。

### 3.3 Track2Mask：物体跟踪与掩码生成

Track2Mask 模块负责生成时序一致的物体掩码观测 $\hat{\mathbf{o}}_i$，其流程如下：

1. **初始标注**：在轨迹的第一帧观测中，通过人工标注（点/框提示）或自动检测模型（如 Grounding DINO）指定任务相关物体；
2. **时序跟踪**：利用 SAM2 模型在后续观测帧中持续跟踪这些物体的分割掩码；
3. **物体修复**：使用图像修复模型（如 LaMa）对被掩码的物体区域进行填充，生成 $\hat{\mathbf{o}}_i$。

该模块仅需在轨迹开始时进行一次物体指定，后续全自动执行，实现了“最小人工干预”的目标。

### 3.4 KDE-PM：扩散策略的概率建模

对于扩散策略（如 Octo、π0），其输出为通过 $K$ 步反向扩散过程采样得到的动作 $\mathbf{a}_i$，而非显式的概率分布。为使其兼容 PCD 的对比解码框架，KDE-PM 通过核密度估计从 $N$ 次独立采样的动作中近似概率密度：

$$\pi_{\boldsymbol\theta}(a_t \mid \boldsymbol{l}, \boldsymbol{o}_i) \approx \frac{1}{C'} \sum_{j=1}^{N} K\left( \frac{a_t - a_t^{(j)}}{b} \right)$$

其中：
- $a_t^{(j)}$：第 $j$ 次采样得到的动作在维度 $t$ 上的值；
- $K(\cdot)$：高斯核函数；
- $b$：带宽参数，控制密度估计的平滑程度；
- $C'$：归一化常数；
- $N$：采样次数（实验中设为 24）。

通过对每个动作维度独立进行 KDE 并取乘积得到联合分布，KDE-PM 使扩散策略能够无缝接入 PCD 的对比解码管道。

### 3.5 推理流程

Algorithm 1 给出了 PCD 的完整推理循环：在每步决策时，Track2Mask 生成物体掩码观测 $\hat{\mathbf{o}}_s$，分别计算原始和掩码观测下的动作概率分布（自回归策略直接获取，扩散策略通过 KDE-PM 近似），应用式 (2) 得到对比概率分布 $\pi_{\boldsymbol\theta}^*$，从中采样并执行动作。整个过程对策略模型本身是黑盒的，无需访问模型权重或进行微调。



## 实验与关键发现

### 核心瓶颈与实验动机

机器人基础模型在预训练过程中会从观测中学习到任务无关的视觉特征（如背景纹理、光照条件、相机视角）与动作之间的虚假相关性。当测试环境发生分布偏移时——例如改变光源位置或抽屉把手朝向——这些虚假相关性会导致策略性能急剧下降。Figure 1 的注意力图可视化表明，基线策略 OpenVLA 的注意力分散在背景区域而非任务相关物体上，这直接解释了其在未见场景中 36% 和 32% 的性能退化。

PCD 通过对比原始观测与物体掩码观测下的动作概率分布，将策略注意力重定向至物体相关特征。以下实验从模拟环境到真实世界，系统验证了这一机制的有效性。

### 模拟环境主结果

Table 1 报告了三种代表性机器人策略在 9 项 SIMPLER 任务上的成功率。PCD 以即插即用方式（使用 Grounding DINO 自动检测目标物体）一致地提升了所有策略：

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_P9PVdWyM3U/figures/006_Table_1.jpg]]
*Table 1: SIMPLER Performance. Task-specific objects in the initial observation are annotated by artificial Point and Box prompts or the automatic detection results of GDINO (Liu et al., 2024b). The results are the success rate and the 95% confidence interval of 300 trials. As a plug-and-play approach, PCD consistently enhances the three policies by large margins over the 9 tasks*

- **OpenVLA**（自回归策略）：平均成功率从 16.8% 提升至 25.3%，相对提升 **50.6%**。在 "Google Close Drawer" 任务上，提升幅度最为显著（47.3% → 73.3%）。
- **Octo**（扩散策略）：平均成功率从 13.8% 提升至 17.9%，相对提升 **29.7%**。
- **π0**（扩散策略）：平均成功率从 63.9% 提升至 69.6%，相对提升 **8.9%**。

三种策略的提升幅度差异反映了其基础能力的差异：π0 本身已具备较强的泛化能力，虚假相关性问题相对较轻，因此 PCD 的边际收益较小；而 OpenVLA 受虚假相关性影响最严重，PCD 的纠正效果最为突出。

使用人工标注的 Point 和 Box 提示时，PCD 同样实现了稳定提升，表明方法对物体标注精度的要求不高。

### 真实世界实验

Figure 3 展示了 PCD 在 6 项真实世界操作任务上的性能。以 π0 为基线策略，PCD 使平均成功率实现 **108% 的相对提升**，从约 13.3% 提升至约 27.5%。具体任务层面：

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_P9PVdWyM3U/figures/007_Figure_3.jpg]]
*Figure 3: Real-world Performance. The target objects in the initial observation are automatically annotated by Grounding DINO (Liu et al., 2024b). PCD delivers a remarkable 108% performance improvement on the baseline, though it incurs a 24% increase in time cost*

- "Pick Ball"：25% → 40%
- "Cookies Towel"：10% → 35%
- "Move Near"：10% → 25%
- "Banana Plate"：20% → 35%
- "Stack Cube"：5% → 10%（该任务本身难度极高）

PCD 的推理延迟约为基线的 2 倍（Table 5），在真实世界执行中增加了约 24% 的时间开销。这一开销主要源于两次前向传播（原始观测 + 掩码观测），但考虑到成功率的显著提升，该权衡在多数场景下是可接受的。

### 消融实验

#### 超参数 α 的敏感性

Figure 4(a) 展示了放大系数 α 对三种策略的影响。α = 0 对应基线性能（无对比解码）。关键发现：

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_P9PVdWyM3U/figures/010_Figure_4.jpg]]
*Figure 4: Ablation studies on (a) the hyperparameter α in Eq. (2), (b) the object detection schemes and (c) object inpainting strategies in Track2Mask. α = 0 in (a) and the black dotted lines in (b)(c) represent the performance of the baseline policies. The results are averaged over the 9 simulation tasks. PCD consistently improves the three policies when $\alpha$ > 0 and exhibits low sensitivity to changes in off-the-shelf object detection and inpainting strategies*

- 当 α > 0 时，PCD 始终提升三种策略的性能。
- Octo 的最优 α 为 **1.0**，OpenVLA 为 **0.8**，π0 为 **0.2**。
- π0 对 α 最敏感，较小的 α 即可达到最优效果；过大的 α 反而导致性能下降，说明过度放大物体相关特征可能破坏 π0 原本良好的特征平衡。

#### 目标检测与修复策略的鲁棒性

Figure 4(b,c) 显示 PCD 对不同的目标检测模型（Grounding DINO、Detic 等）和物体修复策略（LaMa、Telea、Navier-Stokes）表现出低敏感性。无论使用何种检测或修复方案，PCD 均能稳定提升基线性能，表明方法的核心机制——对比原始与掩码观测——对具体的掩码实现细节不敏感。

#### 掩码完整性的影响

Table 8 通过手动排除掩码像素（比例 β）模拟不完美掩码场景。在 "pick coke can" 任务上：

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_P9PVdWyM3U/figures/027_Table_8.jpg]]
*Table 8: Performance of PCD under different ratios (β) of masked pixels manually excluded. The task is “pick coke can”*

- β = 0（完整掩码）：OpenVLA 从 25% 提升至 40%，π0 从 84% 提升至 88%。
- 随着 β 增加，PCD 性能逐步退化。
- 当 β = 0.6（60% 的掩码像素被排除）时，性能退化至接近基线水平。

这表明 PCD 对掩码质量具有一定鲁棒性，但严重不完整的掩码会削弱对比解码的效果。

#### 多物体任务的掩码策略

Table 9 的消融表明，对于涉及多个物体的任务，同时掩码所有任务相关物体可获得最佳性能。仅掩码部分物体会导致策略注意力被剩余物体分散，降低 PCD 的纠正效果。

#### 干扰物鲁棒性

Table 10 显示，在存在大量干扰物的场景下，PCD 比基线策略更具鲁棒性。通过掩码目标物体并对比解码，PCD 有效抑制了策略对干扰物的虚假关注。

### 虚假相关性对抗

Figure 5 系统评估了 PCD 在未见测试场景下对抗不同类型虚假相关性的能力：

- **光照变化**：改变光源位置，基线 OpenVLA 性能下降 36%，PCD 显著恢复性能。
- **物体外观变化**：改变抽屉把手位置，基线性能下降 32%，PCD 同样有效纠正。
- **背景干扰**：引入新的背景物体，PCD 展现出更强的鲁棒性。

这些结果表明，PCD 的重定向机制确实将策略注意力从虚假特征转移到了任务相关物体特征，而非简单地记忆训练分布。

### 与 Classifier-Free Guidance 的对比

Table 6 将 PCD 与扩散模型常用的 Classifier-Free Guidance（CFG）进行了对比。CFG 通过混合条件与无条件预测来引导生成，但 Table 7 显示 CFG 的性能对起始步数敏感（最优起始步数为 4，成功率 64.8%），且提升幅度有限。PCD 的优势在于利用显式的物体掩码提供后验纠正信号，而非依赖隐式的无条件预测。

### 计算开销

Table 5 详细列出了三种策略在 SIMPLER 环境中集成 PCD 前后的推理延迟和内存开销。PCD 使单步推理时间约翻倍（OpenVLA: 0.86s → 1.77s; Octo: 0.21s → 0.39s; π0: 0.37s → 0.72s），内存开销增加约 10-20%。这一开销主要来自 Track2Mask 的 SAM2 推理和第二次策略前向传播。

### 失败模式与局限性

1. **物体检测失败**：当 Grounding DINO 无法正确检测目标物体时，Track2Mask 生成的掩码无效，PCD 退化为基线性能。这在物体严重遮挡或语义模糊的场景中尤为突出。
2. **高延迟任务**：对于需要快速响应的动态操作任务，2 倍的推理延迟可能不可接受。
3. **长周期多子任务**：当前 PCD 需要外部高层规划器来分解子任务并指定每步的掩码对象，无法自主处理复杂指令序列。
4. **训练阶段虚假相关性**：PCD 是测试时纠正方法，无法阻止训练阶段学习虚假相关性。未来可探索将对比解码的思路融入训练过程。

### 拓展实验：LIBERO-90

Table 11 报告了 PCD 在 LIBERO-90 基准的 5 项任务上的表现。以 miniVLA 为基线，PCD 在所有任务上均实现了提升，平均成功率从 71.2% 提升至 78.0%，验证了方法在不同任务分布和策略架构下的泛化能力。



## 定位与知识库关联

### 1. 与基线策略的关系

PCD 作为一种**即插即用、无需训练的推理时纠正方法**，不修改任何基线策略的模型权重，而是将其视为黑盒，仅通过对比原始观测与物体掩码观测下的动作概率分布来重定向策略的注意力。这一设计使其能够兼容两类主流的机器人基础模型：

- **自回归策略**：以 **OpenVLA**（Kim et al., 2024）为代表，其本身输出各动作维度的条件概率分布，PCD 可直接利用式 (2) 进行对比解码。
- **扩散策略**：以 **Octo**（Team et al., 2024）和 **π0**（Black et al., 2024）为代表，其原生输出为经反向扩散过程采样得到的动作向量，而非显式概率分布。为此，PCD 引入 **KDE-PM** 模块，通过核密度估计从多次采样（N=24）的动作中近似各维度的概率密度，从而将对比解码框架无缝扩展到扩散策略。

### 2. 与 Classifier-Free Guidance 的对比定位

PCD 与扩散模型中广泛使用的 **Classifier-Free Guidance (CFG)**（Ho & Salimans, 2022）在形式上具有相似性——两者均通过对比两个条件分布来调整模型输出。然而，二者在**机制本质**和**适用边界**上存在根本差异：

- **CFG** 通过对比条件生成与无条件生成的输出，隐式地放大条件信号，是一种训练阶段即嵌入的引导机制，其引导强度由引导尺度控制，且需要模型在训练时同时学习条件与无条件分布。
- **PCD** 通过对比原始观测与物体掩码观测下的输出，显式地抑制任务无关的虚假特征，是一种纯推理时的后验纠正机制，其放大系数 α 控制对物体相关特征的敏感度。

实验证据（Table 6, Table 7）表明，CFG 在机器人策略上的直接应用效果有限且对起始步数敏感，而 PCD 在不同策略上均表现出稳定且显著的提升，二者在机制上互补而非替代。

### 3. 适用边界与鲁棒性

PCD 的有效性建立在**物体掩码质量**这一关键前提之上。消融实验揭示了以下边界条件：

- **掩码完整性**：当手动排除的掩码像素比例 β 逐步增加时，PCD 性能随之下降；在 β=0.6（即 60% 的目标物体像素被排除）时，性能退化至基线水平（Table 8）。这表明 PCD 对不完美掩码具有一定的容忍度，但严重缺失会导致对比信号失效。
- **目标检测方案的低敏感性**：PCD 对不同的目标检测模型（Grounding DINO、Detic 等）和物体修复策略（LaMa、Telea、Navier-Stokes）表现出低敏感性（Figure 4(b,c)），说明其不依赖于特定检测或修复模型的精度。
- **多物体场景**：对于多物体任务，同时掩码所有任务相关物体可获得最佳性能（Table 9），部分掩码会导致性能次优。
- **干扰物鲁棒性**：在存在大量干扰物的场景下，PCD 比基线更具鲁棒性（Table 10），验证了其抑制虚假特征的核心机制。

### 4. 已知局限

1. **推理延迟加倍**：PCD 需要两次前向传播（原始观测 + 掩码观测），使推理延迟大约加倍。在真实世界实验中，这体现为约 24% 的时间开销增加（Figure 3），对于实时性要求极高的部署场景构成约束。
2. **对预训练模型的依赖**：Track2Mask 模块依赖于 Grounding DINO 和 SAM2 等预训练模型进行目标检测与分割。当这些模型在特定场景下检测失败或产生严重不完整掩码时，PCD 可能退化为基线性能。
3. **长周期任务的规划需求**：对于包含多子任务的长周期指令，当前 PCD 需要额外的高层规划器（如 LLM 规划器）来分解子任务并指定每步的掩码对象，自身不具备任务分解能力。
4. **训练阶段虚假相关性的遗留**：PCD 是一种测试时纠正方法，无法阻止策略在预训练阶段从数据中学习虚假相关性。这意味着模型内部仍然编码了这些虚假关联，PCD 仅在推理时对其进行抑制。

### 5. 开放问题

- **计算效率优化**：能否利用快速 LLM 推理技术（如投机解码、KV-cache 共享）进一步降低 PCD 两次前向传播的计算开销？
- **训练阶段整合**：能否将 PCD 的对比解码思路与训练过程结合，从根源上减少策略对虚假特征的学习，而非仅在推理时纠正？
- **与 CFG 的融合**：如何在一个统一框架内结合 PCD 的显式后验校正与 CFG 的隐式引导，发挥二者的互补优势？
- **复杂场景扩展**：PCD 在更复杂的任务（如灵巧操作、动态环境、多视角输入）下的有效性和扩展性如何？当前实验主要覆盖单视角桌面操作任务。
- **通用对比解码策略**：如何在多视角、多传感器（如深度、触觉）输入下设计更通用的对比解码策略，使其不仅限于视觉掩码这一单一扰动形式？



## 原文 PDF

![[paperPDFs/ICLR_2026/Policy_Contrastive_Decoding_for_Robotic_Foundation_Models.pdf]]
