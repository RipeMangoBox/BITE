---
title: "GIPSO: Geometrically informed propagation for online adaptation in 3d lidar segmentation"
type: paper
paper_level: A
venue: ECCV
year: 2022
pdf_ref: paperPDFs/ECCV_2022/GIPSO_Geometrically_informed_propagation_for_online_adaptation_in_3d_lidar_segmentation.pdf
project_link: null
code_link: https://github.com/saltoricristiano/gipso-sfouda
aliases:
- GIPSO
tags:
- ECCV_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "利用基于MC Dropout的逐类自适应不确定性阈值选择可靠种子伪标签，并通过辅助几何特征编码器将这些标签传播到几何相似区域，同时施加时间一致性约束以平滑在线适应过程。"
primary_logic: "低层几何特征具有跨域泛化能力，可用于引导伪标签扩散；结合类平衡的自适应阈值可以有效缓解伪标签偏差；自监督时间一致性进一步稳定在线适应过程。"
claims:
- "自适应伪标签选择（A）单独带来 +1.07 mIoU 改进，与时间一致性（T）结合提升至 +3.65，最终加入几何传播（P）达到 +4.31 mIoU。"
- "基于不确定性的选择在 Top-1 准确率上优于质心和置信度选择，Top-1 准确率 66.7。"
- "GIPSO 在 Synth4D → SemanticKITTI 上平均 mIoU 提升 +4.31，大幅领先其他在线和离线方法。"
- "Synth4D → SemanticKITTI 上 mIoU improvement over Source = +4.31"
---

# GIPSO: Geometrically informed propagation for online adaptation in 3d lidar segmentation

