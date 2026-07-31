---
title: "StoryMotion Task-aware SFT Data Preparation — pre-merge archive"
status: archived_superseded_by_unified_curation_contract
tags:
  - StoryMotion
  - stage2
  - data-curation
  - sft
  - status/archived
source_notes:
  - "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
  - "[[current]]"
created: 2026-07-22T14:30:00+08:00
updated: 2026-07-22T18:30:00+08:00
archived: 2026-07-22T18:30:00+08:00
superseded_by: "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
---

# StoryMotion Task-aware SFT Data Preparation — pre-merge archive

> [!warning] 已归档
> 本页是 2026-07-22 合并前原稿，仅保留设计与修改 provenance。正式的质量维度、分档标准、实际计数、nested pools、训练分配和当前 gate 已合并到 [[2026-07-17_storymotion-v8-2333-data-curation-plan]]；本页不再是 active contract。

> [!abstract] 判断
> 从完整 PulpMotion 中筛高质量数据再续训是合理方向，但更准确的名称是 **high-quality continuation / annealing**。现已生成全量多维质量梯度和 `8K / 16K / 32K / 64K` research controls，但只有 `D_H` candidate 可完整构造；`q_C`、完整 `q_HC` 与 `q_CT` 尚未闭合，所以 `D_AE / D_C / D_J` 仍是 partial eligibility，所有 artifact 均 `training_authorized=false`。固定 32K、双分数硬求交、直接删除、依赖人工标注，以及把 Human/Camera role rows 当同一种 pair 的做法不执行。

## 1. 接受与拒绝

接受：

- 高质量阶段可以复用预训练见过的 motion。
- 固定 optimizer steps/sample exposures，避免把子集大小与计算量混淆。
- 保留 random、Physical-only、TMR-only、union 与 Pareto+coverage controls。
- 小集合需要 raw replay control，防止 diversity 与长尾覆盖坍缩。
- 同时报告质量、覆盖、长度、速度、稀有动作与语言属性分布。

不直接执行：

- 不把 `32K / 20%` 当成先验最优。
- 不用 Human TMR 与 Physical 的加权和定义全系统质量。
- 不把双高硬交集作为唯一 SFT 集。
- 不伪造尚不存在的 Camera semantic、fine-align、rarity/complexity 分数。
- 不删除 raw 数据；输出必须 immutable、可逆。
- 本阶段不引入人工标签。

## 2. Task-aware 单位

基础是 162,760 joint motion records；326,144 是 162,760 Human role rows 与 163,384 Camera role rows 之和。

质量轴必须分开保存，不能压成单一总分：

| axis | 含义 | 当前状态 |
| --- | --- | --- |
| `q_H` | Human motion quality | available dimensions 已分解；若原始 scorer 未提供的 articulation/contact/path 维度保持 unresolved |
| `q_C` | Camera trajectory quality | center/rotation 的部分 dynamics 可用；path、jerk、discontinuity 未闭合 |
| `q_HC` | Human-Camera geometry/framing quality | valid-length synchronization 可用；projection/framing/Out/center/scale/margin 未闭合 |
| `q_HT` | Human text-motion alignment | TMR cosine 与 latent L2 独立连续梯度及 Pareto depth 已闭合为 candidate evidence |
| `q_CT` | Camera text-trajectory alignment | unresolved；没有 verified scorer |

理论 pool 合同固定为：

- `D_AE = q_H ∧ q_C ∧ q_HC`
- `D_H = q_H ∧ q_HT`
- `D_C = q_H ∧ q_C ∧ q_HC ∧ q_CT`
- `D_J = q_H ∧ q_C ∧ q_HC ∧ q_HT ∧ q_CT`

当前只有 `D_H` candidate 可以按已声明维度完整物化。`D_AE`、`D_C` 与 `D_J` 必须保留 `partial_eligibility` 名称；不得叫 clean pool、不得启动 SFT。实际 quality levels、counts、hashes 与 unresolved fields 的唯一 Markdown owner 是 [[2026-07-17_storymotion-v8-2333-data-curation-plan|v8.2333 curation contract]]。

| task | target / condition | 最终训练资格合同 |
| --- | --- | --- |
| Direct-H | Human text → Human | `D_H` |
| Direct-C | observed Human + Camera text → Camera | `D_C`；Human TMR 不适用 |
| joint | Human text + Camera text → Human + Camera | `D_J` |

