---
created: 2026-04-04
updated: 2026-04-08T13:29
tags:
  - paper-idea
  - roadmap
  - Motion_Generation
  - tamr
  - moprobe
  - MoDebug
---
# TAMR / MoProbe / MoDebug 三线路线图（整理版）

> 本文是三条研究线的单一参考入口。整理自 2026-03-24 至 2026-04-03 期间的全部笔记，去除冗余与矛盾，统一边界与依赖关系。

---
## 一、对你当前理解的评估

你的总体理解**大体正确**，但需要三点收紧。

### 1.1 TAMR — 正确，需补充独立性

你说：「TAMR 构建具备时序感知与时序定位的 motion-text retrieval 模型。」

这是对的。补充：TAMR 是**独立成文的方法工作**，不是 MoProbe 的附属 judge 工具。它输出的是可复用的时序感知表征空间、定位能力与评测协议（TAR@K）。

> 一句话：TAMR 是面向时序约束理解的 motion-text retrieval / localization 方法工作。

### 1.2 MoProbe — 方向正确，需收窄叙事

你说：「MoProbe 聚焦 pretrained motion generation model 的指令跟随能力边界，探索 failure case 的具体原因，以辅助其改进；在时序约束遵循上基于 TAMR 评估。」

方向对，但要避免写成"泛 benchmark"。更准确的定义：

> MoProbe 是对预训练 text-to-motion 生成模型做系统性 failure diagnosis 与 capability boundary probing 的工作。

关键词始终是：failure taxonomy、minimal-pair probing、capability map、**diagnosis 而不是 measurement**。

TAMR 在这里的角色是给 MoProbe 提供更可靠的 temporal feature space / temporal judge / localization support，特别是在顺序、并行、否定、持续时间等时序约束上。但 TAMR 本身不是 MoProbe 的子模块。

### 1.3 MoDebug — 正确，需缩窄

你说：「MoDebug 更进一步地，在指出模型指令跟随不足的同时，尝试修复失败动作。」

正确，但不要定义成"泛化 self-correction 大范式"。更稳的版本：

> MoDebug 聚焦于 local semantic critique + repairability boundary + selective local repair。

即：先发现哪里错了 → 再判断这类错是否可修 → 最后验证 local repair 是否优于 whole regeneration。RL / policy learning 是后续放大器，不是现阶段主命题。

---
## 二、三条线的边界定义

### 2.1 TAMR：方法层

**核心问题**：模型能否理解文本中的时序约束？能否同时完成检索与时间定位？

**关键词**：retrieval、localization / grounding、temporal constraints、event-aware encoding、TAR@K

**不应承载**：生成模型 failure taxonomy、benchmark 叙事主体、repair 策略

**Canonical 设计稿**：`TAMR/2026-03-31_tamr-backbone-data-pipeline-design.md`
**综合分析参考**：`TAMR/2026-03-30_temporal-aware-motion-text-retrieval-analysis.md`

### 2.2 MoProbe：诊断层

**核心问题**：预训练生成模型在哪里失败？为什么失败？是能力缺失、调用失败，还是文本歧义？

**关键词**：failure diagnosis、capability boundary、probing、minimal-pair、capability map

**不应承载**：retrieval backbone 设计、localization 模型设计、repair pipeline

**主定义稿**：`MoProbe/2026-03-26_moprobe-capability-boundary-probing.md`
**竞争分析与模型选择**：`MoProbe/2026-03-27_moprobe-vs-motioncritique-competition-analysis.md`
**Benchmark 综述参考**：`MoProbe/2026-03-28_motion-generation-benchmark-survey.md`
**方法论参考**：`MoProbe/2026-03-28_benchmark-trio-failure-analysis-gap-and-guidance.md`

### 2.3 MoDebug：干预层

**核心问题**：如何在生成后准确定位局部 semantic artifacts？哪些 failure case 是可修的？selective local repair 是否比 whole regeneration 更优？

