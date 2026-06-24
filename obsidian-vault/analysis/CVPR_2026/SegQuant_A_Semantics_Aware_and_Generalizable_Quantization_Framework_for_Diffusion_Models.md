---
title: "SegQuant: A Semantics-Aware and Generalizable Quantization Framework for Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SegQuant_A_Semantics_Aware_and_Generalizable_Quantization_Framework_for_Diffusion_Models.pdf
code_link: "https://github.com/OptiSys-ZJU/segquant"
aliases:
- SegQuant
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过静态计算图拓扑模式匹配自动检测线性层中的语义分割边界，实施分段量化以消除不同语义通道间的量化干扰；采用双尺度分治正、负激活区域，在不引入定制硬件的前提下高保真保留极性细节。
primary_logic: SegQuant 的核心洞察在于：（1）线性层因 chunk/split/concat 等算子而产生的隐含语义分割，可由静态图分析自动检测并用于指导分段量化，无需人工指定架构规则；（2）SiLU/GELU 等激活的负值区域承载高频纹理与语义信息，通过对正负区域独立标度（DualScale）可在标准 GEMM 中高效保留这些细节，同时避免非对称量化的零点和广播开销。
claims:
- 在SD3.5上，SegLinear将DiT.11.norm1_context层的GPTQ量化Frobenius误差从3.02降至1.76，验证分段策略的有效性。
- 在MJHQ-30K上，SegQuant-G在W8A8设置下FID达到23.94，优于Smooth+（24.10）和PTQ4DiT（25.66），图像质量接近FP16（23.70）。
- "DualScale相比定制化的PTQ4ViT在AdaNorm层上提速约4倍（FLUX: 4201→1075 μs），同时保持同等精度，证明硬件友好的双路径设计在效率上的优势。"
- MJHQ-30K 上 FID = 23.94 (SegQuant-G)
---

# SegQuant: A Semantics-Aware and Generalizable Quantization Framework for Diffusion Models

> [!tip] 核心洞察
> SegQuant 的核心洞察在于：（1）线性层因 chunk/split/concat 等算子而产生的隐含语义分割，可由静态图分析自动检测并用于指导分段量化，无需人工指定架构规则；（2）SiLU/GELU 等激活的负值区域承载高频纹理与语义信息，通过对正负区域独立标度（DualScale）可在标准 GEMM 中高效保留这些细节，同时避免非对称量化的零点和广播开销。

