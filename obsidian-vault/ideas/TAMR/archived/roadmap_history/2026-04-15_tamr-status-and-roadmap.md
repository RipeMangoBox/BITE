---
created: 2026-04-15
updated: 2026-04-15 (v6, PRISM-integrated)
status: active
title: "TAMR 现状全景 & ICLR Roadmap"
tags:
  - tamr
  - motionpatches
  - roadmap
  - iclr
---
# TAMR 现状全景 & ICLR Roadmap

> 本文档是 TAMR 项目的总控笔记，梳理当前设计、实验现状、根因分析、ICLR 可行性判断，以及后续 step-by-step roadmap。

---
## 一、当前设计全景

### 1.1 Data

**动作数据格式：**
- 原始数据：HumanML3D `new_joints/*.npy`，shape `[T, J=22, 3]`，全局关节位置（global joint positions），20 FPS，最长 224 帧
- **不是** Guo 263-dim 特征（那是 TMR 用的），而是直接的 3D 关节坐标
- Motion Patches 构造：22 个关节按 5 条运动链（左腿/右腿/脊柱头/左臂/右臂）分组，每条链通过双线性插值 resize 到 16 个 patch → `5×16=80` 空间 patch/帧
- 归一化后 permute 为 `[C=3, T=224, J=80]`，作为 3 通道"图像"送入 ViT
- ViT patch size 16×16 → grid `(14, 5)` = 14 个时间 bin × 5 个身体部位 = 70 patch tokens + 1 CLS token

