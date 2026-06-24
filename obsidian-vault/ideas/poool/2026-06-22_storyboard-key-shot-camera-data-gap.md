---
title: "Storyboard Key-Shot Human Pose with Camera: Data Gap and Decomposed Route"
status: idea/zero-training-mvp-design
hypothesis: "公开数据目前不足以直接训练 <human pose, camera, atmosphere, storyboard style> 联合生成模型；scene 应定义为文本中的画面性场景描述，而非 HSI 物理场景。第一步应做零训练假设检验：显式 shot grammar 是否在相同 body pose 下显著提升 storyboard key-shot 构图一致性。"
source_papers:
  - "[[analysis/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation|Sketch2Anim]]"
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation|ShotVerse]]"
  - "[[analysis/arxiv_2026/CT_1_Camera_Trajectory_Generation_for_Camera_Controlled_Video_Generation|CT-1]]"
  - "[[analysis/arxiv_2026/SymphoMotion_4D_Dynamic_and_Camera_Control_for_Video_Generation|SymphoMotion]]"
  - "[[analysis/arxiv_2026/CamDirector_Camera_Trajectory_Control_for_Long_term_Video_Generation|CamDirector]]"
created: 2026-06-22T22:10:00+08:00
updated: 2026-06-22T23:09:43+08:00
tags:
  - motion_generation
  - storyboard
  - camera_control
  - data_gap
  - zero_training_mvp
  - idea/feasibility
---

# Storyboard Key-Shot Human Pose with Camera: Data Gap and Decomposed Route

> [!warning] Scope
> 本文不是实验结果，也不声称已提出可训练模型。核心结论是：**当前可核验的公开证据不足以支持直接训练“漫画/动画分镜关键帧 + 人体姿态 + 相机 + 氛围文本”的联合生成模型**。这里的 `scene` 指文本中的画面性场景描述和氛围描述，不是 HSI 的可交互三维场景。更现实的第一步是验证 `scene/action text → shot grammar → 3D pose projection` 这条分解是否带来可测收益。


> [!新想法]
>注意点：我说的scene不是HSI的scene，而是指文本描述中的场景描述，是一种画面性的描述，用于引导分镜的生成。
>核心问题：这个工作是个很接近从零到一的工作，你需要充分调研图像、视频领域的相关工作，把核心、可靠工作分析入库。
>核心MVP：需要斟酌MVP设计，快速可靠验证可行性，不要上来就事无巨细地安排每个阶段，可以先小规模验证。

## 2026-06-22 DeepSeek Max 修订

与 DeepSeek Max 严肃讨论后的结论：**这条线有从零到一潜力，但不应优先占用 4090，也不应先训练联合模型。** 当前最缺的不是网络结构，而是一个能让 reviewer 相信任务成立的最小证据：在相同人体姿态基础上，显式 shot grammar 是否真的改善 storyboard key-shot 的画面表达。

因此第一步不做完整 pipeline，而做零训练假设检验：

> 给定同一段 action / scene text 和同一组候选 body pose，加入 LLM 或人工生成的 shot grammar 后，投影出的 key-shot 是否比无 grammar 或随机 grammar 更符合分镜叙事？

### 零训练 MVP

1. **输入样本**：先收集 50-100 条文本画面描述，覆盖动作、情绪、氛围和镜头暗示，例如 `a tired swordsman kneels after losing, low angle, dramatic silence`。这些 `scene` 是画面描述，不要求真实 3D scene。
2. **shot grammar 生成**：用 LLM 或手工规则生成可解释 token：shot scale、angle、view facet、FOV bucket、composition、emotional intent。对比组必须包含 no grammar、random grammar、LLM grammar、少量人工 grammar。
3. **pose 来源**：先用 HumanML3D / OpenT2M 检索或从已有 T2M 结果抽关键帧，避免训练新 pose generator。若 body action 与文本不匹配，直接剔除样本，不把 pose retrieval 问题混进 camera hypothesis。
4. **投影与渲染**：用固定 skeleton / mannequin renderer，根据 shot grammar 设定 weak-perspective 或简单 pinhole camera。第一轮只评估骨架/人体框图构图，不引入强图像生成器，以免风格化质量掩盖 camera 效应。
5. **评估**：人工 5 分制评价叙事构图、人物在框、动作可读性、情绪/氛围一致性；同时记录 in-frame joint ratio、bbox scale、center offset、shot token consistency。

