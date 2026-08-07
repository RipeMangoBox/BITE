---
title: "StoryMotion ICLR Reliability and Closure Contract"
status: in_progress
hypothesis: |
  StoryMotion检验在冻结Human prior及其输出路径时，非对称Human–Camera扩展能否支持
  Direct-H、Direct-C与sequential composition。NoInt-HREL／C1REL Stage1表示审计已闭合；
  C0-LAT是后续唯一operational mainline。C1REL raw-caption Stage2 endpoint已训练完成；
  C1REL-w/o-Interaction16 raw-T0 matched Stage2已在4090启动。Camera recaption v2已完成
  bounded three-short结构修复，等待calibration与sealed审核。
tags:
  - StoryMotion
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
updated: 2026-08-08T12:00:00+08:00
---

# StoryMotion ICLR Reliability and Closure Contract

> [!important] 唯一live范围
> 本页只拥有StoryMotion的claim–evidence gap、投稿实验优先级、停止条件和降级措辞。
> 正式数字与hash只见[[StoryMotion/StoryMotion-valid-metric-ledger]]；DIRECT状态只见
> [[DIRECT/current]]。拆分前完整方案已归档，不再授权Rect、HumanML3D跨配对、program
> solver、Actor–Director数据、ViGen utility、editing或joint-parallel训练。

## 1. 已冻结的方法与已有证据

$$
p(H,C\mid T_H,T_C)=p_H(H\mid T_H)p_C(C\mid H,T_C).
$$

StoryMotion只报告：

1. Direct-H：$T_H\rightarrow H$；
2. Direct-C：observed $H+T_C\rightarrow C$；
3. sequential composition：先生成并固定$H$，再由同一个Camera branch生成$C$。

当前训练主线已经闭合。v11 C0-LAT与C0-GEO共享exact v9 Pulp-only non-causal Stage1、
owning decoder／cache／train-only stats及冻结v9 Human `105K` teacher，仅Camera objective不同。
seed17与seed23四个Camera endpoint均完成`105K`、Pulp pure4,053三接口、official metrics、
decoded geometry／physical diagnostics和10,000次paired bootstrap。24个Camera geometry差异的
95% CI全部跨零，因此统计结论仍是“没有稳健单一objective胜者”，不能写LAT／GEO等价。
2026-08-04作者基于主表指标优先级与更简洁的latent-flow objective，将C0-LAT指定为后续唯一
operational mainline；C0-GEO保留为audited alternate。该选择不是显著性结论。

### 1.1 Pulp Camera full-train threshold audit

512条`paperA_pulp_trimotion_geometry_screen_n512_seed17_20260803`只保留为历史geometry
screen：其gauge／time-reversal检查通过，但均匀压到21 poses导致step时间跨度随clip变化，双簇
阈值与raw-conflict计数均无calibration资格。其v1 Qwen short／long和零重叠扩展仍是review-only、
noncanonical，不进入训练。

无LLM的`paperA_pulp_camera_threshold_audit_train162760_stride4_seed17_4090cpu_20260804`
已经遍历exact StoryMotion train `162,760／162,760`条轨迹，ordered ID SHA256=
`a0981b6c6223409d656ad8c43cfcf95cae6ec9a28640143b87b6322292c51dc9`。它按25 fps、严格
stride4生成`4,733,272`个step，同时保留两种视图：camera-local
$C_t^{-1}C_{t+4}$与TriMotion-compatible first-frame $C_1^{-1}C_t$。40个signal shards保留
完整六轴rate，后续threshold／duration／hysteresis sweep不需要再次读取Pulp；全程
`llm_calls=0`，约`601.6 s`。

| axis | unit | frame K2 node | frame K3 lower／upper | sample-balanced K3 lower／upper |
| --- | --- | ---: | ---: | ---: |
| truck | m/s | 0.003933 | 0.000628／0.017065 | 0.000671／0.018762 |
| pedestal | m/s | 0.002200 | 0.000396／0.008918 | 0.000424／0.009961 |
| dolly | m/s | 0.007110 | 0.001266／0.023299 | 0.001386／0.025952 |
| tilt | deg/s | 0.185004 | 0.050558／0.584493 | 0.055662／0.663148 |
| pan | deg/s | 0.252447 | 0.062405／0.901127 | 0.068056／1.007560 |
| roll | deg/s | 0.219109 | 0.061450／0.600415 | 0.068658／0.686266 |

表中数字是camera-local、log-space weighted KMeans的cluster-center几何中点，只是候选node。
first-frame对应节点幅值接近，但复合运动的方向符号可以改变，不能据此宣称两个坐标语义等价。
若采用[[StoryMotion/Pulp-camera-recaption-contract]]中的rotation-log定义，当前tilt／pan／roll节点
只保留为Euler-screen，不得直接改名晋升。新版已在4,096样本／118,197 steps上验证
`Euler delta → SO(3) → Log`与原轨迹rotvec的rotation max-abs为
`1.52587890625e-05 deg/s`、translation max-abs为`0.0 m/s`，随后转换全部
`162,760`样本／`4,733,272` steps并重新计算rotvec候选节点；权威contract SHA256=
`a99cfc727dc9e7eada3cbf59bbe1a16869e8bdb39ffdc175b193cd5df49282fa`。
Pulp native translation tags给出的弱监督operating points为truck／pedestal／dolly
`0.023874／0.019765／0.023554 m/s`；原始caption弱锚点为
`0.048327／0.040709／0.052767 m/s`。前者来自Pulp自身translation-only rule，后者又由
motion-tag-to-LLM链生成，均非独立ground truth。合理解释只限于：K3 lower近似数值噪声边界、
K3 upper近似弱／显著运动分界、raw-caption anchor近似caption-worthy强运动候选；最终值尚未冻结。

Pulp native source使用camera-local translation、`25 fps`、`0.02 m/s`、dominance差值
`0.4`、56-frame smoothing和25-frame minimum chunk，且rotation segmentation被注释。
TriMotion pinned commit `5b203a8`则使用first-frame RDF、最多81 frames／stride4、每sampled
step固定`0.02 m／0.3°`与dominant ratio `5`，并逐step输出`Time x%`；它不做四阶段压缩。
因此旧Pulp链的“四阶段summary”是本项目改写，已停止作为canonical结构。v2保留可变长
event intervals，但只把最多3个caption-worthy events及最多2条relations送给Qwen生成三条short；
完整event graph不做两两关系组合。

