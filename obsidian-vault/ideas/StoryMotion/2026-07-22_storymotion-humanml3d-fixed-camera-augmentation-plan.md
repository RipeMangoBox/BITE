---
title: StoryMotion HumanML3D fixed-Camera augmentation plan
date: 2026-07-22
status: planned_no_substantive_experiment
type: experiment-plan
tags:
  - StoryMotion
  - data-augmentation
  - HumanML3D
  - human-camera-compatibility
canonical_axis: humanml3d_fixed_camera_augmentation
manual_labels_current: 0
---

# StoryMotion HumanML3D fixed-Camera augmentation plan

## 0. 当前证据边界

截至 2026-07-22，没有 HumanML3D × C3-25 的数据增广实质实验。现存 `render_humanml3d_fixed_camera.py` 与 Gradio 中的 8 条样例只证明 HumanML3D 263D motion 可以经 joints-level adapter 转到 Pulp199，并通过旧 v7.14 Stage1 做 fixed-camera 可视化；它们不是 PulpMotion-HumanML3D 配对、C3-25 encode、HCCC 验收或 Stage2 混合训练证据。

因此本页从 plan 状态开始，不把旧 8 条可视化计为数据质量 screen。原始 PulpMotion 自动筛选由 [[ideas/StoryMotion/2026-07-17_storymotion-v8-2333-data-curation-plan]] 单独管理；本页只管理“创造新 Human-Camera pair”的独立因果轴。

## 1. 核心假设与首选方案

核心假设：在保持真实电影 Camera trajectory 与 camera text 不变时，用语义和动作均高度匹配的 HumanML3D Human 替换 PulpMotion Human，可以增加 Human motion/text 多样性；只有新 Human 与原 Camera 仍保持构图、跟随关系和电影语言兼容时，这些 pair 才能成为有效的 StoryMotion 联合训练数据。

首选方案是 **fixed Camera, augment Human**。暂不执行 fixed Human, generate Camera，因为 PulpMotion Human 原始质量仍在筛选，且 Director 或 video-camera-control 链会同时引入 Camera 生成、视频生成与重估误差，无法把收益归因于多数据集增广。

## 2. 不可改变的边界

- C3-25 的非因果 tokenizer、Human199 + Camera14 表示、Human128 + Camera64 latent 顺序和 owning decoder 不变。
- HumanML3D 不能直接补零或把 263D feature 当作 Pulp199。必须先恢复几何、统一 skeleton/fps/坐标系，再构造 Pulp199。
- first-frame position/heading 对齐发生在 world-space Human geometry 上，不在 z-normalized latent 中直接平移或旋转。对齐完成后才由冻结 C3-25 Stage1 joint encoder 编码 Human + Camera。
- 原始 PulpMotion 与 HumanML3D parent manifests 不可变；每个新 pair 保存双 parent ID、匹配分数、几何变换、Camera owner、caption owner 与 reason codes。
- 当前自动构造与自动筛选阶段不进行人工标记。若未来需要 promotion audit，另建版本化人工抽查合同，不能把本页 plan 写成已有标签。
- MotionStreamer 的 Two-Forward/exposure-bias 思路可以作为训练策略参考，但其 causal tokenizer 不得进入 StoryMotion Stage1/Stage2。

## 3. 数据构造 pipeline

```text
Pulp clean-screen Human/Camera pair
  + HumanML3D train-split motion/captions
  -> canonical geometry conversion and duration compatibility
  -> dual retrieval: CLIP text match AND TMR motion match
  -> mutual-nearest-neighbor and margin checks
  -> align HumanML3D root position + heading to Pulp first valid frame
  -> keep Pulp Camera trajectory + camera text fixed
  -> rebuild Pulp199 Human and project through the real Camera
  -> automatic Human validity + Human-Camera compatibility screen
  -> frozen C3-25 Stage1 joint encode
  -> versioned augmented Stage2 cache
  -> exposure-matched Stage2 mixture ablation
```

### 3.1 Source split

