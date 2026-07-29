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
  - "[[Storymotion-exp-sha]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
  - "[[2026-07-27_storymotion-stage1-human-anchor-residual-control]]"
  - "[[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]"
  - "[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]"
  - "[[2026-07-29_full_re]]"
created: 2026-07-12T14:30:00+08:00
updated: 2026-07-29T15:38:19+08:00
---

# StoryMotion Version Family

> [!abstract] 本页职责
> 本页解释每个版本族在问什么、只改什么、属于 Stage1 还是 Stage2、实际完成到多少 step，以及哪些名字只是诊断编号。当前优先级只看 [[current]]；正式数字只看 [[StoryMotion-valid-metric-ledger]]；SHA 与 immutable identity 只看 [[Storymotion-exp-sha]]；run 中进度只看对应 `runs/` manifest/log。

## v10 Human-relative Camera 前置版本

v10不再修补 v9 的 `interaction16 + conditioned-camera48`。它以 Pulp-only Phase A `210K` 的 Human owner为唯一父节点，显式把Camera转换到 Human heading frame，Stage1只学习独立 relative-Camera48；Stage2 Human与Camera保持单向三角分解。Human teacher前置端点已完成；首条Camera Phase-B长训因缺少framing反传降为历史diagnostic，corrected-framing fresh run已通过30K smoke并在同run续训至210K。Camera flow／Unified-3尚未开始。

| label | parent / Stage | causal question | unique intervention | completed budget | finalized result |
| --- | --- | --- | --- | --- | --- |
| v10 HREL-C old-3-loss Phase B | Pulp-only Phase A `210K` / Stage1 | 冻结 Phase-A Human后，独立 Human-relative Camera48能否形成可重建的Camera表示？ | relative recon + temporal + rotation；漏掉v9合理framing supervision；Human exact；non-causal | Camera-only local `210K` + pure4,053 canonical audit + fixed8 | 历史diagnostic；不得resume、构建cache或晋升 |
| v10 HREL-C corrected-framing Phase B | same Phase-A `210K` / Stage1 | 在不恢复Human／interaction耦合时补齐Camera framing supervision能否形成正式endpoint？ | fresh `E_c,D_c`；fixed-projective center／log-scale／soft-out loss `0.1`；无learned framing head；Human frozen | contract + real-data preflight + first-128 `30K` smoke pass；same-run `30K→210K` active | formal endpoint open；长训与pure4,053 audit前无cache候选 |
| v10 Phase-A Human teacher | same Phase-A Human128 / Stage2 prerequisite | 未来Unified-3同实现Human branch能否独立形成可用Direct-H signal？ | Human-text-only `ViMoGenLightFlow`；fresh `105K` EMA；无Camera参数 | `105K` + first-512 Euler50 CFG1／CFG3 + v9 matched six-way fixed8 | basic generatability pass；CFG不是单调增益；strict physical gate未闭合；可作strict-transfer teacher；非Camera／joint证据 |
| v10 Camera flow / Unified-3 | future corrected Stage1 endpoint + Human teacher105K / Stage2 | 四route Camera flow能否同时支持GT-H Direct-C、sequential joint与synchronous joint？ | new176D cache；Camera48；route embedding与reliability gate；Camera不得影响Human | not run | blocked by corrected Stage1 formal endpoint及Human CFG support合同；不得从历史reconstruction或Human teacher提前推断结果 |

