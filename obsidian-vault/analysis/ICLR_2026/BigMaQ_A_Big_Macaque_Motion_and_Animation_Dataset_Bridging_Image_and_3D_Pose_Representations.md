---
title: "BigMaQ: A Big Macaque Motion and Animation Dataset Bridging Image and 3D Pose Representations"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BigMaQ_A_Big_Macaque_Motion_and_Animation_Dataset_Bridging_Image_and_3D_Pose_Representations.pdf
project_link: https://martinivis.github.io/BigMaQ/
code_link: null
openreview_forum_id: n7viYE7Xbo
aliases:
- BigMaQ
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入基于高质量猕猴模板网格的主题特定纹理化三维虚拟形象，结合多视图无标记运动捕获与时间优化，并首次将3D表面姿态旋转矩阵特征与视觉编码器融合，构成统一的动作识别流。"
primary_logic: "将三维表面模型导出的旋转矩阵形式姿态特征（rotation matrix）与视觉特征融合，可显著提升猕猴动作识别性能；单独姿态流即具备强竞争力，表明高精度3D姿态本身蕴含丰富行为信息。"
claims:
- "仅使用姿态流（pose-only stream）即可达到 mAP 43.5±1.4，超过除DINOv2-base外所有仅视觉基线模型。"
- "在 ResNet50、ViT-base-cls 等六个视觉骨干上，视觉+姿态（Vis+Pose）的 mAP 均显著优于纯视觉（Vis），最高提升近 12 点（ResNet50 34.3→44.0）。"
- "以旋转矩阵 (3D-Rot) 表示的姿态在所有视觉骨干及姿态单独流中均取得最优 mAP，证明该表示对动作识别最有效。"
- "BigMaQ 四段动作序列 (Walk, Food Picking, Branch Shake, Scratch) 上 IoU (序列级均值和单帧均值) = Walk 0.883, Food Picking 0.855, Branch Shake 0.831, Scratch..."
---

# BigMaQ: A Big Macaque Motion and Animation Dataset Bridging Image and 3D Pose Representations

