---
title: "ImmerIris: A Large-Scale Dataset and Benchmark for Off-Axis and Unconstrained Iris Recognition in Immersive Applications"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ImmerIris_A_Large_Scale_Dataset_and_Benchmark_for_Off_Axis_and_Unconstrained_Iris_Recognition_in_Immersive_Applications.pdf
project_link: null
code_link: null
aliases:
- ImmerIris
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 去除归一化（normalization-free），直接将裁剪并适当扩大的虹膜区域送入深度特征提取器。
primary_logic: 深度卷积网络（ResNet + ArcFace）本身已具备足够的非线性，能够从含有上下文线索的原始裁剪图像中学习鲁棒身份表征，从而替代传统精细但脆弱的归一化预处理。
claims:
- SOTA方法在传统CASIA-Iris-V4上FRR极低，但在ImmerIris协议（如Immer-Any）上FRR急剧升高至85%以上（FAR=1e-5），说明无法泛化。
- NormFree在所有综合与孤立挑战协议（Control, Fix, Select, Any, Occlusion, Dilation, Light, Gaze）上均显著优于归一化基线NormKeep及其他SOTA，在Immer-Any左眼上FRR@FAR 1e-5为52.04%，而NormKeep等普遍超过70%。
- 消融实验显示，即使换用更先进的归一化实现，NormKeep性能仅微幅提升；而将骨干网络缩小时NormFree仍保持优势，证明归一化是通用瓶颈而非实现细节。
- Immer-Control (Verification) 上 FRR@FAR 1e-5 (Left Eye) = 5.50%
---

# ImmerIris: A Large-Scale Dataset and Benchmark for Off-Axis and Unconstrained Iris Recognition in Immersive Applications

> [!tip] 核心洞察
> 深度卷积网络（ResNet + ArcFace）本身已具备足够的非线性，能够从含有上下文线索的原始裁剪图像中学习鲁棒身份表征，从而替代传统精细但脆弱的归一化预处理。

| 字段 | 内容 |
|------|------|
| 中文题名 | ImmerIris：面向沉浸式应用的大规模离轴无约束虹膜识别数据集与基准 |
| 英文题名 | ImmerIris: A Large-Scale Dataset and Benchmark for Off-Axis and Unconstrained Iris Recognition in Immersive Applications |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.10113) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | NormFree |
| Dataset | Immer-Control, Immer-Any, Immer-Gaze |

> [!tip] 效果简介
> - Immer-Control (Verification) 上，FRR@FAR 1e-5 (Left Eye) 5.50% vs 未明确给出一致基线，NormKeep 或 SOTA 普遍高于此 (NormFree达到该协议下最优或次优)。
> - Immer-Any (Verification) 上，FRR@FAR 1e-5 (Left Eye) 52.04% vs NormKeep（具体数值未单列，但远高于NormFree） (显著低于SOTA（如Gabor: 85.47%, OM: 88.48%）)。
> - Immer-Any (Identification) 上，Rank-1 Accuracy 94.39% vs SOTA中最高约90%左右 (较SOTA提升数个点)。

## 概要

传统虹膜识别依赖专用设备在受控条件下采集**正轴（on-axis）**图像，样本高度一致，现有SOTA方法在此类场景下已取得极低的错误率。然而，当应用场景转向消费级头戴显示设备（HMD）驱动的沉浸式环境时，采集条件变为**离轴（off-axis）且无约束**，导致虹膜图像出现扭曲、变化与退化（Figure 1）。本文的核心发现是：当前SOTA方法所依赖的**虹膜归一化（normalization）阶段在此类场景中极易失效**，产生严重扭曲的纹理，致使识别性能急剧崩溃——在传统CASIA-Iris-V4上FRR极低的方法，在ImmerIris的Immer-Any协议上FRR@FAR=1e-5飙升至85%以上（Table 3, Figure 2）。

针对这一瓶颈，本文提出**NormFree**：一种**免归一化（normalization-free）的端到端范式**。其核心操作是将传统两阶段流程（分割→轮廓参数化→极坐标归一化）替换为：仅通过预训练检测器获取可靠边界框→放大1.2倍以保留上下文→裁剪后直接送入ResNet IR-50骨干网络，以ArcFace损失进行判别性训练（Figure 6）。背后的机理是：深度卷积网络本身具备足够的非线性，能够从含有上下文线索的原始裁剪图像中学习鲁棒身份表征，从而替代传统精细但脆弱的归一化预处理。

