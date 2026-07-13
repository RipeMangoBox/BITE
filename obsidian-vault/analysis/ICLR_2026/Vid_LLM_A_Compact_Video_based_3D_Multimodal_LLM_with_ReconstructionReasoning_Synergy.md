---
title: "Vid-LLM: A Compact Video-based 3D Multimodal LLM with Reconstruction–Reasoning Synergy"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Vid_LLM_A_Compact_Video_based_3D_Multimodal_LLM_with_ReconstructionReasoning_Synergy.pdf
project_link: https://chenhaijier.github.io/Vid-LLM/
code_link: null
openreview_forum_id: l1cLdEjESj
aliases:
- VL
- Vid-LLM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将输入模态从显式3D数据替换为单目视频，并通过内置的3D重建分支从视频中恢复几何信息（位姿、深度、点云），再利用Cross-Task Adapter将几何先验与语义表征对齐，使得大语言模型能够基于视频输入完成3D视觉语言推理。"
primary_logic: "重建与推理本质上是相互依赖的：几何结构支撑语义理解，而语义推理反过来提供上下文先验以指导和优化几何建模。Vid-LLM通过Cross-Task Adapter中的可学习Bridge Tokens实现了几何与语义在特征层面的内在交互与相互增强，从而在单一框架内同时实现高质量的3D重建与多任务视觉语言推理。"
claims:
- "现有3D-MLLM依赖复杂的显式3D数据输入，限制了可扩展性和实际部署。"
- "Vid-LLM仅需视频输入即可完成3D视觉语言推理，无需外部3D数据。"
- "Cross-Task Adapter通过Bridge Tokens实现几何与语义的内在交互与对齐。"
- "重建与推理的协同使Vid-LLM在多个3D VL任务上达到与基于3D数据的方法相当甚至更优的性能。"
---

# Vid-LLM: A Compact Video-based 3D Multimodal LLM with Reconstruction–Reasoning Synergy

