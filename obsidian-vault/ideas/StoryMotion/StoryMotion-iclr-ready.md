---
title: "StoryMotion ICLR 2027 Paper-Ready Claim and Presentation Owner"
status: drafting_evidence_aware
hypothesis: |
  StoryMotion can be presented as a capability-preserving asymmetric Human–Camera
  generator if the paper separates architectural guarantees from empirical effects,
  treats generated-H Camera generation as two-pass composition, and conditions every
  controllability or superiority statement on its own audited evidence gate.
tags:
  - StoryMotion
  - ICLR_2027
  - paper-ready
  - claim-evidence
  - status/active
aliases:
  - StoryMotion-ICLR-Ready
source_notes:
  - "[[StoryMotion/current]]"
  - "[[StoryMotion/StoryMotion-Contributions]]"
  - "[[StoryMotion/StoryMotion-iclr-reliability]]"
  - "[[StoryMotion/StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion/StoryMotion-metric-computation-io]]"
  - "[[StoryMotion/paper-boundary]]"
  - "[[StoryMotion/tasks/0812-1919]]"
created: 2026-08-12T20:50:00+08:00
updated: 2026-08-13T11:14:41+08:00
---

# StoryMotion ICLR 2027 Paper-Ready Claim and Presentation Owner

> [!important] Owner contract
> 本页只拥有 paper-ready claim tree、表述边界、主表／主图 row recipe、caption、limitation、
> failure taxonomy 与 reviewer-answer wording。正式数字、置信区间和 artifact/hash 仍只由
> [[StoryMotion-valid-metric-ledger]] 拥有；claim gate 与完整风险状态仍只由
> [[StoryMotion-iclr-reliability]] 拥有；运行进度只存在各自 `runs/`。

## 1. 一句话问题、标题与非目标

正式标题保持为：

> **StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera Generation**

Paper-facing problem statement：

> Given a strong Human motion generator, can we add Camera generation conditioned on
> observed or model-generated Human motion without allowing Camera inputs or Camera
> supervision to rewrite the Human generation pathway?

方法的概率分解固定为：

$$
p(H,C\mid T_H,T_C)=p_H(H\mid T_H)\,p_C(C\mid H,T_C).
$$

StoryMotion 的主语不是“首次 Human–Camera generation”，而是**在冻结 Human pathway 的条件下增加
有向 Human→Camera 组合能力**。第三个接口是两个条件分布的 two-pass composition，不是同步 joint
sampling，也不是第三个独立 generator。

明确非目标：

- 不主张 arbitrary editing、actor–director co-design、ViGen controller 或 transferable Camera program；
- 不主张 online、causal、streaming 或 real-time；
- 不主张可直接扩展任意 Human backbone 的 model-agnostic framework；
- 不主张 symmetric joint generation 在所有字段都弱于 asymmetric generation；
- 不主张唯一 GT Camera 是 generated-H 条件下唯一正确的 Camera；
- 不把 DIRECT 的数据、program solver 或 dual-frame intent transfer 计入 StoryMotion 贡献。

## 2. Paper-facing 术语

| 内部 immutable mode | 正文名称 | 条件分布 | 论文解释 |
| --- | --- | --- | --- |
| `direct_h` | Human generation | $p_H(H\mid T_H)$ | 被 Camera 扩展精确保留的 Human 基础能力 |
| `direct_c` | Observed-H Camera generation | $p_C(C\mid H_{obs},T_C)$ | Camera 读取 observed Human motion 与 Camera text |
| `sequential` | Generated-H Human–Camera generation | $p_H(H\mid T_H)p_C(C\mid \hat H,T_C)$ | 先生成并固定 Human，再执行 Camera generation 的 two-pass composition |

推荐使用：

- `capability-preserving asymmetric design`；
- `frozen Human generator/pathway`；
- `Camera training does not change the Human pathway`；
- `human-owned, relation-aware representation with an explicit interaction channel`；
- `directed Human→Camera coupling`；
- `two-pass factorized generation`。

禁止使用：

- `disentangled representation`、`three independent generators`、`simultaneous joint sampling`；
- `independent Camera control` 或 `strong controllability`，直到 Camera-text gate 正式闭合；
- `consistent SOTA`、`global asymmetric superiority`、`model-agnostic`；
- `online`、`streaming`、`real-time`、`free editing`。

