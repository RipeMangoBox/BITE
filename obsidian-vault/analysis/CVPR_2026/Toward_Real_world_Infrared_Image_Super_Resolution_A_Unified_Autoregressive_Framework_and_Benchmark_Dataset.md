---
title: "Toward Real-world Infrared Image Super-Resolution: A Unified Autoregressive Framework and Benchmark Dataset"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Toward_Real_world_Infrared_Image_Super_Resolution_A_Unified_Autoregressive_Framework_and_Benchmark_Dataset.pdf
project_link: null
code_link: "https://github.com/JZD151/Real-IISR"
aliases:
- RI
- TRWIISRUAFBD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 提出 Real-IISR 统一自回归框架，通过热-结构引导模块（TSG）显式编码热语义和边缘信息，条件自适应码本（CAC）动态调制离散表示，以及热顺序一致性损失强制单调性，从而解决上述瓶颈。
primary_logic: 将热辐射分布与结构边缘作为双重先验，通过自适应注意力融合，可缓解红外超分中的热-结构错位；在此基础上，动态码本调制和排序约束进一步保证重建的物理一致性和纹理真实性。
claims:
- FLIR-IISR 数据集包含 1,457 对真实 LR-HR 红外图像，涵盖 6 城市、3 季节、12 场景，填补了真实红外超分数据集的空白。
- TSG 模块通过可学习注意力门控机制自适应融合热图和边缘图，防止模型过度关注高温区域而忽略真实边界。
- CAC 利用低秩扰动根据退化条件动态调整码本嵌入，显著减轻量化偏差和纹理失真。
- FLIR-IISR Set5 上 MUSIQ = 59.9000
---

# Toward Real-world Infrared Image Super-Resolution: A Unified Autoregressive Framework and Benchmark Dataset

