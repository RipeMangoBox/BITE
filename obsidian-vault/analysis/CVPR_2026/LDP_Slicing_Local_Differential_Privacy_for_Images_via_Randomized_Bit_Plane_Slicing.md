---
title: "LDP-Slicing: Local Differential Privacy for Images via Randomized Bit-Plane Slicing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LDP_Slicing_Local_Differential_Privacy_for_Images_via_Randomized_Bit_Plane_Slicing.pdf
project_link: null
code_link: null
aliases:
- LS
- LDP-Slicing
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将像素值分解为8位二进制位平面，通过独立对每个比特施加二进制随机响应，并利用基于位重要性和色道敏感度的优化策略分配隐私预算，以此控制噪声注入量和位置，从而在保持严格ε-LDP的同时保留任务相关结构信息。
primary_logic: 像素的256个离散状态本质上是8位二进制编码，不同比特位对图像语义的贡献呈指数级差异（MSB承载主要结构，LSB近似噪声），因此可将LDP直接应用于比特级别，并根据比特重要性非均匀分配隐私预算。
claims:
- 提出位平面分解解决数据表征不匹配，使得LDP能够高效应用于图像。
- 在四个面部识别基准上，LDP-Slicing性能显著超过所有具备正式DP/LDP保证的方法。
- 身份区分攻击优势远低于对比方法DCTDP。
- 消融实验证明，去除LL剪枝或使用均匀预算分配会导致性能大幅下降。
---

# LDP-Slicing: Local Differential Privacy for Images via Randomized Bit-Plane Slicing

> [!tip] 核心洞察
> 像素的256个离散状态本质上是8位二进制编码，不同比特位对图像语义的贡献呈指数级差异（MSB承载主要结构，LSB近似噪声），因此可将LDP直接应用于比特级别，并根据比特重要性非均匀分配隐私预算。

| 字段 | 内容 |
|------|------|
| 中文题名 | LDP-Slicing：基于随机位平面切片的图像本地差分隐私 |
| 英文题名 | LDP-Slicing: Local Differential Privacy for Images via Randomized Bit-Plane Slicing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.03711) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | LDP-Slicing |
| Dataset | AgeDB-30, LFW, CPLFW, CALFW |

> [!tip] 效果简介
> - AgeDB-30 (face recognition) 上，Accuracy (%) 96.68 (LDP-Slicing) vs 94.37 (DCTDP) (+2.31)。
> - LFW (face recognition) 上，Accuracy (%) 99.75 (LDP-Slicing) vs 99.48 (DCTDP) (+0.27)。
> - CPLFW (face recognition) 上，Accuracy (%) 91.08 (LDP-Slicing) vs 90.60 (DCTDP) (+0.48)。

## 概要

在图像高维像素空间直接应用本地差分隐私（LDP）面临一个根本性瓶颈：每个像素具有256种可能值，k元随机响应机制会注入大量噪声，导致信息几乎完全丢失。这一现象并非LDP固有的“维度诅咒”，而是数据表征与LDP机制之间的领域失配——像素值的离散状态本质上是8位二进制编码，不同比特位对图像语义的贡献呈指数级差异，最高有效位（MSB）承载主要结构信息，而最低有效位（LSB）近似噪声。

针对上述问题，本文提出**LDP-Slicing**，一个轻量级、无需训练的框架。其核心洞察在于：将像素值分解为8个二进制位平面，独立对每个比特施加二进制随机响应，并根据位重要性与色道敏感度进行非均匀隐私预算分配，从而在保持严格ε-LDP保证的同时，最大化保留任务相关的结构信息。此外，框架通过1阶Haar小波变换的LL子带剪枝实现感知混淆，防御人类肉眼检查。

实验表明，在四个面部识别基准（AgeDB-30、LFW、CPLFW、CALFW）上，LDP-Slicing的性能显著超过所有具备正式DP/LDP保证的方法，并在图像分类任务（CIFAR-10/100）上展现出优于中心化DP-SGD的隐私-效用折衷。身份区分攻击优势远低于对比方法DCTDP，消融实验进一步验证了非均匀预算分配与DWT剪枝的关键作用。

### 图像隐私保护的需求与困境

随着人脸识别、医疗影像分析等视觉应用在云服务和边缘设备上的广泛部署，用户原始图像在上传至不可信服务器时面临的隐私泄露风险日益严峻。传统的中心化差分隐私（Centralized DP）方案——如 **DP-SGD**（Abadi et al., CCS 2016）——假设存在一个可信的数据收集者，在训练阶段注入噪声。然而，这一假设在现实场景中往往不成立：用户需要在数据离开本地设备之前就获得隐私保护，而非依赖服务端的可信承诺。

本地差分隐私（Local Differential Privacy, LDP）将隐私保护的责任从服务端前移到数据源头，允许每个用户在本地对其数据进行随机化处理后再上传，从而在数学上保证即使服务器完全不可信，也无法从单个样本中推断出敏感信息。这一范式在表格数据和简单统计查询中已取得显著成功，但在图像领域却长期面临一个根本性瓶颈。

### 核心瓶颈：数据表征与LDP机制的域不匹配

