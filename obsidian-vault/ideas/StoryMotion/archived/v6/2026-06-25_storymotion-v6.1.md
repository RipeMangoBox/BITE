---
title: "StoryMotion v6.1 实验闭环"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - status/active
created: 2026-06-25T00:00:00
updated: 2026-06-28T16:35:00
---

## 结论摘要

v6.1 的核心裁决：

1. **根因成立**：camera latent 的 distance block 依赖逐帧 human/root，因此 camera completion 对 observed human/root 的错误极敏感；human completion 对 observed camera 不对称地稳健。
2. **当前 Stage2 内部修复已基本试完且未解决根因**：camheavy human-first、RootHead-only root-first、neutral inference-time human-first、soft observed alpha、observed schedule boundary、text routing intervention 都不能稳定改善 joint / framing。
3. **P2b 第一版部分有效但不是解法**：bs64 full eval 显示 P2b 明显改善 additive noisy root robustness；但 clean GT-human camera completion 退化，generated-human replay 仍差，missing/root-only 仍没有可接受 framing。
4. **结论边界**：剩余“核心实验”不是再补一个小消融就能解决 coupling；若目标是解决 StoryMotion Stage2 的 human-camera latent prediction 耦合，需要进入第二版训练或结构改造：clean-preserving P2b、真实 generated-human condition 训练、或重定义 camera latent/采样方向以减少 camera 对 decoded human root 的硬依赖。
5. **外部 baseline 边界**：E.T./DIRECTOR 与 MoLingo 都按 Pulp from-scratch 协议，不使用 official checkpoint。DIRECTOR 只是 root-only camera completion adapter，后续只跑 Pulp/StoryMotion Stage2 camera metrics；MoLingo 旧 272 padded 路线作废，尚无正式 human baseline。

---

## 已验证核心事实

### C1. Stage2 生成方向错配

Pulp camera feature 的 distance block 使用逐帧世界坐标 root：

```python
human_translation = human_raw["joints"][..., 0, :3]
distance_feat = camera_translation - human_translation
camera_feat = cat([fov(2), distance(3), cam_vel_rot(9)])
distance_raw = x_distance * std + mean + human_raw.joints[..., 0, :3]
```

因此 camera latent 中的 3 维 distance block 显式依赖 decoded human root。Stage2 直接同步 denoise `concat([z_hum, z_cam])`，没有显式建模 human/root 到 camera 的依赖方向，这是 joint generation 与 completion cross-branch 污染的结构来源。

### C2. Completion reliability 未建模

训练与 eval contract 同时包含两条 observed 注入路径：

- hard replacement：`x = torch.where(obs_mask.bool(), obs_x0, x_t)`
- 显式条件：`TemporalObsUNet.forward` 将 clean `obs_x0` 与 `obs_mask` 拼接输入模型

同时历史训练中 `obs_self_condition_prob=0.0`。模型学到的是“mask=1 的 observed branch 完全可靠”，而不是根据 observed source / corruption strength 动态调信任。

### C3. Human mode 任务定义需要拆分

`camera-conditioned actor recovery`（camera + human text → human）与 `camera-agnostic human generation`（human text → human）回答不同问题，不能混成单一 “human completion” 指标列。当前 v6.1 已证明 camera condition 对 human 语义不是主要瓶颈，但 root-only / no-camera 变体仍需补齐。

---

## 实验总览

| ID          | 目标                                               | 设置                                                                 | 结果                                                                          | 结论                                                                        |
| ----------- | ------------------------------------------------ | ------------------------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| P0          | unified 是否损害 completion 质量                       | 5090 mixed b64，unified vs camera/human specialists                 | camera / human completion 均持平                                               | unified completion 守门通过；仍缺 joint-only 与成本汇总                               |
| P4.1        | 量化 cross-branch pollution                        | dependency matrix 后处理                                              | `PI_C_from_H` 远大于 `PI_H_from_C`                                             | camera 依赖 human/root 是主不对称                                                |
| P2a         | 正确 matched additive-noise 协议                     | observed branch additive noise sweep                               | camera 随 human noise 快速崩；human 对 camera noise 稳健                            | P2b 应聚焦 camera reliability                                                |
| P5          | double-injection dominance 诊断                    | soft alpha / schedule boundary / routing intervention              | alpha < 0.5 后 camera 崩；routing 近似对角                                         | inference-time 干预不够，text routing 无明显结构缺陷                                  |
| P1a         | human-first 训练捷径是否可行                             | 4090 `task_probs=[2,0,1]` camheavy fine-tune                       | camera 与 joint 全面退化                                                         | 禁用 human task 是错误实现                                                       |
| P1b         | RootHead-only root-first 是否修复 C1                 | 4090 neutral `[1,1,1]` + `root_first_weight=0.01`                  | completion human 轻退化，camera/joint 明显退化，Out 45.26%                           | 辅助 RootHead 未转化为 framing / joint 质量                                       |
| P1c         | inference-time human-first 是否有收益                 | 5090 GPU3，neutral `[1,1,1]`，先 joint 生成 human 再做 camera completion  | FDCLaTr 14.50 → 89.39；CLaTr 54.85 → 33.91；root-framing proxy 明显变差           | 当前 two-stage inference 不成立，generated human/root 质量不足会污染 camera            |
| P2b         | reliability-aware camera completion formal train + eval | 4090 训练，4090/5090 full eval，source/quality labeled corruption | additive noise 下 FCD / coverage 明显优于 neutral；clean、generated replay 退化；missing 几何仍差 | 部分有效；不能声称全面解决 coupling |
| split check | 结论是否依赖 mixed split                               | 5090 pure b64 复现 P0/P2a                                            | 趋势一致                                                                        | P0/P2a 不是 split artifact                                                  |
| P6          | GT-human TMR oracle                              | 5090 GPU0，full mixed bs64，10549 samples                            | TMR=17.71，FDTMR≈0，HCov=100%                                                 | 已完成；no-generation oracle，不是生成 baseline                                    |
| Ext-C       | E.T./DIRECTOR camera completion baseline         | 5090 隔离 clone；Pulp `traj/caption_cam/char/char_raw` root-only adapter | original / caption-shuffle / char-shuffle ckpt 已有；Pulp/StoryMotion Stage2 camera metric eval 未完成 | 训练产物存在，但无正式量化结果 |
| Ext-H       | MoLingo human baseline                           | 5090 隔离 clone `hynann/MoLingo`；目标是 Pulp 199 维 VAE 路线 | 旧 199→272 padded train/eval 作废；SAE 放弃 | 不使用 official/HumanML272 checkpoint；需重做 Pulp 199 in/out VAE contract |

