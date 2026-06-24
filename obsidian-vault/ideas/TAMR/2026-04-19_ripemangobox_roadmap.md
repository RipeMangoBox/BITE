# TAMR 执行 Roadmap

## 原则

1. 不强求 TAMR 独立成文，把做出效果作为第一目标
2. TAMR 是方法层，MoProbe / MoDebug 可消费其产出但不构成前置依赖

## 三线关系与并行策略

```
TAMR（方法层：时序感知 retrieval + localization）
  ↓ 提供 temporal feature space / grounding / temporal judge
MoProbe（诊断层：failure diagnosis + capability boundary probing）
  ↓ 提供 failure taxonomy / capability map / repairability prior
MoDebug（干预层：local critique + selective repair）
```

独立性判断：

| 工作      | 独立于 TAMR 的可行性 | 说明                                                                           |
| ------- | ------------- | ---------------------------------------------------------------------------- |
| MoProbe | 高             | 核心是黑盒 minimal-pair probing，大部分维度不依赖 TAMR；时序维度可用 MLLM judge + CAR 兜底          |
| MoDebug | 中             | 数据资产建设（hard subset、局部性统计）可并行；detector 正式训练需要 TAMR grounding 提供高质量 span label |

并行执行方案：

- 立即启动：MoProbe Phase A（MoMask pilot 50-100 条）+ MoDebug 数据资产建设
- 等 TAMR R1 grounding 可用后：MoProbe 时序维度深化 + MoDebug detector 训练

## 设计思路

### Data 级
1. 明确区分"并行"与"因果"——时间并行实为空间并行，空间粒度足够即可处理
2. 动作侧 event 边界的两条路径：
   - 不显式寻找边界：按 motion bin 与 event 时序直接对齐
   - 显式寻找边界：识别关键帧，双向扩充确定边界

### Pipeline 级
1. LLM 架构：引入时间戳 token，构建文本-动作-时间戳三方对齐
2. 非 LLM 架构：temporal positional encoding 注入时序结构

### Training Policy 级
- text embedding 与 motion token 替换，支持帧级或事件级的自由粒度对齐

## 实验设计

### Exp-1：TAMR 自身 vs baseline
1. HumanML3D-E-MP 全集实验
2. condition2 / condition3 / condition4 分层实验
3. condition2/3/4 的 event 顺序扰乱实验（验证时序敏感性）

### Exp-2：TAMR 作为 text encoder 替换 CLIP
1. 冻结 TAMR 表征，在 T2M baseline 上重训
2. 端到端微调 TAMR，在 T2M baseline 上重训

## 执行顺序

### Phase 0：默认配置锁定（已完成）
- 轻量消融结论：`kimodo_like_261` 略优，`pos66` 仅差 0.11；text encoder 收益 schema-dependent
- 消融基于极简架构（`MotionReprBaseline`，9MB ckpt），不可直接迁移到 MotionPatches
- 决策：R1 用 `pos66 + DistilBERT`（MP 原生表示，零额外变量）

### Phase 0.5：MotionPatches 完整架构下的公平消融（暂不进行）

背景：Phase 0 基于 `MotionReprBaseline`（2 层小 Transformer，冻结 text encoder），与 MP 的 `ClipModel`（ViT-B/16 + DistilBERT 端到端微调）架构差异巨大，结论不可直接迁移。

技术挑战：MP 的 `use_kinematic` 要求 `[T, J, 3]` position-based 输入，按 kinematic chain 分组 resize 为 `[T, 80, 3]` patch image。非 position-only 表示（kimodo_like_261/smpl_d135_recon/hy201_recon/guo263/hml272）为 `[T, D]` 2D 格式，需新的 patch 化策略。

阶段 1 — Motion repr 消融（DistilBERT + ViT）：
- 对比 `{kimodo_like_261, guo263, hy201_recon, smpl_d135_recon, hml272}` vs `pos66` baseline
- 实现通用 patch 化适配器：`[T, D]` → `[C, T, W]`
- ViT 使用 `pretrained=True`（ImageNet-21k），`patch_embed.proj.weight` 因通道数变化需重新初始化
- 配置：`train_motion/text_encoder: true, motion_encoder_pretrained: true`
- 训练：50 epoch, batch_size=64, seed=42，与 `plain00_s42` 对齐

阶段 2 — T5 text encoder 消融（Phase 1 冻结策略）：
- 前置：从阶段 1 选出 top-2 motion repr
- 对比 `{t5-base, t5-large, flan-t5-base}` vs `DistilBERT`
- 冻结 T5 主干（`train_text_encoder: false`），仅训练 `text_projection` + ViT
- 若 Phase 1 持平或更优，再考虑解冻 T5 最后 N 层

### Phase 1：R1 核心方法验证（最高优先级）

目标：验证 "structured matching > global matching"

最小可行实验：
- Motion 侧：复用 MP 的 14×5 patch tokens，沿时间维池化为 14 个 segment token
- Text 侧：event encoder 对 HumanML3D-E decomposed events 独立编码
- Matching：event × segment 相似度 → monotonic DP 有序路径 → structured score
- Inference：global top-K 粗检索 → structured score rerank（不替换 global score）
- K=1 样本走 global fallback

