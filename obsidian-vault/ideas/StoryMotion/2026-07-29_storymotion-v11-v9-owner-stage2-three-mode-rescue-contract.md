---
title: "StoryMotion v11 v9-owner Stage2 Three-Mode Rescue Contract"
status: four_arm_105k_pure4053_completed_c0_co_mainline
hypothesis: |
  v9 的 Human-anchor Stage1 与 protected Human teacher 已足以作为可审计的
  三模式父边界；固定 Stage1、Human teacher、LR 与 Camera initialization，
  用 GT-H / GT-H+teacher-final-H 两种 context schedule 和 LAT/GEO 两种
  objective 组成 2×2 的 Stage2 Camera 矩阵，可以判断 Camera generatability、
  generated-final exposure 与 decoded geometry supervision；四臂现已完成
  105K、first-512与pure4,053 formal audit，以及fixed-8 visual。
tags:
  - StoryMotion
  - version/v11
  - stage2
  - protected-human
  - camera
  - joint
  - root-cause
  - status/completed
aliases:
  - StoryMotion-v11-Stage2-Rescue
  - v11-v9-owner
source_notes:
  - "[[current]]"
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[Storymotion-exp-sha]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]"
  - "[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]"
created: 2026-07-29T19:15:43+08:00
updated: 2026-07-31T23:30:00+08:00
---

# StoryMotion v11 v9-owner Stage2 Three-Mode Rescue Contract

> [!abstract] 当前裁决
> v11四臂均已完成Camera optimizer `105K`、first-512／pure4,053三模式formal
> audit、decoded geometry／physical／bootstrap与fixed-8 visual。2026-07-31用户显式
> 将C0-LAT与C0-GEO共同晋升为mainline：两臂共享exact v9 Stage1/Human owner，
> LAT/GEO六项Camera geometry CI全跨零且其余字段为混合Pareto。C1两臂停止；
> C3-25转为former-mainline baseline。历史`diagnostic_only`／eligibility字段不回写。

## 1. 对当前问题的直接回答

### 1.1 v9 Stage1 能否直接适配 v10 Camera48

**不能直接适配。** 两个 representation 的语义与 decoder ownership 不同：

| boundary | v9 owner | v10 owner |
| --- | --- | --- |
| Stage2 cache | Human128 + interaction16 + conditioned-camera48 = 192D | Human128 + independent Human-relative Camera48 = 176D |
| Camera target | Camera64 = interaction16 + conditioned-camera48 | independent relative-Camera48 |
| Camera decoder | 读取 full192D | 只读 Camera48，再由 fixed `PhiInverse` 恢复 world Camera |
| Human owner | Phase-C `636K` 后的 `E_h,D_h` | exact Phase-A `210K` 的 `E_h,D_h` |
| normalization | v9 Camera64 train-only statistics | v10 Camera48 train-only statistics |

因此存在两条合法路径：

1. **v11 主因果路径**：完整保留 v9 Stage1 owner，Camera flow继续生成 Camera64，只修 Stage2；
2. **未来 hybrid control**：复用 v9 Human owner／teacher，但另训 v10-style independent relative-Camera48 encoder／decoder。该路径已经改变 Stage1，必须另立 run family，不能与 v11 Stage2-only 结果混写。

本合同选择第一条。若 v11 成功，支持“v9 Camera失败主要来自Stage2”；若C0的GT_H_CONDITION-only两臂都无法形成健康decoded Camera，再重新授权v10／hybrid Stage1 axis。

### 1.2 Direct-C 与 joint 是否都能让Camera读取已观测的Human

**可以，但必须区分Human的来源。** 从Camera模块的执行图看，两种模式都读取一个已经完成、固定且对Camera可见的Human context：

- Direct-C：`GT_H_CONDITION`，即数据集GT Human128 + Camera text → Camera64；
- formal joint：`TEACHER_FINAL_H_CONDITION`，即先由冻结Human teacher从noise完整生成Human128，再固定该H并生成Camera64。

原文把`observed Human`狭义等同于GT-H，造成了不必要的歧义。v11后续不用`OBSERVED_H`统称，而使用上述两个source name。第二种模式对Camera仍是fixed-H completion，但对完整系统是joint generation，因为Human也由模型生成；如果Human也来自GT，它只能叫Direct-C。

此前把joint-parallel保留为活动gate，是因为项目旧合同把它写成强制标准，不是因为parallel在v11技术上更合理。v9已经显示evolving-H context会叠加Camera instability；本合同现已将v11登记为显式例外：formal joint就是sequential，joint-parallel不训练、不评测、不gate，除非用户另行授权。

这个裁决也改变了v11的能力边界：它验证的是“同一系统依次生成Human与Camera”的三模式，不验证Human／Camera在同一去噪时间轴上的双向或同步耦合。若最终产品要求Camera在Human尚未完成时反向影响Human，sequential不能冒充该能力；那将是另一个需要单独授权的solver axis，而不是v11的晋级条件。

### 1.3 v10 是否已经证明不优于 v9

**没有。** v10 Human teacher与v9是mixed Pareto，但v10 corrected Stage1 Camera endpoint尚未完成formal audit，v10 Camera flow、Direct-C与joint都未运行。因而“v10 Stage2未显著优于v9”不是现有实证结论。

