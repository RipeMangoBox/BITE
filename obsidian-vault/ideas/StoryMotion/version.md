---
title: "StoryMotion Current Version"
status: active
hypothesis: |
  v7.38 L0 clean 105k 是当前唯一 formal E0 主线。v8.0 pure4053 channel oracle 已把 v7.14 的 Stage1 长序列退化定位到累计 yaw velocity，而不是 local-joint reconstruction；因此先在同一 non-causal human199 上训练 yaw/root geometry supervision，再独立验证 clean data 与 non-AR latent diffusion。v8 通过 Stage1 gate 前只是 candidate family，不覆盖 v7.14/v7.38。
tags:
  - StoryMotion
  - version
  - stage1
  - stage2
  - status/active
aliases:
  - StoryMotion-Current-Version
source_notes:
  - "[[history]]"
  - "[[2026-07-12_storymotion-valid-metric-ledger]]"
  - "[[2026-07-09_storymotion-metric-computation-io]]"
  - "[[2026-07-13_storymotion-runs-layout-rootcause-plan]]"
  - "[[2026-07-16_storymotion-v739-v741-core-experiment-decision]]"
  - "[[2026-07-17_storymotion-stage1-length-condmdi-causal-priority]]"
  - "[[2026-07-17_storymotion-fixed300-offline-ar-motionstreamer-v746-deployment]]"
  - "[[2026-07-17_storymotion-v8-yaw-quality-nonar-diffusion]]"
  - "[[2026-07-17_storymotion-v8-3-data-curation-plan]]"
  - "[[2026-07-17_storymotion-v8-3-data-curation-progress]]"
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness]]"
  - "[[analysis/CGF_2024/Cinematographic_Camera_Diffusion_Model]]"
  - "[[analysis/ICCV_2025/VACE_All-in-One_Video_Creation_and_Editing]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation]]"
  - "[[analysis/CVPR_2024/MoMask_Generative_Masked_Modeling_of_3D_Human_Motions]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI]]"
  - "[[analysis/arxiv_2025/MotionFlux_Efficient_Text_Guided_Motion_Generation_through_Rectified_Flow_Matching_and_Preference_Alignment]]"
  - "[[analysis/NEURIPS_2025/TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_Generation]]"
  - "[[analysis/ECCV_2024/Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation]]"
created: 2026-07-12T14:30:00+0800
updated: 2026-07-17T18:25:00+0800
---

# StoryMotion Current Version

> [!abstract] 当前裁决
> corrected v7.14 camera14 joint AE仍是实现上的Stage1 mainline，但不再视为长序列human质量已通过。v8.0 owning-decoder oracle 已进一步把问题收窄：193–256帧注入GT yaw后，root/global MPJPE从`132.22/429.43 mm`降到`8.68/38.99 mm`；local-joint channel oracle没有改善。root-aligned MPJPE没有移除heading，故此前的“local pose随长度恶化”主要是yaw误差。v8.1A human199 geometry loss、v8.1B matched residual AE 与 v8.2 human200 已按用户授权提前并行训练，但都尚无 endpoint geometry，不能据 early loss 晋级。camera Stage1 Cam-ADE约`41.8 mm`，而v7.38 Direct C/joint Cam-ADE为`1.51/2.91 m`，camera主要风险仍在Stage2。v8通过Stage1 gate前不覆盖v7.14/v7.38。

## 0. v8 candidate 已开启

完整方案、架构检索、数据清洗、预注册 gate 与 artifacts 见 [[2026-07-17_storymotion-v8-yaw-quality-nonar-diffusion]]。当前顺序固定为：

1. v8.1A 同结构 human199 yaw/root geometry loss；final 使用 `162,760 × 500 = 81.38M` sample exposures；
2. loss稳定但容量不足时才做 matched non-causal residual AE；
3. matched endpoint仍有heading slope才迁移到 non-integrative human200；
4. representation通过后，以 Motion Mamba-style latent DDPM 做第一条最小 non-AR pure-diffusion implementation，TransPhase作为严格 post-2024 long-composition control；
5. physical/semantic cleaning使用独立 immutable manifests，与representation/backbone分轴。

本地 Pulp/MARDM epoch320 reproduction 已完成 pure4053 screen但明确 No-Go：overall root/global=`286.82/953.45 mm`。它只说明现有 `30.53M` exposure、fixed64、feature-MSE checkpoint不能直接替代v7.14，不否定matched residual architecture；也确认feature MSE不能继续充当Stage1 checkpoint selection gate。

