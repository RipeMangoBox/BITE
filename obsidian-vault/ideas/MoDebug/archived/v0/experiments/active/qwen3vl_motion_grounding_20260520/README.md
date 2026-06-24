---
title: "Qwen3-VL Motion Event Grounding on L40"
created: 2026-05-20T15:08:00+08:00
updated: 2026-05-21T15:16:13+08:00
type: experiment_record
status: active
tags:
  - MoDebug
  - Qwen3_VL
  - motion_event_grounding
  - VLM_side_signal
remote_host: L40
remote_root: /sata/public/ripemangobox/Motion/researchflow/qwen3vl_grounding_20260520
local_artifact_root: artifacts/remoteL40/qwen3vl_grounding_20260520
local_32b_q8_artifact_root: artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_llamacpp
local_32b_q8_mp4_artifact_root: artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_mp4_contactsheet
local_bf16_true_video_artifact_root: artifacts/remoteL40/qwen3vl_grounding_20260520_bf16_true_video
local_vllm_newenv_artifact_root: artifacts/remoteL40/qwen3vl_grounding_20260521_vllm_newenv
evidence_role: cross_check
used_for: observation
limitations: |
  Qwen3-VL grounding is a side signal for event-window inspection. It is not a final evaluator, not a held-out metric, and not a replacement for human or geometry-grounded verification.
---

# Qwen3-VL Motion Event Grounding on L40

## 目标

在 L40 上部署 Qwen3-VL，并用已渲染 motion sequence 资源尝试 event grounding：输入 `gt_motion.mp4`、全局轨迹图和 `0.5s` triplet sheet，要求模型为给定 event 输出候选时间窗、可见性、置信度、视觉证据和限制。

## 部署记录

- 官方仓库：`researchflow/qwen3vl_grounding_20260520/repos/Qwen3-VL`
- 官方仓库 commit：`96588727e44c78b25ba03ea03b8e12f7e64fd0da`
- 远端环境：`/sata/public/ripemangobox/Motion/envs/qwen3vl`
- Python：`3.10.12`
- PyTorch：`2.5.1+cu121`
- Transformers：`4.57.6`
- qwen-vl-utils：`0.0.14`
- decord：`0.6.0`
- 8B 模型：`llm_cache/Qwen3-VL-8B-Instruct`
- 32B BF16 模型：`llm_cache/Qwen3-VL-32B-Instruct`
- 32B Q8 模型：`llm_cache/Qwen3-VL-32B-Instruct-GGUF-Q8_0`
- 32B Q8 runtime：`llama.cpp` `llama-mtmd-cli`，CUDA build，`GGML_CUDA=ON`

> [!note] 环境修正
> 初始尝试安装 `transformers` 主分支得到 `5.8.0.dev0`，但它导入了当前 `torch==2.5.1` 没有的 FSDP API。已切回官方要求范围内的 `transformers==4.57.6`，导入探针通过。

## 输入样本

来自 [[paperIDEAs/MoDebug/experiments/retained_assets/vlm_pilot_20260516|MoDebug VLM切片标注实验总览]] 的三个 retained pilot 样本：

- `011798`：长程往返轨迹样本。
- `Q_009402`：短转身和回起点样本。
- `V_004012`：单腿上抬、踢出、收回样本。

远端输入路径：

```text
researchflow/qwen3vl_grounding_20260520/inputs/vlm_pilot_assets/artifacts/experiments/modebug/vlm_caption/modebug_vlm_slice_caption_pilot_20260513/
```

本地取回结果：

```text
artifacts/remoteL40/qwen3vl_grounding_20260520/
```

## 运行命令

```bash
CUDA_VISIBLE_DEVICES=0 python researchflow/qwen3vl_grounding_20260520/scripts/ground_motion_events_qwen3vl.py \
  --model-path llm_cache/Qwen3-VL-8B-Instruct \
  --inputs-root researchflow/qwen3vl_grounding_20260520/inputs/vlm_pilot_assets \
  --output-dir researchflow/qwen3vl_grounding_20260520/outputs/qwen3vl_8b_both_3samples \
  --sample-ids 011798 Q_009402 V_004012 \
  --mode both \
  --max-new-tokens 1400 \
  --device-map auto \
  --attn-implementation sdpa
```

