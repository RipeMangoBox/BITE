---
title: "Motion-I2V: Consistent and Controllable Image-to-Video Generation with Explicit Motion Modeling"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Motion_I2V_Consistent_and_Controllable_Image_to_Video_Generation_with_Explicit_Motion_Modeling.pdf
aliases:
- MI
- Motion-I2V
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过将I2V解耦为两阶段——第一阶段预测像素级运动轨迹（显式运动场），第二阶段基于预测运动场进行运动增强的时序注意力特征传播——来显式建模运动并扩大时序感受野。"
primary_logic: "将图像到视频生成分解为运动预测和内容传播两个阶段，利用预测的稠密运动场对参考帧特征进行扭曲注入，使生成模型在保持内容一致性的同时，能合成更大运动的视频，并且可通过稀疏轨迹控制运动。"
claims:
- "Motion-I2V将I2V分解为两个阶段，引入显式运动建模。"
- "第一阶段使用基于扩散的运动场预测器，预测像素轨迹。"
- "第二阶段提出运动增强时序注意力，利用预测轨迹传播参考图像特征。"
- "为第一阶段训练稀疏轨迹ControlNet，支持用户精确控制运动轨迹和区域。"
---

# Motion-I2V: Consistent and Controllable Image-to-Video Generation with Explicit Motion Modeling

> [!tip] 核心洞察
> 将图像到视频生成分解为运动预测和内容传播两个阶段，利用预测的稠密运动场对参考帧特征进行扭曲注入，使生成模型在保持内容一致性的同时，能合成更大运动的视频，并且可通过稀疏轨迹控制运动。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Motion-I2V：基于显式运动建模的一致可控图像到视频生成 |
| 英文题名 | Motion-I2V: Consistent and Controllable Image-to-Video Generation with Explicit Motion Modeling |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2401.15977) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Motion-I2V |
| Dataset | UCF-101 / MSR-VTT |

> [!tip] 效果简介
> - UCF-101 / MSR-VTT 上，Frame Consistency 为 0.9871。
> - UCF-101 / MSR-VTT 上，Prompt Consistency 为 34.86。

## 概述

图像到视频生成（I2V）的核心挑战在于，如何在仅给定单张静态参考图像的情况下，合成一段时序连贯且运动幅度可控的视频。现有主流方法——如 **DynamiCrafter**（Xing et al., 2023）、**I2VGen-XL**（Zhang et al., 2023）等——主要依赖视频扩散模型中的一维时序注意力机制来隐式地学习动态信息。这种设计的根本瓶颈在于：一维时序注意力的时间感受野有限，当目标运动幅度较大或涉及显著视角变化时，模型难以在长时序跨度上维持内容的一致性，往往导致生成视频的运动幅度偏小或出现内容失真。与此同时，这些方法普遍缺乏对生成运动的精细控制手段，用户无法指定特定区域的动作轨迹或动画范围。

Motion-I2V 针对上述瓶颈提出了一个显式运动建模框架，其核心洞察是将图像到视频生成解耦为两个阶段：**先预测运动，再传播内容**。具体而言，第一阶段训练一个基于扩散的运动场预测器，从参考图像和文本提示中推断出每个像素在未来帧中的稠密运动轨迹；第二阶段则引入运动增强的时序注意力机制，利用预测的运动场对参考帧特征进行扭曲，并将扭曲后的特征作为注意力中的键和值注入生成过程。这一设计显著扩大了时序感受野，使模型无需直接从零学习复杂的时空模式，从而在保持内容一致性的前提下，能够合成更大运动幅度的视频。

在可控性方面，Motion-I2V 为第一阶段额外训练了一个稀疏轨迹 ControlNet，允许用户通过绘制稀疏轨迹和运动区域蒙版来精确控制运动轨迹和动画范围。此外，第二阶段的运动传播机制天然支持零样本视频到视频翻译——只需将源视频首帧进行风格转换，即可利用提取的运动场驱动整个视频的风格迁移。

定量实验表明，Motion-I2V 在 UCF-101 和 MSR-VTT 基准上取得了最优的指令遵循能力和时序一致性（Frame Consistency 达 0.9871），同时生成了相对较大的运动幅度。定性对比中，DynamiCrafter 和 Pika 1.0 倾向于生成极小运动的视频，Gen-2 虽能产生大运动但无法保持参考图像的身份一致性，而 Motion-I2V 在大运动场景下仍能维持时序连贯性。消融实验进一步验证了显式运动场预测和注意力注入方式对稳定生成和避免极端失真的关键作用。

