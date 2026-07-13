---
title: "CamDirector: Camera Trajectory Control for Long-term Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arXiv_2026/CamDirector_Camera_Trajectory_Control_for_Long_term_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- CamDirector
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 混合warping方案（Hybrid Warping Scheme）通过世界缓存（world cache）显式集成全源视频的静态三维信息，与历史引导的自回归扩散模型（history-guided autoregressive diffusion）联合，前者提供全局一致的粗帧对齐，后者以渐进式缓存更新和段间历史信号传递确保长视频的时序连贯。
primary_logic: 将场景显式解耦为动态与静态区域，把静态区域融合为统一的点云世界缓存并渲染至目标视角，与直接warp的动态区域通过深度比较进行融合，生成高度完整且源对齐的粗帧；在此基础上，通过历史片段引导的segment-wise自回归生成与渐进式世界缓存更新，有效解决了长视频 VTE 中的全局对齐与自一致性难题。
claims:
- 混合warping将场景分为动静区域，动态区域一对一warp保留运动，静态区域构建世界缓存并渲染至目标视角，最后通过深度比较合并形成完整的粗帧。
- 历史引导自回归生成在每一去噪步中同时处理历史片段与当前片段，较干净的历史引导当前去噪，并每次生成后更新世界缓存以强化已填充区域，确保长期一致。
- 消融实验证实各组件高度因果：移除混合warping使PSNR骤降至12.18；取消历史引导使PSNR降至13.39并降低一致性；关闭渐进式缓存更新进一步使PSNR跌至12.86。
- iPhone-PTZ (full video) 上 LPIPS ↓ = 0.4752
---

# CamDirector: Camera Trajectory Control for Long-term Video Generation

> [!tip] 核心洞察
> 将场景显式解耦为动态与静态区域，把静态区域融合为统一的点云世界缓存并渲染至目标视角，与直接warp的动态区域通过深度比较进行融合，生成高度完整且源对齐的粗帧；在此基础上，通过历史片段引导的segment-wise自回归生成与渐进式世界缓存更新，有效解决了长视频 VTE 中的全局对齐与自一致性难题。

| 字段 | 内容 |
|------|------|
| 中文题名 | CamDirector：面向长视频生成的相机轨迹控制 |
| 英文题名 | CamDirector: Camera Trajectory Control for Long-term Video Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.02256) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | CamDirector |
| Dataset | iPhone-PTZ, iPhone |

> [!tip] 效果简介
> - iPhone-PTZ (full video) 上，LPIPS ↓ 0.4752 vs 0.5497 (Gen3C) (-0.0745)；FID ↓ 72.33 vs 86.21 (Gen3C) (-13.88)；Subject Consistency ↑ 0.8574 vs 0.8228 (Gen3C) (+0.0346)。
> - iPhone (short clip) 上，Background Consistency ↑ 0.9489 vs 0.8900 (Gen3C) (+0.0589)。

## 概要

视频轨迹编辑（Video Trajectory Editing, VTE）旨在根据给定的源视频与目标相机轨迹，生成具有全新相机运动、同时保持源场景内容与运动一致性的新视频。现有方法主要沿两条技术路线展开：一类基于嵌入注入（embedding injection），将相机位姿嵌入扩散模型的条件空间，但受限于嵌入层容量，难以精确跟随复杂的相机轨迹；另一类基于逐帧warping（per-frame warping）与修复，通过双向注意力隐式聚合跨帧信息，但在处理长视频时因分块处理丢失全局注意力，导致源内容对齐偏差与生成片段间的时间闪烁。

**CamDirector** 针对上述瓶颈，提出了一套以**混合warping方案（Hybrid Warping Scheme）** 与**历史引导的自回归扩散模型（History-Guided Autoregressive Diffusion）** 为核心的框架。其核心洞察在于：将场景显式解耦为动态区域与静态区域——动态区域通过逐帧warping保留运动保真度，静态区域则跨帧聚合为统一的点云**世界缓存（world cache）** 并渲染至目标视角，经深度融合生成全局一致的粗帧。在此基础上，采用segment-wise自回归生成，每一去噪步同时处理历史片段与当前片段，以更干净的历史信号引导当前去噪，并在每段生成后渐进更新世界缓存，从而有效解决长视频VTE中的全局对齐与自一致性难题。

