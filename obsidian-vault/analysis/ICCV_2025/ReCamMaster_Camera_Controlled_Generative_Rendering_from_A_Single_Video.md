---
title: "ReCamMaster: Camera-Controlled Generative Rendering from A Single Video"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.pdf
code_link: null
project_link: https://jianhongbai.github.io/ReCamMaster/
aliases:
- ReCamMaster
tags:
- ICCV_2025
- topic/camera_controlled_video
- topic/generative_rendering
- topic/video_diffusion
- topic/camera_controlled_video/general
core_operator: "帧维度条件机制（Frame-dimension conditioning）：将源视频和目标视频的令牌沿帧维度拼接，使 3D 自注意力能够同时处理两个视频，实现时空一致的新视角生成。"
primary_logic: "简单地将源视频令牌与目标视频令牌沿帧维度拼接，并利用预训练 T2V 模型中已有的 3D 自注意力进行跨视频交互，是一种被忽视但强大的视频条件策略，远优于通道维度和视图维度条件。"
claims:
- "核心创新是利用预训练 T2V 模型的生成能力，通过视频条件机制实现相机控制。"
- "帧维度条件通过沿帧维度拼接令牌，使自注意力能够跨视频交互，大幅提升视频同步性和一致性。"
- "在视觉质量（FVD 122.74 vs 187.94）和视图同步（Mat.Pix 906.03K vs 521.10K）上，帧维度条件显著优于通道和视图条件。"
- "Conditioning Strategy Ablation (Table 3) 上 FVD ↓ = 122.74 (Frame Concat)"
---

# ReCamMaster: Camera-Controlled Generative Rendering from A Single Video

