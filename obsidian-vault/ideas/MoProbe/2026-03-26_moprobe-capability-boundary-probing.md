---
created: 2026-03-26
updated: 2026-04-08T13:29
tags:
  - research-idea
  - Motion_Generation
  - capability-boundary
  - failure-analysis
  - probing
  - evaluation
status: draft
related:
  - "[[MoDebug]]"
  - "[[paperCollection/by_technique/LLM_Motion]]"
  - "[[paperCollection/by_technique/Fine_Grained_Control]]"
title: "MoProbe: Probing Semantic Capability Boundaries in Text-to-Motion Models"
model_name: MoProbe
---
# MoProbe: Probing Semantic Capability Boundaries in Text-to-Motion Models

> **Model**: MoProbe (Motion Probing)

## 1. 核心问题 (Core Problem)

预训练 text-to-motion 生成器（MDM、MoMask、MotionDiffuse、T2M-GPT 等）的评估依赖聚合指标（FID、R-Precision），这些指标**掩盖了模型在哪里失败、为什么失败**。目前我们无法回答以下问题：

- 哪些语义概念在模型的能力范围之内（能正确生成）？
- 哪些概念超出能力边界（始终失败）？
- 失败的根本原因是什么？
  - **(a) 能力缺失 (Capability Absence)** — 模型从未学过该概念（训练数据稀疏）
  - **(b) 调用失败 (Invocation Failure)** — 模型知道该概念，但 prompt 无法激活它（语言接口缺陷）
  - **(c) 文本歧义 (Text Ambiguity)** — prompt 本身描述不足，概念本就无法单义映射到动作

**研究动机**: 当前评估范式像是用平均分评价学生，无法诊断具体知识漏洞。MoProbe 的目标是建立一套「能力 CT 扫描」工具，精确定位每个生成器的语义盲区。

> 类比：NLP 领域的 BERTology 通过 probing classifiers 揭示了 BERT 内部的语言学知识分布；MoProbe 将类似方法迁移到动作生成领域。

---
## 2. 研究路线

> ⚠️ **定位更新（2026-04-03）**：MoProbe 已从 MoDebug 的 Route B 独立为独立研究线。三线关系为：TAMR（方法层）→ MoProbe（诊断层）→ MoDebug（干预层）。详见 `paperIDEAs/2026-04-04_tamr-moprobe-MoDebug-roadmap.md`。

本工作是独立的 **系统性能力边界探测** 研究，不涉及模型修复。

```
三线研究结构
├── TAMR:       时序感知 retrieval + localization 方法工作
├── MoProbe:    ← 本文（系统性语义能力边界探测，诊断性分析 + benchmark）
└── MoDebug:    local semantic critique + selective local repair
```

### 与 TAMR 的关系及独立性

TAMR 可为 MoProbe 提供更可靠的 temporal judge / localization support，但 MoProbe 的核心流程（黑盒 minimal-pair probing → MLLM judge → failure taxonomy → CapabilityMap）不依赖 TAMR。

| 探测维度 | 是否依赖 TAMR | 替代方案 |
|----------|--------------|----------|
| 身体部位 / 动作原语 / 空间关系 / 修饰语 / 否定 / 量词 / 组合动作 | 否 | MLLM judge 即可 |
| 时序模式（A5）/ 顺序效应（B2） | 弱依赖 | MLLM 视频 judge + ChroAccRet CAR 兜底，精度低于 TAMR 但 pilot 阶段可接受 |

结论：MoProbe Phase A（MoMask pilot 50-100 条）可立即独立启动；时序维度待 TAMR R1 grounding 可用后深化。

### 与 MoDebug 的关系

- MoProbe 的 Failure Taxonomy 为 MoDebug 提供失败类型先验
- MoProbe 的 CapabilityMap 指导 MoDebug 选择哪些失败值得修复
- 两者可独立发表，形成互补研究叙事
- MoProbe 向下游输出 failure taxonomy + capability map + repairability prior；不消费 MoDebug 的任何产出

**独立性**: MoProbe 不依赖任何特定生成器的内部结构，是纯黑盒 (black-box) 探测，适用于所有 text-to-motion 模型。这使本文具有广泛的通用性和社区价值。

