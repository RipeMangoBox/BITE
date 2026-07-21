---
title: "StoryMotion Version Family"
status: active
hypothesis: |
  Stable version-family names must identify the causal question, Stage boundary,
  unique intervention, budget, and evidence level so that experiment state is
  not inferred from a letter or version number alone.
tags:
  - StoryMotion
  - version-family
  - provenance
  - status/active
aliases:
  - StoryMotion-Version-Family
  - StoryMotion-History
  - history
source_notes:
  - "[[current]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
created: 2026-07-12T14:30:00+08:00
updated: 2026-07-21T15:42:04+08:00
---

# StoryMotion Version Family

> [!abstract] 本页职责
> 本页解释每个版本族在问什么、只改什么、属于 Stage1 还是 Stage2、实际完成到多少 step，以及哪些名字只是诊断编号。当前优先级只看 [[current]]；正式数字与 hash 只看 [[StoryMotion-valid-metric-ledger]]；run 中进度只看对应 `runs/` manifest/log。

## v8.1 命名解码与执行状态

> [!warning] 没有独立 v8.1D 或 v8.1H
> `D4/D4.2/D4.3` 属于 v8.1A 的 Stage2-30K 冻结诊断；`C4-H` 属于 v8.1C 的 Stage1 Human-horizon arm。字母 `D` 表示 diagnostic，`H` 表示 Human arm，不代表新的完整版本。

