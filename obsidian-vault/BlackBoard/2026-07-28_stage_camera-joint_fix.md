---
title: "StoryMotion Camera / Joint 修复接力"
status: handoff_ready
tags:
  - StoryMotion
  - stage2
  - camera
  - joint
  - status/handoff
aliases:
  - Stage Camera Joint Fix
source_notes:
  - "[[ideas/StoryMotion/current]]"
  - "[[ideas/StoryMotion/StoryMotion-valid-metric-ledger]]"
  - "[[ideas/StoryMotion/StoryMotion-metric-computation-io]]"
  - "[[ideas/StoryMotion/2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]"
  - "[[ideas/StoryMotion/Storymotion-exp-sha]]"
created: 2026-07-28T15:26:42+08:00
updated: 2026-07-28T15:26:42+08:00
---

# StoryMotion Camera / Joint 修复接力

> [!abstract] 接力结论
> v9 protected-H 的 Human 路由已成功：Camera 训练前后 Human parameters、固定噪声输出和正式结果逐元素完全一致。当前 blocker 是同一 Camera branch 上的 Direct-C／HC 三段 curriculum：先发生跨 route 遗忘，随后约在 global `183K` 出现严重 pre-clip gradient instability，final `210K` EMA 被失败尾段主导。先评估已有 Camera snapshots并定位失稳，不得直接从失败的 `210K` optimizer state续训。C3-25 seed17 Unified-3 `105K` 继续作为 mainline。

## 1. 当前完成态

- Stage1：Pulp-only Human-anchor interaction-residual AE，`636K`，完成。
- Stage2 Human：ViMoGen-light teacher，`105K`，完成并冻结。
- Stage2 Camera：额外`105K`，global endpoint `210K`，完成。
- final `210K` Direct-H、Direct-C、joint-parallel first-512正式 eval均完成。
- Human fixed8及Direct-C／joint fixed8 vis artifacts完成。
- `140K`、`175K`、`189K`非final Camera snapshots尚未做同协议正式eval。
- 截至`2026-07-28T15:26:42+08:00`，4090上未发现当前v9训练／eval进程；接力前重新检查。

## 2. 硬约束

- Stage1／Stage2必须 `is_causal is False`。
- Direct-H只能消费Human text；Camera不得进入Human计算图。
- Camera训练后Human state与固定噪声输出必须exact不变。
- Direct-H、Direct-C、joint parallel来自同一Unified checkpoint。
- v9是diagnostic，`promotion_eligible=false`；不能替换C3-25 mainline。
- Camera14 separate与joint evidence不可混合。
- 新run记录exact parent checkpoint／owning decoder、cache／stats hashes、ordered IDs、seed、train/eval BS、sampler和split。
- 不修改旧run artifacts；新实验使用新run ID、fresh optimizer和fresh EMA。
- 正式数值唯一owner是[[ideas/StoryMotion/StoryMotion-valid-metric-ledger]]。

## 3. 当前实现

### 3.1 Stage1

- normalized Human199 + official Camera14，non-causal。
- Human128 `z_h`只读Human。
- interaction16 `z_hc`读取Human+Camera。
- conditioned camera48 `z_c`。
- Human decoder只读Human128；Camera／framing decoder读取完整192D latent。
- 当前parent是matched Pulp-only arm；同一ordered Pulp cohort分为：
  - `pulp_anchor`：Camera-free，只监督root/yaw/local；
  - `pulp_joint`：full Human199 + Camera14。

核心loss：

```text
L_H = SmoothL1(H_hat,H)
    + first-difference MSE
    + 0.001 * integrated-yaw loss
    + 0.003 * decoded-world-root loss

L_C = SmoothL1(C_hat,C)
    + first-difference MSE
    + 0.1  * framing loss
    + 1e-4 * interaction16 energy
```

阶段：

- A `210K`，anchor : joint=`4:1`，只优化Human；
- B `210K`，joint only，只优化Camera，Human冻结；
- C `216K`，anchor : joint=`3:7`；anchor算`L_H(root_local)`，joint算
  `L_H(full)+L_C`，Human LR为Camera LR的`0.1x`。

Stage1配置：FP32、BS128、AdamW、clip1、base LR `5e-5`，每阶段warmup1K后
cosine到`1e-6`。true-latent reconstruction Camera ADE/FDE约
`0.03765/0.04384 m`，rotation约`0.576°`，所以decoder没有collapse。

### 3.2 Cache

- train `162,760`，pure-test `4,053`；
- `[N,192,75] = Human128 + interaction16 + camera48`；
- Human128与Camera64分别用train-only z-score + branch内full-cov whitening；
- motion／Human text／Camera text ordered IDs一致；
- parent、cache、stats和owning decoder hashes已审计闭合。

### 3.3 Stage2

```text
u ~ Uniform(0,1)
sigma = 5u / (1 + 4u)
x_sigma = (1-sigma) * x_0 + sigma * epsilon
v_target = epsilon - x_0
```

loss是每sample按`valid latent frames × channels`归一化后的masked velocity
MSE。Camera Stage2没有decoded Camera-center、rotation、framing、projection、
outscreen或interaction16／camera48分量级loss。

- Direct-C：clean observed Human128，trust恒为1。
- HC：noisy GT Human经frozen teacher单次conditional forward得到stop-gradient
  predicted-clean Human，trust=`(1-sigma)^1`。
- HC训练Human context是CFG1的一步GT corruption；joint推理context来自CFG3的
  自由Euler trajectory。这是joint-specific exposure mismatch，不能解释使用GT
  Human的Direct-C失败。