关键日志：

- `artifacts/remoteL40/qwen3vl_grounding_20260520/qwen3vl_8b_grounding_full_20260520.log`
- `artifacts/remoteL40/qwen3vl_grounding_20260520/qwen3vl_verify_results_20260520.log`
- `artifacts/remoteL40/qwen3vl_grounding_20260520/qwen3vl_transformers_stable_20260520.log`

## 结果

输出文件：

- `artifacts/remoteL40/qwen3vl_grounding_20260520/outputs/qwen3vl_8b_both_3samples/grounding_results.jsonl`
- `artifacts/remoteL40/qwen3vl_grounding_20260520/outputs/qwen3vl_8b_both_3samples/grounding_results.md`
- `artifacts/remoteL40/qwen3vl_grounding_20260520/outputs/qwen3vl_8b_both_3samples/manifest.json`

JSONL 核验：3 行均可解析，`parse_error=None`；事件数分别为 `011798: 6`、`Q_009402: 4`、`V_004012: 4`。

| 样本 | Event | Qwen3-VL 时间窗 | 状态 | 置信度 | 事件 |
|---|---:|---|---|---:|---|
| `011798` | E1 | `0.0-1.0s` | visible | 0.95 | standing or preparing at the start |
| `011798` | E2 | `1.0-2.5s` | visible | 0.90 | turns and steps backwards |
| `011798` | E3 | `2.5-5.0s` | visible | 0.90 | jogs/runs away from the start |
| `011798` | E4 | `5.0-6.0s` | visible | 0.85 | turns around about 180 degrees |
| `011798` | E5 | `6.0-7.0s` | visible | 0.90 | jogs/runs back toward the start |
| `011798` | E6 | `7.0-7.55s` | visible | 0.90 | stops and returns close to the original stance |
| `Q_009402` | E1 | `0.0-1.5s` | visible | 0.95 | walks forward away from the start |
| `Q_009402` | E2 | `1.5-2.0s` | visible | 0.90 | turns around |
| `Q_009402` | E3 | `2.0-2.95s` | visible | 0.90 | continues walking back toward the start |
| `Q_009402` | E4 | `2.95-3.0s` | visible | 0.95 | stops near the original location |
| `V_004012` | E1 | `0.0-0.5s` | visible | 0.95 | starts from a neutral stance |
| `V_004012` | E2 | `1.0-2.0s` | visible | 0.90 | raises or kicks one leg |
| `V_004012` | E3 | `2.0-2.5s` | visible | 0.85 | holds or reaches the peak leg extension |
| `V_004012` | E4 | `2.5-4.0s` | visible | 0.90 | lowers the leg and returns to neutral stance |

## 观察

1. `mode=both` 可运行，日志显示 `qwen-vl-utils using decord to read video`，说明视频输入路径已经接入。
2. Qwen3-VL-8B 在 L40 GPU0 上可完成三样本 grounding；image-only smoke 占用约 20GB 显存，video+images 正式运行约 22GB 显存。
3. `Q_009402` 的短转身和回起点输出与 retained pilot note 的人工检查方向一致：前行、转身、返回、停止都能被分段。
4. `011798` 和 `V_004012` 的时间窗可作为人工复核候选，但模型给出的边界仍偏粗，尤其是长程往返中的 jog/turn 边界和单腿动作 peak。
5. 早期 smoke 使用 `max_new_tokens=500` 导致 JSON 截断；正式运行提高到 `1400` 后 3 条结果均可解析。

## 证据边界

- role：`cross_check`
- used_for：`observation`
- evaluator：`Qwen3-VL-8B-Instruct`
- protocol：给定 event list + video + trajectory/progression sheets，输出候选时间窗和视觉证据
- n/evaluable：`3/3`
- coverage：`011798`、`Q_009402`、`V_004012`
- limitations：
  - 不作为 formal ordering evidence。
  - 不作为 held-out final evaluator。
  - 不判断精确步数、左右脚身份或严格运动学边界。
  - 输出时间窗需要人工或几何信号复核。

