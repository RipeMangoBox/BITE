---
title: "Zero-to-Hero: Enhancing Zero-Shot Novel View Synthesis via Attention Map Filtering"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/Zero_to_Hero_Enhancing_Zero_Shot_Novel_View_Synthesis_via_Attention_Map_Filtering.pdf
project_link: https://zero2hero-nvs.github.io/
code_link: null
aliases:
- ZH
- Zero-to-Hero
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "自注意力图的可靠性"
primary_logic: "将扩散去噪过程类比为 SGD 优化，视自注意力图为“参数”，借鉴梯度聚合与权值平均技术（步内最小池化、跨步 EMA）提升注意力图鲁棒性，从而改善生成质量。"
claims:
- "将 GT 自注意力图注入去噪过程可大幅提升所有图像质量指标（PSNR 达 21.79），证明自注意力图是决定生成质量的关键因素。"
- "Zero-to-Hero 在 GSO 和 RTMV 数据集上，相比基线 Zero-1-to-3 和 Zero123-XL，在所有指标上一致提升（例如 GSO 上 PSNR 从 17.72 升至 18.35）。"
- "消融实验（Table 2）表明 Hourglass 调度、重采样、注意力图过滤、早期互自注意力四个模块均对性能有正向贡献，组合时效果最佳。"
- "注意力图过滤（AMF）在 ControlNet 和 MVDream 等其他生成模型上同样能够减轻伪影、增强条件遵循度，说明方法的泛化性。"
---

# Zero-to-Hero: Enhancing Zero-Shot Novel View Synthesis via Attention Map Filtering