> [!tip] 核心洞察
> 低层几何特征具有跨域泛化能力，可用于引导伪标签扩散；结合类平衡的自适应阈值可以有效缓解伪标签偏差；自监督时间一致性进一步稳定在线适应过程。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GIPSO：面向3D LiDAR分割的几何引导在线自适应传播 |
| 英文题名 | GIPSO: Geometrically informed propagation for online adaptation in 3d lidar segmentation |
| 会议/期刊 | ECCV 2022 |
| Links | [paper](https://arxiv.org/abs/2207.09763) · [GitHub](https://github.com/saltoricristiano/gipso-sfouda) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GIPSO |
| Dataset | Synth4D → SemanticKITTI, SynLiDAR → SemanticKITTI, Synth4D → nuScenes |

> [!tip] 效果简介
> - Synth4D → SemanticKITTI 上，mIoU improvement over Source 为 +4.31，对比 CBST* (+0.28)，变化 +4.03。
> - SynLiDAR → SemanticKITTI 上，mIoU improvement over Source 为 +3.70，对比 CBST* (+0.28)，变化 +3.42。
> - Synth4D → nuScenes 上，mIoU improvement over Source 为 +0.85，对比 Source (no adaptation)，变化 +0.85。

## 概要

### 问题背景与瓶颈

3D LiDAR点云语义分割是自动驾驶感知的核心任务，但模型在跨传感器、跨场景部署时面临严重的域迁移问题。现有域适应方法大多遵循离线范式，需要同时访问源域数据和目标域数据，这与真实自动驾驶场景中源数据不可得、目标数据在线到达的约束根本冲突。更关键的是，传统的伪标签选择策略——无论是基于置信度排序还是基于类质心距离——在动态环境下的类别分布变化面前容易产生过自信的错误标签，导致模型在线适应时发生灾难性遗忘甚至崩溃。

**GIPSO**（Geometrically Informed Propagation for Online Adaptation）正是为解决这一**在线源自由无监督域适应**（SF-OUDA）问题而提出的。该方法仅需一个在合成数据上预训练的分割模型，即可在目标域数据流到达时持续在线适应，无需任何源数据或目标域标注。

### 核心洞察与方法定位

GIPSO的核心洞察在于：**低层几何特征具有跨域泛化能力**，可以作为伪标签扩散的可靠引导信号。方法由三个协同组件构成：

1. **自适应伪标签选择**：利用MC Dropout计算逐点不确定性，为每个类别设定自适应阈值，选择最可靠的种子伪标签，有效缓解类不平衡下的伪标签偏差。
2. **几何引导传播**：通过辅助几何特征编码器提取局部几何描述符，将种子标签沿几何相似区域扩散，使标签覆盖范围远超传统空间近邻传播。
3. **时间一致性正则**：基于SimSiam框架的自监督损失，利用里程计信息关联连续帧的对应点，强制语义特征在时间维度上平滑演化。

### 主要结果概览

在Synth4D→SemanticKITTI基准上，GIPSO相比源模型实现**+4.31 mIoU**的提升，大幅领先所有在线基线方法（次优方法CBST*仅+0.28 mIoU）。消融实验证实三个组件的因果贡献：自适应选择单独带来+1.07 mIoU，加入时间一致性提升至+3.65，最终几何传播达到+4.31。在SynLiDAR→SemanticKITTI和Synth4D→nuScenes上同样取得显著增益（+3.70和+0.85 mIoU），验证了方法的跨数据集泛化能力。

### 方法谱系与知识库定位

GIPSO属于**在线源自由域适应**方法，其技术路线融合了自训练、几何感知传播和自监督时间学习三条线索。与离线方法（如ADABN通过批归一化统计适配、RayCast通过光线投射生成目标样式源数据）不同，GIPSO完全在目标域在线运行。与同期在线方法相比：CBST*和ProDA*依赖置信度或质心选择伪标签，TPLD*使用空间最近邻传播，而GIPSO的**不确定性驱动自适应阈值+几何传播+时间平滑**三重机制构成了差异化技术路径。方法在3D点云域适应领域首次系统性地将几何特征传播与在线自训练相结合，开辟了利用低层几何先验引导高层语义适应的新范式。

### 3D点云语义分割的域迁移困境

基于深度学习的3D LiDAR点云语义分割模型在自动驾驶感知中扮演关键角色，但其性能高度依赖大规模高质量标注数据。由于真实场景的点云标注成本极高，研究者普遍借助合成数据集（如GTA-V、Synthia、CARLA等）生成带标签的训练数据。然而，合成数据与真实传感器采集的点云之间存在显著的**域差异**——包括激光雷达的物理特性（波束数量、扫描模式、点密度）、环境光照、物体材质和场景布局等因素——导致在源域上训练的模型直接部署到目标域时性能急剧退化。

### 离线域适应的局限性与在线源自由需求

现有域适应方法主要沿两条路径展开：

- **无监督域适应（UDA）**：同时访问源数据和目标数据，通过对抗训练、风格迁移或自训练进行离线对齐。代表性工作包括 **RayCast**（通过光线投射生成目标样式的源数据）、基于批归一化统计的 **ADABN** 等。
- **源自由域适应（SFDA）**：仅使用预训练源模型和目标数据，避免直接访问源数据。例如 **SHOT** 利用信息最大化进行原型适应，**ProDA** 采用基于质心的去噪权重策略。

然而，上述方法均为**离线范式**（Figure 1）：需要收集完整的目标域数据后进行批量处理。在自动驾驶等实际部署场景中，车辆驶入一个未见过的环境时，模型必须在**每一帧到来时立即适应**，无法等待积累足够的目标数据，更无法访问源数据。这种**在线源自由无监督域适应（SF-OUDA）**的设定对现有方法构成了根本性挑战。

### 在线自训练的伪标签陷阱

在线域适应最直接的思路是**自训练**——利用源模型对当前帧的预测作为伪标签进行微调。但在SF-OUDA设定下，这一策略面临两个核心瓶颈：

1. **伪标签质量失控**：源模型在目标域上的预测本身存在大量错误，不加筛选地使用伪标签会导致错误累积和模型崩溃。传统伪标签选择策略——如基于最大置信度（**CBST***）或类质心距离（**ProDA***）——在动态环境中表现出明显缺陷：置信度高的预测未必正确（过自信问题），而质心方法在类别分布变化的在线场景下难以维持准确的类原型。

2. **标签稀疏与信息浪费**：即使筛选出少量可靠的种子伪标签，这些标签通常只覆盖点云中极少的点。现有方法如 **TPLD*** 尝试通过3D空间最近邻传播来稠密化标签，但简单的空间距离无法捕捉语义边界，容易跨越物体边界进行错误传播。

### 几何信息的跨域泛化潜力

值得注意的是，尽管高层语义特征在域间差异显著，**低层几何特征**——如局部表面法向量、曲率、邻域结构等——具有更强的跨域泛化能力。无论传感器如何变化，墙面仍然是平面，树干仍然是柱状结构，路缘仍然是高度突变边缘。这一观察暗示：几何信息可以作为跨域传播语义标签的可靠桥梁，而现有方法尚未系统性地利用这一性质。

### GIPSO的核心动机

综上所述，本文的核心动机在于：**在在线源自由的严苛约束下，如何通过自适应伪标签筛选、几何引导的标签传播和时间一致性约束，构建一个稳定且高效的在线域适应框架**。具体需要回答三个关键问题：

- 如何设计一个对类别分布变化鲁棒的伪标签选择机制？
- 如何利用几何特征的跨域泛化性将稀疏种子标签安全地传播到更大区域？
- 如何利用时序信息平滑在线适应过程，防止帧间剧烈波动？

## 核心方法与创新机理

GIPSO 的核心创新在于针对**在线源自由无监督域适应（SF-OUDA）**这一极具挑战性的设定，设计了三个相互协同的机制，系统性地解决了现有方法在动态点云分割中的关键瓶颈。

### 1. 基于不确定性的自适应伪标签选择

传统在线自训练方法（如 CBST*、ProDA*）依赖置信度排序或类质心距离来选择伪标签，在目标域类别分布动态变化时容易产生**过自信的错误标签**，导致模型崩溃。GIPSO 创新性地引入基于 **MC Dropout 方差的逐类自适应不确定性阈值**：

- 首先对源预训练模型 $F_{\mathcal{S}}$ 执行 $J$ 次 Dropout 推理，得到平均输出分布 $p_{\mathcal{T}}^{t}$（公式 1），然后计算其跨类方差作为逐点不确定性指标 $\nu_{\mathcal{T}}^{t}$（公式 2）。
- 对每个类别独立设定阈值，选择不确定性最低的点作为种子伪标签。这种**类平衡的自适应策略**有效缓解了伪标签偏差，尤其在类别分布不均衡的动态场景中优势显著。

Oracle 研究（Table 6）证实，基于不确定性的选择在 Top-1 准确率上达到 **66.7**，显著优于质心选择（36.4）和置信度选择（56.3），验证了该策略在识别可靠伪标签上的根本性优势。

### 2. 几何特征引导的伪标签传播

现有的伪标签稠密化方法（如 TPLD*）仅依赖空间最近邻传播，无法将标签扩散到度量空间中距离较远但几何结构相似的区域。GIPSO 的核心洞察是：**低层几何特征具有跨域泛化能力**，可作为伪标签扩散的可靠引导。

具体而言，GIPSO 引入一个辅助几何特征编码器 $F_{aux}$（基于 PointNet 架构，在源域 Synth4D 上预训练），提取逐点的局部几何描述符。对于每个种子伪标签点 $\tilde{\mathbf{x}}^{t}$，计算其几何特征与所有目标点特征的 L2 距离集合 $\mathcal{G}_{\tilde{\mathbf{x}}}^{t}$（公式 3），将标签传播到几何最相似的 $K$ 个点。这一机制使伪标签能够跨越空间距离，沿几何一致性区域有效扩散（Figure 4 展示了该过程）。

### 3. 自监督时间一致性约束

所有基线方法均未利用点云序列的时间信息，而自动驾驶场景中连续帧之间存在天然的语义平滑性。GIPSO 首次将 **SimSiam 风格的自监督学习框架**引入在线域适应，通过时间一致性损失强制连续帧对应点的语义特征保持一致：

- 利用里程计信息和对最近邻搜索建立时间对应点集合 $\Omega^{t, t-w}$（公式 4）。
- 通过对称的负余弦相似度损失 $\mathcal{L}_{reg}$（公式 5-6）约束预测特征与目标编码器特征的一致性，包含停止梯度操作以防止模式坍塌。

消融实验（Table 5）清晰揭示了各组件的贡献：仅使用自适应伪标签选择（A）可获得 **+1.07 mIoU** 改进；加入时间一致性（A+T）提升至 **+3.65**；最终融入几何传播（A+T+P）达到完整 GIPSO 的 **+4.31 mIoU**。这表明三个创新组件之间存在显著的协同效应，共同构成了 GIPSO 在 SF-OUDA 设定下的性能优势。

GIPSO 是一个面向三维 LiDAR 点云语义分割的在线、源自由无监督域适应（SF-OUDA）方法。其核心 pipeline 由四个主要模块串联构成：**源预训练模型**、**自适应伪标签选择器**、**几何引导传播模块**和**时间一致性约束模块**，最终通过在线更新头完成目标域模型的持续适应。

### 输入输出流

在时刻 $t$，系统仅接收当前目标域点云帧 $X_{\mathcal{T}}^{t}$ 以及里程计提供的相邻帧相对位姿变换 $T_{t-w t}$。**不访问任何源域数据或目标域真实标签**。输出为当前帧的语义分割预测，同时在线更新目标模型参数。

### 模块关系与数据流

1. **源预训练模型 $F_{\mathcal{S}}$** 作为初始教师模型，对 $X_{\mathcal{T}}^{t}$ 进行多次 MC Dropout 推理，产生平均输出分布 $p_{\mathcal{T}}^{t}$（公式 1），为后续伪标签选择提供原始预测和不确定性估计。

2. **自适应伪标签选择器** 基于 $p_{\mathcal{T}}^{t}$ 计算逐点不确定性指数 $\nu_{\mathcal{T}}^{t}$（公式 2），采用**逐类自适应阈值**策略筛选高可靠种子伪标签。该策略有效缓解了传统置信度或质心方法在动态场景下的过自信错误。

3. **几何特征编码器 $F_{aux}$** 独立于语义分支，提取点云的底层几何局部描述符。**几何传播模块**利用这些特征计算种子点与所有目标点的 L2 距离（公式 3），将种子标签扩散到几何最相似的 $K$ 个点，实现跨度量空间的伪标签稠密化。

4. **时间一致性模块** 通过里程计和最近邻搜索建立相邻帧的点对应关系（公式 4），采用 SimSiam 风格的自监督负余弦相似度损失（公式 5-6）约束对应点的语义特征平滑，稳定在线适应过程。

5. **在线更新头** 综合 Dice 损失 $\mathcal{L}_{dice}$（基于传播后的伪标签）和时间正则损失 $\mathcal{L}_{reg}$，以小批量方式更新目标模型参数。

### 关键设计逻辑

三个模块形成递进互补关系：**自适应选择**提供高质量种子标签，**几何传播**将其扩散到几何一致区域，**时间一致性**则跨帧平滑语义特征，三者协同克服了在线场景下伪标签稀疏、噪声大和分布漂移的瓶颈。消融实验证实这一递进关系：仅自适应选择（A）带来 +1.07 mIoU，加入时间一致性（A+T）提升至 +3.65，完整 GIPSO（A+T+P）达到 +4.31 mIoU（Table 5）。


GIPSO 的核心架构由三个相互协同的模块构成：**自适应伪标签选择器**、**几何特征引导的伪标签传播模块**和**自监督时间一致性约束模块**。三者共同作用于一个预训练的源分割模型 $F_{\mathcal{S}}$，实现在线、源自由的域适应。

### 自适应伪标签选择

该模块解决的核心问题是：在目标域数据流到达时，如何从源模型 $F_{\mathcal{S}}$ 的预测中筛选出可靠的伪标签，避免错误标签在在线学习中累积导致模型崩溃。

GIPSO 采用基于 MC Dropout 的不确定性估计。对当前帧点云 $X_{\mathcal{T}}^{t}$，执行 $J$ 次随机 dropout 前向推理，得到平均输出分布：

$$p_{\mathcal{T}}^{t} = \frac{1}{J} \sum_{j=1}^{J} p\left(F_{\mathcal{S}} | X_{\mathcal{T}}^{t}, d_{j}\right)$$

其中 $d_j$ 表示第 $j$ 次 dropout 掩码，$p(\cdot)$ 为 softmax 输出。基于此，逐点的不确定性指标定义为该分布在 $C$ 个类别上的方差：

$$\nu_{\mathcal{T}}^{t} = E\left[\left(p_{\mathcal{T}}^{t} - \mu_{\mathcal{T}}^{t}\right)^{2}\right]$$

方差越大，表明模型对该点的类别归属越不确定。GIPSO 随后采用**逐类自适应阈值**策略：为每个类别 $c$ 设定独立的不确定性阈值，仅选择不确定性低于该类阈值的点作为种子伪标签。这一设计与传统基于置信度排序或类质心的方法形成关键差异——它能够根据目标域各类别的分布动态调整选择标准，有效缓解类别不平衡带来的伪标签偏差。

### 几何特征引导的伪标签传播

自适应选择产生的种子伪标签通常稀疏且仅覆盖高置信度区域。为扩展监督信号密度，GIPSO 引入一个辅助几何特征编码器 $F_{aux}$，将种子标签传播到几何结构相似的区域。

对于每个种子点 $\tilde{\mathbf{x}}^{t}$，计算其与所有目标点 $X_{\mathcal{T}}^{t}$ 在几何特征空间中的 L2 距离集合：

$$\mathcal{G}_{\tilde{\mathbf{x}}}^{t} = \| F_{aux}(\tilde{\mathbf{x}}^{t}) - F_{aux}(X_{\mathcal{T}}^{t}) \|_{2}$$

选取距离最小的前 $K$ 个点，将种子点的伪标签赋予它们。这一机制的底层假设是：低层几何特征（如局部曲率、法向量分布）具有跨域泛化能力，不受纹理或外观域偏移的影响。因此，即使两点在度量空间中相距较远，只要几何结构相似，标签传播就是合理的。

消融实验表明，传播邻域大小 $K=10$ 时性能最优（+4.31 mIoU），过大的 $K$（如 50 或 100）会引入几何相似但语义不同的错误传播，导致性能下降。

### 自监督时间一致性约束

自动驾驶场景中，连续帧之间存在大量重叠区域，对应点的语义预测应当一致。GIPSO 利用这一先验，通过自监督时间一致性损失对在线适应过程施加平滑约束。

首先，利用里程计信息 $T_{t-w, t}$ 将历史帧 $X_{\mathcal{T}}^{t-w}$ 变换到当前帧坐标系，通过最近邻搜索建立时间对应点集合：

$$\Omega^{t, t-w} = \{ \{ \mathbf{x}^{t}, \mathbf{x}^{t-w} \} : \mathbf{x}^{t} = \mathbb{NN}(T_{t-w, t} \circ \mathbf{x}^{t-w}, X_{\mathcal{T}}^{t}), \|\mathbf{x}^{t} - \mathbf{x}^{t-w}\|_{2} < \tau \}$$

其中 $\tau$ 为距离阈值，过滤里程计误差较大的对应点。

借鉴 SimSiam 的自监督框架，GIPSO 将分割网络拆分为编码器 $f$ 和预测头 $h$。对时间对应点对，计算预测特征 $q$ 与目标编码器特征 $z$ 之间的负余弦相似度（目标分支使用停止梯度）：

$$\mathcal{D}_{t, t-w}(q^{t}, z^{t-w}) = - \frac{q^{t}}{\|q^{t}\|_{2}} \cdot \frac{z^{t-w}}{\|z^{t-w}\|_{2}}$$

最终的对称时间一致性损失为：

$$\mathcal{L}_{reg} = \frac{1}{2} \mathcal{D}_{t, t-w}(q^{t}, z^{t-w}) + \frac{1}{2} \mathcal{D}_{t-w, t}(q^{t-w}, z^{t})$$

该损失与 Dice 分割损失 $\mathcal{L}_{dice}$ 联合优化，使模型在适应目标域的同时保持时序上的语义平滑。消融实验证实，时间窗口 $w=6$ 时平均 mIoU 最高（+4.40），过小则平滑不足，过大则引入场景变化带来的噪声。

### 在线模型更新

上述三个模块产生的伪标签 $\hat{Y}_{\mathcal{T}}^{t}$ 和时间对应点对共同驱动目标模型的在线更新。优化目标为：

$$\mathcal{L} = \mathcal{L}_{dice}(F_{\mathcal{T}}(X_{\mathcal{T}}^{t}), \hat{Y}_{\mathcal{T}}^{t}) + \lambda \mathcal{L}_{reg}$$

其中 $F_{\mathcal{T}}$ 由 $F_{\mathcal{S}}$ 初始化，逐帧更新。这种在线学习范式无需存储源数据，也无需访问目标域真实标签，完全符合源自由在线无监督域适应（SF-OUDA）的设定。

## 实验与关键发现

### 1 实验设置

GIPSO 在三个合成到真实的在线域适应基准上进行评估：**Synth4D → SemanticKITTI**、**SynLiDAR → SemanticKITTI** 和 **Synth4D → nuScenes**。所有实验遵循统一的在线评估协议：模型在当前帧进行适应，然后在下一帧评估，报告所有目标序列的平均 mIoU 改进量。源模型均使用 MinkowskiNet 预训练，在线方法统一采用批次大小为 1、学习率为 1e-3 的设置。辅助几何特征编码器 F_aux 采用 PointNet 风格架构，在 Synth4D 上预训练以输出逐点几何描述符。

### 2 主实验结果

**Synth4D → SemanticKITTI**（Table 2）：GIPSO 在源模型基础上实现平均 **+4.31 mIoU** 的改进，大幅领先所有对比方法。离线方法中，ADABN 仅取得 +0.32，RayCast 为 +0.60。在线方法中，ONDA 为 +0.21，而基于自训练的 CBST* 和 TPLD* 分别仅获得 +0.28 和 +0.06。值得注意的是，SHOT* 和 ProDA* 在此设置下出现严重的性能退化（分别为 -0.42 和 -0.62），分析表明这是因为 SemanticKITTI 的长序列导致质心漂移，使得基于原型的适应策略失效。

**SynLiDAR → SemanticKITTI**（Table 3）：GIPSO 取得 **+3.70 mIoU** 的平均改进，同样显著优于 CBST*（+0.28）和 TPLD*（+0.70）。该结果验证了 GIPSO 在不同合成数据源下的鲁棒性。

**Synth4D → nuScenes**（Table 4）：GIPSO 获得 **+0.85 mIoU** 的改进。增益明显小于 SemanticKITTI 上的表现，这与 nuScenes 使用 32 线 LiDAR 导致点云分辨率较低有关——几何特征的判别力在稀疏点云下有所下降。

### 3 消融实验

Table 5 的组件消融揭示了各模块的贡献。仅使用自适应伪标签选择（A）可获得 **+1.07 mIoU** 的改进；加入时间一致性正则化（A+T）后提升至 **+3.65**；进一步引入几何传播（A+T+P，即完整 GIPSO）达到最佳的 **+4.31**。这一递进关系表明：自适应阈值提供了可靠的种子伪标签基础，时间约束大幅稳定了在线适应过程，几何传播则在两者之上进一步扩展了监督信号的覆盖范围。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2207_09763/figures/011_Table_5.jpg]]
*Table 5: Synth4D→SemanticKITTI ablation study of GIPSO: (A) Adaptive thresholding; (A+T) A + Temporal consistency; (A+T+P) A+T + geometric Propagation. Table 6. Oracle study on Synth4D → SemanticKITTI that compares the accuracy of different pseudo-label selection metrics: Centroid, Confidence and Uncertainty*