实验表明，CamDirector 在 iPhone 和 iPhone-PTZ 两个基准上全面超越现有SOTA方法，同时仅需 2.0B 参数（对比方法为 5.3B–6.7B）。在 iPhone-PTZ 全视频上，LPIPS 降至 0.4752（Gen3C 为 0.5497），FID 降至 72.33（Gen3C 为 86.21）；VBench 感知质量指标上，背景一致性达 0.9489，主体一致性达 0.8574，均显著领先。消融实验进一步证实：移除混合warping导致PSNR骤降至12.18，取消历史引导与渐进式缓存更新分别使PSNR降至13.39与12.86，验证了各组件的因果贡献。

视频轨迹编辑（Video Trajectory Editing, VTE）的目标是，给定一段源视频和一条新的相机运动轨迹，生成一段内容与源视频一致但相机视角沿目标轨迹运动的视频。这一任务在影视创作、虚拟现实和视频重定向等领域具有广泛应用前景，其核心挑战在于：如何在精确跟随目标相机轨迹的同时，保持生成视频的源内容对齐与长程时序一致性。

现有VTE方法可大致分为两条技术路线。其一是**基于嵌入注入（embedding injection）的方法**，如RecamMaster，将目标相机位姿编码为嵌入向量注入扩散模型，通过条件信号引导生成。这类方法受限于嵌入层的表示容量，难以可靠地跟随大范围、多样化的相机运动轨迹，在目标位姿与源位姿差异显著时容易出现视角偏离。其二是**基于单帧warping的方法**，如Gen3C和TrajectoryCrafter，通过对源视频逐帧进行3D warping得到粗帧，再以粗帧为条件进行扩散生成修复。这类方法在短片段上表现良好，但在长视频场景中面临根本性困难：分块处理策略导致各片段独立生成，缺乏跨片段的全局注意力机制，使得粗帧构建时无法利用全源视频的互补信息，造成源内容对齐偏差与生成片段间的时间闪烁。

上述两类方法的共同瓶颈可归结为：**缺乏一个既能提供全局一致的场景参照、又能保证长程时序连贯的生成机制**。单帧warping隐式依赖双向注意力聚合跨帧信息，但在长视频中这种隐式聚合随片段增长而衰减；嵌入注入方法则完全放弃了显式的几何约束，将相机控制完全托付给嵌入层的泛化能力。因此，如何在长视频VTE中实现精确的相机轨迹控制与稳定的内容一致性，成为该领域亟待解决的关键问题。

本文提出CamDirector，通过两个核心设计突破上述瓶颈：（1）**混合warping方案（Hybrid Warping Scheme）**，将场景显式解耦为动态区域与静态区域，对动态区域直接warping以保留运动保真度，对静态区域构建统一的点云**世界缓存（world cache）**并渲染至目标视角，再通过深度比较融合，生成全局一致且源对齐的粗帧；（2）**历史引导的自回归扩散模型（history-guided autoregressive diffusion）**，在每一去噪步中同时处理历史片段与当前片段，以较干净的历史信号引导当前片段的去噪过程，并配合渐进式世界缓存更新，将新修复的静态区域持续融入缓存，为后续片段提供更完整的场景参照。这一设计从根本上解决了长视频VTE中的全局对齐与自一致性难题。

## 核心方法与创新机理

CamDirector 针对现有视频轨迹编辑（VTE）方法在精确相机控制与长程一致性上的根本瓶颈，提出了两个耦合的核心创新：**混合warping方案（Hybrid Warping Scheme）** 与**历史引导的自回归生成（History-Guided Autoregressive Generation）**。前者解决粗帧全局对齐问题，后者确保长视频的时序连贯性。