将LDP直接应用于图像高维像素空间时，遭遇的并非差分隐私固有的“维度诅咒”，而是一个更深层的**表征不匹配**问题。具体而言，标准8位灰度图像的每个像素有 $2^8 = 256$ 种可能取值。若直接对每个像素施加 $k$-元随机响应（$k=256$），为保证 $\varepsilon$-LDP，扰动机制需要在256个离散状态间分配概率质量。在有限的隐私预算下，真实像素值被保留的概率极低，大量噪声被注入，导致图像结构信息几乎完全丢失。

这一困境的本质在于：**LDP机制被设计用于处理类别数有限且各状态语义独立的数据（如选择题的选项），而像素值的256个状态并非语义独立——它们构成了一个有序的、位编码的数值空间，其中不同比特位对视觉语义的贡献呈指数级差异。** 最高有效位（MSB）承载了图像的主要结构信息（边缘、轮廓、大块区域），而最低有效位（LSB）则主要由近似噪声的纹理细节构成。将这一有序结构“扁平化”为256个独立类别，是对数据内在结构的严重误用，导致隐私预算被低效地浪费在保护无意义的噪声位上。

### 现有方法的缺口

近年来，针对人脸识别等任务的隐私保护方法大量涌现，但可大致归为两类，均存在明显局限：

**启发式方法**（如 **InstaHide**、**Cloak**、**PPFR-FD**、**DuetFace**、**PartialFace**、**ProFace**、**AdvFace**、**MinusFace** 等）通过对抗扰动、特征混淆或部分信息屏蔽来阻止视觉检查或黑盒攻击。然而，这些方法缺乏形式化的隐私保证——它们无法量化攻击者在获得辅助信息后的推断优势上界，其安全性依赖于攻击者能力的经验假设，而非数学可证明的界。

**具备形式化DP/LDP保证的方法**则走向另一个极端。**PEEP**（Chamikara et al., Computers & Security 2020）将LDP应用于低维特征空间，但牺牲了像素级的源端保护——特征提取本身就在无保护状态下进行。**DCTDP**（Ji et al., ECCV 2022）在DCT块级别施加差分隐私，但其隐私定义层次与像素级LDP存在根本差异：经顺序组合分析，DCTDP转化到像素级的有效 $\varepsilon_{\text{pixel}}$ 高达94.5，而LDP-Slicing仅使用 $\varepsilon_{\text{total}}=20$，前者的隐私保证实际上宽松约4.7倍。

### 本文动机：从比特层面重建LDP与图像的桥梁

本文的核心洞察是：**像素的256个离散状态本质上是8位二进制编码，而二进制随机响应是LDP中最高效、最成熟的机制之一。** 如果将像素分解为8个独立的位平面，对每个比特单独施加二进制随机响应，则每个比特仅需在 $\{0,1\}$ 两个状态间分配隐私预算，噪声注入效率得到数量级提升。更重要的是，这一分解揭示了不同比特位对下游任务效用的非均匀贡献——MSB需要更多预算保护结构信息，LSB可用极少预算甚至零预算处理——从而为**效用感知的非均匀隐私预算分配**提供了自然的切入点。

基于这一洞察，本文提出 **LDP-Slicing**，一个轻量级、无需训练的框架，通过三个协同模块——感知混淆（防御人类肉眼检查）、位平面切片与随机响应（施加严格 $\varepsilon$-LDP）、效用感知预算优化（保留机器识别所需的结构信息）——在像素级实现形式化可证明的本地差分隐私，同时将下游任务精度损失控制在实用范围内。

## 核心方法与创新机理

LDP-Slicing 的核心创新在于**通过数据表征转换解决图像高维像素空间与 LDP 机制之间的根本性不匹配**，而非引入新的隐私定义或训练范式。其关键洞察是：8 位像素值的 256 个离散状态本质上是 8 位二进制编码，不同比特位对图像语义的贡献呈指数级差异——MSB 承载主要结构，LSB 近似噪声。基于此，LDP-Slicing 将 LDP 直接应用于比特级别，并根据比特重要性非均匀分配隐私预算，从而在保持严格 ε-LDP 的同时保留任务相关结构信息。

### 关键 changed slots

#### 1. 数据表征：从 k 元像素空间到二进制位平面

**Baseline 做法**：直接使用 8 位像素值（k=256）进行 k 元随机响应。在高维像素空间直接应用 LDP 时，每个像素有 256 种可能值，k 元随机响应会注入大量噪声导致信息丢失。

**LDP-Slicing 做法**：将像素分解为 8 个二进制位平面，对每个位独立应用二进制随机响应。具体而言，将 d 位像素值 x 分解为第 ℓ 个比特位：

$$x_{\ell} = \left\lfloor \frac{x}{2^{d-\ell}} \right\rfloor \bmod 2, \quad \ell \in \{1, \dots, d\}$$

随后对每个比特施加 ε_ℓ-LDP 的二进制随机响应：

$$\operatorname*{Pr}[\mathcal{M}_{RR}(x_{\ell}) = \tilde{x}_{\ell}] = \begin{cases} \frac{e^{\varepsilon_{\ell}}}{e^{\varepsilon_{\ell}}+1}, & \text{if } \tilde{x}_{\ell}=x_{\ell}, \\ \frac{1}{e^{\varepsilon_{\ell}}+1}, & \text{otherwise.} \end{cases}$$

