---
created: 2026-03-13T00:00
updated: 2026-04-08T13:29
title: 从五个层次分析动作生成落地距离，结合已有积累与 prompt/agent 技能，给出每层兼顾价值前景与可行性的研究问题。
---
# 2026-03-13 动作生成落地距离：五层分析与研究问题提炼

> 基于 ResearchWY paperCollection + paperAnalysis 的系统检索；聚焦「研究 demo → 可部署产品」的真实距离，结合已有积累（diffusion/tokenization/kinematic loss/motion quality metrics + prompt/agent 使用经验），在数据、质量、控制、系统、对齐五个层次各提炼一个兼顾价值与可行性的研究问题。
>
> 共享母题：与 Agent 化接口、工业场景与 product-ready 讨论重合的背景已抽到 [[2026-04-16_motion-productization-shared-frame|2026-04-16 动作生成落地化共享框架]]。本文保留“五层问题 → 五个可投稿研究题”的独立角度。

---
## 一、想法拆解与联想

### 问题重述

动作生成研究在顶会上每年产出数十篇 SOTA，却鲜有系统在真实业务中稳定运行。差距不在某一单点上，而是**在数据→质量→控制→系统→对齐五个层次叠加的结构性问题**。本文从这五个层次逐一定位：

1. **在哪个层次上，学术进展与工业需求的距离最大？**
2. **在这个距离中，哪些子问题与已有积累对齐，且不需要 RL / LLM 训练即可推进？**
3. **每层是否存在一个「窄而深」的研究问题，可以独立投稿 CCF-A / 顶会？**

### 分层框架（从底层基础到面向用户）

```
Layer 0: 数据与评估层        ← 数据哪里来？评估是否有意义？
Layer 1: 生成质量与物理层    ← 生成的动作本身够不够好？
Layer 2: 可控性与接口层      ← 用户能不能准确表达想要什么？
Layer 3: 系统集成与工作流层  ← 生成模型如何嵌入生产流程？
Layer 4: 感知对齐与持续优化层 ← 如何在部署后与用户偏好对齐？
```

### 与已有 idea 的联动

- 本文补全了 `2025-03-08`（五维缺口 + CCF-A 交叉表）和 `2025-03-09_motion-llm-ideas`（Product-ready 挑战）的「落地视角」，是从「研究问题」到「产品问题」的系统对应。
- 每层的研究问题被设计为与 diffusion/tokenization/kinematic loss/motion-quality-metrics 等已有技能直接衔接，同时利用 prompt/agent 使用经验作为差异化优势。

---
## 二、真实场景与需求痛点

### 五层距离的产业表现

| 层次     | 学术当前状态                               | 业务真实需求                      | 核心距离             |
| ------ | ------------------------------------ | --------------------------- | ---------------- |
| 数据与评估层 | HumanML3D/KIT，简短英文描述，FID+R-precision | 多语言、多领域、真实用户 query，感知质量评估   | 指标失真、标注稀缺、OOD 失效 |
| 生成质量层  | 语义正确但脚滑/浮空/力量感弱                      | 动捕工程师可直接用、符合物理美学的输出         | 物理合理性与表现力细节      |
| 可控性层   | joint/轨迹约束接口，需专业知识                   | 导演/设计师用自然语言即可描述意图与约束        | 控制抽象层缺失          |
| 系统集成层  | 单点 demo，固定 CLI/API                   | 嵌入 Maya/Blender/游戏引擎的可迭代工作流 | 服务化、可组合、可调试      |
| 感知对齐层  | 离线 benchmark，FID 与用户偏好相关性低           | 系统随用户反馈自适应，不需重训             | 在线反馈闭环缺失         |

### 场景定位（集中在以下两类落地方向）

1. **游戏/影视内容制作管线**：动画师用文字/草图描述动作，批量生成→筛选→微调的工作流；需要稳定输出、可解释的质量评估、可编辑的接口。
2. **XR/虚拟人实时交互**：实时在线生成，对延迟、物理一致性、长期角色风格一致性要求高；需要 Agent 级的状态管理和交互接口。

---
## 三、相关工作支持与研究空间（按层次）

### Layer 0：数据与评估层

#### 3.0.1 研究空间定位

**核心问题**：FID、R-precision 是否真的衡量了我们关心的质量？

