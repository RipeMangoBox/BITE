---
title: "Training-free Counterfactual Explanation for Temporal Graph Model Inference"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Training_free_Counterfactual_Explanation_for_Temporal_Graph_Model_Inference.pdf
aliases:
- TTGE
- TFCETGMI
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/alignment_preference
core_operator: "在滑动时间窗口内，通过移除历史边（反事实操作）改变 TGNN 输出，利用结合独立级联模型（ICM）、时间电阻距离（TRD）和指数衰减的时间影响力评分，选择并验证关键节点。"
primary_logic: "通过将独立级联模型、时间电阻距离和指数衰减统一在滑动窗口中，量化节点对目标的影响力，并用贪心验证算法生成满足反事实条件的紧凑时间子图，实现可解释、可查询的时序图模型理解。"
claims:
- "定义反事实边：如果移除边 e 后 TGNN 输出改变，则 e 是反事实边。"
- "解释性子图由解释节点和连接节点组成，满足 δ-可达性以保证时间连贯性。"
- "TemGX 算法对单调次模优化问题提供 (1-1/e) 的近似保证。"
- "在 UCIM+TGN 上，TemGX 的保真度 (0.468) 比 TempME (0.219) 提升 113%。"
---

# Training-free Counterfactual Explanation for Temporal Graph Model Inference

> [!tip] 核心洞察
> 通过将独立级联模型、时间电阻距离和指数衰减统一在滑动窗口中，量化节点对目标的影响力，并用贪心验证算法生成满足反事实条件的紧凑时间子图，实现可解释、可查询的时序图模型理解。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向时序图模型推理的无训练反事实解释 |
| 英文题名 | Training-free Counterfactual Explanation for Temporal Graph Model Inference |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=NqtYz3A8tQ) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/alignment_preference |
| Method | TemGX (TEMporal Graph eXplainer) |
| Dataset | UCIM (Link Prediction), METR-LA (Regression) |

> [!tip] 效果简介
> - UCIM (Link Prediction) 上，Fidelity 为 0.468 (TemGX+TGN)，对比 0.219 (TempME+TGN)，变化 +0.249 (113% 提升)。
> - UCIM (Link Prediction) 上，AUFSC 为 0.475 (TemGX+TGN)，对比 0.218 (TempME+TGN)，变化 +0.257。
> - UCIM (Link Prediction) 上，Runtime (s) 为 8.2 (TemGX+TGN)，对比 88.4 (TempME+TGN)，变化 −80.2s (约 10.8× 加速)。

## 概述

时序图神经网络（TGNN）已被广泛用于动态图中的链接预测、节点分类和时空回归等任务，但其推理过程难以解释，制约了模型在高风险场景中的可信部署。现有解释方法主要在静态或离散快照上生成子图，无法有效建模时间依赖性，缺乏严格的反事实验证，并且不能提供灵活的结构化查询与“what‑if”分析。针对这些瓶颈，本文提出 **TemGX（TEMporal Graph eXplainer）**，一种训练无关的反事实解释框架。TemGX 在滑动时间窗口内，通过独立级联模型（ICM）量化移除历史边造成的模型输出变化，结合时间电阻距离（TRD）和指数衰减捕捉时空影响力，并采用具有近似保证的贪心验证算法，生成包含解释节点和连接节点的 δ‑可达时间子图。该子图在移除后必须改变 TGNN 对目标节点的预测，从而满足严格的反事实要求，同时保持时间连贯性。方法还支持时序模式匹配查询和动态贝叶斯网络推理，提升了交互分析能力。

实验覆盖六个真实动态图数据集和三种主流任务（链接预测、时空回归、节点分类），与 TempME、TGVex、TGNNExplainer、CoDy 等基线进行全面比较。在 UCIM 链接预测任务上，TemGX 的保真度达到 0.468（TGN 主干），较最佳基线 TempME 提升 113%；AUFSC 达到 0.475，同时解释生成速度提升约 10.8 倍（8.2 s vs 88.4 s）。在 METR‑LA 时空回归任务上，保真度亦达 0.471（STGCN 主干）。消融实验表明，ICM 组件对性能贡献最大（去除后保真度下降 34.2%），时间衰减和 TRD 同样不可或缺。翻转率分析进一步确认，移除解释子图后模型预测改变的比例稳定在 81%–87%，说明 TemGX 解释具有高反事实有效性。整体而言，TemGX 无需额外训练，具备理论近似保证和实用效率，为时序图模型的可解释性提供了新的基础方案。

## 背景与动机

