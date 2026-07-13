---
title: "CitySeeker: How Do VLMs Explore Embodied Urban Navigation with Implicit Human Needs?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CitySeeker_How_Do_VLMs_Explore_Embodied_Urban_Navigation_with_Implicit_Human_Needs.pdf
project_link: null
code_link: null
openreview_forum_id: hzf23XSDcs
aliases:
- CBBBCMERAM
- CitySeeker
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过引入类人的认知启发式策略（回溯纠错、空间认知增强、记忆检索）可以部分提升导航成功率，但核心因果杠杆在于模型是否具备城市生活常识（如功能可供性推理）和鲁棒的空间心理模型。简单地增强2D地图理解反而降低任务完成率，说明正确的空间认知表示是敏感调节点。"
primary_logic: "当前VLMs在基于隐性需求的城市导航中的主要瓶颈不是视觉识别，而是缺乏人类般的认知地图和常识推理。任务需要将抽象需求映射为可视觉发现的目标，并动态更新空间信念。模拟人类观察-推理循环的BCR策略（回溯、拓扑认知图、记忆检索）能缓解但远未解决该差距，揭示了空间智能研究的根本挑战。"
claims:
- "最优模型Qwen2.5-VL-32B-Instruct的任务完成率(TCP)仅为21.1%，远低于人类的30.1%。"
- "提供全局2D地图反而使Qwen2.5-VL-32B的TCP从21.1%骤降至7.6%。"
- "组合BCR策略将Qwen2.5-VL-32B的TCP从19.9%提升到27.38%，表明认知启发式有效。"
- "人类主要失败模式为战略性错误(60.7%)，而VLM主要失败模式为认知性错误(32.9%过度/不足推理)。"
---

# CitySeeker: How Do VLMs Explore Embodied Urban Navigation with Implicit Human Needs?

> [!tip] 核心洞察
> 当前VLMs在基于隐性需求的城市导航中的主要瓶颈不是视觉识别，而是缺乏人类般的认知地图和常识推理。任务需要将抽象需求映射为可视觉发现的目标，并动态更新空间信念。模拟人类观察-推理循环的BCR策略（回溯、拓扑认知图、记忆检索）能缓解但远未解决该差距，揭示了空间智能研究的根本挑战。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CitySeeker：视觉语言模型如何探索具有隐性人类需求的具身城市导航？ |
| 英文题名 | CitySeeker: How Do VLMs Explore Embodied Urban Navigation with Implicit Human Needs? |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=hzf23XSDcs) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | CitySeeker Benchmark & BCR (Backtracking, Cognitive-map Enrichment, Retrieval-augmented Memory) 策略 |
| Dataset | CitySeeker (Overall), CitySeeker (BCR improvement) |

> [!tip] 效果简介
> - CitySeeker (Overall) 上，TCP 为 Qwen2.5-VL-32B: 21.1%，对比 Random Choice: 13.9%，变化 +7.2%。
> - CitySeeker (Overall) 上，TCE 为 Qwen2.5-VL-32B: 2.6%，对比 Random Choice: 0.7%，变化 +1.9%。
> - CitySeeker (BCR improvement) 上，TCP 为 Qwen2.5-VL-32B with combined BCR: 27.38%，对比 Qwen2.5-VL-32B without BCR: 19.9%，变化 +7.48%。

## 概要

CitySeeker是一项面向具身城市导航的基准测试，核心挑战在于**隐性需求驱动的视觉定位**——模型需将“我渴了”这类抽象人类意图映射为具体的可导航POI（如便利店、饮水机），而非遵循“前方左转找到星巴克”这样的显式指令。该基准覆盖7个认知难度递增的任务类别（从Basic POI到Abstract Demand与Semantic Preference），在8个全球城市的6,440条轨迹上实施评估。

**核心瓶颈**：当前视觉语言模型（VLMs）在长距离推理中错误累积严重，缺乏人类水平的空间认知与常识推理能力。最优模型**Qwen2.5-VL-32B-Instruct**（Bai et al., 2025）的任务完成率（TCP）仅为21.1%，而人类基线为30.1%。更关键的是，简单地提供全局2D地图反而使该模型的TCP骤降至7.6%，揭示出模型在融合地图与第一人称视角时存在严重的心理旋转与方向感缺陷。

**因果杠杆**：引入类人认知启发式策略——回溯纠错（Backtracking）、空间认知增强（Cognitive-map Enrichment）、记忆检索（Retrieval-augmented Memory）——构成的BCR框架，将Qwen2.5-VL-32B的TCP从19.9%提升至27.38%，证明这些策略是有效的调节点。然而，组合效果并非简单加性，暗示策略间存在复杂交互。

