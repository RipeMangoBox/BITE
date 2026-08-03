---
title: "StoryMotion Paper A ICLR Reliability and Closure Contract"
status: in_progress
hypothesis: |
  Paper A检验在冻结Human prior及其输出路径时，非对称Human–Camera扩展能否支持
  Direct-H、Direct-C与sequential composition。当前剩余两项核心科学任务是修正并审计
  Pulp Camera text，以及完成Human-conditioned Independent Conditional Cascade主对照；
  fully-separate variant作为次要system comparison单列。
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
updated: 2026-08-03T17:36:00+08:00
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
- 小样本log-space双簇得到的临时阈值为每个sampled step `0.0022658727 m`与
  `0.1305610°`；它们没有复制TriMotion的`0.02 m / 0.3°`，但仍只属于screen calibration。
- preliminary raw conflict计数为`263 true / 90 false / 159 unknown`，**不能解释成Pulp缺陷率**：
  当前保守parser主要识别static与truck，而临时阈值又让大量轨迹同时出现正反方向symbolic。
  下一步必须先复核随机／高风险样本，补齐Pulp的push-in／pull-out／boom词表，并重新校准phase
  merge与threshold；在此之前不授权全量处理或LLM short／long realization。

## 2. 独立specialist cascade系统对照

> [!failure] 旧任务不满足`0803-1647`主对照
> v7.33的Camera branch是$E_C(C)$／$D_C(z_C)$，不读取Human；旧任务还fresh重训了Human
> Stage2。它只能作为fully-separate native variant，不能冒充要求$E_C(H,C)$／
> $D_C(H,z_C)$且复用同一冻结Human prior的Independent Conditional Cascade。旧run
> `paperA_v11_specialist_native_lat_h105k_c105k_seed17_4090g0_20260803`已停止并标记
> `stopped_contract_mismatch`；停止点和日志保留，不进入正式比较。

主对照与secondary variant必须分开解释。主对照只替换Camera representation与Camera Stage2，
Human prior及其输出owner与StoryMotion相同；fully-separate variant则同时改变Human Stage1／
Stage2与Camera Stage1／Stage2，是完整系统比较。H199 round-trip仍是另一个可选evaluator-only轴。

| arm | Stage1所有权 | Stage2所有权 | Human接口 | Camera训练positive | 允许回答的问题 |
| --- | --- | --- | --- | --- | --- |
| A · StoryMotion C0-LAT | exact v9 H-anchor Pulp-only；H128＋I16＋C48 | protected Human teacher＋Camera endpoint | H128 latent直连 | paired GT-H latent＋原Camera | current reference |
| B · Independent Conditional Cascade | exact v9 Human owner冻结；独立Camera64 $E_C(H,C)$／$D_C(H,z_C)$，不共享Camera representation／decoder／参数 | 复用exact v9 Human teacher；fresh独立Camera Stage2 optimizer／checkpoint | observed H199，或v9 Human输出decode后的固定H199 | factual paired GT-H199＋GT-C；generated-H只在推理时使用 | relation-aware shared representation相对普通Human-conditioned specialist串联是否有质量／成本优势 |
| C · Fully-Separate-Native-LAT | v7.33独立$E_H/D_H$与无条件$E_C(C)/D_C(z_C)$；H128＋C64 | fresh Human specialist＋fresh Camera specialist；独立optimizer／checkpoint | Stage2 Camera读取GT或先生成并固定的H128 | factual paired GT-H latent＋GT-C；不构造generated-H＋原Camera positive | 完全分离系统在同数据与Stage2预算下的native system boundary；不作主对照归因 |

### 2.1 冻结身份与预算

- B固定exact v9 Stage1 Human owner与v9 Human `105K` teacher，不训练任何Human参数；独立
  Camera Stage1采用Camera64、`is_causal=false`、`326,478`个可训练参数，形式为
  $E_C(H_{199},C_{14})$／$D_C(H_{199},z_C)$。其参数量与v7.33 Camera encoder＋decoder的
  `60,224＋266,254=326,478`精确相同。
- B的Camera Stage1固定seed17、batch128、`210K` steps，即`26,880,000`个Camera sample
  exposures；只从factual pair学习Human-yaw-relative Camera。完成后Camera Stage2固定LAT、
  seed17、batch128、`105K`、EMA `0.9999`，并复用exact v9 Human teacher。
- C复用已审计的v7.33 non-causal separate Stage1，不重复其`636K×128`历史训练；checkpoint
  SHA-256为`b8f8ca74748650481cd0901a1476b1580636aaf5fdcd7d4629b223655811aeb4`，
  pure4,053 artifact SHA-256为
  `ca31514032105a84497083983f8d4fc175526cb0900aeea0d4e503a83d9c018d`。
