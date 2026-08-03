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
  - "[[2026-07-17_storymotion-stage1-length-condmdi-causal-priority]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
  - "[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]"
created: 2026-07-01T14:30:00+0800
updated: 2026-08-03T21:05:00+08:00
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
| Stage2 L0 vs Pulp official | `runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/vis/v738_l0_pulp_official_20260715/render_summary.json` | same 8 fixed pure samples | GT、v7.14 Stage1 identity、L0 parallel、L0 Direct H、Pulp released DiT-xy no-Aux/Aux | same renderer 的 world-skeleton/camera-projection MP4 与 trajectory PNG；Pulp checkpoint/repo/protocol provenance | complete；已从该 tab 移除全部 HumanML3D 内容；4090 port `7865` |
| Stage2 L0 joint geometry Top-5 `2 × 3` | `runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/vis/v738_l0_joint_top5_20260716/` | pure4053 paired-GT geometry；human-only、camera-only、joint 各 5 条，共 15 个无重叠 IDs | 第一行 StoryMotion GT/recon/gen；第二行 joint specialist gen、Pulp recon、Pulp Aux gen | H-MPJPE、Cam-ADE、human/camera text、display-only TMR/CLaTr/in-frame；aggregate 表含 L0、specialist、Pulp no-Aux/Aux | complete；specialist/Pulp MP4 decode `120/120` 与 `150/150`；`Joint Top-5 · 2×3` tab on 4090 port `7865` |
| Stage2 L0 task slices | `runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/vis/v738_l0_direct_tasks_strict_20260715/completion/metrics/std_cfg1.0_eta0.0/render_summary.json` | same 8 fixed pure samples | same L0 step105k human-text-only、camera-from-GT-H、joint parallel/cascade | H/C strict single world/projection/concat MP4 与 trajectory PNG；Direct H projection 的 GT camera 仅作外部显示 | complete；80 MP4、16 PNG；`L0 task slices` tab on 4090 port `7865` |
| Completion peer registry | `configs/completion_vis_registry.json` | same 8 fixed pure samples | separate `Human completion` / `Camera completion` tabs；L0 ready，specialist/baseline placeholders | human 固定 world camera；camera 对 GT human projection；每页同步播放、paired human/camera text 与逐列 asset 状态 | active；ready assets `missing=0`；4090 port `7865` |
| Stage2 L0 single-step gate | `runs/stage2/v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715/vis/l0_single_step_gate_20260715/render_summary.json` | same 8 fixed pure samples | `human`、`camera`、`joint` × raw GT / `t=999,799,599,399,199` | teacher-forced one-step `pred_x0` 的 world/projection MP4 与 geometry PNG | complete；288 MP4、120 PNG；仅作局部诊断，raw-loss gate 已取消（无效） |
| Stage2 C3-25 Human-view architecture screen | `runs/vis/stage2/<H-FULL-or-H-ISOLATED>/architecture_view_{gradio_full,single_step}_r3_20260723/` | fixed 8 + frozen C3-25 joint Top-5；union 13 | Parent C3-25、H-FULL、H-ISOLATED × Direct-H、Direct-C、joint；single-step 为 raw GT + `t=999,799,599,399,199` | world-skeleton / camera-projection MP4、trajectory PNG、exact Human-view contract | active screen-only；r1/r2 invalid outputs excluded，r3 接入 4090 port `7865` |
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
| 4 | Director-C camera completion single assets | corrected Director-C fixed endpoint 与 formal pure4053 已完成并通过；`Camera completion` 已有显式 placeholder | 只从 endpoint SHA `ad2756…e823` 与同一 fixed-8 IDs 生成 GT-human projection，再填 registry；prelaunch smoke 不得展示 |
| 5 | v7.42 H/C specialist single assets | formal 已完成，但当前无 single assets；两个 completion tab 已分别预留列 | 使用各自 fixed endpoint 与同一 fixed-8 IDs；H 用 fixed camera，C 用 GT human |
| 6 | MotionLab-MFT / MoMask-Pulp human single assets | MotionLab formal/geometry已完成但world-root未胜L0；MoMask三阶段fixed endpoint已完成但formal adapter未闭合；`Human completion` 已有两个独立 placeholder | MotionLab可按fixed endpoint生成诊断资产；MoMask等formal闭合后再补，不以未评测endpoint补格 |
| 7 | CCD-Pulp camera single assets | fixed endpoint 与 formal pure4053 已完成；`Camera completion` 仍为显式 placeholder | 对同一 fixed-8 GT human 渲染 camera 后再填列；记录 adapter/checkpoint/sample hash |
| 8 | Pulp official Stage1 recon visual | v6.3 要验证 official ckpt 是否可复现，需要 qualitative upper bound | done in `v7_13_pulp_ae_official_selftrained_stage1_bigtitle_20260709`; remaining work is human last-frame inspection |

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

