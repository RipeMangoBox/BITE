---
title: "SpaceTimePilot: Generative Rendering of Dynamic Scenes Across Space and Time"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpaceTimePilot_Generative_Rendering_of_Dynamic_Scenes_Across_Space_and_Time.pdf
project_link: "https://zheninghuang.github.io/Space-Time-Pilot/"
code_link: null
aliases:
- SpaceTimePilot
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入独立的动画时间参数 'animation time' 以及相应的时序编码模块和训练数据（时序变形增强与 Cam×Time 数据集），使得扩散模型能够将相机变换与时间流作为两个独立的控制信号进行学习。
primary_logic: 在视频扩散模型中，将时间线概念解耦为可显式调控的 'animation time'，并通过在现有数据上进行时序变形增强以及合成密集时空覆盖的数据集，来提供强监督信号，从而使模型学会独立操作空间与时间维度。
claims:
- SpaceTimePilot 在所有时间控制配置下均显著优于基线方法（PSNR 21.16 vs. 17.86 vs. 15.52）
- 所提出的 1D-Conv 时间嵌入能够锁定特定时间状态同时保持相机运动准确，而 MLP 或 RoPE(f') 则会导致相机与时间控制相互干扰
- 联合训练 Cam×Time 数据集能够消除基线中的明显伪影，验证了密集时空监督的有效性
- 时序变形增强相比仅使用静态场景数据提供了更丰富的时间变化信号，显著提升相机－时间解耦能力
---

# SpaceTimePilot: Generative Rendering of Dynamic Scenes Across Space and Time

> [!tip] 核心洞察
> 在视频扩散模型中，将时间线概念解耦为可显式调控的 'animation time'，并通过在现有数据上进行时序变形增强以及合成密集时空覆盖的数据集，来提供强监督信号，从而使模型学会独立操作空间与时间维度。

| 字段 | 内容 |
|------|------|
| 中文题名 | SpaceTimePilot: 跨时空动态场景的生成式渲染 |
| 英文题名 | SpaceTimePilot: Generative Rendering of Dynamic Scenes Across Space and Time |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.25075) · [Project](https://zheninghuang.github.io/Space-Time-Pilot/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SpaceTimePilot |
| Dataset | Cam×Time 测试集, VBench, OpenVideoHD 相机控制评估 |

> [!tip] 效果简介
> - Cam×Time 测试集 上，PSNR (Avg) 21.16 vs 17.86 (ReCamM+jointdata) (+3.30)；LPIPS (Avg) 0.1764 vs 0.3073 (ReCamM+jointdata) (-0.1309)。
> - VBench 上，ImgQ（图像质量） 0.6486 vs 0.6389 (TrajectoryCrafter) (+0.0097)。
> - OpenVideoHD 相机控制评估 上，RelRot（相对旋转误差） 2.71 vs 3.34 (ReCamM+Aug+csrc) (-0.63)。

## 概要

现有的视频生成方法在空间与时间控制上存在根本性割裂：相机视点变换模型（如 ReCamMaster、TrajectoryCrafter）仅能沿单调时间轴进行相机运动，而四维多视图模型（如 4DGS 类方法）虽可生成离散时空采样点，却无法输出连续视频序列。这种局限使得“子弹时间”“慢动作回放”与自由相机轨迹的组合效果难以在单一模型中实现——这正是 **SpaceTimePilot** 要解决的核心瓶颈。

SpaceTimePilot 的核心思想是在视频扩散模型中引入一个可显式调控的**动画时间参数**（animation time），将时间线从隐式的帧序关系中解耦出来。通过独立的时间编码模块与相机轨迹条件协同工作，模型得以将“相机往哪运动”和“场景以何种节奏演进”作为两个正交的控制信号进行学习。为提供充分的监督，方法层面做了两件事：一是在现有动态场景数据上施加**时序变形增强**（反向、慢动作、冻结、锯齿等），人为制造丰富的时间变化模式；二是构建 **Cam×Time 数据集**——对每个场景沿四条相机轨迹以 120 帧全时间覆盖进行密集渲染，形成完整的时空网格，从而提供强监督信号。

实验表明，这一设计带来了显著增益：在 Cam×Time 测试集的时间控制评估中，SpaceTimePilot 的 PSNR 达到 **21.16 dB**，比最佳基线 ReCamMaster + jointdata 高出 **3.30 dB**，LPIPS 降低 **0.13**；在 VBench 六维视觉质量评估中与 TrajectoryCrafter 持平或略优；在 OpenVideoHD 的相机精度评估中，相对旋转误差从 3.34 降至 **2.71**，RTA30 从 46.11% 提升至 **54.44%**。消融实验进一步确认：1D 卷积时间嵌入是解耦成功的关键——MLP 无法锁定时间状态，RoPE 变体会同时锁定相机运动；Cam×Time 数据集则有效消除了基线中出现的明显伪影。

在方法谱系上，SpaceTimePilot 属于**条件视频扩散模型**的延伸，其相机条件机制沿袭了 ReCamMaster 的轨迹投影思路，但首次将时间控制提升为与相机对等的独立维度。与 TrajectoryCrafter 的“先重排后控相机”策略不同，SpaceTimePilot 在扩散去噪过程中同时注入相机与时间信号，避免了相机运动被时间重排干扰的问题。在知识库定位上，该方法填补了“连续时空导航式生成渲染”的空白，为后续研究提供了时空解耦控制的基础框架与数据集基准。

**核心瓶颈：空间与时间控制的耦合困境**

现有的视频生成方法在“相机视点变换”（空间）与“场景动态回放”（时间）两个维度上存在根本性的控制耦合。相机控制类视频到视频（Camera-control V2V）模型，如 ReCamMaster，能够沿给定的相机轨迹生成新视角视频，但其时间线严格单调——只能进行正常速度的正向播放，无法实现慢动作、倒放或子弹时间等非单调时间效果。另一方面，4D 多视图生成模型虽能在离散的时空坐标上合成稀疏视图，却无法生成连续的视频序列。这种“空间可控则时间锁死，时间可控则空间离散”的割裂，使得用户无法自由组合相机运动与时间流，例如在环绕拍摄的同时执行慢动作，或在推拉镜头的同时倒放场景动态。

**因果机制：缺失独立的“动画时间”控制信号**

造成上述困境的深层原因在于，现有方法缺乏一个独立于相机轨迹的“动画时间”控制参数。在典型的相机控制扩散模型中，时间信息仅隐含在帧序列的位置编码中（如 RoPE），模型无法区分“帧的先后顺序”与“场景动态的演进速度/方向”。当用户试图对视频进行时间重排（如先倒放再应用相机控制），时间操作与相机控制会在生成过程中相互干扰——时间重排破坏了相机轨迹的连续性，而相机控制又无法理解非单调的时间流。这本质上是一个**时空解耦问题**：模型需要学会将“相机在哪里看”与“场景运动到哪一时刻”作为两个独立的控制自由度。

**动机与本文目标**

SpaceTimePilot 旨在打破这一耦合壁垒，在单一视频扩散模型中实现统一的时空控制。其核心动机是：通过显式引入一个可调控的“动画时间”参数，并配合相应的时序编码机制与训练数据设计，使模型能够将相机变换与时间流作为两个独立信号进行学习。最终目标是让用户能够自由指定任意相机轨迹与任意时间控制（正向、倒放、慢动作、子弹时间、冻结等）的组合，生成连续、连贯的视频，真正实现“跨时空”的生成式渲染。

**现有方法的缺口与本文定位**

Figure 2 清晰地刻画了方法谱系中的缺口：相机控制 V2V 方法仅在时间单调的约束下改变相机；4D 多视图方法仅在离散时空点上生成稀疏视图；而 SpaceTimePilot 首次实现了在相机轴和时间轴上的自由连续移动，支持方向、速度的完全控制，以及混合时空轨迹。这一能力填补了“连续时空导航”的方法空白，为动态场景的生成式渲染提供了新的控制维度。

## 核心方法与创新机理

SpaceTimePilot 的核心创新在于将视频扩散模型中的**空间（相机运动）与时间（场景动态）显式解耦**，使单一模型能够沿任意时空轨迹生成连续、连贯的视频。现有方法要么只能控制相机轨迹而保持时间单调推进（如 **ReCamMaster**），要么只能生成离散的稀疏视角而无法产出连续视频序列（如 4D 多视图模型），无法实现子弹时间、慢动作与自由相机路径的任意组合。SpaceTimePilot 通过以下三个关键机制突破这一瓶颈。

### 动画时间参数的独立注入

方法引入一个显式的**动画时间参数** $t \in \mathbb{R}^F$，与相机轨迹参数 $\mathbf{c}$ 并列作为扩散模型的条件信号。时间参数首先通过正弦编码映射为帧级嵌入，再经**两层 1D 卷积**压缩到潜帧维度，最终以加法形式注入视频令牌：

$$x' = x + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}) + \mathcal{E}_{\mathrm{ani}}(\mathbf{t})$$

这一设计的关键在于 **1D 卷积压缩器**。消融实验表明（Figure 15 Bottom, Sec. D.3），MLP 压缩器无法有效锁定动画时间状态，而 RoPE(f') 等隐式时间位置编码会同时锁定相机运动，导致相机与时间控制相互干扰。1D 卷积与正弦编码的组合能够锁定特定时间状态，同时保持相机运动的准确性。

### 时序变形增强

现有相机控制视频生成模型（如 ReCamMaster）仅使用单调时间推进的数据训练，缺乏对非单调时间变化的显式监督信号。SpaceTimePilot 对目标视频应用一组**时序变形操作**，包括反向播放、慢动作、冻结帧和锯齿形运动等，而源视频保持标准正向播放。这为模型提供了**多样化且显式的时间变化信号**，使其学会将时间流与相机变换作为两个独立维度进行操作。

消融实验（Figure 14）证实，时序变形增强显著优于仅使用静态场景数据的联合训练策略——后者只能提供单一的时间变化模式，无法支撑复杂的时空解耦。进一步地，包含冻结操作的时序变形比不含冻结的配置效果更佳（Figure 14 Bottom）。

### 源感知的相机条件与 Cam×Time 数据集

传统相机控制方法仅使用目标相机轨迹 $\mathbf{c}_{\mathrm{trg}}$ 作为条件，并假设第一帧相机不变。SpaceTimePilot 同时注入**源相机轨迹** $\mathbf{c}_{\mathrm{src}}$ 和目标轨迹 $\mathbf{c}_{\mathrm{trg}}$，允许生成视频从任意相机角度开始：

$$x_{\mathrm{src}}' = x_{\mathrm{src}} + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}_{\mathrm{src}}) + \mathcal{E}_{\mathrm{ani}}(\mathbf{t}_{\mathrm{src}}), \quad x_{\mathrm{trg}}' = x_{\mathrm{trg}} + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}_{\mathrm{trg}}) + \mathcal{E}_{\mathrm{ani}}(\mathbf{t}_{\mathrm{trg}})$$