该方法也存在一定局限：生成视频往往呈现中等亮度，可能与噪声调度未强制最后时间步达到零信噪比有关；此外，两阶段框架向任意长视频生成以及三维场景动态建模的扩展仍是待探索的开放问题。

## 背景与动机

图像到视频（Image-to-Video, I2V）生成的目标是从单张静态图像出发，合成一段时序连贯的视频。近年来，基于扩散模型（Diffusion Models）的视频生成方法取得了显著进展，但在I2V任务中仍面临两个核心瓶颈。

**时序一致性与大运动的矛盾。** 现有I2V方法（如 **DynamiCrafter**（Xing et al., 2023）、**I2VGen-XL**（Zhang et al., 2023））通常依赖于视频潜在扩散模型中的一维时序注意力机制来隐式地学习帧间动态。这种机制的时间感受野有限——每一帧主要关注其相邻帧，缺乏对长程运动轨迹的全局感知。其直接后果是：当面对大运动或显著视角变化时，生成视频容易出现内容闪烁、身份漂移等时序不一致问题。定性对比（Figure 8）清楚地揭示了这一现象：DynamiCrafter 和商用系统 Pika 1.0 倾向于生成运动幅度极小的视频以规避风险，而 Gen-2 虽能产生较大运动，却难以保持参考图像的视觉身份。

**运动控制能力的缺失。** 主流I2V方法仅通过文本提示（text prompt）来控制生成内容，用户无法精细指定画面中“哪里动”和“如何动”。**VideoComposer**（Wang et al., 2023）等可控视频生成方法虽引入了额外条件，但并未提供针对像素级运动轨迹的精确控制手段。这使得I2V在实际创作场景中的应用受到严重制约——用户无法像在图像编辑中那样，通过简单的交互（如绘制箭头或涂抹区域）来指定期望的运动模式。

上述两个问题本质上是同一根源的不同表现：**运动建模的隐式性**。当模型将运动模式与外观生成混合在同一个黑箱注意力机制中学习时，它既难以捕捉大幅度的时空依赖，也无法将运动作为独立维度暴露给用户进行操控。

Motion-I2V 的核心动机正是打破这一隐式建模范式。其关键洞察在于：**将I2V生成解耦为“预测运动”与“传播内容”两个阶段**。第一阶段显式地推理出参考图像中每个像素在未来帧中的运动轨迹，形成稠密的运动场；第二阶段则利用这些预测的运动场，通过特征扭曲（warping）和运动增强的时序注意力，将参考图像的内容忠实地传播到所有生成帧中。这种解耦不仅通过扩大时序感受野缓解了大运动下的不一致问题，还天然地为运动控制提供了接口——用户只需在第一阶段输入稀疏轨迹或运动区域蒙版，即可精确操控生成视频中的运动。

## 核心创新

Motion-I2V 的核心创新在于将图像到视频生成（I2V）**显式解耦为运动预测与内容传播两个阶段**，从而突破了现有方法的两大瓶颈：一维时序注意力有限的时间感受野，以及缺乏对生成运动的精细控制能力。

### 从隐式学习到显式运动建模

现有 I2V 方法（如 **DynamiCrafter**、**I2VGen-XL**）依赖标准一维时序自注意力隐式地学习视频动态。这种机制的时间感受野有限，当参考图像与目标帧之间存在大位移运动时，模型难以建立远距离的像素对应关系，导致时序一致性下降或运动幅度被人为压缩。

Motion-I2V 将运动建模从隐式学习中剥离，引入一个**独立的运动场预测器**（Stage 1）。该预测器以参考图像和文本提示为条件，直接输出参考帧到每一未来帧的**稠密像素级位移场**（即运动轨迹）。这一设计将“物体往哪里运动”的推理与“物体长什么样”的生成在结构上分离，使运动模式的学习不再与外观生成纠缠。

### 运动增强时序注意力：扩大感受野的关键机制

