---
title: "StoryMotion Decoupled Coupling QA"
hypothesis: "StoryMotion 的核心不应写成三模式统一本身，而应写成 human-camera 受控耦合：保留 Pulp latent contract 的稳定闭环，同时用显式耦合诊断、软条件补全和可靠性协议避免完全耦合、completion 错误传播与 joint 模式污染。"
status: draft
created: 2026-06-24T00:00:00+08:00
updated: 2026-06-24T21:58:50+08:00
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
> 但当前路线确实存在架构上限：completion 分支在这组干预中更像 observed-branch-dominant reconstruction，而不是均衡的 text + observed 条件生成；joint 分支则明显依赖文本，但覆盖/几何质量仍弱于 clean completion / GT-camera oracle。这说明模型存在 **条件优先级失衡、生成相机污染人体、completion 硬条件错误传播** 的风险。
>
> 顶会叙事应从“三模式 SOTA”收缩为 **受控耦合生成的问题定义与验证路线**：在保留 Pulp 稳定 latent 的基础上，提出 human-camera coupling 的诊断指标、可调耦合机制、软条件补全和 camera-projection 可靠性协议。当前数据支持“受控耦合是核心问题”，但还没有证明最终机制已经解决该问题。

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

| 结论 | 证据强度 | 说明 |
| ---- | -------- | ---- |
| Completion 当前主要由 observed branch 支配 | 强证据 | A 中 text noise 基本不动 completion 指标，但 observed branch noise / shuffle / zero 会大幅退化 |
| Completion 和 joint 不是同一种条件机制 | 强证据 | Completion 是 observed-dominant reconstruction-like；joint 是 text-driven generation，shuffle / zero text 会把 TMR / R3 / CLaTr / F1 拉低 |
| replay 不是修复 joint human 的主路径 | 强证据 | generated-camera replay 与 joint shared-noise 指标同区间，不能把 human 拉回 oracle / clean completion 水平 |
| Boundary 是 coupling strength / timing 诊断旋钮 | 强证据 | Cov / MPJPE 随 boundary 后移变好，TMR 下降；但这是 inference gating，不是 learned controller |
| GT camera 降低 semantic metric | 中等证据 | TMR 低于 joint / replay，但 alternative explanation 是 reconstruction-like objective 或 GT camera 几何约束，需补 ground-truth human TMR / oracle 对照 |
| Raw latent concat 导致无控制耦合 | 中等证据 | 架构与 A 矩阵一致指向该问题，但还缺消融证明 relation-space / gate 一定能改善 |
| 4090 screen containment 的 relation-space 有效性 | 推测 | 目前只证明训练原型和 eval 路径可执行；full official metrics 未完成，不能写 Pareto 改善 |

后续核心修改意见只保留四个，不凑数，并按复查意见重排优先级：

| 核心实验                          | 改什么                                                                                                                     | 要回答的问题                                                               | 成功标准                                                                                           |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Soft observed branch training | 对 observed branch 加 corruption training：condition noise / dropout / quality token，先复用现有 `make_observed_condition_x0` 路径 | 只训练“可靠 clean observed branch”是否是 completion 脆弱性的直接根因                 | observed-noise 曲线明显慢于 hard baseline 退化，同时 clean completion 不明显退化                               |
| Fair separate-task baselines  | 训练 same tokenizer / same backbone / same split / same budget 的 joint、human completion、camera completion 单任务模型           | Unified branch-mask 是真实贡献，还是工程拼接后被 reconstruction-like completion 抬高 | Unified controlled-coupling 至少接近单任务模型，并给出参数/训练成本收益                                             |
| Learned coupling gate         | 在 Stage2 中加入 branch-specific stream + 零初始化 cross residual gate，gate 依赖 timestep、task、condition quality                  | corruption training 仍不足时，模型是否需要显式学习“何时耦合、耦合多少”                       | Joint human/camera 指标不低于 baseline，PI / intervention degradation 下降                             |
| Observed-camera hybrid oracle | 用 `α * GT camera + (1-α) * generated camera` 做 human completion，`α∈{0,0.25,0.5,0.75,1}`                                 | joint degradation 是否主要由 generated camera 质量瓶颈导致，还是 coupling 结构本身也有问题 | Human Cov / MPJPE / TMR 随 α 呈清晰趋势；若高 α 才恢复，先修 camera quality；若非线性或不恢复，再上 gate / relation-space |