- **ChroAccRet**（ResearchWY）：提出 ChronologicalAccuracy（CAR）评估时序顺序遵从性，发现多数模型不编码事件顺序——证明 R-precision 存在「内容对但顺序错」的盲区。
- **T2MBench**（arXiv 2025）：out-of-distribution 文本输入下，所有 SOTA 模型在细粒度精度评估上显著下降；证明现有指标严重高估了模型真实泛化能力。
- **MotionCritic**（2025）：引入大规模人类感知数据集，训练一个 critic 模型做实例级感知质量评分；发现 FID 与人类感知一致性相关性很低。
- **MG-MotionLLM**（CVPR 2025）：利用 FineMotion 细粒度标注数据集，结合多粒度 motion script 实现更细致的语义对齐——说明更丰富的标注对评估和训练都有价值。

**支持点**：多项工作已证明 FID 的局限，但统一的「感知对齐评估协议」尚未建立。

**研究空间**：
- 设计一个**自动化的动作质量感知标注 pipeline**：用 VLM/LLM API 对渲染后的动作视频生成多维质量评分（流畅度、力量感、语义一致性、物理合理性），构建训练/评估数据集——完全不需要训练 LLM，只需 prompt engineering + VLM API。
- 设计**基于 VLM-as-judge 的 motion 质量基准**（MotionBench-Perceptual），覆盖：实例级感知质量、细粒度语义对齐、OOD 鲁棒性、跨领域风格一致性。

**可行性**：与 motion-quality-metrics skill 高度衔接；使用 GPT-4V/VideoLLaMA 等 API 零样本评分无需训练；构建基准是独立贡献，可投 CVPR/ECCV/AAAI。

---
#### 3.0.2 推荐研究问题 0

> **「基于 VLM 自动感知评分的动作质量基准 MotionBench-Perceptual」**
>
> 核心问题：如何用 VLM API + 人类参照数据构建一套与人类感知高度对齐的、实例级的动作质量自动评估体系，取代 FID 作为 motion 领域的标准评估协议？
>
> 优势：不需要 RL/LLM 训练；直接用 prompt/VLM-as-judge；与 kinematic-loss-library 和 motion-quality-metrics skill 衔接；基准论文独立贡献明确，适合 CVPR/NeurIPS。

---
### Layer 1：生成质量与物理层

#### 3.1.1 研究空间定位

**核心问题**：已生成的动作如何在不用 RL 的情况下提升物理合理性和表现力细节？

- **Morph**（ResearchWY）：`core_operator` = Motion-Projection RL 后处理；证明物理后处理能显著减少脚滑/穿地，但依赖 RL 与物理模拟器。
- **PhysDiff**（ResearchWY）：在扩散过程中引入物理投影；高质量但端到端 RL 复杂度高。
- **GORP/RPM**（CVPR 2025）：Rolling Prediction + PCAF 控制「平滑 vs. 响应性」折中，实时在线生成；`core_operator` = Prediction Consistency Anchor Function；对平滑性的显式建模证明 kinematic 约束可以在推理时注入而无需 RL。
- **Shape My Moves**（CVPR 2025）：体型感知 + 物理合理性损失；无 RL，用物理软约束训练，极端体型时仍弱。
- **HuTuDiffusion**（AAAI 2024）：`core_operator` = zeroth-order 优化 z* in latent prior per text；以极少人类反馈（few-shot ranking）调整 latent prior——不需要 RL，只是隐空间中的优化。

**支持点**：无 RL 的物理增强路径已有先例（Morph 的 MPR 投影、GORP 的 PCAF、differentiable sim），但这些方法各自孤立；用 Conformal prediction 做「置信区间 + 拒绝/重采样」策略尚无系统研究。

**研究空间**：
- **物理一致性后处理 + 不确定性量化**：结合 Conformal prediction，为生成动作在关节空间/物理空间建立校准置信区间；在置信度低的区域（脚接触、重心不稳）触发局部重采样或 optimization-based 修正——只需 differentiable 约束优化，不需 RL。
- **Kinematic loss 蒸馏（Consistency Distillation for Motion）**：对已训练扩散模型做一致性蒸馏，加入显式 kinematic 损失（脚接触、joint limit、jerk）在蒸馏目标中——与 kinematic-loss-library skill 直接衔接，不需 RL，只需改训练损失。

**可行性**：Conformal prediction 是统计方法，与已有扩散模型无侵入式组合；kinematic-loss-library skill 已有基础；不依赖 RL 或 LLM 训练。

