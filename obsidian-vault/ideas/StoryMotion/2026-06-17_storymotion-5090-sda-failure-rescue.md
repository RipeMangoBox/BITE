---
hypothesis: "2026-06-17 StoryMotion 5090 full-eval 中断不是评测脚本问题，而是 5090 /data 所在 sda 机械盘出现介质级读错误与 ext4 inode table 读失败；已停止实验并把已完成 JSON 与 partial records 迁移到 SSD 与本地 rescue 目录。"
status: in_progress
source_papers:
  - "[[2026-06-16_storymotion-v3-formal]]"
created: 2026-06-17T16:40:00+08:00
updated: 2026-06-17T16:40:00+08:00
---

# StoryMotion 5090 sda 故障与 Rescue 记录

> [!warning] 当前状态
> 5090 的 `/data` 所在 `/dev/sda` 已出现介质级读错误。不要在 `/data` 上继续启动 StoryMotion 训练、评测、TensorBoard 或大规模复制。恢复实验前，应先完成坏盘隔离、关键数据备份与新存储迁移。

## 1. 触发背景

2026-06-17 下午，StoryMotion V3 追加 full metric 评测时，多个进程表现为 GPU 显存占用但功率和利用率上不去。进程不是 zombie，而是卡在 Linux `D` state / disk sleep。

当时运行中的主要任务：

| session / task | 进程状态 | 输出 |
| --- | --- | --- |
| Stage1 mixed full upper-bound | 已停止，未完成 | `stage1_mixed_full.records.jsonl` partial |
| human text `shuffle_camera` full metric | 已完成 | `human_text_shuffle_camera_full.json` |
| human camera latent `shuffle` full metric | 已完成 | `human_camera_latent_shuffle_full.json` |
| human text `zero_human` full metric | 已停止，未完成 | `human_text_zero_human_full.records.jsonl` partial |
| human camera latent `noise_matched` full metric | 已停止，未完成 | `human_camera_latent_noise_matched_full.records.jsonl` partial |

## 2. 故障证据

用户以 root / su 权限读取内核日志后确认 `/dev/sda` 介质错误。关键日志类型包括：

```text
critical medium error, dev sda
Sense Key : Medium Error [current]
Add. Sense: Unrecovered read error
error: { UNC }
EXT4-fs error (device sda): ext4_get_inode_loc: unable to read itable block
EXT4-fs error (device sda) in ext4_reserve_inode_write: IO failure
EXT4-fs error (device sda): ext4_dirty_inode: mark_inode_dirty error
```

root 侧 stack 也显示 Python 在读文件时进入 ext4 inode / buffer 等待路径：

```text
__wait_on_buffer
__ext4_get_inode_loc
ext4_reserve_inode_write
__ext4_mark_inode_dirty
filemap_read
ext4_file_read_iter
vfs_read
```

这说明问题不是 StoryMotion sampler、metric callback 或 CUDA kernel 死锁，而是 `/data` 文件系统底层盘面读失败导致 ext4 无法读取 inode table block，并进一步阻塞 Python 读样本 / 写 records。

## 3. 已执行止损动作

已执行以下操作：

1. 停止 StoryMotion 相关 tmux session：
   - `sm_human_camlatent_ablate_20260617`
   - `sm_human_text_ablate_20260617`
   - `sm_stage1_mixed_full_20260617_retry`
   - `stage2_tensorboard_6006`
2. 对残留 eval / TensorBoard 进程发出停止或终止信号。
3. 确认当前无 StoryMotion eval / TensorBoard 进程。
4. 确认 GPU compute apps 已清空，4 张 GPU 显存回到空闲量级。
5. 将已完成 JSON、logs、records 与 partial records 从 5090 `/data` 尽量复制到 5090 SSD `/home`。
6. 将同一 rescue 目录从 5090 拉回本地 `linkedCodebases/StoryMotion/rescue/`。

## 4. Rescue 路径

5090 SSD 备份：

- `/home/ripemangobox/storymotion_sda_rescue_20260617_163351/`

本地备份：

- `linkedCodebases/StoryMotion/rescue/storymotion_sda_rescue_20260617_163351/`

rescue 目录规模：

