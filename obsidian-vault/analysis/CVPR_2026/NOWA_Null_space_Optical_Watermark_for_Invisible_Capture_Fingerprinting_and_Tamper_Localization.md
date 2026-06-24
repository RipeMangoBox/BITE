---
title: "NOWA: Null-space Optical Watermark for Invisible Capture Fingerprinting and Tamper Localization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NOWA_Null_space_Optical_Watermark_for_Invisible_Capture_Fingerprinting_and_Tamper_Localization.pdf
project_link: null
code_link: null
aliases:
- NNSOW
- NOWA
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 由相位掩膜参数φ决定的成像算子零空间N(A_φ)。该零空间在光学上不可测量但在数学上被定义——通过优化相位掩膜设计可以精准控制零空间结构，从而创建一个传感器无法直接观测但可通过正向模型恢复的安全水印通道。
primary_logic: 利用成像算子的零空间作为安全水印嵌入域：相位掩膜将NOWA编码在传感器无法直接观测的零空间中，使其在拍摄时不可见；NSN在测量一致性约束下重建高质量保护图像，同时将水印锚定在保护图像中；验证时通过零空间投影Π_N提取签名，利用CNN检测篡改引起的零空间统计异常，实现像素级篡改定位。该设计建立了结构性的安全不对称性——没有光学参数和NSN参数，攻击者无法伪造NOWA签名。
claims:
- NOWA在Stable Diffusion编辑场景下达到F1=0.993, AUC=0.999, IoU=0.987，显著优于EditGuard的F1=0.966
- 零空间投影输入使检测性能从图像域直接检测的F1~0.75提升至接近完美，验证了零空间机制的有效性
- NOWA在JPEG Q=70压缩下仍保持F1=0.885, AUC=0.994，抵抗常见退化的能力强于纯数字方案
- 真实原型相机验证了仿真结果的可迁移性，成功检测并定位Photoshop编辑的篡改区域
---

# NOWA: Null-space Optical Watermark for Invisible Capture Fingerprinting and Tamper Localization

> [!tip] 核心洞察
> 利用成像算子的零空间作为安全水印嵌入域：相位掩膜将NOWA编码在传感器无法直接观测的零空间中，使其在拍摄时不可见；NSN在测量一致性约束下重建高质量保护图像，同时将水印锚定在保护图像中；验证时通过零空间投影Π_N提取签名，利用CNN检测篡改引起的零空间统计异常，实现像素级篡改定位。该设计建立了结构性的安全不对称性——没有光学参数和NSN参数，攻击者无法伪造NOWA签名。

| 字段 | 内容 |
|------|------|
| 中文题名 | NOWA：用于不可见拍摄指纹识别与篡改定位的零空间光学水印 |
| 英文题名 | NOWA: Null-space Optical Watermark for Invisible Capture Fingerprinting and Tamper Localization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.22501) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | NOWA (Null-space Optical Watermark) |
| Dataset | EditGuard test set, JPEG Compression Q=70, Gaussian Noise σ=5 |

> [!tip] 效果简介
> - EditGuard test set (COCO 2017, 1000 images) 上，F1 0.993 vs 0.966 (EditGuard) (+0.027)；AUC 0.999 vs 0.971 (EditGuard) (+0.028)；IoU 0.987 vs 0.936 (EditGuard) (+0.051)。
> - JPEG Compression Q=70 上，F1 0.885 vs 0.552 (EditGuard) (+0.333)；AUC 0.994 vs 0.875 (EditGuard) (+0.119)。
> - Gaussian Noise σ=5 上，F1 0.982 vs 0.871 (EditGuard) (+0.111)。

## 概述

### 问题背景

数字图像的真实性认证面临严峻挑战：生成式AI编辑工具（如Stable Diffusion、ControlNet、Photoshop Generative Fill）使图像篡改变得几乎无法察觉，而传统数字水印通常在拍摄后添加，容易被后期编辑或压缩去除。现有光学水印方案要么依赖复杂硬件（结构光投影、全息系统），要么以显著牺牲图像质量为代价。真正的瓶颈在于：**如何在图像形成的物理阶段嵌入对篡改敏感且不可见的认证线索，同时保持高质量重建**。

### 核心思想

NOWA提出了一种混合物理-数字认证范式，核心洞察是**利用成像算子的零空间作为安全水印嵌入域**。具体而言：

- **光学编码**：在相机孔径处安装定制相位掩膜，将NOWA编码在成像算子的零空间 $\mathcal{N}(\mathbf{A}_\phi)$ 中。该零空间内的信号经光学系统后传感器测量为零，因此在拍摄时完全不可见。
- **零空间重建**：零空间网络（NSN）在测量一致性约束下重建高质量保护图像，同时将水印锚定在保护图像中——$\mathbf{x}_p = \hat{\mathbf{x}}_r + \Pi_{\mathcal{N}} \mathcal{U}_\theta(\hat{\mathbf{x}}_r)$。
- **篡改检测**：验证时将保护图像投影到零空间提取签名图 $\mathbf{s} = \Pi_{\mathcal{N}}(\mathbf{x}_p)$，利用CNN检测篡改引起的零空间统计异常，实现像素级篡改定位。

