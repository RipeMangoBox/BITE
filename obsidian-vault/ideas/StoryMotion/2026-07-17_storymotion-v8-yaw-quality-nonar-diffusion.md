---
title: "StoryMotion v8: Yaw-Stable Representation, Curated Pulp, and Non-AR Diffusion"
status: active
hypothesis: |
  v7.14 的长序列 Stage1 几何退化主要由 yaw-velocity 积分误差造成，而不是 local-joint reconstruction 或 64-frame crop。v8 应先用 matched non-causal Stage1 几何监督修复 heading，再独立验证数据清洗，最后比较非自回归 latent diffusion；在 Stage1 gate 通过前，v7.14 与 v7.38 仍分别是实现和 formal 主线。
tags:
  - StoryMotion
  - v8
  - stage1
  - stage2
  - data-curation
  - diffusion
  - status/active
aliases:
  - StoryMotion-v8
  - StoryMotion-v8-Yaw-Quality
source_notes:
  - "[[version]]"
  - "[[history]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[2026-07-17_storymotion-stage1-length-condmdi-causal-priority]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
source_papers:
  - "[[analysis/NEURIPS_2025/TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_Generation]]"
  - "[[analysis/ECCV_2024/Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/ICCV_2025/InfiniDreamer_Arbitrarily_Long_Human_Motion_Generation_via_Segment_Score_Distillation]]"
  - "[[analysis/CVPR_2025/EnergyMoGen_Compositional_Human_Motion_Generation_with_Energy_Based_Diffusion_Model_in_Latent_Space]]"
  - "[[analysis/ICCV_2023/TMR_Text_to_Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis]]"
  - "[[analysis/ICLR_2025/Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning]]"
  - "[[analysis/arxiv_2026/Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval_via_Pyramidal_Shapley_Taylor_Learning]]"
  - "[[analysis/arxiv_2026/MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval]]"
created: 2026-07-17T16:25:00+0800
updated: 2026-07-18T14:44:45+08:00
---

# StoryMotion v8: Yaw-Stable Representation, Curated Pulp, and Non-AR Diffusion

> [!abstract] v8 裁决
> v8 已以 candidate family 开启，但没有替换主线。v8.0 的 pure4053 owning-decoder oracle 已把 Stage1 长序列问题定位到累计 heading：注入 GT yaw velocity 后，193–256 帧 root-aligned/global MPJPE 从 `132.22/429.43 mm` 降到 `8.68/38.99 mm`；注入全部 GT root channels 后为 `8.68/8.68 mm`。因此第一可训练 treatment 是同一 human199 上的累计 yaw/root geometry loss，而不是先换 Stage2、先删数据或直接改 feature layout。数据清洗和非自回归 diffusion 必须作为后续独立轴进入。

## 1. v8 的边界

- corrected v7.14 camera14 joint AE 仍是 StoryMotion Stage1 实现主线，v7.38 L0 clean 105k 仍是 Stage2 formal 主线；v8 candidate 通过下述 gate 前不能覆盖它们。
- StoryMotion v8 的 Stage1、cache、Stage2、checkpoint load 与 eval 全部保持 `is_causal is False`。standalone native MotionStreamer 例外不进入 v8 cache、Unified 或 promotion。
- v8 final Stage1 使用完整 ordered `162,760` train IDs、`500` epochs、约 `81.38M` sample exposures；短 screen 必须显式标成 screen，不能按 matched endpoint 晋级。
- representation、data curation、Stage2 backbone 三个轴分开。不得用一个 run 同时更换 clean manifest、human feature layout 与 denoiser，再宣称单变量收益。
- Stage1 必报 root-aligned/global MPJPE、root ADE/FDE、integrated-yaw geodesic、camera Cam-ADE/Cam-FDE/rotation，并按 `1–64`、`65–128`、`129–192`、`193+` 分桶。

## 2. v8.0：长序列误差的根通道归因

### 2.1 为什么 temporal convolution 仍会随长度恶化