---
## 3. 方法设计 (Method Design)

### 3.1 总体框架：Semantic Probing Protocol

```
[Step 1] Probe Corpus 构建
         结构化原子语义单元 x 维度矩阵
             ↓
[Step 2] Probing Strategy
         控制变量最小对 (minimal-pair) prompts
             ↓
[Step 3] 多模型生成
         MDM / MoMask / T2M-GPT / MotionDiffuse / LMM / AvatarGPT
             ↓
[Step 4] MLLM 自动裁评 + 人工校验
         GPT-4V / MG-MotionLLM 作为 judge
             ↓
[Step 5] Failure Diagnosis Taxonomy 分类
         3 类 13 子类
             ↓
[Step 6] CapabilityMap 可视化
         语义概念空间 → 成功率热力图
             ↓
[Step 7] Cross-Model Comparison
         比较能力图谱 + 架构/数据原因分析
```

### 3.2 Probe Corpus（探测语料库）

设计一个**结构化原子语义单元集合**，覆盖以下维度：


| 维度                       | 覆盖内容      | 示例              |
| ------------------------ | --------- | --------------- |
| 身体部位 (Body Parts)        | 粗粒度 + 细粒度 | 手指、手腕、肩膀、膝盖、踝关节 |
| 动作原语 (Action Primitives) | 基础运动单元    | 抬举、弯曲、旋转、踢、挥手   |
| 空间关系 (Spatial Relations) | 方向 + 相对位置 | 向左、向前、绕圆圈       |
| 时序模式 (Temporal Patterns) | 动态变化规律    | 加速、减速、交替、同步     |
| 修饰语 (Modifiers)          | 风格/方式限定   | 缓慢地、优雅地、用力地     |
| 否定约束 (Negation)          | 负向约束      | 不弯膝盖、不摆动手臂      |
| 量词/数量 (Quantifiers)      | 精确数量      | 三步、两次           |
| 组合动作 (Compositions)      | 跨体部/跨时间   | 跳跃同时挥左手、边走边转头   |


**Probe Corpus 规模目标**: ~1,000 个探测 prompt，覆盖 50+ 语义维度，每维度 15-20 个变体（minimal pairs）。

**词汇来源**: 参考 [[FineMotion (ICCV 2025)]] 的 body-part-level 细粒度描述体系，同时参考 HumanML3D 和 KIT-ML 的自然语言标注风格。

### 3.3 Probing Strategy（探测策略）

借鉴 NLP probing（BERTology 风格），使用**控制变量的最小对 (minimal-pair) prompts** 来隔离每个语义维度：

**示例 1: 测试否定理解 (Negation Blindness)**

- Prompt A: walk forward with arms swinging
- Prompt B: walk forward WITHOUT arms swinging
- 若两者输出相同 → 判定 B3: 否定盲区

**示例 2: 测试量词敏感度 (Quantifier Insensitivity)**

- Prompt A: take three steps to the right
- Prompt B: take many steps to the right
- 若输出步数无显著差异 → 判定 B4: 量词不敏感

**示例 3: 测试修饰语效果 (Modifier Collapse)**

- Prompt A: walk forward
- Prompt B: walk forward slowly and gracefully
- 若生成速度/风格变化不显著 → 判定 B5: 修饰语崩塌

**示例 4: 测试同义词鲁棒性 (Synonym Sensitivity)**

- Prompt A: jog in a circle
- Prompt B: run in a circle
- Prompt C: trot in a circle
- 若三者输出差异过大 → 判定 B1: 同义词敏感

**示例 5: 测试组合动作 (Composition)**

- Prompt A: jump
- Prompt B: wave left hand
- Prompt C: jump while waving left hand
- 若 C 与 A+B 语义叠加偏差大 → 判定 A2: 组合动作能力缺失

### 3.4 MLLM 自动裁评（Judge Model）

将生成的骨骼动画渲染为视频后送入 MLLM judge：

- **GPT-4V**: 语义对齐评估（参考 [[FreeMotion (ECCV 2024)]] 的评估范式）
- **[[MG-MotionLLM (CVPR 2025)]]**: 细粒度动作理解，作为主要 judge 骨干
- **人工校验**: 10% 抽样，计算 Cohen kappa 一致性

