---
title: "Quo Vadis: Is Trajectory Forecasting the Key Towards Long-Term Multi-Object Tracking?"
type: paper
paper_level: A
venue: NeurIPS
year: 2022
pdf_ref: paperPDFs/NEURIPS_2022/Quo_Vadis_Is_Trajectory_Forecasting_the_Key_Towards_Long_Term_Multi_Object_Tracking.pdf
aliases:
- QVITFKTLTMOT
tags:
- NEURIPS_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "在鸟瞰视图（BEV）空间中对丢失轨迹进行多样化且考虑不确定性的长时轨迹预测，从而大幅缩小关联搜索空间，是实现长时跟踪的关键操作。"
primary_logic: "核心洞见在于：通过数据驱动单应性变换将单目检测提升至BEV空间，并在该空间中利用少量但覆盖多模态的生成式轨迹预测，能够有效替代复杂的表观匹配，显著桥接长时遮挡。"
claims:
- "现有先进跟踪器仅能成功关联不到10%的超过3秒的遮挡。"
- "引入BEV轨迹预测后，MOT17 test HOTA从63.05提升至63.14，IDSW减少93；MOT20 test HOTA提升0.10pp，IDSW减少36。"
- "在BEV空间中预测（即使线性Kalman）远优于像素空间预测，且使用多模态生成预测器（MG-GAN 3个样本）在少量预测下即获得最佳跟踪性能。"
- "预测损失（FDE/ADE）的最优并非带来最好跟踪性能；少量多样化且考虑局部不确定性的预测才是关键。"
---

# Quo Vadis: Is Trajectory Forecasting the Key Towards Long-Term Multi-Object Tracking?

