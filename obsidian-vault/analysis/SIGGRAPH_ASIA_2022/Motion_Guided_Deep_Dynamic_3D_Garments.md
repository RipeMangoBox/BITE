---
title: Motion Guided Deep Dynamic 3D Garments
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Motion_Guided_Deep_Dynamic_3D_Garments.pdf
project_link: null
code_link: "https://github.com/MengZephyr/Motion-Guided-Deep-Dynamic-3D-Garment"
aliases:
- MGDD3G
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将服装变形解耦为规范空间局部位移 + 动态蒙皮权重，并先学习一个紧凑的生成潜在空间（正则化自编码器），再学习一个动态感知编码器将历史状态与身体交互映射到该空间。
primary_logic: 先通过生成模型压缩合理服装变形的流形，再利用服装与身体的相对描述符以及显式的速度/加速度信息学习运动到潜在空间的映射，从而仅用少量训练数据即可泛化到未见运动与体型，同时保持细节动态。
claims:
- 我们首先学习一个紧凑的服装几何潜在空间，作为合理变形的生成模型。
- 训练时仅使用 300 帧行走数据，网络即可泛化到未见身体形状和运动序列。
- 逐帧预测动态混合权重的结果优于固定混合权重，尤其对于宽松服装。
- 通过显式访问服装和身体的速度与加速度信息，方法能够学习运动依赖的变形。
---

# Motion Guided Deep Dynamic 3D Garments

> [!tip] 核心洞察
> 先通过生成模型压缩合理服装变形的流形，再利用服装与身体的相对描述符以及显式的速度/加速度信息学习运动到潜在空间的映射，从而仅用少量训练数据即可泛化到未见运动与体型，同时保持细节动态。

| 字段 | 内容 |
|------|------|
| 中文题名 | 运动引导的深度动态3D服装 |
| 英文题名 | Motion Guided Deep Dynamic 3D Garments |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://geometry.cs.ucl.ac.uk/projects/2022/MotionDeepGarment/) · [Code](https://github.com/MengZephyr/Motion-Guided-Deep-Dynamic-3D-Garment) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Motion Guided Deep Dynamic 3D Garments |
| Dataset | T-shirt garment – generalization to unseen motion, T-shirt garment – long roll-out stability, Dress garment – visual quality vs. state-of-the-art, Unseen motion sequence – collision reduction via post-processing |

> [!tip] 效果简介
> - T-shirt garment – generalization to unseen motion (catwalk) 上，平均碰撞顶点百分比 (%) 0.19 (walking-trained network) vs N/A。
> - T-shirt garment – long roll-out stability (armspace-90, 1150 frames) 上，L2 error (×10^{-2}) 0.82 vs N/A。
> - Dress garment – visual quality vs. state-of-the-art 上，动态变形质量 Ours vs Santesteban et al. 2022, 2021; PBNS (Bertiche et al. 2021a) (更生动、更少僵硬，对宽松服装的动态裙摆变形更明显)。

## 概要

从有限运动序列中学习服装的动态变形空间极具挑战：身体姿态与服装几何的组合空间巨大，引入速度/加速度后空间进一步膨胀，直接拟合极易过拟合，难以泛化到新运动和新体型。本文提出**运动引导的深度动态3D服装**方法，核心思路是将服装变形解耦为规范空间的局部位移与动态蒙皮权重，先通过正则化自编码器学习一个紧凑的合理变形生成潜在空间，再训练一个动态感知编码器，将历史服装状态（几何、速度、加速度）及与身体的交互映射到该潜在空间。该方法仅需300帧行走序列训练，即可泛化到未见体型和运动序列，并捕捉宽松服装的运动依赖动态细节。测试时引入基于UV空间的残差位移优化，将身体-服装穿透率从7.01%大幅降至0.15%。与现有最佳方法相比，本方法在不依赖特定身体参数化的情况下，对宽松服装产生更生动、更少僵硬的动态变形。