Pulp human199 的前四维是 `root_z`、local root XY velocity 与 yaw velocity。owning decoder 先对 yaw velocity 做 `cumsum`，再用累计 heading 把每帧 local XY velocity 旋到世界系，最后积分 root XY。卷积本身可以接收任意长度，并不意味着每帧极小 heading bias 不会在 decoder 中累积。

现有 root-aligned MPJPE 只减去 root translation，并不做 yaw Procrustes alignment。因此它保留全身 heading error；此前把它直接解释成“local pose 变差”并不准确。local-joint channel oracle 与 baseline 完全相同，是因为 owning SMPL body-model decode 主要由 pose6D 与 root 驱动，human199 的 `136:199` local-joint channels 不直接决定最终 SMPL joints。

### 2.2 pure4053 oracle 结果

artifact：

`/data/public/ripemangobox/Motion/StoryMotion/runs/stage1/v8_0_representation_oracle_audit_20260717/eval/pure4053_human_channel_oracles.json`

artifact SHA256=`74fe8234da7c62a2a6b85c0258f228d267259263f33d52c31bd636b3360edd6c`。评测覆盖同一 pure4053 ordered IDs，使用 v7.14 checkpoint/owning decoder；oracle 只在 normalized human199 feature 中替换声明通道后解码，是 sensitivity attribution，不是可训练结果。

| version / run | treatment | overall root-aligned MPJPE mm | overall global MPJPE mm | root ADE / FDE mm | 193–256 root / global mm | root / global slope mm per 100f |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | true reconstruction | 80.73 | 212.74 | 169.64 / 415.43 | 132.22 / 429.43 | +29.02 / +145.30 |
| v8.0 / `v8_0_representation_oracle_audit_20260717` | GT root height only | 80.73 | 211.29 | 167.45 / 399.66 | — | — |
| v8.0 / `v8_0_representation_oracle_audit_20260717` | GT root XY velocity only | 80.73 | 210.74 | 165.87 / 411.13 | — | — |
| v8.0 / `v8_0_representation_oracle_audit_20260717` | GT yaw velocity only | 11.96 | 28.00 | 22.49 / 67.46 | 8.68 / 38.99 | −3.69 / +4.85 |
| v8.0 / `v8_0_representation_oracle_audit_20260717` | GT all root channels | 11.96 | 11.96 | 0.00 / 0.00 | 8.68 / 8.68 | −3.69 / −3.69 |
| v8.0 / `v8_0_representation_oracle_audit_20260717` | GT local-joint channels | 80.73 | 212.74 | 169.64 / 415.43 | — | — |
| Pulp released / `aemmardm-xgmj0yjj-325` | true reconstruction | 80.25 | 181.05 | 150.15 / 595.96 | 78.03 / 186.65 | −7.00 / −10.34 |

结论强度固定如下：

1. v7.14 的 length-dependent root-aligned/global error 对 yaw channel 极敏感；heading 是第一责任通道。
2. 这不是“velocity layout 必然失败”的证据，因为 released Pulp AE 使用同类 human199 layout 却没有正长度斜率。
3. 这也不是“GT yaw loss 必然能训练成功”的证据；oracle 只给出上限和实验优先级。

### 2.3 本地 Pulp/MARDM 深层 AE screen

为了区分“浅层 v7.14 AE”与“训练目标”责任，v8.0 还用本地 `AAMMARDM` reproduction epoch320 做了同一 pure4053、true-length、owning-decoder screen。该 checkpoint 训练于 `94,050` mixed samples、约 `30.53M` exposures、固定 64 帧、camera/human/projection 等权 masked MSE；它与 v7.14 的 `81.38M` exposures、数据集合和 loss 不匹配，所以只能否定该 checkpoint，不能否定 AAMMARDM architecture。

artifact：

`/data/public/ripemangobox/Motion/StoryMotion/runs/stage1/v8_0_pulp_repro_deep_ae_screen_20260717/eval/pure4053_epoch320.json`

artifact SHA256=`c9baf13591cda0cad58d6b0a5eacd14443c6fd4ef292d2cf92e2254d850752ab`；override checkpoint SHA256=`396ef423b9d56af98320db165b0fac3a0ce4af56f04e5bd79fbd6ed714bf0282`。

