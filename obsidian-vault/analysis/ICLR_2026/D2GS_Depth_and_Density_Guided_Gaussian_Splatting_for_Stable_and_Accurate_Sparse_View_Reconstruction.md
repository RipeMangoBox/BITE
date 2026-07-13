---
title: "D$^2$GS: Depth-and-Density Guided Gaussian Splatting for Stable and Accurate Sparse-View Reconstruction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/D_2_GS_Depth_and_Density_Guided_Gaussian_Splatting_for_Stable_and_Accurate_Spars_24092536ec5d.pdf
project_link: "https://insta360-research-team.github.io/DDGSwebsite/"
code_link: null
aliases:
- D2DDGGS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 高斯原语的局部密度与到相机的深度距离：近处高密度导致过度重建，远处低密度导致重建不足。
primary_logic: 通过深度与密度联合引导的自适应Dropout机制，抑制近场冗余高斯以缓解过拟合；同时利用单目深度估计掩码加强远场区域监督，提升欠拟合区域的重建细节。
claims:
- 近场区域（绿色框）稀疏视图模型生成11450个高斯，远超稠密视图的6112个，表明严重过拟合。
- 远场区域（红色框）仅生成3082个高斯，明显少于稠密视图的5224个，导致欠拟合。
- D2GS在LLFF 3视图1/8分辨率下PSNR达到21.35 dB，SSIM 0.746，LPIPS 0.179，AVGE 0.087，全面超越所有基线。
- D2GS在MipNeRF360数据集上PSNR达到20.09 dB，比DropGaussian提高0.35 dB。
---

# D$^2$GS: Depth-and-Density Guided Gaussian Splatting for Stable and Accurate Sparse-View Reconstruction

> [!tip] 核心洞察
> 通过深度与密度联合引导的自适应Dropout机制，抑制近场冗余高斯以缓解过拟合；同时利用单目深度估计掩码加强远场区域监督，提升欠拟合区域的重建细节。