> [!tip] 核心洞察
> 核心洞见在于：通过数据驱动单应性变换将单目检测提升至BEV空间，并在该空间中利用少量但覆盖多模态的生成式轨迹预测，能够有效替代复杂的表观匹配，显著桥接长时遮挡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 轨迹预测是否是长期多目标跟踪的关键？ |
| 英文题名 | Quo Vadis: Is Trajectory Forecasting the Key Towards Long-Term Multi-Object Tracking? |
| 会议/期刊 | NeurIPS 2022 |
| Links | [paper](https://arxiv.org/abs/2210.07681); [GitHub](https://github.com/dendorferpatrick/QuoVadis) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | QuoVadis (基于轨迹预测的长时多目标跟踪方法) |
| Dataset | MOT17 test, MOT20 test |

> [!tip] 效果简介
> - MOT17 test 上，HOTA 为 63.14，对比 63.05 (ByteTrack)，变化 +0.09。
> - MOT17 test 上，IDSW 为 2103，对比 2196 (ByteTrack)，变化 -93。
> - MOT20 test 上，HOTA 为 61.48，对比 61.38 (ByteTrack)，变化 +0.10。

## 概述

多目标跟踪（MOT）的核心挑战之一是长时间遮挡下的身份保持。现有基于表观特征的先进跟踪器在遮挡超过3秒时几乎完全失效——仅能成功关联不到10%的丢失轨迹（Figure 1b）。这一瓶颈的根源在于：仅依赖ReID特征无法应对指数增长的关联搜索空间，而简单的线性运动模型又难以捕捉人类复杂的非线性移动模式。

本文提出 **QuoVadis**，一种基于轨迹预测的长时多目标跟踪方法。其核心洞见是：**在鸟瞰视图（BEV）空间中对丢失轨迹进行多样化且考虑不确定性的长时轨迹预测，能够大幅缩小关联搜索空间，从而有效桥接长时遮挡**。具体而言，方法通过三个关键模块实现这一目标：（1）利用数据驱动单应性估计将单目检测提升至BEV空间；（2）在该空间中使用多模态生成式网络对失联轨迹预测少量但多样化的未来路径；（3）基于预测位置与检测的IoU及BEV距离进行匹配，辅以表观阈值过滤。

在MOT17和MOT20测试集上，QuoVadis以ByteTrack为底层跟踪器，将HOTA分别提升至63.14（+0.09pp）和61.48（+0.10pp），身份切换（IDSW）分别减少93和36。更重要的是，在超过3秒的遮挡场景下，ID召回率从基线的不足10%大幅提升至约60%。消融实验进一步揭示了一个反直觉的发现：**预测损失（FDE/ADE）的最优并非带来最好的跟踪性能；少量多样化且考虑局部不确定性的预测才是关键**——使用仅3个生成器的多模态预测（MG-GAN）在保持高关联精度的同时，获得了比使用20个样本的单一GAN更优的跟踪效果。

本工作确立了轨迹预测作为长时多目标跟踪关键组件的方法定位，表明在BEV空间中的生成式运动推理能够有效替代复杂的表观匹配，为遮挡鲁棒跟踪开辟了新范式。

## 背景与动机

### 问题背景：长期遮挡——多目标跟踪的阿喀琉斯之踵

多目标跟踪（MOT）的核心挑战之一是目标在长时间遮挡后重新出现时的身份关联。在MOTChallenge数据集中，约**19.4%的轨迹会经历超过2秒的遮挡**，而现有最先进的跟踪器在遮挡时长超过3秒时几乎完全失效——**仅能成功关联不到10%的丢失轨迹**（Figure 1b）。这意味着，尽管近年来跟踪器在整体指标上取得了显著进步，但其在长时遮挡场景下的鲁棒性仍然是明显的短板。

### 现有方法的缺口：表观匹配与线性运动的局限

当前主流的跟踪范式主要依赖两类机制来桥接遮挡：

1. **表观特征匹配（ReID）**：通过视觉嵌入向量的相似度进行关联。然而，ReID特征在长时遮挡后往往因视角变化、光照差异和形变而失效；更重要的是，随着遮挡时长增加，需要搜索的候选检测数量呈指数增长，仅靠表观相似度难以在庞大的搜索空间中做出可靠决策。

2. **线性运动模型**：如Kalman滤波，假设目标匀速运动，在图像像素空间中进行位置预测。但人类的运动本质上是非线性的——突然转向、变速、停留等行为使得线性外推在超过数秒的预测跨度上产生显著偏差。此外，在像素空间中预测忽略了场景的三维几何约束，导致预测位置与真实世界的物理运动不一致。

这两类机制的共同缺陷在于：它们无法在长时间跨度上生成**物理合理且覆盖多模态可能**的未来轨迹，从而无法有效缩小关联搜索空间。

### 核心动机：从“被动匹配”到“主动预测”

本文的核心动机源于一个关键观察：**如果能够在三维世界空间中推理目标的未来可能位置，就可以将长时遮挡后的关联问题从“大海捞针”式的表观搜索转化为“按图索骥”式的空间匹配**。具体而言：

- **鸟瞰视图（BEV）空间**提供了场景的几何约束，使得运动预测具有物理一致性；
- **多模态轨迹预测**能够覆盖目标可能的多种未来行为（如直行、左转、右转），而非仅依赖单一的线性外推；
- **少量但多样化的预测样本**足以大幅缩小关联时的搜索空间，从而显著提升长时遮挡下的身份保持能力。

基于这一动机，本文提出**QuoVadis**——一种将轨迹预测引入多目标跟踪的通用框架，通过数据驱动的单应性变换将单目检测提升至BEV空间，并在该空间中对丢失轨迹进行长时预测与匹配，从而系统性地桥接长期遮挡。

## 核心创新

QuoVadis 的核心创新在于将长时多目标跟踪问题重新定义为**轨迹预测驱动的关联问题**，而非传统的表观匹配问题。其关键操作体现在以下三个“changed slots”上：

### 1. 运动推理空间：从像素空间到鸟瞰视图（BEV）空间

现有跟踪器（如 **ByteTrack**（Zhang et al., ECCV 2022）、**CenterTrack**（Zhou et al., ECCV 2020））的运动推理完全在图像像素空间进行，依赖短时线性运动模型或回归来维持跟踪。然而，像素空间中的线性运动无法刻画人类复杂的非线性移动，且缺乏物理尺度一致性。

QuoVadis 通过**数据驱动单应性估计**将单目2D检测提升至3D世界坐标系下的鸟瞰视图（BEV）空间（Figure 3）。具体而言，利用单目深度估计器重建第一帧的3D点云，结合语义分割提取地面像素，估计从图像到BEV平面的单应性矩阵 $H$，使得检测框底部中心点 $p$ 可映射为BEV坐标 $x \propto H \cdot p$。这一变换为后续的轨迹预测提供了物理一致的空间基准。

**证据强度**：消融实验（Table 1）表明，即使在BEV空间中使用简单的Kalman滤波进行线性预测，其跟踪性能（HOTA 54.11）也优于像素空间Kalman预测（HOTA 54.08），且ID丢失显著减少。Figure 4进一步证实，BEV空间中的线性运动预测在端点匹配召回率上全面超越像素空间，尤其在长时遮挡下优势更为明显。

### 2. 遮挡关联策略：从表观匹配到轨迹预测引导的关联

传统跟踪器在目标丢失后，仅依赖表观相似度（ReID特征）和简单运动模型进行关联。当遮挡超过3秒时，表观特征因视角、光照变化而不可靠，且关联搜索空间随丢失时长指数增长，导致现有方法仅能成功关联不到10%的长时遮挡（Figure 1b）。

QuoVadis 将关联策略转变为**基于轨迹预测的几何匹配**。当轨迹进入丢失状态时，在BEV空间中对每条丢失轨迹生成 $k$ 条多样化未来路径（预测长度 $\tau_{\max}$），然后通过融合IoU重叠和BEV L2距离的成本函数与新的检测进行二分图匹配：

$$c_{ij} = \left( \Delta_{\mathrm{IoU}} + \max\left( \tau_{L_2} - \Delta_{L_2}, 0 \right) \right) \cdot \left( \Delta_{\mathrm{App}} \geq \tau_{\mathrm{App}} \text{ and } \Delta_{\mathrm{IoU}} \geq \tau_{\mathrm{IoU}} \right)$$

表观模型在此仅作为**辅助过滤器**（$\tau_{\mathrm{App}}=0.8$），而非主要关联依据。这一设计大幅缩小了关联搜索空间，使表观匹配从“大海捞针”变为“验证候选”。

**证据强度**：在MOT17验证集上，引入轨迹预测后CenterTrack的HOTA从54.52提升至58.08（+3.56pp，Table 3）。Figure 1b显示，QuoVadis对超过3秒遮挡的ID召回率约60%，而基线方法低于10%。

### 3. 场景表示与重建：从无显式几何到BEV地面平面

传统跟踪器缺乏场景几何信息，仅使用2D图像坐标进行关联。QuoVadis通过单应性估计重建3D地面平面，为所有轨迹提供统一的物理空间表示。对于静态摄像头，仅需第一帧估计单应性矩阵并复用于整个序列；对于移动摄像头，则通过光流估计帧间像素对应关系，计算帧依赖的单应性 $H_t$ 和自运动平移向量（Figure 5）。

**证据强度**：该模块是BEV空间运动推理的前提，其有效性间接由BEV vs. 像素空间的消融实验（Table 1, Figure 4）支撑。但单应性估计假设场景为平面地面，对坡道、阶梯等非平面区域鲁棒性不足，这是方法的一个已知局限。

---

**核心洞见总结**：QuoVadis 的核心洞见在于，通过数据驱动单应性变换将检测提升至BEV空间，并在该空间中利用少量但覆盖多模态的生成式轨迹预测，能够有效替代复杂的表观匹配，显著桥接长时遮挡。消融实验（Table 1）揭示了一个反直觉的发现：**预测损失（FDE/ADE）的最优并非带来最好跟踪性能**——使用3个生成器的多模态预测（MG-GAN）在FDE并非最优的情况下获得了最高HOTA（54.52）和AssA（54.80），而移除社会交互模块对跟踪影响甚微。这表明对于跟踪而言，**少量多样化的预测**比精确的轨迹回归或复杂的交互建模更为关键。

## 整体框架

QuoVadis 的核心思路是将长期遮挡下的多目标跟踪重新表述为**鸟瞰视图（BEV）空间中的轨迹预测问题**。其整体流水线由三个松耦合但顺序依赖的模块构成，输入为单目视频帧与现成检测器的 2D 边界框，输出为跨长时遮挡的鲁棒轨迹关联。

### 模块关系与数据流

1. **单应性估计模块（Homography Estimation Module）**  
   利用序列首帧的单目深度估计与语义分割，重建三维地面点云并拟合地面平面，从而以数据驱动方式估计图像像素坐标到 BEV 坐标的单应性矩阵 $H$。对于静态相机，该矩阵在整段序列中复用；对于移动相机，通过光流逐帧估计自运动并更新帧依赖的单应性 $H_t$。检测框的底部中心点 $p$ 经 $x \propto H \cdot p$ 映射至 BEV 位置 $x$，为后续预测提供度量一致的物理空间。

2. **轨迹预测网络（Trajectory Forecasting Network）**  
   当某条轨迹因遮挡或检测丢失而失联时，该轨迹被移入非活跃轨迹集 $S_I$。预测网络以该轨迹在 BEV 空间中的历史位置为输入，生成 $k$ 条长度为 $\tau_{\text{max}}$ 的未来可能路径。网络采用多生成器 GAN（MG-GAN）架构，通过训练多个解码器头来捕获运动的多模态性，仅需少量样本（$k=3$）即可覆盖合理的未来位置分布。

3. **预测匹配与过滤模块（Forecast Matching & Filtering）**  
   对每一帧新检测，将非活跃轨迹的所有预测位置与检测结果进行二分图匹配。匹配成本 $c_{ij}$ 融合 BEV 空间中的 L2 距离和边界框 IoU 重叠度，并通过表观相似度阈值 $\tau_{\text{App}}$ 和 IoU 阈值 $\tau_{\text{IoU}}$ 过滤视觉上不兼容的候选对。同时，利用投影地面掩膜施加可见性约束，剔除被遮挡区域内的不合理预测，防止错误关联。

### 关键设计选择

- **BEV 空间作为运动推理空间**：将运动预测从像素空间提升至 BEV 空间是方法的核心操作。即使在 BEV 中仅使用线性 Kalman 滤波器，其端点匹配召回率也远超像素空间的同类预测（Figure 4），因为 BEV 空间中的运动模式更符合物理规律且不受透视畸变影响。
- **少量多样化预测优于大量单一预测**：实验表明，3 个生成器的多模态预测（MG-GAN）在跟踪性能上优于 20 个样本的单一 GAN（Table 1），说明覆盖运动多模态的多样性比预测精度本身对跟踪更重要。
- **表观模型作为辅助验证**：轨迹预测大幅缩小了关联搜索空间，但引入表观阈值过滤仍能有效抑制错误关联，在实践中提升跟踪鲁棒性（Table 2）。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/001_Figure.jpg]]
*Figure: (a) Illustration of our method. (b) ID recall*

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/002_Figure_2.jpg]]
*Figure 2: Our method: we bridge long-term occlusions by (a) localizing object tracks in BEV via estimated homography and (b) forecasting future trajectories for lost tracks. We (d) continually aim to match these inactive track predictions with new object detections and remove incorrect predictions under a visibility constraint (c)*

