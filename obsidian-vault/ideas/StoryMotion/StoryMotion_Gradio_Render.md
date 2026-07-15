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
updated: 2026-07-15T19:07:57+0800
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
| Stage1 v7.12 non-causal default ae_train_split | `runs/visualizations/v7_12_correct_fast_stage1_bigtitle_20260709/summary.json` | 8 pure samples | `gt`, `separate_ae_v7_12`, `separate_vae_v7_12`, `separate_grfsq_v7_12`; trained on original paired full `ae_train_split` | `fixed_camera.mp4`, `orbiting_camera.mp4`, `camera_trajectory.mp4`, `rifke_joints.npz`, concat summaries | active synced-row group; 120 mp4 files; velocity preset AE/VAE `1.0`, GRFSQ `0.5` |
| Stage1 v7.13 joint default ae_train_split | `runs/visualizations/v7_13_joint_default_stage1_bigtitle_20260710/summary.json` | 8 pure samples | `gt`, `joint_ae_v7_13`, `joint_vae_v7_13`, `joint_hfsq_v7_13`; trained on original paired full `ae_train_split` | `fixed_camera.mp4`, `orbiting_camera.mp4`, `camera_trajectory.mp4`, `rifke_joints.npz`, concat summaries | active synced-row group; 120 mp4 files; default group |
| Stage1 v7.32 camera9 separate AE/VAE | `runs/stage1/v7_32_separate_local_ae_500ep_seed17_5090_20260713/vis/pure8_last_ae_vae/summary.json` | 8 fixed pure samples | `gt`, `ae_v7_32`, `vae_v7_32`; non-causal human199 + absolute camera9, last checkpoint | `fixed_camera.mp4`, `orbiting_camera.mp4`, `camera_trajectory.mp4`, `rifke_joints.npz`, concat summaries | complete; 96 MP4; Gradio on 4090 port `7863` |
| Stage1 v7.33 camera14 separate AE/VAE | `runs/stage1/v7_33_separate_official14_ae_500ep_seed17_4090_20260713/vis/pure8_camera14_last_ae_vae/summary.json` | same 8 fixed pure samples | `gt`, `ae_v7_33_camera14`, `vae_v7_33_camera14`; normalized human199 + official camera14 | fixed/orbit/camera trajectory MP4, NPZ, concat summaries | complete; 96 MP4; negative Stage1 promotion result |
| Stage1 Pulp AE official vs self-trained | `runs/visualizations/v7_13_pulp_ae_official_selftrained_stage1_bigtitle_20260709/summary.json` | 8 pure samples | `gt`, `official_pretrained_pulp_ae`, `selftrained_pulp_ae_epoch325`; official pretrained uses Pulp released checkpoint, self-trained uses original Pulp mixed train epoch325 | `fixed_camera.mp4`, `orbiting_camera.mp4`, `camera_trajectory.mp4`, `rifke_joints.npz`, concat summaries | active synced-row group; 96 mp4 files; for last-frame distortion audit |
| Stage2 joint VAE | `runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun/joint_vae_wz_mixed_full/stage2/vis/v4/concat/cfg_h1_c1_seed17_best_eval/v4_4x3_text_global_camera_manifest.json` | 2 mixed samples | `joint`, `human_completion`, `camera_completion` | `gt`, `pulp`, `storymotion` × camera/global × SMPL/skeleton | active rerun; `missing=0` |
| Stage2 joint GRFSQ | `runs/visualizations/stage2/v6_2_joint_stage2_20260701_rerun/joint_grfsq_wz_mixed_full/stage2/vis/v4/concat/cfg_h1_c1_seed17_best_eval/v4_4x3_text_global_camera_manifest.json` | 2 mixed samples | `joint`, `human_completion`, `camera_completion` | `gt`, `pulp`, `storymotion` × camera/global × SMPL/skeleton | active rerun; `missing=0` |
| Stage2 v7.34 prompt-global Unified-3 | `runs/stage2/<v7_34_run>/vis/metrics/std_cfg1.0_eta0.0/render_summary.json` | same 8 fixed pure samples | Balanced and `3:2:5` × `camera`, `human`, `joint` | per task PNG、world-skeleton MP4、camera-projection MP4、concat MP4 | complete; each run 136 render assets，其中 32 个 single camera-projection MP4；unified audit on 4090 port `7864` |
| Stage2 v7.36 matched P0 | `runs/stage2/<v7_36_run>/vis/p0_matched_20260715/<schedule>/metrics/std_cfg1.0_eta0.0/render_summary.json` | same 8 fixed pure samples | A parallel/cascade、B symmetric parallel、C no-joint completion/cascade | task PNG、world-skeleton MP4、camera-projection MP4、concat MP4；caption + checkpoint provenance | complete；400 MP4 全部可解码；evidence desk on 4090 port `7865` |
| Stage2 v7.38 L0 clean 105k | `runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/vis/v738_l0_joint_strict_20260715/<schedule>/metrics/std_cfg1.0_eta0.0/render_summary.json` | same 8 fixed pure samples | same checkpoint directed parallel / human-first cascade | strict `human_first` routing、owning decoder、joint trajectory PNG、world-skeleton MP4、camera-projection MP4、concat MP4 | complete；96 MP4、16 PNG；`L0 schedules` tab on 4090 port `7865` |
| Stage2 L0 vs Pulp official | `runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/vis/v738_l0_pulp_official_20260715/render_summary.json` | same 8 fixed pure samples | GT、v7.14 Stage1 identity、L0 parallel、L0 Direct H、Pulp released DiT-xy no-Aux/Aux、HumanML3D fixed-camera reference | same renderer 的 world-skeleton/camera-projection MP4 与 trajectory PNG；Pulp checkpoint/repo/protocol provenance；HumanML3D 明确为非配对 | complete；主对比 tab on 4090 port `7865` |
| Stage2 L0 task slices | `runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/vis/v738_l0_direct_tasks_strict_20260715/completion/metrics/std_cfg1.0_eta0.0/render_summary.json` | same 8 fixed pure samples | same L0 step105k human-text-only、camera-from-GT-H、joint parallel/cascade | H/C strict single world/projection/concat MP4 与 trajectory PNG；Direct H projection 的 GT camera 仅作外部显示 | complete；80 MP4、16 PNG；`L0 task slices` tab on 4090 port `7865` |
| Stage2 L0 single-step gate | `runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/vis/l0_single_step_gate_20260715/render_summary.json` | same 8 fixed pure samples | `human`、`camera`、`joint` × raw GT / `t=999,799,599,399,199` | teacher-forced one-step `pred_x0` 的 world/projection MP4 与 geometry PNG | complete；288 MP4、120 PNG；只作 Go/No-Go 诊断 |
| HumanML3D human-only adapter | `runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/vis/humanml3d_fixed_camera_20260715/render_summary.json` | 8 HumanML3D test clips | canonical 263D inverse RIC、Pulp199 joints-level adapter、fixed camera | 每样例 MP4/首帧 PNG/NPZ；与 L0 样例仅作非配对语义近邻展示 | complete；8/8 decode；camera conditioning disabled |
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
| 5 | Pulp official Stage1 recon visual | v6.3 要验证 official ckpt 是否可复现，需要 qualitative upper bound | done in `v7_13_pulp_ae_official_selftrained_stage1_bigtitle_20260709`; remaining work is human last-frame inspection |

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
- 5090 Gradio `/tmp/v75_paired_audit_gradio.py` 已在 `2026-07-10` 更新；Stage1 active groups 为 `non-causal joint default ae_train_split`、`Pulp AE official vs self-trained`、`causal original`、`non-causal VAE original`、`non-causal default ae_train_split`，不再展示 branch-reweighted visual groups。
- Stage1 元信息表已标注训练数据：`causal original` / `non-causal VAE original` 使用 original paired full，v7.12 使用 original paired full `ae_train_split`；`default velocity` 明确为 AE/VAE `1.0`、GRFSQ/HFSQ `0.5`、acceleration `0`。
- Pulp AE 对比已上线 Gradio synced-row：official pretrained Pulp AE 与 self-trained Pulp AE epoch325 使用同一批 8 个 pure sample，可直接查看 fixed / orbiting / camera trajectory 的末帧形变；synced-row 现在有独立的 `Group sample` 下拉框，切换 group 时只显示该 group 的可用 sample，避免跨 render-set sample 导致全列 missing。
- Mixed GT eval 已停止，不进入正式 metric ledger；当前对比表以 pure official `4053` 为主。
- v7.13 joint default AE / VAE / HFSQ 训练、pure `4053` official eval、8-sample Stage1 visualization 已完成；Gradio synced-row 默认打开 `non-causal joint default ae_train_split`。
- v7.32 camera9 separate AE/VAE 已完成 `636,000` updates、strict contract postflight、pure `4,053` official eval 与 8-sample visual audit。VAE 在 camera9 内部的 FDTMR/HCov/FDCLaTr/CCov 优于 AE；该结果只作为 fixed-intrinsics/extrinsics 消融，不与 camera14 直接排名。
- v7.20 raw14 与 normalized-camera Stage2 已完成 10k train、contract-verified pure-256 official eval 和 8-sample vis；两条路径分别为 `runs/visualizations/v7_20_completed_20260713/raw14/std_cfg1.0_eta0.0/` 与 `normcam/std_cfg1.0_eta0.0/`，每个 sample 同时保留 single PNG/MP4 与 GT|generated concat。
- `scripts/v715_matched_stage2_gradio.py` 已更新为 v7.20 completed audit：四个 Stage1 reference 列 + raw14 Stage2 + normalized-camera Stage2，顶部显示真实 eval metrics；2026-07-13 通过 Playwright smoke，标题、6 个 video、8 个 sample dropdown options 和 sample 切换均正常。
- v7.20 首次 eval 暴露 cache builder 缺少 `tokenizer_is_causal`；修复 metadata 后才进入 official eval。首次 vis 还修复 owning-decoder tensor `.detach()`，这些 contract/renderer 修复已写入 StoryMotion history/ledger。registry loader 仍是后续结构化重构，不阻塞当前 audit 页面。

