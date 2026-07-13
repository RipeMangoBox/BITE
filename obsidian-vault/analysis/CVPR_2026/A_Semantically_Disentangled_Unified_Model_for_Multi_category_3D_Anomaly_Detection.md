---
title: A Semantically Disentangled Unified Model for Multi-category 3D Anomaly Detection
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/A_Semantically_Disentangled_Unified_Model_for_Multi_category_3D_Anomaly_Detection.pdf
project_link: "https://spoiuy3.github.io/SeDiR/"
code_link: null
aliases:
- SDUMMC3AD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过多分辨率全局特征聚合与类别条件对比学习，显式解耦类别语义并形成清晰的类别流体，使重建过程在高置信的语义身份指导下进行。
primary_logic: 在统一模型中，应当先建立对象的语义身份再进行重建，而非盲目从纠缠特征重建。语义感知的类别解耦能够系统性地提高异常检测的可靠性和泛化性。
claims:
- ICE导致分类分数低的样本重建误差显著升高，验证了语义混淆是重建失败的根本原因。
- CFGT赋予基模型轻微提升，C3L提升O-AUROC 2-3%，GGD再提升1-2%，三者互补。
- 全局token的t-SNE可视化显示类别间簇群清晰分离，且分类准确率高达97.3%（mean pooling仅78.1%）。
- Real3D-AD 上 O-AUROC (mean) = 81.0
---

# A Semantically Disentangled Unified Model for Multi-category 3D Anomaly Detection

