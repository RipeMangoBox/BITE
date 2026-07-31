---
title: "StoryMotion Stage1 Length, CondMDI, and Causality Evidence"
status: archived
hypothesis: |
  v7.14 的主要新增风险不是 64-frame crop，而是 non-causal local human tokenizer 在长序列上的长度泛化与 root-velocity 累积。CondMDI official HumanML3D checkpoint 已完成 all-mask capability闭环，其 text-conditioned all-mask exposure 仍低于 StoryMotion Direct H；下一轮应先比较 Stage1 representation 与 latent generatability，不恢复 causal tokenizer。
tags:
  - StoryMotion
  - stage1
  - stage2
  - experiment
  - decision
  - status/archived
aliases:
  - StoryMotion-Stage1-Length-CondMDI-Causality
source_notes:
  - "[[current]]"
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[current]]"
  - "[[StoryMotion_Gradio_Render]]"
created: 2026-07-17T01:35:00+0800
updated: 2026-07-18T15:20:00+08:00
archived_at: 2026-07-18T15:20:00+08:00
superseded_by:
  - "[[current]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
---

# StoryMotion Stage1 Length, CondMDI, and Causality Evidence

> [!warning] Archived evidence
> 本页保留 length/CondMDI/causality forensic evidence，不再维护 priority、deployment 或 queue。MotionStreamer 的窄例外和所有 StoryMotion non-causal invariant 以根目录 `AGENTS.md` 为准；当前 v8 decision 见 [[current]]。

> [!abstract] 当前裁决
> Direct H 是 human-text-only 的纯 text-to-motion，Direct C 是 complete GT-H latent 加 camera text 的 camera completion。v7.14 真实训练没有 64 帧裁剪，但 pure4053 全序列重建显示 local human branch 随长度显著退化，且该趋势在同样本 Pulp official AE 中不存在。历史所谓 causal 低质主要是 non-causal v7.14 被错误按 causal encoder 构建 cache，并叠加错误 decoder；它不是干净的 causal Stage1 training 结论。下一轮先做 non-causal Stage1 representation 与 generatability control，不启动 causal tokenizer 或 MotionStreamer causal TAE。

## 1. 固定数据与因果边界

“Pulp 数据使用 16w train”在本计划中固定解释为**训练集合大小**，不是 optimizer step：

- Stage1 fit 与 Stage2 train cache 都使用同一 `162,760` 个 ordered train IDs；
- pure test `4,053` 个 IDs 不进入 fit、normalization 或 checkpoint selection；
- 每个 run 仍需独立声明 optimizer steps、batch size 与 sample exposures，不能把 `162,760` 写成 `160k steps`；
- Stage1/Stage2 train、cache build、checkpoint load 与 eval 全部 hard assert `is_causal is False`。

