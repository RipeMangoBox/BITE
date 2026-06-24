---
created: 1970-01-01T08:00
updated: 2026-04-11T00:38
---
# TAMR Stage4.1 D0 执行结果（HumanML3D-E 事件统计）

日期：2026-04-11  
执行脚本：`/home/ripemangobox/Coding/Github/Motion/TMR/scripts/d0_humanml3de_event_stats.py`

## 1. 输入与口径

- 数据：`datasets/motions/HumanML3D-E/data_{train,val,test}.npy`
- 事件解析：从 `caption` 中提取 `action i:` / `condition i:`
- overlap 口径：规则词命中（`while/meanwhile/simultaneous/at same time/during/concurrent`）
- 说明：该文件不含显式 event time span，overlap 比例为文本规则近似值

## 2. 核心统计

- 总 captions：`944`
- 可解析 captions：`938`（`99.36%`）
- 不可解析 captions：`6`

`K` 分布（基于可解析 captions）：

- `K=1`: `276` (`29.42%`)
- `K=2`: `363` (`38.70%`)
- `K=3`: `199` (`21.22%`)
- `K=4`: `70` (`7.46%`)
- `K=5`: `22` (`2.35%`)
- `K=6`: `6` (`0.64%`)
- `K=8`: `2` (`0.21%`)

派生比率：

- `K>=2` 占比：`70.58%` (`662/938`)
- `K=1` 占比：`29.42%` (`276/938`)
- 规则 overlap 占比：`4.48%` (`42/938`)

每条 caption 平均 event 文本长度（词数）：

- mean: `7.2528`
- median: `6.6667`
- p25/p75: `5.5 / 8.5`

每条 caption 平均 event 时长代理（`motion_length / K`，帧）：

- mean: `67.0381`
- median: `60.0`
- p25/p75: `35.0 / 89.875`

## 3. D0 Quantitative Gates 判定

1. Gate-1：`K>=2` 占比 `< 40%` ？
   - 实测 `70.58%` -> **未触发**
2. Gate-2：`K=1` 占比 `> 60%` ？
   - 实测 `29.42%` -> **未触发**
3. Gate-3：并行/overlap 占比 `> 15%` ？
   - 实测 `4.48%`（规则口径）-> **未触发**

## 4. D0 结论（Go/No-Go）

D0 给出的结论为：**GO**。  
即按 V4 路径，进入 `D1`（frozen minimal event-time head）是合理的。

## 5. 产物路径

- JSON: `RUN_DIR/stage4_1_d0_humanml3de/2026-04-11_d0_humanml3de_event_stats.json`
- CSV: `RUN_DIR/stage4_1_d0_humanml3de/2026-04-11_d0_k_distribution.csv`
- Markdown: `RUN_DIR/stage4_1_d0_humanml3de/2026-04-11_d0_report.md`