> [!tip] 核心洞察
> 在统一模型中，应当先建立对象的语义身份再进行重建，而非盲目从纠缠特征重建。语义感知的类别解耦能够系统性地提高异常检测的可靠性和泛化性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向多类别3D异常检测的语义解耦统一模型 |
| 英文题名 | A Semantically Disentangled Unified Model for Multi-category 3D Anomaly Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25159) · [Project](https://spoiuy3.github.io/SeDiR/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | SeDiR |
| Dataset | Real3D-AD, Anomaly-ShapeNet |

> [!tip] 效果简介
> - Real3D-AD 上，O-AUROC (mean) 81.0 vs 78.2 (MC3D-AD) (+2.8%)；P-AUROC (mean) 80.6 vs 76.8 (MC3D-AD) (+3.8%)。
> - Anomaly-ShapeNet 上，O-AUROC (mean) 93.3 vs 84.2 (second-best, not named) (+9.1% over second best)。

## 概要

多类别统一三维异常检测面临一个根本性瓶颈：**类别间特征纠缠（Inter-Category Feature Entanglement, ICE）**。当单一模型处理多个类别的点云时，不同语义对象的特征在潜空间中高度重叠，导致重建过程错误地借用其他类别的先验，产生语义不一致的几何输出与不可靠的异常分数。

针对这一问题，本文提出**SeDiR**——一个语义解耦的统一三维异常检测框架。其核心洞察是：在统一模型中，重建应当以正确的语义身份为条件，而非盲目地从纠缠特征出发。SeDiR通过三个协同模块实现这一目标：

- **Coarse-to-Fine Global Tokenization (CFGT)**：从多分辨率邻域聚合几何线索，形成类别感知的全局表征；
- **Category-Conditioned Contrastive Learning (C3L)**：利用监督对比学习显式分离类别语义，构建清晰的类别流形；
- **Geometry-Guided Decoder (GGD)**：在注意力机制中注入局部几何偏置，引导语义一致的重建。

在Real3D-AD和Anomaly-ShapeNet两个基准上，SeDiR以统一架构超越了类别专用模型与现有统一模型：物体级AUROC分别提升**2.8%**（81.0 vs. 78.2）和**9.1%**（93.3 vs. 次优84.2），点级AUROC也取得**3.8%**的领先。消融实验证实，C3L贡献最大（+2–3% O-AUROC），GGD进一步带来1–2%增益，三者互补。全局token的t-SNE可视化显示类别间簇群清晰分离，分类准确率达**97.3%**，验证了语义解耦的有效性。

在方法谱系上，SeDiR属于**基于重建的统一异常检测**范式，与MC3D-AD等统一模型形成直接对比，同时与BTF、M3DM、PatchCore、CPMF、IMRNet、Reg3D-AD、Group3AD、R3D-AD、ISMP、PO3AD等类别专用方法构成完整的基准参照系。其关键区分在于：首次将语义解耦作为统一异常检测的核心设计原则，而非依赖记忆库或伪异常生成。



### 3D异常检测的范式演进

工业视觉检测正从二维图像向三维点云快速迁移。点云天然携带精确的几何信息，对光照、视角和表面纹理变化不敏感，因而在制造缺陷检测中展现出独特优势。当前3D异常检测的主流方法可归为两类范式：

**类别专用模型（Category-Specific Models）** 为每个对象类别独立训练一个检测模型。这类方法在特定类别上往往表现优异，但面临两个根本性局限：其一，为每个类别维护独立模型导致部署成本随类别数量线性增长；其二，类别间共享的几何异常模式（如凸起、凹陷、缺失）无法跨类别迁移，限制了数据效率。

**统一模型（Unified Models）** 试图用单一模型处理所有类别，以降低部署复杂度。然而，直接将多类别点云混合训练会引入一个被忽视但致命的瓶颈——**类别间特征纠缠（Inter-Category Feature Entanglement, ICE）**。

### 核心瓶颈：类别间特征纠缠

ICE是统一3D异常检测性能退化的根本原因。当不同类别的点云特征在潜空间中发生重叠时，模型在重建阶段无法确定当前样本的语义身份，从而使用错误的类别先验进行重建。这导致两个连锁后果：

- **语义不一致的几何输出**：模型可能将“鸭子”的几何特征按“鸡”的类别先验重建，产生与输入几何不一致的输出；
- **不可靠的异常分数**：正常样本因语义混淆而产生高重建误差，被误判为异常（假阳性）；真实异常则可能因错误的类别先验而被“修正”，导致漏检（假阴性）。

Figure 2 的t-SNE可视化与定量分析直接验证了这一机制：在MC3D-AD（统一模型基线）中，相似类别（如chicken、duck、gemstone）的特征簇高度纠缠；分类置信度低的样本重建误差显著升高，成为假阳性的主要来源。这表明，**语义混淆是重建失败的根本原因**。

### 现有方法的缺口

现有3D异常检测方法在设计上均未显式处理ICE问题：

- **重建类方法**（如BTF、IMRNet、Reg3D-AD、R3D-AD）依赖类别专用的编码器-解码器，天然回避了多类别纠缠，但丧失了统一模型的效率优势；
- **记忆库类方法**（如PatchCore、ISMP）存储类别特定的正常特征，同样无法跨类别泛化；
- **伪异常类方法**（如PO3AD）在训练时模拟异常，但仍在单类别设定下运作；
- **统一模型MC3D-AD**首次尝试多类别联合训练，但仅使用局部特征进行重建，缺乏显式的语义解耦机制，因此成为ICE的典型受害者。

### 本文动机：从“盲目重建”到“语义感知重建”

上述分析揭示了一个核心洞察：**在统一模型中，应当先建立对象的语义身份再进行重建，而非盲目从纠缠特征重建。** 我们将统一3D异常检测重新表述为语义条件重建问题，并提出**语义解耦重建（Semantically Disentangled Reconstruction）** 范式（Figure 1(c)）。该范式的关键转变在于：

- 通过聚合多分辨率几何线索形成**类别感知的全局表征**，而非仅依赖局部点特征；
- 显式解耦类别语义，使潜空间形成**清晰的类别流体**；
- 在解码阶段注入**几何先验**，确保重建输出与输入几何保持一致。

在此范式下，本文提出SeDiR框架，通过三个互补模块——CFGT、C3L和GGD——系统性地解决ICE问题，使统一模型在保持部署效率的同时，达到甚至超越类别专用模型的检测精度。



## 核心方法与创新机理

SeDiR 的核心创新在于将统一多类别 3D 异常检测重新定义为**语义条件重建**问题，并围绕“先建立语义身份，再执行重建”这一洞察，设计了三个相互协同的模块，系统性地解决了统一模型中普遍存在的**类别间特征纠缠（ICE）**瓶颈。

### 1. 从纠缠特征到语义解耦重建：范式转变

现有统一模型（如 MC3D-AD）直接将多类别点云送入共享编码器-解码器，不同类别的特征在潜空间高度重叠。当分类置信度低的样本进入重建阶段时，解码器在不确定的语义先验下工作，产生语义不一致的几何输出，导致正常样本重建误差偏高、异常分数不可靠（Figure 2）。SeDiR 的范式转变在于：**重建过程必须由正确解耦的类别级语义来条件化**，而非盲目从纠缠特征中重建。

### 2. 三个关键 changed slots

相较于基线统一模型，SeDiR 在以下三个关键环节实现了结构性改变：

**Slot 1：全局表征 — 从简单池化到多分辨率类别感知全局 token**

基线方法通常采用 mean/max pooling 或缺乏显式全局 token，导致实例级语义身份模糊。SeDiR 提出 **Coarse-to-Fine Global Tokenization (CFGT)**，在三个对称分辨率（k/2, k, 2k）上提取邻域特征，通过跨尺度余弦对齐损失（公式 4）保持一致性，并引入可学习的 Adaptive Context Token (ACT) 聚合实例级上下文。最终将多分辨率池化特征与 ACT 拼接后经 MLP 投影、L2 归一化，形成类别感知的全局表征（公式 5, 7）。消融实验表明，ACT 的分类准确率达 **97.3%**，远超 mean pooling 的 78.1% 和 max pooling 的 77.3%（Table S8），证明其对类别语义的强辨别力。

**Slot 2：语义解耦 — 从无解耦机制到类别条件对比学习**

基线统一模型缺乏显式解耦机制，特征是自然纠缠的。SeDiR 引入 **Category-Conditioned Contrastive Learning (C3L)**，利用类别标签构建动态缓冲区（L=64），执行监督对比学习（公式 8），强制类内紧凑、类间分离。C3L 的总目标（公式 9）联合优化对比损失、分类损失和余弦对齐损失。这是三个组件中贡献最大的：**C3L 单独提升 O-AUROC 2–3%**（Table 4），且 t-SNE 可视化显示类别间簇群清晰分离（Figure S1），验证了显式语义解耦的有效性。

**Slot 3：解码器引导 — 从标准 Transformer 解码器到几何引导解码器**

基线解码器仅依赖学习到的注意力模式，缺乏对局部几何结构的感知。SeDiR 提出 **Geometry-Guided Decoder (GGD)**，在交叉注意力逻辑中直接加入局部几何偏置项 B_geo（包含法向量差异和曲率变化，公式 10），使解码器在全局语义 token 的查询下，优先关注几何一致的区域。消融实验证实，Bias 策略优于 Mask 和 Gate 等替代方案（Table 6），**GGD 在 C3L 基础上再提升 O-AUROC 1–2%**（Table 4），实现了语义与几何一致的重建。

### 3. 模块协同与证据强度

三个模块形成递进式协同：CFGT 提供高质量的类别感知全局表征（基础），C3L 在此基础上显式分离类别语义（核心增益），GGD 在解耦语义的指导下结合几何先验完成精确重建（精细优化）。Table 4 的消融实验清晰展示了这一叠加效应：基模型 + CFGT 带来轻微提升，+ C3L 提升 2–3%，+ GGD 再提升 1–2%，最终在 Real3D-AD 上达到 **81.0% O-AUROC**，较 MC3D-AD 提升 2.8%。

**证据强度评估**：ICE 作为瓶颈的因果证据来自 Figure 2 的定量分析（分类分数低的样本重建误差显著升高），置信度高。C3L 作为最大贡献因子的结论由 Table 4 和 Table 5 的消融实验直接支持，置信度高。GGD 中 Bias 策略的优势由 Table 6 验证，置信度高。三个模块的互补性由 Table 4 的递进式消融支持，置信度高。

### 4. 局限性

尽管语义解耦设计带来了显著的跨类别稳定性提升，SeDiR 并非在每个类别上都超越 MC3D-AD，反映了类别感知泛化与类别特定特化之间的固有权衡。此外，C3L 依赖类别标签进行对比学习，在完全无标签的开放类别场景中不可直接迁移。计算开销方面，SeDiR 的 FLOPs 为 508.25G，略高于 MC3D-AD 的 439.21G（Table S1），存在进一步优化的空间。



SeDiR 将统一 3D 异常检测重新表述为**语义条件重建**问题，其核心流程分为两个阶段：**语义解耦表征学习**与**语义解耦重建**（Figure 3）。给定一个输入点云，系统首先建立其类别语义身份，再在该语义的指导下进行几何重建，从而避免因类别间特征纠缠（ICE）导致的语义不一致输出。

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/003_Figure_3.jpg]]
*Figure 3: The overview of the proposed method. Our method consists of two main stages: Semantically Disentangled Representation Learning and Semantically Disentangled Reconstruction. Given an input point cloud, CFGT encodes multi-resolution geometric features into a category-aware global token, C3L disentangles the latent semantics, and GGD reconstructs the object conditioned on these disentangled semantics and geometric priors*

