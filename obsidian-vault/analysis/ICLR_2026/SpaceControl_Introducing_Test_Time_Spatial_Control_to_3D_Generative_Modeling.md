---
title: "SpaceControl: Introducing Test-Time Spatial Control to 3D Generative Modeling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SpaceControl_Introducing_Test_Time_Spatial_Control_to_3D_Generative_Modeling.pdf
project_link: https://spacecontrol3d.github.io/
code_link: null
aliases:
- SS
- SpaceControl
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "在预训练的流匹配生成模型（Trellis）中引入测试时的显式空间控制：将用户提供的3D几何信号（超二次曲面、网格等）体素化并编码为潜在变量，通过部分加噪后参与去噪过程，无需任何额外训练即可引导生成结果向给定几何对齐；一个控制参数 τ₀ 允许在几何保真度与真实感之间平滑权衡。"
primary_logic: "利用预训练编码器将几何条件映射到结构生成阶段的潜在空间，并通过调节噪声混合比例控制空间约束的强度，实现了与训练无关的、即插即用的空间控制能力。"
claims:
- "SPACECONTROL 是一种无需训练的测试时方法，可对 3D 资产生成进行显式空间控制。"
- "该方法将用户指定的几何体直接编码为潜在空间中的显式指导，无需额外训练。"
- "在 Toys4K、椅子和桌子数据集上，SPACECONTROL 的 Chamfer 距离显著优于所有基线，同时保持可比的外观质量。"
- "Toys4K (geometric primitives) 上 Chamfer Distance (CD↓, ×10³) = 14.0"
---

# SpaceControl: Introducing Test-Time Spatial Control to 3D Generative Modeling