源和目标令牌沿帧维度拼接后送入全 3D 注意力模块，使模型同时感知源视频的时空状态与目标的期望轨迹。

为提供密集的时空监督，方法构建了 **Cam×Time 数据集**——对每个场景沿多条相机轨迹进行 120 帧的完整时间覆盖渲染，形成全时空网格。Table 1 对比显示，现有数据集（如 ReCamMaster、SynCamMaster）仅提供稀疏的时间采样，而 Cam×Time 支持在 0–120 帧范围内任意采样时间变化。联合训练 Cam×Time 能够消除基线方法中的明显伪影（Figure 15 Top），验证了密集时空监督对解耦质量的决定性作用。

SpaceTimePilot 的整体框架围绕一个核心设计展开：在视频扩散模型中同时注入**相机轨迹**（空间控制）和**动画时间**（时间控制）两路独立的控制信号，从而实现对动态场景的跨时空生成式渲染。其输入为一个源视频 $V_{\mathrm{src}} \in \mathbb{R}^{F \times C \times H \times W}$，输出为一个目标视频 $V_{\mathrm{trg}}$，该目标视频遵循用户指定的相机轨迹 $\mathbf{c}_{\mathrm{trg}}$ 和动画时间序列 $\mathbf{t}_{\mathrm{trg}}$，可产生子弹时间、慢动作、倒放等非单调时间效果，同时保持相机运动的精确可控。

