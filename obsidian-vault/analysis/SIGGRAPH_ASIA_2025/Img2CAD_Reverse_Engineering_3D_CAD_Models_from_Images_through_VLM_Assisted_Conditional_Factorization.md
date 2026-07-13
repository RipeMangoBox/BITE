---
title: "Img2CAD: Reverse Engineering 3D CAD Models from Images through VLM-Assisted Conditional Factorization"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/Img2CAD_Reverse_Engineering_3D_CAD_Models_from_Images_through_VLM_Assisted_Conditional_Factorization.pdf
code_link: https://github.com/qq456cvb/Img2CAD
project_link: https://qq456cvb.github.io/projects/img2cad
aliases:
- Img2CAD
tags:
- SIGGRAPH_ASIA_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "条件分解策略：将任务分为两个子问题，首先由微调的VLM（Llama3.2）预测具有语义部分标签的离散CAD基础结构，然后由专用的Transformer网络（TrAssembler）条件于该结构预测连续属性。此外引入流匹配损失和推理时对称引导，进一步提升重建质量。"
primary_logic: "VLM能够有效地从图像中推断通用的离散结构和语义部分，而条件化后的连续属性预测网络可以共享不同对象间对应部分的属性学习（类似层跨纤维一致性），从而大幅降低数据需求并提高泛化性；层次Transformer和对称约束进一步保证了结构的连接性和对称性。"
claims:
- "与端到端基线DeepCAD-End2End相比，Img2CAD将平均Chamfer距离从0.3108降低至0.1174 (-62.2%)，并将分割准确率提高17.94%、mIoU提高19.03%。"
- "消融实验表明，层次Transformer设计、语义部分嵌入、流匹配损失和对称引导均带来显著性能提升，其中流匹配和对称引导对结构完整性尤其关键。"
- "对称引导将#SCC从1.49降至1.11，SymChamfer从0.1145降至0.0756，表明对称性和连接性改善。"
- "CAD-ified Chair, Table, Cabinet (average) 上 Chamfer Distance (CD) ↓ = 0.1174"
---

# Img2CAD: Reverse Engineering 3D CAD Models from Images through VLM-Assisted Conditional Factorization