这一设计建立了**结构性的安全不对称性**：没有相位掩膜参数和NSN参数，攻击者无法伪造NOWA签名——即使能生成视觉相似的伪造图像，也无法复现零空间签名。

### 方法谱系与知识库定位

NOWA在篡改检测方法谱系中占据独特位置。现有方法可分为两类：**被动取证方法**（如**MVSS-Net**、**PSCC-Net**、**IML-ViT** (Ma et al., arXiv 2023)、**HiFi-Net**、**OSN** (Wu et al., CVPR 2022)）分析图像统计异常但不主动嵌入保护信号，对高质量AIGC编辑效果有限；**主动保护方法**（如**EditGuard** (Zhang et al., CVPR 2024)）在拍摄后数字嵌入签名，但嵌入域位于图像空间或特征域，容易被压缩或编辑削弱。

NOWA的关键范式转换体现在四个维度：

| 设计维度 | 基线方案 | NOWA方案 |
|---------|---------|---------|
| 水印嵌入阶段 | 拍摄后数字嵌入 | 拍摄时通过相位掩膜在零空间光学嵌入 |
| 图像重建方式 | 标准反卷积或端到端去模糊 | NSN在测量一致性约束下重建，添加学习到的零空间分量 |
| 签名嵌入域 | 可见图像域（空间/频率域） | 成像算子零空间（光学不可测量，数学可恢复） |
| 篡改检测域 | 保护图像的图像域或特征域 | 保护图像的零空间投影，抑制自然变化、暴露不变签名 |

### 核心结果

NOWA在多项基准上取得显著优势：

- **AIGC编辑检测**（Stable Diffusion场景）：F1=0.993，AUC=0.999，IoU=0.987，全面超越EditGuard的F1=0.966（Table 1）。
- **鲁棒性**：JPEG Q=70压缩下仍保持F1=0.885 vs EditGuard的0.552（Table 2）；高斯噪声σ=5下F1=0.982 vs 0.871。
- **消融验证**：零空间投影输入使检测性能从图像域直接检测的F1~0.75提升至接近完美（Section 4.3, Figure 3）；移除学习到的相位掩膜后F1降至0.89，证实优化零空间对水印强度至关重要。
- **物理原型验证**：真实原型相机成功检测并定位Photoshop编辑的篡改区域（Figure 8），仿真结果可迁移至物理系统。

### 局限与开放问题

当前框架主要适用于景深范围内的场景；大景深变化或微距成像中PSF变为深度依赖，零空间结构随之变化。实际部署中残余零空间能量从仿真的~10⁻⁵升高到~10⁻⁴，且需针对每个相机原型进行PSF校准和网络微调。未来方向包括：深度感知校准策略、可编程光学元件实现动态零空间签名、以及针对近似成像算子攻击的增强防御。

## 背景与动机

### 数字图像认证的脆弱性

生成式人工智能（AIGC）的快速发展使图像编辑的门槛降至前所未有的低点。扩散模型、大语言模型驱动的图像修复工具可以在数秒内完成高度逼真的局部篡改，而传统取证方法——无论是基于像素统计异常的被动检测，还是拍摄后嵌入的数字水印——都面临结构性困境。

被动取证方法（如 **MVSS-Net**、**OSN** (Wu et al., CVPR 2022)、**PSCC-Net**、**IML-ViT** (Ma et al., arXiv 2023)、**HiFi-Net**）试图从图像内容本身发现篡改痕迹，但它们在面对高质量AIGC生成内容时，篡改区域与原始区域的统计分布差异正在消失。另一方面，主动数字水印方案（如 **EditGuard** (Zhang et al., CVPR 2024)）在拍摄完成后将签名嵌入图像域或特征域，但这意味着水印必须经受后续编辑、压缩、转码等操作的考验——任何能去除或覆盖水印的操作都将使认证失效。

### 现有光学水印方案的代价

将安全认证前移至图像形成阶段——即在拍摄时嵌入物理签名——是一条有前景的路径。然而，现有光学水印方案面临两难选择：要么依赖复杂硬件（如结构光投影系统、全息装置），增加部署成本和体积；要么以牺牲图像质量为代价，在可见域留下可察觉的嵌入痕迹。真正缺失的是一种在图像形成阶段嵌入、对篡改敏感、对视觉不可见、且无需额外投影硬件的物理认证机制。

### 核心瓶颈与本文动机

上述困境指向一个根本性瓶颈：**能否在成像过程中创建一个传感器无法直接观测、但可通过正向模型精确恢复的安全水印通道？**

NOWA 的核心洞察在于利用成像算子的数学结构来回答这个问题。具体而言，当相机孔径处插入一块精心设计的相位掩膜时，成像过程可建模为线性算子 $\mathbf{A}_\phi$。该算子的零空间 $\mathcal{N}(\mathbf{A}_\phi) = \{\mathbf{z} \mid \mathbf{A}_\phi \mathbf{z} = 0\}$ 具有一个关键性质：零空间内的任何信号经光学系统后，在传感器上的测量值为零——它在光学上完全不可观测，但在数学上被唯一定义。这构成了一个天然的安全嵌入域：水印在拍摄时不可见，但可通过零空间投影被精确恢复。