v10当前严格结论是：Phase-A父节点更正与Human teacher长训已经闭合；旧Camera Phase-B `210K`只拥有历史diagnostic身份，corrected-framing Phase-B通过30K screen后正在长训。两条前置路径尚未汇合成Camera flow或Unified checkpoint；Camera启动前还必须固定CFG1-only或离散CFG1／CFG3双cache support。durable训练合同和下一gate见 [[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]。v8.1C C3-25 seed17仍是mainline。

## v9 外部系统与 matched-backbone 证据版本

v9 先以外部系统和 matched-backbone controls整理 v8 mainline 的能力边界，随后完成一条独立的 redesign protected-H Unified-3 diagnostic：Pulp-only Human-anchor Stage1 `636K`，Human teacher `105K`，Camera/joint `105K`。该新 checkpoint不回写 C3 artifacts，也没有 promotion资格；v8.1C C3-25 seed17仍是 mainline。

| label | parent / Stage | causal question | unique intervention | completed budget | finalized result |
| --- | --- | --- | --- | --- | --- |
| v9 E1 G-SYS-H Stage1 | GestureLSM full-system / Stage1 | part-wise RVQ tokenizer 能否可靠重建 Pulp Human？ | upper/lower/torso-style three-region RVQ system、Pulp text-independent paired reconstruction | three RVQ endpoints `30K` + pure4,053 | reconstruction floor pass；只证明 tokenizer 可用 |
| v9 E1 G-SYS-H Stage2 zero-start | E1 RVQ owner / Stage2 | 移除 native observed start 后能否从 Human text 生成 Human199？ | GestureLSM tokenizer + velocity/shortcut objective + Pulp text substitution + zero initial latent | `105K` + N=512 Euler20 | 只关闭 zero-start 变体；不能代表 native continuation |
| v9 E1-R observed-start | E1 RVQ owner / Stage2 continuation | 恢复首 4 latent observed start 后是否出现可用 Human suffix generation？ | exact E1 Stage1/cache/objective；只修正 observed-start 语义 | fresh `105K` + suffix-only N=512 Euler20 | nonzero continuation ability；physical gate not robust；非 Direct-H |
| v9 E2 D-SYS-C | native DC3D-style / Stage2 Camera system control | 正确 MinMax 与充分训练能否得到可用 observed-Human Camera completion？ | raw Human→pose66、train-only MinMax Camera14、native DC3D losses/topology | `105K` + N=512 DDIM50 | broad regress 于 C3 Direct-C；stop；非 joint |
| v9 E3 C3-D-DC | C3-25 / Stage2 matched Direct-C | 固定 C3 representation/objective/evaluator，只换 DC3D topology 是否通过 Camera gate？ | DC3D SepCFG-style transformer topology；其余 C3 Direct-C boundary 固定 | fresh `105K` + N=512 DDIM50 | trajectory/rotation 改善，semantic/coverage 回退；trade-off stop |
| v9 E5 C3-MARDM-H | C3-25 / Stage2 Human-only system interaction | 固定 C3 Human representation 后，MARDM topology + objective 能否产生 Human free generation？ | Human128 masked autoregression + SiT velocity；无 observed start、Camera input/output 或 task row | fresh `105K` + N=512 MAR18 | generation capability pass；semantic/coverage 改善，global/root physical trade-off；非 pure-backbone |
| v9 E6 C3-ViMoGen-light-H | C3-25 / Stage2 Human-only system interaction | 固定 C3 Human representation 后，ViMoGen-light topology + shifted-flow objective 的 CLIP/UMT5 条件端点如何比较？ | Human128 full Transformer + token cross-attention + shifted flow；CLIP 与 UMT5 分别 fresh 训练；无 Camera/joint branch | 两条 fresh `105K` + 同 first-512 Euler50 | CLIP 为本次 E6 综合较强 endpoint；UMT5 只在 HCov 更高；两者 strict physical gate 均未通过，非 pure-backbone |
| v9 H-ANCHOR-S1 | Human-anchor residual control / Stage1 | HumanML anchor exposure 能否在守住 Pulp paired endpoint 时改善跨域 Human reconstruction？ | Human-first asymmetric architecture；Pulp-only control 对比 HML-root-local + Pulp-full | 两条 fresh `636K` + Pulp pure4,053 / HumanML val1,460 true-length audit | Pulp-only fixed8 支持 architecture controllability；mixed 的 rot6D mean-imputation 不合规，checkpoint invalid for Stage2；二者均不晋升 |
| v9 redesign protected-H ViMoGen Unified-3 diagnostic | H-ANCHOR-S1 Pulp-only / Stage2 | 严格保护 ViMoGen-light Human后，同一 checkpoint能否完成 Direct-H、Direct-C与joint parallel？ | Human128独立flow；Camera64 H→C cross-attention；Human105K后冻结，Camera三子阶段105K | global `210K` + 同 first-512三模式 formal + fixed8 | Human teacher/final exact且质量较高；Direct-C与joint Camera fail；diagnostic-only，不晋升 |
| v9 E2-J | external GestureLSM + DC3D / Stage2 joint design | external tokenizer/system 能否同时生成 Human 与 Camera？ | part-wise Human expert + raw/projective Camera expert | not run；非当前队列 | historical unexecuted design |
| v9 E3-J | C3-25 / Stage2 joint design | fixed-C3 dual expert 能否通过 joint Human/Camera gate？ | H128 part projections + C64 DC3D expert + raw geometry sidecar | not run；非当前队列 | historical unexecuted design |
| v9 E4-U3 | E3-J architecture / Unified-3 design | 同一 checkpoint 能否通过 Direct-H、Direct-C、joint parallel？ | topology 固定；只加入三模式 task routing/exposure | not run；非当前队列 | historical unexecuted design；不得追认当前 protected-H run为该编号 |

v9 的严格结论是：corrected E1-R 证明旧 zero-start 适配低估了 GestureLSM continuation 能力，但 physical quality仍不稳健；旧 E2/E3没有保留或完整使用 raw-projective boundary。C3-MARDM与C3-ViMoGen Human-only controls证明 fixed-C3 Human latent在其他 topology/objective/condition系统中可形成更强 Human free-generation signal。H-ANCHOR-S1 Pulp-only支持 Human-first asymmetric decoupling，mixed arm则因 rot6D伪观测被 invalidated for Stage2。随后完成的 redesign protected-H checkpoint确实给出三种 mode：Human被逐元素保护且指标较强，但 Direct-C与joint Camera均失败；Camera curriculum遗忘、CFG／observed-H接口及Camera64 manifold／geometry gate是当前诊断轴。它仍不是可晋升三模式 system，也不支持 pure-backbone capacity归因。完整实现与根因见 [[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]。

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
| C3-25 seed17 Unified | C3-25 seed17 / Stage2 mainline selection | 新 latent 是否可生成，以及 `30K→105K` 是否只是训练成熟度问题 | exact parent/decoder/cache/full-cov stats；同一进程 `0→105K`，30K 固化但不重启 | continuous `0→105K` + formal pure4053 | `30K` 与 `105K` train/formal completed；Direct-H/Direct-C 多数指标击败 v7.38 L0，joint parallel 无 broad regression；当前 Stage2 mainline。历史 contract 的 non-promotion 字段只保留 provenance |
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
| v8.1C P0-JC-9 architecture-view family | C3-25 parent | included in fresh runs | completed within continuous runs | H-FULL/H-ISOLATED/C-JOINT/ALL-JOINT 均 completed；matched N=512 diagnostic closed；四臂 stopped |
| v8.1C P0-HUM-1 Human-only | C3-25 parent | included in fresh run | snapshots at matched exposure boundaries | Human-only `105K` completed；四 snapshots N=512 Direct-H screen closed；no formal |
| v8.1C P0-HATTR-1 no-update | C3-25 Parent + Human-only snapshots | **无训练** | fixed-input task-row/Camera-context、objective/manifold 与 heading attribution completed | diagnostic closed；最初预注册 P0-HVIEW-1，后被 architecture-path evidence 取代 |
| v8.1C P0-HARCH-0 no-update | C3-25 Stage1/Stage2 + Parent/Human-only | **无训练** | Stage1 Camera sensitivity、latent/text normalization path 与 pure-topology preflight completed | diagnostic closed；旧 run 不是真正 Human-only |
| v8.1C targeted Camera attribution | C3-25 Stage1 + Parent/Human-only Stage2 | **无训练** | coherent Stage1 Camera perturbation与 free-DDIM Camera-state matrix completed | Camera coupling与 cross-channel co-adaptation confirmed；Human-only 特有 feedback 主因不支持 |
| v8.1C P0-HVIEW-1 | Human-only native mixed-view parent | not run | not run | `superseded_before_launch`；保留预注册 provenance，无 optimizer/checkpoint |
| v8.1C P0-H128-S1 | native Human-only / Stage1 | short r2 closed；no Pareto | Human199→Human128→Human199；无 Camera data/parameter/loss | first run 因 contract path 违规安全停止且不复用；r2 scratch `10,176` 后按 gate 停止 |
| v8.1C P0-H128-S2 | C3-25 native Human slice | included in continuous run | fresh r2 completed at 35,006；30K/35,006 N=512 stopped | not run；不代表 Camera-free Stage1 |
| E1 G-SYS-H | three part-wise RVQ floors passed | included in zero-start and observed-start long runs | training-only milestones；不作短质量 gate | zero-start + corrected continuation `105K` closed；后者 nonzero ability / physical stop |
| E2 D-SYS-C | no independent Stage1 | included in continuous long run | training-only milestones；不作短质量 gate | MinMax `105K` N=512 Direct-C stopped；非 Human 或 joint evidence |
| E3 C3-D-DC | fixed C3-25 Stage1 | included in continuous long run | training-only milestones；不作短质量 gate | fresh `105K` N=512 geometry–semantics trade-off stopped |
| E5 C3-MARDM-H | fixed C3-25 Stage1 | included in fresh long run | 21K/42K/63K/84K/105K immutable milestones | fresh `105K` N=512 Human generation capability pass / strict physical not passed；非 joint |
| E6 C3-ViMoGen-light-H | fixed C3-25 Stage1 | included in two fresh long runs | CLIP/UMT5 均保留 21K/42K/63K/84K/105K immutable milestones | 两条 `105K` 同 first-512 Human eval closed；CLIP 综合较强，二者 strict physical stop；非 Camera/joint |
| v9 redesign protected-H ViMoGen Unified-3 diagnostic | H-ANCHOR-S1 Pulp-only control | exact-length cache与full-cov boundary闭合 | Human105K + Camera105K milestones、TensorBoard、三模式N512 formal均完成 | Human exact；Camera fail；diagnostic-only；当前做snapshot/CFG/manifold只读归因 |
| E2-J/E3-J/E4-U3 historical designs | parent depends on arm | not run | not run | 非当前队列；不得与已完成 protected-H run混名 |
| v8.1C C3-25 seed23 | completed `636K` | not run | not run | not run |

> [!important] C3-25 的直接答案
> C3-25 seed17 已构建并审计自己的 Stage2 cache，D1 排除了 dead-channel 与 branch-marginal collapse；continuous `30K` 与 `105K` 的 Direct-H、Direct-C、joint-parallel formal audit 均已闭合。global-slope 现为非阻塞 diagnostic pass，C3-25 正式成为 Stage1/Stage2 mainline。run 的历史 eligibility 字段不回写；正式数值只见 [[StoryMotion-valid-metric-ledger]]，artifact identity 只见 [[Storymotion-exp-sha]]。任何 `v8_1a_diag_unified3_30k_*` 仍只属于父候选 v8.1A。

## v8.0+ 家族地图

| family | causal axis | 目标 | 状态 |
| --- | --- | --- | --- |
| v8.0 | Stage1 read-only attribution | 定位 human199 长程误差责任通道 | GT-yaw oracle 完成；existing deep-AE screen No-Go |
| v8.1A | Stage1 geometry loss + Stage2 generatability | 修复 yaw/root 并检查 latent 是否可生成 | Stage1 full、Stage2 `30K` 与 D4 family 完成；无 `105K` |
| v8.1B | Stage1 architecture | residual AE capacity/control | Stage1 full 完成；无 Stage2 |
| v8.1C | Stage1 Camera-center/Human-horizon treatment + audited Unified-3 | 在 v8.1A 上形成 Human/Camera Pareto，并验证 C3 latent generatability | C3-25 seed17 Stage1/Stage2 mainline；`105K` 三路 formal completed；P0-JC-9、P0-HUM-1、P0-H128-S1/S2 与 E1/E2 screens stopped |
| v8.2 | Stage1 feature layout | human200 non-integrative root/yaw | Stage1 full 完成；无 Stage2 |
| v8.2333 | data curation | reversible multi-axis quality gradients、task-aware pools 与 matched continuation contract | v1 raw/Physical-v2/TMR-v4、162,760-row quality table 和五类 nested research pools complete as provenance；axis-purity audit 发现跨轴 strata 与小组尾门不可达，v2 required；Camera/framing/semantic axes unresolved，training unauthorized |
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
- **2026-07-22：** Tb25-band r4 从 C3-105K matched continuation 到 110K 后在 N=512 三模式 screen broad regression 并停止；no-update attribution 未确认 Direct-C/joint-C 在 shared trunk、Camera I/O 与 output head 的负平均梯度夹角，C3-105K 保持 mainline。
- **2026-07-22：** v8.2333 全量 quality gradients 与五类 nested research pools 完成；`manual_labels=0`、`source_deleted=false`、`training_authorized=false`。原 SFT 数据准备稿归档，正式质量/分档/pool/训练分配统一由 [[2026-07-17_storymotion-v8-2333-data-curation-plan]] 持有。
- **2026-07-23：** H-FULL/H-ISOLATED architecture-view 105K 与 matched N=512 screen 闭合；Human semantics/distribution 有局部正信号但 Human geometry 与 Camera endpoint 有代价，两臂均不接管 mainline。Camera 单轴 C-JOINT 与双轴 ALL-JOINT 保持独立剩余实验。
- **2026-07-23：** v8.2333 v1 axis-purity audit 闭合：跨轴 strata 会实际改变数千条 L2 membership，且大量小 stratum 的尾门数学上不可达；v1 artifacts 原样保留为 provenance，新 v2 必须采用 axis-pure strata 与 deterministic min-n/backoff。
- **2026-07-24：** C-JOINT/ALL-JOINT fresh 105K 与 exact-wrapper matched N=512 screen 闭合；Direct-H、arm-effective Camera task 与 joint 均 broad regress。朴素 view equality 路线关闭，四条 architecture-view arm 全部停止，Parent C3-105K 保持 mainline。
- **2026-07-24：** C3-25 原生 Direct-H Human-only `35,006/58,339/70,005/105,000` 四个 snapshots 的 N=512 screen 闭合；全部未形成 Human semantic/distribution 改善，pure4,053 不运行。统一混训/Human dose 不是首要瓶颈，下一轴改为 Human objective、heading 与 latent-manifold no-update attribution。
- **2026-07-24：** P0-HATTR-1 fixed-input no-update attribution 闭合。未训练 row 3 的独立混淆与 Direct-H Camera-context dependence获得支持；`t=799` heading amplification 获得 teacher-forced 支持；当前 manifold projection 与稳定负 shared-gradient conflict 未获支持。只预注册 P0-HVIEW-1：相对 Human-only native parent 单改 Direct-H `mixed→isolated` view，尚未启动。
- **2026-07-24：** P0-HARCH-0 no-update architecture-path attribution 闭合。旧 Human-only 被限定为旧 Unified topology 内的 update-allocation 实验；raw-latent LayerNorm dilution 与显著 Camera parameter-capacity 占用解释被排除，C3 Human code 的 Camera coupling和 Human-only 对循环 Camera state 的失配风险获得支持。
- **2026-07-24：** Human128 Stage1 transfer 与 Stage2 single-branch pipeline preflight 均通过且没有 optimizer update。P0-HVIEW-1 在启动前被取代；P0-H128-S2 被选为 fixed C3 Human representation 上的唯一 architecture-axis short preregistration，但未启动。Stage1 encoder-only/frozen-decoder retrain 保持为后续独立因果轴。
- **2026-07-24：** targeted Stage1 Camera perturbation 与 Parent/Human-only free-DDIM Camera-state matrix 闭合。C3 Human target 对 coherent Camera condition 有可测耦合，zero Camera 是夸大效应的 OOD stress；旧 Stage2 有强 cross-channel co-adaptation，但 zero/oracle/shuffle 均未 Pareto 修复 Human-only，且 Parent 通常更敏感。因此 Human-only 特有的自由 Camera feedback 不作为主要根因。
- **2026-07-24：** P0-H128-S2 首次执行在发现 5090 另一物理卡已有外部负载后于 checkpoint 前安全停止，原 run、一步日志与失败 provenance 原样保留且禁止续用。fresh r2 通过 no-optimizer mutable-boundary audit 与单测后，从 step 0 在物理 GPU2 启动；它仍是唯一授权的 Human architecture-axis short arm。
- **2026-07-24：** 用户另行显式授权独立 P0-H128-S1 native Camera-free Stage1 system screen。首个 run 因 contract 将 logical functional path 展开成 compatibility target，在一段未选训练前缀后安全停止；所有 artifact 原样保留且不续用。fresh r2 通过两机 Camera-free 单测与 contract audit 后，从零在 4090 物理 GPU0 启动；它与 5090 P0-H128-S2 不共享 checkpoint、cache、optimizer 或 causal claim。
- **2026-07-24：** P0-H128-S1 fresh r2 完成 `10,176` steps 与 pure4,053 Camera-free/non-causal/identity audit。matched C3 short 对照下没有 decoded Human Pareto win；paired uncertainty 只确认 heading 稳定退化，训练 objective 的过程表现不改变 decoded stop decision。按预注册停止，不做 full-budget、cache 或 Stage2。首次 run 的目录实际含 step-2,000 checkpoint，故原 manifest 的 `step0` boundary 描述不再作为事实依据；失败 artifacts 与字段仍原样保留。
- **2026-07-24：** Stage2 diagnostic ladder 的 closed-through-Human-only 长快照移动到 `archived/diagnostics/`，pre-refactor `current.md` 移动到 `archived/progress/`，pre-Human-first metric ledger 移动到 `archived/metrics/`；三个 canonical 路径分别重建为 live ladder、current decision 与正交 evidence ledger。历史表格、协议、hash 与来源未删除。
- **2026-07-25：** P0-H128-S2 的 30K/35,006 N=512 hard gate 闭合并停止；训练过程没有转化为 decoded Human semantic、geometry 或 physical-quality 通过。该结果只增强 architecture/inductive-bias/objective/latent-topology mismatch 假设，不证明参数容量或 backbone 能力上限。
- **2026-07-25：** E1/E2 的短质量评测从活动 evidence/decision 撤下；immutable roots、checkpoints、metrics、visuals 与 failure logs 保留 provenance，但不再用于 stop、promotion 或 architecture 归因。
- **2026-07-25：** 四臂未来 optimizer run 新增 fail-closed observability contract：run-local TensorBoard 与总进度 20%/40%/60%/80%/100% checkpoint 为强制项。E1/E2 适配 trainer 已接入；旧 screen 不回写、不补造中间 artifact。E3/E4 只登记设计要求，既有 E4 草稿骨架隔离且不可训练/举证，仍待成功长训后的详细方案与用户确认。
- **2026-07-25：** 用户随后授权按 `105K` 正常训练量重训 E1/E2，并在 5090 GPU2 执行 E3。三条 fresh long run 均完成 TensorBoard 与 20% checkpoint milestones；旧 5K/10K roots、失败日志与 decisions 保持不变。
- **2026-07-25：** v9 三路 105K eval 闭合。E1 Stage1 pure4,053 RVQ reconstruction floor 通过，但 E1 zero-start Stage2 `105K` N=512 Human generation 因 semantic/coverage broad regression 停止；E2 native-MinMax `105K` 仍 broad regress 于 C3 Direct-C；E3 fixed-C3 `105K` 改善 Camera trajectory/rotation、牺牲 semantics/coverage，按 matched gate 停止。C3-25 Unified-3 `105K` 保持 mainline。
- **2026-07-25：** 复核 GestureLSM native code 后确认 `seed` 是首若干 observed latent frames，而非 RNG seed；旧 E1 把该条件置零，只能关闭 zero-start 变体。新 E1-R fresh `0→105K` continuation 已在 4090 GPU0 通过 no-optimizer preflight 后启动；quality eval 只允许 105K endpoint。
- **2026-07-25：** E1-R fresh `105K` 以首 4 latent/16 raw frame 为 observed sequence state 完成 suffix-only N=512 Euler20 eval 与 fixed/anonymous visual。它产生可辨 continuation，证明系统不是完全无法生成，但 8 个匿名样本中仍有明显 bone-length/速度/加速度异常，physical gate 未稳健通过；结果不属于 Direct-H 或 joint evidence。
- **2026-07-25：** joint-first dual-expert 设计启用：E2-J 先测试 external-tokenizer joint system，E3-J 再固定 C3-25 joint representation，E4-U3 最终测试同 checkpoint Direct-H/Direct-C/joint。旧 E2/E3 completion 不再替代 joint evidence。
- **2026-07-26：** E5 fixed-C3 MARDM Human-only fresh `105K` 完成 N=512 MAR18 + native SiT Dopri5 eval 与 raw-length fixed/blind visual。FDTMR/TMR/HCov 相对同 first-512 Parent 改善，8 个样本均非 collapse，generation-capability gate 通过；global/root motion 与部分 blind 样本的速度/骨长仍退化，strict physical gate 未通过。该 arm 同时改变 topology 与 objective，不支持 pure-backbone capacity claim，也没有 Camera/joint 输出。
- **2026-07-27：** E6 ViMoGen-light CLIP 与有效 UMT5 r2 均完成 fixed-C3 Human-only fresh `105K` 和同 first-512 Euler50 canonical eval。CLIP 是本次 E6 综合较强 endpoint；UMT5 只在 HCov 更高。两者 strict physical gate 均未通过，且都没有 Camera/joint 输出；最初 initialized-only UMT5 root 不登记为有效训练。
- **2026-07-27：** H-ANCHOR-S1 两条 matched fresh `636K` run 与 C3-25 Stage1 完成 Pulp pure4,053 / HumanML val1,460 true-length non-causal audit。Pulp-only 保留为 Human-first architecture control；mixed arm 的 HML rot6D mean-imputation因无显式 missingness被判为禁止的伪观测，checkpoint invalid for Stage2，只保留 root/local diagnostic。C3-25 mainline不变。Pulp 四路与 HML root/local 三路 fixed-8 已接入同一 4090:7865 Gradio；MotionStreamer272 副本因缺 1,918 个 split motion 暂不进入 adapter。
- **2026-07-27：** metric owner 整理为只保留 canonical decoded-generation 数值；训练 objective、TensorBoard 与 optimizer 过程只保留在 run contract、manifest 和日志。C3-25 seed17 Unified-3 `105K` mainline status 不变。
- **2026-07-28：** redesign protected-H ViMoGen Unified-3 diagnostic完成 global `210K`与同 first-512 Direct-H、Direct-C、joint-parallel formal。Human teacher105K与final Human参数／输出exact，Camera训练未污染Human；Direct-C与joint Camera在semantic、coverage、caption、projective及geometry上相对matched C3系统总体退化。Camera fixed heldout在三个子阶段发生明显遗忘，alternating尾段梯度全面触发clip，final210K不是最佳Camera endpoint。该run不追认为旧E4-U3，也不晋升；当前只允许existing-snapshot、CFG/trust与interaction16/camera48 manifold归因。
- **2026-07-28：** v9 Camera P0–P3接力闭合。P0确认 `140K` Direct-C健康端点、`175K` HC改善／Direct遗忘与`189K`折中；P1 CFG／trust只有局部 Pareto；P2否定持续负 route cosine并确认历史 moments是放大器；P3两条 same-step balanced `10K`均稳定且Human exact，`1e-4`双路 fixed-loss胜出但仍未进入健康区，first-512 Direct-C／joint decoded gate失败。停止 full budget、PCGrad与P4；C3-25 seed17 mainline不变。
- **2026-07-29：** v10两条4090前置长训闭合。GPU0从Pulp-only Phase A `210K`冻结Human，fresh训练Human-relative Camera48 Phase B到本地`210K`；final `210K`完成pure4,053 canonical endpoint audit。复核确认旧四点表的`projective_outscreen≈0.5`是raw joint occupancy而非paired error，故旧`207K`选择只保provenance；final `210K`当时接管汇报／cache候选，真正paired Out error进入canonical ledger。该cache资格随后被下一条loss-contract更正撤销。GPU1完成同Phase-A Human owner的ViMoGen-light Human teacher `105K`，first-512与fixed8显示非塌缩生成信号，但strict physical gate未闭合。Camera flow、Direct-C、sequential／synchronous joint与Unified-3均未运行；C3-25 mainline不变。
- **2026-07-29（loss contract更正）：** 进一步审计确认v9 Phase B／C的Camera objective都含`0.1 framing`，Phase C没有新增Camera项，只额外加入Human objective；首条v10 Phase-B漏掉framing反传。旧`210K`与formal数值不删除，但降为old-3-loss diagnostic并撤销cache资格。v10用fixed geometry center／log-scale／soft-out framing补齐loss，不恢复interaction16、learned joint framing head或Phase-C Human更新；fresh corrected run从exact Phase-A `210K`父节点通过preflight及first-128 `30K` smoke后，已从exact `30K` checkpoint在同run续训至`210K`。v9／v10 Human teacher同实现同预算但owner latent非等价，四列matched fixed8已接入Gradio。
- **2026-07-29（Human CFG matched补测）：** v10同teacher checkpoint的CFG3 N=512与v9同teacher checkpoint的CFG1 N=512补测闭合；两版本CFG1／CFG3连同GT和v10 Human reconstruction已组成matched six-way fixed8并接入4090 Gradio。CFG3对v10是semantic／retrieval与运动幅度改善、distribution／paired geometry回退的trade-off；matched CFG1下v9／v10同样是混合结果，不能把视觉差异简化为单一CFG效应。代码审计同时确认v9 Camera训练不消费完整CFG1 Human rollout：Direct-C用GT Human，HC用noisy-GT单步conditional predicted-clean；该exposure mismatch只可能解释joint附加退化，不能解释Direct-C失败。v10 Camera启动前新增CFG1-only或离散CFG1／CFG3双cache的合同决策，不直接采用连续随机CFG。

## Bug 与 invalidation provenance

| issue | 影响 | 当前处理 |
| --- | --- | --- |
| v7.5–v7.13 使用旧 raw human199/camera9 与错误 decode contract | local Stage1/Stage2 ranking 不可靠 | 只保 provenance；v7.14 corrected contract 起算 |
| v7.15–v7.16 cache builder 忽略 `is_causal=false`，且 evaluator 用错 decoder | local Stage2 collapse 无法归因 | rows invalidated；v7.17 重建 cache并绑定 owning decoder |
| v7.18 epsilon/v full sampler 曾把 prediction 当 `x0` | pre-fix sampler rows 无效 | 只保修复后 rows；仍未通过 gate |
| v7.34 checkpoint contract 缺相邻 `run_config.json` | 首次 eval 在采样前 hard fail | 补齐 exact contract 后重跑；无无效 metrics |
| historical composed joint 可能让 cascade 两次 pass 使用不同 checkpoint 文件 | attribution provenance 不闭合 | same-run composition 强制同一 checkpoint SHA |
| 旧 E.T./Director artifacts 实际加载 StoryMotion checkpoint，部分还 test-as-validation | external baseline 错标 | 删除无效对象；只保 corrected Director-C |
| H-ANCHOR-S1 mixed 把 HML 非同源 rot6D 改写为 Pulp mean且没有 missingness token | 缺失通道被伪装为观测；full Human199 与后续 Stage2 representation claim 不成立 | immutable run只保 root/local diagnostic；checkpoint 禁止 Stage2/cache/promotion；后续必须使用 verified source SMPL rotations或显式 mask/独立 encoder |
| MoMask 首次从 HDD 随机读取小文件，随后又误用 `30K×512` 预算 | deployment 与预算均不可晋级 | packed-cache fresh run 从零完成 VQ159K、Mask240K、Residual240K；native Direct-H formal eval 已闭合 |
| CCD-Pulp 首次长训缺 owning-decoder SHA | contract 不完整 | 旧 run 标 invalid；corrected run 从 step0 重启 |
| v7.46 把 H/C 不适用的 Out 缺失当失败 | `10K` 后错误停止 | v7.47 从 step0 完整重训；v7.46 只作 bug provenance |
| C3 首次双臂共享 4090 HDD | 两臂只到 step `214`，无模型结论 | aborted state 禁止 resume；fresh fast-tier runs 从零重启；禁止多卡ddp并行单实验 |
| D4.3 v8.1A stats 的 pre-resume serialization 已不存在 | 无法做旧 bytes tensor-by-tensor 追溯 | r3 显式记录 expected/current/source-cache hashes；永久 diagnostic-only |
| C3 trainer 加载既有 full-cov stats 后会无条件重存，改变 serialization bytes | 不同主机产生不同 byte SHA，虽 tensor/content semantic SHA 相同 | 历史 C0 `0c97d247…3400` audit 不回写；新 run 绑定只读 semantic-equivalent artifact `7decc3dd…42af` 与 semantic SHA `2f9946a4…e5f`，trainer 已改为 existing path 只 load+validate、禁止原地保存 |
| architecture-view renderer 的 prompt-off 手工 loader 未恢复 checkpoint `human_view_mode` | H-FULL/H-ISOLATED 的 r1/r2 可视化实际按默认 `mixed` view 推理；不影响走 official bridge 的 N=512 eval | r1/r2 目录与日志原样保留并禁止展示；`render_bilateral_results.py` 修复为恢复并校验 exact Human-view contract（SHA256 `3f4e7662…c8d`），只接入 fresh r3 assets |
| official Stage2 evaluator 原先只重建 base `TemporalObsUNet` | C-JOINT/ALL-JOINT 与 Human-only 首次 r1 因旧 driver signature 在采样前失败；r2 在 exact-loader audit 前后只产生不完整/不可采信的 partial artifact，未形成两臂三模式结论 | r1/r2 roots 与日志原样保留；loader 现在从 run meta fail-close 解析 exact model class/owning trainer，并校验 loaded module/view/SHA。C-JOINT/ALL-JOINT r3 与 Human-only r3 才是有效 screen |
| P0-HATTR-1 contract 的 `created_at` 手填为晚于实际机器时刻 | 只影响 wall-clock metadata；日期、protocol、输入、hash 与 gate 不受影响 | 原 contract bytes 不回写；run-level `audit_report.json` 绑定原 contract SHA，并以 first child manifest start 作为机器观测上界 |
| v8.2333 v1 Physical strata 混合 H/C dynamics，且大量小组无法命中 conditional tail | `q_H/q_C` rank/gate/subset membership 非 axis-pure；v1 counts 不能当最终分层清洗 | v1 全部 artifacts/bytes 保留；v2 sibling builder 必须内嵌 code SHA，使用 axis-pure strata 与用途特定 min-n/backoff，不原地补写 |
| E5 eval/vis mask-length boundary | eval r1 把 latent `[B,75]` mask 与 raw `[B,300]` mask 比较；vis r2 又把 latent token 数当 raw frame 数 | 失败/无效 roots 与日志原样保留；eval r2 使用 `ceil(raw/4)` contract，vis r3 从 records 绑定 exact raw `valid_frames`，只有 r2/r3 进入结论 |
| Pulp TMR `match_skeletons` 用 batch-global 腿长最大值缩放 | 同一样本的 v8.2333 TMR score 会随 batch companions 改变；v1/v2 无效 | v1/v2 保留 invalid；v3 虽只剩 FP32 batch-shape 差，但其容差为事后放宽，亦停止并保留 invalid；v4 固定 singleton inference，64-sample replay exact |
| P3 初始 joint screen用独立实例 teacher作 bitwise functional reference | checkpoint内 Human state exact，但 joint two-branch Euler路径在结果写入前触发 exact guard；只留下空 records与原 contract，无指标 | 原目录与 contract保留为 failed provenance；r2新 driver绑定同一 loaded Human module的 joint two-branch公式，Human max-abs `0.0`后才产出 screen result |
| v10 Phase-B Pareto把native `projective_outscreen`当lower-is-better error | raw逐关节出框occupancy约`0.5`被误解为约50%配对误差，并进入旧framing selection axis | 不覆盖旧四点artifact；final `210K`补做canonical paired Out审计，三种Out语义由metric I/O fail-close区分；后续loss-contract更正使该endpoint只保历史diagnostic |
| v10首条Phase-B objective漏迁v9的`0.1 framing` | FOV／screen center／scale／projective residual只报告不反传；旧`210K`不能回答补齐合理Camera supervision后的结果 | 保留旧run为historical diagnostic；撤销cache资格；fixed-projective framing corrected run从Phase-A父节点fresh训练，trainer revision与contract hash拒绝旧resume |

## Evidence boundary

- 当前 mainline、非阻塞优化轴与下一授权动作：[[current]]。
- 所有正式数值与 uncertainty：[[StoryMotion-valid-metric-ledger]]；所有 SHA 与 immutable identity：[[Storymotion-exp-sha]]。
- Stage2 stop/continue ladder：[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。
- v8.2333 immutable curation contract：[[2026-07-17_storymotion-v8-2333-data-curation-plan]]。
- 旧部署 snapshot、proposal 与 forensic note 保留在 `archived/`；它们不产生第二套 current decision。

## 2026-07-21：P0-JC completion → joint 根因闭合

- C3-25 seed17 `105K` 同 checkpoint 的 GT-H replay 复现 Direct-C，generated-H 与 shuffled-H replay 依次暴露 H→C condition dependency。
- generated-H replay 仍显著优于 joint-parallel，因而根因分成 clean-H exposure gap 与 parallel evolving-H / joint-task gap；Stage1 与 normalization 暂不进入下一 intervention。
- active next event 是独立 Stage2 exposure remedy；v8.1A-105K 只作为新 run 的 budget-matched control，历史 v8.1A-30K stop provenance 不变。
- formal metrics 入口见 [[StoryMotion-valid-metric-ledger#C3-25 completion → joint 条件暴露归因（2026-07-21）]]；artifact identity 见 [[Storymotion-exp-sha#3.4 Relocated legacy identity blocks]]。

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

## 2026-07-22 — P0-JC-4 matched 30K representation diagnostic closed

- Corrected v8.1A and v8.1C C3-25 runs now share the same `4053` ordered IDs, five timesteps, seed/noise formula, batch/decode batch, and teacher-forced single-step boundary.
- v8.1A is better on most Human diagnostics; C3-25 is decisively better on Camera diagnostics. Joint preserves the Camera gain with mixed Human behavior.
- This finalizes C3-25 as a Camera-centered representation improvement, not a universal Human Pareto improvement.

## 2026-07-22 — P0-JC-5 independent v8.1A 105K control closed

- Run `v8_1a_unified3_105k_cont_seed17_4090g1_20260721` completed from the immutable v8.1A `30K` checkpoint with preserved model/optimizer boundary and the predeclared `30001` LR decay.
- All three formal `105K` profiles passed their audits on the same `4053` ordered IDs and sampler settings as C3-25.
- Direct-H mostly favors v8.1A; Direct-C and joint Camera/system favor C3-25. The historical C3-versus-A30 completion statement is invalidated as a maturity-confounded overgeneralization.
- C3-25 remains mainline for the coupled Human-Camera objective. The next intervention moves to Stage2 Camera exposure alignment.
