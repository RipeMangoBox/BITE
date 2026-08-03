---
title: "StoryMotion Camera-Aware Human Co-Design QA"
hypothesis: |
  当首个Human realization使Camera intent只能以高运镜代价满足时，Camera intent
  可以先从同一Human generator的语义等价候选中选择更可拍摄的realization，并只在
  selection仍为高代价时最小调整显式staging自由度；在普通低代价样本上则exact返回首个
  Human。该regret-gated co-design应优于matched Human-generator + given-H
  Camera-planner cascade，同时避免Camera条件污染Human prior。
status: archived_merged
tags:
  - StoryMotion
  - DIRECT
  - camera-aware-human
  - co-design
  - staging
  - counterfactual
  - ICLR
  - ICLR/2027
  - status/archived
source_notes:
  - "[[DIRECT/current]]"
  - "[[2026-07-31_storymotion-v11-actor-director-counterfactual-control]]"
  - "[[2026-07-31_storymotion-v11-explicit-framing-control]]"
  - "[[2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]"
  - "[[2026-07-31_storymotion-v11-human-temporal-locality-control]]"
  - "[[2026-08-01_storymotion-multipair-data-training-plan]]"
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]]"
  - "[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/Uni3C_Unifying_Precisely_3D-Enhanced_Camera_and_Human_Motion_Controls_for_Video_Generation]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/ICLR_2026/The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation]]"
  - "[[analysis/CVPR_2024/DNO_Optimizing_Diffusion_Noise_Can_Serve_As_Universal_Motion_Priors]]"
  - "[[analysis/CVPR_2026/ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero_Shot_Exact_Spatial_Motion_Control]]"
created: 2026-07-31T23:59:55+08:00
updated: 2026-08-03T14:30:39+08:00
---

# StoryMotion Camera-Aware Human Co-Design QA

> [!warning] 已合并归档
> 本页在2026-08-01完整合并入
> [[2026-08-01_storymotion-multipair-data-training-plan]]，只保留为历史QA快照，不再拥有
> live hypothesis、实验顺序或结论。后续修改只进入合并后的唯一owner。

> [!important] 当前结论
> StoryMotion最值得验证的独特性不是“把Human和Camera放进一个网络”，也不是让
> Camera gradient默认回写Human；而是**regret-gated ambiguity resolution**：
> 普通低代价样本exact保留首个Human，只有fixed-H Camera在冻结部署envelope下为高代价
> 时，Camera intent才先选择另一个语义等价Human realization，selection仍高代价时才
> 最小调整显式staging。`certified_infeasible`只保留给解析冲突或可复现下界。
> 当前v11只证明Human→Camera的单向条件生成；Camera→Human selection尚未实现，
> bounded staging也只有endpoint existence evidence，不能提前写成论文贡献。

本页历史上记录“Camera intent是否应影响Human，以及joint co-design是否优于given-H
Camera planning”这一因果轴的QA、upper-bound probe与go／no-go；当前owner已改为
[[2026-08-01_storymotion-multipair-data-training-plan]]。既有正式数字仍只见
[[StoryMotion-valid-metric-ledger]]；Actor／Director反事实、framing、Camera locality与
Human locality的原始screen数字分别只见对应source note，本页只引用其裁决。

## 1. Idea decomposition and association

### Q1：三篇ViGen相关工作的真正边界是什么？

**A：Uni3C与ActCam确实消费外部给定的表演／控制，但Auteur不能简单概括为“必须手工
提供完整Human motion”。**

- [[analysis/SIGGRAPH_ASIA_2025/Uni3C_Unifying_Precisely_3D-Enhanced_Camera_and_Human_Motion_Controls_for_Video_Generation|Uni3C]]
  在共享3D世界中执行外部SMPL-X Human与Camera控制，核心贡献是下游视频控制与几何
  对齐，不负责从两条创作意图选择Human–Camera pair。
