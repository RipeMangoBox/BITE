---
title: "StoryMotion 0619–0626 进度总结"
status: draft
created: 2026-06-26
updated: 2026-06-26
tags:
  - StoryMotion
  - progress-summary
  - experiment
source_notes:
  - "[[2026-06-22_storymotion-v5]]"
  - "[[2026-06-23_storymotion-decoupled-coupling-qa-v5.1]]"
  - "[[2026-06-24_storymotion-decoupled-coupling-claude-review-zh]]"
  - "[[2026-06-25_storymotion-v6]]"
  - "[[2026-06-25_storymotion-v6.1]]"
---

# StoryMotion 0619–0626 进度总结

> 0619 以后的核心进展：从"三模式统一 + 指标 SOTA"叙事，经 source tokenizer 坍塌、containment loss 失败、耦合诊断，收缩为"Pulp frozen Stage1 地基 + human→camera 方向建模 + condition reliability"路线。共完成 **5 个成功确证、4 个失败路线排除、3 个诊断闭环**；外部 baseline 与下一轮 P2b 训练仍在进行中。

---

## StoryMotion 核心假设层级

所有实验按对以下假设的支撑度和相关性排序：

| 假设 | 内容 | 若成立意味着 | 若失败意味着 |
| --- | --- | --- | --- |
| **H1** | Unified branch-mask framework 三模式统一有效 | 统一框架是参数效率与多任务能力的实证贡献 | 三模式只是拼接，unified 没有架构价值 |
| **H2** | Pulp frozen Stage1 是正确地基 | Bottleneck 在 Stage2，集中创新即可；source tokenizer 不可替代 | 需要重新设计 Stage1 contract |
| **H3** | human→camera 因果方向必须被尊重 | 生成顺序应从 human 到 camera，同步 denoising 存在结构错配 | Raw-latent concat 不是核心问题，另找根因 |
| **H4** | Completion 需要 condition reliability modeling | Hard-observed-replacement 是当前 completion 脆弱的主因 | Completion 退化另有来源 |
| **H5** | 受控耦合是关键技术挑战 | Coupling asymmetry 和 branch pollution 是论文核心贡献点 | 简单耦合即可，不需要显式控制 |

---

## 一、成功确证（5 项）

> 按对核心假设的支撑度排序：H3+H5 耦合方向 → H2 地基 → H1 主性能 → H1 辅助证据 → 校准

### S1. Coupling 方向定位完成 — 支撑 H3 + H5

**与核心假设的关系**：这是最塑造后续假设的诊断结果。PI 不对称 + 源码 contract 直接催生了 H3（camera 必须依赖 human root），P2a 退化斜率定义了 H5（耦合是方向性污染，不是简单强度问题）。

**结论**：camera 对 observed human/root 高度依赖，human 对 observed camera 基本稳健。

**数据**（P4.1 PI + P2a matched-noise sweep）：

| 指标 | 值 | 含义 |
| --- | ---: | --- |
| PI_C_from_H (FDCLaTr) | +288.5 | observed human 加噪使 camera 灾难退化 |
| PI_H_from_C (FDTMR) | +27.99 | observed camera 加噪使 human 轻中度退化 |
| camera noise std=0.15 | FDCLaTr 96.9 vs clean 14.8 | camera completion 脆弱支路 |
| human noise std=0.50 | FDTMR 154.7 vs clean 126.7 | human completion 相对稳健 |

**源码根因**：Pulp camera feature 的 distance block 为 `camera_translation - human_root_translation`，decode 又加回 human root。camera latent 不是独立于 human 的变量。

### S2. Pulp Stage1 是稳定表示地基 — 支撑 H2

**与核心假设的关系**：H2 是整个架构的基础——如果 Pulp Stage1 本身是瓶颈，那么所有 Stage2 创新都建立在错误地基上。Stage1 vs Stage2 gap 数据直接证明 bottleneck 在 Stage2，为 H2 提供了最干净的验证。

**数据**：本地 mixed b64 full eval，10549 samples。

| 层级 | Human Cov | Camera Cov | r_fpd | Out |
| --- | ---: | ---: | ---: | ---: |
| Pulp Stage1 reconstruction | 85.41% | 87.16% | 0.238 | 4.64% |
| Pulp Stage2 no-Aux | 10.63% | 51.60% | 5.161 | 26.63% |
| StoryMotion clean joint | 37.43% | 65.80% | 0.482 | 7.58% |

**结论**：Pulp 的主要失真来自 Stage2 generation，不是 tokenizer/decode contract。保留 frozen Pulp Stage1、集中创新在 Stage2 是正确策略。

### S3. StoryMotion clean joint 本地 fair 对比优于 Pulp Stage2 — 支撑 H1

