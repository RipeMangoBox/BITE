---
title: Unified Human-Camera Motion Token Framework
created: 2026-06-05T10:00:00+08:00
updated: 2026-06-10T18:42:06+08:00
status: proposal
hypothesis: 将 human motion 与 camera motion 统一为离散 token 序列，以文本为 condition，通过 mask-then-predict 范式实现统一的生成与 token-level 编辑——目前无人占据 (Human=Y, Camera=Y, Discrete-Token=Y, Masked-Edit=Y) 的四维交叉点。
tags:
  - StoryMotion
  - human_camera_motion
  - unified_token_framework
  - motion_generation
  - motion_editing
  - masked_modeling
source_notes:
  - "[[ideas/StoryMotion/2026-06-04_storymotion_cinematic_section_graph_plan|StoryMotion CSG Plan]]"
  - "[[ideas/StoryMotion/2026-06-05_camera-shot-edit|CameraShotEdit Proposal]]"
  - "[[ideas/camera/2026-06-05_camera-movement-generation-system-survey-llm-audit-merged|Camera Movement Survey]]"
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/ECCV_2024/E.T._the_Exceptional_Trajectories_Text-to-camera-trajectory_generation_with_character_awareness|E.T. / DIRECTOR]]"
  - "[[analysis/ICCV_2025/GenDoP_Auto-regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP / DataDoP]]"
  - "[[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes|AdaViewPlanner]]"
  - "[[analysis/SIGGRAPH_Asia_2024/MotionFix_Text-Driven_3D_Human_Motion_Editing|MotionFix]]"
  - "[[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text-Driven_Multi-Shot_Video_Creation|ShotVerse]]"
  - "[[analysis/ICML_2024/HumanTOMATO_Text-Aligned_Whole-Body_Motion_Generation|HumanTOMATO]]"
  - "[[analysis/ICLR_2026/Beyond_Text-to-Image_Liberating_Generation_with_a_Unified_Discrete_Diffusion_Model|Muddit]]"
  - "[[analysis/CVPR_2025/AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transformers|AC3D]]"
  - ShotVerse_Advancing_Cinematic_Camera_Control_for_Text-Driven_Multi-Shot_Video_Creation
---
[[ShotVerse_Advancing_Cinematic_Camera_Control_for_Text-Driven_Multi-Shot_Video_Creation]]
# Unified Human-Camera Motion Token Framework

> [!abstract] 一句话
> 将 human motion tokens 与 camera motion tokens 放入同一个离散词汇表，文本作为 condition，通过 bidirectional mask-then-predict 实现 human-camera 的统一生成与 token-level 编辑。

---

## Q1: 核心想法是什么？

**灵感来源：** [[analysis/ICLR_2026/Beyond_Text-to-Image_Liberating_Generation_with_a_Unified_Discrete_Diffusion_Model|Muddit]] (ICLR 2026) 提出将 text tokens 与 image tokens 拼接为统一序列，通过控制 mask 位置实现 T2I / I2T / VQA 三模式切换。本方案将这一范式从 text+image 迁移到 human+camera——将 human motion tokens 与 camera motion tokens 放入同一个离散词汇表，文本作为 condition，通过 mask-then-predict 实现统一生成与编辑。

**关键区别：** Muddit 使用离散扩散（mask-and-replace with diffusion schedule），我们考虑两种方案——BERT-style bidirectional mask-predict（训练效率更高，编辑场景双向上文更自然）或 discrete diffusion（生成多样性可能更好）。v0 用 BERT-style，若生成多样性不足则切换到 discrete diffusion。

将 human motion 和 camera motion 统一到同一个离散 token 空间。两组 VQ-VAE 分别将 SMPL-X 姿态参数和 SE(3) 相机轨迹离散化为 token，共享一个统一的 Transformer 词汇表。训练时随机 mask token span，推理时通过控制 mask 位置决定生成目标。

**Generation（三模式）：**

```
<text, human> + <masked camera>       → 预测 camera motion
<text, camera> + <masked human>       → 预测 human motion（全新方向）
<text> + <masked human, masked camera> → 联合生成 human + camera
```

**Edit（token-level）：**

```
<text, human, camera> + <edit_instruction_token> 
→ Edit Locator 定位需修改的 token span → Masked Regeneration → edited human + camera
```

编辑可以是"让走路变跑步"（改 human velocity tokens）或"推近镜头"（改 camera FOV tokens）。**3D camera motion 的 token-level editing 完全空白——Vid-CamEdit 仅在 pixel 层面编辑相机，不涉及 3D trajectory token。**

---

## Q2: 有研究这么做吗？精准的 gap 在哪？

**用 4 个维度交叉定位：**

| 工作                       | Human |   Camera    | 离散 Token |                Masked/Edit                |
| ------------------------ | :---: | :---------: | :------: | :---------------------------------------: |
| Pulp Motion (ICLR 2026)  |   Y   |      Y      | N（连续扩散）  |                     N                     |
| TSA (CVPR 2026)          |   Y   |      Y      | N（连续扩散）  |                     N                     |
| MotionGPT (NeurIPS 2023) |   Y   |      N      |    Y     |           部分（仅 generation 多任务）            |
| GenDoP (ICCV 2025)       |   N   |      Y      |    Y     |                     N                     |
| MoMask (CVPR 2024)       |   Y   |      N      |    Y     | 部分（masked prediction for generation only） |
| MotionFix (SIGAsia 2024) |   Y   |      N      | N（连续扩散）  |            Y（human edit only）             |
| Vid-CamEdit (AAAI 2026)  |   N   | Y（pixel 层面） |    N     |        Y（pixel-level camera edit）         |
| **本提案**                  | **Y** |    **Y**    |  **Y**   |    **Y（token-level edit across both）**    |

**无人占据 (Y, Y, Y, Y) 的格子。**

