---
title: "DiffusionHarmonizer: Bridging Neural Reconstruction and Photorealistic Simulation with Online Diffusion Enhancer"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DiffusionHarmonizer_Bridging_Neural_Reconstruction_and_Photorealistic_Simulation_with_Online_Diffusion_Enhancer.pdf
code_link: null
project_link: https://research.nvidia.com/labs/sil/projects/diffusion-harmonizer/
aliases:
- DiffusionHarmonizer
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "将多步扩散模型转换为确定性单步增强器，配合多尺度感知损失与精心构建的合成数据管线，从而在单GPU上实现实时、时序一致的增强。"
primary_logic: "通过冻结编码器/解码器、微调扩散骨干（加入时序注意力），并采用多尺度感知损失抑制单步微调产生的棋盘伪影，结合涵盖伪影校正、色调协调、重光照和阴影生成的多样化合成数据，DiffusionHarmonizer首次实现了满足在线模拟要求的统一增强框架。"
claims:
- "用户研究中，84.28% 的参与者偏好 DiffusonHarmonizer 的效果优于第二强基线。"
- "在多个评测数据集上，其 FID、FVD、PSNR、SSIM、LPIPS 均大幅超越通用编辑模型和专用 harmonization 方法。"
- "消融实验证实，多尺度感知损失是抑制单步训练高频伪影的关键，而数据管线的每一部分都为模型提供不可替代的监督信号。"
- "Novel Trajectory Simulation (In-domain) 上 FID ↓ = 120.23"
---

# DiffusionHarmonizer: Bridging Neural Reconstruction and Photorealistic Simulation with Online Diffusion Enhancer

