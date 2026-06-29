---
title: Neural Wavelet-domain Diffusion for 3D Shape Generation
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Neural_Wavelet_domain_Diffusion_for_3D_Shape_Generation.pdf
project_link: null
code_link: null
aliases:
- NWDD
- NWDD3SG
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用截断有符号距离场(TSDF)结合双正交小波变换构建紧凑小波表示（粗系数+细节系数），并在该表示上使用扩散概率模型直接生成形状，摒弃了预训练潜空间和表示转换。
primary_logic: 将隐式表面在小波域分解为粗尺度（捕捉整体结构）和细节尺度（捕捉精细细节），并截断SDF以减少冗余，使得扩散模型可有效学习形状分布，生成多样、高质量且结构新颖的三维形状。
claims:
- 仅使用J=3尺度的小波系数（约3%系数量）即可重建TSDF，幅度变化仅2.8%，表明粗系数已保留主要结构。
- 在Chair和Airplane类别上，本方法在MMD、COV和1-NNA三项指标上均超越现有方法（IM-GAN、SPAGHETTI、Voxel-GAN）。
- 消融实验表明，去除细节预测器后COV CD从58.19降至54.20，验证了细节系数的贡献。
- 双正交小波（消失矩6/8）能生成比Haar小波更平滑的重建，避免体素化伪影。
---

# Neural Wavelet-domain Diffusion for 3D Shape Generation

> [!tip] 核心洞察
> 将隐式表面在小波域分解为粗尺度（捕捉整体结构）和细节尺度（捕捉精细细节），并截断SDF以减少冗余，使得扩散模型可有效学习形状分布，生成多样、高质量且结构新颖的三维形状。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于神经小波域扩散的三维形状生成 |
| 英文题名 | Neural Wavelet-domain Diffusion for 3D Shape Generation |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2209.08725) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Neural Wavelet-domain Diffusion |
| Dataset | ShapeNet Chair, ShapeNet Airplane |

> [!tip] 效果简介
> - ShapeNet Chair 上，COV (%) CD 58.19 vs 57.68 (IM-GAN) (+0.51)；MMD (×10⁻³) CD 11.70 vs 12.91 (IM-GAN) (-1.21)；1-NNA (%) CD 61.47 vs 70.72 (IM-GAN) (-9.25)。
> - ShapeNet Airplane 上，COV (%) CD 64.78 vs 58.34 (IM-GAN) (+6.44)；MMD (×10⁻³) CD 3.230 vs 4.062 (IM-GAN) (-0.832)。

## 概要

现有三维形状生成方法难以直接对连续隐式表示（如符号距离场）进行高效建模，因为隐式场包含大量冗余信息，训练计算成本高；而基于预训练潜空间或表示转换的方法则导致生成多样性不足或质量下降。本文提出神经小波域扩散方法，核心思路是将隐式表面在小波域分解为粗系数（捕捉整体结构）与细节系数（捕捉精细特征），并采用截断有符号距离场减少冗余，从而构建一个紧凑的小波表示。在此表示之上，使用去噪扩散概率模型直接生成粗系数体积，再通过细节预测网络从粗系数回归细节系数，最后经逆小波变换和Marching Cubes提取显式网格。在ShapeNet Chair和Airplane类别上，该方法在覆盖率、最大均值差异和1-近邻准确率三项指标上均超越IM-GAN、SPAGHETTI、Voxel-GAN等现有方法，消融实验验证了细节预测器和小波表示对生成质量的关键贡献。该方法以紧凑小波表示替代传统隐式场或潜空间，为扩散模型在三维形状生成中的应用提供了新的技术路径。

## 核心方法与创新机理

### 问题瓶颈与核心思路

现有三维形状生成方法面临一个根本性瓶颈：连续隐式表示（如有符号距离场 SDF）虽然能表达任意拓扑和精细几何，但其体素化形式包含大量冗余信息——物体内部和远离表面的区域对形状表达贡献极小，却占据同等计算资源。直接在此类高维冗余表示上进行生成建模，导致训练计算成本高昂，且生成器难以有效捕捉形状分布的本质结构。现有工作试图通过预训练潜空间（如 IM-GAN 使用隐式场自编码器的潜码）或表示转换（如将隐式场转为点云再生成）来规避此问题，但潜空间的压缩往往牺牲了生成多样性，而表示转换则引入累积误差导致质量下降。