> [!tip] 核心洞察
> VLM能够有效地从图像中推断通用的离散结构和语义部分，而条件化后的连续属性预测网络可以共享不同对象间对应部分的属性学习（类似层跨纤维一致性），从而大幅降低数据需求并提高泛化性；层次Transformer和对称约束进一步保证了结构的连接性和对称性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Img2CAD：通过VLM辅助条件分解从图像逆向工程3D CAD模型 |
| 英文题名 | Img2CAD: Reverse Engineering 3D CAD Models from Images through VLM-Assisted Conditional Factorization |
| 会议/期刊 | SIGGRAPH Asia 2025 |
| Links | [paper](https://arxiv.org/abs/2408.01437) · [GitHub](https://github.com/qq456cvb/Img2CAD) · [Project](https://qq456cvb.github.io/projects/img2cad) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Img2CAD |
| Dataset | CAD-ified Chair, Table, Cabinet (average), Cabinet, 任意视角 (Arbitrary Views, average over categories) |

> [!tip] 效果简介
> - CAD-ified Chair, Table, Cabinet (average) 上，Chamfer Distance (CD) ↓ 为 0.1174，对比 0.3108 (DeepCAD-End2End)，变化 -0.1934 (-62.2%)。
> - CAD-ified Chair, Table, Cabinet 上，Segmentation Accuracy ↑ 为 relative improvement，对比 DeepCAD-End2End，变化 +17.94% (相对提升)。
> - CAD-ified Chair, Table, Cabinet 上，Segmentation mIoU ↑ 为 relative improvement，对比 DeepCAD-End2End，变化 +19.03% (相对提升)。

## 概要

**问题瓶颈**：从单张图像逆向重建3D CAD模型面临双重挑战——离散命令结构与连续属性参数的组合复杂性，以及从单一视角推断完整三维几何的固有歧义性。传统端到端方法（如DeepCAD-End2End）直接回归完整CAD命令序列，难以在有限数据下同时学习离散决策与精确连续参数，导致重建质量受限。

**核心思路**：Img2CAD提出**条件分解策略**，将任务拆解为两个子问题：首先利用微调的视觉语言模型（Llama3.2）从图像中预测带有语义部分标签的离散CAD基础结构，然后由专用的层次Transformer网络（TrAssembler）以该结构为条件，通过流匹配去噪过程回归连续属性参数。这一分解使得VLM发挥其通用视觉理解优势处理离散结构决策，而TrAssembler则专注于条件化连续属性预测，共享不同对象间对应部分的属性学习，大幅降低数据需求并提升泛化性。此外，推理时引入对称引导损失，进一步强化输出CAD模型的对称性与结构完整性。

**方法定位**：Img2CAD属于图像到CAD的逆向工程方法，区别于直接回归的端到端范式（如DeepCAD-End2End）和纯VLM端到端预测方案（如GPT-4o直接输出CAD程序）。其核心创新在于将VLM的语义理解能力与专用几何推理网络解耦协作，并引入流匹配损失和对称引导机制，在CAD-ified ShapeNet数据集（椅子、桌子、柜子）上建立了新的性能基准。

**主要结果**：与端到端基线DeepCAD-End2End相比，Img2CAD将平均Chamfer距离从0.3108降至0.1174（降低62.2%），分割准确率相对提升17.94%，mIoU提升19.03%（Table 1）。消融实验证实，层次Transformer设计、语义部分嵌入、流匹配损失和对称引导各自带来显著增益，其中流匹配损失对Chamfer距离改善最为关键，对称引导则将强连通分量数（#SCC）从1.49降至1.11，对称Chamfer距离从0.1145降至0.0756（Table 2, Table 3）。在任意视角输入下，方法同样保持可比性能（Table 4），并展示了在Pix3D数据集和Google家具图片上的泛化能力。



从单张图像逆向重建三维CAD模型是计算机图形学与工业设计中的核心难题。与传统的网格或点云重建不同，CAD模型由离散的命令序列（如草图绘制、拉伸、切割）和连续的几何属性（如圆心坐标、半径、拉伸距离）构成，这带来了独特的组合复杂性：离散结构的微小错误会导致完全失效的几何输出，而连续属性的回归又高度依赖于离散结构的正确性。此外，单视角图像固有的信息缺失——遮挡、透视畸变、光照变化——进一步加剧了端到端学习的难度。

现有方法主要采用端到端的神经网络直接回归完整的CAD命令序列。以 **DeepCAD-End2End** 为代表的基线将图像编码为隐特征后，联合预测离散命令类型和连续属性值。这种设计面临两个根本性瓶颈：**数据需求巨大**——模型必须从有限样本中同时学习结构推理与精确几何回归，泛化能力受限；**结构-属性耦合**——离散结构的预测误差会直接传导至属性回归，缺乏显式的错误隔离机制。实验表明，DeepCAD-End2End在椅子、桌子、柜子三类上的平均Chamfer距离高达0.3108，分割准确率和mIoU均显著不足（Table 1）。

视觉语言大模型（VLM）的兴起为解决结构推理问题提供了新的可能。VLM在海量图文数据上预训练，具备强大的语义理解和部分分解能力，能够从单张图像中识别物体的语义部件及其拓扑关系。然而，VLM对连续几何属性的精确预测能力严重不足——它们可以告诉你“椅子有四条腿”，却难以给出每条腿的精确三维位置和尺寸（Fig. 6）。这一观察揭示了问题的本质：**离散结构与连续属性需要不同的推理能力，应当由不同的机制处理**。

基于此，Img2CAD提出**条件分解策略**：将图像到CAD的逆向工程分解为两个条件化的子问题——首先由微调的VLM（Llama3.2）预测带有语义部分标签的离散CAD基础结构，然后由专用的层次Transformer网络（TrAssembler）条件于该结构预测连续属性。这种分解使得属性预测网络可以跨不同对象共享对应部分的属性学习模式（类似层间纤维一致性），大幅降低数据需求并提高泛化性（Fig. 4）。此外，引入流匹配损失和推理时对称引导，进一步解决属性回归的多模态分布问题和输出结构的对称性约束。



## 核心方法与创新机理

Img2CAD 的核心创新在于将图像到 CAD 的逆向工程任务进行**条件分解**（conditional factorization），将原本端到端学习的组合复杂性拆解为两个子问题：首先由视觉语言模型（VLM）预测离散的 CAD 基础结构，然后由专用网络条件于该结构回归连续属性。这一策略从根本上改变了任务的学习范式，带来以下关键改进。

### 1. 条件分解策略：离散-连续解耦

传统端到端方法（如 DeepCAD-End2End）试图直接从图像联合预测离散命令类型和连续属性参数，面临巨大的组合搜索空间和跨模态映射困难。Img2CAD 将这一过程显式分解：

- **离散结构预测**：由微调的 Llama3.2 VLM 接收单张图像，预测 CAD 程序的离散命令类型序列，并为每个部分生成语义标签（如“椅背”、“座面”等）。VLM 的通用视觉理解能力使其能够有效推断全局离散结构和语义分解，无需大量 CAD 配对数据即可泛化。
- **连续属性回归**：条件于 VLM 预测的离散结构，由层次 Transformer 网络（TrAssembler）通过流匹配去噪过程预测连续属性参数。由于离散结构已固定，连续属性的学习空间被大幅缩减，且不同对象间对应部分可以共享属性学习（类似跨纤维一致性），显著降低了数据需求并提高了泛化性。

这一分解的合理性在于：VLM 擅长离散语义推理但难以精确预测连续几何量（如图 6 所示，VLM 端到端预测属性效果极差），而专用网络在条件化后可以高效处理连续回归。消融实验（Table 2, row vii）证实，让 VLM 直接预测属性会导致性能崩溃，验证了分工的必要性。

### 2. 层次 Transformer 与语义条件化

TrAssembler 采用**层次 Transformer 架构**（Fig. 5），包含 Part Transformer Encoder 和 Global Transformer Encoder 两级结构。Part Transformer 首先为每个部件生成部件嵌入，Global Transformer 再通过多头自注意力精炼全局上下文中的部件表示，最后经 MLP 解码各命令的属性参数。消融实验（Table 2, row i→ii）表明，相比扁平结构，层次设计显著改善了部件间的连接性和对称性指标。

此外，VLM 预测的**语义部分标签**被注入 TrAssembler 作为条件信号（Table 2, row iii），使得网络能够利用跨形状的语义一致性——不同椅子的“椅背”共享相似的属性分布（Fig. 4），从而加速学习并提升精度。

### 3. 流匹配损失替代直接回归

传统方法使用 L1/L2 损失直接回归属性，难以捕捉多模态分布和细粒度几何约束。Img2CAD 引入 **GMFlow 流匹配损失**（Equation 1）：

$$\mathcal{L} = \mathbb{E}_{t, \mathbf{x}_0, \mathbf{x}_t} \left[ -\log q \left( \frac{\mathbf{x}_t - \mathbf{x}_0}{t} \bigg\vert \mathbf{x}_t \right) \right]$$

该损失在训练时学习从噪声到目标属性的速度场，推理时通过 ODE 求解器迭代去噪。消融实验（Table 2, row v vs iv）表明，以流匹配替换前馈回归头带来了最大的 Chamfer 距离改善，验证了生成式建模对连续属性预测的关键作用。

### 4. 推理时对称引导

CAD 模型通常具有强对称性，但直接从数据学习对称约束较为困难。Img2CAD 在推理时引入**对称引导损失**（Section 4.3）：由 GPT-4o 识别物体的对称类型，在 ODE 求解器每次步后计算对称损失并梯度更新属性：

$$\mathbf{x}_t = \mathbf{x}_t - \lambda \frac{\partial \mathcal{L}_{\mathrm{sym}}}{\partial \mathbf{x}_t}$$

这一测试时优化将强连通分量数（#SCC）从 1.49 降至 1.11，对称 Chamfer 距离从 0.1145 降至 0.0756（Table 3），显著提升了输出结构的连接完整性和对称性。



Img2CAD 将“单张图像→可编辑CAD程序”的逆向工程任务**条件分解**为两个子问题：首先预测全局离散基础结构，再以该结构为条件回归连续属性参数。这一分解策略的核心动机在于：离散命令序列（如草图类型、挤出操作类型）决定了CAD程序的拓扑骨架，而连续属性（如圆心坐标、半径、挤出距离、欧拉角）则决定了精确的几何形态——两者的组合复杂性是端到端学习的根本瓶颈。

### 两阶段流水线

**第一阶段：VLM离散结构预测器**
输入单视角图像，由微调的视觉语言模型 **Llama3.2** 将图像分解为语义部件，并为每个部件生成带有语义标签的离散CAD命令序列。输出包括：每个部件的草图命令类型（直线、圆弧、圆）和挤出命令类型（新建体/切除），以及对应的语义部件标签（如“椅背”、“座面”、“桌腿”）。该阶段仅预测离散结构，不涉及连续数值。

**第二阶段：TrAssembler连续属性回归**
以同一张图像和第一阶段预测的离散结构为条件，采用基于流匹配的去噪过程预测所有连续属性参数。TrAssembler的核心设计包括：
- **层次Transformer架构**：先由Part Transformer Encoder为每个部件生成嵌入，再通过Global Transformer Encoder利用多头自注意力精炼部件间关系，最后由MLP解码器输出每个命令的属性参数。
- **掩码流匹配损失**：训练时采用GMFlow的流匹配目标，对连续属性施加掩码流匹配损失，使网络学习从噪声到目标属性的条件概率流。
- **语义条件化**：VLM提供的语义部件标签作为条件信号注入TrAssembler，使不同对象间对应语义部件（如不同椅子的“座面”）能够共享属性学习，显著降低数据需求并提升泛化性。

**推理时对称引导模块**
在ODE求解器的每一步迭代后，根据GPT-4o识别的对称类型（如反射对称），计算对称损失并沿梯度方向更新属性参数，以增强输出CAD结构的对称性和连接完整性。

### 数据流概览

单张RGB图像 → **Llama3.2 VLM** → 离散命令序列 + 语义部件标签 → **TrAssembler**（条件于图像特征与离散结构）→ 流匹配去噪采样 → 连续属性参数 → **对称引导**（迭代优化）→ 完整CAD程序 → 通过OpenCasCade转换为可编辑3D网格。

该框架的关键洞察在于：VLM擅长从图像中提取通用离散结构和语义知识，但不擅长精确连续数值预测；而专门训练的Transformer网络在条件化结构下能够高效回归连续属性——二者分工协作，避免了端到端方法对海量配对数据的需求，同时提升了重建精度和泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2408_01437/figures/001_Figure_1.jpg]]
*Figure 1: Img2CAD: a framework for reverse engineering 3D CAD models from single-view images. Our method leverages VLM to predict the discrete CAD program structure and then uses a semantic-conditioned transformer to predict the continuous attributes. This approach allows users to easily reconstruct and edit a CAD model from a single-view input image. We use OpenCasCade [Capgemini [n. d.]] to convert the CAD program back to a 3D mesh*



