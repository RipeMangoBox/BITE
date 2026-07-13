---
title: "CameraCtrl II: Dynamic Scene Exploration with Camera-controlled Video Diffusion Models"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/CameraCtrl_II_Dynamic_Scene_Exploration_with_Camera_controlled_Video_Diffusion_Models.pdf
project_link: https://hehao13.github.io/Projects-CameraCtrl-II/
code_link: https://github.com/
aliases:
- CI
- CIDSECCVDM
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 1) 构建基于真实动态视频的REALCAM数据集（VGGSfM估计相机轨迹，尺度校准，轨迹分布平衡）；2) 轻量级相机注入模块（仅在DiT初始层注入Plücker特征）与联合有标签/无标签数据的训练策略；3) 基于干净前序片段条件的自回归视频扩展方法。
primary_logic: 将相机控制信号仅叠加在扩散模型的初始层，可避免对生成过程的过度约束，从而完整保留预训练模型的动态生成能力；同时，利用干净的历史帧作为条件进行自回归扩展，可实现多片段间的外观一致性，从而支持大范围动态场景的连续探索。
claims:
- 仅使用静态数据集会导致运动强度骤降（129.40 vs 306.99）并降低相机控制精度，证明动态视频标注对维持动态生成至关重要。
- 仅在第一层注入相机特征（轻量级注入）比在多层注入或使用复杂编码器能更好地保持运动强度，且相机控制精度相当。
- 采用干净前序帧作为条件并在训练中只对新片段计算损失，相比于对条件帧加噪的策略，外观一致性大幅提升（0.8654 vs 0.8032）。
- Camera-controlled I2V Generation (Mixed Test Set) 上 FVD↓ = 73.11
---

# CameraCtrl II: Dynamic Scene Exploration with Camera-controlled Video Diffusion Models

> [!tip] 核心洞察
> 将相机控制信号仅叠加在扩散模型的初始层，可避免对生成过程的过度约束，从而完整保留预训练模型的动态生成能力；同时，利用干净的历史帧作为条件进行自回归扩展，可实现多片段间的外观一致性，从而支持大范围动态场景的连续探索。