本方法的核心洞察在于：**隐式表面在小波域具有天然的多尺度稀疏性**——粗尺度系数捕捉整体拓扑和主体结构，细节系数仅编码局部精细几何。通过截断有符号距离场（TSDF）将数值范围压缩至 $[-0.1, 0.1]$，可进一步滤除远离表面的冗余区域，使信号能量高度集中于表面附近。在此基础上，采用双正交小波变换将 TSDF 分解为多尺度系数，仅保留 $J=3$ 尺度的粗系数与细节系数对，即可构建一个紧凑且信息充分的小波表示。扩散概率模型在此紧凑表示上进行生成，既避免了潜空间的多样性损失，又绕开了原始 TSDF 的高维冗余问题。

### 关键创新槽位（Changed Slots）

本方法相对于现有工作的核心改变体现在四个技术槽位上：

**槽位一：形状隐式表示——从原始 TSDF / 潜空间隐式场到紧凑小波表示。** 基线方法（如 IM-GAN）使用原始 TSDF 体素或基于自编码器的潜空间隐式场作为生成对象。前者维度高、冗余大；后者依赖预训练编码器，潜空间分布受限于训练数据的编码能力。本方法提出将 TSDF 经截断和双正交小波分解后，仅保留 $J=3$ 尺度的粗系数体积 $C_0$ 和细节系数体积 $D_0$ 作为紧凑表示。实验表明（Section 4.1），仅使用约 3% 的系数（$J=3$ 粗系数）即可重建 TSDF，幅度变化仅 2.8%，验证了粗系数已保留主要结构信息。细节系数则补充精细几何，形成“粗结构 + 细细节”的解耦表示。

**槽位二：生成模型——从 GAN 到去噪扩散概率模型（DDPM）。** 基线方法普遍采用 GAN 框架（IM-GAN、SPAGHETTI、Voxel-GAN），依赖对抗训练来匹配数据分布。GAN 训练存在模式坍塌风险，且生成多样性受限于判别器的容量。本方法采用 DDPM 作为生成器，通过逐步去噪从高斯噪声中生成粗系数体积 $C_0$。扩散模型的似然训练范式天然鼓励覆盖完整数据分布，与紧凑小波表示的低维特性结合，使训练稳定且生成多样。

**槽位三：细节增强模块——从无到细节预测网络。** 基线方法直接生成完整隐式场，未对多尺度信息进行显式建模。本方法引入独立的细节预测网络，以生成的粗系数 $C_0$ 为条件，通过回归预测对应的细节系数 $D_0$。这一“先全局后局部”的生成策略将形状生成分解为两个子任务：扩散模型负责全局结构，细节预测网络负责局部细节补充，降低了单一模型的建模难度。

**槽位四：训练目标——从对抗损失 / 重构损失到噪声预测均方误差。** 基线 GAN 方法使用对抗损失，潜空间方法使用自编码器的重构损失。本方法的扩散生成器采用简化的均方误差损失，直接预测添加到粗系数上的噪声：

$$L_2 = \mathbb{E}_{t, C_0, \varepsilon} \left[ \| \varepsilon - \varepsilon_\theta(C_t, t) \|^2 \right], \quad \varepsilon \sim \mathcal{N}(0, I)$$

其中 $C_t$ 为在时间步 $t$ 经噪声污染后的粗系数，$\varepsilon_\theta$ 为 3D U-Net 预测的噪声。此损失函数避免了 GAN 的 min-max 优化不稳定性，且在小波表示的紧凑空间中收敛高效。

### 方法框架与模块序列

整体方法分为三个递进阶段：数据准备（一次性预处理）、形状学习（训练）、形状生成（推理）。各模块之间的因果关系如下：

**阶段一：数据准备（Data Preparation）**

1. **TSDF 提取与截断**：对每个输入三角网格，计算其有符号距离场并截断至 $[-0.1, 0.1]$。截断操作将远离表面的区域统一设为边界值，大幅减少后续小波变换需要编码的活跃信息量。这一步骤直接决定了紧凑表示的稀疏程度。