> [!tip] 核心洞察
> 通过冻结编码器/解码器、微调扩散骨干（加入时序注意力），并采用多尺度感知损失抑制单步微调产生的棋盘伪影，结合涵盖伪影校正、色调协调、重光照和阴影生成的多样化合成数据，DiffusionHarmonizer首次实现了满足在线模拟要求的统一增强框架。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DiffusionHarmonizer：连接神经重建与逼真模拟的在线扩散增强器 |
| 英文题名 | DiffusionHarmonizer: Bridging Neural Reconstruction and Photorealistic Simulation with Online Diffusion Enhancer |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.24096) · [Project](https://research.nvidia.com/labs/sil/projects/diffusion-harmonizer/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DiffusionHarmonizer |
| Dataset | Novel Trajectory Simulation (In-domain), Object Insertion Simulation (Out-of-domain), ISP Modification (Harmonization) |

> [!tip] 效果简介
> - Novel Trajectory Simulation (In-domain) 上，FID ↓ 为 120.23，对比 129.92 (SDEdit SD3)，变化 -9.69。
> - Novel Trajectory Simulation (In-domain) 上，FVD ↓ 为 470.11，对比 506.86 (Wan-Video V2V)，变化 -36.75。
> - Object Insertion Simulation (Out-of-domain) 上，FID ↓ 为 101.27，对比 104.42 (Wan-Video V2V)，变化 -3.15。

## 概要

**问题瓶颈**：神经重建渲染在生成新视角时引入几何与外观伪影，且插入的动态物体与背景在色调、光照和阴影上存在明显不一致，导致模拟画面的真实感不足，无法满足在线仿真的需求。

**核心方法**：DiffusionHarmonizer 将预训练的非蒸馏图像扩散模型转换为一个**确定性单步时序增强器**。通过冻结编码器/解码器、仅微调扩散骨干并插入时序注意力层，配合多尺度感知损失抑制单步微调产生的高频棋盘伪影，以及一套覆盖伪影校正、色调协调、重光照和阴影生成的五部分合成数据管线，首次实现了满足在线模拟实时性与时序一致性要求的统一增强框架。

**方法定位**：该方法属于**扩散模型蒸馏与在线增强**的交叉范畴。与通用图像/视频编辑基线（如 SDEdit、InstructPix2Pix、Wan-Video V2V）相比，DiffusionHarmonizer 针对神经渲染的特定伪影分布进行了定制化训练；与专用 harmonization 方法（如 VHTT、Ke et al.）相比，它不仅能调整前景外观，还能合成场景一致的逼真阴影，并修复背景中的重建伪影。

**主要结果**：
- 在新轨迹模拟（域内）和物体插入模拟（域外）数据集上，FID 分别降至 120.23 和 101.27，FVD 降至 470.11，均显著优于所有编辑基线（Table 1）。
- 在重光照、阴影和 ISP 修改保留集上，PSNR/SSIM/LPIPS 均大幅领先，与真实世界参考画面高度吻合（Table 2, Table 3）。
- 用户研究中，84.28% 的参与者偏好 DiffusionHarmonizer 的效果优于第二强基线（Table 4）。
- 消融实验证实，多尺度感知损失是抑制单步训练高频伪影的关键（Figure 5），而数据管线的每一部分都提供了不可替代的监督信号（Table 6, Figure 6）。



神经渲染技术（如 3D Gaussian Splatting 和 NeRF）已能从多视图图像中重建驾驶场景，并支持在新视角、新轨迹下进行逼真模拟。然而，这类神经重建的渲染结果存在两个关键缺陷，严重阻碍了其在自动驾驶仿真中的实际应用：

**渲染伪影与视觉退化**。神经重建在新视角下的渲染不可避免地产生模糊、闪烁、几何畸变和纹理缺失等伪影。这些伪影源于重建模型对未观测区域的泛化不足，以及渲染过程中的数值不稳定。当模拟车辆沿不同于训练轨迹的路径行驶时，这些退化尤为明显，直接破坏了仿真的视觉可信度。

**动态物体插入的不一致性**。在仿真中，常需向重建场景插入动态物体（如其他车辆、行人）以构建交互场景。然而，插入的物体资产与神经渲染的背景在色调、光照方向和阴影投射上存在系统性偏差——前景物体可能来自不同采集条件，而背景的照明环境由重建隐式编码，二者缺乏统一的物理光照模型。这种不一致使合成画面呈现明显的“贴图感”，削弱了仿真对感知模型的训练价值。

现有解决方案存在明显缺口。通用图像编辑模型（如 **SDEdit** 基于 Stable Diffusion 3、**InstructPix2Pix**）和视频编辑模型（如 **Wan-Video V2V** 基于 WAN 2.1）虽然具备一定的增强能力，但它们依赖多步随机去噪，推理速度慢且难以保证帧间时序一致性，无法满足在线模拟的实时性要求。专用 harmonization 方法（如 **VHTT** 基于视频三重变换器、**Ke et al.** 预测可解释滤波器）仅能调整前景物体的色调以匹配背景，既无法修复背景的渲染伪影，也无法生成与场景一致的阴影，其功能范围远不足以覆盖神经渲染仿真的全部需求。

因此，本文的核心动机在于：**构建一个统一的在线增强框架，能够同时修复神经渲染的伪影、协调前景与背景的外观、并合成场景一致的阴影与光照效果，且满足实时推理的严苛约束**。这要求方法不仅具备强大的图像生成能力，还需在单步推理中保持时序连贯性，而现有方法无一能同时满足这些条件。



## 核心方法与创新机理

DiffusionHarmonizer 的核心创新在于将预训练多步扩散模型重塑为一个**确定性单步时序增强器**，并配合**多尺度感知损失**与**大规模合成数据管线**，首次在单 GPU 上实现满足在线模拟要求的神经渲染增强。以下从四个关键维度剖析其相对于现有基线的根本性改变。

### 从多步去噪到单步确定性映射

通用扩散编辑方法（如 **SDEdit**、**InstructPix2Pix**、**Wan-Video V2V**）依赖多步随机去噪过程，推理需 50 步以上，无法满足实时模拟需求。DiffusionHarmonizer 将扩散骨干 $\mathcal{F}_\theta$ 重新定义为确定性单步图像到图像转换器：直接将干净潜变量 $\mathcal{E}_\eta(I_t)$ 馈入网络，**不注入噪声**，并将时间步和文本条件 token 固定为空值常量（Sec 3.1）。增强帧通过单次前馈即可获得：

$$\hat{I}_t = \mathcal{D}_\phi(\mathcal{F}_\theta(\mathcal{E}_\eta(I_t)))$$

这一转换消除了扩散模型的多步随机采样瓶颈，使推理速度达到实时水平（1024×576 分辨率下单帧约 50ms，Table 3）。同时，冻结预训练的 VAE 编码器 $\mathcal{E}_\eta$ 和解码器 $\mathcal{D}_\phi$，仅微调扩散骨干 $\mathcal{F}_\theta$，保留了预训练模型的生成先验。

### 从单帧孤立处理到时序上下文建模

图像编辑基线（SDEdit、InstructPix2Pix）逐帧独立处理，缺乏时序建模，导致增强视频出现严重闪烁。视频编辑基线（Wan-Video V2V）虽有时序能力，但依赖全局注意力或光流，计算开销大且难以保持局部结构一致性。

DiffusionHarmonizer 在扩散骨干中**插入时序注意力层**，与空间注意力层交错排列。推理时，将当前退化帧与过去 $K=4$ 帧的历史增强帧潜变量串联为输入：

$$Z_t = [\mathcal{E}_{\eta}(I_t), \mathcal{E}_{\eta}(\hat{I}_{t-1}), \dots, \mathcal{E}_{\eta}(\hat{I}_{t-K})]$$

这一设计使单步前馈即可同时利用空间和时序上下文，输出时序一致的增强结果。消融实验证实，同时加入时序模块和时序扭曲损失将领域内时序一致性从 0.9714 提升至 0.9827（Table 5），并显著减少闪烁。

### 从标准感知损失到多尺度图块感知损失

将扩散模型转换为单步映射面临严重训练不稳定问题：标准 L2 损失导致输出过度平滑，而传统 LPIPS 损失则产生高频棋盘伪影。这是因为单步推理的“去噪轨迹”与多步训练轨迹严重失配。

DiffusionHarmonizer 引入**多尺度感知损失**，在随机采样的方形图块上计算 VGG 特征差异，图块大小在 $[128, 512]$ 范围内随机变化：

$$\mathcal{L}_{\mathrm{perc}} = \mathbb{E}_{k} \left[ \sum_{l} \lambda_{l} \big\| \phi_{l}(\hat{P}_{t}^{(k)}) - \phi_{l}(P_{\mathrm{gt}}^{(k)}) \big\|_{2}^{2} \right]$$

多尺度机制迫使模型同时关注局部细节和全局结构，有效抑制了单步微调特有的高频伪影。消融实验（Figure 5）显示，移除感知监督导致过度平滑，使用 LPIPS 则产生棋盘伪影，仅有多尺度方案能获得视觉上令人满意的结果。

此外，对于时序批次，还引入基于光流扭曲的**时序一致性损失** $\mathcal{L}_{\mathrm{temp}}$，仅在非遮挡区域计算前一帧增强结果的扭曲误差，进一步鼓励时序平滑。训练采用时序与非时序批次交替的策略，防止模型过拟合时序线索，同时充分利用图像和视频数据。

### 从通用预训练数据到五维合成数据管线

通用编辑模型依赖大规模预训练数据，缺乏针对神经渲染伪影的专项监督。DiffusionHarmonizer 构建了包含约 35 万帧的**五部分合成数据管线**（Sec 3.2, Figure 2 top）：

1. **伪影校正**（基于 DIFFIX3D+）：模拟神经重建产生的几何和外观伪影；
2. **ISP 修改**：通过 SAM2 分割掩码合成前景-背景色调不一致的复合图像；
3. **重光照**：改变场景光照条件，训练模型的光照调整能力；
4. **PBR 阴影模拟**：基于物理渲染生成动态物体的真实阴影；
5. **资产重插入**：将动态物体重新合成到不同背景中，训练阴影生成和色调协调。

消融实验（Table 6, Figure 6）表明，移除任一数据源均导致 FID 上升约 3-4 点：去除伪影校正数据则模型无法修复重建错误，去除阴影数据则无法合成逼真阴影，去除外观数据则色调协调失败。这证实了五部分数据提供了**不可替代的互补监督信号**，是 DiffusionHarmonizer 在色调协调、阴影生成和伪影校正三个子任务上统一超越专用方法的根本原因。



![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/001_Figure_1.jpg]]
*Figure 1: DiffusionHarmonizer on Driving Scenes. Our method transforms artifact-prone neural-rendered frames into temporally coherent simulations, improving their realism by jointly correcting shadows, lighting, appearance discrepancies and reconstruction artifacts*

