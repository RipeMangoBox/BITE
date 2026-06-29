---
title: "ICARUS: A Specialized Architecture for Neural Radiance Fields Rendering"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/ICARUS_A_Specialized_Architecture_for_Neural_Radiance_Fields_Rendering.pdf
project_link: null
code_link: null
aliases:
- ISA
- ICARUS
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用专用的全光核心（PLCore）在单核内完成完整的NeRF流水线（位置编码、MLP推理、体渲染），避免中间数据离开芯片；同时将MLP的矩阵向量乘法转为近似可重构多常数乘法（RMCM），通过共享公共子表达式和移位加法降低硬件复杂度。
primary_logic: NeRF的整个渲染流程可完全在专用加速器上完成，无需片外存储中间数据；MLP的乘加操作可利用神经网络的容错性，通过近似移位加减和公共子表达式共享来实现，从而大幅降低计算和功耗。
claims:
- 单PLCore功耗282.8 mW，面积16.5 mm²，能效0.105 μJ/sample，显著优于GPU和TPU的功耗与面积（Table 1）。
- ICARUS在大多数场景下PSNR与GPU差距小于1 dB，且近似RMCM的PSNR可达48.24（Fig. 12, Fig. 8）。
- PLCore设计消除了NeRF流水线中所有中间数据的片外交互，直接输入位置方向输出像素颜色（Section 1, Fig. 3）。
- NeRF rendering (800×800, 192 samples/ray) 上 单帧渲染时间 = 45.75 s
---

# ICARUS: A Specialized Architecture for Neural Radiance Fields Rendering

> [!tip] 核心洞察
> NeRF的整个渲染流程可完全在专用加速器上完成，无需片外存储中间数据；MLP的乘加操作可利用神经网络的容错性，通过近似移位加减和公共子表达式共享来实现，从而大幅降低计算和功耗。

| 字段 | 内容 |
|------|------|
| 中文题名 | ICARUS：面向神经辐射场渲染的专用架构 |
| 英文题名 | ICARUS: A Specialized Architecture for Neural Radiance Fields Rendering |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2203.01414) |
| Topic | #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ICARUS specialized accelerator |
| Dataset | NeRF rendering, NeRF合成场景 |

> [!tip] 效果简介
> - NeRF rendering (800×800, 192 samples/ray) 上，单帧渲染时间 45.75 s vs 27.74 s (TF NeRF, 1x V100) (慢 18.01 s)；功耗 282.8 mW vs 300 W (TDP, 1x V100) (降低约 1000 倍)；芯片面积 16.5 mm² vs 815 mm² (1x V100) (缩小约 49 倍)。
> - NeRF合成场景 上，PSNR (与GPU对比) 多数场景差距<1 dB，最高2 dB (chair) vs GPU (浮点) (轻微质量下降)。

## 概要

神经辐射场（NeRF）渲染需要对每条射线执行数百次MLP查询，通用GPU架构在此过程中产生大量片外数据搬运和中间结果暂存，导致渲染速度受限、功耗居高不下。本文提出**ICARUS**，一种面向NeRF渲染的专用加速器架构。其核心设计是**全光核心（PLCore）**，将位置编码、MLP推理与体渲染完整流水线集成于单一核心内，消除所有中间数据的片外交互。同时，将MLP的矩阵向量乘法转化为近似可重构多常数乘法（RMCM），利用公共子表达式共享和移位加法替代标准乘累加阵列，大幅降低硬件复杂度与功耗。在40 nm工艺、400 MHz下，单PLCore面积16.5 mm²，功耗仅282.8 mW，能效达0.105 μJ/sample；与NVIDIA V100 GPU相比，面积缩小约49倍，功耗降低约三个数量级。渲染质量方面，多数场景PSNR与GPU浮点版本差距不足1 dB，近似RMCM引入的视觉差异可忽略。ICARUS以专用架构在极低功耗预算下实现了与通用GPU可比的渲染质量，为NeRF在边缘和嵌入式设备上的部署提供了可行路径。

## 核心方法与创新机理

### 问题瓶颈与设计哲学

