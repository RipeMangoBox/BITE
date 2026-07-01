---
hypothesis: "PulpMotion stage1 的连续 human/camera latent 不会天然破坏 StoryMotion 的三模式生成；只要 stage2 采用 CondMDI-style branch-mask continuous inpainting，就可以用 human/camera continuous latent 替代原离散 token 主线。"
status: formal_proposal
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI|CondMDI]]"
  - "[[analysis/SIGGRAPH_ASIA_2024/MotionFix_Text_Driven_3D_Human_Motion_Editing|MotionFix]]"
  - "[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness|E.T. / Director]]"
  - "[[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP]]"
  - "[[analysis/CVPR_2024/MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]"
  - "[[analysis/ICLR_2026/Beyond_Text_to_Image_Liberating_Generation_with_a_Unified_Discrete_Diffusion_Model|Muddit]]"
  - "[[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion|Direct-a-Video]]"
  - "[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]"
  - "[[analysis/ICLR_2026/MoCa_Modeling_Object_Consistency_for_3D_Camera_Control_in_Video_Generation|MoCa]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]"
  - "[[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation|COIN]]"
  - "[[analysis/ICLR_2025/3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Generation|3DTrajMaster]]"
  - "[[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation|ShotVerse]]"
  - "[[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes|AdaViewPlanner]]"
  - "[[analysis/arxiv_2026/CT_1_Camera_Trajectory_Generation_for_Camera_Controlled_Video_Generation|CT-1]]"
  - "[[analysis/CVPR_2026/BulletTime_Decoupled_Control_of_Time_and_Camera_Pose_for_Video_Generation|BulletTime]]"
  - "[[analysis/arxiv_2026/CamDirector_Camera_Trajectory_Control_for_Long_term_Video_Generation|CamDirector]]"
  - "[[analysis/CVPR_2026/Taming_Video_Models_for_3D_and_4D_Generation_via_Zero_Shot_Camera_Control|Taming Video Models]]"
  - "[[analysis/ICLR_2026/3D_Scene_Prompting_for_Scene_Consistent_Camera_Controllable_Video_Generation|3D Scene Prompting]]"
  - "[[analysis/TOG_2015/Intuitive_and_Efficient_Camera_Control_with_the_Toric_Space|Toric Space]]"
  - "[[analysis/CVPR_2026/Grounded_Latents_for_Entity_Centric_4D_Scene_Generation|Grounded Latents]]"
  - "[[analysis/ICLR_2026/ConsisDrive_Identity_Preserving_Driving_World_Models_for_Video_Generation_by_Instance_Mask|ConsisDrive]]"
  - "[[analysis/ICLR_2024/UniHSI_Unified_Human_Scene_Interaction_via_Prompted_Chain_of_Contacts|UniHSI]]"
  - "[[analysis/AAAI_2025/ARDHOI_Auto_Regressive_Diffusion_for_Generating_3D_Human_Object_Interactions|ARDHOI]]"
  - "[[analysis/arxiv_2026/HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Motion_Generation|HINT]]"
  - "[[analysis/SIGGRAPH_2025/DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked_Modeling|DuetGen]]"
created: 2026-06-10T19:06:20+08:00
updated: 2026-06-13T20:02:18+08:00
superseded_by: "[[2026-06-13_storymotion-v2-branchmask-inpainting]]"
status: superseded
---

# 2026-06-10 Pulp Stage1 Continuous Latent for Stage2 Three-Mode Generator

> [!abstract] 结论
> **连续 latent 不会从根本上破坏三模式 generation。** 真正的必要条件不是“必须离散 token”，而是 stage2 是否显式学习了 **CondMDI-style branch-mask continuous inpainting**。2026-06-13 的 5090 full generated eval 已完成：6 个 StoryMotion jobs 均为 `exit:0`，每项 `10549` records，无 NaN，指标来自 PulpMotion official callbacks，但采样器是 StoryMotion 自定义 deterministic DDIM START_X，不是 Pulp official sampler。completion 上 `mixed_standard_last` 与 `branch_jh6ft` 基本打平；joint generation 上 `branch_jh6ft` 相比 `mixed_standard_last` 改善 `r_fpd / outscreen / CLaTr / caption F1`，因此保留为当前 joint 候选。与 5090 Pulp no-Aux joint baseline 横向比较时，StoryMotion joint 的 framing 指标显著更好（`r_fpd 0.45`、Out-rate `7.48%`），但语义对齐仍明显落后（TMR `18.72` vs `23.36`，CLaTr `23.70` vs `31.31`，caption F1 `0.284` vs `0.350`）。这不能写成全面优于 PulpMotion；下一步必须先做 text-conditioning、sampler/noise、多样性、输出格式与 outlier / visualization 审计，而不是继续长训。PulpMotion official no-Aux baseline rerun 已在 5090 full mixed split 上完成；`cfg_rate_z=2` 仍只是 no-Aux checkpoint 上的 inference-only projection CFG probe，不能称为论文 Aux baseline。新增 KB 显示 AdaViewPlanner、CT-1、BulletTime、CamDirector、3D Scene Prompting、Taming Video Models 等已覆盖 camera/viewpoint planning 与 4D camera control，StoryMotion 的定位必须落在 subject-relative framing、observed-branch continuity、三模式条件补全与叙事角色层级上。原 2026-06-05 的 unified discrete token 方案应降级为 ablation / 备选路线。

---

## 1. 问题重新定义

原问题是：如果不用离散 token，而直接采用 PulpMotion stage1 的连续 human/camera latent，是否会破坏三模式生成？

三模式目标保持不变：

```text
human text + camera text + human latent  -> camera latent
human text + camera text + camera latent -> human latent
human text + camera text                 -> human + camera latent
```

这里的 `human text` 与 `camera text` 在三种任务中都提供。它们不是 VQA 式的“问题-答案”接口，而是两个固定语义条件：human text 约束人体动作语义，camera text 约束运镜语义。对 `human latent -> camera latent` 来说，camera text 能直接说明运镜目标，human latent 提供具体被拍摄对象，因此“camera 不跟随 human”的风险应通过条件依赖实验量化，而不是作为预设否决项。

关键变化是表示层：

- 旧路线：human motion 与 camera motion 分别离散化为 token，统一放入 mask-then-predict Transformer。
- 新路线：MVP 只保留 human、camera 两个连续 latent block，stage2 在 `concat([z_hum, z_cam])` 空间中做 mask-conditioned continuous diffusion；projection latent 不进入主生成变量。

因此，问题不再是“continuous vs discrete 谁天然支持三模式”，而是：

1. stage1 latent 是否仍保留可切片的 human/camera 分支语义；
2. stage2 训练是否覆盖三种条件缺失模式；
3. 不显式生成 projection latent 时，framing quality 是否仍可由预测的 human/camera 解码后评估并优化。

## 2. Stage1 源码事实

本地源码 artifact：

```text
/data/Life Me/ResearchWY Vault/artifacts/remote4090_motion/pulpmotion_stage1_source_20260610
```

### 2.1 SplitAutoencoder 是显式分支拼接

`SplitAutoencoder.encode` 分别编码 camera 与 human，再 concat：

- camera 输入先拆成 FOV、distance、camera pose；
- camera latent 由 `camera_autoencoder.encode` 得到；
- human latent 由 `human_autoencoder.encode` 得到；
- projection 存在时单独由 `projection_autoencoder.encode` 得到；
- 最终 latent 是 `[camera, projection, human]` 或 `[camera, human]` 的拼接。

`SplitAutoencoder.decode` 又按 `z_distance / z_camera / z_projection / z_human` 切片，并分别调用 camera/human/projection decoder。也就是说，在 split 版本里，latent block 的语义边界是代码级存在的，不是不可拆的黑盒联合向量。

### 2.2 AlignedAutoencoder / AAMMARDM 是联合编码、分支解码

`AlignedAutoencoder.encode` 调用 `autoaligner.encode(camera, human, projection)`。在 `AAMMARDM` 中：

- encoder 输入是 `torch.cat([camera_x, human_x], dim=-1)`；
- joint encoder 输出 camera + human latent 维度；
- projection latent 由 `projection_encoder` 从 joint latent 线性映射；
- 返回时仍 concat 为 `[camera slice, projection slice, human slice]`；
- decode 时用 `camera_latent_dim`、`projection_latent_dim`、`human_latent_dim` 切片，分别送入对应 decoder。

因此，即使 aligned 版本存在 latent entanglement，输出接口仍保留了 branch slice。它不是“一个无法指定 human/camera 的单一 z”。

### 2.3 Pulp sampler 已经按 camera/human index 操作

PulpMotion 的 DDPM sampler 用 `camera_index = net.camera_in_channels` 和 `human_index = -net.human_in_channels` 切分 latent。projection guidance 通过 `W_proj` 和 `Pw_proj` 对 `[camera, human]` 的构图相关方向做投影，再用 `cfg_rate_z` 加权。

MAR sampler 也从全 `mask_latent` 出发，按 schedule 选择待预测 latent positions，再调用 generation sampler 输出连续 latent。它证明 PulpMotion 已有“mask-like schedule + continuous latent denoising”的工程基础。

