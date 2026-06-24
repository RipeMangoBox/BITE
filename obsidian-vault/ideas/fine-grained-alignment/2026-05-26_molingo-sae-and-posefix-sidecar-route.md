---
title: MoLingo TPA-SAE and PoseFix Sidecar Route
created: 2026-05-26T20:10:00+08:00
updated: 2026-05-26T23:01:46+08:00
status: active
hypothesis: MoLingo 的 SAE 可以作为 generation-backbone 预训练分支：在原始 motion-text semantic loss 外加入 Temporal-Phrase Alignment；HumanML3D 上的 FineMotion/PoseFix 路线只作为弱细粒度 sidecar，不升级为正式 event-time ground truth。
tags:
  - MLPA
  - MoLingo
  - SAE
  - temporal_alignment
  - phrase_anchor
  - PoseFix
  - FineMotion
  - HumanML3D
source_papers:
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]"
  - "[[paperAnalysis/Motion_Generation/ICCV_2025/2025_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annotation_for_Fine_grained_Motion_Generation_and_Editing|FineMotion]]"
  - "[[paperAnalysis/Motion_Editing/ICCV_2023/2023_PoseFix_Correcting_3D_Human_Poses_with_Natural_Language|PoseFix]]"
related_notes:
  - "[[ideas/fine-grained-alignment/README|MLPA README]]"
  - "[[ideas/fine-grained-alignment/roadmap|MLPA 当前路线图]]"
  - "[[2026-05-26_kimodo-seed-humanml3d-data-route|Kimodo/SEED 与 HumanML3D 双轨数据路线]]"
---

# MoLingo TPA-SAE and PoseFix Sidecar Route

> [!abstract] 结论
> 这条路线不替代 MLPA 的 correspondence-first 主线。它是一个 **MoLingo backbone retraining 分支**：先在 SAE 预训练阶段加入 **TPA: Temporal-Phrase Alignment**，增强 latent 与短语、窗口和顺序之间的对齐，再检查是否能改善 MoLingo / downstream generator 的文本跟随能力。HumanML3D 上仿 FineMotion 的 PoseFix 流程只作为 weak body-part evidence / diagnostic sidecar，不能写成正式 event boundary ground truth。

## 1. 4090 MoLingo 状态

远端对象：

```text
host: 4090
repo: /data/public/ripemangobox/Motion/MoLingo
branch: TPA
base head: 52e3b4c309256ce1bb29c8c038fe34b88682db08
current head: 45a3f2f
```

2026-05-26 已新增远端分支与代码提交：

```text
branch: TPA
9bdb73d Add TPA SAE semantic loss modes
76d0800 Skip text evaluator for SAE training
45a3f2f Fix SAE semantic loss aggregation
```

本轮新增的 SAE 语义监督参数：

```text
--sem_loss_mode {wm,tpa_abspos,token_sentence}
--sentence_ratio
--tpa_abspos_scale
```

实现边界：

1. `wm` 保持 MoLingo 原始 window-mean token cosine loss。
2. `tpa_abspos` 在 token-level cosine 中，把归一化绝对 token 坐标 `[0, 1]` 作为一维标量同时拼到 motion latent 与 text anchor 上；这是用户指定的 absolute-position diagnostic，不等价于最终 TPA-select。
3. `token_sentence` 保持 token-level loss，并在 `sentence_ratio > 0` 时额外加入整段序列级 semantic loss。由于当前数据集没有独立 sentence T5 embedding，第一版用有效帧 `t5_vec` 的整段均值作为 sequence text anchor。
4. `train_sae.py` 改为 `load_ms_evaluators(load_text=False)`，只加载 SAE eval 需要的 motionencoder，避免不必要的 DistilBERT textencoder 初始化阻塞；其他 MoLingo train/eval caller 默认 `load_text=True`，接口向后兼容。
5. `45a3f2f` 修复了 semantic loss 聚合：`token_cosine_loss` 和 `sentence_cosine_loss` 只用于 logging，真正反传的语义项是乘过 `cosine_ratio=0.001` 的 `cosine_loss`。`45a3f2f` 之前启动的 short run 因该 bug 作废，不能用于任何比较。