## 32B Q8 状态

用户要求同时下载 8B 和 32B，32B 若可行用 Q8 量化。当前使用官方 GGUF 仓库中的 Q8 文件：

- `Qwen/Qwen3-VL-32B-Instruct-GGUF`
- `mmproj-Qwen3VL-32B-Instruct-Q8_0.gguf`
- `Qwen3VL-32B-Instruct-Q8_0.gguf`

截至 `2026-05-20T15:10:32+08:00`，官方元数据中的目标文件大小为：

- `Qwen3VL-32B-Instruct-Q8_0.gguf`：`34,817,720,352` bytes
- `mmproj-Qwen3VL-32B-Instruct-Q8_0.gguf`：`772,360,224` bytes

当前 32B Q8 下载已完成，远端完成证明：

```text
researchflow/qwen3vl_grounding_20260520/provenance/32b_q8_download_complete.txt
```

本地抓回完成证明：

```text
artifacts/remoteL40/qwen3vl_grounding_20260520/32b_q8_download_complete.txt
```

完成时间：`2026-05-20T16:08:20+08:00`。文件核验：

- `.gitattributes`：`1,976` bytes
- `README.md`：`7,860` bytes
- `mmproj-Qwen3VL-32B-Instruct-Q8_0.gguf`：`772,360,224` bytes
- `Qwen3VL-32B-Instruct-Q8_0.gguf`：`34,817,720,352` bytes

## 32B Q8 测试结果

`2026-05-20T17:00:00+08:00` 已在 L40 上从源码构建 `llama.cpp` 的 `llama-mtmd-cli`，CUDA 目标使用 `gcc-11/g++-11` 避开本机 `nvcc 11.8` 与 `gcc 12.3` 的兼容问题。

> [!note] runtime 选择
> 对当前已下载的 Qwen3-VL-32B Q8 GGUF 权重，最直接可控的测试路径是 `llama.cpp` / `llama-mtmd-cli`。`Ollama` 也可加载 GGUF，但不方便记录细粒度多模态参数和原始日志；`vLLM` 更适合后续 API serving，而本轮先以官方 GGUF CLI 路线完成可复现实验。

远端输出路径：

```text
researchflow/qwen3vl_grounding_20260520/outputs/qwen3vl_32b_q8_llamacpp_3samples/
```

本地取回路径：

```text
artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_llamacpp/qwen3vl_32b_q8_llamacpp_3samples/
```

运行协议：

- model：`Qwen3VL-32B-Instruct-Q8_0.gguf`
- mmproj：`mmproj-Qwen3VL-32B-Instruct-Q8_0.gguf`
- backend：`llama.cpp` `llama-mtmd-cli`
- input：每个样本的 `slice_0p5s_triplets_global_trajectory.png`
- generation：`-ngl all`、`-c 4096`、`--image-min-tokens 1024`、`--image-max-tokens 2048`
- role：`cross_check`
- used_for：`observation`

本轮是 sheet-based grounding，不是 `gt_motion.mp4` 视频输入测试。

JSONL 核验：`3/3` 可解析，事件数分别为 `011798: 6`、`Q_009402: 4`、`V_004012: 4`。`011798` 的完整 schema 首次输出被 token 截断，随后用 compact schema 单独重跑并解析成功。

