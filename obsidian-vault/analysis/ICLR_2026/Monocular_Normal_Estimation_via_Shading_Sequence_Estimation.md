---
title: "Monocular Normal Estimation via Shading Sequence Estimation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Monocular_Normal_Estimation_via_Shading_Sequence_Estimation.pdf
project_link: null
code_link: https://github.com/LMozart/ICLR2026-RoSE.git
openreview_forum_id: d7itDxMD1n
aliases:
- MNESSE
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "将单目法向估计重构为视频扩散明暗序列生成加OLS求解。"
primary_logic: "RoSE先从灰度图生成多个规范平行光下的明暗序列，再用普通最小二乘从多光照约束解析恢复法向图。"
claims:
- "明暗序列比直接法向图对细粒度几何变化更敏感，能缓解三维几何失配和过平滑。"
- "CLIP全局条件和VAE局部条件共同引导视频扩散U-Net生成规范光照下的明暗序列。"
- "MultiShade的多材质合成训练数据提升了模型在真实物体法向估计上的泛化。"
- "RoSE在DiLiGenT和LUCES上优于此前单目法向估计方法，9个规范光源取得较好精度效率平衡。"
---

# Monocular Normal Estimation via Shading Sequence Estimation

> [!tip] 核心洞察
> Monocular

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Monocular Normal Estimation via Shading Sequence Estimation |
| 英文题名 | Monocular Normal Estimation via Shading Sequence Estimation |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=d7itDxMD1n) · [GitHub](https://github.com/LMozart/ICLR2026-RoSE.git) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

单目法向估计旨在从单张二维图像中恢复物体表面的逐像素三维朝向。现有方法普遍采用从图像直接回归法向图的端到端范式，但这类方法面临一个根本性瓶颈：**三维几何错位**——估计的法向图在视觉上可能看似合理，但重建的曲面往往丢失了精确的几何细节，呈现过度平滑的结果（Figure 2）。

本文提出了一种范式转换：**将单目法向估计重新表述为明暗序列估计任务**。核心思路是，先利用图像到视频的生成模型预测物体在预定义规范平行光下的明暗序列，再通过普通最小二乘法（OLS）从明暗序列解析求解法向图。这一范式将法向估计从“图像→法向”的直接映射 $`\Phi: \mathbf{I} \to \mathbf{N}`$ 重构为“灰度图→明暗序列→法向”的两阶段流程 $`\Phi_S: \mathbf{I}_g \to \mathbf{S}^s`$。明暗序列表示对几何变化具有更高的灵敏度（Figure 3），为生成模型提供了更丰富的监督信号。

基于该范式，本文提出了 **RoSE** 方法。RoSE 采用视频扩散 U-Net 作为明暗生成器，以灰度输入图像为条件，通过 CLIP 嵌入与 VAE 潜变量拼接的双分支条件策略引导生成过程，并在合成数据集 **MultiShade** 上进行训练。

在真实世界基准数据集上的实验结果显示，RoSE 取得了领先性能：在 **DiLiGenT** 数据集上，MAE 达到 **16.36°**，优于此前最优的单目方法 NiRNE（17.27°）（Table 1）；在 **LUCES** 数据集上同样表现突出（Table 2）。消融实验表明，9 个规范光源的配置在精度与效率之间取得最优平衡。



从单张图像恢复物体表面法线是计算机视觉中的经典任务，其核心挑战在于：输入图像是几何、材质与光照三者耦合的结果，而仅凭单目观测无法唯一地分解这些因素。现有主流方法大多采用端到端的数据驱动策略，直接从 RGB 图像回归法线图。这些方法虽然在视觉上能产生看似合理的法线估计，但存在一个隐蔽而关键的问题——**三维几何失配（3D misalignment）**：估计的法线图在整体外观上可能正确，但由其重建的表面往往缺乏准确的几何细节，呈现出过度平滑的结果（见 **Figure 2**）。这意味着，仅凭法线图的视觉质量并不足以保证底层几何的准确性。

进一步分析表明，这一问题的根源在于**法线图表示本身对几何变化的敏感性不足**。如 **Figure 3** 所示，通过平均总变差（Total Variation）度量，法线图在不同几何细节下的响应强度明显弱于本文提出的**着色序列（shading sequence）表示**。着色序列记录的是物体在多个预定义平行光源下的着色响应，其像素值直接随表面朝向变化，因此对几何细节具有更强的区分能力。这一观察构成了本文方法设计的核心动机。

基于上述洞察，本文提出了一个**新的范式转换**：将单目法线估计重新定义为着色序列估计任务。具体而言，给定任意光照下的单张输入图像，首先利用图像到视频生成模型预测物体在一组规范平行光下的着色序列，再通过普通最小二乘法（OLS）从着色序列解析导出法线图。这一范式将困难的法线直接回归问题，转化为生成模型更擅长的高维序列预测问题，同时利用物理约束保证了几何精度。

为实现这一范式，本文提出了 **RoSE**（**R**estoration of **S**urface normal from **E**stimated shading sequence），并构建了大规模合成数据集 **MultiShade**，涵盖 5657 种 PBR 材质与多样化的光照条件，以支持模型在通用场景下的训练。在真实世界基准数据集 DiLiGenT 和 LUCES 上的实验表明，RoSE 在单目法线估计任务中达到了当时的最优性能（MAE 分别为 16.36° 和 14.48°），验证了着色序列作为中间表示的有效性。



## 核心方法与创新机理

RoSE 的核心创新在于将单目法向估计**重新定义为明暗序列估计（shading sequence estimation）**，从而将问题从直接的图像到法向映射 $\Phi: \mathbf{I} \to \mathbf{N}$ 转化为一个两阶段流程：先用图像到视频生成模型预测物体在多个预定义平行光源下的明暗序列 $\Phi_S: \mathbf{I}_g \to \mathbf{S}^s$，再通过普通最小二乘法解析求解法向图。

这一范式转换的关键洞察在于**表示形式的敏感性差异**：法向图对几何细节变化不够敏感，容易产生“视觉上正确但三维重建时几何失准”的过平滑结果；而明暗序列对局部几何变化具有更高的敏感性（Figure 3 中以平均总变分 TV 度量验证），使得生成模型能够更忠实地捕捉细粒度几何信息。

具体而言，RoSE 在方法层面引入了以下 **changed slots**：

1. **任务重定义**：将法向估计 $\Phi: \mathbf{I} \to \mathbf{N}$ 替换为明暗序列估计 $\Phi_S: \mathbf{I}_g \to \mathbf{S}^s$，其中 $\mathbf{S}^s \triangleq \{ \mathbf{S}_i \mid i \in 1, \dots, f \}$，每个明暗图定义为 $\mathbf{S} \triangleq \{ \mathbf{s}_{\mathrm{p}} = \max(\mathbf{n}_{\mathrm{p}} \cdot \mathbf{l}, 0) \mid \mathrm{p} \in \mathscr{P} \}$。最终法向由求解 $\min_{\mathbf{n}} \sum_i \|\mathbf{s}_i - \max(\mathbf{n} \cdot \mathbf{l}_i, 0)\|^2$ 得到。

2. **生成模型架构**：采用视频扩散 U-Net 作为明暗生成器 $g_\theta(\cdot)$，以灰度图像 $\mathbf{I}_g$ 为输入，通过双分支条件注入（CLIP 嵌入提供全局引导，VAE 潜在拼接提供局部引导）生成明暗序列。训练使用 $\mathbf{z}_0$-重参数化扩散损失 $\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\mathbf{z}_0, c, t} \|\mathbf{z}_0 - \hat{\mathbf{z}}_0\|^2$。

