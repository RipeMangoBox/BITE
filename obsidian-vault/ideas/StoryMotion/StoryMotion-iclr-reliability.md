---
title: "StoryMotion Paper A ICLR Reliability and Closure Contract"
status: in_progress
hypothesis: |
  Paper A检验在冻结Human prior及其输出路径时，非对称Human–Camera扩展能否支持
  Direct-H、Direct-C与sequential composition。当前先闭环C1REL-derived Pulp Camera text，
  同时按0803-2024完成NoInt-HREL／C1REL Stage1表示对照；表示冻结后才授权对应Stage2与
  Matched Symmetric Joint。
tags:
  - StoryMotion
  - paper/A
  - reliability
  - submission-closure
  - status/active
aliases:
  - StoryMotion-ICLR-Reliability
source_notes:
  - "[[StoryMotion/current]]"
  - "[[StoryMotion/version_family]]"
  - "[[StoryMotion/StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion/StoryMotion-metric-computation-io]]"
  - "[[StoryMotion/paper-boundary]]"
created: 2026-06-18T00:00:00+08:00
updated: 2026-08-03T21:12:00+08:00
---

# StoryMotion Paper A ICLR Reliability and Closure Contract

> [!important] 唯一live范围
> 本页只拥有Paper A的claim–evidence gap、投稿实验优先级、停止条件和降级措辞。
> 正式数字与hash只见[[StoryMotion/StoryMotion-valid-metric-ledger]]；DIRECT状态只见
> [[DIRECT/current]]。拆分前完整方案已归档，不再授权Rect、HumanML3D跨配对、program
> solver、Actor–Director数据、ViGen utility、editing或joint-parallel训练。

## 1. 已冻结的方法与已有证据

$$
p(H,C\mid T_H,T_C)=p_H(H\mid T_H)p_C(C\mid H,T_C).
$$

Paper A只报告：

1. Direct-H：$T_H\rightarrow H$；
2. Direct-C：observed $H+T_C\rightarrow C$；
3. sequential composition：先生成并固定$H$，再由同一个Camera branch生成$C$。

当前训练主线已经闭合。v11 C0-LAT与C0-GEO共享exact v9 Pulp-only non-causal Stage1、
owning decoder／cache／train-only stats及冻结v9 Human `105K` teacher，仅Camera objective不同。
seed17与seed23四个Camera endpoint均完成`105K`、Pulp pure4,053三接口、official metrics、
decoded geometry／physical diagnostics和10,000次paired bootstrap。24个Camera geometry差异的
95% CI全部跨零，因此只能写“没有稳健单一objective胜者”；不能写LAT／GEO等价，也不能选择GEO。

### 1.1 Pulp Camera geometry-only screen

`paperA_pulp_trimotion_geometry_screen_n512_seed17_20260803`从train manifest以
`sha256(seed:sample_id)`确定性选择512条轨迹，全程`llm_calls=0`。Pulp loader把KITTI矩阵作为
C2W，并在projection路径取逆后交给OpenCV camera conversion；screen据此冻结输入标识为
OpenCV right-down-forward，并计算$C_1^{-1}C_t$。每条轨迹最多均匀采样21帧。

- 512／512个随机全局刚体gauge检查通过，relative pose最大绝对误差
  `7.105427357601002e-15`；512／512个固定坐标基的时间反转symbolic代数检查通过。
- 输入rotation最大orthogonality误差为`6.425823300126865e-07`，最大determinant偏差为
  `6.512800068136926e-07`。
- TriMotion官方实现并不从数据估计阈值，而是直接固定每个sampled step `0.02 m`与`0.3°`。
  本screen另外引入log-space双簇heuristic，得到`0.0022658727 m`与`0.1305610°`后再送入
  TriMotion-style axis／dominance分类器；因此这两个数**不是TriMotion阈值逻辑的输出**，也没有
  formal calibration资格。
