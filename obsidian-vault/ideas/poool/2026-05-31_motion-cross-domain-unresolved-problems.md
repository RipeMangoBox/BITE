---
created: 2026-05-31T23:28:29+08:00
updated: 2026-06-01T01:28:45+08:00
title: "2024+ Motion 未解需求与跨域机制 idea"
status: draft
hypothesis: "2024+ motion 的高价值机会不在继续堆通用 T2M 语义注入，而在可解释编辑、表征失效诊断、多视角一致性、交互阶段约束和物理适应闭环。"
tags:
  - research-idea
  - Motion_Generation
  - Motion_Editing
  - Human_Object_Interaction
  - evaluation
  - physical-control
  - representation-learning
  - cross-domain-transfer
discussion_sources:
  - multi-agent/explorer-motion-gaps
  - multi-agent/explorer-cross-domain-mechanisms
  - deepseek/two-round-stress-test
  - codex-handoff/019e7e64-534a-74a2-b11f-e8c320d31c8e
source_idea_note: "/home/ripemangobox/Coding/Github/OpenSource/On_Process/ResearchFlow_Process/obsidian-vault/ideas/2026-05-31.md"
external_analysis_root: "/home/ripemangobox/Coding/Github/OpenSource/On_Process/ResearchFlow_Process/obsidian-vault/analysis"
---

# 2024+ Motion 未解需求与跨域机制 idea

> [!abstract] 接力结论
> 不建议继续做“给 T2M 加一个帧级/事件级语义模块”或“把视频里的某个 control trick 直接搬到 motion”的浅层组合。UniMotion、MoLingo、Event-T2M、ActionPlan 已经把帧级、事件级、多 token 条件化推得很前。更值得投入的是三类问题：**已有生成器内部能力如何被诊断和编辑**、**PAE/VQ/VAE/SAE 等表征何时失效以及如何分层补救**、**camera / multiview / semantic-memory 机制如何变成 motion 的评价和生成约束**。

本文是对会话 `019e7e64-534a-74a2-b11f-e8c320d31c8e` 的接力整理。上一版文档仍保留了 `ReMoFuse`，但用户已明确弃用该方向；本版将其降级为反例，不再作为候选 paper idea。

## 0. 证据角色与边界

- 假设当前目标不是写综述，而是生成后续可立项、实验和写 paper 的 idea note。
- `analysis/` 证据来自另一个 vault 路径；正文中的 analysis md 引用统一写成 `[[analysis/...md|缩写]]`，不用反引号包裹。
- 自动指标、probe、MLLM judge、偏好模型分数均只能作为 `dev_metric`、`side_signal`、`diagnostic` 或 `selection` 信号，不能直接升级为 `heldout_final_evaluator`。
- 涉及 arXiv/2026 条目时，只把本地 analysis 和网页检索作为 idea 证据，不声称最终发表状态。
- 本次接力中 DeepSeek max 复核超时，未把该次调用作为新增证据；前序 DeepSeek 两轮反驳与两个子代理结果仍作为 discussion source。
- 按用户要求，不再使用 Kimi MCP。

## 1. 已经被占坑或应降级的方向

### 1.1 帧级/事件级语义注入已被强占

直接做“更强文本语义注入”“更细 frame-level alignment”很容易被 reviewer 认为只是补模块：

