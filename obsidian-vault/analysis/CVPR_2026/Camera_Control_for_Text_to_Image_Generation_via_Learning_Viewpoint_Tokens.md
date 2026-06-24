---
title: Camera Control for Text-to-Image Generation via Learning Viewpoint Tokens
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Camera_Control_for_Text_to_Image_Generation_via_Learning_Viewpoint_Tokens.pdf
project_link: "https://randdl.github.io/viewtoken_control/"
code_link: null
aliases:
- LVTCC
- CCTIGLVT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入一个可学习的参数化视点令牌，显式编码5维相机参数（方位角、仰角、半径、俯仰角、偏航角），并与文本令牌联合处理，从而精确控制生成图像的相机视角。
primary_logic: 通过构建两部分数据集——大量3D渲染提供强几何监督，少量逼真增强维持外观多样性——训练出的视点令牌学到了可迁移的因子化几何表达，不依赖特定物体外观，从而在未知类别上泛化良好，并保持场景整体一致性。
claims:
- 我们的方法在所有相机参数上（不使用先知几何信息的方法中）均优于 Compass Control 和 Stable-Virtual-Camera，方位角平均误差从 31.07° 降至 18.11°。
- 在未见过的 26 个多样化物体上，我们的方位角误差保持 19.06°，而 Compass 退化至 37.29°，证明更强的泛化能力。
- Compass Control 在测试对象（圣诞老人、兔子、海豚）上 94.2% 的生成结果过拟合到训练对象（狮子、鸵鸟、鞋、沙发等），而我们的方法完全没有明显过拟合。
- 在极端视角（后视、高仰角）下，我们的方法仍然保持显著更低的误差，而 Compass Control 性能急剧下降。
---

# Camera Control for Text-to-Image Generation via Learning Viewpoint Tokens

