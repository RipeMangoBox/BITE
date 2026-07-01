---
title: StoryMotion Canonical Plan
created: 2026-06-03T20:05:17+08:00
updated: 2026-06-03T21:32:03+08:00
status: archived
hypothesis: Given a sequence of 3D animation sections and a local keyframe/layer edit, StoryMotion-ASG predicts the affected sections, preserves protected interiors, and repairs only necessary boundary buffers through contact-consistent optimization or a 3D motion conditioner.
source_papers:
  - "[[STMC_Multi-Track_Timeline_Control_for_Text-Driven_3D_Human_Motion_Generation|STMC]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI.md|CondMDI]]"
  - "[[analysis/ECCV_2024/MotionLCM_Real_time_Controllable_Motion_Generation_via_Latent_Consistency_Model.md|MotionLCM]]"
  - "[[analysis/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation.md|Sketch2Anim]]"
  - "[[analysis/SIGGRAPH_ASIA_2024/MotionFix_Text_Driven_3D_Human_Motion_Editing.md|MotionFix]]"
  - "[[analysis/ICCV_2023/PoseFix_Correcting_3D_Human_Poses_with_Natural_Language.md|PoseFix]]"
  - "[[analysis/ECCV_2022/PoseScript_3D_Human_Poses_from_Natural_Language.md|PoseScript]]"
  - "[[analysis/CVPR_2026/ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning.md|ActionPlan]]"
  - "[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.md|PRISM]]"
external_refs:
  - https://amass.is.tue.mpg.de/index.html
  - https://babel.is.tue.mpg.de/
  - https://github.com/EricGuo5513/HumanML3D
  - https://motionfix.is.tue.mpg.de/
  - https://docs.blender.org/manual/en/latest/editors/nla/strips.html
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/cinematic-animation-track-in-unreal-engine
  - https://help.autodesk.com/cloudhelp/2025/ENU/Maya-Animation/files/GUID-BBCA0BC3-7608-4E86-8E9F-B4099C316156.htm
tags:
  - StoryMotion
  - motion_editing
  - animation_workflow
  - contact_constraint
  - production_workflow
---

# StoryMotion Canonical Plan

> [!note] 2026-06-04 继承关系
> 本文档是 human-motion-only ASG 收缩版，保留为 CSG 新版的地基。camera 协同重构后的当前方案见 [[2026-06-04_storymotion_cinematic_section_graph_plan|StoryMotion Cinematic Section Graph Plan]]。

> [!abstract] 当前 source of truth
> 本文档继承并收敛 [[ideas/StoryMotion/archived/v3/2026-06-02_storymotion_novelty_value_positioning|StoryMotion Novelty and Value Positioning]]。旧的 storyboard-conditioned generation 叙事已存档到 `archived/v2`，不再作为当前版本主线。经 DS 多轮反方审查后，核心修正为：**不要把 shot 当电影镜头，也不要把 locked interior / boundary buffer / cache key 伪装成数据集字段。StoryMotion 当前应定义为 Animation Section Graph 上的局部动作编辑与接触一致边界修复。**

## 1. 一句话目标

StoryMotion 第一版不碰手绘 storyboard，也不做 `storyboard image -> 3D animation`。这里的 `shot` 不再表示电影镜头，而是改称 **Animation Section**：一段在 DCC timeline / NLA / Sequencer / animation track 中可被剪切、混合、加层、重定时的 3D motion clip segment。

一句话完整目标：

> **StoryMotion-ASG = 给定一组已有 3D animation sections 和一次局部 keyframe / layer / mask / retiming 编辑，自动判断哪些 section 受影响，保护未编辑 interior，只在必要 boundary buffer 中做接触一致的过渡优化或 3D motion conditioning，从而输出一条可导回 DCC / engine timeline 的稳定多段 3D motion asset。**

这比上一版更窄，但更真实：

- 不声称理解真实分镜或导演镜头语言；
- 不声称从现有数据集中自动获得所有编辑字段；
- 不声称全自动接触 / 道具 / 多人交互；
- 第一版只做 **单人、无道具、motion clip sections、局部编辑后的边界修复与影响传播**。

核心研究价值也因此更明确：DCC 已有 clip / layer / blend，但主要靠人调；CondMDI / MotionFix 已能生成或编辑 motion，但不管理 DCC 式 section、protected interior、dirty propagation、undo/cache 和接触一致边界。StoryMotion-ASG 研究的是二者之间的空白。

