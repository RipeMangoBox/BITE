---
title: "LUVE: Latent-Cascaded Ultra-High-Resolution Video Generation with Dual Frequency Experts"
type: paper
paper_level: A
venue: ICML
year: 2026
pdf_ref: paperPDFs/ICML_2026/LUVE_Latent-Cascaded_Ultra-High-Resolution_Video_Generation_with_Dual_Frequency_Experts.pdf
project_link: https://unicornanrocinu.github.io/LUVE_web/
code_link: https://github.com/NJU-PCALab/LUVE
aliases:
- LUVE
tags:
- ICML_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过在级联式三阶段框架中引入“双频专家”机制：在去噪过程的高噪声阶段注入对注意力模块施加低通滤波的低频专家，显式巩固全局语义结构；在低噪声阶段注入对前馈网络施加高通滤波的高频专家，精炼局部纹理细节；同时配合直接作用于潜空间的视频潜空间上采样器，以高效且保真的方式搭建从低分辨率运动先验到高分辨率内容增强的桥梁。
primary_logic: 视频扩散模型在去噪过程中遵循由低频到高频的逐步重建规律：干净信号首先出现在低频区域，再逐渐扩展至高频。据此，可将语义架构与纹理细节的生成按频带解耦，并通过在相应去噪阶段分别接入专用专家网络，实现结构一致性与感知细腻度的兼顾提升，同时利用可学习的潜空间映射规避传统RGB/Latent插值带来的伪影与计算开销。
claims:
- 在VBench基准上，LUVE取得最高的平均分84.34，显著优于Strong Baseline (Wan2.1-720p为82.98) 和同期UHR方法 (UltraWan, CineScale)。
- 消融实验证实，移除低频专家(LFE)会导致语义规划和内容保真度下降，移除高频专家(HFE)则会使纹理细节明显丢失，表明双频专家分别对全局语义和一局纹理起到了因果性增强作用。
- 功率谱密度(PSD)分析清晰显示，Wan2.1模型在去噪开始时优先重构低频结构，随后才转向高频细节，为双频专家在不同噪声阶段分工提供了理论依据。
- 与多种视频超分(VSR)方法相比，LUVE在MUSIQ、MANIQA、NIQE、DOVER等感知和美学指标上全面领先，表明其超越了简单的锐度提升，实现了更真实的语义和纹理修复。
---

# LUVE: Latent-Cascaded Ultra-High-Resolution Video Generation with Dual Frequency Experts

> [!tip] 核心洞察
> 视频扩散模型在去噪过程中遵循由低频到高频的逐步重建规律：干净信号首先出现在低频区域，再逐渐扩展至高频。据此，可将语义架构与纹理细节的生成按频带解耦，并通过在相应去噪阶段分别接入专用专家网络，实现结构一致性与感知细腻度的兼顾提升，同时利用可学习的潜空间映射规避传统RGB/Latent插值带来的伪影与计算开销。