训练集最长251 frames，对应63 poses／62 stride4 steps；全Pulp目录180,527条的独立扫描同样
最长251 frames。full-train mechanical QC没有触发read／parse、intrinsics shape／frame mismatch或
rotation-quality错误；最大rotation orthogonality与determinant偏差分别为
`9.776571416875157e-07／8.977835164181158e-07`。这只证明文件与矩阵机械完整，不证明方向语义、
caption、threshold、primitive或Human–Camera视觉一致。

原始caption共有19,525个exact unique文本，10,867条进入风险审核池；该池不是错误率。
其中96条有multi-record／prompt contamination，292条有dolly／truck别名冲突，34条混用
truck／pan，207条只有left／right而没有明确primitive，80条含当前translation-only tags不支持的
rotation primitive，41条含zoom／orbit等intrinsics或未支持primitive。另有5,784条left／right
反转或多阶段文本，应保留为合法sequence候选并重点核对顺序。`original_static_*`等parser计数还
受`push-ins／pull-outs`复数词形漏解析影响，只能作为review ordering。

> [!warning] 尚未冻结的标准
> v2已固定camera-local primitive、rotvec与axis-wise detector，不再重开first-frame、Euler或
> winner-take-all dominance轴。在canonical recaption前仍须由512 calibration裁决H0／H1、
> segment salience与sign-consistency；还须确认3-event fact budget、FOV／zoom隔离、CLIP／T5
> checkpoint／pooling／辅助阈值、numeric grouping与人工边界样本协议。
> Web GPT建议的采纳、降级与拒绝，以及最小v2执行gate，统一由
> [[StoryMotion/Pulp-camera-recaption-contract]]拥有。
> exact train rotvec转换、重新计算的候选节点及10万条v2-pre H1 event plan现已闭合；历史Qwen
> 已停。v2结构实现完成不替代H0／H1 calibration、512人工审核、parser gate或sealed 512，
> 候选threshold与语言artifact仍不得进入canonical Stage2。

## 2. `0803-2024`表示因果矩阵

> [!important] 当前优先级
> NoInt-HREL／C1REL Stage1已闭合，C0-LAT仍是默认mainline。作者已根据现有formal
> artifact搁置NoInt-HREL Stage2，并单独授权C1REL raw-`T0` Stage2及
> `C1REL-w/o-Interaction16` Stage1。strict no-I16的广泛退化被作者裁决为Interaction16
> simple-and-effective的正向Stage1 ablation；其raw-`T0` matched Stage2现已启动。WORLD与Matched
> Symmetric不因本次授权进入执行。
> raw-`T0`结果必须与未来canonical Camera text版本分开，不能进入最终caption-matched裁决。

此前的Independent Conditional Camera64与Fully-Separate-Native来自`0803-1647`，不回答本轮
表示问题。前者在审计前已完成`210K`，只保留off-plan HREL-Camera64 diagnostic；后者在约Human
phase `55K`安全停止并保留checkpoint。二者都不进入`0803-2024`主矩阵，也不据此启动Stage2。

| arm | Stage1所有权 | latent／Human接口 | Camera positive | 参数／计算匹配 | 预声明结论 |
| --- | --- | --- | --- | --- | --- |
| A · StoryMotion-HREL | exact v9 Pulp-only owner；owning `D_h/D_c/D_f` | H128＋I16＋C48；official Camera14 relation path | factual GT-H199＋GT-C14 | reference `636K`、batch128、seed17 | current reference；不预设I16必要 |
| B · HREL-w/o-Interaction16 | fresh Stage1；同v9数据、三阶段schedule、loss与exposure | H128＋C48；conditioner／`D_c`／`D_f`输入192→176；Camera48仍读取v9 HREL Camera14 | factual GT-H199＋GT-C14 | `1,273,657`参数；同`636K`、batch128、seed17 | 只回答“显式I16是否必要”；不回答Camera是否依赖Human |
| C · StoryMotion-C1REL | fresh Stage1；同v9数据、三阶段schedule、loss与exposure | H128＋I16＋C48；I16继续读取Human-relative framing，C48输入完整$T_{C1}^{-1}T_{Ct}$；owning decoder恢复首帧锚点 | factual GT-H199＋GT-C14 | `1,480,521`参数，与A exact；同`636K`、batch128、seed17 | 只回答Camera-native motion／Human-relative relation分开表示是否形成稳定Pareto |
| D · C1REL-w/o-Interaction16 | fresh Stage1；相对C只删除I16 | H128＋native C1REL-C48；owning `D_c/D_f`输入192→176 | factual GT-H199＋GT-C14 | `1,273,657`参数；同`636K`、batch128、seed17 | Stage1已支持I16有效性；后续matched Stage2检验generation贡献 |

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
4. C1REL Stage1与v9难分上下，且其坐标表示契合后续Camera text。作者因此授权一条raw-`T0`
   Stage2诊断与D的strict Stage1；这不是C1REL升级事件。D的formal广泛退化支持I16在Stage1
   simple and effective，作者随后授权并启动raw-`T0` matched Stage2，但在结果产生前不写
   generation必要性。
   只有未来canonical caption下同时改善Camera-native adherence并守住Human-relative
   projection／framing，才可讨论替换HREL表示。
5. representation冻结后，才以同一Stage1、latent target、decoder与canonical text训练一个
   Matched Symmetric Joint Stage2；它允许Camera loss影响Human，用于检验protected asymmetric
   factorization，不能与表示变化混在同一run。

### 2.3 当前执行身份

- B：`paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803`；contract SHA256=
  `599faf76f1b019d9d64160cab6e6d3c292a4befb5e1165d4bb54e35979877f66`。4090 GPU0从0 step
  fresh完成`636K`；最终checkpoint SHA256=`968133147d7e1b1202e5bf9ff5e046ae8ff0c592573361821804a1823562ef75`。
