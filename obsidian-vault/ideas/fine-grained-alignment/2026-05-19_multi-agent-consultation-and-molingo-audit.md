---
title: MLPA Multi-Agent Consultation and MoLingo Audit
created: 2026-05-19T16:35:08+08:00
updated: 2026-05-20T01:00:00+08:00
status: draft
hypothesis: 多模型顾问意见收敛到同一条保守路线：不要把 text-motion alignment 讲成几何共享空间或新 generator，而应先做可审计的 event/body/time 局部 correspondence layer，并以 timestamping、rerank、verifier/guidance 作为最小贡献。
tags:
  - research-idea
  - Motion_Generation
  - text-motion-alignment
  - fine-grained-alignment
  - multi-agent-consultation
  - molingo-audit
source_papers:
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]"
  - "[[paperAnalysis/Motion_Generation/AAAI_2026/2026_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text|FineXtrol]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Inference|LaMoGen]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval|PST]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction|MaxSim]]"
related_notes:
  - "[[ideas/fine-grained-alignment/roadmap|MLPA current roadmap]]"
  - "[[2026-05-18_multi-level-pivot-alignment|MLPA main note]]"
---
# MLPA Multi-Agent Consultation and MoLingo Audit

> [!warning] 2026-05-20 Active Override
> 本文件只保留多 agent 顾问意见、MoLingo 审计和风险边界。当前执行路线以 [[ideas/fine-grained-alignment/roadmap|MLPA Current Roadmap]]、[[ideas/fine-grained-alignment/mechanism_transfer/README|Mechanism Transfer Notes]] 和 [[gates|Experimental Gates]] 为准。

> [!abstract] 接力结论
> 五个顾问意见没有支持“L1 字面 shared latent space”或“直接做 3DGS / tri-plane 式大生成器”。共识是：把目标收窄成 **event/body/time 局部 correspondence**，先做 verifier / timestamping / rerank，再考虑 generator conditioning。
>
> 2026-05-20 更新：`HumanML3D_272` 已从 4090 的 datasets 目录接入 MoLingo 默认数据路径；`babel_272_annotation_t5` 也已由本地 zip 上传、解压并通过 `Text2MotionDatasetMSBabel` train/val loader smoke。当前 inference、diagnostic generation、272D eval dataset loader、SAE 数据前置条件均已做轻量验证；但 SAE retraining 和 standard full benchmark eval 尚未运行，不能写成训练或正式评测已完备。

## 1. 多模型顾问意见

### 1.1 Agent 1（gpt 5.5 xhigh）: MoAtlas / Pivot Atlas

Agent 1 的核心判断是：问题不是更强 text encoder，而是 text 和 motion 能否共享一组可验证的局部语义坐标。它把 L1-L4 重写为：

1. **L1: 共享语义流形**。共享的是 grounded semantic factors，而不是所有 motion 细节；风格、速度、个体执行方式应作为 modality-private residual。
2. **L2: pivot-anchored local atlas**。pivot 不是点，而是 `event × time span × body part × attribute` 的局部区域；大量局部 atlas 已对齐，但存在 residual。
3. **L3: 弱配对映射空间**。只有样本级或粗事件级 pair，模型可以生成或检索，但无法解释哪个词对应哪段 motion。
4. **L4: 不可识别或 evaluator-illusory mapping**。文本和 motion 互信息不足，或 evaluator 只奖励 dataset prior。

它提出的三条路线分别是：

1. **显式路线**：Event-Body-Time Pivot Matching。文本侧使用 event decomposition，motion 侧使用 `time × body-part` patch tokens，再用 OT / Sinkhorn / MaxSim 做 soft matching。
2. **隐式路线**：Motion-Language Foundation Aligner。用 global contrastive、masked motion modeling、captioning、T2M denoising、event QA、counterfactual preference 混合训练。
3. **混合路线**：Pivot Atlas + Residual Latent Field。显式 pivot 负责可落地语义骨架，隐式 latent 负责连续性、风格和物理自然性。

