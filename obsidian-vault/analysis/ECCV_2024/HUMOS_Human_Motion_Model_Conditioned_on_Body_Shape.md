---
title: HUMOS Human Motion Model Conditioned on Body Shape
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/HUMOS_Human_Motion_Model_Conditioned_on_Body_Shape.pdf
aliases:
- HHMMCBS
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过循环一致性训练策略实现无配对数据的自监督学习，并引入可微分的直观物理项（地面穿透、漂浮、滑步）与零力矩点（ZMP）动态稳定性项作为约束，强迫模型在生成运动时利用体型信息并保证物理合理性。
primary_logic: 单独使用循环一致性损失易导致模型崩溃到平凡解（忽略目标体型，直接复制源运动）。将物理冲突（如穿透、滑步）和动态不稳定作为损失施加在目标体型生成的中间结果上，能有效阻止这种崩溃，迫使编码器-解码器架构真正根据体型条件调整运动。
claims:
- 单独使用循环一致性损失（L_cycle）相较于基线TEMOS-Rokoko，在穿透（Penetrate）上改善约33%，漂浮（Float）改善约32%，滑步（Skate）改善约25%。
- 加入物理损失（L_physics）进一步改善物理合理性，尤其在脚滑动指标上带来最大改善（约47%）。
- 加入动态稳定性项（L_dyn）使HUMOS在所有指标上达到最佳配置，运动在71.9%的帧中保持动态稳定。
- 在用户感知研究中，HUMOS生成的运动在5分制评分中获得3.64分，显著高于TEMOS-Rokoko（3.25）和TEMOS-Rokoko-G（3.19）。
---

# HUMOS Human Motion Model Conditioned on Body Shape