主要实验结果验证了该范式的有效性：
- 在四个综合挑战协议（Control, Fix, Select, Any）上，NormFree在所有设置下均显著优于保留归一化的NormKeep基线及其他SOTA方法（**Gabor**（Daugman, Elsevier 2009）、**Ordinal Measures**（Sun and Tan, TPAMI 2008）、**Maxout系列**（Wei et al., TIFS 2022）等）。在最具挑战的Immer-Any左眼验证中，NormFree的FRR@FAR=1e-5为52.04%，而Gabor为85.47%、OM为88.48%（Table 4）。
- 在孤立挑战协议（Occlusion, Dilation, Light, Gaze）上，NormFree同样保持优势，尤其在注视变化（Gaze）协议下FRR@FAR=1e-3为16.40%（Table 5）。
- 消融实验表明：即使换用更先进的自适应归一化技术，NormKeep性能仅微幅提升；将骨干网络缩小至IR-18时NormFree仍保持优势，证明归一化阶段本身是通用瓶颈而非实现细节（Table 7）。

**局限性方面**，注视变化（gaze variation）是导致性能下降的最显著因素（平均约37%退化），当前NormFree尚未针对其专门优化；数据集受试者主要为20-40岁亚洲成年人，跨群体泛化性有待验证；此外，NormFree仍依赖预训练检测器，在极度遮挡或模糊时可能失效。



### 虹膜识别范式的历史路径与固有假设

虹膜识别在过去三十年中沿着一条高度受控的技术路径演进。自Daugman（Elsevier 2009）奠基性工作以来，主流方法——包括基于Gabor滤波的编码、**Ordinal Measures (OM)**（Sun and Tan, TPAMI 2008）、以及近年基于深度学习的**Maxout/UE-UGCL**（Wei et al., TIFS 2022）、**ComplexIrisNet**（Nguyen et al., TPAMI 2022）等——几乎无一例外地遵循**两阶段范式**：先通过虹膜分割与极坐标变换将环形虹膜区域展开为矩形归一化纹理，再对该纹理进行特征提取与匹配。这一范式的隐含前提是：采集图像在光轴对准、光照稳定、用户配合的条件下获取，虹膜边界清晰可辨，归一化操作能够可靠地将纹理映射到规范坐标系。

### 沉浸式场景下的范式失效

当应用场景从专用虹膜采集设备迁移至消费级头戴显示设备（HMD）时，上述前提被系统性地打破。如Figure 1所示，沉浸式环境中的眼部图像呈现**离轴视角、非均匀光照、注视方向变化、局部遮挡、运动模糊**等复合退化。此时，归一化阶段成为整个识别管线的致命瓶颈：分割误差与轮廓参数化失准导致极坐标展开产生严重扭曲的纹理（ill-unwrapped textures），这些纹理中的身份判别信息已被不可逆地破坏，后续无论采用何种特征提取器都难以挽回。

这一瓶颈并非个别方法的实现缺陷，而是**归一化操作本身的结构性脆弱性**：它要求精确的虹膜内外边界定位，而这一要求在沉浸式场景中恰恰难以满足。

### 跨场景泛化的崩溃：从受控到无约束

现有SOTA方法在传统数据集上的表现与其在沉浸式场景中的表现之间存在**灾难性断裂**。如Figure 2与Table 3所示，当这些方法在CASIA-Iris-V4（传统受控数据集）上训练并测试时，验证错误率（FRR）极低；但同样的模型在ImmerIris的Immer-Any协议上测试时，FRR急剧攀升至85%以上（FAR=1e-5），表明其习得的特征表示几乎无法泛化至离轴无约束条件。这一跨场景性能崩塌揭示了一个深层问题：**归一化阶段将模型的学习空间过度约束在受控纹理的狭窄流形上，使其丧失了应对分布偏移的鲁棒性。**

### 核心动机：绕开瓶颈而非修复瓶颈

面对这一困境，直接的工程直觉是改进归一化技术本身——例如采用更鲁棒的分割模型或自适应展开策略。然而，本文的核心判断是：**归一化本身即是瓶颈，而非其具体实现形式。** 消融实验（Table 7, Sec 5.6）为此提供了关键证据：即使换用更先进的归一化实现，NormKeep的性能仅获微幅提升；而完全去除归一化的NormFree在模型规模缩小时仍保持显著优势。