- preliminary raw conflict计数为`263 true / 90 false / 159 unknown`，**不能解释成Pulp缺陷率**：
  当前保守parser主要识别static与truck，而临时阈值又让大量轨迹同时出现正反方向symbolic。
  当前人工审核批次固定为完整512条；“风险优先／raw conflict／阈值边界”只改变审核顺序，
  不改变cohort。Gradio读取immutable `records.jsonl`与source contract，审核事件另写
  append-only `human_reviews.jsonl`。必须完成512／512，并裁决全部方向／坐标轴错误、拒绝项和
  `无法判断`后，才重新校准phase merge与threshold；在此之前不授权全量处理或LLM short／long
  realization。

## 2. `0803-2024`表示因果矩阵

> [!important] 当前优先级
> `NoInt-HREL → C1REL → freeze representation → Matched Symmetric → PulpMotion-Repro-162K`。
> WORLD不进入正式实验。Stage1不读取文本，可以与512条人工审核并行；任何Stage2必须等待同一版
> C1REL-derived canonical Camera text冻结。

此前的Independent Conditional Camera64与Fully-Separate-Native来自`0803-1647`，不回答本轮
表示问题。前者在审计前已完成`210K`，只保留off-plan HREL-Camera64 diagnostic；后者在约Human
phase `55K`安全停止并保留checkpoint。二者都不进入`0803-2024`主矩阵，也不据此启动Stage2。

| arm | Stage1所有权 | latent／Human接口 | Camera positive | 参数／计算匹配 | 预声明结论 |
| --- | --- | --- | --- | --- | --- |
| A · StoryMotion-HREL | exact v9 Pulp-only owner；owning `D_h/D_c/D_f` | H128＋I16＋C48；official Camera14 relation path | factual GT-H199＋GT-C14 | reference `636K`、batch128、seed17 | current reference；不预设I16必要 |
| B · HREL-w/o-Interaction16 | fresh Stage1；同v9数据、三阶段schedule、loss与exposure | H128＋C48；conditioner／`D_c`／`D_f`输入192→176；Camera48仍读取v9 HREL Camera14 | factual GT-H199＋GT-C14 | `1,273,657`参数；同`636K`、batch128、seed17 | 只回答“显式I16是否必要”；不回答Camera是否依赖Human |
| C · StoryMotion-C1REL | fresh Stage1；同v9数据、三阶段schedule、loss与exposure | H128＋I16＋C48；I16继续读取Human-relative framing，C48输入完整$T_{C1}^{-1}T_{Ct}$；owning decoder恢复首帧锚点 | factual GT-H199＋GT-C14 | `1,480,521`参数，与A exact；同`636K`、batch128、seed17 | 只回答Camera-native motion／Human-relative relation分开表示是否形成稳定Pareto |

### 2.1 表示与锚点所有权

- B是从当前结构删除I16的matched ablation；Camera conditioner和owning Camera／framing decoder
  仍读取H128＋C48。历史v10虽然也是176D，但其Human owner是Phase-A `210K`，与v9 Phase-C
  `636K`不等价，不能替代B。
- C的C1REL使用完整首帧相对平移向量、旋转、相对速度及FOV，不使用标量distance。缓存／生成的
  C48严格等于$E_C(\mathrm{C1REL}_{14})$，发生在任何Human／I16 conditioning之前；逐元素单测为
  exact `rtol=0, atol=0`。I16仍从paired Human199＋v9 Camera14获得人物相对构图信息，conditioner
  只作为owning decoder侧的首帧锚点adapter，不进入Stage2的C48 target。
- C1REL train-only statistics来自exact 162,760条Pulp train、19,336,827个有效帧；artifact
  SHA256=`7ca04cba4ff6efe573060eea8382e4dc097a9d17b1ab874c32c998661ad13564`。
- 所有新实验默认并显式使用seed17、`is_causal=false`、batch128。不得构造generated-H＋原GT-C
  positive；generated-H只在formal sequential推理时使用。

### 2.2 训练与评测gate

1. B／C均固定v9的Pulp-only A `210K`＋B `210K`＋C `216K` schedule、source cycle、optimizer、
   LR、loss、sample exposure与checkpoint schedule；fresh初始化，不复用旧optimizer或模型权重。