针对每个 probe prompt 设计**二元判断问题** (yes/no)：

- Does the generated motion correctly avoid bending the knees?
- Does the character take exactly three steps?
- Is the left hand waving while the character jumps?

### 3.5 Capability Boundary Map（能力边界图）

- **X 轴**: 语义概念空间（body-part x action-type 二维展开）
- **Y 轴**: 成功率（0-100%，基于 MLLM 判评）
- **可视化形式**: 热力图 (heatmap)、雷达图 (radar chart)、能力前沿曲线
- **目标**: 直观展示「模型能做什么、不能做什么」的精确边界

### 3.6 Cross-Model Comparison（跨模型比较）

探测目标模型（5+ 个 SOTA 生成器）：

- **MDM** (Motion Diffusion Model)
- **MoMask** (Masked Autoregressive)
- **T2M-GPT** (VQ-VAE + GPT)
- **MotionDiffuse** (diffusion-based)
- **[[LMM (ECCV 2024)]]** (unified multi-modal motion model)
- **[[AvatarGPT (CVPR 2024)]]** (unified motion LLM)

产出**比较能力图谱**，揭示不同架构/训练策略的能力差异规律，并分析原因（数据分布、文本编码器选择、架构归纳偏置等）。

---
## 4. 与 Image/Video/MLLM 领域新进展的联系

### 4.1 Probing in NLP / VLM

- **BERTology** (Tenney et al. 2019; Rogers et al. 2020): 用 probing classifiers 揭示 BERT 各层编码的语言学特征。MoProbe 将这一范式迁移到动作语义空间。
- **迁移关键**: 将「分类任务上的探测」替换为「生成任务上的行为对比」，形成适合生成模型的新 probing 范式。

### 4.2 T2I Failure Analysis（文生图失败分析）

- **T2I-CompBench** (Huang et al. 2023): 系统评估文生图模型在属性绑定、空间关系上的能力。MoProbe 是其在动作生成领域的对应工作。
- **Winoground** (Thrush et al. 2022): 用最小对图文对测试 VLM 的组合理解能力。MoProbe 的 minimal-pair 策略直接受其启发。

### 4.3 MLLM as Evaluator

- **[[FreeMotion (ECCV 2024)]]**: 使用 GPT-4V 作为运动生成的自动评估器，验证了 MLLM 判评动作语义的可行性。MoProbe 将此范式系统化。
- **EvalCrafter** (Liu et al. 2024): 多维度视频生成评估，包含动作质量子维度。MoProbe 可视为其动作子维度的深度扩展。

### 4.4 Video Generation Diagnostic

- **T2V-CompBench**: 将视频生成质量分解为语义维度进行评估；MoProbe 对动作生成做类似的维度分解。

### 4.5 LLM-Based Motion Understanding

- **[[MG-MotionLLM (CVPR 2025)]]**: 证明 MLLM 可以在细粒度层面理解运动（body part level）；MoProbe 将其用作 judge model 骨干。
- **[[FineMotion (ICCV 2025)]]**: body-part-level 细粒度描述，为 probe corpus 提供语义词汇表。
- **[[LLaMo (CVPR 2025)]]**: 动作指令调优，显示动作理解模型的能力上限。

---
## 5. 具体失败原因分类 (Concrete Failure Taxonomy)

### Type A: 能力缺失 (Capability Absence)

- **A1: 稀有动作** — 训练数据中该动作出现频率极低 (data sparsity)
- **A2: 复杂组合动作** — 如「跳跃的同时挥动左手」，跨体部同步控制失败
- **A3: 体部隔离失败** — 无法控制单根手指/手腕等细粒度部位
- **A4: 空间关系失败** — 「在桌子左侧移动」等需要场景锚定的指令
- **A5: 时序模式失败** — 「先加速后减速」等时间动态学不到

### Type B: 调用失败 (Invocation Failure)

- **B1: 同义词敏感** — 相同概念、不同词语 → 显著不同输出
- **B2: Prompt 顺序效应** — 词序改变导致生成显著变化
- **B3: 否定盲区** — 「不弯膝盖」等否定指令被完全忽略
- **B4: 量词不敏感** — 「三步」 vs 「许多步」产生相同输出
- **B5: 修饰语崩塌** — 形容词修饰语（「缓慢地」「优雅地」）对生成无影响