历史 binary proposed/proposed 曾得到 Direct-H `161948`、Direct-C `162398`、joint `161948` 个 eligible joint clips；它只是 provenance，不是当前最终清洗标准。`324970` 只是不同行角色 retained rows 的审计和。

## 3. S0：Task-aware candidate

实现：`scripts/storymotion_sft_task_aware_manifest.py`。

输入：immutable raw、Physical `proposed_p995_x999`、Human TMR `proposed_p995`。

输出目录：`runs/data_curation/storymotion_v8_2333_data_curation_20260717/sft_candidates/task_aware_sft_candidate_v1_20260722/`。

输出 `eligibility.jsonl`、`direct_h.jsonl`、`direct_c.jsonl`、`joint.jsonl`、`metadata.json` 与 `manifest.json`。状态只能是 `complete_candidate_only_not_training_authorized`；Camera 记录必须保留 `camera_semantic_status=unresolved_no_verified_scorer`。

## 4. S1：Pareto + coverage research pools 已物化

已从全量 Physical-v2/TMR-v4 score 构建 `D_H` research universe，并生成 nested `8K / 16K / 32K / 64K`。当前 source 与 action 只是拍摄年份和 caption token proxy；Camera semantic、完整 framing、train-only rarity 与 verified action/source taxonomy 仍未闭合，因此这些不是 Unified/joint SFT 数据。

选择规则：

1. catastrophe candidate 只做可逆 exclusion mask。
2. 其余样本做多维 Pareto rank，不允许极差维度被另一维抵消。
3. 在 duration/source/dynamics/language strata 内 deterministic sampling。
4. 四个规模必须 nested，固定 seed 与 parent hash。
5. 同规模提供 random、Physical-only、TMR-only、union、Pareto+coverage controls。

Camera semantic 缺失时，只能构造 Human-only research screen，不得命名为 Unified/joint SFT dataset。

每个规模同时保留 random、Physical-only、TMR-only、union、Pareto+coverage。固定 seed、raw parent SHA、quality-table parent SHA、ordered-ID SHA 和 deterministic tie handling；每个 control 内要求 `8K ⊂ 16K ⊂ 32K ⊂ 64K`。metadata 必须记录 unique motions、role rows、task conditions、duplicate rate，以及 duration/source proxy/dynamics/language/action-token coverage。isolated random/Physical-only/TMR-only controls 允许包含 L1 中的非 `D_H` candidates；union/Pareto+coverage 限于 `D_H` candidate universe。

## 5. S2：Matched continuation

固定 C3-25 representation、owning decoder、cache builder、Unified implementation、seed、task probabilities、optimizer、LR、steps/exposures、sampler 与 eval IDs。

| arm | 数据策略 |
| --- | --- |
| raw continuation | 原始 task sampler |
| random-size control | 与候选集同规模随机采样 |
| task-aware candidate | S0 task-specific eligibility |
| Pareto+coverage | S1 nested subset |
| Pareto+coverage + raw replay | 90/10 与 80/20 |

主比较固定 optimizer steps，并报告 unique condition exposure、重复率与 task exposure；不能按相同 epoch 比较不同规模。

评估统一报告 Direct-H、Direct-C、joint parallel 的 semantic/distribution/coverage、F1、Out、paired geometry、no-reference physical、diversity、长尾/长序列/高动态/组合文本 coverage。指标上升若伴随 entropy、长度或动态范围坍缩，不算有效收益。

## 6. 当前边界

允许物化并审计 quality gradients、设计 Camera semantic/coverage，以及做不训练的 subset feasibility。

禁止冻结 proposed threshold、直接启动 32K SFT、用 Human TMR 过滤 Direct-C、在 Camera semantic 缺失时声称 joint 已清洗、同时修改 Stage1/backbone/sampler，或不可逆删除 raw。


## 保留的历史实施结果：binary task-aware candidate v1（2026-07-22）

> [!warning] 已被多维质量梯度合同取代
> 本节 artifact 不删除，但只保留 binary-threshold provenance。它没有全量连续多维向量、dimension-wise no-compensation 或 nested volume controls，不能称为清洗完成。

判断结论：高质量 continuation、固定 exposure、matched control、Pareto+coverage 与 replay 原则合理；固定写死 `32K`、破坏性删除、伪造不可用特征、用 Human TMR 过滤 Direct-C Camera target，以及当前阶段引入人工标注均不合理。实现因此只生成候选清单，不授予训练权限。