已处理：

1. 已在 EventT2M 远程工作仓库记录 git provenance：`molingo_cleanup_and_sae_design_20260526`、`molingo_cleanup_completed_20260526`。
2. 已删除 MoLingo checkpoint 目录下 4 个已解压后的 archive 文件：
   - `mogen/checkpoints/ms/pretrained_model_272.zip`
   - `mogen/checkpoints/t2m/pretrained_model_263.zip`
   - `mogen/checkpoints/t2m/sae_l2_4_16_1024_d3_kl_1e-05_zero_cos_0.001.zip`
   - `mogen/checkpoints/ms/sae_ms_l2_2_32_1024_d3_kl_1e-05_zero_cos_0.001.zip`
3. 已删除 checkpoint 下载遗留的 `wget-log*`。
4. 删除后 archive 候选为空。

保留状态：

```text
?? artifacts/
?? data/
?? logs/
?? mogen/checkpoints/ms/sae_ms_l2_2_32_1024_d3_kl_1e-05_zero_cos_0.001/
```

这些未跟踪目录可能包含实验产物、数据和已解压 checkpoint，不应在没有进一步确认时删除。

本地审计快照：

```text
artifacts/remote4090/remote4090_molingo_20260526/
artifacts/remote4090/remote4090_molingo_sae_20260526/
```

本轮新增远端日志：

```text
invalid:
  /data/public/ripemangobox/Motion/EventT2M-codes/artifacts/molingo_tpa/sae_tpa_abspos_20260526.log
  /data/public/ripemangobox/Motion/EventT2M-codes/artifacts/molingo_tpa/sae_token_sentence_20260526.log
valid fixed:
  /data/public/ripemangobox/Motion/EventT2M-codes/artifacts/molingo_tpa/sae_tpa_abspos_fix45a3f2f_20260526.log
  /data/public/ripemangobox/Motion/EventT2M-codes/artifacts/molingo_tpa/sae_token_sentence_fix45a3f2f_20260526.log
local copies:
  artifacts/remote4090/molingo_tpa_fix45a3f2f/sae_tpa_abspos_fix45a3f2f_20260526.log
  artifacts/remote4090/molingo_tpa_fix45a3f2f/sae_token_sentence_fix45a3f2f_20260526.log
```

## 2. MoLingo 代码事实

SAE 的原始语义 loss 在远端 `mogen/core/sae_trainer.py` 的 `compute_cosine_loss`：

```text
z: SAE latent tokens, shape [B, token_len, C]
t5_vec: BABEL/T5 per-frame embeddings, shape [B, T, 1024]
stride = 2 ** down_t
history = 4 * stride
for token i:
  start = max(stride * i - history, 0)
  end = stride * i + stride
  text_anchor_i = mean(t5_vec[:, start:end])
  text_anchor_i = Linear(1024 -> C)(text_anchor_i)
  loss_i = 1 - cosine(z_i, text_anchor_i)
```

关键含义：

1. 当前 SAE 的 `sem loss` 是 **motion latent token ↔ 窗口 mean-pooled BABEL/T5 embedding** 的余弦对齐。
2. 训练代码消费的是预计算的 `babel_272_annotation_t5/*.npy`，即逐帧 T5 embedding；原始 BABEL 文本如何从 segment label 变成逐帧 T5 embedding 仍需核查 preprocessing。
3. `--filter` 只过滤相邻近重复 text anchors，不能解决同一窗口内多核心动作被平均的问题。
4. SAE 本体是 causal conv encoder / decoder，已经通过因果卷积感受野和 token 顺序建模时间关系；没有显式 absolute temporal PE 并不等于没有时序信息。
5. MoLingo generator 的 AR Transformer 使用 `build_position_encoding(..., position_embedding="sine")`，即固定 1D sinusoidal absolute PE。
6. Flow MLP 的 `TimestepEmbedder` 是 denoising time embedding，不是 motion token 的 temporal position，不能直接当作 SAE 的 motion-time PE。

