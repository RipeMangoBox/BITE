---
title: Implicit Conversion of Manifold B-Rep Solids by Neural Halfspace Representation
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Implicit_Conversion_of_Manifold_B_Rep_Solids_by_Neural_Halfspace_Representation.pdf
project_link: null
code_link: "https://github.com/guohaoxiang/NH-Rep"
aliases:
- NRNHR
- ICMBRSBNHR
tags:
- SIGGRAPH_ASIA_2022
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 局部采样策略的标准偏差 σ：减小 σ 至 σ/10 可以显著增加窄区域内的有效训练点数，从而解决内部/外部分类混淆。
primary_logic: 将流形B-Rep实体通过神经半空间表示（NH-Rep）转换为隐式场，天然支持布尔操作，并利用自适应局部采样（减小 σ）与更高分辨率的等值面提取，能够在CAD模型上实现优于SPR和IGR的倒角距离和法向角度误差，同时在交并比（IoU）等指标上取得最佳效果。
claims:
- 在FCD、FAE和IoU指标上，NH-Rep方法表现最优。
- NH-Rep在CD、HD和NAE分布上与SPR和IGR相当，且包含更少的极差结果。
- 使用布尔操作使得NH-Rep的SDF近似不如IGR，但仍远优于SIREN。
- Benchmark dataset 上 CD, HD, NAE = NH-Rep (Ours)
---

# Implicit Conversion of Manifold B-Rep Solids by Neural Halfspace Representation

> [!tip] 核心洞察
> 将流形B-Rep实体通过神经半空间表示（NH-Rep）转换为隐式场，天然支持布尔操作，并利用自适应局部采样（减小 σ）与更高分辨率的等值面提取，能够在CAD模型上实现优于SPR和IGR的倒角距离和法向角度误差，同时在交并比（IoU）等指标上取得最佳效果。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于神经半空间表示的流形B-Rep实体隐式转换 |
| 英文题名 | Implicit Conversion of Manifold B-Rep Solids by Neural Halfspace Representation |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://guohaoxiang.github.io/projects/nhrep.html) · [Code](https://github.com/guohaoxiang/NH-Rep) |
| Topic | #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | NH-Rep (Neural Halfspace Representation) |
| Dataset | Benchmark dataset |

> [!tip] 效果简介
> - Benchmark dataset 上，CD, HD, NAE NH-Rep (Ours) vs SPR, IGR (分布相当，极差结果更少)；FCD, FAE, IoU NH-Rep (Ours) vs 所有比较方法（包括SPR, IGR, SIREN） (表现最佳)；SDF approximation (quality) NH-Rep (Ours) vs IGR, SIREN (逊于IGR，但远优于SIREN)。

## 概要

将流形B-Rep实体转换为隐式场表示时，极窄与薄特征区域的等值面提取不稳定，且默认局部采样策略无法在狭窄区域内生成足够训练点，导致网络难以准确区分内外表面。本文提出**NH-Rep**（神经半空间表示），利用神经网络学习半空间隐式场，天然支持布尔操作，并通过自适应局部采样（将采样标准差由默认σ缩减至 $\frac{\sigma}{10}$）与更高分辨率等值面提取解决上述瓶颈。在基准数据集上，NH-Rep在倒角距离（CD）、豪斯多夫距离（HD）和法向角度误差（NAE）分布上与SPR、IGR相当，但极差结果更少；在面片倒角距离（FCD）、面片角度误差（FAE）和交并比（IoU）指标上达到最优。该方法在保持布尔操作能力的同时，SDF逼近精度略逊于IGR，但远优于SIREN。

## 核心方法与创新机理

### 问题背景与核心瓶颈

B-Rep（边界表示）是CAD工业中表示三维实体的标准范式，其通过拓扑面、边、顶点以及底层几何曲面（如NURBS）精确定义流形实体。然而，将这种显式、离散的B-Rep模型转换为连续的隐式场表示（如符号距离场SDF）一直是几何处理中的难题。传统方法在处理复杂CAD模型时面临两个关键瓶颈：

**瓶颈一：极窄与薄特征区域的采样不足。** 局部训练点的生成依赖于从表面点出发的高斯扰动（标准差σ）。在默认参数下，当模型包含极窄通道、薄壁或细长特征时，高斯采样的概率密度在模型内部区域急剧下降，导致网络在这些关键区域几乎没有训练信号。这使得神经网络无法准确学习内外表面的分界，产生错误的重建结果（如Figure 1左侧的错误案例所示）。

