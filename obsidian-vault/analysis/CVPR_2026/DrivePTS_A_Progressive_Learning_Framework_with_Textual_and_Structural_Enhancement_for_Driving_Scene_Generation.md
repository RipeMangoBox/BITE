---
title: "DrivePTS: A Progressive Learning Framework with Textual and Structural Enhancement for Driving Scene Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DrivePTS_A_Progressive_Learning_Framework_with_Textual_and_Structural_Enhancement_for_Driving_Scene_Generation.pdf
project_link: null
code_link: null
aliases:
- DrivePTS
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 渐进式学习策略解耦道路与物体几何条件，VLM生成多视角层次化语义描述，以及频率引导的结构损失增强前景高频细节。
primary_logic: 将场景生成分解为“先道路、后物体”的渐进过程，通过交替训练与互信息约束消除条件耦合；利用细粒度多视角场景描述替代单一简短标注；并引入基于傅里叶高通滤波的结构损失以强化道路边缘与物体轮廓。
claims:
- DrivePTS在nuScenes验证集上FID降至11.45，较次优方法PerLDiff下降约16.7%。
- Road mIoU达到63.95，比第二名高出2.69点。
- 在修改地图布局时，MagicDrive无法适应变化，而DrivePTS能成功生成与更新地图对齐的场景。
- 消融实验显示，同时使用MHD、FGSL与MIC可获得最佳综合性能（FID 11.45，Road mIoU 63.95，Vehicle mIoU 27.82）。
---

# DrivePTS: A Progressive Learning Framework with Textual and Structural Enhancement for Driving Scene Generation

> [!tip] 核心洞察
> 将场景生成分解为“先道路、后物体”的渐进过程，通过交替训练与互信息约束消除条件耦合；利用细粒度多视角场景描述替代单一简短标注；并引入基于傅里叶高通滤波的结构损失以强化道路边缘与物体轮廓。

| 字段 | 内容 |
|------|------|
| 中文题名 | DrivePTS：面向驾驶场景生成的渐进式学习框架与文本及结构增强 |
| 英文题名 | DrivePTS: A Progressive Learning Framework with Textual and Structural Enhancement for Driving Scene Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.22549) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DrivePTS |
| Dataset | NuScenes validation set, NuScenes test set, NuScenes |

> [!tip] 效果简介
> - NuScenes validation set 上，FID↓ 11.45 vs 13.36 (PerLDiff) (-1.91 (约16.7%↓))；Road mIoU↑ 63.95 vs 61.26 (PerLDiff) (+2.69)；NDS↑ 25.49 vs 24.05 (PerLDiff) (+1.44)。
> - NuScenes test set (BEV segmentation boosting) 上，Road mIoU↑ 67.49 (train+Syn.val Ours) vs 67.53 (train+Real val) ; 65.74 (train+Syn.val PerLDiff) (-0.04 vs Real val上限；+1.75 vs PerLDiff)。
> - NuScenes (video generation) 上，FVD↓ 128 (SD-2.1) / 110 (SD-3.5) vs MagicDrive 221, Panacea 139, Drive-WM 122 (超越多数基线，SD-3.5版本取得最优FVD)。

## 概述

驾驶场景生成的核心挑战在于：如何在多视角、多条件约束下，同时实现高保真图像质量与精确的几何可控性。现有方法普遍存在两个瓶颈。其一，**几何条件间的隐式依赖**——高精地图（HD map）与3D边界框（3D box）在训练中被联合学习，导致独立修改某一条件（如改变道路布局）时，生成结果无法与更新后的条件对齐。Figure 1 直观展示了这一现象：主流方法 MagicDrive 在修改地图后生成失败，而本文方法则能成功适应。其二，**文本条件的粗糙性**——现有方法使用视角无关的简短描述，缺乏对时间、天气、道路类型、周围环境、物体及空间关系等多维度信息的细粒度刻画，导致背景建模薄弱，尤其在夜间等复杂场景下易产生幻觉。

针对上述问题，**DrivePTS** 提出了三个核心机制，形成一套渐进式学习框架：

1. **渐进式几何学习策略**：将场景生成分解为“先道路、后物体”的两阶段过程。阶段一通过交替训练分别学习道路布局与物体放置，避免灾难性遗忘；阶段二联合适配，并引入基于 InfoNCE 的互信息约束，显式降低地图特征与边界框特征之间的统计依赖。
2. **VLM 驱动的多视角层次化描述**：利用视觉语言模型（VLM）离线生成覆盖六个维度的多视角场景描述，替代原始数据集中视角无关的简短标注，为生成过程提供更丰富的语义指导。
3. **频率引导的结构损失**：通过傅里叶高通滤波提取图像高频成分，在道路与物体区域施加额外的结构监督，强化边缘与轮廓细节，缓解标准均匀加权去噪损失对前景结构关注不足的问题。

