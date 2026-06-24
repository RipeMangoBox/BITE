---
title: "BulletTime: Decoupled Control of Time and Camera Pose for Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/BulletTime_Decoupled_Control_of_Time_and_Camera_Pose_for_Video_Generation.pdf
project_link: "https://19reborn.github.io/Bullet4D/"
code_link: null
aliases:
- BulletTime
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 解耦的世界时间序列和相机轨迹作为显式条件，通过连续时间旋转位置编码（Time-RoPE/4D-RoPE）注入注意力，并通过自适应层归一化（Time-AdaLN/Camera-AdaLN）在特征层进行调制，从而独立控制场景动态演化和视角移动。
primary_logic: 提出4D可控视频扩散框架，将视频时间分解为连续世界时间与相机姿态，利用统一4D旋转位置编码和双分支自适应层归一化实现时间与相机的解耦控制；同时构建了一个时序变化与相机变化相互独立的合成数据集，使模型能够学习解耦的4D生成。
claims:
- 在合成数据集上，本方法像素精度全面超越基线，PSNR达24.57，比ReCamMaster高2.71 dB。
- 在真实视频上，本方法同时获得最低的旋转误差（1.47）和平移误差（1.32），且时间闪烁、运动平滑度、主体一致性等VBench指标均优于基线。
- 消融实验证实Time-RoPE + AdaLN组合在所有世界时间条件方法中效果最佳（PSNR 32.15），且移除4D-RoPE导致PSNR大幅下降（23.45→21.98）。
- Synthetic dataset (PointOdyssey) 上 PSNR = 24.57
---

# BulletTime: Decoupled Control of Time and Camera Pose for Video Generation