### 模型主干：3D VAE + DiT

SpaceTimePilot 构建于视频扩散模型的标准架构之上，包含两个核心模块：

- **3D VAE**：负责将原始视频帧压缩到潜空间，并在生成完成后将潜变量解码回像素空间。这一压缩步骤降低了扩散模型在高维像素空间中的计算开销。
- **DiT（Diffusion Transformer）**：作为去噪骨干网络，在潜空间中执行多模态令牌的去噪过程。DiT 采用 **Full-3D Attention** 机制，在时空维度上执行全注意力运算，以捕捉视频序列中的长程时空依赖。

### 控制信号注入：相机嵌入与动画时间嵌入

框架的核心创新在于控制信号的注入方式。模型通过**加法式条件注入**将相机轨迹和动画时间信息融合到视频令牌中：

**相机条件注入**。给定相机轨迹序列 $\mathbf{c}$（由每帧的相机外参/内参构成），通过相机嵌入器 $\mathcal{E}_{\mathrm{cam}}$ 将其投影到与视频令牌相同的特征空间，然后直接相加：

$$x' = x + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}) \tag{1}$$

**时空条件注入**。为解耦时间控制，引入独立的动画时间参数 $\mathbf{t} \in \mathbb{R}^F$，通过正弦编码生成帧级时间嵌入 $\mathbf{e}$，再经**两层 1D 卷积**压缩到潜帧维度：