3. **训练数据与增强**：构建 MultiShade 合成数据集（约 300 万图像-法向对），从 MatSynth 的 5657 个 PBR 材质中按概率采样（金属/非金属各 0.25），以覆盖多样化材质与光照条件。

在 DiLiGenT 基准上，RoSE 以 **MAE 16.36°** 超越此前最优单目方法 **NiRNE** 的 17.27°（Table 1），提升 0.91°。这一改进的因果机制在于：明暗序列作为中间表示，迫使模型隐式学习物理上一致的光照-几何关系，而非直接回归可能产生几何失准的法向图。消融实验进一步表明，移除明暗序列的负值裁剪（w/o clamp）或材质增强（w/o MA）均会导致性能退化，验证了各设计选择的必要性。

**证据强度评估**：DiLiGenT 上的对比数据来自 Table 1，置信度 0.98，属于强证据。但需注意，当前分析未提供 NiRNE 之外的完整 baseline 对比细节，且缺乏关于“明暗序列敏感性优势”的定量消融（仅 Figure 3 提供定性可视化），该因果链条的严格验证需进一步确认。



![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_d7itDxMD1n/figures/001_Figure_1.jpg]]
*Figure 1: We present RoSE, a method using a video generative model for monocular normal map estimation, built on a new paradigm that reformulates normal estimation as a shading sequence estimation task. Results on complex and diverse scenarios show that RoSE reconstructs fine-grained geometric details and generalizes robustly to unseen datasets, achieving state-of-the-art performance in object-based monocular normal estimation on benchmark datasets*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_d7itDxMD1n/figures/004_Figure_5.jpg]]
*Figure 5: Pipeline of RoSE. Given a monocular RGB image under arbitrary light, RoSE first converts it into a grayscale image, which is then used to generate the shading sequence via a video diffusion model. This generation is guided by two complementary feature representations extracted from a CLIP encoder and a VAE encoder. Finally, an ordinary least squares problem is solved analytically to estimate the normal map from the generated shading sequence. We train the video diffusion model while freezing the CLIP and the VAE encoder*