Smoke gate：
- K≥2 子集 CAR/TAR 相对 plain00 > +3pp
- 或全局 PrimaryScore > 44.5（超过 S2E-v2 fair 的 44.45）

### Phase 2：消融 + 空间扩展（R1 通过后）
- motion repr × text encoder 2×2 消融，选最优配置
- 最优配置重跑 R1，得到最终数字
- 若 K≥2 子集收益显著，引入 joint-group 打分（R2）

### Phase 3：并行感知 + 收尾
- 并行动作（while/during）放宽顺序约束（R3），仅在误差分析显示必要时启动
- 完整 ablation table + error analysis + 可视化

## 事前验尸：三大致命风险

1. K=1 占比 ~50.7%：一半样本无法受益于 structured matching → 全局指标涨幅可能仅 1~2pp
   - 缓解：分层报告 condition2/3/4 指标，用子集讲故事
2. 14-bin 固定切分 vs 语义边界不对齐：event 边界落在 bin 中间时 segment token 混合两个 event
   - 缓解：先跑 fixed 14-bin，观察 DP 路径质量；不够再上 soft position prior
3. structured score 噪声拖累 global score：新 loss 与 global loss 的 balance 难调
   - 缓解：Phase 1 只做 rerank，structured score 不参与召回，风险隔离

## 0420思考
1. 核心问题：
	1. 动作event是不定长的，甚至有overlap和transition（可能不属于任何event，也可能附带语义）的。基于固定的temporal bin难以精确划分，对alignment带来瓶颈；但非固定的temporal划分又很困难且缺乏gt，或许还得引入弱监督或其他方式。
2. 观察与假设：motionpatches的架构或许存在时序瓶颈
	1. 问题描述
		1. 使用ViT架构本身的时序能力上限需要考核（是否有视频任务基于ViT？毕竟这是image领域的原生应用）；
		2. motion bin将时序划分为bin，bin的大小、bin的硬边界或许都会成为时序切分的瓶颈；
	2. 解决思路
		1. TMR中有提及，使用humanml3d上训练的TMR直接用于BABEL motion序列的滑动窗口匹配，也能得到明显的匹配度谱.![[Pasted image 20260420155144.png]]，但我还没考虑清楚是否需要利用，以及如何利用这一特性（比如寻找motion-text对齐的中心，并设定匹配度阈值确定事件边界，但又需要考虑：
			1. TMR本身能力限制，比如无法很好处理相近语义、局部动作语义、复杂语义等，会限制匹配精度；
			2. 既然使用TMR作数据，是否能力不会超过TMR？同时有点循环依赖的感觉。除非做成“自举式”，但依赖有效的扩张算法。
		2. 是否考虑引入VQVAE等自带temporal压缩的表征模型，一方面对动作数据降维（更平滑）；另一方面时序压缩能将动作序列切分为若干时序精细的片段（一个token对应一个单元片段），从而提供更细粒度的匹配？是否有确定不适用的理由？

### 0420思考评估

#### 证据汇总

1. D2b 1000ep 实验（`tmr_d2b_retrieval_first/guo263`）已完成，关键数据：

| 阶段                     | v_t2m/R01 | v_m2t/R01 | v_evt_align_acc(val/train) |
| ---------------------- | --------- | --------- | -------------------------- |
| Epoch 0（warm-start 起点） | 15.35%    | 15.35%    | 47.0% / 53.0%              |
| Epoch ~50              | ~19%      | ~19%      | ~65% / ~80%                |
| Epoch 999（最终）          | 17.64%    | 18.69%    | 69.7% / 86.2%              |

2. Vanilla TMR warmstart（`tmr/guo263`）仅跑了 20ep，Epoch 19 v_t2m/R01 = 9.93%，仍在快速上升
3. D2b 的 warm-start 起点来自未充分训练的 vanilla TMR（仅 20ep），限制了 finetune 上限
4. evt_align_acc val/train gap（70% vs 86%）表明 event alignment head 存在过拟合

#### 对思考1（不定长 event vs 固定 bin）的评估

- 判断正确：固定 14-bin 确实是对齐精度的瓶颈，但作为 Phase 1 MVP 仍然合理
- 优先级建议：先用固定 bin 验证 "structured > global" 的方向性（Phase 1），边界优化放 Phase 2+
- 弱监督路线（TMR 滑动窗口伪标签）可作为 Phase 2 的 soft position prior，不应作为 Phase 1 核心依赖

#### 对思考2（MotionPatches 时序瓶颈）的评估

- ViT 时序能力：视频领域已有 ViViT / TimeSformer / VideoMAE 等成功案例，ViT + temporal attention 可建模时序。MP 的 patch 化会混合相邻帧，但对 event 级（跨数十帧）粗粒度时序影响有限
- TMR 滑动窗口：可用但存在循环依赖风险（TMR 精度上限 = TAMR 数据质量上限），除非引入自举式 iterative refinement。建议作为辅助信号而非核心依赖
- VQVAE 方向：理论可行但属于架构级变更（替换 motion encoder），不是 TAMR 增量改进。更适合作为独立 ablation（Phase 0.5 motion repr 消融），HumanML3D 14K 样本能否支撑足够细粒度的 codebook 存疑