暂停 v10、优先执行 v11 仍然合理，但理由是 **减少变量、直接检验 v9 Stage1 是否足以支撑更合理的 Stage2**，而不是v10 Camera已经实测失败。

### 1.4 joint阶段能否用小LR同时微调Human和Camera

**v11 禁止。** Camera／joint loss不得更新 Human：

- Human completion必须保持Human-text-only；
- Direct-H与formal sequential joint第一阶段的Human在相同noise／sampler下必须逐元素一致；
- v9 protected-H exact `0.0` 是已闭合成功条件，不能在v11重新打开；
- 同时更新H/C会把Human drift、Camera适配与joint exposure重新耦合，破坏Stage2-only归因。

用户提出的“小LR joint fine-tune”在v11中改写为：**Human frozen，Camera适配teacher-final Human，同时持续replay GT-H**。第一轮LR固定`1e-4`，是否在后续continuation降LR由`30K`矩阵决定。若未来要测试双向joint update，必须另立非protected control，且不具备当前v11资格。

### 1.5 formal sequential joint 是否意味着 Stage2 只剩两个 phase

**从完整系统的训练职责看，是两个训练 phase；从本次四臂新增 optimizer 工作看，只有一个活动 phase。**

1. Stage H 固化 Human teacher：Human-text-only 的 Direct-H owner先完成并冻结。v11复用已闭合的v9 Human EMA `105K`，因此不重复训练。
2. Stage C 训练 Camera：Camera在固定GT Human或teacher-final Human条件下学习Direct-C与formal sequential所需的Camera conditional flow。

formal sequential joint 的“先Direct-H、再Direct-C”是**两个推理 pass**，不是第三个joint optimizer phase。它没有joint loss、不更新Human，也不打开joint-parallel。因而本次四臂`30K→105K`只继续Stage C的Camera optimizer；Stage H是只读父边界，formal joint是组合推理与评测协议。

## 2. v11 固定父边界

### 2.1 Stage1 owner

- version／run：v9 H-anchor Pulp-only `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726`；
- architecture：non-causal `human_anchor_interaction_residual_199_14_128_16_48_v1`；
- latent：Human128 + interaction16 + conditioned-camera48；
- Stage2 Camera target：Camera64 = `[interaction16,camera48]`；
- formal decode：只允许 exact v9 owning decoder；
- representation status：历史合同保留diagnostic-only与`promotion_eligible=false`；该owner通过2026-07-31 v11 C0 selection event成为共同mainline的共享Stage1，immutable字段不回写。

固定 checkpoint／owning-decoder SHA、train/eval cache identity与normalization source只能写入新 run 的 `experiment_contract.json`，本页不手抄mutable hash。

### 2.2 Human teacher owner

- exact v9 teacher：`v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727` 的 Human EMA `105K`；
- topology：ViMoGen-light Human128 shifted flow；
- Stage2 Camera开始前strict加载进同一Unified实现；
- Camera训练期间 `requires_grad=false`、stop-gradient、无Human optimizer group；
- 每个checkpoint执行固定noise Direct-H exact regression。

不得复用v10 Phase-A Human teacher：其owner、raw cache与train-only statistics与v9不等价。

### 2.3 Cache contract

- exact true-length v9 cache `[N,192,75]`；
- Human128与Camera64分别使用v9 exact train-only z-score和full-covariance whitening；
- eval只复用train statistics；
- interaction16与camera48必须分别记录inverse-normalized residual统计，但第一版不拆head、不改loss权重；
- temporal causal tokenizer在cache build、train、load和eval全部fail-close。

## 3. 活动三模式与诊断模式

| mode | Human source | Camera source／condition | v11角色 |
| --- | --- | --- | --- |
| Direct-H | Human text → Human128 | none | 活动gate；沿用frozen teacher |
| Direct-C | dataset GT Human128 | Camera text + `GT_H_CONDITION` | 活动gate与Camera correctness anchor |
| formal joint sequential | Human text → complete Human128 | Camera text + `TEACHER_FINAL_H_CONDITION` | 活动gate；v11唯一formal joint |

> [!important] joint-parallel的边界
> v11明确移除evolving-H parallel denoising，不把它当成待优化目标。训练、short screen、formal evaluation与promotion table都不得创建joint-parallel row。只有用户以后单独授权“重新打开parallel solver axis”，才允许另建diagnostic run；历史parallel结果保持原身份，不回写为sequential证据。

## 4. CFG 合同

### 4.1 Human CFG

- Direct-H独立报告Human CFG `1`与`3`的既有teacher能力；
- v11 Camera训练的TEACHER_FINAL_H_CONDITION cache与formal sequential joint首个baseline固定Human CFG `1`；
- Direct-C读取GT Human，没有Human CFG；
- 只有CFG1下Direct-C与formal sequential joint均形成稳定baseline后，才允许建立matched CFG3 teacher-final cache与CFG3 joint screen；
- CFG1／CFG3 cache保存独立seed、ordered IDs、Human checkpoint和sampler identity，禁止静默替换。

选择CFG1作为首个Camera合同不是声称它全指标优于CFG3，而是为了让teacher-final train context与formal sequential inference先闭合在同一support内，并减少geometry放大。

### 4.2 Camera CFG

第一轮四臂只调用一个fully-conditional Camera velocity：

$$
v_C^{cond}(x_C,t\mid H_{fixed},c_C).
$$

