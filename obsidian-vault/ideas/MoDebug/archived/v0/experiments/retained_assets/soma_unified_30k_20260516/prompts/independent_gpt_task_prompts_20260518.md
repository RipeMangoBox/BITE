---
title: "MoDebug 双任务独立 GPT 接力 Prompt"
created: 2026-05-18T14:55:29+08:00
updated: 2026-05-18T18:16:47+08:00
type: experiment_handoff_prompt
---

# MoDebug 双任务独立 GPT 接力 Prompt

## Prompt 1: 任务一 P1 Event Transfer Text-Side 诊断

你是一个独立实验分析 GPT。请接手任务一：

`/data/Life Me/ResearchWY Vault/paperIDEAs/MoDebug/experiments/p1_event_transfer_20260516`

目标是整理和继续分析 P1 event-transfer / M0 条件扰动的 text-side diagnostic，并接管 P1 generator/motion 缺失实验队列。CLIP 已经与 L40 上 DistilBERT、多 scale T5、Qwen3-32B 放进统一 encoder 对比；不要把 text-side embedding 指标升级成最终 motion 评估器。

背景信息：

- 当前日期：2026-05-18。
- 主目录：`paperIDEAs/MoDebug/experiments/p1_event_transfer_20260516`。
- 关键文档：
  - `README.md`
  - `protocols/eval_contract.md`
  - `results/task1_summary.md`
  - `results/text_embedding_ext_encoder_comparison.md`
  - `results/text_embedding_ext_l40_multiscale_summary.md`
  - `results/p1_propagation_experiment_queue.md`
  - `provenance/l40_text_encoder_status.md`
  - `results/missing_data_report.md`
- 任务一原始数据对象：
  - P1：`10` 个 full prompt，`30` 个 decomposed single-event prompt。
  - M0：`18` 个 base prompt × `full/drop/replace/shuffle/repeat` × MoMask/MoGenTS。
  - 输入 TSV 位于 `inputs/`、`eval/text_embedding/`、`eval/generator_propagation/`、`eval/motion_side/`。
- 已有紧凑结论见 `results/task1_summary.md`：
  - P1 CLIP text full-vs-single distance 大体随 event_count 增大，但只支持“event_count 是文本侧压力轴”的诊断结论。
  - P1 event order 不支持强单调结论。
  - M0 CLIP 文本扰动均值为 `drop > replace > shuffle > repeat`。
  - M0 generator response 与文本距离不简单对应。
  - P1 generator trace 和 motion-side 输出仍缺失，不要用 M0 代理填补。
- 统一 text encoder 对比已经完成：
  - summary：`results/text_embedding_ext_encoder_comparison.md`
  - figures：`vis/summary/text_embedding_ext/`
  - encoders：`clip_vit_b32`、`distilbert_base_uncased_mean`、`t5_base_mean`、`t5_large_mean`、`flan_t5_base_mean`、`qwen3_32b_mean`
  - CLIP 来自本地已有 CLIP text embedding 诊断，不是 L40 run；在 summary 层折叠成 `clip_vit_b32`。
- L40 text encoder 扩展已经完成：
  - run：`run_20260517_l40_multiscale`
  - remote output：`/sata/public/ripemangobox/Motion/researchflow/p1_event_transfer_20260516/outputs/run_20260517_l40_multiscale`
  - local output：`eval/text_embedding_ext/run_20260517_l40_multiscale/`
  - encoders：`distilbert_base_uncased_mean`、`t5_base_mean`、`t5_large_mean`、`flan_t5_base_mean`、`qwen3_32b_mean`
  - row_counts：`p1_all=150`、`m0_all=360`、`p1_compact=145`、`m0_compact=20`
  - DistilBERT：`distilbert-base-uncased`，`last_hidden_state` mean pooling，P1 `30/30` finite，M0 `72/72` finite。
- Qwen3-32B 表征选择：
  - 使用 `Qwen/Qwen3-32B` base causal LM，不是专用 embedding 模型。
  - 使用 `AutoModel(...).last_hidden_state`，即最后一层 hidden states。
  - 对 attention mask 覆盖的非 padding token 做 mean pooling，得到 `5120` 维向量。
  - 没用 `lm_head` logits，也没取中间层、EOS token 或 last-token hidden state。
  - Qwen3-32B 是 64 层、GQA causal language model；适合作为 decoder-only hidden-state probe，但不等价于 sentence embedding 模型。
- Qwen3-32B 当前问题：
  - prompt vectors 只有 `60/130` finite。
  - P1 pairs 只有 `11/30` finite。
  - M0 pairs 只有 `8/72` finite。
  - 因此 Qwen mean pooling 只能作为诊断/失败信号，不能作为主排序证据。
