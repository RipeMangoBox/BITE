---
title: "StoryMotion v7.2 Stage2 正式设计"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - architecture
  - status/active
aliases:
  - StoryMotion-v7.2-stage2
hypothesis: |
  v7.2 以 v7 为标准，不重训 Stage1、不切换 Rectified Flow、不推倒 CondMDI UNet 主干。正式改动只吸收有益的具体化：TextRoleRouter、source metadata TrustGate、soft observed conditioning、relation surrogate/probe、可选 stop-gradient ablation，以及统一实验编排。Full two-path human-first、hard R-only bottleneck、JOINT asymmetric noise 和固定 D_R 阈值不进入默认主线，只作为后续 ablation。
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
created: 2026-07-02T01:00:00+0800
updated: 2026-07-02T11:25:00+0800
---
# StoryMotion v7.2 Stage2 正式设计

## 0. 裁决

v7.2 是 v7 的工程化版本，而不是另起炉灶。

保持不变：

- Stage1 固定使用 Pulp official checkpoint/cache。
- Stage2 继续基于当前 CondMDI UNet 主干。
- diffusion 仍使用现有 DDPM/DDIM-style START_X 训练与采样。
- 三任务仍是 `JOINT / H2C / C2H`。
- 输入文本只有 `e_c` camera text 和 `e_h` human text。

默认新增：

- `TextRoleRouter`：按任务显式切换主文本与辅助文本。
- `SourceEncoder + TrustGate`：observed source 不再 hard replacement，而是 soft conditioning。
- `ReliabilityEncoder`：显式接收 `source_type / sigma / root_drift / mask_ratio`。
- `RelationSurrogate`：从 source latent / projection surrogate 中提取低维 relation condition，默认不做 R-only bottleneck。
- `latent decoupling probe`：作为诊断，不作为硬阈值证明。
- `v7.2 experiment manifest / launcher`：把高优先级实验拆成互不覆盖的配置与输出目录。

默认不新增：

- Full two-path human-first denoising。
- `z_h_pred.detach()` 作为不可选硬契约。
- `D_R=64` 这类固定 relation bottleneck。
- JOINT asymmetric noise `delta_t=100`。
- Rectified Flow。

这些项只保留为后续 ablation。

## 1. 输入与任务契约

```text
e_c: camera text embedding, 512 dims
e_h: human text embedding, 512 dims
e = concat([e_c, e_h]), 1024 dims
```

| task | source | dominant text | auxiliary text | output | default route |
| --- | --- | --- | --- | --- | --- |
| `JOINT` | none | `e_h` and `e_c` | none | `H_hat, C_hat` | 双文本联合生成 |
| `H2C` | `H_source` | `e_c` | `e_h` | `C_hat` | camera text 主导，human source 提供结构条件 |
| `C2H` | `C_source` | `e_h` | `e_c` | `H_hat` | human text 主导，camera source/text 提供 view/framing constraint |

`H2C` 的目标不是“由 human text 生 camera”，而是：

```text
camera text + observed/generated/noisy human source -> camera
```

这点必须通过 camera text shuffle / zero / wrong-text intervention 验证。

## 2. Stage2 模块

### 2.1 CondMDI UNet 主干保留

当前主干的问题不是容量，而是条件注入：

```python
x = torch.where(obs_mask.bool(), obs_x0, x_t)
```

v7.2 保留 UNet blocks，但把 observed source 改成可控 soft conditioning：

```text
x_obs = x_t + trust_gate(q) * obs_mask * (obs_x0 - x_t)
model_input = concat([x_obs, obs_mask])
cond = timestep + TextRoleRouter(e_c, e_h, task) + Source/Relation condition
```

若 `trust_gate(q)=1`，退化为旧 hard inject；若 gate 降低，模型必须更多依赖 dominant text 和 camera/global prior。

### 2.2 TextRoleRouter

```text
H2C:
  main = e_c
  aux  = e_h

C2H:
  main = e_h
  aux  = e_c

JOINT:
  main = e_h + e_c
```

实现上先用低风险线性路由：

```text
routed_text = concat([scale_c(task) * e_c, scale_h(task) * e_h])
```

其中 `H2C` 的 `scale_c` 必须不低于 `scale_h`，`C2H` 相反。后续如果 text intervention 仍弱，再换 cross-attention 级别路由。

### 2.3 TrustGate 与 source metadata

`reliability_meta`：

```text
source_type: gt / noisy_gt / generated / missing
sigma: observed source corruption level
root_drift: optional root drift estimate
mask_ratio: observed branch density
```

第一版使用 global scalar gate：

```python
gate = sigmoid(MLP(reliability_meta))
```

训练时 gate 不应被强制 clean 恒等于 1；只要求大体单调：

```text
clean gt source       -> higher trust
noisy / generated     -> lower or adaptive trust
missing               -> near-zero source trust
```

### 2.4 RelationSurrogate

RelationSurrogate 是 `R` 的轻量版本，不是强瓶颈：

```text
R = MLP(pool(source latent under obs_mask))
```

后续可加入 projection surrogate：

```text
projected bbox center / scale / visible joint ratio / camera-human distance
```

默认 camera path 仍能读取 gated source tokens，避免 R-only bottleneck 破坏 clean H2C。

### 2.5 Optional ablations

