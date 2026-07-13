---
title: "Light-T2M: A Lightweight and Fast Model for Text-to-motion Generation"
type: paper
paper_level: A
venue: AAAI
year: 2025
pdf_ref: paperPDFs/AAAI_2025/Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation.pdf
project_link: null
code_link: https://github.com/qinghuannn/light-t2m
aliases:
- LT
- Light-T2M
tags:
- AAAI_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过引入轻量级局部建模（LIMM）替代部分全局层，并用Mamba+伪双向扫描实现高效全局建模，配合自适应文本注入器（ATII），同时大幅压缩模型并保持/提升生成质量。
primary_logic: 局部运动平滑性对真实运动生成至关重要；卷积与状态空间模型的混合设计，加上门控文本注入，可以在极低参数下实现高性能。
claims:
- Light-T2M仅4.48M参数（MoMask的10%），FID在HumanML3D上为0.040（MoMask为0.045），推理速度提升16%。
- 移除自适应文本注入器（ATII）导致FID从0.040上升至0.102，R-Top1从0.511降至0.489。
- 伪双向扫描（PBDS）以零额外参数实现优于单向扫描和Vim双向扫描的性能。
- LGL（局部-全局-局部）块设计在所有消融配置中取得最佳FID（0.040）和R-Top1（0.511）。
---

# Light-T2M: A Lightweight and Fast Model for Text-to-motion Generation