**关键词**：local critic / detector、hard subset、repairability map、local repair、preservation advantage

**不应承载**：泛 benchmark 叙事、retrieval 主方法工作、过早把 RL 作为唯一主线

**主纲（问题拆解 + 论文边界）**：`MoDebug/2026-03-25_motioncritique-problem-decomposition-and-subpaper-scope.md`
**Detector 架构设计**：`MoDebug/2026-03-24_motioncritique-detection-enhancement-replan.md`
**Reviewer 风险评估**：`MoDebug/2026-03-24_motioncritique-strict-feasibility-assessment-claude.md`
**跨域调研参考**：`MoDebug/2026-03-25_image-video-vlm-self-correction-pipeline-for-MoDebug.md`

---
## 三、三条线的依赖关系

```text
TAMR（时序理解方法层）
  ↓ 提供 temporal-aware representation / grounding / temporal judge
MoProbe（失败诊断层）
  ↓ 提供 failure taxonomy / capability map / repairability prior
MoDebug（局部修复层）
```

### 3.1 TAMR → MoProbe

- TAMR 提供时序敏感特征空间
- TAMR 可支持顺序、并行、否定、持续时间等 temporal probes 的判别
- TAMR 的 grounding 能力可帮助定位失败发生的时间段
- 反向依赖为零——MoProbe 不产出可复用的模型组件

### 3.2 MoProbe → MoDebug

- MoProbe 提供 failure taxonomy（A/B/C 三类 13 子类）
- MoProbe 区分 repairable 与 non-repairable case 的先验
- MoProbe 帮助界定 MoDebug 的适用域

### 3.3 TAMR ↔ MoDebug

- TAMR 可为 MoDebug 的 local semantic detector 提供时序表征支持
- MoDebug 的 failure span 分布统计可反过来提示 TAMR 哪些时序约束最值得建模

---
## 四、各自宏观聚焦方向

### 4.1 TAMR

> 定义：一个"显式时序约束建模"的 retrieval + localization 方法工作。

不要滑向：大而全的 motion understanding 平台 / 各种视频 grounding 技术拼装 / MoProbe 的附属 judge 工具。

**当前最应聚焦的三个主张**：

1. 现有 retrieval 模型（包括 PST 的空间细粒度对齐）对时序约束不敏感
2. 显式事件分解 + 时序负样本 + grounding head 能显著改善
3. 该增益不仅体现在顺序，还体现在并行、否定、持续时间等更广的 temporal constraints

**关键决策已锁定**：
- Backbone：TMR（0331 设计稿已确认）
- 主数据集：HumanML3D + FineMotion 时序标注
- 架构：3 模块（Event-Aware Text Encoding + Temporal-Aware Contrastive Learning + Unified Retrieval-Localization Head）

### 4.2 MoProbe

> 定义：failure diagnosis paper，不是 another benchmark paper。

核心不是"做了多少评测"，而是：你把 failure space 结构化了、把 failure 根因区分清楚了、提供了对后续改进可操作的诊断信号。

**当前最应聚焦的三个主张**：

1. 现有 motion benchmark 大多只能测"多差"，不能诊断"为什么差"
2. Minimal-pair probing 是比聚合指标更适合 failure diagnosis 的协议
3. Capability map 与 failure taxonomy 能支持后续 repair / data augmentation / backbone analysis

**关键决策已锁定**：
- Failure taxonomy：A/B/C 三大类 13 子类
- 叙事定位：Diagnostic Analysis Paper（非 Benchmark Paper）
- 方法论+Benchmark 合并为单篇（不拆分）

### 4.3 MoDebug

> 定义：在复杂文本动作生成中，semantic failure 往往是时间局部的，因此 selective local repair 值得研究。

不要写成：泛化 self-correction 新范式 / RL-first 的 motion reasoner / 一篇论文同时解决 detector + repair + policy learning + benchmark。

**当前最应聚焦的四个主张**：