v8.1 yaw/root loss 的 `0.001/0.003` 已从 smoke 初值冻结为 final recipe。v8.1A/B 分别在 4090 GPU0 运行同一 `81.38M` exposure budget；v8.2 human200 使用独立 train-only stats、owning inverse 和 `camera64+human128` native latent order，在 GPU1 运行同预算。用户授权的提前并行覆盖了原始算力顺序，但不改变科学解释：三条是 system comparisons，必须分别通过 pure4053 geometry gate。v8.3 只有独立 plan/progress，因 v8.2 endpoint 晚于当日22:00而保持全部计数为0。

## 1. 文档职责与读表顺序

本页只回答“当前相信什么、claim 还缺什么、下一步如何选择”。不再保存逐 step 日志、旧假设演进或大段诊断曲线。

| 内容 | 唯一 owner | 使用规则 |
| --- | --- | --- |
| 当前结论、claim 与唯一 P0-G 状态 | 本页 | 其他活动页不得复制另一套结论 |
| 精确指标、version/run、checkpoint 与 artifact | [[2026-07-12_storymotion-valid-metric-ledger]] | 数值冲突时以 ledger 为准 |
| 当前 GPU、进度、ETA 与自动衔接 | [[2026-07-16_storymotion-v739-v741-core-experiment-decision]] | 只保存执行快照，不重复研究叙事 |
| 逐版本事实、bug 与删除 provenance | [[history]] | 历史事实不得覆盖当前决策 |
| 指标定义与 IO contract | [[2026-07-09_storymotion-metric-computation-io]] | 不从指标名猜测实现 |

状态词固定为：

- `已通过`：预注册 gate 已满足；
- `未通过`：有效实验完成但 gate 失败；
- `已完成`：artifact 完整，不自动等价于 claim 通过；
- `进行中`：训练或 formal pipeline 正在运行；
- `未完成`：没有足够有效证据；
- `已取消`：实验设计本身无效，不得复活其结论；
- `后置`：当前不占核心预算。

## 2. 固定任务与 claim

### 2.1 三种模式

| 模式 | 正式条件路径 | 当前主输出 |
| --- | --- | --- |
| human generation | human text → H | human-text-only；不得观察 camera latent |
| camera completion | observed/GT H + camera text → C | complete GT-H latent 为 StoryMotion contract |
| joint generation | paired text → H + C | 同一 Unified-3 checkpoint 的 directed parallel |

human-first cascade 先生成 H、再把 generated H 作为 camera source；当前 human 质量不足会产生显式误差传播，因此它退出活动路线和 promotion gate。已有 GT-H 时直接使用 camera completion；历史 cascade artifacts 只保留用于解释 source gap，不再要求新 treatment 重评。

### 2.2 表示与评测边界

- Stage1 固定为 corrected v7.14 camera14 joint AE：normalized human199 + official camera14、non-causal、human128 + camera64、owning local decoder。
- StoryMotion mainline、representation controls、cache、checkpoint loading 与 Unified eval 仍禁止 temporal causal tokenizer；唯一例外是外置 standalone MotionStreamer native baseline。该例外保留自己的 causal tokenizer/owning decoder，不能进入或 gate StoryMotion cache、Unified 或 representation control。
- formal development comparison 使用 official pure `4,053`、完整 decoded callback 与 run contract。该 split 已被多轮开发诊断消费，论文中不得再称 untouched final test；最终 treatment 锁定后需另冻 held-out final test。
- metric table 混合版本时，每一行必须有非空 `version / run`。camera9 separate 只作 control；camera14 separate 与 camera14 joint 永不合并。
- Stage1 formal必须同时报告human root-aligned/global MPJPE、root ADE/FDE，以及camera Cam-ADE/Cam-FDE、rotation geodesic，并按`1–64`、`65–128`、`129–192`、`193+`分bin。
- Stage2三种模式必须补任务适用的同组decoded geometry；自由text-to-motion的一对一MPJPE/Cam-ADE是mandatory diagnostic而非单独hard gate，GT held-out temporal completion/inpainting的masked-region误差才可直接作hard gate。缺少任务适用metric时artifact状态为不完整。

### 2.3 当前可写 claim

当前只允许写：