完整loss／tag语义查
[[ideas/StoryMotion/StoryMotion-metric-computation-io#7. Current Stage1 / Stage2 training-objective I/O]]。

## 4. Camera curriculum、BS与optimizer

实际immutable run contract：

- Human与Camera micro/effective BS均为`128/128`，accumulation `1`；
- BF16，AdamW，betas `(0.9,0.95)`，weight decay `0.01`；
- clip `1.0`，EMA `0.9999`；
- base LR `2e-4`，warmup `2K`；
- Camera phase step`80K`／global`185000`降到`2e-5`。

每个Camera optimizer step只优化一个route：

1. global `105001–140000`：Direct-C only；
2. global `140001–175000`：HC only；
3. global `175001–210000`：odd Direct-C／even HC。

两路各`52.5K` steps、各`6.72M` exposures；共用Camera weights、AdamW state和
EMA。旧base template中的`micro32 × accumulation4`不是实际run配置。

## 5. 已确认异常与质量

### 5.1 遗忘与失稳

- `140K` fixed EMA：Direct-C `0.6840`，HC `1.0331`。
- `175K`：Direct-C `1.8622`，HC `0.8323`。HC-only改善HC并遗忘Direct-C。
- `185K`：Direct-C暂时恢复到`0.7371`，HC已反增至`0.8521`。
- `210K`：Direct-C `1.5046`，HC `1.1232`。final不是任一路最佳点。
- `183K` 1K window：grad median `1.516`、p90 `30.83`、max `1,200.5`，
  `62.4%`超过clip。
- `184K`：median `1.390`、p90 `20.68`、max `1,132.5`，`65.2%`超过clip。
- LR到global`185000`才降阶，晚于sharp onset。
- `185001–210000`全部25K steps pre-clip norm均大于1，median约247、
  p90约2,235、max约147,711；odd Direct-C median约793，even HC约91.9。
- 训练保持finite；clip防止NaN但没有恢复优化。final EMA中185K以前状态朴素
  残留约`8.2%`。

`loss/camera_train_C_H`在`140001–175000`没有点是该route未运行，不是TB漏写。
两route train tag各52,500点；fixed-EMA tag每次eval同时算。`train_log.jsonl`
每20 steps只命中alternating的even HC，是JSONL盲点。

完整时间线由
[[ideas/StoryMotion/2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis#7.1 根因一：三段 curriculum 的灾难性遗忘与 alternating 冲突]]
拥有。

### 5.2 Headline first-512

- v9 Direct-C：FDCLaTr `232.175`、CLaTr `36.430`、outscreen `0.5000`、
  ADE/FDE `2.625/2.911 m`、rotation `57.564°`。
- matched C3 Direct-C：FDCLaTr `34.077`、CLaTr `60.287`、outscreen
  `0.1514`、ADE/FDE `1.592/1.665 m`、rotation `32.635°`。
- v9 joint：FDCLaTr `181.666`、CLaTr `48.619`、outscreen `0.3157`、
  ADE/FDE `3.312/3.416 m`、rotation `69.886°`。
- fixed8 zero-visible frames：Direct-C约`46.96%`，joint约`3.84%`，GT为0。

Direct-C使用GT Human仍失败，不能把首因归为generated-H。完整正式字段只查
[[ideas/StoryMotion/StoryMotion-valid-metric-ledger]]。

## 6. 其他机制

Camera CFG：

```text
v = v00
  + s_t(v10-v00)
  + s_h(v01-v00)
  + s_r(v11-v10-v01+v00)
```

当前`(3,1,1)`等于`v11 + 2(v10-v00)`，放大“无Human时”的text方向；given-H
方向应更接近`v01 + 3(v11-v01)`，即`(3,1,3)`。两种方向实测cosine仅约
`0.109/0.218/0.256/0.297/0.292`。这是推理接口问题，但CFG不参与训练，不能
解释183K训练失稳。

Stage2 Camera64可能离开Human-conditioned joint manifold，且translation
velocity积分会放大latent偏差；但final latent heldout loss本身也已恶化，所以
geometry gap尚不能称为首因。

已排除为首因：小BS／exposure不足、BF16／NaN、Human污染、cache／text identity
错位、wrong decoder／EMA、causal tokenizer、Stage1 decoder collapse。

## 7. 远端 evidence

Host：`4090`。

```text
Story root:
/data/public/ripemangobox/Motion/StoryMotion

Stage1:
runs/train/stage1/stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726
checkpoint: checkpoints/step_636000.pt

Stage2:
runs/train/stage2/v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727

TensorBoard:
tensorboard/events.out.tfevents.1785155599.user-SYS-7049GP-TRT

Python:
/home/ripemangobox/miniconda3/envs/storymotion-vimogen-light-e6-20260726/bin/python
```

已有 Stage2 snapshots：

```text
step_021000.pt  step_042000.pt  step_063000.pt  step_084000.pt
step_105000.pt  teacher.pt      step_126000.pt  step_140000.pt
step_147000.pt  step_168000.pt  step_175000.pt  step_189000.pt
step_210000.pt  last.pt
```

> [!warning] Snapshot correction
> 没有`180K`、`182K`、`183K`、`185K`或`195K` checkpoint。附录方案中直接评估这些snapshot的步骤不可执行。精确failure replay如有必要，从immutable `175K`创建新diagnostic run，固定batch／noise／dropout重放，不得覆写原run。

已完成eval root：

```text
runs/eval/stage2/v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727
```

已有结果目录：

```text
human_teacher_105k_direct_h_n512_20260728
unified_210k_direct_h_n512_r2_20260728
unified_210k_direct_c_n512_20260728
unified_210k_joint_parallel_n512_r2_20260728
```

Vis root：

```text
runs/vis/stage2/v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727
```

## 8. 本地代码 owner

```text
linkedCodebases/StoryMotion/experiments/stage1_human_anchor_residual/model.py
linkedCodebases/StoryMotion/experiments/stage1_human_anchor_residual/train.py
linkedCodebases/StoryMotion/experiments/stage1_human_anchor_residual_pulp_only_r3/train.py
linkedCodebases/StoryMotion/experiments/stage2_backbone_upper_bound/e6_c3_vimogen_h/model.py
linkedCodebases/StoryMotion/experiments/stage2_protected_h_vimogen/model.py
linkedCodebases/StoryMotion/experiments/stage2_protected_h_vimogen/runner.py
linkedCodebases/StoryMotion/experiments/stage2_protected_h_vimogen/evaluate.py
linkedCodebases/StoryMotion/experiments/stage2_protected_h_vimogen/make_contract.py
```

关键函数：

- `HumanAnchorInteractionResidualAE.human_losses`／`losses`；
- `camera_mode_and_subphase`、`learning_rate`；
- `ProtectedDualStreamFlow.camera_flow_loss`／`_masked_flow_loss`；
- Camera CFG／joint sampling path；
- `runner.py` Camera loop的TB和clip逻辑。

## 9. 接力执行顺序

### P0：先评估现有 snapshots

为`140K`、`175K`、`189K`分别创建新eval contract和输出目录，以与final相同的
first-512 IDs、seed、Camera noise、Euler 50和owning decoder，各跑Direct-C与
joint，不覆盖既有结果。回答：

1. `140K`是否是更好的Direct-C endpoint；
2. `175K`是否呈现HC改善／Direct-C遗忘；
3. `189K`是否为两路折中；
4. decoded metric排序是否与fixed-EMA loss一致。

正式audit后，数字只写metric ledger一次。

### P1：inference-only screen

固定胜出snapshot、first-128和noise，比较：

1. `(1,1,1)`；
2. 当前`(3,1,1)`；
3. given-H `(3,1,3)`；
4. `(3,1,3)` + observed-H trust gamma `0.5/1/2`；
5. joint Human CFG `1 vs 3`。

不改训练权重；胜出臂才跑first-512。

### P2：failure replay

若P0支持“健康能力被尾段破坏”，从`175K`开新diagnostic run：

- 固定batch IDs、noise、sigma和dropout masks；
- 原optimizer state对照fresh moments；
- 记录两route grad norm／cosine、逐层norm、activation和update ratio；
- 定位optimizer moments、route conflict、condition scale或特定sigma／batch。

### P3：最小 clean balanced run

首个训练arm只改route aggregation：

```text
each Camera optimizer step:
  64 Direct-C -> L_direct
  64 HC       -> L_HC
  L_camera = 0.5 * L_direct + 0.5 * L_HC
  one clip -> one optimizer.step -> one EMA update
```

要求：

- 从Human `teacher.pt`边界开始；
- fresh AdamW、fresh EMA；
- effective BS仍128；105K steps总exposure仍13.44M、每路6.72M；
- 不改CFG，不加geometry／adapter／PCGrad；
- LR `5e-5`与`1e-4`各做10K screen；
- 每1K同时eval两route并保存snapshot；
- checkpoint按两route Pareto选，不默认final。

### P4：后续变量

1. 只有paired gradients持续负cosine才测试PCGrad／CAGrad或小adapter。
2. 只有balanced latent flow稳定但decoded geometry仍错位，才做
   interaction16／camera48 oracle、conditional-manifold和decoder sensitivity。
3. 归因成立后再逐项加入低权重Camera-center、rotation、framing auxiliary。
4. Joint exposure mismatch再单独测试teacher CFG匹配／rollout context。

## 10. Guard 与成功标准

候选screen guard，不是永久标准：

- rolling-1K pre-clip p90大于10或clip fraction大于50%连续两个window：停止并
  保存online／EMA／optimizer／batch／noise／sigma／dropout现场；
- 任意non-finite：立即停止；
- 两route fixed-EMA loss同时连续反增：停止；
- Human state和固定噪声输出必须exact `0.0`变化。

balanced run第一目标不是立刻超过C3，而是：

1. 不再出现35K route absence；
2. 两route在同一checkpoint进入健康区间；
3. 不出现持续全量clipping；
4. Direct-C与joint decoded Camera均优于v9 final；
5. Human完全不变。

## 11. 文档与工作区

- 当前决策：[[ideas/StoryMotion/current]]。
- 正式指标：[[ideas/StoryMotion/StoryMotion-valid-metric-ledger]]。
- loss／metric I/O：[[ideas/StoryMotion/StoryMotion-metric-computation-io]]。
- v9根因与修正：
  [[ideas/StoryMotion/2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]。
- SHA：[[ideas/StoryMotion/Storymotion-exp-sha]]。
- `Storymotion-exp-sha.md`、v9 diagnosis和本页受`obsidian-vault/*` ignore规则
  影响；普通`git status`看不到，不代表缺失。
- 工作区已有用户／其他agent修改；只做定向改动，不回退无关diff。

## 12. 外部方案边界

下面原文是候选方案池，尚未执行：

- same-step `64+64`与当前证据方向一致，但未实现；
- 文中若引用不存在的中间snapshot，必须改为从`175K`隔离replay；
- PCGrad、CAGrad、rollout context、geometry auxiliary、sigma重加权均未验证；
- hard-stop阈值、success threshold和auxiliary权重是候选超参，不是既有contract；
- 外部论文／PulpMotion书目信息未经本会话逐项联网核验；
- 不得跳过P0 snapshot eval和failure attribution。

## 附录：外部 Web GPT 候选方案原文（原样保留，未执行）

````latex
\title{\textbf{StoryMotion Camera / Joint 质量退化诊断与最小变量修正方案}}
\date{}

\begin{document}

\maketitle

\section{结论摘要}

基于当前训练时间线、固定 EMA held-out loss、梯度统计、Stage1 重建下限、正式 first-512 指标以及 fixed8 几何诊断，可以将当前问题分为四条相对独立的因果链：

\begin{enumerate}
\item \textbf{训练动力学问题：}
分段 curriculum 已经造成明确的跨 route 遗忘，随后在约 global step 183K 发生严重梯度失稳，最终 210K EMA 被失败尾段主导。

```
\item \textbf{条件接口问题：}
当前 Direct-C 和 Joint 共用的多条件 CFG 公式放大了 ``无 Human 条件下 Camera text 的边际方向''，并不等价于给定 Human 后的 Camera-text guidance。

\item \textbf{HC exposure mismatch：}
HC 训练只使用 noisy-GT 上的一步 predicted-clean Human，而 Joint 推理读取完整自由采样轨迹中的 predicted-clean Human。该 mismatch 确实存在，但只能解释 Joint 的额外问题，不能解释 Direct-C 失败。

\item \textbf{表示与几何目标问题：}
Stage2 仅优化 whitened Camera64 velocity MSE，而 Camera translation velocity 会被时间积分，latent 中不同方向对最终几何误差的敏感度高度不均匀。该问题是明确的 objective gap，但尚未被证明是当前最主要根因。
```

\end{enumerate}

因此，推荐优先级为：

[
\boxed{
\text{failure replay}
\rightarrow
\text{same-step balanced training}
\rightarrow
\text{given-H CFG}
\rightarrow
\text{rollout Human context}
\rightarrow
\text{conditional-manifold attribution}
\rightarrow
\text{geometry auxiliary}
\rightarrow
\text{PCGrad / adapter}
}
]

当前不得从失败的 210K optimizer state 继续训练，也不得同时修改 curriculum、LR、CFG、geometry loss 和模型结构。C3-25 seed17 仍应保留为生产 mainline。

\section{根因排序审查}

\subsection{证据等级总览}

\begin{table}[H]
\centering
\small
\caption{当前根因判断及其证据等级}
\begin{tabularx}{\textwidth}{L{1.0cm} Y L{2.2cm} Y}
\toprule
优先级 & 判断 & 证据强度 & 需要修正或限定的表述 \
\midrule
P0 &
约 183K 后 Camera 优化进入灾难性失稳区 &
已确认 &
这是已确认的训练现象，但具体触发机制仍未定位。 \
\addlinespace

P0 &
210K final checkpoint 与 final EMA 不是合理 endpoint &
已确认 &
不仅不是任一路的最佳点，而且 EMA 已被最后 25K 的失败更新主导。 \
\addlinespace

P0 &
分段 curriculum 造成跨 route 遗忘 &
因果基本确认 &
Direct-C-only 后 Direct-C loss 最优；HC-only 后 Direct-C fixed loss 明显恶化，时间对应关系充分。 \
\addlinespace

P1 &
当前 given-H CFG 方向不合理 &
机制证据很强 &
可解释推理退化，但不能解释 183K 的训练梯度爆炸，因为 CFG 不参与训练 loss。 \
\addlinespace

P1 &
共享 AdamW state 与 route-selection variance 可能促成失稳 &
待验证 &
不能在没有 route-specific gradient cosine 和 failure replay 的情况下直接称为 optimizer ping-pong 根因。 \
\addlinespace

P1 &
独立条件 dropout 导致四个 CFG 分支训练极不均衡 &
配置直接推出 &
当前推理公式高度依赖训练概率最低的 $v_{00}$，会额外放大估计误差。 \
\addlinespace

P1 &
HC 存在 Human-context exposure mismatch &
mismatch 已确认，影响量待验证 &
它只能解释 Joint 相对 Direct-C 的额外退化，不能解释 Direct-C 本身失败。 \
\addlinespace

P2 &
生成 Camera64 离开与 Human 匹配的 conditional manifold &
合理但未验证 &
Camera64 的边缘 Mahalanobis 距离不足，必须测 $p(C_{64}\mid H_{128})$ 或 joint manifold。 \
\addlinespace

P2 &
latent flow MSE 与 decoded geometry 不一致 &
目标缺口已确认，因果未确认 &
balanced training 稳定之前，不应将缺少 geometry loss 直接写成已确认根因。 \
\addlinespace

P2 &
当前 $\sigma$ 分布高噪占比过大，可能削弱低噪几何精修 &
合理机制，未验证 &
应先按 $\sigma$ 统计 loss、gradient 和 geometry error，而不是立即修改 flow path。 \
\bottomrule
\end{tabularx}
\end{table}

\subsection{最可靠的因果链}

当前最可靠的训练退化链条是：

[
\begin{aligned}
&\text{sequential route absence}
\
&\quad\rightarrow
\text{cross-route forgetting}
\
&\quad\rightarrow
\text{alternating recovery}
\
&\quad\rightarrow
\text{optimization instability near 183K}
\
&\quad\rightarrow
\text{persistent gradient clipping}
\
&\quad\rightarrow
\text{failed-tail-dominated EMA}
\
&\quad\rightarrow
\text{poor final checkpoint}.
\end{aligned}
]

其中以下事实已经得到直接支持：

\begin{itemize}
\item Direct-C-only 结束时，Direct-C fixed loss 达到约 $0.684$；
\item 经过 35K HC-only 后，Direct-C fixed loss 恶化至约 $1.862$；
\item 恢复 Direct-C 后，Direct-C loss 暂时恢复；
\item 约 183K 开始，pre-clip gradient norm 出现尖锐上升；
\item 185K 后几乎所有 step 都触发 gradient clipping；
\item 185K 后 Direct-C 和 HC fixed loss 同时恶化；
\item final 210K 并非任何一路的最佳 endpoint；
\item EMA decay 为 $0.9999$ 时，185K 以前参数在最终 EMA 中的朴素残留仅约
[
0.9999^{25000}\approx 8.2%.
]
\end{itemize}

因此，当前 P0 问题并不是 ``Camera 模型没有学会''，而是健康阶段取得的能力被后续 curriculum 和失稳训练破坏。

\subsection{梯度爆炸是现象，不是最终根因}

当 pre-clip norm 长期远大于 clip radius 时，更新近似变成一个被强制投影到单位球面的方向更新：

[
g_t^{\mathrm{clip}}
===================

g_t
\cdot
\min\left(
1,
\frac{c}{|g_t|}
\right),
]

其中 $c=1$。

当 $|g_t|\gg c$ 时：

[
g_t^{\mathrm{clip}}
\approx
c\frac{g_t}{|g_t|}.
]

因此不同 step 的梯度幅值信息几乎被完全抹除，训练主要由高噪声方向决定。对于 AdamW，实际更新还受到一阶、二阶矩估计影响：

[
\Delta\theta_t
==============

-\eta_t
\frac{\widehat m_t}
{\sqrt{\widehat v_t}+\epsilon}.
]

如果梯度分布已经发生数量级变化，历史 optimizer moments 会与当前梯度统计严重不匹配。此时只降低学习率，并不能自动将模型参数、激活分布和 optimizer state 恢复到健康区域。

所以，gradient clipping 在当前尾段只是阻止 NaN，并没有维持有效优化。

\subsection{缺少 decoded geometry loss 不是已确认首因}

Stage1 true-latent reconstruction 的 Camera ADE/FDE 和 rotation error 很低，说明以下结论成立：

\begin{itemize}
\item owning decoder 可以从真实 joint latent 解码出有效 Camera trajectory；
\item Camera decoder 并未发生结构性 collapse；
\item Stage2 最终出现的 $2$--$3$ m Camera error 不能主要归因于 decoder 无法重建有效 latent。
\end{itemize}

但是，这并不能证明 whitened latent velocity MSE 与最终几何误差一致。

设 Stage1 Camera decoder 为：

[
y=D_C(z_H,z_C),
]

其中：

[
z_C=[z_{hc},z_c]\in\mathbb R^{64}.
]

对生成 latent 偏差 $\delta z_C$，局部几何误差近似为：

[
\delta y
\approx
J_D(z_C)\delta z_C,
]

其中：

[
J_D(z_C)
========

\frac{\partial D_C}{\partial z_C}.
]

因此：

[
|\delta y|_2^2
\approx
\delta z_C^\top
J_D^\top J_D
\delta z_C.
]

Stage2 当前优化的是 whitening 空间中的欧氏 MSE，而不是 $J_D^\top J_D$ 加权的几何误差。不同 latent 方向可能具有完全不同的几何敏感度，尤其是 translation velocity 被时间积分后，会产生长期累积误差。

但由于当前 final checkpoint 的 latent fixed loss 本身已经显著恶化，尚无法区分：

[
\text{latent prediction 整体失败}
]

与

[
\text{latent metric 与 decoded geometry 错位}.
]

因此，geometry auxiliary 应作为稳定 balanced baseline 后的第二阶段改动，而不是首个修正。

\subsection{CFG 分支训练概率不均衡}

Camera text dropout 和 Human context dropout 均为 $0.1$，且独立采样，因此四种条件状态的训练概率为：

[
p_{00}
======

# 0.1\times0.1

0.01,
]

[
p_{10}
======

# 0.9\times0.1

0.09,
]

[
p_{01}
======

# 0.1\times0.9

0.09,
]

[
p_{11}
======

# 0.9\times0.9

0.81.
]

其中：

\begin{itemize}
\item $v_{00}$：Camera text 和 Human 都缺失；
\item $v_{10}$：仅 Camera text；
\item $v_{01}$：仅 Human；
\item $v_{11}$：Camera text 和 Human 都存在。
\end{itemize}

当前推理公式为：

[
v
=

v_{00}
+s_t(v_{10}-v_{00})
+s_h(v_{01}-v_{00})
+s_r(v_{11}-v_{10}-v_{01}+v_{00}),
]

取：

[
(s_t,s_h,s_r)=(3,1,1),
]

可化简为：

[
v_{\mathrm{current}}
====================

v_{11}+2(v_{10}-v_{00}).
]

这意味着推理严重依赖只占训练样本约 $1%$ 的 $v_{00}$，以及只占约 $9%$ 的 $v_{10}$。

而 $v_{10}-v_{00}$ 表示的是：

[
\text{没有 Human 条件时，Camera text 的边际方向}.
]

它不等价于给定 Human 后的 Camera-text 条件方向：

[
v_{11}-v_{01}.
]

实测两者 cosine 仅约为：

[
0.109,\ 0.218,\ 0.256,\ 0.297,\ 0.292,
]

说明两种方向在当前模型中并不近似等价。

\section{最小修改的 Camera curriculum}

\subsection{推荐目标}

第一版 clean run 应满足：

\begin{itemize}
\item 不修改 Stage1；
\item 不修改 Camera backbone；
\item 不修改 flow target；
\item 不添加 geometry auxiliary；
\item 不使用 PCGrad 或 CAGrad；
\item 不继承失败的 Camera optimizer state；
\item 每个 optimizer step 同时计算 Direct-C 和 HC；
\item 每步仅执行一次 gradient clipping、optimizer update 和 EMA update。
\end{itemize}

\subsection{同一步混合两个 route}

每个 optimizer step 采样：

[
|B_D|=64,
\qquad
|B_J|=64.
]

Direct-C loss：

[
L_D(\theta)
===========

\frac{1}{|B_D|}
\sum_{i\in B_D}
\ell_{\mathrm{flow}}^D(i).
]

HC loss：

[
L_J(\theta)
===========

\frac{1}{|B_J|}
\sum_{i\in B_J}
\ell_{\mathrm{flow}}^{HC}(i).
]

Camera 总损失：

[
\boxed{
L_{\mathrm{camera}}
===================

\frac{1}{2}L_D
+
\frac{1}{2}L_J
}
]

然后进行一次更新：

[
g
=

# \nabla_\theta L_{\mathrm{camera}}

\frac{1}{2}g_D
+
\frac{1}{2}g_J.
]

这样保持：

[
105000\times128
===============

13.44\text{M}
]

总样本 exposure 不变；每个 route 仍然获得：

[
105000\times64
==============

6.72\text{M}
]

样本 exposure。

\subsection{推荐伪代码}

\begin{lstlisting}[language=Python]
for camera_step in range(num_camera_steps):
optimizer.zero_grad(set_to_none=True)

```
# ---------------------------------------------------------
# Route 1: Direct-C, batch size = 64
# ---------------------------------------------------------
direct_batch = next(direct_loader)

direct_human_context = direct_batch.gt_human_latent.detach()

loss_direct = camera_flow_loss(
    camera_model=camera_model,
    camera_x0=direct_batch.camera_latent,
    camera_text=direct_batch.camera_text,
    human_context=direct_human_context,
    observed_human=True,
)

(0.5 * loss_direct).backward()

# ---------------------------------------------------------
# Route 2: HC / Joint-training context, batch size = 64
# ---------------------------------------------------------
hc_batch = next(hc_loader)

with torch.no_grad():
    hc_human_context = build_hc_predicted_clean_context(
        frozen_human_teacher,
        hc_batch,
    )

loss_hc = camera_flow_loss(
    camera_model=camera_model,
    camera_x0=hc_batch.camera_latent,
    camera_text=hc_batch.camera_text,
    human_context=hc_human_context.detach(),
    observed_human=False,
)

(0.5 * loss_hc).backward()

# One clip, one optimizer step, one EMA update
preclip_norm = torch.nn.utils.clip_grad_norm_(
    camera_model.parameters(),
    max_norm=1.0,
)

optimizer.step()
camera_ema.update(camera_model.parameters())
```

\end{lstlisting}

如果显存允许，也可以先分别通过 \texttt{torch.autograd.grad} 得到 $g_D$ 和 $g_J$，记录诊断后再合并；但第一版稳定训练不要求始终保存两套完整梯度。

\subsection{为什么同一步混合优于 odd/even alternating}

对于普通 SGD，如果每步随机选择 Direct-C 或 HC，梯度在期望上仍可能满足：

[
\mathbb E[g_t]
==============

\frac{1}{2}
\mathbb E[g_D]
+
\frac{1}{2}
\mathbb E[g_J].
]

但它具有额外 route-selection variance：

[
\operatorname{Var}(g_t)
=======================

\mathbb E[
\operatorname{Var}(g_t\mid r)
]
+
\operatorname{Var}(
\mathbb E[g_t\mid r]
).
]

同一步计算两个 route 的平均可以消除第二项中的大部分 route-selection variance。

对于 AdamW，问题更严重，因为：

[
m_t
===

\beta_1m_{t-1}
+
(1-\beta_1)g_t,
]

[
v_t
===

\beta_2v_{t-1}
+
(1-\beta_2)g_t^2.
]

当两个 route 的梯度尺度和方向不同，odd/even 交替会使一阶和二阶矩周期性追随不同分布。由于 $g_t^2$ 和除法操作是非线性的，交替更新并不等价于使用平均梯度更新。

因此，同一步混合是当前最小、最干净的多任务基线。

\section{多任务优化方法的使用顺序}

\subsection{第一阶段不使用 PCGrad}

第一版应直接使用：

[
g
=

\frac{1}{2}g_D+\frac{1}{2}g_J.
]

原因如下：

\begin{enumerate}
\item 当前尚未证明两个 route 持续发生负梯度冲突；
\item 梯度 norm 爆炸可能来自条件尺度、激活异常或 optimizer state，而不是任务冲突；
\item PCGrad 只处理内积为负的梯度分量，不会修复大 norm、异常 activation 或错误 CFG；
\item 直接加入 PCGrad 会使 failure attribution 变得困难。
\end{enumerate}

\subsection{必须记录 paired gradient cosine}

建议每 500 或 1000 step 使用一个专门的 paired diagnostic batch：

\begin{itemize}
\item 相同 sample ID；
\item 相同 Camera $x_0$；
\item 相同 $\epsilon$；
\item 相同 $\sigma$；
\item 相同 Camera text；
\item 唯一差别是 GT-H context 与 HC predicted-clean context。
\end{itemize}

分别计算：

[
g_D
===

\nabla_\theta L_D,
]

[
g_J
===

\nabla_\theta L_J.
]

记录 cosine：

[
c_g
===

\frac{
\langle g_D,g_J\rangle
}{
|g_D|_2|g_J|_2+\epsilon
}.
]

记录 norm ratio：

[
r_g
===

\frac{
|g_D|_2
}{
|g_J|_2+\epsilon
}.
]

还应按以下维度分解：

\begin{itemize}
\item Camera self-attention；
\item Camera-text cross-attention；
\item Human cross-attention；
\item FFN；
\item interaction16 输出头；
\item camera48 输出头；
\item 不同 $\sigma$ 区间。
\end{itemize}

\subsection{PCGrad 的启用条件}

只有同时满足以下条件时，才建议启用 PCGrad：

[
\operatorname{median}(c_g)<-0.1,
]

并且在连续至少 5 个统计窗口中：

[
\Pr(c_g<0)>60%.
]

同时还应满足：

\begin{itemize}
\item pre-clip gradient norm 处于健康区；
\item 没有持续 gradient clipping；
\item 两 route fixed loss 的竞争与负 cosine 时间一致；
\item 冲突集中在共享 Camera trunk，而不是仅发生在输出头。
\end{itemize}

PCGrad 的两任务形式为：

[
g_D'
====

## g_D

\frac{
\min(0,\langle g_D,g_J\rangle)
}{
|g_J|_2^2+\epsilon
}
g_J,
]

[
g_J'
====

## g_J

\frac{
\min(0,\langle g_J,g_D\rangle)
}{
|g_D|_2^2+\epsilon
}
g_D,
]

最后：

[
g_{\mathrm{PCGrad}}
===================

\frac{1}{2}
(g_D'+g_J').
]

\subsection{CAGrad、FAMO 与 adapter 的位置}

推荐顺序：

\begin{enumerate}
\item \textbf{PCGrad：}
在确认持续负梯度冲突后，作为最小投影方法。

```
\item \textbf{CAGrad：}
如果 PCGrad 导致某一路长期欠优化，考虑使用 conflict-averse objective，在平均性能与最差任务局部改善之间平衡。

\item \textbf{FAMO：}
如果 cosine 并不持续为负，但两个 route 的相对下降速度严重不平衡，可使用动态 task weighting。

\item \textbf{route-specific adapter：}
仅当稳定训练后仍证明 clean observed-H 与 generated-H context 需要不同映射时使用。
```

\end{enumerate}

不推荐两个 optimizer 同时更新同一组 Camera shared weights。两套 Adam moments 对同一参数分别更新，会产生更强的顺序依赖和不可解释性。

Separate optimizer 只适用于真正独立的 route adapter 参数；共享 trunk 必须只维护一个 optimizer state。

\section{学习率、scheduler、gradient clipping 与 EMA}

\subsection{推荐初始化}

Camera clean run 必须从 Human teacher 边界重新开始：

\begin{itemize}
\item 加载冻结的 Human teacher；
\item 初始化新的 Camera optimizer；
\item 初始化新的 Camera EMA；
\item 不加载 210K optimizer state；
\item 不加载失败 210K EMA 作为训练起点；
\item Camera online parameters 可以从 Camera 随机初始化或明确指定的健康初始状态开始，但不能从失败尾段继续。
\end{itemize}

\subsection{学习率 screen}

先进行两个完全相同的 10K-step screen：

[
\eta_{\max}
\in
\left{
5\times10^{-5},
1\times10^{-4}
\right}.
]

默认优先选择：

[
\boxed{
\eta_{\max}=5\times10^{-5}
}
]

只有在 $10^{-4}$ 同时满足以下条件时才选用：

\begin{itemize}
\item 两 route fixed loss 下降明显更快；
\item rolling gradient p90 与 $5\times10^{-5}$ 同量级；
\item clip fraction 不显著更高；
\item update norm 稳定；
\item 不出现 route-specific loss 反弹。
\end{itemize}

当前 $2\times10^{-4}$ 不应直接复用。

\subsection{Scheduler}

推荐：

\begin{itemize}
\item warmup：2K--5K steps；
\item 主体：smooth cosine decay；
\item 最终 LR：base LR 的约 $0.1$；
\item 不再使用 80K 时突然降低 10 倍的硬阶跃。
\end{itemize}

形式为：

[
\eta_t
======

\eta_{\min}
+
\frac{1}{2}
(\eta_{\max}-\eta_{\min})
\left[
1+
\cos
\left(
\pi\frac{t-t_w}{T-t_w}
\right)
\right],
]

其中：

[
\eta_{\min}
===========

0.1\eta_{\max}.
]

\subsection{Gradient clipping}

初始仍使用：

[
\texttt{max_grad_norm}=1.0.
]

但 clip 只能作为安全保险，不能作为稳定策略。需要同时记录：

\begin{itemize}
\item pre-clip total norm；
\item post-clip total norm；
\item clip fraction；
\item Direct-C route-specific norm；
\item HC route-specific norm；
\item update norm：
[
|\theta_{t+1}-\theta_t|*2;
]
\item update-to-weight ratio：
[
\frac{
|\theta*{t+1}-\theta_t|_2
}{
|\theta_t|_2+\epsilon
}.
]
\end{itemize}

不建议通过将 clip radius 从 1 降至 0.1 来掩盖失稳。若 norm 长期比 clip radius 高数百倍，进一步减小 clip 只会使更新更接近定长随机方向。

\subsection{EMA}

可继续使用：

[
\beta_{\mathrm{EMA}}=0.9999.
]

但推荐：

\begin{enumerate}
\item warmup 阶段同时评估 online weights；
\item warmup 结束后，将 EMA hard-copy 为当前 online weights；
\item 此后使用 $0.9999$；
\item 每 1K 保存 online 和 EMA snapshot；
\item checkpoint selection 不得默认选择最后一步。
\end{enumerate}

提高 EMA decay 不能修复训练失稳，只会延迟失败参数进入 EMA。

\section{given-H CFG 的修正}

\subsection{推荐统一公式}

Direct-C 和 Joint 的 Camera branch 在推理时都有 Human context：

\begin{itemize}
\item Direct-C：clean observed GT Human；
\item Joint：generated predicted-clean Human。
\end{itemize}

因此 Camera CFG 应围绕 ``给定 Human'' 定义：

[
\boxed{
v_{\mathrm{given-H}}
====================

v_{01}
+
s_t
(v_{11}-v_{01})
}
]

这等价于原始四项分解中的：

[
(s_t,s_h,s_r)=(s_t,1,s_t).
]

当：

[
s_t=3
]

时：

[
v_{\mathrm{given-H}}
====================

v_{01}
+
3(v_{11}-v_{01}).
]

也即：

[
(s_t,s_h,s_r)=(3,1,3).
]

\subsection{更一般的统一表达}

可将推理写成：

[
v
=

v_{00}
+
s_h(v_{01}-v_{00})
+
s_t(v_{11}-v_{01}).
]

其中：

\begin{itemize}
\item $s_h$ 控制是否使用 Human；
\item $s_t$ 控制在给定 Human 后增强 Camera text；
\item 正式 Direct-C 和 Joint 均可固定 $s_h=1$。
\end{itemize}

于是：

[
v
=

v_{01}
+
s_t(v_{11}-v_{01}).
]

\subsection{inference-only ablation}

固定：

\begin{itemize}
\item checkpoint；
\item first-512 cohort；
\item seed17；
\item initial noise；
\item Euler 50 steps；
\item decoder；
\item Human output；
\item Camera trajectory initialization。
\end{itemize}

比较：

\begin{enumerate}
\item 无 Camera CFG：
[
v=v_{11};
]

```
\item 当前公式：
\[
v=v_{11}+2(v_{10}-v_{00});
\]

\item given-H CFG：
\[
v=v_{01}+3(v_{11}-v_{01});
\]

\item given-H CFG scale sweep：
\[
s_t\in\{1,1.5,2,3\}.
\]
```

\end{enumerate}

不建议只比较 $s_t=1$ 和 $s_t=3$。Camera 几何任务可能在较低 guidance scale 已获得语义收益，而更高 scale 会放大 translation velocity 和 rotation error。

\subsection{是否继续使用 Human dropout}

如果 given-H CFG 明显优于当前公式，下一版训练可测试：

[
p_{\mathrm{drop\text{-}Human}}=0,
]

[
p_{\mathrm{drop\text{-}text}}=0.1.
]

原因是正式部署中不存在 Camera-without-H 模式，也不需要 $s_h>1$。

Human dropout 不是解决 HC exposure mismatch 的理想方式，因为：

[
\text{zero Human context}
\neq
\text{generated Human context with rollout error}.
]

\section{HC training/inference exposure mismatch}

\subsection{当前 mismatch}

HC 训练中：

[
H_\sigma
========

(1-\sigma)H_0+\sigma\epsilon_H,
]

冻结 Human teacher 预测：

[
v_H
===

f_H(H_\sigma,\sigma,T_H),
]

然后构造：

[
\widetilde H_0^{\mathrm{one\text{-}step}}
=========================================

H_\sigma-\sigma v_H.
]

但 Joint 推理时，Human state 是通过完整 Euler trajectory 从纯噪声逐步演化得到的：

[
H_{\sigma_K}
\rightarrow
H_{\sigma_{K-1}}
\rightarrow
\cdots
\rightarrow
H_{\sigma_0}.
]

因此 Camera 在推理时读取的 predicted-clean Human：

[
\widehat H_{0,k}^{\mathrm{roll}}
================================

## H_{\sigma_k}^{\mathrm{roll}}

\sigma_k
v_H(
H_{\sigma_k}^{\mathrm{roll}},
\sigma_k,
T_H
)
]

包含之前所有采样 step 的累积误差，而训练中的 one-step context 不包含这些历史误差。

此外：

\begin{itemize}
\item HC 训练中的 Human teacher 等价于 CFG scale 1；
\item Joint 推理中的 Human 使用 CFG scale 3。
\end{itemize}

\subsection{第一级修正：匹配 Human CFG}

训练 HC context 时使用与正式 Joint 推理一致的 Human CFG：

[
v_H^{\mathrm{cfg}}
==================

v_H^{\emptyset}
+
s_H
\left(
v_H^{\mathrm{cond}}
-------------------

v_H^{\emptyset}
\right),
]

其中：

[
s_H=3.
]

然后：

[
\widetilde H_0
==============

## H_\sigma

\sigma
v_H^{\mathrm{cfg}}.
]

该改动只匹配 guidance scale，仍未匹配 rollout history。

需要注意：推理 ablation 中，可以保持 Human 的真实采样轨迹始终使用 CFG=3，保证 Human 最终输出完全不变；只改变同一个 $H_\sigma$ 上提供给 Camera 的 predicted-clean estimate 使用 CFG=1 还是 CFG=3。这样可以隔离 Camera context interface，而不污染 Human 结果。

\subsection{第二级修正：离线 rollout-context cache}

因为 Human teacher 已经冻结，其 rollout distribution 不会随 Camera 训练变化，所以不需要在线 DAgger。可以离线生成 Human rollout context cache。

对训练样本和若干正式采样 timestep，缓存：

[
\left{
\sigma_k,
H_{\sigma_k}^{\mathrm{roll}},
\widehat H_{0,k}^{\mathrm{roll}}
\right}.
]

其中 rollout 使用：

\begin{itemize}
\item 正式 Euler 50 steps；
\item 正式 Human CFG=3；
\item 正式 Human text condition；
\item 冻结 Human teacher；
\item 与 Joint 推理一致的 predicted-clean 计算。
\end{itemize}

HC 训练时：

[
H_{\mathrm{ctx}}
================

\begin{cases}
\widehat H_0^{\mathrm{one\text{-}step}},
&
\text{probability }1-p_{\mathrm{roll}},
[4pt]
\widehat H_0^{\mathrm{roll}},
&
\text{probability }p_{\mathrm{roll}}.
\end{cases}
]

第一版使用：

[
p_{\mathrm{roll}}=0.25.
]

若有效，再测试：

[
p_{\mathrm{roll}}=0.5.
]

不建议第一版直接使用 $p_{\mathrm{roll}}=1$，因为：

\begin{itemize}
\item rollout cache 只覆盖有限 sampler 和 step；
\item 完全替换可能损害模型对局部扰动的平滑性；
\item one-step noisy-GT context 仍提供较干净的局部监督。
\end{itemize}

\subsection{第三级修正：数据驱动的 trust}

当前：

[
\operatorname{trust}(\sigma)
============================

(1-\sigma)^\gamma
]

只是启发式函数。

可以在 rollout cache 上统计：

[
e_H(\sigma)
===========

\mathbb E
\left[
\left|
\widehat H_0^{\mathrm{roll}}
----------------------------

H_0
\right|_2^2
\mid \sigma
\right].
]

再定义经验 trust：

[
q(\sigma)
=========

\frac{
1
}{
1+e_H(\sigma)/\tau
}.
]

或使用离散 bin 的 calibrated trust：

[
q_k
===

\operatorname{clip}
\left(
1-\frac{e_k}{e_{\max}},
0,
1
\right).
]

只有在 rollout context 已证明有效之后，才值得优化 trust。否则无法区分收益来自 context distribution 还是 trust schedule。

\section{表示层与几何归因}

\subsection{不能只测 Camera64 的边缘 manifold}

由于：

[
z_C=[z_{hc},z_c]
]

并不是 standalone Camera latent，而 Camera decoder 读取：

[
[z_h,z_{hc},z_c],
]

所以真正需要测的是 joint distribution：

[
p(z_h,z_C)
]

或 conditional distribution：

[
p(z_C\mid z_h).
]

单独计算：

[
d_C^2
=====

(z_C-\mu_C)^\top
\Sigma_C^{-1}
(z_C-\mu_C)
]

可能出现假阴性：某个 Camera64 在边缘分布上合理，但与当前 Human128 不匹配。

\subsection{conditional Mahalanobis}

在线性高斯近似下，训练集 joint latent 的统计量为：

[
\mu
===

\begin{bmatrix}
\mu_H\
\mu_C
\end{bmatrix},
\qquad
\Sigma
======

\begin{bmatrix}
\Sigma_{HH} & \Sigma_{HC}\
\Sigma_{CH} & \Sigma_{CC}
\end{bmatrix}.
]

给定 $H$，Camera 条件均值为：

[
\mu_{C\mid H}
=============

\mu_C
+
\Sigma_{CH}
\Sigma_{HH}^{-1}
(H-\mu_H).
]

条件协方差为：

[
\Sigma_{C\mid H}
================

## \Sigma_{CC}

\Sigma_{CH}
\Sigma_{HH}^{-1}
\Sigma_{HC}.
]

于是：

[
\boxed{
d_{\mathrm{cond}}^2
===================

(C-\mu_{C\mid H})^\top
\Sigma_{C\mid H}^{-1}
(C-\mu_{C\mid H})
}
]

应计算以下 sample-level 相关性：

[
\rho(
d_{\mathrm{cond}},
\mathrm{ADE}
),
]

[
\rho(
d_{\mathrm{cond}},
\mathrm{rotation\ error}
),
]

[
\rho(
d_{\mathrm{cond}},
\mathrm{outscreen}
).
]

也可使用 train kNN 距离或 learned density model 作为非线性补充。

\subsection{interaction16 与 camera48 的 oracle swap}

应进行：

\begin{enumerate}
\item GT interaction16 + generated camera48；
\item generated interaction16 + GT camera48；
\item GT Camera64 + generated Human128；
\item generated Camera64 + GT Human128；
\item matched Human + generated Camera64；
\item shuffled Human + same generated Camera64。
\end{enumerate}

但需要明确：将 GT interaction16 和 generated camera48 拼接后，组合 latent 未必位于真实联合 manifold。因此该实验只用于敏感性归因，不能单独证明某个子空间是唯一根因。

\subsection{decoder Jacobian 诊断}

对固定 Camera decoder，分别计算：

[
J_{hc}
======

\frac{
\partial y
}{
\partial z_{hc}
},
\qquad
J_c
===

\frac{
\partial y
}{
\partial z_c
}.
]

统计：

[
|J_{hc}|_F,
\qquad
|J_c|_F,
]

以及针对不同输出的 Jacobian：

[
J_{\mathrm{center}},
\quad
J_{\mathrm{rotation}},
\quad
J_{\mathrm{frame}}.
]

如果 interaction16 的 latent MSE 较小，但：

[
|J_{hc}|_F
\gg
|J_c|_F,
]

则 interaction16 的少量误差可能主导 framing 或相对构图错误。

更直接的 sample-level 近似为：

[
\delta y
\approx
J_{hc}\delta z_{hc}
+
J_c\delta z_c.
]

分别测：

[
|J_{hc}\delta z_{hc}|,
\qquad
|J_c\delta z_c|.
]

这比仅比较两个 latent block 的 MSE 更有解释力。

\section{是否添加 decoded geometry auxiliary}

\subsection{添加条件}

只有 balanced clean run 满足以下条件后才添加：

\begin{enumerate}
\item Direct-C 和 HC fixed latent loss 均稳定；
\item gradient norm 和 clip fraction 正常；
\item 不再存在明显跨 route 遗忘；
\item 低 latent loss checkpoint 与低 geometry error checkpoint 仍明显错位；
\item conditional manifold distance 或 decoder Jacobian 能解释 sample-level geometry error。
\end{enumerate}

\subsection{predicted-clean Camera latent}

当前 flow path：

[
x_\sigma^C
==========

(1-\sigma)x_0^C
+
\sigma\epsilon_C,
]

目标 velocity：

[
v^\star
=======

\epsilon_C-x_0^C.
]

模型预测：

[
v_\theta^C
==========

f_\theta(
x_\sigma^C,
\sigma,
T_C,
H_{\mathrm{ctx}}
).
]

predicted-clean Camera latent 为：

[
\widehat x_0^C
==============

## x_\sigma^C

\sigma v_\theta^C.
]

然后进行 inverse whitening：

[
\widehat z_C
============

W_C^{-1}
\widehat x_0^C
+
\mu_C.
]

将其与 Human context 送入固定 Stage1 owning decoder：

[
(\widehat C,\widehat F)
=======================

D_C(
z_H^{\mathrm{ctx}},
\widehat z_{hc},
\widehat z_c
).
]

\subsection{辅助损失}

总损失：

[
L_{\mathrm{total}}
==================

L_{\mathrm{flow}}
+
w_g(\sigma)
\left[
\lambda_pL_{\mathrm{center}}
+
\lambda_rL_{\mathrm{rot}}
+
\lambda_fL_{\mathrm{frame}}
\right].
]

Camera-center loss：

[
L_{\mathrm{center}}
===================

\operatorname{SmoothL1}
(
\widehat p_{1:T},
p_{1:T}
).
]

也可以将 ADE 和 FDE 分开：

[
L_{\mathrm{ADE}}
================

\frac{1}{T}
\sum_{t=1}^{T}
|
\widehat p_t-p_t
|_1,
]

[
L_{\mathrm{FDE}}
================

|
\widehat p_T-p_T
|_1.
]

Rotation geodesic loss：

[
L_{\mathrm{rot}}
================

\frac{1}{T}
\sum_{t=1}^{T}
\arccos
\left[
\operatorname{clip}
\left(
\frac{
\operatorname{tr}
(
\widehat R_t^\top R_t
)-1
}{2},
-1+\epsilon,
1-\epsilon
\right)
\right].
]

Framing loss：

[
L_{\mathrm{frame}}
==================

\operatorname{SmoothL1}
(
\widehat f_t,
f_t
),
]

其中 framing 可以包含：

[
f_t
===

\left[
x_t^{\mathrm{screen}},
y_t^{\mathrm{screen}},
\log(1+d_t^{\mathrm{bbox}}),
r_t^{\mathrm{out}}
\right].
]

不建议直接对 hard zero-visible indicator 反传，应使用连续的 projected joint visibility 或 soft margin。

\subsection{只在中低噪声使用 geometry auxiliary}

高噪声下：

[
\widehat x_0^C
==============

x_\sigma^C-\sigma v_\theta^C
]

误差可能很大，经 decoder 后会产生高方差、低信息量的几何梯度。

第一版使用：

[
w_g(\sigma)
===========

\mathbf 1[
0.1\leq\sigma\leq0.6
].
]

也可以使用平滑窗：

[
w_g(\sigma)
===========

\operatorname{sigmoid}
\left(
\frac{\sigma-0.1}{\tau}
\right)
\operatorname{sigmoid}
\left(
\frac{0.6-\sigma}{\tau}
\right).
]

\subsection{权重初始化}

不要直接复用 Stage1 loss 权重，因为 Stage1 latent 和 Stage2 flow 的梯度尺度不同。

推荐通过梯度比例初始化，使每项 auxiliary 对 Camera 参数的梯度满足：

[
\frac{
|
\lambda_i
\nabla_\theta L_i
|*2
}{
|
\nabla*\theta L_{\mathrm{flow}}
|_2
}
\approx 1%.
]

总 auxiliary gradient 初期不超过：

[
5%
]

的 flow gradient。

如果必须给出数值初始值，且所有几何量均按 train standard deviation 归一化，可以从：

[
\lambda_p=10^{-2},
]

[
\lambda_r=5\times10^{-3},
]

[
\lambda_f=10^{-2}
]

开始，并在前 5K step 线性 warmup：

[
\lambda_i(t)
============

\min
\left(
1,\frac{t}{5000}
\right)
\lambda_i^{\max}.
]

\subsection{梯度路径}

以下参数必须冻结：

\begin{itemize}
\item Stage1 Human encoder/decoder；
\item Stage1 Camera decoder；
\item Human Stage2 teacher；
\item Human context。
\end{itemize}

但是 Camera decoder forward 不能放入 \texttt{torch.no_grad()}，否则：

[
\frac{
\partial L_{\mathrm{geometry}}
}{
\partial \widehat z_C
}
]

无法传回 Camera Stage2。

正确形式为：

\begin{lstlisting}[language=Python]
for p in owning_camera_decoder.parameters():
p.requires_grad_(False)

human_context = human_context.detach()

decoded_camera = owning_camera_decoder(
human_context,
predicted_camera_latent,
)

geometry_loss = compute_geometry_loss(decoded_camera, gt_camera)
geometry_loss.backward()
\end{lstlisting}

\section{Flow noise schedule 的补充诊断}

当前：

[
u\sim\mathcal U(0,1),
]

[
\sigma
======

\frac{5u}{1+4u}.
]

其逆函数为：

[
u
=

\frac{\sigma}{5-4\sigma}.
]

因此 CDF 为：

[
F(\sigma)
=========

# \Pr(\Sigma\leq\sigma)

\frac{\sigma}{5-4\sigma}.
]

于是：

[
\Pr(\sigma>0.8)
===============

# 1-\frac{0.8}{5-3.2}

1-\frac{0.8}{1.8}
\approx55.6%,
]

[
\Pr(\sigma>0.9)
===============

# 1-\frac{0.9}{5-3.6}

1-\frac{0.9}{1.4}
\approx35.7%,
]

[
\Pr(\sigma<0.2)
===============

\frac{0.2}{5-0.8}
\approx4.8%.
]

因此训练样本明显偏向高噪声区域。

这可能对 Camera 特别不利，因为 Camera translation velocity 的小误差会被积分，而精确几何通常依赖低噪声阶段的细粒度修正。

但是 Human branch 使用相同 flow scheme 仍可稳定训练，因此该因素只能列为 P2。

在修改 schedule 之前，应按 $\sigma$ bin 统计：

\begin{itemize}
\item Direct-C fixed flow loss；
\item HC fixed flow loss；
\item route-specific gradient norm；
\item gradient cosine；
\item predicted-clean latent error；
\item decoded Camera-center error；
\item rotation error；
\item outscreen ratio。
\end{itemize}

只有当错误明确集中于低噪声区，才测试：

\begin{enumerate}
\item 当前 high-noise-biased schedule；
\item $\sigma\sim\mathcal U(0,1)$；
\item 当前 schedule 与 uniform 的 mixture；
\item 对低噪声区进行 loss reweight。
\end{enumerate}

该实验必须位于 balanced training 稳定之后。

\section{Ablation Matrix}

所有训练实验必须满足：

\begin{itemize}
\item 相同 Human teacher；
\item 相同 Camera initialization；
\item 相同 Stage1 checkpoint；
\item 相同 train/test ordered IDs；
\item 相同 whitening stats；
\item 相同 owning decoder；
\item fresh optimizer；
\item fresh EMA；
\item 相同 batch exposure；
\item 相同 first-512 cohort、seed、noise、sampler 和 decoder。
\end{itemize}

\begin{longtable}{L{0.8cm} L{3.2cm} L{2.0cm} L{4.1cm} L{4.1cm}}
\caption{推荐 ablation 顺序与 gate}
\label{tab:ablation}\
\toprule
ID &
唯一主要变量 &
运行范围 &
Continue gate &
Stop gate \
\midrule
\endfirsthead

\toprule
ID &
唯一主要变量 &
运行范围 &
Continue gate &
Stop gate \
\midrule
\endhead

\bottomrule
\endfoot

D0 &
对已有 140K、175K、180K、185K、189K、195K、210K snapshots 做统一推理 sweep &
无需训练 &
找到 v9 内部 Direct-C/HC Pareto checkpoint &
不得默认 final 210K 是代表性结果。 \
\addlinespace

D1 &
182K--183K failure replay：原 optimizer state 对比 fresh optimizer state &
1K--2K &
如果 fresh optimizer 消除 sharp onset，则 optimizer moments 被强烈指向 &
若相同 batch 在无参数更新 forward/backward 时也产生异常，则优先查数据、mask、condition 或数值路径。 \
\addlinespace

D2 &
paired Direct-C/HC gradient 诊断；按 layer、$\sigma$、condition state 分解 &
2K--5K &
定位冲突或 norm 异常主要来源 &
本实验不修改模型或 loss。 \
\addlinespace

T1 &
每步 64 Direct-C + 64 HC，LR $5\times10^{-5}$ &
10K &
两 route fixed loss 同时下降，clip fraction $<10%$ &
触发统一 hard-stop gate。 \
\addlinespace

T2 &
仅将 T1 的 LR 改为 $10^{-4}$ &
10K &
下降更快且稳定性不低于 T1 &
gradient p90、clip fraction 或 update ratio 显著恶化。 \
\addlinespace

T3 &
使用胜出 LR 完整训练 balanced curriculum &
105K &
同一 checkpoint 同时接近两个 route 的已知单路最优 &
任一路持续遗忘、两路同时反增或梯度失稳。 \
\addlinespace

I1 &
固定 T3 checkpoint，将当前 CFG 改为 given-H CFG &
first-512 &
Direct-C 几何和出屏改善，语义指标无明显回退 &
主要语义或几何指标明显恶化。 \
\addlinespace

I2 &
仅扫描 given-H text scale $s_t\in{1,1.5,2,3}$ &
first-512 &
得到语义与几何 Pareto 最优 scale &
不得同时修改 trust 或 Human CFG。 \
\addlinespace

C1 &
仅将 Human context dropout 从 0.1 改为 0 &
30K screen &
Direct-C/Joint given-H 推理稳定改善 &
HC 对生成 Human 误差的鲁棒性明显下降。 \
\addlinespace

E1 &
HC predicted-clean Human 的 teacher CFG 从 1 改为 3 &
30K screen &
Joint 改善，Direct-C 基本不变 &
两路同时恶化或 HC gradient 失稳。 \
\addlinespace

E2 &
加入 $p_{\mathrm{roll}}=0.25$ 的 rollout Human context &
30K screen &
Joint ADE、rotation 或 outscreen 改善，Direct-C 回退不超过 5% &
Joint 无改善、Direct-C 明显回退或训练失稳。 \
\addlinespace

E3 &
仅将 $p_{\mathrm{roll}}$ 从 0.25 改为 0.5 &
30K screen &
继续改善 Joint 且保持 Direct-C &
出现 sampler overfit 或 clean-H 能力下降。 \
\addlinespace

R1 &
计算 conditional manifold distance 与 geometry correlation &
无需训练 &
发现稳定、显著的 sample-level 相关性 &
若无相关性，不据此添加 manifold loss。 \
\addlinespace

R2 &
GT interaction16/generated camera48 与反向 oracle swap &
无需训练 &
定位主要敏感子空间 &
不得将 off-manifold 拼接结果直接视为因果证明。 \
\addlinespace

R3 &
decoder Jacobian 分解 interaction16 与 camera48 的几何敏感度 &
无需训练 &
解释 latent MSE 与 geometry error 的错位 &
若两部分均无高敏感方向，不优先修改表示。 \
\addlinespace

G1 &
加入低权重 Camera-center auxiliary &
30K screen &
ADE/FDE 改善，latent fixed loss 回退 $\leq5%$ &
clip fraction 或 gradient norm 明显恶化。 \
\addlinespace

G2 &
在 G1 基础上加入 rotation geodesic loss &
30K screen &
rotation 明显改善，其他指标稳定 &
Camera-center 或语义指标显著回退。 \
\addlinespace

G3 &
在 G2 基础上加入 differentiable framing loss &
30K screen &
outscreen、coverage 或 visible ratio 改善 &
梯度失稳或语义明显下降。 \
\addlinespace

M1 &
PCGrad &
仅在冲突 gate 触发后 &
两 route Pareto 同时改善 &
gradient cosine 原本不持续为负，或 PCGrad 导致某一路欠优化。 \
\addlinespace

M2 &
CAGrad &
仅在 PCGrad 无效后 &
改善最差 route 且保持平均目标 &
训练敏感度和超参数成本过高。 \
\addlinespace

A1 &
小型 observed/generated-H route adapter &
最后阶段 &
稳定 baseline 仍证明两类 Human context 需要不同映射 &
不得改写或污染 Human branch；若 shared trunk 已足够则取消。 \
\end{longtable}

\section{Continue / Stop Gate 与成功标准}

\subsection{统一 hard-stop gate}

任意满足以下条件时停止训练，并保存：

\begin{itemize}
\item online weights；
\item EMA weights；
\item optimizer state；
\item scheduler state；
\item batch IDs；
\item sampled $\sigma$；
\item noise seeds；
\item condition dropout masks；
\item route-specific losses；
\item pre/post clip norm；
\item relevant activations。
\end{itemize}

条件一：

[
\text{rolling-1K grad p90}>10.
]

条件二：

[
\text{rolling-1K clip fraction}>50%.
]

若任一条件连续两个窗口满足，则停止。

其他 hard stop：

\begin{itemize}
\item 出现任意 non-finite loss、gradient、parameter 或 EMA；
\item 单层 gradient norm 超过前 5K 健康中位数的 10 倍；
\item update-to-weight ratio 超过健康阶段中位数的 10 倍；
\item 任一路 fixed loss 连续两次 eval 高于其历史最优值 20%；
\item 两 route fixed loss 同时连续上升。
\end{itemize}

\subsection{balanced training 的 loss 成功标准}

已知单路最佳 fixed loss 为：

[
L_D^\star=0.684,
]

[
L_J^\star=0.832.
]

同一 checkpoint 的强成功标准定义为：

[
L_D
\leq
1.15L_D^\star
\approx
0.787,
]

[
L_J
\leq
1.15L_J^\star
\approx
0.957.
]

宽松 continue gate 为：

[
L_D
\leq
1.20L_D^\star
\approx
0.821,
]

[
L_J
\leq
1.20L_J^\star
\approx
0.998.
]

如果 balanced run 始终无法达到宽松 gate，但梯度稳定，则说明两个 route 可能存在真实容量或表征冲突，此时才进入多任务优化或 adapter。

\subsection{checkpoint 选择}

不得默认选择最后一步。应先根据 validation 上的：

[
(L_D,L_J)
]

选择 non-dominated checkpoints：

若不存在另一个 checkpoint $b$ 满足：

[
L_D(b)\leq L_D(a),
]

[
L_J(b)\leq L_J(a),
]

且至少一个严格小于，则 $a$ 属于 Pareto frontier。

只对 Pareto snapshots 评估：

\begin{itemize}
\item FDCLaTr；
\item CLaTr；
\item coverage；
\item segment F1；
\item outscreen；
\item r-FPD；
\item Camera ADE/FDE；
\item rotation error。
\end{itemize}

first-512 test 不能反复用于超参数选择。正式模型选择应使用独立 validation cohort，first-512 仅用于严格匹配的快速验证。

\subsection{CFG 修正的成功标准}

相对同一个 checkpoint 的当前 CFG，given-H CFG 应满足：

\begin{itemize}
\item Direct-C ADE/FDE 或 outscreen 至少相对改善 10%；
\item FDCLaTr、CLaTr 等语义指标回退不超过 3%；
\item Joint 主要指标回退不超过 5%；
\item Human 输出逐元素完全不变。
\end{itemize}

\subsection{exposure mismatch 修正的成功标准}

加入 Human CFG 匹配或 rollout context 后：

\begin{itemize}
\item Joint ADE、rotation 或 outscreen 至少改善 10%；
\item Direct-C 主要指标变化不超过 5%；
\item HC fixed loss 不显著恶化；
\item route-specific gradient norm 不发生系统性上升。
\end{itemize}

\subsection{geometry auxiliary 的成功标准}

添加 geometry auxiliary 后：

\begin{itemize}
\item ADE/FDE、rotation 或 outscreen 至少一个主要几何指标改善 10%；
\item latent fixed loss 回退不超过 5%；
\item clip fraction 增幅不超过 5 个百分点；
\item Camera semantic metrics 不因几何约束明显下降；
\item Direct-C 与 Joint 均无灾难性回退。
\end{itemize}

\section{生产 mainline 替换标准}

C3-25 seed17 继续作为生产 mainline。任何 v9 后续版本必须满足：

\begin{enumerate}
\item 在完整 pure-test 4053 样本上评估，而非只看 first-512；
\item 至少 3 个 Camera training seeds；
\item Direct-C 与 Joint Camera14 结果分开报告；
\item 使用 paired bootstrap 或置信区间；
\item Human 参数逐元素完全相同；
\item 固定噪声下 Human 输出逐元素完全相同；
\item Direct-H 正式指标完全不变；
\item Camera ADE/FDE、rotation、outscreen 不得相对 C3 显著退化；
\item 语义指标提升不能主要通过牺牲几何稳定性获得；
\item 同一个 unified checkpoint 同时满足 Direct-C、Joint 和 Direct-H；
\item 使用相同 cohort、seed、noise、sampler、decoder 和评估实现。
\end{enumerate}

由于 v9 与 C3-25 的 representation、backbone、objective 和 sampler 并非严格单变量一致，因此二者只能作为 matched-cohort system comparison，不能将差异归因于某一个模块。

\section{最终推荐执行顺序}

\subsection{阶段一：定位 183K sharp onset}

\begin{enumerate}
\item 对 182K--183K 做 deterministic failure replay；
\item 固定 batch IDs、noise、$\sigma$、dropout masks；
\item 比较原 optimizer state 与 fresh optimizer；
\item 记录 Direct-C/HC 分路梯度和逐层 norm；
\item 定位异常是否来自 observed-H route、特定 $\sigma$、特定条件分支或 optimizer moments。
\end{enumerate}

\subsection{阶段二：建立稳定的 balanced baseline}

\begin{enumerate}
\item 从 Human teacher 边界重新开始；
\item 每 step 使用 64 Direct-C + 64 HC；
\item 使用 fresh AdamW 和 fresh EMA；
\item screen $5\times10^{-5}$ 与 $10^{-4}$；
\item 只优化原始 Camera flow loss；
\item 每 1K 同时评估两 route；
\item 按 Pareto 选择 checkpoint。
\end{enumerate}

\subsection{阶段三：只修复推理条件接口}

\begin{enumerate}
\item 固定 balanced checkpoint；
\item 将当前 CFG 改为 given-H CFG；
\item 扫描 $s_t\in{1,1.5,2,3}$；
\item Direct-C 与 Joint 分开报告；
\item 不改变 Human trajectory。
\end{enumerate}

\subsection{阶段四：修复 HC exposure mismatch}

\begin{enumerate}
\item HC teacher predicted-clean 使用 Human CFG=3；
\item 若不足，再加入 $p_{\mathrm{roll}}=0.25$ 的 rollout context；
\item 若有效，再测试 $p_{\mathrm{roll}}=0.5$；
\item 最后才校准 trust。
\end{enumerate}

\subsection{阶段五：表示和 geometry attribution}

\begin{enumerate}
\item conditional Mahalanobis；
\item joint kNN distance；
\item interaction16/camera48 oracle swap；
\item decoder Jacobian；
\item latent distance 与 ADE、rotation、outscreen 的 sample-level correlation。
\end{enumerate}

\subsection{阶段六：添加低权重 geometry auxiliary}

只有在稳定 balanced baseline 仍表现出 latent/geometry 错位后，依次添加：

\begin{enumerate}
\item Camera-center loss；
\item rotation geodesic loss；
\item framing loss。
\end{enumerate}

每次只增加一个主要变量。

\subsection{阶段七：多任务优化与 adapter}

只有在 paired gradient 诊断确认持续负冲突后，依次尝试：

\begin{enumerate}
\item PCGrad；
\item CAGrad；
\item 动态 task weighting；
\item 小型 route-specific context adapter。
\end{enumerate}

\section{核心结论}

当前最优先的问题不是 Camera decoder、数据量、Human 污染或 Stage1 collapse，而是：

[
\boxed{
\text{不合理的 route curriculum}
+
\text{183K 后的优化失稳}
+
\text{失败尾段主导的 final EMA}
}
]

当前 CFG 是一个独立的高优先级推理问题：

[
\boxed{
v_{\mathrm{current}}
====================

v_{11}+2(v_{10}-v_{00})
}
]

应优先替换为：

[
\boxed{
v_{\mathrm{given-H}}
====================

v_{01}
+
s_t(v_{11}-v_{01})
}
]

HC exposure mismatch 是 Joint-specific 问题，应通过正式 Human CFG 和 rollout context 处理，而不能通过简单 Human dropout 代替。

decoded geometry auxiliary 有理论必要性，但只有在 balanced training 稳定后，才能判断它是必要修正还是对训练失败的掩盖。

因此最小、可验证且风险最低的执行路线为：

[
\boxed{
\begin{aligned}
&\text{fresh Camera run}
\
&+
\text{64 Direct-C + 64 HC per optimizer step}
\
&+
\text{LR screen at }5\times10^{-5}\text{ and }10^{-4}
\
&+
\text{strict gradient stop guard}
\
&+
\text{Pareto checkpoint selection}
\
&\rightarrow
\text{given-H CFG}
\
&\rightarrow
\text{rollout context}
\
&\rightarrow
\text{geometry auxiliary if proven necessary}.
\end{aligned}
}
]

\begin{thebibliography}{99}

\bibitem{flowmatching}
Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le.
\newblock Flow Matching for Generative Modeling.
\newblock \emph{International Conference on Learning Representations}, 2023.
\newblock \url{https://arxiv.org/abs/2210.02747}.

\bibitem{cfg}
Jonathan Ho and Tim Salimans.
\newblock Classifier-Free Diffusion Guidance.
\newblock \emph{NeurIPS Workshop on Deep Generative Models and Downstream Applications}, 2021.
\newblock \url{https://arxiv.org/abs/2207.12598}.

\bibitem{composable}
Nan Liu, Shuang Li, Yilun Du, Joshua B. Tenenbaum, and Antonio Torralba.
\newblock Compositional Visual Generation with Composable Diffusion Models.
\newblock \emph{European Conference on Computer Vision}, 2022.
\newblock \url{https://arxiv.org/abs/2206.01714}.

\bibitem{pcgrad}
Tianhe Yu, Saurabh Kumar, Abhishek Gupta, Sergey Levine, Karol Hausman, and Chelsea Finn.
\newblock Gradient Surgery for Multi-Task Learning.
\newblock \emph{Advances in Neural Information Processing Systems}, 2020.
\newblock \url{https://arxiv.org/abs/2001.06782}.

\bibitem{cagrad}
Bo Liu, Xingchao Liu, Xiaojie Jin, Peter Stone, and Qiang Liu.
\newblock Conflict-Averse Gradient Descent for Multi-Task Learning.
\newblock \emph{Advances in Neural Information Processing Systems}, 2021.
\newblock \url{https://arxiv.org/abs/2110.14048}.

\bibitem{famo}
Bo Liu, Xingchao Liu, Xiaojie Jin, Peter Stone, and Qiang Liu.
\newblock FAMO: Fast Adaptive Multitask Optimization.
\newblock \emph{Advances in Neural Information Processing Systems}, 2023.
\newblock \url{https://arxiv.org/abs/2306.03792}.

\bibitem{scheduledsampling}
Samy Bengio, Oriol Vinyals, Navdeep Jaitly, and Noam Shazeer.
\newblock Scheduled Sampling for Sequence Prediction with Recurrent Neural Networks.
\newblock \emph{Advances in Neural Information Processing Systems}, 2015.
\newblock \url{https://arxiv.org/abs/1506.03099}.

\bibitem{dagger}
Stephane Ross, Geoffrey Gordon, and Drew Bagnell.
\newblock A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning.
\newblock \emph{International Conference on Artificial Intelligence and Statistics}, 2011.
\newblock \url{https://proceedings.mlr.press/v15/ross11a.html}.

\bibitem{pulpmotion}
Pulp Motion authors.
\newblock Pulp Motion: Human--Camera Joint Motion Generation.
\newblock arXiv preprint, 2025.
\newblock \url{https://arxiv.org/abs/2510.05097}.

\end{thebibliography}

\end{document}
````
