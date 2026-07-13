---
title: "HARP: Hallucination Detection via Reasoning Subspace Projection"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/HARP_Hallucination_Detection_via_Reasoning_Subspace_Projection.pdf
project_link: null
code_link: null
aliases:
- HHDRSP
- HARP
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将隐藏状态投影到推理子空间（通过SVD分解Unembedding层获得的基向量）提取紧凑的推理特征，可实现高精度、单次采样的幻觉检测。"
primary_logic: "LLM隐藏状态空间可分解为语义子空间与推理子空间的直和；Unembedding层的参数矩阵的SVD能够分离这两个子空间的基向量；将隐藏状态投影到推理子空间基向量上可得到维度仅约5%、噪声低、富含推理信息的特征，从而高效检测幻觉。"
claims:
- "HARP在TriviaQA上AUROC达到92.8%，比此前最佳方法提升7.5%（绝对值）。"
- "消融实验显示，移除推理子空间投影（HARP w/o）导致AUROC从84.0骤降至62.9（NQ Open），随机投影同样显著损害性能。"
- "推理子空间维度取256（约占隐藏状态维度的5%）时检测AUROC最高。"
- "Reasoning Patch实验证明，仅将隐藏状态中的推理子空间成分替换为正确CoT的对应成分，就能使模型在没有显式CoT提示下生成正确的推理步骤。"
---

# HARP: Hallucination Detection via Reasoning Subspace Projection

> [!tip] 核心洞察
> LLM隐藏状态空间可分解为语义子空间与推理子空间的直和；Unembedding层的参数矩阵的SVD能够分离这两个子空间的基向量；将隐藏状态投影到推理子空间基向量上可得到维度仅约5%、噪声低、富含推理信息的特征，从而高效检测幻觉。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | HARP：通过推理子空间投影的幻觉检测 |
| 英文题名 | HARP: Hallucination Detection via Reasoning Subspace Projection |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ShEDWasmDG) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | HARP (HAllucination detection via Reasoning subspace Projection) |
| Dataset | TriviaQA, TruthfulQA, NQ Open |

> [!tip] 效果简介
> - TriviaQA 上，AUROC (%) 为 92.8 (Qwen-2.5-7B-Instruct)，对比 85.3 (previous best)，变化 +7.5。
> - TruthfulQA 上，AUROC (%) 为 88.5 (LLaMA-3.1-8B)，对比 –，变化 –。
> - NQ Open 上，AUROC (%) 为 84.0 (Qwen-2.5-7B-Instruct)，对比 –，变化 –。

## 概要

大型语言模型（LLMs）的幻觉检测面临一个关键瓶颈：现有方法难以有效解耦隐藏状态中的语义信息与推理信息，导致检测精度不足且鲁棒性受限。HARP（HAllucination detection via Reasoning subspace Projection）提出一种基于推理子空间投影的检测框架，其核心洞察是：LLM的隐藏状态空间可分解为语义子空间与推理子空间的直和；通过对Unembedding层参数矩阵进行奇异值分解（SVD），可以获得两个子空间的正交基向量；将隐藏状态投影到推理子空间基上，可提取维度仅约5%、噪声低且富含推理信息的紧凑特征，从而实现高效的单次采样幻觉检测。

与依赖多次采样的基线方法（如语义熵、EigenScore等）不同，HARP仅需一次生成即可完成检测，兼具高准确性与高效率。在Qwen‑2.5‑7B‑Instruct和LLaMA‑3.1‑8B模型上，HARP在TriviaQA数据集的AUROC达到92.8%，较此前最佳方法绝对提升7.5个百分点；在TruthfulQA和NQ Open上亦取得了显著优势。消融实验表明，完全移除推理子空间投影后，AUROC从84.0骤降至62.9，随机投影替代同样严重损害性能，证实了推理子空间特征的决定性作用。此外，仅使用约5%的原始隐藏维度（256维）即可获得最优检测效果。

论文还通过“推理补丁”（Reasoning Patch）实验揭示了推理子空间的因果作用：仅替换隐藏状态中的推理子空间成分，即可引导模型在无显式思维链提示下生成正确的推理步骤，为幻觉缓解提供了新途径。

