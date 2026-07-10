---
title: Hogel-free Holography
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Hogel_free_Holography.pdf
project_link: null
code_link: null
aliases:
- MNAFM
- HFH
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 引入基于Conformer的视觉-声学融合模块（交叉注意力机制）和具有可学习间距的扩张卷积（DCLS）的自适应门控合成模块，使模型能隐式地从视觉特征中推断场景的材料声学属性，并将声音传播分解为混响（从视觉获得）和直达声/早期反射（从位姿条件化），从而实现跨环境的逼真空间音频合成。
primary_logic: 通过将音频合成解耦为两个阶段——先由视觉-声学融合网络捕获几何与材料驱动的全局混响特性，再基于听者与声源的相对位姿动态生成直达声和局部反射——并利用视觉特征作为材料属性的代理，模型能够在新环境中仅凭稀疏录音和图像合成具有高度真实感和空间一致性的音频。
claims:
- Conformer与自适应卷积对合成和真实数据上的音频合成质量都有显著且一致的提升
- 主观用户研究表明，MNAF在VR和AR环境中提供了比基线方法更好的沉浸感和真实感
- SoundSpaces Same Environment 上 Mag↓, LRE↓, RTE↓ = 0.134
- SoundSpaces Same Environment 上 Mag↓, LRE↓, RTE↓ = 1.151
---

# Hogel-free Holography

> [!tip] 核心洞察
> 通过将音频合成解耦为两个阶段——先由视觉-声学融合网络捕获几何与材料驱动的全局混响特性，再基于听者与声源的相对位姿动态生成直达声和局部反射——并利用视觉特征作为材料属性的代理，模型能够在新环境中仅凭稀疏录音和图像合成具有高度真实感和空间一致性的音频。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向沉浸式混合现实的多模态神经声场 |
| 英文题名 | Hogel-free Holography |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://www.cs.unc.edu/~cpk/) |
| Topic | #topic/other_unclear |
| Method | Multimodal Neural Acoustic Fields (MNAF) |
| Dataset | SoundSpaces Same Environment, SoundSpaces Novel Environment, Replay, EnvSound |

> [!tip] 效果简介
> - SoundSpaces Same Environment 上，Mag↓, LRE↓, RTE↓ 0.134；Mag↓, LRE↓, RTE↓ 1.151；Mag↓, LRE↓, RTE↓ 0.034。
> - SoundSpaces Novel Environment 上，Mag↓, LRE↓, RTE↓ 0.186；Mag↓, LRE↓, RTE↓ 1.125；Mag↓, LRE↓, RTE↓ 0.034。
> - Replay (Real-world) 上，STFT Mag 0.142。

## 概要

现有空间音频渲染方法难以从稀疏的视觉-听觉传感器数据中学习场景声学特性并泛化至新环境，且常依赖简化物理模型，无法有效利用视觉线索推断材料对声音传播的影响。本文提出**多模态神经声场（MNAF）**，通过两阶段框架实现跨环境的逼真空间音频合成：首先由基于Conformer的视觉-声学融合模块从图像中隐式捕获几何与材料驱动的全局混响特性，再由集成可学习间距扩张卷积（DCLS）的自适应门控合成模块根据听者与声源的相对位姿动态生成直达声与局部反射。在合成数据集（SoundSpaces）和真实数据集（Replay、EnvSound）上，MNAF在STFT幅度、左右比误差（LRE）、混响时间误差（RTE）等指标上均优于ViGAS等基线方法。消融实验证实Conformer与自适应卷积对性能有显著且一致的贡献。主观用户研究表明，MNAF在VR和AR环境中显著提升了沉浸感（VR中p=0.002）与真实感，且合成音质与参考音频无显著差异（p=0.189），而基线方法则显著差于参考（p=0.006）。该方法定位为基于学习的多模态新视角声学合成，核心创新在于将音频合成解耦为视觉驱动的混响建模与位姿条件化的波形生成。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有空间音频渲染方法面临一个根本性瓶颈：**难以从稀疏的视觉-听觉传感器数据中学习场景的声学特性（尤其是混响），并将其泛化到新视角或完全未见的环境**。传统方法往往依赖简化的物理模型或显式3D网格，无法有效捕获视觉线索提供的材料属性对声音传播的影响——例如，从一张RGB图像中推断墙壁是混凝土还是木材，这对混响特性至关重要。这导致合成音频缺乏沉浸感，无法在混合现实场景中提供可信的空间听觉体验。