RoSE 将单目法向估计重构为**着色序列估计**任务，整体 pipeline 由三个核心阶段串联而成：输入预处理 → 视频扩散着色生成器 → 解析法向求解器。

**输入预处理。** 给定一张任意光照下的单目 RGB 图像 $\mathbf{I}$，首先将其转换为灰度图像 $\mathbf{I}_g$。这一步剥离了颜色信息，使后续生成器专注于几何线索，而非材质与光照的颜色耦合。消融实验表明，使用 RGB 输入会导致 LUCES 上 MAE 劣化 0.79°（Table 6），验证了灰度预处理的必要性。

**着色序列生成。** 灰度图像 $\mathbf{I}_g$ 被送入一个基于视频扩散 U-Net 的着色生成器 $g_\theta(\cdot)$，其目标是预测物体在一组预定义**规范平行光**下的着色序列 $\mathbf{S}^s = \{\mathbf{S}_i \mid i = 1, \dots, f\}$。单个着色图定义为 $\mathbf{S} \triangleq \{ \mathbf{s}_{\mathrm{p}} = \max(\mathbf{n}_{\mathrm{p}} \cdot \mathbf{l}, 0) \mid \mathrm{p} \in \mathscr{P} \}$，即法向与光源方向点积的非负截断。生成器采用双分支条件注入策略：CLIP 嵌入提供全局语义引导，VAE 潜在拼接提供局部结构引导。扩散训练使用 $z_0$-重参数化损失 $\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\mathbf{z}_0, c, t} \|\mathbf{z}_0 - \hat{\mathbf{z}}_0\|^2$。生成后，着色序列经负值截断并线性缩放至 $[-1, 1]$ 以适配 VAE 编码器。

**解析法向求解。** 获得着色序列后，法向图通过求解一个**普通最小二乘**问题解析导出。由于每个像素在多个已知光源方向下的着色值构成线性方程组，法向可直接闭合求解，无需可学习参数。