### Type C: 文本歧义 (Text Ambiguity)

- **C1: 欠定义动作** — 「做运动」可映射到任意动作，失败不能归因于模型
- **C2: 文化特异性** — 手势含义因文化而异，训练集分布失衡
- **C3: 歧义体部引用** — 「把它抬起来」缺乏明确指代

> **诊断提示**: 区分 A/B/C 类的关键在于设计控制实验：若重新训练或 fine-tune 能修复则为 A；若换词后能激活则为 B；若无论如何修改 prompt 都无法定义正确答案则为 C。

---
## 6. 核心贡献 (Key Contributions)

1. 首个针对 text-to-motion 生成器的**系统性语义探测协议** (Semantic Probing Protocol)
2. 结构化**失败分类法** (3 类 13 子类) 及配套诊断标准
3. **CapabilityMap**: 5+ 个 SOTA 生成器的跨模型能力边界可视化
4. 揭示各失败类型背后的架构/数据局限性分析
5. **MoProbe-Bench**: 开放式探测基准测试集，作为社区资源公开

---
## 7. 相关论文 (Related Works from Knowledge Base)


| 论文                           | 与 MoProbe 的关系             |
| ---------------------------- | ------------------------- |
| [[MG-MotionLLM (CVPR 2025)]] | 细粒度动作理解，用作 judge model 骨干 |
| [[LMM (ECCV 2024)]]          | 统一多模态动作模型，探测目标            |
| [[FineMotion (ICCV 2025)]]   | 细粒度体部描述，词汇表来源             |
| [[FreeMotion (ECCV 2024)]]   | GPT-4V 评估范式，判评管线参考        |
| [[AvatarGPT (CVPR 2024)]]    | 统一动作 LLM，探测目标             |
| [[ReMoGPT (AAAI 2025)]]      | 部位级检索，细粒度理解参考             |
| [[FineXtrol (AAAI 2026)]]    | 细粒度控制，揭示可控制性局限            |
| [[LLaMo (CVPR 2025)]]        | 动作指令调优，动作理解模型             |


---
## 8. CCF-A 投稿定位

- **首选**: NeurIPS 2026 / ICLR 2027（分析 + benchmark 论文）
- **备选**: CVPR 2027
- **论文类型**: Diagnostic/Analysis paper with benchmark contribution

**选款理由**: NeurIPS/ICLR 对分析性、诊断性工作有天然亲和力（参考 BERTology 在 ACL 发表，T2I-CompBench 在 NeurIPS 发表）。CVPR 作为备选是因为它对视觉内容理解和评估的工作持开放态度。

---
## 9. 开放问题 (Open Questions)

- **GT 定义**: 如何定义「正确」的动作生成？同一 prompt 可能有多种合理输出。
- **标注一致性**: 如何处理失败语义标注中的标注者间不一致？
- **表示泛化性**: probe corpus 能否跨不同动作表示（SMPL vs joint angles）泛化？
- **模型规模效应**: 能力边界是否随模型规模扩大而改变？
- **跨数据集泛化**: 在 HumanML3D 训练的模型能力边界是否与 KIT-ML 训练的不同？
- **动态探测**: 能力边界是否可以通过 fine-tuning 拓展？如何设计动态探测实验？

---
## 10. 下一步行动 (Next Steps)

- 设计 probe corpus 初始版本（100 prompts 覆盖 10 个关键维度）
- 在 T2M-GPT 上运行初始探测实验，验证 pipeline 可行性
- 调研 MG-MotionLLM 作为 judge 的评估一致性
- 确定跨模型比较的评估指标体系
- 阶段性迭代扩展到 1,000 prompts


---
## 11. 方向聚焦分析：Benchmark vs. 方法论 (Direction Analysis)

### 11.1 两个方向的内在关系

MoProbe 表面上存在两个潜在侧重方向：

- **方向 A（Benchmark 主导）**: 将 MoProbe-Bench 作为核心贡献，强调探测语料库的规模、覆盖度和社区复用价值，论文定位为基准测试资源论文。
- **方向 B（方法论主导）**: 将 Semantic Probing Protocol 和 Failure Taxonomy 作为核心贡献，强调诊断框架的通用性和分析深度，论文定位为分析性方法论论文。