NeRF渲染的核心计算瓶颈在于：每生成一个像素颜色，需要对沿射线的数百个采样点执行完整的MLP前向推理（位置编码→MLP→体渲染），而通用GPU架构在执行这一流水线时，必须反复通过片外内存交换中间数据。具体而言，在GPU上，位置编码在特殊函数单元（SFU）中执行，MLP映射到SIMD核心阵列，体渲染又在另一计算单元完成，每一步的中间结果（编码后的高维特征、MLP输出的颜色与密度、累积透射率等）都需要写入片外DRAM再读出，造成巨大的数据搬运开销和功耗（Fig. 2a）。NPU实现同样存在类似问题：位置编码和体渲染在CPU端完成，仅MLP在PE阵列上加速，中间数据仍需片外交互（Fig. 2b）。

ICARUS的设计哲学直接针对这一瓶颈，提出两条核心原则（Section 3.2）：

1. **全流水线片上封闭**：将NeRF的完整渲染流水线（位置编码→MLP推理→体渲染）封装在单个专用全光核心（PLCore）内，消除所有中间数据的片外传输和临时存储。
2. **定点量化替代浮点**：采用训练后定点数量化，将GPU上预训练的NeRF模型转换为定点版本部署到ICARUS上，以降低硬件复杂度和功耗。

### Changed Slots：相对于GPU/NPU基线的关键变更

ICARUS相对于GPU和NPU基线，在三个关键维度上进行了根本性改变：

**Slot 1：中间数据片外交互（有→无）**

基线GPU/NPU方案中，NeRF流水线的各阶段中间数据必须经过片外内存交换。ICARUS的PLCore设计将PEU、MLP Engine和VRU三个计算模块紧密耦合在单个核心内，输入仅为采样点的位置和方向坐标，输出即为该采样点对像素颜色的贡献，整个过程中没有任何中间数据离开芯片（Abstract, Fig. 3）。这一变更从根本上消除了NeRF渲染的内存带宽瓶颈。

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2203_01414/figures/003_Figure_3.jpg]]
*Figure 3: Overall architecture of the proposed ICARUS. The main computation components in ICARUS is PLCore. For NeRF rendering, a batch of sample points are processed by the PLCore, where the whole NeRF pipeline for a ray is completed inside the PLcore, i.e., a PLCore takes in positions & directions and renders the corresponding pixel colors without any intermediate data going off-chip for temporary storage and exchange*

**Slot 2：MLP矩阵向量乘法的实现方式（标准MAC阵列→近似RMCM）**

基线方案使用标准的乘累加（MAC）单元执行矩阵向量乘法。ICARUS将其转化为可重构多常数乘法（Reconfigurable Multiple Constant Multiplication, RMCM），并进一步引入近似RMCM。其核心思想是：MLP权重在推理时是固定的常数矩阵，因此矩阵向量乘法可以重新表述为输入向量元素与多组常数的乘法。RMCM通过预计算公共子表达式（如3x = 1x << 1 + 1x），在不同乘法器之间共享这些移位加法的中间结果，从而大幅减少硬件乘法器数量。近似RMCM进一步省略了约一半的公共子表达式（9x, 11x, 13x, 15x），用其最近邻值近似替代（Fig. 7b），在几乎不损失渲染质量的前提下（PSNR 48.24, Fig. 8），将硬件复杂度降低约1/3（Section 4.3）。

**Slot 3：数值表示（浮点→定点）**

GPU基线使用浮点数进行计算，ICARUS采用定点数表示。这一变更使得硬件中的乘法器和加法器可以大幅简化，但代价是引入量化误差。论文采用训练后量化策略，将GPU上预训练的浮点NeRF模型直接转换为定点版本部署到ICARUS，未使用量化感知训练（Section 3.2, Section 6）。

### 系统架构与模块顺序

ICARUS的整体架构（Fig. 3）以PLCore为核心计算单元。一个PLCore内部包含三个顺序执行的计算模块和片上SRAM存储：

