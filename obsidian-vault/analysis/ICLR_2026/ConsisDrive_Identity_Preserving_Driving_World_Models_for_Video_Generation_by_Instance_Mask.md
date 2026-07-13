---
title: "ConsisDrive: Identity-Preserving Driving World Models for Video Generation by Instance Mask"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ConsisDrive_Identity_Preserving_Driving_World_Models_for_Video_Generation_by_Instance_Mask.pdf
project_link: https://shanpoyang654.github.io/ConsisDrive/page.html
code_link: null
aliases:
- ConsisDrive
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "利用从3D边界框投影出的实例掩码，显式地控制注意力交互和损失空间权重的分配：在注意力模块中引入实例身份掩码和轨迹掩码，阻止不同实例间的信息泄露并强化实例内时间一致性；在损失函数中通过前景掩码和概率动态策略，将监督信号集中在实例区域，同时保持背景生成质量。"
primary_logic: "将标注3D框与跟踪ID转化为结构化的实例掩码，并将其作为硬性先验注入扩散Transformer的注意力和损失计算中，从而将对象一致性约束从场景级提升到实例级，在保持场景真实感的同时大幅减少身份漂移。"
claims:
- "定性对比显示，现有方法DriveDreamer2出现公交车渐变为卡车（类别漂移），MagicDrive‑V2出现车色变化与前景稀释，而ConsisDrive有效保持实例外观一致性。"
- "在nuScenes验证集上，ConsisDrive取得最佳视频生成质量：FVD 37.23，FID 3.88，均优于所有基线方法。"
- "消融实验证实，移除轨迹掩码使FVD恶化16.43、多目标跟踪身份切换增加549，移除身份掩码和损失掩码也会显著降低视频及下游任务表现。"
- "仅使用ConsisDrive生成的数据训练StreamPETR，3D检测mAP达31.5%，为真实数据Oracle性能的91.3%，大幅领先其他生成方法。"
---

# ConsisDrive: Identity-Preserving Driving World Models for Video Generation by Instance Mask

