---
title: "FlowDirector: Training-Free Flow Steering for Precise Text-to-Video Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlowDirector_Training_Free_Flow_Steering_for_Precise_Text_to_Video_Editing.pdf
project_link: "https://flowdirector-edit.github.io"
code_link: null
aliases:
- FlowDirector
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion/diffusion_image_video
- topic/generative_models_diffusion
core_operator: 将视频编辑建模为数据空间中的直接 ODE 演化，绕过 inversion，并通过三个无训练流校正策略（方向感知、运动-外观解耦、差分平均引导）精准控制编辑过程。
primary_logic: 编辑过程可视为在原生时空流形上的 ODE 驱动演化，通过解耦流动中的语义对抗分量、建立正交运动控制平面以及构造差分信号主动规避高方差区域，实现无逆变的精准且稳定的语义变换。
claims:
- FlowDirector 在多项指标上显著超过现有无训练基线，包括文本对齐、时序一致性和背景保存。
- 方向感知流校正通过正交分解流场，主动抑制与源语义对齐的分量并放大反方向分量，有效打破源视频的“语义引力”。
- 运动-外观解耦校正通过在每个去噪步上优化运动能量函数，将运动一致性建模为可优化的能量项，在保持语义变换的同时传递源运动。
- 差分平均引导通过对比高质量共识估计与高方差基线，提取“噪声漂移”信号，以较低计算成本将轨迹锁定在低方差流形上。
---

# FlowDirector: Training-Free Flow Steering for Precise Text-to-Video Editing