1. **位置编码单元（PEU）**：接收采样点的3D位置坐标和2D方向坐标，通过傅里叶特征映射将其编码到高维空间。
2. **MLP引擎（MLP Engine）**：对编码后的高维特征执行多层感知机推理，输出颜色值和体密度值。
3. **体渲染单元（VRU）**：对沿射线的采样点颜色和密度执行体渲染积分，生成最终像素颜色。

此外，片上SRAM用于存储MLP权重、输入数据和模块间传递的中间结果，片上网络负责在CPU、DRAM和PLCore之间分发输入坐标并收集渲染结果。

### 关键模块的因果机制

#### 位置编码单元（PEU）

PEU的数学基础是傅里叶特征映射：

$$\phi ( x ; A ) = [ \cos A ^ { T } x , \sin A ^ { T } x ]$$

其中 $x$ 是原始输入坐标（位置或方向），$A$ 是频率矩阵。原始NeRF使用固定的频率模式（$2^0, 2^1, ..., 2^{L-1}$ 对位置编码，$L=10$；对方向编码 $L=4$）。ICARUS的PEU被设计为通用可配置单元，支持三种频率模式（Fig. 4a）：固定频率（NeRF）、各向同性随机傅里叶特征（用于隐式几何编码）和各向异性高斯傅里叶特征（用于神经表面光场SLF）。PEU内部通过矩阵乘法计算 $A^T x$，再通过查找表或CORDIC单元计算正弦和余弦值（Fig. 4b, Section 4.2）。

PEU的输出直接流入MLP引擎，无需经过片外存储，这是实现全流水线片上封闭的第一环。

#### MLP引擎与近似RMCM

MLP引擎的核心创新在于将矩阵向量乘法（MVM）转化为近似RMCM操作。标准MLP层的计算为：

$$\pmb { y } = f ( W \pmb { x } + \pmb { b } )$$

其中 $W$ 是权重矩阵，$\pmb{x}$ 是输入向量，$\pmb{b}$ 是偏置，$f$ 是激活函数（ReLU）。

在推理阶段，$W$ 是固定常数矩阵。RMCM的基本原理是：对于输入向量元素 $x$ 与常数 $w$ 的乘法，可以将 $w$ 分解为移位和加法的组合。例如，$3x$ 可以实现为 $(x \ll 1) + x$。RMCM预计算一组公共子表达式（如 $1x, 3x, 5x, 7x, 9x, 11x, 13x, 15x$），然后在所有权重乘法中共享这些中间结果。近似RMCM进一步省略了后半部分子表达式（$9x, 11x, 13x, 15x$），用最近邻值（$7x$ 或 $1x \ll 3$）近似替代，从而将公共子表达式数量减半（Fig. 7b）。

MLP引擎的计算流程（Fig. 5）组织为多个输出网络块（MONB, Fig. 6）和一个单输出网络块（SONB, Fig. 9）。MONB负责计算MLP隐藏层的多输出神经元，每个MONB包含RMCM块、加法器树、偏置加法和ReLU激活。SONB用于计算输出层（颜色和密度），结构类似但不含ReLU激活。

**因果链**：PEU输出的高维特征向量进入MLP引擎 → MONB中的RMCM块将输入元素与权重常数进行移位加法运算 → 公共子表达式在多个乘法器间共享 → 加法器树求和 → 加偏置 → ReLU激活 → 输出传递至下一层或VRU。近似RMCM引入的误差被神经网络的容错性所吸收，实验表明PSNR仅从浮点参考值的约49 dB降至48.24 dB，无视觉差异（Fig. 8）。

#### 体渲染单元（VRU）

VRU实现简化后的体渲染方程：

$$C ( r ) = \sum _ { i = 1 } ^ { N } ( T _ { i } - T _ { i + 1 } ) c _ { i } , \quad T _ { i + 1 } = T _ { i } \cdot \exp ( x _ { i } )$$

其中 $C(r)$ 是射线 $r$ 的像素颜色，$N$ 是沿射线的采样点数，$c_i$ 和 $\sigma_i$ 分别是第 $i$ 个采样点的颜色和体密度（$x_i = -\sigma_i \delta_i$，$\delta_i$ 为采样步长），$T_i$ 是累积透射率。

