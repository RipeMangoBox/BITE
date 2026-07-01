---
title: "StoryMotion 三模式统一架构简报：给网页端 LLM"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - architecture
  - experiment
  - status/active
aliases:
  - StoryMotion-LLM-Brief
hypothesis: |
  StoryMotion 的核心卖点应是一个模型统一支持三种 human-camera 生成模式：joint story-to-human-camera、human-to-camera completion、camera-to-human completion。当前关键问题不是是否要三模式统一，而是现有实现把三模式当成 CondMDI 式对称随机 mask 来混训，默认 observed branch 永远 clean 且 human/camera 可互换补全；这与 StoryMotion 中 human action/root/timing -> camera framing/response 的非对称依赖冲突。阶段性证据显示：clean GT-human camera completion 可行，但 noisy/generated human condition 会让 camera collapse；因此 v6.4 之后要保留统一三模式目标，同时改造三模式的路由、权重、source reliability 和 relation control，而不是放弃统一或继续盲目对称 mask。
created: 2026-07-01T22:10:00+0800
updated: 2026-07-01T22:16:10+0800
---
# StoryMotion 三模式统一架构简报：给网页端 LLM


## 0. 希望网页端 LLM 做什么

你是一个研究型 motion generation / diffusion architecture 顾问。请帮助诊断和设计 **StoryMotion**：一个面向 story-driven human-camera motion generation 的**三模式统一生成系统**。

请重点回答：

1. StoryMotion 的三模式统一卖点应如何保留，而不是退化成单一 camera completion？
2. 当前三模式对称训练的具体架构问题在哪里？
3. 为什么 CondMDI 式对称随机 mask 不适合直接套到 human-camera 三模式训练？
4. 如何把 human branch、camera branch、screen framing relation 和 observed branch reliability 重新设计成“统一但非对称”的框架？
5. 下一批最小实验应该怎么设计，才能验证架构改动是否真正解决 coupling，而不是只改善 clean oracle completion？

请避免泛泛建议。所有建议都应对应到本文列出的失败现象、公开相关工作或可验证实验 gate。

---

## 1. StoryMotion 想实现什么

StoryMotion 的核心卖点不是“从 story text 生成一段 human-camera motion”这么宽泛；更准确地说，它想做的是 **one model, three human-camera generation modes**。

目标任务：

```text
输入：
  story / text description
  optional observed human motion
  optional observed camera motion

输出：
  时间对齐的 human motion + camera motion

要求：
  1. human 动作符合故事语义
  2. camera motion 能合理取景、跟随、构图
  3. human 和 camera 在屏幕空间中协调，不出画、不乱 framing
  4. 同一个模型支持 joint / camera completion / human completion 三种模式
  5. 当 observed 条件来自 generated/noisy source，而不是 GT clean source 时仍可靠
```

三模式定义：

```text
Mode A: JOINT story generation
  input:
    story text only
  output:
    H_hat, C_hat
  desired behavior:
    同时生成 human action/root/timing 与 camera framing/movement。

Mode B: CAMERA completion / camera planning
  input:
    story text + observed/generated human motion H_obs
  output:
    C_hat
  desired behavior:
    根据 human motion 生成能跟随、构图、表达镜头意图的 camera。

Mode C: HUMAN completion / actor blocking
  input:
    story text + observed/generated camera motion C_obs
  output:
    H_hat
  desired behavior:
    在给定镜头或镜头意图下生成与画面协调的人体动作。
```

因此，StoryMotion 的研究价值在于：

```text
同一个 Stage2 policy 能在三种 mode 间切换，
并且 human-camera relation 在 joint / completion 场景中保持一致。
```

关键困难：**三模式不是语义对称的**。真实推理时 camera 往往不会拿到完美 GT human motion。更真实的 joint pipeline 可能是：

```text
text_human -> human prior -> H_hat
text_camera + H_hat -> camera generator -> C_hat
```

也就是说，camera branch 看到的 human condition 通常是 generated human，可能带有 root drift、latent noise、动作语义偏差。反过来，camera-to-human completion 也不是同等级约束：camera 更像 view/framing constraint，不能像 human action/root/timing 那样提供完整动作先验。

