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
  - "[[2026-07-17_storymotion-fixed300-offline-ar-motionstreamer-v746-deployment]]"
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
updated: 2026-07-17T18:25:00+0800
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

> [!important] 2026-07-17 execution override
> 下述“先 A endpoint、再 B/8.2”的顺序仍是原始科学 gate，但用户已显式授权提前并行部署：v8.1A 与 v8.1B 共驻 4090 GPU0，v8.2 独占 GPU1。三条均保持相同 ordered `162,760 × 500 = 81.38M` budget；提前并行只节省墙钟时间，不能把 A/B 或 A/v8.2 写成原始 sequential single-variable attribution。最终结论仍只看各自 pure4053 owning-decoder geometry endpoint。

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

真实 Pulp 的 8 个随机 batch、每批 8 条、最长 250 帧的 loss-scale audit 给出：base gradient norm median=`0.11544`，未加权 yaw/root gradient norm median=`4.33958/3.88529`；raw weight=`1` 会压倒主 loss。finite optimizer-step smoke 因此使用 `yaw=0.001`、`root=0.003`，对应 median gradient ratio 约 `3.8%/10.1%`。该 smoke 已通过：base/weighted-yaw/weighted-root/total loss=`0.455165/0.000938/0.000151/0.456254`，pre-clip grad norm=`0.10911`，step后参数全部finite，且`is_causal=false`。这组权重随后被显式冻结为 final recipe；`v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` 已于 17:29 CST 启动。截至 18:25，step=`54,441/636,000`、近 5k 吞吐=`15.55 step/s`、train total=`0.01751`，step54k pure-test total=`0.02645`，均 finite。预计训练与 queued pure4053 geometry 在 2026-07-18 04:45–05:20 CST 闭合。

### 3.2 v8.1B：matched residual AE

原始 gate 只有在 v8.1A loss 稳定但容量不足时才启动本项；用户已覆盖该算力顺序并要求同步训练。实现为 projection-free、non-causal AAMMARDM-style residual encoder/branch-owning decoder，width=`192`、depth=`2`、dilation growth=`3`、downsample=`4`，从 seed17 随机初始化；已有 epoch320 不复用。`v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` 于 17:43 CST 与 A 共驻 GPU0。截至 18:25，step=`29,268/636,000`、近 5k 吞吐=`12.14 step/s`、train total=`0.03486`，step28k pure-test total=`0.07109`，均 finite；预计 endpoint 与 queued geometry 在 2026-07-18 08:15–09:15 CST 闭合。A/B 同时改变 geometry loss 与 architecture，只能按两因素 system comparison 解释。

### 3.3 v8.2：non-integrative human200

若 v8.1 matched endpoint 仍不能消除 heading slope，再改 feature layout。最小 candidate 是 human200：

```text
root_z 1 + root_xy_relative_to_first_frame 2 + yaw_sin_cos 2
+ pose6d 132 + local_joints 63 = 200
```

owning decoder 直接读取 absolute-relative root XY 与 yaw，不再对 yaw/root velocity 积分。camera14 暂不改，因为 v7.14 Stage1 Cam-ADE 只有约 `41.8 mm`；Stage2 camera 的米级误差先由 Stage2 channel oracle 定位。human200 是新 representation control，必须新建 train-only normalization、Stage1 checkpoint、owning decoder、cache 与 Unified Stage2，不能兼容加载 v7.14 cache。

用户已授权提前实现并占用 GPU1。`v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` 于 18:19 CST 启动；train-only frame-weighted population stats 覆盖 ordered `162,760` IDs、`19,336,840` frames，SHA256=`70623ea927300b107fc49c9f4d4a67a30b45f8565f6bf4e0c27a406296f95011`。checkpoint 内嵌 `camera64+human128` native order、human200 owning inverse、stats/source hashes 与 `is_causal=false`，step0 cache-loader contract preflight 已通过。截至 18:25，step=`6,133/636,000`、近 5k 吞吐=`18.81 step/s`、train total=`0.05389`，step4k pure-test total=`0.11265`，均 finite；预计 endpoint 与 queued pure4053 geometry 在 2026-07-18 03:40–04:20 CST 闭合。

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

因此实现顺序是：Stage1 gate → Motion Mamba-style non-AR DDPM baseline → 同 representation/cache 下引入 TransPhase 的 adjacent-phase alignment。若用户把“必须 2025+”设为硬约束，则直接选择 TransPhase，但必须增加 aperiodic bypass/phase-confidence control，且不能把 transition improvement 当成 within-clip root 修复。

## 5. 数据清洗

### 5.1 物理清洗

物理清洗先产生 quarantine manifest，不直接删除：

- world-root speed、acceleration、jerk 与 yaw rate/acceleration；
- foot contact 时的 world foot sliding、地面穿透与悬空；
- bone-length drift、joint angular velocity/acceleration；若 mesh 可得，再加 body self/environment penetration；
- 按 capture source、duration 和动作类别做 median/MAD robust threshold，避免把跑、跳、旋转等合法高速动作当异常；
- 高置信硬错误进入 `physical_quarantine`，边界样本进入人工审核，保留 reason code、原始值和阈值版本。

“快速漂移”必须区分真实 locomotion 与 capture/root corruption。只有短时 root jerk、脚接触冲突、语义不支持的高速平移等多证据一致时，才升级为高置信物理异常。