大语言模型（LLM）在生成回答时经常输出与事实相冲突的幻觉，严重制约其在可信场景下的部署。针对事实性幻觉的可靠检测已成为构建安全应用的核心需求。当前检测方法可大致分为**多次采样**和**单次采样**两类：多次采样方法（如语义熵、EigenScore、Lexical Similarity等）通过收集多条生成结果的统计量来估计模型不确定性，虽能提升精度，却以数倍甚至数十倍的计算开销为代价；单次采样方法（如Perplexity、HaloScope、LN-Entropy）仅需要一次前向传播，效率优势明显，但精度普遍有限，因为单次输出分布或原始隐藏状态中语义信息占主导，真正指示推理错误的信号微弱且易被噪声淹没。

现有方法的根本瓶颈在于**无法有效解耦隐藏状态中的语义信息与推理信息**。人类在推理与表达之间存在天然的解耦，能够反思和修正推理过程；而LLM中，语义信息（“说什么”）与推理信息（“如何得出”）在隐藏状态空间内高度交织。当检测器直接使用原始隐藏状态或基于其派生的启发式统计量时，语义变化往往会掩盖推理错误的微弱线索，导致检测精度不足且鲁棒性差。例如，消融实验表明，若完全移除对推理信息子空间的利用，检测性能会断崖式下降（在NQ Open上，AUROC从84.0骤降至62.9），而随机投影同样严重损害性能，这强有力地说明显式分离推理信息是突破当前瓶颈的关键。

核心洞察在于：LLM的隐藏状态空间可以分解为语义子空间和推理子空间的直和（$\mathcal{H}_l = \mathcal{S}_{\text{Semantic}} \oplus \mathcal{S}_{\text{Reasoning}}$），且Unembedding层（词表映射矩阵）主要与语义子空间交互（$W_{\text{unemb}} \cdot \mathcal{S}_{\text{Semantic}} \approx W_{\text{unemb}} \cdot \mathcal{H}_l$），对推理子空间几乎无贡献（$W_{\text{unemb}} \cdot \mathcal{S}_{\text{Reasoning}} \approx 0$）。因此，通过对Unembedding参数矩阵进行奇异值分解，可获得分别张成语义子空间和推理子空间的正交基向量。将隐藏状态投影到推理子空间基上，即可提取维度仅约占原始状态5%的紧凑推理特征，该特征信噪比高、几乎不受语义干扰，从而为高效检测事实性幻觉提供了理想的特征表示。

本文提出**HARP（推理子空间投影幻觉检测）**，正是基于上述假设，将单次采样下的幻觉检测转化为一个低维推理特征的监督学习问题：首先利用Unembedding矩阵的SVD构造推理子空间基，然后将每一层的隐藏状态投影至该子空间得到低维投影向量，最后训练一个轻量的MLP检测器输出令牌级幻觉分数。该框架的动机在于同时实现三个目标：（1）**高精度**——通过聚焦于推理信息，检测器能够捕捉传统方法难以感知的推理错误；（2）**高效率**——仅需单次采样，且输入维度远小于原始隐藏状态维度；（3）**强泛化**——推理子空间的构造仅依赖模型参数，不依赖于特定数据集分布，具有跨任务迁移的潜力。后续实验在多模型、多数据集上验证了上述动机的有效性，并展现出相较于先前最优方法的大幅提升。

## 核心方法与创新机理

HARP 的核心创新在于从理论上揭示了 LLM 隐藏状态空间的**语义-推理可分离性**，并将这一性质转化为实际可用的幻觉检测方案。传统方法（无论是单次采样的困惑度、香农熵，还是多次采样的语义熵、特征得分等）都无法有效解耦隐藏状态中混杂的语义信息与推理信息，导致检测对语义表面相似性过拟合、鲁棒性差。HARP 通过**对 Unembedding 参数矩阵进行 SVD 低秩近似**，无监督地构造出语义子空间与推理子空间的标准正交基，从而将每一层的隐藏状态投影到推理子空间上，提取维度极低（约原始维度的 5%）、噪声稀疏的推理特征，仅用单次采样即可实现高精度幻觉检测。这一特征提取范式的改变直接带来了检测精度的大幅提升和推断效率的显著优化，成为区别于所有基线方法的根本瓶颈突破点。

### 相对基线的关键 changed slots

**特征提取**  
基线方法（`Perplexity`、`LN-Entropy`、`Semantic Entropy` 等）依赖启发式统计量或全维隐藏状态，难以避免语义成分的干扰。HARP 将特征提取环节替换为**推理子空间投影**：对第 $l$ 层隐藏状态 $h_l$，投影向量 $\text{proj}_R(h_l) = V_R^\top \cdot h_l$ 被用作检测输入（Eq.15–16）。该投影去除了主导词表预测的语义信息，仅保留对预测贡献可忽略、但与推理过程高度相关的成分，使得特征真正聚焦于“模型的推理是否正确”，而非表面语义流畅度。