| 字段 | 内容 |
|------|------|
| 中文题名 | CameraCtrl II：基于相机控制视频扩散模型的动态场景探索 |
| 英文题名 | CameraCtrl II: Dynamic Scene Exploration with Camera-controlled Video Diffusion Models |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2503.10592) · [Project](https://hehao13.github.io/Projects-CameraCtrl-II/) · [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | CAMERACTRL II |
| Dataset | Camera-controlled I2V Generation, Camera-controlled T2V Generation |

> [!tip] 效果简介
> - Camera-controlled I2V Generation (Mixed Test Set) 上，FVD↓ 73.11 vs 199.53 (CameraCtrl) (-126.42)；Motion strength↑ 698.51 vs 133.37 (CameraCtrl) (+565.14)；TransErr↓ 0.1527 vs 0.2812 (CameraCtrl) (-0.1285)。
> - Camera-controlled T2V Generation (Mixed Test Set) 上，FVD↓ 641.23 vs 987.34 (AC3D) (-346.11)；TransErr↓ 0.1892 vs 0.2976 (AC3D) (-0.1084)。

## 概要

现有相机控制视频生成方法在赋予用户自由控制虚拟摄像机轨迹的能力方面取得了显著进展，但其核心瓶颈在于：一旦引入相机控制信号，预训练视频扩散模型原本具备的动态内容生成能力——尤其是前景物体的自然运动——会出现大幅退化。同时，这些方法通常只能生成固定长度的短视频片段，无法基于先前已生成的内容与用户实时指定的新相机轨迹进行连续的场景探索，严重限制了可探索的空间范围与场景类型的多样性。

针对上述瓶颈，**CAMERACTRL II** 提出了一套系统性的解决方案，其核心洞察在于：**将相机控制信号以极轻量的方式叠加在扩散模型的初始层，可以避免对像素生成过程的过度约束，从而完整保留预训练模型的动态生成能力**；同时，利用干净的历史帧作为条件进行自回归扩展，而非沿用常见的加噪条件策略，能够实现多片段间的外观一致性，支撑大范围动态场景的连续探索。

具体而言，该方法包含三个关键调控节点：

1.  **数据层面**：构建了基于真实动态视频的 **REALCAM** 数据集，利用 VGGSfM 估计相机轨迹，并通过度量深度对齐进行尺度校准与轨迹分布平衡，解决了静态数据集导致运动强度骤降的问题。
2.  **模型架构与训练策略**：设计了**轻量级相机注入模块**，仅在 DiT 初始层通过新增的 patchify 层注入 Plücker 特征，并与视觉特征逐元素相加；同时采用**联合有标签/无标签数据的训练策略**，支持相机分类器自由引导以增强控制精度。
3.  **序列生成方式**：提出**基于干净前序片段条件的自回归视频扩展方法**，将前序片段的干净视觉 token 与当前片段噪声 token 拼接，并仅对新片段计算损失，实现了 clip-wise 的连贯生成。

实验结果表明，CAMERACTRL II 在相机控制精度与动态内容保持两个维度上均显著超越现有基线。在 I2V 设定下，与 **CameraCtrl**（He et al., arXiv 2024）相比，FVD 从 199.53 降至 73.11，运动强度从 133.37 提升至 698.51，平移误差从 0.2812 降至 0.1527；在 T2V 设定下，与 **AC3D**（Bahmani et al., arXiv 2024）相比，FVD 从 987.34 降至 641.23，平移误差从 0.2976 降至 0.1892。消融实验进一步验证了动态视频标注、轻量级注入策略以及干净条件帧设计的关键作用。

本方法也存在已知局限：当相机运动路径与场景几何（如栅栏等遮挡物）发生冲突时，模型因缺乏物理感知能力，可能产生穿模或结构破损等反物理结果；复杂相机轨迹下的整体几何一致性仍有提升空间；模型蒸馏虽大幅加速推理，但会引入相机控制精度的损失，质量-速度的平衡问题尚未完全解决。

### 问题背景：相机可控视频生成的兴起与瓶颈

视频扩散模型近年来在文生视频（T2V）和图生视频（I2V）领域取得了显著进展，使得高质量、高保真度的视频生成成为可能。在此基础上，一个自然且关键的需求浮现：能否让用户像操作摄像机一样，通过指定相机运动轨迹来控制生成视频的视角变化？这一能力对于电影预演、虚拟场景漫游、游戏内容生成等应用具有重要价值。

围绕这一目标，学界已涌现出一批相机控制视频生成方法。**MotionCtrl**（Wang et al., SIGGRAPH 2024）通过专用编码器将相机参数注入预训练视频扩散模型；**CameraCtrl**（He et al., arXiv 2024）进一步引入Plücker嵌入来表示相机位姿，实现了更精确的轨迹跟随；**AC3D**（Bahmani et al., arXiv 2024）则针对视频扩散Transformer架构设计了3D相机控制方案。这些工作初步验证了“用参数化相机轨迹引导视频生成”的技术可行性。

然而，现有方法面临一个核心瓶颈：**相机控制能力与动态内容生成能力之间存在严重的此消彼长**。当模型被微调以严格遵循相机轨迹时，其生成前景物体运动（如行人走动、车辆行驶）的能力会急剧退化。定量数据显示，CameraCtrl生成视频的运动强度仅为133.37，而实际动态场景中该数值可达数百量级。这意味着现有方法生成的视频虽然视角在变化，但场景本身趋于静态，缺乏生命力。

### 瓶颈根源：数据、架构与生成范式的三重制约

上述瓶颈并非偶然，而是源于数据、模型架构和序列生成范式三个层面的系统性缺陷。

**数据层面**，现有相机控制方法几乎全部依赖静态场景数据集（如RealEstate10K、DL3DV10K）进行训练。这些数据集由室内外场景的平移或旋转扫描构成，场景内容本身不发生运动。模型在这样的数据上学习相机-像素对应关系时，会隐式地将“场景静止”作为强先验编码到参数中。当推理时遇到包含动态物体的场景，模型倾向于抑制这些运动以维持其在训练中习得的稳定映射。消融实验证实：仅使用静态数据集训练时，运动强度从306.99骤降至129.40，同时相机控制精度也出现退化（TransErr从0.1830升至0.2069），说明动态视频标注对维持生成质量至关重要。

**架构层面**，主流方法倾向于在扩散模型的多个层级注入相机特征，试图让每一层Transformer或卷积层都感知相机信息。这种做法虽然强化了控制信号，却过度约束了像素生成过程——相机参数本质上描述的是全局刚体变换，而前景物体的运动需要局部、非刚体的像素变化。在每一层反复注入相机特征，相当于在生成过程的每个阶段都施加“场景应随相机刚性移动”的归纳偏置，从而系统性地压制了动态内容的涌现。实验表明，多层注入策略的运动强度显著低于仅在初始层注入的方案。

**序列生成范式层面**，现有方法仅能生成固定长度的短视频片段（通常2-4秒），无法支持用户基于已生成内容进行连续的场景探索。当用户希望“先向左看，再向前走”时，现有方法的做法是取上一片段的最后一帧作为条件图像，独立生成下一片段。这种“单帧接力”的方式缺乏对历史片段的整体感知，导致片段间外观不一致（如光照突变、物体漂移），且误差会沿序列累积放大。

### 本文动机：实现动态场景的连续可控探索

针对上述三重制约，本文提出**CAMERACTRL II**，旨在实现一个关键目标：**让用户能够像在真实3D场景中自由漫游一样，通过连续指定相机轨迹，对包含丰富动态内容的场景进行无缝、一致的视频探索**。

为实现这一目标，本文从三个维度进行系统性突破：（1）构建首个大规模动态视频相机轨迹数据集REALCAM，为模型提供动态场景下的相机-像素对应监督；（2）设计轻量级相机注入机制，仅在扩散模型初始层引入相机信号，最大限度保留预训练模型的动态生成先验；（3）提出基于干净前序片段条件的自回归扩展方法，实现多片段间的外观一致性。这三个设计共同构成了从数据、模型到推理的完整解决方案，使得相机可控视频生成首次能够处理真实世界中的动态场景。

## 核心方法与创新机理

CAMERACTRL II 的核心创新在于系统性地解耦了**相机控制精度**与**动态内容保真度**之间的固有冲突。现有相机控制视频生成方法（如 **CameraCtrl** (He et al., arXiv 2024)、**MotionCtrl** (Wang et al., SIGGRAPH 2024)）在注入相机参数后，前景物体的运动强度会急剧衰减，且仅能生成固定长度的短视频片段。CAMERACTRL II 通过以下三个关键设计突破这一瓶颈：

### 1. 轻量级相机注入：仅在初始层叠加信号

传统方法通常在扩散模型的多层 Transformer 或卷积层中注入相机特征，这种深层、持续的约束会过度干预像素生成过程，抑制模型的动态生成能力。CAMERACTRL II 的核心洞察是：**将相机控制信号仅叠加在扩散模型的初始层，可以避免对生成过程的过度约束，从而完整保留预训练模型的动态生成能力。**

具体而言，该方法在预训练视频扩散模型的 DiT 架构前新增一个独立的 *camera patchify layer*，将 Plücker 嵌入映射为与视觉 token 同维度的相机特征，然后与视觉特征进行**逐元素相加**（element-wise addition），再送入后续所有 DiT 层。消融实验（Table 4）提供了决定性证据：轻量级注入方案的运动强度达到 306.99，而多层注入（Multilayer Injection）和复杂编码器（Complex Encoder）方案均导致动态显著下降，且相机控制精度相当。

### 2. 动态视频数据集与联合训练策略

此前方法普遍依赖静态场景数据集（如 RealEstate10K、DL3DV10K）进行训练，这使得模型在加入相机控制后天然倾向于生成静态内容。CAMERACTRL II 构建了大规模动态视频数据集 **REALCAM**，其数据管道包含三个关键环节：

- **SfM 相机轨迹估计**：利用 VGGSfM 从真实动态视频中提取相机参数。
- **度量深度对齐的尺度校准**：通过最小化 Huber 损失对齐 SfM 深度与度量深度，使用 RANSAC 求解每帧尺度因子 $s_i = \arg\min_s \sum_{p \in \mathcal{P}} \rho(|s \cdot \mathbf{S}_i(p) - \mathbf{M}_i(p)|)$，将所有轨迹统一到真实物理尺度。
- **轨迹分布平衡**：按运动方向与转向类型对长尾轨迹分布进行重平衡。

Table 3 的消融实验表明：仅去除动态视频（w/o Dyn. Vid）会导致运动强度从 306.99 骤降至 129.40，TransErr 从 0.1830 恶化至 0.2069；去除尺度校准（w/o Scale Calib.）使 TransErr 升至 0.2121；去除分布平衡（w/o Dist. Balance）则严重损害相机控制精度（TransErr 0.2834, RotErr 4.56）。这组实验确证了**动态视频标注、统一度量空间和平衡轨迹分布三者对维持动态生成与相机控制精度均不可或缺**。

在训练策略上，CAMERACTRL II 采用**有标签与无标签视频联合训练**，并引入独立的相机分类器自由引导（Camera CFG）：

$$\hat{\epsilon}_{\theta}(z_{t}, c, s, t) = \epsilon_{\theta}(z_{t}, \phi_{text}, \phi_{cam}) + w_{text}(\epsilon_{\theta}(z_{t}, c, \phi_{cam}) - \epsilon_{\theta}(z_{t}, \phi_{text}, \phi_{cam})) + w_{cam}(\epsilon_{\theta}(z_{t}, c, s) - \epsilon_{\theta}(z_{t}, c, \phi_{cam}))$$

该公式将文本引导权重 $w_{text}$ 与相机引导权重 $w_{cam}$ 解耦，允许用户灵活调节控制强度。

### 3. 基于干净历史条件的自回归视频扩展

为实现多片段间的连续场景探索，CAMERACTRL II 提出了一种 **clip-wise 自回归生成方法**。与简单取上一片段最后一帧作为条件图像不同，该方法将前序片段的**干净视觉 token**（而非加噪 token）与当前片段的噪声 token 沿序列维度拼接，并附加二进制掩码标记条件区域；训练时**仅对当前片段计算损失**。

Table 5 的消融实验提供了关键对比：采用干净条件帧（Clean Condition）相比向条件帧加噪（Noised Condition），外观一致性从 0.8032 大幅提升至 0.8654。这一设计有效避免了误差累积，实现了多片段间的外观连贯性。

### 创新点总结

| 设计维度 | 基线方法 | CAMERACTRL II | 核心效果 |
|---------|---------|---------------|---------|
| 相机注入层级 | 多级 DiT 或卷积层注入 | 仅初始层 patchify + 逐元素相加 | 保持运动强度（306.99 vs 129.40） |
| 训练数据 | 静态场景数据集 | REALCAM 动态数据集 + 尺度校准 + 分布平衡 | 同时提升动态与相机控制精度 |
| 训练策略 | 仅标注数据微调 | 有标签/无标签联合训练 + 相机 CFG | 灵活控制强度 |
| 序列生成 | 取最后一帧作为条件图像 | 干净历史 token 拼接 + 掩码 + 仅当前片段损失 | 外观一致性 0.8654 vs 0.8032 |

这些创新共同构成了一个完整的解决方案：轻量级注入保留了预训练模型的动态生成能力，REALCAM 数据集提供了动态场景下的相机控制学习信号，而干净历史条件的自回归扩展则打通了多片段连续探索的技术链路。

CAMERACTRL II 的核心目标是实现**相机可控的动态场景视频生成与连续探索**。其整体 pipeline 可抽象为三个相互衔接的阶段：数据基础构建、单片段相机控制生成、多片段自回归扩展。

### Pipeline 总览

系统的输入是一个起始图像（I2V 模式）或文本描述（T2V 模式），以及用户定义的一系列相机轨迹。输出是多个外观一致的视频片段，用户可在观看前序片段后动态指定下一步的相机运动，实现对场景的持续探索（Figure 1）。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2503_10592/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of CAMERACTRL II. Our camera-controlled video diffusion model generates consistent video sequences for dynamic scenes based on user-defined camera trajectories. The first row represents a generated video clip conditioned on the starting image and a user input camera trajectory. After watching the generated video clip, user can decide next step and specify the corresponding camera trajectories. Subsequent rows show clips conditioned on previous generated videos and these newly provided camera trajectories. The model strictly follows these user camera trajectory inputs while maintaining scene consistency across multiple video clips, enabling seamless navigation around pedestrians...*

**阶段一：动态视频数据标注管道**

该阶段从真实动态视频中构建带相机轨迹标注的数据集 REALCAM。核心流程为：使用 VGGSfM 从视频中估计相机轨迹，通过度量深度对齐进行尺度校准，并按运动方向与转向类型对轨迹分布进行平衡处理（Figure 2）。这一管道解决了现有静态数据集无法支撑动态内容生成的根本瓶颈。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2503_10592/figures/002_Figure_2.jpg]]
*Figure 2: Dataset curation pipeline. We omit the process of dynamic video selection*