| label | parent / Stage | 目标 | 唯一核心操作 | 实际预算 | 已验证结果 |
| --- | --- | --- | --- | --- | --- |
| v8.1A Stage1 | v7.14 / Stage1 | 修复 human199 累计 yaw/root 长程误差 | 保持 architecture/data/IDs/non-causal contract，只加 decoded yaw/root geometry loss | fresh `636K / 81.38M` | 完成；Human 大幅改善，Camera mild regression；原始 gate 未全过 |
| v8.1A G3 | v8.1A / Stage2 | 检查新 latent 的三模式 generatability | exact v8.1A checkpoint/decoder/cache；与 v7.36 同 Unified implementation 和 `30K` 预算 | fresh `30K` train + pure4053 eval | 完成；Human 有 signal，Direct-C 与 parallel Camera broad regression；停止 |
| D4 | v8.1A G3 / Stage2 diagnostic | residual 在哪一段被放大 | N64、`t=50/500/950`，记录 whitened→decoder-input→decoded Camera 链 | **无训练**；read-only one-step | 完成；低噪方向性放大最明显 |
| D4.2 | v8.1A G3 / Stage2 diagnostic | Camera text 是否没接上或被忽略 | 同 N64/noise/`x_t`，只循环错位 Camera-text embedding | **无训练**；read-only one-step | 完成；排除简单 condition neglect |
| D4.3 | v8.1A G3 / Stage2 diagnostic | actual residual 是否命中 owning decoder 高敏方向 | RMS-matched actual/random direction，owning-decoder JVP/VJP | **无训练**；read-only local differential | 完成；仅低噪 `t=50` 通过方向敏感条件 |
| v8.1B | v8.1A / Stage1 architecture control | residual AE 是否增加有效容量 | 同 geometry loss/IDs/budget，改为 non-causal residual AE | fresh `636K / 81.38M` | 完成；Human 改善，Camera short-bin severe regression；无 Stage2 |
| C0 | v8.1A / Stage1 calibration | 标定 decoded Camera-center loss 的量级 | 8 个真实 `B=8` batch 测 shared-encoder gradient | **无训练** | 得到 C1 weight=`0.00406677828128799`，即 raw-center gradient target `5%` |
| C1 | v8.1C / Stage1 short | 高 dose center supervision 是否改善 Camera translation | 在 v8.1A 上只加 C0 weight | fresh `10,176` steps | 通过 structural screen，只授权 C2 full |
| C2 | v8.1C / Stage1 full | C1 高 dose 能否扩展到完整预算 | 与 v8.1A 唯一差异为 center weight=`0.00406677828128799` | fresh `636K / 81.38M` | Camera translation 改善；rotation 与 Human global slope fail；无 cache/Stage2 |
| C3-25 short | v8.1C / Stage1 short | 降低 center dose 后能否形成 Pareto | C1 weight 的 `25%`，即 `0.0010166945703219975` | fresh `10,176` steps | 通过；按预注册成为 selected full arm |
| C3-50 short | v8.1C / Stage1 short | 同一 dose-response 的较高臂 | C1 weight 的 `50%`，即 `0.002033389140643995` | fresh `10,176` steps | 通过；因两臂均过而不被选为主臂 |
| C3-25 seed17 full | C3-25 / Stage1 full | selected treatment 的同 seed 完整预算结果 | fresh seed17；不复用 short/aborted state | fresh `636K / 81.38M` + pure4053 | 完成；当前 Stage1 mainline，global-slope 为非阻塞 diagnostic pass；是下列 Stage2 mainline 的 exact parent |
| C3-25 seed17 Unified | C3-25 seed17 / Stage2 mainline selection | 新 latent 是否可生成，以及 `30K→105K` 是否只是训练成熟度问题 | exact parent/decoder/cache/full-cov stats；同一进程 `0→105K`，30K 固化但不重启 | `30K` 与 `105K` train/formal completed；Direct-H/Direct-C 多数指标击败 v7.38 L0，joint parallel 无 broad regression；当前 Stage2 mainline。历史 contract 的 non-promotion 字段只保留 provenance |
| C3-25 seed23 full | C3-25 / Stage1 robustness | 低 dose signal 是否跨 seed | fresh seed23；不存在 seed23 full A baseline | fresh `636K / 81.38M` + pure4053 | 完成；Human RA `24.70` / global `70.80`；Camera ADE `39.05` translation signal 重现；rotation `0.776°` fail、slope fail；**无 Stage2** |
| C3-50 seed17 full | C3-50 / Stage1 exploratory | 完整预算 dose-response | 用户后授权的 exploratory full；不改变 C3-25 selected 规则 | fresh `636K / 81.38M` + pure4053 | Camera ADE `36.41` 更好；Human global `73.17`、`193+` global `138.49`、slope `36.21` 全面变差；dose-response closed |
| C4 calibration | C3-25 / Stage1 calibration | 分开 Camera rotation 与 Human horizon 责任轴 | 8-batch unit-gradient norm/cosine；两个 arm 各取 parent gradient `1.25%` | **无训练** | 得到 C4-R/C4-H weights；只证明尺度与方向可区分 |
| C4-R | C3-25 / Stage1 arm | 修复 Camera rotation | 只加 decoded SO(3) auxiliary | **未训练** | selected C3-25 rotation 已过门，因此 blocked |
| C4-H | C3-25 / Stage1 short | 降低 Human global slope/long-bin error | 只加 last-valid Human yaw/root horizon auxiliary | fresh `10,176` steps | guards 过但两个 target 反向；gate fail，无 full |
| C5-A | C3-25 / Stage1 diagnostic | old last-valid surrogate 是否错配 formal evaluator | 比较 last-valid 与 four-anchor multi-horizon 的 per-sample alignment/gradient | **无训练**；read-only pure4053 | alignment pass；只允许另写 short-screen 预注册 |
| C5-B calibration | C5-A follow-up / Stage1 calibration | fresh initialization 下 multi-horizon 的可训练 dose 是多少 | seed17/23 各用前 `8×8` train samples、fixed-max 250；各自标到 C3 parent gradient `1.25%` 后取几何均值 | **无训练** | 完成；cross-seed ratio `1.021≤2`，冻结 base=`0.041302533967803944`、dose0.5=`0.020651266983901972`、dose1.0=`0.041302533967803944` |
| C5-B seed17 screen | C5-B / Stage1 short | multi-horizon 是否改善 global slope 与 `193+`，同时守住八项 Pareto guards | 同 seed/IDs/架构/预算比较 control、dose0.5、dose1.0；唯一 intervention 是冻结 weight | 三条 fresh `10,176` + pure4053 | dose0.5 fail；dose1.0 两项 target 与 guards 全过，只授权 seed23 short confirmation |
| C5-B seed23 confirmation | seed17 selected dose / Stage1 short | seed17 的 multi-horizon signal 是否跨 seed | 同 seed23/IDs/架构/预算比较 fresh control 与 dose1.0；唯一 intervention 仍是冻结 weight | 两条 fresh `10,176` + pure4053 | guards 全过但两个 target 都 fail；two-seed screen 停止，无 full |

