---
title: Expanding mmWave Datasets for Human Pose Estimation with Unlabeled Data and LiDAR Datasets
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Expanding_mmWave_Datasets_for_Human_Pose_Estimation_with_Unlabeled_Data_and_LiDAR_Datasets.pdf
project_link: null
code_link: "https://github.com/Shimmer93/EMDUL"
aliases:
- EMDHPEUDLD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过对无标签毫米波数据进行伪标签、并将LiDAR数据集转换为毫米波风格的点云，大幅度扩充训练数据集的体量和多样性。
primary_logic: 提出闭环点云转换流水线（含基于流的关键点过滤FPF）逼真模拟毫米波雷达的运动检测机制，同时结合无监督时间一致性损失（UTCL）提高无标签数据伪标签的可靠性，从而有效扩充数据集。
claims:
- 在MM-Fi上的域内测试中，EMDUL使整体误差降低15.1%；在跨域测试（mmBody→MM-Fi）中降低18.9%。
- 消融实验表明，UTCL中的动态/静态一致性损失组合使用才能显著提升跨域性能；PC转换流水线中FPF带来最大增益。
- 使用FPF后，60.46%的转换LiDAR点云被二元分类器判定为毫米波数据（无FPF仅43.06%），验证了转换的真实性。
- MM-Fi (in‑domain) 上 平均误差降低 = EMDUL (整体框架)
---

# Expanding mmWave Datasets for Human Pose Estimation with Unlabeled Data and LiDAR Datasets