## 8. 2026-07-13 v7.20 Completed Audit

### 8.1 Evidence paths

- Eval JSON：`runs/eval/stage2/v7_20_completed_20260713/raw14_joint_step10000_full.json`、`normcam_joint_step10000_full.json`。
- Raw14 vis：`runs/visualizations/v7_20_completed_20260713/raw14/std_cfg1.0_eta0.0/`。
- Normalized-camera vis：`runs/visualizations/v7_20_completed_20260713/normcam/std_cfg1.0_eta0.0/`。
- Gradio source：`scripts/v715_matched_stage2_gradio.py`，server port `7862`，使用 `.venv-gradio`。

### 8.2 Display contract

Stage2 两列使用 `joint_concat.mp4`，左侧为 GT skeleton、右侧为当前 checkpoint 的 generated joint skeleton；Stage1 四列仍按 fixed/orbit/GT-camera radio 切换。页面不把 `TMR=0` 隐藏成 pending，也不把 Stage2 退化视频误标为 promotion。

## 9. 2026-07-13 Gradio service and canonical runs layout

- 当前远端服务：`127.0.0.1:7862`，入口为 `scripts/v715_matched_stage2_gradio.py`，运行环境为 `.venv-gradio`。
- Mac 端口转发：`ssh -N -L 7862:127.0.0.1:7862 4090`，浏览器打开 `http://127.0.0.1:7862`。
- 新实验不再直接写入旧的 `runs/train`、`runs/eval`、`runs/visualizations`；先使用 `scripts/storymotion_run_layout.py init`，统一落到 `runs/stage1/<run_id>/` 或 `runs/stage2/<run_id>/`。
- 旧目录保持只读，legacy inventory 位于 `runs/registry/legacy_inventory_20260713.json`；当前 v7.24 probes 已写入 `runs/stage2/v7_24_*_20260713/`。