但是，现有 Pulp sampler 不能直接等价为三模式 stage2。它没有保证训练时显式覆盖 `human visible / camera masked`、`camera visible / human masked`、`both masked` 的 branch-level conditional inpainting。因此 stage2 应借鉴 CondMDI 的 observed-mask 训练，而不是直接把 Pulp 原生 joint generation 当作三模式 generator。

### 2.4 Camera 表征是 subject-relative，不是独立世界轨迹

源码快照：

```text
/data/Life Me/ResearchWY Vault/artifacts/remote4090_motion/pulpmotion_stage1_source_20260610
```

`TrajCharProjDataset.get_feat` 中的 camera feature 是三段拼接：

```text
camera_feat = concat([intrinsics_feat, distance_feat, camera_featvel])
distance_feat = camera_translation - human_root_translation
```

其中 `intrinsics_feat` 为 `2D` FOV，`distance_feat` 为 `3D` 相机到人体 root 的相对位移，`camera_featvel` 为 `9D` camera pose / velocity 表征。对应源码位置是 `datasets/modalities/traj+char+proj_dataset.py` 第 `67-74` 行。

`TrajCharProjDataset.get_raw` 会先从 human feature 解码 `human_raw`，再把 camera feature 拆成 `[x_fov, x_distance, x_camera]`。`x_distance` 反归一化后会加回 `human_raw.joints[..., 0, :3]`，随后再写入 camera translation。对应源码位置是同文件第 `90-103` 行。

因此 camera decode 的世界系 translation 不是只由 camera latent 决定；它会通过 decoded human root 被重新锚定。再结合 `models/autoencoders/autoencoder.py` 第 `56-60` 与 `87-95` 行，Pulp 的 camera latent 应拆成两类条件看待：

```text
z_cam = concat([z_distance, z_cam_motion])
z_distance   <- camera_translation - human_root_translation
z_cam_motion <- FOV + camera rotation / velocity encoded by camera_autoencoder
```

这对三模式定义很关键：`camera + text -> human` 不能被写成“给定独立世界相机轨迹做确定性反演”。在 Pulp-v0 中，它应定义为：给定 `z_distance` 提供的 camera-to-subject relative framing envelope、`z_cam_motion` 提供的相机运动 / 内参条件，以及 human / camera text，生成与该 framing condition 相容的 plausible human latent。模型学习的是 `p(z_hum | z_distance, z_cam_motion, text)`，不是确定性逆问题。

结论：

1. Pulp stage1 本身已经在 camera 表征里显式建模 human-camera 相对关系。
2. 交换或扰动 human latent 会影响最终 decoded camera trajectory，即使 camera latent slice 不变。
3. `camera -> human` 模式保留，但必须作为 relative-framing-conditioned human generation 来验证；其有效性要靠 distance shuffle / zero-out / camera-motion shuffle / cycle consistency / generated geometry gate 排除“只靠 text”或“相对距离泄漏”的伪任务风险。
4. 若 Pulp relative camera condition 在这些 gate 上失败，再把 absolute / canonical camera representation 作为后续 ablation 或方法升级；当前主线不预设已使用绝对世界相机表示。

Aligned autoencoder 进一步把 camera/human 共同编码：`AAMMARDM.encode` 对 `camera_x` 与 `human_x` 做 `torch.cat([camera_x, human_x], dim=-1)` 后送入 joint encoder，decode 时仍按 camera / human latent slice 分别进入 decoder。对应源码位置是 `models/autoencoders/modules/mmardm.py` 第 `137-152` 行。

## 3. 论文证据定位

完整支撑笔记：

