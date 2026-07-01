---
title: "StoryMotion Decoupled Coupling QA"
hypothesis: "StoryMotion 的核心不应写成三模式统一本身，而应写成 root/relation-aware 的 human-camera 受控生成：保留 Pulp latent contract，同时显式建模 camera 对 human root 的表示依赖、completion 条件可靠性与不同任务中的条件方向。"
status: draft
created: 2026-06-24T00:00:00+08:00
updated: 2026-06-25T19:38:00+08:00
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI|CondMDI]]"
  - "[[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation|COIN]]"
  - "[[analysis/CVPR_2026/Decoupled_Generative_Modeling_for_Human_Object_Interaction_Synthesis|DecHOI]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/Motion_In_Betweening_for_Densely_Interacting_Characters|Cross-Space In-Betweening]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/StableMotion_Training_Motion_Cleanup_Models_with_Unpaired_Corrupted_Data|StableMotion]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba|TCM]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]"
  - "[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness|E.T. / Director]]"
  - "[[analysis/CVPR_2024/DanceCamera3D_3D_Camera_Movement_Synthesis_with_Music_and_Dance|DanceCamera3D]]"
  - "[[analysis/NEURIPS_2025/Cameras_as_Relative_Positional_Encoding|Cameras as Relative Positional Encoding]]"
web_sources:
  - "https://arxiv.org/abs/2510.05097"
  - "https://arxiv.org/abs/2405.11126"
  - "https://arxiv.org/abs/2408.16426"
  - "https://arxiv.org/abs/2505.03154"
  - "https://arxiv.org/abs/2605.06667"
  - "https://arxiv.org/abs/2504.14899"
---

# StoryMotion Decoupled Coupling QA

> [!abstract] 结论先行
> StoryMotion 当前路线不应被判定为失败。相反，现有证据说明 **Pulp Stage1 frozen latent contract + branch-mask Stage2** 是目前唯一跑通 official reconstruction、joint generation 与三模式接口的稳定闭环；source VAE / GRFSQ 的坍塌反而证明不能轻易替换这个 contract。
>
> 但当前路线确实存在更具体的架构上限：Pulp camera feature 显式包含 `camera_translation - human_root_translation`，decode 时又把 human root 加回 camera translation。camera latent 因而不是独立于 human 的变量。当前 Stage2 同时 denoise `concat([z_hum,z_cam])`，却没有显式建模 root-level 方向性；completion 又把 observed branch 当作近乎绝对可信条件。风险应更准确地写成 **root-level 因果结构缺失、条件优先级失衡、generated/noisy condition 错误传播**。
>
> 2026-06-25 follow-up 进一步确认：当前 `soft observed` 配方没有得到 clean-task Pareto 改善；camera / human single-task specialists 与 unified control 在 native clean completion 上总体接近，但 zero / shuffle observed branch 时仍灾难性退化；screen projection containment 在显著降低 outscreen 的同时破坏 camera generation，并在训练中进入 NaN。下一版不应先在 raw latent 全通道上继续加 gate，而应先决定任务定义，并验证 **root/relation first、条件可靠性和 camera-agnostic human generation** 三类假设。
>
> 同日补齐的 PulpMotion pure / mixed `batch_size=64` Stage1 与 Stage2 full eval 消除了本地 R@K 的主要协议差异。Pulp Stage1 reconstruction 明显优于其 Stage2 generation，确认瓶颈主要在生成器而非 frozen tokenizer；同 `b64` mixed point estimate 下，StoryMotion clean joint 在表列核心指标上优于 Pulp no-Aux，相对 Pulp Aux 仅 TMR 略低，但该结论仍受单 seed、不同模型与 sampler 配方限制，不能扩写为统计 SOTA。

## 2026-06-24 5090 full eval 核心结论

结果目录：`stage2/metrics/v5_controlled_coupling_20260624/`。所有已完成项均为 mixed full test `10549` samples、同 checkpoint、50-step DDIM、`cfg=2.0`、`eta=1.0`、same noise seed。

这批实验不是为了证明某个指标更高，而是回答四个更具体的问题：completion 到底依赖文本还是 observed branch；joint human 退化是不是 simultaneous denoising 造成；GT camera 是否能把 human 拉回几何上界；two-stage coupling schedule 是否已经是可用修复。A dependency matrix 已补齐 `15/15`，可以写依赖诊断结论，但仍不能写“修复已完成”。

| 实验                               | 要回答的问题                                            | 关键结果                                                                                                                                      | 结果标记                                            |
| -------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| A dependency matrix              | text half、observed branch、generated branch 谁在支配输出 | `15/15` full items 完成；completion 两个方向对 text noise 基本不变，对 observed branch 破坏明显退化；joint 对 text perturbation 敏感，shuffle / zero text 会把语义指标拉低 | 完成；支持 condition dominance / branch pollution 诊断 |
| B joint shared-noise             | joint simultaneous denoising 本身是否导致 human 退化      | joint：FDTMR `153.72`，TMR `23.91`，MPJPE `0.1928`                                                                                           | 完成；作为 replay 对照                                 |
| B generated-camera replay        | 先生成 camera 再做人，是否比 joint human 明显更好               | replay：FDTMR `148.69`，TMR `23.54`，MPJPE `0.1947`，与 joint 同区间                                                                              | 完成；主因不是 simultaneous denoising                  |
| C GT-camera oracle               | 如果 camera 条件完全正确，human 是否恢复                       | Human Cov `84.58%`，MPJPE `0.0884`，Contact Δ `0.1543`，但 TMR `18.17`                                                                        | 完成；GT camera 是几何/覆盖上界；语义解释需收缩                   |
| D boundary `0.3` / `0.5` / `0.7` | two-stage schedule 能否作为无需训练的修复                    | boundary 后移时 Cov `59.38%→77.96%`、MPJPE `0.1354→0.1073` 变好，但 TMR `19.82→18.83` 下降                                                          | 完成；这是 coupling 强度 tradeoff，不是 Pareto 修复         |

核心指标数值如下。A 表只用于依赖诊断，不等价于修复结果。

| config                    | task  | FDTMR ↓ | TMR ↑ |   R3 ↑ | Human Cov ↑ | MPJPE ↓ | Contact Δ ↓ | FDCLaTr ↓ | CLaTr ↑ |   F1 ↑ | Out ↓ |
| ------------------------- | ----- | ------: | ----: | -----: | ----------: | ------: | ----------: | --------: | ------: | -----: | ----: |
| B joint shared-noise      | joint |  153.72 | 23.91 | 26.38% |      36.77% |  0.1928 |      0.3428 |     84.82 |   33.76 | 37.81% | 7.72% |
| B generated-camera replay | human |  148.69 | 23.54 | 26.26% |      39.10% |  0.1947 |      0.3427 |         - |       - |      - |     - |
| C GT-camera oracle        | human |  126.63 | 18.17 | 21.83% |      84.58% |  0.0884 |      0.1543 |         - |       - |      - |     - |
| D boundary `0.3`          | human |  133.51 | 19.82 | 23.59% |      59.38% |  0.1354 |      0.2853 |         - |       - |      - |     - |
| D boundary `0.5`          | human |  131.36 | 19.15 | 22.84% |      71.37% |  0.1193 |      0.2608 |         - |       - |      - |     - |
| D boundary `0.7`          | human |  130.23 | 18.83 | 22.75% |      77.96% |  0.1073 |      0.2344 |         - |       - |      - |     - |

