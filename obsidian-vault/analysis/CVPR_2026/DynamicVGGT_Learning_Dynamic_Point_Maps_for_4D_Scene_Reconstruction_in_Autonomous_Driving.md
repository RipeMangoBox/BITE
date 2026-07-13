---
title: "DynamicVGGT: Learning Dynamic Point Maps for 4D Scene Reconstruction in Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DynamicVGGT_Learning_Dynamic_Point_Maps_for_4D_Scene_Reconstruction_in_Autonomous_Driving.pdf
project_link: null
code_link: null
aliases:
- DynamicVGGT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入运动感知时间注意力（MTA）模块和统一的动态点图（DPM）表示，联合预测当前与未来点图，并利用场景流监督显式建模高斯速度，突破静态几何到动态运动的因果屏障。
primary_logic: 在共享规范坐标系中直接预测点图对并计算隐式位移，避免显式外参对齐；同时用可学习运动Token引导时间注意力，并通过3D高斯渲染与场景流监督细化动态几何，实现端到端的前馈4D重建。
claims:
- 联合预测当前与未来点图可实现隐式运动学习。
- MTA模块通过可学习运动Token编码帧间运动信息，引导时间注意力聚焦运动一致区域。
- 消融实验表明添加时序注意力和未来点预测头可将KITTI精度从1.489降至0.927，完整性从0.690降至0.600；引入DGSHead进一步提升精度至0.901和法向一致性至0.939。
- KITTI (monocular, Mean) 上 Accuracy ↓ = 0.901
---

# DynamicVGGT: Learning Dynamic Point Maps for 4D Scene Reconstruction in Autonomous Driving

> [!tip] 核心洞察
> 在共享规范坐标系中直接预测点图对并计算隐式位移，避免显式外参对齐；同时用可学习运动Token引导时间注意力，并通过3D高斯渲染与场景流监督细化动态几何，实现端到端的前馈4D重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | DynamicVGGT：面向自动驾驶的4D场景重建动态点图学习 |
| 英文题名 | DynamicVGGT: Learning Dynamic Point Maps for 4D Scene Reconstruction in Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.08254) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DynamicVGGT |
| Dataset | KITTI, Waymo |

> [!tip] 效果简介
> - KITTI (monocular, Mean) 上，Accuracy ↓ 0.901 vs 1.489 (VGGT) (-0.588)。
> - Waymo (Mean) 上，Accuracy ↓ 4.021 vs 4.635 (VGGT) (-0.614)。

## 概要

### 问题与瓶颈

自动驾驶场景的三维重建正从静态几何感知向动态时序理解演进。现有前馈三维模型（如 **VGGT**，Wang et al., CVPR 2025）在静态多视图重建中表现优异，但其核心瓶颈在于缺乏对动态场景的时间建模能力：它们无法捕捉运动物体的位移模式，也难以建模长程时序依赖。这导致在包含车辆、行人等动态目标的驾驶场景中，重建结果出现几何断裂与时序不一致。

### 核心方法定位

DynamicVGGT 针对上述瓶颈，提出了一套统一的前馈四维重建框架。其核心洞察是：**在共享的规范坐标系中联合预测当前帧与未来帧的点图对，使模型通过时序对应关系隐式学习动态点表示，从而无需显式的外参对齐即可捕获运动信息。**

方法定位如下：

- **动态点图（DPM）表示**：将不同时刻的点图对齐到同一参考坐标系，避免显式依赖帧间外参变换，构建统一的动态几何表示。
- **运动感知时间注意力（MTA）模块**：引入可学习的运动 Token，在特征层面显式编码帧间运动信息，引导时间注意力聚焦于运动一致区域。
- **双任务互补设计**：未来点预测头（FPH）学习隐式运动，动态三维高斯泼溅头（DGSHead）通过场景流监督显式建模高斯速度，二者协同细化动态几何。
- **两阶段课程训练**：合成数据预训练后，在真实数据上微调，并引入深度蒸馏策略缓解稀疏 LiDAR 噪声的影响。

### 主要结果

在 KITTI（单目）和 Waymo 数据集上，DynamicVGGT 相较静态基线 VGGT 取得了显著提升：

