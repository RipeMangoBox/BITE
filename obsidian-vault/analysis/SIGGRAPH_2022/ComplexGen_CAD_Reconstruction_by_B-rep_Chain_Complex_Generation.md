---
title: "ComplexGen: CAD Reconstruction by B-rep Chain Complex Generation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/ComplexGen_CAD_Reconstruction_by_B_rep_Chain_Complex_Generation.pdf
project_link: "https://haopan.github.io/complexgen.html"
code_link: null
aliases:
- ComplexGen
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 显式建模B-Rep链复形结构，通过同时生成顶点、边、面及其邻接关系，并引入流形性和边界闭合等拓扑约束进行全局优化。
primary_logic: 将CAD重建定义为B-Rep链复形的生成问题，通过将拓扑关系作为分类任务、几何嵌入作为回归任务，使网络能够学习结构一致性，并利用链复形约束指导全局组合与几何优化，从而得到拓扑正确、完整且规则化的CAD模型。
claims:
- 与无拓扑生成的基线相比，Ours-Net 在顶点、边、面的检测 F-score 上均有提升，且拓扑误差（FE）从 0.229 降至 0.145。
- 经过全局优化（Ours-All），三个拓扑不一致性指标均降为 0，实现了拓扑上完全有效的 B-Rep 模型。
- 在 ABC 数据集上，ComplexGen 的点覆盖率达到 95.6%、面片召回率 87.9%，显著高于仅做面分割拟合的方法（如 ParseNet 的点覆盖率 80.3%）。
- ABC (3,000 测试样本) 上 点覆盖率 (P-cov %) = 95.6
---

# ComplexGen: CAD Reconstruction by B-rep Chain Complex Generation

> [!tip] 核心洞察
> 将CAD重建定义为B-Rep链复形的生成问题，通过将拓扑关系作为分类任务、几何嵌入作为回归任务，使网络能够学习结构一致性，并利用链复形约束指导全局组合与几何优化，从而得到拓扑正确、完整且规则化的CAD模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | ComplexGen: 基于B-Rep链复形生成的CAD重建 |
| 英文题名 | ComplexGen: CAD Reconstruction by B-rep Chain Complex Generation |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://haopan.github.io/complexgen.html) · [Project](https://haopan.github.io/complexgen.html") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ComplexGen |
| Dataset | ABC |

> [!tip] 效果简介
> - ABC (3,000 测试样本) 上，点覆盖率 (P-cov %) 95.6 vs 80.3 (ParseNet) (+15.3)；面片召回率 (Recall %) 87.9 vs 75.3 (ParseNet) (+12.6)；面到面拓扑误差 (P-to-P) 0.191 vs 0.423 (ParseNet) (-0.232)。

## 概要

现有CAD重建方法将顶点、边、面等不同阶的几何基元分离检测，缺乏对它们之间拓扑关系的统一建模，导致重建结果拓扑不一致、不完整且缺乏全局约束。本文提出ComplexGen，将CAD重建定义为B-Rep链复形的生成问题：通过稀疏CNN编码器与三路Transformer解码器同时生成顶点、边、面及其邻接关系，再经由整数线性规划提取满足流形性与边界闭合约束的有效链复形，并进行约束几何精修。在ABC数据集上，点覆盖率达95.6%、面片召回率87.9%，显著优于基于面分割拟合的ParseNet（80.3% / 75.3%），且拓扑不一致性指标全部降为零，实现了拓扑上完全有效的B-Rep模型重建。该方法定位于将拓扑关系作为显式生成目标，以链复形约束指导全局组合与几何优化，为结构完整、规则化的CAD逆向重建提供了新范式。

## 核心方法与创新机理

### 问题瓶颈与核心思想

现有 CAD 重建方法（如 **ParseNet**、**SPFN**、**PIENET**）将顶点、边、面等不同阶的几何基元视为独立检测任务，缺乏对它们之间拓扑邻接关系的统一建模。这种分离式策略导致重建结果出现三类典型失效：拓扑不一致（边未闭合、面边界不构成环）、元素冗余或缺失、以及全局结构不完整。根本原因在于，B-Rep 模型本质上是一个**链复形**（chain complex）——顶点、边、面通过边界算子 $\partial_1,\partial_2$ 构成代数结构，满足 $\partial_1\circ\partial_2=0$（即每个面的边界边构成闭合环）。分离检测无法保证这一全局约束。