| 字段 | 内容 |
|------|------|
| 中文题名 | SegQuant：面向扩散模型的语义感知与通用量化框架 |
| 英文题名 | SegQuant: A Semantics-Aware and Generalizable Quantization Framework for Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2507.14811) · [Code](https://github.com/OptiSys-ZJU/segquant) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SegQuant |
| Dataset | MJHQ-30K, DCI |

> [!tip] 效果简介
> - MJHQ-30K 上，FID 23.94 (SegQuant-G) vs 24.10 (Smooth+) (-0.16)；Image Reward 0.924 (SegQuant-A) vs 0.851 (Smooth+) (+0.073)；FID 22.85 (SegQuant-A) vs 23.99 (Q-Diffusion) (-1.14)。
> - DCI 上，FID 22.19 (SegQuant-G) vs 23.67 (Q-Diffusion) (-1.48)。

## 概述

扩散模型在图像生成领域取得了显著进展，但其庞大的模型规模和迭代式采样过程对实时部署构成了严峻挑战。后训练量化（PTQ）是缓解这一问题的关键手段，然而现有方法普遍存在两个根本性瓶颈：其一，依赖手动架构规则或运行时动态启发式，与基于静态计算图的AI编译器（如TensorRT）不兼容，形成“编译器鸿沟”；其二，忽略了线性层中语义片段间的异构性以及SiLU/GELU等极性非对称激活中负值区域所承载的高频纹理与语义信息，导致量化后生成质量显著下降。

针对上述问题，本文提出**SegQuant**——一个语义感知且可泛化的部署友好型量化框架。SegQuant的核心方法论包含两大创新组件：

- **SegLinear（语义分割量化）**：通过静态计算图的拓扑模式匹配，自动检测线性层中由chunk/split/concat等算子产生的隐含语义分割边界，实施分段量化，从根本上消除不同语义通道间的量化干扰，无需任何人工指定或动态数据。
- **DualScale（双尺度极性保留）**：针对SiLU/GELU等激活函数的极性非对称特性，对正、负激活区域分别采用独立尺度量化，通过单次BatchedGEMM高效实现，在不引入定制硬件的前提下高保真保留负值区域中的精细细节。

SegQuant采用模块化设计，将现有量化技术统一为**Optimizer**（如SmoothQuant、SVDQuant）和**Calibrator**（如GPTQ、AMax）两类可插拔组件，与SegLinear和DualScale协同工作，兼具高精度与编译器原生兼容性。

实验结果表明，SegQuant在多个主流扩散模型上取得了领先的量化性能。在MJHQ-30K基准上，SegQuant-G在W8A8设置下将SD3.5-DiT的FID降至23.94，优于Smooth+（24.10）和PTQ4DiT（25.66），逼近FP16精度（23.70）；在FLUX-DiT上，SegQuant-A的FID达到22.85，较Q-Diffusion（23.99）降低1.14。消融实验进一步验证了SegLinear与DualScale的互补性：二者组合使FID从23.35降至22.54，Image Reward从0.877提升至0.952。在效率方面，DualScale相比定制化的PTQ4ViT在AdaNorm层上实现约4倍加速（FLUX: 4201→1075 μs），充分体现了硬件友好设计的优势。

## 背景与动机

### 扩散模型量化的困境：编译器鸿沟与语义盲区

扩散模型已成为文本到图像生成的主流架构，但其巨大的推理成本严重制约了实际部署。后训练量化（Post-Training Quantization, PTQ）通过将浮点权重和激活压缩为低位整数，是缓解这一瓶颈的关键技术。然而，现有扩散模型量化方法面临两个根本性缺陷，导致量化后生成质量显著下降。

**编译器鸿沟（Compiler Gap）。** 以 **Q-Diffusion**、**PTQ4DiT** 等为代表的现有方法，依赖手动架构规则或运行时动态启发式来分配量化策略——例如针对 UNet 的跳跃连接定制处理，或根据去噪时间步动态调整量化参数。这些策略与基于静态计算图优化的 AI 编译器（如 TensorRT）根本不相容：动态值无法在图编译阶段被解析，导致算子融合、内核自动调优等关键优化无法执行。这形成了一道“编译器鸿沟”，使得量化方案要么牺牲生成质量以换取部署效率，要么保留精度却无法被编译器原生支持。

**语义异构性的盲区。** 扩散模型中的线性层并非均匀的计算单元。以 DiT 架构的 AdaNorm 层为例，其权重矩阵内部隐含着由 `chunk`、`split`、`concat` 等静态图算子引入的语义分割边界——不同语义通道对应着不同的特征子空间。现有方法对整层采用统一的量化尺度，忽略了这种通道间的异构性，导致不同语义区域的量化误差相互干扰，产生显著的精度损失。实验证据表明，在 SD3.5 的 DiT.11.norm1_context 层上，GPTQ 量化的 Frobenius 误差高达 3.02，而采用分段量化策略后该误差降至 1.76，降幅达 41.7%。

### 极性非对称激活的精细信息丢失

扩散模型广泛采用 SiLU 和 GELU 等非单调激活函数。与 ReLU 直接截断负值不同，SiLU/GELU 在负值区域保留了平滑的非零输出（见 Figure 6）。这些负激活值并非噪声——它们承载着高频纹理和语义细节。当仅对激活的负值部分进行量化时，生成图像的细节和纹理范围出现明显退化（见 Figure 7），证实了负值区域对视觉质量的关键贡献。

然而，标准对称量化使用单一全局尺度，无法同时高保真地保留正、负两个极性区域的信息。非对称量化通过引入零点在一定程度上缓解此问题，但其额外的零点和广播开销与硬件高效计算相悖。定制化的非均匀量化器（如 **PTQ4ViT** 的对数尺度方案）虽能提升精度，却需要特殊的硬件支持，牺牲了通用部署能力。在 FLUX 模型的 AdaNorm 层上，PTQ4ViT 的推理延迟高达 4201 μs，而硬件友好的双路径方案仅需 1075 μs，提速约 4 倍。

### 本文动机：构建编译器原生且语义感知的量化框架

上述分析揭示了一个核心矛盾：扩散模型量化需要在**精度保留**、**编译器兼容性**和**硬件效率**三者之间取得平衡，而现有方法往往顾此失彼。SegQuant 的动机正是弥合这一鸿沟——通过静态计算图的拓扑模式匹配自动感知线性层中的语义分割边界，并以硬件原生的双尺度策略保留极性非对称激活的精细信息，在不牺牲编译器兼容性的前提下实现逼近全精度的生成质量。

## 核心创新

SegQuant 的核心创新并非提出一种全新的量化范式，而是通过**静态图语义感知**与**极性保留量化**两个互补机制，系统性地解决了扩散模型量化中两个被忽视的瓶颈：编译器兼容性鸿沟与极性非对称激活的信息损失。

### 创新一：从手动规则到拓扑感知的语义分割量化（SegLinear）

现有扩散模型量化方法（如 **Q-Diffusion**、**PTQ4DiT**）依赖两种策略：一是针对特定架构（如 UNet 的 skip 连接）设计手工规则；二是基于运行时动态统计（如时间步变异性）调整量化参数。这两种策略均与基于静态计算图的 AI 编译器（如 TensorRT）不兼容，形成所谓的“编译器鸿沟”。

SegLinear 的核心突破在于将量化策略的生成**完全建立在静态计算图分析之上**。其关键洞察是：扩散模型（尤其是 DiT 架构）的线性层中，因 `chunk`、`split`、`concat` 等算子操作，权重矩阵内部隐含着语义异构的通道组——不同通道组承载着不同语义功能（如时间嵌入、文本条件、潜在特征），统一量化会引发跨语义干扰。

SegLinear 通过以下机制实现自动化语义分割：

1. **图模式匹配**：对计算图（如 `torch.fx` 表示）进行拓扑遍历，自动识别 `chunk`/`split`/`concat` 等算子边界，推断语义分段边界与各段维度 $d_i$。
2. **分段独立量化**：将权重矩阵按语义边界分解为子矩阵：
   - **输出分段**：$\mathbf{W} = [\mathbf{W}_1, \mathbf{W}_2, \cdots, \mathbf{W}_N], \quad \mathbf{W}_i \in \mathbb{R}^{k \times d_i}$
   - **输入分段**：$\mathbf{W} = [\mathbf{W}_1^{\mathrm{T}}, \mathbf{W}_2^{\mathrm{T}}, \cdots, \mathbf{W}_N^{\mathrm{T}}]^{\mathrm{T}}, \quad \mathbf{W}_i \in \mathbb{R}^{d_i \times n}$
   各子矩阵独立应用量化参数（尺度、零点或迁移系数 $\alpha$），消除语义通道间的量化干扰。
3. **编译器原生兼容**：整个分析过程无需任何运行时数据或动态分支，量化策略在编译前完全确定，原生兼容图编译器的算子融合与部署优化。

**关键证据**：在 SD3.5 的 `DiT.11.norm1_context` 层上，SegLinear 将 GPTQ 量化的 Frobenius 误差从 **3.02 降至 1.76**（降幅 41.7%），直接验证了语义分割消除跨通道干扰的有效性（Table 3）。拓扑感知分割与随机分块的对比消融进一步证实：在 SD3 `DiT.0.norm1` 层，SegLinear 的 F-norm 误差为 0.5415，而随机分块为 0.7080（Table 6）。

### 创新二：从单尺度到双尺度极性保留量化（DualScale）

扩散模型中广泛使用的 SiLU 和 GELU 激活函数具有**极性非对称**特性——负值区域虽幅度较小，却承载着高频纹理与语义细节。统计数据显示：在 SD3.5-ControlNet 的 AdaNorm 模块中，SiLU 激活的负值通道占比高达 95.5%（Table 1）。传统对称量化使用单一尺度覆盖正负区域，导致负值区域的量化分辨率严重不足；非对称量化虽引入零点偏移，但会破坏标准 GEMM 的硬件优化路径，带来额外的广播开销。

DualScale 的解决方案是将激活张量按符号分解为两部分，分别采用独立尺度：

- **量化函数**：
  $$Q_{\mathrm{dual}}(x) = \begin{cases} \mathrm{round}\left(\frac{x}{s_-}\right), & x < 0 \\ \mathrm{round}\left(\frac{x}{s_+}\right), & x \ge 0 \end{cases}$$

- **尺度计算**：
  $$s_- = \frac{|\min(x)|}{q_{\mathrm{min}}}, \quad s_+ = \frac{\max(x)}{q_{\mathrm{max}}}$$
  负区域尺度由最小值的绝对值决定，正区域尺度由最大值决定，使两部分均获得与其动态范围匹配的量化分辨率。

- **硬件友好的计算实现**：将激活矩阵分解为 $\mathbf{X}_+ = \max(\mathbf{X}, 0)$ 和 $\mathbf{X}_- = \min(\mathbf{X}, 0)$，分别与低精度权重 $\hat{\mathbf{W}}$ 进行矩阵乘法，最终通过单次 **BatchedGEMM** 操作高效重构输出：
  $$\mathbf{Y} \approx s_+ s_w \cdot (\hat{\mathbf{X}}_+ \hat{\mathbf{W}}) + s_- s_w \cdot (\hat{\mathbf{X}}_- \hat{\mathbf{W}})$$

这一设计的精妙之处在于：**仅对激活应用双尺度，权重保持标准低精度**，从而无需定制量化硬件，完全兼容 CUTLASS 等标准 GEMM 库。

**关键证据**：在 FLUX 的 AdaNorm 层上，DualScale 的推理延迟仅为 **1075 μs**，而定制化的 PTQ4ViT 方案为 4201 μs（提速约 4 倍），同时保持同等精度（Table 8），充分证明了硬件友好设计的效率优势。

### 创新协同：编译器原生的模块化框架

SegQuant 将上述两项创新整合为一个**模块化框架**，通过两个抽象插件——**Optimizer**（如 SmoothQuant、SVDQuant）和 **Calibrator**（如 GPTQ、AMax）——统一了现有量化技术。SegLinear 和 DualScale 作为框架增强模块，与 Optimizer/Calibrator 协同工作：SegLinear 为 Optimizer 提供语义感知的通道分组以优化迁移系数 $\alpha$，DualScale 则在激活量化端独立运作，两者互补提升整体量化鲁棒性。

消融实验证实了这种协同效应：在 SD3.5 W8A8 设置下，单独使用 SegLinear 或 DualScale 均能改善 FID 和 Image Reward，而**两者组合达到最优**——FID 从 23.35 降至 22.54，Image Reward 从 0.877 提升至 0.952（Table 4）。

### 与现有方法的本质差异

| 维度 | 现有方法 | SegQuant |
|------|---------|----------|
| 量化策略生成 | 手动架构规则或运行时动态启发式 | 静态计算图拓扑模式匹配，全自动 |
| 激活量化尺度 | 单一全局尺度（对称/非对称）或定制量化器 | 正负区域独立尺度，标准位宽 |
| 编译器兼容性 | 依赖动态值，与静态编译器不兼容 | 编译前确定策略，原生兼容图编译器 |
| 架构泛化性 | 需针对 UNet/DiT 分别设计 | 图分析通用，适用于 AdaNorm、MHA 等任意模块 |

**总结**：SegQuant 的核心创新不在于发明全新的量化算子，而在于**通过静态图语义分析揭示了扩散模型中隐含的结构异质性**，并以**编译器原生**的方式加以利用，同时以**极性保留**机制解决了 SiLU/GELU 激活的精细信息损失——两者共同构成了一个既高效又部署友好的量化框架。

## 整体框架

SegQuant 采用“优化器–校准器”双插件架构，将现有量化技术与两项核心创新——**SegLinear** 和 **DualScale**——统一为编译器原生的推理管线。其工作流自上而下：首先对模型进行静态计算图分析，自动检测线性层中的语义分割边界；随后在优化器阶段插入平滑或低秩调整，在校准器阶段执行权重量化误差最小化；最后输出可直接部署的量化模型。

### 架构总览

框架由四个逻辑模块构成，按执行顺序为：

1. **语义分割检测**：基于 `torch.fx` 静态图，通过拓扑模式匹配自动识别 `chunk`、`split`、`concat` 等算子产生的隐含语义边界，无需任何运行时数据或人工架构规则。
2. **Optimizer（优化器）**：在检测到的语义分段上插入现有平滑方法（如 **SmoothQuant** 或 **SVDQuant**），对激活分布进行迁移调整，降低量化难度。
3. **Calibrator（校准器）**：采用 **GPTQ** 或原生 `amax` 算法，对分段后的权重进行逐组量化误差校准。
4. **DualScale 极性保留**：针对 SiLU/GELU 等非对称激活，将激活张量分解为正、负两部分并分配独立量化尺度，通过单次 BatchedGEMM 恢复输出。

### 模块间的数据流与协作关系

SegQuant 的核心设计在于 **SegLinear 为 Optimizer 和 Calibrator 提供语义分组依据**，而 **DualScale 在推理阶段独立作用于激活量化**，两者互补且不冲突。

**静态图分析 → 分段量化策略生成**  
SegLinear 从 `torch.fx` 计算图中提取线性层的输出/输入分割模式。对于输出分段，权重矩阵按列分解为 $N$ 个子矩阵 $\mathbf{W} = [\mathbf{W}_1, \mathbf{W}_2, \cdots, \mathbf{W}_N]$，每个 $\mathbf{W}_i \in \mathbb{R}^{k \times d_i}$ 对应一个语义通道组；对于输入分段，则按行分解 $\mathbf{W} = [\mathbf{W}_1^{\mathrm{T}}, \mathbf{W}_2^{\mathrm{T}}, \cdots, \mathbf{W}_N^{\mathrm{T}}]^{\mathrm{T}}$。分段边界完全由图拓扑（如 `chunk` 后的 `reshape` 维度、`concat` 的拼接轴）自动推断，不依赖启发式阈值。

**Optimizer 与 Calibrator 的协同**  
在得到语义分段后，Optimizer 在每个分段内独立搜索最优迁移系数 $\alpha$（如 SmoothQuant 的平滑强度），避免不同语义通道间的量化干扰。Calibrator 随后对分段权重执行 GPTQ 逐列误差补偿，或直接使用 `amax` 校准。这一“先平滑、后校准”的流程在分段粒度上运行，显著降低了量化误差——例如，SD3.5 中 `DiT.11.norm1_context` 层的 GPTQ Frobenius 误差从 3.02 降至 1.76（降幅 41.7%）。

**DualScale 的独立作用路径**  
DualScale 不依赖分段信息，而是作用于激活量化端。对于极性非对称激活（如 SiLU 负值区域占比可达 95.5%，见 Table 1），它将激活矩阵 $\mathbf{X}$ 分解为 $\mathbf{X}_+ = \max(\mathbf{X}, 0)$ 和 $\mathbf{X}_- = \min(\mathbf{X}, 0)$，分别以尺度 $s_+$ 和 $s_-$ 量化：

$$Q_{\mathrm{dual}}(x) = \begin{cases} \mathrm{round}\left(\frac{x}{s_-}\right), & x < 0 \\ \mathrm{round}\left(\frac{x}{s_+}\right), & x \ge 0 \end{cases}$$

其中 $s_- = \frac{|\min(x)|}{q_{\mathrm{min}}}$、$s_+ = \frac{\max(x)}{q_{\mathrm{max}}}$。权重 $\mathbf{W}$ 保持标准低精度量化，最终输出通过两次 BatchedGEMM 加权求和重构：

$$\mathbf{Y} \approx s_+ s_w \cdot (\hat{\mathbf{X}}_+ \hat{\mathbf{W}}) + s_- s_w \cdot (\hat{\mathbf{X}}_- \hat{\mathbf{W}})$$

这一设计避免了非对称量化的零点和广播开销，在 FLUX AdaNorm 层上相比定制化 PTQ4ViT 实现约 4 倍加速（4201→1075 μs），同时保持同等精度。

### 编译器兼容性

SegQuant 的量化策略在编译前完全确定——SegLinear 依赖静态图分析，DualScale 使用标准 GEMM 原语——因此原生兼容 TensorRT 等基于静态计算图的 AI 编译器，支持算子融合和图优化。这是其区别于 Q-Diffusion（UNet 专用手动规则）、PTQ4DiT（时间步动态启发式）等方法的根本优势。

### 关键证据强度

- **SegLinear 有效性**：SD3.5 单层误差降幅 41.7%，且消融实验表明拓扑感知分割优于随机分块（F-norm 误差 0.5415 vs. 0.7080）。
- **DualScale 效率优势**：FLUX AdaNorm 推理延迟降低约 75%，同时保持与定制量化器同等的精度。
- **组合增益**：在 MJHQ-30K 上，SegLinear + DualScale 将 FID 从 23.35 降至 22.54，Image Reward 从 0.877 提升至 0.952，证明两者互补提升量化鲁棒性。

需注意，论文主要在 DiT 和 UNet 架构的文本到图像扩散模型上验证，尚未在视频生成或多模态扩散模型上进行广泛测试。DualScale 虽通过 CUTLASS 高效实现，仍引入一次额外 BatchedGEMM 的计算开销。

### 补充图表

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/001_Figure_1.jpg]]
*Figure 1: SegQuant framework follows a top-down workflow that effectively integrates existing quantization techniques with our novel contributions*

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/002_Figure_2.jpg]]
*Figure 2: Structural overview of the DiT diffusion model, highlighting latent-related modules (left) and time-related modules (right)*