DiffusionHarmonizer 的核心流水线由两条对称路径构成：**合成数据管线**（上方）负责生成大规模、多样化的配对训练样本，**单步时序增强模型**（下方）则将这些样本作为监督信号，将带有伪影的神经渲染帧实时转换为时序一致的逼真仿真帧。

### 数据管线：五类互补监督信号

为了让模型同时学会去伪影、色调协调、重光照和阴影生成，作者设计了一条可扩展的合成数据管线，包含五个互补组件（Figure 2 上半部分）：

1. **新视角伪影校正**：基于 **DIFFIX3D+** 框架，对神经渲染产生的新视角帧施加多种退化（几何扭曲、纹理模糊、孔洞等），形成“退化帧—干净帧”配对。
2. **ISP 修改**：利用 **SAM2** 分割前景区域，将前景替换为同一场景在不同 ISP 参数下的渲染结果，构造前景-背景色调不一致的合成图，目标为恢复原始 ISP 下的和谐外观。
3. **重光照**：通过调整场景光照参数生成不同光照条件下的渲染帧，要求模型将任意光照映射回参考光照。
4. **PBR 阴影模拟**：基于物理渲染（PBR）生成带真实阴影的合成帧，为模型提供阴影生成的监督信号。
5. **资产重插入**：将动态物体重新插入背景中，生成物体与场景在阴影、光照上不一致的合成图，目标为生成物理上连贯的合成结果。