> [!tip] 核心洞察
> 将热辐射分布与结构边缘作为双重先验，通过自适应注意力融合，可缓解红外超分中的热-结构错位；在此基础上，动态码本调制和排序约束进一步保证重建的物理一致性和纹理真实性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向真实世界红外图像超分辨率的统一自回归框架与基准数据集 |
| 英文题名 | Toward Real-world Infrared Image Super-Resolution: A Unified Autoregressive Framework and Benchmark Dataset |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.04745) · [Code](https://github.com/JZD151/Real-IISR) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Real-IISR |
| Dataset | FLIR-IISR Set5, M3FD |

> [!tip] 效果简介
> - FLIR-IISR Set5 上，MUSIQ 59.9000 vs 优于其他 9 种对比方法 (最高)；PSNR 28.5126 vs 优于其他 9 种对比方法 (最高)；SSIM 0.8278 vs 优于其他 9 种对比方法 (最高)。
> - M3FD (Set5/15) 上，MUSIQ 最优（具体数值见论文） vs 优于其他对比方法 (最高)；PSNR / SSIM / LPIPS 最优（具体数值见论文） vs 优于其他对比方法 (最佳)。
> - 效率对比 上，FPS 2.45 vs 略低于最快方法，但速度快于基于扩散的 VARSR (比 VARSR 快 6%)。

## 概要

真实世界红外图像超分辨率（IISR）面临两大瓶颈：**真实配对红外退化数据集的缺失**，以及**红外辐射与结构边界的内在错位**。现有方法依赖合成降质模拟，无法重现光学-传感器耦合退化，且忽略热分布与物体边界的对齐关系，导致重建结果出现边界失真和热漂移。

针对上述问题，本文提出 **Real-IISR**，一个统一的**自回归框架**，核心包含三个创新设计：（1）**热-结构引导模块（TSG）**，通过可学习注意力门控自适应融合热语义与边缘结构，提供双重先验引导；（2）**条件自适应码本（CAC）**，根据退化条件以低秩扰动动态调制离散码本嵌入，减轻量化偏差与纹理失真；（3）**热顺序一致性损失（L_TOC）**，强制保持超分结果与高分辨率图像之间的温度排序单调性，保证物理一致性。

为支撑真实场景评估，本文构建了 **FLIR-IISR 数据集**，包含 1,457 对真实 LR-HR 红外图像，覆盖 6 个城市、3 个季节、12 类场景及光学/运动两种真实模糊模式，填补了真实红外超分数据集的空白。

在 FLIR-IISR 和 M3FD 两个基准上，Real-IISR 在 PSNR（28.51）、SSIM（0.8278）、LPIPS（0.1615）及 MUSIQ（59.90）等指标上均优于 9 种对比方法（包括通用 ISR 方法 HAT、BI-DiffSR、PFT-SR，红外专用方法 CoRPLE、InfraFFN、DifIISR，以及真实世界方法 RealSR、SinSR、VARSR），同时推理速度（2.45 FPS）快于扩散模型 VARSR。消融实验验证了 TSG、CAC 和 L_TOC 各自对边界保真、纹理稳定性和热排序一致性的关键贡献。



红外图像超分辨率（Infrared Image Super-Resolution, IISR）旨在从低分辨率红外输入重建高分辨率细节，在安防监控、自动驾驶、军事侦察等任务中具有关键价值。然而，现有研究长期受困于两大瓶颈，导致方法向真实场景迁移时性能急剧退化。

**瓶颈一：真实配对红外退化数据缺失。** 现有 IISR 方法普遍依赖合成降质（如双三次下采样）构建训练对，但这种简化无法模拟真实红外成像中光学模糊、运动模糊与传感器噪声的复杂耦合。由于缺乏真实世界配对数据集，模型在合成域上学到的映射难以泛化至实际退化分布，形成“合成-真实”鸿沟。

**瓶颈二：热辐射与结构边界的固有错位。** 红外图像以热辐射强度编码场景信息，但高温区域常跨越物体边界，导致热分布与几何结构不一致。现有方法（包括通用图像超分方法如 **HAT**、**BI-DiffSR**、**PFT-SR**（Long et al., CVPR 2025），以及专用红外超分方法如 **CoRPLE**（Li et al., ECCV 2024）、**InfraFFN**（Qin et al., 2025）、**DifIISR**（Li et al., CVPR 2025））均未显式建模这一错位关系。其后果是：重建结果在高温区域边界处出现模糊、伪影或“热漂移”——像素强度无法忠实反映真实温度排序，破坏红外图像的物理语义。

上述瓶颈的因果链条可归纳为：缺乏真实数据 → 退化建模失真 → 热-结构错位被忽视 → 边界失真与热漂移。因此，亟需一个能同时填补数据空白并显式编码热-结构双重先验的统一框架。本文正是基于这一动机，提出 **Real-IISR** 统一自回归框架，并构建首个大规模真实配对红外超分数据集 **FLIR-IISR**，从数据与模型两侧协同突破上述瓶颈。



## 核心方法与创新机理

Real-IISR 的核心创新在于通过三个 **changed slots** 系统性地解决了真实世界红外超分辨率中“热-结构错位”与“退化条件失配”两大瓶颈，形成了从引导编码、动态离散表示到物理约束的完整链路。

### 1. 特征引导：热-结构双重先验的自适应融合

现有方法通常将红外图像视为普通灰度图处理，忽略了热辐射分布与物体结构边界之间的内在错位——高温区域未必对应真实边缘，导致重建结果出现边界模糊或热漂移。Real-IISR 提出的 **Thermal-Structural Guidance (TSG)** 模块首次将热辐射语义与结构边缘作为双重先验进行显式编码，并通过可学习的注意力门控机制实现自适应融合：

$$
\mathbf{F}_{\mathrm{Fused}} = \mathbf{F}_{\mathrm{Heat}} \odot \mathbf{W} + \mathbf{F}_{\mathrm{Edge}} \odot (\mathbf{1} - \mathbf{W})
$$

其中门控权重 $\mathbf{W} = \sigma(L(\mathbf{A}) + G(\mathbf{A}))$，$\mathbf{A} = \mathbf{F}_{\mathrm{Heat}} + \mathbf{F}_{\mathrm{Edge}}$。该设计使模型能够动态平衡热特征与结构特征的贡献，防止过度关注高亮热区而忽略真实物体轮廓。融合后的引导特征通过交叉注意力机制传播至低分辨率特征，进一步抑制对高温区域的过拟合。

### 2. 码本设计：退化条件感知的动态嵌入调制

传统 VQ-VAE 类方法采用静态码本查表，在真实红外退化（光学模糊、运动模糊等空间异质性退化）下容易出现码本选择偏差和量化伪影。Real-IISR 的 **Condition-Adaptive Codebook (CAC)** 通过低秩扰动机制，根据退化条件向量 $\mathbf{h}(g)$ 对每个码本嵌入进行动态调制：

$$
\mathbf{Z}^{\prime}(g)[i] = \mathbf{Z}[i] + \tanh(\alpha) \big[ (\mathbf{U}_i \odot \mathbf{h}(g)) \mathbf{V}^{\top} \big]
$$

其中 $\mathbf{U}_i$、$\mathbf{V}$ 为低秩分解矩阵，$\alpha$ 控制扰动幅度。这种设计使得同一码本在不同退化场景下能产生差异化的离散表示，显著减轻了纹理失真和热分布不一致问题。

### 3. 损失函数：热顺序一致性约束

红外图像具有物理上的单调性——温度越高的区域像素值越大。现有方法仅依赖交叉熵和 MSE 损失，无法显式保证这一物理约束。Real-IISR 引入 **Thermal Order Consistency Loss** $\mathcal{L}_{\mathrm{TOC}}$，在相邻 patch 对上惩罚温度排序反转：

$$
\mathcal{L}_{\mathrm{TOC}} = \frac{1}{|\Omega|} \sum_{(i,j)\in\Omega} \mathrm{ReLU}\Big(-\big[(\mathbf{I}_{\mathrm{SR}}^{p}(i) - \mathbf{I}_{\mathrm{SR}}^{p}(j)) \times (\mathbf{I}_{\mathrm{HR}}^{p}(i) - \mathbf{I}_{\mathrm{HR}}^{p}(j))\big]\Big)
$$

该损失强制 SR 图像与 HR 图像在局部区域保持一致的强度排序关系，有效抑制了热峰漂移和局部温度压缩。

### 4. 生成范式：自回归逐级生成

与常见的扩散模型（如 **BI-DiffSR**、**DifIISR** (Li et al., CVPR 2025)）不同，Real-IISR 采用 VAR 自回归框架进行“下一尺度预测”的逐级生成。消融实验表明，VAR 框架在 PSNR (28.51)、LPIPS (0.1615) 和 MUSIQ (59.90) 上均优于扩散基线，且推理速度比扩散增强的 **VARSR** (Qu et al., arXiv 2025) 快 6%，验证了自回归范式更匹配红外成像的离散空间结构。

总体训练目标为上述三个损失项的加权组合：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{CE}} + \lambda_{1} \mathcal{L}_{\mathrm{MSE}} + \lambda_{2} \mathcal{L}_{\mathrm{TOC}}
$$

