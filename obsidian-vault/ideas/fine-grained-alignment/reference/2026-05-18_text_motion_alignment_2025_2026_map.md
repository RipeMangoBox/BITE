---

## title: "2025-2026 提高 Text-Motion Alignment 工作梳理"
created: 2026-05-18T19:41:07+08:00
updated: 2026-05-18T19:41:07+08:00
tags:
  - Motion_Generation
  - text-motion-alignment
  - motion-language-retrieval
  - venue-audit
  - status/curated
category: Motion_Generation
source_log: paperAnalysis/analysis_log.csv

# 2025-2026 提高 Text-Motion Alignment 工作梳理

> [!abstract] **结论先行**
>
> 这次我按两个口径筛：
>
> 1. **直接提高 text-to-motion alignment**：reward / preference / event decomposition / fine-grained text conditioning / better text-conditioned latent space。
> 2. **alignment 邻近工作**：motion-language pretraining / retrieval / caption denoising / retrieval-augmented generation。这类工作不一定直接改 T2M generator，但会明显影响 text-motion 对齐上限或评测。
>
> 本地 `analysis_log.csv` 里 2025-2026 年与这条主线最相关的条目，核心应优先关注：
>
> - **2025**：AToM, MotionCritic, SoPo, Fg-T2M++, MotionFlux, IRG-MotionLLM, LaMP, ReMoGPT
> - **2026**：MoLingo, ReAlign, Event-T2M, Motion-R1, COME, FineXtrol, LaMoGen, PST, MoCHA, MaxSim
> - **2026 且目前本地仍偏 arXiv / 未完全回填 venue 的，也值得盯住**：OpenT2M, CLAW, Kimodo

## 1. 筛选口径

### 1.1 纳入

- 题目或方法明确指向 `alignment / aligned / retrieval / captioning / preference / reward / event-level / fine-grained text / motion-language`
- 或者是 **明显用于改善 text-conditioned motion fidelity** 的方法，即使标题不直接写 alignment
- 2026 年中，即使本地仍写成 `arXiv` / `unknown_2026`，只要属于 motion-language / text-to-motion 主线，也保留

### 1.2 不纳入

- 纯 motion generation 扩规模，但和 text-motion 对齐关系太弱
- 纯 motion editing / retargeting / tracking，除非方法显式围绕文本对齐

## 2. 2025：直接提高 T2M alignment 的主线


| Paper         | Venue / year | analysis_log | 本地状态       | 为什么相关                                         |
| ------------- | ------------ | ------------ | ---------- | --------------------------------------------- |
| AToM          | CVPR 2025    | 1217         | checked    | 事件级 reward，对完整性/顺序/频率做对齐                      |
| MotionCritic  | ICLR 2025    | 1300         | Downloaded | 用 human perception critic 纠正生成质量与主观对齐         |
| SoPo          | NeurIPS 2025 | 1324         | checked    | 半在线 preference optimization，直接优化 T2M 偏好对齐     |
| Fg-T2M++      | IJCV 2025    | 2108         | Downloaded | 细粒度文本驱动生成，LLM 增强细节语义                          |
| MotionFlux    | arXiv 2025   | 1185         | Downloaded | TAPO preference alignment + rectified flow    |
| IRG-MotionLLM | arXiv 2025   | 1183         | checked    | generation-assessment-refinement 闭环，提高文本语义忠实度 |


### 2.1 2025 的 alignment 邻近工作


| Paper   | Venue / year | analysis_log | 本地状态    | 为什么相关                                                              |
| ------- | ------------ | ------------ | ------- | ------------------------------------------------------------------ |
| LaMP    | ICLR 2025    | 1298         | checked | language-motion pretraining，统一 generation / retrieval / captioning |
| ReMoGPT | AAAI 2025    | 1177         | checked | part-level retrieval augmentation，增强细粒度 motion-language 对齐         |


### 2.2 2025 重点备注

- **AToM** 是 2025 里最明确的 alignment 论文之一，核心是事件级 reward。
  - 笔记：[[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward]]
- **MotionCritic** 更偏“人类感知对齐”，不是纯文本对齐，但对生成质量与主观 semantic faithfulness 很重要。
  - 笔记：[[paperAnalysis/Motion_Generation/ICLR_2025/2025_MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions]]
- **SoPo / MotionFlux** 都属于 preference-alignment 线，和 AToM 一样值得放进一个子脉络里看。
  - SoPo 笔记：[[paperAnalysis/Motion_Generation/NeurIPS_2025/2025_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization]]