**结论：两个方向应合并，不宜拆分。**

原因如下：

1. **方法论与 Benchmark 天然耦合**: Semantic Probing Protocol 产生了 MoProbe-Bench，而 Benchmark 反过来验证了方法论的有效性。拆分后两篇论文都会显得「贡献不完整」——纯方法论论文缺乏可复现的资源，纯 Benchmark 论文缺乏理论框架支撑。
2. **标杆先例支持合并**: T2I-CompBench（NeurIPS 2023）、Winoground（ECCV 2022）均以「方法论 + Benchmark」组合形式发表，且获得顶会接收。MoProbe 遵循同样的模式更稳妥。
3. **合并后叙事更强**: 「我们设计了探测协议（方法）→ 构建了探测语料库（工具）→ 发现了系统性失败规律（发现）→ 开放基准供社区复用（贡献）」形成完整闭环，比任一单独方向都更具说服力。

### 11.2 对 CCF-A 论文接收的影响

**合并方向（推荐）对 CCF-A 接收的影响分析**:

| 维度 | 合并方向 | 拆分-仅方法论 | 拆分-仅 Benchmark |
|---|---|---|---|
| NeurIPS/ICLR 接收倾向 | 高（分析+资源双贡献） | 中（需强理论创新） | 中低（资源论文门槛高） |
| CVPR 接收倾向 | 高（视觉内容评估） | 中 | 中 |
| 贡献完整性 | 完整 | 偏弱 | 偏弱 |
| 审稿人质疑风险 | 低 | 高（「为何不发布 Bench?」） | 高（「方法论创新在哪?」） |

**NeurIPS/ICLR 特别说明**: 这两个顶会对「分析性论文 + 开放资源」组合有天然亲和力。Datasets & Benchmarks track（NeurIPS）明确欢迎此类工作，Main track 同样接收有充分实验验证的诊断分析论文。

**CVPR 特别说明**: CVPR 更偏向有明确视觉任务性能提升的论文，但对评估方法论和 benchmark 建设的工作持开放态度（参考 EvalCrafter、T2V-CompBench 等工作的发表情况）。

### 11.3 对后续研究开展的影响

**合并方向对后续研究的优势**:

1. **为 MoDebug Route A 提供完整先验**: 合并版 MoProbe 同时提供 Failure Taxonomy（方法论）和 MoProbe-Bench（测试集），使 Route A 的修复系统有完整的诊断依据和评估基准。
2. **社区影响力最大化**: 开放的 MoProbe-Bench 可被其他研究者用于评估新模型，形成引用飞轮效应，提升后续工作的影响力。
3. **可扩展性**: 合并论文发表后，可以自然延伸出「MoProbe v2」（扩展到更多模型/更细粒度维度）或「MoProbe-Fix」（结合修复方法），形成研究线。

**拆分方向的潜在问题**:

- 方法论论文单独发表后，若无配套 Benchmark，社区难以复现和对比，降低实际影响力。
- Benchmark 论文单独发表，若缺乏深度分析，可能被认为贡献偏工程、缺乏洞察，接收难度上升。

### 11.4 推荐执行策略

**主线**: 合并为单篇完整论文，投 NeurIPS 2026（Datasets & Benchmarks track 或 Main track）。

**备选**: 若论文篇幅过长（内容超出单篇承载），可考虑：
- 主论文聚焦 Protocol + Taxonomy + 核心发现（方法论为主）
- 将完整 Benchmark 作为附录 + 开放数据集，不单独发表
- 避免「一拆为二」降低每篇的贡献密度

---
## 12. 生成模型选择计划

> 来源：[[2026-03-27_moprobe-vs-motioncritique-competition-analysis|0327 竞争分析与模型选择]]

### 12.1 选型标准（四维筛选）

1. **可运行性**：有公开 checkpoint，输出 HumanML3D 263 维格式
2. **架构多样性**：覆盖离散掩码 AR / 双向 AR / 连续扩散 / SSM 扩散
3. **性能梯度**：强（FID<0.1）、中（0.1~0.3）、弱（>0.3）三档
4. **时效性**：仅用 2024+ 中稿顶会