---

## 实验缩写与 Setting 对照

| 缩写          | 模型 / setting                  | 训练或推理设置                                                                                                                                                                  | 目标                                         | 公平性说明                                                       |
| ----------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------ | ----------------------------------------------------------- |
| SM-normal   | 正常 StoryMotion unified        | `independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/last.pt`；三任务 neutral branch-mask training                                                                     | 主对照；P0 的 `unified_camera/human/joint`      | 所有 P1 变体都应与它在同 split、同 bs64、同 official metric 下比较           |
| HF-camheavy | human-first camheavy          | 从 SM-normal fine-tune 到 196k；`task_probs=[2,0,1]`；没有两段式 inference                                                                                                        | 测试 camera-heavy / human-task-disabled 训练捷径 | 不等同于正式 human-first factorization；不能用于否定两段式 human-first      |
| RF-roothead | RootHead-only root-first      | 从 SM-normal fine-tune 到 196k；`task_probs=[1,1,1]`；`root_first_weight=0.01`                                                                                               | 测试辅助 root supervision 是否改善 C1              | 与 SM-normal 对照较公平，但多了 fine-tune 步数和 RootHead                |
| GT-human    | GT human oracle               | dataset GT human raw motion → official HumanMetricCallback；bs64                                                                                                          | 裁决 GT-human TMR 上界                         | TMR/R@K 对 batch size 敏感，必须用 bs64 与 P0 human/joint 表对齐       |
| ET-cam      | E.T./DIRECTOR camera baseline | 隔离 clone `/data/public/ripemangobox/Motion/baselines/DIRECTOR_storymotion_20260626`；Pulp data view `/data/public/ripemangobox/Motion/baselines/data/director_pulp_mixed` | 外部 camera completion baseline              | from-scratch 训练；只用 Pulp/StoryMotion Stage2 camera metrics                     |
| ML-human    | MoLingo human baseline        | 隔离 clone `/data/public/ripemangobox/Motion/baselines/MoLingo_storymotion_20260626`；目标是 Pulp 199 维 VAE adapter | 外部 human completion baseline 待 formal 适配 | 不使用 official/HumanML272 checkpoint；不能使用 199→272 padding |

---

## P0. Unified Completion 守门

**目标**：确认 unified branch-mask model 在 completion 任务上是否接近单任务 specialist。

**设置**：5090，mixed split，b64，cfg=2.0，eta=1.0。

| model / task      | FDTMR↓ |  TMR↑ |  HCov↑ | FDCLaTr↓ | CLaTr↑ |  CCov↑ |   F1↑ |
| ----------------- | -----: | ----: | -----: | -------: | -----: | -----: | ----: |
| camera specialist |      - |     - |      - |    14.34 |  56.99 | 86.98% | 0.658 |
| unified camera    |      - |     - |      - |    14.50 |  55.62 | 87.15% | 0.654 |
| human specialist  | 125.28 | 18.24 | 84.79% |        - |      - |      - |     - |
| unified human     | 126.71 | 18.17 | 84.61% |        - |      - |      - |     - |
| unified joint     | 155.73 | 23.95 | 36.43% |    85.70 |  33.52 | 62.83% |     - |

**结论**：unified 在 camera / human completion 上与 specialist 持平，说明共享 branch-mask framework 没有破坏 clean completion。但 joint-only specialist、参数量、训练 FLOPs、wall-time 仍未补齐，因此 P0 只支持“completion 不劣”，尚不支持完整“统一框架优于三模型 ensemble”。

---

## P4.1 与 P2a. Coupling / Reliability 定位

### P4.1 PI 基线

**目标**：量化 cross-branch dependency 是否对称。

**设置**：从已有 dependency matrix 后处理；matched control 为 clean completion，perturbed 为 additive noise，不混入 random replacement。

