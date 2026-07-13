---
title: "Beyond Entity Correlations: Disentangling Event Causal Puzzles in Temporal Knowledge Graphs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Beyond_Entity_Correlations_Disentangling_Event_Causal_Puzzles_in_Temporal_Knowledge_Graphs.pdf
project_link: null
code_link: null
aliases:
- HHECDRLA
- BECDECPTKG
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: |
  在时序知识图谱中构建事件级结构因果模型，通过反事实检测器、工具变量引导解耦和进化正交模块分离非因果、虚假因果、静态因果与动态因果因素。
primary_logic: |
  先将TKG事件表示为主体、关系、客体和时间的事件序列，再用事件重要性与KL分布差异生成非因果掩码，用IV分数划分真实与虚假因果边，最后以Gram-Schmidt正交化和进化损失分离静态与动态因果表示并服务事件预测。
claims:
- "HEDRA首次在事件层面形式化并解耦TKG中的非因果性、虚假因果性、静态因果性和动态因果性。"
- "在ICEWS14上，HEDRA达到MRR 47.86、Hits@1 35.28、Hits@3 53.32，均高于DECRL。"
- "消融结果显示移除反事实检测器、IV引导解耦模块或进化正交模块都会降低ICEWS14性能。"
---

# Beyond Entity Correlations: Disentangling Event Causal Puzzles in Temporal Knowledge Graphs

> [!tip] 核心洞察
> 在TKG中构建事件级结构因果模型，利用事件重要性和分布差异解耦非因果性，利用工具变量解耦虚假因果性，利用正交约束分离静态与动态因果性，从而获得鲁棒的事件表示用于事件预测。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超越实体相关性：解耦时序知识图谱中的事件因果谜题 |
| 英文题名 | Beyond Entity Correlations: Disentangling Event Causal Puzzles in Temporal Knowledge Graphs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=RdoXks7VmJ) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | HEDRA (Heterogeneous Event causality Disentangling Representation learning Approach) |
| Dataset | ICEWS14 |

> [!tip] 效果简介
> - ICEWS14 上，MRR 为 47.86，对比 42.90 (DECRL)，变化 +11.56%。
> - ICEWS14 上，Hits@1 为 35.28，对比 30.49 (DECRL)，变化 +15.71%。
> - ICEWS14 上，Hits@3 为 53.32，对比 48.07 (DECRL)，变化 +10.92%。

## 概要

本文提出**HEDRA (Heterogeneous Event causality Disentangling Representation learning Approach)**，一种面向时序知识图谱（Temporal Knowledge Graph, TKG）事件预测的异质因果解耦表示学习方法。现有TKG方法仅关注实体或关系层面的相关性，忽略了事件层面固有的异质因果性——包括非因果性、虚假因果性、静态因果性和动态因果性。HEDRA首次在事件层面构建TKG结构因果模型（SCM），通过反事实检测器、工具变量（IV）引导解耦模块和进化正交模块，逐步解耦这四类因果性，从而获得鲁棒的事件表示用于事件预测。在五个真实数据集（ICEWS14、ICEWS18、WIKI、YAGO、GDELT）上，HEDRA在MRR、Hits@1、Hits@3、Hits@10上平均超过第二名5.70%、7.51%、7.21%、2.30%。



### 1 问题定义

TKG $\mathcal{G} = \{ (s, r, o, t) | s \in \mathcal{E}, r \in \mathcal{R}, o \in \mathcal{E}, t \in \mathcal{T} \}$ 是由带时间戳的事件组成的序列，每个事件表示为（主体，关系，客体，时间戳）。事件预测任务定义为：给定历史事件序列 $\mathcal{G}^{1:T-1}$，预测主体 $s$ 和客体 $o$ 之间候选关系的概率分布 $p(\hat{r} | s, o, \mathcal{G}^{1:T-1})$。

### 2 现有方法的瓶颈

现有TKG表示学习方法仅关注实体或关系层面的相关性，忽略了事件层面固有的异质因果性（非因果性、虚假因果性、静态因果性、动态因果性），且缺乏显式监督信号来区分这些因果性。具体而言：

- **非因果性**：事件之间不存在因果关系，仅因时间或空间邻近而共现。
- **虚假因果性**：事件之间因混淆变量而产生虚假关联。
- **静态因果性**：事件之间长期稳定、不随时间变化的因果关系。
- **动态因果性**：事件之间随时间演变的因果关系。