- Pulp source只允许来自最终选定的自动 clean-screen train IDs；Pulp test IDs 不参与 matching 或训练。
- HumanML3D 只使用官方 train split 构造训练 pair。validation/test 保留用于 adapter 与跨数据集检查，不进入增强训练。
- 若无法得到可靠 movie/source identity，所有 learned Human-Camera evaluator 只能作为 diagnostic；不能用随机 sample split 伪装 source-disjoint 泛化。

### 3.2 HumanML3D 到 Pulp199

1. 使用 canonical inverse RIC 恢复 HumanML3D 22-joint geometry 与 global root trajectory。
2. 从 20 fps 重采样到 Pulp 25 fps；禁止简单重复帧。
3. 用既有 adapter 的坐标旋转与 skeleton mapping 作为起点，但重新绑定 C3-25 invariant，并报告 reconstruction、root/yaw 与 bone consistency。
4. 仅匹配 duration ratio 合理的候选；P0 默认 `[0.9, 1.1]`。优先裁剪较长 motion，不对短 motion 做循环或静止尾帧填充。
5. 计算第一有效帧刚体变换，使 HumanML3D root position 与 heading 对齐到目标 Pulp Human；同一 SE(2) 变换作用于完整 Human trajectory，禁止逐帧追 Camera。

## 4. 双检索与自动阈值

对每个通过自动清洗的 Pulp Human pair，在 HumanML3D train split 中执行：

- Text branch：Pulp human caption 与 HumanML3D caption 的 normalized CLIP cosine。
- Motion branch：转换后的 Pulp/HumanML3D motion 经同一冻结 TMR motion encoder，计算 motion-motion cosine。
- Dual gate：初始候选采用 `CLIP >= 0.95 AND TMR-motion >= 0.95`；`0.95` 是待观察的高精度起点，不是预先宣称可达的正式阈值。
- Retrieval gate：要求双向 mutual top-1，且 top-1 相对 top-2 具有预声明 margin；若绝对阈值导致 yield 为零，先报告分布，不可事后降低阈值并仍称其为原 gate。
- 去重：第一阶段每个 Pulp pair 和 HumanML3D motion 最多各使用一次。top-K 复用与交叉交换另立比例 ablation。

必须同时保留四个自动对照：random duration-matched、CLIP-only、TMR-only、CLIP+TMR dual。只有这样才能判断收益来自语义匹配、动作匹配还是仅增加数据量。

## 5. Human-Camera Cinematic Compatibility（HCCC）

设计依据见 [[ideas/camera/2026-06-05_camera-movement-generation-system-survey-llm-audit-merged]] 与 [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness]]。PulpMotion/CondensedMovies 中真实 Camera-Human pair 是弱正例，不是无噪声真值；增强后必须同时接近真实 matched 分布，并显著优于 hard-shuffled negatives。

P0 不压成单一加权分数，报告以下向量：

- `FrameFit`：投影可见率、Out、头脚 margin、bbox scale、景别与主体尺度稳定性。
- `FollowSync`：Human root velocity、heading、动作显著性与 Camera translation/pan/rotation 的 lagged coherence；静态镜头单独分层。
- `ShotDynamics`：Camera jerk、角加速度与连续性在 matched camera-type/action/duration 分层中的 percentile。Camera 固定时该项应与 parent 相同，用作 provenance assertion。
- `CamText`：CLaTr camera text-trajectory 一致性。Camera 与 camera text 均固定时应 bitwise/数值一致，用作构造完整性检查。
- `PairContrast`：`delta_pair = s(H, C, T_h, T_c) - mean_k s(H, C_k_negative, T_h, T_c)`；报告 matched-vs-hard-shuffled AUC 与 rank@K。

hard negative 在相同 duration、capture/source、Human 动作强度与 Camera motion type 内交换 Camera。若训练 learned `PairContrast` evaluator，train/eval 必须 movie/source-disjoint，并禁止使用 pair ID、影片 ID 或年份 proxy 作为输入。

## 6. 实验阶梯