A dependency matrix 的 completion 侧结果：

| task   | intervention            | FDTMR ↓ | TMR ↑ |   R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ |   F1 ↑ | Camera Cov ↑ | MPJPE ↓ |
| ------ | ----------------------- | ------: | ----: | -----: | ----------: | --------: | ------: | -----: | -----------: | ------: |
| camera | text noise camera       |       - |     - |      - |           - |     15.16 |   53.87 | 62.45% |       86.50% |       - |
| camera | text noise human        |       - |     - |      - |           - |     15.20 |   53.84 | 62.43% |       86.71% |       - |
| camera | text noise all          |       - |     - |      - |           - |     15.66 |   53.30 | 61.71% |       86.75% |       - |
| camera | observed human + noise  |       - |     - |      - |           - |    303.00 |   25.68 | 27.82% |       31.04% |       - |
| camera | observed human shuffle  |       - |     - |      - |           - |    117.68 |   14.61 | 19.48% |       50.53% |       - |
| camera | observed human zero     |       - |     - |      - |           - |   1044.19 |    4.36 |  3.79% |        0.35% |       - |
| human  | text noise camera       |  126.70 | 18.15 | 21.64% |      84.61% |         - |       - |      - |            - |  0.0884 |
| human  | text noise human        |  126.66 | 18.10 | 21.77% |      84.61% |         - |       - |      - |            - |  0.0888 |
| human  | text noise all          |  126.77 | 18.09 | 21.72% |      84.61% |         - |       - |      - |            - |  0.0888 |
| human  | observed camera + noise |  154.70 | 14.94 | 20.03% |      72.91% |         - |       - |      - |            - |  0.1162 |

A dependency matrix 的 joint 侧结果：

| intervention                | FDTMR ↓ | TMR ↑ |   R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ |   F1 ↑ | Camera Cov ↑ | Out ↓ | MPJPE ↓ |
| --------------------------- | ------: | ----: | -----: | ----------: | --------: | ------: | -----: | -----------: | ----: | ------: |
| joint shared-noise baseline |  153.72 | 23.91 | 26.38% |      36.77% |     84.82 |   33.76 | 37.81% |       64.07% | 7.72% |  0.1928 |
| text noise camera           |  152.06 | 22.00 | 24.23% |      38.73% |    115.02 |   25.52 | 28.98% |       59.56% | 8.36% |  0.1949 |
| text noise human            |  150.06 | 19.75 | 21.95% |      40.93% |     99.74 |   28.00 | 32.03% |       62.89% | 8.24% |  0.2034 |
| text noise all              |  150.59 | 18.26 | 20.74% |      42.76% |    119.97 |   23.30 | 27.08% |       58.56% | 8.71% |  0.2039 |
| text shuffle all            |  154.41 |  6.37 |  7.44% |      37.42% |     95.63 |   11.21 | 17.70% |       61.36% | 9.23% |  0.2289 |
| text zero all               |  228.16 |  4.79 |  5.66% |      31.08% |     99.75 |   10.75 | 17.46% |       58.15% | 5.35% |  0.2160 |

### ABCD 核心分析

A/B/C/D 给出的不是“某个小技巧已经修好模型”，而是把当前架构上限定位清楚了：

1. **Completion 不是在做均衡的 text + observed branch 条件生成**。A 矩阵里，camera completion 对三种 text noise 基本同区间，但 observed human 被 noise / shuffle / zero 后指标大幅下降；human completion 也一样，text noise 基本同区间，observed camera 加噪后退化。最直接的解释是：当前 completion 的主导条件是 observed branch，文本在这组干预里没有形成强控制面。这个能力可以用于“给一支 clean branch 补另一支”，但不能直接写成 robust text-conditioned completion。
2. **Joint 的问题不是 simultaneous denoising 这个表面形式**。B 里 generated-camera replay 与 joint shared-noise 同区间，replay 没有把 human 拉回 completion / oracle 水平。因此，简单改成“先生成 camera 再做人”不是核心修复。真正的问题更像是 joint 里的 generated branch 质量、文本语义和跨分支耦合强度没有被可靠调度。
3. **正确 camera 条件给出几何/覆盖上界，但不能直接解释为“压制语义”**。C 的 GT-camera oracle 把 Human Cov 拉到 `84.58%`、MPJPE 降到 `0.0884`，接近 clean human completion；TMR 为 `18.17`，低于 joint / replay 的 `23+`。这说明强 camera 条件能稳定几何，但 TMR 下降可能来自重建型任务目标、GT camera 对动作空间的约束，也可能来自语义自由度被压缩；现有数据不能单独判定“语义被 camera 压制”。
4. **D 证明 inference-time temporal gating 是有效诊断旋钮，不证明 learned schedule 已经成立**。Boundary 从 `0.3` 到 `0.7` 时 Human Cov `59.38% -> 77.96%`、MPJPE `0.1354 -> 0.1073`，但 TMR `19.82 -> 18.83` 下降。它说明“什么时候释放 observed branch / 什么时候回到文本生成”会移动几何和语义指标；但这是手调采样门控，不是训练出来的 coupling controller，也没有同时证明 camera 侧不退化。

架构核心上限可以更直白地写成三点：

1. **Hard observed replacement 太硬**：代码层面，`TemporalObsUNet.forward` 直接执行 `x = torch.where(obs_mask.bool(), obs_x0, x_t)`；official eval sampler 还会在每个 DDIM step 把 observed / padding branch 重新注入为 `q(z_gt,t)`，最后再 merge GT branch。训练 checkpoint 的 `obs_self_condition_prob=0.0`，等价于 observed branch 总是 clean / reliable。A 矩阵显示这种设定会让 completion 对 observed branch 形成主导依赖，一旦条件 branch 有噪声、估计误差或前轮生成误差，另一支会被拖垮。
2. **Branch-mask 只告诉模型“哪支可见”，没有告诉模型“该信谁、信多少、什么时候信”**：当前 mask pattern 不能表达 condition quality / trust / timing，也不能表达 human-camera 关系应该早期强耦合、后期弱耦合还是按样本自适应。D 的 boundary 结果说明 timing 本身会显著改变指标，但当前 timing 仍是推理期手调。
3. **Raw latent 拼接耦合缺少关系控制面**：human 和 camera 通过 `concat([z_hum,z_cam])` 与 shared denoising 隐式互相影响，容易把 camera 几何约束、文本语义和 human 动作细节混在一起。这个判断有中等证据：A 的 joint text-noise 对角结构显示 branch-specific routing + cross-talk；但“relation-space 一定能修好”仍是待验证假设，不能当成已证明结论。

Claude / Kiro 复查后的证据强度划分：

