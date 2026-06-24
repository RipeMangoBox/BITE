# 5090 `/data` 到本机 TOSHIBA 3.6T 盘 Rescue 指令

目标：把 5090 坏盘 `/data` 中实际文件级数据复制到新加的 TOSHIBA 3.6T 移动数据盘中，**不再通过网络传输到 4090**。

这块 TOSHIBA 是临时移动救援盘，不会长期挂在 5090 上。不要把它写入 `/etc/fstab`，不要把后续 StoryMotion 训练 / 评测长期路径直接指向这块盘；它的用途是先把坏盘上仍可读的数据带走，再导入到长期稳定存储。

## 0. 当前磁盘识别

5090 当前磁盘：

| 设备 | 大小 | 用途 / 状态 |
| --- | ---: | --- |
| `/dev/sda` | 7.3T | 旧 `/data`，Seagate `ST8000NM0055-1RM112`，已出现介质级读错误 |
| `/dev/sdb2` | 1.7T | 系统盘 `/` |
| `/dev/sdg` | 3.6T | 新 TOSHIBA 移动盘 `MQ04UBB400`，序列号 `Y45DT0CKT` |
| `/dev/sdg2` | 3.6T | 当前为 NTFS，label `EXTERNAL_USB`，未挂载 |

建议使用稳定路径识别新盘，避免设备名变化：

```bash
/dev/disk/by-id/ata-TOSHIBA_MQ04UBB400_Y45DT0CKT
/dev/disk/by-id/ata-TOSHIBA_MQ04UBB400_Y45DT0CKT-part2
```

坏盘已确认有：

```text
critical medium error, dev sda
Unrecovered read error
error: { UNC }
EXT4-fs error: unable to read itable block
```

因此不要再在 `/data` 上启动训练、评测、TensorBoard 或大规模写入。

## 1. 推荐方案：将 TOSHIBA 移动盘格式化为 ext4

如果 TOSHIBA 移动盘里没有需要保留的数据，推荐格式化为 ext4。这样最适合保存 Linux ownership、permissions、xattrs、symlink、hardlink 等元数据。后续要导回 Linux 服务器时，ext4 比 NTFS 更可靠。

不要为了临时挂载把它加入 `/etc/fstab`。每次使用时手动挂载，复制完成后手动卸载。

> [!warning]
> 下面的 `mkfs.ext4` 会清空 TOSHIBA 分区 `/dev/sdg2` 的现有内容。只会操作 TOSHIBA 新盘，不要对 `/dev/sda` 执行格式化。

以 root 登录 5090：

```bash
su -
```

再次确认设备：

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL,MOUNTPOINTS,MODEL,SERIAL
readlink -f /dev/disk/by-id/ata-TOSHIBA_MQ04UBB400_Y45DT0CKT-part2
```

确认输出指向 `/dev/sdg2` 后，格式化：

```bash
mkfs.ext4 -F -L rescue5090 /dev/disk/by-id/ata-TOSHIBA_MQ04UBB400_Y45DT0CKT-part2
```

创建挂载点并挂载：

```bash
mkdir -p /mnt/rescue5090
mount /dev/disk/by-id/ata-TOSHIBA_MQ04UBB400_Y45DT0CKT-part2 /mnt/rescue5090
df -h /mnt/rescue5090
```

确认它是临时挂载，而不是 fstab 自动挂载：

```bash
findmnt /mnt/rescue5090
grep -n 'rescue5090\|Y45DT0CKT\|TOSHIBA' /etc/fstab || true
```

创建目标目录：

```bash
mkdir -p /mnt/rescue5090/5090-data-rescue-20260617/data-root
```

## 2. 尽量停止旧盘写入

确认没有 StoryMotion 任务：

```bash
tmux ls 2>/dev/null || true
pgrep -af 'storymotion|tensorboard|eval_stage1|storymotion_official_full_eval' || true
nvidia-smi
```

尝试将旧 `/data` 只读挂载，减少进一步损坏：

```bash
mount -o remount,ro /data
```

如果失败，查占用：

```bash
lsof +f -- /data | head -100
fuser -vm /data
```

如果只读 remount 失败，也可以继续复制，但不要再启动会写 `/data` 的任务。

## 3. 开始文件级 Rescue

建议在 root tmux 中运行，方便断线后继续观察：

```bash
tmux new -s rescue_sda_to_toshiba
```

在 tmux 中执行：

```bash
mkdir -p /mnt/rescue5090/5090-data-rescue-20260617/logs

cd /data

rsync -aHAXS --numeric-ids --ignore-errors --partial --append-verify --info=progress2 \
  --exclude='/lost+found' \
  ./ /mnt/rescue5090/5090-data-rescue-20260617/data-root/ \
  2>&1 | tee /mnt/rescue5090/5090-data-rescue-20260617/logs/rsync_$(date +%Y%m%d_%H%M%S).log