- **LaMP / ReMoGPT** 更像“alignment 表征层”和“检索增强层”的重要基线。

## 3. 2026：直接提高 T2M alignment 的主线


| Paper     | 当前建议 venue 状态 | analysis_log | 本地状态    | 为什么相关                                                               |
| --------- | ------------- | ------------ | ------- | ------------------------------------------------------------------- |
| MoLingo   | CVPR 2026     | 1238         | checked | 直接做 motion-language alignment，语义对齐潜空间 + multi-token cross-attention |
| ReAlign   | AAAI 2026     | 1180         | checked | step-aware reward-guided alignment                                  |
| Event-T2M | ICLR 2026     | 1305         | checked | event-level conditioning，专治复杂文本多事件对齐                                |
| Motion-R1 | ICLR 2026     | 1184         | checked | CoT + RL binding，强化语义忠实度                                            |
| COME      | ICLR 2026     | 1303         | checked | ccDIT + better representation，提升细粒度 text-conditioning               |
| FineXtrol | AAAI 2026     | 1179         | checked | fine-grained text control                                           |
| LaMoGen   | CVPR 2026     | 1237         | checked | 符号推理把文本语义拆成可控动作单元                                                   |


### 3.1 2026 的 alignment 邻近工作


| Paper                         | 当前建议 venue 状态 | analysis_log | 本地状态       | 为什么相关                                                       |
| ----------------------------- | ------------- | ------------ | ---------- | ----------------------------------------------------------- |
| PST / Beyond Global Alignment | ICML 2026     | 1348 / 2085  | Downloaded | 细粒度 motion-language retrieval，多尺度局部对齐                       |
| MoCHA                         | 暂按 arXiv 2026 | 1347         | checked    | caption supervision denoising，降低 text noise，提高 retrieval 对齐 |
| MaxSim                        | 暂按 arXiv 2026 | 1346         | Downloaded | token-patch late interaction，做可解释细粒度对齐                      |


### 3.2 2026 仍应额外盯住的 arXiv / data-centric motion 工作


| Paper   | 当前建议 venue 状态               | analysis_log | 本地状态       | 为什么仍值得关注                                                   |
| ------- | --------------------------- | ------------ | ---------- | ---------------------------------------------------------- |
| OpenT2M | 大概率 CVPR 2026，但本地未回填        | 1996         | Downloaded | 大规模高质量数据直接影响 alignment 上界                                  |
| CLAW    | 暂按 arXiv 2026               | 2004         | Downloaded | composable language-annotated whole-body motion，数据与控制接口强相关 |
| Kimodo  | 暂按 arXiv / tech report 2026 | 1187         | checked    | 大规模 controllable motion generation，可能成为强数据/模型底座            |


## 4. 我建议优先读的 12 篇

如果目标是系统梳理“**提高 text-motion alignment** 的方法脉络”，建议先按这个顺序：

1. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward]]
2. [[paperAnalysis/Motion_Generation/ICLR_2025/2025_MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions]]
3. [[paperAnalysis/Motion_Generation/NeurIPS_2025/2025_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization]]
4. [[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning]]
5. [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models]]
6. [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation]]
7. [[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment]]
8. [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis]]
9. [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Motion_R1_Enhancing_Motion_Generation_Decomposed_CoT_RL_Binding]]
10. [[paperAnalysis/Motion_Generation/ICLR_2026/2026_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation]]
11. [[paperAnalysis/Motion_Generation/arXiv_2026/2026_MoCHA_Denoising_Caption_Supervision_Motion_Text_Retrieval]]
12. [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval]]

## 5. 2026 venue / status 核验结果

这里区分三类：

### 5.1 已较明确

- **MoLingo -> CVPR 2026**
  - 外部可检索页面已把它列在 `CVPR 2026 / Human Understanding` 下。
- **PST / Beyond Global Alignment -> ICML 2026**
  - 题目已出现在 `icml.cc/Downloads/2026` 列表里。
- **ReAlign -> AAAI 2026**
  - 本地 `analysis_log.csv` 已写 AAAI 2026，本地笔记也按 AAAI 2026 整理。
- **Event-T2M / Motion-R1 / COME -> ICLR 2026**
  - 本地路径与笔记均已是 ICLR 2026 主线。

### 5.2 高概率已更新，但本地还没回填干净