## 3. 三个 bounded claims

| claim | paper-ready wording | 状态 | 当前边界／失败后降级 |
| --- | --- | --- | --- |
| C1 · capability preservation | StoryMotion adds a Camera pathway while keeping the frozen Human generator and its output path unchanged by Camera inputs and supervision. | supported | 这是架构、合同和 exact replay 共同支持的边界；不改写成“symmetric training 必然损伤 Human” |
| C2 · asymmetric composition | One Camera conditional function supports observed-H Camera generation and generated-H two-pass Human–Camera generation in a single audited system. | supported, bounded | Generated-H 是 OOD condition shift；只主张接口与完整 artifact，不把 sequential 包装成同步 joint primitive |
| C3 · Camera-text response | Camera text provides an auditable, localized response in Camera behavior. | partial formal；claim pending；dropout treatment rejected | shuffled／absent full-cohort cells有效且方向上显示广泛回退，但缺同-evaluator factual correct、contradictory与target-attribute paired audit；这些补齐前只写“Camera text is an input condition” |

C1/C2 的正式结果入口只见
[[StoryMotion-valid-metric-ledger#4.1 C0-LAT competition snapshot (pure4053 formal)]]与
[[StoryMotion-valid-metric-ledger#Audited detail — original §3.11 v11 four-arm `105K` pure4,053 formal audit]]。
C3 的关闭条件只见
[[StoryMotion-iclr-reliability#8.7 `0810-2137` reviewer建议执行审计]]与
[[StoryMotion/tasks/0812-1919#4. P0-B：Camera-text ownership 与 Camera CFG]]；已完成但不足以
关闭claim的两条 intervention cell 只见
[[StoryMotion-valid-metric-ledger#Audited detail — §3.27 C0-LAT Camera-text shuffled／absent pure4,053 formal cells]]。

> [!warning] Representation claim boundary
> H128、I16、C48 及 owning decoders 构成明确的 human-owned relation-aware design，但现有 matched
> controls 是 field-wise mixed Pareto。方法部分可以陈述结构和信息流；结果部分不能由此推出严格
> semantic disentanglement、普遍必要性或所有字段 superiority。

## 4. 核心因果矩阵

| causal axis | changed slot | evidence state | 可进入正文的结论 | 不允许的外推 |
| --- | --- | --- | --- | --- |
| Camera expansion preserves Human | Camera pathway is added after freezing Human | supported | Camera training cannot rewrite the finalized Human pathway；Direct-H exact replay | symmetric learning necessarily damages Human quality |
| Phase-C protection provenance | Camera→Human gradient与Phase-C Human update | audited, mixed；no promotion | 关闭 Camera→Human gradient 而保留 Human update 只产生很小的 mixed effect；进一步冻结 Human 显著损伤 Human reconstruction、同时形成 Camera／framing Pareto | 声称 Stage1 全程冻结 Human、Camera gradient 普遍有害，或把未预注册 margin 的近零结果改写成 non-inferiority |
| Camera-text ownership | correct vs shuffled／contradictory Camera text | partial formal；claim pending | shuffled／absent cells已formal，但只有 frozen Human/noise、同 IDs 的 factual sibling 与 contradictory／target-attribute paired response 闭合后才写 bounded response | 把历史 factual row与新cell冒充matched pair，或用absent／Human-text attribution／旧架构 intervention替代current-mainline ownership evidence |
| Camera-text dropout / CFG | Camera-text dropout `0.10` vs matched no-drop | pure4,053 formal audited；dropout rejected；CFG promotion ineligible | dropout在十个方向性semantic／framing aggregates全部回退，六项geometry CI跨零；保留no-drop | 把neutral scale `1.0`称为CFG、用本结果声称controllability、test-set选scale或事后扫dropout rate |
| Simple Human→Camera composition | integrated StoryMotion vs audited off-the-shelf pair | evidence pending | 只能在接口、数据、decoder 和 runtime 差异完整披露后写 system trade-off | 把不同 native system 当作单变量 architecture ablation |
| Asymmetric vs symmetric route | historical P2、exact-init C0、observed-H G-on/G-off | supported, mixed Pareto | C0-LAT 在投稿优先字段形成优势；route repair 与 G-on 只有局部 effect | all-field asymmetric superiority；Camera gradient necessarily harms Human |
| Interaction16 | C1REL vs matched no-I16，含 two-seed窄复验 | supported, field-bounded | explicit interaction channel 对当前 matched component protocol 有效 | universal necessity、semantic disentanglement、Stage2-only causality |
| No-source cleanup | source identity removed from C0-LAT | supported, non-core | 冗余 implementation variable 可清理 | 双来源匹配能力或自动 mainline promotion |
| Fully independent H/C chain | independent Stage1、decoder、cache、normalizer 与 Stage2 | supported, secondary mixed system boundary | native independent chain 可行但有 semantic–geometry／framing trade-off | cascade、independent representation 或 protected asymmetry superiority |

已有轴的正式证据分别路由到
[[StoryMotion-valid-metric-ledger#Audited detail — original §3.19 True-P2 matched symmetric Stage2 pure4,053 formal]]、
[[StoryMotion-valid-metric-ledger#Audited detail — original §3.22 observed=true symmetric route controls pure4,053 formal]]、
[[StoryMotion-valid-metric-ledger#Audited detail — original §3.20 C1REL-noI16 seed23 full-cohort repeat]]、
[[StoryMotion-valid-metric-ledger#Audited detail — original §3.23 C0-LAT no-source implementation cleanup pure4,053 formal]]和
[[StoryMotion-valid-metric-ledger#Audited detail — original §3.24 fully independent dual-EncDec Stage2 pure4,053 formal]]。
Phase-C 的 A0/A1/A2 训练与 paired causal audit 只见
[[StoryMotion-valid-metric-ledger#Audited detail — §6.5 Phase-C gradient／update protection controls]]。

## 5. Evaluation hierarchy 与主表 recipe

### 5.1 三接口指标层级

| paper-facing interface | primary evidence | secondary／diagnostic | 解释限制 |
| --- | --- | --- | --- |
| Human generation | Human semantic、motion quality、coverage | paired geometry、kinematics、cost | 用于验证 preserved Human capability，不由 Camera 指标替代 |
| Observed-H Camera generation | Camera semantic、framing、Camera geometry | dynamics、physical、cost | observed Human 固定，可对唯一 factual Camera 报告 paired deviation |
| Generated-H Human–Camera generation | Camera-text response、framing/coherence、naturalness、blind audit | 对 dataset Camera 的 geometry deviation、cost | 生成 Human 改变条件，Camera ADE/FDE/rotation 不代表唯一正确轨迹 |

指标定义、decoder 与 I/O 语义只见[[StoryMotion-metric-computation-io]]。

### 5.2 Main Table 1：完整系统行

每行必须有非空 `version / run`，且同一行来自一个完整 checkpoint、decoder、cache、stats、sampler 与
artifact。禁止跨候选拼接最优字段。

建议列组：

| version / run | system role | Human generation | Observed-H Camera | Generated-H pair | resource | assurance boundary |
| --- | --- | --- | --- | --- | --- | --- |
| 待从 ledger 选择 | mainline／external／control | semantic＋quality | semantic＋framing＋geometry | semantic＋framing＋diagnostic geometry | latency＋memory | native／matched／system-boundary |

预留 row recipe：

1. operational C0-LAT；
2. C0-GEO audited objective alternate；
3. mode-compatible external Human／Camera baselines；
4. PulpMotion matched available-data native system boundary；
5. audited simple-composition baseline（pending）；
6. no-drop control只在补充ablation表保留；dropout `0.10`已正式拒绝，不进入主表。

所有数值从[[StoryMotion-valid-metric-ledger#4. Active Stage2 full-cohort evidence]]单向填充；本页不缓存数值。

### 5.3 Main Table 2：claim-changing ablations

| version / run | changed slot | matched fields | Human retention | Camera response／quality | causal conclusion |
| --- | --- | --- | --- | --- | --- |
| A0/A1/A2 Phase-C Stage1 / exact run IDs见ledger §6.5 | Camera→Human `G`；Phase-C Human update `U` | exact Phase-B parent、seed17、data/order、216K×128 exposure、4090 runtime | A1 near-zero mixed；A2 all principal Human errors regress | A1 tiny mixed；A2 Camera geometry improves but projective framing regresses | Stage1仍需Human-loss update；不选择protected owner，不授权downstream |
| matched no-source Camera dropout / `sm_c0_lat_nosource_camtextdrop010_c105k_seed17_5090g2_r2_20260812` vs `sm_c0_lat_nosource_nodrop_c105k_seed17_5090g3_r2_20260812` | Camera-text dropout `0.10` vs `0.00` | parent、seed、order、noise、data、exposure、runtime与neutral scale `1.0` matched | Direct-H tensor-exact | 十个semantic／framing aggregate均回退；六项Camera geometry CI跨零 | reject dropout；不产生CFG／ownership claim |

跨 host 或跨 representation 的 row 必须在 `matched fields` 中写明差异，不进入单变量结论。
C1REL／no-I16 的受限 component evidence 进入本表；P2 route、no-source cleanup、independent H/C
与 Human-text attribution 放入 supplementary root-cause／system-boundary tables，不挤占主表。

## 6. 主图与补充视频 registry

| asset | 主信息 | 状态 | canonical input | caption boundary |
| --- | --- | --- | --- | --- |
| Figure 1 · Problem and interfaces | frozen Human owner、observed-H Camera、generated-H two-pass composition | ready to draw | method contract | 不画 joint-parallel 或 evolving-H |
| Figure 2 · Human-owned asymmetric architecture | H128、I16、C48、owning decoders、Stage2 protected routes | ready to draw | architecture／contract owner | I16是explicit interaction channel，不写disentangled |
| Figure 3 · Quality–coherence evidence | 三接口 field-wise Pareto 与 Human exact replay | schema ready；row selection pending | metric ledger | 不用单一平均分掩盖 mixed Pareto |
| Figure 4 · Camera-text response | correct／shuffle／contradictory 与 rejected dropout pair | shuffled／absent cells audited；matched figure仍pending | ledger §3.27 cells＋audited dropout artifacts＋future matched correct／contradictory | partial render roots无manifest；absent只作OOD辅助项；不画CFG scale curve，不用dropout或历史correct替代ownership证据 |
| Figure 5 · Random and failure cases | random、best/worst、failure strata 的匿名对比 | evidence pending | sealed visual registry | blind audit前不写visual superiority或failure rate |
| Supplementary video | fixed-view Human、GT-H Camera projection、generated-H pair projection、side-by-side | registry pending | runs/vis manifests | 每个片段保留run、mode、ID、text、noise、renderer与source hash |

Caption skeleton：

> **Figure 1. StoryMotion preserves a frozen Human generation pathway while adding one
> Camera conditional function.** The Camera function operates on either observed Human
> motion or a Human sample produced in a first pass. Generated-H Human–Camera generation
> is therefore a two-pass composition rather than synchronous joint sampling.

> **Figure 2. Human-owned asymmetric information flow.** The Human decoder consumes only
> the Human-owned latent, whereas Camera and framing decoding additionally consume the
> explicit interaction and Camera channels. In Stage2, Camera supervision is isolated from
> the finalized Human generator.

## 7. Limitations 与 failure taxonomy

必须进入正文 limitations：

1. **Stage1 provenance。** Finalized Stage2 的 Human freeze 不等价于 Stage1 全程隔离。Phase-C formal
   显示关闭 Camera→Human gradient 的效果很小且mixed，但继续用Human loss更新Human branch仍有明确作用；
   未封存numeric non-inferiority margin，因此A1/A2都不替换现有Stage1 owner。
2. **Generated-H shift。** Camera 在 generated Human 上承受 Human generation error 与 condition shift；
   当前 sequential rotation 偏大，不能由 Direct-C 结果代替。
3. **Camera text。** 原始 Camera caption 的质量、坐标语义、primitive 粒度与组合控制能力有限；current
   Camera-text ownership 仍待正式 intervention。
4. **Mixed symmetric evidence。** Asymmetric／symmetric controls是 field-wise mixed Pareto，不支持
   all-field dominance。
5. **Dataset／backbone scope。** 当前只有一个数据域和一个 Human backbone，不写 model-agnostic。
6. **Offline cost。** 方法为 non-causal、two-pass offline generation；资源 profile 封存前不写实时性。
7. **Metric semantics。** Generated-H 下不存在唯一正确 Camera；相对 factual Camera 的 geometry 只是
   dataset-target deviation。
8. **Baseline covariates。** Native systems可能同时改变 representation、decoder、normalizer、cache、mode
   与 runtime；只支持系统级 trade-off。
9. **Excluded capabilities。** 不支持 arbitrary editing、actor–director co-design、ViGen utility、Camera
   program transfer 或 streaming。

视觉 failure code 预注册：

| code | failure | 可观测定义 | 对应证据 |
| --- | --- | --- | --- |
| F-HUM | Human implausibility | foot sliding、penetration、heading／root drift、action mismatch | fixed-view Human＋physical diagnostics |
| F-FRM | framing failure | subject out-of-frame、scale／screen-position失配、composition break | Camera projection＋framing metrics |
| F-CAM | Camera dynamics failure | jitter、rotation spike、implausible acceleration、path discontinuity | trajectory render＋dynamics diagnostics |
| F-TXT | Camera-text mismatch | primitive、direction、speed、timing与文本不符 | sealed target-attribute intervention |
| F-PAIR | pair incoherence | Camera response与Human事件错位、occlusion或temporal mismatch | generated-H pair projection＋blind audit |
| F-OOD | generated-H shift | Direct-C正常但generated-H pair失败 | paired interface comparison |

## 8. Reviewer Q→evidence→paper location

| reviewer question | short answer boundary | evidence owner | paper location |
| --- | --- | --- | --- |
| Why is this not PulpMotion? | PulpMotion performs symmetric joint modeling；StoryMotion asks how to preserve a frozen Human generator while adding observed-H and generated-H Camera composition. | reliability nearest-work gap | Introduction＋Related Work |
| Is generated-H generation just composition? | Yes；the novelty claim is the capability-preserving asymmetric design and audited interface, not a new synchronous primitive. | method contract＋three-interface artifacts | Method＋Evaluation Protocol |
| Was the Human pathway frozen throughout Stage1? | No；the guarantee begins after the finalized Stage1 owner. A matched Phase-C audit shows that removing Human-loss updates harms Human reconstruction, while removing Camera→Human gradients alone has small mixed effects. | metric ledger §6.5 | Method Training Boundary＋Ablation＋Limitations |
| Why not compose two off-the-shelf models? | This remains an evidence gate；report only after a compatibility-audited system comparison. | simple-composition plan | Main Table 1／Ablation |
| Does Camera text actually control Camera? | Current mainline ownership is pending；do not substitute Human-text attribution or old architectures. | Camera-text intervention plan | Camera-text Analysis |
| Is asymmetry universally better than symmetry? | No；formal controls are mixed Pareto. StoryMotion is prioritized on bounded Camera/system fields and offers an exact Human ownership invariant. | symmetric ledger sections | Ablation＋Limitations |
| Are qualitative examples cherry-picked? | No visual claim before frozen random/best/worst sampling and anonymous failure audit. | sealed visual plan | Qualitative＋Supplement |
| Why use GT Camera metrics for generated Human? | They measure dataset-target deviation, not distance to a unique valid Camera. | metric I/O owner | Metrics＋Limitations |
| Is the method real-time or general across backbones? | Neither is claimed；it is offline, non-causal, two-pass and currently validated on one Human backbone/domain. | resource plan＋scope owner | Limitations |

完整 nearest-work changed-slot 对照只见
[[StoryMotion-iclr-reliability#8.2 Nearest-work gap check]]；这里不复制第二张 competing comparison 表。

## 9. Paper section map

1. **Abstract**：问题、受保护的 Human owner、两个条件算子／三个接口、field-wise 证据与边界；
2. **Introduction**：joint optimization 的 quality–coherence tension、bounded research question、贡献；
3. **Related Work**：Human motion、Camera trajectory、joint Human–Camera generation、conditional composition；
4. **Problem Definition and Interfaces**：两个条件分布、三个接口、Generated-H condition shift；
5. **Method**：Stage1 H128/I16/C48、owning decoders、Stage2 frozen-H Camera、non-causal two-pass inference；
6. **Experimental Setup**：matched available-data cohort、original captions、C0-LAT/C0-GEO、native/adapted
   assurance boundary、完整 `version / run` identity；
7. **Results**：Human retention、Observed-H Camera、Generated-H pair、claim-changing controls、Camera-text/CFG、
   simple composition、visual audit 与 resource profile；
8. **Limitations**：OOD shift、metric semantics、caption、scope、offline cost、baseline covariates；
9. **Reproducibility and Conclusion**：contracts、artifact routing、failure-aware conclusion。

中性、可编译的论文骨架已建立在 `paper/storymotion-iclr/`。当前仓库没有官方 ICLR style，故骨架只用
标准 `article` 验证章节与claim-safe文案；加入官方模板后只替换class/style与conference metadata。
`references.bib` 当前为空，禁止编造citation；正式表格仍须从ledger完整row单向填充。

## 10. Abstract 与 contributions 骨架

### 10.1 Abstract skeleton

> Existing Human–Camera generators commonly optimize both modalities together, which makes
> it difficult to preserve an already strong Human generator when Camera generation is added.
> We present StoryMotion, a capability-preserving asymmetric design that freezes the Human
> generation pathway and learns one Camera conditional function over Human motion and Camera
> text. The resulting system supports Human generation, Camera generation conditioned on
> observed Human motion, and two-pass Human–Camera generation conditioned on a model-generated
> Human sample. Across controlled PulpMotion evaluation protocols, we report field-wise Human,
> Camera, framing, and physical evidence rather than a cross-field aggregate winner. **[Insert
> only formally audited result sentence from the metric ledger after final row selection.]**
> Our analysis identifies both the benefits and the limits of asymmetric composition, including
> generated-H condition shift, mixed symmetric controls, and offline two-pass cost.

### 10.2 Contribution bullets

1. **Supported.** A capability-preserving asymmetric Human–Camera design in which Camera
   training cannot rewrite the finalized Human generator, together with three complementary
   paper-facing evaluation interfaces.
2. **Supported, bounded.** A human-owned relation-aware representation and Stage2-protected
   dual-stream generator that implement directed Human→Camera information flow; no claim of
   Stage1-wide freezing, semantic disentanglement, or universal component necessity is made.
3. **Evidence pending.** An audited Camera-text response study. Shuffled and absent full-cohort
   cells are valid but do not form a matched ownership comparison without a same-evaluator factual
   sibling and contradictory target-response audit. The matched Camera-text dropout intervention is
   rejected and supplies no CFG or controllability claim; if the remaining gate fails, this bullet is removed.
4. **Supported as evaluation practice, not SOTA.** A field-wise evaluation and artifact protocol
   separating Human generation, observed-H Camera generation, and generated-H two-pass
   generation, with explicit uncertainty and metric-semantics boundaries.

## 11. Freeze checklist

- [x] 正式标题、核心问题、三接口名称和 non-goals 已固定；
- [x] 所有当前 claims 均标记 `supported / evidence pending` 并指向 canonical owner；
- [x] 主表／ablation 表 schema 要求每行非空 `version / run` 且禁止跨 endpoint 拼字段；
- [x] 主图 caption 不使用 joint-parallel、disentangled、SOTA 或 visual-superiority 表述；
- [x] limitation 与 failure taxonomy 已建立；
- [x] 中性 LaTeX scaffold 已按八个章节建立并通过两次 `pdflatex` 编译；
- [x] Phase-C A1/A2 pure4,053 formal、paired bootstrap 与 Stage1 provenance claim 已闭合；
- [x] matched Camera-text dropout pure4,053 formal已闭合为negative ablation且不进入主表；
- [ ] Camera-text intervention与simple-composition formal 后冻结 C3 与主表 rows；当前I2只有shuffled／absent有效cells，claim未关闭；
- [ ] 完成3×3 sampler-step grid；当前r4为6/9，禁止选择Pareto cell；
- [ ] sealed resource profile 后填写 latency／memory；当前primary未启动、secondary首case失败，无可填写数字；
- [ ] sealed visual audit 后冻结 Figure 4/5 与 failure-rate wording；
- [ ] 最终 abstract result sentence 只从 metric ledger 的完整 audited row 填入；
- [ ] 最终 reviewer audit 确认没有第二份 metric ledger、DIRECT claim crosswire 或 test-set selection。