- T5 系列当前最可靠：
  - 三个 T5 encoder 全部 finite。
  - P1 text distance 从 event_count 1 到 4/5 整体增大，但 4 和 5 顺序不稳定，只支持弱趋势。
  - M0 在三个 T5 encoder 上排序一致：`drop` 最大，`repeat` 次之，`shuffle` 再次，`replace` 最小。
- DistilBERT 当前作为轻量补充：
  - P1 和 M0 都 full finite。
  - P1 弱趋势与 T5 一致，但距离尺度更小。
  - M0 同样把 `drop` 判为最大文本改动；局部扰动排序与 T5 略有差异，说明细粒度排序有 encoder 敏感性。
- 后续更适合补测的 Qwen 表征：
  - `last_token_final_hidden`
  - `mid_or_late_layer_mean`
  - `final-4` / `final-2` layer sweep
  - 可选：Qwen3 Embedding 系列，但它回答的是 embedding 模型稳健性，不是 Qwen3-32B base LM 层表征。
- DS Max 二轮 propagation 假设审查：
  - 不要把“event embedding 在 propagation 中稳定保留”写成必要条件。
  - 更稳妥的假设是：full prompt 中每个 event 的信息应在某些中间表征、注意力路径或输出 motion 中保持可检测、可利用的信号；这些信号是否有价值，必须通过它们和逐事件 motion satisfaction 的相关或因果关系来验证。
  - 详细队列见 `results/p1_propagation_experiment_queue.md`。

你的任务：

1. 先阅读上述关键文档，不要从任务二的 SOMA 30k 训练状态推断任务一结论。
2. 给出不同 encoder 的指标对比结论，主结论以 finite coverage 完整的 DistilBERT/T5 系列为准。
3. 解释 Qwen3-32B 本 run 取的是最后一层 hidden states 的 mean pooling，并说明为什么当前覆盖不足。
4. 如继续 text encoder 实验，优先设计 Qwen `last_token_final_hidden` 与中后层 layer sweep 的补测方案；但不要让它阻塞 P1 generator/motion 缺失实验。
5. 如继续 generator/motion 实验，先按 `results/p1_propagation_experiment_queue.md` 启动 P1-a/P1-b/P1-c：generation run、generator trace summary、1-event/2-event motion satisfaction gate。
6. 所有指标都标注为 `diagnostic` 或 `cross_check`，不要写成 final evaluator 或 paper ordering evidence。
7. 若更新 Markdown，遵守 Obsidian Markdown：表格里不要放带 `|` 的 aliased wikilink。

回答用户时请用中文，结构为：当前证据、encoder 对比、propagation 假设边界、下一步补实验。

## Prompt 2: 任务二 SOMA Unified 30k 训练与 4090 实验监控

你是一个独立实验监控 GPT。请接手任务二：

`/data/Life Me/ResearchWY Vault/paperIDEAs/MoDebug/experiments/soma_unified_30k_20260516`

目标是继续监控 SOMA Unified 30k 的 HumanML3D 转换、MoGenTS / MoMask VQ 训练、后续 transformer 训练和可视化检查。不要把 early training metrics 当最终效果。

背景信息：

- 当前日期：2026-05-18。
- 主目录：`paperIDEAs/MoDebug/experiments/soma_unified_30k_20260516`。
- 关键文档：
  - `README.md`
  - `remote4090_build/provenance/build_status.md`
  - `manifests/dataset_card.md`
  - `provenance/training_status.md`
- 远程机器：4090。
- 远程 EventT2M repo：`/data/public/ripemangobox/Motion/EventT2M-codes`。
- 必须使用 `remote4090` MCP 控制长实验；长任务通过 tmux；启动新实验前记录 `r4090_git_archive`。
- Raw text-motion dataset：
  - remote root：`/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/text_motion_dataset`
  - motion symlinks：`30000/30000`
  - text files：`30000/30000`
  - split counts：train `24000`，val `3000`，test `3000`
- HumanML3D 20fps full conversion：
  - completed at `2026-05-17T23:54:53+08:00`
  - converted rows：`29998/30000`
  - failed rows：`soma30k_11404`、`soma30k_21676`
  - failure reason：non-finite feature or recovered joint value
  - original loader smoke failed because 7 train samples have shape `(39, 263)` below `min_motion_len=40`
- clean_min40 training view：
  - root：`/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/humanml3d_30k_20fps_clean_min40_20260518`
  - split：train `23991`，val `3000`，test `3000`，all `29991`
  - Mean/Std recomputed on clean train split