## 核心模块与公式推导

### 3.1 数据驱动单应性估计模块

该模块的目标是将单目图像中的2D检测框映射至鸟瞰视图（BEV）空间，为后续轨迹预测提供物理一致的坐标基准。其核心操作是估计一个单应性矩阵 $H$，使得图像齐次坐标 $p$ 与BEV齐次坐标 $x$ 满足：

$$x \propto H \cdot p$$

具体估计流程（见 Figure 3）分为三步：

1. **深度重建**：在合成数据集上训练单目深度估计器，对序列首帧重建3D点云。
2. **地面点筛选**：利用语义分割网络识别地面像素，将地面像素与点云建立对应关系，并拟合地平面。
3. **单应性求解**：通过地面点对应关系解算单应性矩阵 $H$。对于静态相机场景，仅对首帧计算 $H$ 并在全序列复用；对于动态相机场景，逐帧计算 $H_t$，并通过光流估计像素对应关系及3D点集间的平移向量来补偿相机自运动。

为抑制远距离变换的畸变，该模块引入线性化约束：要求相邻像素在BEV中的距离不超过0.2m，即：

$$|| \frac { h _ { 2 1 } \cdot p _ { x } + h _ { 2 2 } \cdot p _ { y } + h _ { 2 3 } } { h _ { 3 1 } \cdot p _ { x } + h _ { 3 2 } \cdot p _ { y } + h _ { 3 3 } } - \frac { h _ { 2 1 } \cdot p _ { x } + h _ { 2 2 } \cdot ( p _ { y } + 1 ) + h _ { 2 3 } } { h _ { 3 1 } \cdot p _ { x } + h _ { 3 2 } \cdot ( p _ { y } + 1 ) + h _ { 3 3 } } || \leq 0.2m$$