VRU的硬件结构（Fig. 10）包含指数函数单元（通过查找表或分段线性近似实现）、乘法器和累加器。MLP引擎输出的颜色 $c_i$ 和密度相关值 $x_i$ 直接送入VRU，VRU顺序计算每个采样点的透射率衰减和颜色贡献，累加得到最终像素颜色。

**因果链**：MLP引擎输出的 $(c_i, \sigma_i)$ 直接流入VRU → VRU计算 $x_i = -\sigma_i \delta_i$ → 指数单元计算 $\exp(x_i)$ → 更新累积透射率 $T_{i+1} = T_i \cdot \exp(x_i)$ → 累加颜色贡献 $(T_i - T_{i+1}) c_i$ → 输出像素颜色。VRU作为流水线的最后一级，同样在PLCore内部完成，无需片外存储访问（Section 4.4）。

### 训练/推理路径

ICARUS的部署流程为离线训练→量化转换→硬件推理：

1. **离线训练**：在GPU上使用标准NeRF训练流程（Mildenhall et al., ECCV 2020）获得浮点权重。
2. **训练后量化**：将浮点权重和激活值转换为定点表示，确定整数位宽和小数位宽（Section 6）。
3. **权重部署**：量化后的权重加载到PLCore的片上SRAM中。
4. **推理**：对于每条射线，采样点坐标依次进入PEU→MLP Engine→VRU流水线，在PLCore内部完成所有计算，输出像素颜色。多条射线可批量处理以利用流水线并行。

### 关键公式与变量含义总结

| 公式 | 含义 | 所在模块 |
|------|------|----------|
| $F_{NeRF}: (p, d) \to (c, \sigma)$ | NeRF的全光函数映射 | 系统整体 |
| $\phi(x;A) = [\cos A^T x, \sin A^T x]$ | 傅里叶特征位置编码 | PEU |
| $\pmb{y} = f(W\pmb{x} + \pmb{b})$ | MLP层前向计算 | MLP Engine |
| $3x = (x \ll 1) + x$ | RMCM移位加法示例 | MLP Engine (RMCM) |
| $C(r) = \sum_{i=1}^N (T_i - T_{i+1}) c_i$ | 简化体渲染积分 | VRU |
| $T_{i+1} = T_i \cdot \exp(x_i), x_i = -\sigma_i \delta_i$ | 累积透射率更新 | VRU |

### 方法边界与未验证假设

ICARUS的方法设计存在以下边界条件：

1. **纯MLP架构依赖**：ICARUS严格遵循原始NeRF的纯MLP设计，难以直接适配基于哈希编码（如Instant-NGP）、八叉树或三平面等混合表示的NeRF变体。
2. **训练后量化的局限**：未使用量化感知训练，量化位宽的选择缺乏场景自适应性，部分场景PSNR损失可达2 dB（Fig. 12, chair场景）。
3. **定点精度限制**：定点数表示缺乏动态精度支持，可能限制模型表达能力。
4. **单核性能不足**：单PLCore渲染800×800分辨率、192采样点/射线的图像需45.75秒，远未达到实时，多核扩展方案及其带宽瓶颈尚未验证。

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2203_01414/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of mapping NeRF to (a) GPU (b) NPU and (c) ICARUS. For GPU-based NeRF implementation, positional encoding and volume rendering are executed in the SFU, and MLP is mapped to SIMD core arrays. Intermediate data is exchanged using off-chip memory. For NPU-based NeRF implementation, positional encoding and volume rendering are execuated in CPU and MLP is mapped to PE arrays. Intermediate data is also exchanged using off-chip memory. ICARUS executes the complete NeRF pipeline using dedicated plenoptic cores (PLCore) consisting of a PEU, an MLP engine, and a VRU*

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2203_01414/figures/001_Figure_1.jpg]]
*Figure 1: We demonstrate a specialized hardware architecture for NeRF-based rendering applications. (a) Our hardware design involves operations in NeRF-based rendering. (b) We validate our architecture using an FPGA platform. (c) Potential applications that can benefit from our architecture*

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2203_01414/figures/011_Figure_11.jpg]]
*Figure 11: (a) Block diagram and (b) system setup of the FPGA-based prototype system*