> [!tip] 核心洞察
> 提出闭环点云转换流水线（含基于流的关键点过滤FPF）逼真模拟毫米波雷达的运动检测机制，同时结合无监督时间一致性损失（UTCL）提高无标签数据伪标签的可靠性，从而有效扩充数据集。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用未标记数据和LiDAR数据集扩展毫米波人体姿态估计数据集 |
| 英文题名 | Expanding mmWave Datasets for Human Pose Estimation with Unlabeled Data and LiDAR Datasets |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.14507) · [Code](https://github.com/Shimmer93/EMDUL) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | EMDUL |
| Dataset | MM-Fi, mmBody → MM-Fi, MM-Fi → MM-Fi |

> [!tip] 效果简介
> - MM-Fi (in‑domain) 上，平均误差降低 EMDUL (整体框架) vs 未扩展的原始数据集训练 (15.1% 误差降低)。
> - mmBody → MM-Fi (out‑of‑domain) 上，平均误差降低 EMDUL (整体框架) vs 未扩展的原始数据集训练 (18.9% 误差降低)。
> - MM-Fi → MM-Fi (F→F) 上，MPJPE (cm) 10.06 (EMDUL + P4T) vs 12.23 (P4T, 10% 标记数据) (-2.17)。

## 概要

毫米波雷达人体姿态估计（HPE）面临一个根本瓶颈：**现有毫米波HPE数据集不仅规模小，而且在点云属性（检测噪声、密度、运动灵敏度）和人体姿态多样性上均严重不足**，导致模型在未见场景下的泛化能力极差。

针对这一问题，本文提出 **EMDUL**（Expanding mmWave Datasets with Unlabeled Data and LiDAR Datasets），一种**无需额外人工标注**的数据集扩展框架。其核心思路是通过两个独立且互补的模块，同时从无标签毫米波数据和有标注LiDAR数据集两个维度扩充训练数据：

- **伪标签估计器**：利用无监督时间一致性损失（UTCL）为无标签毫米波数据生成可靠伪标签，从而增加毫米波数据的姿态多样性。
- **闭环点云转换器**：将LiDAR点云转换为毫米波风格点云，其中**流基点过滤（FPF）** 模块通过模拟毫米波雷达的运动检测机制，逼真地再现了毫米波点云的关键属性。

**核心结论**：在仅使用10%标记数据的设定下，EMDUL使域内测试误差降低15.1%，跨域测试误差降低18.9%。消融实验证实，FPF是点云转换流水线中贡献最大的组件——加入FPF后，转换点云被判别器识别为毫米波数据的比例从43.06%跃升至60.46%，验证了其转换逼真度。在仅1%标记数据的极端低资源场景下，EMDUL仍以MPJPE 14.77 cm大幅领先**Mean Teacher**（Tarvainen & Valpola, NIPS 2017）的18.40 cm，展现出极强的数据效率。

### 方法谱系与知识库定位

EMDUL定位于**毫米波人体姿态估计的数据增强与半监督学习交叉点**，其方法谱系可沿两条线索追溯：

**HPE骨干网络**：本文并非提出新的HPE模型架构，而是将数据集扩展框架作为即插即用的增强方案，作用于现有SOTA方法之上。实验覆盖的骨干网络包括基于点云的**P4T**（Fan et al., CVPR 2021）、**SPiKE**（Ballester et al., 2024）、基于Transformer的**PT**（Zheng et al., ICCV 2021）以及基于扩散模型的**mmDiff**（Fan et al., 2024）。EMDUL在这些异构架构上均取得一致且显著的性能提升，证明其扩展策略与具体HPE模型解耦。

**伪标签策略**：在半监督学习维度，EMDUL区别于经典的**Mean Teacher**一致性正则化方法。Mean Teacher仅依赖模型参数的指数滑动平均来约束预测一致性，而EMDUL通过UTCL引入了毫米波雷达的物理先验——动态一致性损失（DCL）鼓励靠近点云的关节具有足够大的运动幅度，静态一致性损失（SCL）则惩罚远离点云的关节产生虚假运动。这一设计将雷达运动检测的物理机制编码为损失函数，使得伪标签更符合毫米波数据的真实特性。

**LiDAR到毫米波的域迁移**：直接使用LiDAR数据集训练毫米波HPE模型效果有限，因为两种传感器的点云分布差异巨大（密度、噪声模式、运动敏感度均不同）。EMDUL的闭环转换流水线（NPA→FPF→RS→NI）通过一系列可解释的几何增强操作，在不依赖可学习参数的情况下缩小这一域差距，为跨传感器数据利用提供了一种轻量且有效的方案。



### 毫米波人体姿态估计的瓶颈

毫米波雷达因其隐私保护、穿透遮挡和低功耗等优势，在人体姿态估计（Human Pose Estimation, HPE）领域受到日益增长的关注。然而，现有毫米波HPE数据集面临**稀缺且多样性不足**的双重困境。这种不足体现在两个维度：

- **点云属性层面**：毫米波点云在检测噪声、密度、运动灵敏度等方面具有独特的物理特性，而现有数据集难以覆盖这些属性的完整变化范围。
- **人体姿态层面**：受限于采集场景和参与者的数量，数据集中的人体姿态多样性远不及LiDAR或视觉数据集。

这一瓶颈直接导致模型**泛化能力差**——在训练场景内表现尚可，但一旦部署到未见过的环境或设备配置下，性能急剧下降。Figure 1 直观展示了该问题：基线方法 P4T（Fan et al., CVPR 2021）在未见场景下出现多处大于10 cm的关节误差（红色标记），而经过数据集扩展后，这些误差显著减少。

### 现有解决方案的缺口

面对数据稀缺问题，已有工作尝试从两个方向突破：

1. **利用无标签毫米波数据**：采用半监督方法（如 Mean Teacher，Tarvainen & Valpola, NIPS 2017）进行伪标签学习。但这类方法缺乏对毫米波物理特性的显式建模，伪标签质量难以保证。

2. **引入LiDAR数据集**：LiDAR人体姿态数据集（如 HmPEAR）具有更丰富的姿态多样性，但其点云分布与毫米波点云存在本质差异——LiDAR点云更密集、噪声模式不同、且不具备毫米波雷达特有的运动检测选择性。直接将LiDAR数据作为附加训练样本，分布差异会限制增益。

### 核心动机

本文的核心洞察在于：**毫米波雷达的运动检测机制本身提供了一个强大的物理先验**。如 Figure 3 所示，毫米波雷达仅对具有足够运动速度的目标产生稳定检测点——高流幅值（黄色）的关节附近点云密集，而低流幅值（深蓝色）的关节则几乎没有对应检测点。这一机制解释了为何毫米波点云在空间分布上与LiDAR存在系统性差异，也为如何将LiDAR点云“翻译”为毫米波风格提供了关键线索。

基于此，本文提出 **EMDUL**（Expanding mmWave Datasets with Unlabeled Data and LiDAR Datasets），通过两个独立模块协同工作：

- **伪标签估计器**：同时利用有标签和无标签毫米波数据训练，并引入**无监督时间一致性损失（UTCL）**约束伪标签满足毫米波运动检测先验。
- **闭环点云转换器**：将LiDAR点云逐步转换为毫米波风格，核心是**流基点过滤（FPF）**——基于骨架流幅值概率性地保留点云点，模拟毫米波雷达对运动目标的敏感检测。

这种设计使得 EMDUL 能够从两个互补方向大幅扩充训练数据的体量和多样性，从而在域内和跨域场景下均显著提升HPE模型的泛化能力。



## 核心方法与创新机理

EMDUL 的核心创新在于**同时从两个维度系统性地扩充毫米波人体姿态估计（HPE）训练数据**：一是利用无标签毫米波数据，二是将标注完备的 LiDAR 数据集转换为毫米波风格点云。这两个维度分别由两个独立模块驱动——伪标签估计器与闭环点云转换器，二者相互正交、可叠加使用，共同缓解毫米波 HPE 领域数据稀缺与多样性不足的瓶颈。

### 伪标签估计器与无监督时间一致性损失（UTCL）

现有伪标签方法（如 **Mean Teacher**，Tarvainen and Valpola, NIPS 2017）在毫米波 HPE 场景下通常仅依赖监督损失训练，或采用缺乏物理先验的一致性约束，导致伪标签质量有限。EMDUL 的伪标签估计器在监督 MSE 损失之外，引入了一种全新的**无监督时间一致性损失（UTCL）**，利用毫米波雷达的运动检测物理机制约束伪标签的时间一致性。

UTCL 由两个互补分量构成：

- **动态一致性损失（DCL）**：对距离点云点足够近（距离小于阈值 $\mu$）的关节，其骨架流幅值应较大——毫米波雷达正是通过检测运动目标来生成点云。DCL 惩罚流幅值低于阈值 $\eta$ 的动态关节，迫使其“动起来”：

$$L^{\mathrm{dyn}} = \frac{1}{|F_{t}^{\mathrm{dyn}}|} \sum_{k=1}^{|F_{t}^{\mathrm{dyn}}|} \max(0, \eta - \| F_{t}^{\mathrm{dyn}}[k] \|_{2})$$

- **静态一致性损失（SCL）**：对距离点云点较远（距离大于阈值 $\rho$）的关节，其骨架流应接近零——这些关节未被雷达检测到，理应静止。SCL 直接惩罚其非零流的幅值：

$$\mathcal{L}^{\mathrm{sta}} = \frac{1}{|F_{t}^{\mathrm{sta}}|} \sum_{k=1}^{|F_{t}^{\mathrm{sta}}|} \| \mathcal{F}_{t}^{\mathrm{sta}}[k] \|_{2}$$

伪标签估计器的总损失为监督 MSE 损失与 UTCL 的加权和：$L = L^{\mathrm{lab}} + \lambda^{\mathrm{con}} L^{\mathrm{con}}$，其中 $L^{\mathrm{con}} = \mathrm{DCL} + \mathrm{SCL}$。

**关键证据**：消融实验（Table 4）表明，DCL 和 SCL 单独使用时均无法显著提升跨域泛化性能，但二者组合使用带来了实质性的增益——在 F→B 设定下，加入 UTCL 后 MPJPE 从 15.22 cm 降至 14.89 cm。这表明 UTCL 的两个分量具有互补性，共同将毫米波雷达的运动检测先验注入伪标签生成过程。

### 闭环点云转换器与流基点过滤（FPF）

直接将 LiDAR 数据集作为附加训练数据使用，由于 LiDAR 与毫米波雷达在点云属性（密度、噪声模式、运动灵敏度等）上存在本质分布差异，效果有限。EMDUL 提出一个**闭环点云转换流水线**，将 LiDAR 点云转换为毫米波风格点云，转换步骤按序执行：**噪点添加（NPA）→ 流基点过滤（FPF）→ 随机采样（RS）→ 坐标噪声注入（NI）**。

其中，**流基点过滤（FPF）** 是最关键的创新模块。它模拟毫米波雷达的运动检测机制：首先基于 LiDAR 数据集已有的骨架标注计算骨架流，再通过反距离加权插值得到点云流：

$$w_t[i,j] = \frac{1}{\lVert P_t[i] - S_t'[j] \rVert_2 + \epsilon}, \quad \tilde{w}_t[i,j] = \frac{w_t[i,j]}{\sum_{k=1}^{J+8} w_t[i,k]}, \quad F_t^P = \tilde{w}_t F_t^{\prime S}$$

随后，以正比于点流幅值的概率保留点云点：

$$\mathcal{P}(P_t[i] \in P_t^{\mathrm{conv}}) = \min\Big(\frac{\lVert F_t^P[i] \rVert_2}{v_t}, 1\Big)$$

其中 $v_t \sim U[\gamma, \delta]$ 为随机采样的流阈值。这一机制使得运动幅度大的点更可能被保留，静态点则大概率被滤除，从而逼真再现毫米波雷达仅检测运动目标的特性。

**关键证据**：
- 消融实验（Table 5/Table 11）显示，去掉 FPF 后 MPJPE 从 14.89 cm 升至 15.47 cm，FPF 贡献最为显著；去掉流水线中任一模块均导致性能下降。
- 在二元分类器判别实验中（Table 7），使用 FPF 后 60.46% 的转换 LiDAR 点云被判定为毫米波数据，而无 FPF 时仅 43.06%，验证了 FPF 对转换逼真度的关键作用。

### 两个维度的协同效应

EMDUL 的两个模块设计为相互独立、可叠加使用。实验表明，同时使用伪标签扩展（无标签毫米波数据）和点云转换扩展（LiDAR 数据集）可获得最佳性能——在仅 10% 标记数据的极端设定下，EMDUL + P4T 在 MM-Fi 域内测试中 MPJPE 达 10.06 cm（基线 12.23 cm），跨域测试（mmBody→MM-Fi）中 MPJPE 达 24.01 cm（基线 33.62 cm），分别降低 17.7% 和 28.6% 的误差。这一协同增益源于两个维度分别从**数据体量**（无标签数据利用）和**姿态多样性**（LiDAR 数据集转换）两个互补方向扩充了训练分布。



**EMDUL** 的整体设计围绕一个核心目标展开：在毫米波人体姿态估计（HPE）任务中，以极低的标注成本，同时利用**无标签毫米波数据**和**带标注的LiDAR数据集**，大幅度扩充训练数据的体量与多样性，从而提升模型的域内与跨域泛化能力。其系统架构由两个相互独立的模块构成：

1.  **伪标签估计器（Pseudo‑label Estimator）**：为无标签毫米波数据生成可靠的伪标签。
2.  **闭环点云转换器（Closed‑Form PC Converter）**：将LiDAR点云转化为逼真的毫米波风格点云。

两个模块协同工作，共同构建**扩展数据集** `D_exp`，随后用于从头训练最终的推理HPE模型。图2展示了这一完整流水线。

### 数据流与模块协作

EMDUL 的输入包含三部分数据：
- **有标签毫米波数据集** `D_lab`：用于监督训练伪标签估计器，并提供最终的扩展数据集基础。
- **无标签毫米波数据集** `D_unlab`：通过伪标签估计器赋予伪标签，形成 `D_pl`。
- **带标注的LiDAR数据集** `D_lidar`：经闭环点云转换器处理后，生成毫米波风格的带标注点云 `D_conv`。

最终的扩展数据集为上述三者的并集：
```
D_exp = D_lab ∪ D_pl ∪ D_conv
```

在每一轮训练迭代中，系统**先更新伪标签估计器并重新为 `D_unlab` 生成伪标签**，再在最新的 `D_exp` 上从头训练推理HPE模型 `θ_infer`。这种在线更新的策略确保了伪标签质量随估计器能力提升而持续改善。

### 伪标签估计器与无监督时间一致性损失

伪标签估计器 `θ_pl` 的核心创新在于其训练方式：它并不仅仅依赖有标签数据的监督信号，而是**同时在无标签数据上施加无监督时间一致性损失（UTCL）**。UTCL 由两个互补的组件构成：
- **动态一致性损失（DCL）**：鼓励那些在物理空间中靠近毫米波检测点的关节具有足够大的运动幅度，以符合毫米波雷达对运动目标的敏感检测特性。
- **静态一致性损失（SCL）**：惩罚那些远离检测点的关节产生非零运动，强制它们保持静止。

这种设计直接利用了毫米波雷达的物理先验——**雷达只能检测到运动目标，静止物体不产生回波点**。通过 UTCL，伪标签估计器学会生成在时序上与毫米波点云观测物理一致的人体姿态序列，从而显著提升伪标签的可靠性。

### 闭环点云转换器

该模块将LiDAR点云转换为毫米波风格点云，其转换流水线由四个顺序执行的增强操作组成：

```
NPA → FPF → RS → NI
```

1.  **噪点添加（NPA）**：引入随机噪点，模拟毫米波雷达的多径反射和杂波。
2.  **流基点过滤（FPF）**：这是转换流水线的核心。它首先利用带标注的LiDAR骨架流插值得到逐点的运动流，然后**以正比于点流幅值的概率保留点**——运动剧烈的点更可能被保留，静止或微动点则大概率被滤除。这一机制直接模拟了毫米波雷达的“运动检测”特性。
3.  **随机采样（RS）**：模拟毫米波雷达点云密度低且不均匀的特点。
4.  **坐标噪声注入（NI）**：模拟毫米波雷达在距离、角度测量上的固有噪声。

图4逐步展示了每个操作对点云属性的影响，直观地呈现了从稠密、完整的LiDAR点云到稀疏、仅保留运动区域的毫米波风格点云的转变过程。

### 关键设计选择

- **硬件无关的点特征**：为提升跨数据集泛化的公平性，EMDUL 仅使用点云的三维坐标（尤其是高度信息）作为输入特征，避免了对硬件相关的多普勒速度等特征的依赖。
- **标准化骨架结构**：所有数据集统一映射到15个关键点的标准化骨架，确保不同数据源之间的标注一致性。
- **模块独立性**：伪标签估计器和点云转换器可独立运行，分别解决无标签数据利用和LiDAR数据迁移两个子问题，使得框架具备良好的可扩展性——任一模块的改进均可直接提升整体性能。

### 补充图表

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/002_Figure_2.jpg]]
*Figure 2: The overview of EMDUL integrating both PC conversion and pseudo-labeling modules*