**与 Kimodo / PRISM 的对比启发：**
- Kimodo 使用 raw motion space：`[r_p, r_a, j_p, j_v, j_a, f]`（root 位置/朝向 + 关节位置/速度/角度 + 足接触），维度更丰富
- Kimodo 的 smoothed root + 非 canonicalized joints 表示更适合长程轨迹连续性
- MP 的 motion patch 表示丢失了速度/加速度/旋转信息，只保留位置 → 时序动态信息被隐式编码在相邻帧差异中，而非显式表达
- PRISM (arXiv'26) 进一步证明：即使不改生成器，仅把 per-frame monolithic latent 改成 per-joint decomposed latent，也能带来数量级收益；这说明 motion tokenization 粒度与运动学对齐本身就是一级设计变量
- **启发**：当前 MP 的 motion patch 表示对时序信息的编码是隐式的，这可能是时序能力学习困难的底层原因之一；同时 Step 3.2 不应再被视为普通 input ablation，而应视为可能决定上限的主线

**文本数据：**
- 原始 caption：HumanML3D `texts/*.txt`，格式 `caption#POS#f_tag#to_tag`
- Event 分解：`HumanML3D-E/data_{train,val,test}.npy` 中的 `text[].decomposed`，由 Gemini 2.5 Flash 生成，每个 caption 分解为有序 event 列表
- GT event 覆盖：corrected D0 全量审计（83347 captions across train/val/test），event extraction coverage 100%，canonical `text[].decomposed` coverage 100%
- K 分布（corrected D0 全量口径，83347 captions）：**K=1 占 50.70%**（42261 条），K≥2 占 49.30%（41086 条），规则 overlap 占 1.81%（1508 条）
- Train split 明细：66636 captions，K=1 ≈ 52.0%，K=2 = 22962，K=3 = 6524
- ⚠️ 旧 D0（938 条 eval split）已被 corrected D0 supersede，本文档所有统计均以 corrected D0 为准

**当前负样本构造：**
- 包含 event 乱序负样本（ordering shuffle、reverse order）
- 还包含：negation insertion、duration modification、relation-sensitive negatives（before↔while swap）、existence negatives
- 这些负样本在 `temporal_utils.py` 中实现；ordering 类负样本已确认接入 S2E-v2，其余类型的实际有效覆盖仍需 Step 3.0 审计

**并行 event 处理现状：**
- ⚠️ 需要检查：当前 HumanML3D-E 的 event 分解是否正确处理了 "and" 表示并列的情况（如 "walking and waving" 应为并行而非顺序两个 event）
- 这是一个潜在的数据质量问题，可能影响 temporal hard negative 的有效性

### 1.2 Pipeline (Model Architecture)

**Motion Encoder：**
- `ViT-Base/16`（timm），ImageNet-21k pretrained
- 12 层 Transformer，12 heads，768-dim hidden，3072 FFN
- 输入 `(3, 224, 80)` → 70 patch tokens + 1 CLS → global avg pool → 768-dim
- 通过 `ProjectionHead`（768→256→256，GELU + residual + LayerNorm）投射到 256-dim 共享空间

**Text Encoder：**
- `DistilBERT-base-uncased`（HuggingFace pretrained）
- **不是基于 pretrained TMR**，是标准 DistilBERT 初始化后端到端 fine-tune
- 取 `[CLS]` token → 768-dim → 同样的 `ProjectionHead` → 256-dim
- TMR 的 text encoder 是 DistilBERT tokens → ACTORStyleEncoder（6L Transformer），两者架构完全不同

**对比 TMR 的创新：**
- TMR 用 263-dim Guo 特征 + 6 层 ACTOR Transformer（~2M params）
- MP 用 raw joint positions + ViT-Base（~85M params），表征能力更强
- MP 的 14×5 patch grid 天然提供了时间-空间分解结构（14 time bins × 5 body parts）
- 但 MP 的 text encoder 更简单（直接 [CLS] pooling vs TMR 的 Transformer encoder）

**Event-Temporal 扩展模块（当前已实现）：**
1. Event CLIP Loss：event text → DistilBERT [CLS] → ProjectionHead → 256-dim，直接与 motion embedding 做 CLIP loss
2. Temporal Hard Negative Loss：margin-based triplet loss，positive_score - negative_score > margin
3. TMR Event Head（辅助）：time tokens (14, 768) → event_proj_t → (14, 256)，event text → event_proj_e → (N, 256)，masked attention pooling → per-event InfoNCE
4. Temporal Token Adapter（已废弃）：TransformerEncoder 处理 14 time tokens + learned temporal pooling，Stage4 实验证明会导致表征漂移

### 1.3 Training Strategy

**当前最佳配方（S2E-v2）：**
```yaml
train_motion_encoder: true    # ViT 全解冻
train_text_encoder: true      # DistilBERT 全解冻
init_from_checkpoint: null    # 从 ImageNet ViT 从零训练（关键！warm-start 会退化）
event_temporal:
  enable: true
  enable_event_loss: true     # event CLIP loss 直接在 retrieval 空间
  enable_temporal_loss: true  # temporal hard negative loss
  event_source.type: gt       # GT events from HumanML3D-E
  loss:
    global_weight: 1.0        # 主 CLIP loss
    event_weight: 0.5         # event CLIP loss
    temporal_weight: 0.3      # temporal hard negative loss
optimizer: Adam
lr: 1e-5 (text) / 1e-4 (motion, projection)
batch_size: 64
epochs: 50
```

**对比学习设计：**
- 主 loss：symmetric CLIP loss（cross-entropy on cosine sim / learnable temperature）
- Event CLIP loss：event text embeddings @ motion embeddings.T，直接在 256-dim retrieval 空间
- Temporal hard negative loss：margin-based，margin=0.1
- ⚠️ 当前没有 blockwise / hierarchical loss 设计
- ⚠️ 当前没有 event 组合边界的显式学习

**已验证的关键教训：**
1. warm-start from pretrained 会导致退化（S2E: 42.76 vs S2E-v2: 44.50）
2. TMR event head 作为辅助 loss 无增量价值，反而干扰（S2E+T: 43.97 < S2E-v2: 44.50）
3. 重型 temporal adapter 会导致表征漂移（Stage4 首轮 No-Go）
4. minimal event head + full unfreeze 是安全的（Phase 1 D2b 验证）

### 1.4 Inference

**当前推理路径（标准）：**
- `encode_motion(motion)` → ViT forward → avg pool → ProjectionHead → L2 normalize → 256-dim
- `encode_text(tokenized)` → DistilBERT [CLS] → ProjectionHead → L2 normalize → 256-dim
- Similarity = `text_embs @ motion_embs.T`（cosine similarity）
- 无特殊 inference 设计

**已实现但未启用的 inference 模块：**
1. Temporal Adapter Inference：用 temporal_token_adapter 替代 avg pool，Stage4 证明有害
2. Event-Patch Alignment：Gaussian prior + content similarity 做 event→time bin 对齐，可用于可视化但不参与 retrieval ranking

**⚠️ 当前 inference 没有任何时序感知设计** — 这是一个潜在的改进方向

### 1.5 Eval 指标体系

**文件位置：** `checkpoints/*/HumanML3D/contrastive_metrics/`

| 文件前缀 | 含义 | 关注维度 |
|---|---|---|
| `normal.yaml` | MP 原生 full test set retrieval | 基础 retrieval 能力 |
| `nsim.yaml` | MP 原生 non-similar split（harder） | 语义区分能力 |
| `guo.yaml` | Guo-style batched eval (batch=32) | 与 generation 论文可比 |
| `threshold_0.95.yaml` | 文本自相似过滤 | 去重后 retrieval |
| `TMR-normal.yaml` | TMR strict split（每 sample 仅第一条 caption） | **主要对比指标** |
| `TMR-nsim.yaml` | TMR strict non-similar split | **主要对比指标** |
| `TMR-guo.yaml` | TMR strict Guo-style | 与 TMR 论文可比 |
| `TMR-threshold_0.95.yaml` | TMR strict 过滤 | 去重 |
| `TMR-temporal-normal.yaml` | 时序感知 retrieval（CAR/TAR） | 时序能力 |
| `TMR-temporal-nsim.yaml` | 时序感知 nsim | 时序能力（harder） |
| `EVT-normal.yaml` | Event-level temporal diagnostics（full set） | **时序诊断核心** |
| `EVT-nsim.yaml` | Event-level temporal diagnostics（nsim） | **时序诊断核心** |

**PrimaryScore 定义：**
```
PrimaryScore = mean(TMR-normal R@1, TMR-normal R@5, TMR-nsim R@1, TMR-nsim R@5) 
               across t2m + m2t (8 个值的平均)
```

**⚠️ 与 generation 论文对齐时的指标解释：**
- `guo.yaml` / `TMR-guo.yaml` 的 `R-Precision` 属于 Guo-style batched matching（通常 batch=32），衡量的是“小批次候选里是否语义匹配”
- 这与 `TMR-normal` / `TMR-nsim` 的 full-gallery retrieval `R@K` 不是同一指标，因此不能把 PRISM 这类 generation 论文的 `R-Precision Top-3` 直接解读为对 TAMR retrieval 的“横扫”

**时序诊断指标（EVT-*）：**
- CAR@K：Chronologically-Accurate Retrieval（event 顺序正确的 retrieval）
- TAR@K：Temporal-Aware Retrieval（所有时序约束的 retrieval）
- DIAG 细分：ordering / before / after / negation / duration / existence / before_after
- margin：positive_score - hardest_negative_score（越大越好）

---
## 二、实验现状：数值全景

### 2.1 Retrieval PrimaryScore 排行（HumanML3D-E strict regime）

| Checkpoint | TMR-normal avg | TMR-nsim avg | PrimaryScore | 状态 |
|---|---:|---:|---:|---|
| **ref00_s43** | **17.81** | **73.20** | **45.50** | REF00 50 epoch, seed=43，当前最高 |
| ref00_s41 | 18.30 | 72.42 | 45.36 | REF00 50 epoch, seed=41 |
| stage2_gt B0 | 18.26 | 71.39 | 44.83 | HumanML3D keyids 训练 |
| **REF00 4-seed mean** | — | — | **44.75 ± 0.79** | working baseline（s41/s42/s43/s44） |
| ref00_s42_70 | 17.80 | 71.39 | 44.60 | seed=42, 70 epoch，较 s42 +0.61 |
| **S2E-v2** | **18.12** | **70.88** | **44.50** | HumanML3D-E keyids，从零训练 ✅ |
| ref00_s44 | 18.45 | 69.85 | 44.15 | REF00 50 epoch, seed=44 |
| D2b (tmr_transfer) | — | — | 44.03 | tmr_transfer full unfreeze |
| ref00_s42 | 17.60 | 70.36 | 43.98 | REF00 50 epoch, seed=42 |
| S2E+T | 18.34 | 69.59 | 43.97 | S2E-v2 + evt_align(0.2)，退化 |
| D1 (frozen) | — | — | 43.69 | tmr_transfer frozen backbone |
| pretrained B0 | 17.99 | 69.07 | 43.53 | 纯 pretrained ViT，无 event 训练 |
| ~~S2E~~ | ~~17.99~~ | ~~67.53~~ | ~~42.76~~ | ~~warm-start 退化，已废弃~~ |

**关键观察：**
- `REF00` 4-seed (50 epoch) 已经足够作为 **working baseline**：mean = `44.75`，std = `0.79`
- 但 variance 仍然偏大，意味着 `< +0.8` 的改进不能轻易宣称为“显著优于 baseline”
- `s42 → s42_70` 的提升为 `+0.61`，说明 50 epoch 对部分 seed 可能略短，但还不足以支持“立即把全体 baseline 改成 70 epoch”

### 2.1.1 相对 `pretrained B0` 的改动说明

这里的 `pretrained B0` 指的是 **原始 MotionPatches pretrained checkpoint**，本身没有 TAMR 的 event-aware 训练改动；后面的三组实验都不是“只换一个 eval 开关”，而是在训练阶段引入了额外修改。

- `pretrained B0`：训练索引来自 `HumanML3D` 默认 train/val split。当前表格里引用的是它在 `HumanML3D-E strict eval regime` 下的**重评结果**，不是在 `HumanML3D-E` keyids 上重新训练后的结果。
- `stage2_gt B0`：在 MP 原始 backbone 上开启 `event_temporal` 训练分支，加入 `event CLIP loss + temporal hard negative loss`，event source 使用 `HumanML3D-E` 的 GT events；但训练样本 keyids 仍然来自 `HumanML3D` 默认 train/val split，不是 `HumanML3D-E` keyid split。
- `S2E-v2`：保留 `stage2_gt B0` 的 event-aware loss 设计，同时把训练 regime 显式切到 `HumanML3D-E` keyid split（`train.dataset_regime=humanml3de`）；另外去掉了早期 `S2E` 的 warm-start 路径，不再从已有 MP retrieval checkpoint 继续训，而是直接在 MP backbone 初始化下重训。
- `S2E+T`：以 `S2E-v2` 为基础，再额外打开 `tmr_event_head`（`evt_align` 辅助 loss，weight=`0.2`），也就是在 `event CLIP + temporal negatives` 之外，再叠加一个 TMR 风格的 temporal grounding 分支。

因此，这三组实验相对 `pretrained B0` 的关系不是同一级别的简单横排：
- `stage2_gt B0` = `pretrained B0` + event-aware losses
- `S2E-v2` = `stage2_gt B0` + HumanML3D-E keyid training regime + 去掉 warm-start
- `S2E+T` = `S2E-v2` + TMR event head / `evt_align`

按**训练索引来源**重新分组，更准确的划分应是：
- `HumanML3D` 默认 keyids 训练：`pretrained B0`、`stage2_gt B0`
- `HumanML3D-E` keyids 训练：`S2E-v2`、`S2E+T`、后续 `REF00`

### 2.2 时序诊断指标对比（EVT-normal）

| Metric | pretrained B0 | S2E-v2 | S2E+T | Delta (S2E-v2 vs B0) |
|---|---:|---:|---:|---:|
| CAR@1 | 6.14 | 8.65 | 9.57 | +2.51 |
| CAR@5 | 21.47 | 29.95 | 30.74 | +8.48 |
| TAR@1 | 3.95 | 4.89 | 5.72 | +0.94 |
| TAR@5 | 12.84 | 17.56 | 18.85 | +4.72 |
| TAR@10 | 18.11 | 25.14 | 26.24 | +7.03 |
| CAR_margin | 0.0372 | 0.3592 | 0.3635 | +0.3220 |

### 2.3 时序诊断指标对比（EVT-nsim，harder）

| Metric | pretrained B0 | S2E-v2 | S2E+T |
|---|---:|---:|---:|
| CAR@1 | 48.48 | 66.67 | 64.58 |
| CAR@5 | 75.76 | 93.75 | 89.58 |
| TAR@1 | 19.00 | 26.80 | 27.84 |
| TAR@5 | 34.00 | 44.33 | 45.36 |
| DIAG_ordering@1 | — | 43.75 | 35.42 |
| DIAG_before@1 | — | 62.50 | 62.50 |
| DIAG_duration@1 | — | 27.84 | 32.99 |

### 2.4 现状一句话总结

> S2E-v2 在时序诊断指标上相比 pretrained B0 有显著提升（CAR@1 +18.19 on nsim），但在主 retrieval 指标上仅 +0.97。这说明 event-aware contrastive learning 确实让模型学到了时序信号，但这些信号没有有效转化为 retrieval ranking 的改善。

### 2.5 REF00 的当前定位

`REF00` 现阶段应被视为 **working baseline**，而不是最终冻结的 paper baseline。

- working baseline 的职责：为 Step 3.1 smoke / Step 3.2 input ablation 提供 paired comparison
- final baseline 的职责：论文中报告的最终参考数字，需要在主方案确定后再结合 bootstrap CI、可能的 epoch-length 对照后冻结
- 当前判断：`REF00` 已经足够支撑下一步实验，但还不适合用来对 `< +0.8` 的增益做强结论

---
## 三、根因分析：为什么 MP 适配没有显著增益？

### 3.1 核心矛盾

TMR 上的适配（Phase 1 D2b）显著改善了 retrieval（normal t2m R@1: 9.46→15.54），但 MP 上的适配（S2E-v2 vs pretrained）仅 +0.97 PrimaryScore。根因有六层：

### 3.2 根因 #1：Auxiliary temporal objective 与 final retrieval scoring 的结构性错位

这是最核心的根因，最能解释"temporal diagnostics 明显涨了，但主 retrieval 只涨 +0.97"这个现象。

- temporal objective（event CLIP / temporal hard negative）优化的是"区分时序正确/错误文本"的能力
- 但 standard retrieval 的 hard cases 更多来自**语义相近动作、局部姿态差异、文本歧义、数据噪声**
- 因此 temporal gain 不一定能强转化为 R@K 改善 — 两个目标的 hard case 分布不同
- TMR event head 更极端：它只优化 `time_tokens → event_proj_t` 这条路径，而最终检索依赖的是 `pool_tokens → motion_projection` 的全局 embedding。两条路径共享 ViT 主干，但不共享最后的评分头，因此 temporal head 学到的局部对齐能力不一定能转化为 global ranking 改善
- **S2E-v2 的 event CLIP loss 之所以相对有效**：因为它直接在 retrieval 空间做 `event_embeds @ motion_embeds.T`，梯度流过 `motion_projection`，与 final scoring function 同构
- ⚠️ 注意：event CLIP loss 已部分缓解了这个问题（它直接优化 retrieval 空间），因此后续 roadmap 的优先级转向 #2/#3 的机制性改动

### 3.3 根因 #2：ViT 缺乏显式时序归纳偏置

- ViT 将 motion 切成 14×5 的 patch grid，时序信息被编码在 14 个时间 bin 的 positional embedding 中
- 但 ViT 的 self-attention 是全局的（所有 70 tokens 互相 attend），没有显式的时序归纳偏置
- 纯 loss 层面的改动不足以重塑 ViT 的时序处理方式
- 这是直接的机制性根因：模型架构缺少强显式时序归纳偏置（absolute PE 提供了弱时序位置信号，但不足以支撑 event-level 的时序区分）

### 3.4 根因 #3：当前设计没有改变 motion 表征本身

- 所有改动都在 loss 层面（event CLIP、temporal hard negative、TMR event head）
- motion encoder 的架构、输入表示、tokenization 方式完全没变
- MP 的 motion patch 只保留位置信息，丢失了速度/加速度/旋转 — 时序动态信息被隐式编码在相邻帧差异中
- 模型学到的时序信号体现在 embedding 空间的微调上，但没有改变 ViT 如何"看"motion
- 外部证据也支持这一判断：PRISM (arXiv'26) 在 generation 场景下仅通过 per-joint latent decomposition、几乎不改生成器，即获得大幅提升
- generation ≠ retrieval，但该结果至少说明 motion tokenization / representation 不是次要工程细节；对 TAMR 来说，Step 3.2 应被视为主线，而不是“有空再做的 input ablation”

### 3.5 根因 #4：MP 的 pretrained baseline 已经很强（headroom 限制）

- MP pretrained B0 PrimaryScore = 43.53，TMR Phase 1 D1 frozen 的 normal t2m R@1 仅 9.46
- MP 用 ViT-Base（85M params）+ ImageNet pretrained，TMR 用 ACTOR（~2M params）从零训练
- MP 的 embedding 空间已经被 ImageNet 预训练 + CLIP loss 充分塑造，event loss 的边际增益自然更小
- 这更像 headroom 限制而非直接机制性根因，但它解释了为什么同样的 loss trick 在 TMR 上涨幅更大

### 3.6 根因 #5：文本侧对 event structure 的利用不足

- 当前文本端是单向 global caption embedding（DistilBERT [CLS]）+ event text 作为 auxiliary（见 `clip.py` L53, L671）
- 但最终 ranking 仍主要受 global text embedding 限制
- 如果文本端没有显式建模 event composition / relations，motion 端再时序化，收益也可能被文本端瓶颈压住
- 需要区分“结构不足”和“规模不足”：generation 模型上 T5 / LLM2Vec / Qwen-style 大 text encoder，多是为了提供 token-level conditioning；TAMR 主检索更关心低成本 global embedding 与判别几何
- 因此当前更合理的假说不是“DistilBERT 太小”，而是“文本端没有显式建模 event composition / relations”
- ⚠️ 这仍是合理假说，尚无 text-side ablation 实验支撑

### 3.7 根因 #6：Temporal supervision 的有效样本密度不高

- K=1 占 50.70%（corrected D0 全量口径，83347 captions）— **超过一半的 caption 没有真正的 event ordering signal**
- Train split K=1 ≈ 52.0%（34673/66636），意味着训练集中有效 temporal supervision 的样本不到一半
- ⚠️ corrected D0 已 supersede 旧 D0（938 条 eval split），所有统计以 corrected D0 为准
- `temporal_utils.py` 中 `relation_sensitive_negatives` 实际上硬设 `relation_types = ["before"] * (len(events)-1)`（L453），并没有从 GT relation 中读取真实的 before/after/overlap 关系
- `parallel_to_sequential`、`causal_reversal` 默认关闭（L432, config.yaml L48），`existence negatives` 主要用于 diagnostic（L506）
- 因此"6 类负样本已稳定用于训练"的表述偏理想化，实际有效的负样本类型更少

**⚠️ 评测集局限：** nsim 只有 97 条样本，单个样本 ≈ 1.03%。很多"提升/退化"在统计上很脆弱，不宜用小样本子集支撑强因果判断。

### 3.8 MP 架构能力上限

**上限未知，当前实现未充分释放其潜力。**

- Beyond Static Scenes (2025) 采用 motion patch 表征做 generation，但 generation ≠ retrieval（generation 看 conditional synthesis capacity，retrieval 看 embedding geometry / ranking discrimination），不能直接类比
- MP 的 14×5 patch grid 天然提供了时间-空间分解，理论上适合时序建模
- 但表示的 expressiveness、backbone 的 inductive bias、pooling 方式、training objective 都影响最终 retrieval ceiling
- 更稳妥的结论：**没有证据表明 Motion Patch 表示本身构成硬上限，但也没有足够证据证明其在 temporal retrieval 上的能力上限很高**

---
## 四、ICLR 可行性判断

### 4.1 当前贡献盘点（诚实评估）

| 维度 | 现状 | ICLR 标准 | 差距 |
|---|---|---|---|
| 方法创新 | 在 MP 上加 event CLIP loss + temporal hard negatives | 需要 representation/architecture 级创新 | **大** |
| 实验增益 | PrimaryScore +0.97（44.50 vs 43.53） | 需要显著且一致的提升 | **大** |
| 时序能力 | CAR/TAR 有显著提升 | 需要新 benchmark + 新指标被社区认可 | 中 |
| 数据贡献 | 使用 HumanML3D-E（已有） | 需要新数据集或显著扩展 | 中 |
| 分析深度 | 详细的 ablation 和诊断 | 需要 insight 驱动的设计 | 中 |

### 4.2 ICLR 的核心门槛

ICLR 2027 对 motion-text retrieval 论文的隐含要求：
1. **不能只是 "stronger backbone + more hard negatives"** — 这是 reviewer 最容易给的批评
2. 需要至少一个 **representation-level 或 architecture-level 的新设计**，而不仅是 loss engineering
3. 需要在 **标准 benchmark 上有显著且一致的提升**，不能只在自定义指标上好
4. 需要 **新的 insight**：为什么现有方法不行，你的方法为什么行，机制是什么

### 4.3 判断：当前状态距 ICLR 有多远？

**当前状态明显不够。** idea 具备继续挖掘价值，但其 top-tier ceiling 仍未被证明。

**idea 上限不足的证据（如果只停留在当前设计）：**
- S2E-v2 本质上是 "MP + event CLIP loss + temporal hard negatives"，没有 architecture 创新
- PrimaryScore +0.97 不足以支撑一篇 top venue 论文
- 时序诊断指标的提升虽然显著，但 CAR/TAR 不是社区公认的标准指标

**需要明确的外部校准（PRISM）：**
- PRISM 是 motion generation 结果，不是 motion-text retrieval；其 HumanML3D `R-Precision Top-3` 属于 Guo-style batch matching，不等于 TAMR 的 full-gallery `R@K`
- 因此 PRISM 不会 scope 掉 TAMR 的问题定义；它对 TAMR 的真正冲击是强化了“表征设计可能比 loss trick 更重要”这一判断

**idea 有继续挖掘价值的证据：**
- "temporal-aware motion-text retrieval" 是一个真实且未被充分解决的问题（ChroAccRet ECCV'24 证明了这一点）
- MP 的 14×5 patch grid 天然适合时序建模，但当前完全没有利用这个结构
- PST (arXiv'26) 占据了 spatial fine-grained，temporal-specific fine-grained retrieval 仍然稀缺、尚未形成强共识方案（但不能说是空白 — ChroAccRet 已进入这个叙事）

**是否能支撑 ICLR 取决于后续是否出现"标准指标上的稳定提升 + 明确的新机制"。** 如果后续只能拿到 < +1.0 的 standard retrieval gain，应转向 benchmark + diagnosis 定位或 workshop/datasets-benchmark track。

### 4.4 达到 ICLR 标准需要什么？

需要同时满足以下 3 条：

1. **Architecture 创新**：一个利用 MP 14×5 patch grid 的时序感知模块（不是简单的 adapter，而是改变 ViT 如何处理时序信息）
2. **显著实验增益**：基于 3-seed mean ± std 的统计门槛
   - 可信改进门槛：3-seed mean PrimaryScore 相对 S2E-v2 提升 ≥ 0.5，且 normal/nsim 双不退化
   - 论文竞争力门槛：3-seed mean PrimaryScore ≥ 45.3 且 temporal 指标同步稳健提升
   - Kill-switch：如果 3-seed mean 提升 < 0.3 且 temporal 指标无显著改善 → 停止当前方案，转下一个候选或转轨 benchmark 定位
   - ⚠️ 45.0-45.2 区间的决策规则：如果 3-seed mean 落在此区间，看 temporal 指标是否有 ≥ 5% 的 CAR@1 提升；如果有，继续叠加模块；如果没有，转轨
3. **新 benchmark 贡献**：temporal-aware retrieval benchmark + 诊断指标体系，让社区可以复用

**额外必须防御的威胁：**
- 更强 backbone baseline（ViT-Large/16、DINOv2 pretrained）可能不改结构就涨 1-2 分 → 必须跑 sanity baseline
- 离散 token 系列（MotionGPT、T2M-GPT、MoMask）在表示学习层面构成替代路线 → 论文需要讨论为什么选择 continuous patch 而非 discrete token
- LaMP 在 retrieval 上是明确竞争者 → 必须作为 baseline 对比

---
## 五、后续 Roadmap (Step-by-Step)

### 总体策略

当前所有改动都在 loss 层面，这是增益有限的根因。后续路线必须同时触及 **motion 表征**、**ViT 架构** 和 **文本侧结构**。受 PRISM 外部证据影响，**motion 表征不再视为普通 input ablation，而是与 temporal inductive bias 并列的主线**；但执行顺序上仍保持 Step 3.1 先 smoke，因为它是最小结构改动、最快验证 architecture story 的入口。优先级原则：**最小结构改动优先，augmentation / loss trick 后置**。

### 路线更新（基于 REF00 4-seed 结果）

基于 `ref00_s41/s42/s43/s44` 的严格评测，路线执行顺序更新如下：

1. **现在就进入 Step 3.1**：`REF00` 已足够作为 working baseline，不再等待 baseline variance 或 epoch-length 问题完全解决
2. **Step 3.1 先做 1-seed smoke**：使用 `seed=41` 做 paired comparison，优先验证方向是否值得投入多 seed
3. **70 epoch 暂不全局替换 baseline**：`s42_70` 只是说明 50 epoch 对部分 seed 略短，不足以支持立即把全体 baseline 改成 70 epoch
4. **Step 3.0 的 "and" 审计 / ViT-Large sanity baseline 可以并行推进**，但不阻塞 Step 3.1 smoke
5. **若 Step 3.1 仅弱阳性，则前置 Step 3.2**：PRISM 已提供外部证据支持 representation 主线，此时不应先堆 text encoder 或 augmentation

### Phase 3: Representation + Architecture Enhancement

#### Step 3.0: 数据质量审计 + Baseline 对齐（3-5 天）⚠️ 最高优先级
**目的：** 确保后续实验建立在干净的数据和可靠的 baseline 基础上。当前数据质量与 supervision density 可能是与架构问题同等级的重要瓶颈，而不是次要噪声源。

**具体动作：**
1. 检查 HumanML3D-E 的 "and" 并列处理：抽样 200 条含 "and" 的 caption，验证 event 分解是否正确区分了并列（"walking and waving" = 并行）vs 顺序（"walk and then sit" = 先后）
2. 审计 `temporal_utils.py` 的实际负样本覆盖：确认 `relation_sensitive_negatives` 是否真的读取 GT relation（当前实现硬设 `["before"] * (len(events)-1)`），`parallel_to_sequential` / `causal_reversal` 是否默认关闭
3. 统计有效 temporal supervision 密度：K≥2 且有可靠 event ordering 的样本实际占比
4. **Sanity baseline**：跑 ViT-Large/16 或更强 ImageNet pretrained backbone 的纯 CLIP baseline，确认 architecture 改动的增益不会被简单换 backbone 抹平

**Gate：** 如果 >15% 的 "and" 被错误处理为顺序，则需要修复后再继续。如果 ViT-Large baseline 直接超过 45.0，则需要重新评估 architecture story。

**ViT-Large 资源假设：** ViT-Large/16 约 304M params，单卡 24GB 可能需要缩减 batch size 或梯度累积。如果显存不足，默认使用 gradient accumulation (effective batch = 128) + mixed precision。1-seed sanity 可在 3-5 天内完成，但若需作为 story-defending baseline（3-seed），预留额外 3-5 天。

#### Step 3.1: 最小结构改动 — Temporal Inductive Bias（3-5 天）⭐ 核心优先
**目的：** 给 ViT 注入时序归纳偏置，这是 architecture 创新的核心。应最先尝试。

**方案优先级排序（基于复查反馈调整）：**

**首推 — 方案 B: Temporal-Spatial Decomposed Relative Position Encoding**
- 在 ViT 的 attention 中叠加 decomposed relative position bias（additive attention bias）
- 时间维度用 1D relative position bias（类似 ALiBi 或 RoPE），空间维度（5 body parts）用 learnable bias
- 让模型能区分 "同一时刻不同部位" vs "不同时刻同一部位"
- 实现策略：**第一版保留 abs PE + 叠加 rel bias**（timm Attention 已支持 attn_mask，可作为 additive bias 传入），跑通后再 ablate 纯 rel bias。对新 bias table 用更小 lr 或短 warmup
- 优点：直接作用于 attention 几何，不引入 train-test mismatch，不依赖 event boundary
- 风险：需要修改 timm attention forward，debug 和兼容 checkpoint 需要时间；但不需要重写 qkv

**Step 3.1 的最新执行策略（2026-04-15 update）：**
- **smoke seed**：固定 `seed=41`
- **最小实验集**：先跑两个新配置
  1. `abs_only_new_impl`：使用新 attention 实现，但关闭 relative bias，用于控制“代码路径变化”的影响
  2. `abs_rel`：主配置，保留 absolute PE 并叠加 decomposed relative bias
- **后置 ablation**：`rel_only` 不作为首轮必跑项；仅当 `abs_rel` 落在灰区或与机制指标出现矛盾时再补
- **Step 3.0 parallel work**：在 smoke 运行期间并行完成 "and" 审计与 negative coverage audit

**次选 — 方案 D: Temporal Convolution / Depthwise Temporal Mixer（新增）**
- 在 ViT block 前/后加轻量 temporal mixer：只沿 14 个 time bins 做 1D depthwise conv 或 MLP mixing，再与原 token 残差相加
- 优点：极简，几乎无额外标注需求，对 14 bins 离散时间结构特别合适
- 风险：可能增益有限

**备选 — 方案 E: Event-Conditioned Adapter（新增）**
- 不改整个 ViT attention，而是在 block 内注入小 adapter，adapter 由 event summary embedding 控制
- 参数量小，易于 ablation，更像 ICLR reviewer 可接受的"机制型改动 + 可控复杂度"

**降级 — 方案 C: Temporal Segment Embedding**
- ⚠️ 存在明显 train-test mismatch：训练用 GT event boundary，推理时无 GT
- 如果坚持做，建议改成 soft segment prior（连续 event-position bias），训练时也随机扰动边界让模型适应 boundary noise
- 不建议作为首推方案

**降级 — 方案 A: Temporal Causal Attention Mask**
- Retrieval 不是 autoregressive prediction，因果 mask 强行禁止看未来，可能损害对整段动作的双向理解
- 更适合 generation / online modeling，不一定适合离线 retrieval embedding

**当前不优先采用的相关方向（2026-04-15 addendum）：**
- **完整 Conformer**：当前阶段**不建议上**。Conformer 的价值主要来自 self-attention + depthwise conv 的结合，但在 MP 的 `14 × 5` patch grid 上，完整替换 12 层 ViT block 的成本过高，而且会破坏 ImageNet pretrained 权重的兼容性。若方案 B 失败，优先试 **方案 D**，它本质上是 Conformer 的“最小有效子集”。
- **直接搬用 Qwen-VL / Qwen2-VL 的 M-RoPE**：当前阶段**不建议直接上**。M-RoPE 的 2D/3D 分解思路值得借鉴，但直接替换 ViT 的 absolute PE 机制会削弱 pretrained abs PE 的迁移价值，实现复杂度也明显高于 additive rel bias。
- **潜在后续升级路线**：如果方案 B（additive rel bias）表现出明确的时序机制正信号但 ranking gain 不够强，可在第二阶段考虑：
  1. `abs PE + 2D RoPE` 叠加方案（保留 pretrained abs PE，再引入时空分解 RoPE）
  2. `MADPE`（Motion-Aware Decomposed Position Encoding）：temporal 维度用 RoPE，spatial 维度用 body-part graph bias
- **优先级结论**：当前执行顺序仍保持 `B -> D -> E`。RoPE 变体和 MADPE 都属于方案 B 验证后的增强版，不应阻塞第一轮 smoke。

**Step 3.1 smoke gate（1-seed, seed=41）：**
- `PrimaryScore delta > +1.0`：**Strong signal**，立即补多 seed
- `PrimaryScore delta ∈ [+0.3, +1.0]`：**Weak positive**，必须同时满足以下至少一条才继续：
  - `EVT-nsim CAR@1 +5pp`
  - `DIAG_ordering@1 +5pp`
  - `CAR_margin +0.05`
- `PrimaryScore delta ∈ [-0.8, +0.3]`：**Inconclusive**，若 temporal diagnostics 也无改善，则转方案 D
- `PrimaryScore delta < -0.8`：**Negative**，停止方案 B，转方案 D

**Step 3.1 final gate（3-seed mean，供后续主实验使用）：**
- `ΔPrimaryScore ≥ +0.5`：可信改进
- `ΔPrimaryScore ≥ +0.8`：论文竞争力信号

**必要 ablation（方案 B）：**
- 首轮 smoke：`abs_only_new_impl` / `abs_rel`
- 条件补充：`rel_only`（仅在 `abs_rel` 弱阳性或灰区时补）
- 论文阶段仍需报告完整的 `abs only / abs+rel / rel only` 三组对比，防御 reviewer 的"是不是只是多加了一个 positional signal"

#### Step 3.2: Motion Representation Enhancement（2-4 天）⭐ 第二优先
**目的：** 改善 motion 输入本身的时序信息密度与运动学对齐。PRISM 的 per-joint latent decomposition 说明表示粒度可能是决定性变量，因此这一步不再被视为普通 input ablation。

**具体设计：**
1. **增加 velocity / acceleration channels**：当前 motion patch 只有位置 (x,y,z)，3 通道。增加帧间速度差分和加速度差分，变为 9 通道（pos + vel + acc）
   - 权重初始化策略：前 3 个位置通道继承 ImageNet pretrained patch embedding 权重，新增 6 个 vel/acc 通道零初始化或小方差初始化（或用 timm 的 `in_chans=9` 适配，它会复制并缩放 RGB 权重）
   - ⚠️ vel/acc 的分布与 pos 不同，**必须重做归一化口径**（当前 `dataset.py` L145, L237 的 mean/std 只针对 3 通道位置）
   - 需要修改：`dataset.py` 的预处理、`clip.py` L70 的 ViT 初始化、归一化统计量
2. **增加 root trajectory / facing direction channel**：参考 Kimodo 的 smoothed root + heading 表示
3. **Multi-stream motion encoder**：position stream + velocity stream，各自过 ViT 后 late fusion（成本较高，作为备选）
4. **Kinematic-aware finer tokenization（PRISM-inspired，新增）**：在不引入生成式 VAE 的前提下，把当前 5 条大运动链的 coarse grouping 细化为更贴近运动学树的 spatial bins（如 root / torso / limbs / 更细 joint groups），做一个 lightweight 对照，验证“更细粒度 + 运动学对齐 tokenization”是否改善 retrieval geometry
   - 目标不是复刻 PRISM 的生成潜空间，而是把“per-joint decomposition matters”转写为 retrieval-friendly 的 tokenization ablation

**优先级：** 方案 1 最轻量；若 Step 3.1 只有 weak positive，优先把方案 1 + 方案 4 前置，而不是先做 augmentation

#### Step 3.3: Event-to-Time Cross-Attention / Soft Alignment（3-5 天）
**目的：** 替代原 blockwise hard alignment 设计。原 blockwise loss 有严重实现难点（没有可靠的 event-to-time boundary supervision，event 数 K 与 time bins 14 粒度不匹配），改为 soft alignment。

**具体设计：**
1. **Event-to-Time Cross-Attention**（首推）：
   - 文本 event tokens 作为 query，time-bin tokens 作为 key/value
   - 得到 event-aware pooled motion representation
   - 再把这些局部表示与 global score 融合
   - 优点：不必硬把 GT event boundary 塞进 motion tokens，不要求 train/test 一致的边界标签
   - ⚠️ 推理路径问题：推理时没有 GT events，需要先对 query text 做 event decomposition。当前 `temporal_utils.py` L78 的 fallback 分解器对 "and" 是启发式切分，对并行/重叠关系不可靠。**解决方案**：改为从 raw caption 内部学 latent event queries（类似 DETR 的 object queries），不依赖外部 event decomposition；或者明确降级为 reranker 而非主检索主干
2. **Monotonic Soft Alignment**：
   - 用 monotonic attention prior（event 1 偏向前面的 time bins，event K 偏向后面的 time bins）
   - 不做 hard block boundary，而是 soft alignment over 14 time bins
3. **Dual-Head Scoring**（备选，更稳）：
   - 保留 global retrieval head，同时增加 temporal consistency reranker
   - 第一阶段 global retrieval，第二阶段 top-K temporal rerank
   - 推理时不需要 event decomposition，只需要 global query + reranker 内部处理

#### Step 3.4: Text Encoder 升级（2-3 天，可与 3.1 并行）
**目的：** 解决文本侧对 event structure 利用不足的瓶颈，同时避免把 generation 里的“大 text encoder”误当成 retrieval 主线。

**策略原则：**
- generation 论文上 T5 / LLM2Vec / CLIP-L + Qwen 这类大 text encoder，主要是为了提供 token-level conditioning 给 DiT / cross-attention，且每个 prompt 只编码一次，成本可接受
- TAMR 主检索的瓶颈更可能是 global embedding 的判别几何与 event structure 缺失，而不是单纯 encoder 参数量；query 侧还对延迟敏感
- 因此短期保持 DistilBERT 主干，优先做结构升级；更大 encoder 只作为受控对照或 reranker 方向
- 从 HY-Motion 真正值得借鉴的不是“换 Qwen”，而是双层文本条件（global + fine-grained）；对 TAMR 可映射为 global caption + event-level dual-granularity representation

**候选方案：**
1. **Event-Structured Text Encoding**（首推）：分别编码每个 event，再用 Transformer 聚合 event embeddings，保留 event 结构信息
2. **Hierarchical Text Encoding**：global caption embedding + event-level embeddings 的双层结构
3. **Encoder-only 升级（BERT-large / DeBERTa-v3）**：作为受控对照，验证“文本侧是否真是瓶颈”，仍保持 encoder-only 与检索推理成本可控
4. **LLM2Vec / Qwen-style encoder**（最后考虑）：仅在 text side 被证实为瓶颈时再上，且优先用于 top-K reranker、离线分析或数据预处理，而非主检索主干

#### Step 3.5: Temporal Augmentation（1-2 天，在结构改动有正信号后再加）
**目的：** 在数据层面增强时序信号。注意：文档自己已得出"只改 loss 收益有限"，因此 augmentation 不应是最先尝试的方向。

**具体设计：**
1. **Patch Shuffle Augmentation**：训练时随机打乱 14 个时间 bin 的顺序，作为负样本
2. **Temporal Crop & Stitch**：构造 "前半段 A + 后半段 B" 的合成样本

#### K≥2 Supervision Density Mitigation（贯穿 Phase 3-4）
**背景：** corrected D0 显示 train split K=1 ≈ 52%，超过一半的训练样本没有 event ordering signal。这直接限制了 temporal loss 的有效梯度密度。

**三选一 mitigation（至少实施一项）：**
1. **Temporal loss 仅对 K≥2 样本生效**：K=1 样本只参与 global CLIP loss，不参与 event CLIP / temporal hard negative loss
2. **K≥2 样本上采样**：在 dataloader 中对 K≥2 样本 2x 上采样，提高 temporal supervision 密度
3. **单独报告 K≥2 子集结果**：在所有 eval 中额外报告 K≥2 子集上的 PrimaryScore / CAR / TAR，作为 temporal capability 的更纯净度量

#### Step 3.6: 新指标设计 & Benchmark 构建（3-5 天）
**目的：** 为论文提供独特的 evaluation 贡献。

**设计：**
1. **Temporal Retrieval Benchmark (TRB)**：从 HumanML3D-E 中筛选 K≥2 event 的样本，标准化评测协议
2. **TAR@K 标准化**：已有初步实现，需要标准化定义
3. **Temporal Discrimination Score (TDS)**：mean(positive_score - hardest_negative_score)

### Phase 4: 实验验证 & 论文准备

#### 实验硬要求（贯穿 Phase 4）
- **Multi-seed**：所有关键实验必须跑 3 seeds，报告 mean ± std。nsim 只有 97 条样本，单 seed 结果不具备统计功效
- **Paired Bootstrap CI**：对 normal 和 nsim 查询分别重采样，重算 PrimaryScore delta，报告 95% CI 和 P(delta>0)。对 nsim 这种 97 条的小集，这是必要项，不是可选项。3-seed std 只反映训练随机性，不反映 test-set sampling uncertainty
  ```
  Bootstrap protocol:
  - resample unit: query id (not motion-caption pair)
  - B = 10000
  - procedure: for each bootstrap iteration, sample query ids with replacement per split,
    compute paired delta (method - baseline) on sampled queries, aggregate split deltas
    into PrimaryScore delta
  - report: percentile 95% CI and P(delta > 0)
  - aggregation: first compute 3-seed mean per query, then bootstrap over queries
  ```
- **Params/FLOPs 控制**：每个新增模块必须报告额外参数量和 FLOPs 增量，防御 reviewer 的"你只是加了模块"批评。目标：额外参数 < 5% of ViT-Base (< 4.3M)

#### Step 4.1: 主实验（5-7 天）
- 在 Step 3.1 的最佳方案上，跑完整的 train + eval
- 对比：pretrained B0 / ViT-Large baseline / S2E-v2 / Step 3.1 best / TMR baseline / LaMP
- 在 TMR-normal, TMR-nsim, EVT-normal, EVT-nsim, TRB 上全面评测

#### Step 4.2: Ablation 实验（3-5 天）
- 逐个 ablate：temporal position encoding / motion representation / event cross-attention / text encoding / augmentation
- 证明每个组件的独立贡献

#### Step 4.3: 论文写作（7-10 天）
- 核心叙事（目标叙事，待 ablation 验证后定稿）："TAMR 通过在 motion patches 上引入时空分解的 attention bias 与显式运动动态通道，把对时序顺序不敏感的 ViT retrieval encoder 变成 temporally-aware motion-text retriever。"
  - ⚠️ 若最终只有方案 B 有效而 repr enhancement 无效，叙事需调整为单一 attention bias story
- **Motivation 段落（论文必须包含）**：现有 motion-text retrieval 模型对时序顺序不敏感（temporally under-sensitive）。例如："walk forward then sit down" 与 "sit down then walk forward" 在现有 embedding 下几乎无法区分；"raise hand while walking" 与 "raise hand then walk" 的 before/while 关系被忽略。这不是边缘 case — corrected D0 显示 49.30% 的 caption 包含 K≥2 events，时序关系是 motion description 的核心组成部分。
  - **必须补充的真实证据（Step 4.1 前完成）**：用 pretrained B0 跑 1-2 个真实 failure case，报告 ordering-swapped pair 的 cosine similarity 差异、top-5 retrieval ranking 对比、以及 best TAMR 模型在同一 case 上的改善。这是论文 motivation figure 的素材。
- 必须显式讨论：PST 正交性、LaMP 对比、discrete token 替代路线、stronger backbone sanity check

### 时间线估算（修正为 9-12 周，单人推进）

```
Week 1-2:  Step 3.0 (数据审计 + ViT-Large sanity baseline)
Week 3:    Step 3.1 smoke (seed=41, abs_only_new_impl + abs_rel) + Step 3.0 parallel audit
Week 4:    如果 smoke 有正信号，补 Step 3.1 multi-seed + 条件性 rel_only ablation；若仅 weak positive，同步前置 Step 3.2(1/4)
Week 5:    Step 3.2 (motion representation, vel/acc + tokenization ablation) + Step 3.4 (text encoder, 并行)
Week 6:    Step 3.3 (event cross-attention / soft alignment) + Step 3.5 (augmentation, 如有正信号)
Week 7-8:  Step 3.6 (benchmark) + Step 4.1 (主实验 3-seed) + Step 4.2 (ablation)
Week 9:    Bootstrap CI + 统计验证
Week 10-12: Step 4.3 (论文写作)
```

**最早可写论文触发点：** 只有在 Step 4.1 完成后，且已有 3-seed 主结果、ViT-Large sanity、不少于 2 个核心 ablation、以及 PrimaryScore delta 的 bootstrap 95% CI 不跨 0，才进入写作。按当前时间线，最早 Week 8 末可以开写初稿，稳妥是 Week 9。

---
## 六、关键问题逐条回答

### Q1: 对比学习的负样本是否包含 event 乱序构造的负样本？

**更准确的说法是：当前训练里确实包含 event 乱序类负样本，但“6 类都稳定生效”这个说法过强。**
1. 已明确可用：ordering shuffle、reverse order
2. 部分可用：negation insertion、duration modification
3. 需审计：relation-sensitive negatives 目前没有读取 GT relation，而是硬设 `before`
4. 主要用于 diagnostic 或默认关闭：existence negatives、`parallel_to_sequential`、`causal_reversal`

因此，S2E-v2 的 temporal hard negative 确实不是空的，但负样本覆盖没有此前表述得那么完整；这正是 Step 3.0 的审计重点。

### Q2: MP 的 text encoder 是否基于 pretrained TMR？

**不是。** MP 的 text encoder 是标准 `distilbert-base-uncased`（HuggingFace pretrained），取 [CLS] token → ProjectionHead → 256-dim。与 TMR 的 text encoder（DistilBERT tokens → ACTORStyleEncoder 6L Transformer → 256-dim）架构完全不同。MP 的 text encoder 从 HuggingFace 权重开始端到端 fine-tune，不继承 TMR 的任何权重。

### Q3: 基于 MIG 和 showlab 的 wiki，是否有值得借鉴的时序 data/pipeline/training？

**值得关注的方向：**
1. **EventT2M (ICLR'26)**：已在 codebase 中，其 MiniConformer + per-event cross-attention 的设计可以启发 TAMR 的 blockwise attention
2. **Kimodo (arXiv'26)**：
   - fine-grained timeline descriptions（overview + atomic event）的双层文本标注思路
   - smoothed root + 非 canonicalized joints 的 motion 表示
   - stitching augmentation 构造组合动作
3. **PRISM (arXiv'26)**：
   - per-joint latent decomposition 证明 motion tokenization / representation 是一级设计变量
   - 对 TAMR 的借鉴点主要在表征粒度与运动学对齐，不是直接照搬 generation objective
4. **ChroAccRet (ECCV'24)**：ordering negatives 的构造方法已被复用
5. **FineMotion (ICCV'25)**：BPMSD 442K 0.5s segments 可作为更细粒度的 temporal annotation source

### Q4: 为什么在 MP 上的适配没有像 TMR 的适配增益显著？

详见第三节根因分析。核心原因（6 层，按机制性排序）：
1. Auxiliary temporal objective 与 final retrieval scoring 的结构性错位（最核心）
2. ViT 缺少强显式时序归纳偏置
3. 所有改动都在 loss 层面，没有触及 motion 表征和 ViT 架构本身
4. MP pretrained baseline 已经很强，边际增益空间小（headroom 限制）
5. 文本侧对 event structure 的利用不足
6. Temporal supervision 的有效样本密度不高（corrected D0：K=1 占 50.70%，超过一半 caption 无 ordering signal）

### Q5: HumanML3D-E 对并行数据的处理是否有问题？

**需要检查。** 当前 event 分解由 Gemini 2.5 Flash 生成，可能存在：
- "walking and waving" 被错误分解为两个顺序 event（应为并行）
- "walk forward and then turn" 被正确分解为两个顺序 event
- 需要抽样验证 "and" 的处理准确率

这是 Step 3.0 数据审计的核心任务。

### Q6: Motion patch 是否需要打乱？

**是的，作为 augmentation。** Step 3.5 提出的 Patch Shuffle Augmentation：
- 训练时随机打乱 14 个时间 bin 的顺序
- 打乱后的 motion 与原始 text 配对作为负样本
- 目的：迫使模型在 embedding 中编码时序顺序信息
- 注意：这是 augmentation，优先级低于结构改动（Step 3.1），应在结构改动有正信号后再叠加

### Q7: Text encoder 是否需要换架构？

**短期不需要换成 generation 式大模型 encoder。** 优先级排序：
1. **最优先**：改变 ViT 的时序处理方式（Step 3.1）— 这是 architecture 创新的核心
2. **次优先**：Event-Structured / Hierarchical Text Encoding（Step 3.4 首推方案）— 保留 event 结构信息
3. **受控升级**：BERT-large / DeBERTa-v3 — 用来验证 text side 是否真是瓶颈
4. **最后考虑**：LLM2Vec 或 Qwen-style encoder — 更适合作为 top-K reranker、离线分析或数据预处理

**原因：** generation 论文需要 token-level conditioning，retrieval 更看重低成本 global embedding 与 embedding geometry；TAMR 当前更像“结构问题”而不是“参数量问题”。

### Q8: 是否需要设计新指标？

**是的，这是论文贡献的重要组成部分。** 当前 CAR/TAR 已有初步实现，但需要：
1. 标准化 benchmark 定义（固定 gallery、固定负样本构造）
2. 新增 Temporal Discrimination Score (TDS)
3. 发布 benchmark 数据和评测代码，让社区可以复用

### Q9: Inference 是否需要特殊设计？

**当前没有，但可以考虑：**
1. **Event-Guided Retrieval**：query 文本先分解为 events，分别检索后融合 scores
2. **Temporal Re-ranking**：先用 global embedding 做粗检索，再用 event-patch alignment 做精排
3. 这些设计可以作为 ablation 展示，但不应是论文的核心贡献

---
## 七、风险与备选方案

### 7.1 最大风险

| 风险                                        | 概率  | 影响  | 缓解                                                   |
| ----------------------------------------- | --- | --- | ---------------------------------------------------- |
| Step 3.1 temporal ViT 改动无效                | 中   | 高   | 准备 5 个方案（B/D/E/C/A），按优先级逐个试                          |
| 更强 backbone baseline 直接抹平增益               | 中高  | 高   | Step 3.0 必须跑 ViT-Large sanity baseline               |
| PrimaryScore 无法突破 45.0                    | 中   | 高   | 转向 benchmark + diagnosis 定位                          |
| PST 开源并占据 temporal 赛道                     | 低   | 高   | 强调 temporal vs spatial 的正交性                          |
| HumanML3D-E 数据质量 / supervision 密度不足       | 中   | 中   | Step 3.0 审计 + 修复负样本实现                                |
| 离散 token 系列（MotionGPT/MoMask）在表示学习上构成替代路线 | 低   | 中   | 论文需讨论 continuous patch vs discrete token 的 trade-off |

### 7.2 备选论文定位

如果 architecture 创新的增益不够大（3-seed mean PrimaryScore 提升 < 0.5），可以转向：
- **Benchmark 论文**：temporal-aware motion-text retrieval benchmark + 诊断工具 + 分析（NeurIPS Datasets & Benchmarks track）
- **Analysis 论文**：深入分析为什么现有 motion-text retrieval 模型是 temporally under-sensitive，提供 insight 和 lightweight fix（ECCV/CVPR workshop）
- 这两种定位对 ICLR 主会来说偏弱，但对上述 track 足够

### 7.3 Contingency: 换范式

如果 B/D/E + representation enhancement 之后仍然都只有 < +0.5 的增益，或者 ViT-Large baseline 一上来就抹平增益，那说明问题可能不只是 PE，而是 **ViT-on-motion-patches 这条路本身的限制**。此时应该：
1. 跑一个 motion-native backbone 作为 disconfirming baseline（如 MotionBERT 的 DSTFormer、或 discrete token + RVQ 路线）
2. 如果 motion-native backbone + temporal loss 能显著超过 MP，则考虑换 backbone
3. 如果 motion-native backbone 也没有显著增益，则说明问题在数据/任务定义层面，应转轨 benchmark 定位

### 7.4 本文档的局限性声明

本文档基于对代码库、实验日志和 eval YAML 的全面阅读撰写，但存在以下局限：
- 部分根因分析（如 objective mismatch 的具体影响程度）是合理推断而非实验验证
- nsim 评测集仅 97 条样本，基于此的数值比较统计功效有限
- 对 MP 架构 ceiling 的判断是"上限未知"而非"上限很高"
- 时间线估算基于单人推进假设，实际可能因 debug、兼容性问题等延长
