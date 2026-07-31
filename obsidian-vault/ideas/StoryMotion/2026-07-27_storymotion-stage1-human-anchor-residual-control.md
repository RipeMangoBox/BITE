---
title: "StoryMotion Stage1 Human-anchor residual control"
status: closed_invalid_hml_imputation_no_stage2
hypothesis: |
  A Camera-free Human anchor is structurally useful, but heterogeneous HumanML
  supervision is admissible only when missing rotations are explicit or derived
  from verified common-source SMPL poses rather than mean-imputed as observations.
tags:
  - StoryMotion
  - stage1
  - HumanML3D
  - representation-control
  - status/closed
source_notes:
  - "[[current]]"
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-22_storymotion-humanml3d-fixed-camera-augmentation-plan]]"
created: 2026-07-27T12:11:37+08:00
updated: 2026-07-28T12:19:45+08:00
---

# StoryMotion Stage1 Human-anchor residual control

> [!abstract] Closed decision
> 两条 non-causal Stage1 fresh `636K` arm 已在 Pulp pure test 与 HumanML3D validation 上完成逐样本真实长度的 owning-decoder reconstruction audit。Pulp-only 保留为 architecture control；mixed arm 虽改善 HumanML3D root/local，却把未同源的 rot6D 通道写成 Pulp mean而没有显式 missingness，这是被禁止的伪观测。该 checkpoint 只保留为 partial-supervision diagnostic，禁止建立正式 Stage2 cache、训练 Stage2 或参与 promotion。C3-25 seed17 Stage1 与 Unified-3 `105K` mainline 不变。

## 1. 与 fixed-Camera augmentation 的边界

本实验不是 [[2026-07-22_storymotion-humanml3d-fixed-camera-augmentation-plan]] 的 A0–A4 数据增广：它没有检索 HumanML3D–Pulp pair、没有构造 fixed-Camera 新样本，也没有建立 HCCC 或 Stage2 mixture。这里回答的是一个独立 Stage1 问题：在同一 Human-anchor/residual architecture 与训练日程下，用 HumanML3D partial root/local exposure 替换 Pulp-only anchor exposure是否形成可晋升的 reconstruction trade-off。

## 2. Matched contract

