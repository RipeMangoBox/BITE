---
title: "StoryMotion / DIRECT 单仓库双论文边界"
hypothesis: |
  Paper A StoryMotion研究如何在保持冻结Human prior及其输出路径不变的前提下，以
  非对称接口增加observed-H与generated-H Camera generation。Paper B DIRECT研究
  transferable dual-frame cinematographic programs。两篇论文共享StoryMotion代码仓库，
  但各自拥有独立的问题、训练边、artifact解释与claim ledger。
status: active_scope_split
tags:
  - StoryMotion
  - paper-positioning
  - paper/A
  - paper/B
  - DIRECT
  - ICLR/2027
  - CVPR
  - SIGGRAPH
  - status/active
aliases:
  - StoryMotion-Two-Paper-Split
  - StoryMotion-DIRECT-Boundary
source_notes:
  - "[[StoryMotion/current]]"
  - "[[DIRECT/current]]"
  - "[[StoryMotion-iclr-reliability]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]"
  - "[[2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract]]"
  - "[[DIRECT/2026-07-31_storymotion-v11-actor-director-counterfactual-control]]"
  - "[[DIRECT/2026-08-01_storymotion-multipair-data-training-plan]]"
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]]"
  - "[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/Uni3C_Unifying_Precisely_3D-Enhanced_Camera_and_Human_Motion_Controls_for_Video_Generation]]"
created: 2026-08-02T23:22:47+08:00
updated: 2026-08-04T14:51:40+08:00
---

# StoryMotion / DIRECT 单仓库双论文边界

> [!important] 当前决策
> 将当前工作拆成两个独立研究问题：Paper A为 **StoryMotion: Preserving Human Motion
> Priors in Asymmetric Human–Camera Generation**；Paper B为 **DIRECT: Dual-Frame
> Cinematographic Intent Transfer across Articulated Human Motions**。两者目前只使用
> StoryMotion代码仓库；`DIRECT`是论文／方法身份，不是新仓库。DIRECT可以使用Paper A
> 作为冻结backbone，但不能把Paper A的能力保持式非对称框架重新计算为自身贡献。

> [!warning] 成熟度边界
> Paper A已有完整C0-LAT mainline endpoint，C0-GEO保留为audited alternate；剩余核心任务是
> C0-LAT-based ablation收口与Pulp Camera文本修正。Camera data因5090断链暂时暂停；
> 当前先冻结protected-H／relation-interface最小机制检查与Matched Symmetric factorization
> control的参数、exposure及成本合同，不启动旧Independent／Fully-Separate specialist长训。
> H199 decode→re-encode只是可选接口消融，不阻塞能力保持式非对称扩展主张。
> DIRECT只有独立的问题定义，`RV-25`的source reconstruction
> 仍为`0/25`，当前不能写成已经闭环的方法，也不授权Rect或A-series长训。

> [!warning] 证据边界
> “三个模式都SOTA”必须最终限定为同一PulpMotion split、同一评测协议及可比较
> baseline下的best-known结果。正式数字继续只由[[StoryMotion-valid-metric-ledger]]
> 持有；本页只冻结论文问题、贡献边界和审稿防守逻辑。

## 0. 单仓库、双论文轨道

- 唯一代码仓库保持为`linkedCodebases/StoryMotion/`；当前不创建`DIRECT`仓库、镜像仓库或
  第二套公共代码根。
- 论文文档物理分目录：Paper A位于`obsidian-vault/ideas/StoryMotion/`，Paper B位于
  `obsidian-vault/ideas/DIRECT/`；文档分目录不改变代码仓库所有权。
- 新实验在同一`runs/`布局中按论文身份分流：Paper A新run使用`paperA_`前缀，DIRECT新run
  使用`direct_`前缀。已有run ID、checkpoint名和`Actor–Director`诊断名均保持不可变。
- Stage1、decoder、evaluator、run harness与正式metric ledger可以共享；研究问题、positive
  定义、训练授权、结果解释、论文表格与claim不得共享默认值。
- 跨论文复用必须显式写成“冻结的Paper A backbone／shared infrastructure”。同一artifact
  若进入两篇论文，必须分别说明它在各自因果问题中的角色，不能把同一贡献计算两次。
- Paper A状态由[[StoryMotion/current|StoryMotion current]]路由，收口计划由
  [[StoryMotion-iclr-reliability]]拥有；Paper B状态由[[DIRECT/current|DIRECT current]]
  路由，研究合同由[[DIRECT/2026-08-01_storymotion-multipair-data-training-plan]]拥有。

## 1. 两篇工作的核心问题

