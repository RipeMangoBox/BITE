---
title: "DIRECT: Dual-Frame Cinematographic Intent Transfer across Articulated Human Motions"
hypothesis: |
  DIRECT不追求一般Human–Camera解耦，而研究如何从factual H-C pair恢复dual-frame
  cinematographic program，并针对不同完整Human motion重新执行。Pulp内部重组是同域
  主证据，HumanML3D跨域重组是可独立失败的扩展证据。
status: active_quality_boundary_before_rect
tags:
  - StoryMotion
  - data
  - multi-pair
  - counterfactual
  - DIRECT
  - paper/B
  - training
aliases:
  - StoryMotion-MultiPair-Plan
  - StoryMotion-Capability-Plan
  - DIRECT-Research-Plan
source_notes:
  - "[[DIRECT/current]]"
  - "[[StoryMotion-iclr-reliability]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[DIRECT/2026-07-31_storymotion-v11-actor-director-counterfactual-control]]"
  - "[[2026-07-31_storymotion-v11-explicit-framing-control]]"
  - "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
  - "[[DIRECT/2026-08-01_storymotion-pulp-hml-stage1-data-mixing]]"
  - "[[StoryMotion/paper-boundary]]"
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation]]"
  - "[[analysis/ICLR_2026/The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation]]"
  - "[[analysis/ICML_2025/Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]]"
  - "[[analysis/SIGGRAPH_2026/ARDY_Autoregressive_Diffusion_with_Hybrid_Representation_for_Interactive_Human_Motion_Generation]]"
created: 2026-07-31T23:41:25+08:00
updated: 2026-08-03T15:13:03+08:00
---

# DIRECT: Dual-Frame Cinematographic Intent Transfer across Articulated Human Motions

> [!important] 单仓库身份合同
> `DIRECT`是Paper B的论文／方法身份，不是新仓库。实现、配置、run与artifact继续位于
> `linkedCodebases/StoryMotion/`及其现有`runs/`布局；不创建DIRECT仓库。新DIRECT run
> 使用`direct_`前缀，已有`storymotion_*`、`v11_*`与`Actor–Director`诊断ID不改名。
> 共享Stage1／decoder／evaluator必须明确写为冻结的StoryMotion／Paper A基础设施，不能
> 把Paper A的能力保持式非对称框架重复计为DIRECT贡献。

> [!important] 当前结论
> 两个高优先级轴都已闭合：`RV-25`因source reconstruction `0/25`不授权Rect；三种Human-text Camera设计完成fresh `105K`与pure4,053 formal后形成geometry／semantic Pareto，没有单一全胜者。caption同义扩写、Stage1 observation替换、B-series、co-design和editing继续后置。

> [!failure] 当前仍未授权Rect训练
> D0发现的parent source-video leakage已经在RV target pool中隔离；旧N32结果仍不回写。新的`RV-25`虽然完成两条route，但source explainability前置门实际为`0/25`，因此target geometry局部通过也不能转成positive。当前停止Rect与HML规模扩展，先修factual program extraction／source reconstruction。

> [!failure] `RV-25 r3`开发screen结论（2026-08-01）
> `rv25_v0_boundary_seed17_5090cpu_r3_20260801`在row选择前从PP target pool剔除了donor split出现过的全部parent videos：移除`1,075`个重叠parent所含`1,418`条target samples，保留`2,635`条，过滤后parent交集为`0`。25个donor及12／8／5类配额先于solver冻结，失败row未补位。当前program template的source re-execution provisional screen为`0/25`；PP／XH target solver hard geometry分别为`14/25`和`16/25`，但source explainability失败使这些target pass均不能升级为positive，Rect edge仍为`0`。lateral path因没有样本同时满足Camera-text ownership与PP／XH exact-length pool而未进入本版，未放宽条件补齐。决策是停止扩Rect与HML规模，下一步先从factual actor-relative framing／style重做program extraction与source reconstruction。

> [!info] Human-text adapter 30K mechanism screen（2026-08-01）
> 三个run使用相同Pulp factual eval first-128 ordered IDs、共享Camera初始噪声、frozen v11 C0-GEO 105K parent与30K adapter exposure；三者`HT0` parent max-abs均为`0`。`HT-FILM`运行在4090，`HT-HX／HT-DR`运行在5090，因此不把跨host绝对值当作严格架构排名，判断以各run内部matching对HT0／HTS的差值为主。下表的两个括号差值依次为`HT−HT0／HT−HTS`，指标均为越低越好。
>
> | version / run | design／condition | Camera64 MSE | GEO | Camera14 recon | temporal | framing | screen判断 |
> | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
> | v11 / `v11_c0_geo_fixedh_gt30k_seed17_5090g3_r2_20260729` | `C0-GEO 0→30K ref` | `1.796990` | `0.113268` | `0.100128` | `0.005414` | `0.077255` | 历史同30K预算参照；不同起点／参数，不是causal control |
> | v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | `HT0／C0-GEO 105K` | `1.458255` | `0.074760` | `0.065600` | `0.003370` | `0.057899` | 三臂共享的exact parent；有效同父节点control |
> | v11 / `v11_ht_film_c0geo105k_30k_seed17_4090g0_r2_20260801` | `HT-FILM matching` | `1.465146`（`+0.006892／-0.011197`） | `0.074677`（`-0.000084／-0.000992`） | `0.065478` | `0.003398` | `0.058001` | 使用文本，但相对HT0没有一致净收益 |
> | v11 / `v11_ht_hx_c0geo105k_30k_seed17_5090g2_r2_20260801` | `HT-HX matching` | `1.467344`（`+0.009089／-0.006500`） | `0.074711`（`-0.000049／-0.000469`） | `0.065502` | `0.003411` | `0.057984` | 使用文本，但相对HT0没有一致净收益 |
> | v11 / `v11_ht_dr_c0geo105k_30k_seed17_5090g3_r2_20260801` | `HT-DR matching` | `1.444918`（`-0.013337／-0.007588`） | `0.074490`（`-0.000270／-0.000202`） | `0.065395` | `0.003348` | `0.057474` | 唯一同时超过HT0与HTS的候选 |
>
> C0-30K post-hoc reference与三臂严格共享first-128 IDs、eval batch、Camera noise、50-step Euler、Stage1／decoder、eval cache／stats、Camera text和GEO target。三个matching HT结果相对它的五项误差均更低，但HT从frozen C0-GEO 105K开始且只训练`166,080`参数adapter；C0-30K则从v11初始状态训练完整Camera 30K。因此该差值包含额外75K parent训练与参数范围差异，不能归因于Human text，也不能代替`HT0／HTS`。
>
> `HT-DR`的matching condition还同时改善Camera14 reconstruction、temporal与framing三个decoded分量，因此进入下一层held-out／event-role验证；`HT-FILM`与`HT-HX`停止升级。该结果没有bootstrap／第二slice，只证明factual Human-text机制可被学习，不证明multi-pair Director、event grounding或Rect有效。