基于这一原理，NOWA 建立了一种**结构性的安全不对称性**：合法认证方持有相位掩膜参数 $\phi$ 和零空间网络参数 $\theta$，可精确提取并验证水印签名；而攻击者即使获得保护图像，在缺乏光学参数的情况下无法伪造有效的零空间签名。本文的动机正是充分挖掘这一不对称性，构建一个从光学编码、计算重建到篡改检测的完整认证流水线。

## 核心创新

NOWA的核心创新在于将水印的嵌入域从传统的图像域或频率域迁移到**成像算子的零空间**，构建了一条光学上不可观测但数学上可恢复的安全水印通道。这一结构性转变带来了四个关键的技术突破，每个突破都对应着对现有方案的实质性改进。

### 创新一：零空间光学嵌入——从拍摄后到拍摄时

传统数字水印方案（如EditGuard、HiDDeN）在图像拍摄完成后在图像域或特征域嵌入签名，水印与图像内容共存于同一表示空间，因此容易受到后期编辑、压缩或噪声的破坏。NOWA将水印嵌入时机前移至**图像形成阶段**：通过在相机孔径处放置参数为φ的相位掩膜，对入射光场进行调制，将NOWA编码在成像算子A_φ的零空间N(A_φ)中。该零空间定义为：

$$\mathcal{N}(\mathbf{A}_\phi) = \{\mathbf{z} \mid \mathbf{A}_\phi \mathbf{z} = 0\}$$

零空间内的信号经光学系统后传感器测量为零，在光学上完全不可观测。这意味着NOWA在拍摄时即被物理嵌入，但在传感器捕获的原始图像中**不可见**——水印与图像内容在测量层面实现了结构性分离，而非仅在像素值上叠加。

### 创新二：测量一致性重建——零空间网络NSN

传统方案在嵌入水印后通常需要端到端的去模糊或增强网络来恢复图像质量，但这些网络可能破坏水印的完整性。NOWA引入**零空间网络**（Null-Space Network, NSN）f_θ，在严格的测量一致性约束下重建保护图像：

$$\mathbf{x}_p = f_{\theta}(\hat{\mathbf{x}}_r) = \hat{\mathbf{x}}_r + \Pi_{\mathcal{N}} \mathcal{U}_\theta(\hat{\mathbf{x}}_r)$$

其中x̂_r为正则化估计，Π_N为零空间投影算子，U_θ为网络学习的零空间分量。这一设计的精妙之处在于：NSN仅在零空间中添加学习到的分量，保证重建结果严格满足A_φ f_θ(x̂_r) = A_φ x̂_r = y，即重建图像的光学测量与原始测量完全一致。这使得NSN在提升图像质量的同时，将NOWA签名**锚定**在保护图像中，两者互不干扰。

### 创新三：零空间投影检测——抑制自然变化、暴露不变签名

现有篡改检测方法直接在保护图像x_p的图像域或特征域进行判别，容易受到自然图像变化（纹理、光照、内容差异）的干扰，产生大量误报。NOWA将检测域迁移到零空间：对保护图像进行零空间投影，提取签名图：

$$\mathbf{s} = \Pi_{\mathcal{N}}(\mathbf{x}_p) = \Pi_{\mathcal{N}} \mathcal{U}_\theta(\hat{\mathbf{x}}_r)$$

利用Π_N(x̂_r)=0和Π_N²=Π_N的性质，签名图s仅包含NSN在零空间中嵌入的水印信息，自然图像变化被完全抑制。CNN检测器d_ψ对s进行像素级分类，输出真实性概率图m ∈ [0,1]^n。消融实验（Figure 3）证实了这一设计的决定性作用：使用图像域直接检测时F1仅约0.75，而零空间投影输入使检测性能提升至接近完美（F1=0.993），验证了零空间投影有效抑制自然图像变化、暴露不变水印签名的机制。

### 创新四：结构性安全不对称

上述三个创新共同构建了一种**结构性安全不对称**：NOWA签名由相位掩膜参数φ和NSN参数θ共同定义，嵌入在成像算子的零空间中。攻击者若想伪造有效的NOWA签名，必须同时掌握：

1. **光学参数φ**：决定零空间的结构和NOWA的编码方式；
2. **NSN参数θ**：决定零空间中嵌入的具体签名模式。

即使攻击者能够获取保护图像x_p，由于零空间在光学上不可测量，无法从单一图像中分离出签名分量。对抗攻击实验（Figure 4）验证了这一安全性：在三种攻击场景（相机模仿、保护图像模仿、混合攻击）下，NOWA检测F1分别为0.901、0.913和0.946，攻击者无法伪造有效的零空间签名。移除学习到的相位掩膜后检测F1降至0.89，进一步证明优化设计的零空间对水印强度和安全性至关重要。

### 创新总结：Changed Slots一览

| 设计维度 | 传统方案 | NOWA方案 | 创新本质 |
|---------|---------|---------|---------|
| 水印嵌入阶段 | 拍摄后数字嵌入 | 拍摄时光学嵌入 | 时机前移，物理绑定 |
| 图像重建方式 | 标准反卷积/端到端网络 | 测量一致性NSN重建 | 零空间约束，签名锚定 |
| 篡改检测域 | 图像域/特征域 | 零空间投影域 | 抑制自然变化，暴露签名 |
| 签名嵌入域 | 可见图像域 | 成像算子零空间 | 光学不可见，数学可恢复 |