这一发现指向一个根本性的范式转换：**深度卷积网络（ResNet + ArcFace）本身已具备足够的非线性建模能力，能够直接从含有上下文线索的原始裁剪图像中学习鲁棒的身份表征，从而替代传统精细但脆弱的归一化预处理。** 换言之，与其在不可靠的归一化结果上“抢救”信息，不如让网络直接从更丰富的原始信号中自主学习不变性特征。

### 本文的核心回应

基于上述分析，本文提出**NormFree**——一种免归一化的端到端虹膜识别范式。该方法仅通过预训练检测器获取可靠边界框，经1.2倍扩展以包含眼周上下文后直接送入特征提取网络，彻底摒弃了极坐标变换与纹理归一化步骤。在ImmerIris数据集上构建的多维度评估协议（综合挑战与孤立挑战）下，NormFree在所有协议上均显著优于归一化基线及其他SOTA方法，验证了这一范式转换的有效性。



## 核心方法与创新机理

### 瓶颈诊断：归一化的脆弱性

现有虹膜识别方法普遍遵循 **Daugman** (Elsevier 2009) 提出的两阶段范式：先对眼部图像进行虹膜分割与轮廓参数化，再通过极坐标变换将环形虹膜区域归一化为矩形纹理，最后提取特征。这一流程在受控的轴上采集场景下表现优异，但在沉浸式离轴无约束场景中，归一化阶段极易失效——离轴视角、瞳孔扩张、注视变化等因素导致轮廓检测不可靠，产生严重扭曲的归一化纹理，进而使识别性能急剧崩溃。

**决定性证据**：在传统数据集 CASIA-Iris-V4 上，SOTA 方法的 FRR 极低；但在 ImmerIris 的 Immer-Any 协议下，**Gabor** 的 FRR@FAR=1e-5 飙升至 85.47%，**Ordinal Measures (OM)** 达 88.48%，**Maxout** 高达 94.09%（Table 3, Figure 2）。这一跨场景泛化崩溃直接指向归一化阶段在沉浸式条件下的根本性脆弱。

### 核心洞察：深度网络可替代精细预处理

论文的核心洞察在于：**深度卷积网络本身已具备足够的非线性表征能力，能够从原始裁剪图像中学习鲁棒的身份特征，从而替代传统精细但脆弱的归一化预处理**。这一判断基于以下因果链条：

- 归一化的本质是将虹膜纹理映射到规范空间以消除几何变化，但这一映射在离轴条件下本身不可靠。
- ResNet + ArcFace 的深度特征提取器具有强大的几何不变性学习能力，当输入图像包含适当的上下文线索（如虹膜周围区域）时，网络可以隐式地处理形变与变化。
- 因此，保留更多原始信息的“粗裁剪”输入，反而比“精细但错误”的归一化纹理更有利于识别。

### Changed Slot：预处理流程的范式转换

**NormFree** 相对于 SOTA 基线的唯一关键改动在于预处理流程（changed slot），实现了从“归一化依赖”到“归一化免除”的端到端范式转换：

| 模块 | 基线值（SOTA） | 提出值（NormFree） |
|------|--------------|-----------------|
| **预处理流程** | 两阶段范式：虹膜分割 → 轮廓参数化 → 极坐标变换 → 归一化为矩形纹理 | 端到端：预训练检测器获取边界框 → 扩大 1.2 倍以包含上下文 → 裁剪并 resize → 直接送入特征提取网络 |

具体而言，NormFree 的 pipeline 仅包含三个模块：

1. **虹膜区域检测与裁剪**：使用预训练检测器获取可靠边界框，扩展 1.2 倍以包含眼周上下文线索，裁剪后 resize 至网络输入尺寸（Sec 4, Figure 6）。
2. **ResNet IR-50 主干网络**：标准人脸识别 ResNet 架构，作为特征提取器（Sec 4）。
3. **ArcFace 损失训练**：基于角度边际的判别性目标函数，学习高度可区分的身份嵌入（Sec 4）。

这一设计的核心逻辑是：检测边界框比完整的归一化流程（分割 + 参数化 + 极坐标变换）更鲁棒，即便在离轴、遮挡、模糊等条件下也能提供可靠的区域定位；而深度网络可以从这个“粗糙但正确”的区域中自行学习不变表征。

### 消融验证：归一化是通用瓶颈而非实现细节

消融实验从两个角度验证了归一化瓶颈的普遍性（Table 7, Sec 5.6）：