> [!tip] 核心洞察
> 提出4D可控视频扩散框架，将视频时间分解为连续世界时间与相机姿态，利用统一4D旋转位置编码和双分支自适应层归一化实现时间与相机的解耦控制；同时构建了一个时序变化与相机变化相互独立的合成数据集，使模型能够学习解耦的4D生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | BulletTime：视频生成中世界时间与相机姿态的解耦控制 |
| 英文题名 | BulletTime: Decoupled Control of Time and Camera Pose for Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.05076) · [Project](https://19reborn.github.io/Bullet4D/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | BulletTime |
| Dataset | Synthetic dataset, Real-World Videos |

> [!tip] 效果简介
> - Synthetic dataset (PointOdyssey) 上，PSNR 24.57 vs ReCamMaster* 21.86 (+2.71)；SSIM 0.6905 vs ReCamMaster* 0.5852 (+0.1053)；LPIPS 0.1265 vs ReCamMaster* 0.1846 (-0.0581)。
> - Real-World Videos (ViPE, camera accuracy) 上，Rotation Error (RotErr) 1.47 vs ReCamMaster* 2.98 (-1.51)；Translation Error (TransErr) 1.32 vs ReCamMaster* 1.85 (-0.53)。
> - Real-World Videos (VBench) 上，Temporal Flickering 0.9780 vs ReCamMaster* 0.9755 (+0.0025)。

## 概述

现有视频扩散模型将场景动态与相机运动耦合在单一视频时间轴上，用户无法独立控制“世界时间”（场景自身的动态演进）和相机视角。这一耦合限制了精确的时空操纵与4D世界建模，例如无法在保持场景动态不变的前提下自由改变拍摄角度，也无法在固定视角下独立控制场景的时间流速。

针对这一瓶颈，本文提出 **BulletTime**——一个4D可控视频扩散框架，将视频时间显式分解为连续世界时间序列与相机轨迹两个正交条件。核心因果机制在于：通过连续时间旋转位置编码（Time-RoPE）和统一4D旋转位置编码（4D-RoPE）将时间与相机几何信息注入注意力层，同时通过双分支自适应层归一化（Time-AdaLN / Camera-AdaLN）在特征层进行调制，从而实现时间与相机的解耦控制。为提供解耦的监督信号，作者构建了一个时序变化与相机变化相互独立的合成数据集。

在合成数据集（PointOdyssey）上，BulletTime 的 PSNR 达到 24.57 dB，比经过同数据集微调的 **ReCamMaster*** 高出 2.71 dB，SSIM 和 LPIPS 也全面领先（Table 1）。在真实视频上，本方法同时获得最低的相机旋转误差（1.47）和平移误差（1.32），且在 VBench 指标上——包括时间闪烁、运动平滑度和主体一致性——均优于基线（Table 2）。消融实验证实，Time-RoPE + AdaLN 组合在所有时间条件方法中效果最优（PSNR 32.15），而移除 4D-RoPE 导致 PSNR 大幅下降（23.45 → 21.98），表明统一4D位置编码对解耦控制至关重要（Table 4–5）。

在方法谱系上，BulletTime 以预训练 **CogVideoX-5B-T2V** 为主干，与仅支持相机控制的 **TrajectoryCrafter***（Mark YU et al., arXiv 2025）和 **ReCamMaster*** 形成对比——后者需通过时间重映射才能扩展至4D控制，且解耦能力显著弱于本方法。在相同相机路径、不同时间控制下，BulletTime 的背景一致性 mPSNR 达 28.29，远优于 ReCamMaster 的 25.80（Table 3），验证了其更强的解耦能力。

本方法仍存在若干局限：对细腻手部动作的生成不佳；输入视频中不可见背景区域缺乏高保真细节；继承自 CogVideoX 的极端视角泛化限制；以及以人物为中心的训练数据使模型在动物、自然场景等未见环境上可能产生次优纹理。

## 背景与动机

视频生成领域近年来取得了显著进展，但现有方法在精确的时空操纵能力上仍存在根本性瓶颈。当前主流的视频扩散模型将场景动态演化与相机运动耦合在单一的视频时间轴上——每一帧既编码了“世界在哪个时刻”的信息，又编码了“从哪个角度观察”的信息。这种纠缠使得用户无法独立控制场景的时间流逝速度和相机的空间运动轨迹，严重限制了视频生成在4D内容创作、电影级特效制作等场景中的应用潜力。

具体而言，现有相机控制视频生成模型（如**TrajectoryCrafter** (Mark YU et al., arXiv 2025)、**ReCamMaster**等）虽然能够根据给定的相机轨迹生成新视角视频，但它们假设输入视频具有固定的均匀时间采样，无法改变场景内部的动态节奏。当用户希望实现“子弹时间”效果——即相机快速环绕运动的同时场景时间减速或冻结——这些方法便暴露出根本性的控制缺失。即便通过时间重映射（time remapping）对输入视频进行预处理来间接扩展这些基线方法，由于缺乏对世界时间的显式建模，生成结果往往出现几何不一致、运动伪影和相机控制失准等问题。

从技术层面审视，这一瓶颈的根源在于两个关键设计缺陷：**第一**，现有视频扩散模型中的位置编码（如标准3D RoPE）基于离散帧索引，无法表达连续的世界时间概念，使得模型难以理解“两帧之间究竟流逝了多少物理时间”；**第二**，缺乏专门的时间调制机制，导致时间控制信号无法以精细化的方式注入生成过程，相机控制与时间控制之间也没有建立联合的4D几何关系。

针对上述问题，本文提出**BulletTime**——一个4D可控的视频扩散框架，其核心动机是将视频生成重新形式化为两个显式且正交的条件信号：**连续世界时间序列**和**相机姿态轨迹**。通过将视频时间轴分解为“世界时间”与“相机时间”两个独立维度，框架能够在注意力机制中注入统一的时间-相机4D位置编码，并在特征层面通过双分支自适应层归一化实现解耦调制，从而首次赋予视频扩散模型独立操纵场景动态与相机视角的能力。

## 核心创新

BulletTime 的核心创新在于将视频生成从单一时间轴解放出来，构建了一个**4D可控视频扩散框架**，首次实现世界时间与相机姿态的显式解耦控制。这一解耦通过三个层面的机制创新实现：

### 1. 连续世界时间控制：Time-RoPE 与 Time-AdaLN

传统视频扩散模型使用标准RoPE对离散帧索引编码，将场景动态与相机运动耦合在统一的视频时间轴上。BulletTime 提出**Time-RoPE**，将旋转位置编码从离散帧索引推广到连续世界时间 $\tau$，使注意力分数仅依赖两帧之间的世界时间差：

$$Q_i^{\mathrm{Time}}(K_j^{\mathrm{Time}})^{\top}=Q_i^{\top}{\bf D}^{\mathrm{Time}}(\tau_i-\tau_j)K_j$$

这一设计将时间控制先验直接注入注意力logits，无需引入额外可学习参数。与之互补的是**Time-AdaLN**，通过自适应层归一化在特征层注入连续时间信号：

$$\tilde{z}_{i,n}'=\mathrm{LN}(\tilde{z}_{i,n})\odot f_{\gamma}(f_{\mathrm{time}}(\tau_i))+f_{\beta}(f_{\mathrm{time}}(\tau_i))$$

AdaLN 的选择基于一个关键洞察：世界时间是一个平滑的全局标量，影响整个场景的动态演化，而非局部空间区域，因此特征级的全局调制比Cross-Attention或Channel Addition等空间局部化方法更适配时间控制任务。

### 2. 统一4D时空位置编码：4D-RoPE

为实现时间与相机的联合解耦控制，BulletTime 在 Time-RoPE 基础上引入相机感知的几何分量，构建**4D-RoPE**——一种融合连续时间差与视角依赖几何关系的统一4D旋转位置编码。4D-RoPE 将时间与相机几何信息同时注入注意力机制，使模型能够区分“场景自身变化”与“观察者移动”这两种不同的视觉变化来源。

### 3. 双分支自适应调制：Camera-AdaLN

与 Time-AdaLN 并行，**Camera-AdaLN** 作为独立的相机姿态调制分支，根据目标相机轨迹调制中间激活特征。这种双分支设计使得时间调制和相机调制在特征空间相互正交，从根本上保障了解耦控制的实现。

### 与基线方法的本质差异

相较于 **TrajectoryCrafter** 和 **ReCamMaster** 等仅支持相机控制的基线方法，BulletTime 的改变槽位（changed slots）体现了方法论层面的根本差异：

| 机制槽位 | 基线方法 | BulletTime |
|---------|---------|------------|
| 时间位置编码 | 标准RoPE（离散帧索引） | Time-RoPE（连续世界时间） |
| 时间调制模块 | 无显式时间调制 | Time-AdaLN（时间条件自适应层归一化） |
| 相机位置编码 | 无显式相机位置编码 | 4D-RoPE（融合时间与相机几何的统一编码） |
| 相机调制模块 | 无显式相机调制 | Camera-AdaLN（相机条件自适应层归一化） |

基线方法仅通过时间重映射（time remapping）扩展至4D控制，缺乏对时间维度的原生建模能力。消融实验证实：Time-RoPE + AdaLN 组合在所有世界时间条件方法中PSNR达32.15，显著优于仅使用AdaLN（29.83）或Cross-Attention（23.86）的变体；移除4D-RoPE导致PSNR从23.45骤降至21.98，降幅1.47 dB，验证了统一4D位置编码对联合时空控制的关键作用。

## 整体框架

BulletTime 构建了一个4D可控视频扩散框架，其核心设计是将传统视频生成中耦合在单一时间轴上的场景动态与相机运动显式解耦，分离为两个正交的控制信号：**连续世界时间序列** $\tau_{\text{world}}$ 与**相机姿态轨迹** $c$。这两个信号通过互补的调制通路注入预训练的 Diffusion Transformer 主干，实现对场景动态演化和视角移动的独立操纵。

**主干模型**基于 CogVideoX-5B-T2V 预训练权重初始化，利用其强大的文本到视频生成先验作为基础生成能力。在此基础上，框架引入两条并行的条件注入支路，分别负责时间控制和相机控制，最终在注意力层融合为统一的4D位置编码。

**输入输出流**如下：给定一段条件输入视频（其相机运动与均匀时间采样相互纠缠），模型接收目标世界时间序列和相机轨迹作为显式条件，生成一段新视频，该视频忠实地遵循指定的时间节奏和相机路径，同时保持场景内容的一致性。

**时间控制支路**包含两个组件：
- **Time-RoPE**（连续时间旋转位置编码）：将标准RoPE从离散帧索引扩展至连续时间域，直接在注意力机制中注入世界时间差 $\tau_i - \tau_j$，使注意力分数仅依赖于两帧之间的时间偏移，无需引入额外可学习参数。
- **Time-AdaLN**（时间自适应层归一化）：通过MLP将连续时间信号映射为缩放因子 $f_\gamma$ 和偏置 $f_\beta$，在特征层级对每一帧进行精细化调制，公式为 $\tilde{z}_{i,n}' = \mathrm{LN}(\tilde{z}_{i,n}) \odot f_\gamma(f_{\mathrm{time}}(\tau_i)) + f_\beta(f_{\mathrm{time}}(\tau_i))$。AdaLN 之所以被选为时间调制方式，是因为世界时间是一个平滑的全局标量，影响整个场景的动态而非局部空间区域。

**相机控制支路**同样包含两个组件：
- **4D-RoPE**：在 Time-RoPE 的基础上融入相机感知的几何分量，将时间差与视角相关的几何关系联合编码为统一的4D旋转位置编码，直接注入注意力机制，实现时间与相机的联合控制。
- **Camera-AdaLN**：与 Time-AdaLN 并行的自适应层归一化分支，根据目标相机轨迹调制中间层激活值。

**训练数据**方面，作者构建了一个4D控制合成数据集，其关键特性是每个场景内包含多样化的时间变化与空间变化，且二者相互独立。这一设计为模型学习解耦的4D生成提供了必要的监督信号——模型必须同时准确跟随时间条件和相机条件，而非将二者混为一谈。

整体框架的模块关系如 Figure 2 所示：输入视频经VAE编码后进入 Diffusion Transformer，在每一层中，时间信号通过 Time-RoPE 和 Time-AdaLN 注入，相机信号通过 4D-RoPE 和 Camera-AdaLN 注入，两条通路在注意力计算中融合，最终由解码器输出符合4D控制条件的目标视频。

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. Given a conditional input video, our diffusion model generates new videos under 4D control using world time and camera trajectory. These two signals are injected into the Diffusion Transformer through complementary modulation pathways. Time control is enabled by*

## 核心模块与公式推导

BulletTime 的核心设计在于将世界时间与相机姿态作为两个正交的控制信号，通过互补的调制通路注入到预训练的 Diffusion Transformer 中。其架构建立在 **CogVideoX-5B-T2V** 预训练模型之上，包含三个关键模块：连续世界时间控制、统一4D时空位置编码、以及相机姿态调制。

### 连续世界时间控制：Time-RoPE 与 Time-AdaLN

传统视频扩散模型使用离散帧索引的位置编码，将场景动态与帧率耦合。BulletTime 引入 **Time-RoPE**（连续时间旋转位置编码），将 RoPE 扩展为直接作用于连续世界时间 τ 的形式。

对于注意力机制中的查询 Q 和键 K，标准缩放点积注意力为：

$$\mathrm{Attn}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d}}\right)V$$

