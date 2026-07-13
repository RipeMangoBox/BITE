---
title: "ExPose: Reinforcing Video Generation Models for Extreme Pose Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ExPose_Reinforcing_Video_Generation_Models_for_Extreme_Pose_Estimation.pdf
project_link: null
code_link: "https://github.com/yh-yoon/ExPose"
aliases:
- ExPose
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过使用姿态估计模型作为几何感知奖励，对视频生成模型进行Group Relative Preference Optimization (GRPO) 优化，从而注入3D一致性。
primary_logic: 将视频生成模型的输出与下游姿态估计目标对齐，通过在线强化学习以姿态误差为奖励信号，使生成的中间帧保持几何一致性，从而显著提升极限视角下的姿态估计性能。
claims:
- ExPose在DL3DV数据集的所有指标上均达到最优（SOTA），MRE为33.78，显著优于直接使用VGGT的54.28和专门的InterPose方法（45.22）。
- 在剑桥地标数据集上，ExPose在旋转误差指标上全面领先，MRE 11.48，优于InterPose的15.36。
- 消融研究表明，加入多样性奖励后完整模型（SFT+GRPO+PIC+Div）达到最佳性能，而中间帧数量超过7帧后性能饱和。
- DL3DV 上 MRE↓ = 33.78
---

# ExPose: Reinforcing Video Generation Models for Extreme Pose Estimation

