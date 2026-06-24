---
title: "Motion Data Rep"
created: 2026-04-16T23:50:18+08:00
updated: 2026-04-17T00:30:21+08:00
tags:
  - rule-insight
  - motion-representation
  - motion-data
  - motion-tokenization
status: refined
source_papers:
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]"
  - "[[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions|Being-M0]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling|MoGenTS]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches|MotionPatches]]"
  - "[[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]"
  - "[[paperAnalysis/Motion_Generation/TPAMI_2023/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory|Bailando]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2023/2023_MDM_Human_Motion_Diffusion_Model|MDM]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction|MaxSim]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_Move_in_2D_2D_Conditioned_Human_Motion_Generation|Move-in-2D]]"
  - "[[paperAnalysis/Motion_Generation/AAAI_2024/2024_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Motion_Synthesis|UNIMASK-M]]"
  - "[[paperAnalysis/Motion_Generation/ICCV_2025/2025_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space|MotionStreamer]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation|COME]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_ViMoGen_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation|ViMoGen]]"
  - "[[paperAnalysis/Human_Interaction/ECCV_2024/2024_MOB_Revisit_Human_Scene_Interaction_via_Space_Occupancy|MOB]]"
  - "[[paperAnalysis/Human_Interaction/SIGGRAPH_Asia_2024/2024_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruction|LINGO]]"
---
# Motion Data Rep

> [!abstract] 审核后的结论
> 这份笔记把“动作数据的表示与表征”整理成 9 条 best practices，并在文末补了两个扩展问题：`是否值得做 3D 表征`，以及 `position + rotation 共存时怎样避免优化目标打架`。
> 其中第 4 条和第 9 条是本次新增独立条目：前者把 `loss 空间对齐` 单列出来，后者补充了 `velocity / acceleration / contact` 这类控制友好的辅助通道。
> 更稳妥的总原则不是“所有东西都 global 化”，而是“global 几何要容易恢复，最终监督要对齐 global 目标”。

## 0. 先说明：1D 和 2D 表征到底指什么？

| 结构       | 含义                        | 典型形式                                    | 优势                       | 代价                    | 代表                                                                                                                                                     |                                                                                                                                                         |                                                                                                                                                                |                                                                                                                                                                               |                 |
| -------- | ------------------------- | --------------------------------------- | ------------------------ | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 1D 单体表征  | 每一帧压成一个向量或一个 token        | `x_t ∈ R^D`，或每帧 1 个离散码                  | 简单，直接兼容标准 Transformer    | 关节拓扑被折叠，细粒度编辑和局部建模能力弱 | 早期 frame-token VQ / VAE 路线                                                                                                                             |                                                                                                                                                         |                                                                                                                                                                |                                                                                                                                                                               |                 |
| 2D 结构化表征 | 显式保留“时间 × 关节”或“时间 × 特征”结构 | `X ∈ R^{T×J×d}`、`T×D` 图像、motion patches | 时空结构显式，局部编辑、部位建模和条件注入更自然 | token 数变多，注意力和量化成本上升  | [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition | PRISM]]、[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling | MoGenTS]]、[[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions | Being-M0]]、[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches | MotionPatches]] |

`PRISM` 的 2D 是 `time × joint token`，`MoGenTS` 的 2D 是 `time × joint` token 图，`Being-M0` 的 2D 是 `time × feature` 图像化 tokenization，`MotionPatches` 则是把 motion 切成时空 patch 再送入 ViT。它们不是同一种 2D，但共同点都是“不再把整帧身体折叠成一个单体 token”。

## 1. 优先保留 global-style geometry，不要过早把 motion 压进强 canonical frame

证据强度：高。