| 字段 | 内容 |
|------|------|
| 中文题名 | LUVE：基于双频专家的潜空间级联超高清视频生成 |
| 英文题名 | LUVE: Latent-Cascaded Ultra-High-Resolution Video Generation with Dual Frequency Experts |
| 会议/期刊 | ICML 2026 |
| Links | [paper](https://arxiv.org/abs/2602.11564) · [Project](https://unicornanrocinu.github.io/LUVE_web/) · [Code](https://github.com/NJU-PCALab/LUVE) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | LUVE |
| Dataset | VBench, UHR Video Assessment, VSR methods comparison, Human Preference Study |

> [!tip] 效果简介
> - VBench (T2V Generation) 上，Average Score 84.34 (2K) / 84.03 (4K) vs 82.98 (Wan2.1-720p); 83.50 (UltraWan-1K) (↑ 1.36 (vs Wan2.1-720p))。
> - UHR Video Assessment (MLLM评价) 上，FID_patch / Realism / Detailness / Alignment 41.03 / 7.64 / 5.36 / 7.90 (2K); 39.87 / 7.46 / 5.40 / 7.80 (4K) vs 48.64 / 6.76 / 4.64 / 6.88 (UltraWan-4K) (FID_patch ▼ 8.77, Realism ↑ 0.88, Detail ↑ 1.16, Alignment ↑ 0.92 (4K))。
> - VSR methods comparison 上，MUSIQ / MANIQA / NIQE / DOVER 58.01 / 0.410 / 3.16 / 0.784 vs 56.54 / 0.402 / 3.20 / 0.755 (FlashVSR, best competitor) (MUSIQ ↑1.47, DOVER ↑0.029)。

## 概要

将现有文生视频（T2V）扩散模型直接扩展至超高清（UHR）场景时，面临一个根本性瓶颈：模型难以同时维系运动连贯性、全局语义规划与细粒度纹理的真实性，往往产生静态输出、物体重复或模糊纹理。基于视频超分（VSR）的后处理方法虽能提升视觉锐度，却无法引入新的语义内容，导致“伪高清”输出。LUVE 针对这一瓶颈，提出了一种基于**双频专家（Dual Frequency Experts）** 的潜空间级联框架，其核心洞察在于：视频扩散模型的去噪过程遵循由低频到高频的逐步重建规律——干净信号首先在低频区域出现，随后扩展至高频（见 Figure 6 的功率谱密度分析）。据此，LUVE 将语义架构的巩固与纹理细节的精炼按频带解耦，在去噪的高噪声阶段注入低频专家（LFE）以强化全局语义结构，在低噪声阶段注入高频专家（HFE）以精细化局部纹理，从而兼顾结构一致性与感知细腻度。

在 VBench 基准上，LUVE 取得平均分 **84.34**（2K）和 **84.03**（4K），显著优于强基线 Wan2.1-720p（82.98）及同期 UHR 方法 UltraWan 和 CineScale（Table 1）。与多种 VSR 方法相比，LUVE 在 MUSIQ、MANIQA、NIQE、DOVER 等感知与美学指标上全面领先，验证了其超越简单锐度提升的语义与纹理修复能力（Table 3）。用户偏好研究中，LUVE 在整体视频质量、细节质量、时序一致性和文本-视频对齐四个维度上均获得压倒性多数偏好（60%–64% vs. 最佳竞争者约 15%–17%，Table 4）。消融实验进一步证实，移除低频专家会导致语义规划与内容保真度下降，而移除高频专家则使纹理细节明显丢失，表明双频专家分别对全局语义与局部纹理起到了因果性增强作用（Table 6）。

在方法谱系上，LUVE 构建于预训练 T2V 模型 **Wan2.1**（Wan et al., 2025）之上，通过三阶段协作架构——低分辨率运动生成（LMG）、视频潜空间上采样（VLU）和高分辨率内容细化（HCR）——实现从低分辨率运动先验到高分辨率语义增强的保真映射。与 **UltraWan**（Xue et al., 2025）的微调范式及 **CineScale**（Qiu et al., 2025）的免训练推理策略不同，LUVE 的核心创新在于将频带分解显式嵌入扩散去噪过程，并配合可学习的视频潜空间上采样器（VLUer）规避传统 RGB/Latent 插值带来的伪影与计算开销。目前该方法仅在 Wan2.1-1.3B 骨干上得到验证，其在其他 DiT 架构（如 CogVideoX、HunyuanVideo）上的泛化性仍属开放问题。



### 超高清视频生成的现实需求与技术瓶颈

随着扩散模型在文生视频（T2V）领域的快速演进，生成视频的视觉质量与运动连贯性已取得长足进步。然而，当用户对分辨率的需求从常规高清（720p/1080p）跃迁至2K乃至4K的超高清（UHR）时，现有模型暴露出系统性的能力短板。直接将预训练T2V模型扩展至UHR场景，往往会导致三类典型的生成失败（Figure 2）：在**运动建模**层面，模型倾向于产生近乎静止的输出，无法捕捉连贯的时序动态；在**语义规划**层面，画面中出现全局或局部的物体重复，反映出模型对高分辨率画布上空间布局的理解不足；在**细节合成**层面，生成帧普遍存在运动模糊与纹理退化。这三重困境的根源在于，高分辨率视频的联合分布远比低分辨率复杂，模型在有限的计算与数据预算下难以同时维系运动、语义与纹理的真实性。

### 现有方案的局限：超分后处理与级联架构的“伪高清”陷阱

针对上述瓶颈，业界初步形成了两条技术路线。第一条路线是将UHR生成视为一个**后处理问题**，即先由T2V模型生成低分辨率视频，再借助视频超分（VSR）方法提升分辨率。代表性方法包括 **RealBasicVSR**（Chan et al., 2022）、**VEnhancer**（He et al., 2024）、**STAR**（Xie et al., 2025）和 **FlashVSR**（Zhuang et al., 2025）等。然而，VSR方法本质上只能增强视觉锐度，无法为画面引入新的语义内容——它们擅长恢复边缘和纹理，却无力修正生成阶段已固化的语义错误或补充缺失的物体结构，最终输出的是“伪高清”视频：清晰但语义贫瘠。

第二条路线是构建**级联式生成架构**，通过一个专门的高分辨率细化阶段来提升画质。但现有级联方法（Figure 3a）的目标函数几乎完全聚焦于细节增强，忽视了高分辨率阶段同样需要维护甚至强化全局语义一致性的需求。当细化网络仅被训练去锐化纹理时，它缺乏足够的驱动力去修复低分辨率阶段遗留的语义偏差，导致输出视频虽然细节更清晰，但整体语义规划仍停留在低分辨率水平。

### 核心洞察：扩散去噪的频率演化规律

本研究的关键理论洞察来自对扩散模型去噪过程的频率域分析。通过对 **Wan2.1**（Wan et al., 2025）模型中间潜变量的功率谱密度（PSD）进行测量（Figure 6），一个清晰的频率演化规律被揭示：在去噪的早期阶段（高噪声水平），干净的潜信号首先在低频区域涌现，构建起视频的全局语义骨架；随着去噪推进至后期（低噪声水平），信号能量才逐渐向高频带扩展，填充纹理和局部细节。这一“先低频、后高频”的逐步重建规律表明，**扩散模型的去噪轨迹天然地将语义架构的生成与纹理细节的生成按频带解耦**。

这一发现直接指向了现有方法的症结：无论是VSR后处理还是传统级联细化，都未能在生成过程中显式地利用频带分工。若能在高噪声阶段有针对性地巩固低频语义结构，并在低噪声阶段专门精炼高频纹理信息，则有望同时突破语义一致性与感知细腻度的瓶颈。这正是LUVE框架设计的理论出发点——通过“双频专家”机制，将语义与纹理的生成责任按去噪阶段解耦，实现结构保真与细节丰富的兼顾。



## 核心方法与创新机理

LUVE 的核心创新并非提出一种全新的生成范式，而是**精确诊断了现有视频扩散模型在超高清（UHR）扩展中的瓶颈，并据此设计了一套高度解耦且可插拔的频带增强机制**。其关键 changed slots 可归纳为以下三个维度。

### 1. 从“像素/潜空间插值”到“可学习的潜空间隐式上采样”

传统级联框架在衔接低分辨率运动先验与高分辨率生成时，普遍采用 RGB 插值或 Latent 插值（Figure 4a, 4b）。这类无参放大会在潜空间中引入结构性失真，迫使后续扩散模型在去噪时额外消耗容量去“修复”这些伪影，而非专注于语义与细节的生成。

LUVE 将这一 slot 替换为**基于隐式神经表示（INR）的视频潜空间上采样器 VLUer**。其核心操作可形式化为：

$$\hat{z}(x, y, t) = \text{Decoder}(U(F, Q(x, y, t)))$$

该模块在潜空间内直接完成任意倍率上采样，完全规避了 VAE 编解码带来的计算开销与信息损失。为保障重建质量，训练时引入了像素空间的联合损失：

$$\mathcal{L}_{pixel} = \mathcal{L}_{1}(x_{sr}, x_{hr}) + \mathcal{L}_{frame}(x_{sr}, x_{hr})$$

其中帧差损失 $\mathcal{L}_{frame}$ 显式约束相邻帧的变化量与真实高分辨率视频一致，有效抑制了时序闪烁。消融实验证实，移除解码器会导致画面模糊，移除像素损失则会产生块状伪影（Figure 5），而 VLUer 在 FID_patch、Realism 和推理延迟上全面优于 RGB/Latent 插值（Table 5）。

### 2. 从“无差别细节增强”到“双频专家解耦生成”

现有高分辨率阶段通常仅对整体画面进行无差别的细节增强（Figure 3a），忽略了扩散模型去噪过程中**由低频到高频的逐步重建规律**。LUVE 通过功率谱密度（PSD）分析揭示了这一关键现象：干净信号首先出现在低频区域，随后才扩展至高频（Figure 6）。

基于此，LUVE 将频率增强模块拆解为两个独立且互补的专家：

- **低频专家（LFE）**：在去噪的高噪声阶段（$t \in [t_{switch}, 1]$）注入，作用于冻结的 Attention 模块，其输入经低通滤波后通过 LoRA 分支增强，显式巩固全局语义结构：
  $$\mathbf{y} = \text{Attention}(\mathbf{x}) + \text{LoRA}(\text{LowPass}(\mathbf{x}))$$

- **高频专家（HFE）**：在去噪的低噪声阶段（$t \in [0, t_{switch}]$）注入，作用于冻结的 FFN 模块，其输入经高通滤波后通过 LoRA 分支精炼局部纹理细节：
  $$\mathbf{y} = \text{FFN}(\mathbf{x}) + \text{LoRA}(\text{HighPass}(\mathbf{x}))$$

消融实验为这一解耦设计提供了因果性证据：移除 LFE 会导致语义规划和内容保真度显著下降，交叉注意力图显示模型注意力在宽广画布上严重分散；移除 HFE 则使纹理细节明显丢失（Table 6, Figure 12）。完整的双频配置在内容保真度与感知质量上均显著优于单纯 UHR 缩放或标准 LoRA 专家。

### 3. 从“无差别数据训练”到“频率感知的数据筛选与增强”

与双频专家的分工相匹配，LUVE 对训练数据施加了频率感知的差异化处理：

- **LFE 训练数据**：使用 HPS v3 评分筛选（阈值 > 6.5），仅保留高美学质量的样本，确保低频专家学到的是优质的全局语义先验。
- **HFE 训练数据**：在筛选后的子集上进一步施加 Unsharp Masking 增强，显式提升高频信息密度，使高频专家能接触到更丰富的纹理信号进行学习（Figure 8）。

这一数据策略与模块设计的协同，使得双频专家各自在最优信号条件下完成专项训练，是性能提升的重要支撑。

### 创新点总结

LUVE 的创新本质在于**将视频扩散模型的频率演化规律转化为可工程化的模块解耦方案**：用 VLUer 解决上采样阶段的伪影引入问题，用双频专家解决高分辨率阶段的语义-纹理兼顾问题，并用频率感知的数据策略保障各模块的训练效率。三者协同，使 LUVE 在 VBench 上以 84.34 的平均分显著超越 Wan2.1-720p（82.98）和同期 UHR 方法 UltraWan（83.50），在人类偏好研究中亦取得压倒性优势（Table 1, Table 4）。



LUVE 采用三阶段级联架构，将超高清视频生成任务分解为 **低分辨率运动生成 (LMG)**、**视频潜空间上采样 (VLU)** 与 **高分辨率内容细化 (HCR)** 三个协同阶段，以解决现有方法在直接扩展至超高清时面临的运动静止、语义重复与纹理退化三重困境（Figure 2）。

### 设计动机与范式差异

现有级联式高分辨率视频生成架构通常将低分辨率输出作为初始值，在高分辨率阶段仅进行细节增强，忽视了语义内容的保真度。LUVE 的核心范式转变在于：**高分辨率阶段应同时强化语义一致性与细粒度纹理生成**，而非简单的锐化后处理（Figure 3a-b）。

### 三阶段 Pipeline

**阶段一：低分辨率运动生成 (LMG)**
以预训练文本到视频模型 **Wan2.1-1.3B** (Wan et al., 2025) 为骨干，在标准分辨率下生成低分辨率视频潜变量 $z_{lr}$。该阶段的核心目标是提供可靠的**运动先验**，确保后续高分辨率合成具备连贯的时间动态。

**阶段二：视频潜空间上采样 (VLU)**
通过提出的轻量级视频潜空间上采样器 **VLUer**，直接在潜空间中执行分辨率提升，生成高分辨率潜变量 $\hat{z}_{hr}$。VLUer 由编码器、基于隐式神经表示的上采样器与解码器构成：
$$\hat{z}(x, y, t) = \text{Decoder}(U(F, Q(x, y, t)))$$
该设计规避了传统 RGB 插值或 Latent 插值引入的伪影与 VAE 编解码带来的计算开销（Figure 4）。

**阶段三：高分辨率内容细化 (HCR)**
以 $\hat{z}_{hr}$ 为初始值进行扩散去噪，在此过程中注入**双频专家**机制：
- **高频噪声阶段** ($t \in [t_{\text{switch}}, 1]$，$t_{\text{switch}}=0.417$)：低频专家 (LFE) 对注意力模块输入施加低通滤波，通过 LoRA 增强全局语义结构。
- **低频噪声阶段** ($t \in [0, t_{\text{switch}}]$)：高频专家 (HFE) 对前馈网络输入施加高通滤波，通过 LoRA 精炼局部纹理细节。

该分工的理论依据来自功率谱密度分析：Wan2.1 在去噪过程中呈现**先恢复低频结构、后补全高频细节**的规律（Figure 6）。

### 数据策略

双频专家的训练数据采用差异化筛选：
- **LFE 训练数据**：使用 HPS v3 评分筛选 (>6.5)，确保语义与美学质量。
- **HFE 训练数据**：在筛选子集上额外施加 Unsharp Masking 增强高频信息，为纹理细化提供更丰富的监督信号（Figure 8）。

### 推理流程

给定文本提示，LMG 生成低分辨率运动潜变量；VLUer 将其上采样至目标分辨率；HCR 阶段以跳跃步数 $S=5$ 进行去噪细化（Table 7 消融验证此为质量-效率最优平衡点），最终通过 VAE 解码器输出超高清视频。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the LUVE framework. (a) and (b) illustrate the core distinction between existing cascaded high-resolution video generation architectures and our proposed paradigm. While previous methods focus on high-resolution detail refinement, our approach prioritizes high-resolution content and semantic fidelity. (c) Our LUVE, which consists of three collaborative stages: low-resolution motion generation (LMG), video latent upsampling (VLU), and high-resolution content refinement (HCR)*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/001_Figure_1.jpg]]
*Figure 1: The base corresponds to the pretrained T2V model used in the first stage of our framework (Wan et al., 2025). As shown, compared with existing VSR methods, our model not only produces videos that are noticeably sharper and richer in fine details, but more importantly, it significantly enhances semantic consistency and plausibility. This demonstrates that UHR generation goes beyond merely enhancing visual sharpness—it fundamentally advances semantic coherence and content fidelity. (Zoom-in for best view)*