因此，TPA 应该利用 **motion token index / phrase window / wrong-window negative** 来强调时序语义，而不是默认给 causal conv latent 再加 absolute PE。

## 3. Loss 方案

统一名称：

```text
TPA = Temporal-Phrase Alignment
TPA-SAE = Temporal-Phrase Aligned Semantic Autoencoder
```

不再使用 `triplet loss` 这个名字。若后续显式加入 anchor / positive / negative 和 margin，可在 TPA 内部做 `contrastive variant`，但主方法名仍保持 TPA。

### 3.1 保留原始 sem loss

```text
L_sem = mean_i [1 - cos(z_i, a_i)]
```

其中 `a_i` 是 MoLingo 现有窗口聚合后的 BABEL/T5 anchor。

### 3.2 添加 TPA loss

第一版不默认加 PE。原因是 causal conv 已经建模局部时序；若只把同一个 `a_i` 加上同一个位置向量再做 cosine，很容易得到位置捷径，而不一定提升语义对齐。TPA 的时序性应主要来自 phrase/window 对应和 wrong-window negative。

最小实现是 `TPA-noPE`：

```text
q_k = phrase/event anchor in R^C
W_{k,i} = phrase k 对 latent token i 的 soft window weight
z_k = sum_i W_{k,i} * z_i / sum_i W_{k,i}
L_TPA = mean_k [1 - cos(z_k, q_k)]
```

总损失：

```text
L_SAE =
  L_rec_feats
  + L_rec_joints
  + L_rec_velocity
  + L_KL
  + lambda_sem * L_sem
  + lambda_tpa * L_TPA
```

可选消融是 `TPA-PE`：

```text
p_i = fixed sine PE(i) in R^C
z_k = sum_i W_{k,i} * norm(z_i + alpha * p_i) / sum_i W_{k,i}
L_TPA_PE = mean_k [1 - cos(z_k, q_k)]
```

PE 使用边界：

1. causal conv + PE 不是 SAE 第一版的必要组合；在纯 TCN / causal conv 里，不加 absolute PE 是常见做法。
2. conv + PE 在 hybrid conv-transformer 或需要绝对位置识别的任务中存在，但不是必须成熟范式；对 motion latent AE，默认加 PE 可能破坏平移等变性或引入位置捷径。
3. 如果试 PE，只用 SAE latent dim `C` 上重新实例化的 fixed sine PE；不复用 AR Transformer 的 `decoder_embed_dim` PE，也不使用 flow MLP denoising `TimestepEmbedder`。
4. `TPA-PE` 只能作为 ablation。如果 `TPA-noPE` 已有效，优先保持无 PE 的简单版本。

### 3.3 对应 time-motion / time-text / motion-text 三边

```text
motion-text: 原始 L_sem，保证 motion latent 与窗口文本语义一致
time-text: phrase/event anchor q_k 带有顺序或窗口权重 W_{k,i}
time-motion: motion token 通过 causal conv 顺序、窗口池化和 wrong-window negative 表达发生位置
```

如果后续需要更强的时序判别，再加入：

```text
positive: correct phrase-window pair
negative: wrong time window / shuffled phrase anchor
loss: margin ranking or InfoNCE
```

## 4. 多短语 Anchor

当前 SAE 的主要风险是窗口级单 anchor 平均。改法不是简单替换 BABEL，而是给一个 latent window 多个可审计短语锚点。

候选来源按可信度排序：

