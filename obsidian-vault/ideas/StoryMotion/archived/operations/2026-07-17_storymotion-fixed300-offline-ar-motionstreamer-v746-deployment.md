---
title: "StoryMotion Fixed-300, Offline AR, MotionStreamer, and v7.46 Deployment Snapshot"
status: archived
hypothesis: |
  Pulp official Stage1 与 v7.14 的关键差异之一是 encoder 输入上下文：Pulp 对每条序列固定到 300 帧并只在 loss/eval mask 无效区，v7.14 则动态 pad 到 batch 最大长度。由于当前 Pulp train/test 最长分别不超过 251 帧，fixed-300 不引入截断，只改变零尾上下文。应先用同一权重做 true-length/fixed-300 成对审计，再训练 matched fixed-300 variant；并用 official AE × same Unified Stage2 隔离 representation generatability。
tags:
  - StoryMotion
  - stage1
  - stage2
  - baseline
  - experiment
  - decision
  - status/archived
aliases:
  - StoryMotion-Fixed300-OfflineAR-MotionStreamer-v746
source_notes:
  - "[[current]]"
  - "[[version_family]]"
  - "[[2026-07-17_storymotion-stage1-length-condmdi-causal-priority]]"
created: 2026-07-17T03:05:00+0800
updated: 2026-07-18T15:20:00+08:00
archived_at: 2026-07-18T15:20:00+08:00
superseded_by:
  - "[[current]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
---

# StoryMotion Fixed-300, Offline AR, MotionStreamer, and v7.46 Deployment Snapshot