这一约束确保BEV空间中的位移量级合理，避免出现不切实际的速度值（见 Figure 6）。

### 3.2 轨迹预测网络

当一条轨迹因遮挡而失联时，该网络在BEV空间中为其生成 $k$ 条长度为 $\tau_{\max}$ 的未来可能路径。网络采用多生成器GAN架构（MG-GAN）：在基础GAN上训练多个解码器头，每个解码器学习聚焦于一种运动模式，从而以少量预测样本覆盖多模态行为。

**关键设计选择**（由 Table 1 消融实验验证）：

- **多模态生成**（3个生成器）优于单模态确定性预测，在保持高关联精度的同时获得最高HOTA（54.52）和AssA（54.80）。
- **多样化预测**比社会交互建模更重要：移除社会交互模块（S-GAN）对跟踪性能影响不大，而使用20个样本的单GAN反而因精度下降导致性能劣于3个生成器的MG-GAN。
- **预测损失最优≠跟踪最优**：FDE/ADE最优的预测器并未带来最佳跟踪性能，少量多样化且考虑局部不确定性的预测才是关键。

### 3.3 预测匹配与过滤模块

该模块负责将失联轨迹的预测位置与新检测进行关联。对于预测 $i$ 与检测 $j$，关联成本定义为：

$$c_{ij} = \left( \Delta_{\mathrm{IoU}} + \max\left( \tau_{L_2} - \Delta_{L_2}, 0 \right) \right) \cdot \left( \Delta_{\mathrm{App}} \geq \tau_{\mathrm{App}} \ \mathrm{and} \ \Delta_{\mathrm{IoU}} \geq \tau_{\mathrm{IoU}} \right)$$