### 创新一：混合warping方案——动静解耦的全局粗帧构建

现有基于单帧warping的方法（如 Gen3C、TrajectoryCrafter）逐帧独立地将源视角映射到目标视角，依赖扩散模型的双向注意力隐式聚合跨帧信息。然而，当相机轨迹变化剧烈或视频较长时，单帧warping因缺乏全局信息而无法覆盖被遮挡或超出当前帧视野的静态区域，导致粗帧出现大面积空洞与内容偏差（Figure 2）。

CamDirector 的混合warping方案将场景**显式解耦为动态区域与静态区域**，并对两者采用截然不同的处理策略：

- **动态区域一对一warping**：对每一源帧的动态前景区域，通过相机位姿变换与点云投影直接映射到目标视角，保留运动保真度。其数学形式为：
  
  $$I_i^{d,t}, Z_i^{d,t}, M_i^{d,t} = \Phi( \Pi_i^t \cdot (\Pi_i^s)^{-1} \cdot ( [P_i, I_i^s] \odot M_i^d ) )$$
  
  其中 $\Pi_i^s$、$\Pi_i^t$ 分别为源视角与目标视角的相机位姿，$P_i$ 为源帧的点云，$M_i^d$ 为动态区域掩膜，$\Phi$ 为投影与渲染操作。

- **静态区域世界缓存聚合与渲染**：将所有源帧的静态区域逐步聚合为一个统一的点云——**世界缓存（world cache）**，然后从目标相机位姿渲染该缓存，获得全局一致的静态背景粗帧。这相当于利用全源视频的三维静态信息，为每一目标帧提供完整的背景参照。

- **深度融合**：将动态区域warping结果与静态区域渲染结果通过深度比较进行合并，生成高度完整且源对齐的粗帧。

这一设计的核心洞察在于：**将场景的动静区域显式分离，使静态信息得以跨帧聚合，从根本上克服了单帧warping的信息孤岛问题**。消融实验强有力地验证了该创新的因果效应——移除混合warping后，PSNR 从 13.99 骤降至 12.18，LPIPS 从 0.4752 升至 0.5347（Table 3），证明其是粗帧全局对齐的核心要素。

### 创新二：历史引导自回归生成——跨段一致性的显式建模

现有VTE方法处理长视频时通常采用分块策略，各片段独立生成，缺乏显式的跨段一致性约束，导致片段间出现时间闪烁与内容跳变。CamDirector 通过**历史引导的自回归扩散机制**与**渐进式世界缓存更新**联合解决这一问题。

**历史引导的去噪过程**：将长视频切分为连续片段，在每一去噪步中同时处理历史片段（已生成的前 $T^*$ 帧）与当前片段（待生成的 $T$ 帧）。历史片段的噪声状态领先当前片段 $\Delta t$ 步，通过分类器自由引导的流预测将更干净的历史信号注入当前去噪：

$$v_t = w \times v_\theta( x_{t-1}^k | x_{t+\Delta t}^{k-1} ) + (1-w) \times v_\theta( x_{t-1}^k | x_{t-1}^{k-1} )$$

其中 $x^{k-1}$ 为历史片段的噪声状态，$x^k$ 为当前片段的噪声状态，$w$ 为引导权重。这一设计使得当前片段的生成始终以已生成的真实历史为条件，而非仅依赖粗帧的弱先验。

**渐进式世界缓存更新**：每生成一个新片段，从其中均匀采样 $C$ 帧作为锚点，将新修复的静态区域融合进世界缓存，为后续片段的粗帧构建提供更完整的参照（Figure 5）。这形成了“生成-更新-参照”的正向循环：越往后的片段，世界缓存越完整，粗帧质量越高。

消融实验分别验证了这两个子组件的独立贡献与协同效应（Table 4）：
- 取消历史引导使 PSNR 降至 13.39，Subject Consistency 降至 0.8543；
- 关闭渐进式缓存更新使 PSNR 进一步跌至 12.86；
- 两者同时移除的退化幅度大于各自单独移除之和，证明它们存在正向协同。