### 4 伪标签选择策略对比

Table 6 的 Oracle 研究直接比较了不同伪标签选择度量的 Top-1 准确率。基于不确定性的选择策略达到 **66.7%**，显著优于基于置信度的 **56.3%** 和基于质心的 **36.4%**。质心策略的低准确率说明在动态场景中类条件分布快速变化时，类原型极易失效；置信度策略虽然优于质心，但仍容易对错误预测产生过自信。基于 MC Dropout 方差的逐类自适应阈值策略通过类平衡机制有效缓解了这一问题。

### 5 关键超参数分析

**几何传播大小 K**（Supp. Table 1）：K=10 时性能最优（+4.31），K=50 时降至 +3.99，K=100 时进一步下降。过大的传播邻域会将几何相似但语义不同的点错误纳入，引入噪声标签。

**时间窗口 w**（Supp. Table 2）：w=6 时平均 mIoU 最高（+4.40）。窗口过小则时间约束不足，过大则可能引入因场景动态变化产生的错误对应。

### 6 定性分析与失败模式

Fig. 6 展示了三种典型场景的定性分割结果。在大幅改进场景（+27.2 mIoU）中，GIPSO 成功纠正了源模型对道路和建筑物的系统性误分；在中等改进场景（+10.0）中，模型有效恢复了被遮挡的车辆区域；在小幅改进场景（+5.1）中，改进主要来自边界区域的细化。