Agent 1 推荐的 MVP 是 **retrieval / localization first**：HumanML3D + HumanML3D-E + BABEL，先训练 event-to-motion-patch matcher，评估 event retrieval、span localization、drop/replace/shuffle counterfactual ranking，再做小规模 reranking / guidance 到 Event-T2M 或 MoLingo。

建议名称：`MoAtlas: Event-Pivot Atlas for Motion-Language Alignment`。

### 1.2 Agent 2（gpt 5.5 xhigh）: 严格 reviewer / verifier 路线

Agent 2 的判断最保守：原始 L1-L4 叙事如果直接写论文，会被认为把 latent shared space、pivot matching、mapping、generation control 和 retrieval alignment 混在一起，按 reviewer 口径接近 `Borderline Reject`。

它指出的最大漏洞：

1. text-motion 不是同构几何空间。文本是欠定、离散、语义压缩的，motion 是连续、高维且包含大量文本未说明细节的物理轨迹。
2. 不能把 VO / 3DGS 的几何配准叙事照搬过来；这些方法有相机几何、投影方程、光度一致性，text-motion 没有这种守恒约束。
3. L1 应改为 `shared semantic factors + modality-private residuals`。
4. pivot 应定义为 `text span × event × body part × temporal span × motion patch`，并允许一对多、多对一。

它认为会被已有工作打掉的 claim：

| Claim 风险 | 会被谁压住 |
| --- | --- |
| 语义结构化 latent / latent alignment 还没人做 | MoLingo, COME |
| 先规划再合成是新路线 | ActionPlan |
| 细粒度 text pivot 控制是新东西 | FineXtrol |
| 部位级局部区域 / 组合式 pivot 是新贡献 | FrankenMotion |
| LLM / symbol intermediate 是新方向 | LaMoGen |
| joint / segment / global 多尺度对齐是新贡献 | PST |
| token-patch late interaction matching 是新贡献 | MaxSim |

它推荐的最小可守贡献是：**generation-oriented local alignment verifier / guidance**。输入普通文本，自动抽取 `event-bodypart-time` anchors，用 late-interaction motion patches 做局部对齐评分，再用于 reranking、training reward 或轻量 conditioning。论文定位应是“现有 T2M generator 的局部事件、部位、时序绑定盲点”，不是“通用 text-motion mapping”。

硬失败判据：

1. 如果 SOTA 在 hard prompts 上没有稳定局部失败，方向停止。
2. 如果 aligner 只提升自己的分数，不能提升 human judgment 或独立 evaluator，方向停止。
3. 如果相对 PST / MaxSim 的局部检索没有清晰增益，方向停止。
4. 如果生成提升来自 prompt expansion / LLM planning baseline，而不是 alignment mechanism，方法贡献不成立。

### 1.3 Agent 3（gpt 5.4 xhigh）: 工程化指标和路线

Agent 3 把问题改写成可计算的 coarse-to-fine latent alignment。它建议统一对象：

```text
text pivots: p_k = {verb, part, order, duration_prior}
motion units: m_n = motion windows / part tokens
alignment: A in R^{K x N}, plus a null column for unsupported pivots
```

四层指标：

| Regime | 可计算指标 |
| --- | --- |
| L1 global alignment | R-Precision, MM-Dist, Matching Score, global cosine gap, shuffle-negative accuracy |
| L2 pivot mostly aligned | Pivot Coverage, Span IoU, Part F1, OrderAcc, motion saliency overlap |
| L3 mapping needed | strict one-to-one score vs flexible OT score, split rate, merge rate, null rate |
| L4 mapping unstable | counterfactual locality, cycle consistency, OOD unsupported pivot rate |

它提出的显式模块：

1. `Text Pivot Parser`：抽取 verb、part、order、duration prior、optional contact。
2. `Motion Pivot Proposal`：用 sliding windows + part tokens，包含 joint position / velocity、foot contact、phase、root trajectory。
3. `Coarse Matching`：成本函数包含 semantic similarity、order、duration、part、contact、null penalty，优先 monotone OT / Sinkhorn with band mask。
4. `Local Refinement`：boundary regression + region-level cross-attention。
5. `Generator Coupling`：小 adapter / masked cross-attention gating，而不是重写 generator。