| version / run | tokenizer | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v7.32 / `v7_32_separate_local_ae_500ep_seed17_5090_20260713` | separate AE | 268.92 | 12.503 | 67.3% | 22.81 | 61.035 | 83.6% | 0.931 | 14.5% |
| v7.32 / `v7_32_separate_local_vae_500ep_seed17_5090_20260713` | separate VAE | 208.39 | 14.673 | 79.7% | 15.01 | 63.650 | 89.6% | 0.927 | 13.4% |

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

## 16. 2026-07-15 旧 P0-G(raw-loss)、Direct H 与 HumanML3D 最终验收

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
  目录名中的 `gate` 是历史 artifact 命名，不代表一个有效 raw-loss 实验 gate。

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

## 17. 2026-07-16 completion peer tabs

### 17.1 Display contract

- `Human completion` 与 `Camera completion` 现在是独立 tab，不再依赖一个 target
  radio 混合解释。
- human 页的 ready 两列为 GT 与 L0 Direct H，均读取固定 world-skeleton view；
  camera text 仍显示为 paired-sample context，但 Direct H 是 human-text-only，不读取
  camera latent 或 camera text。
- camera 页的 ready 两列为 GT camera + GT human 与 L0 Direct C；Direct C 的 renderer
  明确令 `render_joints = gt_joints`，因此生成 camera 始终作用于 GT human，而不是
  同时生成的人体。
- 两页均显示 `sample_id`、valid frames、human text 与 camera text，并提供
  `▶ 同步播放当前组`。同步脚本只控制当前可见 tab 的 video elements，统一归零后播放。

### 17.2 Baseline placeholders

`configs/completion_vis_registry.json` 是 completion 页的唯一列注册表。当前每页五列：

- human：GT、L0 Direct H 已填；v7.42 human specialist、MotionLab-MFT、MoMask-Pulp
  保持显式 placeholder；
- camera：GT、L0 Direct C 已填；v7.42 camera specialist、Director-C、CCD-Pulp
  保持显式 placeholder。

不存在的 asset 返回空视频格并在状态表写明原因，不影响同页已有列。baseline 到 fixed
endpoint 后只需把同一 fixed-8 sample 的 `path_template` 填入 registry；不得用 smoke、
半程 checkpoint 或不同 sample 顶替。

### 17.3 Validation and service

- `--validate-only`：4 runs、11 summaries、8 samples、2 completion modes、1,064
  required ready files、`missing=0`。
- 两个 completion callback 均实测返回 paired human/camera text 与两条 ready media；
  human 路径解析到 `gt_skeleton.mp4` / `human_skeleton.mp4`，camera 路径解析到
  `gt_camera_projection.mp4` / `camera_camera_projection.mp4`。这些文件属于此前已完成
  80/80 decode 的 L0 direct-task asset set，本次没有重新编码视频。
- 该次 completion-only build smoke 得到 298 components 与九个 tab；旧 statistical
  Top-5 版本曾为 326 components，当前 geometry-specialist 版本见 18.3。

## 18. 2026-07-17 L0 joint geometry Top-5 `2 × 3`

### 18.1 Ranking contract

排序来源是 L0 `joint_parallel` 的同一 pure4053 formal sampler：checkpoint
`ab474d…f35`、DDIM50、CFG1、`eta=0`、seed17、human-first routing 与
`c_to_h_blocked`。新跑的 31 个 aggregate metrics 与原 L0 formal 逐项完全一致，最大绝对差
为 `0.0`；experiment-contract audit 通过。

旧 TMR/CLaTr/in-frame 排名无法代表单样本几何质量，已降级且不再由 Gradio 读取。当前逐样本口径为：

- human-only：`reverse_percentile(root-aligned H-MPJPE)`；
- camera-only：`reverse_percentile(camera-center ADE)`；
- joint：上述两个 reverse percentile 的等权均值。