其中：

- $\Delta_{\mathrm{IoU}}$ 为预测框与检测框的交并比距离；
- $\Delta_{L_2}$ 为BEV空间中的L2距离；
- $\tau_{L_2}$ 为L2距离的容忍阈值，超过该阈值的距离差被截断为0；
- $\Delta_{\mathrm{App}}$ 为表观相似度；
- $\tau_{\mathrm{App}}$ 和 $\tau_{\mathrm{IoU}}$ 分别为表观阈值和IoU阈值，作为硬过滤条件：不满足任一阈值的配对成本直接置零。

该成本函数的设计逻辑是：当预测与检测在BEV空间中足够接近时，成本由IoU主导；当距离较远时，L2惩罚生效。表观和IoU阈值则作为安全阀，过滤视觉上不兼容的匹配。消融实验（Table 2）表明，设置 $\tau_{\mathrm{App}}=0.8$ 和 $\tau_{\mathrm{IoU}}=0.2$ 可在恢复约21%丢失轨迹的同时有效抑制错误关联。

此外，模块利用投影的地面掩码（见 Figure 2c）实施可见性约束：若预测位置落入已知的遮挡区域（如建筑物后方），则暂时保留该预测；若预测位置处于可见但无检测对应的区域，则判定为错误预测并予以滤除。

## 实验与分析

### 核心实验设置与公平性说明

QuoVadis 的训练与评测遵循严格的可复现原则。轨迹预测网络**仅在合成数据集 MOTSynth 上训练**，测试时直接泛化至真实 MOT17/MOT20 序列，未使用任何真实数据微调。单应性估计所依赖的深度估计器和语义分割网络均使用第三方预训练模型，所有对比方法在相同检测输入下进行。测试集评测遵循官方“private detector”协议，提交至 MOTChallenge 服务器获得最终分数。

所有基线跟踪器均使用官方开源代码和默认参数，QuoVadis 仅在其基础上添加相同的轨迹预测与匹配模块，确保对比的公平性。

### 主实验结果

#### 长时遮挡关联能力的根本性突破

Figure 1b 揭示了当前跟踪器的核心瓶颈：**现有先进跟踪器仅能成功关联不到 10% 的超过 3 秒的遮挡**。这一发现直接定义了长时多目标跟踪的真正难点——当遮挡时长超过 3 秒，基于表观相似度和线性运动模型的传统关联策略几乎完全失效。QuoVadis 通过在 BEV 空间中进行长时轨迹预测，将超过 3 秒遮挡的 ID 召回率提升至约 60%，实现了约 50 个百分点的飞跃（置信度 0.85）。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/004_Figure.jpg]]
*Figure: (a) Overall recall (BEV and pixel-space). (b) Recall wrt. different occlusion lengths*

