---
title: MotionFix 相关工作、数据完整性与 Motion Editing 对比
created: 2026-05-08T23:55:00+08:00
updated: 2026-05-14T20:18:00+08:00
status: checked
tags:
  - research-summary
  - Motion_Editing
  - MotionFix
  - related-work
  - dataset-audit
source_papers:
  - "[[paperAnalysis/Motion_Editing/SIGGRAPH_Asia_2024/2024_MotionFix_Text_Driven_3D_Human_Motion_Editing]]"
  - "[[paperAnalysis/Motion_Editing/ICCV_2023/2023_PoseFix_Correcting_3D_Human_Poses_with_Natural_Language]]"
  - "[[paperAnalysis/Motion_Generation/ECCV_2022/2022_PoseScript_3D_Human_Poses_from_Natural_Language]]"
  - "[[paperAnalysis/Human_Perception/ECCV_2024/2024_PoseEmbroider_Towards_a_3D_Visual_Semantic_aware_Human_Pose_Representation]]"
  - "[[paperAnalysis/Motion_Generation/ICCV_2023/2023_TMR_Text_to_Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis]]"
  - "[[paperAnalysis/Motion_Editing/SIGGRAPH_2024/2024_Iterative_Motion_Editing_with_Natural_Language]]"
  - "[[paperAnalysis/Motion_Editing/AAAI_2023/2023_FLAME_Free_form_Language_based_Motion_Synthesis_and_Editing]]"
  - "[[paperAnalysis/Motion_Editing/CVPR_2025/2025_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Prediction]]"
  - "[[paperAnalysis/Motion_Editing/CVPR_2025/2025_MotionReFit_Dynamic_Motion_Blending_for_Versatile_Motion_Editing]]"
  - "[[paperAnalysis/Motion_Generation/ICCV_2025/2025_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation_and_Editing]]"
  - "[[paperAnalysis/Motion_Editing/arXiv_2024/2024_Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training_free_Editing]]"
  - "[[paperAnalysis/Motion_Editing/arXiv_2025/2025_PartMotionEdit_Fine_Grained_Text_Driven_3D_Human_Motion_Editing_via_Part_Level_Modulation]]"
  - "[[paperAnalysis/Motion_Editing/arXiv_2026/2026_InterEdit_Navigating_Text_Guided_Multi_Human_3D_Motion_Editing]]"
  - "[[paperAnalysis/Motion_Editing/arXiv_2026/2026_ExpertEdit_Learning_Skill_Aware_Motion_Editing_from_Expert_Videos]]"
  - "[[paperAnalysis/Motion_Editing/arXiv_2026/2026_A_Unified_Conditional_Flow_for_Motion_Generation_Editing_and_Intra_Structural_Retargeting]]"
  - "[[26夏游方案-forme]]"
---

# MotionFix 相关工作、数据完整性与 Motion Editing 对比

> [!abstract] 结论先行
> MotionFix GitHub 仓库本身不包含完整数据文件，只提供 Google Drive 下载脚本和链接；本地 `/data/Life Me/Coding/Github/motionfix/data/motionfix-dataset` 看起来已经包含论文发布的 processed dataset。`.pth.tar` 在这里不是 checkpoint，而是 joblib/pickle 风格的处理后运动三元组数据，包含 `motion_source`、`motion_target` 和 `text`。只靠 JSON 文本、TMED checkpoint 和 TMR evaluator 不能重建完整训练对；TMR 主要用于候选对挖掘和检索评估，不是数据生成器。
>
> 2026-05-14 补充：PoseScript/PoseFix 已按 `posefix` 分支接到本 vault 的 `linkedCodebases`，并在 HumanML3D-E-MP sample `011798` 上跑通了 snippet-level PoseFix paircode caption adapter。它可作为几何侧 `cross_check`，但不能替代动态视频/轨迹 evaluator。

## 0. Scope

筛选标准：

1. MotionFix Semantic Scholar 的 reference / citation 中，与 text-driven 3D human motion editing、motion-language alignment、motion-pair mining、pose/motion semantic representation 直接相关。
2. 2026 年以前优先保留已中稿顶会/主会工作；2025/2026 未中稿 arXiv 只在它们直接扩展 MotionFix benchmark 或定义新 motion-editing 任务时纳入。
3. 本文的“核心程度”是对 MotionFix 研究线的实用相关度，不等于论文影响力排序。

核心程度标记：

| 标记  | 含义                                                    |
| --- | ----------------------------------------------------- |
| S   | 直接定义或改进 motion editing 任务、数据、benchmark 或 MotionFix 基线 |
| A   | 关键语义对齐/生成/控制基础，对 motion editing 方法设计有直接支撑             |
| B   | 相关生成/控制工作，可作为 baseline、组件或历史上下文                       |

本地笔记索引：