### 3 核心洞察

在TKG中构建事件级结构因果模型，利用事件重要性和分布差异解耦非因果性，利用工具变量解耦虚假因果性，利用正交约束分离静态与动态因果性，从而获得鲁棒的事件表示用于事件预测。



## 核心方法与创新机理

1. **首次在事件层面解耦TKG中的异质因果性**：提出事件级TKG结构因果模型（SCM），形式化定义非因果性、虚假因果性、静态因果性和动态因果性，并通过后门调整公式 $P(\mathcal{Y}|\operatorname{do}(\mathcal{D})) = \sum P(\mathcal{S}) \sum P(\mathcal{T}) \sum P(\mathcal{P}) \sum P(\mathcal{Y}|\mathcal{G})$ 估计动态因果性对预测的因果效应。

2. **反事实检测器**：利用事件重要性（注意力权重）和分布差异（KL散度）生成软非因果性掩码，通过对比损失拉近低非因果性对、推远高非因果性对。

3. **IV引导解耦模块**：通过工具变量分数划分真实因果与虚假因果边，通过鲁棒性损失对齐全视图与真实视图、分离虚假视图与真实视图。

4. **进化正交模块**：通过Gram-Schmidt正交化分离动态与静态因果性，通过进化损失保持动态分量的时序依赖性和静态分量的时序独立性。



HEDRA的整体框架如Figure 3所示，以时间戳 $T-1$ 为例，包含以下流水线模块：

1. **关系感知GCN**：建模实体与关系间的结构依赖。
2. **关系更新**：融合当前时间戳的实体表示和历史关系表示更新关系表示。
3. **事件表示构建**：通过MLP编码主体、关系、客体表示构建事件表示。
4. **反事实检测器**：利用事件重要性和分布差异解耦非因果性。
5. **IV引导解耦模块**：利用工具变量解耦虚假因果性。
6. **进化正交模块**：分离动态因果性与静态因果性。
7. **事件预测解码器**：使用ConvTransE进行事件预测。



### 1 事件表示构建

事件表示通过MLP融合主体、关系、客体的表示：
$$\boldsymbol{h}_{event}^t = f_{MLP}([\boldsymbol{h}_s^t; \boldsymbol{h}_r^t; \boldsymbol{h}_o^t])$$

### 2 反事实检测器

**事件重要性权重**：基于事件表示计算候选边 $i \rightarrow j$ 的归一化注意力权重：
$$e_{ij} = \mathrm{LeakyReLU}\left( a^{\top} [W_3 \boldsymbol{h}_{\mathrm{event},i}^t; W_4 \boldsymbol{h}_{\mathrm{event},j}^t] \right), \quad A_{ij} = \frac{\exp(e_{ij})}{\sum_{k \in \mathcal{N}^{\mathrm{in}}(j)} \exp(e_{kj})}$$

**分布差异（KL散度）**：衡量事件 $i$ 和 $j$ 的高斯后验分布之间的差异：
$$D_{ij} = \mathrm{KL}(q_i \parallel q_j) = \frac{1}{2} \sum_{d=1}^D \left[ \log \frac{\sigma_{j,d}^2}{\sigma_{i,d}^2} + \frac{\sigma_{i,d}^2 + (\mu_{i,d} - \mu_{j,d})^2}{\sigma_{j,d}^2} - 1 \right]$$

**非因果性掩码**：融合事件重要性和分布差异生成软掩码：
$$\boldsymbol{S} = (\alpha_{\mathrm{attn}} \cdot \mathrm{logit}(\boldsymbol{A} + \varepsilon) - \beta_{\mathrm{KL}} \cdot \boldsymbol{D}) \odot \boldsymbol{C}, \quad \boldsymbol{M}^{\mathrm{NC}} = \mathbf{1} - \sigma(\boldsymbol{S})$$

**对比损失**：根据非因果性掩码鼓励低非因果性对靠近、高非因果性对远离：
$$\mathcal{L}_{\mathrm{con}} = \frac{1}{|\mathcal{P}|} \sum_{(i,j) \in \mathcal{P}} \left[ (1 - M_{ij}^{\mathrm{NC}})(-\log \sigma(s_{ij}/\tau)) + M_{ij}^{\mathrm{NC}}(-\log(1 - \sigma(s_{ij}/\tau))) \right]$$

### 3 IV引导解耦模块