| 阶段 | 改动 | 规模 | 输出 | 进入下一阶段条件 |
| --- | --- | ---: | --- | --- |
| A0 C3 adapter audit | 只验证 HumanML3D→Pulp199→C3-25 encode/decode | 1,024 HumanML3D train clips | geometry、root/yaw、physical、hash ledger | 无 contract/invariant 错误，adapter 不丢 root travel |
| A1 retrieval screen | random、CLIP-only、TMR-only、dual 四组 | 全量检索，只物化每组 top 1,024 | yield、score/margin、duration/source 分布 | dual 不是零产出且优于单分支 hard controls |
| A2 fixed-Camera construction | 固定真实 Pulp Camera，替换并对齐 Human | dual top 2,048 起步 | Pulp199、projection、HCCC、candidate manifest | Human validity 通过，HCCC 接近 real matched 且优于 shuffled |
| A3 Stage2 mixture screen | 冻结 C3 Stage1，改变 Stage2 train cache mixture | `0% / 10% / 25%`，总 exposure matched | Direct-H、Direct-C、joint parallel、HCCC | joint 改善且 clean Direct-C/Human 不系统退化 |
| A4 formal recipe | 从零或早期引入通过的 mixture | 完整预注册 budget | 4,053 formal + 多 seed | 才可写入 mainline 数据 recipe |

A0-A2 是数据构造实验，不训练新 Stage1/Stage2。A3 只改变 Stage2 数据 mixture；若未来考虑用增强 pair 重训 Stage1，必须另建 representation run，不能与 A3 合并归因。

## 7. 自动 gate 与停止条件

- Adapter gate：所有 shape/fps/坐标、C3 non-causal、checkpoint/decoder/cache hashes 可审计；任何 root travel 被静默抹除即停止。
- Retrieval gate：报告绝对阈值、mutual-NN、margin 后的逐级 yield。若 dual gate 产出不足，不执行 Camera-Human 交换训练。
- Human gate：应用 versioned Physical 与 TMR screen；两者按异常并集排除，不只删除异常交集。
- Camera provenance gate：Camera14、camera text、Camera-only metrics 与 parent 保持一致；不一致说明构造 pipeline 改动了不该改的分支。
- HCCC gate：增强 matched 分布必须显著优于 hard-shuffled；`FrameFit/FollowSync/PairContrast` 任一出现系统性越界即 quarantine candidate。
- Stage2 gate：A3 的训练步数、batch、task ratio、seed 和总 exposure 完全匹配。数据增广不得与 q(H_gt,t)/joint-pred-H robustness screen 同一 run 混合。

## 8. 必需 artifact

- `augmentation_contract.json`：双 parent manifest/hash、split、adapter/code hash、C3 checkpoint/decoder hash、matching encoder hashes、阈值与 seed。
- `match_candidates.jsonl`：Pulp/HumanML3D IDs、两类 caption、CLIP/TMR 分数、rank、margin、duration 与 source strata。
- `geometry_transform.jsonl`：fps、crop、root translation、yaw rotation、first-frame residual。
- `hccc_records.jsonl`：五维 HCCC、hard-negative IDs 与 reason codes。
- `augmented_manifest.jsonl`：只引用 immutable parents 与生成 artifact，不覆盖原始文件。
- `summary.json` 与 artifact SHA manifest：逐阶段 count、zero/nonzero counters、ordered IDs hash 与状态。

## 9. 立即待办

1. 冻结 Pulp 自动筛选采用的 Physical/TMR 阈值组合；当前 3×3 grid 只是 screen，尚无正式 clean parent。
2. 把既有 HumanML3D adapter 绑定到 C3-25 invariant，执行 A0 的 1,024 条 geometry audit。
3. 生成 HumanML3D train caption/motion embedding cache，并分别审计 CLIP/TMR encoder hash 与 batch invariance。
4. 运行 A1 四组 retrieval screen；在看到 yield 分布前，不创建 A2 增强 pair 或 Stage2 cache。