- [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]：连续 human-camera latent + projection latent + 构图投影引导已经有效，但它主要解决联合生成的 framing consistency，不等价于三模式条件补全；同时 DiT 和 MAR 都可作为 backbone 参考，但需要改造成 mask-conditioned continuous inpainting。
- [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]：角色-相机必须显式建模双向交互，说明 stage2 不能只做简单 concat 后 unconditional generation。
- [[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI|CondMDI]]：训练时随机掩码 + 显式 mask 输入，可以让连续扩散模型学会从任意部分观测补全。它是连续 latent 三模式训练的最直接方法论依据。
- [[analysis/SIGGRAPH_ASIA_2024/MotionFix_Text_Driven_3D_Human_Motion_Editing|MotionFix]]：编辑/条件改写不是测试时技巧，必须有源运动和编辑文本作为训练条件；对应到本方案，就是不能只靠推理时固定 visible branch。
- [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness|E.T. / Director]]：camera generation 必须显式看到 character trajectory / motion condition，支持 `human text + camera text + human -> camera` 这种显式角色条件相机生成模式。
- [[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]：已经覆盖 zero-shot joint camera + 3D human motion control；StoryMotion 不能把“相机与人体联合控制”本身当成新颖性，必须强调 subject-relative framing、branch-mask 条件补全、叙事/镜头阶段条件和可评价的三模式生成。
- [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes|AdaViewPlanner]]、[[analysis/arxiv_2026/CT_1_Camera_Trajectory_Generation_for_Camera_Controlled_Video_Generation|CT-1]]：已经把 text / image / 4D content 到相机轨迹规划做成强 camera-planner 竞品。StoryMotion 不能只讲“文本到相机”，必须证明 observed human/camera branch、subject-relative framing 和叙事角色关系共同约束生成。
- [[analysis/CVPR_2026/BulletTime_Decoupled_Control_of_Time_and_Camera_Pose_for_Video_Generation|BulletTime]]、[[analysis/arxiv_2026/CamDirector_Camera_Trajectory_Control_for_Long_term_Video_Generation|CamDirector]]、[[analysis/ICLR_2026/3D_Scene_Prompting_for_Scene_Consistent_Camera_Controllable_Video_Generation|3D Scene Prompting]]、[[analysis/CVPR_2026/Taming_Video_Models_for_3D_and_4D_Generation_via_Zero_Shot_Camera_Control|Taming Video Models]]：覆盖 3D/4D camera control、long-term source consistency 与 zero-shot camera guidance。它们要求 StoryMotion 把 “story time / subject motion / camera observation” 解耦清楚，并在 observed-branch continuation、projection coverage 和长程几何一致性上做评估。
- [[analysis/TOG_2015/Intuitive_and_Efficient_Camera_Control_with_the_Toric_Space|Toric Space]]：不是生成模型竞品，但给 subject-relative / two-target screen-space framing 提供经典几何形式化，应作为 Mode A/B framing gate 的理论锚点。
- [[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation|COIN]]：控制-修复扩散先验、人-场景深度约束与软修复直接支持 branch-mask / inpainting 机制定位，也提醒 naive 多步 sampler 的稳定性不是自动成立。
- [[analysis/ICLR_2025/3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Generation|3DTrajMaster]]、[[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion|Direct-a-Video]]、[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]：相机 + 物体 / 多实体运动解耦控制已有成熟 baseline；StoryMotion 的差异必须落在角色-相机相对构图、主次关系与叙事条件共同约束上。
- [[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP]]、[[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation|ShotVerse]]：覆盖 text / director intent 到 camera trajectory 的 planner 路线；StoryMotion 不能只做 camera planner，必须证明 human/camera/content branch 在同一生成空间中相互条件化。
- [[analysis/CVPR_2024/MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]、[[analysis/ICLR_2026/Beyond_Text_to_Image_Liberating_Generation_with_a_Unified_Discrete_Diffusion_Model|Muddit]]：离散 token + masked prediction 是合理路线，但它们不能证明 StoryMotion 必须离散化；Muddit 只能借鉴多任务 mask 训练和任务轮换经验，不能借 VQA 任务定义。

新增 KB 检索后的定位边界：Pulp Motion / ActCam / AdaViewPlanner / CT-1 / E.T. / GenDoP / ShotVerse / BulletTime / CamDirector / 3D Scene Prompting / Taming Video Models 是直接竞品或强相邻竞品；Toric Space 是 subject-relative framing 的理论根基；COIN、MotionPro、ConsisDrive 是 branch-mask / control-inpainting / identity consistency 机制支撑；3DTrajMaster / Direct-a-Video / MotionCtrl / Grounded Latents 是多实体与全局/局部运动控制 baseline；AnchorCrafter、TeamHOI、VLM-guided HOI、HSI-GPT2、SyncDiff、ReGenHOI、HSI 类工作只作为 interaction mechanism inspiration，不应包装成 StoryMotion 直接竞品。

## 4. 核心技术路线

### 4.1 Stage1：冻结 Pulp continuous tokenizer

推荐先不重训 stage1。直接冻结 PulpMotion stage1，但 MVP 只取 human/camera latent：

```text
z_mvp = concat([z_hum, z_cam])
```

其中：

- `z_hum`：human motion latent；
- `z_cam`：camera FOV / distance / pose latent。

第一版优先使用 Pulp 的 aligned autoencoder，因为它已经把 human-camera 的构图关系压入 human/camera latent；同时保留 split autoencoder 作为 disentanglement 对照。`z_proj` 不作为 MVP 的输入或输出，只在需要时由预测的 `z_hum/z_cam` 重算或通过解码后的 screen-space projection 评估。

### 4.2 Stage2：CondMDI-style Branch-Mask Continuous Inpainting

stage2 训练一个文本条件 masked diffusion generator。它不是直接照搬 Pulp 原生 stage2 joint generation，而是把 Pulp latent 空间改写成 CondMDI-style partial observation problem：

```text
G_theta(z_t, z_visible, mask_branch, human_text, camera_text, t) -> denoised masked branch
```

输入由五部分组成：

1. noisy latent `z_t = concat([z_hum, z_cam])`；
2. visible latent `z_visible`，在未掩码分支中保持真实值；
3. branch mask：标记 human / camera 哪些 block 可见，哪些 block 需要预测；
4. human text embedding 与 camera text embedding；
5. diffusion timestep embedding。

训练时采样以下 mask pattern：

| 模式                | 可见 latent | 文本条件                     | 预测目标           | 用途         |
| ----------------- | --------- | ------------------------ | -------------- | ---------- |
| camera completion | human     | human text + camera text | camera         | 根据人体动作生成运镜 |
| human completion  | camera    | human text + camera text | human          | 根据运镜反推人体动作 |
| joint generation  | none      | human text + camera text | human + camera | 从文本联合生成    |

表格中不放 wikilink，避免 Obsidian table 的 `|` 解析冲突。

### 4.3 Projection latent 的地位：不进 MVP，作为 ablation

`z_proj` 不是三模式 MVP 的必需生成变量。PulpMotion 证明 projection/framing guidance 有价值，但它的目标是改善 joint generation 的屏幕构图；StoryMotion 当前要先验证 human/camera latent 的条件补全是否成立。把 projection latent 过早加入主训练会引入额外变量：

- shortcut：模型可能借 projection 统计规律掩盖 camera/human 预测不足；
- 目标耦合：projection 与 camera/human 同时生成时，loss 权重会变成敏感超参；
- 维度负担：projection 可能扩大输出空间，干扰最小三模式判断；
- mask 复杂度：branch mask 从 human/camera 二分支变成三分支，schedule 更难解释。

因此第一版规则是：

1. stage2 输入/输出只包含 `z_hum` 与 `z_cam`；
2. framing 指标通过预测的 `z_hum/z_cam` 解码后计算 screen-space 投影、Out-rate、subject scale、FD_framing；
3. 若需要 latent-space framing regularization，可用预测的 `z_hum/z_cam` 通过 Pulp 的 `W_proj` 计算派生 projection，而不是喂入 ground-truth `z_proj`；
4. `with projection latent` 作为后续 ablation：只有 no-proj MVP 证明三模式条件补全成立后，再比较是否显著改善 framing 且不损害 human/camera 质量。

可选的派生 projection consistency 写为：

$$
\mathcal{L}_{proj} =
\left\| W_{proj}[\hat{z}_{cam}, \hat{z}_{hum}] - W_{proj}[z_{cam}, z_{hum}] \right\|_2^2
$$

第一版更推荐直接用 screen-space 重投影误差作为评估，而不是把它作为主训练 loss：

$$
\mathcal{L}_{screen} =
\left\| \Pi(C^{pred}, H^{pred}) - S^{gt} \right\|
$$

其中 `Pi` 表示把 generated human joints 通过 generated camera 投影到屏幕空间。

### 4.4 Generator 架构优先级

优先级从稳到进：

1. **CondMDI-style DiT continuous inpainting baseline**：最稳，直接验证三模式是否成立；DiT 输入是 `concat([z_hum, z_cam])`，并显式接收 branch mask。
2. **MAR-style iterative latent refinement**：继承 Pulp 的 masked schedule，但需要升级到 branch-aware mask 和 continuous masked loss。
3. **TSA-style branch interaction block**：若模型忽略 visible branch 或 paired geometry 指标不足，再加入 human-camera cross-attention / pairwise interaction。
4. **Discrete token branch**：只作为 MoMask / GenDoP inspired ablation，不作为主 claim。

第一版不要同时重写 stage1、stage2 和数据协议。最小可验证版本只需：

```text
frozen Pulp stage1 + no-proj concat([z_hum,z_cam]) + CondMDI-style branch mask DiT + three-mode evaluation
```

### 4.5 训练策略：先混合训练，不默认 curriculum

当前保守结论是：**第一版不默认使用课程学习**。现有证据支持的是“目标推理条件必须出现在训练分布中”，而不是“必须先学容易任务再学困难任务”。因此 v0 训练应直接覆盖三种主任务：

```text
camera completion: 1/3  # 可按业务优先级上调到 0.5
human completion:  1/3
joint generation:  1/3
```

`repair/edit` 或时间 span mask 不进入第一版主训练。原因是当前三模式定义是整段 branch completion；过早加入 span 长度、span 比例、局部修复目标，会把 schedule 超参放大，反而不利于判断连续 latent 三模式是否成立。它可以作为后续 ablation：例如 `10%` partial span mask，专门评估局部编辑能力。

目标 loss 仍应只在 masked branch 与 valid latent frames 上计算。visible branch 通过输入保持和采样时 hard replacement 保真，不作为主 loss。

**设计目标**是先按分支归一化，再在 joint generation 中对 human / camera 分支等权合并：

$$
\mathcal{L}_{cam} =
\operatorname{mean}_{t,d}\left\| \hat{z}_{cam} - z_{cam} \right\|_2^2
$$

$$
\mathcal{L}_{hum} =
\operatorname{mean}_{t,d}\left\| \hat{z}_{hum} - z_{hum} \right\|_2^2
$$

joint generation 使用归一化后的 masked 分支 loss 等权合并：

$$
\mathcal{L}_{joint} =
\frac{1}{2}(\mathcal{L}_{cam} + \mathcal{L}_{hum})
$$

这样可以避免 high-dimensional human latent 在梯度上天然压过 camera latent。task sampling probability 和 loss weight 要分开处理：第一版采样等概率、loss 等权；如果 camera completion 是主要业务目标，可把 task sampling 改成 `0.5 / 0.3 / 0.2`，但架构和 loss 仍对 human/camera 一视同仁。

**实现事实（2026-06-12 核查）**：此前远端 `scripts/train_stage2_condmdi_pulp.py` 实际实现是 `element_mean`：对 target mask 中所有元素做 per-sample mean。completion task 只有单个 target branch，因此自然是分支内归一化；但 joint task 同时包含 human `128` 维与 camera `64` 维，所以有效 human:camera 权重约为 `2:1`。因此，2026-06-12 21:12 CST 之前所有 stage2 训练结果都应标注为 `joint_loss_mode=element_mean`，不能当作已验证的等分支 loss。

**修复与验证 setting**：已在远端训练脚本新增 `--joint-loss-mode`：

| Mode | 含义 | 兼容性 |
| --- | --- | --- |
| `element_mean` | 旧行为：joint 中按元素平均，human/camera 约 `2:1` | 默认值；旧实验仍可解释 |
| `branch_mean` | joint 中先算 human/camera 分支均值，再 `0.5 / 0.5` 等权 | 新验证 setting |
| `branch_sum` | joint 中 human/camera 分支均值相加 | 只保留为对照，不默认使用 |

验证记录：

| Check | 结果 |
| --- | --- |
| `py_compile` | 通过 |
| 默认 `element_mean` check | `loss=0.350090` |
| `branch_mean` check | `loss=0.357084`，同时记录 `loss_element_mean=0.350090` 与 `loss_joint_element_mean=0.298074` |
| 新 run | `gpu0_branchmean_equal_scratch_b512_82688_20260612_2112`，mixed, b512, EMA, scheduler, `task_probs=1/1/1`, `joint_loss_mode=branch_mean`，2026-06-12 21:12 CST 启动，step `900` 已有日志，仍在运行 |

可见分支一般不加 identity loss。若采样实现中可见分支会被网络输出覆盖，则每个 denoising step 后强制把 visible branch 替换回输入值；只有在数值漂移无法控制时，才加入极小权重的 visible identity loss，例如 `lambda_visible=0.01`。

curriculum 只作为触发式修复项。触发条件：

1. 某个任务的核心验证指标持续比另外两个任务差 `15%` 以上；
2. 这种差距连续 `15k` steps 没有收敛；
3. 已排除分支 loss 未归一化、projection shortcut、条件注入实现错误。

触发后可把落后任务采样概率临时提高到 `0.5`，另外两个任务各 `0.25`，训练约 `15k` steps 后线性回到 `1/3`。如果 curriculum 后仍不改善，应优先怀疑 backbone / condition fusion，而不是继续调 schedule。

必须同步记录三类审计曲线：

- per-task validation metrics：三种任务分开报，不只报总 loss；
- visible latent reliance：把可见 human/camera latent 替换为 shuffle/noise 后，性能应明显下降；
- text reliance：分别移除 human text 或 camera text，观察 completion 任务退化幅度，确认模型不是只靠双 caption 或只靠 visible branch。

## 5. 为什么连续 latent 不破坏三模式

三模式生成需要的是“可条件化的缺失分支建模”，不是离散 token 本身。

离散 token 的优势：

- mask token 天然明确；
- 预测目标是分类，训练接口简单；
- MoMask / Muddit 已证明 masked prediction 的高效性。

连续 latent 的优势：

- 不引入额外 VQ 量化误差；
- 直接复用 PulpMotion 已训练好的 human-camera-framing latent；
- camera / human / projection block 在源码里仍可切片；
- diffusion / flow / consistency model 都能自然处理连续值。

连续 latent 的代价：

- mask 语义必须显式设计；
- loss 必须处理连续值尺度；
- 条件保真度比 token 分类更难诊断；
- latent entanglement 可能降低条件可控性，但不是天然答案泄漏。

因此结论是：**连续 latent 可行，但三模式能力必须通过训练任务获得，不能由 Pulp stage1 自动继承。**

## 6. 证据账本、风险与声称边界

从本节开始，旧版分散在“风险前置”“最早失败实验”“Phase 1 记录”“当前决策”里的内容合并为一个证据账本。这里的所有训练数值都是 internal latent x0-MSE / condition-reliance / dev sampler 诊断；它们不能替代 PulpMotion official sampler metrics。

文献边界已经确认：[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]] 第 `58 / 95 / 146 / 334-335` 行指出 `(x)+DIRECTOR` / human-first camera 级联缺少反向约束和 screen-space 耦合；[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness|E.T. / Director]] 第 `67 / 87 / 126` 行支持 character-aware camera generation；[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|TSA]] 第 `85 / 115-122 / 268` 行支持 human-camera 双向交互的重要性。结论只能是：human→camera 是合理子模式，但固定 human-first 级联不是完整 StoryMotion 解法。