**瓶颈二：等值面提取的不稳定性。** 在极窄区域，即使隐式场本身学习正确，低分辨率的等值面提取（如Marching Cubes）也可能因网格分辨率不足以解析特征而生成错误的拓扑结构。

### 核心创新：神经半空间表示（NH-Rep）

NH-Rep的核心思想是将流形B-Rep实体分解为一组半空间（halfspaces）的布尔组合，并使用神经网络隐式地学习这些半空间的场函数。具体而言，每个B-Rep实体由多个面（faces）界定，每个面对应一个半空间约束（即点位于面的哪一侧）。NH-Rep通过神经网络$f_\theta: \mathbb{R}^3 \to \mathbb{R}$隐式编码所有半空间的逻辑组合，使得网络的零等值面逼近原始B-Rep实体的边界。

这一表示天然支持布尔操作（交、并、差），因为半空间的逻辑组合本质上就是布尔运算的连续松弛。这是NH-Rep区别于SPR和IGR等纯SDF学习方法的核心优势——后者通常只能表示单一水密流形，而NH-Rep可以隐式地表示由多个半空间布尔组合而成的复杂实体。

### 方法框架与模块顺序

NH-Rep的完整流程包含三个关键模块，按训练到推理的顺序展开：

**模块一：局部采样点生成（训练阶段）**
给定输入B-Rep模型，首先从其表面均匀采样一组表面点$P_s$。然后，对每个表面点$p \in P_s$施加高斯扰动，生成局部训练点集：
$$p_{\text{train}} = p + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2 I)$$
其中$\sigma$是控制扰动范围的标准差。这些训练点分布在表面附近，用于监督网络学习半空间的内外分类。

**模块二：神经半空间表示网络训练**
网络$f_\theta$接收三维坐标$x \in \mathbb{R}^3$作为输入，输出一个标量场值。训练目标是最小化预测场值与真实半空间标签之间的损失。真实标签由B-Rep的几何内核计算：对于每个训练点，判断其位于每个面的内侧还是外侧，进而通过布尔组合确定该点是否在实体内部。网络通过反向传播学习这些半空间的隐式组合规律。

**模块三：等值面提取（推理阶段）**
训练完成后，在规则三维网格上评估网络$f_\theta$，提取零等值面$f_\theta(x) = 0$作为重建的实体边界。提取分辨率是可调节的超参数，提高分辨率可以有效缓解极窄区域的错误等值面问题。

### Changed Slots：关键参数调整

NH-Rep相对于基线方法的关键改进体现在一个决定性的参数调整上：

**Changed Slot：局部采样标准差从$\sigma$降至$\frac{\sigma}{10}$**

这是解决核心瓶颈一的直接手段。原始默认采样策略使用标准差$\sigma$，在极窄区域内采样点数量不足。通过将标准差缩小一个数量级至$\frac{\sigma}{10}$，高斯扰动的概率密度在表面附近更加集中，显著增加了窄通道、薄壁等关键区域内的有效训练点数。这使得网络能够获得足够的监督信号来正确区分内外表面，从根本上解决了极窄区域的重建失败问题。

这一调整的因果关系链清晰：**减小$\sigma$ → 增加窄区域训练点密度 → 网络充分学习内外分类 → 消除错误重建**。该机制在补充材料中得到了明确验证：“By reducing $\sigma$ to $\frac{\sigma}{10}$, more points can be sampled within the model, and the problem can be solved.”

### 训练与推理路径

**训练路径：**
1. 从B-Rep模型表面采样点集$P_s$
2. 以标准差$\frac{\sigma}{10}$生成局部训练点（changed slot）
3. 通过B-Rep几何内核计算每个训练点的真实半空间标签（内部/外部）
4. 前向传播网络$f_\theta$得到预测场值
5. 计算分类损失并反向传播更新网络参数
6. 重复至收敛，网络隐式学会半空间的布尔组合

**推理路径：**
1. 在目标分辨率的三维网格上密集评估$f_\theta$
2. 提取零等值面$f_\theta(x)=0$
3. 可选地提高等值面提取分辨率以处理极窄特征

### 关键公式与变量含义

核心公式为局部采样策略的数学描述：
$$p_{\text{train}} = p + \epsilon, \quad \epsilon \sim \mathcal{N}(0, (\frac{\sigma}{10})^2 I)$$

其中：
- $p \in P_s$：从B-Rep表面均匀采样的表面点
- $\epsilon$：服从多元正态分布的扰动向量
- $\sigma$：原始默认标准差（未明确给出具体数值，但调整比例为$\frac{1}{10}$）
- $I$：单位矩阵，表示各向同性扰动
- $p_{\text{train}}$：最终用于训练的局部点

