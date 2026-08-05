---
title: "Pulp Camera Geometry-Grounded Recaptioning Contract"
status: v2_event_statistics_screen_complete_pending_calibration
hypothesis: |
  使用冻结的camera-local六轴增量、全训练集候选阈值、轴级事件与共时几何事件归并和确定性句子计划，
  可以在不让LLM决定几何真值的前提下，为Pulp构造三条共享事实的可审核Camera short text。
tags:
  - StoryMotion
  - PulpMotion
  - camera-recaptioning
  - data-contract
  - status/proposed
aliases:
  - Pulp-Camera-Recaption-Contract
source_notes:
  - "[[StoryMotion/StoryMotion-iclr-reliability]]"
  - "[[StoryMotion/StoryMotion_Gradio_Render]]"
  - "[[StoryMotion/paper-boundary]]"
  - "[[StoryMotion/dont_read/0805-0137]]"
  - "[[StoryMotion/dont_read/0805-2009]]"
created: 2026-08-05T01:44:13+08:00
updated: 2026-08-05T20:41:25+08:00
---

# Pulp Camera Geometry-Grounded Recaptioning Contract

> [!important] 当前状态
> 本页评估并收敛`0805-0137`中的Web GPT建议，拥有Pulp Camera recaptioning的算法、
> calibration、语言化与QC合同。全量候选阈值及其artifact只见
> [[StoryMotion/StoryMotion-iclr-reliability#1.1 Pulp Camera full-train threshold audit]]。
> 版本注册现已统一：旧512/Euler/逐采样step阈值及其short／long链称为 **v1**；从exact
> `162,760`条train、`4,733,272`个stride-4 step的rotvec rate signal直接重建H0／H1，再经过
> event budget与区间关系校准的链称为 **v2**。历史run／artifact ID中的`v1p0`不改名；它们是
> v2版本注册前产生的`v2-pre / noncanonical` provenance。first-20K暴露的是v2-pre语言规划器
> 缺陷，不是全量rotvec统计失效。现有`event_plan_v2.py`仍从H1历史event records升级文本包，
> 不能生成H0；因此当前准确状态是“signal与几何基础代码闭合、H0／H1同源重放和event budget
> screen已完成、geometry grouping与Calibration-512待执行”，不是“v2实现完成”。尚未生成新Qwen
> 文本、写回canonical manifest或解锁Stage2训练。

## 0. 版本注册与当前显示裁决

| semantic version | 数值输入与阈值 | 语言输出 | 当前身份 |
| --- | --- | --- | --- |
| v1 | 最多21个均匀采样pose；Euler／逐采样step临时阈值；step时长随clip长度变化 | 一条short＋一条long；旧30K／40K及port `7868`页面 | immutable legacy review-only |
| v2-pre | exact full-train rotvec rate候选节点；H1 provisional event graph | 无界required events、quadratic relations、一条short＋一条long | 历史ID仍含`v1p0`；first-20K后停止 |
| v2 | H0／H1都从同一immutable step signals重建；`axis-present → co-temporal geometry → salient → text`分层；event budget由统计与人工共同选择 | 同一fact packet的3条enriched short；count-aware parser；whole-triplet same-gate fallback；CLIP／T5仅作诊断 | full-train H0／H1 screen完成；event grouping／budget／relation planner待校准 |

因此旧页面中的微幅`dolly out／tilt up／tilt down`主要是 **Gradio仍展示v1 artifact**，不是v2
重新把它们判成显著运动。已核对的9条旧组样本中，v2-pre数值plan有8条不再要求运动文本；唯一
保留的是约`4.15°`的tilt-down，继续作为人工边界样本，不据此事后改阈值。port与页面必须显式
显示semantic version，禁止再用“new”指代版本。

## 1. 目标、边界与最小原则

目标是把factual Camera extrinsics确定性转换为Camera-only文本：truck、pedestal、dolly、
tilt、pan、roll、static、复合运动、方向反转及先后关系。每条样本保留raw caption作为provenance，
但raw caption不作为几何真值，也不进入Qwen输入。

本合同不生成以下内容：

- Human-relative位置、人物构图、shot scale、look-at或Human event binding；这些属于DIRECT；
- orbit；仅凭Camera extrinsics不能唯一确定围绕的目标；
- v2中的zoom／FOV；相关raw属性先标记`raw_attribute_unsupported`并按caption-motion pair隔离；
- 通用Camera captioner claim；当前只是Pulp-specific factual recaptioning与审计；
- generated-H与原Pulp GT Camera positive；文本修正不改变factual配对边。

event统计阶段record固定`camera_attribute_scope=extrinsics6`。含raw zoom的motion仍保留；只隔离
含未支持属性的raw caption监督，不删除motion，也不妨碍从同一extrinsics生成六轴文本。但P7前
必须直接读取intrinsics／FOV序列审计数值变化，不能只搜raw text：显著FOV运动且文本ontology仍
不支持zoom的pair写`camera_attribute_scope=extrinsics6_partial`、
`unsupported_geometry_attributes=[zoom]`与`canonical_stage2_eligible=false`，或在Stage2合同中
明确mask对应FOV target。否则extrinsics stationary但FOV变化的Camera14 target仍会形成text-target
语义冲突。

实现遵循四个最小原则：

1. 几何层保留全部strict-stride信号，不为语言长度改变stride或删step；
2. canonical真值是轴级事件，不是Qwen文本；
3. 只实现能由确定性测试或人工边界审核裁决的规则；
4. 语言化失败时回退deterministic template，不通过重复采样“碰”正确答案。

> [!abstract] v2唯一候选主链
> `C2W → C1REL → body-local translation＋rotvec rates → H0/H1 axis-present intervals →`
> `co-temporal geometry events → segment salience → caption fact packet → deterministic clauses →`
> `three-short realization → count-aware reparse／whole-triplet fallback → CLIP/T5 auxiliary QC`

## 2. Web GPT建议的采纳裁决

| 建议 | 裁决 | v2处理 |
| --- | --- | --- |
| `OFF → PRESENT → CAPTION_SALIENT` | 分层采纳 | 显式区分`axis-present／geometry／salient／text`，并区分strict static、weak motion与captionable motion |
| C1REL保存、body-local增量解释primitive | 采纳 | C1REL用于gauge normalization；primitive来自相邻camera-local transform |
| rotation log替代Euler权威标签 | 采纳 | rotvec生成标签；Euler只作Gradio显示 |
| K3 upper／lower直接冻结hysteresis | 不采纳 | 只形成两套全轴共享公式候选，由512 calibration选择 |
| 持续低速累计运动rescue | 简化采纳 | 只用net amplitude与sign consistency；不引入学习器 |
| detector删除winner-take-all dominance | 采纳 | 六轴独立检测；复合运动不会因弱于主轴而被删除 |
| `0.2／0.6`三档overlap关系 | 不采纳 | 保存精确interval；只派生`overlap／contains／reverses` |
| speed profile与change-point | 暂缓 | v1只记录median／peak rate，不生成accelerating等标签 |
| repeated／alternating等macro ontology | 暂缓 | 可由deterministic planner临时措辞，不进入canonical graph schema |
| FOV／zoom进入v2 | 暂缓 | 先隔离raw zoom；独立intrinsics审计不阻塞六轴闭环 |
| Qwen返回`covered_event_ids` | 仅作日志 | 自报ID不作为证据；独立reparse才是gate |
| 对极端长graph分块再总结 | 不采纳 | 完整数值graph保留；先统计3／4／5／6的最小充分预算，不生成long或二次总结 |
| stride2／stride4 sensitivity | 不采纳 | 用户已冻结stride4；用synthetic短事件测试，不重开stride轴 |
| 1,200 calibration＋1,000 sealed | 缩减 | 512 calibration＋512 sealed；其中20%双人复核 |
| 全量复杂Gradio诊断面板 | 缩减 | video、六轴曲线、interval、文本与审核按钮为必需；3D trail按需显示 |
| H0／H1从同一step signals重放 | 采纳 | 历史100K H1仅作provenance；H0不能从H1 event graph反推 |
| 共时轴事件先合为geometry event | 条件采纳 | 只合并近同步、同阶段的跨轴interval；嵌套的短事件不并入长事件；具体容差由全量分布与calibration冻结 |
| 固定`max_caption_events=3` | 撤回 | 比较3／4／5／6；accepted sample不得遗漏任何salient geometry event，overflow隔离而非静默top-K |
| 区间感知`then／overlap／during／reverses` | 采纳 | 只对有界selected events即时计算，Qwen读取确定性clauses，不自行推断interval |
| CLIP／T5作为P7 gate | 不采纳 | 先测direction-flip等诊断判别力；无效即删除该分数，不阻断canonical发布 |
| FOV／zoom只靠raw关键词隔离 | 不采纳 | P7前补geometry-based intrinsics audit；当前事件统计仍只处理extrinsics6 |

### 2.1 明确拒绝的过度复杂化

v2不实现通用change-point clustering、学习式置信度、每轴独立超参数搜索、复杂父子macro节点、
二次LLM总结或VLM视频判定。这些模块会增加新的阈值与不可验证分支，却不是修正Pulp Camera文本
的必要条件。

Web GPT提出的通用time-reversal测试也需要收窄。camera-local frame会随Camera旋转；一般轨迹
反放后，增量应是带frame change的逆变换，不能简单要求六个符号逐项取反。v2只对纯轴synthetic
轨迹检查方向反转，对一般轨迹检查SE(3)逆变换恒等式，不写错误的全局symbolic flip gate。

## 3. 冻结输入与几何定义

阈值只拟合exact StoryMotion train `162,760`条；pure-test和后续sealed cohort不参与拟合。
输入为KITTI row-major C2W，Camera约定为OpenCV right-down-forward。固定：

```text
fps = 25
stride = 4
delta_t = 0.16 s
maximum sampled poses = 63
maximum adjacent steps = 62
```

首帧归一化轨迹为：

$$
\widetilde T_t=T_0^{-1}T_t.
$$

相邻body-local增量为：

$$
\Delta T_t
=\widetilde T_t^{-1}\widetilde T_{t+1}
=T_t^{-1}T_{t+1}
=
\begin{bmatrix}
\Delta R_t & \Delta p_t\\
0 & 1
\end{bmatrix}.
$$

六轴rate定义为：

$$
v_t=\frac{\Delta p_t}{0.16},
\qquad
\omega_t=\frac{\operatorname{Log}(\Delta R_t)^\vee}{0.16}.
$$

translation单位为m/s；rotation实现内部使用rad/s，写artifact与展示时转换为deg/s。六个正负
方向名称不从Web GPT文字直接继承，必须由12条纯轴synthetic tests冻结后写入convention ID。

> [!important] rotvec权威signal已闭合
> 旧full-train shards保存的是同一camera-local增量旋转的Euler `xyz` rate，而不是被阈值删除后的
> labels。首个4,096样本／118,197 steps同时从原轨迹直接计算rotvec，并与
> `Euler delta → SO(3) → Log`确定性转换逐项比较：translation max-abs为`0.0 m/s`，rotation
> max-abs为`1.52587890625e-05 deg/s`、p99为`4.76837158203125e-07 deg/s`，通过预声明
> `2e-05 deg/s`容差。原轨迹全量重读因此以`stopped_superseded_by_audited_euler_to_rotvec_shard_conversion`
> 关闭；随后从immutable父shards转换exact `162,760`样本／`4,733,272` steps并重新计算rotvec
> K3节点。转换不复用旧Euler rotation阈值，也不产生LLM调用。

> [!note] C1REL与primitive并不冲突
> C1REL负责移除任意world gauge；camera-local increment负责在Camera自身当下坐标轴中解释
> truck／pedestal／dolly与body-axis rotation。首帧固定坐标差分只保留为sensitivity字段，
> 不再生成canonical primitive。

## 4. 最小事件抽取规则

### 4.1 阈值符号与唯一候选矩阵

对每个轴$a$，权威signal artifact提供：

- $L_a$：full-train rotvec K3 lower，作为noise floor；
- $U_a$：full-train rotvec K3 upper，作为event enter中心；
- $R_a$：raw-text translation anchor，只用于salience sampling，不作真值；rotation没有$R_a$。

frame-weighted camera-local节点为主，sample-balanced节点只做稳定性检查。v2只比较两套
hysteresis公式，不做每轴网格搜索：

| candidate | $T_{enter,a}$ | $T_{exit,a}$ | 用途 |
| --- | ---: | ---: | --- |
| H0 | $U_a$ | $\sqrt{L_aU_a}$ | Web GPT建议的较宽hysteresis |
| H1 | $U_a$ | $0.5U_a$ | 更保守地切开静止gap |

所有轴共用同一公式身份；calibration只能选择H0或H1，不能为六个轴分别挑更好看的组合。

### 4.2 Axis-wise interval detector

每个轴和符号独立运行：

1. 连续2 steps达到$T_{enter,a}$才启动event；
2. 连续2 steps低于$T_{exit,a}$才结束event；
3. 同轴、同方向、间隔不超过1 step且gap中没有可信反向运动时合并；
4. 相反方向不合并，保留两个event并派生`reverses`；
5. 六轴不做winner-take-all或ratio=5过滤。

这三项时间常数固定为`2 enter／2 exit／1 gap`，只允许在512 calibration整体失败时重开，
不得边看全量caption边逐轴微调。

### 4.3 Salience与持续低速rescue

H0与H1必须分别从同一份immutable per-step signal shards重建，不能读取或升级历史H1 event
records来产生H0。两套候选分别输出完整的axis intervals，再分别计算全训练集segment-level分布：
duration、median rate、net amplitude、path amplitude与sign consistency。该统计不重读Pulp原始
trajectory，不调用LLM，也不选择最终rule。

v2固定区分四层集合：

```text
E_axis_present  = 通过H0或H1 hysteresis的带符号轴级interval
G_geom          = 由近同步、同阶段跨轴interval组成的geometry event
G_salient       = 通过segment salience的geometry event
G_text          = 被完整写入caption fact packet的salient geometry event
```

必须满足`G_text ⊆ G_salient ⊆ G_geom`，而`G_geom`可追溯到`E_axis_present`。状态另行冻结为：

- `strict_static`：`E_axis_present`为空；
- `weak_motion_only`：存在axis-present event，但`G_salient`为空；
- `captionable_motion`：`G_salient`非空；
- `caption_budget_exceeded`：存在salient geometry event，但当前文本预算无法完整覆盖。

只有`strict_static`可生成stationary。`weak_motion_only`不能因“未入选文本”被重标stationary；在
Calibration-512裁决前保留为abstain。`caption_budget_exceeded`同样隔离，不允许静默top-K。

salience只允许以下两条路径：

1. event的median rate越过segment-level显著节点，且持续至少3 steps；
2. 持续低速event的net amplitude越过segment-level显著节点，且sign consistency通过
   calibration阈值。

sign consistency只采用一个确定性定义：

$$
\kappa_e=
\frac{\left|\sum_{t\in e}\Delta x_t\right|}
{\sum_{t\in e}|\Delta x_t|+\epsilon}.
$$

$\kappa_e$接近1表示运动方向稳定，接近0表示来回抵消；不再额外训练置信度模型。

segment-level节点先由全训练集log-K3产生，再由512 calibration裁决。raw-text anchor只用于抽取
边界样本和检查caption提及习惯，不能选择阈值。v2不引入手写的`0.8 s`、`0.8 monotonicity`或
`0.75／1.0／1.25 × raw anchor`多重网格。

跨轴排序使用无量纲score，不能直接比较m/s与deg/s：

$$
s_e=\max\left(
\frac{\operatorname{median\_rate}_e}{S^{\mathrm{rate}}_a},
\mathbf 1[\kappa_e\ge S^{\kappa}_a]
\frac{\operatorname{net\_amplitude}_e}{S^{\mathrm{amp}}_a}
\right),
$$

其中$S^{\mathrm{rate}}_a／S^{\mathrm{amp}}_a／S^{\kappa}_a$分别来自所选H候选的full-train
segment节点，与4.1只作抽样锚点的raw-text $R_a$不同；duration、start time与稳定
`event_id`只作tie-break。历史字段`must_preserve`保留为immutable provenance，但v2不沿用，也不
新建一个同义的“required”布尔值。只有salient geometry events进入文本；`reverses`只在两个
salient同轴反向event间成立。若人工认为某个反向partner必须写、rule却判为非salient，应在
Calibration-512调整全局salience合同，而不是用sample级例外把非salient尾部塞进文本。

### 4.4 Geometry grouping与数据驱动的caption budget

不同轴且开始／结束边界接近、属于同一连续时间阶段的axis intervals可组成一个compound geometry
event，例如同步truck＋pan。下列情况禁止合并：

- 同轴同方向event：由axis detector的gap规则决定是否合并，不由跨轴grouping处理；
- 长event内部嵌套的短event：两者保持独立，以便表达`during`；
- 只有部分重叠但不属于同一阶段的event：保留`overlap`关系，不强行合成compound。

开始／结束容差及“同一阶段”的数值定义尚未冻结。先报告跨轴interval的start delta、end delta、
overlap与containment分布，再在Calibration-512上检验候选；禁止仅为降低event count而放宽合并。

预算校准必须同时报告：

```text
K_axis     = axis-present interval数
K_geom     = co-temporal grouping后的geometry event数
K_salient  = salient geometry event数
K_text     = caption fact packet中的geometry event数
```

比较`max_caption_events ∈ {3, 4, 5, 6}`。选择最小充分预算时，同时报告全量覆盖率、按长度／
compound／reversal分层的overflow率，以及人工可读性；数值门槛在首个full-train screen之后、人工
calibration之前一次性冻结。任何进入canonical dataset的sample必须满足：

```text
K_text = K_salient
all_direct_reversals_selected = true
```

超出预算的复杂尾部写`caption_budget_exceeded`并隔离，不允许以top-K形式留下未写入的salient
target variation。历史`max_caption_events=3`与primary／reversal／overlap selector只作为v2-pre
风险screen，不再是v2合同。

## 5. 最小v2 event与relation schema

canonical graph只保存atomic axis events，不保存易膨胀的语言宏节点：

```json
{
  "convention_id": "pulp_c2w_rdf_body_local_rotvec_stride4_v1",
  "axis_events": [
    {
      "event_id": "e0",
      "primitive": "dolly",
      "direction": "in",
      "start_step": 8,
      "end_step": 19,
      "duration_s": 1.92,
      "median_rate": 0.061,
      "peak_rate": 0.084,
      "rate_unit": "m/s",
      "net_amplitude": 0.118,
      "path_amplitude": 0.123,
      "amplitude_unit": "m",
      "salient": true
    },
    {
      "event_id": "e1",
      "primitive": "pan",
      "direction": "right",
      "start_step": 12,
      "end_step": 17,
      "duration_s": 0.96,
      "median_rate": 1.04,
      "peak_rate": 1.31,
      "rate_unit": "deg/s",
      "net_amplitude": 1.00,
      "path_amplitude": 1.02,
      "amplitude_unit": "deg",
      "salient": true
    }
  ],
  "geometry_events": [
    {
      "event_id": "g0",
      "axis_event_ids": ["e0"],
      "salient": true
    },
    {
      "event_id": "g1",
      "axis_event_ids": ["e1"],
      "salient": true
    }
  ],
  "caption_fact_packet": {
    "selected_geometry_event_ids": ["g0", "g1"],
    "max_caption_events": "pending_full_train_budget_selection",
    "deterministic_clauses": [
      {
        "source": "g0",
        "target": "g1",
        "type": "during"
      }
    ]
  }
}
```

示例为简写；正式record还要保存`axis_event_ids`以从`g*`追溯到`e*`。完整atomic graph不物化
任意两两relation；interval本身已足够复核。只有最终有界的selected geometry events在
deterministic planner中即时计算必要关系。即使预算为6，两两候选也至多15对，不需要为了避免
全图$O(N^2)$而把文本关系压成一条线性链。最小关系集合为：

- `then`：前一event结束后，后一event再发生；
- `overlap`：两个event部分重叠，且互不包含；
- `during`：短event完整发生在长event期间；
- `reverses`：同轴、反向且直接或近直接衔接。

`reverses`的最大gap尚需从direct-transition分布与Calibration-512冻结；超过该gap时只表达
`then`与后续相反方向，不能写成直接反转。`during`保留长dolly中先后两段pan等嵌套事实，避免
旧线性链漏掉第二段pan仍位于dolly期间。planner把interval确定性转换成clauses；Qwen读取clauses，
不读取raw interval，也不自行决定几何关系。`repeats／alternates／accelerates`暂不进入ontology。

### 5.1 最长62 steps的处理

压缩发生在event层，不改stride：

stride-4后最长为62 steps。完整event抽取仍按同轴短gap、方向与interval运行，不裁剪输入；语言
输入只包含有界fact packet，因此不再存在long prompt token超额，也不按长序列分块。QC按
`N_step／K_axis／K_geom／K_salient／K_text`分层报告，用来检测阈值或grouping是否在长样本上
放大噪声，而不是用全图pairwise relations增加文本容量。

## 6. Deterministic plan与Qwen边界

### 6.1 三条short的唯一语义身份

每条样本目标输出`camera_text_enriched_shorts[3]`。三条读取完全相同的geometry event IDs与
deterministic clauses；不设置
“主动作版／时序版／复合版”等角色，不允许某一条独有`start／midway／late`、幅度、速度或构图
强调。差异只允许同义动词／名词、主动或名词化句法、以及表达同一必要关系的连接词。v2不设置
任意embedding距离或最小改写幅度；只拒绝大小写、空白与标点归一化后的完全重复。三条都必须独立
通过同一个count-aware fact gate；若Qwen triplet失败，整组回退为三条同事实、非完全重复的
deterministic templates。训练如何抽取三条在Stage2合同中另行冻结。

三类对象不得混名：

- `camera_motion_axis_events`与`camera_motion_geometry_events`是可追溯数值事实；
- `caption_fact_packet`与`camera_text_canonical_template`是确定性语言合同；
- `camera_text_enriched_shorts[3]`是Qwen受约束的表述增强，不是新的几何标签。

### 6.2 Qwen输入与输出

Qwen只接收最终预算内的bounded fact packet与deterministic clauses，例如：

```json
{
  "events": [
    {"event_id": "g0", "primitive": "pan", "direction": "right"},
    {"event_id": "g1", "primitive": "pan", "direction": "left"}
  ],
  "deterministic_clauses": [
    {"source": "g0", "target": "g1", "type": "reverses", "text": "pan right, then directly reverse to pan left"}
  ]
}
```

Qwen不接收raw Pulp text、video、Human、逐step数值或阈值解释。单次返回3个short；不做
best-of-N或逐条反复重采样。三条不能被prompt分配不同语义侧重。

### 6.3 Independent reparse与fallback

闭集parser以`Counter`保留重复primitive-direction实例，并按文本位置分配给有序event IDs；不再
用set折叠`right → left → right`。任一short缺实例、增加实例、方向相反或关系错误，整个triplet
回退为三条deterministic short。回退triplet必须重新通过同一个fact与三句非重复gate：

```text
qwen_status = rejected_reparse
camera_text_enriched_shorts = revalidated_deterministic_triplet
```

parser必须先补齐单复数、连字符及闭集Camera词形fixture。Qwen的流畅度不能覆盖几何失败，
Qwen自报coverage也不能替代reparse。

### 6.4 CLIP／T5辅助验证

闭集parser仍是hard fact gate。CLIP与T5分别计算：三条short对canonical fact anchor的相似度、
相对方向翻转hard negative的margin，以及三条caption的两两相似度。前两项筛查语义／方向，后一项
只检查是否近重复；不能用“彼此不相似”替代事实正确。两个encoder独立报告，不按其中一个挑文本，
以免污染后续CLIP／T5训练对比。先在direction flip、unplanned event与paraphrase duplicate的
受控集合上报告AUC／排序准确率；若encoder对某项没有可靠判别力，就删除该项阈值，只保留日志。
exact checkpoint与T5 pooling仍需冻结，但CLIP／T5不作为P7 blocker，也不替代parser与人工sealed
审核。

## 7. QC合同

### 7.1 Mechanical QC

沿用现有全量审计：文件／矩阵可读、trajectory结构、cam segment范围、intrinsics shape／frame
对齐、rotation正交性与determinant。它不承担语义正确性。

### 7.2 Geometric-semantic QC

optimizer-free测试至少包含：

1. 12条正负纯轴trajectory：六轴primitive与方向逐项正确；
2. static、单step spike、短gap、compound、reversal synthetic fixtures；
3. 任意global SE(3)左乘后event graph exact不变；
4. C1REL首帧为identity；
5. body-local increments重新积分后恢复C1REL，误差低于预声明浮点容差；
6. 一般轨迹反放满足frame-aware inverse identity；纯轴fixture才检查符号反转；
7. 相同输入重复运行的event graph与deterministic text byte-identical；
8. Qwen reparse fixture覆盖primitive、方向、先后、overlap、reversal与禁止属性。
9. 方向还需独立projection sanity：pan right时光轴与固定world point的图像运动相符；truck right时
   Camera center沿当下camera-local `+x`移动。该测试与12条生成fixture互相独立，避免实现与测试共享
   同一个错误符号表。

任何synthetic符号错误、gauge失败或round-trip失败都阻断calibration，不能靠人工审核豁免。

## 8. 人工calibration与sealed audit

### 8.1 Calibration 512

从train构造一次性512 cohort：

| stratum | 数量 | 目的 |
| --- | ---: | --- |
| uniform random | 192 | 防止只优化风险样本 |
| threshold／duration boundary | 192 | 12个signed primitives各16条，覆盖enter／exit／duration／amplitude rescue |
| compound／overlap | 64 | 检查多轴保留与语言关系 |
| reversal | 32 | 检查方向与顺序 |
| raw-text conflict／contamination | 32 | 第二阶段冲突分类 |

各stratum内部覆盖六轴、正负方向、长度bin与最长序列。Calibration与sealed按parent source video
及near-duplicate cluster分组隔离，不能只保证sample ID不重合。P2第一轮隐藏raw text，只看
human＋ground＋camera video、六轴曲线和event intervals；P4语言pilot才进行第二轮，显示
raw／deterministic／Qwen文本，减少raw text anchoring。随机选104条双人复核。

calibration只允许作出：H0或H1、segment salience节点、sign consistency阈值、co-temporal grouping
容差、direct-reversal gap、全局event budget与sentence plan是否通过。所有候选必须在展示人工结果
前由full-train screen列出；不得扩张新primitive、逐轴微调规则或逐sample补丁。
H0／H1比较报告event precision／recall、false split、false merge与按长度bin的event inflation；人工
标签允许`absent／present-not-salient／salient／uncertain`，不能把`uncertain`强制算成任一候选正确。

### 8.2 Sealed 512

规则、parser与prompt冻结后另选512条：256 uniform random＋256 risk-stratified。sealed结果不再
反向调阈值。第一遍隐藏H0／H1身份、event色块与候选文本，只依据render、Camera frustum／静态网格
和六轴曲线独立标注`absent／present-not-salient／salient／uncertain`及primitive／direction；第二遍
再显示rule与文本，减少候选锚定。最低gate：

- primitive／direction人工正确率不低于95%；
- then／overlap／during／reversal关系正确率不低于90%；
- 三条short各自的caption-packet event-instance recall为100%，hallucinated primitive为0；
- 人工`可直接作为训练文本`通过率不低于90%。

同时报告salient-event precision／recall、direction accuracy、relation accuracy、usable coverage与
95% CI；上述point gates保持现有最低标准，CI lower bound先报告而不在看到sealed结果后追加为新
门槛。`uncertain`作为abstention单独计数，不混入正确样本分母。

任一gate失败时不生成canonical全量版本；可以保留deterministic artifact与失败taxonomy，但不能
把Pulp directional inconsistency或下游改善写成已证实claim。

### 8.3 Numeric grouping与Gradio最小显示

相似组三条不按Qwen text聚类。先固定primary primitive、direction与length bin，再按duration、
median rate、net amplitude和event count的标准化距离选择anchor的两个最近邻。不得把阈值两侧
样本混成“相似”组。

Gradio必需显示：

- human＋ground＋camera高质量压缩video，三条同步播放；
- 六轴rate曲线、$T_{enter}/T_{exit}$和event interval色块；
- v1历史short／long只在对比页显示；v2显示deterministic三条short与Qwen三条short；
- CLIP／T5的fact-anchor、direction-margin和caption-pairwise辅助分数；
- 第二阶段才显示Pulp original Camera text与reason codes；
- `合格／不合格／无法判断`、不合格sample多选、description及`下一组`。

3D trail、RDF axes与完整数值表默认折叠，只在坐标／方向失败时展开，避免界面信息过载。

## 9. 执行顺序与授权gate

| phase | 动作 | 计算 | 输出／gate |
| --- | --- | --- | --- |
| P0 | body-local rotvec实现、parser修正、synthetic／metamorphic tests | CPU | 全部自动测试通过；未读全量raw |
| P1 | 由immutable local-delta shards重建full-train translation＋rotvec signal，并以原轨迹subset验证等价 | CPU | 已闭合`162,760／162,760`、hash、无LLM |
| P2 | 从同一新shards直接运行H0／H1、segment statistics、event-count／relation diagnostics并生成512 geometry calibration | CPU／低GPU渲染 | 人工选择唯一hysteresis／salience／grouping rule；历史H1 graph不得作为H0输入 |
| P3 | 冻结geometry／event／parser、从3／4／5／6选择最小充分budget，生成完整coverage fact packets与deterministic clauses／三条short | CPU | immutable hashes；accepted sample满足`K_text=K_salient`，overflow隔离 |
| P4 | 只跑512 Qwen pilot并完成第二轮language review | 4090或5090 | 冻结prompt、three-short与whole-triplet fallback gate |
| P5 | 在冻结合同上完成sealed 512 | GPU＋人工审核 | 达到四项最低gate；不反向调参 |
| P6 | 生成full-train deterministic triplet与单次Qwen three-short realization | CPU＋GPU | reject整组fallback；不写训练cache |
| P7 | 完成geometry-based FOV／intrinsics audit并写出唯一canonical dataset version | CPU | extrinsics6与Camera14 target scope一致；raw provenance、reason code、hash齐全 |
| P8 | 单独提交raw／canonical-one-short／canonical-three-short与CLIP／T5 Stage2合同 | 待授权GPU长训 | 不由本数据合同自动启动；避免把recaption与augmentation混为一项 |

P8的最小下游矩阵固定解释为：`T0=raw Pulp text`、`T1=同一v2 geometry truth的一条canonical
short`、`T2=同一v2 geometry truth的三条enriched shorts并按exposure均匀抽样`。T0→T1检验
recaption correction，T1→T2才检验语言augmentation；CLIP与T5 text encoder结果分别报告，不能
把encoder变化与caption数量合并成一个实验。

P1原计划执行唯一一次权威全量trajectory重读。实际raw pass在首个4,096样本建立上述等价证据后
因I/O低效停止；完整P1改由已审计的local-delta shards确定性转换，并写齐translation／rotation
signal、sample offsets、histogram与后续event所需字段。P2以后只消费新shards。

> [!warning] 历史10万条provisional例外不改变canonical顺序
> 作者本轮明确要求在calibration前用4090生成10万条新版候选。执行版本固定为
> `pulp_camera_recaption_v1p0_rotvec_h1_eventplan_20260805`：该不可改名ID现登记为v2-pre。全轴统一采用H1，输出记录
> `rule_candidate_status=provisional_not_selected_by_512_calibration`，Qwen只读deterministic
> sentence plan，single-pass后独立reparse，失败即deterministic fallback。数据先确定性分为
> GPU0／GPU1两个互不重叠的50K split。GPU0由两个worker处理；GPU1先由两个worker处理原
> `source_index mod 3 ∈ {0,1}`的33,334条，再由两个worker处理确定性重排的remainder 16,666条。
> 因此始终最多四个模型常驻，四个sample集合互斥并覆盖exact 100K。旧512／30K／40K artifacts
> 不修改。若后续calibration选择H0或更改salience，这10万条只保留为language／throughput
> provenance并整体失去canonical资格，不能局部混入新版本。

### 9.1 v2-pre历史执行artifact（ID保留`v1p0`）

- rotvec conversion：`paperA_pulp_camera_rotvec_shard_conversion_train162760_stride4_v1p0_seed17_4090cpu_20260805`；
  contract SHA256=`a99cfc727dc9e7eada3cbf59bbe1a16869e8bdb39ffdc175b193cd5df49282fa`，
  equivalence SHA256=`1dd01e89e20d1b0c1708a1c11cdd4b3a22879518795e7e3e3acfd9c68fb311a0`。
- provisional H1 event plan：`paperA_pulp_camera_eventplan_n100000_rotvec_h1_v1p0_seed17_4090cpu_20260805`；
  contract SHA256=`f7038bddb805a41e4e4270f898261c2dc46e3bb9759446af8051813426444c2c`，
  共100,000条、842,488个axis events、650,709个required events与19,427条static样本。
- GPU1三逻辑worker run：`paperA_pulp_qwen3_4b_recaption_v1p0_h1_n50000_seed17_4090g1_tri_20260805`；
  contract SHA256=`65fad244ab4a75d6f38692fcf5fd68d65b0a4bd73a933fd33ac44ae752012b10`。
  三模型同时加载的OOM日志保留；修订后只运行worker0／1，worker2队列在产生record前停止。
- GPU1 remainder source：`paperA_pulp_camera_eventplan_gpu1_remainder_n16666_rotvec_h1_v1p0_seed17_4090cpu_20260805`；
  只选择parent `source_index mod 3 = 2`并从零连续reindex，contract SHA256=
  `8b980cef485cdd670be423169fe56ce2aa63327a52e57bd0cdba9758baf859d0`。
- GPU1 remainder双worker run：`paperA_pulp_qwen3_4b_recaption_v1p0_h1_gpu1_remainder_n16666_seed17_4090g1_dual_20260805`；
  contract SHA256=`6185f622176b4aaacd115b478ab966df51f30f9ff3bf325f734e22eca5aeace1`，
  绑定StoryMotion revision `99145173d02aa1f9184eebf9576cc1023236db41`，仅在前两个GPU1
  worker成功完成并释放显存后启动两个worker。
- GPU0双worker run：`paperA_pulp_qwen3_4b_recaption_v1p0_h1_n50000_seed17_4090g0_dual_20260805`；
  contract SHA256=`676b0b76199ee1c29a6ed9fac210697a3cab7cab7b636bae761ef950cbdd09f4`。
- 更改部署合同前的GPU1双worker run保留28条已生成records，不删除、不拼入新run：
  `paperA_pulp_qwen3_4b_recaption_v1p0_h1_n50000_seed17_4090g1_dual_20260805`，contract
  SHA256=`9c44a2b9f587a0cfc7eeffa70ec9566046c00eb545795176338e066990ac3e3e`。

### 9.2 first-20K v2-pre quality audit与停止裁决

> [!failure] v2-pre不得继续扩写
> exact first-completed 20,000条审计发现的不是普通文风问题，而是event-plan、parser与fallback
> 合同冲突。2026-08-05 13:53 +08:00已先停止remainder watcher，再向四个Qwen worker发出
> `SIGTERM`；四进程均正常退出。GPU0／GPU1分别保留9,661／11,397条新版records，共21,058条；
> 旧28条仍隔离，不计入新版。所有Qwen raw text保持逐条immutable，后续修复只做离线reparse，
> 不因本次停止丢失已支付的LLM输出。

评估维度与人工标准冻结为：

| dimension | 合格标准 | 自动检查边界 |
| --- | --- | --- |
| primitive／direction | 不漏主动作、不写反方向、不增加plan外动作 | count-aware primitive-direction recall／precision；重复实例不折叠 |
| temporal structure | 先后、并行、包含与方向反转均与event interval一致 | marker只作proxy；重复同类event的具体配对由人工看interval裁决 |
| short | 一至两句；覆盖主动作与唯一反转；不以冗余换覆盖 | sentence count、required-event coverage与词元粘连 |
| long | 单个连贯段落；覆盖全部required events；不是short的多次改写 | paragraph、coverage、event-ID leak；完整时序仍需人工 |
| fluency | 无粘连、截断、event ID、病句与重复句 | grammar artifact与token-cap flags；不以LLM自评代替人工 |
| training readiness | 前五项同时可接受，无需人工改写即可入库 | mechanical proxy只用于筛查；最终由sealed review决定 |

公平比较只在exact sample identity上进行。first-20K与旧512／30K／40K候选的交集为5,324条；
旧版与新版文本都以新版rotvec H1 event plan为同一参照。正式数字和边界只见
[[StoryMotion-valid-metric-ledger#6A. Pulp Camera recaption first-20K quality audit]]。

结构性失败包括：

1. deterministic short把连接词拼成`rightthen`一类词元，不能被同一closed parser读取；
2. set-based parser只保留每个primitive-direction第一次出现，无法表示
   `right → left → right`的multiplicity与两个reversal；
3. relation graph在复杂样本上组合膨胀，超出一个caption可可靠表达的事实预算；
4. Qwen被拒绝后使用的deterministic fallback没有重新通过同一gate，故`selected_text`并不满足
   “fail-safe”语义。

修复必须是新版本，且不得在当前历史artifact内原地覆盖文本。first-20K后的首版结构修复选择
fixed-top3 fact packet，而不是在60+ step图上做pairwise transitive reduction；其中count-aware
event-instance parser、三条同事实short与whole-triplet same-gate fallback继续进入v2，fixed-top3和
线性relation则因本轮风险审查降级为历史screen。正式v2需先从同源signals完成H0／H1、geometry
grouping与budget calibration，再过6个原语×3条paired review，才可讨论恢复Qwen队列。

审计artifact：

- cohort：`paperA_pulp_camera_recaption_v1p0_first20k_qc_cohort_seed17_4090cpu_20260805`；
  contract SHA256=`a3a4a78eb53ca0c4d9b367f9b039f09bf70259e6d5c0443d503e302374ea133b`；
- comparison：`paperA_pulp_camera_recaption_v1p0_vs_legacy_first20k_qc_seed17_4090cpu_20260805`；
  contract／summary SHA256=`03aecfba2aa8a58fb5dfbb3c47861f44fe6985a4a38608e78ab8546b91514f2d`／
  `3b325cf10a421b7ac1a159232cccef9cb141585cb7182a09a99c45bcac3b8e03`；
- review：`paperA_pulp_camera_recaption_v1p0_vs_legacy_primitive6x3_review_seed17_4090cpu4_20260805`；
  build contract／manifest SHA256=`c8b9ac20bd564a2b80a347a28869243dc4d8d5220a383b402ca0fa761a5ca1dd`／
  `401d2c05fcead399f66419922a10f7fc379ccb3070aaf31feb049a0ed1ffce1f`；
- implementation：StoryMotion revision `fa6361c1`；24项相关unittest通过。

### 9.3 v2结构修复与full-train screen状态

实现位于`experiments/paperA_camera_recaption/`，但需区分可复用组件与尚未成立的v2主链：

- `event_plan_v2.py`只读immutable v2-pre H1 event records；它可用于历史fixed-top3风险screen，
  不能生成H0，也不再是v2 geometry planner；
- `language_realization_v2.py`的count-aware parser、三条同事实deterministic short与whole-triplet
  same-gate fallback继续保留；最终输入需从fixed-top3换成校准后的完整coverage fact packet；
- `text_embedding_qc_v2.py`继续分别记录CLIP／T5分数，但阈值不阻断P7；
- `event_distribution_audit_v2.py`从同一immutable per-step signal shards分别重建H0／H1，第一遍拟合
  各自segment candidate nodes，第二遍报告`K_axis／K_salient`、length bins、预算3／4／5／6覆盖、
  cross-axis overlap／containment、opposite-direction gap，并与历史100K H1按sample核对；
- 新screen不调用LLM、不选择H0／H1、不生成canonical text。run ID为
  `paperA_pulp_camera_event_distribution_h0h1_fulltrain_v2screen_seed17_4090cpu_20260805`；exact
  `162,760` samples／`4,733,272` steps已完成。contract／summary／sample-stats SHA256分别为
  `179eb954b28e8f681df5f9bed1112a82d0b73a75f9c3672ee0de85ff29a4e83f`／
  `b87ffa83a5f8d14ad5cfed7a424a4b8445eb93bfe4d957ab4282045dd23e1c10`／
  `61a66bf0c9d3a3c13d8d1e1c5daa290666c1d108978b932b151406667096ab5b`；该结果仍是screen，
  不在metric ledger登记；
- 当前StoryMotion revision=`65e848f22128e57dd54900aaa5785768b7ef81f5`；相关v1／v2定向单测
  22项通过。远端分支仍为`paper-a-camera-video-review-20260804`。

当前没有经calibration选择的v2 event-plan artifact或v2 Qwen输出；“几何基础代码可运行”不得写成
“v2实现完成”，更不得写成“数据标注完成”。

full-train screen的轴级结果如下；`K_salient`尚未经过跨轴co-temporal grouping，因此不是最终
`K_geom`或文本预算：

| candidate | strict static | weak motion only | captionable motion | `K_axis` mean／p95 | `K_salient-axis` mean／p95 | captionable `K≤3` | captionable `K≤6` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| H0 | 31,621（19.43%） | 57,588（35.38%） | 73,551（45.19%） | 8.273／27 | 1.891／9 | 42,903／73,551（58.33%） | 60,218／73,551（81.87%） |
| H1 | 31,621（19.43%） | 57,918（35.58%） | 73,221（44.99%） | 8.435／28 | 1.872／8 | 42,870／73,221（58.55%） | 60,052／73,221（82.01%） |

该screen关闭四个判断：

1. fresh H1在历史100K同sample上的`K_axis`与`K_salient`均为`100,000／100,000` exact match，
   证明同源replay与历史H1一致；但H0／H1完整geometry graph只在79,034／162,760（48.56%）样本
   exact一致，H0在21,334条（13.11%）产生更少axis events，故H0不能从H1 records反推；
2. 两候选都有约35.4%的`weak_motion_only`，所以“没有caption-selected event即stationary”会造成
   大规模语义误标，必须按4.3分层或abstain；
3. grouping前固定3个event只能完整容纳约58.3%—58.5%的captionable样本；即使预算6也只有约
   81.9%—82.0%。这否决fixed-top3，但不能据此直接选更大K，必须先完成不吞并嵌套事件的
   co-temporal grouping；
4. H0／H1的salient跨轴overlap pairs中，containment分别占69.69%／69.63%，说明`during`不是可省略
   的文风选项。旧100K fixed-top3仅在22,561／44,937（50.21%）captionable样本覆盖全部salient
   axis events；历史`must_preserve`还引入464,258个non-salient events，二者都不能进入v2。

H0／H1的aggregate差距不足以选边；它们共享enter阈值，故strict-static计数相同，主要差异在退出
阈值造成的边界与切段。最终选择仍必须依赖Calibration-512的false split／false merge与人工
salience判断，不能由上表均值直接决定。

### 9.4 尚需敲定的最小标准

以下决定仍未由artifact关闭，不能默认为已解决：

1. Calibration-512在H0／H1中选择唯一hysteresis，并冻结segment salience与sign-consistency；
   “全量统计完成”只证明候选来自完整train，不等于人工边界已经通过；
2. 根据跨轴interval分布提出最小co-temporal grouping候选，并在calibration冻结start／end容差；严禁
   只为减少event数而合并嵌套或异阶段动作；同时冻结compound的salience聚合与哪些弱轴成员可进入
   文本，避免“任一强轴带入全部微弱轴”的噪声放大；
3. 根据`K_geom／K_salient`分布和人工可读性，从3／4／5／6冻结最小充分budget及其coverage门槛；
   accepted sample必须全覆盖，overflow必须隔离；
4. 冻结direct reversal最大gap与`then／overlap／during／reverses`确定性clause模板；
5. Qwen exact checkpoint／revision和JSON triplet解析随pilot冻结。三条仅要求归一化后非完全重复、
   同一fact gate通过，不再人为设embedding距离或“时序版”等差异角色；
6. CLIP exact weights／hash及T5 checkpoint／pooling仍需记录；只有受控诊断显示有效的分数才保留，
   不预设其canonical阈值，也不作为P7 blocker；
7. Stage2若使用三条short，预声明每个exposure均匀`1/3`采样；若要声称三文本提升鲁棒性，必须有
   同一canonical recaption的一条short对照，并分别报告CLIP／T5 encoder，不能把recaption变化与
   augmentation混在一起；
8. 完成按parent source／near-duplicate隔离、带明确v1／v2标识的calibration Gradio、独立sealed
   512，以及基于intrinsics数值而非raw关键词的FOV／zoom scope audit。

> [!warning] 落实裁决
> 可以直接落实且不依赖人工选择的部分只有：H0／H1同源CPU统计、fresh-H1历史一致性检查、
> 12方向＋projection fixtures、parent／near-duplicate分组、intrinsics数值audit及Calibration-512
> 候选构建。最终geometry grouping、event budget、relation clauses与Qwen输入尚不能直接全量落实；
> 它们分别被第2—4项的统计／人工标准阻断。该阻断不授权恢复Qwen或启动任何Stage2长训。

## 10. Artifact schema与版本纪律

每条canonical record至少保存：

```text
sample_id
camera_text_raw
camera_pose_convention_id
camera_attribute_scope
camera_motion_axis_events
camera_motion_geometry_events
motion_state = strict_static | weak_motion_only | captionable_motion | caption_budget_exceeded
caption_fact_packet
camera_text_canonical_template
camera_text_deterministic_shorts[3]
camera_text_enriched_shorts[3]
qwen_status
clip_auxiliary_qc
t5_auxiliary_qc
raw_canonical_conflict
qc_reason_codes
source_hashes
rule_contract_hash
```

数据清洗按caption-motion pair quarantine，不删除整条motion。parent manifest不可变；geometry、
event graph、deterministic text、Qwen output、human review和最终canonical manifest分别保存hash。
旧512／30K／40K Qwen artifacts保持noncanonical provenance，不与新版本拼接。

## 11. 可写claim与停止条件

在P7前只能写：

> We audit Pulp Camera trajectories and define a geometry-grounded recaptioning contract.

不能提前写“发现coordinate-gauge defect”“修复方向错误”或“改善Camera generation”。前两项需要
sealed人工证据；下游改善需要后续raw／canonical matched Stage2实验。

停止或降级条件：

- body-local primitive在synthetic或round-trip测试失败：停止，不进入人工审核；
- H0／H1不能从同一step signal artifact exact重放，或fresh H1与历史H1同sample不一致：停止geometry
  calibration，先修provenance／实现；
- H0／H1都无法在512 calibration达到稳定方向与边界：保留deterministic数值artifact，取消文本贡献；
- 预算内无法完整覆盖salient geometry events：标记`caption_budget_exceeded`并隔离；禁止静默top-K；
- Qwen pilot频繁reparse失败：canonical text使用deterministic template，不继续扩大模型或prompt搜索；
- fallback不能通过与Qwen相同的parser gate，或event multiplicity／relation graph不可表达：立即暂停
  扩写；先修结构contract并离线重放raw Qwen；
- sealed gate失败：只作为内部数据清洗，不列论文贡献；
- matched Stage2没有在raw-conflict stratum产生定向改善：只写数据有效性修正，不写生成收益。

## 12. 相对TriMotion的准确定位

TriMotion提供first-frame RDF、六轴词表、固定per-step threshold、ratio=5和pose-to-symbol-to-Qwen
范式。本方案不声称重新发明该范式；Pulp-specific增量仅是：

1. exact train population上的rate与segment calibration；
2. camera-local primitive避免首帧轴在大旋转后的语义漂移；
3. 对最长62 steps的轴级event归并与deterministic coverage；
4. raw provenance、fallback、人工sealed audit与matched downstream验证。

这四项只有在对应gate完成后才能进入论文。当前优先级是完成一个小而可证伪的v2 canonical
release，不是构建通用cinematographic event language。
