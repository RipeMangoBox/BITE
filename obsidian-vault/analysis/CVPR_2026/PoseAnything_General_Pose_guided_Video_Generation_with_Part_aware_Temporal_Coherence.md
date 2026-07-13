---
title: "PoseAnything: General Pose-guided Video Generation with Part-aware Temporal Coherence"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.pdf
project_link: "https://ryan-w2024.github.io/project/PoseAnything/"
code_link: null
aliases:
- PoseAnything
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 部件感知时序一致性模块（PTCM）通过帧间部件匹配与跨注意力控制，将整体外观一致性分解为部件级精细控制；解耦CFG策略实现了独立的相机运动控制。
primary_logic: 将主体按骨架段分割为多个部件，利用注意力权重建立帧间部件对应，并仅在匹配部件间进行交叉注意力计算，从而将整体外观保持问题转化为细粒度的部件级一致性优化，有效缓解大运动下的外观扭曲。
claims:
- PoseAnything在人类姿态数据集TikTok上全面超越现有方法（PSNR 31.50, FVD 133.95等五项指标均最优）
- 在非人姿态数据集XPose-benchmark上同样取得最佳性能
- 消融实验表明移除PTCM或部件分割匹配步骤均会导致性能下降，验证了PTCM的有效性
- 解耦CFG首次实现姿态引导视频生成中的相机运动控制，消除了耦合注入的相互干扰
---

# PoseAnything: General Pose-guided Video Generation with Part-aware Temporal Coherence

> [!tip] 核心洞察
> 将主体按骨架段分割为多个部件，利用注意力权重建立帧间部件对应，并仅在匹配部件间进行交叉注意力计算，从而将整体外观保持问题转化为细粒度的部件级一致性优化，有效缓解大运动下的外观扭曲。

