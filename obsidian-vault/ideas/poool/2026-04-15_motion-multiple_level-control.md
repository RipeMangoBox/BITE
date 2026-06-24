---
created: 2026-04-15T23:16
updated: 2026-04-15T23:16
status: draft
hypothesis: 全局文本语义、body-part 级结构化中间表示与 joint-level 显式控制需要通过统一的层级接口而非平铺拼接来耦合，否则细粒度控制会持续侵蚀整体指令跟随。
source_papers:
  - '[[paperAnalysis/Motion_Generation/ICLR_2023/2023_LGTM_Local_to_Global_Text_Driven_Human_Motion_Diffusion_Models|LGTM]]'
  - '[[paperAnalysis/Motion_Generation/TPAMI_2024/2024_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generation|GUESS]]'
  - '[[paperAnalysis/Motion_Generation/ICCV_2023/2023_AttT2M_Text_Driven_Human_Motion_Generation_with_Multi_Perspective_Attention_Mechanism|AttT2M]]'
  - '[[paperAnalysis/Motion_Generation/ICCV_2023/2023_Fg_T2M_Fine_Grained_Text_Driven_Human_Motion_Generation_via_Diffusion_Model|Fg-T2M]]'
  - '[[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]'
  - '[[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]]'
  - '[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval|PST]]'
  - '[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]'
  - '[[paperAnalysis/Motion_Generation/TPAMI_2023/2023_MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model|MotionDiffuse]]'
  - '[[paperAnalysis/Motion_Generation/ICCV_2023/2023_GMD_Guided_Motion_Diffusion_for_Controllable_Human_Motion_Synthesis|GMD]]'
  - '[[paperAnalysis/Motion_Generation/ECCV_2024/2024_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis|TLControl]]'
  - '[[paperAnalysis/Motion_Generation/CVPR_2024/2024_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tasks|ProgMoGen]]'
  - '[[paperAnalysis/Motion_Generation/ICLR_2025/2025_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control|DART]]'
  - '[[paperAnalysis/Motion_Generation/ICCV_2025/2025_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control|SFControl]]'
  - '[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]'
  - '[[paperAnalysis/Image_Video_Generation/arXiv_2026/2026_Self_Swap_Guidance_Diffusion_Token_Perturbation|SSG]]'
tags:
  - paper-idea
  - Motion_Generation
  - controllable-generation
  - fine-grained-alignment
  - multi-level-control
---
# 2026-04-15 动作生成：语义层级控制 × joint-level 显式控制

> 基于 `paperAnalysis/` 本地知识库检索后的想法整理。核心目标不是再做一个“更细粒度的 text-to-motion”，而是解决一个更具体也更难的问题：**如何同时保住全局文本指令跟随、body-part 级语义分配，以及 joint-level 显式控制（如轨迹、关键点、局部路径）**。
>
> 共享母题：与 codebook 对齐、统一 MotionLLM、token-level operator 重合的背景已抽到 [[2026-04-16_structured-alignment-multi-level-control-shared-frame|2026-04-16 结构化对齐与多层控制共享框架]]。本文聚焦“层级控制接口”这一主张。

---
## 1. 目标重述

我想做的不是单纯的“细粒度控制”，而是**多层级控制的一致化**：

1. **全局层**：文本给出动作的整体意图、风格、事件顺序、节奏。
2. **部位层**：模型知道哪一段语义主要落在哪个 body part 上。
3. **关节层**：用户还能对少数 joint 给出显式几何信号，例如轨迹、关键帧、目标点、路径约束。

理想状态下，这三层不是互相竞争，而是形成一个自上而下的约束链：

- 全局文本决定“做什么”
- body-part 分解决定“谁来做”
- joint-level 控制决定“具体怎么走”

现在大多数方法只能覆盖其中一到两层，**缺少统一接口**。

---
## 2. 真正的难点