> [!tip] 核心洞察
> 将三维表面模型导出的旋转矩阵形式姿态特征（rotation matrix）与视觉特征融合，可显著提升猕猴动作识别性能；单独姿态流即具备强竞争力，表明高精度3D姿态本身蕴含丰富行为信息。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BigMaQ：一个桥接图像与三维姿态表征的大型猕猴运动与动画数据集 |
| 英文题名 | BigMaQ: A Big Macaque Motion and Animation Dataset Bridging Image and 3D Pose Representations |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=n7viYE7Xbo) · [Project](https://martinivis.github.io/BigMaQ/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | BigMaQ — 面向猕猴的个性化三维表面跟踪与姿态‑动作识别融合框架 |
| Dataset | BigMaQ 四段动作序列 (Walk, Food Picking, Branch Shake, Scratch), 同上四段动作, BigMaQ500 动作识别 (多视觉骨干) |

> [!tip] 效果简介
> - BigMaQ 四段动作序列 (Walk, Food Picking, Branch Shake, Scratch) 上，IoU (序列级均值和单帧均值) 为 Walk 0.883, Food Picking 0.855, Branch Shake 0.831, Scratch 0.843; 单帧总体 0.844 (Table 3)，对比 MAMMAL: 0.771, 0.756, 0.757, 0.722; 单帧总体 0.714; AniMer+: 单帧 0.591，变化 相对 MAMMAL 提升约 10-13 个 IoU 百分点。
> - 同上四段动作 上，MPJPE (mm, 越低越好) 为 Walk 20.402, Food Picking 16.489, Branch Shake 13.633, Scratch 20.481；单帧总体 26.907 (Table 3 上下文)，对比 MAMMAL: 23.493, 25.521, 22.163, 28.843；单帧总体 31.661，变化 提升约 4-11 mm。
> - 同上四段动作 上，MPJTD (mm/frame, 越低越好) 为 Walk 6.875, Food Picking 9.062, Branch Shake 15.515, Scratch 4.422，对比 MAMMAL: 9.961, 13.362, 17.676, 8.498，变化 降低 14% - 48%。

## 概要

### 问题瓶颈

现有非人灵长类行为分析主要依赖稀疏的二维或三维关键点，缺乏准确的三维表面模型。这一局限导致两方面后果：其一，姿态表征的丰富度不足，难以捕捉精细动作的几何细节；其二，尚未有工作将模型化的三维姿态特征与视频视觉特征系统性融合用于动作识别，使得行为理解的精度受限于单一模态的信息瓶颈。

### 核心思路

BigMaQ 通过两条主线破解上述瓶颈。在数据层面，基于高质量猕猴模板网格构建**主题特定的纹理化三维虚拟形象**，结合多视角无标记运动捕获与时间优化，为每只个体生成可任意视角渲染的彩色表面模型。在识别层面，首次将三维表面模型导出的**旋转矩阵形式姿态特征**与多种视觉骨干网络的特征进行融合，构成统一的动作识别流。其核心洞察在于：高精度三维姿态本身蕴含丰富的行为信息——仅使用姿态流即可达到强竞争力性能；而将姿态旋转矩阵特征与视觉特征融合，可显著超越纯视觉基线。

### 方法定位

BigMaQ 在方法谱系中处于**多视角表面跟踪**与**姿态‑视觉融合动作识别**的交叉点。其表面跟踪部分在 **MAMMAL**（An et al., 2023）和 **AniMer+**（Lyu et al., 2025b）等基于模板网格的动物表面建模方法基础上，引入了四项关键改进：时间一致性损失约束帧间运动平滑性、裁剪视图与批量相机处理降低计算开销、顶点颜色学习实现纹理化外观建模、以及骨骼长度与顶点偏移联合优化实现个性化形状适配。动作识别部分则将姿态特征与 **ResNet50**（He et al., 2016）、**ViT**（Dosovitskiy et al., 2021）、**DINOv2**（Oquab et al., 2023）、**TimeSformer**（Bertasius et al., 2021）、**VideoPrism**（Zhao et al., 2024）等多种视觉骨干进行系统对比融合。

### 主要结果

在表面重建质量上，BigMaQ 在四段典型动作序列（行走、取食、摇枝、抓挠）上的 IoU 达到 0.831–0.883，相较 MAMMAL 提升约 10–13 个百分点；MPJPE 降至 13.6–20.5 mm，提升约 4–11 mm。在动作识别任务上，仅使用姿态流即可达到 mAP 43.5±1.4，超过除 DINOv2-base 外的所有纯视觉基线；在六个视觉骨干上，视觉+姿态的 mAP 均显著优于纯视觉，最高提升近 12 点（ResNet50 从 34.3 升至 44.0）。消融实验进一步确认，以旋转矩阵表示的三维姿态在所有表示形式中取得最优识别性能，比三维关键点高约 10 点 mAP。



### 非人灵长类行为分析的瓶颈

理解非人灵长类动物的行为是神经科学、进化生物学和社会行为计算的核心任务。然而，当前的行为分析工具在表征精度上存在根本性瓶颈：现有猕猴行为数据集仅提供稀疏的二维或三维关键点坐标，缺乏准确的三维表面模型。这种表征贫乏直接限制了精细动作识别（如手指抓握、面部交互）的能力，也使得姿态特征的丰富度不足以支撑鲁棒的行为分类。

更关键的是，现有工作从未将模型化的三维姿态特征与视频视觉特征进行系统性融合用于动作识别。视觉模型擅长捕捉场景上下文和外观线索



## 核心方法与创新机理

BigMaQ 的核心创新在于将猕猴行为分析从稀疏关键点层级推进到**个性化三维表面模型层级**，并首次将表面模型导出的姿态特征与视觉编码器深度融合，构成统一的动作识别流。其关键创新点可归结为以下三个维度。

### 1. 从稀疏关键点到个性化纹理化三维形象

现有猕猴姿态与行为数据集（如 OpenMonkeyStudio、MacaquePose）仅提供 2D 或 3D 关键点，缺乏准确的三维表面信息，这限制了精细动作的几何表达和渲染逼真度。BigMaQ 引入了一个**高质量猕猴模板网格**（10,632 顶点，115 关节骨架），并通过以下机制实现主题特定的个性化适配：

- **骨骼长度与顶点偏移联合学习**：不同于固定模板或仅允许骨骼长度缩放的基线方法（如 **MAMMAL** (An et al., 2023)），BigMaQ 同时优化骨骼长度参数 $\alpha$ 和顶点偏移 $\xi$，并施加平滑正则 $L_{sm}$，使模板网格变形为个体特定的形状。
- **顶点级纹理着色**：为每个个体学习顶点颜色向量 $\mathbf{C}$，通过最小化掩码光度损失 $\mathcal{L}_{\mathrm{phot}} = \sum_{\mathbf{p}\in\Omega} \mathbf{S}^{(c)}(\mathbf{p}) \| \hat{\mathbf{I}}^{(c)}(\mathbf{p}) - \mathbf{I}^{(c)}(\mathbf{p}) \|_2$ 估计外观，并利用 scaled sigmoid 将颜色值限制在 $[0, 255]$。这使重建结果从无纹理的几何表面升级为可任意视角渲染的**彩色虚拟形象**。

### 2. 面向大规模数据的时间优化与计算效率改进

将表面跟踪从单帧扩展到大规模连续视频面临计算瓶颈。BigMaQ 在 **MAMMAL** 的逐帧优化框架上进行了三项关键改进：

- **时间一致性损失**：引入角速度损失 $L_{\mathrm{ang}}$ 和全局平移平滑损失，构成综合时间正则项：
  $$L_T = L_{\mathrm{ang}}(\pmb\theta_{:T}) + L_{\mathrm{ang}}(\mathbf{r}_{:T}) + \frac{1}{T-1} \sum_{n=1}^{T-1} \big\| \mathbf{t}^{(n+1)} - \mathbf{t}^{(n)} \big\|_2^2$$
  该损失在批次内联合优化连续帧，强制关节旋转和平移的时序平滑性。消融实验表明，移除时间损失（$\lambda_T=0$）导致运动平滑性显著下降（MPJTD 从 9.076 升至 10.620 mm/frame）。

- **裁剪视图与批量相机处理**：将可微分渲染限制在裁剪视图（cropped views）上，并限制最大边长为 100px，同时采用批量顺序处理相机（batched camera processing），大幅降低显存与计算量。

- **标签置信度加权**：在网格优化中，使用 HRNet-W48 的关键点置信度和 YOLOv8 的检测置信度对各损失项进行加权，使高置信度标注对优化的贡献更大。消融实验证实，移除置信度加权会导致所有指标轻微退化（MPJPE 从 16.479 升至 18.676 mm，IoU 从 0.855 降至 0.847）。

### 3. 旋转矩阵姿态表示与视觉-姿态融合的动作识别

这是 BigMaQ 最具区分度的创新：首次将三维表面模型导出的**旋转矩阵形式姿态特征**与视觉编码器融合用于猕猴动作识别。

- **姿态表示设计**：从优化后的网格参数 $\Theta$ 中提取三种姿态表示——3D 关键点（KP-3D）、网格顶点（M）和旋转矩阵（3D-Rot）。消融实验（Table 5）表明，旋转矩阵在所有视觉骨干及姿态单独流中均取得最优 mAP，比 3D 关键点高约 10 点（pose-only: 43.5 vs 33.4），证明旋转矩阵蕴含最丰富的动作判别信息。

- **两阶段 Transformer 融合**：视觉特征（来自 ResNet50、ViT、DINOv2、VideoPrism 等骨干）与姿态特征拼接后，送入两层 8 头 Transformer 进行融合，输出多标签动作预测。

- **姿态单独流的强竞争力**：仅使用姿态流（pose-only stream）即可达到 mAP 43.5±1.4，超过除 DINOv2-base 外的所有仅视觉基线模型（如 ResNet50 Vis 仅 34.3）。这揭示了一个核心洞察：**高精度 3D 姿态本身蕴含丰富的行为信息**，而表面模型提供的旋转矩阵表示是释放这一潜力的关键。



![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_n7viYE7Xbo/figures/004_Figure_3.jpg]]
*Figure 3: Pipeline overview for generating BigMaQ and the BigMaQ500 action–pose recognition benchmark. The 3D Labeling Tool provides annotations used to train the detection and keypoint models as well as to optimize subject-specific avatars. These optimized avatars are then combined with video-inferred labels to obtain dynamic pose reconstructions. BigMaQ500 includes all annotations available in BigMaQ, and additionally contains video encodings for more than 500 actions for which complete video-to-3D pose correspondences could be established*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_n7viYE7Xbo/figures/002_Table_1.jpg]]
*Table 1: Comparison of BigMaQ with existing pose estimation and action recognition datasets for NHPs, and animals in general. Species-specific datasets other than those containing non-human primates are not included. In the ”Species” column, G denotes general, P primates, C chimpanzees, and M macaques. The column ”Type” differentiates between 2D keypoint, 3D keypoint, and 3Dshape (3D-S) representations. The origin of this 3D data is further specified by S for synthetic and R for real recordings*