> [!tip] 核心洞察
> 利用预训练编码器将几何条件映射到结构生成阶段的潜在空间，并通过调节噪声混合比例控制空间约束的强度，实现了与训练无关的、即插即用的空间控制能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SpaceControl：为3D生成模型引入测试时空间控制 |
| 英文题名 | SpaceControl: Introducing Test-Time Spatial Control to 3D Generative Modeling |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.05343) · [Project](https://spacecontrol3d.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | SpaceControl (SPACECONTROL) |
| Dataset | Toys4K (geometric primitives), Toys4K (meshes), Chair (geometric primitives) |

> [!tip] 效果简介
> - Toys4K (geometric primitives) 上，Chamfer Distance (CD↓, ×10³) 为 14.0，对比 Spice-E 65.9，变化 -51.9。
> - Toys4K (meshes) 上，Chamfer Distance (CD↓, ×10³) 为 4.89，对比 Spice-E 65.9，变化 -61.01。
> - Chair (geometric primitives) 上，Chamfer Distance (CD↓, ×10³) 为 0.98，对比 Spice-E 7.66，变化 -6.68。

## 概要

**问题瓶颈**：现有 3D 生成方法（如 Trellis, Xiang et al., CVPR 2025）主要依赖文本或图像提示，缺乏对生成对象几何形状的精确、直观控制。文本描述具有歧义性，图像难以编辑，用户无法直接操纵对象的几何结构——这是制约 3D 资产生成实用化的关键瓶颈。

**核心方法**：SpaceControl (SPACECONTROL) 提出了一种**无需训练的测试时空间控制**方案。其核心洞察在于：将用户提供的 3D 几何信号（超二次曲面、多边形网格等）体素化后，通过预训练编码器直接映射到结构生成阶段的潜在空间，再以部分加噪的方式参与整流流去噪过程。这一机制无需任何额外训练或架构修改，实现了即插即用的空间控制能力。一个控制参数 $\tau_0$ 允许用户在几何保真度与生成真实感之间进行平滑权衡。

**方法定位**：SPACECONTROL 属于**测试时引导**范式，区别于需要类别特定微调的训练方法（如 Spice-E、SPICE-E-T）和基于优化的测试时方法（如 Coin3D）。它建立在预训练的 Trellis 整流流生成模型之上，利用其编码器-结构流模型-外观流模型-解码器的两阶段管线，将空间条件注入结构生成阶段，而外观生成阶段可独立接受文本或图像条件。

**主要结果**：在 Toys4K 数据集上，SPACECONTROL 以超二次曲面为空间条件时 Chamfer 距离（CD↓, ×10³）为 14.0，以网格为条件时为 4.89，显著优于 Spice-E 的 65.9 和 SPICE-E-T 的 39.1（Table 1）。在 Chair 数据集上同样保持大幅领先（0.98 vs. 7.66）。用户研究（Figure 6）表明，SPACECONTROL 在整体外观、空间控制忠实度和真实感三个维度上均获得显著偏好。调节 $\tau_0$ 可连续控制几何贴合度与视觉质量之间的平衡（Figure 4, Table 2），$\tau_0 \in [4,6]$ 在 Toys4K 上提供了较好的折衷。

3D资产生成近年来取得了显著进展，以Trellis（Xiang et al., CVPR 2025）为代表的基于流匹配的生成模型，能够根据文本或图像提示生成高质量的三维对象。然而，这些方法存在一个根本性的瓶颈：**文本和图像提示难以提供精确、直观的几何形状控制**。文本描述具有天然的歧义性——同一段文字可以对应形态迥异的几何结构；图像虽能传达视觉外观，但其二维本质使得用户无法直接操纵对象的三维几何体，编辑和调整极为不便。

这一缺口直接限制了3D生成模型在实际创作流程中的应用。艺术家和设计师通常需要从粗略的3D草图出发，逐步细化对象的形状和比例，而现有生成范式却将用户隔离在几何控制之外。部分工作尝试引入几何条件，如**Spice-E**通过在Shap-E上微调以支持立方体图元，或**Coin3D**通过测试时优化将几何条件注入多视图生成模型，但这些方法要么需要类别特定的额外训练，要么依赖耗时的优化过程，在效率、精度和泛化性之间难以兼顾。

SpaceControl的出发点是：**能否在不修改预训练模型、不增加任何训练的前提下，让用户通过简单的3D几何体直接控制生成结果的空间结构？** 这一问题的核心挑战在于，预训练生成模型的潜在空间并非为几何条件设计，直接将外部几何信号注入去噪过程可能破坏生成质量。SpaceControl的解决方案利用了预训练编码器将几何条件映射到结构生成阶段的潜在空间，并通过调节噪声混合比例来控制空间约束的强度——一个参数 $\tau_0$ 即可在几何保真度与视觉真实感之间实现平滑权衡。

## 核心方法与创新机理

### 测试时空间控制：无需训练的即插即用机制

现有3D资产生成方法主要依赖文本或图像提示，文本描述具有歧义性，图像难以编辑，用户无法直接操纵对象的几何形状。**SpaceControl** 的核心创新在于将显式的3D空间控制引入预训练生成模型的**测试时推理阶段**，无需任何额外训练或架构修改。

具体而言，SpaceControl 在预训练的流匹配生成模型 **Trellis**（Xiang et al., CVPR 2025）中注入用户提供的3D几何信号——可以是超二次曲面、多边形网格等——通过以下关键步骤实现即插即用的空间引导：

1. **几何编码**：将用户提供的控制几何体体素化为 $64\times64\times64$ 的二值占用网格 $\mathbf{x}_c$，送入预训练编码器 $E$ 获得潜在表示 $\mathbf{z}_{c,0}$。
2. **部分加噪注入**：利用整流流的正向加噪方程，将控制潜在变量与噪声混合至时间步 $t_0$：
   $$\mathbf{z}_{t_0} = t_0 \mathbf{z}_1 + (1 - t_0) \mathbf{z}_{c,0}$$
3. **引导去噪**：从 $t_0$ 开始，由结构流模型在文本特征引导下进行去噪，生成的结构潜在变量 $\mathbf{z}_0$ 经解码器 $D$ 输出占用网格 $\mathbf{x}_0$，随后由外观流模型生成纹理。

这一机制的核心洞察在于：**利用预训练编码器将几何条件映射到结构生成阶段的潜在空间，并通过调节噪声混合比例控制空间约束的强度**，实现了与训练无关的、即插即用的空间控制能力。

### 相对基线的关键差异

| 方法 | 空间控制方式 | 是否需要训练 | 控制强度调节 |
|------|-------------|-------------|-------------|
| **Spice-E** | 微调 Shap-E 以支持立方体图元 | 需要类别特定微调 | 不可调节 |
| **SPICE-E-T** | 在 Trellis 上复现的 Spice-E 训练版本 | 需要类别特定微调 | 不可调节 |
| **Coin3D** | 测试时优化微调多视图生成模型 | 需要测试时优化 | 不可调节 |
| **Trellis (txt-DiT-XL)** | 仅文本提示，无空间引导 | 不适用 | 不适用 |
| **SpaceControl** | 直接编码任意3D几何体为潜在空间引导 | **无需训练** | **$\tau_0$ 连续可调** |

SpaceControl 相对基线的根本性差异体现在两个 **changed slots** 上：

- **空间条件输入**：基线方法仅接受文本或图像提示，无直接几何条件；SpaceControl 接受用户提供的任意3D几何体（超二次曲面、网格等），经体素化和编码器映射为潜在向量后参与去噪过程。
- **几何控制强度**：基线方法不具备可调节的控制强度；SpaceControl 通过参数 $\tau_0$（等价于 $t_0$）实现连续调节——低 $\tau_0$ 趋向高真实感但低保真度，高 $\tau_0$ 更贴合输入几何但可能降低真实感。

### 控制强度权衡机制

$\tau_0$ 是 SpaceControl 的核心控制旋钮，它决定了控制潜在变量在去噪起点中的混合比例。从因果机制来看：

- 当 $\tau_0 \to 0$ 时，$\mathbf{z}_{t_0} \approx \mathbf{z}_{c,0}$，去噪起点几乎完全由控制几何决定，生成结果高度贴合输入几何，但可能牺牲真实感；
- 当 $\tau_0 \to 1$ 时，$\mathbf{z}_{t_0} \approx \mathbf{z}_1$（纯噪声），空间控制几乎失效，生成结果趋向无条件生成。

实验表明（Figure 4, Table 2），在 Toys4K 数据集上，$\tau_0 \in [4, 6]$ 提供了几何保真度与真实感之间的较好折衷。这一设计使得用户可以根据任务需求灵活选择控制强度，而无需重新训练模型。

### 关键证据强度

- **无需训练的特性**得到明确声明（置信度 0.95）："we introduce SPACECONTROL, a training-free test-time method for explicit spatial control of 3D asset generation"；"requiring no additional training"。
- **定量优势**在 Toys4K 数据集上表现显著（置信度 0.95）：SpaceControl 的 Chamfer Distance 为 14.0（超二次曲面）和 4.89（网格），而 Spice-E 为 65.9，SPICE-E-T 为 39.1；在 Chair 和 Table 数据集上呈现相似趋势。
- **控制强度可调性**经消融实验验证（置信度 0.95）：增加 $\tau_0$ 可持续降低 Chamfer 距离，使生成结果更贴合输入空间控制信号。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_05343/figures/002_Figure_2.jpg]]
*Figure 2: Model Overview. Given an input conditioning which includes a spatial control, a text prompt and an image (optional), SPACECONTROL produces realistic 3D assets. First the different conditioning are encoded in a latent space. Specifically, the spatial control is voxelized and encoded by Trellis’ encoder E, the text is encoded by a CLIP encoder $\mathcal { E } _ { C L I P }$ , and the image (if present) is encoded by a DINOv2 encoder $\mathcal { E } _ { D I N O }$ . The obtained latents $\mathbf { z } _ { 0 , c }$ are noised up to $t _ { 0 }$ to obtain $\mathbf { z } _ { t _ { 0 } }$ . . From $t _ { 0 }$ to t = 0 , $\mathbf { z } _ { t _ { 0 } }$ are denoised by the Structure Flow Model (FM), guided by the...