> [!tip] 核心洞察
> 将扩散去噪过程类比为 SGD 优化，视自注意力图为“参数”，借鉴梯度聚合与权值平均技术（步内最小池化、跨步 EMA）提升注意力图鲁棒性，从而改善生成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Zero-to-Hero: 通过注意力图过滤增强零样本新视角合成 |
| 英文题名 | Zero-to-Hero: Enhancing Zero-Shot Novel View Synthesis via Attention Map Filtering |
| 会议/期刊 | NeurIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2405.18677) · [Project](https://zero2hero-nvs.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Zero-to-Hero |
| Dataset | GSO (challenging subset), RTMV |

> [!tip] 效果简介
> - GSO (challenging subset) 上，PSNR↑ 为 18.35，对比 17.72，变化 +0.63。
> - GSO (challenging subset) 上，LPIPS↓ 为 0.153，对比 0.163，变化 -0.01。
> - GSO (challenging subset) 上，IOU↑ 为 78.3%，对比 76.4%，变化 +1.9%。

## 概要

从单张图像合成任意新视角的零样本方法（如 Zero-1-to-3）为三维内容生成带来了便利，但其生成结果常出现几何扭曲、纹理错位等伪影。本文揭示这一瓶颈的根源在于：扩散模型中的交叉注意力退化为全局偏置，自注意力图则因去噪过程中的随机性而不可靠，导致生成视图与输入源图之间产生不一致。

为解决这一问题，本文提出 **Zero-to-Hero**——一种无需额外训练、即插即用的测试时增强方法。其核心洞见是将扩散去噪过程类比为随机梯度下降优化，视自注意力图为“参数”，借鉴梯度聚合与权重平均技术来提升注意力图的鲁棒性。具体而言，Zero-to-Hero 通过**步内最小池化**与**跨步指数移动平均**过滤自注意力图中的异常相关，并辅以**早期互自注意力**将源视角的结构信息注入目标分支，从而在推理阶段显著改善生成质量。

实验表明，Zero-to-Hero 在 GSO 和 RTMV 数据集上一致超越基线 Zero-1-to-3 与 Zero123-XL：在 GSO 挑战子集上，PSNR 从 17.72 提升至 18.35，LPIPS 从 0.163 降至 0.153，IoU 从 76.4% 提升至 78.3%。消融研究验证了沙漏调度、重采样、注意力图过滤与互自注意力四个模块的独立贡献。此外，注意力图过滤在 ControlNet 和 MVDream 等其他生成模型上同样能减轻伪影、增强条件遵循度，展现出良好的泛化性。该方法以约 66 次函数评估的推理开销，在保持时间竞争力的同时，向理想注意力图（oracle）的性能迈出了实质一步。

### 零样本新视角合成的兴起与瓶颈

从单张二维图像生成任意视角下的三维一致视图，是计算机视觉与图形学中长期存在的核心挑战。传统方法依赖多视图立体重建或神经辐射场（NeRF），通常需要密集的多视角输入或针对每个场景进行耗时的优化。近年来，大规模预训练扩散模型的出现，催生了以 **Zero-1-to-3**（Liu et al., arXiv 2023）为代表的零样本新视角合成范式——仅凭一张源图像和一个目标相机姿态，即可在推理时直接生成对应视角的视图，无需针对特定场景进行微调。

然而，这类方法在实际应用中暴露出显著的鲁棒性问题：生成的视图常常出现几何扭曲、纹理不一致以及不自然的伪影。Zero-to-Hero 论文通过深入分析扩散模型内部的注意力机制，揭示了这一瓶颈的根本原因。

### 注意力机制的退化：从交叉注意力到自注意力

扩散模型中的注意力层是连接条件信息与生成内容的关键桥梁。Zero-to-Hero 的分析发现，在 Zero-1-to-3 这类模型中存在两个层面的注意力退化：

**交叉注意力的全局偏置化。** 在 Zero-1-to-3 中，相机姿态信息通过 CLIP 嵌入 $c \in \mathbb{R}^{1 \times d_{CLIP}}$ 注入交叉注意力层，投射为键 $K_t$。由于 softmax 操作要求每行求和为 1，而条件嵌入仅包含单个 token，后 softmax 的注意力图退化为一个常数全 1 矩阵（见 Figure 3）。这意味着交叉注意力实际上沦为全局偏置项，丧失了空间细粒度的条件引导能力，无法有效约束生成内容的几何结构。

**自注意力图的噪声敏感性。** 既然交叉注意力无法提供精确的空间引导，生成质量便高度依赖于自注意力层——即潜在表示中各空间位置之间的相关性建模。然而，扩散模型的去噪过程本质上是随机的：每一步的噪声注入会引入随机性，导致自注意力图中出现异常的强相关或弱相关。这些不可靠的注意力模式直接传导至生成结果，表现为多出一根手指、不自然的拉伸、纹理漂移等伪影。

### 决定性证据：自注意力图是核心控制变量

Zero-to-Hero 通过一个简洁的验证实验确立了自注意力图的因果地位：将目标视角的真实（ground-truth）自注意力图注入去噪过程，所有图像质量指标均出现大幅跃升——PSNR 达到 21.79，远超基线方法（Table 1 底部行，Figure 4）。这一结果表明，**自注意力图是决定生成质量的关键因素**，现有方法的性能瓶颈并非来自模型容量不足，而是去噪过程中自注意力图的可靠性不足。

### 核心洞察：从 SGD 到扩散模型的类比

基于上述发现，Zero-to-Hero 提出了一个概念类比（Figure 5）：将扩散模型的迭代去噪过程视为随机梯度下降（SGD）优化，其中自注意力图扮演“参数”的角色。在 SGD 中，单步梯度更新往往充满噪声，研究者通过梯度裁剪、动量、权值平均等技术来稳定优化轨迹。类似地，扩散模型每一步的自注意力图也受到噪声干扰，需要相应的“聚合”与“平滑”机制来提升其鲁棒性。

这一类比直接催生了 Zero-to-Hero 的核心设计思路：借鉴优化领域的成熟技术，在推理时对自注意力图进行**步内聚合**（类比梯度裁剪/聚合）和**跨步平滑**（类比动量/指数移动平均），从而在不重新训练模型的前提下，显著提升零样本新视角合成的质量与一致性。

### 现有方法的缺口

现有改进零样本新视角合成的尝试大致分为两类：一类通过扩大训练数据或模型规模来提升泛化能力（如 Zero123-XL），但数据量的增加并不能从根本上解决注意力图的随机性问题；另一类引入测试时优化（如 per-step resampling 作为校正机制），但缺乏对注意力图本身的系统性处理。Zero-to-Hero 填补了这一空白：它首次将注意力图可靠性作为核心优化目标，提出了一套即插即用的测试时增强方法。

## 核心方法与创新机理

Zero-to-Hero 的核心创新在于将扩散模型去噪过程中的**自注意力图（self-attention maps）**视为决定生成质量的关键可干预变量，并通过一套无需训练的即插即用机制提升其可靠性。该方法建立在以下关键洞察之上：

### 1. 瓶颈发现：交叉注意力退化与自注意力噪声

对基础模型 **Zero-1-to-3**（Liu et al., arXiv 2023）的注意力层分析揭示了一个此前未被充分重视的退化现象（Figure 3）：由于 softmax 操作的归一化特性，交叉注意力图在后 softmax 阶段**退化为全 1 的常数矩阵**，实质上沦为全局偏置项，丧失了空间定位能力。这意味着模型对目标视角的几何与纹理约束几乎完全依赖自注意力层来传递。然而，自注意力图本身受到去噪过程中随机噪声的干扰，其不可靠性直接导致生成视图出现几何扭曲、纹理偏移等伪影。

**决定性证据**来自一个“神谕实验”（Figure 4, Table 1 底部行）：将真实目标视图的自注意力图注入去噪过程，所有图像质量指标均大幅跃升——PSNR 达到 21.79，相比基线提升超 4 dB。这确凿地证明：**自注意力图的可靠性是零样本新视角合成的核心瓶颈与因果旋钮**。

### 2. 核心类比：从 SGD 到扩散模型

Zero-to-Hero 的方法论创新源于一个概念性类比（Figure 5）：将扩散去噪过程视作随机梯度下降（SGD）优化，自注意力图则对应模型参数。正如 SGD 中梯度噪声导致参数震荡、而梯度聚合（如动量）与权值平均（如 SWA）能提升收敛鲁棒性，扩散模型中的注意力图同样可以通过**步内聚合**与**跨步平滑**来抑制随机性、保留结构信息。这一类比将优化理论中的成熟技术迁移至生成模型的推理阶段，构成了方法设计的理论框架。

### 3. 四个 Changed Slots：从基线到 Zero-to-Hero

相较于基线 Zero-1-to-3 / Zero123-XL 的标准 DDIM 采样流程，Zero-to-Hero 在四个关键环节进行了系统性改造：

| 改造槽位 | 基线方案 | Zero-to-Hero 方案 | 作用机制 |
|---------|---------|-------------------|---------|
| **采样调度** | 均匀 DDIM 采样（25/50/100 步） | Hourglass 调度：去噪首尾阶段以密度因子 λ_den 加密采样，总 26 步 | 早期密集采样利于结构快速成型，末期密集采样提升细节精度 |
| **每步重采样** | 无（每步单次去噪） | 在去噪前期每个时间步迭代 R=5 次加噪-去噪 | 提供步内校正机制，暴露并修正偶然性错误 |
| **注意力图过滤** | 无过滤 | 步内元素级最小池化 + 跨步指数移动平均（EMA） | 抑制异常强相关，保留历史结构信息 |
| **互自注意力** | 无 | 去噪前 1/3 阶段并行生成源视角，注入其键值至目标分支 | 引导目标视角与源视角的几何形状与纹理一致性 |

这四个模块并非简单叠加，而是形成了协同增强的闭环：Hourglass 调度为重采样提供了合适的干预窗口；重采样产生的多份注意力图为步内最小池化提供了聚合素材；跨步 EMA 将过滤后的可靠结构信息传递至后续步骤；互自注意力则在早期阶段提供额外的几何先验，弥补自注意力在去噪初期的信息匮乏。

### 4. 注意力图过滤：步内最小池化与跨步 EMA

注意力图过滤（AMF）是 Zero-to-Hero 最核心的技术创新。其步内聚合采用**元素级最小池化**：

$$\widetilde{M}_{t,r} = \min(M_{t,r}, \{\widetilde{M}_{t,k}\}_{k=1}^{r-1})$$

该操作的理论依据在于：随机噪声倾向于在注意力图中产生**虚假的异常高相关**（即不相关的图像区域被错误地赋予高注意力分数），而最小池化能有效抑制这些离群值，保留跨重采样一致出现的真实结构相关。

跨步平滑则通过**指数移动平均**将当前步的注意力图与历史平滑图融合：

$$\widetilde{M}_{t-1} = \alpha M_t + (1-\alpha) \widetilde{M}_{t-1}, \quad \alpha \in [0,1]$$

这类似于 SGD 中的动量机制，防止结构信息在去噪过程中被过早遗忘。Figure 6 直观展示了 AMF 如何抑制异常强相关：基线 Zero123-XL 的注意力图中，目标区域与无关背景产生虚假高相关，导致生成结果出现不自然的拉伸伪影；而 Zero-to-Hero 的过滤后注意力图则聚焦于语义一致的区域。

### 5. 方法泛化性：超越零样本新视角合成

值得强调的是，注意力图过滤作为一项通用的推理时增强技术，其有效性并不局限于 Zero-1-to-3 架构。实验表明（Figure 7, Figure 14, Figure 15），将 AMF 应用于 **ControlNet** 和 **MVDream** 等其他生成模型时，同样能够减轻伪影、增强条件遵循度。这说明该方法触及了扩散模型注意力机制的一个共性弱点，具有跨架构的迁移潜力。

Zero-to-Hero 是一个在推理阶段即插即用的增强框架，无需额外训练即可提升预训练扩散新视角合成模型的生成质量。其核心思想源于一个关键发现：在 Zero-1-to-3（Liu et al., arXiv 2023）这类模型中，**交叉注意力已退化为全局偏置**（后 softmax 注意力图为常数全 1 矩阵，见 Figure 3），因此视图生成的结构与几何信息几乎完全依赖自注意力层。然而，扩散去噪过程中的随机性会污染自注意力图，导致生成视图与输入不一致，产生几何与外观伪影。

框架将扩散去噪过程类比为 SGD 优化——自注意力图类比为“参数”，每次去噪步类比为一次梯度更新。借鉴梯度聚合与权值平均技术，Zero-to-Hero 通过三个相互协作的模块系统性地提升自注意力图的可靠性，从而改善生成质量。

### 输入输出流

框架的输入为单张源图像 $I_s$ 和目标相机姿态，输出为对应姿态下的新视角图像。整个流程基于预训练的 Zero-1-to-3 或 Zero123-XL 扩散模型，在推理阶段对去噪过程进行干预，不修改模型权重。

### 核心模块与协作关系

如图 Figure 2 所示，Zero-to-Hero 包含四大组件，按执行流程组织如下：

1. **Hourglass 采样调度（HourglassScheduler）**：将去噪过程划分为三个阶段，在早期结构生成阶段和末期细节精化阶段以更高密度采样时间步（密度因子 $\lambda_{den}$），而在中间阶段稀疏采样。总步数仅需 26 步即可超越均匀 DDIM 采样的 25、50、100 步效果（见 Table 6/Table 8），在降低计算开销的同时提升关键阶段的生成质量。

2. **步内重采样与注意力图过滤（ResamplingModule + InStepMapPooling + CrossStepMapEMA）**：在选定的时间步区间 $[t_{min}, t_{max}]$ 内，每个去噪步执行 $R=5$ 次加噪-去噪迭代（重采样）。每次迭代产生的自注意力图通过**元素级最小池化**进行步内聚合：
   $$\widetilde{M}_{t,r} = \min(M_{t,r}, \{\widetilde{M}_{t,k}\}_{k=1}^{r-1})$$
   该操作抑制随机噪声引起的异常强相关（见 Figure 6）。随后，当前步的聚合注意力图通过**跨步指数移动平均**传递至下一时间步：
   $$\widetilde{M}_{t-1} = \alpha M_t + (1-\alpha) \widetilde{M}_{t-1}, \quad \alpha \in [0,1]$$
   EMA 机制保留了历史结构信息，防止细节在去噪过程中过早丢失。

3. **早期互自注意力（MutualSelfAttention）**：在去噪过程的前 1/3 阶段，并行生成一个源视角（使用恒等姿态），并将其自注意力层的键（Key）和值（Value）注入目标视角分支的自注意力层。这一机制引导目标视角在生成早期与源视角保持几何形状与纹理的一致性，对结构一致性贡献显著（IoU 从 76.4% 提升至 77.6%，见 Table 10）。

### 模块间的协同

四个模块并非孤立运作：Hourglass 调度为早期阶段分配更多步数，使互自注意力有充分机会引导结构形成；重采样为注意力图过滤提供多次观测样本，而 EMA 跨步平滑则将这些样本的历史信息串联起来。消融实验（Table 2, Table 5）表明，各模块单独使用均有正向贡献，组合使用时效果达到最优（GSO 上 PSNR 从基线 17.72 提升至 18.35）。

### 计算开销与公平性

框架引入的额外推理时间约为 0.5-1.5 秒。公平性通过控制总函数评估次数（NFE）来保证：Zero-to-Hero 的 66 NFE 与基线 25 步（25 NFE）按生成效果相近的步数进行对比，所有定性比较使用相同随机种子初始化。

### 问题诊断：注意力层的退化与关键性

Zero-to-Hero 的核心动机源于对基础模型 **Zero-1-to-3**（Liu et al., arXiv 2023）中注意力机制的深入分析。研究发现，扩散模型在零样本新视角合成任务中存在两个关键瓶颈：

**交叉注意力的退化。** Zero-1-to-3 使用单点 CLIP 姿态嵌入 $c \in \mathbb{R}^{1 \times d_{CLIP}}$ 作为条件，在交叉注意力层中将其投影为键 $K_t$。由于 softmax 函数的求和恒为 1，后 softmax 注意力图 $\text{softmax}(A)$ 退化为全 1 常数矩阵（见 Figure 3）。这意味着交叉注意力本质上已沦为全局偏置项，丧失了空间差异化的条件引导能力，无法为生成过程提供精确的姿态约束。

**自注意力的关键性与随机性。** 由于交叉注意力失效，生成视图的结构与几何信息实际上由自注意力层通过潜在向量各元素间的相似度得分隐式保留。然而，扩散去噪过程中的随机噪声会引入自注意力图的扰动，导致异常强相关或弱相关，进而产生几何扭曲与外观伪影。决定性证据来自 oracle 实验：将目标视角的 GT 自注意力图注入去噪过程，PSNR 可达 21.79，所有图像质量指标大幅超越基线（Table 1 底部行，Figure 4），明确了自注意力图是决定生成质量的关键控制变量。

### 核心洞察：从 SGD 到扩散模型的类比

Zero-to-Hero 将扩散去噪过程与随机梯度下降（SGD）优化建立概念类比（Figure 5）：

- 自注意力图 $\widetilde{M}_t$ 对应优化中的“参数”；
- 每个去噪步产生的注意力图 $M_t$ 对应单步梯度更新；
- 噪声引起的注意力图随机波动对应梯度噪声。

基于此类比，方法借鉴了 SGD 中提升参数鲁棒性的两类技术：**步内梯度聚合**（对应元素级最小池化）和**跨步动量平均**（对应指数移动平均 EMA），将其迁移到注意力图的优化中。

### 模块一：重采样与步内注意力图聚合

在选定的时间步区间 $[t_{\text{min}}, t_{\text{max}}]$ 内，每个去噪步执行 $R$ 次重采样迭代（$R=5$）：将去噪后的潜在表示 $z_t$ 按正确噪声比例重新加噪至上一采样步 $z_{t+1}$，再次去噪回 $z_t$。这一过程为每个时间步生成 $R$ 个独立的自注意力图 $\{M_{t,1}, M_{t,2}, \ldots, M_{t,R}\}$。

步内聚合采用**元素级最小池化**（in-step min-pooling），逐步融合同一步内的多个注意力图：

$$\widetilde{M}_{t,r} = \min\left(M_{t,r},\; \{\widetilde{M}_{t,k}\}_{k=1}^{r-1}\right)$$

其中 $\widetilde{M}_{t,r}$ 为第 $t$ 步第 $r$ 次重采样后的累积注意力图。最小池化算子的设计意图是抑制随机噪声引起的异常强相关：如果某个空间位置的注意力得分在多次重采样中偶然飙升，取最小值操作可有效将其压制，保留多次采样中一致出现的可靠关联。实验表明，最小池化优于平均池化等其他聚合算子。

### 模块二：跨步指数移动平均

步内聚合后的注意力图通过**指数移动平均**（EMA）传递至下一时间步，实现跨步的历史信息融合：

$$\widetilde{M}_{t-1} = \alpha M_t + (1-\alpha) \widetilde{M}_{t-1}, \quad \alpha \in [0,1]$$

其中 $M_t$ 为当前步经步内聚合后的注意力图，$\widetilde{M}_{t-1}$ 为上一步的 EMA 累积图，$\alpha$ 控制当前步信息的融合权重。这一机制保留了去噪早期建立的结构信息，防止在后期去噪中因细节细化而丢失全局几何约束。Figure 6 通过可视化注意力得分对比，展示了过滤后异常高相关被有效抑制，生成结果避免了不自然的几何拉伸。

### 模块三：早期互自注意力

在去噪过程的前 1/3 阶段，并行运行一个源视角生成分支（使用恒等姿态），将其自注意力层的键 $K$ 和值 $V$ 注入目标视角分支的自注意力层。这一设计的逻辑在于：去噪早期是结构生成的关键阶段，源视角提供了可靠的几何与纹理参考，通过键值注入引导目标视角的自注意力分布，强化跨视角的一致性。消融实验（Table 10）表明，互自注意力将 IoU 从 76.4% 提升至 77.6%，验证了其对结构一致性的关键贡献。

### 模块四：Hourglass 采样调度

将去噪过程划分为三个阶段，在首尾阶段以密度因子 $\lambda_{\text{den}}$ 进行更高密度的 DDIM 采样（总计 26 步）。早期密集采样有助于快速建立合理结构，末期密集采样则提升细节精度；中间阶段可稀疏采样以节省计算。Table 6/Table 8 显示，Hourglass 调度仅用 26 步即可超越均匀 DDIM 采样的 25、50、100 步性能，在减少采样步数的同时轻微提升指标。

## 实验与关键发现

### 核心实验设置

Zero-to-Hero 在 **Zero-1-to-3**（Liu et al., arXiv 2023）和 **Zero123-XL** 两个基线模型上进行测试，测试平台为 GSO 挑战性子集和 RTMV 数据集。实验采用 DDIM 采样器，基础步数为 26 步的 Hourglass 调度，重采样迭代次数 R=5，过滤区间覆盖去噪过程的前 2/3 阶段。公平性方面，所有对比通过控制总函数评估次数（NFE）进行：Zero-to-Hero 的 66 NFE 与基线 Zero-1-to-3 的 25 步（25 NFE）在生成质量相近的条件下进行对比，而非简单按等步数对齐；所有定性比较使用相同的随机种子初始化，确保差异仅由方法引起。

### 主要结果

**Table 1** 展示了 GSO 挑战子集上的定量结果。Zero-to-Hero 在所有指标上一致超越基线方法：

- 基于 Zero123-XL 时，PSNR 从 17.72 dB 提升至 **18.35 dB**（+0.63 dB），LPIPS 从 0.163 降至 **0.153**，IoU 从 76.4% 提升至 **78.3%**（+1.9%）。
- 基于 Zero-1-to-3 时，PSNR 从 16.92 dB 提升至 **17.42 dB**，LPIPS 从 0.177 降至 **0.170**，IoU 从 71.7% 提升至 **73.6%**。

RTMV 数据集上的结果（**Table 3**）呈现相同趋势，Zero-to-Hero 在两个基线模型上均取得一致提升，验证了方法在不同数据分布下的鲁棒性。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2405_18677/figures/015_Table_3.jpg]]
*Table 3: Quantitative evaluation on RTMV dataset. Zero-to-Hero consistently improves performance upon baselines*