> [!tip] 核心洞察
> 编辑过程可视为在原生时空流形上的 ODE 驱动演化，通过解耦流动中的语义对抗分量、建立正交运动控制平面以及构造差分信号主动规避高方差区域，实现无逆变的精准且稳定的语义变换。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlowDirector：无训练流引导的精准文本到视频编辑 |
| 英文题名 | FlowDirector: Training-Free Flow Steering for Precise Text-to-Video Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.05046) · [Project](https://flowdirector-edit.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion/diffusion_image_video #topic/generative_models_diffusion |
| Method | FlowDirector |
| Dataset | Custom 150 video-text pairs |

> [!tip] 效果简介
> - Custom 150 video-text pairs (Internet + DAVIS) 上，Pick Score (%) ↑ 21.82 vs 21.01 (RAVE) (+0.81)；CLIP-T (×10⁻²) ↑ 34.64 vs 33.56 (FLATTEN) (+1.08)；CLIP-F (×10⁻²) ↑ 97.34 vs 95.48 (VideoDirector) (+1.86)。

## 概要

文本到视频编辑任务的核心挑战在于，如何在精准实现语义变换的同时，严格保持原始视频的运动一致性与背景保真度。当前主流的基于反演（inversion-based）的方法存在一个关键瓶颈：反演步骤引入的近似误差会随时间累积，导致外观漂移、运动闪烁和背景失真。FlowDirector 提出了一种**无训练、无反演**的编辑范式，将视频编辑建模为数据空间中的常微分方程（ODE）直接演化，从根本上规避了反演误差的传播。

该方法的核心洞察是：编辑过程可视为在原生时空流形上的 ODE 驱动演化。通过三个无训练流校正策略——**方向感知流校正（DA-FC）**、**运动-外观解耦校正（MAD-FC）** 和**差分平均引导（DAG）**——FlowDirector 实现了对编辑轨迹的精准控制：DA-FC 通过正交分解编辑流场，主动抑制与源语义对齐的分量并放大反向分量，有效打破源视频的“语义引力”；MAD-FC 将运动一致性建模为可优化的能量函数，在语义变换的同时忠实传递源运动；DAG 则通过对比高质量共识估计与高方差基线，提取差分信号将编辑轨迹锁定在低方差流形上，以较低计算成本消除纹理闪烁和伪影。

在包含 150 个视频-文本对的评测集上，FlowDirector 在文本对齐（CLIP-T）、时序一致性（CLIP-F）、结构保真度（WarpSSIM）和综合编辑质量（Q_edit）等指标上均显著超越 FateZero、FLATTEN、TokenFlow、RAVE 等现有无训练基线。消融实验进一步证实，DA-FC 是语义编辑能力的核心驱动力，MAD-FC 是运动一致性的关键保障，而 DAG 则以高效的多轮推断平均策略提升了编辑稳定性。该方法无需任何训练或微调，在单张 GPU 上即可完成编辑，展现出较强的实用价值。



文本到视频（T2V）生成模型近年来取得了显著进展，尤其是在基于扩散变换器（DiT）架构的视频生成基座模型（如 **Wan** 和 **CogVideoX**）出现之后，高质量的视频生成已不再遥不可及。然而，相比从零生成，对已有视频进行精准的语义编辑——即根据文本提示修改视频中的特定对象或场景，同时保持背景、结构和运动的一致性——仍然是一个极具挑战性的开放问题。

### 现有反演式方法的瓶颈

当前主流的零样本视频编辑方法普遍依赖“反演-编辑”两阶段范式：首先通过 DDIM 反演或流匹配反演将源视频映射到高斯潜在空间，然后以该反演状态为起点，在目标提示的引导下进行去噪生成。这一范式虽然直观，却存在一个根本性的瓶颈：**反演步骤不可避免地引入近似误差**。

具体而言，反演误差在时序维度上会逐帧累积，导致编辑后的视频出现两类典型退化：
1. **外观保真度下降**：反演轨迹无法完美重建源视频，编辑结果中未编辑区域的纹理、颜色和细节发生漂移。
2. **运动一致性受损**：时序反演误差的累积破坏了帧间的运动连续性，表现为闪烁、抖动或运动模式失真。

现有方法如 **FateZero**、**FLATTEN**、**TokenFlow**（基于 T2I 模型）以及 **RAVE**、**VideoDirector**（基于 T2V 模型）均未能从根本上规避这一误差累积问题，它们要么依赖复杂的注意力注入机制来维持外观，要么通过额外的时序约束来抑制闪烁，但这些后处理手段本质上是在“修补”反演误差的后果，而非消除其根源。

### 核心动机：从“反演”到“直接演化”

本文的核心动机在于提出一个根本性的范式转换：**视频编辑是否必须经过反演？** 答案是否定的。

在流匹配（Flow Matching）和修正流（Rectified Flow）的理论框架下，视频生成过程可被建模为数据空间中的常微分方程（ODE）演化。给定一个预训练的 T2V 流模型，其速度场 $v_\theta$ 已经学会了如何将噪声逐步传输到视频数据分布。FlowDirector 的关键洞察在于：**编辑过程同样可以被视为数据空间中的直接 ODE 演化，而非潜在空间中的“反演-重建”循环**。

具体而言，FlowDirector 直接在数据空间构造编辑轨迹：在每个时间步 $t$，并行计算源侧状态 $Z_t^{\mathrm{src}}$ 和目标侧状态 $Z_t^{\mathrm{tar}}$，并以两者速度场之差作为编辑流 $V_{\mathrm{edit}}$，驱动视频从源语义向目标语义平滑演变。这一“直接 ODE”范式从根本上绕过了反演步骤，从而彻底消除了反演误差及其在时序上的累积效应。

### 直接演化面临的新挑战

然而，直接 ODE 范式虽然规避了反演误差，却引入了三个新的核心挑战：

1. **语义引力问题**：原始编辑流 $V_{\mathrm{edit}} = V_{\mathrm{tar}} - V_{\mathrm{src}}$ 中同时包含与源语义“对齐”和“对抗”的分量。对齐分量倾向于将编辑轨迹拉回源语义方向，形成一种“语义引力”，严重削弱编辑强度。
2. **运动-外观耦合问题**：直接 ODE 演化缺乏对运动的显式约束，编辑过程中目标的运动模式容易发生偏差或扭曲，而简单的外观锚定又会抑制语义变换本身。
3. **速度场高方差问题**：单次采样的编辑速度估计存在较高的随机方差，导致编辑轨迹偏离低方差流形，表现为纹理闪烁、伪影等时序不稳定现象。

FlowDirector 通过三个无训练流校正策略——**方向感知流校正（DA-FC）**、**运动-外观解耦校正（MAD-FC）** 和 **差分平均引导（DAG）**——分别针对上述三个挑战进行精准调控，从而在无训练、无反演的前提下实现高质量的文本到视频编辑。



## 核心方法与创新机理

FlowDirector 的核心创新在于将视频编辑重新定义为**数据空间中的直接 ODE 演化**，彻底绕过了现有方法中普遍存在的 inversion 步骤。这一范式转变解决了视频编辑领域的根本瓶颈：inversion 的近似误差会沿时间轴累积，导致外观保真度下降和运动一致性受损，表现为时序漂移与闪烁。通过直接在原生时空流形上驱动编辑过程，FlowDirector 从根本上消除了这一误差源。

在此基础上，FlowDirector 引入了三个**无训练流校正策略**，构成其相较于现有 inversion-based 基线（如 **FateZero**、**FLATTEN**、**TokenFlow**、**RAVE**、**VideoDirector** 等）的关键 changed slots：

### 1. 方向感知流校正（DA-FC）

**Changed slot**：编辑流校正机制

现有方法直接使用原始编辑流 $V_{\mathrm{edit}} = V_{\mathrm{tar}} - V_{\mathrm{src}}$，该流中同时包含与源语义对齐的“引力”分量和推动语义变换的反向分量，两者未经区分地混合作用，导致编辑强度与内容保持之间存在难以调和的冲突。

DA-FC 通过**正交分解**将编辑速度场解耦为沿源方向的分量 $V_{\parallel}$ 和垂直分量 $V_{\perp}$（Eq. 5），然后根据分量方向执行差异化处理：对与源语义同向的分量直接抑制（移除），对反向分量的幅度则通过放大因子 $\alpha$ 进行增强（Eq. 6）。这一设计主动打破了源视频的“语义引力”，使编辑轨迹能够更高效地脱离源内容约束，同时保留与编辑方向正交的无关信息。

消融实验证实了这一机制的关键性：移除 DA-FC 后，CLIP-T 从 34.64 降至 32.25，Q_edit 从 27.19 降至 25.42（Table 2），表明语义编辑能力显著退化。进一步地，增大放大因子 $\alpha$ 可持续提升 CLIP-T 和 Q_edit，代价是 WarpSSIM 轻微下降（Table 3），揭示了语义变换强度与结构一致性之间的可控权衡。

### 2. 运动-外观解耦校正（MAD-FC）

**Changed slot**：运动一致性约束

现有 inversion-based 方法缺乏显式的运动约束机制，编辑后的视频容易出现运动形变或与源视频的运动模式不一致。MAD-FC 通过**数学分离纯运动特征与静态外观信息**来解决这一问题：在每个时间步，构造纯运动表示（减去锚定帧以剥离外观），并定义运动能量函数 $J_t$ 来度量源与目标之间的运动差异（Eq. 9）。随后，通过梯度下降在每个去噪步上更新编辑状态 $Z_t^{\mathrm{edit}}$（Eq. 11），在保持语义变换的同时将源运动模式传导至编辑结果。

这一机制的效果在消融实验中表现极为突出：移除 MAD-FC 后，WarpSSIM 从 78.49 骤降至 69.26（Table 2），且定性结果显示编辑视频出现严重形变（Figure 6），充分证明 MAD-FC 是保持运动一致性的关键支柱。超参数分析进一步表明，外观锚定系数 $\phi=0.3$ 和校正强度 $\zeta=0.01$ 可在保持原有运动的同时实现充分的语义变换（Figure 16, 17）。

### 3. 差分平均引导（DAG）

**Changed slot**：速度估计的稳定性

现有方法的编辑速度通常来自单次采样估计，易受随机噪声影响，导致轨迹偏离低方差流形，产生纹理闪烁和伪影。DAG 通过**对比高质量共识估计与高方差基线**来构造差分引导信号：首先对多个随机编辑流取平均得到低方差的高质量估计 $V_{\mathrm{HQ}}$（Eq. 12），再选取与 $V_{\mathrm{HQ}}$ 余弦相似度最低的 $K$ 个流构造高方差基线 $V_{\mathrm{BL}}$（Eq. 13），最后利用两者的差分信号 $\bar{D} = V_{\mathrm{HQ}} - V_{\mathrm{BL}}$ 对 $V_{\mathrm{HQ}}$ 进行增强（Eq. 14），将编辑轨迹锁定在稳定流形上。

DAG 的效率优势显著：仅需 4 轮迭代推断（约 3 分钟/41 帧）即可超越 20 轮常规平均策略（约 19 分钟/41 帧），在效果与计算成本之间取得了更优平衡（Table 4, Figure 12）。消融实验表明，去除 DAG 后 Q_edit 从 27.19 降至 27.11（Table 2），结合定性结果（Figure 7），DAG 有效消除了纹理闪烁和伪影，提升了编辑的时序稳定性。

### 4. 编辑区域局部化

**Changed slot**：编辑范围控制

现有方法通常让编辑流全局作用，容易扰动背景区域。FlowDirector 利用交叉注意力图生成编辑掩膜，并通过**欧氏距离变换软化掩膜边缘**（Eq. 7），实现编辑区域与背景的平滑过渡。将软掩膜 $\widetilde{\mathbf{M}}$ 与校正后的编辑流逐元素相乘（Eq. 8），有效冻结非编辑区域，在保持背景保真度的同时实现精准的局部编辑。

---

**创新总结**：FlowDirector 的四个 changed slots 构成了一个协同的编辑控制系统——DA-FC 负责语义变换的强度与方向，MAD-FC 保障运动一致性，DAG 提升轨迹稳定性，软掩膜实现空间精准控制。这些策略共同使得编辑过程在无需训练、无需 inversion 的条件下，能够精准且稳定地完成语义变换，显著超越现有无训练基线。



FlowDirector 将文本驱动的视频编辑重新建模为**数据空间中的直接 ODE 演化过程**，从根本上规避了传统 inversion-based 方法中反演近似误差带来的外观漂移与时序闪烁问题。其整体 pipeline 由四个核心模块串联构成，形成一条从源视频到编辑结果的端到端无训练推理链路。

### 编辑流生成：统一的 ODE 编辑范式

框架的起点是**编辑 ODE 的构造**。给定源视频 $X_{\mathrm{src}}$、源文本 $c_{\mathrm{src}}$ 和目标文本 $c_{\mathrm{tar}}$，FlowDirector 在每个时间步 $t$ 上同时构建源侧和目标侧的中间状态：

$$Z_t^{\mathrm{src}} = (1-t) X_{\mathrm{src}} + t N_t$$

$$Z_t^{\mathrm{tar}} = Z_t^{\mathrm{edit}} + Z_t^{\mathrm{src}} - X_{\mathrm{src}}$$

其中 $N_t$ 为噪声，$Z_t^{\mathrm{edit}}$ 为当前编辑状态。这两个状态分别通过预训练的流匹配模型 $v_\theta$ 估计其速度场，二者的差值构成编辑 ODE 的速度场：

$$\frac{d Z_t^{\mathrm{edit}}}{d t} = V_{\mathrm{edit}}(t) = v_\theta(Z_t^{\mathrm{tar}}, t, c_{\mathrm{tar}}) - v_\theta(Z_t^{\mathrm{src}}, t, c_{\mathrm{src}})$$

这一范式（Figure 2 中部）的关键优势在于**完全绕过了 inversion 步骤**——编辑状态 $Z_t^{\mathrm{edit}}$ 直接在数据空间中演化，无需将源视频映射到高斯隐空间再反演回来，从而消除了 inversion 近似误差在时序上的累积效应。

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/002_Figure_2.jpg]]
*Figure 2: We compare inversion-based methods, FlowDirector (Direct ODE), and the full FlowDirector. Inversion-based methods first map the source video into a Gaussian latent space and then use this inverted state as the starting point for the subsequent editing process. FlowDirector (Direct ODE) instead constructs source-side and target-side states at each timestep, estimates their velocity fields, and uses the difference between them as an editing flow that drives video editing directly in data space. Building on this formulation, the full FlowDirector further corrects the editing flow at every timestep, yielding a shorter and more efficient editing trajectory and substantially improving the final e...*