三条已完成的技术路线各自为政：
- **路线 A（joint generation）：** Pulp Motion、TSA 使用连续扩散，不做离散 token，不做 edit
- **路线 B（discrete tokens）：** MotionGPT 做 human、GenDoP 做 camera，但从未有人将两者放入同一个 vocabulary
- **路线 C（editing）：** MotionFix 做 human edit、Vid-CamEdit 做 pixel-level camera edit，但没有 3D token-level camera edit

**为什么之前没人做：**
1. 同时包含 human + camera + text 的数据集极少（PulpMotion 和 TSA 自建数据是罕见例外）
2. ==两个社区各自为政——human motion 沿着 MotionGPT/MoMask 的离散 token 路线，camera trajectory 沿着 E.T./GenDoP 的连续扩散路线，从未交汇==
3. 表示空间不同：SMPL 关节旋转（root-relative）vs SE(3) 世界位姿，tokenization 需要精心设计

---

## Q3: camera motion 按 human motion 的 token 化范式处理是否可行？

**可行，已有技术基础。**

### 3.1 表示空间差异

| 维度              | Human Motion                                | Camera Motion                    |
| --------------- | ------------------------------------------- | -------------------------------- |
| 自由度             | ~150 DoF (SMPL-X 关节 + root)                 | 7-9 DoF (SE(3) extrinsics + FOV) |
| 约束类型            | 骨骼长度、关节限位、足部接触                              | 平滑性、look-at 方向、画面构图              |
| 已有 tokenization | VQ-VAE over SMPL (MotionGPT)、残差 VQ (MoMask) | 自回归 trajectory tokens (GenDoP)   |
| 序列长度            | 60-200 frames                               | 相近帧数，变化更慢                        |

### 3.2 推荐的 token 化方案

**双 VQ-VAE + shared Transformer：**
- **Human VQ-VAE：** SMPL-X pose params → discrete tokens（沿用 MotionGPT 的 "motion as foreign language" 范式，或 MoMask 的残差 VQ 多尺度方案）
- **Camera VQ-VAE：** 6-DoF extrinsics + FOV → discrete tokens（沿用 GenDoP 的轨迹 tokenization，256-bin 整型量化）
- **Unified vocabulary：** 两组 VQ-VAE 的 codebook 合并为共享词汇表，加上 text tokens（frozen T5 encoder 输出）、特殊 tokens（`<HUMAN>`、`<CAMERA>`、`<MASK>`、`<EDIT>`）
- **Transformer backbone：** BERT-style bidirectional Transformer（~150M params），对拼接后的 token 序列做 masked prediction

**为什么选 bidirectional 而非 autoregressive：**
- Mask-then-predict 天然支持任意位置的生成和编辑（自回归只能从左到右）
- BERT 的双向上下文对 edit 场景至关重要——模型需要同时看到被编辑 token 的左右上下文
- MoMask 已验证 masked transformer 在 motion generation 上的有效性

#TODO : token预测的顺序，虽然不是自回归，但可以参考[[analysis/ICML_2024/HumanTOMATO_Text-Aligned_Whole-Body_Motion_Generation|HumanTOMATO]]设计交错的token预测，并添加其他手段，目的是严格的时间对齐

> **解答：按帧交错排列 token 序列。** 与 HumanTOMATO 的模态交错（body→hand 分层生成）不同，我们采用**时序交错**：`[H_t0, C_t0, H_t1, C_t1, ...]` 而非 `[H_all, C_all]`。同一帧的 human/camera token 位置相邻，Transformer local attention 自然捕获帧级对齐。辅助手段：(1) shared temporal position encoding 强化时间对应；(2) temporal alignment loss——同帧 H_i 与 C_i 的 hidden states 做对比 loss；(3) frame-level masking——训练时以帧为单位同时 mask H_tk 和 C_tk，迫使模型利用上下文恢复被遮挡帧的联合运动。

### 3.3 现有证据

Pulp Motion 证明了 human 和 camera latent 可以在 screen-space framing 层面有效对齐。GenDoP 证明了 camera trajectory 可以做离散 token 自回归生成。MotionGPT 证明了 "motion as foreign language" 范式可行。三者结合 = unified token 框架的技术组件已全部就绪。

AC3D 是较弱但有用的 camera-control 参考：它不做 human-camera tokenization，也不证明统一离散词表可行；它提供的启发是 camera motion 在视频扩散中更像低频控制信号，且条件注入需要限定时间步和层范围，避免全程全层控制损害视觉质量。迁移到本框架时，应把它作为 camera-token decoder / conditional Transformer 的设计 caution：camera condition 或 camera edit instruction 不一定应该影响所有 token 层，后续可比较 all-layer conditioning 与 camera-token-specific / early-layer conditioning。

---

## Q4: 六种 masking scheme 如何设计？

#TODO text作为通用condition（数据集是否支持？尽量不要自建），进一步思考，text应该如何提供？在不同模式时，只描述对应的unmask content（如只描述human或camera），还是默认同时描述human和camera？

> **解答：渐进式策略。v0 用"描述 unmasked content"，与现有数据集兼容。**
> 
> **数据集现状：** HumanML3D (14.6K) text 仅描述人体动作；DataDoP (29K) text 仅描述 camera 运镜；PulpMotion (193K) text 同时描述 human + camera。仅 PulpMotion 支持策略 B（同时描述两者），但 193K 规模足够 v0 联合微调。
> 
> **三阶段训练中的 text 策略：**
> - Phase 1（单模态预训练）：策略 A——text 仅描述 unmasked modality。`<TEXT> "a person walking" <HUMAN> [h_tokens] <CAMERA> [MASK]`
> - Phase 2（联合微调）：策略 B——PulpMotion 的 text 同时描述两者。`<TEXT> "a tracking shot following a running person" <HUMAN> [h_tokens] <CAMERA> [c_tokens]`
> - Phase 3（合成增强）：对 HumanML3D 的 human motion 用 LLM 合成 camera 描述（"如果以中景跟拍，camera 如何运动？"）；对 DataDoP 合成 human 描述。不建数据集，建 prompt template。
> 
> **混合 batch 格式统一：** 缺失模态侧填 `[MASK]`，text 描述对应存在的模态。

