---
created: 2026-05-11T15:53:16+08:00
updated: 2026-05-11T15:53:16+08:00
title: "Visual-Prior-Assisted Text-to-Motion: Selective Video/Image Priors for Fine-Grained Motion Control"
status: draft
tags:
  - research-idea
  - Motion_Generation
  - text-to-motion
  - visual-prior
  - video-prior
  - adapter
  - fine-grained-control
source_papers:
  - "[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches]]"
  - "[[paperAnalysis/Motion_Generation/ECCV_2022/2022_MotionCLIP_Exposing_Human_Motion_Generation_to_CLIP_Space]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_Move_in_2D_2D_Conditioned_Human_Motion_Generation]]"
  - "[[paperAnalysis/Motion_Editing/CVPR_2025/2025_AnyMoLe_Any_Character_Motion_In_Betweening_Leveraging_Video_Diffusion_Models]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diffusion]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_MVLift_Lifting_Motion_to_the_3D_World_via_2D_Diffusion]]"
  - "[[paperAnalysis/Motion_Generation/ICCV_2025/2025_Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation]]"
  - "[[paperAnalysis/Image_Video_Generation/CVPR_2025/2025_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_Generation]]"
  - "[[paperAnalysis/Image_Video_Generation/CVPR_2025/2025_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human_centric_Video_Generation]]"
  - "[[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_MTVCraft_Tokenizing_4D_Motion_for_Arbitrary_Character_Animation]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2025/2025_HMVLM_Human_Motion_Vision_Lanuage_Model_via_MoE_LoRA]]"
  - "[[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions]]"
---

# Visual-Prior-Assisted Text-to-Motion: Selective Video/Image Priors for Fine-Grained Motion Control

> [!abstract] Conclusion
> idea2 的目标应明确为 **text -> motion**，不是 text/image -> video。图像/视频生成框架只提供先验、tokenizer、adapter 或初始化，最终输出仍然是 3D motion。
>
> 原始宽泛表述“把 motion 接到图像/视频生成框架上”已经被 MotionPatch、AnyMoLe、MTVCraft、HMVLM、Being-M0 等工作大幅占据。剩余 ICLR 级空间不在“再接一次”，而在：**选择性地利用视觉/视频先验，并证明它确实提升细粒度 motion 指令跟随，而不是只增加参数量或换表示。**

## 0. Problem Restatement

用户 idea2：

```text
图像生成、视频生成发展很快。动作生成也是一种时序视觉任务。
能否将动作通过 adapter 等方式接到视频生成、图像生成框架上，
将动作视为一种视觉特征，但保留时序约束，
从而利用图像/视频的海量知识先验，获得更强的动作生成和控制，
包括文本细粒度约束。
```

本文将它收窄为：

```text
输入：text instruction
输出：3D human motion / skeleton / SMPL motion
视觉/视频先验角色：辅助 text-to-motion 的表示、条件、初始化、adapter 或评价信号
非目标：直接生成 video，或把 video generation 当最终任务
```

核心问题不是“motion 能不能图像化”，而是：

```text
哪些视觉/视频先验对 text-to-motion 有真实增益？
这些先验如何接入而不破坏 motion 的 time x joint / kinematic structure？
增益是否体现在细粒度文本约束，而不只是 FID / retrieval 的平均改善？
```

## 1. Retrieved Related Work

本节按链路整理本地 KB 证据。完整来源见 frontmatter `source_papers`。

### 1.1 Motion-as-Image / Vision Encoder Transfer

- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches|MotionPatch]]：将 3D skeleton motion 按身体部位切成 `N x N` 伪图像块，`xyz` 对应 RGB，复用 ImageNet ViT-B/16 做 motion encoder，并与文本做对比学习。它证明 image ViT prior 对 motion representation 有用，尤其在数据稀缺和跨骨骼迁移中有效。

边界：MotionPatch 主要是 encoder / retrieval / representation 工作，不是 text-to-motion generator。它把时序压成伪图像纹理，尚未解决细粒度时序控制和生成端约束。

### 1.2 Visual-Language Semantic Space Transfer

- [[paperAnalysis/Motion_Generation/ECCV_2022/2022_MotionCLIP_Exposing_Human_Motion_Generation_to_CLIP_Space|MotionCLIP]]：把 motion autoencoder latent 对齐到 CLIP text/image 空间，支持开放词汇动作生成和编辑。
- [[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]]：明确指出 CLIP 的图像-语言空间是静态视觉语义，不够 motion-aware；因此做 BLIP-2 风格语言-运动预训练，替代 CLIP 作为 T2M 条件编码器。