实验表明，DrivePTS 在 nuScenes 验证集上取得了 **FID 11.45**，较次优方法 PerLDiff 下降约 16.7%；**Road mIoU 达到 63.95**，超出第二名 2.69 点；Vehicle mIoU 与 NDS 同样达到最优。消融实验进一步证实，多视角层次描述、频率引导结构损失与互信息约束三者协同作用，缺一不可。此外，合成数据在 BEV 分割任务上的数据增强实验显示，使用 DrivePTS 生成的合成数据训练，其 Road mIoU 可逼近使用真实验证集的上限性能。

## 背景与动机

自动驾驶感知模型的训练与评估高度依赖大规模、多样化的驾驶场景数据。然而，真实世界数据的采集与标注成本高昂，且面临长尾场景覆盖不足、隐私与安全等挑战。为此，基于扩散模型的驾驶场景生成方法受到广泛关注，其目标是在给定几何条件（如高精地图、3D边界框）和文本描述的控制下，合成逼真且可控的多视图驾驶图像。

现有方法虽取得显著进展，但仍存在三个核心瓶颈：

**几何条件间的隐式依赖导致可控性受限。** 主流方法（如 **MagicDrive**、**BEVControl**）通常将高精地图与3D边界框作为并行条件同时注入生成网络。然而，道路布局与交通参与者的位置、朝向在物理世界中存在强关联，这种统计依赖性被模型隐式地编码进条件特征中。当用户仅修改地图布局而不改变边界框时，模型无法解耦这种依赖关系，导致生成结果与修改后的地图不一致。如 Figure 1 所示，MagicDrive 在地图布局修改后完全无法适应变化，而本文方法可成功生成与更新地图对齐的场景。

**视角无关的简短文本描述导致背景建模薄弱。** 现有数据集提供的文本标注（如 nuScenes 的 captions）通常为一句全局性的简短描述，缺乏对多视角细节、空间关系、光照与天气等要素的精细刻画。这导致生成模型对背景区域的语义理解不足，容易出现细节丢失或幻觉，尤其在夜间场景中会错误地生成光照区域。

**均匀权重的去噪损失忽视前景结构细节。** 标准扩散模型采用空间均匀加权的 $L_2$ 去噪损失，对图像所有区域同等对待。然而，驾驶场景中道路边缘、车道线和物体轮廓等高频结构信息对下游感知任务至关重要，均匀损失无法有效强化这些关键区域的学习，导致生成图像出现结构模糊与视觉失真。

针对上述问题，本文提出 **DrivePTS**，通过三个核心设计实现突破：(1) 渐进式学习策略解耦道路与物体的几何条件学习；(2) 利用视觉语言模型生成多视角层次化语义描述以增强文本条件；(3) 引入频率引导的结构损失以强化前景高频细节。

## 核心创新

DrivePTS 的核心创新围绕驾驶场景生成中**几何条件耦合**与**视觉结构退化**两大瓶颈展开，形成“渐进解耦—语义增强—结构强化”三位一体的技术路径。

### 1. 渐进式几何条件解耦

现有方法（如 **MagicDrive**、**PerLDiff**）将高精地图（HD map）与 3D 边界框（3D box）同时注入扩散模型，导致两类几何条件间形成隐式依赖关系——当用户独立修改地图布局时，已学习的条件耦合会使模型无法适应变化，生成与更新地图不一致的场景（Figure 1）。

DrivePTS 提出**两阶段渐进式学习策略**，从根本上切断这一依赖：

- **Stage 1（交替训练）**：将场景生成分解为“先道路、后物体”的独立学习过程。道路生成损失仅在道路区域（$M_{\text{map}}$）和背景区域（$M_{\text{bg}}$）施加扩散损失与频率引导结构损失；物体生成损失则仅在边界框区域（$M_{\text{box}}$）施加监督。通过交替优化这两个损失，模型分别建立“地图→道路”和“边界框→物体”的独立映射，避免联合训练中的灾难性遗忘。交替步长设为 1000 时，FID 与几何可控性达到最佳平衡（Figure 3）。

- **Stage 2（联合适配 + 互信息约束）**：在独立学习基础上进行联合微调，同时引入基于 InfoNCE 的互信息约束 $\mathcal{L}_{\text{MI}}$，显式降低地图特征 $f_m$ 与对应边界框特征 $f_b^+$ 之间的相似性：