## 核心方法与创新机理

### 问题瓶颈与核心思路

从有限训练序列中学习运动驱动的服装动态变形空间面临根本性困难：身体姿态与服装几何的组合空间本身已极为庞大，而引入速度、加速度等时序信息后，维度进一步膨胀。若直接以深度网络拟合从运动到服装几何的映射，模型极易过拟合于训练运动模式，难以泛化到新运动序列和未见体型。本文的核心洞察是：**先压缩，再映射**——首先学习一个紧凑的生成潜在空间，编码所有“合理”的服装变形；然后学习一个动态感知编码器，将历史服装状态与当前身体交互映射到该潜在空间。这一解耦策略使得网络仅需约300帧行走数据即可泛化到未见运动与体型，同时保持丰富的动态细节（如宽松裙摆的惯性摆动）。

### 变形表示：规范空间局部位移 + 动态蒙皮权重

方法将服装变形分解为两个互补分量，构成第一个关键 changed slot：

**规范空间局部位移**。设规范姿态下的服装网格为 $G_0$，顶点 $g_0^i$ 处定义局部坐标系 $H_0^i$（由法向量和切向量构成）。对于时刻 $t$，网络预测逐顶点的局部位移向量 $d_t^i$，得到带位移的规范顶点：

$$\hat{g}_t^i = g_0^i + H_0^i d_t^i$$

这一设计使位移在局部坐标系中表达，天然具备旋转不变性，避免了对全局姿态的过拟合。

**动态蒙皮权重**。与现有方法采用固定蒙皮权重或将其约束于扩散身体模型不同，本方法逐帧预测动态蒙皮权重 $W_t$，构成第二个关键 changed slot。权重通过基于可学习部件核半径的高斯核计算：

$$w_t^{ij} = \frac{s_t^{ij}}{\sum_{k \in J} s_t^{ik}}, \quad s_t^{ij} = \exp\left(-\frac{\|\hat{g}_t^i - b_0^j\|^2}{2\rho_{l(j)}^2}\right)$$

其中 $b_0^j$ 为身体种子点，$\rho_{l(j)}$ 为按身体部件可学习的核半径。最终顶点位置通过线性混合蒙皮（LBS）获得：

$$g_t^i = \sum_{j \in J} w_t^{ij} \left( R_t^j ( \hat{g}_t^i - b_0^j ) + b_0^j + T_t^j \right)$$

动态蒙皮权重的消融实验（Fig. 7）证实，相比固定权重，逐帧动态权重在宽松服装上产生更合理的变形，尤其改善了腋下区域的伪影。

### 相对描述符编码：与身体参数化解耦

为实现对未见体型的泛化，方法引入第三个关键 changed slot——将服装几何编码为相对于身体表面种子点的局部描述符，而非依赖特定的身体参数化（如SMPL）。具体而言，对每个服装顶点 $g_t^i$，构造相对描述符 $p_t^i := [g_t^i - b_t^j]_{j \in J}$，即顶点到各身体种子点的偏移向量集合。这一设计使网络完全与身体参数化无关，仅需单一体型训练即可泛化到不同身体形状（Fig. 4），而基线方法 Santesteban et al. 则需多体型训练数据。

![[assets/figures/papers/paper_list_l67_https_geometry_cs_ucl_ac_uk_projects_2022_MotionDeepGarment/figures/005_Figure_4.jpg]]
*Figure 4: Generalization to body shape and walking style. We train our network on a walking sequence of 300 frames on a fixed body shape and test on walking motion with different character armspace settings, different styles of walking, and different body shapes*

### 管道模块与训练/推理路径

方法分为两个阶段训练，管道模块按以下顺序组织（Fig. 2, Fig. 3）：

![[assets/figures/papers/paper_list_l67_https_geometry_cs_ucl_ac_uk_projects_2022_MotionDeepGarment/figures/003_Figure_2.jpg]]
*Figure 2: Method overview. We present a motion guided 3D garment prediction network that takes as input the previous state of the garment*