- **归一化技术替换**：采用更先进的自适应归一化技术仅使 NormKeep 性能微幅提升，表明问题不在于具体归一化算法的实现质量，而是归一化阶段本身在沉浸式场景下的固有限制。
- **模型规模缩减**：将骨干网络从 IR-50 缩小至 IR-18 时，NormFree 依然优于 NormKeep 并超越多数 SOTA，证明免归一化的收益对模型规模不敏感，核心优势来自预处理范式的改变而非更大的模型容量。

### 局限与开放问题

尽管 NormFree 在所有综合与孤立挑战协议上均显著优于归一化基线，但以下问题仍待解决：

- **注视变化是最大退化源**：消融分析表明注视变化（gaze variation）平均导致约 36.99% 的性能退化（Sec 5.4），当前 NormFree 尚未针对其进行专门优化。
- **检测器依赖**：NormFree 仍依赖预训练检测器获取边界框，极端遮挡或模糊下的检测失败仍是潜在风险点。
- **跨群体泛化**：数据集受试者主要为 20-40 岁亚洲成年人，其他种族和年龄组的泛化性需进一步验证。



ImmerIris 提出的 **NormFree** 方法从根本上重构了虹膜识别的处理范式。传统 SOTA 方法普遍遵循 Daugman 经典的两阶段流水线：首先对眼部图像进行虹膜区域分割与轮廓参数化，再通过极坐标变换将环形虹膜展开（unwrap）为矩形归一化纹理，最后送入特征提取器。然而在沉浸式场景中，离轴拍摄、注视变化、光照波动与遮挡等因素使归一化阶段极易产生严重扭曲的纹理，成为整个系统的核心瓶颈（参见 Figure 6(a)）。

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/008_Figure_6.jpg]]
*Figure 6: Paradigm comparison between SOTAs and the proposed method. (a) SOTAs segment the iris region and unwrap the iris contour into a rectangular normalized texture. Unreliable normalization yields ill-unwrapped textures, degrading performance. (b) The proposed method dispenses with normalization and employs the cropped iris region, which is more robust and performs better in immersive iris recognition, as later experimentally found*

NormFree 采用**端到端的免归一化范式**，仅包含三个级联模块：

1. **虹膜区域检测与裁剪**  
   使用预训练的虹膜检测器获取稳定的边界框，将框扩大 1.2 倍以保留邻近眼周区域的上下文线索，裁剪后 resize 至网络输入尺寸。这一步骤替代了传统精细但脆弱的归一化流水线。

2. **ResNet IR-50 主干网络**  
   采用标准人脸识别中广泛使用的 ResNet IR-50 架构作为深度特征提取器。网络直接从包含上下文信息的原始裁剪图像中学习鲁棒的身份表征，利用其自身的非线性建模能力替代手工设计的几何变换。

3. **ArcFace 损失训练**  
   基于角度边际的判别性目标函数，将嵌入空间中的类内分布收紧、类间分布拉开，学习高度可区分的身份嵌入向量。

整个流水线的输入为 VR 头显采集的原始眼部图像，输出为固定维度的虹膜身份嵌入，直接用于验证（verification）或识别（identification）任务。与归一化基线 **NormKeep**（保留归一化但采用相同的骨干网络与损失函数）的对照设计，确保了性能差异仅源于预处理范式的不同，而非骨干网络或训练策略的优势。

Figure 6 直观对比了两种范式：传统范式在归一化阶段将环形虹膜展开为矩形纹理，失败时产生不可逆的纹理失真；NormFree 则绕过该步骤，直接利用裁剪后的虹膜区域进行端到端学习，从根本上规避了归一化失效带来的级联误差。



### 范式重构：从两阶段归一化到端到端免归一化

传统虹膜识别遵循Daugman提出的两阶段范式（Daugman, Elsevier 2009）：首先通过分割获取虹膜轮廓参数，经极坐标变换将环形虹膜展开为矩形归一化纹理，再由特征提取器编码为身份模板。这一流程在受控场景下极为成功，但其核心瓶颈在于**归一化阶段对成像条件的极端敏感性**——在沉浸式离轴无约束场景中，失真、退化等因素会导致展开纹理严重扭曲，使后续特征提取失效。

NormFree的因果调节变量是**彻底移除归一化阶段**，将范式重构为端到端流程：

1. **虹膜区域检测与裁剪**：使用预训练的虹膜检测器获取可靠边界框，将边界框扩大1.2倍以纳入眼周上下文线索，裁剪后resize至网络输入尺寸。
2. **ResNet IR-50主干网络**：采用标准人脸识别ResNet架构作为特征提取器。
3. **ArcFace损失训练**：基于角度边际的判别性目标函数，学习高度可区分的身份嵌入。