### 三大流校正策略：精准控制编辑轨迹

原始编辑流 $V_{\mathrm{edit}}$ 虽然提供了基本的语义变换方向，但存在三个瓶颈：(1) 源视频的“语义引力”导致编辑不充分；(2) 运动信息在编辑过程中被破坏；(3) 单次采样的速度估计存在高方差噪声。FlowDirector 通过三个无训练流校正模块依次解决这些问题。

**方向感知流校正（DA-FC）** 对 $V_{\mathrm{edit}}$ 进行正交分解（Figure 3a），将其拆分为沿源速度方向的分量 $V_{\parallel}$ 和垂直分量 $V_{\perp}$：

$$V_{\parallel} = \frac{\langle V_{\mathrm{edit}}, V_{\mathrm{src}} \rangle}{\|V_{\mathrm{src}}\|^2 + \varepsilon} V_{\mathrm{src}}, \quad V_{\perp} = V_{\mathrm{edit}} - V_{\parallel}$$

随后根据分量的方向进行差异化处理：与源语义同向的 $V_{\parallel}$ 被直接抑制（置零），反向的 $V_{\parallel}$ 则以因子 $(1+\alpha)$ 放大，从而主动打破源视频的语义惯性。校正后的流 $\tilde{V}_{\mathrm{edit}}$ 再与基于交叉注意力图生成的软掩膜 $\widetilde{\mathbf{M}}$ 逐元素相乘，实现编辑区域的精确定位与背景冻结。