**与核心假设的关系**：H1 的核心主张是 unified framework 能生成高质量的 joint human-camera motion。这个结果是 H1 最直接的主性能证据——StoryMotion 显著缩小了 Pulp Stage2 的分布/覆盖/构图缺口。

**数据**：同 mixed split、同 evaluator、同 `batch_size=64` 的 point estimate。

| model | FDTMR | TMR | Human Cov | Camera Cov | r_fpd | Out |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pulp no-Aux | 376.39 | 23.34 | 10.63% | 51.60% | 5.161 | 26.63% |
| Pulp Aux | 426.21 | 24.87 | 8.88% | 49.02% | 3.832 | 17.69% |
| StoryMotion clean | 157.36 | 24.26 | 37.43% | 65.80% | 0.482 | 7.58% |

**边界**：单 seed full-set point estimate，R@K 依赖 batch-size（b64 内公平），不能写成多 seed 显著或 Pulp 默认 b128 SOTA。TMR 低于 Pulp Aux（24.26 vs 24.87）。

### S4. Unified 框架 completion 守门通过 — 支撑 H1

**与核心假设的关系**：H1 的另一半——unified model 不能以牺牲 completion 为代价换取 joint 质量。这个"不劣于 specialist"的守门结果证明共享 branch-mask backbone 不损伤单任务能力，是 H1 成立的必要条件（但仍不充分，缺失 joint-only specialist 对照）。

**数据**：unified model 在 camera/human completion 上与对应 specialist 持平。

| task | unified | specialist |
| --- | ---: | ---: |
| camera FDCLaTr | 14.50 | 14.34 |
| camera CLaTr | 55.62 | 56.99 |
| human FDTMR | 126.71 | 125.28 |
| human TMR | 18.17 | 18.24 |

**边界**：仍缺 joint-only specialist 与参数 / FLOPs / wall-time 成本汇总，不能写"统一框架全面优于三模型 ensemble"。

### S5. GT-human oracle 闭环 — 校准 TMR 解释

**与核心假设的关系**：间接支撑 H3——如果 generated human TMR 远低于 GT-human TMR，那么 joint human 的语义退化可能来自 human 生成能力本身而非 camera coupling。实际结果显示两者同量级，从而把 joint 缺口进一步聚焦到 coverage/framing/coupling，而非 human text semantics。

**数据**：full mixed bs64，10549 samples，TMR=17.71，FDTMR≈0，HCov=100%。

**结论**：当前 generated human TMR（unified 18.17、specialist 18.24）与 GT oracle TMR (17.71) 同量级。StoryMotion 的主要缺口是 joint coverage / framing / coupling，不是单纯 human text semantic score。

---

## 二、失败路线排除（4 项）

> 按对核心假设的测试强度排序：H2 替代方案否定 → H3 修复直接测试 → H3 捷径否定 → 辅助假设

### F1. Source tokenizer 替换 Pulp Stage1 ❌ — 测试 H2 的替代方案

**与核心假设的关系**：这是对 H2 的最强消融——如果任意 Stage1 都能接入 Stage2 并产生可用的 official metrics，那么 H2（"Pulp Stage1 不可替代"）就不成立。8/8 全部坍塌的结果是 H2 的负面对照，它把 H2 从"一个合理选择"升级为"当前唯一可用选择"。

**尝试**：用 joint/separate VAE / HFSQ / GRFSQ 替换 Pulp Stage1 tokenizer，配置 Z-score 归一化与 geo loss 变体。

**数据**（pure human completion，4053 samples）：

| tokenizer | FDTMR | Human Cov |
| --- | ---: | ---: |
| Pulp Stage1 (参考) | 112.28 | 90.58% |
| 8 组 source tokenizer | 1308.67–1413.23 | 0.049%–0.691% |

**结论**：8/8 配置全部坍塌。Z-score 只对齐一阶二阶统计，不能保证 latent 时序相关性、跨分支语义结构或 decoder 有效流形。应停止继续做 Z-score / geo weight / loss-only sweep。保留 Pulp frozen Stage1 为主线。

### F2. RootHead-only root-first ❌ — 直接测试 H3 的修复方案

**与核心假设的关系**：这是对 H3 最直接的修复尝试——如果 C1 的根因是"human root 没有被显式建模"，那么在 neutral training 上加 root 辅助监督应该能改善 camera/joint。结果是否定的：辅助 root loss 没有转化为 camera distance / joint framing 质量。这没有否定 H3 本身（root 信息确实存在但没有被 Stage2 有效利用，恰好说明需要更深的架构级 factorisation，而非辅助 loss），但排除了"加一个 RootHead loss 即可"的最小修复路径。

**尝试**：保持 `task_probs=[1,1,1]` neutral training，添加 RootHead 辅助 root supervision（`root_first_weight=0.01`），测试 root 辅助监督是否修复 C1。

