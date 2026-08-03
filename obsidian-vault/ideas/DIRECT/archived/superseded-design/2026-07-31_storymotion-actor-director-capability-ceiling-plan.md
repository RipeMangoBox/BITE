---
title: "StoryMotion Actor–Director Capability Ceiling Plan"
hypothesis: |
  Pulp-only联合latent不能继续承担StoryMotion的能力上限。更有希望且更简洁的路线是：
  将高质量Human generation作为可替换Actor provider；将Camera建模为text-owned
  semantic program、Human-dependent event alignment与bounded actor-conditioned Camera
  residual组成的连续3D planner；Joint默认Actor→Director，并仅在无训练oracle证明必要时
  开启preservation-gated selection／staging。editing最后作为独立课程学习。
status: archived_merged
tags:
  - StoryMotion
  - DIRECT
  - capability
  - scaling
  - Actor-Director
  - ICLR
  - ICLR/2027
  - status/archived
source_notes:
  - "[[DIRECT/current]]"
  - "[[StoryMotion-iclr-reliability]]"
  - "[[2026-07-31_storymotion-v11-actor-director-counterfactual-control]]"
  - "[[2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]"
  - "[[2026-07-31_storymotion-v11-human-temporal-locality-control]]"
  - "[[2026-08-01_storymotion-multipair-data-training-plan]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
  - "[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]"
source_papers:
  - "[[analysis/ICLR_2026/The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation]]"
  - "[[analysis/ICML_2025/Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion]]"
  - "[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/Uni3C_Unifying_Precisely_3D-Enhanced_Camera_and_Human_Motion_Controls_for_Video_Generation]]"
created: 2026-07-31T19:30:00+08:00
updated: 2026-08-03T14:30:39+08:00
---

# StoryMotion Actor–Director Capability Ceiling Plan

> [!warning] 已合并归档
> 本页在2026-08-01完整合并入
> [[2026-08-01_storymotion-multipair-data-training-plan]]，只保留为历史快照，不再拥有
> live hypothesis、实验顺序或结论。后续修改只进入合并后的唯一owner。

> [!important] 总判断
> 继续在Pulp上增加C0训练步数、MAE预算或Stage1内部部件，不会解决能力上限。
> Human上限主要由数据／外部先验决定；Camera上限同时受Pulp单配对可识别性、Director
> intent ownership、human-relative连续规划与反事实Human鲁棒性约束；Joint上限是
> 两者的级联、pair support及误差传播。
> 三条轴必须分开提升和归因，不能再用一个“统一三模式”均值掩盖。

