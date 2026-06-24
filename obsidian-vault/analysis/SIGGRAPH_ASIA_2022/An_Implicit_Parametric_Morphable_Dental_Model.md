---
title: An Implicit Parametric Morphable Dental Model
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/An_Implicit_Parametric_Morphable_Dental_Model.pdf
project_link: "https://vcai.mpi-inf.mpg.de/projects/DMM/"
code_link: "https://github.com/cong-yi/DMM"
aliases:
- IPMDMCD
- IPMDM
tags:
- SIGGRAPH_ASIA_2022
- topic/benchmarks_datasets_evaluation
core_operator: 采用组合式隐式SDF表示，为每颗牙齿和牙龈分配独立潜码，并引入新颖的质心损失和分割损失，实现组件级建模与控制。
primary_logic: 将牙科几何分解为多个语义组件的符号距离函数，通过分割指示器预测的混合权重进行合成，无需手动非刚性对齐即可自动建立对应关系，实现重构、分割与编辑。
claims:
- 消融实验表明，去除质心损失或分割损失会严重降低重建精度并破坏语义分割（图9、表3）。
- 与DIF的重建质量相当，但额外提供了组件级编辑功能（表1）。
- 在公开数据集上达到与DIF相仿的Chamfer距离和F-score（表2）。
- Custom Aligned Dental Scans (4-fold CV) 上 Chamfer distance (×10²) = 0.552
---

# An Implicit Parametric Morphable Dental Model

> [!tip] 核心洞察
> 将牙科几何分解为多个语义组件的符号距离函数，通过分割指示器预测的混合权重进行合成，无需手动非刚性对齐即可自动建立对应关系，实现重构、分割与编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | 隐式参数化可形变牙齿模型 |
| 英文题名 | An Implicit Parametric Morphable Dental Model |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://vcai.mpi-inf.mpg.de/projects/DMM/) · [Code](https://github.com/cong-yi/DMM) · [Project](https://vcai.mpi-inf.mpg.de/projects/DMM/") |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | Implicit Parametric Morphable Dental Model (Compositional DeepSDF) |
| Dataset | Custom Aligned Dental Scans, Public Dataset |

> [!tip] 效果简介
> - Custom Aligned Dental Scans (4-fold CV) 上，Chamfer distance (×10²) 0.552 vs 0.580 (DIF); DeepSDF/DIT明显更差 (-0.028)；F-score 88.029 vs 88.125 (DIF) (-0.096)。
> - Public Dataset (Ben-Hamadou et al. 2022) 上，Chamfer distance (×10²) 0.463 vs 0.514 (DIF) (-0.051)；F-score 92.182 vs 92.622 (DIF) (-0.440)。

## 概要

现有牙齿几何模型普遍依赖显式网格表示，忽略牙龈结构，且需要复杂的非刚性对齐来建立跨样本对应关系，难以支持对单颗牙齿的独立编辑。全局隐式表示方法（如DeepSDF、DIF）虽然避免了显式网格的拓扑限制，但缺乏组件级控制能力，无法实现语义分割与局部编辑。本文提出首个面向人类牙齿与牙龈的隐式参数化可形变模型——**Implicit Parametric Morphable Dental Model**。其核心思路是采用组合式符号距离函数（Compositional DeepSDF）表示，为每颗牙齿和牙龈分别分配独立的潜码与子网络，通过分割指示器预测的混合权重将各组件的SDF合成为完整几何体，并引入质心损失与分割损失实现无需关键点的空间正则和自动语义标注。在私有牙科扫描数据集与公开基准上，该方法的重建精度与DIF相当（Chamfer距离分别为0.552×10²和0.463×10²），但额外提供了组件级编辑、牙齿替换以及治疗前后插值等DIF不具备的应用能力。该工作属于隐式神经表示与组合式形状建模的交叉，作为首个将组件化隐式SDF引入牙科形态建模的方法，为后续口腔结构建模与正畸可视化提供了新基线。

## 核心方法与创新机理

### 问题瓶颈：从全局隐式到组件级可控表示

现有牙齿数字模型面临两个根本性瓶颈。其一，传统方法依赖显式网格表示（如3D Morphable Model），要求对扫描数据进行复杂的非刚性对齐以建立网格顶点间的稠密对应关系，这一过程对牙齿这种具有显著个体差异和拓扑变化的几何体尤为困难。其二，以**DeepSDF**（Park et al., CVPR 2019）和**DIF**（Deng et al., CVPR 2021）为代表的隐式方法虽然避免了显式对应问题，但它们采用全局表示——整个牙弓几何体由一个统一的隐式函数描述，缺乏对单个牙齿或牙龈的组件级控制能力。这意味着用户无法独立编辑某一颗牙齿的位置或形状，也无法在重建的同时自动获得牙齿的语义分割标注。