### 2.1 粗粒度语义与 joint-level 精确控制天然张力很大

- 动作表征越细，从 holistic rep 到 body-part rep 再到 joint-level rep，低层控制会越来越精确；
- 但文本和动作之间的天然对应关系并不是逐关节的，而是偏事件级、部位级、相对结构级；
- 一旦直接把文本强行压到 joint-level，模型就会面对一个困难问题：
  **文本里没有显式给出的关节细节，到底该由语义补全，还是由几何控制覆盖？**

### 2.2 当前方法大多把“语义分解”和“几何控制”当成两条独立路线

- 语义分解方法更关注 text-to-motion alignment；
- 几何控制方法更关注 trajectory/keyframe/waypoint accuracy；
- 两者的中间接口往往缺失，所以最后只能做“文本条件 + 外部控制信号拼接”，而不是层级一致的控制。

### 2.3 缺少冲突仲裁机制

真正麻烦的不是“同时给两个条件”，而是：

- 文本说“右手自然摆动”，控制信号却要求右手沿一条强约束轨迹运动；
- 文本说“慢慢走向前方”，joint/path control 却要求快速转弯；
- 文本只描述上半身语义，但控制信号落在下肢轨迹上。

现有系统通常没有显式回答：
**哪一层优先？冲突怎么局部化？哪些 joint 应该被强控，哪些 joint 应该自由补全？**

---
## 3. 检索后的相关工作地图

### 3.1 语义层级控制：解决“文本如何分层”，但还没到 joint-level

- [[paperAnalysis/Motion_Generation/ICLR_2023/2023_LGTM_Local_to_Global_Text_Driven_Human_Motion_Diffusion_Models|LGTM]]
  - `core_operator`: LLM-based decomposition of global text into part-level descriptions + local body-part motion encoders + global refinement diffusion
  - 价值：第一次比较清楚地把“全局文本 -> body-part 子描述 -> 全身融合”串起来。
  - 不足：它的最细粒度停在 **body-part**，没有自然落到 joint-level 显式控制接口。

- [[paperAnalysis/Motion_Generation/ICCV_2023/2023_AttT2M_Text_Driven_Human_Motion_Generation_with_Multi_Perspective_Attention_Mechanism|AttT2M]]
  - `core_operator`: BPST VQ-VAE codebook + Global-Local Attention for word-level and sentence-level alignment
  - 价值：把词级局部对齐和句级全局对齐分开建模，说明“局部语义”和“整体语义”确实需要不同接口。
  - 不足：局部对齐仍主要是 **词级到子动作级**，不是 joint 级控制。

- [[paperAnalysis/Motion_Generation/ICCV_2023/2023_Fg_T2M_Fine_Grained_Text_Driven_Human_Motion_Generation_via_Diffusion_Model|Fg-T2M]]
  - `core_operator`: dependency-tree GAT for hierarchical text features + progressive reasoning in diffusion
  - 价值：强调文本内部本身就有层级结构，先全局再局部地推理更适合细粒度词汇。
  - 不足：它细化的是 **文本理解层**，不是控制接口层。

- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]
  - `core_operator`: 多粒度协同预训练，粗粒度任务辅助细粒度理解，细粒度任务反哺全局语义
  - 价值：证明粗/细粒度任务之间确实可以互为脚手架，而不是单纯互相干扰。
  - 不足：它的细粒度主要是 **motion script（时间段 × 体部）**，仍不是 explicit joint control。

- [[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]]
  - `core_operator`: 三级文本条件（序列/动作/部位）联合条件化，实现 part-level 组合生成
  - 价值：把部位级控制真正推进到了更强的组合生成阶段，说明 body-part 级结构是有效的控制中间层。
  - 不足：仍缺一个从 part-level 继续下钻到 joint-level 几何接口的桥。

- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval|PST]]
  - `core_operator`: 关节级 -> 片段级 -> 整体级的金字塔式 Shapley-Taylor 对齐学习
  - 价值：非常重要的证据。它证明**joint、segment、holistic 三层对齐都是真实存在且可学习的**。
  - 不足：PST 是检索/对齐框架，不是生成框架。它告诉我们“可以这样对齐”，但还没有告诉我们“如何这样生成”。

### 3.2 几何显式控制：解决“怎么精确约束”，但通常对语义是盲的

- [[paperAnalysis/Motion_Generation/ICCV_2023/2023_GMD_Guided_Motion_Diffusion_for_Controllable_Human_Motion_Synthesis|GMD]]
  - `core_operator`: Emphasis Projection + Dense Signal Propagation
  - 价值：很好地说明轨迹/关键帧控制失败的根源之一是**高维运动表示中控制信号过稀疏**。
  - 不足：它关心的是“如何让控制信号有效传播”，而不是“这个信号与文本语义是什么关系”。

- [[paperAnalysis/Motion_Generation/ECCV_2024/2024_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis|TLControl]]
  - `core_operator`: trajectory+language coarse proposal + test-time optimization refinement in part-structured latent space
  - 价值：明确提出语言和轨迹可以同时控制，而且 part-structured latent 很关键。
  - 不足：它更像“先生成 plausible motion，再做几何投影修正”，不是层级语义一致建模。

- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tasks|ProgMoGen]]
  - `core_operator`: 将控制任务编程为可微误差函数，优化扩散潜变量
  - 价值：说明 joint-level / geometry-level 控制完全可以被抽象成外部约束语言。
  - 不足：控制语言是“优化目标语言”，不是“语义分层语言”。它不解决 global text 和 local control 的对齐关系。

- [[paperAnalysis/Motion_Generation/ICLR_2025/2025_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control|DART]]
  - `core_operator`: motion primitive latent diffusion + autoregressive rollout + latent-space control
  - 价值：说明实时控制、长程控制、空间控制可以统一到原语级潜空间里。
  - 不足：控制更偏“空间任务执行”，不是 semantic hierarchy。

- [[paperAnalysis/Motion_Generation/ICCV_2025/2025_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control|SFControl]]
  - `core_operator`: 先关键关节轨迹综合，再全身补全，解耦可控性与质量
  - 价值：非常接近这个想法的 joint-level 一侧。它证明把 low-level control 限制在 **关键关节子空间** 是合理的。
  - 不足：Stage 1 的 keyjoint 目标来自外部约束，不来自文本层级分解，因此缺少“为什么控制这些 joint”的语义闭环。

- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]
  - `core_operator`: root/body 两阶段解耦 + 多类运动学约束统一注入
  - 价值：展示了大规模 controllable generation 可以统一支持关键帧、稀疏关节、2D path、foot contact。
  - 不足：它的控制类型极强，但控制与语义的联系更多是“共同输入”，不是层级因果链。

- [[paperAnalysis/Motion_Generation/TPAMI_2023/2023_MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model|MotionDiffuse]]
  - `core_operator`: 噪声插值实现体部独立控制和时变控制
  - 价值：早期就指出 body-part control 不是 impossible，而是可以通过结构化推理时组合实现。
  - 不足：它解决的是“不同文本控制不同体部”，不是“joint-level 显式几何控制”。

### 3.3 表征与桥接基础：提供了可能的底座，但还没把三层串起来

- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]
  - `core_operator`: 逐关节 token 的 2D 潜空间网格 + 统一条件注入
  - 价值：这是目前最强的 **joint-level 表征底座** 之一。它说明关节级 latent 不只是“更细”，而是显著更好。
  - 不足：PRISM 强在表示和统一生成模式，不强在 semantic hierarchy；它还没有定义“全局文本 -> body-part -> joint token”的控制谱系。

