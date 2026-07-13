---
title: "MotionV2V: Editing Motion in a Video"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/MotionV2V_Editing_Motion_in_a_Video.pdf
project_link: null
code_link: null
aliases:
- MotionV2V
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 直接编辑从输入视频提取的稀疏点轨迹（源 tracks）以产生目标轨迹（target tracks），并通过“运动反事实”视频对（内容相同但运动不同的视频对）训练一个视频扩散模型，使其学习根据轨迹偏差生成运动变化。
primary_logic: 将运动变化显式定义为“运动编辑”——输入轨迹与目标轨迹之间的偏差。利用视频扩散模型在保留场景外观的前提下生成符合目标轨迹的输出视频。通过构建运动反事实数据集并冻结主分支训练控制分支，实现了无需掩膜、支持任意帧、通用物体的真实视频运动编辑。
claims:
- 用户研究中以约70%的胜率显著优于先前方法（ATI约25%，ReVideo和Go-with-the-Flow低于5%）
- 在定量重建误差指标上全面超越基线：L2 (0.024 vs 0.038 ATI), LPIPS (0.031 vs 0.072 ATI), SSIM (0.098 vs 0.094 ATI)
- 模型能够编辑任意帧出现的物体，而I2V基线只能利用首帧信息，在相机运动或中间出现物体时失败
- 定制测试集（100个视频，包含首帧不可见内容） 上 L2 (帧级L2重建误差) = 0.024
---

# MotionV2V: Editing Motion in a Video

> [!tip] 核心洞察
> 将运动变化显式定义为“运动编辑”——输入轨迹与目标轨迹之间的偏差。利用视频扩散模型在保留场景外观的前提下生成符合目标轨迹的输出视频。通过构建运动反事实数据集并冻结主分支训练控制分支，实现了无需掩膜、支持任意帧、通用物体的真实视频运动编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionV2V: 视频运动编辑 |
| 英文题名 | MotionV2V: Editing Motion in a Video |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2511.20640) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionV2V |
| Dataset | 定制测试集（100个视频，包含首帧不可见内容）, 用户研究（41人，20个视频） |

> [!tip] 效果简介
> - 定制测试集（100个视频，包含首帧不可见内容） 上，L2 (帧级L2重建误差) 0.024 vs 0.038 (ATI) (-0.014 (-36.8%))。
> - 定制测试集 上，SSIM 0.098 vs 0.094 (ATI) (+0.004 (+4.3%))；LPIPS 0.031 vs 0.072 (ATI) (-0.041 (-56.9%))。
> - 用户研究（41人，20个视频） 上，整体编辑胜率 69% vs ~25% (ATI), <5% (ReVideo, Go-with-the-Flow) (+44/64个百分点)。

## 概要

视频编辑在过去一年取得了显著进展，但现有方法几乎全部聚焦于**外观编辑**——改变视觉风格、替换纹理或添加特效，而保持视频的运动结构不变。一旦尝试改变运动本身（例如让一只猫从走近碗边改为走远、让相机推近变为拉远），基于DDIM反演的外观编辑方法和图像到视频（I2V）运动控制方法都会暴露出根本性的局限：前者无法处理运动编辑中结构对应被打破的难题，后者仅从首帧生成新视频，无法保留输入视频的完整内容，尤其在相机移动或物体在中间帧出现时完全失效（Figure 3）。

**MotionV2V** 针对这一瓶颈提出了一个全新的范式：将运动变化显式定义为“运动编辑”——输入视频中稀疏点轨迹与用户指定目标轨迹之间的偏差。其核心洞察在于，利用视频扩散模型在保留场景外观的前提下，生成符合目标轨迹的输出视频。这一范式的实现依赖两个关键设计：（1）通过“运动反事实”视频对（内容相同但运动不同的视频对）训练模型，使其学习从轨迹偏差到运动变化的映射；（2）采用冻结主分支、训练控制分支的架构，将目标轨迹作为条件注入预训练的文生视频扩散模型。

在包含首帧不可见内容的定制测试集上，MotionV2V 在重建误差指标上全面超越基于点的 I2V 基线 **ATI**：L2 误差从 0.038 降至 0.024（降低 36.8%），LPIPS 从 0.072 降至 0.031（降低 56.9%）（Table 2）。在 41 人参与、20 个视频的用户研究中，MotionV2V 以约 69% 的整体胜率显著优于 ATI（约 25%）、ReVideo（低于 5%）和 Go-with-the-Flow（低于 5%）（Table 1）。该方法无需掩膜、支持任意帧的物体控制，并支持迭代编辑以完成复杂的序列运动变化。

