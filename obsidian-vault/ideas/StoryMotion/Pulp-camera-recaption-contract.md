---
title: "Pulp Camera Geometry-Grounded Recaptioning Contract"
status: active_provisional_h1_labeling
hypothesis: |
  使用冻结的camera-local六轴增量、全训练集候选阈值、轴级事件归并和确定性句子计划，
  可以在不让LLM决定几何真值的前提下，为Pulp构造可审核的Camera short／long text。
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
updated: 2026-08-05T14:19:56+08:00
---

# Pulp Camera Geometry-Grounded Recaptioning Contract

> [!important] 当前状态
> 本页评估并收敛`0805-0137`中的Web GPT建议，拥有Pulp Camera recaptioning的算法、
> calibration、语言化与QC合同。全量候选阈值及其artifact只见
> [[StoryMotion/StoryMotion-iclr-reliability#1.1 Pulp Camera full-train threshold audit]]。
> 2026-08-05作者额外授权：保留全部旧标注artifact，以4090处理10万条显式新版candidates。
> 部署固定为GPU0两个、GPU1两个Qwen BF16模型，共四个常驻实例，不使用`2+1`驻留。GPU1三个
> 模型同时加载的OOM日志保留；原第三分片在没有生成任何record时撤销自动接续，并确定性重排为
> 后续双worker remainder。该授权不等于H1规则冻结；在512 calibration完成前，输出固定标为
> `v1p0-H1 / noncanonical`，不得写回训练manifest或冒充sealed evidence。rotation权威表示已从
> Euler转换为rotvec，后续event sweep与10万条语言化只读新版shards，不重复扫描原轨迹。本授权
> 仍不包含canonical写回、Stage2重训或任何模型长训。

## 1. 目标、边界与最小原则

目标是把factual Camera extrinsics确定性转换为Camera-only文本：truck、pedestal、dolly、
tilt、pan、roll、static、复合运动、方向反转及先后关系。每条样本保留raw caption作为provenance，
但raw caption不作为几何真值，也不进入Qwen输入。

本合同不生成以下内容：

- Human-relative位置、人物构图、shot scale、look-at或Human event binding；这些属于DIRECT；
- orbit；仅凭Camera extrinsics不能唯一确定围绕的目标；
- v1中的zoom／FOV；相关raw属性先标记`raw_attribute_unsupported`并按caption-motion pair隔离；
- 通用Camera captioner claim；当前只是Pulp-specific factual recaptioning与审计；
- generated-H与原Pulp GT Camera positive；文本修正不改变factual配对边。

v1 record固定`camera_attribute_scope=extrinsics6`。含raw zoom的motion仍保留；只隔离含未支持属性的
raw caption监督，不删除motion，也不妨碍从同一extrinsics生成六轴canonical text。

实现遵循四个最小原则：

1. 几何层保留全部strict-stride信号，不为语言长度改变stride或删step；
2. canonical真值是轴级事件，不是Qwen文本；
3. 只实现能由确定性测试或人工边界审核裁决的规则；
4. 语言化失败时回退deterministic template，不通过重复采样“碰”正确答案。

> [!abstract] v1唯一主链
> `C2W → C1REL → body-local translation＋rotvec rates → H0/H1 axis intervals →`
> `segment salience → atomic event graph → deterministic sentence plan →`
> `single-pass Qwen realization → independent reparse／fallback`

## 2. Web GPT建议的采纳裁决

| 建议 | 裁决 | v1处理 |
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
| FOV／zoom进入v1 | 暂缓 | 先隔离raw zoom；独立intrinsics审计不阻塞六轴闭环 |
| Qwen返回`covered_event_ids` | 仅作日志 | 自报ID不作为证据；独立reparse才是gate |
| 对极端长graph分块再总结 | 不预实现 | 先统计event数；复杂尾部直接用deterministic long fallback |
| stride2／stride4 sensitivity | 不采纳 | 用户已冻结stride4；用synthetic短事件测试，不重开stride轴 |
| 1,200 calibration＋1,000 sealed | 缩减 | 512 calibration＋512 sealed；其中20%双人复核 |
| 全量复杂Gradio诊断面板 | 缩减 | video、六轴曲线、interval、文本与审核按钮为必需；3D trail按需显示 |

### 2.1 明确拒绝的过度复杂化

v1不实现通用change-point clustering、学习式置信度、每轴独立超参数搜索、复杂父子macro节点、
二次LLM总结或VLM视频判定。这些模块会增加新的阈值与不可验证分支，却不是修正Pulp Camera文本
的必要条件。

Web GPT提出的通用time-reversal测试也需要收窄。camera-local frame会随Camera旋转；一般轨迹
反放后，增量应是带frame change的逆变换，不能简单要求六个符号逐项取反。v1只对纯轴synthetic
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

frame-weighted camera-local节点为主，sample-balanced节点只做稳定性检查。v1只比较两套
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
边界样本和检查caption提及习惯，不能选择阈值。v1不引入手写的`0.8 s`、`0.8 monotonicity`或
`0.75／1.0／1.25 × raw anchor`多重网格。

### 4.4 `must_preserve`

以下event即使不是主导运动，也必须进入long sentence plan：

- 任意可信方向反转的两侧event；
- 第一个和最后一个salient event；
- 新primitive首次出现；
- 被另一个salient event完全包含的短而显著event。

short允许省略非主导secondary event，但不能省略唯一方向反转。long必须覆盖全部
`salient OR must_preserve`事件。

## 5. 最小canonical event graph

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
  "relations": [
    {
      "source": "e1",
      "target": "e0",
      "type": "overlap"
    }
  ]
}
```

relation只允许：

- `overlap`：两个保留event的interval相交；
- `contains`：一个interval完整包含另一个；
- `reverses`：同轴相反方向按时间相邻。

`before／after`由start step天然确定，不写$O(N^2)$边。`repeats／alternates／continues_through`
只允许planner临时派生措辞，不进入数据ontology。

### 5.1 最长62 steps的压缩

压缩发生在event层，不改stride：

1. 同轴同向短gap合并；
2. 长主event与短overlap event保留两个interval，由planner写成“主运动持续、期间加入次运动”；
3. 同轴反向保留为reversal；
4. 不因速度小幅变化切event。

先统计`N_step／N_event／N_required`的p50／p95／p99。Qwen pilot按`1–4／5–8／>8`
required events分层，冻结通过reparse与人工审核的最大`N_qwen_max`。超过该上限的样本直接使用
覆盖全部required events的deterministic long，不实现分块后再让第二个LLM总结。数字`8`只是
pilot分层边界，不是预先冻结的模型能力结论。

## 6. Deterministic plan与Qwen边界

### 6.1 唯一文本身份

每条样本最终只拥有：

- 一条`canonical_short`：通常1句，必要时2句；覆盖主event与方向反转；
- 一条`canonical_long`：一个连续段落；覆盖全部required events；
- 一条`deterministic_fallback`：由同一sentence plan直接渲染。

long不是多条short改写，也不硬性要求3–5句。保真由event coverage定义，而不是句子数。

### 6.2 Qwen输入与输出

Qwen只接收deterministic sentence plan，例如：

```json
{
  "sentences": [
    {
      "required_event_ids": ["e0"],
      "fact": "the camera dollies in from the start to the end"
    },
    {
      "required_event_ids": ["e1", "e2"],
      "fact": "a right pan begins midway and later reverses left"
    }
  ]
}
```

Qwen不接收raw Pulp text、video、Human、逐step 62行数值或阈值解释。Qwen输出一条caption；可同时
记录其自报event IDs，但自报字段不参与验收。每条只生成一次，不做best-of-N或反复重采样。

### 6.3 Independent reparse与fallback

闭集parser从Qwen文本提取primitive、direction、顺序、overlap与reversal，并与sentence plan比较。
任一required事实缺失、方向相反、关系错误或出现plan外primitive时：

```text
qwen_status = rejected_reparse
canonical_text = deterministic_fallback
```

parser必须先补齐单复数、连字符及现有`push-ins／pull-outs`等词形fixture。Qwen的流畅度不能覆盖
几何失败，Qwen自报coverage也不能替代reparse。

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
- 自动reparse后的long required-event recall为100%，hallucinated primitive为0；
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
- deterministic short／long与Qwen short／long；
- 第二阶段才显示Pulp original Camera text与reason codes；
- `合格／不合格／无法判断`、不合格sample多选、description及`下一组`。

3D trail、RDF axes与完整数值表默认折叠，只在坐标／方向失败时展开，避免界面信息过载。

## 9. 执行顺序与授权gate

| phase | 动作 | 计算 | 输出／gate |
| --- | --- | --- | --- |
| P0 | body-local rotvec实现、parser修正、synthetic／metamorphic tests | CPU | 全部自动测试通过；未读全量raw |
| P1 | 由immutable local-delta shards重建full-train translation＋rotvec signal，并以原轨迹subset验证等价 | CPU | 已闭合`162,760／162,760`、hash、无LLM |
| P2 | 从新shards运行H0／H1、segment statistics并生成512 geometry calibration | CPU／低GPU渲染 | 人工选择唯一rule set |
| P3 | 冻结geometry／event／parser，生成deterministic sentence plans | CPU | immutable hashes与versioned manifest |
| P4 | 只跑512 Qwen pilot并完成第二轮language review | 4090或5090 | 冻结prompt、`N_qwen_max`与fallback gate |
| P5 | 在冻结合同上完成sealed 512 | GPU＋人工审核 | 达到四项最低gate；不反向调参 |
| P6 | 生成full-train deterministic text与单次Qwen realization | CPU＋GPU | reject自动fallback；不写训练cache |
| P7 | 写出唯一canonical dataset version | CPU | raw provenance、reason code、hash齐全 |
| P8 | 单独提交raw／short／short-long matched Stage2合同 | 待授权GPU长训 | 不由本数据合同自动启动 |

P1原计划执行唯一一次权威全量trajectory重读。实际raw pass在首个4,096样本建立上述等价证据后
因I/O低效停止；完整P1改由已审计的local-delta shards确定性转换，并写齐translation／rotation
signal、sample offsets、histogram与后续event所需字段。P2以后只消费新shards。

> [!warning] 10万条provisional例外不改变canonical顺序
> 作者本轮明确要求在calibration前用4090生成10万条新版候选。执行版本固定为
> `pulp_camera_recaption_v1p0_rotvec_h1_eventplan_20260805`：全轴统一采用H1，输出记录
> `rule_candidate_status=provisional_not_selected_by_512_calibration`，Qwen只读deterministic
> sentence plan，single-pass后独立reparse，失败即deterministic fallback。数据先确定性分为
> GPU0／GPU1两个互不重叠的50K split。GPU0由两个worker处理；GPU1先由两个worker处理原
> `source_index mod 3 ∈ {0,1}`的33,334条，再由两个worker处理确定性重排的remainder 16,666条。
> 因此始终最多四个模型常驻，四个sample集合互斥并覆盖exact 100K。旧512／30K／40K artifacts
> 不修改。若后续calibration选择H0或更改salience，这10万条只保留为language／throughput
> provenance并整体失去canonical资格，不能局部混入新版本。

### 9.1 v1p0执行artifact

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

### 9.2 first-20K v1p0 quality audit与停止裁决

> [!failure] v1p0不得继续扩写
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

修复必须是新版本，最小范围仅包括：保序的event-instance parser、基于interval transitive
reduction的relation sparsification、带空格／标点测试的deterministic grammar、以及fallback
same-gate assertion。不得在当前v1p0 artifact内原地覆盖文本。修正版本先对本20K离线reparse，
再过6个原语×3条paired旧／新Gradio；只有结构contract与人工review同时通过才可讨论恢复余下队列。

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

## 10. Artifact schema与版本纪律

每条canonical record至少保存：

```text
sample_id
camera_text_raw
camera_pose_convention_id
camera_attribute_scope
camera_motion_events
camera_text_deterministic_short
camera_text_deterministic_long
camera_text_canonical_short
camera_text_canonical_long
qwen_status
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