**IV分数**：为每条边计算工具变量分数：
$$\Pi_{ij} = f_{\mathrm{IV}}(\boldsymbol{h}_{\mathrm{event},i}^t, \boldsymbol{h}_{\mathrm{event},j}^t, \mathrm{logit}(A_{ij} + \varepsilon), -D_{ij})$$

**虚假因果性掩码**：选择前 $\alpha$ 比例的边作为真实因果，其余为虚假因果：
$$\theta_\alpha = \mathrm{Quantile}_\alpha(\{ \widetilde{\Pi}_{ij} : M_{ij}^{\mathrm{C}} > 0 \}), \quad \boldsymbol{M}^{\mathrm{P}} = \mathbb{I}\{ \widetilde{\Pi} \geq \theta_\alpha \mathbf{1} \}, \quad \overline{\boldsymbol{M}}^{\mathrm{P}} = \mathbf{1} - \boldsymbol{M}^{\mathrm{P}}$$

**鲁棒性损失**：对齐全视图与真实视图表示，分离虚假视图与真实视图表示：
$$\mathcal{L}_{\mathrm{rob}} = \lambda_{\mathrm{align}} \frac{1}{E} \sum_{i=1}^E [-\log \sigma(s(\boldsymbol{h}_{\mathrm{all},i}^t, \boldsymbol{h}_{\mathrm{gen},i}^t)/\tau)] + \lambda_{\mathrm{sep}} \frac{1}{E} \sum_{i=1}^E [-\log(1 - \sigma(s(\boldsymbol{h}_{\mathrm{spur},i}^t, \boldsymbol{h}_{\mathrm{gen},i}^t)/\tau))]$$

### 4 进化正交模块

**静态与动态分量投影**：通过MLP将真实视图事件表示投影为静态和原始动态分量：
$$\boldsymbol{h}_{\mathrm{event},i}^{S,t} = f_{stat}(\boldsymbol{h}_{\mathrm{gen},i}^t), \quad \boldsymbol{h}_{\mathrm{event},i}^{\mathrm{raw},D,t} = f_{dyn}(\boldsymbol{h}_{\mathrm{gen},i}^t)$$

**动态分量正交化**：通过Gram-Schmidt正交化从原始动态分量中去除静态分量：
$$\boldsymbol{h}_{\mathrm{event},i}^{D,t} = \boldsymbol{h}_{\mathrm{event},i}^{\mathrm{raw},D,t} - \frac{\langle \boldsymbol{h}_{\mathrm{event},i}^{\mathrm{raw},D,t}, \boldsymbol{h}_{\mathrm{event},i}^{S,t} \rangle}{\|\boldsymbol{h}_{\mathrm{event},i}^{S,t}\|_2^2 + \varepsilon} \boldsymbol{h}_{\mathrm{event},i}^{S,t}$$

**动态vs静态分类器**：基于分量绝对差异预测事件 $i$ 和 $j$ 之间的因果性是否为动态：
$$p_{ij}^D = \sigma(f_{MLP}([|\boldsymbol{h}_{\mathrm{event},i}^{D,t} - \boldsymbol{h}_{\mathrm{event},j}^{D,t}|; |\boldsymbol{h}_{\mathrm{event},i}^{S,t} - \boldsymbol{h}_{\mathrm{event},j}^{S,t}|]))$$

**进化损失**：保持动态分量的时序依赖性和静态分量的时序独立性：
$$\mathcal{L}_{evo} = \lambda_{dyn} \frac{1}{|\mathcal{G}|} \sum_{g \in \mathcal{G}} \|\boldsymbol{h}_{\mathrm{event},g}^{D,t} - f_{GRU}(\tilde{\boldsymbol{h}}_{\mathrm{event},g}^{D,1;t-1})\|_2^2 + \lambda_{stat} \frac{1}{|\mathcal{G}|} \sum_{g \in \mathcal{G}} \|\boldsymbol{h}_{\mathrm{event},g}^{S,t} - \bar{\boldsymbol{h}}_{\mathrm{event},g}^{S,1;t-1}\|_2^2$$

**融合进化表示**：融合静态视图和动态视图的异质卷积结果并归一化：
$$\boldsymbol{H}_{evo}^t = \mathrm{Norm}(W_5[\mathrm{HConv}(G_{dyn}, \boldsymbol{H}_{gen}^t); \mathrm{HConv}(G_{stat}, \boldsymbol{H}_{gen}^t)])$$