- [[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]
  从driving video恢复已有表演，并在目标Camera参数下构造相机对齐的pose／depth条件；
  它是fixed-performance transfer，而不是performance synthesis。
- [[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation|Auteur]]
  的官方描述输入是自然语言与coarse Human motion；其完整pipeline还能从文本预测粗粒度
  actor program，再围绕该program生成human-relative Camera DSL。因此“无需用户上传
  MoCap”不是StoryMotion对Auteur的充分差异。更准确的差异是：Auteur的actor program
  主要规定root／heading／scale等粗staging，而StoryMotion目标是生成完整articulated
  Human motion，并验证Camera intent能否在其语义等价realization之间作可审计选择。

外部一手边界见[Auteur](https://arxiv.org/abs/2606.01900)、
[Uni3C](https://alibaba-damo-academy.github.io/Uni3C/)与
[ActCam](https://arxiv.org/abs/2605.06667)。

### Q2：是否已有工作做真正的Camera↔Human双向联合生成？

**A：有。仅以“联合建模”作为StoryMotion新颖性已经不成立。**

[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]
已经将任务定义为text-conditioned Human–Camera joint generation，并用screen framing
辅助模态引导联合采样。更直接的是
[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]：
它在两个角色与Camera的联合扩散空间中使用双向成对interaction，使Camera hidden state
影响角色、角色也影响Camera。其局限是双角色、无条件生成、缺少独立Actor／Director
文本控制；但它已经覆盖“Camera可以反向影响Human representation”这一结构性想法。

因此StoryMotion必须证明的changed slot不是bidirectional attention，而是：

1. independent Actor／Director intents；
2. preservation-by-default；
3. selection before adaptation；
4. high-regret-triggered、channel-bounded Human staging；
5. 相对matched cascade的pair-level收益与activation audit。

### Q3：当前v11在数学上究竟是什么？

**A：是合法joint distribution，但只是单向条件联合，不是Human–Camera co-design。**

$$
p_{\mathrm{v11}}(H,C\mid T_H,T_C)
=p_H(H\mid T_H)\,p_C(C\mid H,T_C).
$$

因此：

$$
I(H;T_C\mid T_H)=0.
$$

v11的Camera读取final／observed Human，Human owner从不读取Camera text。当前正式证据
支持Direct-H、observed-H Direct-C与sequential Human→Camera三个接口，支持Human在
Camera训练中exact保护；它**没有**证明Camera text会选择不同Human，也没有证明这种
选择比“同一个Human generator + given-H Camera planner”更好。

### Q4：什么条件下joint co-design才有不可替代价值？

**A：只有fixed-H Camera问题存在不可由Camera单边低代价消解的冲突时。**

given-H planner求解：

$$
C^*(H_0)=\arg\min_C E_{\mathrm{pair}}(H_0,C;T_H,T_C).
$$

允许在Human语义等价邻域中co-design时：

$$
(H^*,C^*)=\arg\min_{H\in\mathcal N_{T_H}(H_0),\,C}
E_{\mathrm{pair}}(H,C;T_H,T_C).
$$

真正要测的headroom是：

$$
\Delta_{\mathrm{co}}
=\min_C E_{\mathrm{pair}}(H_0,C)
-\min_{H\in\mathcal N_{T_H}(H_0),\,C}E_{\mathrm{pair}}(H,C).
$$

只有当$\Delta_{\mathrm{co}}>0$，且Human变化仍在独立审计的语义等价邻域内，joint
co-design才优于cascade。若每个合理Human都能找到平滑、可见、遵循Camera text的低代价
Camera，则given-H planner已经充分，Camera→Human没有方法必要性。

### Q5：Camera影响Human应分成哪些等级？

**A：分成三个授权等级，另有一个明确禁止的实现。**

| level | Human行为 | Camera作用 | 当前授权 |
| --- | --- | --- | --- |
| preservation | 返回首个$H_0$ | 只生成$C\mid H_0,T_C$ | v11默认且必须保留 |
| selection | 从同一$p_H(H\mid T_H)$的语义合格候选中选$H_k$ | 只改变候选索引，不修改候选内容 | 首选研究方向，尚未实现 |
| bounded staging | 只改显式root／heading／time等staging通道 | 仅在selection仍为高regret时启用 | 只有mechanistic headroom |
| raw bidirectional denoising | Camera condition任意改Human latent／backbone | 无默认保护与通道边界 | v11禁止，不重开joint parallel |

最强但仍可审计的目标不是“Camera修改动作”，而是：**Camera intent只解析Human text
未规定的staging自由度；当Camera可单独解决时，Human逐元素不变。**

## 2. Real scenarios and pain points

### Q6：哪些真实冲突可能让given-H planner不足？

**A：冲突必须来自有限Camera工作空间、构图、安全区或时间约束，而不是人为要求模型
同时改变两条轴。** 预声明诊断集至少包含：

1. static Camera + 大范围Human root movement；
2. frontal close-up + 快速转身／长期背身；
3. orbit Camera + 高频Human heading change；
4. fixed focal range + Human快速前后移动；
5. reveal／enter-frame + 入画时序不匹配；
6. side tracking + Human path与Camera workspace冲突；
7. 强制安全区、三分线或occupancy；
8. ordinary camera-solvable control，用于测false activation。

这些场景对应previsualization、虚拟制作、游戏cutscene、有限摄影棚／机器人Camera、
短视频自动运镜等真实需求。产品价值是减少人工重做blocking与staging，而不是单纯省掉
一份Human输入文件。

### Q7：selection为什么比直接训练Camera→Human adapter更值得先做？

**A：它同时提供最低风险实现与最干净的因果对照。**

- Human candidate由原$p_H(H\mid T_H)$完整生成，Human prior与权重不变；
- Camera text只改变“选哪个candidate”，不改变任一candidate；
- 可以用同一Human generator、同一Camera planner、同一候选池构造严格matched baseline；
- 若selection已达到oracle／adaptation效果，就没有理由训练会污染Human的反向模块；
- 若selection不优于Human-quality-only选择，说明当前Human ambiguity未形成Camera价值。

为实现“通常不影响”，selection本身也必须由冻结的regret gate控制：先运行首个$H_0$；
若Camera约束已低代价满足，系统exact返回$H_0$，不因候选排名的微小分差切换Human。

### Q8：bounded staging何时才有应用价值？

**A：只有候选选择后仍为稳定高regret pair时，并且修改可以被限制在导演／blocking通常会调整的
自由度。** 第一阶段只考虑：

- ground-plane root translation；
- global heading；
- 单调的小范围time warp；
- representation支持并可审计后，才考虑head／gaze／chest orientation。

不允许默认修改局部动作类别、肢体语义、foot contact、主要交互关系或用降低动作幅度
换取更容易拍摄。每次启用必须报告activation reason、修改通道、幅度、前后Human质量
和Camera收益。

## 3. Related-work support and research opportunities

### Q9：本地知识库对这一方向提供了哪些支持与反例？

**A：证据同时支持“pair-level协调有价值”和“裸联合建模不够新”。**

- [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]
  证明screen framing可以作为Human／Camera间的桥梁并改善一致性；它也是StoryMotion
  不能宣称首次text-conditioned joint generation的直接反例。
- [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]
  证明双向character–Camera interaction可改善联合运动质量，但其无条件双角色设定没有
  回答Camera影响Human何时应为零，也没有独立双文本与activation audit。
- [[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation|Auteur]]
  证明human-relative DSL、显式framing axis与deterministic 6-DoF解码是强Camera planner；
  它应成为given-H／coarse-H planner baseline，而不是只被当作下游ViGen。
- [[analysis/SIGGRAPH_ASIA_2025/Uni3C_Unifying_Precisely_3D-Enhanced_Camera_and_Human_Motion_Controls_for_Video_Generation|Uni3C]]
  与[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]
  证明协调后的3D控制能被视频生成器有效消费；它们适合验证下游utility，不适合与上游
  planner直接混成一个SOTA表。
- [[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm|MotionLab]]
  的消融支持先学generation prior、再引入条件任务并持续replay；这支持staging adapter
  只能晚于selection与generation gate，而非一开始联合训练。
- [[analysis/ICLR_2026/The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation|ViMoGen]]
  说明Human候选多样性与语义上限受数据／provider限制；Pulp-only selection失败只能
  否定当前系统headroom，不能自动否定高质量Actor provider下的方向上限。

### Q10：相对最近工作的准确一句话差异是什么？

**A：当前安全版本与目标强版本必须分开。**

当前安全版本：

> StoryMotion generates a full articulated human performance and then plans a
> responsive camera from independent actor and cinematography instructions,
> whereas downstream controllers consume externally specified motion controls
> and Auteur primarily plans actor-relative framing around a coarse actor
> program.

目标强版本，只有selection／adaptation正式通过后才可使用：

> Existing systems either execute fixed controls, plan cinematography around a
> fixed or coarse performance, or couple character and camera motion without a
> preservation contract; StoryMotion preserves its generated actor by default
> and invokes camera-aware selection or minimal staging only when a fixed
> performance cannot satisfy the cinematographic intent.

面对Towards Storytelling Animations时，最重要的差异不是“我们也双向”，而是
**independent language intents + continuous regret gate + zero false activation + bounded changed
channels + matched cascade advantage**。

### Q11：上一轮StoryMotion实验已经回答了什么？

**A：它们没有证明co-design收益，但精确排除了三个危险捷径。**

1. **N128 Actor／Director反事实。** 两个v11 endpoint都证明Actor text与Director text
   能改变各自输出，Director edit下Human exact；但Actor replacement后fixed Camera-text
   noninferiority失败，约39%的样本CLaTr下降超过5分。见
   [[2026-07-31_storymotion-v11-actor-director-counterfactual-control]]。这说明当前Director
   会响应Human，却未稳定拥有Camera intent。直接让Camera再反向改Human可能放大闭环
   漂移，不能把“反应强”当成“co-design好”。
2. **Director owner源码审计。** 当前Camera network交替读取Camera text与Human context，
   且v11的Human-context dropout为零；`null_human`没有训练信号。因此不能用
   `full(H)-null(H)`构造免训练interaction residual。真正matched cascade需要另训
   text-owned semantic program／Camera base，或使用明确的Auteur-like planner。
3. **Explicit framing adapter。** counterfactual screen能提高四字段control adherence，
   但30K pure4,053 formal在Direct-C／sequential多字段回退并被拒绝。见
   [[2026-07-31_storymotion-v11-explicit-framing-control]]。因此selection score不能只
   最大化现有framing／CLaTr evaluator；必须有parent replay、独立Human质量与盲评，
   防止metric hacking。
4. **Camera locality。** Camera64在mask外exact时仍因translation velocity积分产生远端
   world-center漂移；endpoint oracle也没有通过`0.10` gate。见
   [[2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]。因此首个co-design
   oracle必须直接工作在explicit 6-DoF／human-relative framing变量上，不能优化
   Camera64 latent后声称局部可行。
5. **Human locality。** Human128的远端Human199 feature逐条exact，但naive edit会因
   root／yaw积分产生world drift；N8 endpoint oracle四格通过，证明存在endpoint closure
   解，却有mask内motion quality恶化案例。见
   [[2026-07-31_storymotion-v11-human-temporal-locality-control]]。这只支持“bounded staging
   机械上可能”，不支持“语义自然且可学习”。selection仍应先于adaptation。

### Q12：当前证据对两个核心问题的直接答案是什么？

**A：**

- “Camera能否合理轻微影响Human？”——当前v11没有该通路；Human endpoint oracle只
  证明受限修改存在解，尚无Camera-conditioned semantic／utility evidence。
- “joint相比given-H Camera有什么优势？”——当前formal sequential只证明完整系统能
  从双文本产出pair，没有matched cascade与$\Delta_{\mathrm{co}}$，因此尚未证明优势。

换言之，这一方向是**高价值未验证假设**，不是上一轮结果已经支持的结论。

## 4. Frontier cross-domain techniques and validation ideas

### Q13：最小且最有信息量的第一个实验是什么？

**A：不是训练adapter，而是zero-training explicit-Camera joint-headroom oracle。**

对同一$(T_H,T_C)$，从冻结Human provider采样$K$个候选$H_1,\ldots,H_K$。先用独立
Human语义／物理条件定义合格集合：

$$
\mathcal K_H=\{k:\ E_H(H_k,T_H)\leq \tau_H,\;
E_{\mathrm{phys}}(H_k)\leq\tau_{\mathrm{phys}}\}.
$$

对每个合格Human，在human-relative framing／explicit 6-DoF空间求解。主标签不是不稳定的
binary feasible，而是constraint vector
$\mathbf e=[e_{\mathrm{hard}},e_{\mathrm{frame}},e_{\mathrm{dynamic}},
e_{\mathrm{style}},e_{\mathrm{visibility}}]$与冻结deployment envelope下的soft regret。
比较四个上限：

$$
\begin{aligned}
R_{\mathrm{fixed}} &= \min_C E(H_0,C),\\
R_{\mathrm{select}} &= \min_{k\in\mathcal K_H}\min_C E(H_k,C),\\
R_{\mathrm{stage}} &= \min_{\delta\in\mathcal S}\min_C E(H_0+\delta,C),\\
R_{\mathrm{oracle}} &= \min_{k\in\mathcal K_H,\delta\in\mathcal S,C}E(H_k+\delta,C).
\end{aligned}
$$

$\mathcal S$只含root `SE(2)`、global heading、time shift与monotone time warp。另比较
full articulated $H$与coarse `{root, heading, height}`，以判断完整Human是否真的给
articulation-aware Camera planning增加信息。

该实验不依赖当前v11 Camera planner的反事实鲁棒性，也不受Camera64 locality失败影响。
它只回答：**Human ambiguity中是否真实存在Camera可利用的pair-level headroom。** 64个
Actor intents分为natural48与预注册challenge16；若自然分布fixed-H低代价可解率至少
90%，或selection／staging显著获益少于10%，立即停止co-design核心主张。若收益来自降低
Human dynamics、静止或牺牲语义／contact，同样判失败；只有通过后才值得学习selector。

可借鉴的跨域思想包括constrained decoding、best-of-$K$ reranking、energy-based
planning、lexicographic optimization和selective prediction／abstention。它们在此不是
新贡献，而是用于建立可证伪upper bound。

[[analysis/CVPR_2024/DNO_Optimizing_Diffusion_Noise_Can_Serve_As_Universal_Motion_Priors|DNO]]
进一步说明冻结motion prior、只优化采样噪声也能构造无需重训的constraint oracle；因此
可作为selection／staging上限探针，而非部署方案。其逐样本数百至上千步优化和显存成本
也恰好要求本页把它限制在small-screen oracle，不把测试时优化收益冒充可用生成能力。
参见[DNO论文](https://openaccess.thecvf.com/content/CVPR2024/html/Karunratanakul_Optimizing_Diffusion_Noise_Can_Serve_As_Universal_Motion_Priors_CVPR_2024_paper.html)。

### Q14：通过oracle后，selection系统应如何运行？

**A：使用regret-gated cascade，而非同步双向去噪。**

```text
H0 = HumanProvider(actor_text, seed0)
C0 = Director(H0, camera_text)
if PairRegret(H0, C0) <= frozen_low_cost_threshold:
    return H0, C0                  # exact preservation

H1...HK = HumanProvider(actor_text, fixed candidate seeds)
keep only semantically/physically qualified candidates
for each Hk: Ck = Director(Hk, camera_text, matched camera noise)
select the qualified pair with minimum predicted regret
if every pair remains high-cost: abstain or enter bounded-staging phase
```

selection训练／推理必须满足：

- 相同Human generator、candidate seeds与Camera planner用于所有baseline；
- C0-LAT与C0-GEO作为co-mainline endpoint分别报告，不挑单臂结果；
- Planner score与formal audit metric分离，避免把同一learned evaluator同时作为优化器和
  成功证明；
- low-cost case返回$H_0$逐元素exact，而不是“平均变化很小”；
- 每个改变Human identity的样本记录activation reason和候选rank。

当前v11 Director可用于instrumentation lower bound，但因N128 fixed-Camera-text gate失败，
其selection结果不能直接成为paper evidence。正式比较前必须建立text-owned program、
Human event alignment与bounded actor-conditioned Camera residual，或接入输入／输出
matched的Auteur-like planner。

### Q15：困难集与首轮screen如何冻结？

**A：先建立不用于论文最终排名的natural48／challenge16，再在全部协议冻结后另建gold。**

首轮计划批次：

- **goal**：检验fixed／selection／staging／oracle regret差，以及camera-aware selection相对
  random、Human-quality与solver-cost selectors是否存在额外headroom；
- **source**：v11共享Human `105K` teacher产生的候选；natural48每组保留一个held-out
  Pulp factual Camera intent并独立抽取三个冻结taxonomy programs，16个预声明Camera
  冲突groups只作challenge diagnostic；
  不改Pulp motion／caption parent，只新增带reason code的可逆diagnostic manifest；
- **selection rule**：看输出前冻结IDs、texts、duration、$K=8$ Human seeds、$M=4$
  Camera programs、solver seeds、hard constraints与low／high-cost thresholds；
- **budget**：512个共享Human candidates、2,048个explicit Camera cell solves；最多一个
  GPU-day，不启动模型optimizer；
- **output target**：`runs/eval/stage2/<same-run-id>/`保存contract、fixed samples、
  per-pair records与results；本页只更新一条screen decision，不进formal ledger；
- **gold rule**：natural48／challenge16一旦用于改solver、taxonomy、gate或路线选择就只是
  audit set；架构、program schema、solver与评价冻结后另建post-freeze natural／expert
  gold，source type对标注者隐藏。

训练、构造、checkpoint与decoder仍需assert `is_causal=false`；本轴不授权joint parallel。

### Q16：最低baseline矩阵是什么？

**A：必须隔离“多采样本身”“Human质量选择”和“Camera-aware选择”。**

| baseline | Human候选 | 选择信息 | Camera planner | 回答的问题 |
| --- | ---: | --- | --- | --- |
| first-H given-H | 1 | 无 | named planner | 标准cascade |
| random-K | K | 随机候选 | 同一planner | 多采样但不看质量是否已足够 |
| Human-only-K | K | Human语义／物理 | 同一planner | 更好的Human是否顺带更好拍 |
| solver-cost-K | K | 显式solver cost | 同一solver预算 | generic best-of-K wrapper是否已足够 |
| Camera-aware-K | K | Human门槛 + predicted regret | 同一planner | learned selector是否利用Human ambiguity或节省solve |
| oracle-K | K | held-out full pair cost | explicit Camera solver | selection理论上限，不是可部署方法 |
| bounded staging | selected H | 仅高regret样本的显式staging | 同一planner | 修改Human是否超过selection收益 |

另做同一Human generator + Auteur-like given-H planner，防止把v11内部planner弱点误写成
joint modeling优势。下游Uni3C／ActCam类renderer只在最后做等3D control utility A/B。

### Q17：什么指标与gate能排除trivial solution？

**A：主要统计与bootstrap单位是Actor-intent parent group，不把同组$K\times M$ cells当
独立样本，也不用单独Human或Camera平均分代替pair成功。**

必须同时报告：

- Human text alignment、motion quality、dynamic amplitude、contact／skate diagnostics；
- Camera instruction adherence、hard-constraint success、out-of-frame、occupancy／framing；
- Camera translation／rotation速度、加速度与jerk；
- constraint-error vector、fixed-H／selected regret、joint blind preference与pair diversity；
- candidate index、activation rate、false activation、abstention rate；
- staging启用时的root／heading／time-warp修改量与局部动作变化。

预声明gate：

1. **Oracle existence**：natural48为主统计cohort，challenge16只作诊断；paired bootstrap
   regret reduction的95%下界大于`0`，benefit rate至少`10%`，且收益不能由降低Human
   dynamics或违反Human门槛解释。
2. **Selection value**：Camera-aware-K在held-out pair cost与constraint success上同时
   优于first-H、random-K、Human-only-K与matched solver-cost-K，或以同等质量显著减少
   solver调用；独立Human evaluator与盲评不劣。
3. **Default preservation**：ordinary low-cost样本的false activation率不超过`5%`，
   gate关闭时Human逐元素exact。
4. **No extreme Camera compensation**：收益不能伴随更大Camera jerk、极端拉远或持续
   zoom；Camera dynamics需非劣。
5. **No diversity collapse**：被选Human不能集中为低位移、低幅度或静止模板；按root
   path、heading、dynamic与动作语义分层报告selection frequency。

### Q18：bounded staging应如何实现，才能与Human endpoint证据适配？

**A：先在decoded显式staging变量上做小型、可逆、零初始化模块，不直接训练全Human
latent。**

建议形式：

$$
H'=\operatorname{ApplyStaging}
\left(H,\;g(H,T_C)\,P_{\mathcal S}\Delta(H,T_C)\right),
$$

其中$g=0$时逐元素返回原Human，$P_{\mathcal S}$只开放root `SE(2)`、global heading与
monotone time warp。训练前先做per-sample explicit optimizer oracle；通过后才摊销为
small head。loss同时约束：

- fixed-H高regret项的下降；
- Human text／local pose／contact保真；
- root position、heading、boundary velocity endpoint closure；
- generation replay与$g=0$ exact；
- 最终Human交回Director重新规划Camera。

Human N8 oracle支持endpoint closure存在，但mask内质量曾恶化；因此staging gate必须比
该oracle更严格。Camera64 endpoint oracle已失败，所以Camera一侧继续使用explicit
6-DoF／human-relative representation。整个流程仍是Human完成后再Camera，无
evolving-H joint parallel。

[[analysis/CVPR_2026/ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero_Shot_Exact_Spatial_Motion_Control|ProjFlow]]
提供另一项实现启发：把可精确计算的空间约束留在显式运动学空间，以projection修正而非
要求生成backbone自行学会每个硬约束。本轴只借用“显式约束 + projection”的求解原则，
用于root `SE(2)`／heading／endpoint closure；它不是StoryMotion的新颖性来源，也不授权
把projected state直接写回非编辑区或绕过decoder审计。参见
[ProjFlow论文](https://openaccess.thecvf.com/content/CVPR2026/html/Watanabe_ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero-Shot_Exact_Spatial_CVPR_2026_paper.html)。

### Q19：哪些结果会立即停止该方向？

**A：**

- explicit Camera oracle显示$\Delta_{\mathrm{oracle}}$没有正headroom；
- natural48中fixed-H低代价可解率至少90%，或显著benefit rate不足10%；
- Camera-aware-K不优于random-K、Human-only-K或solver-cost-K；
- full articulated $H$在articulation-aware stratum不优于coarse
  `{root, heading, height}`；
- 所谓收益主要来自降低Human幅度、静止、缩短root path或牺牲Human text alignment；
- given-H Auteur-like planner已经在同一困难集低代价解决冲突；
- $K$-selection达到bounded staging表现，则停止adapter训练；
- staging只在极端人工冲突有效，则降为optional production tool，不写普遍方法优势；
- 普通低代价样本无法保持exact Human或false activation超gate；
- 必须重开raw joint-parallel、隐藏provider差异或混用decoder才能得到收益。

## 5. Summary and next steps

### Q20：这一方向如何改变StoryMotion的论文中心？

**A：中心从“统一三模式”进一步收敛为“可审计的selective co-design”。**

候选claim阶梯为：

| claim | 当前证据 | 状态 |
| --- | --- | --- |
| Human-generated cinematography | formal sequential Human→Camera已完成 | 当前安全claim，仍需matched external planner |
| Camera-aware Human selection | 无直接实验 | 首要新颖性假设 |
| Optional minimal staging | Human endpoint existence only | 高风险条件claim |
| General Human／Camera editing | Camera hard stop，Human无语义编辑证据 | 继续删除 |

这一路线甚至可以简化Stage1叙事：Human provider、explicit Camera planner与selective
co-design policy各自拥有清楚职责，不需要把`human128+interaction16+camera48`的每个
内部部件写成贡献。joint modeling的价值由$\Delta_{\mathrm{co}}$和activation contract
证明，而不是由“共享一个latent”证明。

### Q21：最短执行顺序是什么？

**A：**

1. **P0-0／P0-M：data与current mechanism。** 完成Pulp配对度审计，以及LAT／GEO的
   fixed-H、fixed-program、null／scrambled text与full-H／coarse-H intervention。
2. **P0-D：Director data oracle。** N32 calibration后按`Rect-64 → Rect-320`检验
   root-level、articulation-aware与staging-conflict三层program；不启动模型optimizer。
3. **P0-J：joint-headroom oracle。** 用current v11 Human candidates与explicit Camera
   solver完成natural48／challenge16，比较fixed／selection／staging／oracle及generic
   selectors；完整合同见[[2026-08-01_storymotion-multipair-data-training-plan]]。
4. **P0-H：external Actor audit。** 获得Kimodo／ViMoGen权重授权后完成native→canonical
   N32，判断Pulp-only Human是否压低headroom。
5. **P1-A：data × matched planner。** GEO A0／A-text／A-pair后按冻结规则复验LAT，再建立
   text-owned program + Human event alignment + bounded actor-conditioned Camera residual；
   关闭现有N128 fixed-Camera-text tail与syntheticity shortcut。
6. **P1-B：camera-aware selection。** 同Human generator、同candidate pool、同planner与
   solve budget，对比first-H、random-K、Human-only-K、solver-cost-K与learned selector。
7. **P2：bounded staging。** 仅当selection通过且仍有稳定residual high-regret时启动
   explicit staging oracle与短screen；否则停止。
8. **P3：下游utility。** 将同一组协调3D controls送入一个Uni3C／ActCam类renderer，
   做随机／最差样本、control fidelity与blind preference，而非只展示best-case Demo。

### Q22：现在最强、最诚实的总括句是什么？

**A：目标句如下，但后半句仍是待证假设：**

> StoryMotion uses grouped counterfactual Actor–Director supervision to separate
> text-owned cinematographic intent from actor-dependent execution, and performs
> preservation-gated co-design: it keeps the default Human realization unchanged
> whenever fixed-H cinematography is adequate, while selecting a semantically
> equivalent realization only when doing so yields a measurable joint advantage.

在$\Delta_{\mathrm{oracle}}$、matched cascade、selection gate与sealed audit闭合前，论文
只能使用前半句。**首个成败问题不是“adapter怎么设计”，而是“当前Human ambiguity中
是否存在Camera单边无法获取的pair-level headroom”。**