| ablation | default | purpose |
| --- | --- | --- |
| stop-gradient source/relation | off | 判断 camera loss 是否污染 human/source path |
| R-only bottleneck | off | 判断 strict relation bottleneck 是否改善 noisy source |
| task-text CLIP latent | off | 判断 MotionLab-style task instruction 是否降低 mode conflict |
| JOINT asymmetric noise | off | 判断不同 denoise uncertainty 是否有用 |
| full two-path human-first | off | 最后级别 ablation，非主线 |

## 3. 高优先级实验

前六个实验按冲突风险从低到高排列。每个实验写入独立 output dir，不共享 checkpoint 写入路径。

| id | priority | experiment | code change | train/eval target | output rule |
| --- | ---: | --- | --- | --- | --- |
| E0 | P0 | baseline replay / command freeze | no model change | 复现 v6.4 clean/noisy/text failure | read-only eval output |
| E1 | P0 | TextRoleRouter only | text routing + task embedding | H2C camera text intervention 变敏感，clean 不大跌 | `runs/train/stage2/v7_2/e1_text_role_*` |
| E2 | P0 | SoftSource + TrustGate | soft observed replacement + metadata gate | noisy `H_source` 退化斜率下降 | `runs/train/stage2/v7_2/e2_soft_trust_*` |
| E3 | P1 | Source reliability finetune | E2 checkpoint + source corruption schedule | clean/noisy Pareto | `runs/train/stage2/v7_2/e3_reliability_*` |
| E4 | P1 | RelationSurrogate | E3 checkpoint + source pooled relation condition | Out/SRE/projection 指标改善且 clean/noisy 不退化 | `runs/train/stage2/v7_2/e4_relation_*` |
| E5 | P1 | TrustGate ablation | correct tag vs wrong tag vs no tag, multi timestep/sigma probe | 证明 gate 不是装饰变量 | `runs/eval/stage2/v7_2/e5_trust_ablation_*` |

延后实验：

| id | reason to delay |
| --- | --- |
| task-text CLIP latent | 只有 E1-E4 后仍 mode conflict 才做 |
| stop-gradient / R-only bottleneck | 只有 E4 显示 source path 仍过度耦合才做 |
| full two-path human-first | 只有 E1-E5 全部无法解决 noisy/text 三联症状才做 |
| Rectified Flow | v7.2 不做 |

## 4. 判据

每个 checkpoint 必须输出：

| eval | condition | required readout |
| --- | --- | --- |
| clean oracle | clean GT source | clean H2C 不显著差于 v6.4 |
| noisy source | sigma `0.05/0.10/0.15/0.30` | degradation curve |
| generated replay | external human prior / replay cache | reliability under generated source |
| text intervention | shuffle/zero/wrong dominant text | dominant text 是否真的控制输出 |
| trust probe | correct/wrong/no source tag | gate 是否有可测作用 |

硬性停止：

- E1 clean H2C F1 低于 v6.4 20% 以上：先修 text/source injection，不进入 E2。
- E3 noise `0.15` 仍接近 v6.4 collapse：检查 hard shortcut 是否残留，不换 RF。
- E4 relation 改善 Out 但 FDCLaTr/F1 大崩：RelationSurrogate 不进入主方法。
- E5 correct/wrong/no tag 无差别：TrustGate 只是装饰变量。

## 5. 实验落地原则

为了防止 6 卡实验互相冲突：

1. 每个实验有固定 `experiment_id` 和唯一 output dir。
2. 训练、eval、probe 输出分目录，不覆盖。
3. E0-E5 使用统一 manifest 生成命令，避免手写命令漂移。
4. 代码默认保持旧行为；只有显式 `--v72-*` 参数才启用新路径。
5. 所有 checkpoint meta 记录 `v72_config`。
6. DS Max 审核通过后再启动正式长训。

## 6. 代码落地映射

| design item | implementation | default |
| --- | --- | --- |
| TextRoleRouter | `scripts/train_stage2_condmdi_pulp.py --v72-text-role-router --v72-aux-text-scale` | off |
| soft observed source | `--v72-soft-source` | off |
| TrustGate + metadata | `--v72-trust-gate`, `source_type/sigma/root_drift/mask_ratio` | off |
| RelationSurrogate | `--v72-relation-surrogate` | off |
| E0-E5 manifest | `configs/storymotion_v72_experiments.json` | command source |
| conflict-free launcher | `scripts/launch_storymotion_v72_experiments.py` | dry-run unless `--execute` |
| TrustGate probe | `scripts/storymotion_v72_trust_probe.py` | E5 only |

所有 v7.2 开关默认关闭；不带 `--v72-*` 的训练应保持旧 CondMDI 行为。

`E3` 和 `E4` 在 manifest 中显式写入 `depends_on/base_checkpoint`，launcher 在 `--execute` 模式会检查 checkpoint 是否存在，避免误从头训练。`E5` 默认做 `3 timesteps x 3 sigmas x 2 tasks` 的 gate/loss probe。

## 7. 正式版本一句话

```text
StoryMotion v7.2 keeps the v7 boundary: fixed Pulp Stage1, existing CondMDI UNet, and diffusion training. It only adds task-aware text routing, soft source trust gates, and lightweight relation conditioning, with strict experiment isolation for E0-E5.
```