Img2CAD 将图像到 CAD 的逆向工程分解为两个条件化子任务：离散结构预测与连续属性回归。其核心模块包括 VLM 离散结构预测器、TrAssembler 条件属性回归网络，以及推理时对称引导模块。

### VLM 离散结构预测器

该模块接收单张 RGB 图像，输出 CAD 程序的离散命令类型序列，并为每个几何部分赋予语义标签。具体而言，方法微调 Llama3.2 视觉语言模型，使其将输入图像分解为语义部分（如椅背、椅腿、座面），并生成对应的草图-挤出命令结构。草图命令包括直线、圆弧和圆三类基本图元；挤出命令则指定 NewBody（新增体）或 Cut（切除）等布尔操作类型。这种显式的离散结构预测利用了 VLM 的通用视觉理解能力，避免了端到端网络对离散组合空间的黑盒学习。

### TrAssembler：层次 Transformer 流匹配网络

TrAssembler 以输入图像和 VLM 预测的离散基础结构为条件，通过流匹配去噪过程回归连续属性参数。其架构采用层次 Transformer 设计，包含三个关键子模块：

1. **Part Transformer Encoder**：对每个由 Llama 预测的部分结构进行编码，生成部分嵌入向量。该编码器利用 VLM 提供的语义标签实现跨形状的对应部分共享表示（如图 4 所示，不同椅子的“座面”部分具有相似的属性参数分布）。