**运动-外观解耦校正（MAD-FC）** 在每个去噪步上通过梯度下降优化运动能量函数，将源视频的运动模式传导至编辑结果。具体而言，MAD-FC 从状态中减去锚定帧以提取“纯运动”表示，并定义运动能量 $J_t$ 来度量源与目标之间的运动差异，随后沿能量梯度方向更新编辑状态：

$$Z_t^{\mathrm{edit}} \leftarrow Z_t^{\mathrm{edit}} - \zeta \big[ (Z_0^{\mathrm{tar}} - Z_0^{\mathrm{src}}) - \phi (A_h^{\mathrm{tar}} - A_h^{\mathrm{src}}) \big]$$

其中 $\phi$ 控制外观锚定强度，$\zeta$ 为校正步长。该模块在保持语义变换的同时，有效抑制了运动形变。

**差分平均引导（DAG）** 通过集成多个随机编辑流来稳定速度估计（Figure 3b）。它首先对 $L_{\mathrm{HQ}}$ 个随机流取平均，获得低方差的高质量估计 $V_{\mathrm{HQ}}$；再选取 $K$ 个与 $V_{\mathrm{HQ}}$ 余弦相似度最低的流构造高方差基线 $V_{\mathrm{BL}}$。二者的差分信号 $\bar{D} = V_{\mathrm{HQ}} - V_{\mathrm{BL}}$ 捕获了“噪声漂移”方向，最终引导速度定义为：

$$V_{\mathrm{DAG}} = V_{\mathrm{HQ}} + w \bar{D}$$

该策略以仅 4 轮迭代推断的计算成本（约 3 分钟/41 帧），将编辑轨迹锁定在低方差流形上，有效消除了纹理闪烁和伪影。

### 模块间的数据流与协同

上述模块按顺序作用于每个去噪步：编辑流生成模块输出原始 $V_{\mathrm{edit}}$，经 DA-FC 校正并施加软掩膜后得到 $\hat{V}_{\mathrm{edit}}$，再经 MAD-FC 在状态空间中进行运动一致性优化，最后由 DAG 提供稳定的速度引导信号驱动 $Z_t^{\mathrm{edit}}$ 沿 ODE 轨迹演化。整个流程无需任何训练或微调，仅依赖预训练流匹配模型的一次前向推理，在单张 NVIDIA H20/H800 GPU 上即可完成编辑。



FlowDirector 将视频编辑建模为数据空间中的直接 ODE 演化，通过三个无训练流校正策略——方向感知流校正（DA-FC）、运动-外观解耦校正（MAD-FC）和差分平均引导（DAG）——精准控制编辑过程。以下按流水线模块逐一展开关键公式与变量含义。

### 编辑流生成（Editing Flow Generation）

给定源视频 $X_{\mathrm{src}}$、源提示 $c_{\mathrm{src}}$ 和目标提示 $c_{\mathrm{tar}}$，FlowDirector 首先构造源侧与目标侧的中间状态，并计算编辑 ODE 的速度场。

**源状态**通过源视频与噪声的线性插值获得：

$$Z_t^{\mathrm{src}} = (1 - t) X_{\mathrm{src}} + t N_t$$

其中 $N_t$ 为噪声，$t \in [0, 1]$ 为时间参数。

**编辑状态**直接在数据空间构造，无需反演：

$$Z_t^{\mathrm{edit}} = X_{\mathrm{src}} - Z_t^{\mathrm{src}} + Z_t^{\mathrm{tar}}$$

**目标状态**由编辑状态反推：

$$Z_t^{\mathrm{tar}} = Z_t^{\mathrm{edit}} + Z_t^{\mathrm{src}} - X_{\mathrm{src}}$$

**编辑 ODE 的速度场**定义为目标速度与源速度之差：

$$\frac{d Z_t^{\mathrm{edit}}}{d t} = V_{\mathrm{edit}}(t) = v_{\theta}(Z_t^{\mathrm{tar}}, t, c_{\mathrm{tar}}) - v_{\theta}(Z_t^{\mathrm{src}}, t, c_{\mathrm{src}})$$

其中 $v_{\theta}$ 为预训练的流匹配模型（基于 Rectified Flow 目标训练），其训练损失为：

$$\mathcal{L}_{\mathrm{RF}} = \mathbb{E} \big[ \| v_{\theta}(x_t, t) - (x_1 - x_0) \|^2 \big]$$

该损失将 Flow Matching 特化到线性路径上，学习连接先验与数据分布的直连速度。

### 方向感知流校正（DA-FC）