| 字段 | 内容 |
|------|------|
| 中文题名 | 深度与密度引导的高斯泼溅：面向稀疏视图的稳定精确重建 |
| 英文题名 | D$^2$GS: Depth-and-Density Guided Gaussian Splatting for Stable and Accurate Sparse-View Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7yvz93kBw9) · [Project](https://insta360-research-team.github.io/DDGSwebsite/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | D^2GS (Depth-and-Density Guided Gaussian Splatting) |
| Dataset | LLFF, MipNeRF360, DTU |

> [!tip] 效果简介
> - LLFF (3-view, 1/8分辨率) 上，PSNR 21.35 vs 20.76 (DropGaussian) (+0.59 dB)。
> - LLFF (3-view, 1/4分辨率) 上，PSNR 20.56 vs 20.01 (DropGaussian) (+0.55 dB)。
> - MipNeRF360 (12-view) 上，PSNR 20.09 vs 19.74 (DropGaussian) (+0.35 dB)。

## 概要

### 问题瓶颈

三维高斯泼溅（3DGS）在稀疏视图设置下面临严重的**近场过拟合**与**远场欠拟合**的结构性矛盾。Figure 1 揭示了这一现象的定量证据：在近场区域（绿色框），稀疏视图模型生成了 11,450 个高斯原语，远超稠密视图（55 视图）的 6,112 个，表明高斯原语在近处过度堆积，导致伪影和混叠；而在远场区域（红色框），稀疏视图仅生成 3,082 个高斯原语，明显少于稠密视图的 5,224 个，造成细节模糊和重建不足。这一瓶颈的因果根源在于：高斯原语的**局部密度**与**到相机的深度距离**之间存在系统性失配——近处高密度导致过度重建，远处低密度导致重建不足。

### 核心方法

D²GS（Depth-and-Density Guided Gaussian Splatting）通过两个互补模块解决上述矛盾：

- **DD-Drop（深度与密度引导的自适应 Dropout）**：为每个高斯原语分配一个基于归一化深度和局部密度的 Dropout 分数 $S_i = \omega_{depth} \tilde{d}_i + \omega_{density} \tilde{\rho}_i$，并通过全局深度分层衰减因子 $\lambda_{middle}$、$\lambda_{far}$ 进一步调制，使近场冗余高斯以更高概率被移除，从而抑制过拟合。Dropout 比例在训练过程中线性增加 $r(t) = r_{min} + (r_{max} - r_{min}) \frac{\min(t, T)}{T}$，实现渐进式正则化。

- **DAFE（距离感知保真度增强）**：利用单目深度估计器（DepthAnything V2）预测的深度图生成远场掩码 $M_{dis}(x,y)$，仅对远场区域施加额外的 L1 损失 $L_{DAFE}$，增强对欠拟合区域的监督信号，提升远场重建细节。

此外，D²GS 提出了**模型间鲁棒性指标 IMR**，将 3DGS 模型抽象为高斯混合分布，通过近似 2-Wasserstein 距离量化独立训练模型间的一致性，弥补了传统图像域指标（PSNR/SSIM/LPIPS）无法衡量训练稳定性的缺陷。

### 方法谱系与知识库定位

D²GS 建立在 3DGS（Kerbl et al., 2023）的基础框架之上，与现有稀疏视图 3DGS 方法形成差异化定位：

- 相较于 **DropGaussian** 采用的均匀随机 Dropout 策略，D²GS 的 DD-Drop 引入了深度与密度的结构化先验，使 Dropout 具有空间自适应性。
- 相较于 **DNGaussian**（Li et al., 2024）的深度正则化，D²GS 不仅利用深度进行正则化，更将深度信息同时用于 Dropout 引导和远场监督增强。
- 相较于 **FSGS**（Zhu et al., ECCV 2024）和 **CoR-GS**（Zhang et al., ECCV 2024）通过伪视图生成或共正则化来弥补视图稀疏性，D²GS 从高斯原语分布调控的角度直接解决过拟合与欠拟合的根源问题。

### 主要结果

在 LLFF 数据集 3 视图、1/8 分辨率设置下，D²GS 达到 **PSNR 21.35 dB，SSIM 0.746，LPIPS 0.179**，全面超越 DropGaussian（PSNR 20.76 dB）等基线方法。在 MipNeRF360 数据集 12 视图设置下，D²GS 达到 **PSNR 20.09 dB**，比 DropGaussian 提高 0.35 dB。在模型鲁棒性方面，D²GS 的 IMR 指标在 LLFF 3 视图和 6 视图下分别达到 **3.039** 和 **3.109**，为所有方法中最低，表明模型间一致性最强。

消融实验证实：单独加入密度得分将基础 PSNR 从 19.22 提升至 21.02，加入深度得分后进一步提升至 21.10，完整 DD-Drop 达到 21.17，最终加入 DAFE 模块后达到 21.35，验证了各组件的独立贡献。

### 局限与开放问题

DD-Drop 仍需手工设定的深度阈值和固定权重系数，可能无法充分捕捉复杂场景的特异性先验。IMR 指标仅关注模型间一致性，尚未考虑动态视图合成下的感知稳定性。值得探索的方向包括：自适应 Dropout 调度策略替代手工深度阈值、可学习的监督掩码改善场景特异性、以及面向动态视图合成的感知时间稳定性指标。

### 稀疏视图重建的核心矛盾

3D高斯泼溅（3DGS）在稠密多视图重建中展现了卓越的渲染质量与实时性能，但当输入视图极度稀疏（如3–6张）时，其重建质量会出现严重退化。这种退化并非均匀分布，而是呈现鲜明的空间不对称性：**近场区域过拟合产生伪影，远场区域欠拟合导致细节模糊**。

Figure 1 通过对比稠密视图（55张）与稀疏视图（3张）下的高斯原语分布，揭示了这一瓶颈的因果机制。在近场区域（绿色框），稀疏视图模型生成了11,450个高斯原语，远超稠密视图的6,112个——过量且冗余的高斯原语在训练视图上过度拟合，导致渲染出现锯齿状伪影。相反，在远场区域（红色框），稀疏视图模型仅生成3,082个高斯原语，明显少于稠密视图的5,224个——高斯覆盖不足使得这些区域缺乏足够的表达能力，重建细节严重丢失。

### 现有方法的缺口

当前面向稀疏视图的3DGS改进方法主要沿两个方向展开：

- **深度正则化方法**（如 **DNGaussian**，Li et al., 2024）通过引入单目深度估计作为几何先验约束高斯分布，但缺乏对过拟合区域的针对性抑制。
- **Dropout策略方法**（如 **DropGaussian**）采用均匀随机Dropout来减少高斯原语数量，但忽略了深度与密度的空间异质性——近场区域的高斯密度天然高于远场，均匀Dropout无法精准识别并抑制过拟合热点。
- **伪视图生成方法**（如 **CoR-GS**，Zhang et al., ECCV 2024；**FSGS**，Zhu et al., ECCV 2024）通过生成额外视图或迭代优化来扩充监督信号，但计算开销显著增加，且未从根本上解决高斯分布的空间失衡问题。

这些方法的共同缺口在于：**缺乏一种空间自适应的机制，能够感知高斯原语的局部密度与深度距离，从而差异化地调控近场与远场的表达能力**。

### 本文动机

D$^2$GS的核心动机源于一个关键观察：**高斯原语的过程与不足，本质上是其局部密度与到相机深度距离的函数**。近场区域高斯密集是过拟合的温床，远场区域高斯稀疏是欠拟合的根源。这一因果关系的识别，为设计空间自适应的Dropout策略提供了理论锚点。

基于此，D$^2$GS提出两个互补机制：
1. **深度与密度引导的自适应Dropout（DD-Drop）**：根据每个高斯原语的局部密度和深度距离计算Dropout分数，高分数的高斯以更高概率被移除，从而精准抑制近场过拟合。
2. **距离感知保真度增强（DAFE）**：利用单目深度估计生成远场掩码，对远场区域施加额外的L1损失，强化欠拟合区域的监督信号。

此外，稀疏视图下3DGS训练的随机性导致不同训练轮次之间渲染质量高度不一致（Figure 3左），现有图像域指标（PSNR/SSIM/LPIPS）无法捕捉这种模型间的不稳定性。为此，D$^2$GS提出基于高斯混合分布间Wasserstein距离的**模型间鲁棒性指标（IMR）**，从几何一致性角度量化重建的可靠性。

## 核心方法与创新机理

D$^2$GS 针对稀疏视图下 3DGS 的过拟合与欠拟合并存问题，提出了三个相互协同的关键创新，构成一个完整的“抑制–增强–评估”闭环。

### 1. 深度与密度引导的自适应 Dropout（DD-Drop）

现有稀疏视图 3DGS 方法（如 **DropGaussian**）采用均匀随机 Dropout 策略，忽略了高斯原语在空间分布上的结构性差异——近场区域高斯过密导致过拟合伪影，远场区域高斯稀疏导致细节模糊。DD-Drop 将 Dropout 从“无差别删减”转变为“空间自适应正则化”，其核心机制包含两个层次：

**局部分数计算**：为每个高斯原语 $G_i$ 计算一个 Dropout 分数 $S_i$，由归一化深度 $\tilde{d}_i$ 和局部密度 $\tilde{\rho}_i$ 的加权和给出：

$$S_i = \omega_{depth} \tilde{d}_i + \omega_{density} \tilde{\rho}_i$$

其中深度越小（越靠近相机）、局部密度越高的高斯原语获得更高的 Dropout 分数，表明其更可能造成过拟合。

**全局分层衰减**：考虑到远场区域本身高斯覆盖不足，直接按局部分数 Dropout 会加剧欠拟合。DD-Drop 引入深度分层衰减因子，将 Dropout 概率 $P_i$ 按深度区间调制：

$$P_i = \begin{cases} S_i, & d_i \leq D_{near}, \\ \lambda_{middle} S_i, & D_{near} < d_i \leq D_{middle}, \\ \lambda_{far} S_i, & d_i > D_{middle} \end{cases}$$

其中 $\lambda_{middle} < \lambda_{far} \ll 1$，确保 Dropout 操作主要集中在近场过拟合区域，而对远场区域几乎不施加删减压力。此外，全局 Dropout 比例 $r(t)$ 在训练过程中从 $r_{min}$ 线性增长至 $r_{max}$，实现渐进式正则化。

这一设计的因果逻辑清晰：**深度指示“过拟合风险的空间位置”，密度量化“过拟合的严重程度”**，两者联合引导 Dropout 精确作用于冗余高斯，而非无差别削弱模型容量。

### 2. 距离感知保真度增强损失（DAFE）

DD-Drop 解决了近场过拟合，但远场欠拟合问题仍需额外的监督信号。DAFE 模块通过单目深度估计器（如 **DepthAnything V2**）预测的深度图构建远场掩码，对远场区域施加额外的 L1 重建损失。

远场掩码 $M_{dis}$ 定义为：

$$M_{dis}(x,y) = \begin{cases} 1, & \text{if } D(x,y) > \tau D_{max}, \\ 0, & \text{otherwise} \end{cases}$$

其中 $\tau$ 为深度阈值，控制远场区域的比例。DAFE 损失仅在掩码激活的像素上计算：

$$L_{DAFE} = \frac{1}{\sum M_{dis}} \sum_{x,y} M_{dis}(x,y) \cdot \| \hat{I}(x,y) - I(x,y) \|_1$$

最终训练目标将 DAFE 损失与标准 L1、D-SSIM 损失联合优化：

$$L_{total} = L_1(\hat{I}, I) + \lambda_{SSIM} L_{D-SSIM}(\hat{I}, I) + \lambda_{DAFE} L_{DAFE}(\hat{I}, I)$$

该设计的精妙之处在于：**DAFE 并非对所有像素均匀加力，而是通过深度先验精确锁定欠拟合的远场区域**，避免了对已充分重建的近场区域引入冗余约束。

### 3. 模型间鲁棒性指标（IMR）

稀疏视图训练的 3DGS 存在严重的训练不稳定性——同一场景的多次独立训练可能产生渲染质量差异显著的模型。现有指标（PSNR、SSIM、LPIPS）仅评估单模型与真值的偏差，无法量化模型间的结构一致性。IMR 从“分布对齐”角度填补了这一空白。

IMR 的计算流程为：将每个 3DGS 模型抽象为以不透明度为权重的高斯混合分布，计算模型对之间的混合 Wasserstein 距离，再通过加权差异惩罚模型间不一致性：

$$\mathrm{IMR} = \ln\left(\frac{\sum_{1 \leq i < j \leq N} S_{ij}^2}{\sum_{1 \leq i < j \leq N} S_{ij}}\right)$$

其中 $S_{ij}$ 为模型 $i$ 与 $j$ 之间的高斯分布距离。IMR 值越低，表明多次训练得到的模型在几何结构上越一致，方法鲁棒性越强。

### 创新点总结

三个创新形成因果闭环：**DD-Drop 抑制近场过拟合（减），DAFE 增强远场监督（加），IMR 量化模型间鲁棒性（评）**。相较于 DropGaussian 的均匀随机 Dropout 和现有方法的无差别损失，D$^2$GS 首次将深度与密度信息同时编码为 Dropout 的先验引导和损失的空间权重，实现了稀疏视图下高斯原语分布的显式结构调控。

D$^2$GS 的整体流程以稀疏视图图像为输入，首先通过 Structure-from-Motion（SfM）从输入图像中提取初始点云与相机位姿。随后，该初始点云被送入一个包含两个核心模块的 3DGS 训练管线中：**深度与密度引导的自适应 Dropout（DD-Drop）** 模块和**距离感知保真度增强（DAFE）** 模块。DD-Drop 模块在训练过程中根据每个高斯原语的局部密度和相机距离计算 Dropout 分数，自适应地移除近场区域中冗余的高斯原语，以抑制过拟合；DAFE 模块则利用单目深度估计器预测的深度图生成远场掩码，对远场区域施加额外的 L1 损失，从而增强欠拟合区域的监督信号。训练完成后，D$^2$GS 还引入了一个**模型间鲁棒性指标（IMR）**，通过将独立训练的多个 3DGS 模型抽象为高斯混合分布，并计算它们之间的 Wasserstein 距离来量化模型在稀疏视图条件下的训练稳定性和一致性。整个框架的输入输出流和模块关系如 Figure 2 所示。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_7yvz93kBw9/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of*

### DD-Drop：深度与密度引导的自适应 Dropout

DD-Drop 的核心思想源于一个关键观察：在稀疏视图设置下，近场区域的高斯原语数量远超稠密视图（11450 vs 6112），表明存在严重的局部过拟合；而远场区域的高斯原语数量则明显不足（3082 vs 5224），导致欠拟合。为缓解这一不平衡，DD-Drop 为每个高斯原语分配一个 Dropout 分数 $S_i$，该分数由归一化深度分数 $\tilde{d}_i$ 和归一化密度分数 $\tilde{\rho}_i$ 的加权和给出：

$$S_i = \omega_{depth} \tilde{d}_i + \omega_{density} \tilde{\rho}_i$$

其中，深度分数反映高斯原语到相机的距离（近处分数更高），密度分数反映其局部邻域内的原语密集程度。在此基础上，DD-Drop 引入全局深度分层衰减机制，将 Dropout 概率 $P_i$ 按深度区间进一步调制：

$$P_i = \begin{cases} S_i, & d_i \leq D_{near}, \\ \lambda_{middle} S_i, & D_{near} < d_i \leq D_{middle}, \\ \lambda_{far} S_i, & d_i > D_{middle} \end{cases}$$

同时，全局 Dropout 比例 $r(t)$ 在训练过程中线性增长，以逐步强化正则化效果：

$$r(t) = r_{min} + (r_{max} - r_{min}) \frac{\min(t, T)}{T}$$

这种“局部打分 + 全局分层衰减 + 时变比例”的三层设计，使得 DD-Drop 能够精准地抑制近场过拟合，同时避免对远场区域产生不必要的干扰。

### DAFE：距离感知保真度增强

DAFE 模块针对远场区域监督不足的问题，利用单目深度估计器（如 DepthAnything V2）预测的深度图 $D(x,y)$ 生成远场掩码 $M_{dis}$：

$$M_{dis}(x,y) = \begin{cases} 1, & \text{if } D(x,y) > \tau D_{max}, \\ 0, & \text{otherwise} \end{cases}$$

其中 $\tau$ 为深度阈值，$D_{max}$ 为深度图的最大值。DAFE 损失仅在远场区域计算 L1 损失：

$$L_{DAFE} = \frac{1}{\sum M_{dis}} \sum_{x,y} M_{dis}(x,y) \cdot \| \hat{I}(x,y) - I(x,y) \|_1$$

最终，整体训练目标将标准 L1 损失、D-SSIM 损失与 DAFE 损失相结合：

$$L_{total} = L_1(\hat{I}, I) + \lambda_{SSIM} L_{D-SSIM}(\hat{I}, I) + \lambda_{DAFE} L_{DAFE}(\hat{I}, I)$$

通过这一设计，DAFE 在不增加近场区域监督负担的前提下，显著提升了远场区域的重建细节。

### IMR：模型间鲁棒性评估

为量化稀疏视图下 3DGS 模型训练的稳定性，D$^2$GS 提出 IMR 指标。其计算流程如 Figure 3 所示：首先将每个 3DGS 模型抽象为以不透明度为权重的高斯混合分布：

$$G_i = \sum_{j=1}^{K_i} w_{i,j} \cdot N(m_{i,j}, \Sigma_{i,j}), \quad w_{i,j} = \frac{\alpha_{i,j}}{\sum_{k=1}^{K_i} \alpha_{i,k}}$$

然后通过引入熵正则化的最优传输问题求解混合 Wasserstein 距离，并采用深度分层重要性采样策略选取约 10,000 个高斯原语以保证计算可处理性。最终，IMR 通过加权差异惩罚模型对之间的不一致性：

$$\mathrm{IMR} = \ln\left(\frac{\sum_{1 \leq i < j \leq N} S_{ij}^2}{\sum_{1 \leq i < j \leq N} S_{ij}}\right)$$

IMR 值越低，表明多次独立训练得到的模型在几何结构上越一致，即模型鲁棒性越强。

### 深度与密度引导的自适应Dropout（DD-Drop）

稀疏视图下3DGS的核心瓶颈在于高斯原语的分布失配：近场区域因高斯密度过高导致过拟合（产生伪影），远场区域因覆盖不足导致欠拟合（细节模糊）。DD-Drop通过**局部分数**与**全局分层衰减**的联合机制，自适应地抑制近场冗余高斯。

**局部Dropout分数**定义为归一化深度与密度分数的加权和：

$$S_i = \omega_{depth} \tilde{d}_i + \omega_{density} \tilde{\rho}_i$$

其中 $\tilde{d}_i$ 为高斯原语 $i$ 到相机的归一化深度，$\tilde{\rho}_i$ 为其局部邻域内的归一化高斯密度。$\omega_{depth}$ 和 $\omega_{density}$ 为权重系数（消融实验表明 $\omega_{depth}=0.5$、$\omega_{density}=0.5$ 时性能最优）。深度越小（越近）、密度越高，$S_i$ 越大，该高斯被丢弃的概率越高。

**全局分层衰减**将场景沿深度方向划分为近、中、远三个区域，对Dropout概率施加分层调制：

$$P_i = \begin{cases} S_i, & d_i \leq D_{near}, \\ \lambda_{middle} S_i, & D_{near} < d_i \leq D_{middle}, \\ \lambda_{far} S_i, & d_i > D_{middle} \end{cases}$$

其中 $D_{near}$ 和 $D_{middle}$ 为深度阈值，$\lambda_{middle}$ 和 $\lambda_{far}$ 为衰减因子（$\lambda_{far} < \lambda_{middle} < 1$）。这一设计确保近场高密度区域的高斯被优先剪枝，而远场高斯得以保留。

**时变全局Dropout率**在训练过程中线性增长，实现从保守到激进的渐进式剪枝：

$$r(t) = r_{min} + (r_{max} - r_{min}) \frac{\min(t, T)}{T}$$

其中 $r_{min}$ 和 $r_{max}$ 分别为最小和最大Dropout比例，$T$ 为总迭代次数。每轮训练中，按 $P_i$ 降序排列，选择前 $r(t)$ 比例的高斯原语执行Dropout。

### 距离感知保真度增强（DAFE）

DAFE模块针对远场欠拟合问题，通过单目深度估计器生成的深度图构建距离感知掩码，对远场区域施加额外的重建监督。

**远场掩码**通过深度阈值 $\tau$ 将渲染视图划分为近场和远场：

$$M_{dis}(x,y) = \begin{cases} 1, & \text{if } D(x,y) > \tau D_{max}, \\ 0, & \text{otherwise} \end{cases}$$

其中 $D(x,y)$ 为像素 $(x,y)$ 的单目深度估计值，$D_{max}$ 为当前视图的最大深度。

**DAFE损失**仅在远场区域计算L1损失，增强该区域的重建精度：

$$L_{DAFE} = \frac{1}{\sum M_{dis}} \sum_{x,y} M_{dis}(x,y) \cdot \| \hat{I}(x,y) - I(x,y) \|_1$$

**总训练目标**将DAFE损失与标准L1和D-SSIM损失联合优化：

$$\boldsymbol{L}_{\mathrm{total}} = \boldsymbol{L}_{1}(\hat{I}, I) + \lambda_{\mathrm{SSIM}} \boldsymbol{L}_{\mathrm{D-SSIM}}(\hat{I}, I) + \lambda_{\mathrm{DAFE}} \boldsymbol{L}_{\mathrm{DAFE}}(\hat{I}, I)$$

消融实验表明 $\lambda_{\mathrm{DAFE}}=1.0$ 时达到最佳LPIPS（0.179），同时PSNR和SSIM最优。

### 模型间鲁棒性度量（IMR）

IMR旨在量化独立训练模型之间的一致性，其核心是将每个3DGS模型抽象为以不透明度为权重的混合高斯分布：

$$G_i = \sum_{j=1}^{K_i} w_{i,j} \cdot \mathcal{N}(m_{i,j}, \Sigma_{i,j}), \quad w_{i,j} = \frac{\alpha_{i,j}}{\sum_{k=1}^{K_i} \alpha_{i,k}}$$

其中 $m_{i,j}$ 为高斯中心，$\Sigma_{i,j}$ 为协方差矩阵（由缩放和旋转参数构造），$\alpha_{i,j}$ 为不透明度。

**近似2-Wasserstein距离**采用Bures距离的一阶泰勒近似，避免矩阵平方根计算：

$$\tilde{W}_2^2(\mu_1,\mu_2) = \| m_1 - m_2 \|^2 + \frac{1}{4} \mathrm{tr}\big((\Sigma_1 - \Sigma_2) \Sigma_2^{-1} (\Sigma_1 - \Sigma_2)\big)$$

**IMR指标**通过加权差异惩罚模型对之间的不一致性：

$$\mathrm{IMR} = \ln\left(\frac{\sum_{1 \leq i < j \leq N} S_{ij}^2}{\sum_{1 \leq i < j \leq N} S_{ij}}\right)$$

其中 $S_{ij}$ 为模型 $i$ 与 $j$ 之间的混合Wasserstein距离。IMR值越低，表明模型间一致性越强。在LLFF 3视图设定下，D²GS的IMR达到3.039，优于DropGaussian的3.205。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_7yvz93kBw9/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of Gaussian primitives and rendered images between dense views (55 views) and sparse views (3 views) settings. Overfitting occurs in the near field (green box), while underfitting appears in the far field (red box). The number of Gaussian primitives in the corresponding field is shown below the images*

## 实验与关键发现

### 瓶颈验证：稀疏视图下的过拟合与欠拟合

D²GS的核心动机源自对3DGS在稀疏视图下失败模式的精确诊断。如图1所示，在仅使用3张视图的稀疏设定下，近场区域（绿色框）生成了11450个高斯原语，远超稠密视图（55视图）下的6112个；而远场区域（红色框）仅生成3082个高斯原语，明显少于稠密视图的5224个。这一现象揭示了稀疏视图3DGS的结构性缺陷：**近场区域因高斯原语过度密集导致过拟合，产生漂浮物等伪影；远场区域因高斯覆盖不足导致欠拟合，细节严重模糊**。D²GS正是围绕这一“近场过密—远场过疏”的因果瓶颈展开设计。

### 主实验结果

**LLFF数据集（3视图）**。表1汇总了LLFF数据集上3视图稀疏设定下的定量对比。D²GS在1/8分辨率下取得PSNR 21.35 dB、SSIM 0.746、LPIPS 0.179、AVGE 0.087，全面超越所有基线方法。相比DropGaussian的20.76 dB，PSNR提升0.59 dB；相比CoR-GS（Zhang et al., ECCV 2024）的20.53 dB，提升0.82 dB。在1/4分辨率下，D²GS同样保持最优，PSNR达20.56 dB，较DropGaussian提升0.55 dB。图4的定性对比进一步验证：D²GS有效消除了近场漂浮伪影，同时保持了远场区域的清晰结构。

**MipNeRF360数据集**。表2展示了MipNeRF360数据集上的12视图稀疏重建结果。D²GS以PSNR 20.09 dB位居榜首，较DropGaussian（19.74 dB）提升0.35 dB，较CoR-GS（19.52 dB）提升0.57 dB。在更大规模、更复杂的前向场景中，DD-Drop与DAFE的联合作用依然稳定。

**扩展视图设定**。在LLFF 6视图设定下（表8），D²GS取得PSNR 24.84 dB，较DropGaussian（24.43 dB）提升0.41 dB。在MipNeRF360 24视图设定下，D²GS同样保持最优。在DTU数据集上（表9），3视图设定下D²GS PSNR达21.25 dB，较DropGaussian（20.29 dB）提升0.96 dB，优势进一步扩大。

### 模型鲁棒性分析

稀疏视图下3DGS存在严重的训练不稳定性——同一设定下多次独立训练会产生高度不一致的重建结果。D²GS提出**模型间鲁棒性指标IMR**（Inter-Model Robustness），将每个3DGS模型抽象为高斯混合分布，通过熵正则化的混合Wasserstein距离量化模型间的结构一致性。IMR值越低，表示独立训练模型间的几何一致性越强。

表3显示，在LLFF 3视图和6视图设定下，D²GS的IMR分别为3.039和3.109，在所有方法中最低（DropGaussian分别为3.205和3.184）。这表明DD-Drop通过抑制近场冗余高斯，不仅提升了单模型质量，还显著增强了训练过程的稳定性与可复现性。

### 消融实验

**模块有效性**（表4）。以无任何正则化的基础3DGS为起点（PSNR 19.22 dB），单独引入密度得分将PSNR提升至21.02 dB；进一步加入深度得分后提升至21.10 dB；完整的DD-Drop（含全局分层衰减）达到21.17 dB。最终加入DAFE模块后，PSNR达到21.35 dB，SSIM 0.746，LPIPS 0.179，IMR 3.039，所有指标达到最优。这表明DD-Drop与DAFE分别针对过拟合和欠拟合问题，二者互补且不可或缺。

**超参数敏感性**（表5）。DD-Drop的深度权重ω_depth与密度权重ω_density在均为0.5时取得最优PSNR 21.16 dB，过高偏向任一因子均导致性能下降，验证了联合引导的必要性。DAFE损失系数λ_DAFE=1.0时达到最佳LPIPS 0.179，同时PSNR和SSIM最优。

**深度估计器选择**（表6）。使用DepthAnything V2（Yang et al., 2024）作为单目深度估计器取得最高PSNR 21.35 dB，优于MiDas（Ranftl et al., 2022）和DPT（Ranftl et al., 2021），表明更精确的深度先验对DAFE模块的远场掩码生成至关重要。

### 训练效率

表7报告了LLFF 3视图设定下的训练时间对比。D²GS的训练耗时与DropGaussian基本持平，显著低于CoR-GS等需要额外伪视图生成的方法。DD-Drop的密度信息每500次迭代更新一次，深度信息每迭代更新，额外计算开销可控。

### 局限性与待验证问题

尽管D²GS在多个基准上取得一致优势，仍存在以下局限：（1）DD-Drop依赖手工设定的深度阈值（D_near、D_middle）和固定权重系数，可能无法充分捕捉复杂场景的特异性先验；（2）IMR指标仅度量模型间几何一致性，尚未覆盖动态视图合成下的感知时间稳定性。这些方向值得后续探索，但当前证据已充分支撑D²GS在稀疏视图重建中的有效性。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_7yvz93kBw9/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Comparison on LLFF dataset (Mildenhall et al., 2019). Comparisons were conducted with 3DGS, CoR-GS, DropGaussian. Our method effectively avoids the artifacts and maintains accurate reconstructions*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_7yvz93kBw9/figures/006_Table_2.jpg]]
*Table 2: Performance comparisons of sparse-view synthesis on MipNeRF360 dataset. The best, second-best, and third-best entries are marked in red, orange, and yellow, respectively*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_7yvz93kBw9/figures/007_Table_3.jpg]]
*Table 3: IMR comparison on LLFF Dataset with 3- view and 6-view Settings. All results are tested on ten independent training models*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_7yvz93kBw9/figures/008_Table_4.jpg]]
*Table 4: Ablation Study on proposed components. The ✓indicates adding the module*