1. Kimodo / SEED official event text + official timestamp：最适合正式 event-time supervision，但数据体量和格式切换成本高。
2. MoLingo BABEL-T5 frame embedding：与当前代码最兼容；需要核查的是生成 `babel_272_annotation_t5/*.npy` 时如何处理同一帧/窗口的多个 BABEL segment label。
3. HumanML3D-E text event list：适合 small ablation 和 failure bank，不是 motion-side boundary GT。
4. FineMotion/PoseFix-style snippet descriptions：适合 body-part weak sidecar，不是动态 event GT。
5. HumanML3D 原始 caption 自动短语切分：成本最低，但时间窗分配噪声最大。

最小实现：

```text
caption / event text
-> extract K core phrases, K <= 6
-> T5 encode each phrase
-> Linear(1024 -> C)
-> assign soft window weights W_{k,i}
-> phrase loss = weighted cosine or InfoNCE over pooled z_i
```

关于 BABEL / T5 的口径：

1. MoLingo 当前 SAE 确实已经使用 T5 embedding，而不是训练时直接读取 raw label。
2. “核查多 label 或单 label”指的是 **T5 embedding 的预处理源头**：如果某一帧有多个 BABEL segment/action label，预处理脚本可能选择主 label、拼接多 label 文本、分别编码后平均，或按其他规则生成单个 1024D frame embedding。
3. 如果某帧/窗口本来只有一个核心动作 label，当前 mean-pool 基本不受“多 label 平均”问题影响；它的上限主要受 label 粒度和 body-part 信息缺失限制。
4. 如果某帧/窗口有多个 key labels，即使最终被 mean 成一个 T5 vector，也通常好过只保留单 label，因为至少保留了更多语义来源；问题是多个可分离动作/部位被压成单 anchor，训练时无法知道该分别对齐到哪些 token、窗口或 body-part cue。
5. TPA 的目的不是否定 MoLingo 的 T5 anchor，而是在多核心语义存在时，把一个 mean anchor 拆成多个可追溯 phrase/event anchors。

第一版不建议让 LLM 自由生成新 action label。应只允许：

1. 从已有 caption / event list 中抽取 verb phrase、body part phrase、direction / temporal phrase；
2. 保留原文 span 和 phrase id；
3. 对低置信 phrase 标记 `ambiguous` 或 `null`；
4. 训练时记录 phrase source，避免把弱短语写成官方标注。

## 5. 单 4090 训练顺序

不要直接承诺 full MoLingo generator retrain。推荐先做 SAE memory probe 和 **Stage 1 clean proof-of-concept**：用可恢复的 BABEL raw segment label 构造 oracle phrase/event anchors，直接验证 TPA 是否优于 MoLingo 的 token-local window mean anchor。只有 Stage 1 成立后，再进入无 raw label 的 Stage 2。

### 5.1 Stage 1：BABEL oracle / clean proof

目标不是直接追 FID，而是证明：

```text
可追溯 phrase/event anchor 选择
> MoLingo token-local window mean anchor
> 单 label / 单 anchor baseline
```

多核心样本定义：

1. **multi-core**：同一 motion 中有不少于 2 个 BABEL phrase/event segments，每段时长不低于 `0.5s`，主要段覆盖率不低于 `80%`。
2. **single-core**：只有 1 个主要 phrase/event segment 覆盖大部分 motion，用于确认 TPA 不会在单动作样本上退化。
3. 训练和测试都混合 multi-core / single-core；先用小样本平衡集做 memory probe，例如 `500 + 500`。

四个最小实验：

| 名称 | Anchor target | 作用 |
| --- | --- | --- |
| `SL` | 全序列或主 label 的单 anchor，所有 token 共用 | 单 label / 单语义 baseline |
| `WM` | MoLingo 原始 token-local causal/history window mean anchor | 当前真实 baseline |
| `MWM` | 使用同样 BABEL segments，但把窗口内多个 phrase anchors 按重叠比例加权混合 | 控制“使用了 segment 信息但仍混合语义” |
| `TPA-select` | 每个 token 选择重叠最多或中心帧所在的 phrase/event anchor | 核心方法：选择而不是混合 |