**因果机制**：这一转换将 LDP 的操作域从 256 元空间降至 2 元空间，使随机响应机制仅需决定是否翻转单个比特，噪声注入量大幅降低。本质上，它解决了“数据表征与 LDP 机制不匹配”这一真实瓶颈，而非 LDP 固有的维度诅咒。

#### 2. 隐私预算分配：从均匀分配到基于位重要性与色道敏感度的优化分配

**Baseline 做法**：在所有位平面上均匀分配总预算 ε_total/24，忽略了不同比特位和色道对下游任务效用的巨大差异。

**LDP-Slicing 做法**：通过约束优化问题求解每个位平面的最佳预算分配：

$$\underset{\{\varepsilon_{c,b}\}}{\operatorname*{min}} \sum_{c,b} \frac{W_{c,b}}{\varepsilon_{c,b}} \quad \mathrm{s.t.} \sum_{c,b} \varepsilon_{c,b} = \varepsilon_{\mathrm{total}}, \; \varepsilon_{c,b} \geq 0$$

其闭式最优解为：

$$\varepsilon_{c,b} = \varepsilon_{\mathrm{total}} \cdot \frac{\sqrt{W_{c,b}}}{\sum_{i\in\{\mathrm{Y},\mathrm{Cb},\mathrm{Cr}\}} \sum_{j=1}^{8} \sqrt{W_{i,j}}}$$

其中权重 W_{c,b} 基于位重要性和色道敏感度设定——亮度通道（Y）权重远高于色度通道（Cb, Cr），MSB 权重远高于 LSB。

**因果机制**：该分配策略将更多隐私预算集中在承载主要结构信息的 MSB 和 Y 通道，而在近似噪声的 LSB 上使用极少预算，实现了在固定总预算下最小化加权失真。消融实验（Table 3）证实，采用均匀预算分配会导致 AgeDB-30 准确率从 96.68% 骤降至 89.82%，证明非均匀分配至关重要。

#### 3. 预处理：引入基于小波的感知混淆

**Baseline 做法**：无预处理或简单像素化，人类观察者可直接从私有化图像中感知语义内容。

**LDP-Slicing 做法**：通过 1 阶 Haar 小波变换（DWT）将 LL 子带系数置零后 IDWT 重构，去除人类可感知的低频信息，防御肉眼检查。

**因果机制**：LL 子带承载图像的低频概貌信息，置零后图像对人眼呈现为不可辨认的噪声状纹理，但高频细节子带（LH, HL, HH）得以保留，为下游机器识别任务保留了关键的高频特征。消融实验（Table 3）表明，移除 LL 剪枝仅导致轻微性能下降，说明该模块主要服务于人类感知防御，对机器识别任务影响较小。值得注意的是，以 DCT 剪枝替代 DWT 剪枝会降低效用，说明 DWT 更好地保留了机器识别所需的高频细节。

### 创新点的协同效应

三个 changed slots 形成递进式协同：感知混淆首先阻断人类视觉通路，位平面切片将问题从高维像素空间降至二进制域，效用感知的预算优化则在比特级别精准分配隐私资源。最终，扰动后的比特位通过加权求和重构像素值：

$$\tilde{x} = \sum_{\ell=1}^{8} 2^{8-\ell} \cdot \tilde{x}_{\ell}$$

这一整套机制使得 LDP-Slicing 在保持严格 ε-LDP 保证的同时，在面部识别基准上显著超越所有具备正式 DP/LDP 保证的方法（Table 1），并在身份区分攻击中展现出远低于 DCTDP 的敌手优势（Table 2）。

LDP-Slicing 的整体 pipeline 由两个串行阶段构成，其设计逻辑直接回应了核心瓶颈：**在图像高维像素空间直接应用 LDP 时，数据表征与机制的不匹配导致信息大量丢失**。该框架通过“表征变换—逐位扰动—优化重构”三步，将 ε-LDP 的噪声注入从像素级别下沉到比特级别，从而在严格隐私约束下保留任务相关结构信息。

### 阶段一：感知混淆（Perceptual Obfuscation）

输入图像首先被转换到 YCbCr 色彩空间，随后对每个通道独立执行 **1 阶 Haar 离散小波变换（DWT）**，得到四个子带：低频近似子带（LL）和三个高频细节子带（LH、HL、HH）。框架将 LL 子带系数全部置零，然后通过逆 DWT（IDWT）重构图像。这一操作的因果作用是**移除人类视觉系统可感知的低频结构信息**，使重构图像对人眼呈现噪声化外观，从而防御基于肉眼检查的隐私泄露。消融实验表明，移除 LL 剪枝仅导致面部识别准确率轻微下降（Table 3），证实该模块主要服务于人类感知防御，对机器识别任务影响有限。

### 阶段二：位平面随机化（Bit-Plane Randomization）

混淆后的图像进入核心隐私保护阶段，该阶段包含三个紧密耦合的子模块：