> [!tip] 核心洞察
> 简单地将源视频令牌与目标视频令牌沿帧维度拼接，并利用预训练 T2V 模型中已有的 3D 自注意力进行跨视频交互，是一种被忽视但强大的视频条件策略，远优于通道维度和视图维度条件。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReCamMaster：基于单视频的相机控制生成式渲染 |
| 英文题名 | ReCamMaster: Camera-Controlled Generative Rendering from A Single Video |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2503.11647) · [Project](https://jianhongbai.github.io/ReCamMaster/) |
| Topic | #topic/camera_controlled_video #topic/generative_rendering #topic/video_diffusion #topic/camera_controlled_video/general |
| Method | Frame-dimension conditioning, 3D self-attention video conditioning, mixed T2V/I2V/V2V training |
| Dataset | UE5 multi-camera synchronized video dataset, 136K videos, 40 scenes, 122K camera trajectories |

> [!tip] 效果简介
> - Conditioning Strategy Ablation (Table 3) 上，FVD ↓ 为 122.74 (Frame Concat)，对比 187.94 (Channel Concat)，变化 -65.20。
> - Conditioning Strategy Ablation (Table 3) 上，Matched Pixels (K) ↑ 为 906.03，对比 521.10，变化 +384.93。
> - Training Strategy Ablation (Table 4) 上，FVD ↓ 为 122.74 (All strategies)，对比 171.80 (Baseline)，变化 -49.06。

## 概要

**核心问题**：给定一段单目源视频，如何生成一段相机轨迹可控的新视频，同时保持场景外观一致性和时序同步？现有方法面临双重瓶颈——缺乏高质量的多摄像机同步视频训练数据，且常用的视频条件机制（通道拼接或视图注意力）无法充分保持源视频的外观一致性与时序同步。

**核心方法**：ReCamMaster 提出**帧维度条件机制**（Frame-dimension conditioning），将源视频与目标视频的令牌沿帧维度拼接，使预训练 T2V 模型中的 3D 自注意力能够同时处理两个视频，实现时空一致的新视角生成。这一设计的关键洞见在于：利用预训练模型中已有的 3D 自注意力进行跨视频交互，是一种被忽视但极其强大的视频条件策略，远优于通道维度和视图维度条件。

**方法定位**：ReCamMaster 属于相机可控的视频到视频生成方法，与 GCD（Van Hoorick et al., arXiv 2024）的通道拼接方案、ReCapture（Zhang et al., arXiv 2024）的逐视频优化方案、MotionCtrl（Wang et al., arXiv 2023）和 CameraCtrl（He et al., arXiv 2023）的相机控制方案形成对照。其核心架构基于 Rectified Flow 框架的 Transformer 扩散模型，通过 3D VAE 压缩视频，并仅微调 3D 注意力层与相机编码器以保持基础模型能力。

**主要结果**：在视觉质量与视图同步指标上，帧维度条件显著优于通道条件（FVD 122.74 vs 187.94）和视图条件（Matched Pixels 906.03K vs 521.10K）。配合高质量多摄像机同步渲染数据集（136K 视频、40 个场景、122K 条相机轨迹）和混合训练策略（T2V/I2V/V2V），模型在相机准确性、外观一致性和时序同步方面均取得领先性能。

### 问题背景：相机控制下的视频重生成

给定一段单目源视频，用户希望以全新的相机轨迹“重拍”该视频——即生成一段保持源视频外观一致性和时序同步的新视频，同时精确遵循用户指定的目标相机运动。这一任务被称为**相机控制的视频重生成**（camera-controlled video re-generation），在影视创作、虚拟现实和视频编辑等领域有广泛应用前景。

传统方法通常依赖显式3D重建或多视图几何，但面对动态场景、复杂遮挡和非朗伯表面时往往力不从心。近年来，生成式模型特别是文本到视频（T2V）扩散模型的快速发展为这一任务提供了新范式：利用预训练T2V模型强大的生成先验，通过某种条件机制将源视频信息注入生成过程，从而避免显式3D重建。

### 现有方法缺口

当前相机控制视频生成方法存在两个核心瓶颈：

**1. 训练数据匮乏。** 相机控制视频生成需要成对的、多摄像机同步拍摄的视频数据——即同一动态场景从不同相机视角同时记录的视频对。这类数据在真实世界中极难获取，因为需要精确标定的多相机阵列和完全同步的拍摄条件。现有方法如**GCD**（Van Hoorick et al., arXiv 2024）和**ReCapture**（Zhang et al., arXiv 2024）要么依赖单视频逐帧优化，要么使用通道拼接的条件策略，其训练数据规模和质量均受限于此瓶颈。

**2. 视频条件机制不足。** 现有方法主要采用两种条件策略将源视频信息注入生成过程：
- **通道维度拼接**（Channel-dimension concatenation）：如GCD等方法将源视频与目标视频的潜变量沿通道维度拼接后输入模型。这种方式迫使模型在通道维度上混合两个视频的特征，但通道维度的信息容量有限，难以完整保留源视频的外观细节和时序动态，容易导致内容不一致和异步伪影。
- **视图维度注意力**（View-dimension attention）：多视图生成方法中常见，将不同视图的令牌在注意力计算中交互。但这种方式通常针对静态场景设计，难以处理动态视频中的时序同步问题。

这两种策略均未能充分保持源视频的**外观一致性**（appearance consistency）和**时序同步**（temporal synchronization），导致生成视频出现纹理漂移、运动异步等严重伪影（见Figure 5）。

### 本文动机与核心思路

针对上述瓶颈，本文提出**ReCamMaster**，核心创新在于一种简单但被忽视的视频条件策略——**帧维度条件**（Frame-dimension conditioning）。

**核心洞察**：预训练T2V模型中的3D自注意力机制天然具备处理时空令牌的能力。如果简单地将源视频令牌和目标视频令牌沿帧维度拼接，使3D自注意力能够同时处理两个视频的所有时空令牌，就能实现跨视频的全局时空交互。这一策略远优于通道维度和视图维度条件，因为它充分利用了预训练模型中已有的强大注意力机制，无需引入额外的条件模块或复杂的特征注入方式。

为支撑这一方法，本文还构建了首个大规模、高质量的**多摄像机同步视频数据集**，使用Unreal Engine 5渲染引擎生成136K视频，涵盖40个高保真3D场景、13.6K动态场景和122K不同相机轨迹，为相机控制视频生成提供了系统性的训练和评估基础。

**动机总结**：ReCamMaster旨在通过帧维度条件机制和高质量渲染数据集，解决现有方法在视频条件策略和数据规模上的双重不足，实现外观一致、时序同步且相机精确可控的视频重生成。

## 核心方法与创新机理

ReCamMaster 的核心创新在于提出了一种**帧维度条件机制（Frame-dimension conditioning）**，用于将单视角源视频注入到预训练的文生视频（T2V）扩散模型中，从而实现相机可控的生成式渲染。该机制的本质是一个被忽视但极为有效的视频条件策略：将源视频与目标视频的令牌沿帧维度拼接，使模型内置的 3D 自注意力能够同时处理两个视频序列，实现跨视频的时空交互。

### 瓶颈与动机

现有的相机可控视频生成方法面临两个关键瓶颈：
1. **训练数据匮乏**：缺乏高质量的多摄像机同步视频数据，使得模型难以学习精确的视角变换与外观保持。
2. **条件机制低效**：已有方法采用的视频条件策略——如通道维度拼接（Channel-dimension concatenation，见于 **GCD** (Van Hoorick et al., arXiv 2024)）或视图维度注意力（View-dimension attention，见于多视图方法）——无法充分保持源视频的外观一致性与时序同步，常导致显著的伪影、内容不一致及动态异步。

### 核心因果旋钮：帧维度条件

ReCamMaster 将视频条件从“通道维度”或“视图维度”切换为“帧维度”，这一 changed slot 是性能跃升的直接因果旋钮。具体而言：

- **基线做法**：通道维度拼接将源视频和目标视频的潜变量在通道维上堆叠，作为扩散模型的输入；视图维度条件则将源视频作为额外的视图输入，通过交叉注意力或类似机制进行交互。
- **ReCamMaster 做法**：将源视频和目标视频经 3D VAE 编码并分块（patchify）后的令牌沿帧维度直接拼接，形成统一的输入序列 $x_i = [x_s, x_t]_{\mathrm{frame-dim}}$。随后，该序列进入预训练的 Transformer DiT 骨干网络，其 3D 时空自注意力层能够自然地跨源视频和目标视频的所有帧进行全局交互。

这一设计的核心洞察在于：预训练 T2V 模型中已有的 3D 自注意力机制本身具备强大的时空建模能力，只需将源视频令牌与目标视频令牌在帧维度上对齐并拼接，即可“免费”获得跨视频的同步与一致性约束，无需引入额外的条件分支或复杂的视图编码器。

### 证据强度

帧维度条件相对于通道/视图维度条件的优势得到了充分的实验验证（Table 3, Figure 5）：

- **视觉质量**：帧维度条件的 FVD 为 **122.74**，显著优于通道维度条件的 187.94（降低 65.20）和视图维度条件的 194.47。
- **视图同步性**：帧维度条件的匹配像素数（Matched Pixels, K）达到 **906.03**，远超通道维度条件的 521.10（提升 384.93）和视图维度条件的 573.92。

定性对比（Figure 5）进一步表明，通道条件和视图条件生成的视频存在明显的伪影、内容不一致以及与源视频的异步动态，而帧维度条件则能很好地保持外观一致性和时序同步。

### 辅助创新：相机位姿条件与混合训练策略

除核心的帧维度条件外，ReCamMaster 还引入了两个支撑性创新：

1. **相机位姿条件简化**：模型仅以目标相机的外参（旋转矩阵 $\mathbf{R}$ 和平移向量 $\mathbf{t}$）作为条件，通过 MLP 编码后加到空间注意力输出特征上：$F_i = F_o + \mathcal{E}_c(\mathsf{cam}_t)$。这隐式地让模型从源视频中推断源相机位姿，简化了输入设计。
2. **混合训练策略**：在训练中以一定概率（如 20%）将源视频帧替换为噪声，从而将 T2V、I2V 和 V2V 任务统一到同一框架中，增强了模型的泛化能力。消融实验（Table 4）表明，采用全部训练策略时 FVD 为 122.74，而基线策略（无混合训练）为 171.80，性能提升显著（降低 49.06）。

### 局限与待验证点

- 帧维度拼接使输入令牌数量加倍，增加了计算和内存开销。如何在不损失性能的前提下降低这一成本，是后续优化的开放问题。
- 模型在真实世界视频上的泛化性能仍需进一步验证，因为训练数据完全来自渲染引擎，域隙不可避免。
- 模型继承自预训练 T2V 模型的手部生成缺陷（尤其在人物特写时）尚未解决（Figure 11）。

ReCamMaster 的整体 pipeline 围绕一个核心设计展开：**将源视频的相机重拍摄问题建模为条件视频生成任务**。给定一段源视频 $V_s$ 和一条新的目标相机轨迹，模型需要生成一段在目标视角下、与源视频保持外观一致性和时序同步的新视频 $V_t$。这一目标的实现依赖于三个关键模块的协同：**视频压缩与重建的 3D VAE**、**基于 Rectified Flow 的 Transformer 去噪骨干网络**，以及本文核心的**帧维度条件注入机制**。

### 输入输出流

系统的输入端包含三个信息源：
1. **源视频 $V_s \in \mathbb{R}^{f \times c \times h \times w}$**：包含 $f$ 帧的原始视频，提供需要保持的外观和动态信息。
2. **目标相机外参 $\mathsf{cam}_t$**：描述目标视角的相机旋转矩阵 $\mathbf{R}$ 和平移向量 $\mathbf{t}$，用于控制生成视频的视角变化。
3. **目标文本提示 $p_t$**（可选）：描述目标视频内容的文本，用于统一 T2V/I2V/V2V 任务。

输出为与源视频帧数相同、但视角随目标相机轨迹变化的目标视频 $V_t$。

### 模块关系与数据流

整个 pipeline 的数据流可分为编码、条件注入、去噪生成和解码四个阶段：

**1. 3D VAE 编码阶段**  
源视频 $V_s$ 首先通过预训练的 3D VAE 编码器压缩到潜在空间，得到源潜在表示 $z_s$。同时，目标视频 $V_t$（训练时已知，推理时从噪声初始化）同样被编码为目标潜在表示 $z_t$。3D VAE 在时空维度上对视频进行压缩，显著降低了后续 Transformer 处理的计算开销。

**2. 帧维度条件注入（核心创新）**  
这是 ReCamMaster 区别于所有先前工作的关键设计。将源潜在表示 $z_s$ 和目标潜在表示 $z_t$ 分别划分为 patch 令牌后，**沿帧维度进行拼接**，形成统一的输入序列：
$$x_i = [x_s, x_t]_{\mathrm{frame-dim}}$$
其中 $x_s$ 和 $x_t$ 分别是源视频和目标视频的 patch 化潜在令牌。这种拼接方式使得后续的 3D 自注意力层能够**同时处理两个视频的所有时空令牌**，实现跨视频的全局交互。相比于先前方法采用的通道维度拼接（如 GCD）或视图维度注意力（如多视图方法），帧维度拼接让模型能够自然地学习源视频与目标视频之间的时空对应关系，这是实现高同步性和外观一致性的根本原因。

**3. 相机姿态编码与注入**  
目标相机外参 $\mathsf{cam}_t$ 通过一个轻量的 MLP 编码器 $\mathcal{E}_c$ 映射为相机特征向量，随后以加法方式注入到 Transformer 的空间注意力输出特征中：
$$F_i = F_o + \mathcal{E}_c(\mathsf{cam}_t)$$
其中 $F_o$ 是空间自注意力层的输出特征，$F_i$ 是注入相机信息后的特征，将送入后续的 3D 时空注意力层。值得注意的是，ReCamMaster **仅对目标相机外参进行编码**，而不显式提供源相机参数——模型通过帧维度条件机制中的跨视频交互，隐式地从源视频令牌中推断源视角信息。

**4. Transformer 去噪骨干与解码**  
骨干网络采用基于 DiT（Diffusion Transformer）的架构，包含空间自注意力、交叉注意力（用于文本条件）和 3D 时空自注意力层。去噪过程遵循 Rectified Flow 框架，在噪声分布 $p_1$ 和数据分布 $p_0$ 之间建立直线路径：
$$z_t = (1 - t) z_0 + t \epsilon$$
模型学习预测向量场 $v_{\Theta}(z_t, t)$，通过 ODE 映射实现从噪声到目标视频潜在表示的转换。训练时，模型以源视频令牌、目标相机姿态和目标文本为条件，重建目标视频的潜在表示。推理时，从随机噪声出发，通过 Euler 离散化迭代采样生成目标潜在表示，最后经 3D VAE 解码器重建为像素空间的目标视频。

**5. 混合训练策略**  
为统一 T2V（文本到视频）、I2V（图像到视频）和 V2V（视频到视频）的相机控制任务，ReCamMaster 在训练中以 20% 的概率将源视频令牌替换为噪声。这一简单策略使单一模型能够处理多种输入模态：当源视频令牌为噪声时，模型退化为 T2V 相机控制生成；当仅提供单帧源图像时，模型执行 I2V 任务；当提供完整源视频时，模型执行标准的 V2V 重拍摄任务。

### 训练与推理流程

训练阶段，模型在构建的大规模多摄像机同步渲染数据集上进行优化。该数据集包含 136K 视频，覆盖 40 个高质量 3D 环境、13.6K 个动态场景和 122K 条不同相机轨迹。训练时仅微调 3D 时空注意力层和相机姿态编码器，冻结其他参数以保持预训练 T2V 模型的生成能力。

推理阶段，用户提供源视频和目标相机轨迹，模型通过迭代去噪生成目标视频。目标相机轨迹可通过手动设计或从源视频中估计获得，支持匀速和变速（通过指数插值函数控制）两种运动模式。

![[assets/figures/papers/paper_list_l1494_https_arxiv_org_abs_2503_11647/figures/011_Figure_7.jpg]]
*Figure 7: Overview of the base text-to-video generation model. Figure 8. Rendered multi-camera synchronized dataset*

### 3D VAE 编解码与 Rectified Flow 框架

ReCamMaster 基于预训练的文本到视频（T2V）扩散模型构建，其基础架构如图 7 所示。视频首先通过 **3D VAE 编码器** 压缩到潜空间，得到潜变量 $z_0$；生成后再由 **3D VAE 解码器** 重建为像素视频。去噪过程在潜空间中进行，主干网络为 **Transformer DiT**，包含空间注意力、3D 时空注意力和交叉注意力层。

生成模型采用 **Rectified Flow** 框架定义噪声调度与去噪过程。前向过程沿直线路径在数据分布与标准正态分布之间插值：

$$z_t = (1 - t) z_0 + t \epsilon \quad \text{(Eq. 1)}$$

其中 $z_0$ 为干净潜变量，$\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声，$t \in [0, 1]$ 为时间步。去噪过程通过常微分方程（ODE）将噪声分布 $p_1$ 映射回数据分布 $p_0$：

$$d z_t = v_{\Theta}(z_t, t) dt \quad \text{(Eq. 2)}$$

训练目标为条件流匹配损失，回归概率路径上的向量场：

$$\mathcal{L}_{LCM} = \mathbb{E}_{t, p_t(z, \epsilon), p(\epsilon)} \| v_{\Theta}(z_t, t) - u_t(z_0 | \epsilon) \|_2^2 \quad \text{(Eq. 3)}$$

推理时采用欧拉离散化逐步采样：

$$z_t = z_{t-1} + v_{\Theta}(z_{t-1}, t) \cdot \Delta t \quad \text{(Eq. 4)}$$

### 帧维度条件机制（Frame-Dimension Conditioning）

这是 ReCamMaster 的核心创新。给定源视频潜变量 $x_s \in \mathbb{R}^{f \times c \times h \times w}$ 和目标视频潜变量 $x_t$（训练时为真实目标，推理时为噪声初始化），**帧维度条件** 将两者沿帧维度拼接后输入 DiT 骨干网络：

$$x_i = [x_s, x_t]_{\text{frame-dim}} \quad \text{(Eq. 8)}$$

拼接后的令牌序列长度为 $2f$，3D 时空自注意力层因此能够同时处理源视频和目标视频的所有帧令牌，实现跨视频的时空交互。这一设计的核心洞察在于：预训练 T2V 模型中已有的 3D 自注意力机制天然具备处理帧间关系的能力，只需将源视频令牌作为额外的帧维度输入，即可实现强大的视频条件注入，无需引入新的注意力模块或交叉注意力。

消融实验（Table 3）证实了这一设计的决定性优势：帧维度条件在视觉质量（FVD 122.74 vs. 通道拼接 187.94）和视图同步性（Matched Pixels 906.03K vs. 521.10K）上均大幅优于通道维度和视图维度条件方案。

### 相机姿态编码模块

相机控制通过向空间注意力输出注入目标相机外参实现。目标相机外参 $\mathsf{cam}_t$（包含旋转矩阵 $R$ 和平移向量 $t$）首先经过一个 **MLP 编码器** $\mathcal{E}_c$ 映射为特征向量，然后以加法形式注入空间注意力层的输出特征 $F_o$：

$$F_i = F_o + \mathcal{E}_c(\mathsf{cam}_t) \quad \text{(Eq. 9)}$$

注意，ReCamMaster 仅条件化目标相机外参，源相机信息由模型通过帧维度条件中的源视频令牌隐式推断，这简化了输入设计并避免了源相机显式建模的复杂性。

### 混合训练策略

为统一相机控制的 T2V、I2V 和 V2V 任务，ReCamMaster 在训练中以 20% 的概率将源视频潜变量 $x_s$ 替换为纯噪声，此时模型退化为标准 T2V 生成；其余 80% 情况下使用完整源视频进行 V2V 训练。这一混合策略使单一模型具备了处理多种输入模态的能力（见图 9），并在 Table 4 中得到消融验证：使用全部训练策略时 FVD 为 122.74，而基线（无混合训练）为 171.80，性能提升显著。

### 变速相机轨迹插值

为支持丰富的相机运动速度变化，ReCamMaster 采用指数插值公式计算第 $i$ 帧的相机位置 $L_i$：

$$L_{i} = L_{start} + (L_{end} - L_{start}) \cdot \left( \frac{1 - \exp(-a \cdot i / f)}{1 - \exp(-a)} \right)$$

其中 $L_{start}$ 和 $L_{end}$ 为起止位置，$f$ 为总帧数。参数 $a > 0$ 时运动先快后慢，$a < 0$ 时先慢后快，$a = 0$ 退化为匀速运动。该公式在附录 C 中给出，用于构造训练数据中的多样化相机轨迹。

## 实验与关键发现

### 主结果：与 SOTA 方法的定量对比

ReCamMaster 在视觉质量、相机精度和视图同步三个维度上全面超越现有方法。Table 1 汇总了与 **GCD** (Van Hoorick et al., arXiv 2024)、**ReCapture** (Zhang et al., arXiv 2024)、**MotionCtrl** (Wang et al., arXiv 2023) 和 **CameraCtrl** (He et al., arXiv 2023) 的定量对比。在核心视觉质量指标上，ReCamMaster 取得 FID 57.10 和 FVD 122.74，显著优于次优方法。相机精度方面，旋转误差（RotErr）和平移误差（TransErr）均达到最低，表明模型能准确执行目标相机轨迹。视图同步性指标 Matched Pixels (K) 达到 906.03，远超其他方法，验证了帧维度条件机制在保持源视频时空一致性上的核心优势。Table 2 进一步展示了在 VBench 基准上的全面领先，涵盖主体一致性、背景一致性、运动平滑度等维度。

![[assets/figures/papers/paper_list_l1494_https_arxiv_org_abs_2503_11647/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods on visual quality, camera accuracy, and view synchronization*

![[assets/figures/papers/paper_list_l1494_https_arxiv_org_abs_2503_11647/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison with state-of-the-art methods on VBench [23] metrics*

### 消融实验：条件策略的决定性作用

Table 3 对视频条件策略进行了严格消融，这是本文最核心的实验发现：

![[assets/figures/papers/paper_list_l1494_https_arxiv_org_abs_2503_11647/figures/008_Table_3.jpg]]
*Table 3: Quantitative comparison on the video conditioning strategy*

| 条件策略 | FVD ↓ | Mat. Pixels (K) ↑ |
|----------|-------|-------------------|
| 帧维度拼接（ReCamMaster） | **122.74** | **906.03** |
| 通道维度拼接（GCD 方案） | 187.94 | 521.10 |
| 视图维度注意力（多视图方案） | 194.47 | 573.92 |

帧维度拼接在 FVD 上较通道拼接降低 65.20，较视图注意力降低 71.73；在 Matched Pixels 上分别提升 384.93K 和 332.11K。Figure 5 的定性对比揭示了失败机制：通道维度条件导致严重伪影和内容不一致，视图维度条件则出现异步动态——两者均无法有效利用预训练 T2V 模型的 3D 自注意力进行跨视频交互。帧维度拼接通过将源视频和目标视频令牌沿帧维度合并，使 3D 自注意力能同时处理两个视频的时空关系，从而实现了外观一致性和时序同步的根本性突破。

### 训练策略与数据质量消融

Table 4 对训练策略进行了系统性消融。基线模型（仅使用 V2V 训练）的 FVD 为 171.80。引入 T2V/I2V/V2V 混合训练后，FVD 降至 122.74（降低 49.06），验证了以 20% 概率丢弃源视频帧（替换为噪声）统一多任务训练的有效性。仅微调 3D 注意力层和相机编码器，冻结其他参数，在保持基础模型生成能力的同时实现了最佳性能。

![[assets/figures/papers/paper_list_l1494_https_arxiv_org_abs_2503_11647/figures/010_Table_4.jpg]]
*Table 4: Ablation on our training strategies*

Table 5 揭示了数据质量的关键影响。使用高质量多相机同步渲染数据集（136K 视频，40 个场景，122K 条轨迹）训练的模型 FID 为 57.10，相比使用玩具数据集（Toy data）的 69.35 降低 12.25，在所有评估指标上均有显著提升。这证实了多样化、大规模、高质量的同步视频数据是模型性能的基础保障。

![[assets/figures/papers/paper_list_l1494_https_arxiv_org_abs_2503_11647/figures/012_Table_5.jpg]]
*Table 5: Ablation study on training data construction*

### 失败模式与局限性

Figure 11 可视化了典型失败案例，揭示了两个系统性缺陷：

1. **手部生成质量低下**：当人物特写时，生成的手部动作出现严重畸变和伪影。这是继承自预训练 T2V 模型的固有问题，ReCamMaster 的微调策略未能克服这一局限。
2. **小物体生成失败**：场景中尺寸较小的物体（如远处行人、细小道具）在生成过程中容易丢失或变形。

此外，帧维度拼接使输入令牌数量加倍，显著增加了计算和内存开销。训练数据完全由 Unreal Engine 5 渲染生成，尽管努力模拟真实世界，域隙仍然存在，在真实野外视频上的泛化能力需进一步验证。模型推理时依赖用户提供精确的目标相机轨迹，这一要求在真实应用中通常难以满足。

## 定位与知识库关联

### 核心贡献与因果机制

ReCamMaster 解决的核心瓶颈是：**缺乏高质量的多摄像机同步视频训练数据，且现有视频条件机制无法充分保持源视频的外观一致性和时序同步**。其因果操控变量是**帧维度条件机制（Frame-dimension conditioning）**：将源视频与目标视频的令牌沿帧维度拼接，使预训练 T2V 模型中的 3D 自注意力能够同时处理两个视频，实现跨视频的时空一致交互。

这一设计背后的核心洞察是：简单地将源视频令牌与目标视频令牌沿帧维度拼接，并利用预训练 T2V 模型中已有的 3D 自注意力进行跨视频交互，是一种被忽视但强大的视频条件策略，远优于通道维度和视图维度条件。实验证据（Table 3）表明，帧维度条件在视觉质量（FVD 122.74 vs 187.94）和视图同步（Mat.Pix 906.03K vs 521.10K）上显著优于通道和视图条件。

### 关键模块与设计选择

| 模块 | 功能 | 设计依据 |
|------|------|----------|
| 3D VAE 编码器/解码器 | 视频潜在空间压缩与重建 | 继承预训练 T2V 模型架构 |
| Transformer DiT 骨干 | 含空间注意力、3D 时空注意力和交叉注意力的扩散去噪 | 基于 Rectified Flow 框架 |
| 帧维度拼接模块 | 将源视频与目标视频的 patchified latents 沿帧维度拼接（Eq. 8: $x_i = [x_s, x_t]_{\mathrm{frame-dim}}$） | 核心创新，使 3D 自注意力跨视频交互 |
| 相机姿态编码器（MLP） | 编码目标相机外参 $(R, t)$ 并加至空间注意力输出（Eq. 9: $F_i = F_o + \mathcal{E}_c(\mathsf{cam}_t)$） | 仅条件于目标相机，依赖模型推断源相机 |
| 混合训练策略 | 以 20% 概率将源视频帧替换为噪声，统一 T2V/I2V/V2V 任务 | 增强泛化能力（Table 4 消融验证） |

### 与现有工作的关系

**相对于相机控制视频生成方法：**

- **MotionCtrl**（Wang et al., arXiv 2023）和 **CameraCtrl**（He et al., arXiv 2023）聚焦于从文本或单序列相机控制生成视频，未涉及将已有源视频重拍为新视角的任务。
- **ReCapture**（Zhang et al., arXiv 2024）支持相机控制视频重拍，但需要逐视频优化，缺乏前馈泛化能力。
- **GCD**（Van Hoorick et al., arXiv 2024）是此前最先进的前馈相机控制视频到视频生成方法，采用通道维度拼接作为视频条件机制。ReCamMaster 将其条件策略从通道维度改为帧维度，获得了显著的性能提升。

**相对于视频条件机制：**

ReCamMaster 系统比较了三种视频条件策略（Figure 3, Table 3）：
- **通道维度条件**（GCD 等方法采用）：将源视频与目标视频沿通道维度拼接，导致内容不一致和异步动态。
- **视图维度条件**：类似多视图方法中的视图注意力，同样存在显著伪影。
- **帧维度条件**（ReCamMaster 提出）：沿帧维度拼接，使 3D 自注意力自然实现跨视频交互，大幅提升同步性和一致性。

### 适用边界与局限

1. **训练数据域隙**：训练数据完全由 Unreal Engine 5 渲染生成（136K 视频，40 个场景，122K 轨迹），尽管努力模拟真实世界，域隙仍然存在，在真实野外视频上的泛化能力需进一步验证。

2. **继承自预训练模型的缺陷**：依赖预训练 T2V 模型，继承了其手部生成质量低（尤其是人物特写时）和小物体生成失败的局限（Figure 11）。

3. **相机轨迹假设**：推理时需用户提供目标摄像机轨迹，该轨迹通常难以精确获取；模型假设目标相机已知，未处理相机内参估计不准确的场景。

4. **计算开销**：帧维度拼接使输入 token 数量加倍，增加了计算和内存成本。

5. **评价局限性**：测试集完全由渲染视频组成，评价指标主要反映相机准确性和视觉质量，缺乏人类主观评估。

### 开放问题

1. 如何减少源视频和目标视频令牌拼接带来的计算开销，使方法更适用于资源受限场景？
2. 如何改善预训练 T2V 模型继承的手部生成问题，特别是在人物特写场景下？
3. 模型如何处理超出训练分布的极端摄像机轨迹（如大角度旋转、快速变焦）？
4. 变速轨迹参数 $a$（Eq. 7 中的指数衰减系数）对最终生成质量有何定量影响？
5. 在真实世界视频的摄像机内参估计不准确时，模型性能如何退化？是否需要引入内参估计模块或鲁棒性增强策略？

## 原文 PDF

![[paperPDFs/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.pdf]]