ComplexGen 的核心创新在于将 CAD 重建重新定义为 **B-Rep 链复形生成问题**：同时预测三类基元及其邻接矩阵（FE、EV、FV），并利用链复形约束进行全局优化。这一设计将拓扑关系从隐式后处理提升为显式学习目标，使网络能够感知跨阶元素的结构一致性。

### 整体框架：两阶段流水线

方法分为两个阶段（图 2）：

1. **ComplexNet 神经网络**：从输入点云生成带概率的 B-Rep 链复形，包括顶点、边、面的存在性、类型、几何嵌入及拓扑邻接矩阵。
2. **全局优化**：以网络预测为引导，通过整数线性规划（ILP）提取满足流形约束的有效链复形，再进行约束几何精修。

### 第一阶段：ComplexNet 网络架构

#### 稀疏 CNN 编码器

输入点云被离散化为稀疏体素，经稀疏 CNN 编码器提取多尺度空间特征。编码器采用残差块结构（图 14），输出特征图作为后续解码器的条件信息。

#### 三路 Transformer 解码器：跨元素组通信

这是 ComplexNet 最关键的架构创新。与基线方法使用三个独立 transformer 分别解码顶点、边、面不同，ComplexNet 采用**三路交叉注意力机制**实现元素组间的信息交换。

解码器维护三组可学习查询向量 $\mathbf{Q}_v,\mathbf{Q}_e,\mathbf{Q}_f$，分别对应 $N_v$ 个顶点、$N_e$ 条边、$N_f$ 个面。每组查询经过多层解码，每层包含三个注意力步骤：

1. **自注意力**：组内元素交互，公式为
   $$\mathbf{H}_t^i \mathrel{+}= \mathrm{SA}\big(\mathrm{LN}(\mathbf{H}_t^i)+\mathbf{Q}_t,\;\mathrm{LN}(\mathbf{H}_t^i)\big)$$
   其中 $t\in\{v,e,f\}$ 表示元素类型，$\mathbf{H}_t^i$ 为第 $i$ 层的隐状态。