MNAF的核心洞察在于**将音频合成解耦为两个阶段**：首先由视觉-声学融合网络捕获几何与材料驱动的全局混响特性，再基于听者与声源的相对位姿动态生成直达声和局部反射。这一设计的关键在于**利用视觉特征作为材料属性的隐式代理**，使模型能够在新环境中仅凭稀疏录音和图像合成具有高度真实感和空间一致性的音频。

### 问题形式化与两阶段合成框架

给定源视角的音频 $A_S$、RGB图像 $V_S$、声源位姿 $P_S$ 和目标听者位姿 $P_R$，MNAF学习一个映射函数：

$$f : \left( A _ { S } , V _ { S } , P _ { S } , P _ { R } ; E \right) \mapsto A _ { R }$$

其中 $E$ 表示环境上下文，$A_R$ 为目标双耳音频。该映射被分解为两阶段过程：

$$A _ { R } = f _ { \mathrm { A S } } \left( f _ { \mathrm { V A F } _ { E _ { R } } } ( A _ { S } , V _ { S } ; E _ { S } ) , P _ { S } , P _ { R } ; E _ { R } \right)$$

**第一阶段（视觉-声学融合，VAF）**：从源音频和视觉数据中学习房间的隐式声学表征，主要捕获高阶反射和混响——这些特性由场景几何和材料决定，与听者具体位置无关。**第二阶段（声学合成，AS）**：以上述混响表征为基础，条件化于声源和听者的相对位姿，动态生成直达声和早期反射，实现空间化的双耳音频输出。

### Changed Slot 1：视觉-声学融合方式——从简单拼接到交叉注意力Conformer

**基线方案（ViGAS, Chen et al., CVPR 2023）** 采用简单拼接视觉特征和坐标特征的方式，缺乏对音视频时间相关性的显式建模。MNAF将其替换为**基于交叉注意力机制的堆叠式Conformer网络**，这是第一个关键创新点。

Conformer编码器的输入包括源音频 $A_S$ 和从预训练ResNet18提取的视觉特征 $\mathcal{V}_F$。其核心操作是交叉模态注意力：

$$\mathcal { F } _ { \mathrm { c m } } ( A _ { S } , \mathcal { V } _ { F } ) = \mathrm { s o f t m a x } \left( \frac { A _ { S } \mathcal { V } _ { F } ^ { T } } { \sqrt { H } } \right) \mathcal { V } _ { F }$$

该机制使音频特征能够**主动查询视觉特征空间中与声学相关的区域**——例如，模型可以学会关注图像中的墙壁、地板等反射面，从而推断混响特性。Conformer的堆叠结构进一步通过自注意力层捕获长程时间依赖，最终输出隐式房间声学表征：

$$\mathcal { C } = \mathrm { C o n f o r m e r } ( A _ { S } , V _ { S } )$$

这一表征 $\mathcal{C}$ 编码了场景的几何和材料属性对声音传播的影响。随后，$\mathcal{C}$ 经上采样后与源音频特征融合：

$$M = \mathrm { F u s i o n } ( \hat { C } , \hat { A _ { S } } )$$

融合结果 $M$ 作为第二阶段的输入，携带了完整的混响信息。

**因果链路**：Conformer的交叉注意力机制使模型能够从视觉数据中隐式学习材料声学属性 → 生成的 $\mathcal{C}$ 捕获了场景的混响特性 → 这为后续的位姿条件化合成提供了准确的声学基础。消融实验（Table 2, Table 3）证实，将Conformer替换为简单拼接会导致RTE从0.034升至0.037（合成数据）和整体性能下降（真实数据），验证了该模块的因果贡献。

### Changed Slot 2：声学合成卷积类型——从固定扩张到可学习间距扩张卷积（DCLS）

**基线方案** 在波形合成网络中使用固定扩张率的1D标准卷积。MNAF将其替换为**具有可学习间距的扩张卷积（DCLS）并结合门控自适应层**，这是第二个关键创新点。