**错误模式对比**：人类主要失败模式为战略性/导航性错误（60.7%），而VLM的瓶颈在于认知性错误——32.9%的失败源于过度推理或推理不足，表现为路径偏离、重复徘徊和过早终止。这揭示了当前VLMs的根本短板不在于视觉识别，而在于缺乏城市生活常识（如功能可供性推理）和鲁棒的空间心理模型。

**方法定位**：CitySeeker采用ReAct风格的“观察-思考-行动-反思”循环，智能体在每步独立决策，不依赖持久记忆。BCR策略通过基于置信度的回溯触发（$\bar{s} < 0.75$）、拓扑认知图构建、Neo4j图数据库检索等手段，模拟人类的空间元认知过程，为空间智能研究提供了可操作的干预框架。

### 隐性需求：城市导航中被忽视的认知鸿沟

城市导航研究长期聚焦于显式指令——如“前往最近的星巴克”或“左转进入主街”——这类任务的核心是将明确的实体标签与视觉环境对齐。然而，人类日常导航中大量存在另一类更为本质的需求：**隐性需求**（implicit needs）。例如，“我渴了”并不直接指定目标，而是要求导航系统理解“渴”对应便利店、饮水机或自动贩卖机等**功能可供性**（affordance），并结合当前城市环境做出合理选择。这种从抽象需求到具体POI的映射，涉及常识推理、空间认知和文化语境理解，构成了视觉语言导航（Vision-Language Navigation, VLN）中一个尚未被系统探索的认知断层。

CitySeeker基准的提出正是为了填补这一空白。如图1所示，该基准将导航指令明确区分为显式需求（如“最近的药店”）和隐性需求（如“我需要休息一下”），后者要求模型自主推断目标POI类别。这种区分揭示了当前视觉语言模型（VLMs）的一个根本性瓶颈：**模型在将抽象需求映射为可视觉发现的目标时表现不佳**，尤其在长距离推理中错误累积严重，缺乏人类级别的空间认知和常识推理能力。

### 现有VLN基准的局限性

现有的视觉语言导航数据集（如R2R、REVERIE、Touchdown等）虽然在推动具身导航研究方面发挥了重要作用，但其任务设计存在两个关键局限。首先，这些基准的指令几乎全部为显式目标描述，回避了需求推断这一核心认知挑战。其次，它们大多基于室内或合成环境，缺乏真实城市街景的视觉复杂性和空间尺度。CitySeeker通过构建**6,440条轨迹、覆盖8个全球分布的城市区域**的大规模基准（图2），将评估场景拓展到真实街景全景数据之上，并引入7个认知难度递增的任务类别——从直接的“Basic POI”识别到高度抽象的“Abstract Demand”和“Semantic Preference”推理——系统性地测量VLM在隐性需求驱动的城市导航中的能力边界。

### 核心瓶颈：认知失败而非视觉失败

初步实验揭示了一个反直觉的发现：**当前最优VLM（Qwen2.5-VL-32B-Instruct）的任务完成率（TCP）仅为21.1%，远低于人类参与者的30.1%**。更值得注意的是，模型的失败模式与人类存在本质差异——人类的主要失败模式为战略性/导航性错误（60.7%），而VLM的主要瓶颈在于**认知性错误**（32.9%的过度推理或推理不足）。这意味着，当前VLMs在城市导航中的短板并非视觉识别能力不足，而是缺乏人类般的**认知地图**（cognitive map）和常识推理机制。模型虽然有完美的记忆潜力，但无法像人类一样形成稳定的空间心理表征，导致路径偏离、重复徘徊和过早终止。

这一诊断将问题焦点从传统的感知-控制流水线转移到了**空间智能**（spatial intelligence）的深层挑战：VLMs能否学习从第一人称视角的街景观察中构建内在的空间信念，并动态更新以支持长距离目标导向导航？CitySeeker的设计正是为了将这一根本问题置于可量化评估的框架之内。

## 核心方法与创新机理

CitySeeker的核心创新在于将城市导航任务从**显式目标指令**转向**隐性人类需求驱动**，并针对该范式下VLM暴露出的系统性缺陷，提出了一套**认知启发式增强策略（BCR）**。这并非模型架构层面的创新，而是任务定义、评估框架与推理时策略的三层重构。

### 1. 任务范式创新：从“找什么”到“需要什么”