| version / run | Stage / mode | 唯一数据轴 | 完成边界 | 可解释范围 |
| --- | --- | --- | --- | --- |
| Pulp-only matched / `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726` | Stage1 paired reconstruction | anchor batches 只来自 Pulp；其余 architecture、objective、phase length、role exposure 与 mixed arm matched | fresh `636K` | Pulp paired reconstruction 与跨域 HumanML root/local control |
| HML-root-local + Pulp-full / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_seed17_5090g2_20260726` | Stage1 paired reconstruction diagnostic | HumanML3D 只监督 root/local；Pulp full batches 保持 Human199 + Camera14 | fresh `636K` | 只允许审计 Pulp paired 与 HumanML root/local；因 HML rot6D 伪缺失输入而禁止 Stage2/promotion |

两条 arm **都基于同一个 redesigned Stage1**：`human_anchor_interaction_residual_199_14_128_16_48_v1`，从 seed17 fresh 训练，architecture、objective、phase length、optimizer steps 与 role exposure matched；不是一条 redesigned、一条旧 C3。两条 checkpoint、构造器、加载与 evaluator 均显式断言 `is_causal is False`。

### 2.1 `r2/r3/r4` 不是 setting

run 名里的 `rN` 只表示该 artifact lineage 内部的 revision/retry ordinal，用来保证 fail-close 后启用新 root；它不是 seed、模型代际、数据版本、训练轮数或结果等级。training `r3`、Pulp eval `r4`、HML eval `r2` 与 visual bundle 的 `r1` 分属独立计数器，彼此不能对齐。完整语义只由 run ID 和相邻 contract定义；旧 revision被删除或归档后，ordinal gap 仍有意保留。

## 3. 64-frame 与有效长度审计

- 旧/mainline C3-25 Stage1 的 `fixed_max_frames=0`；Pulp collator 使用 batch 内动态最大长度与有效帧 mask。配置中的 `seq_len=64` 不是对真实 Pulp sample 的首 64 帧裁切，pure-test 实际长度范围为 `9–251`。
- redesigned Stage1 的 Pulp collator同样是 `fixed_max_frames=0`，训练不丢弃长 sample 的第 65 帧以后内容。
- HumanML3D adapter 先做 `20→30 fps`，再按最大 `300` 帧、stride `240` 形成 sliding windows，并强制加入 tail-aligned 最后窗口。因此它会分窗，但不是 first-window-only，也不会静默丢掉长 motion 尾部。
- formal eval 则在每个 sample 进入 non-causal encoder–decoder 前裁到 exact valid length，future batch padding 不可见。

结论：两版 Stage1 都没有“固定只训练 first 64 frames”的严格裁切。Pulp 使用原始全长；当前 HumanML preprocessing 对超过 300 帧的序列做覆盖尾部的重叠分窗。

## 4. HML 与 Pulp 如何联合训练

| phase | steps | HML+Pulp arm | Pulp-only matched arm | 更新边界 |
| --- | ---: | --- | --- | --- |
| A | 210K | anchor cycle `HML×4 + Pulp×1` | 以 Pulp anchor 替代 HML，保持相同 role exposure | Human anchor/local modules |
| B | 210K | Pulp full joint | Pulp full joint | Camera/framing/interaction；Human modules frozen |
| C | 216K | replay `HML×3 + Pulp×7` | matched Pulp replay | joint；Human learning rate 为主率 `0.1×` |

“HML-root-local”描述的是这次 artifact 的 **partial supervision boundary**，不是一个合规的 full-Human representation：

- Human199 的 root/yaw 是 channels `0:4`，joint rot6D 是 `4:136`，RIFKE local joints 是 `136:199`。
- 当前 RIC263 adapter 曾经用 IK 派生 `4:136` 的 rot6D，但这些旋转不是 Pulp TRAM/SMPL 通道的同源观测。dataset loader把它们改为 Pulp-normalized mean（归一化后为零），HML objective再排除该块；真正参与 HML supervision 的只有 root/yaw + local joints。
- 这种处理没有 availability mask，因而把“未知”伪装成“观测到平均姿态”。按当前政策这是禁止的，不再称为可接受的 missing-data policy。历史 artifact 的 machine key `pose6d_policy` 是旧命名；其语义实际是 rot6D。
- Pulp full batches仍监督完整 Human199、Camera14 与 framing；因此 HML+Pulp checkpoint 不是 root/local-only 模型，但它的 HML 域证据只能写成 root/local-only。

### 4.1 为什么 RIC263 rot6D 不能直接变成 Pulp rot6D

rot6D 只是一种矩阵编码；真正不可逆的是其上游。HumanML RIC263 先把关节放到 fixed skeleton、地面、原点和初始朝向，再从 joints通过 IK 选出一组 21-joint rotations；Pulp 则使用 TRAM/SMPL 给出的 22-joint local rotations并按自身 RIFKE 处理 root yaw。仅由 joint positions 不能恢复 bone-axis twist，leaf orientation也完全不可观测，IK 的平滑/先验只是在多解中选一个。因此当前 RIC263 路径无法恢复与 Pulp 同源的旋转观测。

如果回到 HumanML/AMASS 的原始 SMPL-family axis-angle 或 rotation matrix，则原则上可以转换：统一 body model、joint hierarchy/order、rest offsets、坐标基、root-yaw factorization，并在 SO(3) 上做 20→30 fps 插值；随后用 FK/SMPL round-trip 和逐关节 geodesic 审计。此时转换的是共同上游 pose，而不是从 RIC joints 猜回已丢失的旋转。若原始 pose 不可得，合规替代是独立 root/local encoder或带 availability mask 的 auxiliary，不是 mean fill。

## 5. Canonical evaluation closure and reversal

- Pulp：pure test `N=4,053`，固定 ordered-ID cohort；Human199 与 Camera14 均由各自 exact checkpoint 的 owning decoder 重建。
- HumanML3D：validation `N=1,460`，固定 ordered-ID cohort；只评价 converted root/local geometry。
- Camera14 采用 Pulp owning policy：第一帧 decoded Human root 加第一帧 relative distance 定义 Camera origin，随后累计反归一化 translation velocity。
- Pulp `N=4,053` 是 Pulp TRAM/SMPL + Camera14 域；Pulp-only 获得更多 matched anchor exposure，因此在 Human root/heading/global 与 Human–Camera projective geometry 上明显更好。同一 GT-Human origin 下两条 Camera branch 接近，因此主要回退不能写成 standalone Camera decoder failure。
- architecture 在代码上保证 `z_h=E_h(H)` 与 Camera 输入逐元素无关，preflight 也用随机 Camera 验证该不变量；这支持 Human branch 的单向解耦有效。Camera decoder仍读取 `z_h/z_hc/z_c`，owning origin 与 projection仍读取 decoded Human，所以这不是双向或端到端完全独立。
- HumanML `N=1,460` 是 converted 20→30 fps root/local-only 域；mixed arm 直接接受该域 supervision，因此在 root/local geometry 上明显更好。该结论不覆盖 rot6D、Camera、projective、text semantic 或 free generation。
- 优势反转不是 `N=4,053` 和 `N=1,460` 的样本数本身导致，而是 **eval domain 与训练 exposure 对齐发生反转**；同时说明当前 replay ratio 与 rot6D 伪缺失输入是 setting boundary。由于 mixed setting 本身已被判为不合规，这一反转只能保留为 retrospective diagnostic，不能证明一种可部署的跨域训练配方。
- 两个 cohort 不可合并成一个排名。数据源替换形成 domain trade-off，没有跨域 Pareto win。
- mixed arm 的 checkpoint 明确 invalid for Stage2；Pulp-only 只保留为 architecture/matched control，不替换 C3-25。
- 本实验不授权任何 redesign Stage2 cache/training，也不产生 Direct-H、Direct-C 或 joint-parallel generation claim。

完整 Stage1 decoded metric table 只见 [[StoryMotion-valid-metric-ledger#6. Canonical Stage1 true-length paired reconstruction]]。

## 6. MotionStreamer272 completeness and adapter boundary

4090 的 `/data/public/ripemangobox/Motion/datasets/HumanML3D_272` 是指向 `272-dim-HumanML3D` 的 symlink。MotionStreamer schema 确实包含构造 full motion199 所需的旋转信息候选：root planar velocity `2D`、heading angular rot6D `6D`、22-joint local position `66D`、local velocity `66D`、22×joint rot6D `132D`，合计 `272D`。

2026-07-27 全量只读扫描结果：

- split 唯一 ID `28,764`，实际可读 motion arrays `26,846`，缺 `1,918`；train/val/test 为 `23,384 / 1,338 / 4,042`，因此 val/test 均不是原 HumanML3D `1,460 / 4,384` 的完整副本。
- 现有 26,846 个 array 全部为 finite `[T,272]`、`float64`；长度 `3–300`，其中 `26,276` 条超过 64 帧。`Mean.npy` / `Std.npy` shape 均为 `[272]` 且 Std 全正。
- dataset metadata SHA256 为 `6cfb0e739b7fa0f3feef777fb5d619d5cef6df4273adb9981d0e683d9010598e`；Mean/Std SHA256 为 `1200c165…1272` / `cb699c61…d99c`。

本机相邻 codebase 的 `build_humanml3d_272_self.py` 显示，一条更可靠的 272 路径可以直接读取 HumanML source `pose_data` 的 axis-angle，取 22-joint local rotations 后再构造 heading-free 272；这避免了从 RIC joints做 IK 的根本歧义。但当前下载目录没有把每个 array 与该 builder/source pose 的 immutable provenance闭合，而且目录本身 **不完整，不能直接替换** 当前 RIC263 adapter。修复缺失 array 后，还需预注册 Y-up→Story Z-up、20→30 fps 的 SO(3) 插值、root heading delta/origin、SMPL joint hierarchy/rest pose、rot6D row/column serialization 与 Pulp normalization，并用 FK/SMPL round-trip、逐关节 geodesic 和分布审计确认它能产生同语义 Human199；“维度包含 rot6D”不等于“已与 Pulp Human199 对齐”。

## 7. Visualization and evidence routing

统一 Gradio 运行于 4090 `0.0.0.0:7865`；Mac 端继续使用：

```bash
ssh -N -L 17867:127.0.0.1:7865 4090
```

同一应用包含 Stage2 六路 backbone 页，以及：

- `Stage1 · Pulp four-way`：GT、C3-25 Stage1、redesign Pulp-only、redesign HML+Pulp；每路同时显示 global Human + owning Camera 与 projective geometry。
- `Stage1 · HML root/local`：HML reference、redesign Pulp-only、redesign HML+Pulp；明确限制为 root/local。
- 每个 tab 都有“同步播放当前组”，真实浏览器验证四路/三路视频均从 `t≈0` 同步启动；Stage2 六路页仍正常加载。

本轮 fixed-8 视觉审查记录为：

- Pulp 页中 redesign Pulp-only 是 redesign 两臂的明确胜者，并显示出更强的 Human-first independent-control 观感；相对 C3-25 Stage1 未见明显视觉质量恶化。该判断不覆盖 formal Pulp Human reconstruction 排名，后者仍由 ledger 的 canonical 数值单独解释。
- C3-25 与 redesign Pulp-only 都在若干 sample 最后一帧出现 Camera 跳动，导致 owning-camera projection骤变。当前只记录为共享 terminal-boundary failure；需从 fixed samples审计末两帧 Camera center/rotation/projection delta 后才能归因于 Camera14 velocity endpoint、decoder padding/crop 或数据终点。
- HML 页中 redesign Pulp-only 对若干动作已具备预期的 zero-shot root/local reconstruction，HML+Pulp 更好；但两者都会随时间出现整人异常旋转。该页渲染不读取 decoded rot6D，所以直接可见责任是累计 root/yaw；mean-imputed rot6D 只能作为可能的 shared-encoder/domain-cue 间接因素，不能写成已确认根因。

新 bundle root：

`/data/public/ripemangobox/Motion/StoryMotion/runs/vis/stage1/stage1_c3_hanchor_gradio_fixed8_r1_seed17_4090g0_20260727/`

manifest / asset builder / merged Gradio SHA256：`39f649a2d074f1bffab607d70fbaf54d087263164498e898cadcfb7f7b7404fe` / `d996e04c5f5eed45fa65d35ced2e2261dd416e85e5f4005579ef0c6c629146c0` / `ad7f275348397b80dd44bb327681ca55329a01c2f529820eb4e4ef7761a6a50c`。

- machine-readable result、records、fixed samples与 Stage1 decoded metrics：[[StoryMotion-valid-metric-ledger#6. Canonical Stage1 true-length paired reconstruction]]；eval/vis manifest 与 checkpoint/contract identities：[[Storymotion-exp-sha]]
- 当前 mainline 与下一授权动作：[[current]]
- finalized milestone：[[version_family]]
- true-length、Human199/Camera14 与 owning-decoder语义：[[StoryMotion-metric-computation-io]]

若未来重开该轴，必须另立新 contract，至少补齐可观察且 provenance-closed 的 rot6D supervision、replay-ratio ablation、末帧 Camera probe 与跨 seed 验证；不得复用本次 mixed checkpoint，也不得从本次 root/local partial result 推导 Stage2 或 joint 能力。更完整的架构推理与可迁移检查表见 [[StoryMotion_Checkmate]].