对 QA 的直接更新：

1. **Q1：少部分耦合可行，但必须可控**。D 证明 two-stage schedule 能移动“几何/语义”的边界，但现在只是诊断旋钮；不能当成最终修复。下一步应把 schedule 变成 learned / quality-aware gate，而不是继续手调 boundary。
2. **Q2：当前路线的主要上限是 condition dominance / branch pollution**。A 已经把问题说得很直白：completion 两个方向在当前设置下没有测出对 text noise 的明显依赖，真正支配输出的是 observed branch；observed branch 被破坏时，另一支会明显退化。joint 模式则相反，对 text perturbation 很敏感，shuffle / zero text 会把 TMR、R3、CLaTr、F1 拉到很低。
3. **Q3：论文叙事应写 controlled coupling boundary**。这批结果不支持“统一三模式已经全面解决”，但支持一个更强、更稳的命题：StoryMotion 应证明如何诊断、调度和约束 human-camera coupling。

## 2026-06-24 4090 screen containment 状态

4090 上的 Pulp 主路线 screen projection containment 旧 run 已结束但不是成功完成：`runs/train/stage2/v5_indepdrop_screen_projection_20260624/gpu0_indepdrop_screen_w0p01_jointonly_sub16_b512` 从 `step=146000` 目标续训到 `196000`，实际只写到 `step=148000`，没有 `last.pt` / `best_eval.pt`，也没有 official eval 结果。

根因已定位为代码级 eval metric 聚合 bug，不是设备问题，也不是 screen containment 架构本身失效：`diffusion_loss()` 记录了字符串字段 `screen_projection_task_scope = joint`，训练日志可以接受该字段，但 `evaluate()` 把所有 metric list 直接交给 `np.mean`，导致首次 eval 触发 `UFuncNoLoopError`。因此旧 run 不能从 `step=148000` 原地续跑；可用续跑点仍是原始 `step=146000` checkpoint。

修复后状态：`evaluate()` 已改为只聚合有限数值字段，并在 eval / test 前先保存 `last.pt`，避免再次因评估失败丢失当前步。smoke run `runs/train/stage2/_check_indepdrop_screen_w0p01_evalfix_20260624` 已从 `146000` 跑到 `146001`，写出 `train` / `eval` / `test` 三类记录，并产生 `last.pt` 与 `best_eval.pt`。完整 rerun `runs/train/stage2/v5_indepdrop_screen_projection_20260624/gpu0_indepdrop_screen_w0p01_jointonly_sub16_b512_evalfix` 已通过旧崩溃点 `step=148000` 的首次 eval、`step=150000` 的 eval / test，以及 `step=152000` 的 eval；其中 `152000` eval 的 `joint_screen_projection_loss = 0.000731`、`joint_screen_projection_outscreen = 0.0`。日志为 `logs/indepdrop_screen_w0p01_joint_only_gpu0_evalfix_20260624.log`；run 仍在继续，尚未完成 `196000` full official eval，所以只能写“评估路径已修复并持续通过”，不能写 projection / semantic Pareto 改善已经成立。

## Q1：是否有其他方法实现少部分耦合？

结论：有，而且应优先做 **受控耦合**，不是完全解耦，也不是完全共享 latent。可参考的机制不是单一方法，而是一组共同原则：主分支保持独立生成能力，只在明确的关系空间、时序阶段或质量不确定区域打开 cross-branch 信息流。

### 推荐机制 1：实体独立编码 + 可门控交互残差

把 human 与 camera 当作两个独立实体，在 Stage2 内保留 branch-specific denoising stream，再通过零初始化或小权重初始化的 residual gate 注入 cross-branch 信息：

```text
h_h' = h_h + g_c2h(t, q) * R_c2h(h_h, h_c, text, frame)
h_c' = h_c + g_h2c(t, q) * R_h2c(h_c, h_h, text, frame)
```

