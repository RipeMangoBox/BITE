---
## created: 2026-04-05
updated: 2026-04-11
status: historical
note: >
  Phase 1 总纲。Phase 划分和 backbone 迁移计划以
  2026-04-11_tamr-roadmap-phase1-vs-phase2.md 为准。
source:
  - paperIDEAs/2026-04-04_tamr-moprobe-mocritique-roadmap.md
  - paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches.md
  - paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling.md
  - /home/ripemangobox/Coding/Github/Motion/EventT2M-codes-main/src/tools/data_preprocess_decomposed.py
  - /home/ripemangobox/Coding/Github/Motion/TMR/retrieval_results_summary_pretrained.md
tags:
  - research-idea
  - temporal-aware
  - motion-text-retrieval
  - motionpatches
  - eval-regression-scaffold
  - canonical-design
status: canonical-design
title: "TAMR v2: MotionPatches-Based Temporal-Aware Motion Retrieval with an Evaluation-and-Regression Roadmap"
model_name: TAMR

# TAMR v2: MotionPatches-Based Temporal-Aware Motion Retrieval with an Evaluation-and-Regression Roadmap

> 本文取代 `2026-03-31_tamr-backbone-data-pipeline-design.md`，作为 TAMR 的最新 canonical 设计稿。
> 核心变化只有三条：
>
> 1. backbone 从 TMR 切换为 MotionPatches；
> 2. 论文主轴从 "retrieval + grounding 双主任务" 收紧为 "temporal discriminative retrieval 为主，coarse grounding 为证据"；
> 3. 整体推进方式从 "先想完整模型" 改为 "先搭评测与回归支架，再按能力阶梯逐层注入时序能力"。
>
> `2026-04-07` 更正：当前 TAMR 主线以 `HumanML3D-E` 的 GT `decomposed` event text 为准，后续实验固定沿这条主线推进。
> `2026-04-09` 术语更正：本文历史上使用的 `harness`，统一应理解为“评测与回归支架”，不是 agent harness / 权限边界设定。

---
## 一、定稿结论

### 1.1 TAMR 的最终定位

TAMR 不再定义为一个“全能 motion understanding 平台”，而是一个**面向多种时序约束的 discriminative retrieval 方法工作**。

它的 strongest claim 应该是：

> 现有强检索模型即使语义匹配很强，仍然对多事件、多关系、带时间片段需求的查询缺乏完整的时序感知与跟随能力；TAMR 在保持强检索基线的同时，通过表示层时序建模、事件级训练和 coarse evidence localization，显著提升这种能力。

这比只说“比 ChroAccRet 更强”更稳。  
ChroAccRet 是一个重要对手，但不应成为 TAMR 叙事的上限。

### 1.2 Grounding 要不要保留

**结论：保留，但降级为 supporting evidence，而不是 co-primary task。**

原因分三层：

1. **如果完全拿掉 grounding**
  论文风险会变成：“这是不是只是更强的 temporal negatives + 更好的 retrieval backbone？”  
   对 ICLR 级别投稿来说，这样的故事容易被压缩成 incremental retrieval improvement。
2. **如果把 grounding 重新抬到主任务**
  TAMR 会被迫滑向 unified understanding / generation / dense grounding 的大系统，标注、模型、训练预算都会迅速膨胀，主线反而变虚。
3. **最佳平衡点**
  让 TAMR 输出“检索结果 + 粗时间证据”。  
   也就是：不仅判断“这个动作是否存在 / 是否满足时序约束”，还给出**大致时间片段**。这足以支撑“模型真的理解了时间约束”，但不会把项目拖进重型 grounding 赛道。

因此，TAMR 的任务层次应是：

1. **主任务**：temporal discriminative retrieval
2. **必要辅助证据**：action existence + coarse temporal localization
3. **非当前主线**：自由问答式 dense grounding、生成理解统一模型

### 1.3 对“如果没有 grounding，TAMR 不足以单独支撑 ICLR”的回应

这个担心是合理的，但不代表 TAMR 必须做成完整 grounding paper。

更稳的版本是：

- 论文 headline 仍然是 retrieval
- 但必须带有**可验证的时序证据输出**
- 这份证据输出最好是**粗粒度时间定位**，而不是只给一个 yes/no