- **KITTI**：精度（Accuracy）从 1.489 降至 **0.901**，完整性（Completeness）从 0.690 降至 **0.600**。
- **Waymo**：精度从 4.635 降至 **4.021**，完整性从 2.332 降至 **2.103**。

消融实验证实了各模块的因果贡献：添加时序注意力与未来点预测头即可将 KITTI 精度从 1.489 改善至 0.927；进一步引入 DGSHead 将精度提升至 0.901，并将法向一致性提升至 0.939。深度蒸馏策略有效缓解了稀疏 LiDAR 造成的深度图不平滑与点云粗糙问题。

### 局限与展望

DynamicVGGT 依赖冻结的 VGGT 骨干，可能限制端到端适应新场景的能力；常速度运动假设仅适用于短时序片段；真实数据中的稀疏 LiDAR 噪声虽经深度蒸馏缓解，仍会导致一定的性能退化。这些局限为后续研究指明了方向：更灵活的动态运动模型、更鲁棒的真实数据训练策略，以及骨干网络的自适应解冻机制。

自动驾驶系统对环境的精确感知是安全决策的基础。近年来，前馈3D重建方法取得了显著进展，其中**VGGT**（Wang et al., CVPR 2025）通过交替注意力机制在静态场景中实现了高质量的多视图几何重建。然而，真实驾驶场景本质上是动态的——车辆、行人等运动物体持续改变其空间位置，形成了静态几何向动态4D理解的关键缺口。

现有前馈3D模型面临一个根本性瓶颈：**缺乏对动态场景的时间建模能力**。这些模型仅预测当前帧的点图，无法捕捉跨帧的运动信息与长程时序依赖。当场景中存在显著运动时，静态模型不仅丢失了运动物体的轨迹信息，其几何重建质量也会因时序不一致而退化。**StreamVGGT**（Zhuo et al., arXiv 2025）尝试将时序注意力引入VGGT框架，但其设计面向室内场景，缺乏对自动驾驶中大规模运动、稀疏观测和复杂动态的针对性建模。

DynamicVGGT正是针对这一瓶颈而提出。其核心动机在于回答一个关键问题：**能否在不依赖显式相机外参对齐的前提下，让前馈模型直接学习动态场景的几何与运动？** 为此，该方法引入统一的动态点图（Dynamic Point Maps, DPM）表示，在共享规范坐标系中联合预测当前与未来点图，使模型通过时序对应隐式学习动态表征。同时，通过运动感知时间注意力（MTA）模块和动态3D高斯泼溅头（DGSHead），模型得以显式建模帧间运动信息，从而突破从静态几何到动态运动的因果屏障。

## 核心方法与创新机理

DynamicVGGT 的核心创新在于将前馈式静态 3D 重建模型 **VGGT**（Wang et al., CVPR 2025）扩展为面向自动驾驶场景的动态 4D 重建框架，其关键突破体现在以下四个“changed slots”上。

### 1. 运动感知时间注意力（MTA）模块

现有静态基线仅使用交替注意力（AA）块进行帧内空间几何推理，缺乏对帧间时间依赖的建模能力。DynamicVGGT 引入 **运动感知时间注意力（Motion-aware Temporal Attention, MTA）** 模块，通过可学习的运动 Token 并行建模帧间时间依赖关系。具体而言，第 $l$ 层 MTA 的输入定义为：

$$F_{m,v,t}^{(l)} = \begin{cases} \mathrm{Concat}(M_{v,t}^{(l)}, F_{v,t}^{p(l)}), & l=1, \\ \mathrm{Concat}(M_{v,t}^{(l)}, F_{v,t}^{p(l)} + F_{v,t}^{p(l-1)}), & l>1, \end{cases}$$

其中 $M_{v,t}^{(l)}$ 为运动 Token，$F_{v,t}^{p(l)}$ 为图像块 Token。时间注意力权重融合了旋转位置编码：