五部分数据共约 35 万帧，覆盖了神经渲染仿真中最主要的真实感退化类型。消融实验证实，移除任一数据源均会导致 FID 上升约 3–4 点（Table 6, Figure 6），表明各组件提供的监督信号不可相互替代。

### 模型架构：从多步扩散到单步确定性增强器

增强模型的核心思想是将预训练的多步图像扩散模型改造为**确定性单步前馈映射**（Figure 2 下半部分）。具体而言：

**编码-解码冻结**：给定当前退化帧 $I_t$，预训练的 VAE 编码器 $\mathcal{E}_\eta$ 将其压缩至潜空间，得到干净潜变量 $\mathcal{E}_\eta(I_t)$；增强后的潜变量经预训练解码器 $\mathcal{D}_\phi$ 重建为输出帧 $\hat{I}_t$。整个训练过程中，编码器和解码器均保持冻结。

**扩散骨干微调**：唯一的可训练模块是扩散骨干 $\mathcal{F}_\theta$。与标准扩散模型的多步随机去噪不同，这里直接将干净潜变量输入网络，**不注入噪声**，并将时间步和文本条件标记固定为常量空值（null），从而将随机生成过程转化为确定性图像到图像翻译：

$$\hat{I}_t = \mathcal{D}_\phi(\mathcal{F}_\theta(\mathcal{E}_\eta(I_t)))$$

这一设计使得单次前向传播即可完成增强，为实时在线仿真奠定基础。

**时序条件注入**：为实现时序一致性，在扩散骨干中插入**时序注意力层**，与原有的空间注意力层交错排列。推理时，将当前帧潜变量与过去 $K=4$ 帧已增强帧的潜变量拼接：

$$Z_t = [\mathcal{E}_\eta(I_t), \mathcal{E}_\eta(\hat{I}_{t-1}), \dots, \mathcal{E}_\eta(\hat{I}_{t-K})]$$

$Z_t$ 经时序注意力处理后，单步即可输出时序连贯的增强结果。这一设计避免了视频扩散模型的多步推理开销，同时通过显式利用历史增强帧的上下文，有效抑制了逐帧独立处理带来的闪烁。

### 训练策略：多尺度感知损失与混合批次

单步微调的关键挑战在于：预训练扩散模型的多步去噪轨迹与单步确定性映射之间存在不匹配，直接使用 L2 或 LPIPS 损失容易产生高频棋盘伪影（Figure 5）。为此，作者引入**多尺度感知损失**：

$$\mathcal{L}_{\mathrm{perc}} = \mathbb{E}_{k} \left[ \sum_{l} \lambda_{l} \big\| \phi_{l}(\hat{P}_{t}^{(k)}) - \phi_{l}(P_{\mathrm{gt}}^{(k)}) \big\|_{2}^{2} \right], \quad k \in [128, 512]$$

该损失在随机采样的 128×128 至 512×512 方形图块上计算 VGG 特征差异，通过多尺度感受野覆盖，有效抑制了单步微调引入的高频伪影。

时序一致性则通过**时序扭曲损失**加强：

$$\mathcal{L}_{\mathrm{temp}} = \frac{1}{|\Omega|} \sum_{x \in \Omega} [ \hat{I}_{t}(x) - \mathrm{Warp}(\hat{I}_{t-1}, F_{t t-1})(x) ]^{2}$$

利用 RAFT 估计的光流 $F_{t t-1}$ 将前一帧增强结果扭曲到当前帧，仅在非遮挡区域 $\Omega$ 计算一致性约束。

总体训练目标为三者的加权和：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{l_2} \mathcal{L}_{l_2} + \lambda_{perc} \mathcal{L}_{\mathrm{perc}} + \lambda_{temp} \mathcal{L}_{\mathrm{temp}}$$