H-MPJPE 逐帧去除 human root 后比较生成与 paired GT joints；Cam-ADE 比较生成与 paired GT
camera centers。TMR、CLaTr 与 in-frame 仍显示，但不参与选择；集合级 FID/coverage/density同样
不参与。未过滤短序列，页面显式显示 valid frames。该选择服务于几何对齐检查，不等价于自然度、
文本一致性或无偏总体质量估计。

### 18.2 Top-5 samples

| rank | human-only ID | H-MPJPE | camera-only ID | Cam-ADE | joint ID | H-MPJPE / Cam-ADE |
| ---: | --- | ---: | --- | ---: | --- | ---: |
| 1 | `2015_fSu5W0BtXG8_00006_001_a` | 0.0345 | `2017_PXmtu0Kd0ms_00008_000_a` | 0.0842 | `2015_F0KcFyR2uAc_00009_000_a` | 0.0556 / 0.3231 |
| 2 | `2015_S58poUaNwiw_00051_000_a` | 0.0391 | `2011_v-0Z_0SUtJw_00031_000_a` | 0.0928 | `2014_LJAUOJDM88o_00005_000_a` | 0.0754 / 0.2608 |
| 3 | `2018_MYkSUEjYLc0_00006_000_a` | 0.0412 | `2015_7okueIbuBDE_00028_002_b` | 0.1186 | `2012_NRjWEE0hmjQ_00023_002_a` | 0.0581 / 0.3438 |
| 4 | `2014_R2zNRrOXbPY_00010_001_a` | 0.0459 | `2011_tetwGGL997s_00033_001_a` | 0.1381 | `2011_2O-CC3IVPVg_00033_000_a` | 0.0632 / 0.3513 |
| 5 | `2014_R6-LDKl3FOs_00014_000_a` | 0.0479 | `2017_yk5d161ytXE_00027_000_a` | 0.1456 | `2011_BFUVGfsVzhQ_00023_000_a` | 0.0816 / 0.2811 |

三组共 15 个 unique IDs。human-only 不约束 camera，camera-only 不约束 human；joint 才同时要求
两项几何误差位于低端。因排名由 L0 自身选样，页面上的 L0/specialist 逐样本胜负不得外推为总体
方法比较；总体结论仍使用 pure4053 formal。

### 18.3 Visual contract and artifacts

每个选择项固定六格。此次只替换旧第二行第一格的重复 GT；第二、三格继续保留 Pulp reconstruction/generation：

| row | column 1 | column 2 | column 3 |
| --- | --- | --- | --- |
| StoryMotion | raw paired GT | corrected v7.14 joint-AE owning recon | L0 directed joint parallel |
| specialist / Pulp | v7.42 exposure-matched joint specialist parallel | Pulp official owning reconstruction | Pulp official Aux generation |

每格同时提供 world-skeleton 与 camera-projection MP4；页面显示 human text、camera text、TMR、
CLaTr、in-frame、H-MPJPE 与 Cam-ADE，并提供 `▶ 同步播放当前组`。第二行第一格必须使用 joint
specialist；H/C direct specialist 的 observation contract不同，不能替代 joint-mode同任务对照。页面 aggregate 表同时显示 v7.38 L0、v7.42 joint specialist、Pulp no-Aux 与 Pulp Aux 的 official pure4053 metrics；Pulp row 是 native-system baseline，不是单变量消融。

- geometry ranking：`.../v738_l0_joint_top5_20260716/per_sample_geometry_quality.json`，schema `2`，SHA256=`d26c2fe9040296ae076170515b5105b4850dcae698dbe6959825ff4dac437dc7`；
- aggregate replay：`.../v738_l0_joint_top5_20260716/full_quality_eval.json`，SHA256=`162751ac43fd8946d890cbb0dc9fd53e31719e75410ee4823349cadc5a3b0f15`；
- specialist comparison summary：`.../v738_l0_joint_top5_20260716/comparison_geometry_specialist/render_summary.json`，SHA256=`a5107469c182644d57f4b4cf5b83b093e7d29de3d6f013a2d2800ca7ffd76a9c`。
- Pulp comparison summary：`.../v738_l0_joint_top5_20260716/comparison_geometry_pulp/render_summary.json`，SHA256=`b1662c1325d26b7a5712eeca64c7eaee65c51b970addc1cc267351efca0b2b17`。
- 旧 statistical ranking保留作 provenance，但页面不再读取；geometry specialist 与 geometry Pulp summaries 的 15 个 IDs/order 已严格匹配。