$$\mathcal{L}_{\mathrm{MI}} = \mathbb{E}_{(f_m, f_b^+)} \left[ \log \frac{\exp(\sin(f_m, f_b^+))}{\sum_{j=1}^{N} \exp(\sin(f_m, f_{b,j}))} \right]$$

该约束迫使模型学习条件独立的特征表示，而非记忆条件间的统计相关性。消融实验表明，加入 MIC 后 FID 从 11.68 进一步降至 11.45，Road mIoU 从 63.60 提升至 63.95（Table 3），验证了解耦对联合适配的关键作用。

### 2. VLM 驱动的多视角层次化场景描述

现有方法的文本条件采用**简洁且视角不变**的场景描述，缺乏对场景语义的细粒度刻画，导致背景建模薄弱、细节缺失。DrivePTS 利用视觉语言模型（VLM）离线生成覆盖六个维度的**多视角层次化描述**：时间、天气、道路类型、周围环境、物体、空间关系（Figure 7）。

这一设计的核心价值在于**视角感知的语义丰富性**——不同相机视角获得差异化的文本描述，使扩散模型能够建立视角-语义的对齐关系。定性结果表明，层次化描述显著改善了场景重建的细节完整性，尤其在夜间场景中，原始简短标注容易产生虚构的照明区域，而多视角层次描述能忠实还原真实的夜间氛围（Figure 8、Figure 9）。消融实验进一步证实，仅引入 MHD 即可将 FID 从 15.10 降至 12.03，Road mIoU 从 59.77 提升至 61.22（Table 3）。

### 3. 频率引导的结构损失

标准扩散损失对所有空间位置施加均匀权重，忽视了对驾驶场景生成至关重要的**前景结构细节**（道路边缘、车道线、车辆轮廓），导致生成图像出现模糊和几何失真。

DrivePTS 提出**频率引导的结构损失** $\mathcal{L}_{\text{freq}}$，通过傅里叶高通滤波提取预测图像与目标图像的高频成分并计算 L2 差异：

$$\mathcal{L}_{\mathrm{freq}} = \lVert \mathcal{H}(x_{\mathrm{pred}}) - \mathcal{H}(x_{\mathrm{target}}) \rVert_2^2$$

其中高通滤波器 $\mathcal{H}(x) = \mathcal{F}^{-1}(M(\omega) \cdot \mathcal{F}(x))$，掩模 $M(\omega)$ 保留高于阈值 $\tau=0.5$ 的频率成分。该损失仅在道路区域和物体区域施加，避免背景噪声干扰。

单独施加 FGSL 使 Road mIoU 从 59.77 升至 62.92，车辆结构清晰度和道路边界完整性也获得显著改善（Table 3、Figure 6）。与 MHD 组合后，FID 进一步降至 11.68，Road mIoU 提升至 63.60，验证了两组件在语义增强与结构强化上的协同增益。

### 创新总结

| 创新维度 | 基线做法 | DrivePTS 方案 | 关键机制 |
|---------|---------|--------------|---------|
| 几何条件学习 | 同时学习，条件间存在隐式依赖 | 渐进式“先道路后物体”，交替训练 + 互信息约束 | 条件解耦，独立编辑可控 |
| 文本条件 | 视角无关的简短标注 | VLM 生成的六维度多视角层次化描述 | 视角感知的语义增强 |
| 结构监督 | 均匀空间加权的去噪损失 | 频率引导的高通滤波结构损失 | 前景高频细节强化 |

三者协同使 DrivePTS 在 nuScenes 验证集上取得 FID 11.45（较 PerLDiff 降低约 16.7%）、Road mIoU 63.95（超出次优方法 2.69 点）的最优性能，并在修改地图布局时展现出基线方法无法实现的独立可控性。

## 整体框架

DrivePTS 的整体生成流程围绕“先道路、后物体”的核心洞察构建，形成一条从几何条件解耦到多模态条件融合的渐进式生成管线。图 2 给出了框架的全貌，其输入输出流与模块关系可概括为三个层次：条件编码、渐进式训练与结构监督。

**条件注入网络**。几何条件通过双路 T2I-Adapter 并行注入 Stable Diffusion 的 UNet 编码器。高精地图（HD map）输入 **Map T2I-Adapter**，3D 边界框输入 **Box T2I-Adapter**，二者分别提取多尺度特征 $F_c = T(C)$，并逐级与 UNet 编码器特征相加：$\hat{F}_{enc}^i = F_{enc}^i + F_c^i, i \in \{1,2,3,4\}$。文本条件则来自 **VLM Captioner** 离线生成的多视角层次化描述，覆盖时间、天气、道路类型、周围环境、物体及空间关系六个维度，经 CLIP 文本编码后通过交叉注意力注入去噪过程。多视图一致性由 **Cross-View Module** 在各视角特征间进行交互来维护。