### 整体框架：三阶段级联架构

LUVE 采用三阶段级联式架构，将超高清视频生成分解为三个协同模块：**低分辨率运动生成（LMG）**、**视频潜空间上采样（VLU）** 和 **高分辨率内容细化（HCR）**。该设计源于一个关键观察：现有级联方法在高分辨率阶段仅关注细节增强，而 LUVE 将高分辨率阶段重新定位为**语义保真与内容增强**（Figure 3）。

- **LMG**：基于预训练 Wan2.1 生成低分辨率视频潜变量，为后续合成提供可靠的运动先验。
- **VLU**：通过轻量级视频潜空间上采样器（VLUer）直接在潜空间中进行任意倍率的上采样，规避传统 VAE 编解码带来的计算开销与伪影。
- **HCR**：利用双频专家机制，在扩散去噪的不同噪声阶段分别强化全局语义一致性与局部纹理细节。

### 核心模块一：视频潜空间上采样器（VLUer）

传统上采样方案存在根本性缺陷：RGB 插值需反复经过 VAE 编解码，引入严重计算负担；潜空间插值则因潜变量的非光滑性导致重建质量下降（Figure 4）。VLUer 通过隐式神经表示（INR）架构直接在潜空间内完成上采样，核心公式为：

$$\hat{z}(x, y, t) = \text{Decoder}(U(F, Q(x, y, t)))$$