启示：直接借 CLIP / image prior 的上限有限。idea2 必须提出 motion-aware bridge，否则会被 LaMP 类工作攻击为“静态视觉语义错配”。

### 1.3 2D / Video Data as Motion Prior

- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_MAS_Multi_view_Ancestral_Sampling_for_3D_motion_generation_using_2D_diffusion|MAS]]：用 2D diffusion + 多视角一致性在无 3D 数据下生成 3D motion。
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MVLift_Lifting_Motion_to_the_3D_World_via_2D_Diffusion|MVLift]]：用单视角 2D pose 序列和渐进多视角一致性建立 3D motion。
- [[paperAnalysis/Motion_Generation/ICCV_2025/2025_Motion_2_to_3_Leveraging_2D_Motion_Data_to_Boost_3D_Motion_Generation|Motion-2-to-3]]：从大规模 2D 视频中学习局部运动先验，再通过多视角 diffusion 升维到 3D。

启示：2D / 视频数据补 3D motion 数据瓶颈已经是强赛道。idea2 若只说“用视频数据增强 motion”不够，需要聚焦 **视觉/视频预训练先验如何提升 text-to-motion control**。

### 1.4 Motion as Control Interface for Video Generation

- [[paperAnalysis/Image_Video_Generation/CVPR_2025/2025_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_Generation|HumanDreamer]]：text -> 2D pose -> pose-to-video，说明 pose/motion 是人体视频生成的重要中间控制接口。
- [[paperAnalysis/Image_Video_Generation/CVPR_2025/2025_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human_centric_Video_Generation|TokenMotion]]：在视频 DiT 中把 camera 和 human pose 都编码成时空 token，通过 dynamic mask 融合控制。
- [[paperAnalysis/Image_Video_Generation/ICLR_2026/2026_MTVCraft_Tokenizing_4D_Motion_for_Arbitrary_Character_Animation|MTVCraft]]：将 SMPL 3D motion 量化为离散 4D motion tokens，并插入 video DiT motion attention，驱动任意角色动画视频。

启示：**motion -> video** 已经很强，尤其 MTVCraft 直接占据“motion tokens 接入 video DiT”。idea2 必须反过来强调 **video/image prior -> motion output**，否则会被认为是 MTVCraft 的相邻变体。

### 1.5 Adapter / LoRA Multi-Modal Connection

- [[paperAnalysis/Motion_Generation/NeurIPS_2025/2025_HMVLM_Human_Motion_Vision_Lanuage_Model_via_MoE_LoRA|HMVLM]]：用 MoE-LoRA 和 body-part tokenizer 统一 T2M、HPE、HVU，并用零专家缓解灾难性遗忘。
- [[paperAnalysis/Motion_Generation/ICML_2025/2025_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions|Being-M0]]：百万级 MotionLib + 2D-LFQ motion tokenizer + LLM，验证 motion scaling。

启示：adapter / tokenizer / scaling 本身不是新意。需要把 adapter 的作用限定为 **选择性注入视觉/视频先验以解决 motion-only 模型的可诊断弱点**。

## 2. What Is Already Occupied

| Claim | Status | Pressure |
| --- | --- | --- |
| 把 motion reshape 成图像/patch 后用 ViT | 已被 MotionPatch 占据 encoder/retrieval 版本 | 需要生成端和时序控制新贡献 |
| 把 motion latent 对齐到 CLIP | 已被 MotionCLIP 占据，LaMP 指出 CLIP 不够 motion-aware | 需要 motion-aware bridge |
| 用 2D/video 数据补 3D motion 数据 | MAS/MVLift/Motion-2-to-3 已很完整 | 需要不是数据扩展，而是先验选择与控制 |
| motion token 接 video DiT | MTVCraft 已强占 | idea2 应改成 video prior 辅助 motion，而不是 motion 控 video |
| LoRA/adapter 接多模态 | HMVLM 已占 | adapter 必须有清晰机制和消融 |
| 大规模 motion tokenizer + LLM | Being-M0 已占 | 不宜走纯 scaling claim |

## 3. Remaining ICLR-Level Space

剩余空间集中在一个更窄问题：

