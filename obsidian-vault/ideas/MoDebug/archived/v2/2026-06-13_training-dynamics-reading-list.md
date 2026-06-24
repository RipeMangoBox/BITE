---
title: "MoDebug 推荐阅读：MoLingo CFG Residual + Training Dynamics"
created: 2026-06-09T17:00:00+08:00
updated: 2026-06-13T16:11:58+08:00
status: reference
tags:
  - reading_list
  - cfg_guidance
  - modebug
  - molingo
  - spatial_temporal_training
hypothesis: "2026-06-13 二次复评后，当前 P0 从无目标 atlas 转为目标驱动的 layer-step-token-part guidance modulation。两周内优先服务 T1 时间区间控制和 T2 身体部件控制；MoLingo 本体列为 S0；CFG / flow 工作列为 S1 机制库；motion attention / temporal control / part guidance 列为 S2 可控生成机制库；fine-grained retrieval 列为 S3 评估库。"
---

# MoDebug 推荐阅读：MoLingo CFG Residual + Training Dynamics

> [!abstract] 更新说明
> 本文件替代旧的 `2026-06-09_training-dynamics-reading-list.md`。2026-06-13 二次复评后，阅读优先级改为：S0 精读 MoLingo 本体；S1 精读 CFG / flow 机制库；S2 精读 motion attention、temporal control、part guidance 机制库；S3 选读 fine-grained retrieval、motion attribution 和 STGT 旧线。跨域工作不是简单压缩 novelty，而是 MoDebug 做 motion-specific adaptation 的主要机制来源；当前阅读应优先服务 T1 时间区间控制和 T2 身体部件控制，而不是无目标扩展 atlas。

---

## S0：分析目标

链接：[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation|MoLingo]]。

| 论文 | 必读原因 | 需要关注 |
|---|---|---|
| MoLingo | 当前所有实验的被分析模型；如果不精通其 SAE、multi-token cross-attention、rectified flow、CFG 采样细节，任何 L15 解释都会漂浮 | `forward_z`、`forward_with_cfg`、cross-attention 注入、T5 token 使用、SAE/VAE 差异、official evaluator protocol |

阅读任务：

1. 精读架构与 CFG 采样细节。
2. 明确 `CFG_CA` 的层结构、文本 token 与 motion latent 的交互位置。
3. 对照 MoDebug hook 是否真的作用于 MoLingo 论文中最关键的条件注入位置。

---

## S1：CFG / Flow 机制适配库

链接：[[analysis/ICLR_2025/CFG_Manifold_constrained_Classifier_Free_Guidance_for_Diffusion_Models|CFG++]]、[[analysis/ICLR_2025/Eliminating_Oversaturation_and_Artifacts_of_High_Guidance_Scales_in_Diffusion_Models|APG]]、[[analysis/CVPR_2025/TCFG_Tangential_Damping_Classifier_free_Guidance|TCFG]]、[[analysis/CVPR_2026/C2FG_Control_Classifier_Free_Guidance_via_Score_Discrepancy_Analysis|C2FG]]、[[analysis/CVPR_2026/CFG_Ctrl_Control_Based_Classifier_Free_Diffusion_Guidance|CFG-Ctrl]]、[[analysis/arxiv_2025/CFG_Zero_Improved_Classifier_Free_Guidance_for_Flow_Matching_Models|CFG-Zero*]]、[[analysis/CVPR_2026/FlowMotion_Training_Free_Flow_Guidance_for_Video_Motion_Transfer|FlowMotion]]。

| 论文 | 核心机制 | MoDebug 适配任务 |
|---|---|---|
| CFG++ | 条件插值、无条件重噪声、流形约束 | 检查 fixed-scale substitution 是否本质上是避免过度外推；在 motion latent / velocity prediction 空间做插值式替换。 |
| APG | parallel / orthogonal 分量分解、rescale、reverse momentum | 旧 hidden APG 失败后，改在 velocity、denoised latent、layer residual 三个空间比较方向分量。 |
| TCFG | cond/uncond 法向对齐、切向不对齐、SVD 阻尼 | 用 L10-L15 × step 的谱分析定位 L14/L15 是否出现切向漂移，再决定是否阻尼。 |
| C2FG | score discrepancy 的时间依赖规律 | 把 MoDebug 从层级 alpha 扩展到 layer-specific step schedule。 |
| CFG-Ctrl | 语义误差 `e(t)` 与 `e_dot(t)` 的反馈控制 | 只在 L15 有振荡证据时尝试 damping/control，不预设控制律一定有效。 |
| CFG-Zero* | Flow Matching 速度尺度校正、early-step zero-init | 检查 MoLingo rectified flow 的 early step 或特定 layer 是否需要无条件速度尺度校正。 |
| FlowMotion | 输出端 `z0_hat` / latent prediction 作为 motion representation | 用 `z0_hat` 做 probe 和正则，验证内部 hook 发现是否真正投影到运动空间。 |