视频编辑是视觉内容创作的核心需求，但现有方法在**运动编辑**这一维度上存在根本性局限。当前主流范式可分为两类：一类是基于DDIM反演的外观编辑方法，它们仅修改视觉风格（如纹理、色调）而完整保留输入视频的运动结构；另一类是图像到视频（Image-to-Video, I2V）生成方法，它们从单帧静态图像出发合成新视频，天然无法利用输入视频中除首帧以外的任何信息。这两条技术路线都无法解决运动编辑的核心挑战——**结构对应被打破**：当用户希望改变物体的运动轨迹、相机路径或事件时序时，输入与输出之间的像素级对应关系不复存在，传统的外观编辑范式完全失效。

I2V方法的缺陷在真实场景中尤为突出。当相机发生显著移动，或重要物体在视频中间帧才出现时，仅凭首帧信息无法获知这些内容的存在，更无法对其进行控制。例如，一段视频中，路牌在第三帧才进入画面，I2V方法既无法“知道”路牌的存在，也无法移动它（Figure 3）。这一缺口揭示了根本瓶颈：**运动编辑必须基于完整输入视频，而非仅首帧**。

MotionV2V正是在这一背景下提出。其核心动机是将运动编辑形式化为一个显式问题：给定输入视频及其稀疏点轨迹（源轨迹），用户指定目标轨迹以表达期望的运动变化，模型在保留场景外观的前提下生成符合目标轨迹的输出视频。这一范式将运动变化定义为**源轨迹与目标轨迹之间的偏差**，从而将运动编辑转化为一个可控的、可学习的条件生成任务。

为实现这一目标，MotionV2V引入了一个关键创新：**运动反事实（motion counterfactuals）视频对**——内容完全相同但运动不同的视频对。通过从长视频中系统性地生成此类数据，模型得以学习“给定内容，改变运动”这一映射，而非简单记忆视频。这解决了训练数据缺乏配对真值的核心瓶颈。

## 核心方法与创新机理

### 1. 问题定位：运动编辑的“结构对应断裂”

现有视频编辑方法面临一个根本性瓶颈：**外观编辑**（如基于DDIM反演的方法）仅修改视觉风格，保留原始运动结构；而**图像到视频（I2V）运动控制方法**（如ATI、ReVideo、Go-with-the-Flow）仅从首帧生成新视频，无法保留输入视频的完整内容。当相机运动或物体在中间帧才出现时，首帧与后续帧之间的结构对应被打破，I2V方法必然失败（Figure 3）。

MotionV2V的切入点正是这一“结构对应断裂”——将运动变化显式定义为**源轨迹与目标轨迹之间的偏差**，并训练视频扩散模型在保留场景外观的前提下，生成符合目标轨迹的输出视频。

### 2. 关键控制变量：从“首帧条件”到“全帧轨迹偏差”

MotionV2V相对于I2V基线的方法论转变体现在四个核心维度：

| 控制维度 | I2V基线方法 | MotionV2V | 机制差异 |
|---------|------------|-----------|---------|
| **输入信息范围** | 仅首帧 | 完整视频所有帧 | 允许从任意帧提取内容，而非仅依赖首帧 |
| **运动控制信号** | 首帧上的点轨迹或光流 | 全视频稀疏点轨迹 + 显式编辑偏差 | 将“运动变化”编码为可学习的条件信号 |
| **时间控制能力** | 仅控制从首帧开始的运动 | 支持任意帧的时间控制（如延迟物体出现） | 通过轨迹可见性（点存在/消失）编码时间信息 |
| **训练数据范式** | 无需特殊训练对 | 运动反事实视频对 | 提供“内容相同、运动不同”的监督信号 |

这三个维度的转变构成了MotionV2V的核心创新骨架，其因果链条为：**全帧输入 → 轨迹偏差编码 → 运动反事实训练 → 任意帧运动编辑能力**。

### 3. 运动反事实数据：训练信号的根本重构

这是方法层面最关键的创新。传统I2V方法无需构建特殊的训练对，但也因此无法学习“内容不变、运动变化”的映射。MotionV2V通过以下流程生成运动反事实视频对（Figure 4）：