> [!tip] 核心洞察
> 局部运动平滑性对真实运动生成至关重要；卷积与状态空间模型的混合设计，加上门控文本注入，可以在极低参数下实现高性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | Light-T2M：面向文本到动作生成的轻量快速模型 |
| 英文题名 | Light-T2M: A Lightweight and Fast Model for Text-to-motion Generation |
| 会议/期刊 | AAAI 2025 |
| Links | [Code](https://github.com/qinghuannn/light-t2m) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Light-T2M |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.040±.002 vs 0.045±.002 (MoMask) (-0.005)；#Params 4.48M vs 44.85M (MoMask) (-90.0%)；Average Inference Time (AIT)↓ 0.151s vs 0.180s (MoMask) (-0.029s (↓16%))。
> - KIT-ML 上，FID↓ 0.161±.009 vs 0.228 (MoMask) (-0.067)；R-Precision Top1↑ 0.444±.006 vs 0.406 (MoMask, est.) (+0.038)。

## 概要

文本到动作生成（Text-to-Motion, T2M）旨在根据自然语言描述合成逼真的三维人体运动序列。近年来，基于扩散模型和Transformer架构的方法取得了显著进展，但现有工作普遍存在**模型参数冗余、推理速度慢**的瓶颈——典型代表如**MoMask**（Guo et al., 2024）需要约45M可训练参数。造成这一问题的深层原因在于：现有方法过度依赖Transformer的全局自注意力机制进行建模，**忽视了局部运动平滑性这一对真实运动生成至关重要的先验**，同时文本信息的注入方式也较为低效。

针对上述问题，本文提出**Light-T2M**，一种面向文本到动作生成的轻量级快速模型。其核心设计理念是：**以轻量级局部建模替代部分全局建模，并用状态空间模型实现高效全局信息交互**。具体而言，Light-T2M引入了三个关键创新：

1. **局部信息建模模块（LIMM）**：基于一维深度可分离卷积，以极低参数代价捕获相邻帧间的运动平滑性。
2. **Mamba + 伪双向扫描（PBDS）**：将Mamba状态空间模型引入T2M任务，并通过序列反转拼接实现零参数增加的双向信息交互效果。
3. **自适应文本注入器（ATII）**：利用Sigmoid门控机制对文本嵌入进行通道级重加权，使文本语义能够自适应地注入各个运动片段。

在架构层面，Light-T2M采用**局部-全局-局部（LGL）**的块设计——每个基本块包含两个LIMM模块和一个集成了ATII与Mamba的全局建模模块，配合下采样/上采样操作在压缩的时序长度上进行语义注入与全局交互。

实验结果表明，Light-T2M在**仅4.48M参数（约为MoMask的10%）**的条件下，在HumanML3D数据集上取得了**0.040的FID**（MoMask为0.045），在KIT-ML数据集上取得了**0.161的FID**（MoMask为0.228），同时推理速度提升约16%。消融实验进一步验证了ATII和PBDS的关键作用：移除ATII导致FID从0.040显著上升至0.102；PBDS以零额外参数实现了优于单向扫描和标准双向扫描的性能。这些结果共同表明，**局部建模与高效全局建模的混合设计，配合门控文本注入，可以在大幅压缩模型规模的同时保持甚至提升生成质量**，为T2M模型的轻量化部署提供了可行路径。



文本到动作生成（Text-to-Motion, T2M）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，基于扩散模型的方法显著提升了生成质量，代表性工作如 **MDM**（Tevet et al., 2023）、**MLD**（Chen et al., 2023）和 **MoMask**（Guo et al., 2024）在 HumanML3D 和 KIT-ML 等基准上取得了令人瞩目的结果。

然而，现有方法存在一个被普遍忽视的结构性瓶颈：**过度依赖 Transformer 的全局自注意力机制进行序列建模**。这种设计带来了两方面的问题。其一，自注意力的计算复杂度随序列长度呈二次增长，导致模型参数量庞大、推理速度缓慢——例如 MoMask 的可训练参数高达 44.85M，单次推理耗时约 0.180 秒。其二，Transformer 层擅长捕获长程依赖，却**缺乏对局部运动平滑性的显式建模能力**。真实人体运动在时间上具有天然的连续性和平滑性，相邻帧之间的关节角度和位置变化应遵循物理约束，而纯全局建模无法有效利用这一先验。

此外，现有方法中**文本语义的注入方式也存在效率问题**。主流方案通常采用交叉注意力或自注意力的混合模式将文本嵌入与运动特征融合，这种“一刀切”式的注入策略忽略了不同运动片段对文本语义需求的差异性——某些片段（如“挥手”）需要强语义引导，而过渡性片段则更依赖运动自身的平滑先验。

针对上述问题，**Light-T2M** 的提出基于一个核心洞察：**局部运动平滑性对真实运动生成至关重要，通过卷积与状态空间模型的混合设计，配合自适应的门控文本注入，可以在极低参数量下实现甚至超越大模型的性能**。具体而言，该工作从三个层面重新审视了 T2M 模型的设计范式：

1. **局部建模的必要性**：引入轻量级的局部信息建模模块（LIMM），利用一维深度可分离卷积显式捕获相邻帧之间的平滑约束，弥补 Transformer 在局部感知上的不足。
2. **全局建模的效率革命**：采用 Mamba 状态空间模型替代 Transformer 编码器层，配合提出的**伪双向扫描**（Pseudo-Bidirectional Scan, PBDS），以零额外参数实现双向信息交互，在保持全局建模能力的同时大幅降低参数量和计算开销。
3. **文本注入的自适应化**：设计**自适应文本信息注入器**（Adaptive Textual Information Injector, ATII），通过 Sigmoid 门控机制根据运动片段的语义需求动态调制文本嵌入的通道权重，实现“按需注入”。

这一设计理念在实验中得到了充分验证：Light-T2M 仅使用 4.48M 可训练参数（MoMask 的 10%），在 HumanML3D 上取得了 0.040 的 FID（MoMask 为 0.045），推理速度提升 16%（**Figure 1**；**Table 1**）。



## 核心方法与创新机理

Light-T2M 的核心创新并非单一技术的堆砌，而是源于对现有文本到动作（T2M）生成范式的系统性反思：**当前主流方法过度依赖 Transformer 的全局自注意力机制，忽视了运动序列内在的局部平滑性，导致模型参数冗余、推理缓慢，且文本语义注入方式低效**。针对这一瓶颈，Light-T2M 进行了三个关键层面的变革，形成了“局部-全局-局部”（LGL）的轻量级混合架构。

### 1. 局部信息建模模块（LIMM）：用卷积填补 Transformer 的盲区

现有 SOTA 方法（如 MoMask）几乎完全依赖 Transformer 层进行序列建模，隐式地假设全局注意力足以捕获所有运动模式。Light-T2M 的核心洞察在于：**人体运动的自然平滑性——相邻帧之间的关节角度、速度变化通常具有高度连续性——是一种强先验，而全局自注意力对此既不敏感，也引入了不必要的计算开销**。

为此，Light-T2M 设计了**局部信息建模模块（LIMM）**，其结构极为精简：由一层 1D 逐点卷积 $f^p(\cdot)$ 和一层 1D 深度可分离卷积 $f^d(\cdot)$ 级联，辅以 LayerNorm 和 ReLU 激活，并通过残差连接与输入相加：

$$\hat{X} = X + \operatorname{ReLU}(\operatorname{Norm}(f^p(f^d(X))))$$

这一设计的因果机制在于：深度可分离卷积在通道和时序维度上解耦建模，以极少的参数（相比自注意力的二次复杂度）显式编码局部时间邻域内的运动连续性。在消融实验中，将 LIMM 替换为 Transformer 层（即 LGL → TGT 等变体）导致 FID 从 0.040 显著恶化（Table 2），直接验证了局部显式建模对运动质量的关键作用。

### 2. 伪双向扫描（PBDS）：零参数代价的双向全局建模

在全局信息建模层面，Light-T2M 大胆地**用 Mamba（状态空间模型）替代 Transformer 编码器**，以利用其线性时间复杂度和高效的长序列处理能力。然而，原生 Mamba 的单向扫描机制限制了每个位置只能获取左侧上下文，这在需要双向理解的运动生成中构成缺陷。

为解决此问题，Light-T2M 提出了**伪双向扫描（PBDS）**，其操作简洁而巧妙：将输入运动序列 $X^o$ 沿时间轴反转得到 $X^r$，将两者拼接后同时送入 Mamba 扫描，最终仅保留原始序列 $X^o$ 对应的输出。如 Figure 3 所示，这一操作使得原始序列中的每个元素能够间接“看到”原本位于其右侧的信息，**在不增加任何参数的前提下实现了双向扫描的效果**。

消融实验（Table 3）提供了决定性证据：PBDS 在 4.48M 参数下取得 FID 0.040，而单向扫描（SDS）的 FID 为 0.088，Vim 的双向扫描（BDS）为 0.067。PBDS 以零额外参数超越了两种替代方案，其因果逻辑在于：双向信息流使 Mamba 能更完整地建模运动序列的全局依赖，而简单的序列反转策略避免了 BDS 中双分支带来的特征不一致风险。

### 3. 自适应文本注入器（ATII）：从“拼接”到“门控调制”的语义注入

传统方法通常将文本嵌入与运动特征简单拼接或通过交叉注意力注入，这种方式忽略了**不同运动片段对文本语义的需求存在显著差异**——例如，“抬手”这一动作中，手臂抬起的片段需要强语义约束，而保持静止的片段则几乎不需要文本引导。

Light-T2M 的**自适应文本注入器（ATII）** 通过一个受 LSTM 门控机制启发的通道重加权策略解决了这一问题。具体而言，对于每个运动片段特征 $X_i$ 和文本嵌入 $y$，ATII 首先将它们拼接后通过一个小型网络 $g^c$ 预测通道维度的权重，再通过 Sigmoid 门控对文本嵌入进行调制：

$$\hat{y} = \operatorname{Sigmoid}(g^c(X_i, y)) \odot y$$

随后，调制后的文本特征 $\hat{y}$ 与运动片段 $X_i$ 通过融合网络 $g^f$ 进行整合：

$$\hat{X}_i = g^f(X_i, \hat{y})$$

这一设计的因果效应在消融实验中得到了强力验证（Table 3）：**移除 ATII 的门控机制（直接将拼接特征送入融合层）导致 FID 从 0.040 急剧上升至 0.102，R-Top1 从 0.511 降至 0.489**。这表明，让文本语义的注入强度自适应于运动片段的实际需求，是保证生成质量与文本一致性的关键控制变量。

### 4. 扩散预测目标的转变：从噪声到原始运动

一个常被忽视但重要的创新点是 Light-T2M 对扩散预测目标的重新选择。主流扩散模型（如 MDM）通常预测注入的噪声 $\epsilon$，而 Light-T2M 改为**直接预测原始干净运动 $M^0$**：

$$\mathcal{L} = \mathbb{E}_{M^0, t, \epsilon} \left\| M^0 - \phi_\theta(M^t, t, c) \right\|^2$$

这一转变的动机在于：运动数据的结构高度规整，直接预测 $M^0$ 使模型能够更直接地利用运动的物理约束（如关节角度范围、骨骼长度守恒）。在推理时，预测的 $M^0$ 通过公式 $\epsilon = \frac{M^t - \sqrt{\bar{\alpha}_t} M^0}{\sqrt{1 - \bar{\alpha}_t}}$ 转换回噪声，以兼容分类器无关引导（CFG）。虽然该设计的独立消融未在文中单独报告，但其与 LGL 架构的协同构成了整体性能提升的基础。

### 创新总结：三个 changed slots 的系统性协同

Light-T2M 相对于 SOTA baseline（MoMask）的核心创新可归纳为三个 **changed slots** 的系统性重构：

| 创新维度 | Baseline（MoMask 等） | Light-T2M | 因果效应 |
|---------|---------------------|-----------|---------|
| **局部建模** | 无（仅全局自注意力） | LIMM（1D 深度可分离卷积） | 显式编码运动平滑性，大幅压缩参数 |
| **全局建模** | Transformer 编码器 | Mamba + 伪双向扫描（PBDS） | 线性复杂度，零参数双向信息流 |
| **文本注入** | 自/交叉注意力混合 | 自适应文本注入器（ATII） | 片段级门控调制，文本一致性显著提升 |

这三个创新并非孤立存在，而是通过 **LGL（局部-全局-局部）块设计** 形成有机整体：LIMM 在全局建模前后分别施加，既预处理局部特征以提升全局建模效率，又后处理全局输出以恢复细节平滑性。Table 2 的消融实验证实，LGL 配置在所有变体（TLL、LTL、GLL 等）中取得最优 FID（0.040）和 R-Top1（0.511），验证了“局部包围全局”这一设计哲学的有效性。

最终，这三个 changed slots 的协同效应使 Light-T2M 仅用 MoMask 10% 的可训练参数（4.48M vs 44.85M），在 HumanML3D 上取得更优的 FID（0.040 vs 0.045），并将推理速度提升 16%（0.151s vs 0.180s），实现了效率与质量的双重突破。



Light-T2M 是一个基于扩散框架的文本到动作生成模型，其核心设计目标是在极低参数量的前提下保持甚至超越现有 SOTA 的生成质量。模型整体采用“局部-全局-局部”（LGL）的块堆叠架构，由 $N$ 个基本块串联组成，每个基本块内部包含**两个局部信息建模模块（LIMM）** 和一个**全局信息建模与文本注入模块**，形成对称的信息提取与融合流水线 [Figure 2]。

![[assets/figures/papers/paper_list_l1823_Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Light-T2M. (a) Our Light-T2M consisting of N basic blocks aims to predict*

### 数据流与模块协作

给定文本描述，首先通过冻结的 CLIP 文本编码器提取文本嵌入 $y$，作为全局条件信号贯穿整个去噪网络。运动生成端则从随机噪声 $M^T$ 出发，逐步去噪得到干净运动 $M^0$。每一层基本块的数据流如下：

1. **局部建模前置**：输入运动序列首先经过第一个 LIMM，利用轻量 1D 深度可分离卷积捕获相邻帧间的局部运动平滑性，这是模型对“运动连续性”这一物理先验的显式编码。
2. **下采样与语义提取**：经局部增强后的序列进入全局模块，首先通过下采样操作沿时间轴压缩序列长度，将运动划分为若干语义片段。这一步不仅降低了后续全局建模的计算量，还使得每个片段携带更完整的局部语义信息。
3. **自适应文本注入**：下采样后的每个运动片段 $X_i$ 与文本嵌入 $y$ 一同送入自适应文本信息注入器（ATII）。ATII 通过拼接 $X_i$ 和 $y$ 预测通道级门控权重，对文本嵌入进行重加权：$\hat{y} = \text{Sigmoid}(g^c(X_i, y)) \odot y$，使得不同运动片段能够自适应地吸收与自身最相关的文本语义，而非均等地接受全局文本信号。
4. **全局信息建模**：注入文本语义后的片段序列进入 Mamba 模块进行全局依赖建模。此处采用伪双向扫描（PBDS）策略——将原始序列反转后与原序列拼接送入 Mamba，仅保留原始序列对应的输出，以零额外参数实现双向信息交互。
5. **上采样与融合**：Mamba 输出的序列经上采样恢复至原始时间长度，然后与第一个 LIMM 的输出通过融合层进行残差式融合：$\hat{X} = h(X + \bar{X})$，确保全局语义信息与局部细节信息充分混合。
6. **局部建模后置**：融合后的序列经过第二个 LIMM，进一步精炼局部运动细节，输出当前块的最终表示。

### 扩散预测目标与推理流程

与主流扩散模型预测噪声 $\epsilon$ 不同，Light-T2M 直接预测干净运动 $M^0$，训练目标为 $\mathcal{L} = \mathbb{E}_{M^0, t, \epsilon} \| M^0 - \phi_\theta(M^t, t, c) \|^2$。在推理阶段，模型预测出 $\hat{M}^0$ 后，通过前向扩散公式反推出等效噪声 $\epsilon = \frac{M^t - \sqrt{\bar{\alpha}_t} \hat{M}^0}{\sqrt{1 - \bar{\alpha}_t}}$，再结合分类器无关引导（CFG）公式 $\hat{\epsilon} = (1 + s) \cdot \epsilon_c - s \cdot \epsilon_u$ 计算引导后的噪声，最终通过 DDIM 或 UniPC 采样器更新 $M^{t-1}$，完成一步去噪。

### 效率来源

整个 pipeline 的效率优势来自三个关键设计决策的叠加：(1) LIMM 使用深度可分离卷积替代 Transformer 的自注意力层，大幅压缩参数量；(2) 下采样操作将 Mamba 全局建模的计算量控制在较低水平；(3) PBDS 以零参数代价实现双向扫描效果，避免了传统双向 Mamba 的参数量翻倍。最终模型仅需 4.48M 可训练参数（约 MoMask 的 10%），推理速度提升 16%，同时 FID 在 HumanML3D 上达到 0.040，优于 MoMask 的 0.045 [Table 1]。



Light-T2M 是一个基于扩散框架的文本驱动动作生成模型，其核心设计围绕三个关键模块展开：**局部信息建模模块（LIMM）**、**全局信息建模与文本注入模块**，以及**自适应文本信息注入器（ATII）**。整体架构由 N 个基本块堆叠而成，每个基本块包含两个 LIMM 和一个全局模块，形成“局部-全局-局部”（LGL）的信息流结构（Figure 2）。

---

### 扩散框架与训练目标

模型采用标准的去噪扩散概率模型（DDPM）框架，但预测目标从常规的噪声 $\epsilon$ 改为**预测原始干净运动 $M^0$**。给定文本条件 $c$ 和带噪运动 $M^t$，去噪网络 $\phi_\theta$ 直接输出对 $M^0$ 的估计：

$$
\mathcal{L} = \mathbb{E}_{M^0, t, \epsilon} \left\| M^0 - \phi_\theta(M^t, t, c) \right\|^2 \tag{1}
$$

前向扩散过程按标准方式向干净运动逐步注入高斯噪声：

$$
M^t = \sqrt{\bar{\alpha}_t} M^0 + \sqrt{1 - \bar{\alpha}_t} \epsilon \tag{2}
$$

推理阶段采用分类器无关引导（CFG）。由于模型预测的是 $M^0$ 而非 $\epsilon$，需先将预测的 $M^0$ 转换为等效噪声后再进行引导混合：

$$
\hat{\epsilon} = (1 + s) \cdot \epsilon_c - s \cdot \epsilon_u \tag{3}
$$

其中 $\epsilon_c$ 和 $\epsilon_u$ 分别由条件预测 $M^0_c$ 和无条件预测 $M^0_u$ 通过下式反算：

$$
\epsilon = \frac{M^t - \sqrt{\bar{\alpha}_t} M^0}{\sqrt{1 - \bar{\alpha}_t}} \tag{8}
$$

这一“预测 $M^0$ + CFG 中转换为噪声”的设计，使模型在推理时能灵活控制文本约束强度，同时保持训练目标的简洁性。

---

### 局部信息建模模块（LIMM）

LIMM 的设计动机源于一个被现有方法忽视的观察：**局部运动平滑性对真实动作生成至关重要**。该模块基于轻量级 1D 卷积实现，结构为“逐点卷积 → 深度卷积 → 归一化 → ReLU”，并辅以残差连接：

$$
\hat{X} = X + \operatorname{ReLU}(\operatorname{Norm}(f^p(f^d(X)))) \tag{4}
$$

其中 $f^p(\cdot)$ 为 1D 逐点卷积（point-wise convolution），$f^d(\cdot)$ 为 1D 深度卷积（depth-wise convolution）。深度可分离卷积的组合极大降低了参数量，同时有效捕获相邻帧之间的局部运动连续性。该模块在每个基本块的首尾各放置一次，形成对局部细节的双重精炼。

---

### 全局信息建模与伪双向扫描

全局模块承担两个职责：**时序下采样后的长程依赖建模**和**文本语义注入**。输入运动序列首先经过下采样压缩时序长度，得到蕴含局部语义的运动片段（segment），随后依次通过 ATII 注入文本信息和 Mamba 块进行全局建模，最后上采样恢复原始长度并与残差路径融合：

$$
\hat{X} = h(X + \bar{X}) \tag{5}
$$

其中 $\bar{X}$ 为上采样后的序列，$h(\cdot)$ 为融合层。

Mamba 作为一种状态空间模型（SSM），本身仅支持单向扫描，这限制了每个位置获取全局上下文的能力。为此，Light-T2M 提出了**伪双向扫描（Pseudo-Bidirectional Scan, PBDS）**（Figure 3）：将输入运动序列反转得到 $X^r$，与原序列 $X^o$ 一同送入 Mamba 扫描，但仅保留原序列对应的输出。这一技巧使每个元素能够间接获取其右侧元素的信息，实现双向扫描的效果，且**不引入任何额外参数**。消融实验（Table 3）表明，PBDS（FID 0.040）显著优于单向扫描 SDS（FID 0.088）和 Vim 的双向扫描 BDS（FID 0.067）。

![[assets/figures/papers/paper_list_l1823_Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation/figures/003_Figure_3.jpg]]
*Figure 3: In our pseudo-bidirectional scan, each element in the original sequence can obtain the information from elements originally on its right, achieving the effect of bidirectional scanning without increasing parameters*

---

### 自适应文本信息注入器（ATII）

ATII 是全局模块中的关键组件（Figure 4），其核心思想是**让每个运动片段自适应地决定需要多少文本语义以及哪些语义维度**。具体而言，对于第 $i$ 个运动片段 $X_i$ 和文本嵌入 $y$，先通过拼接和线性变换预测通道级门控权重，再对文本嵌入进行重加权：

![[assets/figures/papers/paper_list_l1823_Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of our Adaptive Textual Information Injector. ⊙ and*

$$
\hat{y} = \operatorname{Sigmoid}(g^c(X_i, y)) \odot y \tag{6}
$$

其中 $g^c(\cdot)$ 为门控预测函数，$\odot$ 表示逐元素乘积。调制后的文本特征 $\hat{y}$ 随后与运动片段融合：

$$
\hat{X}_i = g^f(X_i, \hat{y}) \tag{7}
$$

$g^f(\cdot)$ 为融合函数。这种门控机制使文本注入具有**片段级自适应性**：不同运动阶段可根据自身状态选择性吸收文本语义，而非被动接受固定的交叉注意力。消融实验（Table 3）证实，移除 ATII（替换为直接拼接后融合）导致 FID 从 0.040 急剧上升至 0.102，R-Top1 从 0.511 降至 0.489，验证了门控重加权机制的重要性。

---

### 模块协同与设计选择

LGL（局部-全局-局部）的块排列是经过消融验证的最优设计（Table 2）：在 4.48M 参数下取得 FID 0.040、R-Top1 0.511、R-Top3 0.795。相比之下，将 LIMM 替换为 Transformer 层（TTT）或调整排列顺序（如 LTL、GLL）均导致性能下降，印证了**局部建模与全局建模交替进行**的有效性。下采样尺度为 8 时达到最佳平衡（Table 6）：尺度 1 时 R-Top1 较低，尺度 16 时性能轻微下降。



## 实验与关键发现

### 主实验结果

Light-T2M 在两个主流基准 HumanML3D 和 KIT-ML 上进行了全面评估，与当前 SOTA 方法 **MoMask**（Guo et al., 2024）、**MDM**（Tevet et al., 2023）、**MLD**（Chen et al., 2023）、T2M-GPT、MotionDiffuse 等进行了对比。核心结果如 Table 1 所示：

![[assets/figures/papers/paper_list_l1823_Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation on the HumanML3D and KIT-ML test set. Following previous works, we replicated the experiment 20 times to calculate the average results, presented with a 95% confidence interval (denoted by±). The best result is bolded and the second is underlined. Average Inference time (AIT) is calculated from the average across 100 samples using the same RTX 3090Ti GPU*

- **HumanML3D 数据集**：Light-T2M 以仅 **4.48M** 可训练参数（MoMask 的 10%）取得了 **FID 0.040±.002**，优于 MoMask 的 0.045±.002，同时平均推理时间从 0.180s 降至 **0.151s**（↓16%）。R-Precision Top1 为 0.511±.003，略低于 MoMask 的 0.521±.002，但 MM Dist 和 Diversity 指标保持竞争力。
- **KIT-ML 数据集**：Light-T2M 的 FID 达到 **0.161±.009**，显著优于 MoMask 的 0.228，R-Precision Top1 为 0.444±.006，同样优于 MoMask（估计约 0.406）。

Figure 1 的 FID-参数量散点图直观展示了 Light-T2M 的效率优势：模型越靠近原点，综合性能越好。Light-T2M 在极低参数量下实现了最优 FID，验证了轻量局部建模与高效全局建模混合设计的有效性。

![[assets/figures/papers/paper_list_l1823_Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation/figures/001_Figure_1.jpg]]
*Figure 1: Comparison on FID and the number of parameters. The closer the model is to the origin, the better. Only trainable parameters are calculated*

所有方法的推理时间均在相同 RTX 3090Ti GPU 上测量（未使用混合精度，重复 20 次取平均），参数计数仅包括可训练参数，不包括 CLIP 等固定编码器。

### 消融实验

#### 模型设计消融（Table 2 / Table 5）

![[assets/figures/papers/paper_list_l1823_Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation/figures/008_Table_2.jpg]]
*Table 2: Analysis of Model Design. We evaluate the performance when replacing basic blocks in Light-T2M with other basic blocks. “T” denotes one Transformer encoder layer. “L” denotes our Local Information Modeling Module. “G” denotes our Global Information Modeling and Injection Textual Information Module. “M” and “M∗” denote an original Mamba block and a BiMamba block in (Zhu et al. 2024)*

为验证 LGL（局部-全局-局部）块设计的有效性，论文将 Light-T2M 的基本块替换为不同组合进行对比：

- **LGL 配置**（两个 LIMM + 一个全局模块）：取得最佳 FID **0.040** 和 R-Top1 **0.511**。
- **TLL 配置**（Transformer 替代前端局部模块）：FID 上升至 0.072，R-Top1 降至 0.505，表明前端局部建模对运动细节捕捉至关重要。
- **LTL 配置**（中间层替换为 Transformer）：FID 为 0.055，性能有所下降，说明 Mamba 的全局建模效率优于 Transformer。
- **GLG 配置**（全局模块前置）：FID 为 0.066，R-Top1 降至 0.498，验证了“先局部后全局”的设计合理性。
- **MMM 配置**（全部替换为原始 Mamba 块）：FID 为 0.112，性能显著下降，证明仅靠 Mamba 无法充分捕获局部运动平滑性。
- **M\*M\*M\* 配置**（全部替换为 BiMamba 块）：FID 为 0.088，虽优于单向 Mamba，但仍不及 LGL。

这些结果表明，局部信息建模模块（LIMM）与 Mamba 全局模块的协同是性能提升的关键，单一模块类型无法同时兼顾局部平滑性和全局语义。

#### 扫描策略消融（Table 3）

![[assets/figures/papers/paper_list_l1823_Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation/figures/009_Table_3.jpg]]
*Table 3: Evaluation of Different Scans in Mamba and Analysis on Adaptive Textual Information Injectior (ATII). SDS denotes the original single-directional scan in Mamba. BDS denotes the bidirectional scan in (Zhu et al. 2024). PBDS denotes our pseudo-bidirectional scan. “w/o gating” denotes that we directly feed the concatenation of segment token and text token into the fusion layer*

针对 Mamba 的扫描方式，论文对比了三种策略：

- **单向扫描（SDS）**：FID 0.088，R-Top1 0.505。
- **Vim 双向扫描（BDS）**：FID 0.067，R-Top1 0.507，参数增加。
- **伪双向扫描（PBDS）**：FID **0.040**，R-Top1 **0.511**，**零额外参数**。

PBDS 通过将输入序列反转后与原序列拼接送入 Mamba，仅保留原始序列输出，以零参数代价实现了双向信息交互。这一设计使得序列中每个元素都能获取原本位于其右侧的信息（Figure 3），在参数效率上远超 BDS。

#### 自适应文本注入器消融（Table 3）

移除 ATII 的门控机制（即直接拼接运动片段和文本嵌入后送入融合层）导致性能大幅下降：

- FID 从 0.040 上升至 **0.102**（↑155%）
- R-Top1 从 0.511 降至 **0.489**
- MM Dist 从 2.870 上升至 2.940

这表明基于 Sigmoid 门控的通道重加权机制（Eq. 6-7）能有效筛选与当前运动片段相关的文本语义，抑制无关信息的干扰，是文本-运动对齐的核心组件。

#### 下采样尺度消融（Table 6）


全局模块中的下采样操作旨在压缩时序长度以提取语义片段并降低计算量：

- 尺度为 **8** 时 FID 和 R-Top1 最优。
- 尺度为 1（无下采样）时 R-Top1 较低，可能因为缺乏语义聚合。
- 尺度为 16 时性能轻微下降，可能因过度压缩丢失时序细节。

#### 采样步数与采样器消融（Table 7）


使用 UniPC 采样器时：

- 10 步即可取得接近最佳的结果，继续增加步数收益甚微。
- 5 步时 DDIM 优于 UniPC，表明 UniPC 在极低步数下不稳定。

这一发现为推理加速提供了实用指导：10 步 UniPC 即可在速度与质量间取得良好平衡。

#### 引导尺度消融（Table 9）


分类器无关引导（CFG）尺度 s 控制文本约束强度：

- s = 3 或 4 时性能最佳。
- s ≥ 5 后 FID 迅速上升，表明过强的文本约束会损害运动自然度。

### 与同期工作对比（Table 8）

![[assets/figures/papers/paper_list_l1823_Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation/figures/014_Table_8.jpg]]
*Table 8: Quantitative comparison with Motion Mamba on the HumanML3D and KIT-ML test set*

与同期工作 **Motion Mamba** 的对比显示，Light-T2M 在 HumanML3D 和 KIT-ML 上的 FID 均优于 Motion Mamba，且参数量更少（4.48M vs Motion Mamba 的更大模型）。由于 Motion Mamba 代码未公开，无法评估其推理时间。

### 定性分析（Figure 5）

Figure 5 展示了 Light-T2M 与 MoMask 等方法的生成动作定性对比。红色标注区域指示了生成内容与文本不匹配或肢体失真的问题，绿色/红色虚线分别表示人物运动轨迹是否符合文本描述。Light-T2M 在文本-动作对齐和肢体合理性方面表现更优。

### 失败模式与局限性

1. **数据集泛化性**：仅在 HumanML3D 和 KIT-ML 上评估，未在其他运动数据集上验证。
2. **参数统计口径**：参数计数不包括 CLIP 等固定编码器，实际部署成本可能略高于报告值。
3. **消融实验标准差**：部分消融未报告多次运行的标准差，结论可能受随机性影响。
4. **长文本处理**：ATII 对复杂长描述的处理能力未深入探讨。
5. **极低参数量极限**：模型在 <2M 参数时能否保持可接受质量尚待验证（Figure 6 展示了参数量的影响趋势，但具体数值需查阅原文）。

![[assets/figures/papers/paper_list_l1823_Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation/figures/007_Figure_6.jpg]]
*Figure 6: Impact of The Number of Parameters*

### 开放问题

- 伪双向扫描是否可推广到其他序列建模任务？
- 将 ATII 应用于纯 Transformer 架构是否能取得更好结果？
- 引导尺度、下采样尺度、采样步数等超参数的最优组合是否跨数据集稳定？
- 能否进一步压缩模型至移动端可部署的规模（如 <1M）？



## 定位与知识库关联

### 1. 与现有工作的关系

Light-T2M 处于文本驱动动作生成（Text-to-Motion, T2M）的扩散模型谱系中，其核心贡献在于对“效率—质量”权衡的重新审视。现有 T2M 方法可分为两条主线：

**基于扩散的生成范式。** **MDM**（Tevet et al., 2023）开创性地将扩散模型引入 T2M，直接在原始运动空间进行去噪，但依赖 Transformer 编码器实现文本条件注入，参数量大且推理速度慢。**MLD**（Chen et al., 2023）将扩散过程迁移到 VAE 潜空间以加速推理，但潜空间的压缩—重建过程可能损失细粒度运动细节。**MotionDiffuse** 则在扩散框架中探索了文本驱动的细粒度控制。Light-T2M 继承了扩散范式的基本骨架（前向加噪、反向去噪），但做出了关键改变：将预测目标从噪声 $\epsilon$ 改为原始运动 $M^0$（见 Eq. 1），这一选择使得分类器无关引导（CFG）可以通过噪声恢复公式（Eq. 8）间接实现，而非直接预测噪声。

**基于 VQ-VAE 的离散化范式。** **T2M-GPT** 将运动量化为离散 token，用 GPT 风格的 Transformer 进行自回归生成。**MoMask**（Guo et al., 2024）进一步引入掩码建模和层次化量化，在生成质量上达到 SOTA，但其 Transformer 解码器仍带来 44.85M 的可训练参数。Light-T2M 以 MoMask 为主要对标基线，在 HumanML3D 上以仅 10% 的参数量（4.48M vs. 44.85M）实现了更优的 FID（0.040 vs. 0.045），同时推理速度提升 16%（0.151s vs. 0.180s），证明了轻量扩散架构在 T2M 任务中的竞争力。

**状态空间模型（SSM）的引入。** 同期工作 **Motion Mamba** 率先将 Mamba 引入 T2M，但采用 Vim（Zhu et al., 2024）中的双向扫描方案。Light-T2M 的伪双向扫描（PBDS）与之形成直接对比：PBDS 通过序列反转拼接实现双向信息交互，参数零增长，在消融实验中 FID 达到 0.040，优于 Vim 双向扫描的 0.067 和单向扫描的 0.088（Table 3），表明 PBDS 是更高效的扫描策略。

### 2. 适用边界

**数据集范围。** 当前验证仅覆盖 HumanML3D 和 KIT-ML 两个英文文本—运动数据集。HumanML3D 包含约 14,616 个动作序列，KIT-ML 约 3,911 个，均为单人在有限动作类别内的运动。模型在更大规模、更多样化运动类型（如双人交互、手部精细动作、舞蹈等）数据集上的泛化能力尚未验证。

**文本复杂度。** ATII 的门控机制在标准文本描述上表现出色，但其对复杂长描述、多动作序列组合、否定语义等情况的处理能力未做深入分析。消融实验显示移除门控后 FID 从 0.040 飙升至 0.102，R-Top1 从 0.511 降至 0.489（Table 3），说明文本注入质量对整体性能极为敏感，但当前实验未覆盖文本复杂度的系统性变化。

**参数效率的下界。** 当前最优配置为 4.48M 参数（4 个基本块）。Figure 6 展示了参数量的影响趋势，但模型在更低参数量（如 <2M 甚至 <1M）时能否保持可接受的生成质量，以及性能崩溃的临界点在哪里，仍是开放问题。

**实时部署。** 推理时间 0.151s 是在 RTX 3090Ti 上测量，未使用混合精度。实际移动端或边缘设备部署时，推理延迟可能显著增加，且参数统计不包括 CLIP 文本编码器等固定组件，实际部署的内存占用可能高于报告值。

### 3. 局限性与已知失败模式

**文本—动作错位。** Figure 5 的定性对比显示，Light-T2M 在某些情况下仍存在生成动作与文本描述不对应的问题（红色标注区域），例如文本要求“向前走”但生成动作的移动路径（绿色/红色虚线）不符合描述。这表明 ATII 的门控机制虽然有效，但在细粒度语义对齐上仍有改进空间。

**肢体失真。** 同样在 Figure 5 中，部分生成结果存在肢体扭曲等物理不合理现象。这可能是 LIMM 的局部卷积感受野有限，无法完全保证全局运动学一致性所致。

**超参数敏感性。** 多项消融揭示了关键超参数的敏感区间：下采样尺度为 8 时最优，尺度 1 时 R-Top1 较低，尺度 16 时性能轻微下降（Table 6）；引导尺度在 3–4 时最佳，≥5 后 FID 迅速上升（Table 9）；UniPC 采样器在 10 步即可接近最优，但 5 步时 DDIM 优于 UniPC（Table 7）。这些最优配置是否跨数据集稳定，尚未验证。

**评估的统计稳健性。** 消融实验（Table 2, Table 3, Table 5–9）未报告多次运行的标准差，而主实验（Table 1）提供了 20 次重复的 95% 置信区间。部分消融结论可能受单次运行的随机性影响，需要手动验证。

**与 Motion Mamba 的对比受限。** 由于 Motion Mamba 代码未公开，无法公平对比推理时间和部分指标，当前对比仅基于论文报告值（Table 8），其可信度受限于对方论文的完整性。

### 4. 开放问题

1. **伪双向扫描的泛化性。** PBDS 以零参数代价实现双向效应，这一策略是否可推广到其他序列建模任务（如语音合成、时间序列预测）值得探索。

2. **ATII 的架构独立性。** 将 ATII 的门控文本注入机制应用于纯 Transformer 架构是否能取得类似或更好的效果？当前消融仅对比了“有/无门控”，未测试 ATII 与其他 backbone 的组合。

3. **局部—全局块的排列优化。** LGL（局部-全局-局部）排列在消融中取得最优（FID 0.040），但 Table 2 和 Table 5 的变体探索仍有限。是否存在更优的排列（如 LGLGL）或动态排列策略，是架构搜索的潜在方向。

4. **极端压缩的可行性。** 模型能否进一步压缩至移动端可部署规模（<1M 参数）？这可能需要更激进的卷积核缩减、通道剪枝或知识蒸馏，但当前 Figure 6 的趋势分析不足以预测极端压缩后的性能下限。

5. **多模态扩展。** 当前仅支持文本输入，能否将 LIMM + Mamba + ATII 的轻量架构扩展到语音、音乐或视频驱动的动作生成，是值得关注的方向。



## 原文 PDF

![[paperPDFs/AAAI_2025/Light_T2M_A_Lightweight_and_Fast_Model_for_Text_to_Motion_Generation.pdf]]