![[assets/figures/papers/paper_list_l67_https_geometry_cs_ucl_ac_uk_projects_2022_MotionDeepGarment/figures/004_Figure_3.jpg]]
*Figure 3: Deep dynamic garment architecture. Our approach first learns a compact generative space of plausible garment deformations. We achieve this by encoding a garment geometry ???? represented as relative to the underlying body ????*

**阶段一：静态自编码器——学习生成潜在空间**

1. **相对描述符编码**：将服装几何 $G_t$ 转换为相对描述符 $P_t$。
2. **静态编码器 $\mathcal{E}^{Sta}$**：将 $P_t$ 编码为潜在码 $Z_t$。
3. **位移与混合权重解码器 $D$**：从 $Z_t$ 解码几何特征图 $M_t^\xi \in \mathbb{R}^{w \times h \times 128}$。
4. **逐顶点预测 MLP $R$**：通过 $d_t^i = R(\xi_t^i, u^i)$ 预测局部位移，其中 $\xi_t^i$ 为特征图上采样得到的逐点特征，$u^i$ 为UV坐标。
5. **重建损失**：$L_{rec} = \|G_t - G_t^*\|_1 + \|\Delta G_t - \Delta G_t^*\|_1$，对顶点位置和拉普拉斯坐标施加L1损失，保持形状细节。

此阶段的自编码器通过正则化训练，学习到的潜在空间构成了“合理服装变形”的生成模型。Fig. 9 展示了在该空间中插值可产生平滑的布料卷曲变形，验证了空间的连续性和合理性。

**阶段二：动态感知编码器——学习运动到潜在空间的映射**

6. **运动特征图 $M_{t-1}^{V,\dot{V}}$**：编码上一帧服装的速度和加速度信息。
7. **交互特征图 $C_t$**：编码服装与身体的相对关系，包括有符号距离 $q_t^{ij} := (g_{t-1}^i - b_t^j) \cdot n_t^{bj}$（检测穿透）和交互力幅值 $\text{ReLU}(-q_t^{ij})$。
8. **动态感知编码器 $\mathcal{E}^{Dyn}$**：将上一帧服装状态 $S(M_{t-1}^{P})$ 与交互特征 $E_t$ 拼接后映射到潜在空间，得到 $Z_t := \mathcal{E}^{Dyn}(S(M_{t-1}^{P}), E_t)$。

关键训练约束：当身体和服装均保持静止（$E_t = 0$）时，强制潜在码与前一帧一致，即 $Z_t = Z_{t-1}$。这一约束通过虚拟训练样本实现，消融实验（Fig. 10）证实其有助于学习更精确的变形动态。

**推理路径**：给定初始服装状态 $G_0$ 和身体运动序列，网络自回归地预测每一帧的潜在码 $Z_t$，解码得到局部位移 $d_t^i$ 和动态蒙皮权重 $w_t^{ij}$，通过LBS计算最终顶点位置。预测结果作为下一帧的历史输入，支持长达千帧的迭代推出（Fig. 6）。

### 测试时碰撞处理

尽管训练中包含碰撞损失，网络预测仍可能残留身体-服装穿透。方法引入第四个 changed slot——测试时优化方案：在UV空间优化一个残差位移图，监督信号为服装顶点到身体的有符号距离。碰撞损失定义为 $L_{collision} = \sum_i \text{ReLU}(-o_t^{ik})$，仅惩罚穿透顶点。实验显示该方案可将穿透顶点百分比从7.01%大幅降至0.15%（Fig. 8），且残差位移通过反馈网络隐式传播到后续帧，避免逐帧独立优化。

### 与基线的关键差异

