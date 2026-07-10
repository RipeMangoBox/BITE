# ACM PDF 浏览器下载流程（2026-06-30 验证）

## 结论

可行方法不是 `curl` 加 cookies，而是复用当前 Edge 的已通过 Cloudflare/机构访问会话：

1. 使用 Edge `Profile 1`。
2. 保持 Edge 设置 `Always download PDF files`。
3. 通过命令行向当前 Edge 追加 `dl.acm.org/doi/pdf/<doi>` 新标签。
4. 从 `~/Downloads/acm_sig_auto/` 监控并导入下载完成的 PDF。

本次复现样本：

- URL: `https://dl.acm.org/doi/pdf/10.1145/3731189`
- 标题: `4D Gaussian Videos with Motion Layering`
- 下载结果: `~/Downloads/acm_sig_auto/3731189.pdf`
- 校验: 文件头 `%PDF-1.7`，14 页，首页文本包含目标标题
- 已移动到: `obsidian-vault/paperPDFs/SIGGRAPH_2025/4D_Gaussian_Videos_with_Motion_Layering.pdf`

## 成功案例来源

检索 `~/.codex/sessions/2026/06/27` 及之后会话，成功案例在：

`/home/ripemangobox/.codex/sessions/2026/06/29/rollout-2026-06-29T13-25-18-019f11d6-d066-7a01-9b54-f41a0a3253ec.jsonl`

关键证据：

- 会话中新增脚本: `scripts/local_maintenance/download_acm_siggraph_from_paper_list.py`
- 成功方式: 普通 Edge 浏览器批量打开 ACM PDF URL，Edge 设置为始终下载 PDF
- 下载目录: `~/Downloads/acm_sig_auto`
- 历史结果: SIG/SIGA/TOG 的 ACM DOI 项回填 `Downloaded=430`，剩余 4 个为解析/匹配问题

## 当前 Edge 配置

已确认当前配置在：

`~/.config/microsoft-edge/Profile 1/Preferences`

关键字段：

```json
{
  "download": {
    "default_directory": "/home/ripemangobox/Downloads/acm_sig_auto"
  },
  "plugins": {
    "always_open_pdf_externally": true
  }
}
```

如果下载没有发生，先在当前 Edge UI 检查：

- `edge://settings/content/pdfDocuments`
- 开启 `Always download PDF files`
- 下载目录设为 `/home/ripemangobox/Downloads/acm_sig_auto`

## 单条验证

使用当前 Edge 的 `Profile 1`，不要启动 Playwright 临时浏览器：

```bash
mkdir -p ~/Downloads/acm_sig_auto
microsoft-edge --profile-directory='Profile 1' --new-tab 'https://dl.acm.org/doi/pdf/10.1145/3731189'
```

等待 `~/Downloads/acm_sig_auto/` 出现 `.crdownload`，完成后变为 `.pdf`：

```bash
find ~/Downloads/acm_sig_auto -maxdepth 1 -type f -printf '%TY-%Tm-%Td %TH:%TM %f\t%s bytes\n' | sort | tail
```

快速校验 PDF：

```bash
python3 - <<'PY'
from pathlib import Path
import fitz
p = Path.home() / 'Downloads/acm_sig_auto/3731189.pdf'
print(p, p.exists(), p.stat().st_size if p.exists() else 0)
print(p.read_bytes()[:8])
with fitz.open(p) as doc:
    print('pages', doc.page_count)
    print(doc.load_page(0).get_text('text')[:300])
PY
```

## 从统一队列批量打开

当前统一 ACM 队列：

`obsidian-vault/batches/wait_pdf_unified_queue_20260630/edge_acm_download_queue_20260630.csv`

先生成小批量 URL 文件，例如 10 条：

```bash
python3 - <<'PY'
import csv
from pathlib import Path
q = Path('obsidian-vault/batches/wait_pdf_unified_queue_20260630/edge_acm_download_queue_20260630.csv')
out = Path('_private/acm_download_recovery/queue/current_batch_urls.txt')
out.parent.mkdir(parents=True, exist_ok=True)
urls = []
for r in csv.DictReader(q.open(encoding='utf-8')):
    url = r.get('resolved_pdf_url') or r.get('pdf_url') or r.get('url') or ''
    if 'dl.acm.org/doi/pdf/' in url:
        urls.append(url)
    if len(urls) >= 10:
        break
out.write_text('\n'.join(urls) + '\n', encoding='utf-8')
print(out, len(urls))
PY
```

按 3 到 5 秒间隔打开，避免 Cloudflare 或 Edge 下载队列压力过大：

```bash
while IFS= read -r url; do
  [ -n "$url" ] || continue
  microsoft-edge --profile-directory='Profile 1' --new-tab "$url"
  sleep 4
done < _private/acm_download_recovery/queue/current_batch_urls.txt
```

监控下载完成：

```bash
watch -n 2 "find ~/Downloads/acm_sig_auto -maxdepth 1 -type f \\( -name '*.pdf' -o -name '*.crdownload' \\) -printf '%f\t%s bytes\n' | sort"
```

## 导入原则

现有脚本 `scripts/local_maintenance/download_acm_siggraph_from_paper_list.py` 的 `browser-batch` / `import-folder` 针对 `paper_list.csv` 设计，成功导入会修改 `paper_list.csv`。如果只想验证，不回填列表，必须加：

```bash
--import-dry-run
```

当前 `wait_pdf_unified_queue_20260630` 是独立队列；导入时应按队列中的 `target_pdf_path` 移动文件，并用 PyMuPDF 校验：

- 文件头必须是 `%PDF`
- `fitz.open()` 能打开且页数大于 0
- 首页或前两页文本应匹配队列标题
- 不匹配的 PDF 放到 `_private/acm_download_recovery/reports/unmatched_pdfs/`，不要直接写入 `paperPDFs`

## 注意事项

- 不要依赖 `_private/acm_download_recovery/secrets/dl.acm.org_cookies.txt` 做 `curl` 下载；本轮测试中 cookies 方式仍返回 Cloudflare 403。
- 不要新建 Playwright 临时 profile；Cloudflare 会重新验证，质量不稳定。
- 使用 `microsoft-edge --profile-directory='Profile 1' --new-tab URL` 会复用当前 Edge 会话。
- 批量建议先用 10 条验证，再扩到 25 或 50；若出现验证码、下载失败或标题错配，立即降回 10。
- 下载期间不要让自动化抢鼠标；该流程只追加浏览器标签并监控文件系统。