本文的核心洞察在于：**将牙科几何体分解为多个语义组件的符号距离函数（SDF），通过分割指示器预测的混合权重进行合成，从而在无需手动非刚性对齐的前提下，同时实现高精度重建、自动语义分割和组件级编辑。**

### 组合式隐式SDF表示框架

方法的核心是构建一个组合式（compositional）隐式可形变模型，将完整的牙弓几何体建模为$m=15$个独立组件的加权组合：1个牙龈组件加上最多14颗牙齿组件（考虑单颌的典型牙位分布）。整体SDF函数定义为：

$$f(\mathbf{p}, \mathbf{z}_1, \ldots, \mathbf{z}_m) = \sum_{i=1}^{m} w_i \cdot f_i(\mathbf{p}, \mathbf{z}_i) = \sum_{i=1}^{m} w_i \cdot (s_i + \Delta s_i)$$

其中$\mathbf{p} \in \mathbb{R}^3$为空间中的查询点，$\mathbf{z}_i$为第$i$个组件的独立潜码（latent code），$s_i$为该组件在参考空间中该点的基准SDF值，$\Delta s_i$为变形后的SDF修正量。混合权重$w_i$通过各组件预测的分割指示器$\delta_i$进行归一化计算：

$$w_i := \frac{\delta_i}{\sum_{j=1}^{m} \delta_j}$$

这一公式设计使得空间中任意点的最终SDF值由各组件根据其“所有权”程度进行软混合，边界区域自然过渡。

### 三个关键Changed Slot

相较于DeepSDF和DIF等基线方法，本文在以下三个核心设计点上进行了根本性改变：

**Slot 1：场景表示——从全局SDF到组件级SDF混合。** DeepSDF为整个物体学习单一SDF网络，DIF在此基础上增加了全局变形场，但两者均将牙弓视为不可分割的整体。本文为每颗牙齿和牙龈分配独立的SDF组件，通过分割指示器驱动的加权混合实现整体几何合成。这一改变是后续所有编辑和分割能力的基础。

**Slot 2：潜码分配——从单码到多码。** 基线方法为每个训练扫描分配一个全局潜码$\mathbf{z}$。本文为每个扫描分配$m$个独立潜码$\{\mathbf{z}_i\}_{i=1}^m$，分别控制对应组件的形状变化。这使得不同牙齿的形状变异被解耦到各自的潜空间中，为组件级插值和编辑提供了可能。

**Slot 3：变形参数化——从通用位移场到牙齿刚体变换+牙龈位移场。** DIF为所有点学习通用位移向量。本文针对牙齿和牙龈的物理特性进行差异化建模：牙齿采用螺旋轴（screw axis）参数化的刚体变换（旋转+平移），符合牙齿作为刚性结构的解剖学先验；牙龈则采用位移场建模，以捕捉其柔性变形。这一设计显著提升了牙齿区域的重建精度，同时避免了位移场在刚性区域引入不自然的局部扭曲。

### 模块化网络架构与数据流

整个流水线由以下模块按顺序构成（参见Fig. 3）：

**模块1：Component Deform-Net（变形网络）。** 每个组件$i$拥有独立的变形网络$\Phi_i$，其权重由Hyper-Net根据该组件的潜码$\mathbf{z}_i$动态生成。对于输入的查询点$\mathbf{p}$，$\Phi_i$预测两个输出：(a) 将$\mathbf{p}$变形至组件参考空间的位移向量，得到变形后的点$\mathbf{p}_i'$；(b) 该点属于组件$i$的分割指示器$\delta_i(\mathbf{p})$。

**模块2：Component Ref-Net（参考形状网络）。** 每个组件的参考网络$\mathcal{R}_i$学习该组件在参考空间中的模板SDF，其网络参数在所有训练样本间共享（独立于潜码）。对于变形后的点$\mathbf{p}_i'$，$\mathcal{R}_i$输出基准SDF值$s_i$和SDF修正量$\Delta s_i$。

**模块3：混合权重计算。** 收集所有组件的分割指示器$\{\delta_i(\mathbf{p})\}_{i=1}^m$，通过softmax归一化得到混合权重$\{w_i\}_{i=1}^m$。

**模块4：全局SDF组装。** 将各组件的$(s_i + \Delta s_i)$按$w_i$线性组合，得到查询点$\mathbf{p}$的最终有符号距离值$s$。几何表面即为$f(\cdot)=0$的决策边界。