**（1）位平面切片（Bit-Plane Slicing）**  
将每个 8 位像素值按位分解为 8 个二进制位平面。对于 YCbCr 三个通道，共计生成 24 个位平面。分解公式为：
$$x_{\ell} = \left\lfloor \frac{x}{2^{d-\ell}} \right\rfloor \bmod 2, \quad \ell \in \{1, \dots, d\}$$
其中 $d=8$，$\ell=1$ 对应最高有效位（MSB），$\ell=8$ 对应最低有效位（LSB）。这一分解的核心洞察在于：**不同比特位对图像语义的贡献呈指数级差异**——MSB 承载主要结构信息，LSB 近似噪声（Figure 2 直观展示了这一非均匀分布）。因此，将 LDP 直接应用于比特级别，而非原始的 256 值像素空间，从根本上解决了数据表征不匹配问题。

**（2）逐位随机响应（Randomized Response per Bit）**  
对每个位平面中的每个比特，独立应用 $\varepsilon_{\ell}$-LDP 的二进制随机响应机制：
$$\operatorname*{Pr}[\mathcal{M}_{RR}(x_{\ell}) = \tilde{x}_{\ell}] = \begin{cases} \frac{e^{\varepsilon_{\ell}}}{e^{\varepsilon_{\ell}}+1}, & \text{if } \tilde{x}_{\ell}=x_{\ell}, \\ \frac{1}{e^{\varepsilon_{\ell}}+1}, & \text{otherwise.} \end{cases}$$
该机制以概率 $e^{\varepsilon_{\ell}}/(e^{\varepsilon_{\ell}}+1)$ 保持原始比特值，以概率 $1/(e^{\varepsilon_{\ell}}+1)$ 翻转该比特。由于每个比特独立扰动，整个机制的隐私保证可通过 LDP 的串行组合定理严格推导。

**（3）效用感知的预算优化与重构（Utility-Aware Budget Optimization）**  
这是决定隐私-效用平衡的关键控制旋钮。框架通过求解约束优化问题，将总隐私预算 $\varepsilon_{\mathrm{total}}$ 非均匀分配给 24 个位平面：
$$\underset{\{\varepsilon_{c,b}\}}{\operatorname*{min}} \sum_{c,b} \frac{W_{c,b}}{\varepsilon_{c,b}} \quad \mathrm{s.t.} \sum_{c,b} \varepsilon_{c,b} = \varepsilon_{\mathrm{total}}, \; \varepsilon_{c,b} \geq 0$$
其中 $W_{c,b}$ 为色道 $c$ 中第 $b$ 位的权重，基于色道敏感度（Y 通道承载主要结构信息，Cb/Cr 权重较低，Figure 3 验证了这一点）和位重要性（MSB 权重大于 LSB）联合设定。该优化问题存在闭式解：
$$\varepsilon_{c,b} = \varepsilon_{\mathrm{total}} \cdot \frac{\sqrt{W_{c,b}}}{\sum_{i\in\{\mathrm{Y},\mathrm{Cb},\mathrm{Cr}\}} \sum_{j=1}^{8} \sqrt{W_{i,j}}}$$
这意味着**重要位平面获得更多隐私预算（噪声更小），次要位平面获得更少预算（噪声更大）**，从而在总量约束下最大化效用。消融实验证实，采用均匀预算分配会导致性能大幅下降（AgeDB-30 从 96.68 降至 89.82），证明非均匀分配至关重要。最后，扰动后的比特按位权重加权求和重构像素值：
$$\tilde{x} = \sum_{\ell=1}^{8} 2^{8-\ell} \cdot \tilde{x}_{\ell}$$

### 端到端数据流

整个框架的输入为任意 8 位 RGB 图像，输出为满足严格 ε-LDP 保证的私有化图像，且输出图像与输入图像尺寸完全一致，**无额外存储或传输开销**（Table 5）。数据流可概括为：**RGB → YCbCr → DWT → LL 剪枝 → IDWT → 位平面切片 → 逐位随机响应 → 加权重构 → 私有化图像**。该框架无需训练，轻量级部署于客户端，适用于面部识别、图像分类等下游任务。

![[assets/figures/papers/paper_list_l2106_https_arxiv_org_abs_2603_03711/figures/013_Table_5.jpg]]
*Table 5: Storage and transmission overhead analysis. Overhead is reported as a multiple of the size of a standard image (our method, ×1). Lower is better. LDP-Slicing introduces zero overhead*

![[assets/figures/papers/paper_list_l2106_https_arxiv_org_abs_2603_03711/figures/001_Figure_1.jpg]]
*Figure 1: The LDP-Slicing framework. Our method consists of two primary stages: (1) Perceptual obfuscation: the input image is transformed into the frequency domain via DWT, where the low-frequency (LL) band is pruned to remove human-perceptible information. (2) Bit-plane randomization: The obfuscated image is decomposed into binary bit-planes. A utility-aware randomized response mechanism is applied to each bit and enforces a strict ε-Local Differential Privacy guarantee before the final image is reconstructed*