**阶段二：轻量级相机注入与联合训练**

在预训练视频扩散模型的基础上，CAMERACTRL II 仅在 DiT 的初始层添加一个额外的 camera patchify 层（Figure 3a）。该层将 Plücker 嵌入编码为与视觉特征同形状的相机特征，通过逐元素相加后送入后续 DiT 层。训练时联合使用有标签和无标签视频数据，并支持相机分类器自由引导（Camera CFG），以灵活调节控制强度。

**阶段三：视频片段自回归扩展**

为实现连续场景探索，模型提取前序片段的最后 n 帧作为干净视觉 token，与当前片段的噪声 token 沿序列维度拼接，并附加二进制掩码区分条件帧与生成帧（Figure 3b）。训练时仅对当前片段的 token 计算损失，推理时基于历史干净帧与新相机轨迹生成下一片段，实现 clip-wise 自回归扩展。

### 模块间关系

三个阶段构成递进依赖关系：阶段一提供动态标注数据，使阶段二的轻量级注入模型能够同时保持动态生成能力和相机控制精度；阶段二训练出的单片段模型是阶段三自回归扩展的基础；阶段三利用阶段二模型的去噪能力，通过干净条件帧拼接实现多片段间的外观一致性。

### 关键设计决策

整个框架围绕一个核心洞察展开：**将相机控制信号仅叠加在扩散模型的初始层，可避免对生成过程的过度约束，从而完整保留预训练模型的动态生成能力**。这一设计在架构层面体现为轻量级注入（仅初始层 patchify + element-wise addition），在数据层面体现为动态视频标注的必要性（静态数据导致运动强度从 306.99 骤降至 129.40），在扩展层面体现为干净条件帧策略（外观一致性 0.8654 vs 加噪策略的 0.8032）。