核心洞察在于：深度卷积网络（ResNet + ArcFace）本身已具备足够的非线性建模能力，能够从包含上下文线索的原始裁剪图像中直接学习鲁棒身份表征，从而替代传统精细但脆弱的归一化预处理。

### 关键公式

论文未提出新的数学公式或理论推导。方法层面的核心设计体现在**流程架构的简化**而非公式创新：

- **特征提取**：给定裁剪后的眼部图像 $\mathbf{I}_{\text{crop}}$，直接通过骨干网络 $f_\theta$ 提取嵌入向量 $\mathbf{e} = f_\theta(\mathbf{I}_{\text{crop}})$。
- **训练目标**：采用标准ArcFace损失进行度量学习，在角度空间施加分类边际，增强嵌入的类间可分性与类内紧凑性。

由于NormFree的创新本质是**去除归一化模块**而非引入新的数学构造，本节无新增公式需要推导。该设计的有效性完全由实验验证支撑：消融实验表明，即使换用更先进的自适应归一化技术，NormKeep性能仅微幅提升；而将骨干网络缩小至IR-18时NormFree仍保持优势，证明归一化是通用瓶颈而非实现细节（Table 7, Sec 5.6）。



## 实验与关键发现

### 实验设置概览

论文构建了八个评估协议，系统考察光照、注视、遮挡、瞳孔扩张、反射和模糊六类退化因素对虹膜识别的影响。其中四个为**综合挑战协议**（Immer-Control、Immer-Fix、Immer-Select、Immer-Any），难度递增，同时包含多种退化因素的组合；另四个为**孤立挑战协议**（Immer-Occlusion、Immer-Dilation、Immer-Light、Immer-Gaze），分别隔离单一退化因素以精确归因。各协议所研究的因素矩阵详见 Table 2。

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/007_Table_2.jpg]]
*Table 2: Summary of evaluation protocols by the factors studied. “I, G, O, D, R, B” denote illumination, gaze, occlusion, dilation, reflection, and blur. Symbols “•, ◦, △” indicate explicitly, partially, and implicitly included factors, and “×” indicates exclusion*

所有方法均采用 ResNet IR-50 作为骨干网络，以 ArcFace 损失进行训练。NormFree 仅需检测器提供的边界框（扩展 1.2 倍后裁剪），而对比基线 NormKeep 则沿用完整的归一化流水线（分割→参数化→极坐标展开）。评估指标包括验证场景下的 FRR@FAR（1e-1、1e-3、1e-5）和识别场景下的 Rank-1 准确率。

### 跨场景泛化崩溃：SOTA 在沉浸式条件下的失效

Table 3 和 Figure 2 揭示了核心瓶颈：现有 SOTA 方法在传统受控数据集 CASIA-Iris-V4 上表现优异，但在 ImmerIris 的 Immer-Any 协议上性能急剧崩溃。以 FRR@FAR 1e-5 为例，**Gabor**（Daugman, Elsevier 2009）从 CASIA-T 上的极低错误率飙升至 85.47%，**Ordinal Measures**（Sun and Tan, TPAMI 2008）升至 88.48%，基于深度学习的 **Maxout** 系列（Wei et al., TIFS 2022）更是普遍超过 90%。这一崩溃的根本原因在于：沉浸式场景中的离轴拍摄、注视变化和各类退化导致归一化阶段产生的展开纹理严重扭曲，使得后续特征提取无法获得可靠输入。

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/002_Figure_2.jpg]]
*Figure 2: Performance of SOTAs and our normalization-free approach on CASIA-Iris-V4 [7] and 4 increasingly challenging ImmerIris protocols. Lower FRR is better. SOTAs perform well on the traditional setup yet drop sharply under immersive conditions, whereas our approach consistently outperforms them*

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/009_Table_3.jpg]]
*Table 3: Verification FRR@FAR (↓) of SOTAs trained on CASIA-T and tested on (a) CASIA-T and (b) Immer-Any. Results on left and right eyes are averaged due to space constraints*

### 主要结果：NormFree 在综合挑战协议上的优势