1. Semantic error 的局部性是真实存在且可统计证明的
2. Local detector 能稳定定位错误 span
3. 在 repairable 子集上，local repair 比 whole regeneration 更优
4. 不可修样本应被显式建模，而不是被隐藏

**关键决策已锁定**：
- 差异化锚点：span-localized repair + failure benchmark + local > whole proof
- 第一版论文范围：detector + repairability boundary，暂不做 RL
- 核心竞争对手：Motion-R1、IRG-MotionLLM、MoRL（需明确差异化）

---
## 五、各自待进一步明确的问题

### 5.1 TAMR

**方法定义层**：
1. 最小核心创新到底是哪三个模块？（当前设计已有，但需实验验证每个模块的独立增益）
2. 主打"retrieval 改进"还是"retrieval + localization unified"？
3. Strongest claim 是 ordering，还是更一般的 six temporal constraints？

**数据与评测层**：
1. HumanML3D + FineMotion 的事件聚合规则如何固定？（0.5s 片段 → 语义事件的聚合阈值）
2. TAR@K 与现有 CAR / R@K 的关系如何定义得足够清晰？
3. 时序 hard negative 的六种构造中，哪些是真正必要的，哪些只是可选扩展？

**实验层**：
1. 主干是否稳定锁定 TMR？（已锁定，但需 Stage 0 复现验证）
2. Localization 的收益是否显著支持 joint training，而不是拖累检索？
3. 是否需要跨数据集验证（KIT-ML），还是先把 HumanML3D 做扎实？

### 5.2 MoProbe

**问题定义层**：
1. Failure taxonomy 是否固定为 A/B/C 三大类 13 子类？（当前设计已有，需 pilot 验证可区分性）
2. 每一类失败是否都有清晰、可客观验证的 probe 设计？
3. Diagnosis 与 benchmark 的叙事边界是否已经写清？

**数据构造层**：
1. Pilot 阶段的最小 prompt 集应有多少条，覆盖哪些子类？（建议 50-100 条）
2. Minimal-pair 的可验证性如何优先保证，而不是追求规模？
3. 哪些 probe 需要 temporal-aware judge（依赖 TAMR），哪些用现有 judge 即可？

**模型比较层**：
1. 第一阶段到底比较几个 backbone 最合适？（Phase A: MoMask → Phase B: +BAMM+Motion Mamba+MARDM）
2. 核心结论是"不同模型失败模式不同"，还是"failure root cause 可系统分解"？
3. Capability map 的可视化与统计显著性如何设计得足够令人信服？

### 5.3 MoDebug

**检测层**：
1. Local semantic detector 的输出协议是否固定？（当前有 JSON schema 设计，需工程验证）
2. Hard subset 定义是否已经先于实验固定？（四维 hard score 已设计，需实例化）
3. Detector 的标注资产如何从 pseudo-label 过渡到可投稿级验证集？

**Repair 层**：
1. Local repair 的 action space 到底是什么？（token span / masked regeneration / prompt rewrite）
2. Local repair 与 whole regeneration 的 compute-matched 对照是否已经规划清楚？
3. Repairability score 的预算与惩罚项如何正式定义？

**论文边界层**：
1. 第一篇 MoDebug 论文是否只做 detector + repairability boundary，而暂不做 RL？（建议是）
2. Local > whole 的主张在哪些 hard case 上成立，在哪些 case 上不成立？
3. 需不需要把 non-repairable case 明确写成论文的重要结果之一？（建议是）

---
## 六、建议的执行顺序

### 方案 A：最稳顺序

```text
Step 1: TAMR → ECCV 2026 或 NeurIPS 2026
Step 2: MoProbe → ICLR 2027
Step 3: MoDebug → CVPR 2027 或 NeurIPS 2027
```

### 方案 B：工程上可并行的顺序（推荐）