这四个changed slots并非独立的改进，而是围绕**零空间作为安全水印通道**这一核心洞察的有机整体：光学嵌入创建通道，NSN重建锚定签名，零空间投影提取签名，三者共同实现了从“拍摄后添加”到“拍摄时嵌入”、从“图像域隐藏”到“零空间分离”的范式转变。

## 整体框架

NOWA提出了一种混合物理-数字的脆弱认证流水线，其核心思想是在图像形成阶段——而非拍摄之后——将不可见的水印签名嵌入成像算子的零空间中。该流水线由四个紧密耦合的模块构成，形成一条从光学编码到篡改检测的端到端可训练链路。

### 流水线总览

如图1所示，系统分为两个阶段：**(a) 光学-数字指纹嵌入**与**(b) 图像验证**。

**嵌入阶段**的输入为自然场景 $\mathbf{x}$。首先，安装在相机孔径处的相位掩膜 $g_\phi$ 对入射光场进行调制，将场景经光学系统编码为传感器测量 $\mathbf{y} = g_\phi(\mathbf{x})$。这一光学编码过程的核心机制在于：相位掩膜参数 $\phi$ 决定了成像算子 $\mathbf{A}_\phi$ 的零空间结构 $\mathcal{N}(\mathbf{A}_\phi) = \{\mathbf{z} \mid \mathbf{A}_\phi \mathbf{z} = 0\}$，该零空间内的信号在光学上完全不可观测——传感器对其测量响应为零。NOWA签名正是被嵌入这一“光学盲区”中，从而在拍摄时对传感器不可见。

随后，零空间网络（Null-Space Network, NSN）$f_\theta$ 在测量一致性约束下从编码测量 $\mathbf{y}$ 重建高质量保护图像 $\mathbf{x}_p$：

$$\mathbf{x}_p = f_{\theta}(\hat{\mathbf{x}}_r) = \hat{\mathbf{x}}_r + \Pi_{\mathcal{N}} \mathcal{U}_\theta(\hat{\mathbf{x}}_r)$$

其中 $\hat{\mathbf{x}}_r$ 为正则化估计（如Wiener反卷积结果），$\Pi_{\mathcal{N}}$ 为零空间投影算子，$\mathcal{U}_\theta$ 为NSN学习到的零空间分量生成网络。该设计的精妙之处在于：NSN仅在零空间中添加学习到的分量，严格保证 $\mathbf{A}_\phi f_\theta(\hat{\mathbf{x}}_r) = \mathbf{A}_\phi \hat{\mathbf{x}}_r = \mathbf{y}$，即重建图像与传感器测量保持完全一致。这一测量一致性约束同时将NOWA签名锚定在保护图像 $\mathbf{x}_p$ 中。

**验证阶段**的输入为待检测图像。系统将其投影到成像算子零空间，提取签名图：

$$\mathbf{s} = \Pi_{\mathcal{N}}(\mathbf{x}_p) = \Pi_{\mathcal{N}} \mathcal{U}_\theta(\hat{\mathbf{x}}_r)$$

利用 $\Pi_{\mathcal{N}}(\hat{\mathbf{x}}_r) = 0$ 和 $\Pi_{\mathcal{N}}^2 = \Pi_{\mathcal{N}}$ 的性质，签名图 $\mathbf{s}$ 仅包含NSN注入的零空间分量，自然图像内容被完全抑制。最后，CNN检测器 $d_\psi$ 对签名图进行像素级分类，输出真实性概率图 $\mathbf{m} = d_\psi(\mathbf{s})$，其中 $m_i \in [0,1]$ 表示每个像素未被篡改的概率。

### 模块间因果链路

四个模块之间的因果链路构成了NOWA的安全不对称性基础：

1. **光学编码模块 $g_\phi$** 创建了物理层面的安全通道——零空间在光学上不可测量，但其结构完全由相位掩膜参数 $\phi$ 决定。没有 $\phi$ 的知识，攻击者无法获知零空间的基向量。

2. **NSN重建模块 $f_\theta$** 在测量一致性约束下将NOWA锚定在保护图像中。NSN的参数 $\theta$ 与相位掩膜 $\phi$ 联合优化，使得注入的零空间分量既保持图像质量，又对篡改高度敏感。

3. **零空间投影模块 $\Pi_{\mathcal{N}}$** 充当“签名解码器”——将保护图像映射回零空间，隔离出纯净的水印签名。这一步骤是检测性能的关键：消融实验表明，直接在图像域检测的F1仅约0.75，而零空间投影输入使检测性能提升至接近完美（F1≈0.993），验证了零空间投影有效抑制自然图像变化、暴露不变水印签名的机制。

4. **CNN检测器 $d_\psi$** 学习区分零空间签名中的“正常系统噪声”与“篡改引起的异常”。由于NOWA签名由光学过程物理锚定，任何像素级篡改都会破坏测量一致性，在零空间投影中产生可检测的统计异常。

### 端到端联合训练