在第二阶段视频渲染中，Motion-I2V 并不直接使用标准时序注意力，而是提出了**运动增强时序注意力**。其核心操作是：利用 Stage 1 预测的运动场 $f_{0 \to i}$ 对参考帧的潜在特征 $z[0]$ 进行前向扭曲，得到对齐后的特征 $z[i]' = \mathcal{W}(z[0], f_{0 \to i})$。这些扭曲特征被插入到时序注意力的键（Key）和值（Value）中，与原始帧特征交错排列，而查询（Query）仍来自原始特征：

$$z'' = \mathrm{Attention}(Q, K, V) = \mathrm{Softmax}(QK^T)V$$

其效果是：注意力机制可以直接在参考帧的对应位置上检索内容，无需在长时序范围内自行“寻找”匹配。这等价于将时序感受野从相邻帧扩展到了整个视频序列，使模型在合成大运动视频时仍能保持内容一致性。消融实验证实，采用注意力自适应注入扭曲特征（而非直接相加）能进一步提升一致性并避免极端失真。

### 从仅文本控制到稀疏轨迹与运动刷的精细交互

传统 I2V 方法仅支持文本提示控制，用户无法精确指定运动路径或动画区域。Motion-I2V 通过在 Stage 1 上训练一个**轨迹 ControlNet**，首次实现了对运动的像素级交互控制。该 ControlNet 接收用户绘制的稀疏轨迹（红色曲线箭头）和对应二值蒙版作为条件，输出稠密光流场。用户可同时使用**运动刷**指定动画区域（紫色蒙版），未蒙版区域保持静止，两种控制方式可组合使用（Figure 6）。

这一可控性扩展源于框架的模块化设计：运动预测是独立的生成任务，因此可以像文生图中的 ControlNet 一样，通过注入额外条件来引导运动场的生成，而无需重新设计整个视频生成管线。

## 整体框架

![[assets/figures/papers/paper_list_l3_Motion_I2V_Consistent_and_Controllable_Image_to_Video_Generation_with_Ex/figures/003_Figure_3.jpg]]
*Figure 3: Overview of trajectory ControlNet. We train a Trajectory ControlNet based on the pre-trained stage 1 of Motion-I2V. It takes sparse trajectories and corresponding binary mask as additional conditions, and output dense optical flow maps*

