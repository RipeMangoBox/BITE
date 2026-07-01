---
title: StoryMotion V6
hypothesis: StoryMotion V6 以 Pulp frozen Stage1 为稳定表示地基，在统一 branch-mask diffusion 接口中支持 joint human-camera generation、camera completion 与 human mode；下一版核心技术问题是显式建模 human→camera 条件方向与 completion condition reliability。
status: draft
created: 2026-06-25T20:05:00+08:00
updated: 2026-06-25T20:05:00+08:00
supersedes: "[[ideas/StoryMotion/2026-06-22_storymotion-v5]]"
source_notes:
  - "[[2026-06-23_storymotion-decoupled-coupling-qa-v5.1]]"
  - "[[ideas/StoryMotion/2026-06-24_storymotion-decoupled-coupling-claude-review-zh]]"
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI|CondMDI]]"
  - "[[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation|COIN]]"
  - "[[analysis/CVPR_2026/Decoupled_Generative_Modeling_for_Human_Object_Interaction_Synthesis|DecHOI]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/StableMotion_Training_Motion_Cleanup_Models_with_Unpaired_Corrupted_Data|StableMotion]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]"
---

# StoryMotion V6

> [!abstract] 核心正文
> StoryMotion V6 的主线是一个统一的 human-camera motion latent diffusion framework：在 frozen Pulp Stage1 latent contract 上，用同一个 Stage2 branch-mask denoiser 覆盖 text-only joint generation、text + human -> camera completion、text + camera / relation -> human mode。统一接口本身是第一贡献，但必须通过 fair internal baselines 证明参数效率、训练成本和三任务质量，而不能只写成工程拼接。
>
> 现有 full-set 证据支持保留 Pulp Stage1。Pulp Stage1 reconstruction 在 mixed b64 上达到 Human / Camera coverage `85.41% / 87.16%`，而 Pulp Stage2 no-Aux 下降到 `10.63% / 51.60%`；source VAE / HFSQ / GRFSQ 接入 Stage2 后 official human metrics 坍塌。StoryMotion clean joint 在同 mixed split、同 evaluator、同 `batch_size=64` 的 point estimate 下显著缩小 Pulp Stage2 generation 的分布和覆盖缺口，但 joint 仍明显低于 Stage1 reconstruction 上界。
>
> 下一版的核心技术问题不是继续加 raw-latent gate，而是显式处理 camera 对 human 的表示依赖（camera translation 由 human root 定义），并将 human→camera 的因果方向体现在生成顺序中；同时区分不同 human mode 的任务边界，以及 completion observed condition 的可靠性。V6 应把 human-first factorization、condition reliability 和 coupling diagnostics 作为第二阶段贡献闭环。

## 1. 问题定义

Human-camera motion generation 同时包含三个条件方向：

| 模式                | 条件                                   | 输出             | 目标                                                                                  |
| ----------------- | ------------------------------------ | -------------- | ----------------------------------------------------------------------------------- |
| joint generation  | text                                 | human + camera | 从文本同时生成动作与镜头，保证语义、运动分布、构图和画面包含度                                                     |
| camera completion | text + human motion                  | camera         | 给定演员动作，生成 cinematic camera trajectory                                               |
| human mode        | text + camera / none                 | human          | 区分 camera-conditioned actor recovery 和 camera-agnostic human generation |

V6 的论文问题应表述为：

```text
Can a unified latent diffusion model support joint human-camera generation and directional completion while respecting the human→camera causal direction and modeling condition reliability?
```

这个表述包含三层要求：

1. **统一接口**：同一个 Stage2 backbone 和 mask pattern 支持三类条件方向。
2. **受控耦合**：human 与 camera 需要共享 root/framing relation，但不能让 full latent condition 污染另一支生成。
3. **可靠 completion**：observed branch 可能来自 clean GT、noisy estimate、previous generation 或 missing input，模型需要知道 condition source 和 trust level。