**Table 1 底部行**（GT maps）是理解方法上限的关键证据：将真实目标视角的自注意力图注入去噪过程后，PSNR 飙升至 **21.79 dB**，LPIPS 降至 0.121，IoU 达到 87.7%。这一结果直接证明自注意力图是决定生成质量的核心瓶颈——Zero-to-Hero 正是通过逼近这一 oracle 性能来改善生成效果。

### 消融实验

**Table 2** 系统拆解了四个模块的贡献（基于 Zero123-XL）：

| 配置 | PSNR↑ | LPIPS↓ | IoU↑ |
|------|-------|--------|------|
| 基线（25 步均匀采样） | 17.72 | 0.163 | 76.4% |
| + Hourglass 调度 | 17.80 | 0.161 | 76.7% |
| + Hourglass + Resample | 17.85 | 0.160 | 77.1% |
| + Hourglass + Resample + AMF | 17.92 | 0.157 | 77.6% |
| + 全部模块（含 MSA） | **18.35** | **0.153** | **78.3%** |

每个模块均提供正向贡献，且组合使用时效果最优。在 Zero-1-to-3 上重复的消融实验（**Table 5**）呈现一致的贡献模式，排除了模块效果依赖于特定基线的可能性。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2405_18677/figures/018_Table_5.jpg]]
*Table 5: Ablation study — Zero-1-to-3. We demonstrate the importance of each of Zero-to-Hero modules, applied to the base method Zero-1-to-3: Sample scheduling (Hourglass), Resampling (Resample), Attention map filtering (AMF), and Early stage Mutual Self-Attention (MSA)*