LDP-Slicing 的核心设计围绕一个关键洞察展开：8 位像素值的 256 个离散状态本质上是二进制编码，不同比特位对图像语义的贡献呈指数级差异——最高有效位（MSB）承载主要结构信息，而最低有效位（LSB）近似噪声。基于这一洞察，该方法将图像隐私保护分解为三个串联模块。

### 模块一：感知混淆（Perceptual Obfuscation）

该模块的目标是防御人类肉眼检查，而非直接贡献于机器识别效用。对输入图像的每个通道执行 1 阶 Haar 离散小波变换（DWT），得到四个子带：低频近似子带（LL）和三个高频细节子带（LH, HL, HH）。随后将 LL 子带系数全部置零，再通过逆离散小波变换（IDWT）重构图像。LL 子带承载了人类视觉感知依赖的低频信息，置零后图像在视觉上变得不可辨识，但高频细节子带中仍保留了机器识别所需的结构信息（见 Figure 3）。

### 模块二：位平面切片与随机响应（Bit-Plane Slicing & Randomized Response）

这是实现严格 ε-LDP 保证的核心机制。将混淆后的图像从 RGB 转换到 YCbCr 色彩空间，三个通道共产生 24 个位平面（每通道 8 位）。对每个位平面独立施加二进制随机响应。

首先，将 d 位像素值 $x$ 分解为第 $\ell$ 个比特位 $x_{\ell}$：

$$x_{\ell} = \left\lfloor \frac{x}{2^{d-\ell}} \right\rfloor \bmod 2, \quad \ell \in \{1, \dots, d\}$$

其中 $\ell=1$ 对应 MSB，$\ell=8$ 对应 LSB。随后，对每个比特位 $x_{\ell}$ 施加 $\varepsilon_{\ell}$-LDP 的二进制随机响应机制 $\mathcal{M}_{RR}$：

$$\operatorname*{Pr}[\mathcal{M}_{RR}(x_{\ell}) = \tilde{x}_{\ell}] = \begin{cases} \frac{e^{\varepsilon_{\ell}}}{e^{\varepsilon_{\ell}}+1}, & \text{if } \tilde{x}_{\ell}=x_{\ell}, \\ \frac{1}{e^{\varepsilon_{\ell}}+1}, & \text{otherwise.} \end{cases}$$

该机制以较高概率保留原始比特值，以较低概率翻转。由于每个比特的扰动相互独立，整个像素的隐私保证可通过组合定理严格推导。

### 模块三：效用感知的预算优化与重构（Utility-Aware Budget Optimization & Reconstruction）

若在所有位平面上均匀分配总隐私预算 $\varepsilon_{\mathrm{total}}$，MSB 和 LSB 将受到同等程度的扰动，导致结构信息严重丢失。LDP-Slicing 通过求解约束优化问题，实现基于位重要性和色道敏感度的非均匀预算分配。

设 $W_{c,b}$ 为色道 $c$ 中第 $b$ 个比特位的效用权重（反映该位对下游任务的贡献），优化目标为最小化加权失真：

$$\underset{\{\varepsilon_{c,b}\}}{\operatorname*{min}} \sum_{c,b} \frac{W_{c,b}}{\varepsilon_{c,b}} \quad \mathrm{s.t.} \sum_{c,b} \varepsilon_{c,b} = \varepsilon_{\mathrm{total}}, \; \varepsilon_{c,b} \geq 0$$

该问题有闭式解：

$$\varepsilon_{c,b} = \varepsilon_{\mathrm{total}} \cdot \frac{\sqrt{W_{c,b}}}{\sum_{i\in\{\mathrm{Y},\mathrm{Cb},\mathrm{Cr}\}} \sum_{j=1}^{8} \sqrt{W_{i,j}}}$$

预算分配与权重平方根成正比——重要位获得更多隐私预算（噪声更少），次要位获得更少预算（噪声更多）。实际中，亮度通道 Y 的权重设为色度通道 Cb/Cr 的 4 倍（即 Y:Cb:Cr = 4:1:1），同一通道内比特权重按 $2^{b-1}$ 递减，反映从 MSB 到 LSB 的结构信息衰减。

最后，将扰动后的比特位按位权重重构像素值：

$$\tilde{x} = \sum_{\ell=1}^{8} 2^{8-\ell} \cdot \tilde{x}_{\ell}$$

### 隐私保证的理论上界

LDP-Slicing 提供端到端的 ε-LDP 保证。对于任意两个相邻输入，机制输出分布的总变差距离满足：

$$\mathrm{TV}(P,Q) \leq \frac{e^{\varepsilon}-1}{e^{\varepsilon}+1} = \tanh(\varepsilon/2)$$

在身份区分攻击场景中，敌手优势的上界为：

$$\mathsf{Adv}_{\mathcal{M}}^{\mathrm{link}} \leq \frac{1}{2} \tanh(\varepsilon/2)$$

该上界仅依赖于总隐私预算 $\varepsilon$，与数据维度无关，从理论上保证了 LDP-Slicing 在高维像素空间中的隐私保护强度。