> [!tip] 核心洞察
> 通过构建两部分数据集——大量3D渲染提供强几何监督，少量逼真增强维持外观多样性——训练出的视点令牌学到了可迁移的因子化几何表达，不依赖特定物体外观，从而在未知类别上泛化良好，并保持场景整体一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过学习视点令牌实现文本到图像生成的相机控制 |
| 英文题名 | Camera Control for Text-to-Image Generation via Learning Viewpoint Tokens |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.19954) · [Project](https://randdl.github.io/viewtoken_control/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Learnable Viewpoint Tokens for Camera Control |
| Dataset | 自定义测试集（37个物体，5,550个样本）, 多样化物体子集（26个物体） |

> [!tip] 效果简介
> - 自定义测试集（37个物体，5,550个样本） 上，Azimuth Mean Error (↓) 18.11° vs 31.07° (Compass Control) (-12.96°)。
> - 自定义测试集 上，CLIP Similarity (↑) 0.3555 vs 0.3433 (Compass Control) (+0.0122)。
> - 多样化物体子集（26个物体） 上，Azimuth Mean Error (↓) 19.06° vs 37.29° (Compass Control) (-18.23°)。

## 概述

当前文本到图像（T2I）生成模型尽管在图像质量上取得了长足进步，却面临一个根本性的控制瓶颈：**仅凭自然语言无法精确传达相机视点信息**。用户即使给出详尽的方位描述（如“从左侧后方45°俯视”），模型仍倾向于生成姿态几乎一致的图像——始终保持前视或地平线居中的构图偏好。这一缺陷源于文本嵌入空间对三维几何信息的表达能力不足，导致视点模糊、生成结果缺乏可控的姿态一致性。

针对上述问题，本文提出了一种**可学习视点令牌（Learnable Viewpoint Tokens）**方法，将显式的相机参数编码为与文本令牌同维度的嵌入，直接注入T2I骨干网络进行联合处理。其核心洞察在于：通过精心设计的两部分训练数据集——大规模3D渲染提供强几何监督，少量逼真增强图像维持外观多样性——视点令牌能够学到**可迁移的因子化几何表达**，不依赖特定物体外观，从而在未见类别上展现出良好的泛化能力。

在方法谱系中，该工作填补了“仅文本控制”与“依赖先知几何信息（如深度图）的强条件控制”之间的空白。与需要测试时深度图的 **ControlNet-Depth**（Zhang et al., ICCV 2023）不同，本方法仅需文本与相机参数作为输入；与仅支持方位角且存在严重过拟合的 **Compass Control** 相比，本方法支持五维相机参数（方位角、仰角、半径、俯仰角、偏航角），并在泛化性上取得质的突破。

主要实验结果表明：在自定义测试集的37个物体上，本方法的方位角平均误差降至 **18.11°**，显著优于 Compass Control 的 31.07° 和 Stable-Virtual-Camera 的 54.89°；在更具挑战性的26个多样化物体子集上，方位角误差仅小幅上升至 **19.06°**，而 Compass Control 退化至 37.29°，验证了方法的强泛化能力。CLIP 图文相似度也维持在 **0.3555**，表明视点控制精度的提升并未牺牲图像质量。在极端视角（后视、高仰角）条件下，本方法同样保持显著更低的误差，而对比方法性能急剧下降。

值得注意的是，Compass Control 在测试对象上存在严重的训练对象过拟合现象——94.2% 的生成结果呈现出狮子、鸵鸟、鞋、沙发等训练物体的外观特征，而本方法完全没有此类问题。这一对比有力证明了因子化几何表达相对于直接记忆训练外观的优势。

本方法仍存在若干局限：T2I骨干网络对地平线居中构图的先验偏好难以完全克服；当前数据集仅覆盖仰角 [0°, 45°]，不包含 roll 旋转及可变内参；极端视角下逼真增强数据的合成仍面临挑战；人脸及精细结构生成中偶有质量下降。这些开放问题为后续研究指明了方向。

## 背景与动机

文本到图像（T2I）生成模型在图像质量、文本遵循度和构图多样性方面取得了显著进展，但在**精确相机控制**这一维度上仍存在根本性瓶颈。当前模型仅依赖自然语言描述来传达视点意图——例如“从左侧45°看一辆白色轿车”——但这种方式存在两个固有缺陷：其一，自然语言对连续几何参数的表达能力有限，无法精确量化方位角、仰角等相机参数；其二，即使提供了详细的空间描述，模型也常常无法一致地遵循这些指令。

这一问题的严重性在近期最强模型中同样突出。**GPT-5** 在接收“从前视图向左/右偏离45°/30°看一辆白色轿车”的提示时，三次生成结果的方向几乎完全相同（Figure 2），表明模型对语言中的视角变化不敏感。**Gemini 2.5 Flash Image（Nano Banana）** 即便获得了详尽的相机描述（如“从后四分之三角度斜向展示其尾部和左侧”），也经常无法生成正确的相机姿态（Figure 1）。这些失败案例揭示了一个核心事实：**自然语言本质上不是相机参数的合适载体**。

### 现有方法的局限

为解决这一问题，已有工作尝试引入额外的几何条件信号。**ControlNet-Depth**（Zhang et al., ICCV 2023）通过深度图提供精确的几何先验，能够实现高精度的视点控制，但其需要测试时提供目标物体的深度信息——这是一种“先知”级别的几何信息，在实际生成场景中不可得。**Stable-Virtual-Camera** 则要求提供前视图图像作为输入，本质上属于新颖视角合成而非纯文本驱动的生成。**Compass Control** 首次尝试将方位角编码为可学习的视点令牌，仅需文本和方位角参数即可控制相机，但其存在严重的**过拟合问题**：在测试对象（圣诞老人、兔子、海豚）上，94.2%的生成结果过拟合到训练对象（狮子、鸵鸟、鞋、沙发等），且仅支持方位角单一维度的控制，无法处理仰角、半径、俯仰角和偏航角。

### 本文动机与核心思路

上述分析指向一个清晰的研究缺口：**如何在不依赖测试时几何先验的前提下，实现对相机视角的多维度、可泛化精确控制？**

本文的核心洞察是：相机视点本质上是一个**因子化的几何表示**——方位角、仰角、半径、俯仰角、偏航角这五个参数独立地定义了相机相对于物体的空间关系，且这种几何关系应当与物体的具体外观解耦。基于这一洞察，本文提出将相机参数显式编码为**可学习的视点令牌**，与文本令牌联合输入T2I骨干网络。关键在于训练策略：通过构建**两部分数据集**——大规模3D渲染提供强几何监督（373K张），少量逼真增强维持外观多样性（6.6K张），等比例采样训练——使视点令牌学到可迁移的几何表达，而非记忆特定物体的外观-视角关联。

这种设计的因果机制在于：渲染数据提供了无歧义的几何真值，迫使模型学习参数化视角与图像投影之间的确定性映射；而逼真增强数据则防止模型退化到仅能生成渲染风格的图像。两者结合，使得视点令牌在未见过的物体类别上仍能保持几何控制的精度（方位角误差19.06° vs Compass Control的37.29°），同时维持高图像质量和文本遵循度。

## 核心创新

当前文本到图像（T2I）模型的核心瓶颈在于：无论使用多么精细的自然语言描述（如“从后方四分之三视角展示其尾部与左侧”），模型仍难以精确解释相机参数，导致视点模糊、同一物体在不同生成中姿态不一致。本文的因果调控点在于引入一种**可学习的参数化视点令牌**，将5维相机参数显式编码为与文本令牌同维度的嵌入，并与文本令牌联合处理，从而在生成过程中精确控制相机视角。

与现有工作的关键差异体现在以下三个 changed slots 上：

### 输入类型：从纯文本到显式相机参数编码

现有 T2I 模型仅接受纯文本提示，即使部分方法（如 Compass Control）引入了视点令牌，也仅支持单一的方位角控制。本文提出将相机视点参数化为一个5维向量：

$$\pmb \theta = ( \theta _ { \mathrm { a z } } , \theta _ { \mathrm { e l } } , r , \theta _ { \mathrm { p i t c h } } , \theta _ { \mathrm { y a w } } ) \in \mathbb { R } ^ { 5 }$$

该表示包含方位角、仰角、半径、俯仰角和偏航角，覆盖了完整的相机外参空间。通过一个3层 MLP（ViewpointMLP）将编码后的参数映射为 $d$ 维令牌嵌入：

$$\mathbf { e } _ { \mathrm { v i e w } } = \mathbf { M L P } _ { \mathrm { v i e w } } ( \phi ( \pmb { \theta } ) ) \in \mathbb { R } ^ { d }$$

其中 $\phi(\pmb\theta)$ 对方位角采用正余弦编码以处理周期性，其余参数直接使用弧度值（半径归一化到 $[0,1]$）。该视点令牌被插入到文本描述中物体名称附近，与文本令牌一同送入 T2I 骨干网络进行联合处理。

### 训练数据集构成：大规模3D渲染 + 逼真增强的双轨策略

通用图文对数据缺乏精确的相机标注，无法为视点控制提供有效监督。本文构建了一个两部分数据集：
- **大规模3D渲染子集**（373K 张）：提供强几何监督，使模型学习精确的相机-图像对应关系；
- **逼真增强子集**（6.6K 张）：通过 Nano Banana 对渲染图像进行风格化增强，维持外观多样性，防止模型过拟合到渲染域。

训练时以等比例采样两个子集。消融实验证实了该策略的关键性：移除渲染子集后，方位角平均误差从 18.11° 升至 22.98°，证明几何监督是视点精度不可替代的支柱。

### 视点参数化：从单一维度到因子化5维表示

Compass Control 仅支持方位角控制，且存在严重的训练对象过拟合问题——在测试对象上 94.2% 的生成结果过拟合到训练对象（狮子、鸵鸟、鞋、沙发等）。本文的因子化5参数表示使视点令牌学到了可迁移的几何表达，不依赖特定物体外观。消融实验进一步验证了该编码的优越性：使用 Plücker 射线编码或12维相机矩阵编码分别导致方位误差升至 21.61° 和 24.44°，均劣于本文的因子化编码。

这一因子化设计带来的泛化能力在多样化物体子集上尤为突出：在 26 个未见过的物体上，本文方法的方位角误差保持 19.06°，而 Compass Control 退化至 37.29°，差距从主测试集的 12.96° 扩大至 18.23°。即使在极端视角（后视、高仰角）下，本文方法仍保持显著更低的误差（方位角 23.27° vs. Compass 39.07°），而 Compass Control 性能急剧下降。

## 整体框架

本研究提出一种可学习视点令牌（Learnable Viewpoint Tokens）方法，将显式相机参数注入文本到图像（T2I）生成流程，实现对生成图像视角的精确控制。该方法的核心思想在于：将相机视点参数编码为与文本令牌同维度的嵌入向量，插入到文本提示中，使 T2I 骨干网络在联合处理文本与视点信息时，能够感知并遵循指定的几何约束。

### 输入与输出

方法的输入包含两部分：
- **文本提示**：描述场景内容的自然语言字符串，例如“A photo of a sedan in an ancient Greek temple ruin”。
- **相机参数 $\pmb \theta$**：一个 5 维向量，显式定义相机视点：

$$\pmb \theta = ( \theta _ { \mathrm { a z } } , \theta _ { \mathrm { e l } } , r , \theta _ { \mathrm { p i t c h } } , \theta _ { \mathrm { y a w } } ) \in \mathbb { R } ^ { 5 }$$

其中 $\theta_{\mathrm{az}}$ 为方位角（azimuth），$\theta_{\mathrm{el}}$ 为仰角（elevation），$r$ 为半径（radius），$\theta_{\mathrm{pitch}}$ 和 $\theta_{\mathrm{yaw}}$ 分别为俯仰角和偏航角（Sec 3.1, Eq 1）。该参数化采用球坐标系，将相机视点因子化为五个独立维度，便于模型学习解耦的几何表征。

输出为一张与输入文本描述一致、且严格遵循指定相机参数的生成图像。

### 模块架构与数据流

整个 pipeline 由三个核心模块串联构成，如 Figure 3 所示：

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/004_Figure_3.jpg]]
*Figure 3: Architecture overview. An MLP encoder maps camera parameters to a token embedding that is processed jointly with text tokens for viewpoint-conditioned image generation. We fine-tune the image generation model [7, 34, 42] jointly with the camera token encoder. The rendered red car in the prompt is only shown to illustrate the desired viewpoint*