其中 $\lambda_{temp}=1$ 仅在时序批次中激活，非时序批次中为 0。训练采用**混合批次策略**——交替使用时序视频批次和非时序图像批次——以避免模型过拟合于强时序线索，同时充分利用全部五类数据。

### 推理流程

推理时，对于每一帧 $I_t$，模型执行以下步骤：
1. VAE 编码器将 $I_t$ 压缩为潜变量；
2. 与历史 $K$ 帧增强潜变量拼接后送入扩散骨干；
3. 骨干经空间注意力和时序注意力处理后输出增强潜变量；
4. VAE 解码器重建为最终增强帧 $\hat{I}_t$。

整个过程为确定性前馈，无需迭代去噪，在单 GPU 上即可实现 30 FPS 的实时推理。



### 单步确定性增强器

DiffusionHarmonizer 的核心是将预训练的多步扩散模型改造为确定性单步增强器。具体而言，给定退化帧 $I_t$，其增强过程为：

$$\hat{I}_t = \mathcal{D}_\phi(\mathcal{F}_\theta(\mathcal{E}_\eta(I_t)))$$

其中 $\mathcal{E}_\eta$ 和 $\mathcal{D}_\phi$ 分别为预训练的 VAE 编码器与解码器，训练期间保持冻结；$\mathcal{F}_\theta$ 为扩散骨干，是唯一可训练的模块。推理时，干净潜变量 $\mathcal{E}_\eta(I_t)$ 直接送入网络，不注入噪声，时间步和文本条件 token 均固定为常量空值（Sec 3.1）。这一设计将多步随机去噪转化为单步确定性前馈映射，是实现实时在线增强的基础。

### 时序条件建模

为获得时序一致的输出，扩散骨干中插入了与空间注意力交错的时序注意力层。在时刻 $t$，将当前帧与历史增强帧的潜变量沿序列维度拼接：

$$Z_t = [\mathcal{E}_{\boldsymbol{\eta}}(I_t), \mathcal{E}_{\boldsymbol{\eta}}(\hat{I}_{t-1}), \dots, \mathcal{E}_{\boldsymbol{\eta}}(\hat{I}_{t-K})]$$

其中 $K=4$ 为上下文长度。$Z_t$ 经时序注意力处理后，单步即可输出当前帧的增强潜变量，再由解码器重建为最终帧 $\hat{I}_t$（Eq. (2), Sec 3.1）。该方法无需多步扩散或光流对齐即可在单次前馈中融合时序信息。

### 多尺度感知损失

单步微调扩散模型容易产生高频棋盘伪影。为稳定训练，本文提出多尺度感知损失，在随机采样的方形图块上计算 VGG 特征差异：

$$\mathcal{L}_{\mathrm{perc}} = \mathbb{E}_{k} \left[ \sum_{l} \lambda_{l} \big| \big| \phi_{l}(\hat{P}_{t}^{(k)}) - \phi_{l}(P_{\mathrm{gt}}^{(k)}) \big| \big|_{2}^{2} \right], \quad k \in [128, 512]$$

其中 $\hat{P}_{t}^{(k)}$ 和 $P_{\mathrm{gt}}^{(k)}$ 分别为预测帧与真值帧上随机裁剪的边长为 $k$ 的图块，$\phi_l$ 为 VGG 网络第 $l$ 层的特征图，$\lambda_l$ 为各层权重。多尺度设计迫使模型在不同感受野下保持感知一致性，经验上显著抑制了棋盘伪影（Eq. (4), Sec 3.3）。

### 时序扭曲损失

为进一步鼓励时序平滑，引入基于光流的扭曲损失：

$$\mathcal{L}_{\mathrm{temp}} = \frac{1}{|\Omega|} \sum_{x \in \Omega} [ \hat{I}_{t}(x) - \mathrm{Warp}(\hat{I}_{t-1}, F_{t t-1})(x) ]^{2}$$

其中 $F_{t t-1}$ 为 RAFT 估计的从 $t$ 到 $t-1$ 的光流，$\mathrm{Warp}(\cdot)$ 为扭曲操作，$\Omega$ 为非遮挡像素集合。该损失仅惩罚可见区域的时序不一致，避免遮挡区域的错误监督（Eq. (5), Sec 3.3）。

### 总体训练目标

完整训练目标为三项损失的加权和：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{l_{2}} \mathcal{L}_{l_{2}} + \lambda_{perc} \mathcal{L}_{\mathrm{perc}} + \lambda_{temp} \mathcal{L}_{\mathrm{temp}}$$