### 如何避免变成 demo

- 研究假设必须写清楚：**shot grammar 是必要中间变量**，不是为了做一个好看的 storyboard 页面。
- 必须有消融：no grammar、random grammar、LLM grammar、human grammar。没有 random grammar 对照时，任何好看结果都不能说明 grammar 有用。
- 人工评分要盲评，且样本要固定同一 body pose，尽量只改变 camera / composition。
- 若 LLM grammar 与 human grammar 差距很大，这反而是一个可写问题：`text scene → shot grammar` 需要学习或更强约束。

### 修订后的止损标准

- LLM grammar 相比 no grammar / random grammar 的人工评分提升低于 0.8 分（5 分制），且不显著，则停止，不进入训练。
- in-frame joint ratio、bbox scale、center offset 等客观构图指标不优于简单 camera heuristic，则 camera grammar 无研究价值。
- 如果输出质量主要取决于风格化模型 seed，而不是 shot grammar，停止图像化，退回 skeleton/mannequin panel。
- 如果核心文献入库后发现图像/视频领域已有公开 `text scene → shot grammar → human key-shot` 数据或模型覆盖该问题，则重写定位为 benchmark / data audit，而非新任务。

### 需要补充入库的可靠相关工作

当前 note 已有 Sketch2Anim、Pulp Motion、ShotVerse、CT-1、SymphoMotion、CamDirector。下一轮如果推进项目 2，应优先把图像/视频 storyboard、cinematic shot planning、text-to-camera、controllable character pose 这些工作入库，再判断是否真的存在未覆盖 gap。未入库前，不应声称该方向已经构成完整方法论文。

## 原始想法

目标是生成漫画、动画或 AI 漫剧制作流程里的关键分镜动作。输入有两类：

- `human text + camera text`：分别描述人物动作和镜头。
- 画面描述：包括人物、场景、气氛、情绪，模型自行判断 camera。

输出不是完整动作序列，而是符合 camera 约束的一帧人物动作关键帧。预期上，人物姿态要比普通 text-to-motion 更匹配氛围，相机投影进一步服务叙事和情绪。

这个想法最吸引人的地方是**关键帧单帧化**：相比生成整段 motion，它更接近 storyboard 和 key animation。但最大问题也是数据：我们需要含有人体姿态、相机、画面氛围描述的配对样本。

## Evidence Layer

### 直接相关但不完整的证据

- [[analysis/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation|Sketch2Anim]] 是最贴近 storyboard 的强证据。它从 2D 草图关键姿态、关节轨迹和动作词生成 3D animation，并通过“3D 替身训练 + 2D-3D embedding 对齐”绕过草图到 3D 的病态提升问题。它证明 storyboard/sketch 条件可作为动作控制接口，但不包含相机语法、氛围文本或漫画镜头构图的联合标注。
- [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]] 证明 human motion 与 camera trajectory 的联合生成需要屏幕构图约束。它将人体和相机潜变量映射到 framing latent，并用辅助采样降低出画率。它非常支持“人-相机不能独立生成”的判断，但输出是运动和相机序列，不是漫画/动画单帧关键姿态。

### Camera/cinematic 证据：能支持相机规划，但不能替代 human-keyshot 数据