### 6.1 已验证证据账本

本表按验证目的排布，而不是按实验时间排布；相同目的的实验相邻放置。每条证据都标明它验证什么，以及不能证明什么。

| 验证目的                        | 证据组                           | 状态    | 关键结果                                                                                                                                          | 当前结论 / 边界                                                                                                                    |
| --------------------------- | ----------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 表示协议是否成立                    | no-proj latent protocol       | 已完成   | mixed cache: train `94,050`、val `10,549`；`z=[N,192,75]`；human/camera dims `128/64`；valid rule `ceil(num_frames / 4)`                          | MVP 表示采用 `concat([z_hum,z_cam])`；projection latent 不进入第一版 stage2                                                             |
| 表示协议是否成立                    | stage1 branch controllability | 部分完成  | cross-swap nearest-source pass rate 均为 `1.000`；self A/B MPJPE `0.1979 / 0.2511`                                                               | stage1 branch 可控；完整 oracle camera error / out-rate 仍未补齐                                                                      |
| 三任务是否能训练收敛                  | three-task element_mean pilot | 已完成   | `mixed_standard_last` test: camera `0.001405`、human `0.005222`、joint `0.051723`                                                               | 连续 latent 三任务 inpainting 可收敛；仅 internal x0-MSE，不是 official generated quality                                                 |
| 三任务是否能训练收敛                  | checkpoint selection          | 已完成   | 5-seed 4096 复评后 no-EMA 优势消失；`last.pt` 优于 `best_eval.pt`                                                                                       | `mixed_standard_last` 保留为主线 checkpoint                                                                                       |
| 条件是否被利用                     | visible-branch reliance       | 已完成   | mixed visible-shuffle delta: camera `+1.1016`，human `+1.3672`                                                                                 | completion 不是只靠 text 的均值补全；但仍是 latent reliance，不等于 generated geometry                                                        |
| Mode B 是否不是伪任务              | camera-latent causal gate     | 部分完成  | `branch_jh6ft` 4096 样本 latent gate：base human median `0.003662`；camera zero / shuffle / matched-noise median `0.216638 / 0.314891 / 0.774336` | Mode B 确实依赖整体 camera latent；但 cache 未暴露 `z_distance / z_cam_motion` 子切片，不能声称 distance 与 motion 独立贡献，也不能替代 generated geometry |
| 生成链路是否真实可解码                 | dev sampler / decode smoke    | 已完成   | completion sampler 可解码；joint text-only mode 明显退化，`50` step joint latent median `0.385576`                                                     | 说明真实 decode bridge 可用；不是 official benchmark                                                                                  |
| joint 退化来自哪里                | joint decomposition           | 已完成   | joint pred camera + GT human camera RMSE `0.117474`；GT camera + pred human MPJPE `0.139109`                                                   | joint 退化来自 human/camera 两分支共同偏离，不能归因于单一 decode 问题                                                                            |
| joint sampler 是否可用          | naive DDIM-style proxy        | 已完成诊断 | 1024 样本 joint median：`branch_jh6ft` teacher-forced `0.016472`，1-step `0.292046`，20-step `0.617884`，50-step `0.740053`                         | naive multi-step sampler 随步数退化；当前不能把训练 x0-MSE 改善写成可生成质量改善                                                                    |
| 指标是否稳健                      | robust / outlier audit        | 已完成诊断 | camera median `0.000602`、human median `0.003603`、joint median `0.021433`；per-sample loss 与 latent norm 强相关：`corr_z_sq_mean` camera / human / joint 为 `0.975 / 0.960 / 0.964`；个别 slice 出现 camera max `297`、human max `2160`、joint max `1551` | mean 不能作为主结论；需先审计 high-magnitude latent 是数据异常、合法极端镜头、stage1 encode/normalization 问题，还是训推分布不匹配 |
| loss 口径是否影响结论               | loss normalization readout    | 已完成   | same-seed `element_equal` vs `branch_equal` joint median `0.019149 / 0.019239`；`branch_jh6ft` joint median `0.018638`、p99 `0.483041`          | `branch_mean` 没有决定性优势；`branch_jh6ft` 只作为候选 checkpoint，不能替代 sampler / official bridge                                         |
| 是否可与 PulpMotion official 比较 | StoryMotion generated eval + Pulp callbacks | 已完成，需审计 | 6 个 full jobs 均为 `exit:0`，每项 `10549` records，无 NaN；`branch_jh6ft` joint: `r_fpd 0.450`、Out-rate `7.48%`、TMR `18.72`、CLaTr `23.70`、caption F1 `0.284` | 只能称为 StoryMotion generated eval with Pulp official callbacks；joint framing 强但 semantic alignment 弱，不能写全面优于 PulpMotion |


旧离散 token 方案降级为 ablation / 备选路线。它的 mask pattern 思路保留，但“必须统一离散 vocabulary”不是当前主线；连续 latent 的核心条件是显式 branch mask / inpainting 训练，而不是 Pulp stage1 自动继承三模式能力。

### 6.2 当前风险判断

核心风险不再是“continuous latent 是否能训练”，而是以下五点：

1. **branch_mean 证据不足风险**：same-seed readout 后，`branch_mean` 与 `element_mean` 在 median / tail / reliance 上差异很小；`branch_jh6ft` 只在 joint tail 上略好，不能作为继续长训的充分理由。
2. **official metrics 命名风险**：StoryMotion full generated eval 已经跑通 Pulp official callbacks，但采样器仍是 StoryMotion custom deterministic DDIM START_X；不能称为 Pulp official sampler，也不能把 completion 与 Pulp joint baseline 混表。
3. **semantic alignment 风险**：joint framing / projection 指标明显优于 Pulp no-Aux，但 TMR、CLaTr、caption F1 全部低于 Pulp。当前问题从“能否进入 evaluator”转为“为什么几何强、语义弱”。
4. **sampler / diversity 风险**：deterministic DDIM `eta=0` 可能过度压缩生成多样性，造成高 framing、低文本覆盖；必须做 empty/random text、noise / eta、DDPM 或 schedule 消融后再判断模型能力。
5. **tail 与格式口径风险**：full eval 仍需按 sample_id 做 visualization / outlier audit，并检查 StoryMotion raw output 是否完全匹配 Pulp TMR / CLaTr / captions evaluator 的骨架、尺度和时长预期。

### 6.3 声称边界

不能写：

- “我们的方法全面优于 PulpMotion”。当前只支持 joint framing / outscreen 在本采样设定下优于 5090 Pulp no-Aux；语义对齐仍弱于 Pulp。
- “解决了 human-camera 双向约束”。branch-mask continuous inpainting 能学习条件补全，但尚未显式引入 TSA-style bidirectional interaction block。
- “Evaluation Contract 已完成”。它只是待满足的 paper-level contract。
- “text + camera 可以确定性反演 human”。这个任务天然一对多，只能生成与 camera / text 相容的 plausible human motion。
- “连续 latent 天然支持三模式”。三模式能力来自 stage2 branch-mask 训练。
- “`branch_mean` 明确优于 `element_mean`”。当前 same-seed 与 full-eval 证据只支持二者接近，不能支持优势声称。
- “已证明 `z_distance` 与 `z_cam_motion` 分别被利用”。当前 gate 只干预整体 camera latent block。
- “成功复现了 PulpMotion 全部指标”。当前 `cfg_rate_z=0` 只是 no-Aux 数值接近；`r_fpd` 仍有约 `+5.1%` gap，且 Aux 未复现。
- “`cfg_rate_z=2` 是 PulpMotion Aux baseline”。`dit_xy` 配置的 projection latent dim 为 `0`，训练 loss `do_projection:false`；该设置只是 no-Aux checkpoint 上的 inference-only projection CFG probe。
- “StoryMotion 使用了 Pulp official sampler”。本次 StoryMotion full eval 只使用 Pulp official metric callbacks，采样器是自定义 deterministic DDIM START_X。
- “completion 指标可以直接和 Pulp joint baseline 比”。completion 是 conditional inpainting task，Pulp no-Aux baseline 表只用于 joint generation 对照。