| 指标                        |         值 | 含义                                   |
| ------------------------- | --------: | ------------------------------------ |
| PI_H_from_C (FDTMR)       |    +27.99 | observed camera 加噪使 human 轻中度退化      |
| PI_H_from_C (HumanCov)    |  −11.7 pp | human coverage 下降                    |
| PI_C_from_H (FDCLaTr)     |    +288.5 | observed human 加噪使 camera 灾难退化       |
| PI_C_from_H (CamCov)      | −56.11 pp | camera coverage 大幅下降                 |
| ReplayGap_H (FDTMR)       |     +5.03 | camera-first replay 与 joint 同区间      |
| GTCameraGain_H (HumanCov) | +47.81 pp | 正确 camera condition 对 human 几何有强约束价值 |

**结论**：耦合高度不对称，camera 对 human/root 的依赖远强于 human 对 camera 的依赖；这与源码中的 `camera_translation - human_root_translation` contract 一致。

### P2a Matched Additive-Noise Sweep

**目标**：用正确协议替代旧的 random replacement + noise 混合评估，测量 clean observed branch 被 additive noise 污染时的退化斜率。

**设置**：unified checkpoint，mixed b64，observed branch 加 `level * per-channel-std * noise`，clean 行取 P0。

| noise std | cam FCD↓ | cam CCov↑ | cam CLaTr↑ | hum FTD↓ | hum TMR↑ | hum HCov↑ |
| --------: | -------: | --------: | ---------: | -------: | -------: | --------: |
|      0.00 |     14.8 |     86.6% |       55.6 |    126.7 |    18.17 |     84.6% |
|      0.05 |     22.0 |     85.6% |       53.2 |    126.7 |    18.13 |     84.5% |
|      0.10 |     51.9 |     80.2% |       48.7 |    126.6 |    18.02 |     84.5% |
|      0.15 |     96.9 |     70.1% |       43.5 |    126.9 |    17.83 |     84.2% |
|      0.30 |    216.8 |     46.7% |       33.0 |    131.7 |    16.85 |     81.1% |
|      0.50 |    303.0 |     31.0% |       25.7 |    154.7 |    14.94 |     72.9% |

**结论**：camera completion 是脆弱支路，std=0.15 时 FCD 已从 14.8 退化到 96.9；human completion 对 observed-camera noise 基本稳健。P2b reliability-aware training 应主要服务 camera completion，对 observed human 的 source / quality 建模。

### Pure Split 复现

**设置**：5090 pure split，4053 samples，b64。

| model / task      | FDCLaTr↓ mixed/pure | FDTMR↓ mixed/pure | 主要结论                 |
| ----------------- | ------------------: | ----------------: | -------------------- |
| unified camera    |       14.79 / 23.36 |                 - | completion 持平趋势复现    |
| unified human     |                   - |   126.71 / 111.14 | completion 持平趋势复现    |
| unified joint     |       85.70 / 91.47 |   155.73 / 137.12 | joint 仍弱于 completion |
| camera noise 0.30 |       216.8 / 205.1 |                 - | camera collapse 复现   |
| human noise 0.50  |                   - |     154.7 / 134.4 | human 退化仍更温和         |

**结论**：P0/P2a 的方向性不依赖 mixed split。

---

## P5. Double-Injection 与 Routing 诊断

### Soft Observed Alpha

**目标**：评估降低 observed branch 信任强度是否能替代重训。

| `--soft-observed-alpha` | cam FDCLaTr↓ | CLaTr↑ | CCov↑ |
| ----------------------: | -----------: | -----: | ----: |
|                    0.00 |        474.2 |    8.9 |  6.6% |
|                    0.25 |         96.0 |   44.7 | 74.0% |
|                    0.50 |         16.8 |   54.4 | 86.8% |
|                    0.75 |         14.8 |   54.8 | 86.9% |
|                    1.00 |         14.8 |   55.6 | 86.6% |

**结论**：observed branch 存在约 `0.5` 的信任阈值；低于阈值 camera completion 快速崩塌。单纯削弱 observed 强度不是可靠修复。

### Observed Schedule Boundary

**目标**：评估缩短 observed conditioning 覆盖的去噪步数是否更稳。

| boundary | cam FDCLaTr↓ | CLaTr↑ | CCov↑ |
| -------: | -----------: | -----: | ----: |
|      0.3 |         70.4 |   38.1 | 70.1% |
|      0.5 |         69.5 |   39.2 | 72.5% |
|      0.7 |         64.3 |   41.1 | 74.3% |
|      0.9 |         47.1 |   45.4 | 78.3% |
|      1.0 |         14.8 |   55.6 | 86.6% |

**结论**：schedule boundary 比 alpha 退化更平滑，但 boundary=0.9 仍与 clean 有约 3 倍 FDCLaTr gap，不能替代 P2b。

### Routing Text Intervention

**目标**：区分 joint 弱是 text routing cross-talk 还是 latent branch coupling。

| intervention        | cam CLaTr↑ | hum TMR↑ | 结论                    |
| ------------------- | ---------: | -------: | --------------------- |
| clean joint         |       33.5 |    23.95 | baseline              |
| zero camera text    |       12.0 |    24.34 | camera 语义崩，human 基本不变 |
| shuffle camera text |       12.1 |    23.49 | 同上                    |
| zero human text     |       42.4 |     4.45 | human 语义崩，camera 不崩   |
| shuffle human text  |       31.6 |     6.63 | 同上                    |