- C fresh训练Human Stage2 `105K×128`与Camera Stage2 `105K×128`；两者分别为独立权重、
  optimizer与逻辑checkpoint。Camera Stage2仍以GT-H latent为训练条件，LAT-only。
- 本轮不把specialist轴与LAT／GEO轴相乘：B和C均只跑LAT。最终表分别报告Stage1／Stage2
  参数、checkpoint数、历史与新增sample exposure、实测GPU小时、峰值显存及三接口p50／p95
  latency；不能把C写成与A／B的单变量parameter-matched ablation。

### 2.2 训练与评测gate

1. B先训练独立Human-conditioned Camera Stage1；构造optimizer前必须通过v9 owner hash、
   Human无梯度、Camera参数`326,478`、non-causal、production batch128、finite decoder与初态hash
   检查。Stage1 endpoint审计通过后才生成Camera cache并授权Camera Stage2 `105K`。
2. C先用v7.33 owner按exact valid length重建train／pure-test cache；optimizer前必须通过
   Stage1 strict load、H／C参数不共享、cache身份、H128＋C64、non-causal、decoder round trip、
   production-shape forward／backward与初态hash检查。
3. B与C均只用真实Pulp pair训练$p_C(C\mid H,T_C)$；不得把generated-H与原GT Camera组成
   positive。generated-H route只做formal sequential推理分布测试。
4. B与C的正式Camera endpoint均固定EMA `105K`，在同一pure4,053上报告Direct-H、Direct-C、
   sequential、official metrics、decoded geometry／physical、10,000次paired bootstrap和盲样本。
5. A对B是Paper A主因果比较；若B质量接近，只能在参数、checkpoint或计算成本实测占优时支持
   StoryMotion interface优势。A对C只作native full-system comparison，不把差异归因于单个模块。

### 2.3 当前执行身份

- B Stage1：`paperA_independent_conditional_camera64_stage1_210k_seed17_4090g1_20260803`；
  无优化器预检已通过，活动训练合同固定`210K`。其后Camera Stage2尚未创建；必须同时等待
  Stage1 endpoint审计与Camera caption选择冻结，不能因GPU空闲自动启动。
- C Stage2：`paperA_fully_separate_native_lat_h105k_c105k_seed17_4090g0_r2_20260803`；
  exact-length cache与无优化器预检已通过，活动训练合同固定Human／Camera各`105K`。它使用当前
  Pulp raw Camera text，只能作为`T_0` raw-caption native-system control；若caption选择不是raw，
  最终caption-matched C仍需从相同初态按胜出文本另训，当前checkpoint不能冒充该结果。
- 首个同名无`r2`的C准备任务因引用合同缺少Human／Camera分栏manifest，在optimizer前失败并保留；
  它没有训练结果。所有run进度与checkpoint只写各自manifest／log，不在vault复制step流水。

### 2.4 可选H199接口消融

`H128 → D_H → H199 → E_H → H128`仍只检验显式Human API round-trip；它不属于本次
B／C训练，也不阻塞Paper A。正文不声称latent接口优越时不执行。

## 3. 投稿闭环矩阵

| 优先级 | 闭环单元 | 当前artifact事实 | 最小剩余动作 | 是否训练 | 关闭后的claim |
| --- | --- | --- | --- | --- | --- |
| P0 scientific core | Pulp Camera文本 | `paperA_pulp_trimotion_geometry_screen_n512_seed17_20260803`已完成512条无LLM screen；gauge／time-reversal自动检查通过；阈值与raw conflict仍是preliminary | 复核随机／高风险样本，校正阈值与parser；再冻结全量symbolic及short／long realization合同 | 否，先审计 | 通过后写版本化factual caption修正 |
| P0 system control | Independent Conditional Cascade | B的Human-conditioned Camera64 Stage1合同与无优化器预检已闭合；Stage1训练活动中，Camera Stage2尚未创建 | Stage1 `210K`审计后训练Camera Stage2 `105K`；三接口pure4,053 formal | 是，Camera Stage1＋Stage2 | 与相同冻结Human prior的普通conditional cascade比较relation-aware interface |
| P0 secondary control | Fully-Separate-Native-LAT | v7.33 Stage1可复用；C的cache与无优化器预检已闭合，Human／Camera Stage2活动中 | 完成两段`105K`及三接口pure4,053 formal | 是，仅Stage2 | 完整H／C分离native system comparison；不作单变量归因 |
| P1 submission | Human保持 | seed17／23 Direct-H共享冻结owner；seed23 replay已过 | 把checkpoint／输出逐元素保持检查固化为公开测试 | 否 | Camera扩展不改变Human owner及输出路径 |
| P1 submission | relation-interface机制 | 结构合同存在；活动ledger没有正式zero／shuffle／route机制表 | 仅在正文需要机制归因时做冻结checkpoint敏感性检查 | 否 | 最多支持接口被使用，不宣称每个Stage1部件必要 |
| P1 submission | 同协议主表 | C0、C3与PulpMotion pure4,053已有正式行；v9仅first-512；TSA／Auteur无活动formal row | 冻结baseline eligibility、split、N、decoder和指标；补可执行且任务匹配的缺行，不可比字段留空 | 原则上评测；未定义实现不长训 | 只作同协议或显式system-boundary比较 |
| P1 submission | Sealed final audit | pure4,053已多次用于开发；seed23复现已闭合 | 冻结方法／指标／prompt taxonomy后，以新sampling seed一次性跑三接口及预注册表 | 否 | 降低selection leakage；不再据sealed结果改模型 |
| P1 submission | 感知与失败披露 | fixed样例存在；随机／最好／最差分层和盲评未闭合 | 冻结cohort与排序规则，完成基础盲评、failure taxonomy、random／best／worst补充材料 | 否 | 视觉可信度与局限；不承担production claim |
| P1 submission | 复现与成本 | contracts、hash和正式artifact齐，但论文包未冻结 | clean revision、环境、命令、三接口evaluator、参数量、GPU小时、p50／p95延迟、显存、table generator和最小demo | 否 | 可复现性与计算成本 |
| P2 optional | H199 interface | C0已是Stage2 specialist decomposition；没有H199 round-trip正式结果 | 只有选择latent-interface优势claim时才做identity guard、pure4,053与paired bootstrap | 否 | 只决定可选接口优势，不决定Paper A主张 |