```

说明：

- `-aHAXS`：尽量保留权限、owner、hardlink、ACL、xattr、稀疏文件。
- `--numeric-ids`：保留 UID/GID 数字，不依赖用户名映射。
- `--ignore-errors`：遇到坏盘读失败时继续复制。
- `--partial --append-verify`：中断后可续传。
- `--info=progress2`：显示总体进度、速度和 ETA。
- `--exclude='/lost+found'`：跳过 ext4 系统恢复目录。

临时离开 tmux：按 `Ctrl-b`，再按 `d`。

重新查看进度：

```bash
tmux attach -t rescue_sda_to_toshiba
```

## 4. 单独查看复制进度

另开一个 shell 查看目标大小：

```bash
watch -n 60 'du -sh /mnt/rescue5090/5090-data-rescue-20260617/data-root 2>/dev/null; df -h /mnt/rescue5090'
```

查看 rsync 是否仍在运行：

```bash
pgrep -af rsync
```

查看坏盘是否继续报错：

```bash
dmesg -T | tail -n 80
```

## 5. 预计耗时

按约 2.5T 传输量估算：

| 实际速度 | 预计耗时 |
| ---: | ---: |
| 50 MB/s | 约 14 小时 |
| 100 MB/s | 约 7 小时 |
| 150 MB/s | 约 4.6 小时 |
| 200 MB/s | 约 3.5 小时 |

坏盘读到坏块时会卡顿，实际耗时可能更长。

## 6. 卡住坏块时：快速跳过坏区，先复制健康文件

如果总复制量长期停在同一数值，例如 `/mnt/rescue5090` 已用量数小时不增长，且日志出现大量：

```text
Input/output error (5)
read errors mapping
readlink_stat(...) failed
failed verification -- update retained
```

不要原样重复第 3 节命令。原命令会继续撞同一批坏 inode / 坏文件，速度可能越来越慢。

`rsync` 不能在硬盘坏块上“立刻超时跳过”，它必须等待内核读请求返回错误；如果进程处于 `D` 状态，说明还在等待坏盘 I/O，不能被普通信号立即杀掉。正确策略是：软停止当前 rsync，然后新开 fast pass，显式排除已知坏区，先把其余健康文件复制完。

### 6.1 停止当前卡住的 rsync

在任意 shell 执行：

```bash
tmux send-keys -t rescue_sda_to_toshiba C-c
```

等待 1-5 分钟，确认 rsync 是否退出：

```bash
ps -eo pid,ppid,state,stat,wchan:40,etime,cmd | grep -E '[r]sync|[t]ee .*/rsync_'
```

如果仍看到 `D` / `D+` 状态，表示它还卡在内核坏盘读请求里。此时继续等，不要重启，不要拔盘。

### 6.2 建立 fast pass 排除列表

当前已知坏区主要集中在 StoryMotion eval 记录和 PulpMotion 数据集局部目录。先排除它们，避免健康数据被坏区拖住：

```bash
RESCUE=/mnt/rescue5090/5090-data-rescue-20260617
mkdir -p "$RESCUE/logs"

cat > "$RESCUE/logs/fastpass_exclude_20260619.txt" <<'EOF'
/lost+found
/public/ripemangobox/Motion/datasets/pulpmotion-data/cam_segments/
/public/ripemangobox/Motion/datasets/pulpmotion-data/caption_cam/
/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v3_closure_20260616/full/gpu1_humjoint_besteval_joint_std_cfg2_eta1.records.jsonl
/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v3_closure_20260616/full/gpu3_jointheavy_h2_besteval_joint_std_cfg2_eta1.records.jsonl
EOF
```

如果后续日志继续出现新的 `Input/output error` 路径，把对应文件或目录追加到这个 exclude 文件中，再重跑 fast pass。

### 6.3 新开 fast pass，复制剩余健康文件

新开 tmux：

```bash
tmux new -s rescue_fastpass_healthy
```

在 tmux 里执行：

```bash
RESCUE=/mnt/rescue5090/5090-data-rescue-20260617
cd /data || exit 1

ionice -c2 -n7 nice -n 10 rsync -aAXS --numeric-ids \
  --ignore-errors --partial --ignore-existing --info=progress2 \
  --exclude-from="$RESCUE/logs/fastpass_exclude_20260619.txt" \
  ./ "$RESCUE/data-root/" \
  2>&1 | tee "$RESCUE/logs/rsync_fastpass_$(date +%Y%m%d_%H%M%S).log"
```

说明：

- `--ignore-existing`：跳过目标盘已有文件，优先抢救尚未复制的健康文件。
- `--partial`：保留中断文件，后续可继续处理。
- 这里故意不使用 `--append-verify`，避免在 fast pass 阶段反复校验已经卡坏的 partial 文件。
- 这一步的目标是先扩大健康数据覆盖率，不是修复坏文件。

查看进度：

```bash
tmux capture-pane -pt rescue_fastpass_healthy -S -40
df -h /mnt/rescue5090
tail -f "$RESCUE"/logs/rsync_fastpass_*.log
```

### 6.4 fast pass 后再单独处理坏区

fast pass 完成后，再从日志汇总坏文件：

```bash
grep -aEi 'Input/output error|read errors mapping|readlink_stat|failed verification|rsync error' \
  /mnt/rescue5090/5090-data-rescue-20260617/logs/rsync*.log \
  /mnt/rescue5090/5090-data-rescue-20260617/logs/rsync_fastpass_*.log \
  | tee /mnt/rescue5090/5090-data-rescue-20260617/logs/error_files_summary_20260619.txt