![[assets/figures/papers/paper_list_l2106_https_arxiv_org_abs_2603_03711/figures/002_Figure_2.jpg]]
*Figure 2: Bit-plane slicing reveals the non-uniform distribution of structural information. An 8-bit image (left) is decomposed into its planes (right), from LSB (top-left) to MSB (bottomright). This visualization shows that coarse structural information is concentrated in the high-order MSB planes, while low-order LSB planes consist primarily of noise-like texture. This motivates our non-uniform, utility-aware budget optimization strategy*

## 实验与关键发现

### 核心性能：人脸识别基准

LDP-Slicing 在四个主流人脸识别基准上与现有方法进行了系统对比，结果汇总于 **Table 1**。在所有具备正式 DP/LDP 保证的方法中，LDP-Slicing 取得了全面最优：AgeDB-30 上达到 96.68%，比最强的正式隐私方法 **DCTDP**（Ji et al., ECCV 2022）高出 2.31 个百分点；LFW 上达到 99.75%（+0.27%）；CPLFW 上 91.08%（+0.48%）；CALFW 上 96.02%（+2.55%）。值得注意的是，LDP-Slicing 与 DCTDP 的隐私定义层次存在本质差异——DCTDP 提供块级 DP，转换到像素级后其 ε 高达 94.5，而 LDP-Slicing 仅使用 ε_total=20，这意味着 LDP-Slicing 的实际隐私保证严格约 4.7 倍，却仍取得更高的识别精度。与无隐私的非私有基线 **ArcFace**（Deng et al., TPAMI 2022）相比，LDP-Slicing 的精度损失控制在 2–4 个百分点以内，表明该方法在严格 LDP 约束下仍能保留面部识别的关键判别信息。

![[assets/figures/papers/paper_list_l2106_https_arxiv_org_abs_2603_03711/figures/005_Table_1.jpg]]
*Table 1: Benchmarks on face recognition accuracy (%). LDP-Slicing is compared with a non-private baseline, heuristic methods, and methods with formal privacy guarantees. Bold indicates the best result among DP/LDP methods*

### 图像分类任务上的隐私-效用折衷

在 CIFAR-10 和 CIFAR-100 图像分类任务上，LDP-Slicing 与中心化 DP 的代表性方法 **DP-SGD**（Abadi et al., CCS 2016）进行了对比（见 **Figure 7**）。在 CIFAR-10 上，当 ε ≤ 12 时 LDP-Slicing 的精度一致优于 DP-SGD；在 CIFAR-100 上，LDP-Slicing 在所有测试的 ε 取值下均保持领先。这一结果尤其值得关注，因为 LDP-Slicing 工作在本地差分隐私的更强威胁模型下（不依赖可信中心服务器），而 DP-SGD 需要可信策展方收集原始数据后集中加噪。随着隐私预算进入实用区间（ε 较小），LDP-Slicing 的优势进一步扩大，说明位平面分解策略有效缓解了高维像素空间直接应用 LDP 的信息损失问题。

### 身份区分攻击防御

**Table 2** 报告了身份区分攻击下的敌手优势（定义见公式 $\mathsf{Adv}_{\mathcal{M}}^{\mathrm{link}} \leq \frac{1}{2} \tanh(\varepsilon/2)$）。LDP-Slicing 在所有数据集上的攻击优势均显著低于 DCTDP：例如，CIFAR-10 上仅为 0.25%（DCTDP 为 2.09%），LFW 上为 4.5%（DCTDP 为 13.88%）。低攻击优势直接验证了 ε-LDP 理论保证在实践中的有效性——敌手即使完全掌握机制细节，也难以从私有化输出中可靠推断原始图像的身份信息。

### 隐私预算变化下的效用衰减

**Table 4** 展示了不同 ε_total 取值下人脸识别精度的平滑衰减曲线。随着 ε_total 从 58 降至 1，四个基准上的精度单调下降，但即使在 ε_total=1 的极端隐私设置下，LDP-Slicing 仍保持远高于随机水平的识别能力。PSNR 指标与隐私预算呈正相关，进一步验证了理论预期——更强的隐私保护（更小的 ε）对应更大的像素级失真，但机器识别精度对失真表现出更强的鲁棒性。

### 消融实验：关键组件贡献

**Table 3** 通过四项消融配置解构了 LDP-Slicing 各组件的贡献（固定 ε_total=20）：

- **移除 LL 剪枝（A 配置）**：仅导致轻微性能下降（例如 AgeDB-30 从 96.68% 降至约 95%），表明小波域低频剪枝主要服务于防御人类肉眼检查的感知混淆目标，对机器识别任务影响有限。
- **均匀预算分配（B 配置）**：将总预算均匀分配给所有 24 个位平面，导致性能大幅下降——AgeDB-30 从 96.68% 骤降至 89.82%。这一结果直接证明了基于位重要性和色道敏感度的非均匀预算分配策略是 LDP-Slicing 高性能的核心驱动力：高位 MSB 承载主要结构信息，需要更多隐私预算保护；低位 LSB 近似噪声，可接受更强的扰动。
- **以 DCT 剪枝替代 DWT 剪枝（C 配置）**：性能低于完整方案，说明 Haar 小波变换相比离散余弦变换能更好地保留机器识别所需的高频细节，同时有效混淆人类可感知的低频信息。

### 存储与传输开销