公平性约束：

1. 四个实验使用同一 SAE 架构、同一 `L_rec`、同一 `lambda_sem / lambda_tpa` 量级、同一 optimizer 和 epoch。
2. `MWM` 和 `TPA-select` 使用相同 raw segments 和 phrase texts；唯一区别是 `mix` vs `select`。
3. `WM` 只使用 MoLingo 当前已存在的 `babel_272_annotation_t5/*.npy` 窗口 mean，不额外给 raw segment。
4. `SL` 用于量化“单 label anchor”的下限，不作为主要强 baseline。

主要指标：

1. **Semantic Attribution Accuracy, SAA**：给定测试样本的所有 phrase anchors，计算每个 latent token 与所有 phrase anchors 的 cosine，取 argmax，判断是否归属到 token 中心帧所在 segment。只统计离边界有 margin 的 token，避免边界歧义。
2. **Semantic Purity**：token 表示是否更接近单一 phrase anchor，而不是同时接近多个不相容 anchors；可报告 top-1 vs top-2 margin、in-segment cosine、wrong-segment cosine gap。
3. **Traceability table**：每个 phrase/event segment 的 token coverage、null / background token 比例、错误最常混淆的 phrase pair。
4. **Reconstruction guardrail**：MPJPE / reconstruction loss / velocity loss 只作 guardrail，防止 TPA 提升可追溯性但损害 motion reconstruction。

成功条件：

```text
TPA-select 在 SAA、top1-top2 margin、wrong-segment gap 上显著优于 WM 和 MWM，
且 reconstruction guardrail 不显著退化。
```

这能证明增益来自“可追溯 anchor 选择”，而不是简单多用了 label 或多了 anchor。

### 5.2 Stage 2：无 raw label 泛化

Stage 1 通过后，才进入无 raw BABEL segment 的泛化版本：

1. **T5 embedding-change pseudo segments**：从 `babel_272_annotation_t5/*.npy` 的逐帧 embedding 变化点发现候选语义段。
2. **HumanML3D-E event text**：用已有 text-side event decomposition 构造 phrase anchors，但明确不当作 motion-side boundary GT。
3. **FineMotion/PoseFix sidecar**：提供 body-part phrase 或局部几何 evidence，作为 weak side signal。
4. **Kimodo/SEED official timeline**：若切到官方 event-time supervision，则作为更强的 formal 数据路线。

Stage 2 的对比沿用 Stage 1 的 `WM / MWM-like / TPA-select` 思路，但所有 pseudo segment 必须记录 source、confidence、limitations。

单卡训练建议：

1. SAE 比 full generator 更适合先在 4090 上跑，因为 T5/BABEL embedding 已预计算，主干是 causal conv VAE。
2. 首次 memory probe 不开大规模评估，先用官方 train split 的小视图或 debug loader。
3. `lambda_tpa` 从 `lambda_sem` 同量级或更小开始，例如 `0.25x / 0.5x / 1.0x` 扫描，避免 phrase/window 伪监督压过重建目标。
4. Stage 1 的 raw segment anchor 是 oracle proof，不应写成最终通用数据依赖；Stage 2 才验证无 raw label 的扩展。
5. 任意 HumanML3D / PoseFix / Qwen sidecar 输出只能记为 `diagnostic` 或 `side_signal`。

### 5.3 2026-05-26 首轮并行诊断实验

已完成代码级检查：

1. `python -m py_compile` 通过：`mogen/core/sae_trainer.py`、`mogen/options/sae_option.py`、`mogen/train_sae.py`、`mogen/utils/eval_utils.py`。
2. 最小 tensor 单测通过：`wm`、`tpa_abspos`、`token_sentence` 和 `tpa_abspos + filter` 都能 forward/backward，`z` 与 `t5_proj` 梯度非零。
3. 真实 debug batch smoke 通过，使用 `ms_dataset.debug=True` 的前 100 个官方 train split 样本，只验证代码路径，不作为实验指标。