2. optimizer前必须通过implementation／data／stats hash、non-causal、Human latent对Camera扰动
   exact invariance、4-sample finite backward、32-sample deterministic replay及500-step one-batch
   overfit；long-run model在preflight后仍为0 step。
3. Stage1先做pure4,053 owning-decoder reconstruction、world／relative geometry与framing audit。
   严重退化可按预声明降低对应Stage2优先级，但不能用中间train loss作论文结论。
4. C1REL只有在Camera-native text adherence改善且Human-relative projection／framing守住时才可升级。
   没有稳定优势则保留HREL；C1REL胜出才条件性补`C1REL-w/o-Interaction16`，不默认做全排列。
5. representation冻结后，才以同一Stage1、latent target、decoder与canonical text训练一个
   Matched Symmetric Joint Stage2；它允许Camera loss影响Human，用于检验protected asymmetric
   factorization，不能与表示变化混在同一run。

### 2.3 当前执行身份

- B：`paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803`；contract SHA256=
  `599faf76f1b019d9d64160cab6e6d3c292a4befb5e1165d4bb54e35979877f66`。preflight通过后在4090
  GPU0从0 step fresh训练。
- C：`paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803`；contract SHA256=
  `745ff16cc853ce20de6c86690dcc8a9569c2cf4a9a1ce8cb8ab12f959fd0e9c2`。preflight通过后在4090
  GPU1从0 step fresh训练。
- 两条preflight的Human invariance与32-sample repeat max-abs均为`0.0`，500-step overfit ratio
  分别为`0.02673799`与`0.02824479`，且没有把preflight optimizer state带入长训。
- 两条合同绑定StoryMotion revision
  `f36bfc230bb23a75e55c08e3f095fee108afc7fd`；B／C preflight artifact SHA256分别为
  `e52207abb05f2186e2a53d4c7a773ec62c5247a4586f4ccb55910fd57799b862`／
  `ac2083ec64aeb551352e4e6767c41f8d3a3a2f28d1d4a2ba46b3afc61178f4b8`。
- 首轮无`r2`任务在TensorBoard step `15,367`停止：NoInt标记
  `stopped_superseded_by_native_c1rel_r2`，C1REL标记
  `stopped_contract_mismatch_c1rel_camera48_conditioned_by_relation`。原因是首版C1REL把C48再次经过
  H128＋I16 conditioner，不满足Camera-native ownership；两条均无required checkpoint，任何模型／
  optimizer state都不复用。共享实现修正后两臂一起从零重启，避免代码版本不匹配。
- 所有有限step、ETA与checkpoint进度只写run manifest／TensorBoard／driver log。本页不复制
  running loss；当前只登记合同与授权状态。

### 2.4 Stage2文本gate

Stage1质量通过不自动授权Stage2。先冻结同一版C1REL-derived canonical short／long text、split、
sample identity与text artifact hash，再按冻结的winning representation决定最小Stage2矩阵。任何使用
raw Camera text的历史run只能标为raw-caption control，不能冒充caption-matched结果。

## 3. 投稿闭环矩阵

