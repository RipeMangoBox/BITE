# ACM 下载进度断点（2026-06-30 19:50 CST）

## 状态

- 自动下载脚本已停止：`_private/acm_queue_browser_downloader.py` 当前无运行进程。
- 停止方式：对会话 `20469` 发送 Ctrl-C。
- 中断点：第 3 批打开到第 23 个标签后收到 `KeyboardInterrupt`。
- 没有继续进入第 3 批导入阶段。
- 当前没有 `.crdownload` 或 `.part` 残留。

## 已完成落盘

统一 ACM 队列：

`obsidian-vault/batches/wait_pdf_unified_queue_20260630/edge_acm_download_queue_20260630.csv`

统计：

- 队列总数：`910`
- 已在目标 `paperPDFs` 路径存在并通过 `%PDF` 文件头检查：`56`
- 目标路径仍缺失：`854`
- 目标路径存在但不是 PDF：`0`

已完成来源：

- 单条复现样本：`1`
- 小批量验证：`5`
- 正式批次 1：`25`
- 正式批次 2：`25`

## 尚未导入但已下载

第 3 批已有 `23` 个 PDF 下载完成，仍在：

`~/Downloads/acm_sig_auto/`

这些文件尚未移动到 `paperPDFs`，后续恢复时应先导入/校验这些残留，再继续打开新链接。

| 文件 | 大小 | 标题 |
|---|---:|---|
| `3721238.3730608.pdf` | 26861687 | Guided Lens Sampling for Efficient Monte Carlo Circle-of-Confusion Rendering |
| `3721238.3730620.pdf` | 14193706 | Gaussian Fluids: A Grid-Free Fluid Solver based on Gaussian Spatial Representation |
| `3721238.3730622.pdf` | 33998666 | Fast Physics-Based Modeling of Knots and Ties using Templates |
| `3721238.3730758.pdf` | 9580068 | Gaussian Compression for Precomputed Indirect Illumination |
| `3721250.3742968.pdf` | 4034229 | From Style to Identity: AI Pipelines for Visual and Character Coherence in Film |
| `3721250.3742971.pdf` | 3942343 | Exploring AI Frame Interpolation Techniques for Watercolour Animation |
| `3721250.3742972.pdf` | 1584987 | G-FED: G-Buffer Guided Frame Extrapolation in Video Diffusion Models |
| `3721250.3742974.pdf` | 1402903 | Gaze Entropy and Driver Safety: Understanding Cognitive Failure and Situational Response Before Take-over |
| `3721250.3742987.pdf` | 2136772 | Full-Color Natural Light Holographic Video Camera |
| `3721250.3742994.pdf` | 569688 | Efficient Proxy Raytracer for Optical Systems Using Implicit Neural Representations |
| `3721250.3742995.pdf` | 728303 | Exploring Real-Time Water Surface Simulation for Immersive Virtual Reality Using Marker-Based Tracking |
| `3721250.3743005.pdf` | 1851335 | Exploring Distance Management in Immersive Combat Sports Training With Encountered-Type Haptic Feedback |
| `3721250.3743014.pdf` | 3967549 | Emulating Emulsion: A Compact Physically-Based Model for Film Colour |
| `3721250.3743020.pdf` | 1329326 | Hand Gesture-Driven Vertical Teleportation: Navigating Complex Height Differences in VR |
| `3721250.3743024.pdf` | 4351877 | Foliager: Procedural Forest Generation From Natural Language Using Scientific Data and AI |
| `3721250.3743031.pdf` | 1205037 | Evaluating Skin Tone Biases in Virtual Human Rendering |
| `3721250.3743041.pdf` | 5584063 | Evaluating the Effectiveness of Configurable Virtual Reality System for Multi-sensory Spatial Audio Training |
| `3727620.pdf` | 8242676 | Fast Determination and Computation of Self-intersections for NURBS Surfaces |
| `3730889.pdf` | 145454238 | Field Smoothness-Controlled Partition for Quadrangulation |
| `3731160.pdf` | 6199398 | Generating Past and Future in Digital Painting Processes |
| `3731192.pdf` | 12884380 | Fluid Simulation on Compressible Flow Maps |
| `3731212.pdf` | 144626170 | Faraday Cage Estimation of Normals for Point Clouds and Ribbon Sketches |
| `3731216.pdf` | 220756540 | Feature-Aligned Parametrization in Penner Coordinates |

## 恢复建议

1. 不要先清空 `~/Downloads/acm_sig_auto/`。
2. 先按 DOI 后缀把上述 23 个 PDF 校验并移动到队列中的 `target_pdf_path`。
3. 再继续运行浏览器下载流程。
4. 继续时建议保持 `batch_size=25`，因为前两批 `50/50` 均标题校验通过且无 timeout。

## 相关产物

- 下载流程文档：`_private/acm_browser_download_workflow_20260630.md`
- 当前队列下载器：`_private/acm_queue_browser_downloader.py`
- 成功小批量报告：`_private/acm_download_recovery/reports/acm_queue_browser_download_20260630T114535Z.json`
- 历史下载目录残留已移动到：`_private/acm_download_recovery/reports/preexisting_acm_sig_auto_20260630/`