Time-RoPE 定义了一个块对角旋转矩阵，将连续世界时间 τ 注入到注意力计算中：

$$\mathbf{D}^{\mathrm{Time}}(\tau) = \mathrm{diag}\big(\mathbf{R}(\tau\theta_1), \mathbf{R}(\tau\theta_2), \dots, \mathbf{R}(\tau\theta_{d'/2})\big)$$

其中 $\mathbf{R}(\tau\theta)$ 是二维旋转矩阵，$\theta$ 为频率参数。对待查帧 i 和要查帧 j 的查询与键分别施加时间依赖旋转：

$$Q_i^{\mathrm{Time}} = (\mathbf{D}^{\mathrm{Time}}(\tau_i))^{\top} Q_i, \quad K_j^{\mathrm{Time}} = (\mathbf{D}^{\mathrm{Time}}(\tau_j))^{\top} K_j$$

旋转后，注意力分数仅依赖于两帧的世界时间差 $(\tau_i - \tau_j)$：

$$Q_i^{\mathrm{Time}}(K_j^{\mathrm{Time}})^{\top} = Q_i^{\top}\mathbf{D}^{\mathrm{Time}}(\tau_i - \tau_j)K_j$$

这一设计的核心优势在于：① 无需引入额外可学习参数，直接将时间控制先验注入注意力 logit；② 连续时间编码使模型能够泛化到训练时未见过的帧率与时间重映射模式。

与 Time-RoPE 互补，**Time-AdaLN** 在特征层面进行逐帧时间调制。世界时间 τ 经过 MLP $f_{\mathrm{time}}$ 编码后，通过自适应层归一化的缩放与偏移参数注入：

$$\tilde{z}_{i,n}' = \mathrm{LN}(\tilde{z}_{i,n}) \odot f_{\gamma}(f_{\mathrm{time}}(\tau_i)) + f_{\beta}(f_{\mathrm{time}}(\tau_i))$$

其中 $\tilde{z}_{i,n}$ 为第 i 帧第 n 层的中间特征，$f_{\gamma}$ 和 $f_{\beta}$ 分别为缩放与偏移的线性投影。选择 AdaLN 而非 Cross-Attention 或 Channel Addition 的理由在于：世界时间是一个平滑的全局标量，影响整个场景的动力学而非局部空间区域，AdaLN 的特征级全局调制天然适合这一特性。消融实验证实了这一点——Time-RoPE + AdaLN 组合在 PSNR 上达到 32.15，显著优于 RoPE + CrossAttention（23.86）和 RoPE + Channel Addition（25.31）。

### 统一4D时空位置编码：4D-RoPE

为实现世界时间与相机姿态的联合解耦控制，BulletTime 将 Time-RoPE 扩展为 **4D-RoPE**——一个融合时间几何与相机几何的统一位置编码。

4D-RoPE 的核心思想是：在注意力机制中同时注入连续时间差和视角依赖的几何关系。当相机姿态发生变化时，同一空间点的投影位置在不同帧之间产生位移，4D-RoPE 通过相机感知的几何分量来建模这种对应关系，使注意力机制能够同时感知“何时”和“从哪看”两个维度。

### 相机姿态调制：Camera-AdaLN

与 Time-AdaLN 并行，**Camera-AdaLN** 引入独立的 AdaLN 分支用于相机姿态调制。相机轨迹被编码后，通过缩放与偏移参数调制中间层特征，使生成过程遵循目标相机运动。这一双分支设计（Time-AdaLN + Camera-AdaLN）使得时间和相机控制通路相互独立，是实现解耦控制的关键结构。

消融实验（Table 5）验证了各组件的必要性：完整模型的 PSNR 为 23.45，移除 4D-RoPE 后骤降至 21.98（降幅 1.47 dB），移除 Camera/Time AdaLN 后降至 22.74。4D-RoPE 的降幅最大，表明统一的时空位置编码对 4D 联合控制至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/001_Figure_1.jpg]]
*Figure 1: Time- and camera-controlled 4D video generation. Given a single input video where camera motion is entangled with uniform temporal sampling (top row), our method synthesizes new videos that enable decoupled control over world time and camera pose*

## 实验与分析

### 核心瓶颈与因果机制

现有视频扩散模型将场景动态演化与相机运动耦合在单一视频时间轴上，导致无法独立操纵“世界时间”（场景内物体自身的运动进度）与相机视角。**BulletTime** 针对这一瓶颈，引入两个正交控制信号——连续世界时间序列与相机轨迹——并通过双分支调制通路显式解耦：**Time-RoPE** 将连续时间差直接注入注意力 logit，**Camera-AdaLN** 在特征层对相机姿态进行自适应缩放与偏移。这一设计使模型能够独立控制“子弹时间”等经典影视效果中的时间流速与视角移动，而无需重新训练或事后插值。

### 合成数据集上的像素级精度

在 PointOdyssey 合成数据集上，BulletTime 在所有像素级指标上均显著超越基线方法（Table 1）。PSNR 达 **24.57**，比经过同一 4D 数据集微调的 **ReCamMaster\*** 高出 **2.71 dB**（21.86），比 **TrajectoryCrafter\*** 高出 **6.85 dB**（17.72）。结构相似性 SSIM 为 **0.6905**，较 ReCamMaster\* 的 0.5852 提升 0.1053；感知损失 LPIPS 降至 **0.1265**，远低于 ReCamMaster\* 的 0.1846。这一差距的核心成因在于：TrajectoryCrafter\* 依赖单目深度估计构建动态点云，不准确的深度估计常导致几何扭曲与相机控制失准；ReCamMaster\* 虽经微调后性能大幅提升（PSNR 从 19.67 升至 21.86），但因其缺乏显式的世界时间建模，仍无法在时间重映射场景下保持像素级精度。

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/004_Table_1.jpg]]
*Table 1: Comparison of Camera- and Time-Controlled Video Generation on the Synthetic Dataset. Baseline methods designed solely for camera control (denoted with *) are extended to 4D control by applying time remapping [33] to the input videos prior to camera-conditioned generation. Our approach attains the highest pixel-level accuracy across all metrics, demonstrating its effectiveness in jointly modeling camera and temporal control*