---
#### 3.1.2 推荐研究问题 1

> **「无 RL 的动作物理合理性增强：Kinematic-Conformal 后处理框架」**
>
> 核心问题：如何在不引入 RL 和物理仿真器的情况下，为扩散生成的动作提供可量化的物理置信评估，并在低置信区域自动触发基于可微约束优化的局部修正？
>
> 技术路线：(1) 用 Conformal prediction 在关节速度/接触状态空间构建校准置信区间；(2) 低置信帧触发 differentiable kinematic constraint optimization（foot contact IK、joint limit projection）；(3) 全流程无物理仿真器、无 RL。
>
> 优势：与 kinematic-loss-library + diffusion-model-blocks skill 直接衔接；Conformal prediction 是已有积累中明确列出的交叉技术；可投 NeurIPS/ICLR（方法创新）或 CVPR（motion quality 系统贡献）。

---
### Layer 2：可控性与接口层

#### 3.2.1 研究空间定位

**核心问题**：如何让非专家用户用自然语言即可精确表达动作意图，而不是手工指定关节轨迹？

- **OmniControl**（ResearchWY）：支持任意关节任意时刻的空间控制，但接口要求用户手动指定关节轨迹——专业门槛高。
- **FineXtrol**（AAAI 2026）：细粒度文本控制 motion；但自然语言仍有歧义，underspecified 时无解析机制。
- **ProgMoGen**（CVPR 2024）：LLM 将复杂任务描述转换为可微约束代码（Python），驱动约束满足型扩散采样；但约束库有限，尚无覆盖「模糊需求 → 结构化约束」的完整协议。
- **IRG-MotionLLM**（arXiv 2025）：LLM 在生成、评估、修正之间迭代对话——首次系统引入「LLM 作为修正 agent 的闭环」，但仍属单模型系统，无法对接外部工具。
- **CoMA**（arXiv 2025）：多个 agent 协作做 body-part 级指令分解 + self-correction；直接用 LLM/VLM API，不训练。

**支持点**：LLM 解析自然语言 → 结构化约束的能力已被 ProgMoGen、CoMA、IRG-MotionLLM 等证明；但「歧义消解 → 约束规范 → 质量验证」的完整闭环仍缺少系统研究。

**研究空间**：
- **动作意图对话式解析协议（Motion Intent DSL + LLM parser）**：设计一套面向动作生成的 DSL（Domain-Specific Language），覆盖空间约束、时序约束、风格约束、物理约束；用 LLM（GPT-4o API）将自然语言 → DSL，再通过 function-calling 映射到生成模型的控制参数。
- **歧义主动消解（Clarification Agent）**：当 LLM 检测到用户描述歧义（空间/时序/风格 underspecified）时，主动发起追问，获取补充信息后再生成——完全 prompt/agent 实现，不训练任何模型。

**可行性**：完全基于 prompt + LLM API（GPT-4o / Claude）；与已有 ProgMoGen 的约束函数库可直接对接；不依赖 RL/LLM 训练；利用了 prompt/agent 的核心技能。

---
#### 3.2.2 推荐研究问题 2

> **「动作控制意图的对话式解析：Motion Intent DSL + Clarification Agent」**
>
> 核心问题：如何用 LLM API + prompt 工程，构建一个能将用户自然语言描述（包含模糊表达）自动解析为结构化运动控制规范、并在歧义时主动追问的控制前端，从而让 OmniControl/ProgMoGen 等控制型生成器对非专家用户开放？
>
> 技术路线：(1) 设计 Motion Control DSL（spatial/temporal/style/physical slots）；(2) LLM few-shot → DSL 生成 + slot 完整性检测；(3) 缺失 slot 触发 Clarification Agent 追问；(4) 完整 DSL → 映射到控制信号，输入 OmniControl/ProgMoGen。
>
> 优势：完全 prompt/agent 技能，零训练成本；可与 ProgMoGen/FineXtrol 的控制接口直接对接；研究问题新颖（控制接口工程化 + 可用性），适合 CVPR/AAAI 系统论文或 ACM CHI（HCI 方向）。

---
### Layer 3：系统集成与工作流层

#### 3.3.1 研究空间定位

**核心问题**：如何把现有生成模型封装为可组合的、可在生产流程中调用的工具，而不是一个黑箱 demo？