其中 $\lambda_{temp}=1$ 仅对时序批次激活，非时序批次中 $\lambda_{temp}=0$。这一混合训练策略使模型同时利用图像配对数据和视频时序数据，避免对强时序线索的过拟合（Eq. (6), Sec 3.3）。



## 实验与关键发现

### 核心瓶颈与设计验证

DiffusionHarmonizer 针对的核心瓶颈是：神经重建渲染（如 3DGS）产生的新视角伪影，以及插入动态物体后与背景在色调、光照和阴影上的不一致。论文通过将多步扩散模型转换为**确定性单步增强器**，配合**多尺度感知损失**与**五部分合成数据管线**，在单 GPU 上实现了实时、时序一致的增强。以下实验系统性地验证了这一设计逻辑。

### 主结果：感知质量、结构保持与时序一致性

**Table 1** 报告了在新轨迹模拟（域内）和物体插入模拟（域外）两个基准上的全面对比。在域内测试中，DiffusionHarmonizer 的 FID 达到 120.23，优于最强图像编辑基线 **SDEdit**（SD3）的 129.92（↓9.69）；FVD 为 470.11，优于视频编辑基线 **Wan-Video V2V** 的 506.86（↓36.75）。在域外物体插入场景中，FID 为 101.27，同样超越 Wan-Video V2V 的 104.42。更重要的是，方法在 DINO 结构距离（0.9215）和时序一致性（0.9827）两项指标上均取得最优，表明单步增强器在提升感知真实感的同时，有效保持了场景几何结构并抑制了帧间闪烁。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/006_Table_1.jpg]]
*Table 1: Quantitative Comparison on Novel Trajectory Simulation (In-domain Test) and Object Insertion Simulation (Out-of-domain Test) Datasets. Our method outperforms all editing baselines in perceptual quality (lower FID/FVD) and preserves scene structure more faithfully (lower DINO-Struct-Dist). It also achieves strong temporal consistency (measured by VBench++ temporal flickering score), surpassing image-editing methods and matching video diffusion models, with only a marginal gap to WAN V2V*

在拥有真实标签的 holdout 数据集上（**Table 2**），方法的重光照 PSNR 达到 28.10，LPIPS 低至 0.0020；PBR 阴影数据的 LPIPS 为 0.0042，相比 SDEdit 的 0.0098 降低了 57%；ISP 修改数据上 PSNR 为 23.93，SSIM 高达 0.9974。这些结果表明，合成数据管线提供的像素级监督使模型能够精确逼近真实世界的渲染结果。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/008_Table_2.jpg]]
*Table 2: Quantitative Results on Relighting, PBR Shadow, and ISP Modification Holdout Sets. Our method achieves substantially better PSNR, SSIM, and LPIPS, closely matching real-world references*

与专用 harmonization 方法的对比（**Table 3**）进一步揭示了方法的核心优势：在 ISP 修改子集上，DiffusionHarmonizer 的 PSNR 达到 28.58，显著高于 **Ke et al.** 的 25.98（+2.60 dB），LPIPS 低至 0.0021。值得注意的是，**VHTT** 仅修饰前景区域且需要分割掩码，而 DiffusionHarmonizer 处理全图且无需掩码，却仍在对齐的前景区域指标上全面领先。定性结果（**Figure 4**）显示，所有 harmonization 基线均无法生成逼真的阴影，而 DiffusionHarmonizer 能合成与场景光照一致的软阴影，这正是数据管线中 PBR 阴影模拟组件的直接贡献。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/010_Table_3.jpg]]
*Table 3: Quantitative Comparison with Harmonization Baselines. Evaluated on the harmonization subset (ISP Modification), our method outperforms all baselines. Inference speed reported at 1024 × 576 resolution for Ours and Ke et al. [17], and at 576 × 320 resolution for VHTT*

### 用户研究与 VLM 评估

**Table 4** 的用户研究提供了最强有力的主观证据。在与各基线的两两对比中，DiffusionHarmonizer 被人类参与者的偏好率从 84.28% ± 10.92%（vs SDEdit）到 90.11% ± 14.13%（vs Wan-Video V2V）。VLM 评估器（Gemini-2.5-Flash）的偏好率与人类高度一致，验证了自动评估的可靠性。这一结果直接支撑了论文的核心主张：方法首次实现了满足在线模拟要求的统一增强框架。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/011_Table_4.jpg]]
*Table 4: User Study. Both human participants and VLM evaluators were asked to compare our results against each individual baseline and select the better one. We report the percentage of samples where our method is preferred over the baselines. A preference rate above 50% indicates that our method is preferred. Table 5. Ablation on Temporal Components. Adding temporal loss and temporal modules effectively improves temporal consistency*