**主要失败模式**包括：
- **行人类别**：由于严重的类别不平衡，适应性提升有限，这是所有方法的共同瓶颈。
- **几何歧义区域**：具有相似几何结构但不同语义的物体（如低矮墙体与路缘）可能发生错误传播。
- **低分辨率场景**：在 nuScenes 的 32 线 LiDAR 数据上，几何特征的判别力不足，增益显著收窄。
- **尾部类别**：当前方法未使用源数据进行类平衡重加权，导致尾部类别的自适应困难。

### 7 特征质量演变

Fig. 5(b) 使用 Davies-Bouldin Index（DB-Index）追踪了适应过程中特征分离度的变化。GIPSO 的 DB-Index 随时间持续下降，表明语义特征在适应过程中逐渐形成更好的类间分离，这与 mIoU 的逐步提升（Fig. 5(a)）呈正相关。该趋势验证了在线适应不仅改善分类决策边界，也在特征空间层面产生了结构性的正向变化。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2207_09763/figures/009_Figure_5.jpg]]
*Figure 5: (b) Fig. 5. (a) Per-class improvement of GIPSO over time on Synth4D→SemanticKITTI. (b) DB-Index over time on Synth4D→SemanticKITTI. The lower the DB-Index, the better the class separation of the features*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2207_09763/figures/002_Table_1.jpg]]
*Table 1: Comparison between public synthetic datasets and Synth4D in terms of sensor specifications, acquisition areas, number of scans, number of points, presence of odometry data, and whether the semantic classes are all or partially shared*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2207_09763/figures/006_Table_2.jpg]]
*Table 2: Synth4D → SemanticKITTI online adaptation. Source: pre-trained source model (lower bound). We report absolute mIoU for Source and mIoU relative to Source for the other methods. Key. SF: Source-Free. UDA: Unsupervised DA. O: Online*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2207_09763/figures/007_Table_3.jpg]]
*Table 3: SynLiDAR → SemanticKITTI online adaptation. Source: pre-trained source model (lower bound). We report absolute mIoU for Source and mIoU relative to Source for the other methods. Key. SF: Source-Free. UDA: Unsupervised DA. O: Online*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2207_09763/figures/015_Table_3.jpg]]
*Table 3: Ablation study on Synth4D → SemanticKITTI reporting the improvement of state-of-the-art methods by using GIPSO adaptive selection strategy and propagation strategy*

