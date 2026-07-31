---
hypothesis: "以 official main 严格复现为基线，P0 已定位到 Stage2 tr 分支：模型在 rare open-dance mode 上预测了错误的完整相对轨迹。下一步优先审计 decoder 可见的 residual-level 求和空间与逐层 all_quantizeds loss 是否错配，并验证显式 initial placement/root-path 建模；music 不是伴舞生成的主条件，相关修复后移。"
status: validated-diagnosis
created: 2026-07-16T14:54:10+08:00
updated: 2026-07-18T16:20:23+08:00
official_repo: https://github.com/RipeMangoBox/ReactDance
official_commit: 3d7bc40727097b4b0bf506b05f430306f76acdb4
diagnostic_branch: diagnostics/official-stage2-audit-3090
diagnostic_commit: 35d024c
source_papers:
  - "[[analysis/ICLR_2026/ReactDance_Hierarchical_Representation_for_High_Fidelity_and_Coherent_Long_Form_Reactive_Dance_Generation]]"
  - "[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion]]"
  - "[[analysis/ICLR_2024/Duolando_Follower_GPT_with_Off_Policy_Reinforcement_Learning_for_Dance_Accompaniment]]"
  - "[[analysis/SIGGRAPH_2025/DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked_Modeling]]"
  - "[[analysis/ICCV_2025/Align_Your_Rhythm_Generating_Highly_Aligned_Dance_Poses_with_Gating_Enhanced_Rhythm_Aware_Feature_Representation]]"
tags:
  - idea/reactdancepp
  - topic/motion_animation
  - topic/generative_models_diffusion
  - diagnosis/stage2
  - audit/official-main
---

# ReactDance Stage2 远距离失败与音乐不敏感：official-main 复核