**训练路径：** 训练时，对于每个扫描样本，所有组件的潜码$\{\mathbf{z}_i\}$与网络参数联合优化。损失函数在组件级和全局级两个层面施加约束。组件级损失包括：(a) 分割损失$\mathcal{L}_i^{\mathrm{seg}}$——二值交叉熵，监督表面点属于组件$i$的概率；(b) 质心损失$\mathcal{L}_i^{\mathrm{centroid}}$——L1距离，约束牙齿变形后的质心靠近训练数据中该牙位的平均质心，这是实现无关键点空间正则的核心创新；(c) 对应损失$\mathcal{L}_i^{\mathrm{corres}}$——确保变形后的点与参考形状保持语义对应；(d) 变形平滑损失$\mathcal{L}_i^{\mathrm{smooth}}$——约束位移场的空间梯度；(e) 潜码正则损失$\mathcal{L}_i^{\mathrm{latent}}$——防止潜码幅值过大；(f) SDF修正正则$\mathcal{L}_i^{\mathrm{correction}}$——限制$\Delta s_i$的幅度；(g) 组件级SDF损失$\mathcal{L}_i^{\mathrm{SDF}}$——确保预测SDF值与表面法向一致。全局级损失$\mathcal{L}^{\mathrm{SDF}}$则对整体混合后的SDF施加一致性约束。总目标函数为所有组件损失与全局损失的加权和（Eq. 11）。

**推理路径：** 给定一个新的牙科扫描，固定网络参数，仅优化所有组件的潜码$\{\mathbf{z}_i\}$和指示牙齿存在与否的布尔向量。推理完成后，任意空间点的SDF值可通过前向传播直接计算，Marching Cubes提取表面网格。同时，分割指示器$\delta_i(\mathbf{p})$直接提供逐点的牙齿语义标签。

### 质心损失：无关键点的空间正则机制

质心损失是本文最具创新性的设计之一，解决了组件级隐式模型中的关键挑战：如何在没有显式关键点标注的情况下，约束变形后的牙齿组件保持在合理的空间位置。其核心思想是：对于每颗牙齿$i$，在训练数据中统计其质心的平均位置$\bar{\mathbf{c}}_i$，然后约束该组件变形后的质心$\mathbf{c}_i'$靠近这一平均位置：

$$\mathcal{L}_i^{\mathrm{centroid}} = \| \mathbf{c}_i' - \bar{\mathbf{c}}_i \|_1$$

这一损失项的作用机制是：在训练初期，各组件的参考空间位置尚未确定，变形网络可能将牙齿“拉”到任意位置。质心损失提供了一个温和的空间锚点，引导每颗牙齿的参考模板收敛到其对应的解剖位置附近。与显式关键点标注相比，质心统计完全自动从训练数据中获得，无需人工介入。消融实验（Fig. 9, Tab. 3）证实，去除该损失会导致牙齿位置漂移和严重的重建伪影。

### 分割损失：语义一致性的自监督信号

分割损失$\mathcal{L}_i^{\mathrm{seg}}$是另一个关键创新，它使得模型在重建几何的同时自动学习语义分割能力。对于每个表面采样点$\mathbf{p} \in S_i$（属于组件$i$的真实表面），该损失要求变形网络输出的分割指示器$\delta_i(\mathbf{p})$趋近于1（即该点被正确分配给组件$i$）：

$$\mathcal{L}_i^{\mathrm{seg}} = \sum_{\mathbf{p} \in S_i} \mathrm{BCE}(\delta_i(\mathbf{p}), \ell_i(\mathbf{p}) == i)$$

这一损失与SDF重建损失形成协同效应：准确的分割指示器使得混合权重$w_i$在组件边界处正确衰减，从而提升全局SDF的重建质量；反过来，高质量的SDF重建又为分割预测提供了更清晰的几何边界。消融实验（Fig. 10）表明，去除分割损失不仅丧失了语义标注能力，还会因混合权重失准而导致重建精度下降。

![[assets/figures/papers/paper_list_l19_https_vcai_mpi_inf_mpg_de_projects_DMM/figures/003_Figure_3.jpg]]
*Figure 3: The pipeline of our proposed method. We use a component-wise SDF representation where each tooth and the gum is represented by a separate "Component Shape Model". These models learn a reference shape for each component (in the Ref-Net), that is queried at those points to which the input points are warped by Deform-Net. Based on the component-wise SDF values and the segmentation indicators ?? predicted for each component, we compute the full geometry as a weighted sum (see top right)*

## 实验与关键发现