## 2. 方法主线

当前稳定地基是 Pulp frozen Stage1：

```text
z = concat([z_hum, z_cam])
z_hum in R^{128 x T}
z_cam in R^{64 x T}
```

Stage2 使用 branch-mask latent diffusion。每个训练样本从 task distribution 中采样任务，构造 observed branch、target branch 和 text condition：

```text
joint:  text -> z_hum, z_cam
camera: text, z_hum_obs -> z_cam
human:  text, z_cam_obs or relation_obs -> z_hum
```

V6 保留这个统一框架，但将 human mode 拆为两个可检验变体：

| 变体                                | 条件                              | 用途                                       |
| --------------------------------- | ------------------------------- | ---------------------------------------- |
| camera-conditioned actor recovery | full camera latent + human text | 测试 camera 是否能恢复演员的 root/framing posterior |
| camera-agnostic human generation  | human text only                 | 提供 human-only baseline 和污染对照；判断 camera condition 是提供几何价值还是 latent 污染 |

第二阶段方法应从 human-first factorization 开始。Pulp camera feature 明确包含：

```text
camera_translation - human_root_translation
```

decode 时再把 decoded human root 加回 camera translation。因此 camera latent 不是与 human 独立并列的变量——camera 在表示层依赖 human。更合理的生成分解是：

```text
p(human, camera | text)
≈ p(human | text)
  · p(camera | human, text)
```

Camera 依赖 human 这一事实通过 human→camera 的生成顺序来尊重，避免了不必要的串行误差传播，同时保留了 camera 对 actor trajectory 的依赖。

## 3. 可靠实验事实

### 3.1 Pulp Stage1 是稳定表示地基

本地 b64 full eval 已补齐 Pulp Stage1 / Stage2 的 mixed 和 pure 对照。mixed split 覆盖 `10549` samples，pure split 覆盖 `4053` samples。

| model / split                    | FDTMR ↓ | TMR ↑ | Human R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ | Camera R3 ↑ | Camera Cov ↑ |   F1 ↑ | r_fpd ↓ |  Out ↓ |
| -------------------------------- | ------: | ----: | ---------: | ----------: | --------: | ------: | ----------: | -----------: | -----: | ------: | -----: |
| Pulp Stage1 mixed reconstruction |  124.46 | 18.17 |     21.81% |      85.41% |     15.51 |   58.10 |      54.53% |       87.16% | 67.01% |   0.238 |  4.64% |
| Pulp Stage2 mixed no-Aux         |  376.39 | 23.34 |     20.44% |      10.63% |     88.17 |   30.52 |      23.00% |       51.60% | 34.16% |   5.161 | 26.63% |
| Pulp Stage2 mixed Aux            |  426.21 | 24.87 |     21.21% |       8.88% |     80.20 |   32.84 |      24.31% |       49.02% | 36.36% |   3.832 | 17.69% |
| StoryMotion clean joint          |  157.36 | 24.26 |     26.84% |      37.43% |     76.85 |   36.16 |      29.83% |       65.80% | 40.21% |   0.482 |  7.58% |

结论：

1. Pulp Stage1 reconstruction 与 Pulp Stage2 generation 之间存在大 gap，说明瓶颈主要在生成器、采样和条件利用，而不是 tokenizer/decode contract。
2. StoryMotion clean joint 在同 b64 point estimate 下明显优于 Pulp Stage2 的 distribution、coverage、framing 和 outscreen 指标，但 TMR 不全面领先。
3. 这些结果仍是单 seed full-set point estimate，不写统计显著，也不与 Pulp 默认 b128 R@K 混表。

### 3.2 Completion 当前接近 reconstruction-like 上界

clean completion 在 native task 上接近 Pulp Stage1 reconstruction 区间：