**子空间构建**  
基线方法未对隐藏状态进行显式的语义‑推理分离（或依赖有监督探针）。HARP 利用 Unembedding 矩阵 $W_{\text{unemb}}$ 的 SVD 分解 $W_{\text{unemb}} = U \Sigma V^\top$，基于 Eckart–Young–Mirsky 定理选取前 $k$ 个右奇异向量作为语义子空间基 $V_S$，剩余 $d-k$ 个向量构成推理子空间基 $V_R$（Eq.7–14）。该构建完全无监督，仅需分解一次 LM 头矩阵，计算开销极小（例如 Qwen2.5‑72B‑Instruct 的 SVD 仅需约 9.8 秒，Table 6）。更重要的是，它从理论上保证了 **$W_{\text{unemb}} \cdot \mathcal{S}_{\text{Reasoning}} \approx 0$**（Eq.6），即推理子空间成分对词表预测不产生影响，因而投影操作不会破坏模型的生成质量（Figure 5a 显示即使去除推理子空间，token 排序也基本不变）。

**检测器输入维度**  
基线检测器通常以全维隐藏状态（Qwen‑2.5‑7B 为 3584 维）为输入。HARP 将输入压缩至推理子空间的低维投影，最优维度仅 256（Figure 5b），参数效率和计算效率均大幅提升。实际使用的幻觉检测器为两层 MLP（隐藏维度 1024，ReLU 激活），在整个回答中取 token 级分数的最大值作为最终幻觉得分（Eq.16），结构轻量却保持了极高的检测精度。

### 支撑创新的关键实证

- **主性能大幅领先**：在 TriviaQA 上 AUROC 达 92.8%，较此前最优方法高出 7.5%（绝对值）；在 TruthfulQA、NQ Open 等数据集上同样一致超越所有基线（Table 1），且均为单次采样。
- **投影策略的因果必要性**：完全移除推理子空间投影（HARP w/o）使 AUROC 从 84.0 骤降至 62.9（NQ Open, Qwen‑2.5‑7B），随机投影替代学习到的子空间基也导致性能显著恶化（Table 3），证明 SVD 导出的特定基向量的不可替代性。
- **维度‑性能峰形关系**：推理子空间维度在 256 时 AUROC 达到最高（Figure 5b），进一步增加维度带来的增益有限甚至下降，验证了“低维推理流形”的假设。
- **因果操纵验证**：Reasoning Patch 实验（Figure 9‑11）显示，仅将隐藏状态中的推理子空间成分替换为正确链式思维（CoT）对应成分，模型即可在没有显式提示的情况下生成正确的推理步骤，为推理子空间的功能因果性提供了直接证据。

上述 changed slots 共同构成了 HARP 的创新能力：将幻觉检测从“语义表面统计”深化到“推理内在状态感知”，同时保持单次采样的高效性。当前方法主要针对**事实性幻觉**，其子空间构建依赖标准的 Unembedding 层，对于逻辑错误等类型的失效模式仍需进一步探索。