## 实验与关键发现

### 评估平台与对比基线

ICARUS的原型系统基于FPGA实现（Fig. 11），工作频率400 MHz，单PLCore面积16.5 mm²，功耗282.8 mW。对比基线包括：运行TF NeRF/JaxNeRF的NVIDIA V100 GPU（12nm工艺，815 mm²，TDP 300 W）和TPUv2（16nm工艺）。需注意，GPU/TPU采用更先进制程且TDP为热设计功耗而非实际运行功耗，ICARUS则基于较老的40nm工艺，直接对比存在工艺代差。

### 核心性能指标

Table 1汇总了GPU、TPU与ICARUS在800×800分辨率、每射线192采样点下的NeRF渲染性能对比：

| 指标 | TF NeRF (1×V100) | JaxNeRF (1×V100) | JaxNeRF (8×V100) | JaxNeRF (TPUv2) | ICARUS (1×PLCore) |
|------|------------------|-------------------|-------------------|-----------------|-------------------|
| 单帧时间 | 27.74 s | 57.56 s | 7.56 s | 8.26 s | 45.75 s |
| 功耗 | 300 W (TDP) | 300 W (TDP) | 2400 W (TDP) | 未报告 | 282.8 mW |
| 芯片面积 | 815 mm² | 815 mm² | 6520 mm² | <331 mm² | 16.5 mm² |
| 能效 | 未报告 | 未报告 | 未报告 | 未报告 | **0.105 μJ/sample** |

**关键发现**：
- **功耗优势显著**：单PLCore功耗仅282.8 mW，约为V100 TDP的1/1000。即使考虑工艺缩放（40nm→12nm约可降低3-5倍功耗），ICARUS的能效优势依然显著。
- **面积效率突出**：16.5 mm²的PLCore面积约为V100的1/49，且该面积包含了完整的NeRF流水线（PEU+MLP引擎+VRU+片上SRAM）。
- **速度并非优势**：单PLCore渲染一帧需45.75秒，慢于单V100的27.74秒，远慢于8×V100的7.56秒。ICARUS的设计目标是能效而非绝对速度，实时渲染需多核系统。
- **能效唯一报告**：0.105 μJ/sample是Table 1中唯一报告的能效值，GPU/TPU基线均未提供该指标，表明能效是ICARUS的核心差异化优势。

### 渲染质量对比

Fig. 12展示了GPU（浮点）与ICARUS（定点量化+近似RMCM）在NeRF合成场景上的PSNR对比。**多数场景PSNR差距小于1 dB**，但chair场景差距可达约2 dB。这表明训练后量化策略在某些几何复杂场景下存在质量瓶颈，量化感知训练有望缩小这一差距。

### 关键消融实验

**近似RMCM的有效性验证**（Section 4.3, Fig. 8）：将MLP矩阵向量乘法从标准MAC阵列转换为RMCM（可重构多常数乘法），并进一步采用近似RMCM——省略一半预计算公共子表达式（9x, 11x, 13x, 15x），用最近邻值近似替代。结果显示：
- 硬件复杂度减少约1/3（相比完整RMCM）
- 渲染PSNR达48.24，与原浮点NeRF无视觉差异（Fig. 8对比）
- 证明神经网络对乘法近似具有较强容错性，该特性是ICARUS硬件简化的理论基石

**定点量化的质量代价**（Section 5.1, Fig. 12）：ICARUS采用训练后定点量化，未使用量化感知训练。多数场景PSNR损失<1 dB，但chair等场景损失可达2 dB。这揭示了当前量化策略的边界：对于密度和颜色变化剧烈的区域，定点表示精度不足。

**VRU专用模块的必要性**（Section 4.4）：体渲染单元在片上完成指数运算、透射率累积和颜色积分，避免了传统GPU/NPU架构中体渲染中间结果需写回片外存储再读回的开销。这是ICARUS实现“零片外中间数据交换”设计目标的关键模块。