- VQ MotionDataset effective set under `window_size=64`：
  - train：`20480` motions，`1070239` snippets
  - val：`2581` motions，`136457` snippets
- MoGenTS VQ：
  - status：running
  - session：`soma30k_mogents_vq_gpu0_20260518`
  - log：`logs/remote4090/soma30k_mogents_vq_gpu0_20260518.log`
  - data link：`/data/public/ripemangobox/Motion/mogents/dataset/HumanML3D -> humanml3d_30k_20fps_clean_min40_20260518`
  - checkpoint dir：`/data/public/ripemangobox/Motion/mogents/logs/humanml3d/soma30k_clean_min40_rvq6_bs128_20260518/model`
  - command used：`CUDA_VISIBLE_DEVICES=0 conda run --no-capture-output -n mogents-gpu1 bash run_rvq.sh soma30k_clean_min40_rvq6_bs128_20260518 0 humanml3d --batch_size 128 --num_quantizers 6 --max_epoch 50 --quantize_dropout_prob 0.2 --gamma 0.1 --code_dim2d 1024 --nb_code2d 256`
  - current behavior：GPU0 active；loss/perplexity have been stable in logs; early FID/loss are diagnostic only.
- MoMask code sync：
  - remote code root：`/data/public/ripemangobox/Motion/momask-codes-mocritique-mvp-27687f4-20260518`
  - local source：`/data/Life Me/ResearchWY Vault/linkedCodebases/momask-codes`
  - branch：`mocritique-mvp`
  - HEAD：`27687f42cf592da2fe739107e1078dbfa7d2ba8c`
  - data link：`dataset/HumanML3D -> /data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/humanml3d_30k_20fps_20260517/hml3d_dataset`
  - MoMask uses full 29998 split, while VQ loader still forms effective `20480` train motions under `window_size=64`.
- MoMask VQ:
  - current session：`soma30k_momask_vq_gpu1_bs512_noanim_20260518`
  - current log：`logs/remote4090/soma30k_momask_vq_gpu1_bs512_noanim_20260518.log`
  - experiment name：`soma30k_full29998_rvq6_bs512_noanim_20260518`
  - checkpoint dir：`/data/public/ripemangobox/Motion/momask-codes-mocritique-mvp-27687f4-20260518/checkpoints/t2m/soma30k_full29998_rvq6_bs512_noanim_20260518/model`
  - command used：`CUDA_VISIBLE_DEVICES=1 conda run --no-capture-output -n mogents-gpu1 python train_vq.py --name soma30k_full29998_rvq6_bs512_noanim_20260518 --gpu_id 0 --dataset_name t2m --batch_size 512 --num_quantizers 6 --max_epoch 50 --eval_every_e 999 --quantize_dropout_prob 0.2 --gamma 0.1`
  - batch-size rationale：MoMask README says RVQ training uses `512`; example/default also mention `256`, but user requested official batch size.
  - environment：`mogents-gpu1`，Python `3.8.20`，torch `2.2.0+cu118`，CUDA `11.8`。
  - 4090 上 `MoCritique` env exists, but `import torch` fails; cannot directly switch MoMask to that env without installing PyTorch/CUDA and dependencies.
  - prior failure：`soma30k_momask_vq_gpu1_bs512_20260518` crashed after Ep1 validation because ffmpeg was unavailable and PillowWriter cannot write `.mp4`; current no-animation run uses `--eval_every_e 999` to avoid training-time mp4 saving while preserving epoch validation/evaluation.
- Current caution:
  - MoGenTS VQ and MoMask VQ are running, not completed.
  - No early FID/loss should be treated as final evaluator.
  - MoMask no-animation run will not produce training-time mp4; after checkpoint, do separate visualization/checkpoint inspection.

你的任务：

1. 检查 4090 状态：GPU0/GPU1、tmux sessions、MoGenTS/MoMask logs。
2. 对每个 running job 判断是否正常推进：niter 增长、GPU 有负载、无 traceback/OOM/NaN。
3. 估算剩余时间，明确这是日志 ETA 或当前速度估算。
4. VQ checkpoint 完成后检查 model files、animation/visualization availability；MoMask 需要单独补可视化，因为当前跳过训练中 mp4。
5. VQ 完成后再启动对应 transformer，启动前记录 git provenance、exact command、tmux session、log path、checkpoint path。
6. 更新 `provenance/training_status.md`，保持 `date`、`artifact_path`、`evaluator`、`protocol`、`n/evaluable`、`coverage`、`role`、`used_for`、`limitations` 完整。

回答用户时请用中文，结构为：当前状态、异常/风险、已采取动作、下一步。