声学合成解码器由多个门控自适应层堆叠而成，每层的形式为：

$$x ^ { k } = \operatorname { t a n h } \left( u _ { A } ^ { k } ( M _ { R } ^ { k - 1 } ) + u _ { V } ^ { k } ( \hat { z } ) \right) \odot \sigma \left( \nu _ { A } ^ { k } ( M _ { R } ^ { k - 1 } ) + \nu _ { V } ^ { k } ( \hat { z } ) \right)$$

其中 $\hat{z}$ 是声源和听者位姿经MLP编码后的位置特征，$M_R^{k-1}$ 是前一层的音频特征。该门控机制通过tanh分支提供非线性变换，sigmoid分支作为门控信号，**动态调节位置信息对音频特征的影响程度**——这使模型能够根据相对位姿自适应地决定何时加强直达声、何时保留混响。

在这些门控层中，MNAF集成了DCLS。标准扩张卷积的扩张率是固定的，限制了感受野的灵活性。DCLS将卷积核的每个元素视为具有**可学习位置**的参数：

$$F : \mathbf { w } , \mathbf { p } \mapsto K = \sum _ { i = 1 } ^ { m } f ( w _ { i } , p _ { i } )$$

其中 $w_i$ 是可学习权重，$p_i$ 是可学习位置。当位置为分数时，通过线性插值得到最终的核元素：