## 定位与知识库关联

### 问题定位与核心瓶颈

D²GS 瞄准的是**稀疏视图 3D 高斯泼溅（3DGS）**场景中的结构性失败模式：在仅提供 3–6 张输入视图的条件下，标准 3DGS 及其变体会同时遭受**近场过拟合**与**远场欠拟合**的双重困境。论文通过定量证据揭示了这一瓶颈的物理根源——

- **近场过拟合**：在 Figure 1 的绿色框区域，先前方法生成了 11,450 个高斯原语，远超稠密视图（55 视图）下的 6,112 个，表明高斯在相机邻近区域过度增殖，产生混叠伪影。
- **远场欠拟合**：同一场景的红色框区域仅生成 3,082 个高斯原语，明显少于稠密视图的 5,224 个，导致远处纹理细节模糊甚至缺失。

这一现象的因果机制可归结为：**高斯原语的局部密度与到相机的深度距离形成非均匀分布**——近处高密度导致过度重建，远处低密度导致重建不足。D²GS 的贡献正是在这一因果链条上引入可控的干预机制。

### 与基线方法的关系网络

D²GS 建立在 **3DGS**（Kerbl et al., 2023）的基础框架之上，但不同于直接沿用原始 3DGS 训练策略的稀疏视图方法，它从**正则化**和**监督增强**两个维度对现有工作进行了系统性改进。

