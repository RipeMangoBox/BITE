---
title: "StoryMotion v7 Stage2 架构设计"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - architecture
  - status/active
aliases:
  - StoryMotion-v7-stage2
hypothesis: |
  v7 不重训 Stage1，不借机切换 Rectified Flow，也不推倒 CondMDI UNet 主干。v7 的核心是基于现有 Stage2 做最小必要结构改造：保留 JOINT / H2C / C2H 三任务统一接口，但把 hard observed injection 改成 source encoder + trust gate，把 human text / camera text 做任务主辅分流，并加入 relation token、task embedding 和可选 task-text CLIP latent 插件。
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
created: 2026-07-01T23:08:48+0800
updated: 2026-07-01T23:24:14+0800
---
# StoryMotion v7 Stage2 架构设计

## 0. 设计裁决

本轮和 DeepSeek Max 做了两轮严肃对照。DS 的有效意见是：不要现在换 Rectified Flow，不要大换 backbone；当前失败源更像 condition injection / source reliability / task routing，而不是扩散范式或 UNet 容量不足。DS 第一轮误把 H2C 文本主次说反、把噪声训练重点放到 text 上；第二轮已修正为：H2C 的主文本是 camera text，核心噪声训练对象是 observed human source。

我的最终裁决：

```text
v7 = fixed Pulp official Stage1 + minimally modified CondMDI UNet Stage2
```

不做：

- 不重训或替换 Pulp official Stage1 tokenizer / cache。
- 不把 diffusion 换成 Rectified Flow。
- 不把 CondMDI UNet 主干推倒重写成 DiT / Transformer。
- 不把 `H2C` 和 `C2H` 当成严格对称任务。

必须做：

- 去掉 observed branch hard inject。
- 显式区分 `human text` 和 `camera text` 的任务主辅角色。
- 引入 `task_id` embedding / router。
- 引入 source metadata 与 trust gate。
- 加入 screen-framing relation token。
- 用 clean / noisy / generated replay / text intervention 四类 eval 同时判定。

## 1. 输入契约

v7 的文本输入：

```text
e_c: camera text embedding, 512 dims
e_h: human text embedding, 512 dims
e = concat([e_c, e_h]), 1024 dims
```

所有任务都读取同一个 1024 维 text embedding，但 Stage2 内部按任务解释主辅关系。

| task | motion source | dominant text | auxiliary text | output | interpretation |
| --- | --- | --- | --- | --- | --- |
| `JOINT` | none | `e_h` and `e_c` both strong | none | `H_hat, C_hat` | 双文本联合生成，human text 控制动作，camera text 控制镜头 |
| `H2C` | `H_source` | `e_c` | `e_h` | `C_hat` | camera text 是目标语义；human source 是结构条件；human text 只补动作上下文 |
| `C2H` | `C_source` | `e_h` | `e_c` | `H_hat` | human text 是动作语义；camera source/text 提供 framing/view constraint |

关键纠偏：`H2C` 不能只用 human text。v6.4 的 camera text shuffle/zero 几乎不影响 clean output，正说明 camera text 主通路没有建立起来。

## 2. 是否需要新 architecture

结论：**需要 Stage2 局部结构改造，不需要新主干 architecture。**

当前 CondMDI-style UNet 的主问题不是时序建模能力，而是把 observed source 当 clean truth hard inject：

```python
x = where(obs_mask, obs_x0, x_t)
```

这会让 `H2C` 直接走 `H_gt/root -> C` shortcut，进而压掉 `e_c` 和 relation control。v7 应保留 UNet denoiser 主干，但改条件注入路径：

```text
noisy target latent
  + task embedding
  + text main/aux cross-attention
  + source encoder tokens
  + trust gate
  + relation token
  -> UNet
  -> task-specific output head / adapter
```

### 2.1 最小必要模块

| module | must-have | reason |
| --- | --- | --- |
| `TaskEmbedding` | yes | 区分 `JOINT / H2C / C2H`，避免三任务退化成 mask pattern |
| `TextRoleRouter` | yes | 按任务设置 `e_h / e_c` 的主辅角色 |
| `SourceEncoder` | yes | 把 observed motion 从 hard replacement 改为 condition token |
| `ReliabilityEncoder` | yes | 编码 `gt/noisy/generated/missing` 和 noise metadata |
| `TrustGate` | yes | 控制模型读取 source 的强度，避免 noisy source 直接污染 target |
| `RelationToken` | yes | 显式承载 screen framing / human-camera relation |
| separated head/adapter | recommended | 减少 human/camera 输出互相污染；可先用 adapter，不必重写 UNet |
| task-text CLIP latent | optional | MotionLab-style 插件，默认关闭，只做 ablation |