| 结论                                           | 证据强度  | 说明                                                                                                                                     |
| -------------------------------------------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Completion 当前主要由 observed branch 支配          | 强证据   | A 中 text noise 基本不动 completion 指标，但 observed branch noise / shuffle / zero 会大幅退化                                                       |
| Completion 和 joint 不是同一种条件机制                 | 强证据   | Completion 是 observed-dominant reconstruction-like；joint 是 text-driven generation，shuffle / zero text 会把 TMR / R3 / CLaTr / F1 拉低      |
| replay 不是修复 joint human 的主路径                 | 强证据   | generated-camera replay 与 joint shared-noise 指标同区间，不能把 human 拉回 oracle / clean completion 水平                                           |
| Boundary 是 coupling strength / timing 诊断旋钮   | 强证据   | Cov / MPJPE 随 boundary 后移变好，TMR 下降；但这是 inference gating，不是 learned controller                                                          |
| GT camera 降低 semantic metric                 | 中等证据  | TMR 低于 joint / replay，但 alternative explanation 是 reconstruction-like objective 或 GT camera 几何约束，需补 ground-truth human TMR / oracle 对照 |
| Raw latent concat 导致无控制耦合                    | 中等证据  | 架构与 A 矩阵一致指向该问题，但还缺消融证明 relation-space / gate 一定能改善                                                                                    |
| 4090 screen containment 的 relation-space 有效性 | 反例性诊断 | pre-NaN `best_eval@170000` 将 Out 降到 `0.50%`，但 FDCLaTr 恶化到 `350.06`，训练从 `175100` 起 NaN；不能写 Pareto 改善                                    |

2026-06-24 的原 follow-up 计划已完成 soft observed 与 camera/human specialist 的第一轮验证，但后续代码审计改变了优先级：

1. **Root/relation 方向先于 gate。** camera feature 对 human root 的依赖是表示事实；learned gate 只有在 root/relation 接口确定后才有清晰作用域。
2. **Human mode 先拆任务。** camera-conditioned actor recovery、root-only conditioning 与 text-only generation 不能继续混成一个 completion claim。
3. **Reliability training 仍必要，但不是唯一根因。** 第一版 soft observed 没有 Pareto 结果，且 robustness protocol 需要重做。
4. **Boundary 只保留为辅助诊断。** 它说明 trust/timing 会移动 tradeoff，不是论文前两位贡献，也不是最终控制器。

## 2026-06-25 follow-up full eval

结果目录：

- 5090：`stage2/metrics/v5_followup_20260625/last/`
- 4090：`stage2/metrics/v5_followup_20260625/last/` 与 `stage2/metrics/v5_followup_20260625/screen_best/`

原 follow-up 共完成 `16` 个 mixed full test：5090 上 `14` 项，4090 上 `2` 项；随后又在 5090 对两个 4090 checkpoint 完成 `4` 个 batch-size 对照复评。每项均为 `10549` samples、50-step DDIM、`cfg=2.0`、`eta=1.0`。

> [!warning] 统计与协议边界
> 所有训练和评估均为单 seed，当前表格是 full-set point estimate，不包含多 seed 方差或置信区间，不能宣称统计显著。
>
> PulpMotion 本地 official 配置 `configs/compnode/1g_1n.yaml` 的默认 eval batch size 是 `128/GPU`，其 `src/evaluate.py` 直接用该值构造 test DataLoader。Pulp 的 `RetrievalMetric.update()` 每个 batch 单独计算 `B×B` 距离矩阵，R@K 的候选池就是当前 batch，因此 R@K 不是 batch-size invariant。2026-06-25 已额外完成 Pulp pure / mixed `batch_size=64` rerun；本文新增的 Pulp-vs-StoryMotion b64 表可作内部公平比较，但仍不等于复现论文默认 b128 R@K。
>
> 名为 `observed_noise_matched` 的两项评估没有匹配训练噪声：代码先用同均值/标准差高斯随机量**整支替换** observed latent，再叠加 `observed_noise_level=1.0` 的相对噪声；训练使用的是 `noise_std=0.15` 加性扰动。该协议也缺少 clean-control 的同干预对照，因此只能标记为无效 robustness probe，不能据此判断 soft observed 成功或失败。

### PulpMotion b64 Stage1 / Stage2 公平基线

结果目录：`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_core_bs64_20260625/`。

协议如下：

- Stage1：Pulp official autoencoder reconstruction，pure / mixed full test，`batch_size=64`。
- Stage2：Pulp official DiT `(x,y)` checkpoint；mixed `step=330750`，pure `step=92950`。
- Stage2 sampler：50 steps、seed `42`、`cfg_rate_c=11.0`；no-Aux 使用 `cfg_rate_z=0.0`，Aux 使用 `cfg_rate_z=0.25`。
- mixed 共 `10549` samples，pure 共 `4053` samples。pure 与 mixed 是不同数据分布，不能把两者数值差异直接解释成训练配方的因果效果。

Stage1 reconstruction upper bound：

| split | n | FDTMR ↓ | TMR ↑ | Human R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ | Camera R3 ↑ | Camera Cov ↑ | F1 ↑ | r_fpd ↓ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mixed | 10549 | 124.46 | 18.17 | 21.81% | 85.41% | 15.51 | 58.10 | 54.53% | 87.16% | 67.01% | 0.238 | 4.64% |
| pure | 4053 | 109.34 | 15.94 | 20.13% | 92.43% | 17.66 | 60.53 | 34.62% | 84.53% | 77.62% | 0.137 | 3.47% |

Pulp Stage2 generation：

| split / guidance | FDTMR ↓ | TMR ↑ | Human R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ | Camera R3 ↑ | Camera Cov ↑ | F1 ↑ | r_fpd ↓ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mixed no-Aux | 376.39 | 23.34 | 20.44% | 10.63% | 88.17 | 30.52 | 23.00% | 51.60% | 34.16% | 5.161 | 26.63% |
| mixed Aux | 426.21 | 24.87 | 21.21% | 8.88% | 80.20 | 32.84 | 24.31% | 49.02% | 36.36% | 3.832 | 17.69% |
| pure no-Aux | 377.55 | 20.60 | 17.91% | 14.98% | 93.02 | 36.55 | 20.08% | 49.84% | 48.90% | 7.224 | 38.36% |
| pure Aux | 419.24 | 21.69 | 17.89% | 14.56% | 90.62 | 38.90 | 20.90% | 44.83% | 52.04% | 5.711 | 27.08% |

同一 mixed split、同一 evaluator、同一 `batch_size=64` 的本地直接比较：

| model | FDTMR ↓ | TMR ↑ | Human R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ | Camera R3 ↑ | Camera Cov ↑ | F1 ↑ | r_fpd ↓ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pulp no-Aux | 376.39 | 23.34 | 20.44% | 10.63% | 88.17 | 30.52 | 23.00% | 51.60% | 34.16% | 5.161 | 26.63% |
| Pulp Aux | 426.21 | 24.87 | 21.21% | 8.88% | 80.20 | 32.84 | 24.31% | 49.02% | 36.36% | 3.832 | 17.69% |
| StoryMotion clean joint | 157.36 | 24.26 | 26.84% | 37.43% | 76.85 | 36.16 | 29.83% | 65.80% | 40.21% | 0.482 | 7.58% |
| StoryMotion soft observed | 154.76 | 23.76 | 26.42% | 36.84% | 69.20 | 37.10 | 30.55% | 66.43% | 41.30% | 0.543 | 8.26% |

由此得到四个受限结论：