**与 DropGaussian 的关系**：DropGaussian 是 D²GS 最直接的对比基线和实现基础（论文明确指出其代码基于 DropGaussian 构建）。DropGaussian 采用**均匀随机 Dropout** 策略来抑制过拟合，但这一策略忽视了高斯原语的空间分布异质性——近场和远场区域被以相同概率丢弃，无法针对性地解决前述双重困境。D²GS 将均匀 Dropout 替换为**基于深度和密度的自适应 Dropout（DD-Drop）**，使 Dropout 概率成为局部场景复杂度的函数，从而在近场冗余区域施加更强的正则化，同时保留远场稀疏区域的高斯原语。

**与 FSGS 和 CoR-GS 的关系**：**FSGS**（Zhu et al., ECCV 2024）和 **CoR-GS**（Zhang et al., ECCV 2024）代表了稀疏视图 3DGS 的另一条技术路线——通过生成伪视图或共正则化来扩充有效监督信号。D²GS 与这些方法形成互补而非替代关系：FSGS/CoR-GS 侧重**增加视图覆盖**，而 D²GS 侧重**优化已有视图下的高斯分布质量**。实验结果表明，D²GS 在 LLFF 3 视图 1/8 分辨率下 PSNR 达到 21.35 dB，分别超过 FSGS（20.16 dB）和 CoR-GS（20.47 dB）达 1.19 dB 和 0.88 dB（Table 1），证明分布优化策略在极稀疏设置下的有效性。

