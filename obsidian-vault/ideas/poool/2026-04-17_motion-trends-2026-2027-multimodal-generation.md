---
title: "FineXtrol: Controllable Motion Generation via Fine-Grained Text"
venue: AAAI
year: 2026
tags:
  - Motion_Generation
  - task/text-to-motion
  - diffusion
  - controlnet
  - contrastive-learning
  - dataset/HumanML3D
  - dataset/FineMotion
  - opensource/no
core_operator: 用“带明确时间区间和身体部位语义的细粒度文本”替代全局坐标控制信号，并以双分支残差控制框架和分层对比学习文本编码器，实现更自然且更易用的可控动作生成。
primary_logic: |-
  粗粒度文本 + FineMotion 提供的时间显式、部位显式细粒度文本控制信号
  → 先用分层对比学习训练 T5，使其分别在 sentence / snippet / sequence 三个层级上学会区分细粒度动作语义
  → 冻结该控制文本编码器，提取更可分辨的 control embedding
  → 下支路保留原始 MDM 负责稳定的粗文本到动作生成，上支路复制 MDM 并接收细粒度控制 embedding
  → 通过零初始化线性层把上支路的残差控制逐层注入下支路
  → 生成既符合 coarse text，又在指定时间段内 obey 指定 body part 控制的动作序列
claims:
  - 在 HumanML3D 的单部位平均控制设置下，FineXtrol 达到 FID 0.245、R-Top3 0.685，显著优于无控制的 MDM（0.544 / 0.611）以及同模态文本控制基线 CoMo（0.347 / 0.625）。
  - 在更困难的多部位 Cross 控制设置下，FineXtrol 取得 FID 0.351、R-Top3 0.676，优于 OmniControl（0.624 / 0.601）和 CoMo（0.606 / 0.611）。
  - 控制范式和文本编码器都不可缺：直接把 coarse text 与 fine-grained control 拼成单输入会把 FID 拉高到 1.383，而把分层对比学习编码器替换成原始 T5 也会使 FID 从 0.245 退化到 0.374。
pdf_ref: paperPDFs/Motion_Generation/AAAI_2026/2026_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text.pdf
category: Motion_Generation
created: 2026-03-02T23:15
updated: 2026-04-16T00:00
---

# 2026-04-17 2026-2027 Motion 趋势变化与多模态动作生成机会

> [!abstract] 范围说明
> - 主证据来自当前仓库 `paperAnalysis/`。
> - 补充检查了父目录 `../paperAnalysis/`，仅发现一个空白的 `EasyTune` 占位文件，没有新增可用实证，因此本文的证据主体仍以当前仓库为准。
> - 文中所有“2027”判断都是基于 2025-2026 公开论文与项目的推断，不是已发生事实。
> - 本文显式忽略 HOI、HSI、RL 作为主线，只保留与多模态驱动动作生成直接相关的内容。

## 1. Idea decomposition and association

- 问题重述：
  需要回答的不是“motion 论文又多了什么 trick”，而是 2026 到 2027 之间，motion 在学界与工业界会如何从一个相对独立的生成任务，变成跨 text, video, image, avatar, MLLM 的中间能力层。
- 观察范围：
  重点看 [[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions|Motion_Generation]]、[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_MTVCraft_Tokenizing_4D_Motion_for_Arbitrary_Character_Animation|Motion_Controlled_ImageVideo_Generation]]、[[paperAnalysis/Motion_Editing/CVPR_2026/2026_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing|Motion_Editing]]、[[paperAnalysis/Image_Video_Generation/NeurIPS_2025/2025_FramePack_Frame_Context_Packing_and_Drift_Prevention_in_Next_Frame_Prediction_Video_Diffusion_Models|Video_Generation]]、[[paperAnalysis/Vision_Language_Model/Qwen_2025/2025_Qwen3_VL_Technical_Report|Vision_Language_Model]]。
- 关键拆解维度：
  数据与规模、表征与 token、规划与控制、流式执行、跨模态接口、评测与 judge、身份一致性与个性化、工业部署成本。