这一公式的关键在于标准差的选择直接决定了训练点在表面附近的分布密度。在极窄区域（如宽度为$d$的通道），原始$\sigma$可能导致$\text{Prob}(p_{\text{train}} \in \text{窄区域}) \approx 0$，而$\frac{\sigma}{10}$将该概率提升至可训练水平。

### 模块间因果关系

三个模块之间存在紧密的因果依赖：

1. **采样模块 → 训练模块**：采样点的质量和密度直接决定网络的学习效果。减小$\sigma$使得窄区域的采样密度从“几乎为零”提升至“充分”，这是解决瓶颈一的充分条件。

2. **训练模块 → 推理模块**：网络$f_\theta$学到的隐式场质量决定了等值面提取的保真度。然而，即使隐式场正确，低分辨率提取仍可能在窄区域产生错误拓扑（瓶颈二）。因此，推理模块需要独立地提高分辨率来补偿。

3. **采样模块与推理模块的协同**：减小$\sigma$解决了训练信号不足的问题，提高等值面分辨率解决了提取精度的问题。两者共同作用，才能完整地解决极窄区域的重建挑战。补充材料明确指出：“Increasing the isosurfacing level to a higher resolution can solve this issue in most cases.”

### 与基线方法的本质区别

相对于SPR和IGR，NH-Rep的根本区别不在于网络架构，而在于**表示范式**：SPR和IGR学习的是单一符号距离场（SDF），要求整个实体由一个连续函数表示；NH-Rep学习的是多个半空间的布尔组合，这使得它能够自然地处理由多个面布尔运算构成的复杂B-Rep实体。这一表示层面的优势使得NH-Rep在FCD、FAE和IoU等指标上表现最优。

然而，布尔操作的引入也带来了代价：由于半空间的组合需要通过网络的隐式编码实现，其对真实SDF的逼近精度不如直接学习SDF的IGR方法。这是NH-Rep的一个固有权衡——以略微牺牲SDF精度为代价，换取了布尔操作能力和更优的整体重建指标。

## 实验与关键发现

### 主要定量结果

NH-Rep 在 Benchmark dataset 上与三个代表性基线方法进行了系统比较：**SPR**、**IGR** 和 **SIREN**。实验覆盖了七项重建质量指标，结果呈现出明显的指标依赖性分化。

**表面距离指标（CD, HD, NAE）：分布相当，极端值更少。** 在倒角距离（Chamfer Distance, CD）、豪斯多夫距离（Hausdorff Distance, HD）和法向角度误差（Normal Angular Error, NAE）三项指标上，NH-Rep 的整体分布与 SPR 和 IGR 处于同一水平线，但表现出更优的鲁棒性——其分布尾部更短，包含明显更少的极差重建结果。图 2 的直方图分布直观展示了这一特征：NH-Rep 的 CD、HD、NAE 分布中心与 SPR/IGR 基本重合，但在高误差尾部区域，NH-Rep 的频率显著低于对比方法。这一结果说明，虽然 NH-Rep 在常规区域的表面重建精度与最优方法持平，但其对困难案例的处理更为稳健。

**体积与特征保持指标（FCD, FAE, IoU）：全面领先。** 在特征倒角距离（Feature Chamfer Distance, FCD）、特征角度误差（Feature Angular Error, FAE）和交并比（Intersection over Union, IoU）三项指标上，NH-Rep 在所有比较方法中表现最佳。这三项指标侧重衡量重建结果对原始模型尖锐特征和整体体积的保持能力，NH-Rep 的领先优势表明其神经半空间表示在保留 CAD 模型的几何特征方面具有本质优势。图 3 的指标直方图显示，NH-Rep 在 FCD 和 FAE 上的分布整体左移（向低误差方向），IoU 分布则右移（向高重合度方向），与所有基线方法形成清晰的分隔。

**SDF 逼近精度：介于 IGR 和 SIREN 之间。** 由于 NH-Rep 依赖布尔操作来组合多个半空间以构建复杂实体，其学习到的隐式场并非严格的带符号距离场（SDF），而是半空间交/并/差组合后的隐式场。这一设计使得 NH-Rep 在 SDF 逼近质量上逊于专门优化 Eikonal 约束的 IGR，但仍远优于使用周期激活函数的 SIREN。这一折中体现了 NH-Rep 的核心设计权衡：以部分 SDF 精度换取原生布尔操作能力。

### 关键消融实验