真实 debug batch smoke 输出：

```text
dataset_len: 73
batch: motion [2, 300, 272], t5_vec [2, 300, 1024], has_babel=[False, True], lengths=[154, 166]
wm: total loss=0.899877, raw_sem=1.024717, weighted cosine_loss=0.001025, grad ok
tpa_abspos: total loss=0.899843, raw_sem=0.990682, weighted cosine_loss=0.000991, grad ok
token_sentence: total loss=0.900497, raw_sem=1.644446, weighted cosine_loss=0.001644, grad ok
```

DS Max / DeepSeek 检查结论：

1. `sem_loss_mode` 的 shape、mask 和 gradient 路径没有发现 blocking bug。
2. `unit_length == 2 ** down_t` 在 `train_sae.py` 中成立，因此 latent mask 与 token stride 一致。
3. `token_sentence` 的句级 loss 是整段均值约束，可能与 token loss 相关但不完全等价；第一版只能作为 diagnostic。
4. `tpa_abspos` 把同一绝对标量拼到两侧，可能形成位置捷径，不能被解释为最终 TPA 的核心贡献。
5. motion-only evaluator 改动安全，前提是 `train_sae.py` 不使用第一个返回值；当前代码只使用 `_`。
6. 修复聚合后无 blocking bug；可以继续短诊断。非阻塞风险是 `cosine_ratio=1e-3` 可能让语义信号很小，且当前 `filter=False` 不能验证后续 `TPA-select` 的 anchor 选择逻辑。
7. 2026-05-26T22:43 第二次 DeepSeek 短审结论：当前改动无 blocking bug，可训练；非阻塞风险是 `z.shape[1] == t5_embed.shape[1]` 仍是隐含假设，未来结构变化时应显式 assert；`load_text=False` 只适合 SAE 训练，不能用于需要 textencoder 的评估路径。

旧 run 作废：

| run | gpu | command role | status |
| --- | --- | --- | --- |
| `molingo_tpa_abspos_20260526` | `0` | `sem_loss_mode=tpa_abspos`, `batch_size=16`, `max_epoch=5` | invalid: semantic raw losses were included in total loss before `45a3f2f` |
| `molingo_token_sentence_20260526` | `1` | `sem_loss_mode=token_sentence`, `sentence_ratio=0.5`, `batch_size=16`, `max_epoch=5` | invalid: semantic raw losses were included in total loss before `45a3f2f` |

`45a3f2f` 后已重启两个并行 short diagnostic：

| run | gpu | command role | status |
| --- | --- | --- | --- |
| `molingo_tpa_abspos_fix45a3f2f_20260526` | `0` | `sem_loss_mode=tpa_abspos`, `batch_size=16`, `max_epoch=5` | completed diagnostic; initial `MPJPE=145.5051`, `FID=683.7445`; observed GPU memory about `2319 MiB`; wrote `checkpoint-last.ckpt` at 2026-05-26T22:48:36+08:00 |
| `molingo_token_sentence_fix45a3f2f_20260526` | `1` | `sem_loss_mode=token_sentence`, `sentence_ratio=0.5`, `batch_size=16`, `max_epoch=5` | completed diagnostic; initial `MPJPE=145.5051`, `FID=683.7445`; observed GPU memory about `2301 MiB`; wrote `checkpoint-last.ckpt` at 2026-05-26T22:48:34+08:00 |

远端 checkpoint 产物：

```text
/data/public/ripemangobox/Motion/MoLingo/mogen/checkpoints/ms/sae_tpa_abspos_diag_e5_bs16_fix45a3f2f_20260526_tpa_abspos_l2_2_32_1024_d3_kl_1e-05_zero_cos_0.001_sent_0.0_pos_1.0/model/checkpoint-last.ckpt
size: 162621438 bytes

/data/public/ripemangobox/Motion/MoLingo/mogen/checkpoints/ms/sae_token_sentence_diag_e5_bs16_fix45a3f2f_20260526_token_sentence_l2_2_32_1024_d3_kl_1e-05_zero_cos_0.001_sent_0.5_pos_1.0/model/checkpoint-last.ckpt
size: 162621438 bytes
```