| 设计维度 | 基线方法 | 本方法 |
|---------|---------|--------|
| 蒙皮权重 | 固定或约束于扩散身体模型 | 逐帧动态预测，基于可学习部件核半径 |
| 变形表示 | 姿态空间位移或PCA降维 | 规范空间局部位移 + LBS |
| 运动编码 | 身体姿态参数或骨架关节 | 显式服装速度/加速度图 + 身体交互特征 |
| 碰撞处理 | 训练时碰撞损失或逐帧顶点推挤 | 测试时UV空间残差位移优化 |
| 体型泛化 | 需多体型训练 | 单体型训练，通过相对编码泛化 |

这些 changed slots 之间的因果关系清晰：相对描述符编码使网络与身体参数化解耦，为泛化奠定基础；生成潜在空间压缩了合理变形流形，防止过拟合；动态蒙皮权重和显式运动/交互特征使网络能够捕捉运动依赖的惯性变形；测试时碰撞优化作为安全网，处理极端姿态下的残留穿透。

## 实验与关键发现

本文的实验评估围绕三个核心能力展开：**泛化能力**（未见运动、未见体型）、**长期推出预测的稳定性**、以及**动态变形质量**。所有网络均在固定体型的行走序列（armspace-75，300帧）上训练，随后在未见运动与体型上测试，这本身就构成了一种极端的泛化压力测试。

### 泛化到未见运动与体型

**Table 2** 报告了不同测试运动下服装顶点穿透身体网格的平均百分比。以行走序列训练的网络，在常规行走（armspace-75）上穿透率仅 0.06%，在未见的手臂间距行走（armspace-90）上为 0.19%，在更具挑战性的猫步（catwalk）上仍保持在 0.19%。相比之下，以舞蹈序列训练的网络在行走测试上穿透率高达 24.94%，揭示了跨运动类型泛化的根本困难：**当测试运动在统计分布上远离训练运动时（如 Figure 5 的 t-SNE 可视化所示），网络的预测质量会显著下降**。这一发现直接界定了方法的有效边界：网络能够泛化到同一运动风格的变体（如不同手臂间距、不同行走风格），但无法在差异极大的运动类型之间进行零样本迁移。

在体型泛化方面，网络仅使用单一固定体型的训练数据，却成功泛化到不同身高、体重的角色上（Figure 4）。这一能力的根源在于**相对描述符编码**：服装几何被表示为相对于身体表面种子点的局部描述符，而非绝对坐标，使网络与具体的身体参数化无关。这构成了相对于基线方法 Santesteban et al. [2022] 的关键优势——后者需要多体型训练数据。

### 长期推出预测的稳定性

网络以自回归方式运行：当前帧的预测结果作为下一帧的输入，形成迭代推出预测。**Table 3** 报告了在 1150 帧长序列上的 L2 误差：行走序列（armspace-75）为 0.82×10⁻²，未见的手臂间距（armspace-90）为 0.82×10⁻²，猫步为 0.64×10⁻²。Figure 6 展示了长达 1000 帧的推出预测结果，服装变形始终保持稳定，未出现漂移或发散。这种稳定性得益于**动态感知编码器的零状态约束**：当身体和服装的相对状态为零时，潜在编码应与前一帧保持一致（Figure 10 验证了该约束的有效性）。

![[assets/figures/papers/paper_list_l67_https_geometry_cs_ucl_ac_uk_projects_2022_MotionDeepGarment/figures/009_Table_3.jpg]]
*Table 3: To evaluate the stability of our network, we report the L2 error when predicting long motion sequences at test time by iterative roll-out prediction for more than a thousand frames*

### 训练数据长度的决定性影响

**Table 4** 的消融实验揭示了训练数据长度对泛化性能的非单调影响。在 armspace-90 长期推出测试上：

- 50 帧训练：短期推出误差 1.09×10⁻²，长期推出误差 1.17×10⁻²——**过拟合**导致泛化能力差。
- 300 帧训练：短期推出误差 0.82×10⁻²，长期推出误差 0.82×10⁻²——**最佳平衡点**。
- 900 帧训练：短期推出误差 1.05×10⁻²，长期推出误差 0.93×10⁻²——网络偏向已见运动，短期推出误差反而增加。