BigMaQ 的整体框架围绕一个核心目标展开：从多视角视频记录中同时获取高质量的**三维表面模型**与**动作标签**，并将二者桥接为一个统一的动作识别基准。其技术路线可分解为两条交织的流水线，如图 3 所示。

**上游感知与标注链。** 原始多视角视频首先通过一个三维标注工具进行人工标注，产生训练数据。基于此，框架训练了两个关键模型：
- **YOLOv8** 检测模型（Jocher et al., 2023），用于识别每只猴子的个体身份并输出包围框；
- **HRNet-W48** 二维关键点估计器（Wang et al., 2021a），在裁剪后的图像上预测每只猴子的 20 个关键点（含手掌、脚掌末端位置）。

同时，**SAM 2**（Ravi et al., 2024）作为零样本基础模型被引入，以检测框为提示生成实例分割掩码，为后续表面跟踪提供前景轮廓约束。

**下游表面重建与动作识别链。** 检测、关键点与掩码输出共同驱动一个**多阶段网格优化**流程，其核心机制如下：
1. **模板初始化**：采用一个包含 10,632 个顶点和 115 个关节的高质量猕猴模板网格，通过线性混合蒙皮（LBS）实现姿态变形。
2. **个性化适配**：联合学习骨骼长度参数 $\alpha$ 和顶点偏移 $\xi$，并施加平滑正则 $L_{sm}$，使模板网格适配每只猴子的个体形态差异。
3. **纹理着色**：为每个个体学习顶点颜色向量 $\mathbf{C}$，通过最小化掩码光度损失 $L_{phot}$ 估计纹理，并利用缩放 sigmoid 函数将颜色值限制在 $[0, 255]$ 范围内。
4. **动态姿态拟合**：采用分阶段优化策略（姿态对齐→形状适配→纹理着色→动态姿态拟合），使用 Adam 优化器结合 Procrustes 对齐，逐帧估计个性化网格参数 $\Theta$。