对 MLLM 路线的建议是：不要让 MLLM 直接生成 motion token，先做 planner / grounder / rewarder。对 3D / tri-plane 路线的判断是：纯 HumanML3D T2M 帮助有限，只有 HOI / scene / avatar 场景才明显有价值。motion 中更合理的类 tri-plane 是 `time × body-part`、`time × phase`、`body-part × semantic slot`，不是 radiance field。

两周 MVP：

1. 做 event / part parser。
2. 建 CAR、Pivot Coverage、OrderAcc、Span IoU、Counterfactual Locality。
3. 跑 TMR / Event-T2M / 现成 diffusion baseline。
4. 冻结 backbone，训练 monotone OT + boundary refiner。
5. 做无事件、无 part、无 monotone、strict vs flexible、无 counterfactual loss 的 ablation。

两个月 prototype：

1. 建 pseudo-labeled pivot corpus。
2. 训练 explicit aligner + generator coupling。
3. 建 heldout annotation set，按 event count、body-part count、drop/replace/shuffle 分桶。
4. 加 MLLM planner 或 reward model。
5. 做独立 human pairwise eval。

### 1.4 DeepSeek V4 Pro Max

DeepSeek 第一次长 prompt 调用超时，第二次短评审返回。它的判断：

1. L1 不能写成无损 shared latent，应视为粗对齐先验。
2. L2 正确，但“大量 key pivots”容易导致稀疏性灾难，需要明确语义锚点和 residual 偏移。
3. L3 是跨模态常态，应重定义为显式对齐模块。
4. L4 应作为未对齐尾分布，用拒绝采样或编辑式修复，而不是正式能力层级。

它推荐 **explicit pivot matching + atlas / residual latent**，但这个建议应被 Agent 2 的 reviewer 风险约束：atlas / residual 可以作为后续扩展，不应抢占第一版 MVP 的主 claim。

DeepSeek 的三个 gate：

1. BABEL 上 pivot 中间表征检索命中率是否优于 TAMR / Event-T2M。
2. atlas + residual 是否真正改善局部部位控制和多样性，而不是只改 FID。
3. 未见动词、部位、时间组合上是否能组合泛化。

### 1.5 Kimi K2.6

Kimi 的判断比较明确：L1 是伪目标，L2 是真实 frontier。它建议把 L1 改成“在 pivot 子空间上共享度量结构”，而不是字面同一空间。

它推荐路线是 **显式对齐**，但强调不是视觉里程计式 matching，而是层次化语义-运动锚点发现与校准。它提出的 HPA 三层：

```text
Level-1 Event Pivot: text event ↔ motion interval
Level-2 Action Pivot: verb phrase ↔ key pose sequence
Level-3 Manner Pivot: adverb/adjective ↔ local trajectory deformation
```

架构建议：

1. Motion Encoder 加 `Pivot Proposal Network`，输出候选 pivot 特征、时间戳和置信度。
2. Text Encoder 加 `Pivot Extraction Adapter`，输出 type、description、order。
3. Hierarchical Cross-Pivot Attention 对 event、action、manner 分层匹配。

它提出的风险是 Pivot-Contrastive 数据构建成本高，自动标注噪声可能让 manner 层学不到。这个点适合作为后续扩展，不适合作为第一阶段主依赖。

## 2. 收敛后的路线选择

五个顾问意见的交集可以压缩成一句：

```text
先把 text event / body phrase / temporal cue 到 motion chunk / body-part token 的局部对应关系做成可审计中间层，再用它服务 timestamping、rerank、verifier 或轻量 guidance。
```

建议保留的主线名称仍是主笔记里的 **MLPA: Multi-Level Pivot Alignment**。其他名称的取舍：

| 名称                | 优点                                       | 风险                              |
| ----------------- | ---------------------------------------- | ------------------------------- |
| MLPA              | 和主笔记一致，强调多级 pivot 与 correspondence layer | 略宽，需要在 claim 中限定 frozen-first   |
| MoAtlas           | 强调 local atlas，适合后续 residual latent 扩展   | 容易被 reviewer 追问 atlas 新意和 3D 类比 |
| HPA               | 层级清晰                                     | 容易落到新模型架构，数据成本更高                |
| PivotMotion-Atlas | 记忆点强                                     | 过早承诺 atlas/residual generation  |