1. 一个 asymmetric Unified-3 checkpoint可运行human generation、camera completion与joint generation，并产出finite的distribution/semantic结果；这不等于decoded geometry或视觉质量已可用；
2. same-implementation evidence只支持shared training改善joint distribution/semantic/coverage，尚未覆盖MPJPE/Cam-ADE；
3. camera模式仍存在specialist gap，Director-C与L0在既有指标上是system-level Pareto；
4. human/joint几何可用性、三模式全面非劣、跨seed复现与最终external-peer优势均未成立。

### 2.4 CondMDI all-masked 与 Stage1 source 裁决

- CondMDI released training 以 `keyframe_mask_prob=0.1` 清空整条 observation mask，同时以 `cond_mask_prob=0.1` 做 text CFG dropout；若两者独立，text 保留且 observation 全空约占 `9%`。它在 HumanML3D 上明确支持 `edit_mode=uncond`，所以“CondMDI 架构只能补间、不能 all-masked generation”不成立；但这条能力仍需 official checkpoint 的 all-zero-mask 闭环与质量评测分开报告。
- official HumanML3D random-frames 750k checkpoint 的闭环已完成：`edit_mode=uncond`、saved observation-mask sum=`0`、72-frame motion全 finite且有非零时间方差/root displacement。sampling 结果已保存；随后 official visualization helper因 zero keyframe 报错，只是 renderer boundary bug。该 smoke 证明 capability，不证明 pure T2M quality，也不与 Pulp pure4053混表。
- StoryMotion L0 的 `human_first` 路由明确令 Direct H 的 human/camera latent observation mask 全零，只优化 human latent；`task_probs=[1,1,1,0]` 使 Direct H 约占三分之一 Stage2 slots。故 StoryMotion 的 all-mask exposure 不是更低，差异在于 CondMDI 还覆盖 partial observation，而 StoryMotion 没有按 mask 数量构造连续密度课程。released CondMDI `random_frames` 当前固定 20 个 keyframes，也不是显式的多 density bucket 配比。
- v7.42 human specialist只把 L0 从 `333.88/13.294/40.54%` 改到 `328.62/13.438/42.22%`。独占相同 branch implementation 与 matched exposure 仍只小幅改善，削弱了“主要是共享容量或梯度冲突”的解释，也使 residual/adapter 不再是默认修复。
- L0 使用的 v7.14 是本地训练 joint AE：normalized human199 + official camera14、non-causal、latent `128+64`、约 `0.96M` 参数、Smooth-L1 + velocity、完整变长序列与 `636k` updates。`run_config` 的 `seq_len=64` 只属于 synthetic 分支；真实 `synthetic=false` 数据没有 64-frame crop。official Pulp AE 是发布 checkpoint：同为 human199 + camera14、non-causal、latent `128+64`，但使用更深的 MARDM residual convolution、约 `3.20M` active parameters、ReLU/nearest-upsample，且训练数据、loss 与 checkpoint-selection recipe未公开。两者并非“只差数据量”；`94,050` 是已知 official Stage2 cache row 数，不是可核验的 official AE train-set size。
- pure4053 full-sequence reconstruction 的 valid length 为 `9–251` 帧。v7.14 local human root-aligned MPJPE 从 `1–64` 帧的 `70.8 mm` 升到 `193–251` 帧的 `132.0 mm`，global MPJPE 从 `146.8` 升到 `428.7 mm`；同样本 official AE 的 root-aligned MPJPE为 `85.4 → 78.0 mm`。因此当前 P0 是 local human length generalization/root drift，不是 crop bug。精确 contract 与 paired delta 见 [[2026-07-17_storymotion-stage1-length-condmdi-causal-priority#3. 64-frame 问题：代码事实与 full-sequence 证据]]。
- 同权重 true-length/fixed-300 pure4053审计已进一步排除“测试时补零即可修复”：official AE 的 fixed − true root-aligned MPJPE overall/short/long 为 `−1.60/−2.70/−0.28 mm`，而 v7.14 为 `+5.03/+2.22/+8.97 mm`；v7.14 global overall也恶化 `+14.04 mm`。fixed-300 不是普适 MPJPE优势；v7.44 只测试按该 context重新训练能否对齐 Stage1 fit 与 Stage2 cache。
- v7.44 已完成636k/81.38M matched exposure并否定该training treatment：overall root/global=`82.58/218.21 mm`，193–251帧为`137.60/458.67 mm`，比v7.14同bin再差`5.56/29.93 mm`；fixed-max与true-length inference overall只差`−0.25/−0.09 mm`。因此不构建v7.44 cache。其camera Cam-ADE/rotation为`41.48 mm/0.619°`，official AE为`137.45 mm/1.792°`，当前Stage1主风险明确集中于human long/root drift。
- pure4053 reconstruction 上，本地 v7.14 AE 的 FDTMR/FDCLaTr/coverage/F1 明显优于 official AE，但 official AE 的 TMR `15.94 > 14.99`、Out `3.5% < 5.1%`。重建强不等于 latent 更易生成；历史 v7.17 10k screen 反而显示 official latent 的 Stage2 learnability 更好，但与当前 L0 recipe/budget不匹配，只能支持新的 representation control，不能直接决定换回 official tokenizer。
- temporal convolution没有时长上限不蕴含误差对时长不变：局部root velocity/heading偏差会在世界坐标积分成global drift，边界比例、低频行为和长动作内容难度也会变化。当前bin是不同样本的横截面，不能把相关性写成纯长度因果；但同一ordered IDs上official/local曲线显著分离，足以否定“这是不可避免的长序列现象”。
- Stage2存在独立world-root trajectory风险。pure4053中v7.45相对v7.38把FDTMR/TMR/HCov从`333.88/13.294/40.54%`改善到`149.16/17.729/49.86%`，root-aligned MPJPE从`250.4`降到`242.5 mm`；但global MPJPE从`863.1`升到`1249.1 mm`，最长bin从`1294.3`升到`2412.7 mm`。因此v7.45未通过geometry promotion且不扩展camera/joint。两者Stage2 operator/text encoder/exposure/sampler不同，加上自由T2M一对多，不能把该Pareto写成CondMDI架构能力的严格单变量结论；representation责任仍等v7.47。
- v7.38 L0三模式geometry已完成：Direct H root/global=`250.36/863.11 mm`；Direct C Cam-ADE/FDE/rotation=`1.512/1.606 m/32.93°`；joint为human root/global=`252.67/842.30 mm`、camera=`2.912/3.026 m/72.93°`。这与其既有distribution/semantic formal同时成立，直接关闭“现有统计可代表视觉质量”的假设。由于三任务自由生成均是一对多，paired geometry不设事后hard threshold；当前状态是decoded-quality claim不成立，而不是用单GT距离证明所有输出必然不自然。

## 3. StoryMotion 与 baseline/specialist 的公平对比

比较分三层：

| tier | 定义 | 可支持的结论 |
| --- | --- | --- |
| A | 与 Unified-3 共享 Stage1、branch implementation、cache、初始化与 evaluator，只改变 task exposure | shared-vs-specialist 归因 |
| B | 复用 corrected v7.14 latent、同 split 与 evaluator，但保留 baseline generator/objective | representation-matched system comparison |
| C | 同任务、同 pure split、同 official callback，保留方法自身 representation 与 sampler | native-system peer；不得作单变量归因 |

未完成 row 保留 placeholder；screen、smoke、旧错标 checkpoint 或不同 split 不得填入。

v7.43 B/C 是 routing/joint-exposure 的 matched attribution controls，不是 baseline 或 specialist，因此不放入本节三张 peer table；其 H/C/parallel/cascade formal 到达后进入 attribution ledger 与 claim 状态。

### 3.1 Human generation

![[2026-07-12_storymotion-valid-metric-ledger#^fair-human-comparison]]

结论：

- human specialist 相对 L0 的 FDTMR `-5.26`、TMR `+0.144`、HCov `+1.68 pp`，是轻微但方向一致的优势；没有预注册 non-inferiority margin/CI，不能写 Unified human 已非劣。
- MotionLab-MFT formal与geometry补审均已完成：FDTMR/TMR/HCov=`156.35/18.172/59.19%`，相对L0三项全面改善；root-aligned/global MPJPE=`250.78/951.38 mm`、root ADE/FDE=`857.64/1436.40 mm`，相对L0分别变化`+0.42/+88.27/+88.37/+156.33 mm`。因此Direct-H semantic/distribution external gap成立，但MotionLab没有修复world-root trajectory，不能按decoded geometry晋级。
- MoMask-Pulp 已完成 secondary native-operator peer 的三阶段训练：Pulp human199、human-text-only、non-causal RVQ + 双向 Mask/Residual Transformer。VQ 以 v7.14 Stage1 sample exposure 对齐到 `159k × 512 = 81.408M`；Mask/Residual 各为 `240k × 64 = 15.36M`。VQ/Mask/Residual endpoint SHA256分别为`e21d4268…8664`、`03787132…f3c`、`89faab30…0b1`；当前没有formal/eval artifact，因此仍不能产生性能结论。
- MotionStreamer 已按用户显式授权作为独立 native diagnostic 放行：Pulp normalized human199、causal TAE、随机 64-frame crop、短序列补零并 mask，Stage1 使用同一 `162,760 × 500 = 81.38M` sample exposures。它不进入 StoryMotion invariants/cache/Unified，也不能替代 MotionLab 或 MoMask-Pulp 的证据角色；当前只训练 Stage1，Stage2/formal 尚未完成。

### 3.2 Camera completion

![[2026-07-12_storymotion-valid-metric-ledger#^fair-camera-comparison]]

结论：

- camera specialist 相对 L0 的 FDCLaTr `-0.23`、CLaTr `+2.694`、CCov `+3.40 pp`、Caption F1 `+0.035`，说明 direct camera 存在明确 specialist gap。
- Director-C 相对 L0 的 FDCLaTr 约 `-0.86`、CCov `+8.26 pp`，但 CLaTr 约 `-2.98`、Caption F1 约 `-0.027`。二者是 Pareto，不能写任一方全面胜出。
- Director-C 使用 GT pelvis translation trajectory、native 9D camera target 与 EDM10；L0 使用 complete GT-H latent、camera14 joint latent 与 DDIM50。相同 pure IDs 与 official callback 使它成为合法 system peer，但不使它成为 representation-matched ablation。
- 第二 camera peer CCD-Pulp 已完成：FDCLaTr `101.03`、CLaTr `33.095`、CCov `59.91%`、Caption F1 `0.442`。L0 四项分别领先 `67.74`、`22.545`、`13.32 pp` 与 `0.273`，因此 L0 对该 representation-matched external operator 是四项主指标 dominance。
- CCD-Pulp 属于 tier B task port：保留 CCD 四层 Transformer、linear DDPM1000、epsilon objective、Adam `1e-4`、text dropout 与 CFG `2`；输入 corrected v7.14 complete GT-H latent 与 camera text，只预测 camera latent，并由 owning non-causal decoder 解码。固定预算为 `60k × 256 = 15.36M` exposures；generator architecture、objective、预算与 CFG 仍不同，因此不能写成单变量消融。
- 旧 E.T./Director 行实际读取 StoryMotion checkpoint，旧 Director fit 又含 test-as-validation；这些结果已删除且不出现在 placeholder 中。

### 3.3 Joint generation

![[2026-07-12_storymotion-valid-metric-ledger#^fair-joint-comparison]]

结论：

- L0 parallel 相对 joint specialist 的 FDTMR、TMR、HCov、FDCLaTr、CLaTr 与 CCov 均更好；specialist 的 Out 低 `2.36 pp`，Caption F1 仅高 `0.001`。这支持 shared-training joint benefit，但不是逐指标全面 dominance。
- L0 parallel 与旧 cascade 共享 checkpoint并曾形成指标 Pareto；但 cascade 的 generated-H source 会传播当前 human error，现只作为历史 source-gap 诊断，不再进入活动主张或 promotion。
- v7.43-C 与 L0 匹配到同一 final budget，但将 joint loss 固定为 `0`；其 direct H、direct C 与 human-first cascade 的 distribution、semantics、coverage、Caption F1 均回退，cascade Out 也从 `13.95%` 升至 `17.94%`。这关闭了“completion-only 可替代 joint exposure”的假设，支持显式 joint training 对三种输出的正迁移。
- 相对 Pulp official native rows，L0 在 distribution、coverage、camera semantics、Caption F1 与 framing 上占优；Pulp 的 TMR 更高。由于 AE、objective 与 sampler 不同，这仍是系统级 Pareto，不是 objective 单变量消融。
- v7.40 RF formal 是 StoryMotion 内部 architecture challenger，不是 external baseline；其 direct/cascade semantic-recall 改善与 parallel/coverage/framing 回退见 ledger 第 16 节。formal promotion 未通过，不能替换 L0。

## 4. P0-G：raw/decoded auxiliary 的唯一状态

本节是 P0-G 的唯一活动表述；旧别名 `P0-R` 停用。

| 子问题 | 状态 | 有效证据 | 当前结论 |
| --- | --- | --- | --- |
| 旧 teacher-forced one-step `P0-G(raw-loss)` gate | 已取消 | 只有 GT/noisy latent 的单步 decoded 曲线；没有 training treatment、raw/decoded auxiliary、optimizer step 或新 checkpoint | gate 设计无效，不能判 Go/No-Go |
| broad raw-loss 裁决 | 未完成（尚未裁决；旧 No-Go 已撤回） | 旧 gate 不足以否定可训练 auxiliary | 不是“已通过”，也不是“未通过” |
| matched O0/O1/O2 Stage2 training screen | 未完成；未启动 | O0 latent-only、O1 decoded feature/velocity、O2 normalized raw-GT 尚无 matched train/full reverse | 当前不占卡 |
| raw/decoded auxiliary promotion | 未完成 | 尚无梯度比例、full-sampler decoded quality 与 blind render | 只有 O1/O2 胜过 O0 且无 broad regression 才可标已通过 |

> [!important] 一句话状态
> P0-G 整体为**未完成、尚未裁决**；旧 one-step gate 是**已取消**，不是“raw-loss 未通过”。

若未来重启，必须从同一 parent、seed、cache、steps 与 sampler 运行 O0/O1/O2；记录实际 loss weight、主/辅梯度比例、checkpoint hash，并用 full reverse、human/camera/joint decoded metrics、jitter 与 random blind render 裁决。`2%/5%` 只能作为待 screen 初值，不是既有合理权重。

P0-G 后置于 MotionLab geometry、MoMask-Pulp formal 与 seed17 final recipe 锁定；它不能借用 latent-only L0 的 B/C controls 证明新 objective 的 routing/joint 因果性。

## 5. 当前证据闭环

| item | 状态 | 当前裁决 / 缺口 |
| --- | --- | --- |
| corrected v7.14 Stage1 | contract通过；long-human质量未通过 | non-causal assertion与owning decoder固定；human `193–251`帧root/global=`132.0/428.7 mm`。仍是实现mainline，不支撑长程quality claim |
| v7.44 fixed-300 Stage1 | 已完成；promotion未通过 | 636k/81.38M；overall root/global=`82.58/218.21 mm`，193+为`137.60/458.67 mm`；不构建Stage2 cache。camera Cam-ADE=`41.48 mm` |
| v8.1A human199 geometry Stage1 | 进行中；无endpoint结论 | frozen yaw/root=`0.001/0.003`；GPU0 matched `636k/81.38M`；pure4053 geometry已排队 |
| v8.1B residual human199 Stage1 | 进行中；用户授权提前 | 与A共用IDs/budget/loss并从零训练；GPU0共驻；只能作两因素system comparison，pure4053 geometry已排队 |
| v8.2 human200 Stage1 | 进行中；contract preflight通过 | GPU1 matched `636k/81.38M`；train-only stats覆盖162,760 IDs/19,336,840 frames；新owning decoder/cache contract，不兼容v7.14 |
| v8.3 data curation | 已预注册；未启动 | 22:00 endpoint gate closed；processed/annotated/quarantined/manifests/jobs均为0 |
| CondMDI official all-mask smoke | 已完成 capability闭环 | HumanML3D random-frames 750k；`edit_mode=uncond`；saved mask sum=`0`；motion finite且非静态；不产生 Pulp quality结论 |
| MotionStreamer Pulp Stage1 | 已完成；standalone exception | 636k/81.38M；pure4053 overall root/global=`79.94/281.52 mm`，193+为`96.53/414.17 mm`；不作为 StoryMotion causality ablation |
| v7.46 official AE × Unified | step10k screen与post-stop pure4053完成；gate contract待修 | pure4053 HCov=`22.72%`、CCov=`80.48%`；joint H/C coverage=`32.15/45.62%`、Out=`22.34%`。stop仅因H/C不产出Out且缺失值被判失败；不能标105k formal |
| v7.47 official AE × Unified | corrected 10k gate已通过；继续105k | N64 H/C/joint适用coverage=`81.41%/100%/84.36%+82.95%`，joint Out=`14.36%`；只证明结构可学，不是formal representation结论 |
| v7.38 L0 clean 105k | distribution/semantic与三模式geometry均已完成；decoded-quality claim不成立 | 唯一E0 implementation mainline；single training seed；paired geometry量级大且尚无blind/physical gate，不能写视觉已可用 |
| v7.38 L0 geometry re-audit | 已完成 | Direct H root/global=`250/863 mm`；Direct C Cam-ADE=`1.51 m`；joint human root/global=`253/842 mm`、Cam-ADE=`2.91 m`；三项各4,053 records |
| v7.45 offline Direct H | 训练/formal已完成；promotion未通过 | FDTMR/TMR/HCov与root-aligned MPJPE改善，但global MPJPE=`1249.1 mm`、root ADE=`1164.2 mm`；停止human-only，不扩展camera/joint |
| v7.40 full-sequence RF | 已完成；promotion 未通过 | 只保留 semantic/recall Pareto challenger |
| v7.42 H/C/J specialists | 已完成 | human 轻微 specialist 优势；camera specialist 优势；shared-training joint benefit |
| Director-C camera peer | 已完成；formal artifact audit 通过 | camera system-level Pareto；Director 任务已释放 |
| CCD-Pulp camera peer | 已完成；formal artifact audit 通过 | L0 的 FDCLaTr、CLaTr、CCov 与 Caption F1 全部占优；4090 GPU1 已释放 |
| MotionLab-MFT human peer | formal与geometry补审已完成 | FDTMR/TMR/HCov三项胜L0；root/global=`250.78/951.38 mm`，global/root trajectory反而差于L0，semantic/geometry Pareto |
| MoMask-Pulp human peer | 三阶段训练已完成；formal待部署 | tier-C native-operator；Stage1-matched VQ `159k`→Mask `240k`→Residual `240k` endpoints齐全，尚无pure4053 artifact |
| v7.43 B symmetric final-budget control | 已完成 | camera/joint broad regression；支持 asymmetric routing，symmetric human 不入 human-text-only 主表 |
| v7.43 C no-joint final-budget control | 已完成 | H/C 与历史 cascade 全部 broad regression；支持 joint exposure，不恢复 completion-only recipe |
| L0 joint per-sample Top-5 | 已完成 | 第一行 StoryMotion GT/recon/gen；第二行 v7.42 joint specialist gen、Pulp recon、Pulp Aux gen；aggregate 表含两条 Pulp baseline |
| independent seeds 23/29 | 后置 | seed17 final recipe 锁定后从零训练；不继承 seed17 parent |
| blind study / held-out final test | 未完成 | 自动指标与视觉 naturalness 的最终外部效度仍开放 |

因此 paper-level claim 目前只能写成“单 checkpoint可运行三模式，并在distribution/semantic层面具有分层Pareto与routing/joint-exposure归因证据；camera completion在既有非几何主指标上胜CCD-Pulp、与Director-C构成Pareto”。这不是decoded human/joint视觉质量已成立，更不是“所有模式优于specialist/baseline”。geometry、Human external peers、completion specialist gap、独立seeds与blind study任一未处理，都不允许升级为全面统一优越性。

## 6. 下一步选择规则

当前处于“验证 Stage2 生成骨干与 latent representation”的根因阶段。`promotion gate` 不再把所有 baseline 混成一个阈值，含义固定如下：

1. **Hard gate 只比较 matched StoryMotion rows**：Direct H 候选相对 L0 必须在 FDTMR、TMR、HCov 至少两项改善，第三项不得出现超出预注册 margin/CI 的退化；Direct C 候选在 FDCLaTr、CLaTr、CCov、Caption F1 至少三项改善，其余项与几何/in-frame 不得显著退化；joint parallel 相对 L0 的 H/C distribution、semantics、coverage、Caption F1 与 Out 不得出现跨多项的显著回退。Cascade 不参与。
2. **Specialist 是 matched gap reference，不是另一个强制阈值**：v7.42 H/C specialist回答“去掉多任务共享最多能改善多少”。候选若超过 specialist当然最好；若只显著胜 L0，也可晋级到下一阶段。Director、CCD、MotionLab、MoMask保留各自 representation/sampler，只用于论文系统比较，绝不拿来定义内部训练是否通过。
3. **Stage1 length/representation已完成一轮否证**：v7.44 fixed-300未通过，不建cache。下一条local Stage1 treatment必须改变human architecture/loss或root/global trajectory建模；不能再次只改padding context。
4. **matched Stage2 representation control改由v7.47回答**：冻结official Pulp non-causal AE，复用matched `162,760/4,053` cache，并匹配L0的train-only full-cov normalization、human-first Unified architecture、两阶段LR、sampler与`105k × 512` budget。v7.46只保留错误gate的10k diagnostic；v7.47从step0执行corrected gate并最终只用pure4053裁决。
5. **generation-native Stage2 human-only已裁决为Pareto/未通过**：v7.45改善distribution/semantics与local pose，但world-root trajectory broad regression；不设计camera/joint integration。它不否定其他generator，下一条Stage2改动必须显式建模或约束root trajectory，并与blind render一起评估。
6. **闭合与复现**：MotionLab-MFT geometry已闭合；下一步完成MoMask-Pulp formal adapter/评测和几何Top-5。锁定通过上述hard gate的parallel recipe后，从零训练seed23，再决定seed29，最后冻结held-out final test并做blind study。

GPU当前状态：4090 GPU0 共驻 v8.1A/v8.1B，GPU1 独占 v8.2；GPU1 上另有只等待 endpoint 的串行 pure4053 geometry queue，不会与训练抢占。5090仅GPU0可用并运行v7.47；不得调度5090 GPU1/2/3。v8.3 gate closed，不占GPU。精确run、step、吞吐与ETA见 [[2026-07-16_storymotion-v739-v741-core-experiment-decision]]；历史v7.44–v7.47部署见 [[2026-07-17_storymotion-fixed300-offline-ar-motionstreamer-v746-deployment]]。

2026-07-17 03:28 CST 四卡部署验收已完成，但长训未完成：v7.44 已完成 pure4053 step-0 并到 train step14；v7.45 human-only train/eval/test step-1均 finite；v7.46 已到 step200且三任务 exposure=`102,400`；MotionStreamer 已到 step1400且 loss持续下降。对应 contract SHA、PID、cache hash、失败重启审计与首步数值以该 canonical deployment note 为准。

2026-07-17 11:45 CST endpoint复核修正了上一快照：MotionStreamer 已完成；v7.46 只到step10k并因gate/evaluator缺失指标不一致停止，未进入105k。GPU0/1 post-stop pure4053三模式已完成且指标finite；不得把 `screen_stopped` 写成representation失败或full endpoint完成。

2026-07-17 14:10 CST：v7.44 human length gate失败；v7.45 formal完成并形成semantic/local-pose改善、global-root退化的Pareto，未通过promotion。v7.38 joint→Direct-C geometry仍在第二张4090串行重评。corrected v7.47已在唯一可用5090 GPU0从零训练；截至该快照尚无完整official-tokenizer Unified Stage2 endpoint。

2026-07-17 14:17 CST：v7.38 Direct H/Direct C/joint geometry全部完成，4090双卡释放。human与camera的Stage2 paired geometry均远大于Stage1 reconstruction；旧distribution/semantic formal保留，但decoded-quality claim明确降级为未成立。v7.47继续独占5090 GPU0。

2026-07-17 18:25 CST：v8.1A/B已在GPU0到step54,441/29,268，v8.2已在GPU1到step6,133；三条train/test、grad与checkpoint均finite。按近5k吞吐，v8.2/A/B连同queued geometry预计分别在07-18 03:40–04:20、04:45–05:20、08:15–09:15 CST闭合。这是部署/ETA，不是性能结果；v8.3仍为零进度。

## 7. 已删除或降级的活动证据

- v7.15–v7.16 wrong decoder、causal cache 与漂移 normalization 结果只留 forensic history，不进入当前结论。
- 缺少精确 `version / run` 的 legacy camera9-joint 数值已从 canonical ledger 删除。
- Pulp official Stage2 旧汇总值已由可核验的 2026-06-16 pure4053 no-Aux/Aux artifacts 替换。
- 旧 E.T./Director 错标指标、数值发散 runs、test-as-validation runs 与派生 shuffle views 已删除；只接受 corrected Director-C fixed endpoint。
- N64、latent loss、teacher-forced single-step 与 bridge smoke 都不能替代 pure4053 formal；不再在当前版本页复制其数值。
- v7.39/v7.41 未满足 formal gate，只保留在 history/ledger 的诊断边界，不占当前主表。

## 8. 不可破坏的边界

- 不恢复 **StoryMotion** causal Stage1，不加载 causal tokenizer/cache/checkpoint 进入 StoryMotion Stage1/Stage2/Unified train 或 eval；standalone MotionStreamer native baseline只能使用自己的 causal contract与 owning decoder。
- 不把 camera14 separate 与 camera14 joint 证据合并，不把 camera9 control 外推为 mainline。
- 不把 observed-camera→human symmetric control 写成 human-text-only generation。
- 不把 native-system peer 写成 representation-matched ablation。
- 不训练与 Unified-3 无实现或权重联系的 specialist 来替代 same-implementation gate。
- 不用 pure4053 的反复开发结果宣称 untouched final test。
- 不用 P0-G 单步曲线写 raw-loss 已通过或未通过。