### 3.1 基础扩散框架

CAMERACTRL II 构建在预训练视频扩散模型之上，其基础训练目标为标准的去噪损失函数：

$$L ( \theta ) = \mathbb { E } _ { z _ { 0 } , \epsilon , c , s , t } [ | \epsilon - \hat { \epsilon } _ { \theta } ( z _ { t } , c , s , t ) | _ { 2 } ^ { 2 } ]$$

其中 $z_0$ 为干净视频潜变量，$\epsilon$ 为添加的高斯噪声，$c$ 为文本条件，$s$ 为相机条件，$t$ 为时间步，$\hat{\epsilon}_{\theta}$ 为去噪网络预测的噪声。该框架为后续相机控制注入与序列扩展提供了统一的优化基础。

### 3.2 相机轨迹编码与尺度校准

**Plücker 嵌入。** 对于每帧给定的相机外参矩阵 $E = [R; t]$ 和内参矩阵 $K$，对每个像素 $(u, v)$ 计算其 Plücker 嵌入 $p = (o \times d', d')$，其中 $o$ 为相机光心坐标，$d'$ 为归一化的光线方向。最终每帧构建 $P_i \in \mathbb{R}^{6 \times h \times w}$ 的 Plücker 嵌入张量，作为后续相机注入模块的输入。