**结论**：text routing 基本对角，joint 弱主要来自 latent human-camera coupling，而不是 camera/human text 串味。

---

## P1. 方向修复实验

### 正常 StoryMotion Setting

v6.1 的正常 StoryMotion 对照是 `runs/train/stage2/independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/last.pt`，使用同一 Pulp latent contract（human latent + camera relative-distance latent）、同一 official eval callback 与三任务 neutral branch-mask training。P0 中的 `unified_camera`、`unified_human`、`unified_joint` 都来自这个 setting。

对比边界：

- `human-first camheavy` 与正常 setting 不只差“方向”，还差 task distribution：它从正常 checkpoint fine-tune 到 196k，并设 `task_probs=[2,0,1]`，禁用 human-only task；没有实现 inference-time 两段式 `human → camera` sampling。因此它应解释为 **camera-heavy / human-task-disabled control**，不是正式 human-first factorization。
- `root-first` 与正常 setting 的对照更公平：同样从正常 checkpoint fine-tune 到 196k，保持 `task_probs=[1,1,1]`，唯一核心增量是 RootHead 辅助 root supervision（`root_first_weight=0.01`）。它的负结果可以视为 RootHead-only root-first 方案的有效反证。

### P1a Human-First Camheavy

**目标**：测试强化 camera / joint、关闭 human-only 任务的训练捷径是否可行。该实验不等同于正式 human-first factorization。

**设置**：4090，step=196k，`task_probs=[2.0,0.0,1.0]`，mixed b64。

| model                       | FDTMR↓ |  TMR↑ | HCov↑ | FDCLaTr↓ | CCov↑ |   Out↓ |
| --------------------------- | -----: | ----: | ----: | -------: | ----: | -----: |
| unified camera baseline     |      - |     - |     - |    14.50 | 87.2% |      - |
| human-first camheavy camera |      - |     - |     - |    84.94 | 64.7% |      - |
| unified joint baseline      | 155.73 | 23.95 | 36.4% |    85.70 | 62.8% |   7.9% |
| human-first camheavy joint  | 366.63 | 20.42 |  8.7% |   192.24 | 40.5% | 21.39% |

**结论**：该实现失败，且实现不符合原计划中的两段式 human-first。`task_probs_human=0.0` 破坏 standalone human generation，joint 与 camera completion 同时失去 human/root 锚点。该结果只能否定“禁用 human-only 任务”的训练捷径，不能否定保持 neutral training 后在 inference-time 执行 `human → camera` 两段式采样。

### P1b RootHead-Only Root-First

**目标**：在保持 neutral 三任务训练的前提下，用辅助 RootHead 显式监督 root，测试是否能修复 camera 对 human root 的依赖。

**设置**：4090，`runs/train/stage2/v6_rootfirst_20260626/last.pt`，step=196k，`task_probs=[1,1,1]`，`root_first_weight=0.01`，RootHead width=128。正式训练末段 `root_aux_loss_weighted≈0.001–0.004`，未明显压制主 loss。

| model / task | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | Out↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unified camera baseline | - | - | - | 14.50 | 55.6 | 87.1% | - |
| root-first camera | - | - | - | 65.12 | 41.55 | 69.6% | - |
| unified human baseline | 126.71 | 18.17 | 84.6% | - | - | - | - |
| root-first human | 137.80 | 18.12 | 81.0% | - | - | - | - |
| unified joint baseline | 155.73 | 23.95 | 36.4% | 85.70 | 33.5 | 62.8% | 7.89% |
| root-first joint | 264.54 | 24.65 | 15.3% | 140.63 | 19.97 | 49.9% | 45.26% |

**结论**：RootHead-only root-first 未通过 P1。它比 camheavy 更干净地保留了 human completion，但没有把 root 辅助监督转化为 camera distance / joint framing 质量，joint Out 达到 `45.26%`。后续不能只监控 training-time `root_aux_loss`，必须补 eval-time root trajectory error / framing fidelity。

### P1c Neutral Inference-Time Human-First

**目标**：不改训练，在 neutral `[1,1,1]` baseline 上做两段式采样，判断 human-first factorization 本身是否有收益。

**设置**：5090 GPU3，`runs/train/stage2/independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/last.pt`，mixed full test 10549 samples，bs64，cfg=2.0，eta=1.0。baseline 是正常 camera completion；two-stage 是先用 joint task 生成 human branch，再把 generated human branch 作为 camera completion 的 observed human condition。

| mode                     | samples | FDCLaTr↓ | CLaTr↑ |  CCov↑ | caption F1↑ | root err↓ | camera-root dist err↓ | root in-frame proxy↑ | static cam ratio↓ |
| ------------------------ | ------: | -------: | -----: | -----: | ----------: | --------: | --------------------: | -------------------: | ----------------: |
| normal camera completion |   10549 |    14.50 |  54.85 | 87.15% |       0.638 |     0.266 |                 0.226 |                0.815 |             0.214 |
| generated-human replay   |   10549 |    89.39 |  33.91 | 63.12% |       0.378 |     1.075 |                 1.028 |                0.277 |             0.096 |

**产物**：

- `stage2/metrics/v6_humanfirst_inference_20260627_gpu3/camera_baseline_full_b64.json`
- `stage2/metrics/v6_humanfirst_inference_20260627_gpu3/camera_generated_human_replay_full_b64.json`