整个流水线通过联合优化损失函数端到端训练：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rec}} + \beta \mathcal{L}_{\mathrm{perc}} + \lambda \mathcal{L}_{\mathrm{cls}}$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为L2重建损失（保证图像质量），$\mathcal{L}_{\mathrm{perc}}$ 为感知特征损失（保持纹理和结构），$\mathcal{L}_{\mathrm{cls}}$ 为像素级二值交叉熵分类损失（监督篡改检测）。训练时，相位掩膜参数 $\phi$、NSN参数 $\theta$ 和检测器参数 $\psi$ 同步更新，使光学编码、图像重建和篡改检测三个目标协同优化。模型在FFHQ数据集上训练，在COCO 2017的EditGuard测试集上评估，验证了跨域泛化能力。

### 安全不对称性的结构性来源

NOWA的安全保障根植于其物理-数字混合架构的结构性不对称：攻击者若想伪造有效的NOWA签名，必须同时掌握光学参数 $\phi$（获取零空间结构）和NSN参数 $\theta$（生成正确的零空间分量）。即使攻击者拥有大量配对数据 $(\mathbf{x}_p, \mathbf{y})$ 并尝试学习近似成像算子，对抗实验表明NOWA在此类攻击下仍保持F1=0.901–0.946的检测性能。移除学习到的相位掩膜后，检测F1降至0.89，进一步证明优化设计的零空间对水印强度和稳定性至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/001_Figure_1.jpg]]
*Figure 1: A hybrid physical-digital pipeline for fragile authentication. (a) Optical-digital fingerprint: A phase mask (PM) in the camera aperture optically encodes the scene, embedding a unique physical signature before digitization. A neural network*

## 核心模块与公式推导

NOWA的核心架构由四个功能模块串联构成，形成一条从光学编码到像素级篡改定位的完整流水线。

### 模块一：光学编码模块 $g_\phi$

该模块在相机孔径处引入一片可学习的相位掩膜，对入射光场进行波前调制。掩膜的高度轮廓由截断Zernike多项式展开参数化：

$$h_\phi(x,y) = \sum_{k=1}^{K} \phi_k Z_k(x,y)$$

其中 $\phi_k$ 为可学习系数，$Z_k(x,y)$ 为第 $k$ 阶Zernike基函数。掩膜引入的波长依赖相位延迟为：

$$\phi_M(x,y) = k (n_M(\lambda)-1) h_\phi(x,y)$$

与透镜传输函数 $t_L(x,y) = \exp(-i \frac{k}{2f}(x^2+y^2))$ 结合后，完整的瞳孔函数为 $P(x,y) = A(x,y) t_L(x,y) t_M(x,y)$。该瞳孔函数决定了成像算子的点扩散函数（PSF），进而定义了整个光学前向模型 $g_\phi$。

**关键机制**：相位掩膜的设计使得成像算子 $\mathbf{A}_\phi$ 存在一个非平凡的零空间：

$$\mathcal{N}(\mathbf{A}_\phi) = \{\mathbf{z} \mid \mathbf{A}_\phi \mathbf{z} = 0\}$$

该零空间内的信号经光学系统后，在传感器上的测量值为零——即光学上完全不可观测。这构成了NOWA的安全嵌入域：水印在拍摄时即被物理编码，但传感器无法直接感知。

### 模块二：零空间网络重建模块 $f_\theta$ (NSN)

传感器获得编码测量 $\mathbf{y} = \mathbf{A}_\phi \mathbf{x}$ 后，NSN负责在测量一致性约束下重建高质量保护图像。其核心公式为：

$$\mathbf{x}_p = f_\theta(\hat{\mathbf{x}}_r) = \hat{\mathbf{x}}_r + \Pi_{\mathcal{N}} \mathcal{U}_\theta(\hat{\mathbf{x}}_r)$$

其中 $\hat{\mathbf{x}}_r$ 为通过正则化反演获得的初始估计，$\mathcal{U}_\theta$ 为可学习网络，$\Pi_{\mathcal{N}}$ 为零空间投影算子。该设计的精妙之处在于：

- **测量一致性保证**：$\mathbf{A}_\phi f_\theta(\hat{\mathbf{x}}_r) = \mathbf{A}_\phi \hat{\mathbf{x}}_r = \mathbf{y}$，因为添加的零空间分量经 $\mathbf{A}_\phi$ 后为零
- **水印锚定**：NSN在零空间中学习添加特定的结构化分量，将NOWA签名锚定在保护图像中，同时提升重建质量

### 模块三：零空间投影模块 $\Pi_{\mathcal{N}}$

验证阶段，将保护图像 $\mathbf{x}_p$ 投影到零空间以提取签名图：

$$\mathbf{s} = \Pi_{\mathcal{N}}(\mathbf{x}_p) = \Pi_{\mathcal{N}} \mathcal{U}_\theta(\hat{\mathbf{x}}_r)$$

该步骤利用了两个关键性质：$\Pi_{\mathcal{N}}(\hat{\mathbf{x}}_r) = 0$（正则化估计不含零空间分量）和 $\Pi_{\mathcal{N}}^2 = \Pi_{\mathcal{N}}$（投影幂等性）。签名图 $\mathbf{s}$ 隔离了NSN嵌入的零空间水印，同时抑制了自然图像内容的变化——这是检测性能从图像域直接检测的F1~0.75跃升至接近完美的根本原因（参见Figure 3消融实验）。

### 模块四：CNN篡改检测器 $d_\psi$

检测器对签名图进行像素级二分类，输出真实性概率图：

$$\mathbf{m} = d_\psi(\mathbf{s})$$