可以写：

- “基于 PulpMotion 可切片连续 latent 的三模式 branch-conditioned continuous inpainting 框架。”
- “在不引入 VQ 量化误差的前提下，复用 PulpMotion human/camera continuous latent 作为 stage2 生成空间。”
- “当前 generated eval 支持 completion mode 可运行且两个 checkpoint 表现接近；joint generation 中 `branch_jh6ft` 比 `mixed_standard_last` 更适合作为下一轮候选。”
- “Mode B 在 latent-level gate 下依赖 camera condition；但 distance / motion 分解、cycle consistency 与 generated geometry 仍未完成。”
- “PulpMotion no-Aux official checkpoint 在本地 5090 环境下的 rerun 与论文 no-Aux 数值接近，但仍需 split hash、metric implementation 和随机性审计后才能称为严格复现。”
- “No-Aux checkpoint + inference-only projection CFG (`cfg_rate_z=2.0`) 降低 outscreen，但显著损害 TMR / CLaTr / caption F1；它是反例式 probe，不是 Aux reproduction。”
- “在 joint generation 无 observed human/camera branch 的设定下，StoryMotion `branch_jh6ft` 的 framing 指标强于 5090 Pulp no-Aux，但 TMR / CLaTr / caption F1 明显更弱；该结果指向 text-conditioning / sampler diversity / output-format audit，而不是直接长训。”

## 7. Evaluation Contract（部分满足）

本节是 official / paper-level evaluation contract，不等于已经获得可对外宣称的 paper-level StoryMotion 指标。PulpMotion official evaluator 不是缺失状态：远端 PulpMotion 有 `camera_metrics.py`、`human_metrics.py`、`joint_metrics.py` 和 Hydra `evaluate.py`。2026-06-13 新增的 `storymotion_official_bridge_smoke.py` 已经完成最小 raw callback contract smoke：StoryMotion stage2 latent 可以通过 Pulp autoencoder / dataset 解码成 callbacks 期望的 `raw_input`、`raw_output`、`x_output`，并在 camera / human / joint 三模式上通过 key / shape 检查。随后已从 PulpMotion 官方 HuggingFace repo 补齐 CLaTr/TMR checkpoint layout 与 PyTorch3D runtime dependency；32-sample callback smoke 证明 camera / human / joint official callbacks 能加载 checkpoint，并分别输出 `test/clatr/*`、`test/tmr/*` 与 `test/proj/*` keys。2026-06-13 进一步完成 full generated eval，但它仍是 StoryMotion custom sampler + Pulp official callbacks，不是 Pulp official sampler。

这次 5090 PulpMotion official baseline rerun 与前期 4090 评估不是同一性质。前期 4090/本地结果主要服务于 StoryMotion stage2 diagnostics、callback bridge、small-sample smoke 和实现排障；本次 5090 run 的目标是用 PulpMotion official checkpoint、official config / sampler / callbacks 在 full mixed test split 上建立对照基线。它回答“我们的 evaluator / data / checkpoint 是否能接近论文 Pulp no-Aux 数值”，不回答“StoryMotion 是否优于 PulpMotion”。

三模式保持不变，但 Mode B 的 `camera` 必须按 Pulp-v0 data representation 定义为 relative framing condition，而不是独立世界相机轨迹。

### 7.1 PulpMotion official baseline alignment（5090, 2026-06-13）

5090 full jobs 已完成且 marker 为 `exit:0`。checkpoint 为官方 HuggingFace 文件 `runs/dit-xy-ddpm-4dlbunha-330750.ckpt`，远端 sha256 为 `a7e6b65cc1a81eaaec946fd30bf950f06ee7ec2a5accf713f88ce4fccae075a2`，`load_state_dict` 为 `missing=[] / unexpected=[]`，global step 为 `330750`。配置为 `config_dit_xy`、full mixed test split `10549 / 10549`、`num_steps=50`、`cfg_rate_c=11.0`。

下表只用于 no-Aux baseline preliminary alignment，不是 StoryMotion main result，也不是 Aux reproduction 表。

| 对照 | 设置 | Samples | `r_fpd` ↓ | Out-rate ↓ | TMR ↑ | CLaTr ↑ | Caption F1 ↑ | 判读 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Paper DiT `(x,y)` no-Aux | paper table | - | `4.90` | `25.98%` | `23.50` | `30.75` | - | 论文 no-Aux 对照 |
| 5090 rerun no-Aux | `cfg_rate_c=11.0`, `cfg_rate_z=0.0` | `10549` | `5.15` | `26.59%` | `23.36` | `31.31` | `0.350` | 数值接近，但 `r_fpd` 相对论文约 `+5.1%`；只能称 alignment preliminary check |

论文 Aux 表值 `FD_framing=3.37`、Out-rate `16.76%`、TMR `25.05`、CLaTr `32.81` 当前没有复现。它们不和下面的 probe 混表，因为下面的 probe 不是训练得到的 Aux 模型。

Inference-only projection CFG probe on no-Aux checkpoint（not comparable to paper Aux）：

| Probe | 设置 | Samples | `r_fpd` ↓ | Out-rate ↓ | TMR ↑ | CLaTr ↑ | Caption F1 ↑ | 判读 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 5090 probe | no-Aux checkpoint + inference-only projection CFG, `cfg_rate_z=2.0` | `10549` | `5.57` | `9.38%` | `22.11` | `15.15` | `0.162` | 不是 Aux baseline；outscreen 下降但文本/人体/语义指标显著退化 |

关键解释：

1. `config_dit_xy` 使用 `dit_xy_ddpm`，autoencoder projection latent dim 为 `0`，`do_projection:false`；`cfg_rate_z` 在 sampler 中只是推理期投影梯度项，不等价于训练了 projection / Aux 变量的模型。
2. `cfg_rate_z=0` 与论文 no-Aux 的 TMR / CLaTr / Out-rate 接近，但 `r_fpd` 仍有约 `+5.1%` gap。按 DeepSeek Max 审计意见，不能写“复现成功”，只能写“数值初步吻合，待 split hash、metric implementation、seed 方差审计”。
3. `cfg_rate_z=2` 必须命名为 `PulpMotion-NoAux official checkpoint + inference-only projection CFG (cfg_rate_z=2.0)`。它可以作为投影引导副作用的反例 probe，不能作为 PulpMotion Aux baseline、不能与 StoryMotion 主结果并列。
4. `cfg_rate_z=2` 的 outscreen 下降伴随 TMR / CLaTr / caption F1 明显退化，符合无对应训练条件的 CFG 扭曲语义空间的风险；它从侧面说明该 no-Aux checkpoint 行为不能代表 Aux 算法能力。
5. StoryMotion full generated eval 已完成；当前 blocker 从 evaluator 缺失转为 text-conditioning、sampler diversity、output-format 与 visualization / outlier audit。

### 7.2 StoryMotion generated eval with Pulp callbacks（5090, 2026-06-13）

本节是 **StoryMotion generated eval with PulpMotion official metric callbacks**，不是 Pulp official sampler。脚本为 `scripts/storymotion_official_full_eval.py`，远端输出在：

```text
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/storymotion_official_full_eval_20260613/
```

执行状态：

1. 6 个 full jobs 全部 `exit:0`。
2. 每项 `evaluated_samples=10549`，对应 `records.jsonl` 均为 `10549` 行。
3. camera / human / joint 分别输出 `13 / 10 / 31` 个 metric keys。
4. 所有数值检查无 NaN。
5. sampler 为 deterministic DDIM START_X，`num_steps=50`，`eta=0`，每样本 deterministic noise seed；completion 模式每步对 observed branch 与 padding frames 走 `q(z_gt,t,noise)`，模型 forward 内部按训练口径用 clean `obs_x0` 替换 observed positions；joint 模式没有 observed human/camera branch，只回填 padding invalid frames。

Completion 只做 StoryMotion checkpoint 内部比较，不能与 Pulp joint baseline 混表：

| Run | Step | Camera CLaTr ↑ | Camera FCD ↓ | Camera caption F1 ↑ | Human TMR ↑ | Human FTD ↓ | Human precision / recall ↑ | 判读 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `mixed_standard_last` | `82688` | `53.54` | `14.99` | `0.622` | `18.20` | `126.81` | `0.803 / 0.931` | completion 稳定基准 |
| `branch_jh6ft` | `102688` | `53.29` | `15.91` | `0.619` | `18.19` | `126.24` | `0.803 / 0.931` | completion 基本打平；没有明显收益，也没有明显退化 |