传统视觉语言导航（VLN）任务通常给出明确的物体或地点描述（如“前往最近的星巴克”），而CitySeeker引入了**隐性需求驱动的视觉定位**（Implicit-Need-Driven Visual Grounding）。指令不再是具体目标，而是抽象的人类需求陈述（如“我渴了”“我需要处理紧急工作”），要求智能体自主完成从需求到POI功能可供性的映射，再通过视觉搜索定位目标。

这一转变将任务的认知负荷从**视觉匹配**转移到**常识推理与空间认知**上。任务按认知难度分为7个子类，形成从直接识别（Basic POI）到高度抽象推理（Abstract Demand, Semantic Preference）的难度谱系（见Figure 1）。跨文化共识调查（N=120，平均共识度83.39%）验证了需求到POI映射的合理性，确保评估的生态效度。

### 2. 评估框架创新：多维度空间推理度量

CitySeeker的评估体系超越了简单的任务完成率（TCP），引入了**任务完成效率（TCE）**——仅在严格路径约束下完成才算成功——以区分“碰巧到达”与“高效导航”。配合nDTW（归一化动态时间规整）、SPL（路径长度加权成功率）等指标，形成对空间推理质量的细粒度度量。这一设计直接暴露了当前VLM的核心瓶颈：最优模型Qwen2.5-VL-32B-Instruct的TCP仅为21.1%，TCE更是低至2.6%，而人类基线分别为30.1%和5.5%（Table 2）。

### 3. BCR策略：三个认知启发式增强槽位

针对VLM在长距离推理中的错误累积、空间认知缺失和记忆断裂问题，BCR策略在三个可插拔的槽位上引入了类人认知启发式，每个槽位均从“无”变为“有”：

| 策略槽位 | 基线状态 | 创新设计 | 核心机制 |
|---------|---------|---------|---------|
| **Backtracking（回溯纠错）** | 无回溯机制，错误路径不可逆 | B1: 置信度滑动窗口触发；B2: 拓扑距离单调递增触发；B3: 人导方向提示 | 模拟人类“走错了回头”的元认知监控 |
| **Spatial Cognition（空间认知增强）** | 仅有第一人称视角，无全局空间感知 | C1: 拓扑认知图（节点-边结构）；C2: 相对位置图（方向线索+估计距离） | 为VLM注入结构化空间上下文，模拟认知地图 |
| **Memory Retrieval（记忆检索）** | 无状态智能体，每步独立决策 | R1: 基于Neo4j的拓扑检索；R2: 空间邻近检索；R3: 轮内历史轨迹查询 | 提供持久化记忆能力，避免重复徘徊 |

**回溯机制**的核心创新在于将VLM的“自我怀疑”量化为可操作的触发信号。基础回溯（B1）利用VLM自身输出的置信度分数，当滑动窗口内平均置信度低于阈值 $\theta=0.75$ 时触发回退：

$$\bar{s} = \frac{1}{k} \sum_{i=n-k+1}^{n} s_i < \theta$$

步长奖励回溯（B2）则用客观的拓扑距离替代主观置信度，当距离连续 $k$ 步单调递增时触发：

$$\bigwedge_{i=0}^{k-1} \left( d_{t-i} > d_{t-(i+1)} \right)$$

人导回溯（B3）在回溯后通过最小化期望未来图论距离选择最优动作，提供了理论上的上界参考：

$$a^{*} = \underset{a \in \mathcal{A}}{\arg\min} \mathbb{E}[d_{t+1} | a_t = a]$$

**空间认知增强**的关键洞察是：直接提供全局2D地图反而使Qwen2.5-VL-32B的TCP从21.1%骤降至7.6%（Table 13），表明VLM缺乏将2D地图与第一人称视角进行心理旋转和对齐的能力。C1和C2转而提供**结构化文本描述**的空间关系，避开了视觉-空间模态融合的障碍。

**记忆检索**的引入打破了基线中“每步独立决策”的设计约束，使智能体能够利用历史信息避免重复访问和路径循环。

### 4. 组合效应与相互作用

BCR策略的组合并非简单加性。组合策略（B2+B3+C1+R3）将Qwen2.5-VL-32B的TCP从19.9%提升至27.38%（+7.48%），但仍远低于人类水平（Table 14）。各策略间存在复杂的相互作用：例如，B1对大多数模型有效，却在MiniCPM-V-2.6上导致TCP从11.3%降至9.1%（Table 3），说明置信度校准能力是回溯有效性的前提条件。