其中 $m_i \in [0,1]$ 表示第 $i$ 像素为真实的概率。检测器学习区分两类零空间异常：系统固有的可预测噪声（由校准误差、制造公差引起）与篡改引入的测量不一致性残差。

### 端到端联合训练

整个流水线通过联合损失端到端优化：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rec}} + \beta \mathcal{L}_{\mathrm{perc}} + \lambda \mathcal{L}_{\mathrm{cls}}$$

- $\mathcal{L}_{\mathrm{rec}}$：L2重建损失，约束保护图像与原始场景的保真度
- $\mathcal{L}_{\mathrm{perc}}$：感知特征损失，保持纹理和结构质量
- $\mathcal{L}_{\mathrm{cls}}$：像素级二值交叉熵分类损失，驱动检测精度
- $\beta$ 和 $\lambda$ 平衡图像质量与检测性能的权衡

**核心洞察**：该流水线建立了结构性的安全不对称性——相位掩膜参数 $\phi$ 和NSN参数 $\theta$ 共同定义了零空间签名。攻击者即使拥有保护图像，若不知道光学参数和网络参数，也无法伪造有效的零空间签名（消融实验表明，移除学习到的相位掩膜后检测F1降至0.89）。

### 补充图表

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative ablation of detector input. Comparison of detected tamper when input to*

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/008_Figure_6.jpg]]
*Figure 6: Optical encoding. A commercial YONGNUO lens is disassembled to attach the design phase mask on the back side of the lens aperture. The inset shows the quantized designed phase mask*

## 实验与分析

### 实验设置

NOWA的训练在FFHQ数据集上进行，评估则使用EditGuard测试集（包含1000张来自COCO 2017的图像），验证了跨域泛化能力。所有基线方法均使用官方实现和推荐配置，在五种代表性AIGC编辑流程（Stable Diffusion、ControlNet、SDXL、RePaint、Lama）上统一评估。评估指标统一采用F1分数、AUC和IoU。模型在单块NVIDIA H100 GPU (80 GB)上训练，使用AdamW优化器（学习率1e-4，权重衰减1e-2，批量大小32）。

### 主实验结果

Table 1展示了NOWA与多种先进篡改定位方法在五种AIGC编辑场景下的定量比较。在Stable Diffusion编辑场景中，NOWA达到F1=0.993、AUC=0.999、IoU=0.987，显著优于次优方法**EditGuard**（Zhang et al., CVPR 2024）的F1=0.966、AUC=0.971、IoU=0.936，IoU提升达5.1个百分点。在其他四种编辑方法（ControlNet、SDXL、RePaint、Lama）上，NOWA同样保持一致的领先优势，验证了混合光学-数字框架在多种编辑范式下的鲁棒性。

与其他纯数字检测方法（**MVSS-Net**、**OSN** Wu et al., CVPR 2022、**PSCC-Net**、**IML-ViT** Ma et al., arXiv 2023、**HiFi-Net**）相比，NOWA的性能优势更为显著——这些方法缺乏物理层面的认证线索，在AIGC编辑场景下定位精度明显不足。Figure 2的定性比较进一步证实：NOWA生成的篡改定位掩膜更精确地覆盖编辑区域，同时更好地保持结构细节，而基线方法常出现边界模糊或漏检。

### 鲁棒性分析

Table 2报告了在噪声和JPEG压缩退化下的篡改定位鲁棒性。在JPEG Q=70强压缩下，NOWA保持F1=0.885、AUC=0.994，而EditGuard降至F1=0.552、AUC=0.875，NOWA的F1优势达+0.333。在高斯噪声σ=5条件下，NOWA的F1=0.982，EditGuard为0.871，优势+0.111。这一鲁棒性优势源于NOWA在成像阶段嵌入物理签名——光学水印对后期数字退化具有天然的抗性，而纯数字方案在压缩和噪声下签名信息易被破坏。

### 消融实验

**零空间投影的有效性。** Section 4.3和Figure 3揭示了检测器输入域的关键作用。当检测器d_ψ直接以保护图像x_p（图像域）作为输入时，检测性能仅为F1≈0.75、AUC≈0.82、IoU≈0.69，且出现大量散在假阳性。当输入切换为零空间投影Π_N(x_p)时，检测性能提升至接近完美。这一对比验证了核心设计原理：零空间投影有效抑制自然图像变化，暴露不变的水印签名，使CNN检测器能够专注于篡改引起的零空间统计异常。

**学习型相位掩膜的必要性。** 移除学习到的相位掩膜后（Section 4.3），检测性能降至F1=0.89、IoU=0.81。这表明端到端优化设计的零空间结构对NOWA的嵌入强度、稳定性和判别力至关重要——随机或非优化的相位掩膜无法创建有效的安全水印通道。

### 安全性评估

Section 4.4和Figure 4评估了三种对抗攻击场景下的系统安全性：（1）**相机模仿攻击**——攻击者尝试复制光学系统生成伪造保护图像；（2）**保护图像模仿攻击**——攻击者直接模仿保护图像外观；（3）**混合攻击**——结合上述两种策略。NOWA检测F1分别为0.901、0.913、0.946。尽管伪造图像在视觉外观上高度相似，但无法复现底层零空间签名，验证了结构安全不对称性——没有光学参数φ和NSN参数θ，攻击者无法伪造有效的NOWA签名。