2. **Global Transformer Encoder**：接收所有部分嵌入，通过多头自注意力机制建模部分间的全局关系，精细化各部分的特征表示。

3. **MLP Decoder**：将精炼后的部分特征解码为每个命令的连续属性参数。

对于圆的草图命令，连续属性为 $(x, y, r)$，分别表示圆心坐标和半径。对于挤出命令，连续属性为 $E: (\alpha, \theta, \gamma, x, y, z, e)$，其中 $(\alpha, \theta, \gamma)$ 为三个欧拉角，定义挤出坐标系的方向；$(x, y, z)$ 为坐标系原点；$e$ 为挤出距离。

### 掩码流匹配损失

TrAssembler 的训练采用 GMFlow 的掩码流匹配损失，替代传统的前馈回归损失（如 L1/L2）。给定真实属性 $\mathbf{x}_0$ 和噪声样本 $\mathbf{x}_t$，损失函数为流速度的负对数似然：

$$\mathcal{L} = \mathbb{E}_{t, \mathbf{x}_0, \mathbf{x}_t} \left[ -\log q \left( \frac{\mathbf{x}_t - \mathbf{x}_0}{t} \bigg\vert \mathbf{x}_t \right) \right]$$

其中 $t$ 为时间步，$\mathbf{x}_t$ 为加噪后的属性向量。该损失引导网络学习从噪声到真实属性的条件流场，使推理时可通过 ODE 求解器迭代去噪生成精确的连续参数。消融实验（Table 2，行 v 对比行 iv）表明，流匹配损失是 Chamfer 距离改善的最大贡献因素。