原始编辑流 $V_{\mathrm{edit}}$ 中同时包含推动语义变化的分量和维持源语义的冗余漂移。DA-FC 通过正交分解，主动抑制与源语义对齐的分量，放大反向分量。

**正交分解**将编辑速度投影到源速度方向：

$$V_{\parallel} = \frac{\langle V_{\mathrm{edit}}, V_{\mathrm{src}} \rangle}{\|V_{\mathrm{src}}\|^2 + \varepsilon} V_{\mathrm{src}}, \quad V_{\perp} = V_{\mathrm{edit}} - V_{\parallel}$$

其中 $V_{\mathrm{src}} = v_{\theta}(Z_t^{\mathrm{src}}, t, c_{\mathrm{src}})$ 为源侧速度场，$\varepsilon$ 为防止除零的小常数。

**校正规则**根据分量方向进行选择性处理：

$$\tilde{V}_{\mathrm{edit}} = \begin{cases} V_{\perp}, & \text{if } \langle V_{\parallel}, V_{\mathrm{src}} \rangle \geq 0, \\ (1+\alpha) V_{\parallel} + V_{\perp}, & \text{if } \langle V_{\parallel}, V_{\mathrm{src}} \rangle < 0. \end{cases}$$

当平行分量与源速度同向（$\langle V_{\parallel}, V_{\mathrm{src}} \rangle \geq 0$）时，直接丢弃该分量以打破源视频的“语义引力”；当反向时，以因子 $\alpha$ 放大该分量以增强语义变换。默认 $\alpha = 0.25$。

**软掩膜融合**进一步利用交叉注意力图生成编辑掩膜，并通过欧氏距离变换软化边缘：

$$\widetilde{\mathbf{M}}_{c,t}(x,y) = \mathbf{M}_{c,t}(x,y) + (1-\mathbf{M}_{c,t}(x,y)) e^{-\lambda d_{c,t}(x,y)}$$

其中 $\mathbf{M}_{c,t}$ 为二值注意力掩膜，$d_{c,t}(x,y)$ 为像素到编辑区域边界的欧氏距离，$\lambda$ 控制软化程度（默认 $\lambda = 0.25$）。最终将软掩膜作用于校正后的编辑流以冻结背景区域：

$$\hat{V}_{\mathrm{edit}} = \tilde{V}_{\mathrm{edit}} \odot \widetilde{\mathbf{M}}$$

### 运动-外观解耦校正（MAD-FC）

MAD-FC 通过构造纯运动表示并定义可优化的运动能量函数，在每个去噪步上将源运动传导至编辑结果，同时保持语义变换不受影响。

**纯运动表示**通过减去锚定帧（$t=0$ 时刻状态）来剥离静态外观信息：

$$G_{\mathrm{src}} = Z_t^{\mathrm{src}} - Z_0^{\mathrm{src}}, \quad G_{\mathrm{tar}} = Z_t^{\mathrm{tar}} - Z_0^{\mathrm{tar}}$$

**运动能量函数**定义为源与目标纯运动表示之间的差异：

$$J_t(Z) = \frac{1}{2} \| G_{\mathrm{tar}} - G_{\mathrm{src}} \|_2^2$$

**MAD-FC 更新规则**通过梯度下降最小化运动能量：

$$Z_t^{\mathrm{edit}} \leftarrow Z_t^{\mathrm{edit}} - \zeta \big[ (Z_0^{\mathrm{tar}} - Z_0^{\mathrm{src}}) - \phi (A_h^{\mathrm{tar}} - A_h^{\mathrm{src}}) \big]$$

其中 $\zeta$ 为校正强度（默认 $\zeta = 0.01$），$\phi$ 为外观锚定系数（默认 $\phi = 0.3$），$A_h^{\mathrm{tar}}$ 和 $A_h^{\mathrm{src}}$ 分别为目标与源的锚定帧。$\phi$ 控制外观保留与运动传导之间的权衡：过高的 $\phi$ 会还原源外观，过低的 $\zeta$ 导致运动偏差。

### 差分平均引导（DAG）

DAG 通过对比高质量共识估计与高方差基线，提取“噪声漂移”差分信号，以较低计算成本将编辑轨迹锁定在低方差流形上。

**高质量估计**通过平均 $L_{\mathrm{HQ}}$ 个随机编辑流获得：

$$V_{\mathrm{HQ}}(Z_t^{\mathrm{edit}}, t) = \frac{1}{L_{\mathrm{HQ}}} \sum_{\ell=1}^{L_{\mathrm{HQ}}} V_{\mathrm{edit}}^{(\ell)}(\cdot)$$

**基线估计**选取与高质量估计余弦相似度最低的 $K$ 个流取平均，构造高方差参照：

$$V_{\mathrm{BL}}(Z_t^{\mathrm{edit}}, t) = \frac{1}{K} \sum_{i \in \mathcal{T}_K} V_{\mathrm{edit}}^{(i)}(\cdot)$$

**DAG 引导速度**利用差分信号增强高质量估计：

$$V_{\mathrm{DAG}} = V_{\mathrm{HQ}} + w \bar{D}, \quad \bar{D} = V_{\mathrm{HQ}} - V_{\mathrm{BL}}$$

其中 $w$ 为引导强度（默认 $w = 2.75$）。差分信号 $\bar{D}$ 捕捉了随机流中的高方差漂移方向，通过将其反向叠加到高质量估计上，主动规避纹理闪烁和伪影区域。实验表明，DAG 仅需 4 轮迭代推断即可超越 20 轮常规平均策略的效果，在效率与稳定性之间取得更优平衡。