## 10. 2026-07-14 v7.32 camera9 Stage1 audit

### 10.1 Official metric evidence

共同口径：official pure `4,053`、last checkpoint、non-causal、human199 + absolute camera9、500 epochs / `636,000` updates、seed17。所有 official metric 值有限，两个 records 文件均为 `4,053` 行。

| tokenizer | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v7.32 separate AE | 268.92 | 12.503 | 67.3% | 22.81 | 61.035 | 83.6% | 0.931 | 14.5% |
| v7.32 separate VAE | 208.39 | 14.673 | 79.7% | 15.01 | 63.650 | 89.6% | 0.927 | 13.4% |

证据路径：

- AE JSON：`runs/stage1/v7_32_separate_local_ae_500ep_seed17_5090_20260713/eval/official_pure4053_last.json`
- VAE JSON：`runs/stage1/v7_32_separate_local_vae_500ep_seed17_5090_20260713/eval/official_pure4053_last.json`
- Vis summary：`runs/stage1/v7_32_separate_local_ae_500ep_seed17_5090_20260713/vis/pure8_last_ae_vae/summary.json`

### 10.2 Gradio deployment

- 服务主机：4090；监听 `127.0.0.1:7863`。旧的 v7.20 audit 继续保留在 `7862`。
- 服务脚本：`/tmp/v732_camera9_stage1_gradio.py`；页面动态读取两份 metric JSON 与 shared vis summary。
- Mac 转发：`ssh -N -L 7863:127.0.0.1:7863 4090`，浏览器打开 `http://127.0.0.1:7863`。
- 浏览器 smoke：检测到 8 个 sample options、3 个 view radios 和 GT/AE/VAE 3 个视频；切换到第 2 个 sample 与 `GT camera` 后，三条媒体 URL 均返回 `200 video/mp4`，无 console/page error。

