---
title: "StoryMotion ICLR 2027 Reliability Plan"
hypothesis: |
  StoryMotion最有机会中稿的主张是可审计的non-causal asymmetric Human-first
  generation，而不是全面SOTA或未经验证的editing。v11 C0-LAT/C0-GEO已经提供
  系统端点；剩余工作应优先关闭贡献可解释性、统计复现、感知评测和复现性缺口。
status: in_progress
tags:
  - StoryMotion
  - reliability
  - contribution
  - ICLR
  - ICLR/2027
  - status/active
source_notes:
  - "[[current]]"
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract]]"
  - "[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]"
source_papers:
  - "[[analysis/ICCV_2025/VACE_All-in-One_Video_Creation_and_Editing]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion]]"
created: 2026-06-18T00:00:00+08:00
updated: 2026-07-31T23:30:00+08:00
supersedes: "[[2026-06-16_storymotion-v3-formal]]"
---

# StoryMotion ICLR 2027 Reliability Plan

> [!important] 总判断
> StoryMotion 已经从“模型是否能工作”进入“论文是否能被相信”的阶段。v11
> C0-LAT 与 C0-GEO 的 pure4,053 三模式、geometry、physical、bootstrap 与 visual
> evidence 足以冻结共同 mainline，但尚不足以直接支撑 ICLR 接收。最大风险不是再少
> 一个内部 arm，而是：方法故事仍显工程化、Stage1 必要性没有干净因果证据、主线仅
> 有 seed17、视觉优势缺少盲评、external baseline 与复现实验包尚未形成闭环。

正式数字与 hashes 只见 [[StoryMotion-valid-metric-ledger]]；本页只拥有论文
claim-evidence gap、优先级、停止条件与 acceptance strategy。

## 1. 建议冻结的论文中心

### 1.1 一句话主张

> StoryMotion uses a non-causal asymmetric Human-first factorization to
> support Human generation, observed-Human camera completion, and sequential
> Human–Camera generation under an auditable representation and evaluation
> contract.

中文含义是：先建立可保护的人体生成 owner，再让 Camera 读取明确来源的 fixed
Human context；联合生成采用 Human→Camera sequential solver，避免把 evolving-H
parallel denoising重新引入主线。C0-LAT 与 C0-GEO 是同一方法的两个 Camera objective
endpoint，用来诚实呈现 semantic／geometry Pareto，而不是两套互相竞争的方法。

### 1.2 三项可写贡献

1. **Asymmetric Human-first formulation。** 一个非因果、来源显式的 Human／Camera
   latent factorization，支持 Direct-H、Direct-C 与 sequential joint，并在 Camera
   训练中逐位保护 Human owner。
2. **Objective-level Pareto evidence。** 在固定 Stage1、Human teacher、cache、sampler
   和预算下，只改变 Camera LAT/GEO objective；结果不支持虚假的单一胜者，而支持
   双 endpoint 的可复现 Pareto 报告。
3. **Auditable system evaluation。** 把 checkpoint／decoder／cache／sample IDs／sampler
   与 semantic、decoded geometry、framing、physical diagnostics、bootstrap 和 visual
   evidence绑定，明确 system comparison 与 matched ablation 的边界。

第三项只有在代码、配置和最终复现实验包真正可发布时才能写成贡献；否则降为实验
严谨性，不单独占 contribution bullet。

### 1.3 不应进入主 claim

- “所有指标全面 SOTA”或“C0-GEO 稳健优于 C0-LAT”；现有证据不支持。
- “C0 sequential 在 matched 条件下支配 C3 joint parallel”；formal solver不同。
- “v10 证明简化 Stage1 必然失败”；v10同时改变多个变量。
- “支持 motion editing”；尚无正式任务、训练阶段或 masked-region evidence。
- “physical validity 已解决”；contact／skate 仍是 heuristic。

## 2. 距离 ICLR 中稿还有多远

当前状态属于**有完整系统结果，但论文因果链尚未闭合**。如果不再新增内部功能，
仍需要完成以下 hard gaps：