**1. 相机参数编码器（ViewpointMLP）**

该模块负责将 5 维相机参数映射为与文本令牌同维度的嵌入向量。首先通过编码函数 $\phi$ 对原始参数进行预处理：

$$\phi ( \pmb \theta ) = [ \sin ( \theta _ { \mathrm { a z } } ) , \cos ( \theta _ { \mathrm { a z } } ) , \theta _ { \mathrm { e l } } , r , \theta _ { \mathrm { p i t c h } } , \theta _ { \mathrm { y a w } } ] \in \mathbb { R } ^ { 6 }$$

该编码策略的关键在于：对方位角使用正弦和余弦编码以处理其周期性（$0°$ 与 $360°$ 应等价），其余参数直接使用弧度值或归一化后的标量值（Sec 3.2, Eq 2）。随后，一个 3 层 MLP 将 6 维编码向量映射为 $d$ 维视点令牌嵌入：

$$\mathbf { e } _ { \mathrm { v i e w } } = \mathbf { M L P } _ { \mathrm { v i e w } } ( \phi ( \pmb { \theta } ) ) \in \mathbb { R } ^ { d }$$

其中 $d$ 与 T2I 骨干网络的文本令牌嵌入维度一致（Sec 3.2, Eq 3）。

**2. 视点令牌注入**