### 2.2 不建议现在做的新 architecture

| proposal | verdict | reason |
| --- | --- | --- |
| 全新 DiT / Transformer Stage2 | no | 会把变量扩大到 backbone、训练长度、schedule；不直接回答 v6.4 failure |
| 三个完全独立模型 | no for v7 | 可作为 kill criteria 后备，但会丢 unified framework 卖点 |
| 重训 Stage1 tokenizer | no | 当前训练不出更好的 tokenizer，污染 Stage2 结论 |
| Rectified Flow | no | 不解决 hard inject / text shortcut / source reliability，且需重写 sampler 和 loss |

## 3. 是否换 Rectified Flow

结论：**不换。**

理由：

1. v6.4 已证明 clean capacity 存在：`H_gt -> C` clean `FDCLaTr 15.00 / F1 0.629` 接近旧 clean 水平。
2. failure 是 `H_source` 变脏时 camera collapse，以及 `e_c` 被 shortcut 掩盖；RF 不会自动修复条件通路。
3. RF 会引入新变量：flow matching target、ODE sampler、NFE、loss scaling、CFG 适配。
4. 当前 6 卡资源更适合跑 condition injection / reliability ablation，而不是同时换生成范式。

RF 只能作为未来 v8 或 speed ablation：

```text
条件：v7 已经解决 noisy/generated source 和 text sensitivity。
目的：验证 RF 是否减少 sampling steps 或提升 low-NFE quality。
```

## 4. Stage2 路由设计

### 4.1 TextRoleRouter

每个任务显式定义主文本和辅助文本：

```text
H2C:
  main_text = e_c
  aux_text = e_h

C2H:
  main_text = e_h
  aux_text = e_c

JOINT:
  main_text_h = e_h
  main_text_c = e_c
```

建议实现：

```text
main_text_tokens -> normal cross-attention
aux_text_tokens  -> low-weight cross-attention or relation-token update
```

如果 `H2C` 的 camera text shuffle/zero 仍几乎无影响，说明 TextRoleRouter 失败；需要增大 main camera text path 的注入强度，或降低 source residual gate。

### 4.2 SourceEncoder + TrustGate

替代 hard inject：

```text
source latent -> SourceEncoder -> source tokens
source metadata -> ReliabilityEncoder -> q
source tokens + q -> TrustGate -> gated source tokens
```

`source metadata`：

```text
source_type: gt / noisy_gt / generated / missing
sigma: injected or estimated latent noise
root_drift: estimated root displacement error
mask_ratio: observed density
source_confidence: optional scalar
```

`H2C` 中：

```text
pred_z_c = CameraGlobal(e_c, task=H2C)
         + trust_gate(q) * CameraResidual(H_source, R, e_h)
```

`C2H` 中：

```text
pred_z_h = HumanPrior(e_h, task=C2H)
         + weak_gate(q) * HumanViewResidual(C_source, R, e_c)
```

### 4.3 RelationToken

`R` 不改 Stage1。第一版用可计算 surrogate：

```text
R_t = [
  projected human bbox center,
  projected bbox scale,
  visible joint ratio,
  relative camera-human distance,
  view direction / facing summary
]
```

如果 Pulp `W` row-space 可以直接复用，则把 Pulp framing latent 作为附加 `R` token。否则先使用 projection surrogate，避免卡在 Stage1。

## 5. 三任务流程

### 5.1 `H2C`: human-to-camera

```text
input:
  e_c dominant
  e_h auxiliary
  H_source
  source metadata

flow:
  H_source -> HSourceEncoder -> h_tokens
  metadata -> ReliabilityEncoder -> q
  h_tokens, q -> TrustGate -> h_trusted
  e_c -> CameraGlobalHead
  h_trusted, e_h, R -> CameraResidualHead
  output C_hat
```

目标：

- 保持 clean H2C 能力。
- 显著改善 noisy/generated human source。
- 让 camera text shuffle/zero 明显影响 output。

### 5.2 `C2H`: camera-to-human

```text
input:
  e_h dominant
  e_c auxiliary
  C_source
  source metadata

flow:
  e_h -> HumanPriorHead
  C_source, e_c -> weak view/framing residual
  output H_hat
```

原则：

- `C2H` 是弱约束 actor blocking，不是 `H2C` 镜像。
- human text 不能被 camera source 压掉。
- `C2H` loss 权重低于 `H2C`，以免破坏 human prior 和 H2C。

### 5.3 `JOINT`: text-to-human-camera