**Table 5** 显示 LDP-Slicing 不引入任何存储或传输开销（开销倍数为 ×1），与标准图像尺寸完全相同。相比之下，部分对比方法因需要传输辅助信息或加密元数据而产生额外开销。这一特性使 LDP-Slicing 在带宽受限的边缘设备部署场景中具有实际优势。

### 重建攻击弹性

**Figure 5** 和 **Figure 6** 分别展示了白盒和黑盒重建攻击下的视觉结果。在白盒设置中，敌手完全知晓 LDP-Slicing 流水线并训练了专门的两阶段反演模型；即使在 ε_total=5.2 的较弱隐私设置下，重建图像仍无法恢复可辨识的面部身份。黑盒对比中，LDP-Slicing 在 ε_total=20 时的重建质量显著低于 DCTDP 在 ε_mean=0.5 时的结果，进一步验证了位平面级别随机响应对基于生成先验的攻击具有更强的固有弹性。

### 跨数据集泛化与局限性

**Table 6** 的额外实验揭示了 LDP-Slicing 的零样本跨数据集泛化能力有限：在 VGGFace2 和 CelebA 等未见域上，中等隐私预算下的准确率仍较低，表明该方法对训练数据分布偏移的鲁棒性不足。此外，在极低隐私预算（ε < 1）下效用下降明显，且色度权重（Y:Cb:Cr = 4:1:1）为手工设定的静态值，虽然实验有效，但未必是全局最优。针对更复杂的虚拟对抗样本攻击，其防御能力仍需进一步验证。

![[assets/figures/papers/paper_list_l2106_https_arxiv_org_abs_2603_03711/figures/009_Table_3.jpg]]
*Table 3: Ablation study of key components of LDP-Slicing. Results show face recognition accuracy (%) on four benchmarks, with a fixed privacy budget of*

![[assets/figures/papers/paper_list_l2106_https_arxiv_org_abs_2603_03711/figures/014_Table_4.jpg]]
*Table 4: Privacy-utility trade-off on face recognition accuracy (%). As the privacy budget εtotal decreases, utility across all benchmarks declines smoothly, aligning with theoretical expectations. PSNR values also correlate with the applied privacy budget*

## 定位与知识库关联

### 问题定位：高维像素空间与LDP机制的失配

在图像数据上直接应用本地差分隐私（Local Differential Privacy, LDP）面临一个根本性瓶颈：每个像素具有256种可能的离散值（8位深度），若直接使用k元随机响应（k-ary Randomized Response），需要将大量概率质量分配给所有非真值状态，导致注入的噪声完全淹没图像中的结构化信息。LDP-Slicing指出，这一瓶颈的根源并非LDP固有的“维度诅咒”，而是**数据表征与扰动机制之间的领域失配**——将连续或高基数离散的像素空间强行适配到为低基数符号设计的LDP框架中。

这一诊断与现有工作的路径形成鲜明对比。此前具备正式DP/LDP保证的图像隐私方法主要采取两种策略：一是将扰动操作下推到特征空间，如**PEEP**（Chamikara et al., Computers & Security 2020）在特征向量上施加差分隐私，但这牺牲了像素级（源级）的隐私保证，无法防御对原始图像的推断攻击；二是在变换域进行块级扰动，如**DCTDP**（Ji et al., ECCV 2022）对DCT系数块施加差分隐私，但其隐私定义层次为块级，转化为等效像素级隐私预算后高达ε≈94.5，实际隐私保护强度远弱于LDP-Slicing所使用的ε_total=20（严格约4.7倍）。此外，大量启发式方法——包括**InstaHide**（Huang et al., 2021）、**Cloak**（Mireshghallah et al., The Web Conference 2021）、**PPFR-FD**（Wang et al., AAAI 2022）、**DuetFace**（Mi et al., ACM Multimedia 2022）、**PartialFace**（Mi et al., ICCV 2023）、**ProFace**（Yuan et al., ACM Multimedia 2022）、**AdvFace**（Wang et al., CVPR 2023）和**MinusFace**（Mi et al., CVPR 2024）——虽在特定任务上表现良好，但均不提供形式化的隐私保证，其安全性依赖于攻击者能力的经验性假设。

### 核心洞察：位平面分解与表征适配

LDP-Slicing的核心洞察在于认识到**像素的256个离散状态本质上是8位二进制编码**，且不同比特位对图像语义的贡献呈指数级差异：最高有效位（MSB）承载主要的结构信息（边缘、轮廓），而最低有效位（LSB）近似于噪声纹理。这一观察通过位平面切片可视化得到直观验证（Figure 2）。基于此，LDP-Slicing将数据表征从“8位像素值”切换为“8个独立的二进制位平面”，从而将LDP的施加对象从k=256的高基数空间降为k=2的二进制空间。在这一新表征下，每个比特仅需一个二进制随机响应（Binary Randomized Response），其保持原值的概率为$e^{\varepsilon_\ell}/(e^{\varepsilon_\ell}+1)$，翻转概率为$1/(e^{\varepsilon_\ell}+1)$，噪声注入量由每位分配的隐私预算$\varepsilon_\ell$精确控制。