- **SOLAMI**（CVPR 2025）：把 VLA 嵌入 VR 沉浸式交互，是 end-to-end social agent；但 API 不开放，不可组合。
- **Digital Life Project**（CVPR 2024）：Agent + motion matching + social intelligence，是完整系统但不可扩展。
- **HSI-GPT**（CVPR 2025）：scene–motion–language 统一 LLM，LoRA 微调；接口设计统一，但仍是整体模型，非 skill 化。
- **Sitcom-Crafter**（ICLR 2025）：plot → stage → motion，但 stage 到 motion 的 API 还不是开放标准。
- **MCP 类比**（见 `2025-03-08` Idea 2）：将 motion 生成封装为 Agent Skill，LLM 通过 function-calling 按需调用。

**支持点**：Agent 框架（LangGraph / AutoGen / MCP）已经成熟；motion generation 模型的 REST API 也已经存在（如 MDM、MoMask 等有开源实现）；缺乏的是「标准化的 motion skill 接口设计 + 工作流编排方案」。

**研究空间**：
- **Motion Generation MCP Toolkit**：设计标准化 motion skill API（`generate`, `edit`, `extend`, `evaluate`, `retarget`），用 MCP 协议封装，接入主流 Agent 框架（Claude + MCP / LangGraph）；并在游戏内容制作场景中构建端到端 demo（脚本→分镜→动作→评估→迭代）。
- **多 Agent 动作协作生产框架**：参考 CoMA 的 multi-agent body-part 协作思路，设计「总导演 Agent + 分部位 motion specialist Agent」的分工架构，用 LLM 做高层协调，调用各专门的生成/编辑工具——完全 prompt/agent，无训练。

**可行性**：直接利用 prompt/agent 使用经验；MCP 协议已成熟（Claude MCP SDK）；可基于 MDM/MoMask 等开源模型构建原型；适合投稿 AAAI（AI 系统）或以系统论文形式投 SIGGRAPH Asia / CHI。

---
#### 3.3.2 推荐研究问题 3

> **「Motion-as-a-Skill：基于 MCP 的动作生成工具化与 Agent 驱动内容制作管线」**
>
> 核心问题：如何设计一套动作生成 skill 的标准接口规范，并通过 Agent 框架实现「剧本/描述 → 分镜规划 → 多段动作生成 → 自动评估 → 迭代修改」的完整内容制作闭环，将研究级别的 motion 模型变成一个可被 LLM Agent 可靠调用的生产工具？
>
> 技术路线：(1) 定义 Motion Skill Schema（输入/输出/约束/metadata）；(2) 封装 MDM/MoMask/SALAD 等为 MCP tool；(3) LLM 主 Agent 做 workflow 规划（ProgMoGen/Sitcom-Crafter 思路）；(4) 接 VLM-as-judge 做自动质量审查；(5) 闭环迭代直到通过审查。
>
> 优势：核心技能完全在 prompt/agent 范围内；方法论新颖（motion skill 工具化标准）；有清晰的产业需求（游戏/影视内容管线）；可作为系统论文投 AAAI/SIGGRAPH/CHI，或作为 CVPR 系统 demo track。

---
### Layer 4：感知对齐与持续优化层

#### 3.4.1 研究空间定位

**核心问题**：系统部署后，如何在不重新训练模型的情况下，根据用户/创作者的偏好持续调整生成结果？

- **HuTuDiffusion**（AAAI 2024）：`primary_logic` = few-shot ranking → zeroth-order 优化隐空间先验 z*；**少量反馈即可调整生成方向，无需 RL/微调**。这是目前最贴近「测试时偏好对齐」的方案。
- **PersonaBooth**（CVPR 2025）：用少量参考动作微调 diffusion adapter，实现个性化；需要模型微调，但 adapter 规模小。
- **RealDPO**（arXiv 2025）：DPO 式偏好优化 motion diffusion；需要偏好对数据和训练，不适合无训练场景。
- **ReAlign**（AAAI 2026）：step-aware reward guided alignment；reward model 仍需训练。
- **IRG-MotionLLM**（arXiv 2025）：生成→评估→修正迭代；LLM 充当评审给出结构化反馈，无需 reward model 训练。

**支持点**：HuTuDiffusion 证明了 zeroth-order 隐空间优化的可行性；IRG-MotionLLM 证明了 LLM-as-evaluator 的有效性；两者结合可构成「无训练的测试时偏好对齐闭环」。