### Dose 到底代表什么

`dose` 是 auxiliary loss 的 **shared-encoder gradient target**，不是数据比例、训练比例或实验完成度：

| arm | loss weight | 相对 C1 weight | raw Camera-center gradient target |
| --- | ---: | ---: | ---: |
| C1 | `0.00406677828128799` | `100%` | `5.0%` |
| C3-50 | `0.002033389140643995` | `50%` | `2.5%` |
| C3-25 | `0.0010166945703219975` | `25%` | `1.25%` |

所有 C3 short 都完整训练 `10,176` optimizer steps；所有 C3 full 都从零训练 `636,000` optimizer steps。`25%/50%` 不能写成只用了 `25%/50%` 数据或只完成相同比例训练。

C5-B 的 `0.5×/1.0×` 是相对 **fresh two-seed multi-horizon base weight** 的 loss dose；它与 C3 的 Camera-center `25%/50%` 不是同一 auxiliary，也不是数据或进度比例。C5-B short 同样必须完整训练 `10,176` optimizer steps，唯一 intervention 是 `human_multi_horizon_weight`。

## Stage2 完成度速查

| family / run | Stage1 | Stage2 `10K` | Stage2 `30K` train/eval | Stage2 `105K` train/eval |
| --- | --- | --- | --- | --- |
| v7.38 L0 | v7.14 parent | completed in historical ladder | completed | completed former formal mainline；当前为 C3-25 comparator |
| v7.46 official-AE control | official AE parent | completed screen | not completed | not completed |
| v7.47 official-AE control | official AE parent | completed | completed | **completed formal system control** |
| v8.1A | completed `636K` | completed within G ladder | **completed and audited** | **not run；stopped at 30K** |
| v8.1B | completed `636K` | not run | not run | not run |
| v8.2 | completed `636K` | not run | not run | not run |
| v8.1C C3-25 seed17 | completed `636K` | included in continuous run | **completed and audited；three active profiles pass** | **completed and audited；Direct-H and Direct-C beat v7.38 L0** |
| v8.1C C3-25 seed23 | completed `636K` | not run | not run | not run |

> [!important] C3-25 的直接答案
> C3-25 seed17 已构建并审计自己的 Stage2 cache，D1 排除了 dead-channel 与 branch-marginal collapse；`v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` 的 `30K` 与 **`105K`** 三路 formal audit 均已闭合。**`105K` Direct-H TMR `14.389` / FTD `222.12` 双双击败 former mainline v7.38 L0（`13.294 / 333.88`）；Direct-C CLaTr `59.539` / FCD `25.09` 双双击败 v7.38 L0（`55.64 / 33.29`）**。global-slope 现为非阻塞 diagnostic pass，C3-25 正式成为 Stage1/Stage2 mainline。run 的 `promotion_eligible=false` 是不可回写的历史执行字段。任何 `v8_1a_diag_unified3_30k_*` 仍只属于父候选 v8.1A。

## v8.0+ 家族地图