### 创新三：多模态条件扩散模型（CCDM）——更强的源内容与视角约束

作为上述创新的基座，CamDirector 设计了**粗视频控制扩散模型（CCDM）**，在条件输入上相比基线有显著增强：

| 条件槽位 | 基线方法 | CamDirector |
|---------|---------|-------------|
| 粗帧条件 | 无或简单warping帧 | 混合warping生成的粗视频，通过 ControlNet 注入 |
| 源内容条件 | 仅依赖粗帧的隐式信息 | 源帧 token 与目标 token 拼接，经 LoRA 适配输入基础 T2V 模型 |
| 相机位姿条件 | 嵌入注入（受限于嵌入层容量） | Plücker 嵌入，提供精确的逐像素射线几何约束 |

消融实验表明（Table 3），去掉 Plücker 条件使 PSNR 降至 13.18，去掉源帧条件使 PSNR 降至 13.04，证明额外的相机与源内容条件信号对精确轨迹跟随不可或缺。值得注意的是，CamDirector 的模型参数仅 2.0B，显著小于对比方法（5.3B–6.7B），却在更低的容量下实现了更优的定量与定性结果，排除了参数规模带来的不公平优势。

### 创新总结

CamDirector 的三个创新形成了清晰的因果链条：混合warping 提供全局一致的粗帧先验 → CCDM 的多模态条件将粗帧、源内容、相机位姿强约束注入扩散过程 → 历史引导自回归生成以历史真实信号和渐进更新的世界缓存确保长程一致性。这一设计有效解决了现有 VTE 方法中“全局对齐偏差”与“片段间时间闪烁”两大核心瓶颈。

CamDirector 的整体 pipeline 围绕一个核心洞察展开：将源视频的场景显式解耦为动态区域与静态区域，并分别以不同策略处理，从而在长视频轨迹编辑中同时实现精确的相机控制与长程时序一致性。框架由两大阶段串联构成：**混合warping粗帧构建** 与 **历史引导自回归生成**，二者通过“世界缓存”这一显式三维表征紧密耦合。

### 模块关系与数据流

如图 Figure 3 所示，系统接收一段源视频、其对应的相机位姿序列以及用户指定的目标相机轨迹作为输入。数据流沿以下路径传递：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_02256/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our framework. Left: The hybrid warping scheme leverages the entire source video to construct coarse frames by processing dynamic and static regions separately, providing a global reference of the original scene content. Right: The CCDM conditions the generation on the coarse video via ControlNet, while source-frame tokens are concatenated with target tokens as inputs to the base T2V model to provide reliable motion and appearance priors*

1. **动静解耦与混合warping（Section 3.1）**  
   首先，源视频的每一帧被分解为动态区域与静态区域。动态区域（如移动的人物或车辆）采用逐帧一对一 warping 的方式直接投影到目标视角，以完整保留运动保真度。静态区域（如背景建筑、地面）则被渐进式聚合为一个统一的点云表征——**世界缓存**，随后根据目标相机位姿渲染到目标视角。最后，动态 warping 结果与静态渲染结果通过深度比较进行融合，生成全局一致且源对齐的**粗帧**序列。这一混合策略从根本上解决了单帧 warping 因缺乏全局信息而导致的空洞与对齐偏差问题（见 Figure 2 对比）。

2. **CCDM 基础模型（Section 3.2）**  
   粗帧序列进入**粗视频控制扩散模型**。CCDM 以预训练视频扩散模型 Wan-T2V-1.3B 为骨干，通过 ControlNet 接收粗视频作为空间引导，同时将源帧 token 与目标帧 token 拼接输入，并以目标相机位姿的 Plücker 嵌入作为显式视角条件。这种三重条件设计（粗视频结构 + 源内容先验 + 相机位姿）使模型在短片段生成中即可实现精细的纹理修复与视角一致性。