Table 4 汇总了所有方法在四个综合挑战协议上的验证性能。NormFree 在绝大多数设置下取得最优或次优结果，且优势随协议难度增加而扩大：

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/010_Table_4.jpg]]
*Table 4: Verification FRR@FAR (↓) of SOTAs and the proposed method on 4 evaluation protocols of increasing difficulty, capturing multiple challenges in combination. Bold and underline indicate the best and second-best results, respectively; the same applies hereafter. Note that the dual-eye testing on Immer-Select is oversimplified hence omitted, as discussed in Sec. 3.5*

- **Immer-Control**（最简协议）：NormFree 左眼 FRR@FAR 1e-5 为 5.50%，右眼 4.93%，双眼 5.17%，与归一化基线 NormKeep 及 SOTA 方法处于可比或更优水平。
- **Immer-Fix**：NormFree 左眼 FRR@FAR 1e-5 降至 15.22%，而多数 SOTA 方法已超过 20%。
- **Immer-Any**（最具挑战性协议）：NormFree 左眼 FRR@FAR 1e-5 为 52.04%，远低于 Gabor（85.47%）、OM（88.48%）和 Maxout 系列（>90%）。这一近 30 个百分点的差距直接验证了去除归一化的因果效应——深度网络从包含上下文线索的原始裁剪区域中学习到的表征，远比经过脆弱归一化处理的纹理更鲁棒。

Figure 2 以可视化形式呈现了这一趋势：NormFree 在 CASIA-Iris-V4 上性能与 SOTA 持平，但随着协议从 Control 到 Any 逐步增难，其性能下降曲线明显缓于所有归一化方法。

### 孤立挑战协议：退化因素的归因分析

Table 5 进一步在四个孤立挑战协议上分解性能。NormFree 在所有协议上均保持优势，但不同退化因素的影响程度存在显著差异：

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/011_Table_5.jpg]]
*Table 5: Verification FRR@FAR (↓) of SOTAs and the proposed method on 4 evaluation protocols of isolated challenges*

- **Immer-Gaze** 是造成性能下降的最主要因素。NormFree 左眼 FRR@FAR 1e-3 为 16.40%，虽优于其他方法，但相较 Control 协议仍有大幅退化。消融分析（Sec 5.6）指出，注视变化平均导致约 36.99% 的性能退化，是当前方法面临的最大挑战。
- **Immer-Occlusion** 和 **Immer-Dilation** 场景下，NormFree 的优势尤为突出：左眼 FRR@FAR 1e-5 分别为 8.23% 和 4.53%，表明去除归一化后网络能更好地利用眼周上下文信息补偿遮挡和瞳孔形变带来的纹理损失。
- **Immer-Light** 场景下所有方法表现相对接近，说明光照变化对归一化流程的破坏性相对有限。

### 识别场景：Rank-1 准确率

Table 6 报告了各协议下的识别性能。在 Immer-Any 协议上，NormFree 的 Rank-1 准确率达到 94.39%，较 SOTA 中最高水平（约 90%）提升数个点。在 Immer-Control 和 Immer-Fix 上，NormFree 同样保持领先或与最优方法持平，进一步验证了免归一化范式在封闭集识别任务中的有效性。

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/012_Table_6.jpg]]
*Table 6: Identification rank-1 accuracy (↑) of SOTAs and the proposed method on different evaluation protocols*

### 消融实验：验证因果机制

Table 7 通过两组消融实验排除了混淆因素，强化了“归一化是瓶颈”这一因果推断：

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/013_Table_7.jpg]]
*Table 7: Verification FRR@FAR (↓) of NormKeep and NormFree under alternative (Alt.) model scale and iris normalization technique, averaged over left and right eyes on Immer-Any*

1. **模型规模敏感性**：将骨干网络从 IR-50 缩小至 IR-18 后，NormFree 在 Immer-Any 上仍优于 NormKeep，且超越多数 SOTA。这表明 NormFree 的收益并非依赖大模型容量，而是源于范式层面的结构性改进。
2. **归一化实现替换**：为 NormKeep 换用更先进的自适应归一化技术后，其性能仅获微幅提升，仍远低于 NormFree。这排除了“归一化效果差是具体实现问题”的替代解释，确证归一化阶段本身——而非其实现细节——是沉浸式场景下的通用瓶颈。

### 失败模式与局限

尽管 NormFree 展现了显著优势，其性能在 Immer-Any 协议上仍有 52.04% 的 FRR（FAR=1e-5），表明沉浸式虹膜识别远未解决。主要失败模式包括：