### 推理时对称引导

在 ODE 求解器的每一步迭代中，对称引导模块根据 GPT-4o 识别的对称类型计算对称损失 $\mathcal{L}_{\mathrm{sym}}$，并通过梯度下降更新属性向量：

$$\mathbf{x}_t = \mathbf{x}_t - \lambda \nabla \log \mathcal{p}_{\mathrm{sym}}(t) = \mathbf{x}_t - \lambda \frac{\partial \mathcal{L}_{\mathrm{sym}}}{\partial \mathbf{x}_t}$$

其中 $\lambda$ 为引导强度。该机制将属性推向对称流形，显著改善输出 CAD 模型的对称性与连接性。Table 3 显示，对称引导将强连通分量数（#SCC）从 1.49 降至 1.11，对称 Chamfer 距离从 0.1145 降至 0.0756。当前版本仅优化单一对称类型，但已足以产生一致的性能提升。

### 关键设计决策的证据

消融实验（Table 2）系统验证了各模块的必要性：层次 Transformer 设计（行 i→ii）相比扁平结构显著提升连接性和对称性指标；语义部分嵌入（行 iii）进一步改善性能；以流匹配损失替换前馈回归头（行 v）带来最大的 CD 改善；直接使用 VLM 端到端预测连续属性（行 vii）性能显著劣化，证实了 VLM 不适合连续属性预测的结论（Fig. 6 亦定性展示了 VLM 在连续属性预测上的失败案例）。



## 实验与关键发现

Img2CAD 在 CAD-ified ShapeNet 数据集（椅子、桌子、柜子三类）上进行了系统评估。实验从重建精度、语义一致性、结构完整性和跨视角泛化四个维度展开，并与多个基线方法进行对比。

### 6.1 主要定量结果

Table 1 报告了各方法在 CAD-ified 测试集上的平均性能。Img2CAD 在所有指标上均显著优于端到端基线 **DeepCAD-End2End**：

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2408_01437/figures/008_Table_1.jpg]]
*Table 1: Image to CAD reconstruction results comparison on CAD-ified Chair, Table, and Cabinet test dataset*