| 模式                | Mask 位置                                  | 预测目标                            | 是否已有工作覆盖                             |
| ----------------- | ---------------------------------------- | ------------------------------- | ------------------------------------ |
| Camera-from-human | `camera_tokens` 全部 mask                  | camera trajectory               | E.T.、AVP（连续空间，非 token）               |
| Human-from-camera | `human_tokens` 全部 mask                   | human motion                    | **全新。可能 ill-posed**                  |
| Joint generation  | `human_tokens` + `camera_tokens` 全部 mask | human + camera                  | Pulp Motion、TSA（连续空间）                |
| Human editing     | 编辑指令定位的 `human_tokens` span mask         | 该 span 的新 human tokens          | MotionFix（连续空间，非 token）              |
| Camera editing    | 编辑指令定位的 `camera_tokens` span mask        | 该 span 的新 camera tokens         | **全新。3D token-level camera edit 空白** |
| Joint editing     | 编辑指令定位的 mixed span mask                  | 该 span 的新 human + camera tokens | **全新**                               |

**Human-from-camera 的 ill-posed 问题：** 同一个 camera 轨迹可以对应无限多种 human motion（例如 static wide shot 可以拍走路、跑步、站立）。需要额外的 human motion prior 约束，或者在训练时要求 text condition 提供足够的歧义消除信息。

---

## Q5: camera 渲染视图是否参与训练？监督信号从哪来？

### 5.1 现有工作监督方式

#TODO 进一步思考视图的作用，能解决无视图的什么问题，以及效果是否显著？有哪些弊端需要进一步解决？

> **解答：视图解决三个核心问题，Pulp Motion 已验证效果显著，但有四个弊端需处理。**
> 
> **视图解决的核心问题：**
> 1. **3D 连续 ≠ 屏幕连续。** human 和 camera 各自在 3D 空间平滑，投影后仍可能出现 bbox 跳变、headroom 突变、主体出画。视图是唯一的 screen-space ground truth。
> 2. **弱监督对齐信号。** unpaired 数据上，投影后 human 在画面中的位置/大小是否合理 → 隐式的 human-camera plausibility 信号。可支撑 cycle consistency。
> 3. **可量化的构图指标。** 无视图只能评 ATE（3D trajectory），有视图可评 FD_framing、out-of-frame rate、subject scale consistency。
> 
> **效果显著性（Pulp Motion 证据）：** auxiliary sampling 的 2D 正交投影将 FD_framing 从 4.90→3.37，Out-rate 从 25.98%→16.76%。edit 场景需重新验证（edit 前后帧数不变，视图变化可能更 subtle）。
> 
> **四个弊端：**
> 1. **正交投影 ≠ 真实相机。** 忽略透视畸变、景深。Pulp Motion 的 framing loss 仅在正交投影下有效。v0 可接受此近似。
> 2. **约束冲突。** 视图约束（保持构图）与 3D 约束（接触连续）可能冲突。CSG 的 multi-objective QP 提供了此类 trade-off 的 formalization。
> 3. **依赖配对数据。** framing loss 需要 human-camera paired data 计算投影。unpaired 单模态数据无法使用→ Phase 2/3 仅在有配对数据时启用。
> 4. **计算开销（小）。** 正交投影 + SMPL→3D joints→2D 投影，每个 batch 约 <5% 开销。预计算投影参数可进一步降低。

| 工作          | 监督信号                                                 | 渲染参与？                |
| ----------- | ---------------------------------------------------- | -------------------- |
| Pulp Motion | GT human + camera，正交投影计算 on-screen framing loss      | 是（2D 投影作为辅助 loss）    |
| E.T.        | GT camera trajectories from movie data（115K samples） | 否（纯 3D trajectory）   |
| GenDoP      | GT camera trajectories + RGBD（29K shots）             | 部分（depth 参与，RGB 不直接） |

### 5.2 统一框架中的监督设计

**v0 方案（全监督）：**
- Human GT：PulpMotion（193K）、HumanML3D（14.6K）、AMASS
- Camera GT：PulpMotion、DataDoP（29K）、E.T.（115K）
- Loss：token prediction cross-entropy（标准 masked LM loss）+ screen-space framing consistency（可选辅助 loss）
- 渲染：正交投影计算 2D framing loss，轻量可微，仅在 paired data 上使用

AC3D 对监督设计的弱补充是“不要把 camera control 监督无差别灌入所有层/所有预测阶段”。如果 v1 引入 camera-specific control branch 或 edit instruction branch，应增加一个轻量消融：全层 conditioning、camera-token-only conditioning、早层 conditioning、后层 conditioning。该消融只用于 camera control 范围判断，不作为本提案的核心 novelty。

**进一步探索（v1+）：**
- **弱监督：** unpaired human-camera data 上，framing consistency 作为弱对齐信号
- **自监督：** 单模态数据上做 self-reconstruction（mask 部分 human tokens → 预测，不涉及 camera），类似 MaskedMimic 的范式
- **无监督：** 目前不可行。camera trajectory GT 标注成本高但 v0 必需初始监督

---

## Q6: 多数据集能力如何挖掘？

统一 token 框架的核心优势：**不同数据集分模块训练，在 shared vocabulary 中对齐。**

| 数据集               | 提供                                   | 缺失                   |
| ----------------- | ------------------------------------ | -------------------- |
| PulpMotion (193K) | human + camera + framing + text      | —（最完整）               |
| HumanML3D (14.6K) | human + text                         | camera               |
| DataDoP (29K)     | camera + depth + text                | human                |
| E.T. (115K)       | camera + character trajectory + text | 完整 SMPL human motion |
| TSA               | character + camera                   | text condition 不完整   |