### 3.1 Caption训练的条件边界

Camera文本修正通过数据审计后，默认只构成数据质量贡献，不自动授权Camera `105K`重训。
只有正文准备主张“geometry-derived caption改善生成”，才需要另冻raw-text／geo-text matched
训练合同、单一objective、预算和决策阈值；没有这项训练时，正文不得写生成增益。

### 3.2 Baseline边界

- C3-25与PulpMotion native的Pulp pure4,053行已经存在，不应重复训练。
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

- Pulp Camera caption修正能否列为数据贡献；由一致性审计和人工抽检决定。
- StoryMotion相对Independent Conditional Cascade是否形成质量、参数或推理成本优势；由B的
  预声明LAT单臂决定。
- fully-separate native system是否构成更强系统边界；由C决定，但不能替代A对B的主因果比较。
- 是否优于公开baseline、是否有主观优势；由同协议主表、sealed audit与盲评决定。

### 4.3 可选、不阻塞主张

- 若正文不声称latent接口优于显式Human API，则无需运行H199 cascade。
- 若正文需要relation／interaction机制归因，再补zero／shuffle／route检查；否则只把Stage1写成
  冻结representation owner，不写component necessity。

### 4.4 当前禁止写入摘要或contribution

- “latent直连优于普通cascade”——除非未来选择并完成H199接口消融。
- “relation-aware shared interface优于Independent Conditional Cascade”——等待B正式结果。
- “StoryMotion优于完全分离系统”——等待C正式结果，且必须注明Human owner与历史Stage1
  exposure也不同。
- “LAT与GEO等价”或“GEO优于LAT”。
- “Stage1每个部件都必要”、全面SOTA、calibrated physical validity或production-ready。
- 同步joint generation、独立双文本控制、editing、Rect、program transfer或ViGen utility。

## 5. 本周初稿与实验冻结顺序

初稿可以立即开始。方法、问题定义、数据边界、现有seed17／23结果和限制可直接成文；数据贡献
和baseline superiority暂留占位符。当前顺序是：

1. 复核无LLM `N=512` Camera geometry screen，冻结Pulp convention、阈值、symbolic schema与
   raw-conflict判定，再授权全量symbolic／语言化；
2. 完成Independent Conditional Cascade的Camera Stage1＋Stage2与formal audit；
3. 完成Fully-Separate-Native-LAT两套Stage2与formal audit，保持secondary system解释；
4. Camera caption审计通过后，按预声明`raw / canonical-short / canonical-short-long`合同决定
   是否训练生成增益三臂；Stage1不重训，`T_2`不获得双倍caption exposure；
5. 冻结同协议baseline表，并按正文实际claim决定是否补matched symmetric joint与最小机制检查；
6. 冻结所有选择后做sealed audit、盲评、失败分层及复现／成本包；
7. H199 evaluator-only审计仅在选择latent-interface优势claim时执行。

当前不进入critical path：H199 round-trip、v10、C1、editing、
Camera MAE、Human locality short screen、joint-parallel和DIRECT实验。

## 6. 历史材料

重构前的完整reliability页与拆分前Actor–Director附录保留在
[[StoryMotion/archived/paper-scope/2026-08-03_storymotion-iclr-reliability-pre-closure-refactor]]。
它只作provenance，不是当前Paper A训练授权。