SPACECONTROL 构建在预训练的 Trellis 两阶段生成模型（**Trellis**，Xiang et al., CVPR 2025）之上，通过测试时注入空间控制信号，在不修改模型架构、不进行任何额外训练的前提下，实现显式的 3D 几何引导。其整体流程如图 2 所示，核心思路是将用户提供的 3D 几何条件（超二次曲面或任意多边形网格）编码进 Trellis 的潜在空间，并利用整流流模型（rectified flow）的部分加噪-去噪机制，使生成过程向给定几何对齐。

### 输入与条件编码

SPACECONTROL 接受三类可选的条件输入：**空间控制几何体**、**文本提示**和**图像**。其中，空间控制几何体是该方法的核心创新——用户通过简单的 3D 图元（如超二次曲面）或精细的多边形网格来指定目标物体的几何形状。

编码流程分为三条并行的通路：
- **空间几何编码**：将用户提供的控制几何体体素化为二值占用网格 $x_c \in \{0,1\}^{64 \times 64 \times 64}$，然后送入 Trellis 预训练的编码器 $E$，得到干净的结构潜在变量 $z_{c,0}$。
- **文本编码**：文本提示通过 CLIP 编码器 $\mathcal{E}_{CLIP}$ 提取语义特征。
- **图像编码**（可选）：输入图像由 DINOv2 编码器 $\mathcal{E}_{DINO}$ 编码为视觉特征。

### 两阶段生成流程

SPACECONTROL 沿用 Trellis 的两阶段生成范式，分为**结构生成**和**外观生成**两个串行步骤。