其中 $\lambda_1 = 0.2$，$\lambda_2 = 0.8$，体现了对物理一致性约束的高度重视。



Real‑IISR 是一个面向真实世界红外图像超分辨率的统一自回归框架，其核心设计目标是在单一模型中同时解决**热辐射‑结构边界错位**和**真实退化多样性**两大瓶颈。框架的整体数据流可概括为：输入真实低分辨率红外图像 → 多模态先验编码 → 退化感知离散表示 → 逐尺度自回归生成 → 物理一致性约束输出。

### 模块组成与信息流

框架由三个关键功能模块和一个生成主干构成，其拓扑关系如 Figure 2 所示。

![[assets/figures/papers/paper_list_l788_https_arxiv_org_abs_2603_04745/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Real-IISR. The Thermal-Structural Guidance (TSG) module fuses thermal priors for degradation-aware encoding. The VAR backbone performs scale-by-scale generation via next-scale prediction, while the Condition-Adaptive Codebook (CAC) dynamically adjusts quantized embeddings based on degradation-aware priors for thermal fidelity. Finally, the Thermal Order Consistency Loss LTOC preserves physically consistent thermal ordering*

1. **热‑结构引导模块 (Thermal‑Structural Guidance, TSG)**  
   作为入口级编码器，TSG 从低分辨率观测中显式提取热辐射语义特征 $\mathbf{F}_{\mathrm{Heat}}$ 和结构边缘特征 $\mathbf{F}_{\mathrm{Edge}}$。二者通过可学习的注意力门控权重 $\mathbf{W}$ 进行自适应融合：
   
$$
\mathbf{F}_{\mathrm{Fused}} = \mathbf{F}_{\mathrm{Heat}} \odot \mathbf{W} + \mathbf{F}_{\mathrm{Edge}} \odot (\mathbf{1} - \mathbf{W})
$$

   融合后的引导特征 $\mathbf{F}_{\mathrm{Fused}}$ 通过交叉注意力机制注入低分辨率特征空间，防止模型过度关注高温区域而忽略真实物体边界，从而在源头缓解热‑结构错位问题。

2. **VAR 自回归主干 (VAR backbone)**  
   采用“下一尺度预测”(next‑scale prediction) 的生成范式，将超分辨率过程分解为从粗到细的逐级 token 生成。与常见的扩散模型不同，VAR 的离散多尺度结构天然匹配红外图像中空间辐射分布的层次性，且推理速度优于基于扩散的同类方案（如 VARSR）。

3. **条件自适应码本 (Condition‑Adaptive Codebook, CAC)**  
   在 VAR 的离散表示空间中，CAC 替代传统的静态码本查表。给定退化感知的条件向量 $\mathbf{h}(g)$，每个码本嵌入 $\mathbf{Z}[i]$ 通过低秩扰动进行动态调制：
   
$$
\mathbf{Z}^{\prime}(g)[i] = \mathbf{Z}[i] + \tanh(\alpha) \big[ (\mathbf{U}_i \odot \mathbf{h}(g)) \mathbf{V}^{\top} \big]
$$

   这一机制使码本能够根据输入图像的退化类型（光学模糊、运动模糊等）自适应调整离散表示，显著减轻量化偏差和纹理失真。

4. **损失函数体系**  
   训练目标由三项损失加权联合驱动：
   
$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{CE}} + \lambda_{1} \mathcal{L}_{\mathrm{MSE}} + \lambda_{2} \mathcal{L}_{\mathrm{TOC}}
$$

   - $\mathcal{L}_{\mathrm{CE}}$：token 级交叉熵损失，监督离散表示预测；
   - $\mathcal{L}_{\mathrm{MSE}}$：像素级均方误差，保证重建保真度；
   - $\mathcal{L}_{\mathrm{TOC}}$：热顺序一致性损失，在相邻 patch 对上惩罚温度排序反转，强制保持 SR 与 HR 之间的物理单调性（见 Eq. 3）。

其中 $\lambda_1=0.2$、$\lambda_2=0.8$，表明热顺序一致性约束在训练中占据较高权重，体现了红外图像物理先验的重要性。

### 输入输出规范

- **输入**：真实低分辨率红外图像（在 FLIR‑IISR 数据集中，LR 与 HR 的空间分辨率比为 4×，即 128×128 → 512×512）。
- **输出**：高分辨率红外重建图像，同时保持热辐射分布的结构一致性和纹理真实性。
- **中间表示**：TSG 输出的融合引导特征作为全局条件贯穿 VAR 主干的各级生成，CAC 在每一尺度提供退化自适应的离散码本支持。

### 框架设计的因果逻辑

上述模块并非简单堆叠，而是围绕红外超分的两个根本瓶颈形成了因果闭环：TSG 解决**热‑结构错位**→ 为后续生成提供准确的空间先验；CAC 解决**退化多样性**→ 使离散表示能够灵活匹配真实世界的复杂降质；$\mathcal{L}_{\mathrm{TOC}}$ 则从物理规律层面约束生成结果的热力学一致性。三者协同，使得 Real‑IISR 在 FLIR‑IISR 和 M3FD 两个真实红外数据集上均取得了最优的有参/无参指标（见表 1、表 2），同时保持 2.45 FPS 的推理速度（NVIDIA A800），在效率‑质量权衡上优于扩散基线。



### 3.1 热-结构引导模块 (Thermal-Structural Guidance, TSG)

真实世界红外图像中，热辐射分布与物体结构边界存在内在错位——高温区域常跨越多个物体边界，而现有方法缺乏对此双重先验的显式建模。TSG 模块通过可学习的注意力门控机制，自适应融合热语义特征 $\mathbf{F}_{\mathrm{Heat}}$ 与结构边缘特征 $\mathbf{F}_{\mathrm{Edge}}$，形成统一的引导表示。

融合过程由以下公式定义：

$$\mathbf{F}_{\mathrm{Fused}} = \mathbf{F}_{\mathrm{Heat}} \odot \mathbf{W} + \mathbf{F}_{\mathrm{Edge}} \odot (\mathbf{1} - \mathbf{W})$$

其中，门控权重 $\mathbf{W}$ 通过 $\mathbf{W} = \sigma(L(\mathbf{A}) + G(\mathbf{A}))$ 计算，$\mathbf{A} = \mathbf{F}_{\mathrm{Heat}} + \mathbf{F}_{\mathrm{Edge}}$，$L(\cdot)$ 和 $G(\cdot)$ 分别为局部和全局特征变换，$\sigma$ 为 Sigmoid 激活。该设计使模型能够根据输入内容动态平衡热辐射与结构信息的贡献，防止过度关注高温区域而忽略真实边界。

随后，融合特征通过交叉注意力机制注入低分辨率特征：

$$\mathrm{softmax}\left(\frac{Q K^{\top}}{\sqrt{d}}\right) V$$

此操作将热-结构先验传播至低分辨率表示中，有效抑制模型对高强度热区的过拟合，同时促进准确边界重建。

### 3.2 条件自适应码本 (Condition-Adaptive Codebook, CAC)

传统 VQ-VAE 类方法采用静态码本查表，在真实红外退化下易产生量化偏差和纹理失真。CAC 通过低秩扰动根据退化条件动态调整码本嵌入，其更新规则为：

$$\mathbf{Z}^{\prime}(g)[i] = \mathbf{Z}[i] + \tanh(\alpha) \big[ (\mathbf{U}_i \odot \mathbf{h}(g)) \mathbf{V}^{\top} \big]$$

其中，$\mathbf{Z}[i]$ 为第 $i$ 个原始码本嵌入，$\mathbf{h}(g)$ 为从低分辨率观测及热-结构先验中提取的条件向量，$\mathbf{U}_i$ 和 $\mathbf{V}$ 构成低秩扰动项，$\tanh(\alpha)$ 控制扰动幅度。该机制使码本能够适应不同退化模式（光学模糊、运动模糊等），显著减轻量化偏差，生成结构一致且纹理丰富的红外重建结果。

### 3.3 热顺序一致性损失 (Thermal Order Consistency Loss, $\mathcal{L}_{\mathrm{TOC}}$)

红外图像具有物理单调性：像素强度与温度呈正相关。为保持此约束，提出热顺序一致性损失，在相邻 patch 对上惩罚温度排序反转：

$$\mathcal{L}_{\mathrm{TOC}} = \frac{1}{|\Omega|} \sum_{(i,j)\in\Omega} \mathrm{ReLU}\Big(-\big[(\mathbf{I}_{\mathrm{SR}}^{p}(i) - \mathbf{I}_{\mathrm{SR}}^{p}(j)) \times (\mathbf{I}_{\mathrm{HR}}^{p}(i) - \mathbf{I}_{\mathrm{HR}}^{p}(j))\big]\Big)$$

其中，$\Omega$ 为相邻 patch 对集合，$\mathbf{I}^{p}$ 表示 patch 的平均像素强度。当超分结果的强度差符号与高分辨率真值不一致时，ReLU 激活惩罚项生效，强制维持温度排序的单调性。

### 3.4 总体训练目标

整体训练目标由三部分组成：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{CE}} + \lambda_{1} \mathcal{L}_{\mathrm{MSE}} + \lambda_{2} \mathcal{L}_{\mathrm{TOC}}$$

