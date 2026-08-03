---
title: "StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera Generation — Reliability Plan"
hypothesis: |
  Paper A StoryMotion主张收口为capability-preserving asymmetric extension：
  冻结Human prior及其输出路径，以一个共享Camera模型增加observed-H与generated-H
  Camera generation。Pulp Camera坐标／文本修正是次要数据贡献；Paper A仍需关闭
  matched cascade、文本有效性、统计／感知、公开baseline与复现缺口。
status: archived_pre_closure_refactor
archived: 2026-08-03
tags:
  - StoryMotion
  - reliability
  - contribution
  - paper/A
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
  - "[[2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]"
  - "[[2026-07-31_storymotion-v11-human-temporal-locality-control]]"
  - "[[StoryMotion/paper-boundary]]"
source_papers:
  - "[[analysis/ICLR_2026/The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation]]"
  - "[[analysis/ICML_2025/Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion]]"
  - "[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/Uni3C_Unifying_Precisely_3D-Enhanced_Camera_and_Human_Motion_Controls_for_Video_Generation]]"
created: 2026-06-18T00:00:00+08:00
updated: 2026-08-03T14:30:39+08:00
supersedes: "[[2026-06-16_storymotion-v3-formal]]"
---

# StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera Generation — Reliability Plan

> [!important] Paper A唯一live范围
> 本页只授权Paper A的能力保持式非对称扩展、共享Camera接口、matched specialist
> cascade、Pulp Camera坐标／文本修正、公开baseline、sealed audit与复现成本。
> DIRECT、RV、Rect、HumanML3D跨配对、Camera program solver、Human-text Director与
> ViGen utility均不属于本页；其唯一live owner是
> [[DIRECT/2026-08-01_storymotion-multipair-data-training-plan]]。两篇工作只共享StoryMotion仓库，
> 不创建DIRECT仓库。

> [!warning] 拆分前总判断（只读历史，不作Paper A门槛或训练授权）
> 拆分前的Actor–Director、Rect、Human selection、editing与旧reviewer诊断仅保留在
> Appendix A–I供provenance追溯；它们不属于本页的live queue、Paper A claim或训练门槛。

正式数字与 hashes 只见 [[StoryMotion-valid-metric-ledger]]；本页只拥有论文
claim-evidence gap、优先级、停止条件与 acceptance strategy。