#### 第一阶段：结构生成

结构生成的目标是产生与空间控制信号对齐的物体几何体。关键操作是将编码后的控制潜在变量 $z_{c,0}$ 注入去噪过程：

1. **控制注入**：利用整流流的前向加噪公式，将 $z_{c,0}$ 与纯噪声 $z_1$ 混合，得到时间步 $t_0$ 处的带噪潜在变量：
   $$z_{t_0} = t_0 z_1 + (1 - t_0) z_{c,0}$$
   其中 $t_0$ 对应于用户可调的控制强度参数 $\tau_0$。这一步骤决定了空间约束的强弱——$t_0$ 越小（$\tau_0$ 越小），$z_{t_0}$ 越接近干净的控制信号 $z_{c,0}$，生成结果越贴合输入几何。

2. **结构去噪**：以 $z_{t_0}$ 为起点，结构流模型（Structure Flow Model）在文本提示特征的引导下，通过迭代去噪步骤逐步恢复到 $t=0$ 的干净潜在变量 $z_0$。去噪过程遵循整流流的离散化反向步骤：
   $$\mathbf{z}_{t(i+1)} = \mathbf{z}_{t(i)} - \mathbf{v}_{\theta}(\mathbf{z}_{t(i)}, t(i)) (t(i) - t(i+1))$$

3. **几何解码**：解码器 $D$ 将干净的结构潜在变量 $z_0$ 解码为二值体素网格 $x_0$，完成几何结构的生成。

#### 第二阶段：外观生成

外观生成在已确定的几何结构上进行：

1. **活动体素扩展**：根据 $x_0$ 中的活动体素位置，为每个点分配带噪声的潜在外观特征。
2. **外观去噪**：外观流模型（Appearance Flow Model）使用文本或图像条件引导去噪过程，生成干净的外观潜在变量。
3. **多格式解码**：通过特定的外观解码器 $\mathcal{D}_O = \{\mathcal{D}_{GS}, \mathcal{D}_{RF}, \mathcal{D}_{M}\}$，将外观特征解码为多种可视化格式，包括 3D 高斯（3D Gaussians）、辐射场（Radiance Fields）和网格（Meshes）。

### 核心机制：控制强度调节

SPACECONTROL 的核心创新在于通过单一超参数 $\tau_0$ 实现几何保真度与生成真实感之间的平滑权衡。这一参数直接控制 $z_{c,0}$ 的噪声混合比例，进而影响空间约束的强度：

- **低 $\tau_0$**：控制信号较弱，生成结果更依赖文本提示的先验分布，倾向于产生高真实感但可能与输入几何存在偏差的资产。
- **高 $\tau_0$**：控制信号较强，生成结果更严格贴合输入几何，但可能牺牲一定的视觉真实感。

实验表明，$\tau_0 \in [4,6]$ 在 Toys4K 数据集上提供了较好的折衷（参见图 4 和表 2）。用户可根据具体应用场景自由选择 $\tau_0$ 值，无需重新训练或调整模型。

### 与基线方法的本质区别

相比需要类别特定微调的 **Spice-E** 和 **SPICE-E-T**，以及基于测试时优化的 **Coin3D**，SPACECONTROL 的即插即用特性源于其对预训练编码器 $E$ 的充分利用——将几何条件直接映射到结构生成阶段的潜在空间，而非修改生成模型本身。这一设计使其在无需训练的前提下，既能处理粗略的 3D 草图（如超二次曲面），也能精确对齐精细的网格控制信号。

### 问题瓶颈与因果调节变量

现有3D生成方法（如基于文本或图像的提示）难以提供精确、直观的几何形状控制——文本具有歧义性，图像难以编辑，用户无法直接操纵对象几何体。SpaceControl（SPACECONTROL）的核心因果调节变量是：**在预训练的流匹配生成模型（Trellis）中引入测试时的显式空间控制**，将用户提供的3D几何信号体素化并编码为潜在变量，通过部分加噪后参与去噪过程，无需任何额外训练即可引导生成结果向给定几何对齐。

### 管道模块

SPACECONTROL 建立在 Trellis（Xiang et al., CVPR 2025）的两阶段生成框架之上，由以下关键模块构成（参见Figure 2）：

**Encoder E**：将体素化的控制几何体 $x_c \in \{0,1\}^{64\times64\times64}$ 编码为潜在表示 $z_{c,0}$。这是将显式几何信号映射到结构生成潜在空间的关键桥梁，使空间条件能够直接参与后续的去噪过程。

