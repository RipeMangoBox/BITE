---
title: "StoryMotion Gradio Render"
status: active
tags:
  - StoryMotion
  - visualization
  - gradio
  - status/active
aliases:
  - StoryMotion-Gradio-Render
source_notes:
  - "[[2026-07-01_storymotion-v6.2-metric-data]]"
created: 2026-07-01T14:30:00+0800
updated: 2026-07-01T17:45:00+0800
---

## 0. 当前裁决

可视化展示改为 **Gradio 按 single assets 动态组装**，不再依赖预先拼好的 concat 视频作为主要查看方式。已有 concat / 4x3 视频只保留为 legacy summary 和 smoke check；正式浏览入口应读取 manifest 中的单视频资产，根据 `stage`、`mode`、`sample_id`、`variant`、`view` 动态排列。

## 1. 当前产物索引

根目录在 5090：

`/data/public/ripemangobox/Motion/StoryMotion/runs/visualizations`

| scope | manifest | samples | variants / modes | single assets | status |
| --- | --- | ---: | --- | --- | --- |
| Stage1 source tokenizers | `runs/visualizations/stage1/stage1_tokenizers_20260701_rerun/manifest.json` | 4 mixed samples | `gt`, `molingo_vae_noz`, `separate_ae_noz`, `separate_grfsq_bs128_noz`, `separate_hfsq_wscale_noz`, `separate_vae_wz` | `fixed_camera_mp4`, `orbiting_camera_mp4`, `camera_trajectory_mp4`, `npz` | active rerun; `rerun_reason` set |
| Stage1 joint tokenizers | `runs/visualizations/stage1/v6_2_joint_stage1_20260701_rerun/manifest.json` | 2 mixed + 2 pure samples | `gt`, `joint_vae_wz_*`, `joint_grfsq_wz_*` | `fixed_camera_mp4`, `orbiting_camera_mp4`, `camera_trajectory_mp4`, `rifke_joints_projection_npz` | active rerun; `rerun_reason` set |
| Stage2 joint VAE | `runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun/joint_vae_wz_mixed_full/stage2/vis/v4/concat/cfg_h1_c1_seed17_best_eval/v4_4x3_text_global_camera_manifest.json` | 2 mixed samples | `joint`, `human_completion`, `camera_completion` | `gt`, `pulp`, `storymotion` × camera/global × SMPL/skeleton | active rerun; `missing=0` |
| Stage2 joint GRFSQ | `runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun/joint_grfsq_wz_mixed_full/stage2/vis/v4/concat/cfg_h1_c1_seed17_best_eval/v4_4x3_text_global_camera_manifest.json` | 2 mixed samples | `joint`, `human_completion`, `camera_completion` | `gt`, `pulp`, `storymotion` × camera/global × SMPL/skeleton | active rerun; `missing=0` |
| Screen projection containment | `runs/visualizations/archived/screen_projection_containment_20260625/*/manifest.json` | legacy diagnostic | `clean_best`, `clean_last`, `screen_best` | per-sample camera projection / camera view videos | archived; exclude from registry |

## 2. 目标目录规范

后续新增可视化统一落在：

`runs/visualizations/{stage}/{run_name}/...`

推荐单视频目录结构：

```text
runs/visualizations/
  stage1/
    {run_name}/
      manifest.json
      {split}/
        {variant}/
          {sample_id}/
            fixed_camera.mp4
            orbiting_camera.mp4
            camera_trajectory.mp4
            rifke_joints_projection.npz
  stage2/
    {run_name}/
      {variant}/
        manifest.json
        {sample_id}/
          {mode}/
            camera_projection/
              {column}/
                {column}_camera_view_mesh.mp4
                {column}_camera_projection_skeleton.mp4
            {column}_global_smpl_camera.mp4
            {column}_global_skeleton_camera.mp4
```

命名约束：

- `stage` 只用 `stage1` / `stage2`。
- `mode` 只用 `joint` / `human_completion` / `camera_completion`。
- `variant` 表示实验分支，例如 `separate_ae_noz`、`joint_vae_wz_mixed_full`。
- `column` 表示同一个 sample 内横向比较列，例如 `gt`、`pulp`、`storymotion`。
- 新产物禁止只输出 concat；必须输出 single assets 和 manifest。concat 可以作为可选 summary。

## 3. Gradio 页面规则

### 3.1 顶层控件

| control | type | values | rule |
| --- | --- | --- | --- |
| Stage | segmented / radio | `stage1`, `stage2` | 切换 reconstruction 与 generation/completion |
| Mode | segmented / radio | `joint`, `human_completion`, `camera_completion` | Stage1 默认只显示 `joint/reconstruction`；Stage2 必须三模式 |
| Run | dropdown | manifest run names | 从 manifest registry 自动发现 |
| Split | dropdown | `mixed`, `pure`, `mixed_test` | 只显示当前 run 中存在的 split |
| Sample page | pager | 5 samples per page | 每页最多 5 个 sample group |
| Variant columns | checkbox group | manifest variants / columns | 支持动态增删列，不需要重拼视频 |
| View rows | checkbox group | camera/global × SMPL/skeleton | 支持只看 camera projection 或 global view |

### 3.2 Sample group

每个 sample group 顶部显示：

- `sample_id`
- `num_frames` / `valid_frames`
- human text
- camera text
- mode provenance：例如 camera completion 是 GT human condition + generated camera target

每个 sample group 下面是动态 grid：