生成的视点令牌 $\mathbf{e}_{\mathrm{view}}$ 被插入到文本令牌序列中，位置靠近描述目标物体的词语（Sec 3.2）。这种注入策略使视点信息在注意力机制中与物体语义紧密关联，而非作为全局上下文松散地影响整个场景。最终，扩展后的令牌序列作为 T2I 骨干网络的输入。

**3. 文本到图像骨干网络**

骨干网络接收文本令牌与视点令牌的联合序列，通过扩散模型或类似架构生成最终图像。该方法设计为与任意基于文本嵌入的 T2I 模型兼容（Sec 3）；主实验使用 Harmon 作为骨干，并在 Stable Diffusion 2.1 和 Stable Diffusion 3.5 上验证了泛化性（Table 6）。

### 训练策略与数据流

训练时，ViewpointMLP 与 T2I 骨干网络进行联合微调。消融实验表明，冻结骨干网络仅训练 MLP 会导致方位角误差从 18.11° 急剧上升至 40.19°，证明骨干网络必须通过微调获得 3D 几何感知能力（Table 6）。训练采用差异化学习率：ViewpointMLP 使用 $2 \times 10^{-4}$，预训练骨干网络使用 $2 \times 10^{-5}$，以平衡新模块的快速收敛与骨干网络知识的保留（Sec 4.1）。

训练数据由两部分等比例采样构成：大规模 3D 渲染数据集（373K 张）提供强几何监督，逼真增强数据集（6.6K 张）维持外观多样性。消融实验证实，移除渲染子集会导致方位误差从 18.11° 升至 22.98°，说明几何监督对学习精确视点控制至关重要（Table 6）。

### 与基线方法的关键差异

相比仅支持方位角控制的 Compass Control，本方法将控制维度扩展至完整的 5 参数相机位姿，并通过因子化编码与两阶段数据集设计，实现了更强的泛化能力——在未见过的 26 个多样化物体上，方位角误差仅为 19.06°，而 Compass Control 退化至 37.29°（Table 3）。与使用深度图作为先知几何信息的 ControlNet-Depth（Lvmin Zhang et al., ICCV 2023）相比，本方法仅需文本与相机参数作为输入，无需测试时几何信息，属于更轻量且更通用的方案。

## 核心模块与公式推导

### 方法总览

本文提出一种**可学习视点令牌 (Learnable Viewpoint Tokens)** 机制，将显式相机参数编码为与文本令牌同维度的嵌入向量，注入文本到图像 (T2I) 生成骨干网络，实现精确的相机视角控制。该方法无需深度图等先知几何信息，可与任何以文本嵌入为输入的 T2I 模型兼容。

整体架构如 Figure 3 所示，包含三个核心模块：**视点参数化**、**ViewpointMLP 编码器**、**视点令牌注入**。给定文本提示与 5 维相机参数 $\pmb{\theta}$，ViewpointMLP 将其映射为 $d$ 维嵌入 $\mathbf{e}_{\mathrm{view}}$，插入文本令牌序列中物体名称附近，与文本令牌联合输入 T2I 骨干网络进行微调。