**渐进式训练流程**。训练分为两个阶段。**阶段一**将场景生成分解为道路生成与物体生成两个交替进行的子任务：道路训练时仅在地图区域与背景区域施加扩散损失，并在道路区域附加频率损失；物体训练时仅在边界框区域施加扩散与频率损失。这种交替训练策略缓解了物体学习对道路生成能力的灾难性遗忘。**阶段二**进行联合适配，同时使用全部几何条件，并引入基于 InfoNCE 的互信息约束来显式降低地图特征与边界框特征间的统计依赖性，消除条件耦合带来的生成失败。

**结构监督**。**Frequency-Guided Structure Loss** 通过傅里叶高通滤波 $\mathcal{H}(x) = \mathcal{F}^{-1}(M(\omega) \cdot \mathcal{F}(x))$ 提取预测图像与目标图像的高频成分，计算二者间的 $L_2$ 差异，从而强制模型关注道路边缘与物体轮廓等结构细节。该损失在阶段一按区域施加，在阶段二同时覆盖道路与物体区域。

整个管线最终以端到端方式输出六视角驾驶场景图像，其生成过程可接受独立编辑的地图布局或边界框条件，实现对道路结构与物体配置的解耦控制。

### 补充图表

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/002_Figure_2.jpg]]
*Figure 2: The overall architecture of our proposed DrivePTS. The left part illustrates our adopted generative network structure, while the center depicts the training process corresponding to the proposed progressive learning strategy. The right part highlights the implementation of frequency-guided structure loss*

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/020_Figure_10.jpg]]
*Figure 10: Examples of targeted road removal in driving scene generation using our DrivePTS framework. Each group shows: (1) original geometric conditions, (2) original scene generation, (3) modified geometric conditions after road removal, and (4) updated scene generation. Green boxes indicate areas corresponding to the geometric modifications*

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/021_Figure_11.jpg]]
*Figure 11: Examples of targeted road addition in driving scene generation using our DrivePTS framework. The visualization follows the same four-row format as above, where the third row shows geometric conditions with added roads*

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/022_Figure_12.jpg]]
*Figure 12: Additional examples of targeted road addition using our DrivePTS framework. The visualization format follows the same structure as above*

## 核心模块与公式推导

### 3.1 基础生成架构

DrivePTS 以 Stable Diffusion 为骨干，在潜在空间执行去噪扩散过程。基础去噪损失为：

$$L_{\mathrm{diff}} = \mathbb{E}_{Z_t, C, \epsilon, t} \left[ \| \epsilon - \epsilon_{\theta}(Z_t, C) \|_2^2 \right] \quad \text{(1)}$$

其中 $Z_t$ 为噪声潜在表示，$C$ 为条件信号，$\epsilon_{\theta}$ 为 UNet 预测的噪声。

几何条件注入采用双路 T2I-Adapter 机制。高精地图（HD Map）和 3D 边界框分别通过 Map T2I-Adapter 和 Box T2I-Adapter 提取多尺度特征，逐级注入 UNet 编码器：

$$F_c = T(C), \quad \hat{F}_{enc}^i = F_{enc}^i + F_c^i, \quad i \in \{1,2,3,4\} \quad \text{(2)}$$

其中 $T(C)$ 为 T2I-Adapter 从几何条件 $C$ 提取的特征，$F_{enc}^i$ 为 UNet 编码器第 $i$ 层原始特征，$\hat{F}_{enc}^i$ 为注入后的特征。此外，跨视角模块（Cross-View Module）在阶段二引入，用于多视角特征交互以保持六视图一致性。

### 3.2 渐进式学习策略与互信息约束

核心问题在于 HD 地图与 3D 边界框之间存在隐式统计依赖——道路结构决定了车辆的可能位置分布。当直接联合训练时，模型学习到的是耦合条件，导致独立修改某一条件时生成失败。

**阶段一：交替解耦训练。** 将场景生成分解为“先道路、后物体”两个子任务，采用交替训练策略，每 $K$ 步切换一次（消融实验表明 $K=1000$ 时道路与物体质量最佳）。道路训练时仅使用 Map T2I-Adapter，物体训练时仅使用 Box T2I-Adapter，从源头阻断条件间的联合学习。

**阶段二：联合适配与互信息约束。** 引入双路 Adapter 进行联合微调，同时施加基于 InfoNCE 的互信息约束，显式降低地图特征 $f_m$ 与对应边界框特征 $f_b^+$ 之间的相似性：