$$\widetilde{\mathbf{e}} = \mathrm{Conv1D_2}(\mathrm{Conv1D_1}(\mathbf{e}))$$

压缩后的时间特征通过动画时间嵌入器 $\mathcal{E}_{\mathrm{ani}}$ 与相机特征一同注入：

$$x' = x + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}) + \mathcal{E}_{\mathrm{ani}}(\mathbf{t}) \tag{2}$$

这一设计的因果机制在于：1D 卷积压缩器能够将帧级时间信号平滑地映射到潜空间帧维度，使得时间控制与相机控制相互独立。消融实验证实，若改用 MLP 压缩器则时间控制失效，若改用 RoPE(f') 则相机与时间控制会相互干扰（见 Figure 15 Bottom 及 Sec. D.3）。

**源感知条件注入**。在推理阶段，模型需同时感知源视频和目标视频的时空状态。为此，框架将源视频令牌 $x_{\mathrm{src}}$ 和目标视频令牌 $x_{\mathrm{trg}}$ 分别注入各自的相机轨迹和动画时间信息，然后沿帧维度拼接：

$$x_{\mathrm{src}}' = x_{\mathrm{src}} + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}_{\mathrm{src}}) + \mathcal{E}_{\mathrm{ani}}(\mathbf{t}_{\mathrm{src}}), \quad x_{\mathrm{trg}}' = x_{\mathrm{trg}} + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}_{\mathrm{trg}}) + \mathcal{E}_{\mathrm{ani}}(\mathbf{t}_{\mathrm{trg}}), \quad x' = [x_{\mathrm{trg}}', x_{\mathrm{src}}']_{\mathrm{frame-dim}} \tag{3}$$

这一设计允许目标视频的第一帧相机位姿与源视频不同，突破了现有方法“首帧相机不变”的假设，是实现任意相机轨迹控制的关键。

### 推理管道：多轮自回归生成

为生成长视频，SpaceTimePilot 采用**多轮自回归推理方案**（见 Figure 9）。模型首先生成一个 81 帧的视频片段，该片段以源视频和用户指定的时空轨迹为条件。随后，生成的片段被复用为下一轮的“次级源视频”，与原始源视频共同作为条件，生成新的视频片段。通过链式迭代和片段拼接，模型能够产生沿任意时空路径的长连贯视频（见 Figure 10），实现从低角度到鸟瞰视角的大跨度相机变换，同时保持视觉与运动的连贯性。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_25075/figures/014_Figure_9.jpg]]
*Figure 9: Overview of the multi-turn autoregressive inference scheme. The model first generates an 81-frame segment conditioned on the source video and a chosen space–time trajectory. The resulting output is then reused as a secondary source video for subsequent iterations, each with its own camera and temporal trajectory. By chaining these iterations and stitching the outputs, SpaceTimePilot produces a long, coherent video that follows an arbitrary space–time path*

### 架构总览

Figure 8 给出了 SpaceTimePilot 的完整架构图。模型通过时空注意力机制联合条件化相机轨迹与时间控制信号，使 DiT 骨干网络能够在去噪过程中同时感知空间与时间维度的控制意图，从而支持反转、重复、加速、锯齿时间等非单调运动生成。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_25075/figures/013_Figure_8.jpg]]
*Figure 8: Architecture of SpaceTimePilot. Our model jointly conditions on camera trajectories and temporal control signals via space–time attention, enabling non-monotonic motion generation such as reversals, repeats, accelerations, and zigzag time*

### 3.1 基础架构：视频扩散模型

SpaceTimePilot 建立在视频扩散模型的框架之上。输入源视频 $V_{\mathrm{src}} \in \mathbb{R}^{F \times C \times H \times W}$ 首先经过 3D VAE 编码，压缩到潜空间得到潜在特征 $x$。随后，一个基于 Transformer 的去噪模型（DiT）在潜空间中对加噪的潜在特征进行迭代去噪，最终通过 3D VAE 解码器重建出目标视频。