换句话说，TAMR 不应该去掉 grounding，而应该把 grounding 改写成：

> retrieval-centered temporal understanding with coarse evidence localization

这足以把 TAMR 从“更会排顺序的检索模型”拉升为“更完整的时序理解与跟随模型”。

---
## 二、为什么 backbone 改成 MotionPatches

### 2.1 本地证据

当前本地实验与配置已经给出足够强的切换理由：

- MotionPatches 预训练配置：`50` epoch，`batch_size=128`
- TMR 导出配置：`500` epoch，`batch_size=32`
- 在本地汇总的 pretrained retrieval 结果里，MotionPatches 在 `normal`、`threshold_0.95`、`nsim`、`guo` 等协议上整体优于 TMR

最关键的一点不是“它训练更短”，而是：

> 它在更短训练周期下已经是更强检索表征。

这意味着 TAMR 不必再花论文预算去解释“为什么先把一个弱 backbone 拉到可用”，而可以直接把研究重心放到**时序能力注入**上。

### 2.2 为什么 MotionPatches 训练更短却更强

现阶段最合理的解释是四点共同作用：

1. **ViT 预训练迁移先验更强**
  MotionPatches 不是从零学习 motion encoder，而是把 motion patch 映射到 ViT 友好的结构。
2. **表征形态更适合数据稀缺场景**
  HumanML3D 量级不大，强先验 + patch 化表示通常比从头学 ACTOR-style motion encoder 更占优。
3. **优化目标更纯**
  MotionPatches 更偏纯检索表征学习，TMR 还有 VAE / reconstruction 等额外训练负担。
4. **更大的对比学习 batch**
  对 contrastive retrieval 而言，batch 大小本身就会影响负样本质量与收敛速度。

当然，这不是严格 apples-to-apples 的训练耗时比较，但对于 backbone 选择已经足够。

### 2.3 对 TAMR 的意义

这次切 backbone 反而让 TAMR 的论文故事更强：

- 先用更强的语义检索 backbone 打底
- 再证明：**即便是强 backbone，仍然存在时序盲区**
- 最后展示：时序注入后带来的增益不是“修补弱基线”，而是“补足强检索模型的能力缺口”

这比在 TMR 上做增量更有说服力。

### 2.4 需要明确的边界：MotionPatches 原论文没有 event 概念

这一点必须明确写清，否则后续实现讨论会混淆“原始 backbone 能力”和“本地新增 scaffold”。

MotionPatches 原论文与原始实现的核心是：

- 用 motion patches 替代传统 motion sequence 表示
- 用预训练 ViT 编码整段 motion
- 把**整段 motion**与**整句文本**做全局对齐

它**没有**：

- event-level motion-text alignment
- event-level text encoder
- coarse temporal grounding head
- 基于 `14 x 5` token 网格的显式时序监督

因此，TAMR 不是“打开 MotionPatches 里已有但未使用的 event 能力”，而是：

> 以 MotionPatches 为强全局检索 backbone，在其之上增量注入 event-aware / temporal-aware 能力。

这也意味着当前本地 `MotionPatches-main` 里已经出现的 `event + temporal scaffold`，应被视为**TAMR 的实验性增量**，而不是 MotionPatches 原始能力的一部分。

---
## 三、TAMR v2 的论文主张

### 3.1 主问题

TAMR 要回答的不是“motion-text retrieval 能不能再涨一点 R@1”，而是下面三个问题：

1. **现有强检索表征能否真正理解文本中的时序约束？**
2. **这种能力能否在表示层而不是只在后处理层被注入？**
3. **模型能否给出粗时间证据，证明自己不是只在做全局语义匹配？**

### 3.2 建议写进摘要的三条贡献

1. **方法贡献**
  基于 MotionPatches 提出一个面向多时序约束的 retrieval architecture，在表征层显式注入 temporal discrimination。
2. **训练与数据贡献**
  构建 event-first、timestamp-later 的训练框架，把 HumanML-E 事件监督与 coarse temporal bins 结合起来。
3. **评测贡献**
  提出一个以评测与回归支架为中心的体系，不只看 R@K，还系统评估顺序、并行、持续时间、否定、存在性与粗定位能力。

### 3.3 与 ChroAccRet 的关系

TAMR 不应被表述为 “ChroAccRet++”。