> [!tip] 核心洞察
> 将视频生成模型的输出与下游姿态估计目标对齐，通过在线强化学习以姿态误差为奖励信号，使生成的中间帧保持几何一致性，从而显著提升极限视角下的姿态估计性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | ExPose：通过视频生成模型强化极限姿态估计 |
| 英文题名 | ExPose: Reinforcing Video Generation Models for Extreme Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yoon_ExPose_Reinforcing_Video_Generation_Models_for_Extreme_Pose_Estimation_CVPR_2026_paper.html) · [Code](https://github.com/yh-yoon/ExPose) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ExPose |
| Dataset | DL3DV, NAVI, Cambridge Landmarks |

> [!tip] 效果简介
> - DL3DV 上，MRE↓ 33.78 vs 54.28 (VGGT) (-20.50)；MRE↓ 33.78 vs 45.22 (InterPose) (-11.44)。
> - NAVI 上，AUC↑ 75.37 vs 72.14 (InterPose) (+3.23)。
> - Cambridge Landmarks 上，MRE↓ 11.48 vs 15.36 (InterPose) (-3.88)。

## 概要

**问题瓶颈**：现有视频生成模型在合成中间帧时缺乏3D一致性，导致生成的帧在空间上不可信，进而降低极限视角下姿态估计的准确性。直接使用两视图姿态估计器（如**VGGT**，Wang et al., CVPR 2025）在极端视角变化下误差较大，而基于测试时缩放的重采样策略（如**InterPose**，Cai et al., CVPR 2025）虽有所改善，仍未能从根本上解决几何一致性问题。

**核心方法**：ExPose通过将视频生成模型的输出与下游姿态估计目标对齐，以在线强化学习注入3D一致性。具体而言，该方法结合伪视频监督微调（SFT）与Group Relative Preference Optimization（GRPO），以冻结的3D基础模型（如VGGT）计算的姿态误差作为奖励信号，并引入姿态插值约束（PIC）和基于点追踪的多样性奖励，使生成的中间帧保持几何一致性。

**主要结果**：在DL3DV数据集上，ExPose的MRE达到33.78，显著优于直接使用VGGT的54.28和InterPose的45.22；在Cambridge Landmarks数据集上，MRE为11.48，优于InterPose的15.36。消融实验证实，SFT、GRPO、PIC和多样性奖励四个组件均对性能有正向贡献，其中多样性奖励带来的收益尤为关键。

**方法定位**：ExPose属于“生成增强式姿态估计”范式，不同于直接估计或纯测试时增强方法，它通过在线强化学习将视频生成模型转化为几何感知的中间帧合成器，为极限姿态估计提供了一条新的技术路径。

相机姿态估计是三维视觉的基础任务，旨在从图像中恢复相机的6自由度位姿。在自动驾驶、机器人导航和增强现实等应用中，系统经常需要在视角变化剧烈的条件下运行。然而，当参考图像与目标图像之间的基线极大、视角重叠极小时——即所谓的**极限姿态估计**场景——传统方法面临根本性困难。

### 现有方法的瓶颈

当前主流的姿态估计方法大致可分为两类。一类是基于学习的**双视图直接估计器**，如 **VGGT**（Wang et al., CVPR 2025），它们直接从稀疏图像对中回归相对位姿。这类方法在常规视角下表现良好，但在极限视角下，由于两帧之间缺乏足够的共视区域和纹理对应，其3D理解能力急剧退化，导致估计结果不可靠。

另一类方法尝试借助**视频生成模型**作为中间桥梁。其核心思路是：利用预训练的视频生成器在参考帧和目标帧之间合成中间帧，从而将困难的宽基线估计问题转化为一系列更容易的小基线估计问题。代表方法包括 **DynamiCrafter**（Xing et al., ECCV 2024）、**Aether**（Zhu et al., ICCV 2025）和 **LTX-Video**（HaCohen et al., arXiv 2024），以及专门为此设计的 **InterPose**（Cai et al., CVPR 2025）。InterPose 进一步提出测试时缩放策略，通过生成多个候选视频并选择姿态一致的样本，在一定程度上提升了鲁棒性。

然而，这些方法存在一个**根本性缺陷**：现有的视频生成模型在合成中间帧时缺乏3D一致性。它们被训练来生成视觉上连贯的视频，但并不保证生成帧所隐含的相机运动和场景几何是物理上可信的。这导致合成的中间帧在空间上相互矛盾，进而使下游姿态估计器产生错误预测。简言之，**生成模型的优化目标（视觉质量）与姿态估计的需求（几何精度）之间存在错位**。

### 核心动机与研究思路

ExPose 的核心洞察在于：与其被动接受视频生成模型的输出，不如**主动将生成过程与下游姿态估计目标对齐**。具体而言，该方法将姿态估计模型作为一个几何感知的“裁判”，以姿态误差作为奖励信号，通过在线强化学习直接优化视频生成器，使其输出的中间帧保持3D几何一致性。

这一思路将问题从“生成好看的视频再做姿态估计”转变为“为姿态估计而生成几何正确的视频”，从而在因果链条上直接针对瓶颈进行干预。实验表明，这种目标对齐策略在多个极限姿态估计基准上带来了显著且一致的性能提升，超越了所有现有方法。

## 核心方法与创新机理

ExPose的核心创新在于**将视频生成模型的输出与下游姿态估计目标对齐**，通过在线强化学习以姿态误差为奖励信号，使生成的中间帧保持几何一致性，从而显著提升极限视角下的姿态估计性能。与直接使用预训练视频生成模型（如LTX-Video、DynamiCrafter）合成中间帧的基线方法相比，ExPose在四个关键维度上引入了根本性改变。

### 从无训练到联合优化

现有方法直接使用冻结的视频生成模型，仅依赖其预训练的视频先验来合成中间帧，缺乏对下游姿态估计任务的适配。ExPose引入了**两阶段联合优化策略**：首先利用辅助帧构建伪视频，通过逐帧重建损失进行监督微调（SFT），为模型提供稳定且几何合理的初始化；随后引入**姿态引导的在线GRPO强化学习**，以冻结的3D基础模型（如VGGT）计算姿态误差作为奖励，直接优化视频生成器的参数，使其输出有利于姿态估计的几何一致帧。消融实验（Table 5）证实，GRPO的加入相对于仅SFT带来了显著且一致的性能提升。

### 从无奖励到几何感知奖励

基线方法仅依赖视频质量本身，缺乏明确的几何约束信号。ExPose设计了**基于姿态估计误差的复合奖励函数**：

$$r_{\mathrm{pose}, i} = -\lambda_{\mathrm{rot}} d_{\mathrm{SO}(3)}(\hat{\mathbf{R}}_i, \mathbf{R}^\star) - \operatorname{arccos}(\tilde{\mathbf{t}}_i^\top \mathbf{u}^\star)$$

该奖励结合测地线旋转距离和单位平移方向角误差，尺度无关，直接量化生成视频对姿态估计的贡献。此外，引入**姿态插值约束（PIC）**，惩罚相机中心轨迹偏离端点间等距的偏差，强制平滑连续的相机运动：

$$r_{\mathrm{pic}} = -\lambda_{\mathrm{pic}} \cdot \frac{d\lvert d(\mathbf{c}_m, \mathbf{c}_1) - d(\mathbf{c}_T, \mathbf{c}_m) \rvert}{D + \varepsilon}$$

### 从确定性采样到多样性探索

基线方法采用确定性ODE采样，生成单一轨迹，容易导致策略坍缩。ExPose将确定性ODE转换为保持边缘分布的SDE采样：

$$\mathcal{D}_\phi(x_t, t) := v_\phi(x_t, t) + \frac{\sigma_t^2}{2t} \big(x_t + (1-t) v_\phi(x_t, t)\big)$$

在此基础上生成候选群组，并引入**基于点追踪的多样性奖励**，仅基于参考帧生成多条早期轨迹，计算点追踪位移的成对差异并奖励，鼓励探索更广泛的相机路径：

$$r_{\mathrm{div}}(i) = \lambda_{\mathrm{div}} \cdot \frac{1}{B-1} \sum_{j \neq i} D_{ij}$$

消融实验（Table 5）表明，完整模型（SFT+GRPO+PIC+Div）在所有指标上达到最佳性能，尤其验证了多样性奖励的关键贡献。

### 关键改变的因果机制

上述四个改变槽位形成了完整的因果链条：SFT提供稳定初始化，避免RL阶段的剧烈波动；GRPO通过姿态奖励注入3D一致性信号，直接将生成质量与下游任务性能挂钩；PIC约束相机轨迹的物理合理性；多样性奖励防止策略坍缩至有限路径，确保探索充分的解空间。这一设计使得ExPose在DL3DV数据集上将MRE从VGGT的54.28降至33.78，并显著优于专门设计的InterPose（45.22）。

ExPose 的核心思路是将视频生成模型重塑为极限视角姿态估计的几何一致性增强器。其整体 pipeline 由三个互补的训练阶段构成，共同驱动视频生成器 $G_\phi$ 学会从稀疏的参考–目标图像对中合成有利于下游姿态估计的中间帧。

**输入输出流**：在训练阶段，系统接收三张图像——参考帧 $I_{\mathrm{ref}}$、目标帧 $I_{\mathrm{target}}$ 以及从两者之间选取的辅助帧 $I_{\mathrm{aux}}$（Figure 2）。辅助帧用于构建伪视频监督，而推理阶段仅需 $\{I_{\mathrm{ref}}, I_{\mathrm{target}}\}$ 作为输入。视频生成器 $G_\phi$ 输出 $N$ 帧中间图像序列，随后由冻结的 3D 基础模型（如 **VGGT** (Wang et al., CVPR 2025) 或 **MapAnything** (Keetha et al., arXiv 2025)）对该序列进行姿态估计，得到最终的相对旋转 $\hat{\mathbf{R}}$ 和平移 $\hat{\mathbf{t}}$。

**三个核心训练模块**：

1. **伪视频监督微调（SFT）**：利用辅助帧构建几何一致的伪视频 $\mathcal{V}$，通过逐帧 L1 重建损失 $\mathcal{L}_{\mathrm{SFT}}$ 对生成器进行初始化，为后续强化学习提供稳定且保留场景结构的起点（Sec. 3.1）。

2. **姿态引导的在线强化学习（GRPO）**：以冻结的 3D 基础模型计算姿态误差作为奖励信号 $r_{\mathrm{pose}}$，采用 Group Relative Preference Optimization 在线更新视频生成器。奖励函数结合了测地线旋转距离和单位平移方向角误差，使生成器学会输出有利于姿态估计的几何一致帧（Sec. 3.2, Figure 3）。同时引入姿态插值约束（PIC）奖励 $r_{\mathrm{pic}}$，惩罚相机中心轨迹偏离端点间平滑插值的偏差，强制生成连续、非碎片化的相机运动。

3. **轨迹探索多样性奖励**：为防止策略坍缩至有限的相机路径，系统仅基于参考帧生成多条早期轨迹，计算点追踪位移的成对差异作为多样性奖励 $r_{\mathrm{div}}$，鼓励模型探索更广泛的相机运动空间（Sec. 3.3, Figure 4）。

**训练总损失**为 GRPO 偏好损失与 SFT 监督损失的联合优化：
$$\mathcal{L} = \mathcal{L}_{\mathrm{GRPO}} + \lambda_{\mathrm{SFT}} \mathcal{L}_{\mathrm{SFT}}$$

**推理阶段**：仅需输入参考帧与目标帧，视频生成器合成中间帧序列，再由姿态估计器输出最终相机姿态。整个流程无需辅助帧或额外 3D 监督，实现了从两视图到精确姿态的端到端增强。

![[assets/figures/papers/paper_list_l2481_https_openaccess_thecvf_com_content_CVPR2026_html_Yoon_ExPose_Reinforcin/figures/001_Figure_1.jpg]]
*Figure 1: Overview. We introduce ExPose, a novel extreme pose estimation framework via off-the-shelf 3D foundation models with an aid of pose-rewarded reinforcement learning of video generation models. Compared to directly using the original video generation model, ExPose achieves state-of-the-art performance in extreme baseline pose estimation by synthesizing intermediate frames that more faithfully capture underlying 3D structure. Here, blue, red, and yellow denote the reference pose, the estimated target pose, and the ground-truth (GT) target pose, respectively*

![[assets/figures/papers/paper_list_l2481_https_openaccess_thecvf_com_content_CVPR2026_html_Yoon_ExPose_Reinforcin/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline overview. During training, an auxiliary frame*

ExPose 的训练流程由四个互补模块构成：伪视频监督微调（SFT）、姿态引导的在线 GRPO 强化学习、姿态插值约束（PIC）以及多样性探索奖励。这些组件协同工作，将视频生成模型的输出与下游姿态估计目标对齐。

### 伪视频监督微调

直接对视频生成模型进行在线 RL 训练存在两大挑战：一是仅有两帧输入时模型难以保持场景结构，二是从零开始的 RL 探索效率低下。为此，ExPose 首先构建伪视频数据集进行监督微调。

具体而言，给定参考图像 $I_{\mathrm{ref}}$ 和目标图像 $I_{\mathrm{target}}$，从二者之间选取一帧辅助图像 $I_{\mathrm{aux}}$，利用多条件视频生成器产生 $N$ 帧伪视频：

$${ \mathcal { V } } ( I _ { \mathrm { r e f } } , I _ { \mathrm { a u x } } , I _ { \mathrm { t a r g e t } } ) = \left\{ { V ^ { ( n ) } } ( I _ { \mathrm { r e f } } , I _ { \mathrm { a u x } } , I _ { \mathrm { t a r g e t } } ) \right\} _ { n = 1 } ^ { N }$$

其中 $V^{(n)}$ 表示第 $n$ 帧。随后，视频生成模型 $G_{\phi}$ 仅以 $I_{\mathrm{ref}}$ 和 $I_{\mathrm{target}}$ 为输入，预测 $N$ 帧序列：

$$\left\{ \hat { V } ^ { ( n ) } ( I _ { \mathrm { r e f } } , I _ { \mathrm { t a r g e t } } ) \right\} _ { n = 1 } ^ { N } = G _ { \phi } ( I _ { \mathrm { r e f } } , I _ { \mathrm { t a r g e t } } )$$

SFT 损失采用逐帧 L1 重建损失，将生成视频与伪视频对齐：

$$\mathcal { L } _ { \mathrm { S F T } } ~ = ~ \frac { 1 } { N } \sum _ { n = 1 } ^ { N } \left\| \hat { V } ^ { ( n ) } ( I _ { \mathrm { r e f } } , I _ { \mathrm { t a r g e t } } ) - V ^ { ( n ) } ( I _ { \mathrm { r e f } } , I _ { \mathrm { a u x } } , I _ { \mathrm { t a r g e t } } ) \right\| _ { 1 }$$

这一阶段为后续 RL 提供了稳定且几何合理的初始化策略，使模型在仅有两帧输入的条件下仍能保持场景结构。

### 随机采样与候选群组生成

在线 RL 阶段需要生成多样化的候选视频以进行偏好优化。ExPose 将 LTX-Video 原有的确定性 ODE 采样 $d x _ { t } = v _ { \phi } ( x _ { t } , t ) d t$ 替换为保持边缘分布的 SDE 采样：

$$x _ { t + \Delta t } = x _ { t } + \mathcal { D } _ { \phi } ( x _ { t } , t ) \Delta t + \sigma _ { t } \sqrt { \Delta t } \, \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I})$$

其中漂移项定义为：

$$\mathcal { D } _ { \phi } ( x _ { t } , t ) : = v _ { \phi } ( x _ { t } , t ) + \frac { \sigma _ { t } ^ { 2 } } { 2 t } \big ( x _ { t } + ( 1 - t ) v _ { \phi } ( x _ { t } , t ) \big )$$

随机噪声项 $\sigma_t \sqrt{\Delta t} \, \epsilon$ 引入的随机性使得同一输入对可生成多条不同的中间帧轨迹，为 GRPO 提供候选群组。

### 姿态引导的 GRPO 奖励

ExPose 的核心创新在于利用冻结的 3D 基础模型（如 VGGT）作为几何感知奖励函数。姿态估计器 $\mathcal{F}_{\theta}$ 从参考-目标图像对输出相对旋转 $\hat{\mathbf{R}}$ 和平移 $\hat{\mathbf{t}}$：

$$( \hat { \mathbf { R } } , \hat { \mathbf { t } } ) = \mathcal { F } _ { \boldsymbol { \theta } } ( I _ { \mathrm { r e f } } , I _ { \mathrm { t a r g e t } } )$$

对于每个候选视频 $i$，姿态奖励结合测地线旋转距离和单位平移方向角误差：

$$r _ { \mathrm { p o s e } , i } = - \lambda _ { \mathrm { r o t } } d _ { \mathrm { S O ( 3 ) } } ( \hat { \mathbf { R } } _ { i } , \mathbf { R } ^ { \star } ) - \operatorname { a r c c o s } ( \tilde { \mathbf { t } } _ { i } ^ { \top } \mathbf { u } ^ { \star } )$$

其中 $\mathbf{R}^\star$ 和 $\mathbf{u}^\star$ 为真值旋转和平移方向，$\tilde{\mathbf{t}}_i$ 为归一化平移向量。该奖励是尺度无关的，仅衡量方向和旋转精度。

在获得候选群组的奖励后，采用 GRPO 损失进行策略更新：

$$\mathcal { L } _ { \mathrm { G R P O } } = - \sum _ { \mathrm { g r o u p s } } \sum _ { ( i \succ j ) } \log \sigma \big ( \beta \left( s _ { i } - s _ { j } \right) \big ) + \mathcal { L } _ { \mathrm { K L } }$$

其中 $s_i$ 为样本 $i$ 的标准化奖励，$i \succ j$ 表示 $i$ 优于 $j$ 的偏好对，$\mathcal{L}_{\mathrm{KL}}$ 为 KL 正则化项，防止策略偏离初始 SFT 模型过远。

### 姿态插值约束

为强制生成视频的相机轨迹在端点间平滑连续，ExPose 引入姿态插值约束奖励。设 $\mathbf{c}_1$、$\mathbf{c}_m$、$\mathbf{c}_T$ 分别为首帧、中间帧和末帧的相机中心位置，$D$ 为 $\mathbf{c}_1$ 到 $\mathbf{c}_T$ 的总距离，则 PIC 奖励为：

$$r _ { \mathrm { p i c } } = - \lambda _ { \mathrm { p i c } } \cdot \frac { d \lvert d ( \mathbf { c } _ { m } , \mathbf { c } _ { 1 } ) - d ( \mathbf { c } _ { T } , \mathbf { c } _ { m } ) \rvert } { D + \varepsilon }$$

该奖励惩罚相机中心偏离端点间等距位置的偏差，有效抑制跳跃或碎片化的运动轨迹。

### 多样性探索奖励

为防止策略坍缩至有限几条相机路径，ExPose 在训练早期仅基于参考帧生成多条轨迹，利用点追踪计算成对多样性。对于样本 $i$，多样性奖励定义为：

$$r _ { \mathrm { d i v } } ( i ) = \lambda _ { \mathrm { d i v } } \cdot \frac { 1 } { B - 1 } \sum _ { j \neq i } D _ { i j }$$

其中 $D_{ij}$ 为样本 $i$ 和 $j$ 在早期轨迹段上点追踪位移的成对差异度量，$B$ 为批次大小。该奖励鼓励模型探索更广泛的相机路径空间。

### 联合训练目标

最终训练损失联合 GRPO 偏好损失与 SFT 监督损失：

$$\mathcal { L } = \mathcal { L } _ { \mathrm { G R P O } } + \lambda _ { \mathrm { S F T } } \mathcal { L } _ { \mathrm { S F T } }$$

SFT 损失在 RL 阶段持续发挥作用，防止生成质量退化。总奖励信号为姿态奖励、PIC 奖励和多样性奖励的加权和，驱动视频生成模型输出有利于下游姿态估计的几何一致中间帧。

## 实验与关键发现

### 实验设置

ExPose 以 **LTX-Video**（HaCohen et al., arXiv 2024）作为基础视频生成模型，采用 **VGGT**（Wang et al., CVPR 2025）作为默认的冻结姿态估计器提供奖励信号。为验证对估计器的鲁棒性，还引入 **MapAnything**（Keetha et al., arXiv 2025）作为替代估计器。训练分为三个阶段：利用辅助帧构建伪视频进行监督微调（SFT），随后以姿态误差为奖励进行在线 GRPO 强化学习，同时引入姿态插值约束（PIC）和多样性奖励（Div）防止策略坍缩。推理时模型仅需参考帧与目标帧作为输入，生成中间帧后交由姿态估计器计算相对位姿。

评估在四个数据集上进行：**DL3DV**、**NAVI**、**ScanNet** 和 **Cambridge Landmarks**。指标涵盖平均旋转误差（MRE↓）、平均平移误差（MTE↓）、旋转/平移准确率（R_acc@k° / T_acc@k°）以及曲线下面积（AUC↑）。为保证公平比较，InterPose 被重新实现，使用 LTX-Video 作为基础模型并遵循原始设置生成四个缩放样本。

### 主要结果

**Table 1** 展示了在 DL3DV、NAVI 和 ScanNet 上使用 VGGT 的定量比较。ExPose 在 DL3DV 的所有指标上均达到最优（SOTA），MRE 为 33.78，显著优于直接使用 VGGT 的 54.28（相对提升 37.9%）和专门设计的 **InterPose**（Cai et al., CVPR 2025）的 45.22（提升 25.3%）。在 NAVI 数据集上，ExPose 的 AUC 达到 75.37，超过 InterPose 的 72.14。这些结果表明，通过姿态奖励强化学习优化的视频生成模型能够合成几何上更一致的中间帧，从而在极限视角下大幅提升姿态估计精度。

**Table 2** 给出了 Cambridge Landmarks 数据集上的结果。该数据集仅提供旋转真值，ExPose 在所有旋转误差指标上全面领先，MRE 为 11.48，优于 InterPose 的 15.36。值得注意的是，即使在该数据集的场景分布与训练数据存在差异的情况下，ExPose 仍表现出良好的泛化能力。

**Table 3 和 Table 4** 使用 MapAnything 作为替代姿态估计器进行跨估计器验证。在 NAVI 和 ScanNet 上，ExPose 在所有指标上保持 SOTA（Table 3）；在 Cambridge Landmarks 上，ExPose 同样优于其他视频生成模型（Table 4）。这一致性表明 ExPose 的优化目标与特定估计器解耦，生成的中间帧对不同 3D 基础模型具有普适的几何一致性增益。

### 消融实验

**Table 5** 对 ExPose 的四个核心组件进行了消融分析（基于 DL3DV，LTX-Video + VGGT）。结果表明：

- **SFT alone**：仅使用伪视频监督微调即可将 MRE 从基础 LTX-Video 的 44.13 降至 38.07，验证了伪视频初始化的有效性。
- **+GRPO**：加入姿态奖励的在线强化学习后，MRE 进一步降至 35.41，证明以姿态误差为奖励信号能有效注入 3D 一致性。
- **+PIC**：姿态插值约束使 MRE 降至 34.89，表明平滑相机轨迹约束有助于抑制碎片化运动。
- **+Div（完整模型）**：多样性奖励的加入使 MRE 达到最优的 33.78，验证了轨迹探索对防止策略坍缩至有限路径的关键作用。

**Figure 6** 展示了中间帧数量对 MRE 和 MTE 的影响曲线。随着中间帧数量从 1 帧增加到 7 帧，误差持续下降；超过 7 帧后改善趋于饱和。这表明 7 帧左右的中间帧已能充分覆盖极限视角间的几何过渡，更多帧带来的边际收益有限。

### 定性分析

**Figure 5** 提供了定性比较。在极端视角变化下，VGGT 直接估计往往产生显著偏差（如点云错位或姿态偏移），而 LTX-Video 生成的中间帧虽能提供部分补充信息，但几何一致性不足。ExPose 生成的中间帧在保持场景结构的同时，使 VGGT 估计的目标姿态（红色）更接近真值（黄色），直观体现了 3D 一致性注入的效果。

### 失败模式与局限性

尽管 ExPose 在多个基准上取得 SOTA，仍存在以下局限：

1. **奖励信号上限**：方法依赖预训练的 3D 基础模型（VGGT 或 MapAnything）提供奖励，这些模型本身在极限视角下可能不够精确，从而限制优化的理论上限。当奖励信号存在系统性偏差时，GRPO 可能被引导至次优策略。
2. **计算开销**：在线 GRPO 需要为每个训练样本生成多个候选视频并计算姿态奖励，加上 SFT 阶段辅助帧的选择，显著增加了训练计算量，可能限制在资源受限场景下的应用。
3. **视角跳变泛化**：目前主要在固定间隔的视角变化上验证，对于非均匀或大幅度的极端视角跳动，泛化能力未经充分测试。
4. **点跟踪依赖**：多样性奖励基于点跟踪质量，当跟踪失败（如遮挡或纹理缺失区域）时可能引入噪声或误导信号，影响轨迹探索的有效性。

![[assets/figures/papers/paper_list_l2481_https_openaccess_thecvf_com_content_CVPR2026_html_Yoon_ExPose_Reinforcin/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on the DL3DV, NAVI, and ScanNet datasets using VGGT. We evaluate the camera pose estimates from VGGT based on images generated by each video generation model. The intermediate images produced by generative models lead to more accurate pose estimation in extreme-view scenarios, highlighting the value of high-quality generative priors. Our method performs well across most metrics on all datasets and achieves state-of-the-art results on every metric of the DL3DV dataset*

![[assets/figures/papers/paper_list_l2481_https_openaccess_thecvf_com_content_CVPR2026_html_Yoon_ExPose_Reinforcin/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison on the Cambridge Landmarks dataset using VGGT. Our method achieves state-of-theart performance across all rotation error metrics*

![[assets/figures/papers/paper_list_l2481_https_openaccess_thecvf_com_content_CVPR2026_html_Yoon_ExPose_Reinforcin/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison on the DL3DV, NAVI, and ScanNet using MapAnything. We evaluate camera pose estimations from MapAnything using images generated by different video generation models, where intermediate frames help improve accuracy in extreme-view settings. Our method further achieves state-of-the-art performance across all metrics on the NAVI and ScanNet datasets*

![[assets/figures/papers/paper_list_l2481_https_openaccess_thecvf_com_content_CVPR2026_html_Yoon_ExPose_Reinforcin/figures/009_Table_5.jpg]]
*Table 5: Quantitative ablation study. We evaluate four key components of our method: supervised finetuning (SFT), group relative policy optimization (GRPO), pose interpolation constraint (PIC), and diversity reward (Div). The evaluation uses the DL3DV dataset, with LTX-Video for video generation and VGGT for pose estimation*

## 定位与知识库关联

### 与基线方法的关系

ExPose 并非孤立地提出一种新的姿态估计器，而是在**视频生成模型与3D基础模型之间建立了一条强化学习驱动的对齐管道**。理解其定位需要厘清它与三类基线工作的关系。

**直接姿态估计基线**：**VGGT**（Wang et al., CVPR 2025）作为3D基础模型，直接从参考-目标图像对回归相对位姿。当视角变化剧烈时，两帧之间的视觉重叠极小，VGGT 缺乏足够的对应线索，导致估计精度急剧下降（DL3DV 上 MRE 高达 54.28，见 Table 1）。ExPose 并非替换 VGGT，而是通过生成几何一致的中间帧为其“铺路”——将极端视角问题转化为一系列小视角变化问题，使 VGGT 的逐帧估计结果在合并后显著提升。

**视频生成增强基线**：将预训练视频生成模型直接用于合成中间帧是一种自然思路。**DynamiCrafter**（Xing et al., ECCV 2024）、**Aether**（Zhu et al., ICCV 2025）和 **LTX-Video**（HaCohen et al., arXiv 2024）均属此类。然而，这些模型的训练目标是最小化视频重建损失，而非保证中间帧的3D几何一致性。Table 1 显示，虽然它们均优于直接使用 VGGT（MRE 从 54.28 降至 43–46 区间），但改善幅度有限，且在不同数据集上表现不稳定。**InterPose**（Cai et al., CVPR 2025）在此基础上引入测试时缩放策略，通过重采样多个生成轨迹并选择最优结果，将 MRE 进一步降至 45.22，但仍受限于基础生成模型缺乏显式几何约束。

ExPose 的核心突破在于**将下游姿态估计目标反馈到生成模型的训练过程中**，通过 GRPO 使生成器主动学习产生有利于姿态估计的中间帧。这解释了为何 ExPose 能在 DL3DV 上将 MRE 降至 33.78，较 InterPose 再降 11.44 个点，差距显著。

**替代估计器验证**：为排除对特定姿态估计器的过拟合，ExPose 在 **MapAnything**（Keetha et al., arXiv 2025）上进行了完整验证。Table 3 和 Table 4 表明，ExPose 生成的中间帧对 MapAnything 同样有效，在 NAVI 和 ScanNet 上达到 SOTA，证明其学到的几何一致性是可迁移的。

### 适用边界

ExPose 的有效性依赖于几个关键前提，这些前提构成了其适用边界：

1. **预训练3D基础模型的质量**：奖励信号由冻结的 VGGT 或 MapAnything 计算。若这些模型在特定场景（如无纹理区域、重复结构、极端光照）下本身精度不足，奖励信号将带有噪声，限制优化上限。论文在 limitations 中明确承认这一依赖。

2. **视频生成模型的基础能力**：ExPose 以 LTX-Video 为骨干，其生成质量和多样性上限受限于该模型的架构与预训练数据分布。对于超出 LTX-Video 训练分布的图像内容，SFT 和 GRPO 的改进空间有限。

3. **视角变化的均匀性假设**：当前验证集中在固定间隔采样的视角变化上（DL3DV、NAVI、ScanNet 等数据集）。对于非均匀或跳变式的极端视角变化，姿态插值约束（PIC）和多样性奖励的设计可能不够充分，泛化能力未经测试。

4. **计算开销**：训练需在线生成候选视频并调用3D基础模型计算奖励，SFT 阶段还需选择和编码辅助帧。这增加了训练成本，可能限制在计算资源受限场景下的应用。

### 局限与开放问题

**已识别的局限**：

- **奖励模型瓶颈**：3D基础模型在极端视角下的精度直接影响 GRPO 优化的上限。若奖励信号系统性地偏向错误方向，策略可能被误导。
- **点跟踪依赖性**：多样性奖励基于点追踪位移计算。当场景包含动态物体、遮挡或纹理不足区域时，点跟踪可能失败，引入噪声奖励。
- **辅助帧需求**：SFT 阶段依赖辅助帧构建伪视频监督。对于完全无中间视角信息的输入对，该策略不可用，限制了方法在极稀疏输入场景下的适用性。

**开放问题**：

1. **框架的通用性**：能否将“生成模型输出 + 下游任务奖励”的对齐框架扩展到其他3D视觉任务，如深度估计、场景重建或新视角合成？这需要设计对应的任务奖励函数。

2. **无辅助帧的伪视频构建**：是否可以通过纯生成方式（如单目深度估计 + 视角合成）构建伪视频监督，完全摆脱对辅助帧的依赖，使其适用于无重叠的输入对？

3. **多样性奖励的语义化**：当前的多样性奖励仅基于运动幅度的差异，未考虑场景语义。能否结合语义分割或物体检测，鼓励生成内容相关但相机路径多样的视频，进一步提升探索效率？

4. **复杂运动的轨迹先验**：姿态插值约束假设相机中心沿直线平滑移动。对于包含大角度旋转与平移耦合的运动，是否需要更精细的轨迹先验（如样条曲线或物理约束）？

5. **与稀疏视角重建的联合优化**：ExPose 目前以姿态估计为单一目标。能否将其与稀疏视角场景重建联合优化，使生成的中间帧同时服务于位姿估计和3D结构恢复，形成闭环提升？

## 原文 PDF

![[paperPDFs/CVPR_2026/ExPose_Reinforcing_Video_Generation_Models_for_Extreme_Pose_Estimation.pdf]]
