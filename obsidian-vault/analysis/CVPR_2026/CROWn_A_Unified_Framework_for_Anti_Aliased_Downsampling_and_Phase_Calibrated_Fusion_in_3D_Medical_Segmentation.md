---
title: "CROWn: A Unified Framework for Anti-Aliased Downsampling and Phase-Calibrated Fusion in 3D Medical Segmentation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CROWn_A_Unified_Framework_for_Anti_Aliased_Downsampling_and_Phase_Calibrated_Fusion_in_3D_Medical_Segmentation.pdf
project_link: null
code_link: "https://github.com/IMOP-lab/CROWn"
aliases:
- CCFMLCAN
- CROWn
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入多相协同注意力与显式抗混叠滤波的降采样（µPCAD）以及八相位陪集分解与边沿门控的跳连接校准（OCF），可主动抑制混叠并保留边界相关高频成分，从而稳定边界定位。
primary_logic: 将采样理论（多相分析、陪集分解）与深度表征学习（交叉源协同注意力、相位注意力、边沿门控）相结合，联合解决降采样中的混叠抑制和跳连接的对齐问题，实现了各向异性和异质扫描条件下的一致精细分割。
claims:
- CROWn在15个公开基准上均取得最佳的IoU和Dice，有效降低了HD95。
- µPCAD在所有编码器降采样阶段部署时带来最稳定的性能提升，验证了逐级抗混叠的必要性。
- 将µPCAD插入CNN、Transformer、ConvNeXt和Mamba等不同骨干网络，一致提升重叠和边界指标，证明其通用性。
- OCF的八相位陪集分解、相位注意力和边沿门控对跳连接校准具有可加性的贡献，在FLARE2022上得到验证。
---

# CROWn: A Unified Framework for Anti-Aliased Downsampling and Phase-Calibrated Fusion in 3D Medical Segmentation

> [!tip] 核心洞察
> 将采样理论（多相分析、陪集分解）与深度表征学习（交叉源协同注意力、相位注意力、边沿门控）相结合，联合解决降采样中的混叠抑制和跳连接的对齐问题，实现了各向异性和异质扫描条件下的一致精细分割。