双文本：

```text
input:
  e_h
  e_c
  no source

flow:
  e_h -> HumanHead -> z_h^0
  e_h, e_c, z_h^0 -> RelationToken -> R^0
  e_c -> CameraGlobalHead -> z_c_global
  z_h^0, R^0, q=generated -> CameraResidualHead -> z_c_residual
  optional low-noise joint refine on R and z_c
```

`JOINT` 仍然是 unified Stage2 的任务之一，但采样顺序承认 human action/root/timing 对 camera framing 更强。

## 6. Phase 是什么

这里的 `phase` 指 **training schedule 阶段**，不是论文贡献阶段，也不是模型模块阶段。

建议使用 3 个训练 phase，其中 Phase 3 可选：

| phase | required | name | target |
| --- | --- | --- | --- |
| Phase 0 | yes | fixed Stage1 / eval sanity | 确认 Pulp official cache、sampler、official callback、v6.4 baseline 可复现 |
| Phase 1 | yes | clean multi-task training | 学 clean source 下的三任务基础能力和 text role routing |
| Phase 2 | yes | source reliability finetune | 对 `H_source/C_source` 做 noisy/generated/missing 训练，修 source collapse |
| Phase 3 | optional | text sensitivity finetune | 若 Phase 2 后 camera text 仍无效，再做 text dropout / wrong-text 对抗 |

Phase 2 的噪声对象是 motion source，不是 text：

```text
H2C:
  corrupt H_source, keep e_c/e_h intact

C2H:
  corrupt C_source, keep e_h/e_c intact

JOINT:
  no source; optional simulated generated source only for low-noise refine
```

建议 source corruption 先沿用现有可比网格：

```text
sigma in {0.0, 0.05, 0.10, 0.15, 0.30}
missing_prob in {0.0, 0.1}
generated_replay: from external human prior or fixed replay cache
```

不建议一开始用 DS 第一轮提到的 `std 0.2-1.0` 大噪声，因为它可能直接把 source 变成 out-of-distribution，无法和 v6.4/P2a 对齐。

## 7. 新设计与当前 StoryMotion Stage2 的点对点区别

| aspect | current Stage2 | v7 Stage2 | priority | verification |
| --- | --- | --- | --- | --- |
| input text | 1024 concat text，但任务主辅不显式 | 明确 `e_c/e_h`，按任务设 dominant/auxiliary | high | H2C camera text shuffle/zero 必须有影响 |
| task definition | `TASK_CAMERA/TASK_HUMAN/TASK_JOINT` as mask patterns | `H2C/C2H/JOINT` as asymmetric routes | high | mode-specific eval + no-task-embedding ablation |
| observed source | `where(obs_mask, obs_x0, x_t)` hard inject | `SourceEncoder + TrustGate` soft conditioning | highest | noisy source `FDCLaTr/F1` |
| source quality | P2b metadata exists but not enough | metadata drives trust gate and source tokens | highest | correct/wrong source tag ablation |
| text conditioning | camera text can be shortcuted by GT human | dominant text path per task | highest | H2C text shuffle/zero |
| relation modeling | implicit in concat latent | explicit `R` token from projection/Pulp relation | high | OutRate, SRE, visible joint ratio |
| output heads | largely shared denoising output | shared UNet + task adapters or separated heads | medium | head ablation; check task interference |
| backbone | CondMDI-style UNet | same UNet main trunk | fixed | compare against current under same sampler |
| diffusion type | DDPM/DDIM-style diffusion | keep diffusion | fixed | RF deferred |
| Stage1 | Pulp official cache / tokenizer | same fixed contract | fixed | Stage1 sanity only |
| training schedule | mixed branch-mask + P2b corruption | clean multi-task -> source reliability finetune -> optional text sensitivity | high | phase-wise checkpoint eval |
| data processing | GT source / noisy source partially supported | add generated replay cache and source metadata table | high | generated replay eval must use external human prior/cache |
| eval | clean often over-emphasized | report clean/noisy/generated/text-intervention together | highest | every checkpoint has four-way report |
| task CLIP latent | absent | optional plugin, default off | low | only if mode conflict persists |

## 8. 高优先级实验表：6 卡计划

资源假设：4090/5090 共 6 卡可用。主线实验尽量串行依赖，副线 ablation 并行填满空卡。所有实验使用 Pulp official Stage1 cache，先不动 RF。

### 8.1 必跑主线

