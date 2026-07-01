---
title: "StoryMotion 工业需求 Brainstorm：现有数据下的 human-camera control 后训练方向"
status: draft
created: 2026-06-30T17:25:00+0800
updated: 2026-06-30T19:10:00+0800
tags:
  - StoryMotion
  - Motion_Generation
  - Camera_Control
  - Skeleton_Reconstruction
  - Motion_Understanding
  - post-training
  - industrial-research
  - status/draft
aliases:
  - StoryMotion industrial brainstorm
hypothesis: |
  StoryMotion 目前不应把“统一框架”本身包装成工业级核心贡献。更合理的 brainstorm 边界是：只利用现有数据和已有生成结果，在 4 卡 5090 资源内，通过后训练、多数据集分步训练、mask curriculum、轻量 reward 或 repair model，让 human/motion 相关能力获得以往工作较难覆盖的新能力。范围可以包括 human motion、camera control、skeleton representation、motion reconstruction、motion understanding，但必须能回到可控、可修、可复用的 motion 生产链路。
source_papers:
  - "[[analysis/SIGGRAPH_2022/LookOut_Interactive_Camera_Gimbal_Controller_for_Filming_Long_Takes|LookOut]]"
  - "[[analysis/SIGGRAPH_2022/Shoot360_Normal_View_Video_Creation_From_City_Panorama_Footage|Shoot360]]"
  - "[[analysis/TOG_2024/SKEL_Betweener_a_Neural_Motion_Rig_for_Interactive_Motion_Authoring|SKEL-Betweener]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/StableMotion_Training_Motion_Cleanup_Models_with_Unpaired_Corrupted_Data|StableMotion]]"
  - "[[analysis/WACV_2026/No_MoCap_Needed_Post-Training_Motion_Diffusion_Models_with_Reinforcement_Learning_using_Only_Textual_Prompts|No MoCap Needed]]"
  - "[[analysis/ICLR_2025/MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions|MotionCritic]]"
  - "[[analysis/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength|I2VControl-Camera]]"
  - "[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]"
  - "[[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion|Direct-a-Video]]"
  - "[[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation|MotionCanvas]]"
  - "[[analysis/SIGGRAPH_2022/Do_We_Measure_What_We_Perceive_Comparison_of_Perceptual_and_Computed_Differences_Between_Hand_Animations|Do We Measure What We Perceive]]"
  - "[[analysis/SIGGRAPH_2022/Evaluating_the_Quality_of_a_Synthesized_Motion_With_the_Fréchet_Motion_Distance|Fréchet Motion Distance]]"
  - "[[analysis/arxiv_2026/MoCapAnything_V2_End_to_End_Motion_Capture_for_Arbitrary_Skeletons|MoCapAnything V2]]"
  - "[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]"
  - "[[analysis/arxiv_2026/UniMo_Unified_Motion_Generation_and_Understanding_with_Chain_of_Thought|UniMo]]"
  - "[[analysis/arxiv_2026/Reconstruction-Anchored_Diffusion_Model_for_Text-to-Motion_Generation|RAM]]"
  - "[[analysis/arxiv_2026/Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval_via_Pyramidal_Shapley_Taylor_Learning|Fine-Grained Motion-Language Retrieval]]"
related_notes:
  - "[[ideas/StoryMotion/2026-06-29_storymotion-v6.2|StoryMotion v6.2]]"
  - "[[social/TX|腾讯混元实习电话沟通规划]]"
---

## 修正后的边界

这份笔记只做 brainstorm，不选定最终方案，也不写时间路线。

前一版把 StoryMotion-QA 定为工业主线过早了。QA/诊断仍然有价值，但如果只停在“质量评估工具”，对 StoryMotion 本体的贡献会偏外围。当前更应该问的是：