## 核心模块与公式推导

SegQuant 框架在两个核心模块上实现突破：**SegLinear**（语义分割量化）与 **DualScale**（双尺度极性保留）。两者分别解决线性层语义异构性与极性非对称激活的量化瓶颈，并通过与现有 Optimizer/Calibrator 插件的组合形成完整量化管线。

### 3.1 SegLinear：语义感知的分段量化

**动机**：扩散模型（尤其是 DiT）的线性层中存在隐含的语义分割结构——例如 TimeEmbedding 模块中 AdaNorm 的权重矩阵呈现明显的语义分块模式（Figure 4）。若对此类线性层采用全局统一的量化尺度，不同语义通道间的量化误差会相互干扰，导致生成质量下降。

**核心机制**：SegLinear 通过静态计算图（如 `torch.fx` 表示）的拓扑模式匹配，自动检测由 `chunk`、`split`、`concat` 等算子产生的语义分割边界，无需任何手动架构规则或运行时动态数据。检测到的分割边界将权重矩阵按语义通道分解为若干子矩阵，各子矩阵独立执行量化。

**输出分段量化**（Output-Segmented）：当计算图中存在对线性层输出的分割操作时，权重矩阵按列分解：

$$\mathbf{W} = [\mathbf{W}_1, \mathbf{W}_2, \cdots, \mathbf{W}_N], \quad \mathbf{W}_i \in \mathbb{R}^{k \times d_i}$$

