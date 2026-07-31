---
title: "StoryMotion Current — Pre Human-first Orthogonalization Snapshot"
status: archived_superseded_current_snapshot
hypothesis: |
  v8.1C C3-25 seed17 is the audited Stage1 and Stage2 mainline. The former
  Human global-slope threshold is a non-blocking diagnostic pass. v7.14 and
  v7.38 are former-mainline comparators; seed23 Stage2 remains audit-pending.
tags:
  - StoryMotion
  - version
  - stage1
  - stage2
  - status/archived
source_notes:
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[StoryMotion-iclr-reliability]]"
  - "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
source_papers:
  - "[[analysis/ECCV_2024/Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation]]"
  - "[[analysis/NEURIPS_2025/TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_Generation]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/CVPR_2025/SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation_and_Editing]]"
  - "[[analysis/arxiv_2026/Reconstruction-Anchored_Diffusion_Model_for_Text-to-Motion_Generation]]"
  - "[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion]]"
created: 2026-07-12T14:30:00+08:00
updated: 2026-07-24T12:10:00+08:00
archived: 2026-07-24
superseded_by: "[[current]]"
---

# StoryMotion Current

<!-- c3-25-stage2-status-20260721 -->
> [!success] v8.1C C3-25 Stage2 已闭环
> `seed17` 已完成 Stage2 训练、Direct-H / Direct-C / joint parallel 正式评估与审计。相对旧 mainline 的匹配基线 v7.38 L0，C3-25 在大多数已审计正式指标上显著更优；当前状态应标记为“Stage2 train/eval completed”，而不是“训练中”或“待评估”。

> [!success] Mainline decision
> Stage1 Human global-slope 的旧 `≤20 mm/100f` 阈值不再是强制 gate，C3-25 的该项 diagnostic 判定为通过；原始数值 `26.302 mm/100f` 继续保留。结合 Stage1 Human/Camera Pareto 与已审计 Stage2 三路结果，C3-25 seed17 正式成为当前 mainline。`seed23` 仍为 `result_written_audit_pending`，不得并入正式 multi-seed 结论。

> [!abstract] 当前裁决
> **当前 mainline 是 v8.1C C3-25 seed17**：Stage1 fresh `636K / 81.38M` owning-decoder audit 已闭合；旧 global-slope 阈值改为非阻塞 diagnostic 并判定通过。Stage2 `105K` Direct-H TMR `14.389` 与 FTD `222.12` 均击败 former mainline v7.38 L0（`13.294 / 333.88`）；Direct-C CLaTr `59.539` 与 FCD `25.09` 均击败 v7.38 L0（`55.64 / 33.29`）；joint parallel 无 broad regression。v7.14/v7.38 现为 former-mainline comparators。C5-B repair 轴因 seed23 未复现 target 而关闭，但不影响 C3-25 mainline。Stage2 seed23 三路 `105K` result/records 已写出，仍为 `result_written_audit_pending`，不能作为 formal multi-seed 复现。v8.2333 的 representation owner 已固定为 C3-25，但阈值、quarantine、clean manifest 与训练仍需单独授权。