3. **历史引导自回归生成（Section 3.2）**  
   对于长视频，系统将视频切分为连续的时间片段。在每个去噪步中，上一片段已生成的“干净”历史帧与当前片段的噪声帧被联合处理：历史帧的噪声状态领先当前帧 $\Delta t$ 步，通过分类器自由引导的流预测机制（公式 (2)）向当前片段传递时序一致性信号。每生成完一个片段，系统会从中采样锚帧，将新修复的静态区域融合进世界缓存（Figure 5），使后续片段的粗帧构建拥有更完整的场景参照。这一“生成-更新”循环在片段间滚动推进，直至完整长视频生成完毕。

### 关键设计决策的因果链条

框架设计的因果逻辑可归纳为以下链条：

- **瓶颈**：现有 VTE 方法在长视频场景中因分块处理丢失全局注意力，导致源内容对齐偏差与片段间时间闪烁。
- **因果旋钮**：引入显式的世界缓存，将全源视频的静态三维信息作为全局锚点，配合历史引导的自回归扩散机制传递跨段时序信号。
- **效果**：混合 warping 提供全局一致的粗帧基底；历史引导确保片段间平滑过渡；渐进式缓存更新使场景表征随生成推进而逐步完整，三者协同解决了长视频 VTE 中的全局对齐与自一致性难题。

消融实验为上述因果链条提供了强证据支撑：移除混合 warping 后 PSNR 骤降至 12.18（Table 3）；取消历史引导使 PSNR 降至 13.39 并降低 Subject Consistency（Table 4）；关闭渐进式缓存更新进一步使 PSNR 跌至 12.86（Table 4）。这些结果表明，三个模块各自承担不可替代的功能，且其协同效应是方法性能的核心来源。

CamDirector 的核心架构由两个关键模块构成：**混合warping方案（Hybrid Warping Scheme）** 与 **历史引导的自回归生成（History-Guided AutoRegressive Generation）**。前者负责从源视频构建全局一致的粗帧，后者以粗帧为条件，通过段间历史信号传递实现长视频的时序连贯生成。

### 3.1 混合warping方案

现有VTE方法普遍采用逐帧warping策略，仅通过双向注意力隐式聚合跨帧信息，导致粗帧构建不完整且源内容对齐偏差显著。CamDirector提出将场景显式解耦为动态区域与静态区域，并采用差异化处理策略。

**动态区域warping**：对每一源帧的动态区域，通过相机位姿变换与点云投影直接映射到目标视角，以保留运动保真度。其核心变换公式为：

$$I_i^{d,t}, Z_i^{d,t}, M_i^{d,t} = \Phi( \Pi_i^t \cdot (\Pi_i^s)^{-1} \cdot ( [P_i, I_i^s] \odot M_i^d ) )$$

其中，$I_i^s$为源帧$i$的RGB图像，$P_i$为对应的点云，$M_i^d$为动态区域掩膜；$\Pi_i^s$与$\Pi_i^t$分别表示源视角与目标视角的相机投影矩阵；$\Phi$为投影与渲染算子。该公式输出warp后的RGB图像$I_i^{d,t}$、深度图$Z_i^{d,t}$及有效像素掩膜$M_i^{d,t}$。

**静态区域世界缓存**：与动态区域的一对一warping不同，静态区域被渐进式聚合为统一的点云表示——世界缓存（world cache）。该缓存集成了全源视频的静态三维信息，随后被渲染至目标相机位姿。最后，动态warping结果与静态渲染结果通过深度比较进行融合，生成高度完整且源对齐的粗帧。

Figure 2 直观对比了逐帧warping与混合warping的效果差异：混合warping产生的粗帧更完整，空洞区域显著减少。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_02256/figures/002_Figure_2.jpg]]
*Figure 2: Visual comparison between per-frame warping (a), our hybrid warping (b), and ground truth (c). Hybrid warping tends to produce more complete and source-aligned coarse frames*

### 3.2 历史引导的自回归生成

长视频生成的核心挑战在于跨段时序一致性。CamDirector设计了历史引导的自回归扩散模型，将长视频切分为连续片段，在生成当前片段时显式利用已生成的历史片段作为引导信号。