其中 $N$ 为语义段数，$d_i$ 为第 $i$ 段的输出维度，满足 $\sum d_i = d$。各段独立量化后，通过拼接恢复完整输出：

$$\hat{\mathbf{Y}} = [\hat{\mathbf{X}} \hat{\mathbf{W}}_1, \hat{\mathbf{X}} \hat{\mathbf{W}}_2, \cdots, \hat{\mathbf{X}} \hat{\mathbf{W}}_N]$$

**输入分段量化**（Input-Segmented）：当计算图中存在对线性层输入的分割操作时，权重矩阵按行分解：

$$\mathbf{W} = [\mathbf{W}_1^{\mathrm{T}}, \mathbf{W}_2^{\mathrm{T}}, \cdots, \mathbf{W}_N^{\mathrm{T}}]^{\mathrm{T}}, \quad \mathbf{W}_i \in \mathbb{R}^{d_i \times n}$$

**关键优势**：
- **编译器原生兼容**：量化策略在编译前通过静态图分析完全确定，与 TensorRT 等基于静态计算图的 AI 编译器原生兼容，弥合了“编译器鸿沟”。
- **架构无关泛化**：自动图分析方法适用于任意架构（包括 AdaNorm、MHA 等），无需针对特定模型设计规则。
- **与逐通道量化的协同**：SegLinear 在语义一致的通道组内共享优化超参数（如 SmoothQuant 中的迁移强度 $\alpha$），与逐通道量化形成互补。

