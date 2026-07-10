---
title: "ChinaMM审稿意见 - 面向大规模缺失图像修复的频域结构增强方法"
type: review
venue: ChinaMM
created: 2026-05-12
updated: 2026-05-12
tags:
  - review
  - ChinaMM
  - image_inpainting
---

# ChinaMM审稿意见

## 1. Please confirm that the language used in the review is consistent with the language of the manuscript.

我方确认审稿所用语言与稿件采用的语言完全一致。

## 2. Please provide a summary of the paper.

本文针对大面积缺失内容的图像修复任务，提出了一种改进的 LaMa 框架。作者在网络中嵌入频率可靠性感知 FFC 单元，用于约束不可靠的频域响应；同时设计方向引导的结构传播模块，在解码阶段增强边缘连贯性，并保持细长结构的一致性。论文在 CelebA-HQ 和 Paris Street View 数据集上进行了较充分的实验，结果表明所提方法相较原始 LaMa 模型和其他主流对比方法取得了较明显的性能提升。在缺失比例较高的掩码条件下，性能提升更加突出。

## 3. Please list the major contributions of the paper.

- 论文关注图像修复中大面积缺失场景下的结构恢复问题，研究问题明确且具有实际意义。
- 所提出的两个模块动机较清晰，并且能够较自然地嵌入 LaMa 框架。
- 实验覆盖了两个数据集、多种掩码比例、多种基线方法以及常用评价指标。
- 消融实验表明，FFC-RF 和 DSP 两个模块均对最终性能有贡献。

## 4. Please list the major weaknesses of the paper.

- 论文创新性相对中等。该方法主要是在 LaMa/FFC 基础上的增量式扩展，且没有充分说明其与密切相关工作的区别，尤其是 Chu 等人在 ICCV 2023 发表的 *Rethinking Fast Fourier Convolution in Image Inpainting*。该工作同样分析了 LaMa 式图像修复中 FFC 的局限。建议作者进一步明确 FFC-RF 与 UFFC 的区别，并说明可靠性感知频域调制具体针对哪些失败案例。
- 若干实现细节仍不够清楚，包括频率划分的具体方式、可靠性权重的形状与计算过程、复数频域特征的处理方式、DSP 的传播步长、采样细节，以及各模块具体插入网络的位置。
- 实验设置描述不够充分。建议补充学习率、批大小、训练轮数、损失权重、输入分辨率、数据集划分、掩码生成策略，以及基线模型是重新训练还是使用官方预训练权重等关键信息。
- 论文声称 FFC-RF 能够抑制异常频率成分，DSP 能够改善方向结构连续性，但目前证据主要是间接的。若能补充频域/可靠性可视化、方向场可视化，或针对结构区域的评价指标，将更有助于支撑论文论点。
- 论文没有报告效率指标。由于该方法是在 LaMa 基础上进行修改，建议补充参数量、FLOPs、显存占用和推理时间，并与原始 LaMa 进行比较。
- 高分辨率泛化能力目前主要由少量定性结果支撑，证据仍偏弱。

## 5. Comments and recommendations to the author.

建议作者补充对最接近的频域图像修复工作的讨论，尤其是 Chu 等人的 *Rethinking Fast Fourier Convolution in Image Inpainting*（ICCV 2023）。虽然该论文并非最新工作，但它与本文同处 LaMa/FFC 设计空间，是非常直接的相关工作。除此之外，建议作者增加一个简洁的实现细节表，进一步明确训练设置和基线设置，补充模块可视化和效率指标。关于高分辨率泛化能力的表述，建议要么通过与 LaMa 的定量比较进一步支撑，要么适当弱化相关结论。