Pulp Stage1 的精确公开 recipe 仍不完整。[Pulp issue #7](https://github.com/robincourant/pulp-motion/issues/7) 目前只能证明 split、crop、loss weight、optimizer 与 checkpoint selection 尚未得到作者确认，不能据此反推官方 AE 使用 64-frame crop。

## 2. Direct Human / Camera 的目标与 setting

| mode | 模型实际读取 | 预测目标 | 实验问题 | 主指标 |
| --- | --- | --- | --- | --- |
| Direct H / `human_first` | human text；human/camera observation mask 都为空 | 只预测 human latent；camera 不计 target loss | Unified-3 是否学到纯 text-to-human prior；排除 camera observation 泄漏 | FDTMR、TMR、HCov 与 decoded geometry |
| Direct C | complete GT human latent 加 camera text | 只预测 camera latent；human 固定不生成 | 在理想 human source 下，camera completion 是否仍存在 shared-vs-specialist gap | FDCLaTr、CLaTr、CCov、Caption F1 与 framing/geometry |

两者共享 v7.38 L0 checkpoint、同一 branch implementation、frozen corrected v7.14 non-causal joint AE、owning decoder、train-only normalization、cache、seed 与 DDIM50 evaluator。v7.42 H/C specialists 只改变 task exposure，用于诊断参数共享，不是外部 baseline。Direct H 的 camera-projection 视频若存在，只把 paired GT camera 当外部显示视角，模型没有读取 camera latent。

## 3. 64-frame 问题：代码事实与 full-sequence 证据

### 3.1 代码事实

- v7.14 runner 的真实数据分支逐条加载完整变长序列，collate 只 pad 到当前 batch 最大长度。
- `run_config.json` 中的 `seq_len=64` 只由 `--synthetic` 数据分支消费；v7.14 为 `synthetic=false`。
- `train_pulp_raw_tokenizers.py` 的 best-effort reproduction 确实有 first-64 truncate，但它不是 corrected v7.14 mainline。
- 新评测对每条样本按 valid length 一次 encode/decode；没有 crop、tiling 或 sliding window。Pulp official AE 仅为 temporal stride 做右侧 padding，输出再裁回 valid length。

### 3.2 pure4053 全序列重建

证据 artifact：

`runs/train/stage1/v7_14_official_contract_20260710/joint_ae_official_4090_gpu0_r2/eval/long_sequence_geometry_pure4053_paired_20260717.json`

artifact SHA256=`42b75ab9b6cc72f937e86e9205fde320efe77ad00fa37a47d68163aab57f9e82`；local checkpoint SHA256=`91248bf440a4a5493a0f8b4994d6d36479fcaa221d331f6995a91ed1af8e7ce1`；Pulp official `aemmardm-xgmj0yjj-325.ckpt` SHA256=`e0ff0a66129d77eb27a18d0034b23f692aaec3ef53afd540097d8d9544a73e52`；评测脚本 SHA256=`f3a7f127ad53a52788ab9692d2487de3c99ff7b58ae72feb9de56764b9bc3858`。artifact 含 `4,053` unique IDs 与 `8,106` local/official records，所有 metric finite。

样本长度为 `9–251` 帧，中位数 `71`，P90 `188`。下表单位为 mm；每行是同一批 paired samples。

| valid frames | samples | local H root-aligned MPJPE | Pulp official | local global MPJPE | Pulp official | local camera-center ADE |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1–64 | 1,805 | 70.8 | 85.4 | 146.8 | 194.5 | 43.2 |
| 65–128 | 1,411 | 77.3 | 78.5 | 208.8 | 168.3 | 39.2 |
| 129–192 | 456 | 87.6 | 67.0 | 305.9 | 162.6 | 39.1 |
| 193–251 | 381 | 132.0 | 78.0 | 428.7 | 186.7 | 47.6 |

同样本 `local − official` 的 root-aligned MPJPE 从短序列 `−14.6` mm 变为最长 bin `+54.0` mm；global MPJPE 从 `−47.6` mm 变为 `+242.1` mm。paired delta 对长度的斜率为 root-aligned `+36.0 mm / 100 frames`、global `+155.5 mm / 100 frames`。相反，local camera-center ADE 的长度斜率只有约 `+1.4 mm / 100 frames`。

> [!important] 证据允许的结论
> 不能写“64-frame crop 导致长序列失败”，因为 crop 不存在。可以写“corrected v7.14 local human tokenizer 有相对 Pulp official AE 的 length-dependent reconstruction gap，主要表现为 root/global drift，并伴随较弱的 root-aligned pose 退化”。当前是强相关定位，不是对具体卷积层或 loss 的最终因果证明。

## 4. CondMDI all-mask 的准确比较

CondMDI released training 默认 `keyframe_mask_prob=0.1`，会独立地把整条 observation mask 清空；text CFG dropout 为 `cond_mask_prob=0.1`。因此：

- observation 全空约占 `10%`；
- 若两个 mask 独立，text 保留且 observation 全空约占 `0.9 × 0.1 = 9%`；
- released `random_frames` 路径当前固定选择 20 个 keyframes，并没有按多个 mask-density bucket 显式分配训练比例；`random_joints` 才会随机改变 frame/joint 数量。

StoryMotion L0 的 `task_probs=[1,1,1,0]` 使 Direct H 约占三分之一 slots，而且该模式每次都是 human/camera observation 全空。故 StoryMotion 的问题不能表述为“all-mask 比 CondMDI 更少”：它的纯 all-mask exposure 反而更高。更准确的差异是 CondMDI 还覆盖 partial observation，而 StoryMotion 当前任务族没有按 mask 数量构造连续密度课程。

官方 checkpoint 闭环只回答“released CondMDI conditional model 能否在 HumanML3D 上走通 text + all-zero observation mask”，不直接回答 Pulp latent 上的质量，也不能与 StoryMotion pure4053 指标混表。运行必须记录 checkpoint SHA、`edit_mode=uncond`、prompt、observed-mask sum、finite/temporal-variance 检查与输出路径。

闭环已完成：使用 official README 的 `condmdi_randomframes/model000750000.pt`，checkpoint SHA256=`914b61980917333fef98e64ab45c3644ddb3f41a20dd323b77c28540dc49581a`，dataset=`humanml`、`abs_3d=true`、`edit_mode=uncond`。prompt 为 `a person walks forward then turns around`，有效长度 `72` 帧；saved `observed_mask` shape=`1 × 22 × 1 × 196`、sum=`0`，motion 全 finite，平均 temporal std=`0.2573`、平均逐帧变化=`0.0443`、root displacement=`1.1080`。结果位于：

`/data/public/ripemangobox/Motion/CondMDI/save/results/storymotion_condmdi_randomframes_allmask_text_20260717/results.npy`

结果 SHA256=`b692fd6c298b7b9dfca17ae3647a894178a78a4900bf508136fbc0c34ce49b0f`。official sampler 已生成并保存结果；随后 visualization helper 因 all-zero observation 没有可画的 input keyframe 而在 `matplotlib.animation` 报错。该错误发生在 `results.npy` 保存之后，是 renderer 的 zero-keyframe boundary bug，不是 model sampling failure。此 smoke 证明 capability，不证明 CondMDI 的 pure T2M quality足够好。

## 5. 历史 causal 低质的归因

v7.15–v7.16 不是“causal Stage1 训练后接 Stage2”的干净实验：

1. owning checkpoint 是 non-causal v7.14；
2. cache builder 忽略 `run_config.json`，错误地按 causal encoder 重建同一权重；
3. evaluator 又错误使用 official Pulp decoder，而不是 owning local decoder；
4. 修正 cache causality 与 decoder 后，灾难性 collapse 大幅缓解，但仍剩 Stage2 learnability/sampler 问题，后续 v7.30/v7.38 才逐步解决。

因此“causal 导致低质”首先定位在 **Stage1 checkpoint 的错误应用/cache boundary**，并非已证明 causal Stage1 training 本身差，也不能据此声称 Stage2 架构天然不兼容 causal latent。重新训练 causal joint AE 再接 MoLingo+RF 会同时改变 representation 与 causality，而且违反当前固定 invariant，故不执行。

## 6. MoLingo Stage1 与 AR Stage2

更合理的顺序是先问 representation，再问 generator：

1. 在完整 `162,760` Pulp train IDs 上训练 non-causal MoLingo-style AE/VAE human tokenizer；
2. 用 full-sequence、length-binned reconstruction 检查 pose、root ADE/FDE、velocity 与 latent statistics；
3. reconstruction 通过只说明 necessary condition，仍需短程 human text-to-motion generatability screen；
4. 只有 Stage1 与短程 Stage2 都通过，才投入 matched full-budget Stage2 与 joint/camera extension。

当前 v7.14 latent**不能直接加载 official MoLingo AR checkpoint**：官方模型假定不同的 temporal downsample、latent dim、human-only token layout、text encoder/cross-attention 与训练分布；StoryMotion 是 joint `human128 + camera64` latent。可以保留 AR operator 并从零训练新的 input/output projection 与 generator。对离线整段 text-to-motion，Stage1 encoder non-causal 并不阻止 Stage2 自回归地产生 latent；代价是不能声称 streaming，也不能复用 official weights，decoder 需要拿到完整 latent sequence 后再解码。

v7.40 MoLingo-derived RF 已使用正确的 non-causal v7.14 cache；它在 `30k` 出现 semantic/recall 改善，但 coverage、joint 与 framing 退化。它说明该 operator 是 Pareto challenger，不是 causal tokenizer 的证据，也不足以否定重新设计的 human-only AR control。

## 7. MotionStreamer

MotionStreamer native TAE 与 streaming generator 都依赖 temporal causal semantics。把它改成 non-causal 后不再是 native MotionStreamer；保留 causal 又违反 StoryMotion 的固定 Stage1/Stage2 invariant。因此当前状态是**blocked by experiment contract**，不启动 Pulp Stage1 长训。只有显式修改 `AGENTS.md` 与 `storymotion/experiment_invariants.py` 的 causality contract 后，才能把它作为独立 native-system diagnostic 重新预注册；该动作不能由普通 control 默许触发。

## 8. 实验优先级与 gate

| priority | experiment | 当前动作 | Go 条件 |
| --- | --- | --- | --- |
| P0-A | v7.14 full-sequence length audit | 已完成 pure4053 | 已定位 human length gap；转入 representation treatment |
| P0-B | CondMDI official HumanML3D all-mask closed loop | 已完成 random-frames 750k checkpoint；renderer-only zero-keyframe bug已隔离 | output finite、有非零时间方差、mask sum=`0`；只记 capability，不做跨数据 ranking |
| P0-C | non-causal Stage1 representation screen | local v7.14、official Pulp AE、MoLingo-style AE/VAE；全 `162,760` train IDs | 长 bin paired gap明显缩小，短 bin不出现 broad regression；latent scale/ownership contract通过 |
| P1-A | same Stage2 × representation control | 先用 official Pulp AE cache复刻 L0，之后只晋级通过的 local candidate | Direct H 与 joint parallel同时改善，Direct C/geometry不 broad regress |
| P1-B | generation-native human Stage2 | local/candidate latent 上从零训练 AR 或 matched text-to-motion generator | 先过 human-only screen，再跑 full budget；reconstruction 单独不能触发长训 |
| P2 | candidate joint integration | 仅在 P0-C 与 P1-B 都通过后设计 camera/joint token layout | Direct H/C 改善且守住 L0 joint parallel hard gate |
| blocked | causal joint AE、MotionStreamer causal TAE | 不启动 | 必须先由用户显式修改 causality contract |

任一新 Stage1/Stage2 run 都必须把 exact `162,760` ordered train IDs、train/eval cache IDs、checkpoint 与 owning-decoder SHA、train-only stats、seed、batch、sampler与 sample exposures 写入 contract。不同版本混表必须有非空 `version / run`。