**尺度校准。** 由于 SfM 重建存在尺度歧义，需将估计的相机轨迹对齐到度量空间。对每帧 $i$，通过最小化 Huber 损失 $\rho$ 求解最优尺度因子：

$$s_i = \arg\min_s \sum_{p \in \mathcal{P}} \rho(|s \cdot \mathbf{S}_i(p) - \mathbf{M}_i(p)|)$$

其中 $\mathbf{S}_i(p)$ 为 SfM 估计的深度，$\mathbf{M}_i(p)$ 为度量深度（如来自深度传感器或单目深度估计器），$\mathcal{P}$ 为有效像素集合。采用 RANSAC 求解以增强对离群点的鲁棒性。

### 3.3 轻量级相机注入与联合训练

**相机注入机制。** 区别于现有方法在多个 DiT 层或通过专用编码器注入相机特征，CAMERACTRL II 仅在扩散模型的初始层添加一个额外的相机 patchify 层。该层接收 Plücker 嵌入作为输入，输出与视觉特征相同形状的相机特征 $p_{feat}$，随后与视觉特征 $z_{feat}$ 进行逐元素相加：

$$z_{feat} = z_{feat} + p_{feat}$$

融合后的特征送入后续 DiT 层进行去噪。这一设计避免了相机信号对生成过程的过度约束，从而完整保留预训练模型的动态内容生成能力。

**联合训练策略。** 模型在有标签（含相机轨迹标注）和无标签视频数据上联合训练所有参数。对于无标签数据，相机条件被设为空 $\phi_{cam}$，使模型同时学习条件生成和无条件生成能力，为相机分类器自由引导提供基础。

**相机分类器自由引导。** 推理时采用独立的文本引导权重 $w_{text}$ 和相机引导权重 $w_{cam}$：

$$\hat{\epsilon}_{\theta}(z_{t}, c, s, t) = \epsilon_{\theta}(z_{t}, \phi_{text}, \phi_{cam}) + w_{text}(\epsilon_{\theta}(z_{t}, c, \phi_{cam}) - \epsilon_{\theta}(z_{t}, \phi_{text}, \phi_{cam})) + w_{cam}(\epsilon_{\theta}(z_{t}, c, s) - \epsilon_{\theta}(z_{t}, c, \phi_{cam}))$$

其中 $\phi_{text}$ 和 $\phi_{cam}$ 分别表示空文本条件和空相机条件。通过调节 $w_{cam}$ 可灵活控制相机轨迹的遵循强度，而不影响文本对齐质量。

### 3.4 自回归视频片段扩展

为实现多片段连续场景探索，CAMERACTRL II 采用基于干净前序片段条件的自回归扩展机制。