- [[paperAnalysis/Motion_Editing/SIGGRAPH_Asia_2024/2024_MotionFix_Text_Driven_3D_Human_Motion_Editing|MotionFix]]
- [[paperAnalysis/Motion_Editing/ICCV_2023/2023_PoseFix_Correcting_3D_Human_Poses_with_Natural_Language|PoseFix]]
- [[paperAnalysis/Motion_Generation/ECCV_2022/2022_PoseScript_3D_Human_Poses_from_Natural_Language|PoseScript]]
- [[paperAnalysis/Human_Perception/ECCV_2024/2024_PoseEmbroider_Towards_a_3D_Visual_Semantic_aware_Human_Pose_Representation|PoseEmbroider]]
- [[paperAnalysis/Motion_Generation/ICCV_2023/2023_TMR_Text_to_Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis|TMR]]
- [[paperAnalysis/Motion_Editing/SIGGRAPH_2024/2024_Iterative_Motion_Editing_with_Natural_Language|Iterative Motion Editing]]
- [[paperAnalysis/Motion_Editing/AAAI_2023/2023_FLAME_Free_form_Language_based_Motion_Synthesis_and_Editing|FLAME]]
- [[paperAnalysis/Motion_Editing/CVPR_2025/2025_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Prediction|SimMotionEdit]]
- [[paperAnalysis/Motion_Editing/CVPR_2025/2025_MotionReFit_Dynamic_Motion_Blending_for_Versatile_Motion_Editing|MotionReFit]]
- [[paperAnalysis/Motion_Generation/ICCV_2025/2025_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm|MotionLab]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_SALAD_Skeleton_aware_Latent_Diffusion_for_Text_driven_Motion_Generation_and_Editing|SALAD]]
- [[paperAnalysis/Motion_Editing/arXiv_2024/2024_Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training_free_Editing|MotionCLR]]
- [[paperAnalysis/Motion_Editing/arXiv_2025/2025_PartMotionEdit_Fine_Grained_Text_Driven_3D_Human_Motion_Editing_via_Part_Level_Modulation|PartMotionEdit]]
- [[paperAnalysis/Motion_Editing/arXiv_2026/2026_InterEdit_Navigating_Text_Guided_Multi_Human_3D_Motion_Editing|InterEdit]]
- [[paperAnalysis/Motion_Editing/arXiv_2026/2026_ExpertEdit_Learning_Skill_Aware_Motion_Editing_from_Expert_Videos|ExpertEdit]]
- [[paperAnalysis/Motion_Editing/arXiv_2026/2026_A_Unified_Conditional_Flow_for_Motion_Generation_Editing_and_Intra_Structural_Retargeting|Unified Conditional Flow]]

## 1. MotionFix Repo 与本地数据审计

### 1.1 GitHub 是否包含完整数据集下载

结论：**不把数据文件放在 repo 里，但包含完整下载入口**。

证据：

- README 的 `Getting MotionFix Dataset` 给了两类入口：annotation JSON 的 Drive 文件，以及 processed ready-to-use data 的 Drive folder。
- `scripts/download_data.sh` 会下载四类内容：`motionfix-dataset`、`tmr-evaluator`、SMPLH body models、TMED checkpoint。
- README 的 data setup 预期结构包含 `motionfix.pth.tar`、`motionfix_val.pth.tar`、`motionfix_test.pth.tar`。
- `configs/data/motionfix.yaml` 默认把 datapath 指到 `data/motionfix-dataset/motionfix.pth.tar`。

因此 repo 的状态更准确说是：**代码开源 + 数据外链公开 + checkpoint 外链公开**，而不是 GitHub 仓库内直接托管完整数据。

### 1.2 本地 `motionfix-dataset` 是否完整

本地目录：

```text
/data/Life Me/Coding/Github/motionfix/data/motionfix-dataset
```

检查结果：

| 文件                          |      大小 | 作用                                         | 状态  |
| --------------------------- | ------: | ------------------------------------------ | --- |
| `motionfix.pth.tar`         | 5.38 GB | train/全量 processed triplets，loader 默认读取    | 存在  |
| `motionfix_val.pth.tar`     |  263 MB | validation processed triplets              | 存在  |
| `motionfix_test.pth.tar`    |  805 MB | test processed triplets，TMR evaluator 默认读取 | 存在  |
| `amt_motionfix_latest.json` | 6.29 MB | AMT annotation metadata，6730 条             | 存在  |
| `splits.json`               |   94 KB | split ids，train 5388 / val 330 / test 1013 | 存在  |

关键判断：

- `splits.json` 总 ID 数为 6731，唯一 ID 也是 6731；`amt_motionfix_latest.json` 为 6730 条。存在一个 train split ID 不在 AMT JSON 里的轻微不一致。
- `motionfix_val.pth.tar` 与 `motionfix_test.pth.tar` 对应 val/test 数量；主数据包在可用 joblib 环境中抽检为 6730 entries。
- 样本字段包含 `motion_source`、`motion_target`、`text`；motion 内含 `rots`、`trans`、`joint_positions`、`timestamp` 等处理后数组。

结论：**本地目录基本可视为 MotionFix 公开 processed dataset 的完整落地版本**。唯一需要记录的 caveat 是 split JSON 多 1 个 train ID；若要严格复现训练，建议在正式训练前检查该 ID 是否被 loader 忽略，或确认论文发布数据的最新 Drive 是否仍一致。

### 1.3 `.pth.tar` 到底是不是数据

这里的 `.pth.tar` **是数据，不是 checkpoint**。