## 2. 术语落地

### 2.1 Animation Section

**Animation Section** 是一个连续 motion segment，等价于工作流中的 animation clip / action strip / animation section，而不是电影 shot。

可对应到：

- Blender NLA 的 Action Strip / Transition Strip / blend in-out；
- Unreal Sequencer 的 Animation Sequence section、track layers、weight keyframes、automatic blend curves；
- Maya Animation Layers 的 additive / override layers；
- Unity Timeline Animation Track 的 track offsets、avatar mask、offset match fields。

因此，ASG 的节点不是“镜头”，而是“可编辑动作片段”。边表示相邻 section 的时间顺序、root/heading/contact 状态匹配要求、以及缓存失效依赖。

### 2.2 字段定义

| 术语              | 概念                                 | 是否来自数据集                          | 在 v0 中怎么用                                             |
| --------------- | ---------------------------------- | -------------------------------- | ----------------------------------------------------- |
| frame range     | section 的起止帧或起止秒                   | 可直接给或脚本生成                        | 用 BABEL start/end、HumanML3D clip range 或固定窗口切段        |
| semantic label  | section 的动作类别或文本描述                 | BABEL / HumanML3D / MotionFix 可给 | 用于分组、检索和生成编辑模板，不作为硬约束                                 |
| start/end state | section 起点和终点的姿态、root 位置、root 朝向   | 从 motion frames 可推导              | 作为边界匹配的主要状态                                           |
| root path       | root / pelvis 在时间上的轨迹              | AMASS / HumanML3D 表示中可得到或恢复      | 用于 trajectory edit、heading edit、transition continuity |
| heading         | 角色朝向，通常由 root orientation 推导       | 从 root rotation 可推导              | 判断下一个 section 是否需要重新对齐                                |
| contact state   | 脚或手是否接触地面 / 物体                     | 没有可靠直接字段                         | v0 只做脚接触，启发式估计 + 主动人工校正                               |
| locked interior | section 内部不允许被优化或生成器改动的帧 / 关节 mask | 不是数据集字段                          | 编辑协议元数据，类似 protected keyframes / locked mask          |
| boundary buffer | section 边界附近允许被修复的短窗口              | 不是数据集字段                          | 系统参数，默认约 0.2-0.4 秒，做 ablation                         |
| cache key       | section 计算结果的版本 hash               | 不是数据集字段                          | 工程元数据，用于 dirty flag 和 undo/cache                      |
| dirty flag      | section 或 edge 是否因编辑失效             | 不是数据集字段                          | 编辑器状态，用于影响传播                                          |
| edit command    | 可撤销的编辑操作记录                         | 不是数据集字段                          | 支持 undo/redo 和复现实验                                    |

重要修正：**Part I 不是训练模型从数据集中预测所有字段。Part I 是 compiler，把数据集直接字段、脚本推导字段、用户/系统编辑元数据合成 ASG。**

## 3. 数据地基

### 3.1 字段来源矩阵

可用数据源的定位如下：

