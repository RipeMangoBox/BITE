---
title: "MoDebug Core Idea"
status: active
created: 2026-05-16T20:20:17+08:00
updated: 2026-05-20T00:00:00+08:00
hypothesis: "文本条件在预训练动作生成器内部存在可观测的传播瓶颈；针对瓶颈做最小引导能提升动作质量与指令跟随。"
tags:
  - MoDebug
  - core_idea
  - text_condition_propagation
  - guidance
source_papers:
  - "[[paperAnalysis/Motion_Generation/CVPR_2023/2023_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete_Representations|T2M-GPT]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling|MoGenTS]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2025/2025_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with_LLMs|Motion-Agent]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation_and_Editing|SALAD]]"
  - "[[paperAnalysis/Motion_Editing/CVPR_2025/2025_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Prediction|SimMotionEdit]]"
  - "[[paperAnalysis/Motion_Editing/arXiv_2024/2024_Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training_free_Editing|MotionCLR]]"
---

# MoDebug Core Idea

> [!abstract] 核心机制
> MoDebug 不是新的 motion generator，而是一个面向预训练动作生成器的机制调试与引导框架。它追踪文本条件如何进入生成器、如何在层间或步骤间传播、如何影响 motion token / latent / denoising path，并在失真位置做最小干预。

## 一句话问题

复杂文本指令中的方向、顺序、计数、部位、速度、物体交互等约束，经常在最终 motion 中被弱化或错绑。MoDebug 关心的不是先给失败贴标签，而是回答：

```text
这些文本条件在生成器内部哪一步开始失效，
失效是否能被 trace 信号复查，
针对该失效位置做 guidance 是否能改善输出？
```

## 研究对象

MoDebug 把文本条件拆成多粒度单元：

1. 全句 prompt；
2. 动作短语；
3. 属性词，如方向、计数、速度、风格、身体部位；
4. token span；
5. 语义步骤；
6. planner 或 LLM 改写后的子指令。

这些单元统一进入传播链，而不是绑定到某一种标注格式。

## 方法链路

```text
text unit construction
-> perturbation battery
-> trace extraction
-> propagation signature discovery
-> signature-targeted guidance
-> full-motion paired evaluation
```

每个环节的输出都必须带 `role` 与 `limitations`，避免把诊断信号升级成最终评价。

## 可证伪假设

| 假设 | 要验证的问题 | 失败后动作 |
| --- | --- | --- |
| H1 文本可分性 | 关键文本单元在 encoder 或 adapter 输出中是否可区分 | 更换文本单元构造或 prompt packing |
| H2 投影瓶颈 | 可分文本信号进入 condition projection 后是否被压扁 | 检查 normalization、gating 或 adapter |
| H3 传播衰减 | 信号在层间、采样步或重掩码过程中是否变弱 | 对衰减位置设计重加权或 bias |
| H4 错误绑定 | 信号是否影响错误的时间、身体部位或 token 区域 | 引入 body/time aware trace 或 rerank |
| H5 引导有效性 | 针对 signature 的最小干预是否改善输出 | 若无改善，回到 signature 定义而不是扩 baseline |

## 适合的模型家族

MoDebug 优先选择能导出内部传播信号的预训练模型：

| 模型 | 观察接口 | 适合回答的问题 |
| --- | --- | --- |
| T2M-GPT | condition feature、next-token logit、结束 token 概率 | 文本条件是否调制离散 motion token 生成 |
| MotionGPT | encoder-decoder attention、motion-token logit、prompt format sensitivity | 文本和 motion token 共享语言空间时如何传播 |
| Motion-Agent / MotionLLM | planner 子指令、调用路径、motion token translator 输出 | 规划改写是否改善传播链 |
| MoMask | mask confidence、remasking trajectory、candidate confidence | 非自回归 token prior 是否保留局部文本条件 |
| MoGenTS | time-joint token grid、body/time response | 文本条件是否绑定到正确身体部位和时间区域 |

SALAD、MotionCLR、SimMotionEdit 作为 attention、编辑性和局部变化分析参照，不承担主 claim。

## 最小实验闭环

1. 选择能生成 full motion 的 baseline，建立同 prompt、同 seed 或同 candidate pool 的 `B` vs `B+MoDebug` 比较。
2. 为同一批 prompts 构造全句、短语、属性和语义步骤扰动。
3. 在可用模型上记录 `embedding_delta`、`projection_delta`、`hidden_delta`、`logit_delta`、`confidence_delta` 或 `trajectory_delta`。
4. 找到一个跨模型或跨 prompt bucket 复现的 propagation signature。
5. 对该 signature 做一种最小 guidance。
6. 用 full-motion human preference、quality guardrail、geometry / VLM side signal 和 independent scorer 做输出交叉检查。

## 论文贡献形态

MoDebug 可以写成三类贡献：

1. 一个 text-to-motion 生成器内部文本条件传播的诊断协议；
2. 一组可复现的传播失真 signature；
3. 一个 signature-targeted guidance 插件，证明诊断信号能转化成 full-motion 输出改进。

这比继续堆 baseline 更可控，因为每个实验都必须连接到同一条传播链。