| config                 | task   |   FD ↓ | score ↑ |   R3 ↑ |   F1 ↑ | coverage ↑ |
| ---------------------- | ------ | -----: | ------: | -----: | -----: | ---------: |
| clean control          | camera |  13.80 |   55.40 | 51.56% | 64.24% |     86.74% |
| camera specialist      | camera |  14.33 |   57.04 | 53.32% | 65.98% |     86.68% |
| clean control          | human  | 126.30 |   18.22 | 21.83% |      - |     84.86% |
| human specialist       | human  | 125.28 |   18.24 | 22.01% |      - |     84.82% |
| CondMDI-style internal | human  | 125.44 |   18.24 | 21.99% |      - |     84.70% |

这里 camera task 的 `FD / score` 是 FDCLaTr / CLaTr，human task 的 `FD / score` 是 FDTMR / TMR。

结论：

1. Unified control 与 camera / human specialists 在 clean completion 上总体接近。
2. 当前数据不支持单独宣称 unified model 在 completion 质量上显著优于 specialists。
3. Unified framework 的价值需要用三任务平均质量、参数量、训练 FLOPs、采样成本和维护成本一起证明。

### 3.3 Dependency matrix 定位了 condition 使用方式

5090 `v5_controlled_coupling_20260624` 已完成 mixed full test dependency matrix、generated-camera replay、GT-camera oracle 和 boundary scan。

| 结论                                | 实验                                   | 关键数值                                                                                  | 可写含义                                                      |
| --------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| completion 对 text noise 不敏感       | camera / human completion text noise | camera FDCLaTr `15.16 / 15.20 / 15.66`；human TMR `18.15 / 18.10 / 18.09`              | clean completion 主要不是由 text perturbation 决定               |
| completion 强依赖 observed branch    | observed zero / shuffle / noise      | camera observed zero coverage `0.35%`；human observed camera + noise coverage `72.91%` | practical completion 需要 condition reliability modeling    |
| joint 对 text 依赖强                  | joint text shuffle / zero            | TMR 从 `23.91` 到 `6.37 / 4.79`                                                         | joint 是 text-driven generation                            |
| generated-camera replay 未改善 human | camera-first replay                  | replay FDTMR `148.69`，joint FDTMR `153.72`                                            | full camera-first 不是当前主修复                                 |
| GT camera 给出几何上界                  | GT-camera oracle                     | Human Cov `84.58%`，MPJPE `0.0884`                                                     | correct camera/relation condition 对 geometry 有强约束价值       |
| boundary 是诊断旋钮                    | boundary `0.3 / 0.5 / 0.7`           | Cov `59.38% -> 77.96%`，TMR `19.82 -> 18.83`                                           | temporal trust schedule 会移动 geometry / semantics tradeoff |

这些结果支持将下一步从”继续调 raw latent coupling”转为”先做 human-first 生成顺序、condition reliability 和 human mode 定义”。

### 3.4 Soft observed 与 screen containment 的现状

第一版 soft observed `p=0.5, std=0.15` 改变了 clean-task tradeoff，但没有形成 Pareto 改善。joint camera 部分指标改善，joint human、clean camera completion 和 outscreen 有退化。当前名为 `observed_noise_matched` 的 probe 实际包含整支 random replacement 与额外噪声，不是 matched additive-noise robustness test。

Screen projection containment 的 pre-NaN best checkpoint 将 Out 降到 `0.50%`，但 FDCLaTr 达到 `350.09`、F1 为 `17.44%`、Camera Cov 为 `33.14%`，训练后续从 `175100` 起 NaN。该实验说明强 projection penalty 可以压低出屏率，但当前配方会破坏 camera distribution 和语义。

## 4. 现有问题

### 4.1 三模式统一还缺 fair baseline 闭环

V6 可以把 unified branch-mask framework 写为第一贡献，但还需要补齐：

1. joint-only specialist。
2. camera-only specialist。
3. human-only / human-mode specialists。
4. unified vs three separate models 的参数量、训练 FLOPs、wall time 和采样成本。
5. 相同 tokenizer、backbone、split、budget 和 eval batch size 的 full metrics。

