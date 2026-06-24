---
title: "DSG-Net: Learning Disentangled Structure and Geometry for 3D Shape Generation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/DSG_Net_Learning_Disentangled_Structure_and_Geometry_for_3D_Shape_Generation.pdf
project_link: "http://geometrylearning.com/dsg-net/"
code_link: null
aliases:
- DN
- DSG-Net
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 将形状结构（符号化层次与关系）和几何（可变形网格）编码到两个独立的潜空间，并通过循环解耦机制（Cycled Disentanglement）实现自监督解耦学习。
primary_logic: 通过分离但协同的结构VAE和几何VAE，利用层次化递归网络与双向映射，在确保生成形状合理性的同时，实现对结构（部件组成与关系）和几何（部件细节）的独立插值与操控。
claims:
- 在PartNet椅子重建任务上，DSG-Net的CD为2.96，HierInsSeg为0.45，显著优于StructureNet（4.59, 0.66）和SDM-Net（6.92, 1.59）。
- 在用户研究中，DSG-Net在形状生成的几何与结构质量上获得平均排名1.80（1为最佳），优于SDM-Net、StructureNet和SN+Mesh。
- PartNet Chairs (Reconstruction) 上 CD (×10⁻³) ↓ = 2.96
- PartNet Chairs (Reconstruction) 上 HierInsSeg(HIS) ↓ = 0.45
---

# DSG-Net: Learning Disentangled Structure and Geometry for 3D Shape Generation

> [!tip] 核心洞察
> 通过分离但协同的结构VAE和几何VAE，利用层次化递归网络与双向映射，在确保生成形状合理性的同时，实现对结构（部件组成与关系）和几何（部件细节）的独立插值与操控。