> **注意**：上述公式均源自论文 Section 3 的原始推导，变量含义严格依据原文定义。未在 verified_analysis 中出现的公式不予推导。

### 补充图表

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of proposed Direction-Aware Flow Correction (DA-FC, a) and Differential Averaging Guidance (DAG, b). DA-FC strengthens editing through orthogonal decomposition of the editing flow, amplifying parallel components that oppose the source semantics while eliminating co-directional components. (a) shows the case of amplifying the inverse component. DAG guides the editing flow toward a stable state by generating differential signals*

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/008_Table_2.jpg]]
*Table 2: Ablation results for Direction-Aware Flow Correction (DA-FC), Motion-Appearance Decoupling Correction(MAD-FC) and Differential Averaging Guidance (DAG). We highlight the best values for each metric*



## 实验与关键发现

### 主要定量结果

FlowDirector 在包含 150 个视频-文本对（来自 Internet 与 DAVIS 数据集）的自定义基准上，与五个代表性的零样本视频编辑基线方法进行了系统比较，涵盖基于 T2I 的 FateZero、FLATTEN、TokenFlow，以及基于 T2V 的 RAVE 和 VideoDirector。

**Table 1** 报告了 41 帧和 81 帧视频上的五项核心指标：Pick Score（人类偏好对齐）、CLIP-T（文本对齐度）、CLIP-F（帧间语义一致性）、WarpSSIM（光流结构保真度）和 Q_edit（综合编辑质量）。FlowDirector（1.3B 模型）在 41 帧设置下取得 Pick Score **21.82%**、CLIP-T **34.64×10⁻²**、CLIP-F **97.34×10⁻²**、WarpSSIM **78.49×10⁻²**、Q_edit **27.19×10⁻⁶**，在所有指标上均超过最强基线。与次优方法相比，CLIP-F 领先 **+1.86×10⁻²**（对比 VideoDirector），CLIP-T 领先 **+1.08×10⁻²**（对比 FLATTEN），Q_edit 领先 **+1.18×10⁻⁶**（对比 FLATTEN）。当模型规模扩展至 14B 参数时，所有指标进一步提升，Pick Score 达 22.61%，Q_edit 达 28.67×10⁻⁶。

值得注意的是，部分基线方法（FateZero、VideoDirector）因内存限制无法处理 81 帧视频，而 FlowDirector 在 81 帧设置下指标几乎无衰减（WarpSSIM 甚至略升至 79.10×10⁻²），展现出优良的长视频可扩展性。

### 消融实验

为验证三个核心流校正模块的独立贡献，进行了系统的模块消融实验（**Table 2**），以 1.3B 模型在 41 帧设置下评估。

**方向感知流校正（DA-FC）的关键作用**：移除 DA-FC 的平行分量抑制与反向分量放大（即 w/o Para, α=0.25 设置）后，CLIP-T 从 **34.64 骤降至 32.25**，Q_edit 从 **27.19 降至 25.42**。这直接验证了 DA-FC 通过正交分解编辑流、主动打破源视频“语义引力”的核心机制——不进行校正时，编辑轨迹被源语义方向拖拽，无法充分完成语义变换。**Table 3** 进一步消融放大因子 α：当 α 从 0 增至 0.25 时，CLIP-T 和 Q_edit 持续提升，同时 WarpSSIM 轻微下降，表明更强的语义变换以适度牺牲结构一致性为代价，用户可根据任务需求调节该参数。

**运动-外观解耦校正（MAD-FC）的决定性影响**：移除 MAD-FC 后，WarpSSIM 从 **78.49 骤降至 69.26**（降幅达 11.8%），为所有消融中最大单项降幅。**Figure 6** 的定性对比直观展示了这一退化：无 MAD-FC 时编辑视频出现严重形变与运动失真，而加入校正后运动模式与源视频保持高度一致。这一结果证实，仅靠编辑流无法自动传导源运动信息——MAD-FC 通过在每个去噪步最小化运动能量函数 $J_t$（Eq. 9），将源视频的纯运动表示（减去锚定帧后的时序变化）作为可优化约束，是实现运动一致性的必要条件。

**差分平均引导（DAG）的稳定性增益**：去除 DAG 后，定量指标下降幅度相对温和（Q_edit 从 27.19 降至 27.11），但 **Figure 7** 的定性对比揭示了 DAG 的核心价值：无 DAG 时编辑结果出现明显的纹理闪烁和局部伪影，尤其在放大视图中清晰可见。DAG 通过构造高质量估计 $V_{\mathrm{HQ}}$（多轮平均的低方差速度）与高方差基线 $V_{\mathrm{BL}}$ 之间的差分信号 $\bar{D}$（Eq. 12-14），以极低的额外计算成本将编辑轨迹锁定在低方差流形上，有效消除噪声诱导的漂移。

**MAD-FC 超参数敏感性**：**Figure 16** 展示了外观锚定系数 $\phi$ 的影响——$\phi=0.3$ 在“熊→恐龙”任务中成功实现语义变换同时保持原运动模式，过高 $\phi$ 会过度还原源外观。**Figure 17** 展示了校正强度 $\zeta$ 的影响——将 $\zeta$ 从 0.003 增至 0.01 显著改善运动对齐，过低 $\zeta$ 导致运动偏差。

### 效率分析

**Table 4** 在单张 NVIDIA H800 80G GPU 上比较了各方法的推理时间与峰值显存占用（编辑 41 帧视频）。FlowDirector 在效率上具有显著优势，且 DAG 策略仅需 **4 轮迭代推断**（约 3 分钟）即可超越常规 **20 轮平均策略**（约 19 分钟），在效果与效率之间取得更优平衡。**Figure 12** 的定性对比进一步证实，4 轮 DAG 的编辑质量优于 20 轮常规平均，说明差分信号的引导作用比单纯增加采样轮次更有效。

