---
title: "AnyLift: Lifting Unseen In-the-Wild Human Motions via Camera-Aware 2D Diffusion"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/AnyLift_Lifting_Unseen_In-the-Wild_Human_Motions_via_Camera-Aware_2D_Diffusion.pdf
project_link: null
code_link: null
aliases:
- AnyLift
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: Mock causal knob.
primary_logic: Mock core insight.
claims:
- Mock evidence.
- Mock core insight.
---

# AnyLift: Lifting Unseen In-the-Wild Human Motions via Camera-Aware 2D Diffusion

> [!tip] 核心洞察
> Mock core insight.

| 字段 | 内容 |
|------|------|
| 中文题名 | 模拟论文 |
| 英文题名 | AnyLift: Lifting Unseen In-the-Wild Human Motions via Camera-Aware 2D Diffusion |
| 会议/期刊 | arXiv 2026 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MockMethod |
| Dataset |  |

## 概述

待人工补充。

## 背景与动机

待人工补充。

## 核心创新

待人工补充。

## 整体框架

待人工补充。

### 补充图表

![[assets/figures/papers/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion_da04afb8c963/figures/001_Figure_1.jpg]]
*Figure 1: Human and human-object interaction (HOI) motions lifted by our approach. Trained on 2D keypoints and corresponding camera trajectories, our framework AnyLift reconstructs world-coordinated 3D human motion and HOI from monocular videos captured by dynamic cameras. We demonstrate its effectiveness on human motion reconstruction from Internet gymnastics videos (left) and on HOI reconstruction from captured real-world videos (right). Please refer to our project page for video results*

![[assets/figures/papers/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion_da04afb8c963/figures/002_Figure_2.jpg]]
*Figure 2: Overview of AnyLift. (a) We first train a single-view 2D motion diffusion model conditioned on camera trajectories and epipolar lines to synthesize multi-view 2D training data. (b) During training, we employ a hybrid data source strategy that enhances viewpoint coverage by combining global 2D pose sequences from videos with locally reprojected poses. (c) Finally, we train a multi-view 2D motion diffusion model to reconstruct consistent world-coordinated 3D human and HOI motions from real-world videos*

## 核心模块与公式推导

待人工补充。

## 实验与分析

待人工补充。

### 补充图表

![[assets/figures/papers/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion_da04afb8c963/figures/010_Figure_S.1.jpg]]
*Figure S.1: Facing direction distributions of estimated humans in the gymnastics (upper) and martial arts (lower) videos under the camera coordinate system. The angular axis indicates the facing direction and the radial axis represents number of frames*

![[assets/figures/papers/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion_da04afb8c963/figures/003_Table_2.jpg]]
*Table 2: Quantitative evaluation on our collected Internet videos. AnyLift outperforms all baselines across most metrics, demonstrating the plausibility of our method on Internet videos*

![[assets/figures/papers/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion_da04afb8c963/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on the AIST++ dataset [19] under (1) static-camera setup (upper) and (2) dynamic-camera setup (lower). AnyLift achieves competitive 3D joint accuracy and improved root translation estimation while maintaining robustness under dynamic camera*

![[assets/figures/papers/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion_da04afb8c963/figures/005_Table_3.jpg]]
*Table 3: Human study on reconstructed human motions from our collected Internet videos. Participants prefer our reconstruction results for their better ground contact and motion quality*

![[assets/figures/papers/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion_da04afb8c963/figures/008_Table_4.jpg]]
*Table 4: Quantitative evaluation on the BEHAVE dataset [1] under (1) static-camera setup (upper) and (2) dynamic-camera setup (lower). AnyLift outperforms all baselines across object categories and achieves robust performance under dynamic-camera conditions*

![[assets/figures/papers/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion_da04afb8c963/figures/009_Table_5.jpg]]
*Table 5: Ablation study on our collected Internet videos. Performance drops across all metrics without incorporating local 2D poses from diverse viewpoints*

![[assets/figures/papers/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion_da04afb8c963/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative comparison of human motion reconstruction on our collected Internet videos. AnyLift produces more plausible motions, mitigating the root trajectory errors, inaccurate local body pose, and self-penetration artifacts observed in baselines*

![[assets/figures/papers/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion_da04afb8c963/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of HOI reconstruction on the BEHAVE [1] dataset. We show results on two object categories, chair and table. AnyLift produces coherent and physically plausible human-object interactions with accurate contact and minimal penetration*

## 方法谱系与知识库定位

待人工补充。

## 原文 PDF

![[paperPDFs/arxiv_2026/AnyLift_Lifting_Unseen_In-the-Wild_Human_Motions_via_Camera-Aware_2D_Diffusion.pdf]]