| family | causal axis | 目标 | 状态 |
| --- | --- | --- | --- |
| v8.0 | Stage1 read-only attribution | 定位 human199 长程误差责任通道 | GT-yaw oracle 完成；existing deep-AE screen No-Go |
| v8.1A | Stage1 geometry loss + Stage2 generatability | 修复 yaw/root 并检查 latent 是否可生成 | Stage1 full、Stage2 `30K` 与 D4 family 完成；无 `105K` |
| v8.1B | Stage1 architecture | residual AE capacity/control | Stage1 full 完成；无 Stage2 |
| v8.1C | Stage1 Camera-center/Human-horizon treatment + audited Unified-3 | 在 v8.1A 上形成 Human/Camera Pareto，并验证 C3 latent generatability | C3-25 seed17 Stage1/Stage2 mainline；`105K` 三路 formal completed；C5-B optional repair two-seed short fail |
| v8.2 | Stage1 feature layout | human200 non-integrative root/yaw | Stage1 full 完成；无 Stage2 |
| v8.2333 | data curation | reversible physical/semantic pair quarantine | G1/raw 与 physical distribution complete、TMR singleton distribution active；G0/G2 decision gate closed，quarantine 仍为 `0` |
| v8.4-A | Stage2 backbone | Motion Mamba-style non-AR latent DDPM | C3-25 representation owner 已固定；待单独授权 |
| v8.4-B | Stage2 backbone | TransPhase-style adjacent-phase control | blocked on v8.4-A matched baseline |

## v1–v7 家族压缩索引

| family | 主要问题 | 当前证据定位 |
| --- | --- | --- |
| v1–v3 | storyboard、ASG、局部编辑问题定义 | proposal provenance；无可比模型结果 |
| v4–v6.4 | official Pulp latent 上的 unified/completion/coupling/reliability | historical official-system anchors 与 condition diagnostics |
| v7.0–v7.4 | Stage2 routing、TrustGate、relation 与 asymmetric schedule | historical Stage2 design family；不回答 local tokenizer 质量 |
| v7.5–v7.13 | data hygiene 与 local tokenizer AE/VAE/quantizer 探索 | 受旧 feature/decode contract 影响，不进入当前 ranking |
| v7.14 | corrected normalized human199 + camera14 joint AE | former Stage1 implementation mainline；当前 comparator |
| v7.15–v7.16 | local Stage2 transfer | wrong decoder/causal cache invalidated evidence |
| v7.17–v7.30 | corrected cache/decoder、loss/normalization/sampler collapse closure | diagnostic chain；v7.30 证明 catastrophic collapse 可排除 |
| v7.32–v7.35 | camera/topology controls 与 Unified-3 task conditioning | system controls；camera9 separate 不能并入 camera14 joint evidence |
| v7.36 | `30K` asymmetric Unified-3 matched control | v8.1A G3 的唯一同预算 comparator |
| v7.38 | `105K` L0/L1–L4 long-run family | L0 是 former Stage2 formal mainline；当前 comparator |
| v7.42–v7.45 | specialists/external operator/curriculum controls | task/operator attribution；不是统一 representation ranking |
| v7.46 | official-AE Unified initial gate | 仅 `10K`；任务不适用 Out gate bug 后停止 |
| v7.47 | corrected official-AE Unified full control | `105K` formal audited system control；不替换主线 |

## Finalized milestones