## 定位与知识库关联

### 问题定位：在线源自由域适应的空白

GIPSO 瞄准的是 **SF-OUDA（Source-Free Online Unsupervised Domain Adaptation）** 这一未被充分探索的交叉设定。在 3D LiDAR 语义分割领域，现有域适应方法主要分为两类：**离线 UDA** 和 **源自由 UDA**，但两者均无法满足自动驾驶场景下的在线部署需求。

**离线 UDA 方法**（如 ADABN、RayCast）假设源域和目标域数据可同时访问，通过对抗训练或风格迁移来对齐特征分布。然而，这些方法存在两个根本性限制：（1）需要离线批量处理，无法逐帧适应；（2）依赖源数据，在存储和隐私受限的车载场景中不可行。

**源自由 UDA 方法**（如 SHOT、ProDA）移除了对源数据的依赖，仅使用预训练模型进行目标域适应。但它们的原型更新、去噪权重等机制设计为离线操作，直接迁移到在线场景时会出现严重的类别漂移——例如 SHOT* 和 ProDA* 在长序列上质心迅速偏离（Table 2 中分别仅获得 +0.21 和 -0.29 的 mIoU 改进）。

GIPSO 首次在 3D 点云分割中同时满足 **在线、源自由、无监督** 三个约束，其核心设计逻辑是：低层几何特征具有跨域泛化能力，可作为伪标签传播的可靠媒介；结合时间维度上的自监督平滑，可以在不访问源数据的情况下稳定在线适应过程。