当前最稳 claim：

```text
We introduce a model-agnostic local correspondence layer for text-to-motion generation,
which localizes event, body-part, and temporal anchors in generated or ground-truth motions
and uses the resulting structure for timestamping, reranking, and alignment diagnosis.
```

## 3. MoLingo 4090 配置审计

只读检查对象：

```text
remote host: 4090
repo: /data/public/ripemangobox/Motion/MoLingo
git head: 52e3b4c
```

### 3.1 已具备的入口

远端仓库存在：

```text
README.md
environment.yml
prepare/download_evaluator.sh
prepare/download_glove.sh
prepare/download_models.sh
mogen/train_sae.py
mogen/train_molingo.py
mogen/demo.py
mogen/eval_mogen.py
```

README 中对应能力：

1. SAE training：`python mogen/train_sae.py --data_root {data_root}`。
2. MoLingo training：`torchrun --standalone --nnodes=1 --nproc_per_node=4 mogen/train_molingo.py --data_root {data_root} --vae {vae_name} --batch_size {batch_size}`。
3. Demo：`python mogen/demo.py -a 1 -i assets/example.txt -b {your_smpl_model_path}`。
4. Evaluation 263D：`python mogen/eval_mogen.py -d 263 -c 5.5 -a 3 -r 20 -dr {your_data_root}`。
5. Evaluation 272D：`python mogen/eval_mogen.py -d 272 -c 7.0 -a 5 -r 20 -dr {your_data_root}`。

### 3.2 Checkpoint 和 evaluator 状态

已看到关键 checkpoint：

```text
mogen/checkpoints/ms/pretrained_model_272/net_best_fid.pth
mogen/checkpoints/ms/pretrained_model_272/opt.txt
mogen/checkpoints/ms/sae_ms_l2_2_32_1024_d3_kl_1e-05_zero_cos_0.001/model/net_best_fid.ckpt
mogen/checkpoints/ms/sae_ms_l2_2_32_1024_d3_kl_1e-05_zero_cos_0.001/opt.txt
mogen/checkpoints/t2m/pretrained_model_263/net_best_fid.pth
mogen/checkpoints/t2m/pretrained_model_263/opt.txt
mogen/checkpoints/t2m/sae_l2_4_16_1024_d3_kl_1e-05_zero_cos_0.001/model/net_best_fid.ckpt
mogen/checkpoints/t2m/sae_l2_4_16_1024_d3_kl_1e-05_zero_cos_0.001/opt.txt
```

MS evaluator 相关目录存在于 `mogen/checkpoints/ms/configs`。没有看到已有 `eval_res.txt`，因此只能说 evaluation 脚本和 checkpoint / evaluator 资产存在，不能说 full benchmark eval 已跑通。

### 3.3 数据状态

2026-05-20 重新检查后，4090 上完整 272D HumanML3D 数据位于：

```text
/data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D
```

该目录包含：

```text
mean_std/Mean.npy
mean_std/Std.npy
motion_data/
split/train.txt
split/val.txt
split/test.txt
texts/
```

已将 MoLingo 默认数据入口切换为软链接：

```text
/data/public/ripemangobox/Motion/MoLingo/data/HumanML3D_272
-> /data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D
```

旧的不完整目录保留为：

```text
/data/public/ripemangobox/Motion/MoLingo/data/HumanML3D_272.backup.20260520_001154
```

数据规模检查：

| Field | Count / shape |
| --- | --- |
| Mean / Std | `(272,)` / `(272,)` |
| `motion_data` files | 26846 |
| `texts` files | 29232 |
| `split/train.txt` | 23384 lines |
| `split/val.txt` | 1338 non-empty ids |
| `split/test.txt` | 4042 non-empty ids |

`babel_272_annotation_t5` 已补齐：

```text
source archive: /home/ripemangobox/Downloads/babel_272_annotation_t5.zip
remote archive: /data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D/babel_272_annotation_t5.zip
sha256: b5dc078d8b9a9a33f535f21c2a55f21e5f84497e62f8ee815f46e8af8072cde9
extracted dir: /data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D/babel_272_annotation_t5
files: 8851 npy files
sample shape: (T, 1024), float32
```