其中 `g_c2h` / `g_h2c` 是随扩散时间步、任务模式和条件质量变化的门控。`q` 可以来自 condition quality、observed branch dropout mask、projection error 或 learned uncertainty。

依据：

- [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]] 证明角色与相机应作为独立实体，再用成对交互残差建模，而不是简单拼接。
- [[analysis/SIGGRAPH_ASIA_2025/Motion_In_Betweening_for_Densely_Interacting_Characters|Cross-Space In-Betweening]] 说明密集交互中直接拼接或普通交叉注意力会混淆坐标空间；显式相对空间变换 + FiLM 调制更稳。
- 对 StoryMotion 来说，这不要求推翻 Pulp Stage1。可以先在现有 `z_hum/z_cam` 之上改 Stage2 block：branch self-denoise 为主，cross residual 为可消融模块。

### 推荐机制 2：扩散时间上的 two-stage coupling schedule

早期强耦合锁定大结构与构图，后期弱化 cross-branch 条件，让 human 与 camera 各自恢复高频细节和语义自由度：

```text
early denoise: text + human-camera relation + observed branch strong
middle denoise: relation gate decays, branch self prior increases
late denoise: preserve observed branch softly, generated branch refines independently
```

依据：

- Pulp Motion 的 auxiliary guidance 显示适中 framing guidance 改善构图，过强会伤害保真度；这本质上就是“耦合强度有 Pareto 边界”。
- ActCam 使用两阶段 conditioning schedule：早期 pose + sparse depth 保结构，后期移除 depth、保留 pose 细化，避免过约束。
- StoryMotion 可实现最小版本：按 diffusion timestep 扫描 `cross_gate_boundary = 0.3/0.5/0.7`，报告 joint official metrics、completion metrics、projection jitter 与污染指数。

### 推荐机制 3：软条件补全，而不是硬 observed-branch 写死

当前 completion 将 observed branch 当作强条件。如果 observed branch 是 GT latent，结果可能很好；但实际应用中 observed human/camera 常来自估计器、编辑器或前一轮生成，误差会沿 branch coupling 放大。更稳的方式是软 inpainting：

```text
z_obs_soft = alpha(t, q) * z_obs + (1 - alpha(t, q)) * z_model_prior
```

`alpha` 不应固定，需随条件可信度和 denoising stage 变化。轻微错误晚修、严重错误早修。

依据：

- [[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation|COIN]] 指出扩散运动先验对 latent 小扰动敏感，用动态控制与软修复保持观测一致又避免硬传播。
- [[analysis/SIGGRAPH_ASIA_2025/StableMotion_Training_Motion_Cleanup_Models_with_Unpaired_Corrupted_Data|StableMotion]] 用质量变量和 adaptive cleanup 控制修复强度，说明“条件质量”本身可以成为生成变量。
- 对 StoryMotion：给 observed branch 加 noise/dropout/quality token，训练模型在 noisy condition 下补全，并报告噪声退化曲线。

### 推荐机制 4：关系空间耦合，而非 raw latent 全通道耦合

human-camera 不应在所有 latent channel 上自由耦合。更合理的是只通过少量关系变量耦合：

```text
relation r = projection/framing/contact-like descriptor
z_hum self prior: p(z_hum | text_h, r)
z_cam self prior: p(z_cam | text_c, r)
```

关系变量可以是 Pulp 的 screen framing latent、2D bbox center/scale、in-frame joint ratio、subject-relative distance 或 Toric-style screen coordinates。这样 camera 可以约束“怎么拍到人”，但不直接决定“人该怎么动”；human 可以约束“被拍对象在哪里”，但不直接决定 camera 的所有高频轨迹。

依据：

- [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]] 的核心是用 on-screen framing 作为桥接模态，而不是让所有 human/camera latent 无约束混合。
- [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]] 用 Toric screen-space 表示把相机参数与构图意图绑定。

### 推荐机制与最小修复路线的对应性

`### 最小修复路线` 目前主要落实的是诊断闭环，不是完整机制训练。对应关系如下：