**条件构造。** 从前序生成片段中提取最后 $n$ 帧的视觉 token $z_0^{i}$ 作为上下文条件，保持其干净状态（不添加噪声）。当前待生成片段的 token $z_t^{i+1}$ 按标准扩散流程添加噪声。两者沿序列维度拼接，并附加二进制掩码 $m \in \mathbb{R}^{q \times 1}$（条件 token 位置为 1，当前片段 token 位置为 0）。

**训练目标。** 仅对当前片段的 token 计算去噪损失，条件 token 不参与损失计算。这一设计确保模型学习如何基于干净的历史帧推断新视角下的场景内容，而非简单地对条件帧进行去噪重建。消融实验（Tab. 5）证实，相比向条件帧加噪的策略，干净条件训练使外观一致性从 0.8032 提升至 0.8654，FVD 也有显著改善。

## 实验与关键发现

### 主实验结果

CAMERACTRL II 在图像到视频（I2V）和文本到视频（T2V）两种设定下，均显著优于现有相机控制视频生成方法。表2汇总了与 **MotionCtrl**（Wang et al., SIGGRAPH 2024）、**CameraCtrl**（He et al., arXiv 2024）和 **AC3D**（Bahmani et al., arXiv 2024）的定量对比。

在 I2V 设定下，CAMERACTRL II 的 FVD 降至 73.11，而 CameraCtrl 为 199.53，MotionCtrl 为 221.23，降幅超过 63%。相机控制精度方面，TransErr 从 CameraCtrl 的 0.2812 降至 0.1527，RotErr 从 2.81° 降至 1.58°，几何一致性从 52.12 跃升至 88.70。最关键的动态保持指标——运动强度（Motion strength）——从 CameraCtrl 的 133.37 飙升至 698.51，提升超过 4 倍，直接验证了轻量级注入策略对预训练模型动态生成能力的有效保护。

在 T2V 设定下，CAMERACTRL II 相比 AC3D 同样取得压倒性优势：FVD 从 987.34 降至 641.23，TransErr 从 0.2976 降至 0.1892。需注意，AC3D 开源版本仅支持 T2V，因此外观一致性指标在该行标记为 N/A。

### 消融实验

消融实验从数据管道、模型架构和序列扩展三个维度，系统验证了各设计选择的必要性。

**数据管道消融**（表3）揭示了三个关键发现。其一，去除动态视频数据集（w/o Dyn. Vid）导致运动强度从 306.99 骤降至 129.40，同时 TransErr 从 0.1830 恶化至 0.2069，证明仅使用静态场景数据会严重抑制动态内容生成并损害相机控制精度。其二，去除尺度校准（w/o Scale Calib.）使 TransErr 升至 0.2121，验证了将 SfM 估计轨迹对齐到统一度量空间的必要性。其三，去除轨迹分布平衡（w/o Dist. Balance）造成最严重的控制精度退化——TransErr 升至 0.2834，RotErr 升至 4.56°，几何一致性降至 40.78，表明平衡长尾轨迹分布对模型泛化至关重要。

**架构与训练策略消融**（表4）的核心结论是：轻量级注入（仅在初始层通过 patchify 层注入 Plücker 特征并逐元素相加）在保持运动强度（306.99）的同时，取得了与复杂编码器相当的相机控制精度；而多层注入（Multilayer Inj.）或使用复杂编码器（Complex Encoder）均会不同程度地抑制动态生成。联合有标签/无标签数据的训练策略进一步提升了控制精度。

**序列扩展消融**（表5）聚焦于自回归生成中的条件帧处理策略。采用干净前序帧作为条件（Clean Condition）相比对条件帧加噪（Noised Condition），外观一致性从 0.8032 提升至 0.8654，FVD 也有显著改善。此外，使用前序片段最后一帧作为参考系（Last Frame Ref.）优于使用首帧（First Frame Ref.），因为前者与当前片段的起始帧在视觉上更连贯。

### 蒸馏效率与质量权衡

表1展示了模型蒸馏前后的效率对比。在 4 张 H800 GPU 上生成 4 秒 12fps 视频，原始模型推理耗时 13.83 秒；经渐进式蒸馏后降至 2.61 秒；采用 APT 一步蒸馏后进一步压缩至 0.59 秒。然而，速度提升伴随相机控制精度的退化：TransErr 从 0.1892 升至 0.2500（APT），RotErr 从 1.66° 升至 2.56°。这表明质量-速度的平衡仍是开放问题。

### 三维几何一致性验证