**结论**：neutral inference-time human-first 未通过。generated human/root condition 明显污染 camera completion：FDCLaTr 从 `14.50` 升到 `89.39`，CLaTr 从 `54.85` 降到 `33.91`，root in-frame proxy 从 `0.815` 降到 `0.277`。该结果比 P1a 更直接地否定当前 checkpoint 上的 naive two-stage human-first inference，但仍不能否定未来使用更强 generated human 或 reliability-aware camera branch 的 factorization。

---

## Oracle 与未完成 Baseline

### P6. GT-Human TMR

**状态**：已完成。2026-06-26 在 5090 GPU0 用 `scripts/eval_gt_human_tmr_v61.py` 完成 full mixed bs64 eval，共 10549 samples，用时 1747.77 秒。结果写入 `stage2/metrics/v6_p6_gt_human_tmr_20260626/gt_human_mixed_b64.json`。

**目的**：直接用 dataset GT human motion 走 official HumanMetricCallback，得到 human TMR / FDTMR 的 oracle 上界，用于判断 GT-camera oracle 下 TMR 低是否只是 reconstruction-like objective 的自然结果。

**公平性约束**：TMR score / R@K 可能受 batch-local retrieval 候选池影响，GT-human 必须用 `batch-size=64` 跑 full mixed，才能与 v6.1 的 P0 `unified_human`、`unified_joint`、specialist human 表格公平对比。smoke 结果只用于接口验证，不进入结论表。

| source          | batch | samples | FDTMR↓ |  TMR↑ |  HCov↑ |   R1↑ |    R2↑ |    R3↑ | mm distance↓ |
| --------------- | ----: | ------: | -----: | ----: | -----: | ----: | -----: | -----: | -----------: |
| GT-human oracle |    64 |   10549 |  ~0.00 | 17.71 | 100.0% | 9.73% | 16.40% | 21.97% |        49.60 |

**解释**：GT-human 使用 PulpMotion dataset 的真实 human raw input，不经过生成，因此 FDTMR、coverage、precision、recall、density 接近理想值。TMR=17.71 与 `unified_human` 的 18.17、human specialist 的 18.24 同量级，说明当前 generated human 的 TMR 分数没有被 GT-camera condition 大幅压制；StoryMotion 的主要缺口仍在 joint coverage、framing 与 camera-human coupling，而不是单纯 human text semantic score。

### E.T./DIRECTOR Camera Completion Baseline（legacy tombstone）

**2026-07-16 清理裁决**：这一节原先记录的旧 root-only/shuffle 训练、test-as-validation checkpoint，以及把 StoryMotion checkpoint 错标为 `et_director` 的推理结果均不再是实验资产。相关 run、派生 shuffle data view、JSON/records/logs/marker 与废弃 adapter scaffold 已从 5090 删除；本归档不再保留旧 checkpoint 路径或指标，防止被重新加入表格。

当前唯一可用的 Director-C baseline 状态、合同与结果入口改由 [[2026-07-16_storymotion-v739-v741-core-experiment-decision]] 管理：train-only derived dev、shuffle DataLoader、fixed-budget endpoint、GT-H 加 camera text、owning official callback。其 prelaunch N20 只作 non-promotable bridge gate；只有 corrected endpoint 的 formal pure4053 row 才能进入 baseline 表。

### MoLingo Human Baseline

**状态**：未完成 formal human baseline training/eval。2026-06-26 已在 5090 隔离 clone `https://github.com/hynann/MoLingo` 到 `/data/public/ripemangobox/Motion/baselines/MoLingo_storymotion_20260626`，并配置 `molingo-pulp-cu128` 环境。torch 按用户要求使用 `pip install torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128`。

**训练协议**：from scratch on Pulp dataset，不使用 official MoLingo checkpoint，不使用 HumanML272 pretrained ckpt。v6.1 早期的 `HumanML3D_272` / 199→272 zero padding 路线已判为不合格适配，不能再作为 train/eval 证据。合法路线是只使用 MoLingo 的 VAE 思路/模块，在 Pulp `smpl_rifke` 199 维 data 上重训练，input/output 都保持 Pulp 199 维 contract。

因 PulpMotion human text 为 sequence level，缺乏 frame-level label，因此不进行 SAE 适配。

**脚本边界**：旧 `_private/storymotion_baselines/run_molingo_pulp_train.sh`、`export_pulp_to_molingo272.py` 等 272 padding 路线只保留为历史错误路径，不应再运行。后续需要新建 Pulp 199 in/out 的 VAE adapter 脚本，并先通过 shape / round-trip / sentinel smoke。

**风险**：zero padding 会让 MoLingo 主模型学习恒定零维，且把 HumanML272 的 layout、normalization、转置假设带入 Pulp 输出。该 baseline 只有在完成 Pulp 199 in/out VAE smoke、Pulp/StoryMotion human metric 接口与必要训练后，才能写成 StoryMotion human completion baseline。

## P2b. Reliability-Aware Camera Completion

**目标**：P2b 不是单纯提高 clean GT-human camera completion，而是降低 camera 对 noisy / generated / missing human root condition 的退化斜率。P2a 已证明当前 camera branch 把 observed human/root 当成高可信条件，std=0.15 时 FDCLaTr 已从约 `14.8` 退化到约 `96.9`，std=0.30 / 0.50 时进一步退化到约 `216.8` / `303.0`。