**研究空间**：
- **LLM-as-judge × Latent Prior Adaptation**：将 HuTuDiffusion 的 zeroth-order prior 优化中的「human oracle ranking」替换为「VLM/LLM 自动评分」，实现全自动的测试时偏好对齐——用 VLM API 评分（不训练），用 zeroth-order 优化调整 z*（只需少量前向推理）。
- **风格个性化的 prompt adaptation**：类比图像领域 textual inversion，用「动作 prompt 向量」表示个人风格，通过少量参考动作做 prompt embedding 优化——不微调整个模型，只优化 prompt vector。

**可行性**：VLM-as-judge 只需 API 调用；zeroth-order 优化（如 CMA-ES）是标准优化工具，不涉及 RL；可基于 HuTuDiffusion 开源代码快速构建原型；与 PersonaBooth 形成鲜明对比（有训练 vs. 无训练）。

---
#### 3.4.2 推荐研究问题 4

> **「无需重训的测试时动作偏好对齐：VLM-Judge × Latent Prior Optimization」**
>
> 核心问题：能否用 VLM API 的自动评分（替代人类偏好标注）驱动对扩散模型隐空间先验的 zeroth-order 优化，使生成风格在部署阶段向特定创作者偏好/风格规范靠拢，而无需重新训练或 RL？
>
> 技术路线：(1) 渲染生成动作为视频帧；(2) 用 GPT-4V / VideoLLaMA 按「自然感/力量感/风格一致性」多维评分；(3) 以评分作为目标函数，用 CMA-ES 优化 HuTuDiffusion 式的 latent prior z*；(4) 优化后的 prior 持久化为用户 profile，后续按 text similarity 选用。
>
> 优势：完全无 RL 训练；VLM 评分 = prompt engineering；zeroth-order 优化无需梯度；与 HuTuDiffusion 形成直接对比（人工排序 → VLM 自动评分 → 全自动测试时对齐）；适合投 AAAI/ICLR/NeurIPS。

---
## 四、前沿交叉技术与验证思路