| version / run | samples | overall root / global MPJPE mm | 193–256 root / global mm | root / global slope mm per 100f | camera ADE / rotation |
| --- | ---: | ---: | ---: | ---: | ---: |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | 4,053 | 80.73 / 212.74 | 132.22 / 429.43 | +29.02 / +145.30 | 41.76 mm / 0.619° |
| v8.0 screen / `pulp_repro_epoch320` | 4,053 | 286.82 / 953.45 | 265.94 / 1275.88 | −24.92 / +310.27 | 285.23 mm / 2.088° |

该 checkpoint 明确 No-Go。它同时说明 `val_human feature MSE=0.06918` 不能作为 Stage1 promotion gate；integrated geometry 必须在训练过程和 checkpoint selection 中出现。下一步不是把这个 checkpoint 接 Stage2，也不是只把 v7.14 换成更深网络。

## 3. v8.1–v8.2：Stage1 treatment 顺序

> [!important] 解释边界
> 2026-07-17 用户授权 v8.1A、v8.1B 与 v8.2 提前并行。三条均保持 `162,760 × 500 = 81.38M` exposure budget，但 A/B 或 A/v8.2 不是原始 sequential 单变量归因；它们是带已知改动集合的 system comparison。训练进度、ETA 与 worker 日志不再保存在本文。

### 3.1 v8.1A：human199 yaw/root geometry supervision

第一条 matched train 保持 v7.14 architecture、camera14、human199、latent `128+64`、non-causal、ordered IDs 和 budget，只增加 valid-mask-aware decoded geometry：

```text
theta_pred[t] = cumsum(delta_yaw_pred)[t]
L_yaw = mean(1 - cos(theta_pred - theta_gt))
root_xy_pred = cumsum(R(theta_pred) @ velocity_xy_pred)
L_root = SmoothL1(root_xy_pred, root_xy_gt)
```

现有 feature/velocity loss 保留。loss 权重先用完整 train IDs 的短 screen 检查数值尺度、主辅梯度比与 camera regression，再冻结一个配方做 `162,760 × 500`；pure4053 不用于逐 checkpoint 调权。训练与 eval 必须记录独立 batch size、steps、sample exposures 和 loss weights。

v8.1A promotion gate 在训练前固定为：

- overall human root-aligned/global MPJPE `≤85/190 mm`；
- `193+` human root-aligned/global MPJPE `≤90/210 mm`；
- root/global MPJPE length slope `≤5/20 mm per 100 frames`；
- camera Cam-ADE `≤50 mm`、rotation `≤0.75°`；
- no NaN、owning-decoder/checkpoint/cache hashes 完整；不以 feature MSE 替代上述 gate。

可执行入口已加入现有 Stage1 trainer，默认 `human_yaw_weight=human_root_weight=0`，所以历史 recipe 不变。非零时只接受 `joint_ae + normalized human199 + is_causal=false`，并把两项权重写入 `run_config.json` 与 `experiment_contract.json`。mask/gradient 单元测试已通过。