### 3.2 DualScale：双尺度极性保留

**动机**：扩散模型中广泛使用的 SiLU 和 GELU 激活函数具有极性非对称特性——负值区域承载高频纹理与语义信息（Figure 6、Figure 7），但传统对称量化因单一全局尺度而丢失负值区域的精细分辨率。非对称量化虽可保留负值信息，但需引入零点偏移和广播操作，与标准 GEMM 不兼容。

**核心机制**：DualScale 将激活张量分解为正、负两部分，分别应用独立的量化尺度，通过单次 BatchedGEMM 高效恢复输出，无需定制硬件。

**激活分解**：

$$\mathbf{X}_+ = \max(\mathbf{X}, 0), \quad \mathbf{X}_- = \min(\mathbf{X}, 0)$$

**双尺度量化函数**：

$$Q_{\mathrm{dual}}(x) = \begin{cases} \mathrm{round}\left(\frac{x}{s_-}\right), & x < 0 \\ \mathrm{round}\left(\frac{x}{s_+}\right), & x \ge 0 \end{cases}$$

其中尺度由各区域极值决定：

$$s_- = \frac{|\min(x)|}{q_{\mathrm{min}}}, \quad s_+ = \frac{\max(x)}{q_{\mathrm{max}}}$$

**输出重构**：仅对激活 $\mathbf{X}$ 施加双尺度量化，权重 $\mathbf{W}$ 保持标准低精度。正、负部分分别与量化权重执行矩阵乘法，加权求和得到最终输出：

$$\mathbf{Y} \approx s_+ s_w \cdot (\hat{\mathbf{X}}_+ \hat{\mathbf{W}}) + s_- s_w \cdot (\hat{\mathbf{X}}_- \hat{\mathbf{W}})$$

该计算通过 CUTLASS 库实现为单次高效的 BatchedGEMM 操作，避免非对称量化的零点和广播开销。