### 输入与数据组织

训练集由多个类别的正常点云组成，形式为 $\mathcal{D}_{\mathrm{train}}^{c} = \{ P_q^{c} \}_{q=1}^{\bar{M}_c}$，其中 $P_q^{c} \in \mathbb{R}^{N \times 3}$。测试时，每个样本附带异常标签 $t_q^{c} \in \{0,1\}$。模型在所有类别上联合训练，但仅在正常样本上学习，不接触异常数据。

### 阶段一：语义解耦表征学习

该阶段的目标是从原始点云中提取一个**类别感知的全局表征**，并显式地将不同类别的语义在潜空间中分离。

1. **多分辨率局部编码**：使用预训练的 PointMAE 作为局部编码器 $E$，对输入点云中均匀采样的 $g$ 个中心点 $\mathbf{s}_m$ 提取多尺度邻域特征。以基础邻域大小 $k$ 为中心，定义对称分辨率集合 $\mathcal{R} = \{k/2, k, 2k\}$，对每个分辨率 $r$ 计算：
   $$
   \mathcal{N}_r(\mathbf{s}_m) = \mathrm{kNN}(\mathbf{s}_m; r), \quad \mathbf{f}_m^{(r)} = E\big(\mathcal{N}_r(\mathbf{s}_m)\big)
   $$
   由此获得细粒度（$k/2$）、基础（$k$）和粗粒度（$2k$）三个尺度的特征序列 $\mathbf{F}^{(r)}$。