### 伪标签估计器与无监督时间一致性损失

EMDUL 的伪标签估计器 $\theta_{\text{pl}}$ 同时利用有标签毫米波数据和无标签毫米波数据进行训练。其核心创新在于引入 **无监督时间一致性损失（Unsupervised Temporal Consistency Loss, UTCL）**，迫使伪标签满足毫米波雷达的运动检测物理先验。

毫米波雷达的核心工作机制是：只有当关节存在足够运动时，其附近才会产生检测点。基于这一观察，UTCL 将骨架关节划分为动态集合与静态集合，并分别施加约束。

**动态关节集合**定义为距离最近点云点小于阈值 $\mu$ 的关节：

$$F_{t}^{\mathrm{dyn}} = \{ \hat{F}_{t}^{S}[j] : \min_{i} \| \hat{S}_{t}[j] - P_{t}[i] \|_{2} < \mu \}$$

其中 $\hat{F}_{t}^{S}$ 为骨架流向量，$\hat{S}_{t}[j]$ 为关节 $j$ 的位置，$P_{t}[i]$ 为点云中的点。**动态一致性损失（DCL）** 惩罚流幅值低于阈值 $\eta$ 的动态关节，鼓励其保持运动：

$$\mathcal{L}^{\mathrm{dyn}} = \frac{1}{|F_{t}^{\mathrm{dyn}}|} \sum_{k=1}^{|F_{t}^{\mathrm{dyn}}|} \max(0, \eta - \| F_{t}^{\mathrm{dyn}}[k] \|_{2})$$