### 12.2 推荐选型

| 优先级 | 模型 | Venue | FID↓ | 架构 |
|--------|------|-------|------|------|
| P1 必选 | MoMask | CVPR 2024 | 0.045 | RVQ-VAE + 双路掩码 Transformer |
| P2 推荐 | BAMM | ECCV 2024 | 0.055 | 双向 AR |
| P2 推荐 | Motion Mamba | ECCV 2024 | 0.281 | Mamba SSM 扩散 |
| P2 推荐 | MARDM | CVPR 2025 | 0.045 | 连续掩码自回归扩散 |
| P3 补充 | MotionLCM / EnergyMoGen / ScaMo | 2024-2025 | 0.188-0.467 | 各异 |
| 暂缓 | TriC-Motion / COME | ICLR 2026 | 0.033-0.041 | 待开源 |

### 12.3 分批执行

```
Phase A（立即）：MoMask → pilot 50-100 条 minimal-pair probe
Phase B（核查后）：+BAMM +Motion Mamba +MARDM → 全量 500-1000 条
Phase C（条件允许）：+MotionLCM +EnergyMoGen +ScaMo +ICLR 2026 SOTA
```

### 12.4 关键执行注意点

- text 集构造先于生成，避免修改导致重复生成
- 输出统一转换为 HumanML3D 263 维格式
- 每条 text 生成 k=5~10 条动作（参照 T2I-CompBench k=10）
- MoMask 生成复用 `shared/script_momask/phase1_generate_momask.py`

---
## 13. Text 集构造方法论参考

> 来源：[[2026-03-28_benchmark-trio-failure-analysis-gap-and-guidance|Benchmark 三部曲方法论参考]]、[[2026-03-28_motion-generation-benchmark-survey|Motion Generation Benchmark 综合调研]]

### 13.1 跨域 Benchmark 数据构造五原则

1. **按能力维度分类，而非随机采样**：MoProbe 的 minimal-pair text 集应按「归因类别 × 语义维度」设计
2. **规模不必大，可验证性优先**：T2I-CompBench 每子类 1000 条、T2V-CompBench 每类 200 条、EvalCrafter 总计 700 条——pilot 50-100 条已足够验证归因三分法
3. **每条 probe 的正确答案必须可被客观验证**：设计为可判定属性（「是否弯曲膝盖」），而非主观感知质量
4. **评估工具可用性约束 prompt 类别划分**：归因类别的划分需匹配现有运动检测工具的能力边界
5. **每条 prompt 生成多个样本**：k=5~10 条动作/text

### 13.2 现有 Benchmark 空缺与 MoProbe 定位

| 维度 | 已有覆盖 | 空缺（MoProbe 填补） |
|------|----------|----------------------|
| 感知质量 | MotionCritic (ICLR 2025) | 无 span 定位、无失败归因 |
| OOD 泛化 | ViMoGen-MBench (ICLR 2026) | 无失败根因区分 |
| 时序顺序 | ChroAccRet-CAR (ECCV 2024) | 仅覆盖 ordering error |
| 细粒度时空 | FineMotion (ICCV 2025) | 标注失败 span，非评测失败 |
| **失败根因分类** | **无** | **能力缺失 vs 调用失败 vs 文本歧义** |
| **Minimal-pair probing** | **无** | **控制变量隔离单一语义维度** |
| **能力边界地图** | **无** | **按语义类型标注可修性** |

### 13.3 个人方法论笔记

**Benchmark 对 follow 工作提供什么**：
1. metrics，引领更合理的 evaluation。例如 [[2024_EvalCrafter_Benchmarking_and_Evaluating_Large_Video_Generation_Models|EvalCrafter]] 指出 FVD 只关注分布匹配而非 text-video 配对质量，因此提出新指标。

**数据构造流程**：
1. 分析主流指标不足 → 主流 dataset 不足 → 得出 problem formulation
2. 现有 dataset metaword 分析，提取 object、verb、relation 等
3. 基于 metaword 和 formulation 构造 benchmark prompts

**MLLM Evaluation**：
- 为防止幻觉，使用链式提问，先让 MLLM 描述画面再提问
