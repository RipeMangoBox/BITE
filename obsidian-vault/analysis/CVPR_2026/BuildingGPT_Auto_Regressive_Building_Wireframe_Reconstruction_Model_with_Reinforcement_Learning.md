---
title: "BuildingGPT: Auto-Regressive Building Wireframe Reconstruction Model with Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/BuildingGPT_Auto_Regressive_Building_Wireframe_Reconstruction_Model_with_Reinforcement_Learning.pdf
project_link: null
code_link: "https://github.com/3dv-casia/BuildingGPT/"
aliases:
- BuildingGPT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将任务重新定义为自回归序列生成，并通过分层建筑线框分词（足迹→墙壁→屋顶）为模型提供强烈的结构和语义先验，使自回归模型能够学习序列依赖。
primary_logic: 利用分层分词捕捉建筑线框的结构与语义依赖，结合自回归生成实现端到端重建，并通过 DPO 后训练对齐人类偏好，进一步提升重建的几何精度和拓扑正确性。
claims:
- Table 1 显示 BuildingGPT 在 MunichWF 数据集上全面超越现有最先进方法，取得最优 WED 0.98、CF1 97.4、EF1 94.4 等指标。
- Table 2 的消融实验表明，分层分词和 DPO 后训练各自带来显著的性能提升，验证了每个组件的有效性。
- MunichWF 上 WED = 0.98
- MunichWF 上 CF1 = 97.4
---

# BuildingGPT: Auto-Regressive Building Wireframe Reconstruction Model with Reinforcement Learning

> [!tip] 核心洞察
> 利用分层分词捕捉建筑线框的结构与语义依赖，结合自回归生成实现端到端重建，并通过 DPO 后训练对齐人类偏好，进一步提升重建的几何精度和拓扑正确性。

