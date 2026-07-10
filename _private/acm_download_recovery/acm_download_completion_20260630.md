# ACM PDF 下载完成记录 2026-06-30

## 队列

- 队列文件：`obsidian-vault/batches/wait_pdf_unified_queue_20260630/edge_acm_download_queue_20260630.csv`
- 总条目：910
- 目标 PDF 已有效存在：872
- 已记录 skip：38
- 未完成且未 skip：0
- 下载目录残留：0

## 本轮浏览器下载

- 使用方式：当前 Microsoft Edge `Profile 1`，自动打开 ACM PDF URL，下载到 `~/Downloads/acm_sig_auto` 后校验并移动到目标目录。
- 本轮命令：`python3 _private/acm_queue_browser_downloader.py --batch-size 10 --delay 3 --wait 600`
- 本轮报告：`_private/acm_download_recovery/reports/acm_queue_browser_download_20260630T165119Z.json`
- 本轮结果：新增成功 169，失败 2，剩余 0。

## 失败项

本轮新增失败均为 ACM 返回文件可下载但 PyMuPDF 判定 `zero_pages`：

- `3763366` — Curvature Enthusiasm: Correspondence-Free Interpolation and Matching of Articulated 3D Shapes using Compressed Normal Cycles
- `3763321` — Gaussian Integral Linear Operators for Precomputed Graphics

完整跳过清单见：

- `_private/acm_download_recovery/reports/acm_queue_skip_suffixes_20260630.txt`

## 清理状态

- 已归档此前下载目录残留：`_private/acm_download_recovery/reports/stale_skipped_download_dir_20260630/`
- 当前 `~/Downloads/acm_sig_auto` 无残留 PDF 或 `.crdownload` 文件。
- 未发现仍在运行的 `acm_queue_browser_downloader` 自动下载进程。