1. **目标视频提取**：从长视频 $V_{\text{full}}$ 中随机截取长度为 $F$ 的连续片段作为 $V_{\text{target}}$，起始帧 $f_{\text{start}} \sim \text{Uniform}(0, F_{\text{full}} - F)$。
2. **反事实视频生成**：随机选择起始帧 $f_{\text{start}}^{\text{cf}}$ 和结束帧 $f_{\text{end}}^{\text{cf}}$，通过帧插值或时间重采样生成 $V_{\text{cf}}$，其首尾帧与 $V_{\text{target}}$ 对齐，但中间运动轨迹不同。
3. **轨迹对应建立**：使用双向点跟踪器TAPNext在 $V_{\text{full}}$ 上跟踪关键点，获得目标轨迹 $T_{\text{target}}$ 和反事实轨迹 $T_{\text{cf}}$。

这一数据构造策略的本质是：**利用同一视频的不同时间片段，天然保证内容一致性，同时提供运动差异**。无需人工标注或3D合成，即可规模化生成训练数据。

### 4. 架构创新：冻结主分支 + 控制分支注入

MotionV2V的模型架构（Figure 5）在预训练T2V DiT模型基础上引入运动条件控制分支，其设计遵循了ControlNet的零初始化注入范式，但针对视频运动编辑做了专门适配：

- **控制分支**：复制基座DiT的前18个Transformer块，通过零初始化MLP将控制信息注入冻结的主分支。这种设计保护了预训练模型的生成质量，同时允许控制分支学习运动条件映射。
- **条件通道**：控制分支的patchifier处理48个输入通道（$3 \times 16$），对应三个条件视频在潜空间中的表示：反事实视频 $V_{\text{cf}}$、反事实轨迹 $T_{\text{cf}}$、目标轨迹 $T_{\text{target}}$。
- **轨迹栅格化**：跟踪点被渲染为不同颜色的高斯斑，作为运动条件通道。这种可视化编码使扩散模型能够直接“看见”运动偏差。

与I2V方法的核心架构差异在于：I2V方法将首帧作为条件注入，模型必须从单帧“想象”整个视频的运动；而MotionV2V同时输入完整视频和轨迹偏差，模型的任务是“修改运动”而非“生成运动”，这从根本上降低了对模型生成能力的依赖。

### 5. 推理时的反直觉设计：轨迹抖动

一个值得注意的细节是推理时对轨迹坐标的消融发现（Figure 12）：**向所有跟踪点的 $(x, y)$ 坐标添加 $\epsilon \sim \mathcal{U}(-2, 2)$ 的均匀随机噪声**，可以打破模型复制原始视频语义的倾向，使其正确遵循编辑后的运动。这一发现揭示了扩散模型在运动编辑任务中的一种“身份复制偏好”——当输入轨迹与训练数据中的源轨迹过于相似时，模型倾向于直接复制原始视频内容而非执行运动编辑。1-2像素的微小抖动足以打破这种偏好，而不会显著影响运动控制的精度。

### 6. 创新边界与待验证假设

当前创新的几个边界条件需要关注：

- **跟踪点数量约束**：推理时限制约20个跟踪点，点太少可能控制不足，太多可能导致模型忽略部分对应。这一限制与轨迹栅格化的空间分辨率有关，但具体机制尚待定量分析。
- **迭代编辑的漂移问题**：虽然支持将输出作为新输入进行迭代编辑（Figure 6），但多次迭代后主体可能逐渐漂移。当前通过重新采样缓解，但漂移的定量规律和上限未明确。
- **复杂遮挡与重光照**：动态相机与物体交互产生的复杂遮挡效果，当前模型的处理能力缺乏系统评估。

MotionV2V 提出了一种全新的视频运动编辑范式：**直接编辑从输入视频中提取的稀疏点轨迹（source tracks），将其变换为目标轨迹（target tracks），并由条件视频扩散模型生成符合目标运动、同时保留场景外观的输出视频**。该框架的核心创新在于将运动变化显式定义为输入轨迹与目标轨迹之间的“运动编辑”偏差，从而绕开了传统视频编辑方法（如基于 DDIM 反演的外观编辑或图像到视频生成）中运动结构与外观耦合的难题。

### 输入输出流

框架的输入端由三个组件构成：

1. **输入视频**：一段完整的 RGB 视频，包含待编辑的原始运动。与图像到视频（I2V）方法仅依赖首帧不同，MotionV2V 利用视频的所有帧作为条件，从而能够保留在中间帧才出现的物体信息。
2. **源轨迹（source tracks）**：从输入视频中通过双向点跟踪器（TAPNext）提取的稀疏点轨迹，以彩色高斯斑的形式栅格化渲染为视频条件通道，编码了物体的原始运动路径。
3. **目标轨迹（target tracks）**：用户通过编辑界面（Figure 8）对源轨迹进行拖拽、位移或时间重排后得到的期望运动轨迹，同样被栅格化为视频条件通道。

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/010_Figure_8.jpg]]
*Figure 8: Interface for creating motion edits. The red arrow shows the transformation from source trajectory (line) to target trajectory (triangle)*