> [!warning] Archived deployment snapshot
> 这是一份已闭合的 2026-07-17 部署/执行快照，不再维护 live queue、GPU、ETA 或 current decision。当前结论见 [[current]]；正式数值见 [[StoryMotion-valid-metric-ledger]]；v8 的下一步见 [[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。

> [!abstract] 当时裁决
> v7.44 已完成并否定 fixed-300 training treatment：相对 v7.14，human 的四个长度 bin 没有改善，最长 bin 还进一步退化；因此不构建 v7.44 Stage2 cache。camera Stage1 的 Cam-ADE 约 `41.5 mm` 且随长度稳定，明显优于 official AE 的 `137.4 mm`，所以当前 representation 风险集中在 local human 的长程/root trajectory，而不是 human/camera 一起失效。
>
> v7.45 offline masked-iterative Direct H 的 `240k × 64` 与 pure4053 formal均已完成：distribution/semantics/coverage和root-aligned MPJPE改善，但global MPJPE、root ADE/FDE严重恶化，形成明确Pareto且未通过geometry promotion，不扩展camera/joint。v7.38 L0 的Direct H、Direct C与joint geometry已全部补齐：paired Cam-ADE为Direct C `1.51 m`、joint `2.91 m`，而Stage1 reconstruction只有`41.5 mm`，所以camera当前主要是Stage2生成/条件路径风险。v7.46仍只是错误gate停在10k；真正的official-tokenizer isolation是唯一可用5090 GPU0上从零训练的v7.47，corrected 10k gate已通过并继续105k。

> [!important] 2026-07-18 execution correction
> v7.47 已完成 step105k 与 Direct-H、Direct-C、joint parallel、human-first cascade 四个 pure4053 profile。driver 只回传了 JSON/records SHA；普通 5090 SSH root 暂看不到 runner chroot overlay 中的 raw artifacts。因此本页此前所有“继续105k”“GPU0正在执行”的快照均已过期，execution 完成不等于 audit 或 representation 结论通过。

## 1. Pulp fixed maximum 与 mask 的代码事实

Pulp 的公开数据配置固定 `num_frames=300`。human/camera dataset 对不足 300 帧的序列右补零，对超过 300 帧的序列截断，并产生 padding mask；投影/joint feature builder 会把无效区清零。official AEMMARDM 的 `encode` 不读取 mask，因此 convolution encoder 实际看到的是“有效段 + 归一化 feature-space 零尾”；mask 在 reconstruction loss、metric 与下游有效 latent frame 中排除无覆盖区。

StoryMotion v7.14 的真实数据分支没有 64-frame crop。它按完整序列加载，collate 只 pad 到当前 batch 最大长度，loss mask 无效区。两者都 mask loss，但 encoder 的右侧上下文不同。

当前 matched 数据的边界是：

- train 为 `162,760` 个 ordered IDs，valid length `5–251`；
- pure test 为 `4,053` 个 IDs，valid length `9–251`；
- 没有任何样本超过 300，因此本轮 fixed-300 treatment **不会截断**，只改变统一零尾上下文；
- corrected v7.14 Stage2 cache 的 latent shape 为 `162760 × 192 × 75`，说明 cache 构建端已经沿用 Pulp fixed-300 输入边界，而原 v7.14 Stage1 fit 使用 dynamic batch-max。该 Stage1 fit / Stage2 cache 上下文不一致本身就是需要闭合的 contract 风险。

### 1.1 “fixed-300 是否使 MPJPE 更优”如何回答

必须分开两个问题：

1. **同一权重的 inference context effect**：对 local v7.14 与 official Pulp AE 分别比较 true-length 和 fixed-300，一条序列只做一次完整 encode/decode，所有 MPJPE 只统计 valid frames。这回答零尾上下文本身如何改变短/长重建。
2. **training treatment effect**：用 v7.14 原结构、原 loss、原 seed、原 `162,760 × 500` 暴露，只把 collate 改为 fixed-300 + masked loss，再做相同 pure4053 length bins。这才回答固定上下文训练是否修复长序列。

不能用 official AE 优于 local v7.14 的历史结果直接归因 fixed-300，因为两者还同时不同于网络深度、residual topology、参数量、训练 recipe 与 checkpoint selection。

成对审计 artifact 预注册为：

`runs/train/stage1/v7_14_official_contract_20260710/joint_ae_official_4090_gpu0_r2/eval/length_context_fixed300_vs_true_pure4053_20260717.json`

该 artifact 已完成，SHA256=`e4134b28c26de8db1d7237c509bf775517ad1845a75dc75ad792638c3313c080`；script SHA256=`6b6ad9a626c0e1ec75be9985d4d53881105d192fbc2981a019f91af4ed986180`。它包含 local/official × true/fixed 四个 source、同一 `4,053` IDs、`16,212` records、short/long bins 与 paired delta，所有指标 finite。

下表是 fixed-300 减 true-length 的 paired delta，单位 mm；负值才是 fixed-300 更好。

| model / context delta | 1–64 root / global | 65–128 | 129–192 | 193–251 | overall |
| --- | ---: | ---: | ---: | ---: | ---: |
| v7.14 fixed − true | `+2.22 / +5.96` | `+5.52 / +16.74` | `+11.34 / +39.47` | `+8.97 / +11.86` | `+5.03 / +14.04` |
| official fixed − true | `−2.70 / −1.54` | `−0.93 / −0.26` | `−0.43 / −0.08` | `−0.28 / +0.05` | `−1.60 / −0.78` |

> [!important] 成对裁决
> fixed-300 对已经按该输入边界训练的 official AE 只有小幅 short/overall收益，最长 bin 基本不变；把 dynamic-context 训练的 v7.14 同一权重直接切到 fixed-300 则四个 root-aligned bins 全部恶化。故 fixed-300 不是动作 MPJPE 的普适优势，也不能解释 official 的长序列优势。v7.44 的价值是测试 **training treatment / fit-cache contract alignment**，不是把 inference padding 当成修复。

## 2. Online 与 offline 的核心区别

| 维度 | online / streaming | offline full-sequence |
| --- | --- | --- |
| 可用信息 | 时刻 `t` 只能使用已到达的 prompt、motion prefix 与状态 | 开始生成前可读取完整 prompt、目标长度与全局条件 |
| temporal operator | encoder/decoder 与 generator 必须保证因果可用性；未来 token 不得改变已输出 token | 可使用双向 self-attention、全局 mask schedule、反复修订未定 token |
| 输出时机 | 首块低延迟输出，后续增量生成；需要 bounded state/KV cache | 完整 latent sequence 生成后统一 decode；不承诺首帧延迟或流式一致性 |
| 错误修订 | 已提交 prefix 通常不能被未来信息重写 | sampling 期间可用全局上下文反复修订整段 latent |
| 评价重点 | latency、real-time factor、prefix consistency、long-horizon drift | full-sequence quality、semantic alignment、coverage、global coherence |

StoryMotion v7.14 Stage1 是 non-causal，因此不能支持真正 streaming claim；但它不妨碍 Stage2 在 latent grid 上训练离线生成器。MoLingo operator 可改写为 offline masked-iterative RF：保留 frozen T5-large multi-token text、cross-attention 与 token-wise RF head，使用 cosine-ratio temporal masks 和双向 clean-token context，从零训练 v7.14 `human128` target。它不是严格 left-to-right AR，也不能复用 official MoLingo checkpoint；准确名称是 **offline masked-iterative autoregressive-style RF**。

本轮只训 human-only Direct H，固定 `240,000 × 64 = 15.36M` generation-component exposures。它不观察 camera latent，不扩展 camera/joint；只有 human screen/formal 显示有效后才设计 joint token layout。

## 3. MotionStreamer × Pulp 的独立边界

用户已显式授权修改 causal contract，但例外被限制为 standalone native baseline：

- MotionStreamer 保留 causal TAE、owning causal decoder 与随机 64-frame crop；
- representation 改为 Pulp normalized human199，任务是 human text → human motion；
- 所有 `162,760` train IDs 都保留。短于 64 帧的序列右补零并 mask reconstruction/root/KL，长序列每次 exposure 随机 crop；
- batch size `128`、500 个完整 data passes，与 v7.14 一样为精确 `162,760 × 500 = 81,380,000` sample exposures；不能把名义 `636,000 × 128 = 81.408M` 当成实际暴露，因为每个 epoch 最后一个 batch 只有 24；
- append-only `metrics.jsonl` 与 TensorBoard 持续记录 reconstruction、KL、root loss、LR、sample exposure，以及 full-valid-sequence short/long root-aligned/global MPJPE；
- checkpoint/cache/decoder 归 MotionStreamer 所有，不得进入或 gate StoryMotion Unified-3。

Stage2 adapter 固定为 released MotionStreamer offline text-to-motion path：owning causal TAE full-sequence latent、end latent、LLaMA/two-forward diffusion head 与 human caption。按用户要求，本轮只训练 Stage1；Stage2 不在 Stage1 endpoint reconstruction gate 前启动。

## 4. 为什么 official AE × Unified 先短训

10k 不是为了用 test 指标挑 checkpoint，也不是以短训代替 105k 结论。它只检查一次 representation switch 是否满足：

- cache basis、train-only full-cov normalization 与 owning official decoder 全部一致；
- loss/gradient/metrics finite，三种 task 都获得非零 exposure；
- N64 Direct H、Direct C 与 joint parallel 不发生结构性 collapse；
- 预注册宽松门槛为相关 TMR/CLaTr coverage `≥ 20%`、Out `≤ 70%`。

这类错误在 10k 前已经可见，而 full endpoint 为 `105,000 × 512 = 53.76M` task assignments；先做结构 gate 可避免在 decoder/basis 接错时浪费约九成计算。门槛通过后必须从同一个 step10k checkpoint、optimizer 与 RNG lineage继续：`0–30k` 使用 L0 parent recipe 的 `lr=1e-4`，`30k–105k` 使用 `lr=3e-5`。最终裁决只接受 pure4053 owning-decoder H/C/joint artifacts，N64 不进入 formal table。

历史 v7.17 official-AE 10k 只训练 joint，且 routing、normalization 与当前 L0 不同，所以只能支持“official latent 可能可学”，不能替代 v7.46 matched screen。

## 5. 四卡部署与优先级

| priority | host / GPU | run | fixed budget / gate | 证据角色 | 状态 |
| --- | --- | --- | --- | --- | --- |
| P0 | 5090 / GPU3 | fixed-300 same-weight pure4053 audit | 4,053 paired IDs；四 source | 决定零尾 inference context effect | 已完成；official小幅改善，v7.14同权重恶化 |
| P0 | 4090 / GPU1 | `v7_44_joint_ae_fixed300_masked_seed17_4090g1_20260717` | `162,760 × 500`；bs128 | dynamic vs fixed-300 Stage1 treatment | 已完成；pure4053 human long-bin退化，未通过promotion |
| P1 | 5090 / GPU3 | `v7_46_official_ae_unified_matched_seed17_5090g3_20260717` | 10k N64 gate → 30k → 105k → pure4053 | frozen representation isolation | 10k screen与post-stop pure4053完成；contract待裁决，未进入105k |
| P1 | 4090 / GPU0 | `v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717` | `240k × 64 = 15.36M` | v7.14 latent 的 offline Direct-H generator | 训练/formal已完成；semantic与local-pose改善但global-root严重退化，未通过promotion |
| P1 | 5090 / GPU0 | `v7_47_official_ae_unified_matched_seed17_5090g0_20260717` | corrected 10k gate → 30k → 105k → pure4053 | frozen representation isolation | 10k gate已通过，继续30k/105k；只占用当前唯一可用5090 GPU0 |
| P1 baseline | 5090 / GPU0 | `motionstreamer_pulp_stage1_500ep_seed17_5090g0_20260717` | `162,760 × 500`；bs128 | standalone native causal Direct-H Stage1 | 已完成636k/81.38M与pure4053重建评测 |

当前资源约束为4090 GPU0/1可用、5090仅GPU0可用。v7.45、v7.38与MotionLab geometry评测均已完成，4090 GPU0/1释放；5090 GPU0继续执行v7.47。历史v7.46虽在5090 GPU3运行过，但不代表该卡当前可调度，不得在5090 GPU1/2/3启动新任务。

MoMask-Pulp的旧“仍在长训”状态也已纠正：run=`momask_pulp_human_native_seed17_5090g3_stage1matched_20260716`在02:29写出`ALL_TRAINING_COMPLETE.json`，VQ/Mask/Residual endpoint SHA256依次为`e21d42684e4441b67782b8951e1a5e6c9e5c25bbd1bc460aa7fda138ea348664`、`037871329eaf980e320961445f5492c7a79ad85d60e9e2b79640678dfabeff3c`、`89faab30ffb62d185a789a814ae7c061ed5f5375f9ce5128dc4764756c43e0b1`。该run没有formal/eval文件；adapter README也只预注册“later formal-evaluation adapter”，当前Pulp pure4053实现与审计尚未闭合。5090 GPU0正执行v7.47、其余5090卡未获授权；4090 GPU1虽空闲，也不能跳过adapter实现/审计直接迁移checkpoint，因此本轮只登记endpoint，不部署MoMask formal。

> [!important] 2026-07-18 resource correction
> 4090 GPU0/1 与 5090 GPU0/1/2/3 均已空闲。v7.47 的唯一剩余工作是 export raw JSON/records、重新执行 contract/artifact audit、再做相对 v7.38 的 matched analysis；在此之前不启动新的 Stage2 task。

## 6. Promotion 与停止规则

1. v7.44 已完成且未满足 gate：不构建新 Stage2 cache，也不替换 v7.14。fixed-300 既不是 local human 长程误差的修复，也不是 official AE 优势的充分解释。
2. v7.45 是 generator/operator control，不改变v7.14 Stage1；formal已显示semantic/local-pose改善但global-root broad regression，因此停止在human-only，不扩展camera/joint。该结果不能证明所有非CondMDI operator无效。
3. v7.46 的 10k 只决定是否继续花 compute；其 gate contract错误后保持冻结。v7.47 从零重做 corrected gate，105k pure4053 才能回答 representation。只有 Direct H 与 joint parallel改善且 Direct C/geometry不 broad regress，official AE representation 才进入下一轮讨论。
4. MotionStreamer 是 tier-C native-system baseline。即使 Stage1 MPJPE更好，也不能当作 StoryMotion causality ablation；必须完成其 own Stage2/formal 后才能比较 Direct H system quality。
5. 所有 metric table继续要求非空 `version / run`；true-length、fixed-300、local v7.14、official Pulp AE 与 MotionStreamer 不得合并成一个 tokenizer row。

## 7. Contract 修改

根 `AGENTS.md`、StoryMotion `AGENTS.md` 与 experiment contract 已加入唯一 causal exception：只允许 standalone native MotionStreamer baseline 保留 causal tokenizer/decoder；StoryMotion mainline、representation controls、cache、Unified Stage2 与 evaluator仍强制 `is_causal is False`。`storymotion/experiment_invariants.py` 不放宽。

## 8. 部署验收

截至 2026-07-17 03:28 CST，四个指定 GPU 均已越过预处理并产生可核验的有限训练指标。这里的“完成”仅指 **实验部署完成**；长训、10k gate、Stage1 endpoint 与 formal evaluation 仍在进行。

| host / GPU | run / PID | contract SHA256 | 首个或当前活性证据 |
| --- | --- | --- | --- |
| 4090 / GPU1 | v7.44 / `1430633` | `e2b752f6…fc6c4e` | pure4053 step-0 `total_loss=0.66583`；训练 step 14 `total_loss=0.52971`、`grad_norm=0.10366`；进程显存 `1,776 MiB` |
| 4090 / GPU0 | v7.45 / `1443506` | `34544e15…d163a` | step-1 train/eval/test loss=`2.25163/2.53431/2.86910`，human exposure=`64`；进程显存 `4,896 MiB`，与既有 MotionLab formal eval 共驻 |
| 5090 / GPU3 | v7.46 driver / trainer `359326/386812` | `a4d2c038…29824` | train step 1→200 loss=`1.11457→0.50524`；三任务 exposure=`102,400`；进程显存 `15,294 MiB` |
| 5090 / GPU0 | MotionStreamer / `993683` | `45b55f59…90581` | step 200→1,400 total loss=`2,606,006→1,574,901`，exposure=`179,144`；进程显存 `3,382 MiB` |

v7.45 首次 launcher 曾因先创建 `driver/`、后由训练入口按“run 根目录是否存在”判断初始化，导致缺少 `manifest.json` 而退出。失败现场保存在 `runs/archive/failed_start_v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717/`。正式重启先调用 canonical run initializer，再创建 driver；同时复用与 v7.40 相同 train/val IDs 和 cache SHA 的确定性 caption cache：train=`a5bec2b1…c47c8`、val=`56cf0cc6…bc18`。这只消除约 32.5 万个重复小文件读取，不改变样本、caption 或训练 treatment。

v7.46 的 official AE matched cache 已在 5090 核验：train `162,760` 条，SHA256=`1924c632…1e8`；val `4,053` 条，SHA256=`c642f7c7…1d3d`。train-only full-cov stats、official owning-decoder identity smoke 与三任务 step-1 exposure 均已闭合；这是 03:28 的部署验收事实。实际 10k gate 因 evaluator contract 不一致停止，未继续30k/105k，最终状态以第9节为准。

## 9. Endpoint、评测与剩余时间更新

### 9.1 MotionStreamer-Pulp Stage1 endpoint

run=`motionstreamer_pulp_stage1_500ep_seed17_5090g0_20260717` 已完成 `636,000` optimizer steps、`81,380,000` sample exposures 与 epoch-500 pure4053 full-sequence owning-decoder reconstruction。checkpoint=`last.pt`，SHA256=`825b15e3946bc511fa560ae9f7b34a76d1d19458d01aad0ec36be15a1b57016d`；completion artifact=`training_complete.json`。

| version / run | valid length | samples | root-aligned MPJPE / mm | global MPJPE / mm |
| --- | ---: | ---: | ---: | ---: |
| MotionStreamer-Pulp / `motionstreamer_pulp_stage1_500ep_seed17_5090g0_20260717` | 1–64 | 1,805 | 80.658 | 219.311 |
| MotionStreamer-Pulp / `motionstreamer_pulp_stage1_500ep_seed17_5090g0_20260717` | 65–128 | 1,411 | 75.063 | 299.147 |
| MotionStreamer-Pulp / `motionstreamer_pulp_stage1_500ep_seed17_5090g0_20260717` | 129–192 | 456 | 78.304 | 362.423 |
| MotionStreamer-Pulp / `motionstreamer_pulp_stage1_500ep_seed17_5090g0_20260717` | 193+ | 381 | 96.527 | 414.168 |
| MotionStreamer-Pulp / `motionstreamer_pulp_stage1_500ep_seed17_5090g0_20260717` | overall | 4,053 | 79.937 | 281.524 |

feature MSE=`0.174889`。训练末期 reconstruction/total 为负来自 MotionStreamer optimal-sigma NLL 的标度，不等于负 MSE；endpoint 的几何判断以 valid-frame MPJPE 为准。该结果显示 root-aligned 误差相对稳定，但 global drift 随长度增加；仍只能作为 native causal system 的 Stage1 diagnostic，不能归因于 causality，也尚不是 Direct-H Stage2 system result。

### 9.2 v7.46 10k gate contract mismatch

v7.46 的实际 endpoint 是 step10k，manifest=`screen_stopped`，不是105k complete。被 screen 使用的 `last.pt` SHA256=`f58cb83cf9cf779f0aaf106b61353c4a30802dfce402fff74dfc1dcd15412d7c`；owning official decoder SHA256=`e0ff0a66129d77eb27a18d0034b23f692aaec3ef53afd540097d8d9544a73e52`。

| version / run | N64 profile | relevant coverage | Out | gate evidence |
| --- | --- | ---: | ---: | --- |
| v7.46 / `v7_46_official_ae_unified_matched_seed17_5090g3_20260717` | human | TMR 65.64% | 未产出 | coverage通过；gate把缺失Out当作失败 |
| v7.46 / `v7_46_official_ae_unified_matched_seed17_5090g3_20260717` | camera | CLaTr 100.00% | 未产出 | coverage通过；gate把缺失Out当作失败 |
| v7.46 / `v7_46_official_ae_unified_matched_seed17_5090g3_20260717` | joint | TMR 90.77%；CLaTr 73.59% | 20.09% | 全部通过预注册数值阈值 |

> [!warning] 不允许的结论
> 当前 `stop_after_10k` 不能解释为 official AE representation 失败：记录中的两个 reason 都是 H/C 缺少 `test/proj/outscreen`。但也不能静默删除预注册 gate 后直接续训；必须先决定 camera completion 是否应补 projection metric，以及 human-text-only 是否本来就不适用 Out，再修复 gate/evaluator contract。

按用户指定，step10k 的 pure4053 **post-stop diagnostic** 已完成：5090 GPU0执行human，GPU1串行执行camera→joint。输出目录为 `eval/poststop10k_pure4053_diagnostic/`，driver logs 为 `driver/poststop10k_pure4053_human_gpu0.log` 与 `driver/poststop10k_pure4053_camera_joint_gpu1.log`。

| version / run | pure4053 profile | distribution | semantics | coverage | Caption F1 | Out |
| --- | --- | --- | --- | --- | ---: | ---: |
| v7.46 step10k / `v7_46_official_ae_unified_matched_seed17_5090g3_20260717` | human | FDTMR 290.453 | TMR 16.034 | H 22.72% | — | 不适用 |
| v7.46 step10k / `v7_46_official_ae_unified_matched_seed17_5090g3_20260717` | camera | FDCLaTr 28.022 | CLaTr 58.470 | C 80.48% | 0.7553 | 当前callback不产出 |
| v7.46 step10k / `v7_46_official_ae_unified_matched_seed17_5090g3_20260717` | joint | H FDTMR 223.725；C FDCLaTr 166.708 | H TMR 15.908；C CLaTr 18.109 | H 32.15%；C 45.62% | 0.2310 | 22.34% |

三项均为 `4,053/4,053` samples与records、所有指标finite，并共享 step10k checkpoint SHA256=`f58cb83c…12d7c` 与official owning decoder SHA256=`e0ff0a66…73e52`。artifact SHA256：human JSON/records=`8a32acd5…a61af`/`1804f994…d3de3`；camera=`df366dde…430e`/`50dd2afd…a27cb`；joint=`b6299c47…b07a1`/`01f47379…d9b78`。

若 gate 按任务适用性解释为“human只查TMR coverage、camera查CLaTr coverage、joint查双coverage与Out”，则 N64 与 pure4053 都过宽松数值门槛；但 post-stop diagnostic 不能事后改写 launch-time contract。这些结果不得标作105k formal或直接触发promotion。

### 9.3 v7.44 fixed-300 Stage1 endpoint

v7.44 已完成 `636,000` steps、`81,380,000` sample exposures 与 pure4053 true-length/fixed-300双上下文评测。last checkpoint SHA256=`121de69767c35f6588fe6b1d4c2dd74f792dddd70bc3567d9bf17a65db7113e1`；best validation 为 step635k、`val_loss=0.0155314`；geometry artifact SHA256=`bb6e3df67ffe35abbeb2cc06752eb911bcab8861026ec5e08511e05ebcd32d77`。artifact记录 exact non-causal checkpoint、official owning decoder、同一 `4,053` ordered IDs，全部指标finite。

下表均为 true-length、valid-frame、整段一次 encode/decode；单位 mm。

| version / run | valid length | samples | root-aligned MPJPE | global MPJPE |
| --- | ---: | ---: | ---: | ---: |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | 1–64 | 1,805 | 70.797 | 146.843 |
| v7.44 / `v7_44_joint_ae_fixed300_masked_seed17_4090g1_20260717` | 1–64 | 1,805 | 72.078 | 148.130 |
| Pulp official AE / `aemmardm-xgmj0yjj-325` | 1–64 | 1,805 | 85.429 | 194.473 |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | 65–128 | 1,411 | 77.338 | 208.780 |
| v7.44 / `v7_44_joint_ae_fixed300_masked_seed17_4090g1_20260717` | 65–128 | 1,411 | 79.047 | 212.556 |
| Pulp official AE / `aemmardm-xgmj0yjj-325` | 65–128 | 1,411 | 78.527 | 168.342 |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | 129–192 | 456 | 87.583 | 305.918 |
| v7.44 / `v7_44_joint_ae_fixed300_masked_seed17_4090g1_20260717` | 129–192 | 456 | 89.088 | 312.208 |
| Pulp official AE / `aemmardm-xgmj0yjj-325` | 129–192 | 456 | 66.967 | 162.589 |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | 193–251 | 381 | 132.041 | 428.743 |
| v7.44 / `v7_44_joint_ae_fixed300_masked_seed17_4090g1_20260717` | 193–251 | 381 | 137.596 | 458.668 |
| Pulp official AE / `aemmardm-xgmj0yjj-325` | 193–251 | 381 | 78.034 | 186.646 |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | overall | 4,053 | 80.720 | 212.803 |
| v7.44 / `v7_44_joint_ae_fixed300_masked_seed17_4090g1_20260717` | overall | 4,053 | 82.577 | 218.212 |
| Pulp official AE / `aemmardm-xgmj0yjj-325` | overall | 4,053 | 80.254 | 181.053 |

v7.44 相对 v7.14 在最长 bin 的 root-aligned/global MPJPE 分别恶化约 `5.56/29.93 mm`；相对 official AE 则恶化 `59.56/272.02 mm`。overall root-aligned只差 `2.32 mm` 会掩盖严重的长序列失配，因此不能只看单一总体均值。v7.44 fixed-max inference 与 true-length 几乎相同：overall root/global 为 `82.330/218.122 mm`，相对 true-length仅 `−0.247/−0.089 mm`；这进一步排除了 eval context policy 是主因。

camera 结论与 human 不同：

| version / run | context | samples | Cam-ADE / mm | camera rotation / deg |
| --- | --- | ---: | ---: | ---: |
| v7.44 / `v7_44_joint_ae_fixed300_masked_seed17_4090g1_20260717` | true-length | 4,053 | 41.484 | 0.619 |
| Pulp official AE / `aemmardm-xgmj0yjj-325` | true-length | 4,053 | 137.449 | 1.792 |

因此 v7.44 **未通过 human promotion，不构建 Stage2 cache**；同时不能把当前问题概括成“joint tokenizer 的 human 与 camera 都差”。local camera representation 当前不是首要瓶颈。

### 9.4 v7.45 endpoint 与4090评测

v7.45 已完成 `240,000 × 64 = 15.36M` human generation exposures。last/best-eval checkpoint SHA256分别为 `4669a56fb6c9a4adafc2cfedef39b27c060cd00949a7407c86c68cc9fa30200d` 与 `08dd9e0d73a7696dd6bd4fcc72b0f4c7d3a1b0792293e525b64fd3e28b43a846`。train loss 从 early mean `1.1686` 降至 final mean `0.5295`；eval 最佳为 step235k 的 `0.64245`，test 最佳为 step228k 的 `0.65746`，显示稳定平台而非训练 collapse。

last checkpoint的pure4053、RF50、unmask15、CFG4 owning-decoder formal已完成。artifact SHA256=`445695958ba86c11831cbc8f931939c71f72135453b21ca6b6d5e2f170b6f685`；records SHA256=`6edb7d5f9e54a61540b175028cad6911d5b573d4290e7dc95edc7e6fce122a9c`。records为64个batch rows，展开后是`4,053` unique ordered IDs、indices `0..4052`；artifact内paired geometry为`4,053` records。checkpoint、cache、owning non-causal decoder与sample-ID SHA均通过审计。

| version / run | FDTMR ↓ | TMR ↑ | HCov ↑ | root-aligned MPJPE / mm ↓ | global MPJPE / mm ↓ | root ADE / mm ↓ | root FDE / mm ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | 333.880 | 13.294 | 40.54% | 250.364 | 863.112 | 769.275 | 1280.066 |
| v7.45 / `v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717` | 149.163 | 17.729 | 49.86% | 242.502 | 1249.134 | 1164.249 | 2007.279 |

| version / run | valid length | samples | root-aligned MPJPE / mm ↓ | global MPJPE / mm ↓ |
| --- | ---: | ---: | ---: | ---: |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | 1–64 | 1,805 | 253.586 | 677.934 |
| v7.45 / `v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717` | 1–64 | 1,805 | 251.390 | 842.422 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | 65–128 | 1,411 | 249.884 | 895.589 |
| v7.45 / `v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717` | 65–128 | 1,411 | 235.229 | 1310.340 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | 129–192 | 456 | 234.630 | 1135.359 |
| v7.45 / `v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717` | 129–192 | 456 | 221.093 | 1697.425 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | 193+ | 381 | 255.706 | 1294.288 |
| v7.45 / `v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717` | 193+ | 381 | 252.949 | 2412.741 |

v7.45在所有长度bin的root-aligned MPJPE均小幅改善，并把FDTMR/TMR/coverage全部大幅改善；但global MPJPE在所有bin退化，最长bin增加`1118.45 mm`，overall root ADE/FDE增加`394.97/727.21 mm`。因此它是semantic/local-pose与world-root trajectory之间的Pareto，不是可晋级的Direct-H替代。两条run只共享Stage1/cache/decoder/pure IDs；generator、text encoder、训练human exposure与sampler/CFG均不同，所以该比较不能写成CondMDI-vs-MoLingo单变量因果实验。

### 9.5 corrected official-AE Stage2 v7.47

v7.46 不是完整 official-tokenizer StoryMotion Stage2：它停在step10k。修正 gate 为 human只查TMR coverage、camera只查CLaTr coverage、joint查两者与Out后，v7.47 从step0重新训练，不继承 v7.46 的 optimizer或checkpoint。run=`v7_47_official_ae_unified_matched_seed17_5090g0_20260717`，contract SHA256=`5fab7f34230ff16080fe45177d6be98cbe6dbf49b3189891c2037ec892692847`；cache、owning official decoder、width416、asymmetric Unified、task probabilities与 `105k × 512` budget保持matched。

14:48的corrected N64 gate已通过并自动续训：human TMR coverage=`81.41%`，camera CLaTr coverage=`100%`，joint TMR/CLaTr coverage=`84.36%/82.95%`、Out=`14.36%`，reasons为空；gate JSON SHA256=`5bb7b04106c205d824ce62d01b95a79774ca972aa9929ff7db62e3ffd5d886c8`，step10k checkpoint SHA256=`53c11f62cf0737cc230598c392221d960e649d4c315f6297181db9133d5e347b`。这只通过structural learnability gate，不进入formal ranking，也没有回答representation优劣；105k与pure4053仍约需10–12 h。

10k screen使用的evaluator SHA256=`fbba2024…c35`，产生有效gate metrics但尚无paired geometry。screen完成后只热更新未来formal的evaluator与geometry helper，SHA256分别为`fc9e97c0ba7a3423d676b4ac53f01f099699244fc193db3b3f739b24a6dd9d3f`与`4ab7d96db9a42cf728df8c220a822658157ea638ad8d2d8f27dc2c3bfe2c0af3`；remote compile/`--help`通过。训练模型、optimizer、cache、driver与已生成screen artifacts均未改动；105k formal将按新contract产出MPJPE/Cam-ADE。

2026-07-18 12:11 CST，105k formal 的 Direct-H、Direct-C、joint parallel 与 human-first cascade 均完成 `4,053` samples。driver 回传 JSON SHA256 依次为`4330f300e7c361718b116fb81774fc2cef4c59a0de638d54d033bc2692bdc9d7`、`90114c336862f0300218fb3f2bac11bb27e03578ec7ce2ad859c1d31972d35f6`、`84fc0d21d8bcb6ff1806b71bbab2d968d126c2443c7dbdcf6983383b3bac25e3`、`132f728417bf73435e8e878b225e50699091c4a15941025d032aa630cf3f02e2`。records SHA 亦由 driver 回传，但 runner chroot overlay 没有导出 JSON/records 到普通 5090 SSH root；所以本节只记录 execution provenance，不记录 metrics，也不写 formal audit 或 representation 结论。

### 9.6 v7.38 L0 三模式 geometry closure

4090双卡补审已完成。Direct H、Direct C与joint均为pure4053、seed17、DDIM50、CFG1、同一L0 step105k checkpoint SHA256=`ab474d353a29a4ee707c8ed4e37599fcc47ea79c124452ebdd366d5bdafdaf35`、同一owning non-causal decoder SHA256=`91248bf440a4a5493a0f8b4994d6d36479fcaa221d331f6995a91ed1af8e7ce1`，每项各有`4,053` records与同一ordered-ID SHA256=`a0d7627e…6b93`。

| version / run | profile | human root-aligned / global MPJPE / mm | root ADE / FDE / mm | Cam-ADE / Cam-FDE | rotation / deg |
| --- | --- | ---: | ---: | ---: | ---: |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Direct H | 250.364 / 863.112 | 769.275 / 1280.066 | — | — |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Direct C | — | — | 1.512 / 1.606 m | 32.926 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | joint parallel | 252.670 / 842.297 | 742.287 / 1234.715 | 2.912 / 3.026 m | 72.928 |

| version / run | profile / valid length | samples | Cam-ADE / m | Cam-FDE / m | rotation / deg |
| --- | --- | ---: | ---: | ---: | ---: |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Direct C / 1–64 | 1,805 | 1.520 | 1.568 | 35.081 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Direct C / 65–128 | 1,411 | 1.486 | 1.582 | 31.637 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Direct C / 129–192 | 456 | 1.491 | 1.640 | 31.809 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Direct C / 193+ | 381 | 1.602 | 1.834 | 28.832 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | joint / 1–64 | 1,805 | 2.793 | 2.861 | 73.947 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | joint / 65–128 | 1,411 | 2.897 | 3.014 | 72.269 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | joint / 129–192 | 456 | 3.096 | 3.266 | 72.999 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | joint / 193+ | 381 | 3.311 | 3.566 | 70.458 |

artifact/records SHA256分别为：Direct H=`beb4956c…2cf`/`a3cd8256…bcb`，Direct C=`806d88a7…955`/`2fc183ac…031`，joint=`e8b39450…0a7`/`f134370f…c0a`。既有distribution/semantic指标完全复现旧formal：Direct C FDCLaTr/CLaTr/CCov/F1=`33.295/55.640/73.23%/0.715`；joint FDTMR/TMR/HCov=`282.374/14.420/48.98%`、FDCLaTr/CLaTr/CCov/F1=`58.959/47.129/65.68%/0.569`、Out=`21.69%`。

这组结果直接证明“旧三模式统计不差”与“paired decoded geometry接近GT”不是同一件事。Direct C与joint是one-to-many生成，单GT Cam-ADE/rotation仍不能独立判定自然度；但相对Stage1的Cam-ADE=`0.0415 m`，Stage2的`1.51/2.91 m`量级说明camera tokenizer不是当前paired误差主源，Stage2生成/conditioning至少贡献了主要增量。

### 9.7 MotionLab-MFT completed formal 与 geometry补审

此前文档中的“MotionLab进行中”是过期状态。run=`baseline_motionlab_mft_v714_human_seed17_4090g0_20260716`已在03:11完成step30k/`15.36M` human-only exposures，并在03:42完成pure4053 RF50/CFG2.5 formal；manifest=`evaluated`。checkpoint SHA256=`45477134830f25c58b6db2ea54cfdce4cadd8f0e84c0e9312f1ead73bce468dd`，原formal JSON SHA256=`bd8eba338960f3be71bf6f97d269e3c85183766ae1a2c93f83b7f4cd80633bcb`。

| version / run | FDTMR ↓ | TMR ↑ | HCov ↑ | geometry状态 |
| --- | ---: | ---: | ---: | --- |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | 333.880 | 13.294 | 40.54% | 已完成 |
| v7.45 / `v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717` | 149.163 | 17.729 | 49.86% | 已完成；global-root退化 |
| MotionLab-MFT / `baseline_motionlab_mft_v714_human_seed17_4090g0_20260716` | 156.350 | 18.172 | 59.19% | geometry已完成；root/global=`250.78/951.38 mm` |

MotionLab在existing formal三项上全面胜L0；相对v7.45则TMR/coverage更高、FDTMR略差，形成Pareto。为执行新mandatory metric contract，evaluator只增加paired geometry收集与汇总，script SHA256=`541c2d084444431ca26080d6313379b52fd3948efd3142af4a1f6d47a74d452b`；4090 GPU0以同checkpoint/sampler/IDs重跑到新artifact，不覆盖原formal。补审完成`4,053` records、同一ordered-ID SHA256=`a0d7627e…6b93`，root-aligned/global MPJPE=`250.782/951.380 mm`、root ADE/FDE=`857.640/1436.396 mm`。相对L0，root-aligned仅`+0.418 mm`，但global/ADE/FDE恶化`88.268/88.365/156.330 mm`；所以MotionLab的semantic/distribution提升没有转化为world-root提升。geometry JSON/records SHA256=`f1a45654d740d8937152c96b75f88a53a765bc37977719d6628ccef6c36d79ba`/`2b6d42544e75ad330e01091e4a3a294a67e02f2fe0db17ba14fc12e5afdca765`。

## 10. 当前根因判断与 metric contract

“StoryMotion整体不可用，因为Stage1 human质量差”目前过强；更准确的判断是两个可独立成立的风险：

1. **Stage1 human representation已有严格证据不合格，但camera Stage1不是主瓶颈**：local v7.14/v7.44的长序列human root-aligned与global MPJPE显著上升，而同一数据的official AE保持平坦；fixed-300训练没有修复。反之local camera Stage1 Cam-ADE=`0.0415 m`，所以不能把两个branch一起判坏。
2. **Stage2还有独立且更大的geometry风险**：v7.38 Direct H/joint的human root/global约`250/842–863 mm`，Direct C/joint Cam-ADE约`1.51/2.91 m`；都远高于owning Stage1 reconstruction。v7.45虽改善root-aligned MPJPE与distribution/semantics，却进一步把global MPJPE推到`1249.1 mm`。自由生成的一对一geometry不能单独证明自然度失败，但matched IDs上的broad regression可否定v7.45 promotion，也说明旧分布指标不足以支撑视觉质量。official representation责任仍需v7.47 endpoint闭合。

“没有时长限制的 temporal convolution 理应长度不敏感”也不成立。finite receptive field只约束局部依赖，不保证世界坐标轨迹误差不累积；root velocity、朝向和低频偏差经时间积分会放大 global MPJPE，边界比例与长动作内容难度也随长度变化。当前 length bins又是不同样本的横截面，不能单独证明纯粹的长度因果；但 official/local在同一 ordered IDs上的差异足以否定“长序列退化不可避免”。后续若要进一步做因果诊断，应使用同一样本的 prefix/interior consistency，而不是继续增加跨样本 bin。

强制 metric 列表已写入 StoryMotion experiment contract：

- Stage1：human root-aligned/global MPJPE、root ADE/FDE；camera Cam-ADE/Cam-FDE、rotation geodesic；全部报告 `1–64`、`65–128`、`129–192`、`193+` 与 overall。
- Stage2 Direct H、Direct C、joint：必须产出任务适用的同组 paired geometry，并继续报告 TMR/CLaTr distribution、semantics与coverage；joint另报projection/framing/Out。
- 自由 Direct H/joint 的单GT MPJPE是 mandatory diagnostic，不是 standalone hard gate；若用于选择，需预注册 Best-of-K或多实现协议。GT held-out temporal completion/inpainting的 masked-region MPJPE/Cam-ADE才可作为 hard gate。
- free generation还需无GT physical指标与blind render；缺少任务适用 metric 的 artifact标为不完整，不把缺失值当成通过或失败。

### 10.1 后续结果如何归因

| version / run contrast | 保持相同 | 仍不同 | 改善时支持 | 不改善时排除或降级 |
| --- | --- | --- | --- | --- |
| v7.45 / `v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717` vs v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` Direct H | v7.14 tokenizer/cache、owning decoder、pure IDs | generator architecture/objective、text encoder、human exposure与sampler/CFG | local representation不变时，generation-native operator可改善Direct H | 该masked-iterative RF recipe不值得扩展camera/joint；不能据此否定所有非CondMDI operator |
| v7.47 / `v7_47_official_ae_unified_matched_seed17_5090g0_20260717` vs v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | asymmetric Unified、width、task routing/probabilities、budget、normalization policy、sampler | frozen Stage1 representation/cache与owning decoder | official representation提高generatability，local Stage1是主要因果因素之一 | 在matched Unified下更换representation不足；Stage2 human all-mask生成或conditioning成为更高优先级 |

只有第二行接近representation单变量；第一行是same-representation system comparison，不应写成“CondMDI与MoLingo的严格单变量因果实验”。若两行都改善，则Stage1与Stage2是叠加瓶颈；若只有v7.47改善，优先切换/复现official representation；若只有v7.45改善，优先替换human generator；若都不改善，则停止继续做padding variant，转向conditioning、decoded objective、physical metric与blind render闭环。

v7.45的实际结果已经裁决第一行：semantic/distribution与local pose改善，但world-root trajectory未改善，因此视为Pareto challenger并停止扩展；它既不能替换L0，也不能为CondMDI“生成能力充分”或“架构必然不足”作单向证明。