### 失败模式与局限性

**Figure 15** 展示了一类典型失败案例：当目标提示未能完全替换源描述时（如残留源对象关键词），编辑视频会保留大量原始内容特征。这一现象的根本原因在于 FlowDirector 的编辑驱动力主要来自源-目标速度场的差异——若提示差异不足以产生显著的对抗性速度分量，DA-FC 的放大机制缺乏作用空间。此外，论文指出该方法在视频风格迁移任务上表现相对有限，因为其编辑机制倾向于结构保留，主要由文本差异驱动，对整体风格变化不敏感。编辑质量还高度依赖源文本的全面性，过于简单的源提示可能导致次优结果。

### 关键图表结论速览

- **Figure 5（定性对比）**：FlowDirector 在多种编辑任务（物体替换、属性修改、背景保留）上视觉质量和时序一致性均显著优于 FateZero、FLATTEN、TokenFlow、RAVE 等基线。
- **Figure 11（DA-FC 消融定性）**：无 DA-FC 时编辑强度与一致性难以平衡；加入 DA-FC 后可在显著修改目标语义的同时有效保留无关区域和运动一致性。
- **Figure 13（DAG 引导强度 ω）**：ω=2.75 为默认最优值，适度增强差分信号可有效消除伪影。
- **Figure 14（DAG 集成规模）**：不同平均策略构造的高质量估计与基线估计产生不同的引导增强效果。

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison. Our method outperforms previous methods across diverse editing tasks, demonstrating superior visual quality and temporal consistency. Best viewed zoomed-in*

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/014_Figure_11.jpg]]
*Figure 11: Ablation study of Direction-Aware Flow Correction. Without DA-FC, it is difficult to achieve an effective balance between editing strength and consistency. In contrast, incorporating DA-FC enables significant semantic modifications of the target object while effectively preserving irrelevant regions and maintaining motion consistency. Our modules are crucial for achieving high-quality video editing*

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/017_Figure_13.jpg]]
*Figure 13: Ablation study of guidance strength ω. The ω controls the guidance strength of the differential signal. By enhancing the differential signal, artifacts can be effectively eliminated and the editing results can be optimized. We use ω = 2.75 as the default value. Best viewed zoomed in*

### 补充图表

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison. We report Pick-Score, CLIP-T, CLIP-F, WarpSSIM, and*

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/010_Table_3.jpg]]
*Table 3: Ablation results for Direction-Aware Flow Correction (DA-FC). Para denotes the parallel component aligned with the source semantic direction. Therefore, w/o Para indicates removal of only this component, while a ’-’ value for α signifies no amplification of the opposite component. We highlight the best values for each metric*

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/015_Table_4.jpg]]
*Table 4: Efficiency Comparison. We report the inference time and peak GPU memory usage for editing a 41-frame video on a single NVIDIA H800 80G GPU. The upper section compares existing SOTA methods, while the lower section analyzes the efficiency of different strategies within our framework. The symbol “–” indicates cases where the method exceeded the single-GPU memory limit and required specific optimization strategies to execute; consequently, these metrics are omitted to ensure a fair comparison of native performance*

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/007_Figure_6.jpg]]
*Figure 6: Ablation study of Motion-Appearance Decoupling Correction. Without MAD-FC, the edited video exhibited severe distortion. After using MAD-FC correction, the motion of the edited video remained largely consistent with the original video*

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/009_Figure_7.jpg]]
*Figure 7: Ablation study of Differential Averaging Guidance. In the “Zoom” column: Top row is with DAG, bottom row is without DAG*

![[assets/figures/papers/paper_list_l2311_https_arxiv_org_abs_2506_05046/figures/016_Figure_12.jpg]]
*Figure 12: Qualitative comparison between the editing results of a multi-round inference averaging strategy and using a DAG. The Sample Average strategy is set to use a regular averaging strategy for 20 rounds of iterative inference at every denoising step to obtain the editing flow. The DAG setting uses 4 rounds of iterative inference to obtain a high-quality estimate and perform reinforcement-guided generation of the editing flow. Best viewed zoomed in*



## 定位与知识库关联

### 1. 与现有方法的谱系关系

FlowDirector 属于**无训练、零样本视频编辑**方法，其核心突破在于完全摒弃了 inversion 步骤，将编辑过程建模为数据空间中的直接 ODE 演化。与现有工作相比，其谱系定位可从以下维度理解：

**Inversion-based 方法（直接前身）**  
现有主流零样本视频编辑方法普遍依赖 DDIM inversion 或其变体，将源视频映射至高斯隐空间，再以该反演状态为起点进行编辑。代表性工作包括：

- **FateZero**：基于 T2I 模型的零样本视频编辑，通过融合注意力图实现时空一致的编辑，但 inversion 的近似误差会导致外观漂移和时序闪烁。
- **FLATTEN**：在 FateZero 基础上引入光流引导的注意力融合，增强运动一致性，但仍受限于 inversion 误差累积。
- **TokenFlow**：通过跨帧 token 传播保持语义一致性，同样依赖 inversion 作为编辑起点。
- **RAVE**：基于 T2V 模型的零样本编辑，利用随机反演策略缓解误差，但未能根本解决反演-编辑域差异问题。
- **VideoDirector**：基于 T2V 模型的编辑框架，引入时序注意力机制，但仍需 inversion 步骤。

这些方法的共同瓶颈在于：inversion 步骤的近似误差会沿编辑轨迹累积，导致外观保真度下降和运动一致性受损。FlowDirector 通过直接 ODE 演化绕过 inversion，从根源上消除了这一误差源。