**注意力图过滤（AMF）的独立贡献**在 Table 7 中进一步验证：在重采样基础上加入 AMF，PSNR 从 17.85 提升至 17.92，LPIPS 从 0.160 降至 0.157。**早期互自注意力（MSA）** 的消融（Table 10）显示，MSA 将 IoU 从 76.4% 提升至 77.6%，验证了其对结构一致性的关键作用；同时发现将去噪步数从 1000 压缩至 600 时效果最优，表明 MSA 在去噪早期阶段介入最为有效。

**Hourglass 调度**的消融（Table 6/Table 8）表明，仅用 26 步即可超越均匀 DDIM 采样的 25、50、100 步，在减少采样步数的同时轻微提升所有指标，验证了“首尾密集、中间稀疏”的采样策略在效率与质量上的双重优势。

### 定性分析

**Figure 1** 和 **Figure 10** 展示了 Zero123-XL 与 Zero-to-Hero 在多个视角下的生成对比。Zero-to-Hero 生成的视图在几何一致性（物体轮廓完整、无异常拉伸）和纹理保真度（细节清晰、与源图一致）上显著优于基线，尤其在基线容易产生伪影的大角度视角变换场景中改善明显。

**Figure 6** 从注意力图层面解释了改善机制：Zero123-XL 的自注意力图中存在随机性强相关区域（对应生成结果中的伪影），而 Zero-to-Hero 通过注意力图过滤有效抑制了这些异常相关，使注意力分布更聚焦于合理的结构区域。