2. **多尺度小波分解**：对截断后的 TSDF 体素应用双正交小波变换（合成小波消失矩 6，分析小波消失矩 8），迭代分解至 $J=3$ 尺度。每一级分解将输入体积分离为低通滤波的粗系数和高通滤波的细节系数。最终保留 $J=3$ 的粗系数体积 $C_0$ 和对应尺度的细节系数体积 $D_0$ 作为紧凑表示。选择双正交小波而非 Haar 小波的关键原因在于：Haar 小波的不连续性会在重建中引入严重的体素化伪影（Figure 3d），而高消失矩的双正交小波能产生平滑的表面重建（Figure 3b-c）。

**阶段二：形状学习（Shape Learning）**

3. **扩散生成器训练（3D U-Net + 自注意力）**：生成器采用改进的 3D U-Net 架构，在瓶颈层嵌入自注意力机制以捕捉全局结构依赖。训练遵循 DDPM 范式：对真实粗系数 $C_0$ 逐步添加高斯噪声得 $C_t$，生成器 $\varepsilon_\theta$ 学习从 $C_t$ 和时间步 $t$ 预测所添加的噪声 $\varepsilon$，损失函数为上述 $L_2$。此模块建立了从随机噪声到粗系数分布的映射，是形状全局结构生成的核心。

4. **细节预测网络训练（3D U-Net）**：细节预测网络同样采用 3D U-Net 架构（不含自注意力），以真实粗系数 $C_0$ 为输入，通过回归预测对应的细节系数 $D_0$。训练目标为最小化预测细节系数与真实细节系数之间的均方误差。此模块学习粗-细节系数之间的条件映射关系，使后续推理时能从生成的粗系数恢复一致的细节几何。

**阶段三：形状生成（Shape Generation）**

5. **扩散采样生成粗系数**：从标准高斯噪声 $\mathcal{N}(0, I)$ 开始，迭代执行 DDPM 的反向去噪过程，逐步生成粗系数体积 $C_0$。方差调度采用 $\sigma_t = \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \beta_t$，其中 $\bar{\alpha}_t$ 为累积信号保留率，$\beta_t$ 为噪声添加率。

6. **细节预测**：将生成的 $C_0$ 输入训练好的细节预测网络，输出对应的细节系数 $D_0$。

7. **逆小波变换与网格提取**：对 $\{C_0, D_0\}$ 执行一系列逆小波变换（从 $J=3$ 逐级上溯至原始分辨率），重建完整 TSDF。随后使用 Marching Cubes 算法从重建 TSDF 中提取显式三角网格，得到最终生成的三维形状。

### 模块间因果关系

整个框架的设计遵循“压缩-生成-增强-重建”的因果链条：

- **截断 TSDF → 小波分解**：截断创造了稀疏性前提，使小波分解的能量集中于表面附近，确保粗系数即能捕获主体结构。
- **小波分解 → 扩散生成器**：紧凑表示的低维度（仅约 3% 系数量）使扩散模型能在合理计算资源下有效学习形状分布，避免了在高维 TSDF 上直接扩散的困难。
- **扩散生成器 → 细节预测网络**：生成器输出的粗系数 $C_0$ 已确定形状的全局拓扑和主体几何，细节预测网络仅需补充局部高频信息，两个网络各司其职，降低了各自的学习难度。
- **细节预测网络 → 逆小波变换**：细节系数 $D_0$ 的预测质量直接影响最终网格的精细程度和表面光滑性；若去除细节预测器（消融实验 Table 2），COV CD 从 58.19 降至 54.20，验证了此模块对生成质量的因果贡献。

### 关键公式与变量含义