### 10.3 Evidence boundary

camera9 缺少 FOV、actor-relative distance 与 velocity，因此不能把 v7.32 结果解释为 camera14 主线通过。后续 camera14 matched AE/VAE 已完成并作为负结果记录在第 11 节；camera9 仍只作为 fixed-intrinsics/extrinsics ablation，其 FOV 指标保持 `N/A`。

## 11. 2026-07-14 camera14 + Unified-3 audit

### 11.1 Evidence paths

- Stage1 camera14 eval：`runs/stage1/v7_33_separate_official14_{ae,vae}_500ep_seed17_4090_20260713/eval/official_pure4053_last.json`。
- Stage1 camera14 vis：`runs/stage1/v7_33_separate_official14_ae_500ep_seed17_4090_20260713/vis/pure8_camera14_last_ae_vae/`；8 samples、96 MP4。
- Balanced eval/vis：`runs/stage2/v7_34_unified3_balanced_prompt_global_30k_seed17_5090_20260714/{eval,vis}/`。
- `3:2:5` eval/vis：`runs/stage2/v7_34_unified3_artllm325_prompt_global_30k_seed17_5090_20260714/{eval,vis}/`。
- Gradio source：`_private/v735_camera14_unified3_gradio.py`；4090 runtime copy 为 `/tmp/v735_camera14_unified3_gradio.py`。

### 11.2 Display contract

- Stage1 camera14 tab：GT、camera14 AE、camera14 VAE 三列；sample 与 fixed/orbit/GT-camera view 可切换；顶部动态读取两份 pure-4053 JSON。
- Stage1 camera9 tab：同样的 8 个 sample 和 GT/AE/VAE 三列；单独展示 v7.32 camera9 指标，不把 camera9 与 camera14 视为单变量排名。
- Stage2 tab：GT、Balanced、`3:2:5` 三列，`Render` 默认为 `Camera projection`，可切换为 `World skeleton`；页尾保留两张 run-specific geometry PNG。
- camera projection 使用实际 decode 的 camera `c2w` 与 intrinsics：camera completion 为 observed GT human + generated camera，human completion 为 generated human + observed/reconstructed camera，joint 为 generated human + generated camera。该产物是骨架在相机平面上的投影，不是 RGB 或 mesh 渲染。
- completion metric 表只显示生成 target branch；observed GT branch 不进入表格。joint 才同时显示 human、camera 与 Out。
- renderer 对 prompt-enabled checkpoint 复用 official `load_stage2` 重建 global task instruction；prompt-off legacy load regression 同时通过。

每组 v7.34 现有 8 个 sample × `GT + camera + human + joint = 32` 个 single camera-projection MP4，另有 24 个 task-specific projection concat；`vis/projection_assets.complete` 标记已写入。renderer 实现位于 `scripts/render_bilateral_results.py`。

### 11.3 Service