**CCDM基座模型**：以预训练视频扩散模型Wan-T2V-1.3B为基础，通过ControlNet注入粗视频条件，同时将源帧token与目标帧token拼接作为输入，辅以目标相机位姿的Plücker嵌入。这一多模态条件设计确保生成过程同时受粗视频结构、源内容外观与目标视角的强约束。

**历史引导去噪**：在每一去噪步中，两个连续片段（历史片段与当前片段）被同时处理。历史片段的噪声状态领先当前片段$\Delta t$步，通过分类器自由引导（classifier-free guidance）机制将干净的历史信息注入当前去噪过程。其预测流公式为：

$$v_t = w \times v_\theta( x_{t-1}^k | x_{t+\Delta t}^{k-1} ) + (1-w) \times v_\theta( x_{t-1}^k | x_{t-1}^{k-1} )$$

其中，$x_{t-1}^k$表示当前片段$k$在去噪步$t-1$的噪声状态，$x_{t+\Delta t}^{k-1}$为历史片段$k-1$在更干净噪声水平$t+\Delta t$的状态；$v_\theta$为模型预测的流向量；$w$为引导权重。该机制使历史片段的干净信息成为当前去噪的条件锚点，有效抑制段间时序闪烁。

**渐进式世界缓存更新**：每生成一个新片段后，从该片段均匀采样$C$帧作为锚帧，将其中新修复的静态区域融合进世界缓存。更新后的缓存为下一片段的粗帧构建提供更完整的静态场景参照，形成正向反馈循环。Figure 5 展示了这一渐进更新过程，新融合区域以红色高亮。

Figure 3 与 Figure 4 分别呈现了整体框架概览与历史引导自回归生成的完整流程。消融实验证实：取消历史引导使PSNR降至13.39，关闭渐进式缓存更新使PSNR进一步跌至12.86，验证了两组件各自及协同提升长程一致性的因果作用。

## 实验与关键发现

CamDirector 的实验评估围绕两个核心维度展开：**短片段与全视频的定量/定性对比**，以及**各组件的消融验证**。评估在原有 iPhone 基准和新提出的 iPhone-PTZ 基准上进行——后者引入了更大范围的相机运动与轨迹变化，对方法的泛化能力提出更高要求。

### 主结果：SOTA 性能与参数效率

在 iPhone-PTZ 全视频基准上，CamDirector 以仅 **2.0B** 参数（对比方法为 5.3B~6.7B）取得了全面的 SOTA 超越。如 Table 1 所示，与基于 warp-and-inpaint 的 SOTA 方法 **Gen3C** 相比，CamDirector 将 LPIPS 从 0.5497 降至 **0.4752**（降幅 13.5%），FID 从 86.21 降至 **72.33**（降幅 16.1%）。在短片段场景中，PSNR 达到 **13.78**，同样优于所有对比方法。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_02256/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison on iPhone and iPhone-PTZ benchmark. Results for short clips are on the left, full videos are on the right. The best results are highlighted in bold*

Table 2 的 VBench 感知质量指标进一步揭示了性能优势的来源：在 iPhone 短片段上，Background Consistency 达到 **0.9489**（Gen3C 为 0.8900），Subject Consistency 达到 **0.9400**；在更具挑战的 iPhone-PTZ 全视频上，Subject Consistency 仍保持 **0.8574**，显著优于 Gen3C 的 0.8228。这表明混合 warping 提供的全局一致粗帧与历史引导自回归机制共同作用，有效抑制了长视频生成中的内容漂移与时间闪烁。

值得注意的是，CamDirector 在参数规模显著更小的情况下实现了上述优势，排除了“以更大模型换取更好性能”的不公平竞争。

### 消融实验：各组件的因果贡献

消融实验系统性地验证了三个关键设计选择的因果作用。