**训练策略（三阶段）：**
1. **Phase 1（单模态预训练）：** HumanML3D 上训 human VQ-VAE + human reconstruction；DataDoP 上训 camera VQ-VAE + camera reconstruction。混合 batch，仅激活对应 head。
2. **Phase 2（联合微调）：** PulpMotion 上 joint training，对齐 shared Transformer 中的 human-camera 交互。引入 screen-space framing loss。
3. **Phase 3（跨数据集泛化）：** 混合所有数据集，human-only batch 只优化 human head，camera-only batch 只优化 camera head，paired batch 优化全部。自监督单模态 reconstruction 作为正则化。

**关键风险：** 不同数据集 motion 分布不同（PulpMotion 偏舞蹈/表演，HumanML3D 偏日常动作），shared codebook 可能退化为按数据集聚类的 trivial solution。Phase 3 的 mixed-dataset strategy 需要对抗这种退化。

---

## Q7: edit 怎么做？现有工作是否覆盖 camera edit？

### 7.1 覆盖情况

- **Human motion edit：** MotionFix（text-driven diffusion）、InterEdit（multi-human joint edit）、Unified Conditional Flow（generation + editing + retargeting 统一）
- **Camera motion edit：** **没有 3D token-level 的工作。** Vid-CamEdit 在 video pixel 层面编辑相机轨迹（flow field + 生成式渲染），不涉及 3D trajectory token。

### 7.2 Token-level edit pipeline

```
输入: [text_cond, <HUMAN>, human_tokens, <CAMERA>, camera_tokens] + <EDIT> + edit_instruction_token
  ↓
Edit Locator: 识别需要修改的 token span
  （如 "push in closer on frame 30-60" → camera_tokens[30:60] 的 FOV bin）
  实现方式（v0 可选）:
  - 规则：关键词 → token span 映射（快但不灵活）
  - 学习：轻量 span predictor（需要 edit 标注数据）
  - LLM-based：用 LLM 做 instruction parsing，输出 token span indices
  ↓
Span Masking: 仅 mask 被定位的 token span，其余 token 保持可见
  ↓
Bidirectional Regeneration: Transformer 基于双向上下文预测 mask 位置的 token
  ↓
Consistency Gate: 验证未编辑 token 未漂移（reconstruction error < ε）
  若漂移超过阈值 → 报告可能无法完全保留未编辑内容
  ↓
输出: edited [human_tokens', camera_tokens']
```

**合成 edit 训练数据的方法（v0）：**
1. 从 paired data 中取一条完整 human-camera sequence
2. 随机扰动 human tokens 的某些 span（如 velocity 维度加噪声）或 camera tokens（如 FOV 偏移）
3. 记录扰动前后的 diff → 作为编辑 GT
4. 自动生成 edit instruction text（模板："将第 30-60 帧的镜头推近 20%"）

---

## Q8: text 如何纳入统一框架做 generation & understanding？

**Generation（已有方案）：**
- Text → frozen T5/CLIP encoder 输出 text tokens
- Text tokens 作为序列前缀，与 human/camera tokens 做 bidirectional attention

**Understanding（新问题）：**

v0 最可行的 understanding 任务：
1. **Motion Captioning（反向生成）：** `<human, camera> + <masked text>` → 生成动作/运镜描述。PulpMotion 的 text annotations 提供监督。
2. **Camera Edit Understanding：** "这段 trajectory 和原版有什么不同？" 构造方法：随机 edit camera trajectory → 生成 diff description → 训练模型预测 diff。
3. **Motion QA：** "这段运镜的主体是谁？""第 50 帧为什么切特写？"需要构建 QA 数据集，v1+。

---

## Q9: v0 MVP 的可行范围？

**目标：** 证明 unified token 框架在三项 generation task 上不退化于 modality-specific baseline。

**架构：**
- Human VQ-VAE：复用 MotionGPT 的预训练 codebook
- Camera VQ-VAE：GenDoP 风格的 trajectory quantization
- Transformer：BERT-base scale（~150M params），bidirectional，12 layers
- Text encoder：frozen T5-base

**数据：**
- 主训练集：PulpMotion（193K，唯一 paired 数据）
- 辅助：HumanML3D + DataDoP（单模态 reconstruction 正则化）

**Baselines：**
1. Human generation upper bound：MotionGPT / MoMask（human-only）
2. Camera generation upper bound：GenDoP（camera-only）
3. Joint generation upper bound：Pulp Motion（continuous diffusion，SOTA）
4. Naive pipeline：MotionFix（human edit）→ E.T.（camera from human）

**核心验证指标：**
- Human quality：FID、Diversity、Foot Contact（vs MotionGPT）
- Camera quality：ATE、Framing FID（vs GenDoP）
- Joint consistency：CLaTr-Score（vs Pulp Motion）
- 关键问题：unified model 的 human quality 是否显著低于 human-only baseline？camera quality 是否显著低于 camera-only baseline？如果不退化太多（<10%），则 unified 范式的 overhead 是可接受的。

**v0 不做的：**
- Token-level editing（v1）
- Understanding tasks（v1）
- Multi-dataset mixed training with alignment losses（v1）
- 真实视频渲染验证（v1）

---

## Q10: 主要风险和开放问题？

| 风险 | 严重度 | 缓解 |
|---|---|---|
| Human-from-camera 可能 ill-posed（一个 camera 对应无穷 human） | 高 | 要求 text condition 提供充分约束；v0 先验证 camera-from-human 和 joint gen |
| VQ 量化精度不够，camera 细微运动丢失 | 中 | 残差 VQ（MoMask 方案）提高精度；必要时保留 continuous residual |
| Unified model 在单一模态上退化严重（>15%） | 高 | 单模态 reconstruction 正则化；若退化不可接受则降级为 multi-head 分离架构 |
| Paired human-camera-text 数据稀缺 | 高 | PulpMotion 做主力，混合单模态数据 + self-reconstruction 正则化 |
| Pulp Motion 团队可能正在做类似方向 | 中 | 加速 v0；通过 token-level edit 形成差异化（Pulp 的 auxiliary sampling 不是 mask-predict） |
| 缺乏 camera editing 的标准评测 | 中 | v0 暂不做 edit；v1 自行构造编辑评测集（合成扰动 + GT diff） |