其中 $F$ 为编码器从低分辨率潜变量提取的特征，$Q(x, y, t)$ 对目标高分辨率坐标进行查询，$U$ 为 INR 上采样器，Decoder 将上采样后的特征映射回潜空间。该模块由三个组件构成：编码器、视频 INR 上采样器和解码器。

为增强 RGB 空间保真度与时序一致性，VLUer 训练时引入像素空间联合损失：

$$\mathcal{L}_{pixel} = \mathcal{L}_{1}(x_{sr}, x_{hr}) + \mathcal{L}_{frame}(x_{sr}, x_{hr})$$

其中帧差损失显式约束相邻帧变化与真实高分辨率视频一致：

$$\mathcal{L}_{frame}(x_{sr}, x_{hr}) = \frac{1}{n-1} \sum_{t=2}^{n} \| \Delta x_{sr}^{(t)} - \Delta x_{hr}^{(t)} \|_1$$

消融实验证实，移除解码器会导致画面模糊（PSNR_rgb 降至 26.02），移除像素损失则产生块状伪影（PSNR_rgb 降至 29.09），完整 VLUer 达到 29.42（Table 12）。

### 核心模块二：双频专家（Dual Frequency Experts）

双频专家的设计动机源于对扩散去噪过程频率演化规律的理论分析。对 Wan2.1-1.3B 模型中间潜变量的功率谱密度（PSD）分析揭示了一个清晰的频率递进模式：干净信号首先在低频区域涌现，随后逐步向高频带扩展（Figure 6）。据此，LUVE 将语义架构与纹理细节的生成按频带解耦，在去噪的不同阶段注入专用专家网络。