动态网络（如金融交易、网络安全、交通预测等）的建模越来越依赖时序图神经网络（Temporal Graph Neural Networks, TGNN）。TGNN 通过编码器‑解码器结构（$f_{E}, f_{D}$）将历史交互序列映射为节点嵌入，并对未来链路概率、节点属性等进行预测（Section 2）。然而，TGNN 的决策过程高度不透明，在金融欺诈检测（Figure 1 中的 Peel Chain 与 Spindle 洗钱模式）、多阶段攻击链溯源等安全关键应用中，模型预测的“黑箱”属性严重制约了其可信部署与人工审核。因此，如何为 TGNN 预测提供可解释、可验证的解释成为迫切需求。

现有 TGNN 解释方法尚面临四个核心缺口：

1. **时间依赖性建模有限**。多数方法仅利用静态结构或局部时间模式：TGVex 将静态图解释器 GVex 扩展为在每个快照独立生成子图，丢失了快照间的动态传播逻辑；TempME 虽引入时间模体，但无法刻画跨越多个时间步的累积影响力与衰减效应。TGNNExplainer 的导航器‑探索者框架亦未显式量化时间维度上的影响传播——节点对目标的作用应随间隔增大而减弱，且受拓扑与嵌入相似性共同调节，现有方法缺乏统一建模。

2. **缺乏严格的反事实验证**。解释的真正效力在于：移除解释结构应确实改变模型输出。已有工作或未实施反事实检查（仅依赖启发式行为），或需要额外训练（如 CoDy 搜索最小反事实边集但未将反事实条件深度嵌入时间影响评估），导致解释的真实性难以保障。

3. **训练开销大**。TGVex、TGNNExplainer、TempME、CoDy 均需为特定 TGNN 再训练导航器、解释器或搜索代理，限制了通用性与实用效率，尤其在大规模动态图上重训练代价极高。

4. **无法提供灵活的查询与分析能力**。现有方法输出单一静态子图，不支持用户依时序模式进行实时交互查询或“what‑if”推理，难以直接融入动态网络的分析工作流。

上述不足使现有解释频繁出现时间上不连贯的孤岛事件，且难以适配实际动态网络的解释需求。

针对这些瓶颈，本文提出 **TemGX (TEMporal Graph eXplainer)**——一个**训练无关、反事实**的时序图解释框架。其核心洞察为：**在滑动时间窗口内，通过独立级联模型（ICM）、时间电阻距离（TRD）与指数衰减的统一量化节点对目标的影响力，并借助贪心验证算法生成满足反事实条件的紧凑时间子图**，从而实现可解释、可查询的 TGNN 输出理解 [core_insight]。具体而言，TemGX 具备三项动机驱动的关键能力：

- **强制时间一致性**：要求解释子图满足 δ‑可达性，确保所有解释节点通过时间路径与目标节点相连，避免时间断裂（Section 3）。  
- **严格反事实验证**：每次候选节点加入均执行 `Verify` 过程，基于反事实边定义（移除节点后模型输出改变）筛选解释节点，从机制上保证解释的因果性（Section 3, 4）。  
- **训练无关 + 可查询**：直接复用预训练 TGNN，无需额外训练；并支持时序模式查询与动态贝叶斯网络摘要，赋予用户“what‑if”推理能力（Section 3, Appendix B）。

实验表明，TemGX 在保真度与效率上显著超越现有基线：在 UCIM 数据集上相对 TempME 保真度提升 113%（0.468 vs. 0.219，Table 1），且消融实验确认 ICM、TRD 与时间衰减等都是保障性能的关键组件（Table 3）。至此，TemGX 填补了时序图模型解释中训练无关的反事实方案与时间感知互动能力的空白。

## 核心创新

相较于现有的 TGNN 解释方法，TemGX 在三个层面形成了关键突破：**解释结构的时序化、影响力建模的体系化、验证与优化的严格化**，并将训练依赖转化为训练无关的实用框架。以下根据相对基线的 changed slots 逐一展开。

1. **从静态/边级解释到时间连贯的解释性子图**  
   现有方法（如 TGVex 在每个快照上独立生成子图，TempME 输出局部模体）大多丢失了时间上下文，导致解释结构在时序上割裂。TemGX 以 **δ‑可达性** 为核心约束，将解释定义为“解释节点 $V_s$ + 连接节点 $V_c$”组成的紧致时序子图，强制要求解释结构在滑动窗口内形成连贯的因果链。这一结构创新使得解释能够保留时间依赖，并在定性对比中展现出显著的高时间一致性（Table 7）。