### 视点参数化 (Viewpoint Parameterization)

相机视点采用因子化的 5 维球坐标表示：

$$\pmb{\theta} = (\theta_{\mathrm{az}}, \theta_{\mathrm{el}}, r, \theta_{\mathrm{pitch}}, \theta_{\mathrm{yaw}}) \in \mathbb{R}^{5}$$

各参数含义：
- **$\theta_{\mathrm{az}}$**：方位角 (azimuth)，控制相机绕物体的水平旋转角度。
- **$\theta_{\mathrm{el}}$**：仰角 (elevation)，控制相机垂直方向的观察角度，数据集覆盖 $[0^\circ, 45^\circ]$。
- **$r$**：半径 (radius)，相机到物体的距离，归一化到 $[0, 1]$。
- **$\theta_{\mathrm{pitch}}$**：俯仰角 (pitch)，相机绕自身横轴的旋转。
- **$\theta_{\mathrm{yaw}}$**：偏航角 (yaw)，相机绕自身纵轴的旋转。

该因子化表示将相机外参分解为直观可控的分量，相较于 Plücker 射线或 12 维相机矩阵，更易于学习且泛化性更强（消融实验证实后者方位误差分别升至 21.61° 和 24.44°，Table 6）。

### 参数编码函数 (Parameter Encoding)

为处理方位角的周期性，对 $\theta_{\mathrm{az}}$ 施加正余弦编码，其他参数保持原始弧度值：

$$\phi(\pmb{\theta}) = [\sin(\theta_{\mathrm{az}}), \cos(\theta_{\mathrm{az}}), \theta_{\mathrm{el}}, r, \theta_{\mathrm{pitch}}, \theta_{\mathrm{yaw}}] \in \mathbb{R}^{6}$$

该 6 维编码 $\phi(\pmb{\theta})$ 作为 ViewpointMLP 的输入。正余弦编码确保 $\theta_{\mathrm{az}}$ 在 $0^\circ$ 和 $360^\circ$ 处的连续性，避免网络学习到虚假的不连续边界。

### ViewpointMLP 编码器

视点令牌嵌入由三层 MLP 生成：

$$\mathbf{e}_{\mathrm{view}} = \mathbf{MLP}_{\mathrm{view}}(\phi(\pmb{\theta})) \in \mathbb{R}^{d}$$

其中 $d$ 与 T2I 骨干网络的文本令牌嵌入维度一致。**ViewpointMLP** 是整个方法中唯一新增的可学习模块，参数量极小，训练时使用独立的学习率 $2 \times 10^{-4}$（骨干网络学习率为 $2 \times 10^{-5}$）。

### 视点令牌注入 (Viewpoint Token Injection)

生成嵌入 $\mathbf{e}_{\mathrm{view}}$ 后，将其插入文本令牌序列中目标物体名称的相邻位置。具体而言，若文本提示为 “A photo of a [object]”，则令牌序列变为：

```
[A, photo, of, a, <viewpoint_token>, <object_token>, ...]
```

这种插入策略使得视点信息在注意力机制中与物体语义紧密耦合，引导生成模型在保持物体外观一致性的同时，精确服从指定的相机姿态。实验表明，该设计使得视点控制与文本理解协同工作，而非相互干扰（Table 4 中 GenEval 单物体与颜色一致性指标保持稳定）。

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/008_Table_4.jpg]]
*Table 4: GenEval benchmarks for single object and color adherence*

### 训练策略

训练采用两部分数据集等比例采样：大规模 3D 渲染数据（373K 张）提供强几何监督，逼真增强图像（6.6K 张）维持外观多样性。ViewpointMLP 与 T2I 骨干网络联合微调，共 7,500 次迭代，batch size 192，优化器为 AdamW。消融实验证实，冻结骨干网络仅训练 MLP 会导致方位误差升至 40.19°，而移除渲染数据子集则使误差升至 22.98°（Table 6），表明骨干网络的 3D 几何感知能力和渲染数据的几何监督均不可或缺。

## 实验与分析

### 核心实验设计

为系统评估可学习视点令牌对相机控制的精度与泛化能力，作者构建了一个包含 37 个物体、每个物体 150 个视点（共 5,550 个样本）的测试集。评估指标覆盖所有 5 维相机参数——方位角（azimuth）、仰角（elevation）、半径（radius）、俯仰角（pitch）、偏航角（yaw）的均值和中位数角度误差，以及半径归一化误差和 CLIP 图文相似度。视点估计由一个在 Objaverse 渲染数据上训练的回归器完成，其跨数据集精度经 Table 7 验证可靠。