这一结果表明，**更长的训练序列并不总是有益的**：过度暴露于特定运动模式会使潜在空间向该模式收缩，削弱对未见运动的泛化能力。300 帧恰好提供了足够的变形多样性，同时避免了过拟合。

### 动态蒙皮权重的消融验证

Figure 7 对比了固定蒙皮权重与逐帧动态蒙皮权重的效果。对于宽松的 T 恤，动态权重在腋下区域产生了明显更合理的变形，消除了固定权重下的拉伸伪影。动态权重的计算基于**可学习的部件核半径**：每个身体部件拥有独立的核半径参数 ρ_{l(j)}，通过高斯核函数将服装顶点软分配到身体骨骼上。这种设计在鲁棒性和捕捉动态之间取得了良好平衡——过于刚性的分配无法适应宽松服装的滑动，而过于柔性的分配则会导致变形失去物理意义。

### 显式碰撞处理的效果与局限

原始网络预测的服装存在一定的身体穿透。Figure 8 显示，在未见运动序列上，穿透顶点百分比高达 7.01%。通过测试时优化 UV 空间的残差位移图，穿透率大幅降至 0.15%（减少 6.86 个百分点）。该优化仅需在稀疏的关键帧上进行，残差位移会通过网络的反馈机制隐式传播到后续帧。

然而，**该方法在极端情况下仍可能失败**：当两个身体部位相互靠近且服装宽松时（如腋下、大腿内侧），测试时优化可能无法完全消除穿透。这是基于表面距离的碰撞处理方法的固有限制——当身体表面自交时，有符号距离场本身就会产生歧义。

### 与现有方法的定性对比

Figure 12 将本方法与 Santesteban et al. [2022]、Santesteban et al. [2021] 以及 PBNS（Bertiche et al. 2021a）进行了定性比较。在宽松连衣裙的测试场景中，本方法产生了更生动的动态裙摆变形，而基线方法的结果则显得僵硬。这归因于两个关键设计：**显式的速度/加速度信息输入**使网络能够学习运动依赖的变形，以及**逐帧动态蒙皮权重**使宽松服装能够自然地相对于身体滑动。

### 多层服装扩展的初步验证

Figure 11 展示了方法向多层服装的扩展能力。首先训练一个网络预测黄色连衣裙的变形，然后将该连衣裙视为“交互身体”，训练第二个网络学习紫色裙子的变形。这种层级式训练策略利用了方法不依赖特定身体参数化的特性，但当前实现忽略了外层对内层的反馈影响，这是多层服装建模的一个已知局限。

![[assets/figures/papers/paper_list_l67_https_geometry_cs_ucl_ac_uk_projects_2022_MotionDeepGarment/figures/008_Table_2.jpg]]
*Table 2: To quantitatively evaluate the generalization ability, we show the average percentage of garment vertices inter-penetrating the body meshes across different testing motions produced by the two networks trained with walking motion sequence and dancing motion sequence respectively*

![[assets/figures/papers/paper_list_l67_https_geometry_cs_ucl_ac_uk_projects_2022_MotionDeepGarment/figures/006_Figure_5.jpg]]
*Figure 5: We visualize the distribution of the training and testing motion sequences via t-SNE [Maaten and Hinton 2008]. The testing motions of armspace-60 and armspace-90 are close to the training walking motion; hiphop, rumba, and salsa motions are within the distribution of the training dancing motion; and catwalk is away from the distribution of either training walking or training dancing motions*

## 定位与知识库关联

本文 **Motion Guided Deep Dynamic 3D Garments**（Meng et al., SIGGRAPH Asia 2022）在服装动态变形这一研究脉络中，相对于已有工作改变了四个关键 slot，构成了其独特的知识库挂载点。