| gap | 当前证据 | 审稿风险 | 接收前最低闭环 | 优先级 |
| --- | --- | --- | --- | --- |
| 方法中心与新颖性 | 有v11三模式和protected-H/sequential设计 | 被看成多个工程修补的组合 | 一张方法图、一句核心原则、三项以内贡献；每个模块绑定failure mode | P0 hard |
| Stage1设计依据 | v9 Stage1有效，但Human anchor、interaction residual、三阶段schedule复杂 | “为什么需要这么复杂；简单模型是否也行？” | 明确它是贡献还是backbone；若是贡献，补最小matched ablation；若非贡献，收缩claim并给机制probe | P0 hard |
| 统计复现 | 主线selection来自seed17；LAT/GEO CI只覆盖matched samples | seed特例、训练偶然性 | 至少完成独立Stage2 seeds；报告mean／std与失败率，不再用单seed选臂 | P0 hard |
| 感知有效性 | fixed-8 visual已齐，C3有“平均化”视觉问题 | 指标与实际观感错位 | 预注册盲评：随机系统名、同prompt、质量／构图／动作一致性／偏好，报告置信区间 | P0 hard |
| Baseline公平性 | C3、v9、Pulp已有；协议不完全一致 | 内部baseline多、公共同任务baseline不足 | 以Pulp native为必要外部baseline；其余只纳入能匹配任务和输出的公开系统，并逐行标差异 | P0 hard |
| Generalization | pure4,053已被反复用于开发 | test-set overfitting／selection leakage | 冻结所有选择后，用新sampling seeds与预注册盲评cohort做一次sealed final audit | P0 hard |
| Reproducibility | contracts／hashes丰富，远端代码仍有未入Git工作 | 结果不可复现、artifact依赖主机 | clean Git commit、配置、环境、命令、模型身份、训练成本、最小demo与table generator | P0 hard |
| Editing | 尚未验证 | 若标题／摘要提及会成为直接缺陷 | 要么从主claim删除，要么完成独立Edit phase与formal masked evaluation | P1 conditional |
| 跨数据域 | HumanML控制存在但有invalid arm | 只在Pulp有效 | 作为限制可接受；若宣称通用，必须补合法外域实验 | P1 conditional |

在上述 hard gaps 中，继续训练 C1、恢复 v10 Camera Stage2 或新增更多 Camera objective
都不是默认解法。它们提高内部覆盖，却不直接提高论文可信度。

## 3. Stage1 复杂性：如何避免被 reviewer argue

### 3.1 先做贡献归属决策

有两条合法路线，必须二选一，不能同时模糊表述：

**路线 A：Stage1 是论文贡献。** 需要证明 Human anchor、interaction residual 和训练
分阶段各自解决什么，以及删掉它们会损害哪一项。审稿人会合理要求 matched
ablation；仅展示最终重建和 Stage2 结果不够。

**路线 B：Stage1 是可靠 backbone。** 主贡献放在 protected Human、fixed-context
Camera 和 sequential solver。Stage1 只需说明设计原则、非因果合同、owning decoder
和必要的机制检查，不声称每个部件都是新颖或最优。这条路线更容易在当前证据下
闭环，也是建议默认。

### 3.2 可以清楚说出的设计依据

v9 Stage1 的复杂度可以压缩为三个功能，而不是逐项罗列内部版本：

1. `z_h` 只由 Human 输入拥有，`D_h` 只读取 `z_h`，用于给冻结 Human teacher一个
   Camera-free owner。
2. `z_hc` 单独承载 Human–Camera framing interaction，避免把全部耦合塞回 Human
   latent或 Camera trajectory latent。
3. `z_c` 承载 Camera-native trajectory；`D_c/D_f`联合读取`z_h,z_hc,z_c`，使
   Camera reconstruction与构图仍有 owning decoder。

三阶段 schedule 的合理解释是：先建立 Human owner，再学习 Camera／interaction，
最后以低 Human 学习率做joint calibration。这个解释是机制假设；只有已有的Human
invariance、decoder/oracle与阶段checkpoint evidence能支持到哪，就写到哪，不把它
扩张成“所有阶段均已证明必要”。