$$L_{\mathrm{MI}} = \mathbb{E}_{(f_m, f_b^+)} \left[ \log \frac{\exp(\sin(f_m, f_b^+))}{\sum_{j=1}^{N} \exp(\sin(f_m, f_{b,j}))} \right] \quad \text{(3)}$$

该约束将正样本对 $(f_m, f_b^+)$ 与负样本对 $(f_m, f_{b,j}), j \neq +$ 进行对比，最小化正样本对的相似度，迫使两个几何编码器学习独立表征，从而消除条件冗余依赖。

### 3.3 多视角层次化文本描述（MHD）

现有数据集（如 nuScenes）提供的文本标注为简洁且视角不变的单一描述，缺乏对背景环境、空间关系、时间天气等细粒度信息的刻画，导致生成场景的背景建模薄弱。

DrivePTS 引入 VLM Captioner 模块，离线调用视觉语言模型（VLM）为每帧六视图图像生成覆盖六个维度的层次化描述：时间、天气、道路类型、周围环境、物体、空间关系。这些描述以多视角形式组织，为扩散模型提供细粒度语义指导，增强场景真实性与多样性。

### 3.4 频率引导的结构损失（FGSL）

标准去噪损失对所有空间位置施加均匀权重，忽视了道路边缘、车辆轮廓等高频结构细节，导致生成结果出现模糊和几何失真。

FGSL 通过傅里叶高通滤波提取图像高频成分，并仅在结构区域施加额外监督。高通滤波定义为：

$$\mathcal{H}(x) = \mathcal{F}^{-1}(M(\omega) \cdot \mathcal{F}(x)) \quad \text{(4)}$$

其中 $\mathcal{F}$ 为傅里叶变换，高通掩模 $M(\omega)$ 保留频率高于阈值 $\tau$ 的成分：

$$M(\omega) = \begin{cases} 0, & \|\omega\| \le \tau \\ 1, & \|\omega\| > \tau \end{cases}$$

$\tau$ 经验设置为 0.5。频率引导的结构损失计算预测图像与目标图像高频成分的 L2 距离：

$$L_{\mathrm{freq}} = \lVert \mathcal{H}(x_{\mathrm{pred}}) - \mathcal{H}(x_{\mathrm{target}}) \rVert_2^2 \quad \text{(5)}$$

### 3.5 分阶段训练目标

**阶段一道路训练损失**：仅在道路区域 $M_{\mathrm{map}}$ 和背景区域 $M_{\mathrm{bg}}$ 施加扩散损失，在道路区域附加频率损失以强化路面边界：

$$\mathcal{L}_{\mathrm{road}} = \mathcal{L}_{\mathrm{diff}} \odot (M_{\mathrm{map}} + M_{\mathrm{bg}}) + \lambda_{\mathrm{freq}} \cdot \mathcal{L}_{\mathrm{freq}} \odot M_{\mathrm{map}} \quad \text{(6)}$$

**阶段一物体训练损失**：仅在边界框区域 $M_{\mathrm{box}}$ 施加扩散和频率损失：

$$L_{\mathrm{object}} = L_{\mathrm{diff}} \odot M_{\mathrm{box}} + \lambda_{\mathrm{freq}} \cdot L_{\mathrm{freq}} \odot M_{\mathrm{box}} \quad \text{(7)}$$

**阶段二联合训练损失**：在道路和物体区域均施加频率损失，并加入互信息约束：

$$\mathcal{L}_{\mathrm{stage2}} = \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{freq}} \cdot \mathcal{L}_{\mathrm{freq}} \odot (M_{\mathrm{map}} + M_{\mathrm{box}}) + \lambda_{\mathrm{MI}} \cdot \mathcal{L}_{\mathrm{MI}} \quad \text{(8)}$$

消融实验确定最优超参数为 $\lambda_{\mathrm{freq}} = 0.5$、$\lambda_{\mathrm{MI}} = 0.05$。过高的 $\lambda_{\mathrm{MI}}$ 会破坏地图与边界框之间必要的空间关系，导致性能下降。

### 补充图表

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative comparison of scene generation with and without frequency-guided structure loss. Columns 1-2 show vehicle structure improvements, while columns 3-4 show road boundary enhancements. Red boxes highlight structural distortions without the proposed loss, whereas green boxes indicate successful mitigation with the loss*

## 实验与分析

### 核心定量结果

DrivePTS在nuScenes验证集上取得了最优的图像生成保真度与几何可控性。如Table 1所示，其FID降至11.45，较此前最强的PerLDiff（13.36）下降约16.7%，表明生成图像在分布层面更接近真实场景。在几何可控性方面，Road mIoU达到63.95，比PerLDiff高出2.69点；Vehicle mIoU为27.82，领先次优方法0.69点。这一差距在道路结构上尤为显著，直接印证了渐进式学习策略“先道路、后物体”的设计逻辑——模型对道路布局的建模精度得到了系统性增强。

