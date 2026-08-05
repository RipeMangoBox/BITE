---
title: "Pulp Camera Geometry-Grounded Recaptioning Contract"
status: v2_implementation_complete_pending_calibration
hypothesis: |
  使用冻结的camera-local六轴增量、全训练集候选阈值、轴级事件归并和确定性句子计划，
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
created: 2026-08-05T01:44:13+08:00
updated: 2026-08-05T16:45:00+08:00
---

# Pulp Camera Geometry-Grounded Recaptioning Contract

> [!important] 当前状态
> 本页评估并收敛`0805-0137`中的Web GPT建议，拥有Pulp Camera recaptioning的算法、
> calibration、语言化与QC合同。全量候选阈值及其artifact只见
> [[StoryMotion/StoryMotion-iclr-reliability#1.1 Pulp Camera full-train threshold audit]]。
> 版本注册现已统一：旧512/Euler/逐采样step阈值及其short／long链称为 **v1**；复用exact
> `162,760`条train、`4,733,272`个stride-4 step的rotvec rate统计，并采用有界事实包的链称为
> **v2**。历史run／artifact ID中的`v1p0`不改名；它们是v2版本注册前产生的
> `v2-pre / noncanonical` provenance。first-20K暴露的是v2-pre语言规划器缺陷，不是全量
> rotvec统计失效。v2代码修正已完成，但尚未生成新Qwen文本、写回canonical manifest或解锁
> Stage2训练。

## 0. 版本注册与当前显示裁决

| semantic version | 数值输入与阈值 | 语言输出 | 当前身份 |
| --- | --- | --- | --- |
| v1 | 最多21个均匀采样pose；Euler／逐采样step临时阈值；step时长随clip长度变化 | 一条short＋一条long；旧30K／40K及port `7868`页面 | immutable legacy review-only |
| v2-pre | exact full-train rotvec rate候选节点；H1 provisional event graph | 无界required events、quadratic relations、一条short＋一条long | 历史ID仍含`v1p0`；first-20K后停止 |
| v2 | 复用v2-pre的全量统计与全部atomic events；caption fact packet最多3个event、最多2条稀疏relation | 同一fact packet的3条short；count-aware parser；whole-triplet same-gate fallback；CLIP/T5辅助QC | 实现与单测完成；待calibration／新artifact |

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

v2 record固定`camera_attribute_scope=extrinsics6`。含raw zoom的motion仍保留；只隔离含未支持属性的
raw caption监督，不删除motion，也不妨碍从同一extrinsics生成六轴canonical text。

实现遵循四个最小原则：

1. 几何层保留全部strict-stride信号，不为语言长度改变stride或删step；
2. canonical真值是轴级事件，不是Qwen文本；
3. 只实现能由确定性测试或人工边界审核裁决的规则；
4. 语言化失败时回退deterministic template，不通过重复采样“碰”正确答案。

> [!abstract] v2唯一候选主链
> `C2W → C1REL → body-local translation＋rotvec rates → H0/H1 axis intervals →`
> `segment salience → complete atomic event graph → bounded caption fact packet →`
> `three-short realization → count-aware reparse／whole-triplet fallback → CLIP/T5 auxiliary QC`

## 2. Web GPT建议的采纳裁决

| 建议 | 裁决 | v2处理 |
| --- | --- | --- |
| `OFF → PRESENT → CAPTION_SALIENT` | 简化采纳 | OFF隐含；每个event保存`salient`与`must_preserve`两个布尔字段 |
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
| 对极端长graph分块再总结 | 不采纳 | 完整数值graph保留；语言侧先压到最多3个event，不生成long或二次总结 |
| stride2／stride4 sensitivity | 不采纳 | 用户已冻结stride4；用synthetic短事件测试，不重开stride轴 |
| 1,200 calibration＋1,000 sealed | 缩减 | 512 calibration＋512 sealed；其中20%双人复核 |
| 全量复杂Gradio诊断面板 | 缩减 | video、六轴曲线、interval、文本与审核按钮为必需；3D trail按需显示 |

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

- $L_a$：K3 lower，作为noise floor；translation已有候选，rotation待rotvec pass；
- $U_a$：K3 upper，作为event enter中心；translation已有候选，rotation待rotvec pass；
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

所有检测到的event都保存在canonical graph；是否写入语言由`salient`决定。先基于H0／H1输出的
全训练集events计算segment-level分布：duration、median rate、net amplitude、path amplitude与
sign consistency。该统计直接读取现有signal shards，不重读Pulp。

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

### 4.4 完整数值graph与有界caption fact packet

`salient`与`must_preserve`仍保留在完整atomic event graph中，用于审计阈值是否产生过多event；
它们不再等于“全部塞进一句文本”。语言侧固定最多3个event instance：

1. 先取跨轴归一化salience最高的primary；
2. 若primary存在可信同轴反向event，优先保留最近的reversal partner；
3. 再优先保留与primary重叠的最强不同轴event；
4. 仍有空位时按归一化salience补齐。

完整graph不删除任何检测结果；未进入文本的event记录`omitted_from_caption_packet`，不是被重新判为
static。`max_caption_events=3`是当前v2实现常数，需由calibration 512确认；若失败，只能整体重开
fact-budget合同，不能对个别sample手工扩容。

## 5. 最小v2 event与relation schema

canonical graph只保存atomic axis events，不保存易膨胀的语言宏节点：

```json
{
  "convention_id": "pulp_c2w_rdf_body_local_rotvec_stride4_v1",
  "events": [
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
      "salient": true,
      "must_preserve": true
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
      "salient": true,
      "must_preserve": false
    }
  ],
  "caption_fact_packet": {
    "selected_event_ids": ["e0", "e1"],
    "max_caption_events": 3,
    "relations": [
    {
      "source": "e0",
      "target": "e1",
      "type": "overlap"
    }
    ]
  }
}
```

完整atomic event graph不物化任意两两relation；interval本身已足够复核。只有最多3个入选
caption events产生relation，每个后续event至多一条边，故最多2条。relation只允许：

- `overlap`：当前event与前一个入选event的interval相交；
- `reverses`：当前event相对最近的同轴入选event反向；
- `then`：既非overlap也非reversal的顺序连接。

这不是对完整graph做transitive reduction，而是先有界选择、再在线性大小的文本子图上建立必要
关系。`contains／repeats／alternates／continues_through`不进入v2文本ontology，避免60+ steps
样本产生$O(N^2)$关系。

### 5.1 最长62 steps的处理

压缩发生在event层，不改stride：

stride-4后最长为62 steps。完整event抽取仍按同轴短gap、方向与interval运行，不裁剪输入；语言
输入只包含有界fact packet，因此不再存在long prompt token超额，也不按长序列分块。QC仍按
`N_step／N_event／N_required`分层报告，用来检测阈值是否在长样本上放大噪声，而不是增加文本容量。

## 6. Deterministic plan与Qwen边界

### 6.1 三条short的唯一语义身份

每条样本最终提供`canonical_shorts[3]`。三条读取完全相同的event IDs与relations；不设置
“主动作版／时序版／复合版”等角色，不允许某一条独有`start／midway／late`、幅度、速度或构图
强调。差异只允许同义动词／名词、主动或名词化句法、以及表达同一必要关系的连接词。三条都必须
独立通过同一个count-aware fact gate；训练如何抽取三条在Stage2合同中另行冻结。

### 6.2 Qwen输入与输出

Qwen只接收最多3个event的bounded fact packet，例如：

```json
{
  "events": [
    {"event_id": "e0", "primitive": "pan", "direction": "right"},
    {"event_id": "e1", "primitive": "pan", "direction": "left"}
  ],
  "relations": [{"source": "e0", "target": "e1", "type": "reverses"}]
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
canonical_shorts = revalidated_deterministic_triplet
```

parser必须先补齐单复数、连字符及闭集Camera词形fixture。Qwen的流畅度不能覆盖几何失败，
Qwen自报coverage也不能替代reparse。

### 6.4 CLIP／T5辅助验证

闭集parser仍是hard fact gate。CLIP与T5分别计算：三条short对canonical fact anchor的相似度、
相对方向翻转hard negative的margin，以及三条caption的两两相似度。前两项筛查语义／方向，后一项
只检查是否近重复；不能用“彼此不相似”替代事实正确。两个encoder独立报告，不按其中一个挑文本，
以免污染后续CLIP／T5训练对比。exact checkpoint、T5 pooling与数值阈值必须在calibration上冻结；
冻结前只输出辅助分数，不作canonical pass/fail。

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

任何synthetic符号错误、gauge失败或round-trip失败都阻断calibration，不能靠人工审核豁免。

## 8. 人工calibration与sealed audit

### 8.1 Calibration 512

从train构造一次性512 cohort：

| stratum | 数量 | 目的 |
| --- | ---: | --- |
| uniform random | 192 | 防止只优化风险样本 |
| threshold／duration boundary | 192 | 选择H0／H1与segment salience |
| compound／overlap | 64 | 检查多轴保留与语言关系 |
| reversal | 32 | 检查方向与顺序 |
| raw-text conflict／contamination | 32 | 第二阶段冲突分类 |

各stratum内部覆盖六轴、正负方向、长度bin与最长序列。P2第一轮隐藏raw text，只看
human＋ground＋camera video、六轴曲线和event intervals；P4语言pilot才进行第二轮，显示
raw／deterministic／Qwen文本，减少raw text anchoring。随机选104条双人复核。

calibration只允许作出四个选择：H0或H1、segment salience节点、sign consistency阈值、是否通过
当前sentence plan。不得扩张新primitive或逐轴微调规则。

### 8.2 Sealed 512

规则、parser与prompt冻结后另选512条：256 uniform random＋256 risk-stratified。sealed结果不再
反向调阈值。最低gate：

- primitive／direction人工正确率不低于95%；
- overlap／reversal关系正确率不低于90%；
- 三条short各自的caption-packet event-instance recall为100%，hallucinated primitive为0；
- 人工`可直接作为训练文本`通过率不低于90%。

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
| P2 | 从新shards运行H0／H1、segment statistics并生成512 geometry calibration | CPU／低GPU渲染 | 人工选择唯一rule set |
| P3 | 冻结geometry／event／parser，生成bounded fact packets与deterministic三条short | CPU | immutable hashes、最多3 events／2 relations与versioned manifest |
| P4 | 只跑512 Qwen pilot并完成第二轮language review | 4090或5090 | 冻结prompt、three-short与whole-triplet fallback gate |
| P5 | 在冻结合同上完成sealed 512 | GPU＋人工审核 | 达到四项最低gate；不反向调参 |
| P6 | 生成full-train deterministic triplet与单次Qwen three-short realization | CPU＋GPU | reject整组fallback；不写训练cache |
| P7 | 写出唯一canonical dataset version | CPU | raw provenance、reason code、hash齐全 |
| P8 | 单独提交raw／canonical-one-short／canonical-three-short与CLIP／T5 Stage2合同 | 待授权GPU长训 | 不由本数据合同自动启动；避免把recaption与augmentation混为一项 |

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

修复必须是新版本，且不得在当前历史artifact内原地覆盖文本。v2选择有界fact packet，而不是在
60+ step图上做pairwise transitive reduction；实现包括count-aware event-instance parser、最多3个
caption events／2条relations、三条同事实short、whole-triplet same-gate fallback与CLIP/T5辅助QC。
新artifact仍须先过calibration和6个原语×3条paired review，才可讨论恢复Qwen队列。

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

### 9.3 v2结构修复状态

v2实现位于`experiments/paperA_camera_recaption/`：

- `event_plan_v2.py`只读immutable v2-pre event records和parent hashes，复用全量阈值统计，不重扫
  raw trajectory；输出新label `pulp_camera_recaption_v2_rotvec_three_short_20260805`；
- `language_realization_v2.py`生成三条共享fact packet的deterministic short，按event instance计数和
  文本位置验收重复动作，Qwen失败时整组三条回退并重新验收；
- `text_embedding_qc_v2.py`分别计算CLIP／T5 fact-anchor、方向翻转margin与三句两两相似度；阈值
  未经calibration前只报告diagnostic；
- v1＋v2定向单测共19项通过，覆盖十二个方向、static／overlap、60-event有界选择、线性relation、
  完整graph omission provenance、重复`right → left → right`、词元边界、unplanned event、
  same-gate fallback和双encoder分离报告；
- StoryMotion revision=`43ee3a6c8f6b53c5e516bf0c20f6d926aeaeaa8d`，远端分支
  `paper-a-camera-video-review-20260804`。

当前没有v2全量event-plan artifact或v2 Qwen输出；“实现完成”不得写成“数据标注完成”。

### 9.4 尚需敲定的最小标准

以下决定仍未由artifact关闭，不能默认为已解决：

1. calibration 512在H0／H1中选择唯一hysteresis，并冻结segment salience与sign-consistency；
   “全量统计完成”只证明candidate nodes来自完整train，不等于人工边界已经通过；
2. 验证`max_caption_events=3`及当前primary／reversal／overlap选择是否在random、长序列、compound和
   reversal strata中可接受；若不通过，整体重开fact-budget，禁止逐sample补丁；
3. 冻结三条short的最小／最大词汇差异，防止仅换标点，也防止为了差异加入独有事实；Qwen exact
   checkpoint／revision和JSON triplet解析随pilot一并冻结；
4. 冻结CLIP exact weights／hash，以及T5 exact checkpoint、token pooling与两套encoder各自的
   fact-anchor、direction-margin和pairwise-similarity阈值；两者都只作辅助，不替代rule gate；
5. Stage2若使用三条short，预声明每个exposure均匀`1/3`采样；若要声称三文本提升鲁棒性，必须有
   同一canonical recaption的一条short＋CLIP对照，不能把recaption变化与augmentation混在一起；
6. 完成带明确v1／v2标识的calibration Gradio、FOV／zoom pair quarantine和独立sealed 512。

## 10. Artifact schema与版本纪律

每条canonical record至少保存：

```text
sample_id
camera_text_raw
camera_pose_convention_id
camera_attribute_scope
camera_motion_events
caption_fact_packet
camera_text_deterministic_shorts[3]
camera_text_canonical_shorts[3]
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
- H0／H1都无法在512 calibration达到稳定方向与边界：保留deterministic数值artifact，取消文本贡献；
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

这四项只有在对应gate完成后才能进入论文。当前优先级是得到一个小而可证伪的v1，不是构建通用
cinematographic event language。