- 能否只用现有数据和已有生成结果，通过后训练或多数据集分步训练，让 StoryMotion 获得以往方法没有解决的新能力。
- 这个新能力必须落在 human/motion 相关问题上，包括 human motion、camera control、skeleton representation、motion reconstruction、motion understanding，而不是泛化成 3D 数据平台、UI 系统或纯数据治理。
- 资源假设是独立实验，最多 4 卡 5090；不依赖腾讯内部数据，不做大规模数据构建，不重训 foundation-scale 模型。
- 可接受的技术形态是 LoRA/adapter、短程 fine-tuning、mask curriculum、synthetic corruption、generated-output replay、小规模 reward tuning、小型 repair/refiner。
- 不接受把工业贡献建立在“需要腾讯给大量数据、标注平台、内部视频模型或专业用户研究”之上。

## 当前事实边界

- StoryMotion 的 joint generation 优势较明显，可以支撑 unified branch-mask / joint modeling 的学术叙事。
- Camera completion 相比 E.T./DIRECTOR 没有显著优势，不能写成相机补全能力已经工业可用。
- MoLingo human completion baseline 仍在跑，human completion 是否真正补齐尚未闭合。
- v6.2 的关键诊断是：Pulp-style camera latent 含 `camera_translation - human_root_translation`，camera branch 结构性依赖 human/root。
- hard observed replacement 使 Stage2 学到 observed branch 完全可信，导致 reliability mismatch：observed/generated/noisy human/root 一旦不可靠，camera completion 退化明显。
- 这组事实更适合导向“如何让 camera control 适应不完美 human condition”，而不是导向“我们已有强 camera completion”。

## 工业需求约束

真实工业需求不是单纯提高 FID/FMD，而是让模型输出进入创作、预演、动画或数据生产流程时更可控、更稳、更可修。

在当前约束下，比较可信的工业问题是：

- 给定不完美 human motion，camera 是否仍能稳定跟随、构图和补全。
- 给定少量 human/camera keyframe，系统能否补出可用的中间运动。
- 生成结果出现 root jump、camera jitter、出屏、距离突变时，能否自动修复而不是重生成。
- 用户能否控制相机跟随强度、镜头运动强度、构图强度，而不是只能给 caption。
- 多数据集 human motion 能否提升同一个 human-camera 框架的 motion 语义和补全能力，而不破坏 camera coupling。
- skeleton 表示、SMPL/关节位置/旋转之间的转换是否会引入不可控误差，能否通过轻量 reconstruction/refiner 降低生产链路损耗。
- motion understanding 能否反过来服务控制、筛选、reward 和 editing，而不是只做 motion caption 或 retrieval。

## 证据锚点

[[analysis/TOG_2024/SKEL_Betweener_a_Neural_Motion_Rig_for_Interactive_Motion_Authoring|SKEL-Betweener]] 的工业动机是减少关键帧动画劳动，并支持任意时间/关节稀疏约束的交互式补间。这说明“少量约束到可编辑运动”比黑盒生成更接近动画生产。

[[analysis/SIGGRAPH_ASIA_2025/StableMotion_Training_Motion_Cleanup_Models_with_Unpaired_Corrupted_Data|StableMotion]] 的核心价值是 motion cleanup，而不是重新生成一切。它利用混合质量、未配对 corrupted motion 和质量变量学习修复，说明现有生成结果和扰动数据可以成为训练信号。

[[analysis/WACV_2026/No_MoCap_Needed_Post-Training_Motion_Diffusion_Models_with_Reinforcement_Learning_using_Only_Textual_Prompts|No MoCap Needed]] 证明 motion diffusion 可以用 LoRA 与 reward 做 post-training，不一定需要新的 mocap 数据。这里的启发是“小资源后训练可以改变生成偏好”，但不能直接照搬，因为它没有解决 camera-human coupling。

[[analysis/ICLR_2025/MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions|MotionCritic]] 的启发是 learned evaluator / perceptual reward 能作为后训练信号。当前不适合自建大规模 preference 数据，但可以做 proxy reward 或小规模 preference calibration。

[[analysis/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength|I2VControl-Camera]] 把相机控制和动态物体运动分解，并引入可调 motion strength。它的训练规模对当前不可行，但“控制强度标量”和“相机/主体运动解耦”可迁移到 StoryMotion。