更准确的关系是：

- ChroAccRet 证明了主流 motion-text retrieval 对**顺序**敏感度不足
- TAMR 进一步证明：问题不只在顺序，而在更一般的**temporal following**
- TAMR 的贡献也不只是 hard negative 构造，而是：
  - 更强 backbone 上的时序缺口诊断
  - 表征层 temporal module
  - 事件级训练协议
  - coarse temporal evidence 输出
  - 基于能力层级的分层评测

---
## 四、评测与回归支架视角下的 TAMR 实现路线

### 4.1 这里的“评测与回归支架”指什么

这里说的“评测与回归支架”不是单个评测脚本，而是一个**验证、训练、回归、分析一体化的支架**。

它必须回答五个问题：

1. 这次改动有没有跑对
2. 这次改动有没有学到 temporal signal
3. 它提升的是哪一种时序能力
4. 它有没有伤害原本的 retrieval 表现
5. 它输出的 temporal evidence 是否可信

因此 TAMR 的推进顺序不应是：

`先堆完整模型 -> 最后补评测`

而应是：

`先固定评测与回归 contract -> 再按能力层级递增建模`

### 4.2 Capability Ladder

建议把 TAMR 的能力目标拆成五层，每一层都要有独立数据、损失、指标和 go/no-go 门槛。


| Capability Level | 能力目标        | 最小任务形式                                               | 训练信号                               | 评测指标                                       | 作用                          |
| ------------- | ----------- | ---------------------------------------------------- | ---------------------------------- | ------------------------------------------ | --------------------------- |
| H0            | 语义检索不退化     | 标准 caption-to-motion retrieval                       | 原始 MP 对比学习                         | MP native R@K, MedR, TMR-aligned R@K       | 锁住 backbone 下限              |
| H1            | 顺序敏感        | A then B vs B then A                                 | ordering negatives                 | CAR@K, pair accuracy                       | 对齐 ChroAccRet 起点            |
| H2            | 多事件时序跟随     | event sequence retrieval                             | event-aware positives / negatives  | TAR@K, event-sensitive recall              | 超越单一顺序                      |
| H3            | 多种时序关系      | before / after / while / duration / negation / count | relation-specific negatives        | per-relation TAR, consistency gap          | 建立“完整 temporal following”主张 |
| H4            | 存在性 + 粗时间证据 | “是否存在 X？若存在在何时段？”                                    | existence label + coarse span bins | existence F1/AUROC, span Hit@K, coarse IoU | 证明不是纯全局匹配                   |


如果未来想继续延展，再加一个可选层：


| Capability Level | 能力目标                         | 最小任务形式                                  | 训练信号                             | 评测指标                              | 作用                                      |
| ------------- | ---------------------------- | --------------------------------------- | -------------------------------- | --------------------------------- | --------------------------------------- |
| H5            | 自由问答式 temporal understanding | instruction query -> retrieve + explain | LLM teacher / instruction tuning | open-form QA + retrieval evidence | 对接 unified understanding，但不属于当前 ICLR 主线 |


**关键判断**：  
当前投稿版本做到 `H4` 即可。  
`H5` 是后续扩展，不应前置。

### 4.3 评测与回归支架的工程组成

建议把实现拆成五个稳定接口：

1. **Data contract**
2. **Model slots**
3. **Loss board**
4. **Eval board**
5. **Regression board**

每个接口都应能单独迭代，而不是所有逻辑都耦合在同一个训练脚本里。

---
## 五、数据 contract：先 event，后 timestamp

### 5.1 对当前疑问的明确回答

你之前提出的路线是：

> 先基于 event 切分训练，再逐步增强 timestamp 概念。

**结论：这是合理的，而且是推荐路线。**

原因是：

1. 时间理解的第一性问题不是“秒数回归”，而是**事件边界与事件关系**
2. 如果一开始就要求模型理解精细 timestamp，会把数据、文本模型、损失函数同时复杂化
3. HumanML3D-E 已经足够支撑**文本侧事件监督**与初步 retrieval 验证
4. 动作侧时间建模也不必依赖额外动作侧锚点或精确人工边界

### 5.1.1 HumanML3D-E 当前到底提供了什么

按当前主线口径，HumanML3D-E 真正纳入 TAMR 的是**文本侧 GT 事件监督**。