**静态关节集合**定义为距离最近点云点大于阈值 $\rho$ 的关节：

$$F_{t}^{\mathrm{sta}} = \{ \hat{F}_{t}^{S}[j] : \min_{i} \| \hat{S}_{t}[j] - P_{t}[i] \|_{2} > \rho \}$$

**静态一致性损失（SCL）** 惩罚静态关节的非零流，鼓励其保持静止：

$$\mathcal{L}^{\mathrm{sta}} = \frac{1}{|F_{t}^{\mathrm{sta}}|} \sum_{k=1}^{|F_{t}^{\mathrm{sta}}|} \| \mathcal{F}_{t}^{\mathrm{sta}}[k] \|_{2}$$

伪标签估计器的总损失为监督 MSE 损失与 UTCL 的加权和：

$$\mathcal{L} = \mathcal{L}^{\mathrm{lab}} + \lambda^{\mathrm{con}} \mathcal{L}^{\mathrm{con}}$$

其中 $\mathcal{L}^{\mathrm{con}} = \mathcal{L}^{\mathrm{dyn}} + \mathcal{L}^{\mathrm{sta}}$，$\lambda^{\mathrm{con}}$ 为平衡权重。实验配置中，$\mu = 20$ cm，$\eta = 5$ cm，$\rho = 5$ cm，$\lambda^{\mathrm{con}} = 0.01$。