| Q1 推荐机制                            | 已落实到最小修复路线的部分                                                                             | 当前状态                                                                            | 缺口                                                                        |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| 实体独立编码 + 可门控交互残差                   | Dependency matrix、Generated-camera replay、GT-camera oracle                                | 已落实为诊断：A/B/C 定位了 completion 的 observed-branch dominance、joint text sensitivity，以及 replay 不是主修复路径 | 还没有真正实现 branch-specific stream + learnable cross residual gate            |
| 扩散时间上的 two-stage coupling schedule | Two-stage coupling schedule                                                               | 已落实为 D：扫描 boundary `0.3/0.5/0.7`，确认存在几何/语义 tradeoff                             | 目前是 inference 手调边界，不是 learned 或 quality-aware schedule                    |
| 软条件补全，而不是硬 observed-branch 写死      | Soft observed branch、Dependency matrix                                                    | 已落实为诊断：A 直接显示 observed branch 破坏会导致 completion 明显退化，尤其 camera completion 对 observed human zero 几乎失去覆盖 | 还没有 condition noise / dropout / quality token 训练，也没有噪声退化曲线                |
| 关系空间耦合，而非 raw latent 全通道耦合         | GT-camera oracle、Two-stage coupling schedule；4090 screen projection containment evalfix rerun | 部分落实为诊断和工程可行性：C/D 说明 camera 条件强度会移动几何/语义边界；4090 containment 已验证 joint-only relation-space loss 可进入训练，eval 聚合 bug 已修复，且 eval / test 路径持续通过 | 尚未把 projection/framing descriptor 做成 Stage2 内部显式 relation variable 或 gate；完整 rerun official metrics 未完成，尚未证明 Pareto 改善 |

因此，当前最小修复路线已经覆盖了推荐机制 2 的实验验证，并为机制 1/3/4 提供了诊断证据；4090 containment 已把机制 4 推进到“训练原型可执行 + eval/test 路径通过”，但还没有推进到“性能有效”。下一轮不应直接把 relation-space 当成已证实解法，而应先做 **soft observed branch training + fair separate-task baselines + learned coupling gate + observed-camera hybrid oracle**。不要把 A/B/C/D 写成修复结果；它们是问题定位。

## Q2：当前路线是否有严重弊端或能力上限？

结论：有上限，但不是“Pulp Stage1 + CondMDI-like Stage2 这条路错了”。更准确的判断是：

1. **Pulp Stage1 是当前稳定地基**：official reconstruction upper bound 好，Pulp decode/evaluator 闭环完整；source VAE / GRFSQ 直接替换后 official metrics 坍塌，说明不要轻易拆 Stage1。
2. **Stage2 的 branch-mask 设计已暴露过耦合风险**：completion 中 observed branch latent 可能压过文本与 branch self prior；joint 时 generated camera latent 可能污染 generated human。
3. **能力上限来自缺少“耦合控制面”**：当前模型知道三种 mask pattern，但不知道何时应强耦合、何时应隔离、何时 observed branch 不可信。

### 风险表

| 风险                                  | 当前证据                                                                      | 影响                                                           | 推荐修复                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------- |
| Pulp latent contract 脆弱             | source VAE / GRFSQ 接 Stage2 后 official metrics 坍塌                         | 不能把任意 Stage1 当 drop-in replacement                           | 保留 Pulp 主线；只做 adapter / distillation / affine normalization 小实验         |
| observed camera 支配 human completion | zero/shuffle observed camera latent 后 human 指标大退化；camera-text half 扰动几乎不变 | completion 可能变成 camera-latent-driven，而不是 text + camera 的可控生成 | human-text/all-text 对称 intervention；condition dropout；软 observed branch |
| joint generated camera 污染 human     | human completion 对 camera latent 强敏感，joint 中 camera 又是生成值；replay 与 joint 同区间，说明不是简单 sequential 修复 | joint human 质量可能被 camera branch 错误拖垮，但还需 hybrid oracle 判断相机质量瓶颈占比 | observed-camera hybrid oracle、two-stage coupling schedule、learned coupling gate |
| hard completion 错误传播                | 当前 completion 默认条件 branch 可靠                                              | 真实应用输入有估计噪声、编辑误差或前轮生成误差                                      | condition noise training、quality token、adaptive soft inpainting         |
| 指标不能证明视觉可用                          | FDframing/Out 好不等于 human motion perceptual quality 好                      | 顶会审稿会质疑 aggregate metric 掩盖失败样本                              | camera projection render gate + per-frame failure taxonomy              |

