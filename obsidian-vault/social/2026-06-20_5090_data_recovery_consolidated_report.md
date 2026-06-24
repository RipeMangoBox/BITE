---

## title: "5090 数据恢复与挂载切换合并报告"
type: incident-recovery-report
server: "5090"
tags:
  - operations/data-recovery
  - status/completed
aliases:
  - 5090 Data Recovery Report
created: 2026-06-20T15:38+08:00
updated: 2026-06-20T15:38+08:00

# 5090 数据恢复与挂载切换合并报告

> [!abstract] 结论
> 多轮 rsync 已结束，最终非排除范围遍历到 `to-chk=0/4941167`，但以 code 23 结束，不能视为无损完整备份。日志合并得到 2,966 个唯一报错路径，其中 2,956 个仍需用户核验或重建，10 个在同轮重试后恢复。2026-06-20 15:32 已完成挂载切换：新盘为 `/data`，坏盘为 `/data_broken`。

完整逐路径清单见 [[social/2026-06-20_5090_data_damage_manifest|5090 数据恢复受损与未完成路径清单]]；可发送通知见 [[social/2026-06-20_5090_data_damage_user_notice|5090 数据受损用户通知]]。

## 当前挂载状态


| 路径             | 设备          | UUID                                   | 状态                 |
| -------------- | ----------- | -------------------------------------- | ------------------ |
| `/data`        | `/dev/sdh1` | `c771d501-6cf9-4176-bd5c-0e91d2f957ca` | 新盘，读写挂载，写入测试通过     |
| `/data_broken` | `/dev/sda`  | `c3a6fb55-ef69-4b2f-8748-0081b74e37fd` | 原坏盘，保留用于必要的只读式人工取证 |
| `/data_new`    | 无           | 无                                      | 已卸载，仅保留普通目录        |


- fstab 已同步更新，`findmnt --verify` 为 0 个解析错误、0 个错误。
- 唯一警告是既有 `/swapfile` 条目，不属于本次数据盘切换。
- Docker、Docker socket 与 containerd 已恢复为 active。
- fstab 切换前备份：`/etc/fstab.before_data_swap_direct_20260620_153103`。
- 直接卸载时终止了所有仍占用旧 `/data` 的 shell、Agent 与 Docker 进程；用户任务需自行重新启动。

## 合并日志结论

### 证据分层


| 证据                                        | 唯一路径数 | 解释                                      |
| ----------------------------------------- | ----- | --------------------------------------- |
| `failed verification -- update discarded` | 790   | 文件内容读取失败，rsync 未采用坏盘版本更新新盘；目标可能缺失或保留旧版本 |
| 报错且位于最终排除范围                               | 2,150 | 后续轮次主动跳过，目录或文件完整性未验证                    |
| 最终一轮仍报错                                   | 16    | 15 个路径/元数据读取失败，1 个目录枚举失败                |
| 历史读错但同轮重试恢复                               | 10    | 未出现 `update discarded`，从待处理主清单中排除       |
| 唯一报错路径总数                                  | 2,966 | 上述四类合计                                  |


待处理路径按用户统计：`zz` 2,955 个，`ripemangobox` 1 个。目录枚举失败可能隐藏未进入日志的子项，因此 2,956 不是理论上限。

### 原始错误消息统计

- `Input/output error (5)`：3,949 次。
- `Bad message (74)`：93 次。
- 合计错误消息：4,042 次。
- 其中 `read errors mapping`：1,590 次，去重后涉及 800 个文件；790 个最终丢弃更新，10 个重试恢复。
- `readlink_stat`：2,473 次，去重后涉及 2,165 个路径。
- `readdir`：13 次，去重后涉及 1 个目录。

### 多轮拷贝日志

下表的字节数和 `xfr` 是每个日志的最后可见进度，不可相加：各轮会重复扫描、补拷或保留既有目标文件。


| 日志                                              | 最后可见传输量             | `xfr`     | I/O   | Bad | 结果                             |
| ----------------------------------------------- | ------------------- | --------- | ----- | --- | ------------------------------ |
| `rsync_sdg_to_sdh_20260619_174524.log`          | 1,587,161,950,813 B | 3,332,854 | 0     | 0   | `to-chk=0/3356531`；早期完整遍历日志    |
| `rsync_sda_to_sdh_repair_20260619_234732.log`   | 765,045,290,810 B   | 1,703,495 | 3,197 | 69  | 运行约 13 小时 21 分；在密集坏块区停止        |
| `rsync_sda_to_sdh_fastpass_20260620_131257.log` | 0 B                 | 0         | 54    | 2   | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_132510.log` | 41,976,345,002 B    | 84,833    | 75    | 16  | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_134207.log` | 0 B                 | 0         | 44    | 0   | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_134828.log` | 0 B                 | 0         | 30    | 0   | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_135332.log` | 2,714,072,458 B     | 65,716    | 121   | 0   | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_141222.log` | 16,642,845 B        | 1,143     | 81    | 0   | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_142245.log` | 1,421,636,843 B     | 17,445    | 67    | 6   | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_143108.log` | 1,196,906,714 B     | 31,720    | 98    | 0   | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_144717.log` | 1,332,397,612 B     | 25,193    | 89    | 0   | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_145957.log` | 970,940,681 B       | 12,203    | 65    | 0   | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_150827.log` | 0 B                 | 0         | 12    | 0   | 发现集中错误后扩展 exclude              |
| `rsync_sda_to_sdh_fastpass_20260620_151147.log` | 15,502,836,541 B    | 590       | 16    | 0   | `to-chk=0/4941167`，code 23；最终轮 |