**Figure 11** 分别展示了 MSA 和 AMF 在不同场景下的贡献：MSA 在需要保持源图几何结构的场景（如对称物体、规则形状）中效果突出；AMF 则在减少随机纹理伪影（如不自然的拉伸、模糊区域）方面表现更佳。

### 泛化性验证

注意力图过滤（AMF）的泛化性在 **ControlNet** 和 **MVDream** 上得到验证。**Figure 7** 显示，将 AMF 应用于姿态条件的 ControlNet 后，生成结果更好地遵循了条件信号，同时减少了伪影；Figure 14 和 Figure 15 进一步在 MVDream 上验证了 AMF 的跨模型有效性。这表明 AMF 作为一种即插即用的推理时增强模块，不依赖于特定模型架构。

### 计算开销

**Table 4** 的运行时分析显示，Zero-to-Hero 引入的额外计算开销为 0.5–1.5 秒，在可比 NFE 下仍保持时间竞争力。重采样与互自注意力的引入增加了约 50% 至 100% 的推理时间，但考虑到无需任何训练或微调，这一开销在多数应用场景中是可接受的。

### 局限性与失败模式

1. **多样性-真实感权衡**：注意力图过滤的强度（通过增大 R 或延长过滤区间）与生成多样性呈负相关（Figure 12）。过滤迭代次数增加时，结果趋于更真实但多样性降低，需要在两者间折衷。
2. **严重条件偏差的改善有限**：方法基于固定的预训练模型权重，当基线模型本身无法正确理解极端姿态条件时，注意力图过滤难以从根本上纠正条件遵循错误。
3. **场景泛化边界**：当前评估主要限于 GSO、RTMV 等前景分割清晰的数据集，在复杂背景或非物体中心场景上的表现尚待验证。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2405_18677/figures/009_Table_2.jpg]]
*Table 2: Ablation Study. We demonstrate the importance of each of Zero-to-Hero modules, applied to the base method Zero123-XL: Sample scheduling (Hourglass), Resampling (Resample), Attention map filtering (AMF), and Early-Stage Mutual Self-Attention (MSA). Consistent conclusions are reached with the base model Zero-1-to-3 and are shown in Sec. 8.6 of the appendix*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2405_18677/figures/019_Table_6.jpg]]
*Table 6: Ablation study: Hourglass scheduling — Zero123-XL. We demonstrate the superiority of our Hourglass scheduling over uniform DDIM sampling with different number of denoising steps. The experiments are based on Zero123-XL*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2405_18677/figures/020_Table_7.jpg]]
*Table 7: Ablation study: Attention map filtering — Zero123-XL. We demonstrate the importance of Attention Map Filtering (AMF) over only applying Resampling (Resample). The experiments are based on Zero123-XL*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2405_18677/figures/021_Table_8.jpg]]
*Table 8: Ablation study: Hourglass scheduling — Zero-1-to-3. We demonstrate the superiority of our Hourglass scheduling over uniform DDIM sampling with different number of denoising steps. The experiments are based on Zero-1-to-3*