所以，只证明 `GT human -> camera` 的 clean completion 很强，并不能证明 StoryMotion 已经解决三模式统一生成。当前要解决的不是“要不要统一三模式”，而是：

```text
如何保留三模式统一接口，
同时承认 human -> camera 与 camera -> human 的条件信息量、可靠性、因果方向都不同。
```

---

## 2. 当前核心架构

StoryMotion 当前是两阶段系统。

### 2.1 Stage1：motion autoencoder / latent tokenizer

Stage1 把原始 human 与 camera motion feature 压成 latent，再由 decoder 还原到 official metric 所需的运动空间。

概念上：

```text
human raw feature H_raw  -> encoder -> z_human
camera raw feature C_raw -> encoder -> z_camera
latent = concat([z_human, z_camera])
decoder(latent) -> reconstructed human/camera motion
```

当前参考上界来自 **Pulp Motion** 的 official Stage1 autoencoder。Pulp Motion 是最直接相关工作：

- Paper: [Pulp Motion: Framing-aware multimodal camera and human motion generation](https://arxiv.org/abs/2510.05097)
- Code: [https://github.com/robincourant/pulp-motion](https://github.com/robincourant/pulp-motion)

Pulp Motion 的重要思想：human-camera joint generation 不是简单拼接两个 latent，而是引入 screen-space framing latent。它学习一个线性映射 `W`，把 human-camera latent 映射到 screen framing relation，并在采样时用这个 relation subspace 做 auxiliary guidance。

这对 StoryMotion 的启发：

- camera generation 的核心不是 raw trajectory regression，而是 screen framing relation。
- human-camera 应有显式 relation / framing control 面。
- Stage1 的好坏不能只看 reconstruction loss，必须看 decoded motion 进入 official TMR/CLaTr/projection metric 后是否仍强。

### 2.2 Stage2：branch-mask diffusion generator

Stage2 在 latent space 上训练一个 diffusion model。当前主干接近 CondMDI-style observed-mask diffusion，但对象从单人体 motion keyframe mask 变成 human/camera 分支 mask。

当前三种任务正是 StoryMotion 的卖点来源：

```text
TASK_CAMERA:
  observed branch = z_human
  target branch   = z_camera
  用 human condition 补全 camera

TASK_HUMAN:
  observed branch = z_camera
  target branch   = z_human
  用 camera condition 补全 human

TASK_JOINT:
  observed branch = none
  target branch   = z_human + z_camera
  从 text 同时生成 human 和 camera
```

当前关键输入逻辑类似：

```python
x = where(obs_mask, obs_x0, x_t)
model_input = concat(x, obs_mask, text_embedding, timestep)
loss = MSE(pred_x0, target_x0) only on target branch
```

文本 embedding 约定：

```text
text_embedding dim = 1024
first 512 dims  = camera text
last 512 dims   = human text
```

当前训练想用同一个 diffusion generator 覆盖三种 mode，这是合理目标。但现有实现把三种 mode 组织成类似 CondMDI 的**对称 observed-mask training**：

```text
sample one mode
choose one branch as observed
hard inject observed branch
predict the other branch or both branches
treat CAMERA/HUMAN/JOINT as mask pattern variants
```

这会带来一个关键错误假设：

```text
human branch and camera branch are interchangeable missing parts
```

但 StoryMotion 的真实结构更接近：

```text
human action/root/timing  ->  camera framing/following/shot response
camera path/framing       ->  weak or partial human constraint
story text                ->  shared semantic prior
screen relation           ->  coordination contract
```

因此，当前问题不是“三模式统一生成”这个卖点错了，而是**用对称随机 mask 实现三模式统一**错了。

---

## 3. 为什么不能直接套 CondMDI 随机 mask

CondMDI 是优秀的 motion in-betweening 工作：

- Paper: [Flexible Motion In-betweening with Diffusion Models](https://arxiv.org/abs/2405.11126)
- Code: [https://github.com/setarehc/diffusion-motion-inbetweening](https://github.com/setarehc/diffusion-motion-inbetweening)

CondMDI 的场景是：同一个 human motion 序列中，随机 keyframes / joints 被观测，模型补全缺失部分。它的前提是：

```text
同一模态内的局部观测 -> 补全同一模态
```

StoryMotion 的场景不同：

```text
human action/root/timing -> camera framing/residual
```

human 与 camera 是两个语义不同的分支：

- human branch 是动作主体和 root/timing source。
- camera branch 是视角、构图、跟随和 screen framing response。
- camera 依赖 human 是合理的，但 camera 不应该盲信任何 human source。
- human branch 不应被 camera branch 的噪声反向污染。

所以 StoryMotion 的 mask 不是 CondMDI 里的“同质局部 mask”，而是“异质语义分支 mask”。更具体地说，三模式对称训练会制造四个问题：

1. **条件方向被错当成对称**

   `TASK_CAMERA: H -> C` 与 `TASK_HUMAN: C -> H` 不是互逆任务。human motion 含 action/root/timing，camera 更像 framing/view response；camera condition 对 human 的约束更弱、更歧义。

2. **observed source 被错当成 clean truth**

   hard injection 让模型默认 observed branch 总是 GT clean。但三模式真实推理中，observed branch 可能来自上游 generated human、用户粗糙输入、noisy latent 或 missing condition。

3. **JOINT 与 completion 被错当成同分布**

   `TASK_JOINT` 没有 observed branch，需要从 text 建立 human-camera relation；completion task 有 observed branch，容易走 shortcut。把它们同权混训会让模型在 joint 中学不到稳定 relation，在 completion 中过度依赖 observed branch。

4. **text control 被 observed shortcut 掩盖**

   在 `TASK_CAMERA` 中，GT human/root 已经强到可以预测大部分 camera，模型可能忽略 camera text。v6.4 的 camera text shuffle/zero 结果已经支持这个诊断。

这意味着：

```text
StoryMotion should remain a unified three-mode model,
but the three modes need asymmetric routing, asymmetric losses,
source tags, reliability control, and explicit relation modeling.
```

而不是：

```text
CAMERA / HUMAN / JOINT = symmetric random masks over concat([H, C])
```

---

## 4. 当前具体问题：三模式对称训练如何导致 coupling

当前失败可以概括为一条因果链：

```text
三模式统一目标
  -> 采用 CondMDI-style 对称随机 branch mask
  -> TASK_CAMERA / TASK_HUMAN / TASK_JOINT 被当作同一类 mask completion
  -> observed branch hard-injected as clean x0
  -> 模型学会依赖 observed human/root shortcut
  -> camera text 与 relation control 被削弱
  -> clean GT-human camera completion 仍强
  -> noisy/generated-human condition 下 camera collapse
```

更具体地拆开：

| component | current symmetric assumption | why it fails for StoryMotion |
| --- | --- | --- |
| `TASK_CAMERA` | human observed, predict camera; equivalent to another mask pattern | H -> C 是强方向，模型容易把 H 当 clean oracle，忽略 camera text 和 source reliability |
| `TASK_HUMAN` | camera observed, predict human; symmetric counterpart of `TASK_CAMERA` | C -> H 信息量弱且多解，不能和 H -> C 同权、同结构、同 loss 处理 |
| `TASK_JOINT` | no observed branch, predict both; just another mask ratio | joint 需要从 text 建立 human-camera relation，不能依赖 completion shortcut |
| observed injection | observed branch is ground-truth x0 | generated/noisy observed source 会把错误直接传入 target branch |
| concat denoising | H/C are channels of one latent tensor | human root/action 与 camera framing 的语义角色不同，raw concat 容易产生错误串扰 |

因此，当前要问网页端 LLM 的不是“如何把 StoryMotion 改成 camera specialist”，而是：

```text
如何设计一个统一三模式接口，
但内部使用非对称 mode routing：
  JOINT: text -> H,C with relation prior
  CAMERA: H_source-aware + camera_text + relation -> C
  HUMAN: C_as_weak_constraint + human_text + relation -> H
```

后续 v6.4 的 camera specialist 只是诊断用切片：它验证 `H_gt -> C` clean 能力与 noise robustness 问题，不代表最终系统要放弃三模式统一。

---

## 5. 已经完成的尝试与阶段性结论

### 5.1 Stage1 official upper bound 很强

Pulp official Stage1 autoencoder 的 decoded reconstruction 很强，可作为目标上界：

| Stage1 ckpt | split | samples | human FDTMR↓ | human TMR↑ | human coverage↑ | camera FDCLaTr↓ | camera CLaTr↑ | camera coverage↑ | camera F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pulp official AE | mixed | 10549 | 124.46 | 18.17 | 85.4% | 15.51 | 58.10 | 87.2% | 0.670 | 4.6% |
| Pulp official AE | pure | 4053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% |

结论：如果 Stage1 复现达到这个量级，Stage2 的失败才可以更干净地归因到 generator / architecture。

### 5.2 本地 Stage1 复现未通过 official gate

本地尝试复现 Pulp official Stage1 AE，但 posthoc official eval 明显弱于 official ckpt：

| Stage1 ckpt | split | samples | human FDTMR↓ | human TMR↑ | human coverage↑ | camera FDCLaTr↓ | camera CLaTr↑ | camera coverage↑ | camera F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reproduced AE latest | mixed | 10549 | 423.10 | 8.74 | 34.1% | 76.97 | 35.86 | 68.2% | 0.373 | 28.6% |
| reproduced AE latest | pure | 4053 | 438.99 | 7.88 | 41.4% | 99.98 | 38.27 | 67.1% | 0.453 | 23.3% |

阶段结论：

- 本地 Stage1 复现还没达到 official Pulp AE contract。
- 不能把 Stage1 training loss 或 feature MSE 当作成功。
- 不能基于 reproduced Stage1 继续做 Stage2 正结论。
- 需要优先检查 config、normalization、checkpoint selection、EMA/best epoch、data split、metric loading 是否与 official Pulp 完全一致。

### 5.3 多个自训练 tokenizer / Stage2 组合都失败

已经尝试过：

- separate AE no-z
- separate VAE with-z
- joint VAE with-z
- joint GRFSQ with-z
- MoLingo-style human-only adaptation
- v6.3 camera-only / completion-only / joint-only mode conflict split

主要观察：

- 有些 Stage1 feature reconstruction loss 很低，但 Stage2 official metrics 仍崩。
- self-trained joint VAE source tokenizer 上，即使拆成 camera-only、completion-only、joint-only，clean official eval 仍崩。
- v6.3 mode-conflict 四个 run 都训练到 step `50000`，但 first-wave clean official eval 已经失败：

| v6.3 run | task | samples | human FDTMR↓ | camera FDCLaTr↓ | camera CLaTr↑ | camera F1↑ | Out↓ | conclusion |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| camera-only, camera-text only | camera | 10549 | - | 957.83 | 3.13 | 0.060 | - | collapse |
| camera-only, full text | camera | 10549 | - | 957.45 | 3.10 | 0.060 | - | collapse |
| completion-only | camera | 10549 | - | 955.99 | 3.18 | 0.060 | - | collapse |
| joint-only | joint | 10549 | 2228.68 | 967.49 | 3.31 | 0.063 | 100.0% | collapse |

阶段结论：

- 这组失败不能证明非对称架构无效，因为它被 self-trained Stage1 latent contract failure 主导。
- 它只能证明：在当前 self-trained joint VAE latent 上，拆任务不能自动救 Stage2 transfer。

### 5.4 使用 Pulp official Stage1 cache 时，clean camera completion 可以强

在 Pulp official Stage1 cache 上，旧 StoryMotion v6 clean camera completion 曾达到：

```text
clean GT-human camera completion:
  camera FDCLaTr = 14.50
  camera F1      = 0.638
```

这很重要，因为它说明：

- Stage2 模型容量不一定是最大瓶颈。
- official metric bridge 不一定有问题。
- 当 observed human 是 GT clean human，camera completion 能做到很强。

但这只是 oracle setting。

### 5.5 旧 P2a noise test 显示 camera 对 human noise 极敏感

在旧 P2a matched noise protocol 中，给 observed human/root latent 加噪后，camera 迅速退化：

| observed human/root noise std | camera FDCLaTr↓ | camera CLaTr↑ | camera coverage↑ | camera F1↑ |
| ---: | ---: | ---: | ---: | ---: |
| 0.00 | 14.50 | 54.85 | 87.1% | 0.638 |
| 0.05 | 22.02 | 53.15 | 85.6% | 0.625 |
| 0.10 | 51.89 | 48.66 | 80.2% | 0.573 |
| 0.15 | 96.87 | 43.54 | 70.1% | 0.503 |
| 0.30 | 216.79 | 32.96 | 46.7% | 0.360 |
| 0.50 | 303.00 | 25.68 | 31.0% | 0.278 |

阶段结论：camera branch 在 GT human 下强，但对 noisy/generated human condition 不鲁棒。这是 Stage2 coupling / reliability 的核心证据。

### 5.6 v6.4 GPU1：非对称 camera specialist 的 clean/noise 结果

v6.4 GPU1 是一个更明确的非对称诊断实验。注意：它不是最终 StoryMotion 形态，也不是放弃三模式统一；它的目的只是隔离 `TASK_CAMERA`，判断在 verified Stage1 latent 上 clean completion 与 noise robustness 分别怎样。

```text
task distribution:
  TASK_CAMERA = 1.0
  TASK_HUMAN  = 0.0
  TASK_JOINT  = 0.0

input:
  observed human latent H
  camera text
target:
  camera latent C

training:
  Pulp official Stage1 cache
  camera-only specialist
  P2b reliability augmentation enabled
```

Official eval:

| eval | observed human condition | camera text intervention | camera FDCLaTr↓ | camera CLaTr↑ | camera coverage↑ | camera F1↑ | conclusion |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| clean camera | GT human latent | none | 15.00 | 54.87 | 84.9% | 0.629 | clean passes |
| noise 0.15 | noisy human latent | none | 530.27 | 9.46 | 4.0% | 0.103 | robustness fails |
| noise 0.30 | noisy human latent | none | 493.82 | 10.24 | 6.0% | 0.110 | robustness fails |
| text shuffle | GT human latent | camera text shuffled | 15.63 | 53.89 | 84.5% | 0.618 | camera text weak |
| text zero | GT human latent | camera text zeroed | 14.16 | 53.29 | 84.0% | 0.609 | camera text weak |

阶段结论：

- v6.4 camera-only specialist 可以保持 clean camera completion。
- 但它没有解决 noisy/generated human condition reliability。
- camera text 控制力弱，模型大概率仍主要依赖 observed human/root shortcut。
- 因此，非对称方向是合理的，但“只做 camera-only + P2b augmentation”不够。

---

## 6. Clean / noise 实验到底代表什么

### 6.1 Clean 是什么

`clean camera` 是 oracle camera completion：

```text
condition = H_gt  # GT human latent, no generation error
target    = C_gt  # GT camera latent
model     = camera_specialist(camera_text, H_gt) -> C_hat
```

它测试：

1. camera specialist 是否有基本生成能力；
2. Pulp official Stage1 cache 是否能支撑 high-quality camera decode；
3. sampler 和 official metric bridge 是否正常；
4. 非对称 camera-only training 是否会破坏 clean camera quality。

v6.4 clean 通过，说明模型不是完全没能力生成 camera。

### 6.2 Noise 是什么

`noise 0.15 / 0.30` 是把 observed human latent 加入 matched latent noise：

```text
condition = H_noisy = H_gt + sigma * matched_latent_noise
target    = C_gt
model     = camera_specialist(camera_text, H_noisy) -> C_hat
```

它不是测试 camera diffusion noise，而是测试 **camera 对 human condition 质量的鲁棒性**。

为什么必要：

- 真实 joint inference 中 camera 看到的是 human prior 生成的 `H_hat`，不是 `H_gt`。
- `H_hat` 会有 root drift、latent noise、动作偏差。
- 如果 camera branch 只会在 `H_gt` 下工作，一旦 `H` 稍微变脏就崩，那它只是 oracle completion 模型，不是 robust StoryMotion。

### 6.3 clean pass + noise fail 如何定位 coupling

v6.4 的组合结果是：

```text
clean pass
noise fail
camera text weak
```

这给出清晰诊断：

```text
camera generation capacity exists
official Stage1 cache / sampler / metric bridge are basically fine
but model has learned to over-trust observed human/root latent
and has not learned robust source-aware conditioning or camera-text-driven framing
```

所以当前 architecture coupling 不是“camera 不能依赖 human”，而是：

```text
camera should depend on human,
but dependence must be source-aware, trust-gated, relation-mediated,
not hard-clamped and not blind.
```

---

## 7. 当前最可能的根因

### 7.1 hard observed injection

当前 Stage2 把 observed branch hard-replace 到 input：

```python
x = where(obs_mask, obs_x0, x_t)
```

这会让模型学习到：

```text
observed human is always clean truth
```

一旦推理时 observed human 是 noisy/generated，camera branch 就会跟着错误 root / latent drift 崩。

### 7.2 root-relative camera contract

Pulp-style camera latent 可能包含 human-root-relative camera quantities。若 camera decode 依赖 human root，那么 human root 的误差会直接变成 world camera 误差。

需要拆分：

```text
camera = text-driven global camera prior + human-conditioned framing/root residual
```

而不是让所有 camera latent 都 raw depend on human latent。

### 7.3 camera text 被 observed human shortcut 掩盖

v6.4 中 camera text shuffle / zero 几乎不破坏 clean output，说明模型主要靠 GT human/root shortcut 完成 camera completion。

这对真实 story-driven generation 不够，因为 camera text 描述了 shot type、framing intention、movement style，例如 follow shot、close-up、orbit、pan、tilt、dolly。若 camera text 不控制 output，StoryMotion 只是 human-conditioned camera interpolator。

### 7.4 raw concat + shared denoise 造成错误串扰

human 与 camera latent 被 concat 后交给共享 TemporalObsUNet。joint 模式中二者通过共享通道双向影响；completion 模式中 observed branch hard injection 又让 target branch 盲信 observed branch。

更合理的是：

```text
human stream: learns action/root/timing prior
camera stream: reads human through controlled cross-branch interface
relation stream: encodes screen framing / character-camera geometry
```

---

## 8. 公开相关工作证据链

### 8.1 Pulp Motion：screen framing relation 是核心控制面

Pulp Motion:

- Paper: [https://arxiv.org/abs/2510.05097](https://arxiv.org/abs/2510.05097)
- Code: [https://github.com/robincourant/pulp-motion](https://github.com/robincourant/pulp-motion)

关键证据：

- human-camera joint generation 需要 screen-space framing relation。
- auxiliary sampling 使用 learned linear map `W` 和 row-space projection 引导构图。
- 公开结果显示 auxiliary guidance 可降低 framing FID 和 out-of-screen rate。

对 StoryMotion：

- 增加 relation token / `W` row-space guidance。
- 在 camera branch 显式建模 screen framing，而不是只预测 raw camera latent。

### 8.2 Towards Storytelling Animations：human/camera 应作为实体交互建模

Towards Storytelling Animations:

- Paper: [CVPR 2026 openaccess](https://openaccess.thecvf.com/content/CVPR2026/html/Cheng_Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions_CVPR_2026_paper.html)

关键证据：

- 把 character 与 camera 作为独立实体。
- 显式建模 character-camera pairwise interaction。
- 消融显示交互模块对 human/camera motion quality 和 coordination 重要。

对 StoryMotion：

- 不要只 raw concat latent。
- 应设计 branch-specific stream + relation / pairwise adapter。

### 8.3 CondMDI：mask training 有用，但不能照搬

CondMDI:

- Paper: [https://arxiv.org/abs/2405.11126](https://arxiv.org/abs/2405.11126)
- Code: [https://github.com/setarehc/diffusion-motion-inbetweening](https://github.com/setarehc/diffusion-motion-inbetweening)

关键证据：

- 在单人体 motion 中，训练时随机 keyframe / joint mask 可让模型学会灵活 in-betweening。

对 StoryMotion：

- 可以保留 mask + observed branch idea。
- 但 human/camera 是异质语义分支，不能当作对称 random mask。

### 8.4 MotionLab：统一多任务需要 task instruction 与 curriculum

MotionLab:

- Paper/project: [https://diouo.github.io/motionlab.github.io/](https://diouo.github.io/motionlab.github.io/)
- Code: [https://github.com/Diouo/MotionLab](https://github.com/Diouo/MotionLab)

关键证据：

- Motion-Condition-Motion 统一范式。
- task instruction modulation。
- motion curriculum learning。
- 消融显示去掉 curriculum 会造成多任务训练严重退化。

对 StoryMotion：

- 不要把 camera/human/joint 三模式同权随机混训。
- 应有 task/source instruction：`gt_human`、`noisy_human`、`generated_human`、`missing_human`。
- 训练顺序应从 human prior、camera specialist 到 relation refinement。

### 8.5 PriorMDM / MDM：强 prior + 轻量协调优于从零 share-all

PriorMDM:

- Paper/project: [https://priormdm.github.io/priorMDM-page/](https://priormdm.github.io/priorMDM-page/)
- Code: [https://github.com/priorMDM/priorMDM](https://github.com/priorMDM/priorMDM)

MDM:

- Code: [https://github.com/GuyTevet/motion-diffusion-model](https://github.com/GuyTevet/motion-diffusion-model)

关键证据：

- 冻结或轻微微调的 motion diffusion prior 可通过 handshake、communication block、model blending 组合出更复杂能力。

对 StoryMotion：

- 先用可靠 human prior，再训练 camera specialist。
- 用轻量 relation / communication adapter 协调，而不是让一个 share-all model 同时承担所有任务。

### 8.6 AnyMo：统一任意条件需要规模、分层表示和课程

AnyMo:

- Paper: [https://arxiv.org/abs/2605.29488](https://arxiv.org/abs/2605.29488)
- Dataset: [https://huggingface.co/datasets/L-yiheng/OmniHuMo](https://huggingface.co/datasets/L-yiheng/OmniHuMo)

关键证据：

- 统一多模态 motion generation 不是简单拼接条件。
- 需要 residual tokenization、parallel masked modeling、large-scale data、staged curriculum。

对 StoryMotion：

- 若要统一 story / human / camera / relation，必须保留 modality-specific capacity 与 staged training。

---

## 9. 建议的新架构方向

### 9.1 最小推荐框架

```text
Goal:
  Preserve one unified three-mode StoryMotion interface.
  Avoid implementing it as symmetric random masks.

Stage1:
  Use verified Pulp official-equivalent AE.
  Do not promote self-trained AE until official recon gate passes.

Shared components:
  text encoder
  temporal backbone or shared prior blocks
  explicit relation / screen framing tokens
  mode embedding in {joint, camera_completion, human_completion}
  source embedding in {gt, noisy_gt, generated, missing}

Mode-specific routes:
  JOINT:
    text_human + text_camera + relation_prior -> H_hat, C_hat

  CAMERA:
    camera_text + H_condition + source_tag + trust + relation -> C_hat

  HUMAN:
    human_text + C_condition + source_tag + weak_camera_constraint + relation -> H_hat
```

A practical staged version can still use specialists, but only as components or diagnostics:

```text
Human prior:
  text_human -> H_hat
  goal: generate action/root/timing latent

Camera specialist:
  inputs:
    camera_text
    H_condition
    source_tag in {gt, noisy_gt, generated, missing}
    trust_scalar or sigma
    relation_token / screen_framing_token
  output:
    C_hat

Joint inference:
  H_hat = human_prior(text_human)
  C_hat = camera_specialist(camera_text, H_hat, source=generated, trust=q)
```

最终论文卖点仍可表述为 unified three-mode StoryMotion；实现上则是 unified interface + asymmetric internals，而不是 one raw concat denoiser with symmetric random mask.

### 9.2 必须新增的机制

1. **Trust-gated observed human**

不要 hard-clamp noisy/generated human：

```text
bad:  always replace observed branch with H_obs
good: use source tag + trust scalar + gated cross-branch read
```

2. **Camera root residual split**

```text
C = C_global_text_prior + C_human_conditioned_residual
```

把 text-driven global camera motion 与 human-root-dependent framing residual 分开，避免 human root error 直接污染整个 camera。

3. **Relation / screen framing token**

引入显式 `R`：

```text
R = screen framing / human-camera geometry / Pulp W row-space surrogate
camera branch reads: camera_text + H + R
```

4. **Mode-specific routing, not mode collapse**

```text
JOINT route:
  text -> shared relation prior -> H,C

CAMERA route:
  H_condition is strong but source-gated
  camera_text must remain active

HUMAN route:
  C_condition is weak/ambiguous
  human_text and human prior must dominate
```

这保留了三模式统一，但不再假设三模式是同一种 mask completion。

5. **Branch-specific adapters or heads**

保留共享时序 prior 可以，但输出 head、condition path、cross-branch adapter 应分开。human stream 不应随意读取 camera noise。

6. **External generated-human replay**

测试 camera specialist 时，generated-human replay 必须接一个外部 human prior：

```text
H_hat = human_prior(text_human)
C_hat = camera_specialist(camera_text, H_hat, source=generated)
```

不能用 camera-only checkpoint 自己先生成 human，这不是有效 replay。

---

## 10. 每个新方案必须通过的实验 gate

| gate | setting | success criterion |
| --- | --- | --- |
| Stage1 official recon | decode AE output, run human/camera/projection official metrics | close to Pulp official AE upper bound |
| three-mode sanity | evaluate JOINT / CAMERA / HUMAN separately | no mode collapses hidden by average score |
| clean camera completion | condition on GT human latent | camera FDCLaTr/F1 close to old clean `14.50 / 0.638` |
| noisy human condition | add matched noise `0.15/0.30` to observed human | much better than old P2a and v6.4 noise collapse |
| generated-human replay | condition camera on external human prior output | not close to replay collapse |
| camera text shuffle/zero | perturb camera text only | output should meaningfully degrade if camera text controls camera |
| mode weight ablation | change JOINT/CAMERA/HUMAN sampling weights | identifies whether symmetric equal mixing causes conflict |
| source tag ablation | remove gt/noisy/generated/missing tag | robustness should degrade if reliability modeling is doing real work |
| relation/framing eval | screen framing / out-of-screen / root-in-frame metrics | improved framing without killing human quality |
| sampler audit | compare teacher, 1-step, 20-step, 50-step | no large teacher-to-sampler gap |

---

## 11. 明确不要做的事

不要：

- 把 clean GT-human camera completion 称为 robust joint generation。
- 把 StoryMotion 改写成单纯 story text -> human-camera generation，而忘掉核心卖点是三模式统一。
- 把 Stage1 training loss 或 feature MSE 称为 Stage1 成功。
- 继续把 CondMDI 的随机 mask 原样套到 human-camera 三模式。
- 把 `TASK_CAMERA`、`TASK_HUMAN`、`TASK_JOINT` 当成完全对称、同权、同结构的 mask cases。
- 在 Stage1 official recon gate 失败时，比较 self-trained tokenizer 上的 Stage2 架构优劣。
- 用 camera-only checkpoint 自己生成 human 来做 generated-human replay。
- 直接换 Transformer / DiT / RF 并期待自动解决 coupling；routing 和 reliability 未修时，backbone 替换大概率只是重置问题。

---

## 12. 请网页端 LLM 给出的理想输出

请基于以上信息输出：

1. **根因诊断**：必须先解释三模式对称训练为什么与 human-camera 非对称依赖冲突，再按 Stage1 contract、hard observed injection、root-relative camera contract、text shortcut、raw concat coupling 分层分析。
2. **架构方案**：提出一个最小可实现的新 Stage2，要求保留三模式统一接口，但内部使用非对称 routing / loss / source reliability；不要泛泛说“加 attention”，要说明输入、输出、条件路由、loss、sampler。
3. **实验矩阵**：列出 3-5 个最小 ablation，每个说明改变什么、验证哪个假设、成功/失败如何解释。
4. **风险清单**：说明哪些风险必须先排除，哪些可以暂时绕过。
5. **论文叙事建议**：如果要写 ICLR，贡献应定位为 task/protocol/diagnosis/repair，还是完整 robust generation method。

请用严格研究判断回答；如果某个建议只是猜测，请明确标注“假设”并给出验证实验。