### 消融实验：损失设计的关键作用

**Figure 5** 和定量消融揭示了多尺度感知损失对稳定单步训练的决定性作用。移除感知监督导致输出过度平滑，丢失纹理细节；使用传统 LPIPS 损失则产生严重的高频棋盘伪影。多尺度感知损失通过在随机 128–512 大小的图块上计算 VGG 特征差异，有效抑制了单步微调中因去噪轨迹不匹配而产生的伪影，这是方法实现单步推理而不牺牲质量的关键技术手段。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/009_Figure_5.jpg]]
*Figure 5: Ablation on Loss Design. Removing perceptual supervision leads to oversmoothed outputs, while using a conventional LPIPS loss produces high-frequency artifacts. Our multi-scale formulation mitigates these artifacts and yields perceptually better results. Table 6. Quantitative ablation on curated data sources. Model trained on all data sources provides the best performance*

### 消融实验：时序组件的贡献

**Table 5** 的消融表明，同时引入时序注意力层和时序扭曲损失将域内时序一致性从 0.9714 提升至 0.9827。定性上，移除时序模块导致明显的帧间闪烁和过渡不平滑。仅添加时序损失而不加时序模块，一致性提升有限（0.9806），说明时序注意力层对利用历史帧上下文至关重要。

### 消融实验：数据管线的互补性

**Table 6** 和 **Figure 6** 展示了数据源消融的显著影响。移除任一数据成分——伪影校正数据、阴影数据或外观数据（ISP 修改 + 重光照）——均导致 FID 上升约 3–4 点。定性上：无伪影校正数据时，模型无法修复重建错误；无阴影数据时，无法合成合理阴影；无外观数据时，色调协调能力显著下降。这验证了五部分数据管线中每一部分都提供不可替代的互补监督信号。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/012_Figure_6.jpg]]
*Figure 6: Ablation on Curated Data Sources. Removing any curated data source degrades performance: without artifact-correction data the model fails to fix reconstruction errors; without shadow data it cannot synthesize plausible shadows; and without appearance data it produces color-tone inconsistencies. Each data source provides complementary and essential supervision*

### 失败模式与局限性

尽管 DiffusionHarmonizer 在整体性能上表现优异，论文指出了若干值得关注的局限性：

1. **域外泛化边界**：模型的域外泛化能力仅在 Waymo 数据集上验证，对于其他传感器配置或极端环境（如夜间、雨天）的表现未充分探索，需要手动验证其在不同天气和光照条件下的鲁棒性。
2. **严重几何错误的处理**：单步推理虽然在效率和时序一致性上取得平衡，但可能无法完全消除大范围缺失区域或严重几何错误，这类情况可能需要多步扩散或专门的修复模块。
3. **时序上下文长度限制**：时序上下文固定为 K=4，对于长程场景变化或剧烈运动，可能仍会产生短期不一致。论文将此列为开放问题，建议探索增加上下文帧数或引入递归状态单元。
4. **数据管线构建成本**：训练依赖大规模定制合成数据管线（约 35 万帧），构建成本较高，且不能直接从真实世界无配对数据中学习。PBR 阴影与现实域之间存在 gap，论文建议通过域适应或在线微调缩小这一差距。
5. **基座模型规模未探索**：模型基于 Cosmos 0.6B 预训练扩散模型，更大规模基座模型的潜力尚未探索，这可能限制性能上限。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/007_Figure.jpg]]

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/019_Figure_13.jpg]]
*Figure 13: Comparison with Ground Truth on Holdout Datasets. Our model’s predictions closely match the ground-truth real-world captures, producing faithful, physically plausible results suitable for online simulation systems*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/005_Table.jpg]]

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2602_24096/figures/014_Figure_8.jpg]]
*Figure 8: User Study Interface. We show our study instructions and interface. Evaluators are shown the input image and two predictions (ours and a baseline) and asked to select the more realistic result, with prediction order randomized to avoid bias*



## 定位与知识库关联

### 与通用图像/视频编辑方法的对比