对比基线分为三类：（1）纯文本提示方法，包括原生 Harmon、SD2.1、SD3.5 及 Nano Banana（Gemini 2.5 Flash Image）；（2）使用先知几何信息的 ControlNet-Depth（**Lvmin Zhang et al., ICCV 2023**），作为精度上限；（3）仅需文本输入的视点控制方法 Compass Control 和 Stable-Virtual-Camera，构成本文的直接竞争对手。为公平起见，Compass Control 在测试时额外提供了 2D 边界框作为辅助条件。

### 主定量结果

Table 2 汇总了核心对比结果。在不使用先知几何信息的方法中，本文方法在所有相机参数上均取得最优：

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of camera pose fidelity and CLIP score. Methods are evaluated on mean and median angular errors (degrees), radius error (normalized by object size), and CLIP prompt-image similarity. Our approach achieves the best performance across all metrics among models without using oracle geometry information*

- **方位角均值误差 18.11°**，显著优于 Compass Control 的 31.07° 和 Stable-Virtual-Camera 的 54.89°。中位数误差差距更大（9.71° vs. 26.22° vs. 55.53°），说明本文方法的误差分布更集中，极端偏差更少。
- **仰角误差 8.75°**，远低于 Compass Control 的 17.46°。半径、俯仰角、偏航角误差同样全面领先。
- **CLIP 相似度 0.3555**，略高于 Compass Control 的 0.3433，表明视点控制精度的提升并未以牺牲图像质量或文本对齐为代价。

ControlNet-Depth 因使用测试物体的深度图作为输入，方位角误差仅 11.52°，代表了该任务的上限。本文方法在无需任何测试时几何信息的条件下，已将该差距缩小至约 6.6°。

### 泛化能力验证

Table 3 将 37 个测试物体按难度分为两组：11 个“简单”物体（训练集中有相似类别）和 26 个“多样化”物体（训练集中无对应类别）。在多样化子集上：

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/007_Table_3.jpg]]
*Table 3: Azimuth error breakdown across 11 “easy” and 26 “diverse” objects*

- **本文方法方位角误差保持 19.06°**，相比完整测试集仅上升 0.95°，泛化衰减极小。
- **Compass Control 则退化至 37.29°**，误差上升 6.22°，暴露了严重的过拟合问题。

Section 4.5 的定性分析揭示了 Compass Control 过拟合的具体表现：在测试对象（圣诞老人、兔子、海豚等）上，**94.2% 的生成结果过拟合到训练对象**（狮子、鸵鸟、鞋、沙发、泰迪熊等），即模型倾向于将测试物体替换为训练时见过的外观。本文方法完全未出现此类过拟合，归因于两部分数据集的精心设计——大规模 3D 渲染提供因子化的几何监督，逼真增强数据维持外观多样性，二者等比例采样迫使视点令牌学习与物体外观解耦的几何表达。

### 极端视角鲁棒性

Table 5 专门评估了后视、高仰角等挑战性视角下的表现。本文方法在极端视角子集上的方位角误差为 23.27°，而 Compass Control 飙升至 39.07°。值得注意的是，在“后视”条件下（方位角接近 180°），本文方法误差仅小幅上升，而 Compass Control 几乎失效。这验证了因子化 5 参数编码在处理全周向视角时的优势——方位角的正余弦编码天然适配周期性，避免了角度边界处的歧义。

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/009_Table_5.jpg]]
*Table 5: Challenging viewpoints. Camera pose accuracy and CLIP score. Values in parentheses show differences compared to the main test set*

### 消融实验

Table 6 系统消融了方法的关键设计选择：

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/011_Table_6.jpg]]
*Table 6: Backbone Variation and Ablation study*

**数据策略消融：**
- **移除渲染数据子集**：方位角误差从 18.11° 升至 22.98°，证实了大规模 3D 渲染提供的几何监督对学习精确视点控制的不可或缺性。仅靠 6.6K 张逼真增强图像不足以建立稳健的相机-图像映射。

**训练策略消融：**
- **冻结骨干网络（仅训练 ViewpointMLP）**：方位角误差飙升至 40.19°，表明 T2I 骨干网络需要联合微调才能获得 3D 几何感知能力。仅靠 MLP 映射无法将相机参数有效注入扩散模型的去噪过程。

**编码方式消融：**
- **Plücker 射线编码**：方位角误差升至 21.61°，比因子化编码差约 3.5°。
- **12 维相机矩阵编码**：方位角误差升至 24.44°，差约 6.3°。
- **额外令牌**：增加视点令牌数量未带来明显收益（18.03° vs. 18.11°），表明单个令牌已能有效承载 5 维视点信息。

因子化编码的优势在于直接对应相机的物理自由度，避免了 Plücker 射线或矩阵表示中参数间的耦合与冗余，使 MLP 更容易学习解耦的几何映射。