| 字段 | 内容 |
|------|------|
| 中文题名 | DSG-Net：学习三维形状生成中结构与几何的解耦表示 |
| 英文题名 | DSG-Net: Learning Disentangled Structure and Geometry for 3D Shape Generation |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](http://geometrylearning.com/dsg-net/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | DSG-Net |
| Dataset | PartNet Chairs, PartNet Lamps |

> [!tip] 效果简介
> - PartNet Chairs (Reconstruction) 上，CD (×10⁻³) ↓ 2.96 vs StructureNet 4.59 (-1.63 (-35.5%))；HierInsSeg(HIS) ↓ 0.45 vs StructureNet 0.66 (-0.21 (-31.8%))。
> - PartNet Lamps (Reconstruction) 上，CD (×10⁻³) ↓ 7.15 vs StructureNet 17.31 (-10.16 (-58.7%))。
> - PartNet Chairs (Generation) 上，FPD ↓ 9.73 vs StructureNet 22.30 (-12.57 (-56.4%))。

## 概要

现有三维形状生成方法难以同时处理复杂结构和高精度几何细节，且缺乏对形状结构与几何的独立控制能力。本文提出 **DSG-Net**，将形状解耦为两个独立但协同的潜空间：结构 VAE 编码符号化的部件层次与关系，几何 VAE 编码可变形网格的 ACAP 特征，并通过**循环解耦机制（CycD）**以自监督方式强化二者的分离。在 PartNet 椅子重建任务上，DSG-Net 的倒角距离（CD）为 2.96，层次实例分割指标（HierInsSeg）为 0.45，显著优于 StructureNet（4.59, 0.66）和 SDM-Net（6.92, 1.59）；生成任务的 FPD 为 9.73，较 StructureNet 降低 56.4%。用户研究进一步表明，DSG-Net 在几何与结构质量上均获最优评价。该方法定位于结构化变形网格生成与解耦表示学习的交叉点，为可控三维形状生成提供了新范式。

## 核心方法与创新机理

DSG-Net 的核心目标是在三维形状生成中同时处理复杂结构和精细几何，并实现两者的解耦控制。现有方法（如 StructureNet 的单一递归 VAE 联合建模结构与点云，或 SDM-Net 为不同语义部件训练独立 VAE）难以在结构多样性与几何精度之间取得平衡，更缺乏对这两个维度的独立操控能力。DSG-Net 的关键洞察是：将形状解构为**符号化结构层次**（部件标签、层级关系、空间关系）和**可变形网格几何层次**两个平行空间，通过分离但协同的 VAE 学习各自的潜表示，并引入**循环解耦机制（CycD）** 以自监督方式强化解耦。

### 1. 形状的双层次解耦表示

给定一个三维形状，DSG-Net 将其表示为一一对应的两个层次树（Fig. 3）：

![[assets/figures/papers/paper_list_l15_http_geometrylearning_com_dsg_net/figures/003_Figure_3.jpg]]
*Figure 3: An example showing the proposed disentangled but highly synergistic representation of shape geometry and structure hierarchies. There is a bijective mapping between the tree nodes in the two hierarchies. In the structure hierarchy, we consider symbolic part semantics and a rich set of part relationships (orange arrows), such as adjacency*

- **结构层次**：$(\langle l_1, l_2, \cdots, l_N \rangle, \mathbf{H}, \mathbf{R})$，其中 $l_i$ 为部件语义标签，$\mathbf{H}$ 为父子层级关系，$\mathbf{R}$ 为部件间的空间关系（如相邻、对称等）。
- **几何层次**：$\langle G_1, G_2, \cdots, G_N \rangle$，其中每个叶节点部件 $G_i = (X_i, c_i)$ 包含 ACAP 变形特征 $X_i$ 和部件中心坐标 $c_i$。

两个层次树的节点之间存在双射映射，确保结构信息与几何信息在层级上严格对齐，但编码到两个独立的潜空间。

### 2. 条件部件几何 VAE（Conditional Part Geometry VAE）

在叶节点层面，DSG-Net 使用统一的、以结构上下文为条件的部件几何 VAE 来编码和解码每个部件的网格几何（Fig. 4b）。这是与 SDM-Net（为每个语义类别训练独立 VAE）的关键差异点。

具体流程：
1. **网格配准**：将所有部件网格通过非刚性配准变形到一个统一的单位立方体模板网格（5402 个顶点），提取 ACAP 特征 $X_i$ 以紧凑表示局部变形（Fig. 4a）。
2. **条件编码**：编码器 $\mathrm{Enc}_{PG}$ 将 $(X_i, c_i)$ 映射到 128 维潜码 $z_i$，同时以部件语义标签和当前结构上下文（通过结构 VAE 提供的条件信息）作为条件输入。
3. **条件解码**：解码器 $\mathrm{Dec}_{PG}$ 从 $z_i$ 和相同的结构条件重建 $\hat{X}_i$ 和 $\hat{c}_i$。

训练损失为：
$$\mathcal{L}_{\mathrm{cond-PartVAE}} = \lambda_1 \mathcal{L}_{\mathrm{cond-PartVAE}}^{\mathrm{recon}} + \mathcal{L}_{\mathrm{cond-PartVAE}}^{\mathrm{KL}}$$
其中重建损失为 ACAP 特征和部件中心的 MSE：
$$\mathcal{L}_{\mathrm{cond-PartVAE}}^{\mathrm{recon}} = \|\hat{X}_i - X_i\|_2^2 + \|\hat{c}_i - c_i\|_2^2$$

这种设计的因果优势在于：统一的 VAE 通过参数共享学习跨语义的几何先验，同时结构条件引导解码器生成与当前结构树节点协同的几何形态。消融实验证实，统一条件 VAE 的重建 CD 为 1.98，而独立语义 VAE 为 14.22（Table 8），验证了参数共享和结构条件的关键作用。

### 3. 分离但协同的结构 VAE 与几何 VAE

在层次化形状层面，DSG-Net 训练两个递归 VAE，分别学习结构潜空间和几何潜空间（Fig. 5）。

![[assets/figures/papers/paper_list_l15_http_geometrylearning_com_dsg_net/figures/005_Figure_5.jpg]]
*Figure 5: We train two disentangled but synergistic geometry and structure variational autoencoders (VAEs) with recursive encoders and decoders to learn disentangled latent spaces for shape geometry and structure. The figure illustrates the joint learning procedure of the structure VAE (red) and the geometry VAE (blue). In the encoding stage, the structure features summarize the symbolic part semantics and recursively compute sub-hierarchy structure contexts, while the geometry features encode the detailed part geometry for leaf nodes and propagate the geometry information along the same hierarchy. The decoding procedures of the VAEs are supervised to reconstruct the hierarchical structure and geomet...*

**结构 VAE**：
- 递归编码器从叶节点开始，自底向上聚合符号化结构信息（标签、层级、关系），通过图消息传递模块处理部件间的边关系，最终得到全局结构潜码 $S$。
- 递归解码器从 $S$ 出发，自顶向下生成结构层次，预测每个节点的语义标签、父子关系和空间关系。

**几何 VAE**：
- 递归编码器同样自底向上聚合几何特征，但其关键设计是**受结构 VAE 的条件引导**：在每一层聚合时，几何编码器接收对应结构节点的特征作为条件，确保几何潜空间编码与结构协同的信息。
- 递归解码器从全局几何潜码 $G$ 出发，自顶向下生成几何层次，同样以结构解码器的输出为条件，指导部件几何的生成。

两个 VAE 的协同关系体现为双向条件引导：结构信息约束几何的生成范围，几何信息反过来影响结构节点的特征表示。消融实验显示，移除边组件和消息传递（w/o edge）后，椅子重建 CD 从 1.98 升至 3.59（Table 7），证明结构关系对几何重建至关重要——缺失边信息导致部件间空间关系丢失，产生分离部件（Fig. 21）。

### 4. 循环解耦机制（Cycled Disentanglement, CycD）

虽然分离的 VAE 架构初步实现了结构/几何的分离，但两个潜空间仍可能包含冗余信息。DSG-Net 提出 CycD 机制（Fig. 7），以自监督方式进一步强化解耦：

![[assets/figures/papers/paper_list_l15_http_geometrylearning_com_dsg_net/figures/007_Figure_7.jpg]]
*Figure 7: We propose a new Cycled Disentanglement mechanism to further disentangle the geometry and structure of shapes. Based on the pre-trained DSG-Net, we decouple two shapes (?? and ??) into geometry*

给定两个形状 A 和 B：
1. 提取 A 的结构码 $S_A$ 和 B 的几何码 $G_B$。
2. 交换组合：用 $S_A$ 和 $G_B$ 通过预训练的 DSG-Net 解码器合成新形状 C。
3. 重新编码 C，得到 $\hat{S}_C$ 和 $\hat{G}_C$。
4. 施加循环一致性损失：
   - 结构损失：$\mathcal{L}_{\mathrm{struct}} = \|S_C - S_A\|_2^2$，鼓励合成形状 C 的结构码与源形状 A 一致。
   - 几何损失：$\mathcal{L}_{\mathrm{geo}} = \|G_C - G_B\|_2^2$，鼓励合成形状 C 的几何码与源形状 B 一致。

CycD 的因果逻辑是：如果结构和几何真正解耦，那么交换潜码后合成的形状应保留各自源形状的结构和几何特征。消融实验验证了 CycD 的有效性：移除 CycD 后，椅子重建 CD 从 1.98 升至 2.39，结构指标 HierInsSeg 从 0.45 升至 0.58（Table 7）。

### 5. 训练与推理路径

**训练流程**：
1. **第一阶段**：预训练条件部件几何 VAE，学习叶节点部件的几何编码/解码。
2. **第二阶段**：联合训练结构 VAE 和几何 VAE，使用重建损失和 KL 散度学习两个潜空间。
3. **第三阶段**：在预训练的 DSG-Net 基础上施加 CycD 机制，通过循环一致性损失微调解耦。
4. 端到端训练与分步训练效果相近（椅子 CD 1.98 vs 2.10，Table 9），为简洁选择端到端方案。

**推理流程**：
1. 从结构潜空间和几何潜空间分别采样 $S$ 和 $G$（或从输入形状编码得到）。
2. 结构解码器从 $S$ 递归生成结构层次。
3. 几何解码器从 $G$ 递归生成几何层次，以结构解码器输出为条件。
4. 条件部件几何 VAE 解码每个叶节点的 ACAP 特征和中心坐标，重建部件网格。
5. 后处理优化：固定网络参数，仅优化部件中心位置以消除部件间距，提升连接紧密性。

### 6. 关键创新总结

DSG-Net 的三个核心 changed slots 形成因果链：
1. **形状表示**：从单一联合编码变为分离的结构/几何双层次表示，为解耦提供架构基础。
2. **部件几何生成**：从独立语义 VAE 变为统一的、以结构上下文为条件的 VAE，实现参数共享和结构自适应几何生成。
3. **解耦策略**：从无约束变为 CycD 循环一致性机制，以自监督方式强化潜空间解耦。

这三个模块的协同关系是：双层次表示定义了分离的编码空间；统一条件 VAE 确保几何生成与结构协同；CycD 消除潜空间间的信息泄漏，最终实现可独立操控的结构/几何生成（Fig. 13 展示固定一个潜码、采样另一个潜码的生成结果）。

![[assets/figures/papers/paper_list_l15_http_geometrylearning_com_dsg_net/figures/004_Figure_4.jpg]]
*Figure 4: We present: (a) the non-rigid part mesh registration process, and (b) the architecture of our conditional part geometry variational autoencoder. In (a), we deform a box mesh to any given part geometry and then extract ACAP [Gao et al. 2019a] feature based on the registration. In (b), for a single part mesh geometry, the encoder maps the part ACAP feature and its center position into a 128-dimensional geometric latent code, while the decoder reconstructs the part geometry by decoding the ACAP feature and the center vector. Both networks are conditioned on the part structure information along the structure hierarchy to generate specialized part geometry for different structure contexts*

![[assets/figures/papers/paper_list_l15_http_geometrylearning_com_dsg_net/figures/006_Figure_6.jpg]]
*Figure 6: We illustrate the detailed architecture of recursive graph encoders*

![[assets/figures/papers/paper_list_l15_http_geometrylearning_com_dsg_net/figures/030_Figure_20.jpg]]
*Figure 20: We show some qualitative comparisons between our final DSG-Net (the disentangled pipeline) with two ablated versions: one is the approach that naively combines StructureNet and ACAP mesh representation (without disentanglement design), namely SN+Mesh, and the other is DSG-Net without the cycled disentanglement, namely Ours (w/o CycD). While three methods demonstrate strong performance for shape reconstruction, we still observe that our final version achieves higher accurate reconstruction regarding some part geometric details, such as the supporting pole of the left lamp, the chain of the right lamp, the back of the left chair, and the arm of the right sofa. This explains the performance bo...*

## 实验与关键发现

### 评估设置

DSG-Net 在 PartNet 数据集上进行评估，所有方法使用相同的官方训练/测试划分。几何重建质量采用倒角距离（CD, ×10⁻³）和推土机距离（EMD, ×10⁻²），均在采样点云上计算；结构重建质量采用层次实例分割一致性指标 HierInsSeg（HIS），衡量预测的部件层次结构与真实标注的一致性。生成质量采用 Fréchet Point-cloud Distance（FPD）评估生成点云的多样性与质量。用户研究通过 119 次成对比较试验收集排名（1 为最佳，4 为最差），参与者包括具有 3D 背景的研究生。

### 主实验结果

**形状重建。** 在 PartNet 椅子类别上，DSG-Net 取得了 CD 2.96、EMD 2.88、HIS 0.45 的最佳综合表现。相比最强基线 StructureNet（CD 4.59, EMD 3.98, HIS 0.66），CD 降低 35.5%，HIS 降低 31.8%；相比 SDM-Net（CD 6.92, EMD 4.62, HIS 1.59），优势更为显著。在台灯类别上，DSG-Net 的 CD 从 StructureNet 的 17.31 降至 7.15，降幅达 58.7%，表明该方法对不同复杂度的物体类别均具有鲁棒的几何重建能力。与隐式场方法 IM-Net（CD 8.92）和 BSP-Net（CD 6.38）相比，DSG-Net 在几何精度上同样大幅领先，同时额外提供了结构层次信息。

**形状生成。** 在椅子生成任务上，DSG-Net 的 FPD 为 9.73，StructureNet 为 22.30，降幅 56.4%。与 SAG-Net 的对比中，DSG-Net 在所有几何和结构指标上均取得更优或可比结果，且无需体素化带来的分辨率损失。

**用户研究。** 在几何质量、结构质量和整体偏好三个维度上，DSG-Net 的平均排名分别为 1.75、1.80、1.80，均显著优于 SDM-Net（3.10, 2.95, 2.95）、StructureNet（2.65, 2.70, 2.70）和 SN+Mesh（2.50, 2.55, 2.55），验证了解耦表示在感知质量上的优势。

### 关键消融实验

**结构关系建模（w/o edge）。** 移除边组件和图消息传递模块后，椅子重建 CD 从完整模型的 1.98 升至 3.59，HIS 从 0.35 升至 0.47。这表明部件间的结构关系（如对称性、邻接关系）为几何重建提供了关键的上下文约束，缺失该信息会导致几何精度大幅下降。

**循环解耦机制（w/o CycD）。** 移除 CycD 后，椅子 CD 升至 2.39，HIS 升至 0.58。在合成数据的解耦重建实验中，无 CycD 版本的解耦误差显著增大，验证了 CycD 通过交换结构/几何潜码的自监督训练有效强化了潜空间的解耦性。

**统一条件部件 VAE vs. 独立 VAE。** 使用统一的、以结构上下文为条件的部件几何 VAE，椅子重建 CD 为 1.98；为每个语义部件训练独立 VAE 时 CD 高达 14.22。统一 VAE 不仅参数效率更高，且通过跨部件的参数共享，使模型能够利用结构上下文适应不同部件的几何生成需求。

**端到端 vs. 分步训练。** 端到端训练（CD 1.98）与先训练条件部件 VAE 再训练递归 VAE 的分步策略（CD 2.10）效果相近，为简洁性选择端到端方案。

### 失败模式与适用边界

**失败案例分析。** DSG-Net 生成的形状中仍存在以下典型问题：部件缺失（如椅子缺少扶手）、部件分离（如桌腿与桌面未连接）、不对称部件（如扶手左右不对称）、额外部件或尺寸不兼容。这些问题部分源于网络重建的是隐式结构树，部件间的物理连接通过后处理优化完成，而非端到端学习。

**后处理优化的作用与局限。** 后处理优化通过调整部件中心位置来消除间距，可改善连接性，但无法修复根本性的结构错误（如部件缺失或语义不匹配）。

**结构约束。** 当前方法假设每个父节点最多有 10 个子节点，限制了处理具有大扇出结构的物体（如多辐条车轮）。此外，训练依赖 PartNet 提供的细粒度层次化部件标注和关系注释，这类标注获取成本较高，限制了方法向弱标注或无监督场景的推广。

**适用边界总结。** DSG-Net 在具有清晰层次化部件结构的刚性物体（如椅子、桌子、台灯）上表现优异，但在处理柔性物体、非层次化结构或超高扇出节点时存在局限。部件连接质量依赖后处理而非端到端学习，在需要精确关节合成的场景下需结合专门方法。

## 定位与知识库关联

DSG-Net 的核心贡献在于将三维形状生成任务中的**形状表示**这一关键 slot 从“单一潜空间联合建模”改变为“分离的结构潜空间与几何潜空间协同学习”。此前的方法或使用统一的递归 VAE 同时编码结构信息与几何坐标（如 StructureNet），或为不同语义部件训练独立 VAE（如 SDM-Net），均未在潜空间层面显式解耦结构与几何。DSG-Net 通过引入**循环解耦机制（CycD）**，在自监督框架下实现了这一分离，使得用户能够独立操控形状的部件组成关系与部件几何细节，这是现有方法所不具备的能力。

在知识库中，该工作的挂载点位于**结构化三维生成模型**与**解耦表示学习**的交叉节点。上游可追溯至：（1）基于递归神经网络的形状结构化建模，如 StructureNet（Mo et al., SIGGRAPH 2019），其首次将形状表示为层次化图并通过单一递归 VAE 编码，但未区分结构与几何；（2）变形网格生成方法，如 SDM-Net（Gao et al., NeurIPS 2019），其采用 ACAP 特征表示部件几何并训练独立 VAE，但缺乏统一的几何潜空间且未建模结构关系；（3）隐式场生成方法，如 IM-Net（Chen & Zhang, CVPR 2019）和 BSP-Net（Chen et al., CVPR 2020），其虽能生成高质量表面，但无法提供结构化的部件层次信息。DSG-Net 在 StructureNet 的层次化图表示基础上，将单一的潜空间拆分为结构与几何两个独立空间，并用双向映射（bijective mapping）保持两者的协同性，从而在保留结构化建模优势的同时获得了独立的控制维度。

与 SAG-Net（Wu et al., CVPR 2020）相比，后者虽然也尝试解耦结构与几何，但基于体素表示且使用单一潜空间，解耦程度受限于表征能力。DSG-Net 通过分离的 VAE 设计和 CycD 机制，在网格表示的精度和解耦的彻底性上均有显著提升。此外，与 SDM-Net 为每个语义部件训练独立 VAE 的策略不同，DSG-Net 采用统一的、以结构上下文为条件的部件几何 VAE，参数共享且能适应不同结构，这一设计不仅减少了参数量，更使得几何潜空间具有跨部件的泛化能力。

**适用边界**方面，DSG-Net 依赖 PartNet 提供的细粒度层次化部件标注和关系注释，这限制了其在缺乏此类标注的数据集上的直接应用。方法假设每个父节点最多有 10 个子节点，对于具有大量兄弟部件（如车轮辐条）的形状类别存在容量限制。此外，部件间连接仅通过后处理优化中心位置实现，未端到端学习关节或连接合成，在需要物理一致性的应用场景中存在不足。生成结果中仍可能出现部件缺失、分离或不对称等失败情况。

**后续启发**方面，DSG-Net 的解耦框架为以下方向提供了基础：一是与部件连接/关节合成方法（如 COALESCE）的集成，有望实现端到端的物理一致形状生成；二是将解耦策略推广至场景布局生成或动态物体合成，通过分离布局结构与物体几何实现更灵活的操控；三是探索弱监督或无监督的层次结构发现方法，降低对精细标注的依赖。在知识库中，该工作可作为“结构化解耦生成”节点的奠基性工作，连接结构感知生成与解耦表示学习两条主线，为后续研究提供可扩展的框架模板。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/DSG_Net_Learning_Disentangled_Structure_and_Geometry_for_3D_Shape_Generation.pdf]]