**与 DNGaussian 的关系**：**DNGaussian**（Li et al., 2024）首次将深度正则化引入 3DGS 稀疏视图训练，但其深度信息主要用于约束高斯原语的几何一致性。D²GS 的 DAFE 模块将深度先验的使用方式从**几何正则化**转向**监督增强**——利用单目深度估计器生成的远场掩码，仅对欠拟合区域施加额外的 L1 损失，形成更具针对性的保真度提升机制。

**与 LoopSparseGS 的关系**：**LoopSparseGS**（Bao et al., 2025）通过循环一致性增强稀疏初始化的质量，属于 SfM 初始化阶段的改进。D²GS 的 DD-Drop 和 DAFE 模块作用于训练过程本身，与 LoopSparseGS 在流程上前后衔接，可视为互补组件。

### 方法谱系中的创新维度

D²GS 在 3DGS 稀疏视图方法谱系中引入了三个独特的创新维度：

1. **空间自适应 Dropout 机制**：不同于 DropGaussian 的均匀随机丢弃，DD-Drop 通过局部分数 $S_i = \omega_{depth} \tilde{d}_i + \omega_{density} \tilde{\rho}_i$ 和全局分层衰减因子 $\lambda_{middle}, \lambda_{far}$，实现了深度感知的差异化正则化。这一设计将 Dropout 从盲目的模型容量控制工具转变为**场景结构感知的过拟合抑制器**。