- 服务主机：4090；监听 `127.0.0.1:7864`。旧 v7.20 与 v7.32 audit 继续保留在 `7862/7863`。
- Mac 转发：`ssh -N -L 7864:127.0.0.1:7864 4090`，浏览器打开 `http://127.0.0.1:7864`。
- Browser smoke 已通过：三个 tab（camera14 Stage1、camera9 Stage1、Unified-3 Stage2）均正常；camera9 与 Stage2 各 8 个 sample。camera9 的 GT/AE/VAE 三视频、Stage2 的三路 camera projection、三路 world skeleton 与两张 geometry PNG 均返回 HTTP `200`，两种 Stage2 render 的 media source 确实不同；无 console/page error 或 unexpected request failure。组件切换取消旧 media/queue stream 的 `net::ERR_ABORTED` 被单独识别为预期行为。

## 12. 2026-07-15 v7.36 matched P0 evidence desk

### 12.1 Evidence paths

- A vis：`runs/stage2/v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714/vis/p0_matched_20260715/{parallel,cascade}/`
- B vis：`runs/stage2/v7_36_p0b_sym_unified3_joint30k_seed17_4090g1_20260714/vis/p0_matched_20260715/parallel/`
- C vis：`runs/stage2/v7_36_p0c_asym_nojoint30k_seed17_5090g0_20260714/vis/p0_matched_20260715/{completion,cascade}/`
- Gradio source：`scripts/v736_p0_matched_gradio.py`
- Browser smoke：`_private/v736_gradio_smoke.py`

C 的 metric、vis、experiment contract 与 manifest 已从 5090 镜像到 4090 的
同一相对路径；源端与目标端逐文件 SHA256 完全一致。模型 checkpoint 没有复制，
展示服务只读取 immutable JSON/PNG/MP4 evidence。

### 12.2 Display contract

- `Joint schedules`：GT、A-parallel、A-cascade、B-symmetric parallel、
  C-no-joint cascade 五列；camera projection/world skeleton 两种视角；四列
  run-specific trajectory geometry 图。
- `Completion branches`：GT 与 A/B/C 四列；human/camera target 可切换；
  camera projection/world skeleton 可切换；metric 表只报告生成 target。
- 两个 tab 共用相同的 8 个 fixed pure sample IDs。每个 sample 显示真实
  human/camera caption 与 valid frames；caption 从 dataset `caption_raw` 写入
  render summary，不由页面推断。
- metric 表动态读取十份 official pure `4,053` JSON，并显式显示
  `version / run`。B-human 明确标为 observed-C symmetric control，不伪装成
  human-text-only specialist。
- renderer summary 新增 checkpoint path、checkpoint step、owning decoder 与
  caption provenance；五份 summary 均记录 step `30,000`。

### 12.3 Service and validation

- 服务主机：4090；监听 `127.0.0.1:7865`；进程脚本为
  `scripts/v736_p0_matched_gradio.py`。
- Mac 转发：`ssh -N -L 7865:127.0.0.1:7865 4090`，浏览器打开
  `http://127.0.0.1:7865`。
- `--validate-only`：3 runs、5 summaries、8 samples、330 required files、
  `missing=0`。
- 媒体校验：五组 render 共 400 个 MP4，逐文件调用 renderer 所属 FFmpeg
  解码首帧，`decoded=400`、`failed=0`。
- Browser smoke：两个 tab 均可见；joint 页 5 videos + 4 geometry images，
  completion 页 4 videos；样本、target 与 view 切换均生效；抽查媒体全部返回
  HTTP `200` 与正确 content type；无 page error、console error 或 unexpected
  request failure。

## 13. 2026-07-15 v7.38 L0 joint schedules

### 13.1 Evidence contract

- Run：`runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/`。
- Parallel vis：`vis/v738_l0_joint_strict_20260715/parallel/`。
- Cascade vis：`vis/v738_l0_joint_strict_20260715/cascade/`。
- 两路 summary 均记录 step `105,000`、checkpoint
  `ab474d353a29a4ee707c8ed4e37599fcc47ea79c124452ebdd366d5bdafdaf35`、
  same owning decoder、seed `17`、DDIM50、CFG `1`、`eta=0` 与同一 8 个 pure
  sample IDs。
- Parallel 是同一步联合 H/C 采样；cascade 以同一 Unified-3 checkpoint 的
  `human` task 先生成 H，再以该 H 和 camera text 执行 camera task。没有外部
  specialist 权重。

### 13.2 Assets and service

- 两个 schedule 各含 8 个 sample；合计 96 MP4、16 trajectory PNG。96/96 MP4
  均使用 renderer 实际解析到的 FFmpeg `7.0.2` 解码首帧成功。
