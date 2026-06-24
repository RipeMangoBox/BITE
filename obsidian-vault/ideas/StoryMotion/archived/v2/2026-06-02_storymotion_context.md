---
title: StoryMotion Session Context
created: 2026-06-02T00:00:00+08:00
archived: 2026-06-03T20:05:17+08:00
status: archived
hypothesis: "结构化 multi-shot storyboard（shot列表 + blocking pose + 6DoF waypoint）→ 可编辑3D motion中间层，实现shot级局部重生成。PRISM/Kimodo/ActionPlan均无法做到shot-local preservation。"
tags:
  - StoryMotion
  - storyboard
  - motion_generation
  - previsualization
  - context
  - archived
---

# StoryMotion Session Context

> [!warning] Archived
> 这个文档压缩保留 2026-06-02 版本的旧叙事：`storyboard-conditioned 3D motion generation with editable spatial anchors`。当前 source of truth 已切换到 [[ideas/StoryMotion/2026-06-04_storymotion_cinematic_section_graph_plan|StoryMotion Cinematic Section Graph Plan]]。旧版中关于 4090 环境、已入库论文和早期 MVP 的信息可作为历史记录，但不再代表当前方案。

## 1. Idea 来源

详见父文档：`obsidian-vault/ideas/2026-06-01_motion-storyboard-previs-ideas.md`

三个方向：
- **Idea A (主线)**: StoryMotion — Storyboard-Conditioned Motion Generation for 3D Previsualization
- **Idea E (场景交互)**: AnchorMotion — Affordance Anchor-Driven Scene-Aware Motion Editing
- **Idea F (长程连续)**: MemoMotion — Memory-Anchored Cross-Shot Motion Continuity

当前聚焦 **Idea A (StoryMotion)**，MemoMotion 可作为其关键模块集成。

## 2. 命名：StoryMotion

**全称**: Storyboard-Conditioned 3D Motion Generation with Editable Spatial Anchors

### 为什么不是 Complex T2M 或 Motion In-betweening

| 维度   | Complex T2M | Motion In-betweening |                        StoryMotion                        |
| ---- | :---------: | :------------------: | :-------------------------------------------------------: |
| 输入   |   单段自然语言    |    关键帧 pose + 时间戳    | **结构化 shot 列表** [(text, start_pose, end_pose, waypoints)] |
| 空间锚点 |     隐式      |        无空间语义         |                   **显式 6DoF** waypoint                    |
| 输出   |  最终 motion  |      补间 motion       |                   motion + **可编辑中间表示**                    |
| 编辑   |  改文本→整段重生成  |      改关键帧→重新补间       |                 **改一个 anchor→只重生成该 shot**                 |
| 跨段状态 |     无保证     |         不适用          |        **显式 memory anchor** (root/heading/contact)        |

**核心定位**: StoryMotion 不是更好的 T2M，也不是更好的 inbetweening。它是第一个把**结构化 multi-shot storyboard** 编译为**可编辑 3D motion 中间表示**的框架，支持 **shot 级局部重生成**和**显式跨 shot 状态记忆**。

## 3. Shot 的定义与 Multi-Shot 组织

### Shot 数据结构

```text
Shot:
├── shot_id: int
├── text: str
├── start_pose: [J, 3] | None
├── end_pose: [J, 3]
├── root_waypoints: [(frame, x, z, θ)]
├── duration: int
└── camera_metadata: optional
```

### Multi-Shot 组织

```text
Storyboard:
  Shot 1: "walk to door"
    start_pose = standing @ origin
    end_pose = standing @ door
    waypoints = [(0,0,0,0°), (60,1.5,0,0°), (120,3,0,90°)]
  Shot 2: "open door and enter"
    start_pose = standing @ door
    end_pose = stepping through doorway
    waypoints = [(0,3,0,90°), (60,3.5,0,90°)]
  Shot 3: "look around room"
    start_pose = inside doorway
    end_pose = standing @ center
    waypoints = [(0,4,0,90°), (90,5,2,180°)]
```

关键约束:

- `Shot_N.end_pose ≈ Shot_{N+1}.start_pose`
- `Shot_N.root_waypoints[-1] ≈ Shot_{N+1}.root_waypoints[0]`

**与 PRISM/ActionPlan 的本质区别**: 它们是逐帧/逐段 autoregressive 滑窗，没有显式的 shot 边界和独立可编辑单元。StoryMotion 的 shot 是有**语义边界的、可独立操作的 conditioning block**。

## 4. Adversarial Survey 结果

对 StoryMotion 进行了系统性的 adversarial 调研（主动寻找撞车工作），结论：

### Novelty 评分

| Claim | 新颖度 | 判定 |
| --- | ---: | --- |
| Multi-shot storyboard 输入 (3D skeleton) | 4/5 | 视频域有 STAGE / FairyGen，3D skeleton 域无 |
| Shot-local 编辑 + 未编辑 shot 保持 bit-identical | 5/5 | PRISM 自回归链级联，Kimodo overlap blending |
| 显式跨 shot 状态记忆 (root/heading/contact) | 4/5 | PRISM 传隐式 latent，Kimodo 传 overlap keyframe |
| 持久化可编辑中间表示 | 5/5 | Kimodo 编辑输入而非中间表示；PRISM latent 不可人工编辑 |

### 最大威胁