| 字段 | 内容 |
|------|------|
| 中文题名 | CROWn：面向三维医学分割的抗混叠降采样与相位校准融合统一框架 |
| 英文题名 | CROWn: A Unified Framework for Anti-Aliased Downsampling and Phase-Calibrated Fusion in 3D Medical Segmentation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Huang_CROWn_A_Unified_Framework_for_Anti-Aliased_Downsampling_and_Phase-Calibrated_Fusion_CVPR_2026_paper.html) · [Code](https://github.com/IMOP-lab/CROWn) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CROWn (Coset-fibRated micrO-local co-attention Network) |
| Dataset | MSD Pancreas Tumour, MSD Lung Tumour, MSD BRATS Tumour, FLARE2022 |

> [!tip] 效果简介
> - MSD Pancreas Tumour 上，IoU / Dice / HD95 79.16 / 87.26 / 3.12 vs Best competing method (see Table 1) (N/A)。
> - MSD Lung Tumour 上，IoU / Dice / HD95 82.65 / 89.76 / 4.30 vs Best competing method (see Table 1) (N/A)。
> - MSD BRATS Tumour 上，IoU / Dice / HD95 84.05 / 91.05 / 2.86 vs Best competing method (see Table 1) (N/A)。

## 概述

三维医学图像分割面临一个普遍但常被忽视的瓶颈：各向异性的体素间距导致编码器下采样过程中产生混叠伪影，同时跳连接中的高分辨率特征与解码器特征之间存在相位失准。这两者共同引发边界模糊、拓扑断裂和细小结构泄漏，尤其在高异质性扫描（如CT与MRI之间）下更为严重。现有U形网络（如**3D U-Net**（Cicek et al., MICCAI 2016）、**UNETR**（Hatamizadeh et al., WACV 2022）、**SwinUNETR**（Hatamizadeh et al., MICCAI 2022）、**MedNeXt**（Roy et al., MICCAI 2023）、**SegMamba**（Xing et al., MICCAI 2024）等）普遍依赖步长卷积或池化进行降采样，缺乏显式的抗混叠控制，且跳连接采用直接拼接，未对跨尺度特征的相位一致性进行校准。

CROWn（Coset-fibRated micrO-local co-attention Network）针对上述问题，将采样理论与深度表征学习相耦合，提出了一个统一的抗混叠降采样与相位校准融合框架。其核心贡献包括两个模块：

- **µPCAD（微局部多相协同注意力降采样器）**：在编码器各降采样阶段执行轴感知的多相分析，通过池化-子带协同注意力将方向性高频证据路由至低分辨率网格，并施加显式抗混叠低通滤波，在抑制混叠的同时保留边界相关成分。
- **OCF（八相位陪集融合模块）**：在跳连接路径上，先对高分辨率特征进行抗混叠预滤波，再通过三维空间到深度转换将其分解为八个陪集，利用相位注意力与Sobel边缘门控进行加权聚合，最终以深度可分离卷积生成紧凑、相位对齐且边界感知的跳连接特征。

在15个公开基准上的系统实验表明，CROWn在所有数据集上均取得了最佳的IoU和Dice指标，并在各向异性队列和细粒度结构数据上展现出显著的边界连贯性提升。消融研究进一步证实，µPCAD在所有编码器阶段部署时带来最稳定的性能增益，且其抗混叠降采样策略优于SE、CBAM等经典模块；OCF的八相位分解、相位注意力和边缘门控对跳连接校准具有可加性贡献。CROWn以23.78M参数和199.58G FLOPs的可控计算成本，在CT、MRI、OCT等多模态上实现了跨域鲁棒的一致精细分割。

## 背景与动机

三维医学图像分割是临床诊断与手术规划的核心技术。然而，医学影像数据普遍存在**各向异性体素间距**——CT扫描的层内分辨率通常远高于层间分辨率，MRI和OCT数据同样面临类似的非均匀采样问题。这种空间分辨率的异质性在U形分割网络中引发了两个深层瓶颈：

1. **下采样混叠**：编码器中的步长卷积或池化操作在降采样时未进行显式抗混叠滤波，导致高频成分折叠为低频伪影，模糊了器官边界和细小结构的空间定位信息。
2. **跨尺度相位失准**：跳连接直接将高分辨率编码器特征与低分辨率解码器特征拼接，但两者在空间格点上存在相位偏移，使得融合时边界证据无法精确对齐，造成拓扑断裂和边界泄漏。

现有U形网络——从经典的**3D U-Net** (Çiçek et al., MICCAI 2016)、**V-Net** (Milletari et al., 3DV 2016)，到基于Transformer的**UNETR** (Hatamizadeh et al., WACV 2022)、**SwinUNETR** (Hatamizadeh et al., MICCAI 2022)、**nnFormer** (Zhou et al., TIP 2023)，再到Mamba架构的**SegMamba** (Xing et al., MICCAI 2024)和ConvNeXt风格的**MedNeXt** (Roy et al., MICCAI 2023)——虽然在特征容量和感受野设计上持续演进，但均未显式控制降采样过程中的混叠注入，也未对跳连接的高分辨证据进行相位校准。这导致在各向异性强的数据集（如胰腺肿瘤、视网膜OCT层分割）上，边界模糊和拓扑不连贯的问题尤为突出。

本文的核心动机在于：将**采样理论**（多相分析、陪集分解、微局部传输）与**深度表征学习**（交叉源协同注意力、相位注意力、边缘门控）相结合，从信号处理层面根本性地解决上述两个瓶颈。CROWn框架通过两个互补模块——µPCAD（抗混叠降采样）和OCF（相位校准融合）——在编码器下采样和跳连接两个关键接口上同时抑制混叠并保留边界相关的高频证据，从而在各向异性和异质扫描条件下实现一致精细的分割。

## 核心创新

CROWn的核心创新在于将**采样理论与深度表征学习耦合**，针对三维医学分割中两个被长期忽视的结构性瓶颈——各向异性体素间距导致的**下采样混叠**和跨尺度特征的**相位失准**——提出了统一解决方案。与现有U形网络依赖步长卷积/池化进行隐式降采样、并通过直接拼接实现跳连接融合的范式不同，CROWn在两个关键操作槽位（changed slots）上引入了根本性的机制变革。

### 创新一：µPCAD——抗混叠的边界保留降采样

传统编码器的下采样操作（步长卷积或池化）未施加显式抗混叠低通滤波，导致高频边界信息以混叠伪影的形式注入低分辨率特征，造成边界模糊和拓扑断裂。**µPCAD（Microlocal Polyphase Co-Attentive Decimator）** 将这一隐式过程替换为三个协同步骤：

1. **轴感知多相分析**：沿指定轴对特征图执行可分离Haar小波分解，将信号拆解为LL、LH、HL、HH四个子带（公式1），显式提取方向性高频信息。
2. **池化-子带协同注意力**：以池化特征作为查询（Query）和键（Key），以小波子带拼接作为值（Value），通过多头交叉源注意力（公式3）将子带中的边界证据路由到降采样网格，实现高频信息的可控传递。
3. **显式抗混叠低通滤波**：在协同注意力聚合后施加显式低通滤波，抑制降采样引入的混叠分量。

子空间组合阶段通过可学习的逻辑门控（公式4）融合低频结构、注意力输出与LL子带对齐信号，并施加通道SE重标定，最终输出混叠抑制且边界保留的低分辨率特征。

**因果机制**：µPCAD将降采样从“无防护的信号抽取”转变为“先分析-再路由-后滤波”的三阶段过程，主动保留边界相关高频成分的同时衰减步长引入的混叠伪影，从而在源头控制混叠注入。

### 创新二：OCF——相位校准的跳连接融合

传统跳连接直接将高分辨率编码器特征拼接到解码器，忽略了降采样造成的**相位失准**——高分辨特征的格点位置与解码器特征格点之间存在亚像素偏移，导致融合时边界信息错位。**OCF（Octaphase Coset-fibRated Fusion）** 通过以下机制实现相位对齐的跳连接校准：

1. **抗混叠预滤波**：对高分辨率跳连接特征先施加抗混叠低通滤波，阻断混叠向解码器传播。
2. **八相位陪集分解**：对预滤波后的特征执行3D空间到深度（space-to-depth）转换，按体素坐标的奇偶性分解为$2^3=8$个陪集（公式6），每个陪集对应一个亚像素相位。
3. **相位注意力聚合**：学习每个空间位置对各陪集的softmax权重（公式7），自适应地加权求和，实现相位对齐的特征重建。
4. **Sobel边缘门控**：利用三轴Sobel算子计算通道平均场的边缘响应（公式8），生成边缘门控信号，增强边界区域的融合精度。
5. **深度可分离整合**：通过逐通道-逐点卷积将相位对齐特征压缩为紧凑的跳连接输出（公式9）。

整个OCF可表达为纤维丛上的单一传输算子（公式10），包含抗混叠、陪集提升、相位注意聚合、边缘门控和卷积整合五个连续操作。

**因果机制**：OCF将跳连接从“无校准的特征搬运”转变为“相位感知的纤维丛传输”，通过陪集分解显式建模亚像素偏移，利用相位注意力实现自适应对齐，边缘门控进一步强化边界区域的校准精度，从而消除融合阶段的相位失准。

### 创新机制的系统性协同

µPCAD和OCF并非孤立模块，而是采样理论在U形网络两个关键接口的系统性应用：µPCAD在**编码器下采样阶段**控制混叠注入，OCF在**跳连接融合阶段**纠正相位失准。两者共同构成“源头抑制-路径校准”的双重保障，使得解码器接收到的多尺度特征既无混叠污染，又在空间相位上精确对齐，从而稳定边界定位并改善拓扑连续性。

**证据强度**：消融实验表明，µPCAD在所有编码器阶段均部署时带来最稳定的性能提升（Supplementary Table S2），且将其插入CNN、Transformer、ConvNeXt和Mamba等不同骨干网络后一致提升重叠和边界指标（Supplementary Table S3），验证了逐级抗混叠的必要性和跨架构通用性。OCF的八相位分解、相位注意力和边缘门控对跳连接校准具有可加性贡献（Table 4, Table 5），且带来更优的重叠-边界权衡。

## 整体框架

CROWn（Coset-fibRated micrO-local co-attention Network）是一个面向三维医学分割的统一框架，其核心设计动机源自一个被长期忽视的瓶颈：各向异性体素间距导致的下采样混叠与跨尺度特征相位失准，造成边界模糊和拓扑断裂。现有U形网络在下采样时普遍采用步长卷积或池化，未显式控制混叠注入；在跳连接中直接拼接高分辨率特征，缺乏相位对齐机制。CROWn通过将采样理论（多相分析、陪集分解）与深度表征学习（交叉源协同注意力、相位注意力、边沿门控）相结合，系统性地解决了这两个问题。

框架由四个主要模块构成，沿编码器-解码器主干展开：

1. **Encoder (backbone)**：提取多尺度特征，可替换为CNN、Transformer、ConvNeXt或Mamba等任意骨干网络。
2. **µPCAD（Microlocal Polyphase Co-Attentive Decimator）**：部署于编码器的每个下采样阶段，执行轴感知多相分析与池化-子带协同注意力，随后施加显式抗混叠低通滤波，在抑制混叠的同时保留边界相关的高频证据。
3. **OCF（Octaphase Coset-fibRated Fusion）**：位于跳连接路径上，对高分辨率特征先进行抗混叠预滤波，再通过三维空间到深度（space-to-depth）操作分解为八个相位陪集，利用相位注意力与Sobel边缘门控进行加权聚合，最终经深度可分离卷积输出紧凑、相位对齐的边界感知特征。
4. **Decoder**：融合经OCF校准的多尺度跳连接特征与解码器上采样特征，生成最终分割图。

整个pipeline的输入输出流清晰：输入三维医学影像（CT/MRI/OCT等）经编码器逐级下采样，每一级由µPCAD完成抗混叠降采样；对应尺度的跳连接特征经OCF进行相位校准后注入解码器；解码器逐级上采样并与校准特征融合，最终输出分割结果。该设计使得CROWn在保持可控计算量（23.78M参数，199.58G FLOPs）的前提下，实现了对各向异性和异质扫描条件下的一致精细分割。

### 补充图表

![[assets/figures/papers/paper_list_l2457_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_CROWn_A_Unified/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed CROWn, included µPCAD and OCF. µPCAD performs axis-aware polyphase analysis and pooled–subband co-attention, then applies an explicit anti-alias low-pass to yield alias-suppressed, boundary-preserving features at lower scales. OCF anti-aliases the high-resolution skip, restructures it via 3D space-to-depth into eight cosets, applies phase attention with Sobeldriven edge gating, and aggregates with depthwise–pointwise convs to produce compact, phase-aligned, boundary-aware skips*

## 核心模块与公式推导

CROWn 的核心由两个模块构成：**µPCAD**（微局部多相协同注意力降采样器）和 **OCF**（八相位陪集纤维化跳连接校准模块），分别解决编码器下采样中的混叠注入与跳连接跨尺度相位失准问题。

### µPCAD：抗混叠边界保留降采样

µPCAD 将下采样操作重新设计为一个轴感知的多相分析—协同注意力—显式抗混叠滤波的级联过程。其关键步骤如下：

**多相分解**：对于输入特征图沿指定轴（如 W 轴对应切片方向）的每个 2D 切片 $\widetilde{\mathbf{Z}}_{b,c,:,:}^{[w]}$，使用可分离 Haar 小波滤波器进行多相分解：

$$
\mathbf{V}_{b,c,i,j}^{\sigma,[w]} = \sum_{u=0}^{1} \sum_{v=0}^{1} \kappa_{u,v}^{\sigma} \widetilde{\mathbf{Z}}_{b,c,2i+u,2j+v}^{[w]}
$$

其中 $\sigma \in \{LL, LH, HL, HH\}$ 表示四个子带，$\kappa_{u,v}^{\sigma}$ 为 Haar 滤波器系数。该分解将特征分离为低频结构（LL）与三个方向性高频子带（LH、HL、HH），为后续边界相关高频成分的保留提供显式证据。

**交叉源协同注意力**：以池化后的特征作为查询（Query）和键（Key），将四个小波子带拼接作为值（Value），通过多头注意力机制将子带中的高频证据传递到池化网格：

$$
\mathbf{A}_{b,:,i,j}^{[w]} = \sum_{\mathfrak{h}=1}^{H_a} \sum_{(i',j')\in\Pi_r} \frac{\exp(\langle \mathbf{q}_{b,i,j}^{[w],\mathfrak{h}}, \mathbf{k}_{b,i',j'}^{[w],\mathfrak{h}} \rangle / \sqrt{\delta_{\mathfrak{h}}})}{\sum_{(u,v)\in\Pi_r} \exp(\langle \mathbf{q}_{b,i,j}^{[w],\mathfrak{h}}, \mathbf{k}_{b,u,v}^{[w],\mathfrak{h}} \rangle / \sqrt{\delta_{\mathfrak{h}}})} \mathbf{v}_{b,i',j'}^{[w],\mathfrak{h}}
$$

其中 $\mathbf{q}$、$\mathbf{k}$ 分别由池化查询 $\mathbf{Q}^{[w]}$ 和池化键 $\mathbf{K}^{[w]}$ 经线性投影得到，$\mathbf{v}$ 由拼接的子带 $[\mathbf{V}^{LL},\mathbf{V}^{LH},\mathbf{V}^{HL},\mathbf{V}^{HH}]$ 投影得到，$\delta_{\mathfrak{h}}$ 为第 $\mathfrak{h}$ 个注意力头的缩放因子。

**子空间组合与门控**：将低频结构 $\mathbf{L}^{[w]}$、协同注意力输出 $\mathbf{A}^{[w]}$ 以及对齐的 LL 子带 $\mathbf{V}^{L\dot{L},[w]}$ 通过可学习的逻辑门控进行融合：

$$
\mathbf{F}^{[w]} = \dot{\sigma}(\alpha) \mathbf{L}^{[w]} + \sigma(\beta) \mathbf{A}^{[w]} + \gamma \dot{\mathcal{J}}(\mathbf{V}^{L\dot{L},[w]})
$$

其中 $\dot{\sigma}(\cdot)$ 和 $\sigma(\cdot)$ 为带温度参数的逻辑函数，$\alpha$、$\beta$、$\gamma$ 为可学习参数，$\dot{\mathcal{J}}$ 为通道 SE 重标定操作。融合后的特征再经过显式抗混叠低通滤波，最终产生混叠抑制且边界保留的低分辨率特征。

**微局部传输方程统一形式**：上述过程可被统一表达为格点索引形式的微局部传输方程（Equation 4），将协同注意力、多相分析、门控以及 W 轴模糊投影-降采样整合为单一算子，从理论上保证了操作的局部性与因果性。

### OCF：八相位陪集纤维化跳连接校准

OCF 对跳连接路径上的高分辨率特征进行抗混叠预滤波后，通过陪集分解、相位注意力和边缘门控实现与解码器特征的相位对齐融合。

**八相位陪集分解**：对经抗混叠预滤波的跳连接特征 $\mathbf{B}$，采用 3D 空间到深度（space-to-depth）操作将其分解为八个相位陪集：

$$
\mathbf{P}_{b,c,i,j,k}^{pqr} = \mathbf{B}_{b,c,2i+p,2j+q,2k+r}, \quad (p,q,r) \in \{0,1\}^3
$$

每个陪集对应下采样格点的一个相位偏移，显式保留了因步长卷积丢失的亚格点相位信息。

**相位注意力聚合**：使用 softmax 归一化的相位注意力权重对各陪集加权求和，得到相位对齐的特征张量：

$$
\mathbf{Z}_{b,c,i,j,k} = \sum_{(p,q,r)\in\{0,1\}^3} \omega_{pqr}(b,i,j,k) \mathbf{P}_{b,c,i,j,k}^{pqr}
$$

其中 $\omega_{pqr}$ 为空间位置 $(i,j,k)$ 处第 $(p,q,r)$ 相位的注意力权重，由小型卷积子网络预测并经 softmax 归一化。

**Sobel 边缘门控**：基于三轴 Sobel 算子在通道平均场上的边缘响应生成门控信号：

$$
\mathbf{E} = \sqrt{ (\boldsymbol{K}_x \ast \mathbf{A})^2 + (\boldsymbol{K}_y \ast \mathbf{A})^2 + (\boldsymbol{K}_z \ast \mathbf{A})^2 + \varepsilon }
$$

其中 $\mathbf{A}$ 为跳连接特征的通道均值，$\boldsymbol{K}_x$、$\boldsymbol{K}_y$、$\boldsymbol{K}_z$ 为三轴 Sobel 核。边缘强度 $\mathbf{E}$ 用于调制相位聚合特征，在边界区域增强高分辨率证据的贡献。

**深度可分离整合**：最终的 OCF 输出通过逐通道卷积、边缘门控和逐点卷积的级联生成（Equation 9），将相位对齐、边缘感知与通道混合统一为紧凑的跳连接特征 $\mathbf{G}$。

**纤维丛传输闭合形式**：OCF 可被表达为纤维丛上的单一传输算子（Equation 10）：

$$
\mathbf{G} = \mathbf{N}_{\zeta} \Big( \mathbf{M} \Big( \big( \kappa \star ( \Gamma \cdot \bigoplus_a \mathrm{lift}_\pi [ \mathcal{G} * \mathbf{U} ] ) \big) \Big) \Big)
$$

该形式将抗混叠滤波 $\mathcal{G} *$、陪集提升 $\mathrm{lift}_\pi$、相位注意力聚合 $\bigoplus_a$、边缘门控 $\Gamma \cdot$ 以及卷积整合 $\kappa \star$、$\mathbf{M}$、$\mathbf{N}_{\zeta}$ 统一为从跳连接源到解码器的纤维丛传输算子，从数学上保证了操作的相位等变性与边界保持特性。

## 实验与分析

### 主实验结果

在15个公开医学影像分割基准上，CROWn在所有数据集上均取得最优的IoU和Dice，并普遍降低HD95边界误差（Table 1）。这一结果覆盖了CT、MRI和OCT三种模态，包含高各向异性体素间距的胰腺肿瘤（MSD Pancreas Tumour，IoU 79.16 / Dice 87.26 / HD95 3.12）、肺部肿瘤（MSD Lung Tumour，IoU 82.65 / Dice 89.76 / HD95 4.30）以及脑肿瘤（MSD BRATS Tumour，IoU 84.05 / Dice 91.05 / HD95 2.86）等任务。对比的17个先进方法包括**3D U-Net**（Cicek et al., MICCAI 2016）、**nnFormer**（Zhou et al., TIP 2023）、**MedNeXt**（Roy et al., MICCAI 2023）、**SegMamba**（Xing et al., MICCAI 2024）、**nnWNet**（Zhou et al., CVPR 2025）等，CROWn在重叠度指标上的一致优势表明，联合抗混叠降采样与相位校准跳连接的设计在跨模态、跨解剖结构的场景中具有鲁棒性。

![[assets/figures/papers/paper_list_l2457_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_CROWn_A_Unified/figures/002_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art 3D medical image segmentation methods on 15 public benchmarks. CROWn attains the best IoU and Dice on all datasets, with clear gains on anisotropic cohorts and fine-structure data, demonstrating strong cross-modality robustness*

定性结果（Figure 2）进一步印证了这一趋势：CROWn在胰腺肿瘤边界上产生更清晰、无泄漏的分割轮廓，在OIMHS数据集中保留了连续的层间界面并显著减少阶梯状伪影，在FLARE2022上则展现出更强的细小结构保持能力。

![[assets/figures/papers/paper_list_l2457_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_CROWn_A_Unified/figures/003_Figure_2.jpg]]
*Figure 2: Qualitative comparison on the MSD Pancreas Tumour, OIMHS, and FLARE2022*

所有对比方法采用统一的训练协议——相同的3D数据增强（随机旋转、平移、缩放）、96×96×96随机裁剪、DiceCE损失和AdamW优化器，训练至320k步——确保性能差异反映架构特性而非训练协议偏差。

### 消融实验

#### µPCAD的消融分析

**与经典模块的对比**（Table 2）：将µPCAD与SE、CBAM、大核卷积等经典注意力或容量扩展模块进行对比，µPCAD在边界相关指标上的优势最为显著。这表明，通过显式抗混叠低通滤波和多相协同注意力保留边界相关高频成分，比单纯增加模型容量或通道注意力更有价值。

**轴感知分析**（Table 3）：µPCAD支持沿不同轴（W、H、D或组合）执行多相分析。在OIMHS数据集上，W轴配置（slice-wise）取得最佳性能，验证了针对各向异性体素间距进行轴感知设计的有效性——医学影像中slice方向通常是分辨率最低、混叠风险最高的维度。

**部署阶段消融**（Supplementary Table S2）：将µPCAD插入编码器的不同下采样阶段，当在所有阶段均部署时产生最稳定的性能提升。这验证了逐级抗混叠的必要性：混叠一旦在某一级注入，后续层的非线性变换会将其扩散并放大，因此需要在每个降采样接口进行控制。

**骨干网络通用性**（Supplementary Table S3）：将µPCAD插入CNN、Transformer、ConvNeXt和Mamba等不同骨干网络，一致提升重叠和边界指标，证明该模块独立于特定编码器架构，可作为通用的抗混叠降采样插件。

#### OCF的消融分析

**与经典跳连接模块的对比**（Table 4）：OCF相较于直接拼接、SE门控、大核卷积融合等经典跳连接处理方式，在边界连贯性和拓扑完整性上均有显著提升，验证了相位对齐校准的必要性。

**内部组件贡献**（Table 5）：在FLARE2022上对OCF进行组件级消融，八相位陪集分解、相位注意力和Sobel边缘门控各自带来可加性的性能增益（Dice从基线逐步提升至82.65±7.20），且三者组合实现了最优的重叠-边界权衡。这表明：
- 陪集分解保留了完整的空间相位信息，避免了传统降采样跳连接的信息丢弃；
- 相位注意力通过学习各陪集的softmax权重，实现了数据驱动的相位对齐；
- Sobel边缘门控利用三轴边缘强度（Equation 8）增强边界区域的响应，进一步抑制边界模糊。

#### 计算效率

CROWn总体参数量23.78M，FLOPs 199.58G（96×96×96输入），在保持可控计算成本的同时达到SOTA性能（Table 6）。与参数量更大或计算量更高的方法相比，CROWn的性价比优势明显，这得益于µPCAD和OCF的紧凑设计——多相分析和陪集分解均利用高效的张量重塑操作，避免了额外的可学习参数膨胀。

![[assets/figures/papers/paper_list_l2457_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_CROWn_A_Unified/figures/009_Table_6.jpg]]
*Table 6: Model size and compute. Parameter and FLOPs of representative 3D medical segmentation models for a 96×96×96 input*

### 失败模式与局限性

尽管CROWn在15个基准上表现优异，仍存在以下局限：

1. **极细小结构的连续性**：对于直径接近体素分辨率的管状结构（如微小血管），边界监督和拓扑引导的跳连接选择尚未整合，可能导致细分目标的断裂。定性结果中偶见此类不连续，但定量影响有限。

2. **严重域漂移下的鲁棒性**：当前工作未引入自监督预训练或测试时自适应（TTA），在扫描仪参数、重建算法显著不同的域漂移场景下，抗混叠低通滤波器的固定截止频率可能不再最优。需要进一步验证。

3. **单模态输入**：框架目前针对单模态设计，尚未引入自适应多模态权重融合，在多序列MRI或多模态（PET/CT）场景中需要扩展。

4. **移动端部署**：虽然参数量和FLOPs在通用分割基准上控制得当，但µPCAD的多头协同注意力和OCF的相位注意力仍包含矩阵乘法密集的操作，进一步压缩和量化尚未探索。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| **Table 1** | CROWn在15个基准上IoU/Dice全最优，HD95普遍降低，跨模态鲁棒 |
| **Table 2** | µPCAD在边界指标上显著优于SE/CBAM等经典模块，抗混叠降采样比容量扩展更关键 |
| **Table 3** | W轴µPCAD在各向异性数据上最优，轴感知设计有效 |
| **Table 4** | OCF显著优于直接拼接等经典跳连接，相位校准对边界连贯性至关重要 |
| **Table 5** | OCF三组件（陪集分解+相位注意力+边缘门控）贡献可加，联合实现最优重叠-边界权衡 |
| **Table 6** | 23.78M参数/199.58G FLOPs，在可控成本下达到SOTA |
| **Figure 2** | 定性展示CROWn边界更清晰、泄漏更少、层间界面更连续 |
| **Figure 3** | µPCAD定性消融：边界保持能力明显优于经典模块 |
| **Figure 4** | OCF定性消融：跳连接校准有效减少阶梯伪影和相位错位 |

![[assets/figures/papers/paper_list_l2457_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_CROWn_A_Unified/figures/004_Table_2.jpg]]
*Table 2: Comparison of µPCAD with classic modules*

![[assets/figures/papers/paper_list_l2457_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_CROWn_A_Unified/figures/005_Table_4.jpg]]
*Table 4: Comparison of OCF with classic modules*

![[assets/figures/papers/paper_list_l2457_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_CROWn_A_Unified/figures/006_Table_3.jpg]]
*Table 3: Axis-wise analysis about µPCAD*

![[assets/figures/papers/paper_list_l2457_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_CROWn_A_Unified/figures/010_Table_5.jpg]]
*Table 5: Phase anti-aliasing about OCF*

![[assets/figures/papers/paper_list_l2457_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_CROWn_A_Unified/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative comparison of µPCAD on the OIMHS dataset*

![[assets/figures/papers/paper_list_l2457_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_CROWn_A_Unified/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative comparison of OCF on the OIMHS dataset*

## 方法谱系与知识库定位

### 核心创新定位

CROWn 的根本贡献在于将**经典采样理论**（多相分析、陪集分解）与**深度表征学习**（交叉源协同注意力、相位注意力、边缘门控）进行系统耦合，形成两个可插拔的模块——µPCAD 和 OCF。这一定位区别于现有 U 形网络的两条主流改进路径：一是通过扩大感受野或增强注意力机制提升容量（如 SE、CBAM、大核卷积），二是通过 Transformer 或 Mamba 等架构替代 CNN 骨干。CROWn 指出，上述路径均未显式控制各向异性体素间距引发的**降采样混叠注入**和**跨尺度特征相位失准**，而这两个瓶颈正是边界模糊与拓扑断裂的直接诱因。

### 与基线方法的关系

#### 下采样操作：µPCAD vs. 经典模块

现有 3D 医学分割网络的下采样几乎全部采用步长卷积或池化，缺乏显式抗混叠设计。CROWn 的 µPCAD 通过**轴感知多相分析 + 池化-子带协同注意力 + 显式抗混叠低通滤波**三阶段流水线，将下采样重新定义为一个边界保留的混叠抑制过程。消融实验（Table 2）表明，将 µPCAD 替换为 SE、CBAM、大核卷积、非局部注意力等经典容量扩展模块后，边界指标显著下降，证明**抗混叠降采样比单纯容量扩展更有价值**。进一步的骨干网络兼容性实验（Supplementary Table S3）显示，将 µPCAD 插入 **3D U-Net**（Çiçek et al., MICCAI 2016）、**UNETR**（Hatamizadeh et al., WACV 2022）、**MedNeXt**（Roy et al., MICCAI 2023）和 **SegMamba**（Xing et al., MICCAI 2024）等 CNN、Transformer、ConvNeXt 和 Mamba 架构后，重叠度和边界指标一致提升，验证了其作为**骨干无关的下采样算子**的通用性。

#### 跳连接融合：OCF vs. 经典校准策略

传统跳连接直接将高分辨率特征拼接到解码器，忽略了跨尺度特征之间的相位偏移。OCF 通过**抗混叠预滤波 → 八相位空间到深度陪集分解 → 相位注意力 → Sobel 边缘门控 → 深度可分离聚合**的完整管线，将跳连接校准为一个相位对齐的纤维丛传输过程。消融实验（Table 4）将 OCF 与 Dense Skip、Attention Gate、SE Skip 等经典跳连接模块对比，OCF 在重叠度和边界误差上均取得最优。Table 5 进一步验证了八相位分解、相位注意力和边缘门控三者具有**可加性贡献**，共同实现了更优的重叠-边界权衡。

#### 综合性能：15 个基准上的 SOTA 定位

CROWn 在 15 个公开基准上与 17 个先进方法进行了系统对比（Table 1），涵盖 **nnFormer**（Zhou et al., TIP 2023）、**SegFormer3D**（Perera et al., CVPR 2024）、**SwinSMT**（Plotka et al., MICCAI 2024）、**VSmTrans**（Liu et al., Medical Image Analysis 2024）、**nnWNet**（Zhou et al., CVPR 2025）、**SuperLightNet**（Yu et al., CVPR 2025）、**DiffUNet**（Xing et al., Medical Image Analysis 2025）、**HiPaSNet**（Chu et al., Nature Communications 2025）等最新工作。CROWn 在所有数据集上均取得最优 IoU 和 Dice，在各向异性队列和细结构数据上的优势尤为显著，同时将 HD95 控制在较低水平。值得注意的是，CROWn 仅使用 23.78M 参数和 199.58G FLOPs（Table 6），在计算效率上具备竞争力。

### 适用边界与局限

1. **单模态输入假设**：当前 CROWn 设计面向单模态 3D 体积（CT、MRI、OCT），尚未引入自适应多模态权重融合机制。在多模态配准输入场景下，µPCAD 的轴感知分析和 OCF 的相位校准如何扩展到跨模态特征对齐，需要进一步验证。

2. **域漂移鲁棒性未充分验证**：尽管在 15 个基准上表现稳健，但所有实验均在标准训练-测试协议下进行，未涉及自监督预训练或测试时自适应（TTA）。在扫描仪间点扩散函数差异显著的严重域漂移场景下，抗混叠滤波器的固定截止频率可能不再最优。

3. **极细小结构的拓扑连续性**：当前 OCF 的边缘门控基于 Sobel 算子，对管状或线状细分目标的边界检测能力有限。边界监督和拓扑引导的跳连接选择（如基于持久同源性的筛选）尚未整合，可能影响细小结构的连续性。

4. **移动端部署优化不足**：虽然 23.78M 参数和 199.58G FLOPs 在通用分割基准上可控，但 µPCAD 的多头协同注意力和 OCF 的八相位分解引入了额外的计算分支，进一步轻量化仍需探索。

### 开放问题

- **跨模态泛化**：µPCAD 的抗混叠低通滤波器在超声、PET 等噪声特性迥异的成像模态中是否同样有效？其截止频率是否需要根据模态的点扩散函数自适应调整？

- **理论最优性**：OCF 的相位注意力机制是否具有接近小波框架的理论最优性？能否建立陪集分解与调和分析中多相表示的严格对应关系？

- **任意下采样比例**：当前陪集分解基于 2×2×2 的八相位空间到深度转换，能否泛化到任意下采样比例（如各向异性的 1×2×2）而不损失相位对齐性质？

- **测试时自适应**：能否通过 TTA 在线估计扫描仪的点扩散函数，并据此动态校准 µPCAD 的低通滤波器和 OCF 的相位注意力权重？

- **拓扑引导的跳连接选择**：引入持久同源性等拓扑工具对跳连接进行筛选，是否会进一步提升管状结构（如血管、胆管）的分割连续性？

## 原文 PDF

![[paperPDFs/CVPR_2026/CROWn_A_Unified_Framework_for_Anti_Aliased_Downsampling_and_Phase_Calibrated_Fusion_in_3D_Medical_Segmentation.pdf]]