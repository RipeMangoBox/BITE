---
created: 2026-04-16T00:00
updated: 2026-04-17T00:00
tags:
  - rule-insight
  - motion-text-alignment
  - granularity
  - representation
---
# Motion-Text 粒度与对齐

## Q1：PRISM 对 text 是否有与 joint-level 对应的细化处理？

**没有。** PRISM 的文本处理是标准的全局编码：T5-XXL 编码整句文本 → cross-attention 注入 DiT。motion 侧精细到 23 个 joint token，但 text 侧仍是全局语义向量。

这意味着 PRISM 的 motion-text 交互存在**粒度不对称**：
- Motion：每帧 23 个 joint token，每个 token 有明确的解剖学语义（左肘、右膝…）
- Text：T5-XXL 输出的 token 序列是语言学分词（subword），不对应任何身体部位或时间段

PRISM 依赖 cross-attention 隐式学习"哪些 text token 应该关注哪些 joint token"，但没有显式的粒度对齐机制。这是一个明确的设计空白。

## Q2：粒度对齐是否是 motion-language alignment 的前提？

**是必要条件，但不是充分条件。** 从 KB 中的证据链来看：

1. **全局对齐的天花板已经可见**：
   - [[2026_MoCHA_Denoising_Caption_Supervision_Motion_Text_Retrieval|MoCHA]] 证明即使在全局对齐框架下，标注噪声（同一动作不同标注者的描述差异）就足以让正样本嵌入方差膨胀 11-19%，限制检索精度
   - [[2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval|PST]] 直接命名为"Beyond Global Alignment"，实验证明关节级→片段级→整体级的金字塔对齐在所有粒度上都优于纯全局对齐