## 0. 当前ICLR数据与监督边界

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1080" width="100%" role="img" aria-labelledby="iclr-data-title" font-family="Inter, Arial, 'Noto Sans CJK SC', sans-serif">
  <title id="iclr-data-title">StoryMotion ICLR data supervision and evaluation flow</title>
  <rect x="0" y="0" width="1200" height="1080" fill="#ffffff"/>
  <defs><marker id="arrow-iclr" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#4b5563"/></marker></defs>
  <text x="600" y="28" text-anchor="middle" font-size="22" font-weight="700" fill="#111827">ICLR Paper A · data, supervision and evaluation</text>
  <rect x="420" y="48" width="360" height="54" rx="8" fill="#f3f4f6" stroke="#4b5563" stroke-width="2"/>
  <text x="600" y="80" text-anchor="middle" font-size="16" fill="#111827">Pulp factual: (T_H, H199, T_C^raw, C14)</text>
  <rect x="440" y="132" width="320" height="50" rx="8" fill="#f3f4f6" stroke="#4b5563" stroke-width="2"/>
  <text x="600" y="162" text-anchor="middle" font-size="15" fill="#111827">official split + parent-source audit</text>
  <rect x="820" y="50" width="340" height="86" rx="8" fill="#fde7e7" stroke="#a33b3b" stroke-width="2"/>
  <text x="990" y="73" text-anchor="middle" font-size="13" fill="#4a1717"><tspan x="990">OUT OF PAPER A DATA</tspan><tspan x="990" dy="19">RV · Rect · HumanML3D · program solver</tspan><tspan x="990" dy="19">· ViGen utility</tspan></text>
  <path d="M600 102 L600 132" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-iclr)"/>
  <rect x="28" y="218" width="724" height="526" rx="12" fill="#f8fbff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="390" y="250" text-anchor="middle" font-size="20" font-weight="700" fill="#244b7a">Pulp train · v9 non-causal Stage1 owner</text>
  <rect x="305" y="270" width="170" height="42" rx="7" fill="#f3f4f6" stroke="#4b5563" stroke-width="2"/>
  <text x="390" y="296" text-anchor="middle" font-size="14" fill="#111827">Pulp train</text>
  <rect x="70" y="346" width="250" height="56" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="195" y="369" text-anchor="middle" font-size="13" fill="#10243e"><tspan x="195">train-only z-normalization</tspan><tspan x="195" dy="18">stats</tspan></text>
  <rect x="455" y="346" width="250" height="56" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="580" y="369" text-anchor="middle" font-size="13" fill="#10243e"><tspan x="580">train-pair projection</tspan><tspan x="580" dy="18">+ framing targets</tspan></text>
  <rect x="250" y="438" width="280" height="54" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="390" y="460" text-anchor="middle" font-size="14" fill="#10243e"><tspan x="390">Stage1 factual H / C</tspan><tspan x="390" dy="19">reconstruction</tspan></text>
  <rect x="225" y="524" width="330" height="58" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="390" y="548" text-anchor="middle" font-size="13" fill="#3f2a0d"><tspan x="390">freeze encoder + owning decoders</tspan><tspan x="390" dy="18">+ stats + sample identity</tspan></text>
  <rect x="230" y="614" width="320" height="54" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="390" y="636" text-anchor="middle" font-size="13" fill="#3f2a0d"><tspan x="390">train cache: Human128</tspan><tspan x="390" dy="18">+ interaction16 + camera48</tspan></text>
  <rect x="56" y="686" width="280" height="46" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/>
  <text x="196" y="714" text-anchor="middle" font-size="13" fill="#113522">T_H → Human128 → protected H flow</text>
  <rect x="444" y="686" width="280" height="46" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/>
  <text x="584" y="706" text-anchor="middle" font-size="12" fill="#113522"><tspan x="584">fixed H128 + T_C(raw / geo) → Camera64</tspan><tspan x="584" dy="16">→ C0-LAT or C0-GEO flow</tspan></text>
  <path d="M600 182 L600 200 L390 200 L390 270" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-iclr)"/>
  <path d="M390 312 L390 328 L195 328 L195 346 M390 312 L390 328 L580 328 L580 346" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-iclr)"/>
  <path d="M195 402 L195 420 L390 420 L390 438 M580 402 L580 420 L390 420" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-iclr)"/>
  <path d="M390 492 L390 524 M390 582 L390 614" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-iclr)"/>
  <path d="M390 668 L390 678 L196 678 L196 686 M390 668 L390 678 L584 678 L584 686" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-iclr)"/>
  <rect x="790" y="218" width="382" height="526" rx="12" fill="#faf7ff" stroke="#7251a5" stroke-width="2"/>
  <text x="981" y="250" text-anchor="middle" font-size="20" font-weight="700" fill="#51377a">Pulp held-out eval</text>
  <rect x="876" y="284" width="210" height="44" rx="7" fill="#f3f4f6" stroke="#4b5563" stroke-width="2"/>
  <text x="981" y="311" text-anchor="middle" font-size="14" fill="#111827">held-out factual pairs</text>
  <rect x="836" y="376" width="290" height="56" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/>
  <text x="981" y="399" text-anchor="middle" font-size="13" fill="#2c1c48"><tspan x="981">eval cache from the same</tspan><tspan x="981" dy="18">frozen Stage1 owner / decoder</tspan></text>
  <rect x="836" y="484" width="290" height="56" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/>
  <text x="981" y="507" text-anchor="middle" font-size="13" fill="#2c1c48"><tspan x="981">eval-only projection</tspan><tspan x="981" dy="18">+ framing references</tspan></text>
  <path d="M600 182 L600 200 L981 200 L981 284 M981 328 L981 376 M981 328 L1140 328 L1140 466 L981 466 L981 484" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-iclr)"/>
  <rect x="28" y="778" width="1144" height="270" rx="12" fill="#fbf9fe" stroke="#7251a5" stroke-width="2"/>
  <text x="600" y="809" text-anchor="middle" font-size="20" font-weight="700" fill="#51377a">Three-mode formal evaluation</text>
  <rect x="65" y="838" width="280" height="58" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/>
  <text x="205" y="861" text-anchor="middle" font-size="13" fill="#2c1c48"><tspan x="205">Direct-H</tspan><tspan x="205" dy="18">T_H → generated Human</tspan></text>
  <rect x="460" y="838" width="280" height="58" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/>
  <text x="600" y="861" text-anchor="middle" font-size="13" fill="#2c1c48"><tspan x="600">Direct-C</tspan><tspan x="600" dy="18">observed H + T_C → Camera</tspan></text>
  <rect x="855" y="838" width="280" height="58" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/>
  <text x="995" y="861" text-anchor="middle" font-size="13" fill="#2c1c48"><tspan x="995">Sequential</tspan><tspan x="995" dy="18">generate H → FIX H → generate C</tspan></text>
  <rect x="400" y="928" width="400" height="48" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/>
  <text x="600" y="957" text-anchor="middle" font-size="14" fill="#2c1c48">frozen Stage1 owning decoders</text>
  <rect x="390" y="996" width="420" height="42" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/>
  <text x="600" y="1022" text-anchor="middle" font-size="13" fill="#2c1c48">Human + Camera + geometry + physical + bootstrap evidence</text>
  <path d="M196 732 L196 760 L205 760 L205 838 M196 732 L196 758 L995 758 L995 838 M584 732 L584 758 L600 758 L600 838 M584 732 L584 758 L995 758" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-iclr)"/>
  <path d="M981 432 L981 750 L205 750 L205 838 M981 432 L981 750 L600 750 L600 838 M981 432 L981 750 L995 750 L995 838" fill="none" stroke="#4b5563" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrow-iclr)"/>
  <path d="M205 896 L205 914 L600 914 L600 928 M600 896 L600 928 M995 896 L995 914 L600 914 M600 976 L600 996 M981 540 L1150 540 L1150 1017 L810 1017" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-iclr)"/>
</svg>