- **2026-07-18：** v8.1A/B 与 v8.2 Stage1 endpoints 闭合；v8.1A 仅获 diagnostic-only Stage2 ladder。
- **2026-07-18：** v8.1A G3 `30K` 完成并因 Camera broad regression 停止；D4 family 随后只作冻结归因。
- **2026-07-19：** C3-25/50 fresh short 均完成；按预注册选择较低 dose C3-25。
- **2026-07-19：** C3-25 seed17/seed23 与 exploratory C3-50 full 均完成 Stage1 audit；C3-25 seed17 形成最佳 Human/Camera Pareto，global slope 保留为诊断项。
- **2026-07-19：** C4-H short fail；C5-A read-only alignment pass，但未授权 C5 training。
- **2026-07-19：** C5-B fresh seed17/23 train-distribution calibration 完成；两条 recommendation 的 max/min=`1.021`，稳定性 guard 通过并冻结 `0.5×/1.0×` short doses。该事件只授权预注册 short，不授权 full。
- **2026-07-19：** C5-B seed17 matched screen 完成；dose0.5 未过 target，dose1.0 通过两项 target 与八项 guards，按预注册只进入 seed23 confirmation，仍不授权 full。
- **2026-07-19：** C5-B seed23 matched confirmation 完成；八项 guards 全过但两个 target 都未复现，two-seed screen 按预注册停止，不启动 full/cache/Stage2。
- **2026-07-19：** 用户授权 C3-25 seed17 独立 Stage2 continuous `0→105K` diagnostic；exact cache、train-only full-cov normalization 与 run contract 审计通过，30K/105K active three-profile eval 由里程碑监督器执行且不在 30K 重启训练。
- **2026-07-19：** C3-25 Stage2 D1 完成 full train estimate 与 frozen pure4053 eval cache audit；未发现 dead-channel 或 branch-marginal collapse，raw Camera latent 仍呈低有效秩。该结果只关闭 cache health 风险，不产生生成质量结论。
- **2026-07-19：** MoMask-Pulp native VQ/Mask/Residual endpoint 的 Direct-H pure4053 formal eval 与独立 audit 闭合；第二次 full replay 的 4,053 条 records byte-exact。它只作为 C-tier native-system baseline，不解释为 StoryMotion representation ablation。
- **2026-07-19：** active Stage2 standard 收敛为 Direct-H、Direct-C 与 joint parallel；cascade 降为历史/显式 root-cause diagnostic。
- **2026-07-19：** `version.md` 与 v8 总页合并为 [[current]]；`history.md` 重构为本页；data-curation axis 改名 v8.2333，避免占用正常迭代号。
- **2026-07-20：** C3-25 seed17 Stage2 immutable `30K` Direct-H、Direct-C 与 joint parallel formal audit 全部通过 matched practical screen；decision=`pass_30k_active_profiles_continue_105k`，同一训练进程继续至 `105K`。
- **2026-07-21：** C3-25 seed17 Stage2 `105K` 三路 formal audit 闭合；Direct-H 与 Direct-C 多数指标击败 v7.38 L0，joint parallel 无 broad regression。selection policy 将 global-slope 改为非阻塞 diagnostic 并判定通过，C3-25 正式成为 Stage1/Stage2 mainline；历史 run ID/contract 字段不回写。

## Bug 与 invalidation provenance

| issue | 影响 | 当前处理 |
| --- | --- | --- |
| v7.5–v7.13 使用旧 raw human199/camera9 与错误 decode contract | local Stage1/Stage2 ranking 不可靠 | 只保 provenance；v7.14 corrected contract 起算 |
| v7.15–v7.16 cache builder 忽略 `is_causal=false`，且 evaluator 用错 decoder | local Stage2 collapse 无法归因 | rows invalidated；v7.17 重建 cache并绑定 owning decoder |
| v7.18 epsilon/v full sampler 曾把 prediction 当 `x0` | pre-fix sampler rows 无效 | 只保修复后 rows；仍未通过 gate |
| v7.34 checkpoint contract 缺相邻 `run_config.json` | 首次 eval 在采样前 hard fail | 补齐 exact contract 后重跑；无无效 metrics |
| historical composed joint 可能让 cascade 两次 pass 使用不同 checkpoint 文件 | attribution provenance 不闭合 | same-run composition 强制同一 checkpoint SHA |
| 旧 E.T./Director artifacts 实际加载 StoryMotion checkpoint，部分还 test-as-validation | external baseline 错标 | 删除无效对象；只保 corrected Director-C |
| MoMask 首次从 HDD 随机读取小文件，随后又误用 `30K×512` 预算 | deployment 与预算均不可晋级 | packed-cache fresh run 从零完成 VQ159K、Mask240K、Residual240K；native Direct-H formal eval 已闭合 |
| CCD-Pulp 首次长训缺 owning-decoder SHA | contract 不完整 | 旧 run 标 invalid；corrected run 从 step0 重启 |
| v7.46 把 H/C 不适用的 Out 缺失当失败 | `10K` 后错误停止 | v7.47 从 step0 完整重训；v7.46 只作 bug provenance |
| C3 首次双臂共享 4090 HDD | 两臂只到 step `214`，无模型结论 | aborted state 禁止 resume；fresh fast-tier runs 从零重启；禁止多卡ddp并行单实验 |
| D4.3 v8.1A stats 的 pre-resume serialization 已不存在 | 无法做旧 bytes tensor-by-tensor 追溯 | r3 显式记录 expected/current/source-cache hashes；永久 diagnostic-only |
| C3 trainer 加载既有 full-cov stats 后会无条件重存，改变 serialization bytes | active contract 的 stats file hash 会漂移，但本次前后统计 tensor exact equal | 保留漂移副本 `7decc3dd…42af`；从 exact train cache 与原 `created_at` 重建并恢复 contracted `0c97d247…3400`，重新 audit 通过；active run 结束前不改 tracked trainer code |
| Pulp TMR `match_skeletons` 用 batch-global 腿长最大值缩放 | 同一样本的 v8.2333 TMR score 会随 batch companions 改变；v1/v2 无效 | v1/v2 保留 invalid；v3 虽只剩 FP32 batch-shape 差，但其容差为事后放宽，亦停止并保留 invalid；v4 固定 singleton inference，64-sample replay exact |

