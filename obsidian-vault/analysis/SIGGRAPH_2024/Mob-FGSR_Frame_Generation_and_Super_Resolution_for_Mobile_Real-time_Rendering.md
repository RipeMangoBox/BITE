---
title: "Mob-FGSR: Frame Generation and Super Resolution for Mobile Real-time Rendering"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Mob_FGSR_Frame_Generation_and_Super_Resolution_for_Mobile_Real_time_Rendering.pdf
project_link: null
code_link: null
aliases:
- MF
- Mob-FGSR
tags:
- SIGGRAPH_2024
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过基于溅射的运动向量重建（无需神经网络或额外硬件）和轻量级手工设计模型，实现移动设备上的实时帧生成与超分辨率。
primary_logic: 利用二次运动假设和深度感知的溅射，结合原子操作与细化模块，能够仅从已渲染帧的颜色、深度和运动向量中高效重建精确的运动向量，从而支持在移动设备上进行高质量的帧插值/外推和超分辨率，并且运行时不使用神经网络。
claims:
- Mob-FGSR的帧生成模型在Unity场景上的PSNR/SSIM大幅超越其他轻量级方法，最低提升4.22dB和0.049 SSIM。
- 在Snapdragon 8 Gen 3上，帧生成仅需2.2ms (720P)，帧生成+超分辨率仅需2.3ms (1080P)，显著快于现有方法。
- Ours-SR在UE场景上的PSNR略优于TSR，且整体视觉质量逼近深度学习方法（DLSS/NSR等）。
- Unity scenes (SV, HA, ME, DP) 上 PSNR / SSIM = Ours-I/Ours-E (平均)
---

# Mob-FGSR: Frame Generation and Super Resolution for Mobile Real-time Rendering

> [!tip] 核心洞察
> 利用二次运动假设和深度感知的溅射，结合原子操作与细化模块，能够仅从已渲染帧的颜色、深度和运动向量中高效重建精确的运动向量，从而支持在移动设备上进行高质量的帧插值/外推和超分辨率，并且运行时不使用神经网络。