| row | Stage1 source | Stage1 joint | Stage2 |
| --- | --- | --- | --- |
| camera projection skeleton | `rifke_joints_projection.npz` 可派生；当前未统一导出 mp4 | `rifke_joints_projection.npz` 可派生；当前未统一导出 mp4 | `{column}_camera_projection_skeleton.mp4` |
| camera projection SMPL | not available in current Stage1 assets | not available in current Stage1 assets | `{column}_camera_view_mesh.mp4` |
| global skeleton | `fixed_camera.mp4` / `orbiting_camera.mp4` 近似替代 | `fixed_camera.mp4` / `orbiting_camera.mp4` 近似替代 | `{column}_global_skeleton_camera.mp4` |
| global SMPL | not available in current Stage1 assets | not available in current Stage1 assets | `{column}_global_smpl_camera.mp4` |
| camera trajectory | `camera_trajectory.mp4` | `camera_trajectory.mp4` | optional diagnostic row |

Stage1 目前没有统一导出 `camera projection SMPL` / `global SMPL` single mp4；Gradio 需要把这些格子标成 missing，不应静默拿 concat 替代。

## 4. Manifest Registry

Gradio 启动时读取一个 registry，不递归扫描全部目录。建议 registry 手工维护为 JSON 或 YAML，内容类似：

```yaml
runs:
  - name: stage1_source_tokenizers_20260701_rerun
    stage: stage1
    manifest: runs/visualizations/stage1/stage1_tokenizers_20260701_rerun/manifest.json
    status: complete
  - name: stage1_joint_tokenizers_20260701_rerun
    stage: stage1
    manifest: runs/visualizations/stage1/v6_2_joint_stage1_20260701_rerun/manifest.json
    status: complete
  - name: stage2_joint_vae_wz_mixed_full_20260701_rerun
    stage: stage2
    manifest: runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun/joint_vae_wz_mixed_full/stage2/vis/v4/concat/cfg_h1_c1_seed17_best_eval/v4_4x3_text_global_camera_manifest.json
    status: complete
  - name: stage2_joint_grfsq_wz_mixed_full_20260701_rerun
    stage: stage2
    manifest: runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun/joint_grfsq_wz_mixed_full/stage2/vis/v4/concat/cfg_h1_c1_seed17_best_eval/v4_4x3_text_global_camera_manifest.json
    status: complete
```

## 4.1 Legacy Exclusion

Gradio registry 禁止递归纳入 `runs/visualizations/archived/`。截至 2026-07-01，以下旧可视化只保留为历史证据，不进入 active registry：

| legacy path | status | action |
| --- | --- | --- |
| `runs/visualizations/archived/stage1/stage1_tokenizers_20260630/manifest.json` | superseded by active rerun | keep archived; exclude |
| `runs/visualizations/archived/stage1/v6_2_joint_stage1_20260701/manifest.json` | superseded by active rerun | keep archived; exclude |
| `runs/visualizations/archived/stage2/v6_2_joint_stage2_20260701/...` | superseded by active rerun | keep archived; exclude |
| `runs/visualizations/archived/screen_projection_containment_20260625/*/manifest.json` | diagnostic only | keep archived; exclude |

## 5. 需要补的 single render

| priority | missing item | why | target |
| ---: | --- | --- | --- |
| 1 | Stage1 camera projection skeleton mp4 | 目前只有 `npz`，不便 Gradio 直接播放 | 每个 Stage1 sample / variant 输出 `{variant}_camera_projection_skeleton.mp4` |
| 2 | Stage1 global skeleton canonical row | `fixed_camera` 与 `orbiting_camera` 不等价于 Stage2 global row | 输出 `{variant}_global_skeleton_camera.mp4` |
| 3 | Stage1 SMPL camera projection / global mp4 | 与 Stage2 四行 grid 对齐 | 如果 Stage1 renderer 能稳定加载 mesh，则补齐；否则明确标 missing |
| 4 | E.T./DIRECTOR camera completion single assets | 当前 metric 有 baseline/replay，Gradio comparison 还没有统一 single assets | 加入 Stage2 `camera_completion` columns：`et_root_only`, `et_replay` |
| 5 | Pulp official Stage1 recon visual | v6.3 要验证 official ckpt 是否可复现，需要 qualitative upper bound | 与 self-trained Stage1 放同一 Stage1 grid |

## 6. 实现检查

Gradio loader 必须做这些检查：

1. manifest path 存在。
2. 每个 selected sample 的 selected variant / mode 都能解析到单视频资产。
3. 不存在的视频显示 `missing` cell，不抛异常阻断整页。
4. 每个视频用 `ffprobe` 或 manifest probe 检查 `frames > 0`、`duration > 0`、首帧非空。
5. 文本区域从 manifest 或 source metadata 读取；读不到时显示 sample id，不编造 text。

## 7. 当前状态

- 已重新渲染 active rerun 到 `runs/visualizations/stage1/` 和 `runs/visualizations/stage2/` 两个主目录。
- Stage2 joint VAE / joint GRFSQ 的 single assets 已经存在于 active rerun 的 `v4_4x3_work`，concat 只是 summary。
- Stage1 所有已完成 tokenizer 的 reconstruction 可视化已有 manifest，但还没补齐与 Stage2 对齐的 SMPL / camera projection single mp4。
- 下一步不是继续做 concat，而是实现 Gradio registry loader，并补 Stage1 missing rows。