更稳妥的说法是：在长序列生成、约束控制和多段拼接场景里，`global / global-style reference` 往往比“每帧都强 canonicalize 到局部朝向”更稳定。[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 明确指出，per-frame heading canonicalization 容易在急转、翻滚和 continuation 时引入不连续；因此它采用 `smoothed global root position`，并保留更接近 global 的 joint geometry。

但这不等于“所有旋转都必须用 global rotation”。[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 仍使用 SMPL 原生的局部 6D rotation，只是把 root 位置和全局朝向单独显式建模，并通过 FK / global-space loss 对齐最终目标。因此当前更合理的默认配方是：`root position + heading` 尽量保持 global，可动肢体仍可用运动树局部 6D rotation。

## 2. Root / trajectory 的第一优先级是消灭 xz 抖动；如果预测帧间位移，就监督累计轨迹

证据强度：高。

[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 用 `smoothed global root position` 代替直接 pelvis 投影，核心就是先把 path 的高频抖动压掉，否则模型很容易学成“贴着约束线走，但 gait 不自然”。

[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 则进一步给出更强的 training recipe：如果 root token 里包含帧间位移 `Δp_t`，那么监督累计轨迹 `cumsum(Δp_t)` 比逐帧 delta supervision 更好，因为模型必须为长期偏移负责，而不是只在单帧误差上做局部最优。对流式生成来说，这一条几乎是默认必做项。

## 3. 初始位置和朝向要随机化，避免模型过拟合 canonical heading

证据强度：高。

[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 对每个 clip 做随机 `xz` 平移和随机 `y` 轴旋转，直接针对“训练时全都从原点朝 +z 开始，推理时却要从任意位置和任意朝向接段”的分布错位。

[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 没有用完全相同的增强写法，但它用 `c_dir` 加非 canonicalized joints，从表征定义上解决了同一类问题。两者可以一起看成同一原则的两种实现：一个通过增强扩展分布，一个通过表示避免不连续。

## 4. 新增：loss 空间要和最终优化目标对齐，优先在 global / FK space 计算 supervision

证据强度：高。

这条原本隐含在“global 优于 canonical”里，但实际上值得单列。问题的关键不是“表征必须 global”，而是“最终 loss 不能只在 local / canonical space 自嗨”。[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 的 FK supervision 很典型：VAE 在 rotation space 工作，但监督通过 FK 映射到 3D joint positions，直接惩罚真正影响视觉质量和物理合理性的 global-space error。[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 的 FK consistency 也是同一个思想。

所以更准确的经验不是“canonical 不行”，而是“如果你用了 local / canonical 表征，loss 也最好能回到 global / FK space 计算”，这样优化条件与优化目标才一致。

## 5. 含 FK 链式重建的 VAE / tokenizer，训练时优先用 fp32

证据强度：中高。

[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 明确记录：其 VAE 训练必须使用 float32，bfloat16 会因为 FK 中三角函数和矩阵乘法的级联误差导致崩溃；而生成器 DiT 则仍可用 bfloat16。

因此更通用的表述应是：不是“所有 VAE 都必须 fp32”，而是“只要你的 reconstruction 或 auxiliary loss 里含有 FK / rotation chaining / 累计轨迹这类高敏感几何计算，就先默认 fp32，再逐项验证 mixed precision”。

## 6. 在计算允许时，2D 结构化表征通常优于 1D 单体表征

证据强度：高。

[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling|MoGenTS]] 说明，把每帧整姿态压成一个 token 会让量化精度和空间拓扑都受损；改成 `T × J` 的 2D token 图后，码本利用率显著提高，还打开了局部时空编辑能力。[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 则用 `time × joint token` 的 2D latent grid，让潜空间本身就和运动学结构对齐。[[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions|Being-M0]] 把 motion 升维为 `T × D` 的 2D 图像，再用 2D-LFQ 解决 1D tokenizer 的信息瓶颈和 codebook collapse。[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches|MotionPatches]] 则证明 patch 化后的时空块表示可以更自然地复用 ViT 的建模能力。

代价同样很明确：2D 结构会让 token 数接近 `J` 倍增长，若直接全局 self-attention，复杂度近似平方上升。因此实际落地通常要配 axial attention、patching、层级分解或稀疏注意力。

## 7. Motion 侧的分解粒度越细，通常越有利于精细动作建模，即便 text 侧还没有等粒度对齐

证据强度：中高。

[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 是最直接的证据：它的文本条件仍然是标准 T5 全局注入，但 motion latent 已经细到逐关节 token，结果单靠潜空间设计就显著提升重建和生成质量。[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches|MotionPatches]] 和 [[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]] 也都支持同一趋势：哪怕 text 还不是 joint-level 或 part-level，对 motion 做更细粒度的结构化切分，仍然会提升局部建模与组合控制能力。

但这条结论应带一个硬约束：粒度不是越细越好，而是“细到足以承载可控性和局部动态，但不把注意力成本和接口复杂度推爆”。实践里常见的平衡点是 `part-level`、`joint-level` 或 `patch-level`，而不是无限细分。

## 8. 动作表示最好同时保留 rotation 和 position，而且 position 要能轻易恢复 global position

证据强度：高。

如果只保留 position，很多下游任务最终还得做 IK，容易引入额外误差。[[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions|Being-M0]] 明确把 `SMPL-D135` 相比 `H3D-Format` 的优势归因于“保留原始关节旋转，更无损”；[[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]] 也强调 `HuMo263` 直接保留 6D rotations + position + foot contact，避免从 position 反推 rotation 的 IK 开销和误差。

但如果只保留 rotations，做 trajectory conditioning、waypoint、path control 或 position-conditioned editing 又会变得很别扭。[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 的 raw motion space 同时保留 root / joint positions、rotations、velocity、contact；[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 也把 global root position、global orientation 和 joint rotations拆开表示。[[paperAnalysis/Motion_Generation/TPAMI_2023/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory|Bailando]] 甚至用 hybrid training 先借助 3D positions 学“空间可分辨”的码本，再回到 rotations 输出，说明两种信息是互补而不是二选一。

## 9. 新增：面向控制和编辑时，显式保留 velocity / acceleration / contact 这类辅助通道往往很值

证据强度：中。

这条目前最强的直接证据来自 [[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]。它的 raw motion space 显式包含 `r^p, r^a, j^p, j^v, j^a, f`，于是 path、keyframe、joint rotation、foot contact 都能统一成“部分维度已知 + mask”的补全问题。这类设计在 authoring、constraint satisfaction 和 multi-prompt composition 中尤其有价值。

这条我会把它标成“新增且证据强度中等”，因为目前还没有像前几条那样被多篇工作同时反复验证。但如果我们的目标明确包含 `path control / contact control / transition stability`，那它很值得作为默认配置打开。

## 推荐默认配方

如果目标是 text-to-motion、streaming generation 或 controllable generation，一个相对稳妥的默认 motion representation 可以是：

1. `root`: smoothed global position，外加 global heading；若做流式建模，再显式加入 `Δp_t`。
2. `body`: 关节旋转优先用连续 6D rotation；同时保留可恢复 global position 的 position 通道。
3. `layout`: 优先选择 2D 结构化布局，如 `time × joint`、`time × feature` 或 `time × part patch`。
4. `training`: 随机 `xz` 平移 + 随机 `y` 轴旋转；trajectory 用 cumulative loss；几何一致性用 FK / global-space loss。
5. `precision`: 含 FK 的 tokenizer / VAE 先用 fp32，生成器再考虑 bf16。
6. `optional channels`: 如果有 authoring / control 需求，再加 velocity、acceleration、foot contact。

## 本次新增条目

1. `loss 空间对齐` 被单独提成一条，因为它比“global vs canonical”更本质。
2. `velocity / acceleration / contact` 被补成一条新的控制导向经验，但当前证据强度低于前 8 条。


## 扩展思考

### Q1：常见有 1D 和 2D 表征，是否值得继续做“3D 表征”？能否复用 video generation 的 pipeline？

短答：**值得想，但本地 KB 里还没有一个已经被充分验证的“body motion 3D tokenization”主流范式。当前更成熟的做法，仍然是 1D 或 2D；真正稳定的“3D”更多出现在 `scene / condition` 侧，而不是把 skeleton 本体直接体素化。**

这里最好先区分三件事：

1. **输出是 3D motion**，不等于**内部表征是 3D tensor**。像 [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]、[[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions|Being-M0]]、[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling|MoGenTS]] 输出的当然都是 3D 人体运动，但它们内部仍主要是 `1D` 或 `2D` 结构化表示。
2. **3D 场景条件已经很成熟**，但那是 `scene representation`，不是 `body motion representation`。[[paperAnalysis/Human_Interaction/ECCV_2024/2024_MOB_Revisit_Human_Scene_Interaction_via_Space_Occupancy|MOB]]、[[paperAnalysis/Human_Interaction/SIGGRAPH_Asia_2024/2024_LINGO_Autonomous_Character_Scene_Interaction_Synthesis_from_Text_Instruction|LINGO]] 里的 3D occupancy / voxel 很有用，可见当第三个维度对应外部几何约束时，3D 表征是高价值的。
3. **motion body 本体的主流仍是 2D 优先**。[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches|MotionPatches]]、[[paperAnalysis/Motion_Generation/AAAI_2024/2024_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Motion_Synthesis|UNIMASK-M]]、[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling|MoGenTS]]、[[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions|Being-M0]] 都在说明：只要把“整帧单体 token”升维到 `time × joint / feature / patch`，很多信息瓶颈就已经明显缓解。

从本地 KB 看，**video / image generation 的 pipeline 是可以复用的，但复用的是 pipeline，不是视觉表征假设本身**。

可以直接借的部分主要有三类：

1. **patch / token 化思路可以借**。[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches|MotionPatches]] 已经证明，把 motion 变成与图像 patch 同构的伪图像后，可以直接复用 ImageNet 预训练 ViT；[[paperAnalysis/Motion_Generation/AAAI_2024/2024_UNIMASKM_A_Unified_Masked_Autoencoder_with_Patchified_Skeletons_for_Motion_Synthesis|UNIMASK-M]] 则说明 patchified skeleton 在 synthesis 任务里也成立；[[paperAnalysis/Motion_Generation/CVPR_2025/2025_Move_in_2D_2D_Conditioned_Human_Motion_Generation|Move-in-2D]] 进一步说明，只要条件本身具有局部空间结构，保留 patch token 往往比先压成单个 global token 更有效。
2. **latent generative backbone 可以借**。[[paperAnalysis/Motion_Generation/ICCV_2025/2025_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space|MotionStreamer]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]、[[paperAnalysis/Motion_Generation/ICLR_2026/2026_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation|COME]]、[[paperAnalysis/Motion_Generation/ICLR_2026/2026_ViMoGen_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation|ViMoGen]] 都说明 motion 生成已经越来越像 image/video foundation model：连续 latent、DiT、flow matching、cross-attention、知识蒸馏，这些都能平移。
3. **foundation prior 也能借**。[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches|MotionPatches]] 借的是 ImageNet ViT，[[paperAnalysis/Motion_Generation/ICLR_2026/2026_ViMoGen_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation|ViMoGen]] 借的是 video generation prior，这两条线都说明“先拿强视觉基础模型，再做 motion-side 适配”是可行路线。

但我不建议把“3D 表征”理解成**把 skeleton 直接体素化成 video volume 再照搬视频管线**，原因有三：

1. motion 是**稀疏的运动学对象**，不是 dense texture field。video volume 里的局部邻域是像素邻域，motion 里更重要的是骨架树、部位耦合和接触事件。
2. 如果第三维只是“把 feature 再堆一维”，但没有明确语义，那么复杂度会上升，信息增益却未必高于精心设计的 2D 表征。
3. motion 比 video 更依赖**显式几何约束**。[[paperAnalysis/Motion_Generation/ICLR_2023/2023_MDM_Human_Motion_Diffusion_Model|MDM]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 都说明，FK、trajectory、foot contact 这些约束不会因为 latent 变“更像 video”就自动解决。

所以当前更稳妥的判断是：

> **如果要做 3D motion representation，更值得尝试的不是“dense voxelized body motion”，而是 skeleton-aware 的 pseudo-3D：把 `time × joint` 再扩成 `time × joint × attribute/channel/event` 或 `time × part × level`，然后复用 3D patch / tube tokenization + latent DiT pipeline。**

换句话说，**可复用的是 video generation 的建模栈；第三维本身则必须由 motion 语义来定义，而不是照搬视觉坐标轴。**

### Q2：动作表示如果同时保留 position 和 rotation，会不会引入分布不匹配和训练目标分歧？现有方法怎么处理？

短答：**会有这个风险，但在 controllable generation / editing 里通常仍然值得保留两者。更关键的是：本地 KB 里几乎没有看到“显式对齐 position 与 rotation 分布”的单独主流方法，主流做法是用共享的几何目标，把二者重新绑回同一个评价空间。**

为什么二者容易“打架”：

1. **单位和尺度不同**：position 是长度量，rotation 是角度或 6D 连续表示，直接拼接后做等权 loss 很容易数值失衡。
2. **语义层级不同**：rotation 更接近局部关节姿态，position 更接近全局几何结果，特别是轨迹、末端落点和场景对齐。
3. **它们冗余但不等价**：rotation 经 FK 能推出大量 position，但 root trajectory、contact 和全局落点又不是只靠局部 rotation 就能稳定表达。
4. **rotation 误差的 position 后果不均匀**：近端关节很小的旋转误差，经 FK 后可能在远端放大成很大的位置偏差。这正是 [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]、[[paperAnalysis/Motion_Generation/ICLR_2023/2023_MDM_Human_Motion_Diffusion_Model|MDM]] 强调几何 supervision 的原因。

但从现有方法看，**position + rotation 共存本身并不是例外，反而很常见**。例如 [[paperAnalysis/Motion_Generation/ICLR_2023/2023_MDM_Human_Motion_Diffusion_Model|MDM]] 的 263 维表示里就已经混合了 root、position、velocity、rotation、foot contact；[[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]] 的 `HuMo263` 也保留了 rotation + root + 冗余 position + foot contact。真正的问题从来不是“能不能共存”，而是“共存后怎么不让优化目标彼此掣肘”。

本地 KB 里比较稳定的解决方式主要有四类：

1. **用 FK / global-space loss 作为共同裁判**。这是最主流的方法。[[paperAnalysis/Motion_Generation/ICLR_2023/2023_MDM_Human_Motion_Diffusion_Model|MDM]] 用 `Lpos / Lvel / Lfoot`，[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 用 FK 后的 `L_joints` 与累计轨迹监督，[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 用 FK consistency。共同点都是：**不是分别在各自空间里自洽，而是让两者都对最终 global geometry 负责。**
2. **用 staged / hybrid training 降低早期冲突**。[[paperAnalysis/Motion_Generation/TPAMI_2023/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory|Bailando]] 先用 3D positions 学到“空间可分辨”的码本，再冻结码本训练 rotation decoder。它隐含的判断很重要：position 更适合学空间先验，rotation 更适合做最终可驱动输出。
3. **用结构分解取代“硬拼一个大向量”**。[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 把 root position、global orientation 和 joint rotation 拆成不同 token；[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 把 `root / joint pos / joint vel / joint angle / contact` 组织成显式多通道 raw motion space；[[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]] 也说明这些量最好有明确分工，而不是假装它们是同质特征。
4. **按任务主动偏向一种表示，而不是永远“两者都要”**。[[paperAnalysis/Motion_Generation/arXiv_2026/2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction|MaxSim]] 给了一个很好的反例：在 token-patch 级细粒度 matching 里，位置表示反而比角度表示更容易引入虚假的空间相关性，所以作者主动改用 joint angle motion image。也就是说，**retrieval / alignment** 任务里，rotation / angle 常常更干净；而 **trajectory / control / scene grounding** 任务里，position 则不可或缺。

因此这件事的更稳妥结论是：

> **如果目标是生成、编辑或控制，position 和 rotation 同时保留通常是值得的；但不要在拼接向量上直接做“等权 MSE”，而应在结构层拆开，在 loss 层用 FK / global-space 重新对齐。**

一个更实用的 recipe 是：

1. 表征层保留二者，但把 `root position / heading / local rotations / optional global positions / contact` 分开建模；
2. 训练层至少加入一个 shared geometric objective，例如 FK joint loss、trajectory cumulative loss、foot-contact loss；
3. 如果任务本身更接近 fine-grained matching，而不是 control，就优先用 angle / rotation 作原子表示，把 position 留给下游或后处理。

所以，**现有方法的主流不是显式做“position-rotation distribution alignment”，而是通过“共享几何监督 + 结构分解 + 分阶段学习”来绕开这个冲突。**