**Flow Matching 与 Rectified Flow 的理论基础**  
FlowDirector 的数学框架建立在 Flow Matching 和 Rectified Flow 之上。Flow Matching 训练时间相关矢量场将先验分布传输至数据分布，而 Rectified Flow 将其特化到线性路径上，学习直连速度。FlowDirector 将这一生成范式迁移至编辑场景，利用预训练 T2V 模型的速度场预测能力，直接在数据空间构造编辑轨迹。

**与 Classifier-Free Guidance 的对比**  
传统 Classifier-Free Guidance 通过混合条件与无条件预测来增强文本对齐，但其作用域在速度场内部，不涉及编辑轨迹的几何结构。FlowDirector 的 DAG 机制在更高层次上操作——通过对多个随机编辑流进行差分平均，主动引导轨迹远离高方差区域，本质上是一种**轨迹级引导策略**，与 CFG 形成互补。

### 2. 适用边界与能力范围

**强适用场景**  
- **局部语义替换**：如“吉普车→保时捷”、“熊→恐龙”等对象级编辑，方法能够精准定位编辑区域并保持背景不变。
- **属性编辑**：颜色、纹理、材质等对象属性的修改，语义变换清晰且结构保持良好。
- **运动保持型编辑**：需要保留源视频运动模式（如行走、旋转）同时改变外观的任务，MAD-FC 模块提供了显式的运动约束。

**弱适用场景**  
- **视频风格迁移**：该方法倾向于结构保留，主要由文本差异驱动，对整体风格变化（如“写实→卡通”）不敏感。这源于编辑流主要捕捉语义差异，而非全局纹理统计量。
- **大幅度文本替换**：当目标提示与源提示差异过大，或目标提示中残留源描述时，编辑结果会保留大量原始内容特征（见 Figure 15）。这表明方法的编辑强度受限于速度场差异的幅度。
- **源提示不完整时**：编辑质量高度依赖源文本的全面性；过于简单的源提示会导致速度场估计不准确，产生次优结果。

**计算资源边界**  
- 在单张 NVIDIA H800 80G GPU 上，编辑 41 帧视频约需 3 分钟（DAG 模式，4 轮迭代），峰值显存占用与基线方法可比（Table 4）。
- 方法支持 81 帧视频编辑，但部分基线方法（FateZero、VideoDirector）因内存限制无法评估该长度。
- 对极长视频（>100 帧）和高分辨率视频的可扩展性尚未验证，计算成本可能随帧数线性增长。

### 3. 局限性与已知失效模式

**文本替换不完全**  
当目标提示中残留源对象描述时，编辑视频会混合源与目标特征。Figure 15 展示了这一失效案例：目标文本替换不彻底导致编辑结果保留了原始内容的显著痕迹。该问题源于编辑流由文本差异驱动，若差异信号不够“纯净”，速度场中就会残留源语义分量。

**风格迁移能力有限**  
方法对全局风格变换的表现较弱。这是因为 DA-FC 的正交分解机制主要针对语义方向进行校正，而风格变化通常涉及更弥散、更低频的速度场分量，难以被当前的编辑流充分捕捉。

**超参数敏感性**  
- DA-FC 的放大因子 α 控制语义变换强度：增大 α 提升 CLIP-T 和 Q_edit，但 WarpSSIM 轻微下降（Table 3），表明更强的编辑以牺牲结构一致性为代价。
- MAD-FC 的外观锚定系数 ϕ 和校正强度 ζ 需要针对不同任务调节：ϕ 过高会还原源外观，ζ 过低则运动偏差增大（Figure 16–17）。
- DAG 的引导强度 ω 默认值为 2.75，需根据视频内容和噪声水平调整（Figure 13）。

**对基础模型的依赖**  
FlowDirector 的编辑质量上限受限于底层 T2V 模型的能力。当基础模型对特定概念的理解不足时，速度场估计将不准确，编辑结果也会退化。方法在 1.3B 和 14B 模型上均进行了验证，但不同模型架构（如 DiT vs. U-Net）的适配性尚需进一步确认。

### 4. 开放问题与未来方向

**编辑强度的可控性**  
当前方法通过 α 参数调节编辑强度，但该机制是全局的、均匀的。如何实现空间自适应的编辑强度控制——例如对前景施加强编辑而对背景施加弱编辑——仍是一个开放问题。

**风格迁移的扩展**  
能否将框架扩展到视频风格迁移等弱结构变换任务？这可能需要引入额外的风格表示（如 Gram 矩阵或 CLIP 风格嵌入），并将其融入编辑流的速度场构造中。

**长视频与高分辨率的可扩展性**  
方法对极长视频（>200 帧）和高分辨率视频（>1080p）的计算成本是否仍然可控？DAG 的多轮推断策略在长序列上可能面临线性增长的开销，需要探索更高效的轨迹引导方案。

**提示工程的改进空间**  
文本替换不完全的问题是否可以通过改进提示工程或引入额外约束（如负向提示、注意力重加权）来缓解？这涉及编辑流构造的“信号纯度”问题，可能需要从速度场分解的角度进行更深入的分析。

**与其他生成范式的融合**  
FlowDirector 的 ODE 编辑框架是否可以与扩散模型的随机微分方程（SDE）采样、或与一致性模型等快速生成范式结合？这有望在保持编辑质量的同时进一步降低计算成本。



## 原文 PDF

![[paperPDFs/CVPR_2026/FlowDirector_Training_Free_Flow_Steering_for_Precise_Text_to_Video_Editing.pdf]]