### 创新边界与遗留问题

BCR策略本质上是**推理时的启发式补丁**，并未改变VLM自身的空间推理能力。核心因果杠杆——模型是否具备城市生活常识（如功能可供性推理）和鲁棒的空间心理模型——仍未被触及。如何将人类水平的常识推理注入VLM，以及如何实现真正的认知地图式内在空间表征，是CitySeeker揭示的根本性开放问题。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_hzf23XSDcs/figures/005_Figure_4.jpg]]
*Figure 4: The CitySeeker Implicit-Need-Driven Embodied Urban Navigation Framework. 4 EVALUATION ON CITYSEEKER*

### 任务形式化

CitySeeker将具身城市导航建模为图上的视觉语言导航（VLN）任务。城市路网被离散化为有向图 $\mathcal{G} = (\nu, \mathcal{E})$，其中节点 $\nu$ 表示每隔约20米采样的地理位置，边 $\mathcal{E}$ 表示可导航的街道连接。每个节点 $v_t$ 处，360度全景影像被分割为 $n$ 个透视图，构成观察集 $\mathcal{O}_t = \{ o_{t,1}, o_{t,2}, \ldots, o_{t,n} \}$，每个透视图对应一个可行的移动方向。

给定一段隐含用户需求的自然语言指令 $\mathcal{W}$（如“我渴了”或“找个安静的地方看书”），智能体从起始节点 $v_0$ 出发，在每一步 $t$ 接收当前状态 $s_t$（包含全景观察和指令），通过策略 $\pi_{\Theta}$ 输出三元组：

$$(\Phi_t, a_t, c_t) = \pi_{\Theta}(\mathcal{W}, s_t)$$

其中 $\Phi_t$ 为推理依据（自然语言思维链），$a_t$ 为选中的动作索引（即透视图编号），$c_t$ 为当前决策的置信度分数。智能体沿所选方向移动到下一节点，循环直至触发终止条件或达到最大步数限制。

### 观察-推理-行动-反思循环

框架采用ReAct风格的认知循环，由四个串行模块构成（图4）：

1. **全景捕捉与投影（Panoramic Capture & Projection）**：在当前视点捕获360度全景，按可行方向分割为多个透视图，每个透视图对应一个候选移动方向。这一预处理步骤将连续的全景空间离散化为VLM可处理的图像序列。

2. **观察（Observe）**：VLM接收当前透视图集与任务指令，提取环境中的视觉线索——店招文字、建筑外观、街道特征等——作为后续推理的感知基础。

3. **思考（Think）**：基于观察结果，VLM推断导航意图与子目标。这一步骤是隐性需求映射的核心：模型需将抽象需求（“我饿了”）转化为可视觉定位的目标类别（餐厅、便利店），并据此判断当前视野中哪个方向最可能通向目标。

4. **行动（Act）**：选择最匹配推理意图的透视图作为移动方向，执行一步导航。

5. **反思（Reflect）**：输出当前决策的置信度分数 $c_t$。该分数既作为回溯机制的触发信号，也为后续分析提供决策质量的可量化指标。

### 无状态设计选择

为隔离模型的核心空间推理能力，框架刻意保持每步决策的独立性：智能体不维护持久记忆，也不将先前的内部状态馈入后续决策。这一设计使得任何导航成功必须完全依赖当前观察与指令的实时推理，从而暴露VLMs在缺乏累积空间认知时的真实能力边界。

### 评测基准配置

CitySeeker基准包含6,440条轨迹，覆盖全球8个城市区域（包括北京、纽约等），涉及7个认知难度递增的任务类别：Basic POI（基本POI识别）、Brand-Specific（品牌特定导航）、Transit Hub（交通枢纽）、Latent POI（隐性POI映射）、Abstract Demand（抽象需求推理）、Inclusive Infrastructure（无障碍设施）、Semantic Preference（语义偏好）。每条轨迹配有经跨文化共识验证（N=120，平均共识度83.39%）的需求-POI映射真值。

评测指标包括任务完成率（TCP，以距目标50米内为成功）、严格完成率（TCE，精确到达目标节点）、任务完成覆盖率（TCC）、路径长度加权成功率（SPL）和归一化动态时间规整距离（nDTW）等。

### 导航任务形式化