在BEV分割模型的数据增强实验中（Table 2），使用DrivePTS生成的合成验证集（Syn.val Ours）训练CVT模型，Road mIoU达到67.49，仅比使用真实验证集的上限（67.53）低0.04点，几乎完全逼近真实数据的效果。相比之下，PerLDiff生成的合成数据仅达到65.74，与上限差距为1.79点。这一结果说明DrivePTS生成的场景不仅视觉逼真，其底层几何结构也足够精确，可直接用于下游感知任务的训练数据扩充。

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/004_Table_2.jpg]]
*Table 2: Performance comparison for the boosting performance of BEV segmentation models using synthesized dataset on the NuScenes test set using CVT. The “train + Real val” configuration serves as a benchmark, representing the ideal upper performance limit achievable. The numbers in parentheses indicate the performance disparity relative to the “train + Real val” configuration*

视频生成方面（Table 5），基于SD-2.1的DrivePTS取得FVD 128，优于MagicDrive（221）和Panacea（139）；基于SD-3.5的版本进一步降至110，超越Drive-WM（122），取得最优时间一致性。这表明渐进式学习策略和结构损失在时序生成中同样有效。

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/011_Table_5.jpg]]
*Table 5: Comparison of temporal consistency for different video generation methods on the NuScenes dataset. Lower FVD scores indicate better temporal coherence*

### 消融实验：各组件的独立与协同贡献

Table 3系统拆解了多视角层次描述（MHD）、频率引导结构损失（FGSL）与互信息约束（MIC）三个核心组件的作用。

**MHD的独立贡献**：仅添加MHD（不使用FGSL和MIC）时，FID从15.10降至12.03，Road mIoU从59.77提升至61.22。这说明VLM生成的细粒度多视角场景描述显著增强了图像的逼真度和场景可控性——原始数据集中的简短、视角无关标注无法为背景建模提供足够约束，而层次化描述覆盖了时间、天气、道路类型、周围环境等多个维度，有效弥补了这一缺陷。

**FGSL的独立贡献**：单独施加FGSL使Road mIoU升至62.92，提升幅度超过MHD（+3.15 vs +1.45），直接验证了高频结构监督对道路边缘和物体轮廓的强化作用。标准扩散损失在空间上均匀加权，对前景结构细节缺乏针对性关注；FGSL通过傅里叶高通滤波将损失聚焦于高频成分，迫使模型精确重建道路边界和物体轮廓。

**协同增益**：MHD与FGSL组合将FID进一步降至11.68，Road mIoU提升至63.60，表明文本增强与结构监督存在互补——MHD提供语义层面的场景约束，FGSL在信号层面强化几何细节。在此基础上加入MIC后达到全局最优（FID 11.45，Road mIoU 63.95，Vehicle mIoU 27.82），证明显式解耦地图与边界框条件间的统计依赖对联合适配阶段至关重要。若缺少MIC，两个几何条件在联合训练时会产生冗余交互，破坏各自已学到的生成能力。

### 关键超参数分析

Table 4展示了损失系数对性能的影响。频率损失权重λ_freq在0.5时取得Road mIoU与Vehicle mIoU的最佳平衡——过低的权重无法充分约束结构细节，过高则可能压制扩散损失对整体分布的建模能力。互信息约束系数λ_MI设为0.05时最优，进一步增大反而导致性能下降，说明过度解耦会破坏地图与物体间必要的空间关系（如车辆必须位于道路上），需要在独立性与空间一致性之间保持适度张力。

Stage 1交替训练步长的消融（Figure 3）显示，步长设为1000时能较好兼顾道路与物体的生成质量。过短的步长导致模型在两类生成任务间切换过于频繁，无法充分学习各自的特征；过长的步长则可能引发灾难性遗忘，后学的任务覆盖先学的能力。

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/005_Figure_3.jpg]]
*Figure 3: Impact of different iterative steps on the FID and geometry controllability of generated images*

### 定性分析：条件解耦与可控性

Figure 1展示了DrivePTS在条件解耦方面的核心优势。当修改高精地图布局时，MagicDrive无法适应变化——其生成结果仍与原始地图对齐，暴露了地图与边界框条件间的隐式依赖：模型在训练中将两者耦合学习，一旦单独修改地图，边界框条件产生的梯度仍将生成拉向旧布局。DrivePTS通过渐进式学习与互信息约束消除了这种耦合，成功生成与新地图对齐的场景。