- [[analysis/3DV_2025/UniMotion_Unifying_3D_Human_Motion_Synthesis_and_Understanding.md|UniMotion]]：统一运动合成和帧级运动理解，支持层级文本控制、motion-to-frame-text、联合生成和编辑。
- [[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]：SAE 语义对齐潜在空间 + 多 token 交叉注意力，直接覆盖“潜在空间语义对齐”和“更强文本条件化”。
- [[analysis/ICLR_2026/Event_T2M_Event_level_Conditioning_for_Complex_Text_to_Motion_Synthesis.md|Event-T2M]]：LLM 事件分解 + 事件级交叉注意力，专攻复杂多动作顺序。
- [[analysis/CVPR_2026/ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning.md|ActionPlan]]：逐帧 action plan + 异构扩散时间步，打通离线和流式。

剩余缺口不是“有没有帧级语义”，而是：

- 帧级监督稀缺，BABEL/HumanML3D 交集覆盖有限；
- 长序列、罕见动作、物理交互、多人交互没有闭环；
- 编辑和评价缺少可靠局部诊断；
- 真实创作、仿真和机器人场景需要连续修改、物理可执行和低延迟。

### 1.2 `ReMoFuse` 不再作为主线

用户已明确弃用 `ReMoFuse`：单人 motion 伪造 interaction 的工作 2023 年已有，现在多人/交互数据也更多。继续把“单人片段拼成伪多人交互”作为主贡献，风险很高：

- 容易被认为是 synthetic data stitching，而不是新的 interaction modeling；
- 难证明伪交互学到的是真正 reaction、contact、delay 和 force response；
- HOI / HHI 近两年已有大量 body-object-contact、role-aware、phase-aware 或 policy-guided 工作，低质量伪数据不再是强缺口。

可保留的部分只有一个：**counterfactual composition 作为诊断工具**。例如替换非目标角色、交换 camera、打乱 contact window，用来检测模型是否偷用上下文 shortcut。它不应再作为 paper 主线。

### 1.3 直接做 `PAE for generation/reconstruction/physics` 已经不够新

PAE / phase manifold 的价值真实存在，但“把 PAE 用到生成、重建、物理一致性”已经被多条路线覆盖：

- [[analysis/TOG_2022/DeepPhase_periodic_autoencoders_for_learning_motion_phase_manifolds.md|DeepPhase]]：PAE 学习多局部周期通道，强在 temporal/spatial alignment 和 motion matching。
- [[analysis/SIGGRAPH_2024/WalkTheDog_Cross_Morphology_Motion_Alignment_via_Phase_Manifolds.md|WalkTheDog]]：VQ-PAE 用共享离散 amplitude codebook + phase manifold 做人狗跨形态对齐。
- `FunPhase` 进一步把 phase manifold 扩成 functional autoencoder，目标包括任意时间分辨率采样、super-resolution 和 partial-body completion。
- `POMP` 把 phase manifold 用作物理一致 motion prior，并采用连续 amplitude space 避免 VQ-PAE 离散切换不平滑。

因此新意不能停在“PAE 更适合 motion”。必须落到更窄的问题：**哪类 motion 可以被 phase scaffold 解释，哪类必须靠 residual/detail/contact token 补，失效时怎么诊断**。

### 1.4 HOI 已有强占坑，WalkTheDog 不能直接平移

HOI 近两年已经覆盖多个关键层面：

- [[analysis/ICLR_2026/Unleashing_Guidance_Without_Classifiers_for_Human_Object_Interaction_Animation.md|LIGHT]]：body / hand / object 分模态，引导接触和物体运动。
- [[analysis/SIGGRAPH_ASIA_2025/MaskedManipulator_Versatile_Whole_Body_Manipulation.md|MaskedManipulator]]：spatio-temporal goal-conditioning 扩到物体操作。
- [[analysis/ICLR_2026/Human_Object_Interaction_via_Automatically_Designed_VLM_Guided_Motion_Policy.md|VLM-RMD]]：用 VLM 构造 relative movement dynamics 目标和奖励。
- `HOIDiNi`：object-centric phase 决定 contact blueprint，human-centric phase 实现全身动作。
- `Uni-HOI`：text、human motion、object motion 经 motion-specific VQ-VAE token 化后交给 LLM 联合建模。
- `UniHM`：进一步把 human motion、object interaction 和 indoor scene 绑定建模，说明 HOI 已经进入 scene-aware object interaction 生成阶段。

剩余窄切口不是“VQ-PAE 做 HOI”，而是：

- 周期或准周期协同任务中的 phase scaffold，例如推箱子步态同步、双人循环舞步、人-机器同频搬运；
- 将 phase code 只作为 coarse temporal scaffold，把 contact lifecycle、object 6DoF、hand detail 和物理可行性交给独立 token / critic / controller；
- 用 PAE/VQ/SAE 诊断 HOI 失败，而不是直接生成完整 HOI。

## 2. PAE / VQ / VAE / SAE 的真实分工

| 表征                     | 最适合解决的问题                                                          | 不适合承担的问题                     | 剩余新意                                              |
| ---------------------- | ----------------------------------------------------------------- | ---------------------------- | ------------------------------------------------- |
| `PAE / phase manifold` | 周期或准周期 motion 的 temporal alignment、phase/frequency 解耦、跨角色/跨形态阶段对齐 | 非周期转场、长程语义规划、精细接触、逐帧高保真重建    | 作为 coarse rhythm / phase scaffold，而不是完整 tokenizer |
| `VQ / codebook`        | 离散动作 primitive、robust tokenization、多模态选择、控制接口                     | 高频手部细节、连续风格 nuance、稀有动作、复杂接触 | 放在 residual / body-part / contact 层，而不是单一窄码本      |
| `VAE / cVAE`           | 部分约束补全、多解采样、masked inpainting、连续 residual                         | 强约束下易平均化，细节发糊                | 接在 phase / VQ 后做 continuous residual repair       |
| `SAE`                  | 可解释诊断、发现节奏/风格/接触/部位稀疏因子                                           | 直接当高保真 motion generator 主干   | 作为 latent / residual / failure factor probe       |

可取的组合不是“表征大杂烩”，而是分层职责清楚：

1. `PAE` 负责粗节奏和阶段对齐。
2. `VQ / FSQ / LFQ` 负责局部离散 primitive 或 body-part token。
3. `VAE / cVAE` 负责连续 residual、masked completion 和多解补全。
4. `SAE` 只做诊断和可解释控制，不直接声称提升生成质量。

这个分工能解释用户的舞蹈实验：`PAE+VQ` 如果只用一个窄 codebook 同时承载全局节奏、局部手脚细节、转场、音乐语义和风格 nuance，重建差是预期风险，不一定是实现错误。

## 3. 为什么 `PAE+VQ` 做舞蹈重建可能很差

### 3.1 方法假设层面

- `PAE` 偏好周期或准周期结构；复杂舞蹈有停顿、爆发、转身、非周期转场、局部异步。
- 单一 phase 难表达手、脚、躯干不同频率；舞蹈常需要 multi-channel 或 hierarchical phase。
- 窄 `VQ` codebook 强化对齐但牺牲重建；WalkTheDog 的价值是跨形态 alignment，不是逐帧高保真压缩。
- 最近邻量化会吞掉连续风格 nuance，尤其是手臂 flourish、躯干 wave、脚尖细节。

### 3.2 数据域层面

- 舞蹈风格、音乐节拍、动作密度和转场模式远复杂于 locomotion。
- 如果切窗没有覆盖完整乐句或 beat bar，phase 会学到碎片周期。
- 手部、脚部、躯干局部细节噪声高，codebook 容易把噪声和真实风格混在一起。
- 音乐条件、队形、leader-reactor 关系若没有进入 latent，PAE/VQ 只能压缩骨架轨迹。

### 3.3 实现层面

- codebook size、commitment loss、code reinitialization、usage balance 对 VQ-PAE 很敏感。
- window length 若与舞蹈节拍错位，会导致相位漂移。
- root normalization、rotation representation、velocity/position loss 权重不当会放大滑步或旋转误差。
- decoder 太弱会恢复不了复杂姿态；decoder 太强又可能绕过 codebook。

### 3.4 评估目标层面

- 若目标是 reconstruction MPJPE，窄 VQ-PAE 天然吃亏；它更像 alignment/compression scaffold。
- 舞蹈质量还要看 beat alignment、style consistency、foot contact、hand detail、body wave，而不只是逐帧 L2。
- 对齐好不等于重建好。WalkTheDog 的成功点是 shared semantic phase，不是压缩所有细节。

### 3.5 最小诊断实验

1. `PAE without VQ`、`VQ-PAE`、`VQ-VAE`、`residual VQ`、`hierarchical VQ/FSQ` 做同数据对照。
2. 按 periodicity 分桶：locomotion-like loop、重复舞步、非周期转场、手部 flourish，分别看误差。
3. 扫 codebook size、commitment loss、reinitialization，记录 code usage、perplexity、dead code、phase drift。
4. 做 body-part error map：root、legs、feet、arms、hands、torso 分开看。
5. 比较 beat-aligned window 和 fixed-length window。
6. 用 high-frequency energy loss、foot-contact loss、beat alignment、style retrieval 作为 `diagnostic`，不要把它们当最终评价。

## 4. Jianhong Bai 路线能给 motion 的真实启发

Jianhong Bai 相关路线不应浅层理解为“把 camera control 搬到 motion control”。更有价值的抽象是：**把原本被当作 nuisance 的观察轴、视角轴、历史上下文和语义规划空间，显式变成数据构造、条件注入和评价闭环**。

### 4.1 可迁移抽象

- `SynCamMaster`：multi-view synchronization module + camera extrinsic embedding + cross-view attention，目标是在多视角下保持外观、几何和动态一致。
- `ReCamMaster`：frame-dimension conditioning，把 source/reference video token 与 target/noise token 沿 frame dimension 拼接，让 3D self-attention 自己做时空同步。
- `CamCloneMaster`：reference-based camera control，不要求用户写显式 camera parameters，而是从参考视频复制 camera style。
- `Context as Memory`：长视频不是靠无限 context，而是检索历史 scene context 做一致性约束。
- `SemanticGen`：先在 compact semantic space 做全局规划，再映射到 VAE latent 补高频细节。
- `RoboMaster`：把机器人操作视频拆成前交互、交互、后交互阶段，并分配 motion dominance，缓解多对象交互特征纠缠。

### 4.2 Motion 里的对应缺口

- 3D motion 评估通常默认 canonical/world coordinates，很少问同一动作在 front、side、orbit、follow、low-angle 下是否仍可读且一致。【动作数据是smplx等3d骨架格式，自然在不同视角下都是可读的，没有视角的失真问题，除非动作本身失真】
- 视频 motion control 已经拆 camera motion 和 object motion，但 3D human motion 侧缺 camera-aware generation/evaluation 闭环。【动作生成领域目前只关注动作本身的质量高低，后续就能导入渲染引擎进行多视角的观察，因此相机在动作生成中不是核心信息。除非重心放在相机轨迹、分镜生成】
- 多视角是 motion 的天然 evaluator：如果一个 3D motion 只在正面好看，换视角后脚滑、朝向错、交互关系崩坏，说明 motion 本身或 motion-to-video 渲染不稳。【多视角观察更多是视频生成领域的需求，动作生成产出的是标准空间中的3d动作序列】
- 长序列 motion 也需要 memory：相同角色、风格、节奏、接触对象、空间关系应跨窗口保持，而不是每个窗口重新采样。
- 复杂动作可先在 compact semantic/contact space 规划，再生成高频关节细节；这比直接在全关节轨迹空间做长程扩散更可控。

### 4.3 可行迁移方向

1. **MV-MotionEval / Camera-aware MotionEval**：同一 3D motion 渲染成多视角 2D pose/video，用 view-consistency、semantic visibility、reprojection stability、text-motion retrieval variance 评价动作是否真正 3D 一致。
2. **Reference-camera-conditioned Motion**：用户给一段 reference video 的 camera style，模型生成 3D motion + camera trajectory，并保持动作语义可读；重点是 camera 作为 observation condition，而非纯镜头特效。
3. **Semantic-Memory Motion Planning**：先生成 event/contact/body-part 级 compact plan，检索历史 motion memory 保持长序列一致，再交给 motion decoder 生成高频细节。
4. **Stage-Dominance HOI**：借 RoboMaster 的阶段 dominance，把 approach、engagement、release 中 human root、hands、object 6DoF、camera/view 的主导权分开建模。

## 5. 推荐写成 paper idea 的方向

### 5.1 Idea A: `ProbeEdit`，预训练 motion diffusion 的可解释连续编辑

一句话定位：在已有 T2M diffusion 上发现可解释 latent / attention / condition directions，并用 time-joint diagnostic evaluator 做连续、少 mask、保上下文的编辑。

已有边界：

- MotionCLR 已证明 attention 可用于 training-free editing，但需要手动控制，且主要是单人。
- InterEdit / PartMotionEdit 做有监督编辑，但依赖编辑三元组，长序列空间关系仍会漂移。
- MotionCritic 给全局偏好分，不足以定位失败窗口和关节。

核心机制：

1. 在 denoising latent、condition embedding offset、cross-attention、self-attention texture space 中抽取候选方向。
2. 用 NoiseCLR / attribution 风格的对比或干预发现跨样本稳定方向，例如速度、幅度、左右手参与、跳跃高度、接触强度。
3. 训练或构造 `<source motion, edit instruction, edited motion>` 三元组诊断器，输出 time-window / body-part / joint 级别反馈。
4. 诊断器只作为 `diagnostic` 和 `dev_metric`，最终用盲人评、独立 text-motion evaluator、foot contact / non-target preservation 交叉验证。

最小实验：

- 选 MoLingo、MDM、MotionDiffuse 或可访问 hidden state 的 T2M backbone。
- 构造 50-100 个属性编辑 prompt pairs：更快、更慢、更大幅度、只改右手、保留左腿、计数变化。
- 比较 prompt-only edit、MotionCLR attention edit、PCA/ICA direction、NoiseCLR direction。
- 做 causal intervention：改变一个方向后检查其他属性是否保持。

主要风险：

- latent direction 纠缠，速度、风格、接触一起变化。
- 诊断器学到数据偏见，奖励错误但“看起来像”的动作。
- 若 backbone hidden state 不开放，工程成本上升。

短期优先级：高。它最少依赖新数据和仿真系统。

### 5.2 Idea B: `DancePhaseProbe`，舞蹈/协同动作的分层 phase-residual 表征诊断【我不做舞蹈生成了，这里提及只是为了说明我尝试过PAE+VQ，但效果不好这个事实而已】

一句话定位：不把 PAE+VQ 当通用 tokenizer，而是建立舞蹈和周期协同任务的 phase/residual/contact 分层诊断框架，判断哪些动作由 phase scaffold 解释，哪些必须靠 residual token 或连续 decoder 修复。

已有边界：

- DeepPhase、WalkTheDog、FunPhase、POMP 已经证明 phase manifold 对 alignment、generation、reconstruction、physics consistency 有价值。
- Uni-HOI 和 UniHM 已经覆盖 HOI 中 text/human/object tokenization 与 scene-aware object interaction 生成。
- REACTDANCE / MotionBricks 类工作已经说明高保真长舞蹈需要分层或模块化 representation。

核心机制：

1. 将 motion 拆成 `global rhythm phase`、`body-part residual token`、`foot/contact token`、`style/detail continuous residual`。
2. 用 PAE 只建模粗节奏和阶段；用 residual VQ/FSQ/LFQ 表示手脚和局部 primitive；用 VAE/cVAE 修复连续细节。
3. 在 latent 和 decoder residual 上训练 SAE-style temporal probes，标出 failure factor：foot-slide、arm-flourish loss、turning transition、beat mismatch、contact miss。
4. 对 HOI 只做窄扩展：在周期协同或阶段明显的任务中使用 phase scaffold，例如推箱子同频、双人循环舞步、人-机器同步搬运；完整 hand-object contact 交给 object/contact tokens 与 physics critic。

最小实验：

- 数据：一组舞蹈片段 + locomotion-like loop + 非周期转场，最好有 beat 或音乐边界。
- 对照：PAE、VQ-PAE、VQ-VAE、residual VQ、hierarchical tokenization。
- 指标角色：MPJPE / reconstruction error 为 `dev_metric`，beat alignment、body-part error、code usage、phase drift、foot contact 为 `diagnostic`；最终用人审和风格/节奏一致性 cross-check。
- HOI 小样例：选低接触、周期性强的协同任务，只验证 phase scaffold 是否改善 timing，不宣称解决完整 HOI。

主要风险：

- 舞蹈数据和音乐条件不足时，phase 分解只会学到噪声周期。
- 分层表征可能工程复杂，但提升只体现在局部指标。
- 若直接和 FunPhase / UniHM 正面对比，必须强调“失效诊断 + 分层修复”，不能只比重建。

短中期优先级：中高。它直接回应用户 PAE+VQ 实验失败经验，也有明确诊断实验。

### 5.3 Idea C: `MV-MotionEval`，camera / multiview 作为 motion 一致性评价和生成约束

一句话定位：把 camera/viewpoint 从 motion 里的隐藏 nuisance 变成显式评价轴和训练约束，检查同一 3D motion 在多视角下是否语义可读、几何一致、交互稳定。

已有边界：

- MotionCtrl、MotionCanvas、ReCamMaster、SynCamMaster、CamCloneMaster 已在视频侧推进 camera/object/multiview control。
- 3D motion generation 侧通常仍在 canonical skeleton 坐标评估，缺少 view-dependent semantic visibility 和 multiview consistency。
- 现有 motion 指标如 FID、R-precision、MPJPE 很难发现“只在某个视角好看”的动作。

核心机制：

1. 用 AMASS/HumanML3D/InterHuman 渲染同一 motion 的 front、side、back、orbit、follow、low-angle 等视角。
2. 设计三类诊断：2D reprojection consistency、view-conditioned action readability、text-motion retrieval variance。
3. 将 SynCamMaster 的 cross-view synchronization 思路迁移为 motion-side multi-view consistency regularizer。
4. 扩展到 reference-camera-conditioned motion：参考视频只提供 camera style，motion 语义由文本或动作计划决定。
5. 长序列版本引入 Context-as-Memory：检索历史 motion / camera / contact context，约束跨窗口一致。

最小实验：

- 100 条 HumanML3D/AMASS motion，渲染 6 个视角。
- 比较 GT、T2M baseline、编辑后 motion、物理修复 motion 的 view-consistency variance。
- 让 VLM / 2D pose estimator / text-motion retriever 只作为 `diagnostic`，最终以人工盲评和独立 evaluator cross-check。
- 做 ablation：单视角评价 vs 多视角评价；canonical-only training vs multiview regularization；explicit camera script vs reference-camera embedding。

主要风险：

- 渲染和 2D pose estimator 的误差会污染评价。
- VLM 对动作细节不稳，不能直接当 final evaluator。
- 如果只做“加 camera 条件”，会被视频 camera control 工作压住；必须强调 motion 侧 3D 一致性和评价缺口。

中期优先级：中高。数据构造可控，且和视频生成前沿有清晰差异。

### 5.4 长期备选：`TreeGRPO-Move`，条件嵌入空间中的物理适应

一句话定位：把预训练流式 motion diffusion 的 condition embedding perturbation 当作在线动作空间，用物理反馈做树状信用分配，实现低成本物理适应。

保留原因：

- MaskedMimic / MoConVQ / SuperPADL 说明物理控制很强，但开放文本、实时低延迟、环境泛化仍难。
- AC3D 启发 “probe-then-inject”，TreeGRPO 启发扩散或序列生成中的 credit assignment。

进入条件：

- 先证明 condition embedding offset 能单调控制速度、方向、接触或平衡，且不会破坏语义。
- 先做短窗口、简单环境、best-of-N / greedy embedding search，对照 no adaptation 和 post-processing。
- 物理 reward 只能作为 `dev_reward` 或 `selection`；最终看 held-out environment success、fall/contact violation、独立 realism evaluator 和人评。

优先级：长期。工程重，不建议先投入全部资源。

## 6. 推荐执行顺序

### 6.1 立即做：`ProbeEdit`

1. 选一个可访问 hidden / attention / latent 的 T2M backbone。
2. 构造 20-50 个 pilot edit cases：幅度、速度、部位、方向、计数、非目标保持。
3. 做最小 intervention：condition offset、attention scaling、latent direction。
4. 建立局部诊断协议，明确 `diagnostic`、`dev_metric`、`final_eval` 分离。

成功标准：

```text
同一个方向能跨样本稳定改变目标属性；
非目标局部保持优于 prompt-only/edit baseline；
诊断器定位的失败窗口与人审一致性高于全局 evaluator。
```

### 6.2 并行做小诊断：`DancePhaseProbe`

1. 复现或整理用户已有 PAE+VQ 舞蹈重建结果。
2. 加入 PAE without VQ、VQ-VAE、residual VQ、hierarchical token baseline。
3. 做 body-part / beat / periodicity 分桶，先找失败根因。
4. 只在诊断成立后，再考虑提出分层 tokenizer。

成功标准：

```text
能明确证明错误来自 phase 假设、VQ 量化、decoder 容量、窗口节拍错位或数据域；
分层 residual/detail token 对具体失败桶有稳定改善；
不是只在平均 MPJPE 上小幅提升。
```

### 6.3 中期推进：`MV-MotionEval`

1. 用现成 SMPL/joint renderer 渲染多视角 motion。
2. 先做 evaluator，不急着训练 generator。
3. 对 GT、baseline、edit output、physics output 做排序 sanity check。
4. 若 evaluator 能发现单视角指标漏掉的问题，再做 multiview regularization 或 reference-camera-conditioned generation。

成功标准：

```text
多视角诊断能识别 canonical 指标漏掉的语义不可读、脚滑、朝向错、交互崩坏；
指标与人审或独立 evaluator 有正相关；
同一 evaluator 没有同时作为 tuning reward 和 final claim。
```

## 7. 候选论文定位

### 7.1 `ProbeEdit`

```text
现有 motion editors 要么依赖手动 mask/attention，要么依赖有监督 edit triplets。
我们证明预训练 motion diffusion 中已有可复用的 latent edit directions，
但可靠编辑需要 time-joint 级诊断反馈。
因此我们提出 direction discovery + localized diagnostic feedback 的闭环编辑框架，
实现少 mask、连续、保上下文的 motion editing。
```

### 7.2 `DancePhaseProbe`

```text
PAE/VQ 在跨形态对齐和周期运动中有效，但不是通用高保真 motion tokenizer。
我们把舞蹈和协同动作拆成 phase scaffold、body-part residual token、
contact token 和 continuous detail residual，并用 sparse temporal probes 诊断失效来源。
该框架解释 PAE+VQ 何时失败，并给出针对性修复，而不是盲目扩大 codebook。
```

### 7.3 `MV-MotionEval`

```text
当前 text-to-motion 评估大多发生在 canonical 3D 坐标中，
无法发现只在单视角成立的动作语义、交互和物理伪影。
我们把 camera/viewpoint 作为显式评价轴，将同一 3D motion 投影到多视角，
用 view consistency、semantic visibility 和 reprojection stability 诊断 motion 质量，
并进一步把多视角一致性转化为生成约束。
```

## 8. 路线漂移记录

old_plan -> new_plan -> evidence -> affected_docs -> next_action

```text
MoLingo/SAE direct improvement
-> pass or downgrade
-> UniMotion/MoLingo/Event-T2M already cover frame-level and event-level semantic injection
-> this note
-> focus on editing/evaluation/representation failure/multiview constraints
```

```text
MotiF-style key joint/segment weighted training
-> only keep if converted into diagnostic/editing feedback
-> MotiF and Motion Attribution show motion focus is valuable, but direct velocity weighting is likely incremental
-> ProbeEdit
-> test event/contact/frequency-aware focus against raw velocity focus
```

```text
AC3D-style pretrained implicit ability injection
-> probe-then-inject, not direct layer/time-step copying
-> AC3D depends on camera-specific low-frequency structure; motion needs separate probing
-> ProbeEdit and TreeGRPO-Move
-> run scope probes before proposing control injection
```

```text
ReMoFuse pseudo-interaction
-> remove as candidate idea
-> user explicitly rejected it; pseudo interaction from single-person motion is no longer a strong gap
-> this note
-> retain only counterfactual composition as diagnostic shortcut test
```

```text
WalkTheDog -> generic HOI
-> narrow to cyclic/coordinated phase scaffold and failure diagnostics
-> Uni-HOI/UniHM/HOIDiNi/LIGHT/MaskedManipulator already occupy broad HOI tokenization/contact generation
-> DancePhaseProbe
-> test only low-contact or phase-dominant coordination first
```

```text
Jianhong Bai camera-control analogy
-> map to multiview evaluation, reference-camera-conditioned observation, semantic-memory planning
-> SynCamMaster/ReCamMaster/CamCloneMaster/Context-as-Memory/SemanticGen provide data/conditioning/memory abstractions
-> MV-MotionEval
-> build evaluator before training camera-aware generator
```

## 9. 关键证据索引

本地 analysis：

- [[analysis/3DV_2025/UniMotion_Unifying_3D_Human_Motion_Synthesis_and_Understanding.md|UniMotion]]
- [[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]
- [[analysis/ICLR_2026/Event_T2M_Event_level_Conditioning_for_Complex_Text_to_Motion_Synthesis.md|Event-T2M]]
- [[analysis/CVPR_2026/ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning.md|ActionPlan]]
- [[analysis/arxiv_2024/MotionCLR_Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training-free_Editing.md|MotionCLR]]
- [[analysis/arxiv_2026/InterEdit_Navigating_Text_Guided_Multi_Human_3D_Motion_Editing.md|InterEdit]]
- [[analysis/ICLR_2025/MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions.md|MotionCritic]]
- [[analysis/TOG_2022/DeepPhase_periodic_autoencoders_for_learning_motion_phase_manifolds.md|DeepPhase]]
- [[analysis/SIGGRAPH_2024/WalkTheDog_Cross_Morphology_Motion_Alignment_via_Phase_Manifolds.md|WalkTheDog]]
- [[analysis/TOG_2024/MoConVQ_Unified_Physics_Based_Motion_Control_via_Scalable_Discrete_Representations.md|MoConVQ]]
- [[ReactDance_Hierarchical_Representation_for_High_Fidelity_and_Coherent_Long_Form_Reactive_Dance_Generation|REACTDANCE]]
- [[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.md|MotionBricks]]
- [[analysis/ICLR_2026/Temporal_Sparse_Autoencoders_Leveraging_the_Sequential_Nature_of_Language_for_Interpretability.md|Temporal SAE]]
- [[analysis/ICLR_2026/Unleashing_Guidance_Without_Classifiers_for_Human_Object_Interaction_Animation.md|LIGHT]]
- [[analysis/SIGGRAPH_ASIA_2025/MaskedManipulator_Versatile_Whole_Body_Manipulation.md|MaskedManipulator]]
- [[analysis/ICLR_2026/Human_Object_Interaction_via_Automatically_Designed_VLM_Guided_Motion_Policy.md|VLM-RMD]]
- [[analysis/ICLR_2026/UniHM_Unified_Dexterous_Hand_Manipulation_with_Vision_Language_Model.md|UniHM]]
- [[analysis/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.md|ReCamMaster]]
- [[analysis/ICLR_2025/SynCamMaster_Synchronizing_Multi_Camera_Video_Generation_from_Diverse_Viewpoints.md|SynCamMaster]]
- [[analysis/SIGGRAPH_ASIA_2025/CamCloneMaster_Enabling_Reference_based_Camera_Control_for_Video_Generation.md|CamCloneMaster]]
- [[analysis/SIGGRAPH_ASIA_2025/Context_as_Memory_Scene_Consistent_Interactive_Long_Video_Generation_with_Memory_Retrieval.md|Context as Memory]]
- [[analysis/arxiv_2025/SemanticGen_Video_Generation_in_Semantic_Space.md|SemanticGen]]

网页补充：

- [ReCamMaster](https://arxiv.org/abs/2503.11647)
- [SynCamMaster](https://arxiv.org/abs/2412.07760)
- [CamCloneMaster](https://arxiv.org/abs/2506.03140)
- [Context as Memory](https://arxiv.org/abs/2506.03141)
- [SemanticGen](https://arxiv.org/abs/2512.20619)
- [FunPhase](https://arxiv.org/abs/2512.09423)
- [POMP](https://openaccess.thecvf.com/content/CVPR2025/papers/Ji_POMP_Physics-consistent_Motion_Generative_Model_through_Phase_Manifolds_CVPR_2025_paper.pdf)
- [HOIDiNi](https://arxiv.org/abs/2506.15625)
- [Uni-HOI](https://arxiv.org/abs/2604.27491)
- [UniHM](https://arxiv.org/abs/2505.12774)