| 工作 | 核心研究问题 | 主要证据 | 不进入该工作的内容 |
| --- | --- | --- | --- |
| Paper A：StoryMotion | 能否保持强Human prior及其输出路径不变，同时增加observed-H与generated-H Camera generation，并让两条Camera route共享同一个关系感知模型？ | Human逐输出保持、Stage1／Stage2接口、两条Camera route与Pulp正式指标；Camera坐标／文本修正作为次要贡献 | Rect、HML跨配对、Camera program solver、DIRECT数据贡献、ViGen应用突破 |
| Paper B：DIRECT | 如何从factual H-C pair恢复dual-frame cinematographic program，并针对不同完整Human重新执行？ | program ownership、source reconstruction、compatibility、target-H re-execution、multi-pair训练、视觉／用户／下游utility | 重新把StoryMotion三模式与能力保持式框架当作新贡献 |

这不是把一个大系统机械切成上下两半。两篇工作的**因果单位不同**：

- Paper A改变的是模型架构与条件生成接口，事实训练单元仍是Pulp的一对一配对；
- Paper B改变的是监督关系本身，从factual pair扩展为program-conditioned多对多边，
  并要求新的合法性、求解与验证合同。

DIRECT中的`dual-frame`明确指actor／event-relative intent frame与world execution frame：
前者保存可迁移的摄影意图，后者针对目标Human重新求解6-DoF Camera。它不表示source／target
样本的简单跨配对。

## 2. 为什么合并反而削弱两篇工作

### 2.1 Paper A的主语应是能力保持式扩展

Paper A不是“一个新模型同时学会三个任务”，而是一个受保护的非对称扩展：

1. 预训练Human branch拥有$p_H(H\mid T_H)$，在Camera扩展中冻结；
2. 新增的$p_C(C\mid H,T_C)$同时服务observed-H与generated-H；
3. Direct-H是被精确保留的基础能力，Composition是两个分布的顺序组合，不是第三个generator；
4. C0-LAT mainline与C0-GEO alternate的正式结果证明三个接口可运行并形成Camera Pareto；H199 round-trip
   只在正文选择“内部latent接口优于显式Human API”时作为可选消融。

这里的核心问题是：**能否在不污染Human prior的条件下增加Camera composition，并由同一
Camera模型执行两种Human来源。** “三接口”是系统结果，不单独承担新颖性。

### 2.2 DIRECT会改变论文主语

一旦把multi-pair数据、program solver和下游ViGen utility放进同一篇论文，reviewer会自然
把主问题改读为“如何构造可迁移的导演监督”。此时：

- StoryMotion只剩一个被调用的backbone；
- Stage1／Stage2统一设计会被数据构造贡献遮盖；
- Human generation容易退化为给Director提供输入的工具分支；
- 三模式SOTA会被看作第二篇方法的baseline，而不是第一篇的核心证据；
- 论文同时需要回答架构、数据合法性、solver、自然度与下游视频质量，审稿标准失焦。

因此两个方向不是简单相加，而是存在**贡献所有权冲突**。拆分是为了保持两个问题各自
可证伪、可评测，而不是为了增加论文数量。