**混合 warping 是粗帧全局对齐的核心。** Table 3 显示，移除混合 warping（退化为 per-frame warping）导致 PSNR 骤降至 **12.18**，LPIPS 升至 0.5347。这一定量退化在 Figure 9 的定性对比中表现为粗帧出现大面积空洞与源内容错位，最终生成视频的静态区域严重失真。混合 warping 通过世界缓存将全源视频的静态三维信息显式集成，弥补了 per-frame warping 因分帧处理而丢失的全局参照。

**历史引导与渐进式缓存更新协同保障长程一致性。** Table 4 的消融表明：取消历史引导使 PSNR 降至 **13.39**，Subject Consistency 降至 0.8543；关闭渐进式世界缓存更新则使 PSNR 进一步跌至 **12.86**。Figure 10 的可视化对比直观展示了这一退化——无缓存更新的变体在长视频末尾出现明显的几何错位，而无历史引导的变体则产生与源内容不一致的纹理。两者各自并协同地解决了长视频生成中的自一致性难题。

**多模态条件信号不可或缺。** Table 3 还显示，去掉 Plücker 相机位姿嵌入或源帧拼接条件分别使 PSNR 降至 ~13.04–13.18，LPIPS 升至 ~0.4897。这证明 CCDM 对目标视角的强约束（Plücker 嵌入）与对源内容外观的保持（源帧 token）是精细修复质量的双重保障。

### 失败模式与局限性

尽管 CamDirector 在定量指标上表现优异，论文明确指出了两个局限性：

1. **复杂纹理区域的过度平滑**：生成视频在具有丰富纹理细节的区域（如织物、自然场景）出现 over-smoothing 现象。其根因在于训练所用的动态多视图数据集本身纹理较为粗糙，而非方法设计缺陷。Figure 7 和 Figure 8 的部分样本可观察到这一现象。
2. **预训练模块的误差累积**：系统依赖 VGGT 深度估计、Pi3 点云估计以及运动分割模型，这些模块的估计误差可能在 pipeline 中传播，影响粗帧构建质量。Figure 6 展示了深度估计修正前后的 warping 质量差异，说明深度精度对最终结果有直接影响。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_02256/figures/009_Figure_8.jpg]]
*Figure 8: Qualitative comparison of full videos on iPhone-PTZ dataset*

### 待验证的开放问题

以下结论来自论文的讨论与展望，其有效性需后续工作验证：

- 引入真实世界静态多视图数据或高级生成对抗训练策略能否显著提升纹理细节与真实感？
- 当前世界缓存更新策略能否自然扩展至包含多个独立运动物体的复杂动态场景？
- 是否存在端到端可学习方案，完全规避显式深度估计与点云重建的中间过程，从而减少误差累积？

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_02256/figures/011_Table_3.jpg]]
*Table 3: Ablation on hybrid warping and CCDM conditions*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_02256/figures/010_Table_4.jpg]]
*Table 4: Ablation on history-guided autoregressive generation*

## 定位与知识库关联

### 1. 与基线方法的关系与关键差异

CamDirector 聚焦于视频轨迹编辑（Video Trajectory Editing, VTE）任务，其设计直接回应了现有两类主流方法的根本性缺陷。

**（1）相对于基于嵌入注入的方法**

以 **RecamMaster** 为代表的嵌入注入方法，试图将相机轨迹信息编码为条件嵌入注入扩散模型。这类方法的控制精度受限于嵌入层的表征容量，在长视频、大轨迹变化场景下无法可靠跟随目标相机路径。CamDirector 完全摒弃了这种间接控制策略，转而采用显式的几何 warping 生成粗帧作为强条件信号，从根本上解除了嵌入容量的瓶颈。

**（2）相对于基于单帧 warping 的方法**

以 **Gen3C** 和 **TrajectoryCrafter** 为代表的 warp-and-inpaint 方法，在短片段上表现尚可，但其核心缺陷在于：仅对每一帧独立执行 warping，缺乏对整个源视频的全局信息聚合。这导致两个连锁问题——（a）粗帧在遮挡区域出现大面积空洞，源内容对齐偏差显著；（b）在长视频场景中，分块处理使得各片段之间失去全局注意力联系，产生严重的时间闪烁（temporal flickering）。