为处理大规模数据，框架引入了两项关键工程改进：
- **时间一致性损失**：在批次内联合优化连续帧，引入角速度损失 $L_{ang}$ 和全局平移平滑损失，强制运动轨迹的时序平滑性；
- **渲染与内存优化**：使用裁剪视图和批量顺序处理相机，限制渲染最大边长为 100px，显著降低显存占用与计算开销。

**动作识别融合流。** 优化完成的个性化虚拟形象被用于提取三维姿态特征。框架将姿态特征（以旋转矩阵 $\theta$ 表示）与从视频中提取的视觉编码拼接，送入一个两层、8 头的 Transformer 融合网络，输出多标签动作分类结果。这一设计使得**纯姿态流**（pose-only stream）本身即具备强竞争力，而视觉与姿态的融合则进一步提升了所有视觉骨干网络的动作识别性能。

最终，框架产出两个互补的数据集产物：**BigMaQ**（包含 173,543 帧三维形状数据、763 个标注动作、12,000 段视频及对应的包围框、掩码与关键点）和 **BigMaQ500**（一个包含超过 500 个动作的完整视频到三维姿态对应关系的动作识别基准）。

> **需要手动验证**：管道图中 SAM 2 与 YOLOv8/HRNet-W48 之间的具体数据依赖关系（并行调用还是串行级联）在正文中未明确描述，建议参照 Figure 3 及附录确认。



BigMaQ 的三维表面跟踪与动作识别框架由两条技术主线构成：**个性化三维表面重建管线**和**姿态‑视觉融合动作识别模块**。前者负责从多视角视频中恢复高精度、带纹理的猕猴三维虚拟形象，后者则利用该形象导出的姿态特征与视频编码器协同进行动作分类。

### 三维表面重建管线

表面重建的核心思想是：将高质量猕猴模板网格适配到每只个体，通过可微渲染和重投影约束，在多视角视频中联合优化形状、姿态、纹理和时间一致性。管线包含以下关键模块：

**模板网格与线性混合蒙皮（LBS）**。使用一个包含 10,632 顶点和 115 关节骨架的猕猴模板网格。变形后的顶点坐标通过以下公式计算：

$$ \mathbf{V}_P = \gamma \cdot \mathbf{R} \cdot \text{LBS}(\pmb{\theta}; \mathbf{V}, \mathbf{J}, \mathbf{W}) + \mathbf{t} $$

其中 $\pmb{\theta}$ 为关节旋转参数，$\mathbf{J}$ 为关节位置，$\mathbf{W}$ 为蒙皮权重，$\mathbf{R}$ 和 $\mathbf{t}$ 分别为全局旋转与平移，$\gamma$ 为全局缩放因子。该公式将模板顶点 $\mathbf{V}$ 通过 LBS 变形后，再施加全局刚体变换得到最终的空间顶点位置。