**关键优势**：
- **高保真负值保留**：正负区域独立标度，在不增加位宽的前提下保留极性细节。
- **硬件友好**：保持标准比特宽度，利用 BatchedGEMM 实现高效推理。在 AdaNorm 层上相比定制化的 PTQ4ViT 提速约 4 倍（FLUX: 4201→1075 μs，Table 8）。
- **鲁棒性**：对校准百分位设置和校准集大小不敏感（Table 5），表明方法具有较好的泛化稳定性。

### 3.3 框架集成

SegQuant 将上述模块与现有方法统一为两个抽象插件：

- **Optimizer**：插入 SmoothQuant 或 SVDQuant 等现有优化器，平滑激活分布或执行低秩调整。
- **Calibrator**：采用 GPTQ 或 AMax 等算法对权重量化误差进行优化或直接校准。

SegLinear 与 DualScale 作为框架增强模块嵌入此管线：SegLinear 在 Optimizer 阶段指导分段量化的超参数优化，DualScale 在 Calibrator 阶段提供双尺度激活量化策略。消融实验（Table 4）表明，两者组合使用将 FID 从 23.35 降至 22.54，Image Reward 从 0.877 提升至 0.952，验证了互补增益。

### 补充图表

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of weights in AdaNorm within the TimeEmbedding module. The distribution reveals distinct semantic patterns*

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/008_Figure_6.jpg]]
*Figure 6: Activation curves of SiLU, GELU, and ReLU. The shaded regions show how SiLU and GELU retain negative values, while ReLU suppresses them*

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/007_Figure_7.jpg]]
*Figure 7: Visual impact of negative-range quantization in SD3.5 (timestep 60, COCO). Only the negative part of activations is quantized to isolate its contribution to image details. (a) and (c) show full images; (b) and (d) zoom in to highlight detail and range loss*

## 实验与分析

### 瓶颈验证：时间相关层与极性非对称激活的量化脆弱性

在构建完整方法之前，SegQuant 首先通过系统性的量化误差分析验证了扩散模型中的两个核心瓶颈。Figure 3 展示了 DiT 扩散模型中各线性层在 INTW8A8 量化下的 Frobenius 误差随去噪时间步的演化：**时间相关模块（time-related layers）的量化误差显著高于潜在相关模块（latent-related layers）**，且误差在不同时间步呈现剧烈波动。这一现象揭示了传统统一量化策略的根本缺陷——它无法适应时间嵌入模块内部的结构异质性。

进一步地，Table 1 提供了 SD3.5-ControlNet 在 COCO 数据集上 SiLU 和 GELU 激活的极性统计（30 个时间步平均）。数据显示，AdaNorm 模块的 SiLU 激活中，**仅含负值的通道占比高达 95.5%（DiT）和 64.5%（ControlNet）**，而 FFN 模块的 GELU 激活中该比例也分别达到 74.4% 和 58.9%。与 ReLU 直接截断负值不同，SiLU 和 GELU 保留了大量负值信息（Figure 6），这些负值区域承载着高频纹理和语义一致性（Figure 7 可视化验证）。传统的单尺度量化器在覆盖正负双极分布时，因尺度由全局极值决定，导致负值区域的量化分辨率严重不足。

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/006_Table_1.jpg]]
*Table 1: Polarity statistics of SiLU and GELU activations from SD3.5-ControlNet on COCO, averaged over 30 timesteps. “Neg/- Pos Ratio” shows the asymmetry in activation distributions*

### 主实验结果

Table 2 汇总了 SegQuant 在不同骨干网络（SD3.5-DiT、FLUX-DiT、SDXL-UNet）和量化位宽设置下的主要结果，评估基准为 MJHQ-30K 数据集。

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/009_Table_2.jpg]]
*Table 2: Main results across different backbones and models on the MJHQ-30K dataset*

**SD3.5-DiT W8A8 设置下**，SegQuant 的两个变体均展现出显著优势：
- **SegQuant-G**（GPTQ 校准器）取得 FID 23.94，优于 **Smooth+**（24.10）、**PTQ4DiT**（25.66）和 **Q-Diffusion**（24.57），逼近 FP16 基线（23.70）。Image Reward 达到 0.924，超越 Smooth+ 的 0.851 达 8.6%。
- **SegQuant-A**（AMax 校准器）在 Image Reward 上表现最佳（0.924），同时 FID（24.12）和 LPIPS（0.226）也具备竞争力。

**FLUX-DiT W8A8 设置下**，SegQuant-A 取得 FID 22.85，相较于 Q-Diffusion（23.99）降低 1.14，PSNR 从 21.82 dB 提升至 22.22 dB。在 DCI 数据集上（Table 11），SegQuant-G 的 FID 达到 22.19，较 Q-Diffusion（23.67）降低 1.48。

**SDXL-UNet W8A8 设置下**，SegQuant-G 在 FID（21.74）和 Image Reward（0.855）上均优于 Smooth+（22.10 / 0.827）和 Q-Diffusion（21.88 / 0.830），验证了方法对 UNet 架构的跨架构泛化能力。

**W4A8 低比特场景下**，SegQuant-G 与 **SVDQuant** 结合后，在 SD3.5-DiT 上取得 FID 24.06，优于 SVDQuant 单独使用（24.32），证明了 SegLinear 和 DualScale 在极低比特下仍能提供增益。

Figure 8 和 Figure 11-14 的主观对比可视化进一步证实，SegQuant 生成的图像在纹理细节、语义一致性和色彩保真度上均更接近 FP16 参考，尤其在复杂场景和人脸区域优势明显。

### 消融实验