整个 pipeline 的输入是单张任意光照 RGB 图像，输出是高质量法向图 $\mathbf{N}$，中间表示着色序列作为几何信息的可泛化载体，将生成模型的先验与物理约束解耦。



### 范式重构：从法向估计到明暗序列估计

RoSE 的核心创新在于将单目法向估计任务重新定义为**明暗序列估计**任务。传统方法直接学习从输入图像 $\mathbf{I}$ 到法向图 $\mathbf{N}$ 的映射 $\Phi : \mathbf{I} \to \mathbf{N}$，而 RoSE 转而学习从灰度输入图像 $\mathbf{I}_g$ 到明暗序列 $\mathbf{S}^s$ 的映射 $\Phi_S : \mathbf{I}_g \to \mathbf{S}^s$，再通过解析求解器从明暗序列中恢复法向图。

**明暗图**定义为法向与光源方向的夹紧点积：

$$\mathbf{S} \triangleq \{ \mathbf{s}_{\mathrm{p}} = \max(\mathbf{n}_{\mathrm{p}} \cdot \mathbf{l}, 0) \mid \mathrm{p} \in \mathscr{P} \}$$

其中 $\mathbf{n}_{\mathrm{p}}$ 为像素 $\mathrm{p}$ 处的表面法向，$\mathbf{l}$ 为光源方向，负值被夹紧至零以符合物理约束。

**明暗序列**则是在多个预定义规范平行光源下获得的一组明暗图：

$$\mathbf{S}^s \triangleq \{ \mathbf{S}_i \mid i \in 1, \dots, f \}$$

其中 $f$ 为光源数量，实验表明 $f = 9$ 时性能最优（在 LUCES 上相比 6 光源提升 10.74°，而 12 光源反而下降 1.31°）。

### 明暗序列生成器

明暗生成器 $g_\theta(\cdot)$ 基于标准视频扩散 U-Net 架构实现，由多个空间和时间 Transformer 块组成。该架构沿用了 Voleti et al., 2024 的设计。

**双分支条件注入**策略是生成器的关键设计：
- **全局引导**：通过 CLIP 嵌入提供语义级条件
- **局部引导**：通过 VAE 潜在特征拼接提供空间级条件

输入图像首先被转换为灰度图，以剥离无关的颜色信息，迫使模型聚焦于几何相关的明暗变化。消融实验证实，使用 RGB 输入会导致性能下降 0.79°（MAE 从 14.48° 升至 15.27°）。

### 扩散训练损失

训练采用 $\mathbf{z}_0$-重参数化的扩散损失：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\mathbf{z}_0, c, t} \left\| \mathbf{z}_0 - \hat{\mathbf{z}}_0 \right\|^2$$

其中 $\hat{\mathbf{z}}_0$ 为模型从带噪潜在变量 $\mathbf{z}_t$ 中预测的干净潜在变量，$c$ 为条件信息，$t$ 为扩散时间步。该损失直接监督去噪输出与目标之间的像素级重建。

### 预处理与后处理

**明暗序列缩放**：在输入 VAE 编码器之前，经负值夹紧后的明暗序列通过线性变换 $S \mapsto S \times 2 - 1$ 重新缩放至 $[-1, 1]$ 区间，以匹配 VAE 编码器的输入要求。

**法向求解**：生成明暗序列后，通过求解普通最小二乘问题从多光照明暗约束中解析恢复法向图。该步骤将生成模型的输出转化为最终的法向估计，无需额外学习参数。

### 训练数据与优化

模型在自建的 **MultiShade** 合成数据集上训练，包含约 300 万对图像-法向对。数据使用 Blender 以 $576 \times 576$ 分辨率渲染，材质来自 MatSynth 数据集（5,657 种高质量 PBR 材质），其中金属和非金属类别各以 0.25 的概率采样。训练使用 8 块 NVIDIA H100 GPU（80GB），优化器为 AdamW，学习率 $1 \times 10^{-5}$。