> [!important] Human-text fresh `105K` formal结论（2026-08-02）
> 后续用户独立授权三种设计从相同Camera初始状态fresh训练完整Camera分支与Human-text模块到`105K`。三臂与exact matched C0-GEO共同完成pure4,053 Direct-H、Direct-C、formal sequential、decoded geometry、physical diagnostics、10,000次matched bootstrap与固定8例可视化。HT-HX的Camera geometry最强但sequential语义明显回退；HT-DR的Camera semantic／caption最强但相对C0-GEO六项geometry CI全部跨零；HT-FILM较均衡。故30K时“只升级HT-DR”的短筛结论被更完整的Pareto证据取代，不选择单一设计、不改C0-LAT／C0-GEO共同mainline。由于105K formal只评matching Human text，仍需同endpoint absent／shuffled held-out归因后才能声称正确Human语义带来收益。正式数值与哈希只见[[StoryMotion-valid-metric-ledger#3.13 v11 Human-text Camera fresh 105K pure4,053 formal audit]]。

> [!important] “去耦”用词修正
> Stage1让Camera依赖Human是合理的几何耦合；数据扩充要消除的是“某个Human／parent ID只能对应某条Camera”的一对一捷径，而不是让Camera脱离Human。目标是同时增强Camera-text所有权与Human-conditioned execution的可识别性。

本页是DIRECT数据构造、Human-text注入、训练顺序和降级条件的唯一live owner。正式数字、哈希与不确定性只写入[[StoryMotion-valid-metric-ledger]]；版本事件只写入[[version_family]]；run进度只保留在StoryMotion仓库对应`runs/` manifest／log。Pulp清洗与quarantine继续由[[2026-07-17_storymotion-v8-2333-data-curation-plan]]维护。solver输出统一称为`solver-qualified target`，不称GT。

## 1. 研究问题、系统边界与优先级

### 1.1 DIRECT的论文问题

DIRECT不能把主贡献写成一般Human–Camera解耦，也不能只写“同时生成Human和Camera”。目标问题收缩为：

> 给定final articulated Human motion与Camera instruction，同一Camera program迁移到不同Human realization时，能否保持Camera文本拥有的shot intent，同时依据Camera文本没有给出的动作事件、朝向、局部关节状态和world geometry，重新确定执行时刻与continuous 6-DoF Camera trajectory？

这里的`dual-frame`有固定含义：program在**actor／event-relative frame**表达应跨Human保持的
摄影意图，在**world execution frame**中针对目标Human重新求解continuous 6-DoF Camera。
它不是把source Human与source world Camera直接搬到另一个Human，也不是把HumanML3D Human
和原Pulp world Camera组成positive。

系统继续采用有向Actor–Director分解：

$$
p(H,C\mid T_H,T_C)
=p_H(H\mid T_H)\,p_C(C\mid H,T_H,T_C).
$$

其中Actor先生成final Human，Director随后生成Camera；不重开evolving-H joint parallel，也不让Camera gradient更新Human owner。Human text是否应进入Director是本轮待验证变量，而不是已证实设计。

当前v11边界保持不变：C0-LAT与C0-GEO仍为`105K`共同mainline，共享exact v9 Pulp-only non-causal Stage1、owning decoder／cache／train-only statistics与冻结Human teacher。当前Camera observation不是root-only，也不是raw Human199：Human199先由v9 Stage1编码为逐帧Human128，再投影成v11 Camera blocks读取的Human tokens。它拥有full-motion来源，但并不保证所有关节／事件信息都被保留或使用。

### 1.2 当前任务排序

| 优先级 | 任务 | 当前目的 | 现在不做什么 |
| --- | --- | --- | --- |
| 高 | `RV-25`数据构造与可视化 | 分别认识Pulp内部重组和Pulp-program→HML的质量边界 | 不盲评、不直接训练、不用开发集冻结成功claim |
| 高 | Human text注入Camera分支 | 验证动作语义／角色／事件提示能否补足Human observation | 不改Stage1、不把两种文本扁平拼接 |
| 次序后置 | Rect-N训练 | 在规则冻结和held-out确认后检验counterfactual target是否改善Director | 不让HML路线掩盖Pulp内部失败 |
| 低 | caption同义扩写 | 增加语言覆盖并构成text-only control | 不当作数据贡献或Rect同义词 |
| 低 | Stage1 observation替换 | 定位H128是否丢失显式几何／事件 | 不阻塞RV、HT或首轮A-series |
| 条件 | B-series、co-design、external provider | 只在前一层已有正信号时增加机制或上限实验 | 不与data、HT、Stage1同时改变 |

### 1.3 最小成功与降级目标

本轮不以“大模型级完美效果”作为继续条件。最低有价值结果是：在不破坏v11 factual replay和Human输出的前提下，Human、Camera、projection／pair或sequential质量中的目标字段形成可复现改善，并能由matched ablation说明改善来自target-H re-execution或Human-text角色信息。

贡献强度按证据降级：

1. Pulp内部重组有效、HML失败：只主张同域grouped counterfactual Director supervision；
2. Pulp与HML均有效：再主张跨Human-source program transfer；
3. raw solver pair有效但v9 Stage1 support失败：保留数据构造／solver诊断，不主张learned Director已吸收；
4. Human-text无效或与shuffled control无差异：删除该路径，v11输入合同不变；
5. A-pair只带来局部改进：按实际改善字段收缩claim，不声称完整DIRECT能力闭合。

## 2. 统一符号与数据语义

### 2.1 符号表

| 符号 | 唯一含义 |
| --- | --- |
| $H$ | canonicalized full Human motion sequence；来源可为Pulp或HumanML3D |
| $C$ | continuous 6-DoF Camera trajectory及其intrinsics |
| $\Pi(H,C)$ | 由$H$与$C$计算的逐帧screen-space projection／framing sequence |
| $T_H$ | Human motion caption |
| $T_C$ | Camera caption／instruction |
| $P=(a,M)$ | 从Pulp factual donor抽取的Camera program；$a$为结构化属性，$M$为文本所有权mask |
| $A_r(H,P)$ | 路线$r$的applicability判定：当前Human是否具备执行该program所需的几何、path或event |
| $S(H,P)$ | solver根据目标Human重新执行program后产生的Camera candidate或solution set |
| $V_r(H,C,P)$ | 与solver objective分离的路线$r$验证器；检查projection、owned attributes、dynamics与event |
| $C^*$ | 同时满足$A_r=1$、solver成功且$V_r=1$的solver-qualified Camera target |

`A_r(H,P)=1`只表示“这个program适用于该Human”，不表示Camera已经求解成功。`V_r(H,C,P)=1`只表示独立验证通过。只有两者与solver状态同时成立时，cell才是候选positive；因此正文不再用“默认每个cell都合法”这种缺少定义的表述。

### 2.2 两条数据路线

设Pulp factual source为：

$$
F_s=(H_s^{P},C_s^{P},\Pi(H_s^{P},C_s^{P}),T_{H,s}^{P},T_{C,s}^{P}).
$$

从$F_s$抽取的是Camera program $P_s$，不是把$C_s^P$原样复制给另一个Human。两条目标路线分别为：

$$
\text{PP}:\quad H_t^{P}+P_s\rightarrow C_{t,s}^{*,PP},
$$

$$
\text{XH}:\quad H_t^{HML}+P_s\rightarrow C_{t,s}^{*,XH}.
$$

`PP`是Pulp→Pulp内部重组，是最先建立因果机制的同域路线；`XH`是Pulp program→HumanML3D Human的跨域路线。HumanML3D不提供Camera GT，Camera监督只可能来自对目标Human的重新求解与独立验证。

Pulp内部扩充同时包含两个正交方向，而不只是一条Pulp＋HML路线：

$$
H_i^P\times\{P_1,\ldots,P_M\}
\quad\text{与}\quad
\{H_1^P,\ldots,H_K^P\}\times P_m.
$$

前者让同一Human被多个Camera programs拍摄，后者让同一program在多个Pulp Humans上重新执行。XH只把第二个方向扩展到外部Human source；它不是Pulp内部矩阵的替代品。

有效edge写为：

$$
\mathcal E_r^+
=\left\{(H_i,P_m,C_{i,m}^*):A_r(H_i,P_m)=1,\;V_r(H_i,C_{i,m}^*,P_m)=1\right\}.
$$

直接复制world Camera得到的$(H_t,C_s^P)$只标为`naive_control`。Human没有required event标为`not_applicable`；solver未收敛或验证器无法裁决标为`unknown`；二者均不得作为negative或trajectory target。

## 3. 数据构造：先认识边界，再生成Rect

### 3.1 Stage1耦合与数据扩充并不冲突

v9 Stage1把Human与Camera共同编码／解码，是为了保留投影、相对距离和构图所需的几何依赖。需要打破的是训练数据中的偶然绑定：

- 固定$H$、改变$P$时，Camera-owned shot属性应随$T_C$改变；
- 固定$P$、改变$H$时，actor-relative intent应保持，而event time和world Camera execution应随目标Human改变。

所以更准确的目标是`deconfound one-to-one pairing`，不是让$H$与$C$独立。新数据反而要求Camera更认真地读取Human，只是不再允许它用Human identity或parent ID猜唯一Camera。

真实风险在representation support：v9 Stage1只看过Pulp factual pairs，新组合即使raw geometry合理，也可能落在其Camera64 manifold之外。处理顺序固定为：

1. 在raw $H,C,\Pi$空间构造和审计，不先生成latent cache；
2. 规则冻结后，用exact v9 owner比较factual、source re-execution和target re-execution的encode→decode误差；
3. Stage1 support通过后才将child编码给v11；失败时保留raw数据结论，不为过门而重训joint Stage1。

### 3.2 `RV-25`的准确含义

`RV-25`表示**25个冻结的Pulp Camera-program donors**，不是25个总cell。相同25个donor进入两个独立面板：

- `RV-PP25`：每个program配一个split-disjoint Pulp target Human；
- `RV-XH25`：同一program配一个经过external-Human adapter的HumanML3D target Human。

两个面板各为25行×4列，共200个video cells。路线、指标、失败分母与结论分别报告；`RV-XH25`不能补齐或平均掉`RV-PP25`的失败。

每个面板的四列固定为：

| 列 | 内容 | 必须展示的信息 | 回答的问题 |
| --- | --- | --- | --- |
| Factual source | $(H_s^P,C_s^P,\Pi_s^P)$ | Pulp $T_{H,s}^P$、$T_{C,s}^P$、owned fields | donor是否来自真实可解释镜头 |
| Source re-execution | $(H_s^P,\widetilde C_s,\Pi(H_s^P,\widetilde C_s))$ | 同一双文本、source explainability vector | program＋solver能否解释source |
| Target-H re-execution | $(H_t^r,C_{t,s}^{*,r},\Pi(H_t^r,C_{t,s}^{*,r}))$ | target $T_{H,t}^r$、donor $T_{C,s}^P$、applicability／solver／validator状态 | 同一program能否按目标Human重新执行 |
| Naive world-C copy | $(H_t^r,C_s^P,\Pi(H_t^r,C_s^P))$ | 同一target Human text与donor Camera text | 重执行是否优于生硬复制world Camera |

HumanML3D若有多条caption，界面显示一条canonical caption并允许展开全部原始captions；不得先让LLM改写后再假装是原始文本。每个cell的一个video同时显示world Human、Camera trajectory与Camera projection。

当前`RV-25`是open-label开发诊断：显示路线、source ID、program class、文本、各项metric和reason code，不做身份隐藏或blind preference。目的不是估计正式成功率，而是找到solver、applicability、adapter与自然度的失败边界。失败row不得被替换成更容易的样本。

### 3.3 donor与target的冻结选择原则

25个donor在运行solver之前冻结，覆盖三种迁移难度：

- 12个`actor-relative generic`：shot scale、view azimuth、screen anchor、static／follow；
- 8个`root/path-conditioned`：root displacement、速度、转向或lead／trail关系；
- 5个`articulated-event-conditioned`：只选source与target均有高置信event的边界诊断。

`scene/world-dependent` program不进入RV positive候选。上述比例是小样本质量边界设计，不用于估计真实数据分布；最终manifest必须逐row公开program class。
5个event rows即使开发观感良好，也不能覆盖既有N32 event-alignment失败或直接获得训练资格。

target在看到solver结果前选择：

1. 先按duration、root-path type、heading change、active body parts与required event召回候选；
2. PP从parent source-video隔离的Pulp pool选取；XH从HumanML3D原始motion lineage选取；
3. 文本／TMR分数只负责top-$K$召回，motion-derived signature负责适用性复核；
4. 尽量让PP与XH target落在同一motion-signature stratum，以便定位domain shift；
5. 不因为solver失败而重抽target，也不为了凑满25个positive强行time-warp或替换root path。

### 3.4 共同筛选链与状态

每个cell按固定顺序通过六层检查，不用单一加权总分：

| 层 | 检查 | 输出 |
| --- | --- | --- |
| 0. Source integrity | $H_s,C_s,\Pi_s,T_{H,s},T_{C,s}$有限、同步、caption非空、split合法 | `source_valid`或reason code |
| 1. Program ownership | 只冻结Camera文本明确表达的shot scale、azimuth、anchor、primitive、target actor与event binding | 属性$a$与ownership mask $M$ |
| 2. Source explainability | 在$H_s$上re-execute后恢复owned attributes、visibility／framing与factual dynamics envelope | donor可迁移或仅保留factual replay |
| 3. Target applicability | 路线特定的$A_r(H_t,P)$；检查path、heading、body extent与required event | `applicable`、`not_applicable`或`unknown` |
| 4. Solve | 在目标Human上优化Camera，不复制source world trajectory；记录所有hard／soft costs | solution set或`solver_failed` |
| 5. Independent validation | 独立计算projection、occupancy、visibility、owned-attribute adherence、event alignment和Camera velocity／acceleration／jerk | `validator_pass`或逐项失败 |

开发期最后增加人工标签：`natural`、`acceptable_with_issue`、`unacceptable`、`uncertain`，并必须选择failure taxonomy；它帮助定义边界，不覆盖自动hard failure。

单cell只有在source integrity、program ownership、source explainability、target applicability、solver与independent validation全部通过，且人工不标`unacceptable`时，才记为`solver_qualified_candidate`。RV阶段只报告每层的分子、分母和失败原因，不设一个route平均分；route级训练门要等规则冻结后的held-out confirmation再预注册。

合法状态只允许：

- `factual`：不可改写的Pulp真实pair；
- `candidate`：尚未完成全部门的组合；
- `solver_qualified_candidate`：RV开发集中通过全部门，但尚未获得训练授权；
- `naive_control`：直接复制source world Camera；
- `not_applicable`：目标Human不具备program前提；
- `unknown`：solver或validator未给出可靠裁决；
- `rejected`：存在明确可复现的hard、adapter、semantic或naturalness失败。

### 3.5 PP与XH的标准差异

两条路线共享program ownership、source explainability、target-H re-execution、projection与Camera dynamics检查，但不能共用全部前置条件：

| 检查面 | `RV-PP25`：Pulp→Pulp | `RV-XH25`：Pulp program→HML |
| --- | --- | --- |
| Human representation | 原生Pulp Human199与现有坐标／fps | 优先回到原始AMASS／SMPL，再运行统一Pulp 22-joint extractor |
| adapter | 不需要跨数据集adapter | 只允许world-up、fps、skeleton、body scale与初始global $SE(2)$对齐 |
| 禁止变换 | 不跨parent复制Camera | 不替换HML root path、heading evolution或event timing，不从RIC263强行反解rot6D作为首选positive |
| semantic retrieval | Human caption与motion signature联合筛选 | 多caption／TMR只召回，最终由motion-derived action、path、heading、event与contact复核 |
| split | 按parent source video、Human asset、near-duplicate cluster隔离 | 按AMASS sequence／subject／near-duplicate lineage隔离 |
| naturalness anchor | Pulp factual distribution直接校准 | 同时报告对Pulp envelope的shift和HML自身Human质量；不得为HML重估Camera normalization |
| 可用program | generic、path与高置信event diagnostic | 无scene时禁用scene-dependent；event必须在target motion重新检测并重定位 |

PP target不必与donor Human具有完全相同的动作类别：一个generic side full-shot可适用于走路或挥手，只要$A_{PP}=1$。只有未来co-design比较多个“同一Actor intent”的Human时，才额外要求Human semantic equivalence。XH则多了一层domain adapter与text-motion一致性风险，因此其通过标准只会更严格，不会因为数据更大而放宽。

### 3.6 从RV到Rect-N

`RV-25`结束后先冻结三类东西：route-specific applicability规则、各hard metric的物理单位阈值／factual envelope、以及failure reason taxonomy。阈值只从Pulp train factual calibration与source reconstruction获得，不能根据某条synthetic route的成功率反向调松。

开发集冻结规则后，必须在未参与规则修改的held-out donors／targets上做一次confirmation audit，才能把`solver_qualified_candidate`升级为训练可用positive。当前不预设blind review，也不在尚未看清失败分布时伪造通过率门槛；正式论文自然度证据仍需在方法冻结后另做blind／sealed评价。

Rect使用带mask的稀疏Human–Program图。`Rect-N`中的$N$是target Human parent数，不是positive edge数，也不是rectified flow：

| 名称 | 规模含义 | 当前作用 |
| --- | --- | --- |
| Rect-64 | 64个target Human parents的pilot；合法edge数另报 | confirmation后做Stage1 support与小规模训练 |
| Rect-320 | 320个target Human parents；合法edge数随applicability变化 | A-series主要data experiment |
| Rect-4096 | 4,096个target Human parents | 仅在Rect-320有效后检验规模效应 |

每个名称必须加route字段，例如`Rect-64-PP`或`Rect-64-XH`。执行顺序是PP先证明同域机制，XH再作为独立扩展；二者可以同时构造／审阅，但不能从第一轮就混成一个dataloader。HML失败不阻止PP，PP失败则停止把HML当作Director训练救援。

### 3.7 Manifest与split最小合同

每个factual parent与child至少记录：

- Human来源、raw asset／subject／parent video、canonicalization revision与hash；
- source／target $T_H$、source $T_C$、program ID／class、owned fields与ownership mask；
- source pair、target Human、route、candidate selection reason与near-duplicate lineage；
- applicability、required event及其target-frame distribution；
- solver revision／seed／config／solution-set ID与逐项cost；
- independent-validator revision、metric vector、manual state与reason codes；
- split、Camera normalization source、projection／video hashes。

split先按parent source video、Human asset／AMASS lineage与near-duplicate cluster冻结，再生成child。任何factual parent都不得被synthetic child覆盖或删除。具体历史Pulp＋HML Stage1混合方式仍只见[[2026-08-01_storymotion-pulp-hml-stage1-data-mixing]]；它不等于这里的Director pair construction。

## 4. Human text进入Camera分支

### 4.1 三类条件的角色不能扁平化

| 输入 | 拥有的信息 | 不应拥有的信息 |
| --- | --- | --- |
| Camera text $T_C$ | shot scale、angle、screen anchor、Camera primitive、target actor、event relation | target Human的真实event frame与world位置 |
| Human observation $O_H(H)$ | 实际root／heading／关节几何、动作实现、event是否存在与发生时刻 | Camera style或未写入Human的摄影要求 |
| Human text $T_H$ | actor role、动作类别、主动身体部位、事件语义消歧 | 覆盖motion事实或直接指定Camera trajectory |

motion是最终权威：如果$T_H$说“举手”但final $H$没有举手事件，Camera不能只凭文本触发push-in。Camera text也不能把factual trajectory中偶然存在、但caption未表达的style字段据为己有。

### 4.2 最小层次化adapter

保持exact v9 Stage1、Camera64 target、v11 C0-GEO Camera flow和Human-first推理不变；冻结parent Camera、Human teacher与owning decoder，只训练zero-initialized adapter。三种设计分别检验Human text应在哪一层发挥作用：

| design | 精确定义 | 检验的问题 |
| --- | --- | --- |
| `HT-FILM` | 对Human text tokens做masked pooling，以channel-wise scale／shift调制Human128 | 全局动作语义是否已足够 |
| `HT-HX` | 每个Human temporal token作为query，对Human text tokens做cross-attention residual | Human text是否需要与动作时序位置对齐 |
| `HT-DR` | 由当前noisy Camera64与Human128联合query Human text，再对Camera flow velocity加独立residual | Human text是否更适合直接修正Director执行，而不改写Human observation |

三者都让Camera text继续走原有摄影条件路径，Human text不与Camera text拼成一串。`HT-FILM`与`HT-HX`改变Camera读取的Human条件；`HT-DR`保留原Human条件并只增加Camera residual。三者共享相同parent、初始化seed、ordered factual stream、Camera噪声、optimizer与30K exposure；adapter输出层在step 0为零。

每种design内部使用相同四条件机制评估：

| mode | 输入 | 因果作用 |
| --- | --- | --- |
| `HT0` | `condition_present=False` | 必须与frozen C0-GEO parent逐元素一致 |
| `HT` | matching $T_H$ | 检验正确Human text的条件收益 |
| `HTS` | batch内cyclic shuffle $T_H$ | 排除参数增加、caption长度或无关文本激活效应 |
| `HTZ` | present为真但Human-text tokens全零 | 区分真实文本内容与仅开启adapter路径 |

first-128共享噪声只用于mechanism screen：先要求`HT0` exact，再看`HT`是否同时优于`HT0`与`HTS`；`HTZ`用于解释adapter activation。只有winning design在更完整的event／actor-role、Camera-text adherence与factual replay中复现，才保留Human-text路径。若有稳定正信号，再补`HT-flat`作为直接拼接双文本的matched baseline；没有正信号时不实现flat baseline。

### 4.3 与multi-Human的边界

当前合同仍是single-Human Director。未来multi-Human shot除了多条Human motion，还需要per-actor identity／role binding、遮挡、depth order、screen occupancy和叙事主体标注。Human text可帮助角色绑定，但Pulp当前没有足够监督；本轮不得把matching-HT screen外推成multi-Human Director claim。

## 5. 最小实验顺序与评价

### 5.1 避免组合爆炸与返工

三个变量位于不同层：Rect改变target pair；HT改变Stage2 condition；O系列会改变Stage1 Camera observation／owning decoder。最小顺序为：

| 顺序 | 唯一变量 | 产物／判断 |
| --- | --- | --- |
| 1. RV raw audit | PP与XH route | 先认识构造质量边界；与Stage1无关 |
| 2. HT screen | `HT-FILM／HT-HX／HT-DR × HT0／HT／HTS／HTZ`，固定current O0与factual data | 判断Human text是否被使用、哪一层更合适以及是否有净收益 |
| 3. Rule freeze＋confirmation | 固定RV得到的route-specific规则 | 决定哪些route可生成训练positive |
| 4. A0 vs A-pair pilot | 只改是否加入re-solved target，固定current O0与HT0 | 先回答pair augmentation本身是否有效 |
| 5. 最小交互 | `A0/A-pair × HT0/HT-best`，仅当两单轴有信号 | 排除data与Human-text强交互 |
| 6. A-text | 同trajectory caption扩写 | 在正式归因前排除纯语言覆盖解释 |
| 7. O-series | H128与raw／coarse observation sibling | 仅在主线稳定后定位representation上限 |

raw Human、Camera、projection、program与manifest都保持representation-agnostic。首轮A-series直接使用current O0／v9 owner，不等待低优先级O-series；因此O-series失败时不需要回滚RV、HT或data manifest。

### 5.2 A-series与B-series

`A-series`只改变数据，不改v11架构／objective：

- `A0`：Pulp factual matched control；
- `A-text`：trajectory不变，只加入筛选后的等价caption；
- `A-pair`：加入对目标Human重新求解并验证的Camera target。

正式比较共享相同C0 parent、base factual stream、optimizer／EMA reset、sample exposure、seed、sampler与eval IDs。PP与XH必须先分臂；只有PP的A-pair有效后，才允许用XH回答跨域增益。

`B-series`是条件性架构实验，不是更大数据的别名：

- `B0`：在A-pair数据上加入text-owned program与Human-event adapters，但仍使用flattened batch；
- `B1`：再加入同$H$多$P$、同$P$多$H$的group-aware batch与actor-relative invariance loss。

只有A-pair相对A0与A-text的target-pair效应成立，才实现B0／B1。B-series不得与Rect规模、Stage1 observation或Human provider同时改变。

### 5.3 Stage1 support gate

confirmation通过的raw pairs在进入v11前必须通过exact v9 O0 owner：

1. Human branch与parent Human128保持逐元素exact；
2. Camera encode→decode的trajectory、rotation、FOV与projection误差相对同stratum factual calibration不显著越界；
3. synthetic latent相对冻结Pulp train statistics的median、p95、max与q99.9 exceedance单独报告；不得为HML重估stats掩盖shift；
4. 所有Stage1／Stage2入口assert `is_causal is False`。

若raw pair通过但O0失败，先把原因标为representation support gap；不把它误写成solver数据无效，也不立即用Rect重训joint Stage1。

### 5.4 评价拆成四层

| 层 | 核心问题 | 最小指标 |
| --- | --- | --- |
| Human | Actor是否保持语义、几何与物理 | Human reference metrics、root／joint error、bone／velocity／acceleration／jerk、foot skate／contact heuristic |
| Camera | Camera轨迹本身是否合理 | Camera reference metrics、translation／rotation／FOV、velocity／acceleration／jerk、workspace |
| Pair／projection | Camera是否正确拍摄当前Human | visibility、out-of-frame、occupancy、screen anchor、actor-relative distance／azimuth、projection error |
| Program transfer | 同一program跨Human是否语义稳定且执行改变 | owned-attribute adherence、same-program relative invariance、event timing、world-execution difference |

多解Camera不能只用paired Camera ADE裁决。先报告hard constraint vector，再报告soft cost与自然度。RV评价是data-builder质量；A／B评价是模型是否学会，二者不得混成一个“solver metric”。所有混合版本表逐row包含非空`version / run`。

### 5.5 停止条件

- PP source re-execution普遍无法解释factual shot：先修program抽取／solver，停止Rect；
- PP target re-execution不优于naive copy：停止pair augmentation主张，HML不得充当救援；
- PP通过而XH adapter／semantic／solver大量失败：保留Pulp-only路线，HML退回Human-only support；
- confirmation或Stage1 support失败：不训练相应route；
- A-pair不优于A0，或只在synthetic cohort改善而Pulp Natural／factual replay退化：停止扩到Rect-320／4096；
- matching `HT`不能同时优于`HT0`与`HTS`：不把该design升级为Human-text路径；
- 需要同时更换Stage1、objective与data才能看到收益：当前证据不可归因，不执行该组合。

## 6. Gradio页面合同

### 6.1 数据构造页

新建独立顶层标签页`Data construction · RV-25`，不要覆盖现有`Pulp 100-pair`：

- 子标签`Pulp→Pulp · RV-PP25`与`Pulp→HML · RV-XH25`；
- 每个子标签一次完整呈现25行×4列；
- 四列固定为Factual source、Source re-execution、Target-H re-execution、Naive world-C copy；
- 每个video同步显示Human motion、Camera trajectory和Camera projection；
- 行头固定展示source／target Human text、donor Camera text、program class与route；
- 指标面板分为Human、Camera、pair／projection、program／event四组；
- 显示applicability、solver、validator、manual状态和reason codes；
- 当前不隐藏列身份，不提供blind mode作为通过条件。

HML没有Camera GT，因此XH target列的Camera reference metric显示`N/A`及原因，不能用零值填充。projection与no-reference Camera／pair metrics仍正常计算。

### 6.2 模型比较页

Human-text结果放在独立顶层标签页`Human-text ablation`，按`HT-FILM／HT-HX／HT-DR`分子标签，并在相同fixed-8 rows比较Pulp factual、`HT0／HT／HTS／HTZ`；每个cell显示Human、Camera、projection、相对GT metric与no-reference physical diagnostic，并明确`version / run`。未来A-series放在`Rect training comparison`，不与RV的data-builder审计混在一起。

现有`Pulp 100-pair`只展示naive unpaired compatibility control；它不是RV source re-execution，也不是Rect positive。已交付页面与run provenance保持不改名。

## 7. 缩写与编号

| 缩写 | 完整含义 |
| --- | --- |
| D0 | 全量pair graph、duplicate与split-lineage审计；不是训练run |
| P0-M | observed-H／generated-H定向机制screen；保留原始边界，不等于Rect资格 |
| N16／N32 calibration | 每事件16条／平衡32条的solver与validator校准cohort |
| RV-25 | 25个冻结Pulp program donors的open-label Rect-validity开发审计总称 |
| RV-PP25 | 同25 donors在Pulp target Humans上的内部重组面板 |
| RV-XH25 | 同25 donors在HumanML3D target Humans上的跨域面板 |
| Rect-N | $N$个target Human parents上的masked rectangular supervision；valid edge数另报 |
| Rect-64／320／4096 | 64-parent pilot／320-parent主要data experiment／4,096-parent条件性规模实验 |
| F／M／X | Pulp factual／同Human多program target／同program跨Human target |
| A0／A-text／A-pair | factual data control／caption-only control／re-solved target-pair augmentation |
| B0／B1 | factorized Director flattened-batch版／group-aware batch与invariance版 |
| HT-FILM／HT-HX／HT-DR | pooled FiLM Human-condition调制／Human-token cross-attention／Camera-velocity direct residual三种adapter design |
| HT0／HT／HTS／HTZ | Human text absent／matching／cyclic-shuffled／present但zero-token四种机制模式 |
| HT-flat | 直接拼接Human与Camera text的条件性baseline；只在winning design有稳定信号后补 |
| O0／O1／O2／O3 | H128 baseline／H199／J66 root-local／J66 global Camera observation |
| N1／N2／N3 | Coarse-H／Coarse-H＋oracle event／Full-H＋predicted event necessity controls |
| J66-RL／J66-G | world root＋root-relative joints／22个world-space joints；均为66D |
| H68-HYB | world root 3D＋heading 2D＋heading-local joints 63D |
| H128／Human128 | exact v9 Stage1的128D Human latent；表示维数 |
| N64／N128／N512 | 64／128／512个样本的评估cohort；这里的`N`是sample count，不是latent维数 |
| N128 shared-noise | v11 Actor／Director反事实screen：128个ordered samples在对照条件间共享初始噪声，以减少采样方差；不是Human128表示实验 |
| C0-LAT／C0-GEO | v11共同mainline的latent-flow／decoded-geometry Camera objective endpoints |
| J16／J64 | 16／64个Actor-intent groups的co-design oracle headroom检查 |

`N1–N3`是necessity-control编号，`N128`是样本量，两者没有继承关系。正文首次出现任何新缩写时必须同时写出全称；表格仍必须保留`version / run`列。

## 8. 当前执行顺序

1. `RV-25 r3`已完成parent-disjoint PP pool、25个donor与PP／XH target预冻结、raw $H,C,\Pi$构造、自动指标和25行×4列open-label可视化；r1／r2保留为失效审计，不改写。
2. source explainability为`0/25`，因此先修factual program extraction／source reconstruction；不进入manual taxonomy、held-out confirmation或Rect-64。
3. current O0／v11上的三种Human-text Camera设计已完成30K机制screen与fresh `105K` pure4,053 formal；当前是HT-HX geometry、HT-DR semantic、HT-FILM balance的Pareto，不选单一winner。若继续，只补同endpoint matching／absent／shuffled held-out归因，不改Stage1。
4. 只有新的source reconstruction版本通过后，才重新冻结route-specific规则并在held-out donors／targets做confirmation；只有通过的route可生成Rect-64 raw targets。
5. 先用PP做A0／A-pair；两者有信号时补最小data×HT交互，再补A-text完成正式归因。
6. 只有PP有效后才训练XH arm；只有A-pair有效后才考虑Rect-320、B-series或Rect-4096。
7. Stage1 observation、caption规模扩写、co-design与editing保持后置。

每个新run在执行前冻结checkpoint／owning decoder／cache／stats／sample IDs／split／seed／batch／sampler／optimizer与EMA初始化。当前页只给研究合同；run级命令、进度和artifact hash不得回填到这里。

## 9. 关闭、低优先与条件性路线

### 9.1 v10已关闭

不再补v10 corrected endpoint、176D cache或Stage2。准确结论是“v10没有形成可替换v9的闭环”，不是“简化Stage1已被单变量证明失败”。v10同时改变Human owner、Camera representation、interaction16、decoder、Phase-C joint fine-tune与framing loss历史实现，无法把差异唯一归因于复杂度。详细provenance仍只见[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]。

### 9.2 MARDM／ViMoGen-light Human-only历史对照

这些确实是额外的fresh train／eval，不是只引用论文结果：

| 历史arm | 实际操作 | 已支持什么 | 没有支持什么 |
| --- | --- | --- | --- |
| C3-MARDM-H | 固定C3 Human representation，fresh训练masked-autoregressive＋SiT velocity到`105K`，N=512评估 | Human free-generation capability与局部semantic／coverage改善 | strict physical未过；没有Camera／composition |
| C3-ViMoGen-light-H CLIP | 固定C3 Human representation，fresh训练full Transformer＋shifted flow到`105K` | 三个Human-only endpoints中综合较强的ViMoGen-light端点 | strict physical未过；没有Camera／composition |
| C3-ViMoGen-light-H UMT5 | 同上，改用UMT5 text condition并fresh训练到`105K` | HCov局部更高 | strict physical未过；没有Camera／composition |

因此旧文中的“three external-style Human systems”应理解为一个MARDM-style端点加两个ViMoGen-light条件端点。它们都是在StoryMotion／Pulp合同内重新训练的架构—objective对照，不是MARDM或ViMoGen官方权重、官方数据上限或外部provider结果。正式数值仍只见[[StoryMotion-valid-metric-ledger]]，版本里程碑仍只见[[version_family]]。

### 9.3 低优先：caption同义扩写

Pulp绝大多数Human与Camera sample各只有一条caption，因此可对同一motion／trajectory生成`3–5`条语义等价表述，并做round-trip attribute parse、语义保持、近重复与split-lineage检查。它改善语言覆盖，但target不变，只属于`A-text`，不构成Rect或数据方法贡献。

### 9.4 低优先：Stage1 Human observation sibling

所有control保留exact v9 Human owner、Camera64 layout与non-causal边界，只替换Camera observation和owning Camera／framing decoder：

| ID | observation | 精确定义 |
| --- | --- | --- |
| O0／H128 | current baseline | Human199经exact v9 Human encoder得到Human128 |
| O1／H199 | Pulp Human199 | root height／local root velocity／yaw delta 4D＋rot6D 132D＋local joints 63D |
| O2／J66-RL | root＋root-relative joints | world root 3D＋其余21 joints减world root所得63D；joint axes仍是world axes |
| O3／J66-G | global joints | 22个world-space joints，$22\times3=66D$ |
| N1／Coarse-H6 | coarse Human | world root xyz＋heading sin／cos＋body height，共6D |
| N2／Coarse-H6＋E-oracle | coarse＋oracle event | N1加仅由Human gold产生的event distribution，不读取Camera target |
| N3／Full-H＋E-pred | selected full observation＋predicted event | 从$H,T_H$预测event distribution |
| H68-HYB | optional hybrid | world root 3D＋heading 2D＋heading-local joints 63D |

`J66-RL`的“local”只指去除root translation，不代表heading-local。ARDY的root raw＋local latent只提供层次表示先验，不证明哪种表示最适合StoryMotion；其causal tokenizer不得进入StoryMotion Stage1／Stage2。

### 9.5 条件性后置路线

- `B-series`：只有A-pair先证明target-pair effect才实现；
- `J16→J64 co-design`：只检验多个语义等价Human realization是否存在fixed-H Camera无法补偿的joint headroom，不阻塞Director数据；
- external Human provider：只作license／adapter sensitivity；HumanML3D raw motion pool不等于外部生成器；
- multi-Human Director：需要独立的per-actor binding与scene supervision，本轮不claim；
- MAE／general editing：与v11 Stage2训推合同不兼容且Camera64 locality／oracle已失败，退出投稿queue；
- learned bounded staging、PairGate、六路混训、style latent与大规模solver solution-set learning：只有前述简单规则成为实证瓶颈时再立项。

## 10. 论文表述边界

若PP A-pair有效，最稳妥的贡献表述是：

> DIRECT recovers an auditable dual-frame cinematographic program from a factual Human–Camera pair and re-executes it for a different articulated Human. The resulting supervision preserves text-owned cinematographic intent while adapting event timing and world-space Camera execution to the target Human.

只有XH route在独立adapter、compatibility、solver、Stage1与natural evaluation中也通过，才补充“跨Human source”。只有matching `HT`在独立评价中稳定超过`HT0`与`HTS`，才声称Human text有助于Camera执行动作事件／角色消歧。任何结果都不得被写成ViGen无法控制Human与Camera；DIRECT的区别必须落在可审计dual-frame program transfer与target-H re-execution。