> [!info] P0 condition-exposure 裁决（2026-07-22）
> Tb25-band r4 的 matched `105K→110K` 训练、三模式 `N=512` screen、evaluator 等价性复跑与 no-update gradient attribution 均已闭合。Tb25 在 Direct-H、Direct-C 与 joint Camera 上形成 broad regression，当前 arm 停止；C3-105K 保持正式 mainline。共享 trunk 与 Camera path 没有确认 completion/joint 负梯度冲突；仅 Camera task embedding 上出现 clean-H 与 qH 的局部反向信号，而 source router 未启用。数值、hashes 与裁决只见 [[archived/diagnostics/2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder_closed-through-human-only_20260724#P0-JC-8：Tb25-band lower-dose condition exposure（2026-07-22 预注册）]]。

> [!failure] Human-only 已闭合但未修复 Human（2026-07-24）
> C3-25 原生 Direct-H Human-only 在四个预注册 exposure/compute boundary 均未形成
> semantic/distribution 改善；paired global/root trajectory 的改善伴随
> root-aligned pose、wrapped heading 或分布代价。统一混训与 Human dose 因而不是
> 当前首要解释；不运行 pure4,053，不晋升 specialist。下一步只做 Human
> objective、near-zero identity、heading、decoder/manifold 的 no-update attribution。
> 精确合同与裁决见
> [[archived/diagnostics/2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder_closed-through-human-only_20260724#P0-HUM-1：C3-25 原生 Direct-H 单任务学习曲线（2026-07-23 预注册）]]。

> [!warning] 最容易混淆的命名
> 仓库中没有独立的 “v8.1D” 或 “v8.1H” 完整版本。`D4/D4.2/D4.3` 是 v8.1A `30K` checkpoint 的 Stage2 只读诊断；`C4-H` 是 v8.1C 内部的 Stage1 Human-horizon short arm。完整命名、dose 和 step 对照只见 [[version_family#v8.1 命名解码与执行状态]]。

精确指标、valid-length bins 与 artifact/checkpoint/record hashes 只见 [[StoryMotion-valid-metric-ledger]]；指标定义与 decoder/evaluator 语义只见 [[StoryMotion-metric-computation-io]]。

## 1. 当前决策板

| family / run | Stage 与预算 | 要回答的问题 | 已验证状态 | 现在允许的行动 |
| --- | --- | --- | --- | --- |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | Stage1 `636K` | corrected local tokenizer 能否作为 implementation baseline | former implementation mainline；long Human geometry 仍是已知风险 | 保持为 matched representation comparator |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Stage2 `105K` | Unified-3 formal reference 是什么 | former Stage2 formal mainline | 作为 matched `105K` comparator |
| v7.47 / `v7_47_official_ae_unified_matched_seed17_5090g0_20260717` | Stage2 `105K` | official AE system 在同预算 Unified 中表现如何 | audited system control；Direct-H/Direct-C 有 signal，parallel Camera 退化；strict representation isolation 未建立 | 保留为 system evidence，不替换 C3-25 mainline |
| v8.1A / `v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` | Stage1 `636K` | yaw/root geometry supervision 能否修复 Human 长程误差 | Human 显著改善，Camera mild regression；原始 Stage1 gate 未过 | 保留为 v8.1C parent 与 Stage2 generatability control |
| v8.1A / `v8_1a_diag_unified3_30k_seed17_4090g0_20260718` | Stage2 `30K` | v8.1A latent 是否更易生成 | Direct-H 有 signal；Direct-C 与 joint parallel Camera broad regression；正式停止 | 不续 `105K`；只保留已闭合 D4 family 归因 |
| v8.1C C3-25 / `v8_1c_center25pct_full636k_seed17_4090g0_20260719` | Stage1 `636K` | 低 dose Camera-center loss 能否兼顾 Human 与 Camera | 当前 Stage1 mainline；Human/Camera Pareto 通过，global-slope 为非阻塞 diagnostic pass | 作为下列 Stage2 mainline 的 exact parent |
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | Stage2 `0→105K` | C3-25 latent 在同 Unified 与长预算下能否生成 | exact cache/contract、D1、`30K` 与 `105K` active three-profile formal audit 均闭合；Direct-H 与 Direct-C 多数指标击败 v7.38，joint parallel 无 broad regression | 当前 Stage2 formal mainline；run ID 与 contract 中的 diagnostic 字段仅保留历史 provenance；physical/render 与 multi-seed 继续补强外推证据 |
| C3-25 P0-JC-7/8 / Parent、C0、Tq、Tb25、Tj family | Stage2 matched `5K` + `N=512` full-sampling；timestep attribution；no-update gradients | noisy observed-H exposure 能否同时保住 completion、joint 与 framing；是否存在共享参数冲突 | Tb25-band r4 broad regression 并停止；evaluator 标准路径等价；仅在 r4 endpoint/IDs/`t=399–799` 的 aggregate attribution 中，Direct-C↔joint-C 在 shared trunk/Camera path/output head 为正余弦；结构性正交只属于不同 task rows/不相交 output slices；Camera task embedding 有局部 clean/qH 反向信号 | Parent 保持 mainline；不启用 PCGrad/CAGrad；任何 source-conditioned Camera-only 方案都需新 contract 与 Human hard gate |
| C3-25 P0-JC-9 / H-FULL、H-ISOLATED、C-JOINT、ALL-JOINT | four fresh Stage2 `0→105K` + matched `N=512` screen | Direct/joint 的 Human/Camera view mismatch 是否是主要根因 | 四臂全部闭合；H-axis 只有局部 Human signal，C-JOINT/ALL-JOINT broad regress；朴素 view equality fail | 四臂停止，Parent 保持 mainline；VACE 式分离控制面仅作后续设计先验，不立即训练 adapter |
| C3-25 / `p0_c3_25_human_only_native_0_105k_seed17_5090g2_20260723` | Human-only fresh `0→105K`；四 snapshots | Unified 混训、Human dose还是当前 Human generator 上限 | 四个 Direct-H N=512 screens 均无 semantic/distribution 改善；paired geometry mixed | 不做 formal；先做 heading/identity/decoder/manifold attribution，再授权单变量 Human short arm |
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_seed23_105k_4090g1_20260720` | Stage2 `0→105K` | seed17 Stage1 representation 下的 Unified-3 signal 是否跨 Stage2 seed | Human、Camera、joint parallel `105K` result/records 已写出；未见对应 contract audit/profile audit | 保持 `result_written_audit_pending`；先补 provenance/audit，禁止进入 ledger、version milestone 或 multi-seed claim |
| v8.1C C3-25 / `v8_1c_center25pct_full636k_seed23_5090g0_20260719` | Stage1 `636K` | C3-25 signal 是否跨 seed | Human RA `24.70` / global `70.80` / slope `27.59 mm/100f`；Camera ADE `39.05` 与 translation signal 重现；rotation `0.776° > 0.75` fail；slope fail | 只作 robustness evidence，不替代 seed17 selected arm |
| v8.1C C3-50 / `v8_1c_center50pct_full636k_seed17_4090g1_exploratory_20260719` | Stage1 `636K` | 更高 center dose 的完整预算代价是什么 | Camera ADE `36.41` 更好，但 Human overall `73.17` / long `193+` global `138.49` 与 slope `36.21` 全面变差 | dose-response 已闭合；不再增大 center dose |
| v8.1C C5-B / two-seed matched short family | Stage1 calibration + fresh `10,176` screens | four-anchor multi-horizon 是否进一步改善 C3-25 的 Human horizon | seed17 dose1.0 过 gate，但 seed23 两项 target 未复现；two-seed screen fail | optional repair 正式关闭；不影响 C3-25 mainline |
| v8.1B / `v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` | Stage1 `636K` only | residual AE 是否增加有效容量 | Human 改善，Camera short-bin severe regression；无 Stage2 | 不建 Unified；仅作 architecture control |
| v8.2 / `v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` | Stage1 `636K` only | non-integrative human200 是否解决 root/yaw 累积 | Human 改善，Camera center translation 退化；无 Stage2 | 不建 Unified；仅作 representation control |
| v8.2333 / `quality_gradients_nested_v1` | future data axis | pair-level curation 是否改善 prior | 全量多维 quality table 与五种 `8K/16K/32K/64K` v1 controls 已审计；实现复核发现 `q_H` stratum 混入 Camera dynamics，且 Camera/framing/semantic axes 未闭合 | 新 root 重建 axis-pure v2，补 `q_C`、完整 `q_HC`、`q_CT`；不得称 clean、冻结阈值、建训练 cache 或训练 |
| v8.4-A/B | future Stage2 backbone | non-AR backbone 是否改善生成 | not started | 以 C3-25 mainline 做 matched backbone axis；仍需单独授权 |

## 2. 不可变边界

- Stage1/Stage2 的 tokenizer 固定为 non-causal；construct、checkpoint/cache load、train 与 eval 均断言 `is_causal=false`。standalone native MotionStreamer 是唯一外置例外，不能进入 StoryMotion cache、Unified 或 promotion gate。
- Human completion 是 `human text → H`；Camera completion 是 `GT/observed H + camera text → C`；active evaluation 固定为 Direct-H、Direct-C 与 joint parallel。Cascade 只作历史或显式 root-cause attribution，不是必报分数或 gate。
- Stage2 必须绑定 exact Stage1 checkpoint、owning decoder、train/eval cache hashes、train-only normalization source、ordered IDs、seed、train/eval batch size、sample count 与 sampler。
- pure4053 已被多轮开发和候选选择使用。它现在支持当前 mainline decision，但不等于独立外部验证；面向论文的强泛化 claim 仍需训练前冻结新的 sealed audit set。
- GT 是 reconstruction/paired-target reference，不是 one-to-many Stage2 generator。PulpMotion 的 released AE 与 official DiT 是 native-system baselines；只有在 Stage、任务、IDs、预算和 evaluator 都写清时才能与 StoryMotion 并列。

## 3. v8 假设与 mainline selection policy

v8.0 owning-decoder oracle 已把 v7.14 的主要长程问题收窄到累计 heading：替换 GT yaw velocity 会大幅降低 long-bin root/global error，而替换 local-joint channels 不改变最终 SMPL joint error。它证明 yaw channel 是首要责任通道，但不证明某个可训练 loss 必然成功。

v8 candidate 的 Stage1 原始 gate 不追溯改写：

| gate | threshold |
| --- | ---: |
| overall Human RA-MPJPE | `≤85 mm` |
| overall Human global MPJPE | `≤190 mm` |
| `193+` Human RA/global MPJPE | `≤90 / 210 mm` |
| Human RA/global length slope | `≤5 / 20 mm per 100f` |
| Camera Cam-ADE | `≤50 mm` |
| Camera rotation | `≤0.75°` |
| contract | finite；checkpoint/owning-decoder/IDs/hashes 完整 |

C3-25 seed17 的 Stage1 Human/Camera Pareto 与 Stage2 三路 formal evidence 已通过 mainline selection。global slope 原始值高于旧阈值，但该阈值现为非阻塞 diagnostic，状态记为 pass；原始数值不改写。

三个因果轴必须分开：

1. **v8.1 representation/loss**：先修 Stage1 yaw/root、Camera center 和 Human horizon。
2. **v8.2333 data curation**：固定已晋级 representation/backbone，只改变 immutable train manifest；完整 contract 见 [[2026-07-17_storymotion-v8-2333-data-curation-plan]]。
3. **v8.4 Stage2 backbone**：先做 Motion Mamba-style non-AR latent DDPM，再以同 representation/cache 测 TransPhase-style adjacent-phase alignment。它们不能替代 Stage1 gate。

## 4. 当前根因判断

### 4.1 为什么 C3-25 成为当前 mainline

C3-25 的 25% 表示 **C1 Camera-center weight 的 25%**，不是 25% 数据、训练步数或样本。它等价于 C0 raw-center unit gradient 的约 `1.25%` target dose；C3-50 则约为 `2.5%`。两条 short 都是 fresh `10,176` steps，两条 full 都是 fresh Stage1 `636K`。

低 dose 在 seed17 full 上同时守住或改善 Human、Camera translation 与 rotation；更高 dose 则把 Human long horizon 推坏，说明 C3-25 是当前 Pareto 选择。global slope 保留为非阻塞 diagnostic 和后续优化轴。C4-H 的 old last-valid objective 在 matched `10,176`-step short 中 fail；C5-A 只读 audit 显示 four-anchor multi-horizon surrogate 与 formal global/yaw/root-ADE 更对齐。C5-B 随后完成 fresh two-seed calibration 与 matched shorts：seed17 选择 dose1.0，但 seed23 未复现两个 target，因此 optional repair 轴按预注册停止，不进入 full。

因此 C3-25 当前状态是 **Stage1/Stage2 mainline**。晋升依据是自己的 exact checkpoint、owning decoder、cache、normalization 与 `105K` formal eval artifacts；不能继承或改名 v8.1A 的 `30K` 结果。历史 run 的 diagnostic contract 不回写，但不再代表当前 eligibility。

### 4.2 v8.1A Stage2 为什么停在 30K

v8.1A 与 v7.36 做了同 Unified implementation、seed、预算和 sampler 的 G3 `30K` screen。Human 侧出现可重复 signal，但 Direct-C 与 joint parallel Camera 在 semantic/distribution/coverage 上 broad regression。D4/D4.2/D4.3 进一步表明：Camera text 确实被使用；主要问题是 near-manifold 低噪 residual 更集中命中 v8.1A owning decoder 的 Camera 高敏方向，即 Stage1 manifold/decoder 与 Stage2 objective/response 的 cross-stage calibration mismatch。

这个证据当时不支持把“继续训练到 `105K`”当作自动修复，因此原 run 的 `105K` authorization 正确关闭，历史正式端点仍是 `30K`。2026-07-21 新授权的是独立的 **budget-matched causal control**：从只读 `30K` optimizer checkpoint 建立新 run ID，按 C3-25 相同的 `30,001` LR decay 续到 `105K`；它只回答同预算比较，不回写原 run，也不预设 v8.1A 会被修复或晋升。

### 4.3 Stage2 → Stage1 reconstruction ceiling 的转化缺口

> [!warning] 问题边界
> Stage1 reconstruction 是给定真实 motion 后的 paired 上界；Stage2 text generation 是 one-to-many 条件生成，不能要求自由采样逐样本等于同一 GT。这里所谓“更好拟合 Stage1”严格指：在相同 `z_gt`、噪声、timestep 与任务视图下，Stage2 的 `pred_x0` 经 owning Stage1 decoder 后应更接近 `Dec(z_gt)`，并把这种局部 fidelity 转化为更好的自由生成分布、语义与几何；不能直接拿 Stage1 paired 数字作为 Stage2 promotion gate。

四条 architecture-view arm 与 Human-only 当前支持以下**设计不足候选**，但尚不构成
单因果证明：

先保留两个重要的非单调事实：H-ISOLATED 的 Human distribution/semantics 改善但
global geometry 退化；Human-only 的 paired global/root trajectory 改善但
semantic/distribution broad regress。C-JOINT/ALL-JOINT 则说明把 numeric view
强制统一会全面退化。当前 endpoint 对“接近 Stage1 paired geometry”与“自由生成
semantic/distribution”给出了不同排序，不能用任一侧替代另一侧。完整 screen 数值
只见 [[StoryMotion-valid-metric-ledger#5.4 Architecture-view consistency 四臂 N=512 screen]]
与 [[StoryMotion-valid-metric-ledger#5.5 C3-25 原生 Direct-H Human-only 学习曲线 N=512 screen]]。

1. **latent objective 与 decoder geometry 不对齐。** 当前主损失是在 Human/Camera 分块 full-cov whitening 后，对 valid target elements 做 `START_X` MSE。whitening 只校正线性二阶统计，不等价于 owning decoder 的 Jacobian metric，也不约束预测落在 Stage1 可稳定解码的 latent manifold。两条 H arm 与 parent 的 active held-out latent losses 很接近，但 decoded screen 明显分叉；这使“继续压低同一个 element-MSE”不再是充分解释。现有 D4.3 也只支持低噪、方向选择性的 decoder amplification，不能外推为全 timestep 结论。
2. **低噪 Stage1 细节没有解析 identity path，uniform timestep 也不等于 uniform gradient dose。** `sample_t` 在 `0–999` 均匀取样，但 `START_X` 使用未分 timestep 加权的完整 latent MSE；高噪 bin 若误差与梯度更大，仍可能主导共享优化。更直接的是，当前 head 输出完整 `pred_x0`，`prediction_to_x0` 对 `START_X` 原样返回预测，没有从已经携带局部细节的 `x_t` 到 `x_0` 的解析 residual/identity 路径；低噪细节也必须经过整套 shared U-Net 重写。当前 single-step grid 的最低点 `t=199` 在 cosine schedule 下仍有约 `0.318` 的 noise coefficient，不足以单独诊断 Stage1-near identity；这个候选必须等近零噪声点、逐 timestep loss/gradient budget 与 no-op baseline 后才能判定。
3. **共享优化轨迹会跨任务改写输出，即使该任务的数据流未变。** 两条 H arm 都保留 mainline Direct-C 的 clean-H、Camera text 与 Camera-only loss，Direct-C/joint-C 却随 Human view 改动而变化。这说明 inference mask 本身不是完整控制；当前 U-Net 用一个 `1×1 in_conv` 立即混合 `128H + 64C` latent channels，再共享全部 temporal trunk，只有最终 output rows 被 target mask选择。shared trunk/output head 因而会在长期联合训练中到达不同 shared endpoints。它不等于已确认负梯度冲突，因为已有 no-update cosine 只覆盖一个 checkpoint/batch/timestep 邻域。
4. **当前 text fusion 不是 modality-presence invariant。** 路由先将 Camera 或 Human 的 `512-d` text half 缩放为零，再把整个 `1024-d` concat 输入同一个 `LayerNorm(1024) + MLP`。所以 `[e_C,0] → [e_C,e_H]` 不只是增加 Human 信息，也会改变同一个 `e_C` 的归一化均值、方差和投影坐标；Human 侧同理。arm（1）–（4）因此同时改变 auxiliary information 与 active-text coordinate system，不能只解释为“是否使用另一 branch text”。
5. **联合损失的隐式分支权重与 task probability 不是同一件事。** task allocation 虽为 `[1,1,1]`，`joint_loss_mode=element_mean` 在 joint sample 内由 `128` 个 Human latent channels 与 `64` 个 Camera channels形成约 `2:1` 的 element count。此项可能影响 Camera ceiling transfer，但不能通过降低 Human loss来修复；任何平衡实验都必须保持 Human hard gate。
6. **缺少显式 manifold/reconstruction anchor。** trainer 已有冻结 owning decoder 的 feature/velocity auxiliary 实现，但 C3-25 mainline 的 `geo_loss_weight=0`，且现有实现没有低噪 band gate。它是可审计的候选工具，不是当前已授权答案；直接全 timestep 开启会把 decoder fidelity、timestep weighting 与 architecture 三个因素混在一起。
7. **validation 汇总含 inactive Human-text task。** evaluator 会遍历四个 task ID，而当前训练概率的第四项为 `0`；`selection_metric=auto` 在多 active task 时选择 aggregate `loss`。本轮 early stopping/EMA 均关闭且正式使用 `last.pt`，所以这没有改变现有 `105K` endpoint，但它会污染 `best_eval` 的解释，未来任何 checkpoint selection 前必须改成 active-task-only 汇总。

P0-HUM-1 已排除“简单移除混训或增加 Human dose即可修复”的解释。本轮不再用无归因
的 `105K` 猜测上述因素；以下 E0–E3 先定位 objective、decoder/manifold 与 heading
根因：

1. **E0 — no-update ceiling-transfer attribution。** 对 Parent、Human-only `105K`
   做 Human primary，ALL-JOINT 只作 architecture negative control；固定同一
   checkpoint-level IDs、noise 与 timestep grid，保留现有
   `199/399/599/799/999`，并新增 `0/49/99` 三个 near-reconstruction 点。分别报告
   whitened latent error、inverse-whitened branch error、`Dec(pred_x0)` 对
   `Dec(z_gt)` 的 Human/Camera feature、velocity、root/yaw、Camera
   center/rotation/framing error，以及 `Dec(z_gt)` 对 raw GT 的 Stage1 floor。
   加入 `x_t` 原样与 Gaussian-prior posterior mean `sqrt(alpha_bar_t)·x_t` 两个
   不训练 baseline；若 model 在 near-zero-noise 端反而破坏已存在的信息，应优先查
   parameterization/identity path。必须按 Direct-H、Direct-C、joint-H、joint-C
   分开，不能只报总 MSE。同一 probe 额外记录每个 timestep bin 的 loss 与
   parameter-block gradient norm/dose，并记录 `[e_C,0]`、`[0,e_H]`、
   `[e_C,e_H]` 在 concat LayerNorm 前后与 `text_mlp` 后的
   active-half/condition cosine、norm 和 auxiliary-shuffle delta，以区分
   “新增语义”与“归一化坐标被重写”。
2. **E1 — inference-only Stage1 projection oracle。** 将完整预测 latent 做一次 `Enc(Dec(pred_x0))`，Direct-C 重新 clamp observed Human，再以 owning decoder 评估；不更新任何参数。若 projection 显著恢复几何且不损害语义/coverage，才支持 off-manifold/output-projection 解释；若无恢复，则停止该分支。
3. **E2 — no-update auxiliary gradient calibration。** 仅当 E0 显示 decoder-space excess error 时，在相同 batch/timestep 上比较 latent MSE 与 frozen-decoder feature/velocity anchor 的 parameter-block cosine、norm ratio 和 Human/Camera branch dose；同时汇总各 timestep bin 对共享梯度 norm 的占比。权重按共享梯度 dose 校准，不按 raw loss scalar 猜值。
4. **E3 — 单变量短训，必须由 E0–E2 选择。**
   - 若低噪 decoder amplification 或 projection oracle 命中：从同一 C3-105K parent 建立新的 matched continuation，仅对 target branch、只在命中的低噪 band 加入低 dose reconstruction anchor；同时保留 exact zero-dose continuation。Stage1 全冻结，task probabilities、task embeddings、loss masks 与 Human loss不变。
   - 若 model 在低噪端未超过 no-op baseline，或 timestep gradient budget 明显被高噪 bin 主导，而 projection 无效：另开 `START_X` 对 v-prediction或显式 SNR weighting 的 matched fresh screen，一次只改一个变量，不与 decoder anchor 合并。v-prediction 的解析 `x_t` 路径是待验证机制，不是预设优势；[[analysis/CVPR_2025/SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation_and_Editing|SALAD]] 的结果只作外部先验，不当作 StoryMotion 证据。
   - 若 condition-code audit 显示 active text 被另一 half 的存在显著重标定：优先独立的 per-modality LayerNorm/projection与 learned null token，使 condition 写成显式 gated `P_C(e_C) + P_H(e_H)`；单独做 matched fresh screen，不与 latent-view或decoder anchor合并。
   - 若 Direct-C ceiling-transfer 良好而 joint-C 持续欠拟合，且 no-update attribution 未显示 Camera/Human 冲突：可用 `branch_sum` 加 `joint_loss_weight=2/3` 做 Human-dose-preserving control。它把当前 joint sample 近似的 `2/3·L_H + 1/3·L_C` 改为 `2/3·L_H + 2/3·L_C`，保持 Human 系数不变、只补 Camera dose；普通 `branch_mean` 会降低 Human 系数，不授权。
   - C-JOINT/ALL-JOINT 已证明直接 view tying 无效，因此当前不授权 adapter。
     只有 Human 修复后 Direct-C ceiling-transfer 良好而 joint-C 仍呈稳定
     source mismatch，才考虑 identity-init、Camera-only 的
     task/source-conditioned residual output adapter；shared Human path 不加
     adapter。PCGrad/CAGrad 仍需新的跨 timestep/block 冲突证据。

E3 的 hard stop：Direct-H 任一 primary semantic/distribution/coverage 或 Human global/root geometry出现 practical broad regression；或者 decoded fidelity 改善却伴随 Camera/Human semantic collapse。低噪 paired fidelity、完整 single-step grid与 DDIM50自由生成必须同时报告，任何一层都不能替代另一层。

本地证据只提供方法先验：[[analysis/arxiv_2026/Reconstruction-Anchored_Diffusion_Model_for_Text-to-Motion_Generation|Reconstruction-Anchored Diffusion]] 支持把 reconstruction 作为中间监督/采样锚点；[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion|Diffusion-Friendly Latent Manifold]] 明确提示 reconstruction quality 不自动推出 generation quality。它们与 StoryMotion representation、任务和 evaluator 不同，因此只用于提出 E0–E3，不用于宣称机制已经成立。

## 5. 核心 TODO

完整 contribution/claim 边界见 [[StoryMotion-iclr-reliability]]。当前只保留会改变主结论的任务：

1. **P0 — 做 Human heading/identity/decoder/manifold no-update attribution。**
   heading 拆 Stage1 floor、Stage2 excess、yaw/root/pose6d/RIFKE-local oracle 与
   invalid-tail leakage；Stage1 目前是高疑放大器，不预设为主要 capacity bottleneck。
2. **P0 — 仅按 attribution 命中证据授权一个单变量 Human 短训。**
   Human Stage2 objective、逐帧 relative Camera decoder、context adapter、
   decoded anchor 与 SNR target 不能合并；Human no-regression 保持硬边界。
3. **P0/P1 — task-row/context-role 只读归因。** ALL-JOINT endpoint 已就绪，但
   该 probe 只判断接口字段效力，不自动授权 VACE adapter。
4. **P1 — 重建 axis-pure v2 并闭合 Camera 质量轴。** v1 artifacts 保留；新 root
   用 min-n/backoff 拆 `q_H/q_C/q_HC` strata，Physical-v3 与 q_HC projection
   分开物化，再补 `q_CT`。在此之前不得训练或命名 clean Unified dataset。
5. **P1/P2 — Human 修复后再评 VACE 式分离控制面。** 保留 clean-H completion；
   condition value、role、source reliability、text presence 与 loss mask 分离，
   Camera adapter 只能作用于 Camera path。
6. **P2 — 数据增广只按 coverage 缺口启动。** 先验证 heading/decoder/padding 与
   size curve；HumanML3D 只允许未来做 source-heldout Direct-H dose screen，
   不能先进入 Stage1 joint、Direct-C 或 joint。
7. **P2 — 重做 seed23 与外推证据。** 正确的 seed23 repeat 与 sealed
   blind/no-reference evidence保持独立因果轴。

## 6. 文档与证据路由

- 当前主线、active blocker 与允许行动：本页。
- 版本家族、命名、目标、唯一操作、Stage 与已完成 steps：[[version_family]]。
- 已审计数值、fair comparison、valid-length geometry 与 hashes：[[StoryMotion-valid-metric-ledger]]。
- metric/evaluator/decoder 定义：[[StoryMotion-metric-computation-io]]。
- Stage2 screen/continue/stop gate：[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。
- v8.2333 curation contract 与全部零/非零计数：[[2026-07-17_storymotion-v8-2333-data-curation-plan]]。

run 中的 ETA、有限 step、worker output 和 checkpoint 只进入 `runs/` manifest/log；formal audit 后才更新 ledger、本页和 version family。

## Active evidence boundary — 2026-07-24

- v8.1C C3-25 seed17 仍是 formal `105K` mainline，但这是综合 Camera/joint-system
  选择，不代表 Human 已达到 Pareto 上限。
- Human-only 四个边界已闭合且未形成 semantic/distribution 改善；统一混训和
  Human dose 不是首要解释，下一主轴是 Human objective/heading/manifold。
- H-FULL、H-ISOLATED、C-JOINT、ALL-JOINT 四臂均已闭合；局部收益伴随跨端点代价，
  C/ALL 两臂 broad regress。四臂都不接管 architecture owner。
- Tb25-band r4 与 no-update Camera attribution 已闭合；没有确认 shared
  trunk/Camera path/output head 的负平均夹角，不授权全模型梯度手术。
- VACE 式分离控制面仍是设计先验，但 ALL-JOINT 已否定朴素 view equality；
  任何 adapter 都后移到 Human 修复之后，并保持 Human hard boundary。
- v8.2333 v1 quality gradients 与 `8K/16K/32K/64K` research pools 已物化但
  axis-purity 不足；新 v2 与 `q_C`、完整 `q_HC`、`q_CT` 仍是 clean-data blocker。