> **公平性说明**：为公平比较，作者在本文构建的 4D 控制数据集上对 ReCamMaster 进行了微调；TrajectoryCrafter 的劣势源于其单目深度估计的固有局限，并非有意削弱。

### 真实视频上的相机控制精度与时序质量

在真实视频基准 ViPE 上，BulletTime 同时取得最低的旋转误差 **RotErr = 1.47**（ReCamMaster\* 2.98，TrajectoryCrafter\* 5.44）和平移误差 **TransErr = 1.32**（ReCamMaster\* 1.85，TrajectoryCrafter\* 3.31）（Table 2）。这表明 4D-RoPE 联合编码时间与相机几何关系的方式，比单纯依赖时间重映射的扩展策略更精确地保留了目标相机轨迹。

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/005_Table_2.jpg]]
*Table 2: Comparison of Camera- and Time-Controlled Video Generation on Real-World Videos. Our method achieves the most accurate camera pose control and produces videos with reduced temporal flicker, smoother motion, and higher subject–background consistency, indicating stronger 4D controllability while maintaining high visual quality*

在 VBench 视频质量指标上，BulletTime 同样表现最优：时间闪烁 **0.9780**（ReCamMaster\* 0.9755）、运动平滑度 **0.9923**（ReCamMaster\* 0.9911）、主体一致性 **0.9428**（ReCamMaster\* 0.9375）。这些指标的提升幅度虽小但一致，说明解耦控制不仅提升了相机精度，也间接改善了生成视频的时序稳定性——当相机轨迹偏离时，基线方法往往产生几何不一致的闪烁伪影，而 BulletTime 的独立时间调制通路（Time-AdaLN）保持了帧间动态的平滑过渡。