### 3.3 v10 能说明什么、不能说明什么

v10更简单，但它同时改变了 Human owner、interaction16、Camera factorization、loss
contract、训练phase与下游Stage2完成度；早期版本还遗漏framing反传。因此：

- 可以把v10写成“独立相对Camera factorization的探索性负结果／未闭合路线”；
- 不能把v9-v10差异写成单变量Stage1复杂度消融；
- 不能因为v10 Stage1/Stage2退化就断言interaction residual或三阶段schedule必需。

### 3.4 最小补强，而不是重开大矩阵

按收益排序：

1. **零训练机制表。** 汇总 `z_h` Camera invariance、`z_hc/z_c` zero／shuffle／oracle、
   owning-decoder敏感性和阶段checkpoint，只回答“模块是否被实际使用”。
2. **若采用路线B，到此停止Stage1新训练。** 把复杂度诚实列为backbone limitation，
   论文贡献不依赖其component-wise optimality。
3. **若坚持路线A，只补一个matched ablation family。** 固定数据、参数量、loss、phase、
   seed和Stage2协议，分别去掉interaction residual或合并phase；预注册一个主要问题，
   不把v10拿来替代。没有资源完成端到端matched ablation时，应回到路线B。

## 4. 接收导向的最小实验包

### 4.1 必做

1. **独立Stage2复现。** 固定同一Stage1/Human owner，C0-LAT与C0-GEO各补至少两个
   独立训练seed；同三模式、same pure cohort、same evaluator报告mean／std。共同
   mainline身份不因单个seed raw mean改变，只有系统性失败才重开selection。
2. **盲评。** C0-LAT、C0-GEO、C3与Pulp共享prompt cohort；至少评动作文本一致性、
   Camera文本一致性、主体可见／构图、运动自然度和总体偏好。样本顺序与系统名随机，
   统计unit是rater×sample而不是视频帧。
3. **Sealed final audit。** 现在冻结模型选择与指标代码；更换生成seed并冻结一组此前
   未用于挑选截图的prompt／sample，最终只跑一次。
4. **公开baseline矩阵。** Pulp native必须保留；C3作为former-mainline internal
   baseline；v9作为同owner失败端点。新增公开baseline只在能执行相同任务时进入，
   不能用缺失模式补造排名。
5. **复现实验包。** 两个mainline配置、exact artifact identities、环境、训练／评估
   命令、三模式输出schema、table generator、fixed demo和计算成本一次冻结。

### 4.2 强烈建议

- 至少一个独立 Stage1/Human owner seed，再在预注册的一个 Camera objective 上完成
  end-to-end repeat。这比继续扩 Camera objective 更直接检验整条pipeline稳定性。
- 按长度、转向强度、Camera文本类型、主体出框风险做 failure taxonomy，并把最好、
  随机、最差样本都纳入补充材料。
- 报告参数量、训练GPU小时、推理延迟、显存和solver步数；共同mainline不能只报告
  最好臂而隐藏另一臂成本。

### 4.3 低收益或暂缓

- C1 swapped-host replay：只在论文要声称teacher-final mixed context因果失败时需要。
- v10 Camera Stage2：除非决定把Stage1简化作为论文主贡献，否则不阻塞中稿。
- 更多LAT/GEO权重、Camera CFG、PCGrad或新adapter：当前没有直接关闭hard gap。
- 对已开发的pure4,053继续挑checkpoint或样本：会加重selection leakage。

## 5. Editing：先决定是否值得进入论文

### 5.1 推荐默认

如果论文标题和摘要聚焦 generation，**本轮不把 editing 作为必做**。明确写成future
work比提供一个弱、无协议的demo更安全。三种generation模式已经足以形成完整主线。

### 5.2 若坚持把 editing 写成贡献

先冻结任务合同，再写代码。建议新增独立的 Stage2 Edit phase，初始化自两个C0
endpoint，但不改写generation checkpoints：