输出端为一段与输入视频内容一致、但运动符合目标轨迹的编辑后视频。该框架天然支持**任意帧的时间控制**——例如，用户可以将物体的出现时间推迟到中间帧，这是所有基于首帧的 I2V 方法无法实现的（Figure 3）。

### 核心模块与数据流

MotionV2V 的 pipeline 由以下关键模块串联而成，其架构总览见 Figure 5：

**1. 运动反事实数据生成（训练阶段）**
这是模型能够学习“内容不变、运动改变”映射的关键。从长视频中随机截取一段作为目标视频 $V_{\text{target}}$，然后通过帧插值或时间重采样生成一个内容相同但运动不同的反事实视频 $V_{\text{cf}}$。两者的首帧和末帧直接对齐，为后续的点跟踪提供锚点（Figure 4）。这一过程产生了训练所需的“运动反事实”视频对。

**2. 双向点跟踪与轨迹栅格化**
使用 TAPNext 在视频对上建立点级运动对应，分别提取目标轨迹 $T_{\text{target}}$ 和反事实轨迹 $T_{\text{cf}}$。随后，将跟踪点渲染为不同颜色的高斯斑，形成与 RGB 视频帧尺寸相同的运动条件通道。这些通道以可视化的方式将稀疏运动信息注入模型。

**3. 3D Causal VAE 压缩**
RGB 视频帧和三个运动条件通道（反事实视频、反事实轨迹、目标轨迹）分别通过 3D Causal VAE 压缩到低维潜空间。压缩后的潜空间尺寸为：
$$F_{\text{latent}} = \left(\frac{F-1}{4}+1\right), \quad W_{\text{latent}} = \frac{W_{\text{rgb}}}{8}, \quad H_{\text{latent}} = \frac{H_{\text{rgb}}}{8}$$
控制分支的 patchifier 接收 48 个输入通道（$3 \times 16$），对应三个条件视频在潜空间中的表示。

**4. 运动条件控制分支**
在预训练的文本到视频（T2V）DiT 模型基础上，复制其前 18 个 Transformer 块作为控制分支。控制分支处理运动条件信息，通过零初始化 MLP 将控制信号注入冻结的主分支，类似于 ControlNet 的设计。这种设计确保了训练初期模型行为与原始 T2V 模型一致，随后逐步学习运动编辑能力。

**5. 文本条件**
通过预训练 T2V 模型的文本编码器提供语义级别的控制信号，辅助模型理解编辑意图。

### 推理时的关键技巧

在推理阶段，一个重要的发现是：**向所有跟踪点的 $(x, y)$ 坐标添加 1–2 像素的均匀随机噪声 $\epsilon \sim \mathcal{U}(-2, 2)$**，可以打破模型直接复制原始视频语义的倾向，迫使其真正遵循编辑后的运动轨迹（Figure 12）。如果不加抖动，模型倾向于在输出中保留原始物体的运动模式，导致编辑失效（如出现不应存在的第二个物体）。

### 补充图表

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/001_Figure_1.jpg]]
*Figure 1: Motion Edits Framework: Users provide an input video along with source motion tracks (colored dots connected by lines, extracted from the input) and target motion tracks (user-specified desired motion). Lines indicate point trajectories while dot presence/absence indicates visibility. Our diffusion model generates an output video matching the target motion. Applications: Our method can edit videos in a true sense, where content is preserved but motion is changed*

MotionV2V的核心架构围绕一个关键洞察展开：将运动变化显式建模为“源轨迹”与“目标轨迹”之间的偏差，并训练一个视频扩散模型在保留场景外观的前提下生成符合目标运动轨迹的输出视频。整个pipeline由四个紧密耦合的模块构成。

### 运动反事实数据生成

这是整个训练方法的基石。模型需要学习“内容相同但运动不同”的映射关系，因此必须构造运动反事实视频对。具体流程如Figure 4所示：从一段长视频 $V_{\mathrm{full}}$ 中随机截取长度为 $F$ 的连续片段作为目标视频 $V_{\mathrm{target}}$，起始帧 $f_{\mathrm{start}}$ 服从均匀分布：