1. **稳定可直接使用的文本事件监督**
  - `data_train.npy / data_val.npy / data_test.npy`
  - 其中每条 `text_dict` 已带 `decomposed` 字段
  - 这足以替换当前 MotionPatches 里 rule-based event split

因此，当前主线并不假设已经拥有“完整、干净、可即插即用的 motion event segmentation”。

### 5.1.2 初期是否需要先把动作切段

**结论：不需要。**

初期最稳的验证不应该是“先把一段 motion 硬切成若干子 motion 再训练”，而应该是：

- 保留整段 motion
- 用 GT event decomposition 替换规则文本切分
- 先验证 event supervision 本身是否有增益

原因是：

1. 硬切 motion 边界噪声大，容易把第一轮实验做脏
2. 会破坏 MotionPatches 原始“整段 motion 全局检索”的比较口径
3. 你当前最需要回答的问题，是**文本事件结构有没有帮助**，而不是“精细定位现在能不能做得漂亮”

因此，当前更合适的路线是：

- **第一阶段**：不切动作，只做整段 motion + GT event text 验证
- **第二阶段**：继续 `HumanML3D-E-only` 的 event-aware retrieval / 支架化评测验证
- **第三阶段**：再做 token-level temporal module 与 coarse evidence head

### 5.2 不建议一开始就上 LLaMa 3 8B

这是一个非常重要的定稿判断：

**不要因为“最终想理解时间戳”，就把整个文本侧提前替换成 LLaMa 3 instruct 8B。**

原因：

1. TAMR 当前主任务是 discriminative retrieval，不是开放式时序问答
2. timestamp supervision 完全可以先做成**结构化离散标签**
3. 一旦换成 8B 级文本 backbone，训练、显存、缓存、预处理、对齐方式都会整体重构
4. 这会把本来可以在 1-2 个阶段内验证的核心假设，变成一个高风险大工程

更稳的路线应是：

- **阶段 1-3**：保留轻量文本编码器或中等规模编码器，采用结构化 event/timestamp 表示
- **阶段 4**：如果需要更自然的问句理解，再引入 LLM teacher 或 adapter
- **阶段 5**：只有当“自由语言形式的时间提问”成为核心 benchmark 时，才考虑真正切到 instruction LLM 主干

### 5.3 推荐的数据层级

建议把监督分成三层：

1. **L0: caption-level**
  - 原始 HumanML3D caption
  - 用于锁住原始 retrieval 能力
2. **L1: event-level**
  - 来自 HumanML3D-E 的 `decomposed` 文本事件结构
  - 仅文本侧 supervision，不要求动作边界
  - 用于做第一轮 GT-event retrieval 验证
3. **L2: optional refined timestamp-level**
  - 少量人工修正或更高质量边界
  - 只用于分析、校准或后续增强，不作为当前主线必要条件

### 5.4 为什么 coarse timestamp 最适合绑定 MotionPatches

MotionPatches 在 `max_motion_length=224`、`patch_size=16` 下天然对应 `14` 个时间窗口。  
再乘以 `5` 个 body-part patch，就得到 `14 x 5` 的 token 网格。

这给了 TAMR 一个非常自然的注入点：

- **时间边界不标原始帧号**
- 而是标成 `start_bin`, `end_bin`，范围落在 `0..13`

如果一个 event 横跨多个 bin，**不要强行压成单 bin**。  
正确做法是把它视为一个 span：

- `start_bin = floor(start_frame / 16)`
- `end_bin = floor((end_frame - 1) / 16)`

也就是说，一个 event 可以自然覆盖多个连续 bin。

这会带来四个好处：

1. 标注成本低于精细帧级边界
2. 监督形式与 motion token 网格天然对齐
3. coarse grounding head 可以直接对 `14` 个时间 bin 做分类或 span prediction
4. 文本侧无需立刻学“绝对秒数推理”，只要学离散时序概念

这也是 TAMR v2 最重要的结构性简化之一。

但这里也要明确一个工程现实：

> 当前 MotionPatches 实现默认只输出全局 pooled motion embedding，还没有把 `14 x 5` token-level 表征暴露出来。

所以：

- **第一轮 GT-event 验证**不需要 token-level 改动
- **真正使用 bin/span supervision**时，才需要轻量架构改动把 token-level features 暴露出来