### 解耦效果的定量验证

解耦能力的核心检验来自 Table 3：在相同相机轨迹、不同世界时间控制下，测量背景区域的一致性。BulletTime 的掩码 PSNR（mPSNR）达 **28.29**，显著高于 ReCamMaster\* 的 25.80（+2.49 dB）；mSSIM 为 **0.9096**（ReCamMaster\* 0.8789），mLPIPS 为 **0.1119**（ReCamMaster\* 0.1527）。这一结果表明，ReCamMaster\* 在改变时间条件时无法维持一致的相机控制，背景区域出现几何漂移；而 BulletTime 的双分支 AdaLN 设计使相机调制独立于时间信号，从而在时间变化时保持视角稳定。

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/009_Table_3.jpg]]
*Table 3: Evaluation of Disentangled Camera and Time Control. Background consistency is measured between videos generated under identical camera trajectories but different time controls using masked image metrics [19] (mPSNR, mMAE, mSSIM, mLPIPS), where the prefix “m” indicates evaluation within the masked background region. Our method achieves higher consistency than ReCamMaster, indicating more effective disentanglement and improved 4D coherence*

### 消融实验：时间调制机制

Table 4 系统比较了不同世界时间条件注入方式的性能。在仅进行时间控制（无相机变化）的设置下：

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/010_Table_4.jpg]]
*Table 4: Ablation on World-Time Conditioning. We compare different temporal conditioning mechanisms for fine-tuning CogVideoX [78] toward world-time-controlled video-to-video generation. AdaLN provides the strongest performance among the learnable baselines (CrossAttention and ChannelAddition). Time-RoPE itself offers strong controllability and consistently improves upon standard RoPE across all configurations, with Time-RoPE + AdaLN achieving the best overall results*