不再把它记作`v_{11}`，也不构造Camera的`v_{00}`／`v_{10}`／`v_{01}`分支。四位下标原本只表示同一个Camera forward内Camera text与Human context是否存在；Human teacher是另一条flow，所以sequential Human→Camera并不等于Camera内部的`v_{10}`再接`v_{01}`。稳定baseline后若另行授权Camera-text CFG，才在固定Human条件下比较fully-conditional与Human-only Camera velocity；第一轮不做该实验。

## 5. Human context 与 reliability

### 5.1 v11核心训练route

v11主Camera flow只使用两种fixed-H source：

| route | context | reliability `q_h` | 对应能力 |
| --- | --- | ---: | --- |
| GT_H_CONDITION | dataset GT Human128，stop-gradient | 1 | Direct-C |
| TEACHER_FINAL_H_CONDITION | frozen Human CFG1 sampler的完整endpoint，stop-gradient | 1 | formal sequential joint |

两个核心route都读取完整且固定的Human latent，首版 `q_h=1`。不引入连续confidence scalar，也不直接缩放Human tensor。route/source identity显式进入Camera branch，使Direct-C与sequential joint可以共享Camera weights而不把GT/generated source伪装成同一分布。

### 5.2 暂不进入核心objective的route

- `TF_INTERMEDIATE_H`：noisy-GT上的单步conditional predicted-clean，只作near-manifold mechanism probe；
- `ROLLOUT_INTERMEDIATE_H`：parallel evolving-H solver所需的intermediate context；v11禁用。

这两路不是v11 Camera objective的一部分。不得默认恢复v10的 `64/40/12/12`，也不得用intermediate-route curriculum重新引入parallel instability。若GT-H与teacher-final-H之间仍有negative transfer，先调整两route比例、source embedding或C0 warm-start anchor，不增加intermediate route。

## 6. 训练矩阵与执行合同

### 6.1 Stage H：Direct-H owner固化

该阶段不重训，直接strict-transfer已闭合的v9 Human teacher `105K`：

- materialize exact Human EMA；
- 保存teacher boundary；
- 冻结全部Human参数；
- 复现fixed-noise Direct-H与既有N=512 identity；
- Camera branch fresh初始化。

这对应用户所说“先独立完成Direct-H”，但不重复消耗Human训练预算。

### 6.2 固定超参数

- 四臂统一LR `1e-4`，取消`5e-5／1e-4` LR screen；
- 四臂都从同一fresh Camera initialization开始，不继承旧Camera specialist、C0或C1权重；
- 每臂首轮预算都是`30K` optimizer steps；
- micro／effective batch固定`128/128`，bf16、AdamW、同一seed与batch／noise／dropout trace；
- Human与owning decoder参数冻结，但GEO arm保留owning decoder到Camera latent的可导路径；
- 第一轮只调用fully-conditional Camera velocity，不训练或评测Camera CFG分支。

### 6.3 Stage C0：LAT／GEO并行GT-H reference

| arm | objective | training context | budget | device |
| --- | --- | --- | ---: | --- |
| C0-LAT | `L_flow` | `GT_H_CONDITION` only | `30K` | 5090 GPU2 |
| C0-GEO | `L_flow + lambda_geo L_geo^S1` | `GT_H_CONDITION` only | `30K` | 5090 GPU3 |

C0回答：在GT Human条件下，Camera64是否可生成；GEO是否相对LAT改善decoded Camera且不牺牲semantic／coverage／optimization stability。C0不再是C1的前置gate，两行与C1两行同时启动。

### 6.4 Stage C1：LAT／GEO并行GT-H + teacher-final-H主臂

C1-LAT与C1-GEO分别与对应C0 objective使用相同fresh Camera initialization、LR、batch／noise／dropout trace与objective；不能继承C0能力。

每个Camera step：

```text
64 GT_H_CONDITION examples            -> mean L_gt
64 TEACHER_FINAL_H_CONDITION examples -> mean L_final
L_camera = 0.5 L_gt + 0.5 L_final
one backward -> one clip -> one optimizer step -> one EMA update
```

C1-LAT对两route都使用 `L_flow`；C1-GEO对两route都使用相同的 `L_flow + lambda_geo L_geo^S1`。Human永久冻结。两route每一步都出现，从结构上消除v9的route absence，同时只覆盖v11活动的Direct-C与formal sequential joint。

| arm | objective | training context | budget | device |
| --- | --- | --- | ---: | --- |
| C1-LAT | `L_flow` | `64 GT_H + 64 TEACHER_FINAL_H` | `30K` | 4090 GPU0 |
| C1-GEO | `L_flow + lambda_geo L_geo^S1` | `64 GT_H + 64 TEACHER_FINAL_H` | `30K` | 4090 GPU1 |

这四行构成一个同时启动的`2 objectives × 2 context schedules`矩阵，不是“C0通过后才允许C1”的阶段curriculum。5090与4090的分配是执行资源边界，不是研究变量；四臂必须锁定代码、环境、precision与deterministic trace。若结论接近噪声或出现仅随GPU型号分组的异常，需交换GPU复验，不能直接归因于context或objective。

解释：