2. **深度引导的监督增强**：DAFE 模块通过远场掩码 $M_{dis}(x,y)$ 和仅在远场区域计算的 L1 损失，实现了对欠拟合区域的定向监督增强。这与传统的全局损失加权策略形成对比——后者可能在不必要地增强近场监督的同时，未能充分补偿远场的监督稀疏性。

3. **模型间鲁棒性量化**：IMR 指标将独立训练的 3DGS 模型抽象为高斯混合分布，通过近似 2-Wasserstein 距离 $\tilde{W}_2^2$ 和最优传输理论量化模型间的一致性。这一指标填补了稀疏视图 3DGS 在**训练稳定性评估**方面的空白——传统 PSNR/SSIM 仅衡量单次训练的渲染质量，无法反映不同随机种子下模型的输出方差。

### 适用边界与局限

D²GS 的适用边界受以下因素约束：

- **深度先验依赖性**：DD-Drop 的深度分数和 DAFE 的远场掩码均依赖单目深度估计器的输出质量。消融实验（Table 6）表明，使用 DepthAnything V2 时 PSNR 达到 21.35 dB，而使用 MiDas 时降至 20.89 dB，说明方法性能与深度估计器的精度强相关。在深度估计器失效的场景（如无纹理墙面、重复纹理区域），DD-Drop 的分层衰减可能引入错误的先验偏置。