CAMERACTRL II 生成的视频不仅满足逐帧相机控制约束，其底层三维几何也保持高度一致。使用 FLARE 对生成视频帧进行三维点云重建（图6），结果表明模型能够生成几何上合理的场景结构，而非仅在二维像素空间进行外观拼接。这归因于 Plücker 嵌入所提供的显式三维几何先验与扩散模型隐式三维表征能力的协同作用。

### 失败模式分析

CAMERACTRL II 的主要失败模式出现在相机运动路径与场景几何发生物理冲突时。图7展示了一个典型案例：用户指定的相机轨迹穿越栅栏，模型严格遵循该轨迹生成视频，导致栅栏结构出现破损和穿模现象。这一问题的根源在于模型缺乏显式的场景几何感知能力——它仅根据相机参数和图像条件进行像素级生成，无法推断场景中的遮挡关系和物理边界。当相机路径要求“穿过”一个不透明的场景元素时，模型会尝试生成看似合理但物理上不可能的中间帧，从而产生反现实的结构变形。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2503_10592/figures/005_Table_2.jpg]]
*Table 2: Quantitative Comparisons. We compare against MotionCtrl [54] and CameraCtrl [21] in image-to-video setting, the AC3D [2] in the text-to-video setting. Since open-sourcing AC3D only supports text-to-video generation, appearance consistency between given image and generated videos is not available*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2503_10592/figures/007_Table_3.jpg]]
*Table 3: Ablation study on dataset curation pipeline*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2503_10592/figures/009_Table_5.jpg]]
*Table 5: Ablation study on key design choices in extending the single-clip model to enable scene exploration*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2503_10592/figures/010_Figure_5.jpg]]
*Figure 5: Visualization results of CAMERACTRL II across diverse scenes. Our model demonstrates effective camera control in various visual environments, including Minecraft-style game scenes (top row), black and white foggy London streets (second row), abandoned hospital interiors (third row), fantasy forest hiking trails (fourth row), and animated palace scenes (bottom row). The results are generated using the I2V setting, with the first image as the condition image. The camera trajectories are shown on the left of each row*

## 定位与知识库关联

### 与基线方法的关系

CAMERACTRL II 直接对标三类相机控制视频生成基线：基于图像到视频（I2V）的 **MotionCtrl**（Wang et al., SIGGRAPH 2024）和 **CameraCtrl**（He et al., arXiv 2024），以及基于文本到视频（T2V）的 **AC3D**（Bahmani et al., arXiv 2024）。这些基线共享一个核心范式——将相机参数注入预训练视频扩散模型，但在注入机制与数据策略上存在根本分歧。

**注入机制的代际差异**。MotionCtrl 与 CameraCtrl 均采用专用编码器将相机参数注入到预训练模型的多个层级（如每个 Transformer 块或卷积层），试图通过深层条件化强化控制精度。然而，这种做法对像素生成过程施加了过度约束，导致一个被 CAMERACTRL II 揭示的关键瓶颈：**相机控制与动态内容生成之间存在零和博弈**——控制精度越高，前景物体的运动强度越弱。在定量层面，CameraCtrl 的运动强度仅为 133.37，而 CAMERACTRL II 达到 698.51（Tab. 2），差距超过 5 倍。CAMERACTRL II 的因果调节器是将相机注入严格限制在 DiT 的初始层：通过新增的 camera patchify 层将 Plücker 嵌入转换为与视觉特征同形的张量，经逐元素相加后送入后续 DiT 层，不再在深层重复注入。这一设计使相机信号仅作为“初始引导”而非“持续约束”，从而完整保留预训练模型的动态生成能力。消融实验（Tab. 4）证实，多层注入会导致运动强度显著下降，而轻量级注入在保持动态的同时实现了与复杂编码器相当的相机控制精度（TransErr 0.1830 vs 0.1892~0.2001）。

**数据策略的代际差异**。MotionCtrl 与 CameraCtrl 的训练数据以静态场景数据集（如 RealEstate10K、DL3DV10K）为主，这些数据中相机运动与场景内容高度耦合（相机运动即场景视差变化），缺乏独立的前景物体运动。CAMERACTRL II 构建了 REALCAM——一个基于真实动态视频的大规模数据集，利用 VGGSfM 估计相机轨迹，并通过度量深度对齐进行逐帧尺度校准，同时按运动方向和转向类型平衡轨迹分布。消融实验（Tab. 3）给出了决定性证据：去除动态视频后，运动强度从 306.99 骤降至 129.40，相机控制精度也同步恶化（TransErr 从 0.1830 升至 0.2069），说明动态标注视频对维持“控制-动态”双目标优化至关重要。

**训练策略的扩展**。CAMERACTRL II 在训练中联合使用有标签和无标签视频数据，并设计了独立的相机分类器自由引导（Camera CFG）公式：