### 不建议的解决方式

1. **不建议立刻放弃 Pulp Stage1**。本地结果已经显示 source Stage1 路线在 official metric 上坍塌。更合理的是保留 Pulp frozen tokenizer，把创新集中在 Stage2 的受控耦合和可靠性。
2. **不建议只调 task ratio / loss weight**。比例扫描只能给诊断信号；如果某分支质量下降导致 coupling delta 下降，那是伪解耦，不是成功。
3. **不建议宣称 completion 已公平胜出**。目前没有 same tokenizer、same backbone、same split、same budget 的 single-task completion baseline。
4. **不建议把“联合建模”作为唯一新颖性**。Pulp Motion、Towards Storytelling Animations、ActCam、Uni3C 等已经覆盖 joint camera-human/control 叙事，StoryMotion 必须证明它解决的是 partial observation、conditional completion 与受控耦合。

### 最小修复路线

优先级仍是先诊断，再加机制。A/B/C/D 已经完成第一轮诊断；下一轮只安排 4 个核心实验，其中前两个先回答“训练可靠性”和“公平基线”，第三个再动架构，第四个用最小 oracle 分解 generated-camera 质量瓶颈：

| 优先级 | 核心实验                          | 当前证据来源                                                                                                              | 直接目标                                                     | 继续 / 停止标准                                                                             |
| --- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 1   | Soft observed branch training | A 显示 completion 被 observed branch 主导；代码已有 `make_observed_condition_x0`，但当前 checkpoint `obs_self_condition_prob=0.0` | 用 corruption training 打破 clean-GT observed branch 的可靠性假设 | observed-noise 曲线慢于 hard baseline 退化；clean completion 不明显退化                           |
| 2   | Fair separate-task baselines  | 当前 unified 缺 same-budget single-task 对照                                                                             | 判断统一三模式到底是贡献还是工程拼接                                       | Unified controlled-coupling 接近单任务模型，同时给出参数/训练成本收益                                     |
| 3   | Learned coupling gate         | A/B/C/D 显示 coupling strength 需要按任务、时间步和条件质量调度                                                                       | 让模型学习何时打开 cross-branch residual                          | Joint 指标不低于 baseline，intervention degradation 下降                                      |
| 4   | Observed-camera hybrid oracle | C 只有 GT oracle，B 只有 generated-camera replay，还缺中间质量曲线                                                                | 分解 generated-camera 质量瓶颈和 coupling 结构瓶颈                  | Human Cov / MPJPE / TMR 随 α 呈清晰趋势；若高 α 才恢复，优先修 camera quality；若不恢复，再证明结构性 coupling 问题 |

当前可写的最小结论：`A/B/C/D` 已经把问题定位到 **condition dominance + branch pollution + coupling strength / timing**，而不是 sampling 同步问题。还不能写“修复已完成”；也不能把 relation-space containment 写成性能已验证。下一步就是上面四个核心实验，不再额外凑诊断项。

## Q3：如何提升工作上限和顶会门槛？

结论：StoryMotion 顶会门槛的核心不应是“三模式大部分 SOTA”，而应是下面这个更强命题：

> Human-camera motion generation 的难点不是耦合越多越好，而是找到可诊断、可调度、可应用的 **受控耦合边界**。StoryMotion 用一个统一 latent diffusion 覆盖 joint generation 与双向 completion，并提出 coupling diagnostics、soft conditional completion 与 projection reliability protocol；下一步必须证明这些机制能同时改善构图一致性、补全鲁棒性和实际可编辑性。

### 可形成的三个贡献点

贡献点 1：三模式 unified branch-mask generator，但必须配 fair internal baselines。