2. **从局部时间模式到统一的时间影响力评分**  
   基线方法或仅依赖静态图结构，或只利用简单的时序模体，无法充分捕捉节点在动态网络中的累积影响。TemGX 集成了三个互补机制：  
   - **独立级联模型（ICM）** 计算逐条边移除时 TGNN 输出的变化概率；  
   - **时间电阻距离（TRD）** 在嵌入空间中度量解释节点与目标节点的结构/语义距离；  
   - **指数衰减函数** 模拟时间远近对影响力的弱化。  
   三者通过滑动窗口内的递归聚合构成影响力得分 $\Phi$（式 3），从而将拓扑影响、嵌入相似性和时间因素统一建模。消融实验表明，ICM 是影响保真度最大的组件（移除后下降 34.2%），而 TRD 和时间衰减也分别贡献约 17% 和 15% 的性能，验证了多组件协同的必要性。

3. **从无验证到强制反事实验证的贪心算法**  
   已有解释器（包括 CoDy 的蒙特卡洛搜索）普遍缺乏严格的反事实要求。TemGX 原创性地定义了 **counterfactual edge** 概念，并要求算法内部对每个候选节点执行 Verify 过程——只有当移除该节点确实改变模型输出时，才将其保留为解释节点。同时，它将解释节点选择规约为单调次模最大化问题，采用贪心替换策略且提供了 **$(1-1/e)$ 近似保证**（Lemma 3），在可证明的质量边界内高效生成解释。这一设计从根本上消解了传统启发式方法的不确定性。

4. **从训练依赖到训练无关的运行范式**  
   CoDy 等需要额外训练解释器模型，成本高且泛化受限。TemGX 完全基于预训练 TGNN 的前向推理，无需任何训练步骤，因此不仅降低了使用门槛，还大幅缩短了运行时间——在 UCIM+TGN 上，单次解释仅需 8.2 s，比 TempME 快约 10.8 倍（88.4 s），体现出“训练无关”架构在实用性上的决定性优势。

5. **从固定结果到可交互的解释与查询**  
   传统方法仅输出一个最终子图，而 TemGX 进一步支持时序模式查询，并能从一批解释实例中学习 **动态贝叶斯网络（DBN）** 作为概率化摘要（通过 BIC 得分优化结构，附录 B）。这使领域专家可以执行“what‑if”推理和交互式验证，将解释从一次性产出转变为持续的分析工具。

上述 changed slots 共同支撑了 TemGX 在核心指标上的大幅提升：在 UCIM+TGN 上，相较于最强的基线 TempME（保真度 0.219），TemGX 达到 0.468（提升 113%），同时 AUFSC 达到 0.475，验证了时序反事实解释框架的有效性。

## 整体框架

![[assets/figures/papers/iclr26_0013_NqtYz3A8tQ_Training-free_Counterfactual_Explanation_for_Tem/figures/002_Figure_2.jpg]]
*Figure 2: Overview of TemGX framework. Given a target node vt and temporal graph $G _ { t }$ , it constructs a $\delta \mathrm { - }$ reachable candidate pool and estimate influence as the probability of changes when removing each candidate. TRD back-propagation captures temporal resistance, and a temporal influence score $\phi$ combines influence, TRD, and temporal decay. Top-scoring nodes form the explanatory set $V _ { s }$ , induced connectors $V _ { c }$ ensure temporal connectivity, and counterfactual verification confirms that removing $V _ { s } \cup V _ { c }$ changes the TGNN prediction M ( $G _ { t } , v _ { t }$ ) , which in turn contribute to temporal explanations

TemGX 提出一种训练无关的时序图神经网络解释框架，其核心是将解释问题建模为滑动窗口内的时间反事实子图搜索。整体流水线以预训练 TGNN、时序图、目标节点和少量超参数为输入，依次完成候选池构建、多因素影响评分、贪婪选择与验证、连通性诱导及子图输出，并可进一步生成动态贝叶斯网络摘要以支持交互式查询。

### 输入与输出
- **输入**：预训练的 TGNN 模型 $M$、历史时序图 $\mathcal{G}_t$、目标节点集 $V_T$、时间窗口大小 $\delta$、邻域搜索深度 $L$、解释预算 $k$ 以及时间衰减率 $\lambda$。
- **输出**：对每个窗口内的每一目标节点，输出一个解释性子图 $G_\epsilon=(V_\epsilon, E_\epsilon)$，其中 $V_\epsilon = V_s \cup V_c$（$V_s$ 为解释节点集，$V_c$ 为维持 $\delta$-可达的连接节点集）；可选地，生成动态贝叶斯网络结构及其条件概率表，用于“what‑if”推理。

### 核心模块与数据流（参见 Figure 2）

1. **滑动窗口构建**（Algorithm TemGX 行 2–3）  
   在连续时间图上以长度 $\delta$ 滑动，将全局时序依赖分解为局部可操作的窗口 $\mathcal{G}_W$，保证解释的上下文连贯性。