CitySeeker将具身城市导航建模为图上的顺序决策问题。城市路网被离散化为导航图 $\mathcal{G} = (\nu, \mathcal{E})$，其中节点 $\nu$ 表示地理位置（每20米采样一个节点），边 $\mathcal{E}$ 表示可导航的连接。在每个时间步 $t$，智能体位于节点 $v_t$，接收由全景图分割产生的 $n$ 个透视图观测集 $\mathcal{O}_t = \{ o_{t,1}, o_{t,2}, \ldots, o_{t,n} \}$，每个透视图对应一个可行的行进方向。

给定自然语言指令 $\mathcal{W}$（包含隐性需求描述），策略 $\pi_{\Theta}$ 输出三元组：

$$(\Phi_t, a_t, c_t) = \pi_{\Theta}(\mathcal{W}, s_t)$$

其中 $\Phi_t$ 为推理依据（自然语言思维链），$a_t$ 为选择的透视图索引（即动作方向），$c_t$ 为当前决策的置信度分数。状态 $s_t$ 仅包含当前观测，不维护跨步持久记忆——这一设计有意隔离模型的核心空间推理能力。

### 观察-推理-行动-反思流水线

框架采用类ReAct的认知循环，包含五个顺序模块：

1. **全景捕获与投影**：在当前视点捕获360°全景图像，按可行方向分割为多个透视图。
2. **观察**：VLM处理当前透视图集和导航指令，提取环境语义信息。
3. **思考**：基于观察推断导航意图与子目标，生成推理依据 $\Phi_t$。
4. **行动**：选择最匹配当前意图的透视图作为移动方向 $a_t$。
5. **反思**：输出置信度分数 $c_t$，用于回溯触发的状态监控。

### 基础回溯触发条件

基础回溯策略通过滑动窗口内的平均置信度监测智能体的决策质量。当最近 $k$ 步的平均置信度低于预设阈值 $\theta$ 时触发回溯：

$$\bar{s} = \frac{1}{k} \sum_{i=n-k+1}^{n} s_i < \theta \quad (\theta = 0.75)$$

触发后，智能体沿历史轨迹回退至最后一个高置信度节点，重新选择方向。

### 步长奖励回溯触发条件

步长奖励回溯将主观置信度替换为客观进度度量——当前节点到目标节点的拓扑距离 $d_t$。回溯在拓扑距离连续 $k$ 步单调递增时触发，表明智能体正在系统性地远离目标：

$$\bigwedge_{i=0}^{k-1} \left( d_{t-i} > d_{t-(i+1)} \right)$$

该条件通过纯客观的空间度量避免了VLM过度自信导致的错误累积。

### 人导回溯最优动作选择

人导回溯在触发后不仅回退，还提供方向性纠正提示。回溯后的最优动作选择通过最小化期望未来图论距离实现：

$$a^{*} = \underset{a \in \mathcal{A}}{\arg\min} \mathbb{E}[d_{t+1} | a_t = a]$$

其中 $\mathcal{A}$ 为当前节点的可行动作集，$d_{t+1}$ 为执行动作后的拓扑距离。

### 路径一致性动作选择

在空间认知增强模块中，当提供相对位置地图时，动作选择通过路径一致性函数引导：

$$\phi(a) = \mathbb{I}_{\theta_a \in \Theta_{optimal}} \cdot \cos(\theta_a - \theta_{path})$$

其中 $\mathbb{I}$ 为指示函数，筛选位于最优方向扇区 $\Theta_{optimal}$ 内的候选动作；$\cos(\theta_a - \theta_{path})$ 度量候选方向与最优路径方向的余弦相似度。选择 $\phi(a)$ 最大的动作，确保行进方向与全局路径规划保持一致。

### 空间认知增强与记忆检索的表示层

**拓扑认知图**将环境建模为结构化图，节点表示已访问/已知位置，边表示可行动作转换。该图以文本形式注入VLM提示，提供环境的连接性先验。

**相对位置地图**以方向线索（如“左侧”、“稍右”）和估计距离描述位置间的空间关系，强调空间定向而非精确度量。

**记忆检索**基于Neo4j图数据库实现，包含三种检索模式：拓扑检索沿图结构查询关联节点、空间检索按邻近度召回位置、历史轨迹查找提供当前回合内的短期路径记忆。

## 实验与关键发现

### 评估设置与基线

CitySeeker基准在8个全球城市区域上构建了6,440条导航轨迹，涵盖7个认知难度递增的任务类别：Basic POI、Brand-Specific、Transit Hub、Latent POI、Abstract Demand、Inclusive Infrastructure和Semantic Preference。评估采用多维度指标：任务完成率（TCP，以50m为阈值）、严格完成率（TCE，精确到达目标节点）、完成一致性（TCC）、路径效率（SPD）和归一化动态时间规整（nDTW）。