媒体完整性使用 `imageio-ffmpeg` bundled binary做实际 decode；主机未安装系统
`ffmpeg`/`ffprobe`，不能把 command-not-found 误写为 codec 失败。

最终验收：15 个 unique samples、三组各 5 条且 ranking IDs 与 samples 完全一致；specialist set 的
120 个 MP4 已解码 `120/120`，新增 Pulp set 的 150 个 MP4 已解码 `150/150`、失败 `0`。`--validate-only`
扫描 4 runs、11 summaries、8 个 fixed samples、2 个 completion modes、15 个 Top-5
samples 与 1,245 个 required files，`missing=0`。30 个 Top-5 callback views（15 选择 ×
2 视图）均返回六个存在的媒体路径；Gradio build 为 313 components，HTTP `/config`
返回十个 tab并包含 `Joint Top-5 · 2×3`。配置中的四处 `HumanML3D` 文本全部只属于
独立 HumanML3D tab；其他页面和 callback不再返回相关内容。服务 PID `1379105` 已重载于 4090
`127.0.0.1:7865`；转发命令保持不变。

浏览器层再用 headless Chromium 经 SSH tunnel 等待 `networkidle` 后打开 Top tab：10 个 tab 均可发现，六个目标 label 全部 visible，visible video count=`6`，page errors=`0`、console errors=`0`。实际截图确认第二行视觉顺序为 joint specialist gen、Pulp recon、Pulp Aux gen，aggregate 表同时含 Pulp no-Aux/Aux。

## 19. 2026-07-23 C3-25 Human-view architecture desk

### 19.1 Evidence boundary