Figure 4进一步展示了通过编辑HD地图实现道路布局可控修改的能力——新增道路结构后，生成图像准确反映了这些变化，道路走向、交叉口形态与地图标注一致。Figure 10-12展示了目标道路移除与添加的更多案例，验证了框架在几何条件部分编辑下的鲁棒性。

### 文本增强与结构损失的定性证据

Figure 7对比了原始数据集文本与VLM生成的多视角层次描述。原始文本通常为一句简短且视角不变的描述（如“a car driving on a road”），缺乏对天气、时间、周围环境等背景要素的刻画。VLM生成的描述覆盖了时间、天气、道路类型、周围环境、物体、空间关系六个维度，且针对不同视角提供差异化信息。

Figure 8和Figure 9展示了文本质量对场景重建的影响。使用原始简短标注时，重建图像常出现细节缺失（如建筑物纹理模糊、背景物体丢失）；在夜间场景中，原始标注甚至导致模型幻觉出不存在的照明区域。层次化描述显著改善了这些问题，重建结果更忠实地还原了真实场景的细节和氛围。

Figure 6直观展示了频率引导结构损失的作用。未使用FGSL时，车辆轮廓和道路边界存在明显模糊与失真（红色框标注）；加入FGSL后，这些结构细节得到显著改善（绿色框标注），车辆边缘更清晰，道路标线更锐利。

### 失败模式与局限性

尽管DrivePTS在道路和车辆生成上取得了显著提升，论文明确指出**车道线和交通标志的细节生成仍不够理想**。这反映了当前方法的一个内在局限：高精地图和3D边界框提供的是粗粒度的几何约束（道路区域、物体位置），而车道线、交通标志等细粒度结构需要更精确的空间和语义控制信号。频率引导结构损失虽能强化高频细节，但缺乏对这些特定语义类别的针对性监督，导致模型在重建这些局部结构时精度不足。

### 补充图表

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/006_Table_3.jpg]]
*Table 3: Ablation study on the effectiveness of Multi-View Hierarchical Descriptions (MHD), Frequency-Guided Structure Loss (FGSL), and Mutual Information Constraint (MIC) in driving scene generation*

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of various scene generation methods on the modified map layouts. The first column highlights the modified regions of each map. While MagicDrive fails to adapt to map modifications, our DrivePTS successfully generates scenes aligning with the updated map configurations*

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/018_Figure_8.jpg]]
*Figure 8: Qualitative comparison of scene reconstruction quality between original dataset captions and our multi-view hierarchical descriptions. For each example: original image (top), reconstruction from original captions (middle), and our results (bottom). Red regions indicate missing details with original captions, while green regions highlight successful recovery through our fine-grained descriptions*

![[assets/figures/papers/paper_list_l2468_https_arxiv_org_abs_2602_22549/figures/019_Figure_9.jpg]]
*Figure 9: Qualitative comparison of scene reconstruction quality between original dataset captions and our multi-view hierarchical descriptions. Notably, in night scene generation, original captions tend to produce hallucinated illuminated areas due to insufficient contextual information, while our multi-view hierarchical descriptions faithfully reconstruct authentic nighttime atmospheres*

## 方法谱系与知识库定位

### 1. 与现有驾驶场景生成方法的关系

DrivePTS 的基线谱系主要覆盖三类方法：基于 BEV 布局的生成、基于扩散模型的场景生成，以及面向多视图一致性的视频生成。

**基于 BEV 布局的生成方法。** **BEVGen** 与 **BEVControl** 率先探索了从鸟瞰图布局生成多视图驾驶场景的范式，但其生成质量与可控性受限于早期架构。DrivePTS 继承了这一“几何条件驱动生成”的思路，但将条件注入机制升级为双路 T2I-Adapter 架构，分别处理高精地图与 3D 边界框，从而获得更精细的空间控制能力。

**扩散模型驱动的驾驶场景生成。** **MagicDrive** 是该方向的主要基线，其将地图与边界框条件同时输入扩散模型，但两个几何条件之间存在隐式依赖关系——当独立修改某一条件时，生成结果往往无法适应变化。DrivePTS 的核心突破在于通过“先道路、后物体”的渐进式学习策略解耦这两个条件，并引入基于 InfoNCE 的互信息约束显式降低条件特征间的统计依赖性。**PerLDiff** 作为强基线，在 FID 和 Road mIoU 上均表现突出，DrivePTS 在此基础上将 FID 从 13.36 降至 11.45（降幅约 16.7%），Road mIoU 从 61.26 提升至 63.95。**Panacea** 则代表了面向视频生成的扩散方法，DrivePTS 在视频生成实验中以 SD-3.5 版本取得 FVD 110，优于 Panacea 的 139 和 MagicDrive 的 221。