- **OpenT2M**
  - 发现冲突信息：
    - OpenReview 上有 **ICLR 2026 withdrawn submission**
    - 作者/实验室主页当前又把它列为 **CVPR 2026**
  - 因此更合理的处理是：
    - 在这份笔记里先记为 **“大概率 CVPR 2026，需最终人工二次确认后再改 log”**
    - 不建议直接无备注覆盖 `analysis_log.csv`

### 5.3 目前仍应视为 arXiv / preprint

- **MoCHA**
- **MaxSim**
- **CLAW**
- **Kimodo**

我这次没有查到足够强的官方会议信息来证明它们已经被 2026 某个正式 venue 接收，因此这里先保守地继续按 `arXiv / preprint / tech report` 处理。

## 6. 本地 metadata 漂移与重复项

### 6.1 `analysis_log.csv` 建议回填的地方


| line | 当前记录                      | 建议                            |
| ---- | ------------------------- | ----------------------------- |
| 1184 | Motion-R1 = `arxiv 2025`  | 应回填为 `ICLR 2026`              |
| 1191 | ActionPlan = `arXiv_2026` | 路径已在 `CVPR_2026`，应统一 venue 格式 |
| 1346 | MaxSim = `unknown_2026`   | 先改成 `arXiv 2026` 更合适          |
| 1347 | MoCHA = `unknown_2026`    | 先改成 `arXiv 2026` 更合适          |
| 1348 | PST = `unknown_2026`      | 应回填 `ICML 2026`               |
| 1996 | OpenT2M = `arXiv 2026`    | 暂记“待确认 CVPR 2026”更稳妥          |
| 2085 | Beyond Global Alignment   | 与 1348 高度疑似重复，建议合并核对          |


### 6.2 笔记层的漂移

- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation]]
  - frontmatter 里 `venue: arXiv`，但文件路径和 `analysis_log.csv` 都是 `ICLR 2026`
- [[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment]]
  - 文件名保留了 `Bilingual` 版本，但笔记标题是 `ReAlign: Text-to-Motion Generation via Step-Aware Reward-Guided Alignment`
- [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation]]
  - 文件名是 `Text_to_Motion_Generation`，笔记标题是 `Text-to-Human Motion Generation`

## 7. 这份梳理里最值得补分析的“仅下载未分析”条目

优先级建议：

1. **PST**：已经基本可视为 `ICML 2026`，但本地还是 `Downloaded`
2. **MotionFlux**：preference alignment 主线里很关键
3. **Fg-T2M++**：2025 细粒度文本生成线，适合和 FineXtrol / MoLingo 对照
4. **OpenT2M**：虽然更偏数据，但 2026 主线影响很大
5. **MaxSim**：和 PST / MoCHA 组成 retrieval 细粒度对齐三件套
6. **CLAW**：如果后续要看 whole-body / robotics 方向的 language-annotated motion，这篇要补

## 8. 外部核验来源

- ICML 2026 Downloads: [https://icml.cc/Downloads/2026](https://icml.cc/Downloads/2026)
- PST arXiv: [https://arxiv.org/abs/2601.21904](https://arxiv.org/abs/2601.21904)
- MoCHA arXiv: [https://arxiv.org/abs/2603.23684](https://arxiv.org/abs/2603.23684)
- MaxSim arXiv: [https://arxiv.org/abs/2603.09930](https://arxiv.org/abs/2603.09930)
- OpenT2M OpenReview: [https://openreview.net/forum?id=YcJnHKVB9v](https://openreview.net/forum?id=YcJnHKVB9v)
- OpenT2M 作者主页条目: [https://z0ngqing.github.io/publication/](https://z0ngqing.github.io/publication/)
- OpenT2M 项目页: [https://research.beingbeyond.com/opent2m](https://research.beingbeyond.com/opent2m)
- Kimodo 项目页: [https://research.nvidia.com/labs/sil/projects/kimodo/](https://research.nvidia.com/labs/sil/projects/kimodo/)
- Kimodo arXiv: [https://arxiv.org/abs/2603.15546](https://arxiv.org/abs/2603.15546)
- CLAW arXiv: [https://arxiv.org/abs/2604.11251](https://arxiv.org/abs/2604.11251)
- MoLingo 外部 CVPR 2026 收录页: [https://en.papernotes.org/CVPR2026/human_understanding/molingo_motion-language_alignment_for_text-to-motion_generation/](https://en.papernotes.org/CVPR2026/human_understanding/molingo_motion-language_alignment_for_text-to-motion_generation/)