**最小实现**：

- 在 camera completion branch 的训练中加入 observed human corruption curriculum，覆盖 clean GT root、加噪 GT root、generated root、missing / root-only fallback。
- 显式输入 source / quality 标签：source 可设为 `gt`、`noisy_gt`、`generated`、`missing/root_only`；quality 可设为连续 noise level 或离散 bin，例如 `0`、`0.05`、`0.10`、`0.15`、`0.30`。
- source one-hot + quality scalar 先映射为小 embedding，拼到 timestep / text / task embedding 或 UNet condition embedding；FiLM gating 可作为第二版，不应作为第一版复杂化入口。
- loss 仍以 camera latent denoising 为主，同时记录 decoded root / camera framing sanity metrics。

**为什么预计有效**：当前训练 contract 通过 hard replacement 与 `obs_x0 + obs_mask` clean condition 让模型学到“observed branch 完全可信”。P2a 的退化曲线说明错误 root 会直接污染 camera distance block；RootHead-only 失败说明只监督 root 不足以改善 framing。P2b 直接把 observed condition 的可靠性作为可见变量，使模型在高质量条件下信任 root，在低质量或 missing 条件下回退到 camera/text prior 与平滑 trajectory。

**必须消融**：clean baseline、noisy observed eval、无标签 noisy augmentation、source/quality labeled P2b、generated-human condition、caption shuffle、char shuffle、fixed caption / fixed root 诊断。可加 oracle reliability 或固定阈值 gating 作为上限/简化对照，但不能用它替代训练时 labeled corruption curriculum。

**必须报告**：metric vs noise level degradation slope、camera FDCLaTr / CLaTr / coverage、decoded root trajectory error、camera distance consistency、outscreen / framing fidelity、static camera ratio、root in-frame ratio。完整 PulpMotion `FDframing / Out-rate / MPJProjPE` 需要 joint/full projection pipeline；root-only adapter 只能先报告 root-framing proxy。

### P2b Formal Train

**状态**：formal train 已完成，matched robustness eval 主体已完成。

**设置**：4090 GPU0，`runs/train/stage2/v6_p2b_reliability_20260627/gpu0_p2b_labeled_neutral_146k_to196k`。从 neutral checkpoint `independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/last.pt` 的 step `146000` resume，fine-tune 到 `196000`，bs64，`task_probs=[1,1,1]`。P2b corruption curriculum 使用：

- `--p2b-enable`
- `--p2b-prob 1.0`
- `--p2b-noise-levels 0 0.05 0.10 0.15 0.30`
- `--p2b-missing-prob 0.2`

**实现边界**：第一版 source / quality condition layout 是 `[gt, noisy_gt, generated_reserved, missing, quality]`。已实现 `gt`、`noisy_gt`、`missing`；`generated_reserved` 保留标签位，但 formal train 中未默认在线生成 human condition，避免每步额外 joint sampling 使训练成本失控。generated-human condition 需要在后续 eval 或第二版训练中补。

**训练完成证据**：

- `last.pt` 已写出：`runs/train/stage2/v6_p2b_reliability_20260627/gpu0_p2b_labeled_neutral_146k_to196k/last.pt`
- `train_log.jsonl` 共 626 行。
- 末步 train：step `196000`，loss `0.0148`，camera loss `0.0081`，human loss `0.0101`，joint loss `0.0282`。
- 末步 eval：loss `0.0258`，camera loss `0.0176`，human loss `0.0074`，joint loss `0.0526`。
- 末步 test：loss `0.0319`，camera loss `0.0332`，human loss `0.0089`，joint loss `0.0535`。
- 训练日志中 `p2b_selected_frac`、`p2b_noisy_frac`、`p2b_missing_frac`、`p2b_quality_mean` 持续非空，说明 source/quality labeled corruption 实际进入训练。

**运行状态**：4090 GPU0 formal train 已完成；2026-06-28 已用 4090 / 5090 跑完 P2b 与 neutral matched robustness eval 主体。P2b checkpoint 已从 4090 同步到 5090 供评测复用。

**eval loader 修正**：原 `storymotion_official_full_eval.py` 不能直接评测 P2b checkpoint，因为 `load_stage2` 未按 `reliability_cond_dim=5` 实例化 `TemporalObsUNet`，也没有向 sampler 传 `reliability_cond`。2026-06-28 已补丁：

- checkpoint meta 中 `p2b_reliability.enabled` 或 args `p2b_enable` 为真时，实例化 `TemporalObsUNet(..., reliability_cond_dim=5)`。
- eval-time condition layout 与训练一致：`[gt, noisy_gt, generated, missing, quality]`。
- clean camera completion 使用 `[1,0,0,0,0]`；observed noise level `L` 使用 `[0,1,0,0,L]`；missing / zero observed human 使用 `[0,0,0,1,1]`；generated-human replay 使用 `[0,0,1,0,1]`。
- neutral checkpoint 无 `reliability_mlp` 时不传 reliability condition。