这一表征切换是LDP-Slicing区别于所有现有工作的关键“因果旋钮”。它使得隐私预算可以从“是否扰动整个像素”的粗粒度决策，细化为“扰动哪些比特位、扰动到什么程度”的精细控制。

### 预算分配策略：从均匀到效用感知的优化

在二进制位平面表征之上，LDP-Slicing进一步引入**效用感知的隐私预算优化分配**。若在所有24个位平面（3个色道×8个比特位）上均匀分配总预算$\varepsilon_{\text{total}}$，则MSB和LSB受到同等程度的扰动，导致重要结构信息被不必要地破坏。消融实验证实，均匀分配导致AgeDB-30上的面部识别准确率从96.68%骤降至89.82%（Table 3）。

LDP-Slicing的优化策略基于两个维度的异质性：**色道重要性**和**位重要性**。亮度通道（Y）承载了主要的空间结构信息，而色度通道（Cb、Cr）对识别任务的贡献相对较小（Figure 3验证了这一判断）。同时，高位平面（MSB）的扰动对像素重建值的失真贡献远大于低位平面（LSB）。通过求解约束优化问题：

$$\min_{\{\varepsilon_{c,b}\}} \sum_{c,b} \frac{W_{c,b}}{\varepsilon_{c,b}} \quad \mathrm{s.t.} \sum_{c,b} \varepsilon_{c,b} = \varepsilon_{\mathrm{total}},\; \varepsilon_{c,b} \geq 0$$

得到闭式解$\varepsilon_{c,b} = \varepsilon_{\text{total}} \cdot \frac{\sqrt{W_{c,b}}}{\sum_{i,j} \sqrt{W_{i,j}}}$，其中权重$W_{c,b}$编码了位平面的相对重要性。该解表明，隐私预算应按权重平方根的比例分配——重要性越高的位平面获得越多的预算（即更低的扰动概率），从而在严格满足ε-LDP的前提下最大化下游任务效用。

### 感知混淆模块：防御人类视觉检查的补充机制

LDP-Slicing还包含一个独立的感知混淆模块：通过1阶Haar离散小波变换（DWT）将图像分解为LL（低频逼近）和LH、HL、HH（高频细节）子带，将LL子带系数置零后通过逆DWT重构。这一操作去除了人类视觉系统最敏感的低频信息，使得私有化图像对人类观察者呈现为无法辨识的模糊状态，从而防御肉眼检查这一实际部署中的常见威胁。

消融实验表明，移除LL剪枝仅导致轻微的性能下降（Table 3, 配置A vs D），说明该模块主要服务于人类感知防御，对机器识别任务的影响可控。同时，以DCT剪枝替代DWT剪枝会降低效用（Table 3, 配置C vs D），验证了DWT更好地保留了机器识别所需的高频细节。

### 适用边界与局限性

尽管LDP-Slicing在面部识别和图像分类基准上取得了显著的隐私-效用折衷优势，其适用边界存在以下限制：

1. **极低隐私预算下的效用衰减**：当ε_total < 1时，所有位平面的扰动概率急剧上升，效用下降较为明显。这是LDP机制的理论下界所决定的，但位平面分解策略在一定程度上延缓了这一衰减。

2. **静态权重假设**：色度权重（Y:Cb:Cr = 4:1:1）为手工设定的静态值，虽然实验有效（Table 7验证了该权重的优越性），但未必是全局最优。针对不同下游任务，可学习的权重分配可能进一步改善隐私-效用平衡。

3. **跨数据集泛化能力**：在VGGFace2和CelebA等跨数据集场景中，中等隐私预算下的准确率仍较低，表明该方法对域偏移的鲁棒性有限。

4. **对抗性攻击的验证边界**：虽然LDP-Slicing在白盒重建攻击（攻击者完全知晓流水线并训练专用反演模型）和黑盒重建攻击下均展示了较强的抵抗性（Figure 5, Figure 6），但在更复杂的虚拟对抗样本或自适应攻击下的表现仍需进一步验证。

### 开放问题

1. **可学习权重优化**：能否通过端到端学习自动优化色道和位重要性权重，使隐私预算分配自适应于具体下游任务的数据分布特性？

2. **跨模态扩展**：基于位平面的LDP机制能否扩展到视频数据（时域位平面）或其他高维结构化数据（如体素、多光谱图像），同时保持隐私-效用折衷的优势？

3. **与中心化DP的协同**：若将LDP-Slicing输出的私有图像直接用于DP-SGD训练，能否结合本地和中心化隐私保证的优势，进一步提升最终模型的隐私-效用前沿？初步证据来自CIFAR-10/100上的对比实验（Figure 7），其中LDP-Slicing在ε≤12时优于中心化的DP-SGD，但协同使用的潜力尚未被探索。

4. **纯位平面扰动的理论上界**：是否存在不需要LL剪枝而仅依靠位平面扰动本身即可完全抵抗强重建攻击的理论保证？当前LL剪枝作为补充防御机制，其必要性是否可以通过更精细的预算分配策略来消除，是一个开放的理论问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/LDP_Slicing_Local_Differential_Privacy_for_Images_via_Randomized_Bit_Plane_Slicing.pdf]]