> [!abstract] 结论先行
> 1. 本笔记现在以 [official ReactDance repository](https://github.com/RipeMangoBox/ReactDance) 的 `main@3d7bc40727097b4b0bf506b05f430306f76acdb4` 为唯一规范基线。5090/4090 的 4 月后调整只能提供待验证线索；按用户补充，它们没有有效 matched attempt，不能用于方法优劣排序。
> 2. release Stage2 checkpoint 有四个旧命名条件投影参数；在共享 module alias 下表现为八个 serialized keys。映射后完整 Stage2 generator `703/703` strict load，内嵌 Stage1 `426/426` 与外部 checkpoint 逐 tensor 相等。三样本 Stage1/Stage2 可视化与固定 seed 重复生成确认 checkpoint 加载正确。
> 3. 远距离失败被 oracle 明确定位到 `tr`：far 样本 Stage2 root ADE 为 `1.508m`；替换为 GT/Stage1 `tr` 后降到 `0.156m`，替换 body 而保留预测 `tr` 仍为 `1.508m`。错误是完整相对轨迹/方向 mode，而不只是首帧 offset 或身体姿态。
> 4. train 中 far windows 只占 `11.7%`，但 distance-balanced sampling 并未优于 uniform control；anchored leader root 更会维持距离，却没有恢复正确方向轨迹；只在低噪声 timestep 使用 geometry loss 也没有收益。far-tail、root 条件缺失和高噪声 geometry 都是相关因素，但现有单项干预不是充分修复。
> 5. HFSQ per-dimension std 的确跨 `24.78×`，但 `D→E→D` projection 对 16 个 Stage2 cases 的 overall root ADE 只改善 `0.003m`，far 只改善 `0.0028m`；true z-score 退火短训则明显崩坏。HFSQ manifold/scale 降为从头训练时的 P2 设计项，不支持作为当前 checkpoint 远距离失败主因。
> 6. 完整 DDIM 反事实确认 music shortcut：phase shift 只改变最终 latent `0.103%`；swap music 为 `3.04%`，swap leader 为 `133.3%`，逐 case `swap music / swap leader` 中位数仅 `1.38%`。matched local follower 的 beat alignment 对 music 为 `0.212`，对 leader 为 `0.558`。
> 7. parity-initialized time-resolved music 短训把 phase-shift 响应提高到 `2.26%`、music/leader 中位数提高到 `2.95%`，证明 block pooling 是因果瓶颈之一；但 beat-to-music 只到 `0.231`，且远距离质量恶化。强 leader-drop/music-keep 收益更弱且破坏生成质量。
> 8. corrected 50-step DDIM 只把 far ADE 从 `0.714` 改到 `0.702m`；真正启用 CFG 后各权重均未稳定改善 overall/far 权衡。它们是应修的实现硬伤，不是科学主因。
> 9. 720-frame 长序列中边界 root-step error 是内部的 `1.68×`，但 far 窗口为 `0.99×`；continuity anchor 只把 overall ADE `0.3303→0.3283m`。BLC 是 seam/瞬移放大器，不是 far failure 起点。
> 10. 当前唯一 P0 是修复 `tr` 与由此造成的整体 reactor motion 低质：先分解 decoder 可见的 residual-level 求和误差与逐层分解误差，再验证显式 initial relative placement、root velocity/path 与独立 root head。music 不是主 condition，后移到 P2；不要让 music 实验占用 P0 训练预算。
> 11. 2026-07-18 的本地 screen 停在 epoch 249：Stage1 在 decoder-visible 空间对小扰动稳定，但 Stage2 的 far 中噪声 `tr` 误差只有 `56.6%` 位于可见 level-sum 子空间，未达到 sum-aware 续训门槛。root-only `C3` 初始站位 oracle 虽带来 `10.4%` far ADE 降幅，但 FDE 退化，联合 gate 未命中；因此不泄漏 GT、不恢复当前训练，也不启动新的 Stage2 condition adaptation。

## 1. 范围、基线与证据口径

本笔记接受以下事实，不再把数据或 Stage1 普遍重建失败列为首要嫌疑：

- GT 数据和渲染正确。
- HFSQ 重建在视觉和整体指标上较好，只有少数样本可见差异。
- 目标是解释 Stage2 的 distance-selective failure 与 music insensitivity，而不是先设计更大的 ReactDance++。

证据等级：

- `C`：official commit 中可直接确认的代码或配置事实。
- `O`：既有 checkpoint、生成结果或本地数据中的观测，但缺完整 run manifest。
- `P`：论文正文或附录报告。
- `H`：尚需 matched experiment 判定的机制假设。

### 1.1 规范基线

| 对象 | 用途 | 当前处理 |
| --- | --- | --- |
| official GitHub `main@3d7bc407` | 定义正式实现与可复现 baseline | **唯一规范代码基线** |
| official paper/PDF | 定义论文声称的方法与训练 recipe | 与代码逐项对照，不默认二者一致 |
| 5090/4090 4 月后调整 | 产生过 root loss、condition、root/body 等候选方向 | 只当 hypothesis inventory；无有效 matched result |
| 旧 `epoch_500` 生成目录 | 量化用户所述症状 | 只作 `O` 级症状证据，需补 checkpoint/code hash |

official `main` 当前共有 7 个 commits，HEAD 为 2026-04-04 的 `fix evaluation yaml path`。这里的“基线”指正式发布身份，不等于文件时间上最新。后续机器目录即使更新，也不能在无有效实验合同的情况下覆盖 official 结论。

## 2. 对旧版建议的调整

| 旧结论 | official 复核 | 调整 |
| --- | --- | --- |
| Stage2 optimizer 更新了共享 `hfsq_tr` decoder | official 仅把 HFSQ 放在 Lightning module 的 `self.hfsq` 和 diffusion 的普通 `dict` 中；optimizer 是 `self.model.parameters()`，denoiser 没有 `set_root_latent_decoder` | **撤回为 official 主因**；这是后续分支可能引入的 regression |
| `hard_mining`、curriculum 配置存在但没有实现 | official config 中不存在这些字段 | **从 official gate 删除**；后续无效实验不得用于否定 sampler/curriculum 假设 |
| `zero + TR_delta + TR_path + augmentation` 是可靠主线 | 这套 recipe 不在 official，且用户确认调整后没有有效尝试 | **撤回“可靠主线”称号**；official 原始 recipe 才是 baseline |
| root-traj/kimodo fp16 NaN 已确认 | 这是后续分支现场记录，不是 official main 的直接证据 | 降为待复现的 dtype 风险 |
| root-aware metric 缺失 | official 代码直接成立 | 保留并升为 Gate 0 |
| CFG/LDCFG no-op | official `guided_forward` 直接早退 | 保留并升为论文—代码一致性 Gate 0 |
| DDIM 跳过首 pair | official 直接成立 | 保留；先做低成本 sampler parity test |
| release checkpoint 可直接由 official 加载 | Stage2 有四个旧命名条件输入 key；`strict=False` 静默漏载 | **升为最前置复现 Gate 0**；精确映射后必须 strict check |
| HFSQ latent 被强制 identity normalization | official 直接成立 | 保留；进入 representation/conditioning 诊断 |
| music 被 block pooling、leader 通路更强 | official 直接成立 | 保留；仍是音乐问题 P1 |
| far error 与 GT distance 强相关 | 34 序列重算相关系数 `0.955`，并按 GT distance 分桶 | 提升为量化 `O`；生成数组仍需与完整 run manifest 绑定后才能比较分支 |

最重要的方向变化是：**不再先追 decoder 污染或后续分支 recipe，而是先建立 official 可复现合同，并验证 root conditional ambiguity、far-tail coverage 与 timestep-dependent geometry supervision。**

## 3. official 实际数据流

### 3.1 Stage1 target

`FullBody_HFSQ.encode` 把 reactor 分成三路：

- `up`：reactor 以自身 root 为中心的上身。
- `down`：reactor 以自身 root 为中心的下身。
- `tr`：逐帧相对位移 `reactor_root - leader_root`。

每一路使用 8 groups、2 residual FSQ levels；Stage2 预测的是各层经 `project_out` 后的 `all_quantizeds`，三路各 256 维，总计 768 维/token。

### 3.2 Stage2 target 与 loss

official diffusion：

- 直接预测 HFSQ `x0`，不是 epsilon。
- `up/down/tr` 各自按 residual levels `[2, 1]` 做 latent MSE。
- 将随机 timestep 的 `x0_pred` 直接送进 HFSQ decoder，再施加 pose、velocity、acceleration、contact、relative orientation、distance/contact 和 root translation geometry losses。
- `use_pred_as_target=True`，geometry target 是 `D(E(GT))`，可避免 Stage1 reconstruction floor 与 Stage2 error 混在一起。

### 3.3 条件路径

official 在送入 Stage2 前执行：

```python
pose_seql, _ = self.hfsq.rootl_full_forward(pose_seql)
```

因此 leader 每一帧都减去自己的 root。Stage2 看见的是：

- music feature；
- leader local articulated pose；
- 看不见 leader anchored global root trajectory、root velocity，以及 reactor 的 initial relative offset。

目标 `tr(t)` 却是 reactor 与 leader 的逐帧相对 root。绝对世界坐标本身不需要，但 leader root velocity、anchored trajectory 和 initial relative placement 都可能降低 open/far choreography 的条件不确定性。

### 3.4 music/leader 融合

默认 `music_time_merged=True`：

- leader tokens 保留逐 token 时间结构，作为 cross-attention memory；
- music tokens 在每个 60-token block 内 mean pooling；
- pooled music hidden 被复制到整块，只加到 timestep embedding 并进入 FiLM。

训练窗恰好是 240 frames，经 4 倍下采样为 60 tokens。因此同一训练窗内每个 latent token 获得相同的 8 秒 music summary，而 leader 保持逐 token 对齐。

### 3.5 长序列

official 默认 `attn_mask_type=interval`：

- 每 60 latent tokens 一个 block；
- block 之间完全隔离；
- block 内是双向 attention，不是 causal；
- sinusoidal positional encoding 每块从 0 重启；
- 每个 block 从噪声独立生成，无 previous-root anchor 或 overlap constraint。

HFSQ convolutional decoder 是唯一跨 block 边界提供隐式平滑的组件。它能平滑局部 body motion，不保证两个独立 block 的绝对相对 root offset 属于同一轨迹分支。

## 4. official 中确认的实现与复现问题

### 4.1 `C`：论文 recipe 与 public code 不一致

| 项目 | 论文 | official code/config | 影响 |
| --- | --- | --- | --- |
| BLC mask | periodic causal masking | 默认 `interval`，block 内双向 | public recipe 不是论文所述 PCAM |
| condition dropout | 每个 HFSQ residual layer 独立 drop，`p=0.2` | music/leader modality 各自 drop，`p=0.1`，所有 HFSQ levels 共用 mask | 不支持 layer-isolated conditional learning |
| LDCFG | 每个 residual layer 独立 guidance | 计算 unconditional 后直接 `return pm_conditioned` | guidance scale 是输出 no-op，且多做一次 forward |
| Stage2 epochs | 1500 | 501 | 训练预算不一致 |
| Stage2 batch | 256 | 128 | 优化 recipe 不一致 |
| Stage1 epochs/batch | 200/256 | 301/512 | Stage1 public recipe 也不完全等同论文 |

这不自动证明论文结果无效，但说明不能把 paper table、official config 和本地 `epoch_500` 当成同一个 run contract。第一步必须明确目标是“复现 public release”还是“复现 paper method”。

### 4.2 `C`：HFSQ 权重没有被 optimizer 更新，但没有真正冻结

official 的 optimizer 只接收 `self.model.parameters()`；HFSQ 是 Lightning module 上独立的 `self.hfsq`，没有注册进 denoiser，所以旧版所述 optimizer pollution 不成立。

但 `self.hfsq = hfsq.cuda().eval()` 只切换 eval mode，没有：

- `self.hfsq.requires_grad_(False)`；
- 对 `encode/decode target` 使用 `torch.no_grad()`；
- 对 `x_start` 或 geometry target 做 detach。

HFSQ encode 中的 FSQ/project path 允许梯度传播，手动优化又只对 Stage2 optimizer 执行 `zero_grad()`。所以 Stage1 参数可能持续累积无用 gradients，增加显存和计算；权重本身因不在 optimizer 中不会更新。

**结论**：这是应该修的训练硬伤和 provenance 风险，但不是 official 远距离选择性退化的直接解释。

### 4.3 `C`：`TR_*` 权重配置没有按名字生效

loss key 为 `Geometry_TR_recon`、`Geometry_TR_vel`、`Geometry_TR_acc`，聚合代码却使用：

```python
self.weights[term.split('_')[-1]]
```

实际路由分别变成 `w_recon/w_vel/w_acc=0.1`，而不是 YAML 中的 `w_TR_recon/w_TR_vel/w_TR_acc=0.05`。

因此：

- official 实际 root geometry 权重比 YAML 声称的高一倍；
- 不能把远距离失败简单归因为“root loss 太小”；
- 任何 `TR_*` weight ablation 在修复 key routing 前都不可解释。

此外，`forward_reconstruction` 只用 `w_recon` 决定 recon/vel/acc 三项是否全部启用；`forward_translation` 也只用 `w_TR_recon` 控制三项。独立开关语义并不存在。

### 4.4 `C`：decoded geometry loss 对所有 diffusion timesteps 生效

训练均匀采样 `t∈[0,999]`，对每个 `t` 的 `x0_pred` 都：

1. 解码为 motion；
2. 与单一 GT/HFSQ reconstruction target 做 L1 geometry regression；
3. 不使用已创建的 p2/SNR weight，也没有低噪声 gating。

在高噪声 `t`，far/open dance 的 relative root 后验可能多模态或不确定。此时对 decoded path 施加确定性 L1/L2 目标，可能强化 conditional median/mean，表现为向数据中更常见的近距离 mode 收缩。这一机制与“近距离好、远距离坏”有直接方向一致性，优先级高于单纯增加 root loss。

### 4.5 `C`：interaction geometry 对 far region 的显式约束较弱

`DM` 只对 `pred_distance < 1 m` 的 joint-pair 距离计算匹配，`JA` 只对 GT contact `<0.1 m` 生效。远距离/open choreography 中，大量 joint pairs 不进入 `DM/JA`；剩余约束主要是 latent MSE 与 `TR_recon/vel/acc`。

这不等于 far samples 没有监督，但意味着 close/contact mode 拥有额外的几何约束，而 far mode 更依赖 `tr` latent conditional modeling。该不对称与用户观察相符。

### 4.6 `C`：CFG/LDCFG 是 no-op

`guided_forward` 计算 unconditional 与 fully conditional 后立即：

```python
return pm_conditioned
```

后续 guidance 混合不可达；不可达分支还引用未定义的 `m_guidance_weight`。因此 official `sample_mode` 的 `pm_guidance_weight=1.2` 与普通 conditional sampling 输出相同，只多一次 denoiser forward。

这说明：

- guidance 不是当前 far failure 的原因，因为它实际上没有改变输出；
- official code 无法复现论文的 LDCFG table；
- 修复 CFG 会改变采样分布，必须作为独立 ablation，不能悄悄混入 baseline。

### 4.7 `C`：DDIM 少执行第一步

50-step DDIM 原本生成 50 pairs，从 `(999,979)` 到 `(19,-1)`。代码执行 `[1:]` 后只剩 49 pairs，从 `t=979` 开始处理标准高斯，跳过 `999→979`。

该偏差在 cosine schedule 的高噪声端可能影响不大，但它是明确且低成本可验证的 sampler mismatch。优先做相同 noise 的 49-step/50-step parity，不应先假定它是 teleport 主因。

### 4.8 `C`：训练评估、正式 synthesis 和指标不统一

official 存在以下路径差异：

- train-time full test eval 调用普通 `sample`；
- standalone synthesis 调用 `sample_cfg`，当前输出虽相同但计算路径不同；
- standalone synthesis 额外执行 `motion_temporal_filter`；
- train-time eval 与 synthesis 都由 `use_amp=True` 包裹；
- config 的 `Trainer.precision=32` 不等于上述 sampling 强制 fp32。

指标方面：

- MPJPE/MPJVE 先逐帧减去 follower root，完全看不见 global relative-root error；
- duet FID 使用整段时间平均的 pairwise distances，能感知总体距离分布，但不能定位瞬时 teleport 或 block boundary；
- official checkpoint callback 只是每 50 epochs 保存，不按这些指标自动选 best；
- `val_dl` 和 training-time full evaluation 都来自 `split=test`，属于 test-set reuse。

这些问题会掩盖或混淆 failure，但不能单独生成 distance-selective error。

### 4.9 `C`：raw HFSQ latent normalization

`MotionNormalizerTorch` 读取 HFSQ normalizer 后，主动把 HFSQ mean 改为 0、std 改为 1。因此 Stage2 的 forward diffusion、unit Gaussian noise 和 latent loss都作用在 raw `all_quantizeds` 上。

既有 Stage1 checkpoint 的本地统计：

- 768 维 mean absolute average 约 `0.0374`；
- 逐维 std 从 `0.0354` 到 `0.8775`，约 `24.8×`；
- `tr` 分支约 `22.4×`；
- residual level 1/2 的平均 std 约 `0.4123/0.2605`。

这些数值需要在最终 canonical Stage1 hash 上重算，但 code-level identity normalization 已确认。

## 5. 症状证据及其边界

### 5.1 `O`：旧 `epoch_500` 输出复现 distance-selective failure

旧归档目录：

`results/generated/ReactDance/reactdance/epoch_500.ckpt/samples/pos3d_npy`

对 34 个 test sequences 的水平面 relative root 测量：

| GT 每段平均距离 | 样本数 | GT 平均距离 | 预测平均距离 | relative-root ADE |
| --- | ---: | ---: | ---: | ---: |
| `<0.4 m` | 12 | 0.274 m | 0.255 m | 0.098 m |
| `0.4–0.8 m` | 2 | 0.686 m | 0.722 m | 0.484 m |
| `0.8–1.2 m` | 17 | 0.989 m | 0.811 m | 0.637 m |
| `>1.2 m` | 3 | 1.295 m | 0.827 m | 0.954 m |

GT mean distance 与 root error 的相关系数约 `0.955`。结果显示模型在 far samples 上向中等/较近距离收缩。

> [!warning] Provenance 限制
> 该目录命名与 official recipe 对齐，但当前没有把 checkpoint SHA、official commit、config snapshot、normalizer SHA、sampler、dtype 和 filter 绑定在一起。因此这些数值只证明用户描述的症状确实存在，不能证明某一个后续调整优于或劣于 official。

### 5.2 `C/O`：far 是尾部，distance 与 dynamics 混杂

既有 DD100 train 统计覆盖 133 pairs、279,576 frames、61,951 个 stride-4 windows：

| 统计 | 数值 |
| --- | ---: |
| window mean distance median | 0.591 m |
| p90 / p95 / p99 | 1.262 / 1.567 / 2.130 m |
| window mean distance `≥1.5 m` | 5.84% |
| frame distance `≥1.5 m` | 8.26% |

window mean distance 与 distance range 的相关系数约 `0.809`。所以实验必须用“mean distance × distance range”二维分桶；只按 high-variation 分组会把绝对距离与动态混在一起。

### 5.3 `O`：BLC boundary 是放大器

旧 `epoch_500` 输出中，距每个 240-frame boundary ±4 frames 的 root step error 约为 block interior 的 `1.33×`；大 jump 在 boundary 邻域富集，但多数错误仍发生在 block 内。

因此 BLC 无 anchor 很可能解释“瞬移感”的一部分，但不是 far absolute-placement error 的唯一来源。

## 6. 实验前机制猜想与优先级（保留作预注册）

> [!note] 阅读口径
> 本节与第 7–8 节保留实验前的假设和判据，用于防止事后改写。已完成结果与当前排序以第 10.4–10.9 节为准。

### 6.1 远距离失败

| 排名 | 假设 | 支持度 | 关键证据/预测 |
| --- | --- | --- | --- |
| P1 | **far/open choreography 条件不充分且是尾部，模型向常见 close mode 回归** | 高 | official 删除 leader root trajectory；不提供 initial relative offset；far windows 少；误差随 distance 急升 |
| P1 | **所有 `t` 上的 decoded geometry regression 强化高噪声 posterior mean/median** | 中高 | geometry loss 无 SNR/gating；far/open conditional entropy 更高；按 `t` 测 root gradient/预测收缩应在高 `t` 最明显 |
| P1 | **close mode 有 `DM/JA` 额外约束，far mode 主要依赖 `tr` latent** | 中高 | `DM` 阈值 1 m、`JA` 阈值 0.1 m；far relational geometry coverage 低 |
| P2 | **raw HFSQ latent 各向异性导致分支/维度有效 SNR 失衡** | 中高 | official identity normalization；逐维 std 约 `24.8×`；true z-score 应改善 standardized error |
| P2 | **continuous `z_pred` 偏离 HFSQ support，`tr` decoder 邻域不平滑** | 中 | recon 好不能排除；若 `D(E(D(z_pred)))` 显著恢复则成立 |
| P2 | **独立 BLC blocks 缺 root anchor，边界重新采样 offset mode** | 中 | boundary error 富集；oracle anchor 应只改善 boundary、不修复 block interior ADE |
| P3 | **49-step DDIM、AMP 或 filter 造成主要 far failure** | 低到中 | 它们是合同问题，但缺 distance-specific 机制；matched parity 可快速证伪 |
| 已撤回 | official HFSQ decoder 被 Stage2 optimizer 污染 | 不成立 | official module registration/optimizer path 不支持该机制 |

这里的 P1 不是说“leader absolute world position 必须输入”。更准确的是需要验证：translation-invariant 的 leader root velocity/anchored trajectory，以及 initial relative-placement control，是否能降低 far/open mode 的条件熵。

### 6.2 音乐不敏感

| 排名 | 假设 | 支持度 | 关键预测 |
| --- | --- | --- | --- |
| P1 | **60-token block pooling 丢掉 local music timing** | 高 | pooling 前 music token 有时序 variance，pooling 后同一 block response 近似常量；`music_time_merged=False` 应提高 phase-shift sensitivity |
| P1 | **leader 是高带宽 music proxy，形成 shortcut** | 高 | fixed music 换 leader 的输出变化远大于 fixed leader 换 music |
| P1 | **论文的 layer dropout/LDCFG 没有在 official 实现** | 已确认 | 当前 `p=0.1` modality dropout 不能强迫各 HFSQ levels 学独立 music contribution |
| P2 | **训练目标和监控指标不奖励 music 的独特信息** | 高 | matched 与 shuffled music 的 denoise loss差异小；现有 root-centered motion metrics 不测反事实 sensitivity |
| P2 | **music branch gradient/scale 被 leader path 压制** | 中 | pooling 前尚有信息，但 finite-difference response 与 gradient norm 远小于 leader |
| P3 | **原始 music feature 本身不含有效节奏** | 低 | 只有 time-resolved fusion 和 probe 仍失败后再检查输入 feature |

## 7. 已执行的验证计划（原预注册）

### Phase 0：锁定 official baseline 与实验合同

#### V0.1 两套 recipe 不再混称

明确区分：

1. `B-release`：严格复现 official public config/behavior。
2. `B-paper`：按论文实现 causal PCAM、per-layer `p=0.2` dropout、LDCFG、1500 epochs、batch 256。

本轮诊断先用 `B-release` 与现有 official checkpoint；`B-paper` 只有在 release failure 已定位后再训练。任何表格必须有 `recipe`、commit、checkpoint SHA 和 config hash。

#### V0.2 建立不改变输出语义的 clean evaluator

固定：

- 直接调用 conditional `sample`，CFG 标为 disabled；
- fp32、相同 initial noise、相同 49-step official DDIM；
- metric 前不做 temporal filter；filter 另列 visual-only；
- 相同 test IDs、leader/follower 顺序与 HFSQ decoder hash；
- 不使用 test split 选择超参数，另建 held-out validation IDs。

新增：

- relative-root ADE/FDE；
- root distance MAE、方向误差；
- root velocity/acceleration error；
- teleport rate，阈值由 train GT root-step 的 p99.9 或 robust MAD 预注册；
- boundary ±4/±16 与 block interior 分开；
- local root-centered MPJPE 与 global MPJPE 并列；
- 所有指标按 mean distance × distance range 二维 buckets 报告。

#### V0.3 冻结与 loss 语义测试

不改变 Stage2 function 的 hygiene patch：

1. `self.hfsq.requires_grad_(False)`。
2. GT encode/decode target 放入 `torch.no_grad()` 并 detach。
3. optimizer names、Stage1 tensor hash、100-step hash equality 做 assertion。
4. 修复 `TR_*` key routing，但先把 `w_TR_*` 设为 `0.1` 以保持 official 实际有效权重；之后再单独 ablate。
5. 为 recon/vel/acc 三项各自的 enable/weight 写 unit test。

#### V0.4 sampler parity

固定 checkpoint/noise 比较：

- official 49-step DDIM；
- 补回 `(999,979)` 的 50-step DDIM；
- AMP vs fp32；
- filter off/on，仅看后处理影响。

如果 50-step 只带来微小变化，就把 sampler 从主因列表降级。CFG 修复另开实验，不混入此 parity。

**Phase 0 成功标准**：同一 checkpoint 可重复；所有配置改动有行为测试；root collapse/teleport 不再被 aggregate metrics 隐藏。

### Phase 1：零重训的 failure localization

#### V1.1 五级 oracle chain

对 close-stable、close-dynamic、far-stable、far-dynamic 四个 buckets 比较：

1. GT。
2. `D(E(GT))`。
3. teacher-forced `x0_pred(t)`，固定 noise，`t={0,50,250,500,750,999}`。
4. 完整 DDIM `z_pred`。
5. round-trip projection `D(E(D(z_pred)))`。

分别记录 `up/down/tr`：

- raw MSE 与 true-std standardized MSE；
- predicted mean/std、tail quantiles、effective rank；
- `z_pred` 到 `E(D(z_pred))` 的距离；
- decoded root ADE/velocity/teleport；
- latent loss与每项 geometry loss的 gradient norm/cosine，按 timestep 和 bucket 分开。

判读：

| 结果 | 指向 |
| --- | --- |
| far 在高 `t` 已向近距离收缩，低 `t` 尚可 | all-t geometry / x0 posterior regression |
| teacher-forced 各 `t` 好，full DDIM 才坏 | sampler/error accumulation |
| round-trip 显著恢复 | off-support / decoder local continuity |
| projection 无帮助，`tr` target 本身预测错 | conditional information / tail coverage |
| 仅 boundary 坏 | BLC anchor |
| block interior 也随 distance 变差 | far-tail supervision/condition 为主 |

#### V1.2 root conditional-information oracles

先用小型 root-only diagnostic 或 frozen checkpoint probe，不立即改 unified architecture：

- `C0`：official leader local pose + music。
- `C1`：`C0 + leader root velocity`。
- `C2`：`C0 + anchored leader root trajectory`，首帧归零。
- `C3`：`C0 + GT initial relative root`，只作为 upper-bound oracle。
- `C4`：`C0 + desired initial distance/direction token`，若任务允许用户控制初始站位。

若 `C1/C2` 改善 far-dynamic，说明删除 leader locomotion 是信息瓶颈；若只有 `C3/C4` 改善 far-stable，说明 initial placement/mode ambiguity 是核心；若都无效，再转向 latent/loss。

#### V1.3 music counterfactual quartet

固定 leader、initial noise、`x_t` 和 timestep，只替换 music：

1. matched；
2. 同 genre/tempo shuffled；
3. circular phase-shifted；
4. zero。

正对照为固定 music、swap leader；负对照为完全相同条件重复 forward。测：

- matched vs mismatched denoise loss gap；
- `up/down/tr` 的 `Δx0` 和 decoded `Δmotion`；
- output beat 对输入 music beat，而不是 leader beat；
- music-sensitivity / leader-sensitivity ratio。

#### V1.4 BLC boundary oracle

同一序列比较：

- 单独生成恰好 240 frames；
- full-length BLC 中对应 block；
- 后一 block root offset 平移接续前一 block，仅作 oracle；
- root latent overlap/inpainting，仅作 oracle。

若 oracle 只消除 boundary jumps，保留 block interior far ADE，则 BLC 是放大器，不是首因。

**Phase 1 stop-loss**：完成这一步前，不重训 HFSQ、不上 root/body 大改、不加 RL。

### Phase 2：最小短程训练矩阵

每项只改一个变量，先用固定 steps/10% budget 筛选；相同 Stage1、seed、noise 和 evaluator。

#### V2.1 timestep-aware geometry

从冻结干净的 official baseline 比较：

- `L0`：现状，所有 `t` geometry。
- `L1`：geometry 只在低噪声 `t` 生效。
- `L2`：按 SNR/p2 对 geometry weighting。
- `L3`：只对 `tr` geometry 做 timestep gate，body 保持不变。

选择标准不是总 loss，而是 far-stable root ADE、far-dynamic root velocity 和 near local quality 的 Pareto 改善。

#### V2.2 distance-balanced sampling

比较 uniform 与按 train window mean distance 分层的 sampler；distance range 只做正交 stratification。每 epoch 保存实际 sampling histogram，避免再次出现“配置存在但干预未发生”。

#### V2.3 root condition

只训练 Phase 1 oracle 支持的最小输入：

- leader root velocity 或 anchored trajectory；
- initial relative-root/distance token；
- 若任务不允许给初始站位，则用可采样 distance/direction mode token，而不是把 GT 泄漏到正式推理。

#### V2.4 true latent z-score

比较：

- `Z0`：official raw HFSQ latent。
- `Z1`：train-only true per-dimension mean/std，对 `up/down/tr` 一致用于训练、加噪、loss、sampling 与 inverse decode。

不能只在 decode-time 切 normalizer。判据是 standardized latent error 和 far root 同时改善，且 HFSQ recon 与 near quality 不退化。

#### V2.5 time-resolved music

第一对照只切已有开关：

- `M0`：`music_time_merged=True`。
- `M1`：`music_time_merged=False`，music 与 leader time-resolved tokens 一起进入 cross-attention。

先看 counterfactual sensitivity，再看 aggregate FID/BAS。若 `M1` 有 sensitivity 但 interaction 下降，下一步才增加有效的 leader-drop/music-keep 比例或对 lower-body/root 加 music gate。

#### V2.6 何时才改 tokenizer/architecture

只有满足以下之一才进入 ReactDance++ 表示改造：

- conditional oracle、timestep-aware loss、balanced sampler 和 z-score 均不能修复 far root；
- round-trip 明确证明 `tr` decoder 邻域不连续；
- root-only diagnostic 好而 unified model 差，证明 body/root interference。

届时按成本递增：

1. root/body denoising heads 解耦，但共用同一 frozen HFSQ 与 evaluator。
2. `tr` 表示改为 initial offset + delta/velocity，并验证长程积分漂移。
3. prior-aligned continuous root latent 或独立 root AE。

## 8. 实验前优先级排序（最终更新见第 10.9 节）

### 8.1 先做 gates，不把它们误称为科学主因

1. Stage2 四 key 精确映射，随后 strict load；记录 checkpoint/config/code/normalizer hashes。
2. HFSQ 真冻结、target detach、`TR_*` routing 语义修复。
3. root-aware evaluator 与 held-out validation。
4. plain conditional、fp32、filter-off 的唯一评估入口。
5. 49/50-step DDIM parity。
6. 论文 method 与 release recipe 分表，不再混报。

### 8.2 远距离科学假设顺序

1. **root 条件信息/初始 placement ambiguity + far-tail coverage。**
2. **all-timestep decoded geometry 导致高噪声 mode averaging。**
3. **raw HFSQ latent anisotropy / off-support。**
4. **BLC block root anchor 缺失。**
5. **sampler/AMP/filter 细节。**
6. **重新设计 HFSQ 或 root/body architecture。**

### 8.3 音乐科学假设顺序

1. **block-pooled music vs time-resolved leader 的结构不对称。**
2. **leader shortcut + 当前 modality dropout 不足。**
3. **训练/评估没有反事实 music objective。**
4. music branch scale/gradient。
5. 新音频特征或复杂 rhythm module。

## 9. 当前不建议做的事

- 不再用 5090/4090 调整后的无效 run 给建议排序。
- 不把后续分支的 shared decoder pollution 归因到 official。
- 不把 `hard_mining/curriculum` no-op 写成 official bug。
- 不因为 `TR_*` YAML 数值小就继续加权；当前实际路由是 `0.1`，先修语义。
- 不在正式推理默认启用 CFG；修复后的 matched sweep 没有改善整体/far 权衡。
- 不先多训到 1500 epochs；先确认 release/paper recipe 和 failure mechanism。
- 不重训 HFSQ；projection 与短程 z-score 已未命中，只有从头 Stage2 matched training 才保留 true z-score 选项。
- 不把 filter 后视频与未 filter 指标混在一张表。
- 不用 root-centered MPJPE 判断远距离是否修好。
- 不把 causal PCAM、LDCFG、501-epoch public model 和论文 1500-epoch结果混称为同一实现。

## 10. 3090 official-baseline 实测

### 10.1 基线与 checkpoint 合同

测试分支为 `diagnostics/official-stage2-audit-3090`，直接起于 official `main@3d7bc407`。本地 `main@cd547ed` 与 official 无共同 merge base，不能作为正式基线；其 4 月修改只能逐项作为候选干预。

| 对象 | 核心结果 |
| --- | --- |
| Stage1 `epoch_200.ckpt` | SHA256 `279df3b2...476b864`；metadata epoch 200、step 23707；official `LitReactDance_hfsq` strict load 无 missing/unexpected key |
| Stage2 `epoch_500.ckpt` | SHA256 `570acbbd...1868b`；文件名为 500，但 metadata epoch 477、step 129538 |
| Stage2 recipe | checkpoint 随附 YAML 为 801 epochs、batch 128、`dtype=both`；当前 public YAML 为 501 epochs、batch 128、`dtype=['pos3d']` |
| Stage2 official 直接加载 | 四个 `feature_encoder.{music,leader_pos}_input_attn.downsample.{weight,bias}` missing，同时出现四个旧 `mda.mda.*` unexpected key |
| 精确兼容映射 | 四个逻辑 key 在共享 module 下对应八个 serialized aliases；映射后 full generator 703/703 strict load，内嵌 Stage1 426/426 与外部 checkpoint 逐 tensor 相等 |
| music normalizer | official branch 未发布该文件；probe 使用本地 `main:data_lazy/music/music_normalizer.pt`，SHA256 `c95787fd...9068067` |

官方 sample loader 使用 `strict=False`，因此不会报错，而会让四个已训练的条件输入投影保持随机初始化。单个固定输入上，未映射与正确映射模型的 denoiser 输出相对 RMS 差异为 `91.91%`，其中 `tr` 为 `102.02%`。

> [!warning] 解释边界
> 这是 release 复现硬伤，也是所有后续 official-checkpoint 诊断的 P0 gate；但它不自动解释原训练代码自身产生的远距离失败。若原训练/推理始终使用旧命名，两端可能一致。随附 YAML 差异与缺失 normalizer 也意味着该 checkpoint 不能视为“按当前 public YAML 从头复现”的 matched baseline。科学归因必须在正确映射并绑定全部哈希后进行。

### 10.2 远距离 root 误差

对既有 `epoch_500.ckpt` 生成目录中的 34 个序列，分别在预测 leader 坐标系与 GT leader 坐标系中计算相对 root，避免把预测 follower 与 GT leader 混用。

| GT 平均距离桶 | 序列数 | GT 距离 | 预测距离 | relative-root ADE |
| --- | ---: | ---: | ---: | ---: |
| `<0.4m` | 12 | 0.274m | 0.255m | 0.098m |
| `0.4–0.8m` | 2 | 0.686m | 0.722m | 0.484m |
| `0.8–1.2m` | 17 | 0.989m | 0.811m | 0.637m |
| `>=1.2m` | 3 | 1.295m | 0.827m | 0.954m |

核心读数：

- GT 平均距离与 relative-root ADE 的跨序列相关系数为 `0.955`。
- 最远桶的预测平均距离从 GT `1.295m` 收缩到 `0.827m`，支持“向常见近距离 mode 回归”，而不只是局部姿态变差。
- 240-frame BLC 边界附近 root step error 是内部的 `1.366×`；top 5% 大跳步在边界的富集倍数为 `2.387×`。因此 BLC 更像瞬移放大器，尚不能判定为最初根因。
- `0.4–0.8m` 只有 2 个序列，不用于单独下结论；主要对比为 close、`0.8–1.2m` 与 far。

### 10.3 music 与 leader 条件敏感性

在四个距离分位窗口上，用 `t={50,500,950}`、两个固定 seed 构成 24 cases；每次固定 noisy latent，只替换一个条件。以下均为正确四 key 映射后，输出变化 RMS 除以 baseline 输出 RMS：

| 反事实干预 | 相对 RMS 变化均值 | 中位数 |
| --- | ---: | ---: |
| music phase shift | 0.093% | 0.063% |
| swap music | 1.575% | 1.242% |
| zero music | 1.638% | 0.934% |
| swap leader | 77.295% | 90.891% |
| `swap music / swap leader`，逐 case | 4.017% | 2.458% |

leader 的影响按逐 case 比值约为 music 的 `25–41×`。四个距离窗口均保持 leader-dominant；最远 Samba 窗口的比值中位数约 `1.27%`。这直接支持 leader shortcut 与条件路径不对称，但该 probe 只测单步 denoiser 机制，不代替完整 DDIM 生成、节拍对齐与感知评价。

同一 probe 也实证 `pm_guidance_weight=1.2` 与 plain conditional 输出逐元素完全相同，确认当前 CFG 是 exact no-op。

### 10.4 strict checkpoint 可视化确认

精确映射四个逻辑参数后，完整 generator `703/703` strict load；checkpoint 内嵌 Stage1 `426/426` 与外部 `epoch_200.ckpt` 逐 tensor 相等。固定 seed 重复生成的 latent `max_abs=0`。

| 距离 | 样本 | Stage1 root ADE | Stage2 root ADE |
| --- | --- | ---: | ---: |
| near | `Waltz_010_000[f1380]` | 0.0116m | 0.0435m |
| mid | `Qiaqiaqia_010_004[f2040]` | 0.0346m | 0.3080m |
| far | `Samba_005_001[f360]` | 0.1563m | 1.5082m |

三段视频均同时展示 GT、Stage1 strict 与 Stage2 remapped-strict 的正视/俯视结果。Stage1 视觉重建与既有判断一致；正确加载的 Stage2 仍在 far 样本产生错误路径和大位移。因此 key mismatch 是 release 复现 gate，不是原始 far failure 的充分解释。机器可读 manifest 与视频位于 `results/diagnostics/checkpoint_triplet/`。

### 10.5 far failure localization 与 matched 短训

far 样本的分支 oracle：

| 组合 | root ADE |
| --- | ---: |
| Stage2 baseline | 1.5082m |
| predicted body + Stage1/GT `tr` | 0.1563m |
| Stage1/GT body + predicted `tr` | 1.5082m |

结论是错误几乎全部由 `tr` 分支承担。首帧 offset、最佳常量平移、最佳刚体 XY 对齐只能把 far ADE 分别降到 `1.296/1.227/1.052m`，仍远高于 Stage1 floor；因此模型选错的是完整相对轨迹/方向 mode。teacher-forced `t=950` 时，far `tr` latent MSE 为 `0.1789`，near 为 `0.0348`，差距在完整 DDIM 前已经形成。

精确 lazy dataset 与 official preprocessing 逐元素一致：train 共 `60,713` windows，near `41.7%`，far `7,103` windows、占 `11.7%`。四个 150-step matched 诊断均从同一 release checkpoint、optimizer state、seed 和 8 个固定 test windows 开始：

| 变体 | 唯一干预 | far root ADE | far distance MAE | near root ADE |
| --- | --- | ---: | ---: | ---: |
| control | uniform/local/all-`t` | 0.554m | 0.371m | 0.034m |
| balanced | 四距离桶等概率 | 0.609m | 0.491m | 0.031m |
| anchored | leader anchored root + train-only stats | 0.628m | **0.196m** | 0.042m |
| low-`t` | geometry 仅在 `t≤500` | 0.614m | 0.420m | 0.040m |

release 在同一固定 far 窗口上的起点为 root ADE `0.714m`、distance MAE `0.270m`。control 说明继续训练能部分调整方向，但距离仍恶化；balanced 不优于 control，否定“只因 far 数量少”；anchored 更会保持距离，却未恢复完整路径；low-`t` 不支持高噪声 geometry 是首要单因。每桶只有两个固定窗口，所以这些是机制筛选，不是最终 benchmark。

### 10.6 完整 music 反事实与最小训练对照

四个距离分位窗口、两个 seed；每个 case 固定 leader、初始 noise 和 sampler，只替换 music。完整 49-pair DDIM 结果：

| 干预 | 最终 latent 相对 RMS | 关键读数 |
| --- | ---: | --- |
| phase shift 60 frames | 0.103% | 时间错位几乎不改变输出 |
| swap music | 3.04% | 中位数为 1.87% |
| normalized-zero music | 1.78% | 删除 music 仍影响很小 |
| swap leader | 133.3% | leader 改变整个生成 mode |

逐 case `swap music / swap leader` 的 latent 中位数为 `1.38%`，`tr` 为 `1.02%`，解码 translation 为 `0.40%`。matched local follower 的 beat alignment 对输入 music 为 `0.212`，对 root-centered leader 为 `0.558`。world-space beat 分数因共享 leader root 有机械相关，结论只使用 root-centered local 指标。

两个 150-step 对照：

| 变体 | music sensitivity | 质量代价 | 判断 |
| --- | --- | --- | --- |
| time-resolved | phase shift `0.103%→2.26%`；music/leader 中位数 `1.38%→2.95%` | matched local beat-to-music 仅 `0.231`；far ADE/distance MAE `0.664/0.481m` | block pooling 是因果瓶颈，但单独解开不够 |
| leader-drop/music-keep | phase shift仅 `0.131%`；music/leader 中位数 `2.45%` | near ADE `0.087m`，mid/far 同样退化 | 强 dropout 淘汰 |

time-resolved 模型使用 parity initialization：训练前与 release denoiser `max_abs=0`；新增 fusion 参数单独低 LR 与 clip，旧 344 个参数保留 release optimizer state。由此可以把 sensitivity 增量归因给逐 token music 通路，而不是随机重初始化。

### 10.7 HFSQ manifold 与尺度

HFSQ train normalizer 的 per-dimension std 为 `0.0354–0.8775`，跨度 `24.78×`，说明 raw latent 各向异性确实存在。但 off-manifold projection 没有形成对应的运动修复：

| 指标 | Stage2 | `D→E→D` projected |
| --- | ---: | ---: |
| overall root ADE，16 cases | 0.3895m | 0.3865m |
| far root ADE | 0.6813m | 0.6785m |
| overall local MPJPE | 0.1272m | 0.1262m |
| `tr` target standardized MSE | 8.45 | 9.26 |

Stage1 自身的 `D→E` 也不幂等，例如 down standardized MSE 为 `1.85`，所以 projection displacement 不能直接等同于“Stage2 在 manifold 外”。更重要的是 projection 对 far 仅改善 `0.0028m`，不足以解释米级失败。

这里的“不幂等”准确指：令 `z=E(x)`，观测到 `E(D(z))≠z`；它不是说视觉重建 `D(E(x))` 很差。HFSQ 的 `all_quantizeds` 保留两个 residual FSQ level 的逐层输出，但 decoder 会先对两个 level 直接求和。因而 decoder 只看求和结果，逐层之间如何分配并非完全可辨识；motion 经 decoder 后再编码，可能得到另一组逐层分解，同时仍对应相近运动。当前 `D→E→D projection` 因此只是“重新编码/量化控制”，不是严格的正交 manifold projection。

这也暴露出一个比普通各向异性更值得 P0 验证的目标错配：Stage2 diffusion 与 latent loss 逐维拟合 `all_quantizeds` 的特定 residual-level 分解，而最终 root decoder 只消费各 level 的和。下一步必须把 `tr` 误差拆成：

1. decoder 可见的 level-sum/path error；
2. decoder 不敏感的 residual redistribution/null error；
3. level-sum 正确但 root decoder/path 仍错误的部分。

只有第一项随 far 显著上升，才能把 raw latent 表示/损失错配升为核心原因；若主要是第二项，则 raw latent MSE 虽大，却不是 reactor 低质的直接来源。

从 identity 线性退火到真实 train-only z-score 的 150-step 控制，在终点 loss 升至 `6.08`；far ADE/distance MAE 为 `1.029/0.670m`，near ADE 为 `0.101m`。这只否定“从 release checkpoint 短程切换 z-score”，不否定从 Stage2 初始化时就使用 z-score；但结合 projection 结果，当前没有依据重训 tokenizer。

### 10.8 sampler、CFG 与 BLC

| 推理设置 | overall root ADE | far root ADE | far distance MAE |
| --- | ---: | ---: | ---: |
| official 49 pairs | 0.3920m | 0.7141m | 0.2700m |
| corrected 50 pairs | **0.3907m** | 0.7015m | **0.2641m** |
| CFG 1.2 | 0.4032m | 0.7043m | 0.2780m |
| CFG 2.0 | 0.4022m | **0.6977m** | 0.3461m |
| CFG 5.0 | 0.4046m | 0.7187m | 0.4155m |
| corrected50 + CFG1.2 | 0.4018m | 0.6957m | 0.2708m |

50-step 修正有小幅一致收益，应作为工程修复；真正启用 joint CFG 后，没有权重同时改善整体、far 路径和 far 距离，说明 guidance 放大了错误条件方向。CFG 不应默认开启。

3 个 720-frame/3-block 长窗口中，official Stage2 的 boundary root-step error 为 interior 的 `1.68×`；near/mid 约 `2×`，far 为 `0.99×`。continuity-velocity anchor 把 overall ADE `0.3303→0.3283m`，GT block-start anchor 反而恶化到 `0.3645m`。BLC seam 可单独修，但不能修复 far block interior 的错误轨迹。

### 10.9 更新后的当前优先级

1. **P0 baseline 固化**：保留四 key 映射、full strict load、HFSQ freeze/detach、正确 `TR_*` 路由、root-aware evaluator、loss 分项日志和 corrected 50-step DDIM。默认不启用 CFG。
2. **P0 `tr` target semantics**：先做 residual-level sum/null error decomposition；比较逐层 `all_quantizeds` loss、decoder-visible summed-quantized loss 与直接 root-path loss。该 gate 不需要 music 改造。
3. **P0 root trajectory 建模**：先用 root-only diagnostic 验证 `initial relative placement + relative velocity/path`；命中后再接独立 root trajectory head 或 `tr` head，并用生成 root 驱动完整 reactor。不得在正式推理泄漏 GT initial placement。
4. **P0 质量判据**：同时报告 root ADE/FDE、distance/direction、velocity/teleport、global MPJPE 和 local MPJPE。目标是修复整体 reactor motion，而不是只让 root 数值下降。
5. **P1 数据与训练**：distance-balanced 只作为 batch 合同；还要按 choreography dynamics、path curvature、relative speed 分层。true HFSQ z-score 仅作为从 step 0 开始的 matched control，不重训 tokenizer。
6. **P2 music**：music 不是伴舞生成的主 condition。保留已有反事实证据与 time-resolved 方案，但暂停训练，等 `tr` P0 命中后再评估是否需要加入 residual/gate。
7. **P2 long-form**：用 continuity anchor/overlap 修 BLC seam，但不得把它作为 far-distance 主修复。

核心源码位于分支 `diagnostics/official-stage2-audit-3090`；最终诊断代码 HEAD 为 `35d024c`。机器可读结果分别保存在 `results/diagnostics/` 与 `results/experiments/` 下，由 Git 忽略。

## 11. 当前最终判断

### 远距离问题

最可能的主链调整为：

```text
leader condition 删除 root locomotion，且没有显式 initial relative placement
  + far/open choreography 是低频、条件熵更高的 path/direction mode
  + Stage2 主要以逐点 latent/geometry 回归学习连续 tr，没有 mode-aware path 目标
  → tr 分支预测错误的整段相对轨迹，而不只是首帧 offset
  → 常见 close mode 的距离/方向先验主导；续训可改方向或距离之一，却难同时修复
  → BLC 在部分边界放大 seam，但 far block interior 已经错误
  → root-centered MPJPE 又隐藏 global placement failure
```

`tr` oracle 是当前最强定位证据。far-balanced、anchored root、low-`t` geometry、重新编码控制、短程 z-score、DDIM/CFG 均未成为充分修复，因此不能再把任何一项单独列为主因。普通 off-manifold 解释缺少米级收益证据；但 `all_quantizeds` 逐层 loss 与 decoder level-sum 的目标错配尚未被 sum/null decomposition 排除，作为 `tr` P0 子假设优先验证。

### 音乐问题

```text
leader motion 已隐含节奏
  + leader 保留逐 token cross-attention
  + music 被 60-token/240-frame mean pooling 后只做 FiLM
  + dropout 按 modality 而非 HFSQ layer，LDCFG 又未真正实现
  + 现有指标不测 fixed-leader music counterfactual
  → 网络优先走 leader shortcut
  → phase-shift music 时最终 latent 几乎不变
  → time-resolved 通路能提高 sensitivity，但没有充分的 music objective/gate 来转化为节拍和质量收益
```

### 一句话决策

**下一轮只做 `tr` P0：先判定 residual-level sum/null target mismatch，再训练显式 relative-placement/root-path 或独立 root head，并以整体 reactor 的 global/local 指标验收。music 后移；corrected DDIM 和 BLC continuity 只作工程修复，HFSQ tokenizer、强 leader dropout 与 CFG 不进入当前主线。**

## 12. official 证据锚点

代码基线：

- [official commit](https://github.com/RipeMangoBox/ReactDance/tree/3d7bc40727097b4b0bf506b05f430306f76acdb4)
- `LightningModel.py:652-732`：HFSQ 加载、未冻结、leader per-frame root removal、Stage2 target。
- `LightningModel.py:744-825`：train-time eval 与 standalone synthesis 分叉、CFG 与 filter。
- `models/hfsq_rep/fullbody_hfsq.py:140-166`：leader local pose 与 `translf` 定义。
- `models/reactdance/denoiser.py:500-535`：CFG early return。
- `models/reactdance/denoiser.py:553-647`：music/leader pooling、dropout 与 fusion。
- `models/gaussian/GaussianDiffusion.py:295-345`：DDIM pair skip。
- `models/gaussian/GaussianDiffusion.py:419-502`：raw latent x0 loss、任意 `t` decode 后 geometry。
- `models/nets/losses.py:435-475`：`DM/JA` mask 与 `TR_*` weight routing。
- `models/model_utils/data_utils.py:107-117`：HFSQ stats 被改为 identity。
- `models/nets/nn.py:6-45`：`interval` 与 `triangle_interval` mask。
- `models/reactdance/layers/structure_utils.py:158-220`：每块重启 positional encoding。
- `utils/metrics_duet_on_training.py:175-207`：root-centered MPJPE/MPJVE。
- `reactdance.py:16-54`：val/test loader 都来自 test config。
- `reactdance.py:196-214`：periodic checkpoint，不按 root metric 选 best。
- `configs/reactdance.yaml:13-24,37-52,77-106,124-147`：official Stage2 recipe。

论文：

- Section 3.3–3.5：Stage2 objective、BLC/PCAM/PPE、LDCFG。
- Appendix A.2：Stage2 1500 epochs、batch 256。
- Table 5：HFSQ reconstruction 随 `R` 改善而 diffusion generation 变差，证明 recon 不足以代表 diffusion-friendliness。
- Table 8：condition ablation 只能证明 retrained aggregate effect，不能证明同 checkpoint 的 music counterfactual sensitivity。

## 13. 2026-07-18 本地 Stage1 generatability 与 Stage2 适配 screen

> [!warning] 证据边界
> 本节是本地 `HFSQ_tr_sum_cycle_w0p1_from_scratch_3090` 家族的筛查记录，不是 official baseline 的替代，也没有使用它更新第 10 节的正式 comparison。所有生成质量读数仍需经过独立 held-out contract 才能进入正式结果表。

### 13.1 停止当前 Stage2 训练

已向运行中的 Stage2 进程发送 `SIGINT`，训练正常退出；当前没有匹配的 `reactdance.py ... stage2` 训练进程。最近一个完整、可恢复检查点为：

- `epochepoch=249.ckpt`，SHA256 `644f9c9dbe58ebb53a6d59a2297d3eea49432ba6adc6ee87f426bc98af9222ed`；metadata 为 epoch `249`、global step `118500`。
- Stage1 `last.ckpt`，SHA256 `5ef5734b0427081a0c98c68bc3f329e84e673b87bd09970afbb700a522890fbc`。

之后只完成到 epoch `280` 的部分训练/评估，没有新的完整 checkpoint；保留其日志和中间 artifact，不将其当作可恢复状态。

停止依据是没有稳定的 held-out 改善，而不是单个随机 synthesis 点：`VAL_LOSS` 的全程最低值为 `0.292654`，在 global step `3791`；epoch `200–239` 到 `240–279` 的均值由 `0.363382` 升至 `0.366078`，`mpjpe` 由 `123.394` 升至 `125.153`，`fid_k` 由 `15.847` 升至 `18.430`。epoch `280` 的单个 `fid_k=5.753` 不足以推翻该判断，因为 train-time eval 复用了 test split 且逐 epoch synthesis 波动很大。

### 13.2 冻结 Stage1 的生成适配性探测

机器可读结果：`ReactDance_Open_Process/results/diagnostics/stage1_generatability_hfsq_tr_sum_cycle_3090/generatability.json`。探测使用 train-only latent 统计与固定 seed 的 16 个 test windows，每个距离桶 4 个；它不替代固定预算的 Stage2 generation comparison。

- raw residual joint latent 的通道 std 比为 `26.34×`，decoder-visible level-sum 降为 `2.42×`，没有 dead channel。raw 表示的尺度/分解确实比 decoder 实际消费的空间更难条件化。
- decoder-visible nearest-neighbor 的 dance-style proxy 命中率为 `54.3%`，随机基线为 `10.5%`；distance bucket 为 `78.9%`，随机基线为 `24.7%`。这只是文件名前缀 proxy，不等价于语义检索证据。
- level-sum 尺度的 `0.20σ` 扰动，overall root ADE 相对 Stage1 decode 为 `1.46cm`，far 桶为 `3.22cm`；overall local MPJPE 为 `0.44cm`，运动学超过 train p99 的比例很低。sum-preserving residual redistribution 在数值精度内不改变 decode，验证了 sum/null 分解本身。

判定：Stage1 没有显示“微小 decoder-visible 扰动即崩坏”的充分证据，不能以 tokenizer 不可生成解释当前 Stage2 失败；但 raw residual 目标含有 decoder-invisible 自由度，必须在 Stage2 中显式审计，而不能只看 raw latent loss。

### 13.3 Stage2 raw/sum/null 教师强制诊断

机器可读结果：`ReactDance_Open_Process/results/diagnostics/stage2_sum_target_hfsq_tr_sum_cycle_3090/teacher_forced_epoch249.json`。该工具对本地 Lightning `model.* + hfsq.*` schema strict load，并逐 tensor 验证内嵌 HFSQ 与上列 Stage1 hash 相等；它在固定 test windows、固定噪声和 `t=50/500/950` 下只做教师强制 denoise，不训练也不采样。

在 `t=500` 的 far 桶，4 个窗口的 Stage1-relative root ADE 为 `0.123m`；`tr` raw error 的 decoder-visible fraction 为 `56.65%`，null fraction 为 `43.35%`，level-sum relative MSE 为 `0.115`。高噪声 `t=950` 的 far root ADE 升至 `0.793m`，`tr` level-sum relative MSE 升至 `0.873`，说明 far path 误差在完整 DDIM 前已经显著存在。

预注册的 sum-aware 短训 gate 要求 far `t=500` 的 visible fraction 至少 `60%` 且 root ADE 至少 `0.05m`。后者满足，前者不满足；不因观察到 `56.65%` 而事后调低门槛。因此不启动 sum-aware continuation。当前结果也排除了“误差主要全在 decoder-invisible null 空间”的解释，但不足以把 residual-level loss mismatch 升为主修复。

### 13.4 root-condition 适配筛查与下一门槛

机器可读结果：`ReactDance_Open_Process/results/diagnostics/root_condition_hfsq_tr_sum_cycle_3090/root_condition_screen.json`。固定预算 root-only regression 使用相同的小模型、初始化、优化器、500 step、距离均衡 train sampler 及 16 个 held-out test windows；它筛查条件信息，不是 Stage2 replacement。

| 条件 | far root ADE | 相对 C0 | 判定 |
| --- | ---: | ---: | --- |
| C0：现有 leader local 加 music | `1.153m` | — | baseline |
| C1：加 leader root velocity | `1.149m` | `0.35%` 改善 | 未命中 |
| C2：加 anchored leader root trajectory | `1.120m` | `2.80%` 改善 | 未命中 |
| C3：加 GT initial relative root，oracle | `1.032m` | `10.42%` ADE 改善 | FDE 回退，淘汰 |

C3 的 far FDE 为 `1.150m`，高于 C0 的 `1.119m`，且每桶只有 4 个窗口；联合 gate 因此淘汰 C1/C2/C3 全部条件。C3 只保留为“initial placement 存在有限可利用上界”的弱线索，不支持将 GT initial root 输入正式推理。C1/C2 未命中也表示单独恢复 leader locomotion 不是充分适配。

本轮没有 Stage2 condition adaptation 获得许可。若未来在独立 held-out contract 下重启该方向，只允许以下无泄漏合同之一：

1. 若任务接口允许控制初始站位，使用用户指定的 distance/direction token。
2. 若不允许外部控制，训练时从 train-only target 构造离散 root-placement mode，推理时必须由现有条件预测或采样该 mode，绝不读取 GT initial root。

进入 matched short screen 的验收条件是 far root ADE 和 FDE 同时优于 raw continuation，并且 near local MPJPE 不退化；否则保留当前结论，转向 root-path target/独立 `tr` head 而不是继续扩展条件。