空间控制信号通过相机轨迹序列 $\mathbf{c}$ 注入。相机轨迹经过一个专用的相机嵌入器 $\mathcal{E}_{\mathrm{cam}}$ 投影到与视频令牌相同的特征空间，然后直接加到视频令牌上：

$$x' = x + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}) \tag{1}$$

模型采用 Full-3D Attention 机制，在时空维度上执行全注意力，以捕捉视频帧间的长程依赖关系。

### 3.2 时空解耦的核心机制

#### 3.2.1 动画时间嵌入

现有视频生成方法的时间控制是隐式的——时间信息仅通过帧的排列顺序体现，无法独立操控。SpaceTimePilot 的核心创新在于引入一个显式的**动画时间参数** $\mathbf{t} \in \mathbb{R}^F$，将时间线与相机轨迹解耦为两个独立的控制信号。

具体实现流程如下：
1. 对动画时间序列 $\mathbf{t}$ 的每一帧时间戳应用正弦位置编码，得到原始帧级时间嵌入 $\mathbf{e}$。
2. 由于视频在潜空间中的帧数 $F'$ 小于原始帧数 $F$，需要将 $\mathbf{e}$ 压缩到潜帧维度。作者采用两层一维卷积实现：

$$\widetilde{\mathbf{e}} = \mathrm{Conv1D_2}(\mathrm{Conv1D_1}(\mathbf{e}))$$

3. 压缩后的时间嵌入 $\widetilde{\mathbf{e}}$ 与相机嵌入一同加到视频令牌上：

$$x' = x + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}) + \mathcal{E}_{\mathrm{ani}}(\mathbf{t}) \tag{2}$$

**设计选择的因果逻辑**：消融实验（Figure 15 Bottom, Sec. D.3）揭示了不同时间嵌入方案的失败模式——MLP 压缩器无法有效锁定时间状态，导致相机与时间控制相互干扰；RoPE(f') 虽然能锁定时间，但同时也会锁定相机运动，破坏空间控制的独立性。1D-Conv 结合正弦编码是唯一能够**锁定特定时间状态同时保持相机运动准确**的方案。

#### 3.2.2 时序变形增强

仅靠架构设计不足以实现时空解耦——训练数据的信号强度同样关键。现有方法通常只使用静态场景数据集来提供时间变化信号，但这只能提供单一的时间模式（静止 vs. 运动），监督信号过于稀疏。

SpaceTimePilot 提出**时序变形增强**：对目标视频的时间戳应用非线性变形函数 $\mathbf{t}_{\mathrm{trg}} = \tau(\mathbf{t}_{\mathrm{src}})$，生成多样化的时间控制样本：
- **反向播放**：时间戳逆序排列
- **慢动作**：时间戳拉伸
- **冻结**：时间戳重复同一值
- **锯齿运动**：时间戳来回震荡

如 Figure 3 所示，这些操作在保留源视频为标准正向参考的同时，为目标视频提供了显式的时间变化监督信号，其多样性远超仅使用静态场景数据的方案。

### 3.3 源感知的相机条件注入

传统相机控制方法假设生成视频的第一帧与源视频第一帧的相机位姿相同，这限制了应用的灵活性。SpaceTimePilot 将条件信号扩展为同时注入源相机轨迹 $\mathbf{c}_{\mathrm{src}}$ 和目标相机轨迹 $\mathbf{c}_{\mathrm{trg}}$：

$$x_{\mathrm{src}}' = x_{\mathrm{src}} + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}_{\mathrm{src}}) + \mathcal{E}_{\mathrm{ani}}(\mathbf{t}_{\mathrm{src}})$$

$$x_{\mathrm{trg}}' = x_{\mathrm{trg}} + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}_{\mathrm{trg}}) + \mathcal{E}_{\mathrm{ani}}(\mathbf{t}_{\mathrm{trg}})$$

$$x' = [x_{\mathrm{trg}}', x_{\mathrm{src}}']_{\mathrm{frame-dim}} \tag{3}$$

源视频和目标视频的令牌分别注入各自的相机和动画时间信息后，沿帧维度拼接，共同输入去噪网络。这一设计允许生成视频从任意相机角度开始，突破了第一帧位姿必须与源视频一致的约束。

### 3.4 多轮自回归生成管道

为实现长视频生成，SpaceTimePilot 采用多轮自回归推理方案（Figure 9）。每轮生成一个 81 帧的视频片段，该片段同时以原始源视频和上一轮生成的片段作为条件。通过链式迭代和片段拼接，模型能够生成沿任意时空轨迹的长视频，同时保持时间连续性和运动一致性。

### 3.5 方法总结

SpaceTimePilot 通过三个关键设计实现时空解耦：
1. **动画时间嵌入**（1D-Conv + 正弦编码）：提供独立的时间控制信号
2. **时序变形增强**：提供多样化的时间变化监督
3. **源感知相机条件**：允许生成视频从任意相机角度开始

这三个组件协同作用，使得扩散模型能够独立操作空间（相机）和时间（动画）维度，实现子弹时间、慢动作、反向播放等效果与任意相机轨迹的自由组合。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_25075/figures/009_Table_5.jpg]]
*Table 5: Time-embedding compressor ablation. The proposed time-embedding method, trained with temporal warping on the proposed dataset, yields sharper results overall*