| 优先级 | 闭环单元 | 当前artifact事实 | 最小剩余动作 | 是否训练 | 关闭后的claim |
| --- | --- | --- | --- | --- | --- |
| P0 scientific core | Pulp Camera文本 | 固定512条无LLM screen及append-only人工审核界面已存在；自动gauge／time-reversal通过，阈值与raw conflict仍是preliminary | 完成512／512审核与异常裁决，校准阈值／phase／parser；冻结全量symbolic及short／long合同 | 否，先审计 | 通过后写版本化factual caption修正 |
| P0 representation | HREL-w/o-I16 | 176D matched合同与preflight闭合；seed17 `636K` Stage1活动中 | pure4,053 Stage1 gate；canonical text冻结后才决定Stage2 | 是，Stage1＋条件性Stage2 | 显式I16在HREL Camera48存在时是否必要 |
| P0 representation | StoryMotion-C1REL | 192D parameter-matched合同、train-only stats与preflight闭合；seed17 `636K` Stage1活动中 | pure4,053同时检查Camera-native与Human-relative framing；再冻结表示 | 是，Stage1＋条件性Stage2 | Camera-native motion与Human-relative relation分开表示是否形成稳定Pareto |
| P0 method control | Matched Symmetric Joint | 尚未创建；必须复用冻结后的Stage1、latent target、decoder与canonical text | 表示冻结后只训练matched Stage2；允许Camera loss影响Human | 是，仅Stage2 | protected asymmetric factorization相对symmetric joint denoising的因果价值 |
| P1 external baseline | PulpMotion-Repro-162K | 现有native PulpMotion行不能自动视为exact 162,760 reproduction | canonical text冻结后，按PulpMotion own representation／model在相同split、exposure和评测协议复现 | 是，Stage1＋Stage2 | 外部系统边界；不是StoryMotion组件消融 |
| P1 submission | Human保持 | seed17／23 Direct-H共享冻结owner；seed23 replay已过 | 把checkpoint／输出逐元素保持检查固化为公开测试 | 否 | Camera扩展不改变Human owner及输出路径 |
| P1 submission | relation-interface机制 | 结构合同存在；活动ledger没有正式zero／shuffle／route机制表 | 仅在正文需要机制归因时做冻结checkpoint敏感性检查 | 否 | 最多支持接口被使用，不宣称每个Stage1部件必要 |
| P1 submission | 同协议主表 | C0、C3与PulpMotion pure4,053已有正式行；v9仅first-512；TSA／Auteur无活动formal row | 冻结baseline eligibility、split、N、decoder和指标；补可执行且任务匹配的缺行，不可比字段留空 | 原则上评测；未定义实现不长训 | 只作同协议或显式system-boundary比较 |
| P1 submission | Sealed final audit | pure4,053已多次用于开发；seed23复现已闭合 | 冻结方法／指标／prompt taxonomy后，以新sampling seed一次性跑三接口及预注册表 | 否 | 降低selection leakage；不再据sealed结果改模型 |
| P1 submission | 感知与失败披露 | fixed样例存在；随机／最好／最差分层和盲评未闭合 | 冻结cohort与排序规则，完成基础盲评、failure taxonomy、random／best／worst补充材料 | 否 | 视觉可信度与局限；不承担production claim |
| P1 submission | 复现与成本 | contracts、hash和正式artifact齐，但论文包未冻结 | clean revision、环境、命令、三接口evaluator、参数量、GPU小时、p50／p95延迟、显存、table generator和最小demo | 否 | 可复现性与计算成本 |
| P2 optional | H199 interface | C0已是Stage2 specialist decomposition；没有H199 round-trip正式结果 | 只有选择latent-interface优势claim时才做identity guard、pure4,053与paired bootstrap | 否 | 只决定可选接口优势，不决定Paper A主张 |

### 3.1 Caption训练的条件边界

Camera文本修正通过数据审计后，成为后续NoInt／C1REL／Matched Symmetric／PulpMotion reproduction
共享的唯一canonical text输入；它只解锁已预声明的Stage2，不自动扩张矩阵。若正文还准备主张
“geometry-derived caption本身改善生成”，必须另冻raw-text／geo-text matched合同、单一objective、
预算和决策阈值；没有该matched轴时，正文只能写factual caption修正，不能写生成增益。

### 3.2 Baseline边界

- C3-25已有Pulp pure4,053行，不应重复训练。现有PulpMotion native行先审计是否满足exact
  162,760 train identity、split、exposure与owning model；不满足时按`PulpMotion-Repro-162K`
  在canonical text冻结后复现，不能把StoryMotion representation移植进去。
- v9只有first-512，不能伪装成pure4,053 matched row。
- TSA／Auteur只有在输入、输出、数据和指标能对齐且存在可执行artifact时才进入formal表；
  否则只进入related-work任务边界，不为凑表启动未定义长训。