**Structure Flow Model**：以带噪的控制潜在变量 $z_{t_0}$ 为起点，结合文本提示特征进行去噪，生成结构潜在变量 $z_0$。该模块是空间控制的核心执行者——从时间步 $t_0$ 开始（而非纯噪声 $t=1$），模型在文本语义的引导下将粗略的几何条件细化为完整、合理的3D结构。

**Decoder D**：将结构潜在变量 $z_0$ 解码为二值占用网格 $x_0$，确定物体的几何形状。

**Appearance Flow Model**：为活动体素生成外观特征，可使用文本或图像条件。该模块独立于结构生成，使得纹理和材质可以在几何结构确定后灵活指定。

**Appearance Decoders ($D_{GS}, D_{RF}, D_M$)**：将外观特征解码为多种可视化格式，包括3D高斯（GS）、辐射场（RF）和网格（M）。

### 关键公式推导

**整流流去噪步骤**（Eq. 1）：SPACECONTROL 建立在整流流模型（Rectified Flow Models）之上，其离散化的反向去噪过程为：

$$\mathbf{z}_{t(i+1)} = \mathbf{z}_{t(i)} - \mathbf{v}_{\theta}(\mathbf{z}_{t(i)}, t(i)) \, (t(i) - t(i+1))$$

其中 $t(i)$ 为离散化时间步，$\mathbf{v}_{\theta}$ 为学习到的速度场。该公式描述了从噪声逐步恢复干净潜在变量的迭代过程。

**时间步重缩放**（Eq. 2）：为调节生成质量，引入因子 $\lambda$ 对时间步进行重缩放：

$$t(\tau) = \frac{\lambda t(\tau)}{1 + (\lambda - 1) t(\tau)}$$

该变换改变了采样过程中各时间步的密度分布，影响生成结果的细节层次。

**控制潜在变量的前向加噪**（Eq. 4）：这是SPACECONTROL实现测试时空间控制的核心操作。将编码后的控制潜在变量 $z_{c,0}$ 与纯噪声 $z_1$ 按时间步 $t_0$ 混合：

$$\mathbf{z}_{t_0} = t_0 \mathbf{z}_1 + (1 - t_0) \mathbf{z}_{c,0}$$

该公式的因果含义是：$t_0$ 越大，混合中噪声比例越高，几何条件的影响越弱，模型有更大自由度生成偏离控制几何的结构（高真实感、低保真度）；$t_0$ 越小，控制潜在变量的权重越大，生成结果越贴合输入几何（高保真度、可能降低真实感）。这构成了用户可调节的控制参数 $\tau_0$（或等价 $t_0$）的理论基础。

**超二次曲面参数方程**（Eq. 3）：作为空间控制的基础几何图元，正则超二次曲面的参数方程为：

$$s(\eta, \omega) = \begin{bmatrix} s_x \cos(\eta)^{\epsilon_1} \cos(\omega)^{\epsilon_2} \\ s_y \cos(\eta)^{\epsilon_1} \sin(\omega)^{\epsilon_2} \\ s_z \sin(\eta)^{\epsilon_1} \end{bmatrix}$$

其中 $s_x, s_y, s_z$ 控制各轴缩放，$\epsilon_1, \epsilon_2$ 控制形状的圆度/方度。该参数化允许用户通过少量参数快速构建3D草图，实现从粗略到精细的空间控制（见Figure 9）。

**局部-全局交叉注意力组合**（Appendix A.4）：在结构生成过程中，每个点的特征通过局部与全局语义条件的交叉注意力进行组合：

$$z_i \gets 0.5 \cdot \mathbf{CA}(z, c_{global,i}) + 0.5 \cdot \mathbf{CA}(z, c_{local,i})$$

该机制使模型能同时关注整体语义（如“椅子”）和局部几何约束，是实现文本-几何联合引导的关键。

## 实验与关键发现

### 主结果：几何保真度与真实感的量化对比

SpaceControl 在三个数据集上进行了全面的量化评估：Toys4K（玩具类）、Chair（椅子）和 Table（桌子），分别使用超二次曲面图元和完整多边形网格作为空间控制信号。评估指标包括 Chamfer 距离（CD↓，×10³，衡量几何保真度）、CLIP-I（↑，衡量文本一致性）、FID（↓，衡量纹理真实感）和 P-FID（↓，衡量几何真实感）。所有 SPACECONTROL 结果均基于 τ₀ = 6 的配置，但用户可根据需求自由选择该参数。