**关键开放问题：**
1. Human token 和 camera token 的最优比例？2:1？1:1？取决于各自 VQ codebook 大小
2. Screen-space framing loss 在 token 框架中的最佳注入点？Encoder 侧（影响 token 表示）还是 Decoder 侧（影响预测分布）？
3. 能否用 pretrained video diffusion model 的隐空间作为 human-camera 对齐信号（AdaViewPlanner 思路的泛化）？
4. Token-level edit 的 locator 精度：规则方法 vs 学习方法的 tradeoff？

---

## 2026-06-08 接力审查：MoLingo / ActionPlan 组合方案

> [!warning] 结论
> 原始设想 **no-go as proposed**：PulpMotion 当前公开数据支持的是 sequence-level 双 caption，而不是 frame-level `human-frame_text` / `camera-frame_text` 监督；ActionPlan 的 frame-level action plan 与 MoLingo 的 SAE 语义对齐都不能直接迁移。应 pivot 到 **PulpMotion-native branch-masked conditional generation**：保持 PulpMotion 的数据结构、AE、latent space、Aux sampling 不变，只测试分支条件解耦是否有正向收益。

### 真实数据结构核查

数据源为 4090 上的 `/data/public/ripemangobox/Motion/datasets/pulpmotion-data`，抽样来自 `mixed_test_split.txt`。PulpMotion 的 joint sample 由 `TrajCharProjDataset` 组装：

- camera：`traj/{sample_id}.txt`、`intrinsics/{sample_id}.npy`、`cam_segments/{sample_id}.npy`
- human：`smpl_raw_rifke/{sample_id}.npy`、`smpl/{sample_id}.npy`
- caption：`caption_char/{sample_id}.txt` 与 `caption_cam/{sample_id}.txt`
- 模型输入：`human_feat` 是 SMPL RIFKE 运动特征，不是 TMR/CLaTr；TMR/CLaTr 是评估与文本 embedding 相关字段。
- PulpMotion 的 `caption_char` / `caption_cam` 是整段文本；前 1000 个 mixed test 样本中，轨迹长度 min/mean/max 为 `9 / 124.76 / 251` 帧，human caption 词数为 `6 / 14.06 / 41`，camera caption 词数为 `6 / 14.03 / 75`。

| sample_id | human motion text | camera text | frames | camera summary | human summary |
|---|---|---|---:|---|---|
| `2011_-4GsCEopbd4_00008_001_a` | A person leans forward and bends their head towards the table, focusing intently on an object in front of them. | The camera moves laterally to the left (trucking left) for the entire shot. | 69 | `traj` 69x4x4, `intrinsics` 69x4, `cam_segments` 82; camera translation first/mid/last = `[-0.0182, 1.1093, 1.2763]` / `[0.2413, 1.0111, 1.2869]` / `[0.2316, 1.0116, 1.2922]`; path length `0.4294`. | `smpl_raw_rifke` 69x199; SMPL keys `betas/body_pose/global_orient/transl`; root translation first/mid/last = `[0.0028, 0.2400, 0.9857]` / `[0.0827, 0.2512, 0.8699]` / `[0.1613, 0.2551, 0.9617]`; root path length `0.8495`. |
| `2011_-4GsCEopbd4_00017_000_a` | A person stands still and turns his head slightly to the right. | The camera remains static throughout the entire shot. | 105 | `traj` 105x4x4, `intrinsics` 105x4, `cam_segments` 126; camera translation first/mid/last = `[-0.3291, 2.1156, 1.4867]` / `[-0.3294, 2.1150, 1.4977]` / `[-0.3287, 2.1190, 1.4978]`; path length `0.0595`. | `smpl_raw_rifke` 105x199; SMPL keys `betas/body_pose/global_orient/transl`; root translation first/mid/last = `[0.0020, 0.2173, 0.8309]` / `[0.0475, 0.2270, 0.8351]` / `[0.0174, 0.2517, 0.8136]`; root path length `0.3540`. |
| `2011_-EuO6OFypLo_00002_000_a` | A person walks forward, swings their arms, and steps over a staircase. | The camera begins with a trucking right-pull-out motion, followed by a continuous trucking right motion. | 159 | `traj` 159x4x4, `intrinsics` 159x4, `cam_segments` 190; camera translation first/mid/last = `[3.1742, 3.4468, 1.6271]` / `[3.0208, 3.8645, 1.6735]` / `[2.8165, 4.1444, 1.8000]`; path length `0.8471`. | `smpl_raw_rifke` 159x199; SMPL keys `betas/body_pose/global_orient/transl`; root translation first/mid/last = `[0.0030, 0.2459, 0.8875]` / `[1.3840, 3.0592, 0.9986]` / `[0.8796, 3.8097, 1.3571]`; root path length `4.6283`. |
| `2011_-EuO6OFypLo_00002_000_b` | A person walks forward, extends their arms outward, and then turns slightly to the right. | The camera starts static and transitions to a boom top position during the shot. | 137 | `traj` 137x4x4, `intrinsics` 137x4, `cam_segments` 164; camera translation first/mid/last = `[0.3720, 2.0013, 1.2070]` / `[0.3555, 2.0022, 1.2107]` / `[0.3226, 1.9818, 1.2881]`; path length `0.1368`. | `smpl_raw_rifke` 137x199; SMPL keys `betas/body_pose/global_orient/transl`; root translation first/mid/last = `[0.0030, 0.2459, 0.9204]` / `[0.0246, 0.1897, 0.9310]` / `[0.0357, -0.3146, 1.4843]`; root path length `1.5635`. |

**关键推论：** 这些样本能支持“sequence-level human caption + sequence-level camera caption + paired human/camera motion”的联合建模；不能直接支持 ActionPlan 式逐帧 action plan，也不能直接支持 MoLingo 式 BABEL frame-label SAE 对齐。若要得到 `human-frame_text` 或 `camera-frame_text`，需要额外构造伪标签，例如规则分段、LLM caption decomposition、或从 `cam_segments` / SMPL phase 自动派生；这会引入一个新的数据构造课题，不应作为当前 MVP 前提。