- **Time-RoPE + AdaLN** 组合取得最优 PSNR **32.15**（SSIM 0.8962，LPIPS 0.0631）。
- 将 Time-RoPE 替换为标准 RoPE 后，PSNR 降至 29.83（-2.32 dB），证明连续时间编码优于离散帧索引编码。
- 仅使用 Time-RoPE 而无 AdaLN 时，PSNR 为 30.45（-1.70 dB），说明特征级调制提供了互补的时间控制能力。
- AdaLN 在所有可学习基线中表现最强：RoPE+AdaLN（29.83）远优于 RoPE+CrossAttention（23.86）和 RoPE+ChannelAddition（25.31）。

这一消融揭示了关键设计原则：**Time-RoPE 在注意力层注入时间差先验，AdaLN 在特征层提供逐帧精细调制，二者互补而非冗余**。AdaLN 之所以优于 Cross-Attention，是因为世界时间是平滑的全局标量，影响整个场景的动态而非局部空间区域，逐通道的缩放-偏移操作比交叉注意力更适配这一特性。

### 消融实验：4D 联合控制

Table 5 评估了完整 4D 控制框架中各组件的贡献。完整模型 PSNR 为 **23.45**；移除 **4D-RoPE** 后 PSNR 骤降至 **21.98**（-1.47 dB），这是所有消融中降幅最大的操作，表明统一的时空旋转位置编码对联合控制至关重要。移除 Camera/Time AdaLN 后 PSNR 降至 22.74（-0.71 dB），降幅较小但仍显著，说明 AdaLN 分支在 4D 场景下同样提供有效调制。

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/012_Table_5.jpg]]
*Table 5: Ablation on 4D Conditioning. Our 4D-RoPE and Time/Camera AdaLN enhance 4D conditioning scores*

4D-RoPE 的核心价值在于：它将时间差旋转与相机几何旋转统一在同一注意力 logit 中，使模型能够学习“在特定世界时间、从特定视角观察”的联合表示。移除后，模型退化为两个独立调制通路的简单组合，无法捕捉时间与视角的交互效应。

### 失败模式与局限性

尽管 BulletTime 在定量指标上全面领先，论文明确指出了以下失败模式：

1. **细腻手部动作生成不佳**：在特定视角下，手部运动可能违反物理合理性或显得低质量。这源于训练数据以人物为中心但缺乏足够的手部精细标注。
2. **不可见区域的细节缺失**：输入视频中未出现的背景区域（如被遮挡或超出原视角的部分）缺乏高保真细节，因为训练数据仅限于合成环境，模型未见过真实世界的大基线遮挡补全。
3. **预训练模型的泛化瓶颈**：继承自 CogVideoX-5B-T2V 的生成限制，对极端视角（如完全背向原视频的视角）的泛化能力有限。
4. **场景类型的分布外退化**：数据集以人物为中心，对动物、自然场景等未见环境虽能泛化，但可能产生次优纹理。

### 开放问题

论文提出的开放方向包括：如何捕获真实世界物理、光照和大基线相机运动下的完整长期场景动态；如何设计自回归或循环结构以实现无界长视频生成和在线轨迹控制；如何结合真实视频数据学习解耦，提高对现实开放场景的泛化能力；以及如何将框架扩展以支持物理感知的时间推理与场景理解。这些问题指向一个共同目标：从“合成数据上的解耦控制”走向“开放世界的物理一致 4D 生成”。