消融实验（Table 4）验证了 UTCL 的关键作用：在 F→B 设定下，仅使用监督伪标签（无 UTCL）时 MPJPE 为 15.22 cm，加入 UTCL 后降至 14.89 cm。更重要的是，DCL 和 SCL 单独使用时均无法独立提升跨域泛化性能，但二者组合使用才能带来显著增益——这印证了动态/静态一致性联合约束的必要性。

### 闭环点云转换流水线

为将 LiDAR 数据集转换为毫米波风格点云，EMDUL 设计了闭环转换流水线，按顺序施加四步增强：**噪点添加（NPA）→ 流基点过滤（FPF）→ 随机采样（RS）→ 坐标噪声注入（NI）**。

其中，**流基点过滤（Flow-based Point Filtering, FPF）** 是流水线的核心模块，直接模拟毫米波雷达的运动检测机制。其计算流程如下：

首先，将骨架流插值为点云流。定义点 $P_t[i]$ 到扩展关节 $S_t'[j]$ 的反距离权重：

$$w_t[i,j] = \frac{1}{\lVert P_t[i] - S_t'[j] \rVert_2 + \epsilon}$$

其中 $\epsilon = 10^{-6}$ 防止除零。归一化后得到：

$$\tilde{w}_t[i,j] = \frac{w_t[i,j]}{\sum_{k=1}^{J+8} w_t[i,k]}$$

点云流即为扩展骨架流的线性组合：

$$F_t^P = \tilde{w}_t F_t^{\prime S}$$

随后，以正比于点流幅值的概率保留点，模拟毫米波雷达对运动目标的敏感检测：

$$\mathcal{P}(P_t[i] \in P_t^{\mathrm{conv}}) = \min\Big(\frac{\lVert F_t^P[i] \rVert_2}{v_t}, 1\Big)$$

其中 $v_t \sim \mathcal{U}[\gamma, \delta]$ 为随机采样的流阈值，实验配置中 $\gamma = 2$ cm，$\delta = 5$ cm。该机制使得运动幅度越大的点被保留的概率越高，逼真再现了毫米波雷达仅检测运动目标的物理特性。

消融实验（Table 5 / Table 11）表明，FPF 是流水线中贡献最显著的模块：去掉 FPF 后 MPJPE 从 14.89 cm 升至 15.47 cm；去掉任一模块均导致性能下降。此外，真实性验证实验（Table 7）显示，使用 FPF 后 60.46% 的转换 LiDAR 点云被二元分类器判定为毫米波数据，而无 FPF 时仅 43.06%，定量证明了 FPF 对转换逼真度的关键贡献。

### 模块间的协同关系

伪标签估计器与点云转换流水线在 EMDUL 框架中相互独立但协同工作。每次训练迭代中，$\theta_{\text{pl}}$ 先更新并重新生成伪标签 $D_{\text{pl}}$，随后推理 HPE 模型 $\theta_{\text{infer}}$ 在扩展数据集 $D_{\text{exp}} = D_{\text{lab}} \cup D_{\text{pl}}$ 上从头训练。转换后的 LiDAR 数据 $D_{\text{lidar}}$ 则直接作为额外训练样本加入。这种解耦设计使得两个模块可以独立优化，同时共同扩充数据集的体量和多样性。

### 补充图表

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/004_Figure_4.jpg]]
*Figure 4: Step-by-step visualization of the point-cloud (PC) conversion pipeline Blue joints have lower flow magnitudes and yellow joints higher ones*

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/011_Figure_6.jpg]]
*Figure 6: Comparison of pseudo-labels generated with and without UTCL. (a) Two consecutive ground-truth skeletons in*