- 一个直观信号：
  当前仓库中 `Motion_Generation` 在 2025 有 66 篇、2026 有 25 篇；而 `Motion_Controlled_ImageVideo_Generation` 从 2025 的 3 篇增到 2026 的 11 篇。这说明 2026 的新增重点已经明显向“motion 驱动 video/avatar/image”迁移，而不只是继续堆单一 T2M 指标。

## 2. Real scenarios and pain points

- 典型场景：
  数字人/Avatar 内容生产、游戏与影视动画管线、短视频人物生成、可控视频编辑、XR/VTuber、动作感知图像编辑。
- 核心需求：
  要同时满足语义跟随、动作自然、身份稳定、长时一致、低延迟交互、可局部修改、跨角色泛化。
- 当前方案的痛点：
  纯 coarse text 条件过于模糊，很难表达“哪一段、哪个部位、以什么方式动”。
- 当前方案的痛点：
  纯 motion 任务与 video/avatar/image 任务割裂，导致 motion 不能稳定迁移成视觉生成中的通用控制接口。
- 当前方案的痛点：
  长时序生成一旦漂移，往往只能整段重采样，缺少规划、诊断、局部修复的闭环。
- 当前方案的痛点：
  学术指标多数仍偏向 HumanML3D 一类标准集，难以覆盖泛化、产品一致性、身份保持、实时性能。
- 当前方案的痛点：
  工业侧真正在意的是“稳定可控的内容管线”，所以数据清洗、推理速度、可组合控制、少样本定制通常比单点 SOTA 更重要。

## 3. Related-work support and research opportunities

### 3.1 Related-work overview

- [[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions|Being-M0]] 与 [[paperAnalysis/Motion_Generation/CVPR_2025/2025_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Model|ScaMo]]：把动作生成从“小模型+小词表+小数据集”的方法论文，推进到真正的 scale law 讨论。
- [[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion|HY-Motion 1.0]] 与 [[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]：代表工业侧开始把 motion 当成大模型底座和产品级 controllable asset，而不是单纯 benchmark 模型。
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]、[[paperAnalysis/Motion_Generation/CVPR_2025/2025_LLaMo_Human_Motion_Instruction_Tuning|LLaMo]]、[[paperAnalysis/Motion_Generation/ICLR_2025/2025_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with_LLMs|Motion-Agent]]：说明 motion-language 不再只是检索/描述，而是在向统一理解、生成、编辑接口发展。
- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]、[[paperAnalysis/Motion_Generation/CVPR_2026/2026_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Inference|LaMoGen]]、[[paperAnalysis/Motion_Generation/AAAI_2026/2026_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text|FineXtrol]]、[[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]]：共同指向“结构化规划和细粒度控制”成为 2026 的主旋律。
- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_ViMoGen_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation|ViMoGen]]、[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]、[[paperAnalysis/Motion_Generation/ICLR_2026/2026_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation|COME]]：重心从“哪种 backbone 更强”转向“泛化数据、语义对齐潜空间、评测闭环”。
- [[paperAnalysis/Motion_Generation/ICCV_2025/2025_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space|MotionStreamer]]、[[paperAnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]：把在线生成从“能流式”推进到“能规划、能快、能长、能编辑”。
- [[paperAnalysis/Image_Video_Generation/CVPR_2025/2025_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_Generation|HumanDreamer]]、[[paperAnalysis/Image_Video_Generation/CVPR_2025/2025_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human_centric_Video_Generation|TokenMotion]]、[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_MTVCraft_Tokenizing_4D_Motion_for_Arbitrary_Character_Animation|MTVCraft]]、[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_MotionStream_Real_Time_Video_Generation_with_Interactive_Motion_Controls|MotionStream]]、[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_OmniHuman_1_5_Instilling_an_Active_Mind_in_Avatars_via_Cognitive_Simulation|OmniHuman-1.5]]：共同表明 motion 已经进入 video/avatar 主干，而不是外接 pose 条件。
- [[paperAnalysis/Motion_Editing/CVPR_2026/2026_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing|MotionEdit]]：说明 image editing 也开始把“motion understanding”视为一个独立能力，而非从语义编辑顺带得到。

