---
title: "StoryMotion Decoupled Coupling QA - Claude/Kiro 复查中文整理"
hypothesis: "Claude/Kiro 复查认为当前证据支持 StoryMotion 的核心问题定位为 condition dominance、branch pollution 与 coupling strength/timing，但不支持把 A/B/C/D 写成修复完成或 controlled coupling 已验证。"
status: draft
created: 2026-06-24T22:14:01+08:00
updated: 2026-06-24T22:14:01+08:00
source_notes:
  - "[[ideas/StoryMotion/2026-06-23_storymotion-decoupled-coupling-qa]]"
---

# StoryMotion Decoupled Coupling QA - Claude/Kiro 复查中文整理

> [!note] 整理说明
> 本文是对 Claude/Kiro 反馈的中文整理译文。原反馈中存在明显断行、乱码和字段残缺；本文保留可辨认的技术判断、数值和优先级，按原有结构整理为可读中文。本文不是新增实验结论。

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

4. **Generated-camera replay 不能解释或修复 joint degradation。** Replay 的 FDTMR `148.69`、TMR `23.54`、MPJPE `0.1947`，与 joint baseline 的 FDTMR `153.72`、TMR `23.91`、MPJPE `0.1928` 基本同区间。两者都远差于 GT-camera oracle。因此文档中“replay 不是修复路径”的结论正确；瓶颈更像是 generated camera 质量，而不是 simultaneous denoising 这个表面形式。

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

### 4. 4090 screen containment 证据不能提前写成性能结论

文档可以写 4090 containment 的代码路径和 evalfix 状态，但不能写 relation-space 已验证有效。当前证据只说明：

- screen projection containment 的训练原型可运行；
- eval 聚合 bug 已修复；
- eval / test 路径能够继续通过。

在 full official metrics 完成之前，不能声称它改善了 projection / semantic Pareto。

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

## VI. 论文 claim 收缩建议

| Claim                                                      | 判断     | 建议改写                                                                                       |
| ---------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| Unified three-mode SOTA                                    | Reject | Completion 和 joint 是不同机制；需要 same-tokenizer、same-backbone、same-budget 单任务 baseline 才能写 SOTA |
| StoryMotion achieves decoupling                            | Reject | A 矩阵显示 completion 是 observed-dominant，joint 有 text coupling 和 branch cross-talk            |
| Completion has fairly won                                  | Reject | 目前没有公平 single-task completion baseline；observed-GT completion 更像 reconstruction            |
| Controlled coupling is the core problem                    | Accept | 数据和代码共同支持 condition dominance、branch pollution、timing tradeoff 是核心问题                       |
| Pulp Stage1 is stable foundation                           | Accept | 在当前 scope 内，Pulp latent contract 是稳定地基；source VAE / GRFSQ 坍塌支持保留它                          |
| Branch-mask diffusion needs upgrade to controlled coupling | Accept | root cause 确认；应升级到 corruption training、learned gate、quality-aware conditioning             |

## VII. Next steps 优先级

### Priority 1：Soft observed branch training

结论：保留，最高优先级。

要做什么：

- 使用现有 `make_observed_condition_x0` 路径；
- 训练 `obs_self_condition_prob > 0`；
- 使用 `mode=noisy` 或 `mode=mixed`；
- 加 condition quality token 或等价质量信号；
- 不再让 mask=1 永远对应 clean GT observation。

为什么优先：

- 这是对当前根因最直接的修复；
- 代码路径已经存在，改动相对小；
- 可以直接验证“clean observed reliability assumption”是否是 completion 脆弱的主要来源。

验证方式：

- 对 human completion / camera completion 做 observed-noise sweep；
- 噪声强度建议覆盖 `0.0 / 0.3 / 0.5 / 0.7 / 1.0`；
- 看 FD、coverage、MPJPE、TMR、F1 等完整指标。

成功标准：

- observed branch 质量下降时，退化曲线明显慢于当前 hard baseline；
- clean completion 不明显退化。

### Priority 2：Fair separate-task baselines

结论：保留，第二优先级。

要做什么：

- 训练 joint-only；
- 训练 camera-completion-only；
- 训练 human-completion-only；
- 使用 same tokenizer、same backbone、same split、same budget。

为什么优先：

- 这是任何 unified / SOTA claim 的前提；
- 可以判断 unified branch-mask 是真实贡献，还是只是工程拼接；
- 也能判断 completion 结果好是否只是 reconstruction-like 任务本身简单。

验证方式：

- 每个任务对比 native metrics；
- 报告参数量、训练 FLOPs、采样成本；
- 对比 unified vs three separate models。

### Priority 3：Learned coupling gate

结论：保留，但应在 Priority 1 / 2 之后。

要做什么：

- 加 branch-specific streams；
- 加零初始化 cross residual；
- gate 条件依赖 timestep、task、condition quality；
- 让模型学习什么时候耦合、耦合多少。