**matched robustness eval**：full mixed test，10549 samples，cfg=2.0，eta=1.0，seed `20260613`，noise seed `20260624`。2026-06-28 已把 P2b checkpoint 同步到 5090，并补齐关键 P2b 条件的 bs64 eval。下表只保留与裁决直接相关的 bs64 行；早期 b32 结果仅作历史 smoke / OOM 记录，不进入核心结论。

| model | condition | batch | FDCLaTr↓ | CLaTr↑ | CCov↑ | camera-root dist err↓ | root in-frame proxy↑ | static cam ratio↓ |
| ---- | ---- | ----: | ----: | ----: | ----: | ----: | ----: | ----: |
| neutral | clean | 64 | 14.50 | 54.85 | 0.871 | 0.226 | 0.815 | 0.214 |
| P2b | clean | 64 | 88.84 | 27.82 | 0.622 | 0.656 | 0.397 | - |
| P2b | noise 0.05 | 64 | 28.24 | 42.47 | 0.778 | 0.296 | 0.676 | 0.178 |
| neutral | noise 0.15 | 64 | 96.87 | 43.54 | 0.701 | 0.231 | 0.781 | 0.072 |
| P2b | noise 0.15 | 64 | 30.36 | 40.73 | 0.777 | 0.290 | 0.689 | - |
| neutral | noise 0.30 | 64 | 216.79 | 32.96 | 0.467 | 0.266 | 0.731 | 0.022 |
| P2b | noise 0.30 | 64 | 46.84 | 38.96 | 0.750 | 0.320 | 0.646 | 0.144 |
| neutral | noise 0.50 | 64 | 303.02 | 25.68 | 0.310 | 0.302 | 0.664 | 0.007 |
| P2b | noise 0.50 | 64 | 66.38 | 34.56 | 0.702 | 0.330 | 0.617 | - |
| neutral | missing / zero | 64 | 1044.19 | 4.36 | 0.004 | 1.181 | 0.240 | 0.000 |
| P2b | missing / zero | 64 | 234.88 | 19.44 | 0.300 | 1.116 | 0.235 | 0.119 |
| neutral | generated-human replay | 64 | 89.39 | 33.91 | 0.631 | 1.028 | 0.277 | 0.096 |
| P2b | generated-human replay | 64 | 110.60 | 17.33 | 0.486 | 1.320 | 0.234 | - |

**结果裁决**：

- P2b 对 additive noisy observed human/root 的 FDCLaTr / coverage 退化斜率明显有效：noise 0.15、0.30、0.50 的 FDCLaTr 分别从 neutral `96.87 / 216.79 / 303.02` 降到 `30.36 / 46.84 / 66.38`，coverage 从 `0.701 / 0.467 / 0.310` 升到 `0.777 / 0.750 / 0.702`。
- P2b 不是 clean improvement：clean FDCLaTr 从 neutral `14.50` 退化到 `88.84`，CLaTr 从 `54.85` 降到 `27.82`，root in-frame proxy 从 `0.815` 降到 `0.397`。这说明 reliability fine-tune 牺牲了 clean GT-human camera completion。
- P2b 对 missing / zero observed human 只在分布指标上部分有效：FDCLaTr `1044.19 -> 234.88`、coverage `0.004 -> 0.300`，但 camera-root distance error 仍约 `1.116`，root in-frame proxy 仍约 `0.235`，没有形成可接受 framing。
- P2b 对 generated-human replay 仍失败：FDCLaTr 从 neutral replay `89.39` 退化到 `110.60`，CLaTr 从 `33.91` 降到 `17.33`，root in-frame proxy 从 `0.277` 降到 `0.234`。第一版训练中 `generated` 标签只是 reserved，未在线训练 generated-human condition，这个结果符合风险预期。
- 因此 P2b 的正式表述应是：**labeled reliability training partially improves robustness to additive noisy observed human/root, but degrades clean and generated-human conditions and does not solve missing/framing geometry**。

**剩余核心实验边界**：no-label noisy augmentation 只能回答“收益是否来自标签”，不能单独解决 coupling。真正可能继续解决 Stage2 human-camera latent prediction 耦合的剩余实验只剩三类：clean-preserving P2b v2（降低 corruption 概率、加入 clean preservation loss）、generated-human-aware P2b v2（训练时真实喂 generated root，而非 reserved label）、结构性解耦（重定义 camera latent 或两阶段/因子化采样，使 camera 不再硬依赖错误 decoded root）。多 seed、bootstrap、完整 `FDframing / Out-rate / MPJProjPE` 是可信度和指标闭环，不是新的修复机制。

## TMR 与 Human 可视化质量冲突

**现象**：joint human 可视化质量可能不如 human completion，但 TMR 更高；GT-human oracle 的 TMR 也不高，甚至与 generated human completion 同量级。该现象不能直接解释为 joint 更好，也不能把 TMR 当作 trajectory error。

**优先审计**：

- TMR 是否 batch-local retrieval，bs64 / b128 是否混用。
- generated / GT human 输入 TMR encoder 前是否同一 feature layout、同一维度裁剪、同一 mask 与同一 normalization。
- 是否走了同一 canonicalize / de-canonicalize / global-root 处理。
- human completion 与 joint mode 的 text、camera condition、root/global 坐标是否对齐。
- GT-human oracle 是否与 generated output 走完全相同 metric preprocessing。
- TMR 与 skeleton visual quality、contact quality、root-camera framing quality 的相关性是否足够；若相关性弱，TMR 只能作为 text-motion embedding alignment 辅助指标。