DiffusionHarmonizer 与当前主流的通用图像编辑和视频编辑方法存在本质差异。**SDEdit**（基于 Stable Diffusion 3）和 **InstructPix2Pix** 等图像编辑基线依赖多步随机去噪过程（通常 50 步以上），推理速度慢且缺乏时序建模能力，逐帧独立处理导致严重的闪烁和不一致。**Wan-Video V2V**（基于 WAN 2.1 扩散模型）虽然具备视频编辑能力，但其多步去噪机制仍无法满足在线模拟的实时性要求，且对神经渲染特有的伪影（如新视角合成产生的几何错误和阴影缺失）缺乏针对性处理。相比之下，DiffusionHarmonizer 将多步扩散模型转换为确定性单步增强器，配合时序注意力层（K=4 帧上下文）和混合时序训练策略，在单 GPU 上实现实时推理的同时保持时序一致性，这是通用编辑方法无法达成的关键优势。

### 与专用 Harmonization 方法的对比

专用 harmonization 方法主要关注前景物体的外观调整，但普遍缺乏阴影生成和伪影修复能力。**VHTT**（视频三重变换器方法）需要输入前景分割掩码，仅在前景区域计算指标，且评估分辨率较低（576×320）。**Ke et al.** 的方法仅预测可解释滤波器来调整前景色调，报告的速度（约 10ms）仅为六次滤波器应用的时间，不包括全图生成。这些方法在处理神经渲染的复合退化（包括背景伪影、全局光照不一致和阴影缺失）时能力严重不足。DiffusionHarmonizer 通过五部分合成数据管线（DIFFIX3D+ 伪影校正、ISP 修改、重光照、PBR 阴影模拟、资产重插入），统一处理色调协调、重光照和阴影生成，在全图范围内实现端到端增强，无需分割掩码。

### 适用边界与泛化能力

当前方法的域外泛化能力仅在 Waymo 自动驾驶数据集上得到验证。对于其他传感器配置（如不同相机参数、激光雷达融合场景）或极端环境条件（夜间、雨天、雪天），模型的表现未充分探索。训练依赖大规模定制合成数据管线（约 35 万帧），构建成本较高，且不能直接从真实世界无配对数据中学习，限制了向新场景的快速迁移。模型基于 Cosmos 0.6B 预训练扩散模型，更大规模基座模型（如 7B+ 参数级别）的潜力尚未挖掘，可能进一步提升生成质量但会牺牲实时性。

### 技术局限与失败模式

单步推理虽然在效率和时序一致性上取得平衡，但可能无法完全消除严重的几何错误，例如大范围缺失区域或极端遮挡导致的神经渲染失败。时序上下文固定为 K=4，对于长程场景变化（如长时间遮挡后物体重新出现）或剧烈运动，可能仍会产生短期不一致。多尺度感知损失虽然有效抑制了单步微调产生的棋盘伪影，但其对图块尺寸范围（128-512）的敏感性未做系统消融。此外，PBR 阴影数据与真实世界阴影之间存在域间隙，当前管线未引入域适应或在线微调机制来缩小这一差距。

### 开放问题与后续方向

1. **长程时序建模**：能否在保持实时性的前提下，通过增加上下文帧数（K>4）或引入递归状态单元（如轻量级时序记忆模块）进一步提升长程时序连贯性？
2. **域适应与在线学习**：当前数据管线中 PBR 阴影与现实域之间存在 gap，能否通过域适应技术（如对抗训练或特征对齐）或在线微调（利用仿真运行中收集的真实-渲染配对）缩小这一差距？
3. **跨场景泛化**：方法在非自动驾驶场景（如机器人操作、室内导航、AR/VR）的适用性如何？需要如何调整数据管线以适应不同的传感器和场景特性？
4. **模型压缩与独立性**：是否可以通过知识蒸馏或直接训练，避免依赖预训练扩散模型，从而减少模型体积（当前约 0.74B 参数）并避免潜在的基础模型版权和许可问题？
5. **高度动态场景**：如何处理多个快速移动物体的同时插入，此时光流估计不可靠、时序信息因严重遮挡而失效？是否需要引入物体级别的跟踪或运动补偿机制？
6. **评估体系完善**：当前评估主要依赖 FID/FVD 等分布层面指标和用户研究，缺乏对物理真实性（如阴影方向一致性、光照物理正确性）的定量度量，未来需要建立更细粒度的评估基准。



## 原文 PDF

![[paperPDFs/CVPR_2026/DiffusionHarmonizer_Bridging_Neural_Reconstruction_and_Photorealistic_Simulation_with_Online_Diffusion_Enhancer.pdf]]