## 实验与关键发现

### 核心实验设计

SpaceTimePilot 的实验围绕一个核心问题展开：模型能否在自由组合的相机轨迹与时间操控下，生成连贯且高质量的目标视频。为此，作者构建了三个维度的评估体系：**时间控制精度**（Cam×Time 测试集上的 PSNR/SSIM/LPIPS）、**视觉质量**（VBench 六维指标）和**相机控制精度**（OpenVideoHD 上的旋转/平移误差）。所有对比方法在相同的数据集切分、相机轨迹和评估协议下进行，确保公平性。相机控制评估使用一致的位姿对齐方法，并通过 DUSt3R 估计第一帧位姿以消除尺度歧义。

### 时间控制主结果

Table 2 报告了在 Cam×Time 测试集上各方法的时间控制量化对比，覆盖方向控制（前向/后向）、速度控制（慢动作模式）和子弹时间三种配置。SpaceTimePilot 在所有配置下均显著优于基线：

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_25075/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison across temporal controls (Direction (forward, backward motion), Speed (slow modes), Bullet Time). We report PSNR↑, SSIM↑, and LPIPS↓. Best results are in bold. SpaceTimeMethod showcase best performance for temporal control overall*

- **平均 PSNR**：21.16（vs. ReCamMaster+jointdata 的 17.86，提升 +3.30；vs. ReCamMaster+preshuffled 的 15.52，提升 +5.64）
- **平均 LPIPS**：0.1764（vs. ReCamMaster+jointdata 的 0.3073，降低 0.1309）
- **平均 SSIM**：0.7674（vs. ReCamMaster+jointdata 的 0.6769）

关键对比揭示了不同时间控制策略的本质差异：**ReCamMaster+preshuffled** 通过帧重排模拟时间控制，但无法真正解耦空间与时间，表现最弱；**ReCamMaster+jointdata** 联合静态场景数据集训练获得一定时间控制能力，但控制模式单一；**TrajectoryCrafter** 先对视频进行时间重排再应用相机控制，往往导致相机运动不正确。SpaceTimePilot 通过显式的动画时间嵌入和时序变形增强训练，实现了真正的时空解耦。

### 视觉质量评估

Table 3 展示了 VBench 六维视觉质量评估结果。SpaceTimePilot 在图像质量（ImgQ 0.6486）上略优于 TrajectoryCrafter（0.6389），在背景一致性、运动平滑度、主体一致性、闪烁度和美学质量等维度上与基线方法保持可比水平。这表明引入时空解耦控制并未以牺牲生成质量作为代价。

### 相机控制精度

Table 4 报告了 OpenVideoHD 上的相机控制精度。SpaceTimePilot 在相对旋转误差（RelRot 2.71 vs. ReCamM+Aug+csrc 的 3.34）和角度 30 度内比率（RTA30 54.44% vs. 46.11%）上均取得最优。值得注意的是，增强的相机控制机制（同时使用源相机轨迹 $c_{\text{src}}$ 和目标轨迹 $c_{\text{trg}}$）使生成视频可以从任意相机角度开始，同时保持良好的相机精度，这是现有相机控制方法所不具备的能力。

### 消融实验

#### 时序变形增强 vs. 联合数据集训练

Figure 14 对比了时序变形增强（Temporal Warping）与仅使用静态场景数据集的训练效果。在子弹时间效果（t=40）下，时序变形增强提供了更多样化的时间变化信号，使模型更好地学习相机-时间解耦。进一步消融显示，在时序变形中包含冻结操作（freeze）比不包含冻结的训练效果更佳，因为冻结操作提供了“时间静止但相机运动”的极端解耦信号。