### 2.3 两篇工作的数据与监督边界图

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 930" width="100%" role="img" aria-labelledby="two-paper-data-title" font-family="Inter, Arial, 'Noto Sans CJK SC', sans-serif">
  <title id="two-paper-data-title">StoryMotion Paper A and DIRECT Paper B data boundary</title>
  <rect x="0" y="0" width="1200" height="930" fill="#ffffff"/>
  <defs><marker id="arrow-data" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#4b5563"/></marker></defs>
  <text x="600" y="28" text-anchor="middle" font-size="22" font-weight="700" fill="#111827">两篇工作的数据与监督边界</text>
  <rect x="430" y="48" width="340" height="54" rx="8" fill="#f3f4f6" stroke="#4b5563" stroke-width="2"/>
  <text x="600" y="80" text-anchor="middle" font-size="17" fill="#111827">Pulp factual: (T_H, H, T_C, C)</text>
  <rect x="28" y="135" width="535" height="700" rx="12" fill="#f8fbff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="295" y="166" text-anchor="middle" font-size="19" font-weight="700" fill="#244b7a">Paper A · capability-preserving StoryMotion</text>
  <rect x="145" y="190" width="300" height="48" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="295" y="219" text-anchor="middle" font-size="15" fill="#10243e">official split + parent-source audit</text>
  <rect x="58" y="270" width="220" height="60" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="168" y="294" text-anchor="middle" font-size="14" fill="#10243e"><tspan x="168">factual H / C / projection</tspan><tspan x="168" dy="19">Stage1 reconstruction</tspan></text>
  <rect x="312" y="270" width="220" height="60" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="422" y="294" text-anchor="middle" font-size="13" fill="#3f2a0d"><tspan x="422">Camera convention + T_C^geo</tspan><tspan x="422" dy="19">keep T_C^raw provenance</tspan></text>
  <rect x="145" y="370" width="300" height="52" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="295" y="392" text-anchor="middle" font-size="15" fill="#3f2a0d"><tspan x="295">frozen cache + stats</tspan><tspan x="295" dy="19">+ owning decoders</tspan></text>
  <rect x="58" y="460" width="220" height="58" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/>
  <text x="168" y="484" text-anchor="middle" font-size="14" fill="#113522"><tspan x="168">Human supervision</tspan><tspan x="168" dy="19">T_H → Human128</tspan></text>
  <rect x="312" y="460" width="220" height="58" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/>
  <text x="422" y="484" text-anchor="middle" font-size="14" fill="#113522"><tspan x="422">Camera supervision</tspan><tspan x="422" dy="19">fixed H + T_C → Camera64</tspan></text>
  <rect x="128" y="563" width="334" height="52" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/>
  <text x="295" y="594" text-anchor="middle" font-size="15" fill="#2c1c48">Direct-H · Direct-C · Sequential H→C</text>
  <rect x="128" y="658" width="334" height="60" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/>
  <text x="295" y="682" text-anchor="middle" font-size="14" fill="#2c1c48"><tspan x="295">Human + Camera + geometry</tspan><tspan x="295" dy="19">+ physical formal metrics</tspan></text>
  <path d="M600 102 L600 118 L295 118 L295 190" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <path d="M295 238 L295 252 L168 252 L168 270 M295 238 L295 252 L422 252 L422 270" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <path d="M168 330 L168 350 L295 350 L295 370" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <path d="M295 422 L295 442 L168 442 L168 460 M295 422 L295 442 L422 442 L422 460 M422 330 L520 330 L520 442 L422 442 L422 460" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <path d="M168 518 L168 540 L295 540 L295 563 M422 518 L422 540 L295 540" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <path d="M295 615 L295 658" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <rect x="637" y="135" width="535" height="700" rx="12" fill="#fffcf5" stroke="#a86b16" stroke-width="2"/>
  <text x="905" y="166" text-anchor="middle" font-size="20" font-weight="700" fill="#74480d">Paper B · DIRECT (exploration)</text>
  <rect x="775" y="190" width="260" height="44" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="905" y="217" text-anchor="middle" font-size="15" fill="#3f2a0d">Pulp Camera donor</text>
  <rect x="755" y="258" width="300" height="50" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="905" y="279" text-anchor="middle" font-size="14" fill="#3f2a0d"><tspan x="905">program + ownership</tspan><tspan x="905" dy="18">+ event extraction</tspan></text>
  <rect x="755" y="334" width="300" height="50" rx="7" fill="#fde7e7" stroke="#a33b3b" stroke-width="2"/>
  <text x="905" y="355" text-anchor="middle" font-size="14" fill="#4a1717"><tspan x="905">source reconstruction gate</tspan><tspan x="905" dy="18">current RV = 0 / 25</tspan></text>
  <rect x="660" y="412" width="205" height="44" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="762" y="439" text-anchor="middle" font-size="14" fill="#3f2a0d">Pulp target-H</text>
  <rect x="945" y="412" width="205" height="44" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="1048" y="439" text-anchor="middle" font-size="14" fill="#3f2a0d">HumanML3D target-H</text>
  <rect x="660" y="484" width="205" height="50" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="762" y="505" text-anchor="middle" font-size="13" fill="#3f2a0d"><tspan x="762">Pulp→Pulp</tspan><tspan x="762" dy="18">compatibility</tspan></text>
  <rect x="945" y="484" width="205" height="50" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="1048" y="505" text-anchor="middle" font-size="13" fill="#3f2a0d"><tspan x="1048">adapter + cross-source</tspan><tspan x="1048" dy="18">compatibility</tspan></text>
  <rect x="785" y="564" width="240" height="46" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="905" y="592" text-anchor="middle" font-size="14" fill="#3f2a0d">target-H Camera re-solve</text>
  <rect x="760" y="638" width="290" height="50" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="905" y="659" text-anchor="middle" font-size="13" fill="#3f2a0d"><tspan x="905">projection · dynamics · event</tspan><tspan x="905" dy="18">· naturalness validation</tspan></text>
  <rect x="785" y="714" width="240" height="46" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="905" y="742" text-anchor="middle" font-size="14" fill="#3f2a0d">masked Rect positive</text>
  <path d="M600 102 L600 118 L905 118 L905 190" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <path d="M905 234 L905 258 M905 308 L905 334" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <path d="M762 456 L762 484 M1048 456 L1048 484" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <path d="M905 384 L905 470 L762 470 L762 484 M905 384 L905 470 L1048 470 L1048 484" fill="none" stroke="#4b5563" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrow-data)"/>
  <path d="M762 534 L762 548 L905 548 L905 564 M1048 534 L1048 548 L905 548" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <path d="M905 610 L905 638 M905 688 L905 714" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <rect x="785" y="783" width="240" height="42" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="905" y="809" text-anchor="middle" font-size="13" fill="#3f2a0d">factual-anchored Director</text>
  <path d="M905 760 L905 783" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-data)"/>
  <rect x="150" y="870" width="900" height="42" rx="7" fill="#fde7e7" stroke="#a33b3b" stroke-width="2"/>
  <text x="600" y="896" text-anchor="middle" font-size="15" fill="#4a1717">Naive H_i + another world C_j → negative / diagnostic only; never positive</text>