本页只登记可视化资产与服务验收。H-FULL、H-ISOLATED 和 Parent C3-25 的 matched
`N=512` 三模式 screen 数字、hashes 与 architecture 裁决由
[[archived/diagnostics/2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder_closed-through-human-only_20260724#H-axis 两端点 N=512 screen（2026-07-23）]]
唯一持有；这些 screen 不进入正式 metric ledger。Gradio 的 v7.38 L0 row 只提供
former-mainline 历史视觉上下文，不混入该 matched 数字表，也不改变 C3-25 seed17
`105K` 的 mainline 身份。

两个 fresh Stage2 endpoint 为：

- H-FULL：`p0_c3_25_unified3_hview_full_0_105k_seed17_4090g0_20260722`，
  checkpoint SHA256=`63c2e96dc685c1b1d447de334c77f1df18867d9b5243b114fbfb857da879999a`；
  Direct-H 与 joint-H 均恢复为 `[H_t,C_t] + [e_C,e_H]`。
- H-ISOLATED：`p0_c3_25_unified3_hview_isolated_0_105k_seed17_4090g1_20260722`，
  checkpoint SHA256=`04ad0044870498f1c5a49e9048b02b6792c0b2644cf878df354e299bb53649e4`；
  Direct-H 与 joint-H 均恢复为 `[H_t,0] + [0,e_H]`。

### 19.2 Renderer invalidation 与 fresh r3

精确 bug provenance 只见 [[version_family#Bug 与 invalidation provenance]]。展示层的
artifact 裁决如下：

- `architecture_view_gradio_full_20260723` 的 r1 只渲染默认三个 ID，保留为不完整
  launch provenance。
- `architecture_view_gradio_full_r2_20260723` 虽各有 13 个 ID，但 prompt-off 手工
  loader 实际使用默认 `mixed` Human view，因此两份 summary
  `3141bc53…0d1 / 3555851f…164` 永久禁止展示。
- `architecture_view_single_step_r2_20260723` 在发现同一 loader 问题后中止，H-FULL /
  H-ISOLATED 分别保留 `166 / 168` 个 partial files，无完成 summary。
- 所有 r1/r2 目录、summary 与日志原样保留；页面只读取全新的 r3 路径，未覆盖或删除
  任何历史文件。

有效 r3 资产为：

| arm | full render summary SHA256 | full files | single-step summary SHA256 | single-step files |
| --- | --- | ---: | --- | ---: |
| H-FULL | `ef09530f3d701afcf4789c9ec9851f0e67189e92e05d2b5c92daec20d890dcad` | `222` = 182 MP4 + 39 PNG + summary | `e443ede34dc28dd8bd86b52c7a1bd56893cfdd947e229dc4328c7455bc5cebdc` | `409` = 288 MP4 + 120 PNG + summary |
| H-ISOLATED | `6e19af51ddb4963ebf6075b696ff4ca3e5348ab29b0a918fb302d8bee08014b3` | `222` = 182 MP4 + 39 PNG + summary | `74ae27ec5c8ccfa075f94a801931304f63b058af64c2851cf25f1030b37455cc` | `409` = 288 MP4 + 120 PNG + summary |

full render 使用固定 8 个 display IDs 加冻结的 C3-25 joint Top-5，去重后共 13 个
ordered IDs；协议为 DDIM50、CFG1、`eta=0`、seed17。single-step 使用相同 fixed-8，
每个 task 显示 raw GT 与 `t=999,799,599,399,199` 五个 teacher-forced
`q(z_gt,t) → one pred_x0` 结果。两类 summary 都绑定 exact checkpoint SHA，并显式
记录完整 `human_view` contract 及 Camera latent/text conditioning flags。

修复后代码 SHA256：

- `scripts/render_bilateral_results.py`：`3f4e76628ab0de857762ba5bc52805526b87bac560373a4b1a570afb8580cc8d`；
- `scripts/render_l0_single_step_gate.py`：`463b69fa4532155f695ca249e87aa57d51846c3179fc713d6c31d9e9a5d0f107`；
- `scripts/v736_p0_matched_gradio.py`：`05206dbba4393d2d5552d7c8720552800d3e25b05be8448df7600f0c4f3f63be`。

三个脚本在 4090 与 5090 的 byte SHA 相同。renderer 会恢复 checkpoint
`human_view_mode`、与记录的完整 contract 做 exact comparison，并在加载后再次校验
model attribute；Gradio 进一步检查 checkpoint SHA、ordered IDs、Human-view contract
及三项 conditioning flags，任一不一致即 fail-close。

### 19.3 Tabs、layout 与验收

五个标签页最终命名与可见媒体数为：

| tab | layout | visible videos |
| --- | --- | ---: |
| `H Completion · Architecture` | frozen GT/C3-25/L0 row + H-FULL row + H-ISOLATED row | 9 |
| `C Completion · Architecture` | frozen GT/C3-25/L0 row + H-FULL row + H-ISOLATED row | 9 |
| `Joint Top-5 · Architecture` | GT、C3-25、L0、H-FULL、H-ISOLATED 各一行；projection/skeleton 两列 | 10 |
| `Single-step · Architecture` | C3-25、H-FULL、H-ISOLATED 三个分割区；每区 raw GT + 五个 timestep | 18 |
| `HumanML3D · Stage1` | 独立 Stage1 adapter 边界 | 2 |

最终验收：

- `--validate-only`：13 个 render IDs、8 个 single-step IDs、3 个 six-video groups、
  `required_files=1206`、`missing=0`，三份 screen manifest 的 ordered-ID SHA256 均为
  `6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df`。
- fresh r3 新增媒体使用 renderer 所属 FFmpeg `7.0.2` 实际解码首帧：
  MP4=`940/940`、失败 `0`；PNG=`318/318` verify、失败 `0`。
- `_private/storymotion_architecture_view_gradio_smoke.py` 经 SSH tunnel 运行 headless
  Chromium：五个 tab 的 exact label、row headings 与上述 visible-video 数全部通过；
  page errors=`0`、console errors=`0`。
- 新服务 PID `3904710` 运行于 4090 port `7865`；Mac 转发仍为
  `ssh -N -L 7865:127.0.0.1:7865 4090`。

## 20. 2026-07-29 v10 GT／Human reconstruction／v10-v9 Human teacher

### 20.1 Evidence与展示边界

4090 evidence root：

```text
runs/vis/stage2/
  v10_hrelcam_phasea210k_human_teacher105k_seed17_4090g1_20260729/
    gt_hrecon_v10v9_teacher_cfg1_cfg3_fixed8_r4_20260729/
```

首标签页仍命名为`v10 · GT / H recon / teacher`。每个fixed ID显示六个standalone MP4，按三行两列排列：

1. Pulp pure-test GT Human；
2. exact Phase-A `210K` frozen Human owner的deterministic reconstruction；
3. v10 Phase-A-owner Stage2 Human-text-only teacher `105K`的CFG1输出；
4. v9 Phase-C-owner Stage2 Human-text-only teacher `105K`的CFG1输出；
5. 同一v10 teacher checkpoint的CFG3输出；
6. 同一v9 teacher checkpoint的CFG3输出。

六路使用完全相同的8个sample ID、raw length、GT Human tensor与per-sample world display bounds。manifest同时校验Stage1 fixed source、两条teacher checkpoint、各自owning decoder以及CFG1／CFG3字段；任一来源、角色、视频SHA或non-causal字段不符即fail-close。CFG1与CFG3是同一teacher checkpoint的两种inference guidance，不是四条独立训练run。artifact与implementation SHA只见 [[Storymotion-exp-sha]]。

> [!warning] Claim boundary
> 第二路虽然从旧三项loss Phase-B final-210K fixed artifact读取，但其Human branch与Phase-A owner逐元素exact；这里只把它作为Stage1 Human reconstruction，不把该文件当Camera证据。四条teacher视图使用相同ViMoGen-light topology与`105K`配方，但v10与v9分别属于Phase-A `210K`与Phase-C `636K` Human owner；其raw cache／train-only statistics不等价，不能复用teacher权重。精确owner审计见 [[StoryMotion-valid-metric-ledger#5.6 v9／v10 Human teacher owner非等价审计]]。本标签没有v10 Camera generation、Direct-C、sequential joint、synchronous joint或Unified-3证据。

### 20.2 验收与服务

- visual manifest SHA只见 [[Storymotion-exp-sha]]；`status=rendered`、8个ordered IDs、每ID恰有`gt / human_reconstruction / v10_human_teacher_cfg1 / v9_human_teacher_cfg1 / v10_human_teacher_cfg3 / v9_human_teacher_cfg3`六种role；
- renderer所属FFmpeg `7.0.2`完整解码MP4=`48/48`，失败=`0`；
- Gradio `--validate-only`：`required_files=1452`、`missing=0`、`v10_human_compare_samples=8`；
- headless Chromium：exact tab label、六个heading、8个sample options、六路媒体HTTP、切换第二样本与同步播放全部通过；page errors=`0`、console errors=`0`、unexpected failed requests=`0`；
- 当前4090服务PID=`1316999`，监听`0.0.0.0:7865`，HTTP=`200`；日志为`/tmp/storymotion_gradio_7865_v10v9_cfg13_20260729.log`。

## 21. 2026-08-03 Paper A Pulp Camera 512条人工审核

该界面只服务`paperA_pulp_trimotion_geometry_screen_n512_seed17_20260803`，不调用LLM，
也不修改source `records.jsonl`或geometry contract。固定cohort为完整512条；风险优先、原文本冲突、
阈值边界与未审核filter只改变浏览顺序，不改变样本集合。

每条显示raw Camera text、symbolic phases、阈值／confidence、QC reason、C1REL三个正交轨迹投影及
平移／旋转时序。人工字段包括Camera坐标约定、symbolic verdict、corrected primitives、阈值、
phase segmentation、raw-text agreement与备注。每次保存向`human_reviews.jsonl`追加独立事件；
同一reviewer重审不会覆盖旧事件。review contract要求512／512完成，并裁决全部方向／坐标轴错误、
拒绝项和`无法判断`后，才允许冻结full-data threshold或canonical text。

4090 artifact root：

`runs/artifacts/paperA_camera_recaption/paperA_pulp_trimotion_geometry_screen_n512_seed17_20260803/`

- source records约3.19 MB，512条，LLM calls=`0`，SHA256=
  `3a9788293e1003cfabf244a3726d18f0db55072e4e309cb9c1568116cfd9843a`；
- review contract：`human_review_contract.json`，SHA256=
  `24981e98f43d4e74bc7ae75f5c0b4cd258a230824fd4cfc1acd522668f5fe0d2`；
- append-only output：`human_reviews.jsonl`；
- service：PID=`5935`，`0.0.0.0:7868`，HTTP=`200`；
- SSH转发：`ssh -N -L 7868:127.0.0.1:7868 4090`，浏览器打开`http://127.0.0.1:7868`。