## Evidence boundary

- 当前 mainline、非阻塞优化轴与下一授权动作：[[current]]。
- 所有正式数值、uncertainty 与核心 hashes：[[StoryMotion-valid-metric-ledger]]。
- Stage2 stop/continue ladder：[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。
- v8.2333 immutable curation contract：[[2026-07-17_storymotion-v8-2333-data-curation-plan]]。
- 旧部署 snapshot、proposal 与 forensic note 保留在 `archived/`；它们不产生第二套 current decision。

## 2026-07-21：P0-JC completion → joint 根因闭合

- C3-25 seed17 `105K` 同 checkpoint 的 GT-H replay 复现 Direct-C，generated-H 与 shuffled-H replay 依次暴露 H→C condition dependency。
- generated-H replay 仍显著优于 joint-parallel，因而根因分成 clean-H exposure gap 与 parallel evolving-H / joint-task gap；Stage1 与 normalization 暂不进入下一 intervention。
- active next event 是独立 Stage2 exposure remedy；v8.1A-105K 只作为新 run 的 budget-matched control，历史 v8.1A-30K stop provenance 不变。
- formal metrics 与 artifact hashes 只见 [[StoryMotion-valid-metric-ledger#C3-25 completion → joint 条件暴露归因（2026-07-21）]]。

## 2026-07-22 — P0-JC-4 v8.1A corrected side closed; matched decision remains open

- Finalized the corrected v8.1A `30K` single-step evaluation for Direct-H, Direct-C, and joint-parallel over five timesteps and the full `4053` test samples.
- The prior run without `--eval-source single_step` remains invalid and cannot be reused as single-step evidence.
- The A-side result establishes that joint degradation is not solely a multi-step rollout artifact; high-noise Camera degradation is already present inside the joint denoising mode.
- No v8.1A-versus-C3 family decision is recorded from P0-JC-4 yet because the completed C3-25 `30K` artifacts are unavailable while the 5090 host is offline.

## 2026-07-22 — existing Stage2 seed23 105K repeat invalidated

- Run `v8_1c_c3_25_diag_unified3_seed23_105k_4090g1_20260720` is fail-closed and is not a formal seed23 repeat.
- Its immutable `30K` checkpoint is seed23, but the continuation driver omitted `--seed`; the trainer initialized seed17 before resume, and the checkpoint did not preserve RNG state while resume restored only model and optimizer. The actual trajectory is therefore `0–30K seed23 + 30K–105K seed17`.
- The three endpoint evaluations share the same `105K` checkpoint and otherwise match `4053` samples, ordered IDs, batch/decode batch, and DDIM settings, but they cannot repair the training-seed boundary. Their missing experiment contract/profile audits, `diagnostic_contract=null`, and absent explicit version/run identity are additional formal blockers.
- Run-local provenance audit: `runs/train/stage2/v8_1c_c3_25_diag_unified3_seed23_105k_4090g1_20260720/provenance_audit_20260722.json`; SHA-256 `a8af56f7b2538216b079fe7b2cc2612bfc38b262ce6d16678f6b6ed54a12cae9`.
- These results must not enter the metric ledger or multi-seed aggregate. A corrected seed23 run requires a new run ID and a predeclared seed/RNG-resume contract.