$$f_{\mathrm{start}} \sim \mathrm{Uniform}(0, F_{\mathrm{full}} - F)$$

反事实视频 $V_{\mathrm{cf}}$ 则通过帧插值或时间重采样生成——随机选取 $V_{\mathrm{full}}$ 中的起始帧和结束帧 $f_{\mathrm{start}}^{\mathrm{cf}}, f_{\mathrm{end}}^{\mathrm{cf}} \sim \mathrm{Uniform}(0, F_{\mathrm{full}} - 1)$，利用视频生成器在两者之间插值出新的运动轨迹。由于 $V_{\mathrm{cf}}$ 的首尾帧与 $V_{\mathrm{target}}$ 的首尾帧直接匹配（锚定在原视频的相同帧上），两者共享场景内容但运动路径不同，构成了天然的训练监督对。

### 双向点跟踪与轨迹栅格化

在获得视频对后，使用双向点跟踪器 **TAPNext** 在 $V_{\mathrm{full}}$ 上建立点级运动对应。跟踪点首先在目标视频的首帧上初始化（例如通过均匀采样或用户指定），然后双向传播到整个视频序列，得到目标轨迹 $T_{\mathrm{target}}$。反事实轨迹 $T_{\mathrm{cf}}$ 则通过将相同的初始点集应用于 $V_{\mathrm{cf}}$ 的首帧并跟踪获得。

为了将轨迹信息输入扩散模型，每个跟踪点被渲染为不同颜色的高斯斑（Gaussian blob），形成与视频帧空间对齐的运动条件通道。点的存在与否直接编码了物体的可见性——点消失表示被遮挡，点出现表示物体进入画面。这种稀疏点轨迹表示是MotionV2V区别于基于密集光流方法（如Go-with-the-Flow）的关键设计选择。

### 3D Causal VAE潜空间压缩

RGB视频帧和运动条件通道通过3D Causal VAE压缩到低维潜空间。给定输入帧数 $F$ 和RGB分辨率 $H_{\mathrm{rgb}} \times W_{\mathrm{rgb}}$，潜空间维度为：

$$F_{\mathrm{latent}} = \left(\frac{F-1}{4}+1\right), \quad W_{\mathrm{latent}} = \frac{W_{\mathrm{rgb}}}{8}, \quad H_{\mathrm{latent}} = \frac{H_{\mathrm{rgb}}}{8}$$

三个条件视频（反事实视频 $V_{\mathrm{cf}}$、反事实轨迹 $T_{\mathrm{cf}}$、目标轨迹 $T_{\mathrm{target}}$）各自压缩为16通道的潜表示，拼接后形成48通道的条件输入。因果VAE确保时间维度上的因果性，即每一帧的编码仅依赖当前及之前的帧，避免未来信息泄露。

### 运动条件控制分支

如Figure 5所示，MotionV2V在预训练T2V DiT模型的基础上扩展了一个控制分支。该分支复制基座DiT的前18个Transformer块，通过零初始化MLP将控制信息注入冻结的主分支，设计理念类似ControlNet。

控制分支的patchifier处理48通道的条件潜表示，将其映射到与主分支兼容的token序列。零初始化MLP确保训练初期控制分支的输出为零，模型从原始T2V行为开始，逐步学习利用运动条件。文本条件通过预训练T2V模型的文本编码器提供语义控制，与运动轨迹条件互补——文本描述场景内容，轨迹指定运动模式。

### 推理时的轨迹抖动

消融实验揭示了一个关键实现细节：推理时向所有跟踪点的 $(x, y)$ 坐标添加均匀随机噪声：

$$\epsilon \sim \mathcal{U}(-2, 2)$$

这一1-2像素的抖动操作打破了模型“复制原始视频语义”的倾向。如Figure 12所示，不添加抖动时模型可能错误地复制出第二个物体（例如出现两个篮球），而添加抖动后模型正确遵循编辑后的运动轨迹。推测原因是训练数据的轨迹分布与推理时的精确编辑存在domain gap，抖动起到了正则化作用，迫使模型依赖轨迹偏差而非身份记忆来生成输出。

### 补充图表

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/005_Figure_5.jpg]]
*Figure 5: Our motion-conditioned video diffusion architecture. We extend a T2V DiT model with a control branch that processes three additional video conditioning channels: the counterfactual video, counterfactual motion tracks, and target motion tracks. The control branch duplicates the first 18 transformer blocks and integrates with the main branch through zero-initialized MLPs, similar to ControlNet*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/004_Figure_3.jpg]]
*Figure 3: Controlling Content on Any Frame. By conditioning on the full video, we can move and preserve content appearing on any frame. Methods like ATI rely on the first frame, failing to control objects, like the sign, that emerge mid-sequence*