Joint generation 可与 5090 Pulp no-Aux baseline 做受限横向比较；限制是 StoryMotion 采样器不同，不是 Pulp official sampler：

| Run | Step | `r_fpd` ↓ | Out-rate ↓ | TMR ↑ | CLaTr ↑ | Caption F1 ↑ | 判读 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 5090 Pulp no-Aux rerun | `330750` | `5.15` | `26.59%` | `23.36` | `31.31` | `0.350` | Pulp official checkpoint + Pulp sampler/callbacks |
| `mixed_standard_last` | `82688` | `0.545` | `8.34%` | `18.65` | `20.74` | `0.252` | framing 强于 Pulp，但语义明显弱 |
| `branch_jh6ft` | `102688` | `0.450` | `7.48%` | `18.72` | `23.70` | `0.284` | 当前 joint 候选；比 `mixed_standard_last` 更好，但仍不是全面优于 Pulp |

关键结论：

1. **Completion 已可进入 official callbacks 口径**：两个 checkpoint 在 Mode A / B 上几乎打平，`branch_jh6ft` 没有破坏 completion，但也没有给出决定性 completion 收益。
2. **Joint 上保留 `branch_jh6ft`**：相对 `mixed_standard_last`，`branch_jh6ft` 改善 `r_fpd`、Out-rate、CLaTr 与 caption F1，TMR 小幅改善。
3. **不能写全面优于 PulpMotion**：StoryMotion joint 的 framing / outscreen 很强，但 TMR、CLaTr、caption F1 均低于 5090 Pulp no-Aux。
4. **异常模式是“几何强、语义弱”**：由于 joint 模式没有 observed branch，不能把 joint framing 优势简单归因于 observed-branch oracle。更可能的风险是 deterministic sampler / diversity collapse、text condition 利用不足、output-format 与 evaluator 口径、或 StoryMotion 学到强构图 prior 但语义耦合不足。
5. **下一步不是继续长训**：必须先做 empty / random text 诊断、sampler noise / eta / DDPM 消融、格式对齐检查、paired visualization 与 outlier audit。

| 模式                        | 输入条件定义                                                                                                                   | 要回答的问题                                                     | official / screen-space 指标                                                                                                                     | 当前 blocker                                                                      |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| A: human + text -> camera | 给定 `z_hum`、human text、camera text                                                                                        | 生成相机是否真的拍摄给定 human                                         | out-rate、projected joint center error、subject scale、relative distance / heading、camera jerk、CLaTr camera-text alignment、visible-human reliance | full callback metrics 已通；还缺 paired geometry visualization / outlier audit |
| B: camera + text -> human | 给定 `z_cam = [z_distance,z_cam_motion]`、human text、camera text；`z_distance` 是 camera-to-subject relative framing envelope | 生成 human 是否与给定 framing / camera motion 相容，而不是唯一反演 GT human | human quality / diversity、root-camera consistency、distance distribution match、condition sensitivity、TMR metrics                                | full callback metrics 已通；还缺 component perturbation gate、generated geometry 与 diversity |
| C: text -> human + camera | 给定 human text、camera text，无 visible latent                                                                               | 联合生成是否接近或超过 PulpMotion baseline                            | FDframing、Out-rate、TMR-Score、CLaTr-Score、human quality、camera quality、triadic consistency                                                      | full metrics 已通；关键 blocker 转为 text-conditioning、sampler diversity、output-format audit |

Mode B 的方法候选写法：Pulp-v0 复用现有 relative camera latent，把 camera condition 拆成 `z_distance` 与 `z_cam_motion`，学习 `p(z_hum | z_distance, z_cam_motion, text)`。Pulp decode contract 中 `camera_world = decoded_human_root + decoded_distance` 只作为 human-camera 一致性的内部契约和 cycle check；纯 Mode B 推理输出是 plausible human latent，不要求唯一匹配某个 GT human。

Mode B 的必过 gate：

1. **Distance shuffle**：固定 text 与 `z_cam_motion`，shuffle `z_distance` 后生成 human root / geometry 必须显著变化，用于排除纯 text shortcut。
2. **Distance zero-out**：置零 `z_distance`，观察输出是否退化到不同的 framing 分布，用于测试 relative envelope 是否真的被使用。
3. **Camera-motion shuffle**：固定 `z_distance`，shuffle FOV / rotation / velocity 条件，用于区分模型是否只看 relative distance。
4. **Cycle consistency**：Mode B 生成 human 后，再用 human->camera 或 Pulp contract 检查输入 framing 是否可恢复；这只是诊断，不作为 main metric。
5. **Generated geometry**：报告 generated samples 的 projection coverage、relative distance / heading、subject scale、out-rate，与 text-only baseline 和 camera-shuffle baseline 对比。

当前完成 / 未完成拆分：

1. **已完成**：latent data/order/mask contract；internal latent diagnostics；raw callback key/shape contract smoke。
2. **已完成 callback smoke**：CLaTr/TMR checkpoint layout 与 PyTorch3D dependency 已补齐；`mixed_standard_metric_smoke_pytorch3d.json` 中 camera 输出 `13` 个 `test/clatr/*` / captions keys，human 输出 `10` 个 `test/tmr/*` keys，joint 输出 `31` 个 keys，包含 `test/proj/*`、`test/clatr/*` 与 `test/tmr/*`。
3. **已完成 Pulp baseline rerun**：PulpMotion official no-Aux checkpoint 在 5090 full mixed split 上已跑完 `cfg_rate_z=0.0` 与 `cfg_rate_z=2.0` 两个设置；前者是 no-Aux alignment preliminary check，后者是 inference-only projection CFG probe。
4. **未完成 Pulp strict alignment**：还缺 split sample-id hash、metric implementation audit、seed / stochasticity 方差审计；因此 no-Aux 只能写“数值接近”，不能写“严格复现”。
5. **已完成 StoryMotion full generated eval**：6 个 full jobs 均为 `exit:0`，每项 `10549` records；但采样器是 StoryMotion deterministic DDIM，不是 Pulp official sampler，结果仍需 text / sampler / format / outlier 审计后才可对外宣称。
6. **未完成 Aux reproduction**：`cfg_rate_z=2.0` run 不是 PulpMotion paper Aux，不允许进入 Aux baseline 表。

paper-level 完成标准更新为四项：

1. `official_metric_bridge` 能在同一 generated sample set 上输出 CLaTr、TMR、projection / outscreen、segment F1 指标。
2. `official_sampler_records` 为每条样本保留 prompt、source id、mode、seed、checkpoint、loss mode、raw output path。
3. `baseline_alignment` 同口径列出 PulpMotion Table 4 / Table 8 可比较项；禁止把 x0-MSE、32-sample smoke、Pulp no-Aux preliminary check 与 StoryMotion full generated official metrics 混表。
4. `pulp_alignment_audit` 至少给出 split sample ids / hash、checkpoint sha、official config、sampler CFG 公式、seed 方差或重复 run 说明。若审计未完成，所有 Pulp rerun 数值标注为 alignment provisional。

公平对比锁定协议：

1. **同一评测集合**：所有 checkpoint / sampler / loss 对比必须使用同一个 split、同一批 sample ids、同 prompts、同 tokenizer / Pulp dataset / stage1 autoencoder、同有效帧 mask。
2. **同一生成预算**：除非该 gate 专门研究 sampler budget，否则固定 sampler 类型、step 数、timestep schedule、CFG / condition strength、batch size、seed list 和 postprocess。
3. **同一 evaluator**：所有 official 数值必须来自同一 Pulp callback / config / checkpoint / PyTorch3D 环境；不能把 32-sample smoke 数值、latent MSE 和 full-split official metrics 混在一张主表里。
4. **一次只改一个变量**：checkpoint 对比时固定 sampler；sampler 对比时固定 checkpoint；loss / task-prob 对比时固定训练预算、seed 规则和 eval set。若历史 run 不能满足同口径，只能标为 exploratory，不作为主结论。
5. **成对报告**：正式表优先报告 paired delta、median / p95 / p99、bootstrap CI 或 seed 方差；mean 只作为附录，并必须同时列出 tail / outlier audit。
6. **命名不偷换**：`cfg_rate_z=2.0` 在 `dit_xy` no-Aux checkpoint 上只能称为 inference-only projection CFG probe；只有使用论文 Aux 对应 checkpoint / config / training objective 并通过同口径审计后，才允许称为 Aux baseline。


## 8. 高优先级实验队列

本节是唯一的优先实验表。已完成训练用于解释当前证据；后续 planned tasks 必须被 gates 约束，不能继续无边界堆长训。

### 8.1 Element-Mean 训练矩阵：目标是验证三任务混合训练是否必要

目标：判断 continuous latent stage2 是否必须同时保留 camera completion、human completion 和 joint generation 三种任务。简单结论：必须保留 completion task；`joint-only` 会毁掉 A/B 两个核心模式，`mixed_standard_last` 是当前最稳基准。所有下表结果使用旧 `joint_loss_mode=element_mean`，即 joint task 对 human/camera 按元素平均，human:camera 权重约 `2:1`。这些是 internal latent x0-MSE，不是 official generated quality。