### 5.5 推荐的数据 schema

```json
{
  "sample_id": "hml_000123",
  "motion_path": "data/HumanML3D/new_joints/000123.npy",
  "caption": "a person raises both arms and then squats",
  "duration_sec": 7.2,
  "events": [
    {
      "event_id": 0,
      "text": "raise both arms",
      "order": 0,
      "span_source": "optional_coarse_annotation",
      "start_bin": 2,
      "end_bin": 5
    },
    {
      "event_id": 1,
      "text": "squat",
      "order": 1,
      "start_bin": 7,
      "end_bin": 10
    }
  ],
  "relations": [
    {
      "type": "before",
      "head": 0,
      "tail": 1
    }
  ],
  "diagnostic_views": {
    "positive_query": "raise both arms before squatting",
    "negative_queries": [
      "squat before raising both arms",
      "raise both arms while squatting",
      "raise one arm before squatting"
    ],
    "existence_queries": [
      {
        "query": "is there a squat?",
        "label": 1,
        "target_event_id": 1
      }
    ]
  }
}
```

### 5.6 标注推进顺序

推荐按下面顺序推进，而不是一次性做完所有标注：

1. `HumanML3D caption -> event decomposition`
2. `整段 motion + GT event text -> 初步 retrieval 验证`
3. `optional coarse spans / bins -> token-level temporal supervision`
4. `coarse bins -> 少量精细边界子集`

其中最后一步只用于分析和 sanity check，不必作为当前主监督。

---
## 六、模型设计：MotionPatches 上的时序能力注入

### 6.1 总原则

模型设计必须满足三个条件：

1. **不破坏 MotionPatches 原始检索路径**
2. **优先在表征层注入时序能力**
3. **grounding 只做 coarse evidence，不做重型 dense grounding**

### 6.1.1 架构修改应当后置，而不是先行

当前 MotionPatches 的默认形态本质上还是：

- 整段 motion -> 全局 pooled embedding
- 整句 text -> 全局 pooled embedding
- 全局 contrastive retrieval

因此，第一阶段最应该验证的是：

> 把 GT event text 接进现有全局检索框架，是否已经能稳定提升 temporal-aware retrieval。

只有在这个问题得到正向答案后，才值得继续推进下面两类架构修改：

1. 暴露 token-level motion features
2. 在 token-level features 上增加 temporal adapter / span head

### 6.2 推荐的核心模块

建议把 TAMR v2 的模型增量收缩为三个模块。

#### 模块 A：Temporal Patch Relation Adapter

目标：在 MotionPatches 的 `14 x 5` token 网格上注入时序敏感性。

推荐做法：

- 保留原始 global embedding 路径
- 在 patch token 上增加一个轻量 temporal adapter
- 采用**时间优先、空间其次**的 factorized 建模

这里可以明确借鉴 MoGenTS 的思想，但不要直接照搬其生成式重型结构。  
真正值得借鉴的是：

1. **时间轴和空间轴分开建模**
2. **在结构上保留二维 token 关系**
3. **时序模式不是靠最终 pooling 才出现，而是在 token 层被建模**

可以把模块设计成：

```text
patch tokens (14 x 5 x d)
-> temporal mixing across 14 bins
-> part-aware mixing across 5 body groups
-> event-aware pooled tokens
-> global temporal embedding + coarse span logits
```

这一步是 TAMR 相比原始 MotionPatches 最关键的“表征层创新”。

#### 模块 B：Event-Aware Text Structuring

目标：让文本侧从“一整句 caption”转为“全局语义 + 事件结构”的双视图。

推荐做法：

- 保留原始 caption encoder
- 额外构造 event sequence view
- 用轻量 parser / rule-based decomposition 起步
- 将时间关系离散化为结构标签，而不是一开始追求自由语言推理

文本侧输出建议分成三类向量：

1. `z_global_text`：保持与原始 retrieval 兼容
2. `z_event_text[i]`：对齐事件级 motion 表征
3. `z_relation_text`：编码 before / after / while / duration / negation / count

#### 模块 C：Coarse Evidence Head

目标：给出“动作是否存在，以及大概出现在什么时候”的证据。

推荐做法：