| task | eligible unit | 数量 | 当前限制 |
| --- | --- | ---: | --- |
| Direct-H | motion/Human row | 161,948 | proposed Physical + TMR exclusion |
| Direct-C | motion | 162,398 | 不施加 Human-TMR target filter |
| Direct-C | Camera-condition row | 163,022 | 多 Camera captions 展开 |
| joint | motion | 161,948 | Physical/TMR motion-level union |
| joint | Human×Camera combination | 162,560 | 多 Camera captions 展开 |

原始基数为 `162,760` joint motions、`162,760` Human rows、`163,384` Camera rows。`326,144` 仅是两个 caption roles 的行数之和，不是 joint pair 数。当前候选为 Physical `362` motions、TMR `450` Human rows，人工标签数为 `0`。

状态：

- `complete_candidate_only_not_training_authorized`
- Camera semantic scorer：unresolved
- LaMP：unresolved
- threshold/coverage gate：not frozen
- artifact：`runs/data_curation/storymotion_v8_2333_data_curation_20260717/sft_candidates/task_aware_sft_candidate_v1_20260722/`
- builder commit：`aed514788f3e8bc6ad76193b105baa4a8c714399`

输出哈希：

| 文件 | SHA256 |
| --- | --- |
| `eligibility.jsonl` | `9de1264495ec70a36efdc4e9628e45cbe5bd6eb42a77b3a05084c8b4d1ac853f` |
| `direct_h.jsonl` | `ac855a7228efc49724c1efe98209ab09429879874957c1261ad987bda563f375` |
| `direct_c.jsonl` | `bcf89f9a6528dad7615ce9808ce2a86e63e9f990635cc196ed2e3ec15edf80cb` |
| `joint.jsonl` | `cce4f29392c0d9caf13e8dcfd67b5d3bb6ee8093ae7341177a877b0c604fcce1` |

其后的 full quality-gradient builder 已完成 `D_H` nested research pools，但并未消除 Camera 轴 blocker。下一步仍不是直接 SFT：必须先闭合 `q_C`、完整 `q_HC` 与 `q_CT`，再重新生成 pools，并预注册固定 exposure 的 matched controls。

## 当前训练分配合同

本轮只生成 manifests，不训练。将来只有在 Camera 轴闭合并另行授权后，才按下列合同进入 matched continuation：

1. Direct-H 只从 `D_H` 取样；Direct-C 只从 `D_C` 取样；joint parallel 只从 `D_J` 取样。
2. 每个 `8K / 16K / 32K / 64K` 规模同时比较 random、Physical-only、TMR-only、union、Pareto+coverage；不得只挑一个看起来最好的规模。
3. 固定 representation、owning decoder、Unified implementation、seed、task probabilities、optimizer、LR、steps、sampler 与 eval IDs；主比较固定 optimizer steps/sample exposures，不按 epoch 对齐。
4. 记录 unique motion exposure、role/task-condition exposure、重复率和 coverage；小池必须另设 raw replay `90/10` 与 `80/20` controls。
5. `manual_labels=0`、`source_deleted=false` 保持不变；任何训练都需要新的 `training_authorized=true` contract，不能回写本轮只读 manifests。


---
更详细的版本，涉及 clean 多类数据区分，以及不同阶段训练的数据分配
可以，而且**不做增广时，训练逻辑反而更清楚**：

> **Stage1 学表示和几何关系：尽量利用 Pulp 的规模，但按质量屏蔽损失。
> Stage2 学文本条件生成：以 clean data 为核心，full data 只按不同模式选择性复用。**

不要简单理解成：

```text
Stage1 = Pulp full
Stage2 = clean
```

更准确的是要把“clean”拆成不同维度，因为三种 Stage2 模式对数据质量的要求不同。

---

# 一、先把 Pulp 数据划成几个可复用子集

设完整数据为 (D_{\text{full}})，建议至少保留五个质量标签：

[
q_H,\quad q_C,\quad q_{HC},\quad q_{HT},\quad q_{CT}
]

分别表示：

* (q_H)：human motion 本身合理；
* (q_C)：camera trajectory 本身合理；
* (q_{HC})：human-camera 几何和 framing 合理；
* (q_{HT})：human motion 与 human text 对齐；
* (q_{CT})：camera trajectory 与 camera text 对齐。

据此构造：

[
D_{\mathrm{AE}}
===============

{q_H\land q_C\land q_{HC}}
]

[
D_H
===

{q_H\land q_{HT}}
]