## 实验与关键发现

### 核心实验设定

实验在两个毫米波人体姿态估计数据集上进行：**MM-Fi**（321K帧，4个场景）和**mmBody**（200K帧，9个场景）。为模拟数据稀缺的真实场景，主实验仅使用10%的标记数据训练，剩余90%作为无标签数据。LiDAR数据集**HmPEAR**用于点云转换扩展。所有实验统一使用15个关键点的标准化骨架结构，输入为连续5帧、每帧截断或填充至256个点的点云序列。评估指标采用**MPJPE**（平均关节位置误差）和**PA-MPJPE**（Procrustes对齐后的MPJPE），单位均为厘米。

为消除硬件差异对跨域泛化的干扰，点特征仅使用与硬件无关的**高度坐标**，而非多普勒速度等设备相关特征。这一选择经初步实验验证（Table 3），在跨域场景下具有更好的泛化公平性。

### 主实验结果

**Table 1** 展示了EMDUL与现有方法的全面对比。在域内设定（MM-Fi → MM-Fi，记作F→F）中，EMDUL使P4T的MPJPE从12.23 cm降至10.06 cm，使SPiKE从11.85 cm降至10.40 cm，整体误差降低**15.1%**。在跨域设定（mmBody → MM-Fi，记作B→F）中，EMDUL使P4T的MPJPE从33.62 cm降至24.01 cm，降幅达**18.9%**，远超域内改进幅度，表明数据扩展对分布外泛化的增益尤为显著。

与其他HPE基线模型（PT、mmDiff）相比，EMDUL扩展后的P4T在所有设定下均取得最优或接近最优的性能。值得注意的是，在仅使用10%标记数据且不引入LiDAR数据的设定下，EMDUL的伪标签模块（EMDUL-PL）已使P4T的MPJPE从12.23 cm降至10.69 cm（F→F），验证了无标签数据利用的有效性。

**Table 2** 对比了EMDUL与经典半监督方法Mean Teacher在不同LiDAR数据源下的表现。EMDUL在F→B设定下以14.89 cm的MPJPE显著优于MT的16.12 cm，且这一优势在不同LiDAR数据集上保持稳定，表明闭环点云转换流水线比简单的伪标签策略更能弥合LiDAR与毫米波数据之间的分布差异。

### 消融实验

#### 伪标签模块消融

**Table 4** 分析UTCL各组件的作用。在F→B设定下，仅使用监督MSE损失训练伪标签估计器时MPJPE为15.22 cm。单独添加动态一致性损失或静态一致性损失均未带来显著提升，但**两者组合使用**后MPJPE降至14.89 cm。这一结果表明，UTCL的动态/静态约束具有互补性——单独约束某一类关节无法充分捕获毫米波雷达的运动检测物理先验，只有同时迫使“近点关节运动、远点关节静止”才能生成时间一致的伪标签。

**Figure 6** 提供了定性证据：不使用UTCL的伪标签在连续帧之间出现明显的关节抖动，而UTCL约束后的伪标签在时间维度上更加平滑稳定。

#### 点云转换模块消融

**Table 5** 对闭环点云转换流水线的四个模块进行消融。完整流水线（NPA → FPF → RS → NI）在F→B设定下MPJPE为14.89 cm。逐一移除各模块后性能均下降，其中**移除FPF**导致MPJPE升至15.47 cm，降幅最大，验证了流基点过滤是模拟毫米波运动检测机制的核心环节。移除噪点添加、随机采样或坐标噪声注入也分别导致不同程度的性能退化。

**Table 11**（补充材料）提供了更全面的消融，进一步确认FPF在所有模块中贡献最显著，且各模块之间存在协同效应。

#### 超参数敏感性

**Table 6** 分析UTCL和FPF的关键超参数。UTCL的动态关节距离阈值μ、流幅值阈值η以及静态关节距离阈值ρ在合理范围内（μ∈[10,30] cm，η∈[3,7] cm，ρ∈[3,7] cm）时性能稳定。FPF的流阈值采样范围γ和δ同样表现出一定的鲁棒性。这表明方法对超参数不敏感，无需精细调参即可获得稳定增益。

#### 转换点云真实性验证

**Table 7** 通过二元分类任务量化转换点云的真实性。训练一个区分毫米波与LiDAR点云的分类器后，使用FPF的转换点云有**60.46%**被判定为毫米波数据，而无FPF时仅43.06%。这一差距直接证明了FPF能有效赋予LiDAR点云毫米波雷达的运动检测特征，使转换后的点云在统计上更接近真实毫米波数据。

### 极端低资源场景

**Table 8** 测试了不同标记数据比例下的性能。在仅使用**1%标记数据**的极端设定下，EMDUL以MPJPE 14.77 cm大幅领先MT的18.40 cm（F→B），降幅达19.7%。随着标记数据比例增加，EMDUL的优势持续保持但差距缩小，说明数据扩展在标注极度稀缺时价值最大。

### LiDAR数据规模的影响