## 实验与关键发现

### 核心定量结果

RoSE 在两个真实世界基准数据集上均取得单目法向估计的最优性能。在 **DiLiGenT** 数据集上，RoSE 的均值 MAE 为 **16.36°**，优于此前最优的单目方法 **NiRNE**（17.27°），提升幅度为 0.91°（Table 1）。在 **LUCES** 数据集上，RoSE 的均值 MAE 为 **14.48°**，显著优于第二名 **Lotus-G**（17.44°），提升幅度达 2.96°（Table 2）。在合成数据集 **MultiShade** 测试集上，RoSE 的均值角度误差为 **15.37°**（Table 3）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_d7itDxMD1n/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison in terms of MAE (↓) of the normal map on DiLiGenT benchmark dataset. Highlighted numbers indicate the best and second best results among monocular estimation methods*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_d7itDxMD1n/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison in terms of MAE of the normal map on LUCES benchmark dataset (Mecca et al., 2021). Highlighted numbers indicate the best and second best results among monocular estimation methods*

定性结果（Figure 6）显示，RoSE 在 DiLiGenT 的 COW 物体和 LUCES 的 SQUIRREL 物体上，法向图与误差图均表现出对几何细节更好的保真度，误差分布更均匀且无明显结构性偏差。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_d7itDxMD1n/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison on selected objects from two benchmark dataset (COW from DILIGENT (Shi et al., 2016) and SQUIRREL from LUCES (Mecca et al., 2021). Row 1 & 3: normal map comparison. Row 2 & 4: error map comparison.) Best viewed in color with zooming in. Table 3: Quantitative comparison in terms of Mean and Median Angular Errors of the normal map on MultiShade test set, and the percentage of objects below a specific error bound. Highlighted numbers indicate the best and second best results among monocular estimation methods. Analysis on shading sequence estimation. We conduct quantitative analyses1 of the predicted shading sequences on the LUCES dataset to illustrate RoSE’s ability to...*

### 消融实验分析

消融实验在 LUCES 数据集上进行，以均值 MAE 为指标（Table 6），揭示了以下关键设计的作用：

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_d7itDxMD1n/figures/012_Table_6.jpg]]
*Table 6: Ablation study in terms of MAE of the normal map on LUCES benchmark dataset (Mecca et al., 2021). In particular, “+M”(“+L”) means training on Multishade (LightProp) dataset, ‘w/o clamp’ means removing clamping on shading sequence. ‘w/o MA’ means training on dataset without material augmentation. Highlighted numbers indicate the best and second best results*

- **灰度输入 vs. RGB 输入**：将输入从 RGB 替换为灰度图像后，MAE 从 15.27° 降至 14.48°，提升 0.79°。这表明去除颜色信息有助于模型聚焦于几何线索而非纹理干扰。
- **负值钳位（clamping）**：移除对 shading sequence 的负值钳位（即将 max(n·l, 0) 改为保留负值）会导致性能下降（具体数值需查 Table 6 确认）。钳位操作使 shading 表示更符合物理光照模型，有助于后续最小二乘求解的稳定性。
- **材料增强（Material Augmentation, MA）**：在训练时引入 MatSynth 数据集的 5,657 种 PBR 材质（金属与非金属各 0.25 采样概率）对性能有正向贡献。移除材料增强后性能下降（具体数值需查 Table 6 确认），说明多样化材质覆盖对泛化至真实场景至关重要。
- **数据集影响**：在 MultiShade（+M）上训练的模型性能优于在 LightProp（+L）上训练的模型，验证了大规模、多材质合成数据对真实场景泛化的支撑作用。
- **骨干网络替换**：将视频扩散骨干替换为 SVD XL 后，MAE 为 14.58°，与默认配置（14.48°）接近，表明方法对扩散模型架构选择具有一定鲁棒性。