| 字段 | 内容 |
|------|------|
| 中文题名 | BuildingGPT：自回归建筑线框重建模型与强化学习 |
| 英文题名 | BuildingGPT: Auto-Regressive Building Wireframe Reconstruction Model with Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_BuildingGPT_Auto-Regressive_Building_Wireframe_Reconstruction_Model_with_Reinforcement_Learning_CVPR_2026_paper.html) · [Code](https://github.com/3dv-casia/BuildingGPT/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | BuildingGPT |
| Dataset | MunichWF |

> [!tip] 效果简介
> - MunichWF 上，WED 0.98 vs 1.39 (vanilla tokenization pre-trained) (-0.41)；CF1 97.4 vs 96.0 (vanilla tokenization pre-trained) (+1.4)。

## 概要

从三维点云重建建筑线框是城市场景理解的关键任务，但现有方法面临瓶颈：基于检测或扩散模型的方案往往丢失顶点或边，依赖非端到端的后处理，难以捕捉建筑的全局拓扑结构。**BuildingGPT** 将任务重新定义为自回归序列生成问题，通过**分层建筑线框分词**（足迹→墙壁→屋顶）为模型注入结构与语义先验，使自回归模型能够学习序列依赖。在此基础上，引入基于 **DPO（Direct Preference Optimization）** 的后训练阶段，对齐人类偏好，进一步提升几何精度与拓扑正确性。

在 MunichWF 数据集上，BuildingGPT 全面超越现有最先进方法，取得 WED 0.98、CF1 97.4、EF1 94.4 等最优指标。消融实验证实，分层分词与 DPO 后训练各自带来显著性能增益，验证了每个组件的有效性。

城市三维建模是数字孪生、智慧城市与自动驾驶等应用的基础技术，而建筑作为城市场景中最主要的构成元素，其精确重建一直是该领域的核心挑战。建筑线框（building wireframe）以顶点和边的拓扑结构描述建筑几何，是实现轻量级、结构化建筑表达的关键形式。

现有建筑线框重建方法主要沿三条技术路线展开：**基于顶点检测的方法**（如 **PC2WF**，Liu et al., ICLR 2021）首先从点云中检测候选顶点，再通过后处理步骤连接成边；**基于边检测的方法**（如 **Building3D**，Wang et al., ICCV 2023；**BWFormer**，Liu et al., CVPR 2025）直接预测边及其连接关系；**基于扩散模型的方法**（如 **EdgeDiff**，Liu et al., CVPR 2025）将线框生成建模为去噪扩散过程。这些方法虽然在特定场景下取得了可观效果，但存在一个共同的**结构性瓶颈**：它们或依赖非端到端的后处理来连接检测到的基元，或难以显式建模建筑全局拓扑结构，导致重建结果中频繁出现顶点丢失、边断裂或拓扑错乱等问题。

从任务本质来看，建筑线框天然具有**层次化的结构与语义依赖关系**：足迹（footprint）定义了建筑的平面轮廓，墙壁（wall）从足迹向上延伸形成立面，屋顶（roof）则封闭建筑的顶部结构。这一“足迹→墙壁→屋顶”的层次顺序蕴含了强烈的几何与语义先验，但此前的方法均未有效利用这一结构特性来指导重建过程。

与此同时，自回归序列生成在自然语言处理等领域已展现出强大的序列依赖建模能力。这引出了一个自然的问题：能否将建筑线框重建重新表述为自回归序列生成任务，从而端到端地捕捉建筑的全局拓扑结构？

**BuildingGPT** 正是基于这一动机提出的。该方法将建筑线框重建重新定义为**边序列的自回归生成问题**，并设计了**分层建筑线框分词策略**，将线框按照“足迹→墙壁→屋顶”的层次顺序组织为离散标记序列。这一分词策略为自回归模型提供了强烈的结构与语义先验，使其能够学习序列间的长程依赖关系，从而在生成过程中更好地保持拓扑一致性。在此基础上，BuildingGPT 进一步引入**基于直接偏好优化（DPO）的后训练阶段**，通过构造偏好对数据集并利用强化学习微调，使重建结果与人类对几何精度和拓扑正确性的偏好对齐，有效缓解预训练模型中的局部错误。

简言之，BuildingGPT 的核心创新在于**以层次化分词为桥梁，将自回归序列生成范式引入建筑线框重建**，并通过偏好对齐后训练进一步提升重建质量，为这一任务开辟了全新的技术路径。

## 核心方法与创新机理

BuildingGPT 的核心创新在于将建筑线框重建从传统的检测或扩散范式**重新定义为自回归序列生成问题**，并围绕这一范式转变设计了三个关键机制，形成“范式转变—结构化先验注入—人类偏好对齐”的创新链条。

### 范式转变：从检测/扩散到自回归序列生成

现有方法主要依赖两类范式：**基元检测**（如 **PC2WF** (Liu et al., ICLR 2021)、**Point2Roof** (Li et al., ISPRS 2022)、**Building3D** (Wang et al., ICCV 2023)、**BWFormer** (Liu et al., CVPR 2025)、**PBWR** (Huang et al., CVPR 2024)）直接预测顶点或边，或**扩散生成**（如 **EdgeDiff** (Liu et al., CVPR 2025)）通过去噪过程生成线框。这两类方法共同面临一个结构性瓶颈：它们往往丢失顶点或边，且依赖非端到端的后处理步骤来修复拓扑缺陷，难以捕捉建筑全局拓扑结构。

BuildingGPT 将任务重新表述为：给定输入点云 $P$，自回归地生成建筑线框序列 $S$，其联合概率分布为：

$$Pro(S|P) = \prod_{i=1}^{n_s} Pro(T_i | S_{1:i-1}, P)$$

这一范式转变使得模型能够端到端地学习序列依赖关系，从根本上避免了对后处理的依赖。

### 结构化先验注入：分层建筑线框分词

自回归生成的有效性高度依赖序列的组织方式。基线方法采用简单的“按 z-y-x 升序排列顶点”的朴素分词策略，缺乏对建筑结构的语义理解。BuildingGPT 提出了**分层建筑线框分词**策略，将线框序列按“足迹（Footprint）→ 墙壁（Wall）→ 屋顶（Roof）”的层次组织：

$$B = (F, W, R) = (f_1, ..., f_{n_f}, w_1, ..., w_{n_w}, r_1, ..., r_{n_r})$$

这一设计为自回归模型提供了强烈的结构和语义先验，使模型能够更好地捕捉建筑线框内部的层级依赖关系。消融实验（Table 2）验证了其有效性：仅将朴素分词替换为分层分词，WED 从 1.39 降至 1.19，CF1 从 96.0 提升至 96.7。

### 人类偏好对齐：DPO 后训练

预训练的自回归模型虽然能生成合理的线框，但仍存在局部边缘缺失或错乱等问题。BuildingGPT 引入**直接偏好优化（DPO）后训练**阶段，通过构建偏好对数据集使模型输出对齐人类偏好。具体而言，设计偏好评分函数（PSF）综合 Corner F1、Edge F1 和 Wireframe Edit Distance 三项指标，自动筛选正负样本对，并通过 DPO 损失进行微调：

$$L_{\mathrm{DPO}} = -\log \sigma (\beta \log \frac{\pi_p(y^+|p)}{\pi_r(y^+|p)} - \beta \log \frac{\pi_p(y^-|p)}{\pi_r(y^-|p)})$$

同时引入 NLL 损失 $L_{\mathrm{NLL}} = -\frac{\log \pi_p(y^+|p)}{|y^+|}$ 稳定训练。消融实验表明，在分层分词基础上加入 DPO 后训练，WED 进一步降至 0.98，CF1 提升至 97.4，验证了偏好对齐对重建质量的增益。

### 创新链条总结

BuildingGPT 的三个创新点形成递进关系：**自回归范式**为端到端拓扑学习提供了框架基础；**分层分词**注入建筑结构先验，使序列生成更具语义合理性；**DPO 后训练**则通过人类偏好信号进一步修正局部错误。这一创新链条在 MunichWF 数据集上取得了 WED 0.98、CF1 97.4、EF1 94.4 的最优性能（Table 1），全面超越现有最先进方法。

BuildingGPT 将建筑线框重建任务重新定义为**自回归序列生成问题**，并采用**两阶段训练范式**：预训练与后训练。整体流程如图 2 所示。

**输入与编码。** 原始输入为建筑点云 $P$。点云编码器首先通过最远点采样（FPS）选取 $n_q$ 个查询点，随后利用自注意力和交叉注意力操作，将查询点特征聚合成一个固定长度的全局结构隐码。该隐码作为条件信号，被前置到待生成的线框序列之前。

**分层分词与序列构建。** 线框并非以无序顶点集合表示，而是通过**分层建筑线框分词**策略组织为具有结构与语义先验的序列。具体而言，建筑线框 $B$ 按照足迹（Footprint, $F$）、墙壁（Wall, $W$）、屋顶（Roof, $R$）的语义层级排列：

$$B = (F, W, R) = (f_1, ..., f_{n_f}, w_1, ..., w_{n_w}, r_1, ..., r_{n_r})$$

每条边由六个顶点坐标组成，所有坐标经向量量化后转换为离散标记。这一“足迹→墙壁→屋顶”的顺序为自回归模型提供了强烈的结构依赖关系，使其能够学习序列中远距离标记之间的拓扑约束。

**自回归解码。** 解码器采用基于 OPT 架构的 decoder-only Transformer。给定点云隐码和已生成的标记序列 $S_{1:i-1}$，模型以自回归方式预测下一个标记 $T_i$，其联合概率分布为：

$$\text{Pro}(S|P) = \prod_{i=1}^{n_s} \text{Pro}(T_i | S_{1:i-1}, P)$$

预训练阶段使用标准的交叉熵损失优化该分布：

$$L_{\text{pre}} = \text{CE}(S, S_{\text{gt}})$$

**偏好对齐后训练。** 预训练完成后，引入基于直接偏好优化（DPO）的后训练阶段。首先利用偏好评分函数（PSF）在模型自身生成的候选结果中构建偏好对数据集，其中正样本符合人类对几何精度与拓扑正确性的期望，负样本则包含典型错误（结构细节缺失、边连接不完整、边拓扑混乱，如图 3 所示）。随后，通过 DPO 损失和 NLL 损失的联合优化，使模型输出向人类偏好对齐：

$$L_{\text{pos}} = \mathbb{E}_{(p, y^+, y^-) \sim \mathcal{D}} (L_{\mathrm{DPO}} + L_{\mathrm{NLL}})$$

$$L_{\mathrm{DPO}} = -\log \sigma \left(\beta \log \frac{\pi_p(y^+|p)}{\pi_r(y^+|p)} - \beta \log \frac{\pi_p(y^-|p)}{\pi_r(y^-|p)}\right)$$

$$L_{\mathrm{NLL}} = -\frac{\log \pi_p(y^+|p)}{|y^+|}$$

其中 $\pi_p$ 为当前策略模型，$\pi_r$ 为冻结的参考模型（预训练模型），$\beta$ 控制偏好强度的温度系数。

**模块关系总结。** 四个核心模块形成端到端管线：点云编码器提取全局几何上下文 → 分层分词器将线框结构转化为语义有序的离散序列 → 自回归解码器在隐码条件下逐标记生成线框 → DPO 后训练模块利用偏好对进一步消除局部错误，提升几何精度与拓扑正确性。

![[assets/figures/papers/paper_list_l2714_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_BuildingGPT_Auto_R/figures/001_Figure_1.jpg]]
*Figure 1: Comparisons of different pipelines. Prior works focus on primitive detection (vertex (a) / edge (b)) or edge diffusionbased generation (c). In contrast, BuildingGPT (d) formulates the building wireframe reconstruction task as an edge-sequence autoregressive generation process*

![[assets/figures/papers/paper_list_l2714_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_BuildingGPT_Auto_R/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of BuildingGPT. Our BuildingGPT is trained in two stages. In the first stage, the model is pre-trained in an auto-regressive manner. Given the latent code encoded by the point cloud encoder, the wireframe sequence is generated through next-token prediction. In the second stage, we construct a preference pair dataset using the proposed Preference Score Function (PSF) and post-train the model with Direct Preference Optimization (DPO) to further enhance reconstruction quality*

BuildingGPT 的核心架构由四个功能模块构成，协同完成从点云到建筑线框的自回归重建。

**点云编码器** 负责将非结构化的输入点云压缩为固定长度的全局结构隐码。该模块首先通过最远点采样（FPS）选取 $n_q$ 个查询点，随后利用自注意力和交叉注意力操作，使查询点特征聚合整个点云的信息，最终输出一个紧凑的隐式表示，作为后续自回归生成的条件注入。

**分层分词器** 是方法的关键创新。它将建筑线框显式组织为具有结构与语义先验的序列，遵循“足迹→墙壁→屋顶”的层级顺序。具体而言，一条完整的建筑线框序列 $B$ 定义为：

$$B = (F, W, R) = (f_1, ..., f_{n_f}, w_1, ..., w_{n_w}, r_1, ..., r_{n_r}) = (z_{f_1}^1, y_{f_1}^1, x_{f_1}^1, ..., z_{w_1}^1, y_{w_1}^1, x_{w_1}^1, ..., z_{r_{n_r}}^2, y_{r_{n_r}}^2, x_{r_{n_r}}^2)$$

其中 $F$、$W$、$R$ 分别表示足迹边、墙壁边和屋顶边，每条边由六个顶点坐标（两端点的 $(z, y, x)$）表示。该序列随后被量化为离散标记（tokens），供自回归模型进行下一标记预测。

**自回归解码器** 采用基于 OPT 架构的解码器专用 Transformer。给定点云编码器输出的隐码 $P$ 和已生成的前缀序列 $S_{1:i-1}$，模型通过自回归方式预测下一个标记 $T_i$，其联合概率分布为：

$$Pro(S|P) = \prod_{i=1}^{n_s} Pro(T_i | S_{1:i-1}, P)$$

预训练阶段使用标准的交叉熵损失进行优化：

$$L_{pre} = CE(S, S_{gt})$$

**DPO 后训练模块** 在自回归预训练之后引入，旨在使重建结果进一步对齐人类偏好。该模块首先利用偏好评分函数构建偏好对数据集：

$$PSF = \frac{F_c + F_e}{F_{wed}}$$

该函数综合了角点 F1 分数（$F_c$）、边 F1 分数（$F_e$）和线框编辑距离（$F_{wed}$），得分更高的样本被视为正例。后训练阶段在偏好数据集 $\mathcal{D}$ 上的总损失为：

$$L_{pos} = \mathbb{E}_{(p, y^+, y^-) \sim \mathcal{D}} (L_{\mathrm{DPO}} + L_{\mathrm{NLL}})$$

其中 DPO 损失通过策略模型 $\pi_p$ 与参考模型 $\pi_r$ 的对数概率比来优化偏好对齐：

$$L_{\mathrm{DPO}} = -\log \sigma (\beta \log \frac{\pi_p(y^+|p)}{\pi_r(y^+|p)} - \beta \log \frac{\pi_p(y^-|p)}{\pi_r(y^-|p)})$$

NLL 损失针对正样本计算负对数似然并按序列长度归一化，用于稳定训练：

$$L_{\mathrm{NLL}} = -\frac{\log \pi_p(y^+|p)}{|y^+|}$$

整个两阶段训练流程（预训练 + DPO 后训练）的架构如 Figure 2 所示：第一阶段通过自回归方式从点云隐码生成线框序列，第二阶段利用 DPO 对预训练模型进行偏好微调，以进一步提升重建的几何精度与拓扑正确性。

![[assets/figures/papers/paper_list_l2714_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_BuildingGPT_Auto_R/figures/003_Figure_3.jpg]]
*Figure 3: Examples of the constructed preference pair dataset. Using the Preference Score Function (PSF), the preference pair dataset is constructed in which the positive samples align with human preferences, while the negative ones exhibit representative errors such as: (a) missing structural details, (b) incomplete edge connections, and (c) disordered edge topology. The input point cloud and ground-truth wireframe are overlaid for clearer visualization. Green boxes highlight the differences between the positive and negative samples*

## 实验与关键发现

### 主实验定量对比

BuildingGPT 在 MunichWF 数据集上与现有最先进方法进行了全面对比（Table 1）。结果表明，BuildingGPT 在所有核心指标上均取得最优性能，具体包括：**WED 0.98**、**ACO 0.88**、**CF1 97.4** 和 **EF1 94.4**。对比的基线方法涵盖三类主流范式：基于顶点/边检测的方法如 **PC2WF** (Liu et al., ICLR 2021) 和 **Point2Roof** (Li et al., ISPRS 2022)、基于扩散生成的方法如 **EdgeDiff** (Liu et al., CVPR 2025)，以及混合方法如 **Building3D** (Wang et al., ICCV 2023)、**BWFormer** (Liu et al., CVPR 2025) 和 **PBWR** (Huang et al., CVPR 2024)。BuildingGPT 在几何精度（WED、ACO）和拓扑正确性（CF1、EF1）两个维度上均显著超越这些基线，验证了自回归序列生成范式对建筑线框全局结构建模的优势。

![[assets/figures/papers/paper_list_l2714_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_BuildingGPT_Auto_R/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison between BuildingGPT and baselines. Our model achieves superior performance in both geometric accuracy and topological correctness compared to other state-of-the-art methods. Best results are highlighted in bold font, and the same notation applies to subsequent tables*

> **注意**：由于数据提取限制，Table 1 中各基线的具体数值未能获取，需查阅原文进行人工核实。上表仅展示 BuildingGPT 的最优结果。

### 消融实验

Table 2 系统消融了 BuildingGPT 的两个核心设计：**分层建筑线框分词**和 **DPO 后训练**。基线模型使用 vanilla 分词策略（按 z-y-x 升序排列顶点）进行纯自回归预训练。

![[assets/figures/papers/paper_list_l2714_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_BuildingGPT_Auto_R/figures/006_Table_2.jpg]]
*Table 2: Ablation study on the different components of BuildingGPT. The baseline model is pre-trained with vanilla tokenization which sorts the sequences in ascending z-y-x order*

消融结果揭示了清晰的因果链条：

1. **分层分词的关键作用**：将 vanilla 分词替换为分层分词（足迹→墙壁→屋顶）后，WED 从 1.39 降至 1.19，CF1 从 96.0 提升至 96.7。这一提升源于分层分词为自回归模型提供了强烈的结构和语义先验，使序列中的 token 依赖关系更符合建筑几何的天然层次结构。

2. **DPO 后训练的叠加增益**：在分层分词预训练基础上引入 DPO 后训练，WED 进一步降至 0.98，CF1 提升至 97.4。这表明偏好对齐能够有效修正预训练模型在局部边缘完整性和拓扑一致性上的残余错误。

消融实验的证据链完整且置信度高，明确验证了两个组件各自独立且互补的贡献。

### 扩展实验

Figure 6(a) 展示了模型与数据规模的扩展规律：同时增大模型参数量和训练数据规模能够持续提升重建性能，表明 BuildingGPT 框架具备良好的可扩展性。Figure 6(b) 给出了不同规模模型的具体配置，其中 L、H、Hd 分别表示层数、注意力头数和隐藏维度。

### 鲁棒性分析

Table 3 评估了 BuildingGPT 对输入点云质量退化的鲁棒性。实验通过随机移除点模拟稀疏性，通过高斯扰动引入噪声。结果表明：

![[assets/figures/papers/paper_list_l2714_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_BuildingGPT_Auto_R/figures/012_Table_3.jpg]]
*Table 3: Experiments on the impact of input point cloud quality. Sparsity is simulated by randomly removing points, and noise is introduced via Gaussian perturbations at varying scales*

- **中度退化下性能稳定**：在 25% 和 50% 点移除、噪声尺度为 0.01 和 0.02 的条件下，重建性能保持稳定。
- **极端退化下性能下降**：当点移除比例达到 75% 或噪声尺度增至 0.05 时，性能出现明显下滑（稀疏性 -75% 下 WED 升至 2.68；噪声 0.05 下 WED 升至 2.13）。这一现象揭示了当前模型在严重信息缺失场景下的瓶颈。

### 跨数据泛化

Figure 7 展示了 BuildingGPT 在未见过的 AHN3 数据集上的泛化能力。无需微调，模型重建的线框能够准确捕捉建筑几何结构并保持拓扑一致的连接性。需要注意的是，AHN3 数据集提供的是 mesh 格式的真值，而 BuildingGPT 输出的是线框，因此该对比为定性评估。

### 失败案例分析

Figure 8 展示了 BuildingGPT 的典型失败案例。对于结构复杂的建筑，模型仍会出现**局部边缘缺失**或**边缘拓扑错乱**的问题。这些失败模式与当前分层分词仅覆盖足迹、墙壁和屋顶三类边有关——门窗、楼梯等细粒度构件未被纳入分词体系，导致模型对复杂细节的建模能力不足。

### 实验总结

BuildingGPT 的实验体系覆盖了主结果验证、组件消融、扩展性、鲁棒性和泛化性五个维度，证据链完整。核心结论是：分层分词为自回归序列建模提供了有效的结构先验，DPO 后训练通过偏好对齐进一步消除局部错误，两者协同使 BuildingGPT 在 MunichWF 上取得最优性能。当前主要局限在于复杂结构下的局部失败和分词粒度的限制，这指向了未来构建更大规模精细标注数据集和设计更细粒度分词策略的方向。

## 定位与知识库关联

### 任务范式的代际转换

建筑线框重建（Building Wireframe Reconstruction）经历了从**检测范式**到**生成范式**的演进，BuildingGPT 将这一演进推向自回归序列建模的新阶段。

早期方法以**几何基元检测**为核心。**PC2WF**（Liu et al., ICLR 2021）和 **Point2Roof**（Li et al., ISPRS 2022）分别从点云中检测顶点或边，再通过后处理组装成完整线框。这类方法的根本局限在于检测与组装的解耦：顶点/边的局部预测无法保证全局拓扑一致性，后处理步骤往往依赖手工规则，难以处理复杂屋顶结构。

**扩散模型**的引入代表了第一次范式升级。**PBWR**（Huang et al., CVPR 2024）和 **EdgeDiff**（Liu et al., CVPR 2025）将线框生成建模为去噪扩散过程，实现了端到端的全局生成，避免了显式的后处理组装。然而，扩散模型在建筑线框这类**稀疏、结构化离散序列**上的效率与精度平衡仍存挑战——扩散过程天然适合连续信号，对离散拓扑结构的建模需要额外的技巧。

**BuildingGPT 的核心范式转换**在于将任务重新定义为**自回归序列生成**。这一转换的关键洞察是：建筑线框天然具有层次化结构（足迹→墙壁→屋顶），这种结构依赖可以被自回归模型的序列建模能力所捕获。与检测范式相比，自回归生成是端到端的，无需后处理；与扩散范式相比，自回归模型对离散序列的建模更为自然，且推理效率更高。

### 与检测/扩散路线的关键差异

BuildingGPT 与两类基线方法的本质差异体现在三个维度：

| 维度 | 检测方法（PC2WF, Building3D） | 扩散方法（PBWR, EdgeDiff） | BuildingGPT |
|------|------------------------------|---------------------------|-------------|
| **任务建模** | 局部基元检测 + 后处理组装 | 全局扩散去噪生成 | 自回归序列生成 |
| **结构先验** | 隐式（通过后处理注入） | 隐式（通过扩散条件注入） | 显式（分层分词强制足迹→墙壁→屋顶顺序） |
| **端到端程度** | 非端到端 | 端到端 | 端到端 |
| **推理机制** | 单次前向 + 规则组装 | 多步迭代去噪 | 逐标记自回归解码 |

**Building3D**（Wang et al., ICCV 2023）和 **BWFormer**（Liu et al., CVPR 2025）虽然引入了 Transformer 架构，但仍停留在检测范式的框架内——它们预测的是顶点/边的存在性，而非直接生成完整的线框序列。BuildingGPT 的突破在于**将“检测什么存在”转变为“按什么顺序生成”**，这使得模型能够显式学习建筑结构的序列依赖。

### 分层分词：结构先验的显式注入

BuildingGPT 最具辨识度的设计选择是**分层建筑线框分词**（Hierarchical Building Wireframe Tokenization）。与简单的 z-y-x 升序排列（vanilla tokenization）不同，分层分词将线框序列组织为：

$$B = (F, W, R) = (f_1, ..., f_{n_f}, w_1, ..., w_{n_w}, r_1, ..., r_{n_r})$$

其中 $F$（足迹）、$W$（墙壁）、$R$（屋顶）三类边按语义层次排列，每条边由六个顶点坐标组成。这一设计的因果作用机制在于：**自回归模型的预测质量高度依赖于序列中标记的顺序**。当序列按足迹→墙壁→屋顶排列时，模型在预测墙壁边时可以条件化于已生成的足迹边，预测屋顶边时可以条件化于已生成的足迹和墙壁边——这种条件依赖恰好反映了建筑结构的物理约束。

消融实验（Table 2）验证了这一设计的因果效应：仅将 vanilla tokenization 替换为分层分词，WED 从 1.39 降至 1.19，CF1 从 96.0 提升至 96.7。这 0.20 的 WED 改善和 0.7 的 CF1 提升，完全归因于序列顺序的结构化重组，而非模型容量或训练策略的改变。

### DPO 后训练：从似然最大化到偏好对齐

BuildingGPT 的两阶段训练策略（预训练 + DPO 后训练）借鉴了大语言模型的对齐范式，但在建筑线框重建这一几何任务中赋予了新的内涵。

**预训练阶段**使用标准的交叉熵损失：

$$L_{pre} = CE(S, S_{gt})$$

这一阶段最大化 ground truth 序列的似然，使模型学会生成“平均意义上正确”的线框。

**后训练阶段**引入 DPO，其核心机制是通过偏好对数据优化策略模型：

$$L_{\mathrm{DPO}} = -\log \sigma \left(\beta \log \frac{\pi_p(y^+|p)}{\pi_r(y^+|p)} - \beta \log \frac{\pi_p(y^-|p)}{\pi_r(y^-|p)}\right)$$

偏好对的构建依赖**偏好评分函数**（PSF）：

$$PSF = \frac{F_c + F_e}{F_{wed}}$$

该函数综合了 Corner F1（$F_c$）、Edge F1（$F_e$）和 Wireframe Edit Distance（$F_{wed}$），将几何精度和拓扑正确性统一为标量评分。正样本（高分）代表符合人类偏好的重建，负样本（低分）包含三类典型错误：结构细节缺失、边连接不完整、边拓扑错乱（Figure 3）。

消融实验表明，DPO 后训练在分层分词基础上进一步将 WED 从 1.19 降至 0.98，CF1 从 96.7 提升至 97.4。这 0.21 的 WED 改善揭示了 DPO 的独特价值：**预训练的最大似然目标无法区分不同错误类型的严重程度**，而 DPO 通过偏好对显式地将模型推向“几何更精确、拓扑更正确”的方向。Figure 4 的定性对比进一步显示，DPO 后训练有效修复了预训练模型中的局部错误，如缺失短边和边连接断裂。

### 适用边界与局限

BuildingGPT 的适用边界由以下几个因素界定：

**1. 复杂结构的局部失效。** 对于结构极其复杂的建筑（如多坡屋顶、不规则轮廓），模型仍可能出现局部边缘缺失或错乱（Figure 8）。这表明自回归模型的序列建模能力在极端结构复杂度下仍有瓶颈——当序列长度过长或结构依赖过于复杂时，误差累积效应可能超过模型容量。

**2. 分词粒度的上限。** 当前分层分词仅覆盖足迹、墙壁和屋顶三类边，尚未包含门窗、楼梯等细粒度建筑构件。这一限制源于数据集的标注粒度，也反映了分词策略本身的扩展性挑战：更细粒度的分词需要更长的序列长度和更复杂的层次结构，可能加剧自回归解码的误差累积。

**3. 偏好评分的工程依赖。** PSF 函数依赖 Corner F1、Edge F1 和 WED 的线性组合，权重设计依赖人工经验。这一设计可能无法完全捕捉人类对拓扑正确性的全部期望——例如，某些拓扑错误（如面的错误闭合）可能在 PSF 中得不到充分惩罚。

**4. 数据集规模与泛化。** 尽管 BuildingGPT 在 MunichWF 数据集上表现优异，且对未见过的 AHN3 数据集展现了跨域泛化能力（Figure 7），但数据集规模和标注精细度仍是制约模型性能上限的关键因素。缩放实验（Figure 6a）显示，增大模型和数据规模持续带来性能提升，暗示当前模型尚未达到数据饱和点。

### 开放问题与未来方向

BuildingGPT 开辟了若干值得探索的方向：

- **更大规模、更精细标注的数据集构建**是提升模型泛化能力和覆盖细粒度构件的关键前提。
- **更细粒度的分词策略**可以扩展至门窗、楼梯、烟囱等建筑组件，使自回归模型捕捉更完整的建筑语义层次。
- **超越 DPO 的强化学习方法**（如基于过程奖励的 RLHF 变体）可能进一步提升几何精度，特别是对长序列中误差累积的抑制。
- **极端条件下的鲁棒性增强**：Table 3 显示模型在 75% 点云稀疏度或 0.05 尺度噪声下性能显著下降，设计针对性的鲁棒训练策略是一个实用需求。

## 原文 PDF

![[paperPDFs/CVPR_2026/BuildingGPT_Auto_Regressive_Building_Wireframe_Reconstruction_Model_with_Reinforcement_Learning.pdf]]