### 与在线自训练方法的关系

GIPSO 的方法论根植于 **在线自训练（Online Self-Training）** 范式，但与现有工作存在关键差异。

**CBST***（类平衡自训练）和 **TPLD***（伪标签稠密化）是 GIPSO 最直接的在线基线。CBST* 采用置信度阈值进行伪标签选择，而 TPLD* 在此基础上增加了 3D 空间最近邻传播。GIPSO 在这两个维度上均做出了实质性改进：

- **伪标签选择**：从置信度排序转向基于 **MC Dropout 方差的逐类自适应不确定性阈值**。实验表明，不确定性选择的 Top-1 准确率达到 66.7，显著优于置信度（56.3）和质心（36.4）（Table 6 Oracle study）。其因果机制在于：置信度仅反映模型对该预测的确信程度，但无法区分“正确的高置信度”和“错误的高置信度”；而不确定性通过多次 dropout 推理的方差捕捉模型的知识边界，能更有效地过滤掉分布外样本上的过自信错误。

- **伪标签传播**：从 3D 空间最近邻（TPLD*）转向 **几何特征空间的相似性传播**。这一改变的深层逻辑是：在动态场景中，空间邻近的物体可能具有完全不同的语义（如停放的汽车与旁边的行人），而几何局部描述符（由 PointNet 风格的辅助编码器 F_aux 提取）能够捕捉形状和结构的相似性，使得标签可以传播到空间上远离但几何上一致的区域（Figure 4）。消融实验证实，仅传播模块（P）的加入在 A+T 基础上额外贡献 +0.66 mIoU（Table 5）。