**Table 10**（补充材料）消融了LiDAR数据使用量。随着HmPEAR数据使用比例从25%增至100%，MPJPE从15.71 cm单调降至14.89 cm，未出现饱和迹象，暗示引入更多样化的LiDAR数据可能带来进一步增益。

### 失败模式与局限性

尽管EMDUL在跨域泛化上取得显著提升，仍存在以下不足：

1. **转换流水线的经验性**：NPA的噪点数量、FPF的流阈值范围、RS的采样点数等参数基于经验设定，可能不适用于所有LiDAR数据集或雷达型号。缺乏自适应的参数学习机制是当前流水线的主要局限。
2. **复杂运动的伪标签质量**：UTCL基于“近点运动、远点静止”的简化物理先验，对于快速旋转、自遮挡或多人交互等复杂运动模式，该先验可能失效，导致伪标签质量下降。
3. **单人场景限制**：当前方法仅适用于单人姿态估计，未扩展到多人场景。多人场景中的遮挡、身份匹配等问题需要额外的技术设计。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| **Table 1** | EMDUL在域内降低15.1%误差，跨域降低18.9%误差，跨域增益更显著 |
| **Table 4** | UTCL的动态/静态一致性损失必须组合使用才能提升跨域性能 |
| **Table 5** | FPF是点云转换流水线中贡献最大的模块 |
| **Table 7** | FPF使转换点云被判定为毫米波的比例从43%提升至60% |
| **Table 8** | 在1%标记数据极端设定下，EMDUL仍以19.7%优势领先MT |
| **Figure 6** | UTCL显著改善伪标签的时间一致性和平滑性 |

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/006_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art mmWave HPE methods. Each model is trained with only 10% labeled data from MM-Fi (F) or mmBody (B). Depending on the setting, methods may additionally use the remaining 90% unlabeled mmWave data and/or the LiDAR dataset HmPEAR. All results are reported in centimeters (cm), and lower is better*

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/007_Table_4.jpg]]
*Table 4: Ablation study on pseudo-labeling of unlabeled data*

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/009_Table_5.jpg]]
*Table 5: Ablation study on PC conversion of a LiDAR dataset*

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/013_Table_7.jpg]]
*Table 7: Ratio of PCs classified as mmWave in a binary classification task distinguishing between and mmWave and LiDAR data*

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/014_Table_8.jpg]]
*Table 8: Performance under different ratios of labeled mmWave data*

### 补充图表

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/008_Table_2.jpg]]
*Table 2: Comparison with Mean Teacher (MT) pseudo-labeling when expanding MM-Fi (F) with different LiDAR datasets. P4T [11] serves as the common HPE model*

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/012_Table_6.jpg]]
*Table 6: Ablation study on hyperparameters in UTCL and FPF under F→B*

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/001_Figure_1.jpg]]
*Figure 1: Examples illustrating the effect of dataset expansion. (a) Samples from an mmWave HPE training dataset. (b) Samples from a LiDAR dataset with richer pose diversity used for dataset expansion; (c) An mmWave PC from an unseen scenario. (d) The ground-truth skeleton. (e) The predicted skeleton of SOTA P4T [11] without expansion. (f) The predicted skeleton of P4T trained on EMDUL-expanded dataset. Joints are colored red for errors > 10 cm and green otherwise. EMDUL achieves stronger generalization ability than the baseline P4T*