**Table 1** 的结果揭示了几个关键发现：

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_05343/figures/006_Table_1.jpg]]
*Table 1: Comparison with Baselines. We evaluate faithfulness to spatial and textual control via Chamfer Distance (CD, $\mathsf { \bar { \times } }$ 1 $0 ^ { 3 }$ ) and CLIP-I, and realism via FID (texture) and P-FID (geometry). Results for SPACE-CONTROL use $\tau _ { 0 }$ = 6 . † indicates methods fine-tuned on chair and table categories. Trellis (Xiang et al., 2025) (txt-DiT-XL) is included for reference only as it does not support spatial guidance

- **几何保真度的决定性优势**：在 Toys4K 数据集上，SPACECONTROL 使用超二次曲面图元时的 CD 为 **14.0**，使用网格时为 **4.89**，而基于训练的 Spice-E 方法 CD 高达 65.9，SPICE-E-T 为 39.1。在 Chair 数据集上，SPACECONTROL 的 CD 低至 **0.98**（图元）和 **0.66**（网格），相比 Spice-E 的 7.66 和 SPICE-E-T 的 6.54 有数量级的提升。Table 数据集呈现相同趋势：SPACECONTROL 的 CD 为 3.72（图元）和 0.48（网格），远优于 Spice-E 的 16.4 和 SPICE-E-T 的 26.1。

- **真实感指标的竞争力**：尽管 SPACECONTROL 在几何保真度上大幅领先，其 FID 和 P-FID 得分仍与基线保持可比水平。例如，Toys4K 网格条件下 SPACECONTROL 的 FID 为 244，P-FID 为 72.47，而 SPICE-E-T 分别为 199 和 74.6。这表明该方法并未以牺牲视觉质量为代价来换取几何对齐。

- **文本一致性的保持**：CLIP-I 指标在各方法间差异不大，SPACECONTROL 在 Toys4K 图元上为 0.32，网格上为 0.29，与 Spice-E 的 0.33 和 SPICE-E-T 的 0.31 接近，证明空间控制的引入并未损害文本条件的影响。

**Figure 5** 的定性对比进一步印证了量化结果：Spice-E 生成的收音机天线位置错误，SPICE-E-T 生成的小鸡身体部件解剖学位置不正确，而 SPACECONTROL 在真实感和几何忠实度之间取得了良好平衡。

### 控制强度 τ₀ 的消融分析

**Table 2** 和 **Figure 4** 系统分析了控制参数 τ₀ 的作用机制：

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_05343/figures/007_Table_2.jpg]]
*Table 2: Analysis of $\tau _ { 0 }$ . . We evaluate faithfulness to spatial and textual control via Chamfer Distance (CD, scaled by 1 $0 ^ { 3 }$ ) and CLIP-I, respectively. Realism is assessed via FID for texture and P-FID for geometry. Results are reported for spatial control provided as geometric primitives (P) and meshes (M). can see that by increasing the value of $\tau _ { 0 }$ and thus strength of the spatial conditioning, we obtain generations which align more closely to the input spatial control

- **单调的保真度提升**：随着 τ₀ 从 0 增加到 10，Chamfer 距离持续下降。在 Toys4K 图元条件下，CD 从 τ₀=0 时的 11775.4 骤降至 τ₀=4 时的 24.6，在 τ₀=10 时进一步降至 8.85。网格条件下趋势一致：τ₀=0 时 CD 为 11775.4，τ₀=10 时降至 3.50。

- **真实感-保真度权衡曲线**：Figure 4（左）展示了 CD 与 FID 的权衡关系。低 τ₀ 值（0-2）对应高 FID（低真实感）但 CD 也较高；τ₀ ∈ [4, 6] 提供了较好的折衷，在 Toys4K 上实现了较低的 CD 和可接受的 FID；过高的 τ₀（8-10）虽然进一步降低 CD，但 FID 开始回升，表明过度约束可能损害生成结果的真实感。

- **定性可视化**：Figure 4（右）以无纹理几何体的形式展示了不同 τ₀ 下的生成结果，直观呈现了从松散对齐到紧密贴合控制信号的渐变过程。

### 用户研究

**Figure 6** 报告了用户研究结果。在整体外观、空间控制忠实度和真实感三个维度上，SPACECONTROL 均获得了相对于 Spice-E 和 SPICE-E-T 的显著偏好。这一结果与定量指标一致，验证了该方法在人类主观评价中的优势。

### 图像条件与空间对齐分析

**Figure 7** 揭示了两个重要的机制特性：

- **图像条件的作用解耦**（Figure 7a）：图像条件主要影响生成资产的纹理外观，对几何结构的影响较小。这支持了跨模态纹理迁移的应用场景——用户可以使用一个空间控制信号定义形状，用另一张图像指定纹理风格。