2. **由粗到细的全局 Token 化（CFGT）**：引入一个可学习的 Adaptive Context Token（$\mathbf{t}_{\mathrm{act}}$），将其前置到基础分辨率特征序列中，通过自注意力聚合实例级全局上下文。同时，对三个分辨率的特征分别进行池化，得到多尺度全局描述子 $\mathbf{g}^{(k/2)}, \mathbf{g}^{(k)}, \mathbf{g}^{(2k)}$。跨尺度余弦对齐损失 $\mathcal{L}_{\mathrm{cos}}$ 强制基础分辨率 token 与细/粗尺度 token 保持一致。最终，全局表征由拼接与投影得到：
   $$
   \mathbf{f}_{\mathrm{global}} = \mathrm{concat}\big([\mathbf{g}^{(k)}, \mathbf{g}^{(2k)}, \mathbf{g}^{(k/2)}, \mathbf{t}_{\mathrm{act}}^{\mathrm{enc}}]\big)
   $$
   经两层 MLP 投影器（LayerNorm + GeLU）映射为 $\mathbf{z} \in \mathbb{R}^{d_z}$ 并 L2 归一化。该 $\mathbf{z}$ 即为类别感知的全局语义 token。

3. **类别条件对比学习（C3L）**：利用类别标签构造监督对比损失 $\mathcal{L}_{\mathrm{scl}}$，配合一个动态缓冲区（大小 $L=64$）提供正负样本，强制类内紧凑、类间分离。C3L 的总目标联合优化对比损失、分类损失和余弦对齐损失：
   $$
   \mathcal{L}_{\mathrm{C3L}} = \lambda_{\mathrm{scl}} \mathcal{L}_{\mathrm{scl}} + \lambda_{\mathrm{cls}} \mathcal{L}_{\mathrm{cls}} + \lambda_{\mathrm{cos}} \mathcal{L}_{\mathrm{cos}}
   $$
   这一阶段输出的解耦全局 token $\mathbf{z}$ 将作为后续重建的条件信号。

### 阶段二：语义解耦重建

重建阶段以第一阶段产生的语义 token 为查询，在输入几何的引导下恢复完整的局部特征序列。

1. **几何引导解码器（GGD）**：以全局语义 token $\mathbf{z}$ 作为 Transformer 解码器的查询（Query），以基础分辨率局部特征 token 作为键（Key）和值（Value）。在标准注意力逻辑中显式注入局部几何偏置 $\mathbf{B}_{\mathrm{geo}}$（由法向量和曲率变化构成）：
   $$
   \mathrm{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \mathrm{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}} + \beta \mathbf{B}_{\mathrm{geo}}\right) \mathbf{V}
   $$
   该偏置引导注意力权重朝向几何一致的区域，使重建结果同时忠于语义身份和输入几何。

2. **重建损失**：对重建后的特征 token $\hat{\mathbf{F}}^{(k)}$ 与原始编码特征 $\mathbf{F}^{(k)}$ 计算 MSE：
   $$
   \mathcal{L}_{\mathrm{rec}} = \frac{1}{g} \sum_{j=1}^{g} \|\hat{\mathbf{f}}_j^{(k)} - \mathbf{f}_j^{(k)}\|_2^2
   $$

### 联合训练与推理

整体训练目标将语义解耦与重建统一优化：
$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{C3L}} + \mathcal{L}_{\mathrm{rec}}
$$

推理时，异常评分基于重建误差：对逐点 L2 距离进行归一化与高斯平滑后，取最大值作为物体级异常分数 $S_{\mathrm{obj}}$，逐点分数则直接用于异常定位。这一流程确保了模型在统一的架构下，对多类别输入均能产生语义一致、几何精确的重建，从而给出可靠的异常判断。



SeDiR 的核心由三个模块串联构成：**多尺度全局特征聚合（CFGT）**、**类别条件对比解耦（C3L）** 以及 **几何引导解码器（GGD）**。三者共同实现“先建立语义身份，再执行几何重建”的范式，从根本上缓解统一模型中的类别间特征纠缠（ICE）问题。

### 3.1 多尺度全局特征聚合（CFGT）

给定输入点云，首先通过最远点采样（FPS）选取 $g$ 个中心点 $\{\mathbf{s}_m\}_{m=1}^g$。对每个中心点，以基础邻域大小 $k$ 为基准，定义一组对称的多分辨率半径 $R = \{k/2, k, 2k\}$，利用预训练的 PointMAE 编码器 $E$ 提取多尺度局部几何特征：