论文通过定性分析揭示了两个对重建质量有决定性影响的控制因子，并给出了明确的消融验证。

**局部采样标准差 σ 的调整：解决窄区域训练不足。** NH-Rep 的默认训练采样策略是从表面点出发，使用标准差为 σ 的正态分布 N(0, σ) 进行扰动生成局部采样点。在极窄和薄的特征区域（如肋板、薄壁结构），默认 σ 值导致大部分扰动点落在模型外部，网络无法获得足够的内部训练信号来正确区分内外表面，最终在等值面提取时产生错误的拓扑结构。将标准差减小至 $\frac{\sigma}{10}$ 后，采样点更集中地落在窄区域内部，网络能够学习到正确的半空间决策边界，问题得到解决。图 1 左侧展示了这一改进前后的定性对比：减小 σ 后，原本在窄区域的错误等值面被修正，重建结果与 Ground Truth 模型趋于一致。

**等值面提取分辨率的提升：缓解薄特征区域的提取不稳定。** 即使网络已经学习了正确的隐式场，在等值面提取阶段，低分辨率网格可能无法准确捕捉极窄和薄的特征区域，导致等值面出现断裂或错误连接。将等值面提取分辨率提高到更高水平，可以在大多数情况下解决此问题。这一发现表明，NH-Rep 的最终重建质量受训练采样策略和推理阶段等值面提取参数的双重影响，两者需要协同调整。

### 失败模式与局限性

论文明确指出了 NH-Rep 的三项主要局限性：

1. **极窄与薄特征区域的不稳定性。** 这是 NH-Rep 最主要的失败来源。即使通过减小 σ 和提高等值面分辨率可以缓解，但在极端几何条件下（如厚度接近或小于采样密度的特征），重建仍可能出现错误。根本原因在于局部采样策略的统计性质：当特征尺度与 σ 可比时，很难保证足够的有效采样点。

2. **默认采样策略的覆盖不足。** 默认的全局 σ 设置缺乏对局部几何复杂度的适应性，在窄区域系统性欠采样。这一问题通过手动减小 σ 得到验证，但需要针对不同模型调整参数，缺乏自动化。

3. **布尔操作带来的 SDF 精度损失。** 与 IGR 相比，NH-Rep 的 SDF 近似精度存在差距。这是其核心设计（神经半空间表示 + 布尔操作）的固有代价：布尔操作在隐式场中引入了不可微的组合逻辑，使得网络无法像 IGR 那样严格满足 Eikonal 方程。

### 适用边界

综合实验结果，NH-Rep 的适用边界可归纳为：

- **优势场景：** 需要保留 CAD 模型尖锐特征和精确体积的 B-Rep 实体隐式转换任务，尤其是下游应用涉及布尔操作的工作流。在 FCD、FAE、IoU 指标上的领先表明其特别适合特征敏感型应用。
- **持平场景：** 常规区域的表面重建精度与 SPR/IGR 相当，在 CD、HD、NAE 指标上不存在显著差距。
- **劣势场景：** 对 SDF 精度有严格要求的应用（如基于 SDF 梯度的物理仿真）可能受限于其布尔操作带来的精度损失；极窄薄壁结构的重建需要额外的参数调优（减小 σ、提高等值面分辨率），在自动化流程中可能成为瓶颈。

### 开放问题

论文的实验分析引出了两个值得进一步探索的方向：一是开发自适应局部采样策略，根据几何复杂度自动调整 σ 值，避免手动调参；二是在保持布尔操作能力的前提下，通过改进网络架构或训练约束来缩小与 IGR 在 SDF 逼近精度上的差距。

![[assets/figures/papers/paper_list_l60_https_guohaoxiang_github_io_projects_nhrep_html/figures/002_Figure_2.jpg]]
*Figure 2: Metric histogram of different methods.The metrics include CD,HD,and NAE*

![[assets/figures/papers/paper_list_l60_https_guohaoxiang_github_io_projects_nhrep_html/figures/003_Figure_3.jpg]]
*Figure 3: Metric histogram of different methods.The metrics include FCD,FAE,DE,and loU*

## 定位与知识库关联

本文的核心贡献在于提出 **NH-Rep（Neural Halfspace Representation）**，将流形 B-Rep 实体转换为可学习的神经隐式场。相对于已有的隐式场重建方法，NH-Rep 改变的 **关键 slot** 是 **几何表示范式**：从直接学习符号距离函数（SDF）转向学习 **半空间隐式场**，天然内嵌布尔操作能力。这一改变决定了该方法在整个知识库中的定位——它位于 **B-Rep 实体表示** 与 **神经隐式场** 的交叉地带，既不是纯粹的 CAD 边界表示，也不是传统意义上的 SDF 学习。