```text
立即启动（与 TAMR 并行）：
├── MoProbe Phase A：MoMask pilot 50-100 条 minimal-pair probe
│   └── 时序维度暂用 MLLM judge + ChroAccRet CAR 兜底
├── MoDebug 数据资产：hard subset 定义 + semantic error 局部性统计
│   └── 用 MLLM 视频 judge 做粗粒度 span annotation

等 TAMR R1 grounding 可用后：
├── MoProbe 时序维度深化：接入 TAMR temporal judge
├── MoDebug detector 正式训练：用 TAMR grounding 提供高质量 span label

最后：
└── MoDebug local repair 研究
```

理由：
- TAMR 是方法主线，产出可被后续两线消费的工具层
- MoProbe 的大部分探测维度（8 个中的 6 个）不依赖 TAMR，可完全独立先跑
- MoDebug 的数据资产建设可低风险并行，但 detector 训练需要 TAMR localization 的高质量 span label
- MoProbe 不必等 TAMR 全部完成，但时序维度的精度提升需要 TAMR temporal judge
- 真正的 repair 研究应后置

---
## 七、整理后的文件索引

### TAMR（1 篇）

| 文件 | 角色 |
|------|------|
| `TAMR/2026-03-31_tamr-backbone-data-pipeline-design.md` | Canonical 设计稿（含 PST 竞争分析 + Qwen3-VL 启发） |

### MoProbe（1 篇）

| 文件 | 角色 |
|------|------|
| `MoProbe/2026-03-26_moprobe-capability-boundary-probing.md` | 主定义稿（含模型选择计划 + benchmark 方法论参考 + 综合定位） |

### MoDebug（2 篇）

| 文件 | 角色 |
|------|------|
| `MoDebug/2026-03-25_motioncritique-problem-decomposition-and-subpaper-scope.md` | 主纲：问题拆解 + 论文边界 + 知识库评估 + 竞争可行性 + 跨域调研摘要 |
| `MoDebug/2026-03-24_motioncritique-detection-enhancement-replan.md` | Detector v2 架构设计（hard subset 定义 + 三路评分 + span proposal/verification） |

### 已删除文件

| 文件 | 处理方式 |
|------|----------|
| `TAMR/2026-03-30_*.md` | Qwen3-VL 启发部分提取到 0331，其余已被 0331 覆盖 |
| `MoProbe/2026-03-27_*.md` | 模型选择计划提取到 0326，竞争分析已被 0326 覆盖 |
| `MoProbe/2026-03-28_*survey.md` | 综合定位表提取到 0326 |
| `MoProbe/2026-03-28_*guidance.md` | 5 条构造原则提取到 0326 |
| `MoDebug/2026-03-24_*feasibility*.md` | 核心结论 + Go/No-Go 提取到 problem-decomposition |
| `MoDebug/2026-03-25_*vlm-self-correction*.md` | MVP JSON schema + 四类路径提取到 problem-decomposition |
| `MoDebug/2026-03-25_*trainingfree*.md` | 内容被 problem-decomposition + detection-enhancement 覆盖 |
| `MoProbe/*.bak*` | 旧版备份 |

---
## 八、一句话收束

- **TAMR**：做时序理解方法，不做 benchmark 杂糅
- **MoProbe**：做 failure diagnosis，不做 another benchmark
- **MoDebug**（原 MoDebug）：做 local critique + repairability + selective repair，不做泛化 self-correction 大一统叙事

后续所有新笔记都应先判断自己属于**方法层 / 诊断层 / 干预层**中的哪一层，再决定放到 TAMR、MoProbe 还是 MoDebug。

---
## 附：论文 Title

| 项目      | 模型缩写    | Title                                                                                                                         |
| ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| TAMR    | TAMR    | Beyond Semantic Matching: Event-Level Temporal Constraint Modeling for Motion-Text Retrieval and Grounding                    |
| MoProbe | MoProbe | Why Does Your Motion Generator Fail? A Diagnostic Framework for Semantic Capability Boundary Probing in Text-to-Motion Models |
| MoDebug | MoDebug | Locate, Judge, Repair: Selective Local Correction for Semantic Failures in Motion Generation                                  |