结论：

1. **Inference / custom prompt diagnostic generation 已经可用**，因为已有 pretrained checkpoints、SAE checkpoints、SMPL body model 路径、T5 local path 和 batch artifacts。
2. **MoLingo 272D dataset loader 已验证可用**：`Text2MotionDatasetMS` 能读取 test split，初始化后 `dataset_len = 4404`，首样本 motion shape 为 `(300, 272)`。
3. **MoLingo generation smoke 已验证可用**：272D pretrained 在新数据软链接路径下生成 1/1 成功。
4. **MoLingo training 的主数据路径已具备**，但还没有启动 training run，因此不能说 training 已跑通。
5. **SAE retraining 的数据前置条件已验证**：`Text2MotionDatasetMSBabel` train split 初始化得到 `dataset_len = 19720`、`has_babel = 4158`，val split 初始化得到 `dataset_len = 1228`、`has_babel = 261`；抽样 `has_babel=True` 返回 motion `(300, 272)` 和 T5 `(300, 1024)`。但还没有启动 `train_sae.py`，所以不能说 SAE 已 retrained。
6. **Standard full benchmark evaluation 仍未验证完备**，因为只做了 dataset-loader smoke 和 1-prompt generation smoke，尚未运行 `eval_mogen.py -d 272 -r 20` 并产出 `eval_res.txt`。

### 3.4 已有 diagnostic artifacts

已有 MoDebug batch generation artifacts：

```text
artifacts/modebug_molingo_90prompt_20260512/
logs/modebug_molingo_20260512/
logs/modebug_molingo_20260513/
```

smoke 结果：

| Run | model | prompts | generated_ok | role |
| --- | --- | --- | --- | --- |
| results_smoke_272 | molingo_272 | 1 | 1 | diagnostic |
| results_smoke_272_localt5 | molingo_272 | 1 | 1 | diagnostic |
| results_smoke_263_localt5 | molingo_263 | 1 | 1 | diagnostic |
| results_smoke_272_datasetlink_20260520 | molingo_272 | 1 | 1 | diagnostic |

full90 结果：

| Artifact | model | prompts | generated_ok | n/evaluable |
| --- | --- | --- | --- | --- |
| molingo_272_eval90_20260513 | molingo_272 | 90 | 90 | 90/90 |
| molingo_263_eval90_20260513 | molingo_263 | 90 | 90 | 90/90 |
| molingo_272_eval90_mp4_20260513 | molingo_272 | 90 | 90 | 90/90 |
| molingo_263_eval90_mp4_20260513 | molingo_263 | 90 | 90 | 90/90 |

这些 run manifest 已把 evaluator 标为 `modebug_molingo_geometry_trace_audit`，role 为 `diagnostic`，used_for 为 `observation`。不能把它们升级为 formal evaluator。

2026-05-20 新 smoke provenance：

```text
date: 2026-05-20T00:14:40+08:00
artifact_path: /data/public/ripemangobox/Motion/MoLingo/artifacts/modebug_molingo_90prompt_20260512/results_smoke_272_datasetlink_20260520
evaluator: modebug_molingo_geometry_trace_audit
protocol: m0_gt_paired_fixed_repeat_20260510 MoLingo 90-prompt diagnostic generation
motion_source: MoLingo pretrained_model_272 on 4090
condition_pair: full/drop, full/replace, full/shuffle, full/repeat
n/evaluable: 1/1
coverage: 18 GT-paired base cases x 5 conditions from m0_gt_paired_fixed_repeat_20260510 manifest; smoke used limit=1
role: diagnostic
used_for: observation
limitations: Custom 1-prompt smoke generation; not a formal FID/R-Precision evaluator. 272D outputs are converted to HumanML-style 22-joint positions from generated 272D local-position representation, not SMPL mesh renders.
```

## 4. MoLingo 与 ActionPlan 的关系

ActionPlan 可以理解为和 MoLingo 共享若干基础假设的后续 / 平行升级路线，但不是简单的 MoLingo++。

相同点：