#### 低频专家（LFE）

在扩散去噪的高噪声阶段（$t \in [t_{switch}, 1]$），LFE 对注意力模块的输入施加低通滤波，通过 LoRA 增强模型对全局语义结构的捕获：

$$\mathbf{y} = \text{Attention}(\mathbf{x}) + \text{LoRA}(\text{LowPass}(\mathbf{x}))$$

LFE 仅集成于冻结的注意力模块中，其低通滤波操作抑制高频噪声干扰，使模型在高噪声阶段专注于巩固语义布局和内容规划。交叉注意力图分析（Figure 12）显示，缺少 LFE 时模型注意力在宽广画布上严重分散，而 LFE 可使注意力高度集中并维护全局语义连贯性。

#### 高频专家（HFE）

在扩散去噪的低噪声阶段（$t \in [0, t_{switch}]$），HFE 对前馈网络（FFN）的输入施加高通滤波，通过 LoRA 精细化纹理和局部细节：

$$\mathbf{y} = \text{FFN}(\mathbf{x}) + \text{LoRA}(\text{HighPass}(\mathbf{x}))$$

HFE 仅集成于冻结的 FFN 模块中，其高通滤波操作提取边缘和纹理信息，使模型在低噪声阶段专注于细节生成。消融实验（Table 6）证实：移除 LFE 导致内容保真度下降，移除 HFE 则使纹理细节明显丢失，验证了双频专家分别对全局语义和局部纹理起到的因果性增强作用。