**个性化形状适配**。为适应不同个体的体型差异，联合学习骨骼长度参数 $\alpha$ 和顶点偏移 $\xi$，并施加平滑正则 $L_{sm}$ 防止偏移过度。这一设计使得同一模板网格可变形为针对特定猕猴的个性化三维模型。

**逐帧复合目标函数**。对于每一帧，优化目标为以下加权损失之和：

$$ L(\Theta) = \lambda_P L_P + \lambda_b L_b + \lambda_{sm} L_{sm} + \sum_{\text{cam } c} \left( \lambda_{kp} L_{kp}^c + \lambda_{sil} L_{sil}^c \right) $$

其中 $L_P$ 为姿态先验损失，$L_b$ 约束骨骼长度合理性，$L_{sm}$ 为顶点偏移平滑项。对每个相机视角 $c$，$L_{kp}^c$ 为关键点重投影损失，$L_{sil}^c$ 为轮廓损失。关键点重投影损失采用置信度加权均方误差形式：

$$ L_{kp}^{c}(\Theta) = \frac{1}{\sum_{k=1}^{N_K} w_k} \sum_{k=1}^{N_K} w_k \| \Pi_c(J_P^k) - P_c^k \|_2^2 $$

其中 $w_k$ 为 HRNet-W48 预测的二维关键点置信度，$\Pi_c$ 为相机投影函数，$J_P^k$ 为三维骨架关节点，$P_c^k$ 为对应的二维关键点。轮廓损失仅在关键点误差低于阈值 $\sigma_{kp}$ 时激活，防止错误轮廓误导优化：

$$ L_{sil}^{c}(\Theta) = \frac{1}{I_W^c I_H^c} \| \hat{S}^{(c)} - S^{(c)} \|_2^2, \quad \text{if } L_{kp}^{c}(J_P) < \sigma_{kp} $$

**时间一致性损失**。为增强跨帧运动平滑性，引入基于角速度的时间正则项。对 $T$ 帧序列中 $J$ 个关节，角速度损失定义为：

$$ L_{\mathrm{ang}} = \frac{1}{(T-1)J} \sum_{n=1}^{T-1} \sum_{j=1}^{J} \big\| \omega_j^{(n)} \big\|_2^2 $$

综合时间正则 $L_T$ 同时约束关节旋转、全局旋转的角速度以及全局平移的离散差分：

$$ L_T = L_{\mathrm{ang}}(\pmb\theta_{:T}) + L_{\mathrm{ang}}(\mathbf{r}_{:T}) + \frac{1}{T-1} \sum_{n=1}^{T-1} \big\lVert \mathbf{t}^{(n+1)} - \mathbf{t}^{(n)} \big\rVert_2^2 $$

**纹理与渲染优化**。为每个个体学习顶点颜色向量 $\mathbf{C}$，通过可微渲染生成图像 $\hat{\mathbf{I}}^{(c)} = \mathcal{R}(\Pi_c, \mathbf{V}_P, \mathbf{F}, \mathbf{C}, \boldsymbol{\ell})$，并最小化掩码光度损失：

$$ \mathcal{L}_{\mathrm{phot}} = \sum_{\mathbf{p}\in\Omega} \mathbf{S}^{(c)}(\mathbf{p}) \left| \hat{\mathbf{I}}^{(c)}(\mathbf{p}) - \mathbf{I}^{(c)}(\mathbf{p}) \right|_2 $$

通过 scaled sigmoid 函数将 $\mathbf{C}$ 限制在 $[0, 255]$ 范围内。采用裁剪视图和批量顺序处理相机的方式降低显存开销，限制渲染最大边长为 100px。

### 动作识别模块

动作识别采用两阶段 Transformer 架构。视觉编码器（如 ViT、DINOv2、VideoPrism）提取视频特征，姿态编码器从三维表面模型中提取姿态描述子。两者拼接后送入 Transformer 进行多标签动作分类。

**姿态表示**。从优化后的三维网格中可提取多种姿态特征：二维/三维关键点位置（KP-2D / KP-3D）、变形后的网格顶点坐标（M）、以及关节旋转矩阵形式（3D-Rot）。消融实验表明，旋转矩阵表示在所有视觉骨干下均取得最优 mAP，是信息最丰富的姿态描述子。

### 评估指标

表面重建质量采用三个指标衡量：

- **IoU**：渲染轮廓与 SAM 2 分割掩码的交并比，衡量表面拟合的空间准确性。
- **MPJPE**：三维骨架关节点与三角化关键点之间的平均欧氏距离：