### DS 严格审查后的前提判断

| 原设想 | 审查结论 | 处理 |
|---|---|---|
| stage1 用 MoLingo SAE 生成 `human-frame_text` / `camera-frame_text` 双分支对齐 | 前提过强。MoLingo SAE 依赖 human frame-level text labels；PulpMotion 没有 frame-level human/camera text，且 MoLingo 不含 camera 分支。 | 不作为当前路线。只能借鉴“多 token 条件化”和“语义辅助 loss”的思想。 |
| 直接使用 ActionPlan 的 frame-level action plan 作为 stage2 条件 | 不可直接实现。ActionPlan 官方仓库截至 2026-06-08 公开 inference code 和 weights，training/evaluation code 未公开；并且 frame-level plan 依赖 BABEL-style 标注。 | 不作为当前路线。只能借鉴分支 mask、异质 timestep、progressive denoising 的思想。 |
| 用 MoLingo SAE 替换 PulpMotion `human_feat` | 不可作为小改动。PulpMotion 的 `human_feat` 是 SMPL RIFKE 运动特征，并与 camera 特征共同进入已训练 joint AE；替换表示会破坏 AE / decoder / Aux projection 契约。 | 禁止作为 MVP。若要替换表示，等同于重训 AE 与扩散主干。 |
| `<human motion, motion frame text, camera trajectory, camera frame text>` 同时送入 diffusion 多任务训练 | 目标合理但当前数据不支撑 `frame text`。 | 改写为 `<human latent, camera latent, human caption, camera caption>` 的 branch-masked conditional generation。 |

### 推荐 pivot：PulpMotion-native branch-masked conditional generation

保留 PulpMotion 原生工作面：

- 不替换 `smpl_rifke` / camera trajectory 表示。
- 不重训或破坏 `AlignedAutoencoder` / `AAMMARDM` 的 latent contract。
- 保留 Aux sampling 的 `W_proj` / `Pw_proj` screen-space framing 引导。
- 只在 diffusion condition 与训练 corruption 上做可控小补丁。

**MVP 核心问题：** 在 sequence-level 双 caption 条件下，独立 mask human/camera 条件是否能让模型更清楚地区分“人体语义”和“相机语义”，从而改善 mixed subset 的 FD_framing、Out-rate、TMR-Score、CLaTr-Score？

### 4090 可执行 MVP

1. **Baseline 固化**
   - 使用 PulpMotion 原版 `config_dit_xy` 或 `config_mar_xy`，先在 small validation subset 上跑原始 checkpoint 的指标。
   - 只使用可比较指标：FD_framing、Out-rate、FD_TMR、TMR-Score、FD_CLaTr、CLaTr-Score、F1、Coverage。

2. **Text branch mask training**
   - 在 `DualCaptionDataset` 或训练 step 中保留 camera/human caption 的 512+512 concat 结构。
   - 训练时独立 dropout：`p_drop_human_text=0.20`、`p_drop_camera_text=0.20`、`p_drop_both=0.10`。
   - 目标不是生成 `frame_text`，而是让模型学会 human caption 与 camera caption 的独立条件贡献。

3. **Latent branch mask training**
   - 在扩散 loss 前对 `z_input` 的 camera latent 或 human latent 做整段 corruption / mask，而不是改 raw feature。
   - 建议先只做一种：`p_mask_camera_latent=0.15`，训练模型在 human latent + 双 caption 条件下恢复 camera latent；反向 `p_mask_human_latent=0.15` 作为第二阶段。
   - 避免在 raw `human_feat` / `camera_feat` 上置零，因为这会引入 AE 外分布；latent 层 mask 更接近扩散 denoising 的任务形式。

4. **最小评估**
   - 使用相同 checkpoint step、相同 seed、相同 eval subset。
   - 如果 full mixed test 太慢，先取固定 `N=512` 或 `N=1024` subset 做 proxy；正向后再跑完整 mixed test。
   - 对照表必须包含原始 PulpMotion checkpoint、text branch mask、latent branch mask 三行。

### 可借与不可借

| 来源 | 可借 | 当前不可借 |
|---|---|---|
| MoLingo | 多 token cross-attention 的条件化思想；sequence-level joint latent 与 dual caption 的弱对比 loss；更强 text adapter 的设计经验。 | SAE frame-level semantic alignment；human-only SAE 直接替换 PulpMotion human 表示。 |
| ActionPlan | 分支 mask / missing modality 训练思想；后续可探索 branch-specific timestep embedding。 | frame-level action plan；official training pipeline；直接复用 streaming sampler 训练。 |
| PulpMotion | 数据、joint AE、DiT/MAR 扩散主干、Aux sampling、评价脚本。 | 直接提供 frame-level text 监督。 |

### Go / no-go 与 kill criteria

**Go:** PulpMotion-native branch-masked MVP。

**No-go:** 原始“MoLingo SAE + ActionPlan frame plan + `human-frame_text/camera-frame_text`”路线。

**Kill criteria:**

- text branch mask 或 latent branch mask 后，FD_framing 没有改善 `> 3%`，且 Out-rate / TMR-Score / CLaTr-Score 任一明显劣化。
- masked 训练使 Out-rate 超过原版 `+5%`，说明跨模态幻觉或构图约束失衡。
- 4090 上一次 small-subset 训练/评估迭代无法在可控时间内完成，或 batch size 过低导致指标噪声无法解释。
- 若需要构造 frame-level pseudo label 才能继续，则暂停，不把它混入当前 MVP；另开数据标注/自动分段路线。

---

## 2026-06-10 修正审查：Stage2 必须分离 human / camera tokens