### 3.2 Support points: 2026 observed changes and 2027 inferred shifts

- `底座层`
  2026 已观测到从 scale law、数据引擎、对齐潜空间、泛化评测四件套重新定义 motion foundation model；2027 很可能继续往“统一底座 + 标准化评测 + 多任务蒸馏”收敛。证据主要来自 [[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions|Being-M0]]、[[paperAnalysis/Motion_Generation/CVPR_2025/2025_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Model|ScaMo]]、[[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion|HY-Motion 1.0]]、[[paperAnalysis/Motion_Generation/ICLR_2026/2026_ViMoGen_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation|ViMoGen]]。
- `控制层`
  2026 已经从 coarse sentence control 转到 event, part, frame, symbolic plan 这些结构化接口；2027 预计会出现更像“motion DSL / motion compiler”的表示层。证据主要来自 [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]、[[paperAnalysis/Motion_Generation/CVPR_2026/2026_LaMoGen_Language_to_Motion_Generation_Through_LLM_Guided_Symbolic_Inference|LaMoGen]]、[[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]]、[[paperAnalysis/Motion_Generation/AAAI_2026/2026_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text|FineXtrol]]。
- `执行层`
  2026 已经不满足于离线采样，而是在做 streaming, real-time, future-aware generation；2027 很可能把“planning + streaming + local repair + verification”整合成 anytime generation。证据主要来自 [[paperAnalysis/Motion_Generation/ICCV_2025/2025_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space|MotionStreamer]]、[[paperAnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]。
- `跨模态层`
  2026 已观测到 motion 从“输出结果”变成“video/avatar/image 的中间控制表征”；2027 更可能形成 motion latent 的统一接口，让角色动画、人物视频、图像编辑、故事板生成共享同一运动中间层。证据主要来自 [[paperAnalysis/Image_Video_Generation/CVPR_2025/2025_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_Generation|HumanDreamer]]、[[paperAnalysis/Image_Video_Generation/CVPR_2025/2025_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human_centric_Video_Generation|TokenMotion]]、[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_MTVCraft_Tokenizing_4D_Motion_for_Arbitrary_Character_Animation|MTVCraft]]、[[paperAnalysis/Motion_Editing/CVPR_2026/2026_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing|MotionEdit]]。
- `工业层`
  2026 的工业信号更关心 controllability, identity, speed, asset reuse, retargeting，而不是只关心 HumanML3D；2027 大概率继续向“全链路动作内容生产工具”推进。证据主要来自 [[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion|HY-Motion 1.0]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]、[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_OmniHuman_1_5_Instilling_an_Active_Mind_in_Avatars_via_Cognitive_Simulation|OmniHuman-1.5]]、[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_MotionStream_Real_Time_Video_Generation_with_Interactive_Motion_Controls|MotionStream]]。

### 3.3 Research opportunities

- `机会 A：Motion Planner / DSL`
  把 `Event-T2M` 的事件分解、`LaMoGen` 的符号中间层、`FrankenMotion` 的部位级组合、`ActionPlan` 的帧级规划统一成一个可执行的 motion planning language。这个方向最像 2027 的“结构层创新点”。
- `机会 B：Motion as a Universal Latent Interface`
  把 `MoLingo` 的语义潜空间、`PRISM` 的关节分解潜码、`MTVCraft` 的 4D motion token、`MotionEdit` 的 motion-aware image edit 接到同一 latent 接口上，目标不是只做 T2M，而是让 motion 成为 image/video/avatar/editing 的统一中间变量。
- `机会 C：Long-Horizon Streaming with Local Repair`
  以 `MotionStreamer`、`ActionPlan`、`PRISM` 为基础，引入分段诊断、局部再采样、未来约束一致性检查，让 streaming generation 不再是“一路滚下去”，而是“边生成边纠偏”。