#### Cam×Time 数据集有效性

Figure 15（Top）展示了 Cam×Time 数据集与静态场景数据集的消融对比。在子弹时间效果下，联合训练 Cam×Time 数据集能够有效消除基线中的明显伪影，验证了密集时空监督的价值。Cam×Time 提供的全网格渲染（Table 1）使目标视频可以在 0 到 120 帧的完整时间范围内采样任意时序变化，这是现有数据集所不具备的。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_25075/figures/004_Table_1.jpg]]
*Table 1: Comparison of existing multi-view datasets for camera and temporal control against Cam×Time. Cam×Time provides full-grid rendering (Figure 4), enabling target videos to sample arbitrary temporal variations over the full range from 0 to 120*

#### 时间嵌入压缩器设计

Table 5 和 Figure 15（Bottom）系统消融了时间嵌入压缩器的设计选择。核心发现是：**1D-Conv 压缩器与正弦编码结合**能够锁定特定时间状态同时保持相机运动准确。相比之下，MLP 压缩器无法有效传递时间控制信号；而 RoPE(f') 方案虽然能锁定时间状态，却会同时锁定相机运动，导致相机与时间控制相互干扰。这一消融直接支撑了论文的核心设计决策——使用两层 1D 卷积（$\widetilde{\mathbf{e}} = \text{Conv1D}_2(\text{Conv1D}_1(\mathbf{e}))$）将原始帧级时间嵌入压缩到潜帧维度。

### 定性结果与失败模式分析

Figure 6 提供了时空解耦控制的定性对比。在一个要求“反向播放+从第一帧位姿开始向右平移”的测试用例中（源视频原始相机运动为推进式），SpaceTimePilot 同时实现了正确的相机控制（红色框标注）和准确的时间控制（绿色框标注）。TrajectoryCrafter 先反转帧再应用视点控制，导致相机运动不正确；ReCamMaster（联合数据集训练）无法执行时间控制，产生失败案例。

Figure 5 和 Figure 13 展示了更多时空控制组合的定性结果，包括正常播放、反向播放、子弹时间、慢动作、重放运动以及复杂的相机路径（平移、倾斜、缩放、垂直运动），模型在所有组合下均生成连贯视频。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2512_25075/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results of SpaceTimePilot. Our model enables fully disentangled control over camera motion and temporal dynamics. Each row shows a different combination of camera trajectory (left icons) and temporal warping (right icons). SpaceTimePilot produces coherent videos under diverse controls, including normal playback, reverse playback, bullet-time, slow-motion, replay motion, and complex camera paths (pan, tilt, zoom, and vertical motion)*

需要指出的是，当前论文未明确报告失败模式（如极端时空组合下的伪影、长视频自回归生成中的漂移累积等），这部分需要结合补充材料或实际使用进行人工验证。

## 定位与知识库关联

### 核心瓶颈与突破路径

现有视频生成方法在空间（相机运动）与时间（场景动态）控制上长期处于割裂状态。以 **ReCamMaster** 为代表的相机控制型视频到视频（V2V）模型仅能沿单调时间轴修改相机轨迹，无法实现倒放、慢动作、子弹时间等非单调时间流；而 4D 多视图生成方法（如 **DG4D** 等）虽能合成离散的稀疏时空视图，却无法生成连续的动态视频序列。**TrajectoryCrafter** 试图通过“先重排视频帧再施加相机控制”的两阶段策略来弥补这一缺陷，但帧重排破坏了原始相机运动的时空一致性，导致最终相机轨迹不可靠。

SpaceTimePilot 的核心突破在于将时间线概念从隐式的帧序关系中解耦为可显式调控的“动画时间”（animation time）参数，并在视频扩散模型中引入独立的时序编码模块，使相机变换与时间流成为两个独立可控的信号通道。这一设计使得模型能够自由组合任意相机轨迹与时间控制模式（倒放、慢动作、冻结、锯齿形运动等），首次在单一模型中实现了真正的时空解耦生成。

### 与基线方法的关键差异

与现有工作的本质区别体现在三个控制维度上：

| 方法 | 相机控制 | 时间控制 | 时空解耦 |
|------|----------|----------|----------|
| ReCamMaster | ✓ 任意轨迹 | ✗ 仅单调前进 | ✗ |
| TrajectoryCrafter | ✓（但帧重排后失效） | △ 帧重排模拟 | ✗（相机运动被破坏） |
| 4D 多视图方法 | ✓ 离散视点 | ✓ 离散时间点 | △（仅稀疏采样） |
| **SpaceTimePilot** | ✓ 任意轨迹 | ✓ 任意时间流 | ✓ 完全解耦 |

具体而言，**ReCamMaster + preshuffled** 变体通过帧重排模拟时间控制，但无法真正解耦空间与时间；**ReCamMaster + jointdata** 变体联合静态场景数据集训练以获得一定时间控制能力，但控制模式单一，在复杂时间操作（如子弹时间）下产生明显伪影。SpaceTimePilot 通过以下三个关键设计实现了质的跨越：

1. **动画时间嵌入与 1D 卷积压缩**：引入动画时间参数 $t \in \mathbb{R}^F$，经正弦编码后通过两层 1D 卷积压缩到潜帧维度，再与视频令牌相加（$x' = x + \mathcal{E}_{\mathrm{cam}}(\mathbf{c}) + \mathcal{E}_{\mathrm{ani}}(\mathbf{t})$）。消融实验证实（Figure 15 Bottom），1D-Conv 嵌入能够锁定特定时间状态同时保持相机运动准确，而 MLP 方案失败、RoPE(f') 方案则会同时锁定相机，导致空间与时间控制相互干扰。