### 补充图表

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/003_Figure_3.jpg]]
*Figure 3: Comparison on Synthetic Videos. GT frames compared with predictions from our method and state-of-the-art novelview synthesis models. Our method adheres most closely to the target camera conditions and produces the finest level of detail*

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Comparison of Camera- and Time-Controlled Video Generation on Real-World Videos. Qualitative comparison between our method and state-of-the-art novel-view synthesis models extended with time remapping [33]. In the left example, existing methods struggle under extreme view and time changes, producing severe artifacts (ReCamMaster) and showing imprecise camera control (TrajectoryCrafter). The right example similarly illustrates strong artifacts and reduced detail from ReCamMaster, while TrajectoryCrafter again fails to follow the prescribed trajectory*

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/007_Figure_5.jpg]]
*Figure 5: 4D Control: Camera and Time Manipulation. Our model generates videos that faithfully follow independently specified camera and time controls. Each row shows combinations of fixed or moving camera viewpoints () and fixed or changing world time (7). The model correctly applies each control mode, including challenging settings such as moving camera with fixed time (bullet time effect), while preserving scene dynamics and visual coherence. These results indicate strong disentanglement between camera and world time conditioning as well as robust generalization across diverse real world inputs*

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/011_Figure_7.jpg]]
*Figure 7: Comparison of Camera–Time Disentanglement. When varying the time condition while keeping the camera condition fixed, state-of-the-art camera-controlled video generation methods such as ReCamMaster fail to maintain consistent camera control, resulting in geometric inconsistencies within the generated content*

![[assets/figures/papers/paper_list_l2444_https_arxiv_org_abs_2512_05076/figures/008_Figure_6.jpg]]
*Figure 6: Time Control Generalization. Three generations produced by our method from the same input video under different time conditions. Although the model is trained on only a limited subset of time remappings, it generalizes well to complex and previously unseen temporal inputs*

## 方法谱系与知识库定位

### 1. 问题定位：从耦合到解耦的4D生成

现有视频扩散模型的核心瓶颈在于，场景动态演化（世界时间）与相机运动被耦合在单一的“视频时间轴”上。无论是基于文本的视频生成模型（如CogVideoX），还是相机可控的视频生成方法，其时间维度本质上对应的是帧索引的离散序列，无法区分“场景自身的变化”与“观察视角的变化”。这导致两个关键局限：（1）无法独立控制世界时间和相机姿态，限制了精确的时空操纵；（2）难以从单段耦合视频中恢复出完整的4D世界表示。

BulletTime的核心洞察在于将视频生成重新形式化为一个4D可控问题：引入两个显式且正交的条件信号——连续世界时间 $\tau_{\mathrm{world}}$ 和相机姿态 $c$，共同定义一个可控的4D坐标系。这一形式化使得模型能够学习从“观察到的耦合视频”到“解耦的4D世界”的映射，从而支持任意世界时间与相机轨迹的组合生成。

### 2. 方法谱系：与基线工作的关系

BulletTime构建在预训练视频扩散模型CogVideoX-5B-T2V之上，但与现有相机可控视频生成方法存在本质差异。

**与相机控制方法的对比。** 当前最先进的相机可控视频生成模型，如**ReCamMaster**和**TrajectoryCrafter**（Mark YU et al., arXiv 2025），仅支持对相机姿态的控制，其时间轴仍与输入视频的帧序列绑定。为进行公平比较，BulletTime对这两种基线方法进行了扩展：通过时间重映射（time remapping）技术，将输入视频重新采样以匹配目标世界时间条件，再输入到相机控制模型中。这一扩展使得基线方法在形式上能够处理4D控制任务，但其内在的时间-相机耦合机制并未改变。

实验结果表明，即使经过在BulletTime的4D控制数据集上微调，ReCamMaster的PSNR从19.67提升至21.86，仍显著落后于BulletTime的24.57（+2.71 dB）。这一定量差距揭示了时间重映射这种“外挂式”扩展的根本局限：它无法在模型内部建立时间与相机的解耦表示。TrajectoryCrafter的劣势更为明显（PSNR仅17.72），其依赖单目深度估计构建动态点云的策略在深度不准确时会导致几何扭曲和相机控制失准，这是该方法固有的结构性问题。

**方法差异的本质。** BulletTime与基线方法的核心差异不在于模型规模或训练数据，而在于条件注入机制的设计哲学：

| 机制维度 | 基线方法（ReCamMaster等） | BulletTime |
|---------|------------------------|-----------|
| 时间表示 | 离散帧索引（通过时间重映射间接控制） | 连续世界时间 $\tau$，通过Time-RoPE直接注入注意力 |
| 时间调制 | 无显式时间调制模块 | Time-AdaLN：特征级自适应层归一化 |
| 相机位置编码 | Plücker坐标或射线编码 | 4D-RoPE：融合时间差与相机几何关系的统一旋转位置编码 |
| 相机调制 | 通常通过交叉注意力或拼接 | Camera-AdaLN：与Time-AdaLN并行的双分支调制 |
| 时间-相机关系 | 耦合在单一视频时间轴上 | 解耦：两个独立条件信号，通过统一4D编码协同工作 |