扩散生成器的训练损失已在上文给出。推理阶段的反向扩散过程遵循 DDPM 标准公式，从 $t=T$ 到 $t=1$ 迭代去噪，每一步根据预测噪声 $\varepsilon_\theta$ 更新 $C_{t-1}$。方差调度 $\sigma_t$ 的公式中，$\bar{\alpha}_t = \prod_{s=1}^t \alpha_s$ 为累积信号保留系数，$\beta_t = 1 - \alpha_t$ 为单步噪声添加量。此调度控制着扩散过程中信号与噪声的比例变化，影响生成样本的多样性与质量平衡。

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2209_08725/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our approach. (a) Data preparation builds a compact wavelet representation (a pair of coarse and detail coefficient volumes) for each input shape using a truncated signed distance field (TSDF) and a multi-scale wavelet decomposition. (b) Shape learning trains the generator network to produce coarse coefficient volumes from random noise samples and trains the detail predictor network to produce detail coefficient volumes from coarse coefficient volumes. (c) Shape generation employs the trained generator to produce a coarse coefficient volume and then the trained detail predictor to further predict a compatible detail coefficient volume, followed by an inverse wavelet transform an...*

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2209_08725/figures/006_Figure_6.jpg]]
*Figure 6: Shape novelty analysis. Top: From our generated shape (in green), we retrieve top-four most similar shapes (in blue) in training set by CD and LFD. Bottom: We generate 500 chairs using our method; for each chair, we retrieve the most similar shape in the training set by LFD; then, we plot the distribution of LFDs for all retrievals, showing that our method is able to generate shapes that are more similar (low LFDs) or more novel (high LFDs) compared to the training set. Note that the generated shape at*

## 实验与关键发现

### 主实验结果：生成质量与多样性的全面验证

论文在ShapeNet的Chair和Airplane两个类别上，采用与现有方法完全一致的评估协议（MMD、COV、1-NNA三项指标，分别基于Chamfer Distance（CD）和Earth Mover‘s Distance（EMD）），与IM-GAN、SPAGHETTI、Voxel-GAN等方法进行定量对比。Table 1的数据表明，本方法在几乎所有评测组合上均取得最优结果。

在Chair类别上，本方法的COV CD达到**58.19%**，超越IM-GAN的57.68%（+0.51%），MMD CD降至**11.70×10⁻³**（IM-GAN为12.91，下降1.21），1-NNA CD降至**61.47%**（IM-GAN为70.72%，下降9.25个百分点）。在Airplane类别上，优势更为显著：COV CD达到**64.78%**，远超IM-GAN的58.34%（+6.44%）；MMD CD降至**3.230×10⁻³**（IM-GAN为4.062，下降0.832）。COV指标衡量生成样本覆盖训练集多样性的能力，MMD衡量生成分布与真实分布的整体差异，1-NNA则通过最近邻分类精度评估生成样本的真实性——三项指标的同步改善，说明本方法不仅生成的形状质量更高，且多样性更充分，未出现模式坍塌。

值得注意的是，Airplane类别上的提升幅度明显大于Chair类别。Airplane具有更规则的几何结构和更明确的部件组成（机身、机翼、尾翼），小波表示可能更有效地捕捉其结构规律；而Chair类别形态变异更大（扶手椅、吧台椅、办公椅等），结构复杂性更高，对所有方法都构成更大挑战。

### 消融实验：关键模块的因果贡献

Table 2通过系统消融揭示了三个核心设计选择的因果作用（均在Chair类别上评测）。

**细节预测器的作用**：去除细节预测器（W/o detail predictor）后，COV CD从58.19降至**54.20**（下降3.99个百分点），COV EMD从55.46降至**50.96**（下降4.50个百分点），MMD和1-NNA也同步劣化。这直接验证了细节系数对生成质量的关键贡献——粗系数虽能保留整体结构，但缺乏细节系数会导致生成的形状表面粗糙、精细结构缺失。细节预测器通过学习从粗系数到细节系数的条件映射，以回归方式补全了扩散模型未直接生成的精细几何信息。

**扩散模型与小波表示的协同**：将生成器替换为VAD生成器（即变分自编码器架构）后，COV CD骤降至**21.83**，性能坍塌式下降。这证明了扩散概率模型在学习小波系数分布上的有效性——小波系数的高维连续分布需要扩散模型的逐步去噪机制才能准确建模，而VAE的潜空间假设可能无法捕捉其复杂结构。

**紧凑小波表示的必要性**：直接预测TSDF（Direct predict TSDF）的COV CD仅为**50.51**，显著低于完整方法的58.19。TSDF的原始表示包含大量冗余信息（体素网格中大量值为截断边界的区域），直接生成面临维度灾难和训练困难。小波变换将信息压缩至约3%的系数中（J=3尺度），使扩散模型能够聚焦于形状的关键结构特征，从而提升生成质量。

### 视觉质量与结构新颖性