2. **候选池生成**（行 4–5）  
   对每个目标节点 $v$，在 $\mathcal{G}_W$ 内抽取其 $L$-跳时序邻居，形成候选集 $C$。这一步界定了后续影响评分的范围，并通过 $L$ 折中解释覆盖度与计算复杂度。

3. **时序影响力计算**（Section 3）  
   每个候选节点 $v_s$ 对目标 $v$ 的影响力得分 $\Phi(v_s, v)$ 由三个互补量度合成：
   - **ICM 时间影响力**：计算移除与 $v_s$ 相连的时间边前后 TGNN 输出概率的变化，并沿时间路径递归聚合（影响概率 $p_e$ 的级联乘积），刻画直接与间接因果效用。
   - **时间电阻距离**：利用快照图拉普拉斯伪逆在嵌入空间中度量候选节点与目标节点之间的结构/语义距离，反映拓扑相似性。
   - **指数时间衰减**：赋予近期交互更大的权重，使模型贴合动态网络的记忆衰减特性。
   三项通过单调递减函数 $g(\cdot)$ 调制后求和，形成统一的 $\Phi$ 得分（见公式 6）。该得分是后续贪心选择的单一目标函数，具备单调次模性质。

4. **贪婪选择与反事实验证**（行 7–9）  
   按 $\Phi$ 的边际增益贪心地选择候选节点加入解释集 $V_s$，并立即执行 **Verify** 过程：去除该节点关联的时间边，检验 TGNN 对 $v$ 的预测是否确实改变。只有满足反事实条件的节点才予保留。此验证步在 PTIME 内完成（Lemma 1），确保输出的结构是严格反事实的，而非仅凭启发式分数。

5. **替换策略**（行 10–14）  
   当 $|V_s|$ 达到预算 $k$ 后，后续候选若替换已有节点能提升总 $\Phi$，则执行交换。该机制在维持基数的同时逼近 $(1-1/e)$-近似最优（Lemma 3），无需重新访问已处理节点。

6. **解释子图构造**（行 15）  
   以最终 $V_s$ 为基础，按 $\delta$-可达性扩充连接节点集 $V_c$，保证解释节点在时间窗口内彼此连通。诱导出的时间子图 $G_\epsilon$ 即为输出解释，具备时间因果链的完整性。

7. **查询与摘要生成**（Section 3 查询；Appendix B）  
   累积的实例解释可依用户定义的时序模式匹配（如“Peel Chain”“Spindle”），亦可学习动态贝叶斯网络结构（使用 BIC 得分），实现跨时间片的概率推理——例如回答“若移除某类节点，模型输出会如何变化”等交互查询。

### 关键设计权衡与证据

- **训练无关**：直接调用预训练模型进行干扰和推断，无需额外训练解释器，避免了额外建模偏差和训练开销。
- **时间连贯性**：$\delta$-可达约束强制解释子图在时间上相邻且因果连通，克服了静态方法或独立快照解释器的时间断裂问题。
- **硬性反事实**：Verify 过程杜绝了“高分数但无因果影响”的假阳性解释，是保真度提升的根本原因之一；消融实验显示去除 ICM 组件导致保真度下降 34.2%（UCIM+TGN），证实因果影响量化的核心地位。
- **近似保证**：单向滑动窗口与贪心替换的配合保证了 $(1-1/e)$ 近似比，且整体为“一遍式”处理，窗口内复杂度与候选集大小和单次推断开销 $T_I$ 线性相关。
- **超参敏感性**：时间衰减率 $\lambda$、窗口大小 $\delta$ 和邻域深度 $L$ 需根据数据域调整（例如社交网络 $\lambda=0.1$ 而交通数据 $\lambda=0.07$），否则性能会显著下降；电阻距离近似在大规模图上可能成为瓶颈。

框架集中解决了现有 TGNN 解释方法在时间依赖性捕捉、反事实验证和可查询性三方面的缺失，但结构级子图尚未包含节点特征重要性分析，且其通用性目前绑定于编码器‑解码器架构的 TGNN 模型。

## 核心模块与公式推导

### 关键模块

TemGX 的推理流程由七个核心模块串联构成，每个模块解决解释生成中的一个子问题：

1. **滑动时间窗口构建**  
   以长度 $\delta$ 在时序图 $\mathcal{G}_t$ 上滑动，生成当前窗口内的时序子图 $G_W$，确保解释始终在局部时间上下文中进行。

2. **候选池生成**  
   在窗口内提取目标节点 $v$ 的 $L$-跳时序邻居，形成候选解释集合；同时为每个候选计算初始影响力分数，作为后续排序的基础。