$$ \mathrm{MPJPE}(\mathbf{J}_P, \mathbf{P}) = \frac{1}{N_K} \sum_{k=1}^{N_K} \| \mathbf{J}_P^{k} - \mathbf{P}^{k} \|_2 $$

- **MPJTD**：相邻帧间关节点位移的平均范数，衡量运动时序平滑性：

$$ \mathbf{MPJTD}(\mathbf{J}_P) = \frac{1}{T-1} \frac{1}{N_K} \sum_{n=1}^{T-1} \sum_{k=1}^{N_K} \| \mathbf{J}_P^{(n,k)} - \mathbf{J}_P^{(n+1,k)} \|_2 $$

动作识别以多标签平均精度均值（mAP）为核心指标，并按行为谱类别（移动、物体交互、社会交互、其他）进一步细分。



## 实验与关键发现

### 表面跟踪重建评估

BigMaQ 在四段代表性动作序列（Walk、Food Picking、Branch Shake、Scratch）上与现有方法进行了定量对比。**Table 2** 报告了序列级均值指标，BigMaQ 在所有三个维度上均显著优于基线方法 **MAMMAL**（An et al., 2023）：

- **IoU（交并比）**：BigMaQ 在四段动作上分别达到 0.883、0.855、0.831、0.843，相较 MAMMAL 的 0.771、0.756、0.757、0.722 提升约 10–13 个百分点。单帧总体 IoU 为 **0.844**，而 MAMMAL 仅为 0.714，通用哺乳动物表面模型 **AniMer+**（Lyu et al., 2025b）更低至 0.591（**Table 3**）。
- **MPJPE（平均每关节位置误差，mm）**：BigMaQ 在四段动作上分别为 20.402、16.489、13.633、20.481，较 MAMMAL 的 23.493、25.521、22.163、28.843 降低 4–11 mm。
- **MPJTD（平均每关节时间偏差，mm/frame）**：BigMaQ 在四段动作上分别为 6.875、9.062、15.515、4.422，较 MAMMAL 的 9.961、13.362、17.676、8.498 降低 14%–48%，表明引入的时间一致性损失有效提升了运动轨迹的平滑性。

定性对比（**Figure 4**）进一步显示，BigMaQ 的纹理化虚拟形象（BigMaQ-C）在未参与优化的新视角下仍能保持与图像高度一致的轮廓贴合，而 MAMMAL 和 AniMer+ 在四肢末端和身体轮廓处出现明显偏差。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_n7viYE7Xbo/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison of different surface-tracking approaches for BigMaQ, illustrated for four actions of different individuals (rows). Only perspectives that were not used for multi-view optimization are shown. The second and third columns show the surface fits of BigMaQ with color texture (BigMaQ-C) and without (BigMaQ-M)*

### 动作识别主结果

**Table 4** 报告了 BigMaQ500 基准上的动作识别性能。核心发现如下：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_n7viYE7Xbo/figures/008_Table_4.jpg]]
*Table 4: Comparison of action recognition based on pose representations θ and visual features including confidence intervals (mean ± std) for multiple training runs: Including pose features improves performance across visual backbones. The overall mean average precision (mAP) is further broken down by the categories defined in our ethogram: the subscripts L, OI, SI, and O denote Locomotion, Object Interaction, Social Interaction, and Others, respectively*

1. **纯姿态流（Pose-only stream）即具备强竞争力**：仅使用 3D 旋转矩阵姿态特征，mAP 达到 **43.5 ± 1.4**，超过除 DINOv2-base 外的所有纯视觉基线模型（如 ResNet50 Vis 34.3、ViT-base-cls Vis 32.9、TimeSformer Vis 36.3）。

2. **视觉+姿态融合普遍显著提升性能**：在 ResNet50、ViT-base-cls、ViT-base (patch tokens)、DINOv2-base-cls、DINOv2-base (patch tokens)、TimeSformer 六个视觉骨干上，Vis+Pose 的 mAP 均显著优于纯视觉 Vis。提升幅度最大的 ResNet50 从 34.3 跃升至 44.0（+9.7 点），ViT-base-cls 从 32.9 升至 44.0（+11.1 点）。视频级模型 VideoPrism-base 的 Vis+Pose 也达到 43.8 ± 2.9。

3. **社会互动（Social Interaction）是所有模型中最具挑战性的类别**，其子类 mAP 远低于移动（Locomotion）、物体交互（Object Interaction）等类别，表明多猴交互场景下的精细行为识别仍需突破。

