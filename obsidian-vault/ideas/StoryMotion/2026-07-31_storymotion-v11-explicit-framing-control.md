---
title: "StoryMotion v11 Explicit Screen-space Framing Control"
hypothesis: |
  A zero-initialized adapter on the frozen v11 C0-GEO Camera branch can expose
  explicit subject screen position, scale, and visibility control while the
  absent-control path remains exactly identical to the selected parent and the
  Human owner remains frozen.
status: preregistered_screen
tags:
  - StoryMotion
  - version/v11
  - control/framing
  - status/active
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/CGF_2024/Cinematographic_Camera_Diffusion_Model]]"
  - "[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation]]"
created: 2026-07-31T03:05:00+08:00
updated: 2026-07-31T03:41:15+08:00
---

# StoryMotion v11 Explicit Screen-space Framing Control

> [!important] Causal question
> 在 exact v11 C0-GEO Camera EMA `105K`、固定 observed Human 与原 Camera
> caption 下，只增加一个 zero-init framing adapter，显式输入 subject screen
> `x / y / log-scale / out-of-frame` 的 sequence summary，能否提高构图约束服从度，
> 且 absent-control 路径与父 endpoint forward exact？

本页是 explicit framing control 的唯一计划与 screen 裁决所有者。运行进度只写
`runs/`；screen 数字只在本页形成裁决，正式审计后才进入
[[StoryMotion-valid-metric-ledger]]。

方法定位参考
[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]、
[[analysis/CGF_2024/Cinematographic_Camera_Diffusion_Model|Cinematographic Camera Diffusion Model]] 与
[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation|Auteur]]。
本实验不声称首次提出 cinematographic framing；changed slot 是在 StoryMotion
Human-first 3D planner 中增加数值化、subject-aware 的 composition condition，并
结构性保护原三模式能力。

## 1. 固定与可训练边界

- parent：v11 C0-GEO EMA Camera `105K`；C0-LAT 共同 mainline 身份不变。
- Stage1、owning decoder、Human teacher、Camera parent 与 text encoder 全部冻结；
  temporal tokenizer 保持 `is_causal=false`。
- adapter 输入是 train-only 标准化的 sequence-mean framing4 与
  `condition_present`；输出一个 Camera token residual。
- adapter 最后一层 zero-init；`condition_present=false` 时 residual 结构性为零，
  训练前后都必须与 parent Camera forward 逐元素相同。
- 不训练、不评估 joint-parallel；首轮只在 Direct-C 使用 GT Human。

## 2. 两臂短 screen

两个 arm 使用相同 parent、adapter 初始化、first-512 overfit subset、batch／noise
trace、LR 与 `2K` optimizer budget，在双 4090 同时运行：

| arm | train objective | changed comparison |
| --- | --- | --- |
| F-LAT | Camera64 masked-valid flow | framing condition 是否能仅靠 flow 进入 frozen prior |
| F-GEO | 同一 flow + 继承 C0-GEO calibration 的 decoded Camera14／framing auxiliary | 显式 decoded supervision 是否改善 control adherence |

Camera base、Human 与 decoder 均没有 optimizer group。screen 每 `500` step 保存
adapter raw／EMA；`2K` endpoint 在同 ordered first-64、Euler50、相同 Camera noise
上评测。

## 3. Screen 指标与 gate

评测包括：

- target-condition：predicted sequence-mean framing4 对目标的逐字段 MAE；
- swap-condition：将控制 summary 循环移位，输出构图向 swap target 移动的比例，
  并验证其不是完全忽略 condition；
- parent comparison：同噪声 Direct-C 的 Camera geometry、framing 与 latent 幅度；
- absent-control exact：Camera forward max-abs `0.0`；Direct-H 由冻结 owner 保持
  exact；
- stability：finite loss／grad、EMA 与 raw 均可加载。

Continue 条件：两臂至少一臂相对 parent 在四个 framing 字段形成明确 control
adherence 改善；swap response 方向正确；absent-control exact；Camera center／rotation
与 boundary dynamics 不出现灾难性回退。若 F-GEO 只改善 target reconstruction 但
swap 不响应，则判为 label leakage／memorization，不长训。若 F-LAT 与 F-GEO 都忽略
condition，则停止小 adapter，不能靠延长预算救活。

## 4. 有条件长训

screen 胜出 arm 从 parent fresh adapter initialization 在 full train set 启动 `30K`
长训，不从 first-512 overfit 权重续训。每 `1K` 保存 raw／EMA 与完整 resume state，
每 `5K` 执行 fixed first-64 target／swap screen。连续两个 screen control adherence
反转、parent geometry 灾难性退化或 gradient instability 时 guard stop。

`30K` 只是正式评测候选，不自动进入 C0 co-mainline；正式 evidence 仍需 Direct-H、
Direct-C、sequential Human→Camera、explicit-control task、decoded geometry、固定视觉
与 sample identity 审计。