repo loader 直接做：

```python
dataset_dict_raw = joblib.load(ds_db_path)
```

随后 `__getitem__` 读取：

```python
datum["motion_source"]
datum["motion_target"]
datum["text"]
```

而 checkpoint 是另一路：

```text
experiments/tmed/checkpoints/last.ckpt
```

这也是为什么 Drive 文件看起来像 PyTorch checkpoint，但在 MotionFix 里实际作为 processed dataset 使用。

### 1.4 是否能只靠 checkpoint + JSON text + TMR 构造数据对

不能完整重建。

原因：

1. JSON annotation 主要给文本、AMASS provenance、pair metadata、时间戳等，不等于完整 source/target motion tensor。
2. TMR 在 MotionFix 里是候选对挖掘与评估 backbone：用 embedding 找语义接近但不完全相同的 motion pair，并在评估时算 generated-to-target / generated-to-source retrieval。
3. TMED checkpoint 只是模型权重，不能反推训练集中每对 source/target 的真实 motion。

可行但成本高的替代路线是：拿 annotation 里的 AMASS path/timestamp，准备完整 AMASS/SMPLH 依赖，按作者 preprocessing pipeline 重新抽取 motion；这仍然不是“checkpoint+JSON+TMR 自动构造”，而是依赖原始 AMASS 数据和预处理脚本重建。

## 2. Semantic Scholar 核心 reference / citation

已保存来源：

- `paperSources/motionfix_semantic_scholar_references_20260508.json`
- `paperSources/motionfix_semantic_scholar_citations_20260508.json`
- `paperSources/motionfix_semantic_scholar_seed_2026_05_08_20260508_231419/`

说明：`papers-collect-from-web` 对 Semantic Scholar 静态 HTML 抽取到 0 个候选，主要因为页面依赖动态渲染；可复查来源改用 Semantic Scholar Graph API JSON。下表是人工过滤后的核心集合。

### 2.1 MotionFix reference 侧