- [[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation|ShotVerse]] 构建 `(Caption, Trajectory, Video)` 三元组，并把相机生成拆成 `P(Trajectory | Caption)` 和 `P(Video | Caption, Trajectory)`。这是强 camera/cinematic 数据证据。GitHub `Songlin1998/ShotVerse` 约 102 stars，2026-03-13 有 push，但无 license；适合作为 camera planning 参考，不适合作为 human pose 数据基础。
- [[analysis/arxiv_2026/CT_1_Camera_Trajectory_Generation_for_Camera_Controlled_Video_Generation|CT-1]] 从参考图像和 camera text 生成 SE(3) 轨迹，CameraBench100 平均成功率 81.6%。GitHub `gulucaptain/Camera-Transformer-1` 约 308 stars，但当前 API 看到仓库内容偏 README/coming soon，license 缺失，复现风险较高。它支持“从画面/文本自动推 camera”这个子问题。
- [[analysis/arxiv_2026/SymphoMotion_4D_Dynamic_and_Camera_Control_for_Video_Generation|SymphoMotion]] 提供相机和 3D 物体轨迹联合控制证据，说明 2D 轨迹无法区分相机视差和真实物体运动，需要 3D 感知控制。但它的对象是物体，不是人体关键姿态。
- [[analysis/arxiv_2026/CamDirector_Camera_Trajectory_Control_for_Long_term_Video_Generation|CamDirector]] 支持长视频相机轨迹编辑和世界缓存，但偏视频重渲染，不解决 storyboard pose 数据。

### 弱证据或趋势线索

- [[analysis/CGF_2024/Cinematographic_Camera_Diffusion_Model|Cinematographic Camera Diffusion Model]] 可作为相机控制趋势引用，但本地笔记显示元数据和基线细节不足，不应作为核心证据。
- ShotVerse、CT-1、CamDirector 等可以证明 camera control 是热点，但不能证明“漫画关键帧人体姿态 + camera + atmosphere”数据存在。

## Data Gap

当前缺的是以下联合样本：

$$
(\text{human pose or 3D body},\ \text{camera extrinsics/intrinsics or shot type},\ \text{scene/atmosphere/emotion text},\ \text{storyboard/comic/anime visual style})
$$

可用数据分布是割裂的：

- **Sketch/storyboard → 3D motion**：Sketch2Anim 有 2D keypose/trajectory 与 3D motion 条件路线，但 camera 不在主任务里。
- **text/caption → camera trajectory/video**：ShotVerse/CT-1 有 camera 规划和视频生成证据，但 human pose 不是结构化输出。
- **human motion + camera/framing**：Pulp Motion 有 human-camera-framing，但不是漫画 key-shot，也不是单帧叙事姿态。
- **comic/anime 图像**：可能有图像和文本，但难以取得可靠 3D camera 和 3D pose 标注。

因此，直接训练一个端到端模型会遇到两个硬问题：第一，配对数据不存在或质量不可控；第二，漫画单帧中的 camera 本身可能只是透视/构图风格，不一定可唯一反演为 SE(3)。

## Reframed Research Question

不应问：

> 能否直接从画面描述生成漫画分镜人体动作和相机？

应改成：

> 在缺乏联合数据的前提下，能否把 storyboard key-shot generation 分解为可验证的三个子问题：人体关键姿态生成、shot/camera grammar 选择、投影构图与风格化？

## Proposed Decomposed Route

### Stage 1: Text or scene description to 3D human keypose

输入人类动作描述和情绪词，输出一帧或少量候选 3D pose。该阶段可以复用 text-to-motion 的单帧采样、keyframe bottleneck 或 retrieval。

Baseline:

- T2M generator 中采样完整 motion，再抽取关键帧。
- Sketch2Anim-style keypose control，如果输入来自草图。
- HumanML3D retrieval：从已有动作库取最匹配帧。

最低指标：

- pose-text retrieval score。
- action recognizability。
- pose diversity。
- joint limit / contact plausibility。

### Stage 2: Description to shot/camera grammar

不要一开始生成连续 SE(3)，先预测可解释 shot tokens：

- shot scale: close-up, medium, full body。
- angle: low angle, eye-level, high angle。
- view facet: front, profile, back, three-quarter。
- lens/FOV bucket。
- composition: centered, rule-of-thirds, silhouette, over-shoulder。
- emotional intent: pressure, loneliness, reveal, impact。

这些 tokens 可从 ShotVerse/CT-1/Pulp Motion 的相机知识中抽象，而不是直接复制它们的连续轨迹模型。

最低指标：

- shot-token classification accuracy on curated data。
- consistency between prompt emotion and selected shot。
- in-frame joint ratio after projection。
- body scale and bbox center stability。