阅读任务：

1. 每篇整理一个可落地 adaptation slot：作用空间、调度变量、最小 hook、Go/Stop。
2. 每篇整理一个 motion-specific gap：为什么图像/video 方法不能直接解决 text-to-motion 的 layer/step/token/part 分工。
3. 不得把 MoDebug 写成比这些工作更通用的 CFG 方法；创新应来自 motion 适配和跨 baseline 验证。

---

## S2：Motion 可控生成机制库

### S2-A Attention / Weak Branch

链接：[[analysis/ECCV_2024/Self_Rectifying_Diffusion_Sampling_with_Perturbed_Attention_Guidance|PAG]]、[[analysis/NEURIPS_2024/Smoothed_Energy_Guidance_Guiding_Diffusion_Models_with_Reduced_Energy_Curvature_of_Attention|SEG]]、[[analysis/NEURIPS_2024/Guiding_a_Diffusion_Model_with_a_Bad_Version_of_Itself|Autoguidance]]、[[analysis/CVPR_2026/Self_Swap_Guidance_Guiding_a_Diffusion_Model_by_Swapping_Its_Tokens|Self-Swap Guidance]]、[[analysis/ICLR_2025/No_Training_No_Problem_Rethinking_Classifier_Free_Guidance_for_Diffusion_Models|No Training, No Problem]]。

| 论文 | 读它的目的 | 对 MoDebug 的启发 |
|---|---|---|
| PAG | attention perturbation 构造结构退化负例 | 如果要重启 negative branch，不能只做 `replace`，应有可控退化强度。 |
| SEG | attention smoothing / energy curvature | 可启发 attention entropy 与平滑探针。 |
| Autoguidance | 用坏版本模型作为负分支 | 帮助理解 weak branch 与 quality gap。 |
| Self-Swap | token-level perturbation 比全局噪声更可控 | 比 APG/norm clamp 更接近 token-level MoLingo 探针。 |
| No Training, No Problem | 不训练无条件分支也可构造 guidance 信号 | 如果 MoLingo uncond branch 不可靠，可考虑替代 branch 设定。 |

### S2-B Token-Time-Part Control in Motion / Video