其中 $\mathcal{L}_{\mathrm{CE}}$ 为 token 级交叉熵损失（监督 VAR 自回归预测），$\mathcal{L}_{\mathrm{MSE}}$ 为像素级均方误差损失，$\lambda_1 = 0.2$、$\lambda_2 = 0.8$ 为平衡系数。该组合在 token 级监督、像素保真与物理一致性之间取得平衡。

### 补充图表

![[assets/figures/papers/paper_list_l788_https_arxiv_org_abs_2603_04745/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative ablation on the Thermal-Structural Guidance (TSG) and Condition-Adaptive Codebook (CAC)*



## 实验与关键发现

### 主实验结果

Real-IISR 在构建的真实世界红外超分辨率基准 FLIR-IISR 和公开红外数据集 M3FD 上与 9 种竞争方法进行了全面对比，包括通用图像超分方法（**HAT**、**BI-DiffSR**、**PFT-SR** (Long et al., CVPR 2025)）、红外超分方法（**CoRPLE** (Li et al., ECCV 2024)、**InfraFFN** (Qin et al., 2025)、**DifIISR** (Li et al., CVPR 2025)）以及真实世界超分方法（**RealSR**、**SinSR** (Wang et al., CVPR 2024)、**VARSR** (Qu et al., arXiv 2025)）。所有对比方法均在 FLIR-IISR 数据集上以相同设置（分辨率从 512×512 降采样至 128×128，随机裁剪增强）重新训练，确保公平性。评估采用有参考指标（PSNR、SSIM、LPIPS）和无参考指标（MUSIQ、MANIQA）双重标准。

在无参考感知质量方面，Real-IISR 在 FLIR-IISR Set5 上取得 MUSIQ 59.90 的最高分，在所有子集上均优于其他对比方法（Table 1）。在 M3FD 数据集上同样取得最优 MUSIQ 表现。在有参考重建指标方面，Real-IISR 在 FLIR-IISR Set5 上取得 PSNR 28.5126、SSIM 0.8278、LPIPS 0.1615 的最佳综合表现（Table 2），在 M3FD 子集上同样保持领先。

![[assets/figures/papers/paper_list_l788_https_arxiv_org_abs_2603_04745/figures/004_Table_1.jpg]]
*Table 1: No-reference Metrics Comparison on FLIR-IISR and*

![[assets/figures/papers/paper_list_l788_https_arxiv_org_abs_2603_04745/figures/005_Table_2.jpg]]
*Table 2: Reference-based Metrics Comparison on FLIR-IISR and M3FD datasets. The best is in bold, while the second is underlined. For M3FD, Set5/15 are randomly sampled subsets. For FLIR-IISR, Set5/15 corresponds to motion/optical blur*

在效率方面，Real-IISR 在单张 NVIDIA A800 GPU 上实现 2.45 FPS 的推理速度（Figure 4），尽管参数量为 1144.6M，属于中等规模，但推理速度比基于扩散的 VARSR 快约 6%。这一效率优势源于其简洁的自回归架构设计，无需额外的扩散精炼步骤。

![[assets/figures/papers/paper_list_l788_https_arxiv_org_abs_2603_04745/figures/006_Figure_4.jpg]]
*Figure 4: Efficiency comparison in terms of perceptual MUSIQ and FPS; circle diameter indicates model parameters*

### 消融实验

为验证各核心组件的有效性，论文进行了系统的定性和定量消融实验。

**热-结构引导模块（TSG）的移除**导致热辐射与物体边界对齐失准，边缘模糊、结构轮廓减弱。定量结果表明 MUSIQ 和 SSIM 显著下降（Figure 6、Figure 7），验证了显式编码热语义和边缘信息作为双重先验的必要性。

**条件自适应码本（CAC）的排除**导致纹理不稳定、热分布不一致，MUSIQ 和 SSIM 出现明显退化（Figure 6、Figure 7）。这证实了动态码本调制对减轻量化偏差和纹理失真的关键作用——静态码本查表无法适应真实世界中空间变化的红外退化。

**热顺序一致性损失（L_TOC）的移除**导致热强度排序被打乱，出现热峰漂移和局部温度压缩现象（Figure 8）。定量消融显示，缺少 L_TOC 后 PSNR 和 MUSIQ 均下降，验证了该损失在保持红外图像物理单调性方面的重要性。

同时使用 TSG 和 CAC 取得了最佳整体性能，验证了两者的协同效应。此外，VAR 自回归框架与扩散框架的对比消融表明，VAR 基线在 PSNR (28.51)、LPIPS (0.1615) 和 MUSIQ (59.90) 上均优于扩散变体（Figure 9），说明逐级预测的自回归范式更适合红外成像的离散空间结构。

![[assets/figures/papers/paper_list_l788_https_arxiv_org_abs_2603_04745/figures/010_Figure_9.jpg]]
*Figure 9: Quantitative ablation on the baseline choice of diffusion and VAR*

### 关键图表结论

- **Table 1 & Table 2**：Real-IISR 在 FLIR-IISR 和 M3FD 两个数据集上，无论有参考还是无参考指标均取得最优综合表现，证明其统一的退化自适应能力优于现有通用和专用方法。
- **Figure 4**：Real-IISR 在感知质量-推理速度的权衡中占据优势位置，以中等参数量实现接近最快的推理速度，且感知质量最高。
- **Figure 5**：定性对比中，Real-IISR 重建的红外图像在灰度波动曲线上最接近 HR 真值，其他方法在热峰位置和边界过渡区域存在明显偏差。
- **Figure 6 & Figure 7**：TSG 和 CAC 的消融可视化清晰展示了热-结构错位和纹理失真的具体表现，定量消融进一步量化了两者的独立与协同贡献。
- **Figure 8 & Figure 9**：L_TOC 消融的热峰漂移现象和 VAR 框架的定量优势，分别从物理一致性和生成范式角度支撑了方法设计的合理性。

![[assets/figures/papers/paper_list_l788_https_arxiv_org_abs_2603_04745/figures/011_Figure_7.jpg]]
*Figure 7: Quantitative ablation of TSG, CAC, and*

![[assets/figures/papers/paper_list_l788_https_arxiv_org_abs_2603_04745/figures/008_Figure_8.jpg]]
*Figure 8: Qualitative ablation on the Thermal Order Consistency Loss*

![[assets/figures/papers/paper_list_l788_https_arxiv_org_abs_2603_04745/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of IISR with SOTA methods on FLIR-IISR and M3FD datasets. The graph illustrates grayscale fluctuations along the blue-marked sampling line, and red-marked sampling line denotes the HR*

### 补充图表

![[assets/figures/papers/paper_list_l788_https_arxiv_org_abs_2603_04745/figures/003_Figure_3.jpg]]
*Figure 3: Data collection pipeline of FLIR-IISR*



## 定位与知识库关联

### 方法谱系：从通用超分到红外物理先验

Real-IISR 的谱系可沿两条轴线追溯：**图像超分辨率（ISR）的生成范式演进**，以及**红外图像超分辨率（IISR）的物理先验引入**。

在通用 ISR 轴线上，该工作继承了视觉自回归（VAR）的“下一尺度预测”生成范式，将其从自然图像生成迁移至红外超分重建。与基于扩散的生成方法（如 **SinSR**（Wang et al., CVPR 2024）、**VARSR**（Qu et al., arXiv 2025））相比，VAR 主干通过逐级离散 token 预测天然匹配红外成像的离散空间结构，避免了扩散模型在红外域中常见的过度平滑和热漂移问题。定量消融证实：VAR 基线的 PSNR（28.51）、LPIPS（0.1615）和 MUSIQ（59.90）均优于扩散变体。

在 IISR 轴线上，Real-IISR 的独特贡献在于首次将**热辐射分布与结构边缘作为双重显式先验**引入超分流程。此前的红外超分方法——如 **CoRPLE**（Li et al., ECCV 2024）、**InfraFFN**（Qin et al., 2025）和 **DifIISR**（Li et al., CVPR 2025）——或依赖隐式特征学习，或侧重频域增强，均未显式建模热-结构错位这一红外域的核心瓶颈。Real-IISR 通过 TSG 模块的自适应注意力门控机制，以可学习权重 $\mathbf{W}$ 动态平衡热图 $\mathbf{F}_{\mathrm{Heat}}$ 与边缘图 $\mathbf{F}_{\mathrm{Edge}}$ 的贡献，从机制层面解决了“高温区域过拟合、真实边界被忽略”的问题。

### 关键技术差异化

与现有方法的四个关键差异槽位如下：

| 差异维度 | 基线方法特征 | Real-IISR 创新 |
|---------|------------|---------------|
| **特征引导** | 未显式融合热与结构先验（如 CoRPLE、DifIISR） | TSG 模块通过自适应注意力门控融合热图和边缘图，提供热-结构双重引导 |
| **码本设计** | 静态码本查表（通用 VQ-VAE 范式） | CAC 根据退化条件通过低秩扰动 $\mathbf{Z}^{\prime}(g)[i] = \mathbf{Z}[i] + \tanh(\alpha) [(\mathbf{U}_i \odot \mathbf{h}(g)) \mathbf{V}^{\top}]$ 动态调整嵌入 |
| **损失函数** | 仅交叉熵与 MSE 损失 | 额外引入热顺序一致性损失 $\mathcal{L}_{\mathrm{TOC}}$，强制保持 SR 与 HR 之间的温度排序单调性 |
| **生成范式** | 基于扩散的生成模型（如 SinSR、VARSR） | 基于 VAR 的自回归“下一级预测”生成，匹配红外成像的离散空间结构 |

CAC 模块的低秩扰动设计尤为关键：它避免了静态码本在真实退化条件下的量化偏差和纹理失真，使离散表示能够根据红外场景的空间变异退化条件自适应调整。消融实验表明，排除 CAC 会导致纹理不稳定和热分布不一致，MUSIQ 和 SSIM 均明显下降。

### 适用边界

Real-IISR 的设计面向**真实世界红外图像超分辨率**场景，其适用边界由以下因素界定：

1. **数据依赖**：方法假设存在真实配对 LR-HR 红外数据用于训练。FLIR-IISR 数据集覆盖 6 城市、3 季节、12 场景和两类真实模糊（光学模糊与运动模糊），但模型在分布外退化类型（如极端噪声、非均匀热晕）上的泛化能力尚未验证。

2. **物理先验的有效域**：$\mathcal{L}_{\mathrm{TOC}}$ 基于“温度-像素强度单调关系”的物理假设。在存在热交叉、多热源叠加或非朗伯体辐射的场景中，该单调性可能被破坏，损失函数的约束效果需要进一步检验。

3. **计算效率**：模型参数量为 1144.6M，推理速度 2.45 FPS（单张 NVIDIA A800 GPU），虽比 VARSR 快 6%，但仍不适用于实时嵌入式红外系统（如无人机机载处理）。效率对比图（Figure 4）显示，Real-IISR 处于感知质量-速度权衡曲线的中上区域，但距离轻量化部署仍有差距。

4. **尺度因子**：当前验证基于 4× 超分（512×512 → 128×128），其他尺度因子的性能未经报告。

### 局限与开放问题

**已识别的局限**：

- **物理先验的鲁棒性**：TSG 和 $\mathcal{L}_{\mathrm{TOC}}$ 的有效性依赖于热图与边缘图的准确提取。在低对比度或低 SNR 红外场景中，边缘检测和热辐射估计的质量下降可能级联影响融合引导效果。论文未报告在此类极端条件下的性能退化程度。
- **单模态限制**：Real-IISR 仅利用红外单模态信息，未探索可见光-红外多模态融合在超分中的潜力。在部分场景中，可见光边缘信息可能弥补红外结构模糊的不足。
- **生成多样性控制**：自回归生成虽然保证了结构一致性，但在高度不确定的纹理区域可能产生确定性伪影。论文未讨论生成多样性与保真度之间的可控权衡。

**开放问题**：

1. **跨退化泛化**：FLIR-IISR 仅包含光学模糊和运动模糊两类真实退化。模型能否泛化至大气湍流、热晕、探测器非均匀性等其他真实红外退化类型，需要新的基准数据集和系统评估。

2. **物理先验的通用性**：$\mathcal{L}_{\mathrm{TOC}}$ 的单调性约束是否可推广至其他物理成像模态（如多光谱、高光谱超分），是一个值得探索的方向。

3. **轻量化与实时性**：如何在保持热-结构引导和动态码本调制优势的前提下，通过知识蒸馏、结构剪枝或高效注意力设计实现轻量化，是实际部署的关键瓶颈。

4. **无配对场景的拓展**：当前框架依赖配对 LR-HR 数据进行监督训练。在无法获取 HR 真值的真实场景中，能否通过自监督或物理模型驱动的方式实现有效训练，是一个重要的开放挑战。

> **注意**：上述局限部分主要基于方法设计的逻辑推断和实验覆盖范围的分析，论文本身未设专门的“Limitations”章节。部分边界条件（如极端 SNR 下的性能）需要手工验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Toward_Real_world_Infrared_Image_Super_Resolution_A_Unified_Autoregressive_Framework_and_Benchmark_Dataset.pdf]]