### 5 总体训练目标

加权组合TKG损失、对比损失、鲁棒性损失和进化损失：
$$\mathcal{L} = (1-\lambda_{con}-\lambda_{rob}-\lambda_{evo}) \mathcal{L}_{TKG} + \lambda_{con} \mathcal{L}_{con} + \lambda_{rob} \mathcal{L}_{rob} + \lambda_{evo} \mathcal{L}_{evo}$$

其中 $\mathcal{L}_{TKG}$ 为事件预测的交叉熵损失：
$$\mathcal{L}_{TKG} = -\frac{1}{N_S} \sum_{i=1}^{N_S} \sum_{j=1}^{N_r} (y_{i,j} \log p_{i,j} + (1-y_{i,j}) \log(1-p_{i,j}))$$



## 实验与关键发现

### 1 主要结果

HEDRA在五个真实数据集上达到最先进性能。以下为关键结果：

**Table 1: ICEWS14和ICEWS18上的性能对比**

| 方法 | ICEWS14 MRR | ICEWS14 Hits@1 | ICEWS14 Hits@3 | ICEWS14 Hits@10 | ICEWS18 MRR | ICEWS18 Hits@1 | ICEWS18 Hits@3 | ICEWS18 Hits@10 |
|------|-------------|----------------|----------------|-----------------|-------------|----------------|----------------|-----------------|
| HEDRA | **47.86** | **35.28** | **53.32** | **75.65** | **46.77** | **33.62** | **52.23** | **75.06** |
| DECRL (第二名) | 42.90 | 30.49 | 48.07 | 72.35 | 43.36 | 30.07 | 48.51 | 72.98 |
| 提升 | +11.56% | +15.71% | +10.92% | +4.56% | +7.86% | +11.81% | +7.67% | +2.85% |

**Table 2: WIKI和YAGO上的性能对比**

| 方法 | WIKI MRR | WIKI Hits@1 | WIKI Hits@3 | WIKI Hits@10 | YAGO MRR | YAGO Hits@1 | YAGO Hits@3 |
|------|----------|-------------|-------------|--------------|----------|-------------|-------------|
| HEDRA | **99.14** | **98.93** | **99.37** | **99.57** | **99.12** | **98.97** | **99.27** |
| 第二名 | 99.00 (TiRGN) | 98.73 (TiRGN) | 99.30 (TiRGN) | 99.50 (TiRGN) | 95.84 (DECRL) | 93.76 (DECRL) | 97.93 (DECRL) |
| 提升 | +0.14% | +0.20% | +0.07% | +0.07% | +3.42% | +5.56% | +1.37% |

**Table 3: GDELT上的性能对比**

| 方法 | MRR | Hits@1 | Hits@3 | Hits@10 |
|------|-----|--------|--------|---------|
| HEDRA | **24.64** | **13.93** | **25.53** | **49.02** |
| DECRL (第二名) | 22.74 | 12.56 | 22.57 | 45.89 |
| 提升 | +8.36% | +10.91% | +13.11% | +6.82% |

### 2 消融实验

**Table 4: 消融实验结果（ICEWS14）**

| 变体 | MRR | Hits@1 | Hits@3 | Hits@10 |
|------|-----|--------|--------|---------|
| HEDRA (完整) | **47.86** | **35.28** | **53.32** | **75.65** |
| HEDRA-w/o-CDM (移除反事实检测器) | 47.11 | 34.25 | 52.12 | 75.04 |
| HEDRA-w/o-IVDM (移除IV引导解耦模块) | 46.47 | 33.77 | 51.65 | 74.75 |
| HEDRA-w/o-EOM (移除进化正交模块) | 46.24 | 33.49 | 51.79 | 74.10 |

关键发现：
- 移除反事实检测器（HEDRA-w/o-CDM）导致性能轻微下降（MRR从47.86降至47.11），表明非因果性对事件预测的贡献有限。
- 移除IV引导解耦模块（HEDRA-w/o-IVDM）导致性能显著下降（MRR从47.86降至46.47），表明该模块在消除虚假因果性中起关键作用。
- 移除进化正交模块（HEDRA-w/o-EOM）导致性能下降（MRR从47.86降至46.24），表明分离动态与静态因果性对事件预测有益。

### 3 案例研究