**组件贡献分解**（Table 4）：在 SD3.5-DiT W8A8 设置下，仅使用 SegLinear 将 FID 从基线 23.35 降至 22.83，Image Reward 从 0.877 提升至 0.907；仅使用 DualScale 将 FID 降至 22.79，Image Reward 提升至 0.915。**两者组合取得最佳效果**：FID 22.54，Image Reward 0.952，验证了分段量化与双尺度极性保留的互补性。Figure 9 和 Figure 15 的主观消融可视化展示了从基线到逐步叠加 SegLinear 和 DualScale 后图像质量的递进改善。

**单层量化误差**（Table 3）：在 SD3.5 的 DiT.11.norm1_context 层上，SegLinear 将 GPTQ 的 Frobenius 误差从 3.02 降至 1.76（降低 41.7%）。在 DiT.8.norm1 层上，误差从 0.849 降至 0.524。Table 12 的补充结果进一步验证了这一趋势在多个层上的一致性。

**语义分割有效性**（Table 6）：在 SD3 DiT.0.norm1 层上，拓扑感知的 SegLinear 分割（F-norm 误差 0.5415）显著优于随机分块（0.7080）和错误匹配的分块策略（0.7053），证明静态图语义引导的分割是降低量化误差的关键，而非单纯的分块操作。

**DualScale 敏感性分析**（Table 5）：在不同校准百分位数（99.9%-99.999%）和校准集大小（N=16/32/64）设置下，DualScale 的相对 F-norm 误差保持稳定，表明方法对校准超参数不敏感，具有良好的鲁棒性。

### 效率分析

**推理速度**（Table 8）：在 FLUX AdaNorm 层的 W8A8 推理中，DualScale 的实现耗时 1074.93 μs，相较于定制化非对称量化方法 **PTQ4ViT** 的 4201.05 μs 提速约 **3.9 倍**，同时保持同等精度。这一优势源于 DualScale 将正负双路径计算融合为单次 BatchedGEMM 调用，避免了非对称量化的零点和广播开销。

**整体效率**（Figure 10）：在 RTX 4090 上，SegQuant 的 INT8（W8A8）配置将 SD3.5 骨干网络尺寸从 8.2 GB 压缩至 2.1 GB（约 4×），每步推理时间从 73 ms 降至 41 ms（约 1.8× 加速）。INT4（W4A4）配置进一步将模型尺寸压缩至 1.1 GB，每步推理时间降至 29 ms，同时保持可控的质量损失。

**层覆盖统计**（Table 7）：SegLinear 自动识别并处理了 SD3.5 中 120 个可量化线性层中的 24 个（20%），DualScale 覆盖 48 层（40%）。估计的额外内存开销仅为 0.07 MB（SegLinear）和 0.02 MB（DualScale），几乎可忽略。

### 失败模式与局限

1. **架构覆盖范围**：当前验证集中于 DiT 和 UNet 架构的文本到图像扩散模型。视频生成模型中的时序注意力机制和多模态扩散模型中的跨模态融合层可能引入新的语义分割模式，SegLinear 的图模式匹配规则在这些场景下的覆盖率需进一步验证。

2. **DualScale 的计算开销**：虽然 BatchedGEMM 实现高效，但 DualScale 在推理时仍引入一次额外的矩阵乘法操作。在批量较小或序列长度较短的场景下，kernel launch 开销可能抵消计算节省，需要手动评估是否启用。

3. **极低比特下的累积效应**：在 W4A4 设置下，SegLinear 的分段量化与 DualScale 的双路径计算叠加，可能因分段后子矩阵过小导致 GPU 利用率下降，需结合算子融合策略进一步优化。

4. **动态形状适应性**：SegLinear 的静态图分析依赖固定的张量维度信息。对于支持多分辨率生成的扩散模型，动态形状可能导致分割边界失效，需要引入运行时形状推断或回退机制。

### 补充图表

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/014_Table_3.jpg]]
*Table 3: Frobenius norm of quantization error for single linear layers in SD3.5, comparing SmoothQuant (W8A8, tuned α), SVDQuant (W4A8, per-channel), and GPTQ (fixed α=0.5)*

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/015_Table_4.jpg]]
*Table 4: Ablation study on MJHQ-30K with SD3.5 and W8A8 DiT quantization (32 images calibrating). Using SmoothQuant as our optimizer (fixed α=0.5) and AMax*

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/019_Table_8.jpg]]
*Table 8: Runtime comparison of AdaNorm layer quantization and inference (W8A8) on an NVIDIA RTX 4090 GPU*

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/017_Table_6.jpg]]
*Table 6: Semantics Ablation on SD3 DiT.0.norm1. Comparison of our topology-aware segmentation against random and mismatched chunking strategies*

![[assets/figures/papers/paper_list_l930_https_arxiv_org_abs_2507_14811/figures/012_Figure_10.jpg]]
*Figure 10: Performance of quantization strategies on SD3.5 (RTX 4090). INT8 (W8A8) uses SmoothQuant; INT4 (W4A4) uses SVDQuant. Model size includes only the backbone; inference time is per-step (end-to-end)*

## 方法谱系与知识库定位

### 1. 基线方法谱系与关系定位

SegQuant 的核心贡献在于弥合了现有扩散模型量化方法与 AI 编译器之间的“编译器鸿沟”，同时解决了线性层语义异构性和极性非对称激活的量化难题。以下从三个维度梳理其与基线工作的关系：

**（1）基于手动规则的量化方法**