- **手工阈值限制**：DD-Drop 仍需手工设定深度阈值 $D_{near}, D_{middle}$ 和固定权重系数 $\omega_{depth}, \omega_{density}$。尽管消融实验（Table 5）给出了最优参数组合（$\omega_{depth}=0.5, \omega_{density}=0.5$），但这些参数可能无法充分捕捉复杂场景的特异性先验——例如在近场包含重要细节（如前景文字）的场景中，过强的近场 Dropout 可能反而损害重建质量。

- **IMR 指标的感知局限性**：IMR 仅关注模型间高斯分布的一致性，尚未考虑动态视图合成下的感知稳定性。两个模型可能在高斯分布层面高度一致，但在特定视角的渲染结果上仍存在人类可感知的差异。

### 开放问题

论文提出的框架引出以下有待探索的方向：

1. **自适应深度阈值调度**：能否用可学习的 Dropout 调度策略替代手工深度阈值？例如，将 $D_{near}$ 和 $D_{middle}$ 参数化为场景特征的函数，或通过元学习在多个场景间共享先验。

2. **可学习监督掩码**：DAFE 的远场掩码目前由固定的深度阈值 $\tau$ 决定。可学习的掩码生成器（例如轻量 CNN 预测逐像素监督权重）能否进一步改善场景特异性，同时避免对深度估计器精度的过度依赖？

3. **感知时间稳定性指标**：能否开发考虑感知时间稳定性的鲁棒性指标，用于动态视图合成场景？IMR 的 Wasserstein 距离框架可扩展至时序高斯分布序列，衡量模型在相邻帧间的输出一致性。

4. **与伪视图方法的深度融合**：DD-Drop 和 DAFE 目前仅利用输入视图的深度信息。结合 FSGS 或 CoR-GS 生成的伪视图深度，能否在更极端的稀疏设置（如 2 视图）下维持重建质量？

## 原文 PDF

![[paperPDFs/ICLR_2026/D_2_GS_Depth_and_Density_Guided_Gaussian_Splatting_for_Stable_and_Accurate_Spars_24092536ec5d.pdf]]