| 位置 | 文件数 | 大小 |
| --- | ---: | ---: |
| 5090 `/home` rescue | 29 | 46M |
| 本地 `linkedCodebases` rescue | 29 | 46M |

## 5. 已保留结果

已完成且可作为正式 evidence 的 JSON：

- `linkedCodebases/StoryMotion/rescue/storymotion_sda_rescue_20260617_163351/runs/eval/stage1/official_upper_bound_20260617/stage1_pure_full.json`
- `linkedCodebases/StoryMotion/rescue/storymotion_sda_rescue_20260617_163351/runs/eval/stage2/human_completion_dependency_20260617/human_text_zero_camera_full.json`
- `linkedCodebases/StoryMotion/rescue/storymotion_sda_rescue_20260617_163351/runs/eval/stage2/human_completion_dependency_20260617/human_text_shuffle_camera_full.json`
- `linkedCodebases/StoryMotion/rescue/storymotion_sda_rescue_20260617_163351/runs/eval/stage2/human_completion_dependency_20260617/human_camera_latent_zero_full.json`
- `linkedCodebases/StoryMotion/rescue/storymotion_sda_rescue_20260617_163351/runs/eval/stage2/human_completion_dependency_20260617/human_camera_latent_shuffle_full.json`

已保留但不能当 full metric 结论的 partial records：

- `linkedCodebases/StoryMotion/rescue/storymotion_sda_rescue_20260617_163351/runs/eval/stage1/official_upper_bound_20260617/stage1_mixed_full.records.jsonl`
- `linkedCodebases/StoryMotion/rescue/storymotion_sda_rescue_20260617_163351/runs/eval/stage2/human_completion_dependency_20260617/human_text_zero_human_full.records.jsonl`
- `linkedCodebases/StoryMotion/rescue/storymotion_sda_rescue_20260617_163351/runs/eval/stage2/human_completion_dependency_20260617/human_camera_latent_noise_matched_full.records.jsonl`

这些 partial records 只用于排障和恢复记录。由于当前 eval 脚本启动时会删除同名 records，不能把 partial records 直接当断点续跑结果。

## 6. 对 V3 结论的影响

保留不变的 V3 结论：

1. `stage1_pure_full.json` 已完成，仍可支持 pure Stage1 reconstruction upper-bound 结论。
2. `human_text_zero_camera_full.json` 与 `human_text_shuffle_camera_full.json` 已完成，支持 camera-text half 对当前 human completion 影响很弱。
3. `human_camera_latent_zero_full.json` 与 `human_camera_latent_shuffle_full.json` 已完成，支持 observed camera latent block 对 human completion 是强条件。

需要撤回为 pending 的内容：

1. Stage1 mixed full 没有 full JSON，不能写 completed conclusion。
2. human text `zero_human` / `shuffle_human` / `zero_all` 没有 full JSON，不能写 completed conclusion。
3. camera latent `noise_matched` 没有 full JSON，不能写 completed conclusion。

## 7. 恢复前置条件

恢复实验前建议完成：

1. 停止所有对 `/data` 的写入任务。
2. 尽量将 `/data` remount 为只读：

```bash
mount -o remount,ro /data
```

3. 如果 remount 失败，先查占用：

```bash
lsof +f -- /data
fuser -vm /data
```

4. 备份关键路径到非 `/data` 介质。
5. 更换或隔离 `/dev/sda`，至少离线执行 SMART 与文件系统检查。
6. 后续 StoryMotion full eval 不应直接从坏盘 `/data` 读写；应迁移 cache、checkpoint、repo 与输出到 SSD 或新盘。

## 8. 后续实验建议

重启实验时优先级如下：

1. 先在健康存储上重新建立 StoryMotion repo、PulpMotion linked tree、cache 与 checkpoints。
2. 先复核已完成 JSON 的 SHA / 样本数，确认 rescue 与本地 evidence 一致。
3. 再重跑 Stage1 mixed full，避免与其他 full eval 并发。
4. 最后重跑 human text `zero_human` / `shuffle_human` / `zero_all` 与 camera latent `noise_matched`。
5. 每次只跑 1 到 2 个 full eval，降低随机小文件读和 records 写对机械盘 / 文件系统的压力。