1. **Pulp bottleneck 在 Stage2 generation，不在 Stage1 tokenizer。** mixed Stage1 Human Cov / Camera Cov 为 `85.41% / 87.16%`，Stage2 no-Aux 下降到 `10.63% / 51.60%`；`r_fpd` 从 `0.238` 上升到 `5.161`。这为“保留 Pulp frozen Stage1”提供了直接数值证据。
2. **Pulp Aux 是明确 tradeoff，不是全指标 Pareto。** mixed Aux 相对 no-Aux 将 `r_fpd` 降低 `25.75%`、Out 降低 `8.94` 个百分点，并提高 TMR / CLaTr / F1；但 FDTMR 恶化 `13.24%`，Human Cov 和 Camera Cov 分别下降 `1.74 / 2.58` 个百分点。pure 上同样表现为 projection / semantic 改善与 human distribution / coverage 退化并存。
3. **StoryMotion clean joint 在同 b64 point estimate 下整体强于 Pulp Stage2。** 相对 mixed Aux，StoryMotion clean 的 FDTMR 低 `63.1%`、Human Cov 高 `28.54` 个百分点、Camera Cov 高 `16.78` 个百分点、`r_fpd` 低 `87.4%`、Out 低 `10.11` 个百分点；TMR 则低 `0.61`。这支持“本地公平协议下多数核心指标更优”，不支持“全面或统计显著 SOTA”。
4. **StoryMotion completion 已接近 Pulp Stage1 reconstruction 区间，joint 仍有明显缺口。** clean human completion 的 FDTMR / coverage 为 `126.30 / 84.86%`，接近 mixed Stage1 的 `124.46 / 85.41%`；clean camera completion 的 FDCLaTr / coverage 为 `13.80 / 86.74%`，也与 Stage1 的 `15.51 / 87.16%` 同区间。FD 不是逐样本重建误差，不能把更低的 FDCLaTr 解释成“超过 tokenizer 上界”。clean joint coverage 仍只有 `37.43% / 65.80%`，因此下一版主要空间仍在 Stage2 joint factorization。

### 训练与评估状态

| run                           | 训练设置                                     |                       checkpoint | full eval                              | 判定                                  |
| ----------------------------- | ---------------------------------------- | -------------------------------: | -------------------------------------- | ----------------------------------- |
| clean continued control       | `task_probs=1/1/1`，无 observed corruption |                         `196000` | joint / camera / human                 | 本轮因果对照                              |
| soft observed                 | `prob=0.5`，`mode=noisy`，`noise_std=0.15` |                         `196000` | clean 三任务 + 2 个错误协议 probe              | clean 指标有效；robustness 未被正确测量        |
| camera specialist             | `task_probs=1/0/0`                       |                         `196000` | clean camera + observed zero / shuffle | 有效内部 baseline                       |
| human specialist              | `task_probs=0/1/0`                       |                         `196000` | clean human + observed zero / shuffle  | 有效内部 baseline                       |
| CondMDI-style human-only      | 旧 branch-mask 脚本，`task_probs=0/1/0`      |                         `196000` | 4090 b16 + 5090 b16/b64                | checkpoint 有效；不是官方 CondMDI baseline |
| screen projection containment | projection weight `0.01`                 | `best_eval=170000`；`last=176000` | 4090 b16 + 5090 b16/b64                | best 有效；last 从 `175100` 起 NaN       |

### Clean full metrics

Joint generation：

| config               | FDTMR ↓ | TMR ↑ |   R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ |   F1 ↑ | Camera Cov ↑ | Out ↓ |
| -------------------- | ------: | ----: | -----: | ----------: | --------: | ------: | -----: | -----------: | ----: |
| clean control        |  157.36 | 24.26 | 26.84% |      37.43% |     76.85 |   36.16 | 40.21% |       65.80% | 7.58% |
| soft observed        |  154.76 | 23.76 | 26.42% |      36.84% |     69.20 |   37.10 | 41.30% |       66.43% | 8.26% |
| screen best `170000` |  157.72 | 24.54 | 26.93% |      36.19% |    350.09 |   20.98 | 17.44% |       33.14% | 0.50% |

Completion：

| config                 | task   |   FD ↓ | score ↑ |   R3 ↑ |   F1 ↑ | coverage ↑ |
| ---------------------- | ------ | -----: | ------: | -----: | -----: | ---------: |
| clean control          | camera |  13.80 |   55.40 | 51.56% | 64.24% |     86.74% |
| soft observed          | camera |  15.59 |   53.94 | 48.84% | 61.55% |     83.62% |
| camera specialist      | camera |  14.33 |   57.04 | 53.32% | 65.98% |     86.68% |
| clean control          | human  | 126.30 |   18.22 | 21.83% |      - |     84.86% |
| soft observed          | human  | 125.77 |   18.88 | 22.36% |      - |     82.12% |
| human specialist       | human  | 125.28 |   18.24 | 22.01% |      - |     84.82% |
| CondMDI-style internal | human  | 125.44 |   18.24 | 21.99% |      - |     84.70% |

这里 `FD / score` 在 camera task 分别指 FDCLaTr / CLaTr，在 human task 分别指 FDTMR / TMR。表中 4090 checkpoint 的 R@K 已改用 5090 `batch_size=64` 复评值，与其余 StoryMotion 及新增 Pulp b64 表项保持同协议；仍不能写“匹配官方 CondMDI”，因为这是内部实现，也不能把本地 Pulp b64 rerun 写成论文默认 b128 结果。

### 4090 checkpoint、NaN 与跨机器指标审计

结果目录：`stage2/metrics/v5_followup_20260625/reeval_4090_ckpt_on_5090/`。

| checkpoint / eval    |   FDTMR |    TMR | Human R1/R2/R3     | Human Cov | FDCLaTr | Camera R3 |     F1 |   Out |
| -------------------- | ------: | -----: | ------------------ | --------: | ------: | --------: | -----: | ----: |
| CondMDI 4090 b16     | 125.445 | 18.238 | 23.17/38.31/48.90% |    84.70% |       - |         - |      - |     - |
| CondMDI 5090 b16     | 125.446 | 18.237 | 23.19/38.30/48.89% |    84.69% |       - |         - |      - |     - |
| CondMDI 5090 b64     | 125.441 | 18.237 | 9.65/16.28/21.99%  |    84.70% |       - |         - |      - |     - |
| screen best 4090 b16 | 157.718 | 24.537 | 28.14/44.81/56.76% |    36.29% | 350.064 |    43.75% | 17.42% | 0.50% |
| screen best 5090 b16 | 157.725 | 24.537 | 28.19/44.80/56.75% |    36.34% | 350.077 |    43.83% | 17.39% | 0.50% |
| screen best 5090 b64 | 157.717 | 24.538 | 12.10/20.40/26.93% |    36.19% | 350.086 |    19.18% | 17.44% | 0.50% |

审计结论：