[
D_C
===

{q_H\land q_C\land q_{HC}\land q_{CT}}
]

[
D_J
===

{q_H\land q_C\land q_{HC}\land q_{HT}\land q_{CT}}
]

其中理论上的 (D_J) 是最严格的 clean joint set。

> [!warning] 当前可构造性
> 下文描述的是 Camera 质量轴闭合后的目标训练路由，不代表现有数据已经达到这些集合。2026-07-22 的现状只有 `D_H` candidate 可完整物化；`D_AE`、`D_C`、`D_J` 均为 partial eligibility，禁止训练。

这个划分非常重要，因为：

* human text 错误的样本不能训练 Direct-H；
* 但如果 human-camera 几何和 camera text 没问题，它仍然可以训练 Direct-C；
* camera text 错误但 human text 正确的样本，仍可训练 Direct-H；
* 只有五项基本都合格，才能训练 joint parallel。

PulpMotion 本身依赖 paired human-camera 数据学习共享 latent，并通过屏幕投影 framing 显式建模二者关系，因此 joint 模式对 pair 质量最敏感。([arXiv][1])

---

# 二、Stage1：joint tokenizer 怎么训练

你的 Stage1 是：

```text
human199 + camera14
        ↓
joint non-causal encoder
        ↓
human latent128 + camera latent64
        ↓
independent human/camera decoders
```

Pulp 原始设计也是 joint encoder、独立 decoder，并额外通过 human-camera latent 预测 framing latent。([arXiv][1])

## Stage1 不需要 text-motion 语义对齐

因为 Stage1 没有文本条件，所以：

* (q_{HT}) 和 (q_{CT}) 不是 Stage1 的必要条件；
* human motion 本身质量、camera 本身质量、human-camera 几何一致性才是关键。

也就是说，**不要因为 caption 不对就把样本从 Stage1 删除**。只要 H、C 和二者几何关系可靠，它仍然是有效 tokenizer 数据。

---

## 推荐的三段式训练

### Phase 1：大规模表示预训练

使用经过最低硬过滤后的 Pulp full：

```text
Pulp full
- 损坏序列
- NaN / 骨架爆炸
- 严重 camera discontinuity
- 极端穿地或人物完全出画
```

训练约 **60%～70% Stage1 steps**。

目标是先学到：

* human motion 的基础重建；
* camera trajectory 的基础重建；
* 两类 latent 的整体分布；
* 不同镜头、时长和动作的覆盖。

这一阶段不建议直接使用完全未经处理的 raw full。至少要做硬错误过滤。

### Phase 2：clean oversampling

训练约 **20%～30% steps**，采用：

```text
50% 从 full-valid 采样
50% 从 clean-pair 采样
```

注意 clean 本身是 full 的子集，因此这是对 clean 样本进行额外过采样，而不是两个独立数据集简单拼接。

作用是：

* 保留 full data 的覆盖；
* 逐渐将 latent manifold 拉向高质量区域；
* 强化可靠的 human-camera coupling。

### Phase 3：clean-only annealing

最后 **10%～15% steps**：

```text
只使用 clean-pair
learning rate 降至之前的 0.1～0.2 倍
```

这一阶段主要修正：

* 低质量 human motion 对 latent 的污染；
* 不稳定 camera trajectory；
* 错误 human-camera 几何相关性；
* framing decoder 的异常映射。

然后**冻结 Stage1**，再开始 Stage2。

---

## 已经有官方 Pulp Stage1 checkpoint 时

不必重新完整训练 full data，直接：

```text
official Pulp tokenizer
        ↓
full-valid : clean = 1 : 1
低学习率适配
        ↓
clean-only annealing
```

推荐只跑原 Stage1 训练量的约 **10%～25%**，重点监控：

* human reconstruction；
* camera reconstruction；
* projected joint reconstruction；
* out-of-frame rate；
* latent variance；
* code/latent utilization。

避免 clean 数据较少时把 tokenizer 微调过窄。

---

# 三、Stage1 不同损失应按数据质量分别 mask

不要只设置一个 `is_clean`，然后决定整条样本用或不用。

假设：

[
\mathcal L_{\mathrm{S1}}
========================

\lambda_H\mathcal L_H+
\lambda_C\mathcal L_C+
\lambda_F\mathcal L_F
]

其中：

* (\mathcal L_H)：human reconstruction；
* (\mathcal L_C)：camera reconstruction；
* (\mathcal L_F)：human-camera framing reconstruction。