3. **时序影响分数计算**  
   采用**独立级联模型（ICM）** 估计边的移除概率变化，融合**时间电阻距离（TRD）** 与**指数衰减**，计算综合影响力分数 $\Phi$。该分数同时捕获拓扑传播、嵌入空间距离和时间衰减三种信号。

4. **贪心选择与反事实验证**  
   每轮选择 $\Phi$ 最大的候选节点加入解释集；随后执行 `Verify` 过程，强制检查移除该节点集是否确实改变 TGNN 输出（即满足反事实要求）。若不满足则舍弃该节点。

5. **替换策略**  
   当解释集大小达到预算 $k$ 时，尝试替换现有节点以进一步提升边际收益，保证解的单调次模性质。

6. **解释子图构建**  
   从最终的解释节点集 $V_s$ 及其时间连接节点 $V_c$ 诱导出 $\delta$-可连通的解释子图 $G_\varepsilon$，形成紧凑、时间连贯的解释结构。

7. **查询与总结**  
   支持对解释子图的时序模式查询，并可学习动态贝叶斯网络（DBN）结构，以贝叶斯信息准则（BIC）进行概率推理与摘要（附录 B）。

### 关键公式与变量含义

以下公式建立在**反事实边**的定义之上：若移除边 $e$ 后模型对目标节点 $v$ 的预测发生变化，则 $e$ 为反事实边。解释的目标是找到一小组反事实节点，其移除能改变模型输出。

#### 边的影响概率
$$
p_{e} = \left| \Pr(\mathcal{G}_t, v) - \Pr(\mathcal{G}_t \setminus \{e\}, v) \right|
$$
- $p_e$：移除边 $e$ 后目标节点 $v$ 输出概率的绝对变化量。
- $\mathcal{G}_t$：时刻 $t$ 的完整时序图。
- $\Pr(\cdot, v)$：TGNN 解码器对节点 $v$ 的预测概率。