- **Chamfer Distance (CD)**：从 0.3108 降至 0.1174，降幅达 62.2%。这表明条件分解策略有效缓解了端到端学习中的组合复杂性，重建的 3D 网格与真值在几何上更接近。
- **分割准确率 (Seg Acc)**：相对提升 17.94%，**分割 mIoU** 相对提升 19.03%。这说明 VLM 预测的语义部分标签不仅指导了属性回归，还使得重建结果具备可解释的部件级语义，便于后续编辑。
- 与仅添加流匹配损失的 **DeepCAD+FlowMatching** 相比，Img2CAD 仍保持大幅领先，证明 VLM 提供的离散结构先验是性能提升的核心驱动力，而非单纯依赖更强的生成式损失。
- 以点云为输入的 **DeepCAD+PC** 和 **PointNet+FM** 性能均弱于 Img2CAD，说明从单张 RGB 图像直接推理 CAD 程序结构需要更强的语义理解能力，这正是 VLM 的优势所在。
- 直接提示 **GPT-4o** 预测完整 CAD 程序的结果极差，验证了 VLM 不适合直接回归连续属性（详见 Fig. 6）。

### 6.2 结构质量分析

Table 3 从连通性和对称性两个维度评估重建 CAD 模型的结构完整性：

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2408_01437/figures/012_Table_3.jpg]]
*Table 3: Structural quality analysis: number of strongly connected components (SCC, lower is better) and symmetry chamfer (lower is better)*

- **强连通分量数 (#SCC)**：Img2CAD 的 #SCC 为 1.11，接近理想值 1.0，表明生成的 CAD 程序各部分之间连接紧密，未出现碎片化部件。
- **对称 Chamfer 距离 (SymChamfer)**：Img2CAD 为 0.0756，远低于无对称引导变体的 0.1145。推理时对称引导模块通过梯度下降将属性参数约束到对称流形上，显著改善了输出模型的对称性，尤其对椅子、桌子等强对称人造物效果明显。

### 6.3 消融实验

Table 2 的系统消融揭示了各设计组件的贡献：

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2408_01437/figures/009_Table_2.jpg]]
*Table 2: Ablation study on TrAssembler*

- **层次 Transformer 设计**（行 i → ii）：将扁平 Transformer 替换为包含 Part Transformer 和 Global Transformer 的层次结构后，CD 和分割指标均有改善。Part Transformer 先编码每个部件的局部结构，Global Transformer 再建模部件间关系，这种分层建模更符合 CAD 程序的层次化本质。
- **语义部分嵌入**（行 iii）：在层次 Transformer 基础上注入 VLM 预测的语义标签后，性能进一步提升。Fig. 4 解释了其机制：不同形状的同类部件（如不同椅子的座面）共享相似的属性分布，语义标签使网络能够跨实例共享参数先验，降低了对大规模训练数据的依赖。
- **流匹配损失**（行 iv → v）：将前馈回归头替换为 GMFlow 流匹配损失后，CD 改善最为显著。流匹配通过去噪过程逐步细化连续属性，能够更好地捕捉多模态属性分布，避免前馈回归中的均值化问题。
- **推理时对称引导**（行 vi）：在流匹配 ODE 采样过程中加入对称损失梯度更新，将 #SCC 从 1.49 降至 1.11，SymChamfer 从 0.1145 降至 0.0756。该模块以极小的计算开销显著提升了结构规整性。
- **VLM 端到端预测属性**（行 vii）：让 VLM 直接预测连续属性导致性能急剧下降，验证了 VLM 擅长离散结构推理但缺乏精确连续参数预测能力的核心假设（Fig. 6 提供了定性证据）。

### 6.4 跨视角泛化

Table 4 展示了 Img2CAD 在任意视角输入下的性能。模型仅在正视图中训练，但在任意视角测试集上仍取得 CD 0.1396 的平均结果，与正视图性能（0.1174）差距较小。这表明 VLM 的视觉理解能力具备一定的视角不变性，且 TrAssembler 条件于离散结构后对视角变化具有鲁棒性。Fig. 10 和 Fig. 11 提供了任意视角重建的可视化示例。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2408_01437/figures/013_Figure_10.jpg]]
*Figure 10: Example output visualizations given arbitrary-view inputs. Fig. 11. Example visualizations of reconstruction results from frontal and arbitrary-view inputs*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2408_01437/figures/011_Table_4.jpg]]
*Table 4: Our model achieves comparable performance on arbitrary views. Results are averaged over categories*

### 6.5 失败模式与局限性

Fig. 13 展示了典型失败案例，分析如下：