$$\mathcal{N}_r(\mathbf{s}_m) = \mathrm{kNN}(\mathbf{s}_m; r), \quad \mathbf{f}_m^{(r)} = E\big(\mathcal{N}_r(\mathbf{s}_m)\big) \tag{1}$$

其中 $\mathcal{N}_r(\mathbf{s}_m)$ 为以 $\mathbf{s}_m$ 为中心、半径 $r$ 内的 $k$ 近邻点集。各分辨率下的特征序列记为 $\mathbf{F}^{(r)} = [\mathbf{f}_1^{(r)}, \dots, \mathbf{f}_g^{(r)}]$。

为形成实例级语义身份，引入一个可学习的 **自适应上下文 token** $\mathbf{t}_{\mathrm{act}}$，将其前置拼接到基分辨率 $k$ 的特征序列中，经 Transformer 编码器交互后，取出编码后的 ACT token $\mathbf{t}_{\mathrm{act}}^{\mathrm{enc}}$。同时，对各分辨率特征序列进行池化，得到多尺度池化向量 $\mathbf{g}^{(r)}$。为保证跨尺度语义一致性，施加余弦对齐损失：

$$\mathcal{L}_{\mathrm{cos}} = \frac{1}{g}\sum_{m=1}^{g}\sum_{r\in\{k/2,2k\}}\Big[1 - \cos\big(\tilde{\mathbf{f}}_m^{(k)}, \tilde{\mathbf{f}}_m^{(r)}\big)\Big] \tag{4}$$

其中 $\tilde{\mathbf{f}}_m^{(r)}$ 为投影后的特征。最终，将多尺度池化向量与编码后的 ACT token 拼接，形成全局表征：

$$\mathbf{f}_{\mathrm{global}} = \mathrm{concat}\big([\mathbf{g}^{(k)}, \mathbf{g}^{(2k)}, \mathbf{g}^{(k/2)}, \mathbf{t}_{\mathrm{act}}^{\mathrm{enc}}]\big) \tag{5}$$

该全局表征经两层 MLP 投影器（含 LayerNorm 与 GeLU）映射至 $d_z$ 维，并进行 L2 归一化：

$$\mathbf{z} = \mathrm{Proj}(\mathbf{f}_{\mathrm{global}}), \quad \mathbf{z} = \frac{\mathbf{z}}{\|\mathbf{z}\|_2} \tag{7}$$

### 3.2 类别条件对比学习（C3L）

C3L 的目标是显式分离不同类别的语义表征。维护一个动态缓冲区 $\bar{\mathbf{B}} = \{(\mathbf{z}_j, c_j)\}_{j=1}^{L}$（$L=64$），存储历史样本的归一化全局 token 及其类别标签。对当前样本 $i$，定义正样本集合 $\mathcal{P}(i)$（同类别）和负样本集合 $\mathcal{A}(i)$（异类别），计算监督对比损失：

$$\mathcal{L}_{\mathrm{scl}}(i) = \frac{1}{|\mathcal{P}(i)|}\sum_{\mathbf{z}_{pos}\in\mathcal{P}(i)} -\log\frac{\exp(\mathbf{z}_i^{\top}\mathbf{z}_{pos}/\tau)}{\sum_{\mathbf{z}_a\in\mathcal{A}(i)}\exp(\mathbf{z}_i^{\top}\mathbf{z}_a/\tau)} \tag{8}$$

其中 $\tau$ 为温度系数。C3L 的总目标联合优化对比损失、分类损失与跨尺度对齐损失：

$$\mathcal{L}_{\mathrm{C3L}} = \lambda_{\mathrm{scl}}\mathcal{L}_{\mathrm{scl}} + \lambda_{\mathrm{cls}}\mathcal{L}_{\mathrm{cls}} + \lambda_{\mathrm{cos}}\mathcal{L}_{\mathrm{cos}} \tag{9}$$

消融实验表明，最优权重组合为 $\lambda_{\mathrm{scl}}=0.001$、$\lambda_{\mathrm{cos}}=0.001$、$\lambda_{\mathrm{cls}}=0.01$（Table S7）。该模块贡献了 2–3% 的 O-AUROC 提升（Table 4），是缓解 ICE 的核心机制。

### 3.3 几何引导解码器（GGD）

GGD 以解耦后的全局语义 token 为查询 $\mathbf{Q}$，以局部特征序列为键 $\mathbf{K}$ 和值 $\mathbf{V}$，并在标准注意力逻辑中加入局部几何偏置 $\mathbf{B}_{\mathrm{geo}}$（由法向差异与曲率变化构成），引导解码器朝向几何一致的重建：

