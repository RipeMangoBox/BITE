---
title: "5090 数据受损用户通知"
type: incident-user-notice
server: "5090"
tags:
  - operations/data-recovery
  - status/needs-user-action
aliases:
  - 5090 Data Damage Notice
created: 2026-06-20T15:38+08:00
updated: 2026-06-20T15:38+08:00
---

# 5090 数据受损用户通知

> [!warning] 通知结论
> 5090 原数据盘出现不可恢复的连续 I/O 错误。新盘现已挂载为 `/data`，原坏盘保留在 `/data_broken`。大部分可读取数据已迁移，但部分文件未能更新，部分高密度错误目录被跳过。相关用户必须核验或重建下列内容后再继续实验。

全部 2,956 个待处理路径见 [[social/2026-06-20_5090_data_damage_manifest|逐路径受损与未完成清单]]。技术过程见 [[social/2026-06-20_5090_data_recovery_consolidated_report|恢复与挂载切换合并报告]]。

## 通用说明

- 本通知中的 `/data/...` 均指新盘上的预期位置；坏盘对应位置为 `/data_broken/...`。
- “丢弃更新”表示新盘未成功接收坏盘上的该版本，目标可能缺失或保留旧版本。
- “排除”表示后续补拷不再扫描该范围，不代表目录中的每个文件都已证明损坏，也不保证目录完整。
- 不建议直接在 `/data_broken` 上继续实验或批量读取。

## 给 ripemangobox

最终补拷仍无法枚举以下目录，目录内可能存在未进入逐文件日志的缺失项：

- `/data/public/ripemangobox/Motion/datasets/pulpmotion-data/smpl_rifke`

以下内容被主动排除，未完成完整性验证：

- `/data/public/ripemangobox/Motion/datasets/pulpmotion-data/cam_segments/`
- `/data/public/ripemangobox/Motion/datasets/pulpmotion-data/caption_cam/`
- `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v3_closure_20260616/full/gpu1_humjoint_besteval_joint_std_cfg2_eta1.records.jsonl`
- `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v3_closure_20260616/full/gpu3_jointheavy_h2_besteval_joint_std_cfg2_eta1.records.jsonl`

建议从原始数据源重新生成两个数据目录，并重新运行或从其他机器恢复两个评估 JSONL；同时抽查 `smpl_rifke` 的文件数量和可读性。

## 给 zz

### 影响规模

- 待处理路径：2,955 个。
- 明确发生内容读取失败且 rsync 丢弃更新：790 个文件。
- 位于最终排除范围且完整性未验证：2,150 个路径。
- 最终补拷仍报错：15 个路径。

按一级目录统计：`baseline` 1,441、`dataset` 786、`research` 711、`home-migrated` 11、`paper` 3、`.cache` 3。

### 明确丢弃更新的集中位置

- `/data/public/zz/dataset/skillflow-code/...`：776 个文件。
- `/data/public/zz/home-migrated/miniconda3/...`：11 个文件。
- `/data/public/zz/.cache/home-cache/...`：3 个文件。

这些文件可能不存在于新盘，或新盘保留的是早期版本。`skillflow-code/jobs` 下的实验输出应按逐路径清单核验，无法确认时重跑对应任务。

### 最终补拷仍失败的 15 个路径

- `/data/public/zz/dataset/huggingface/datasets/hotpotqa___hotpot_qa/fullwiki/0.0.0/1908d6afbbead072334abe2965f91bd2709910ab/dataset_info.json`
- `/data/public/zz/dataset/huggingface/hub/datasets--hotpotqa--hotpot_qa`
- `/data/public/zz/research/AFSE_EMNLP2026/.git/modules/external/gepa/objects/6f`
- `/data/public/zz/research/AFSE_EMNLP2026/.git/modules/external/gepa/objects/af`
- `/data/public/zz/research/AFSE_v3/.codex/skills/research-paper-writing/references/examples/introduction/pipeline-not-recommended-abstract-only.md`
- `/data/public/zz/research/AFSE_v3/.codex/skills/research-paper-writing/references/examples/introduction/pipeline-version-1-one-contribution-multi-advantages.md`
- `/data/public/zz/research/AFSE_v3/.codex/skills/research-paper-writing/references/examples/introduction/pipeline-version-2-two-contributions.md`
- `/data/public/zz/research/AFSE_v3/.codex/skills/research-paper-writing/references/examples/introduction/pipeline-version-3-new-module-on-existing-pipeline.md`
- `/data/public/zz/research/AFSE_v3/.codex/skills/research-paper-writing/references/examples/introduction/pipeline-version-4-observation-driven.md`
- `/data/public/zz/research/AFSE_v3/.git/objects/09/daa55482fe596316819a0675c4a075fdd44d30`
- `/data/public/zz/research/AFSE_v3/.git/objects/2f`
- `/data/public/zz/research/AFSE_v3/.git/objects/e6/d34816524592b129d304cdad5182f7572dde3f`
- `/data/public/zz/research/AFSE_v3/.venv/lib/python3.13/site-packages/fonttools-4.63.0.dist-info/entry_points.txt`
- `/data/public/zz/research/AFSE_v3/AFSE/benchmarks/__pycache__`
- `/data/public/zz/research/AFSE_v3/experiments/configs/hotpotqa_distractor_skill_only_seed_54mini_solver_55lowstandard_afse.yaml`

Git object、Hugging Face cache、虚拟环境和 `__pycache__` 可直接重新拉取或重建；两个 Markdown 示例与实验 YAML 需要从版本库、其他机器或提交记录恢复。

### 最终排除范围

- `/data/public/zz/research/AFSE_EMNLP2026/external/gepa/.venv/`
- `/data/public/zz/baseline/`
- `/data/public/zz/research/AFSE_v2/root_cache_moved/miniforge3/`
- `/data/public/zz/research/AFSE_v2/runs/`
- `/data/public/zz/research/AFSE_v3/.envs/`
- `/data/public/zz/research/AFSE_v3/docs/runs/`
- `/data/public/zz/research/AFSE_v3/external/`
- `/data/public/zz/research/AFSE_v3/runs/`
- `/data/public/zz/dataset/skillflow-task/.git/lfs/`
- `/data/public/zz/paper/SkillFlow:Benchmarking Lifelong Skill Discovery and Evolution for Autonomous Agents/`

建议处理顺序：

1. 重新 clone 或修复 Git 仓库并执行 `git fsck`；重新 pull Git LFS。
2. 重建 `.venv`、`.envs`、Miniforge 环境、缓存和外部依赖。
3. 对 `runs`、`docs/runs`、`skillflow-code/jobs` 按逐路径清单定位对应实验，优先从日志平台或其他节点恢复，否则重跑。
4. 对 SkillFlow 论文目录先从版本库和协作者副本恢复，再核对无法再生成的手工文档。
5. 处理完成前，不要把新 `/data` 中现存文件默认视为故障前最新版本。