| 字段 | 内容 |
|------|------|
| 中文题名 | Mob-FGSR：面向移动实时渲染的帧生成与超分辨率框架 |
| 英文题名 | Mob-FGSR: Frame Generation and Super Resolution for Mobile Real-time Rendering |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](http://www.cad.zju.edu.cn/home/jin/Sig20241/Mob-FGSR.htm) |
| Topic | #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Mob-FGSR |
| Dataset | Unity scenes, UE scene, Snapdragon 8 Gen 3 |

> [!tip] 效果简介
> - Unity scenes (SV, HA, ME, DP) 上，PSNR / SSIM Ours-I/Ours-E (平均) vs 3DWarp, BSR, AFME (最佳者) (PSNR ≥ +4.22 dB, SSIM ≥ +0.049)。
> - UE scene (Bunker) 上，PSNR Ours-SR 30.85 vs TSR 29.07 (+1.78 dB)。
> - Snapdragon 8 Gen 3 上，Runtime (ms) Ours-SR 1.66 ms vs MNSS 12.84 ms (-11.18 ms (约7.7倍加速))。

## 概要

移动端GPU性能与功耗严重受限，现有超采样方案（DLSS、FSR等）依赖高端GPU的硬件光流或神经网络，无法直接在移动设备上实现高效的帧生成与超分辨率。Mob-FGSR提出了一种面向移动实时渲染的轻量级超采样框架，仅需前向渲染输出的颜色、深度和运动向量，通过基于溅射的运动向量重建、深度感知原子操作与细化模块，在不使用任何神经网络的前提下实现精确的像素级运动估计，同时支持帧插值、帧外推及其超分辨率变体共四种模式。

在Unity场景上，Mob-FGSR的帧生成模型PSNR/SSIM相较3DWarp、BSR、AFME等轻量级基线最低提升4.22 dB和0.049；在Unreal Engine场景上，其超分辨率模型PSNR略优于TSR（30.85 vs 29.07），视觉质量逼近DLSS 2等深度学习方法。在Snapdragon 8 Gen 3平台上，720P帧生成仅需2.2 ms，1080P帧生成+超分辨率仅需2.3 ms，显著快于现有方案。该方法的主要局限在于忽略着色变化计算，导致动态阴影、反射和透明物体场景下出现明显失真，且外推模式在去遮挡区域可能产生鬼影。

## 核心方法与创新机理

### 问题瓶颈与设计哲学

移动端GPU在功耗和算力上的严格限制，使得桌面级超采样方案（如DLSS、FSR 2）所依赖的硬件光流加速器或深度神经网络无法直接迁移。现有轻量级帧生成方法（如3DWarp、BSR、AFME）普遍存在运动估计精度不足、薄物体丢失、扭曲伪影等问题，而移动端超分辨率方案则受限于延迟渲染管线或计算开销。Mob-FGSR的核心设计哲学是：**在不引入任何神经网络推理的前提下，仅利用前向渲染管线天然输出的颜色、深度和运动向量，通过溅射（splatting）机制重建精确的像素级运动场，进而驱动帧生成与超分辨率**。

### 核心创新：基于溅射的运动向量重建

这是整个框架最关键的技术突破，也是与所有基线方法形成根本差异的“changed slot”。传统方法（如3DWarp）通过投影方式传递运动向量，在物体边缘和遮挡区域产生严重失真；BSR采用迭代优化但计算量大且仍丢失薄结构。Mob-FGSR的方案建立在两个关键假设之上：

**二次运动假设**：对于插值帧$I_\alpha^i$（$\alpha \in (0,1)$为时间参数），假设物体在连续三帧间做匀加速运动。给定I帧$F_0$和$F_1$的渲染数据，以$F_1$中像素位置$p_1$为参考，利用其运动向量$m_1$反向追踪到$F_0$中的位置$p_0$，再进一步回溯到$F_{-1}$中的位置$p_{-1}$。基于匀加速模型，可推导出物体在插值时刻$\alpha$的位置$p_\alpha$以及对应的双向运动向量$m_{0\to\alpha}$和$m_{1\to\alpha}$（见Figure 3）。外推帧$I_{1+\alpha}^e$的运动向量$m_{1\to 1+\alpha}$也由同一运动模型导出。这一假设避免了光流估计的复杂性，同时比线性运动假设更贴合渲染场景中的加速运动。

**深度感知的原子溅射**：计算得到的运动向量需要“写入”目标帧的像素网格。Mob-FGSR采用最近邻溅射（nearest-neighbor splatting），将每个源像素的运动向量分配到目标位置。关键挑战在于：多个源像素可能溅射到同一目标像素（尤其在物体边缘），产生冲突。框架引入**深度感知的原子操作**来解决：在溅射时比较各候选向量的深度值，仅保留来自最近深度表面的运动向量。这一机制无需显式的遮挡推理，却能在GPU上高效实现，且天然保持物体边界的运动不连续性。

**运动向量细化**：溅射产生的运动向量场存在网格状间隙（因最近邻分配导致部分像素未被覆盖）。细化模块通过检测这些空洞，利用邻域有效向量的插值进行填充。Figure 4展示了细化前后的运动向量场对比，间隙被有效消除，运动场完整性显著提升。这一步骤对后续图像扭曲的质量至关重要。

### 去遮挡填充策略

插值帧中，被前景遮挡的背景区域在$F_0$和$F_1$中分别可见，但在重建的运动向量场中可能缺失。Mob-FGSR针对插值和推外模式采用差异化策略：

- **插值模式**：利用双向运动向量的互补性。若某像素在$M_{0\to\alpha}$中缺失但在$M_{1\to\alpha}$中存在（或反之），则直接采用可用向量的反向投影进行填充。这种对称设计充分利用了插值场景的信息冗余。
- **外推模式**：由于仅依赖$F_1$的单向运动向量，去遮挡区域的信息天然缺失。框架采用简化方案——直接复用$F_1$中对应位置的运动向量进行填充，虽无法完美恢复遮挡区域的真实运动，但在移动端性能约束下是合理的折中。

### 图像重建与混合规则

获得目标帧的运动向量后，Mob-FGSR通过后向扭曲（backward warping）将I帧对齐到目标时刻。插值帧的生成涉及两个扭曲结果$I_{0\to\alpha}^w$和$I_{1\to\alpha}^w$的融合，核心是处理遮挡和着色变化：

$$
I_{\alpha}^{i}(r) = \begin{cases}
I_{0\to\alpha}^{w}(r), & \Delta D(r) > T_{D}, \\
I_{1\to\alpha}^{w}(r), & \Delta D(r) < -T_{D}, \\
\text{blend based on } \Delta B \text{ and } \alpha, & \text{otherwise}
\end{cases}
$$

其中$\Delta D(r)$为两帧扭曲后像素的深度差，$T_D$为深度阈值。当深度差超过阈值时，表明该像素在一帧中被遮挡，直接选择可见帧的扭曲结果。当深度差在阈值内时，进一步根据亮度差$\Delta B$和时间参数$\alpha$进行加权混合，以缓解着色变化（如动态光源）带来的闪烁。阈值$T_D = 0.0028$和$T_B = 0.13$通过数据驱动的优化确定。

### 超分辨率模块的无缝集成

Mob-FGSR的超分辨率模块以极低开销嵌入帧生成管线。其核心创新在于**基于查找表（LUT）的图像扭曲**：传统超分辨率需要在亚像素级别进行重采样，双三次插值虽质量尚可但计算开销较高。Mob-FGSR将重采样权重预计算并存储在一个$32 \times 32 \times 16$的LUT中——$32 \times 32$覆盖亚像素采样位置的空间，16个通道对应不同的采样模式。推理时，根据运动向量的小数部分直接查表获取权重，避免了运行时插值计算。

SR重建的混合公式为：

$$
q = a \cdot \frac{\sum_{s \in \Omega_{p}} (1 - b \cdot d_{s}) \cdot s}{n} + (1 - a) \cdot q^{w}
$$

其中$q$为当前高分辨率像素，$q^w$为历史帧扭曲到当前帧的像素，$\Omega_p$为当前低分辨率帧中对应位置的邻域样本集合，$d_s$为样本到中心的距离，$a$和$b$为可调参数。这一设计将时间抗锯齿（TAA）的思想融入超分辨率，通过历史帧信息的累积提升边缘平滑度和细节还原。

### 模块间的因果链路

整个管线的因果依赖关系清晰且紧凑：

1. **运动溅射**提供原始运动场估计，其精度直接决定后续所有模块的上限——若运动向量错误，扭曲和混合都无法挽救。
2. **细化与去遮挡填充**修复溅射的结构性缺陷，保证运动场的完整性和边界准确性。
3. **LUT扭曲**将运动场转化为像素重采样操作，其效率是移动端实时性的关键保障。
4. **像素混合**作为最终的质量守门员，通过深度和亮度感知的选择/融合策略，抑制遮挡区域的鬼影和着色变化导致的闪烁。

值得注意的是，整个管线完全避免了神经网络的前向推理，所有参数（LUT权重、混合阈值）虽通过离线学习获得，但推理时仅涉及查表、插值和简单算术运算，这使得框架可以在移动GPU上以极低功耗运行。这一“学习优化参数但不学习推理函数”的策略，是Mob-FGSR在移动端实现高质量实时超采样的核心工程智慧。

![[assets/figures/papers/paper_list_l22_http_www_cad_zju_edu_cn_home_jin_Sig20241_Mob_FGSR_htm/figures/003_Figure_2.jpg]]
*Figure 2: Framework overview. For interpolation, MVs reconstruction of the B-frame*

![[assets/figures/papers/paper_list_l22_http_www_cad_zju_edu_cn_home_jin_Sig20241_Mob_FGSR_htm/figures/014_Figure_9.jpg]]
*Figure 9: Example results of our extrapolation method on dynamic shadow (a), metal reflection (b), and a translucent object (c), with each compared to the reference image for clearer visibility. Our lightweight approach ignores costly shading calculations, which can cause low frame rate effects such as misaligned shadows, reflections, and translucent objects comparing with the reference (refer to red line indicators). Avoiding low frame rate inputs before frame generation can mitigate these issues. We recommend an input frame rate greater than 30 fps*

## 实验与关键发现

### 主实验结果

Mob-FGSR在Unity和Unreal Engine两类场景上进行了系统的定量与定性评估，覆盖帧生成（FG）和超分辨率（SR）两个核心任务。

**帧生成任务。** 在Unity场景（SV, HA, ME, DP）上，Ours-I（插值）和Ours-E（外推）在PSNR和SSIM上显著超越所有轻量级基线方法。与3DWarp、BSR、AFME中表现最佳者相比，PSNR提升幅度不低于4.22dB，SSIM提升不低于0.049（Tab. 2）。这一差距反映了基于溅射的运动向量重建在像素级运动估计精度上的核心优势——传统3DWarp的投影式方法产生“橡皮布”伪影，BSR丢失薄物体的运动信息，AFME则频繁出现扭曲失真（Fig. 7）。

在Unreal Engine场景（Bunker）上，帧生成任务中ExtraNet凭借深度学习模型预测着色变化，在动态阴影区域表现更准确（Fig. 8上方，红色线标注处）；而Mob-FGSR及其他轻量级方法均无法有效处理动态阴影，暴露了手工设计模型在着色变化建模上的固有短板。

**超分辨率任务。** Ours-SR在UE场景上PSNR达到30.85dB，优于TSR的29.07dB（+1.78dB，Tab. 3）。视觉质量方面，Ours-SR、Ours-ISR和Ours-ESR在Unity场景上一致生成高质量结果，虽略逊于基于深度学习的MNSS和NSR，但明显优于FSR 1（Fig. 7下方）。在UE场景上，TSR、FSR 2和Ours-SR均能产生可比的图像分辨率提升，但在快速运动物体的边缘处理上均存在困难；相比之下，DLSS 2生成的边缘更平滑，视觉质量更高（Fig. 8下方）。

**端到端联合方案。** Ours-ISR和Ours-ESR将帧生成与超分辨率串联，在Unity场景上的PSNR/SSIM同样大幅领先于3DWarp+FSR 1等组合基线（Tab. 2中Alice blue行）。

### 运行时效率

在Snapdragon 8 Gen 3移动SoC上的实测（Tab. 4）表明，Mob-FGSR具有显著的实时性优势：

- 帧生成（Ours-I/Ours-E）在720P下仅需约2.2ms；
- 帧生成+超分辨率（Ours-ISR/Ours-ESR）在1080P下仅需约2.3ms；
- Ours-SR单独运行仅需1.66ms，相比MNSS的12.84ms实现约7.7倍加速。

这一效率优势源于两个设计选择：完全摒弃神经网络推理，以及用基于LUT的图像扭曲替代传统插值。LUT方法在SSIM上（0.933）优于双线性插值（0.907），与双三次插值（0.931）持平，但运行时间更短（0.905ms vs 1.145ms），验证了手工优化在移动端的关键价值。

### 消融实验

**LUT采样策略消融。** 针对SR模块中图像扭曲的采样方式，对比了双线性插值、双三次插值和基于LUT的采样。结果表明，LUT方法在SSIM上比双线性高0.026，与双三次相当（0.933 vs 0.931），且运行时间比双三次减少约21%（0.905ms vs 1.145ms）。这一消融确认了LUT在质量-效率权衡上的帕累托最优性。

**阈值参数优化。** 插值混合规则中的深度差阈值$T_D$和亮度差阈值$T_B$通过深度学习框架优化，最终取值为$T_D = 0.0028$、$T_B = 0.13$。这些阈值直接控制去遮挡区域的像素选择策略（Eq. 1），其优化对减少鬼影伪影至关重要。

### 失败模式与边界条件

**着色变化失效。** Mob-FGSR的核心设计假设是忽略着色计算开销，仅依赖已渲染帧的颜色、深度和运动向量进行图像级操作。这一简化在动态阴影、金属反射和半透明物体上导致明显的失真：外推帧中的阴影位置与参考帧错位，反射内容滞后于几何运动，半透明物体的折射效果无法正确更新（Fig. 9）。论文建议输入帧率大于30fps以减轻低帧率下的着色滞后效应，但未从根本上解决着色变化预测问题。

**外推去遮挡伪影。** 外推模式（Ours-E）在去遮挡区域可能产生鬼影（Fig. 7蓝色框标注的龙翼右侧区域），其简化的去遮挡填充策略（直接复用I帧1的运动向量）在暴露的新区域缺乏真实的运动信息。论文建议配合插值策略使用以减轻该问题。

**快速运动边缘退化。** 在SR任务中，Mob-FGSR与TSR、FSR 2一样，在快速运动物体的边缘上表现不佳（Fig. 8下方），而DLSS 2通过深度学习生成了更平滑的边缘。这表明基于手工规则的SR方法在亚像素级细节重建上存在能力上限。

### 公平性说明

为与仅支持延迟渲染的TSR、FSR 2等方法公平对比，论文在UE场景中额外构建了测试环境。所有对比在相同输入分辨率、帧率和Snapdragon 8 Gen 3硬件条件下完成，运行时测量在同一设备上进行。

![[assets/figures/papers/paper_list_l22_http_www_cad_zju_edu_cn_home_jin_Sig20241_Mob_FGSR_htm/figures/010_Table_4.jpg]]
*Table 4: Runtime performance analysis. We report the inference times of our models on a modern mobile SoC (Snapdragon 8 Gen3) and compare them with alternative solutions*

![[assets/figures/papers/paper_list_l22_http_www_cad_zju_edu_cn_home_jin_Sig20241_Mob_FGSR_htm/figures/013_Figure_8.jpg]]
*Figure 8: Comparison of our method to supersampling baselines in UE scenes, including frame generation methods (3DWarp, BSR, ExtraNet) and SR methods (TSR, FSR 2, DLSS 2). In frame generation (upper section), ExtraNet employs a deep learning model to predict shading changes, offering more accurate shadow predictions (see red line indicators). On the contrary, other lightweight methods do not effectively handle dynamic shadows. In the SR task (lower section), TSR, FSR2, and our method all produce comparable improvements in image resolution. However, they have difficulty with the edges of fast-moving objects. In contrast, the deep learning approach (DLSS 2) generates smoother edges, resulting in higher...*

![[assets/figures/papers/paper_list_l22_http_www_cad_zju_edu_cn_home_jin_Sig20241_Mob_FGSR_htm/figures/005_Figure_3.jpg]]
*Figure 3: Motion estimation process. A green ball is thrown, tracing a trajectory marked at*

![[assets/figures/papers/paper_list_l22_http_www_cad_zju_edu_cn_home_jin_Sig20241_Mob_FGSR_htm/figures/011_Figure_7.jpg]]
*Figure 7: Comparison of our method to supersampling baselines in Unity scenes, including frame generation methods (3DWarp, BSR, AFME) and SR methods (FSR 1, MNSS, NSR). MSAA and TAA serve as frame generation and SR references, respectively. In frame generation (upper section), the Ours-I model provides accurate motion estimation while maintaining high image quality. The Ours-E model also produces comparable quality, but it occasionally deviates in motion estimation (see the dragon’s wingtip in the orange box) and produces artifacts in disocclusions (see the right region of dragon’s wingtip in the blue box). Baseline methods have several limitations, including ‘rubber sheet’ artifacts in 3DWarp, motio...*

## 定位与知识库关联

Mob-FGSR 在实时渲染超采样这一技术线上，改变的核心 slot 是**运动向量获取与图像重建的计算范式**：将运动估计从“基于投影/光流/神经网络”彻底转为“基于溅射的二次运动假设 + 深度感知原子操作”，同时将图像重建从“神经网络推理”转为“手工设计模型 + 查找表扭曲”。这一双重范式转换，使其在移动端实时渲染这个特定边界内，形成了一条与现有方法截然不同的技术路径。

**相对帧生成方法的差异。** 传统轻量级帧生成方法可归为两类：基于投影的 **3DWarp**（Mark et al., 1997）通过反向投影从前帧推导后帧运动，但会产生“橡胶片”伪影；基于迭代优化的 **BSR**（Yang et al., 2011）和 **AFME**（Holmes and Wicks, 2020）试图改善运动质量，却分别存在薄物体运动丢失和频繁扭曲的问题。这些方法的共同瓶颈在于运动向量的重建精度受限于投影几何假设或迭代收敛条件。Mob-FGSR 用溅射替代投影——将 I 帧的运动向量按二次运动假设直接“溅射”到目标帧的像素位置，并通过深度感知的原子操作解决边缘冲突，再经细化模块填充网格状间隙。这一改变的本质是**将运动估计从“目标帧主动查询”变为“源帧主动写入”**，从而在无神经网络、无专用硬件的条件下获得像素级精度的运动向量。

**相对超分辨率方法的差异。** 移动端可用的 SR 方案存在明显的分层：**FSR 1** 是纯空间上采样，质量有限；**TSR**（Epic 2022）和 **FSR 2**（AMD 2022）依赖延迟渲染的 G-buffer 和历史帧，不支持移动端主流的前向渲染管线；**DLSS 2**（Liu 2020）、**NSR**（Xiao et al., 2020）、**MNSS**（Yang et al., 2023）则依赖神经网络推理，在移动 GPU 上耗时过高（MNSS 需 12.84ms，而 Mob-FGSR 的 SR 仅需 1.66ms）。Mob-FGSR 改变的关键 slot 是**用基于查找表的扭曲替代神经网络重建**：将学习到的重采样权重编码进 32×32×16 的 LUT，在 backward warping 时直接查表，避免了 shader 中的复杂插值计算和神经网络推理。这使得 SR 模块可以无缝嵌入帧生成管线，且仅需前向渲染输出的颜色、深度和运动向量。

**知识库挂载点。** 本文在实时渲染知识库中的挂载位置是“移动端超采样”这一新兴子领域。其上游连接两条知识线：一是**基于运动向量的帧插值/外推**（从 3DWarp 到 ExtraNet 的演进），Mob-FGSR 以溅射重建替代了该线的运动估计环节；二是**时序超分辨率**（从 TAA 到 DLSS/FSR 的演进），Mob-FGSR 以无网络 LUT 方案替代了该线的重建网络。其下游可连接的方向包括：轻量级着色变化预测模块（解决动态阴影/反射/透明物体的失真）、NPU 加速的极轻量边缘细化网络（改善快速运动边缘的锯齿）、以及基于 G-buffer 引导的去遮挡填充改进（减少外推鬼影）。

**适用边界与局限。** Mob-FGSR 的设计前提是“忽略着色变化计算”，这一简化使其在动态阴影、金属反射和半透明物体上产生明显失真（见 Fig. 9），因为着色变化无法通过纯几何运动向量捕获。论文建议输入帧率不低于 30fps 以缓解该问题。外推模式在去遮挡区域仍有鬼影，实际部署中更适合插值为主的策略。此外，该方法假设前向渲染管线可用，且依赖引擎提供的深度和运动向量精度——在延迟渲染或运动向量质量较低的引擎中需额外适配。

**后续启发。** Mob-FGSR 证明了一个重要命题：在移动端的严格功耗和算力约束下，**用领域知识替代通用学习**（溅射替代光流网络，LUT 替代重建网络）可以同时获得质量逼近深度学习方法、速度远超传统方法的帕累托最优解。这一思路对移动端图形学的其他任务（如降噪、抗锯齿、帧预测）具有方法论层面的迁移价值。论文提出的三个开放问题——着色变化高效预测、更轻量去遮挡填充、极轻量神经网络辅助——也直接指向了该技术线的下一步演进方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Mob_FGSR_Frame_Generation_and_Super_Resolution_for_Mobile_Real_time_Rendering.pdf]]