$$A_{t,t'}^{(l)} = \mathrm{Softmax}\left(\frac{Q_t^{\mathrm{attn},(l)}(K_{t'}^{\mathrm{attn},(l)})^\top}{\sqrt{d}} + B_{t,t'}^{\mathrm{time}}\right)$$

该模块使模型能够显式地在特征层面建模运动线索，引导时间注意力聚焦于运动一致区域，从而突破静态几何到动态运动的因果屏障。

### 2. 未来点预测头（FPH）与隐式运动学习

VGGT 仅预测当前帧的点图，无法捕捉场景动态。DynamicVGGT 引入 **未来点预测头（Future Point Head, FPH）**，从时序增强特征 $TA_{v,t}$ 直接预测下一帧的点图：

$$\hat{P}_{v,t+\delta}^{\mathrm{fut}} = \mathrm{DPT}_p(TA_{v,t})$$

并施加时序一致性正则损失，强制预测位移场与真实位移场一致：

$$\mathcal{L}_{\mathrm{temp}} = \frac{1}{|\mathcal{N}|}\sum_{i\in\mathcal{N}} \left\|(\mathbf{p}_{v,t+\delta}^{(i)}-\mathbf{p}_{v,t}^{(i)}) - (\hat{\mathbf{p}}_{v,t+\delta}^{(i)}-\hat{\mathbf{p}}_{v,t}^{(i)})\right\|_1$$

这一设计使模型能够在共享规范坐标系中隐式学习动态点表示，避免了显式外参对齐的需求。

### 3. 动态 3D 高斯泼溅头（DGSHead）与显式运动建模

为进一步细化动态几何，DynamicVGGT 设计了 **动态 3D 高斯泼溅头（Dynamic 3D Gaussian Splatting Head, DGSHead）**。该模块融合图像外观特征与几何特征，使用可学习运动 Token 解码高斯速度基，并以场景流监督显式建模高斯运动：

$$\mu_{i,t+\delta} = \mu_{i,t} + \delta \cdot \nu_{i,t}$$

场景流监督损失为：

$$\mathcal{L}_{\mathrm{flow}} = \mathrm{MSE}(\mathbf{s}_{v,t}, \hat{\mathbf{s}}_{v,t})$$

这一设计补偿了冻结 AA 块导致的外观线索弱化问题，使模型在保持预训练几何先验的同时，获得高质量的动态渲染能力。

### 4. 两阶段课程训练与深度蒸馏

DynamicVGGT 采用两阶段课程训练策略：首先在合成数据上预训练，随后在真实数据上微调。针对真实驾驶数据中稀疏 LiDAR 导致的深度图不平滑和点云粗糙问题，引入深度蒸馏策略，以第一阶段点图深度作为教师信号正则化高斯深度预测：

$$\mathcal{L}_{\mathrm{distill}} = \|D_{g,v,t} - \mathrm{sg}(D_{v,t}^{\mathrm{pm}})\|_1$$

该策略有效缓解了稀疏监督带来的噪声，稳定了高斯优化过程。

### 因果链路总结

上述四个 changed slots 形成了一条清晰的因果链：**MTA 模块**提供时序特征基础 → **FPH** 实现隐式运动学习 → **DGSHead** 细化显式动态几何 → **深度蒸馏** 保障真实数据训练稳定性。消融实验（Table 4）验证了这一链路：从 VGGT 基线出发，添加时序注意力和未来点预测头将 KITTI 精度从 1.489 降至 0.927，完整性从 0.690 降至 0.600；引入 DGSHead 后精度进一步提升至 0.901，法向一致性提升至 0.939。

DynamicVGGT 的整体管线围绕**动态点图（Dynamic Point Map, DPM）** 这一统一几何表示展开，将静态多视图三维感知扩展为端到端的前馈四维重建，无需显式相机外参对齐或稠密场景标注。其核心设计遵循一条清晰的因果链：**共享坐标系的点图对 → 运动感知时间注意力 → 隐式/显式运动联合建模 → 动态高斯渲染**。

### 输入输出与模块拓扑

给定一段多视图图像序列 $\{V_1, V_2, V_3\}$（每个 $V_t$ 包含多个视角的图像），模型以端到端方式输出：

- 当前帧与未来帧的**点图预测** $\hat{P}_{v,t}, \hat{P}_{v,t+\delta}$，用于隐式运动学习；
- 带速度的**动态 3D 高斯原语**，支持新视角合成与显式运动建模。

管线由以下模块串联构成（对应 Figure 2 架构）：

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_08254/figures/002_Figure_2.jpg]]
*Figure 2: Proposed DynamicVGGT training framework. Given a sequence of multi-view images*