实验设置了三类基线：（1）**人类基线**，由10名不同文化背景的参与者通过交互平台完成导航任务；（2）**随机选择基线**，在每一步随机选择一个可行方向；（3）**前进方向基线**，始终选择朝向目标大致方向移动的朴素启发式。评估覆盖27个视觉语言模型，包括GPT-4o、GPT-4o-mini、o4-mini、Gemini-2.5-pro等闭源模型，以及Qwen2.5-VL-32B-Instruct（Bai et al., 2025）、InternVL3-8B/38B、Llama-4-Scout-17B等开源模型。

### 主要结果

**Table 2** 呈现了完整基准结果。最优模型Qwen2.5-VL-32B-Instruct的整体TCP仅为21.1%，TCE仅为2.6%，而人类基线TCP为30.1%。随机选择基线的TCP为13.9%，TCE为0.7%，表明当前VLMs在该任务上的表现仅略优于随机策略。InternVL3-38B以19.3%的TCP位居第二，GPT-4o的TCE为2.4%。所有模型在TCE指标上均表现极低，说明精确到达目标节点的能力严重不足。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_hzf23XSDcs/figures/006_Table_2.jpg]]
*Table 2: The performance of CitySeeker Framework. For Subcategory evaluations, the TCP score is reported. Top performers are highlighted in bold, while secondary leaders are underlined. For details on the AS metric and a more comprehensive evaluation of the models, please refer to Appendix C.3*

从子类别来看（**Figure 5**雷达图），模型在Brand-Specific（品牌特定）导航上表现最佳，而在Abstract Demand（抽象需求）和Semantic Preference（语义偏好）等需要深层推理的类别上表现最差。城市间对比（**Figure 5**柱状图）显示，模型在北京和纽约的表现存在差异，但跨语言实验（**Table 12**）表明，将提示本地化为中文并未带来一致提升，说明语言偏见不是城市间性能差异的主要驱动因素。

**Figure 6**的热力图和散点图揭示了路径行为的深层问题：GPT-4o的轨迹分布显示出明显的偏离和徘徊模式，且随着步数增加，nDTW变得高度离散，表明长距离导航中错误累积严重。

### 失败模式分析

**Table 15** 对人类与最优VLM（Qwen2.5-VL-32B）的失败模式进行了详细比较。人类的主要失败模式为战略性/导航性错误（60.7%），即路径规划层面的失误；而VLM的关键瓶颈在于**认知性错误**——过度推理或推理不足占32.9%。**Figure 18**展示了Qwen2.5-VL-32B和InternVL3-8B的错误类型分布，进一步证实认知失败是VLM的核心短板。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_hzf23XSDcs/figures/038_Table_15.jpg]]
*Table 15: Detailed comparison of primary failure modes between humans and the top-performing VLM (Qwen2.5-VL-32B)*

具体而言，VLMs在需要从隐含需求推断POI功能时频繁出错，例如将“我渴了”映射到便利店或饮水机时出现功能可供性推理失败。模型虽有完美的记忆潜力，但无法形成类人的认知地图，导致路径偏离、重复徘徊和过早终止。

### 消融实验：地图增强的意外退化

**Table 13** 报告了一项关键消融：向Qwen2.5-VL-32B-Instruct提供全局2D地图后，TCP从21.1%骤降至7.6%，TCE从2.6%降至0.4%。虽然nDTW有所改善（从147.0降至54.4，表明路径更接近最优轨迹），但任务完成率的大幅下降揭示了**2D地图与第一人称视角对齐的根本困难**。模型缺乏心理旋转与空间方向感，融合地图信息反而干扰了其基于视觉的语义推理。**Figure 10**展示了地图增强下的典型推理失败案例，模型在理解自身在地图中的位置和朝向时出现严重混乱。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_hzf23XSDcs/figures/024_Table_13.jpg]]
*Table 13: Performance comparison between the map-free and map-augmented navigation settings on the full test set. The new results reveal a trade-off where map guidance improves path following (nDTW) but degrades task completion (TCP/TCE)*

### BCR策略效果

针对上述瓶颈，论文提出了BCR三管齐下策略：回溯机制（Backtracking）、空间认知增强（Spatial Cognition Enrichment）和记忆检索（Memory-Based Retrieval）。**Table 3** 报告了各策略在五个模型上的独立效果：

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_hzf23XSDcs/figures/012_Table_3.jpg]]
*Table 3: Performance of different models on TCP and nDTW under three strategies. The best results are highlighted in bold*