| Run | 初始化 | Task probs | Final step | Test camera | Test human | Test joint | 结论 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `mixed_standard_last` | scratch baseline | `1 / 1 / 1` | `82,688` | `0.001405` | `0.005222` | `0.051723` | completion 稳定基准；full generated eval 已完成，仍需 semantic audit |
| `jointonly_scratch` | scratch | `0 / 0 / 1` | `82,688` | `0.443160` | `0.208769` | `0.045091` | 只训练 joint 会毁掉 completion；不能作为三模式主线 |
| `jointheavy4_scratch` | scratch | `1 / 1 / 4` | `82,688` | `0.002779` | `0.010546` | `0.050005` | 保留 completion task 时 joint-heavy 不会崩 |
| `jointheavy6_ft` | resume `mixed_standard_last` | `1 / 1 / 6` | `102,688` | `0.001468` | `0.005230` | `0.047894` | joint-heavy finetune 保留 completion 量级，joint x0 略优 |
| `jointonly_ft` | resume `mixed_standard_last` | `0 / 0 / 1` | `102,688` | `0.007360` | `0.019352` | `0.047883` | joint-only finetune 有遗忘；不应去掉 completion regularization |

### 8.2 Branch-Mean / Joint-Heavy 矩阵：目标是验证是否值得继续长训

目标：检验 `branch_mean` loss 和 joint-heavy task sampling 是否能带来足够强的 joint 改善，同时不破坏 completion。简单结论：`branch_jh6ft` 的 one-step joint x0 最好；在 2026-06-13 full generated eval 中，它也成为当前 joint 候选，但仍不能支持继续长训，因为语义指标低于 Pulp no-Aux。2026-06-12 21:54 CST 后的四卡矩阵已完成。GPU1 原 `branchmean_equal_seed42_scratch` 启动后被 DeepSeek 审核判定为低优先级随机复现，已在早期停止并保留日志；GPU1 改跑同 seed fair baseline。下表仍是 internal latent x0-MSE，不是 generated quality。

| Run | 初始化 | Task probs | Loss mode | Test camera | Test human | Test joint | 结论 |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| `element_equal_seed41` | scratch | `1 / 1 / 1` | `element_mean` | `0.001512` | `0.005331` | `0.047632` | same-seed fair baseline |
| `branch_equal_seed41` | scratch | `1 / 1 / 1` | `branch_mean` | `0.001475` | `0.005266` | `0.046112` | one-step x0 略优，但 full-eval median / tail 没有决定性优势 |
| `element_jh4_old` | scratch | `1 / 1 / 4` | `element_mean` | `0.002779` | `0.010546` | `0.050005` | joint-heavy scratch 会牺牲 completion |
| `branch_jh4_seed43` | scratch | `1 / 1 / 4` | `branch_mean` | `0.002409` | `0.010489` | `0.045719` | 比旧 jh4 更好，但仍有 completion 代价 |
| `element_jh6ft_old` | resume `mixed_standard_last` | `1 / 1 / 6` | `element_mean` | `0.001468` | `0.005230` | `0.047894` | finetune 保持 completion |
| `branch_jh6ft_seed44` | resume `mixed_standard_last` | `1 / 1 / 6` | `branch_mean` | `0.001442` | `0.005248` | `0.038759` | one-step joint x0 最好；但 sampler proxy 未传导，不能作为继续长训依据 |

### 8.3 2026-06-13 Gated Diagnostics：目标是验证条件依赖、sampler 退化和 official bridge 层级

目标：回答四个决策问题：Mode B 是否真依赖 camera latent、`branch_mean` 是否值得升级为主线、StoryMotion 输出是否能进入 Pulp official evaluator、PulpMotion official baseline 是否可作为公平对照。简单结论：Mode B 依赖整体 camera latent；teacher-forced `0.016472` 是训练分布单步 x0 重建，不是 official metric；raw bridge、official callback smoke 和 full generated eval 均已打通；Pulp no-Aux official checkpoint full rerun 已完成但仍是 alignment provisional；StoryMotion 当前最大问题是 joint framing 强但 semantic alignment 弱。三项 latent diagnostics 已在 5090 GPU0-2 并行完成，输出在 `remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2_gated_diag_20260613/`。评估脚本为 `remote 5090: /data/public/ripemangobox/Motion/StoryMotion/scripts/storymotion_stage2_gated_eval.py`。official bridge smoke 脚本为 `remote 5090: /data/public/ripemangobox/Motion/StoryMotion/scripts/storymotion_official_bridge_smoke.py`，输出在 `remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2_official_bridge_smoke_20260613/`。Pulp official baseline rerun 脚本为 `scripts/pulpmotion_official_baseline_eval.py`，远端输出在 `remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_official_baseline_20260613/`。StoryMotion full generated eval 脚本为 `scripts/storymotion_official_full_eval.py`，远端输出在 `remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/storymotion_official_full_eval_20260613/`。

| Gate | 运行内容 | 关键结果 | 决策 |
| --- | --- | --- | --- |
| G0 `branchmean_readout` | `element_equal` / `branch_equal` / `branch_jh6ft` 4096 样本 median / p95 / p99 / visible-shuffle | `element_equal` joint median / p99 `0.019149 / 0.530845`；`branch_equal` `0.019239 / 0.510605`；`branch_jh6ft` `0.018638 / 0.483041` | `branch_mean` 只有弱趋势，不能声称优于 `element_mean`；`branch_jh6ft` 保留为候选 checkpoint |
| G2 `camera_to_human_rep_gate` | `branch_jh6ft` Mode B human completion，整体 camera latent zero / shuffle / matched-noise | base human median `0.003662`；zero `0.216638`；shuffle `0.314891`；matched-noise `0.774336` | Mode B 确实依赖 camera latent；但未分解 `z_distance / z_cam_motion`，也不是 generated geometry |
| G3 `joint_sampler_reeval` | `mixed_standard` / `element_jh6ft` / `branch_jh6ft` 的 teacher-forced x0 与 1 / 20 / 50 step DDIM-style proxy | `branch_jh6ft` teacher median `0.016472`，1-step `0.292046`，20-step `0.617884`，50-step `0.740053` | `0.016472` 只表示 training-distribution 单步 x0 denoising，不是 official metric；naive multi-step sampler 退化，优先修 sampler dynamics |
| G4 `official_bridge_smoke` | `mixed_standard_last` StoryMotion latent → Pulp autoencoder / dataset → official callbacks | raw key / shape OK；官方 CLaTr/TMR checkpoint 与 PyTorch3D 已补齐；32-sample `--run-metrics` 产出 camera `13` keys、human `10` keys、joint `31` keys，joint keys 含 `test/proj/*` | official callback smoke 已通；已升级到 full generated eval |
| G5 `pulp_official_baseline_rerun` | Pulp official `dit_xy` checkpoint, full mixed test split, `cfg_rate_c=11.0`, `cfg_rate_z=0.0 / 2.0` | no-Aux rerun: `r_fpd=5.15`, Out-rate `26.59%`, TMR `23.36`, CLaTr `31.31`；projection CFG probe: `r_fpd=5.57`, Out-rate `9.38%`, TMR `22.11`, CLaTr `15.15` | no-Aux 数值接近但 strict alignment 未完成；`cfg_rate_z=2.0` 不是 Aux baseline，只能作为 inference-only projection CFG probe |
| G6 `storymotion_full_generated_eval` | `mixed_standard_last` / `branch_jh6ft` 三模式 full split，StoryMotion DDIM sampler + Pulp callbacks | 6 jobs `exit:0`；`branch_jh6ft` joint: `r_fpd 0.450`、Out-rate `7.48%`、TMR `18.72`、CLaTr `23.70`、caption F1 `0.284` | `branch_jh6ft` 保留为 joint 候选；下一步查 text-conditioning / sampler diversity / format / outlier |

`teacher-forced 0.016472` 的准确含义：它来自自定义诊断脚本 `storymotion_stage2_gated_eval.py` 的 `run_joint_sampler()`，不是 PulpMotion official evaluator，也不是 CondMDI 官方自带指标。具体实现是对真实 latent `z` 随机采样 timestep 与 noise，执行 `x_t = q_sample(z,t,noise)`，调用同一个 stage2 模型单步预测 `x0`，再对 `pred_x0` 与真实 `z` 计算 latent branch MSE。它属于训练分布上的 denoising readout，不是 decoded generated quality，也不是 multi-step generation。

teacher-forced 远好于旧 1 / 20 / 50 step proxy 的原因：teacher-forced 输入仍然由真实 `z` 加噪得到，状态在训练分布上；旧 naive sampler 从纯高斯噪声开始，且 joint 模式下 `obs_x0=0`、`obs_mask=0`，每一步都把模型预测误差重新注入下一步。这个历史诊断不能草率归因于“训练失败”或“数据坏”，更精确地说是 **train-time one-step x0 objective 与 inference-time recursive sampler 之间存在 mismatch**。2026-06-13 新增的 `storymotion_official_full_eval.py` 已用 deterministic DDIM START_X 与 Pulp callbacks 跑完整 split；当前 blocker 不再是“能否生成 full records”，而是几何强、语义弱的 text-conditioning / sampler diversity / output-format 根因。