**Table 5: 案例研究——ICEWS14上的Top-5预测关系对比**

| 测试样本 | HEDRA Top-5 | DECRL Top-5 |
|---------|-------------|-------------|
| (Barack Obama, ?, Xi Jinping, 2014/11/13) | ✓ **Make a visit**, Consult, Engage in negotiation, Make a statement, Express intent to meet or negotiate | Host a visit, ✓ **Make a visit**, Consult, Make a statement, Engage in negotiation |
| (Police (Hong Kong), ?, Protester (Hong Kong), 2014/11/29) | ✓ **Use unconventional violence**, ✓ **Fight with small arms and light weapons**, ✓ **Fight with artillery and tanks**, ✓ **Employ aerial weapons**, ✓ **Engage in violent acts for political gain** | Return, release person(s), Use unconventional violence, Fight with small arms and light weapons, Fight with artillery and tanks, Employ aerial weapons |

HEDRA在第一个样本中正确预测了“Make a visit”，在第二个样本中仅预测负面关系，与香港抗议事件的真实情况一致，而DECRL错误地预测了正面关系“Return, release person(s)”。

### 4 超参数敏感性分析

- 历史窗口长度 $N_{window}$ 对性能影响较小。
- 邻居数 $k$ 对性能影响显著，$k > 7$ 时性能趋于稳定（Figure 5）。
- HEDRA对损失权重系数 $\alpha_{attn}$ 和 $\lambda_{align}$ 在合理范围内变化具有鲁棒性，默认对称设置（约0.5）接近最优（Figure 6）。

### 5 资源与效率

| 数据集 | 参数量 | 峰值CUDA内存 | 训练时间 | 推理时间 |
|--------|--------|-------------|---------|---------|
| ICEWS14 | 20.7M | 2.95 GB | 1226.63 s | 195.15 s |
| GDELT | 22.1M | 9.91 GB | 14274.41 s | - |

与DHyper和DECRL相比，HEDRA在ICEWS14上MRR提升约15%和12%，但训练延迟分别增加约2倍和1.3倍，形成清晰的Pareto前沿（Figure 4）。

### 6 少样本关系性能

在少样本关系设置下（20%关系保留20%四元组），HEDRA在ICEWS14上MRR为26.68，在ICEWS18上MRR为17.44，表明对有限监督数据具有一定鲁棒性（Table 11）。

### 7 训练动态与虚假质量诊断

**Table 10: ICEWS14上的训练动态与虚假质量诊断**

| Epoch | $\mathcal{L}_{TKG}$ | $\mathcal{L}_{con}$ | $\mathcal{L}_{rob}$ | $\mathcal{L}_{evo}$ | $\bar{p}_s$ |
|-------|---------------------|---------------------|---------------------|---------------------|-------------|
| 1 | 0.023 | 0.693 | 0.693 | 0.001 | 0.817 |
| 3 | 0.018 | 0.693 | 0.693 | 0.001 | 0.832 |
| 5 | 0.015 | 0.693 | 0.693 | 0.001 | 0.845 |
| 7 | 0.013 | 0.693 | 0.693 | 0.001 | 0.852 |
| 8* | 0.012 | 0.693 | 0.693 | 0.001 | 0.852 |

诊断统计量 $\bar{p}_s = \frac{1}{|\mathcal{E}_s|} \sum_{e \in \mathcal{E}_s} p_s(e)$ 从0.817增加到约0.852并饱和，表明IV引导模块逐渐对虚假因果边更加自信，性能提升与模型识别和抑制虚假因果性的能力提高相一致。

### 8 动态与静态分量分析

Figure 7展示了中国和日本实体的动态与静态分量步长变化。对于中国和日本，动态分量变化幅度更大，表明短期冲击被动态分量吸收，而静态分量保持相对稳定。



## 定位与知识库关联

### 1 与现有方法的关系

HEDRA属于**结构派生方法**，与以下基线方法形成对比：

- **浅层编码器基线**：TTransE (Leblay & Chekol, 2018)、TA-TransE (Garcia-Duran et al., 2018)
- **循环图卷积基线**：RE-GCN (Li et al., 2021b)、TiRGN (Li et al., 2022)、LogCL (Chen et al., 2024b)
- **结构派生基线**：EvoExplore (Zhang et al., 2022)、GTRL (Tang & Chen, 2024)、DHyper (Tang et al., 2024)、DECRL (Chen & Chen, 2024)