| 字段 | 内容 |
|------|------|
| 中文题名 | PoseAnything：通用姿态引导视频生成与部件感知时序一致性 |
| 英文题名 | PoseAnything: General Pose-guided Video Generation with Part-aware Temporal Coherence |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_PoseAnything_General_Pose-guided_Video_Generation_with_Part-aware_Temporal_Coherence_CVPR_2026_paper.html) · [Project](https://ryan-w2024.github.io/project/PoseAnything/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PoseAnything |
| Dataset | TikTok, XPose-benchmark |

> [!tip] 效果简介
> - TikTok (Human) 上，PSNR / SSIM / L1 / LPIPS / FVD 31.50 / 0.836 / 2.79e-5 / 0.224 / 133.95 vs state-of-the-art methods (Disco, AnimateAnyone, Animate-X, Champ, MagicAnimate,... (在所有五项指标上均取得最优)。
> - XPose-benchmark (Non-human) 上，FVD / PSNR / SSIM 等 见原文表格 vs state-of-the-art methods (显著超越所有基线方法)。

## 概要

**PoseAnything** 是一个通用的姿态引导视频生成框架，旨在解决现有方法仅支持人类姿态、无法维持运动过程中精细外观一致性、且缺乏相机运动控制能力的瓶颈。其核心思想是将主体按骨架段分割为多个部件，利用注意力权重建立帧间部件对应关系，并仅在匹配部件间进行交叉注意力计算，从而将整体外观保持问题转化为细粒度的部件级一致性优化。

方法上，PoseAnything 基于 **Wan2.2-TI2V-5B** 预训练文生视频骨干网络，引入三个关键改进：**通道维姿态注入**将姿态潜在表示与参考图像潜在在通道上拼接后输入 DiT 块；**部件感知时序一致性模块（PTCM）** 通过骨架段膨胀生成部件掩码、基于注意力权重匹配帧间对应部件、并在匹配部件令牌间计算交叉注意力，实现部件级精细外观控制；**主体与相机运动解耦 CFG** 首次在姿态引导视频生成中实现独立的相机运动控制，将主体姿态注入正锚点、相机运动注入负锚点，消除耦合注入的相互干扰。

在实验验证上，PoseAnything 在人类姿态数据集 **TikTok** 上全面超越现有方法（PSNR 31.50, FVD 133.95 等五项指标均最优，见 Table 1），在非人姿态数据集 **XPose-benchmark** 上同样取得最佳性能（Table 2）。消融实验表明，移除 PTCM 模块或省略部件分割匹配步骤均导致性能显著下降（Table 3），验证了部件级一致性机制的有效性。解耦 CFG 策略成功实现了相机运动控制，消除了主体与相机条件耦合注入的干扰（Figure 8）。



姿态引导视频生成（Pose-guided Video Generation）旨在根据给定的参考图像与目标姿态序列，生成符合指定动作的视频片段。该技术在虚拟数字人、影视特效、游戏动画等领域具有广泛的应用前景。然而，现有方法面临两大核心瓶颈：

**通用性受限。** 当前主流方法——如 **Disco**（Wang et al., CVPR 2024）、**AnimateAnyone**（Hu, CVPR 2024）、**MagicAnimate**（Xu et al., CVPR 2024）和 **Champ**（Zhu et al., ECCV 2024）——几乎全部聚焦于人类姿态驱动。尽管 **Animate-X**（Tan et al., ICLR 2025）初步探索了非人姿态生成，但整体而言，面向任意骨架结构（如四足动物、多足生物、机械体等）的通用姿态引导视频生成仍是一个未被充分解决的开放问题。

**外观一致性难以维持。** 在驱动主体执行大幅运动时，现有方法通常依赖基于 ControlNet 或参考图的全局交叉注意力来维持时序一致性。这类全局机制缺乏对主体不同部位（如四肢、躯干、尾部）的细粒度感知，容易导致运动过程中的外观扭曲、纹理漂移和部件错位，尤其在非人主体的复杂骨架运动下更为严重。

**相机运动控制缺失。** 现有姿态引导视频生成方法不支持独立的相机运动控制，或将其与主体运动条件耦合注入，导致两者相互干扰，无法实现“主体按指定姿态运动，同时镜头按指定轨迹推拉摇移”的精细控制。

针对上述问题，本文提出 **PoseAnything**——一个通用的姿态引导视频生成框架，核心动机包括：（1）支持任意骨架输入，覆盖人类与非人主体；（2）通过**部件感知时序一致性模块（Part-aware Temporal Coherence Module, PTCM）**将全局外观保持问题分解为部件级的精细一致性优化；（3）通过**解耦分类器自由引导（Decoupled CFG）**首次实现主体运动与相机运动的独立控制。



## 核心方法与创新机理

PoseAnything 针对通用姿态引导视频生成中两个尚未被现有方法解决的核心瓶颈，提出了三项关键创新。

### 瓶颈一：通用姿态支持与精细外观一致性

现有方法（如 **AnimateAnyone** (Hu, CVPR 2024)、**Disco** (Wang et al., CVPR 2024)）仅支持人类姿态，且依赖基于 ControlNet 或参考图的全局交叉注意力来维持时序一致性。这种方式在大幅度运动下容易产生外观扭曲，无法保持主体细节。**Animate-X** (Tan et al., ICLR 2025) 虽然探索了非人姿态生成，但其一致性控制仍停留在整体层面。

PoseAnything 的核心突破在于**将整体外观保持问题分解为部件级的精细控制**：

- **部件感知时序一致性模块 (Part-aware Temporal Coherence Module, PTCM)**：将主体按骨架段分割为多个部件，利用注意力权重建立帧间部件对应关系，并仅在匹配的部件令牌对之间计算交叉注意力。具体而言，对于每对匹配部件 $\langle m_{0j}, m_{ij} \rangle$，交叉注意力计算为：

$$x' = x + \text{Cross-Attn}(Q_j, K_j, V_j),\; Q_j = m_{ij} X W_q,\; K_j = m_{0j} X_0 W_k,\; V_j = m_{0j} X_0 W_v$$

其中 $m_{0j}$ 和 $m_{ij}$ 分别为第一帧与第 $i$ 帧的第 $j$ 个部件掩码。该模块插入在每个 DiT 块原有的交叉注意力层之后，通过对齐对应部件的令牌，有效缓解了大运动下的外观扭曲。

- **帧间部件匹配机制**：基于注意力权重建立帧间部件对应：

$$s_{ij'} \sim s_{0j} \iff j' = \arg\max_t \text{attn\_weight}[m_{0j}][m_{it}]$$

- **部件掩码生成**：通过对骨架段 $s_{ij}$ 进行膨胀操作获得部件掩码：

$$m_{ij} = \text{Dilate}(s_{ij}, \alpha)$$

消融实验证实，移除 PTCM 模块或移除部件分割与匹配步骤均会导致性能显著下降（Table 3），验证了部件级一致性控制的有效性。

### 瓶颈二：相机运动控制缺失

现有姿态引导视频生成方法不支持相机运动控制，或将相机运动与主体运动条件耦合注入，导致两者相互干扰。

PoseAnything 首次实现了姿态引导视频生成中的**相机运动独立控制**，其核心是**解耦分类器自由引导 (Decoupled CFG)**：

$$\tilde{\epsilon} = \hat{\epsilon}_{\theta}(\emptyset_s, z_c) + s \cdot (\hat{\epsilon}_{\theta}(z_s, \emptyset_c) - \hat{\epsilon}_{\theta}(\emptyset_s, z_c))$$

其中 $z_s$ 为主体姿态条件，$z_c$ 为相机运动条件。该策略将主体姿态注入正锚点，相机运动注入负锚点，消除了耦合注入带来的相互干扰（Figure 5, Figure 8）。

### 姿态条件注入方式改进

相较于常见的 MLP 融合或宽度拼接方式，PoseAnything 采用**通道维拼接**将姿态潜在表示与噪声潜在融合后输入 DiT：

$$Z_{agr} = [Z_0, Z_p] \in F \times H \times W \times 2C, \; Z = \text{Conv}(Z_{agr}) \in f \times h \times w \times c$$

论文指出通道维条件注入方式在姿态引导视频生成中展现出显著优势（详见补充材料）。

### 创新总结

| 改进槽位 | 基线方法 | PoseAnything |
|---------|---------|-------------|
| 时序一致性机制 | 基于 ControlNet/参考图的全局交叉注意力 | PTCM：部件分割→帧间匹配→部件感知交叉注意力 |
| 相机运动控制 | 不支持或与主体运动耦合 | 解耦 CFG：主体注入正锚点，相机注入负锚点 |
| 姿态条件注入 | MLP 融合或宽度拼接 | 通道维拼接后经卷积输入 DiT |

这三项创新共同构成了 PoseAnything 的方法核心：PTCM 提供了细粒度的外观一致性保障，解耦 CFG 赋予了独立的相机运动控制能力，通道维拼接优化了姿态条件的注入效率。三者协同使得 PoseAnything 能够同时支持人类与非人主体的通用姿态引导视频生成。



PoseAnything 的整体 pipeline 以 Wan2.2‑TI2V‑5B 预训练文生视频模型为骨干，将姿态引导视频生成分解为三个标准化阶段：姿态编码与条件注入、部件感知时序一致性控制、以及主体‑相机运动解耦采样。给定一张参考图像 $I_r$ 和一段任意骨架的姿态序列 $P$，系统首先将姿态序列编码为潜在表示 $Z_p$，再与参考图像的潜在 $Z_0$ 沿通道维拼接后馈入 DiT 模块；随后，在每个 DiT 块中插入部件感知时序一致性模块（PTCM），通过帧间部件匹配与部件级交叉注意力实现细粒度外观保持；最后在采样阶段采用解耦 CFG，将主体姿态与相机运动分别注入正/负锚点，消除相互干扰。整个框架的输入输出流与模块关系如 Figure 4 所示。

![[assets/figures/papers/paper_list_l1000_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PoseAnything_Gene/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our PoseAnything. Given a reference image Ir and a pose sequence P , we first encode P into pose latent*

### 3.1 姿态编码与条件注入

与常见采用 MLP 融合或宽度拼接的方式不同，PoseAnything 采用通道维拼接策略，将姿态条件与噪声潜在在特征维度上直接耦合。具体而言，参考图像 $I_r$ 经 VAE 编码得到初始潜在 $Z_0 \in \mathbb{R}^{F \times H \times W \times C}$，姿态序列 $P$ 经姿态 VAE 编码得到姿态潜在 $Z_p$，二者沿通道维拼接后通过卷积层进行 patchify，形成 DiT 块的统一输入：

$$Z_{agr} = [Z_0, Z_p] \in \mathbb{R}^{F \times H \times W \times 2C}, \quad Z = \text{Conv}(Z_{agr}) \in \mathbb{R}^{f \times h \times w \times c}$$

该设计使姿态信息与图像内容在 DiT 的整个推理过程中保持紧密耦合，为后续的部件级控制提供了统一的特征基础。消融实验表明，通道拼接注入相较于 MLP 融合方式在姿态引导视频生成中具有显著优势（详见原文补充材料）。

### 3.2 部件感知时序一致性模块

PTCM 是 PoseAnything 的核心创新模块，被插入到每个 DiT 块中原有交叉注意力层之后。该模块将整体外观一致性分解为部件级精细控制，其工作流程分为三步：

1. **部件分割与掩码生成**：将姿态骨架按骨架段分割为多个部件 $s_{ij}$（$i$ 表示帧索引，$j$ 表示部件索引），对每个骨架段进行膨胀操作获得部件掩码 $m_{ij} = \text{Dilate}(s_{ij}, \alpha)$，从而将主体划分为空间上可区分的部件区域。

2. **帧间部件匹配**：利用注意力权重建立第一帧与后续帧之间的部件对应关系。对于第一帧的部件 $s_{0j}$ 与第 $i$ 帧的候选部件 $s_{it}$，匹配规则为：

$$s_{ij'} \sim s_{0j} \iff j' = \arg\max_t \ \text{attn\_weight}[m_{0j}][m_{it}]$$

即选择注意力权重最高的部件作为对应匹配，确保不同帧中同一语义部件（如“左前腿”）被正确关联。

3. **部件感知交叉注意力**：对于每对匹配部件 $\langle m_{0j}, m_{ij} \rangle$，仅使用对应部件的令牌计算跨帧交叉注意力：

$$x' = x + \text{Cross-Attn}(Q_j, K_j, V_j)$$

其中 $Q_j = m_{ij} X W_q$、$K_j = m_{0j} X_0 W_k$、$V_j = m_{0j} X_0 W_v$，$X_0$ 和 $X$ 分别为第一帧和当前帧的特征。通过将交叉注意力的计算限制在匹配部件之间，PTCM 有效抑制了大运动下全局交叉注意力带来的外观扭曲问题。

### 3.3 主体与相机运动解耦 CFG

传统姿态引导视频生成方法要么不支持相机运动控制，要么将相机运动与主体姿态条件耦合注入，导致二者相互干扰。PoseAnything 提出解耦 CFG 策略，首次实现了独立的相机运动控制。其核心思想是：在采样过程中，将主体姿态条件注入正锚点，将相机运动条件注入负锚点，从而在 CFG 框架内解耦两类运动信号：

$$\tilde{\epsilon} = \hat{\epsilon}_{\theta}(\emptyset_s, z_c) + s \cdot \left(\hat{\epsilon}_{\theta}(z_s, \emptyset_c) - \hat{\epsilon}_{\theta}(\emptyset_s, z_c)\right)$$

其中 $z_s$ 为主体姿态条件，$z_c$ 为相机运动条件，$\emptyset_s$ 和 $\emptyset_c$ 分别表示置空对应条件。该公式通过正锚点 $\hat{\epsilon}_{\theta}(z_s, \emptyset_c)$ 强化主体运动遵循，通过负锚点 $\hat{\epsilon}_{\theta}(\emptyset_s, z_c)$ 引入相机运动引导，二者在减法项中自然解耦，消除了耦合注入时的相互干扰（机制示意见 Figure 5）。

### 3.4 训练策略

PoseAnything 的训练分三阶段进行：第一阶段使用 XPose 数据集和 15,000 个内部人类视频进行 3k 次迭代，学习率 $5 \times 10^{-5}$；第二阶段保持相同学习率继续训练；第三阶段进行 8k 次迭代，学习率降至 $1 \times 10^{-5}$。分阶段训练策略有助于模型先学习通用的姿态‑外观映射，再精细优化时序一致性。



PoseAnything 的核心架构围绕三个关键设计展开：**通道维姿态条件注入**、**部件感知时序一致性模块（PTCM）** 以及 **主体与相机运动解耦 CFG**。以下逐一展开其公式化表述与工作机制。

### 4.1 姿态条件注入：通道维拼接

给定参考图像潜在表示 $Z_0 \in \mathbb{R}^{F \times H \times W \times C}$ 和姿态序列的潜在表示 $Z_p$（由姿态 VAE 编码得到），PoseAnything 采用通道维拼接进行条件注入，而非 MLP 融合或宽度拼接：

$$Z_{agr} = [Z_0, Z_p] \in \mathbb{R}^{F \times H \times W \times 2C}$$

随后通过卷积层降维并分块，输入 DiT 模块：

$$Z = \mathrm{Conv}(Z_{agr}) \in \mathbb{R}^{f \times h \times w \times c}$$

其中 $F, H, W, C$ 为原始潜在空间的帧数、高度、宽度和通道数，$f, h, w, c$ 为分块后的维度。这一设计的优势在于保留了姿态与图像特征在通道维的完整交互空间，避免了 MLP 逐元素加和可能带来的信息压缩。消融实验（见 #Suppl）表明，通道维条件注入在姿态引导视频生成中显著优于 MLP 融合方案。

### 4.2 部件感知时序一致性模块（PTCM）

PTCM 是 PoseAnything 解决大运动下外观扭曲问题的核心创新，其工作流程分为三步：

**步骤一：部件掩码生成。** 对于任意骨架的第 $j$ 个段 $s_{ij}$（第 $i$ 帧），通过膨胀操作获得部件掩码：

$$m_{ij} = \mathrm{Dilate}(s_{ij}, \alpha)$$

其中 $\alpha$ 为膨胀系数，控制掩码覆盖范围。膨胀后的掩码 $m_{ij}$ 用于在注意力计算中筛选属于该部件的令牌。

**步骤二：帧间部件匹配。** 基于 DiT 块中已有的注意力权重，将第一帧的每个部件与后续帧的对应部件建立对应关系。匹配规则为：对于第一帧部件 $s_{0j}$，在后续帧 $i$ 中寻找注意力权重最大的部件 $s_{ij'}$：

$$s_{ij'} \sim s_{0j} \iff j' = \arg\max_t \mathrm{attn\_weight}[m_{0j}][m_{it}]$$

这一匹配机制利用了扩散模型内部注意力图已蕴含的语义对应信息，无需额外的显式匹配网络。

**步骤三：部件感知交叉注意力。** 在 DiT 块的原始交叉注意力层之后插入部件感知交叉注意力模块。对于每对匹配部件 $\langle m_{0j}, m_{ij} \rangle$，仅用对应部件的令牌计算跨帧交叉注意力：

$$x' = x + \mathrm{Cross\text{-}Attn}(Q_j, K_j, V_j)$$

其中：

$$Q_j = m_{ij} X W_q, \quad K_j = m_{0j} X_0 W_k, \quad V_j = m_{0j} X_0 W_v$$

这里 $X$ 和 $X_0$ 分别为当前帧和第一帧的令牌表示，$W_q, W_k, W_v$ 为可学习的投影矩阵。通过掩码 $m_{ij}$ 和 $m_{0j}$ 的筛选，交叉注意力仅在对应部件之间进行，从而将全局外观一致性分解为细粒度的部件级控制。这一设计有效缓解了大运动下全局交叉注意力容易产生的纹理混叠和身份漂移问题。

### 4.3 主体与相机运动解耦 CFG

传统姿态引导视频生成方法不支持相机运动控制，或将其与主体运动条件耦合注入，导致二者相互干扰。PoseAnything 提出解耦 CFG 策略，将主体姿态注入正锚点、相机运动注入负锚点：

$$\tilde{\epsilon} = \hat{\epsilon}_{\theta}(\emptyset_s, z_c) + s \cdot \big(\hat{\epsilon}_{\theta}(z_s, \emptyset_c) - \hat{\epsilon}_{\theta}(\emptyset_s, z_c)\big)$$

其中 $\hat{\epsilon}_{\theta}$ 为扩散模型的噪声预测函数，$z_s$ 和 $z_c$ 分别表示主体姿态条件和相机运动条件，$\emptyset_s$ 和 $\emptyset_c$ 为对应的空条件，$s$ 为引导强度。该公式的含义是：以仅注入相机条件的预测为基底，加上主体条件与相机条件之间的差异项进行引导，从而实现两类运动的独立控制。这一设计首次在姿态引导视频生成中实现了相机运动控制，消除了耦合注入的相互干扰（见 Figure 8 的相机控制效果展示）。

### 补充图表

![[assets/figures/papers/paper_list_l1000_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PoseAnything_Gene/figures/005_Figure_5.jpg]]
*Figure 5: Subject and Camera Decoupled Control Based on CFG. dex of the segment of the current pose. To obtain the pixels*



## 实验与关键发现

### 实验设置

PoseAnything 以 **Wan2.2-TI2V-5B** 预训练文生视频模型为骨干网络，训练数据包含两部分：自建的 **XPose** 通用姿态数据集（约 36,000 个非人主体视频片段）与 15,000 个内部人类视频。训练分三阶段进行：第一阶段 3k 次迭代，学习率 5×10⁻⁵；第二阶段保持相同学习率；第三阶段 8k 次迭代，学习率降至 1×10⁻⁵。评估覆盖人类姿态数据集 **TikTok** 和自建的非人姿态基准 **XPose-benchmark**，指标包括 PSNR、SSIM、L1、LPIPS 和 FVD。

### 人类姿态生成：TikTok 数据集

Table 1 给出了 TikTok 数据集上的定量对比。PoseAnything 在全部五项指标上均取得最优：

![[assets/figures/papers/paper_list_l1000_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PoseAnything_Gene/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparisons with the state-of-the-arts on TikTok dataset (Human)*

- **PSNR**: 31.50（超越 Disco、AnimateAnyone、Animate-X、MagicAnimate、Champ、UniAnimate 等基线）
- **SSIM**: 0.836
- **L1**: 2.79×10⁻⁵
- **LPIPS**: 0.224
- **FVD**: 133.95

这一结果验证了通道维姿态拼接注入与部件感知时序一致性模块（PTCM）的有效性。相比 **Disco**（Wang et al., CVPR 2024）等前期方法采用的 MLP 融合或宽度拼接方案，通道拼接保留了更完整的姿态空间信息；相比 **AnimateAnyone**（Hu, CVPR 2024）和 **MagicAnimate**（Xu et al., CVPR 2024）基于参考图的全局交叉注意力机制，PTCM 将外观保持分解为部件级精细控制，在大幅度运动下显著缓解了外观扭曲。

### 非人姿态生成：XPose-benchmark

Table 2 展示了 XPose-benchmark 上的定量结果。PoseAnything 同样显著超越所有基线方法，证明了其通用骨架输入设计的优势。**Animate-X**（Tan et al., ICLR 2025）虽已探索非人姿态生成，但其一致性控制仍依赖全局注意力，在处理多段骨架主体（如四足动物、机械臂）时容易出现部件混淆。PoseAnything 的帧间部件匹配机制——基于注意力权重建立第一帧与后续帧的部件对应，并仅在匹配部件间计算交叉注意力——从根本上规避了这一问题。

![[assets/figures/papers/paper_list_l1000_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PoseAnything_Gene/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison between the state-of-the-arts and Ours on XPose-benchmark (Non-human)*

Figure 7 的定性对比进一步印证：基线方法在非人主体的大幅度旋转、多肢协调运动场景下普遍出现部件错位或纹理模糊，而 PoseAnything 能保持各部件外观的稳定一致。

![[assets/figures/papers/paper_list_l1000_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PoseAnything_Gene/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative comparison with existing state-of-the-art methods on XPose-benchmark*

### 消融实验

Table 3 报告了消融实验的定量结果，核心发现如下：

![[assets/figures/papers/paper_list_l1000_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PoseAnything_Gene/figures/011_Table_3.jpg]]
*Table 3: Quantitative results of ablation study*

1. **移除 PTCM 模块**（w/o PTCM）导致各项指标显著下降，验证了部件级时序一致性控制是性能提升的关键因果机制。
2. **移除部件分割与匹配步骤**同样造成性能损失，说明仅靠全局交叉注意力无法有效建立帧间细粒度对应。PTCM 的完整流程——骨架段膨胀生成部件掩码 $m_{ij}$、基于注意力权重的帧间匹配、匹配部件间的交叉注意力计算——三者缺一不可。

### 相机运动解耦控制

Figure 8 展示了主体与相机运动解耦 CFG 的控制效果。传统方案将相机运动与主体姿态条件耦合注入，导致两者相互干扰（例如相机平移时主体外观出现非预期变形）。PoseAnything 的解耦策略——将主体姿态注入正锚点、相机运动注入负锚点，公式为：

![[assets/figures/papers/paper_list_l1000_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PoseAnything_Gene/figures/010_Figure_8.jpg]]
*Figure 8: Demonstration of Camera Control Cases*

$$\tilde{\epsilon} = \hat{\epsilon}_{\theta}(\emptyset_s, z_c) + s \cdot (\hat{\epsilon}_{\theta}(z_s, \emptyset_c) - \hat{\epsilon}_{\theta}(\emptyset_s, z_c))$$

首次在姿态引导视频生成中实现了独立的相机运动控制，消除了耦合注入的相互干扰。

### 局限性与讨论

需要指出的是，训练所用的 15,000 个人类视频为内部数据，未完全公开，这在一定程度上限制了完全复现的可能性。但 XPose 数据集已开源，为社区研究非人姿态生成提供了基础。此外，当前方法在处理极端遮挡或骨架关键点严重缺失的场景时，部件匹配的准确性可能下降，该问题有待进一步探索。



## 定位与知识库关联

### 1. 与现有方法的继承与突破关系

PoseAnything 建立在两条技术路线的交汇点上：**姿态引导视频生成** 和 **图像动画/主体一致性保持**。其核心突破在于将“整体外观一致性”问题分解为“部件级精细控制”，并首次在姿态引导视频生成中引入解耦的相机运动控制。

#### 1.1 姿态引导视频生成路线的演进

早期姿态引导视频生成方法以 **Disco** (Wang et al., CVPR 2024) 为代表，通过 ControlNet 类架构将姿态条件注入扩散模型，但仅支持人类姿态且在大幅度运动下容易出现外观扭曲。**AnimateAnyone** (Hu, CVPR 2024) 进一步优化了人类姿态驱动的视频生成质量，但仍受限于固定的人体骨架拓扑。

PoseAnything 在三个关键维度上实现了突破：

- **通用骨架支持**：不同于 Disco 和 AnimateAnyone 仅处理人体姿态，PoseAnything 通过通道维拼接的方式注入任意骨架序列的潜在表示，使其能够处理从四足动物到多足昆虫等非人主体的姿态。这一设计直接回应了 **Animate-X** (Tan et al., ICLR 2025) 对非人姿态生成的初步探索，但 Animate-X 仍缺乏精细的时序一致性机制。

- **条件注入方式的改进**：现有方法常见采用 MLP 融合或宽度拼接注入姿态条件，PoseAnything 改用通道维拼接（$Z_{agr} = [Z_0, Z_p] \in F \times H \times W \times 2C$），将参考图像潜在与姿态潜在在通道上拼接后通过卷积层输入 DiT 块。这一设计在补充实验中被验证具有显著优势（见 #Suppl ），其直觉在于通道拼接保留了姿态信号与图像信号的空间对齐关系，而 MLP 融合可能丢失这种空间对应。

#### 1.2 时序一致性机制的进化

主体外观一致性是姿态引导视频生成的核心挑战。现有方法主要依赖两类机制：

- **基于 ControlNet 的全局控制**（Disco 等）：通过姿态骨架图作为额外条件输入，但缺乏帧间显式的对应关系建模。
- **基于参考图的全局交叉注意力**（**MagicAnimate** (Xu et al., CVPR 2024)、**Champ** (Zhu et al., ECCV 2024)、**UniAnimate** (Wang et al., arXiv 2024)）：将第一帧作为参考图像，通过交叉注意力将外观信息传播到后续帧。这种方法在人体动画中效果显著，但全局注意力在大运动或复杂变形下容易失效——不同身体部位可能错误地关注到无关区域。

PoseAnything 的 **部件感知时序一致性模块（PTCM）** 将这一范式从“全局”推进到“部件级”：

1. **部件分割**：将主体按骨架段分割为多个部件，通过膨胀骨架段获得部件掩码 $m_{ij} = \mathrm{Dilate}(s_{ij}, \alpha)$。
2. **帧间部件匹配**：利用注意力权重建立第一帧与后续帧的部件对应关系 $s_{ij'} \sim s_{0j} \iff j' = \arg\max_t \mathrm{attn\_weight}[m_{0j}][m_{it}]$。
3. **部件感知交叉注意力**：仅在匹配的部件对之间计算交叉注意力，$x' = x + \mathrm{Cross-Attn}(Q_j, K_j, V_j)$，其中 $Q_j$ 来自当前帧部件令牌，$K_j, V_j$ 来自第一帧对应部件令牌。

这一设计的核心洞察在于：**将整体外观保持问题转化为细粒度的部件级一致性优化，有效缓解大运动下的外观扭曲**。消融实验（Table 3）验证了移除 PTCM 或移除部件分割匹配步骤均会导致性能显著下降。

#### 1.3 相机运动控制的首次实现

在 PoseAnything 之前，姿态引导视频生成方法**不支持相机运动控制**，或将主体运动与相机运动条件耦合注入，导致相互干扰。PoseAnything 提出的**解耦 CFG 策略**首次实现了独立的相机运动控制：

$$\tilde{\epsilon} = \hat{\epsilon}_{\theta}(\emptyset_s, z_c) + s \cdot (\hat{\epsilon}_{\theta}(z_s, \emptyset_c) - \hat{\epsilon}_{\theta}(\emptyset_s, z_c))$$

其原理是将主体姿态注入正锚点（$z_s$），相机运动注入负锚点（$z_c$），通过 CFG 的减法操作消除耦合干扰。这一设计使得用户可以在不改变主体动作的前提下独立控制镜头运动（如平移、倾斜），如图 8 所示。

### 2. 适用边界与局限

#### 2.1 适用场景

PoseAnything 在以下场景展现出显著优势：

- **通用主体姿态驱动**：支持任意骨架拓扑的主体（人类、动物、机器人等），只要能够提取骨架序列。
- **大幅度运动下的外观保持**：PTCM 的部件级控制在主体发生大幅度旋转、遮挡或变形时仍能维持精细外观一致性。
- **需要相机运动控制的场景**：解耦 CFG 使得镜头运动成为独立可控维度。

#### 2.2 已知局限

根据论文披露的信息，以下局限需要注意：

- **训练数据的非完全公开性**：训练数据包含 15,000 个内部人类视频，这部分数据未公开，可能影响完全复现的公平性。不过 XPose 数据集已开源，为社区研究非人姿态生成提供了基础。
- **对骨架提取质量的依赖**：PTCM 的部件分割依赖于骨架提取的准确性。对于骨架提取困难的主体（如软体动物、流体形态），方法可能失效——这一点需要手动验证，论文未提供相关实验。
- **计算开销**：PTCM 在每个 DiT 块的交叉注意力层后插入额外的部件感知交叉注意力，增加了推理时的计算量。论文未提供与基线的推理速度对比，实际部署效率需要进一步评估。

### 3. 开放问题与未来方向

基于论文的方法设计和实验设置，以下开放问题值得关注：

1. **部件数量的自适应选择**：当前方法将主体按骨架段固定分割为多个部件，但不同主体（如蛇 vs. 人类）的合理部件粒度可能不同。是否存在自适应部件分割策略？

2. **多主体交互场景**：PoseAnything 当前处理单个主体的姿态驱动。在多主体交互场景（如两人搏击、动物群运动）中，PTCM 的部件匹配机制如何扩展？

3. **与 3D 先验的结合**：Champ 等方法利用 3D 参数模型（SMPL）提升人体动画的一致性。PoseAnything 的通用骨架方法能否与类别特定的 3D 先验结合，在已知类别上获得更强的几何约束？

4. **长时序稳定性**：部件感知交叉注意力依赖第一帧作为外观参考。在极长视频生成中，第一帧的外观信息可能不足以覆盖后续帧的视角变化和遮挡，是否需要引入动态更新的参考帧机制？

5. **相机控制的精细度**：解耦 CFG 当前支持离散的相机运动指令（如“pan left”）。能否扩展为连续的相机轨迹控制，实现更自然的镜头语言？



## 原文 PDF

![[paperPDFs/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.pdf]]