| 样本 | Event | 32B Q8 时间窗 | 状态 | 置信度 | 事件/证据 |
|---|---:|---|---|---:|---|
| `011798` | E1 | `0.0-0.5s` | visible |  | Standing still at start, minimal movement in s1 |
| `011798` | E2 | `0.5-1.5s` | visible |  | Body rotates and steps backward, visible in s2-s3 |
| `011798` | E3 | `1.5-4.0s` | visible |  | Forward jogging motion with leg swing, seen in s4-s8 |
| `011798` | E4 | `4.0-5.0s` | visible |  | 180-degree turn, body rotates back, visible in s9-s10 |
| `011798` | E5 | `5.0-7.0s` | visible |  | Jogging backward toward start, legs moving in reverse, s11-s14 |
| `011798` | E6 | `7.0-7.5s` | visible |  | Slows and stops near original position, s15-s16 |
| `Q_009402` | E1 | `0.0-1.5s` | visible | 0.90 | walks forward away from the start |
| `Q_009402` | E2 | `1.5-2.0s` | visible | 0.85 | turns around |
| `Q_009402` | E3 | `2.0-3.0s` | visible | 0.90 | continues walking back toward the start |
| `Q_009402` | E4 | `2.5-3.0s` | visible | 0.80 | stops near the original location |
| `V_004012` | E1 | `0.0-0.5s` | visible | 0.90 | starts from a neutral stance |
| `V_004012` | E2 | `1.0-1.5s` | visible | 0.85 | raises or kicks one leg |
| `V_004012` | E3 | `2.5-3.0s` | visible | 0.90 | holds or reaches the peak leg extension |
| `V_004012` | E4 | `3.5-4.0s` | visible | 0.85 | lowers the leg and returns to neutral stance |

关键运行日志：

- `artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_llamacpp/qwen3vl_32b_q8_3samples_20260520.log`
- `artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_llamacpp/qwen3vl_32b_q8_3samples_resume_20260520.log`
- `artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_llamacpp/qwen3vl_32b_q8_011798_compact_20260520.log`

主要观察：

1. 32B Q8 + Q8 `mmproj` 可在单张 L40 上完成 image-sheet grounding；运行中 GPU1 约占用 `35GB` 显存。
2. `Q_009402` 的 32B Q8 窗口与 8B `mode=both` 大体一致，均能切出前行、转身、返回和停止。
3. `011798` 的 32B Q8 给出更早的 jog/turn 边界，和 8B 结果存在差异，适合作为人工复核候选而不是结论。
4. `V_004012` 的 32B Q8 将 peak leg extension 放在 `2.5-3.0s`，比 8B 的 `2.0-2.5s` 更晚；该差异需要用 frame-level 或几何信号复核。
5. `llama-server` 目标构建因 UI 资源下载超时失败，但 `llama-mtmd-cli` 已成功构建并完成本轮推理；如需 API 服务，可用 `LLAMA_BUILD_UI=OFF` 重新构建 server。

## 32B Q8 MP4-Derived 测试结果

`2026-05-20T18:03:24+08:00` 补跑 `gt_motion.mp4` 来源的 32B Q8 grounding。当前 `llama-mtmd-cli` help 仅暴露 `--image/--audio`，没有直接 `--video` 参数，因此本轮协议是先从每个 `gt_motion.mp4` 以 `0.5s` 间隔抽帧，生成带时间戳标签的 contact sheet PNG，再喂给 Qwen3-VL-32B Q8。

> [!warning] 与上一节区分
> 本节输入来源是 `gt_motion.mp4`，实际模型输入是 `mp4-derived contact sheet PNG`。上一节输入是预渲染的 `slice_0p5s_triplets_global_trajectory.png`，包含轨迹 sheet 信息。两个结果不可直接混作同一个 protocol。

远端输出路径：

```text
researchflow/qwen3vl_grounding_20260520/outputs/qwen3vl_32b_q8_llamacpp_mp4_contactsheet_3samples/
```

本地取回路径：

```text
artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_mp4_contactsheet/qwen3vl_32b_q8_llamacpp_mp4_contactsheet_3samples/
```

运行协议：

- source input：`gt_motion.mp4`
- actual model input：`mp4-derived contact sheet PNG with timestamp labels`
- frame sampling：`0.5s` 间隔，末帧额外补齐
- generated contact sheets：
  - `011798`：`7.55s`，`16` frames
  - `Q_009402`：`3.00s`，`7` frames
  - `V_004012`：`4.00s`，`9` frames
- model：`Qwen3VL-32B-Instruct-Q8_0.gguf`
- mmproj：`mmproj-Qwen3VL-32B-Instruct-Q8_0.gguf`
- backend：`llama.cpp` `llama-mtmd-cli`
- role：`cross_check`
- used_for：`observation`

JSONL 核验：`3/3` 可解析，事件数分别为 `011798: 6`、`Q_009402: 4`、`V_004012: 4`。