运行口径：

1. 数据来自 MoLingo `data/HumanML3D_272`，其中 `motion_data` 26846 个、`babel_272_annotation_t5` 8851 个，split 使用该目录下官方 `train/val/test` 文件。
2. 环境使用 4090 上已有 `event-t2m` conda env，因为 `environment.yml` 指定的 `molingo` env 在远端不存在；这是运行环境替代，需在记录中保留。
3. 两个 fixed run 都是 `diagnostic`，用于验证 loss 有限、训练可跑、显存是否可承受和 early trajectory；不能作为正式排序证据。
4. 全量 dataset 初始化已完成：train init `23384/23384` 用时约 `6:53`，val init `1338/1338` 用时约 `2s`；每个 run 报告 `Total Iters=6160`、`Iters Per Epoch=1232`、`Validation=76`。
5. 两个 fixed run 均已退出，4090 GPU 回到空闲；日志中未检出 `Traceback`、`RuntimeError`、`CUDA out`、`out of memory`、`NaN`、`nan` 或 `Killed`。
6. 当前日志没有稳定输出 early loss 数值；只记录可核到的初始评估、显存、完成状态和 checkpoint 保存状态，不把内部 progress bar 当成正式收敛证据。
7. 可观测性限制：当前命令设置 `save_every_e=1000`、`eval_every_e=1000`、`anim_every_e=1000`，因此本次 `6160` step short diagnostic 不会中途 eval、不会中途保存 best checkpoint；训练代码只在 epoch 结束写 W&B train loss，progress bar 也只有 `global_step % 15000 == 0` 才更新，所以 pane 长时间停在 `0%` 不等价于训练停滞。

## 6. FineMotion / PoseFix 支线

FineMotion 的关键不是让 LLM 直接看 motion 幻想细节，而是：

```text
motion sequence
-> fixed 0.5s snippets
-> start pose + end pose
-> PoseFix correctional text generation
-> BPM snippet descriptions
-> Gemini only connects ordered snippet descriptions into paragraph
```

PDF 3.1 明确说明：

1. 固定 snippet duration 是为了可扩展、避免人工边界，并降低模型输入复杂度。
2. `Ts=0.5s` 来自 PoseScript semantic feature similarity 与 PoseFix 最大 pose-pair interval 的折中。
3. Gemini 的输入是所有 snippet descriptions；prompt 明确要求不要添加原列表不存在的身体部位动作。

因此，HumanML3D 支线应从 Qwen full-video free caption 改成 PoseFix-first：

```text
HumanML3D / HumanML3D-E motion
-> 0.5s snippets, optional 1.0s for robustness
-> root-centered first/last 22-joint pose pair
-> PoseFix modifier
-> root trajectory / yaw / contact / velocity metrics
-> snippet evidence record
```

现有脚本已基本符合这条路线：

```text
scripts/modebug_posefix_snippet_caption.py
scripts/modebug_integrate_posefix_snippet_caption.py
```

允许用途：

1. weak body-part evidence；
2. MLPA body-part cue diagnostic；
3. MoLingo phrase-anchor side signal；
4. Qwen / VLM 失败样例的几何 cross-check。

禁止用途：

1. 正式 motion event boundary GT；
2. final evaluator；
3. 动态速度、步数、接触、意图的完整 caption；
4. 替代 Kimodo/SEED official event-time supervision。

## 7. 与 MLPA / MoDebug 的边界

MLPA 主线仍然是：

```text
event / phrase / temporal attribute
<-> motion chunk / body-part cue / root-contact evidence
```