1. **VLM 结构预测错误**：Llama3.2 可能产生幻觉，遗漏部分结构（如缺失椅子扶手）或生成不合理的命令序列。这源于 VLM 对 3D 几何的隐式理解尚不完善，尤其在遮挡或非典型视角下。
2. **长尾形状属性偏差**：TrAssembler 在处理复杂、长尾分布的形状时，位置属性预测可能不够精确（如 Fig. 13 最右侧示例），导致部件错位或穿透。这与流匹配模型在训练数据稀疏区域的泛化能力有限有关。
3. **单一对称类型限制**：当前仅优化单一对称类型，对于需要多对称轴或非标准对称的复杂对象可能效果有限。

### 6.6 定性结果

Fig. 8 对比了 Img2CAD 与各基线的重建可视化。Img2CAD 生成的 CAD 模型在几何精度、部件完整性和结构规整性上均明显优于 DeepCAD-End2End 和 DeepCAD+FlowMatching，尤其体现在细粒度结构（如椅子靠背的镂空）和对称性保持上。Fig. 12 和 Fig. 14 分别展示了在 Pix3D 数据集和 Google 家具图片上的泛化结果，进一步验证了方法的实用性。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2408_01437/figures/014_Figure_12.jpg]]
*Figure 12: Image to CAD results on Pix3D dataset*



## 定位与知识库关联

### 任务定义与核心瓶颈

Img2CAD 解决的是从单视角图像逆向工程 3D CAD 模型的问题。该任务的核心瓶颈在于：CAD 程序同时包含离散的命令类型序列（如草图命令、挤出操作）和连续的属性参数（如圆心坐标、挤出距离），两者构成一个组合复杂度极高的搜索空间。此外，输入仅为单张 2D 图像，必须从部分观测中推断完整的 3D 几何结构，而光照、视角和噪声变化进一步增加了端到端学习的难度。现有方法要么依赖大量标注数据直接回归 CAD 程序，要么将问题简化为点云重建而丢失 CAD 的可编辑结构，难以兼顾重建精度与结构完整性。

### 条件分解策略与设计动机

Img2CAD 的核心创新在于**条件分解策略**：将图像到 CAD 的逆向工程显式地拆分为两个子问题——首先预测离散的 CAD 基础结构，然后条件于该结构回归连续属性。这一设计基于一个关键洞察：VLM（视觉语言模型）能够从图像中有效地推断通用的离散结构和语义部分标签，但难以精确预测连续数值；而专门的条件化回归网络可以在不同对象间共享对应部分的属性模式（类似层跨纤维一致性），从而大幅降低数据需求并提高泛化能力。

具体而言，Img2CAD 采用微调的 **Llama3.2** VLM 作为第一阶段，接收单张图像并输出带有语义部分标签的离散 CAD 命令序列（如“椅背：草图→挤出 NewBody”，“座面：草图→挤出 NewBody”）。第二阶段引入 **TrAssembler**——一个层次化 Transformer 网络，以图像特征和 VLM 预测的离散结构为条件，通过**流匹配**去噪过程回归连续的属性参数。推理时，额外施加**对称引导**损失，利用 GPT-4o 识别的对称类型对属性进行梯度更新，以增强输出结构的对称性和连接性。

### 与基线方法的关系

Img2CAD 与以下基线方法形成对比，其改进点可归纳为四个关键槽位：

| 槽位 | 基线方法 | Img2CAD 方案 | 证据锚点 |
|------|----------|-------------|----------|
| 离散结构预测 | 端到端神经网络隐式学习（如 **DeepCAD-End2End**） | 微调 VLM（Llama3.2）显式预测，附加语义部分标签 | Section 4.1, Fig.3 |
| 连续属性回归 | 与离散结构联合由单一网络预测 | 条件于 VLM 预测的离散结构，由层次 Transformer（TrAssembler）回归 | Section 4.2, Fig.5 |
| 损失函数 | 直接回归损失（L1/L2） | 掩码流匹配损失（GMFlow） | Equation (1), Section 4.2 |
| 对称约束 | 无 | 推理时对称引导损失，通过 GPT-4o 确定对称类型并优化属性 | Section 4.3 |

**DeepCAD-End2End** 是论文的主要端到端基线，直接以图像为输入回归完整的 CAD 命令序列。Img2CAD 在平均 Chamfer 距离上将其从 0.3108 降至 0.1174（-62.2%），分割准确率相对提升 17.94%，mIoU 相对提升 19.03%（Table 1）。该基线未使用流匹配和对称引导，其性能差距主要源于端到端学习难以同时捕获离散结构和连续属性的复杂耦合关系。