**文本条件增强。** 现有方法普遍使用数据集中简短且视角不变的场景描述，导致背景建模弱、细节丢失。DrivePTS 借助 VLM 离线生成覆盖时间、天气、道路类型、周围环境、物体、空间关系六个维度的多视角层次化描述，将文本条件从“粗略标签”升级为“细粒度场景先验”。消融实验表明，仅引入多视角层次描述（MHD）即可将 FID 从 15.10 降至 12.03，Road mIoU 从 59.77 提升至 61.22。

### 2. 核心机制的知识贡献

DrivePTS 的知识增量集中在三个可迁移的设计选择上：

| 设计维度 | 现有做法 | DrivePTS 方案 | 可迁移性 |
|---------|---------|--------------|---------|
| 几何条件学习 | 同时注入所有条件，存在隐式耦合 | 渐进式交替训练 + 互信息约束解耦 | 适用于任何多条件扩散生成任务 |
| 文本条件粒度 | 单一简短标注，视角无关 | VLM 生成多视角层次化语义描述 | 可推广至其他需要细粒度文本引导的生成任务 |
| 结构监督 | 均匀空间加权的去噪损失 | 频率引导的结构损失，通过高通滤波强化前景高频细节 | 适用于需要保持边缘/轮廓精度的图像生成任务 |

**频率引导结构损失的设计原理值得关注。** 该损失通过傅里叶高通滤波器提取预测图像与目标图像的高频成分，计算二者之间的 L2 差异，迫使模型关注道路边缘和物体轮廓等结构细节。消融实验中，单独施加 FGSL 使 Road mIoU 升至 62.92，定性结果（Figure 6）显示其有效缓解了车辆结构失真和道路边界模糊问题。损失系数 $\lambda_{\mathrm{freq}} = 0.5$ 时取得道路与车辆生成质量的最佳平衡，过高会抑制整体图像质量。

**互信息约束的实现方式具有参考价值。** 该约束作用于 Stage 2 联合训练阶段，通过最小化地图特征 $f_m$ 与对应边界框特征 $f_b^+$ 的余弦相似度，降低两个几何条件间的冗余依赖。系数 $\lambda_{\mathrm{MI}} = 0.05$ 为最优值，过高会破坏必要的空间关系。这一设计可推广至其他需要多模态条件解耦的场景。

### 3. 适用边界与限制

**当前局限。** 论文明确指出，生成的车道线和交通标志细节仍然不够理想，需要更精确的空间和语义控制。这一局限的根源在于：高频结构损失虽然强化了道路边界，但对细窄、稀疏的线状结构（如车道线、交通标志）的监督信号仍不足，因为这些结构在高通滤波后的能量占比有限。

**适用场景边界。** DrivePTS 的有效性在 nuScenes 数据集上得到验证，该数据集以城市道路场景为主。论文未在极端天气、高动态交通或非结构化道路场景下进行测试，这些场景下的可控性与生成质量需要进一步验证。此外，渐进式学习策略的交替训练步长（经验最优值为 1000 步）可能需要根据数据集规模和场景复杂度重新调整。

**计算开销。** VLM 描述生成是离线完成的，不增加推理开销；但双路 T2I-Adapter 和跨视图交互模块增加了模型参数量，论文未提供与基线的推理效率对比数据，这一点需要手动验证。

### 4. 开放问题与后续方向

1. **细粒度局部结构的精确控制。** 如何通过更细粒度的约束（如车道线级别的分割监督、交通标志的语义嵌入）进一步提升线状结构的生成精度，是直接可延续的方向。

2. **极端场景泛化。** 该方法是否可以拓展到极端天气（暴雨、暴雪）、高动态交通（密集车流、复杂交互）等场景并保持可控性，需要进一步的实验验证。

3. **条件解耦的理论分析。** 互信息约束的有效性已通过消融实验验证，但其对条件特征空间的具体影响机制（如特征维度的独立性、跨条件信息流动的阻断程度）缺乏深入的理论分析，这为后续研究提供了可探索的空间。

4. **与下游任务的闭环优化。** Table 2 展示了合成数据对 BEV 分割模型的增强效果（Road mIoU 67.49，接近真实验证集上限 67.53），但生成质量与下游任务性能之间的定量关系尚未建立，如何针对特定下游任务优化生成策略是一个有应用价值的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/DrivePTS_A_Progressive_Learning_Framework_with_Textual_and_Structural_Enhancement_for_Driving_Scene_Generation.pdf]]