## 定位与知识库关联

### 问题定位：扩散新视角合成的注意力退化瓶颈

Zero-to-Hero 针对的是**零样本新视角合成**（NVS）任务中一个被忽视的根本性问题：预训练扩散模型（以 **Zero-1-to-3**（Liu et al., arXiv 2023）及其增强版 **Zero123-XL** 为代表）的注意力层在推理阶段会系统性地退化。具体而言：

- **交叉注意力退化**：Zero-1-to-3 将单点 CLIP 姿态嵌入 $c \in \mathbb{R}^{1 \times d_{CLIP}}$ 作为条件，经 softmax 归一化后，后 softmax 注意力图退化为全 1 常数矩阵（见 Figure 3），等价于一个全局偏置项，丧失了条件引导能力。
- **自注意力随机性**：自注意力图受扩散噪声的随机扰动，产生异常强相关或弱相关，导致生成视图与输入源图在几何结构和纹理上不一致，表现为拉伸、错位等伪影。

这一诊断通过一项关键实验得到确证：将目标视角的 GT 自注意力图注入去噪过程，PSNR 可飙升至 21.79（Table 1 底部行），证明**自注意力图的可靠性是决定生成质量的核心因果杠杆**。

### 核心洞察：从 SGD 到扩散模型的类比迁移