图中只有Pulp factual pair进入Paper A训练。Direct-H、Direct-C与sequential共享同一
Stage1 owner和Stage2 branch实现；sequential是Human完成后固定再生成Camera，不是
joint-parallel训练。`RV`、`Rect`、HumanML3D与Camera program重求解的完整数据图由
[[StoryMotion/paper-boundary#2.3 两篇工作的数据与监督边界图]]拥有，
这些数据不再构成ICLR Paper A的训练输入或接收门槛。

Camera文本修正仍位于同一factual edge内：固定extrinsic convention，从实际Camera参数
变化生成$T_C^{geo}$，同时保留$T_C^{raw}$、来源和修订版本。它不产生新的Human–Camera
配对，也不包含DIRECT的dual-frame program或event ownership。

## 0.1 当前Paper A的claim–evidence合同

$$
p(H,C\mid T_H,T_C)=p_H(H\mid T_H)\,p_C(C\mid H,T_C).
$$

Paper A包含两个条件分布和三个推理接口。Direct-H复用冻结Human prior；Direct-C给定
observed Human；Composition先生成并固定Human，再调用同一Camera模型。Direct-H质量是
被保留的基础能力，不计作Camera扩展带来的新增益。

| 当前主张 | 已有证据 | 投稿前硬缺口 |
| --- | --- | --- |
| Camera扩展不改变Human owner | seed17／23的Direct-H与Composition共享冻结owner；seed23逐样本replay守卫通过 | 将保持审计固化为公开测试与复现包 |
| 一个Camera模型执行两种Human来源 | Direct-C与formal sequential共享v11 Camera branch | matched specialist cascade；在质量或系统成本上至少建立一项优势 |
| protected latent interface承载Human–Camera关系 | v9 Stage1 owner、owning decoder与v11 Camera64合同已审计 | 只补最小zero／shuffle／route检查，不用v9-v10多变量差异代替因果证据 |
| Pulp Camera文本可被几何校正 | 已定位世界坐标选择会翻转部分方位描述 | 冻结convention；新增$T_C^{geo}$并保留原文；完成自动一致性检查、人工抽检与方向子集对照 |
| 三接口形成可报告系统结果 | seed17／23 pure4,053、geometry、physical与bootstrap已闭合；seed17固定样例已齐 | 同协议公开baseline、sealed audit、失败分层和复现包 |

> [!danger] 降级条件
> 若matched cascade在质量、成本和稳定性上与StoryMotion等价，则不再主张统一框架带来
> 方法优势，只保留受保护接口、Camera文本修正与同协议系统结果。若Camera修正未通过
> 轨迹－文本一致性审计，则它只能写成数据局限与未完成方案，不能列为贡献。

## 0.2 seed23复现已闭合；不自动授权后续长训

当前双卡只执行一个matched causal unit：在同一训练种子`23`下，分别从零训练
`C0-LAT`与`C0-GEO`至Camera optimizer `105K`。两臂共享v9 Pulp-only non-causal
Stage1 owner、冻结Human teacher、cache／stats／sample identities、batch顺序、噪声、
dropout、训练exposure与固定eval seed；唯一臂间变量是Camera objective。`5K`与`30K`
只作健康检查和不可变恢复点，不按中间指标择优停训。

判定规则如下：

1. 两臂都必须通过contract、Stage1 owner、cache identity、`is_causal=false`与
   Direct-H逐元素保持检查；任一臂fail-close时，本组记为不完整，不把另一臂写成
   multi-seed证据。
2. 到`105K`后，每条seed23结果只与同objective的seed17 mainline比较；LAT与GEO的
   seed23配对只回答objective差异是否稳定，不跨objective汇总均值。
3. 正式结论使用pure4,053 Direct-H、Direct-C与sequential，加decoded geometry、
   physical diagnostics和matched bootstrap；训练完成本身不等于复现通过。

> [!success] seed23 repeat结果（2026-08-03）
> 两臂均完成合法full-state `0→105K`训练与pure4,053 formal audit，Direct-H frozen-owner
> replay通过。seed17／23各自的GEO−LAT以及LAT／GEO各自的seed23−seed17，在Direct-C与
> sequential的ADE、FDE、rotation上共24个95% CI全部跨零。独立seed门因此关闭，但结论是
> “没有稳健单一objective胜者”，不是选择GEO或LAT；两臂继续共同mainline。完整数值与
> artifact identity只见[[StoryMotion-valid-metric-ledger#3.14 v11 C0 seed23 105K pure4,053 matched repeat]]。

seed23复现已经闭合。下一步specialist先做no-training identity guard与H199 evaluator-only
audit，不预注册新的Stage1或Stage2长训。Pulp Camera坐标／文本修正先完成CPU侧一致性审计
与人工抽检，只有数据版本通过后才另行决定是否需要raw-text／geometry-text matched训练。
最小机制检查、公开baseline复现、盲评和封存评测不同时改变训练变量。

## 0.3 Matched specialist causal contract（2026-08-03冻结）

> [!success] 针对“H–C separate Stage1是否需要重训”的裁决
> **Matched specialist不重训Human／Camera separate Stage1。** “specialist独立”只要求
> Human Stage2与Camera Stage2的权重、优化器和checkpoint独立；representation仍由同一个
> exact v9 Pulp-only non-causal Stage1及其owning decoder／stats持有。current C0已经满足
> Stage2 specialist decomposition。该Stage1的Human anchor本来就是Camera-free的
> $E_H(H)$；Camera侧保留Human condition是$p_C(C\mid H,T_C)$的任务要求，不能把
> “separate”误解为去掉$H$。B只增加冻结的`H128 → D_H → H199 → E_H → H128`
> 串行接口并复用现有endpoint，新增optimizer steps为`0`。若重训H/C separate Stage1，
> representation、decoder、参数、训练exposure与GPU小时都会同时变化，只能列为未授权的
> Cascade-Native system comparison，不能作为Paper A matched baseline。

> [!important] 已确认的实现事实
> 正式seed23 contract与revision `31b4d88d919e9340588a48f860f4d1b995087870`表明：
> current C0从v9 teacher分别载入Human与Camera子模块，冻结全部Human参数，优化器只持有
> `model.camera.parameters()`，并单独保存Camera EMA checkpoint；C0训练schedule为
> `GT_ONLY`，每步`128`个Pulp factual GT-H pair，共`105,000`步，generated-H训练
> exposure为`0`。正式repeat audit SHA256为
> `b87872ef96af20afaf385c54cae5ea5c754208c405b6dd2328de86730d4fb2a4`。
> 因此“同一H128接口 + 同一GT-H训练 + 独立Camera checkpoint”已经是C0本身，不能再作
> 新baseline或启动重复`105K`。

| arm | Stage1所有权 | Human→Camera接口 | Camera训练数据 | 参数／计算匹配 | 预声明结论边界 |
| --- | --- | --- | --- | --- | --- |
| A · StoryMotion current | exact v9 Pulp-only non-causal Stage1与owning decoder由两侧共享 | Direct-C读取observed-H的H128；sequential直接读取冻结Human teacher的final H128 | 仅Pulp factual GT-H／Camera pair；`GT_ONLY`；`105K × 128`；无generated-H positive | Stage1、Human teacher、Camera EMA三个logical weight owner；共享权重只计一次 | 当前reference；是两段顺序组合，不是同步joint generator |
| B · Cascade-Matched H199 | 冻结同一个exact v9 Stage1；不重训、不复制representation owner | Human specialist先用`D_H`输出H199；Camera specialist再用同一`E_H`和train-only stats回到H128；observed-H也从H199进入 | 与A逐ID、target、batch order、noise、exposure完全相同；generated-H只作推理分布测试 | 参数与logical owner数必须与A相同；sequential只多一次`D_H + E_H`；不得把文件打包方式算成参数优势 | 只检验protected latent直连是否优于普通H199串行API；不检验共享训练正迁移 |
| C · Cascade-Native（可选upper bound） | Human侧保留v9 owner；Camera specialist拥有另一套独立、non-causal、Pulp-only Stage1与owning decoder | H199是跨系统边界；Camera侧用自己的Human encoder重编码 | 仍只允许Pulp factual GT-H／Camera pair；禁止generated-H配原GT Camera；Stage2另起独立checkpoint | 额外Stage1参数、checkpoint、exposure、GPU小时全部计入；不要求与A／B参数相等 | 只能作system comparison／upper bound，不能归因于A的单个机制 |

### 0.3.1 B的同义守卫与唯一干预

先构造不进入主表的`B-latent-identity`：把现有Human teacher与Camera-only EMA作为两个
standalone module加载，但仍直接传H128。固定输入、valid mask、source id、初始噪声与
Euler50后，Direct-C与sequential的latent、decoded output及metric input必须逐元素
`max_abs=0`；state key、shape和value也必须完全相同。该测试通过只证明“拆成两个文件／
wrapper没有形成新系统”，不产生一行新结果；失败则是实现错误，禁止进入B-H199。

B-H199的唯一干预预声明为：

$$
R(z_H)=\operatorname{Norm}_H\!\left(E_H\!\left(D_H\!\left(
\operatorname{Denorm}_H(z_H)\right)\right)\right),
$$

其中$E_H,D_H$与normalization都来自exact v9 Stage1 owner。Direct-H继续输出原
$D_H(\operatorname{Denorm}_H(z_H))$，不得用二次round-trip结果覆盖Human；Direct-C用
observed H199经$E_H$得到的context，并须与现有cache逐元素一致；只有sequential Camera
condition从$z_H$改为$R(z_H)$。Camera source id、Camera noise、sampler、CFG、decoder与
所有official metric input保持不变。

这一定义与A在推理接口上非同义，但Camera训练路径仍同义：A的cache本来就是factual H199
经exact $E_H$所得，且没有合法的generated-H re-execution target。因此B不新增optimizer：

1. 先在seed17 LAT／GEO两个现有co-mainline endpoint上做同一first-128的identity守卫与
   H199接口smoke；两臂都检查是因为它们共同mainline，不据screen选臂。
2. 只有`B-latent-identity` exact且$R(z_H)-z_H$确实非零，才对两个现有seed17 endpoint做
   pure4,053 Direct-H、Direct-C与sequential evaluator-only audit及10,000次paired bootstrap。
3. seed23不默认扩展；只有seed17两objective给出相反方向的正式结论，或结论明显依赖
   objective，才按同一冻结合同复核seed23。全过程不启动新`105K`。
4. C保持未授权。只有B-H199 formal表明round-trip形成实质上限、且论文确实需要回答
   “Camera-owned representation能否恢复该上限”时，才另冻C的Stage1架构、loss和预算；
   第一条只做LAT以隔离Stage1 ownership，不把LAT称为优胜objective。GEO只有在C-LAT触及
   预声明决策边界且结论需要跨objective时才讨论。

### 0.3.2 匹配与成本口径

- **参数量：** 分别报告Stage1、Human Stage2与Camera Stage2的total／trainable scalar
  count；按唯一tensor storage去重。A与B必须完全相同；C的第二Stage1完整计入。
- **checkpoint数：** 统计logical weight owner，不统计容器文件数或EMA／raw／resume副本。
  A与B都是Stage1、Human、Camera三个owner；重新打包不能写成系统优势。
- **训练exposure：** 每段按`optimizer steps × effective batch × route multiplier`计算，
  分列Stage1、继承的v9 Human／Camera lineage和新增Camera训练。A的本轮Camera exposure为
  `105,000 × 128 = 13,440,000` factual pair；B新增为`0`。不得用并行双卡缩减总exposure。
- **GPU小时：** 每个GPU分别累计immutable manifest的`completed_at - started_at`，跨resume
  lineage求和；data build、training、formal eval与render分列，不以两卡wall-clock代替
  GPU-hours。
- **推理成本：** 固定同一host／GPU／environment、batch `1`和`32`、Euler50、相同长度桶、
  warm-up与CUDA synchronize；分别报告Direct-H、Direct-C、sequential的forward次数、
  p50／p95 latency和peak allocated memory。Stage1 encode／decode计入；text encoder因当前
  evaluator使用cache而单列。B唯一允许增加的是sequential的`D_H + E_H`。

### 0.3.3 预声明结果解释

- `B-latent-identity` exact后，论文必须承认current C0已可分解为独立优化的Human与Camera
  specialist；不得再主张A因“一个checkpoint”减少参数或获得共享训练正迁移。
- B-H199的Direct-H必须与A逐元素相同，Direct-C context必须与现有cache逐元素相同；任一
  失败都先修接口，不能解释成方法差异。
- A只在sequential的至少一个semantic／caption primary field和至少一个Camera geometry
  primary field的paired 95% CI都支持A，且没有primary field的CI支持B时，才能写
  “protected latent interface避免了H199 round-trip损失”。这不支持joint-training claim。
- 若primary CI全部跨零，结论是“未发现稳健接口优势”，不是“A／B等价”；若字段形成混合
  Pareto，也不选单一胜者。若B有反向稳健优势，则删除latent直连必要性主张。
- C无论胜负都只回答native specialist system上限；它与A／B的Stage1参数、exposure和decoder
  不同，必须逐row显式标注，不能进入matched ablation结论。

## Appendix A. 拆分前方案：Actor–Director（只读历史）

### 1.1 目标主张

> StoryMotion uses grouped counterfactual Actor–Director supervision to separate
> text-owned cinematographic intent from actor-dependent execution, and performs
> preservation-gated selective co-design: it keeps the default Human realization unchanged
> whenever fixed-H cinematography is adequate, while selecting a semantically
> equivalent realization only when doing so yields a measurable joint advantage.

这一主张对应三个不对称接口：Actor是Human instruction → 3D Human；
Director是final／observed Human + Camera instruction → continuous 6-DoF Camera；
Composition是Actor→Director。第三项是前两项的有向组合，不是第三个对称
generator，也不重开evolving-H joint parallel。后半句只有P0-J在自然分布通过后才成立；
否则目标主张必须降级为Human-aware Camera generation。

### 1.2 当前paper-safe版本

> StoryMotion supports Human generation, observed-Human Camera planning, and
> sequential Human-then-Camera generation with explicit source identities and
> a non-causal audited representation contract.

当前只能写到这里。Actor／Director N128 screen证明了双轴响应，但因Actor
replacement后fixed Camera-text noninferiority未关闭，不能写“independently
editable instructions”。C0-LAT与C0-GEO仍是同一v11方法的两个Camera
objective endpoint，用于诚实呈现semantic／geometry Pareto。

### 1.3 目标三项贡献及证据门槛

1. **Grouped counterfactual Actor–Director supervision。** 同Human多Camera与同program
   跨Human的矩形数据，分离Camera text拥有的program和actor-dependent execution；需
   A-pair超过A0／A-text，并排除synthetic shortcut。
2. **Articulation-aware Director。** text-owned program、Human-dependent event alignment
   与bounded actor-conditioned Camera residual；需在articulation-aware stratum证明full-H
   优于coarse `{root, heading, height}`。
3. **Preservation-gated co-design。** fixed-H低代价时Human逐元素不变，高regret时才选择
   语义等价Human或最小staging；需P0-J、matched generic selectors与Human质量不降证据。

三项都是目标claim，尚未全部闭合。完整执行合同见
[[DIRECT/2026-08-01_storymotion-multipair-data-training-plan]]。

### 1.4 不应进入主 claim

- “所有指标全面 SOTA”或“C0-GEO 稳健优于 C0-LAT”；现有证据不支持。
- “对称统一Human／Camera／Joint三种生成”；Joint是Actor→Director组合。
- “独立双文本控制已闭合”；N128 screen的fixed Camera-text gate失败。
- “ViGen无法联合控制Human／Camera”；Uni3C／ActCam已接收给定的两类控制。
- “C0 sequential 在 matched 条件下支配 C3 joint parallel”；formal solver不同。
- “v10 证明简化 Stage1 必然失败”；v10同时改变多个变量。
- “支持 motion editing”；Camera已触发hard stop，Human只有endpoint existence oracle。
- “physical validity 已解决”；contact／skate 仍是 heuristic。

## Appendix B. 拆分前gap表（只读历史）

当前状态属于**已有可审计基线，但新颖性、上限与可用性因果链未闭合**。

| gap | 当前证据 | 审稿风险 | 接收前最低闭环 | 优先级 |
| --- | --- | --- | --- | --- |
| 方法中心与新颖性 | v11有三个entry points，Actor／Director screen双轴有响应 | “三模式统一”不准确；Auteur已是语言Camera planner | 冻结Actor–Director定义；以dense reaction、counterfactual independence和explicit 3D plan与Auteur matched | P0 hard |
| 数据可识别性 | 当前Pulp loader／text cache对每个sample只绑定一个Camera target；v0 N32 hard／event gate失败 | Human identity、Camera text与trajectory共变；solver output也可能是不自然或不可解释的伪positive | D0／split修复 → `RV-PP25`与`RV-XH25` open-label边界审计 → 规则冻结与held-out confirmation → Rect-64／320 → A0／A-pair／A-text | P0 hard |
| co-design必要性 | 当前sequential只实现$H\sim p(H\mid T_H)$后$C\sim p(C\mid H,T_C)$；无matched fixed-H headroom | Human generator + Auteur-like planner可能复现全部产品接口 | J16 early oracle → positive才扩J64；hard rescue／vector improvement优先于scalar regret | P0 independent |
| Actor能力上限 | 当前Human owner仅消费Pulp；official ViMoGen／Kimodo尚未接入 | J oracle可能被候选质量封顶 | 本投稿只做license／adapter unit test；仅当超过20% groups不足4个合格候选才做provider sensitivity | conditional |
| Director独立可控 | N128两臂语义响应通过，fixed Camera-text noninferiority均失败 | Human变化时Camera instruction被级联context淹没 | text-owned program + Human event alignment + bounded actor-conditioned Camera residual；同时关闭tail、visibility与parent replay | P0 hard |
| Stage1 Camera observation | v11 Camera读取由Human199压缩的H128；是否保留root／joint event未知 | H128可能root-dominant；raw global joints又可能过拟合 | 首轮固定current O0完成RV、HT和A-pair；只有主线稳定或support失败指向representation时，再做H128／H199／J66／Coarse-H sibling screen | low-priority diagnostic |
| 统计复现 | 主线selection来自seed17；LAT/GEO CI只覆盖matched samples | seed特例、训练偶然性 | 至少完成独立Stage2 seeds；报告mean／std与失败率，不再用单seed选臂 | P0 hard |
| 感知有效性 | fixed-8 visual已齐，C3有“平均化”视觉问题 | 指标与实际观感错位 | 预注册盲评：随机系统名、同prompt、质量／构图／动作一致性／偏好，报告置信区间 | P0 hard |
| Baseline／实用性 | C3、v9、Pulp已有；尚无Auteur matched或下游ViGen utility | 内部baseline多，没有证明为什么ViGen需要StoryMotion | Pulp native + Auteur matched planner；Uni3C／ActCam／ViMoGen只做等接口的downstream utility | P0 hard |
| Generalization | pure4,053已被反复用于开发 | test-set overfitting／selection leakage | 冻结所有选择后，用新sampling seeds与预注册盲评cohort做一次sealed final audit | P0 hard |
| Reproducibility | contracts／hashes丰富，远端代码仍有未入Git工作 | 结果不可复现、artifact依赖主机 | clean Git commit、配置、环境、命令、模型身份、训练成本、最小demo与table generator | P0 hard |
| Editing | Camera gate与oracle失败；Human只有endpoint existence | MAE只消费C0 prior | general editing与learned staging退出本次投稿时间线；只保留J中的explicit staging oracle | out of scope |

继续训练C1、恢复已关闭的v10 Camera Stage2、延长MAE或新增Camera objective都不会
自动关闭这些缺口。

## Appendix C. 拆分前Stage1边界（只读历史）

### 3.1 贡献归属已冻结为路线B

当前v11投稿线不把`human128 + interaction16 + camera48`、Human anchor或三阶段
schedule分别写成贡献。它们是failure-driven backbone，只需说明non-causal
合同、owner／decoder身份与已有机制检查。如果未来重新把Stage1写成贡献，必须
另行授权matched component ablation；当前不用v10代替该证据。

新Raw-H control也不重新解释v9每个内部件：第一轮保留`interaction16 + conditioned-camera48`
及Camera64 target，只把Camera observation与owning decoder从H128换成显式Human sequence。
删除interaction或改Camera latent必须另立后续单变量合同，不能在本轮顺手“简化”；这样它才是
v11与sibling observation的matched比较，而不是v10式多轴重做。

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
- 2026-08-01已按scope关闭：不补formal endpoint、176D cache或Stage2；Raw-H observation是保留v9 Human owner／Camera64 layout的新sibling，不是v10续作。

### 3.4 最小补强

按收益排序：

1. **零训练机制表。** 汇总 `z_h` Camera invariance、`z_hc/z_c` zero／shuffle／oracle、
   owning-decoder敏感性和O0–O3坐标可恢复性，只回答“信息是否存在／模块是否被使用”。
2. **Raw-H统一短筛。** 冻结exact v9 Human branch与Camera64 target encoder，只替换Camera
   observation projector及owning Camera/framing decoder；N64 overfit后以同一短预算比较
   H128、H199、J66 root-local／global和Coarse-H，只取一个winner。
3. **保持co-mainline可回退。** winner先做C0-GEO screen、再由C0-LAT确认；失败逐元素退回
   O0/H128。新owner不覆盖v11 artifact，也不与Rect、Human-text或Camera objective同run改变。

## Appendix D. 拆分前实验包（只读历史）

### 4.1 必做

1. **共享冻结。** 修复D0 parent split；保持program／metric v0、observed／generated-H分层P0-M及N16／N32失败边界。冻结同25个Pulp donors，分别完成`RV-PP25`与`RV-XH25` open-label边界审计；两条route分别报告，当前RV不授权Rect positive。
2. **高优先条件轴。** 在current O0/H128与factual data上做HT0／HT1／HTS；Human text只通过zero-init motion-token adapter进入，Camera text继续独立拥有program。
3. **规则确认。** 根据RV冻结route-specific规则与阈值，再以held-out donors／targets确认；PP失败时XH不得救援。
4. **Director分支。** 先在通过confirmation的PP route生成Rect-64-PP并审计exact v9 Stage1 support，再运行A0／A-pair；有信号后补最小data×HT交互与A-text归因。PP有效后才训练XH route。
5. **co-design分支。** J16与上述分支并行；只有natural正信号才扩J64。P0-J失败不阻止
   A-series，P0-D失败但J为正时只保留显式solver selection／staging。
6. **条件factorization。** 只有A-pair超过A0且正式归因时也超过A-text，才实现小型$G_T/G_A/G_E$ adapters与B0／B1。
7. **统计与感知闭环。** 选定架构后再做独立训练seeds，并预注册盲评：
   Actor语义、Director语义、主体可见／构图、运动自然度与总体偏好；统计unit是
   rater×sample。
8. **Sealed competitor audit。** 冻结架构、指标与prompt taxonomy后，以新
   sampling seed只跑一次；Pulp／C3保留，Auteur只在匹配输入／输出下进表，
   Uni3C／ActCam／ViMoGen只评downstream control utility。
9. **复现实验包。** clean revision、provider／license、exact artifact identities、
   环境、命令、Actor／Director／Composition schema、table generator、random／best／worst
   demo与计算成本一次冻结。

### 4.2 强烈建议

- Actor replacement根据Camera caption taxonomy分层：world-static、human-relative、
  truck／dolly／orbit不得静默混合；同时报均值与tail failure rate。
- 按长度、转向强度、Camera文本类型、主体出框风险做failure taxonomy，并把最好、
  随机、最差样本都纳入补充材料。
- 报告参数量、训练GPU小时、推理延迟、显存和solver步数；provider与
  StoryMotion成本分开，不隐藏外部先验的计算／数据代价。
- P0-H只维持license／weight preflight与adapter unit tests；Day 5没有可运行权重时跳过。

### 4.3 低收益或暂缓

- C1 swapped-host replay：只在论文要声称teacher-final mixed context因果失败时需要。
- v10 Camera Stage2：已按scope关闭；它不是matched simplification control，不恢复。
- 更多LAT/GEO权重、Camera CFG、PCGrad、framing sidecar或长程MAE：当前没有
  直接关闭Actor ceiling／Director ownership／decoded locality。
- 对已开发的pure4,053继续挑checkpoint或样本：会加重selection leakage。

## Appendix E. 拆分前Editing诊断（只读历史）

MAE从pretrained C0初始化，它能学习如何利用／重定向C0 prior，但不能证明
C0的conditional support被抬高。generation与editing必须分checkpoint、分表与分claim。

当前Camera temporal-inpainting oracle已给出更硬的负面证据：Camera64在mask外逐位
exact不变，decoded rotation泄漏较小，但world Camera center因velocity integration持续
漂移；endpoint optimizer仍未达到预声明locality gate。详见
[[2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]。因此：

- 不在现有Camera64／velocity-integrated decoder上启动MAE长训；
- Human128 screen中mask外latent与guard-band外Human199均exact `0.0`，但world root／
  global joints因root／heading增量累积而失败；N8 mask-local endpoint oracle随后四格
  通过，只授权一次带root／heading loss并同时检查语义、边界、mask内质量与generation
  replay的amortized短screen；详见
  [[2026-07-31_storymotion-v11-human-temporal-locality-control]]；
- 只有Actor／Director generation endpoint先关闭，且摊销后的Human root／heading与
  Camera新表示的world-center locality都通过，才允许重开formal editing；
- 重开时遵循generation prior → editing curriculum并保留generation replay；Human edit
  先完成，Camera只读取final Human，仍禁止joint parallel。

在这些条件闭合前，editing从标题、摘要和主contribution删除。如果产品目标只是
Camera edit，优先在显式6-DoF／DSL／screen-space representation上做确定性编辑与平滑，
不必强行继承当前Camera64 latent。

## Appendix F. 拆分前claim-evidence matrix（只读历史）

| candidate claim | 当前状态 | paper-safe wording | 缺失证据 |
| --- | --- | --- | --- |
| Actor、Director与Composition三个接口 | 已有pure4,053 formal endpoint | supports Human generation, observed-H Camera planning and sequential Human-then-Camera generation | multi-seed + sealed audit |
| Actor／Director独立文本控制 | N128响应通过，fixed Camera-text gate失败 | screen-level response only；omit independent control claim | Director intent owner + formal counterfactual audit |
| 外部Human prior抬高能力上限 | 未验证 | omit | official provider native／adapter／composition matrix |
| 对下游ViGen有不可替代的utility | 未验证 | exports explicit 3D controls；不写improves ViGen | matched downstream control study |
| LAT/GEO存在可报告Pareto | 已有matched bootstrap | two co-mainline objectives expose a semantic/geometry Pareto | training-seed stability |
| v11系统优于former C3 | 部分支持 | improves several semantic, coverage, framing and geometry axes under a system boundary | blind preference；不写全面支配 |
| Stage1每个复杂部件均必要 | 未支持 | failure-driven backbone；不写component novelty | Raw-H observation只回答信息接口，不替代component necessity |
| Editing能力 | Camera hard stop；Human仅有endpoint existence headroom | omit / future work | 本投稿不补；只保留J中的explicit staging oracle |
| Physical validity | 未闭合 | reports no-reference kinematic diagnostics | calibrated ground/contact evaluation |

## Appendix G. 拆分前go／no-go标准（只读历史）

### 可进入投稿整合

- 中心主张稳定为Actor–Director planner，Composition明确为有向组合；
- Director intent owner关闭Actor replacement tail，且不回退parent Direct-C／sequential；
- 唯一observation owner先由Pulp matched短筛冻结；Rect-64随后通过O0／O* support audit；
- 最终endpoint的多seed没有系统性崩溃；
- 盲评至少支持一项主观优势，且失败样本已披露；
- Pulp／C3／Auteur对照与至少一个ViGen utility study完成，不可比字段显式标注；
- Stage1冻结为backbone且不写component novelty；
- 代码、配置、artifact身份、表格生成和demo可从clean Git revision复现；
- editing与learned staging完全退出主claim。

### 应暂停扩功能，先修论文

- 新实验不能关闭上述任一hard gap；
- 又引入新的representation／objective／solver而没有淘汰旧claim；
- 只在开发cohort、单seed或挑选视频上改善；
- 外部Human优势在canonical adapter后消失，或Director修复依赖metric hacking；
- 与Auteur相比只剩Pulp内部指标，无dense reaction、independent control或downstream utility；
- 为了“更多功能”牺牲Human保护或sequential合同；
- 结果需要靠改名、隐藏sample count或混合decoder才能看起来更好。

## Appendix H. 拆分前优先顺序（只读历史）

1. 冻结C0-LAT／C0-GEO co-mainline；v10正式关闭，所有新结果来自sibling contract。
2. 先修D0 parent split并保持失败的v0 calibration边界；针对N32 hard failure做版本化solver诊断，不用人工标注覆盖失败。
3. 冻结同25个Pulp donors，完成`RV-PP25`与`RV-XH25`两块25×4 open-label审计；显示双方Human text、donor Camera text、Human、Camera与projection，失败row不补位，两条route不合并。
4. 并行在current O0上做HT0／HT1／HTS；caption families与Stage1 observation替换均降为低优先级。
5. 根据RV冻结route-specific规则，再用held-out donors／targets做confirmation；PP通过才构造Rect-64-PP并做exact v9 Stage1 support audit。
6. 在current O0上先运行A0／A-pair；两单轴有信号时补`A0/A-pair × HT0/HT1`，再补A-text排除caption-only解释。PP有效后才训练XH route。
7. A-pair通过后才授权O-series、B0／B1或Rect-320／4096；J64强通过时优先solver-based selection，
   不要求Director链同时成功才报告headroom。
8. 选定架构后才执行multi-seed、Auteur／Pulp／C3对照、ViGen utility、
   blind gold与sealed audit。
9. P0-H不阻塞本地分支；editing与learned bounded staging退出当前queue。

这个顺序先测能力上限和方法必要性，再投入大规模统计预算；不以更多内部
arm代替更强的因果证据。

截至2026-08-01，[ICLR 2027官方作者指南](https://iclr.cc/Conferences/2027/AuthorGuidelines)
给出的abstract／paper deadline为09-18／09-25 AoE。逐周硬门与降级claim规则由
[[DIRECT/2026-08-01_storymotion-multipair-data-training-plan#8. 当前执行顺序]]拥有。

## Appendix I. 拆分前reviewer stress test（2026-07-31，只读历史）

### 9.1 Overall risk verdict

> [!danger] 暂定裁决：高拒稿风险，尚未达到目标标准
> 对“当前证据不足”的判断置信度高；对“最终新颖性是否足够”的判断置信度受限，
> 因为作者尚未亲自冻结StoryMotion相对Auteur、Uni3C与ActCam的各一句核心差异。
> 这不是对未来路线的否定：v11是强且可审计的system baseline，但目标Actor–Director
> claim仍缺少决定性反事实、上限、竞品与sealed evidence。

### 9.2 Major concerns（rejection-level）

| concern | reviewer会否定什么 | 最小repair |
| --- | --- | --- |
| 最近工作边界未闭合 | Auteur已覆盖语言驱动human-relative Camera planning；“三个模式”本身不是足够新颖性 | 作者冻结top-3差异；完成Auteur matched protocol，并把dense reaction／独立双文本写成可测主张 |
| 独立控制合同失败 | N128平均语义响应不能抵消约四成`>5`分的fixed-Camera-text tail | 建立text-owned program、Human event alignment与bounded actor-conditioned Camera residual；原gate、tail、visibility、parent replay同时通过 |
| 联合必要性尚未证明 | 完整双文本接口可由Human generator + Auteur-like planner复现 | J16正信号才扩J64；以hard rescue／vector improvement和Human noninferiority判定，否则降级为Camera-control论文 |
| Actor上限与贡献归属混淆 | Pulp-only Human限制generalization；外部provider收益也不能算StoryMotion贡献 | 明确列为scope limitation；只在超过20% J groups候选不足时做provider sensitivity，每row报告provider／adapter |
| Stage1 observation可能丢失root／event，synthetic support也未知 | H128可能root-dominant；J66 global可能走absolute shortcut | 首轮固定O0完成raw RV与HT；Rect-64-PP只审计exact v9 support。若support失败指向representation，再后置比较H128／H199／J66／Coarse sibling |
| 统计与选择泄漏 | 单训练seed、反复使用pure4,053、fixed demo不足以排除偶然性和test-guided selection | 架构冻结后独立seeds、预注册盲评、新sampling seeds与一次sealed audit |
| 实用性只停留在接口 | Uni3C／ActCam已能消费给定3D控制；接ViGen出视频不证明StoryMotion必要 | 同一renderer／prompt下比较无planner、Auteur／StoryMotion control，评估指令保持、主体可见、轨迹忠实与盲偏好 |

### 9.3 Minor concerns

- 统一使用Actor／Director／Composition，避免Human／Camera／Joint被误读为三个对称
  generator；Direct-C与Composition的Human source必须逐row可见。
- 报告external provider的数据、model license、GPU小时、推理延迟与显存；不能隐藏
  外部先验成本。
- 单独披露Pulp caption／motion质量、长尾动作、不同Camera caption strata与失败样本，
  不把dataset bias包装为method failure或method success。
- physical diagnostics仍不是grounded contact truth；表述保持no-reference heuristic。

### 9.4 Nearest-work gap check

1. **Auteur是最相近方法。** 它已经把human-relative cinematography、稀疏可编辑DSL与
   连续6-DoF解码连成系统。StoryMotion可能的差异只剩独立Actor／Director文本、完整
   3D Human、dense learned reaction及反事实稳定性；这些目前尚未全部被证实。
2. **Uni3C与ActCam是下游control/rendering竞品。** 它们削弱“ViGen缺少Human–Camera
   control”的动机，但不直接取代上游language-to-3D planner。StoryMotion必须用
   downstream utility证明planner带来额外价值。
3. **ViMoGen／Kimodo是Actor prior与下游系统边界。** 它们用于测试Human能力上限或
   control消费，不应与StoryMotion Camera planner混为同一方法表。

在作者冻结top-3一句话差异前，novelty confidence保持`limited`，不得把上述候选差异
提前写成已证实贡献。

### 9.5 Repair paths

- **最短方法repair**：先用`RV-PP25`与`RV-XH25`认识两条route的质量边界，冻结规则后做held-out confirmation；同时只在current O0上短筛HT0／HT1／HTS。随后以Rect-64-PP、exact v9 support与A0／A-pair证明data target效应，再补A-text完成归因。Stage1 observation是后置诊断，A-pair通过后才实现最小$G_T/G_A/G_E$ adapters。
- **最短上限repair**：J16先验证当前Human候选是否足够；只有预注册provider-limited状态
  才接一个外部provider做sensitivity，不进入主模型。
- **最短论文repair**：Actor–Director主叙事、Auteur matched、反事实tail、multi-seed、
  blind study和sealed audit；editing与“foundation model”主张删除。
- **最短实用性repair**：固定一个公开ViGen renderer做等接口A/B，不以best-case视频
  代替随机／最差样本和控制指标。

### 9.6 Re-review checklist

只有以下证据会把裁决从高风险下调：

- 作者亲自冻结StoryMotion相对Auteur／Uni3C／ActCam的top-3一句话差异；
- Director counterfactual原gate与tail均通过，且parent Direct-C／sequential不回退；
- balanced Rect数据、Stage1 support与A-series关闭caption-vs-pair因果问题；
- 若J64进入主claim，natural有效获益率与full-H event evidence达到预注册gate；
- 独立training seeds、盲评、Auteur matched与一次sealed final audit完成；
- clean revision可复现contracts、模型／decoder／provider身份、表格和随机／最差Demo。