- **注视变化**：如前述，gaze variation 是最大的单一退化源，当前 NormFree 未对其做专门建模，导致大角度离轴注视时特征判别力急剧下降。
- **检测器依赖**：NormFree 仍依赖预训练检测器提供边界框。在极度遮挡或严重模糊的场景下，检测失败将直接导致识别失败——尽管论文主张该检测器比完整归一化流程更鲁棒，但这一依赖关系仍是潜在的单点故障。
- **群体泛化性**：ImmerIris 受试者主要为 20-40 岁亚洲成年人，种族和年龄覆盖有限，跨群体泛化性能尚未验证。

### 关键图表指引

- **Figure 2**：一图胜千言——SOTA 在传统数据集上的优异表现与在 ImmerIris 上的崩溃形成鲜明对比，NormFree 的鲁棒性一目了然。
- **Table 4**：核心结果表，涵盖所有方法在四个综合协议上的完整验证性能。
- **Table 5**：孤立挑战归因表，用于定位各退化因素的独立影响。
- **Table 7**：消融实验表，验证“归一化是瓶颈”的因果推断并排除混淆因素。

### 补充图表

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/003_Table_1.jpg]]
*Table 1: Comparison of existing iris recognition datasets and ImmerIris in terms of acquisition setup and scale*

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/004_Figure_3.jpg]]
*Figure 3: Data acquisition setup. (a) Screen interface of the VR headset, where red squares numbered 1-9 mark gaze points for sequential fixation. Live camera previews assist proper wearing. A full-screen white panel gradually increases in brightness to simulate illumination changes. (b) Actual scene of data acquisition*