#### 节点递归影响力
$$
\operatorname{inf}(v_s, v, t) = 1 - \prod_{\substack{(v', v, t') \in E \\ t-\delta \leq t' \leq t}} \left(1 - p_{(v',v,t')} \cdot \operatorname{inf}(v_s, v', t')\right)
$$
- $\operatorname{inf}(v_s, v, t)$：从解释候选 $v_s$ 到目标 $v$、在时间窗口 $[t-\delta, t]$ 内的递归影响力。
- 产品项遍历所有在窗口内指向 $v$ 的时序边，并乘以递归求得的上游节点 $v'$ 的影响力。
- 该递归式基于独立级联模型（ICM），刻画影响力沿时间路径的级联传播。

#### 时间电阻距离（TRD）
$$
\operatorname{trd}(v_s, v, t') = \bigl( Z^{t'}(v_s) - Z^{t}(v) \bigr)^\top L_{t'}^{I} \bigl( Z^{t'}(v_s) - Z^{t}(v) \bigr)
$$
- $Z^{t}(v)$：TGNN 编码器在时刻 $t$ 输出的节点嵌入向量。
- $L_{t'}^{I}$：时刻 $t'$ 的快照图拉普拉斯矩阵的伪逆。
- TRD 量化解释节点 $v_s$ 与目标 $v$ 在嵌入空间中的“电阻距离”，捕捉结构和语义的相似性：距离越小，两者在嵌入空间中越接近。

#### 时间窗影响力聚合 $\Phi$
$$
\Phi(V_s, v) = \frac{1}{\delta} \sum_{v_s \in V_s} \sum_{t'=t-\delta+1}^{t-1} \operatorname{inf}(v_s, v, t') \; g\!\left(\operatorname{trd}(v_s, v, t')\right) \; e^{-\lambda (t - t')}
$$
- $\Phi(V_s, v)$：解释节点集 $V_s$ 对目标 $v$ 的综合时序影响力得分。
- $\delta$：滑动窗口长度，用于归一化。
- $g(\cdot)$：针对 TRD 的单调递减函数（原文中实现为取负指数或倒数映射），使嵌入距离小的节点获得更高权重。
- $\lambda$：时间衰减率；$e^{-\lambda(t-t')}$ 赋予较近时间步更大的贡献。

#### 优化目标与近似保证
解释节点集 $V_s$ 的优化目标为
$$
V_s^{*} = \arg\max_{|V_s| \leq k} \sum_{v \in V_T} \sum_{v_s \in V_s} \Phi(V_s, v)
$$
即在基数约束 $k$ 下最大化所有目标节点 $V_T$ 的总影响力。TemGX 的贪心选择配合替换策略能保证此单调次模优化问题的 $(1-1/e)$ 近似比（Lemma 3）：
$$
\Phi(V_s, v) \geq \left(1 - \frac{1}{e}\right) \Phi(V_s^{O}, v)
$$
其中 $V_s^{O}$ 为最优解释集。该理论保障了算法输出解释的高质量。

> **理论性质补充**：验证给定节点集是否构成反事实解释是多项式时间可解的（Lemma 1），但解释生成问题本身是 NP‑hard 的（Lemma 2），这也是采用贪心近似算法的根本原因。

#### 辅助公式

- **BIC 得分**（用于 DBN 摘要学习）  
  $$
  \psi(\mathcal{P}, \eta.S) = \mathrm{LL}(\eta.S \mid \mathcal{P}) - \frac{|\mathcal{P}|}{2} \log |\eta.S|
  $$
  其中 $\mathcal{P}$ 为 DBN 结构，$\eta.S$ 为解释子图样本集，$\mathrm{LL}$ 为对数似然。

- **翻转率**（附录 K 验证指标）  
  $$
  \text{flip-rate} = \frac{|\{v_t \in V_T : M(G_t \setminus G_\varepsilon, v_t) \neq y_{\text{pred}}\}|}{|V_T|}
  $$
  直接度量移除解释子图后预测发生改变的节点比例。

## 实验与分析

### 主结果
TemGX 在链接预测、时空回归与分类三类任务上均表现出显著优势，在保持高解释保真度的同时大幅缩减运行时间。  
- **链接预测（Table 1）**：在 UCIM+TGN 上，TemGX 的保真度达到 0.468，相较最优基线 TempME（0.219）提升 113%，AUFSC 从 0.218 升至 0.475；单次解释仅需 8.2 s，约为 TempME（88.4 s）的十分之一。在 Wiki+TGAT 上，保真度仍保持 0.335（TempME 0.154）。TemGX 是唯一在所有“数据集‑主干”组合中都取得最高保真度和 AUFSC 的方法。  
- **时空回归（Table 2）**：在 METR‑LA+STGCN 上，TemGX 相对 TGVex 将保真度从 0.276 提升至 0.471，AUFSC 从 0.273 提升至 0.478。类似优势在 PEMS‑BAY 上复现，表明整合 TRD 与指数衰减对捕捉交通时序依赖至关重要。  
- **分类（Elliptic++）**：TemGX 取得了 0.358 的保真度（Table 8 上下文），但因缺乏统一基线对比，其相对优势仍需额外验证。

总体上，TemGX 的无训练反事实框架同时实现了更高解释性和更低计算成本，其核心驱动来自统一的时序影响力评分与严格的反事实验证。

### 消融研究
为量化各组件的贡献，分别在 UCIM+TGN 和 METR‑LA+STGCN 上开展消融（Table 3，Table 4）。  
- **ICM 影响传播** 是解释性能的首要瓶颈：移除 ICM 后，UCIM+TGN 上的保真度从 0.468 骤降至 0.308（－34.2%），METR‑LA 下降 15.7%。这表明独立级联模型对捕捉动态连锁效应不可或缺。  
- **时间衰减与 TRD** 发挥重要但相对次要的作用：去除时间衰减造成 UCIM 保真度下降 14.5%，METR‑LA 下降 16.6%；去除 TRD 分别下降 17.1% 和 14.4%。二者从动态演化与结构距离两个维度互补支撑解释精度。  

参数敏感性分析进一步揭示（Figure 6，Figure 7）：  
- 解释大小 k 增大持续提升保真度，但 k≥30 后收益趋缓，说明紧凑解释已能捕获关键信息。  
- 时间衰减率 λ 的最优值因数据域而异——社交网络（UCIM）为 0.1，交通数据（METR‑LA）为 0.07——若跨域错误迁移将明显损害保真度。  
- 滑动窗口大小 δ 的敏感性（Figure 10）表明，过小或过大的窗口均降低保真度，存在域相关最优区间。

![[assets/figures/papers/iclr26_0013_NqtYz3A8tQ_Training-free_Counterfactual_Explanation_for_Tem/figures/012_Figure_6.jpg]]
*Figure 6: Ablation results on UCIM+TGN. (a) compares component settings, (b) studies the impact of sparsity bound k, (c) evaluates the influence of the L-hop temporal neighborhood, and (d) analyzes temporal decay rate λ sensitivity*

![[assets/figures/papers/iclr26_0013_NqtYz3A8tQ_Training-free_Counterfactual_Explanation_for_Tem/figures/017_Figure_7.jpg]]
*Figure 7: Ablation results on METR-LA+STGCN. (a) compares component settings, (b) studies the impact of sparsity bound k, (c) evaluates the influence of the L-hop temporal neighborhood, and (d) analyzes temporal decay rate λ sensitivity for traffic regression*

### 失败模式与局限性
尽管 TemGX 表现突出，仍存在以下失效或受限场景：  
1. **超参数域敏感**：λ 和 δ 需根据领域知识调优，否则保真度可能大幅下滑。例如，若将交通域 λ=0.07 直接用于社交网络，会导致保真度折损（Figure 6d vs Figure 7d）。缺乏自动选择机制限制了其“即插即用”能力。  
2. **大规模图可扩展瓶颈**：可扩展性测试（Figure 11）显示，运行时间随解释 k 或目标节点数 |V_T| 呈近似对数‑线性增长。TRD 的拉普拉斯伪逆计算在超大规模图上可能仍成为性能短板，阻碍实时流式分析。  
3. **解释粒度限于结构**：TemGX 仅输出时序子图，未分解节点特征对决策的贡献。在需要特征级归因的任务中，用户可能认为解释不够精细。  
4. **泛化性未经验证**：方法专门围绕消息传递类的 TGNN（TGN, TGAT, STGCN, DCRNN）设计，对其他类时序图模型（如基于随机游走的方法）的有效性未知。  

此外，分类任务（Elliptic++）上尚缺乏直接基线对比，无法定量衡量 TemGX 的绝对增益，令结论的完备性受限。

### 重要图表结论
- **Table 1**：定量确认 TemGX 在链接预测上全面领先，相比 TempME 保真度最大提升 113%，且时间开销仅为其 1/10 左右。  
- **Figure 4（保真度‑稀疏度曲线）**：在同等稀疏度下，TemGX 的保真度始终高于其他方法，说明其解释子图的信息密度更高。  
- **Table 3 & Table 4**：消融指明 ICM 是解释力的最大来源（－34.2%），时间衰减与 TRD 各贡献约 14‑17% 的保真度，三者协同构成核心评分公式。  
- **Figure 6d & Figure 7d**：强调 λ 的域依赖性，λ=0.1（社交）与 λ=0.07（交通）的错配将造成明显保真度下降，提示部署时须针对领域校准。  
- **Figure 5 & Table 5, Table 6**：定性展示 TemGX 能重建比特币洗钱模式（Peel Chain／Spindle）和多阶段网络攻击链，生成的 δ‑可达子图时间连贯，与真实事件序列高度吻合；相比之下，基线（如 TempME）产生的子图常出现时间不连续或碎片化（Table 7）。  
- **Figure 8**：验证 TemGX 的查询能力——用户可通过时序模式匹配或动态贝叶斯网络推理进行“what‑if”分析，使解释从静态子图升级为可交互的推理工具。  

综上，TemGX 通过反事实验证与多尺度时序影响力聚合，在保真度、效率和解释连贯性上显著超越现有方法，但其超参数域敏感性和大规模效率问题仍是未来优化的主要方向。

### 补充图表

![[assets/figures/papers/iclr26_0013_NqtYz3A8tQ_Training-free_Counterfactual_Explanation_for_Tem/figures/003_Table_1.jpg]]
*Table 1: AUFSC, Fidelity, and Runtime (seconds) of generating one explanation on each dataset/backbone (mean ± std)*

![[assets/figures/papers/iclr26_0013_NqtYz3A8tQ_Training-free_Counterfactual_Explanation_for_Tem/figures/008_Table_3.jpg]]
*Table 3: Component ablation on UCIM+TGN. Fidelity is reported at the highest sparsity level*

![[assets/figures/papers/iclr26_0013_NqtYz3A8tQ_Training-free_Counterfactual_Explanation_for_Tem/figures/013_Table_4.jpg]]
*Table 4: Ablation study on METR-LA+STGCN. Fidelity is reported at the highest sparsity level*

## 方法谱系与知识库定位

### 在时序图解释生态中的定位  
现有方法可按设计倾向分为三条线路：① **静态解释器的时序拼接**（TGVex）将每个快照视为独立静态图，丢失跨时间传播信号；② **基于信息瓶颈或局部时间模式的解释**（TGNNExplainer 采用导航者-探索者框架，TempME 利用时间模体）虽开始关注时间因素，但缺乏严格反事实约束，无法保证移除解释结构必然改变模型输出；③ **可训练的反事实解释**（CoDy）通过蒙特卡洛树搜索寻找最小反事实边集，却依赖额外训练且可扩展性受限。TemGX 首次将**无训练、反事实强制、多机制时间影响力建模与交互查询**统一于一个框架，填补了“训练无关的严格反事实时序解释”这一空白。其在解释结构与粒度、时间依赖性建模、反事实验证需求、训练开销和查询能力五个维度上对现有基线形成系统改进（见表 1、Table 3-4 的消融验证）。

### 核心改进的因果机制  
TemGX 相对于基线方法的优势并非来自单一模块的叠加，而是源于一套因果一致的解决方案（详见 Section 3 定义与 Section 4 算法）：

- **解释结构与时间连贯性**：基线通常输出边级或静态子图，而 TemGX 在滑动窗口内构造由解释节点 $V_s$ 和连接节点 $V_c$ 组成的 δ‑可达时序子图（Section 3 explanatory temporal subgraph definition），强制时间路径的连续性（见 Table 7 定性对比）。
- **时间依赖性多机制融合**：TempME 仅利用模体，TGVex 无时间依赖，TemGX 则集成**独立级联模型（ICM）**模拟影响传播、**时间电阻距离（TRD）**捕捉嵌入空间的结构/语义距离，以及**指数衰减**控制远近期影响的权重（时间影响力聚合公式 $\Phi(V_s, v)$ 见 Section 3）。消融实验显示，在 UCIM+TGN 上移除 ICM 导致保真度下降 34.2%，是影响最大的组件（Table 3）。
- **严格反事实验证**：其他方法无验证或仅启发式处理，TemGX 将对每个候选节点执行 Verify 过程（Section 4），确保“移除解释结构后模型预测必须改变”（反事实边定义见 Section 3）。
- **训练无关与查询能力**：TemGX 不训练额外模型，直接利用预训练 TGNN 推理计算影响力；且支持时序模式查询与动态贝叶斯网络摘要（Appendix B），实现“what‑if”推理（Figure 8）。

### 适用边界与敏感条件  
TemGX 设计适用于**已训练的 TGNN 编码器‑解码器架构**（如 TGN、TGAT、STGCN、DCRNN）在实例级解释上的任务，覆盖链接预测、回归和分类三种典型设置（Table 1 及 Table 8）。其必要条件是输入为离散快照序列的时间图，且需足够历史长度以容纳滑动窗口（δ 的选择可参照 Table 2 数据集统计）。解释粒度定位在**子图/节点层级**，不提供节点特征的重要性分解。  

方法对超参数敏感，构成一个实际约束：窗口大小 δ、时间衰减率 λ、L‑跳邻域范围和解释预算 k 均需根据数据域手动调整。例如，消融显示 UCIM 社交网络最优 λ=0.1，而 METR‑LA 交通数据最优 λ=0.07（Figure 6(d), 7(d)）；解释大小 k 从 5 增至 50，保真度在 UCIM+TGN 上从 0.325 升至 0.468（Figure 6(b)）。若参数选择不当，性能会显著退化。此外，TRD 依赖快照拉普拉斯伪逆的计算，虽经贪心单遍扫描实现近似线性时间（$O(|N_L(v)| T_I)$ 每轮选择），但在大规模稠密图上仍可能成为速度瓶颈（Figure 11 仅展示有限规模下的可扩展性，仍需人工验证超大规模情形）。模型范畴上，TemGX 基于节点嵌入的时间图神经网络，未在其他类型动态模型（如随机游走、时序知识图谱）上验证。

### 局限性  
- **超参数可选性依赖先验知识**：δ、λ、L、k 无自动选择机制，消融中组件移除的最大性能降幅达 34.2%（ICM），说明错误配置会严重损害解释质量。  
- **计算瓶颈未彻底消除**：TRD 的反向传播虽实现单次扫描，但窗口内逆矩阵运算在节点数或密度增大时可能成为限制因素。  
- **模型泛化边界明确但未经验证**：方法专门针对基于嵌入的 TGNN，对异构图、动态知识图谱或非图模型的解释能力未知。  
- **解释层次欠缺特征归因**：当前只输出时间子图结构，不能反映节点特征如何驱动决策，对于需要细粒度归因的用户而言解释深度不足。

### 开放问题  
1. **面向实时流与大规模分布式系统的优化**：TemGX 目前设计为离线批处理，如何进一步降低单窗开销使之适应流式数据与分布式动态网络仍需探索。  
2. **跨模型与跨图类型扩展**：框架能否推广到异构图、时序知识图谱或其他非 TGNN 的时序预测模型（如时序随机游走模型），是拓宽其解释覆盖面的关键。  
3. **超参数自适应机制**：研发基于数据特性（如图密度、时间相关性）的自动窗口大小和衰减率选择策略，降低对专家经验的依赖。  
4. **特征级解释的融合**：在现有反事实子图解释之上，是否可自然地嵌入节点特征重要性（如通过特征掩码的反事实操作），以提供更完整的归因视图。

## 原文 PDF

![[paperPDFs/ICLR_2026/Training_free_Counterfactual_Explanation_for_Temporal_Graph_Model_Inference.pdf]]