- 4090 `127.0.0.1:7865` 的 evidence desk 已新增首个 `L0 schedules` tab：GT、
  directed parallel、human-first cascade 三列，可切换 camera projection / world
  skeleton，并显示两列 trajectory geometry 与 official pure-4,053 指标。
- 全 desk 静态校验更新为 4 runs、7 summaries、8 samples、412 required files、
  `missing=0`。
- Browser smoke 覆盖三个 tab；L0 页为 3 videos + 2 images，legacy joint 页为
  5 videos + 4 images，completion 页为 4 videos。样例、target、view 切换与媒体
  HTTP 响应全部通过，无 page error、console error 或 unexpected request
  failure。
- Mac 转发保持 `ssh -N -L 7865:127.0.0.1:7865 4090`，浏览器打开
  `http://127.0.0.1:7865`。

## 14. 2026-07-15 L0 vs Pulp official native comparison

### 14.1 Evidence contract

- Renderer：`scripts/render_l0_pulp_official_comparison.py`。
- Pulp source：`/data/public/ripemangobox/Motion/PulpMotion`，commit
  `b81c7d95f451ed8728791c7b60f7b1f19503bf1a`。
- Pulp released checkpoint：
  `/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models/runs/dit-xy-ddpm-p2ee3dj7-92950.ckpt`，
  step `92,950`，SHA256
  `7c11cb59d5f51b9090abc1448e76329d157459fc30485031f5a79a7a119660d9`。
- 8 个 sample 与 L0 fixed-8 顺序完全相同。Pulp no-Aux/Aux 共享同一
  checkpoint 和 per-sample noise seed，只切换 released sampler 的 `w_z=0/0.25`。
- GT、v7.14 Stage1 identity 和 Pulp 三列由同一脚本/同一 renderer
  导出；L0 parallel 与 Direct H 复用已审计的 immutable assets。Direct H 在
  `human_first` routing 下只消费 human text。

### 14.2 Display and interpretation boundary

`L0 vs Pulp official` 为 evidence desk 的第一个 tab，每个 sample 显示
7 列视频：GT、v7.14 Stage1 reconstruction、L0 parallel、L0
Direct H、Pulp no-Aux、Pulp Aux、HumanML3D fixed-camera human；另有 6 列
camera/root 或 fixed-frame geometry 图。
可切换 camera projection/world skeleton。

HumanML3D 列不是配对 GT，也不参与 Pulp/L0 指标表；它只用语义近邻动作帮助观察
human motion 先验。view 开关不会改变该列的固定相机。Pulp199 joints 往返误差已审计，
但 pose 特征相对 Pulp stats 仍明显 OOD，因此页面不能把它标成可直接混训的数据。

顶部指标表明确标注为 native-system comparison：L0 使用 DDIM50、
CFG1、`eta=0`；Pulp 使用 released DiT-xy DDPM50、text-CFG11 和
`w_z=0/0.25`。它适合回答“发布系统之间呈现什么质量差异”，
不是对 Stage1 representation、Stage2 architecture、prediction target 或 raw
loss 的单变量归因。

### 14.3 Validation

- comparison assets：64 MP4、24 PNG；64/64 MP4 通过 OpenCV 首帧解码。
- 全 desk `--validate-only`：4 runs、11 summaries、8 samples、1016 required
  files、`missing=0`。
- Browser smoke：6 个 tab 全可见；comparison 页为 7 videos + 6 images，
  single-step 页为 6 + 5，
  L0 页为 3 + 2，joint 页为 5 + 4，L0 task slices 为 4 + 3，
  v7.36 controls 为 4 videos。
  sample/view/target 切换生效，抽查媒体均返回正确 HTTP content type，
  无 page error 或 unexpected request failure。
- 服务已重载于 4090 `127.0.0.1:7865`；Mac 转发命令不变。

## 15. 2026-07-15 synchronized playback and L0 task slices

### 15.1 Layout and playback

- 每个 tab 的当前视频组顶部新增 `▶ 同步播放当前组`；按下后只选取
  当前可见 tab 的 video elements，统一 pause、归零并 play。
- 7 路 L0/Pulp/HumanML3D comparison 固定排为 `3 + 3 + 1`；4 路 task/control
  comparison 排为 2 × 2；5 路 joint controls 为 3 + 2。不再使用横向
  overflow 的单行六列。末行 HumanML3D 保持三分之一列宽；6 路 geometry
  固定换行为 3 + 3，不再向右裁切。