推荐按样本做：

[
\mathcal L_{\mathrm{S1}}
========================

q_H\lambda_H\mathcal L_H
+
q_C\lambda_C\mathcal L_C
+
q_Hq_Cq_{HC}\lambda_F\mathcal L_F
]

也就是说：

| 数据状态           | Human loss | Camera loss | Framing/joint loss |
| -------------- | ---------: | ----------: | -----------------: |
| H 好、C 好、pair 好 |          ✓ |           ✓ |                  ✓ |
| H 好、C 好、pair 差 |          ✓ |           ✓ |                  ✗ |
| H 差、C 好        |          ✗ |           ✓ |                  ✗ |
| H 好、C 差        |          ✓ |           ✗ |                  ✗ |

这样可以回收大量 Pulp full，而不让错误 pair 污染跨模态关系。

另外，human latent 128、camera latent 64，不能直接按全部维度求和，否则 human 分支天然获得约两倍权重。建议分别按维度取 mean：

[
\mathcal L_H
============

\frac{1}{128}\sum_{d=1}^{128}\ell_d,\qquad
\mathcal L_C
============

\frac{1}{64}\sum_{d=1}^{64}\ell_d
]

然后再给 modality-level 权重，例如先用：

```text
λH = 1
λC = 1
λF = 0.5 → 1.0
```

---

# 四、Stage2：三种模式分别吃什么数据

Stage1 固定以后，用它为每条 Pulp 数据预编码 latent，然后训练 Unified-3。

## 1. Direct-H：human text → H

使用：

[
D_H={q_H\land q_{HT}}
]

这里不要求：

* camera text 正确；
* camera trajectory 优质；
* human-camera framing 合理。

因为 Direct-H 学的是：

[
p(H\mid t_H)
]

所以只需 human motion 和 human text 可靠。

### 不应使用

* human motion 本身严重错误；
* caption 只描述 camera、不描述 human；
* caption 与 motion 方向、身体部位或动作类别冲突；
* motion 几乎静止但 text 描述明显动态动作。

---

## 2. Direct-C：observed H + camera text → C

使用：

[
D_C
===

{q_H\land q_C\land q_{HC}\land q_{CT}}
]

这里 **不需要 (q_{HT})**。

即使 human caption 错误，只要：

* 输入 human motion 可用；
* camera trajectory 可用；
* human-camera framing 合理；
* camera text 与 camera 对齐；

就可以训练 Direct-C。

Direct-C 的 loss 推荐写成：

[
\mathcal L_{\mathrm{DC}}
========================

\mathcal L_C
+
\lambda_F
\mathcal L_{\mathrm{frame}}(H_{\mathrm{GT}},\hat C)
]

因为此时 human 是 observed GT，可以直接投影预测 camera 下的人体，计算：

* joint NDC error；
* out-of-frame；
* screen-center trajectory；
* shot scale；
* head/pelvis margin。

Direct-C 是最适合回收 Pulp 非严格 clean 数据的模式。

---

## 3. Joint parallel：text → H + C

只使用最严格的：

[
D_J
===

{q_H\land q_C\land q_{HC}\land q_{HT}\land q_{CT}}
]

因为这里模型同时学习：

[
p(H,C\mid t_H,t_C)
]

任何一个维度错误都会产生冲突监督：

* human text 错，会污染 H；
* camera text 错，会污染 C；
* pair 几何错，会污染 H-C coupling；
* human motion 差，会降低动作生成质量；
* camera 差，会降低运镜质量。

所以：

> **Joint parallel 不应该直接吃 Pulp full。它应当是 clean data 最集中的训练模式。**

PulpMotion 的实验也强调，仅先生成 human、再条件生成 camera，不足以获得最好的 framing；joint generation 对跨模态连贯性更有价值，因此 joint 训练数据宁可少一些，也不能明显错配。([arXiv][1])

---

# 五、推荐的 Stage2 训练顺序

## Phase 0：latent interface adaptation

如果 Unified-3 原 checkpoint 使用的不是你当前 Stage1 tokenizer，先冻结主体，只训练：

* input projection；
* output head；
* modality embedding；
* latent normalization；
* 新增 mode embedding。

约占总 Stage2 steps 的 **5%～10%**。

数据使用 clean 为主，避免模型刚适配 latent 时同时学习大量噪声。

---

## Phase 1：按模式进行 broad training