- Uni3C、ActCam与ViGen utility不属于Paper A实验门槛。

## 4. Claim冻结表

### 4.1 初稿现在可以写死

- 方法是能力保持式非对称扩展，不是对称joint generator。
- Direct-H复用冻结Human prior；Direct-C与sequential复用同一Camera branch。
- Composition是两个条件分布的顺序组合，`joint_parallel=false`。
- seed17／23不支持稳健的单一LAT／GEO胜者；两者作为共同mainline报告。
- Paper A只使用Pulp factual Human–Camera pairs；不构造generated-H与原GT Camera positive。

### 4.2 必须等实验再决定

- Pulp Camera caption修正能否列为数据贡献；由自动一致性与完整512条人工审核决定。
- 显式interaction16是否必要；由matched NoInt-HREL Stage1／Stage2决定，结论不得扩大为
  “Camera不依赖Human”。
- HREL还是C1REL作为Paper A主表示；C1REL必须同时改善Camera text control并守住人物构图。
- protected asymmetric factorization是否优于matched symmetric joint；必须在表示与文本冻结后
  用同一Stage1／decoder／target比较。
- 是否优于公开baseline、是否有主观优势；由同协议主表、sealed audit与盲评决定。

### 4.3 可选、不阻塞主张

- 若正文不声称latent接口优于显式Human API，则无需运行H199 cascade。
- `C1REL-w/o-Interaction16`仅在C1REL升级为mainline时触发；否则不做HREL／C1REL全排列。
- 若正文需要更多relation机制归因，再补zero／shuffle／route检查；NoInt本身只支持I16 necessity。

### 4.4 当前禁止写入摘要或contribution

- “latent直连优于普通cascade”——除非未来选择并完成H199接口消融。
- “interaction16必要”——等待NoInt-HREL正式结果；即使通过也不能写成Camera完全依赖Human。
- “C1REL优于HREL”——等待Camera-native与Human-relative framing两类正式证据及稳定性判断。
- “protected asymmetry优于symmetric joint”——等待representation冻结后的matched Stage2。
- “LAT与GEO等价”或“GEO优于LAT”。
- “Stage1每个部件都必要”、全面SOTA、calibrated physical validity或production-ready。
- 同步joint generation、独立双文本控制、editing、Rect、program transfer或ViGen utility。

## 5. 本周初稿与实验冻结顺序

初稿可以立即开始。方法、问题定义、数据边界、现有seed17／23结果和限制可直接成文；数据贡献
和baseline superiority暂留占位符。当前顺序是：

1. 复核无LLM `N=512` Camera geometry screen，冻结Pulp convention、阈值、symbolic schema与
   raw-conflict判定，再授权全量symbolic／语言化；
2. 完成NoInt-HREL与C1REL Stage1 pure4,053 gate；严重退化的臂可降级，不用train loss提前裁决；
3. 以HREL／C1REL的Camera-native adherence与Human-relative framing冻结主表示；仅当C1REL胜出时
   补`C1REL-w/o-Interaction16`；
4. 使用同一canonical text完成winning representation所需的最小Stage2，并训练Matched Symmetric
   Joint；不把表示变化与factorization变化合并；
5. canonical text冻结后并行完成`PulpMotion-Repro-162K`，再冻结同协议baseline表；
6. 冻结所有选择后做sealed audit、盲评、失败分层及复现／成本包；
7. H199 evaluator-only审计仅在选择latent-interface优势claim时执行。

当前不进入critical path：旧Independent／Fully-Separate specialist Stage2、H199 round-trip、v10、
WORLD、editing、Camera MAE、Human locality short screen、DIRECT实验。`joint_parallel`对v11 mainline
仍禁用；唯一获准的joint轴是未来单独命名的Matched Symmetric Stage2。

## 6. 历史材料

重构前的完整reliability页与拆分前Actor–Director附录保留在
[[StoryMotion/archived/paper-scope/2026-08-03_storymotion-iclr-reliability-pre-closure-refactor]]。
它只作provenance，不是当前Paper A训练授权。