> [!tip] 核心洞察
> 重建与推理本质上是相互依赖的：几何结构支撑语义理解，而语义推理反过来提供上下文先验以指导和优化几何建模。Vid-LLM通过Cross-Task Adapter中的可学习Bridge Tokens实现了几何与语义在特征层面的内在交互与相互增强，从而在单一框架内同时实现高质量的3D重建与多任务视觉语言推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Vid-LLM：具备重建-推理协同的紧凑型视频驱动3D多模态大语言模型 |
| 英文题名 | Vid-LLM: A Compact Video-based 3D Multimodal LLM with Reconstruction–Reasoning Synergy |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=l1cLdEjESj) · [Project](https://chenhaijier.github.io/Vid-LLM/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Vid-LLM |
| Dataset | ScanQA (3D Question Answering), SQA3D (3D Question Answering), Scan2Cap (3D Dense Captioning), ScanRefer (3D Visual Grounding) |

> [!tip] 效果简介
> - ScanQA (3D Question Answering) 上，CIDEr↑ 为 101.9，对比 104.8 (3DRS, 基于3D数据的最优方法)，变化 -2.9。
> - SQA3D (3D Question Answering) 上，EM@1↑ 为 57.3，对比 60.6 (3DRS, 基于3D数据的最优方法)，变化 -3.3。
> - Scan2Cap (3D Dense Captioning) 上，CIDEr@0.5↑ 为 81.5，对比 86.1 (3DRS, 基于3D数据的最优方法)，变化 -4.6。

## 概要

现有3D多模态大语言模型（3D-MLLM）普遍依赖点云、深度图、相机位姿等显式三维数据作为输入，这种设计带来了高昂的数据采集与预处理成本，严重制约了模型的可扩展性和实际部署能力。Vid-LLM针对这一瓶颈，提出了以单目视频为唯一输入模态的新范式：模型内置3D重建分支，从视频中端到端恢复相机位姿、深度图与点云等几何信息，再通过Cross-Task Adapter（CTA）将几何先验与语义表征对齐，使大语言模型能够直接基于视频完成3D视觉语言推理。

该方法的核心洞察在于：**重建与推理并非孤立任务，而是相互依赖的**——几何结构为语义理解提供空间支撑，语义推理则反向提供上下文先验以指导几何建模。Vid-LLM通过CTA中的可学习Bridge Tokens，在特征层面实现了几何与语义的双向交互与相互增强，从而在单一框架内同时达成高质量的3D重建与多任务视觉语言推理。

实验表明，尽管Vid-LLM仅使用视频输入（信息量天然少于显式3D数据），其在3D问答、密集描述和视觉定位等多项基准上仍达到与依赖3D数据的最优方法相当甚至更优的性能：ScanQA上CIDEr达101.9（3DRS为104.8），ScanRefer上Acc@0.25达63.2（超越3DRS†的62.9），Nr3D上整体准确率达65.4（超越3D-VisTA的64.2）。在联合框架对比中，Vid-LLM以1.6秒/场景的推理速度显著快于VGGT+LLaVA-3D串联框架的2.7秒/场景，体现了端到端设计的效率优势。



### 3D多模态大语言模型的现状与瓶颈

近年来，3D多模态大语言模型（3D-MLLM）在三维场景理解与交互方面取得了显著进展，能够执行3D问答、密集描述和视觉定位等多种任务。然而，现有方法普遍存在一个根本性瓶颈：**它们无一例外地依赖显式三维数据输入**，包括点云、重建后的场景网格、多视图渲染图像、深度图以及物体级标注等。这种对复杂输入模态的强依赖带来了以下连锁问题：

1. **数据采集成本高**：获取高质量的点云或深度数据需要专业传感器（如LiDAR、RGB-D相机），限制了数据来源的多样性。
2. **预处理流程复杂**：从原始传感器数据到可供模型使用的结构化3D表示，需要经过配准、融合、分割等多步处理，系统复杂度显著增加。
3. **计算开销大**：显式3D表示（尤其是稠密点云）的存储和计算开销远高于2D图像，制约了模型的可扩展性。
4. **实际部署困难**：在真实场景（如移动机器人、AR/VR设备）中，往往只能获取单目视频流，无法保证完整的3D先验数据。

正如论文所指出的，"these methods invariably depend on complex inputs such as point clouds, reconstructed scenes, multi-view renderings, or object-level annotations, which impose substantial burdens on data acquisition, preprocessing, and computation, thereby limiting scalability and transferability"（第2节相关工作）。这一瓶颈使得现有3D-MLLM难以从实验室走向大规模实际应用。

### 核心动机：从显式3D数据到单目视频的范式转变

Vid-LLM的核心动机在于**将输入模态从显式3D数据替换为单目视频**——一种获取成本极低、无处不在的视觉数据形式。这一转变并非简单的输入替换，而是触及了一个更深层的问题：**几何重建与语义推理是否可以相互增强，而非彼此独立？**

传统方案通常将重建与推理视为串行流程：先由独立的重建模块（如VGGT）从视频中恢复几何信息，再将重建结果输入到3D-MLLM中进行语义推理。这种"拼接式"方案存在两个关键缺陷：

- **信息单向流动**：几何信息可以辅助语义推理，但语义上下文无法反向指导和优化几何建模过程。
- **误差累积**：重建阶段的误差会不可逆地传播到推理阶段，缺乏联合优化的纠错机制。

Vid-LLM的出发点是：**重建与推理本质上是相互依赖的**——几何结构为语义理解提供空间锚点，而语义推理反过来提供上下文先验以约束和优化几何估计。例如，识别出"椅子"这一语义类别后，模型可以对椅子区域的深度估计施加更强的几何先验（如平面性、对称性），从而提升重建质量。

### 技术挑战与本文应对

实现上述范式转变面临三个核心技术挑战：

1. **如何从视频中端到端恢复真实尺度几何？** 传统视频深度估计方法通常只能输出相对深度，缺乏真实尺度信息，无法直接支撑精确的3D空间推理。

2. **如何建立几何与语义特征的内在交互？** 简单的特征拼接或单向注入无法实现双向增强，需要设计一种机制使几何流和语义流在特征层面进行动态对齐与互补。

3. **如何在不依赖外部3D标注的前提下，使LLM获得充分的3D空间感知能力？** 视频本身不包含显式的3D坐标，需要将重建分支恢复的几何信息有效转化为LLM可理解的空间表征。

针对这些挑战，Vid-LLM提出了三个关键设计：**Cross-Task Adapter（CTA）** 通过可学习Bridge Tokens实现几何-语义的双向交互与对齐；**Metric Depth Model** 端到端预测真实尺度深度，摆脱对后处理尺度对齐的依赖；**两阶段训练策略** 通过双教师蒸馏和联合优化，使重建与推理在统一框架内协同收敛。



## 核心方法与创新机理

Vid-LLM的核心创新在于将3D多模态大语言模型的输入模态从显式三维数据替换为单目视频，并通过重建-推理协同架构在单一框架内同时实现几何重建与空间语义推理。其关键设计变更体现在以下五个维度。

### 1. 输入模态：从显式3D数据到单目视频

现有3D-MLLM普遍依赖点云、深度图、多视图渲染图像或物体级标注等显式三维数据输入，这些数据的采集与预处理成本高、系统复杂度大，严重限制了模型的可扩展性和实际部署能力。Vid-LLM将输入简化为单目视频帧序列（每场景均匀采样32帧），无需任何外部3D数据，从根本上降低了部署门槛。

### 2. 几何信息来源：内置3D重建分支端到端恢复几何

传统方法依赖外部深度传感器、预计算相机位姿或独立的3D场景重建模块来获取几何信息。Vid-LLM通过内置的3D重建分支，基于Global-Frame Attention骨架从视频中端到端恢复几何：相机头估计内参-外参，DPT头预测相对深度图，Metric Depth Model则通过基于bin的深度估计与自适应bin中心细化，直接输出真实尺度深度。三者配合，使模型无需任何外部几何先验即可获得完整的场景几何表征。

### 3. 几何-语义对齐：Cross-Task Adapter与Bridge Tokens

基线方法通常采用分离的几何编码器与语言编码器，或简单的特征拼接，缺乏深层的跨任务交互。Vid-LLM设计了Cross-Task Adapter（CTA），引入可学习的Bridge Tokens，通过双向多头注意力分别与几何增强特征和语义增强特征交互，动态捕获两者的互补信息。这一机制在特征层面建立了几何与语义的内在交互与相互增强——几何结构支撑语义理解，语义推理反过来为几何建模提供上下文先验。

### 4. 深度尺度：端到端真实尺度深度预测

现有方法多输出相对深度，需通过后处理尺度对齐才能获得真实尺度。Vid-LLM的Metric Depth Model采用鲁棒的度量深度损失函数（包含全局尺度偏置项与自适应加权残差项），端到端预测真实尺度深度，并通过加权最小二乘法将相对深度与度量深度对齐，使重建结果同时具备精细结构细节和尺度一致性。

### 5. 训练策略：两阶段双教师蒸馏

Vid-LLM采用两阶段训练策略。阶段一通过双教师蒸馏（DINO教师提供语义监督，CLIP教师提供视觉-语言对齐，辅以结构一致性损失保持几何与语义特征之间的相对结构关系），使共享编码器和CTA快速习得高质量的几何与语义表征。阶段二联合优化所有模块，但重建损失不反向传播至3D-VL分支，确保CTA作为稳定的几何-语义交互桥梁。这一策略在收敛速度和最终性能上均显著优于单阶段训练或单教师蒸馏方案。

上述五项设计变更共同构成了Vid-LLM的因果机制：输入模态的简化降低了系统复杂度，内置重建分支消除了对外部几何数据的依赖，CTA的Bridge Tokens实现了几何与语义的深层协同，Metric Depth保证了尺度一致性，两阶段训练则确保了多任务联合优化的稳定性。实验表明，尽管Vid-LLM仅使用信息量天然较少的视频输入，其在3D问答、密集描述和视觉定位等任务上仍达到与基于3D数据方法相当甚至更优的性能。



![[assets/figures/papers/iclr26_0009_l1cLdEjESj_Vid-LLM_A_Compact_Video-based_3D_Multimodal_LLM/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of Vid-LLM. From video, a shared DINOv2 encoder produces tokens that are bidirectionally fused by Cross-Task Adapter with learnable Bridge Tokens, yielding geometric and semantic streams. The reconstruction branch predicts camera poses, depth and recovers realscale via a Metric-Bins module, while the 3D-VL branch lifts features into 3D tokens for LLM reasoning*

![[assets/figures/papers/iclr26_0009_l1cLdEjESj_Vid-LLM_A_Compact_Video-based_3D_Multimodal_LLM/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the two-stage training strategy. Stage-1 employs dual-teacher distillation to align geometry and semantics, and Stage-2 jointly optimizes reconstruction and 3D vision–language tasks*

Vid-LLM的整体架构围绕一个核心设计原则展开：**重建与推理在特征层面实现内在交互与相互增强**。如图2所示，系统以单目视频帧序列为唯一输入，通过共享视觉编码器、跨任务适配器、3D重建分支和3D视觉语言分支四个核心模块协同工作，端到端地完成几何重建与多任务空间推理。

### 输入与共享表征

系统从输入视频中均匀采样32帧，经DINOv2-L视觉编码器提取统一的视觉基础token $T_{base} \in \mathbb{R}^{N \times C}$。这一共享表征是后续所有几何与语义处理的唯一信息源头——无需外部深度传感器、预计算相机位姿或显式3D场景模型。

### Cross-Task Adapter：几何-语义交互枢纽

共享token首先通过两个轻量MLP投影头分别映射到几何特定空间和语义特定空间：

$$T_{geom} = \phi_{geom}(T_{base}), \quad T_{lang} = \phi_{lang}(T_{base})$$

Cross-Task Adapter（CTA）的核心创新在于引入一组可学习的**Bridge Tokens** $T_{bridge} \in \mathbb{R}^{K \times C}$（默认K=16），这些token作为几何与语义信息交换的专用潜在空间。Bridge Tokens通过双向注意力机制同时与几何增强特征和语义增强特征交互：

$$T_{bridge}' = \text{Attn}(T_{bridge}, T_{geom}^{fused}, T_{geom}^{fused}) + \text{Attn}(T_{bridge}, T_{lang}^{fused}, T_{lang}^{fused})$$

更新后的Bridge Tokens再分别注入几何分支和语义分支，实现信息的双向流动。这种设计使几何结构信息能够指导语义理解，而语义上下文反过来为几何建模提供先验约束——这正是“重建-推理协同”的机制基础。

### 3D重建分支：从视频恢复真实尺度几何

几何增强特征进入重建分支后，首先经过Global-Frame Attention骨架处理，整合多帧间的空间对应关系。随后分两路输出：

- **相机头**：估计每帧的内参矩阵$K$和相机位姿$(R, t)$
- **DPT深度头**：预测相对深度图$\hat{D}_{rel}$

为获得真实尺度深度，系统额外设计了**Metric Depth Model**，基于自适应bin中心细化策略端到端预测度量深度$\hat{D}_{metric}$。通过加权最小二乘法估计相对深度与度量深度之间的全局缩放因子，将两者对齐后生成兼具精细结构细节和尺度一致性的最终深度图，进而反投影得到真实尺度点云。

### 3D视觉语言分支：2D语义到3D空间的提升

语义增强特征$T_{lang}'$利用重建分支输出的深度、位姿和内参进行3D反投影：

$$P_v(i,j) = \hat{R}^{-1} K^{-1} [i,j,1]^{\top} \hat{D}(i,j) - \hat{R}^{-1} \hat{t}$$

将像素坐标$(i,j)$映射到相机坐标系下的3D点$P_v(i,j)$。随后，3D坐标经位置编码后与语义特征逐元素融合，形成3D Patch Token：

$$T_{3D}(i,j) = T_{lang}'(i,j) + P_v'(i,j)$$

这些同时携带空间位置信息和语义信息的3D token最终送入大语言模型（LLM），与文本指令一起执行3D问答、密集描述和视觉定位等多任务推理。

### 两阶段训练策略

训练分为两个阶段（图3），以平衡几何与语义表征的学习稳定性：

- **阶段1：双教师蒸馏**。几何教师（VGGT）和语义教师（CLIP）分别提供特征监督，配合结构一致性损失$L_{sc}$保持几何与语义特征之间的相对结构关系。蒸馏损失为：

$$L_{distill} = L_{geo}^{feat} + L_{lang}^{feat} + \lambda L_{sc}$$

- **阶段2：联合优化**。端到端训练所有模块，优化目标为：

$$L_{joint} = L_{recon-task} + L_{VL-task} + L_{MD}$$

其中$L_{MD}$为鲁棒的度量深度损失，通过全局尺度偏置项和自适应加权机制抑制系统性偏差和异常深度值的影响。关键设计是：**重建损失不反向传播至3D-VL分支**，确保CTA作为稳定的几何-语义桥梁，避免两任务间的梯度冲突。

### 数据流总结

整个pipeline的数据流可概括为：**视频帧 → 共享DINOv2 token → CTA解耦为几何/语义双流 → 重建分支输出位姿、深度、点云 → 3D-VL分支将语义特征提升为3D token → LLM执行空间推理**。这一设计使Vid-LLM成为首个在单一框架内同时实现高质量3D重建与多任务视觉语言推理的紧凑模型，推理速度达1.6秒/场景，显著快于串联式方案（如VGGT+LLaVA-3D的2.7秒/场景）。



### 共享视觉编码器与特征投影

Vid-LLM 采用 DINOv2-L 作为共享视觉编码器，从输入视频帧序列中提取统一的基础 token 表征 $T_{base} \in \mathbb{R}^{N \times C}$。该编码器包含 24 层 Transformer，隐层维度为 1024，是重建分支与推理分支的唯一视觉前端。

为将共享表征解耦为几何特定和语义特定的特征空间，Vid-LLM 使用两个轻量 MLP 投影头：

$$T_{geom} = \phi_{geom}(T_{base}), \quad T_{lang} = \phi_{lang}(T_{base})$$

其中 $\phi_{geom}$ 和 $\phi_{lang}$ 均为两层全连接网络，扩展因子为 4，激活函数为 GELU。$T_{geom}$ 承载场景的几何结构信息，$T_{lang}$ 承载语义与视觉语言信息，二者作为后续 Cross-Task Adapter 的输入。

### Cross-Task Adapter 与 Bridge Tokens

Cross-Task Adapter（CTA）是 Vid-LLM 实现几何-语义协同的核心机制。其关键设计在于引入一组可学习的 Bridge Tokens $T_{bridge} \in \mathbb{R}^{K \times C}$（默认 $K=16$），作为几何流与语义流之间信息交换的专用隐空间。

Bridge Tokens 的更新过程为：

$$T_{bridge}' = \text{Attn}(T_{bridge}, T_{geom}^{fused}, T_{geom}^{fused}) + \text{Attn}(T_{bridge}, T_{lang}^{fused}, T_{lang}^{fused})$$

其中 $T_{geom}^{fused}$ 和 $T_{lang}^{fused}$ 分别为经自注意力融合后的几何特征与语义特征。Bridge Tokens 通过多头注意力分别与两个特征流交互，动态捕获互补信息并更新自身表征。这种双向交互使几何先验能够指导语义理解，同时语义上下文也能反向约束几何建模，在特征层面建立了内在的几何-语义对齐。

消融实验证实了该设计的必要性：移除 CTA 导致 ScanQA 从 45.7 降至 42.1、Scan2Cap 从 53.2 降至 48.6、ScanRefer 从 48.4 降至 44.2；Bridge Tokens 数量为 16 时在性能与复杂度之间取得最优平衡，4 或 8 个 token 对齐不充分，32 个 token 则边际收益递减。

### 3D 反投影与 Patch Token 融合

3D 视觉语言推理分支的核心操作是将 2D 语义特征提升到 3D 空间。给定估计的旋转矩阵 $\hat{R}$、平移向量 $\hat{t}$、内参矩阵 $K$ 和深度图 $\hat{D}$，每个像素 $(i,j)$ 在相机坐标系下的 3D 坐标为：

$$P_v(i,j) = \hat{R}^{-1} K^{-1} [i,j,1]^{\top} \hat{D}(i,j) - \hat{R}^{-1} \hat{t}$$

该公式将 2D 像素通过针孔相机模型反投影到 3D 空间，其中 $\hat{R}^{-1} K^{-1} [i,j,1]^{\top} \hat{D}(i,j)$ 为带深度的射线方向，$\hat{R}^{-1} \hat{t}$ 为相机中心在世界坐标系下的位置补偿。

随后，3D 位置编码与语义特征通过逐元素相加融合，形成 3D Patch Token：

$$T_{3D}(i,j) = T_{lang}'(i,j) + P_v'(i,j)$$

其中 $P_v'$ 为 $P_v$ 经位置编码映射后的嵌入，$T_{lang}'$ 为经 CTA 增强的语义特征。该融合方式使每个 token 同时携带空间位置信息和语义内容信息，作为 LLM 进行空间推理的输入。

### 训练损失函数

Vid-LLM 采用两阶段训练策略，各阶段损失函数如下。

**阶段一：双教师蒸馏损失**

$$L_{distill} = L_{geo}^{feat} + L_{lang}^{feat} + \lambda L_{sc}$$

其中 $L_{geo}^{feat}$ 为几何特征与 VGGT 教师之间的 L2 损失，$L_{lang}^{feat}$ 为语义特征与 LLaVA-3D 教师之间的余弦相似度损失，$L_{sc}$ 为结构一致性损失，通过学生与教师表征的 Gram 矩阵间 Frobenius 范数保持几何-语义的相对结构关系：

$$L_{sc} = \frac{1}{M^2} \| S_{stu} - S_{tea} \|_F^2, \quad S_{stu} = Z_{stu} Z_{stu}^{\top}$$

**阶段二：联合优化损失**

$$L_{joint} = L_{recon-task} + L_{VL-task} + L_{MD}$$

其中 $L_{recon-task}$ 为 3D 重建任务损失（含相机位姿、深度图等），$L_{VL-task}$ 为 3D 视觉语言任务损失（问答、描述、定位的交叉熵），$L_{MD}$ 为度量深度损失。

**度量深度损失**采用鲁棒的自适应加权设计：

$$L_{MD} = b^2 + \frac{1}{K} \sum_{i=1}^{K} \frac{(e_i - b)^2}{1 + \alpha |e_i - b|}$$

其中 $b$ 为全局尺度偏置项，惩罚系统性偏差；$e_i$ 为第 $i$ 个像素的深度残差；分母 $1 + \alpha |e_i - b|$ 对大残差进行自适应降权，$\alpha$ 控制鲁棒性强度。该损失使 Vid-LLM 能够端到端预测真实尺度深度，无需后处理尺度对齐。



## 实验与关键发现

### 核心实验设定

Vid-LLM采用DINOv2-L作为共享视觉骨干（24层Transformer，隐藏维度1024），投影MLP使用两层全连接层（扩展因子4，GELU激活）。每场景均匀采样32帧，短边缩放至518像素，裁剪至14的倍数分辨率。训练采用两阶段策略：阶段1进行双教师蒸馏（VGGT作为几何教师，LLaVA-3D作为语义教师），阶段2联合优化重建、视觉语言和度量深度损失。重建分支的梯度不反向传播至3D-VL分支，保持Cross-Task Adapter（CTA）作为几何-语义交互的稳定桥梁。

### 3D问答任务

**Table 1**展示了ScanQA和SQA3D上的3D问答结果。Vid-LLM在ScanQA上取得CIDEr 101.9，仅次于基于3D数据的最优方法3DRS（104.8），在视频驱动方法中排名第一，较3DRS†（同样使用VGGT几何信息）平均领先11%。在SQA3D上，Vid-LLM的EM@1达到57.3，与3DRS（60.6）的差距仅为3.3个百分点。值得注意的是，Vid-LLM仅依赖视频输入，而3DRS需要完整的点云和相机位姿，这一性能差距在输入信息量天然不对等的前提下显得尤为突出。


![[assets/figures/papers/iclr26_0009_l1cLdEjESj_Vid-LLM_A_Compact_Video-based_3D_Multimodal_LLM/figures/004_Table_1.jpg]]
*Table 1: Evaluation of 3D Question Answering on ScanQA and SQA3D. Methods marked with * are 3D MLLM evaluated in video mode. † indicates the model consumes VGGT-generated 3D geometry. ”C” stands for ”CIDEr”, ”B-4” for ”BLEU-4”, ”M” for ”METEOR”, ”R” for ”ROUGE”, and ”EM@1” for top-1 exact match*

### 3D密集描述任务

**Table 2**报告了Scan2Cap上的密集描述结果。Vid-LLM的CIDEr@0.5达到81.5，在视频驱动方法中表现最优。其M@0.5得分（28.7）与基于3D数据的最优模型（29.0）几乎持平，表明从视频恢复的几何信息足以支撑精细的物体级空间描述。3DRS仍以CIDEr@0.5 86.1保持整体领先，但Vid-LLM在B-4@0.5和M@0.5上与其他3D-based方法互有胜负。

### 3D视觉定位任务

**Table 3**和**Table 4**分别报告了ScanRefer/Multi3DRefer和Nr3D/Sr3D上的视觉定位结果。Vid-LLM在ScanRefer上Acc@0.25达到63.2，超过此前最优的视频驱动方法3DRS†（62.9）；在Multi3DRefer上Acc@0.25为61.6，同样领先3DRS†（60.4）。在Nr3D上，Vid-LLM的整体准确率65.4超越此前最优的3D-VisTA（64.2），在Hard子集（57.9）和View Dep子集（61.9）上也保持优势。Sr3D上整体准确率77.8，略胜SceneVerse（77.5）。这些结果表明，CTA实现的内在几何-语义对齐在需要精确空间推理的定位任务中发挥了关键作用。


![[assets/figures/papers/iclr26_0009_l1cLdEjESj_Vid-LLM_A_Compact_Video-based_3D_Multimodal_LLM/figures/006_Table_3.jpg]]
*Table 3: Evaluation of 3D Visual Grounding on ScanRefer and Multi3DRefer*

![[assets/figures/papers/iclr26_0009_l1cLdEjESj_Vid-LLM_A_Compact_Video-based_3D_Multimodal_LLM/figures/008_Table_4.jpg]]
*Table 4: Evaluation of 3D Visual Grounding on Nr3D and Sr3D. Results are reported in grounding accuracy (%)*

### 联合重建-推理框架对比

**Table 5**将Vid-LLM与串联框架（VGGT+LLaVA-3D）和端到端联合框架（Uni3DR、VGLMM-Rec）进行综合对比。Vid-LLM在ScanQA（45.7）、Scan2Cap（53.2）、ScanRefer（59.8）三项VL任务上全面领先，同时保持有竞争力的重建质量（ScanNet F-score 0.582）。更关键的是，Vid-LLM的推理速度仅为1.6秒/场景，显著快于串联框架的2.7秒/场景，体现了端到端设计在消除冗余计算方面的效率优势。

### 消融实验

**Table 6**系统消融了CTA和Metric Depth模块的贡献：


![[assets/figures/papers/iclr26_0009_l1cLdEjESj_Vid-LLM_A_Compact_Video-based_3D_Multimodal_LLM/figures/010_Table_6.jpg]]
*Table 6: Ablation on Cross-Task Adapter (CTA) and Metric Depth (MD) Modules*

- **移除CTA（w/o CTA）**：ScanQA降至42.1，Scan2Cap降至48.6，ScanRefer降至44.2，降幅分别达7.9%、8.6%和8.7%，证实几何-语义对齐对下游VL任务至关重要。
- **Bridge Tokens数量**：16个token在性能和复杂度间取得最佳平衡。4/8 token时对齐不充分（ScanQA 43.8/44.5），32 token时边际收益递减（45.3），均不如16 token的45.7。
- **Bridge机制设计**：简单拼接后自注意力（Concat-SA，ScanQA 43.1）或移除Bridge仅用交叉注意力（w/o Bridge，42.9）均显著弱于完整CTA方案，验证了Bridge Tokens作为专用潜在空间对跨任务交互的必要性。
- **Metric Depth贡献**：移除Metric Depth（w/o MD）导致VL性能下降（ScanQA 44.8）且重建F-score降至0.568；仅保留对齐步骤（w/o Alignment）同样造成性能损失（F-score 0.574）。这表明真实尺度几何信息同时服务于高质量重建和精确空间推理。

**Figure 5**展示了不同训练策略的收敛曲线。完整两阶段策略（双教师蒸馏+结构一致性损失）的测试损失最低且收敛最快；单阶段训练收敛缓慢且稳定在高损失水平；移除结构一致性损失会显著拖慢收敛速度并降低最终精度。这验证了阶段1的几何-语义对齐为阶段2的联合优化提供了关键的初始化基础。

### 失败模式分析

**Figure 7**展示了三个典型失败案例，揭示了当前框架的核心局限：

1. **有限视角导致几何不完整**：输入视频未能覆盖场景所有区域时（如部分遮挡的椅子），重建中缺失该物体，导致问答中的物体计数错误。这是视频驱动方法的内在约束——模型只能推理所见之物。
2. **反光表面破坏深度估计**：高度反光表面（如玻璃桌面）导致深度估计不稳定，重建几何质量下降，使得3D边界框预测偏小。这暴露了纯视觉几何重建在非朗伯表面上的固有问题。
3. **极端视角下的重建退化**：仅短暂出现或从极端斜视角观察的物体表面（如柜顶）重建质量较差。虽然2D语义线索可以补偿获得准确的文本描述，但定位精度受到直接制约。

这些失败模式共同指向一个核心瓶颈：**重建分支的几何忠实度直接决定下游VL任务性能的上限**，改善重建质量是进一步提升整体性能的关键方向。

### 补充重建实验

附录中的**Table 7-9**验证了Vid-LLM重建分支的独立性能：

- **相机位姿估计**（Table 7）：在Co3Dv2上RTA@15达到93.4，与VGGT（93.3）持平；RealEstate10K上mAA(30)为83.1，接近VGGT（83.8）。
- **深度估计**（Table 8）：在NYU Depth v2上log10误差0.010，优于VGGT†（0.011）和VCoT†（0.011）。注意VGGT†和VCoT†输出相对尺度需后处理对齐到真值尺度，而Vid-LLM端到端预测真实尺度，在此设定下仍取得更优精度。
- **点云重建**（Table 9）：ScanNet上F-score 0.582，略优于VGGT†（0.580），验证了Metric Depth Model和尺度对齐策略的有效性。

这些结果表明，Vid-LLM的重建分支在独立评估中已达到甚至超越专用重建方法VGGT的水平，为下游VL任务提供了可靠的几何基础。



## 定位与知识库关联

### 与现有方法的谱系关系

Vid-LLM 立足于两个交叉领域的前沿：**视频驱动的3D重建**与**3D多模态大语言模型（3D-MLLM）**。现有3D-MLLM——包括3DRS、LLaVA-3D、ChatScene、LEO、Video-3D LLM、Grounded3D-LLM等——普遍依赖点云、多视图渲染图像、深度图或物体级标注等显式3D数据作为输入。这一依赖导致数据采集与预处理成本高昂、系统复杂度大，严重限制了模型的可扩展性和实际部署能力。Vid-LLM 的关键突破在于**将输入模态从显式3D数据替换为单目视频**：每场景均匀采样32帧，无需任何外部3D数据即可完成3D视觉语言推理，使模型具备面向真实世界部署的实用性。

在几何信息来源方面，Vid-LLM 与 VGGT 构成直接的谱系关系。VGGT 作为视频驱动的3D重建SOTA方法，其几何编码器被 VGLLM 等视频基3D-MLLM所沿用。Vid-LLM 继承了这一技术路线，但将几何重建**内化**为框架的一个有机分支：通过 Global-Frame Attention 骨架配合相机头与 DPT 深度头，端到端地从视频恢复位姿、深度和点云，而非依赖外部预计算模块。更重要的是，Vid-LLM 引入了 **Metric Depth Model**，基于自适应bin中心细化的深度估计策略，使模型输出真实尺度深度，避免了VGGT等方法的相对深度需后处理尺度对齐的缺陷。

Vid-LLM 与 LLaVA-3D 的关系体现在**语义教师**角色上：LLaVA-3D 作为基于多视图渲染特征的3D-MLLM，在阶段1训练中充当语义蒸馏教师，与几何教师VGGT共同指导共享编码器和Cross-Task Adapter的学习。

### 适用边界

Vid-LLM 的设计基于**静态场景假设**，当前框架未明确处理动态物体或非刚性运动。模型主要在室内场景（ScanNet、NYU Depth v2）上评估，其在室外大规模环境（如城市街道、自然景观）中的泛化能力尚未得到验证。此外，模型性能与输入视频的视角覆盖度高度相关：当视频未能覆盖场景所有区域时，几何重建会出现缺失，进而影响下游任务的准确性。

### 因果机制与瓶颈分析

Vid-LLM 的核心因果机制在于**重建与推理的相互依赖与协同增强**：几何结构支撑语义理解，而语义推理反过来提供上下文先验以指导和优化几何建模。这一机制通过 **Cross-Task Adapter（CTA）** 中的可学习 Bridge Tokens 实现——Bridge Tokens 通过双向注意力同时与几何特征和语义特征交互，在特征层面建立内在的几何-语义对齐。消融实验提供了决定性证据：移除CTA（w/o CTA）导致 ScanQA 从45.7降至42.1、Scan2Cap 从53.2降至48.6、ScanRefer 从48.4降至44.2，证明 CTA 对几何-语义对齐至关重要。

该因果链条的薄弱环节在于**重建分支的几何忠实度直接影响下游VL任务性能**。当输入视频存在有限视角、高度反光表面（如玻璃桌面）或极端斜视角（如柜顶）时，深度估计不稳定，重建几何质量下降，导致3D边界框预测偏差或物体计数错误。改善重建质量是进一步提升整体性能的关键方向。

### 局限与开放问题

**已知局限**：
- **视角不完整性**：有限相机视角导致几何重建缺失未覆盖区域的物体，影响问答中的物体计数和定位精度。
- **材质敏感性**：高度反光表面导致深度估计不稳定，重建几何质量下降，使3D边界框预测偏小。
- **斜视角退化**：仅短暂出现或从极端斜视角观察的物体表面重建质量较差，虽可利用2D语义线索补偿描述准确性，但定位精度受到制约。
- **静态场景约束**：当前框架基于静态场景假设，未处理动态物体或非刚性运动。

**开放问题**：
- 如何将 Vid-LLM 扩展到包含动态物体和人物交互的视频场景中，在不依赖3D标注的前提下保持几何-语义的一致性？
- 当前框架主要在室内场景上评估，其在室外大规模环境中的泛化能力如何？
- Bridge Tokens 机制是否可推广到其他跨模态对齐任务（如音频-视觉、触觉-视觉），其通用性边界在哪里？
- 能否在推理阶段引入**主动视角选择策略**——根据当前几何不确定性或语义歧义动态决定下一帧的观测角度？
- 如何在一个统一框架内同时支持几何重建和基于物理的渲染/重光照，使3D VL推理具有更强的交互性和可解释性？



## 原文 PDF

![[paperPDFs/ICLR_2026/Vid_LLM_A_Compact_Video_based_3D_Multimodal_LLM_with_ReconstructionReasoning_Synergy.pdf]]