这种设计差异的根源在于BulletTime对“时间”的重新定义。标准RoPE基于离散帧索引计算位置编码，而Time-RoPE直接操作于连续世界时间，使得注意力分数仅依赖于两帧之间的世界时间差 $\tau_i - \tau_j$。这一性质使得模型能够自然地处理任意时间间隔的帧关系，而无需依赖固定的帧率假设。

### 3. 适用边界与条件依赖

BulletTime的有效性高度依赖于其训练数据的设计。该方法构建了一个专门的4D控制合成数据集，其核心特征是：每个场景内包含多样化的时间变化（场景动态）和空间变化（相机视角），且两者相互独立。这一数据设计提供了必要的监督信号，使模型能够学习解耦的4D生成。数据集以人物为中心，基于PointOdyssey等合成环境构建。

这一数据依赖定义了BulletTime的适用边界：

- **优势场景**：人物为中心的视频，相机运动与场景动态需要独立控制的场景（如子弹时间效果、视角旋转同时保持/改变场景时间），合成环境或可控真实场景。
- **泛化边界**：对于训练分布之外的未见环境（如动物、自然场景），模型虽能泛化，但可能产生次优纹理。输入视频中不可见的背景区域缺乏高保真细节，因为训练数据仅限于合成环境。
- **继承限制**：作为基于CogVideoX的微调模型，BulletTime继承了预训练模型的生成限制，包括对极端视角的泛化能力有限。

### 4. 局限与已知失效模式

根据论文中明确报告的局限性，BulletTime存在以下已知问题：

1. **细粒度运动生成不足**：在某些视角下，细腻的手部动作生成质量不佳，运动可能违反物理合理性或显得低质量。这表明模型在局部动态建模上仍有改进空间。

2. **不可见区域的保真度受限**：输入视频中未观察到的背景区域缺乏高保真细节。这是单目视频到4D生成的固有挑战——模型需要“想象”未见过区域的内容，而当前训练数据（合成环境）的多样性不足以支撑高质量的补全。

3. **继承自预训练模型的限制**：对极端视角的泛化有限，这是CogVideoX本身的能力边界。

4. **数据分布限制**：训练数据以人物为中心，对非人物场景的纹理生成可能次优。

### 5. 开放问题与未来方向

论文明确提出了四个开放问题，代表了该方向的关键挑战：

1. **真实世界物理与长期动态捕获**：如何捕获真实世界物理、光照和大基线相机运动下的完整长期场景动态？当前方法在合成数据上训练，缺乏对真实物理约束（如遮挡、光照变化、非刚性变形）的建模。

2. **无界长视频生成与在线控制**：如何设计自回归或循环结构以实现无界长视频生成和在线轨迹控制？当前框架生成固定长度的视频，无法支持流式或交互式的4D操控。

3. **真实视频数据学习**：如何结合真实视频数据学习解耦，提高对现实开放场景的泛化能力？真实视频中时间与相机天然耦合，如何从中提取解耦的监督信号是一个开放挑战。

4. **物理感知的时间推理**：如何将框架扩展以支持物理感知的时间推理和场景理解？当前方法主要依赖数据驱动的时间模式学习，缺乏对物理因果关系的显式建模。

### 6. 知识库定位

BulletTime在视频生成领域的知识谱系中占据以下位置：

- **上游依赖**：CogVideoX（视频扩散模型主干）、RoPE（旋转位置编码，Su et al.）、AdaLN（自适应层归一化，源自DiT等架构）、PointOdyssey（合成数据环境）。
- **横向对比**：与ReCamMaster、TrajectoryCrafter等相机可控方法形成直接对比，核心区分点在于时间-相机解耦的架构设计。
- **下游拓展潜力**：可向4D场景重建、自由视点视频生成、物理感知的动态场景建模等方向延伸。其解耦框架为未来结合3D Gaussian Splatting等显式4D表示提供了自然的接口。

**证据强度评估**：本文的核心主张（解耦控制、性能优势）有充分的定量实验支撑（Table 1-5，消融实验），证据置信度高。局限性和开放问题的讨论诚实且具体。需要注意的是，该方法在真实世界复杂场景下的泛化能力尚未经过大规模验证，开放问题中提出的方向（如物理感知推理、无界生成）目前仍处于概念阶段，需要后续工作的实质性推进。

## 原文 PDF

![[paperPDFs/CVPR_2026/BulletTime_Decoupled_Control_of_Time_and_Camera_Pose_for_Video_Generation.pdf]]