#### MOT17/MOT20 测试集表现

在 ByteTrack 基线上叠加 QuoVadis 后，MOT17 test set 的 HOTA 从 63.05 提升至 **63.14**（+0.09pp），IDSW 从 2196 降至 **2103**（减少 93 次）；MOT20 test set 的 HOTA 从 61.38 提升至 **61.48**（+0.10pp），IDSW 减少 36 次（Table 5, Table 6）。虽然 HOTA 的绝对提升看似微小，但需注意：(1) ByteTrack 本身已是当时最强的跟踪器之一，在其基础上进一步提升极为困难；(2) IDSW 的显著减少直接验证了长时遮挡关联能力的改善。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/010_Table_6.jpg]]
*Table 6: Comparison under the "private detector" protocol on MOT20 test set. state-of-the-art in terms of HOTA (63.14). We observe similar trends on MOT20, where we improve over the base tracker ByteTrack [80] by +0.5 in terms of IDF1 and reduce the number of identity switches by 36, similarly establishing a new state-of-the-art (61.48 HOTA)*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/011_Table_5.jpg]]
*Table 5: Comparison under the "private detector" protocol on MOT17 test set*

#### 跨跟踪器的通用性验证

Table 3 展示了 QuoVadis 对 8 个先进跟踪器的改进效果。以 CenterTrack 为基线的 MOT17 验证集上，HOTA 从 54.52 提升至 **58.08**（+3.56pp），提升幅度远超 ByteTrack 上的表现，说明**基础跟踪器越依赖运动模型，QuoVadis 的增益越显著**。所有 8 个跟踪器在添加 QuoVadis 后均获得一致的 HOTA 和 AssA 提升，验证了方法的通用性。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/008_Table_3.jpg]]
*Table 3: We improve tracking results of all top-8 state-of-the-art models (MOT17 validation set and MOT20 training set). Differences to the baseline performance are shown in (·)*

### 关键消融实验

#### BEV 空间 vs. 像素空间预测（Table 1, Figure 4）

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/005_Table_1.jpg]]
*Table 1: Which forecasting modules matter for tracking? Evaluated on MOT17 validation set*

这是 QuoVadis 最关键的消融发现。**即使使用最简单的线性 Kalman 滤波器，在 BEV 空间中预测也比在像素空间预测显著降低了 ID 丢失**，HOTA 从 54.08 提升至 54.11（MOT17-val）。Figure 4 进一步揭示：BEV 空间的线性预测在短时遮挡（<1s）下的端点匹配召回率与像素空间相当，但随着遮挡时长增加，BEV 空间的优势急剧扩大——这是 BEV 空间能够保持物理上合理的匀速直线运动，而像素空间的投影运动受透视效应严重扭曲。

#### 多模态生成预测的独特价值（Table 1, Section 4.2）

Table 1 揭示了反直觉的关键发现：**预测损失（FDE/ADE）的最优并非带来最好的跟踪性能**。使用 3 个生成器的多模态预测（MG-GAN）在仅生成 3 个样本的情况下，获得了最高 HOTA（54.52）和 AssA（54.80），而使用 20 个样本的单一 GAN 虽然 FDE 更低，但跟踪性能反而下降。这表明：少量但覆盖多模态的多样化预测，比大量但模式单一的预测更有利于关联匹配。

移除社会交互模块（S-GAN）对跟踪性能影响不大，进一步证实**多样化预测比交互建模对跟踪更重要**（置信度 0.85）。

#### 匹配阈值的作用（Table 2, Section 4.3）

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of BEV reconstruction for moving camera sequence and egomotion estimation. Table 2: Ablation of matching prediction and effect of different thresholds τ on different tracking metrics*

匹配阶段引入表观阈值 $\tau_{\mathrm{App}}=0.8$ 和 IoU 阈值 $\tau_{\mathrm{IoU}}=0.2$ 取得了最佳平衡：在恢复约 21% 丢失轨迹的同时，有效抑制了错误关联，达到最高 HOTA（54.27）。过高的阈值会拒绝正确的长时关联，过低的阈值则引入噪声匹配——这一平衡点对实际部署至关重要。