![[assets/figures/papers/paper_list_l1018_https_arxiv_org_abs_2603_14507/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the motion-detection mechanism in mmWave radar using an MM-Fi sample. Joints with high flow (yellow) lie close to detected points, while low-flow joints (dark blue) have no nearby points*



## 定位与知识库关联

### 1. 方法谱系

EMDUL 处于毫米波人体姿态估计（mmWave HPE）与半监督/跨模态数据扩展的交叉点，其核心贡献在于**同时利用无标签毫米波数据和有标签LiDAR数据**来扩充训练集，而非改进HPE骨干网络本身。其方法谱系可从以下三条线索追溯：

**（1）毫米波HPE骨干网络**
EMDUL 的推理HPE模型直接复用现有骨干，包括：
- **P4T** (Fan et al., CVPR 2021)：基于Transformer的时序点云处理模型，是文中主要的HPE基线。
- **SPiKE** (Ballester et al., 2024)：较新的mmWave HPE方法。
- **PT** (Zheng et al., ICCV 2021)：Transformer-based HPE基线。
- **mmDiff** (Fan et al., 2024)：扩散模型驱动的HPE基线。

这些骨干在未扩展数据集上的性能构成了EMDUL的参照系。EMDUL的增益完全来自数据扩展，而非模型架构创新——这一设计选择使得该方法具有**骨干无关性**，可适配任意HPE模型。

**（2）半监督伪标签方法**
在无标签数据利用方面，EMDUL 的直接基线是 **Mean Teacher (MT)** (Tarvainen & Valpola, NIPS 2017)。MT 通过教师-学生一致性约束实现半监督学习，但在mmWave HPE场景下，其伪标签缺乏对毫米波物理特性的显式建模。EMDUL 的改进在于：
- 将MT的一致性约束替换为**无监督时间一致性损失（UTCL）**，该损失直接编码了毫米波雷达的**运动检测物理先验**——即只有运动关节附近才存在点云检测点。
- 伪标签估计器与推理模型**解耦**，每次epoch先更新估计器并重新生成伪标签，再从头训练推理模型，避免了MT中教师-学生耦合可能带来的确认偏差。

**（3）跨模态数据转换**
在LiDAR数据利用方面，直接使用LiDAR点云训练mmWave HPE模型效果有限（分布差异大）。EMDUL 提出**闭环点云转换流水线**，其核心创新在于：
- **流基点过滤（FPF）**：这是流水线中最关键的模块。FPF基于骨架流插值得到点云流，以正比于流幅值的概率保留点，从而模拟毫米波雷达对运动目标的敏感检测机制。这一设计将毫米波的物理成像原理转化为可微的概率过滤操作。
- 其余模块（噪点添加NPA、随机采样RS、坐标噪声注入NI）解决点云密度和噪声属性的对齐问题。

### 2. 适用边界

**（1）数据条件**
- EMDUL 假设存在**少量有标签毫米波数据**（实验中低至1%仍有效）、**大量无标签毫米波数据**（同域或跨域）以及**有标签LiDAR数据集**。三者缺一不可。
- 当仅有有标签毫米波数据时，EMDUL退化为标准监督训练，无扩展增益。
- LiDAR数据集需包含与目标mmWave数据集兼容的15关键点骨架标注。

**（2）场景条件**
- 当前方法仅适用于**单人HPE**，未扩展到多人场景。多人场景下的遮挡、交互和身份关联问题未被处理。
- 实验覆盖的数据集为 MM-Fi（4个场景，321K帧）和 mmBody（9个场景，200K帧），场景多样性有限。对其他毫米波雷达硬件或更复杂环境的泛化性尚未验证。

**（3）物理先验的依赖性**
- UTCL 的有效性依赖于毫米波雷达“运动检测”机制的普适性。对于采用不同信号处理流水线的雷达设备，该先验可能不完全成立。
- FPF 的流阈值 $v_t \sim U[\gamma, \delta]$ 依赖经验设定（$\gamma=2\text{cm}, \delta=5\text{cm}$），对不同运动速度分布的场景可能需要重新校准。

### 3. 局限与开放问题

**（1）已确认的局限**
- **经验参数依赖**：PC转换流水线的所有模块（NPA的噪声分布、FPF的流阈值、RS的采样率、NI的噪声幅度）均依赖手工设定的参数。这些参数在MM-Fi和mmBody间可能需要独立调优。
- **运动模式覆盖不足**：UTCL仅通过流幅值阈值区分动态/静态关节，无法捕捉复杂运动模式（如旋转、加速度变化、非刚性变形）。
- **单人限制**：方法框架假设场景中仅存在单个人体，无法处理多人HPE中的检测、关联和遮挡问题。

**（2）开放问题**
- **自适应转换**：能否设计可学习的点云转换模块（如基于GAN或扩散模型），自动适配不同LiDAR数据集的分布特征，替代手工设计的闭环流水线？
- **时序建模增强**：当前UTCL仅利用相邻帧的骨架流信息。引入更长时序依赖（如时序注意力、状态空间模型）是否可进一步提升伪标签的时间一致性和鲁棒性？
- **多人扩展**：如何将EMDUL的数据扩展策略迁移至多人HPE？需要解决的关键问题包括：多人检测与身份关联、跨人体遮挡导致的点云缺失、以及多人交互场景下的运动模式建模。
- **跨硬件泛化**：当前实验仅覆盖特定毫米波雷达设备。不同雷达的波形设计、天线阵列和信号处理算法会导致点云属性（密度、噪声统计、检测灵敏度）的系统性差异。EMDUL的转换流水线能否通过域自适应方法泛化到未见雷达硬件，是一个重要的工程问题。

### 4. 知识库定位

EMDUL 的核心知识贡献在于：
1. **物理先验驱动的无监督损失设计**：UTCL 将毫米波雷达的成像物理（运动→检测）编码为可微损失函数，为其他物理感知任务提供了范式参考。
2. **闭环跨模态转换的模块化设计**：FPF作为关键创新模块，以概率过滤方式桥接LiDAR和毫米波点云的属性差异，其“骨架流插值→流幅值过滤”的思路可推广至其他点云模态转换任务。
3. **数据扩展的骨干无关性验证**：在多个HPE骨干（P4T、SPiKE）上一致取得显著增益，证明了数据层面的改进比模型层面的改进更具通用价值。

在更广泛的半监督学习和跨模态学习领域，EMDUL 属于**物理先验增强的半监督跨模态数据扩展**方法，与纯数据驱动的域自适应（如对抗域适应）和纯半监督方法（如FixMatch）形成互补。其关键区别在于对源模态和目标模态之间**物理成像机制的显式建模**，而非仅依赖统计分布对齐。



## 原文 PDF

![[paperPDFs/CVPR_2026/Expanding_mmWave_Datasets_for_Human_Pose_Estimation_with_Unlabeled_Data_and_LiDAR_Datasets.pdf]]