### 相对于基线方法的本质差异

与基线方法 **SPR** 和 **IGR** 相比，NH-Rep 不直接逼近 SDF，而是通过神经网络学习一组半空间，再经由布尔运算组合成最终的隐式场。这一设计带来了两个直接后果：

1. **布尔操作的原生支持**：SPR 和 IGR 学习的是单一 SDF，对布尔操作没有天然支持；NH-Rep 的半空间结构使得并、交、差等布尔操作成为网络输出的直接组合，无需后处理或额外训练。这使 NH-Rep 天然适配 CAD 建模中常见的特征组合工作流。

2. **SDF 逼近精度的代价**：分析证据明确指出，“The use of Boolean operations makes our method worse than IGR in approximating SDF but still much better than SIREN”。这表明半空间表示在获得布尔操作能力的同时，牺牲了部分对真实 SDF 的逼近精度。这一 trade-off 是理解该方法适用边界的关键：当应用场景需要精确的 SDF 值（如基于 SDF 的物理仿真），IGR 可能更优；当应用场景需要灵活的布尔操作（如交互式 CAD 编辑），NH-Rep 的优势显现。

### 知识库挂载点

NH-Rep 可挂载到以下知识库节点：

- **神经隐式表示（Neural Implicit Representations）**：与 **SIREN**（Sitzmann et al., NeurIPS 2020）等基于周期激活函数的隐式表示不同，NH-Rep 在表示层面引入了结构化先验（半空间分解），而非仅依赖网络架构设计。这为“如何将几何先验注入神经隐式场”提供了一个新方向。

- **B-Rep 到隐式场的转换**：传统方法将 B-Rep 转换为 SDF 通常依赖解析计算或体素化，NH-Rep 提供了一条基于学习的转换路径，使得转换过程可以端到端优化，且能处理解析方法难以覆盖的复杂拓扑。

- **自适应采样策略**：NH-Rep 揭示了一个关键瓶颈——默认的局部采样策略（以表面点为中心、标准差 $\sigma$ 的正态分布扰动）在极窄和薄特征区域内采样点不足，导致网络无法正确区分内外表面。将标准差减小至 $\frac{\sigma}{10}$ 可以显著改善这一问题。这一发现对神经隐式场训练中的采样策略设计具有普遍参考价值，可挂载到“隐式场训练的采样策略”知识节点。

### 适用边界

基于分析证据，NH-Rep 的适用边界可明确界定：

- **优势域**：包含窄缝、薄壁等精细特征的 CAD 模型，且需要布尔操作能力。在 FCD、FAE 和 IoU 指标上，NH-Rep 表现最优（confidence 0.95）；在 CD、HD 和 NAE 分布上，与 SPR 和 IGR 相当，但极差结果更少（confidence 0.95）。

- **劣势域**：对 SDF 逼近精度要求极高的场景。由于布尔操作引入的近似误差，NH-Rep 的 SDF 质量逊于 IGR。

- **已知失效模式**：极窄和薄的特征区域仍可能导致等值面提取不稳定，即便减小采样标准差和提高等值面提取分辨率也只能“在大多数情况下”解决（confidence 0.85），并非完全消除。这意味着在极端几何条件下，NH-Rep 的重建结果可能仍存在局部错误。

### 后续启发与开放问题

NH-Rep 为后续研究留下了两个明确的开放方向：

1. **自适应采样策略**：当前需要人工将 $\sigma$ 减小至 $\frac{\sigma}{10}$ 来解决窄区域训练不足的问题。能否开发根据局部几何复杂度自动调整采样密度的自适应策略，使方法对各类几何特征都具有鲁棒性？这一方向与知识库中“几何自适应的采样”节点直接关联。

2. **SDF 逼近精度与布尔操作能力的权衡**：在保持布尔操作能力的同时，能否通过改进网络架构或训练策略，进一步缩小与 IGR 在 SDF 逼近精度上的差距？这涉及表示能力的根本性权衡，可能需要新的半空间参数化或损失函数设计。

总体而言，NH-Rep 在神经隐式表示与 CAD 实体表示之间建立了一座桥梁，其半空间分解的设计选择带来了明确的优势与代价，为后续工作在表示能力、采样策略和布尔操作支持三个维度上的改进提供了清晰的起点。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Implicit_Conversion_of_Manifold_B_Rep_Solids_by_Neural_Halfspace_Representation.pdf]]