以 **Q-Diffusion** 和 **PTQ4DiT** 为代表的方法依赖架构特定的手动规则或运行时动态启发式。Q-Diffusion 针对 UNet 架构的 skip 连接设计专用量化策略，PTQ4DiT 则利用时间步变异性进行动态量化调整。这些方法与基于静态计算图的 AI 编译器（如 TensorRT）不兼容，因为编译器在部署前需要确定的量化配置，而动态启发式无法在图编译阶段解析。SegQuant 的 SegLinear 模块通过静态图拓扑模式匹配自动检测语义分割边界，将量化策略的生成完全前置到编译阶段，从根本上解决了这一兼容性问题。

**（2）基于平滑迁移的量化方法**

**SmoothQuant** 和 **SVDQuant** 作为 SegQuant 框架中的 Optimizer 插件被直接集成，分别负责激活-权重的平滑迁移和低秩调整。SegQuant 的创新在于将这两种方法纳入统一的 Optimizer/Calibrator 抽象，并通过 SegLinear 为语义相关的通道组优化共享超参数（如 SmoothQuant 中的迁移强度 $\alpha$），从而提升平滑效果。实验表明，SegQuant-G（采用 SmoothQuant + GPTQ 组合）在 SD3.5-DiT W8A8 设置下 FID 达到 23.94，优于直接使用 Smooth+ 的 24.10（Table 2）。

**（3）针对极性非对称激活的量化方法**

**PTQ4ViT** 采用定制化量化器处理 ViT 中的 GELU 激活，但需要非标准硬件支持。SegQuant 的 DualScale 模块以硬件友好的方式解决同一问题：通过将激活张量分解为正、负两部分并分别赋予独立尺度，利用标准 BatchedGEMM 实现高效计算。在 FLUX AdaNorm 层的推理性能对比中，DualScale 耗时仅 1074.93 μs，而 PTQ4ViT 需要 4201.05 μs，提速约 4 倍（Table 8），同时保持同等精度。

### 2. 适用边界与泛化能力

**已验证的架构范围：** SegQuant 在 DiT（SD3.5、FLUX）和 UNet（SDXL）架构上进行了全面验证，涵盖 W8A8 和 W4A8 两种量化位宽设置。SegLinear 的静态图分析方法被证明适用于 AdaNorm、Multi-Head Attention 等异构子模块，无需针对不同架构修改规则。

**泛化潜力的证据：** SegLinear 的语义分割完全基于计算图（如 torch.fx）的拓扑模式匹配，理论上可推广到任何包含 chunk/split/concat 等结构算子的模型。Table 7 统计了各组件实际优化的线性层数量，表明 SegLinear 在 SD3.5 和 FLUX 中均能自动识别大量可分段层。

**未验证的边界：** 论文明确指出尚未在视频生成或多模态扩散模型上进行广泛测试，这是当前方法适用性的已知盲区。此外，DualScale 在极低比特（W4A4 及以下）设置下的表现尚未系统探索。

### 3. 局限性与开放问题

**已知局限：**

1. **架构覆盖有限：** 主要验证集中在文本到图像扩散模型（DiT、UNet），对视频生成、3D 生成等更复杂的扩散架构缺乏实验支撑。
2. **轻微计算开销：** DualScale 在推理时增加一次 BatchedGEMM 操作，虽通过 CUTLASS 库高效实现，但仍引入额外计算。在 W8A8 设置下该开销可忽略，但在更低比特或更大批量下可能成为瓶颈。
3. **静态图依赖：** SegLinear 依赖静态计算图进行分析，对于动态形状（如可变分辨率）或控制流密集的模型，图分析的完整性可能受限。

**开放问题：**

1. **动态形状兼容性：** SegLinear 的静态图分析方法能否有效推广到动态形状的扩散模型？这需要验证图模式匹配在符号形状追踪下的鲁棒性。
2. **极低比特扩展：** DualScale 在 W4A4 及以下结合位分配搜索是否能进一步降低量化误差？当前实验仅覆盖 W8A8 和 W4A8。
3. **时序校准融合：** 将 SegQuant 与时间步重建等时序校准方法结合，能否在保持编译器兼容性的同时进一步提升生成质量？这需要在 Optimizer 抽象中引入时间维度的校准策略。

### 4. 知识库定位

SegQuant 在扩散模型量化领域的定位可概括为：**首个编译器原生、语义感知的通用量化框架**。其核心贡献不在于发明全新的量化算子，而在于：

- **桥接编译器鸿沟：** 将量化策略的生成从运行时动态决策转变为编译期静态分析，使扩散模型量化首次与工业级 AI 编译器（如 TensorRT）原生兼容。
- **语义感知的分段量化：** 通过图模式匹配自动发现线性层中的隐含语义分割，将“架构感知”从人工规则提升为算法自动识别。
- **硬件友好的极性保留：** DualScale 在不引入定制硬件的前提下，以标准 GEMM 实现极性非对称激活的高保真量化，为 SiLU/GELU 激活的量化提供了实用方案。

从更广的模型优化视角看，SegQuant 的 Optimizer/Calibrator 插件架构为未来扩散模型量化方法的集成提供了统一框架，后续工作可在该框架下探索新的平滑策略、校准算法或分段模式。

## 原文 PDF

![[paperPDFs/CVPR_2026/SegQuant_A_Semantics_Aware_and_Generalizable_Quantization_Framework_for_Diffusion_Models.pdf]]