下一步 gated task 重新排序：

| Gate | 触发条件                       | 任务                               | 完成标准                                                                                                                                                                        |
| ---- | -------------------------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| G1   | 已完成                        | `official_callback_smoke`        | CLaTr/TMR checkpoint layout 与 PyTorch3D 已补齐；小样本 `--run-metrics` 输出 camera `test/clatr/*`、human `test/tmr/*`、joint `test/proj/*`；只作为 callback smoke，不报告正式数值 |
| G1b  | 已完成，待审计                   | `pulp_official_baseline_rerun`   | full mixed split `10549 / 10549`、marker `exit:0`、checkpoint sha / load state 记录完整；no-Aux 只标 alignment provisional，`cfg_rate_z=2.0` 不标 Aux |
| G2   | 现在并行做                      | `pulp_alignment_audit`           | 固定 Pulp official checkpoint，补 split sample-id hash、metric implementation 口径、CFG 公式、至少 seed / stochasticity 说明；若 `r_fpd` gap 无法解释，baseline 表必须继续标 provisional |
| G3   | 已完成                        | `storymotion_full_generated_eval` | 6 个 full jobs 均为 `exit:0`，每项 `10549` records；结果只称 StoryMotion generated eval with Pulp callbacks |
| G4   | 现在立即做                      | `text_conditioning_diagnosis`    | 固定 `branch_jh6ft` joint，同 sample ids / sampler / seed，对 empty text、random text / shuffled text embedding 与原始文本比较 TMR、CLaTr、caption F1、framing |
| G5   | G4 后并行做                    | `sampler_diversity_probe`        | 固定 `branch_jh6ft` joint，扫描 eta / DDPM-like noise / timestep grid，观察 `r_fpd`、Out-rate、TMR、CLaTr、caption F1 的 Pareto trade-off |
| G6   | G4 / G5 后                   | `output_format_audit`            | 抽样检查 raw human/camera、骨架尺度、padding、有效帧、Pulp TMR/CLaTr/captions evaluator 输入口径，排除格式导致的语义低估 |
| G7   | Mode B 要进入方法 claim         | `camera_to_human_component_gate` | 在 raw adapter 或 tokenizer metadata 暴露子切片后，分别做 distance shuffle、distance zero-out、camera-motion shuffle、cycle consistency、generated geometry |
| G8   | human→camera 需要证明 geometry | `paired_geometry_eval`           | standard / branch_mean / text-only / visible-shuffle 的 projected center、out-rate、scale、relative pose 对比 |
| G9   | 解释 geometry / semantic 分裂   | `outlier_visual_audit`           | 各抽取 good framing / bad caption / high outscreen / random 样本可视化，判断是否 oversmooth、冻结、文本错配或 evaluator artifact |

证据路径：

```text
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/stage2_completed_summary_20260612.md
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/runs/eval/stage2_posthoc_mixed_20260612/summary.json
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/runs/eval/stage2_multiseed_mixed_20260612/
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/runs/eval/stage2_mixed_condition_reliance_20260612/
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/runs/eval/stage2_per_sample_stats_20260612/
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/runs/eval/stage2_outlier_audit_fullval_20260612/
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/runs/eval/stage2_trimodal_latent_render_20260612/
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/runs/eval/stage2_decode_render_smoke_20260612/
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/runs/eval/stage2_sampler_decode_smoke_20260612/
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/runs/eval/stage2_sampler_decode_stress_20260612/
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/runs/eval/stage2_joint_decomposition_20260612/
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/pulp_official_full_mixed_20260611/
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2_gated_diag_20260613/
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2_official_bridge_smoke_20260613/
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2_official_bridge_smoke_20260613/mixed_standard_metric_smoke.json
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2_official_bridge_smoke_20260613/mixed_standard_metric_smoke_pytorch3d.json
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2_official_eval_20260613/pytorch3d_install.log
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_official_baseline_20260613/dit_xy_mixed_wz0_wc11_full.json
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_official_baseline_20260613/dit_xy_mixed_wz2_wc11_full.json
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_official_baseline_20260613/logs/
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/storymotion_official_full_eval_20260613/
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/storymotion_official_full_eval_20260613/mixed_standard_last_camera_full.json
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/storymotion_official_full_eval_20260613/mixed_standard_last_human_full.json
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/storymotion_official_full_eval_20260613/mixed_standard_last_joint_full.json
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/storymotion_official_full_eval_20260613/branch_jh6ft_camera_full.json
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/storymotion_official_full_eval_20260613/branch_jh6ft_human_full.json
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/storymotion_official_full_eval_20260613/branch_jh6ft_joint_full.json
remote 5090: /data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models/runs/dit-xy-ddpm-4dlbunha-330750.ckpt
scripts/pulpmotion_official_baseline_eval.py
scripts/storymotion_official_full_eval.py
scripts/run_storymotion_official_full_eval_5090.sh
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/scripts/train_stage2_condmdi_pulp.py
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/scripts/storymotion_stage2_gated_eval.py
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/scripts/storymotion_official_bridge_smoke.py
remote 5090: /data/public/ripemangobox/Motion/PulpMotion/src/callbacks/{camera_metrics.py,human_metrics.py,joint_metrics.py}
```

## 9. 决策逻辑与停止条件

当前主线仍是 continuous latent stage2。`mixed_standard_last` 保留为 completion 稳定基准；`branch_jh6ft` 升级为当前 joint generation 候选。原因是：PulpMotion stage1 已提供可切片 human/camera continuous latent；no-proj 协议和 cross-swap 审计支持表示可控；三任务 mixed pilot 已收敛；visible reliance 与 Mode B gate 排除了“只靠 text”的主要失败模式；2026-06-13 full generated eval 显示 `branch_jh6ft` 在 joint `r_fpd / outscreen / CLaTr / caption F1` 上优于 `mixed_standard_last`，且 completion 未明显退化。但它的 TMR、CLaTr、caption F1 仍低于 5090 Pulp no-Aux joint baseline。当前 bottleneck 不是 evaluator 或 full records，而是 text-conditioning、sampler diversity、output-format consistency、visualization / outlier audit 和 Pulp baseline strict alignment。

决策 gates：

1. **暂不继续长训**：full eval 已暴露“几何强、语义弱”的主要矛盾；继续长训前必须先定位 text-conditioning / sampler / format 根因。
2. **保留 `mixed_standard_last` 为 completion 基准**：它的 Mode A/B 指标与 `branch_jh6ft` 基本持平，证据最完整。
3. **保留 `branch_jh6ft` 为 joint 候选**：它在 full generated eval 中 joint `r_fpd`、Out-rate、CLaTr、caption F1 均优于 `mixed_standard_last`，但不能写全面优于 Pulp。
4. **Mode B 继续保留**：整体 camera latent zero / shuffle / noise 会显著拉高 human prediction loss，说明 `camera + text -> human` 不是纯 text shortcut；但 distance / motion component gate、cycle consistency 与 generated geometry 仍未完成。
5. **Pulp baseline 只作 provisional 对照**：`cfg_rate_z=0.0` full rerun 接近论文 no-Aux，但不能写严格复现；`cfg_rate_z=2.0` 是 no-Aux checkpoint 的 inference-only projection CFG probe，不能叫 Aux baseline。
6. **先诊断 semantic gap，再决定训练**：优先跑 empty/random/shuffled text、sampler eta/noise、format audit、visual audit；若 text condition 确认弱，再改训练目标或 conditioning，而不是堆步数。
7. **公平性优先于跑更多实验**：后续主表必须锁定 split、sample ids、prompts、seeds、sampler、生成预算、Pulp evaluator 和 postprocess；任何额外变量变化都单独开 gate，不和 checkpoint / loss 结论混在一起。

停止条件：

1. `text_conditioning_diagnosis`、`sampler_diversity_probe`、`output_format_audit` 和 `outlier_visual_audit` 完成前，不启动新的主线长训。
2. 如果 empty / random text 与原始 text 的 TMR、CLaTr、caption F1 差异很小，停止调 sampler，优先修 text conditioning 或训练目标。
3. 如果 sampler noise / eta 提升语义但显著伤害 framing，需要报告 Pareto trade-off，而不是挑单一最好数字。
4. 如果 output-format audit 发现骨架、尺度、padding 或有效帧口径不一致，先修 adapter，再重跑 full generated eval。
5. 如果没有拿到论文 Aux 对应 checkpoint / config / training objective，不再把 `cfg_rate_z` sweep 结果命名为 Aux，只能作为 inference-time guidance ablation。
6. 若 component-level Mode B gate 无法证明 `z_distance / z_cam_motion` 分别有效，Mode B 只能保留为 relative camera-latent conditioned generation，不能写成核心方法贡献。