```

确认健康文件已经尽量复制完后，再决定是否对坏目录做单独 rescue。坏目录单独处理时建议小范围逐个目录复制，不要再全盘扫。

## 7. 中断后续传

如果传输中断，重新挂载目标盘后重复第 3 节同一条 `rsync` 命令即可。`rsync` 会跳过已完成文件并继续 partial 文件。

如果是因为坏块卡住而主动中断，优先使用第 6 节 fast pass，不要直接原样续传。

确认挂载：

```bash
mount | grep rescue5090 || mount /dev/disk/by-id/ata-TOSHIBA_MQ04UBB400_Y45DT0CKT-part2 /mnt/rescue5090
```

然后重新运行：

```bash
cd /data

rsync -aHAXS --numeric-ids --ignore-errors --partial --append-verify --info=progress2 \
  --exclude='/lost+found' \
  ./ /mnt/rescue5090/5090-data-rescue-20260617/data-root/ \
  2>&1 | tee -a /mnt/rescue5090/5090-data-rescue-20260617/logs/rsync_resume_$(date +%Y%m%d_%H%M%S).log
```

## 8. 完成后校验与安全拔盘

查看总大小：

```bash
du -sh /mnt/rescue5090/5090-data-rescue-20260617/data-root
df -h /mnt/rescue5090
```

统计文件数：

```bash
find /mnt/rescue5090/5090-data-rescue-20260617/data-root -xdev -type f | wc -l
find /mnt/rescue5090/5090-data-rescue-20260617/data-root -xdev -type d | wc -l
```

检查日志中的坏文件：

```bash
grep -Ei 'Input/output error|failed|error' /mnt/rescue5090/5090-data-rescue-20260617/logs/rsync_*.log | tee /mnt/rescue5090/5090-data-rescue-20260617/logs/error_files_summary.txt
```

保存一份 manifest：

```bash
{
  date -Is
  lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL,UUID,MOUNTPOINTS,MODEL,SERIAL
  df -h /data /mnt/rescue5090
  du -sh /mnt/rescue5090/5090-data-rescue-20260617/data-root
} | tee /mnt/rescue5090/5090-data-rescue-20260617/rescue_manifest.txt
```

卸载前同步：

```bash
sync
umount /mnt/rescue5090
```

移动盘建议做一次“卸载后复挂校验”，确认数据落盘后再拔出：

```bash
mount /dev/disk/by-id/ata-TOSHIBA_MQ04UBB400_Y45DT0CKT-part2 /mnt/rescue5090
du -sh /mnt/rescue5090/5090-data-rescue-20260617/data-root
test -f /mnt/rescue5090/5090-data-rescue-20260617/rescue_manifest.txt && echo manifest_ok
sync
umount /mnt/rescue5090
```

确认没有进程占用后再拔盘：

```bash
findmnt /mnt/rescue5090 || echo unmounted_ok
lsof +f -- /mnt/rescue5090 2>/dev/null || true
```

## 9. 如果必须保留 TOSHIBA 现有 NTFS

不推荐。NTFS 不适合完整保存 Linux owner、permissions、xattrs、symlink/hardlink 语义。只有在必须保留该盘现有内容时才用。

挂载 NTFS：

```bash
mkdir -p /mnt/rescue5090_ntfs
mount -t ntfs3 /dev/disk/by-id/ata-TOSHIBA_MQ04UBB400_Y45DT0CKT-part2 /mnt/rescue5090_ntfs
mkdir -p /mnt/rescue5090_ntfs/5090-data-rescue-20260617/data-root
```

复制时不要使用 `-A -X --numeric-ids`，只保留普通文件内容和时间：

```bash
cd /data

rsync -rtDhl --ignore-errors --partial --append-verify --info=progress2 \
  --exclude='/lost+found' \
  ./ /mnt/rescue5090_ntfs/5090-data-rescue-20260617/data-root/ \
  2>&1 | tee /mnt/rescue5090_ntfs/5090-data-rescue-20260617/rsync_ntfs_$(date +%Y%m%d_%H%M%S).log
```

## 10. Rescue 后不要继续使用旧盘或移动盘跑实验

即使复制完成，也不要继续把旧 `/dev/sda` 当可靠数据盘使用；也不要把 TOSHIBA 移动盘当 5090 长期 `/data` 替代品。后续建议：

1. 更换 `/dev/sda`。
2. 在新健康盘上恢复 `/data`。
3. 将 TOSHIBA 移动盘上的 rescue 数据导入新健康盘或 4090 / NAS 等长期稳定存储。
4. StoryMotion / PulpMotion cache、checkpoint、runs 迁移到新盘。
5. 再重跑未完成 full metric：
   - Stage1 mixed full
   - human text `zero_human`
   - human text `shuffle_human`
   - human text `zero_all`
   - camera latent `noise_matched`