真实 Pulp 的 loss-scale audit 显示 raw weight=`1` 会压倒主损失；因此冻结 `yaw=0.001`、`root=0.003`，对应中位梯度比例约 `3.8%/10.1%`。finite optimizer-step smoke、mask/gradient unit tests 与 `is_causal=false` 断言均通过。训练日志和完整 endpoint 数值分别由 run artifact 与 [[StoryMotion-valid-metric-ledger#18.1.1 v8 endpoint：与 corrected v7.14 的完整同脚本比较]] 持有。

### 3.2 v8.1B：matched residual AE

原始 gate 只有在 v8.1A loss 稳定但容量不足时才启动本项；用户覆盖该算力顺序并要求同步训练。实现为 projection-free、non-causal AAMMARDM-style residual encoder/branch-owning decoder，width=`192`、depth=`2`、dilation growth=`3`、downsample=`4`，从 seed17 随机初始化；已有 epoch320 不复用。A/B 同时改变 geometry loss 与 architecture，只能按两因素 system comparison 解释。

### 3.3 v8.2：non-integrative human200

若 v8.1 matched endpoint 仍不能消除 heading slope，再改 feature layout。最小 candidate 是 human200：

```text
root_z 1 + root_xy_relative_to_first_frame 2 + yaw_sin_cos 2
+ pose6d 132 + local_joints 63 = 200
```

owning decoder 直接读取 absolute-relative root XY 与 yaw，不再对 yaw/root velocity 积分。camera14 暂不改，因为 v7.14 Stage1 Cam-ADE 只有约 `41.8 mm`；Stage2 camera 的米级误差先由 Stage2 channel oracle 定位。human200 是新 representation control，必须新建 train-only normalization、Stage1 checkpoint、owning decoder、cache 与 Unified Stage2，不能兼容加载 v7.14 cache。

human200 的 train-only frame-weighted population stats 覆盖 ordered `162,760` IDs、`19,336,840` frames，SHA256=`70623ea927300b107fc49c9f4d4a67a30b45f8565f6bf4e0c27a406296f95011`。checkpoint 内嵌 `camera64+human128` native order、human200 owning inverse、stats/source hashes 与 `is_causal=false`；因此它必须拥有独立 cache/contract，不能兼容加载 v7.14 cache。

### 3.4 2026-07-18 endpoint、amended screen 与 camera 根因边界

三条训练都已完成 `636,000` steps / `81.38M` exposures，并完成 true-length pure4053 endpoint。完整总指标、四个时序 bin、artifact SHA256 与 paired-bootstrap 区间见 [[StoryMotion-valid-metric-ledger#18.1.1 v8 endpoint：与 corrected v7.14 的完整同脚本比较]]。三者对 v7.14 的 human geometry 都是大幅改善：v8.1A 的 overall RA/global 是 `24.700/71.180 mm`，v8.1B 是 `28.245/76.655 mm`，v8.2 是 `12.999/68.706 mm`，相对 v7.14 的 `80.731/212.735 mm`，每条的 paired bootstrap CI 均不跨零。

原先的 absolute gate 是训练前的预注册定义，不能事后改写成“已通过”。但它把一个明确以 human yaw/root 为目标的 treatment，要求同时命中固定的 camera 绝对值和极小 global-slope 上限；v8.1A 的 global slope 是 `+31.103 mm per 100f`，虽未达到 `≤20`，却比 v7.14 的 `+145.300` 降低 `78.6%`。为评估用户提出的“总体显著优化可容忍轻微退化”，账本新增了 amended screen：human core 至少两项改善 `20%` 且 paired CI 支持，long-bin global 不得变差，camera 只容忍有限的 ADE/FDE/rotation 退化。它是 endpoint 后的辅助决策规则，不是 retroactive preregistration。

裁决如下：

1. `v8.1A` 通过 amended non-promotion screen。camera 的 `+14.2%` ADE、`+8.8%` FDE 与 `+0.098°` rotation 在容忍边界内，但并不等价于 camera 无损。
2. `v8.1B` 不通过。它相对 A 在短段 `1–64` 的 camera ADE/FDE/rotation 为 `58.691/75.239 mm/1.637°`，明显高于 A 的 `48.971/55.828 mm/0.955°`；反而在长段 camera error 下降，且 camera slope 为负。这把问题定位到 residual architecture 或 shared-branch optimization 的短序列/boundary reconstruction，而不是 root/yaw 的长程积分累积。现有 evidence 还不能把责任精确归到某一层或某一个 loss 项。
3. `v8.2` 不通过。camera14 的 feature width、loss weight 与 non-causal contract 没有改变，但其 center ADE 在四个 bin 均高于 v7.14，而 rotation overall 从 `0.619°` 改善至 `0.569°`，long-bin rotation 也更低；Cam-ADE slope 为 `−0.872 mm per 100f`。因此这是 shared human200 representation、normalization 或 joint-optimization 引起的 camera translation trade-off，不是 rotation 或 temporal integration 失败。区分 shared-gradient scale、joint layout 与 owning-decoder interaction 需要单变量 ablation。

所需的下一条诊断保持 non-promotion：固定 v8.1A 的 human treatment，单独检查 camera branch/decoder 的 short-bin reconstruction 与 loss-gradient scale；对于 human200，固定 camera14 后分别替换 human layout、stats 与 joint optimization。受控表征—Stage2 probe 的顺序、停止规则与 cache 禁令见 [[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]；它不改变任何 v8 candidate 的 promotion 状态。

#### v8.1C — camera14 decoded-center auxiliary pre-screen

`camera14` 不是纯逐帧 camera pose：其 `[11:14]` 是 normalized c2w translation velocity。Pulp `traj+char+proj` decoder 对第 `1:` 帧反归一化后累加该 velocity，并加上 **第 0 帧** reconstructed human root 和 relative-distance `[2:5]` 作为原点。因此现有 camera feature reconstruction / temporal-diff loss 能约束 velocity 及其差分，却没有直接约束最终累计 camera center；而第 0 帧 velocity 在原有 feature loss 中被置零、却仍会进入 decoder 的累计路径。

最小可归因 treatment 是保持 v8.1A 的 human199、camera14、joint-AE、non-causal、`yaw/root=0.001/0.003` 与所有数据/optimizer 边界，仅附加：

```text
camera_center = cumsum(decoded_camera_velocity)
              + decoded_relative_distance[t=0]
              + decoded_human_root[t=0]
L_camera_center = SmoothL1(camera_center_pred, camera_center_gt)
```

执行顺序与停表规则：

1. **C0 gradient calibration**：同 ordered train IDs、seed17、8 个真实 batch、`B=8`、最大 `250` frames；以 raw camera-center loss 的中位梯度，选择只占 v8.1A base-plus-human-aux gradient `5%` 的 weight。保存 manifest/hash、每 batch ID hash、原始 loss 与梯度中位数。没有此 artifact 不启动训练。
2. **C1 10K-class structural screen**：仅在 C0 finite、mask/unit test 通过后，在 4090 GPU1 从随机初始化训练 `8` epochs，即 `10,176 × 128` exposures；这是现有 epoch-bounded trainer 的最近精确预算，不能写成恰好 `10,000`。输出 Stage1 true-length pure4053 geometry，特别报告 camera center ADE/FDE/rotation 的四个长度 bin、human yaw/root 和 first-velocity offset。若 camera center 没有相对 v8.1A 改善、human core 退化超过 amended screen 容忍，或出现任何 contract/cache/decoder 不一致，停止。
3. **C2 matched endpoint only if C1 is directionally positive**：从零重训完整 `636K / 81.38M` Stage1 endpoint，不能把 C1 checkpoint、optimizer 或 screen result 当作 promotion evidence。C2 仍只是 v8 candidate；它通过 Stage1 gate前不建 Unified cache，更不进入 30K/105K。

截至 `2026-07-18T14:32:35+08:00`，C0 已成功完成，artifact 为 `runs/stage1/v8_1c_camera14_center_aux_seed17_4090g1_20260718/calibration.json`，SHA256=`901e3c2fe4ce41fb51f7174a823f9dccd4e99d3ec817217682de5ee2ba561544`。8 个真实 batch 的 base/v8.1A/raw-center gradient median 分别为 `0.114611/0.119016/1.463273`，故冻结 `camera_center_weight=0.00406677828128799`。C1 已从随机初始化启动为 `v8_1c_joint_ae_yaw001_root003_cctr004067_screen10k_seed17_4090g1_20260718`；本页只记录其为 running，未有 Stage1 endpoint、C2 或 promotion 结论。

这条诊断回答“camera14 的积分路径是否是 camera 退化的可修复责任通道”，不证明人类 yaw auxiliary 是 camera 回归的唯一原因。shared joint encoder 的梯度竞争、camera relative-distance branch 和 v8.2 的 human layout/stats 仍是并列解释；v8.1B 与 v8.2 不因 C1 而获得 Stage2 预算。

## 4. 架构检索：哪篇作为 non-AR pure diffusion 起点

本轮 `papers-query-knowledge-base` 的结论不是“越新越合适”。没有一篇 2025+ 顶会工作同时满足 StoryMotion 的两阶段、非自回归、pure diffusion、长序列、非周期 Pulp 与 joint human-camera contract。

| paper | 可复用部分 | 与 v8 的冲突 | 裁决 |
| --- | --- | --- | --- |
| TransPhase / NeurIPS 2025 | ACT-PAE、semantic phase diffusion、bidirectional adjacent-phase alignment；并行长段合成 | phase prior 偏周期动作，公开证据主要是多段 transition，不直接解决单 clip yaw integration | 严格“2024 后”最贴题；作为 v8.4-B long-composition control，不先于 Stage1 gate |
| Motion Mamba / ECCV 2024 | Motion VAE + non-AR latent diffusion，HTM/BSM 线性时序模块，明确长序列评测 | 年份不满足严格 post-2024；仍继承 Stage1 representation | v8.4-A 第一实现，改动最小、归因最干净 |
| EnergyMoGen / CVPR 2025 | 两阶段 latent pure diffusion、组合语义 energy guidance | 不是 long-root 专用架构 | semantic/composition 模块候选，不是第一 backbone |
| MotionLab / ICCV 2025 | MCM 接口、MFT、Aligned RoPE、长任务 curriculum | rectified flow，不是 strict pure diffusion；本地 formal 已改善语义但 global MPJPE 仍约 `951 mm` | 只借接口/RoPE，不复刻 objective |
| InfiniDreamer / ICCV 2025 | overlapping segment score distillation、geometry constraints、任意长 inference | training-free refinement，慢且依赖已有短 motion model | 可选 inference control，不是 Stage2 backbone |
| MARDM / CVPR 2025；MoLingo / CVPR 2026 | 强生成与 masked/continuous latent modeling | masked autoregressive；MoLingo 还依赖 causal SAE | 与 v8 strict non-AR 路线不符，排除 |

因此 **promotion-bearing v8.4** 的实现顺序仍是：Stage1 gate → Motion Mamba-style non-AR DDPM baseline → 同 representation/cache 下引入 TransPhase 的 adjacent-phase alignment。若用户把“必须 2025+”设为硬约束，则直接选择 TransPhase，但必须增加 aperiodic bypass/phase-confidence control，且不能把 transition improvement 当成 within-clip root 修复。v8.1A 的 non-promotion generatability ladder 不替代这条顺序，也不使用 v8.4 backbone。

## 5. v8.3 数据清洗轴

v8.3 的完整 preregistration、当前 gate、所有零/非零进度、四层 immutable manifest、scorer checkpoint 禁令和 pair-level 例子只由 [[2026-07-17_storymotion-v8-3-data-curation-plan]] 维护。当前状态是 `not_started / blocked_no_promoted_representation`：三条 v8 Stage1 endpoint 都未通过原始 promotion gate，故 processed、annotated、quarantined、materialized manifests 与 launched jobs 均为 `0`。本页不再维护第二份清洗规则或 progress。

## 6. v8.0+ 版本矩阵与因果顺序

| version / run | 目标 | 核心实验与固定边界 | 结果 / 结论 | 唯一允许的下一步 |
| --- | --- | --- | --- | --- |
| v8.0 / `v8_0_representation_oracle_audit_20260717` | 定位 human199 长时误差的责任通道 | v7.14 owning decoder；pure4053；仅替换声明的 GT root/yaw/local-joint channel | GT yaw 将 long root/global 由 `132.22/429.43` 降至 `8.68/38.99 mm`；heading 是第一责任通道，不等于可训练收益 | 用 matched yaw/root supervision 测试，而非直接改 Stage2 |
| v8.0 / `v8_0_pulp_repro_deep_ae_screen_20260717` | 筛查现成深层 AE 是否可直接替代 | epoch320 不匹配 exposure/data/loss；true-length pure4053 screen | overall root/global=`286.82/953.45 mm`，No-Go；否定该 checkpoint，不否定架构家族 | 不接 cache 或 Stage2 |
| v8.1A / `v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` | 在同 human199 AE 上修复累计 yaw/root | v7.14 architecture、camera14、non-causal、同 IDs/budget；只加 decoded geometry loss | human geometry 广泛改善；camera 为有限退化。原始 gate 未过，amended non-promotion screen 通过 | 只可进入受控 non-promotion generatability ladder；不得建 promotion cache |
| v8.1C / `v8_1c_joint_ae_yaw001_root003_cctr004067_screen10k_seed17_4090g1_20260718` | 判断 camera14 velocity-integral path 是否能修复 camera center 而不牺牲 v8.1A human gain | 固定 v8.1A，唯一加 decoded c2w center SmoothL1；C0 8-batch calibration 后以 `0.00406677828128799` 训练 C1 `10,176` steps | C0 complete；C1 running；任何 C1/C2 都是 non-promotion Stage1 diagnostic | C1 正向后才允许完整 636K Stage1；绝不直接进 Stage2 |
| v8.1B / `v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` | 测试 residual capacity 是否带来额外收益 | non-causal residual AE；同 IDs/budget/loss；与 A 同时改变 loss/architecture | human 改善，但 camera ADE/FDE/rotation severe regression，短段边界最明显 | 先做 camera branch/gradient root-cause diagnostic；不做 30K/105K Unified |
| v8.2 / `v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` | 测试非积分 human200 layout | human200、独立 train-only stats/owning inverse/cache；camera14 不变 | human 改善；camera center translation 四 bin 均退化，rotation 改善；为 shared layout/stats/joint-opt trade-off 假设 | 先拆分 layout、stats、joint optimization；不做 30K/105K Unified |
| v8.3 / `clean_manifest_ablation` | 测试 pair-level curation 是否改善 Stage2 prior | 固定已 promoted representation/backbone；只改变 immutable train manifest | 未启动；无 promoted representation，全部计数为 `0` | 等 prospective promotion 后按 curation contract 开 gate |
| v8.4-A / `motion_mamba_ldm` | 测试最小 non-AR latent DDPM backbone | 同 representation/cache 的 raw-manifest first control | 尚未开始；不是 v8.1A 的表征 probe 替代品 | 仅在 representation promotion 后实施 |
| v8.4-B / `transphase_control` | 测试 phase alignment 对长组合的增益 | 与 v8.4-A 同 cache/exposure，另加 aperiodic bypass/phase-confidence control | 尚未开始 | 在 v8.4-A 后作为 matched control |

任何 Stage2 diagnostic 都必须在 human generation、camera completion、joint parallel 与 human-first cascade 报告任务适用的 distribution/semantic 指标、decoded geometry 与四个时长 bin。自由生成的一对一 MPJPE/Cam-ADE 是 mandatory diagnostic，不单独构成质量 hard gate；物理、blind render 与 text-motion retrieval 共同决定 promotion。v8.1A 的控制性 Stage2 ladder、GT-channel/oracle 分解和停止规则只见 [[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。

## 7. 当前允许的结论

1. StoryMotion 当前确有 human geometry 问题，但 Stage1 长序列问题已从宽泛的“local tokenizer 差”收窄为“累计 heading supervision 不足”。
2. v7.14 的 Stage1 camera reconstruction 不是主风险，但 v8 endpoint 显示 shared joint tokenizer 的 human treatment 会带来 camera trade-off；这不是 Stage2 Direct C/joint 米级误差的充分解释，camera representation 与 joint optimization 必须分开诊断。
3. 数据错配真实存在，但没有证据表明它解释了 v7.14 Stage1 reconstruction；cleaning 主要面向 Stage2 semantic/physical prior。
4. 新 Stage2 architecture 不能替代 Stage1 gate。MotionLab 已给出实际反例：语义改善不自动带来 world-root geometry 改善。
5. v8 是有 gate 的实验族，不是新名字覆盖旧主线。