- [[paperAnalysis/Motion_Generation/TPAMI_2024/2024_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generation|GUESS]]
  - `core_operator`: cascaded latent diffusion across multi-scale skeleton abstractions
  - 价值：说明 coarse-to-fine skeleton abstraction 是有效的，尤其适合把“先整体后细节”做成结构化生成流程。
  - 不足：它的 coarse-to-fine 更偏 **生成粒度递进**，不是 **语义控制递进 + 几何控制递进** 的统一版本。

---
## 4. 反思：现有工作共同缺了什么

### 4.1 缺少一个“层级控制接口”，而不是缺少某一层能力

检索完之后，一个更清楚的判断是：

- 不是没有 **body-part 语义控制**
- 不是没有 **joint-level 显式控制**
- 不是没有 **joint-level 表征**

真正缺的是：
**从全局文本到部位语义，再到 joint-level control slots 的统一接口。**

也就是说，现有工作各自会做：

- `text -> part script`
- `constraint -> keyjoint trajectory`
- `joint tokens -> high-quality motion`

但很少有人做：

- `global text -> part script -> selected joint anchors -> full-body motion`

### 4.2 语义路线和控制路线停在不同中间层

- 语义路线一般停在句子、短语、body-part、time segment；
- 控制路线一般起于 keyjoint、trajectory、waypoint、constraint mask；
- 两条路线中间没有稳定的“翻译层”。

这意味着系统只能依赖启发式：

- 把文本 embedding 和 control embedding 拼接；
- 或者在推理时后处理地强行满足控制。

这不是“层级控制”，而是“条件堆叠”。

### 4.3 缺少不确定性分配

joint-level 控制不应该覆盖所有关节、所有时间、所有自由度。

更合理的逻辑应该是：

- 文本强约束的部分，保留 semantic priority；
- 用户显式给 signal 的 joint/time slot，保留 control priority；
- 没有明确约束的自由度，交给生成器补全。

但现有方法通常没有显式建模：

- 哪些关节应该被强控；
- 哪些只是由文本弱约束；
- 哪些完全自由生成。

### 4.4 缺少跨层一致性评测

目前评测往往二选一：

- 要么看 text-motion 对齐；
- 要么看 trajectory / keyframe 误差。

但如果目标是多层级控制，就应该同时问：

1. 全局文本语义是否还在？
2. body-part 级语义是否分配正确？
3. joint-level 显式信号是否满足？
4. 在满足 joint-level 控制后，是否伤害了 1 和 2？

这类“层级保持曲线”现在几乎没人测。

---
## 5. 一个更清晰的研究主张

### 5.1 核心假设

**不要直接把文本压到 joint-level，也不要直接把 joint control 拼回全局生成器。**

更合理的路线应该是：

1. **全局文本规划层**
   - 生成 sequence-level action plan；
   - 决定整体意图、时间结构、动作顺序。

2. **body-part 语义分配层**
   - 将全局语义拆成 `time × body-part` 的结构化控制脚本；
   - 类似 LGTM / MG-MotionLLM / FrankenMotion 的中间表示，但要更明确地服务下游 joint control。

3. **joint anchor grounding 层**
   - 只把需要精确控制的部位/时间段下钻到 joint-level；
   - 生成 sparse joint anchors，如关键点、轨迹、姿态 token、mask。

4. **joint-level 执行层**
   - 在 PRISM 这类逐关节 latent 上执行生成；
   - joint anchors 是强约束，其余 joint/token 由模型补全。

5. **跨层反射层**
   - 从生成结果反推出 body-part script / global summary；
   - 检查 global text、part script、joint signal 是否一致；
   - 出现冲突时只局部修正对应层级，而不是整段重采样。

### 5.2 关键不是“更细”，而是“只在必要处更细”

这个方向如果要成立，必须避免一个常见误区：
**不是所有语义都应该被 joint 化。**

更好的形式应该是“选择性下钻”：

- 高层文本保留抽象；
- body-part 层负责定位控制责任；
- joint 层只接管真正需要显式几何约束的局部。