**DeepCAD+FlowMatching** 在 DeepCAD 架构上添加了流匹配损失，但仍未采用条件分解策略。消融实验（Table 2）表明，流匹配损失本身能带来显著的 CD 改善，但若不与条件分解和层次 Transformer 结合，性能仍远低于 Img2CAD。

**GPT-4o** 作为 VLM 基线，被直接提示预测完整的 CAD 程序。实验表明，VLM 虽然能有效分解语义部分，但无法准确预测连续属性（Fig.6），这验证了条件分解策略中将连续属性预测交由专用网络处理的必要性。

**DeepCAD+PC** 和 **PointNet+FM** 分别以点云为输入（而非图像），用于比较模态差异。Img2CAD 在图像输入条件下取得了与这些点云方法可比的性能，表明条件分解策略有效弥补了图像模态的信息损失。

### 消融实验揭示的关键设计因素

消融实验（Table 2, Table 3, Fig.9）系统验证了各设计组件的贡献：

1. **层次 Transformer 设计**（行 i→ii）：将扁平结构替换为 Part Transformer + Global Transformer 的层次架构，显著改善了连接性指标（SCC 降低）和对称性指标（SymChamfer 降低）。这验证了层次化建模对捕获部分间关系的重要性。

2. **语义部分嵌入**（行 iii）：在层次 Transformer 基础上添加 VLM 预测的语义部分标签，进一步提升了各项指标。这支持了“跨形状共享部分语义有助于属性预测”的核心假设（Fig.4）。

3. **流匹配损失**（行 v vs iv）：将前馈回归头替换为 GMFlow 流匹配损失，带来了最大的 CD 改善。流匹配通过建模属性分布而非点估计，能够更好地处理连续属性的多模态不确定性。

4. **对称引导**（行 vi vs v）：推理时对称引导将 SCC 从 1.49 降至 1.11，SymChamfer 从 0.1145 降至 0.0756（Table 3），表明对称约束有效提升了结构的连接性和对称性，且几乎不增加训练成本。

5. **VLM 的角色边界**（行 vii）：尝试让 VLM 端到端预测连续属性（而非仅预测离散结构）导致性能显著下降，进一步证实了 VLM 不适合连续属性预测，条件分解策略的合理性得到强化。

### 适用边界与局限

Img2CAD 的适用性受以下因素限制：

- **VLM 幻觉与结构遗漏**：Llama3.2 可能产生幻觉或遗漏部分结构（Fig.13），导致预测的离散程序不完整。这种错误会传播到第二阶段，TrAssembler 无法恢复缺失的部分。
- **长尾复杂形状的精度下降**：TrAssembler 在处理长尾复杂形状时，位置属性预测可能不够精确（Fig.13 最右），表明当前架构对稀有几何配置的泛化仍有限。
- **单一对称类型假设**：当前方法仅优化单一对称类型（如反射对称），可能无法适应需要多种对称类型组合的复杂对象。
- **推理速度**：流匹配的迭代采样过程导致推理速度较慢，限制了实时应用场景。
- **数据集构建偏差**：CAD-ified 数据集的构建依赖 GPT-4V 的半自动流程，可能引入标注噪声和偏差，影响模型在真实场景中的表现。

### 开放问题

1. **加速推理**：能否利用单步或少量步数的扩散/流匹配方法加速推理过程？
2. **训练时对称约束**：能否在流匹配训练过程中直接施加硬对称约束，而非仅依靠测试时引导？
3. **增强 VLM 的 3D 理解**：如何增强 VLM 的 3D 几何理解能力，以提高离散结构预测的准确性和完整性？
4. **扩展 CAD 操作集**：如何将该方法扩展到更多日常对象类别和更复杂的 CAD 操作（如倒角、旋转、扫掠等）？
5. **数据集质量**：如何量化并减少 GPT-4V 辅助数据集构建的标注噪声与偏差？



## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/Img2CAD_Reverse_Engineering_3D_CAD_Models_from_Images_through_VLM_Assisted_Conditional_Factorization.pdf]]