- **回溯机制**：B1（置信度触发回溯）普遍提升TCP，但在MiniCPM-V-2.6上反而从11.3%降至9.1%，说明对推理能力较弱的模型可能产生干扰。B3（人导回溯）将GPT-4o-Mini的TCP提升至18.2%，nDTW从337.1降至258.3，显著改善路径效率。
- **空间认知增强**：C1（拓扑认知图）将GPT-4o-Mini的TCP从12.5%提升至17.2%，但C2（相对位置图）的效果不如C1稳定。
- **记忆检索**：R3（短期轨迹历史）对多数模型有正向效果，但提升幅度有限。

**Table 14** 报告了组合BCR策略的效果：将B2、B3、C1和R3组合应用于Qwen2.5-VL-32B，TCP从19.9%提升至27.38%（+7.48%），但效果并非简单加性，表明策略间存在复杂的相互作用。组合策略仍远未达到人类水平（30.1%），揭示了空间智能研究的根本挑战。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_hzf23XSDcs/figures/035_Table_14.jpg]]
*Table 14: Performance with combined BCR strategies*

### 核心发现总结

1. **认知瓶颈优先于视觉识别**：当前VLMs在隐性需求城市导航中的主要瓶颈不是视觉感知，而是缺乏类人的认知地图和常识推理能力。
2. **2D地图融合是敏感调节点**：简单地增强全局地图理解反而降低任务完成率，说明正确的空间认知表示形式至关重要。
3. **BCR策略缓解但远未解决差距**：认知启发式策略能部分提升成功率，但组合优化空间大，且效果受模型基础能力制约。
4. **失败模式存在质的不同**：人类偏战略性失误，VLM偏认知性失误，指向了常识注入和空间表征学习的根本性研究需求。

## 定位与知识库关联

### 与现有视觉语言导航基准的关系

CitySeeker 在视觉语言导航（VLN）领域引入了一个此前未被系统评估的维度：**隐性需求驱动的具身城市导航**。传统 VLN 基准如 Room-to-Room（R2R）、Touchdown 等主要关注显式指令下的室内或街景导航（见表1），而 CitySeeker 将任务定义从“按指令到达指定位置”转变为“从隐含的人类需求推断目标并自主导航到达”，这要求模型具备城市生活常识与功能可供性推理能力。

该基准包含 7 个认知难度递增的任务类别：从直接识别的“Basic POI”到高度抽象的“Abstract Demand”和“Semantic Preference”，覆盖 8 个全球城市区域的 6,440 条轨迹。与现有数据集的核心区别在于，CitySeeker 的指令不显式命名目标地点，而是通过隐性需求（如“我渴了”）或抽象偏好（如“我想去一个安静的地方看书”）来驱动导航决策。

### 基线模型谱系

CitySeeker 在 27 个模型上进行了系统评估，基线覆盖以下类别：

**专有闭源模型**（zero-shot baseline）：**GPT-4o**、**GPT-4o-mini**、**o4-mini**、**Gemini-2.5-pro** 等。这些模型在通用视觉推理任务上表现强劲，但在隐性需求导航中暴露出显著缺陷——GPT-4o 的总体任务完成率（TCP）仅为 17.3%，任务完成效率（TCE）为 2.4%。

**开源视觉语言模型**（zero-shot baseline）：**Qwen2.5-VL-32B-Instruct**（Bai et al., 2025）以 21.1% 的 TCP 取得最优表现，**InternVL3-38B** 以 19.3% 紧随其后，**InternVL3-8B**、**Llama-4-Scout-17B** 等模型表现进一步下降。

**人类基准**：10 名不同文化背景的参与者通过交互式平台完成任务，取得 30.1% 的 TCP，在所有指标上均优于最佳模型。

**启发式下界**：Random Choice Baseline（TCP 13.9%）和 Forward Direction Baseline 作为导航策略的朴素参照。

### BCR 策略的方法定位

BCR（Backtracking, Cognitive-map Enrichment, Retrieval-augmented Memory）策略并非提出新的模型架构，而是**在现有 VLM 推理流程之上叠加类人的认知启发式模块**，其设计借鉴了认知科学中关于人类空间导航的经典理论——认知地图、路径整合和回溯纠错。三组策略的技术谱系如下：