- [AMASS](https://amass.is.tue.mpg.de/index.html)：统一不同 mocap 数据到 SMPL/参数化人体表示，适合作为 raw 3D motion source。
- [BABEL](https://babel.is.tue.mpg.de/)：给 AMASS mocap 加 sequence label 和 frame label；官方页面说明约 43 小时 AMASS motion、超过 28k sequence labels、63k frame labels、250+ action categories。
- [HumanML3D](https://github.com/EricGuo5513/HumanML3D)：从 HumanAct12 和 AMASS 构建的 motion-language 数据，包含 14,616 motions 和 44,970 descriptions，motion 被降采样到 20 fps、片段约 2-10 秒。
- [MotionFix](https://motionfix.is.tue.mpg.de/)：source motion、target motion、edit text 三元组，适合提供 text-driven edit 的监督和 baseline。
- PoseFix / PoseScript：静态 pose 或 pose-delta 的语言描述，可用于生成局部姿态编辑模板，但不能直接提供连续 section 边界或接触。

| ASG 维度                        | 直接来源                                                               | 脚本推导                                      | 用户 / 系统生成                       | v0 判断    |
| ----------------------------- | ------------------------------------------------------------------ | ----------------------------------------- | ------------------------------- | -------- |
| raw motion frames             | AMASS、HumanML3D、MotionFix source/target                            | 统一 skeleton、fps、坐标系                       | source id、版本号                   | 可靠       |
| frame range                   | BABEL start/end、HumanML3D clip range                               | 固定窗口、速度极小值、BABEL action segment 转帧        | DCC 手动 split                    | 可靠但需质控   |
| semantic label                | BABEL labels、HumanML3D captions、MotionFix edit text                | label normalize、action grouping           | 用户自定义 label                     | 可用但不作硬约束 |
| start/end pose                | raw motion 首尾帧                                                     | 全局 joint positions、6D rotations、SMPL pose | 无                               | 可靠       |
| root path / heading           | AMASS root translation / orientation、HumanML3D root representation | 坐标系 canonicalize、yaw 提取                   | root offset edit                | 可靠       |
| foot contact                  | 无可靠直接来源                                                            | foot height + velocity heuristic、置信度估计    | 主动人工校正                          | 只能半自动    |
| hand/prop contact             | 基本无                                                                | 无可靠推导                                     | 需用户 / 场景标注                      | v0 不做    |
| locked interior               | 无                                                                  | 根据 edit mask 自动生成                         | protected keyframes、locked mask | 协议字段     |
| boundary buffer               | 无                                                                  | 根据 fps 转为帧数                               | 用户调参                            | 协议字段     |
| cache key / dirty flag / undo | 无                                                                  | 无                                         | 系统生成                            | 工程字段     |

### 3.2 自动处理路径

`ShotGraph-Bench-v0` 应改名为 `ASG-Bench-v0`。自动处理流程：

1. 读取 AMASS / HumanML3D / MotionFix 的 motion frames，并统一到同一 skeleton、fps、root 坐标系。
2. 用 BABEL action segment 的 `start_t / end_t` 或固定窗口切出 2-5 个 animation sections。
3. 对每个 section 抽取 `frame_range`、`semantic_label`、`start/end pose`、`root_path`、`heading`。
4. 用 foot height + velocity 估计脚接触，并输出 confidence；低置信度或 QP 失败时进入主动人工校正。
5. 默认生成 `locked_interior_mask`：非编辑 section 全锁定，编辑 section 只释放 edit mask 和 boundary buffer。
6. 系统生成 `dirty flag`、`cache key`、`edit command log`。

这条路径能自动构造大部分 v0 数据，但必须承认：**contact state 不是可靠自动标签，prop state 在 v0 中不存在。**

## 4. 真实工作流与研究缺口

### 4.1 DCC 流程是否真的存在

这些概念不是凭空造的：

- Blender NLA Manual 中，Action Strip 播放 keyframe action，Transition Strip 在相邻 action strips 之间插值；strip 可有 blend in/out。
- Unreal Sequencer Animation Track 支持 Animation Sequence section、multiple track layers、section weight keyframe、overlapping sections 自动形成 blend curve、section range、play rate、start/end offsets。
- Maya Animation Layers 官方文档把 animation layers 分为 Additive 和 Override 两类，支持在不覆盖原 animation curves 的情况下叠加修改。
- Unity Timeline Animation Track 的属性包括 Track Offsets、Avatar Mask、Default Offset Match Fields，可用于 clip 起始位置/旋转偏移、身体部位 mask 和 clip gap matching。

所以“section、layer、mask、blend curve、offset、lock、play rate、undo”确实是动作编辑 / engine timeline 中真实存在的概念。上一版的问题是用了 `approved interior`、`release boundary` 这类过虚术语；新版应改成 DCC 能理解的语言。

### 4.2 旧术语替换

| 旧词                | 新词                                          | 为什么                                                  |
| ----------------- | ------------------------------------------- | ---------------------------------------------------- |
| shot              | animation section                           | 避免误解为电影镜头，直接对应 clip / strip / section                |
| approved interior | protected interior / locked mask            | DCC 中更接近 section lock、keyframe protect、avatar mask   |
| release boundary  | editable boundary buffer / blend window     | DCC 中实际是 blend curve、transition strip、overlap window |
| B affects C       | boundary state mismatch / dirty propagation | 用 root、heading、contact 状态定义依赖，而不是叙事因果泛化              |
| cache valid       | cache key + dirty flag                      | 工程上可实现，不能伪装成数据标注                                     |
| undo restore      | command log + state snapshot                | 编辑器机制，服务可复现实验                                        |

### 4.3 真正的研究缺口

如果只做 `clip + layer + linear blend + cache`，确实只是工程包装。StoryMotion-ASG 必须抓住以下不可替代点：

1. **依赖传播不是普通 DCC blending**：当某个 section 的 end root / heading / foot contact 改变，系统要判断哪些后续 edges 失配、哪些 interiors 仍可锁住。DCC 通常提供混合工具，但不自动给出生成式局部编辑后的最小重算范围。
2. **接触一致边界修复不是普通 inpainting**：CondMDI 可以补间，但不保证 protected interior 不漂移、不管理 undo/cache，也不把 foot contact 当硬约束。ASG 的边界 solver 要在短 buffer 内最小化平滑能量，同时尽量保持接触点世界坐标稳定。
3. **主动接触标注是可控成本的现实折中**：全自动 contact 不可信；全人工标注成本高。可研究的是：启发式先猜，优化失败或低置信度时只请求用户标注少量关键帧。
4. **DCC 可导出性是限制也是价值**：输出应能变成 FBX / animation sequence / blend curve / offset layer，而不是只生成一个不可编辑的 motion tensor。

因此，论文主张不能是“我们发明了动画时间线”，而应是：

> We formulate local revision of multi-section 3D animation assets as a DCC-compatible Animation Section Graph problem, and solve the hard part: minimal dirty propagation and contact-consistent boundary repair under protected interiors.

## 5. 总分结构

StoryMotion-ASG 的四个 Part 应重新定义如下。

### 5.1 Part I: Animation Section Data Compiler

目标：从现有 motion 数据和 DCC clip 切段中构造 ASG。

输入：

- AMASS / HumanML3D / BABEL / MotionFix motion frames；
- BABEL action segments 或固定 section split；
- 可选 DCC timeline 导出的 clip ranges。

输出：

- section nodes：frame range、source id、semantic label、start/end pose、root path、heading；
- edge states：相邻 section 的 root/heading/contact continuity requirements；
- protocol metadata：locked masks、boundary buffers、dirty flags、cache keys、edit log。

必须说明：`locked masks / boundary buffers / cache keys` 是 ASG compiler 生成的协议字段，不是数据集字段。

### 5.2 Part II: Edit-to-State and Dirty Propagation Compiler

目标：把一次局部编辑变成可验证的影响范围。

输入：

- keyframe edit：改某帧 root / joint；
- layer edit：叠加 additive 或 override layer；
- mask edit：只影响上半身、下半身、root 或局部关节；
- retiming edit：改变 section duration / play rate；
- optional text edit：来自 MotionFix 风格的 edit text。

输出：

- target constraints；
- protected interior mask；
- dirty sections / dirty edges；
- boundary states that must be repaired。

v0 不需要复杂图理论，但必须有确定性规则：

- 不改变 start/end state 的 interior edit，只 dirty 当前 section；
- 改变 end root / heading 的 edit，dirty 当前 section 的 outgoing edge；
- 改变接触状态的 edit，dirty 到下一个需要匹配 contact 的 edge；
- 被保护 interior 永不被 generator 改写，除非用户显式解锁。

### 5.3 Part III: Contact-Consistent Boundary Solver and 3D Conditioner

目标：只在 boundary buffer 里修复过渡。

第一版不要重新训练大 generator，优先做两个层次：

1. **Deterministic / optimization solver**：线性、Hermite、spline、QP 或投影优化，目标是 root/heading/velocity 平滑，并在有接触标注时保持 foot contact 世界坐标稳定。
2. **3D motion conditioner wrapper**：把 CondMDI / MotionLCM / MotionFix 类方法限制在 boundary buffer 或 edited mask 内，用 ASG contract 约束它不得修改 protected interior。

控制应拆成两层：

- **Trajectory / root control**：root path、heading、section duration、boundary alignment。
- **Local motion control**：joint pose delta、body-part mask、foot contact、upper/lower-body layer。

研究增量不在“又一个 diffusion backbone”，而在 **ASG contract + dirty propagation + contact-aware boundary repair**。

### 5.4 Part IV: Editing Contract Evaluator

目标：证明这不是普通 inpainting，也不是 DCC 工具复述。

核心指标：

| 指标 | 解释 |
|---|---|
| edit target error | 被编辑 keyframe / root / heading / duration 是否达成 |
| protected interior drift | locked interior 相对原 motion 的 MPJPE / rotation drift |
| boundary continuity | root jump、heading jump、velocity jump、transition jerk |
| foot contact violation | foot skating、floor penetration、contact point drift |
| dirty radius | 被标记为 dirty 或实际重算的 sections / frames |
| cache reuse | 未受影响 sections 的 cache 是否保持有效 |
| undo fidelity | undo 后 motion 和 metadata 是否恢复 |
| annotation cost | 接触主动标注的帧比例 |
| review scope | 用户需要重看的 section 范围 |

## 6. 第一版实验与删减

### 6.1 v0 实验

v0 定位：**ASG-Bench-v0: DCC-compatible local section editing with contact-aware boundary repair**。

数据：

- AMASS / BABEL：构造 3-5 section 的单人 motion sequences；
- HumanML3D：提供 clip-level text，可用于筛选和 caption，不依赖其做精细边界；
- MotionFix：提供 text edit baseline 和 edit templates；
- PoseFix / PoseScript：提供静态 pose delta 和局部姿态语言模板；
- 少量主动人工接触校正：只标脚接触，不标手 / 道具。

任务：

- `section.end_root` 偏移；
- `section.end_heading` 改变；
- `section.duration` retiming；
- upper-body additive layer edit；
- replacing one section with a similar section from the same action group。

Baseline：

- direct cut；
- linear blend / Hermite / spline；
- DCC-style overlap blend approximation；
- CondMDI boundary inpaint；
- MotionFix / TMED edit if available；
- StoryMotion-ASG without contact constraints；
- StoryMotion-ASG without dirty propagation。

必须实验：

1. **数据可得性实验**：统计每个 ASG 字段来自 direct / script / user-system 的比例，证明地基不虚。
2. **contact annotation ablation**：0%、heuristic-only、1%、3%、5%、10% 主动标注，测 foot skating 和 QP 成功率。
3. **boundary repair**：比较 cut、blend、CondMDI、ASG solver 的 boundary continuity 和 protected drift。
4. **dirty propagation**：随机编辑中间 section，测预测 dirty radius 与实际需要重算范围。
5. **multi-step edit stability**：连续 5-10 次 edit 后，locked interior drift、cache reuse、undo fidelity。

### 6.2 v1 / v2

v1 才做生产式 timeline prototype：

- Blender / Unreal 导入导出；
- layer / mask / blend curve UI；
- 小规模 animator review；
- section-level diff 和 review scope。

v2 才考虑结构化 story beat，但仍然是 **script beat -> animation sections**，不是手绘 storyboard，也不是完整影视镜头语言。

### 6.3 必须删除或降级的 claim

必须删除：

- 第一个 storyboard-conditioned 3D motion generator；
- 从真实手绘分镜到完整 3D animation；
- 全自动 contact / prop / 多人交互；
- 完整影视 / 游戏制作 pipeline；
- universal motion representation。

必须降级：

- `ShotGraph` 降级并改名为 `Animation Section Graph`；
- `contact state` 降级为启发式 + 主动人工校正；
- `prop state` 放到 future work；
- `SIGGRAPH claim` 降级为：只有当 v0 证明数据字段可得、contact-aware boundary repair 有显著信号，且 v1 有 DCC prototype / user review，才可能达到 SIGGRAPH/TOG 系统论文标准。

### 6.4 下一步

1. 写 ASG schema：严格区分 `data_fields`、`derived_fields`、`protocol_metadata`。
2. 用 BABEL `start_t / end_t` + AMASS motion 生成 100 条 3-5 section sequences。
3. 先跑字段可得性统计和 foot contact heuristic 质控，不急着训练 generator。
4. 做 deterministic boundary baselines：cut、linear、Hermite、spline、QP。
5. 接 CondMDI 只做 boundary buffer inpaint，验证它是否真的能替代 solver。
6. 若 foot contact heuristic 太不稳，立刻把论文主线改成 active contact annotation，而不是硬撑全自动。

## 7. 会话结论

本次重构的关键判断：

- 数据地基必须先于模型设计。`frame range / semantic label / start/end state / root path` 有较可靠来源；`contact state` 只能半自动；`locked interior / boundary buffer / cache key` 是编辑协议字段，不是数据字段。
- 产业落地不能用虚词。DCC 真实概念是 clip、section、track、layer、mask、blend curve、keyframe、offset、dirty flag、undo。
- StoryMotion 不能靠“中间片段替换”与 CondMDI 区分；必须靠 protected interior、dirty propagation、contact-consistent boundary repair、active contact annotation 和 DCC-compatible export 区分。
- v0 的首要目标不是漂亮 demo，而是证明 ASG 字段能自动/半自动构造，且 boundary repair 与 dirty propagation 有不可替代信号。
