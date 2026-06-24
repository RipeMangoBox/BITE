---
created: 2026-04-19
updated: 2026-04-19
status: active
title: "Roadmap Existing Experiment Verification"
---
# Roadmap Existing Experiment Verification

## 结论

短答案：**否。**

按当前活跃路线图 `ROADMAP.md` 的 R1 定义，仓库里**还没有完成同一实验**。
但仓库里已经完成了几条**非常接近的相邻实验线**，它们验证的是：

- global event-aware training 是否有效
- training-time temporal supervision 是否有效
- 最小 event head + motion unfreeze 是否能在 MotionPatches 上工作

而当前 R1 要验证的是：

- **structured matching > global matching**
- `event x segment` 有序匹配
- `monotonic DP` 结构化打分
- `global top-K -> structured rerank`

因此，当前 Phase 1 应被视为**待启动**，不是“已完成但换了数据集”。

## 当前 R1 的严格定义

当前 `ROADMAP.md` 里的最小可行实验是 `V1 Ordered Event-Segment Rerank`，核心约束有 5 条：

1. Motion 侧使用 MotionPatches 的 `14x5` patch tokens，并沿时间维池化为 14 个 segment tokens
2. Text 侧对 HumanML3D-E 的 `decomposed events` 做独立 event encoding
3. 用 `event x segment` 相似度做 ordered matching，并通过 `monotonic DP` 得到 structured score
4. 推理时先走 global top-K coarse retrieval，再用 structured score rerank
5. `K=1` 样本走 global fallback

这和已有实验最大的区别不在数据集名字，而在**最终 retrieval score 的形成机制**。

## 已有最接近实验

### 1. `plain00_s42`

- 定位：当前 fair global baseline
- 机制：纯 global embedding 检索
- 作用：当前 R1 的零增量锚点
- PrimaryScore：`43.8275`

### 2. `stage5_s2e_v2`

- 定位：当前 same-regime 最强正信号
- 机制：`event CLIP + temporal negatives`
- 关键点：**最终仍然是 global 打分**
- PrimaryScore：
  - `EXPERIMENTS.md` 口径：`44.4487`
  - report 四舍五入口径：`44.50`
- 它证明了：event-aware global training 有效
- 它没有证明：structured rerank 有效

### 3. `stage5_s2e_t`

- 定位：`S2E-v2` 上叠加 TMR event head 的负结果
- 机制：在 global event-aware 训练上再加 `evt_align`
- 关键点：仍然不是 structured rerank，而是 training-time auxiliary temporal grounding
- PrimaryScore：`43.97`
- 它证明了：**只加 temporal head 不足以解决当前瓶颈**

### 4. `stage5_mp_tmrtransfer_d2b`

- 定位：TMR D2b 机制迁移到 MotionPatches 的保留结果
- 机制：minimal event head + motion-only unfreeze
- PrimaryScore：约 `44.03`
- 它证明了：TMR 风格最小 head 在 MotionPatches 上有可迁移性
- 它没有证明：event-segment ordered rerank 优于 global matching

## 为什么这些实验不等价于当前路线

### 差异 1：最终检索打分路径不同

当前路线要求：

- `global_score + structured_score`
- 先 coarse retrieval，再 rerank

现有实验实际做的是：

- 训练后导出一个 global text embedding
- 训练后导出一个 global motion embedding
- 直接计算 `sim_matrix`

也就是说，现有结果仍属于“**单全局相似度排序**”，不是“**结构化二阶段排序**”。

### 差异 2：matching 粒度不同

当前路线要求：

- `event x segment`
- ordered path
- DP 路径分数

现有相近实验实际做的是：

- global contrastive learning
- 或 event-conditioned attention pooling
- 或 temporal hard negatives

这些都在给 global space 提供监督，但**没有把最终匹配单元换成 ordered event-segment path**。

### 差异 3：推理时行为不同

当前路线显式要求 3 类样本处理：

- `single`
- `ordered`
- `parallel`

并要求：

- `ordered` 用 monotonic DP
- `parallel` 放宽顺序
- `K=1` global fallback

现有实验没有这套 inference branch，也没有 sample-type-aware rerank 逻辑。

### 差异 4：当前研究主张已经切换

现有最好结果 `stage5_s2e_v2` 的主张是：

- global event-aware 训练能超过 plain global baseline

当前路线图的主张是：

- **structured matching 本身比 global matching 更强**

这不是同一个问题。前者是“监督增强是否有效”，后者是“最终 scoring mechanism 是否应该改写”。

## 当前代码与实验资产说明

### 已经具备、可以直接复用的部分

- HumanML3D-E strict regime 评测支架已经有了
- HumanML3D-E GT event lookup 已经有了
- MotionPatches `14x5` patch token 结构已经能暴露出 `time_tokens`
- `plain00_s42` 可以继续作为 fair anchor
- `stage5_s2e_v2` 可以继续作为 current best global-event-aware reference
- `stage5_s2e_t` 可以继续作为“只加 temporal head 不够”的负结果证据

### 还没有完成、必须新增的部分

- `event x segment` structured score
- monotonic DP / ordered path search
- global top-K rerank 分支
- `single / ordered / parallel` 三类样本推理逻辑
- `global_score + structured_score` 的组合与 smoke gate 验证

## 对当前路线图的解释

`ROADMAP.md` 把 `S2E-v2` 放在“旧 TAMR”位置是合理的，不是重复劳动。

更准确地说：

- **已完成的是上一代路线**：global event-aware / temporal-aware training
- **未完成的是当前路线**：structured matching rerank

所以当前路线图并不是“把已有实验换个名字再做一遍”，而是在已有 global-event-aware 正信号之上，继续验证**最终检索打分是否应该从 global 改成 structured**。

## 建议保留的正式表述

若后续需要在 roadmap / paper note / session handoff 里引用，这里推荐保留下面这句：

> 现有实验已经验证了 global event-aware training 的有效性，但尚未验证当前 R1 所要求的 structured event-segment matching 与 inference-time rerank；因此 `stage5_s2e_v2` 应被视为当前路线的 strongest old-generation baseline，而非当前 R1 的已完成版本。

## 可直接复用的对照关系

| 当前路线角色 | 对应现有实验 | 用途 |
| --- | --- | --- |
| fair anchor | `plain00_s42` | global baseline |
| 当前最强旧路线 | `stage5_s2e_v2` | old-generation positive signal |
| temporal-head 负结果 | `stage5_s2e_t` | 证明“只加 head”不够 |
| TMR 迁移参考 | `stage5_mp_tmrtransfer_d2b` | 证明 minimal head + motion unfreeze 可迁移 |

## 一句话版本

**仓库里已经做过“像”的实验，但还没有做过“同一个”实验；当前路线真正未完成的，是 structured score 进入最终 retrieval ranking 这一跳。**