$$K _ { \ell } = { \left\{ \begin{array} { l l } { w ( 1 - r ) } & { { \mathrm { ~ i f ~ } } \ell = \lfloor p \rfloor } \\ { w r } & { { \mathrm { ~ i f ~ } } \ell = \lfloor p \rfloor + 1 } \end{array} \right. }$$

**因果链路**：门控自适应层根据位姿动态调节音视频特征与位置信息的融合比例 → DCLS提供灵活的感受野，使网络能够学习最优的时间跨度来建模不同延迟的反射路径 → 两者协同使合成音频在直达声和反射之间实现平滑过渡。消融实验（Table 2）显示，去掉自适应卷积后STFT幅度误差从0.134升至0.150，LRE从1.151升至1.260；在真实数据（Table 3）上LRE从0.664升至0.804，证实了该模块的因果贡献。

### 模块顺序与训练/推理路径

**训练路径**：
1. **视觉特征提取**：预训练ResNet18从源视角RGB图像提取视觉特征 $\mathcal{V}_F$
2. **Conformer编码**：堆叠式Conformer通过自注意力和交叉注意力处理 $(A_S, V_S)$，输出隐式房间声学表征 $\mathcal{C}$
3. **特征融合**：上采样后的 $\hat{C}$ 与 $\hat{A}_S$ 拼接融合为 $M$
4. **位置编码**：声源位姿 $P_S$ 和听者位姿 $P_R$ 经MLP编码为 $\hat{z}$
5. **声学合成解码**：多个门控自适应层（集成DCLS）以 $M$ 和 $\hat{z}$ 为输入，逐层生成目标音频
6. **损失计算**：使用STFT幅度损失和立体声平衡损失进行优化

$$L _ { \mathrm { m a g } } = \left| \left| \mathrm { S T F T } ( \hat { A } _ { R } ) \right| - \left| \mathrm { S T F T } ( A ) \right| \right|$$

$$L _ { \mathrm { t o t a l \_ l o s s } } = L _ { \mathrm { m a g } } + \alpha L _ { \mathrm { s t e r e o } }$$

训练配置：ADAM优化器（β1=0.9, β2=0.999），学习率5e-4，α=0.02，10个epoch。

**推理路径**：与训练路径相同，但不需要真实音频 $A_R$ 参与损失计算。给定新环境的源音频和单张RGB图像，模型即可合成任意听者位置的双耳音频。

### 模块间因果关系总结

Conformer编码器（VAF阶段）负责从视觉数据中提取**位姿无关的全局声学特性**（主要是混响），这是后续空间化的基础。声学合成解码器（AS阶段）在此基础上引入**位姿相关的局部声学效果**（直达声和早期反射），通过门控机制和DCLS实现动态调节。两阶段的因果分离使模型能够：
- 在新环境中仅需少量视觉数据即可推断混响特性
- 对未见过的听者位置进行泛化，因为直达声的生成仅依赖相对位姿
- 通过视觉特征隐式学习材料属性，无需显式物理建模

这一设计从根本上解决了“从稀疏传感器数据学习场景声学并泛化到新环境”的瓶颈问题。

![[assets/figures/papers/paper_list_l3_https_www_cs_unc_edu_cpk/figures/001_Figure.jpg]]
*Figure: Remote Concert in AR Remote Concert in VR*

![[assets/figures/papers/paper_list_l3_https_www_cs_unc_edu_cpk/figures/011_Table_3.jpg]]
*Table 3: Ablation on Realistic Dataset. Ablation tests and analysis of our method on real-world dataset (Replay)*

## 实验与关键发现

MNAF 在合成数据集（SoundSpaces）、真实数据集（Replay）以及自建的 EnvSound 真实会话数据集上进行了系统验证，并辅以消融实验、HRTF 模块评估和主观用户研究。以下聚焦核心结果与关键发现。

### 主实验结果

Table 1 汇总了 MNAF 与现有方法在四个基准上的客观指标对比，评估维度包括 STFT 幅度误差（Mag↓）、左右耳能量比误差（LRE↓）和混响时间误差（RTE↓）。

![[assets/figures/papers/paper_list_l3_https_www_cs_unc_edu_cpk/figures/006_Table_1.jpg]]
*Table 1: Results on Simulated and Real-world Datasets. The Simulated Dataset includes the SoundSpaces dataset, featuring novel views collected in both the Same Environment and Novel Environment. The Real-world Dataset includes the Replay dataset, which contains novel views in the same environment, and the EnvSound dataset, which we collected ourselves across various environments. The Replay dataset was collected using a professional setup, whereas the EnvSound dataset was captured using a phone recorder. We consider the metric of STFT magnitude (Mag), left/right ratio error (LRE), and RT60 error (RTE). We evaluate the novel environment for the SoundSpaces dataset for it has a subset rendered on nove...*

在 SoundSpaces 合成数据上，MNAF 在“相同环境”（Same Environment）设置下取得 Mag 0.134、LRE 1.151、RTE 0.034；“新环境”（Novel Environment）设置下取得 Mag 0.186、LRE 1.125、RTE 0.034。新环境下性能与相同环境接近，表明模型具备跨环境泛化能力——视觉-声学融合模块从源场景图像中提取的材料和几何线索可迁移至未见场景。

在 Replay 真实数据集上，MNAF 取得 Mag 0.142、LRE 0.664、RTE 0.046。在自建的 EnvSound 真实会话数据集上，取得 Mag 0.035、LRE 5.21、RTE 0.038。值得注意的是，EnvSound 的 LRE 值明显偏高（5.21），这可能与该数据集包含多样化噪声环境和会话内容有关，左右声道能量分布的预测难度更大，但 Mag 和 RTE 仍保持较低水平，说明频谱包络和混响特性的合成质量依然稳健。

与基线方法相比，MNAF 在所有基准上均优于朴素基线（直接复制源音频）、TF Estimator 和 DSP 方法。与当前顶尖的新视角声学合成方法 **ViGAS**（Chen et al., CVPR 2023）相比，MNAF 在合成数据和真实数据上均展现出一致优势，尤其在混响相关指标（RTE）和立体声空间一致性（LRE）上提升显著。

### 关键消融实验

为验证两个核心创新模块的因果贡献，论文在合成数据（Table 2）和真实数据（Table 3）上进行了消融。

**自适应卷积（DCLS + 门控层）的贡献：** 在合成数据上，将自适应卷积替换为标准卷积后，Mag 从 0.134 恶化至 0.150，LRE 从 1.151 恶化至 1.260，RTE 从 0.034 升至 0.036。在真实数据（Replay）上，去掉自适应卷积后 LRE 从 0.664 升至 0.804，恶化幅度达 21%。这表明可学习间距的扩张卷积和门控自适应层对精确建模听者-声源相对位姿驱动的直达声和早期反射至关重要，尤其在真实环境中，固定扩张率的卷积无法灵活捕获不同场景下的空间声学变化。

**Conformer 视觉-声学融合模块的贡献：** 在合成数据上，将 Conformer 替换为简单的视觉与坐标特征拼接后，RTE 从 0.034 升至 0.037，Mag 从 0.134 升至 0.142。在真实数据上，去掉 Conformer 导致 Mag 从 0.142 升至 0.159，RTE 从 0.046 升至 0.051。Conformer 的交叉注意力机制显式建模了音视频时间相关性，使模型能从视觉特征中隐式推断房间的混响特性；简单拼接无法有效捕获这种跨模态交互，导致混响预测精度下降。

**HRTF 模块的影响：** Table 4 和 Table 5 展示了添加 HRTF 模块在 SoundSpaces 上的效果。在相同环境下，HRTF 模块使双耳间相位误差（Phase）从 1.629 降至 1.420，延迟误差（Delay）从 2.683 降至 1.815；在新环境下也有类似改善。这说明显式引入头部相关传递函数可增强模型对双耳线索的建模能力，但整体频谱幅度和混响指标的改善有限，表明 Conformer 和自适应卷积仍是性能提升的主驱动。

### 主观感知研究

**音质感知实验：** Table 6 显示，在 12 次对比试听中，参与者对 MNAF 合成音频与参考音频“无法区分”的试听次数与参考音频自身对比无显著差异（p=0.189），而基线方法（ViGAS）与参考音频的差异显著（p=0.006）。这从感知层面验证了 MNAF 合成音频的高度逼真性。

**VR/AR 沉浸感评估：** Figure 8 展示了基于 PQ 和 IPQ 问卷的主观评分。在 VR 环境中，MNAF 的沉浸感（Immersion）相对基线平均提升 26%，方差降低 51.4%（配对 t 检验 p=0.002）；真实感（Realism）平均提升 13.4%，方差降低 34.5%（p=0.054，接近显著）。在 AR 环境中，沉浸感提升同样显著（p=0.007）。参与度（Involvement）和保真度（Fidelity）维度也呈现一致的正向趋势。方差的大幅降低表明 MNAF 在不同场景和用户间的体验一致性更强，这对实际部署至关重要。

### 适用边界与失效模式

尽管 MNAF 在多个基准上表现优异，论文明确指出以下局限：

1. **视觉信息缺失场景：** 当场景缺乏有意义的几何结构或材料纹理（如纯白墙壁、空旷空间）时，视觉提示不足以推断声学特性，模型性能下降。这是因为 Conformer 依赖视觉特征作为材料属性的隐式代理。
2. **360 度视频输入不支持：** 当前实现仅处理单视角 RGB 图像，限制了 VR/AR 中全向视觉的沉浸感。扩展到全景视觉输入需要重新设计特征提取和融合架构。
3. **动态多声源与高噪声环境：** 当前模型假设单声源和相对受控的声学环境，尚未在包含多个移动声源和极高背景噪声的真实场景中验证。
4. **材料属性的隐式学习：** 模型通过视觉特征隐式推断材料对声音衰减的影响，而非显式建模。在材料声学特性与视觉外观不一致的场景（如透明隔音板）中可能存在系统性偏差。
5. **实时性与功耗未验证：** 论文未报告在不同 AR/VR 硬件平台上的推理延迟和功耗数据，实际部署的可行性有待进一步工程验证。

总体而言，MNAF 通过 Conformer 视觉-声学融合和自适应卷积两个核心创新，在合成与真实数据上均实现了新视角声学合成的最优性能，消融实验和主观研究为其因果机制提供了有力证据。但其在视觉贫乏场景、动态多声源环境和实际硬件部署中的表现仍是待解决的关键挑战。

![[assets/figures/papers/paper_list_l3_https_www_cs_unc_edu_cpk/figures/009_Table_4.jpg]]
*Table 4: HRTF module in SoundSpaces - Same Environment*

![[assets/figures/papers/paper_list_l3_https_www_cs_unc_edu_cpk/figures/010_Table_5.jpg]]
*Table 5: HRTF module in SoundSpaces - Novel Environment*

![[assets/figures/papers/paper_list_l3_https_www_cs_unc_edu_cpk/figures/014_Figure_8.jpg]]
*Figure 8: Subjective evaluation of Immersive Audio in VR/AR. Our post-study survey includes questions (detailed in Supp.) from the PQ and IPQ questionnaires. The Likert-scale responses are combined to evaluate both conditions across four dimensions: Immersion, Sensory Fidelity, Involvement, and Realism, with higher scores reflecting better performance. The boxes represent the data range between the first and third quartiles (Q1-Q3), with dots showing the mean and lines indicating the median. Error bars represent the farthest data points within 1.5× the interquartile range (IQR) from the boxes*

## 定位与知识库关联

MNAF 的核心定位在于：将空间音频合成从“基于简化物理模型或3D网格的显式声学模拟”推进到“从稀疏多模态传感数据中隐式学习场景声学特性”的范式。其改变的关键 **slot** 有两个：

1. **视觉-声学融合方式**：从 ViGAS（Chen et al., CVPR 2023）等现有方法的“简单拼接视觉和坐标特征”转变为“基于交叉注意力机制的堆叠式 Conformer 网络”。这一改变使模型能够显式建模音视频时间相关性，从视觉特征中隐式推断场景的材料声学属性（如墙面材质对混响的影响），而非依赖人工设计的物理参数或3D网格。
2. **声学合成卷积类型**：从“固定扩张率的1D标准卷积”转变为“具有可学习间距的扩张卷积（DCLS）结合门控自适应层”。这使得模型能够动态调节位置信息对音频波形的影响范围，更灵活地捕获不同空间尺度下的直达声与早期反射。

与现有工作的本质差异在于：ViGAS 等方法将视觉信息作为辅助条件直接拼接到声学特征中，缺乏对“视觉线索如何驱动声学特性变化”的显式建模；而 MNAF 通过两阶段解耦——先由视觉-声学融合网络捕获几何与材料驱动的全局混响特性，再基于听者-声源相对位姿动态生成直达声和局部反射——将声音传播的物理过程隐式地编码到了网络结构中。这一设计使得模型能够泛化到完全未见的新环境：只要提供新场景的稀疏录音和图像，即可合成具有空间一致性的双耳音频。

**知识库挂载点**：MNAF 可挂载到以下知识节点：
- **神经声场渲染**：作为 Neural Acoustic Fields（NAF）的多模态扩展，将单模态（仅音频+位姿）的声场学习推广到视觉-声学联合建模，证明了视觉特征可作为材料属性的有效代理。
- **多模态融合架构**：Conformer 中交叉注意力机制的设计为“如何将非对齐的音频-视觉信号融合为统一隐式表征”提供了可复用的范式，可迁移到其他需要从视觉推断物理特性的任务（如振动感知、流体声学）。
- **可学习卷积结构**：DCLS 在音频合成中的成功应用表明，可学习间距的扩张卷积比固定扩张率更适合处理具有多尺度时间依赖的波形生成任务，这对通用音频生成架构设计具有启发意义。

**适用边界**：
- 当前方法假设场景具有“有意义的几何结构和材料纹理”，在纯白墙或空白空间中视觉提示不足，性能下降。这意味着模型实际上学习的是“视觉纹理→声学特性”的统计关联，而非真正的物理声学模拟。
- 不支持360度视频输入，限制了全向视觉信息对混响建模的贡献；不支持动态多声源和极度嘈杂环境，表明模型的时间上下文建模能力有限。
- 材料衰减等物理属性仅通过视觉特征隐式学习，缺乏显式物理约束，在极端材质（如全金属反射面）场景中可能出现不符合物理规律的合成结果。

**后续启发**：
- 引入显式的材料属性学习模块（如从图像中分割材质并映射到声学阻抗参数）可能进一步提升跨环境泛化能力和物理一致性。
- 将模型扩展到360度视频输入和多声源动态场景，是通向真正沉浸式VR/AR空间音频的关键一步。
- 融合深度、IMU等额外传感模态，有望在视觉纹理不足的场景中提供补充的几何信息，弥补当前方法的盲区。
- 在不同AR/VR硬件平台上的实时性和功耗优化，是方法落地应用的必要工程步骤。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Hogel_free_Holography.pdf]]