HEDRA是首个在事件层面解耦TKG中异质因果性的工作，与静态图因果学习方法（如PGExplainer (Luo et al., 2020)）和动态图因果学习方法（如DyGNNExplainer (Zhao & Zhang, 2024)）在问题设定和方法论上均有本质区别。

### 2 局限性

1. HEDRA的计算复杂度为 $O(E^2 D + (N_e + N_r + E) D^2)$，在大规模数据集（如GDELT）上训练时间较长（约3.97 GPU小时）。
2. 在GDELT上，HEDRA的MRR仅为24.64，Hits@1为13.93，表明在事件数量极大、关系稀疏的场景下性能仍有提升空间。
3. 少样本关系设置下（ICEWS14 MRR 26.68，ICEWS18 MRR 17.44），性能显著低于全监督设置，表明对极稀疏关系的鲁棒性有限。
4. 方法依赖于多个超参数（如 $k$、$\alpha_{attn}$、$\lambda_{align}$ 等），虽然敏感性分析表明在一定范围内鲁棒，但最优值仍需通过NNI搜索确定。
5. 当前方法仅在TKG事件预测任务上验证，未在更广泛的动态图因果学习任务上测试其泛化性。

### 3 开放问题

1. 如何进一步降低HEDRA在大规模TKG上的计算开销，例如通过近似最近邻或采样策略？
2. IV引导解耦模块中 $\alpha$ 分位数的选择是否可以在不同数据集上自适应调整？
3. 进化正交模块中的GRU是否可以被更高效的时序模型（如Transformer）替代以捕获更长程依赖？
4. HEDRA的解耦框架是否可以推广到其他动态图任务（如社交网络演化、交通流预测）？
5. 如何为解耦后的静态和动态因果性提供更直观的可视化或可解释性分析？
6. 在少样本场景下，是否可以引入元学习或外部知识来增强HEDRA的鲁棒性？

### 整体框架

![[assets/figures/papers/iclr26_0002_RdoXks7VmJ_Beyond_Entity_Correlations_Disentangling_Event_C/figures/001_Figure_1.jpg]]
*Figure 1: An example of heterogeneous causalities at the event level. IAEA denotes the International Atomic Energy Agency.*

### 实验与分析

### 补充图表

![[assets/figures/papers/iclr26_0002_RdoXks7VmJ_Beyond_Entity_Correlations_Disentangling_Event_C/figures/004_Table_1.jpg]]
*Table 1: The performance of HEDRA and the compared approaches on ICEWS14 and ICEWS18. An asterisk ( ^ { 6 6 * } ) indicates that HEDRA significantly outperforms the compared approaches based on pairwise t-tests at a 95% confidence level. The best performance is highlighted in bold, while the runner-up is underlined.*

![[assets/figures/papers/iclr26_0002_RdoXks7VmJ_Beyond_Entity_Correlations_Disentangling_Event_C/figures/005_Table_2.jpg]]
*Table 2: The performance of HEDRA and the compared approaches on WIKI and YAGO. Since the YAGO dataset contains only 10 relation types, the Hits@10 metric is not statistically meaningful and is therefore denoted as “–”. Other notations follow Table 1.*

![[assets/figures/papers/iclr26_0002_RdoXks7VmJ_Beyond_Entity_Correlations_Disentangling_Event_C/figures/006_Table_3.jpg]]
*Table 3: The performance of HEDRA and the compared approaches on GDELT. “TLE” indicates a single epoch exceeded 24 hours. “OOM” indicates out of memory. Other notations follow Table 1.*

![[assets/figures/papers/iclr26_0002_RdoXks7VmJ_Beyond_Entity_Correlations_Disentangling_Event_C/figures/007_Table_4.jpg]]
*Table 4: The performance of HEDRA and its variants. The best performance is highlighted in bold.*

![[assets/figures/papers/iclr26_0002_RdoXks7VmJ_Beyond_Entity_Correlations_Disentangling_Event_C/figures/008_Table_5.jpg]]
*Table 5: Top-5 predicted relations for two representative test samples on ICEWS14. Correctly predicted relations are indicated by a leading check mark (✓) and highlighted in bold.*



## 原文 PDF

![[paperPDFs/ICLR_2026/Beyond_Entity_Correlations_Disentangling_Event_Causal_Puzzles_in_Temporal_Knowledge_Graphs.pdf]]