$$\mathrm{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \mathrm{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}} + \beta\mathbf{B}_{\mathrm{geo}}\right)\mathbf{V} \tag{10}$$

其中 $\beta$ 为可学习缩放因子。消融实验证实，Bias 策略优于 Mask、Gate 等替代方案（Table 6）。解码器输出重建特征 token $\hat{\mathbf{f}}_j^{(k)}$，通过 MSE 损失约束重建质量：

$$\mathcal{L}_{\mathrm{rec}} = \frac{1}{g}\sum_{j=1}^{g}\|\hat{\mathbf{f}}_j^{(k)} - \mathbf{f}_j^{(k)}\|_2^2 \tag{11}$$

整体训练目标将语义解耦损失与重建损失合并：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{C3L}} + \mathcal{L}_{\mathrm{rec}} \tag{12}$$

### 3.4 异常评分

推理时，计算原始特征与重建特征的逐点 L2 距离，经归一化与高斯平滑后，取最大值作为物体级异常分数：

$$\mathbf{S}_p = \mathrm{Gauss}_{k_g,\sigma}\Big(\mathrm{Norm}\big(\|\hat{\mathbf{F}}^{(k)} - \mathbf{F}^{(k)}\|_2\big)\Big), \quad S_{\mathrm{obj}} = \max(\mathbf{S}_p) \tag{13}$$

其中 $k_g$ 和 $\sigma$ 为高斯核参数。逐点分数 $\mathbf{S}_p$ 同时用于异常区域定位。

### 补充图表

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/004_Figure_4.jpg]]
*Figure 4: Overview of the Geometry-Guided Decoder (GGD). Geometric priors*



## 实验与关键发现

### 主实验结果

#### Real3D-AD 数据集

Table 1 报告了 Real3D-AD 数据集 12 个类别上的物体级 AUROC 对比。在统一模型设置下，SeDiR 取得 **81.0%** 的平均 O-AUROC，相比统一基线 MC3D-AD（78.2%）提升 **+2.8%**。值得注意的是，SeDiR 以统一架构超越了所有类别专用方法（上栏），包括基于记忆库的 PatchCore（FPFH 特征 73.9%、PointMAE 特征 76.1%）和重建类方法 IMRNet（76.9%）。

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of AUROC (%) at the object levels on Real3D-AD across 12 categories. The best and second-best results are highlighted in bold and underline, respectively. Methods in the upper block are trained and evaluated in the single-category setting, while methods in the lower block use a unified model for the multi-category setting across all 12 categories*

Table 3 给出的点级异常定位结果中，SeDiR 平均 P-AUROC 达到 **80.6%**（Table S9 提供逐类别详情），较 MC3D-AD（76.8%）提升 **+3.8%**。定位能力在统一模型中排名第二，仅次于依赖记忆库的 ISMP（82.0%），表明语义解耦对细粒度重建误差度量的正向作用，但记忆库方法在逐点判别上仍具一定优势。

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/008_Table_3.jpg]]
*Table 3: Comparison of mean point-level AUROC (%) on Real3D-AD and Anomaly-ShapeNet datasets. The detailed per-category results are provided in the supplementary*

#### Anomaly-ShapeNet 数据集

在 40 类物体的 Anomaly-ShapeNet 上，SeDiR 取得 **93.3%** 的物体级 AUROC（Table 2），超过第二名 **+9.1 个百分点**。该结果验证了语义解耦策略在大规模多类别场景下的泛化优势。点级 AUROC 同样达到第二优水平（Table 3），详细逐类别数据见 Table S10，AUPR 指标见 Table S11。

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/006_Table_2.jpg]]
*Table 2: Comparison of object-level AUROC (%) of various methods on the Anomaly-ShapeNet*

#### 定性分析

Figure 5 展示了与 MC3D-AD 在 Real3D-AD 上的定性对比。MC3D-AD 常遗漏真实异常区域（如凸起、凹陷）或产生误报，而 SeDiR 的异常热力图与真值标注更一致，定位更精确完整。Anomaly-ShapeNet 上的更多定性对比见 Figure S2。

### 消融实验

#### 核心组件消融

Table 4 系统剥离了 CFGT、C3L、GGD 三个核心模块。以仅含局部特征与标准 Transformer 解码器的基模型为起点（O-AUROC 约 75%），依次启用各组件：

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/007_Table_4.jpg]]
*Table 4: Ablation studies on the effectiveness of core components*

- **CFGT**：引入多分辨率聚合与自适应上下文 token（ACT），带来轻微但稳定的性能增益，验证了类别感知全局表征对重建的辅助作用。
- **C3L**：贡献最为显著，O-AUROC 提升 **2–3%**。该增益直接归因于对比学习对类别语义的显式解耦——类内紧凑、类间分离的嵌入空间有效缓解了 ICE 问题。
- **GGD**：在 C3L 基础上再提升 **1–2%**，证明几何偏置引导注意力可使重建在语义正确的前提下保持几何一致性。

