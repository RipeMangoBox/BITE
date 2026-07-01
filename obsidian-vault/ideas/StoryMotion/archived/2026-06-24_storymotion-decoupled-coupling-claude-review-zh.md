---
title: StoryMotion Decoupled Coupling QA - Claude/Kiro 复查中文整理
hypothesis: Claude/Kiro 复查与后续代码审计共同支持：StoryMotion 的问题应进一步收缩为 camera 表示对 human root 的结构依赖、completion condition dominance 与任务定义混杂；root-first 等方案仍待对照。
status: draft
created: 2026-06-24T22:14:01+08:00
updated: 2026-06-25T19:38:00+08:00
source_notes:
  - "[[2026-06-23_storymotion-decoupled-coupling-qa-v5.1]]"
---

# StoryMotion Decoupled Coupling QA - Claude/Kiro 复查中文整理

> [!note] 整理说明
> 本文是对 Claude/Kiro 反馈的中文整理译文。原反馈中存在明显断行、乱码和字段残缺；本文保留可辨认的技术判断、数值和优先级，按原有结构整理为可读中文。本文不是新增实验结论。

> [!warning] 2026-06-25 follow-up 回填
> 下文 Priority 1 / 2 是 2026-06-24 的审查建议。最新完整数据和重构后的任务定义见 [[2026-06-23_storymotion-decoupled-coupling-qa-v5.1#2026-06-25 follow-up full eval|主 QA follow-up]]。核心变化是：R@K 异常已定位为 eval batch-size 依赖，Pulp pure / mixed b64 Stage1 与 Stage2 公平基线已补齐；第一版 soft observed 没有 clean-task Pareto 改善；代码确认 Pulp camera translation feature 显式依赖 human root，因此下一版优先讨论 root/relation factorization，而不是直接在 raw latent 上加 gate。

## 2026-06-25 follow-up verdict

StoryMotion 与 mixed Pulp full eval 均覆盖 `10549` samples，pure Pulp eval 覆盖 `4053` samples；训练只有单 seed，因此只能报告 point estimates，不能声称统计显著。

| 项目 | 结果 | 对原复查建议的更新 |
| --- | --- | --- |
| soft observed `p=0.5, std=0.15` | joint camera 指标部分改善，但 joint human / outscreen 有退化；clean camera completion 全面退化；clean human completion 为质量/coverage tradeoff | Priority 1 已执行第一版，但没有形成 Pareto 解法 |
| camera specialist | clean camera 与 unified control 总体接近；CLaTr / R3 / F1 更高，FDCLaTr 略差 | Priority 2 的 camera baseline 已完成 |
| human specialist | clean human 与 unified control 几乎持平 | Priority 2 的 human baseline 已完成 |
| specialist observed zero / shuffle | 两个方向均大幅崩溃，zero 时 coverage 接近 `0` | single-task training 不能解决 condition dominance |
| CondMDI-style internal run | 5090 b16 复现 4090 b16；b64 只改变 R@K，FDTMR / TMR / coverage 不变 | checkpoint 有效；历史异常来自 batch-local retrieval，不是数据 |
| screen projection containment | pre-NaN best 的 Out `0.50%`，但 FDCLaTr `350.06`、F1 `17.42%`、Camera Cov `33.32%`；训练随后 NaN | 当前实现是失败性 tradeoff，不进入主线 |
| Pulp b64 Stage1 / Stage2 | Stage1 mixed coverage 为 Human `85.41%`、Camera `87.16%`；Stage2 no-Aux 降为 `10.63% / 51.60%` | Pulp 的主要瓶颈在 Stage2 generation，Stage1 stable foundation 获得直接数值证据 |
| StoryMotion vs Pulp mixed b64 | StoryMotion clean joint 在表列指标上优于 Pulp no-Aux；相对 Pulp Aux 仅 TMR 略低 | 内部同 batch-size 比较已公平；仍不能声称多 seed 显著或论文默认 b128 SOTA |

`observed_noise_matched` 的 follow-up eval 名称具有误导性：实现实际先随机替换整支 observed latent，再叠加 `1.0` 相对噪声，不匹配训练时 `0.15` 加性扰动，也没有 clean-control 同协议对照。因此 soft-observed robustness 仍未被正确验证。下一步先敲定 human task 与 root/relation 接口，再设计 matched reliability protocol；learned gate 后置。

### R@K 与 checkpoint 审计补充

- Pulp local official 默认 eval batch 是 `128/GPU`；2026-06-25 已额外完成 pure / mixed b64 rerun。StoryMotion 当前主表为 b64，历史 4090 异常项为 b16。
- Pulp retrieval callback 在每个 batch 内构造 `B×B` 候选池，因此 R@K 只在相同 eval batch size 下可比。
- 两机 b16 同 checkpoint 结果几乎一致；5090 b64 仅使 R@K 回落，FD、score、coverage、F1、Out 基本不变。
- 新增 Pulp b64 与 StoryMotion b64 可作本地直接对照；Pulp paper/default b128 仍应单独标记，不能混入同一 R@K 表。
- 两机 train/val cache、split、metric 权重及 screen 原始几何字段同 hash；数据分叉被排除。
- CondMDI `last@196000` 训练无 NaN 且权重有限；screen `best@170000` 有限，`last@176000` 从 `175100` 起 NaN 并失效。

### Pulp b64 公平基线补充

结果目录：`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_core_bs64_20260625/`。

| model / split | FDTMR ↓ | TMR ↑ | Human R3 ↑ | Human Cov ↑ | FDCLaTr ↓ | CLaTr ↑ | Camera R3 ↑ | Camera Cov ↑ | F1 ↑ | r_fpd ↓ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pulp Stage1 mixed reconstruction | 124.46 | 18.17 | 21.81% | 85.41% | 15.51 | 58.10 | 54.53% | 87.16% | 67.01% | 0.238 | 4.64% |
| Pulp Stage2 mixed no-Aux | 376.39 | 23.34 | 20.44% | 10.63% | 88.17 | 30.52 | 23.00% | 51.60% | 34.16% | 5.161 | 26.63% |
| Pulp Stage2 mixed Aux | 426.21 | 24.87 | 21.21% | 8.88% | 80.20 | 32.84 | 24.31% | 49.02% | 36.36% | 3.832 | 17.69% |
| StoryMotion clean joint | 157.36 | 24.26 | 26.84% | 37.43% | 76.85 | 36.16 | 29.83% | 65.80% | 40.21% | 0.482 | 7.58% |

这组结果改变了两个证据状态：

1. **Pulp Stage1 stable foundation 从推断升级为直接实证。** Stage1 reconstruction 与 Stage2 generation 之间存在明显 gap，说明 Pulp checkpoint 的主要失真来自 Stage2，而不是 tokenizer/decode contract。
2. **StoryMotion 的本地 Pulp 对比不再受 b64/b128 R@K 混用影响。** 同 mixed split、同 evaluator、同 b64 下，StoryMotion clean joint 相对 Pulp Aux 的 FDTMR 低 `63.1%`、Human / Camera coverage 高 `28.54 / 16.78` 个百分点、`r_fpd` 低 `87.4%`、Out 低 `10.11` 个百分点，但 TMR 低 `0.61`。应写成单 seed point estimate，而不是全面 SOTA。

## 复查元信息

- 主题：StoryMotion Decoupled Coupling QA critical review
- 原始日期字段：`2026-`，结合上下文应为 `2026-06-24`
- Reviewer：Kiro，Opus 4.8
- 已核查数据：5090 metrics、`v5_controlled_coupling` 结果、训练代码、checkpoint metadata
- 核心被复查对象：decoupled coupling QA 文档中的数据、结论、架构分析和 next step

## I. 核心 verdict

1. **数据本身是可信的。** 5090 full eval 文件与文档转录的数字匹配；样本数为 `10549`，checkpoint 为 `step=146000`，评估协议一致。

2. **跨任务 seed 不完全一致，是中等风险，不是结论推翻点。** 实际 seed 里 camera completion、joint 等任务使用了不同随机种子，因此 joint vs completion 这类跨 family 比较要加 warning。但 C 的 GT-camera oracle 和 clean human completion 的结果几乎相同，例如 FDTMR `126.63` vs `126.70`、coverage `84.58%` vs `84.61%`、MPJPE `0.0884` vs `0.0888`，说明结果对噪声 seed 基本确定。结论：seed mismatch 对跨任务比较有风险，但主要结论仍稳定。

3. **Observed-branch dominance 是强证据。** A 矩阵显示 completion 任务对 text noise 基本不敏感，但 observed branch 被 zero / shuffle / noise 后会灾难性退化。camera completion 在 observed human zero 时 coverage 只有 `0.35%`；human completion 在 observed camera + noise 时 coverage 从 clean 的 `84.61%` 降到 `72.91%`。根因不是单个指标异常，而是 observed branch 在评估 harness 里 hard replacement，并且又作为显式 `obs_x0` 条件进入模型；训练时 binary mask=1 总是配 clean GT `obs_x0`，checkpoint metadata 也确认 `obs_self_condition_prob=0.0`，没有 corruption training。

4. **Generated-camera replay 不能修复 joint degradation，但不能据此否定 root-first。** Replay 的 FDTMR `148.69`、TMR `23.54`、MPJPE `0.1947`，与 joint baseline 基本同区间。它测试的是“先生成 full camera，再由 camera 生 human”，与 camera 表示的 `human root -> relative camera` 方向相反；它没有测试“先 human root，再 camera”。

5. **GT-camera oracle 的语义解释有过度宣称。** 文档把 GT camera 下 TMR `18.17` 解释为“GT camera suppresses text semantics”。Kiro 认为这只是中等证据：低 TMR 也可能来自 reconstruction-like 任务目标、GT camera 对 human motion 空间的强约束，或者训练中从 GT camera 间接锁定 GT human。没有 ground-truth human TMR baseline 时，不能把它唯一解释成“语义被 camera 压制”。

6. **Boundary 结论方向正确，但机制解释要收缩。** Boundary schedule 控制的是 temporal injection schedule / active observed steps，不是 learned coupling。Boundary `0.3 -> 0.7` 时 coverage `59.38% -> 77.96%`、MPJPE `0.1354 -> 0.1073` 变好，TMR `19.82 -> 18.83` 下降。它证明的是 inference-time reconstruction vs generation tradeoff，而不是已经学到了 coupling controller。

## II. 数据支持表

| 结论                              | 实验                                     | 关键数值                                                                                                                   | 证据强度                    |
| ------------------------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| Completion 对 text noise 不敏感     | A camera / human completion text noise | camera FDCLaTr `15.16 / 15.20 / 15.66`；human TMR `18.15 / 18.10 / 18.09`                                               | 强                       |
| Completion 被 observed branch 主导 | A observed branch perturbation         | camera observed zero：coverage `0.35%`，FDCLaTr `1044.19`；human observed camera + noise：coverage `72.91%`，MPJPE `0.1162` | 强                       |
| Joint 对文本强依赖                    | A joint text shuffle / zero            | baseline TMR `23.91`；shuffle `6.37`；zero `4.79`                                                                        | 强                       |
| Replay 不是修复 joint human 的主路径    | B generated-camera replay              | replay FDTMR `148.69` vs joint `153.72`；TMR `23.54` vs `23.91`                                                         | 强                       |
| GT camera 给出几何上界                | C GT-camera oracle                     | HumanCov `84.58%`，MPJPE `0.0884`，Contact Δ `0.1543`                                                                    | 强                       |
| GT camera “压制语义”                | C GT-camera oracle                     | TMR `18.17` 低于 joint / replay 的 `23+`                                                                                  | 中等，存在替代解释               |
| Boundary 插值出几何/语义 tradeoff      | D boundary scan                        | Cov `59.38% -> 77.96%`；TMR `19.82 -> 18.83`                                                                            | 强，但机制是 inference gating |
| Branch pollution / cross-talk   | A joint text perturbation              | camera-text noise 更伤 camera F1；human-text noise 更伤 human TMR                                                           | 中等到强                    |

## III. 架构诊断

### 1. Hard observed replacement：正确，但原文低估了机制强度

代码证据显示 observed branch 不是普通条件，而是被硬写入：

```text
x = torch.where(obs_mask.bool(), obs_x0, x_t)
```

此外还有双重注入：

- observed branch 在 sampler / eval harness 中作为 hard replacement 进入；
- observed branch 又作为显式 `obs_x0` 条件传给模型；
- binary `obs_mask=1` 在训练中总是配 clean GT observation；
- checkpoint metadata 显示 `obs_self_condition_prob=0.0`，说明当前 v5 checkpoint 没有使用 noisy / mixed observed self-conditioning。

因此，更准确的根因表述是：模型学到的是“mask=1 的 observed branch 完全可靠”，而不是“根据 observed branch 质量动态决定信任程度”。

`疑惑`：具体指违背了哪一条优化实验的claim吗，还是指StoryMotion independent-dropout的训推不合理？

### 2. Branch-mask 只表达 visibility，不表达 trust / timing

这个判断正确。当前 branch mask 只告诉模型“哪一支可见、哪一支要生成”，没有表达：

- observed branch 的质量；
- condition trust；
- 不同 timestep 何时应强耦合或弱耦合；
- 生成支和观测支之间的动态权重；
- per-sample uncertainty。

D boundary 结果进一步证明 timing 本身重要，但当前 timing 是手调 schedule，不是 learned schedule。

### 3. Raw latent concat 缺少 relation-space control：部分正确

当前 latent 形态是：

```text
z = concat([z_hum, z_cam])
z_hum: [0:128]
z_cam: [128:192]
```

这说明 human / camera 在同一个 denoising stream 中共享上下文，确实容易造成 uncontrolled coupling。不过 Kiro 认为文档还漏了一个更细的现象：text routing 有 branch-specific 结构，同时存在 cross-talk。

joint 中：

- camera-text noise 更明显伤 camera 指标；
- human-text noise 更明显伤 human TMR；
- 但两者都有 off-diagonal 影响，说明不是完全解耦。

因此“raw latent concat 有无控制耦合风险”是中等证据；但“relation-space 一定能修好”仍需实验证明。

### 4. Camera representation 的 root 依赖：代码级强证据

Pulp camera feature 明确包含：

```text
camera_translation - human_root_translation
```

decode 时又把 decoded human root 加回 camera translation。因此 camera latent 不是与 human 独立并列的变量。更合理的结构假设是先生成 human root / coarse relation，再生成 body 与 camera；不是先完整 human，也不是先 full camera。该事实提升了 root-first 的研究优先级，但 root-first 的性能仍需 ablation。

### 5. 4090 screen containment 是负面对照，不是 relation-space 成功证据

5090 已复评 pre-NaN `best@170000`。它将 Out 降到 `0.50%`，但 b64 FDCLaTr 为 `350.09`、F1 为 `17.44%`、Camera Cov 为 `33.14%`；后续 `last@176000` 又因训练 NaN 失效。因此只能写“强 projection penalty 造成 containment/camera quality 的失败性 tradeoff”，不能写 relation-space 已验证有效。

## IV. 文档中过度宣称的地方

1. **“GT camera suppresses text semantics” 过度。** 数据只显示 GT-camera oracle 下 TMR 较低；不能排除 reconstruction-like objective、GT camera 几何约束、或训练数据泄漏式重建假设。

2. **“Boundary 是 Pareto schedule / learned coupling” 过度。** Boundary 只是 inference-time temporal gating。它能移动 geometry / semantics tradeoff，但不是训练出来的 controller。

3. **“Completion 是公平的 text + observed dual conditioning” 过度。** Completion 在 A 矩阵中明显是 observed-dominant。text noise 几乎不影响 completion，而 observed branch 破坏会使指标大幅下降。

4. **“统一三模式”叙事过强。** 虽然代码统一了接口和 mask pattern，但三种模式处在不同机制中：
   - completion：observed-dominant / reconstruction-like；
   - joint：text-driven generation；
   - oracle：强 observed geometry condition。

5. **“Soft observed 已经是实验结果” 不准确。** 代码中有 `make_observed_condition_x0`、noisy / mixed mode 等路径，但当前 checkpoint 没有训练这些路径。正确写法应是“已有 infrastructure，可用于 retrain”，而不是“当前模型已验证 soft observed”。

## V. 文档遗漏的重点

1. **Double injection。** Observed branch 不仅通过 latent replacement 进入，还作为显式 `obs_x0` 条件传给模型。这解释了为什么 observed branch dominance 如此强。

2. **耦合不对称。** Joint text perturbation 显示 human-text 与 camera-text 的影响不是完全对称；human 语义和 camera 构图之间存在方向性依赖。

3. **结果确定性。** C 的 GT-camera oracle 与 clean human completion baseline 在不同 seed 下几乎一致，说明主要结论不是随机噪声造成。

4. **Checkpoint metadata。** `obs_self_condition_prob=0.0` 是关键事实：代码支持 noisy observed branch，但当前 checkpoint 没用。

5. **Task C 不是完全独立 oracle。** C 几乎等同于 clean human completion baseline 的跨 seed 验证；它是几何上界证据，但不是独立证明语义抑制的 oracle。

6. **Diagonal / off-diagonal text routing。** A 矩阵不仅说明 joint 依赖 text，还说明 text half 的影响有 branch-specific 对角结构和 cross-talk。

7. **Human task 定义混杂。** camera-conditioned actor recovery、root-only conditioned human generation 与 human-text-only generation 回答不同问题。最后一种是有效的解耦对照，但严格说不再是给定 camera 的 completion。

## VI. 论文 claim 收缩建议

| Claim                                                          | 判断     | 建议改写                                                                                       |
| -------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| Unified three-mode SOTA                                        | Reject | Completion 和 joint 是不同机制；需要 same-tokenizer、same-backbone、same-budget 单任务 baseline 才能写 SOTA |
| StoryMotion achieves decoupling                                | Reject | A 矩阵显示 completion 是 observed-dominant，joint 有 text coupling 和 branch cross-talk            |
| Completion has fairly won                                      | Reject | 目前没有公平 single-task completion baseline；observed-GT completion 更像 reconstruction            |
| Root/relation-aware conditional generation is the core problem | Accept | camera 表示依赖 human root，任务条件方向与可靠性需要显式建模                                                    |
| Pulp Stage1 is stable foundation                               | Accept | mixed b64 reconstruction 的 Human / Camera coverage 为 `85.41% / 87.16%`，明显高于 Pulp Stage2；source VAE / GRFSQ 坍塌进一步支持保留它 |
| Branch-mask diffusion needs structural upgrade                 | Accept | 优先 root/relation factorization 与任务拆分，其次 reliability training；gate 后置                       |

## VII. 重构后的决策顺序

当前不直接启动下一轮多卡训练。先依次敲定：

1. human mode 是 camera-conditioned actor recovery、root-only generation，还是 human-text-only generation；三者可并存，但不能混称同一任务。
2. joint 主假设是否改为 root-first；优先比较 current simultaneous 与 root-first，不先做 full human-first。
3. practical completion 的 condition source 是否覆盖 clean / additive-noisy / generated / missing，并用 quality/source token 显式标记。
4. 本地公平比较使用已完成的 Pulp / StoryMotion b64；论文对外协议再统一到 Pulp b128，或改成 batch-invariant global retrieval。
5. 只有前三项仍不能解决问题时，再考虑 root/relation-space gated residual。

### 候选对照

| 候选                                                    | 回答的问题                                          | 关键指标                                                |
| ----------------------------------------------------- | ---------------------------------------------- | --------------------------------------------------- |
| current simultaneous vs root-first joint              | root-level 因果分解是否改善 joint                      | human/camera official metrics、root error、projection |
| full camera vs root-only vs no-camera human           | camera 提供的是 root posterior 还是 latent 污染        | root MPJPE、body MPJPE excluding root、HumanCov、TMR   |
| clean/noisy/generated/missing observed + source token | brittle completion 是否来自 clean-only reliability | clean 保真、noise curve、generated-condition recovery   |
| real/zero/shuffled human text × observed source       | text 在何种 reliability 下有约束价值                    | TMR、output change、root/body 分离指标                    |
| unified vs task-specific models                       | unified 是否有质量或效率贡献                             | native metrics、参数量、FLOPs、wall time                  |

## VIII. 需要补查的数据或代码位置

1. **Contact Δ 来源。** 文档列出 C / D 的 Contact Δ 数值，例如 `0.1543 / 0.2853 / 0.2608 / 0.2344`，但需要明确它们来自哪个 JSON 字段或是否为后处理计算。

2. **4090 screen containment full metrics。** 2026-06-25 已在 5090 重评 pre-NaN `best_eval@170000`：b64 Out `0.50%`、FDCLaTr `350.09`、F1 `17.44%`、Camera Cov `33.14%`；训练从 `175100` 起 NaN。结论是 best 可加载但方法 tradeoff 失败，`last@176000` 无效。

3. **Pulp Stage1 稳定地基的引用证据。** 已完成：mixed b64 reconstruction 的 Human FDTMR / coverage 为 `124.46 / 85.41%`，Camera FDCLaTr / coverage 为 `15.51 / 87.16%`，`r_fpd=0.238`、Out `4.64%`；对应 Stage2 no-Aux coverage 仅 `10.63% / 51.60%`。

4. **Ground-truth human motion TMR。** 用于区分 GT camera 下 TMR `18.17` 到底是 semantic suppression，还是 reconstruction-like oracle 的自然结果。

5. **Training convergence / dominance 过程。** CondMDI TensorBoard 已确认无 NaN，但仍需按 checkpoint 做 intervention trajectory，判断 observed dominance 是何时形成，而不是只看 loss。

6. **Root-first 具体接口。** 需要决定 root/coarse relation 是从 Pulp human feature 显式切片、独立 tokenizer，还是从 decoded root 监督的辅助 latent；在接口确定前不启动多卡训练。

## IX. 最终推荐写法

不要写：

```text
StoryMotion has validated controlled coupling.
```

建议写：
【完全打回，内容完全不在StoryMotion的要点，且没有按重要性分点，也不满足ICLR的风格。另外，`boundary / temporal gating 能移动 reconstruction fidelity 与 text-driven generation 的权衡`只能算是第三个或者更低优先级的贡献点，前两位一个是unified framework for 三模式生成，另一个待定；】
```text
StoryMotion 在统一 latent diffusion 接口下覆盖 joint human-camera generation、camera completion 和 human mode，但这些任务运行在不同条件机制中。Pulp camera representation 显式依赖 human root，而当前 Stage2 同时 denoise human/camera latent，没有显式建模 root-level 条件方向；completion 又把 observed branch 当作高可信条件，使 text、root posterior 和 full latent 污染混在一起。

在同 mixed split、同 evaluator、同 `batch_size=64` 的本地 point estimate 下，StoryMotion clean joint 在表列指标上优于 Pulp no-Aux，相对 Pulp Aux 仅 TMR 略低；同时 Pulp Stage1 reconstruction 明显优于其 Stage2 generation，说明应保留 frozen Stage1，并把下一版改动集中在 Stage2 factorization。

下一版研究问题应写成：能否用 root/relation-first factorization 统一 joint generation 与多种条件方向，并区分 camera-conditioned actor recovery、root-only human generation、human-text-only generation和 reliability-aware completion。Boundary / temporal gating 只保留为辅助诊断；raw-latent learned gate 后置。现阶段已完成根因收缩和协议审计，训练好的解决方案仍待验证。
```

## X. 一句话总结

Claude/Kiro 问答与后续代码审计的核心结论是：**camera latent 的定义依赖 human root，当前 simultaneous raw-latent denoising 没有显式建模这一方向；completion 还混合了 actor recovery、root inference 与 text-only generation。下一步先定任务和 root/relation 接口，再决定训练，不把 gate 或 soft observed 提前写成答案。**