![[assets/figures/papers/paper_list_l3_Motion_I2V_Consistent_and_Controllable_Image_to_Video_Generation_with_Ex/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Motion-I2V. The first stage of Motion-I2V targets at deducing the motions that can plausibly animate the reference image. It is conditioned on the reference image and text prompt, and predicts the motion field maps between the reference frame and all the future frames. The second stage propagates reference image’s content to synthesize frames. A novel motion-augmented temporal layer enhances 1-D temporal attention with warped features. This operation enlarges the temporal receptive field and alleviates the complexity of directly learning the complicated spatial-temporal patterns*

Motion-I2V 将图像到视频生成（I2V）解耦为两个显式阶段，核心思路是将运动预测与内容传播分离，从而突破传统一维时序注意力在时间感受野上的瓶颈。

**输入与输出流**：系统接受一张参考图像 $I_0$ 和一段文本提示 $c$ 作为输入，最终输出一段 $N+1$ 帧的视频。整个 pipeline 如图 Figure 2 所示，分为两个串行阶段：

1. **第一阶段——运动场预测器（Motion Field Predictor）**：以参考图像和文本提示为条件，预测参考帧与所有未来帧之间的稠密像素级运动轨迹，即前向光流场 $f_{0 \to i}$（$i=1, \dots, N$）。该阶段基于视频扩散模型构建，并使用光流 VAE 将二维光流场编码为潜在表示 $z_{0i,0} = E_{flow}(f_i)$ 供扩散模型处理。其训练目标是最小化噪声预测的均方误差：
   $$l_\epsilon = ||\epsilon - \epsilon_\theta(z_t, t, c)||_2^2$$

2. **第二阶段——运动增强视频渲染器（Motion-Augmented Video Renderer）**：利用第一阶段预测的运动场，对参考帧的潜在特征 $z[0]$ 进行前向扭曲，生成每一帧对应的扭曲特征：
   $$z[i]' = \mathcal{W}(z[0], f_{0 \to i})$$
   这些扭曲特征与原始特征沿时间维度交错拼接，形成增强特征。在时序注意力层中，查询（Query）来自原始特征，键（Key）和值（Value）来自增强特征，从而在注意力计算中显式注入运动信息：
   $$z'' = \mathrm{Attention}(Q, K, V) = \mathrm{Softmax}(QK^T)V$$
   此外，第二阶段采用选择性加噪策略，始终将干净的参考帧潜在码 $z_{ref}$ 与带噪的潜在码 $z_{0:N,t}$ 沿时间轴拼接，以在去噪过程中保持参考内容的一致性。

**模块间关系**：两个阶段之间通过预测的稠密运动场 $f_{0 \to i}$ 实现信息传递。第一阶段专注于“运动理解”，第二阶段专注于“内容传播”——这种分工使得模型无需在单阶段内同时学习复杂的时空模式，而是将运动建模的负担从视频生成模型中剥离出来，由专门的运动预测器承担。消融实验证实，利用第一阶段预测的运动场能显著稳定视频生成，而采用注意力机制自适应注入扭曲特征（相较于直接相加）能进一步提升一致性并避免极端失真（Table 2）。

**可控性扩展**：在第一阶段预训练模型的基础上，可训练一个轨迹 ControlNet（Figure 3），接收用户绘制的稀疏轨迹和对应二值蒙版作为额外条件，输出稠密光流场，从而支持精确的运动轨迹控制和区域特定动画（运动刷）。

## 核心模块与公式推导

Motion-I2V 将图像到视频生成分解为两个串联阶段，其核心模块围绕显式运动建模展开：第一阶段预测稠密运动场，第二阶段利用该运动场进行特征传播与帧合成。

### 扩散模型基础

两个阶段均基于视频潜在扩散模型构建。给定潜在码 $z_0$，前向扩散过程逐步添加高斯噪声：

$$z_t = \sqrt{\overline{\alpha}_t} z_0 + \sqrt{1 - \overline{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

去噪网络 $\epsilon_\theta$ 以噪声潜在码 $z_t$、时间步 $t$ 和条件 $c$ 为输入，通过均方误差损失训练：

$$l_\epsilon = ||\epsilon - \epsilon_\theta(z_t, t, c)||_2^2$$

### 第一阶段：运动场预测器

该模块以参考图像和文本提示为条件，预测参考帧与所有未来帧之间的像素级运动轨迹。为适配扩散模型的处理方式，引入光流 VAE 编码器 $E_{flow}$，将二维光流图 $f_{0 \to i}$ 编码为潜在表示 $z_{0i,0}$，从而将运动预测转化为潜在空间中的生成任务。此阶段输出的稠密位移场 $f_{0 \to i}$ 描述了参考帧每个像素在后续各帧中的空间位置，为第二阶段提供显式的运动先验。

### 第二阶段：运动增强视频渲染器

第二阶段的核心是运动增强时序注意力机制。标准视频扩散模型的时序注意力仅沿一维时间轴操作，时间感受野有限。Motion-I2V 利用第一阶段预测的运动场对参考帧特征进行前向扭曲，将扭曲后的特征注入时序注意力以扩大感受野。

具体而言，对于第 $i$ 帧，利用运动场 $f_{0 \to i}$ 对参考帧特征 $z[0]$ 执行前向扭曲操作：

$$z[i]' = \mathcal{W}(z[0], f_{0 \to i})$$

扭曲后的特征图 $z[i]'$ 与原始特征图沿时间维度交错排列，构成增强特征。在时序注意力计算中，查询 $Q$ 来自原始特征，键 $K$ 和值 $V$ 来自增强特征：

$$z'' = \mathrm{Attention}(Q, K, V) = \mathrm{Softmax}(QK^T)V$$

这一设计使生成帧能够直接关注参考帧中被扭曲到对应位置的内容，从而在保持内容一致性的同时合成大运动视频。此外，第二阶段采用选择性加噪策略，始终将干净的参考帧潜在码 $z_{ref}$ 与其他带噪潜在码沿时间轴拼接，进一步保持参考内容的保真度。

### 轨迹 ControlNet

为实现精细的运动控制，Motion-I2V 在第一阶段预训练模型的基础上训练了一个轨迹 ControlNet。该模块接收用户绘制的稀疏轨迹和对应的二值蒙版作为额外条件，输出稠密光流图。对于区域特定动画（运动刷），输入稀疏光流 $f_{sparse}$ 设为零图，蒙版 $m$ 中用户指定区域置为 0、其余区域置为 1，使未蒙版区域保持静止。

## 实验与分析

### 主实验结果

Motion‑I2V 在指令遵循能力与时序一致性两项核心指标上均优于对比方法。在 UCF‑101 与 MSR‑VTT 两个基准上，Motion‑I2V 取得了最高的 Prompt Consistency 得分 34.86 与最高的 Frame Consistency 得分 0.9871（Table 1）。与此同时，该方法的平均像素位移量达到 20.06，表明其在保持强时序一致性的前提下仍能生成较大幅度的运动。


![[assets/figures/papers/paper_list_l3_Motion_I2V_Consistent_and_Controllable_Image_to_Video_Generation_with_Ex/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison. Motion-I2V shows best instruction-following ability and temporal consistency. Meanwhile, Motion-I2V generates relatively large motions*

定性对比（Figure 8）进一步揭示出不同方法的运动‑一致性权衡。DynamiCrafter 与 Pika 1.0 倾向于生成极小运动的视频，避免了大位移带来的时序断裂，但牺牲了动态表现力。Gen‑2 虽然能生成与 Motion‑I2V 相当的大运动，却难以保持参考图像的身份特征，出现明显的形变。相比之下，Motion‑I2V 在大运动场景中成功维持了时序一致性，验证了显式运动建模对扩大有效时间感受野的关键作用。

### 消融实验

消融实验围绕两个核心设计展开：第一阶段运动场的必要性，以及扭曲特征注入方式（Table 2）。


![[assets/figures/papers/paper_list_l3_Motion_I2V_Consistent_and_Controllable_Image_to_Video_Generation_with_Ex/figures/009_Table_2.jpg]]
*Table 2: Ablation study. Utilizing the motion fields from stage 1 can significantly stabilize the prediction. Additionally, using attention to adaptively inject the warped features into synthesized frames can further increase consistency and avoid extreme distortions*

**运动场的作用。** 移除第一阶段预测的运动场后，模型直接依赖隐式时序注意力学习动态，视频生成的稳定性显著下降。这一结果支持了核心假设：显式运动场为第二阶段提供了强先验，使模型无需从零学习复杂的时空耦合模式。

**注意力融合 vs. 直接相加。** 在扭曲特征注入方式上，采用注意力机制自适应地注入扭曲特征，相比直接将扭曲特征与原始特征相加，Frame Consistency 进一步提升至 0.9871，且避免了极端失真。其因果机制在于：注意力允许模型根据当前帧的内容需求，动态决定从参考帧扭曲特征中获取多少信息，而非强制等权融合，从而在保持内容一致性的同时抑制了扭曲误差的累积。

### 失败模式与局限性

论文明确指出一个已知的失败模式：生成视频往往具有中等亮度。这一现象可能源于扩散模型的噪声调度未在最后时间步强制达到零信噪比，导致解码端出现亮度偏移。该问题在潜在扩散模型中较为常见，但论文未提供定量化程度分析或缓解方案。

### 图表核心结论

- **Table 1** 确立了 Motion‑I2V 在指令遵循、时序一致性和运动幅度三个维度的综合优势，构成全文定量证据的核心。
- **Table 2** 通过消融实验分离出运动场先验和注意力注入两个设计的独立贡献，为两阶段框架的有效性提供了因果证据。
- **Figure 8** 以定性方式直观展示了不同方法在大运动场景下的行为差异，补充了定量指标无法完全反映的身份保持和运动幅度权衡。

### 补充图表

![[assets/figures/papers/paper_list_l3_Motion_I2V_Consistent_and_Controllable_Image_to_Video_Generation_with_Ex/figures/004_Figure_5.jpg]]
*Figure 5: Examples of region-specific I2V. Users can precisely Specify the animated regions by motion brush (purple mask). Unmasked regions remains static*

![[assets/figures/papers/paper_list_l3_Motion_I2V_Consistent_and_Controllable_Image_to_Video_Generation_with_Ex/figures/005_Figure_6.jpg]]
*Figure 6: Combination of motion trajectories and motion brush. Motion-I2V supports the combined usage of motion brush and trajectory guidance*

![[assets/figures/papers/paper_list_l3_Motion_I2V_Consistent_and_Controllable_Image_to_Video_Generation_with_Ex/figures/006_Figure_4.jpg]]
*Figure 4: Examples of sparse trajectory guided I2V. Users can precisely control the synthesized motions by drawing one or multiple trajectories (red curved arrow)*


## 方法谱系与知识库定位

### 与已有方法的关系

Motion‑I2V 的核心设计动机源于对现有图像到视频（I2V）生成方法两个结构性不足的回应：**隐式运动学习的时序感受野受限**，以及**运动控制粒度的缺失**。主流 I2V 方法——如 **DynamiCrafter**（Xing et al., 2023）、**I2VGen‑XL**（Zhang et al., 2023）——以及商用系统 **Pika 1.0** 和 **Gen‑2**，均依赖视频潜在扩散模型中的一维时序自注意力来隐式地捕获动态。这类机制的有效感受野受限于注意力窗口和帧间特征相似度，当面对大位移或视角剧烈变化时，模型难以在远隔帧之间建立可靠的对应关系，导致内容漂移或运动幅度被人为压缩。

Motion‑I2V 将这一隐式学习过程**显式化并解耦为两个阶段**：先预测稠密的像素级运动轨迹，再利用这些轨迹引导参考帧特征向生成帧传播。这一思路与光流/轨迹引导的视频生成范式（如视频帧插值、视图合成中的前向扭曲）存在谱系关联，但其创新在于将运动预测建模为一个**条件视频扩散过程**，并将扭曲特征通过**运动增强时序注意力**注入生成模型，而非简单的相加或拼接。这种“预测‑传播”的两阶段架构，使得模型的时间感受野从局部的注意力窗口扩展到整个预测轨迹所覆盖的帧范围，从根本上缓解了大运动下的时序一致性问题。

在可控性维度上，Motion‑I2V 与 **VideoComposer**（Wang et al., 2023）等可控视频生成方法形成对比。VideoComposer 支持多种条件输入（如深度图、草图、运动向量），但其运动控制仍以全局或隐式条件为主。Motion‑I2V 则通过为第一阶段训练**稀疏轨迹 ControlNet**，首次在 I2V 场景中实现了**像素级、区域可指定的运动轨迹控制**——用户仅需绘制一条或多条稀疏轨迹（红色曲线箭头）并指定运动区域（运动刷，紫色蒙版），即可精确引导对应区域的运动方向和幅度，而未遮罩区域保持静止。这一交互范式更接近动画制作中的关键帧曲线和遮罩工具，显著降低了运动控制的表达成本。

### 适用边界与局限

Motion‑I2V 的两阶段设计在带来大运动一致性和精细控制能力的同时，也引入了若干适用边界：

1. **运动预测的误差传播**：第二阶段的视频渲染质量高度依赖第一阶段运动场预测的准确性。当参考图像包含复杂遮挡关系或非刚体形变时，前向扭曲可能产生空洞或伪影，而注意力融合机制虽能缓解这一问题，但无法完全消除极端失真。消融实验（Table 2）证实，直接使用随机运动场或移除扭曲特征注入会导致一致性显著下降，说明系统对运动预测精度存在硬性依赖。

2. **亮度偏置问题**：论文明确指出生成视频“往往具有中等亮度”，并将其归因于噪声调度未能在最后时间步强制达到零信噪比。这是一个与扩散模型采样调度相关的系统性偏差，可能限制该方法在高动态范围或暗光场景下的直接应用。

3. **长视频生成的未验证性**：当前实验主要验证了固定帧数（通常为 16 帧）的生成能力。两阶段框架在理论上支持通过预测更长轨迹来扩展生成长度，但论文未提供任意长视频生成的实验证据。轨迹累积误差和注意力机制的线性增长是否会成为瓶颈，仍属开放问题。

4. **三维场景与复杂动态的泛化**：显式运动建模目前限于二维像素轨迹。对于包含显著三维旋转、非平面运动或流体/烟雾等非刚性动态的场景，二维运动场能否充分表征真实物理运动，论文未作探讨。

### 开放问题

- 如何从噪声调度或后处理层面解决生成视频的亮度偏暗问题，是该方法的直接改进方向。
- 两阶段框架能否扩展至任意长视频生成并保持时序一致性，需要进一步验证轨迹预测的长期稳定性和注意力机制的可扩展性。
- 显式运动建模是否可以推广到三维场景表示（如 NeRF、3D Gaussian Splatting）或更复杂的物理动态生成，是该方法向三维生成领域延伸的关键问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Motion_I2V_Consistent_and_Controllable_Image_to_Video_Generation_with_Explicit_Motion_Modeling.pdf]]