$$\hat{\epsilon}_{\theta}(z_{t}, c, s, t) = \epsilon_{\theta}(z_{t}, \phi_{text}, \phi_{cam}) + w_{text}(\epsilon_{\theta}(z_{t}, c, \phi_{cam}) - \epsilon_{\theta}(z_{t}, \phi_{text}, \phi_{cam})) + w_{cam}(\epsilon_{\theta}(z_{t}, c, s) - \epsilon_{\theta}(z_{t}, c, \phi_{cam}))$$

该公式将文本引导权重 $w_{text}$ 与相机引导权重 $w_{cam}$ 解耦，允许在推理时灵活调节控制强度，而基线方法通常将相机条件与文本条件捆绑处理。

**序列生成能力的代际差异**。MotionCtrl 与 CameraCtrl 仅支持单片段生成；在需要多片段探索时，通常取上一片段的最后一帧作为条件图像生成下一片段，这会累积误差并破坏外观连贯性。CAMERACTRL II 提出了 clip-wise 自回归扩展机制：将前序片段的**干净**视觉 token 与当前片段的噪声 token 沿序列维度拼接，并附加二进制掩码以区分条件区域与生成区域，训练时仅对新片段计算损失。这一设计使外观一致性从 0.8032（对条件帧加噪的策略）提升至 0.8654（Tab. 5），同时 FVD 也显著改善。

### 适用边界

**场景类型边界**。CAMERACTRL II 在多样化场景中展现了有效的相机控制能力，包括游戏画面（Minecraft 风格）、雾中街景、废弃建筑室内、森林徒步小径和动画宫殿场景（Fig. 5）。然而，其动态场景探索能力依赖于 REALCAM 数据集的覆盖范围——该数据集通过 VGGSfM 估计相机轨迹，对于高度动态或遮挡严重的场景，SfM 估计的鲁棒性存在天然上限。

**物理感知边界**。模型严格遵循用户指定的相机轨迹，但**不具备场景几何感知能力**。当相机路径与场景结构（如栅栏、墙壁等遮挡物）发生物理冲突时，模型会生成穿模或结构破损等反物理结果（Fig. 7）。这是当前相机控制视频生成方法的共性局限，根源在于扩散模型仅学习像素级分布，缺乏显式的 3D 几何表示。

**质量-速度权衡边界**。CAMERACTRL II 探索了两种蒸馏策略以加速推理：渐进式蒸馏将 4 秒 12fps 视频的生成时间从 13.83s 降至 2.61s（4×H800 GPU），而 APT 一步蒸馏进一步压缩至 0.59s。然而，加速伴随着相机控制精度的损失——APT 蒸馏后 TransErr 从 0.1892 升至 0.2500，RotErr 从 1.66 升至 2.56（Tab. 1），说明当前蒸馏方案尚未解决质量-速度的最优平衡。

### 局限与开放问题

**已知局限**。除物理感知缺失和质量-速度权衡外，论文明确指出的局限包括：（1）在复杂相机轨迹下，生成场景的整体几何一致性仍有待提升；（2）REALCAM 数据集依赖 VGGSfM 的估计精度，对于高度动态或遮挡严重场景的泛化性尚不明确。

**开放问题**。从方法逻辑与实验结果中可推导出以下待解问题：

1. **几何感知注入**：能否在相机注入模块中引入场景几何先验（如单目深度估计或 NeRF 式隐式表示），使模型在遵循相机轨迹的同时感知并规避物理冲突？这需要将当前的 2D Plücker 嵌入扩展为 3D 感知的条件信号。

2. **3D 一致性强化**：虽然 CAMERACTRL II 生成的视频可通过 FLARE 重建出合理的 3D 点云（Fig. 6），但复杂轨迹下的几何一致性仍有限。是否需要在训练目标中显式加入多视图几何一致性约束（如光度重投影损失或 3D 几何正则项）？

3. **蒸馏质量保持**：APT 一步蒸馏带来的控制精度损失是否可通过更大的蒸馏 batch size、更多的计算资源或改进的蒸馏损失函数来缓解？这指向一个更一般的问题——如何在少步采样框架下保持条件生成的质量。

4. **SfM 依赖的鲁棒性**：REALCAM 的标注质量受限于 VGGSfM 的性能上限。对于动态前景占比高、运动模糊严重或纹理稀疏的视频，是否需要引入额外的深度传感器数据或自监督深度估计作为补充监督信号？

## 原文 PDF

![[paperPDFs/arxiv_2025/CameraCtrl_II_Dynamic_Scene_Exploration_with_Camera_controlled_Video_Diffusion_Models.pdf]]