| 技术方向                               | 如何接入当前层次的 idea              | 简要说明                                 | 相关链接                                                                                                                                          |
| ---------------------------------- | --------------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| VLM-as-judge（GPT-4V / VideoLLaMA）  | Layer 0 质量评估 + Layer 4 偏好信号 | 用视频理解能力对渲染动作做多维感知评分，替代人工标注或 FID      | [MotionCritic (arXiv 2025)](https://arxiv.org/abs/2407.02272)                                                                                 |
| Conformal Prediction               | Layer 1 物理不确定性量化            | 为生成动作构建校准置信区间，在低置信处触发约束优化修正          | [Conformal Prediction Tutorial](https://people.eecs.berkeley.edu/~angelopoulos/publications/downloads/gentle_introduction_conformal_2021.pdf) |
| Zeroth-Order Optimization (CMA-ES) | Layer 4 隐空间先验优化             | 不需要梯度，直接优化隐空间向量以对齐 VLM 评分目标          | [HuTuDiffusion (AAAI 2024)](https://arxiv.org/abs/2312.15611)                                                                                 |
| Motion DSL / 程序化约束                 | Layer 2 意图解析                | 将约束结构化为可验证的 DSL，LLM 生成 + 语法检查        | [ProgMoGen (CVPR 2024)](https://arxiv.org/abs/2402.14407)                                                                                     |
| MCP / LangGraph / AutoGen          | Layer 3 系统集成                | 将 motion 模型封装为标准 tool，LLM Agent 按需调用 | [MCP Protocol](https://modelcontextprotocol.io/); [LangGraph](https://www.langchain.com/langgraph)                                            |
| Consistency Distillation           | Layer 1 生成加速 + 质量保持         | 对扩散模型做一致性蒸馏，在蒸馏目标中嵌入 kinematic 损失    | [LCM (arXiv 2023)](https://latent-consistency-models.github.io/)                                                                              |
| T2MBench OOD 评估                    | Layer 0 鲁棒性评估               | 已有 OOD benchmark 框架，可直接扩展到多域         | [T2MBench (arXiv 2025)](https://arxiv.org/html/2602.13751v1)                                                                                  |

### 验证方案

- **Layer 0**：在 HumanML3D + BABEL 上跑 VLM-as-judge pipeline，计算与人类评分的 Spearman 相关；对比 FID/R-precision 的相关性。
- **Layer 1**：对 MDM/SALAD 输出 + Kinematic-Conformal 后处理，计算脚滑率/穿地率/joint limit 违规率，与 Morph、PhysDiff 对比（无 RL baseline）。
- **Layer 2**：用户研究（n=20）：专家 vs. 非专家用文字描述动作意图，使用/不使用 Clarification Agent，评估 intent-motion 一致性与操作效率。
- **Layer 3**：在 Motion-as-a-Skill pipeline 中运行 3 个真实内容制作任务（打招呼/交接物体/群舞），评估任务完成率/修改轮次/最终质量。
- **Layer 4**：在 10 个创作者各提供 5 段参考动作的场景下，对比 VLM-judge × Latent Prior vs. HuTuDiffusion（human oracle） vs. Baseline，在 R-precision/VLM 评分/用户满意度上评估。

---
## 五、总结与下一步

### 五层研究问题总览与优先级

| 层次 | 推荐研究问题（简称） | 价值前景 | 可行性 | 技能匹配度 | 建议优先级 |
|------|------------------|--------|------|----------|----------|
| Layer 0 | MotionBench-Perceptual | ★★★★ | ★★★★★ | ★★★★★ | **第一优先** |
| Layer 1 | Kinematic-Conformal 后处理 | ★★★★ | ★★★★ | ★★★★★ | **第一优先（并行）** |
| Layer 2 | Motion Intent DSL + Clarification Agent | ★★★☆ | ★★★★★ | ★★★★★ | 第二优先 |
| Layer 3 | Motion-as-a-Skill MCP Pipeline | ★★★★ | ★★★★ | ★★★★★ | 第二优先（并行） |
| Layer 4 | VLM-Judge × Latent Prior Optimization | ★★★★ | ★★★★ | ★★★★☆ | 第三优先 |

### 为什么 Layer 0 + Layer 1 最优先

1. **正交性**：评估基准（L0）和质量增强（L1）不互相依赖，可完全并行推进。
2. **积累匹配**：L0 完全基于 prompt/VLM API + 已有 motion-quality-metrics skill；L1 完全基于 kinematic-loss-library + diffusion-model-blocks skill + Conformal prediction，无 RL/LLM 训练需求。
3. **发表策略**：L0 可作为 benchmark/dataset 论文投 CVPR/NeurIPS，L1 作为方法论文投 ICLR/CVPR，两篇结构不重叠、相互引用。

### 近期可执行步骤

1. **Week 1–2（Layer 0 原型）**：
   - 选取 50 段 HumanML3D test set 动作，渲染为视频；
   - 设计 VLM 评分 prompt（4 维：流畅度/物理合理性/语义一致性/表现力），用 GPT-4V API 批量评分；
   - 收集 20 人人类评分，计算 Spearman ρ，对比 FID 基线。
2. **Week 2–4（Layer 1 原型）**：
   - 对 MDM/MoMask 输出运行 kinematic-loss-library 中的 foot contact / joint velocity 检测；
   - 实现 Conformal prediction 置信区间（基于校准集）；
   - 在低置信帧上接 foot contact IK 修正，评估修正前后物理指标。
3. **Month 2（Layer 2 + Layer 3 探索）**：
   - 草拟 Motion Control DSL（参考 ProgMoGen 的约束代码形式）；
   - 用 LLM API 实现初版 DSL parser + 歧义检测；
   - 搭建 Motion Skill MCP server（基于 MDM 或 SALAD 开源实现）。

### 潜在投稿 Venue

| 问题 | 首选 | 备选 |
|------|------|------|
| Layer 0 MotionBench-Perceptual | CVPR 2027 / NeurIPS 2026 Dataset Track | ECCV 2026 |
| Layer 1 Kinematic-Conformal | ICLR 2027 / NeurIPS 2026 | CVPR 2027 |
| Layer 2 Motion Intent DSL | AAAI 2027 / ACM CHI 2027 | CVPR 2027 |
| Layer 3 Motion-as-a-Skill | AAAI 2027 / SIGGRAPH Asia 2026 | ACM MM 2026 |
| Layer 4 VLM-Judge × Prior | NeurIPS 2026 / ICLR 2027 | AAAI 2027 |