2. **跨元素组注意力**：当前组与其他两组交换信息，
   $$\mathbf{H}_t^i \mathrel{+}= \mathrm{CA}\big(\mathbf{X}_t+\mathbf{Q}_t,\;[\mathbf{X}_{t'\neq t}+\mathbf{Q}_{t'}+\mathbf{G}_{t'}]\big)$$
   其中 $\mathbf{G}_{t'}$ 是可学习的组类型嵌入，用于区分不同元素组。这一步使顶点解码器能够感知边和面的状态，反之亦然，从而促进一致结构的涌现。

3. **编码器-解码器交叉注意力**：以编码器输出的稀疏体素特征为键值，注入输入点云的几何信息。

每层解码器输出用于预测元素存在性（validness）、类型分类、拓扑邻接概率（FE、EV、FV）以及几何潜码。

#### 几何超网络

每条边和每个面的几何形状通过**超网络**（HyperNet）从潜码映射到参数域。具体地，边的几何嵌入模块将潜码映射为从规范参数域 $[0,1]$ 到空间曲线的映射；面的几何嵌入模块将潜码映射为从单位正方形到空间曲面的映射（图 4）。这种设计使网络能够生成包括自由曲面在内的多种几何类型，而非仅限简单解析曲面。

#### 训练损失与匹配

训练时需将预测元素与真值元素进行最优二分匹配。匹配代价定义为：
$$C(p,q) = \sum_c D_{KL}\big(c(q)\,\|\,c(p)\big) + w_{geo} D_{geo}(p,q)$$
其中第一项为类型分类的 KL 散度，第二项为几何距离（如曲线/曲面的 Chamfer 距离）。匹配后计算总损失：
$$L = L_{val} + L_{cls} + w_{geo}L_{geo} + w_{topo}L_{topo}$$
包含有效性损失（二元交叉熵）、类型分类损失、几何回归损失（$w_{geo}=300$）和拓扑预测损失（$w_{topo}=10$）。拓扑损失对 FE、EV、FV 邻接矩阵施加监督，使网络显式学习元素间的连接关系。

### 第二阶段：全局优化

#### 链复形提取（整数线性规划）

网络输出为概率形式的 B-Rep 链复形，需转化为满足拓扑约束的二进制结构。该问题被形式化为整数线性规划（ILP），目标函数包含三项：

- **一元项**：基于网络预测的存在概率和类型概率
- **二元项**：基于网络预测的拓扑邻接概率
- **几何似然项**：基于几何邻近得分 $S(a,b)=\exp(-d_{a,b}^2/\epsilon^2)$，衡量元素间的实际几何距离，$\epsilon=0.1$

约束条件包括流形边约束 $\sum_i \mathbf{FE}[i,j]=2\mathbf{E}[j]$（每条边恰邻接两个面）、边-顶点约束 $\sum_j \mathbf{EV}[i,j]=2\mathbf{E}[i]\mathbf{O}[i]$（开放边有两端点，闭合边为零），以及面边界闭合约束 $\mathbf{FE}\times\mathbf{EV}=2\mathbf{FV}$（保证 $\partial_1\circ\partial_2=0$）。ILP 求解器在满足所有约束的前提下最大化目标函数，输出拓扑上完全有效的 B-Rep 结构。

#### 约束几何精修

ILP 确定了拓扑结构后，几何精修阶段在拓扑约束下将基元形状迭代拟合到输入点云（算法 1）。拓扑结构为几何拟合提供了显式约束（图 5）：例如，圆柱面的轴线被约束为平行于直线边界、垂直于圆形边界；圆锥面的轴线被约束为垂直于圆形边界。这些约束大幅减少了几何优化的自由度，使拟合更稳定、结果更规则。

### Changed Slots 总结

相对于基线方法，ComplexGen 在三个关键维度上进行了根本性改变：

| 维度 | 基线做法 | ComplexGen 做法 |
|------|----------|-----------------|
| 元素组交互 | 三个独立 transformer，无跨组通信 | 三路交叉注意力，显式建模跨阶依赖 |
| 拓扑关系 | 未显式预测邻接关系 | 预测 FE/EV/FV 邻接矩阵，作为分类任务训练 |
| 后处理优化 | 直接使用网络输出或简单聚类 | ILP 链复形提取 + 约束几何精修，保证拓扑有效性 |

这三个改变形成因果链条：跨组通信使网络能够感知元素间的一致性 → 拓扑预测为后续优化提供强先验 → ILP 和几何精修将概率预测转化为严格有效的 B-Rep 模型。消融实验（Table 2）验证了这一链条的有效性：移除跨组通信（Baseline）导致检测精度和拓扑精度大幅下降；加入 ILP 和几何精修后（Ours-All），三个拓扑不一致性指标全部降为零。

![[assets/figures/papers/paper_list_l6_https_haopan_github_io_complexgen_html/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of ComplexGen. The point cloud (a) first goes through the ComplexNet with sparse CNN encoder and transformer decoders to generate primitive elements of different orders, i.e. corners, curves and faces, and their mutual topology. (b) shown here are the elements with validness probabilities above 0.5; the corners/curves and patches are shifted apart for better visibility. The curve ??18 and its adjacent patches are highlighted as an example of the predicted topology. (c) the probabilistic B-Rep chain complex then goes through a global optimization that solves for the optimal connection and existence of elements, where the patches adjacent to*

![[assets/figures/papers/paper_list_l6_https_haopan_github_io_complexgen_html/figures/007_Figure_6.jpg]]
*Figure 6: Result gallery. Our framework can recover CAD models with complete B-Rep structures from the unstructured input points. Freeform surfaces (a)(e), smooth junction corners and curves (d) and narrow surface patches (b)(c)(d)(f ) can be generated by our framework*

![[assets/figures/papers/paper_list_l6_https_haopan_github_io_complexgen_html/figures/008_Figure_7.jpg]]
*Figure 7: Ablation results. We test the impact of the different components of our framework. For network predictions, we round the validness of elements by 0.5 to obtain the above results. Compared with a baseline detection network, ComplexNet generation contains fewer redundancies and more accurate elements. Our chain complex extraction and geometric refinement further turn the network predictions into clean and complete B-Rep models*

## 实验与关键发现

### 一、核心消融实验：拓扑建模与全局优化的因果贡献

ComplexGen 的核心主张是显式建模 B-Rep 链复形结构能带来拓扑一致且完整的 CAD 重建。Table 2 的消融实验为该主张提供了最直接的因果证据，其对比了三个递进配置：

![[assets/figures/papers/paper_list_l6_https_haopan_github_io_complexgen_html/figures/009_Table_2.jpg]]
*Table 2: Statistics of test results for ablation settings. The baseline approach detects corners, curves and patches separately and suffers from low geometric and topological accuracies. Ours-Net improves the baseline by modeling topology explicitly. Ours-All further improves the network predictions with guaranteed topology consistency and highly improved geometric fitness (Fig. 7)*

**Baseline（独立检测）**：三个独立的 Transformer 分别生成顶点、边、面，各元素组之间无跨组通信，也不显式预测拓扑邻接关系。该配置在顶点 F-score 上仅 77.0，边 75.0，面 77.1，且面-边拓扑误差（FE）高达 0.229。

**Ours-Net（加入跨组通信与拓扑预测）**：引入三路 Transformer 解码器的跨注意力机制，同时预测 FE、EV、FV 邻接矩阵。顶点 F-score 提升至 80.9（+3.9），面 F-score 提升至 78.8（+1.7），FE 拓扑误差降至 0.145（−0.084）。这一组对比说明：**跨元素组的通信使网络能学习结构一致性，直接抑制了拓扑不一致的基元组合**。边 F-score 仅从 75.0 微升至 75.2，提示边的检测本身难度较高，网络预测仍存在冗余或遗漏。

**Ours-All（加入链复形提取与几何精修）**：在网络预测的概率化 B-Rep 链复形基础上，通过整数线性规划（ILP）提取满足流形约束的有效结构，再进行约束几何精修。三个拓扑不一致性指标（TEV、TFE、TFV）全部降为 0，实现了**拓扑上完全有效的 B-Rep 模型**。同时几何误差大幅改善，验证了链复形约束对几何拟合的强指导作用。

| 配置 | 顶点 F-score | 边 F-score | 面 F-score | FE 拓扑误差 | 拓扑不一致性 |
|------|-------------|-----------|-----------|------------|-------------|
| Baseline | 77.0 | 75.0 | 77.1 | 0.229 | 非零 |
| Ours-Net | 80.9 | 75.2 | 78.8 | 0.145 | 非零 |
| Ours-All | — | — | — | — | **全 0** |

*Table 2 消融实验定量统计（节选关键指标）*

定性结果（Fig. 7）进一步印证：Baseline 产生大量冗余基元且拓扑混乱，Ours-Net 显著减少了不一致元素，而 Ours-All 输出干净、完整的 B-Rep 模型。

### 二、与面分割+拟合方法的系统对比

Table 3 在 ABC 数据集 3,000 测试样本上将 ComplexGen 与 ParseNet（Sharma et al., ECCV 2020）等基于点云面分割与拟合的方法进行了全面比较，覆盖几何精度、覆盖完整性和拓扑保真度三个维度：

![[assets/figures/papers/paper_list_l6_https_haopan_github_io_complexgen_html/figures/010_Table_3.jpg]]
*Table 3: Comparison with “patch segmentation+fitting” approaches. The metrics evaluate patch fitting accuracy (residual), coverage and recall rate, as well as topology fidelity3. P-cov and P-to-P stand for p-coverage and patch-to-patch topology error, respectively*

| 指标 | ParseNet | ComplexGen | 差异 |
|------|----------|------------|------|
| 点覆盖率 (P-cov %) | 80.3 | **95.6** | +15.3 |
| 面片召回率 (Recall %) | 75.3 | **87.9** | +12.6 |
| 面到面拓扑误差 (P-to-P) | 0.423 | **0.191** | −0.232 |
| 残余误差 (Residual) | **0.013** | 0.019 | +0.006 |

*Table 3 与面分割+拟合方法的比较（节选 ABC 数据集关键指标）*

**覆盖率与召回率的显著领先**（+15.3% 和 +12.6%）表明：面分割方法在局部点云质量下降或基元边界模糊时容易遗漏面片，而 ComplexGen 通过同时生成顶点、边、面并施加拓扑约束，能够推断出被遮挡或采样稀疏区域的完整基元结构。

**拓扑误差的大幅降低**（−0.232）直接验证了链复形建模的核心优势：ParseNet 仅关注面的几何拟合，相邻面之间缺乏显式的边界一致性约束，导致面间拓扑关系错乱；ComplexGen 的拓扑预测与 ILP 提取则强制保证了流形边约束（每条边恰与两个面相邻）和面边界闭合约束。

**残余误差的微小劣势**（+0.006）揭示了拓扑约束与拟合精度之间的固有权衡：ComplexGen 的几何精修在拓扑约束下进行，某些局部几何细节的拟合自由度受限；而 ParseNet 无拓扑约束，可在局部更自由地贴合点云。然而这一微小代价换来了拓扑正确性和覆盖完整性的质变。

### 三、压力测试与泛化能力

**噪声与部分输入**（Table 4, Fig. 10）：在添加 σ=0.02 高斯噪声或仅提供部分点云的条件下，ComplexGen 相较 ParseNet 保持了显著优势。其鲁棒性源于多阶基元的相互约束——即使局部点云质量下降，拓扑结构仍能约束基元的存在性和几何形态。相比之下，基于分割的方法对局部采样质量更敏感，噪声或缺失直接导致面片分割失败。

**跨数据集泛化**（Fig. 11）：在 ShapeNet 模型和 AIM@SHAPE-VISIONAIR 真实扫描数据上，ComplexGen 展现了超出训练分布（ABC 数据集）的泛化能力。真实扫描存在底部缺失和高度非均匀采样，ComplexGen 仍能恢复出合理的 B-Rep 结构，但完整性和精度相比 ABC 测试集有所下降——这暴露了当前模型对训练数据分布的依赖性。

**PIENET 定性比较**（Fig. 9）：与仅检测尖锐边角的 PIENET（Wang et al., NeurIPS 2020）相比，ComplexGen 的链复形结构确保曲线和角点连接成有效面边界，因而重建更完整；同时 ComplexGen 还能检测光滑曲线（如圆柱面边界），这是 PIENET 所不具备的能力。

### 四、失败模式与适用边界

**元素容量限制**：网络预设了最大基元数量 $N_v, N_e, N_f$，当 CAD 模型超出此规模时，部分基元无法被检测。这是固定容量生成式方法的固有瓶颈，对极端复杂模型需手动调整容量上限。

**小基元丢弃风险**：非极大抑制和 ILP 提取中的阈值机制可能丢弃部分正确的微小基元（如窄面片、短边），导致局部几何细节丢失。Fig. 13 的有效性分析示例展示了因曲线类型预测错误（圆弧被预测为直线）导致的冗余基元问题。

**ILP 求解时间**：链复形提取的平均求解时间为 545 秒，占总流程时间的绝对主导（网络推理仅 89 ms，几何精修 8 秒）。这限制了 ComplexGen 在实时或交互式场景中的应用，是该框架的主要工程瓶颈。

**几何约束类型有限**：当前几何精修中可自动推断的约束类型有限（如圆柱轴与边界平行/垂直、圆锥轴与圆形边界垂直），更多 CAD 操作（倒角、旋转面、扫掠面等）的约束尚未被利用，导致此类特征的拟合精度受限。

**真实扫描的精度上限**：尽管展示了泛化能力，但在严重噪声或高度不规则采样的真实扫描上，重建的完整性和精度仍有明显提升空间。这是从合成数据（ABC）向真实数据迁移时的普遍挑战。

### 五、有效性评估的统计证据

Fig. 12 展示了全部 3,000 测试样本的有效性分布直方图：以 0.03 为阈值，绝大多数样本具有高比例的几何可实现拓扑连接。这一统计表明 ComplexNet 预测的拓扑关系在几何层面高度自洽，为后续 ILP 提取提供了可靠的概率基础。Fig. 13 的具体案例分析揭示了少数不一致的来源：拓扑上相连的边和角点因曲线类型预测错误而无法在几何上实现，且这些元素在真值中本身是冗余的——说明网络在复杂局部结构上仍存在过预测倾向。

![[assets/figures/papers/paper_list_l6_https_haopan_github_io_complexgen_html/figures/012_Figure_9.jpg]]
*Figure 9: PIENET comparison. We compare our method with PIENET that detects sharp corners and curves. For (a)(b), our complex structure ensures that the curves and corners connect into valid patch boundaries and therefore more complete. For (c), we detect smooth curves in addition to sharp ones, as smooth curves delineate primitive patches*

## 定位与知识库关联

ComplexGen 的核心定位是将 CAD 重建从“几何基元检测”提升为“B-Rep 链复形生成”。其相对于已有工作的本质差异在于改变了三个关键 slot，从而将拓扑一致性从后处理补救转变为核心生成目标。

### 改变的 Slot 与本质差异

**Slot 1：元素组之间的交互机制。** 此前的代表性方法——如基于点云面分割的 **ParseNet** (Sharma et al., ECCV 2020)、监督式基元拟合的 **SPFN** (Li et al., CVPR 2019)、参数化边缘检测的 **PIENET** (Wang et al., NeurIPS 2020) 以及经典的 **Efficient RANSAC** (Schnabel et al., 2007)——均将顶点、边、面作为独立检测任务处理，各元素组之间不存在信息交换。这种分离范式导致网络无法学习跨阶一致性：一条边是否应存在，不仅取决于其自身的几何证据，还取决于其端点顶点和邻接面的存在性。ComplexGen 将这一 slot 从“无跨组通信”改为“三路 Transformer 解码器通过跨注意力交换信息”，使顶点、边、面的生成相互制约，从机制上促进了结构一致元素的共现。

**Slot 2：拓扑关系的显式预测。** 已有方法将拓扑关系视为检测结果的隐式副产品——ParseNet 通过面分割的邻接关系间接推断拓扑，PIENET 仅检测边缘曲线而不建模其与面的邻接关系，SPFN 和 Efficient RANSAC 则完全不涉及拓扑。ComplexGen 将拓扑关系从“未显式预测”改为“作为分类任务直接输出 FE、EV、FV 邻接矩阵”，并将这些概率化的拓扑预测作为后续全局优化的目标函数项。这一改变使拓扑正确性成为可监督、可优化的学习目标，而非事后启发式修复的对象。

**Slot 3：后处理的全局约束优化。** 已有方法的后处理通常限于非极大抑制、简单聚类或独立基元拟合，缺乏对 B-Rep 整体有效性的保证。ComplexGen 将这一 slot 从“无全局约束”改为“基于整数线性规划的链复形提取与约束几何精修”，显式施加流形边约束（$\sum_i \mathbf{FE}[i,j] = 2 \mathbf{E}[j]$）、边-顶点约束和面边界闭合约束（$\mathbf{FE} \times \mathbf{EV} = 2 \mathbf{FV}$），确保最终输出的 B-Rep 模型在拓扑上完全有效。

### 知识库挂载点

ComplexGen 在知识库中的挂载点位于 **CAD 逆向工程与结构化三维重建** 的交叉节点。其上游连接两条知识线：（1）基于学习的几何基元检测（SPFN、ParseNet、PIENET），ComplexGen 继承了其将基元检测形式化为集合预测问题的范式，但将输出空间从独立基元扩展为带拓扑关系的链复形；（2）B-Rep 拓扑形式化理论（链复形代数），ComplexGen 将抽象的边界算子 $\partial_2, \partial_1$ 和链复形条件 $\partial_1 \circ \partial_2 = 0$ 转化为可优化的线性约束，实现了拓扑理论的工程落地。

其下游可挂载至：（1）CAD 模型编辑与参数化重建——ComplexGen 输出的有效 B-Rep 可直接导入 CAD 软件进行编辑；（2）逆向工程中的约束推断——几何精修阶段已利用拓扑关系推断部分几何约束（如圆柱轴线与圆形边界的垂直关系），可进一步扩展为更丰富的 CAD 操作约束自动推断；（3）交互式重建修复——通过有效性评估指标识别拓扑不一致区域，引导用户进行最少交互的修复。

### 适用边界

ComplexGen 的适用性受以下边界条件限制：（1）**模型复杂度上限**：网络预设了最大元素数量 $N_v, N_e, N_f$，超出训练规模的极端复杂模型可能无法被完全覆盖；（2）**输入质量要求**：实验主要在相对清洁的 ABC 合成数据集上进行，尽管对噪声和部分数据进行了压力测试（Table 4），真实扫描数据上的完整性和精度仍有提升空间；（3）**计算效率约束**：链复形提取的整数线性规划求解平均耗时 545 秒，适合离线批量重建，不适用于实时交互场景；（4）**几何细节覆盖**：非极大抑制和 ILP 提取可能丢弃部分正确的小基元，难以完美覆盖所有几何细节。

### 后续启发

ComplexGen 为后续工作提供了三个方向的启发：（1）**拓扑感知的生成式重建**——将拓扑约束纳入学习目标而非后处理的范式，可推广至其他需要结构化输出的重建任务（如建筑建模、电路板重建）；（2）**神经引导的组合优化**——用网络预测的概率作为组合优化目标函数的系数，在保证全局约束的前提下最大化数据似然，这一范式在需要保证硬约束的生成任务中具有通用价值；（3）**分割方法与生成方法的融合**——ComplexGen 在残余误差上略逊于 ParseNet，说明基于分割的局部拟合在几何精度上有优势，如何将分割方法的局部精度与生成方法的全局一致性结合，是值得探索的方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/ComplexGen_CAD_Reconstruction_by_B_rep_Chain_Complex_Generation.pdf]]