**审计通过后的谨慎解释**：strong camera condition 可能压缩 text-motion semantic diversity，使 GT / human completion 在 embedding retrieval 中不占优但几何更好；joint mode 可能更贴近 text embedding，却有局部 skeleton/contact/framing 问题。因此后续裁决不能只看 TMR，必须并列 visual、root、framing 与 contact sanity。

---

## 当前裁决

### 已成立

- C1 的源码根因成立：camera distance block 依赖逐帧 world root。
- C2 的 double-injection / reliability 问题成立：observed branch 被训练成完全可信条件。
- Unified completion 不劣于 specialist completion。
- Joint 弱不是 text routing cross-talk，而是 latent human-camera coupling 与 observed reliability 的问题。
- P2b 对 additive noisy observed human/root 的 camera distribution robustness 部分成立，尤其 noise 0.15 / 0.30 / 0.50 的 FDCLaTr 与 coverage 在 bs64 下明显优于 neutral。

### 未成立

- camheavy human-first 不是有效 P1 实现。
- 当前 RootHead-only root-first 不是有效 P1 修复。
- neutral inference-time human-first 不是有效 P1 修复。
- P0 还不能完整支持 unified framework 的成本优势；缺 joint-only specialist 与成本表。
- P3 / C3 还未完全裁决；缺 no-camera 与 root-only human variants。
- P2b 不能声称全面有效：clean GT-human camera completion 明显退化；generated-human replay 退化；missing / zero 只改善 FDCLaTr 和 coverage，root-framing proxy 仍差。
- E.T. root-only camera completion baseline 尚未形成正式量化结果；original / caption-shuffle / char-shuffle training ckpt 已有，但 Pulp/StoryMotion Stage2 camera metric eval 未完成。
- MoLingo human baseline 尚未形成正式结果。

### 剩余核心实验

能继续尝试解决 Stage2 human-camera latent prediction coupling 的核心实验只剩：

1. **Clean-preserving P2b v2**：降低 corruption 概率，加入 clean preservation loss 或 clean replay regularization，目标是在保持 clean FDCLaTr≈14–15 的同时保留 noisy robustness。
2. **Generated-human-aware P2b v2**：训练时真实使用 generated human/root condition，而不是只保留 `generated` 标签位，目标是修复 generated-human replay 退化。
3. **结构性解耦**：重定义 camera latent（减少或替代 `camera_translation - human_root_translation` 的硬绑定）、显式 root/camera factorization，或训练真正的 two-stage `human/root → camera` 模型。这个方向才可能从根上降低 joint generation 的 cross-branch pollution。

不再视为“解决 coupling”的核心实验：

- no-label noisy augmentation：只用于确认 P2b 收益是否来自 source / quality 标签。
- TMR metric audit：只裁决指标可信度，不修复生成。
- DIRECTOR / MoLingo：是外部 baseline，不修复 StoryMotion Stage2。
- P0 cost / joint-only specialist：只闭环统一框架论证，不修复 coupling。

### 同步状态

2026-06-28 已同步 P2b eval 必需代码与结果：4090 的 P2b checkpoint 已同步到 5090，`last.pt` / `best_eval.pt` SHA256 一致；4090/5090 的 P2b 与 neutral robustness JSON 已双向同步。5090 已补齐 P2b clean、noise 0.15、noise 0.50、generated-human replay 的 bs64 rerun，四个 `*5090rerun.json` 在 4090/5090 SHA256 一致。为评测 P2b，5090 StoryMotion 的 `scripts/train_stage2_condmdi_pulp.py` 已备份为 `scripts/train_stage2_condmdi_pulp.py.backup_before_p2b_eval_20260628` 后同步为 4090 的 P2b-capable 版本；该 repo 仍是 dirty worktree。DIRECTOR repo 曾为 official eval 修复新增 `src/__init__.py`、`src/training/__init__.py`、`src/training/losses/__init__.py`，但当前 StoryMotion 路线不再需要 E.T. official CLaTr eval。

### 当前机器状态

2026-06-29 复核：MoLingo `pulp199pad272` 相关 train/eval 不再作为有效状态记录，5090 / 本机对应污染产物应删除或隔离。DIRECTOR original / caption-shuffle / char-shuffle training ckpt 已完成；下一步是 Pulp/StoryMotion Stage2 camera metric eval，不是 DIRECTOR official CLaTr eval。

---

## 协议约束

- 当前所有训练结果仍是单 seed point estimate；论文中不能写“显著改善”，除非补多 seed 或 bootstrap uncertainty。
- 当前 b64 与 Pulp 默认 b128 的 R@K 不可直接混表；TMR score / R@K 是 batch-local retrieval，需要统一 batch size 或实现 global/chunked retrieval。v6.1 内部公平对比统一使用 bs64；GT-human oracle 与 P2b 关键 rerun 已按 bs64 完成。
- P2b 早期 b32 结果只作为历史记录；核心裁决使用 5090 bs64 rerun。
- PI 与 P2a 必须使用 additive noise protocol；random replacement 应作为单独 robustness intervention，不可混入 matched-noise 曲线。
- P1 后续训练必须保持 human-only 能力，不能再用 `task_probs_human=0.0` 作为 human-first 近似。
