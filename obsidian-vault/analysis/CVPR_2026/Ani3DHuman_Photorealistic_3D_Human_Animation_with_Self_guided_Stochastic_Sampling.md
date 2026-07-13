---
title: "Ani3DHuman: Photorealistic 3D Human Animation with Self-guided Stochastic Sampling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Ani3DHuman_Photorealistic_3D_Human_Animation_with_Self_guided_Stochastic_Sampling.pdf
project_link: null
code_link: "https://github.com/qiisun/ani3dhuman"
aliases:
- Ani3DHuman
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 自引导随机采样通过随机校正OOD输入和自引导保持身份，解决了从粗渲染恢复高质量视频的难题，从而为4D优化提供了强有力的监督。
primary_logic: 将运动学动画与视频扩散先验结合，利用分层运动表示解耦刚性与非刚性运动，并通过自引导随机采样实现从OOD粗渲染到真实感视频的恢复，最终实现身份保持、动态丰富的三维人体动画。
claims:
- 确定性Flow-ODE在处理OOD粗渲染时无法校正分布偏差，导致不正确的采样轨迹和低质量输出。
- 自引导随机采样在保持身份的同时生成了清晰、真实的非刚性动态，明显优于SDEdit、FlowEdit、MCS等竞争采样方法。
- 在ActorsHQ数据集上，本文方法在FID指标上（105.3）比最佳竞争者LHM（124.1）提升了18.8，且用户研究在所有维度均获最高偏好（总体54.4%）。
- 消融实验证实：去除随机采样导致严重质量下降，去除自引导使身份丧失（CLIP-Identity从0.8838降至0.8220）。
---

# Ani3DHuman: Photorealistic 3D Human Animation with Self-guided Stochastic Sampling

> [!tip] 核心洞察
> 将运动学动画与视频扩散先验结合，利用分层运动表示解耦刚性与非刚性运动，并通过自引导随机采样实现从OOD粗渲染到真实感视频的恢复，最终实现身份保持、动态丰富的三维人体动画。