![[assets/figures/papers/iclr26_0014_ShEDWasmDG_HARP_Hallucination_Detection_via_Reasoning_Subsp/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the proposed HARP framework for hallucination detection. HARP separates the reasoning information $h _ { l , \mathrm { R e a s o n i n g } }$ from the hidden state $h _ { l }$ to compute token-level hallucination scores, with the maximum score taken as the hallucination score of the entire response*

![[assets/figures/papers/iclr26_0014_ShEDWasmDG_HARP_Hallucination_Detection_via_Reasoning_Subsp/figures/004_Figure_4.jpg]]
*Figure 4: (a) Singular value distributions of W _ { u n e m b } after SVD, with hidden state dimensions of 3584 for Qwen-2.5-7B-Instruct and 4096 for LLaMA-3.1-8B. (b) Projections of hidden states onto the basis vectors of the semantic and reasoning subspaces across layers, where the first row shows the first three layers and the second row shows the last three layers. Further details are provided in Appendix B*

HARP 的幻觉检测 pipeline 围绕“推理子空间投影”构建，将隐藏状态中的语义与推理信息解耦，并仅使用低维推理特征完成检测。其核心因果机制是：LLM 的隐藏状态空间可分解为语义子空间和推理子空间的直和（$$\mathcal{H}_l = \mathcal{S}_{\mathrm{Semantic}} \oplus \mathcal{S}_{\mathrm{Reasoning}}$$, Eq.3），其中语义子空间主导 Unembedding 输出，推理子空间对 token 预测几乎无贡献（$$W_{\mathrm{unemb}} \cdot \mathcal{S}_{\mathrm{Reasoning}} \approx 0$$, Eq.6）。因此，通过 SVD 分解 Unembedding 参数矩阵即可获得两个子空间的正交基，将隐藏状态投影到推理子空间基上得到的低维向量（维度约原始隐藏状态的 5%）仅含推理信息，噪声低，可作为高效检测特征。

整体流程如图 1 所示，分为三个阶段：
1. **子空间构建**：对 Unembedding 参数矩阵 $$W_{\mathrm{unemb}}$$ 进行 SVD（$$W_{\mathrm{unemb}} = U \Sigma V^\top$$, Eq.7），得到右奇异向量 $$V = [v_1,\dots,v_d]$$。利用低秩近似（Eckart–Young–Mirsky 定理, Eq.13‑14）确定最优秩 $$k$$，取前 $$k$$ 个向量张成语义子空间基 $$V_S$$，后 $$d-k$$ 个向量张成推理子空间基 $$V_R$$（Eq.9‑10）。图 4 展示了奇异值分布及隐藏状态在两个子空间上的投影能量差异，验证了分离的有效性。
2. **特征投影**：对生成回答中每个 token 的隐藏状态 $$h_l$$（取自模型某一高层），计算其在推理子空间上的投影 $$\mathrm{proj}_R(h_l) = V_R^\top h_l$$（Eq.15）。该低维投影仅保留推理相关信息，过滤了语义噪声；消融实验表明，去掉该投影（HARP w/o）会使 AUROC 从 84.0 骤降至 62.9（Qwen‑2.5‑7B‑Instruct 在 NQ Open 上，Table 3），而随机投影替代同样导致性能崩溃。
3. **幻觉检测**：投影向量输入一个两层 MLP（隐藏维度 1024，ReLU 激活），输出 token 级幻觉分数。整个 QA 对的幻觉分数取所有 token 分值的最大值：$$g_{\theta}(y|x) = \max_{1 \leq i \leq n} g_{\theta}(\mathrm{proj}_R(h_l^{(i)}))$$（Eq.16）。最终分数用于二分类判定回答是否含幻觉，仅需单次采样，无需多次生成，因而在精度与效率上均显著优于需要多次采样的基线方法（Table 1）。

训练阶段，使用集束搜索对每个问题生成 10 条候选答案，根据与参考答案的相似度标注幻觉标签，构造正负样本训练 MLP 检测器；推理时仅需一次前向传播即可输出结果。推理子空间维度取 256 时检测 AUROC 最高（Figure 5b），此时占用维度仅为原始隐藏状态的约 5%，且对语义信息完整保留，不影响 token 预测（Figure 5a）。

> **输入输出流总结**：输入为问题 $$x$$ 与模型生成的完整回答 $$y$$；步骤包括 ① 提取 $$y$$ 中各 token 的隐藏状态，② 利用预计算的 $$V_R$$ 将各隐藏状态投影到推理子空间，③ 将投影向量逐 token 输入 MLP 得到分数，④ 取最大值作为最终幻觉分数。

HARP 的核心设计建立在两条关键假设之上：（1）LLM 的隐藏状态空间可以分解为语义子空间与推理子空间的直和（Eq. 3）；（2）Unembedding 层（LM Head）几乎只传递语义信息，推理子空间的成分对 token 预测的贡献近似为零（Eq. 5‑6）。基于这两个假设，所有模块都围绕**推理子空间的构造与投影**展开，从而将高维、含噪的隐藏状态压缩为紧凑且富含推理信息的特征向量，再送入一个轻量检测器。

### 关键模块

- **Unembedding SVD 分解模块**  
  对 Unembedding 参数矩阵 $W_{\mathrm{unemb}} \in \mathbb{R}^{d_{\mathrm{vocab}} \times d}$ 执行奇异值分解（SVD），获得右奇异向量矩阵 $V = [v_1, …, v_d]$。前 $k$ 个对应大奇异值的方向张成语义子空间 $\mathcal{S}_{\mathrm{Semantic}}$，余下的 $(d-k)$ 个方向张成推理子空间 $\mathcal{S}_{\mathrm{Reasoning}}$（Eq. 9‑10）。在实际实现中，由于奇异值不会严格为零，需采用 Eckart‑Young‑Mirsky 定理对 $W_{\mathrm{unemb}}$ 进行秩‑$k$ 最优近似（Eq. 13），并确保近似误差远小于保留谱能量（Eq. 14）。该模块仅依赖 Unembedding 层的静态参数，**无需任何训练或微调**。

- **推理子空间投影模块**  
  对第 $l$ 层解码器的隐藏状态 $h_l$，通过左乘推理子空间基 $V_R$ 得到低维投影：
  $$\mathrm{proj}_R(h_l) = V_R^{\top} \; h_l \quad \text{(Eq. 15)}$$
  该投影仅保留隐藏状态中与推理子空间对齐的分量，有效剥离语义主导的维度，同时将维度从原始的 3584/4096 降至约 256（约占 5%），极大降低了后续检测器的输入噪声与复杂度。

- **幻觉检测器（MLP）**  
  接收每个 token 的投影向量，经过一个两层 MLP（隐藏维 1024，ReLU 激活）输出 token 级幻觉分数；整个回答的分数取所有 token 分数的最大值：
  $$g_{\theta}(y|x) = \max_{1 \le i \le n} \; g_{\theta}\!\left( \mathrm{proj}_R(h_l^{(i)}) \right) \quad \text{(Eq. 16)}$$
  采用 max‑pooling 的原因在于：幻觉往往由个别关键 token 的不可靠推理所触发，全局平均会稀释此类异常信号。检测器的训练仅需要构造好的幻觉/非幻觉标注数据，无需调整 LLM 主体参数。

- **训练数据构造模块（集束搜索采样）**  
  训练阶段对每个问题使用一次集束搜索（beam search）生成 10 条候选答案，并根据答案是否与标准答案一致自动标注幻觉状态（Eq. 1‑2）。该模块保证了大规模、低成本的训练数据获取，避免人工标注，并与推理子空间投影过程解耦。

### 核心公式与变量含义

**空间分解与假设**

- 隐藏状态空间分解：
  $$\mathcal{H}_l = \mathcal{S}_{\mathrm{Semantic}} \oplus \mathcal{S}_{\mathrm{Reasoning}} \tag{Eq. 3}$$
  $\mathcal{H}_l$：第 $l$ 层隐藏状态所处的空间。该式断言该空间可正交分解为语义和推理两个子空间的直和。

- Unembedding 相互作用：
  $$W_{\mathrm{unemb}} \cdot \mathcal{S}_{\mathrm{Semantic}} \approx W_{\mathrm{unemb}} \cdot \mathcal{H}_l, \qquad W_{\mathrm{unemb}} \cdot \mathcal{S}_{\mathrm{Reasoning}} \approx 0 \tag{Eq. 5‑6}$$
  表明 Unembedding 矩阵 $W_{\mathrm{unemb}}$ 几乎完全忽略推理子空间的分量，因此通过该层的输出 logits 无法直接观测推理信息。这一“信息瓶颈”是 HARP 强制执行子空间分离的理论基础。

**子空间构造**

- SVD 分解：
  $$W_{\mathrm{unemb}} = U \Sigma V^{\top} = \sum_{i=1}^{d} u_i \sigma_i v_i^{\top} \tag{Eq. 7}$$
  其中 $u_i \in \mathbb{R}^{d_{\mathrm{vocab}}}, \sigma_i \in \mathbb{R}, v_i \in \mathbb{R}^{d}$ 分别为左奇异向量、奇异值和右奇异向量。

- 语义与推理基：
  $$\mathcal{S}_{\mathrm{Semantic}} = \operatorname{Span}\{v_1, v_2, \dots, v_k\} \tag{Eq. 9}$$
  $$\mathcal{S}_{\mathrm{Reasoning}} = \operatorname{Span}\{v_{k+1}, v_{k+2}, \dots, v_{d}\} \tag{Eq. 10}$$
  $k$ 的选择需要在信息保留和维度压缩之间平衡：实验（Figure 5b）表明 $k=256$ 时检测 AUROC 达到峰值，此时仅保留约 5% 的维度，去掉的大部分维度对应推理信息，但保留了语义信息完整性（Figure 5a 显示即使 $k$ 很小，top token 排名几乎不变）。

- 秩‑$k$ 近似条件：
  $$W_k = \arg\min_{\mathrm{rank}(A) \le k} \|W_{\mathrm{unemb}} - A\|_F = \sum_{i=1}^{k} u_i \sigma_i v_i^{\top} \tag{Eq. 13}$$
  $$\|W_{\mathrm{unemb}} - W_k\|_F = \sqrt{\sum_{i=k+1}^{d} \sigma_i^2} \ll \sqrt{\sum_{i=1}^{k} \sigma_i^2} \tag{Eq. 14}$$
  该条件保证 $W_k$ 保留了 Unembedding 矩阵的主体作用方向，使得取下近似后仍可用于复原隐藏状态中的语义分量。

**检测的效能证据**  
消融实验（Table 3）直接验证了模块设计的必要性：  
- 完全移除推理子空间投影（“HARP w/o”）后，NQ Open 上的 AUROC 从 84.0 骤降至 62.9；  
- 用随机投影替代学习到的 $V_R$，性能同样大幅退化。  
这证实了推理子空间的信息是检测幻觉的关键信号，且该信号并非由任意低维投影可模仿。

整体而言，HARP 通过无监督的 SVD 基构造将 LLM 内部状态解耦为语义与推理两个正交空间，再以极其紧凑的推理子空间投影作为检测输入，实现了单次采样即可高精度检测幻觉的轻量框架。

## 实验与关键发现

### 主结果：单次采样的高精度幻觉检测
HARP 在所有评测基准上均以显著优势超越现有方法。对于 Qwen-2.5-7B-Instruct 模型，在 TriviaQA 上取得 92.8% 的 AUROC，相较此前最优结果（85.3%）绝对提升 7.5 个百分点；在 NQ Open 与 TruthfulQA 上分别达到 84.0% 和 88.5%（Table 1，LLaMA-3.1-8B 在 TruthfulQA 上亦为 88.5%）。更重要的是，HARP 仅需单次采样即可完成检测，而主对比基线如 Semantic Entropy、EigenScore、Lexical Similarity 等方法依赖于 5-10 次重复生成，效率与部署成本差距显著。这一结果直接验证了核心主张：通过将隐藏状态投影到推理子空间，能够以极低的特征维度和单次前向传播捕获回答是否包含幻觉的强信号。

### 消融实验：推理子空间投影的关键作用
消融结果（Table 3）表明，完全移除推理子空间投影（HARP w/o）后，检测性能剧烈退化。在 Qwen-2.5-7B-Instruct 的 NQ Open 上，AUROC 从 84.0 骤降至 62.9，降幅超过 20 个百分点；以随机投影替代学得的投影矩阵同样导致性能大幅下降，证实基向量的语义有效性对检测至关重要。进一步，控制推理子空间维度 $k$ 的分析（Figure 5b）显示，$k=256$（约占原始 3584 维状态空间的 5%）时检测 AUROC 达到最高，过大或过小的维度均使性能下降，尤其在 $k \le 64$ 时下降更为明显。这说明推理子空间维度需在信息完整性与抗噪能力之间平衡：维度不足会丢失关键推理信号，维度过度则会引入语义空间的冗余噪声。

### 维度敏感性与潜在局限
HARP 对推理子空间的维度敏感，本质上构成一种故障模式：若不在部署前通过少量验证集正确选择 $k$，检测精度可能明显低于报告值。此外，当前工作存在以下边界：①幻觉缓解实验（Table 4）仅在有限案例上进行定性检验，未报告定量的缓解成功率；②检测对象聚焦于事实冲突型幻觉（fact‑conflicting），对逻辑错误等其它类型幻觉的有效性尚未探索；③幻觉检测器的训练依赖于集束搜索采样构造的已知/未知‑正确/错误标注（Section 4.4），标注过程中的相似度阈值 $\lambda$ 以及搜索参数会间接影响训练数据分布，但在论文公开范围内未提供对该超参的敏感性分析。尽管如此，跨数据集泛化实验（Figure 7）显示，当训练集与测试集分布不同时（如 TriviaQA→NQ Open 或 TruthfulQA→TriviaQA），HARP 仍保持较高 AUROC，一定程度上缓解了过拟合担忧。

### 图表综合结论
- **Table 1** 确立了 HARP 的 state‑of‑the‑art 地位：在 Qwen‑2.5‑7B‑Instruct 和 LLaMA‑3.1‑8B 上，于四个数据集全面领先，单次采样机制使其效率优势突出。
- **Table 3** 提供了因果支持：推理子空间投影是性能的主要来源，移除或随机化该投影可使 AUROC 坍塌至随机水平。
- **Figure 5b** 给出了超参数操作的实用指南：推理子空间维度设为约 5% 的原始隐藏维度即可近乎最优。
- **Figure 7** 证明 HARP 的幻觉信号具有跨数据集迁移性，非数据集特定过拟合。
- 附录中 Reasoning Patch 实验（Figure 9‑11）从因果操纵的角度进一步强化了子空间解耦的有效性：仅将推理子空间成分替换为正确 CoT 的对应部分，就能引导模型在无显式 CoT 提示下生成正确推理步骤，为子空间的可干预性和解释性提供了有力证据。

![[assets/figures/papers/iclr26_0014_ShEDWasmDG_HARP_Hallucination_Detection_via_Reasoning_Subsp/figures/005_Table_1.jpg]]
*Table 1: Main result. Comparison of different methods on hallucination detection performance across multiple datasets. All values are AUROC percentages. “Single” indicates whether multiple samplings are required for hallucination detection*

![[assets/figures/papers/iclr26_0014_ShEDWasmDG_HARP_Hallucination_Detection_via_Reasoning_Subsp/figures/009_Table_3.jpg]]
*Table 3: Hallucination detection performance under different projection strategies*

![[assets/figures/papers/iclr26_0014_ShEDWasmDG_HARP_Hallucination_Detection_via_Reasoning_Subsp/figures/008_Figure_5.jpg]]
*Figure 5: (a) Greedy token rankings in $\mathrm { \it { l o g i t s } ^ { \prime } }$ under different reasoning subspace dimensions. (b) Effect of reasoning subspace dimension on hallucination detection performance

![[assets/figures/papers/iclr26_0014_ShEDWasmDG_HARP_Hallucination_Detection_via_Reasoning_Subsp/figures/012_Figure_7.jpg]]
*Figure 7: Cross-dataset generalization. “(s)” indicates the source dataset used for training the hallucination detector; “(t)” indicates the target dataset*

## 定位与知识库关联

### 与基线方法的关系及核心突破

现有幻觉检测方法可大致分为两类：仅需单次采样的基线（如Perplexity、HaloScope）和依赖多次采样的基线（如Semantic Entropy、EigenScore、LN-Entropy、Lexical Similarity）。其中多次采样方法虽能捕捉回答间的语义一致度，但计算成本高且在低采样次数下性能退化；单次采样方法则通常基于原始隐藏状态或启发式统计量，难以有效分离对幻觉检测至关重要的推理信息与语义信息，导致精度受限。这一瓶颈在HARP中得到根本性突破：**通过将隐藏状态投影到推理子空间上，提取紧致且低噪声的推理特征**，从而在仅需单次采样的条件下大幅提升检测性能。在TriviaQA上，HARP（基于Qwen‑2.5‑7B‑Instruct）的AUROC达到92.8%，比此前最佳方法高出7.5个百分点（绝对值）；在TruthfulQA和NQ Open等数据集上同样展现出显著的领先优势（Table 1）。

这一进步的机理可归结为三个**关键方法槽位（changed slots）**的更新：

1. **特征提取方式**——基线方法直接使用全维隐藏状态或从多答案中计算的熵、相似度等浅层统计量；HARP则将每一层的隐藏状态$h_l$投影到推理子空间的基向量上，得到维度仅为原始约5%（≈256维）的紧凑特征向量$V_R^\top \cdot h_l$（Eq.15）。该投影特征保留了令牌级的推理证据，同时滤除了语义噪声，使得检测器能更专注于与事实正确性直接相关的信号。

2. **子空间构建策略**——先前工作无显式分解语义/推理信息，或需依赖有监督探针；HARP提出对Unembedding层的参数矩阵进行SVD，利用其右奇异向量张成语义子空间（前$k$个主成分）和推理子空间（剩余成分）（Eq.7–10）。在非理想条件下，通过Eckart‑Young‑Mirsky定理取最佳秩$k$近似，保证推理子空间包含那些对直接预测贡献极微但富含内部推理过程的信息（Eq.13）。

3. **检测器输入维度**——从全维隐藏状态（Qwen‑2.5‑7B为3584维）骤降至推理子空间维度（最优约256维），使得下游幻觉检测器（一个两层MLP，隐藏维度1024）的训练和推理极度轻量，同时也缓解了过拟合风险（Figure 5b）。

消融实验（Table 3）直接验证了上述改进的因果性：若完全移除推理子空间投影（HARP w/o），NQ Open上的AUROC从84.0%暴跌至62.9%；代之以随机投影同样严重损害性能。这说明学习的子空间投影是精度核心。

### 适用边界与假设

HARP的有效性建立在以下两个核心假设之上：① LLM的隐藏状态空间可分解为语义子空间与推理子空间的直和（$\mathcal{H}_l = \mathcal{S}_{\text{Semantic}} \oplus \mathcal{S}_{\text{Reasoning}}$）；② 推理子空间可通过Unembedding矩阵的SVD（或低秩近似）被可靠分离。这两个假设在当前主流的解码器架构（Qwen‑2.5系列、LLaMA‑3.1系列）上得到了实验结果的支持，但对以下情形需保持谨慎：

- **非标准Unembedding层**：若模型修改了LM head的结构或参数化方式，SVD得到的子空间基可能不再具备原有的解耦效果，需额外适配。
- **幻觉类型的覆盖**：当前的实验设计、标注与评测主要围绕**事实冲突型（fact‑conflicting）幻觉**展开。对于逻辑错误、推理链断裂等非事实性幻觉，HARP的检测能力尚未经过系统验证，即便推理子空间理论上可能蕴含这些错误的信息，其有效性仍是开放问题。
- **数据与模型分布的泛化**：跨数据集实验（Figure 7）显示，在源域与目标域分布不一致时HARP仍能保持较高AUROC，表明其具备一定泛化性；但目前的验证集中于标准的开放域QA数据集，对于长文本、多语言或复杂对话场景的鲁棒性有待进一步检验。

此外，方法要求训练阶段通过集束搜索生成多条候选答案并标注幻觉标签，因此依赖参考标准答案；在无参考答案的开放式场景中，数据构造方式需要重新设计。

### 主要局限

1. **幻觉缓解仅定性演示**：论文在少量案例上实验了通过移除或替换推理子空间成分来缓解幻觉（如Table 4、Reasoning Patch实验），但缺乏定量化的缓解性能指标和系统性评估，目前仅停留在概念验证层面。

2. **对Unembedding层的依赖性**：子空间构建完全绑定于模型的Unembedding参数；若某模型不包含标准Softmax头（例如生成式嵌入模型），该方法无法直接复用。

3. **未覆盖非事实性幻觉**：正如适用边界中所述，逻辑错误、不一致性等更微妙的幻觉形式是否可被推理子空间捕获仍是未知数。

4. **SVD计算成本随词表与维度增长**：尽管论文提供了H100 GPU上的SVD开销（例如Qwen‑2.5‑72B‑Instruct耗时9.83秒，Table 6），但对于拥有更大词表（如多语言词汇表扩充版）或更高维度的模型，SVD的内存和计算需求可能成为部署瓶颈，且该操作目前为一次性离线步骤，在线推理不受影响。

### 开放问题与未来方向

- **非事实性幻觉的检测与缓解**：推理子空间是否蕴含逻辑错误、循环论证等推理缺陷的表示？能否通过微调或扩展子空间构建方式，使HARP框架覆盖更广阔的幻觉类型？
- **自动化推理子空间干预**：Reasoning Patch实验证明，仅替换推理子空间成分即可让模型在没有显式思维链提示下生成正确推理步骤；但当前操作需要预先获取正确的CoT推理轨迹作为监督信号，属于半自动化。如何设计无监督或自反馈的干预策略，使之成为通用的幻觉缓解工具，是下一步的重要挑战。
- **深层“解码器”机制**：实验观察到深层（如Layer‑22）在隐瞒推理信息、控制输出方面起着关键作用（Table 4），其作为一个“语义解码器”将内部推理表征转化为最终语义输出，这一机制的本质是什么？能否形式化并迁移到其他层以增强对幻觉的控制？
- **子空间构建的效率与可扩展性**：能否通过稀疏SVD、随机化SVD或增量更新方式，进一步降低大规模模型上的计算开销，同时保持子空间质量？在不重新训练检测器的情况下，子空间的动态自适应更新也是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/HARP_Hallucination_Detection_via_Reasoning_Subspace_Projection.pdf]]