1. **指标巨大差异不是数据或 checkpoint 异常，而是 eval batch size 改变了 R@K 候选池。** 5090 b16 几乎逐项复现 4090 b16；同一 5090 环境改成 b64 后，CondMDI Human R3 从 `48.89%` 降到 `21.99%`，screen Human R3 从 `56.75%` 降到 `26.93%`、Camera R3 从 `43.83%` 降到 `19.18%`，但 FD、score、coverage、F1 和 Out 基本不变。
2. **两机数据一致。** `train.pt`、`val.pt`、`summary.json`、mixed train/test split、metric model 文件均同 hash；screen loss 额外读取的 `intrinsics`、`proj_joints`、`traj`、`cam_segments` 目录汇总 hash 也一致。
3. **4090 run 不是用 batch 16 训练。** 两个 run metadata 的训练 `batch_size=512`；screen 配置中的 `screen_projection_max_samples=16` 只是每个训练 batch 参与辅助 projection loss 的样本上限。`16` 是此前 full eval 为避免 4090 OOM 使用的 eval batch size。
4. **CondMDI `last@196000` 有效。** TensorBoard 43 个 scalar tag 与非 resume 原始日志均无 NaN/Inf；model、raw model、EMA 权重全部有限。human native eval loss 稳定，total eval loss 上升来自未训练 camera/joint task 被一并平均，不能解释为 human 训练发散。
5. **screen `best@170000` 有效，但 `last@176000` 失效。** best 权重全部有限；原始日志从 `step=175100` 起 `loss / grad_norm / screen_projection_loss` 同时 NaN，共 `10` 个非有限训练记录。TensorBoard 因过滤非有限 loss 而在 `175000` 截断，对应 outscreen 在 `176000` 跳到 `1.0`；`last@176000` 的 model/raw/EMA 权重全部非有限。

### 干预结果

| model / task         | observed intervention            |    FD ↓ | score ↑ |   R3 ↑ |   F1 ↑ | coverage ↑ |
| -------------------- | -------------------------------- | ------: | ------: | -----: | -----: | ---------: |
| camera specialist    | clean                            |   14.33 |   57.04 | 53.32% | 65.98% |     86.68% |
| camera specialist    | shuffle                          |  101.55 |   13.92 |  9.70% | 18.59% |     51.69% |
| camera specialist    | zero                             | 1036.55 |    5.66 | 10.59% |  4.53% |      0.27% |
| human specialist     | clean                            |  125.28 |   18.24 | 22.01% |      - |     84.82% |
| human specialist     | shuffle                          |  194.03 |    4.70 |  7.09% |      - |     57.42% |
| human specialist     | zero                             | 1974.43 |    6.73 |  6.76% |      - |      0.15% |
| soft observed camera | random replacement + extra noise |  448.49 |   12.96 | 11.84% | 12.47% |     11.37% |
| soft observed human  | random replacement + extra noise |  937.32 |    0.00 |  7.79% |      - |      1.41% |

最后两行不是 matched additive-noise test，不与 clean control 做因果比较。

### 统计分析与决策

1. **Soft observed 没有形成 Pareto 改善。** 相对 clean control，joint camera 的 FDCLaTr 改善 `9.96%`，CLaTr / F1 / coverage 小幅上升，但 joint human TMR 下降 `2.05%`、Human Cov 下降 `0.59` 个百分点，Out 上升 `0.68` 个百分点。clean camera completion 五个主指标全部退化，其中 FDCLaTr 恶化 `12.95%`、coverage 下降 `3.12` 个百分点。clean human completion 的 FDTMR / TMR / R3 改善，但 coverage 下降 `2.74` 个百分点。当前配方只能写“改变了任务权衡”，不能写“解决了 controlled coupling”。
2. **Specialists 与 unified control 在 native clean completion 上总体接近。** camera specialist 的 CLaTr、R3、F1 更高，但 FDCLaTr 略差 `3.87%`，coverage 基本不变；human specialist 的 FDTMR 改善 `0.81%`，其余变化接近零。单 seed 结果既不支持 unified 有质量优势，也不支持 specialist 明显更优。统一接口可能仍有参数与维护效率价值，但本轮没有统计参数量 / 总训练成本，也没有 joint-only specialist，因此 fair three-model baseline 只完成了一部分。
3. **Single-task training 没有解决 observed-branch dominance。** 两个 specialist 在 observed zero 时 coverage 均接近 `0`，shuffle 时语义与分布指标也显著崩溃。这把根因从“多任务互相干扰”进一步缩小到 hard observed injection / reliability modeling 本身。
4. **Soft-observed robustness 仍未回答。** 当前错误协议不能测训练噪声鲁棒性。最小补测应对 clean control 与 soft observed 使用完全相同的 additive noise sweep，例如 `0.0 / 0.05 / 0.10 / 0.15 / 0.30 / 0.50`，并禁止 latent replacement。
5. **Screen projection containment 是失败性 tradeoff。** pre-NaN best 相对 clean control 将 Out 从 `7.58%` 降至 `0.50%`，但 FDCLaTr 恶化 `355.49%`、F1 下降 `56.69%`、Camera Cov 下降 `49.36%`；随后训练从 `175100` 起 NaN。它证明强 projection penalty 可把相机约束到 screen 内，却会造成 camera distribution / semantics collapse，当前实现应停止作为主线修复。
6. **R@K 必须固定 eval batch size。** StoryMotion 与 Pulp 的本地 b64 对照已补齐，可用于内部公平比较；历史 b16 和论文默认 b128 仍不能混入同一张 R@K 表。对外最终协议仍应选择统一 b128，或实现收集全量 embedding 后的 batch-invariant global/chunked retrieval。
7. **本轮没有统计显著性结论。** `n=10549` 只说明每个点估计覆盖完整测试集；训练仍是单 seed。论文中应写 point estimates，并补至少 `3` 个独立训练 seed 或预注册 bootstrap / repeated-sampling 方案后再使用“显著改善”“等价”等措辞。

当前决策：

| 方向                              | 状态                  | 下一动作                                                                           |
| ------------------------------- | ------------------- | ------------------------------------------------------------------------------ |
| soft observed `p=0.5, std=0.15` | 不接受为最终配方            | 先修 robustness eval；若 matched sweep 仍无优势，再调整 corruption 分布与 quality signal      |
| camera / human specialists      | native baseline 已完成 | 补 joint-only specialist、参数量、总训练 FLOPs / wall time，完成真正的 three-model comparison |
| root-first joint                | 待定义接口               | 先确定 root/coarse relation 表示，再与 simultaneous baseline 同预算比较                     |
| human condition variants        | 待敲定                 | full camera / root-only / no-camera 分开命名和比较                                    |
| reliability-aware completion    | 第一版失败               | 任务定义确定后再设计 clean/noisy/generated/missing source 与 quality token                |
| learned coupling gate           | 后置                  | 只在 root/relation 与 reliability 路线仍不足时考虑                                        |
| screen projection containment   | 当前实现停止              | 只保留失败诊断；若重启需 bounded loss、gradient/finite guard 与渐进权重                          |
| R@K protocol                    | b64 内部基线已完成        | 论文对外比较仍统一到 Pulp default b128，或改为 batch-invariant retrieval                   |

## 2026-06-24 4090 screen containment 状态

4090 上的 Pulp 主路线 screen projection containment 旧 run 已结束但不是成功完成：`runs/train/stage2/v5_indepdrop_screen_projection_20260624/gpu0_indepdrop_screen_w0p01_jointonly_sub16_b512` 从 `step=146000` 目标续训到 `196000`，实际只写到 `step=148000`，没有 `last.pt` / `best_eval.pt`，也没有 official eval 结果。

根因已定位为代码级 eval metric 聚合 bug，不是设备问题，也不是 screen containment 架构本身失效：`diffusion_loss()` 记录了字符串字段 `screen_projection_task_scope = joint`，训练日志可以接受该字段，但 `evaluate()` 把所有 metric list 直接交给 `np.mean`，导致首次 eval 触发 `UFuncNoLoopError`。因此旧 run 不能从 `step=148000` 原地续跑；可用续跑点仍是原始 `step=146000` checkpoint。