- Browser smoke 实际点击同步播放按钮，确认 7 个 visible videos 同时为
  `paused=false` 且 `currentTime>0`；comparison row counts 为 `[3,3,1]`，
  L0 task row counts 为 `[2,2]`。

### 15.2 L0 matched task-slice evidence

- 旧 `Completion branches` 实际是 v7.36 A/B/C step30k，已重命名为
  `v7.36 controls`，防止被误解为 L0。
- 新 `L0 task slices` 将 GT、L0 direct task、L0 joint parallel、L0 joint
  cascade 放在同一页。human/camera target 和 camera projection/world skeleton
  均可切换；所有 generated columns 共享 step105k checkpoint
  `ab474d353a29a4ee707c8ed4e37599fcc47ea79c124452ebdd366d5bdafdaf35`。
- human task 在 `human_first` routing 下不消费 camera condition；camera task 使用
  observed GT H。parallel 同时生成 H/C，cascade 先 H 后 C；页面和 metric note
  显式保留这些 source-difficulty 差异。
- task-slice render 为 8 samples、80 MP4、16 PNG；80/80 MP4 通过 OpenCV
  首帧解码。

## 16. 2026-07-15 P0-G、Direct H 与 HumanML3D 最终验收

### 16.1 Strict visualization contract

- 主比较页用 L0 Direct H 替代 cascade；cascade 仍只保留在 schedule/task-slice
  诊断页。Direct H summary 记录 `task_routing=human_first`、
  `human_task_camera_conditioning=false`；camera-projection 的 GT camera 仅为外部
  显示视角。
- L0 parallel/cascade 已重渲到 `vis/v738_l0_joint_strict_20260715/`；两者均为
  `strict_run_sampler=true`、`joint_coupling_scale=0`、
  `joint_coupling_mode=c_to_h_blocked`。cascade 使用同一 L0 checkpoint，第一段
  task=`human`，第二段 H→C source=`replay`。
- single-step 页读取 `vis/l0_single_step_gate_20260715/`：8 samples ×
  human/camera/joint × raw GT/`t=999,799,599,399,199`，共 288 MP4、120 PNG。
  每行是 teacher-forced `q(z_gt,t)→one pred_x0`，不冒充 partial/full reverse。

### 16.2 HumanML3D boundary

- 8 个 HumanML3D test clip 使用 canonical 263D inverse RIC；root X/Z 轨迹按速度
  积分保留，再以 proper rotation 从 Y-up 转为 StoryMotion Z-up。fixed camera 不进入
  model conditioning。
- canonical joints 与 `new_joints` 最大误差为 `0`；Pulp199 joints 往返最大误差
  `1.19e-7`。但 Pulp stats 下 normalized pose `|z|` 最大为 `102.8`，故该列只作
  unpaired semantic approximation / adapter audit，不宣称 training-compatible。
  下一关是 SMPL/rest-frame pose retarget、v7.14 Stage1 reconstruction 与 latent OOD。

### 16.3 Validation and service

- 新增/重渲资产：Direct H/C 80 MP4 + 16 PNG，single-step 288 + 120，strict
  joint 96 + 16，HumanML3D 8 MP4 + 8 PNG + 8 NPZ。合计 472/472 MP4 首帧解码
  成功，所有 HumanML3D NPZ 有限。
- 18 份 full-4053 diagnostic JSON 与 `72,954` records 通过 provenance 审计；
  noise seed base=`8026`。元数据修复前后 metrics 完全一致，第二次修复后 36 个
  JSON/records 文件哈希不变。
- Gradio `--validate-only`：4 runs、11 summaries、8 samples、1016 required files、
  `missing=0`。Playwright smoke 通过 6 tabs；主比较 7 videos + 6 images，row
  counts=`[3,3,1]`；single-step 6 + 5，rows=`[3,3]`。sample/task/view、同步播放、
  媒体 HTTP、page/console error 检查均通过。
- 服务运行于 4090 `127.0.0.1:7865`。Mac 转发：
  `ssh -N -L 7865:127.0.0.1:7865 4090`，浏览器打开
  `http://127.0.0.1:7865`。