</svg>

这张图冻结五个边界：

- Paper A只消费Pulp factual一对一监督；projection与framing由同一对$H,C$计算，
  不是额外数据源；
- Paper A增加Camera坐标／文本修正：由实际extrinsics变化生成无歧义$T_C^{geo}$，保留
  原$T_C^{raw}$与来源。它修复factual监督，不产生跨Human新边；
- Paper B可以复用Pulp作为donor、target-H pool与factual anchor，但必须把新监督归因于
  program extraction、compatibility和target-H re-execution；
- Pulp内部组合与HumanML3D跨源组合走不同compatibility route，不能用一套阈值混判；
- 在source reconstruction与独立验证通过前，不产生Rect positive。HumanML3D motion与
  Pulp原world Camera的直接拼接只允许作为negative或诊断样本。

## 3. 当前正确的Stage1／Stage2分离结构

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1150" width="100%" role="img" aria-labelledby="storymotion-arch-title" font-family="Inter, Arial, 'Noto Sans CJK SC', sans-serif">
  <title id="storymotion-arch-title">StoryMotion Stage1 and Stage2 separated architecture</title>
  <rect x="0" y="0" width="1200" height="1150" fill="#ffffff"/>
  <defs><marker id="arrow-arch" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#4b5563"/></marker></defs>
  <rect x="20" y="35" width="1160" height="375" rx="12" fill="#f8fbff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="600" y="66" text-anchor="middle" font-size="21" font-weight="700" fill="#244b7a">Stage1 · non-causal representation and reconstruction</text>
  <rect x="50" y="92" width="110" height="44" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="105" y="119" text-anchor="middle" font-size="15" fill="#10243e">Human199</text>
  <rect x="50" y="242" width="110" height="44" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="105" y="269" text-anchor="middle" font-size="15" fill="#10243e">Camera14</text>
  <rect x="205" y="82" width="170" height="44" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="290" y="109" text-anchor="middle" font-size="14" fill="#10243e">Human encoder</text>
  <rect x="205" y="150" width="170" height="54" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="290" y="172" text-anchor="middle" font-size="13" fill="#10243e"><tspan x="290">Human–Camera</tspan><tspan x="290" dy="18">interaction encoder</tspan></text>
  <rect x="205" y="240" width="170" height="48" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="290" y="269" text-anchor="middle" font-size="13" fill="#10243e">Camera-base encoder</text>
  <rect x="415" y="82" width="120" height="44" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="475" y="109" text-anchor="middle" font-size="14" fill="#10243e">Human128</text>
  <rect x="415" y="154" width="120" height="44" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="475" y="181" text-anchor="middle" font-size="14" fill="#10243e">interaction16</text>
  <rect x="415" y="242" width="120" height="44" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="475" y="269" text-anchor="middle" font-size="14" fill="#10243e">camera-base48</text>
  <rect x="605" y="205" width="180" height="48" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="695" y="234" text-anchor="middle" font-size="14" fill="#10243e">Camera conditioner</text>
  <rect x="825" y="205" width="130" height="48" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="890" y="226" text-anchor="middle" font-size="13" fill="#10243e"><tspan x="890">conditioned</tspan><tspan x="890" dy="17">camera48</tspan></text>
  <rect x="985" y="120" width="165" height="146" rx="9" fill="#dceaff" stroke="#3769a3" stroke-width="2"/>
  <text x="1068" y="151" text-anchor="middle" font-size="15" font-weight="700" fill="#10243e">Stage1 latent</text>
  <text x="1068" y="183" text-anchor="middle" font-size="13" fill="#10243e">Human128</text>
  <text x="1068" y="207" text-anchor="middle" font-size="13" fill="#10243e">interaction16</text>
  <text x="1068" y="231" text-anchor="middle" font-size="13" fill="#10243e">camera48</text>
  <rect x="735" y="326" width="180" height="46" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="825" y="354" text-anchor="middle" font-size="14" fill="#10243e">owning decoders</text>
  <rect x="950" y="316" width="200" height="66" rx="7" fill="#e8f1ff" stroke="#4f7dbd" stroke-width="2"/>
  <text x="1050" y="340" text-anchor="middle" font-size="13" fill="#10243e"><tspan x="1050">Human199 + Camera14</tspan><tspan x="1050" dy="18">+ framing4 reconstruction</tspan></text>
  <path d="M160 114 L205 104 M160 114 L185 114 L185 177 L205 177 M160 264 L185 264 L185 177 L205 177 M160 264 L205 264" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <path d="M375 104 L415 104 M375 177 L415 176 M375 264 L415 264" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <path d="M535 104 L570 104 L570 229 L605 229 M535 176 L575 176 L575 229 L605 229 M535 264 L575 264 L575 229 L605 229" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <path d="M785 229 L825 229" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <path d="M535 104 L940 104 L940 151 L985 151 M535 176 L985 193 M955 229 L985 229" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <path d="M1068 266 L1068 296 L825 296 L825 326 M915 349 L950 349" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <rect x="400" y="446" width="400" height="58" rx="9" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="600" y="470" text-anchor="middle" font-size="14" fill="#3f2a0d"><tspan x="600">freeze Stage1 owner + decoders</tspan><tspan x="600" dy="19">+ train-only normalization stats</tspan></text>
  <rect x="400" y="536" width="400" height="58" rx="9" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/>
  <text x="600" y="560" text-anchor="middle" font-size="14" fill="#3f2a0d"><tspan x="600">latent cache = Human128 + Camera64</tspan><tspan x="600" dy="19">Camera64 = interaction16 + camera48</tspan></text>
  <path d="M1068 266 L1160 266 L1160 425 L600 425 L600 446 M600 504 L600 536" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <text x="600" y="620" text-anchor="middle" font-size="14" font-weight="700" fill="#74480d">fixed Stage1 boundary ↓</text>
  <rect x="20" y="642" width="1160" height="430" rx="12" fill="#f7fcf9" stroke="#337653" stroke-width="2"/>
  <text x="600" y="674" text-anchor="middle" font-size="21" font-weight="700" fill="#24563d">Stage2 · asymmetric conditional generation</text>
  <rect x="45" y="696" width="340" height="304" rx="10" fill="#ffffff" stroke="#337653" stroke-width="2"/>
  <text x="215" y="724" text-anchor="middle" font-size="18" font-weight="700" fill="#24563d">Direct-H</text>
  <rect x="120" y="748" width="190" height="40" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="215" y="773" text-anchor="middle" font-size="14" fill="#113522">Human text</text>
  <rect x="105" y="817" width="220" height="44" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="215" y="844" text-anchor="middle" font-size="14" fill="#113522">protected Human flow</text>
  <rect x="125" y="890" width="180" height="40" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="215" y="915" text-anchor="middle" font-size="14" fill="#113522">generated Human128</text>
  <rect x="90" y="952" width="250" height="40" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/><text x="215" y="977" text-anchor="middle" font-size="13" fill="#2c1c48">Human decoder → Human199</text>
  <path d="M215 788 L215 817 M215 861 L215 890 M215 930 L215 952" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <rect x="430" y="696" width="340" height="304" rx="10" fill="#ffffff" stroke="#337653" stroke-width="2"/>
  <text x="600" y="724" text-anchor="middle" font-size="18" font-weight="700" fill="#24563d">Direct-C</text>
  <rect x="475" y="748" width="250" height="50" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="600" y="769" text-anchor="middle" font-size="13" fill="#113522"><tspan x="600">observed Human128 (fixed)</tspan><tspan x="600" dy="17">+ Camera text</tspan></text>
  <rect x="490" y="827" width="220" height="44" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="600" y="854" text-anchor="middle" font-size="14" fill="#113522">shared Camera flow</text>
  <rect x="510" y="900" width="180" height="40" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="600" y="925" text-anchor="middle" font-size="14" fill="#113522">generated Camera64</text>
  <rect x="465" y="952" width="270" height="40" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/><text x="600" y="977" text-anchor="middle" font-size="13" fill="#2c1c48">Camera decoder → C14 + framing</text>
  <path d="M600 798 L600 827 M600 871 L600 900 M600 940 L600 952" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <rect x="815" y="696" width="340" height="304" rx="10" fill="#ffffff" stroke="#337653" stroke-width="2"/>
  <text x="985" y="724" text-anchor="middle" font-size="18" font-weight="700" fill="#24563d">Sequential H→C</text>
  <rect x="842" y="748" width="125" height="40" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="904" y="773" text-anchor="middle" font-size="13" fill="#113522">Human text</text>
  <rect x="1002" y="748" width="125" height="40" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="1064" y="773" text-anchor="middle" font-size="13" fill="#113522">Camera text</text>
  <rect x="835" y="815" width="170" height="44" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="920" y="842" text-anchor="middle" font-size="13" fill="#113522">protected H flow</text>
  <rect x="835" y="885" width="170" height="44" rx="7" fill="#fff2d9" stroke="#a86b16" stroke-width="2"/><text x="920" y="904" text-anchor="middle" font-size="12" fill="#3f2a0d"><tspan x="920">generated H128</tspan><tspan x="920" dy="16">then FIX Human</tspan></text>
  <rect x="1018" y="885" width="120" height="44" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="1078" y="904" text-anchor="middle" font-size="12" fill="#113522"><tspan x="1078">same shared</tspan><tspan x="1078" dy="16">Camera flow</tspan></text>
  <rect x="1018" y="950" width="120" height="38" rx="7" fill="#e6f5ec" stroke="#337653" stroke-width="2"/><text x="1078" y="974" text-anchor="middle" font-size="12" fill="#113522">Camera64</text>
  <path d="M904 788 L904 815 M920 859 L920 885 M1002 907 L1018 907 M1064 788 L1064 885 M1078 929 L1078 950" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <rect x="850" y="1010" width="285" height="42" rx="7" fill="#f2eafd" stroke="#7251a5" stroke-width="2"/><text x="992" y="1036" text-anchor="middle" font-size="12" fill="#2c1c48">both decoders → Human199 + C14 + framing</text>
  <path d="M920 929 L920 995 L992 995 L992 1010 M1078 988 L1078 995 L992 995" fill="none" stroke="#4b5563" stroke-width="2" marker-end="url(#arrow-arch)"/>
  <path d="M600 594 L600 625 L215 625 L215 696 M600 594 L600 625 L600 696 M600 594 L600 625 L985 625 L985 696" fill="none" stroke="#4b5563" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arrow-arch)"/>
  <rect x="180" y="1092" width="840" height="42" rx="7" fill="#fde7e7" stroke="#a33b3b" stroke-width="2"/>
  <text x="600" y="1118" text-anchor="middle" font-size="15" fill="#4a1717">No Camera→Human write-back · No evolving-H joint parallel · LAT/GEO differ only in Camera objective</text>
