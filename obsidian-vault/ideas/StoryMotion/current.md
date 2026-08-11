---
title: "StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera Generation"
status: v11_c0_lat_mainline
hypothesis: |
  StoryMotion uses v11 C0-LAT as the operational mainline and tests a
  capability-preserving asymmetric Human–Camera extension. NoInt-HREL and
  C1REL-w/o-Interaction16 Stage1 audits and both C1REL Stage2 sequential
  formal artifacts are complete. The exact HREL-vs-C1REL Stage2 comparison is
  now formal but mixed-Pareto: HREL is stronger on Camera geometry while C1REL
  has higher Camera semantic aggregates; Human geometry has no clear winner.
  Observed-Human G-on/G-off route controls and the fully independent Human/
  Camera Stage1 native-system diagnostic are also formally closed. Its
  separately authorized Stage2 remains a secondary system-boundary run;
  neither changes the C0-LAT mainline.
  Original Pulp captions are authoritative and recaption is not a current
  evidence gate.
tags:
  - StoryMotion
  - version/v11
  - stage1
  - stage2
  - protected-human
  - status/active
aliases:
  - StoryMotion-Current
source_notes:
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[Storymotion-exp-sha]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[StoryMotion-iclr-reliability]]"
  - "[[paper-boundary]]"
  - "[[analysis/CVPR_2025/Dynamic_Motion_Blending_for_Versatile_Motion_Editing]]"
created: 2026-07-12T14:30:00+08:00
updated: 2026-08-12T01:45:27+08:00
---

# StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera Generation

> [!important] 当前裁决
> 自 2026-08-04 起，v11 C0-LAT 的 EMA Camera `105K` endpoint是后续唯一operational
> mainline。C0-LAT与C0-GEO同享 exact v9 Pulp-only Stage1、owning
> decoder/cache/train-only statistics 与冻结 Human `105K` teacher，只在 Camera
> objective 上分叉。选择LAT的理由是作者侧主表指标优先级与更简洁的单一latent-flow
> objective，便于后续训练和维护；不是geometry显著性裁决。C0-GEO相对C0-LAT的
> Direct-C与sequential六项Camera geometry 95% CI全部跨零，故GEO保留为完整审计的
> objective alternate／control。C3-25仍是former-mainline system baseline。