MoLingo SAE 分支的角色是 **generation backbone pretraining / coupling candidate**，不是 MLPA 第一阶段主 claim。它可以在以下条件下进入 MLPA 后置阶段：

1. MLPA timestamping 或 rerank gate 有正信号；
2. TPA-SAE 不只改善自身 training loss，也改善 SAA / Semantic Purity / downstream independent check；
3. 生成质量、naturalness、diversity、contact guardrail 不显著退化；
4. 使用的 sidecar / pseudo-label 角色完整记录。

MoDebug 的角色是：

1. 提供 hard prompts 和 failure cases；
2. 作为生成后诊断和局部修复工具；
3. 不把 MoDebug 的 scorer 或 Qwen / PoseFix sidecar 升级成 final evaluator。

## 8. 下一步

最小可执行任务：

1. 补 `WM` 对照 short diagnostic，使用与 fixed run 相同的数据、epoch、batch 和可观测记录口径。
2. 做 `batch_size=32` memory probe；若不稳定，回退到 `8/16`。
3. 找到或恢复 `babel_272_annotation_t5/*.npy` 对应的 raw BABEL segment label / text / time 文件，确认能生成 `(phrase_text, start_frame, end_frame)`。
4. 构建 Stage 1 小样本平衡集：multi-core / single-core 各一部分，并生成 phrase-anchor manifest。
5. 实现四个正式 clean-proof loss mode：`SL`、`WM`、`MWM`、`TPA-select`，先只跑 short-run，并把 `save_every_e/eval_every_e` 设成能产生中途可观测结果的值。
6. 报告 SAA、Semantic Purity、Traceability table 和 reconstruction guardrail；只有 `TPA-select > WM/MWM` 后，才进入 Stage 2 pseudo segment 或 generator retrain。

## 9. 记录可靠性

- date: `2026-05-26`
- artifact_path: `paperIDEAs/fine-grained-alignment/2026-05-26_molingo-sae-and-posefix-sidecar-route.md`
- evaluator: `Codex + FineMotion sidecar agent + DeepSeek multi-round cross-check`
- protocol: `remote4090 MoLingo source audit; local FineMotion PDF extraction; PoseFix adapter review; DS Max TPA Stage 1/2 design stress-test; TPA branch code implementation; tensor smoke; fixed debug real-batch smoke after 45a3f2f; invalidated pre-45a3f2f short runs; two fixed short diagnostic tmux runs completed with checkpoint-last`
- motion_source: `MoLingo HumanML3D_272 / BABEL-T5; HumanML3D/HumanML3D-E diagnostic sidecar`
- condition_pair: `MoLingo WM -> SL/MWM/TPA-select clean proof; Qwen full-video route -> PoseFix-first weak sidecar`
- n/evaluable: `debug smoke: 73 debug dataset samples; two fixed full-split diagnostic runs completed, each 6160 planned optimization steps and checkpoint-last generated; no final eval metric because eval_every_e=1000`
- coverage: `MoLingo SAE loss design, TPA naming, PE ablation boundary, Stage 1 oracle proof, Stage 2 pseudo-anchor route, FineMotion/PoseFix sidecar, 4090 cleanup, branch TPA implementation, fixed smoke, completed diagnostic short runs`
- role: `diagnostic`
- used_for: `observation`
- limitations: `当前只完成 fixed smoke 和两个 short diagnostic，尚无正式收敛、正式排序结果或 final eval；本次 save_every_e/eval_every_e=1000，只有 checkpoint-last，无中途 eval 曲线或 best checkpoint；45a3f2f 前两个旧 run 因 semantic loss 聚合 bug 作废；BABEL 原始 label cardinality 未从 preprocessing 源头复核；tpa_abspos 可能引入位置捷径；token_sentence 暂用 frame-level T5 均值而非独立 sentence embedding；PoseFix 只能描述 pose-pair 几何差异，不能提供完整动态事件语义。`