**数据**（4090，mixed b64）：

| model | camera FDCLaTr | human FDTMR | joint Out |
| --- | ---: | ---: | ---: |
| unified baseline | 14.50 | 126.71 | 7.89% |
| root-first | 65.12 | 137.80 | 45.26% |

**结论**：RootHead 没有把 root 辅助监督转化为 camera distance / joint framing 质量。joint Out 达 45.26%。后续不能只看 training-time `root_aux_loss`，必须补 eval-time root trajectory error。H3 的修复需要更深层的生成顺序改动，而非辅助 loss。

### F3. Human-first camheavy 训练捷径 ❌ — 测试 H3 的错误实现

**与核心假设的关系**：测试了 H3 的一个实现变体——通过 task distribution 强行压制 human-only 任务来"模拟" human-first。该实现违背了 H3 的核心逻辑（human-first 要求先生成 human 再生成 camera，而不是禁用 human 生成能力），因此失败不能否定 H3。但它提供了有价值的工程教训：`task_probs_human=0.0` 会同时破坏所有依赖 human root 的任务。

**尝试**：从 normal checkpoint fine-tune，设 `task_probs=[2,0,1]`（禁用 human-only 任务），测试强化 camera/joint 的捷径。

**数据**（4090，mixed b64）：

| model | camera FDCLaTr | joint FDTMR | joint Out |
| --- | ---: | ---: | ---: |
| unified baseline camera | 14.50 | — | — |
| camheavy camera | 84.94 | — | — |
| unified baseline joint | — | 155.73 | 7.9% |
| camheavy joint | — | 366.63 | 21.39% |

**结论**：`task_probs_human=0.0` 破坏 standalone human generation，camera/joint 同时失去 human/root 锚点。该结果只能否定"禁用 human-only 任务"的训练捷径，不能否定 inference-time human→camera 两段式采样。

### F4. Screen projection containment 主线路 ❌ — 辅助假设

**与核心假设的关系**：测试一个与核心假设正交的辅助假设——"containment loss 可以在不破坏语义的前提下降低 outscreen"。它不是对 H1-H5 任一假设的直接测试，而是对潜在附加贡献点的可行性验证。失败结论（强约束导致 camera collapse + NaN）使该路线被排除，但对核心假设体系无直接影响。

**尝试**：在 Pulp 主路线上加 projection containment loss (w=0.01)，压低出屏率。

**数据**（5090 b64 full eval）：

| checkpoint | Out | FDCLaTr | F1 | Camera Cov |
| --- | ---: | ---: | ---: | ---: |
| clean control | 7.58% | 76.85 | 40.21% | 65.80% |
| screen best@170000 | 0.50% | 350.09 | 17.44% | 33.14% |
| screen last@176000 | NaN | NaN | NaN | NaN |

**结论**：强 projection penalty 可压低出屏率，但破坏 camera distribution/semantics，训练从 175100 起 NaN。当前实现停止进入主线；若重启需 bounded loss、gradient guard 与渐进权重。

---

## 三、诊断闭环（3 项）

> 按对核心假设的贡献排序：H4+H5 基础诊断 → H5 排他诊断 → 工程修复

### D1. Controlled coupling dependency matrix — 催生 H4 + H5

**与核心假设的关系**：这是最基础的诊断实验，A/B/C/D 的结果直接定义了 H4（completion 是 observed-dominant，不是均衡条件生成）和 H5（耦合不对称，camera 依赖 human 远强于反向）。没有这个矩阵，后续假设无处锚定。

**完成**：A 矩阵 15/15 items，B/C/D 全部完成（mixed full test，10549 samples）。

**关键发现**：
- Completion 不是 text + observed 均衡条件生成，而是 observed-dominant（text noise 基本不影响指标，observed branch 破坏则灾难退化）
- Joint 是 text-driven generation（shuffle/zero text 后语义指标大幅下降）
- Generated-camera replay 不能修复 joint human（与 joint baseline 同区间）
- Boundary schedule 是诊断旋钮而非修复（手调 inference gating，不是 learned controller）
- GT-camera oracle 给出几何/覆盖上界（Human Cov 84.58%，MPJPE 0.0884）

### D2. Text routing 诊断 — 排除 H5 的替代解释

**与核心假设的关系**：H5 认为 joint 弱来自 latent human-camera coupling。一个竞争解释是 text routing cross-talk——camera text 和 human text 在 joint 中互相串味导致指标下降。D2 用 clean 对角结果排除了这个替代解释，把根因更干净地聚焦到 latent coupling。

**数据**（routing intervention）：

| intervention | cam CLaTr | hum TMR |
| --- | ---: | ---: |
| clean joint | 33.5 | 23.95 |
| zero/shuffle camera text | 12.0 | 24.34 |
| zero human text | 42.4 | 4.45 |