2. **粒度不匹配导致的具体失败模式**：
   - 复合指令遗漏：全局 CLIP/T5 编码把"先走再跳再挥手"压成一个向量，生成器丢失事件顺序 → [[2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]] 的动机
   - 局部控制失效：全局文本无法指定"右手在 0.5-1.0s 做某动作" → [[2026_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text|FineXtrol]] 的动机
   - 语义漂移：长序列中全局条件信号衰减 → [[2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 和 [[2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]] 都需要额外机制（Self-Forcing / Action Plan）来补偿

3. **但粒度对齐本身不够**：
   - 还需要**语义规范化**（MoCHA 的文本去噪）
   - 还需要**时序对齐**（Event-T2M 的事件分解）
   - 还需要**物理一致性**（FK 监督、运动学约束）

结论：粒度对齐是 M-T alignment 的**结构性前提**——没有它，后续的语义对齐、时序对齐都缺乏锚点。

---
## Q3：25/26 年 M-T 对齐工作全景

### 对齐层级分类

| 层级             | 对齐粒度                              | 代表工作                                                                                                                                                                                       | 核心机制                           | 任务      |
| -------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------ | ------- |
| L0: 全局         | sentence ↔ sequence               | TMR (ECCV'24), LaMP (ICLR'25)                                                                                                                                                              | 对比学习（InfoNCE）在全局嵌入空间           | 检索/生成条件 |
| L1: 事件级        | event ↔ motion segment            | [[2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis\|Event-T2M]] (ICLR'26)                                                                                          | LLM 事件分解 + 事件级 cross-attention | 生成      |
| L2: 帧级         | frame-label ↔ frame               | [[2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation\|MoLingo]] (CVPR'26)                                                                                                | SAE 帧级文本标签对比损失                 | 生成      |
| L3: 部位级        | body-part text ↔ body-part motion | [[2026_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text\|FineXtrol]] (AAAI'26)                                                                                               | 分层对比编码器 + ControlNet 分支        | 可控生成    |
| L4: 关节-token 级 | text token ↔ joint patch          | [[2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction\|MaxSim]] (arXiv'26), [[2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval\|PST]] (arXiv'26) | MaxSim 后交互 / STI 金字塔           | 检索      |

### 25/26 年各工作详细对比

| 工作                                                                                                   | 年份       | Text 侧处理               | Motion 侧处理                      | 对齐机制                                         | 关键创新                               |
| ---------------------------------------------------------------------------------------------------- | -------- | ---------------------- | ------------------------------- | -------------------------------------------- | ---------------------------------- |
| [[2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning\|LaMP]]            | ICLR'25  | CLIP text encoder      | VQ-VAE motion tokens            | BLIP-2 四路预训练（对比/匹配/双向生成）                     | 用运动感知预训练替代 CLIP 的图像-语言空间           |
| [[2026_MoCHA_Denoising_Caption_Supervision_Motion_Text_Retrieval\|MoCHA]]                            | arXiv'26 | LLM 规范化 C(t) → 剥离标注者噪声 | 标准运动编码器                         | Blend Training（规范化+原始双通道对比）                  | 文本去噪：正样本方差降 11-19%，跨数据集迁移 +94%     |
| [[2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval\|PST]]                     | arXiv'26 | DistilBERT 词级 token    | ViT 关节级 token                   | 金字塔 STI：关节级→片段级→整体级渐进对齐                      | Shapley-Taylor 交互量化跨模态 token 对关联强度 |
| [[2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction\|MaxSim]]                   | arXiv'26 | DistilBERT token 级     | 关节角度 Motion Image → ViT patch 级 | MaxSim 后交互（每个 text token 找最大匹配 motion patch） | 关节角度→伪图像，关节-patch 一一对应             |
| [[2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation\|MoLingo]]                    | CVPR'26  | T5 + 文本适配器 → 多 token   | SAE 帧级语义对齐潜码                    | 帧级文本标签对比损失 + 多 token cross-attention         | 潜空间本身就是语义结构化的                      |
| [[2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis\|Event-T2M]]              | ICLR'26  | LLM 事件分解 + TMR 检索编码    | 标准运动表征                          | 事件级 cross-attention（Conformer）               | 定义"事件"为最小语义自包含动作单元                 |
| [[2026_FineXtrol_Controllable_Motion_Generation_via_Fine_Grained_Text\|FineXtrol]]                   | AAAI'26  | T5 分层对比编码器（句/片段/序列）    | MDM + ControlNet 分支             | 细粒度文本信号按部位+时间段注入                             | 首个以细粒度文本（非坐标）做部位级控制                |
| [[2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment\|ReAlign]] | AAAI'26  | 标准文本编码                 | 标准运动扩散                          | 推理期 reward-guided sampling（语义对齐+真实感奖励）       | 不改模型参数，即插即用                        |
| [[2026_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation\|MoRL]]             | arXiv'26 | LLM 推理链                | 运动 token                        | RL 对齐（语义相似度奖励）                               | 推理链作为中间对齐桥梁                        |

### 共性趋势

1. **从全局到局部**：25 年还以全局对比为主（LaMP），26 年几乎所有新工作都在做某种形式的细粒度对齐
2. **文本侧分解成为标配**：Event-T2M 用 LLM 做事件分解，FineXtrol 用结构化细粒度描述，MoLingo 用帧级标签——都在打破"一句话→一个向量"的瓶颈
3. **检索与生成的对齐需求分化**：检索侧（PST, MaxSim）追求 token-level 可解释对应；生成侧（MoLingo, Event-T2M）追求条件注入的粒度匹配
4. **后交互 > 早期融合**：MaxSim 和 PST 都用后交互（late interaction）替代早期全局嵌入，保留细粒度信息

### 遗留问题

1. **关节级对齐只在检索中验证，未进入生成**：PST 和 MaxSim 做到了 joint-token ↔ text-token 的细粒度对应，但这种对齐能力还没有被用作生成模型的条件注入机制
2. **PRISM 的粒度不对称未被解决**：motion 已经精细到 joint token，但 text 仍是全局注入——这是一个明确的研究空白
3. **时序对齐与空间对齐的统一**：Event-T2M 做时序（事件→片段），PST/MaxSim 做空间（关节→token），但没有工作同时做两者
4. **对齐质量的评估缺失**：现有 benchmark（HumanML3D, KIT-ML）的文本标注粒度太粗，无法评估关节级对齐质量。FineMotion 数据集是一个开始，但覆盖有限
5. **对齐与控制的断层**：FineXtrol 证明细粒度文本可以做部位级控制，但它的文本格式是人工设计的结构化信号，不是自然语言——从自然语言到结构化控制信号的自动转换仍是开放问题

---
## Q4：三篇 idea 笔记中的 M-T 粒度相关启发

### motion-multiple_level-control.md — 最直接相关

这篇笔记的核心假设就是 M-T 粒度问题：

> "全局文本语义、body-part 级结构化中间表示与 joint-level 显式控制需要通过统一的层级接口而非平铺拼接来耦合"

关键洞察：
- semantic papers 解决了"文本怎么拆"（Event-T2M, FineXtrol）
- controllable papers 解决了"约束怎么打"（Kimodo, OmniControl）
- representation papers 解决了"joint-level 怎么表示"（PRISM, MaxSim）
- **但还没有工作把三者接成同一条控制链**：`global text → body-part script → sparse joint anchors → joint-level generation → cross-level reflection`

### motion-token-swap-guidance.md — 间接相关

Token Swap Guidance 的前提是 motion token 有明确的语义结构（关节×时间）。如果 text-motion 对齐做到了 joint-token 级别，那么 swap 的"对抗性选择"可以用对齐分数来指导——交换对齐分数最低的 joint token 对，构造更有针对性的负样本。

### motion-gen-high-dim-ideas-backbone.md — 框架性相关

这篇提炼的六条高维设计哲学中，H1（表征解纠缠）和 H3（对齐训练）直接关联 M-T 粒度问题。其中"机会 4：Token Swap Guidance"明确提到 PRISM 的 23-joint token 空间可以作为 swap 的操作空间。

---
## 研究空白与可能方向

### 空白 1：Joint-Aware Text Conditioning for Generation

将检索侧的 joint-token 对齐能力（PST/MaxSim）迁移到生成侧：
- 在 PRISM 的 DiT 中，用 PST 风格的 STI 或 MaxSim 风格的后交互替代标准 cross-attention
- 每个 joint token 只关注与其语义最相关的 text token 子集
- 预期收益：减少"左右混淆"、"部位遗漏"等细粒度语义错误

### 空白 2：Unified Temporal-Spatial Alignment

同时做事件级时序对齐（Event-T2M）和关节级空间对齐（PST）：
- Text → LLM 事件分解 → 每个事件内部做关节级对齐
- 形成 3D 对齐张量：(event × joint × text-token)

### 空白 3：PRISM + Fine-Grained Text = ?

PRISM 的 joint-factorized latent space 是天然的细粒度 motion 表征，但缺少对应的细粒度 text 处理。如果将 FineXtrol 的分层文本编码器或 MoLingo 的帧级文本标签对比损失接入 PRISM 的 2D latent grid，可能实现目前最细粒度的 text-conditioned motion generation。

---
## Q5：常见是 1D / 2D 表征，那有没有值得探索的 3D 表征？能否复用 video generation 的 pipeline？

**短答：有，但它在当前 motion KB 里还不是成熟主流，更像是下一步值得做的结构升级。video generation 的 pipeline 可以复用一大半“生成器外壳”，但不能原样照搬 dense video 的表示假设。**

### 先区分三种“3D 表征”

1. **伪 3D tensor**
   - 例如把 motion 显式写成 `time × joint × channel`
   - 这其实已经比 2D 更接近 3D，只是很多方法把 `channel` 维藏进 token embedding，没有把它作为独立结构维来建模
   - [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 的 `time × joint token` 已经站在这条路的门口，但第三维仍是隐式 feature channel

2. **语义级 3D 结构**
   - 例如 `event × joint × time`
   - 这在 motion-language alignment 里尤其自然，因为事件、部位、时间本来就是三种不同轴
   - 这比单纯 `time × joint` 更适合表达“哪个事件在什么时候驱动哪个身体部位”
   - 从这个角度看，我前面写的 `Unified Temporal-Spatial Alignment` 本质上已经是在提一个 3D 对齐张量

3. **真正借用 video / 3D generation 的 latent volume / tri-plane / tri-grid**
   - 这类表示在当前 motion generation 主线里还几乎没有成熟代表作
   - 本地 KB 里更接近的旁证来自 video / 3D generation：例如 [[paperAnalysis/Motion_Editing/SIGGRAPH_2024/2024_Portrait3D_Text_Guided_High_Quality_3D_Portrait_Generation_Using_Pyramid_Representation_and_GANs_Prior|Portrait3D]] 用 tri-grid 做 3D 表示；[[paperAnalysis/Image_Video_Generation/arXiv_2024/2024_HunyuanVideo_A_Systematic_Framework_For_Large_Video_Generative_Models|HunyuanVideo]] 则代表了 `causal 3D VAE + DiT` 的成熟视频路线

### 为什么 motion 里还没有“标准 3D 表征”？

因为 motion 不是 dense video。video 的 3D latent volume 通常建模的是 `time × height × width` 的局部连续纹理；而 human motion 更像**稀疏、受运动学树约束的 articulated manifold**。如果直接把 skeleton 当成 voxel 或 dense cube 来建模，会遇到三个问题：

- **结构浪费**：人体只有几十个关节，远比图像像素稀疏，直接上体素/volume 很容易把大量容量浪费在空白区域
- **拓扑不对齐**：video 的空间邻近是欧式邻近，motion 的空间邻近更接近运动学树邻近；左手和右手在欧式坐标上可能接近，但在骨架拓扑上并不相邻
- **物理异质性**：position、rotation、contact、velocity 的物理单位不同，不像 RGB 视频那样天然处在同一像素网格里

所以对 motion 来说，更合理的 3D 路线很可能不是“直接照搬 video latent volume”，而是做一种 **skeleton-aware pseudo-3D representation**：例如 `time × joint × channel`、`event × joint × time`，或者 `time × part × feature-plane` 这类带强先验的结构。

### 那 video generation 的 pipeline 到底能借什么？

**能借，而且已经部分借到了。**

1. **能直接借 backbone 范式**
   - `DiT + Flow Matching` 已经在 [[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion|HY-Motion]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 这类工作中成立
   - `dual-stream → single-stream`、RoPE、窄带时间注意力等，本质上也都是从 image/video foundation model 演化过来的

2. **能借 latent pipeline 思想**
   - 我本地的 cross-domain 笔记已经总结过：video 的 `causal 3D VAE` 在 motion 里对应的是 `causal temporal motion VAE`
   - [[paperAnalysis/Motion_Generation/ICCV_2025/2025_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space|MotionStreamer]]、[[paperAnalysis/Motion_Generation/ICLR_2026/2026_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation|COME]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 都可以看作这条路在 motion 里的不同落点

3. **能借 patch / token 化策略**
   - [[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches|MotionPatches]] 证明了把 motion 变成“伪图像 patch”以后，确实能直接复用 ImageNet ViT
   - [[paperAnalysis/Motion_Generation/arXiv_2026/2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction|MaxSim]] 进一步说明，如果你把关节角度排成 motion image，还可以继续借 ViT patch pipeline 做 token-level matching
   - [[paperAnalysis/Motion_Generation/CVPR_2025/2025_Move_in_2D_2D_Conditioned_Human_Motion_Generation|Move-in-2D]] 则显示：对场景条件，保留 patch token 的局部结构比压成一个全局 token 更有效

### 但不能直接照搬什么？

- **不能直接把 motion 当作低分辨率 video 来做**：motion token 有明确的身体语义，video patch token 则更多是局部纹理，两者的 inductive bias 不同
- **不能直接用视觉空间邻域替代运动学邻域**：motion 的“相邻”应优先由骨架树和功能耦合决定
- **不能假设 3D latent 自己会学会物理一致性**：motion 比 video 更需要 FK、速度、足接触、trajectory 等显式几何约束

### 当前更稳妥的判断

我会把这个问题总结成一句话：

> **3D motion representation 值得做，但更可能成功的路线不是“video volume 直接平移”，而是“在 skeleton-aware 先验下，把 2D 的 `time × joint` 继续升维成 pseudo-3D 的 `time × joint × channel / event` 结构，并复用 video generation 的 latent-DiT pipeline”。**

也就是说，**可复用的是 pipeline，不是表示假设本身**。

---
## Q6：同时保留 position 和 rotation 会不会引入分布不匹配与训练目标分歧？现有方法怎么处理？

**短答：会有这个风险，而且在细粒度建模里是一个真实问题；但目前主流不是把二者完全分开，而是通过“共享几何目标”把它们重新对齐。**

### 为什么 position 和 rotation 可能“打架”？

1. **物理单位不同**
   - position 是米/毫米尺度，rotation 是角度或 6D 连续表示
   - 如果直接拼接后等权优化，loss 的数值尺度很容易失衡

2. **语义层级不同**
   - rotation 更接近局部关节姿态
   - position 更接近全局几何结果，尤其对 root trajectory、end-effector、场景落点更重要

3. **它们既冗余又不完全等价**
   - 在固定骨长的骨架上，rotation 经 FK 可以导出大量 position 信息
   - 但 global root position、接触、路径、场景落点又不是仅靠局部 rotation 就能稳定表达的

4. **同样大小的 rotation 误差，其 position 后果并不均匀**
   - 肩膀 1° 误差和手腕 1° 误差在 rotation loss 里看起来一样
   - 但经 FK 后，肩膀误差会在末端手部放大得多
   - 这正是 [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 强调 FK supervision 的原因

所以问题并不是“position 和 rotation 不能共存”，而是**如果它们共存，优化目标必须有共同的几何裁判**。

### 本地 KB 里已有的几种解决方式

#### 1. 用 FK / global-space loss 把 rotation 和 position 拉回同一个评价空间

这是最主流、也最关键的答案。

- [[paperAnalysis/Motion_Generation/ICLR_2023/2023_MDM_Human_Motion_Diffusion_Model|MDM]] 在预测 `x0` 后直接加 `Lpos / Lvel / Lfoot`
  - `Lpos` 本质上就是 `FK(x̂) ≈ FK(x)`，让 rotation-domain 的预测对 global joint position 负责
- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 的 `L_joints` 更明确：在 rotation space 操作，但通过 FK 映射到 3D joint position 再监督
- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 的 FK consistency 同样是用共享几何空间来避免各分量各自为政

这类方法的共同点是：**不是分别给 position 和 rotation 各自找一个“正确答案”，而是让二者都对最终的 global geometry 负责。**

#### 2. 用 staged / hybrid training，避免 position 和 rotation 一开始就在同一阶段硬碰硬

[[paperAnalysis/Motion_Generation/TPAMI_2023/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory|Bailando]] 很有代表性。它不是一上来就要求同一个 tokenizer 同时把 position 和 rotation 都学好，而是：

1. 先用 3D positions 学到“空间可分辨”的码本
2. 冻结编码器/码本
3. 再训练 rotation decoder 输出 SMPL rotations

这相当于承认：**position 更适合学空间结构先验，rotation 更适合做最终可驱动输出**。两者不是在同一步强行对齐，而是分阶段协作。

#### 3. 用结构分解减少内部冲突，而不是把所有量硬拼成一个平面向量

- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 把 root position、global orientation、joint rotations 拆成不同 token
- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 把 `root / joint pos / joint vel / joint angle / foot contact` 组织成显式多通道 raw motion space
- [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]] 的 `HuMo263` 也是把 rotations、root、冗余 positions、foot contact 一起保留，但并没有把它们视为同质特征

它们的共同思想是：**position 和 rotation 可以共存，但最好“分工明确、接口明确”，不要让一个单体 token 被迫同时隐式承载所有物理量。**

#### 4. 如果任务是细粒度 matching / retrieval，可能需要主动放弃 position，改用角度表征

这不是因为 position 没用，而是因为它在某些任务里更容易引入虚假的空间相关性。[[paperAnalysis/Motion_Generation/arXiv_2026/2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction|MaxSim]] 的实验很说明问题：

- 在 token-patch 级细粒度匹配里，**关节角度 + MaxSim** 明显优于 **位置表示 + MaxSim**
- 作者解释是：位置特征更纠缠，细粒度匹配时容易把全局平移或局部偶然接近误当成语义对应

这说明“position + rotation 一起用”并不是所有任务的最优选择。**如果目标是 fine-grained semantic matching，rotation / angle 往往是更干净的原子语义；如果目标是 control、trajectory 或 scene grounding，position 又不可或缺。**

### 所以，是否真的存在“优化目标分歧”？

**存在，但不是致命矛盾，更像一个需要显式桥接的结构问题。**

目前 KB 里的证据更支持下面这个判断：

- 如果只是把 position 和 rotation 粗暴拼接，再做统一回归，确实容易出现目标不一致和尺度失衡
- 但如果你：
  - 先做结构分解，
  - 再用 FK / global-space loss 做共享监督，
  - 必要时用 staged training，
  
  那么它们更像是**互补视角**，不是互斥目标

### 目前最稳妥的结论

> **同时保留 position 和 rotation 通常是有益的，但前提是不要把它们当成“同质特征”直接混训；更好的做法是先在表征层分解，再在优化层用 FK / global geometry 重新对齐。**

如果后面真要往这个方向做新方法，我觉得一个很自然的升级版问题就是：

> 能不能设计一个 `time × joint × channel-group` 的 pseudo-3D latent，把 `position / rotation / velocity / contact` 分到不同 channel group，再通过 group-aware attention + FK-consistent loss 统一训练？

这比简单问“要不要都保留”更接近真正的方法问题。
