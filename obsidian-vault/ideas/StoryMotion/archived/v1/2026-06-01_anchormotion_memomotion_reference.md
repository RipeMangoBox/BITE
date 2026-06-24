---
title: "AnchorMotion & MemoMotion — Reference"
created: 2026-06-01T14:05:11+08:00
updated: 2026-06-02T00:00:00+08:00
status: reference
source: "Extracted from obsidian-vault/ideas/archived/StoryMotion_v1/2026-06-01_motion-storyboard-previs-ideas.md §4.2-4.3"
tags:
  - Motion_Generation
  - research_idea
  - scene_aware_motion
  - motion_continuity
  - reference
---

# AnchorMotion & MemoMotion Reference

> [!abstract]
> 从 2026-06-01 脑暴文档中提取的两个扩展方向。StoryMotion 为主线（见 `2026-06-02_storymotion_context.md`），AnchorMotion 为场景交互分支，MemoMotion 为长程连续模块。两者均非当前 MVP 范围，保留为后续扩展参考。

## Idea B: AnchorMotion — Affordance Anchor-Driven Scene-Aware Motion Editing

**全称**: AnchorMotion: Affordance Anchor-Driven Scene-Aware Motion Editing

**一句话定义**：把 storyboard 中的物体交互转成 affordance anchors，生成可编辑的 scene-object-aware 3D motion previs。

### Problem Definition

输入：
- 单个 shot 的动作文本；
- 3D object anchor：物体位置、朝向、可交互部位、功能类型；
- 可选 root waypoint 和 start pose。

输出：
- 角色 motion；
- 接触时刻和接触部位；
- 当物体移动时，局部调整 motion。

这不是完整 HOI 终局生成，而是 previs 阶段的可编辑 motion blocking。

### Difference from Competitors

- 相对 UniHM：从"文本 + 场景点云"转向"storyboard + object affordance anchor"，强调创作者可编辑。
- 相对 Sitcom-Crafter：物体关系由用户/分镜显式指定，不交给 LLM 自由决定。
- 相对 GRAB / BEHAVE 类 HOI：不只复现单物体交互，而是把交互 anchor 接到 storyboard previs 接口。
- 相对 Sketch2Anim：从 sketch pose/trajectory 扩展到可移动物体 anchor。

### Method Core

- **Affordance Anchor Embedding**：把物体交互点表示为连续 6DoF anchor，加功能类型，如 `sit`、`grasp`、`place`、`lean`。
- **Contact-Aware Generator**：生成时显式约束手/脚/骨盆与 anchor 的距离和时序接触状态。
- **Per-Joint Local Editing**：借鉴 PRISM 的关节分解思想，物体移动时优先重生成 root、spine、arm 等受影响 token，而不是整段重采样。

### Minimum Experiment

先不做完整室内场景，只做 **single-object single-shot affordance control**：

- 数据：GRAB / BEHAVE / HIMO / CHAIRS 中 pick、place、sit、touch 等简单交互。
- 任务：给定 object anchor 和文本，生成接触合理的短 motion。
- Baseline：只给文本；给文本 + root target；UniHM-style waypoint without contact anchor。
- 指标：contact distance、penetration / collision proxy、root-target error、MPJPE、物体移动后的局部编辑成功率。
- 成功标准：物体位置变化后，接触误差明显低于纯文本和 root-only baseline，且不需要整段重采样才能适配。

### Biggest Risk and Scope Cut

- 风险：真实物体交互太难，接触/穿模指标容易不稳定。砍法：第一版只做单手触碰或拿取。
- 风险：scene mesh / object annotation 成本高。砍法：只用 object anchor，不用完整 mesh。
- 风险：与 UniHM 重叠。砍法：强调 `editable affordance anchor for previs`。

**保留判断**：作为 StoryMotion 的场景交互扩展保留。单独成主线风险较高，但能显著提高 idea 的工业 previs 价值。

---

## Idea C: MemoMotion — Memory-Anchored Cross-Shot Motion Continuity

**全称**: MemoMotion: Memory-Anchored Cross-Shot Motion Continuity

**一句话定义**：为多段 motion generation 显式维护最小必要状态记忆，让下一段生成继承上一段的 root、heading、foot contact 和可选 hand-object state。

### Problem Definition

长动作或多 shot 生成中的核心失败不是"不能继续生成"，而是段落边界状态断裂：
- root 位置/朝向突然跳；
- 脚触地状态不连续，引起滑步；
- 手持物或接触对象状态丢失；
- 上一段末尾姿态没有以可控方式进入下一段。

目标是在不引入视频或相机的前提下，定义 motion 专用的 memory anchor，作为下一段生成条件。

### Difference from Competitors

- 相对 STAGE：借鉴 memory pack 思想，但 memory 内容从像素实体一致性改为 3D motion state consistency。
- 相对 PRISM：PRISM 用 causal VAE 和 self-forcing 抑制长序列漂移，但关键状态主要隐式存在 latent 中；这里显式定义 root/contact/object memory。
- 相对 ActionPlan：ActionPlan 有逐帧语义 plan 和 latent-specific timestep，但没有专门建模段间物理状态。
- 相对 FlowMDM / PriorMDM：它们更像片段 composition / blending，这里强调"最小必要状态"作为可解释条件。
- 相对 UniHM：waypoint 可指定空间目标，但不等于跨段状态记忆，尤其不处理接触状态。

### Method Core

- **Memory Anchor Encoder**：从上一段末尾 K 帧提取 root position、root velocity、heading、foot contact、可选 hand-object state，编码为固定维度 anchor。
- **Anchor-Conditioned Generation**：下一段生成时将 anchor 作为 cross-attention / FiLM 条件注入扩散或 flow 模型。
- **Boundary Loss**：只在下一段前若干帧施加 root continuity、heading continuity、foot contact consistency，避免整个片段被锚点过度束缚。
- **Optional Memory Bank**：多 shot 时保存最近几个 anchor；第一版只用 last anchor。

### Minimum Experiment

做 **two-segment continuation**，不直接挑战无限长：

- 数据：HumanML3D / BABEL 中切分长 motion，前段 A 给真实 motion，后段 B 给文本或动作标签。
- Baseline：纯文本生成后 root 对齐；简单插值/平滑；ActionPlan / PRISM 风格 continuation；FlowMDM/PriorMDM composition。
- Ours：root + heading anchor，增强版加 foot contact anchor。
- 指标：boundary root error、heading error、first-second foot slip ratio、transition jerk、用户偏好。
- 成功标准：root 对齐 baseline 不能解决 foot slip / jerk，而 anchor 模型能显著降低边界 artifact。

### Biggest Risk and Scope Cut

- 风险：简单 root 对齐 + 平滑就能解决大部分问题，导致方法显得过度设计。砍法：必须把 foot contact / heading / transition jerk 作为核心指标。
- 风险：contact 标签噪声高。砍法：第一版只用 root + heading anchor。
- 风险：多段误差累积。砍法：限制为两段或三段 continuation，先证明 memory anchor 的局部价值。

**保留判断**：更适合作为 StoryMotion 的关键模块，而不是独立主线。若实验证明它比 root 对齐 + smoothing 强，再独立扩展。

---

## 相关文件

- `[[2026-06-02_storymotion_context]]` — StoryMotion 主线 context
- `[[../archive/2026-06-01_motion-storyboard-previs-ideas]]` — 原始脑暴文档（已归档）
- `obsidian-vault/ideas/2026-06-01_motion-storyboard-previs-ideas.md` — 原文档完整版本