> [!important] seed23 matched repeat已闭合
> 两条C0 objective均以训练seed23从零启动并完成Camera `105K`、pure4,053三模式、
> decoded geometry／physical与10,000次paired bootstrap。Direct-H frozen-owner replay
> 通过；两个seed内的GEO−LAT及两个objective的seed23−seed17共24项Camera geometry
> 95% CI全部跨零。独立训练seed缺口已经关闭，但sealed audit与视觉失败分层仍未完成；
> 本结果支持保留统计不确定性，不阻止作者侧把C0-LAT设为后续operational mainline。正式证据见
> [[StoryMotion-valid-metric-ledger#4A. v9+ Stage2 audited detail tables]]。

> [!important] Stage1表示审计已闭合
> NoInt-HREL与C1REL均从零完成seed17 `636K`，并以exact pure4,053、真实有效长度、owning
> decoder和10,000次paired bootstrap完成正式审计。两臂都基本守住Human reconstruction；
> NoInt-HREL的Camera／framing系统性回退，支持I16参与Stage1 reconstruction，但不单独证明
> Stage2 generation necessity。作者据此搁置NoInt-HREL Stage2。C1REL的Camera
> trajectory／rotation回退且projective字段混合，与v9难分上下；其坐标语义更契合后续
> Camera text。C1REL与`C1REL-w/o-Interaction16` Stage2现均有原始Pulp caption下的
> pure4,053 sequential formal；只删除I16即广泛损害owning reconstruction／framing，
> 并在Camera生成中造成显著退化。这是有用的正向ablation evidence。C1REL seed23 的
> Direct-H／Direct-C／sequential 已完成 4,053 条 repeat audit；它仍是 raw-caption `T0`
> diagnostic-only、不可promotion的 cross-seed repeat，不替代最终 caption-matched retraining。
> 数值与 paired geometry uncertainty 只见
> [[StoryMotion-valid-metric-ledger#4A. v9+ Stage2 audited detail tables]]。
> HREL与C0-LAT的当前mainline身份不变。正式数值见
> [[StoryMotion-valid-metric-ledger#3. Active full-cohort Stage1 owner]]。

> [!important] HREL matched Stage2 formal已闭合
> HREL matched Stage2三接口均以pure `N=4,053`完成并通过artifact/hash、ordered-ID、
> non-causal与Direct-H teacher gate。与C1REL的exact ordered comparison是mixed Pareto：
> HREL的Direct-C三项Camera geometry及sequential ADE/FDE显著更强，rotation CI跨零；C1REL的
> Camera semantic aggregate更高，但semantic/framing没有逐样本paired unit，不能声称显著；
> Human geometry CI均跨零。完整数字与protocol exception只见
> [[StoryMotion-valid-metric-ledger#4A. v9+ Stage2 audited detail tables]]。

> [!important] C1REL Stage2 formal与caption边界
> GPU0运行`sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804`：复用已审计
> C1REL Stage1及owning decoder／新建C1REL cache与train-only stats，fresh训练Human
> teacher `105K`，冻结后再训练GT-H-only LAT Camera `105K`；该run已到达总step `210K`，并完成
> Direct-H、Direct-C与sequential pure4,053 formal。`rawt0`只属于immutable run identity；原始
> Pulp captions是authoritative text，不存在当前recaption依赖。GPU1运行
> `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804`：保留native
> C1REL-C48，只删除I16，latent为H128＋C48＝176D；其matched Stage2也已完成同一原始
> caption、exposure与sequential formal protocol。完整证据与剩余 queue 见
> [[StoryMotion-iclr-reliability#8.1 Evidence closure matrix]]。

> [!note] C1REL seed23 repeat boundary
> `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` 的三模式 artifact/hash、样本顺序、
> non-causal 与 checkpoint／decoder identity 已闭合；Direct-H=`17.455219 / 102.077736`，
> Direct-C Camera=`61.610401 / 20.361712`，sequential Camera=`60.909504 / 18.602613`。
> seed17↔seed23 的逐样本 geometry 95% CI 全部跨零；aggregate TMR/CLaTr 没有逐样本 semantic
> bootstrap 单位，不能写成显著性结果。审计 JSON 及 SHA 只见 ledger §3.17。

> [!important] C1REL-noI16 seed23 repeat已闭合
> `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` 的三模式pure4,053、artifact/hash、
> checkpoint/decoder identity与field-wise uncertainty已sealed。相对同seed full-C1REL，预声明的
> Camera semantic／framing退化方向再次通过，但geometry为mixed Pareto；seed17 noI16 reference另有
> training-contract旧bytes缺失，故cross-seed只作provenance-limited secondary repeat。该结果支持
> 两seed matched component protocol下的可重复贡献，不升级为普遍必要性或Stage2-only消融。数字只见
> ledger §3.20。

> [!important] 当前长训与评测边界
> PulpMotion native Stage2
> `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809`
> 已完成210K训练、105K／210K full-state checkpoint与4,053 native-joint formal audit；它与StoryMotion
> 的train/eval ID集exact匹配为`162,760/4,053`，不是StoryMotion的更小训练子集。结果有效但很弱，
> 且representation／decoder／mode不同，只作system-boundary negative result。true-P2 fresh symmetric
> 已完成105K joint endpoint及pure4,053三接口formal；结果是Human／sequential geometry改善、Direct-C
> 与sequential semantic／framing回退的field-wise mixed Pareto；这不等于总体相当，C0-LAT在投稿
> 优先的Direct-C geometry及两种Camera接口semantic／framing上明确占优。P1 HREL仅作同evaluator secondary control，严格
> 初始化C0-LAT reference现已完成同evaluator三模式formal及paired audit：相对C0，P2的Human与
> sequential Camera geometry更低，但Direct-C geometry及两种Camera接口的semantic／framing回退，
> 仍是mixed Pareto。source-row replay同时确认C0 sequential使用训练未覆盖的row1，并在4,053/4,053
> 个样本上改变Camera输出。该row来自共享C0／C1实现中的C1 route adaptation；StoryMotion从未主张
> observed／generated Human双来源匹配，因此它是historical C0的冗余实现变量，而不是核心claim缺口；
> 既有formal artifact继续有效。正式结果见
> [[StoryMotion-valid-metric-ledger#4A. v9+ Stage2 audited detail tables]]。
> observed-Human root-cause pair现已formal闭合：4090 GPU0的
> `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810`（G=on）与5090 GPU3的
> `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810`（G=off）均完成`105K` endpoint、九次
> gradient audit、full-state reload与pure4,053三接口seal。G=on相对G=off显著改善Direct-C三项
> Camera geometry及sequential ADE/FDE，Human geometry CI均跨零；semantic／framing仍是mixed
> Pareto，且跨4090／5090必须保留runtime covariate。相对historical `observed_human=false`，新route
> 大幅修复两种Camera接口的semantic／framing collapse，但六项Camera geometry显著回退；相对exact-init
> C0-LAT也不存在全局winner。因此本组关闭route root-cause执行，不支持protected-asymmetry全面优越。
> 这里的“无全局winner”只否定逐字段支配，不撤销C0-LAT在作者优先Camera／系统质量字段上的主线优势；
> 4090 GPU1的exact-init C0 source-row diagnostic仅作为historical实现provenance保留。作者已另行授权
> 只删除source identity的fresh C0-LAT Camera Stage2 `105K`清理臂
> `sm_c0_lat_nosource_c105k_seed17_4090g0_20260812`；v9 Stage1与Human teacher冻结，endpoint／formal
> audit前不替换mainline。正式结果与hash只见ledger §3.22。
> 完全独立Human／Camera Stage1 native-system也已完成两条fresh `210K`、105K／210K full-state、
> pure4,053与paired bootstrap。两branch独立性、train-only normalizer/cache及latent non-collapse均通过；
> 210K在各自全部预声明error字段上显著优于105K，但Human仍弱于v9 owner，Camera与v9为不同
> representation／decoder下的mixed comparison。它只保secondary system boundary；后续独立双EncDec
> Stage2已获单独授权；live execution state只由其run manifest／logs拥有，当前尚无endpoint或formal
> generation结论。Stage1正式结果只见ledger §6.9。
> no-I16 seed23的`210K`训练、Direct-H、Direct-C、sequential pure4,053与sealed audit均已闭合；
> 完整数值只见ledger §3.20，本页只保留上述mixed-geometry与非Stage2-only边界。
> 已部署的Human-text条件归因矩阵
> `sm_ht_condition_attribution_pure4053_20260810_r2`：HT-FILM／HX／DR各自只改变Camera侧
> Human-text为absent或fixed-point-free shuffled，覆盖Direct-C与sequential完整4,053；Camera text、
> Human context、sample IDs、noise与checkpoint固定，且不构造optimizer。该矩阵只判断matching-text
> 改善能否归因于正确Human语义，不参与C0-LAT promotion；结果尚未审计。
> step与ETA只见各自`runs/`，本页不重复。

> [!warning] ICLR QA status
> symmetric route-control执行缺口已经关闭，但结论是field-wise mixed Pareto；historical source-row
> 只属于C1 route adaptation遗留的实现清理，不是StoryMotion claim或投稿阻塞项。sealed blind audit
> 仍在pending。PulpMotion native
> Stage2 已闭合为有效弱system-boundary result，不再是执行缺口。C1REL seed23 的 raw-caption repeat audit 已闭合，但仍是
> diagnostic-only，不能当作最终 caption-matched evidence；C1REL-noI16 seed23也已sealed，支持两seed
> component方向复现但不支持普遍必要性。exact HREL-vs-C1REL Stage2缺口已经关闭，
> 但结论是mixed Pareto。独立H/C Stage1同样只关闭secondary native-system reconstruction，不提供
> Stage2或核心单变量证据；剩余投稿QA是C0-LAT Camera-text ownership、sealed blind audit／visual
> failure taxonomy、sealed resource profile与release package。

> [!note] Caption boundary
> 当前StoryMotion正式证据冻结使用原始Pulp captions；历史recaption/v2-pre artifacts只保留为
> provenance，不写回当前training manifest，也不阻塞投稿。若投稿后继续做caption curation，
> 必须另建版本化数据合同，不改写本轮formal run。

> [!note] Compositional utility边界
> StoryMotion的核心仍是capability-preserving human-motion generation与sequential Human→Camera；
> composition/editing只是secondary utility extension，不升格为第二主问题。MotionRemix／MotionCutMix
> 借用的是raw Human composition operator，目的不是上／下半身增广本身，而是构造组合式H–C训练pairs、
> 打破原始一对一Human–Camera pair correlation。
> 每个composite Human必须把独立Camera program／trajectory retarget或re-solve到新的Human上，重新生成
> Camera14、projection与framing并重算pair-dependent I16／C48；不得直接保留不再有效的$C_A$或拼接旧latent。
> 数据构造需允许每个Human对应多个Camera program、每个program对应多个Human，manifest记录source、operator、
> retarget／re-solve、filter reason与split，并使用composition-disjoint eval。由于v9 Stage1已在Camera14、
> I16、C48及$D_c/D_f$处耦合H–C，第一步只能做frozen Stage1 support audit；优先冻结$E_H/D_H$，finetune
> pair-side encoder／decoder／framing并混合factual replay；若support失败，才授权fresh Stage1全训并生成
> 新checkpoint、cache、stats与decoder，完整复验Human prior后才能训练Camera Stage2。当前不部署长训；任一
> data／Stage1／Human-retention gate失败即留作future work，不写free editing。完整gate见
> [[StoryMotion-iclr-reliability#4.5 Compositional utility边界]]。

> [!important] Scope
> 本页只服务 **StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera
> Generation**。DIRECT文档已迁移到`obsidian-vault/ideas/DIRECT/`，其状态只见
> [[DIRECT/current|DIRECT current]]。两篇论文仍共享StoryMotion代码仓库；当前不创建
> DIRECT代码仓库。完整贡献边界见[[paper-boundary]]。

> [!failure] Explicit framing `30K` 不进入 mainline
> 冻结 C0-GEO 上的 CF-4 framing adapter 虽在 N64／pure4,053 都形成可测 control
> adherence，absent-control 路径也保持 exact，但 matched pure4,053 Direct-C 与
> sequential 在 semantic、coverage、caption 与 projective framing 多字段回退。
> 因而该轴以 diagnostic-only 关闭；不替换C0-LAT mainline。裁决见
> [[archived/experiments/2026-07-31_storymotion-v11-explicit-framing-control]]，正式数值见
> [[StoryMotion-valid-metric-ledger#6. Special diagnostics retained outside ranking]]。

> [!warning] Camera temporal editing触发hard stop；组合式H–C utility不得直接进入长训
> Camera64在mask外exact时仍造成far world Camera-center漂移，endpoint oracle也失败，
> 因而当前Camera representation停止。Human128的naive clamp同样产生root／global-joint
> 漂移，但N8 mask-local endpoint oracle四格全过，证明当前Human128存在端点闭合headroom。
> 这只保留为endpoint-existence evidence；为收缩投稿scope，不再安排Human短screen，temporal editing／MAE
> 轴不启动长训，也不形成paper editing claim。组合式H–C utility另受4.5的data、Stage1 support与Human
> retention gates约束，未通过前不部署长训。该hard stop只约束temporal editing／MAE轴，不覆盖
> `0803-2024`已单独定义的NoInt-HREL与C1REL表示对照。分别见
> [[archived/experiments/2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]与
> [[archived/experiments/2026-07-31_storymotion-v11-human-temporal-locality-control]]。

> [!important] v10关闭；Raw-H只作为v9 sibling control
> 不再补v10 corrected endpoint、176D cache或Stage2。Stage1 observation现为低优先级，
> 只允许在保留exact v9 Human owner、Camera64 layout与non-causal边界下另建sibling；当前
> StoryMotion不启动Raw-H Stage1长训，也不借该历史轴改变当前matched representation合同。

## 0. 文档路由

- 当前论文：StoryMotion。
- 当前方法owner：v11 C0-LAT operational mainline；C0-GEO audited alternate。
- 当前实验owner：[[StoryMotion-iclr-reliability]]。
- 正式数字owner：[[StoryMotion-valid-metric-ledger]]。
- DIRECT状态与队列：[[DIRECT/current|DIRECT current]]；不在本页复述。
- 代码仍只有`linkedCodebases/StoryMotion/`；文档按StoryMotion／DIRECT分目录。

本页只拥有当前选择、允许的 claim、活跃 blocker 与 evidence link。正式数字与哈希
只见 [[StoryMotion-valid-metric-ledger]]；版本事件只见 [[version_family]]；StoryMotion中稿
差距与优先级只见[[StoryMotion-iclr-reliability]]。

## 1. Mainline 合同

| component / run | fixed boundary | current role |
| --- | --- | --- |
| shared Stage1 / `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726` | non-causal；Human199 + Camera14；`human128+interaction16+camera48`；owning `D_h/D_c/D_f` | C0-LAT mainline与C0-GEO alternate的共同representation owner |
| shared Human / `v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727` | Human text → Human128；EMA `105K`；Camera 训练全程冻结 | Direct-H owner；sequential 的第一阶段 |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | GT-H Camera training；latent flow；Camera EMA `105K` | 后续唯一operational mainline与默认ablation parent |
| v11 C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 同 C0-LAT，另加 calibrated Stage1-style decoded Camera auxiliary | audited alternate／objective control；不再默认续训 |
| v8.1C C3-25 / canonical `105K` | former joint-AE + Unified-3；formal joint parallel | primary former-mainline baseline |

两个 v11 endpoint 都必须报告三种模式：

1. Direct-H：Human text → Human；
2. Direct-C：GT／observed Human + Camera text → Camera；
3. formal sequential：先 Human text → Human，再以最终 Human + Camera text → Camera。

`joint_parallel=false` 是 v11 固定边界。未经单独授权，不补训、不评估，也不以
joint parallel gate v11。历史合同中的 `diagnostic_only=true` 与
`promotion_eligible=false` 保留为当时执行授权的 provenance；本次 selection event
不回写 immutable artifacts。

## 2. 选择依据与结论边界

- 四臂均已闭合 Camera optimizer `105K`、pure4,053 三模式 formal audit、decoded
  geometry、no-reference physical diagnostics、10,000 次 matched bootstrap 和
  fixed-8 visual。C1 两臂不进入 mainline。
- C0-LAT 与 C0-GEO 的 Human 输出逐字段相同；Camera objective 差异没有形成稳健
  geometry 胜者，且 semantic／coverage／framing 各有取舍。C0-LAT的mainline身份是
  基于作者侧主表优先级与更少objective组成的operational选择；不得改写为LAT统计显著支配GEO。
- 对 C3-25 的比较是 system replacement boundary：Stage1、decoder、sampler 和
  formal joint solver 都不同。可以报告三模式系统级 Pareto，不写成单变量支配。
- v9是首个可用Stage1 owner；其普通first-512 Stage2 screens已退出活动证据，不进入排名。
  PulpMotion是native joint baseline；sample count、条件合同与decoder不同的字段必须显式留空或限制结论。
- v11 自由 Human 的语义／构图改善与偏低 dynamics 幅度并存。contact／skate 仍是
  heuristic，不能写成 calibrated physical validity。

## 3. 当前论文主张

StoryMotion 的目标是中稿 ICLR 2027。当前中心主张收口为：

> 在一个non-causal capability-preserving asymmetric design中支持Human generation、observed-Human
> Camera generation与sequential Human-then-Camera generation；在Camera扩展中保持
> Human owner及其输出路径不变，并由同一Camera模型执行observed-H与generated-H。

Sequential是factorized joint distribution的两个推理pass，不声称同步或双向joint
denoising。Direct-H是被保留的基础能力，不写成Camera扩展带来的新提升。后续训练、
消融与主表默认使用C0-LAT；C0-GEO作为同方法objective alternate保留完整数值、视觉与
统计边界，不跨endpoint摘取单列最优。DIRECT的可迁移摄影program属于第二篇，不再覆盖本主张。

与Auteur的边界必须明确：Auteur uses Human trajectory to anchor Camera trajectory for downstream
ViGen；StoryMotion works on Human motion generation and capability-preserving Human–Camera generation。

本轮StoryMotion正式证据继续使用原始Pulp captions；历史recaption候选与caption curation不属于
当前方法贡献或实验门槛。若未来将数据修订写成独立贡献，必须保留原caption、来源和版本化合同，
并单独证明其增益；本轮不把它与C1REL Stage2或任何baseline superiority claim绑定。

## 4. 活跃 blocker

1. **表示与factorization主对照。** NoInt-HREL Stage2保持搁置；strict C1REL-noI16的Stage1与
   matched Stage2 formal已闭合，支持Interaction16的simple-and-effective组件价值。exact
   HREL-vs-C1REL Stage2已formal闭合，但为mixed Pareto，不支持单边representation superiority。
   full-C1REL seed23 raw-T0 repeat audit与历史true-P2三接口formal均已闭合；
   `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` 与
   `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` 已完成`observed_human=true`下
   G=on／off（U均为on）的endpoint、三接口及matched comparison audit。G-on改善Camera geometry但
   semantic／framing mixed，observed route修复历史semantic／framing collapse却牺牲Camera geometry；
   不形成单边factorization superiority。同初始化C0-LAT reference与source-row diagnostic已sealed；
   后者定位C1 route adapter在historical C0中的冗余影响，不是双来源能力缺口。用户已另行授权并部署
   `sm_c0_lat_nosource_c105k_seed17_4090g0_20260812`，只删除source identity并fresh训练C0-LAT
   Camera Stage2 `105K`；其完成与否不改变核心claim定义；
   C1REL-noI16 seed23三模式与sealed audit已闭合，不再是执行缺口。
   完整边界见
   [[StoryMotion-iclr-reliability#2. `0803-2024`表示因果矩阵]]。
2. **投稿证据闭环。** PulpMotion native Stage2 已在matched available-data cohort上formal闭合；
   保持PulpMotion自身representation／decoder／native-joint mode，结果只作system boundary，不与
   StoryMotion三模式伪装成单变量对照。Direct-H已恢复MoMask-Pulp native与
   MotionLab-MFT representation-matched adaptation两条formal pure4,053行；MoLingo-derived
   v7.45只有provisional full-cohort screen，缺独立audit与可恢复的历史训练源码SHA。
   MotionStreamer仍只有Stage1 reconstruction，缺native text→motion Stage2。Direct-C已恢复
   corrected Director-C／E.T.正式行；CCD-Pulp合同、fixed endpoint、完整IDs与records可核验，
   但缺独立audit artifact。两者均缺同口径decoded Camera geometry。PulpMotion与TSA是结构化
   motion主baseline，Auteur、Uni3C与ActCam按不同任务层级比较。
   C0 seed23独立长训与matched repeat audit已闭合，两个C0 seed都不支持单一
   Camera objective胜出；仍需sealed audit、随机／最好／最差可视化和failure taxonomy。
   observed=true G-on／G-off pair的endpoint、三模式与matched comparison均已sealed；4090 GPU1的
   exact-initialization C0-LAT及`source_id` row0／row1 diagnostic也已sealed。旧C0的row语义作为
   historical实现provenance披露；4090／5090 runtime covariate继续约束跨主机因果比较。
   完全独立Human／Camera Stage1的105K／210K pure4,053 audit亦已闭合。核验表明每臂210K是
   optimizer steps、各26.88M exposure，不是v9双倍样本；用户据此另行授权独立H128+C64 cache／
   normalizer／decoder的Human105K+Camera105K LAT Stage2。该链仍只作secondary native-system
   boundary，不进入核心单变量矩阵；endpoint与formal结果产生前不写generation结论。
   `0810-2137`建议中，current C0-LAT的Camera-text correct／shuffle／absent ownership audit、
   sealed visual blind audit与latency／参数／显存profile仍是明确缺口。
   基础盲评只用于可信度。最终还需冻结论文代码、配置、三接口evaluator、checkpoint／decoder身份、
   参数量、GPU小时、推理成本与最小复现实验包。
3. **措辞边界。** sequential不写成同步joint；显式3D motion generation不写成ViGen
   controllability；生产可用性、Rect与program transfer全部留给DIRECT。
4. **组合式utility gate。** MotionRemix／MotionCutMix只提供raw Human composition operator的参考；
   组合式H–C pair构造必须先通过独立Camera program retarget／re-solve、Camera14／projection／framing／
   I16重算、filter、many-to-many manifest与composition-disjoint eval，再做frozen Stage1 support audit。
   在$E_H/D_H$冻结、pair-side finetune＋factual replay或必要的fresh Stage1及Human-prior复验完成前，
   不得部署Camera Stage2长训；失败则留future work，不写free editing。

RV、Rect、HumanML3D、Director ownership与ViGen utility均由
[[DIRECT/current|DIRECT current]]路由，不再阻塞StoryMotion收口。

## 5. 当前行动边界

- 冻结C0-LAT为后续唯一operational mainline与默认ablation parent；C0-GEO保持audited alternate，
  不删除其正式结果，也不默认复制后续训练矩阵。
- StoryMotion后续实验若没有另行说明，默认seed17；run ID与contract仍必须显式记录
  `seed17`。改变seed必须预先写明理由，历史seed23 provenance不改名。
- NoInt-HREL Stage2保持搁置；C1REL与`C1REL-w/o-Interaction16` Stage2 sequential formal
  均已完成并使用原始Pulp captions。full-C1REL seed23 raw-T0 repeat audit已闭合；新部署的
  `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` 是 no-I16 seed23 replication，
  已完成`210K`训练、三模式pure4,053与sealed audit；结论限于两seed component方向复现、geometry
  mixed Pareto及non-Stage2-only边界。PulpMotion Stage2已formal闭合为有效弱system-boundary result；true-P2
  fresh Matched Symmetric已完成训练endpoint及三接口formal，保留mixed-Pareto与P1初始化不匹配边界。
  observed=true coupled／detached pair的endpoint、三模式、paired bootstrap与sealed comparison均已完成；
  结论限于route repair与G-on局部Camera geometry effect，保留mixed semantic／framing与
  cross-runtime边界。GPU1 exact-initialization C0-LAT与`source_id` diagnostic只建立historical
  implementation sensitivity；它不对应双来源claim。已授权的no-source C0-LAT只重训Camera Stage2，
  在完整审计前不触发mainline promotion。
  exact HREL-vs-C1REL Stage2已闭合并保留mixed-Pareto边界，
  不由当前结果自动扩张其他Stage2矩阵。
- `C1REL-w/o-Interaction16`严格matched Stage1与Stage2均已闭合；广泛退化作为Interaction16的
  正向组件ablation。no-I16 seed23的正式评测与审计进一步复现semantic／framing方向，但不把
  mixed geometry或provenance-limited cross-seed包装成普遍必要性；既有artifact不回写。HREL matched
  comparison已在上方formal closure中闭合。
- 历史`pulp_camera_recaption_v1p0_rotvec_h1_eventplan_20260805`现登记为v2-pre并保持immutable；
  recaption不属于当前formal evidence gate，也不恢复旧100K队列；任何未来数据修订都必须另建
  版本化合同与人工复审。
- H199与历史双Stage2 cascade保持从投稿核心队列删除。完全独立H/C Stage1 native-system diagnostic
  已完成105K／210K formal audit；用户在exposure复核后另行授权适配后的独立双EncDec Stage2，当前只作
  secondary system boundary；live execution state只见run manifest／logs。它同时改变表示、decoder、参数量、normalization
  与Stage2接口，在endpoint与formal evaluation闭合前不得产生generation结论或回流核心单变量矩阵。
- multi-seed matched repeat已经闭合，不再等待Rect或ViGen utility。
- v10 Camera Stage2、WORLD、swapped-host replay和Camera64 MAE长训均保持关闭；当前获授权的
  C1REL是新建的matched representation arm，不是历史v10/C1队列恢复。
- 组合式H–C utility只作为secondary extension：先完成data／Stage1 support／Human-retention gates，
  再决定是否允许pair-side finetune与后续Camera Stage2；当前不部署editing长训。任一gate失败即留作
  投稿后future work，不写free editing或任意Human／Camera替换能力。

## 6. Canonical owners

- 当前选择、blocker 与行动边界：本页。
- 正式数值、公平对比与 artifact hashes：[[StoryMotion-valid-metric-ledger]]。
- 其余 run identity 与 visual index：[[Storymotion-exp-sha]]。
- evaluator／decoder／指标语义：[[StoryMotion-metric-computation-io]]。
- 版本完成事件与 invalidation：[[version_family]]。
- 两篇论文正式题名、单仓库规则、scope与venue边界：
  [[paper-boundary]]。
- StoryMotion的claim–evidence gap、降级条件与reliability计划：
  [[StoryMotion-iclr-reliability]]；其中拆分前内容不是当前实验授权。
- DIRECT当前状态与全部Paper B owner：[[DIRECT/current|DIRECT current]]。
- Camera temporal editing representation stop：
  [[archived/experiments/2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]。
- Human temporal locality与endpoint headroom：
  [[archived/experiments/2026-07-31_storymotion-v11-human-temporal-locality-control]]。
- v11 原始四臂合同与停止规则：
  [[archived/versions/v11/2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract]]。