1. **DINOv2 骨干网络**：对每个视角的图像提取图像块 Token 和相机 Token，提供通用的视觉先验。
2. **交替注意力（AA）模块**：对单帧内的空间几何进行推理。该模块继承自预训练的 VGGT（Wang et al., CVPR 2025）并被**冻结**，以保留其静态几何先验。
3. **运动感知时间注意力（MTA）模块**：与 AA 模块并行工作，通过可学习的运动 Token 显式编码帧间运动信息，引导时间注意力聚焦于运动一致区域，输出时序增强特征 $TA_{v,t}$。
4. **未来点预测头（FPH）**：从 $TA_{v,t}$ 预测下一帧的点图 $\hat{P}_{v,t+\delta}^{\text{fut}}$，并通过时序一致性损失 $\mathcal{L}_{\text{temp}}$ 约束预测位移场与真实位移场一致，从而**隐式**学习逐点运动。
5. **动态 3D 高斯泼溅头（DGSHead）**：融合图像外观特征 $F_{v,t}^{\text{app}}$ 与几何特征 $F_{g,v,t}$，从 $TA_{v,t}$ 解码高斯深度 $D_{g,v,t}$ 与速度 $\nu_{i,t}$，以场景流监督 $\mathcal{L}_{\text{flow}}$ **显式**约束高斯运动，输出可渲染的动态高斯场。

### 数据流与关键设计决策

数据流的核心瓶颈在于**如何将静态几何先验转化为动态运动理解**。DynamicVGGT 通过以下因果机制解决这一问题：

- **共享参考坐标系下的点图对**：模型联合预测 $\hat{P}_{v,t}$ 与 $\hat{P}_{v,t+\delta}$，两者定义在同一坐标系中，使模型能通过时序对应**隐式**学习动态点表示（Eq. 4），避免了显式外参对齐的复杂性。
- **运动 Token 作为信息瓶颈**：可学习的运动 Token $M_{v,t}^{(l)}$ 在 MTA 各层中与图像块 Token 拼接，作为帧间运动信息的载体。时间注意力权重 $A_{t,t'}^{(l)}$ 融合旋转位置编码 $B_{t,t'}^{\text{time}}$（Eq. 6），使注意力机制能感知帧间时间距离。
- **外观特征融合补偿冻结骨干的信息损失**：由于 AA 模块被冻结以保留预训练先验，模型倾向于过度强调几何推理而弱化外观线索。DGSHead 通过卷积提取图像特征 $F_{v,t}^{\text{app}}$ 并与几何特征融合，补偿渲染所需的外观信息。
- **两阶段课程训练**：第一阶段在合成数据上预训练点图预测与隐式运动学习（损失函数见 Eq. 16）；第二阶段在真实数据上微调，引入**深度蒸馏损失** $\mathcal{L}_{\text{distill}}$ 以第一阶段点图深度为教师信号，缓解稀疏 LiDAR 监督带来的深度不平滑与点云粗糙问题（Figure 4）。

### 证据强度评估

上述框架设计的有效性由消融实验（Table 4）提供强证据支持：从 VGGT 基线出发，添加时间注意力与未来点预测头使 KITTI 精度从 1.489 降至 0.927、完整性从 0.690 降至 0.600；进一步引入 DGSHead 将精度提至 0.901、法向一致性提至 0.939。这些结果直接验证了 MTA 模块与双头设计（隐式+显式运动建模）的因果贡献，证据置信度较高。

DynamicVGGT 的核心架构由四个关键模块构成，其设计围绕一个统一的动态点图（Dynamic Point Map, DPM）表示展开。整体框架如图 Figure 2 所示：给定多视图图像序列，模型首先通过冻结的 DINOv2 骨干网络提取各视图的 Patch Token 和 Camera Token，同时初始化可学习的 Motion Token 以编码时序先验。随后，空间交替注意力（AA）模块与运动感知时间注意力（MTA）模块并行处理这些 Token，分别建模帧内几何与帧间运动。最后，时序增强特征 $TA$ 分别送入未来点预测头（FPH）和动态 3D 高斯泼溅头（DGSHead），完成隐式与显式的动态建模。

### 动态点图（DPM）公式化

静态点图定义为通过相机内外参反投影得到的 3D 坐标：