- 用同一个 Pulp Stage1、同一 DiT backbone、同一 split、同一训练预算，分别训练 Joint / Camera Completion / Human Completion 三个 single-task models。
- 报告 unified vs three separate models 的参数、训练成本、采样成本、三任务平均质量。
- 这样三模式统一才不是“把 mask 拼进去”，而是参数效率与多任务能力的实证贡献。

贡献点 2：human-camera coupling diagnostics。

需要提出并固定一组污染/依赖指标：

```text
PI_H<-C = degradation(H metric | camera branch perturbed) - degradation(H metric | matched control)
PI_C<-H = degradation(C metric | human branch perturbed) - degradation(C metric | matched control)
ReplayGap_H = metric(joint_human) - metric(human_completion_given_joint_camera)
GTCameraGain_H = metric(human_completion_given_GT_camera) - metric(human_completion_given_joint_camera)
```

这些指标回答“模型是否真的利用少量耦合，还是被另一分支绑架”。这比只报 FDTMR / FDCLaTr 更像 research contribution。

贡献点 3：completion as practical editing / recovery task。

把 completion 作为应用主线：

- **Camera director mode**：给定 human motion，自动生成 cinematic camera。
- **Actor recovery mode**：给定 camera path 和文本，补全符合取景的 human motion。
- **Interactive repair mode**：给定一支有噪声或缺失的 branch，软修复另一支 branch，同时保持 projection reliability。

completion 不必一开始全面超过所有方法，但必须证明公平 baseline、输入噪声鲁棒性、失败样本分类和可视化可用性。

### 需要新增的评价协议

| 协议                            | 目的                         | 成功标准                                                                  |
| ----------------------------- | -------------------------- | --------------------------------------------------------------------- |
| FairIntra-BL                  | 证明 unified 不是简单工程拼接        | 与 three separate models 持平或更优，同时参数 / 训练成本更低                           |
| Coupling intervention         | 区分有益耦合与污染                  | PI 下降，同时 FDTMR/FDCLaTr/coverage/projection 不退化                        |
| Condition noise robustness    | 验证 completion 实用性          | 输入噪声增加时，soft completion 退化慢于 hard completion                          |
| Camera projection render gate | 验证视觉可用性                    | in-frame ratio、bbox jitter、outlier rate、render failure taxonomy 闭环    |
| Replay / hybrid diagnosis     | 定位 joint human degradation | 能判定 simultaneous denoising、generated camera 分布偏差或 condition dominance |

### 论文叙事边界

可以写：

- StoryMotion 在 Pulp Stage1 latent contract 上，用 branch-mask diffusion 实现 joint generation、camera completion、human completion 的统一接口。
- 当前评估揭示三种任务处在不同条件机制中：joint 是 text-driven generation，completion 是 observed-dominant reconstruction-like completion。
- Completion 是新的 conditional generation / editing task，当前需要 fair internal baselines 和 condition-noise robustness 才能宣称方法优势。
- 关键技术问题是 controlled coupling：过弱则 human-camera 不一致，过强则 completion 错误传播和 joint branch 污染。

不要写：

- “全面超过 PulpMotion”。
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
2. **把 Stage2 从 branch-mask diffusion 升级为 controlled coupling diffusion**：先做 soft observed branch training 和 fair separate-task baselines，再上 branch-specific stream / learned gate；relation-space constraint 等 4090 full official eval 或 hybrid oracle 后再决定是否进入主线。
3. **把 completion 从附加能力升级为应用任务**：补 fair internal baselines、noise robustness、projection render gate。
4. **把顶会 insight 写成“受控耦合边界”**：先证明当前 branch-mask diffusion 的污染和错误传播，再验证软条件、learned gate 或 relation-space 约束能带来 joint framing 与 completion utility 的 Pareto 改善。

最小论文闭环不是继续堆一个更高的单表指标，而是证明以下 Pareto 改善：

```text
joint geometry / coverage 不下降
completion noise robustness 上升
coupling pollution index 下降
camera projection visual reliability 上升
fair separate-task baseline 不优于 unified controlled-coupling model
```

如果这五点成立，StoryMotion 就不只是 Pulp + CondMDI 的组合，而是一个可复用的 human-camera controlled-coupling 生成框架。