#### 切换时间步与数据策略

双频专家的切换时间步设为 $t_{switch} = 0.417$。训练数据方面，LFE 使用 HPS v3 评分筛选（阈值 > 6.5）的高质量样本以保证语义和美学质量；HFE 则在此基础上额外使用 Unsharp Masking 增强高频信息（Figure 8），为纹理精炼提供更丰富的训练信号。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/009_Figure_8.jpg]]
*Figure 8: Data Selection and Augmentation. (a) First row: low-HPS V3 scores; second row: high-HPS V3 scores. (b) First row: original data; second row: Unsharp Masking-enhanced data*

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/007_Figure_7.jpg]]
*Figure 7: (a) The architecture of the low-frequency expert. (b) The architecture of the high-frequency expert*



## 实验与关键发现

### 主实验：VBench基准评估

LUVE在VBench综合基准上取得了**84.34（2K）和84.03（4K）**的平均分，显著超越基础模型**Wan2.1-720p**（82.98）以及同期UHR方法**UltraWan-1K**（83.50）和**CineScale**（83.03）。该结果（Table 1）表明，级联式三阶段框架配合双频专家机制，在运动连贯性、语义规划与细节保真度三个维度上实现了协同提升，而非简单的分辨率缩放。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison on VBench. Compared with recent SOTA methods, LUVE demonstrates a substantial improvement in generative capability*

在针对UHR场景的专属评估中（Table 2），LUVE以**FID_patch 39.87、Realism 7.46、Detailness 5.40、Alignment 7.80**（4K）全面领先UltraWan-4K（48.64 / 6.76 / 4.64 / 6.88）。FID_patch采用256×256局部块测量，有效捕捉了高分辨率下的局部纹理退化；Realism和Detailness由MLLM评估，直接反映感知真实性与细节丰富度。Alignment的提升（↑0.92）证实LUVE并非仅增强锐度，而是真正改善了语义内容与文本提示的对齐。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/012_Table_2.jpg]]
*Table 2: Quantitative comparison for UHR video assessment*

### 与视频超分方法的对比

将LUVE与四种代表性VSR方法（**RealBasicVSR**、**VEnhancer**、**STAR**、**FlashVSR**）对比（Table 3），LUVE在MUSIQ（58.01 vs. 56.54）、MANIQA（0.410 vs. 0.402）、NIQE（3.16 vs. 3.20）和DOVER（0.784 vs. 0.755）上均取得最优。这一结果验证了核心洞察：UHR生成超越视觉锐度增强，需在生成过程中注入新的语义内容——这正是基于超分的后处理方法无法实现的“伪高清”瓶颈。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/011_Table_3.jpg]]
*Table 3: Quantitative comparison with VSR methods*

用户偏好研究（Table 4）进一步强化了上述结论。在整体视频质量、细节质量、时序一致性和文本-视频对齐四个维度上，LUVE分别获得**63.50%、60.33%、62.25%、61.08%**的压倒性偏好率，远超最优竞争者STAR（15.67%~16.50%）。所有得分均通过置信区间检验（Table 13），具有统计显著性。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/014_Table_4.jpg]]
*Table 4: User study evaluation*

### 消融实验

#### 上采样策略（Table 5）

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/016_Table_5.jpg]]
*Table 5: Ablation study with different upsampling*