**回溯机制（B1-B3）** 从简单的置信度阈值触发（B1：滑动窗口平均置信度 $\bar{s} < \theta = 0.75$），到基于客观拓扑距离的步长奖励回溯（B2：连续 $k$ 步距离单调递增 $\bigwedge_{i=0}^{k-1} (d_{t-i} > d_{t-(i+1)})$），再到利用 Oracle 信息的 Human-Guided Backtracking（B3：选择最小化期望未来距离的动作 $a^{*} = \arg\min \mathbb{E}[d_{t+1} | a_t = a]$）。这种从主观置信度到客观度量再到理想信息的递进设计，旨在诊断错误检测机制的有效性上限。

**空间认知增强（C1-C2）** 试图弥补 VLM 缺乏心理地图的根本缺陷。C1 的拓扑认知图以节点-边结构表示位置间可达关系，C2 的相对位置图则提供方向线索和估计距离。值得注意的是，直接提供全局 2D 地图反而使 Qwen2.5-VL-32B-Instruct 的 TCP 从 21.1% 骤降至 7.6%，表明**简单的空间信息注入与 VLM 的第一人称视角推理之间存在严重对齐障碍**——模型缺乏心理旋转和方向感，无法有效融合鸟瞰地图与街景观察。

**记忆检索（R1-R3）** 基于 Neo4j 图数据库实现，分别从拓扑关系（R1）、空间邻近性（R2）和短期轨迹历史（R3）三个维度检索相关信息。这与现有 VLN 工作中使用外部记忆增强导航的策略思路一致，但 CitySeeker 的独特之处在于将记忆检索与隐性需求推理相结合——模型需要记住的不是显式路标，而是与抽象需求相关的功能场所分布。

### 适用边界

BCR 策略的有效性存在明确的边界条件：

1. **模型能力依赖**：B1（置信度回溯）在 MiniCPM-V-2.6 上反而导致 TCP 从 11.3% 降至 9.1%，说明置信度校准能力不足的模型无法从简单的阈值触发中获益。B3（人导回溯）将 GPT-4o-Mini 的 TCP 推至 18.2%，nDTW 从 337.1 降至 258.3，但其依赖 Oracle 信息，不具备实际部署的可行性。

2. **路径长度敏感**：随着路径步数增加，模型性能持续下降。当步数达到约 35 步时，nDTW 变得高度离散，表明长距离导航中错误累积效应显著——早期推理错误会级联放大，导致路径偏离和重复徘徊。

3. **路网结构影响**：模型在不规则路网中性能下降明显，BCR 策略对此类场景的改善有限。拓扑认知图（C1）的前提是路网具有良好的图结构表示，对于复杂交叉口或非标准道路布局，其有效性需要进一步验证。

4. **组合效应非线性**：组合 BCR 策略将 Qwen2.5-VL-32B 的 TCP 从 19.9% 提升至 27.38%，但提升幅度并非各策略效果的简单加和，存在复杂的相互作用——某些策略组合可能产生冗余甚至冲突。

### 局限与开放问题

**核心局限**：

- **长上下文推理瓶颈**：长距离导航需要处理大量视觉和文本 token，导致早期信息遗忘和重复回路。当前的无状态推理设计虽然隔离了模型的核心空间推理能力，但也排除了持续上下文保留的可能性。
- **2D 地图融合失败**：模型缺乏心理旋转与方向感，融合地图信息反而降低完成率，揭示了第一人称视角与全局空间表征之间的根本性对齐难题。
- **实时性不足**：VLM 决策延迟大，冗余视觉处理限制了实际部署的可能。
- **缺乏个性化建模**：当前框架未考虑用户偏好的个体差异，所有导航决策基于通用常识映射。

**关键开放问题**：

1. 如何将人类水平的常识推理与功能可供性知识注入 VLM，以减少“认知失败”（当前 VLM 主要失败模式中 32.9% 为过度/不足推理）？
2. 如何有效融合 2D 地图与第一人称街景，同时保留语义推理能力——是改进空间表示形式，还是增强模型的内部空间表征能力？
3. VLM 能否通过学习获得类似认知地图的内在空间表征，而非依赖外部图结构？这触及空间智能研究的根本问题。
4. BCR 策略的组合优化空间远未穷尽，如何找到特定场景下的最优策略组合？
5. 跨城市泛化能力如何提升？语言本地化实验表明语言偏见并非城市间性能差异的主要驱动因素，暗示更深层的视觉和文化因素在起作用。

## 原文 PDF

![[paperPDFs/ICLR_2026/CitySeeker_How_Do_VLMs_Explore_Embodied_Urban_Navigation_with_Implicit_Human_Needs.pdf]]