| 样本 | Event | MP4-derived 时间窗 | 状态 | 置信度 | 事件 |
|---|---:|---|---|---:|---|
| `011798` | E1 | `0.0-0.5s` | visible | 0.90 | standing or preparing at the start |
| `011798` | E2 | `1.0-2.0s` | visible | 0.80 | turns and steps backwards |
| `011798` | E3 | `2.5-5.5s` | visible | 0.90 | jogs/runs away from the start |
| `011798` | E4 | `5.5-6.0s` | visible | 0.80 | turns around about 180 degrees |
| `011798` | E5 | `6.5-7.0s` | visible | 0.80 | jogs/runs back toward the start |
| `011798` | E6 | `7.0-7.5s` | visible | 0.90 | stops and returns close to the original stance |
| `Q_009402` | E1 | `0.0-1.0s` | visible | 0.90 | walks forward away from the start |
| `Q_009402` | E2 | `1.0-1.5s` | visible | 0.80 | turns around |
| `Q_009402` | E3 | `1.5-2.95s` | visible | 0.90 | continues walking back toward the start |
| `Q_009402` | E4 | `2.95-3.0s` | visible | 0.80 | stops near the original location |
| `V_004012` | E1 | `0.0-0.5s` | visible | 0.90 | person starts in neutral stance with both legs straight and close together |
| `V_004012` | E2 | `1.0-1.5s` | visible | 0.80 | person raises or kicks one leg |
| `V_004012` | E3 | `2.0-2.5s` | visible | 0.80 | person holds or reaches peak leg extension |
| `V_004012` | E4 | `3.0-3.95s` | visible | 0.90 | person lowers the leg and returns to neutral stance |

关键输出：

- `artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_mp4_contactsheet/qwen3vl_32b_q8_llamacpp_mp4_contactsheet_3samples/grounding_results.jsonl`
- `artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_mp4_contactsheet/qwen3vl_32b_q8_llamacpp_mp4_contactsheet_3samples/grounding_results.md`
- `artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_mp4_contactsheet/qwen3vl_32b_q8_llamacpp_mp4_contactsheet_3samples/contact_sheets/`
- `artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_mp4_contactsheet/qwen3vl_32b_q8_mp4_probe_20260520.log`
- `artifacts/remoteL40/qwen3vl_grounding_20260520_32b_q8_mp4_contactsheet/qwen3vl_32b_q8_mp4_contactsheet_20260520.log`

主要观察：

1. MP4-derived contact sheet 能让 32B Q8 完成三样本 grounding，且 `3/3` JSON 可解析。
2. `Q_009402` 的转身窗口变为 `1.0-1.5s`，早于 trajectory sheet protocol 的 `1.5-2.0s`，说明是否提供全局轨迹图会影响边界判断。
3. `V_004012` 的 peak leg extension 为 `2.0-2.5s`，与 8B `mode=both` 接近，也早于上一节 32B Q8 trajectory sheet 的 `2.5-3.0s`。
4. 该结果仍是 VLM 侧信号。由于 contact sheet 是抽帧摘要，不能替代直接视频时序建模，也不能作为 held-out final evaluator。

## 下一步

1. 对 8B、32B Q8 trajectory sheet、32B Q8 MP4-derived 三组结果做人眼复核，标记边界是否过宽、过窄或语义漂移。
2. 若要继续评估 32B Q8，优先尝试真正的视频输入 runtime；当前 GGUF CLI 路线只能用抽帧 contact sheet 近似 `gt_motion.mp4`。
3. 若要长期服务化，重新构建 `llama-server` 时关闭 UI 构建，或评估 vLLM/SGLang 对 Qwen3-VL 多模态视频输入的稳定性。

## 32B BF16 True-Video Transformers Smoke

`2026-05-20T22:04:23+08:00` 尝试用 BF16 版 `Qwen3-VL-32B-Instruct` 直接读取 `Q_009402/gt_motion.mp4`，目标是验证非 GGUF、非 contact-sheet 的 true-video 输入路径。

运行协议：