## 实验与关键发现

### 整体实验设计

实验评估围绕两个核心维度展开：**运动编辑质量**（用户主观偏好）和**重建保真度**（定量误差指标）。为公平比较，作者构建了一个包含100个视频的定制测试集，这些视频经过精心筛选：首先将视频在中点处切分为前后两段，再将其中一段进行时间反转，从而生成两个首帧对齐但运动轨迹不同的视频对（见Figure 11）。该设计使得仅依赖首帧的图像到视频（I2V）基线方法能够正常运行，同时刻意纳入中间帧才出现的重要物体（如突然出现的路标、行人），以暴露I2V方法无法利用完整视频信息的固有缺陷。所有基线方法均使用官方代码和默认参数运行，不提供任何手动分割或旋转掩膜，以模拟真实用户场景。

### 用户研究：编辑质量全面领先

作者进行了4选1的头部对比用户研究，招募41名参与者评估20个视频，从三个维度进行评判：**内容保留**（Q1）、**运动反映**（Q2）和**整体偏好**（Q3）。结果如Table 1所示，MotionV2V在所有维度上均以压倒性优势胜出：

- 内容保留胜率约70%，运动反映胜率约71%，整体偏好胜率约69%
- 最强基线**ATI**的整体胜率约为25%，而**ReVideo**和**Go-with-the-Flow**均低于5%

Figure 9的柱状图进一步展示了逐问题的胜率分布，MotionV2V在所有问题上保持稳定优势。这一结果验证了V2V范式在保留场景外观方面的根本性优势——当物体在中间帧才出现时，I2V方法完全无法获取其视觉信息，而MotionV2V通过双向信息流可以从任意帧“拉取”内容。

### 定量重建误差：显著优于基线

Table 2报告了帧级光度重建误差。MotionV2V在所有指标上均取得最优结果：

| 方法 | L2 ↓ | SSIM ↑ | LPIPS ↓ |
|------|------|--------|---------|
| MotionV2V (Ours) | **0.024** | **0.098** | **0.031** |
| ATI | 0.038 | 0.094 | 0.072 |
| Go-with-the-Flow | 0.067 | 0.089 | 0.120 |
| ReVideo | 0.096 | 0.080 | 0.185 |

关键分析：
- **L2误差**：MotionV2V比ATI降低36.8%（0.024 vs 0.038），说明生成的视频帧在像素级上与目标更接近
- **LPIPS感知相似度**：MotionV2V比ATI降低56.9%（0.031 vs 0.072），表明模型在保持纹理和结构细节方面优势更加突出
- **SSIM**：提升幅度相对较小（+4.3%），这符合预期——SSIM对结构性扭曲敏感，而运动编辑场景中结构变化本身就是期望的输出，因此该指标的区分度有限

值得注意的是，Go-with-the-Flow和ReVideo的表现显著弱于ATI，这可能与它们使用较旧的Stable Video Diffusion骨架有关，而ATI和MotionV2V均基于更新的Wan系列基座模型。

### 定性对比：八种挑战场景

Figure 7展示了八个具有代表性的运动编辑场景的定性对比，涵盖**人体姿态修改**、**物体移动**、**相机运动控制**、**时间控制**和**全帧变化**等任务类型。红色圆圈标注了基线方法的关键失败点：

- **中间出现物体**：当路标、行人等在视频中段才出现时，ATI完全无法生成这些物体，因为它们不在首帧中
- **相机运动**：在相机缩放或平移场景中，I2V方法无法保持场景内容的一致性，往往产生内容漂移
- **全帧变化**：当输入和输出视频没有任何共享帧时（如时间重映射），I2V方法理论上不可行，而MotionV2V仍能通过完整视频条件完成任务

### 迭代编辑能力

Figure 6展示了MotionV2V的迭代编辑能力——将一次编辑的输出作为下一次编辑的输入，可实现复杂的连续运动变化。例如，先用黄色跟踪点完成第一次编辑，再用绿色/青色跟踪点进行第二次编辑。作者指出迭代编辑可能导致主体逐渐漂移，但可通过将输出作为新输入重新采样来缓解。

### 关键消融：轨迹抖动