### 主结果：重建精度与DIF持平，同时解锁组件级编辑

在自建对齐牙科扫描数据集（4折交叉验证）上，本文方法与三个隐式重建基线进行定量对比（Table 1）。核心指标为对称Chamfer距离（×10²，越低越好）和F-score（越高越好）。**DMM的Chamfer距离为0.552，与DIF的0.580基本持平**（Δ = −0.028），而DeepSDF和DIT的重建误差明显更大。F-score方面，DMM达到88.029，DIF为88.125（Δ = −0.096），同样处于同一水平。

![[assets/figures/papers/paper_list_l19_https_vcai_mpi_inf_mpg_de_projects_DMM/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison with related works. The reconstruction accuracy is evaluated by the symmetric Chamfer distance (lower is better) and F-score (higher is better). Our overall reconstruction accuracy is on par with DIF. However, DIF does not enable the novel applications our method is capable of (Sec. 5.3)*

在公开数据集（Ben-Hamadou et al. 2022）上的二次验证（Table 2）进一步确认了这一结论：DMM的Chamfer距离为0.463，优于DIF的0.514（Δ = −0.051）；F-score为92.182，略低于DIF的92.622（Δ = −0.440）。两组实验一致表明：**本文方法在全局重建精度上与当时最优的隐式方法DIF相当，但DIF不具备任何组件级编辑能力**。

![[assets/figures/papers/paper_list_l19_https_vcai_mpi_inf_mpg_de_projects_DMM/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison to related works on a publicly available dataset [Ben-Hamadou et al. 2022]. The accuracy and F-scores are evaluated in the same way as Tab. 1. Similarly, our overall reconstruction accuracy is on par with DIF*

定性对比（Fig. 6）通过误差热力图揭示了一个关键细节：DMM在牙齿区域的重建误差比DIF更低，这得益于其组合式设计将每颗牙齿作为独立组件进行建模，而非用一个全局变形场统一处理所有几何细节。

![[assets/figures/papers/paper_list_l19_https_vcai_mpi_inf_mpg_de_projects_DMM/figures/006_Figure_6.jpg]]
*Figure 6: Comparison of reconstruction results with DIF [Deng et al. 2021], DeepSDF [Park et al. 2019], and DIT [Zheng et al. 2021]. Our method clearly outperforms DIT and DeepSDF. Furthermore, the error heat map shows that our method reconstructs the teeth region more accurately than DIF. Note that our method is the only one that offers independent control over each tooth and and the gums, thus enabling interesting editing applications (see Sec. 5.3)*

### 消融实验：质心损失与分割损失的决定性作用

消融实验（Table 3, Fig. 9, Fig. 10）系统验证了各设计选择的因果贡献。完整方法在所有消融变体中取得了最优的Chamfer距离和F-score。

**去除质心损失（w/o centroid loss）** 导致重建Chamfer距离显著增大，并在牙齿区域出现严重伪影（Fig. 9红色虚线标注处）。质心损失的核心机制是约束每颗牙齿变形后的质心靠近训练数据的平均质心位置，这是一种无需关键点标注的空间正则化策略。缺少该约束时，组件变形网络可能将牙齿映射到不合理的空间位置，破坏整体几何一致性。

**去除分割损失（w/o segmentation loss）** 同样造成重建精度下降，更关键的是完全破坏了语义标注能力（Fig. 10）：无分割损失时，模型无法为表面点分配正确的牙齿标签，组件混合权重失去语义意义，导致组件间的边界模糊。分割损失通过二值交叉熵监督表面点属于特定组件的概率，是组合式表示能够自动输出语义分割的根本保障。

两项损失的消融结果共同说明：**组合式隐式表示的成功不仅取决于架构设计，更依赖于针对组件级控制而专门设计的损失函数**。

### 编辑能力验证：插值与替换

除重建精度外，实验还验证了DMM独有的编辑能力。**治疗计划可视化**（Fig. 7）：在正畸治疗前后的扫描之间对潜码进行线性插值，可生成平滑的牙齿移动过渡序列，为正畸医生与患者的沟通提供视觉辅助。**牙齿替换编辑**（Fig. 8）：可将排列不齐的切牙替换为排列更整齐的对应牙齿，同时保持其余牙齿不变。该示例中的原始模型缺少犬齿，进一步验证了模型对缺失牙齿场景的适应能力。

![[assets/figures/papers/paper_list_l19_https_vcai_mpi_inf_mpg_de_projects_DMM/figures/011_Figure_8.jpg]]
*Figure 8: Teeth replacement demonstration. (a) and (d) show two malaligned incisors from bottom and side view respectively (see dashed red). (b) and (e) show the result of replacing these two incisor teeth by some counterparts that are aligned better, while keeping all the other teeth unchanged. (c) and (f ) encode the difference between before and after the edit. Note that the original model has no canine. Thus, we selected to process this example to show that we can reconstruct a model with originally missing teeth*

![[assets/figures/papers/paper_list_l19_https_vcai_mpi_inf_mpg_de_projects_DMM/figures/010_Figure_7.jpg]]
*Figure 7: In each row we interpolate between the reconstruction of a pre-treatment scan (first column) and the reconstruction of a post-treatment scan (last column). The arrows show the direction of interpolation. We can render plausible visualizations of orthodontic treatment plans in this way, which is best illustrated by our supplemental video results*

### 失败模式与适用边界

**缺失牙齿的布尔向量依赖**是最突出的失效场景（Fig. 11）。当提供的布尔向量与真实情况不符（例如将存在的右侧切牙标记为缺失），重建结果会出现强烈伪影。模型无法自动推断牙齿的存在与否，这一限制源于训练时该布尔向量作为输入条件被直接编码到组件激活状态中。

**训练数据规模与覆盖范围**构成另一边界条件。模型在约39例扫描上训练，仅覆盖单颌（上颌或下颌），未扩展至上下颌联合建模。此外，当前模型仅包含牙龈和牙齿的几何形状，未建模舌头、纹理等其他口腔结构。这些限制意味着模型在数据分布外的泛化能力尚待更大规模、更多样化数据集的验证。

**与DIF的精度差距**虽小但存在：在公开数据集上F-score略低于DIF（−0.440），可能源于组合式表示在组件边界处的混合权重计算引入的微小误差。这一差距在实际应用中是否可感知，需结合具体临床任务的精度要求进行判断。

## 定位与知识库关联

本文的核心贡献在于将**全局隐式SDF表示**替换为**组合式组件级隐式SDF表示**，这是相对于已有工作的根本性slot变更。具体而言，**DeepSDF**（Park et al., CVPR 2019）和**DIF**（Deng et al., CVPR 2021）均采用全局潜码控制整个几何体，缺乏对单个牙齿或牙龈的独立建模能力；**DIT**（Zheng et al., CVPR 2021）虽引入模板学习，但同样未解耦语义组件。本工作将场景表示从“一个潜码→一个完整SDF”改为“m个组件潜码→m个组件SDF→加权混合”，从而在不牺牲重建精度的前提下，首次在隐式形态模型中实现了组件级编辑、语义分割和平滑插值。

在知识库中的挂载点，该工作处于**隐式神经表示**与**牙科形态建模**的交叉节点。从隐式表示脉络看，它继承并改造了DeepSDF的自动解码器框架和DIF的变形场机制，但通过引入**分割指示器**和**质心损失**将对应关系建立从手工标注推进到自动学习。从牙科建模脉络看，它是对传统显式网格形态模型（如3DMM在牙齿上的应用）的隐式替代，省去了复杂的非刚性对齐流程，同时首次将牙龈纳入统一建模框架。

**适用边界**需明确以下几点。第一，该模型仅处理单颌（上颌或下颌）几何，未扩展至上下颌联合建模，这限制了其在全口咬合分析中的应用。第二，模型需要人工提供指示每颗牙齿存在与否的布尔向量（Fig. 11），无法自动推断缺牙情况，这在实际临床部署中是一个需要手动验证的环节。第三，训练数据规模有限（约39例四折交叉验证），且仅包含几何形状，无纹理或外观信息，因此无法直接用于需要真实感渲染或软组织模拟的场景。第四，模型未包含舌头建模，对完整口腔内部重建而言仍不完整。

**后续启发**可从以下几个方向展开。在方法层面，如何自动推断牙齿存在/缺失的布尔向量是一个直接且实用的扩展方向，可能通过引入牙齿存在性的先验概率或与牙齿检测网络联合训练来实现。在表示层面，将纹理信息集成到隐式模型中（例如通过附加颜色场或神经辐射场组件）可大幅提升可视化质量，使其更适用于患者沟通场景。在应用层面，该模型的组件级编辑能力使其天然适合正畸治疗计划的可视化（Fig. 7的插值演示已初步验证），但需进一步验证其在不同牙科异常（如多生牙、阻生牙）下的泛化性。此外，将模型扩展至双颌联合建模并加入咬合约束，可使其在口腔修复和正颌手术规划中发挥更大作用。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/An_Implicit_Parametric_Morphable_Dental_Model.pdf]]