### 动态场景与移动相机

Table 4 展示了在 MOT17 验证集动态场景（排除 MOT17-05）上的结果，QuoVadis 在所有 8 个跟踪器上仍保持一致的改进。Figure 5 可视化了移动相机序列的 BEV 重建和自运动估计效果，表明通过逐帧光流估计平移向量的策略在动态场景下仍能维持可用的 BEV 定位精度。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/009_Table_4.jpg]]
*Table 4: Results of top-8 state-of-the-art models on dynamic scenes of the MOT17 validation set excluding MOT17-05. Differences in the baseline performance are shown in (·)*

### 失败模式与局限性

1. **单应性估计误差传播**：轨迹预测模型未显式建模 BEV 定位的不确定性，预测精度受限于单应性变换误差，尤其在远距离或非平面区域（坡道、阶梯）会出现系统性偏差。
2. **时间一致性问题**：单目深度估计器在连续帧间的一致性较弱，可能导致移动场景下的变换抖动，影响长时预测的稳定性。
3. **模块化流水线的效率瓶颈**：整体系统由深度估计、语义分割、光流、轨迹预测、匹配等多个独立模块串联，计算开销较大，且缺乏端到端优化。
4. **类别泛化未知**：实验集中在行人跟踪，对车辆等其他类别及非 MOTChallenge 场景的泛化性尚未验证。

### 开放问题

- 如何设计时间一致的深度估计器以提升单应性变换的稳定性？
- 能否在轨迹预测模型中直接输入 BEV 定位的不确定性（如协方差），使预测更鲁棒？
- 如何设计新的预测评价指标，使其与下游跟踪性能（HOTA/IDSW）更好对齐？
- 是否可能通过端到端学习联合优化深度估计、单应性回归与轨迹预测，以减少模块间误差累积？

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/012_Figure_6.jpg]]
*Figure 6: Demonstration of horizon and linearization threshold for sequence image. Linearization of homography transformation is necessary to prevent enormous distances in the transformed coordinates and unrealistic velocities*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/013_Figure_7.jpg]]
*Figure 7: Demonstration of prediction for MG-GAN in BEV and Kalman filter in pixel space*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2210_07681/figures/003_Figure_3.jpg]]
*Figure 3: We estimate the homography H for a sequence by reconstructing a 3D point cloud using a monocular depth estimator. We obtain ground image-to-point-cloud correspondences using a semantic segmentation model that masks ground pixels as needed to estimate the homography matrix. With the estimated homography matrix, we transform the bottom points of bounding boxes to 2D BEV coordinates*

## 方法谱系与知识库定位

### 1. 核心问题与因果机制

当前多目标跟踪（MOT）的主流范式长期依赖表观特征（ReID）进行关联。然而，**QuoVadis**（NeurIPS 2022）揭示了一个根本性瓶颈：在遮挡时长超过3秒的场景下，现有最先进跟踪器仅能成功关联不到10%的轨迹（Figure 1b）。其因果机制在于，长时间遮挡导致基于表观相似度的关联搜索空间呈指数级膨胀，而传统的线性运动模型（如Kalman滤波）在图像像素空间中对人类复杂的非线性移动几乎无能为力。

本文的核心操作是**将运动推理从图像像素空间提升至鸟瞰视图（BEV）空间**，并在该空间中对丢失轨迹进行多样化且考虑不确定性的长时轨迹预测。这一操作大幅缩小了关联搜索空间，使得即使仅使用简单的L2距离和IoU重叠进行匹配，也能有效桥接长时遮挡。

### 2. 与基线方法的关系

**QuoVadis**并非一个独立的跟踪器，而是一个**即插即用的长时关联模块**，可叠加于任何现有跟踪器之上。论文在8个最先进跟踪器上验证了其通用性（Table 3），包括：

- **ByteTrack**（Zhang et al., ECCV 2022）：作为主要基线及最终测试集评测的底层跟踪器
- **CenterTrack**（Zhou et al., ECCV 2020）：用于验证及BEV重建分析
- **FairMOT**（Zhang et al., IJCV 2021）、**JDE**、**CSTrack**、**TraDes**、**QDTrack**、**TransTrack**：作为对比的先进跟踪器

所有基线均使用官方开源代码和默认参数，仅在其基础上添加相同的轨迹预测与匹配模块，确保对比的公平性。