### 光照数量与表示灵敏度

方法设计中，shading sequence 使用 9 个正则平行光源（ring light setup, Figure 4）达到最优。实验表明，从 6 个光源增加到 9 个，LUCES 上角度误差降低 10.74°；继续增加至 12 个光源时，性能反而下降 1.31°。这说明 9 个光源在信息充分性与模型学习难度之间取得了平衡。

### Shading Sequence 估计质量

在 LUCES 数据集上，RoSE 估计的 shading sequence 在 PSNR（20.74）、SSIM 和 LPIPS 三项指标上均达到最优（Table 4），表明视频扩散模型能够有效预测与真实几何一致的多光照 shading 模式。此外，在锐利法向误差（Sharp Normal Error, SNE）指标上，RoSE 达到 26.74，与 NiRNE 相当（Table 5），说明方法在保持边缘锐度方面具有竞争力。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_d7itDxMD1n/figures/010_Table_4.jpg]]
*Table 4: Quantitative comparison on estimated shading sequence in terms of PSNR (↑), SSIM (↑), and LPIPS (↓) on LUCES benchmark dataset (Mecca et al., 2021). Highlighted numbers indicate the best and second best results*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_d7itDxMD1n/figures/011_Table_5.jpg]]
*Table 5: Quantitative analysis in terms of MAE and SNE of the normal map on LUCES benchmark dataset (Mecca et al., 2021). Highlighted numbers indicate the best and second best results*

### 已知局限与失败模式

论文讨论部分（Section 5）指出以下局限，需在阅读时注意：

1. **极端光照条件**：在光照严重不足的场景下，shading sequence 的生成质量可能下降，进而影响法向估计精度。这是 shading-based 方法的固有瓶颈。
2. **计算开销**：视频扩散模型的推理计算量较大，限制了实时应用场景的部署。
3. **材质覆盖边界**：对透明或半透明物体，当前 shading 模型（基于漫反射假设）可能失效，方法尚未支持此类材质。
4. **个别物体表现**：在 DiLiGenT 的 GOBLET 和 LUCES 的 HOUSE 物体上，RoSE 未进入前两名（Table 1, Table 2），可能与非朗伯反射或复杂几何结构有关，具体原因需进一步分析。



## 定位与知识库关联

### 任务范式转换：从直接法向映射到明暗序列估计

传统单目法向估计方法通常学习从输入图像 $\mathbf{I}$ 到法向图 $\mathbf{N}$ 的直接映射 $\Phi : \mathbf{I} \to \mathbf{N}$。RoSE 的核心范式转换在于将这一任务重构为明暗序列估计问题，即学习映射 $\Phi_S : \mathbf{I}_g \to \mathbf{S}^s$，其中 $\mathbf{I}_g$ 为灰度输入图像，$\mathbf{S}^s$ 为在多个规范平行光源下的明暗图序列（论文 Section 3.1）。法向图随后通过求解一个普通最小二乘问题从明暗序列解析导出，无需额外的神经网络推理。

这一范式转换的关键动机在于：明暗序列作为中间表示，对几何变化的敏感性优于直接法向图表示。论文 Figure 3 通过平均总变分（TV）度量验证了这一点——明暗序列在几何细节区域的 TV 值更高，表明其对表面变化具有更强的响应能力。这解释了为什么基于生成模型的明暗序列预测能够恢复更精细的几何细节，而直接法向估计方法（如 Figure 2 所示）往往产生过度平滑的结果，在 3D 重建中出现几何失准。

### 与现有工作的关系

**基于学习的单目法向估计方法。** 在 DiLiGenT 基准上，RoSE 以 16.36° 的平均 MAE 超越了此前最优的单目方法 **NiRNE**（17.27° MAE，Table 1）。在 LUCES 基准上，RoSE 以 14.48° MAE 显著优于 **Lotus-G**（17.44° MAE，Table 2）。这些对比表明，引入视频扩散模型作为明暗序列生成器，相比直接回归法向图的范式具有明显优势。