这会比“全文本 -> 全 joint”更稳定，也更符合用户真实使用方式。

---
## 6. 为什么这个方向有意义

### 6.1 学术意义

它直指一个现在还没被很好解决的核心问题：
**细粒度可控性和整体语义一致性如何共存。**

如果这个问题解决了，贡献不会只是“一个更强 controllable motion generator”，而是：

- 给 motion generation 引入真正的 **hierarchical control interface**；
- 把“语义对齐”和“几何控制”从两条路线合成一条路线；
- 让 future work 可以在统一接口上扩展 contact、scene、object、human-human interaction 等更多控制源。

### 6.2 实用意义

真实用户想要的往往是这种混合式指令：

- “向前走，同时右手挥手，但右脚沿这条路径走”
- “坐下时左手扶桌边，身体保持转向观众”
- “整体像跳舞，但某只手在这几个时间点到达指定位置”

这类需求天然就是多层级控制，不是纯文本，也不是纯 trajectory。

---
## 7. 可能的最小可行方案

如果真往实验方向推进，一个更现实的 MVP 不是一步到位做完整系统，而是：

1. **表示层**：采用 [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 式 joint-level latent 作为底座。
2. **语义层**：采用 [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]] / [[paperAnalysis/Motion_Generation/CVPR_2026/2026_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition|FrankenMotion]] 风格的 `time × body-part` script 作为中间层。
3. **控制层**：借鉴 [[paperAnalysis/Motion_Generation/ICCV_2025/2025_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control|SFControl]]，只对少量 keyjoint 建立显式控制通道。
4. **对齐层**：借鉴 [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval|PST]] 的 multi-scale alignment 思想，检查 joint / segment / holistic 三层一致性。

这样可以先回答一个最小问题：

> 当 joint-level 控制逐渐增强时，global text fidelity 会如何退化？  
> 如果加上 body-part 中间层，这个退化能否显著减缓？

这会是一个很干净、也很有论文味道的问题。

---
## 8. 可以进一步明确的研究问题

### RQ1

body-part script 是否真的是 global text 和 joint-level control 之间最合适的中间层？

### RQ2

joint-level 控制应该作用在：

- 关节位置
- 关节旋转
- root/path
- 还是 latent anchor

哪一种最不伤害全局语义？

### RQ3

当文本和 joint control 冲突时，应该：

- semantic priority
- control priority
- 还是 uncertainty-aware arbitration

哪种更合理？

### RQ4

是否能定义一条 **hierarchical control frontier**：

- x 轴是 joint-level control strength
- y 轴是 global semantic fidelity

优秀方法应当把 frontier 往右上角推，而不是只优化某一个点。

---
## 9. 可能有借鉴作用的跨域算子

- [[paperAnalysis/Image_Video_Generation/arXiv_2026/2026_Self_Swap_Guidance_Diffusion_Token_Perturbation|SSG]]
  - 图像里用 token swap 构造“精细但不粗暴”的扰动分支。
  - 对这个方向的启发是：如果 future motion backbone 采用 joint-token transformer，那么也许可以在推理时做 **joint-token / temporal-token 的受控交换**，把它当成一种一致性 stress test 或 guidance 信号。
  - 这不是主线，但可能是很好的 inference-time diagnostic / refinement 工具。

---
## 10. 当前结论

目前最清楚的一句话总结是：

**这条线的空白不在于“还没人做细粒度控制”，而在于还没人把 semantic hierarchy 和 explicit joint control 真的接成同一条控制链。**

更具体地说：

- semantic papers 解决了“文本怎么拆”
- controllable papers 解决了“约束怎么打”
- representation papers 解决了“joint-level 怎么表示”

但还缺一个工作，把三者合成：

> `global text -> body-part script -> sparse joint anchors -> joint-level generation -> cross-level reflection`

这可能才是“multiple-level control”真正值得做的版本。