约占 Stage2 的 **50%～60% steps**：

```text
Direct-H       40%
Direct-C       35%
Joint parallel 25%
```

数据来源：

| 模式       | 数据                             |
| -------- | ------------------------------ |
| Direct-H | (D_H)，可明显大于 clean intersection |
| Direct-C | (D_C)，可回收大量 human-caption 错误样本 |
| Joint    | 只用 (D_J)                       |

这个阶段让模型充分学习三个接口，同时尽量利用 full Pulp 中可用的局部监督。

---

## Phase 2：clean multi-mode SFT

约占 **25%～35% steps**：

```text
Direct-H       35%
Direct-C       30%
Joint parallel 35%
```

三个模式都优先从 clean data 中采样，学习率降到 Phase 1 的：

```text
0.2～0.5 倍
```

作用是把 full-data 阶段学到的宽分布向高质量分布收敛。

---

## Phase 3：joint-focused annealing

最后 **10%～15% steps**：

```text
Direct-H       25%
Direct-C       25%
Joint parallel 50%
```

只使用 clean data，低学习率训练。

原因是：

* Direct-H、Direct-C 的单模态能力在前面已经基本稳定；
* 最后重点强化 joint human-camera coupling；
* 同时保留一半单模态任务，防止 joint 训练破坏 H 或 C 的独立质量。

---

# 六、三种模式必须使用不同 loss mask

不要把三种模式都当作相同的 192 维 latent prediction。

建议：

## Direct-H

```text
输入：human text
加噪：H latent
预测：H
loss：L_H
```

不要计算 camera loss。

## Direct-C

```text
输入：observed H + camera text
固定：H
加噪：C latent
预测：C
loss：L_C + λF L_frame
```

不要让模型重新预测 observed H，否则任务会退化成 joint reconstruction。

## Joint parallel

```text
输入：human text + camera text
加噪：H latent + C latent
预测：H + C
loss：L_H + L_C + λF L_frame
```

这里建议保证：

[
\lambda_H\mathcal L_H
\quad\text{和}\quad
\lambda_C\mathcal L_C
]

在训练初期的数值量级接近，而不是因为 human latent 维度更多就自动主导训练。

一个可用起点是：

```text
Direct-H:  L = 1.0 L_H
Direct-C:  L = 1.0 L_C + 0.5 L_frame
Joint:     L = 1.0 L_H + 1.0 L_C + 0.5 L_frame
```

后期可以把 joint 模式的 framing 权重提高到 1.0，但要监控是否牺牲 human FID 或 camera diversity。PulpMotion 的消融同样显示，过强的 coherence guidance 会开始损害单模态 fidelity，因此 framing 约束不是越大越好。([arXiv][1])

---

# 七、只有“full”和单一“clean intersection”时的最保守方案

假设你目前只有：

```text
D_full
D_clean = alignment ∩ physics ∩ geometry
```

还没有 (D_H,D_C,D_J) 的细粒度标签，那么先采用：

## Stage1

```text
前 70%：full-hard-filtered
中间 20%：full : clean = 1 : 1
最后 10%：clean only
```

## Stage2

```text
Direct-H       clean
Direct-C       clean
Joint parallel clean
```

Pulp full 暂时不要进入 Stage2，因为你不知道具体是哪一维出了问题。

不过这会浪费很多数据。下一步最值得做的不是立刻增广，而是把 clean 标记拆成：

```text
human_valid
camera_valid
pair_valid
human_text_valid
camera_text_valid
```

这样无需新增任何数据，就能显著扩大 Direct-H 和 Direct-C 的有效训练集。

---

# 最终推荐配置

```text
Stage1
├── broad AE training
│   └── Pulp full after hard validity filtering
├── quality reweighting
│   └── full-valid : clean-pair = 1 : 1
└── clean annealing
    └── clean-pair only
```

```text
Stage2
├── Direct-H
│   └── human-valid + human-text-valid
├── Direct-C
│   └── camera-valid + pair-valid + camera-text-valid
└── Joint parallel
    └── strict clean intersection only
```

最核心的原则是：

> **Stage1 可以容忍文本不对齐，但不能容忍表示本身损坏；Direct-H 可以忽略 camera 质量；Direct-C 可以忽略 human caption 质量；Joint 则必须使用最严格的 clean pair。**

先把 Pulp full 做成**按监督维度路由的数据池**，通常比只构造一个严格交集、然后所有模式都只吃同一批 clean data 更高效。