对比RGB插值、Latent插值与提出的**VLUer**，VLUer在FID_patch（41.03）、Realism（7.64）和美学质量AQ（59.78）上全面领先，同时推理延迟仅**0.922秒**。RGB插值虽在PSNR_rgb上略高（29.42 vs. 29.09），但会产生严重块状伪影（Figure 5）；Latent插值则导致画面模糊。VLUer通过隐式神经表示直接在潜空间上采样，规避了VAE编解码的计算开销与伪影引入。移除解码器（w/o Decoder）导致PSNR_rgb降至26.02，画面模糊；移除像素损失（w/o Pixel Loss）则出现明显块状伪影（PSNR_rgb 29.09），证实了这两个组件对重建质量的关键作用（Table 12）。

#### 双频专家（Table 6）

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/017_Table_6.jpg]]
*Table 6: Ablation study with dual experts*

完整的双频专家配置（LFE+HFE）相较于单纯UHR缩放（w/o Experts）和标准LoRA专家，在内容保真度与感知质量上均有显著提升。单独移除低频专家（w/o LFE）导致语义规划能力下降，交叉注意力图分析（Figure 12）显示模型注意力在宽广画布上严重分散；单独移除高频专家（w/o HFE）则使纹理细节明显丢失。这验证了频段解耦设计的因果性：**LFE在高噪声阶段（$t \in [t_{switch}, 1]$）巩固全局语义结构，HFE在低噪声阶段（$t \in [0, t_{switch}]$）精炼局部纹理**。

数据策略的消融进一步表明，对LFE使用HPS v3筛选（阈值>6.5）保证了语义/美学质量，对HFE额外使用Unsharp Masking增强高频信息则显著提升了细节丰富度（Figure 8）。

#### 跳过步数与效率（Table 7）

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/019_Table_7.jpg]]
*Table 7: Ablation study with different skipped steps*

在高分辨率内容细化阶段跳过**S=5步**在生成质量与效率间取得最佳平衡。跳过步数过少（S=0）导致静态输出或语义错误，过多（S=10）则丢失细节（Figure 13）。效率对比（Table 8）显示，LUVE在4K视频生成上的推理时间和内存消耗均优于UltraWan和CineScale，但生成4K视频仍需约**91分钟**，是当前方法的主要效率瓶颈。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2602_11564/figures/020_Table_8.jpg]]
*Table 8: Efficiency comparison with UHR video generation models on 4K video generation*

### 失败模式与局限

尽管LUVE在多数场景下表现优异，但在极端复杂的物理交互场景（如流体飞溅、多物体严重遮挡）中，仍可能出现局部语义错误或运动不连贯。用户研究中少数案例反映了这一问题。此外，双频专家的性能高度依赖数据筛选阈值（HPS v3>6.5）和切换时间步（$t_{switch}=0.417$），这些超参数可能需要针对不同基础模型重新调优。目前仅在Wan2.1-1.3B骨干上验证，其在其他DiT架构（如CogVideoX、HunyuanVideo）上的泛化性尚未得到充分探究。



## 定位与知识库关联

### 1. 与现有方法的谱系关系

LUVE 处于**文本到视频（T2V）扩散模型**与**视频超分辨率（VSR）**两条技术路线的交汇点，但其核心范式与两者均有本质区别。

**与 T2V 扩散模型的关系。** LUVE 以 **Wan2.1**（Wan et al., 2025）为骨干，继承了其运动先验生成能力，但针对直接扩展至超高清（UHR）场景时暴露的三类瓶颈——运动静止、语义重复、纹理退化（Figure 2）——进行了结构性改造。与 **UltraWan**（Xue et al., 2025）这类通过微调将 Wan2.1 直接适配到 UHR 的方案不同，LUVE 不试图让单一模型同时承担运动生成与高分辨率内容合成，而是将其解耦为级联三阶段框架（LMG→VLU→HCR），使得低分辨率阶段专注运动连贯性，高分辨率阶段专注内容增强。与 **CineScale**（Qiu et al., 2025）这类免训练的推理策略不同，LUVE 引入了可学习的潜空间上采样器和双频专家，从而具备生成新语义内容的能力，而非仅对现有信号进行重分布。

**与视频超分辨率（VSR）方法的关系。** LUVE 与 **RealBasicVSR**（Chan et al., 2022）、**VEnhancer**（He et al., 2024）、**STAR**（Xie et al., 2025）、**FlashVSR**（Zhuang et al., 2025）等 VSR 方法在目标上部分重叠——均追求高分辨率视频的视觉质量提升——但技术逻辑截然不同。VSR 方法本质上是对已生成的低分辨率视频进行后处理增强，受限于输入信号的语义信息上限，仅能提升视觉锐度，无法修复缺失的语义内容或纠正结构错误（即“伪高清”问题）。LUVE 则在高分辨率阶段通过双频专家主动生成新的语义细节：低频专家（LFE）在去噪前期巩固全局语义架构，高频专家（HFE）在去噪后期精炼局部纹理。Table 3 的定量对比证实，LUVE 在 MUSIQ（58.01 vs. 56.54）、DOVER（0.784 vs. 0.755）等感知和美学指标上全面超越最强 VSR 基线 FlashVSR，表明其超越了简单的锐度提升，实现了更真实的语义修复。