$$P_{v,t} = \pi^{-1}(I_{v,t}; K_{v,t}, E_{v,t})$$

其中 $I_{v,t}$ 为视图 $v$ 在时刻 $t$ 的图像，$K_{v,t}$、$E_{v,t}$ 分别为内参与外参。为统一建模动态场景，所有帧的点图被对齐到共享参考坐标系：

$$P_{v,t}^{(\mathrm{ref})} = \mathcal{T}_{(v,t)\mathrm{ref}}\big(\pi^{-1}(I_{v,t}; K_{v,t}, E_{v,t})\big)$$

这一对齐操作避免了在动态公式化中显式依赖外部指定的帧到参考坐标系的变换。模型的核心任务是联合预测当前与未来点图：

$$\hat{P}_{v,t}, \hat{P}_{v,t+\delta} = f_\theta(\{I_{v,t}\})|_{(v,t),(v,t+\delta)}$$

通过在共享坐标系中预测点图对，模型能够通过时序对应隐式学习动态点表示，无需显式的外参对齐。

### 运动感知时间注意力（MTA）

MTA 模块在特征层面显式建模运动线索。第 $l$ 层 MTA 的输入由 Motion Token $M_{v,t}^{(l)}$ 与 Patch Token $F_{v,t}^{p(l)}$ 拼接而成，并通过残差连接融合前一层特征：

$$F_{m,v,t}^{(l)} = \begin{cases} \mathrm{Concat}(M_{v,t}^{(l)}, F_{v,t}^{p(l)}), & l=1, \\ \mathrm{Concat}(M_{v,t}^{(l)}, F_{v,t}^{p(l)} + F_{v,t}^{p(l-1)}), & l>1 \end{cases}$$

时间注意力权重融合了旋转位置编码 $B_{t,t'}^{\mathrm{time}}$，以编码帧间时序关系：

$$A_{t,t'}^{(l)} = \mathrm{Softmax}\left(\frac{Q_t^{\mathrm{attn},(l)}(K_{t'}^{\mathrm{attn},(l)})^\top}{\sqrt{d}} + B_{t,t'}^{\mathrm{time}}\right)$$

可学习 Motion Token 动态编码帧间运动信息，引导时间注意力聚焦于运动一致区域，这是突破静态几何到动态运动建模的关键机制。

### 未来点预测头（FPH）

FPH 从时序增强特征 $TA_{v,t}$ 直接预测下一帧的点图，实现隐式运动学习：

$$\hat{P}_{v,t+\delta}^{\mathrm{fut}} = \mathrm{DPT}_p(TA_{v,t})$$

为确保预测的时序一致性，引入时序一致性正则损失，强制预测位移场与真实位移场一致：

$$\mathcal{L}_{\mathrm{temp}} = \frac{1}{|\mathcal{N}|}\sum_{i\in\mathcal{N}} \left\|(\mathbf{p}_{v,t+\delta}^{(i)}-\mathbf{p}_{v,t}^{(i)}) - (\hat{\mathbf{p}}_{v,t+\delta}^{(i)}-\hat{\mathbf{p}}_{v,t}^{(i)})\right\|_1$$

### 动态 3D 高斯泼溅头（DGSHead）

DGSHead 提供显式的运动监督。首先，通过卷积提取图像外观特征以补偿冻结 AA 块导致的外观信息弱化：

$$F_{v,t}^{\mathrm{app}} = \mathrm{Conv}(I_{v,t})$$

随后从时序增强特征预测高斯特征与深度：

$$F_{g,v,t}, D_{g,v,t} = \mathrm{DPT}_g(TA_{v,t})$$

高斯中心由预测深度与相机参数重建的点图初始化，并假设常速度运动模型：

$$\mu_{i,t+\delta} = \mu_{i,t} + \delta \cdot \nu_{i,t}$$

其中 $\nu_{i,t}$ 为可学习 Motion Token 解码得到的高斯速度。场景流监督损失显式约束高斯运动与真实场景流一致：

$$\mathcal{L}_{\mathrm{flow}} = \mathrm{MSE}(\mathbf{s}_{v,t}, \hat{\mathbf{s}}_{v,t})$$

### 训练目标与深度蒸馏

第一阶段在合成数据上预训练，组合损失为：

$$\mathcal{L}_{\mathrm{stage1}} = \mathcal{L}_{\mathrm{cam}} + \mathcal{L}_{\mathrm{depth}} + \mathcal{L}_{\mathrm{point}}^{(t)} + \mathcal{L}_{\mathrm{point}}^{(t+\delta)} + \lambda_{\mathrm{temp}} \mathcal{L}_{\mathrm{temp}}$$

第二阶段在真实数据上微调，针对稀疏 LiDAR 导致的深度噪声问题，引入深度蒸馏策略，以第一阶段点图深度作为教师信号正则化高斯深度预测：

$$\mathcal{L}_{\mathrm{distill}} = \|D_{g,v,t} - \mathrm{sg}(D_{v,t}^{\mathrm{pm}})\|_1$$

其中 $\mathrm{sg}(\cdot)$ 为停止梯度操作。该策略有效缓解了点云稀疏性带来的深度不平滑和点图粗糙问题（见 Figure 4）。

## 实验与关键发现

### 点图重建主结果

DynamicVGGT在KITTI与Waymo两个自动驾驶基准上进行了点图重建评估，结果汇总于Table 1。KITTI采用单目输入，每相机取连续3帧；Waymo采用FRONT、SIDE LEFT、SIDE RIGHT三个相机，各取3帧（步长4），每组共9张图像。

在KITTI上，DynamicVGGT将Accuracy从VGGT基线的1.489大幅降至0.901（↓0.588），Normal Consistency达到0.939。在Waymo上，Accuracy从4.635降至4.021（↓0.614），Normal Consistency达到0.603。这一提升的关键在于运动感知时间注意力（MTA）模块与未来点预测头（FPH）的联合作用：MTA通过可学习运动Token并行建模帧间时间依赖，FPH从时序增强特征预测下一帧点图并施加时序一致性正则损失，使模型在共享参考坐标系中隐式学习动态点表示。定性对比（Figure 5）进一步表明，DynamicVGGT重建的点图比VGGT更稠密、更平滑，且在大视角或场景变化下仍保持时序几何一致性。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_08254/figures/006_Figure_5.jpg]]
*Figure 5: Point map reconstruction. DynamicVGGT reconstructs denser, smoother, and more geometrically consistent point maps than VGGT, maintaining temporal coherence even under large viewpoint or scene changes. Zoom in for better view*