Figure 5的视觉对比显示，本方法生成的形状在细节丰富度和表面清洁度上明显优于对比方法。IM-GAN生成的形状常出现表面噪声和不完整结构，SPAGHETTI的生成结果存在部件断裂和拓扑错误，Voxel-GAN受限于体素分辨率而产生阶梯状伪影。相比之下，本方法得益于双正交小波（消失矩6/8）的平滑重建特性（Figure 3验证），避免了Haar小波导致的体素化伪影，生成的网格表面光滑、细节清晰。

Figure 6的新颖性分析进一步表明，本方法并非简单记忆训练样本。通过Light Field Descriptor（LFD）检索最相似训练样本，生成形状的LFD距离分布覆盖了从高度相似（低LFD）到高度新颖（高LFD）的广泛区间，且第50百分位的生成形状与训练集最近邻已存在显著差异。这说明扩散模型在小波表示上学习到了可泛化的形状先验，能够生成训练集中未曾出现的新颖结构。

### 失败模式与适用边界

需要指出的是，论文将局限性讨论置于补充材料，正文未提供具体内容，因此以下分析基于实验数据的间接推断，需人工核实补充材料。

从Table 1的1-NNA指标来看，Airplane类别上本方法的1-NNA CD为**71.69%**，而IM-GAN为70.72%——本方法在该指标上并未取得优势，甚至略有劣化。1-NNA衡量的是生成样本与真实样本的区分难度，该结果可能暗示在Airplane这一结构相对规整的类别上，本方法生成的形状在局部几何细节上与真实样本仍存在可察觉差异，扩散模型可能过度平滑了某些高频特征。

此外，实验仅在ShapeNet的两个类别（Chair和Airplane）上验证，且均为刚性、部件明确的人造物体。对于具有极细细节（如植物、毛发）或高度可变拓扑（如服装）的类别，小波表示能否有效压缩并保留关键信息，扩散模型能否学习其分布，仍是开放问题。论文提出的开放问题也指出，将该方法扩展至三维场景生成和条件生成（如图像或点云条件下的形状重建）是需要进一步探索的方向。

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2209_08725/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison between the generated shapes produced by our method and four state-of-the-art methods. We follow the same setting to conduct this experiment as in the state-of-the-art methods. From the table, we can see that our generated shapes have the best quality for almost all cases (lowest MMD, largest COV, and lowest 1-NNA) for both the Chair and Airplane categories. The units of CD and EMD are*

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2209_08725/figures/007_Table_2.jpg]]
*Table 2: Comparing our full pipeline with various ablated cases on the Chair category. The units of CD and EMD are*

## 定位与知识库关联

### 一、相对已有方法的本质差异

本工作在“形状隐式表示”与“生成模型”两个关键slot上同时做出了改变，形成了与现有三维形状生成方法的本质差异。

**改变slot 1：形状隐式表示——从原始隐式场到紧凑小波表示。** 已有方法（如IM-GAN、SPAGHETTI）直接操作原始TSDF或依赖预训练潜空间进行生成，面临隐式表示冗余度高、训练计算成本大的瓶颈。本工作将TSDF截断至$[-0.1, 0.1]$后，通过双正交小波变换分解为粗系数与细节系数，仅保留$J=3$尺度的系数对作为紧凑表示。实验证据表明，仅用约3%的系数量即可重建TSDF，幅度变化仅2.8%，证明粗系数已保留主要结构信息（Section 4.1）。这一表示转换是方法有效性的核心前提——它使扩散模型能够在低维、信息密集的空间中学习形状分布，而非在冗余的高维隐式场上直接操作。

**改变slot 2：生成模型——从GAN到扩散概率模型。** 主流方法多采用GAN框架（如IM-GAN、SPAGHETTI、Voxel-GAN），依赖对抗训练生成形状。本工作改用去噪扩散概率模型（DDPM）直接在小波粗系数体积上建模分布，训练目标为预测噪声的均方误差$L_2 = E_{t, C_0, \epsilon} [ \| \epsilon - \epsilon_\theta(C_t, t) \|^2 ]$。消融实验中的决定性证据是：将扩散生成器替换为VAD生成器后，COV CD从58.19骤降至21.83（Table 2），验证了扩散模型在小波表示上学习形状分布的有效性远超GAN方案。