> [!tip] 核心洞察
> 将标注3D框与跟踪ID转化为结构化的实例掩码，并将其作为硬性先验注入扩散Transformer的注意力和损失计算中，从而将对象一致性约束从场景级提升到实例级，在保持场景真实感的同时大幅减少身份漂移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ConsisDrive：基于实例掩码的身份保持驾驶世界模型 |
| 英文题名 | ConsisDrive: Identity-Preserving Driving World Models for Video Generation by Instance Mask |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zgqFQM8VNe) · [Project](https://shanpoyang654.github.io/ConsisDrive/page.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ConsisDrive |
| Dataset | nuScenes (T+I)2V validation set, 3D Detection on generated data (StreamPETR, Gen. only), 3D Perception on generated nuScenes validation (StreamPETR) |

> [!tip] 效果简介
> - nuScenes (T+I)2V validation set 上，FVD↓ 为 37.23，对比 38.06 (InstaDrive)，变化 -0.83。
> - nuScenes (T+I)2V validation set 上，FID↓ 为 3.88，对比 3.96 (InstaDrive)，变化 -0.08。
> - 3D Detection on generated data (StreamPETR, Gen. only) 上，mAP↑ 为 31.5%，对比 34.5% (Oracle on real data)，变化 -3.0% (91.3% of Oracle)。

## 概要

自动驾驶世界模型为端到端规划与仿真提供可控视频生成能力，但现有方法普遍存在**身份漂移**问题：同一目标在连续帧中的类别、颜色或形状发生不可控变化。其根源在于：（1）缺乏显式的实例身份条件；（2）扩散Transformer中的标准3D全注意力不加区分地混合所有实例token，造成跨实例信息泄露；（3）全帧均匀重建损失使背景像素主导梯度，稀释对前景对象身份一致性的监督。

针对上述瓶颈，本文提出 **ConsisDrive**——一种基于实例掩码的身份保持驾驶世界模型。其核心思路是将标注的3D边界框与跟踪ID转化为结构化的*实例掩码*，并将其作为硬性先验分别注入注意力和损失函数：

- **实例掩码注意力（Instance‑Masked Attention, IMA）**：通过实例身份掩码将视觉token的注意力严格限制在同实例的条件嵌入上，阻断跨实例信息交互；同时利用轨迹掩码强化同一实例跨帧token的自注意力，保障时序一致性。
- **实例掩码损失（Instance‑Masked Loss, IML）**：基于实例掩码对覆盖前景对象的token施加更大损失权重，并以概率 $\alpha$ 在掩码损失与全帧损失之间动态切换，在维持背景质量的同时将监督聚焦于关键区域。

在nuScenes验证集上，ConsisDrive取得最佳视频生成质量（FVD 37.23，FID 3.88），显著优于所有对比基线，并有效消除了类别漂移与颜色漂移（Figure 1）。仅使用生成数据训练3D检测器StreamPETR，mAP达31.5%（相当于真实数据Oracle性能的91.3%），多目标跟踪中的身份切换（IDS）从687降至525。消融实验证实，移除轨迹掩码使FVD恶化16.43、IDS增加549，移除身份掩码或损失掩码也显著降低视频及下游任务表现，验证了各模块通过*实例级硬约束*抑制身份漂移的因果作用。ConsisDrive未改变主干生成架构，而是以实例掩码统一范式将身份、轨迹与前景约束显式注入，为实例感知的驾驶世界模型提供了一种轻量而高效的路径。



自动驾驶世界模型通过生成多视角视频，为感知模型提供低成本、可控的合成数据，正成为数据驱动闭环仿真的重要基础。然而，现有方法在生成可控布局视频时普遍面临**实例身份漂移**问题：同一目标在连续帧中，其颜色、形状乃至语义类别发生不受控的变化。如 **Figure 1** 所示，DriveDreamer2 (Zhao et al., 2024) 生成的公交在时间轴上逐渐演变为卡车（类别漂移），MagicDrive‑V2 (Gao et al., 2024b) 则出现车辆颜色不一致与前景目标稀释等现象。这些缺陷严重制约了生成数据在下游感知与跟踪任务中的可用性。

造成身份漂移的根本瓶颈来自三个层面：
1. **实例条件缺失**：现有方法通常仅将布局信息（如3D框投影）作为全局条件注入，缺少对个体实例跟踪ID、外观属性的显式建模，使同一实例在不同帧中无法绑定一致的身份表征。
2. **注意力机制失焦**：扩散Transformer骨干（如MMDiT）采用全注意力设计，所有视觉与条件token可任意交互，导致不同实例间信息泄露，同时缺少对同一实例跨帧时间一致性的强制约束。
3. **监督信号稀释**：训练损失在所有时空像素上均匀计算，背景区域因占比高而主导梯度更新，对前景实例身份的监督信号被严重冲淡，难以驱动模型学习稳定的实例外观。

上述缺口直接催生了本文的核心动机：**将场景级一致性约束提升为实例级一致性约束**。具体而言，ConsisDrive 从标注的3D边界框与跟踪ID中构造结构化**实例掩码**（身份掩码、轨迹掩码、损失掩码），并将其作为硬性先验注入两个关键环节：**实例掩码注意力（IMA）** 通过掩码自注意力显式阻断跨实例交互，同时强化同实例跨帧注意力；**实例掩码损失（IML）** 通过前景掩码将监督信号集中到实例区域，并采用概率动态策略平衡前景一致性与背景生成质量。这一设计旨在以最小结构侵入性，将身份保持能力内化到世界模型的生成过程中，从而在保持场景真实感的同时，大幅抑制身份漂移。



## 核心方法与创新机理

自动驾驶世界模型在视频生成时普遍遭遇**身份漂移**：同一目标在连续帧中可出现类别（公交车→卡车）或外观（车色）变化，其根本原因并非模型容量不足，而是在三个设计层面缺失实例级约束——  
- 扩散 Transformer 的稠密注意力不区分实例，导致跨实例信息泄露（泄漏源）；  
- 模型未获取显式的实例身份条件（如跟踪 ID 与实例尺寸），身份特征只能隐式推断；  
- 均匀的全帧损失使背景像素主导梯度，稀释了对前景实例一致性的监督（监督稀释）。

ConsisDrive 的核心创新在于，将标注 3D 框与跟踪 ID 转化为**三种结构化实例掩码**（身份掩码、轨迹掩码、损失掩码），并将其作为硬性先验同时注入注意力计算与损失函数。该设计将一致性约束从场景级提升至实例级，在不牺牲背景生成质量的前提下，大幅抑制身份漂移。其具体的 **changed slots** 如下：

### 1. 注意力机制：从全帧稠密注意力到实例掩码注意力（IMA）
原始的 MMDiT 全注意力允许所有视觉 token 与条件 token 任意交互，不同实例的信息会混叠。**Instance‑Masked Attention (IMA)** 通过两个互补的掩码矩阵重构注意力拓扑：
- **实例身份掩码**：强制每个视觉 token 仅关注其所属实例的身份条件嵌入，屏蔽其他实例的条件，从而防止类别/外观信息在不同实例间泄漏（`Section 3.2.2`, Equation (2)）。
- **实例轨迹掩码**：确保同一实例在跨帧 token 间可互注意，但禁止不同实例间的时间交互，以此强化实例内在时间一致性。

掩码注意力的输出通过可学习门控 `tanh(ω)` 加回主干网络（`Equation (5)`），使模型平稳适配新约束。**消融证据**（Table 5）：移除轨迹掩码后 FVD 恶化 16.43，多目标跟踪身份切换（IDS）暴增 549；移除身份掩码后不仅 FVD/FID 上升，且发生类别漂移（交通锥→行人，Figure 3）。这直接证明掩码注意力是抑制身份漂移的因果性关键。

### 2. 实例身份注入方式：从无显式条件到全局身份嵌入
多数基线方法仅用 3D 框投影作为布局指导，未赋予模型实例的持久身份信息。ConsisDrive 为每个实例构建**全局身份条件嵌入** `g_i`：
$$g_{i} = \mathbb{MLP}([\tau_{\theta}(c_{i}), \gamma(s_{i}), \gamma(ID_{i})])$$
（类别 `c_i`、3D 尺寸 `s_i`、跟踪 `ID_i` 经嵌入与 MLP 融合，见 `Equation (1)`）。该嵌入随后在 IMA 模块中与视觉 token 进行掩码绑定，确保同一实例在全部生成帧中获得一致的身份信号。实验间接证明：使用 ConsisDrive 生成数据训练下游 StreamPETR 时，3D 检测 mAP 达 31.5%（真实数据 Oracle 的 91.3%，Table 2），大幅领先其他生成方法，说明身份属性被准确绑定于视觉生成中。

### 3. 训练损失权重分配：从均匀全帧损失到实例掩码概率动态损失
标准 DDPM 损失赋予所有像素同等权重，前景（尤其小目标）的监督信号被背景淹没。**Instance‑Masked Loss (IML)** 利用二值前景掩码（由 token 到实例指示函数构建，覆盖至少一个实例的区域）对损失施加权重，同时引入概率动态策略：
$$\tilde{\mathcal{L}}_{\mathrm{mask}} = \begin{cases} \mathcal{L}_{\mathrm{mask}}, & \text{if } p < \alpha \\ \mathcal{L}, & \text{otherwise} \end{cases}$$
即以概率 $\alpha$ 选用前景聚焦的掩码损失，其余步骤使用标准全帧损失（`Equation (6)`）。该策略平衡了两者：掩码损失强化前景身份一致性，全帧损失防止背景退化。**消融证据**（Table 5）：完全移除该损失（w/o CML）导致感知 NDS 下降 4.53、IDS 增加 112，验证了前景监督对下游任务身份保持的必要性。

**综合效果**：上述两个 changed slots 协同作用，使 ConsisDrive 在 nuScenes 验证集上取得当时最佳的视频生成保真度（FVD 37.23，FID 3.88），并在单纯用生成数据训练的 3D 感知与多目标跟踪任务中大幅降低身份切换（IDS 从 687 降至 525），实现了实例级的时间一致性闭环。



![[assets/figures/papers/iclr26_0014_zgqFQM8VNe_ConsisDrive_Identity-Preserving_Driving_World_Mo/figures/004_Figure_2.jpg]]
*Figure 2: Overview. (a) Instance-Masked Attention, which explicitly directs the model’s attention to each individual instance by incorporating both an instance identity mask and trajectory mask. (b) Instance-Masked Loss Supervision, a probabilistic instance-focused training objective that employs instance loss masks to emphasize supervision on foreground regions. (c) Instance Mask Construction. Illustration of how the Instance Identity Mask, Instance Trajectory Mask, and Instance Loss Mask are constructed from 3D box projections*

ConsisDrive 的整体架构围绕一个基于扩散 Transformer 的去噪骨干展开，并引入了三个关键组件以显式施加实例级时间一致性约束：**实例身份条件提取**、**实例掩码注意力（Instance‑Masked Attention, IMA）** 以及 **实例掩码损失（Instance‑Masked Loss, IML）**，整体结构如图 2 所示。

### 条件编码与去噪骨干
模型以文本描述、道路地图以及包含类别、跟踪 ID 与尺寸的实例 3D 边界框作为输入。首先通过一个 ControlNet 将布局条件（3D 框投影、地图）注入去噪骨干；骨干基于 OpenSora V2.0 的 Video DC‑AE 和 T5/CLIP 编码器执行多视图视频的扩散生成（Section 3.1）。这一流程提供了场景级的结构控制，但本身无法区分不同实例的身份，容易导致跨帧的外观漂移（Figure 1）。

### 实例身份条件提取
为赋予模型实例级的身份感知能力，对每一个出现在视频中的实例 $i$，将其类别标签 $c_i$、3D 框尺寸 $s_i$ 和跟踪 ID 通过嵌入与 MLP 融合为全局身份条件嵌入：

$$
g_{i} = \mathbb{MLP}([\tau_{\theta}(c_{i}), \gamma(s_{i}), \gamma(ID_{i})]). \tag{1}
$$

该嵌入作为实例的“身份签名”，将与视觉 token 一同送入后续的掩码注意力模块，从而将身份信息绑定到每一个目标实例。

### 实例掩码注意力 (IMA)
在去噪骨干的 MMDiT 副本块之后，插入实例掩码注意力模块。其核心是利用从 3D 边界框投影构建的**实例身份掩码**和**实例轨迹掩码**来显式控制 token 间的交互（Figure 2 (a)(c)）。

具体而言，设视觉 token 集合为 $V$，实例身份条件 token 集合为 $G=\{g_i\}$，在拼接后的序列 $[V, G]$ 上执行掩码自注意力：

$$
\tilde{V} = \mathrm{SA}_{\mathrm{mask}}([V, G]). \tag{2}
$$

注意力掩码 $M$ 的构建规则如下：将 3D 框角点通过相机内外参投影到 2D 图像平面（Equation (3)），若某个视觉 token $v_k$ 落在某实例的投影区域中，则将其归属给该实例；令 $I(v_k)$ 返回所有覆盖此 token 的实例 ID 集合（Equation (4)）。掩码要求只有当两个 token 属于同一实例（$I(v_k) \cap I(v_j) \ne \varnothing$）时才允许注意力交互，否则将该连接置为 $-\infty$。这一机制**阻止了不同实例间的信息泄露**，同时**保证了同一实例内跨帧 token 的互相关注**（即轨迹掩码），从而在时间维度上维护实例身份的一致性。

掩码注意力的输出通过一个可学习的门控标量 $\omega$（初始化为 0）以残差方式加回主干：

$$
V = V + \tanh(\omega) \tilde{V}[:m], \tag{5}
$$

使得模型可以在训练初期绕过新模块，逐步学会利用实例级别的注意力约束。

### 实例掩码损失 (IML)
均匀的全帧重建损失会导致背景像素主导梯度，稀释对前景对象的监督，进而引发身份漂移。IML 根据投影得到的实例区域构建一个二值损失掩码 $M_{\mathrm{Loss}}$，对覆盖至少一个实例的 token 施加更大的损失权重，而纯背景区域的权重为零（Section 3.3）。为进一步防止前景过拟合并保留背景生成质量，采用概率动态切换策略：以概率 $\alpha$ 使用掩码损失 $\mathcal{L}_{\mathrm{mask}}$，否则使用标准全帧损失 $\mathcal{L}$：

$$
\tilde{\mathcal{L}}_{\mathrm{mask}} =
\begin{cases}
\mathcal{L}_{\mathrm{mask}}, & \text{if } p < \alpha \\
\mathcal{L}, & \text{if } p \ge \alpha
\end{cases} \tag{6}
$$

这一策略在**强化实例外观一致性**与**维持整体场景真实感**之间取得了动态平衡。

### 整体数据流与关键设计差异
从前向流程看，模型的输入‑输出关系为：**文本/地图/3D 实例框 → ControlNet 条件编码 → MMDiT 去噪骨干 → IMA 掩码注意力注入 → 视频预测；训练时额外施加 IML 损失进行监督**。与现有驾驶世界模型（如 DriveDreamer2、MagicDrive‑V2 等）相比，ConsisDrive 的关键改变集中于三个设计槽位：  
1. **注意力机制**：从无约束的全注意力变为实例掩码注意力，仅允许同实例 token 与对应身份条件交互，截断跨实例信息流。  
2. **实例身份注入**：从无显式实例条件到为每个实例构建全局身份嵌入（类别+ID+尺寸），并通过掩码注意力绑定。  
3. **损失权重分配**：从均一全帧损失变为基于实例掩码的动态加权损失，使监督信号向前景实例集中。

这些设计共同将身份一致性约束从场景级提升至实例级，从而在可控性与生成质量之间取得了显著平衡。



ConsisDrive 在 MM-Diffusion Transformer (MMDiT) 骨干上引入两个核心模块，从根本上解决身份漂移：**Instance‑Masked Attention (IMA)** 模块显式约束自注意力的交互范围，阻止不同实例间的信息泄漏；**Instance‑Masked Loss (IML)** 模块将重建损失集中到前景实例区域，避免背景像素主导梯度。两个模块均依赖从 3D 边界框与跟踪 ID 导出的结构化掩码，构造过程如图 2(c) 所示。

### 实例身份条件建模

为使模型分辨不同实例的持久身份，ConsisDrive 为每个实例构建一个**全局身份条件嵌入** $g_i$：

$$
g_{i} = \operatorname{MLP}\bigl([\tau_{\theta}(c_{i}),\; \gamma(s_{i}),\; \gamma(ID_{i})]\bigr) \tag{1}
$$

其中 $c_i$ 为实例类别标签（经文本编码器 $\tau_\theta$ 得到文本嵌入），$s_i$ 为 3D 边框尺寸 (l, w, h)，$ID_i$ 为该实例在序列中的唯一跟踪 ID；$\gamma(\cdot)$ 表示正弦余弦位置编码。所有实例条件嵌入叠成全局条件矩阵 $G \in \mathbb{R}^{n\times d}$，供后续掩码注意力使用。

### Instance‑Masked Attention (IMA)

IMA 模块穿插在 MMDiT 的每个副本块之后。设视频去噪网络中某一层的视觉 token 为 $V \in \mathbb{R}^{m\times d}$，拼接全局条件 $G$ 后执行**掩码自注意力**：

$$
\tilde{V} = \operatorname{SA}_{\text{mask}}([V, G]) \tag{2}
$$

注意力掩码 $M \in \{0, -\infty\}^{(m+n)\times (m+n)}$ 通过两种二进制掩码构造：

1. **实例身份掩码**：控制视觉 token 只与其所属实例的条件 token 交互。定义指示器函数 $I(v_k)$，返回视觉 token $v_k$ (对应时空位置 $(t, p)$) 所覆盖的全部实例 ID：

   
$$
I(v_k) \equiv I(t, p) = \{ i \mid \exists (x, y),\; \tilde{BM}_i(t, x, y) = 1 \} \tag{4}
$$

   其中 $\tilde{BM}_i$ 是实例 $i$ 的 2D 二值掩码，由 3D 框角点投影得到：

   
$$
\tilde{\mathbf{x}}_{i,c}^{t} = \mathbf{K}^{t}(\mathbf{R}^{t}\mathbf{X}_{i,c} + \mathbf{T}^{t}),\quad
   \mathbf{x}_{i,c}^{t} = \bigl(\frac{\tilde{x}}{\tilde{z}}, \frac{\tilde{y}}{\tilde{z}}\bigr) \tag{3}
$$

   若 $I(v_k) \cap I(v_j) = \varnothing$，则对应的注意力值被置为 $-\infty$，彻底阻断跨实例信息流动。

2. **轨迹掩码**：进一步保证同一实例在不同帧的视觉 token 能够相互关注，而不同实例的 token 即使在相邻帧也不得交互。该掩码结合帧索引与实例 ID，形成实例内的时序通路。

经过掩码注意力后的前端 $m$ 个 token $\tilde{V}[:m]$ 通过可学习的门控机制加回到 backbone 表示：

$$
V = V + \tanh(\omega)\;\tilde{V}[:m] \tag{5}
$$

标量参数 $\omega$ 初始化为 0，使 IMA 从恒等映射逐渐增强，稳定训练。

### Instance‑Masked Loss (IML)

标准的全帧扩散损失 $\mathcal{L}$ 对每个像素等权监督，导致大量背景像素稀释前景实例的梯度。ConsisDrive 构建**实例损失掩码** $M_{\text{Loss}} \in \{0,1\}^{\tilde{T}_{\text{comp}} \times H_{\text{comp}} \times W_{\text{comp}}}$：若某时空位置被至少一个实例掩码覆盖，对应元素为 1，否则为 0。据此计算前景聚焦的掩码损失 $\mathcal{L}_{\text{mask}} = M_{\text{Loss}} \odot \mathcal{L}$。

为避免过度前景拟合损害背景泛化，训练时采用**概率动态掩码策略**：

$$
\tilde{\mathcal{L}}_{\text{mask}} = 
\begin{cases}
\mathcal{L}_{\text{mask}}, & \text{if } p < \alpha \\
\mathcal{L}, & \text{if } p \geq \alpha
\end{cases} \tag{6}
$$

每一步从均匀分布采样概率 $p$，以概率 $\alpha$ 使用掩码损失，否则使用标准全帧损失。此机制在强化实例一致性与保持场景真实感之间取得平衡。

上述模块协同工作，将对象一致性约束从场景级提升到实例级：IMA 从注意力层面阻止语义与颜色信息的跨实例混淆，IML 从监督层面将梯度聚焦于关键前景区域。消融实验证实，移除身份掩码导致类别漂移（交通锥变为行人），移除轨迹掩码则引起颜色漂移和 FVD 恶化 16.43，证实两个组件的独立作用与互补性 (Table 5, Figure 3)。



## 实验与关键发现

### 主结果：视频生成质量与下游任务增益

ConsisDrive 在 nuScenes 验证集上取得了领先的视频生成质量，并在多项下游感知与跟踪任务中展现出显著的数据增强效果。定量结果分为三组：视频保真度、感知任务收益及数据驱动的多目标跟踪改进。

**视觉与时间保真度**（表1）表明，ConsisDrive 在自动驾驶世界模型中达到了最优的 FVD 37.23 和 FID 3.88，均优于包括 InstaDrive 在内的所有基线。FVD 的低值归因于实例掩码注意力（IMA）中的轨迹掩码，它显式地约束了同一实例的跨帧 token 交互，从而抑制了时序身份漂移。FID 的改善则源于损失掩码对前景区域的集中监督，避免了背景像素对梯度的稀释。

![[assets/figures/papers/iclr26_0014_zgqFQM8VNe_ConsisDrive_Identity-Preserving_Driving_World_Mo/figures/005_Table_1.jpg]]
*Table 1: Visual and Temporal Fidelity: Comparison with SoTA methods on nuScenes validation set*

**3D 检测与感知增强**：将 ConsisDrive 生成的数据直接用于训练下游检测器 StreamPETR，mAP 达到 31.5%（即 Oracle 真实数据性能的 91.3%，表2），显著超越其他合成数据增强方法。在生成验证集上直接评估预训练 StreamPETR 时，NDS 提升至 41.38（表3），表明模型不仅能生成高保真画面，还能准确绑定实例的类别、尺寸和位置等属性，使得生成数据中的实例属性与真实标注保持一致，可直接被感知模型利用。

![[assets/figures/papers/iclr26_0014_zgqFQM8VNe_ConsisDrive_Identity-Preserving_Driving_World_Mo/figures/006_Table_2.jpg]]
*Table 2: Comparison on perception tasks with Panacea. Training StreamPETR with synthetic data augmentation leads to significant performance improvements, highlighting the value of generated data for perception*

**多目标跟踪身份保持**：在数据增强实验中（表4），结合真实数据与 ConsisDrive 生成数据训练跟踪器，身份切换（IDS）从 687 降至 525，降幅达 162。这一改善直接印证了轨迹掩码强制同一实例跨帧具备一致身份的有效性，进一步验证了因果枢纽——通过实例掩码切断跨实例注意力、同时强化实例内时序交互——能够从场景级一致性提升到实例级一致性。

![[assets/figures/papers/iclr26_0014_zgqFQM8VNe_ConsisDrive_Identity-Preserving_Driving_World_Mo/figures/008_Table_4.jpg]]
*Table 4: Comparison involving data augmentation using synthetic data on multi object tracking*

### 消融实验：实例掩码注意力的结构分解

为量化各模块的贡献，论文在 nuScenes (T+I)2V 设定下进行了三项消融（表5，图3）。

![[assets/figures/papers/iclr26_0014_zgqFQM8VNe_ConsisDrive_Identity-Preserving_Driving_World_Mo/figures/009_Table_5.jpg]]
*Table 5: Ablation study results in (T+I)2V scenarios on the nuScenes validation set*

- **移除实例身份掩码（w/o IMA(Identity)）**：FVD 恶化 3.66，FID 上升 1.41，并出现类别混淆（如交通锥渲染为蹲姿行人，图3a）。这表明身份掩码作为视觉 token 与实例类别、ID 条件之间的硬约束，直接阻止了跨实例的信息泄露，是类别一致性的关键。
- **移除轨迹掩码（w/o IMA(Trajectory)）**：造成最严重的性能退化：FVD 急剧上升 16.43，多目标跟踪中 IDS 增加 549。轨迹掩码确保同一实例在各帧的 token 关注彼此，缺失后颜色漂移（图3b）和身份断裂频发，确证了该掩码是跨帧身份保持的因果性设计。
- **移除实例掩码损失（w/o CML，即 IML 组件）**：导致感知 NDS 下降 4.53，IDS 增加 112。这证实了将损失监督集中在前景实例上对下游任务至关重要，且概率动态策略（以概率 α 在掩码损失与全帧损失间切换）在保持背景质量与强化前景一致性之间取得了平衡。

### 定性分析与失败模式

图1 的定性对比清晰展示了现有方法的身份漂移瓶颈：DriveDreamer2 中公交车渐变为卡车（类别漂移），MagicDrive-V2 中车辆颜色跨帧变化（外观漂移）及前景稀释导致小目标如行人消失。ConsisDrive 通过实例级显式约束有效解决了这些缺陷，在相同场景下保持目标类别、颜色和尺寸的一致性。

![[assets/figures/papers/iclr26_0014_zgqFQM8VNe_ConsisDrive_Identity-Preserving_Driving_World_Mo/figures/003_Figure_1.jpg]]
*Figure 1: Limitations of Prior Works in Instance Identity Preservation Across Frames. (a) Category Shift: In DriveDreamer2 Zhao et al. (2024), the bus gradually turns into a truck, indicating a failure to preserve semantic identity over time. (b) Color Shift: In MagicDrive-V2 Gao et al. (2024b), the car’s color changes inconsistently across frames, violating temporal appearance consistency. (b) Foreground Dilution: In MagicDrive-V2 Gao et al. (2024b), scene-level supervision dilutes supervision over critical foreground regions, breaking temporal identity consistency for small instances like pedestrians. In contrast, our method explicitly enforces instance-level temporal constraints, maintaining consi...*

论文未提供 ConsisDrive 自身的失败案例，但提出的开放问题暗示了潜在局限：拥挤场景中严格禁止跨实例注意力可能丢失有益的上文关联；概率掩码损失的超参数 α 需要手工调节，自动选择机制尚未探索；可学习门控参数 ω 的优化特性对极端场景的适应性有待验证。这些点建议手动验证，当前结论均基于 nuScenes 干净标注场景，复杂多遮挡场景的性能需结合实际测试评估。



## 定位与知识库关联

自动驾驶世界模型的视频生成研究沿着“布局可控 → 场景多样性 → 实例级一致性”的脉络演进。早期工作 BEVControl、DriveDiffusion 将鸟瞰图或中心线布局作为控制条件，实现了多视图画面的空间对齐，但对时间维度的保真度关注有限。随后，DriveDreamer2 引入大语言模型增强轨迹多样性，Panacea 与 UniMLVG 支持全景或统一多视图长视频生成，MagicDrive‑V2 通过自适应控制进一步提升了分辨率与时长。然而，这些方法普遍依赖**场景级均匀训练信号**，在视频扩散过程中缺乏对目标个体身份的显式约束，导致同一物体在连续帧中出现类别混淆（例如公交车渐变为卡车）、颜色漂移或前景目标“稀释”等身份漂移现象（Figure 1）。ConsisDrive 正是在这一瓶颈处切入，将研究方向从场景级保真推向**实例感知的身份保持**，与同期工作 InstaDrive 共同属于该分支。其核心差异在于：ConsisDrive 不单借助实例条件注入，更将 3D 边界框与跟踪 ID 转化为三种结构化的实例掩码，作为硬性先验重写扩散 Transformer 的注意力交互与损失空间，从而使身份一致性约束由场景级精细化至实例级。

### 与基线／同期方法的关系

ConsisDrive 与主流方法的差异集中体现在**显式的实例掩码注意力与实例掩码损失**上。在基线方法 MagicDrive‑V2、DriveDreamer2 中，扩散 Transformer 通常采用全注意力机制，所有视觉 token 可以不加区分地互相关注，导致不同实例间的信息泄露；同时，训练损失对所有像素等权计算，背景像素数量占优，稀释了本应聚焦前景的监督信号。ConsisDrive 通过实例身份掩码限制视觉 token 仅与其自身实例的全局身份条件交互，并通过轨迹掩码保证同一实例跨帧 token 相互关注，从而在注意力层面彻底阻断跨实例信息泄露（Section 3.2）。在损失层面，根据实例掩码对前景区域施加更大权重，并采用概率 α 在掩码损失与全帧损失之间动态切换，避免前景过拟合（Section 3.3）。定量结果印证了这一设计：在 nuScenes 验证集上，ConsisDrive 取得 FVD 37.23、FID 3.88，优于所有对比方法（Table 1）。定性对比亦显示，DriveDreamer2 出现公交车变卡车（类别漂移），MagicDrive‑V2 出现车色变化与前景稀释，而 ConsisDrive 有效保持了实例外观与类别的一致性（Figure 1）。

与同期工作 InstaDrive 相比，两者虽同属实例感知路线，但实现方式不同：InstaDrive 更多地通过在 token 层面引入实例 ID 嵌入，而 ConsisDrive 进一步构造了轨迹掩码与实例损失掩码。数据显示 ConsisDrive 在 FVD（37.23 vs 38.06）和 FID（3.88 vs 3.96）上均略有领先（Table 1）。尤其值得关注的是，当移除轨迹掩码时，FVD 恶化 16.43，多目标跟踪的 ID switch 激增 549；移除实例掩码损失则使感知 NDS 下降 4.53（Table 5），表明这些组件对跨帧身份保持具有决定性作用，且不易被同期工作所替代。

在下游任务数据增强方面，ConsisDrive 生成的视频对感知模型训练的价值显著超越先前方法。仅用生成数据训练 StreamPETR 时，3D 检测 mAP 达 31.5%，达到真实数据 Oracle 性能的 91.3%（Table 2），大幅领先 Panacea 等模型。在多目标跟踪任务中，使用 ConsisDrive 增强数据可使 ID switch 从 687 降至 525（Table 4），再次证明其绑定的实例属性（类别、ID、尺寸）在物理仿真中高度可靠。

### 适用边界

ConsisDrive 的有效性建立在精确的 **3D 边界框与跟踪 ID 标注**之上，这决定了其应用场景目前主要限定于像 nuScenes 这样具备全息感知标注的数据集。对于缺失实例级标注或仅有弱监督信号的环境（如众包街景或无标签视频），方法将无法直接迁移。同时，现有实验仅覆盖 nuScenes 验证集，对天气、地域、道路结构变化较大的其他驾驶数据集（如 Waymo、Argoverse）的泛化能力尚未检验，需谨慎外推。

从架构角度，额外的实例掩码注意力分支与掩码损失计算会引入一定的训练和推理开销。在需要实时应用（如车载在线仿真）时，当前模型规模可能构成瓶颈。此外，硬性禁止跨实例注意力在高度拥挤、交互频繁的交通场景下是否会导致合理的信息交互被切断，亦尚未探索：完全隔离的策略可能削弱模型对遮挡、穿插等复杂空间关系的建模。最后，方法目前仅针对**驾驶视频生成**设计，其核心思想——利用几何投影构建掩码约束注意力与损失——能否直接泛化至通用视频生成或其他领域的对象一致性任务，仍有待验证。

### 局限与开放问题

围绕上述适用边界，以下开放问题需要进一步研究：

1. **动态掩码概率 α 的敏感性与自适应选择**。当前 α 为固定概率，但其最优值可能随训练阶段、场景复杂度变化；如何自动调节 α 以平衡前景一致性与背景质量，是一个尚未探索的超参数问题。
2. **门控参数 ω 的作用机制**。式 (5) 中通过 $\tanh(\omega)$ 将掩码注意力输出加回骨干网络，ω 初始化为零。该门控在训练过程中的演化如何影响收敛稳定性与最终视频质量，以及是否存在更优的初始化或调度策略，尚需厘清。
3. **严格禁止跨实例注意力的边界**。当前掩码策略完全切除不同实例间的注意力连接，这在稀疏场景下高效合理，但在密集交通或大量遮挡情形下，是否需要引入可学习的自适应掩码或部分连接（如允许同类别实例共享信息），是一个关键设计问题。
4. **跨领域泛化能力**。方法强依赖 3D 框投影与跟踪 ID，脱离自动驾驶感知标注体系后，掩码构建框架需重新设计。如何将该范式迁移至人体动作、运动比赛等对象的身份保持生成，尚未有任何验证。
5. **长序列与大规模实例的可扩展性**。论文中视频帧数和实例数受限于现有计算资源，随着序列增长，掩码注意力的计算复杂度上升，且身份保持的难度可能非线性增加，需要进一步分析并优化架构。

上述局限和问题表明，ConsisDrive 在实例级身份保持的自动驾驶世界模型方向上迈出了重要一步，但其设计假设与通用性仍有广阔的探索空间，为后续工作给出了清晰的研究脉络。



## 原文 PDF

![[paperPDFs/ICLR_2026/ConsisDrive_Identity_Preserving_Driving_World_Models_for_Video_Generation_by_Instance_Mask.pdf]]