**视频扩散模型的应用。** RoSE 的 shading generator 基于标准视频扩散 U-Net 架构，由多个空间和时间 Transformer 块组成，遵循 Voleti et al., 2024 的设计。其双分支条件策略结合了 CLIP 嵌入的全局引导和 VAE 潜在拼接的局部引导（Section 3.3）。消融实验（Table 6）显示，将骨干网络替换为 SVD XL 后性能仅轻微下降至 14.58° MAE（vs. 原版 14.48°），表明该方法对扩散模型架构的选择具有一定鲁棒性。

**训练数据策略。** RoSE 在自建的 MultiShade 合成数据集上训练，该数据集包含约 300 万图像-法向对，使用 Blender 以 576×576 分辨率渲染。材料采样策略结合了 MatSynth 数据集（Vecchio & Deschaintre, 2024）中的 5,657 种高质量 PBR 材质，对金属类和非金属类材质各分配 0.25 的采样概率（Section 4）。消融实验（Table 6）证实，MultiShade 数据集（+M）相比 LightProp 数据集（+L）带来了显著的性能提升，验证了多样化材质和光照条件对泛化能力的关键作用。

### 适用边界与关键设计约束

**灰度输入的强制性。** 消融实验（Table 6）表明，使用 RGB 输入替代灰度输入会导致性能下降 0.79°（MAE 从 14.48° 升至 15.27°）。这表明去除颜色信息有助于模型聚焦于几何线索，避免材质颜色对明暗估计的干扰。

**负值钳位的作用。** 移除明暗序列上的负值钳位操作（w/o clamp）会导致性能下降（Table 6），说明将 $\max(\mathbf{n}_p \cdot \mathbf{l}, 0)$ 约束显式编码到数据预处理中对稳定训练和推理是必要的。

**光源数量的敏感性。** 论文报告 9 个规范光源达到最优性能，相比 6 个光源在 LUCES 上提升了 10.74°；但增加到 12 个光源后性能反而下降 1.31°（Section 3 实验证据）。这一非单调关系表明，光源数量过少会导致法向求解的欠定问题，过多则可能引入冗余信息干扰扩散模型的生成质量。

### 局限与开放问题

1. **计算开销。** 论文在 Discussion（Section 5）中明确指出，视频扩散模型的推理计算开销是限制实时应用的主要瓶颈。训练使用 8 块 NVIDIA H100 GPU（80GB），推理阶段的多帧生成成本远高于单帧前馈方法。

2. **极端光照条件下的退化。** 论文提及在光照不足的极端条件下性能可能下降，但未提供定量分析。这一局限源于明暗序列估计对输入图像中可辨识几何线索的依赖——当输入图像本身缺乏足够的 shading 信息时，生成模型难以推断正确的表面朝向。

3. **材质泛化边界。** 论文明确将透明和半透明物体列为当前方法不支持的范围（Section 5）。这是因为渲染方程中的 $\max(\mathbf{n} \cdot \mathbf{l}, 0)$ 假设仅适用于不透明表面的漫反射分量，无法建模折射、次表面散射等复杂光传输现象。

4. **特定物体的性能波动。** 在 DiLiGenT 的 GOBLET 物体和 LUCES 的 HOUSE 物体上，RoSE 未进入前两名（part_006 开放问题）。这可能与这些物体包含的凹面结构、自遮挡或材质特性有关，但论文未提供针对性的失败案例分析。

5. **合成到真实的域间隙。** 尽管 MultiShade 数据集在材质多样性上做了增强，训练数据仍完全来自 Blender 合成渲染。论文未系统分析合成数据与真实基准（DiLiGenT、LUCES）之间的域间隙对性能的具体影响。



## 原文 PDF

![[paperPDFs/ICLR_2026/Monocular_Normal_Estimation_via_Shading_Sequence_Estimation.pdf]]