1. 都使用 HumanML3D-272 / BABEL frame-level label 作为重要语义监督来源。
2. 都认为纯 motion reconstruction latent 不够，必须引入 semantic intermediate。
3. 都用中间语义层降低 motion generation 的学习难度。

不同点：

| 维度 | MoLingo | ActionPlan |
| --- | --- | --- |
| 主问题 | 语义结构化 latent 和文本条件注入 | future-aware streaming / offline / editing / inbetweening unified synthesis |
| 第一阶段 | SAE 用 BABEL frame label 做 semantic latent alignment | diffusion 先生成 frame-level Action Plan |
| 条件注入 | T5 + multi-token cross-attention | clean Action Plan as per-frame semantic anchors |
| 关键创新 | SAE + cross-attention + masked autoregressive rectified flow | Action Plan + latent-specific timestep + progressive denoising schedule |
| 最强 claim | latent semantic structure makes diffusion easier | clean future-aware plan makes streaming and editing possible |

因此对 MLPA 的启发不同：

1. MoLingo 证明 representation stage 可以做 semantic pivot，但 pivot 仍偏粗。
2. ActionPlan 证明 clean intermediate plan 能减少 motion denoising 难度，但它的 Action Plan 仍未直接输出 event/body/time correspondence verification。

## 5. ActionPlan demo 抖动的可能来源

这里只能列 hypothesis，不能写成事实结论。

1. **不优先怀疑传统 IK**：ActionPlan 使用 HumanML3D-272 / SMPL-style representation，MoLingo README 也强调 272D 直接提取 rotation component 以避免 IK error。若 demo pipeline 没额外做 joints-to-SMPL IK，抖动更可能来自 latent / decoding / rendering / contact 处理，而不是传统 IK。
2. **frame-level Action Plan 可能引入高频条件噪声**：如果逐帧语义锚点在边界处跳变，motion denoiser 会受到生硬局部约束，可能造成 token boundary jitter。
3. **latent-specific timesteps 和 progressive denoising 可能造成局部不连续**：不同 latent token 处于不同去噪阶段，若 schedule 或 decoder smoothing 不足，边界会有高频残差。
4. **BABEL label 覆盖与 mask loss 可能造成 plan 噪声**：ActionPlan note 中记录 frame-level text labels 只覆盖约 30% 序列，未覆盖部分依赖 mask loss 和数据规模补偿。
5. **渲染层也可能放大抖动**：MP4 中可见抖动未必等于 272D motion 本身的 jerk，需要回到原始 joint / root / contact 曲线检查。

推荐验证：

1. 对 ActionPlan offline 和 streaming 输出分别算 joint jerk、root acceleration、foot contact sliding、token-boundary jerk。
2. 比较 Action Plan latent 的相邻帧变化量和 motion jerk 是否同步峰值。
3. 比较相同 prompt 下 ActionPlan、MoLingo 272D、MoLingo 263D 的 frequency spectrum。
4. 用 MP4 只做观察，不把视频主观抖动当 formal evidence。

## 6. 下一步最低成本实验

第一阶段不训练 generator，先做三个 gate：

1. **Timestamp Gate**：HumanML3D-E ordered events + GT motion，恢复 event spans，要求 boundary quality 优于 equal split。
2. **Verifier Gate**：生成候选 motion，MLPA local score 的 human preference / event satisfaction 高于 global score rerank。
3. **Part Gate**：FineMotion / FrankenMotion-style subset 上，body-part phrase 能定位到正确 body group，且 mask correct part 的 score drop 大于 irrelevant part。

记录时必须保留 provenance：

```text
date
artifact_path
evaluator
protocol
motion_source
condition_pair
n/evaluable
coverage
role
used_for
limitations
```

当前路线漂移记录：

```text
old_plan: shared latent / large generator / possible 3DGS-triplane analogy
new_plan: frozen-first local correspondence layer for timestamping, rerank, verifier/guidance
evidence: MoLingo and ActionPlan occupy semantic intermediate; PST and MaxSim occupy local retrieval; TAMR warns against early training-time alignment loss; agents converged on verifier-first route
affected_docs: MLPA main note; this consultation note
next_action: build timestamping and local rerank gates before generator retraining
```