修复后状态：`evaluate()` 已改为只聚合有限数值字段，并在 eval / test 前先保存 `last.pt`，避免再次因评估失败丢失当前步。完整 rerun 通过了早期 eval，但从 `step=175100` 起 `loss / grad_norm / screen_projection_loss` 全部 NaN，`screen_projection_outscreen=1.0`，`last.pt@176000` 无效。可用的 `best_eval.pt` 位于 `step=170000`。其 full official pre-NaN probe 将 Out 降到 `0.50%`，但 camera FDCLaTr 为 `350.06`、F1 为 `17.42%`、coverage 为 `33.32%`，远差于 clean control。结论已从“路径可运行、效果待定”更新为“当前 loss 配方不稳定且造成强约束下的 camera collapse”。

## Q1：是否应改为 human-root-first / relation-first？

结论：这是当前最值得优先验证的结构假设，但应写成 **root/relation first**，不是完整 human-first。

### 1. 已确认的数据表示事实

Pulp `TrajCharProjDataset` 的 camera feature 由三部分组成：

```text
camera_feat = [FOV(2), camera_translation - human_root_translation(3), camera_rotation_and_velocity(9)]
```

decode 时，代码先从 human feature 解出 human root，再执行：

```text
camera_translation = decoded_relative_distance + decoded_human_root
```

因此 camera branch 在表示和解码上都依赖 human root。这是代码级强证据，不是根据指标推断。当前 `concat([z_hum,z_cam])` simultaneous denoising 要同时预测父变量 human root 与依赖该父变量定义的 camera relation，确实存在 root-level 循环依赖风险。

### 2. 更合理的最小因果分解

```text
p(human, camera | text)
≈ p(root_human | text_human)
  · p(body_motion | root_human, text_human)
  · p(camera | root_human, text_camera, coarse_body_or_framing)
```

最小父变量应优先包含 human root trajectory、facing、coarse body extent / bbox 和 action phase，而不是完整 body motion。完整 human-first 会增加串行误差传播；root-first 只先解决坐标系和主轨迹。

证据边界：

| 判断 | 证据强度 | 当前解释 |
| --- | --- | --- |
| camera 表示依赖 human root | 强 | feature 和 decode 代码直接确认 |
| raw simultaneous denoising 存在结构错配风险 | 中等 | 与表示事实和 joint/condition 诊断一致，但尚无 root-first 对照 |
| root-first 优于 full human-first | 强推理、待实验 | camera 主要需要 root/relation，不需要完整 body 高频细节 |
| root-first 一定优于当前 joint | 未验证 | 不能在对照完成前写成性能结论 |

Generated-camera replay 只测试了“先生成 camera，再由 camera 生 human”，且使用 full generated camera condition；它没有测试“先 human root，再 camera”。因此 replay 失败不能否定 root-first，反而否定了与数据因果方向相反的 camera-first 修复。

## Q2：human completion 应如何定义？

“相机跟人走”描述的是物理因果 `human root -> camera`；给定 camera 生成 human 则是统计反问题 `p(human | camera, text)`。camera 可以提供 human root posterior，但不应决定 body semantics。需要把三种任务明确分开：

| 变体 | 条件 | 研究问题 | 命名边界 |
| --- | --- | --- | --- |
| camera-conditioned actor recovery | camera latent + human text | camera 中的 root/framing 信息能否帮助恢复 human | 当前 human completion |
| root/relation-conditioned human generation | 从 camera 提取的 root/relation + human text | 只保留有因果意义的几何约束，隔离 full camera latent 污染 | 推荐的结构化 completion |
| camera-agnostic human generation | human text only | human 是否根本不需要 camera；作为解耦上界和污染对照 | 严格说不是同定义 completion，而是 human-only generation 变体 |

用户提出的“human completion 只依赖 human text”是必要对照。它若优于 camera-conditioned 版本，说明当前 camera condition 的污染大于其 root posterior 价值；若几何/coverage 显著下降但语义保持，则说明 camera 的主要价值确实是 root/framing 约束。文档和论文中必须避免把它与给定 camera 的 actor recovery 当成同一任务直接宣称胜负。

## Q3：completion 是否需要 corrupted observed condition？

需要，但不能只训练单一轻噪声。第一版 `p=0.5, std=0.15` 没有 clean Pareto 改善，且现有 robustness probe 协议错误；下一版应把问题定义为 condition reliability，而不是继续盲加噪：

```text
observed source ∈ {clean, additive-noisy, generated, missing}
quality q ∈ [0, 1] or a discrete source token
p(target | observed, q, task text)
```

建议保留 clean 样本作为主分布，用 additive noise、generated condition 和 missing/dropout 覆盖实际输入。quality token 不能简单等同于把 binary mask 改为连续数值；它需要与 corruption source/strength 一致，避免模型把未知噪声继续当成可信条件。

## Q4：text 与 observed 应如何平衡？

先定义任务，再决定 text 的必要性：

- clean reconstruction-like completion：text 可以弱；
- camera-conditioned actor recovery：human text 应控制 body/action semantics，camera 只提供 root/relation；
- editable/robust completion：observed 不可靠时，real text 必须明显优于 shuffled/zero text；
- camera-agnostic human generation：human text 是唯一外部语义条件。

训练上不应通过增加 text dropout 来“增强 text”。text dropout 主要服务 CFG/robustness；更直接的做法是保留真实 task text，同时对 observed condition 做 source-aware corruption/dropout，使模型在 observed 不可靠时必须回退到 text + branch prior。

## 候选架构

| 架构候选 | 核心分解 | 优点 | 主要风险 | 当前状态 |
| --- | --- | --- | --- | --- |
| A. root-first joint | root -> body + camera | 符合 camera 表示方向；最接近根因 | 串行误差、root 表示需重新设计 | 首要架构假设 |
| B. root-only human completion | camera -> root/relation extractor -> human | 保留几何价值，隔离 full camera latent | camera 到 root 的反演可能多解 | 首要 completion 假设 |
| C. text-only human generation | human text -> human | 最干净的解耦/污染对照 | 不再满足给定 camera 的 actor recovery | 必要 baseline/变体 |
| D. reliability-aware completion | observed + quality/source + text -> target | 面向 noisy/generated practical input | source mixture 与 quality calibration 复杂 | 需先修正评估协议 |
| E. branch-specific gated residual | self stream + root/relation cross gate | 可在必要位置恢复双向交互 | 若仍在 raw latent 上开 gate，可能重复当前问题 | 后置于 A/B 诊断 |
| F. temporal coupling schedule | timestep-dependent trust/gate | 已有 D boundary 诊断支持 | 只是调度，不解决父变量定义 | 辅助机制，不是主贡献 |

当前不启动新训练。下一步需要先在 A/B/C/D 中敲定任务定义和最小对照，再决定多卡预算。

## Q5：当前路线是否有严重弊端或能力上限？

结论：有上限，但不是“Pulp Stage1 + CondMDI-like Stage2 这条路错了”。更准确的判断是：