- **精细空间对齐**（Figure 7b）：SPACECONTROL 能够与非轴对称的条件几何体精确对齐，同时保持网格质量。相比之下，Spice-E 和 SPICE-E-T 在相同条件下出现了明显的对齐偏差。Figure 10 进一步展示了不同 τ₀ 值下的对齐精度变化，高 τ₀ 值使生成结果几乎完美贴合输入控制几何。

### 失败模式与局限

- **预训练模型依赖性**：SPACECONTROL 的表现高度依赖预训练 Trellis 模型的能力。对于训练数据中未充分覆盖的类别，生成结果可能不够理想。这一局限源于方法本身无需训练的即插即用特性——它无法补偿基座模型在特定领域的生成能力不足。

- **τ₀ 的手动选择**：控制强度参数 τ₀ 需要用户手动设定，缺乏自动化的适应机制。Table 2 显示最优 τ₀ 值可能因数据集和条件类型而异（例如，图元条件在 Toys4K 上 τ₀=6 时 FID 为 221，而 τ₀=8 时为 228），用户需要通过试错找到适合特定任务的配置。

- **全局均匀控制**：当前方法对所有空间区域施加均匀的控制强度，无法实现局部区域的可变强度控制。这在需要部件感知精细编辑的场景中可能构成限制。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_05343/figures/010_Figure.jpg]]

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_05343/figures/011_Figure.jpg]]

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_05343/figures/013_Figure_9.jpg]]
*Figure 9: Coarse and fine-grained control with superquadrics. Superquadrics offer both fine-grained spatial control when used to sculpt precise geometry (motorbike, staircase, helicopter) and coarse control, when only used to draft a 3D sketch (duck, drumkit)*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

3D 资产生成领域长期受限于控制方式的粗糙性。现有方法主要依赖文本提示或单视图图像作为条件信号，存在两个根本性瓶颈：**文本的歧义性**使得用户无法精确描述几何形状（例如“一把现代椅子”无法指定靠背曲率和扶手位置）；**图像的不可编辑性**使得用户难以直接操纵对象的几何体。这一瓶颈导致生成结果与用户意图之间存在不可控的几何偏差，尤其在需要精确空间对齐的工业设计和游戏资产生成场景中尤为突出。

SpaceControl 的核心洞察在于：**将显式空间控制从训练阶段解耦，以测试时引导的方式注入预训练生成模型**。该方法不改变模型架构，不增加训练成本，仅通过操纵潜在空间中的噪声混合比例来实现几何保真度与视觉真实感之间的平滑权衡。

### 2. 与基线方法的关系谱系

#### 2.1 基于训练的 3D 条件生成方法

**Spice-E** 是直接可比的基于训练的方法，通过在 Shap-E 上微调来支持立方体图元作为几何条件。其核心局限在于：需要类别特定的微调，泛化能力受限；且微调过程改变了原始模型的生成分布，可能损害视觉质量。SpaceControl 在 Toys4K 数据集上以超二次曲面为条件时，Chamfer Distance（CD↓, ×10³）达到 **14.0**，而 Spice-E 为 **65.9**，几何保真度提升约 **78.8%**。

**SPICE-E-T** 是为公平对比在 Trellis 上复现的 Spice-E 训练版本。尽管共享相同的 Transformer 骨干（DiT-XL），其仍需类别特定微调，且 CD 为 39.1，仍显著劣于 SpaceControl 的 14.0。这表明即使模型能力相当，训练时条件注入的方式在几何对齐精度上存在内在劣势。

#### 2.2 基于测试时优化的引导方法

**Coin3D** 采用测试时优化策略，通过微调多视图生成模型来结合几何条件。该类方法需要在推理阶段进行迭代优化，计算开销大且可能陷入局部最优。SpaceControl 与之形成鲜明对比：无需任何优化步骤，仅通过单次前向传播即可完成空间控制，在效率上具有数量级优势。论文未提供与 Coin3D 的直接定量对比，但这一效率优势是测试时引导范式相对于测试时优化范式的结构性优势。

#### 2.3 无条件参考模型

**Trellis** (Xiang et al., CVPR 2025) 作为 SpaceControl 的骨干模型，本身不支持空间引导，仅接受文本或图像条件。SpaceControl 在 Trellis 的整流流（Rectified Flow）框架基础上，通过以下关键改造实现空间控制：