</svg>

图中的边界必须按以下方式解释：

- Stage1负责representation、reconstruction、cache与owning decoder；Stage2不继续更新Stage1；
- Stage2 Camera生成的是`Camera64 = interaction16 + conditioned-camera48`；
- Direct-C读取已观测且固定的Human；sequential先完整生成人物，再固定Human生成Camera；
- formal sequential是两个推理pass，不是第三个joint optimizer phase；
- Camera不回写Human，不重新打开evolving-H joint parallel；
- C0-LAT与C0-GEO共享整套结构，只在Camera objective上不同。

现有文档中，[[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis#1.2 Stage1 精确数据流]]
画出了正确的Stage1实现；但该页[[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis#1.3 Stage2 路由与 Stage1 的边界]]
仍是历史joint-parallel图，不能代表当前v11。以下两个小节只提供v11 Stage2的历史设计依据：
[[2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract#1.5 formal sequential joint 是否意味着 Stage2 只剩两个 phase]]
与[[2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract#3. 活动三模式与诊断模式]]。
当前operational contract仍唯一由StoryMotion仓库的`docs/experiment-contract.md`持有；本节
只解释两篇论文共用的系统边界图。

## 4. Paper A：StoryMotion的能力保持式非对称扩展

### 4.1 一句话定位

> StoryMotion is a non-causal asymmetric framework that unifies text-to-Human
> generation with observed- and generated-Human Camera generation through a
> protected latent interface, preserving the Human prior while sharing one
> relation-aware Camera model across both Camera routes.

中文定位：StoryMotion在保持强Human prior及其输出路径不变的前提下，通过受保护的
非对称接口增加observed-H与generated-H两种Camera generation，并由同一个关系感知
Camera模型执行。重点不是“三接口本身”，也不是同步joint denoising。

### 4.2 建议的主贡献

1. **能力保持式非对称分解。** 用
   $p(H,C\mid T_H,T_C)=p_H(H\mid T_H)p_C(C\mid H,T_C)$定义两个条件分布和三个推理
   接口；Composition是两次采样，不是第三个generator。Camera扩展期间Human owner冻结，
   Camera text不进入Human路径，matched Human seed下Direct-H与Composition必须产生同一$H$。
2. **受保护的关系接口。** `Human128 + interaction16 + camera48`保留Human所有权、
   Human–Camera关系和Camera-native状态；同一个Camera branch同时消费observed与generated
   Human。Direct-H的高质量表述为被保留的基础能力，不计作Camera扩展带来的提升。
3. **Pulp Camera坐标／文本修正。** 固定Camera convention，并根据实际Camera参数变化新增
   无歧义描述；原caption、来源与修订版本全部保留。约16万条数据必须先经过自动几何一致性
   检查，再抽样人工核验。该项是Paper A的次要数据贡献，目前仍是待闭环方案。
4. **三接口实证。** 在统一split、decoder、sample count与正式指标下报告Direct-H、
   Direct-C、Composition、C0-LAT mainline及C0-GEO objective alternate；两endpoint不得按字段
   拼成虚构的单模型。

Stage1可以作为**系统级架构贡献**，但不应在缺少matched component ablation时声称
`interaction16`、conditioner与三阶段schedule中的每一个部件都被单独证明必要。

### 4.3 Paper A主动放弃的claim

- 不把冻结Human branch的Direct-H质量写成统一学习带来的新提升；
- 不声称双向Human–Camera协同或同步joint denoising；
- 不声称独立Actor／Director双文本控制已经闭合；
- 不声称模型学会了可迁移Camera program；
- 不声称达到生产级导演可用性；
- 不声称ViGen没有Camera／Human control；
- 不把RV、Rect、HumanML3D或当前Human-text Camera探索写成主贡献。

## 5. 如何回答“这与串行生成有什么区别？”

### 5.1 先承认事实

StoryMotion的formal joint inference确实是sequential：先生成Human，再生成Camera。
不能用“unified”暗示两者在同一去噪时间轴同步更新，也不能把sequential本身写成新贡献。

### 5.2 当前允许主张的区别

普通串行baseline是两个独立系统在推理时拼接。Paper A当前不主张latent直连必然优于
显式Human API，也不主张统一训练带来参数或正迁移优势。其可审计结构事实是：

- 一个明确的Stage1共享表示与owning decoder合同；
- protected Human owner使Camera训练不改变Direct-H；
- Camera64显式包含interaction与Camera state，而不是仅把独立模型I/O串起来；
- observed-H与generated-H由同一Camera模型执行。

### 5.3 可选H199接口消融

若正文选择“内部latent直连优于显式Human API”这一额外claim，可在冻结相同Stage1、
checkpoint、sampler与评测协议下，把sequential的Human接口替换为
`H128 → D_H → H199 → E_H → H128`，并报告：

- Direct-H保持exact、Direct-C context保持exact；
- sequential Camera semantic与geometry paired差异；
- 额外`D_H + E_H`推理成本。

> [!note] 与主张的关系
> 两条route都保持同一Human owner、Camera branch和$p_Hp_C$顺序分解，因此该消融不决定
> capability-preserving asymmetric extension是否成立；不选择接口优势claim时可以不做。

## 6. 如何回答“这与ViGen Camera control有什么区别？”

### 6.1 任务层级不同

| 系统类别 | 主要输入 | 主要输出 | 核心评价对象 |
| --- | --- | --- | --- |
| StoryMotion Paper A | Human／Camera文字，可选observed Human motion | 显式3D Human motion与6-DoF Camera motion | 结构化motion质量、语义、几何、构图与三接口统一性 |
| Uni3C／ActCam类ViGen control | 参考图像／视频加已给定或已构造的Camera、pose、depth等控制 | 像素视频 | 视频保真度、身份保持、Camera／pose控制精度 |
| Auteur | 已知Human行为加摄影语言／DSL | human-relative Camera plan，再驱动视频生成 | 摄影语言、构图与Camera对Human的响应 |
| Pulp Motion／TSA | Human与Camera运动或其联合分布 | 结构化Human–Camera motion | 多模态一致性、联合运动与构图 |

Uni3C通过对齐点云与SMPL-X控制冻结ViGen，ActCam通过camera-aligned depth／pose做
zero-shot联合控制；它们已经证明ViGen可以消费强3D Camera／Human条件。因此Paper A的
安全差异不是“ViGen做不到控制”，而是：

> ViGen control主要研究**如何遵循给定的控制信号生成视频**；StoryMotion研究
> **如何从语言生成可独立检查、可复用的结构化Human／Camera motion资产**。

Auteur比Uni3C／ActCam更接近DIRECT问题，因为它已经以actor-relative
摄影参数化和DSL生成Camera plan。Pulp Motion与TSA则是Paper A更直接的结构化
Human–Camera generation基线，必须进入相关工作与主表。

### 6.2 Paper A的防守边界

- 可以说显式motion资产可被不同renderer消费；
- 没有matched downstream实验前，不能说StoryMotion改善ViGen；
- 不用像素视频指标与3D motion指标做伪横向SOTA；
- demo负责说明输出可渲染，不负责承担Paper A的全部新颖性；
- 真正的下游utility与可用性证据留给DIRECT。

## 7. Paper B：DIRECT

### 7.1 一句话定位

> 从真实Human–Camera事实配对中提取可迁移的Camera program，筛选满足适用条件的
> 完整Human motion，并针对目标Human重新执行Camera，从而构造可审计的多对多监督，
> 学习Camera intent ownership与Human-conditioned execution。

落脚点不是一般Human–Camera解耦，而是ViGen controller本身通常不负责解决的上游问题：
**哪个摄影意图可以迁移、何时适用，以及如何根据新的完整Human重新求解Camera。**

### 7.2 独立贡献候选

1. Camera program ownership与source reconstruction合同；
2. Human–Program compatibility、event relocalization与target-H re-execution；
3. Pulp内部重组为主证据、HumanML3D跨域重组为可独立失败的扩展；
4. masked rectangular supervision与factual-anchored训练；
5. Human text、Camera text与Human observation的分角色Director架构；
6. matched renderer／ViGen utility、自然度盲评或创作工作流。

当前RV的source reconstruction为`0/25`，所以DIRECT仍处于方法发现期。这个失败不会
反向否定Paper A；它只说明第二篇尚未获得合法multi-pair positive。

### 7.3 CVPR还是SIGGRAPH

| 证据最终落点 | 更自然的目标 | 需要补齐的核心证据 |
| --- | --- | --- |
| 新数据构造算法、learned Director、跨数据泛化与benchmark | CVPR | 大规模自动构造精度、强baseline、跨source泛化、控制与生成指标 |
| 摄影program／solver、可编辑工作流、动画／预演资产与创作者价值 | SIGGRAPH | 高质量视觉、自然度／用户研究、DCC或交互workflow、失败边界与生产可用性 |

Venue不应现在仅按期望选择。先看最终最强证据属于“通用视觉学习方法”还是“摄影／动画
创作系统”，再决定CVPR或SIGGRAPH。

## 8. 两篇论文的防串线合同

| 研究元素 | Paper A：StoryMotion | Paper B：DIRECT |
| --- | --- | --- |
| Pulp factual一对一数据 | 主训练与正式benchmark | factual anchor／donor来源 |
| Pulp Camera坐标／文本修正 | 次要数据贡献：无歧义描述、原文provenance与自动质检 | 作为可靠factual／program输入，不重复计贡献 |
| v9 Stage1与v11 Stage2 | 方法本体 | 冻结backbone或明确baseline |
| protected-H、共享Camera与三接口 | 主方法与系统证据 | 已知父系统，不重复计贡献 |
| RV／Rect／multi-pair | 不进入 | 主方法与数据证据 |
| HumanML3D | 不进入主线 | 跨域Human pool，可独立失败 |
| Human text注入Camera | 不作为Paper A新增贡献 | Director条件设计候选 |
| Camera program solver | 不进入 | 必须先通过source reconstruction |
| ViGen／renderer utility | 仅可选demo与边界说明 | 正式可用性证据 |
| 盲评／用户研究 | 基础视觉可信度 | 自然度、可控性与创作价值主证据 |

第二篇必须：

- 明确引用第一篇并冻结其checkpoint／decoder身份；
- 以`Paper A backbone + factual data`作为baseline；
- 把收益归因于新数据／program／Director机制，而不是再次展示三模式表；
- 使用新的任务、训练边和评价单位，避免形成salami slicing；
- 若最终只剩Human text adapter小改进而multi-pair／program失败，不足以独立成篇。

## 9. Paper A仍需补强什么

“学术工作而非强产品”不妨碍ICLR，但不等于可以只交当前best checkpoint。最低补强包应是：

1. 冻结Pulp Camera convention，生成附带provenance的无歧义caption，并完成自动一致性检查、
   抽样人工核验与canonical directional subset对照；
2. 冻结同协议三接口主表，保证版本、split、sample count、decoder与baseline可比；
3. 按正文实际claim决定是否补最小机制／H199接口消融；
4. 完成sealed audit、随机／最好／最差样本与failure taxonomy；独立训练seed已经闭合；
5. 报告参数、训练成本、推理成本与复现包；production usability留给DIRECT。

## 10. 当前执行裁决

### Paper A：立即收口

- 冻结C0-LAT为后续唯一operational mainline与默认ablation parent；C0-GEO保留audited alternate；
- 停止把DIRECT、Rect和ViGen utility当作Paper A hard blocker；
- 5090断链期间暂停Pulp Camera数据处理，先冻结C0-LAT-based ablation合同；恢复后再继续文本修正；
- H199与最小机制检查只按正文实际claim选择，不进入默认critical path；
- 标题、摘要与contribution围绕capability-preserving asymmetric extension；
- sequential写成factorized joint generation，不写同步或双向协同。

### Paper B DIRECT：继续探索但独立记账

- 先修Camera program extraction与source reconstruction，再讨论Rect规模；
- 当前`0/25`失败保持可审计，不以人工观感覆盖；
- `0.9–1.1`时长兼容与安全裁切只进入新版本数据合同；
- Pulp内部组合先成功，HumanML3D再作为跨域扩展；
- 训练、artifact、指标、文档与claim均使用独立paper identity。

> [!success] 最终边界
> Paper A回答“如何在精确保留Human prior的条件下增加两种Camera generation route”，
> 并以Pulp Camera坐标／文本修正提高基础监督可靠性；DIRECT回答“如何从factual H-C pair
> 恢复dual-frame cinematographic program，并针对不同完整Human重新执行”。前者以能力
> 保持、共享Camera接口与matched证据成立，后者以program合法性、multi-pair学习与可用性成立。