repair 轮产生 3,197 次 I/O 与 69 次 Bad message；12 个 fastpass 合计产生 752 次 I/O 与 24 次 Bad message。

## 最终有效排除内容

最终 exclude 文件包含 15 条有效规则：系统 1 条、`ripemangobox` 4 条、`zz` 10 条。规则按源根目录记录；对应当前新盘路径时在前面加 `/data`，对应坏盘时加 `/data_broken`。

1. `/lost+found`
2. `/public/ripemangobox/Motion/datasets/pulpmotion-data/cam_segments/`
3. `/public/ripemangobox/Motion/datasets/pulpmotion-data/caption_cam/`
4. `/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v3_closure_20260616/full/gpu1_humjoint_besteval_joint_std_cfg2_eta1.records.jsonl`
5. `/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v3_closure_20260616/full/gpu3_jointheavy_h2_besteval_joint_std_cfg2_eta1.records.jsonl`
6. `/public/zz/research/AFSE_EMNLP2026/external/gepa/.venv/`
7. `/public/zz/baseline/`
8. `/public/zz/research/AFSE_v2/root_cache_moved/miniforge3/`
9. `/public/zz/research/AFSE_v2/runs/`
10. `/public/zz/research/AFSE_v3/.envs/`
11. `/public/zz/research/AFSE_v3/docs/runs/`
12. `/public/zz/research/AFSE_v3/external/`
13. `/public/zz/research/AFSE_v3/runs/`
14. `/public/zz/dataset/skillflow-task/.git/lfs/`
15. `/public/zz/paper/SkillFlow:Benchmarking Lifelong Skill Discovery and Evolution for Autonomous Agents/`

全部历史 deferred 文件共出现 18 条字面规则。以下 3 条已被更宽的最终规则覆盖，不再单独计入 15 条有效规则：

- `/public/zz/research/AFSE_v2/root_cache_moved/miniforge3/envs/SGLang/`
- `/public/zz/research/AFSE_v2/root_cache_moved/miniforge3/envs/`
- `/public/zz/research/AFSE_v2/runs/202605232027_hotpotqa_afse_b8_standard_full_50_100_100/`

> [!warning] 排除规则的含义
> 排除不等于整个目录都已证明损坏，也不等于目录完全未复制。它表示后续补拷不再遍历该范围，因此新盘中的版本可能部分存在、过期或缺失，必须由用户从可再生成实验、上游仓库、外部数据源或其他备份恢复。

## 用户影响摘要

### ripemangobox

- 最终轮对 `/data/public/ripemangobox/Motion/datasets/pulpmotion-data/smpl_rifke` 执行目录枚举失败，目录子项可能不完整。
- 另有 2 个数据目录与 2 个评估 JSONL 被主动排除，未验证完整性。

### zz

- 待处理路径 2,955 个：`baseline` 1,441、`dataset` 786、`research` 711、`home-migrated` 11、`paper` 3、`.cache` 3。
- 790 个明确丢弃更新的文件主要集中在 `dataset/skillflow-code` 776 个、`home-migrated/miniconda3` 11 个、`.cache/home-cache` 3 个。
- 2,150 个报错路径落在最终排除范围：`baseline` 1,441、`research` 698、`dataset` 8、`paper` 3。
- 最终轮还有 15 个未排除路径报错：`research/AFSE_v3` 11、`research/AFSE_EMNLP2026` 2、`dataset/huggingface` 2。

## 完整性边界与处理原则

1. `to-chk=0` 只证明最终轮完成了非排除范围的 rsync 遍历，不是逐字节校验。
2. code 23 明确表示仍有文件或属性未传输。
3. 新盘可能保留早期轮次的旧版本；尤其是 `update discarded` 文件，不能默认其内容为故障发生前最新版本。
4. 对实验运行目录，优先重跑或从实验平台导出；对 Git 仓库、环境、缓存和 LFS，优先重新 clone、重新安装或重新 pull。
5. 旧盘 `/data_broken` 应避免常规写入；仅在确有不可再生文件时做定向读取，避免继续扩大介质错误。

## 原始证据位置

- 全部 rsync 日志：`/data/rescue_logs/rsync_*.log`
- 全部 deferred 演进文件：`/data/rescue_logs/fastpass_deferred_*.txt`
- 最终日志：`/data/rescue_logs/rsync_sda_to_sdh_fastpass_20260620_151147.log`
- 最终 exclude：`/data/rescue_logs/fastpass_deferred_20260620_151147.txt`
- 挂载切换日志：`/tmp/data_swap_direct_v2.log`