本页历史上记录下一阶段的能力分解、架构选择、实验顺序与停止条件；当前owner已改为
[[2026-08-01_storymotion-multipair-data-training-plan]]。正式数字只进入
[[StoryMotion-valid-metric-ledger]]；反事实screen数字只见
[[2026-07-31_storymotion-v11-actor-director-counterfactual-control]]；Camera temporal
editing的representation stop只见
[[2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]；Human128 feature／world
endpoint分解只见[[2026-07-31_storymotion-v11-human-temporal-locality-control]]。

## 1. 从“统一三模式”改为Actor–Director系统

### 1.1 准确任务定义

1. **Actor／Human generation**：Human instruction → 3D Human motion。
2. **Director／human-centric Camera planning**：final／observed 3D Human motion与
   Camera instruction → continuous 6-DoF Camera trajectory。
3. **Composition／joint Human–Camera generation**：先生成Actor，再执行Director。

第三项是前两项的有向组合，不是第三个对称生成器。Direct-C是Director在observed
Human上的独立接口；sequential是Director在generated Human上的系统接口。继续禁止
evolving-H joint parallel。

### 1.2 目标论文主张

只有下述证据全部关闭后，目标主张才可写为：

> StoryMotion is a language-directed Actor–Director planner that generates an
> explicit 3D performance and a dense human-reactive camera trajectory from
> independently editable actor and cinematography instructions, providing
> reusable control signals for downstream video generators.

当前paper-safe版本必须更弱：StoryMotion支持Human generation、observed-H Camera
completion与sequential Human→Camera generation；独立双文本控制只完成screen-level
响应，尚未关闭Actor replacement后的Camera instruction robustness。

## 2. 竞品边界与真正值得打的软肋

- [Uni3C](https://alibaba-damo-academy.github.io/Uni3C/)与
  [ActCam](https://arxiv.org/abs/2605.06667)已经能把**给定**Human／Camera控制送入
  Video Generation。StoryMotion不能声称ViGen没有联合控制。
- [Auteur](https://arxiv.org/abs/2606.01900)已经把自然语言与粗Human motion转换为
  human-relative Camera DSL并输出连续6-DoF轨迹，是最直接的Camera planner竞品。
- StoryMotion若要形成必要性，必须在Auteur式sparse DSL之外证明至少一项真实差异：
  dense reactive Camera、独立Actor／Director counterfactual editing、连续复杂运镜，
  或输出可以无缝驱动Uni3C／ActCam／ViMoGen类下游而不牺牲主体可见与文本意图。

因此核心问题不是“能否连接ViMoGen做Demo”，而是**是否生成了下游本身无法从文本
可靠规划的3D控制信号**。连接ViGen只验证接口；Actor–Director counterfactual与
human-reactive planning才验证方法价值。

## 3. 三种模式的独立能力上限

| mode | 当前硬上限 | 最有价值的upper-bound probe | 允许的首个干预 | stop条件 |
| --- | --- | --- | --- | --- |
| Actor／Human | Pulp规模与动作／文本质量；当前“ViMoGen-light”仍是Pulp-only clean-room backbone | 官方ViMoGen／Kimodo provider在原生benchmark与StoryMotion adapter后的sealed OOD质量 | 冻结外部provider，先做representation adapter与Camera compatibility；不先微调 | 外部provider原生优势在adapter后消失，且问题定位为不可逆topology／coordinate loss |
| Director／Camera | Camera text与Human context在同一Transformer中竞争；counterfactual Human造成Camera intent长尾漂移 | text-owned semantic program、Human event alignment、full-H／coarse-H与Auteur matched task | 分离program owner与bounded actor-conditioned Camera residual；只训Camera | 不能同时改善tail control、visibility、articulation-aware event与parent Direct-C replay |
| Composition／Joint | Actor误差进入Director；Pulp只提供paired factual context | 2×2 Actor／Director反事实矩阵与provider swap matrix | Human final后单向执行Director；source identity显式 | 需要joint-parallel或隐藏provider／decoder差异才能成立 |

## 4. Actor：停止Pulp-only“加步数”，接入真正的上限

### 4.1 证据

ViMoGen用228K motion data、ViGen prior与MBench专门解决generalization；Being-M0的
数据消融显示百万级数据显著抬高OOD retrieval。2026-07-31时，官方
[ViMoGen仓库](https://github.com/MotrixLab/ViMoGen)已发布pretrained weights、
ViMoGen-228K与MBench；[Kimodo](https://github.com/nv-tlabs/kimodo)也提供大规模
optical-MoCap预训练模型与约束式authoring接口。继续把本地Pulp-only
`ViMoGen-light`称为ViMoGen上限是不准确的。

### 4.2 最小Provider ABI

下一架构不再要求所有Human provider复用`Human128` latent：

```text
HumanProvider.generate(
    actor_text, duration, seed, optional_constraints
) -> {
    joints_or_smplx,
    root_frame,
    fps,
    valid,
    provider_identity,
    native_artifact_hash
}
```

StoryMotion只新增一个可审计的canonicalization adapter，把provider输出转换为统一
world Human joints／root frame；Camera planner读取显式Human sequence，而不是读取
只有v9 Stage1能产生的私有Human latent。这样可以：

- 真实继承外部Human能力，而不是让外部动作再经过Pulp-only Human encoder损失上限；
- 把Actor provider升级与Director改进分离；
- 让Direct-H指标诚实归属provider，让StoryMotion贡献归属Director与composition。

### 4.3 Provider ladder

1. **原生上限确认。** 固定官方revision／weights／license，在官方MBench或原生测试上
   复现；未复现前不接StoryMotion。
2. **无损adapter检查。** 对同一motion做native render与canonical render，检查root、
   heading、bone length、duration与fps；任何隐式retargeting都单独报告。
3. **Director compatibility。** 先不训练，给现有Camera planner读取canonical Human
   的最小adapter；只判断接口损失与分布移位，不把结果冒充新mainline。
4. **Provider matrix。** 至少比较当前v9 teacher、官方ViMoGen与一个大规模MoCap
   provider；同Actor prompts、duration、seed与Camera text，逐行标provider／adapter。

如果官方provider权重或许可证不允许目标用法，则退回ViMoGen-228K数据蒸馏／adapter
训练；不以名字相似的Pulp-only backbone代替。

### 4.4 P0 source preflight（已完成）

2026-07-31只完成**源码与合同冻结**，没有下载模型权重，也没有把任何外部输出写入
StoryMotion cache／checkpoint：

- ViMoGen冻结为官方revision `bf891dea867c19b99a099e520705e3f9fa0856ec`，只读源码
  位于`StoryMotion-external-controls/20260726/ViMoGen_bf891dea`；源码归档SHA-256为
  `34e892fe0a21911811cbc320b080fddbd150c4a92fcd813bc9cd29e906398802`。仓库当前
  没有可识别的code license；ViMoGen-228K dataset card标为
  Apache-2.0，但Google Drive权重的独立使用条款尚未解析。因此不授权官方权重推理，
  也不把Pulp-only `ViMoGen-light`冒充官方上限。
- Kimodo冻结为官方revision `1aece8c124d73d255ceff5086d983b844c9f4e94`，只读源码
  位于`StoryMotion-external-controls/20260731/Kimodo_1aece8c`；源码归档SHA-256为
  `8b24e1a2163e9ce5772ab425df773ea0a5b5ba42eedc778ce84f7a6783aa9a89`，
  `LICENSE` SHA-256为
  `d1a7d615ab8eff4de143b1456f46dabf232f54daf0fcf9a70442bb6f637a9e95`。
  code是Apache-2.0；首选能力上限候选是`Kimodo-SOMA-RP-v1.1`（700小时Rigplay，
  NVIDIA Open Model），公开数据对照是`Kimodo-SOMA-SEED-v1.1`（288小时
  BONES-SEED）。不选R&D-only的`Kimodo-SMPLX-RP-v1`作为首个provider。
- 精确源码检查确认Kimodo motion denoiser使用无causal mask的
  `torch.nn.TransformerEncoder`，text encoder也显式双向；原生NPZ至少输出
  `posed_joints[T,J,3]`、`root_positions[T,3]`与
  `global_root_heading[T,2]`。这些字段足以定义adapter输入，但SOMA→StoryMotion
  topology／root／heading映射仍必须由真实样本验证，不能从shape推定“无损”。

下一步只有在作者确认模型条款并授权权重下载后，才为
`Kimodo-SOMA-RP-v1.1`建立N32原生／canonical成对artifact。adapter必须读取原生NPZ，
显式记录model revision、weight hash、seed、fps、source artifact hash和
`is_causal=false`；它不得构建或消费StoryMotion Stage1 cache。P0在该N32检查通过前
仍是`in_progress`。

## 5. Director：建立Camera instruction owner

### 5.1 从screen失败反推架构

当前Camera network同时交叉注意Camera text与full Human context。反事实screen证明
Camera会随Human强烈变化，但约四成样本无法守住预声明的fixed-Camera-text margin。
这意味着“会反应”不等于“按同一导演意图反应”。

源码审计进一步排除了一个诱人的伪oracle：当前`CameraFlowBlock`在每层依次执行
Camera-text attention与Human attention，而v11合同把`camera_text_drop_prob`和
`human_context_drop_prob`都固定为`0.0`。虽然实现保留
`force_human_context_unconditional`开关，但对应`null_human`在该训练合同下没有
得到有效训练信号。因此不能用`full(H)-null(H)`事后声称已分离Human residual，也不能
把未训练null-Human路径的结果作为text-only upper bound。

建议的最小vNext分解为：

```text
Semantic program:  P_sem = G_T(camera_text)
Event alignment:   A = G_A(final_human, P_sem)
Camera execution:  C = G_E(final_human, P_sem, A, camera_style_noise)
```

- `G_T`是Camera instruction owner，不读取Human；它拥有shot type、方向、framing style与
  “在转身完成时推近”这类事件语义，但不臆测事件绝对帧号。
- `G_A`只读取final Human以定位事件时间，不重新解释Camera intent。
- `G_E`负责主体相对构图、visibility、world 6-DoF与style variation；actor-conditioned
  Camera residual零初始化且有界，不允许任意改写全部Camera latent。
- Compose优先在human-relative `SE(3)`或screen-space framing变量中执行，再解析为world
  6-DoF。整个结构命名为**text-owned program + bounded actor-conditioned Camera
  residual**，不称“Human residual”。

训练顺序也必须体现owner：先训练`G_T`并冻结，再训练`G_A`与`G_E`吸收Human event与
relative geometry；第二阶段持续replay第一阶段program。residual关闭必须exact复现
**已训练program／base contract**，而不是假装exact复现当前interleaved parent。
当前v11只作为matched parent replay与distillation reference。

这比再加一个framing sidecar更强：此前framing adapter只增加条件，没有建立Camera
text owner，formal结果已经证明“能响应control但整体质量退化”不可接受。

### 5.2 反事实训练数据

完整multi-pair数据、manifest、split、solver验证与data×architecture factorial由
[[2026-08-01_storymotion-multipair-data-training-plan]]独占。本节只保留Director架构对
反事实数据的最低要求。Pulp factual pair不能单独训练Actor replacement；直接shuffle
world Camera也不是合法positive。

Pulp factual pair不足以训练Actor replacement。先做可逆的pseudo-pair oracle：

1. 对同长度Human target／donor计算每帧root frame `F_H`与`F_H'`；
2. 从原Camera `F_C`得到human-relative transform `R=F_H^{-1}F_C`；
3. 构造transported Camera `F_C'=F_H'R`，再检查projection／visibility／smoothness；
4. 只对语义上允许equivariant transport的Camera caption strata使用。world-static、
   absolute truck／dolly等不满足该假设的文本必须隔离，不能静默混入；
5. caption–motion pair按reason code quarantine，不删除原motion，保留parent manifest。

如果transport oracle不能保持Camera语义与视觉几何，就不训练该augmentation。第二种
候选是冻结CLaTr／framing evaluator做counterfactual predicted-clean auxiliary，但必须
先做endpoint oracle排除metric hacking，并用parent replay与visual blind gate约束。

### 5.3 Director success criteria

- 原／编辑Camera文本的factorial CLaTr或Auteur framing score 95%下界均大于`0`；
- Actor replacement后fixed-Camera-text noninferiority关闭，并单独报告tail failure rate；
- Human exact owner、Camera adaptation、visibility、smoothness与parent Direct-C replay
  同时通过；
- 与Auteur做matched输入／输出／prompt taxonomy比较；与Uni3C／ActCam只比较下游
  control utility，不把planner与renderer混排。

## 6. Joint：只报告组合质量与误差传播

Joint formal protocol固定为：

```text
actor_text -> final Human from named provider
final Human + director_text -> Camera plan
Human + Camera -> optional downstream ViGen renderer
```

至少报告四个矩阵：

1. GT Human + target Director；
2. generated Human + target Director；
3. GT／fixed Human + edited Director；
4. edited Actor + fixed Director。

每个row必须写provider、Camera endpoint、Stage1／decoder、run与sampler。只有这样，
“Human变好是否抬高Joint上限”和“Director是否吞掉Actor收益”才可归因。下游ViGen
Demo同时保留输入3D control与rendered video，不能用视频观感替代3D planner指标。

## 7. Stage1简化：从论文主线移出，再做matched替换

### 7.1 当前投稿策略

v11的`human128 + interaction16 + camera48`与636K三阶段schedule暂时只作为
failure-driven backbone，不把每个部件写成贡献。v10同时改变representation、loss、
phase与Stage2完成度，不能作为“简单设计失败”的matched证据。

### 7.2 vNext最简目标

Actor provider输出显式Human；Director直接生成或局部编码Camera plan。优先级为：

1. 移除Human必须经过joint Stage1的要求；
2. 移除`interaction16`作为共享隐变量，把interaction改成Director residual的显式职责；
3. Camera使用absolute center／rotation或segment-anchor + local residual，避免velocity
   integration让局部latent edit永久漂移后续world center；
4. decoder保持non-causal，但表示必须通过decoded locality probe；若可直接生成
   Camera14／6-DoF，则不再为Camera引入单用AE。

简化实验必须固定data、text encoder、Camera objective、parameter budget、sampler、seed
与formal evaluator；只改变representation owner。至少比较：当前v11 owner、无
`interaction16`显式Human-conditioned Camera、direct/local Camera representation。
未完成matched端到端实验前，只能称design target，不能称已经简化成功。

## 8. Editing：不能用MAE掩盖generation ceiling

MAE从pretrained C0初始化，因此只学习“如何利用／重定向C0 prior”；它不能证明C0
的unconditional或conditional support扩大。generation与editing必须分表、分checkpoint、
分claim。

当前Camera inpainting已给出更硬的negative evidence：已知Camera64在mask外逐位
`0.0`仍不足以保护decoded world Camera center；endpoint oracle也未通过locality gate。
因此不在现有Camera64／velocity-integrated decoder上启动MAE长训。

Human轴的零训练representation screen表明：mask外Human128与guard-band外Human199
保持exact，不能把问题笼统归因于“non-causal decoder会任意改远端feature”；naive
clamp的world drift来自edit区root translation／heading增量累积。随后预注册N8
mask-local endpoint oracle四格全过，证明当前Human128存在端点闭合解，但未证明该解
自然、语义正确或可被网络摊销。因此当前Human128无需立即弃用，只授权一个带
root／heading endpoint loss的短screen；Human MAE长训与paper editing claim仍不启动。

重新开放editing的必要条件：

1. Actor与Director generation endpoint先通过各自上限gate；
2. Camera新representation通过world-center locality；Human短screen同时通过Human199、
   root position、heading与global-joint endpoint locality，以及mask内质量gate；
3. 训练遵循MotionLab式generation-prior → editing curriculum，标准generation replay
   始终保留；
4. Human edit先完成，再让Camera读取final Human；仍无joint parallel；
5. outside decoded preservation、boundary continuity、edit success与generation regression
   同时formal评估。

如果目标只是实用Camera edit，优先在显式Camera6-DoF／DSL／screen-space control上做
确定性编辑，再用Director residual平滑；这比在非局部Camera64 latent里强行MAE更简洁。

## 9. 执行顺序与预算边界

### P0-M／P0-D／P0-J：三个无训练falsification gates

- D0后先在current LAT／GEO做fixed-H换Camera text、fixed-program换Human、null／scrambled
  text与full-H／coarse-H intervention；
- P0-D按N32 calibration → `Rect-64` early audit → `Rect-320`顺序检验Director
  identifiability、articulation-aware programs、multi-solution naturalness与syntheticity；
- P0-J以natural48／challenge16、$K=8$ Human candidates、$M=4$ Camera programs比较
  fixed、selection、root／heading／time staging与oracle regret；Human质量必须不降；
- P0-D成功不能替代P0-J。若fixed-H在自然分布至少90%低代价可解，或joint benefit低于
  10%，co-design退出核心claim；
- 详细合同、预算与stop gate只见
  [[2026-08-01_storymotion-multipair-data-training-plan]]。

### P0-H：Human provider零训练上限与接口审计

- **目标**：确认官方Human provider的真实能力与StoryMotion adapter损失；multi-camera
  数据不能替代这一轴；
- **来源**：ViMoGen official `bf891dea…`源码／MBench与Kimodo official
  `1aece8c…`源码／model；权重只有在条款确认后才进入合同；
- **selection**：预声明common prompt、duration与seed；包含Pulp内、MBench OOD与
  camera-challenging动作，不挑visual；
- **预算**：先`N=32` smoke与fixed-8；单provider最多一个GPU-day，未通过即停；
- **当前状态**：source preflight已闭合；真实N32 adapter audit未开始。

三个本地P0不受外部权重条款阻塞，因此先执行；P0-H仍是Actor上限的独立hard gate，
但不混入首轮Director data ablation。

### P1-D：A-series与group-aware Director

- 预注册C0-GEO先跑A0 factual、A-text paraphrase与A-pair multi-target；数据效应成立后，
  C0-LAT只复验A0／A-pair；GEO仅是算力screen，不改变LAT／GEO共同主线；
- 再在GEO比较B0 flattened与B1 group-aware factorized Director，LAT做冻结单点确认；
- 主要gate是within-H控制、cross-H intent保持、fixed Camera-text tail、articulation-aware
  full-H对coarse-H增益、syntheticity与parent replay；
- 只有数据效应在独立natural／expert set复现，才扩`Rect-4096`与训练预算。

### P1-C：Camera-aware Human selection

- 只有P0-J在natural cohort显示headroom才训练；Human provider冻结，ranker预测continuous
  fixed-H regret，不向Human generator回传；
- 与random-H、Human-quality与solver-cost selectors使用相同$K$、planner和总预算；
- fixed-H低代价时exact返回首个Human，learned selector不优于generic wrapper则删除。

### P2：representation simplification control

- 只有新数据在explicit oracle中有headroom、而冻结Stage1不支持它时，才提前转向
  direct／local Camera representation；不先重训joint Stage1；
- current v11 vs direct/local Camera representation做同预算matched screen；
- generation与decoded locality共同gate，只保留一个vNext owner。

### P3：paper closure；P4：editing

- P3完成full data、multi-seed、sealed OOD、Auteur／Pulp matched baseline、ViGen utility、
  blind perceptual study、clean revision与许可证／成本披露；
- P4才考虑bounded staging与editing，不让高风险功能阻塞generation主线。

## 10. Go／no-go

### Go

- P0-D证明合法multi-pair headroom，且A-pair超过A0／A-text并在natural／expert set关闭
  Director counterfactual tail而不回退factual质量；
- P0-J在自然分布证明fixed-H regret、Human质量不降的selection／staging收益，并优于
  matched generic wrapper；
- 官方Human provider在adapter后仍显著抬高Actor与Joint OOD上限；
- Director intent owner关闭反事实tail而不回退Direct-C／sequential；
- 简化representation达到当前生成能力并通过decoded locality；
- StoryMotion能向至少一个公开ViGen系统提供可验证更好的Human／Camera control，而不是
  只展示一次性视频。

### No-go／收缩论文

- multi-pair收益只存在于synthetic caption／solver自评分，或direct solver本身已经是
  更简单、更可靠的完整解；
- natural cohort几乎都能由fixed-H Camera低代价解决，selection／staging只在刻意冲突集
  有效，或收益来自降低Human dynamics／语义质量；此时删除co-design主张；
- full articulated Human在articulation-aware Camera tasks上不优于coarse root／heading／
  height，则不以完整Human planning区分Auteur；
- Human收益只能在原生skeleton成立，canonicalization后消失；
- Camera反事实修复依赖metric adversarial optimization或牺牲parent quality；
- Stage1简化需要更多隐式部件才能追平；
- editing仍无法保护decoded outside region；
- 与Auteur相比只剩数据集内数字，没有dense reactive或独立Actor control差异。

出现No-go时，论文收缩为“audited asymmetric generation system”，不宣称foundation
motion model、independent editing或ViGen necessity。超过ICLR标准来自可证伪的核心
问题、matched competitor与sealed evidence，不来自继续堆功能。