| 字段 | 内容 |
|------|------|
| 中文题名 | Ani3DHuman：基于自引导随机采样的真实感三维人体动画 |
| 英文题名 | Ani3DHuman: Photorealistic 3D Human Animation with Self-guided Stochastic Sampling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.19089) · [Code](https://github.com/qiisun/ani3dhuman) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | ANI3DHUMAN |
| Dataset | ActorsHQ, User Study |

> [!tip] 效果简介
> - ActorsHQ 上，FID↓ 105.3 vs 124.1 (LHM) (-18.8)；CLIP-Identity↑ 0.9160 vs 0.9009 (LHM) (+0.0151)；PSNR↑ 20.08 vs 19.51 (LHM) (+0.57)。
> - User Study (novel motion) 上，Overall Preference 54.4% vs 22.1% (PERSONA), 17.6% (LHM) (>+32.3%)。

## 概要

从单张参考图像合成具有真实感非刚性动态的三维人体动画，是计算机视觉与图形学中长期存在的难题。现有方法面临一个核心瓶颈：运动学驱动的刚性动画方法（如 **LHM**）能够保持身份一致性，但完全缺失衣物褶皱等非刚性动态；而基于视频扩散模型的生成方法虽能产生丰富动态，却普遍存在身份漂移和严重伪影，难以同时兼顾真实感与身份保真度。

**ANI3DHUMAN** 针对上述瓶颈提出了一个因果性解决方案。其核心洞察在于，将运动学动画的刚性结构先验与视频扩散模型的生成先验相结合，通过**分层运动表示**解耦刚性与非刚性运动，并引入**自引导随机采样**机制，从粗渲染中恢复出高质量、身份一致的视频序列，进而为4D高斯表示提供强有力的优化监督。

具体而言，该方法首先利用单图重建获得规范空间下的3D高斯表示，随后通过显式网格变形驱动刚性运动，并辅以隐式残差场建模非刚性动态。刚性变形产生的粗渲染作为输入，经由自引导随机采样——一种结合随机SDE噪声校正与基于掩码的后验均值引导的采样策略——恢复为清晰且身份保持的视频。最终，通过对角线视图-时间采样和渐进数据集更新，将恢复视频中的动态信息蒸馏至4D高斯表示中，实现可实时渲染的真实感动画。

在ActorsHQ数据集上的定量评估表明，ANI3DHUMAN在FID指标上达到**105.3**，较最佳竞争者LHM（124.1）提升18.8；CLIP-Identity达到**0.9160**。用户研究中，该方法在新颖动作场景下获得了**54.4%** 的总体偏好率，远超PERSONA（22.1%）和LHM（17.6%）。消融实验进一步证实，随机采样与自引导机制缺一不可：移除前者导致视频质量显著下降，移除后者则使身份一致性大幅丧失（CLIP-Identity从0.8838降至0.8220）。

在方法谱系上，ANI3DHUMAN处于运动学动画与扩散先验驱动的4D重建交叉点。相较于 **Disco4D** 和 **SV4D 2.0** 等基于SDS或多视图扩散的4D重建方法，它通过视频恢复而非直接生成来规避质量与身份的矛盾；相较于 **PERSONA** 等姿态驱动视频扩散方法，它采用“恢复-优化”两阶段策略，将扩散模型的生成能力转化为4D表示的监督信号，从而实现了身份保持与非刚性动态的真实感统一。

### 问题背景

三维人体动画是计算机视觉与图形学的核心任务之一，其目标是从给定的参考图像和运动序列出发，合成具有真实感外观和动态细节的三维人体动画。这一任务在虚拟现实、数字人交互、影视制作等领域具有广泛的应用前景。然而，实现高质量的三维人体动画面临两大核心挑战：**身份一致性保持**和**真实感非刚性动态建模**。

身份一致性要求动画过程中人物的面部特征、体型、肤色等视觉属性不随时间和视角漂移。非刚性动态则涉及衣物褶皱、头发飘动、肌肉变形等复杂运动，这些动态难以通过简单的运动学变换直接建模。现有方法在这两个维度上往往顾此失彼，难以同时满足。

### 现有方法缺口

当前主流的三维人体动画方法可分为以下几类，但各自存在明显短板：

- **运动学驱动的刚性动画方法**（如 **LHM**）：通过 SMPL 网格变形驱动重建的三维表示。这类方法能够较好地保持身份一致性，但**完全缺乏衣物动态**，生成的动画僵硬、缺乏真实感，仅能表现刚体级别的运动。

- **基于视频扩散先验的动画方法**（如 **PERSONA**）：直接利用姿态条件视频扩散模型生成动画帧。虽然能产生一定的非刚性动态，但**身份漂移问题严重**——扩散模型在生成过程中容易偏离原始人物身份，且容易引入严重伪影。

- **多视图/4D 重建方法**（如 **Disco4D**、**SV4D 2.0**）：从单视图或多视图视频重建动态三维表示。这类方法依赖高质量输入视频，且重建质量受限于输入分辨率与视角覆盖，难以泛化到新颖运动序列。

从更根本的层面看，现有方法的瓶颈在于：**运动学方法缺乏衣物动态，而直接使用视频扩散模型会导致身份漂移和严重伪影**。这一矛盾的根源在于，运动学渲染结果（粗渲染）与扩散模型的训练分布之间存在显著偏差——粗渲染缺乏真实感纹理和动态细节，属于分布外（Out-of-Distribution, OOD）输入，直接输入扩散模型会产生不可靠的生成结果。

### 本文动机

本文的核心动机是**桥接运动学动画的结构保真度与视频扩散先验的生成能力**，在保持身份一致性的前提下恢复真实感非刚性动态。具体而言，我们希望回答以下问题：

1. 如何将运动学动画的刚性结构先验与扩散模型的生成能力有效结合？
2. 如何解决粗渲染作为 OOD 输入时扩散模型的分布偏差问题？
3. 如何在视频恢复过程中同时保持身份一致性和生成质量？

为解决这些问题，本文提出 **ANI3DHUMAN** 框架，其核心思想是：利用分层运动表示解耦刚性与非刚性运动，通过运动学方法生成粗渲染作为结构先验，再设计自引导随机采样策略从粗渲染中恢复高质量、身份一致的视频，最终以恢复视频为监督信号优化完整的三维人体动画表示。

## 核心方法与创新机理

Ani3DHuman 的核心创新并非单纯引入视频扩散模型，而是构建了一套 **“粗渲染—扩散恢复—4D 优化”闭环**，通过三个相互耦合的 changed slots 解决了现有方法在身份保持、非刚性动态和真实感之间的根本矛盾。

### 1. 自引导随机采样：从 OOD 粗渲染恢复身份保持的真实感视频

这是整个方法最关键的创新。现有运动学驱动的动画方法（如 **LHM**）仅能产生刚性网格变形的粗渲染 $y$，缺乏衣物褶皱、肌肉变形等非刚性动态。直接使用视频扩散模型对 $y$ 进行增强面临核心瓶颈：粗渲染是分布外（OOD）输入，确定性 Flow-ODE 采样器无法校正这一分布偏差，导致采样轨迹偏离正确方向，产生模糊或伪影（Fig. 3）。

Ani3DHuman 提出的**自引导随机采样**（Self-guided Stochastic Sampling）通过两个互补机制解决了这一难题：

- **随机性校正（Stochastic Correction）**：将标准确定性 ODE 采样替换为反向时间 SDE 采样，在每一步向预测噪声注入高斯扰动：

$$d \mathbf{x} = \mathbf{v}_t(\mathbf{x}_t, t) dt + g(t) d\mathbf{w}_t$$

这一随机扩散项赋予采样器逃离错误轨迹的能力，从 OOD 输入逐步恢复出清晰、真实的细节。消融实验（Table 4）显示，移除随机采样后 FVD 从 295.2 升至 349.7，生成结果出现严重质量下降（Fig. 7c）。

- **自引导身份保持（Self-Guidance）**：仅靠随机采样虽能提升真实感，但会导致身份漂移。Ani3DHuman 引入基于 DPS 近似的自引导机制，在每次更新中对后验均值施加掩码约束：

$$\hat{\mathbf{x}}_{0|t} \leftarrow \hat{\mathbf{x}}_{0|t} - \lambda \nabla_{\mathbf{x}_t} || \mathcal{M} \odot (\mathbf{y} - \hat{\mathbf{x}}_{0|t}) ||^2$$

通过最小化保留区域（面部、身体轮廓等）的重建误差，迫使生成结果忠于输入粗渲染的身份信息。消融实验证实，移除自引导后 CLIP-Identity 从 0.8838 骤降至 0.8220（Table 4, Fig. 7d），身份严重丢失。

**关键证据**：在视频恢复方法对比中（Fig. 6），自引导随机采样是唯一同时实现“清晰细节生成”与“原始身份保持”的方法，明显优于 SDEdit、FlowEdit、MCS 等竞争采样策略。

### 2. 分层运动表示：解耦刚性与非刚性运动

传统方法使用单一运动场（仅刚性变换或非刚性场），无法同时处理骨骼驱动的整体运动和衣物等局部动态。Ani3DHuman 的**分层运动表示**将运动显式解耦为两个层次：

- **刚性运动层**：通过 SMPL 网格变形驱动 3D 高斯原语，提供稳定的结构先验和身份锚定。
- **非刚性残差运动层**：由 Hexplane + MLP 参数化的隐式残差场建模，从规范空间位置 $\mathbf{p}$ 和时间 $t$ 预测残差变形 $\Delta \mathbf{p}$，捕捉衣物褶皱、肌肉起伏等高频动态。

这一设计使得刚性运动提供可靠的“骨架”，非刚性层仅需学习残差，大幅降低了优化难度。消融实验（Fig. 8）表明，使用单层运动场会导致手部细节丢失和非刚性变形不自然。

### 3. 对角线视图-时间采样：最小化多视图不一致

4D 优化需要从恢复视频中提取多视图监督，但独立视图采样或固定时间采样会引入时空不一致。Ani3DHuman 提出**对角线视图-时间采样**（Fig. 4），在视图-时间矩阵中沿对角线同时演化相机视角和时间步，以最少轨迹数捕获时空信息，最小化暴露于不一致性的风险。配合渐进数据集更新策略，有效防止过度平滑，保留衣物褶皱等高频纹理（Fig. 11c）。

### 创新耦合逻辑

三个 changed slots 并非孤立存在，而是形成因果闭环：分层运动表示产生粗渲染 $y$ → 自引导随机采样将 $y$ 恢复为高质量视频 $x^*$ → $x^*$ 通过对角线采样为残差运动场提供强监督 → 优化后的残差场反过来改善刚性运动的基础渲染质量。这一闭环使得 Ani3DHuman 在 ActorsHQ 数据集上 FID 达到 105.3，比最佳竞争者 LHM（124.1）提升 18.8，用户研究总体偏好达 54.4%（Table 1, Table 2）。

ANI3DHUMAN 的整体 pipeline 围绕一个核心矛盾展开：运动学驱动的网格变形能提供刚性的结构骨架，却无法捕捉衣物的自然褶皱、摆动等非刚性动态；而直接让视频扩散模型从姿态条件生成视频，又会因缺乏结构先验而导致身份漂移和严重伪影。该方法的解决思路是**将刚性动画作为“粗稿”，由扩散模型负责“精修”出非刚性动态，再以精修结果作为监督信号优化可微的4D表示**。

### 输入输出流

系统的输入仅需**一张参考人物图像**和一段**目标SMPL网格序列**（即驱动动作）。输出是一个**可自由视点渲染的4D高斯表示**，该表示在保持参考图像身份的同时，展现出照片级真实的非刚性动态（如裙摆飘动、衣物褶皱），如 Figure 1 所示。

### 四模块串联架构

Figure 2 清晰展示了四个模块的串联关系：

![[assets/figures/papers/paper_list_l1007_https_arxiv_org_abs_2602_19089/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline overview. Our ANI3DHUMAN animates a 3D Gaussian G (reconstructed with LHM [58] from the reference image) with a mesh sequence. Our layered motion combines a mesh-rigged motion with a residual field for non-rigid dynamics. A coarse rendering y from the rigid motion is restored to a high-quality video*

1. **单图3D高斯重建**：使用现成的 **LHM** 方法从参考图像重建规范空间下的3D高斯表示 $G$。该表示作为后续所有动画和优化的基础载体。

2. **分层运动场**：将人体运动解耦为两层——显式的**网格绑定刚性运动**（由SMPL序列驱动3D高斯变形）和隐式的**残差非刚性运动场**（由Hexplane+MLP参数化，预测每个高斯基元的位置、旋转、缩放偏移）。仅使用刚性运动时，渲染结果 $y$ 是身份正确但缺乏衣物动态的“粗渲染”。

3. **自引导随机视频恢复**：这是 pipeline 的核心创新模块。将粗渲染 $y$ 作为输入，通过**自引导随机采样算法**（Algorithm 1）驱动一个个性化的视频扩散先验，生成高质量、身份一致的恢复视频 $x^*$。该采样器同时具备两个关键能力：随机SDE采样校正粗渲染的分布外（OOD）误差，自引导机制保持输入身份不漂移。

4. **渐进式4D优化**：以恢复视频 $x^*$ 作为监督信号，优化残差运动场和3D高斯参数。采用**对角线视图-时间采样**策略（Figure 4）——相机视角和时间同步推进，用最少轨迹数捕获完整的时空信息，最小化多视图不一致。优化过程配合渐进数据集更新，防止过度平滑。

### 信息流动的关键逻辑

粗渲染 $y$ 为扩散模型提供了**强结构和身份先验**——它已经具备正确的人体姿态和大致外观，只是缺失了非刚性动态细节。这一设计使得视频恢复任务从“从零生成”降级为“从OOD输入恢复”，大幅降低了扩散模型的生成难度。恢复后的视频 $x^*$ 再反哺4D优化，形成闭环：**扩散先验负责“想象”非刚性动态，4D优化负责将其蒸馏为可自由视点的显式表示**。

ANI3DHUMAN 的核心技术链路包含四个紧密耦合的模块：**分层运动表示**、**自引导随机视频恢复**、**个性化扩散先验**以及**渐进式4D优化**。本节聚焦前两个核心模块的公式化描述与设计动机。

### 3.1 预备知识：流匹配

方法建立在流匹配（Flow Matching）框架之上。给定数据分布 $p(\boldsymbol{x}_0)$ 和高斯噪声分布 $p(\boldsymbol{x}_1)=\mathcal{N}(0,1)$，流匹配训练一个速度场 $\boldsymbol{v}_\theta$ 来预测从噪声到数据的恒定速度：

$$
\operatorname*{min}_{\theta}\mathbb{E}_{t,\boldsymbol{x}_0,\boldsymbol{x}_1}||\boldsymbol{v}_\theta(\boldsymbol{x}_t,t)-(\boldsymbol{x}_1-\boldsymbol{x}_0)||_2^2 \tag{1}
$$

其中 $\boldsymbol{x}_t = t\boldsymbol{x}_1+(1-t)\boldsymbol{x}_0$ 是线性插值的中间状态。采样时通过积分速度场从 $t=1$ 到 $0$ 生成样本：

$$
d\boldsymbol{x}_t = \boldsymbol{v}_\theta(\boldsymbol{x}_t,t)dt \tag{2}
$$

从中间状态 $\boldsymbol{x}_t$ 可估计干净数据（后验均值）和噪声：

$$
\hat{\boldsymbol{x}}_{0|t} = \boldsymbol{x}_t - \sigma_t\boldsymbol{v}_\theta(\boldsymbol{x}_t,t) \tag{3}
$$
$$
\hat{\boldsymbol{x}}_{1|t} = \boldsymbol{x}_t + (1-\sigma_t)\boldsymbol{v}_\theta(\boldsymbol{x}_t,t) \tag{4}
$$

其中 $\sigma_t = 1-t$。确定性ODE更新通过线性插值实现：

$$
\boldsymbol{x}_{t_{\mathrm{next}}} = (1-\sigma_{t_{\mathrm{next}}})\hat{\boldsymbol{x}}_{0|t} + \sigma_{t_{\mathrm{next}}}\hat{\boldsymbol{x}}_{1|t} \tag{5}
$$

### 3.2 分层运动表示

核心洞察是将人体运动分解为**刚性分量**与**非刚性残差分量**。刚性运动由运动学网格驱动：给定参考图像重建的规范空间3D高斯 $\mathcal{G}$ 和目标SMPL网格序列，通过网格蒙皮变形获得粗动画。然而，这种纯运动学驱动无法建模衣物褶皱、头发飘动等非刚性动态。

为补全这一缺失维度，方法引入一个**隐式残差运动场**，参数化为 Hexplane + MLP 解码器。对规范空间中的每个高斯位置 $\mathbf{p}$，Hexplane 查询特征 $f_p$，MLP 以 $f_p$ 和时间步 $t$ 为输入，输出残差位移 $\Delta\mathbf{p}$ 和残差旋转 $\Delta\mathbf{R}$。最终的高斯运动由刚性网格变形与残差场叠加得到。该分层设计（Fig. 8消融验证）使手部细节和非刚性变形更加自然，而单层运动场则导致细节丢失。

### 3.3 自引导随机视频恢复

仅使用分层运动场渲染的粗结果 $\mathbf{y}$ 在纹理细节和真实感上仍有显著不足。直接将其输入视频扩散模型进行“修复”面临一个根本性挑战：**$\mathbf{y}$ 处于分布外（OOD）**。

**OOD问题的本质**：如 Fig. 3 所示，粗渲染 $\mathbf{y}$ 注入噪声后得到的隐变量偏离了流匹配模型训练时的边际分布。若使用确定性 Flow-ODE（Eq. 5）采样，模型会沿着错误的轨迹积分，无法校正分布偏差，导致输出模糊或带有伪影。

**随机SDE采样**：为解决此问题，方法改用反向时间随机微分方程（SDE），在采样过程中注入扩散项以提供随机校正能力。首先向粗渲染注入高斯噪声至时间 $t$：

$$
\boldsymbol{x}_t = \sigma_t\epsilon + (1-\sigma_t)\mathbf{y},\quad\epsilon\sim\mathcal{N}(0,1) \tag{6}
$$

随后沿反向SDE采样：

$$
d\boldsymbol{x} = \boldsymbol{v}_t(\boldsymbol{x}_t,t)dt + g(t)d\boldsymbol{w}_t \tag{7}
$$

其中 $g(t)d\boldsymbol{w}_t$ 是扩散项，赋予采样轨迹随机探索能力，从而校正OOD输入带来的偏差。实际实现中，随机性通过对预测噪声施加扰动来引入：

$$
\hat{\boldsymbol{x}}_{1|t} \leftarrow \sqrt{\gamma(t)}\epsilon + \sqrt{1-\gamma(t)}\hat{\boldsymbol{x}}_{1|t},\quad\gamma(t)=\sigma_t \tag{8}
$$

**自引导机制**：纯粹的随机采样虽然能生成清晰纹理，但可能丧失输入的身份信息。为此，方法引入基于后验均值的自引导步骤，通过最小化保留区域的L2误差来保持身份一致性。具体而言，使用DPS（Diffusion Posterior Sampling）近似，在每次更新中对后验均值施加梯度校正：

$$
\hat{\boldsymbol{x}}_{0|t} \leftarrow \hat{\boldsymbol{x}}_{0|t} - \lambda\nabla_{\boldsymbol{x}_t}||\mathcal{M}\odot(\mathbf{y}-\hat{\boldsymbol{x}}_{0|t})||^2 \tag{9}
$$

其中 $\mathcal{M}$ 是一个掩码，指示需要保持身份一致性的区域（如面部、衣物主体结构），$\lambda$ 控制引导强度。该自引导项与随机采样步骤（Eq. 8）共同嵌入标准更新规则（Eq. 5），形成完整的**自引导随机采样器**（Algorithm 1）。

**消融验证**（Table 4, Fig. 7）：移除随机采样（仅保留自引导）会导致FVD从295.2升至349.7，生成结果模糊或带伪影；移除自引导（仅保留随机采样）则使CLIP-Identity从0.8838骤降至0.8220，身份严重丢失。两者协同才能同时实现高真实感和身份保持。

### 3.4 渐进式4D优化

恢复后的高质量视频 $\mathbf{x}^*$ 作为监督信号，驱动残差运动场和4D高斯的优化。优化目标为组合损失：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{L1}} + \lambda_1\mathcal{L}_{\mathrm{LPIPS}} + \lambda_2\mathcal{L}_{\mathrm{dssim}} + \lambda_3\mathcal{L}_{\mathrm{mask}} + \lambda_4\mathcal{L}_{\mathrm{reg}} \tag{10}
$$

其中 $\mathcal{L}_{\mathrm{reg}}$ 包含深度正则化项。为高效利用多视图-时间信息，方法采用**对角线视图-时间采样**（Fig. 4）：相机视角与时间步同步演进，以最少轨迹数捕获时空信息，最小化多视图不一致性的暴露。同时，**渐进数据集更新**策略在优化过程中逐步替换监督帧，防止过度平滑，使衣物褶皱等高频纹理保持清晰（Fig. 11c消融验证）。优化使用AdamW，恒定学习率 $1\times10^{-5}$，共25k次迭代。

![[assets/figures/papers/paper_list_l1007_https_arxiv_org_abs_2602_19089/figures/007_Figure_6.jpg]]
*Figure 6: Comparison on other video re-rendering methods. (a) original rendering x; (b-f) competitive sampling methods; (g) our results x∗. Only our self-guided stochastic sampling can generate sharp details while preserving the original identity well*

![[assets/figures/papers/paper_list_l1007_https_arxiv_org_abs_2602_19089/figures/011_Figure_8.jpg]]
*Figure 8: Ablation study on motion field. Our layered motion (right) captures intricate hand details, while the single-layer baseline (left) fails*

## 实验与关键发现

### 主实验结果

我们在ActorsHQ数据集上将ANI3DHUMAN与当前代表性方法进行了全面对比。定量结果（Table 1）显示，本文方法在所有评估维度上均取得最优性能。在图像质量方面，FID达到**105.3**，相比最强基线LHM（124.1）提升了18.8；PSNR为20.08，SSIM为0.8312，LPIPS为0.2125。在身份保持方面，CLIP-Identity达到**0.9160**，优于LHM的0.9009。视频时序一致性指标FVD为295.2，同样领先所有对比方法。

![[assets/figures/papers/paper_list_l1007_https_arxiv_org_abs_2602_19089/figures/008_Table_1.jpg]]
*Table 1: Quantitative results with the state-of-the-art methods of human animation in ActorsHQ [23] dataset*

定性对比（Figure 5）进一步揭示了各方法的本质差异。**Disco4D**和**SV4D 2.0**虽然能生成一定的非刚性动态，但整体渲染质量较低，细节模糊。**PERSONA**在姿态驱动下可直接生成视频，却存在严重的身份漂移问题——生成人物的面部特征与参考图像明显不一致。**LHM**仅依赖网格变形，虽能较好保持身份，但完全无法建模衣物褶皱、裙摆飘动等非刚性动态。本文方法是唯一在保持高保真身份的同时生成真实非刚性动态的方案。

用户研究（Table 2）在全新运动序列上评估了各方法的主观质量。ANI3DHUMAN在身份保持（40.1%）、帧质量（35.3%）、运动真实感（35.3%）、物理合理性（61.8%）四个维度均获得最高偏好，综合偏好率达到**54.4%**，远超PERSONA（22.1%）和LHM（17.6%）。物理合理性维度优势尤为突出（61.8%），表明分层运动表示有效解耦了刚性与非刚性运动，使生成的衣物动态更符合物理直觉。

![[assets/figures/papers/paper_list_l1007_https_arxiv_org_abs_2602_19089/figures/009_Table_2.jpg]]
*Table 2: User study on human animation with novel motion*

### 视频恢复采样方法对比

自引导随机采样是本文方法的核心组件。我们将其与SDEdit、FlowEdit、MCS等竞争采样方法在相同的Flow-Matching基础模型和噪声水平下进行了公平对比（Figure 6）。结果表明，确定性Flow-ODE在处理粗渲染输入时会产生明显伪影和模糊，而纯随机采样虽能改善清晰度，却难以保持原始身份。SDEdit和FlowEdit在身份保持和细节生成之间存在折衷，MCS则倾向于过度平滑。仅本文的自引导随机采样能在生成清晰非刚性细节（如衣物纹理、褶皱）的同时，严格保持输入的身份特征。

### 消融实验

**自引导与随机性的关键作用。** 我们系统消融了采样策略的两个核心组件（Figure 7, Table 4）。移除随机采样（仅保留自引导）导致FVD从295.2恶化至349.7，生成结果出现明显模糊和伪影，验证了随机SDE在纠正OOD输入分布偏差中的必要性（与Figure 3的理论分析一致）。移除自引导（仅保留随机采样）虽略微改善FID，但CLIP-Identity从0.8838骤降至**0.8220**，身份信息严重丢失——生成人物面部特征与参考图像出现明显不一致。这证实了基于掩码的后验均值引导（Eq. 10）是保持身份的关键机制。使用通用扩散先验替代个性化扩散先验会引入轻微性能退化，但整体框架仍保持鲁棒。

**分层运动表示。** 将分层运动场替换为单层运动场（仅网格变形或仅非刚性场）后（Figure 8），手部细节丢失，非刚性变形不自然，表明显式网格变形提供的刚性运动骨架对指导残差场学习至关重要。

**对角线视图-时间采样。** 与固定视图采样相比，对角线采样策略（Figure 4, Figure 9）能产生更锐利的细节并减少漂浮伪影。其核心优势在于以最少轨迹数同时捕获时空信息，最小化多视图不一致性的暴露。

**渐进数据集更新。** 移除渐进更新机制后（Figure 11c），优化结果趋于过度平滑，衣物褶皱等高频纹理细节丢失。渐进更新通过逐步引入恢复视频的监督信号，有效防止了4DGS对扩散模型输出的过拟合。

### 方法定位与对比

Table 3从动画表示、运动类型、优化过程等维度系统对比了各类人体动画方法。传统运动学方法（如LHM）仅支持刚性变形，无需优化但缺乏动态细节。基于SDS监督的方法（如Disco4D）可建模非刚性运动，但受限于扩散模型的随机梯度质量。视频扩散方法（如PERSONA）直接生成动画，但身份保持困难。本文方法通过“恢复粗渲染”范式，将运动学先验与扩散先验有机结合，在刚性运动基础上通过优化学习非刚性残差，实现了身份保持与动态丰富性的统一。

### 失败模式与局限性

尽管ANI3DHUMAN在整体性能上表现优异，仍存在以下局限。首先，最终的4DGS表示因高斯原语的离散性，可能导致极高频纹理细节相比源视频略有平滑。其次，动画质量依赖底层SMPL参数估计的准确性——不准确的SMPL拟合会引入空间对齐误差，导致非刚性运动学习出现偏差。此外，单次视频恢复采样仍需约67秒，虽优于PERSONA的逐帧优化，但尚未达到交互速率。在极端视角或高度复杂的多服装交互场景下，自引导机制的鲁棒性有待进一步验证（需人工确认具体边界条件）。

![[assets/figures/papers/paper_list_l1007_https_arxiv_org_abs_2602_19089/figures/001_Figure_1.jpg]]
*Figure 1: Given a reference human image and a target SMPL mesh sequence, our method synthesizes photorealistic 3D human animation. Unlike the previous state-of-the-art (SOTA) methods (e.g., LHM [58] (top-right)) that are limited to rigid motion, our ANI3DHUMAN (bottom) can further generate high-fidelity nonrigid dynamics, capturing the natural flow of the dress*

## 定位与知识库关联

### 问题定位与核心瓶颈

三维人体动画长期面临一个根本性矛盾：运动学驱动的方法（如 **LHM**）能严格保持身份一致性，但只能产生刚性变形，完全缺乏衣物褶皱、裙摆飘动等非刚性动态；而基于视频扩散模型直接生成的方法（如 **PERSONA**）虽能产生丰富的动态纹理，却伴随严重的身份漂移和时序伪影。**ANI3DHUMAN** 的核心洞察在于，这一矛盾并非不可调和——关键在于将“身份保持”与“动态生成”解耦到不同的表示层次，并通过一个鲁棒的视频恢复机制将二者重新耦合。

### 方法谱系中的位置

从技术路线看，ANI3DHUMAN 处于三个研究方向的交汇点：

**1. 运动学驱动的三维人体动画**

传统方法（**LHM** 等）通过 SMPL 网格变形直接驱动三维表示（如 3D 高斯），身份保持天然成立，但衣物动态完全缺失。这类方法构成了 ANI3DHUMAN 的刚性运动基底——本文的“粗渲染”正是来自这一管线。

**2. 基于扩散先验的 4D 重建与动画**

**Disco4D** 和 **SV4D 2.0** 利用 SDS（Score Distillation Sampling）或多视图扩散模型从单目视频重建 4D 表示，但生成质量受限，且身份保持不稳定。**PERSONA** 更进一步，将姿态条件视频扩散模型与可微渲染联合优化，试图同时处理刚性与非刚性运动，但其直接生成范式导致身份漂移成为系统性问题。ANI3DHUMAN 继承了利用扩散先验提供监督的思路，但将扩散模型的角色从“直接生成器”转变为“粗渲染恢复器”，从根本上改变了扩散模型的使用方式。

**3. 可控视频生成与采样策略**

在视频扩散模型的采样层面，ANI3DHUMAN 与 **SDEdit**、**FlowEdit**、**MCS** 等方法形成竞争关系。这些方法均试图从退化或编辑后的输入恢复高质量视频，但均基于确定性 Flow-ODE 采样。本文的关键发现是：当输入为 OOD（out-of-distribution）的粗渲染时，确定性采样无法校正分布偏差（Fig. 3），导致采样轨迹偏离正确方向。这一洞察直接催生了自引导随机 SDE 采样的设计。

### 核心创新与因果机制

ANI3DHUMAN 的方法创新可归纳为三个因果链环环相扣的设计：

**分层运动表示（解耦瓶颈）**：将运动显式分解为网格驱动的刚性运动（保持身份与结构）和 Hexplane/MLP 参数化的残差非刚性场（建模衣物动态）。消融实验（Fig. 8）证实，使用单层运动场会导致手部细节丢失和非刚性变形不自然，验证了分层解耦的必要性。

**自引导随机采样（恢复瓶颈）**：这是本文最具原创性的贡献。其因果逻辑为：粗渲染 $y$ 是 OOD 输入 → 注入噪声至时间 $t$ 得到 $x_t = \sigma_t \epsilon + (1-\sigma_t)y$ → 使用带扩散项的 SDE 采样 $d\pmb{x} = \pmb{v}_t(\pmb{x}_t, t)dt + g(t)d\pmb{w}_t$ 校正 OOD 误差 → 同时施加基于 DPS 近似的自引导 $\hat{\pmb{x}}_{0|t} \leftarrow \hat{\pmb{x}}_{0|t} - \lambda\nabla_{\pmb{x}_t}||\mathcal{M}\odot(\pmb{y} - \hat{\pmb{x}}_{0|t})||^2$ 保持身份。消融实验（Table 4）给出了决定性证据：移除随机采样导致 FVD 从 295.2 升至 349.7，生成结果模糊；移除自引导使 CLIP-Identity 从 0.8838 骤降至 0.8220，身份严重丢失。

**对角线视图-时间采样与渐进优化（耦合瓶颈）**：在 4D 优化阶段，对角线采样（Fig. 4）以最少轨迹数同时捕获空间与时间信息，最小化多视图不一致性；渐进数据集更新（Fig. 11c）防止过度平滑，保留高频纹理。这两项设计确保恢复视频的监督信号能有效传递到残差运动场和 3D 高斯表示。

### 适用边界与局限

**技术依赖链**：ANI3DHUMAN 的性能受限于底层模块的质量——3D 高斯重建依赖 LHM 的精度，刚性运动依赖 SMPL 参数估计的准确性。SMPL 估计不准确时，粗渲染与真实姿态之间存在空间对齐误差，自引导机制可能因掩码区域错位而失效。

**表示能力边界**：最终的 4DGS 表示因高斯原语的离散性，对极高频纹理（如细密织物纹理）存在轻微平滑效应，与源视频相比仍有可感知的细节损失。

**计算效率**：视频恢复的单次采样仍需约 67 秒，虽优于 PERSONA 的整体时间，但远未达到交互速率。这是扩散模型采样在实时应用中的固有瓶颈。

### 开放问题

1. **采样加速**：能否结合少步采样技术（如一致性蒸馏）将视频恢复时间压缩至秒级，使系统达到交互帧率？

2. **极端条件下的鲁棒性**：在极端视角（如俯仰角 > 60°）或高度复杂的多层服装交互（如外套与裙摆的独立运动）下，自引导机制是否仍能保持身份一致性？当前实验覆盖的场景尚不足以给出结论性判断。

3. **监督信息损失量化**：从扩散模型恢复视频到 4DGS 表示的蒸馏过程中，存在不可避免的信息损失。如何量化并控制这一损失，建立恢复质量与最终动画质量之间的定量关系，是一个尚未探索的理论问题。

4. **多角色扩展**：分层运动表示和自引导采样的设计是否可推广至多人物交互场景？多角色间的遮挡和相互运动耦合将引入新的分布偏移，对采样策略的鲁棒性提出更高要求。

5. **与物理仿真的融合**：当前残差运动场完全由数据驱动，缺乏物理约束（如布料力学）。将物理先验融入残差场的学习过程，可能进一步提升非刚性动态的物理合理性，尤其是在训练数据覆盖不足的运动模式上。

## 原文 PDF

![[paperPDFs/CVPR_2026/Ani3DHuman_Photorealistic_3D_Human_Animation_with_Self_guided_Stochastic_Sampling.pdf]]
