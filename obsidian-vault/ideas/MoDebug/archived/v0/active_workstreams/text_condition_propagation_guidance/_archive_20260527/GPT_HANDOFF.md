# GPT Handoff — MoDebug text-condition trace 项目交接

## 项目目标

研究 motion generation 模型中 text embedding 如何传播并引导动作生成。对 4 个 baseline 模型做 **text vs null_text forward trace**，从内部 delta 张量中找出 success/failure 样本的差异模式，最终设计机制提高指令跟随能力。

## 当前状态

已完成 **8 case pilot run** (4 baseline × 2 outcome = 1 success + 1 failure each)。完整数据链路闭环：`sample → human annotation → motion MP4 → forward NPZ (text+null) → delta NPZ`。

下一步是扩展到 **400 sample** (4 baseline × 100)，然后按 `analysis_plan_400_samples.md` 执行系统分析。

## 目录结构

```
implementation_20260527/
├── trace_adapters/       # hook 模型内部层 → 输出 forward NPZ
│   ├── t5_trace_adapter.py           # MotionGPT, MoLingo
│   └── clip_discrete_trace_adapter.py # MoMask, MoGenTS
├── trace_metrics/        # delta = text_forward − null_forward
│   ├── compute_delta.py
│   └── trace_contract_validator.py
├── sync_index/           # manifest 索引 + 远端同步
│   ├── build_manifest_index.py
│   └── sync_sanity_check.py
├── reports/
│   ├── sample_level_trace_run_report.md  # 主报告（实验方法+指标+结论）
│   ├── provenance.md                     # 远端路径+脚本索引
│   ├── analysis_plan_400_samples.md      # 400 sample 分析方案
│   └── trace_io_contract.md              # NPZ 格式规范
└── visualizations/       # 3 个 SVG + 底层 CSV/JSON
    ├── case_cards.svg
    ├── per_timestep_delta_l2.svg
    ├── time_feature_delta_mass.svg
    └── delta_tensor_summary.json
```

顶层 `README.md` 和各子目录的 `README.md` 说明了每个模块的职责。

## 关键概念

**delta = forward(text) − forward(null_text)**，在同一随机状态下计算。

- `relative_l2 = ||delta|| / ||forward(text)||` — text 对特征的总体影响强度
- `per_timestep_l2[t] = ||delta[t, :]||` — 影响的时间分布
- `time-feature mass` — 对特征维度分箱后，delta L2 在 (时间, 特征区域) 上的分布

4 个模型的 hook 层不同，跨模型 delta 不可直接比较：

| Model | f_name | delta shape | f_space |
|-------|--------|-------------|---------|
| MotionGPT | token_logits | (1, 6, 514) | motion_vocab_logits |
| MoLingo | hidden_state | (1, 49, 1024) | latent_transformer_z |
| MoMask | token_logits | (1, 21-23, 512) | vocab_logits |
| MoGenTS | token_logits | (1, 23-38, 6, 256) | time_joint_vocab_logits |

## 数据位置

- **本地 artifact**: `artifacts/remote/4090/modebug_text_condition_sample_level_20260528/text_condition_sample_level_20260528/`
- **远端**: `4090:/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/modebug/text_condition_sample_level_20260528/`
- **可视化脚本**: `scripts/modebug_visualize_time_feature_delta_mass.py` (用 conda python 跑)
- **关键索引**: `index_outputs/sample_case_index.tsv` (8 row P3 证据链)

## 待做任务（整理版）

### P0 — 数据与工程闭环

1. **批量扩展到 400 sample**: 写 batch wrapper 对现有 4 个 `run_*_sample_trace.py` 做批量 trace，每个 baseline 跑 100 个 sample。已有 Original100 human annotation 数据。
   - 参考: `runners/` 目录在 artifact 里
   - 质控: 跑完自动调 `trace_contract_validator.py` + `build_manifest_index.py`
   - 产出: `batch_manifest_index.tsv`、400 row sample-case 索引、每个 case 的 forward/delta NPZ
