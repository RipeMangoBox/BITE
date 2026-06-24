# sync_index — manifest 索引与同步校验

## 文件

| 文件 | 职责 |
|------|------|
| `build_manifest_index.py` | 扫描 artifact 目录，构建统一的 manifest index (TSV + JSONL)，连接 forward/delta manifest 与 sample case 元信息 |
| `sync_sanity_check.py` | 远端/本都同步完整性检查（NPZ 存在性、manifest row 数量一致性） |

## 输出

- `index_outputs/manifest_index.tsv`: 所有 forward/delta NPZ 行的统一索引
- `index_outputs/sample_case_index.tsv`: 以 sample_id + outcome 为 key 的 P3 证据链索引