![[assets/figures/papers/paper_list_l2098_https_arxiv_org_abs_2510_10113/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of application scenarios. Each sample group is from the same person. (a) Traditional iris recognition acquires on-axis and controlled images with dedicated devices, with samples being highly invariant. (b) Immersive iris recognition collects images using consumer HMDs, yielding off-axis and unconstrained samples that exhibit distortion, variation, and degradation*



## 定位与知识库关联

### 1. 范式断裂：从“分割-归一化-匹配”到“免归一化端到端学习”

传统虹膜识别方法几乎全部遵循 **Daugman 两阶段范式**（Daugman, Elsevier 2009）：首先对眼部图像进行虹膜区域分割与轮廓参数化，然后通过极坐标变换将环形虹膜展开为矩形归一化纹理，最后在归一化纹理上进行特征提取与匹配。这一范式的核心假设是归一化能够消除瞳孔缩放、旋转和尺度变化等几何差异，使后续的特征提取聚焦于纹理信息。在受控的正面采集条件下（如 CASIA-Iris-V4），该假设成立，SOTA 方法的 FRR 可低至 1% 以下。

然而，**ImmerIris 论文的核心发现是：这一假设在沉浸式离轴无约束场景下系统性崩溃**。当 SOTA 方法（包括基于 Gabor 滤波的经典方法、基于序数测度的 **Ordinal Measures**（Sun and Tan, TPAMI 2008）、基于不确定因素学习的 **Maxout/UE-UGCL** 系列（Wei et al., TIFS 2022）、基于上下文测度的 **CM**（Wei et al., TIFS 2022）、复数网络 **ComplexIrisNet**（Nguyen et al., TPAMI 2022）以及深度 Fisher 网络 **DFFN**（Zhang et al., TIFS 2018））从 CASIA-T 直接迁移至 Immer-Any 协议时，FRR@FAR=1e-5 从低于 5% 急剧攀升至 85% 以上（Table 3, Figure 2），表明归一化阶段产生的扭曲纹理已成为性能的致命瓶颈。

**NormFree 提出的范式切换**具有明确的因果逻辑：既然归一化是瓶颈，就将其从流程中完全移除。具体而言，NormFree 仅通过预训练的虹膜检测器获取可靠边界框，将其扩展 1.2 倍以保留上下文信息，裁剪后直接送入 ResNet IR-50 主干网络，以 ArcFace 损失进行端到端训练（Figure 6）。这一设计背后的核心洞察是：**深度卷积网络本身具备足够的非线性表达能力，能够从包含上下文线索的原始裁剪图像中学习鲁棒的身份表征，从而替代传统精细但脆弱的归一化预处理**。

### 2. 与基线方法的本质差异

NormFree 与上述 SOTA 方法的差异不仅是性能层面的，更是**预处理哲学**的根本不同：

| 维度 | 传统 SOTA（NormKeep 范式） | NormFree |
|------|--------------------------|----------|
| 预处理流程 | 分割→轮廓参数化→极坐标变换→归一化矩形纹理 | 检测边界框→1.2×扩展裁剪→直接输入 |
| 特征提取输入 | 归一化后的矩形纹理（丢失空间上下文） | 包含眼周上下文的原始裁剪图像 |
| 对离轴/形变的鲁棒性 | 低：归一化参数估计易失效，产生扭曲纹理 | 高：网络直接从原始像素学习不变表征 |
| 计算复杂度 | 高：需精确分割与归一化计算 | 低：仅需边界框检测 |

消融实验（Table 7, Sec 5.6）进一步验证了这一差异的本质性：
- **模型规模不敏感**：将骨干网络从 IR-50 缩小至 IR-18 后，NormFree 依然优于 NormKeep 并超越多数 SOTA，说明收益并非来自更大的模型容量。
- **归一化实现细节非关键**：即使为 NormKeep 换用更先进的自适应归一化技术，其性能仅微幅提升，证明归一化阶段本身——而非其具体实现——是通用瓶颈。

### 3. 适用边界与已知局限

**适用场景**：
- 离轴、无约束的沉浸式虹膜识别（VR/AR 头显）
- 存在注视变化、瞳孔扩张、光照变化、部分遮挡等复合退化的场景
- 对预处理鲁棒性要求高于精细纹理保真度的应用

**已知局限**（来自 verified_analysis 与论文讨论）：
1. **注视变化是最大退化源**：消融分析（Sec 5.4）表明，注视变化（gaze variation）平均导致约 36.99% 的性能退化，是当前 NormFree 尚未专门优化的最大挑战。
2. **仍依赖预训练检测器**：NormFree 并非完全端到端——若虹膜检测器在极度遮挡或模糊下失败，系统性能会下降；但论文主张检测器比完整归一化流程更鲁棒。
3. **数据集覆盖有限**：ImmerIris 受试者主要为 20-40 岁亚洲成年人，性别比例近平衡，但缺乏对其他种族和年龄组的代表性，跨群体泛化性待验证。
4. **未评估跨设备/跨数据集泛化**：评估协议系统设计了多种挑战模式，但未包含其他 HMD 设备或已有数据集（如 CASIA 系列）的跨域评测。

### 4. 开放问题与未来方向

1. **注视变化的显式建模**：能否设计针对注视方向的条件归一化、形变场预测或数据增强机制，以进一步降低约 37% 的注视相关退化？
2. **几何先验的融入**：在完全免归一化的前提下，是否可以将虹膜的环形几何结构或纹理分布先验融入网络设计（如引入等变卷积或显式形变建模），在不牺牲鲁棒性的前提下提升判别力？
3. **眼周信息的深度融合**：NormFree 的 1.2× 扩展裁剪已隐式引入眼周上下文，但如何高效、自适应地融合眼周与虹膜纹理（尤其在严重模糊或遮挡场景下）仍是一个开放问题。
4. **跨模态与跨设备泛化**：该范式在可见光 vs 近红外、不同 HMD 硬件平台下是否依然有效，需要进一步验证。
5. **与新兴基础模型的结合**：大视觉模型（如 DINOv2、CLIP 视觉编码器）是否能在免归一化范式下提供更强的泛化表征，值得探索。

### 5. 在知识库中的定位

NormFree 在虹膜识别领域的方法谱系中标志着一次**预处理范式的断裂**：从“精细几何归一化+浅层特征匹配”转向“最小预处理+深度表征学习”。它与以下方向形成对话关系：
- **生物特征识别的端到端化趋势**：与人脸识别中从“对齐-特征”到直接端到端学习的演进类似，NormFree 将这一思路系统性地引入虹膜识别，并提供了大规模离轴数据集作为验证基础。
- **鲁棒视觉识别的上下文利用**：1.2× 扩展裁剪的设计与目标检测中“上下文区域提升小目标检测”的思路相通，暗示适度的空间上下文可补偿局部纹理的退化。
- **沉浸式计算的身份认证需求**：ImmerIris 数据集和 NormFree 方法共同填补了 VR/AR 场景下虹膜识别研究的空白，为后续工作提供了基准和基线。



## 原文 PDF

![[paperPDFs/CVPR_2026/ImmerIris_A_Large_Scale_Dataset_and_Benchmark_for_Off_Axis_and_Unconstrained_Iris_Recognition_in_Immersive_Applications.pdf]]