### 真实原型验证

Figure 8展示了真实原型相机（Figure 6）的实验结果。使用商业YONGNUO镜头改装，在孔径处安装3D光刻制造的相位掩膜（Figure 7验证了仿真PSF与实测PSF的结构一致性）。对真实拍摄的保护图像进行Photoshop编辑后，检测器成功定位篡改区域，IoU分数证实了仿真结果向物理系统的可迁移性。

### 失败模式与局限性

尽管NOWA在仿真和原型实验中表现优异，仍存在以下局限：

1. **深度依赖性**：当前框架假设场景在景深范围内，PSF近似不变。在大景深变化或微距场景中，PSF变为深度依赖，零空间结构随之变化，检测性能可能退化。
2. **残余光谱泄漏**：实际原型中残余零空间能量从仿真的~10⁻⁵升高至~10⁻⁴（源于校准误差和光轴对准偏差），虽然仍远低于篡改异常，但表明存在轻微的信息泄漏。
3. **制造公差影响**：相位掩膜的双光子聚合3D光刻层间台阶误差和光轴对准偏差引入额外光学畸变，影响零空间估计精度。
4. **对抗学习威胁**：攻击者若拥有大量配对数据(x_p, y)，可能尝试学习近似成像算子以伪造签名。论文初步评估显示此类攻击下F1降至0.901-0.946，但防御策略仍需进一步探索。
5. **部署复杂度**：每个相机原型需进行实测PSF校准和NSN/检测器微调，增加了部署工作量和数据采集成本。

### 补充图表

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/002_Table_1.jpg]]
*Table 1: Comparison with other competitive tamper localization methods under different AIGC-based editing methods*

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/003_Figure_2.jpg]]
*Figure 2: Qualitative comparison between the proposed method and state-of-the-art approaches. Our method produces more precise localization of manipulated regions and better preserves structural details compared to existing techniques*

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/005_Figure_4.jpg]]
*Figure 4: Robustness of the proposed system against generative and analytical adversaries. For each attack, we show the protected image produced by our system*

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/006_Table_2.jpg]]
*Table 2: Comparison of tampering localization under different levels of noise and compression degradations*

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/007_Figure_5.jpg]]
*Figure 5: Tamper localization from real captures. Each column shows (top) the protected image with the target edit region outlined in green, and (bottom) the tampered image with the estimated manipulation mask overlaid in translucent red. Edits were manually made using Photoshop tools. The IoU scores below each example indicate strong localization accuracy and robust detection of real digital edits, as supported by the visual results*

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/009_Figure_7.jpg]]
*Figure 7: PSF Calibration. Comparison between the optimized simulated PSF (left) and the experimentally measured PSF from the physical prototype (right). The similarity in structure confirms the fidelity of the fabrication process*

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/010_Figure_8.jpg]]
*Figure 8: Real-world prototype results. From left to right: raw capture y, protected reconstruction*

![[assets/figures/papers/paper_list_l2107_https_arxiv_org_abs_2512_22501/figures/011_Figure_8.jpg]]
*Figure 8: (cont.). Real-world prototype results. From left to right: raw capture y, protected reconstruction*

## 方法谱系与知识库定位

### 从数字嵌入到光学-数字混合：水印域的范式转移

传统数字水印方案（如HiDDeN、EditGuard）在拍摄完成后于图像域或特征域嵌入签名，其根本脆弱性在于：水印与图像内容共享同一表示空间，后期编辑、压缩或噪声攻击可直接破坏水印结构。NOWA的核心突破在于将水印嵌入域从**可观测的图像空间**迁移至**成像算子的零空间** $\mathcal{N}(\mathbf{A}_\phi) = \{\mathbf{z} \mid \mathbf{A}_\phi \mathbf{z} = 0\}$——该空间内的信号经光学系统后传感器测量为零，在物理上完全不可见，但可通过正向模型数学恢复。这一设计建立了**结构性的安全不对称性**：合法验证者持有光学参数 $\phi$ 和零空间网络参数 $\theta$，可精准提取签名；攻击者即使获得保护图像 $\mathbf{x}_p$，也无法在缺乏光学参数的情况下伪造有效的零空间签名。

### 与现有篡改检测方法的根本差异

现有像素级篡改定位方法可分为两类范式，NOWA与它们存在本质区别：

**无监督/自监督检测方法**（如MVSS-Net、PSCC-Net、OSN (Wu et al., CVPR 2022)、HiFi-Net）依赖图像内容的统计异常或语义不一致性来识别篡改区域。这类方法的致命弱点是：当AIGC编辑（如Stable Diffusion inpainting、ControlNet局部重绘）产生的篡改区域与原始内容在统计和语义上高度一致时，异常信号消失。Table 1的数据证实了这一点——OSN在Stable Diffusion编辑场景下F1仅0.276，MVSS-Net仅0.316，几乎失效。NOWA不依赖内容异常，而是检测**零空间签名的测量一致性破坏**：篡改操作在图像域引入的修改无法满足成像算子的零空间约束，导致 $\Pi_{\mathcal{N}}(\mathbf{x}_{\text{tampered}})$ 产生可检测的统计偏差。