- sample：`Q_009402`
- source input：`gt_motion.mp4`
- actual model input：true video tensor through `transformers` processor
- model：`llm_cache/Qwen3-VL-32B-Instruct`
- precision：`bfloat16`
- runtime：`transformers` `Qwen3VLForConditionalGeneration`
- device：`CUDA_VISIBLE_DEVICES=0,1` with `device_map=auto`
- video settings：`fps=0.25`、`max_pixels=4096`
- generation：`max_new_tokens=64`、`do_sample=False`
- role：`diagnostic`
- used_for：`observation`

结果：未产出 grounding JSON。14 个 checkpoint shard 成功加载，processor 生成的输入包含：

```text
input_ids: (1, 1189)
attention_mask: (1, 1189)
pixel_values_videos: (4400, 1536)
video_grid_thw: (1, 3)
```

随后在 generation 阶段失败：

```text
RuntimeError: CUDA error: unspecified launch failure
```

报错发生在 `transformers/models/qwen3_vl/modeling_qwen3_vl.py` 的 language model layernorm 前向路径。日志还显示当前环境缺 `torchcodec`，视频解码 fallback 到 `torchvision`，但实际崩溃点在 CUDA generation。

本地抓回证据：

- `artifacts/remoteL40/qwen3vl_grounding_20260520_bf16_true_video/qwen3vl_bf16_true_video_min64_Q_009402_20260520.log`
- `artifacts/remoteL40/qwen3vl_grounding_20260520_bf16_true_video/qwen3vl_32b_bf16_true_video_min64_Q_009402/run.log`
- `artifacts/remoteL40/qwen3vl_grounding_20260520_bf16_true_video/smoke_qwen3vl_bf16_true_video_min64.py`

结论边界：

- 这只是 runtime diagnostic，不是模型能力否定。
- 当前 L40 双卡 + `torch==2.5.1+cu121` + `transformers==4.57.6` + BF16 true-video 路线不稳定。
- 32B 可用路线仍是 Q8 GGUF + `llama-mtmd-cli` image/contact-sheet 输入；8B 可用路线是 `transformers` video+image `mode=both`。

## vLLM 安装尝试

上一轮曾启动 `qwen3vl_vllm_env_install_20260520`，尝试在现有 `envs/qwen3vl` 中安装 `vllm>=0.11.0` 和 `torchcodec`。该安装会拉取 `torch==2.11.0`、CUDA 13、`flashinfer` 等大量依赖；由于本轮已通过 8B `transformers` 与 32B Q8 `llama.cpp` 完成可复查 grounding，继续安装会增加破坏现有稳定环境的风险。

处理记录：

- `2026-05-20T22:59:00+08:00` 左右手动停止 tmux：`qwen3vl_vllm_env_install_20260520`
- 停止后 L40 只剩基础 tmux，会话无 Qwen3-VL 任务运行。
- 本地抓回日志：`artifacts/remoteL40/qwen3vl_grounding_20260520_bf16_true_video/qwen3vl_vllm_env_install_20260520.log`

后续如果要评估 vLLM/SGLang，建议新建独立环境，不复用当前已能跑 8B transformers 和 32B Q8 llama.cpp 的 `envs/qwen3vl`。

## 2026-05-21 vLLM 隔离环境检查

按“不要影响当前环境”的要求，另建隔离环境：

- 新环境：`/sata/public/ripemangobox/Motion/envs/qwen3vl_vllm_20260521`
- 旧环境：`/sata/public/ripemangobox/Motion/envs/qwen3vl`
- 新结果根目录：`/sata/public/ripemangobox/Motion/researchflow/qwen3vl_grounding_20260521`
- 本地证据：`artifacts/remoteL40/qwen3vl_grounding_20260521_vllm_newenv/`

隔离验证：

- 安装前旧环境：`torch==2.5.1+cu121`，`transformers==4.57.6`，无 `vllm`，无 `torchcodec`。
- 安装后旧环境：仍是 `torch==2.5.1+cu121`，`transformers==4.57.6`，无 `vllm`，无 `torchcodec`。
- 新环境：`torch==2.11.0+cu130`，`transformers==5.9.0`，`vllm==0.21.0`，`torchcodec==0.12.0+cpu`，`decord==0.6.0`。

闭环状态：