```text
Phase E-H: observed Human outside mask + text -> masked Human latent
Phase E-C: final/observed Human + observed Camera outside mask + camera text
           -> masked Camera latent
Joint edit: Phase E-H completes first, then Phase E-C; no joint parallel
```

最小训练与推理规则：

- Stage1与owning decoder全冻结；C0-LAT/GEO各自拥有edit checkpoint。
- 训练随机采样prefix、suffix与interior contiguous masks；loss只作用于masked region。
- 每个solver step强制clamp unmasked latent，保证未编辑区域exact preservation。
- Human edit先完成，Camera edit再读取final Human；不重新引入evolving-H parallel。
- 不同时加入新数据清洗、Stage1表示或Camera CFG，保持因果轴单一。

最低formal evaluation：masked-region Human MPJPE／root/yaw、Camera ADE/FDE／rotation、
mask边界速度／加速度连续性、unmasked max-abs preservation、文本编辑成功率和盲评。
prefix／suffix／inbetween必须分开报告。若只完成Camera edit，就明确称Camera trajectory
editing，不称unified motion editing。

停止条件：generation三模式回退、unmasked区域不再exact、编辑只在训练mask形状有效，
或新增能力无法形成比主论文更清楚的第四个实验问题。出现任一项，就把editing移回
future work。

## 6. Paper-ready claim-evidence matrix

| candidate claim | 当前状态 | paper-safe wording | 缺失证据 |
| --- | --- | --- | --- |
| 同一Human owner支持三种不对称模式 | 已有pure4,053 formal | supports Direct-H, observed-H Direct-C and sequential joint generation | multi-seed + sealed audit |
| LAT/GEO存在可报告Pareto | 已有matched bootstrap | two co-mainline objectives expose a semantic/geometry Pareto | training-seed stability |
| v11系统优于former C3 | 部分支持 | improves several semantic, coverage, framing and geometry axes under a system boundary | blind preference；不写全面支配 |
| 优于PulpMotion | 只支持部分native指标 | favorable system-level metrics under explicit native boundaries | blind study；task mismatch说明 |
| Stage1每个复杂部件均必要 | 未支持 | omit；或称failure-driven backbone design | matched component ablation |
| Editing能力 | 未验证 | omit / future work | 完整Edit phase与formal evaluation |
| Physical validity | 未闭合 | reports no-reference kinematic diagnostics | calibrated ground/contact evaluation |

## 7. Go／no-go 标准

### 可进入投稿整合

- 中心主张稳定为Human-first asymmetric generation，贡献不超过三项；
- C0-LAT／C0-GEO多seed没有系统性崩溃；
- 盲评至少支持一项主观优势，且失败样本已披露；
- Pulp与C3对照完成，所有不可比字段显式标注；
- Stage1选择路线A或B，不再用v10做伪matched反证；
- 代码、配置、artifact身份、表格生成和demo可从clean Git revision复现；
- editing要么正式闭合，要么完全退出主claim。

### 应暂停扩功能，先修论文

- 新实验不能关闭上述任一hard gap；
- 又引入新的representation／objective／solver而没有淘汰旧claim；
- 只在开发cohort、单seed或挑选视频上改善；
- 为了“更多功能”牺牲Human保护或sequential合同；
- 结果需要靠改名、隐藏sample count或混合decoder才能看起来更好。

## 8. 当前优先顺序

1. 冻结 C0-LAT／C0-GEO co-mainline、论文一句话主张和 Stage1 路线B。
2. 清理并同步代码／配置，生成一键三模式与baseline结果表。
3. 启动主线独立Stage2 seeds，同时完成盲评协议与sealed cohort冻结。
4. 完成Pulp／C3／v9 baseline矩阵、failure taxonomy与计算成本。
5. 再决定editing：默认不进入主claim；只有能完整承担Phase E才启动。
6. 只有路线A被重新选择时，才运行最小matched Stage1 ablation。

这个顺序优先提高“审稿人是否相信核心结论”，而不是继续提高内部实验数量。