- C0-LAT与C0-GEO都差：30K后再查Camera64／normalization／flow与decoder sensitivity；
- C0好、对应C1 Direct-C差：same-step teacher-final negative transfer；才进入route ratio或anchor loss；
- C1 Direct-C好、formal sequential差：teacher-final support、Camera text／Human condition接口或decode传播问题；
- LAT好、GEO差：geo dose／decoded Jacobian或multi-objective optimization问题；
- GEO好、LAT差：decoded geometry supervision有直接增益，但仍需semantic／coverage non-regression；
- 两臂均好：按Pareto保留一个或两个full continuation，不默认GEO胜出。

四臂先各自训练到`30K`再作矩阵裁决。只有获得新授权的候选arm才从其选中checkpoint续到更长预算；不默认C1、GEO或`30K` final胜出。

### 6.5 checkpoint保存合同

- 每`1K`原子覆盖一个完整`latest` resume state：raw model、EMA、optimizer、scheduler、scaler、RNG与dataloader cursor；
- 每`1K`另存immutable weights-only raw／EMA snapshot，便于定位sharp onset而不复制optimizer moments；
- `5K／10K／15K／20K／25K／30K`保存immutable full resume checkpoint；
- 每`5K`运行相同ordered first-128 Direct-C与formal sequential evaluation；异常gradient onset前后额外保留full checkpoint；
- 所有checkpoint记录step、arm、device UUID、parent／cache／stats hashes与code SHA；
- endpoint按latent、semantic、coverage与decoded geometry Pareto选择，不默认`30K`。

### 6.6 Stage C2：有条件的低LR适配，不是默认阶段

若某个C0 objective arm好而对应C1从scratch出现明确negative transfer，才授权warm-start rescue：

1. 从matched C0 EMA materialize Camera weights；
2. fresh AdamW moments与fresh EMA；
3. Human继续永久冻结；
4. 使用低于C0胜出LR的matched screen；
5. 每一步仍保留GT_H_CONDITION replay，禁止teacher-final-only区间；
6. 若OBS能力仍回退，再单独测试frozen-C0 velocity distillation／trust-region anchor。

该阶段只更新Camera，不允许“小LR同时更新H/C”。显式保真loss是negative-transfer发生后的独立arm，不与LAT/GEO首次比较绑定。

## 7. 失败后才触发的representation与oracle诊断

这些检查不再是四臂启动前提，也不阻塞四个`30K` run。只有矩阵结果指向representation／decode问题时，才按最小充分集合触发：

1. exact checkpoint／owning decoder／cache／normalization identity；
2. true-length Stage1 Human与Camera reconstruction；
3. Camera64 covariance spectrum、condition number、whitening residual、per-channel tail与temporal spectrum；
4. owning decoder对interaction16、camera48各自扰动的JVP／Jacobian sensitivity；
5. 已有P4 native component oracle：Camera48为decoded center／rotation主误差源，interaction16为互补而非主bottleneck。

需要归因generated-final传播时，才在同一ordered first-128上建立四项decode decomposition：

| Human latent | Camera64 | 解释边界 |
| --- | --- | --- |
| GT-H | GT-C64 | Stage1／decoder floor |
| GT-H | generated-C64 | Camera flow本体误差 |
| generated-H | GT-C64 | Human context／decoder传播误差；该cross-pair是mechanism diagnostic |
| generated-H | generated-C64 | 完整joint结果 |

因为v9 Camera64含interaction16且owning decoder读取full192D，`generated-H + GT-C64`不是自然训练pair，只能做误差传播diagnostic，不能当formal生成mode。所有world Camera结论必须同时报告GT-H anchor与joint-center两种reference。

## 8. loss策略

### 8.1 LAT arm

$$
L_{LAT}=L_{flow}.
$$

它提供Camera flow vector field的直接监督，是v11最低复杂度baseline。

### 8.2 GEO arm

$$
L_{GEO}=L_{flow}+\lambda_{geo}L_{geo}^{S1}.
$$

GEO沿用v9 Stage1 Camera objective的内部相对比例：

$$
L_{geo}^{S1}=L_{camera14\_recon}+L_{camera14\_temporal}+0.1L_{framing}.
$$

predicted-clean Camera64先逆whitening／z-score，与fixed Human128拼接后通过frozen owning decoder；Camera14 reconstruction、temporal difference与derived framing均按true length计算。v9 Stage1的`1e-4 interaction-energy`是latent regularizer而非geometry项，不能直接施加到生成的interaction16，故不纳入GEO。center／rotation／acceleration继续作为评测指标，不擅自改写成Stage1从未使用的训练项。

Stage1没有`L_flow`，因此不存在可直接抄写的全局`lambda_geo`。v11只做一次无optimizer的固定batch calibration：保持上述`1:1:0.1`内部比例，令初始化时Camera branch上的`lambda_geo ||grad L_geo^S1||`与`||grad L_flow||`同量级，并将得到的单一`lambda_geo`冻结到C0-GEO与C1-GEO两个30K arm。不得按结果事后调权；calibration batch、norm与最终数值写入两个run contract。

不运行geo-only arm：没有 `L_flow` 时会同时移除flow velocity target，无法把结果归因于geometry auxiliary。

### 8.3 DC3D边界

v11不使用DC3D的representation、network、loss、CFG、data processing、post-processing或论证。历史v9 DC3D controls继续保留原provenance，但不为v11提供设计依据。若未来出现必须借鉴DC3D才能回答的新缺口，先向用户提交独立提案并获得明确同意，再修改本合同。