- 新环境的 Python/package import 层面通过，`vllm` 与 `qwen_vl_utils` 可导入。
- CUDA 初始化失败，无法进入 vLLM 模型加载和 generation 闭环。错误为：`RuntimeError: The NVIDIA driver on your system is too old (found version 12020)`。
- L40 当前驱动为 `535.288.01`；`pip install vllm>=0.11.0` 拉到的 wheel 绑定 `torch==2.11.0+cu130`，和当前驱动不匹配。
- 尝试另建 `envs/qwen3vl_vllm_cu118_20260521` 并安装 `vllm-0.11.0+cu118`，目标 wheel URL 返回 `404`，未得到可运行的 cu118 vLLM 环境。

证据文件：

- `artifacts/remoteL40/qwen3vl_grounding_20260521_vllm_newenv/provenance/old_env_before_vllm_newenv_install.txt`
- `artifacts/remoteL40/qwen3vl_grounding_20260521_vllm_newenv/provenance/vllm_newenv_versions.txt`
- `artifacts/remoteL40/qwen3vl_grounding_20260521_vllm_newenv/provenance/vllm_newenv_smoke_20260521.txt`
- `artifacts/remoteL40/qwen3vl_grounding_20260521_vllm_newenv/provenance/vllm_cu118_install_20260521.txt`

结论：

- “不影响当前环境”已闭环确认。
- vLLM runtime 生成闭环没有完成，阻断点是当前 L40 驱动与新 vLLM wheel 的 CUDA 版本不兼容。
- 若继续走官方 Qwen3-VL vLLM 路线，需要先升级 L40 NVIDIA driver，或找到/构建与当前 `535.288.01` 驱动兼容且包含 Qwen3-VL 支持的 vLLM wheel。

## 2026-05-21 L40 双卡并行检查

另开 agent 做了只读检查。当前 L40 可见两张卡：

- GPU0：`NVIDIA L40`，`46068 MiB`
- GPU1：`NVIDIA L40`，`49140 MiB`
- topology：GPU0 到 GPU1 为 `SYS`，没有 NVLink。
- 旧环境 PyTorch 可见 `2` 张 CUDA 设备。
- `torch.cuda.can_device_access_peer(0, 1)` 和 `torch.cuda.can_device_access_peer(1, 0)` 均为 `True`。

结论：

- 双卡并行基础条件存在，可以用于 tensor parallel / device-map sharding。
- 但链路是跨 CPU/NUMA 的 `SYS`，不是 NVLink；能分摊权重显存，但 TP 通信会比 NVLink 慢。
- 对后续 `Qwen3-VL-32B-Instruct` BF16 路线，双 L40 的显存容量更合理；建议优先用 HF BF16 checkpoint + vLLM `--tensor-parallel-size 2`，而不是依赖 GGUF Q8。

证据文件：

- `artifacts/remoteL40/qwen3vl_grounding_20260521_vllm_newenv/provenance/dualgpu_readonly_probe_20260521.txt`

## 2026-05-21 vLLM 下 Q8 + Video 支持边界

用户补充问题：已有 ckpt 和环境是否支持 vLLM 框架下 Qwen3-VL 的 Q8 推理处理 video 输入？

当前结论：不支持作为可用路线。

分解判断：

- Qwen 官方 README 推荐 Qwen3-VL 用 `vllm>=0.11.0` 部署，并给了 `video_url` 的 vLLM serving 示例；这说明 vLLM 的 Qwen3-VL 路线本身支持 video 输入。
- 当前 `envs/qwen3vl_vllm_20260521` 包内也存在 `vllm.model_executor.models.qwen3_vl`，且源码探针包含 `pixel_values_videos`、`video_grid_thw` 和 timestamp 相关逻辑。
- 但现有 32B Q8 checkpoint 是 llama.cpp 风格 GGUF：一个主模型 `Qwen3VL-32B-Instruct-Q8_0.gguf` 加独立 `mmproj-Qwen3VL-32B-Instruct-Q8_0.gguf` / `mmproj-Qwen3VL-32B-Instruct-F16.gguf`。
- vLLM 的 GGUF 文档把 GGUF 标为高度实验性和 under-optimized，并说明当前只支持 single-file GGUF 模型；示例是 text Qwen3 GGUF，用 base tokenizer 和可选 `--hf-config-path`。
- 本地包内检索能看到 vLLM 的 GGUF loader 和 Qwen3-VL video 模块，但没有找到 llama.cpp `mmproj` 这种双文件 VL projector 加载接口。
- 对现有 Q8 主 GGUF 做 `AutoConfig.from_pretrained(...)` dry probe 没有在有限时间内得到可用 config 结果。