> [!warning] 上一版结论被推翻
> 上一版把 PulpMotion 的 coupled `z` latent 当作 Stage2 主生成变量，这是方向性错误。三模式 generation 的定义要求 human 与 camera 在生成变量上可独立遮挡、独立条件化、独立生成；耦合 latent 无法严格表达 `given human -> camera`、`given camera -> human`、`text -> human + camera` 三种任务。因此 Stage2 必须建立在分离的 `H_tokens` 与 `C_tokens` 上，而不是 PulpMotion joint AE 的单一耦合 latent。

### 修正后的硬约束

- Stage2 是完整 generator 范式，不是局部 edit / repair 模块。
- 主生成变量必须是两个分离序列：`H_tokens` 与 `C_tokens`。
- 训练目标必须覆盖三种 generation：`H -> C`、`C -> H`、`text -> H + C`。
- PulpMotion 的正确位置是 paired data、caption、baseline、evaluation、screen-space framing 证据；不是 Stage2 主 latent。
- 当前已训练的 human / camera VAE、VQVAE、FSQ、HFSQ 应作为 Stage1 separated tokenizer candidates，Stage2 只消费这些 tokens。

### 证据约束

- [[analysis/CVPR_2024/MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]] 的核心证据是 RVQ + masked bidirectional Transformer：它是 human-only，但 masked generation 范式天然支持任意位置遮挡和迭代补全。外部核查确认其官方实现公开在 [MoMask GitHub](https://github.com/EricGuo5513/momask-codes)。
- [[analysis/ICLR_2026/Beyond_Text-to-Image_Liberating_Generation_with_a_Unified_Discrete_Diffusion_Model|Muddit]] 证明统一离散扩散可对多模态 tokens 进行并行 mask generation。外部核查确认其官方实现公开在 [Muddit GitHub](https://github.com/M-E-AGI-Lab/Muddit)。它的 domain gap 大，但范式贴近 `H_tokens + C_tokens + text` 的统一生成。
- [[analysis/ICCV_2025/GenDoP_Auto-regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP]] 是 camera-only AR token generator，不能做 human-camera 主生成器；但其 camera normalization、DataDoP、camera caption 与 trajectory tokenization 对 camera Stage1 / camera-only baseline 有价值。外部核查确认 [GenDoP GitHub](https://github.com/3DTopia/GenDoP) 已公开训练、推理、数据构建代码。
- [[analysis/NEURIPS_2023/MotionGPT_Human_Motion_as_a_Foreign_Language|MotionGPT]] 与 [[analysis/CVPR_2023/T2M-GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete_Representations|T2M-GPT]] 提供 motion-as-language 和 AR token 生成基线。外部核查确认 [MotionGPT GitHub](https://github.com/OpenMotionLab/MotionGPT) 与 [T2M-GPT GitHub](https://github.com/mael-zys/t2m-gpt) 公开；但 AR left-to-right 不天然支持任意 branch mask。
- [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|TSA / JCCMDM]] 的论文证据最贴近“human 与 camera 作为独立实体交互”，但当前未确认可直接复用的官方代码；它应影响 Stage2 的 cross-modal interaction design，而不是成为实现底座。
- [[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation|Pulp Motion]] 仍是最重要的 paired data / evaluation / framing evidence：Aux 在 mixed subset 上将 FD_framing 从 `4.90` 降到 `3.37`，Out-rate 从 `25.98%` 降到 `16.76%`，TMR-Score 从 `23.50` 提到 `25.05`。外部核查确认 [PulpMotion code](https://github.com/robincourant/pulp-motion)、[project](https://www.lix.polytechnique.fr/vista/projects/2025_pulpmotion_courant/) 与 [data](https://huggingface.co/datasets/robin-courant/pulpmotion-data) 公开。
- [[analysis/SIGGRAPH_ASIA_2024/MotionFix_Text-Driven_3D_Human_Motion_Editing|MotionFix]] 是 edit 模型，不适合作为 v0 generator 主框架；只可在 v1 借鉴 edit 数据构造与 source-preserving objective。

### 重新排序

| 优先级 | 框架 / 证据 | 适合作为什么 | 处理 |
|---:|---|---|---|
| 1 | MoMask | 主框架核心 | 扩展其 masked bidirectional generator 到 `H_tokens + C_tokens`；不直接复用 human-only tokenizer 假设。 |
| 2 | Muddit / unified discrete diffusion | 主框架备选 | 若 MoMask 代码过度绑定 human motion，可转向更通用的 discrete diffusion / MaskGIT-style generator；代价是 domain adaptation 更大。 |
| 3 | TSA / JCCMDM | 交互结构证据 | 借“独立实体 + 双向交互”思想，设计 cross-modal attention / modality-specific blocks；不依赖其代码。 |
| 4 | GenDoP | camera 模块与 baseline | 借 camera normalization / trajectory tokenization / camera-only AR baseline；不作为 joint generator。 |
| 5 | MotionGPT / T2M-GPT | AR baseline 与任务模板 | 作为 text-to-motion / text-to-joint-token 自回归对照；不作为主路线。 |
| 6 | PulpMotion | 数据、baseline、eval、framing 监督 | 使用 PulpMotion paired data、caption、split、metrics、screen-space framing；禁止把 coupled `z` latent 当 Stage2 主变量。 |
| 7 | MotionFix | v1 edit 参考 | v0 generation 不采用；v1 可借 edit triples、source preservation、编辑评测思想。 |
| 8 | PulpMotion coupled stage2 | no-go as generator | 只能作为 SOTA continuous coupled baseline；不能实现严格三模式 separated generation。 |

### v0 推荐架构

Stage1 使用分离 tokenizer：

- `H_tokens = Tok_H(human_motion)`：优先比较 human VQVAE / FSQ / HFSQ 的 reconstruction 与 downstream token predictability。
- `C_tokens = Tok_C(camera_trajectory)`：优先比较 camera VQVAE / FSQ / HFSQ 的 reconstruction、smoothness、framing-sensitive errors。
- 不要求 human 与 camera 共享 tokenizer；可以共享 Stage2 vocabulary space，但 token ID namespace 必须保留 modality offset 或 modality embedding，避免 code collision 被误解释为语义共享。

Stage2 使用 MoMask-like masked generator：

```text
input = [TEXT] [H_1 ... H_L] [C_1 ... C_L]
embeddings = token_embedding + modality_embedding + temporal_position_embedding
model = bidirectional Transformer / masked Transformer
objective = cross entropy on masked H/C token positions
```

推荐使用时序交错，而不是简单拼接作为第一版主设置：

```text
[TEXT] [H_t0] [C_t0] [H_t1] [C_t1] ... [H_tL] [C_tL]
```

原因：三模式 generation 最核心的不是“生成两个长序列”，而是保持 human 与 camera 的帧级对齐。交错序列让同一时间的 `H_t` 与 `C_t` 在局部 attention 中自然相邻；同时保留 modality embedding，模型仍可区分两个分支。

### v0 masking schemes

训练时均匀或加权采样以下模式：

| 模式 | 可见 token | mask token | 目标 |
|---|---|---|---|
| Camera-from-human | text + all `H_tokens` | all `C_tokens` | `H -> C` |
| Human-from-camera | text + all `C_tokens` | all `H_tokens` | `C -> H` |
| Joint generation | text only | all `H_tokens` + all `C_tokens` | `text -> H + C` |
| Denoising regularization | text + random visible H/C spans | random H/C spans | 提高局部补全与鲁棒性 |
| Frame mask | text + context frames | same-frame `H_t/C_t` blocks | 强化同步与边界恢复 |

Loss 只在 masked token 上计算：

```text
L = CE(pred_H[mask_H], H_gt[mask_H]) + CE(pred_C[mask_C], C_gt[mask_C])
```

可选辅助 loss：

- 同帧 `H_t` / `C_t` hidden states 的 contrastive / alignment loss。
- 解码后投影到 screen-space 的 framing loss，只在 paired PulpMotion data 上启用。
- 不把 Pulp coupled latent reconstruction loss 混入主目标。

### PulpMotion 在新路线中的正确位置

- **数据**：使用 PulpMotion 的 paired human-camera sequences 与 `caption_char` / `caption_cam`。
- **baseline**：PulpMotion continuous coupled generator 是强 baseline，用于证明 separated-token generator 是否值得。
- **评估**：沿用 FD_framing、Out-rate、TMR-Score、CLaTr-Score、human FID、camera quality 等可比较指标。
- **监督**：screen-space framing 可作为 auxiliary loss / guidance，但必须作用在 decoded `H_tokens` / `C_tokens` 结果上。
- **禁止事项**：不能把 Pulp joint AE 的 coupled `z` 作为 Stage2 生成变量；否则三模式 generation 只是伪条件生成。

### MoMask / Muddit / Pulp stage1 的补正

- **工程优先级**：v0 仍优先 MoMask-like masked Transformer，因为它的代码和训练范式更接近当前 motion-token pipeline；主要改动集中在 paired token dataloader、modality embedding、branch mask sampler、双 head / shared head。
- **研究优先级**：Muddit-style unified discrete diffusion 的范式更干净，天然适配多模态 token 任意条件生成；但 domain gap 和代码改造风险更高，应作为 MoMask v0 失败或效果不足时的回退路线。
- **Pulp stage1 可复用边界**：如果 Pulp AE 只有单一 coupled latent，则不能作为 Stage2 tokenizer；如果其内部显式保留可分离的 human latent `x` 与 camera latent `y`，可作为 continuous-latent ablation 或快速原型，但不应混进 MoMask 式 discrete generator。连续 latent 三模式生成需要 masked diffusion，而不是 token cross entropy。

### No-go / kill criteria

- 三模式中任意一项无法独立推理：直接 no-go。
- `H -> C` 或 `C -> H` 相比 joint generation 指标劣化超过 `20%`，说明模型没有学会 branch-conditional generation。
- camera token reconstruction 好但 decoded trajectory 抖动、framing 失控，说明 camera tokenizer 不适合作为 Stage2 target。
- human token reconstruction 好但 `C -> H` 生成大量平均动作，说明 camera condition 对 human motion 信息不足；需降低该模式权重或要求更强 text condition。
- 交错序列导致 token collision 或 modality confusion，则必须改为 separate vocabulary offset + explicit modality heads。
- 若 MoMask 改造超过“dataset + embeddings + mask sampler + heads”四处核心改动，说明 implementation base 不合适，切换到自写 BERT-style masked Transformer / Muddit-style discrete diffusion。
- 若需要 frame-level text 才能训练，立即暂停；PulpMotion 当前只有 sequence-level human/camera captions，frame-level text 属于新数据构造课题。

---

## 与 StoryMotion-CSG 和 CameraShotEdit 的关系

```
Unified Token Framework（本文）
  ├─ Generation: 三模式 mask-predict
  │   └─ 可从零生成 human-camera asset → 作为 CSG 和 CameraShotEdit 的上游
  └─ Edit: token-level mask + regenerate
      ├─ 覆盖 CSG 的 "local repair"（统一实现：mask boundary tokens）
      └─ 覆盖 CameraShotEdit 的 "joint motion-camera edit"（统一实现：multi-span mask）

StoryMotion-CSG: 保护 interiors + boundary repair → token 框架中的 "mask boundary tokens only"
CameraShotEdit: source motion + edit + shot → token 框架中的 "text-conditioned multi-span mask"
```

统一框架是更底层的范式。CSG 的确定性优化在小规模可控场景可能更可靠；token 框架的优势在于统一 modeling 和 scale。两者可以共存——统一框架生成候选，CSG solver 做确定性验证和精确修复。

---

## Source Links

- [[ideas/camera/2026-06-05_camera-movement-generation-system-survey-llm-audit-merged|Camera Movement Generation 系统调研]]
- [[ideas/StoryMotion/2026-06-04_storymotion_cinematic_section_graph_plan|StoryMotion CSG Plan]]
- [[ideas/StoryMotion/2026-06-05_camera-shot-edit|CameraShotEdit Proposal]]