只有当 unified model 在三任务平均质量接近或优于 separate models，并显著减少参数或训练维护成本时，统一框架才是强贡献。

### 4.2 Human mode 定义混杂

当前 human completion 同时包含两类问题：

| 问题                          | 条件                              | 评价重点                                                 |
| --------------------------- | ------------------------------- | ---------------------------------------------------- |
| actor recovery              | full camera + human text        | camera 是否提供有用的 root/framing posterior |
| camera-agnostic generation  | human text only                 | human semantic baseline 和解耦上界；判断 camera condition 是几何价值还是污染 |

这两者不能放在同一列里直接宣称胜负。V6 需要先固定命名，再决定哪些指标能比较。

### 4.3 Branch mask 表达 visibility，但不表达 trust

当前 mask 告诉模型哪支可见、哪支要生成，但没有表达 observed condition 的来源、质量和可信度。对于 clean GT completion，这个设定能得到高 coverage；对于 noisy / generated / missing condition，它容易错误传播。

practical completion 应写成：

```text
observed source in {clean, additive-noisy, generated, missing}
quality q in [0, 1] or discrete source token
p(target | observed, q, task text)
```

### 4.4 Raw latent concat 缺少 human→camera 方向性

`concat([z_hum,z_cam])` 的 simultaneous denoising 让 human 和 camera 在同一 denoising stream 中互相影响。由于 camera translation feature 本身依赖 human root，同步预测 human 和依赖 human 定义的 camera 存在因果方向错配。

下一步不应先在全通道 raw latent 上加 learned gate。更清晰的顺序是：先改为 human-first 生成顺序（human → camera），让 camera 的表示依赖在生成过程中得到尊重。

### 4.5 R@K 协议必须固定

Pulp / StoryMotion 的 retrieval metric 在 batch 内构造 candidate pool，因此 R@K 依赖 eval batch size。当前本地公平比较使用 b64；历史 4090 b16 和 Pulp 默认 b128 不能混入同一张 R@K 表。对外论文比较需要固定为 Pulp default b128，或实现 batch-invariant global / chunked retrieval。

## 5. V6 下一步方案

### 5.1 先做任务定义，而不是直接开新大训练

第一步输出一个 task spec：

| 决策 | 候选 | 产物 |
| --- | --- | --- |
| human mode 命名 | actor recovery / camera-agnostic generation | 两个独立 eval protocol |
| condition source | clean / additive-noisy / generated / missing | reliability train/eval matrix |
| retrieval protocol | b64 internal / b128 external / global retrieval | 固定 R@K 可比口径 |


### 5.2 Human-first joint 对照

最小实验只比较 current simultaneous 与 human-first：

```text
Stage A: text -> human
Stage B: text_camera, human -> camera
```

这是对 Pulp camera 表示依赖（`camera_translation - human_root_translation`）最直接的架构尊重：先生成 human，再生成依赖 human 定义的 camera。

成功标准：

1. joint human FDTMR、Human Cov 不低于 current simultaneous。
2. joint camera FDCLaTr、Camera Cov、F1 不低于 current simultaneous。
3. Human MPJPE 不退化。
4. Out / r_fpd 不退化。
5. Coupling pollution index 下降。

注意与 generated-camera replay 的区别：replay 测试的是 camera-first（先生成 camera 再做人），与数据因果方向相反，因此 replay 失败（与 joint 同区间）不能否定 human-first。

### 5.3 Human condition variants 对照

对同一 checkpoint 或同预算模型比较：

| 变体 | 条件 | 需要回答的问题 |
| --- | --- | --- |
| full camera | full `z_cam` + human text | full camera latent 是否提供有用的 root/framing posterior |
| no-camera | human text only | camera condition 是否带来污染，human branch 独立上界是多少 |

评价指标：Human FDTMR、TMR、R3、Human Cov、MPJPE、contact / foot sliding。