### 失败模式与适用边界

**单核性能不足以实时渲染**：45.75秒/帧的速度无法满足交互式应用。论文提出多核扩展方案，但多核间的数据分发带宽、权重存储共享、片上网络拥塞等问题尚未验证，这是ICARUS走向实用的核心瓶颈。

**训练后量化的场景依赖性**：定点量化在不同场景的质量损失不一致（<1 dB至2 dB），缺乏动态精度调节机制。对于高精度要求的应用（如医学成像），固定位宽可能不足。

**架构专用性限制泛化能力**：ICARUS专为纯MLP架构的NeRF设计，其PLCore流水线（PEU→MLP→VRU）难以直接适配基于哈希网格（Instant-NGP）、八叉树或三平面表示的NeRF变体。Fig. 13展示了向神经SDF和神经SLF的扩展尝试，但SLF渲染仍需结合网格光栅化，与完整图形管线的集成仍存在挑战。

**工艺与频率劣势**：原型基于40nm工艺、400 MHz时钟，相比GPU的12nm/1.5 GHz存在显著代差。更先进工艺和电路优化有望进一步提升能效和速度，但论文未提供工艺缩放的预估数据。

**对比公平性局限**：GPU功耗使用TDP而非实际运行功耗（实际NeRF渲染功耗通常低于TDP），且GPU包含大量通用计算单元（张量核、光栅单元等），面积对比可能高估ICARUS的相对优势。更公平的对比应使用GPU实际功耗和仅计算单元面积。

### 证据强度评估

- **高置信度**（0.95）：单PLCore面积/功耗数据、零片外中间数据交换的设计目标达成
- **中高置信度**（0.9）：近似RMCM的PSNR结果、定点量化质量损失范围
- **需手动验证**：多核系统的带宽瓶颈分析、与更新NeRF变体（Instant-NGP等）的适配可行性、工艺缩放后的性能预估

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2203_01414/figures/015_Table_1.jpg]]
*Table 1: Comparison of NeRF implementation on GPU, TPU and ICARUS*

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2203_01414/figures/012_Figure_12.jpg]]
*Figure 12: Comparison of NeRF rendering results using GPU and ICARUS. PSNRs are presented below each result*

## 定位与知识库关联

ICARUS 的核心定位是 **NeRF 渲染的专用硬件加速器**，其根本改变在于将 NeRF 的完整渲染流水线（位置编码→MLP 推理→体渲染）封闭在单个全光核心（PLCore）内部完成，消除了 GPU/NPU 架构中不可避免的片外中间数据搬运。这一设计选择直接切中了通用架构在 NeRF 任务上的核心瓶颈：大量 MLP 查询产生的中间数据（位置编码输出、各层激活值、体渲染中间累积量）需要在片外 DRAM 与计算单元之间反复交换，造成严重的功耗和带宽开销。

### 相对基线的本质差异

与 **GPU 上的 NeRF 实现**（Mildenhall et al., ECCV 2020; Deng et al., 2020）和 **TPU 上的 JaxNeRF**（Deng et al., 2020）相比，ICARUS 改变了以下关键 slot：

1. **中间数据片外交互**：GPU 和 NPU 均需将位置编码结果、MLP 各层输出、体渲染中间变量写入片外内存后再读回（Fig. 2），而 ICARUS 的 PLCore 从接收位置/方向到输出像素颜色，全程在片内完成（Abstract, Section 1）。这是架构层面的根本差异，而非简单的算力堆叠。其因果链条是：消除片外访存→大幅降低功耗→使边缘端 NeRF 渲染成为可能。

2. **MLP 计算实现方式**：GPU/NPU 使用标准浮点乘累加（MAC）阵列，ICARUS 则将矩阵向量乘法（MVM）转化为近似可重构多常数乘法（approximated RMCM），通过移位加法和公共子表达式共享替代乘法器（Section 4.3, Fig. 7）。这一变换利用了神经网络的容错性：省略半数预计算公共子表达式（9x, 11x, 13x, 15x），以最近邻近似替代，使硬件复杂度降低约 1/3，而渲染 PSNR 仍达 48.24，视觉上无差异（Fig. 8）。