Section 10报告了一项重要的推理阶段消融实验。作者发现，模型在推理时倾向于“复制”原始视频的语义内容而非遵循编辑后的运动轨迹，表现为生成重复物体（如Figure 12中无抖动时出现了第二个篮球）。通过在推理时向所有跟踪点的$(x,y)$坐标添加均匀随机噪声$\epsilon \sim \mathcal{U}(-2, 2)$（即1-2像素的抖动），可以有效打破这种身份复制偏好，使模型正确遵循目标运动。这一发现揭示了扩散模型在运动条件与内容条件之间存在竞争机制——当轨迹过于“干净”时，模型更依赖内容先验而非运动信号。

### 训练细节与公平性说明

模型在8块H100 GPU上训练约一周。训练中对目标轨迹使用更高的dropout率，以提高模型对不同运动模式的鲁棒性，避免对特定轨迹模式的过拟合。定量测试集的构建方式（中点切分+反转）确保了首帧对齐，使I2V基线能够公平运行，但该设计同时暴露了I2V方法的根本局限——无法处理中间帧信息，这正是MotionV2V的核心优势所在。

### 失败模式与局限

1. **迭代漂移**：多次迭代编辑后主体可能出现逐渐漂移，当前通过重新采样缓解，但未从根本上解决
2. **跟踪点数量限制**：推理时跟踪点数量约为20个，点太少可能控制不足，太多可能导致模型忽略部分对应
3. **极端运动**：在复杂场景或极端运动变化下，扩散模型的生成质量仍可能出现畸变
4. **动态遮挡**：动态相机与物体交互产生的复杂遮挡和重光照效果处理能力有限

### 补充图表

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/006_Table_1.jpg]]
*Table 1: User study win rates across all methods. Participants selected the best video for each question. Our method consistently wins across all evaluation criteria*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/009_Figure_7.jpg]]
*Figure 7: Comparison of our method vs. baselines across eight challenging motion editing scenarios. Each row shows a different editing task with input video, our result, and ATI’s result (with additional baselines shown for subfigure 4). Icon key: Human Pose (modifying human motion), Move Object (repositioning objects), Move Camera (changing camera motion), Time Control (retiming events), Changed All Frames (no shared frames between input/output—impossible for image-to-video methods). Colored dots track correspondence points throughout the video; dot presence/absence indicates object visibility. Red circles highlight key differences where baselines fail*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/011_Figure_9.jpg]]
*Figure 9: User study win rates per question (see Table 1 for values)*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/014_Figure_12.jpg]]
*Figure 12: The effects of trajectory jitter on motion editing. Top: without jitter, a second basketball appears. Bottom: with 1-2 pixel jitter, the edit follows correctly*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/008_Figure_6.jpg]]
*Figure 6: Iterative editing. Outputs can become inputs for subsequent edits, enabling complex sequential motion changes. Yellow dots used for first edit, green/cyan for second. Arrows added from old to new position for ease of visualization*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/002_Figure_2.jpg]]
*Figure 2: From left to right respectively, Cat Fish. In the edited video, the cat moves away from the bowl. Camera control. In the edited video, the first frame is zoomed out, middle frame is identical, the last frame is zoomed in. Duck Zoom. The edited video exhibits different content for a given frame (time) than the original, e.g. in the edited video, the duck is not visible in the first frame whereas it is visible in the original*

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2511_20640/figures/013_Figure_11.jpg]]
*Figure 11: Test Data Generation. A video is separated at the middle, and then one half is reversed. This results in two videos with a common starting frame*

## 定位与知识库关联

### 1. 与基线方法的关系

MotionV2V 的核心突破在于将视频运动编辑从“图像到视频（I2V）生成”范式重新定义为“视频到视频（V2V）运动控制”问题。这一范式转换使其与现有基线方法形成了根本性的差异。

**ATI**（基于 Wan2.1 骨架的 I2V 运动控制方法）是 MotionV2V 最直接的对比对象。ATI 仅以输入视频的首帧为条件，通过点轨迹控制从首帧开始的运动生成。这种设计存在一个结构性缺陷：当视频中存在相机运动或物体在中间帧才出现时，首帧信息不足以提供完整的内容约束。MotionV2V 通过将输入扩展为完整视频的所有帧，从根本上解决了这一问题。定量结果显示，MotionV2V 在 L2 重建误差上比 ATI 降低 36.8%（0.024 vs 0.038），LPIPS 降低 56.9%（0.031 vs 0.072），而 SSIM 提升 4.3%（0.098 vs 0.094），表明 V2V 范式在内容保真度上具有显著优势。