```text
Can pretrained visual/video priors improve text-to-motion fine-grained instruction following
when injected selectively through structure-preserving adapters,
and can we identify which priors help which motion constraints?
```

这里有三点是已有工作没有完全解决的：

1. **归因空白**：视觉/视频先验到底帮助了什么？空间结构、身体对称、局部平滑、物体 affordance、还是只是初始化好？
2. **时序保持空白**：MotionPatch 式图像化容易把时间当纹理；video prior 有时序模块，但不懂 `joint topology`。如何保留 `time x joint / body-part` 结构是关键。
3. **细粒度控制空白**：多数工作汇报 FID、R-Precision、FVD 或定性视频效果。对 body-part、order、speed、duration、frequency 的细粒度文本控制仍缺强评估和专门适配。

## 4. Best Research Cuts

### Cut A: Selective Video-Prior Adapter for Fine-Grained Text-to-Motion

核心主张：

```text
视频先验不替代 motion generator，而是通过一个结构保持 adapter
选择性地注入到 text-to-motion 去噪/生成过程，
提升 motion-only 模型最弱的细粒度时序与 body-part 指令跟随。
```

方法轮廓：

1. Base motion generator 保持为 text-to-motion backbone。
2. 将 motion 表示成 `time x body-part x channel` token，而不是 224x224 静态图。
3. 引入 frozen image/video encoder 或 video diffusion temporal block。
4. Adapter 只输出低秩 residual / gate，不直接覆盖 motion token。
5. gate 按文本约束类型选择是否启用视觉/视频先验。

优势：最贴近用户 idea，同时避开“直接做 video generation”。  
风险：需要强消融证明增益来自 pretrained prior，而不是 adapter 参数量。

### Cut B: What Visual Prior Transfers to Motion? A Controlled Study with Minimal Adapter

核心主张：

```text
系统识别 image/video priors 对不同 motion constraints 的贡献，
并提出一个最小 selective adapter 只保留有效先验。
```

比较对象：

1. random ViT / random VideoMAE；
2. ImageNet ViT；
3. DINOv2；
4. VideoMAE / video diffusion temporal module；
5. motion-only encoder；
6. LaMP-like motion-aware text encoder。

评估维度：

- global semantic matching；
- body-part grounding；
- temporal order；
- speed / duration / frequency；
- physical plausibility。

优势：ICLR 喜欢机制清楚的 controlled study。  
风险：若只做报告像 benchmark，需要最终提出原则性 adapter 或 routing rule。

### Cut C: Motion-as-Video-Latent for Text-to-Motion

核心主张：

```text
从 MotionPatch 的 motion-as-image 升级为 motion-as-video-latent，
让 video prior 看到真实时间维，同时通过 skeleton topology mask 保留运动结构。
```

关键区别：

- 不是把 motion 填进 `224x224x3`；
- 而是构造 `T x body-part x feature` 或 `T x joint x channel` 的 pseudo-video latent；
- 用视频 transformer 的 temporal attention 初始化 / regularize；
- 用 kinematic mask 限制不合理跨关节注意力。

优势：表示层 novelty 较强。  
风险：容易被 MTVCraft / Being-M0 压，需要强调目标是 text-to-motion 细粒度控制，不是 video animation 或 scaling。

## 5. Recommended Main Claim

不要写：

```text
We connect motion generation to image/video generation frameworks and obtain a universal motion generator.
```

建议写：

```text
We study when and how pretrained visual/video priors help text-to-motion generation.
We propose a structure-preserving selective adapter that injects visual/video priors
only for fine-grained constraints where motion-only models are weak,
while preserving the motion manifold and temporal-joint structure.
```

中文版本：

```text
我们不是把动作生成改造成视频生成，也不是声称视觉模型天然懂 3D motion。
我们研究视觉/视频预训练先验在 text-to-motion 中的可迁移边界，
并提出一个保留时序-骨架结构的选择性 adapter，
只在细粒度 body-part、顺序、速度、持续时间等约束上注入视觉/视频先验。
```

## 6. MVP Experiment

### 6.1 Dataset

初步验证：

1. HumanML3D / KIT-ML 常规文本；
2. FineMotion / FineMoGen / HumanML3D-E 类细粒度文本，如果本地可用；
3. 额外合成 200-500 条 controlled prompts：
   - body-part: left arm / right leg / head / torso；
   - order: walk then turn, jump then wave；
   - speed: slowly / quickly / accelerate；
   - duration: hold for two seconds, briefly pause；
   - frequency: clap twice, step three times。