2. **MoLingo mask 问题处理**: 明确 MoLingo 的 `valid_mask` 是 latent AR 初始状态的结构性稀疏，不当作 bug，但所有统计、可视化和差异检验必须只在 valid positions 上计算。
   - 需要记录每个 sample 的 `valid_ratio`，并检查 `valid_ratio` 是否与 outcome / failure_factor 相关
   - delta 计算和特征抽取统一使用 text/null 两个 forward 的有效 mask 交集，避免未激活 token 污染统计
   - 报告中必须同时给出 masked 统计口径和 coverage/valid_ratio，不能只报裸 `relative_l2`
3. **批量质控报告**: 汇总 NaN/Inf、缺失 manifest、空 prompt、空 motion path、低 valid coverage、跨条件 shape 不一致等问题，作为后续分析的入口检查。

### P1 — 分析闭环

1. **描述统计 + 差异检验 (Agent A)**: per-model × per-outcome 的标量统计、Mann-Whitney U test、effect size。
2. **Prompt NLP 特征提取 (Agent D)**: prompt length、子动作数、时序复杂度、prompt embedding、hard prompt 分组。
3. **PCA + t-SNE/UMAP + DTW 聚类 (Agent B)**: 从 `time_feature_mass` 和 `per_timestep_l2_norm` 发现自然 delta 模式。
4. **RF + SHAP 判别分析 (Agent C)**: 找出 success/failure 最相关的 delta 与 prompt 特征，识别 borderline samples。
5. **sample-level case audit**: 对统计异常点、cluster 代表样本、borderline samples 回看 prompt、human annotation、motion MP4 和 delta 可视化，防止只靠 aggregate 指标做机制假设。

### P2 — 核心研究问题闭环

核心问题是: **如何从统计和 sample 级别的信息进行合理的问题发现和机制设计？**

当前方案已经覆盖这个问题的主要部件，但需要把它作为显式验收标准。完成标准如下：

1. **问题发现**: aggregate 统计先给出候选问题，例如 delta 过低、delta 过高、晚期峰值、错误特征路由、时序波动大、prompt 类型困难。
2. **sample 证据回查**: 每个候选问题必须回查代表样本，确认 prompt、human annotation、motion MP4 和 delta trace 是否一致支持该解释。
3. **机制假设**: 每个问题类型必须对应一个可被反驳的机制假设，而不是只给现象命名。
4. **干预设计**: 每个机制假设必须给出最小干预实验、预期 delta 变化、预期 motion-level 改善和失败判据。
5. **证据边界**: trace 只能作为 diagnostic / side signal；若要升级为正式结论，需要 held-out evaluator、random/semantic perturbation 控制和明确 coverage。

### P3 — 机制设计与干预实验

根据分析结果设计干预实验。当前候选方向：
- text-motion balance gate
- sparse text-to-feature routing
- temporal consistency loss
- early-decoding text bias injection
- MoLingo sparse text injection on valid latent tokens
- random text / semantic perturbation / partial text mask 控制条件

### P4 — 可视化与报告质量

1. **解决可视化图片文字重叠**: 修复 `case_cards.svg`、`per_timestep_delta_l2.svg`、`time_feature_delta_mass.svg` 中标题、说明、legend、长 manifest/path 文本的重叠。
   - 优先修改生成脚本，而不是手工改 SVG
   - 长路径和 manifest 使用截断、中间省略或换行
   - 每张图重新导出后检查 desktop/mobile/Obsidian 阅读视图下是否可读
2. **统一图表说明口径**: 图中明确标注 sample-level diagnostic、不是 final evaluator；跨模型不可直接比较绝对值。
3. **更新最终报告**: 汇总 400 sample 分析、核心问题闭环、机制建议、局限和下一步实验。

## 约定

- 所有 `.md` 使用 Obsidian wikilink 格式
- SVG 图表用纯 Python 生成（无 matplotlib 依赖），字体栈 `'Noto Sans CJK SC','Microsoft YaHei','PingFang SC','DejaVu Sans',sans-serif`
- NPZ 必需 key: `signal, valid_mask, meta_json, axis_names_json` (见 `trace_io_contract.md`)
- 跨模型 delta 值不可直接比较，分析时用 per-model 归一化或 ranking
- MoLingo 的 valid_mask 仅 47-78%，所有统计必须 propagate mask