因此：

- 已有 Q8 GGUF 可继续用于 `llama.cpp` 的 image/contact-sheet 近似 video grounding。
- 已有 Q8 GGUF 不应视为可在 vLLM 下处理 true-video 的 checkpoint。
- 若目标是 vLLM + true-video，建议使用 HF BF16 checkpoint `llm_cache/Qwen3-VL-32B-Instruct`，在双卡 `--tensor-parallel-size 2` 下测试；若必须 Q8/低精度，优先找 vLLM 原生支持的 HF 量化格式，例如 FP8、GPTQ、AWQ 或 compressed-tensors，而不是当前 GGUF+mmproj 组合。

## 2026-05-21 DS 迭代后的 BF16/Q8 video 闭环

本轮与 DeepSeek 迭代后，对 32B BF16 true-video 的失败点做了拆分诊断。

新增证据：

- 8B `transformers` 同脚本 `mode=video` 可以处理 `Q_009402/gt_motion.mp4`，说明样本路径、decord 解码和 Qwen3-VL processor video 输入链路是通的。
- 32B BF16 `device_map=auto` + `attn_implementation=sdpa` 在 true-video 生成时触发 CUDA `Indexing.cu` `srcIndex < srcSelectDimSize` / `device-side assert`。
- 输入侧诊断排除了 token 越界：32B `text_config.vocab_size=151936`，实际 `input_ids.max=151656`，`ids_ge_vocab_count=0`，video tensor 为 `pixel_values_videos=(3456,1536)`、`video_grid_thw=(1,3)`。
- 32B BF16 text-only + `sdpa` 也会在 language/layernorm 路径附近报 CUDA illegal instruction；32B BF16 text-only + `eager` 可生成 1 token。
- 32B BF16 true-video + `eager` 可完成 1-token 生成并写出输出，raw response 为 `" Er"`；这证明执行路径可过首 token，但不是可用语义结果。
- 32B BF16 true-video + `eager` 的 128/512 token 探针均进入生成阶段且没有复现 `sdpa` CUDA 断言，但由于双 L40 是 `SYS` 拓扑、无 NVLink，eager 生成过慢，本轮手动停止，未得到完整 JSON。

结论：

- 当前不能把 32B BF16 true-video 判为模型或 video 输入不支持；更准确说法是：`sdpa` 路径在当前 L40 软件栈不稳定，`eager` 路径可启动但太慢，未完成语义闭环。
- 当前 Q8 GGUF 仍不能作为 true-video 输入方案；`llama-mtmd-cli` 无 `--video`，直接 MP4 作为 `--image` 解码失败。
- 当前可用完整结果仍是 Q8 single-GPU 的 mp4-derived contact sheet 三样本 JSON；它是 video-derived image side signal，不是真 video temporal input。

本地证据：

- `artifacts/remoteL40/qwen3vl_video_bf16_q8_20260521/ANALYSIS.md`
- `artifacts/remoteL40/qwen3vl_video_bf16_q8_20260521_ds_iter/qwen3vl_video_8b_mode_video_knownpath_20260521.log`
- `artifacts/remoteL40/qwen3vl_video_bf16_q8_20260521_ds_iter/qwen3vl_32b_input_diag3_20260521.log`
- `artifacts/remoteL40/qwen3vl_video_bf16_q8_20260521_ds_iter/qwen3vl_32b_text_eager_1tok_20260521.log`
- `artifacts/remoteL40/qwen3vl_video_bf16_q8_20260521_ds_iter/qwen3vl_32b_bf16_eager_mode_video_1tok_Q_009402_20260521/grounding_results.md`