**骨干网络变体：**
- 在 SD2.1 上复现得方位角误差 19.16°，在 SD3.5 上得 12.85°，均表现相当或更优，证实该方法不依赖特定骨干架构，几何泛化能力源于视点令牌设计和数据集策略。

### 文本对齐与图像质量

Table 4 在 GenEval 基准上评估了单物体生成和颜色一致性。本文方法在加入视点令牌后，单物体得分和颜色得分与原生 Harmon 持平甚至略优，表明视点令牌的插入未干扰文本理解。这得益于令牌插入策略——将视点令牌放置在物体名称附近，使其作为物体属性的补充而非文本语义的替代。

### 失败模式分析

Figure 9 展示了三类典型失败案例：

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/017_Figure_9.jpg]]
*Figure 9: Examples of failure cases. (a–b) Red circles highlight errors; (c) Misaligned background viewpoints*

1. **骨干先验冲突**：T2I 骨干对眼平面、水平居中的构图存在强烈先验。在生成地标等已知对象时，即使指定高仰角参数，模型仍倾向生成平视构图。这是当前方法最核心的局限性，根源在于预训练数据分布偏差。
2. **精细结构退化**：在人脸及动物五官、细长手脚等精细结构的生成中偶有扭曲或伪影，与视点令牌引入的额外条件可能加剧了扩散模型在某些区域的去噪难度有关。
3. **背景视点失配**：多物体场景中，背景的视点可能与前景物体不完全一致，反映了当前单令牌设计在处理场景级相机一致性上的局限。

### 定性结果要点

- **Figure 4** 的跨方法对比直观展示了本文方法在保持物体身份的同时精确控制视点的能力，而 Compass Control 常出现物体外观漂移，Stable-Virtual-Camera 在非前视角度下质量急剧下降。
- **Figure 7** 验证了视点令牌对不存在物体的泛化——用相同视点参数生成“藤蔓花朵做的小车”、“能量光带翅膀的飞行汽车”等幻想物体时，相机视角保持一致，证明令牌学到的是与物体外观无关的纯几何表达。
- **Figure 8** 展示了多物体独立视角控制——通过为不同物体插入不同的视点令牌，可分别控制金毛犬与马、跑者与轿车、海豚与游艇的相对视角，实现场景级组合控制。

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/019_Figure_7.jpg]]
*Figure 7: Non-existent objects. They use the same viewpoint as Fig. 1. (a): A small car made of vines and flowers on a countryside road, (b): A flying car with wings made of energy ribbons flying through a storm of glowing auroras over the Arctic, (c): An origami elephant standing on a wooden desk under soft sunlight*

### 补充图表

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/001_Figure_1.jpg]]
*Figure 1: Our model vs. Gemini 2.5 Flash Image (Nano Banana) [9]. Our encoded camera viewpoint tokens enable precise camera pose control, while Nano Banana often fails despite detailed descriptions: “angled diagonally to show its rear and left side from a rear three-quarter view (approx. 220° azimuth), with the camera slightly below eye level (10° elevation). It occupies approximately 60% of the image width, positioned in the center slightly to the left.” See Supp. B for more results. Objects shown in prompts and 3D rendering column are only shown to illustrate the desired viewpoints*

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/002_Figure_2.jpg]]
*Figure 2: GPT5 viewpoint failures. Generated by GPT5 [26] using “A white sedan seen from 45°/30° to the left/right of the front view”. All three prompts result in nearly identical orientations*

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/003_Table_1.jpg]]
*Table 1: Comparison with previous work in terms of input type and camera control*

![[assets/figures/papers/paper_list_l2163_https_arxiv_org_abs_2604_19954/figures/016_Figure_10.jpg]]
*Figure 10: Examples of Nano Banana [9] dataset augmentation failing at extreme elevation (75◦, a–b) and roll (30◦, c–d). (a, c) Reference; (b, d) augmented output*

## 方法谱系与知识库定位

### 任务定位：T2I 相机控制的第三条路径

现有文本到图像（T2I）的相机/视角控制方法可归为两条主流路径：（1）**基于先验几何条件**的方法，如 **ControlNet-Depth**（Zhang et al., ICCV 2023），输入测试物体的深度图作为强几何约束，精度极高但依赖先知信息，无法泛化到无3D参考的场景；（2）**基于自然语言描述**的方法，如 GPT-5 和 Gemini 2.5 Flash Image（Nano Banana），仅依赖文本中的视角描述，但如图 2 所示，即使给出精确的角度描述（“从前视图向左/右偏45°/30°”），生成结果的方向几乎完全相同——自然语言无法精确编码连续几何量。