**改变slot 3：细节增强机制——从端到端生成到条件回归。** 已有方法通常试图一次性生成完整形状，而本工作引入独立的细节预测网络，以粗系数为条件回归细节系数。消融实验表明，去除细节预测器后COV CD从58.19降至54.20（Table 2），直接预测TSDF而不使用小波表示则COV CD仅为50.51，证明“粗系数生成+细节条件回归”的两阶段策略对生成质量有决定性贡献。

综合来看，本工作改变的因果链条是：**紧凑小波表示（降低冗余）→ 扩散模型在粗系数上学习全局结构分布（保证多样性与质量）→ 细节预测网络从粗系数回归精细结构（增强局部细节）**。这一链条使得方法在MMD、COV、1-NNA三项指标上全面超越IM-GAN等baseline（Table 1），同时生成形状展现出更复杂的结构、更细粒度的细节和更干净的表面（Figure 5）。

### 二、知识库挂载点

本工作可挂载到以下知识库节点：

**1. 隐式场的小波压缩（连接多尺度表示与形状生成）。** 本工作受Velho et al.（1994）多尺度小波隐式表示的启发，将其首次引入三维形状生成任务。挂载点在于：小波变换为连续隐式场提供了一种信息论上高效的紧凑编码，粗尺度系数捕捉全局拓扑，细节系数编码局部几何。这一表示策略为其他需要处理高维隐式场的生成任务（如神经辐射场生成）提供了可迁移的压缩范式。

**2. 扩散模型在结构化三维数据上的应用（连接DDPM与三维生成）。** 本工作将DDPM应用于小波系数体积，而非原始体素或点云。挂载点在于：扩散模型的逐步去噪过程天然适合学习多尺度结构，而小波表示恰好将尺度信息显式化，二者形成协同。这为扩散模型在三维领域的应用提供了一个“先压缩、再生成”的通用框架。

**3. 三维形状生成评估协议（连接ShapeNet基准）。** 本工作在ShapeNet Chair和Airplane类别上，采用MMD、COV、1-NNA三项标准指标进行评估，与IM-GAN、SPAGHETTI、Voxel-GAN等方法直接可比。挂载点在于：该方法在标准benchmark上建立了新的性能基线，可作为后续三维生成工作的对比参照。

### 三、适用边界

**类别泛化边界。** 当前实验仅在ShapeNet的Chair和Airplane两个类别上进行验证。这些类别具有相对规整的结构和有限的结构多样性。论文未提供在更复杂类别（如具有极细细节的物体、有机形状）或三维场景上的实验结果，因此方法在这些场景下的有效性尚需验证。

**表示分辨率边界。** 小波表示在$J=3$尺度上运行，对应特定的体素分辨率。对于需要极高几何精度的应用（如工业CAD），当前表示可能不足以捕捉微米级细节。此外，截断距离$[-0.1, 0.1]$的选择可能影响对薄结构或尖锐特征的保真度。

**扩散模型效率边界。** DDPM的采样过程需要多步迭代去噪，推理速度慢于单步前馈的GAN方法。论文未报告生成单形状的推理时间，这一效率瓶颈在实时或交互式应用中可能成为限制。

**局限性信息缺失。** 论文将局限性讨论置于补充材料，正文未提供具体内容。上述边界推断基于方法设计和实验设置，需人工确认。

### 四、后续研究启发

**1. 条件生成扩展。** 当前方法仅支持无条件生成。将小波表示与扩散模型结合的条件生成框架（如基于图像、点云或文本提示的形状生成）是一个自然的扩展方向。小波表示的多尺度特性可能有助于在不同尺度上注入条件信号。

**2. 时空三维生成。** 论文提出小波表示是否适用于动画生成中的时空三维表示的问题。将时间维度纳入小波分解（如三维小波+时间轴处理），可能为四维动态形状生成提供紧凑表示。

**3. 表示学习的通用化。** “压缩隐式场→扩散生成”的框架可推广至其他隐式表示（如NeRF、SDF的神经编码），为高维隐式数据的生成建模提供通用方案。关键在于寻找适合目标数据特性的变换基。

**4. 扩散模型效率优化。** 将扩散模型的采样加速技术（如DDIM、一致性模型）应用于小波域生成，有望在保持生成质量的同时显著提升推理速度，拓展方法的实际应用场景。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Neural_Wavelet_domain_Diffusion_for_3D_Shape_Generation.pdf]]