**在级联生成框架谱系中的定位。** 传统级联视频生成框架（如 Figure 3(a) 所示）通常将高分辨率阶段设计为细节增强模块，对低分辨率输出进行补全。LUVE 将这一范式升级为“语义保真型级联”（Figure 3(b)），使高分辨率阶段不仅增强细节，更主动参与语义一致性的维护——这一转变通过双频专家在不同去噪阶段的分工实现，是该工作在方法谱系中的核心区分点。

### 2. 适用边界与局限

**适用场景。** LUVE 在以下条件下表现出显著优势：(1) 需要从文本描述直接生成 2K-4K 超高清视频，且对语义一致性和纹理真实性有较高要求；(2) 基础 T2V 模型（如 Wan2.1）在常规分辨率下已具备较好的运动建模能力，可作为可靠的运动先验源；(3) 存在高质量标注数据（HPS v3 > 6.5）用于训练双频专家。

**已知局限。**

- **推理效率瓶颈。** 生成 4K 视频的推理时间长达 91 分钟（Table 8），远未达到实时或交互式应用的要求。尽管 VLUer 的上采样延迟仅为 0.922 秒（Table 5），但高分辨率内容细化阶段的扩散采样占据了绝大部分时间开销。
- **超参数敏感性。** 双频专家的性能高度依赖数据筛选阈值（HPS v3 > 6.5）和切换时间步（$t_{\text{switch}} = 0.417$）。这些超参数是基于 Wan2.1-1.3B 的 PSD 分析（Figure 6）和实证调优确定的，迁移至其他基础模型时可能需要重新标定。
- **架构泛化性未验证。** 目前仅在 Wan2.1-1.3B 这一 DiT 骨干上进行了完整验证，其在 **CogVideoX**、**HunyuanVideo** 等其他 DiT 架构上的表现尚不明确。双频专家对注意力模块和 FFN 模块的注入方式依赖于 DiT 的标准结构，若目标架构的模块划分不同，需要重新设计注入点。
- **极端物理场景的残差错误。** 用户研究中少数案例显示，在涉及流体飞溅、多物体严重遮挡等极端物理交互场景下，仍可能出现局部语义错误或运动不连贯。这表明双频专家的频带解耦策略在处理高度非线性的时空耦合现象时存在能力边界。

### 3. 开放问题

1. **跨任务迁移性。** 该潜空间级联与双频专家范式是否能无缝迁移至文生图（T2I）或 UHR 图像生成任务？图像生成不存在时序维度，频带分解是否需要调整（例如仅保留空间频率处理）？
2. **推理效率的阶跃式压缩。** 能否通过模型蒸馏、一致性轨迹模型或更高效的注意力机制（如 FlashAttention 的进一步优化）将 4K 生成时间压缩至分钟级以内？Table 7 显示跳过 5 步（S=5）可在质量与效率间取得平衡，但更激进的步数压缩是否可行？
3. **数据依赖的弱化路径。** 当前 LFE 和 HFE 的训练分别依赖 HPS v3 筛选的高质量数据和 Unsharp Masking 增强的高频数据。能否采用弱标注或无标注的大规模 UHR 视频进行自监督训练，降低数据策展成本？
4. **自适应频率调控。** 双频专家的切换时间步 $t_{\text{switch}}$ 目前是全局固定的。能否根据内容复杂度（如场景纹理丰富度、运动剧烈程度）动态调整频率滤波的强度或作用区间，实现更精细的生成控制？
5. **时域频带分解。** 当前双频专家仅对空间维度施加频带处理（LFE 对注意力输入做低通滤波，HFE 对 FFN 输入做高通滤波）。若将时间域也纳入频带分解——例如将运动模式分为低频的全局运动趋势和高频的局部抖动——是否能进一步提升动态场景的真实性？这需要重新设计时域滤波算子和对应的专家注入机制。

---

> **注意：** 上述局限中的“极端物理场景残差错误”和开放问题中的“自适应频率调控”“时域频带分解”等条目来自分析推断，原文未提供对应的定量消融或理论分析，需在后续研究中手动验证。



## 原文 PDF

![[paperPDFs/ICML_2026/LUVE_Latent-Cascaded_Ultra-High-Resolution_Video_Generation_with_Dual_Frequency_Experts.pdf]]