链接：[[analysis/CVPR_2024/Rethinking_the_Spatial_Inconsistency_in_Classifier_Free_Diffusion_Guidance|S-CFG]]、[[analysis/arxiv_2024/Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training_free_Editing|MotionCLR]]、[[analysis/CVPR_2026/TempoControl_Temporal_Attention_Guidance_for_Text_to_Video_Models|TempoControl]]、[[analysis/CVPR_2026/ParTY_Part_Guidance_for_Expressive_Text_to_Motion_Synthesis|ParTY]]、[[analysis/AAAI_2025/ReMoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]、[[analysis/ICML_2024/HumanTOMATO_Text_Aligned_Whole_Body_Motion_Generation|HumanTOMATO]]、[[analysis/CVPR_2024/MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]。

| 论文 | 读它的目的 | MoDebug 适配任务 |
|---|---|---|
| S-CFG | region-level adaptive CFG via attention maps | 把图像 region 映射到 motion part/time span/token phrase，做局部 guidance。 |
| MotionCLR | motion-domain attention map manipulation | 建 token-time attention atlas，并尝试动作强调、替换、时序移动的 MoLingo 版本。 |
| TempoControl | temporal attention signal 可作为推理时控制接口 | 对关键动词做 Pearson / magnitude / entropy 式时间注意力控制。 |
| ParTY | part guidance 兼顾部件对齐与全身协调 | 设计 arms/legs/root/torso part-aware metric 和轻量 part-specific scaling。 |
| ReMoGPT | part-level retrieval 与 6-part ontology | 可作为 body-part 分组参考。 |
| HumanTOMATO | whole-body text-motion alignment | 提醒全局 Matching 不足以证明局部语义修复。 |
| MoMask | RVQ / masked motion token backbone | STGT 与 token-level motion 表征背景。 |

---

## S3：评估、归因与 STGT 旧线

### S3-A Fine-grained Motion-Language Evaluation

链接：[[analysis/arxiv_2026/MaxSim_Fine_grained_Motion_Retrieval_via_Joint_Angle_Motion_Images_and_Token_Patch_Late_Interaction|MaxSim]]、[[analysis/arxiv_2026/Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval_via_Pyramidal_Shapley_Taylor_Learning|PST]]、[[analysis/arxiv_2026/MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval|MoCHA]]。

| 论文 | 可借鉴点 | 用法 |
|---|---|---|
| MaxSim | token-patch late interaction；词元到关节/时间 patch 的显式对齐 | 用于设计 per-token / per-joint 诊断。 |
| PST | joint / segment / holistic 三层对齐 | 用于判断 fixed-scale substitution 是否只改善全局指标。 |
| MoCHA | caption noise 会影响 retrieval 指标 | 用于解释 R-Precision / Matching 波动，不把小差异过度解读。 |

### S3-B Cross-domain Diagnostics

链接：[[analysis/ICML_2026/Motion_Attribution_for_Video_Generation|Motion Attribution]]、[[analysis/CVPR_2026/Improving_Motion_in_Image_to_Video_Models_via_Adaptive_Low_Pass_Guidance|ALG]]、[[analysis/CVPR_2026/Attention_Surgery_An_Efficient_Recipe_to_Linearize_Your_Video_Diffusion_Transformer|Attention Surgery]]。

| 论文 | 可借鉴点 | 用法 |
|---|---|---|
| Motion Attribution | motion-aware gradient mask 与训练样本归因 | 未来可定位哪些动作类型受 L15 intervention 影响。 |
| ALG | early/late condition exposure 调度 | 类比 late-layer signal exposure，但只能作为启发。 |
| Attention Surgery | 少量全局 attention token 可维持时空一致性 | 启发检查 L15 是否承担全局锚点作用。 |

### S3-C STGT 旧线保留阅读

链接：[[analysis/TOG_2022/DeepPhase_periodic_autoencoders_for_learning_motion_phase_manifolds|DeepPhase]]、[[analysis/CVPR_2024/TokenHMR_Advancing_Human_Mesh_Recovery_with_a_Tokenized_Pose_Representation|TokenHMR]]、[[analysis/CVPR_2024/MMM_Generative_Masked_Motion_Model|MMM]]、[[analysis/CVPR_2023/T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete_Representations|T2M-GPT]]、[[analysis/SIGGRAPH_2024/WalkTheDog_Cross_Morphology_Motion_Alignment_via_Phase_Manifolds|WalkTheDog]]。

| 论文 | 保留原因 | 当前状态 |
|---|---|---|
| DeepPhase | phase manifold 与 temporal boundary | STGT 参考，不占 MoLingo P0。 |
| TokenHMR | tokenized pose 与 adaptive loss | STGT spatial weighting 参考。 |
| MMM | masked motion model | token prediction 背景。 |
| T2M-GPT | discrete motion token 基础 | tokenization 背景。 |
| WalkTheDog | phase manifold 跨形态对齐 | 远期 spatial-temporal decomposition。 |

---

## 当前阅读顺序

如果只服务 MoLingo P0：

1. MoLingo
2. FlowMotion
3. CFG++
4. C2FG
5. APG
6. TCFG
7. CFG-Zero*
8. CFG-Ctrl
9. MotionCLR
10. TempoControl
11. S-CFG
12. ParTY
13. MaxSim / PST / MoCHA

如果服务 STGT 旧线：

1. MoMask
2. TokenHMR
3. DeepPhase
4. ReMoGPT
5. T2M-GPT
6. MMM
7. WalkTheDog

---

## 与当前 MoDebug 结论的关系

| MoDebug 当前问题 | 必读参考 | 结论边界 |
|---|---|---|
| L15 fixed-scale substitution 为什么有效 | CFG++、TCFG、CFG-Ctrl、CFG-Zero*、FlowMotion | 只能形成假设；当前先作为强基线和高风险接口约束，不把它当能力展示。 |
| 为什么 adaptive gate 降级 | APG、C2FG、S-CFG | 旧 gate trace 接近常数缩放；下一步若做 gate，必须服务 T1/T2 的 frame/part 选择性，不继续 tau/slope。 |
| 为什么要扩到 MotionCLR / TempoControl | MotionCLR、TempoControl、S-CFG | 扩的不是 baseline，而是 T1 时间区间控制的 token-time attention 接口。 |
| 为什么要做 part/time probe | ParTY、ReMoGPT、MaxSim、PST | 服务 T2 身体部件控制；全局 FID/Matching 不足以解释局部语义影响。 |
| 为什么需要负分支备选 | PAG、SEG、Autoguidance、Self-Swap | 若重启方法路线，应先有可控 weak branch，而不是继续 tau/slope grid。 |

---

## 一句话版本

当前 reading list 的主轴已经从 “防止 MoDebug overclaim” 改为 “为 T1/T2 能力目标建立机制适配库”：MoLingo 本体是 S0，CFG++ / APG / TCFG / C2FG / CFG-Ctrl / CFG-Zero* / FlowMotion 是 guidance / flow 机制库，S-CFG / MotionCLR / TempoControl / ParTY 是时间区间控制和身体部件控制的核心启发，MaxSim / PST / MoCHA 等负责把全局指标拆成细粒度证据。