## 9. CFG、velocity与gradient冲突的分离诊断

| 问题 | 最小probe | 不能据此宣称 |
| --- | --- | --- |
| CFG direction conflict | 第一轮不测；稳定baseline后才在fixed-H下比较fully-conditional与Human-only Camera velocity | inference sweep修好了training |
| conditional velocity conflict | 同Camera state／noise／text，替换GT-H与teacher-final-H context并比较velocity field | 参数梯度必然冲突 |
| route gradient conflict | matched batch计算 `g_gt,g_final` norm／cosine及layerwise贡献 | 正cosine代表长期optimizer健康 |
| curriculum／negative transfer | 两route持续有exposure时比较fixed-EMA loss和decoded checkpoint trajectory | 任何单route回退都叫轮转遗忘 |
| optimizer instability | preclip grad、clip fraction、update norm、raw／EMA gap与non-finite guard | clip后finite代表训练健康 |

若一个route在持续有exposure时改善、另一个持续退化，应称为 **same-step negative transfer**；只有route长时间缺席后回退才称curriculum forgetting。

## 10. `30K`矩阵裁决

### 10.1 C0 GT-H generatability comparison

- first-128、fixed ordered IDs／Camera noise／Euler50／GT-H context；
- C0-LAT／GEO使用同一LR `1e-4`、initial weights与input trace；
- 同时看latent fixed loss、FDCLaTr／CLaTr／coverage／caption、Camera ADE/FDE／rotation、projective Out、zero-visible、velocity／acceleration；
- practical threshold从固定集重复评测、paired bootstrap或历史checkpoint噪声估计，不预写通用 `10%`／`5%` 数字。

C0-LAT与C0-GEO都不通过时不阻止已经并行完成的C1，但长程continuation停止，并按第7节触发最小representation／decoder诊断。

### 10.2 C1 sequential multi-route gate

- first-128 Direct-C与formal sequential joint；不产生joint-parallel row；
- Direct-H exact max-abs必须为 `0.0`；
- C1-LAT／GEO各自与matched C0 objective reference比较，判断teacher-final exposure的收益或negative transfer；
- LAT与GEO比较只归因于decoded geometry auxiliary；
- 连续两个fixed window同时出现loss反转、raw／EMA gap扩大或异常gradient onset时guard stop并保留现场。

四臂`30K`闭合后才选continuation；候选endpoint再做first-512 confirmation。正式promotion仍需pure-test audited contract和三模式共同报告。

### 10.3 后续条件分支

| observation | next action |
| --- | --- |
| C0-LAT／GEO都差 | 触发Camera64、normalization、flow capacity与decoder sensitivity后验诊断 |
| C0好、matched C1 Direct-C差 | 调OBS／FINAL比例或C0 warm-start低LR rescue；Human不解冻 |
| Direct-C好、formal sequential差 | 查generated-final Human distribution、source interface与decoder propagation |
| LAT好、GEO差 | 查geo dose、decoder Jacobian与multi-objective instability |
| GEO好、LAT差 | 确认semantic／coverage non-regression后保留GEO |
| CFG1三模式稳定 | 才讨论Camera CFG与Human CFG3 teacher-final support |

### 10.4 `30K` first-512 audited verdict（2026-07-30）