### 6.2 Baselines

必须包含同参数量和随机初始化对照：

| Baseline | Purpose |
| --- | --- |
| motion-only generator | 基础 T2M 能力 |
| motion-only + same-size random adapter | 排除参数量收益 |
| ImageNet ViT adapter | 测静态视觉先验 |
| DINOv2 adapter | 测空间结构先验 |
| VideoMAE / video temporal adapter | 测视频时序先验 |
| proposed selective adapter | 测选择性注入是否有效 |

### 6.3 Metrics

平均 FID / R-Precision 不够。必须加入细粒度指标：

1. **body-part correctness**：指定身体部位是否执行目标动作。
2. **event order accuracy**：动作事件顺序是否正确。
3. **duration / speed error**：持续时间、速度曲线与文本约束是否一致。
4. **frequency count error**：重复次数是否正确。
5. **physical sanity**：脚滑、root drift、速度爆炸、关节范围。
6. **human preference**：小规模 paired comparison，作为 final anchor。

### 6.4 Key Ablations

1. pretrained visual/video encoder vs random encoder；
2. frozen prior vs finetuned prior；
3. global CLS token vs patch/token sequence；
4. image prior vs video prior；
5. full injection vs selective gate；
6. with / without kinematic topology mask。

通过条件：

```text
proposed selective adapter 在细粒度约束上显著优于 motion-only 和 random adapter；
增益主要出现在预先定义的弱项，例如 order / body-part / speed；
不牺牲 motion plausibility；
human preference 支持自动指标趋势。
```

## 7. Rejection-Level Risks

### Risk 1: Novelty 被 MTVCraft 压住

批评：

```text
MTVCraft already tokenizes 4D motion and injects it into a video DiT.
This paper is an incremental adapter variant.
```

修复：

1. 强调方向相反：MTVCraft 是 motion -> video animation；本文是 visual/video prior -> text-to-motion output。
2. 实验目标不同：本文评估 3D motion 指令跟随，不评估视频 FVD。
3. 加入 MTVCraft-style tokenizer 作为相关对比或分析对象，而不是假装没发生。

### Risk 2: 只是堆模块

批评：

```text
The method simply attaches a pretrained vision/video model to a motion generator.
The improvement may come from extra parameters.
```

修复：

1. 必须有 same-size random adapter。
2. 必须有 frozen pretrained vs finetuned vs random 对照。
3. 必须报告不同 constraint family 的收益分布。

### Risk 3: 视觉先验和 motion 先验混淆

批评：

```text
The method claims visual prior, but the gains may come from motion-domain data or text encoder changes.
```

修复：

1. 固定 motion generator 和 text encoder。
2. 只替换 adapter prior source。
3. 使用相同训练数据、相同训练步数。

### Risk 4: 细粒度评估不可信

批评：

```text
R-Precision and FID do not prove fine-grained instruction following.
```

修复：

1. 构建 controlled prompt set。
2. 使用 explicit rule-based temporal/body-part metrics。
3. 做 human preference 和 failure case audit。

## 8. Execution Plan

### Phase 1: Diagnostic Study

目标：判断视觉/视频先验是否真的有用。

1. 选一个稳定 T2M backbone。
2. 固定 motion/text pipeline，只换 adapter prior source。
3. 先做 200-500 条 controlled prompts。
4. 输出收益矩阵：

```text
prior source x constraint type -> metric gain / regression
```

### Phase 2: Selective Adapter

目标：把诊断结果转为方法。

1. 根据 constraint type 路由不同先验；
2. 只用低秩 residual 注入；
3. 加 kinematic topology mask；
4. 对比 full-injection 和 selective-injection。

### Phase 3: Paper Claim

目标：形成 ICLR 可辩护主张。

```text
视觉/视频先验不是通用增强器；
它对细粒度时序、身体部位、场景/动作 affordance 有选择性帮助；
结构保持 adapter 能把这类帮助转化为 text-to-motion 的可测增益。
```

## 9. Final Verdict

idea2 值得保留，但必须收窄：

```text
不做：motion 接 video generator 生成视频。
不做：大一统视觉先验动作基础模型。
要做：视觉/视频先验辅助 text-to-motion 的细粒度控制，并通过严格消融证明先验来源。
```

最稳的标题方向：

```text
Selective Video-Prior Adapters for Fine-Grained Text-to-Motion Generation
```