[[analysis/SIGGRAPH_2022/LookOut_Interactive_Camera_Gimbal_Controller_for_Filming_Long_Takes|LookOut]] 与 [[analysis/SIGGRAPH_2022/Shoot360_Normal_View_Video_Creation_From_City_Panorama_Footage|Shoot360]] 说明工业相机系统强调高层意图、构图、跟随和可编辑初始化，不是只追求一次性全自动生成。

[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]、[[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion|Direct-a-Video]]、[[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation|MotionCanvas]] 的共同趋势是控制信号解耦：相机、角色、屏幕轨迹、镜头意图需要分别建模和组合。

[[analysis/arxiv_2026/MoCapAnything_V2_End_to_End_Motion_Capture_for_Arbitrary_Skeletons|MoCapAnything V2]] 的重点是任意骨骼动捕和 pose-to-rotation 的病态性。它的 mixed-pose training 直接对应 StoryMotion 的 reliability mismatch：训练时只看完美姿态，推理时接收预测姿态会产生分布偏移。

[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 使用 per-joint latent decomposition 和 SMPL 参数空间生成，说明 skeleton-aware latent 不是装饰性设计，而是长序列、流式和关节结构泛化的核心。

[[analysis/arxiv_2026/Reconstruction-Anchored_Diffusion_Model_for_Text-to-Motion_Generation|RAM]] 把 motion reconstruction branch 用作 latent manifold 锚点，启发 StoryMotion 可以把 reconstruction 从单纯预训练目标变成生成时的质量约束或负参考。

[[analysis/arxiv_2026/UniMo_Unified_Motion_Generation_and_Understanding_with_Chain_of_Thought|UniMo]] 与 [[analysis/arxiv_2026/Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval_via_Pyramidal_Shapley_Taylor_Learning|Fine-Grained Motion-Language Retrieval]] 说明 motion understanding 不只是 captioning；细粒度动作语言对齐可以成为 reward、检索、错误归因和 edit instruction 的中间层。

## 候选方向池

以下方向都默认不构建新大数据集，只使用已有 StoryMotion/Pulp 数据、公开 motion-text 数据、已有生成结果、合成扰动或少量人工校准。

### 1. Reliability-aware camera control post-training

工业痛点：真实生成链路里，camera 往往不是看到 clean GT human/root，而是看到 generated human、noisy root 或 partial human。当前 StoryMotion 的 camera branch 对 human/root 可靠性过度信任，导致 clean completion 指标无法代表真实生成链路。

可能做法：

- 冻结大部分 Stage2，只用 LoRA/adapter 后训练 camera branch 或 condition adapter。
- 用已有 StoryMotion/Pulp 数据构造 clean、noisy、generated-human replay 三类 condition。
- 加入 reliability scalar/token，表示 observed human/root 的可信度。
- 训练目标不是只拟合 GT camera，而是让 camera 在不同可靠性条件下保持构图、平滑和合理距离。

新能力：给定不完美 human motion 时，camera completion/control 仍能稳定工作。这比“GT human 条件下 camera MSE 更低”更接近工业使用。

有限资源可行性：较高。核心是短程后训练和条件扰动，不需要新数据。

主要风险：如果 Pulp relative camera latent 的结构依赖太强，单纯 reliability token 可能不足，需要更明确的 latent decoupling。

### 2. 多数据集分步训练的 human-motion control adapter

工业痛点：StoryMotion 的 human 分支如果只在当前数据分布内成立，实际动作语义和补全能力会弱；但外部 motion dataset 通常没有 camera，直接混训可能破坏 human-camera coupling。

可能做法：

- 阶段 A：保持当前 StoryMotion joint/camera 表示和基础生成能力。
- 阶段 B：只在 human branch 或 shared backbone 的 adapter 上引入 HumanML3D、AMASS、Motion-X 等现有 motion-text/motion 数据。
- 阶段 C：回到 StoryMotion 数据做短程 re-coupling，让 camera branch 适应增强后的 human latent。
- 对比 mixed training 与 staged training，观察是否降低任务干扰。

新能力：同一 StoryMotion 框架下 human motion completion/generation 更强，同时 camera control 不崩。

有限资源可行性：中等。不是重训全模型，但数据格式转换和 adapter 设计有工程成本。

主要风险：外部 motion 数据缺 camera，若 human latent 分布变化太大，camera branch 可能出现新 mismatch。

### 3. Sparse-control cinematic motion inbetweening

工业痛点：动画和预演常见输入不是完整 caption，而是少数关键帧、角色位置、相机位置或构图约束。现有 StoryMotion 的 mask mode 更像 benchmark task，未必支持任意稀疏约束。

可能做法：

- 把 branch mask 扩展为任意时间/关节/camera keyframe mask。
- 从已有完整序列随机采样 start/end、中间少量 joint keyframe、root keyframe、camera keyframe 作为条件。
- 后训练模型补全剩余 human motion 与 camera motion。
- 评价 control accuracy、motion realism、camera smoothness、framing visibility。

新能力：用户给少量 human/camera keyframe，模型补出可用 cinematic motion。这比纯 joint generation 更像可编辑工具。

有限资源可行性：较高。数据来自已有序列的 mask curriculum，不需要新增采集。

主要风险：如果当前架构的 condition mask 只适配固定 task，需要改输入 contract；评估要避免只变成 MSE 补全。

### 4. Quality-conditioned cleanup / repair

工业痛点：生成链路里常见问题是局部坏片段：root jump、foot skating、camera jitter、subject out-of-frame、relative distance spike。工业上经常需要修复而不是整段重生成。

可能做法：

- 用已有 clean/reference 片段合成 corruptions：root jitter、root jump、camera jitter、gaze drift、FOV jump、出屏、时间断裂。
- 把已有 StoryMotion/Pulp 生成结果当作 mixed-quality data。
- 加入 human quality 与 camera quality 条件变量，让模型在 high-quality condition 下输出 cleaned motion。
- 可以训练一个轻量 refiner，也可以复用 Stage2 做 denoising/repair。

新能力：从“生成一段 motion”转为“修复一段 human-camera motion”，直接对应生产中的 cleanup。

有限资源可行性：较高。腐化规则和生成结果 replay 足够起步。

主要风险：cleanup 容易变成过度平滑，修掉语义动作或镜头风格；必须同时看语义保持和 motion quality。

### 5. Proxy-reward post-training for camera-human consistency

工业痛点：监督损失未必优化创作者关心的构图、跟随、稳定性和节奏。单纯 benchmark 指标好不代表可用。

可能做法：

- 对 Stage2 做小规模 LoRA reward tuning。
- reward 由可计算 proxy 组成：human semantic score、camera smoothness、root-in-frame、subject scale stability、relative distance stability、shot continuity。
- 用已有 caption/sequence 采样多候选，按 proxy reward 做 ranking 或 policy update。
- 不自建大规模 human preference，只做少量人工检查来防止 reward hacking。

新能力：模型在相同数据上对工业质量指标更敏感，而不是只最小化 reconstruction loss。

有限资源可行性：中等。采样会吃 GPU，但短序列、低步数、LoRA 可以控制成本。

主要风险：proxy reward 可能互相冲突，尤其 camera dynamic 与 smoothness、framing 与 cinematic style 之间存在张力。

### 6. Camera control strength / follow-strength decomposition

工业痛点：用户不只想“生成相机”，还想控制镜头强度：固定机位、轻微跟随、强跟随、环绕、推拉、锁定主体、保持距离。当前 latent 如果强绑定 human/root，就缺少可解释控制旋钮。

可能做法：

- 引入几个低维 control scalar：follow strength、framing strength、motion strength、reliability strength。
- 从已有 camera trajectory 中用几何统计构造 pseudo label，例如主体屏幕位置稳定性、相机速度、相对距离变化、朝向跟随程度。
- 后训练时让模型根据 scalar 调节 camera behavior。
- 推理时测试同一 human motion 下不同 camera strength 是否产生可预测变化。

新能力：camera control 从 caption 或 task mask 变成可调参数，更接近 authoring。

有限资源可行性：较高。核心是伪标签和条件控制，不需要新数据。

主要风险：伪标签可能只捕捉统计量，不等于真实镜头风格；需要可视化和消融证明 scalar 真有控制力。

### 7. Completion 到 joint generation 到 editing 的分步 curriculum

工业痛点：统一框架可能在 benchmark 上 joint 指标好，但多任务混训可能隐藏任务干扰，特别是 human completion、camera completion、joint generation 对 condition reliability 的要求不同。

可能做法：

- 不改数据，只改训练顺序与任务采样。
- 先训练 clean completion/reconstruction，让模型学稳定 human-camera geometry。
- 再加入 joint generation，让模型学联合分布。
- 最后加入 noisy/generated/sparse editing condition，让模型适应真实使用链路。
- 与原始 mixed multitask training 对比，观察 camera completion、人类补全、joint generation 的 tradeoff。

新能力：用同样数据得到更稳定的 task transfer，尤其是减少 camera branch 对 clean observed human 的过拟合。

有限资源可行性：中等。若要从 checkpoint 继续训练可控；若必须多次完整复现实验会变贵。

主要风险：贡献可能被认为是 training recipe，除非能明确证明它解决了可靠性或编辑能力问题。

### 8. Camera-from-human retargeting / camera style transfer

工业痛点：很多场景已有 human motion，但缺 camera；或者希望把某段镜头风格迁移到另一个角色动作上。盲目 camera completion 不等于可控 camera authoring。

可能做法：

- 从已有数据中提取 camera style code 或 reference camera latent。
- 输入 human motion 加 style/reference camera，输出适配后的 camera trajectory。
- 控制项可以是 static、follow、orbit、push-in、pull-out、handheld-like 等弱标签，也可以用 reference trajectory。
- 评价同一 human motion 下 camera style 是否可迁移，同时保持 framing 和 smoothness。

新能力：camera control 变成 retargeting/style transfer，而不是单一 completion。

有限资源可行性：中等偏高。依赖已有 camera 多样性；如果数据里镜头类型太少，能力上限会低。

主要风险：style label 可能不干净，且 camera style 的自动评估不容易。

### 9. Skeleton-aware representation adapter

工业痛点：生产链路中的 motion 往往需要在 joint position、joint rotation、SMPL、SMPL-X、角色骨骼或游戏引擎 skeleton 之间转换。很多生成模型只在一种表示上指标好，但导出到动画资产时会出现骨长漂移、旋转抖动、局部坐标不一致或 IK 后伪影。

可能做法：

- 在现有 StoryMotion 表示外加一个轻量 representation adapter，学习 joint position 到 rotation/SMPL 参数的可逆或近可逆映射。
- 引入 rest pose、bone length、reference pose-rotation pair 作为几何锚点，避免 pose-to-rotation 的多解问题。
- 用已有 motion 数据做 synthetic retarget/reconstruction，不需要新增采集。
- 评估不只看 MPJPE，还看 rotation error、bone length consistency、foot contact、camera framing 是否受 representation error 影响。

新能力：StoryMotion 输出从“benchmark joint sequence”变成更接近 animation-ready skeleton motion。

有限资源可行性：中等。adapter 本身轻，但需要整理表示转换和评估脚本。

主要风险：如果 StoryMotion 数据没有足够可靠的旋转或 SMPL 标注，需要先限定到可转换子集。

### 10. Reconstruction-anchored StoryMotion

工业痛点：生成模型容易离开 motion manifold，表现为局部姿态怪、root 漂移、相机跟随不自然。只靠 diffusion loss 或最终指标，不一定能在生成过程中识别“当前预测已经不像可重建 motion”。

可能做法：

- 给 Stage2 或 latent space 增加 motion/camera reconstruction branch，约束 latent 必须保留可重建的 human skeleton 与 camera trajectory。
- 推理时把 reconstruction result 作为 negative reference 或 consistency anchor，压制离开数据流形的预测。
- 可以只训练 reconstruction head 或 adapter，不重训完整模型。
- 对比有无 reconstruction anchor 时的 motion smoothness、joint plausibility、camera-human consistency。

新能力：用 reconstruction 作为生成质量约束，而不是只把 reconstruction 当 autoencoder 预训练任务。

有限资源可行性：中等。需要改模型头和训练目标，但数据完全来自已有序列。

主要风险：reconstruction anchor 可能牺牲多样性，导致生成变保守。

### 11. Motion-understanding-guided control and repair

工业痛点：很多坏例不是低层几何错误，而是动作语义和镜头意图错位：文本说转身但 motion 没有转身，镜头应跟随却停住，动作阶段和 shot timing 不匹配。没有 motion understanding，repair/refiner 很难知道该保留什么、改什么。

可能做法：

- 训练或复用轻量 motion-to-text / motion-to-tag / temporal action segmentation 模块。
- 标签来自已有 caption、motion retrieval 模型、自动动作短语解析，不新增大规模标注。
- 把 understanding score 用作 reward、repair condition 或 badcase attribution。
- 重点做细粒度 temporal grounding，例如哪一段发生 jump、turn、sit、run，camera 是否在对应阶段跟随或切换。

新能力：StoryMotion 不只是生成/补全，还能解释动作阶段并据此控制 camera 或修复 motion。

有限资源可行性：中等偏高。可先用 frozen encoder/retrieval score 做弱监督，不必训练大模型。

主要风险：caption 粗糙会限制 understanding 上限，容易变成弱 QA；必须把它接到 control 或 repair 实验上。

### 12. Mixed-pose training for generated skeleton robustness

工业痛点：训练时使用 GT skeleton，推理时接收生成 skeleton 或重建 skeleton，是 motion 系统常见的 train-test gap。camera control、pose-to-rotation、repair model 都会被这个 gap 放大。

可能做法：

- 仿照 mixed-pose 思路，训练时逐步提高 generated/noisy skeleton 的输入比例。
- condition 包括 GT skeleton、StoryMotion generated skeleton、reconstructed skeleton、synthetic noisy skeleton。
- 目标可以是 camera prediction、rotation recovery、motion cleanup 或 joint completion。
- 评估模型面对非 GT skeleton 时的性能退化斜率。

新能力：把 generated skeleton 从 failure source 变成训练时显式建模的输入分布。

有限资源可行性：较高。核心数据来自已有 GT 和当前模型生成结果。

主要风险：如果生成 skeleton 质量太差，混入训练会污染模型；需要 curriculum 而不是一次性混合。

### 13. Fine-grained motion-language alignment for editing

工业痛点：工业编辑不是“整段生成是否符合文本”，而是“某一帧到某一段是否执行了指定动作，并且镜头是否对准了该动作”。全局 text-motion retrieval 分数太粗，无法指导局部修复。

可能做法：

- 从已有 caption 中解析动作短语、时序连接词和身体部位词，构造弱 temporal/part-level supervision。
- 用现有 motion encoder 做 fine-grained retrieval 或 contrastive alignment。
- 让 edit instruction 指向局部片段，例如强化手部动作、放慢转身、保持角色在画面中心。
- 与 sparse-control inbetweening 或 cleanup 结合，证明 understanding 能指导局部编辑。

新能力：从 global caption control 走向局部可编辑 motion understanding。

有限资源可行性：中等。难点在弱标签质量，但不需要新采集。

主要风险：如果没有可靠 temporal grounding，容易只得到漂亮的 retrieval 指标，不能改善生成或编辑。

## 方向对照

| 候选方向 | 真实工业需求 | 主要新增能力 | 资源压力 | 最大风险 |
| --- | --- | --- | --- | --- |
| Reliability-aware camera control | 生成链路中 human condition 不完美 | noisy/generated human 下 camera 仍可控 | 低到中 | latent 结构依赖无法靠 token 修复 |
| 多数据集 human adapter | human motion 泛化弱 | human motion 更强且不破坏 camera | 中 | 外部数据无 camera 导致分布漂移 |
| Sparse-control inbetweening | 动画关键帧补间和预演 | 任意稀疏 human/camera 约束补全 | 低到中 | 架构 mask contract 不够灵活 |
| Quality-conditioned cleanup | 生产中需要修坏片段 | human-camera motion 自动修复 | 低到中 | 过度平滑和语义损失 |
| Proxy-reward post-training | 监督损失不等于可用性 | 对构图/稳定性/跟随偏好优化 | 中 | reward hacking |
| Control strength decomposition | 用户需要镜头强度旋钮 | 可调 follow/framing/motion strength | 低到中 | 伪标签不等于真实风格 |
| 分步 curriculum | 多任务统一框架有干扰 | 同数据下更稳定 task transfer | 中 | 贡献像 recipe |
| Camera style transfer | 已有 human 缺可控 camera | reference/style-conditioned camera | 中 | camera 多样性不足 |
| Skeleton-aware adapter | 生成 motion 难以导出到资产骨骼 | animation-ready skeleton reconstruction | 中 | 旋转或 SMPL 标注不足 |
| Reconstruction anchor | 生成偏离 motion manifold | reconstruction 约束生成质量 | 中 | 生成变保守 |
| Motion understanding guided repair | 动作语义与镜头意图错位 | understanding 反向指导控制和修复 | 中 | caption 或弱标签太粗 |
| Mixed-pose skeleton robustness | GT skeleton 到生成 skeleton 有分布差 | 非 GT skeleton 下仍稳定 | 低到中 | 低质生成样本污染训练 |
| Fine-grained motion-language editing | 全局 caption 无法指导局部编辑 | 局部动作语言对齐和编辑 | 中 | temporal grounding 不可靠 |

## 更值得追问的问题

- 当前 camera completion 不显著优于 E.T.，是否是因为 evaluation 用 clean GT human，而真实失败发生在 generated/noisy human 条件下。
- 如果只做 reliability-aware post-training，能否让 camera 在 generated-human condition 下的退化斜率明显变小。
- 如果用多数据集 human adapter，human motion 变强是否会反过来改善 camera control，还是破坏 relative camera latent。
- 当前 branch mask 是否天然支持任意稀疏 keyframe；如果支持，sparse-control inbetweening 可能是最低成本的工业化扩展。
- Quality-conditioned cleanup 是否能比重新训练 generator 更直接地解决 jitter、出屏、jump 等生产坏例。
- Camera strength scalar 是否能成为可视化、可演示、可量化的用户控制接口。
- skeleton 表示转换误差是否是 StoryMotion 结果无法进入动画资产链路的隐藏瓶颈。
- reconstruction branch 能否作为生成过程的 motion manifold anchor，而不仅是编码器预训练。
- motion understanding 是否能真正改善 control/repair，而不是只新增一个评价器。
- generated skeleton mixed training 能否缓解 StoryMotion 当前最明显的 reliability mismatch。

## 对外表述边界

| 不应写 | 应改写为 |
| --- | --- |
| StoryMotion 已经提供工业可用的自动故事生成工具 | StoryMotion 正在探索现有数据条件下更可控的 human-camera motion 生成与修复能力 |
| 统一建模解决了 human-camera coupling | 当前结果暴露出 human-camera coupling 对 condition reliability 敏感 |
| 指标优势说明生成结果可用于生产 | 指标优势只说明某些 benchmark 维度改善，仍需控制、修复和感知校准 |
| 腾讯实习能保证论文资源 | 公开实验必须独立可复现，腾讯最多提供工业问题观察 |
| QA 是最终工业主线 | QA 是候选支撑模块，核心仍应回到 human/motion 相关的新能力 |

## 暂时排除

- 大规模重训 video/motion foundation model。
- 依赖腾讯内部大数据或闭源模型才能成立的方向。
- 以 UI、用户研究或工程平台作为核心贡献的方向。
- 纯 caption 数据扩充、纯 VLM 打标、纯数据治理，而不改善 human motion、camera control、skeleton reconstruction 或 motion understanding 能力的方向。
- 只做指标 dashboard，却不产生后训练、控制、补全、修复或编辑能力的方向。