Zero-to-Hero 的方法论创新根植于一个概念类比（Figure 5）：将扩散模型的迭代去噪过程视为类似 SGD 的优化过程，其中**自注意力图扮演了“参数”的角色**。基于这一视角，论文将梯度优化中成熟的稳健性技术迁移至注意力图空间：

| SGD 优化技术 | 扩散模型对应 | Zero-to-Hero 模块 |
|---|---|---|
| 梯度聚合（多步累积） | 步内重采样注意力图聚合 | **In-step Min-Pooling** |
| 权值平均（EMA） | 跨步注意力图平滑 | **Cross-step EMA** |
| 学习率调度 | 采样步密度分配 | **Hourglass Scheduling** |

这一类比并非表面修辞，而是直接指导了模块设计：步内最小池化 $\widetilde{M}_{t,r} = \min(M_{t,r}, \{\widetilde{M}_{t,k}\}_{k=1}^{r-1})$ 抑制异常高相关（类比梯度裁剪），跨步 EMA $\widetilde{M}_{t-1} = \alpha M_t + (1-\alpha) \widetilde{M}_{t-1}$ 保留历史结构信息（类比动量）。

### 在 NVS 方法谱系中的位置

零样本新视角合成方法大致可分为两条技术路线：

1. **基于大规模预训练扩散模型**：以 Zero-1-to-3 和 Zero123-XL 为代表，将 2D 扩散先验与相机姿态条件结合，通过微调 Stable Diffusion 实现单图到新视角的生成。此类方法泛化性强但推理时缺乏显式 3D 约束，易产生几何不一致。
2. **基于 3D 重建与渲染**：如 NeRF、3D Gaussian Splatting 等，从稀疏视角重建显式或隐式 3D 表示后渲染新视角。此类方法几何精度高但依赖多视角输入，且计算开销大。