### 4D场景重建与新视角合成

在Waymo验证集上，DynamicVGGT与现有方法进行了4D场景重建对比（Table 2）。在动态区域，DynamicVGGT取得PSNR 18.07、SSIM 0.376，在无需相机外参显式对齐的前提下实现了有竞争力的渲染质量。这得益于动态3D高斯泼溅头（DGSHead）的设计：它融合图像外观特征与几何特征以补偿冻结AA块导致的外观信息弱化，并利用可学习运动Token解码高斯速度，在场景流监督下显式建模高斯运动。Figure 6展示了给定帧0、2、4作为输入时，模型重建对应场景并合成下一帧新视角的结果——在KITTI与Waymo的动态驾驶场景中均实现了高质量重建与逼真的新视角生成。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_08254/figures/007_Table_2.jpg]]
*Table 2: Comparison to state-of-the-art methods on Waymo (val). PSNR and SSIM are reported. Full: requires dense scene annotations. Camera: requires camera intrinsics and extrinsics*

### 深度估计结果

Table 3报告了单目与多视图深度估计结果。在KITTI单目设置下，DynamicVGGT取得Abs Rel 0.070，展现出较强的深度预测能力。然而，真实数据中的稀疏LiDAR点云会劣化深度图质量，导致深度图不够平滑、点云更粗糙（Figure 4）。为此，论文引入深度蒸馏策略：以第一阶段点图深度作为教师信号，用L1损失正则化高斯深度预测（$\mathcal{L}_{\mathrm{distill}} = \|D_{g,v,t} - \mathrm{sg}(D_{v,t}^{\mathrm{pm}})\|_1$），有效缓解了稀疏监督带来的噪声并稳定了高斯优化过程。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_08254/figures/004_Figure_4.jpg]]
*Figure 4: Depth and Point Maps Comparison. The sparsity of LiDAR point clouds degrades the results, leading to less smooth depth maps and rougher point clouds*