## 5. 首轮 sequence-mean adapter screen 裁决

> [!failure] F-LAT／F-GEO 均不得直接长训
> 两臂在 ordered first-64、Euler50、同 Camera noise 上都满足 absent-control sampler
> max-abs `0.0`，swap 四字段 MAE 全部改善，且 Camera center／rotation 没有回退；
> 但 target-condition 只有 screen `x / y` 两字段优于 parent，`log-scale / out-of-frame`
> 均略差。因此严格按预注册的四字段 target gate 停止这两个 objective，不放宽 gate。

| version / run | target 改善字段 | swap 改善字段 | swap 方向一致率范围 | target Camera center／rotation 相对 parent | gate |
| --- | ---: | ---: | ---: | ---: | --- |
| v11 / `v11_f_lat_framing_screen2k_seed17_4090g0_20260731` | 2／4 | 4／4 | 0.688–0.828 | 0.990／0.981 | fail |
| v11 / `v11_f_geo_framing_screen2k_seed17_4090g1_20260731` | 2／4 | 4／4 | 0.688–0.844 | 0.990／0.978 | fail |

该结果排除了“adapter 完全忽略 condition”：swap response 的四字段方向和误差都形成
一致信号。失败点是 own-pair flow／GEO 只提供相关性监督，无法保证每个控制字段朝请求值
移动；target 的 `log-scale / out-of-frame` 方向一致率仅约 `0.44–0.58`，不能靠 inference
guidance 放大修复。

## 6. Counterfactual repair screen

下一轮保持同一 frozen C0-GEO parent 与同一 zero-init adapter，但从 parent fresh 初始化，
在 own-pair F-GEO loss 之外增加 counterfactual decoded-framing loss：batch 内将 framing
condition 循环移位，预测 clean Camera 经 owning Stage1 decoder 得到 true-length sequence
mean framing4，直接对移位后的标准化 control 做四字段 MSE；不使用 counterfactual Camera
latent ground truth。

先在 ordered first-128、optimizer 未启动时分别测 own F-GEO 与 counterfactual loss 对
adapter 的梯度范数，定义 gradient-matched `lambda_cf`。双 4090 配对运行
`CF-1` 与 `CF-4`：二者分别使用 `1× / 4×` matched gradient weight，其余 first-512、
batch、noise、LR、`2K` 与 endpoint evaluation 全部相同。仍使用第 3 节的原四字段
target／swap、absent exact 与 `1.5×` geometry gate；至少一臂完整通过才从 parent fresh
初始化部署 full-train `30K`，不得续用 first-512 screen 权重。

## 7. Counterfactual screen 裁决与长训选择

> [!success] 选择 CF-4，部署 fresh full-train `30K`
> CF-1 与 CF-4 都通过四字段 target、四字段 swap、方向响应、absent exact 与 Camera
> geometry gate。CF-4 在四个 target MAE 与四个 swap MAE 上逐项优于 CF-1，target
> Camera center／rotation 相对 parent 与 CF-1 基本持平，因此选择 CF-4。

| version / run | target MAE `x / y / log-scale / out` | swap MAE `x / y / log-scale / out` | swap 方向一致率范围 | target Camera center／rotation 相对 parent | gate |
| --- | --- | --- | ---: | ---: | --- |
| v11 / `v11_f_cf1_framing_screen2k_seed17_4090g0_20260731` | 0.1902／0.2896／0.0964／0.0510 | 0.2979／0.8149／0.3137／0.2033 | 0.844–0.969 | 0.967／0.921 | pass |
| v11 / `v11_f_cf4_framing_screen2k_seed17_4090g1_20260731` | 0.1854／0.2492／0.0780／0.0490 | 0.2110／0.5168／0.2140／0.1385 | 0.859–0.953 | 0.967／0.925 | pass／selected |

两臂 absent-control 完整 Euler50 sampler max-abs 均为 `0.0`。parent 的 target MAE 为
`0.2630 / 0.3548 / 0.1092 / 0.0631`，parent-to-swap MAE 为
`0.4612 / 1.2159 / 0.4355 / 0.2785`，因此表中改善不是 arm 间相对指标。

选择的长训 run 为
`v11_f_cf4_framing_long30k_seed17_4090g0_20260731`，contract SHA256
`bf2c7b48b6eafbd25b82c3745cbf17f693780e187fed670e9c03888a5148c3f1`。
它从 exact C0-GEO `105K` parent 与 fresh zero-init adapter 开始，使用 full train
`162,760` samples、batch `128`、`30K` optimizer steps、每 `1K` weights／每 `5K`
full-resume；不得加载任一 screen adapter。每 `5K` 的 first-64 control screen 仍使用
第 3 节 gate，连续两个 screen 反转时停止。