Zero-to-Hero 属于**第一类路线的推理时增强方法**，与以下工作形成互补或对比：

- 与 **Zero-1-to-3 / Zero123-XL** 的关系：Zero-to-Hero 直接在这些预训练模型上运行，**无需额外训练**，属于 plug-and-play 的测试时增强方案。它不改动模型权重，仅干预去噪过程中的注意力图计算和采样调度。
- 与基于优化的方法（如 **SDS（Score Distillation Sampling）** 系列）的关系：SDS 类方法通过额外优化步骤提升 3D 一致性，但通常需要多次前向传播和梯度计算，计算成本高。Zero-to-Hero 的重采样机制在概念上类似“校正”，但完全在扩散模型的去噪循环内完成，不引入外部损失或优化器。
- 与注意力控制方法（如 **Prompt-to-Prompt**、**Cross-Attention Control**）的关系：此类工作主要面向文本到图像生成中的布局和内容编辑，通过操控交叉注意力图实现语义控制。Zero-to-Hero 的不同之处在于：(a) 它操作的是**自注意力图**而非交叉注意力；(b) 其目标不是编辑而是**稳健化**——抑制噪声引起的随机波动。

### 适用边界与局限

**适用场景**：
- 以物体为中心的前景分割清晰的数据集（如 GSO、RTMV），模型在这些场景上验证充分。
- 需要快速部署且无法进行模型微调的场景——Zero-to-Hero 的额外推理时间仅 0.5–1.5 秒（在 66 NFE 配置下）。

**已知局限**：
1. **真实感与多样性的折衷**：注意力图过滤的迭代次数 $R$ 越大、过滤时间区间越长，生成结果越真实但多样性越低（Figure 12）。这本质上是 EMA 平滑的固有效应——过度平滑会压制合理的生成变体。
2. **计算开销**：重采样（$R=5$）和互自注意力（并行源视角生成）将推理时间增加约 50%–100%。虽然通过 Hourglass 调度（26 步）部分对冲了步数增加的影响（总 NFE 66 vs 基线 25），但对于实时应用仍有压力。
3. **模型依赖**：方法完全依赖预训练模型 Zero-1-to-3 / Zero123-XL 的生成能力。当基础模型本身存在严重的条件偏差（如极端视角下的姿态理解错误）时，注意力图过滤无法从根本上纠正。
4. **场景泛化性未充分验证**：实验主要局限于前景分割清晰的物体数据集（GSO、RTMV），在复杂背景、多物体交互、室外场景上的表现尚待评估。

### 泛化性证据与开放问题

注意力图过滤（AMF）展现出超越 NVS 任务的泛化潜力：在 **ControlNet**（姿态条件图像生成）和 **MVDream**（多视角扩散）上，AMF 同样能够减轻伪影、增强条件遵循度（Figure 7, Figure 14, Figure 15）。这表明“自注意力图稳健化”可能是一个跨扩散模型任务的通用原则。

**开放问题**：
- 能否**自适应地选择**重采样迭代次数 $R$ 和过滤时间区间 $[t_{min}, t_{max}]$，而非依赖人工调参？例如根据去噪过程中的注意力图方差动态调整。
- 注意力图过滤策略能否**融入训练过程**（如作为正则化项），从而在测试时免除重采样的计算开销？
- 该方法在**视频生成、文本到图像生成**等更广泛的扩散模型任务中的有效性如何？AMF 在 ControlNet 上的初步结果暗示了潜力，但缺乏系统性的定量评估。
- 当前方法完全依赖自注意力图的稳健化，但交叉注意力的退化问题（全 1 矩阵）并未被直接修复。能否通过**重新设计交叉注意力机制**（如多向量条件嵌入）来恢复姿态条件的精确引导，而非仅依赖自注意力来弥补？

## 原文 PDF

![[paperPDFs/NEURIPS_2024/Zero_to_Hero_Enhancing_Zero_Shot_Novel_View_Synthesis_via_Attention_Map_Filtering.pdf]]