三者互补，最终达到 81.0% O-AUROC。

#### C3L 损失项消融

Table 5 拆解了 C3L 的三个损失项。监督对比损失 $\mathcal{L}_{\mathrm{scl}}$ 是主要驱动力，单独使用即可大幅提升性能；分类损失 $\mathcal{L}_{\mathrm{cls}}$ 和余弦对齐损失 $\mathcal{L}_{\mathrm{cos}}$ 各自提供额外增益。Table S7 给出最佳权重组合：$\lambda_{\mathrm{scl}}=0.001$，$\lambda_{\mathrm{cos}}=0.001$，$\lambda_{\mathrm{cls}}=0.01$。

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/009_Table_5.jpg]]
*Table 5: Ablation studies on the contribution of each loss in C3L*

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/020_Table_S.7.jpg]]
*Table S.7: Comparison of different loss weights in C3L*

#### 全局表征策略对比

Table 7 比较了不同全局 token 生成策略。**自适应上下文 token（ACT）** 的分类准确率达 **97.3%**，远超 mean pooling（78.1%）和 max pooling（77.3%），证明 ACT 对类别语义具有强辨别力。Table S8 和 Figure S1 的 t-SNE 可视化进一步确认：ACT 学习到的全局 token 在 Real3D-AD（12 类）和 Anomaly-ShapeNet（40 类）上均形成清晰分离的簇，而 mean/max pooling 的特征分布则高度重叠。

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/012_Table_7.jpg]]
*Table 7: Comparison of different global token strategies*

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/021_Table_S.8.jpg]]
*Table S.8: Category prediction accuracy with different global representations*

#### GGD 几何引导策略

Table 6 对比了三种几何信息融入方式：Mask（掩码）、Gate（门控）和 Bias（偏置）。直接以几何偏置 $\mathbf{B}_{\mathrm{geo}}$ 加入注意力 logits 的 Bias 策略优于 Mask 和 Gate，验证了在注意力计算中显式注入局部几何先验（法向、曲率变化）对重建质量最为有效。

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/011_Table_6.jpg]]
*Table 6: Comparison of different guidance strategies in GGD*

#### 超参数消融

补充材料中报告了多项超参数敏感性分析：CFGT 与 C3L 损失联合消融（Table S2）、不同粗细邻域比例（Table S3）、基础邻域大小 $k$（Table S4）、分组数量（Table S5）、C3L 动态缓冲区大小（Table S6）。总体而言，方法对超参数选择具有较好的鲁棒性，最佳配置下缓冲区大小 $L=64$。

### 计算开销与泛化—特化权衡

Table S1 比较了计算开销。SeDiR 的 FLOPs 为 508.25G，略高于 MC3D-AD（439.21G），增量主要来自多分辨率编码与几何偏置计算。

![[assets/figures/papers/paper_list_l2435_https_arxiv_org_abs_2603_25159/figures/013_Table_S.1.jpg]]
*Table S.1: Comparison of computational cost*

公平性方面，所有方法均仅在正常样本上训练，数据划分与评估协议一致。SeDiR 并非在每个类别上都超越 MC3D-AD，但跨类别方差显著更低，表现更稳定。这反映了类别感知泛化与类别特定特化之间的固有权衡：语义解耦统一模型牺牲了个别类的极致优化，换取了整体鲁棒性和部署的简洁性。

### 方法局限性

1. **泛化—特化权衡**：如上述，个别类别性能未达最优，语义解耦带来的类间分离可能对某些视觉相似类别（如“鸡”与“鸭”）的细粒度判别产生轻微负面影响。
2. **计算开销**：相比 MC3D-AD，FLOPs 增加约 15.7%，在资源受限的工业边缘设备上需进一步轻量化。
3. **点级定位上限**：点级 AUROC 仍次于 ISMP 等记忆库方法，表明单纯依赖重建误差的逐点度量在细粒度异常边界刻画上存在改进空间。
4. **对类别标签的依赖**：C3L 依赖类别标签进行监督对比学习，在完全无标签的开放类别场景中无法直接迁移，限制了方法在未知异常类别检测中的适用性。



## 定位与知识库关联

### 问题定位：统一模型中的类别间特征纠缠

3D异常检测领域长期遵循“每类一模型”的范式，代表性方法包括基于重建的 **BTF**（使用Raw/FPFH特征）、**IMRNet**、**Reg3D-AD**、**R3D-AD**，基于记忆库的 **PatchCore**（FPFH/PointMAE特征）、**ISMP**，以及基于伪异常的 **PO3AD** 等。这些方法在各自类别上表现良好，但需要为每个类别单独训练和部署模型，随着类别数增加，存储和计算开销线性增长。