- 以 `14` 个时间 bin 为输出空间
- 支持两类输出：
  - `existence logit`
  - `start/end bin` 或 `bin distribution`

这个 head 的目标不是追求 video grounding 那样的高精度 IoU，而是提供：

1. 是否真的找到了对应动作
2. 时间证据是否与文本事件基本一致

### 6.3 不推荐的路线

当前不推荐以下方案作为主线：

1. **一开始把文本 backbone 全量替换成 LLaMa 3 8B**
2. **直接做大一统 retrieval + grounding + generation**
3. **把 dense timestamp regression 当成第一阶段目标**
4. **引入过多视频 grounding machinery，导致 MotionPatches 主线被冲淡**

### 6.4 如果后续一定要接 LLaMa

更合理的方式是：

1. 先训练一个 event-specialized retrieval core
2. 再让 LLaMa 作为 teacher / query reformulator / instruction-side adapter
3. 对齐的是“temporal query understanding”，不是重做整个 motion-text backbone

也就是说：

> 优先“时序专用 retrieval core + 之后与 LLM 对齐”，而不是“一开始就把整个文本链路迁移到 LLM”。

---
## 七、训练路线：分阶段、可回归、可止损

### 7.1 Stage 0：锁定 MotionPatches baseline 与 eval 评测支架

目标：

- 保留 MotionPatches 原生指标
- 保留 strict TMR-aligned fair comparison
- 固定当前评测输出协议，防止后面一边改模型一边改口径

阶段产出：

1. MP native retrieval metrics
2. TMR-aligned retrieval metrics
3. TMR-aligned temporal metrics interface

go/no-go：

- 原始 MP 指标必须稳定复现
- 新改动不得破坏 fair comparison 的输出路径

### 7.2 Stage 1：先做 motion-side temporal injection

目标：

- 不改 MotionPatches 主架构
- 用 HumanML3D-E 的 GT `decomposed` events 替换当前 rule-based event split
- 验证“真实事件监督”本身是否有增益

训练信号：

- 原始 retrieval contrastive loss
- GT event text alignment loss
- 现有 temporal hard negatives 可作为辅助，但不应掩盖 GT event 的主作用

go/no-go：

- 标准 retrieval 不显著下降
- temporal retrieval 指标优于 `MP baseline`
- `MP + GT events` 至少应优于 `MP + rule-based events`

### 7.3 Stage 2：继续 `HumanML3D-E-only` 主线

目标：

- 保持整段 motion，不先切成子 motion clip
- 继续回答“仅靠 GT event text，是否已经足够支撑更强的 temporal retrieval / existence 判断”
- 先把 `HumanML3D-E-only` 主线跑稳，并把它作为后续实验的固定主线

训练信号：

- event alignment loss
- relation-aware temporal contrastive loss
- 原始 retrieval contrastive loss

go/no-go：

- `H2-H3` 指标进一步提升
- 在 `GT-event-only` 设定下也能观察到稳定 temporal gain
- 如果这一阶段已足够支撑论文主张，则继续沿这条主线推进

### 7.4 Stage 3：暴露 token-level motion features并加入 temporal adapter

目标：

- 把 MotionPatches 的 token-level `14 x 5` 表征真正接出来
- 在 token-level 表征上加入 temporal adapter
- 让 motion-side temporal modeling 不再只依赖全局 embedding

训练信号：

- 原始 retrieval loss
- event-aware loss
- coarse temporal supervision（仅在额外高质量 span / bins 可用时）
- token-level temporal module regularization（如需要）

go/no-go：

- 在不明显伤害原始 retrieval 的情况下带来稳定 temporal 增益
- token-level temporal module 比单纯文本侧增强更强

### 7.5 Stage 4：加入 coarse evidence localization

目标：

- 让模型能回答“有没有这个动作”和“它大概在哪”

训练信号：

- existence BCE / focal loss
- start-end bin loss 或 span distribution loss

go/no-go：

- existence F1 明显高于检索分数阈值法
- span 命中率具有可解释性

### 7.6 Stage 5：可选的 LLM 对齐

仅在下面条件同时满足时启动：

1. `H0-H4` 已经跑稳
2. 论文主结果已足够成立
3. 你确定下一步要扩展到更自然的时序问答形式

否则，不启动。

---
## 八、评测与论文证据组织

### 8.1 必须保留的三组评测