3. **数值表示**：从浮点数转为定点数，通过训练后量化完成模型转换（Section 3.2, Section 6）。这与量化感知训练路线不同，简化了部署流程，但代价是部分场景 PSNR 下降可达 2 dB（Fig. 12）。

### 知识库挂载点

ICARUS 可挂载到以下知识节点：

- **领域专用架构（DSA）**：作为面向神经渲染的 DSA 实例，ICARUS 展示了“算法-架构协同设计”的范式——不是加速已有算法，而是根据算法特性重构计算流和数据流。与通用 DSA（如 TPU）不同，ICARUS 的专用性体现在流水线封闭和近似计算两个层面。

- **NeRF 加速**：在 NeRF 加速方法谱系中，ICARUS 属于硬件加速分支，与算法加速（如 Instant-NGP 的哈希编码、DONeRF 的采样优化）正交。其设计决策（纯 MLP 架构、固定频率位置编码）锚定于原始 NeRF（Mildenhall et al., ECCV 2020），因此天然不适合直接适配基于哈希或八叉树的变体——这是明确的适用边界。

- **近似计算**：RMCM 近似属于“计算精度换硬件效率”的经典 trade-off，但 ICARUS 的独特之处在于将近似操作嵌入到 MVM 的常数乘法结构中，而非简单的位宽缩减或剪枝。这为其他 MLP 密集型推理任务（如神经 SDF、神经 SLF，见 Fig. 13）提供了可迁移的近似策略模板。

- **边缘端体积渲染**：282.8 mW 的单核功耗和 16.5 mm² 的面积（Table 1）使 ICARUS 适用于 AR/VR 头显、移动设备等功耗受限场景，填补了 GPU 因功耗过高而无法覆盖的边缘端 NeRF 渲染空白。

### 适用边界与局限

1. **单核性能不足以实时**：单 PLCore 渲染 800×800 帧需 45.75 s，比 V100 GPU 慢约 65%（Table 1）。实时渲染需要多核系统，但多核扩展面临权重分发和中间数据汇聚的带宽瓶颈，论文未给出多核系统的验证数据。

2. **工艺代差影响公平比较**：ICARUS 采用 40 nm 工艺原型，而对比的 V100 为 12 nm、TPUv2 为 16 nm。功耗对比中 GPU 侧使用的是 TDP（300 W）而非实际运行功耗，面积和功耗优势可能被高估。

3. **算法灵活性受限**：定点数表示和固定 MLP 架构使其难以支持动态精度或混合精度推理；训练后量化而非量化感知训练限制了质量上限；纯 MLP 设计使其与基于哈希编码的 Instant-NGP 等最新算法存在架构鸿沟。

4. **与图形管线集成困难**：特别是在神经表面光场（SLF）渲染中，ICARUS 的 VRU 需要与网格光栅化结果结合（Fig. 13(b)），如何高效整合到完整图形管线仍是开放问题。

### 后续启发

ICARUS 的核心启发在于：对于 MLP 密集型的神经渲染任务，“流水线封闭 + 近似乘法”的组合策略可以在保持可接受渲染质量的前提下，将功耗降低三个数量级。后续工作可沿以下方向展开：

- **量化感知训练集成**：为不同场景自动搜索最低可行位宽，弥补训练后量化的质量损失。
- **多核内存架构设计**：解决多 PLCore 系统的权重广播和中间数据汇聚瓶颈，是实现实时渲染的关键。
- **算法适配层扩展**：设计可配置的编码单元和稀疏计算模块，使架构能兼容哈希编码、八叉树采样等新范式。
- **跨应用迁移**：将 PLCore 的流水线封闭思想迁移到医学体积渲染（CT/MRI）、神经辐射缓存等更广泛的体积渲染场景，验证其通用性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/ICARUS_A_Specialized_Architecture_for_Neural_Radiance_Fields_Rendering.pdf]]