在方法谱系上，**QuoVadis**与以下工作形成对比：

- **传统运动模型**（如Kalman滤波在像素空间的线性外推）：**QuoVadis**证明，即使使用相同的线性Kalman预测器，仅将预测空间从像素切换至BEV，即可显著降低ID丢失（MOT17-val HOTA从54.08提升至54.11，Table 1）。这揭示了**预测空间的几何合理性比预测器的复杂度更关键**。

- **纯表观关联方法**（如基于ReID的DeepSORT系列）：**QuoVadis**并非替代表观特征，而是将其降级为辅助过滤角色（匹配时引入表观阈值 $\tau_{\mathrm{App}}=0.8$ 和IoU阈值 $\tau_{\mathrm{IoU}}=0.2$），从而在恢复约21%丢失轨迹的同时抑制错误关联（Table 2）。

- **端到端跟踪器**（如CenterTrack、TransTrack）：**QuoVadis**展示了即使在端到端框架上叠加基于预测的关联，仍能带来显著增益（CenterTrack+Ours在MOT17-val静态场景上HOTA从54.52提升至58.08，Table 3）。

### 3. 适用边界与局限

**适用场景**：
- 静态或缓慢移动的监控摄像头下的行人跟踪（MOT17/MOT20验证有效）
- 存在频繁且长时间遮挡的拥挤场景（MOT20上IDSW减少36，Table 6）
- 作为现有跟踪器的后处理增强模块，无需修改原跟踪器结构

**关键局限**（需手动验证部分细节）：

1. **单应性估计的几何假设**：方法假设场景为平面地面，通过数据驱动方式从第一帧估计单应性矩阵 $H$。对于坡道、阶梯、非平面区域，单应性变换会引入系统性误差，尤其在远距离处（Appendix A.1通过线性化条件 $||\dots|| \leq 0.2m$ 缓解畸变，但无法根除）。

2. **深度估计的时间不一致性**：单目深度估计器在不同帧之间可能产生不一致的深度预测，影响移动场景下自运动估计的稳定性。论文通过光流计算帧间像素对应关系来估计相机平移（Section 3.1），但未量化深度不一致性对跟踪性能的影响。

3. **模块化流水线的累积误差**：整体系统由深度估计、语义分割、光流、轨迹预测、匹配等多个独立模块串联而成，缺乏端到端优化。各模块的误差可能逐级放大。

4. **类别泛化性未知**：实验集中在行人跟踪，对车辆、动物等其他类别的有效性未经验证。预测模型仅在合成数据集MOTSynth上训练，虽然展示了向真实MOT场景的零样本泛化能力，但其在其他目标类别或完全动态摄像头场景下的适应性仍是开放问题。

5. **计算开销**：多个独立模块（深度估计器、分割网络、光流、GAN预测器）的推理成本较高，论文未提供实时性分析。

### 4. 开放问题

1. **时间一致的深度估计**：如何设计或微调深度估计器，使其在不同帧之间保持几何一致性，从而提升单应性变换的稳定性？

2. **不确定性感知的轨迹预测**：当前预测模型未显式建模BEV定位的不确定性（如由单应性误差引入的协方差）。能否在预测模型中直接输入定位不确定性，使预测更鲁棒？

3. **预测评价指标与跟踪性能的对齐**：实验揭示了一个反直觉现象——预测损失（FDE/ADE）的最优并不带来最好跟踪性能（Table 1分析，Section 4.2）。少量多样化且考虑局部不确定性的预测才是关键。如何设计新的预测评价指标，使其与下游跟踪性能（HOTA/IDSW）更好对齐？

4. **非行人目标与完全动态场景的泛化**：该方法在车辆跟踪、动物跟踪以及完全由移动摄像头拍摄的场景（如车载视角）下的适应性如何？是否需要重新训练预测模型或调整单应性估计策略？

5. **端到端联合优化的可能性**：是否可能通过端到端学习联合优化深度估计、单应性回归与轨迹预测，以减少模块间误差累积，同时保持对任意底层跟踪器的即插即用特性？

## 原文 PDF

![[paperPDFs/NEURIPS_2022/Quo_Vadis_Is_Trajectory_Forecasting_the_Key_Towards_Long_Term_Multi_Object_Tracking.pdf]]