#### 计划调整

1. 当务之急：vanilla TMR warmstart 需跑满 500ep，当前仅 20ep 的 warm-start 严重限制了 D2b/P2a finetune 上限
2. Phase 1 不变：固定 14-bin + monotonic DP，验证方向性
3. 新增 Phase 2 候选方向：TMR 滑动窗口匹配度谱作为 soft position prior（弱监督边界）
4. VQVAE 方向归入 Phase 0.5 motion repr 消融的可选项，不进入 TAMR 主线

#### 结论

0420 思考提出的两个问题都是真实瓶颈，但当前阶段不应过早引入复杂解法。正确的执行顺序是：先跑满 vanilla TMR warmstart → 用充分训练的 warm-start 重跑 D2b/P2a → Phase 1 验证 structured matching 方向性 → 再根据 DP 路径质量决定是否需要 soft boundary。

### 0420 补充分析：Training-time event alignment 路线复盘

#### 全实验汇总（E-MP guo263, val=1530）

| 模型 | loss 配置 | Epoch | v_t2m/R01 | v_m2t/R01 | 状态 |
|------|----------|-------|-----------|-----------|------|
| vanilla TMR | recons+latent+kl+contrastive | 19/500 | 9.93% | 8.94% | 仅跑20ep，仍在快速上升 |
| D1 (frozen backbone) | global=0.1, evt=1.0 | 27 | 4.44% | 3.46% | 完全失败，retrieval 指标不动 |
| D2b | global=0.1, evt=1.0 | 0 | 10.97% | 7.78% | 仅2ep，第二个epoch崩溃 |
| D2b_retrieval_first | global=1.0, evt=0.25 | 999 | ~19% | ~19% | 饱和，1000ep 无进步 |
| 原始TMR (guoh3dfeats, val=1368) | 同vanilla | 500 | 22.65% | 23.54% | 参考上限 |

#### 根因分析

1. **evt_align loss weight 过高是直接原因**：`global=0.1, evt=1.0` 让 event alignment 主导梯度，破坏 global retrieval。`retrieval_first`（`global=1.0, evt=0.25`）缓解了崩溃但收益有限。
2. **event alignment loss 与 global retrieval loss 存在梯度冲突**：`_masked_event_infonce` 优化的是"event embedding 能从 temporal tokens 中 attend 到正确片段"，这不直接优化 global cosine similarity。
3. **D1 的失败说明 event head 作为独立模块对 retrieval 无帮助**：event alignment 的价值必须通过改变 backbone 表征来体现，但改变 backbone 又破坏 global retrieval。

#### 路线转向决策

Training-time event alignment 路线（D1/D2a/D2b/P2a）在当前 loss 设计下已基本证伪。转向 **推理时 structured rerank** 路线：不改训练过程，只在推理时利用 structured score 重排序，风险隔离。

### ICLR 中稿差距分析

| 维度 | ICLR 中稿水准 | 当前进度 | 差距 |
|------|-------------|---------|------|
| 核心方法 | 有明确技术贡献 + ablation | 核心假设未验证；training-time 路线证伪 | 方法验证 = 0% |
| 实验指标 | 超过或接近 SOTA + 新维度指标 | 所有 event 变体不如 vanilla TMR | 指标 = 负 |
| 数据贡献 | event decomposition 数据集 + 质量验证 | 数据管线已通，缺质量分析 | ≈ 70% |
| 评估协议 | CAR/TAR 定义 + 分层报告 | 定义有，实现无 | ≈ 30% |
| 消融实验 | 每组件 ablation + loss weight 敏感性 | Phase 0 轻量消融完成 | ≈ 15% |
| 写作 | motivation + 方法 + 实验分析 | 未开始 | = 0% |

### R1 步骤化验证方案（推理时 rerank，在 TMR 上先验证）

> 使用蛀牙思维（逐层验证）+ 逆推思维（从目标倒推子能力）

每一步是前一步的 gate，不过就停下分析原因。

| Step | 验证目标 | 方法 | Gate 条件 | 预计耗时 |
|------|---------|------|----------|---------|
| R1-S0 | TMR temporal tokens 有时序区分度 | 滑动窗口编码，检查 latent 随偏移的余弦变化 | 余弦相似度随偏移单调下降 | 2h |
| R1-S1 | Event embeddings 有意义 | TMR text encoder 编码 events，与 motion 片段计算相似度 | event-motion sim > random | 2h |
| R1-S2 | Top-K ceiling 足够高 | 统计 K≥2 子集正确 motion 在 global top-K 内的比例 | ceiling@100 > 80% | 1h |
| R1-S3 | Reverse-order sanity | 正序 vs 反序 event 的 DP score 对比 | 正序 > 反序比例 > 60% | 2h |
| R1-S4 | Structured rerank 端到端 | TMR 上实现 monotonic DP rerank，扫描 λ_s | K≥2 子集 R@1 > +2pp | 4h |

关键：先在 TMR 上验证（代码和 checkpoint 都在），通过后再迁移到 MotionPatches。