### 时间约束的自监督实现

GIPSO 的时间一致性损失并非简单的特征平滑，而是借鉴了 **SimSiam**（Chen & He, 2021）的自监督对比学习框架。具体地，利用里程计将前一帧点云变换到当前帧坐标系，通过最近邻搜索建立时间对应点对，然后对预测头输出 q 和目标编码器输出 z 计算负余弦相似度（Equation 5-6）。这种设计的关键在于 **停止梯度（stop-gradient）** 操作——目标分支不接收梯度回传，从而避免了表示坍缩，使得语义特征在时间维度上平滑而不退化。消融实验表明，时间一致性（T）在自适应选择（A）基础上贡献 +2.58 mIoU（Table 5），是三个组件中增益最大的。

### 适用边界与局限

GIPSO 的有效性存在明确的适用边界：

1. **传感器分辨率依赖性**：在 Synth4D → SemanticKITTI（64线 LiDAR）上获得 +4.31 mIoU 改进，但在 Synth4D → nuScenes（32线 LiDAR，点云密度更低）上仅获得 +0.85 mIoU（Table 4）。低分辨率点云导致几何特征描述符的判别力下降，传播精度受损。

2. **类别不平衡的脆弱性**：行人类别由于在源域和目标域中均极度稀疏，自适应提升有限（Figure 5a 中 person 类改进幅度最小）。当前方法未使用任何源数据统计进行类平衡重加权，尾部类别在在线场景下容易被多数类伪标签淹没。