| Paper                                                                          | Venue         | 核心  | Links                                                                                                                                                                                                          | 中文 TLDR                                                                                      | 中文 abstract                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------ | ------------- | --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PoseFix: Correcting 3D Human Poses with Natural Language                       | ICCV 2023     | S   | [paper](https://arxiv.org/abs/2309.08480); [project](https://europe.naverlabs.com/research/publications/posefix-correcting-3d-human-poses-with-natural-language/); [code](https://github.com/naver/posescript) | 静态 pose editing 的直接前身：从“描述 pose”推进到“描述 A 到 B 的差异”。                                           | 提出 paircodes/super-paircodes，把两个人体 pose 的几何差异离散成可执行 correction text，构建人工和自动 modifier 数据，并训练 text-based pose editing 与 correctional text generation。它不是动态 motion editing，但在“源状态 + 差异文本 -> 目标状态”这一任务形式上与 MotionFix 高度同构。 |
| TMR: Text-to-Motion Retrieval Using Contrastive 3D Human Motion Synthesis      | ICCV 2023     | S   | [paper](https://arxiv.org/abs/2305.00976); [project](https://mathis.petrovich.fr/tmr); [code](https://github.com/Mathux/TMR)                                                                                   | MotionFix 的关键基础设施：用 text-motion retrieval embedding 挖 motion pair，并作为 motion-to-motion 检索评估。 | TMR 用 generative motion synthesis 加强 text-motion 对比学习，得到语义更稳的 motion/text embedding。MotionFix 借它在 AMASS 里找“相似但有可描述差异”的 motion pair，并在评估中用 TMR feature space 衡量 generated-to-target 与 generated-to-source。              |
| Iterative Motion Editing with Natural Language                                 | SIGGRAPH 2024 | S   | [paper](https://arxiv.org/abs/2312.11538); [project/code](https://purvigoel.github.io/iterative-motion-editing/)                                                                                               | LLM 把自然语言编译成 Motion Editing Operators，再由 diffusion infilling 补过渡，特别适合多轮动画精修。                 | 将自由文本先落到可执行 MEO 程序空间，解析成关键帧、关节、速度或相对时刻约束，再用条件扩散补全局部过渡。它牺牲一部分开放表达能力，换来可解释、可回退、可迭代的 motion editing workflow。                                                                                                             |
| FineMoGen: Fine-Grained Spatio-Temporal Motion Generation and Editing          | NeurIPS 2023  | A   | [paper](https://arxiv.org/abs/2312.15004); project/code 未在本轮确认                                                                                                                                                 | 用空间 body-part 与时间 anchor 细化生成控制，是 motion edit 细粒度控制的参考前身。                                    | 通过时空混合注意力和 MoE 将全局文本控制拆到身体部位与时间片段，支持更细粒度的 motion generation/editing。它的价值在于把“局部部位 + 局部时间”的控制问题显式化，和后续 SimMotionEdit/PartMotionEdit 的定位思路相通。                                                                             |
| CoMo: Controllable Motion Generation through Language Guided Pose Code Editing | ECCV 2024     | A   | [paper](https://arxiv.org/abs/2403.13900); [project](https://yh2371.github.io/como/)                                                                                                                           | 把 motion 转成可读 pose code，让 LLM/语言规则直接编辑离散 pose code。                                          | 将 motion 表示为 pose code 序列，并让语言引导 code editing，实现更可解释的 controllable motion generation。它不是 MotionFix 三元组监督路线，但为“语义中间表示 + 可解释编辑”提供了另一条路径。                                                                                 |
| ParCo: Part-Coordinating Text-to-Motion Synthesis                              | ECCV 2024     | A   | [paper](https://arxiv.org/abs/2403.18512); project/code 未在本轮确认                                                                                                                                                 | 六身体部位 token stream + coordination module，服务多部位文本控制。                                          | 将 whole-body motion 离散成多个 body-part token streams，并用协调模块建模部位间通信。它主要做生成，但对 part-level edit 的启发直接，尤其适合分析 PartMotionEdit 的 body-part decomposition。                                                                       |
| TEACH: Temporal Action Composition for 3D Humans                               | 3DV 2022      | B   | [paper](https://arxiv.org/abs/2209.04066); [project](https://teach.is.tue.mpg.de/); [code](https://github.com/athn-nik/teach)                                                                                  | 从单句 motion generation 推到多动作时序组合，用过去动作末端条件化下一动作。                                              | 在 TEMOS 式生成器外加入 past-motion condition，用上一动作末尾若干帧与当前文本共同预测当前动作 latent。它不是编辑模型，但解决 motion sequence composition 与段间过渡，是长时序 editing 需要面对的基础问题。                                                                             |

### 2.2 MotionFix citation / 后续扩展侧

| Paper                                                                                           | Venue      | 核心  | Links                                                                                                                                                 | 中文 TLDR                                                                               | 中文 abstract                                                                                                                                                                                                              |
| ----------------------------------------------------------------------------------------------- | ---------- | --- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SimMotionEdit: Text-Based Human Motion Editing with Motion Similarity Prediction                | CVPR 2025  | S   | [paper](https://arxiv.org/abs/2503.18211); [code](https://github.com/lzhyu/SimMotionEdit)                                                             | 在 MotionFix 上加“帧级相似度预测”辅助任务，让模型先学会哪里该改。                                               | 针对源 motion 与 edit text 难以联合对齐的问题，构造源/目标 motion 的帧级相似度曲线并离散成 3 类监督，训练 Condition Transformer 同时预测 similarity 与生成条件特征。它提升 MotionFix benchmark 上的 target retrieval 与真实感，是 TMED 后最直接的 supervised editor 改进。                   |
| MotionReFit: Dynamic Motion Blending for Versatile Motion Editing                               | CVPR 2025  | S   | [paper](https://arxiv.org/abs/2503.20724); [project](https://awfuact.github.io/motionrefit/); [code](https://github.com/emptybulebox1/motionReFit)    | 用 MotionCutMix 从无标注 motion 动态合成编辑三元组，突破 MotionFix 规模限制。                               | 将 body-part replacement、style transfer 和 fine-grained adjustment 统一到一个 text-guided editor 中。核心是用软掩码在身体部位层面混合 motion，在线生成大量伪三元组；再用自回归 diffusion 和 Body Part Coordinator 缓解组合数据的不协调。                                       |
| SALAD: Skeleton-aware Latent Diffusion for Text-driven Motion Generation and Editing            | CVPR 2025  | A   | [paper](https://arxiv.org/abs/2503.13836); [project](https://seokhyeonhong.github.io/projects/salad/); [code](https://github.com/seokhyeonhong/salad) | 把 latent 做成 skeleton × time 二维结构，并用 cross-attention map 做零样本编辑。                       | 通过骨架时序 VAE 保留 joint-time latent structure，再在 diffusion denoiser 中显式分离 temporal attention、skeleton attention 和 text cross-attention。编辑不是训练一个 MotionFix editor，而是操控 cross-attention 图实现词替换、重加权、镜像等 training-free 操作。       |
| MotionLab: Unified Human Motion Generation and Editing via the Motion-Condition-Motion Paradigm | ICCV 2025  | S   | [paper](https://arxiv.org/abs/2502.02358); [project](https://diouo.github.io/motionlab.github.io/); [code](https://github.com/Diouo/MotionLab)        | 把 source motion、condition 和 target motion 统一成 Motion-Condition-Motion，单模型覆盖生成与编辑。     | 用 rectified flow 和 MotionFlow Transformer 统一文本生成、文本编辑、轨迹生成/编辑、in-between 与风格迁移。它把 MotionFix 从单任务 editor 推到多任务统一框架，核心收益是编辑任务可从生成/轨迹任务共享先验。                                                                                |
| Pay Attention and Move Better / MotionCLR                                                       | arXiv 2024 | A   | [paper](https://arxiv.org/abs/2410.18977); [project](https://lhchen.top/MotionCLR); [code](https://github.com/IDEA-Research/MotionCLR)                | 把 cross-attention 当词-帧对齐器、self-attention 当帧间模式库，靠注意力图做免训练编辑。                          | 重新设计 motion diffusion block，使 timestep 注入、self-attention 和 cross-attention 分工更清晰。作者显示 cross-attention 激活与动作执行时刻高度相关，并通过替换、重加权、平移 attention map 实现原位替换、强调/去强调、擦除和顺序移动。                                                    |
| PartMotionEdit: Fine-Grained Text-Driven 3D Human Motion Editing via Part-Level Modulation      | arXiv 2025 | S   | [paper](https://arxiv.org/abs/2512.24200)                                                                                                             | 在 MotionFix 上继续下钻，从帧级“哪里改”变成部位级“哪个身体部位该改”。                                            | 在源 motion 与 edit text 之间做双向 cross-attention 对齐，并将人体分成 torso、左右臂、左右腿五部分，构造 part-level similarity curve 监督 PMM 预测每个部位每帧的编辑权重。它是 MotionFix/SimMotionEdit 的细粒度部位调制扩展。                                                        |
| InterEdit: Navigating Text-Guided Multi-Human 3D Motion Editing                                 | arXiv 2026 | S   | [paper](https://arxiv.org/abs/2603.13082); [code/data](https://github.com/YNG916/InterEdit)                                                           | 把单人 MotionFix 扩到双人互动编辑，新增 InterEdit3D 三元组数据集。                                         | 定义 Text-guided Multi-human Motion Editing，并基于 InterHuman 构建 5161 个 source-target-text triplets。方法用 plan token 学高层编辑语义，用 frequency token 约束双人同步、交替、接触等互动节律，解决单人 editor 不懂交互结构的问题。                                         |
| ExpertEdit: Learning Skill-Aware Motion Editing from Expert Videos                              | arXiv 2026 | S   | [paper](https://arxiv.org/abs/2604.10466); [project](https://vision.cs.utexas.edu/projects/expert_edit/)                                              | 从 text editing 转向 skill refinement：只用 expert videos，把 novice 关键动作段修得更像专家。             | 不依赖文本、reference clip 或 novice-expert 配对监督。先用 expert motions 训练离散 pose tokenizer 与 masked MotionInfiller，再在 novice motion 的 skill-critical phase 做局部 infilling，保留 root trajectory/orientation，只把技术关键段投影到 expert manifold。 |
| A Unified Conditional Flow for Motion Generation, Editing, and Intra-Structural Retargeting     | arXiv 2026 | A   | [paper](https://arxiv.org/abs/2604.13427)                                                                                                             | 把 text editing 与同拓扑 retargeting 都看成 conditional transport，一套 rectified flow 同时改语义和骨架。 | 以 text condition 与 skeleton condition 双条件建模 motion distribution。推理时改 text 即 zero-shot editing，改 skeleton 即 intra-structural retargeting。它的重点不是 MotionFix 三元组监督，而是统一 generation/editing/retargeting 的条件流视角。               |

## 3. 代码、数据与开源完整性

| Project                  | Code                                                                                                          | Data                                               | Models / ckpt                                     | 完整性判断          | 备注                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------- | -------------- | ------------------------------------------------------------------------------- |
| MotionFix                | [GitHub](https://github.com/atnikos/motionfix)                                                                | Drive processed dataset + annotations              | Drive TMED checkpoint + TMR evaluator             | 完整，需外链下载       | processed `.pth.tar` 数据、split、annotation、本地代码路径均已检查；SMPL/AMASS license 仍需用户自行遵守 |
| PoseScript / PoseFix     | [GitHub](https://github.com/naver/posescript)                                                                 | pose descriptions / modifier data 随项目发布            | 代码为主                                              | 较完整            | 本地已配置 `linkedCodebases/posescript-posefix` -> `/data/Life Me/Coding/Github/Motion/posescript-posefix`，branch `posefix`，commit `f5282b1`；对 MotionFix 是静态 pose-pair 差异语言前身 |
| PoseEmbroider            | [GitHub](https://github.com/naver/poseembroider)                                                              | BEDLAM-Script / BEDLAM-Fix 依项目说明                   | 代码为主                                              | 较完整            | 更偏 representation infrastructure                                                |
| TMR                      | [GitHub](https://github.com/Mathux/TMR)                                                                       | HumanML3D/KIT 等依原始许可                               | model/eval assets 需按 repo 下载                      | 较完整            | MotionFix 自带 evaluator 版本在 `eval-deps`                                          |
| FLAME                    | [GitHub](https://github.com/kakaobrain/flame)                                                                 | AMASS 等需自行申请                                       | repo 含运行脚本                                        | 部分完整           | 代码开源，但原始 motion 数据因 license 不直接提供                                               |
| Iterative Motion Editing | [Project/Code](https://purvigoel.github.io/iterative-motion-editing/)                                         | project 提供数据/示例入口                                  | project 提供                                        | 较完整            | 更偏 graphics workflow，LLM program + diffusion infill                             |
| MotionCLIP               | [GitHub](https://github.com/GuyTevet/MotionCLIP)                                                              | BABEL/SMPL 等需自行准备                                  | repo 说明下载依赖                                       | 部分完整           | 生成/语义编辑基础，不是 MotionFix benchmark editor                                         |
| TEMOS                    | [GitHub](https://github.com/Mathux/TEMOS)                                                                     | KIT/HumanML3D 等需自行准备                               | code/models 页面提供                                  | 较完整            | text-to-motion generation backbone                                              |
| TEACH                    | [GitHub](https://github.com/athn-nik/teach)                                                                   | BABEL 等需自行准备                                       | project/code 可用                                   | 较完整            | temporal composition，非直接 editor                                                 |
| SimMotionEdit            | [GitHub](https://github.com/lzhyu/SimMotionEdit)                                                              | 基于 MotionFix                                       | 未逐项复核 ckpt                                        | 部分完整           | code link 来自论文/检索；训练数据依赖 MotionFix                                              |
| MotionReFit              | [GitHub](https://github.com/emptybulebox1/motionReFit)                                                        | Hugging Face demo data/checkpoints；训练数据依赖多源 motion | [HF](https://huggingface.co/Yzy00518/motionReFit) | 较完整            | repo 明示 demo 所需 checkpoint/data；完整训练数据仍受源数据许可约束                                 |
| SALAD                    | [Project](https://seokhyeonhong.github.io/projects/salad/) / [GitHub](https://github.com/seokhyeonhong/salad) | HumanML3D/KIT                                      | 未逐项复核 ckpt                                        | 部分完整           | 零样本编辑能力来自 attention modulation                                                  |
| MotionLab                | [GitHub](https://github.com/Diouo/MotionLab)                                                                  | 多任务数据依赖 HumanML3D/MotionFix 等                      | repo/project 说明                                   | 较完整            | ICCV 2025 unified framework                                                     |
| MotionCLR                | [GitHub](https://github.com/IDEA-Research/MotionCLR)                                                          | HumanML3D/HVerb 等                                  | 未逐项复核 ckpt                                        | 较完整            | training-free editing 依赖模型 attention                                            |
| PartMotionEdit           | 未见官方 code                                                                                                     | 基于 MotionFix                                       | 未见                                                | 不完整            | 2025 arXiv，核心相关但开源未确认                                                           |
| InterEdit                | [GitHub](https://github.com/YNG916/InterEdit)                                                                 | InterEdit3D download instructions                  | pretrained assets in repo instructions            | 开放中            | 2026 新任务；GitHub 当前可访问并含数据/模型说明                                                  |
| ExpertEdit               | 未见 code                                                                                                       | expert video derived datasets 未见完整开源               | 未见                                                | 项目页开放，代码/数据未确认 | 当前只确认 project page 与 paper                                                      |
| Unified Conditional Flow | 未见 code                                                                                                       | SnapMoGen/Mixamo 派生                                | 未见                                                | 不完整            | 2026 arXiv，偏统一建模视角                                                              |

## 4. Motion Editing 能力对比

| Work                     | 核心  | 编辑接口                                                    | 主要编辑能力                                                                     | 优势特色                                                             | 局限                                                        |
| ------------------------ | --- | ------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------- |
| PoseFix                  | S   | source pose + correction text                           | 静态 3D pose correction；从 pose pair 生成修正文本                                   | paircode/super-paircode 把几何差异变成语言操作；是 MotionFix 的静态先驱            | 不处理动态速度、节奏、接触、长时序                                         |
| FLAME                    | A   | reference motion + text + frame/joint mask              | masked motion inpainting；prediction；in-betweening                          | 早期 diffusion motion editor；生成与局部编辑统一                             | 需要外部 mask；不是 instruction localization                     |
| MotionCLIP               | B   | text/image prompt 或 latent arithmetic                   | semantic latent editing / open vocabulary generation                       | 借 CLIP 语义空间带来开放词汇和可组合 latent                                     | 细粒度时序/部位控制弱；不是 source-target benchmark                    |
| Iterative Motion Editing | S   | source motion + context + iterative text                | 多轮动画精修；关键帧/关节/速度/时刻编辑                                                      | LLM 编译 MEO 程序，diffusion infill 补过渡；可解释可回退                        | 表达受 MEO API 限制；物理/接触语义有限                                  |
| MotionFix / TMED         | S   | source motion + edit text                               | supervised text-driven source-to-target motion editing                     | 首个公开 motion editing triplet benchmark；TMR pair mining + AMT text | 数据 6730 条，长度短；受 TMR 相似 pair 分布约束                          |
| SimMotionEdit            | S   | source motion + edit text                               | 更准确的帧级 edit localization                                                   | similarity prediction 辅助任务让模型知道“哪些帧该改”                           | 仍是全身帧级，不知道具体 body part                                    |
| MotionReFit              | S   | source motion + text                                    | body-part replacement、style transfer、fine adjustment、长序列                   | MotionCutMix 用无标注 motion 在线扩三元组；支持自回归长序列                         | 组合数据有分布偏移；复杂空间/时序推理仍难                                     |
| SALAD                    | A   | prompt edit / attention map edit                        | training-free word replacement、reweighting、attention mirroring             | skeleton-time latent + word-joint-frame attention 可解释            | 依赖 attention alignment；不是 source-target supervised editor |
| MotionCLR                | A   | attention map edit / DDIM inversion                     | training-free in-place replacement、强调、擦除、顺序移动                              | cross-attention 对词-帧，self-attention 对运动模式；编辑成本低                  | 对模糊长文本和物理约束不稳                                             |
| PartMotionEdit           | S   | source motion + edit text                               | part-level fine-grained editing                                            | 五身体部位时序权重 + part-level similarity supervision                    | 需要 MotionFix 三元组；body-part 粒度仍粗                           |
| MotionLab                | S   | source motion 可空 + condition                            | 一模型统一 text generation/editing、trajectory editing、in-between、style transfer | Motion-Condition-Motion + rectified flow；多任务共享先验                 | 单人；训练 curriculum 与多源数据复杂                                  |
| InterEdit                | S   | two-person source motion + edit text                    | 双人互动 motion editing                                                        | plan token 管语义，frequency token 管同步/交互节律；补 InterEdit3D benchmark  | 当前只双人；DCT 频域更擅长节律类关系                                      |
| ExpertEdit               | S   | novice motion + expert-only prior                       | skill-aware refinement，无文本把 novice 改得更 expert-like                         | 不要 paired supervision；局部 critical phase infilling 保轨迹和身份         | 分技术动作训练；依赖 phase heuristic；外部场景/物体未建模                     |
| Unified Conditional Flow | A   | source motion + text/skeleton condition                 | zero-shot text editing + intra-structural retargeting                      | 把 editing 与 retargeting 统一成 conditional transport                | 同拓扑骨架假设；editing 主要靠人评                                     |
| DNO                      | A   | differentiable task loss + diffusion noise optimization | 任意可微约束下的 training-free motion optimization                                 | 把 diffusion initial noise 当可优化 latent，适配多任务约束                    | 慢；需要可微目标；不直接理解自然语言差异                                      |
| CoMo                     | A   | pose code + language-guided code editing                | 可解释 pose-code motion control/editing                                       | 中间表示可读可操作，适合 LLM/规则编辑                                            | code 粒度和规则覆盖限制细节与动态                                       |
| FineMoGen                | A   | fine-grained text/spatio-temporal condition             | 局部时间与部位控制                                                                  | 早期强调 spatio-temporal fine control                                | 主要是 generation/editing hybrid，非 MotionFix triplet editor  |

## 5. 语义对齐基础线

### 5.1 PoseScript -> PoseFix -> MotionFix

这条线的核心是把连续人体几何变成语言可操作的语义单元。

| Work       | 对齐对象                                      | 关键语义单元                                       | 对 MotionFix 的意义                                                              |
| ---------- | ----------------------------------------- | -------------------------------------------- | ---------------------------------------------------------------------------- |
| PoseScript | single static pose ↔ description          | posecodes                                    | 证明 rule-generated body relation text 可以训练 pose-language retrieval/generation |
| PoseFix    | pose A + pose B ↔ modifier                | paircodes / super-paircodes                  | 把语义从“状态描述”推进到“差异操作”，直接对应 source + edit text -> target                        |
| MotionFix  | motion source + motion target ↔ edit text | TMR-mined motion pair + AMT edit instruction | 把 PoseFix 的静态差异语言扩展到动态 motion pair，覆盖速度、时序、方向、体部等编辑                          |

PoseFix 必须加入 motion editing 对比清单，但要标清边界：它是**静态 pose correction**，不是动态 3D motion editor。它的核心价值是任务形式和 comparative language pipeline，而不是直接解决 motion velocity/transition。

### 5.1.1 PoseFix 接到 Motion 数据的试运行

本地配置：

- Code link: [[linkedCodebases/posescript-posefix]]
- External repo path: `/data/Life Me/Coding/Github/Motion/posescript-posefix`
- Branch / commit: `posefix` / `f5282b1`
- Environment: `motionfix` conda env，额外补了 `tabulate`、`nltk` 以满足 PoseFix import。
- Motion data: [[artifacts/modebug_posefix_snippet_caption_20260514/011798/posefix_snippet_results.json]]
- Integrated result: [[artifacts/modebug_posefix_snippet_caption_20260514/011798/gpt_integrated_snippet_caption.json]]
- Adapter scripts: [[scripts/modebug_posefix_snippet_caption.py]], [[scripts/modebug_integrate_posefix_snippet_caption.py]]

适配方式：对 HumanML3D-E-MP 的 22-joint motion 取每个 snippet 的首帧和尾帧，root-center 后送入 PoseFix `paircode / super-paircode` comparative pipeline；root translation 与 torso-lateral yaw 另行统计，再由 GPT 整合成 snippet-level event caption。

关键判断：PoseFix 可以替代 VLM 的一部分 snippet caption 工作，尤其是 body-part geometry、局部 turn、knee/foot/arm change 这些静态差异证据；但它不能替代动态证据。`jog`、step count、contact timing、forward/backward relative to facing 仍需要 trajectory overlay、video 或显式 facing indicator。因此在 MoDebug 里它的角色应是 `cross_check` / `diagnostic`，不是最终 evaluator。

### 5.2 TMR 在 MotionFix 中的角色

TMR 有三个作用：

1. **候选对挖掘**：在 AMASS motion clips 上找语义相近但不完全相同的 pair。
2. **数据甜区过滤**：太近的 pair 没有编辑意义；太远的 pair 难以用一句 edit text 解释。
3. **评估侧 embedding**：generated-to-target / generated-to-source retrieval 在 TMR feature space 中计算。

因此 TMR 是 MotionFix 的 semantic alignment backbone，但不是可从 JSON 和 checkpoint 自动构造数据对的工具。

### 5.3 PoseEmbroider 的补充价值

PoseEmbroider 不直接做 motion editing，但它对后续研究有两个启发：

1. **多模态 pose representation**：image、3D pose、text 任意子集都能汇入一个 global token，适合未来把视频/图像证据接入 motion edit。
2. **instruction generation**：同一 frozen representation 可以服务 pose-pair instruction generation，这和 MotionFix/InterEdit 的 edit text annotation pipeline 有潜在连接。

对 motion edit 来说，它更像一个“语义感知人体 pose encoder”，可作为数据构造、edit instruction generation 或 evaluator 的底层表示候选。

## 6. `papers-collect-from-web` 与 `papers-analyze-pdf` 执行记录

收集：

- Semantic Scholar 页面通过 `papers-collect-from-web` 保存静态 HTML，但静态解析未抽到候选。
- 随后使用 Semantic Scholar Graph API 保存 reference/citation JSON，并人工过滤核心列表。
- `analysis_log.csv` 已追加/更新本次 motion-editing 与语义对齐相关条目，其中本轮新增分析的 10 个 PDF 标为 `checked` 并补齐 `pdf_path`。

本轮按 `papers-analyze-pdf` 结构新增或更新的核心 PDF 笔记：

| Note                                           | PDF                                                                                                                                                           |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Iterative Motion Editing with Natural Language | `paperPDFs/Motion_Editing/SIGGRAPH_2024/2024_Iterative_Motion_Editing_with_Natural_Language.pdf`                                                              |
| FLAME                                          | `paperPDFs/Motion_Editing/AAAI_2023/2023_FLAME_Free_form_Language_based_Motion_Synthesis_and_Editing.pdf`                                                     |
| MotionCLR                                      | `paperPDFs/Motion_Editing/arXiv_2024/2024_Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training_free_Editing.pdf` |
| PartMotionEdit                                 | `paperPDFs/Motion_Editing/arXiv_2025/2025_PartMotionEdit_Fine_Grained_Text_Driven_3D_Human_Motion_Editing_via_Part_Level_Modulation.pdf`                      |
| InterEdit                                      | `paperPDFs/Motion_Editing/arXiv_2026/2026_InterEdit_Navigating_Text_Guided_Multi_Human_3D_Motion_Editing.pdf`                                                 |
| ExpertEdit                                     | `paperPDFs/Motion_Editing/arXiv_2026/2026_ExpertEdit_Learning_Skill_Aware_Motion_Editing_from_Expert_Videos.pdf`                                              |
| Unified Conditional Flow                       | `paperPDFs/Motion_Editing/arXiv_2026/2026_A_Unified_Conditional_Flow_for_Motion_Generation_Editing_and_Intra_Structural_Retargeting.pdf`                      |
| MotionCLIP                                     | `paperPDFs/Motion_Generation/ECCV_2022/2022_MotionCLIP_Exposing_Human_Motion_Generation_to_CLIP_Space.pdf`                                                    |
| TEMOS                                          | `paperPDFs/Motion_Generation/ECCV_2022/2022_TEMOS_Generating_diverse_human_motions_from_textual_descriptions.pdf`                                             |
| TEACH                                          | `paperPDFs/Motion_Generation/3DV_2022/2022_TEACH_Temporal_Action_Composition_for_3D_Humans.pdf`                                                               |

这些笔记由 4 个 gpt-5.4 / xhigh 子代理并行完成，统一检查了 frontmatter、`Part I/II/III`、`### 核心直觉` 和 PDF embed。

## 7. 研究判断

MotionFix 的核心贡献不是 TMED 模型本身多强，而是它把 text-driven 3D motion editing 从“模型 demo”变成了一个可训练、可比较的数据问题。后续工作基本沿三条线推进：

1. **监督式 MotionFix benchmark 提升**：SimMotionEdit、PartMotionEdit 继续把“编辑该发生在哪里”显式化，从帧级推进到部位级。
2. **数据扩展与任务扩展**：MotionReFit 用 MotionCutMix 扩数据，InterEdit 把任务扩到双人互动，ExpertEdit 把文本编辑转成 skill refinement。
3. **training-free / unified control**：SALAD、MotionCLR、Unified Conditional Flow 不一定依赖 MotionFix 三元组，而是把 attention、conditional flow 或 skeleton condition 变成可操控接口。

如果目标是做新的 motion editing 研究，最值得从 MotionFix 继续深挖的空白是：

1. 长时序与多阶段 edit instruction，而不是 3-5 秒片段。
2. body part、time、interaction、contact 的联合定位，而不是只做 frame 或 part。
3. evaluator 分层：TMR retrieval 可作为 side signal，但不能单独升级为最终人类感知/物理合理性的 held-out evaluator。
4. 数据构造自动化：PoseFix/PoseScript/PoseEmbroider 的 rule + representation pipeline 可以和 MotionFix 的 TMR mining 结合，减少 AMT 成本。