- C：`paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803`；contract SHA256=
  `745ff16cc853ce20de6c86690dcc8a9569c2cf4a9a1ce8cb8ab12f959fd0e9c2`。4090 GPU1从0 step
  fresh完成`636K`；最终checkpoint SHA256=`5af7317fcaea0694b457cecf7a106b5ecd26e8acdfbe47a7bd6571cebc0017f0`。
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
- 两条r2均完成exact pure4,053、true-length owning-decoder geometry／framing audit与10,000次paired
  bootstrap。NoInt-HREL在Human基本保持时系统性回退Camera／framing；C1REL守住Human但Camera
  trajectory／rotation回退、projection字段混合，没有形成可晋升的稳定Pareto。完整数字与hash只见
  [[StoryMotion-valid-metric-ledger#6.8 NoInt-HREL／C1REL／C1REL-noI16 matched Stage1 audit]]。
- 原始formal evaluator首次启动因多传`velocity_mean/std`在任何eval artifact写入前fail-closed；失败日志
  保留，修正版重新审计后产生上述唯一正式结果。该实现错误不影响checkpoint或正式artifact。
- C1REL raw-`T0` Stage2：`paperA_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804`；
  exact C1REL Stage1 checkpoint SHA256=`5af7317f…01f0`，新cache按162,760／4,053 ordered
  IDs重建，fresh Human `105K`后冻结，再训练GT-H-only LAT Camera `105K`。
  contract SHA256=`6e58e9aa…337e`，optimizer-free preflight SHA256=`9a75a49d…349`；
  `joint_parallel=false`，generated-H只用于sequential inference。该run已完成总step `210K`，
  Direct-H exact replay max-abs=`0.0`。2026-08-07完成三接口formal评测（seed=17、pure_ set
  4,053 samples、shifted-sigma explicit Euler 50 steps、cfg=1.0、batch_size=128、
  decode_batch_size=1）：
  Direct-H TMR=17.28／FTD=104.33（672s）、Direct-C CLaTr=61.99／FCD=18.18（1,090s）、
  joint_parallel TMR=17.28／FTD=104.33／CLaTr=64.75／FCD=23.20（1,156s）。
  Direct-C joint指标中observed-H TMR=15.65／FTD=7.93。该run绑定旧Pulp Camera caption，
  最终canonical text比较必须另训。
- C1REL-w/o-I16 Stage1：`paperA_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804`；
  latent order为`human128+c1relative_camera48`，只移除I16，contract SHA256=
  `fa0a2d11…f588`。500-step preflight ratio=`0.0249956`、Human invariance max-abs=`0.0`，
  long-run model进入训练前optimizer steps=`0`。该run已完成`636K`及exact pure4,053 formal；相对
  C1REL的Human 5项、Camera／FOV 7项与projective 4项95% CI全部在零上方，Camera ADE为
  `1.501675 m`、rotation为`38.977528°`。该结果正向支持Interaction16对Stage1 owning
  reconstruction／framing的有效贡献。
- C1REL-w/o-I16 raw-`T0` matched Stage2：
  `paperA_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806`；复用上述exact
  C1REL-noI16 Stage1 owner与真实Camera48，重新绑定162,760／4,053 ordered cache、train-only
  full-cov stats、seed17、batch128、Human `105K`＋Camera `105K`和shifted-sigma Euler50。
  `joint_parallel=false`，只评Direct-H、Direct-C与formal sequential。2026-08-07完成三接口
  formal评测（同协议）：
  Direct-H TMR=17.62／FTD=92.03（665s）、Direct-C CLaTr=43.92／FCD=65.43（1,178s）、
  joint_parallel TMR=17.62／FTD=92.04／CLaTr=46.06／FCD=84.30（1,152s）。
  Direct-H产生与C1REL几乎相同的人类动作（同样冻结的v9 Human `105K` teacher，
  TMR 17.62 vs 17.28、jerk 0.016846 vs 0.017046、skate 0.030316 vs 0.030448）；
  Direct-C Camera质量灾难性退化——CLaTr从61.99跌至43.92（−18.07）、FCD从18.18恶化至
  65.43（＋47.25），证明Interaction16对Camera生成是不可或缺的。
- PulpMotion-Repro Stage1：
  当前run为`paperA_pulpmotion_repro162760_stage1_original_seed17_4090g0_r9_20260806`；使用original Pulp
  `162,760` filtered train IDs、native lexicographic order与native Camera＋Human＋projection
  representation，不读取Camera text。r6在`20,150／413,075`因CUDA OOM停止；它只保存model
  state而没有optimizer／scheduler／RNG完整状态，因此不续训。r7／r8从零复现并确认：降低为
  microbatch64×2只能降低瞬时峰值，未使用的Camera FOV／raw-camera／projection raw decode仍让
  live CUDA allocation每optimizer step线性增加约`0.75 MiB`；两条均在再次OOM前主动封存。
  allocation history把六类残留block逐项定位到native `dataset.get_raw()`的上述未使用分支；r9只
  保留六个原loss真正读取的同一个native Human raw-joints decoder，不改变有效batch128、exposure
  或按有效帧数加权的objective。r9 optimizer-free连续16个有效batch的allocated均为
  `70,477,824 bytes`、增长`0 bytes`，训练态step50—300的allocated／reserved也固定为
  `0.097／3.990 GiB`。全量`proj_joints`副本checksum差异为`0`，原生／AE-only loader抽样tensor
  max-abs均为`0.0`，shuffled loader为`1,134.59 samples/s`。2026-08-07完成`413,075` steps
  训练及joint reconstruction formal评测（N=4,053）：Human TMR=15.94／FTD=109.34、
  Camera CLaTr=60.51／FCD=17.68，历时1,915s。Stage2仍被Camera-text gate冻结。

### 2.4 Stage2文本gate

Stage1 formal本身没有测量Camera text adherence或free generation。NoInt-HREL Stage2保持搁置。
C1REL获得一次明确例外：使用旧Pulp Camera caption的raw-`T0`诊断可以训练，但必须绑定caption
版本、split、sample identity与hash，并在canonical three-short text冻结后重训才有最终比较资格。
作者已按D与C共享raw-`T0` caption、exposure、sampler与评测协议启动matched Stage2，并单独记录
参数量／GPU小时。该执行不改变raw-`T0`的diagnostic身份，也不扩张到Matched Symmetric或其他矩阵。

### 2.5 Comparison进度表

> [!note] 三模式与进度快照
> v11三模式固定为Direct-H、Direct-C和sequential Human→Camera；历史C3-25的第三模式是
> joint parallel，不能改名为sequential。Stage1 reconstruction不适用三模式。进度快照时间为
> 2026-08-06 20:33（UTC+8）；未完成行的“结论”按要求留空。

| version / run | stage／比较问题 | Direct-H | Direct-C | 第三模式 | 当前进度 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Stage2 operational reference | formal完成 | formal完成 | sequential formal完成 | seed17／23、pure4,053与bootstrap闭合 | 冻结Human owner下支持三模式；C0-LAT是operational mainline |
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | former-mainline system baseline | formal完成 | formal完成 | joint parallel formal完成；无sequential | pure4,053闭合 | 与v11是representation／sampler／第三模式均不同的system boundary |
| HREL vs C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | Stage1 representation comparison | 不适用 | 不适用 | 不适用 | `636K`＋pure4,053＋bootstrap闭合 | C1REL守住Human但Camera几何回退、projective混合，未形成稳定Pareto |
| C1REL raw-T0 / `paperA_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Stage2 representation diagnostic | formal完成 | formal完成 | joint_parallel formal完成 | Human `105K`＋Camera `105K`训练＋三接口formal完成 | Direct-H TMR=17.28与HREL持平；Direct-C CLaTr=61.99≥PulpMotion；Interaction16对Camera生成关键 |
| PulpMotion-Repro / `paperA_pulpmotion_repro162760_stage1_original_seed17_4090g0_r9_20260806` | Stage1 external-system reproduction | 不适用 | 不适用 | 不适用 | r9 Stage1 `413,075`完成；joint reconstruction formal完成（TMR=15.94／CLaTr=60.51，N=4,053） | PulpMotion joint reconstruction baseline建立；Stage2继续等待canonical text冻结 |
| v8.4-A / 尚未创建run | Stage2 non-AR latent DDPM backbone comparison | 待授权 | 待授权 | 待授权 | 未启动 |  |
| v8.4-B / 尚未创建run | Stage2 adjacent-phase control comparison | 待v8.4-A | 待v8.4-A | 待v8.4-A | blocked on v8.4-A |  |

### 2.6 Ablation进度表

| version / run | stage／消融变量 | Direct-H | Direct-C | 第三模式 | 当前进度 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| C0-GEO vs C0-LAT / seed17＋seed23 `105K` | Stage2 Camera objective | formal完成；两臂共享Human | formal完成 | sequential formal完成 | 两seed、pure4,053与24项geometry CI闭合 | 六组Camera geometry mode-level CI及两seed共24项CI均跨零；没有稳健单一objective胜者 |
| HREL-w/o-I16 / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | Stage1删除I16 | 不适用 | 不适用 | 不适用 | `636K`＋pure4,053＋bootstrap闭合；Stage2关闭 | Human基本保持，Camera／framing系统性回退；只支持Stage1 I16有效性 |
| C1REL-w/o-I16 / `paperA_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | Stage1只删除I16 | 不适用 | 不适用 | 不适用 | `636K`＋pure4,053＋bootstrap闭合 | 所查Human、Camera、FOV与projective 16项CI全部回退；I16对Stage1 reconstruction／framing有效 |
| C1REL-w/o-I16 raw-T0 / `paperA_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | Stage2 matched component ablation | formal完成 | formal完成 | joint_parallel formal完成 | Human `105K`＋Camera `105K`训练＋三接口formal完成 | Direct-H保持（TMR=17.62 vs C1REL 17.28）；Direct-C CLaTr=43.92远低于C1REL 61.99（−18.07），Interaction16对Camera生成有决定性贡献 |
| Matched Symmetric Joint / 尚未创建run | Stage2 protected asymmetric factorization | 待授权 | 待授权 | symmetric joint待授权；不是v11 sequential | 未创建；Camera text冻结期间不启动 |  |
| H199 round-trip / 尚未创建eval run | evaluator-only interface ablation | owner replay待审计 | 不改变Direct-C owner | sequential中插入`D_H→E_H`待审计 | 可选，不训练 |  |
| relation zero／shuffle／route / 尚未创建eval run | evaluator-only mechanism sensitivity | 不适用 | 待正文需要时执行 | sequential待正文需要时执行 | 可选，不训练 |  |

### 2.7 Comparison核心metric表

本表只镜像[[StoryMotion-valid-metric-ledger]]中已审计的headline字段；正式数值、hash与完整字段仍由
ledger唯一拥有。Stage1 framing列为`joint UV L2／paired Out error`，Stage2 framing列为
`r-FPD／Out`。`root jerk／foot skate`只报mean，属于同cohort no-reference heuristic；当前没有
calibrated ground penetration／floating指标，不补造数值。所有生成结果使用Pulp pure-test
`N=4,053`；正在训练或尚未formal的行保持空白。表内不使用train loss。

| version / run | stage／mode | N | H global／root-aligned MPJPE m ↓ | root ADE／FDE m ↓ | Cam ADE／FDE m／rotation deg ↓ | framing ↓ | root jerk／foot skate mean ↓ | status |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| HREL reference / `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726` | Stage1 paired reconstruction | 4,053 | 0.120708／0.042136 | 0.100757／0.248722 | 0.037654／0.043840／0.575890 | 0.160790／0.039550 | 0.027753／0.039454 | formal完成 |
| C1REL / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | Stage1 paired reconstruction | 4,053 | 0.120705／0.042187 | 0.100737／0.248654 | 0.044945／0.057538／0.820222 | 0.157706／0.040497 | 0.027746／0.039503 | formal完成 |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-H | 4,053 | 0.842760／0.228751 | 0.758772／1.283039 |  |  | 0.016892／0.030608 | formal完成 |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C observed-H | 4,053 | 0.125466／0.048796 |  | 1.4125／1.4985／29.922 | 0.8465／0.1052 | 0.027753／0.041858 | formal完成 |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | sequential | 4,053 | 0.842760／0.228751 | 0.758772／1.283039 | 2.9428／3.0422／71.435 | 0.5082／0.0773 | 0.016892／0.030608 | formal完成 |
| v8.1C C3-25 / canonical4053 r2 | Direct-H | 4,053 | 0.845517／0.241475 | 0.753813／1.275453 |  |  | 0.016964／0.031481 | formal完成 |
| v8.1C C3-25 / canonical4053 r2 | Direct-C observed-H | 4,053 |  |  | 1.590954／1.668443／35.2983 | 1.4777／0.1485 |  | formal完成 |
| v8.1C C3-25 / canonical4053 r2 | joint parallel | 4,053 | 0.863815／0.253348 | 0.764885／1.293826 | 2.904159／3.003201／70.8486 | 2.3848／0.1835 | 0.017640／0.032405 | formal完成；非sequential |
| C1REL raw-T0 / `paperA_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Stage2三模式 | 4,053 |  |  |  |  |  | formal完成；见语义表 |
| PulpMotion-Repro / `paperA_pulpmotion_repro162760_stage1_original_seed17_4090g0_r9_20260806` | Stage1 paired reconstruction | 4,053 |  |  |  |  |  | formal完成；见语义表 |

### 2.8 Ablation核心metric表

字段、方向、物理指标边界与上一表一致。C0-LAT／GEO的Direct-H与decoded-Human物理字段逐字段
相同，因此只列产生差异的Direct-C与sequential Camera行；未完成行不填数值。

| version / run | stage／mode | N | H global／root-aligned MPJPE m ↓ | root ADE／FDE m ↓ | Cam ADE／FDE m／rotation deg ↓ | framing ↓ | root jerk／foot skate mean ↓ | status |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C observed-H | 4,053 | 0.125466／0.048796 |  | 1.4125／1.4985／29.922 | 0.8465／0.1052 | 0.027753／0.041858 | formal完成 |
| C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C observed-H | 4,053 | 0.125466／0.048796 |  | 1.3860／1.4711／29.800 | 0.8514／0.1017 | 0.027753／0.041858 | formal完成 |
| C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | sequential | 4,053 | 0.842760／0.228751 | 0.758772／1.283039 | 2.9428／3.0422／71.435 | 0.5082／0.0773 | 0.016892／0.030608 | formal完成 |
| C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential | 4,053 | 0.842760／0.228751 | 0.758772／1.283039 | 2.9368／3.0395／71.507 | 0.5098／0.0768 | 0.016892／0.030608 | formal完成 |
| HREL reference / `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726` | Stage1 paired reconstruction | 4,053 | 0.120708／0.042136 | 0.100757／0.248722 | 0.037654／0.043840／0.575890 | 0.160790／0.039550 | 0.027753／0.039454 | reference |
| HREL-w/o-I16 / `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | Stage1 paired reconstruction | 4,053 | 0.120919／0.042175 | 0.100965／0.249442 | 0.047452／0.067396／0.736642 | 0.180547／0.041164 | 0.027757／0.039482 | formal完成 |
| C1REL reference / `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | Stage1 paired reconstruction | 4,053 | 0.120705／0.042187 | 0.100737／0.248654 | 0.044945／0.057538／0.820222 | 0.157706／0.040497 | 0.027746／0.039503 | reference |
| C1REL-w/o-I16 / `paperA_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | Stage1 paired reconstruction | 4,053 | 0.129549／0.044328 | 0.109197／0.262747 | 1.501675／1.583464／38.977528 | 4.741876／0.306611 | 0.027627／0.039549 | formal完成 |
| C1REL-w/o-I16 raw-T0 / `paperA_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | Stage2三模式 | 4,053 |  |  |  |  |  | formal完成；见语义表 |
| Matched Symmetric Joint / 尚未创建run | Stage2 symmetric joint |  |  |  |  |  |  | 未授权 |

### 2.9 Stage2语义metric表（embedding-based，2026-08-07 formal）

本表提供TMR／FTD（Human语义检索与生成质量）和CLaTr／FCD（Camera文本对齐与分布质量）。
所有评测使用seed=17、pure_ set 4,053 samples、shifted-sigma explicit Euler 50 steps、
cfg_scale=1.0、batch_size=128、decode_batch_size=1。Direct-H列只有Human metric；Direct-C列
只有Camera metric。Direct-C的joint子指标（observed-H）单独标注。
root jerk／foot skate来自decoded human physical diagnostics，均为no-reference heuristic。

**第三模式说明**：v11 C0-LAT使用sequential（先冻结Human owner生成H，再以generated H驱动Camera
branch生成C）。C1REL／C1REL-noI16因evaluate.py实现限制只支持joint_parallel（H与C同时denoising），
与sequential不是同一评测协议。joint_parallel下Human TMR与Direct-H完全一致（共享冻结teacher），
Camera CLaTr因joint denoising可能系统性偏离sequential结果。

| variant | mode | Human TMR ↑ | Human FTD ↓ | Camera CLaTr ↑ | Camera FCD ↓ | root jerk ↓ | foot skate ↓ | elapsed |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| PulpMotion-Repro r9 | Stage1 joint reconstruction | 15.94 | 109.34 | 60.51 | 17.68 | — | — | 1,915s |
| **C0-LAT** (mainline) | Direct-H | 17.61 | 99.39 | — | — | — | — | 2,302s |
| **C0-LAT** (mainline) | Direct-C observed-H | 15.66 (joint) | 7.94 (joint) | 56.93 | 21.17 | — | — | ↑ |
| **C0-LAT** (mainline) | **sequential** | 17.61 | 99.39 | 55.58 | 28.75 | — | — | ↑ |
| C1REL raw-T0 | Direct-H | 17.28 | 104.33 | — | — | 0.017046 | 0.030448 | 672s |
| C1REL raw-T0 | Direct-C observed-H | 15.65 (joint) | 7.93 (joint) | 61.99 | 18.18 | — | — | 1,090s |
| C1REL raw-T0 | joint_parallel ※ | 17.28 | 104.33 | 64.75 | 23.20 | 0.017046 | 0.030448 | 1,156s |
| C1REL-noI16 raw-T0 | Direct-H | 17.62 | 92.03 | — | — | 0.016846 | 0.030316 | 665s |
| C1REL-noI16 raw-T0 | Direct-C observed-H | 15.58 (joint) | 9.83 (joint) | 43.92 | 65.43 | — | — | 1,178s |
| C1REL-noI16 raw-T0 | joint_parallel ※ | 17.62 | 92.04 | 46.06 | 84.30 | 0.016845 | 0.030320 | 1,152s |

> ※ C1REL第三模式实际执行的是joint_parallel（H、C同时denoising），不是v11 C0-LAT的sequential
> （先生成H再生成C）。evaluate.py当前不支持sequential模式。建议在canonical text Stage2前修复
> evaluate.py使其支持sequential，以统一评测协议。

> [!important] Interaction16对Camera生成的决定性贡献
> C1REL Direct-C CLaTr=61.99 vs C1REL-noI16 Direct-C CLaTr=43.92（−18.07）；FCD同时从
> 18.18恶化至65.43（＋47.25）。这是整个消融矩阵中最大的单一效应量。Human Direct-H在两条间
> 几乎一致（TMR 17.28 vs 17.62、jerk 0.017046 vs 0.016846），因为两者共享冻结的v9 Human
> `105K` teacher。该结果将Interaction16从"Stage1 reconstruction有效"升级为
> "Stage2 Camera free generation不可或缺"——在无I16条件下，Camera branch无法从H128＋C48
> latent中恢复camera-native motion。

> [!warning] C0-LAT与C1REL不可直接对比
> C0-LAT使用v9 HREL Stage1（H128+I16+C48、specialist Camera objective），C1REL使用C1REL
> Stage1（H128+I16+C1REL-C48、C1 relative coordinates、LAT Camera objective）。两者Stage1
> latent target定义不同（C48语义不同），Stage2 teacher与optimizer也不同。上表并置仅为方便
> 查阅，不是同协议对比。

## 3. 投稿闭环矩阵

| 优先级 | 闭环单元 | 当前artifact事实 | 最小剩余动作 | 是否训练 | 关闭后的claim |
| --- | --- | --- | --- | --- | --- |
| P0 data | Pulp Camera文本 | full-train rotvec signal与10万条v2-pre H1 event plan已闭合；first-20K定位语言结构失败；v2 bounded fact packet、3-short、count-aware parser、same-gate fallback及CLIP/T5辅助QC实现已通过定向测试 | 生成新v2 artifact；calibration 512冻结H0／H1、salience、3-event预算与encoder阈值；复审6×3并完成sealed 512后才恢复全量语言化 | 当前只需CPU／人工审核；未授权Qwen恢复或模型长训 | 通过calibration与sealed后才写版本化factual caption修正 |
| closed representation | HREL-w/o-I16 | seed17 fresh `636K`、pure4,053 true-length formal与10,000次paired bootstrap闭合；Stage1 Camera／framing系统性回退 | Stage2搁置；不再支付raw或canonical caption长训预算 | 否 | 只支持Stage1 I16 reconstruction贡献；不作generation necessity claim |
| P0 representation | StoryMotion-C1REL raw-`T0` | seed17 Stage1 formal已闭合；raw-caption Stage2已完成fresh Human `105K`＋GT-H LAT Camera `105K`；2026-08-07三接口formal完成：Direct-H TMR=17.28、Direct-C CLaTr=61.99≥PulpMotion 60.51 | 已闭合；只标raw-`T0`，不晋升最终文本版本 | 训练＋评测完成 | C1REL表示在旧caption下支持三接口生成；Camera质量不退化于PulpMotion |
| active component | C1REL-w/o-I16 | strict 176D Stage1 formal已闭合；raw-`T0` matched Stage2已完成Human `105K`＋Camera `105K`训练及三接口formal：Direct-C CLaTr=43.92 vs C1REL 61.99（−18.07） | 已闭合 | 训练＋评测完成 | Interaction16对Stage2 Camera生成不可或缺；从Stage1 reconstruction贡献升级为generation necessity证据 |
| P0 method control | Matched Symmetric Joint | 尚未创建；默认parent已冻结为C0-LAT，必须复用其Stage1、latent target、decoder、数据、exposure与最终canonical text | 先冻结参数／checkpoint／exposure／GPU-hour／inference-cost合同；text恢复前不启动 | 是，仅Stage2；待授权 | protected asymmetric factorization相对symmetric joint denoising的因果价值 |
| P1 external baseline | PulpMotion-Repro-162K | r6在step20,150 CUDA OOM；r7／r8定位并封存未使用raw decode导致的线性live-allocation增长；r9通过16-batch零增长preflight完成`413,075` steps训练；joint reconstruction formal完成（TMR=15.94／CLaTr=60.51） | Stage1 formal已闭合；Stage2继续等待Camera text解冻 | Stage1 r9完成；Stage2冻结 | 外部系统边界；不是StoryMotion组件消融 |
| P1 submission | Human保持 | seed17／23 Direct-H共享冻结owner；seed23 replay已过 | 把checkpoint／输出逐元素保持检查固化为公开测试 | 否 | Camera扩展不改变Human owner及输出路径 |
| P1 submission | relation-interface机制 | 结构合同存在；活动ledger没有正式zero／shuffle／route机制表 | 仅在正文需要机制归因时做冻结checkpoint敏感性检查 | 否 | 最多支持接口被使用，不宣称每个Stage1部件必要 |
| P1 submission | 同协议主表 | C0、C3与PulpMotion pure4,053已有正式行；v9仅first-512；TSA／Auteur无活动formal row | 冻结baseline eligibility、split、N、decoder和指标；补可执行且任务匹配的缺行，不可比字段留空 | 原则上评测；未定义实现不长训 | 只作同协议或显式system-boundary比较 |
| P1 submission | Sealed final audit | pure4,053已多次用于开发；seed23复现已闭合 | 冻结方法／指标／prompt taxonomy后，以新sampling seed一次性跑三接口及预注册表 | 否 | 降低selection leakage；不再据sealed结果改模型 |
| P1 submission | 感知与失败披露 | fixed样例存在；随机／最好／最差分层和盲评未闭合 | 冻结cohort与排序规则，完成基础盲评、failure taxonomy、random／best／worst补充材料 | 否 | 视觉可信度与局限；不承担production claim |
| P1 submission | 复现与成本 | contracts、hash和正式artifact齐，但论文包未冻结 | clean revision、环境、命令、三接口evaluator、参数量、GPU小时、p50／p95延迟、显存、table generator和最小demo | 否 | 可复现性与计算成本 |
| P2 optional | H199 interface | C0已是Stage2 specialist decomposition；没有H199 round-trip正式结果 | 只有选择latent-interface优势claim时才做identity guard、pure4,053与paired bootstrap | 否 | 只决定可选接口优势，不决定StoryMotion主张 |

### 3.1 Caption训练的条件边界

Camera文本修正通过数据审计后，成为后续NoInt／C1REL／Matched Symmetric／PulpMotion reproduction
共享的唯一canonical text输入；它只解锁已预声明的Stage2，不自动扩张矩阵。若正文还准备主张
“geometry-derived caption本身改善生成”，必须另冻raw-text／geo-text matched合同、单一objective、
预算和决策阈值；没有该matched轴时，正文只能写factual caption修正，不能写生成增益。

### 3.2 Baseline边界

- C3-25已有Pulp pure4,053行，不应重复训练。现有PulpMotion native行先审计是否满足exact
  162,760 train identity、split、exposure与owning model；当前`PulpMotion-Repro-162K`只启动text-free
  Stage1，不能把StoryMotion representation移植进去；Stage2继续等待canonical text冻结。
- v9只有first-512，不能伪装成pure4,053 matched row。
- TSA／Auteur只有在输入、输出、数据和指标能对齐且存在可执行artifact时才进入formal表；
  否则只进入related-work任务边界，不为凑表启动未定义长训。
- Uni3C、ActCam与ViGen utility不属于StoryMotion实验门槛。

## 4. Claim冻结表

### 4.1 初稿现在可以写死

- 方法是能力保持式非对称扩展，不是对称joint generator。
- Direct-H复用冻结Human prior；Direct-C与sequential复用同一Camera branch。
- Composition是两个条件分布的顺序组合，`joint_parallel=false`。
- seed17／23不支持稳健的单一LAT／GEO geometry胜者；C0-LAT是后续operational mainline，
  C0-GEO作为audited alternate完整报告。
- StoryMotion只使用Pulp factual Human–Camera pairs；不构造generated-H与原GT Camera positive。

### 4.2 必须等实验再决定

- Pulp Camera caption修正能否列为数据贡献；由自动一致性与完整512条人工审核决定。
- 显式interaction16是否对free generation必要：**已闭合**。C1REL-noI16 Stage2 Direct-C CLaTr=43.92
  相对C1REL 61.99下降18.07点、FCD恶化47.25点，同一冻结Human teacher下Direct-H几乎不变
  （TMR 17.62 vs 17.28）。这是整个消融矩阵中最大的单一效应量，证明Interaction16对Camera
  free generation不可或缺。该结论不依赖canonical text版本，因为raw-T0 matched pair已经
  消除了caption差异。
- HREL还是C1REL作为StoryMotion主表示；raw-`T0`结果不能裁决最终文本版本，C1REL必须在
  canonical text下同时改善Camera control并守住人物构图。
- protected asymmetric factorization是否优于matched symmetric joint；必须在表示与文本冻结后
  用同一Stage1／decoder／target比较。
- 是否优于公开baseline、是否有主观优势；由同协议主表、sealed audit与盲评决定。

### 4.3 可选、不阻塞主张

- 若正文不声称latent接口优于显式Human API，则无需运行H199 cascade。
- `C1REL-w/o-Interaction16`的Stage1＋Stage2审计已形成完整组件证据链：Stage1 reconstruction
  degradation → Stage2 Camera generation collapse（CLaTr −18.07）。不阻塞当前初稿，反而是
  Interaction16必要性的最有力证据。
- 若正文需要更多relation机制归因，再补zero／shuffle／route检查；NoInt目前只支持I16的
  Stage1 reconstruction／framing贡献。

### 4.4 当前禁止写入摘要或contribution

- “latent直连优于普通cascade”——除非未来选择并完成H199接口消融。
- “interaction16对generation必要”——**现已解禁**。C1REL-noI16 matched Stage2 formal已完成，
  Camera CLaTr −18.07／FCD ＋47.25构成决定性证据。但仍须标注”raw-T0 caption下”，
  canonical text版本另需重训确认。
- “C1REL优于HREL”——Stage1没有形成稳定Pareto且不读取文本；当前raw-`T0` Stage2不具备
  最终caption-matched资格，仍需canonical text重训及Camera-native adherence／Human-relative
  framing联合证据。
- “protected asymmetry优于symmetric joint”——等待representation冻结后的matched Stage2。
- “LAT与GEO等价”或“GEO优于LAT”。
- “Stage1每个部件都必要”、全面SOTA、calibrated physical validity或production-ready。
- 同步joint generation、独立双文本控制、editing、Rect、program transfer或ViGen utility。

## 5. 本周初稿与实验冻结顺序

初稿可以立即开始。方法、问题定义、数据边界、现有seed17／23结果和限制可直接成文；数据贡献
和baseline superiority暂留占位符。当前顺序是：

1. C0-LAT保持唯一operational mainline；NoInt-HREL Stage2保持搁置；
2. C1REL raw-`T0` Stage2三接口formal已完成（2026-08-07）；Direct-C CLaTr=61.99≥PulpMotion
   60.51，证明C1REL表示在旧caption下可行但不宣布canonical-text胜者；
3. strict `C1REL-w/o-Interaction16` Stage1＋Stage2 formal已完成（2026-08-07）；Direct-C
   CLaTr=43.92 vs C1REL 61.99（−18.07），构成Interaction16对Camera generation不可或缺的决定性
   证据；可写入初稿但须标注raw-`T0` caption；
4. 历史v2-pre扩写保持暂停；v2结构修复已完成，下一步先生成新CPU artifact并在calibration 512
   确认H0／H1、salience、3-event事实预算和CLIP／T5辅助阈值，再做6×3 paired review；通过后才
   提交是否恢复剩余Qwen队列的新版本合同；
5. 冻结canonical text后重训必要的最小caption-matched Stage2，再以Camera-native adherence与
   Human-relative framing裁决HREL／C1REL；
6. 使用同一canonical text完成获授权representation所需的最小Stage2；Matched Symmetric须另行
   授权，不把表示变化与factorization变化合并；
7. PulpMotion-Repro-162K Stage1 r9已完成（`413,075` steps，joint reconstruction TMR=15.94／CLaTr=60.51）；
   canonical text冻结后再做其Stage2与同协议baseline表；
8. 冻结所有选择后做sealed audit、盲评、失败分层及复现／成本包；
9. H199 evaluator-only审计仅在选择latent-interface优势claim时执行。

当前不进入critical path：旧Independent／Fully-Separate specialist Stage2、H199 round-trip、v10、
WORLD、editing、Camera MAE、Human locality short screen、DIRECT实验。`joint_parallel`对v11 mainline
仍禁用；唯一获准的joint轴是未来单独命名的Matched Symmetric Stage2。

## 6. 历史材料

重构前的完整reliability页与拆分前Actor–Director附录保留在
[[StoryMotion/archived/paper-scope/2026-08-03_storymotion-iclr-reliability-pre-closure-refactor]]。
它只作provenance，不是当前StoryMotion训练授权。

## 7. 2026-08-07 formal后续高优先级实验建议

以下基于2026-08-07完成的7组formal评测。核心发现：C1REL Direct-C CLaTr=61.99；
C1REL-noI16 Direct-C CLaTr=43.92（−18.07），证明Interaction16对Camera生成不可或缺。
**重要**：C1REL第三模式当前是joint_parallel（H／C同时denoising），不是v11 C0-LAT的
sequential（先生成H再驱动C）。evaluate.py需要代码修改才能支持sequential。

### 已完成 vs 未完成的消融全景

| 维度 | 已完成（Stage1） | 已完成（Stage2） | 未完成 |
| --- | --- | --- | --- |
| **表示选择** | HREL (v9)、HREL-noI16、C1REL、C1REL-noI16 | C0-LAT (HREL Stage1)、C0-GEO (HREL Stage1)、C1REL raw-T0、C1REL-noI16 raw-T0 | C1REL canonical text Stage2（P0）；HREL vs C1REL canonical text comparison（P1） |
| **组件消融** | I16删除（HREL／C1REL两臂） | I16删除 matched Stage2（Direct-C −18 CLaTr，已闭合） | — |
| **方法控制** | — | — | Matched Symmetric Joint（P2，Stage2 only） |
| **外部基线** | PulpMotion-Repro r9 | — | PulpMotion Stage2（等canonical text） |
| **评测协议** | — | C0-LAT sequential、C1REL joint_parallel ※ | **C1REL sequential mode**（P0，evaluate.py需修改） |
| **鲁棒性** | — | C0-LAT seed23 | C1REL seed23 replication（P1）；sealed audit（P1） |

### P0 — 投稿前必须完成

| # | 实验 | Stage | 理由 | 阻塞什么claim |
| --- | --- | --- | --- | --- |
| P0-1 | **evaluate.py添加sequential模式** | Stage2 eval | C1REL当前只支持joint_parallel；需要实现先生成H再以generated H驱动Camera branch的sequential路径，与C0-LAT评测协议统一 | C1REL三接口的第三模式定义 |
| P0-2 | **C1REL sequential re-eval** | Stage2 eval | 在P0-1完成后，用已有C1REL checkpoint重新跑direct_h／direct_c／sequential三接口；Direct-H和Direct-C结果不变，只需补sequential | C1REL sequential数字 |
| P0-3 | **C1REL-noI16 sequential re-eval** | Stage2 eval | 同上，补C1REL-noI16的sequential数字 | C1REL-noI16 sequential数字，确认I16 effect在sequential下保持 |
| P0-4 | **Canonical text C1REL Stage2** | Stage2 train+eval | raw-T0结果不能进入最终caption-matched裁决；canonical three-short caption冻结后重训 | "C1REL在最终文本下支持三接口生成" |
| P0-5 | **Canonical text C1REL-noI16 matched Stage2** | Stage2 train+eval | 当前−18 CLaTr效应量在raw-T0下测得；canonical text下复现以排除caption artifact | "Interaction16必要性不依赖caption版本" |

### P1 — 强烈建议

| # | 实验 | Stage | 理由 |
| --- | --- | --- | --- |
| P1-1 | **C1REL vs HREL canonical text comparison** | Stage2 train ×2 | 只有C1REL-noI16 component ablation；HREL vs C1REL representation choice须在canonical text下用同一Stage1 owner裁决 |
| P1-2 | **C1REL seed23 replication** | Stage2 eval | seed17已用于所有开发；seed23复现为sealed audit提供独立采样 |
| P1-3 | **Stage2 geometry metrics提取** | Stage2 eval (CPU) | 从已生成的decoded latent计算MPJPE、ADE、FDE、framing，补齐comparison／ablation核心metric表 |

### P2 — 可选，不阻塞投稿

| # | 实验 | Stage |
| --- | --- | --- |
| P2-1 | Matched Symmetric Joint | Stage2 train |
| P2-2 | C1REL cfg sweep | Stage2 eval |
| P2-3 | H199 round-trip | Stage2 eval |

### 当前最优路径

```
P0-1 evaluate.py sequential支持 → P0-2 + P0-3（并行sequential re-eval，仅GPU时）
canonical text冻结 → P0-4 + P0-5（并行两条Stage2训练）
                  → P1-3（并行提取geometry metrics）
                  → P1-1（若C1REL canonical优于raw-T0，追加HREL comparison）
                  → P1-2（seed23 sealed audit）
                  → 初稿定稿
```

### 远程未提交变更

4090服务器上 `agent/c1rel-stage2-ablation-20260804` 分支有以下未提交修改，必须在任何新实验前
commit或stash：

- `experiments/stage2_protected_h_vimogen/data.py` — `_parse_interaction_dim()`、`C1REL_NOI16_LATENT_ORDER`
- `experiments/stage2_protected_h_vimogen/evaluate.py` — `decode_exact()`动态latent split、source_id、tolerance 5e-4
- `experiments/stage2_protected_h_vimogen/model.py` — `generate_joint()` source_id参数
- `experiments/stage2_protected_h_vimogen/build_cache.py` — C1REL/C1REL-noI16 cache构建支持
- `experiments/stage2_protected_h_vimogen/make_eval_contract.py` — C1REL-noI16 eval contract
- `experiments/stage2_protected_h_vimogen/runner.py` — C1REL-noI16 runner
- `scripts/eval_stage1_pulp_autoencoder_official.py` — PulpMotion r9 eval支持