**Slot 1：蒙皮权重从固定/受限动态变为逐帧可学习动态。** 此前的方法或使用固定蒙皮权重（如 **Santesteban et al., 2022**），或将动态蒙皮权重约束在扩散人体模型上（如 **Santesteban et al., 2021** 和 **PBNS** (Bertiche et al., 2021a)）。本文提出基于服装顶点到身体种子点距离的高斯核来预测逐帧动态权重，且核半径按身体部件可学习。这一改变的本质在于：蒙皮权重的自由度从“身体姿态的函数”升级为“服装-身体相对几何的函数”，使宽松服装的腋下、裙摆等区域的变形不再僵硬。消融实验（Fig. 7）直接验证了动态权重相对于固定权重的定性优势。

**Slot 2：变形表示从姿态空间位移变为规范空间局部位移+线性混合蒙皮。** 传统方法在姿态空间中直接预测顶点位移，或使用 PCA 降维空间。本文将变形分解为规范状态下的局部位移（在顶点局部坐标系中表达）与由动态权重驱动的线性蒙皮。这一分解的因果意义在于：局部位移负责捕捉褶皱等高频细节，蒙皮负责跟随身体的大尺度运动，两者解耦后各自的学习难度降低，且规范空间位移与身体姿态解耦，天然支持跨体型泛化——网络仅用固定体型的 300 帧行走数据训练，即可泛化到未见体型（Fig. 4）。

**Slot 3：运动编码从纯姿态参数变为显式速度/加速度+身体交互特征。** 此前方法通常以身体姿态参数或骨架关节作为输入。本文在动态感知编码器中显式输入上一帧服装的速度、加速度图，以及服装-身体交互特征（包括相对位置和基于有符号距离的穿透力）。这一改变直接回应了宽松服装中常见的运动依赖变形（如裙摆的惯性甩动）——仅靠静态姿态无法区分“手臂正向左挥”与“手臂已停在左侧”，而速度/加速度信息提供了这一区分能力。

**Slot 4：碰撞处理从训练时损失约束变为测试时 UV 空间残差位移优化。** 多数方法在训练时加入碰撞损失，或在推理时逐顶点外推。本文改为在测试时优化一个 UV 空间的残差位移图，监督信号为服装顶点到身体的有符号距离。这一改变的核心优势在于：残差位移会通过网络的反馈回路隐式传播到后续帧，避免逐帧独立处理导致的抖动；Table 2 显示碰撞顶点百分比可从 7.01% 降至 0.15%。

**知识库挂载点与适用边界。** 该方法在知识库中的核心定位是“基于生成潜在空间的运动驱动服装变形预测器”。其前置依赖包括：物理仿真数据生成训练样本、基于身体表面种子点的相对编码（使网络与特定身体参数化解耦）。适用边界明确：网络按服装类型独立训练（T-shirt 和 dress 需分别训练），且跨运动类型的泛化有限——t-SNE 可视化（Fig. 5）表明，当测试运动（如 catwalk）远离训练运动分布时性能下降。此外，当两个身体部位相互靠近且服装宽松时（如大腿内侧），测试时碰撞优化仍可能失败。

**后续启发与开放问题。** 该工作为后续研究留下了几个明确的附着点：（1）隐式三维表示（NeRF/SDF）能否在规范空间和姿态空间中同时强制无碰撞约束，从根本上消除穿透？（2）能否从单目或多视角视频直接学习动态变形，省去物理仿真步骤？（3）多层服装的相互遮挡与交互能否在统一框架内协同建模，而非当前的逐层独立训练？（4）动态编码器的零状态约束（E_t=0 时潜码不变）是否足以应对所有运动模式，是否需要更鲁棒的时间一致性先验？这些问题直接指向了该方法的当前边界，也为知识库的后续扩展提供了明确方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Motion_Guided_Deep_Dynamic_3D_Garments.pdf]]