### 姿态表示消融

**Table 5** 对比了三种姿态表示在动作识别中的效果：2D/3D 关键点位置（KP）、变形网格顶点位置（M）、以及旋转矩阵形式（3D-Rot）。结论明确：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_n7viYE7Xbo/figures/009_Table_5.jpg]]
*Table 5: Overall mAP scores for different pose representations in the BigMaQ action recognition task. Results are shown first for the pose-only stream, followed by ViT-base-cls, DINOv2-base, and VideoPrism visual features in combination with pose features. KP denotes keypoint positions in 2D and 3D, M the posed mesh’s vertex positions, and Rot the matrix form of θ that consistently outperforms other pose descriptors*

- **3D-Rot 在所有设置下均取得最优 mAP**：纯姿态流 43.5，ViT-base-cls + Pose 44.0，DINOv2-base + Pose 41.4，VideoPrism-base + Pose 43.8。
- 相比之下，3D 关键点（KP-3D）纯姿态流 mAP 仅 33.4，网格顶点（M）为 33.1，旋转矩阵高出约 10 个点。这表明关节旋转矩阵蕴含的姿态信息远比稀疏关键点或稠密顶点坐标更适合动作识别，且与视觉特征形成有效互补。

### 损失项消融

**Table 12** 通过依次移除动态优化中的关键损失权重，揭示了各约束项的作用强度：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_n7viYE7Xbo/figures/034_Table_12.jpg]]
*Table 12: Ablation experiment on weighting factors λ in dynamic optimization: mean error metrics for the entire time sequence of the action shown in Figure 11. IoU scores are averaged over time and across cameras involved in the surface reconstruction. Arrows indicate whether lower or higher values are better*

- **移除关键点损失（λ_kp = 0）导致灾难性失败**：MPJPE 从 16.479 mm 飙升至 210.081 mm，IoU 从 0.855 暴跌至 0.375，说明关键点重投影约束是表面拟合的绝对支柱。
- **移除轮廓损失（λ_sil = 0）** 使 IoU 从 0.855 轻微下降至 0.812，MPJPE 和 MPJTD 变化不大，表明轮廓作为辅助约束主要改善边界对齐，对关节点精度影响有限。
- **移除时间损失（λ_T = 0）** 导致运动平滑性显著下降（MPJTD 从 9.076 升至 10.620 mm/frame），但 IoU 几乎不变（0.855 vs 0.853），验证了时间正则主要作用于轨迹平滑而非单帧拟合精度。

### 标签置信度与视角数量消融

**Table 13** 检验了工程优化策略的贡献：

- **不使用标签置信度加权（w/o conf. values）** 在所有指标上均出现轻度退化：MPJPE 从 16.479 升至 18.676 mm，IoU 从 0.855 降至 0.847，证明了利用 HRNet-W48 关键点置信度和 YOLOv8 检测置信度进行加权的有效性。
- **减少优化所用相机视角数量** 会持续降低重建精度：从 6 视角降至 4 视角时退化尚可控，但降至 2 视角时 IoU 降至 0.801，MPJPE 升至 36.053 mm，表明多视角约束对高精度表面跟踪不可或缺。

### 失败模式分析

**Figure 12** 展示了典型失败案例，主要根因包括：

1. **多猴场景下的检测与关键点错误**：当多只猴子空间上靠近或部分遮挡时，YOLOv8 检测框可能发生身份混淆，HRNet-W48 关键点预测出现偏差，导致网格优化收敛到错误姿态。
2. **个体离开相机覆盖区域**：当目标猴子移出部分相机视场时，可用视角减少，三角化精度下降，表面拟合质量随之退化。
3. **贴近玻璃等反射表面**：前景分割掩码（SAM 2）在反射区域可能产生不完整轮廓，导致轮廓损失引导错误。
4. **低面片网格渲染伪影**：低面片模板在背部区域偶尔出现三角形伪影，可通过切换至高面片个性化网格缓解，但需额外存储开销。



## 定位与知识库关联

### 1. 与现有工作的关系

BigMaQ 的核心贡献在于将**多视角无标记运动捕获**与**个性化三维表面建模**引入非人灵长类动作识别，其方法谱系可从表面跟踪和动作识别两条线索追溯。