- **潜在空间注入**：将体素化的控制几何体通过预训练编码器 $E$ 映射为潜在变量 $\mathbf{z}_{c,0}$，在时间步 $t_0$ 处与噪声 $\mathbf{z}_1$ 混合：$\mathbf{z}_{t_0} = t_0 \mathbf{z}_1 + (1 - t_0) \mathbf{z}_{c,0}$。
- **控制强度调节**：通过参数 $\tau_0$（或等价 $t_0$）连续调节几何约束的强度，低 $\tau_0$ 趋向高真实感但低保真度，高 $\tau_0$ 更贴合输入几何但可能降低真实感。

### 3. 方法谱系中的定位

SpaceControl 在 3D 生成控制方法的谱系中占据独特位置：

| 范式 | 代表方法 | 控制方式 | 训练需求 | 几何精度 | 泛化能力 |
|------|----------|----------|----------|----------|----------|
| 训练时条件注入 | Spice-E, SPICE-E-T | 图元条件微调 | 需要类别特定微调 | 中等 | 受限 |
| 测试时优化引导 | Coin3D | 迭代优化 | 需要推理时优化 | 较高 | 中等 |
| **测试时潜在引导** | **SpaceControl** | **潜在空间噪声混合** | **完全无需训练** | **高** | **强** |

这一谱系表明，SpaceControl 代表了从“训练时条件注入”向“测试时即插即用引导”的范式转变。其核心优势在于：

1. **零训练成本**：完全复用预训练 Trellis 的编码器 $E$、结构流模型和解码器 $D$，无需任何微调。
2. **几何类型无关**：支持超二次曲面、多边形网格等多种几何表示，用户可根据需求选择粗略草图或精细网格。
3. **平滑可控性**：$\tau_0 \in [4, 6]$ 在 Toys4K 上提供了较好的几何保真度与真实感折衷（Table 2, Figure 4）。

### 4. 适用边界与局限性

尽管 SpaceControl 展现了强大的空间控制能力，其适用边界受限于以下因素：

**对预训练模型质量的依赖**：SpaceControl 的表现高度依赖 Trellis 骨干模型的生成能力。对于训练数据中未见的类别或复杂拓扑结构，生成结果可能不够理想。这一局限源于测试时引导方法的结构性约束——它只能引导已有生成能力向特定几何对齐，而无法创造模型原本无法生成的结构。

**控制强度的手动调节**：$\tau_0$ 需要用户手动选择，缺乏自动化的适应机制。Table 2 显示，$\tau_0$ 从 0 增加到 10 时，Toys4K 上的 CD 从 11775.4 降至 8.85，但 P-FID（几何真实感）可能随之恶化。最优 $\tau_0$ 因任务而异，用户需要在几何保真度与视觉质量之间进行经验性权衡。

**全局控制的粒度限制**：当前方法对整个生成对象施加统一的控制强度，无法对不同部件施加差异化约束。这在需要局部精细编辑的场景中（如仅调整椅子的扶手而不影响靠背）构成限制。

**图像条件的次要作用**：Figure 7a 的分析表明，图像条件主要影响纹理外观，对几何结构的影响较小。这意味着当用户希望通过图像同时控制几何和外观时，几何控制仍主要依赖显式空间信号。

### 5. 开放问题与未来方向

基于上述分析，以下开放问题值得进一步探索：

1. **自适应控制强度调度**：能否通过元学习或基于类别的先验知识，为 $\tau_0$ 提供自动调度策略？例如，对于结构简单的对象（如桌子）自动采用较低的 $\tau_0$，而对于复杂几何（如摩托车）采用较高的 $\tau_0$。

2. **局部可变强度控制**：全局空间控制机制是否能扩展为局部区域的可变强度控制？这需要解决如何将用户指定的部件级约束映射到潜在空间中的区域特定噪声混合策略。

3. **超二次曲面分解的优化**：不同的超二次曲面组合方式会如何影响生成质量？是否存在最优的图元分解策略，以最小化 Chamfer Distance 同时保持视觉真实感？

4. **跨模型泛化能力**：SpaceControl 的测试时引导范式是否能推广到其他 3D 生成架构（如基于扩散模型的框架）？这需要研究不同生成范式中潜在空间的结构特性。

5. **多模态控制的融合机制**：当同时提供文本、图像和空间控制时，如何优化不同模态信号的融合权重？当前方法采用固定策略，但自适应融合可能进一步提升生成质量。

## 原文 PDF

![[paperPDFs/ICLR_2026/SpaceControl_Introducing_Test_Time_Spatial_Control_to_3D_Generative_Modeling.pdf]]