### 消融实验

Table 4的系统消融揭示了各组件的因果贡献。以VGGT为起点，添加时序注意力与未来点预测头使KITTI Accuracy从1.489降至0.927，Completeness从0.690降至0.600——这验证了时间建模与隐式运动学习的核心价值。进一步引入动态3DGS头后，Accuracy提升至0.901，Normal Consistency提升至0.939，表明显式场景流监督对动态几何细化至关重要。

### 失败模式与局限

尽管DynamicVGGT在多个指标上取得显著提升，仍存在若干值得注意的失败模式：

1. **冻结骨干的适应性问题**：模型依赖冻结的VGGT骨干以保留预训练先验，但这可能限制对新场景的端到端适应能力。虽然通过图像特征融合补偿了外观信息的弱化，但未从根本上解决信息损失。
2. **常速度运动假设的边界**：高斯运动建模采用常速度假设（$\mu_{i,t+\delta} = \mu_{i,t} + \delta \cdot \nu_{i,t}$），仅适用于短时序片段。对于长程或非刚性运动场景，该假设可能不够精确。
3. **稀疏LiDAR噪声残留**：深度蒸馏策略虽缓解了稀疏LiDAR带来的噪声影响，但无法完全消除。在极端稀疏区域，深度图与点云质量仍会出现退化（Figure 4），这在实际部署中需额外注意。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_08254/figures/005_Table_1.jpg]]
*Table 1: Point Map Reconstruction on KITTI and Waymo(val). KITTI uses monocular input with every 3 consecutive frames per camera. Waymo uses 3 frames (stride 4) from FRONT, SIDE LEFT, and SIDE RIGHT cameras, totaling 9 images per group*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2603_08254/figures/009_Table_4.jpg]]
*Table 4: Ablation study. We evaluate ablated variants of DynamicVGGT on point map estimation over KITTI and Waymo (val). KITTI uses monocular input with three consecutive frames, while Waymo uses 3 frames (stride 4) from the FRONT, SIDE LEFT, and SIDE RIGHT cameras, yielding 9 images per sample. Metrics include Accuracy (Acc.), Completeness (Comp.), Normal Consistency (NC)*

## 定位与知识库关联

### 1. 基线关系与差异化定位

DynamicVGGT 的直接技术锚点是 **VGGT**（Wang et al., CVPR 2025），该工作在前馈式多视图静态重建中取得了突破性进展，但其核心交替注意力（Alternating-Attention, AA）模块仅建模帧内空间几何，完全缺乏时间维度上的信息交互能力。DynamicVGGT 将这一静态范式系统性地扩展至动态 4D 场景，其核心差异化体现在三个层面：

**时间建模的因果突破。** VGGT 的 AA 模块在帧间独立运行，无法感知运动线索。DynamicVGGT 引入**运动感知时间注意力（MTA）模块**，通过可学习运动 Token 并行建模帧间时间依赖，并以旋转位置编码显式注入时序先验。这一设计使得模型能够聚焦运动一致区域，而不需要显式的外参对齐——这是静态模型向动态模型跨越的关键因果杠杆。

**表示空间的统一扩展。** VGGT 仅预测当前帧的静态点图。DynamicVGGT 提出**统一动态点图（DPM）表示**，在共享参考坐标系中联合预测当前与未来点图对，通过点图间的隐式位移场学习运动信息。这一设计避免了显式帧间变换估计，将运动建模内化为几何表示的固有属性。

**动态几何的显式细化。** 纯隐式运动学习虽能提供时序一致性约束，但难以精确捕捉细粒度动态几何。DynamicVGGT 进一步引入**动态 3D 高斯泼溅头（DGSHead）**，利用可学习运动 Token 解码高斯速度，并以场景流监督显式约束高斯原语的运动。这形成了“隐式位移学习 + 显式运动监督”的双重动态建模机制。

另一个相关基线是 **StreamVGGT**（Zhuo et al., arXiv 2025），该工作同样尝试为 VGGT 引入时序注意力。然而，StreamVGGT 的设计面向室内场景，其时间建模策略未针对自动驾驶场景中的大规模运动、稀疏 LiDAR 噪声和长程时序依赖进行专门优化。DynamicVGGT 在以下方面形成差异化：引入深度蒸馏策略应对真实 LiDAR 数据的稀疏性；采用两阶段课程训练（合成数据预训练 → 真实数据微调）实现稳定收敛；通过图像外观特征融合补偿冻结 AA 模块造成的外观信息弱化。