关键判断逻辑：
- 若 no-camera 语义更好但几何/coverage 显著下降：camera 的主要价值是 root/framing 约束
- 若 no-camera 全面优于 camera-conditioned：当前 camera condition 的污染 > 价值

### 5.4 Matched reliability protocol

对 clean control 与 reliability-aware model 使用完全相同的 additive noise sweep：

```text
noise_std = 0.0 / 0.05 / 0.10 / 0.15 / 0.30 / 0.50
```

禁止整支 random replacement 混入 additive-noise test。generated-condition test 单独命名，使用 joint-generated branch 作为 observed source，并报告 generated source 的质量。

成功标准：

1. clean performance 不明显低于 baseline。
2. 随 noise 增加，reliability-aware model 的 degradation slope 更小。
3. observed missing 时 text condition 能恢复控制力。
4. quality/source token 与实际 corruption strength 保持单调响应。

### 5.5 Fair unified baseline

补齐 same-budget baselines：

| baseline | 训练任务 | 用途 |
| --- | --- | --- |
| joint specialist | joint only | 检验 unified 是否损害主任务 |
| camera specialist | camera completion only | 已有第一版，需要纳入同表 |
| human specialist | human mode only | 已有第一版，需要按新 human mode 拆分 |
| three-model ensemble | 三个 specialists | 参数量 / FLOPs / wall time 上界 |
| unified model | 三任务共享 | 第一贡献主角 |

报告方式：

1. 每任务 native metrics。
2. 三任务平均 rank 或 normalized score。
3. 参数量、训练总 FLOPs、采样 latency。
4. 多 seed 或 bootstrap uncertainty。

### 5.6 Coupling diagnostics

V6 应固定一组比普通 official metrics 更直接的耦合污染指标：

```text
PI_H_from_C = degradation(H | camera condition perturbed) - degradation(H | matched control)
PI_C_from_H = degradation(C | human condition perturbed) - degradation(C | matched control)
ReplayGap_H = metric(joint_human) - metric(human_given_generated_camera)
GTCameraGain_H = metric(human_given_GT_camera) - metric(human_given_generated_camera)
```

目标不是让耦合最小，而是在 projection、human MPJPE、semantic score 和 distribution coverage 不退化的前提下降低污染性耦合。

## 6. 论文贡献边界

可以写：

1. StoryMotion 提供一个统一 branch-mask latent diffusion framework，在同一个 Pulp Stage1 latent contract 上支持 joint generation、camera completion 和 human mode。
2. 本地 mixed b64 point estimate 显示 StoryMotion clean joint 相对 Pulp Stage2 显著缩小 distribution、coverage、framing 和 outscreen gap；该结论不等价于多 seed 显著或 Pulp default b128 SOTA。
3. Pulp camera representation 显式依赖 human root，因此 human-first 生成顺序（human → camera）是下一版的核心结构假设。
4. Completion 不是单一任务，需要区分 camera-conditioned actor recovery 和 camera-agnostic human generation。
5. Practical completion 需要 condition source / quality modeling，而不是默认 observed branch 完全可靠。

暂不写：

1. 全面、统计显著超过 PulpMotion。
2. human 与 camera 已经解耦。
3. completion 已经公平超过 single-task baselines。
4. boundary schedule 或 screen projection loss 已经是最终修复。
5. source tokenizer replacement 只是缺少调参。

## 7. 最小闭环

V6 的下一轮最小闭环是：

```text
human-first joint >= current simultaneous on joint metrics
camera-agnostic human generation clarifies camera's geometric value vs pollution
matched reliability protocol improves noisy/generated/missing completion
unified model matches specialists with lower total parameter/training cost
coupling pollution index decreases without hurting official metrics
```

如果这五点成立，StoryMotion 的贡献就不只是 Pulp Stage1 + CondMDI-style mask diffusion，而是一个面向 human-camera motion 的统一、方向可控、可靠性可建模的 latent generation framework。