1. **MotionPatches native metrics**
  - 证明没有背离 backbone 原始目标
2. **strict TMR-aligned fair comparison**
  - 证明与 TMR / EventT2M / ChroAccRet 系列是可比的
3. **Temporal diagnostic metrics**
  - 证明提升来自 temporal following，而不是仅语义 matching

### 8.2 Temporal 诊断的推荐指标面板

建议至少包含以下几组：

1. **CAR@K**
  - 对齐 ChroAccRet 的顺序能力
2. **TAR@K**
  - 定义为“满足全部指定 temporal constraints 的 retrieval 成功率”
3. **Per-relation accuracy**
  - before / after / while / duration / negation / count
4. **Existence F1 / AUROC**
  - 查询某动作是否存在
5. **Coarse span Hit@1 / Hit@K / IoU-bin**
  - 大致时间片段是否对

### 8.3 论文中的证据呈现顺序

最稳的实验叙事是：

1. MotionPatches 很强，但 temporal blind spot 仍在
2. 仅靠顺序 hard negative 还不够
3. 表征层 temporal adapter + event training 才带来系统性增益
4. coarse grounding/evidence 证明模型不是只在做全局语义匹配

### 8.4 如果 grounding 最终不够强，怎么办

这也是需要提前写进计划的止损策略。

如果 coarse grounding 的绝对值不够亮眼，不要硬把它升成主结果。  
正确做法是：

- 保留它作为 supporting evidence
- 重点展示 existence + span trend + 典型案例
- 把 headline 继续放在 temporal retrieval improvement

只要 grounding 能证明“模型确实在看时间位置”，它就已经完成使命。

---
## 九、论文风险与对应止损

### 9.1 最大风险

最大的风险不是模型做不动，而是**故事被审稿人读成：更强 backbone 上做了更多 hard negatives**。

### 9.2 对应止损方式

必须保证下面三点至少有两点非常强：

1. **表示层 temporal module 明确有效**
2. **多关系 temporal 诊断显著优于基线**
3. **coarse evidence localization 有说服力**

只要做到这三点里的两点，TAMR 就不会被压缩成简单工程整合。

### 9.3 当前最稳的投稿定位

最稳的投稿定位不是：

- “我们做了一个新的 grounding 模型”
- 也不是“我们把 retrieval 和 grounding 大一统”

而是：

> 我们提出一个以强 retrieval backbone 为基础、显式建模多种 temporal constraints、并带有 coarse temporal evidence 的 motion-text understanding framework。

这个定位更适合当前的资产、预算和可复现性。

---
## 十、接下来的最小可执行路线

### 10.1 先做什么

1. 固定 MotionPatches 当前 eval 输出协议
  保留原生指标与严格公平比较路径，不再反复改命名。
2. 定义 TAMR data contract
  先接入 HumanML3D-E 的 GT event text，不把 weak coarse bins 当成前置依赖。
3. 先做第一轮 GT-event 验证
  保留整段 motion，不先切动作，不先做 token-level 架构改动。
4. 继续沿 `HumanML3D-E-only` GT event 主线补诊断与回归证据
  不再保留其他动作侧时间锚点分支。
5. 最后再进入 token-level temporal adapter
  先不碰 LLM，不碰复杂 grounding。
6. 做第一版评测/诊断数据切片
  先覆盖 ordering / before-after / existence 三类。
7. 在 `H0-H2` 跑通后，再接 `H3-H4`

### 10.2 暂时不要做什么

1. 不要先重构成 LLaMa 3 8B 文本主干
2. 不要先追求精细 timestamp regression
3. 不要先做统一生成理解大模型版本
4. 不要让模型复杂度先于评测与回归支架稳定性增长

---
## 十一、最终定稿版一句话

> TAMR v2 的正确方向，不是把 retrieval 扩写成一个过重的 grounding/unified system，而是以 MotionPatches 为强 backbone，围绕 `14 x 5` token 网格做表示层时序建模，采用 `event-first, timestamp-later` 的数据与训练策略，并通过能力阶梯化的评测与回归支架把 temporal discriminative retrieval 做扎实，再用 coarse temporal evidence 证明模型确实理解了“动作何时发生”。

这就是当前最稳、最完整、也最容易真正落地的 TAMR 方案。