四臂均完成`30K`；`5K→30K` first-128轨迹未触发guard，故按预注册选择各臂EMA `30K`进入first-512 confirmation。正式审计固定ordered-ID SHA-256 `6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df`、Euler50、CFG1、seed17、eval batch32；只评测Direct-C与formal sequential Human→Camera，`joint_parallel=false`，四臂均为non-causal。精确数值与artifact identity只见[[StoryMotion-valid-metric-ledger#3.9 v11 four-arm 30K first-512 audited confirmation]]。

| causal comparison | audited observation | decision |
| --- | --- | --- |
| C0-LAT vs C0-GEO | GEO在Direct-C与sequential的Camera ADE／FDE／rotation均有小幅下降趋势，但六个paired 95% CI全部跨零；同时LAT的CLaTr、coverage、retrieval与多数framing字段更平衡 | 2026-07-30 `30K`当时选择LAT诊断端点；已被第10.8节共同mainline selection覆盖 |
| C1-LAT vs C0-LAT | C1 Direct-C ADE／FDE／rotation分别恶化`+0.3056 m / +0.3072 m / +8.019°`，95% CI均不跨零；Direct-C与sequential semantic／coverage／framing同时回退 | 不支持`64 GT + 64 teacher-final` same-step schedule；C1-LAT停止 |
| C1-GEO vs C0-GEO | C1 Direct-C ADE／FDE／rotation分别恶化`+0.3639 m / +0.3528 m / +8.305°`，95% CI均不跨零；sequential geometry变化不确定且semantic／framing回退 | C1-GEO停止；GEO未消除mixed-context negative transfer |
| v11 vs历史v9 final | 相同v9 Stage1／decoder owner下，C0 Camera generation显著优于历史v9 final | v9历史Stage2 schedule／endpoint是主要blocker之一；不能反推representation已经可晋升 |
| C0-LAT vs v9 P3L exact Camera-phase30K | Stage1／decoder／teacher／cache／stats／first-512／noise／Euler50全匹配且v9转换forward max-abs为`0.0`。C0-LAT Direct-C除FDCLaTr外的主要字段改善，ADE／FDE／rotation配对CI均不跨零；sequential语义与framing偏C0，geometry偏v9且CI不跨零 | v9精确30K比较可用，故不触发“无法比较才四臂续训”条件；C0-LAT保留诊断端点，但不宣称跨模式支配v9 |

> [!warning] Causal attribution boundary
> C0两臂在5090训练，C1两臂在4090训练，context schedule与训练主机完全混杂。当前结果支持 **schedule-associated same-step teacher-final negative transfer**，但不是干净的单变量因果证明。只有另行授权C0-LAT在4090、C1-LAT在5090的swapped-host replay后，才可把差异严格归因于schedule。

裁决为`stop_all_at_30k_select_c0_lat_diagnostic`：精确v9 Camera-phase30K已在同一评测面闭合，因此用户声明的fallback continuation条件未触发；没有自动`105K` continuation，也不触发Camera CFG、Human CFG3、C2 warm-start、representation／oracle或v10 Stage2。C3-25 exact30K只有不同representation／cache／pure4,053／DDIM／joint-parallel的跨系统formal，不能冒充matched first-512；其aggregate数值不推翻人工观察到的无意义平均生成。若需要schedule因果证明，下一最小实验仍是两臂swapped-host LAT replay，须单独授权。

### 10.5 用户新增四臂 `30K→105K` 授权（2026-07-30）

第10.4节保留当时按条件fallback得到的历史裁决。用户在看到精确v9比较后又显式授权四臂全部补全到`105K`，因此本次执行不再依赖原fallback是否触发。新增授权的边界是：

- 每臂从自己immutable full-state `30K`父断点继续，恢复raw model、Camera EMA、optimizer、constant scheduler、disabled scaler、RNG与dataloader cursor；旧`0→30K` run保持只读；
- 目标统一为Camera optimizer global step `105K`，仍用LR `1e-4`、原objective、原context schedule、batch `128/128`与non-causal合同；
- Human teacher与owning decoder继续冻结；不增加joint loss、joint optimizer phase、Camera CFG、Human CFG3、C2 loss或joint-parallel；
- TensorBoard从真实resume boundary `30K`开始，不回填缺失的`0→30K`；每`1K`保存raw／EMA与latest full resume，每`5K`保存immutable full resume并执行既定first-128 evaluation；
- `105K`只是本轮训练终点，不自动成为promotion endpoint。完成后的Direct-C与formal sequential结果仍须formal audit后才能进入metric ledger与版本结论。

活动step、ETA、worker输出、checkpoint与TensorBoard审计只由各run的manifest／`logs/`／`checkpoints/`拥有，本页不复制实时状态。

### 10.6 `105K` first-512 audited verdict（2026-07-30）

四臂均完成Camera optimizer `105K`。最初的`30K→105K`父run在训练到`35K`后因旧screen schedule只允许到`30K`而fail-close；恢复子run从各自immutable full-state `35K`精确继续到`105K`。父run的真实TensorBoard覆盖`30K→35K`，恢复子run覆盖`35K→105K`；旧`0→30K`缺口未回填。四个EMA `105K`随后在同ordered first-512、Euler50、CFG1、seed17、eval batch32、Direct-C + formal sequential合同下通过跨臂审计，并完成相同fixed-8 cohort的三联visual；`joint_parallel=false`。精确数值与artifact identity只见[[StoryMotion-valid-metric-ledger#3.10 v11 four-arm 105K first-512 audited confirmation]]。

| causal comparison | audited observation | decision |
| --- | --- | --- |
| `30K→105K` C0 maturation | C0两臂的Direct-C与sequential在distribution、semantic、caption、geometry与framing上广泛改善 | `30K`不是Camera endpoint；保留`105K`证据 |
| C0-LAT vs C0-GEO | 两模式共六个paired geometry 95% CI全部跨零；semantic／coverage／retrieval／framing仍是混合Pareto | 2026-07-30 first-512当时保留LAT诊断端点；已被第10.8节共同mainline selection覆盖 |
| C1-LAT vs C0-LAT | C1-LAT的Direct-C semantic局部更强，但Direct-C geometry显著更差，formal sequential在semantic、caption、geometry与framing上回退 | 将旧“广泛negative transfer”结论收窄为Direct-C／sequential route trade-off；C1-LAT不接管系统端点 |
| C1-GEO vs C0-GEO | Direct-C与sequential ADE／FDE显著回退，GEO没有消除mixed-context代价 | C1-GEO停止于`105K` |
| C0 `105K` vs v9 | 共同Direct-C字段上广泛优于v9 exact Camera-phase30K与v9 final Camera-phase105K；v9 final没有当前sequential合同结果 | v9历史Camera schedule／endpoint仍是主要blocker；不伪造v9 final sequential排名 |
| C0 `105K` vs C3-25 canonical512 | C0在FDCLaTr、coverage／density／precision、geometry与framing更好；C3在CLaTr、recall与caption更好 | 跨representation／sampler Pareto；aggregate不替代视觉意义判断，也不自动晋升v11 |

当时裁决为`complete_four_arm_105k_select_c0_lat_diagnostic_keep_c0_geo_pareto`。四臂训练、formal confirmation与fixed-8 visual全部闭合；没有Camera CFG、Human CFG3、C2 warm-start、representation／oracle或parallel solver授权。该first-512决策随后由pure4,053 audit与第10.8节显式selection覆盖；原数字与当时授权边界不回写。v11第三模式仍只能是formal sequential Human→Camera。

### 10.7 `105K` pure4,053 audited verdict（2026-07-30）

用户随后授权四臂完成pure4,053完整评测。四个EMA `105K`在相同ordered 4,053 IDs、official inputs、Euler50、CFG1、seed17与eval batch32上完成Direct-H、Direct-C和formal sequential Human→Camera；`joint_parallel=false`。四臂的contract、checkpoint／cache／stats／decoder、non-causal、artifact SHA及全部MPJPE／trajectory／yaw／Camera geometry／decoded-Human physical字段均通过逐臂审计与10,000次matched-sample bootstrap。精确数值、物理诊断、C3 system boundary与artifact identity只见[[StoryMotion-valid-metric-ledger#3.11 v11 four-arm 105K pure4,053 formal audit]]。

| causal comparison | audited observation | decision |
| --- | --- | --- |
| C0-LAT vs C0-GEO | Direct-C与sequential共六项Camera geometry CI全部跨零；LAT保留更强的coverage／precision／framing连续性，GEO保留局部semantic均值优势 | pure4,053不支持稳健单臂胜者；交由独立selection event决定共同保留 |
| C1-LAT vs C0-LAT | Direct-C ADE／FDE／rotation显著恶化`+0.2631 m / +0.2721 m / +5.3279°`；sequential ADE／FDE也显著恶化 | C1-LAT不作为system endpoint；完整cohort确认route trade-off |
| C1-GEO vs C0-GEO | Direct-C ADE／FDE／rotation显著恶化`+0.2316 m / +0.2426 m / +3.9765°`；sequential ADE／FDE也显著恶化 | GEO不消除teacher-final same-step route代价；C1-GEO停止 |
| C0-LAT vs C3-25 pure4,053 | v11 Direct-H semantic／distribution、root-aligned MPJPE与yaw更好；Direct-C大多数字段及Camera geometry／framing更好，但C3保留CLaTr／recall／caption优势 | 2026-07-30形成replacement candidate；2026-07-31与GEO共同晋升；仍是跨system boundary |
| v11 sequential vs C3 joint-parallel | v11的Human／Camera semantic、coverage与framing广泛更好；Camera paired geometry非常接近且C3略低 | formal solver不同，不写成matched joint支配 |
| decoded-Human physical | v11自由Human的dynamics低于reference，C3多数对应physical fields更接近reference；contact／skate只是heuristic | 保留physical trade-off；不宣称calibrated physical validity已通过 |

pure4,053在2026-07-30的审计裁决为`complete_pure4053_keep_c0_lat_as_promotion_candidate`。本合同的训练、三模式正式评测、物理诊断和跨臂审计均已闭合，不再有缺失eval。当时尚无promotion授权；这一状态已由下一节的独立selection event取代，不需要补跑joint-parallel。

### 10.8 C0-LAT／C0-GEO共同mainline selection（2026-07-31）

用户显式选择C0-LAT与C0-GEO为共同mainline。该事件只改变决策层身份，不修改训练、
checkpoint、contract、result或records：

| selection question | evidence | final decision |
| --- | --- | --- |
| 是否从C0两臂选唯一endpoint | 六项Camera geometry 95% CI全部跨零；semantic／coverage／framing为混合Pareto | 不以raw mean选臂；LAT与GEO并列 |
| 是否满足三模式system boundary | 两臂pure4,053 Direct-H、Direct-C、formal sequential、physical与visual均闭合 | 两臂共同成为v11 mainline |
| C3-25如何处理 | 仍保留部分Camera semantic、joint geometry与Human dynamics优势；solver／representation不同 | 转为former-mainline system baseline，不删除artifact |
| 历史eligibility字段如何处理 | run创建时确为diagnostic授权 | immutable contract原样保留；selection由本节、[[current]]与[[version_family]]拥有 |

共同mainline不授权C1续训、joint-parallel、Camera CFG、v10 Camera Stage2或新Stage1；这些
后续工作只在直接关闭[[StoryMotion-iclr-reliability]]中的论文hard gap时重新授权。

## 11. 运行与审计要求

- 新run使用统一 `runs/train|eval|vis` layout与同一run ID；
- 每个run的exact parent、cache、stats、seed、batch、route exposure、sampler与CFG写入immutable `experiment_contract.json`；
- Stage1 harness、cache audit、bridge smoke与official evaluator全部通过；
- Camera specialist必须是同一Unified checkpoint／branch实现的task slice，或将权重显式transfer并验证；
- 按第6.5节保存每`1K` weights snapshot与latest resume、每`5K` immutable full checkpoint；
- 四臂历史`0→30K`没有TensorBoard event，永久登记为观测缺口，不从JSONL回填或伪造曲线。任何未来fresh／resume训练必须从真实起点／resume boundary写run-local TensorBoard：每`20`步记录loss、flow、geo、route flow、decoded auxiliaries、preclip grad与LR；每`1K` flush后执行event可读性与step单调性fail-close审计。若从历史`30K`续训，首个真实TensorBoard boundary就是`30K`，历史缺口保持显式。
- 后续trainer／contract已把TensorBoard设为required且禁止backfill，同时保留每`1K` raw／EMA weights + atomic latest full resume、每`5K` immutable full resume；full checkpoint必须含model、EMA、optimizer、scheduler、scaler、RNG、dataloader cursor与step。每个续训run的精确实现与合同SHA只由其immutable `experiment_contract.json`拥有。
- 不用单个加权总分选endpoint；Direct-H、Direct-C、formal sequential joint同表且每行有non-empty `version / run`；v11不得产生joint-parallel row；
- screen只属于owning plan与run artifacts；formal audit后才写metric ledger与version finalized event。

## 12. 当前授权与非授权

### 已授权设计边界

1. 复用v9 Stage1／cache／owning decoder与v9 Human teacher；
2. 固定LR `1e-4`，同时启动四个`30K` matrix arms；
3. C0-LAT／GEO使用GT_H_CONDITION-only；
4. C1-LAT／GEO每步使用`64 GT_H + 64 TEACHER_FINAL_H`；
5. GEO内部比例固定为Stage1的`1:1:0.1`，以一次无optimizer gradient calibration冻结全局`lambda_geo`；
6. 按第6.5节保存checkpoint，`30K`后再按Pareto选择是否续训。
7. 在第10.4节审计完成后，用户另行授权四臂各自exact full-state `30K→105K`续训；只延长原Camera schedule，不增加新的训练phase或objective。

原始一次性四臂`0→30K`授权已在第10.4节闭合；第7项是后续独立授权，只覆盖现有四臂续训，不授权新arm。

### 尚未授权

- 切换到v10 Camera48或hybrid Stage1；
- joint阶段更新Human；
- joint-only且不replay Direct-C；
- 训练、评测或gate joint-parallel；
- 默认恢复四route `64/40/12/12`；
- 前置LR screen或以representation／四项oracle阻塞四臂启动；
- PCGrad／CAGrad、adapter、双Camera head；
- Stage1合同之外的center／rotation／acceleration training loss或visibility loss；
- geo-only objective；
- Human CFG3 teacher-final cache或连续随机CFG；
- 第一轮Camera CFG分支或四路velocity sweep；
- 任何DC3D内容；
- 把`105K` final自动当作promotion endpoint，或跳过formal audit直接改写主线；2026-07-31的共同mainline是audit完成后的独立selection event，不是自动晋升。

## 13. Claim boundary

可以写：

- “v11固定v9 Stage1与Human teacher，只测试Stage2 Camera training／routing／CFG／objective。”
- “v9 Stage1 reconstruction已闭合，但Camera64 Stage2 generatability仍需C0 GT-H两臂验证。”
- “C0与C1同时启动，组成objective × context schedule的四臂30K矩阵；C0不是C1的前置gate。”
- “Human CFG1是首个matched Camera context合同，不代表CFG1全指标支配CFG3。”
- “Camera对GT-H与teacher-final-H都读取fixed observed context；两者差别是Human source，不是Camera是否能看见Human。”
- “LAT与GEO都保留flow velocity objective；GEO内部使用v9 Stage1 Camera的`1:1:0.1`比例，并以固定batch校准全局lambda。”
- “四臂`105K`、pure4,053 formal与fixed-8 visual均已闭合；C0-LAT与C0-GEO是共同mainline。”
- “C0-GEO相对C0-LAT的两模式paired geometry 95% CI全部跨零，不能宣称稳定净增益。”
- “C1在Direct-C semantic与formal sequential／geometry之间呈现schedule-associated route trade-off；训练主机混杂仍阻止严格单变量归因。”
- “同一v9 Stage1／decoder owner在v11 C0下可以生成明显更健康的Camera，说明历史v9 Stage2 schedule／endpoint是主要blocker之一。”
- “C0 `105K`在共同Direct-C字段上广泛优于v9 P3L exact Camera-phase30K与v9 final Camera-phase105K；v9 final没有当前sequential合同结果。”
- “四臂前30K没有TensorBoard；真实续训event由`30K→35K`父run与`35K→105K`恢复子run共同覆盖，历史曲线没有回填。”

不能写：

- “v10 Stage2已被v9击败”或“v10 Camera48已经失败”；
- “v9 Stage1可以直接产出v10 independent Camera48”；
- “observed-H Camera completion就是joint generation”；
- “joint小LR更新Human仍属于protected-H”；
- “v11 formal joint必须或已经使用joint-parallel”；
- “same-step训练天然不会negative transfer”；
- “正gradient cosine排除了velocity／CFG冲突”；
- “sequential H→C等于Camera内部先运行`v10`再运行`v01`”；
- “v11使用或依赖DC3D内容”；
- “GEO是geo-only而不需要flow velocity监督”；
- “Stage1 reconstruction通过等于Stage2 Camera可生成”；
- “v11在matched单变量意义上全面支配C3-25”；二者只能作system boundary比较。
- “C1回退已经严格证明由teacher-final schedule单独造成”；C0／C1与5090／4090完全混杂。
- “C0-LAT通过等于v9 representation已获promotion资格”或“v11整体优于C3-25”；cohort／sampler／formal joint mode与证据等级不等价。
- “C0-LAT在Direct-C改善等于它在sequential整体支配v9”，或“C3-25 pure4,053 DDIM joint-parallel是v11 first-512 Euler sequential的公平对照”。