3. **几何-语义歧义**：几何传播假设“几何相似则语义相似”，但这一假设在具有相似结构但不同语义的物体上会失效（如路灯杆与树干）。这是几何引导方法的固有局限，目前缺乏有效的歧义消解机制。

4. **里程计依赖**：时间一致性模块依赖里程计进行帧间对齐，在 GPS 信号丢失或里程计失效的场景下无法正常工作。

### 开放问题

基于上述分析，以下问题值得后续研究关注：

- **无源数据的类平衡策略**：是否可以通过在线估计目标域的类别分布来动态调整伪标签选择阈值，从而缓解尾部类别的适应困难？
- **几何编码器的在线进化**：当前 F_aux 在源域预训练后冻结。如果能在线更新几何编码器以适应目标域的几何分布偏移，传播质量可能进一步提升。
- **多传感器扩展与里程计替代**：能否利用 IMU 或视觉里程计替代激光里程计？如何融合相机纹理信息来消解几何-语义歧义？
- **不确定性阈值的自适应调节**：当前阈值参数 a 为固定值。能否根据目标域的数据流统计特性（如序列级别的难度变化）动态调整 a？

## 原文 PDF

![[paperPDFs/ECCV_2022/GIPSO_Geometrically_informed_propagation_for_online_adaptation_in_3d_lidar_segmentation.pdf]]