本文提出的**可学习视点令牌方法**开辟了第三条路径：将显式的5维相机参数（方位角、仰角、半径、俯仰角、偏航角）编码为与文本令牌同维度的嵌入，与文本令牌联合输入 T2I 骨干网络。这既不需要测试时的几何先知信息，又能实现远优于纯文本描述的精确控制。Table 1 明确对比了各方法的输入类型与控制粒度：本文是唯一同时支持文本输入和完整5自由度相机参数控制的方法。

### 与直接竞争方法的关系

**Compass Control** 是最直接的同类方法——同样采用视点令牌嵌入，但仅支持方位角控制，且存在严重的过拟合问题。本文 Section 4.5 揭示：Compass Control 在测试对象（圣诞老人、兔子、海豚）上 **94.2%** 的生成结果过拟合到训练对象（狮子、鸵鸟、鞋、沙发等），而本文方法完全没有明显过拟合。Table 3 的定量对比更直观：在未见过的26个多样化物体上，本文方位角误差保持 **19.06°**，而 Compass 退化至 **37.29°**。

造成这一差异的核心机制在于**训练数据构成**：Compass Control 仅使用有限的逼真图像训练，视点令牌学到了与特定物体外观耦合的虚假关联；本文通过构建两部分数据集——大规模3D渲染（373K张）提供强几何监督，少量逼真增强图片（6.6K张）维持外观多样性——使视点令牌学到可迁移的因子化几何表达，不依赖特定物体外观。

**Stable-Virtual-Camera** 需要给定前视图图像进行新颖视角合成，属于条件图像生成范畴，与本文的纯文本驱动设定有本质区别。Table 2 显示其方位角平均误差高达 **54.89°**，在无先知几何信息的方法中最弱。

### 方法谱系中的位置

从技术组件看，本文方法可拆解为三个可复用的模块：

1. **因子化相机参数编码**（Eq. 1–3）：将5维球坐标参数通过正余弦编码（方位角周期处理）和3层 MLP 映射为 d 维令牌嵌入。消融实验（Table 6）证实，这一编码显著优于 Plücker 射线（方位误差升至21.61°）和12维相机矩阵（24.44°），说明因子化表示更适合单视角 T2I 任务——它直接对应人类对视角的直观描述，降低了模型学习难度。

2. **视点令牌注入策略**：将视点令牌插入文本描述中物体名称附近，使注意力机制自然建立视点-物体的关联。论文未探索更复杂的注入位置或交叉注意力机制，这留下了优化空间。

3. **骨干网络联合微调**：Table 6 的冻结骨干消融（方位误差升至40.19°）表明，仅训练 MLP 编码器不足以让预训练 T2I 模型获得3D几何感知——骨干网络需要联合微调才能将视点令牌的几何信号转化为像素空间的视角变换。

### 适用边界与局限

**数据集覆盖范围**是当前方法的主要边界：训练数据仅覆盖仰角 [0°, 45°]，不包含 roll 旋转及可变内参。Figure 10 展示了 Nano Banana 在极端仰角（75°）和 roll（30°）条件下生成增强数据的失败案例——即使有3D渲染作为参考，逼真数据合成在极端视角下仍然困难，这直接限制了训练数据的多样性。

**骨干网络先验偏置**构成另一重边界：T2I 骨干网络对眼平面、水平居中的构图存在强烈先验。在地标等已知对象上，模型容易忽略指定的高仰角参数，回退到“标准照”构图。Figure 9 的失败案例展示了背景视点与指定参数不一致的问题。

**精细结构退化**：人脸及动物五官、细长手脚等精细结构在视点控制生成中偶有扭曲或伪影，这是 T2I 骨干网络在几何约束与纹理生成之间的固有张力。

### 开放问题

1. **如何突破骨干网络的构图先验？** 当前方法依赖联合微调来部分克服水平居中偏置，但对地标等强先验对象效果有限。可能的改进方向包括：引入显式的构图条件（如物体边界框位置）、在注意力层施加几何正则化、或使用更强的数据增强策略。

2. **极端视角的逼真数据合成**：仰角>45° 和 roll>0° 的逼真训练数据严重不足。能否通过改进增强策略（如更强的条件生成模型、多步精修）或直接使用3D渲染的风格迁移来实现更可靠的极端视角数据合成？

3. **多视角生成中的表示选择**：当前因子化编码适合单视角 T2I，但在多视角一致生成任务中，Plücker 射线等表示可能更有优势——它们天然编码了多视角间的几何约束。未来工作可能需要混合表示策略。

4. **视点令牌对文本理解的干扰**：视点令牌的加入是否削弱了文本令牌的语义表达能力？论文未对此进行精细量化。更优的令牌插入位置、注意力掩码机制或解耦训练策略值得探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Camera_Control_for_Text_to_Image_Generation_via_Learning_Viewpoint_Tokens.pdf]]