1. **Pulp Stage1 是当前稳定地基**：mixed b64 reconstruction 的 Human / Camera coverage 为 `85.41% / 87.16%`，`r_fpd=0.238`、Out `4.64%`，明显优于 Pulp Stage2 generation；Pulp decode/evaluator 闭环完整，source VAE / GRFSQ 直接替换后 official metrics 又发生坍塌，因此不要轻易拆 Stage1。
2. **Stage2 的 branch-mask 设计没有表达 root-level 条件方向**：camera latent 的位置部分由 human root 定义，但 joint 仍把两个 latent 当作并列变量同步生成。
3. **Completion 的能力上限来自任务定义和可靠性混在一起**：camera-conditioned actor recovery、root-only conditioning 与 text-only human generation 尚未被拆开；binary branch mask 也不能表达 condition source / trust。

### 风险表

| 风险                                  | 当前证据                                                                                              | 影响                                                                | 推荐修复                                                                            |
| ----------------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Pulp latent contract 脆弱             | source VAE / GRFSQ 接 Stage2 后 official metrics 坍塌                                                 | 不能把任意 Stage1 当 drop-in replacement                                | 保留 Pulp 主线；只做 adapter / distillation / affine normalization 小实验                 |
| observed camera 支配 human completion | zero/shuffle observed camera latent 后 human 指标大退化；camera-text half 扰动几乎不变                         | completion 可能变成 camera-latent-driven，而不是 text + camera 的可控生成      | human-text/all-text 对称 intervention；condition dropout；软 observed branch         |
| camera 表示依赖 human root，但 joint 同步生成 | camera feature 使用 `camera_translation - human_root`，decode 需加回 human root | root 与 relation 同时预测可能形成循环依赖和误差互相污染 | root-first factorization；不要先完整 human 或先 camera |
| generated camera 污染 human | human completion 对 camera latent 强敏感；camera-first replay 与 joint 同区间 | full camera latent 可能把错误 root posterior 与无关 camera 细节一起注入 human | root-only condition、text-only human 对照、hybrid oracle |
| hard completion 错误传播                | 当前 completion 默认条件 branch 可靠                                                                      | 真实应用输入有估计噪声、编辑误差或前轮生成误差                                           | condition noise training、quality token、adaptive soft inpainting                 |
| 指标不能证明视觉可用                          | FDframing/Out 好不等于 human motion perceptual quality 好                                              | 顶会审稿会质疑 aggregate metric 掩盖失败样本                                   | camera projection render gate + per-frame failure taxonomy                      |

### 不建议的解决方式

1. **不建议立刻放弃 Pulp Stage1**。本地结果已经显示 source Stage1 路线在 official metric 上坍塌。更合理的是保留 Pulp frozen tokenizer，把创新集中在 Stage2 的受控耦合和可靠性。
2. **不建议只调 task ratio / loss weight**。比例扫描只能给诊断信号；如果某分支质量下降导致 coupling delta 下降，那是伪解耦，不是成功。
3. **不建议宣称 completion 已公平胜出**。camera / human same-backbone specialists 已完成，但结果与 unified control 总体接近，且仍缺 joint-only specialist、多 seed 与参数 / 总训练成本对照。
4. **不建议把“联合建模”作为唯一新颖性**。Pulp Motion、Towards Storytelling Animations、ActCam、Uni3C 等已经覆盖 joint camera-human/control 叙事，StoryMotion 必须证明它解决的是 partial observation、conditional completion 与受控耦合。

### 最小修复路线

2026-06-25 follow-up 已执行第一版 soft observed 与 camera / human specialists。下一轮实验暂不启动，先敲定以下决策顺序：

| 决策顺序 | 需要先回答的问题 | 候选选择 | 选择后的实验 |
| --- | --- | --- | --- |
| 1 | human mode 的目标是 actor recovery 还是 human generation？ | camera-conditioned / root-only / text-only | 决定哪些结果可在同一表中比较 |
| 2 | joint 是否采用 root-first 因果分解？ | current simultaneous / root-first / full human-first | 优先比较 current 与 root-first；full human-first 仅作高成本备选 |
| 3 | practical completion 接受哪些 condition source？ | clean / noisy / generated / missing | 设计 matched corruption 与 quality/source token |
| 4 | R@K 对外口径是什么？ | 本地 b64 已完成；Pulp b128 / batch-invariant global retrieval 二选一 | 在论文比较前固定，不再混用 b16/b64/b128 |
| 5 | 是否还需要 learned gate？ | root/relation gate / raw latent gate / no gate | 只有 A/B/D 仍不足时再进入架构级 gate |

当前可写的最小结论：StoryMotion 的根因假设已从泛化的“耦合过强”收缩为 **camera 表示依赖 human root，但 Stage2 未显式建模 root-level 方向；completion 又未区分 condition source、可靠性与任务语义**。root-first、root-only human completion 和 text-only human generation 都是待验证方案，尚不能写“修复已完成”。

## Q3：如何提升工作上限和顶会门槛？

结论：StoryMotion 顶会门槛的核心不应是“三模式大部分 SOTA”，而应是下面这个更强命题：

> Human-camera motion generation 的难点不是耦合越多越好，而是 camera relation 的定义依赖 human root，却又要支持 joint generation、actor recovery 和 camera direction 等不同条件方向。StoryMotion 应在统一接口内显式建模 root/relation 的父变量、completion condition reliability 与任务边界，而不是只在 raw latent 上调整耦合强度。

### 可形成的四个贡献点

贡献点 1：三模式 unified branch-mask generator，但必须配 fair internal baselines。

- 用同一个 Pulp Stage1、同一 DiT backbone、同一 split、同一训练预算，分别训练 Joint / Camera Completion / Human Completion 三个 single-task models。
- 报告 unified vs three separate models 的参数、训练成本、采样成本、三任务平均质量。
- 这样三模式统一才不是“把 mask 拼进去”，而是参数效率与多任务能力的实证贡献。

贡献点 2：root/relation-aware conditional factorization。

- 代码事实确认 camera translation feature 是 subject-relative，并依赖 human root 解码。
- joint 采用 root-first/coarse-relation-first，而不是 camera-first 或完全并列 denoising。
- human mode 区分 camera-conditioned actor recovery、root-only completion 与 text-only human generation。
- 该贡献必须由 current simultaneous vs root-first、full camera vs root-only vs no-camera 对照支撑。

贡献点 3：human-camera coupling diagnostics。

需要提出并固定一组污染/依赖指标：

```text
PI_H<-C = degradation(H metric | camera branch perturbed) - degradation(H metric | matched control)
PI_C<-H = degradation(C metric | human branch perturbed) - degradation(C metric | matched control)
ReplayGap_H = metric(joint_human) - metric(human_completion_given_joint_camera)
GTCameraGain_H = metric(human_completion_given_GT_camera) - metric(human_completion_given_joint_camera)
```

这些指标回答“模型是否真的利用少量耦合，还是被另一分支绑架”。这比只报 FDTMR / FDCLaTr 更像 research contribution。

贡献点 4：completion as practical editing / recovery task。

把 completion 作为应用主线：

- **Camera director mode**：给定 human motion，自动生成 cinematic camera。
- **Actor recovery mode**：给定 camera path 和 human text，利用 root/relation 条件补全符合取景的 human motion。
- **Human generation mode**：只给 human text，不读取 camera，作为解耦变体和污染上界；不与 actor recovery 混称同一 completion task。
- **Interactive repair mode**：给定一支有噪声或缺失的 branch，软修复另一支 branch，同时保持 projection reliability。