统一模型试图用一个架构处理所有类别，**MC3D-AD** 是该方向的代表性基线。然而，统一模型面临一个核心瓶颈——**类别间特征纠缠（Inter-Category Feature Entanglement, ICE）**：不同类别的点云特征在潜空间中重叠，导致重建时使用了错误的类别先验，产生语义不一致的几何输出与不可靠的异常分数。Figure 2 的 t-SNE 可视化清晰展示了这一问题——MC3D-AD 在相似类别（如 chicken、duck、gemstone）之间的特征簇高度混合，分类分数低的样本重建误差显著升高，验证了语义混淆是重建失败的根本原因。

### SeDiR 的核心设计：语义解耦重建范式

SeDiR 将统一3D异常检测重新定义为**语义条件重建问题**，提出“语义解耦重建”范式。其核心洞察是：在统一模型中，应当先建立对象的语义身份再进行重建，而非盲目从纠缠特征重建。这一范式通过三个互补模块实现：

1. **Coarse-to-Fine Global Tokenization (CFGT)**：通过多分辨率邻域编码（基分辨率 $k$ 及对称尺度 $k/2$、$2k$）聚合几何线索，结合可学习的 Adaptive Context Token (ACT)，形成类别感知的全局表征。相比于基线方法中无显式全局 token 或仅用简单池化的做法，CFGT 使全局表征的分类准确率达到 97.3%（mean pooling 仅 78.1%，Table S8）。

2. **Category-Conditioned Contrastive Learning (C3L)**：利用类别标签执行监督对比学习，通过动态缓冲区（大小 $L=64$）构建正负样本对，强制类内紧凑、类间分离。C3L 是性能提升的最大贡献者，单独带来 2–3% 的 O-AUROC 提升（Table 4）。

3. **Geometry-Guided Decoder (GGD)**：在标准 Transformer 解码器的注意力逻辑中加入局部几何偏置 $\mathbf{B}_{\mathrm{geo}}$（法向、曲率变化），引导解码器朝向几何一致的重建。相比于基线中无几何先验的标准解码器，GGD 再带来 1–2% 的提升。消融实验表明，几何偏置（Bias）策略优于 Mask、Gate 等替代方案（Table 6），验证了直接用几何信息引导注意力的有效性。

### 方法谱系中的位置

SeDiR 处于**类别专用模型与统一模型的交叉地带**。它继承了统一模型的参数效率（单一模型处理所有类别），同时通过语义解耦实现了接近甚至超越类别专用模型的性能。在 Real3D-AD 上，SeDiR 以统一架构达到 81.0% O-AUROC，不仅超越统一基线 MC3D-AD（78.2%），也超越了所有类别专用方法（Table 1）。在 Anomaly-ShapeNet 上，SeDiR 达到 93.3% O-AUROC，超越次优方法 9.1%（Table 2）。

值得注意的是，SeDiR 并非在每个类别上都超越 MC3D-AD，但其跨类别方差显著更低，表现更稳定。这反映了**泛化-特化权衡**：语义解耦设计牺牲了个别类的极致优化，换来了更可靠的跨类别一致性。

### 适用边界与局限

1. **标签依赖**：C3L 依赖类别标签进行监督对比学习，在完全无标签的开放类别场景中不可直接迁移。这是该方法最根本的适用边界。

2. **计算开销**：SeDiR 的 FLOPs 为 508.25G，略高于 MC3D-AD 的 439.21G（Table S1），在资源受限的工业部署场景中需要进一步优化。

3. **点级定位能力**：尽管 SeDiR 在物体级检测上达到 SOTA，其点级异常定位仍次于依赖记忆库的 ISMP 或伪异常方法 PO3AD 在某些数据集上的表现（Table 3），表明细粒度重建误差度量仍有改进空间。

4. **几何鲁棒性未验证**：几何偏置的设计对旋转、遮挡等几何变化的鲁棒性尚未在非理想扫描数据下充分验证。

### 开放问题

- **计算效率优化**：能否在保持语义解耦能力的同时降低计算复杂度？可能的路径包括轻量化全局 token 生成、稀疏注意力机制等。
- **开集扩展**：将类别级解耦扩展到实例级或开集（未见过类别）的3D异常检测是否可行？这需要突破 C3L 对类别标签的依赖。
- **跨任务迁移**：语义解耦与重建的联合框架是否可用于其他需要类别感知的三维点云任务（如部分分割、补全）？
- **几何偏置鲁棒性**：需要在更多非理想扫描数据（含噪声、遮挡、旋转）下验证 GGD 中几何偏置的有效性和鲁棒性。



## 原文 PDF

![[paperPDFs/CVPR_2026/A_Semantically_Disentangled_Unified_Model_for_Multi_category_3D_Anomaly_Detection.pdf]]