| 威胁 | 风险 | 为什么不致命 |
| --- | --- | --- |
| **PRISM** (arXiv Mar 2026) | MEDIUM | 技术 DNA 最接近，但自回归链 = 编辑上游必级联下游 |
| **Kimodo** (NVIDIA Mar 2026) | MEDIUM | Keyframe+waypoint+timeline，但无 shot 结构、无 local preservation |
| **MMDM+KAA** (Mar 2026) | LOW | Masked in-betweening 支持局部重生成，但无 shot 结构 |

### Killer Demo

三 shot 序列 A→B→C。修改 shot B 的 end pose，重新生成 B。**A 和 C 保持 bit-identical。** PRISM（自回归级联）和 Kimodo（overlap blending）均无法做到。

## 5. Baseline 选型

### 明确拒绝

- **MDM** (ICLR 2023): 太老，用户明确拒绝

### 推荐 Backbone: MotionLCM (ECCV 2024)

- 已内置 spatial control (pelvis trajectory + initial pose)
- 实时推理 (30ms)，适合交互式编辑
- 在 ControlNet 框架上扩展 "initial pose" → "start+end pose" 改动量最小
- Python 3.10 匹配 4090 环境

### 候选 Backbone: CondMDI (SIGGRAPH 2024)

- 原生 keyframe + text inbetweening
- 需加 waypoint loss + shot 结构
- Python 3.7 需要新 conda 环境

### 不作为 MVP backbone 但参考价值

- **MotionBricks** (SIGGRAPH 2026): 无 text conditioning、无 trajectory/keyframe——本质是 WASD 实时 locomotion 控制器
- **Sketch2Anim** (SIGGRAPH 2025): 代码不完整，输入是 2D 草图而非结构化数据

## 6. MVP 设计（旧版，已被替换）

> [!warning] 注意
> 本节是旧方案。当前新方案见 [[ideas/StoryMotion/2026-06-04_storymotion_cinematic_section_graph_plan|StoryMotion Cinematic Section Graph Plan]]，第一版不再主张 storyboard-conditioned generation，而是 human-camera local editing contract。

```text
实验: Three-shot 解耦生成 + 局部编辑验证

数据构造:
  从 HumanML3D/BABEL 取连续动作 → 自动切分为 3 段 pseudo-shot
  每段提取: text, start_pose, end_pose, root_waypoints

编辑测试:
  修改 shot_B.end_pose 或 shot_B.waypoints
  只重新 gen(B | boundary_state_A) → motion_B'
  验证: motion_A == motion_A' (bit-identical)
```

## 7. 关键论文（旧版记录）

| Paper | Venue | Status |
| --- | --- | --- |
| CondMDI | SIGGRAPH 2024 | PDF + Analysis |
| MotionLCM | ECCV 2024 | PDF + Analysis |
| BAMM | ECCV 2024 | PDF + Analysis |
| PRISM | arXiv Mar 2026 | PDF + Analysis |
| ActionPlan | arXiv Mar 2026 | PDF + Analysis |
| Kimodo | Mar 2026 | PDF + Analysis |
| Sketch2Colab | arXiv 2026 | PDF + Analysis |
| STAGE | arXiv 2025 | PDF + Analysis |
| FairyGen | arXiv 2025 | PDF + Analysis |
| AnyAct | arXiv 2026 | PDF + Analysis |
| MMDM+KAA | arXiv 2026 | PDF + Analysis |
| Multi-level Diffusion | CVPR 2026 | PDF + Analysis |

## 8. 扩展方向（旧版记录）

### 8.1 AnchorMotion

StoryMotion 的场景交互扩展。为 shot 增加 3D object anchor（物体位置、朝向、可交互部位、功能类型如 `sit`/`grasp`/`place`），生成接触合理的 scene-object-aware motion。

### 8.2 MemoMotion

StoryMotion 的长程连续模块。在多 shot 生成中显式维护最小必要状态记忆（root position/velocity、heading、foot contact、可选 hand-object state），作为下一 shot 的条件注入。

## 9. 4090 环境状态（旧版记录）

| 组件 | 路径 | 状态 |
| --- | --- | --- |
| MotionLCM 代码 | `/data/public/ripemangobox/Motion/MotionLCM` | 已 clone |
| MotionLCM deps (glove/t2m/T5/SMPL) | 同上 | 已下载 |
| MotionLCM control checkpoint | 同上 `experiments_control/` | 已解压 |
| CondMDI 代码 | `/data/public/ripemangobox/Motion/CondMDI` | 已 clone |
| CondMDI checkpoint | 同上 `save/` | 已解压 |
| HumanML3D | `/data/public/ripemangobox/Motion/datasets/HumanML3D/HumanML3D` | 已下载 |
| GloVe | `/data/public/ripemangobox/Motion/EventT2M-codes/deps/glove` | 已下载 |
| SMPL | `/data/public/ripemangobox/Motion/datasets/body_models/smpl` | 已下载 |
| Conda env `event-t2m` | Python 3.10, PyTorch 2.2.2, CUDA 12.1 | 可用 |
| GPUs | 2x RTX 4090 (24GB each) | 可用 |

## 10. 旧版待办

- [ ] 用 MotionLCM spatial control 跑通单 shot inference
- [ ] 扩展为 start+end pose conditioning
- [ ] 构建 two-shot/three-shot pseudo-storyboard 数据集
- [ ] 实现解耦生成 + 局部编辑 MVP
- [ ] Baseline: 模拟 PRISM autoregressive 生成，对比编辑后前段保持率
- [x] 入库 Kimodo、Sketch2Colab、STAGE、FairyGen、AnyAct、MMDM+KAA、Multi-level Diffusion 等新论文