completion 不必一开始全面超过所有方法，但必须证明公平 baseline、输入噪声鲁棒性、失败样本分类和可视化可用性。

### 需要新增的评价协议

| 协议                            | 目的                         | 成功标准                                                                  |
| ----------------------------- | -------------------------- | --------------------------------------------------------------------- |
| RootFactor-BL                | 验证 camera 表示依赖是否要求 root-first | current simultaneous vs root-first，同预算比较 joint human/camera 与 root 指标 |
| HumanCondition-BL            | 区分 camera 的几何价值与 latent 污染 | full camera vs root-only vs no-camera，分离 root/body 指标 |
| FairIntra-BL                 | 证明 unified 不是简单工程拼接        | 与 three separate models 持平或更优，同时参数 / 训练成本更低 |
| Coupling intervention         | 区分有益耦合与污染                  | PI 下降，同时 FDTMR/FDCLaTr/coverage/projection 不退化                        |
| Condition noise robustness    | 验证 completion 实用性          | 输入噪声增加时，soft completion 退化慢于 hard completion                          |
| Camera projection render gate | 验证视觉可用性                    | in-frame ratio、bbox jitter、outlier rate、render failure taxonomy 闭环    |
| Replay / hybrid diagnosis     | 定位 joint human degradation | 能判定 simultaneous denoising、generated camera 分布偏差或 condition dominance |

### 论文叙事边界

可以写：

- StoryMotion 在 Pulp Stage1 latent contract 上，用 branch-mask diffusion 实现 joint generation、camera completion、human completion 的统一接口。
- 本地同 mixed split、同 evaluator、同 `batch_size=64` 的 point estimate 下，StoryMotion clean joint 在表列指标上优于 Pulp no-Aux，相对 Pulp Aux 仅 TMR 略低；该结果尚无多 seed 显著性，也不等同于 Pulp 论文默认 b128 协议。
- Pulp camera representation 显式依赖 human root；当前结果支持把 root/relation factorization 作为下一版核心假设，但尚未证明 root-first 性能更优。
- 当前评估揭示三种任务处在不同条件机制中：joint 是 text-driven generation，completion 是 observed-dominant reconstruction-like completion。
- Completion 是新的 conditional generation / editing task；camera / human internal specialists 已显示与 unified control 总体接近，但仍需正确的 condition-noise robustness、joint-only baseline 与多 seed 才能宣称方法优势。
- 关键技术问题是 controlled coupling：过弱则 human-camera 不一致，过强则 completion 错误传播和 joint branch 污染。

不要写：

- “全面、统计显著地超过 PulpMotion”。
- “human 与 camera 已经解耦”。
- “completion 已经公平超过已有方法”。
- “source VAE / GRFSQ 只是没调好，继续调 loss 就能解决”。

## 文献证据归纳

### 本地 KB 证据

- [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]：on-screen framing 是 human-camera 的有效桥接模态；适中 auxiliary guidance 有利，过强损害保真度。这直接支持“受控耦合”而非“越耦合越好”。
- [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]：角色与相机作为独立实体，通过成对交互模块交换信息；支持 StoryMotion 设计 branch-specific stream + gated residual。
- [[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI|CondMDI]]：training-time random mask 和显式 mask input 是补全能力的基础；但 StoryMotion 需要从“任意 mask 能补全”进一步升级为“不同 branch 的 condition priority 可控”。
- [[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation|COIN]]：动态控制、软修复和独立几何约束能缓解 human-camera entanglement；提醒 StoryMotion 不应硬相信 observed branch。
- [[analysis/CVPR_2026/Decoupled_Generative_Modeling_for_Human_Object_Interaction_Synthesis|DecHOI]]：复杂交互可通过“轨迹规划 + 动作合成”解耦降低优化难度；启发 StoryMotion 将 relation/framing planning 与 branch detail generation 分开。
- [[analysis/SIGGRAPH_ASIA_2025/Motion_In_Betweening_for_Densely_Interacting_Characters|Cross-Space In-Betweening]]：跨空间表示 + FiLM 调制比直接拼接更适合交互条件注入。
- [[analysis/SIGGRAPH_ASIA_2025/StableMotion_Training_Motion_Cleanup_Models_with_Unpaired_Corrupted_Data|StableMotion]]：质量变量与 adaptive cleanup 可作为 completion condition uncertainty 的模板。
- [[analysis/SIGGRAPH_ASIA_2025/TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba|TCM]]：条件注入位置会决定时序对齐质量；StoryMotion 后续可尝试把 camera/human temporal condition 注入 dynamics，而不只靠 cross-attention。

### Web 增强来源

- [Pulp Motion](https://arxiv.org/abs/2510.05097)：arXiv 摘要明确将 human motion 与 camera trajectory 的联合生成定义为 text-conditioned joint generation，并用 on-screen framing 作为桥接模态。
- [CondMDI](https://arxiv.org/abs/2405.11126)：arXiv 摘要说明其支持 dense/sparse、partial keyframe constraints，并比较 inference-time guidance / imputation。
- [COIN](https://arxiv.org/abs/2408.16426)：arXiv 摘要强调 moving camera 下 human/camera motion entanglement，并提出 control-inpainting diffusion prior 与 human-scene relation loss。
- [StableMotion](https://arxiv.org/abs/2505.03154)：用于支持质量变量、adaptive cleanup 和无配对损坏数据的运动修复视角。
- [ActCam](https://arxiv.org/abs/2605.06667)：2026 年最新 zero-shot joint camera and 3D motion control，使用 two-phase conditioning schedule，说明 staged guidance 已是强相关竞品思路。
- [Uni3C](https://arxiv.org/abs/2504.14899)：统一 3D-enhanced camera/human control，通过 specific-domain modules 与 jointly aligned 3D world guidance 减少联合标注依赖，提示 StoryMotion 必须强调 motion latent completion 与 controlled coupling 的差异。

## 最终建议

StoryMotion 当前最稳路线是：

1. **保留 Pulp Stage1 主线**，不要把 source tokenizer replacement 当近期主贡献。
2. **先敲定 root/relation factorization**：优先比较 current simultaneous 与 root-first；不要把 camera-first replay 失败误写成 root-first 被否定。
3. **拆分 human task**：camera-conditioned actor recovery、root-only conditioning 和 text-only human generation 分开命名、分开比较。
4. **再处理 condition reliability**：用 matched additive noise、generated、missing source 和 quality/source token；当前 soft observed 配方不是最终解法。
5. **learned gate 后置**：若 root/relation factorization 与 reliability training 仍不足，再在 root/relation 通道而非 raw latent 全通道上加 gate。

最小论文闭环不是继续堆一个更高的单表指标，而是证明以下 Pareto 改善：

```text
root-first joint geometry / coverage 不下降
root-only human condition 优于 full-camera 污染，或明确证明 camera 不需要进入 human branch
completion noise robustness 上升
coupling pollution index 下降
camera projection visual reliability 上升
fair separate-task baseline 不优于 unified controlled-coupling model
```

如果这些点成立，StoryMotion 就不只是 Pulp + CondMDI 的组合，而是一个显式尊重 root/relation 因果结构、同时支持多条件方向的 human-camera 生成框架。