### 5.2 语义清洗

语义清洗以 caption-motion pair 为单位，不默认删除 motion sample：

1. TMR 提供 global alignment；
2. LaMP 提供 motion-aware text/motion embedding 与已公开 retrieval code/checkpoint；
3. PST 提供 joint/segment/global fine-grained mismatch，但当前未登记可复现 checkpoint，首版只保留接口位；
4. MoCHA 用于把不可由动作恢复的风格/场景信息 canonicalize，再同时比较 original/canonical caption；
5. `MARDM-67` 是 evaluator/protocol，不是第四个 retrieval scorer，不进入 ensemble vote。

先人工标注约 `300–500` 个分层 pair，覆盖 posture、direction、body-part、temporal order、locomotion 与否定关系，再校准 scorer。只在多模型一致且超过校准阈值时自动 quarantine；模型分歧进入人工队列。最终保存 raw、physical quarantine、semantic-pair quarantine、clean 四份 immutable manifests，记录 ordered IDs、caption ID、reason、model/checkpoint hash、score、threshold 和 parent-manifest hash。

独立执行契约见 [[2026-07-17_storymotion-v8-3-data-curation-plan]]，零进度与 gate 记录见 [[2026-07-17_storymotion-v8-3-data-curation-progress]]。由于 v8.2 的完整 endpoint 预计在 2026-07-18 凌晨，而不是 2026-07-17 22:00 前完成，清洗 gate 保持 closed：processed/annotated/quarantined/materialized manifests/launched jobs 全部为 `0`。

### 5.3 已核验的错配样本

`2019_vcdDRblTOmM_00038_001_a` 的 htext 是：

> Human: A person stands still and turns their head slightly to the right.

GT 共 35 帧，左右膝平均弯曲约 `85.17°/81.82°`，root Z 约 `0.849 m`，root XY displacement 只有 `0.056 m`；几何与持续坐姿/深屈膝一致，不是站立。该 pair 进入 semantic quarantine；motion 若有其他正确 caption 仍保留。

## 6. v8 实验矩阵与因果顺序

| priority | version / run | 单一问题 | 数据 / budget | 状态与下一步 |
| --- | --- | --- | --- | --- |
| P0 | v8.0 / `v8_0_representation_oracle_audit_20260717` | 哪个 human199 root channel 导致长度退化 | pure4053 diagnostic | 已完成；yaw 是主因 |
| P0 | v8.0 / `v8_0_pulp_repro_deep_ae_screen_20260717` | 现成 self-trained deep AE 能否直接替代 | pure4053 screen；训练 exposure 不匹配 | 已完成，No-Go；不接 Stage2 |
| P0 | v8.1A / `v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` | 同一 AE/layer 上 geometry loss 是否修复 yaw | `162,760 × 500` | GPU0 training；step54,441 finite；endpoint ETA 07-18 04:45–05:20 |
| P1 | v8.1B / `v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` | matched residual AE system 是否增益 | 同 IDs、budget、loss；不复用 epoch320 | 用户授权提前与A共驻GPU0；step29,268 finite；ETA 07-18 08:15–09:15 |
| P1 | v8.2 / `v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` | integration-free layout 是否必要 | 同 IDs/budget；新 stats/decoder/cache | 用户授权提前占GPU1；step6,133 finite；ETA 07-18 03:40–04:20 |
| P1 | v8.3 / `clean_manifest_ablation` | curated pairs 是否改善 semantic/physical quality | 同一 promoted representation/backbone | plan/progress已预注册；22:00 gate closed；全部进度计数为0 |
| P1 | v8.4-A / `motion_mamba_ldm` | non-AR pure latent diffusion 是否改善生成 | promoted representation、raw manifest first | Stage1 gate 后实现 |
| P2 | v8.4-B / `transphase_control` | phase alignment 是否改善 long composition | 同 cache、matched exposure | v8.4-A 后；加 aperiodic control |

Stage2 必须在 human generation、camera completion、joint parallel 上同时报告已有 distribution/semantic metrics 与 decoded geometry。自由生成的一对一 MPJPE/Cam-ADE 是 mandatory diagnostic，不单独作为质量 hard gate；物理指标、blind render 与 text-motion retrieval 一起形成 promotion。另做 Stage2 GT-channel oracle，区分 generated yaw/root 与 pose/channel 对 v7.38 global `863 mm` 的贡献，再决定是否动 camera representation。

## 7. 当前允许的结论

1. StoryMotion 当前确有 human geometry 问题，但 Stage1 长序列问题已从宽泛的“local tokenizer 差”收窄为“累计 heading supervision 不足”。
2. Stage1 camera reconstruction 当前不是主风险；Stage2 Direct C/joint 的米级 Cam-ADE 表明 camera 问题主要由生成/条件路径引入。
3. 数据错配真实存在，但没有证据表明它解释了 v7.14 Stage1 reconstruction；cleaning 主要面向 Stage2 semantic/physical prior。
4. 新 Stage2 architecture 不能替代 Stage1 gate。MotionLab 已给出实际反例：语义改善不自动带来 world-root geometry 改善。
5. v8 是有 gate 的实验族，不是新名字覆盖旧主线。