CamDirector 通过两个核心“槽位替换”实现了范式跃迁：

| 设计槽位 | 基线方案 | CamDirector 方案 |
|----------|----------|------------------|
| 粗帧构建策略 | 单帧 warping，隐式跨帧注意力聚合 | 混合 warping：动静区域显式解耦，静态区域构建世界缓存并渲染，动态区域直接 warping，深度融合 |
| 长视频生成机制 | 分块处理，无显式跨段一致性模块 | 历史引导自回归生成 + 渐进式世界缓存更新 |

### 2. 知识库定位与适用边界

**方法谱系定位**：CamDirector 处于“基于几何先验的视频扩散模型可控生成”这一交叉节点。其上游依赖包括：预训练的视频扩散模型（Wan-T2V-1.3B）、深度估计模型（VGGT）、点云估计模型（Pi3）及运动分割模型。下游则面向任意相机轨迹的长视频重渲染。

**适用边界**：
- **适用场景**：源视频包含显著静态背景的场景（如建筑、风景），且目标相机轨迹在源视频观测范围内。iPhone-PTZ 基准上的 SOTA 结果（PSNR 13.99, LPIPS 0.4752, FID 72.33，参数仅 2.0B）验证了其在该边界内的有效性。
- **不适用/弱适用场景**：（1）源视频中静态区域占比极低的纯动态场景，世界缓存的构建基础将严重不足；（2）目标轨迹大幅偏离源视频观测范围的极端外推场景，warping 产生的空洞区域过大，超出扩散模型的合理修复能力。

### 3. 局限性与失败模式

**（1）复杂纹理区域的过度平滑**：生成结果在精细纹理区域出现 over-smoothing 现象。根因在于训练所用的动态多视图数据集本身纹理粗糙，扩散模型未能学习到高频细节的生成能力。这是一个数据侧瓶颈，而非方法设计缺陷。

**（2）上游模块误差的级联传播**：系统依赖 VGGT 深度估计、Pi3 点云重建及运动分割三个预训练模块。任一模块的估计误差（如深度图偏差导致的 warping 错位，见 Figure 6）都会经混合 warping 传播至粗帧，进而通过 ControlNet 条件影响最终生成质量。该 pipeline 缺乏对中间表示的端到端纠错机制。

**（3）动态区域处理的简化假设**：当前方案将动态区域按“一对一 warping”处理，隐式假设动态物体数量有限且运动幅度可控。当场景中包含多个独立运动物体或快速大位移运动时，动态区域的 warping 质量与跨帧一致性可能显著下降。

### 4. 开放问题

1. **纹理质量提升路径**：能否通过引入真实世界静态多视图数据（如 MegaDepth、ScanNet++）或对抗训练策略，在保持几何一致性的前提下显著提升生成纹理的细节与真实感？

2. **多动态物体扩展**：当前世界缓存仅聚合静态区域。能否将缓存机制扩展为“分层世界缓存”——为每个独立运动物体维护独立的动态缓存，并通过场景流将其与静态缓存统一渲染？这需要解决动态物体的跟踪、分割与跨段关联问题。

3. **端到端可学习 warping**：当前显式深度估计与点云重建的中间过程引入了不可微的误差源。是否存在一种端到端的可学习 warping 方案（如基于 3D Gaussian Splatting 的可微分渲染），能够完全规避显式几何估计，从而减少误差累积并提高 pipeline 的鲁棒性？

4. **轨迹控制的细粒度与可编辑性**：当前方法接受目标相机轨迹作为输入，但未提供轨迹的交互式编辑能力。能否将 CamDirector 与自然语言驱动的相机规划模块结合，实现“文本描述→相机轨迹→视频生成”的端到端创作流程？

## 原文 PDF

![[paperPDFs/arXiv_2026/CamDirector_Camera_Trajectory_Control_for_Long_term_Video_Generation.pdf]]