- `机会 D：MLLM-based Motion Judge / Critic`
  结合 `Qwen3-VL`、`SkeletonLLM`、`ReMoRa`、`ViMoGen` 的 VLM-based benchmark 思路，把 judge 从单一 text-motion retrieval 升级成多维验证器，评估动作语义、局部执行、长时一致性、身份保持与视频可渲染性。
- `机会 E：Product-ready Personalized Motion`
  以 `HY-Motion 1.0`、`Kimodo`、`OmniHuman-1.5`、`SMRABooth` 为信号，做“主体 identity + motion style + task constraint”三者解耦的 few-shot motion personalization，直接对接工业落地。

## 4. Frontier cross-domain techniques and validation ideas

- `Video prior injection`
  Brief description: 用 video foundation model 的泛化先验反哺 motion，而不是把 motion 只当输出。
  How to plug into multimodal motion generation: 把 motion model 训练成 visual generation 的 planning layer，再蒸馏回独立 motion backbone。
  Validation idea: 先做 motion-only 与 motion+video-prior 的 OOD 对比，再看是否提升 image/video downstream controllability。
  Related links: [[paperAnalysis/Motion_Generation/ICLR_2026/2026_ViMoGen_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation|ViMoGen]]、[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_MTVCraft_Tokenizing_4D_Motion_for_Arbitrary_Character_Animation|MTVCraft]]、[ViMoGen Project](https://motrixlab.github.io/2026_iclr_vimogen/)、[MTVCraft OpenReview](https://openreview.net/pdf?id=m7AQM9H6wa)

- `Streaming memory and anti-drift`
  Brief description: video 的长期生成经验可以直接迁移到 long-horizon motion。
  How to plug into multimodal motion generation: 把 memory pack, attention sinking, rolling cache, endpoint planning 变成 motion streaming 的标准组件。
  Validation idea: 评测长序列 jerk, drift, transition failure，并测局部修复后的延迟与稳定性。
  Related links: [[paperAnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]、[[paperAnalysis/Image_Video_Generation/NeurIPS_2025/2025_FramePack_Frame_Context_Packing_and_Drift_Prevention_in_Next_Frame_Prediction_Video_Diffusion_Models|FramePack]]、[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_MotionStream_Real_Time_Video_Generation_with_Interactive_Motion_Controls|MotionStream]]、[MotionStream Project](https://motionstream-page.github.io/)

- `Storyboard and multi-shot planning`
  Brief description: 从 video 叙事生成借结构化 shot planning，而不是只做单段 motion。
  How to plug into multimodal motion generation: 把 storyboard, start-end anchor, shot memory 变成 motion 的高层条件，再让底层执行器生成片段并拼接。
  Validation idea: 从单段动作扩展到“多段意图 + 转场 + 局部重写”，做人评和脚本一致性评测。
  Related links: [[paperAnalysis/Motion_Generation/TOG_2025/2025_Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation|Sketch2Anim]]、[[paperAnalysis/Image_Video_Generation/arXiv_2026/2026_STAGE_Storyboard_Anchored_Generation_for_Cinematic_Multi_shot_Narrative|STAGE]]、[STAGE arXiv](https://arxiv.org/abs/2512.12372)

- `Motion-centric image editing`
  Brief description: image editing 正在单独学习“改动作而不破主体/场景”，这与 controllable motion 的目标高度一致。
  How to plug into multimodal motion generation: 让 motion latent 同时服务于 T2M 和 image edit，形成“先改动作语义，再投影到像素”的统一框架。
  Validation idea: 做同一 latent 下的 motion generation, motion editing, pose transfer 三任务联合实验。
  Related links: [[paperAnalysis/Motion_Editing/CVPR_2026/2026_MotionEdit_Benchmarking_and_Learning_Motion_Centric_Image_Editing|MotionEdit]]、[[paperAnalysis/Image_Video_Generation/NeurIPS_2024/2024_Stable_Pose_Leveraging_Transformers_for_Pose_Guided_Text_to_Image_Generation|Stable-Pose]]、[[paperAnalysis/Image_Video_Generation/NeurIPS_2024/2024_StoryDiffusion_Consistent_Self_Attention_for_Long_Range_Image_and_Video_Generation|StoryDiffusion]]、[MotionEdit arXiv](https://arxiv.org/abs/2512.10284)

- `MLLM planner / judge`
  Brief description: MLLM 不一定负责直接生成 motion，更适合做 plan, diagnosis, verification, data curation。
  How to plug into multimodal motion generation: 让 MLLM 输出事件图、部位约束、失败诊断和修复建议，再由专门 motion executor 执行。
  Validation idea: 先做 plan-only ablation，再加 judge-only，再看 plan+judge 是否明显优于直接 end-to-end。
  Related links: [[paperAnalysis/Vision_Language_Model/Qwen_2025/2025_Qwen3_VL_Technical_Report|Qwen3-VL]]、[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_OmniHuman_1_5_Instilling_an_Active_Mind_in_Avatars_via_Cognitive_Simulation|OmniHuman-1.5]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Rendering_and_MLLMs|SkeletonLLM]]、[[paperAnalysis/Image_Video_Generation/CVPR_2026/2026_ReMoRa_Multimodal_Large_Language_Model_based_on_Refined_Motion_Representation_for_Long_Video_Understanding|ReMoRa]]、[Qwen3-VL arXiv](https://arxiv.org/abs/2511.21631)、[OmniHuman-1.5 Project](https://omnihuman-lab.github.io/v1_5)

- `Inference-time refinement`
  Brief description: image generation 的 interleaving reasoning 与 token perturbation 可以转成 motion test-time compute。
  How to plug into multimodal motion generation: 在 motion sampling 时加入“诊断 token / 局部重采样 / token-level guidance”，重点修复失败片段而非全局重做。
  Validation idea: 比较一次性生成与两轮“生成-诊断-修复”的 semantic alignment、jerk、user preference。
  Related links: [[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_IRG_Interleaving_Reasoning_for_Better_Text_to_Image_Generation|IRG]]、[[paperAnalysis/Image_Video_Generation/arXiv_2026/2026_Self_Swap_Guidance_Diffusion_Token_Perturbation|Self-Swap Guidance]]、[IRG arXiv](https://arxiv.org/abs/2509.06945)、[SSG arXiv](https://arxiv.org/abs/2604.08048)

## 5. Summary and next steps

- 核心结论：
  2026 到 2027 的真正变化，不是 motion 生成从 A backbone 换到 B backbone，而是 motion 在系统位置上的变化。它正在从单点输出任务，转成可规划、可流式执行、可跨模态复用、可工业化部署的中间控制层。学界的关键增量是结构化规划、泛化评测、长时执行和跨模态接口；工业界的关键增量是规模化数据、速度、身份一致性、少样本定制与资产复用。
- 最值得盯的关注点：
  结构化 motion plan、motion latent 统一接口、streaming + local repair、MLLM judge、motion-centric editing、个性化 controllable avatar。
- 最适合立项的 3 个题：
  `1)` Motion Planner/DSL，`2)` Motion as Universal Latent Interface，`3)` Streaming Motion with Local Repair and Judge。
- 近端可执行步骤：
  先从当前仓库抽一个 2025-2026 的核心子集，按 `scale / planning / streaming / video-bridge / judge` 五类重建 mini reading list。
- 近端可执行步骤：
  再选一个最小验证问题，例如“事件级规划 + 局部修复”或“motion latent 同时服务 T2M 和 image editing”，避免一上来做全栈统一。
- 近端可执行步骤：
  评测上不要只看 HumanML3D FID，至少补上长时 drift、局部控制成功率、身份保持、下游 video renderability。
- 潜在目标 venue：
  偏方法与表征可冲 `CVPR 2027 / ICCV 2027`，偏统一生成与推理闭环可冲 `ICLR 2027 / NeurIPS 2027`，偏 avatar / animation / content pipeline 可看 `SIGGRAPH Asia 2026-2027`。