**结论**：text routing 基本对角，joint 弱主要来自 latent human-camera coupling，不是 camera/human text 串味。

### D3. R@K batch-size 依赖定位与修复 — 协议工程

**与核心假设的关系**：不对任何核心假设提供直接支撑或否定。它的价值是清除评估噪声——如果 R@K 随 eval batch size 大幅波动，那么跨模型/跨实验的 R@K 比较都不可信，S3（joint 优于 Pulp）的证据质量也会被质疑。

**发现**：Pulp 默认 eval batch=128，StoryMotion 历史用 b16。Pulp `RetrievalMetric` 每个 batch 内构造 B×B 候选池，R@K 不是 batch-size invariant。

**修复**：
- 补齐 Pulp pure/mixed Stage1/Stage2 b64 rerun
- 跨机器审计确认两机数据一致（b16 复现，b64 只改变 R@K，FD/score/coverage 不变）
- v6.1 内部公平对比统一使用 bs64

**待定**：论文对外比较需统一到 Pulp b128 或实现 batch-invariant retrieval。

---

## 四、未完成与进行中（3 项）

### T1. E.T./DIRECTOR camera completion baseline 🔄

- 隔离 clone 就绪：`robincourant/DIRECTOR` on 5090
- Pulp data view 已准备（mixed train 94050 / test 10549）
- from-scratch training 待启动
- **风险**：Pulp 暂无 `center_char/char_raw` 目录，首轮只能完成 camera-text baseline

### T2. MoLingo human baseline 🔄

- 隔离 clone 就绪：`hynann/MoLingo` on 5090
- Pulp→MoLingo 199→272 维 padding 导出中
- from-scratch SAE + MoLingo training 待启动
- **风险**：zero padding 可能浪费容量；评估必须裁回 199 维

### T3. P3 no-camera / root-only human variants 🔄

- 尚未完成，用于拆清 actor recovery vs camera-agnostic generation

---

## 五、实验缩写对照

| 缩写 | 说明 | 状态 |
| --- | --- | --- |
| SM-normal | `independent_dropout_ft_20260614`，三任务 neutral training | ✅ 主对照 |
| HF-camheavy | `task_probs=[2,0,1]`，human task disabled | ❌ 失败 |
| RF-roothead | `task_probs=[1,1,1]` + RootHead `w=0.01` | ❌ 失败 |
| GT-human | GT human raw → official HumanMetric，TMR/FDTMR oracle | ✅ 完成 |
| ET-cam | DIRECTOR from-scratch on Pulp camera-text | 🔄 进行中 |
| ML-human | MoLingo from-scratch on Pulp human (199→272) | 🔄 进行中 |

---

## 六、核心决策与路线

### 已确定

1. **保留 Pulp frozen Stage1**：source tokenizer 路线已排除
2. **下一版核心技术问题**：human→camera 方向建模（不是 camera-first）、condition reliability、human mode 任务拆分
3. **Split human mode**：区分 camera-conditioned actor recovery / camera-agnostic generation
4. **Completion reliability**：observed source ∈ {clean, additive-noisy, generated, missing} + quality token
5. **R@K 协议**：内部 b64 已完成；论文对比待定 b128 或 batch-invariant
6. **Learned gate 后置**：先在 root/relation 接口确定后再考虑

### 论文可写

- 统一 branch-mask framework 在三模式下的接口与能力
- 本地 b64 公平对比下优于 Pulp Stage2（非统计 SOTA）
- Pulp camera 表示依赖 human root 的代码事实
- Coupling diagnostics（PI、dependency matrix）
- Completion 需要区分任务边界和 condition reliability

### 论文不写

- 全面显著超过 PulpMotion
- human 与 camera 已解耦
- completion 已公平胜出
- source tokenizer 只是没调好
- boundary/screen containment 已是最终修复

### 下一步最小动作

1. DIRECTOR from-scratch 训练与 eval（camera-text baseline）
2. MoLingo from-scratch SAE + 主模型训练
3. Inference-time human-first 两段式采样（不改训练，在 baseline 上测 factorization 收益）
4. Eval-time root/framing metric 补齐
5. P0 closure：补 joint-only specialist + 参数量/FLOPs/wall-time 表
6. P3 closure：补 no-camera 与 root-only human variants

---

## 七、协议约束（全阶段通用）

- 所有训练为单 seed point estimate，不能写"显著改善"
- R@K/TMR 是 batch-local retrieval，内部 bs64、外部待定 b128 或 global retrieval
- PI 与 reliability 测试使用 matched additive noise protocol；random replacement 单独标记
- P1 后续训练必须保持 human-only 能力，禁用 `task_probs_human=0.0`
- 官方 full metrics 为继续条件，不再扩展 loss-only sweep