**ReVideo**（基于 Stable Video Diffusion 骨架）虽然也支持点轨迹控制，并允许用户指定编辑区域，但其本质上仍是 I2V 方法。在用户研究中，ReVideo 的整体编辑胜率低于 5%，远低于 MotionV2V 的 69%。这一巨大差距揭示了 I2V 范式在真实视频运动编辑场景中的根本局限：当编辑操作涉及中间帧内容时，I2V 方法无法获取必要的视觉信息。

**Go-with-the-Flow**（基于 Wan2.2 骨架）采用光流引导噪声的方式进行 I2V 运动控制。尽管光流提供了比点轨迹更密集的运动信息，但其 I2V 的本质限制使其在需要保留中间帧内容的场景中同样失效。定量指标上，Go-with-the-Flow 的 L2 误差为 0.067，约为 MotionV2V 的 2.8 倍。

值得注意的是，所有基线方法均使用官方代码和默认参数运行，且未提供手动分割或旋转掩码，以模拟真实用户场景。这种公平的对比设置使得 MotionV2V 的优势更加可信。

### 2. 方法适用边界

**适用场景**：
- 需要保留输入视频完整外观但改变物体运动轨迹的编辑任务，如物体移位、人体姿态修改、相机运动调整。
- 涉及中间帧才出现的物体的运动编辑——这是 I2V 方法无法处理的场景。
- 时间控制任务，如延迟或提前物体在视频中的出现时间。
- 迭代编辑场景：输出视频可作为新输入进行连续编辑，实现复杂的序列化运动变化。

**不适用或需谨慎使用的场景**：
- 推理时跟踪点数量限制在约 20 个：点太少可能导致控制不足，太多可能导致模型忽略部分对应关系。
- 复杂遮挡与动态光照交互场景：当前模型对极端运动变化下的畸变控制有限，这受限于扩散模型的生成质量。
- 迭代编辑存在主体漂移风险：随着编辑次数增加，输出视频中的主体可能逐渐偏离原始外观，但可通过将输出作为新输入重新采样来缓解。

### 3. 局限与开放问题

**已知局限**：
1. **迭代编辑漂移**：连续编辑可能导致主体外观逐渐偏离原始视频，目前通过重新采样可部分缓解，但未从根本上解决。
2. **复杂场景畸变**：在极端运动变化或复杂遮挡场景下，扩散模型的生成质量成为瓶颈，可能出现视觉畸变。
3. **跟踪点数量约束**：约 20 个点的推理限制可能不足以精细控制复杂场景中的所有运动元素。

**开放问题**：
1. **时空对齐机理**：模型在无时空同步的输入下如何通过 Transformer 块实现对齐？其内在机制有待进一步解释。理解这一机制可能为设计更高效的运动控制架构提供理论指导。
2. **合成数据扩展**：能否利用 3D 软件生成合成运动反事实数据，以提供完美真值对并提升控制精度，甚至减少所需控制点数？这可能突破当前依赖真实视频数据训练的局限。
3. **迭代编辑上限**：迭代编辑的次数上限及质量衰减规律尚未量化研究。未来更强大的基础视频模型能否从根本上消除这种漂移？
4. **动态相机与物体交互**：如何处理动态相机与物体交互产生的复杂遮挡和重光照效果？这需要模型同时理解场景几何和光照变化。

### 4. 知识库定位

MotionV2V 处于视频编辑、运动控制和扩散模型三个领域的交叉点。其核心贡献——运动反事实训练范式——与以下知识体系相关联：

- **视频扩散模型架构**：MotionV2V 继承了 ControlNet 式的控制分支设计（冻结主分支、复制部分 Transformer 块、通过零初始化 MLP 注入控制信号），但将其从图像域扩展到视频域，并针对运动条件进行了专门适配。
- **点跟踪技术**：依赖 TAPNext 等双向点跟踪器建立视频对间的运动对应，将底层跟踪能力转化为高层运动编辑接口。
- **运动控制表示**：采用稀疏点轨迹而非密集光流作为运动控制信号，在表达能力和用户交互便捷性之间取得平衡。轨迹栅格化（将跟踪点渲染为不同颜色的高斯斑）提供了一种直观的运动条件编码方式。

MotionV2V 的 V2V 范式为视频运动编辑设立了新的基准，其运动反事实数据生成策略和全帧条件设计为后续研究提供了可扩展的框架。未来工作可能沿着合成数据增强、更精细的运动控制表示、以及迭代编辑稳定性等方向展开。

## 原文 PDF

![[paperPDFs/arxiv_2025/MotionV2V_Editing_Motion_in_a_Video.pdf]]