### Stage 3: Project 3D pose under camera, then stylize

将 3D pose 按 shot grammar 解码为 camera 或 weak-perspective projection，再生成 2D storyboard image。若目标是研究 motion/camera，不必一开始训练图像生成器；可以先渲染 skeleton/mannequin panel。

最低可行 demo：

- 输入：`a tired swordsman kneels after losing, low angle, dramatic silence`。
- 输出：3D pose + camera projection + rendered key panel。
- 验证：人物是否在画面内，姿态是否表达动作/情绪，shot 是否匹配描述。

## Possible Data Construction

### Safer route: synthetic but controllable

1. 从 motion 数据集抽取语义关键帧。
2. 用可控 camera grammar 渲染多视角 skeleton / mannequin。
3. 用模板或 VLM 生成 scene/atmosphere captions。
4. 人工审核一小部分作为 validation/test。

优点：可控、可复现、有 3D ground truth。  
缺点：风格不是漫画，氛围表达弱，可能更像 camera-aware pose generation。

### Riskier route: video-derived weak labels

1. 从电影/动画视频抽关键帧。
2. 用 pose estimator 获取 2D/3D pose。
3. 用 camera estimation 或 shot classifier 获取 camera/shot labels。
4. 用 VLM 生成 atmosphere captions。

优点：更接近视觉分镜。  
缺点：噪声大，版权/许可复杂，camera 标注不可靠，难以复现。

### Not recommended initially: web comic scraping

漫画图像的相机参数和 3D pose 都高度不可辨识，且版权和可复现性风险很高。除非目标变成纯 2D pose/style，不建议作为第一阶段数据源。

## Baselines

- **Sketch2Anim**：storyboard/sketch 到 3D animation 的核心 baseline。若任务含草图输入，必须对比。
- **Pulp Motion**：human-camera framing baseline。若任务含人体和相机构图，必须评估出画率和 framing。
- **ShotVerse/CT-1**：camera/shot planning baseline。只用于 camera 子模块，不用于人姿态生成。
- **T2M keyframe retrieval**：从完整动作生成或检索关键帧，是单帧 pose 的强简单 baseline。

## Kill Criteria

- 若无法构建至少 1k 条干净 `(pose, shot token, text)` 样本，则不应训练模型。
- 若 shot grammar 投影后的 in-frame joint ratio 低于 Pulp Motion 或简单 camera heuristic，则 camera 模块没有价值。
- 若完整 motion 抽帧 baseline 在 action recognizability 上优于直接 key-shot 模型，则单帧生成路线不成立。
- 若 VLM 自动氛围标签与人工标签一致性低，atmosphere 分支应移除，避免伪多模态。

## What Not To Claim

- 不要声称“解决漫画/动画分镜生成”。目前只能说“提出数据缺口分析与分解路线”。
- 不要声称“存在开源匹配数据集”。当前证据只支持相关子数据存在。
- 不要声称“camera 自动判断已可靠”。CT-1/ShotVerse 是视频 camera 证据，不是人体分镜姿态证据。

## Limitations and Risks

> [!note] Non-experimental status
> 本 note 不含模型训练或实验验证。所有路线判断来自本地 KB 与 web 增强检索的证据归纳。两阶段/三阶段分解只是降低数据需求的设计建议，尚不能视为有效方法。

- 最大风险是联合数据不存在，导致研究退化为数据工程。
- 第二大风险是 camera 与 emotion 的映射主观性强，评估难。
- 如果只生成 skeleton panel，贡献会被认为偏工具；如果生成漫画图像，又会被图像生成模型质量主导。
- 最合适的第一步不是发方法论文，而是做一个 small benchmark：`text + shot grammar → 3D keypose projection`。

## Suggested Claim

> 现有公开数据和方法已经分别覆盖 storyboard-to-motion、camera trajectory planning、human-camera framing，但尚未形成 `<human pose, camera, atmosphere, storyboard style>` 的可靠联合证据。该方向若要成立，应先做可复现的数据与任务分解，而不是直接宣称端到端 storyboard key-shot generation。