### 2. 方法适用边界

DynamicVGGT 的设计假设和训练策略决定了其适用范围存在明确边界：

**场景域限制。** 方法依赖冻结的 DINOv2 骨干和 VGGT 预训练权重，其几何先验主要来自大规模合成数据和多视图自动驾驶数据。对于与训练域差异显著的场景（如极端光照、非刚性形变主导的环境），模型的泛化能力存在不确定性。论文通过图像特征融合分支部分补偿了外观信息的弱化，但未从根本上解决骨干冻结带来的域适应瓶颈。

**运动假设约束。** DGSHead 采用常速度运动模型（$\mu_{i,t+\delta} = \mu_{i,t} + \delta \cdot \nu_{i,t}$），仅适用于短时序片段内的刚体或准刚体运动。对于长时序跨度、显著非刚性形变或运动模式突变的场景，该假设可能导致动态几何建模精度的退化。

**数据质量依赖。** 在真实自动驾驶数据上，稀疏 LiDAR 点云作为监督信号会引入显著的深度噪声，导致点图粗糙和深度不平滑（见 Figure 4）。深度蒸馏策略通过第一阶段点图深度作为教师信号缓解了该问题，但无法完全消除噪声影响。这意味着在 LiDAR 线数较低或点云密度极度稀疏的场景中，性能退化仍不可避免。

**相机配置要求。** 方法在 Waymo 上使用 3 帧（步长 4）来自 FRONT、SIDE LEFT 和 SIDE RIGHT 三个相机共 9 张图像作为输入组，在 KITTI 上使用单目连续 3 帧。多视图输入的视场覆盖和帧间步长直接影响时间注意力的感受野范围，对于相机数量更少或帧率更低的配置，运动感知能力可能受限。

### 3. 局限与开放问题

**骨干冻结的双刃剑效应。** 冻结 VGGT 的 AA 模块保留了预训练的强几何先验，但也阻断了端到端适应新场景的路径。论文通过融合图像外观特征来补偿外观线索的弱化，但这种补偿是附加式的而非结构性的。一个开放问题是：是否存在更优的冻结策略（如部分解冻或适配器微调），能在保留几何先验的同时提升域适应能力？

**常速度假设的泛化边界。** 当前的运动模型适用于短时序片段，但对于包含急加速、急减速或非刚性运动（如行人姿态变化）的自动驾驶场景，常速度假设可能失效。如何在不显著增加模型复杂度的前提下引入更高阶的运动模型，是一个值得探索的方向。

**稀疏监督下的深度质量。** 深度蒸馏策略缓解了 LiDAR 稀疏性带来的噪声问题，但其本质上是用一个预测（第一阶段点图深度）监督另一个预测（高斯深度），存在误差累积的风险。引入额外的密集深度先验（如单目深度估计模型的预测）或自监督深度一致性约束，可能是进一步提升深度质量的方向。

**动态与静态的联合优化平衡。** DynamicVGGT 通过未来点预测头学习隐式运动，通过 DGSHead 学习显式运动，两者共享时间增强特征 $TA_{v,t}$。然而，静态区域和动态区域对时间注意力的需求可能存在冲突——静态区域需要抑制时间扰动以保持几何一致性，动态区域则需要增强时间敏感度以捕捉运动细节。当前设计未显式区分动静区域，如何在特征层面实现动静解耦是值得深入研究的开放问题。

**计算效率与实时性。** 论文未报告推理延迟或计算开销数据。考虑到方法在 VGGT 基础上增加了 MTA 模块、DGSHead 和未来点预测头，且涉及两阶段训练流程，其实时部署的可行性需要进一步验证。对于自动驾驶等对延迟敏感的应用，模型轻量化或推理加速是必要的后续工作。

## 原文 PDF

![[paperPDFs/CVPR_2026/DynamicVGGT_Learning_Dynamic_Point_Maps_for_4D_Scene_Reconstruction_in_Autonomous_Driving.pdf]]