**主动水印方法**（以EditGuard (Zhang et al., CVPR 2024)为代表）在拍摄后嵌入可验证签名，但面临两个瓶颈：(1) 水印嵌入与图像质量存在根本权衡——强水印降低视觉质量，弱水印易被破坏；(2) 水印在图像域易受压缩和噪声退化。Table 2显示，EditGuard在JPEG Q=70压缩下F1从0.966骤降至0.552，而NOWA保持F1=0.885——差距达+0.333。这是因为NOWA的签名锚定在物理成像过程中，与图像内容解耦，对像素域退化具有天然鲁棒性。

### 技术谱系中的定位：混合物理-数字计算成像

NOWA属于**混合物理-数字计算成像**与**光学安全**的交叉领域。其技术祖先可追溯至：

- **编码孔径与相位掩膜成像**：利用相位掩膜进行景深扩展或计算成像的传统工作（如wavefront coding）仅关注图像质量，NOWA首次将相位掩膜设计目标从“最大化可恢复信息”转向“创建安全零空间通道”。
- **光学物理不可克隆函数（PUF）**：利用制造过程中的随机物理变化作为设备指纹，但通常需要额外硬件且签名不可控。NOWA通过**可优化的相位掩膜**实现了可控、可学习的物理签名。
- **零空间学习与测量一致性重建**：NSN的架构 $f_{\theta}(\hat{\mathbf{x}}_r) = \hat{\mathbf{x}}_r + \Pi_{\mathcal{N}} \mathcal{U}_\theta(\hat{\mathbf{x}}_r)$ 借鉴了即插即用（PnP）和深度均衡模型的测量一致性思想，但创新性地将零空间分量 $\Pi_{\mathcal{N}} \mathcal{U}_\theta$ 同时用于图像质量提升和签名嵌入，实现了“一石二鸟”的联合优化。

### 适用边界与关键假设

NOWA的有效性建立在以下假设之上，违反任一条将导致性能退化：

1. **景深范围内成像**：当前框架假设PSF在场景深度范围内近似不变。在大景深变化或微距成像场景中，PSF变为深度依赖函数 $\mathbf{A}_{\phi}(d)$，零空间结构随之变化，导致签名提取失效。这是论文明确指出的首要局限。
2. **相位掩膜制造精度**：零空间结构对相位掩膜的高度剖面 $h_\phi(x,y)$ 敏感。实际制造中，双光子聚合3D光刻的层间台阶误差和光轴对准偏差会引入额外的光学畸变——论文报告残余零空间能量从仿真中的 $\sim 10^{-5}$ 升高到实际拍摄中的 $\sim 10^{-4}$，虽仍远低于篡改引起的异常，但表明存在轻微的光谱泄漏。
3. **攻击者知识边界**：安全不对称性依赖于攻击者无法获取光学参数 $\phi$ 和NSN参数 $\theta$。若攻击者拥有大量配对数据 $(\mathbf{x}_p, \mathbf{y})$，可能尝试学习近似成像算子以伪造签名。论文初步评估了此类攻击场景（F1=0.901-0.946，Figure 4），表明系统保持一定鲁棒性但并非完全免疫。
4. **每设备校准需求**：真实部署需针对每个相机原型进行实测PSF校准和NSN/检测器微调（Figure 7展示了仿真PSF与实测PSF的对比），增加了部署复杂度和数据采集工作量。

### 局限性与开放问题

**已知局限**（论文明确讨论）：

- **深度依赖PSF问题**：当前框架仅适用于景深范围内的场景，无法处理大景深变化或微距成像。需要扩展深度感知校准策略，如校准一组深度依赖的PSF或引入深度条件NSN。
- **制造公差与对准误差**：光学元件的制造公差和光轴对准偏差会引入额外的光学畸变，影响零空间估计精度。实际部署需要更鲁棒的校准流程。
- **对抗学习攻击的防御**：虽然初步评估了相机模仿、保护图像模仿和混合攻击三种场景，但更复杂的自适应攻击（如基于扩散模型的零空间签名伪造）仍需进一步探索。
- **部署复杂度**：每个相机原型需要实测PSF校准和模型微调，限制了规模化部署的便捷性。

**开放问题**（论文未解决但值得探索的方向）：

- **动态可切换零空间签名**：当前框架仅考虑单一相位掩膜设计。能否通过可编程光学元件（如空间光调制器SLM）实现可动态切换的零空间签名，以支持多设备认证或时效性签名需求？
- **深度感知零空间设计**：能否在相位掩膜优化阶段显式建模深度维度，设计深度感知的零空间结构，使NOWA适用于更广泛的三维真实场景？
- **密钥化安全增强**：能否在零空间签名中引入基于密钥的随机化或数字嵌入层，进一步增强安全性，防御利用大量配对数据集近似成像算子的攻击？这将是物理签名与数字密码学的深度融合方向。
- **自动化部署流水线**：能否开发自动化PSF测量和在线微调流程，降低实际部署的校准门槛和人工干预需求？
- **多光谱扩展**：当前框架基于单波长模型。能否扩展至多光谱或高光谱成像，利用不同波长的零空间差异实现更丰富的签名容量？

## 原文 PDF

![[paperPDFs/CVPR_2026/NOWA_Null_space_Optical_Watermark_for_Invisible_Capture_Fingerprinting_and_Tamper_Localization.pdf]]