| id | card | experiment | change tested | train phase | expected output | pass / kill criterion |
| --- | --- | --- | --- | --- | --- | --- |
| E0 | 1 | v6.4 baseline replay | no change；复现 clean/noise/text failure | Phase 0 | baseline report | clean 接近 `15.00/0.629`；noise/text failure 可复现 |
| E1 | 1 | remove hard inject + task/text router | `SourceEncoder + TrustGate` skeleton；`e_c/e_h` 主辅分流；no relation token | Phase 1 | clean + text-intervention report | clean F1 不低于 v6.4 20%；H2C text shuffle/zero 开始影响输出 |
| E2 | 1 | E1 + source reliability finetune | corrupt `H_source/C_source`，train trust gate | Phase 2 | clean/noisy/generated/text report | noise `0.15` FDCLaTr 明显低于 v6.4 `530.27`；优先目标回到旧 P2a 量级 |
| E3 | 1 | E2 + relation token | add projection/Pulp relation token and relation loss | Phase 1+2 | relation + official metrics | OutRate/SRE 改善，且 H2C clean/noisy 不退化 |

主线决策：

- 如果 E2 已显著解决 noisy source 和 camera text sensitivity，E3 可降为 relation ablation。
- 如果 E2 仍 noise `0.15` > 200，优先检查 TrustGate 是否被绕过，而不是换 RF。
- 如果 E1 clean 直接崩，说明去 hard inject 后条件形式不够，需要先修 SourceEncoder / denoising target，而不是进入 E2。

### 8.2 并行 ablation

| id | suggested card | experiment | purpose | dependency | priority |
| --- | --- | --- | --- | --- | --- |
| A1 | 2 | source noise grid | compare sigma sets `{0.05,0.10,0.15,0.30}` vs stronger corruption | E1 checkpoint | high |
| A2 | 3 | trust gate ablation | correct source tag vs wrong tag vs no tag | E2 design | high |
| A3 | 4 | separated heads/adapters | shared head vs task-specific adapters | E1 or E2 | medium |
| A4 | 5 | no task embedding negative control | test mode conflict without task identity | E1 code | medium |
| A5 | 6 | task-text CLIP latent plugin | MotionLab-style task instruction, default-off ablation | after E2 or E3 | low-to-medium |
| A6 | spare / after E2 | Phase 3 text sensitivity finetune | only if camera text still weak | E2 checkpoint | conditional |

### 8.3 每个实验必须输出的统一表

每个 checkpoint 都要有同一张四路评估表：

| eval split | condition | required metrics |
| --- | --- | --- |
| clean oracle | clean GT source | FDCLaTr / CLaTr / F1 / OutRate |
| noisy source | sigma `0.05/0.10/0.15/0.30` | FDCLaTr / F1 degradation curve |
| generated replay | external human prior or replay cache | FDCLaTr / F1 / OutRate |
| text intervention | shuffle/zero/wrong dominant text | CLaTr / FDCLaTr / SRE / diversity |

## 9. Kill criteria

v7 需要用硬 gate 防止“看起来改了很多但核心症状没变”。

| condition | interpretation | action |
| --- | --- | --- |
| E2 noise `0.15` FDCLaTr 仍 > 200 | trust gate / source reliability 没解决主问题 | 不进入 RF；先查 hard shortcut 是否仍存在 |
| H2C clean F1 低于 v6.4 20% 以上 | 去 hard inject 后 clean capacity 丢失 | 修 SourceEncoder / target prediction，不继续加 relation |
| camera text shuffle/zero 仍近似无影响 | dominant camera text path 失败 | 增强 `e_c` cross-attn，降低 source residual gate |
| generated replay 无法构造干净 | eval contract 不成立 | 先做外部 human prior / replay cache，不写 generated claim |
| C2H 加入后 H2C 明显退化 | weak task 负迁移 | 降低 C2H 权重或拆 adapter/head |

如果 E1-E3 全部失败，优先考虑的后备方案不是 RF，而是：

```text
shared Stage2 trunk + stronger task-specific adapters/heads
or
temporarily split H2C/C2H/JOINT specialists for diagnosis
```

## 10. 最终 v7 表述

```text
StoryMotion v7 keeps a unified three-task Stage2 interface over human text and camera text,
but replaces symmetric branch-mask hard injection with asymmetric text-role routing,
source-aware trust gates, and explicit screen-relation tokens on top of the existing CondMDI UNet.
```

这版方案的优先级很清楚：先证明在不换 Stage1、不换 RF、不重写 backbone 的情况下，能否同时扭转三联症状：

```text
clean pass
noise/generated source fail
camera text weak
```

只有这组三联症状被扭转，v7 才能作为 StoryMotion 的 Stage2 主线。