2. **时序变形增强**：对目标视频施加反向播放、慢动作、冻结、锯齿形运动等操作，同时保持源视频为标准前向参考，为时间控制提供显式监督信号。相比仅使用静态场景数据的训练方案，时序变形增强提供了更丰富多样的时间变化信号（Figure 14），显著提升了相机-时间解耦能力。

3. **Cam×Time 数据集**：在现有动态场景多视图数据集上，通过全时空网格渲染（Figure 4）合成密集时空覆盖的训练样本，使目标视频能够采样从 0 到 120 帧范围内的任意时间变化。联合训练 Cam×Time 数据集能够消除基线方法中的明显伪影（Figure 15 Top），验证了密集时空监督的有效性。

### 方法适用边界

**适用场景**：SpaceTimePilot 适用于需要同时精确控制相机运动和场景时间流的动态场景生成任务，包括但不限于：
- 子弹时间效果（相机运动 + 时间冻结/慢动作）
- 倒放与快放（时间方向与速度控制）
- 复杂时空轨迹（如先慢动作后加速，同时伴随相机平移/旋转/变焦）
- 多轮自回归长视频生成（Figure 9-10），支持远超输入视频范围的视点变换

**技术约束**：
- 依赖现有动态场景多视图数据集（如 ReCamMaster、SynCamMaster）进行训练，对数据集的相机轨迹密度和时间覆盖范围有一定要求
- 自回归生成模式下，长视频的质量受限于逐段生成的累积误差
- 当前验证主要在受控的多视图数据集上进行，对完全开放域视频的泛化能力需进一步评估

### 局限与开放问题

尽管 SpaceTimePilot 在时空解耦控制上取得了显著进展，仍存在若干值得关注的局限和开放研究方向：

1. **极端时空组合的生成质量**：当相机运动与时间控制均为极端模式（如大角度旋转 + 极慢动作）时，生成视频的细节保真度和运动连贯性可能下降。当前实验主要覆盖了常见的时间控制模式（Table 2），对更极端的时空组合缺乏系统评估。

2. **长视频生成的时序一致性**：多轮自回归方案虽然支持长视频生成，但轮次间的累积漂移可能导致后期视频出现运动不连续或相机轨迹偏离。如何设计更鲁棒的长程一致性约束是一个开放问题。

3. **与 4D 表示的融合潜力**：当前方法在 2D 视频扩散模型层面实现时空解耦，与显式 4D 场景表示（如动态 NeRF、4D Gaussian Splatting）的结合可能进一步提升几何一致性和渲染质量，这一方向值得探索。

4. **真实世界视频的泛化**：Cam×Time 数据集基于合成或受控采集的多视图数据构建，模型在真实用户拍摄的单目视频上的时空控制能力尚需验证。域迁移（domain adaptation）或少量样本微调策略可能是实用的补充方案。

5. **计算效率**：全 3D 注意力机制（Full-3D Attention）虽然有效捕捉长程时空依赖，但计算开销较大。如何在保持控制精度的前提下降低推理成本，是推动实际应用落地的关键挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/SpaceTimePilot_Generative_Rendering_of_Dynamic_Scenes_Across_Space_and_Time.pdf]]