**表面跟踪线。** 在动物网格跟踪领域，BigMaQ 直接继承并扩展了 **MAMMAL**（An et al., 2023）的多视角模板网格优化框架。MAMMAL 已证明基于可微分渲染的逐帧拟合可重建动物表面，但其优化缺乏时间一致性约束，且未利用纹理信息。BigMaQ 在此基础上引入了三个关键改进：（1）**时间损失**——通过角速度损失 $L_{\mathrm{ang}}$ 和全局平移平滑项联合优化批次内连续帧，使关节轨迹的时间偏差（MPJTD）降低 14%–48%；（2）**纹理着色**——为每个个体学习顶点颜色向量 $\mathbf{C}$，通过掩码光度损失估计外观，使渲染结果具备视觉可解释性；（3）**渲染与内存策略**——采用裁剪视图和批量顺序处理相机，将渲染分辨率限制在最大边长 100px，显著降低显存占用。与另一基线 **AniMer+**（Lyu et al., 2025b）相比，BigMaQ 在单帧 IoU 上领先约 25 个百分点（0.844 vs 0.591），这主要源于 BigMaQ 使用了猕猴专用高面片模板网格（10,632 顶点）和个性化形状适配（学习骨骼长度 $\alpha$ 和顶点偏移 $\xi$），而 AniMer+ 依赖通用 SMAL 模型，缺乏物种特异性。

**动作识别线。** 在将姿态特征用于行为识别方面，BigMaQ 的独特之处在于首次系统比较了**三维表面模型导出的旋转矩阵特征**与传统的 2D/3D 关键点特征。实验表明，仅使用姿态流（pose-only stream）即可达到 mAP 43.5±1.4，超过除 DINOv2-base 外所有仅视觉基线模型（Table 4），这验证了高精度 3D 姿态本身蕴含丰富行为信息。与现有视频理解模型（**TimeSformer**, Bertasius et al., 2021; **VideoPrism-base**, Zhao et al., 2024）相比，BigMaQ 的 Vis+Pose 融合方案在六个视觉骨干上均取得显著提升，最高提升近 12 点 mAP（ResNet50: 34.3→44.0），证明姿态特征与视觉编码器的互补性。

### 2. 方法适用边界与局限

BigMaQ 的表面跟踪流水线依赖多个模块的级联输出，其性能边界由最弱环节决定：

- **关键点质量瓶颈。** 消融实验显示，移除关键点损失（$\lambda_{kp}=0$）导致 MPJPE 从 16.479 mm 激增至 210.081 mm，IoU 从 0.855 降至 0.375（Table 12），表明关键点是网格优化中最关键的约束项。因此，当 HRNet-W48 在多猴场景、个体离开相机视场或贴近玻璃时预测错误，姿态估计会显著退化或失败（Figure 12）。
- **多视角依赖。** 减少优化所用相机视角数量会持续降低重建精度：从 6 视角降至 2 视角时，IoU 从 0.855 降至 0.801，MPJPE 从 16.479 mm 升至 36.053 mm（Table 13）。当前方法仅适用于实验室多相机采集环境，无法直接推广至野外或单视角场景。
- **计算成本。** 动态姿态优化每动作需约 350 epochs（6.65 s/帧），难以实时部署。低面片网格渲染时背部偶尔出现三角面片伪影，虽可切换至高面片模型，但额外占用存储。
- **社会互动识别困难。** 在所有动作类别中，社会互动（Social Interaction）的 mAP 始终最低（Table 4），是多标签动作识别中最具挑战性的子类，可能与互动行为涉及多个个体间的精细时空关系有关。

### 3. 开放问题

基于 BigMaQ 的当前能力边界，以下方向值得进一步探索：

1. **单视角泛化。** 如何利用 BigMaQ 导出的高质量姿态先验正则化单视角重建方法，使表面跟踪技术可推广至野外非人灵长类研究？
2. **多猴场景鲁棒性。** 能否通过多视角一致检测协议或专用掩码质量判别器缓解多猴场景的标签错误，提升复杂社交场景下的跟踪稳定性？
3. **实时化。** 如何在保持重建精度的前提下大幅降低表面拟合的计算成本，使之向实时交互和闭环神经科学实验延伸？
4. **行为学扩展。** 当前动作标签仅覆盖实验室特定猕猴群体的有限行为类别，如何扩展至更广泛的野外行为并获得行为学专家共识？
5. **跨领域应用。** 除动作识别外，高精度 3D 姿态与外观模型还能为神经科学（如脑-行为关联分析）或社会行为计算（如支配等级推断）带来哪些新发现？



## 原文 PDF

![[paperPDFs/ICLR_2026/BigMaQ_A_Big_Macaque_Motion_and_Animation_Dataset_Bridging_Image_and_3D_Pose_Representations.pdf]]