为什么不是第一优先：

- 它是架构级改动，成本更高；
- 如果 corruption training 已经让 completion 鲁棒，gate 的必要性会降低；
- 应先用 Priority 1 判断是否只靠可靠性训练就能解决大部分 dominance。

验证方式：

- A 矩阵 intervention metrics；
- joint baseline；
- branch pollution index；
- semantic pollution index；
- clean task 指标是否保持。

### Priority 4：Observed-camera hybrid oracle

结论：替代原来的 relation-space constraint，作为第四个核心实验。

为什么替换：

- 4090 screen containment 还没有 full official metrics；
- relation-space constraint 现在直接进入核心实验过早；
- 更应该先确认 generated camera quality 是否是 joint degradation 的主要瓶颈。

要做什么：

```text
observed_camera = α * GT_camera + (1 - α) * generated_camera
α ∈ {0.0, 0.25, 0.5, 0.75, 1.0}
```

然后做 human completion。

要回答的问题：

- Human 指标是否随 camera quality 单调恢复；
- 如果 α 增大就恢复，说明 generated camera quality 是主瓶颈；
- 如果 α 增大仍不恢复，说明 coupling / conditioning 结构本身也有问题；
- 如果曲线非线性，说明存在阈值或饱和效应。

指标：

- FDTMR；
- TMR；
- R3；
- HumanCov；
- MPJPE；
- Contact Δ。

### 暂缓或删除的候选项

| 候选项 | 处理 | 理由 |
| ------ | ---- | ---- |
| Generated-camera distribution adapter | 暂缓 | 先确认 camera quality 是否真是主瓶颈 |
| Per-timestep coupling schedule | 暂缓 | D 已经有 boundary scan；learned version 应并入 learned gate |
| Relation-space projection / framing constraint | 暂缓 | 4090 containment 还未完成 full official；先做 hybrid oracle |
| Render-level projection failure taxonomy | 暂缓 | 对论文可视化有用，但不是下一轮核心训练实验 |
| Condition quality token | 合并 | 并入 soft observed branch training |

## VIII. 需要补查的数据或代码位置

1. **Contact Δ 来源。** 文档列出 C / D 的 Contact Δ 数值，例如 `0.1543 / 0.2853 / 0.2608 / 0.2344`，但需要明确它们来自哪个 JSON 字段或是否为后处理计算。

2. **4090 screen containment full metrics。** 当前只能写 evalfix 路径通过，不能写性能改善。需要等 full official eval 完成。

3. **Pulp Stage1 稳定地基的引用证据。** 如果要写 Pulp Stage1 是 stable foundation，需要引用具体 reconstruction upper-bound 或 source VAE / GRFSQ collapse 数值。

4. **Ground-truth human motion TMR。** 用于区分 GT camera 下 TMR `18.17` 到底是 semantic suppression，还是 reconstruction-like oracle 的自然结果。

5. **Training convergence / dominance 过程。** 需要检查 checkpoint 在训练过程中是否逐渐形成 observed branch dominance，还是从一开始就由 hard replacement 诱导。

## IX. 最终推荐写法

不要写：

```text
StoryMotion has validated controlled coupling.
```

建议写：
【完全打回，内容完全不在StoryMotion的要点，且没有按重要性分点，也不满足ICLR的风格。另外，`boundary / temporal gating 能移动 reconstruction fidelity 与 text-driven generation 的权衡`只能算是第三个或者更低优先级的贡献点，前两位一个是unified framework for 三模式生成，另一个待定；】
```text
StoryMotion 在统一 latent diffusion 接口下覆盖了 joint human-camera generation 和双向 completion，但当前评估表明这些模式运行在不同条件机制中：joint 更像 text-driven generation，而 completion 更像 observed-branch-dominant reconstruction-like completion。我们识别出当前 branch-mask diffusion 的核心瓶颈是 double-injected observed branch、binary reliability training 和缺少 trust / timing / quality 控制面；这些因素使 completion 对真实或生成的 noisy condition 脆弱，也使 joint 中 generated camera quality 成为 human 质量瓶颈。

当前贡献应写成问题定位和机制路线：我们提出 coupling diagnostics，验证 boundary / temporal gating 能移动 reconstruction fidelity 与 text-driven generation 的权衡，并给出下一步 controlled coupling 方案，包括 corrupted observed-branch training、fair separate-task baselines、learned coupling gates 和 observed-camera hybrid oracle。现阶段结论是：受控耦合是 StoryMotion 的核心设计问题，训练好的解决方案仍待验证。
```

## X. 一句话总结

Claude/Kiro 的核心意见是：**数据支持“问题定位”，不支持“修复已完成”。StoryMotion 现在最该写的是 condition dominance / branch pollution / coupling timing 的诊断，以及 soft observed training、fair baselines、learned gate、hybrid oracle 的验证路线。**