> [!tip] 核心洞察
> 单独使用循环一致性损失易导致模型崩溃到平凡解（忽略目标体型，直接复制源运动）。将物理冲突（如穿透、滑步）和动态不稳定作为损失施加在目标体型生成的中间结果上，能有效阻止这种崩溃，迫使编码器-解码器架构真正根据体型条件调整运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | HUMOS: 体型条件化的人体运动模型 |
| 英文题名 | HUMOS Human Motion Model Conditioned on Body Shape |
| 会议/期刊 | ECCV 2024 |
| Links | [Code](https://github.com/CarstenEpic/humos) · [arXiv](https://arxiv.org/abs/2003.07254) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HUMOS |
| Dataset | AMASS test split, Perceptual Study |

> [!tip] 效果简介
> - AMASS test split (shape-conditioned motion reconstruction) 上，Dyn. Stability (%) 71.9 vs ~55.9 (TEMOS-Rokoko-G, closest baseline) (+16%)；Skate (%) 7.37 vs ~27.0 (TEMOS-Rokoko-G) (-19.63)。
> - Perceptual Study (5-point Likert scale) 上，Average Rating 3.64 vs 3.25 (TEMOS-Rokoko) (+0.39)。

## 概述

现有运动生成模型普遍使用归一化的平均体型进行训练，忽略了个体体型差异对运动执行方式的根本影响。这一简化导致生成的运动在物理真实性、多样性和动态稳定性方面存在明显不足。更关键的是，真实世界中缺乏不同体型个体执行完全相同动作的配对数据，使得直接训练体型条件化模型变得不可行。

HUMOS 针对上述瓶颈提出了一个体型条件化的人体运动生成框架。其核心思路是：**通过循环一致性自监督训练策略，从无配对的动作捕捉数据中学习一个身份无关的运动潜空间，并引入可微分的直观物理约束与零力矩点（ZMP）动态稳定性约束，迫使模型在生成目标体型运动时真正利用体型信息，而非陷入忽略体型差异的平凡解。**

具体而言，HUMOS 构建了一个基于 Transformer 的条件变分自编码器（c-VAE），以体型参数 β 和性别 G 作为编码器和解码器的显式条件信号。在训练阶段，源运动经编码器提取身份无关的潜编码后，由解码器结合目标体型生成运动，再通过逆向重建计算循环一致性损失。单独使用循环一致性损失即可使穿透指标改善约 33%、漂浮改善约 32%、滑步改善约 25%（相较于 TEMOS-Rokoko 基线）。进一步加入直观物理损失（地面穿透、漂浮、滑步）后，脚滑动指标额外降低约 47%，成为物理合理性提升最显著的项。最终引入基于 ZMP 与压力中心（CoP）距离的动态稳定性损失，使模型在所有指标上达到最优配置，动态稳定帧率达 71.9%。用户感知研究中，HUMOS 生成的运动在 5 分制评分中获得 3.64 分，显著高于 TEMOS-Rokoko（3.25）和 TEMOS-Rokoko-G（3.19）。

该方法的定位是在无配对数据条件下，通过损失函数设计而非网络架构的根本性变革，实现体型条件化的物理合理运动生成。其局限性包括训练数据体型多样性有限（仅 480 个个体）、物理损失未处理肢体自穿透，以及对空中动作的稳定性约束不足。

## 背景与动机

### 人体运动生成中的“体型盲区”

从文本、动作标签或场景约束中生成自然的人体运动，是计算机视觉与图形学领域的长期目标。近年来，基于深度生成模型（尤其是VAE和扩散模型）的运动合成方法取得了显著进展，能够产生流畅、语义合理的运动序列。然而，这些方法普遍隐含一个简化假设：所有运动都由一个标准化的“平均人体”执行。在训练和推理中，它们要么使用SMPL模型的中性平均体型，要么将所有运动数据归一化到统一骨架，完全抹除了个体间的体型差异。

这一假设与物理现实存在根本性冲突。不同体型的人执行同一动作时，运动模式必然不同——高个子与矮个子的步幅、体重较大者与较轻者的重心转移策略、不同性别间的骨盆运动学差异，都会导致运动轨迹的显著变化。现有模型由于缺乏体型条件化能力，生成的运动呈现出“体型同质化”问题：无论目标角色是儿童还是成年人，输出的运动模式几乎一致，物理真实性和视觉多样性均受到严重损害。

### 体型条件化运动生成的核心瓶颈

将体型信息引入运动生成面临一个关键障碍：**缺乏不同个体执行完全相同动作的配对训练数据**。在监督学习范式下，要训练一个模型将源体型的运动“重定位”到目标体型，需要成对的运动序列——同一动作由多个体型各异的个体执行，且时间对齐。这类数据的采集成本极高，现有的大规模运动捕捉数据集（如AMASS）虽然包含多个个体，但每个个体执行的动作集合互不重叠，无法构成配对样本。因此，直接训练一个有监督的体型条件化运动生成模型在数据层面不可行。

### 现有补救方案的局限

面对这一瓶颈，工业界和学术界尝试了几种替代方案，但均存在根本性缺陷：

- **商业重定位系统**（如Rokoko）：将生成的运动通过运动学重定位算法映射到目标骨架上，仅做简单的骨骼缩放和根关节平移。这类方法完全忽略了体型变化对运动动力学的深层影响——例如，一个为平均体型生成的迈步动作直接缩放到一个腿长显著不同的角色上，会导致脚部穿透地面或悬浮空中，物理合理性严重受损。
- **简单地面校正**：对重定位结果施加整体平移，使最低顶点恰好接触地面。这能缓解部分漂浮问题，但无法解决滑步（脚与地面之间的非物理相对滑动）和动态不稳定（如重心超出支撑域导致的失衡）等更深层的物理冲突。

这些后处理方案的本质问题是：它们试图在运动生成之后“修补”物理不合理性，而非在生成过程中主动利用体型信息来塑造运动本身。

### 本文动机与核心思路

HUMOS的出发点在于一个关键洞察：**物理冲突本身可以成为自监督信号**。在没有配对数据的情况下，如果模型仅仅被训练去“复制”源运动而忽略目标体型，生成的运动必然与目标体型的物理约束发生冲突——脚穿透地面、身体悬浮、支撑脚滑动、动态失衡。将这些物理冲突量化为可微损失，并施加在目标体型生成的中间结果上，就能迫使模型在生成过程中真正“考虑”体型信息，而非简单地复制源运动。

这一思路将体型条件化运动生成从一个数据匮乏的监督学习问题，转化为一个物理引导的自监督学习问题。具体而言，HUMOS构建了一个循环一致性训练框架：编码器从源运动提取身份无关的潜编码，解码器以目标体型为条件生成运动，再通过逆向过程重建源运动。在此框架下，直观物理损失（地面穿透、漂浮、滑步）和动态稳定性损失（基于零力矩点ZMP与压力中心CoP的距离）共同构成约束，防止模型崩溃到忽略目标体型的平凡解，从而真正实现体型感知的运动生成。

## 核心创新

HUMOS 的核心创新在于**首次将体型差异显式建模为运动生成的条件信号**，并通过一套自监督训练策略与可微物理约束的组合，解决了该方向长期存在的两大瓶颈：缺乏不同体型执行相同动作的配对训练数据，以及现有模型因忽略体型而导致的运动同质化与物理不真实。

### 创新一：体型条件化的运动生成框架

现有运动生成模型（如 **TEMOS**，Petrovich et al., ECCV 2022）普遍使用 SMPL 中性平均体型，将运动与体型解耦，忽略了“不同体型的人执行同一动作时运动模式存在本质差异”这一事实。HUMOS 将体型参数 $\beta$ 和性别 $G$ 作为显式条件信号，同时注入编码器和解码器：

- **运动编码器**：以源身份特征 $\mathcal{T}_A$ 为条件的 Transformer VAE，将源运动 $\mathbf{M}_A$ 映射到身份无关的运动潜空间 $\mathbf{z}_{M_A}$；
- **运动解码器**：以目标身份特征 $\mathcal{T}_B$ 为条件的 Transformer，从潜编码生成适配目标体型的运动序列 $\hat{\mathbf{M}}_{AB}$。

这一“身份条件化编码器-解码器”架构（Fig. 2）是后续所有创新的结构基础。

### 创新二：无配对数据的循环一致性自监督训练

由于现实世界中几乎不可能获取“同一动作在不同体型上的配对运动捕捉数据”，HUMOS 借鉴图像翻译中的循环一致性思想，设计了**形状-运动空间的循环一致性自监督训练策略**（Sec. 3.2）：

1. 从源身份 $A$ 的运动 $\mathbf{M}_A$ 出发，编码得到身份无关潜编码 $\mathbf{z}_{M_A}$；
2. 以目标身份 $B$ 为条件解码，生成 $\hat{\mathbf{M}}_{AB}$；
3. 再以源身份 $A$ 为条件，将 $\hat{\mathbf{M}}_{AB}$ 编码-解码回 $\hat{\mathbf{M}}_{AA}$；
4. 通过最小化源运动与重建运动之间的旋转测地距离 $\mathcal{L}_{\mathrm{rot}}$ 和位置 L1 损失 $\mathcal{L}_{\mathrm{pos}}$，迫使模型学习身份无关的运动表征。

该策略使模型在完全无配对数据的条件下，学会将运动“迁移”到不同体型上。

### 创新三：可微直观物理损失防止模型崩溃

单独使用循环一致性损失存在一个关键缺陷：**模型容易崩溃到平凡解**——解码器直接忽略目标体型条件，将源运动原样复制输出，因为这样做也能完美满足循环一致性约束。

HUMOS 的核心洞察是：**将物理冲突作为损失施加在目标体型生成的中间结果 $\hat{\mathbf{M}}_{AB}$ 上，能有效阻止这种崩溃**。具体而言，引入三项完全可微的直观物理损失（Sec. 3.3）：

- **穿透损失** $\mathcal{L}_{\mathrm{penetrate}}$：惩罚身体网格与地面的穿透；
- **漂浮损失** $\mathcal{L}_{\mathrm{float}}$：惩罚脚部离地漂浮；
- **滑步损失** $\mathcal{L}_{\mathrm{slide}}$：惩罚支撑脚在地面的滑动。

这些损失仅在目标体型生成的运动上计算，迫使解码器必须真正根据体型条件调整运动，否则将产生严重的物理冲突。消融实验（Tab. 3）证实了这一机制的有效性：单独使用循环一致性损失（$\mathcal{L}_{\mathrm{cycle}}$）相较 TEMOS-Rokoko 基线，穿透改善约 33%，漂浮改善约 32%，滑步改善约 25%；加入物理损失（$\mathcal{L}_{\mathrm{physics}}$）后，脚滑动指标进一步降低约 47%。

### 创新四：基于零力矩点的动态稳定性约束

物理合理性不仅包括避免穿透和滑步，还涉及运动是否在生物力学上可稳定执行。HUMOS 引入基于**零力矩点（ZMP）**的动态稳定性损失 $\mathcal{L}_{\mathrm{dyn}}$（Sec. 3.4）：

$$\mathcal{L}_{\mathrm{dyn}} = \rho( \| \mathcal{C}_P - \mathcal{Z} \|_2 )$$

其中 $\mathcal{Z}$ 为零力矩点，$\mathcal{C}_P$ 为压力中心（CoP），$\rho$ 为 Geman-McClure 鲁棒惩罚函数。当 ZMP 落在支撑多边形（即 CoP 所在区域）内时，运动是动态稳定的。该损失项使 HUMOS 生成的运动在 71.9% 的帧中保持动态稳定，较最接近的基线 TEMOS-Rokoko-G（约 55.9%）提升约 16 个百分点。

### 创新总结：损失协同机制

HUMOS 的总训练损失为五项损失的加权组合：

$$\mathcal{L} = \lambda_{\mathrm{cycle}} \mathcal{L}_{\mathrm{cycle}} + \lambda_{\mathrm{physics}} \mathcal{L}_{\mathrm{physics}} + \lambda_{\mathrm{dyn}} \mathcal{L}_{\mathrm{dyn}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{E}} \mathcal{L}_{\mathrm{E}}$$

其中循环一致性损失提供无配对数据的自监督学习信号，物理损失和动态稳定性损失共同构成“现实性约束”，阻止模型崩溃并保证生成质量。消融实验（Tab. 3）清晰展示了三者的递进贡献：$\mathcal{L}_{\mathrm{cycle}}$ 建立基础的运动迁移能力，$\mathcal{L}_{\mathrm{physics}}$ 大幅改善物理合理性，$\mathcal{L}_{\mathrm{dyn}}$ 使模型在所有指标上达到最优配置。用户感知研究（Tab. 2）进一步验证了这一创新的实际效果：HUMOS 以 3.64/5 的平均评分显著优于 TEMOS-Rokoko（3.25）和 TEMOS-Rokoko-G（3.19）。

## 整体框架

HUMOS 是一个基于条件变分自编码器（c-VAE）的非自回归运动生成模型。其核心目标是在给定目标体型参数（β 和性别 G）的条件下，生成物理合理且动态稳定的三维人体运动序列。整个框架由编码器-解码器架构、自监督循环一致性训练策略、可微物理损失和动态稳定性约束四个关键模块构成。

### 输入输出流

模型的输入包括两个部分：一段源运动序列 $M_A$ 及其对应的源身份特征 $\mathcal{T}_A$（体型参数 β 和性别 G）。输出是适配目标身份特征 $\mathcal{T}_B$ 的运动序列 $\hat{M}_{AB}$。整个生成过程是非自回归的，即一次性输出连续 $T$ 帧的运动特征，而非逐帧预测。

### 编码器：身份条件化的运动编码

运动编码器 $E$ 以源运动 $M_A$ 和源身份 $\mathcal{T}_A$ 为条件输入，将运动映射到一个身份无关的潜空间。具体而言，编码器在 TEMOS（Petrovich et al., ECCV 2022）的 Transformer VAE 架构基础上，显式地将身份特征作为条件信号注入，输出潜分布的均值和对数方差参数，进而采样得到潜编码 $z_{M_A}$。身份条件化的设计使得编码器能够将“运动本身”与“执行该运动的体型”解耦，从而提取出与体型无关的运动语义。

### 解码器：身份条件化的运动生成

运动解码器 $D$ 同样基于 Transformer 架构。它以 $T$ 个正弦位置编码作为查询（query），将潜编码 $z_{M_A}$ 与目标身份特征 $\mathcal{T}_B$ 的拼接向量作为键值（key-value）输入。解码器根据目标体型条件，从身份无关的潜编码中重建出适配目标体型的运动序列 $\hat{M}_{AB}$。这一“潜编码 + 目标身份”的输入设计是体型条件化的核心机制：相同的潜编码搭配不同的身份特征，可以生成同一动作在不同体型上的差异化表现。

### 循环一致性自监督训练

由于缺乏不同个体执行相同动作的配对训练数据，HUMOS 采用循环一致性训练策略来实现自监督学习。具体流程为：将源运动 $M_A$ 编码为 $z_{M_A}$，再以目标身份 $\mathcal{T}_B$ 为条件解码生成 $\hat{M}_{AB}$；随后将 $\hat{M}_{AB}$ 重新编码为 $\hat{z}_{M_{AB}}$，并以源身份 $\mathcal{T}_A$ 为条件解码重建回 $\hat{M}_{AA}$。循环一致性损失 $\mathcal{L}_{\mathrm{cycle}}$ 约束 $\hat{M}_{AA}$ 与原始 $M_A$ 在旋转和位置上一致，从而迫使编码器-解码器在无配对数据的情况下学会体型-运动的正确解耦与重映射。

### 物理与稳定性约束

仅靠循环一致性损失存在模型崩溃风险——网络可能学习到忽略目标体型、直接复制源运动的平凡解。HUMOS 的关键洞察在于，将物理冲突和动态不稳定作为损失施加在目标体型生成的中间结果 $\hat{M}_{AB}$ 上，能有效阻止这种崩溃。

具体而言，可微直观物理损失 $\mathcal{L}_{\mathrm{physics}}$ 包含三项：地面穿透惩罚 $\mathcal{L}_{\mathrm{penetrate}}$、漂浮惩罚 $\mathcal{L}_{\mathrm{float}}$ 和脚滑动惩罚 $\mathcal{L}_{\mathrm{slide}}$。这些损失直接计算在 $\hat{M}_{AB}$ 上，迫使解码器在生成运动时真正利用目标体型信息来避免物理冲突。

动态稳定性损失 $\mathcal{L}_{\mathrm{dyn}}$ 基于零力矩点（ZMP）与压力中心（CoP）之间的欧氏距离构建。当 ZMP 位于支撑多边形（由着地脚形成的凸包）之外时，运动在生物力学上是不稳定的。该损失项通过惩罚 ZMP 偏离 CoP 的程度，使生成的运动在大部分帧中保持动态平衡。

### 完整训练目标

总损失函数为各损失项的加权和：

$$\mathcal{L} = \lambda_{\mathrm{cycle}} \mathcal{L}_{\mathrm{cycle}} + \lambda_{\mathrm{physics}} \mathcal{L}_{\mathrm{physics}} + \lambda_{\mathrm{dyn}} \mathcal{L}_{\mathrm{dyn}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{E}} \mathcal{L}_{\mathrm{E}}$$

其中 $\mathcal{L}_{\mathrm{KL}}$ 对源运动和生成运动的潜分布施加 KL 散度正则化，$\mathcal{L}_{\mathrm{E}}$ 鼓励源运动潜编码与循环生成运动潜编码一致。各权重经实验确定：$\lambda_{\mathrm{cycle}}=1$，$\lambda_{\mathrm{physics}}=1$，$\lambda_{\mathrm{dyn}}=0.0001$，$\lambda_{\mathrm{KL}}=10^{-5}$，$\lambda_{\mathrm{E}}=10^{-2}$。

### 补充图表

![[assets/figures/papers/paper_list_l9_HUMOS_Human_Motion_Model_Conditioned_on_Body_Shape/figures/002_Figure_2.jpg]]
*Figure 2: Visual representation of our architecture. The Encoder takes as input a motion $M _ { A }$ and its associated identity $\mathcal { T } _ { \mathcal { A } }$ . , and outputs a latent (identity invariant) encoding of the motion $z _ { M _ { A } }$ . The Decoder takes as input the latent encoding of the motion $z _ { M _ { A } }$ , along with a different identity ${ \mathcal { T } } _ { B }$ , and produces a retargeted motion appropriate for the $\mathrm { g i }$ ven identity $\hat { M } _ { A B }$ . The same Encoder and Decoder are used with the original identity to produce a cycle loss $\mathcal { L } _ { \mathrm { c y c l e } }$ , while a physics loss $\mathcal { L } _ { \mathrm { p h y s i c s } }$ ensures...*

## 核心模块与公式推导

HUMOS 的整体架构围绕一个**体型条件化的 Transformer VAE** 展开，通过**循环一致性自监督训练**与**可微物理/动力学约束**的联合优化，实现从无配对数据中学习体型-运动解耦的生成能力。以下按模块拆解其核心设计。

### 1. 体型条件化运动编码器与解码器

**运动编码器**以源身份特征 $\mathcal{T}_A$（包含体型参数 $\beta$ 和性别 $G$）为条件，将任意长度 $T$ 的运动序列 $M_A$ 映射到身份无关的潜空间分布。编码器基于 TEMOS（Petrovich et al., ECCV 2022）的 Transformer VAE 架构扩展而来，输出潜编码 $z_{M_A}$ 的分布参数。

**运动解码器**同样采用 Transformer 架构，以正弦位置编码作为 Query，将潜编码 $z_{M_A}$ 与目标身份特征 $\mathcal{T}_B$ 拼接后作为 Key-Value，一次性生成目标体型的 $T$ 帧运动序列 $\hat{M}_{AB}$。该非自回归生成方式保证了推理效率。

### 2. 循环一致性自监督训练

由于不存在不同个体执行相同动作的配对数据，HUMOS 借鉴图像翻译领域的循环一致性思想，构建了**正向生成-逆向重建**的训练回路：

1. **正向路径**：编码器从源运动 $M_A$（身份 $\mathcal{T}_A$）提取潜编码 $z_{M_A}$，解码器以目标身份 $\mathcal{T}_B$ 为条件生成 $\hat{M}_{AB}$。
2. **逆向路径**：将 $\hat{M}_{AB}$ 重新编码，再以原始身份 $\mathcal{T}_A$ 解码，得到重建运动 $\hat{M}_{AA}$。
3. **循环一致性损失** $\mathcal{L}_{\mathrm{cycle}}$ 强制 $\hat{M}_{AA}$ 与原始 $M_A$ 一致，从而约束潜编码 $z_{M_A}$ 真正与身份解耦：

$$\mathcal{L}_{\mathrm{cycle}} = \mathcal{L}_{\mathrm{rot}} + \mathcal{L}_{\mathrm{pos}}$$

其中旋转损失 $\mathcal{L}_{\mathrm{rot}}$ 计算源运动与重建运动各帧旋转矩阵之间的**测地距离**：

$$\mathcal{L}_{\mathrm{rot}} = \sum_{t=1}^{T} \operatorname{arccos} \frac{\mathrm{Tr}\Big(R_{t_A} (\hat{R}_{t_{AA}})^{-1}\Big) - 1}{2}$$

位置损失 $\mathcal{L}_{\mathrm{pos}}$ 计算根关节位置的平滑 L1 距离：

$$\mathcal{L}_{\mathrm{pos}} = \sum_{t=1}^{T} \| \mathbf{x}_{t_A} - \hat{\mathbf{x}}_{t_{AA}} \|_1$$

**关键洞察**：单独使用 $\mathcal{L}_{\mathrm{cycle}}$ 会导致模型崩溃到平凡解——解码器直接忽略目标体型条件，复制源运动。这是后续物理约束必须介入的根本原因。

### 3. 可微直观物理损失

为防止循环一致性训练的平凡解崩溃，HUMOS 在**目标体型生成的中间结果 $\hat{M}_{AB}$ 上直接施加物理惩罚**，强迫模型真正利用体型信息调整运动。物理损失 $\mathcal{L}_{\mathrm{physics}}$ 由三项组成：

$$\mathcal{L}_{\mathrm{physics}} = \mathcal{L}_{\mathrm{penetrate}} + \mathcal{L}_{\mathrm{float}} + \mathcal{L}_{\mathrm{slide}}$$

- **$\mathcal{L}_{\mathrm{penetrate}}$**：惩罚身体网格顶点穿透地面的深度，通过 SMPL 模型的可微顶点计算实现。
- **$\mathcal{L}_{\mathrm{float}}$**：惩罚双脚离地漂浮的高度，确保足部与地面合理接触。
- **$\mathcal{L}_{\mathrm{slide}}$**：惩罚支撑脚在地面上的滑动位移，通过比较相邻帧足部接触点的位置变化计算。

这三项均为**完全可微**的直观物理项，与 SMPL 参数化身体模型天然兼容，无需外部物理引擎。

### 4. 动态稳定性损失

物理合理性仅保证静态接触约束，HUMOS 进一步引入基于**零力矩点（ZMP）**的动态稳定性评估。ZMP 是地面上使惯性力与重力合力矩为零的点，其定义如下：

$$\mathcal{Z} = \mathcal{C}_m - \frac{n \times \mathcal{M}_{\mathcal{C}_m}^{gi}}{\mathcal{F}^{gi} \cdot n}$$

其中各变量含义：
- $\mathcal{C}_m$：质心在地面的投影点
- $n$：地面法向量
- $\mathcal{F}^{gi} = m g - m a_{\mathcal{G}}$：作用在质心 $\mathcal{G}$ 上的惯性力（$m$ 为身体段质量，$g$ 为重力加速度，$a_{\mathcal{G}}$ 为质心加速度）
- $\mathcal{M}_{\mathcal{C}_m}^{gi} = \overrightarrow{\mathcal{C}_m \mathcal{G}} \times m g - \overrightarrow{\mathcal{C}_m \mathcal{G}} \times m a_{\mathcal{G}} - \dot{\mathcal{H}}_{\mathcal{G}}$：关于投影质心的惯性力矩（$\dot{\mathcal{H}}_{\mathcal{G}}$ 为角动量变化率）

动态稳定性损失 $\mathcal{L}_{\mathrm{dyn}}$ 计算压力中心（CoP）$\mathcal{C}_P$ 与 ZMP 的欧氏距离，经 Geman-McClure 鲁棒惩罚函数 $\rho(\cdot)$ 处理：

$$\mathcal{L}_{\mathrm{dyn}} = \rho( \| \mathcal{C}_P - \mathcal{Z} \|_2 )$$

当 ZMP 位于支撑多边形（由足部接触点围成）内时，运动保持动态平衡。该损失仅在双脚着地支撑阶段激活，对空中动作（如跳跃）自动禁用。

### 5. 潜空间正则化与总损失

除上述核心损失外，HUMOS 还引入两项辅助损失以稳定潜空间：

$$\mathcal{L}_{\mathrm{KL}} = \mathrm{KL}(z_{M_A}, \psi) + \mathrm{KL}(z_{M_{AB}}, \psi)$$

将源运动与生成运动的潜分布正则化为标准正态分布 $\psi$。

$$\mathcal{L}_{\mathrm{E}} = \| z_{M_A} - z_{M_{AB}} \|_1$$

鼓励源运动潜编码与循环生成运动潜编码一致，强化身份不变性。

**总训练损失**为各损失项的加权和，权重经实验确定：

$$\mathcal{L} = \lambda_{\mathrm{cycle}} \mathcal{L}_{\mathrm{cycle}} + \lambda_{\mathrm{physics}} \mathcal{L}_{\mathrm{physics}} + \lambda_{\mathrm{dyn}} \mathcal{L}_{\mathrm{dyn}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{E}} \mathcal{L}_{\mathrm{E}}$$

其中 $\lambda_{\mathrm{cycle}} = 1$，$\lambda_{\mathrm{physics}} = 1$，$\lambda_{\mathrm{dyn}} = 0.0001$，$\lambda_{\mathrm{KL}} = 10^{-5}$，$\lambda_{\mathrm{E}} = 10^{-2}$。物理损失与循环损失等权，动态稳定性损失权重较小以避免过度约束运动自然度。

### 补充图表

![[assets/figures/papers/paper_list_l9_HUMOS_Human_Motion_Model_Conditioned_on_Body_Shape/figures/001_Figure_1.jpg]]
*Figure 1: People with different body shapes perform the same motion differently. Our method, HUMOS, generates natural, physically plausible and dynamically stable human motions conditioned on body shape. HUMOS uses a novel identity-preserving cycle consistency loss and differentiable dynamic stability and physics terms to learn an identity-conditioned manifold of human motions. Shown here is the same walk motion with a skip-step in the middle, generated by HUMOS for five different identities IA:E. To demonstrate shape-conditioning, we visualize the same motion but successively change the identity after every 30 frames*

## 实验与分析

### 主实验结果

HUMOS在体型条件化运动重建任务上进行了定量评估，与多个基线方法进行了对比。基线包括：原始TEMOS（Petrovich et al., ECCV 2022）的简单重定位变体TEMOS-Simple、带地面校正的TEMOS-Simple-G、使用商业重定位系统Rokoko的TEMOS-Rokoko，以及其地面校正版本TEMOS-Rokoko-G。评估指标聚焦于物理合理性和动态稳定性，包括穿透（Penetrate）、漂浮（Float）、滑步（Skate）和动态稳定帧率（Dyn. Stability）。

在AMASS测试集上，HUMOS在所有物理合理性指标上均显著优于基线方法。具体而言，HUMOS将滑步（Skate）指标降低至7.37%，相较于最接近的基线TEMOS-Rokoko-G（约27.0%）改善约19.63个百分点。动态稳定帧率方面，HUMOS达到71.9%，比TEMOS-Rokoko-G（约55.9%）提升了约16个百分点（Tab. 1）。

用户感知研究进一步验证了HUMOS生成运动的真实感。参与者观看生成运动视频后，对“给定该体型下运动有多真实？”进行5分制评分。HUMOS获得平均3.64分，显著高于TEMOS-Rokoko（3.25）和TEMOS-Rokoko-G（3.19）（Tab. 2）。这一结果表明，客观物理指标的改善与人类主观感知一致。

**证据强度**：用户感知研究中参与者数量未明确，且仅与两个基线比较，可能存在选择偏差。物理指标测量为客观计算，可信度较高。

### 消融实验

消融实验系统评估了循环一致性损失（L_cycle）、物理损失（L_physics）和动态稳定性损失（L_dyn）的各自贡献（Tab. 3）。

以TEMOS-Rokoko为基线，单独引入循环一致性训练（L_cycle）已带来显著改善：穿透指标提升约33%，漂浮提升约32%，滑步提升约25%。这表明无配对数据的自监督训练框架本身就能有效利用体型信息来改善运动质量。

进一步加入物理损失（L_physics）后，所有物理指标继续改善，其中脚滑动指标改善最为显著（约47%）。这验证了可微直观物理项作为训练损失在防止模型崩溃到平凡解方面的关键作用——仅使用循环一致性损失时，模型可能忽略目标体型直接复制源运动，而施加在目标体型中间结果上的物理惩罚有效阻止了这种退化。

最终，加入动态稳定性损失（L_dyn）使HUMOS在所有指标上达到最佳配置，动态稳定帧率提升至71.9%。各损失项权重经实验确定为：λ_cycle=1，λ_physics=1，λ_dyn=0.0001，λ_KL=10^{-5}，λ_E=10^{-2}。

**因果链**：循环一致性建立体型-运动解耦的基础 → 物理损失阻止解耦崩溃并提供物理合理性信号 → 动态稳定性损失补充生物力学平衡约束，三者互补递进。

**证据强度**：消融实验有明确的定量对比和基线锚定，证据置信度高。

### 定性分析与失败模式

定性对比（Fig. 3）直观展示了HUMOS相对于基线的优势。基线方法在不同体型上生成的运动频繁出现穿透、漂浮和脚滑动等问题（图中红色圈标注），而HUMOS生成的运动在相同帧上表现出更好的物理合理性（绿色圈标注）。

![[assets/figures/papers/paper_list_l9_HUMOS_Human_Motion_Model_Conditioned_on_Body_Shape/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison of shape-conditioned motion generation. Each row represents generations across different methods for a unique body shape and gender. HUMOS generated motions are more realistic, physically plausible and dynamically stable compared to baselines. The red circles on the baseline methods highlight issues such as floating, penetrations, and foot skating, compared to more realistic results on highlighted in green with HUMOS. ü Zoom in*

但方法存在以下已知局限：

1. **训练数据体型多样性有限**：AMASS数据集仅包含480个不同体型的个体（274名男性、206名女性），模型对极端体型的泛化能力可能不足，需在更多样化数据上验证。

2. **肢体自穿透未处理**：当前物理损失仅考虑身体与地面的交互，未处理肢体间的自穿透问题，在复杂交互动作（如打斗、拥抱）中可能出现。

3. **空中动作的稳定性约束缺失**：动态稳定性项依赖地面支撑假设，对跳跃、空翻等空中动作会禁用该项，在这些场景下稳定性可能不足。

4. **身份条件维度有限**：仅以体型和性别作为身份条件，未考虑运动风格属性（如情绪状态、年龄、生理障碍等）的进一步条件化。

**需手动验证**：论文未提供HUMOS在极端姿态和复杂自接触运动上与经典重定位方法的直接定量对比，该方面的相对表现需进一步实验确认。

### 补充图表

![[assets/figures/papers/paper_list_l9_HUMOS_Human_Motion_Model_Conditioned_on_Body_Shape/figures/004_Table_1.jpg]]
*Table 1: Comparison of HUMOS with baselines on the shape-conditioned motion reconstruction task*

![[assets/figures/papers/paper_list_l9_HUMOS_Human_Motion_Model_Conditioned_on_Body_Shape/figures/005_Table_2.jpg]]
*Table 2: Perceptual study comparing HUMOS with two closest baselines. Given a video of a generated motion, participants select 5-point ratings for the question “How realistic is the motion given this body shape?”*

![[assets/figures/papers/paper_list_l9_HUMOS_Human_Motion_Model_Conditioned_on_Body_Shape/figures/006_Table_3.jpg]]
*Table 3: Ablation study comparing the improvements from cycle-consistent training ( $\mathcal { L } _ { \mathrm { c y c l e } }$ ) , physics losses ( $\mathcal { L } _ { \mathrm { { p h y s i c s } } }$ ) and the dynamic stability term $\left( { \mathcal { L } } _ { \mathrm { d y n } } \right$)*

## 方法谱系与知识库定位

HUMOS 建立在**非自回归 Transformer VAE** 的文本-运动生成框架之上，其核心编码器-解码器架构直接继承自 **TEMOS**（Petrovich et al., ECCV 2022）。TEMOS 使用 Transformer 编码器将运动序列映射到潜空间，再用 Transformer 解码器从潜编码重建运动，但这一管线完全在 SMPL 中性平均体型上运行，缺乏对个体体型差异的建模能力。HUMOS 的关键改造在于将身份特征（体型参数 β 和性别 G）作为编码器和解码器的显式条件信号，使潜空间从“运动本身”的表示转变为“身份无关的运动语义”表示——这是实现体型条件化生成的结构性前提。

然而，仅引入体型条件信号并不足以训练出有效的模型，因为**缺乏不同体型个体执行相同动作的配对数据**是这一方向的核心瓶颈。HUMOS 借鉴图像到图像翻译中的循环一致性思想，提出了一种自监督训练策略：将源身份的运动编码为潜变量后，用目标身份解码生成目标运动，再将生成的运动用源身份重新编码-解码，通过最小化源运动与重建运动之间的测地距离和位置损失来约束训练。这一策略在理论上允许模型从无配对数据中学习身份-运动的解耦表示。

但单独使用循环一致性损失存在严重风险——模型可能崩溃到平凡解，即**忽略目标体型信息，直接将源运动复制输出**。HUMOS 的核心洞察在于：将物理冲突作为损失施加在目标体型生成的中间结果上，能够有效阻止这种崩溃。具体而言，可微分的直观物理项（地面穿透、漂浮、脚滑动）和基于零力矩点（ZMP）的动态稳定性项被计算在目标体型运动上，强迫解码器在生成过程中必须考虑体型参数的影响，否则将面临高额物理惩罚。这种“在目标域施加约束”的设计，使得物理损失不仅是质量提升手段，更是训练策略中防止循环一致性退化的必要组件。

从方法谱系定位来看，HUMOS 处于运动重定位与物理仿真两个领域的交叉地带。传统运动重定位方法（如商业系统 Rokoko）依赖显式的运动学约束和人工标定，而 HUMOS 将重定位隐式地嵌入到生成模型的训练目标中。与基于物理仿真器的方法（如通过强化学习在仿真环境中适配运动）相比，HUMOS 的优势在于端到端可微、推理速度快，且不需要显式的动力学模型或仿真环境，但其物理约束是软约束而非硬约束，无法保证严格的无穿透。

### 适用边界与局限

**适用边界**：HUMOS 适用于需要为不同体型个体生成物理合理运动的场景，尤其是动作捕捉数据中体型多样性有限、缺乏配对数据的情况。其自监督训练策略使其能够利用现有的运动捕捉数据库（如 AMASS）进行训练，无需额外采集配对数据。

**已知局限**：
1. **体型多样性受限**：训练数据 AMASS 仅包含 480 个不同体型的个体（274 男性，206 女性），这一有限的体型分布可能影响模型在极端体型（如过度肥胖或极度瘦削）上的泛化能力。
2. **物理约束不完整**：当前的物理损失仅处理身体与地面的交互（穿透、漂浮、滑步），未处理肢体间的自穿透问题，在复杂交互动作（如打斗、拥抱）中可能出现网格交叉。
3. **身份条件维度有限**：方法仅以体型参数 β 和性别 G 作为身份条件，未考虑运动风格属性（如情绪状态、年龄、生理障碍等），尚无法实现多属性联合控制。
4. **动态稳定性假设**：ZMP 动态稳定性项依赖地面支撑假设，对空中动作（如跳跃、空翻）需手动禁用该项，在这些场景下可能稳定性不足。

### 开放问题

1. **极端姿态与复杂接触**：HUMOS 在极端姿态和复杂自接触运动（如打斗、拥抱）上相对于经典重定位方法（如 Rokoko）的表现如何？现有评估未覆盖这类场景。
2. **多属性条件化**：如何将情绪、年龄、生理障碍等运动风格属性作为额外条件信号，实现体型与风格的多属性解耦控制？
3. **体型泛化能力**：训练数据中有限的体型多样性如何定量影响模型在引入新体型时的运动质量和多样性？是否存在系统性的退化模式？
4. **网格自穿透**：如何在形状条件生成过程中有效解决网格自穿透问题，同时保持端到端可微和训练效率？这是当前物理损失体系中的一个明显缺口。

## 原文 PDF

![[paperPDFs/ECCV_2024/HUMOS_Human_Motion_Model_Conditioned_on_Body_Shape.pdf]]