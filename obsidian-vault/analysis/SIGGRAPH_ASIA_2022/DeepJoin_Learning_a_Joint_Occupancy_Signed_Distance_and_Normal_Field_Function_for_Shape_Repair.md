---
title: "DeepJoin: Learning a Joint Occupancy, Signed Distance, and Normal Field Function for Shape Repair"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/DeepJoin_Learning_a_Joint_Occupancy_Signed_Distance_and_Normal_Field_Function_for_Shape_Repair.pdf
project_link: null
code_link: null
aliases:
- DeepJoin
tags:
- SIGGRAPH_ASIA_2022
- topic/other_unclear
core_operator: 联合占用、符号距离和法向场表示，并通过CSG形式化断裂形状与完整形状、断裂面的关系，使网络将断裂形状分解为两个部分补全任务，从而避免伪影并提升修复精度。
primary_logic: 通过联合预测占用、SDF和法向场，并利用占用值作为选择性组合器，网络可以准确分离完整形状和断裂面，进而直接生成无伪影、紧密贴合的修复形状，而非简单地用完整形状减去断裂形状。
claims:
- DeepJoin with Occ+SDF+NF achieves lowest CD (0.062) and NE% 98.8%, outperforming other feature combinations.
- DeepJoin significantly outperforms baselines (DeepSDF, ONet, ESSC) on mean CD (0.062 vs. 0.072/0.141/0.115) and especially NFRE (0.038 vs. 0.181/0.634/0.152), showing minimal surf...
- Using the joint representation (Occ+SDF) enables more stable training and higher NE% (98.9%) compared to SDF alone (failed) or SDF+NF (96.1%).
- Our approach generates restoration shapes that join closely without artifacts, as shown in visual comparisons.
---

# DeepJoin: Learning a Joint Occupancy, Signed Distance, and Normal Field Function for Shape Repair

> [!tip] 核心洞察
> 通过联合预测占用、SDF和法向场，并利用占用值作为选择性组合器，网络可以准确分离完整形状和断裂面，进而直接生成无伪影、紧密贴合的修复形状，而非简单地用完整形状减去断裂形状。

| 字段 | 内容 |
|------|------|
| 中文题名 | DeepJoin: 学习联合占用、符号距离和法向场函数用于形状修复 |
| 英文题名 | DeepJoin: Learning a Joint Occupancy, Signed Distance, and Normal Field Function for Shape Repair |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://nikwl.github.io/publication/2022-deepjoin/) |
| Topic | #topic/other_unclear |
| Method | DeepJoin |
| Dataset | ShapeNet, Google Scanned Objects, QP Cultural Heritage |

> [!tip] 效果简介
> - ShapeNet (synthetic fractures) 上，Chamfer Distance (CD) mean 0.062 vs DeepSDF 0.072, ONet 0.141, ESSC 0.115 (-14% / -56% / -46%)；Normal Consistency (NC) mean 0.631 vs DeepSDF 0.583, ONet 0.423, ESSC 0.289 (+8% / +49% / +118%)；Non-Fracture Region Error (NFRE) mean 0.038 vs DeepSDF 0.181, ONet 0.634, ESSC 0.152 (-79% / -94% / -75%)。
> - Google Scanned Objects 上，CD 0.117 vs N/A (N/A)。
> - QP Cultural Heritage 上，CD 0.144 vs N/A (N/A)。

## 概要

现有形状修复方法依赖对称性先验或完整形状代理，且基于低分辨率体素或减法操作生成修复件，容易在修复区域与非断裂区域产生表面伪影。根本瓶颈在于，单独使用符号距离函数（SDF）表示断裂形状时，无法准确将完整形状与断裂面分解，导致修复精度不足。**DeepJoin** 提出一种联合占用（Occupancy）、符号距离（SDF）和法向场（Normal Field）的隐式形状表示，并通过构造实体几何（CSG）形式化断裂形状、完整形状与断裂面之间的关系，将断裂形状分解为两个互补的补全任务。核心创新在于利用占用值作为选择性组合器，使网络能够准确分离完整形状与断裂面，从而直接生成无伪影、紧密贴合的修复形状，而非简单地从完整形状中减去断裂形状。在 ShapeNet 合成断裂数据集上，DeepJoin 的平均 Chamfer Distance 达到 0.062，相较于 DeepSDF（0.072）、ONet（0.141）和 ESSC（0.115）分别降低 14%、56% 和 46%；非断裂区域误差（NFRE）仅为 0.038，显著优于各基线方法（0.181/0.634/0.152），表明修复件表面伪影极少。该方法在 Google Scanned Objects 和文化遗产类真实扫描数据上也展现出良好泛化能力。定位上，DeepJoin 属于基于学习的形状修复方法，区别于传统对称性修复和减法式补全，其联合表示与 CSG 分解机制为高保真形状修复提供了新的技术路径。

## 核心方法与创新机理

### 问题形式化：断裂形状的CSG分解

DeepJoin的核心洞察在于将断裂形状的修复问题转化为**构造性实体几何（CSG）**的分解问题。如图3所示，给定一个断裂形状 $F$，其可被分解为完整形状 $C$ 与断裂面 $B$ 的交集：

$$F = C \cap B$$

相应地，修复形状 $R$ 定义为完整形状 $C$ 与断裂面补集 $B'$ 的交集：

$$R = C \cap B'$$

这一形式化的关键意义在于：**修复形状不再通过“完整形状减去断裂形状”的减法操作获得**，而是通过网络直接预测完整形状和断裂面两个独立组件，再通过CSG组合得到修复形状。这从根本上避免了减法操作引入的表面伪影问题——减法操作要求完整代理形状与断裂形状精确对齐，任何微小偏差都会在修复件表面产生台阶状或锯齿状伪影。

### 核心创新：联合占用-SDF-法向场表示

**这是论文最关键的changed slot。** 现有方法（DeepSDF、ONet）仅使用单一隐式表示（SDF或占用），而DeepJoin提出一种**联合预测占用（Occupancy）、符号距离函数（SDF）和法向场（Normal Field, NF）**的表示方法。这三个特征的协同机制如下：

- **占用值**作为选择性组合器：占用值 $o(\mathbf{x}) \in \{0, 1\}$ 明确指示点 $\mathbf{x}$ 在形状内部还是外部，为SDF和NF的选择提供硬性决策边界。
- **SDF**提供精确的表面距离信息，确保修复形状的几何精度。
- **NF**提供表面法向信息，增强修复形状的表面光滑度和细节保真度。

单独使用SDF表示断裂形状时，网络无法稳定学习断裂面的表示——因为SDF在断裂面附近存在符号歧义（断裂面两侧的SDF值符号取决于该点属于完整形状还是断裂面），导致训练失败。占用值的引入解决了这一歧义：通过占用值的乘积运算（见下文），网络可以明确区分完整形状和断裂面的空间归属。

### 网络架构与模块顺序

DeepJoin采用**自解码器（autodecoder）架构**，包含两个核心网络模块（图5）：

**模块1：完整形状网络 $f^C$**
- 输入：查询点 $\mathbf{x} \in \mathbb{R}^3$ 和完整形状潜在编码 $\mathbf{z}_C \in \mathbb{R}^{128}$
- 输出：完整形状的占用 $f_o^C(\mathbf{z}_C, \mathbf{x})$、SDF $f_s^C(\mathbf{z}_C, \mathbf{x})$、NF $\mathbf{f}_{\mathbf{n}}^C(\mathbf{z}_C, \mathbf{x})$
- 角色：预测断裂发生前的原始完整形状

**模块2：断裂面网络 $f^B$**
- 输入：查询点 $\mathbf{x}$ 和断裂面潜在编码 $\mathbf{z}_B \in \mathbb{R}^{64}$
- 输出：断裂面的占用 $f_o^B(\mathbf{z}_B, \mathbf{x})$、SDF $f_s^B(\mathbf{z}_B, \mathbf{x})$、NF $\mathbf{f}_{\mathbf{n}}^B(\mathbf{z}_B, \mathbf{x})$
- 角色：预测分割完整形状的断裂面（薄板样条表示的曲面）

**模块3：CSG组合计算（非参数化）**
从 $f^C$ 和 $f^B$ 的输出，通过以下公式计算断裂形状 $F$ 和修复形状 $R$ 的占用、SDF和NF：

断裂形状占用（公式1）：
$$o_F(\mathbf{x}) = o_C(\mathbf{x}) \, o_B(\mathbf{x})$$

修复形状占用（公式2）：
$$o_R(\mathbf{x}) = o_C(\mathbf{x}) (1 - o_B(\mathbf{x}))$$

断裂形状SDF（公式3）：
$$s_F(\mathbf{x}) = \begin{cases} s_B(\mathbf{x}), & \text{if } o_B(\mathbf{x}) = 0 \text{ or } s_B(\mathbf{x}) > s_C(\mathbf{x}) \\ s_C(\mathbf{x}), & \text{otherwise} \end{cases}$$

修复形状SDF（公式4）：
$$s_R(\mathbf{x}) = \begin{cases} -s_B(\mathbf{x}), & \text{if } o_B(\mathbf{x}) = 1 \text{ or } -s_B(\mathbf{x}) > s_C(\mathbf{x}) \\ s_C(\mathbf{x}), & \text{otherwise} \end{cases}$$

**因果链路**：占用乘积 $o_C \cdot o_B$ 确保断裂形状仅在完整形状和断裂面同时占用的区域存在；而修复形状占用 $o_C \cdot (1-o_B)$ 则确保修复件填充断裂面的补集区域。SDF的选择逻辑（公式3-4）进一步保证了断裂面和修复件表面的几何连续性——在断裂面附近，断裂形状的SDF取断裂面的SDF值，而修复形状的SDF取断裂面SDF的相反数，从而确保修复件与断裂形状在断裂面处紧密贴合。

### 训练路径与损失函数

训练采用**配对潜在编码优化**策略。对于每个训练样本（包含完整形状 $C$ 和断裂面 $B$），优化其对应的潜在编码 $\mathbf{z}_C$ 和 $\mathbf{z}_B$，以及网络参数。总训练损失（公式7）：

$$\mathcal{L}_{\mathrm{train}} = \sum_{\mathbf{z}_C \in \mathcal{Z}_C, \mathbf{z}_B \in \mathcal{Z}_B} \left( \mathcal{L}_{CB} + \mathcal{L}_F + \mathcal{L}_R \right) + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}$$

其中各项损失的作用：

- **$\mathcal{L}_{CB}$**（公式8）：完整形状和断裂面的直接监督损失，包含占用交叉熵、SDF的L1损失和NF的L2损失。确保 $f^C$ 和 $f^B$ 分别准确预测其对应形状。
- **$\mathcal{L}_F$**（公式9）：断裂形状重建损失，使用CSG公式（1, 3, 5）从 $f^C$ 和 $f^B$ 的预测值计算断裂形状的真值，并与网络预测值比较。**关键机制**：占用项使用乘积 $f_o^C \cdot f_o^B$ 作为预测值，强制网络学习占用值的空间一致性。
- **$\mathcal{L}_R$**（公式10）：修复形状重建损失，使用CSG公式（2, 4, 6）计算修复形状真值。**因果作用**：通过反向传播，将修复精度的梯度同时传递给 $f^C$ 和 $f^B$，使两个网络协同优化以生成紧密贴合的修复件。
- **$\mathcal{L}_{\mathrm{reg}}$**：潜在编码的L2正则化，防止过拟合。

**训练路径的因果流**：$f^C$ 和 $f^B$ 的输出 → CSG组合 → 断裂/修复形状预测 → 与真值比较 → 联合梯度更新两个网络。这一设计使得网络不仅学习各自的形状表示，还学习二者之间的空间交互关系。

### 推理路径：潜在编码优化

对于一个新的断裂形状 $F$（无完整形状真值），DeepJoin通过**冻结网络参数、优化潜在编码**的方式进行推理。推理损失（公式16）：

$$\mathcal{L}_{\mathrm{inf}} = \mathcal{L}_F + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}$$

仅包含断裂形状损失 $\mathcal{L}_F$（公式9）和正则化项。优化变量为 $\mathbf{z}_C$ 和 $\mathbf{z}_B$，通过最小化预测断裂形状与输入断裂形状的差异，估计出最可能的完整形状和断裂面编码。然后使用公式（4, 6）计算修复形状的SDF，并通过Marching Cubes提取等值面生成修复网格。

**推理路径的因果约束**：推理仅监督断裂形状，但通过CSG公式的耦合，$\mathbf{z}_C$ 和 $\mathbf{z}_B$ 的优化必须同时满足断裂形状的占用、SDF和NF约束，从而隐式地推断出合理的完整形状和修复件。这一设计的优势在于：**无需完整形状的真值即可进行修复**，适用于真实断裂场景。

### 第二个Changed Slot：修复形状的直接生成

传统方法（如ESSC）的修复流程为：补全断裂形状 → 得到完整代理形状 → 减去断裂形状 → 获得修复件。DeepJoin的**changed slot**在于跳过“减法”步骤，直接通过CSG分解生成修复形状的SDF。这一改变的因果效益体现在：

1. **避免减法伪影**：减法操作对完整代理形状的精度极其敏感，任何微小偏差都会在修复件边缘产生锯齿或台阶状伪影。DeepJoin的修复形状SDF直接由 $f^C$ 和 $f^B$ 的预测值组合生成，表面光滑度由NF损失保证。
2. **断裂面贴合精度**：修复形状SDF在断裂面附近取 $-s_B$，确保修复件表面与断裂面精确贴合，而非依赖完整代理形状的边界精度。

### 关键公式的变量含义与因果链

以修复形状SDF损失 $\mathcal{L}_{R_s}$（公式13）为例说明因果链：

$$\mathcal{L}_{R_s} = \begin{cases} || -f_s^B(\mathbf{z}_B, \mathbf{x}) - s_R(\mathbf{x}) ||_1 & \text{if } f_o^B(\mathbf{z}_B, \mathbf{x}) > \mu \text{ or } -f_s^B(\mathbf{z}_B, \mathbf{x}) > f_s^C(\mathbf{z}_C, \mathbf{x}) \\ || f_s^C(\mathbf{z}_C, \mathbf{x}) - s_R(\mathbf{x}) ||_1 & \text{otherwise} \end{cases}$$

- $f_o^B > \mu$：断裂面内部区域（$\mu$ 为占用阈值），修复形状在此区域取断裂面SDF的相反数
- $-f_s^B > f_s^C$：断裂面附近但完整形状SDF更小的区域，同样取相反数以确保贴合
- 其他区域：取完整形状的SDF，保证修复件的整体几何

这一条件选择机制实现了**空间自适应的SDF组合**，在断裂面附近强制贴合，在远离断裂面处保持完整形状的几何特征。

## 实验与关键发现

### 核心定量结果

DeepJoin 在 ShapeNet 合成断裂数据集上全面超越三种基线方法。Table 2 报告了类别均值：DeepJoin 的 Chamfer Distance (CD) 为 **0.062**，相比 DeepSDF 的 0.072 降低 **14%**，相比 ONet 的 0.141 降低 **56%**，相比 ESSC 的 0.115 降低 **46%**。Normal Consistency (NC) 达到 **0.631**，分别超出 DeepSDF (0.583)、ONet (0.423) 和 ESSC (0.289) 约 **8%、49% 和 118%**，表明修复形状的表面法向与真实形状高度一致。

![[assets/figures/papers/paper_list_l42_https_nikwl_github_io_publication_2022_deepjoin/figures/010_Table_2.jpg]]
*Table 2: Chamfer distance (CD), normal consistency (NC) and non-fracture region error (NFRE) for baseline approaches and our approach. Best metric values are bolded. Mean is computed over class means*

更具诊断价值的是 Non-Fracture Region Error (NFRE) 指标——该指标专门衡量非断裂区域的表面伪影程度。DeepJoin 的 NFRE 仅为 **0.038**，而 DeepSDF 为 0.181（高出约 **4.8 倍**），ONet 为 0.634（高出约 **16.7 倍**），ESSC 为 0.152（高出约 **4 倍**）。这一巨大差距揭示了基线方法的根本问题：基于减法操作的修复方式会在非断裂区域产生大量表面伪影，即便经过连通组件过滤（移除体积 < 0.01 的组件）也无法完全消除。DeepJoin 通过 CSG 分解直接生成修复形状的 SDF，从机制上避免了减法带来的伪影。

### 消融实验：联合表示的关键作用

Table 1 的消融实验系统验证了占用 (Occ)、SDF 和法向场 (NF) 三个特征对修复性能的因果贡献：

![[assets/figures/papers/paper_list_l42_https_nikwl_github_io_publication_2022_deepjoin/figures/007_Table_1.jpg]]
*Table 1: Chamfer (CD) and percentage of non-empty restorations (NE%), using DeepJoin with different features. Best values are bolded*

- **仅使用 Occ**：网络能够收敛并生成修复形状（NE% = 89.4%），CD 为 0.099。这表明占用值本身可以驱动形状分解，但缺乏精确的几何约束导致修复精度不足。
- **Occ + SDF**：引入 SDF 后，NE% 跃升至 **98.9%**，CD 降至 0.074。SDF 提供了连续的距离场信息，使网络能够稳定学习断裂面的几何结构，显著提升了修复形状的生成成功率。值得注意的是，仅使用 SDF（无 Occ）的变体完全无法稳定学习断裂面表示，**不生成任何修复形状**——这证实了 Occ 作为选择性组合器的关键作用：占用值通过乘积公式 $o_F(\mathbf{x}) = o_C(\mathbf{x}) o_B(\mathbf{x})$ 和 $o_R(\mathbf{x}) = o_C(\mathbf{x}) (1 - o_B(\mathbf{x}))$ 为 SDF 的选择提供了可靠的区域划分依据。
- **Occ + SDF + NF（完整 DeepJoin）**：进一步加入法向场后，CD 降至最优的 **0.062**，NE% 保持 98.8%。NF 提供了更高阶的表面几何信息，使修复形状的边缘更加锐利、贴合更紧密，这一改进在视觉对比 (Fig. 6, Fig. 8) 中表现为修复件与断裂面的平滑过渡。

![[assets/figures/papers/paper_list_l42_https_nikwl_github_io_publication_2022_deepjoin/figures/006_Figure_6.jpg]]
*Figure 6: Predicted restoration shapes (red), joined to input fractured shapes (gray) and opened to show the fracture*

![[assets/figures/papers/paper_list_l42_https_nikwl_github_io_publication_2022_deepjoin/figures/011_Figure_8.jpg]]
*Figure 8: From left to right: input fractured shapes (gray) and restorations (red) from DeepSDF, ONet, ESSC, DeepJoin, and ground truth*

### 跨域泛化能力

DeepJoin 在未经微调的情况下，直接在三个分布外数据集上展示了泛化能力：

- **Google Scanned Objects**（日常物品 3D 扫描）：CD = 0.117
- **QP Cultural Heritage**（古希腊风格陶器）：CD = 0.144
- **真实断裂物体**：成功生成修复形状并进行了 3D 打印验证 (Fig. 7c)

这表明联合表示学习到的形状先验具有较强的跨域迁移能力，不局限于 ShapeNet 的合成数据分布。

### 失败模式与适用边界

尽管整体性能优异，DeepJoin 存在以下明确边界条件：

1. **修复形状缺失（1.2% 案例）**：当断裂面预测位置偏离实际断裂区域时，网络无法生成修复形状。论文指出此时可回退到完整的形状预测，使用减法方式作为兜底方案。
2. **凹形断裂处理受限**：由于断裂面采用薄板样条（thin-plate spline）表示，该方法无法准确表示凹形断裂面。这是表示能力的固有限制，而非训练问题。
3. **修复件尺寸或位置偏差**：当断裂区域较小时，可能预测出比真实修复件更小或位置错误的修复形状 (Fig. 9 right)。
4. **单组件断裂限定**：当前方法仅处理单组件断裂，不适用于多部件断裂装配场景——后者需要同时估计部件间的相对变换。

![[assets/figures/papers/paper_list_l42_https_nikwl_github_io_publication_2022_deepjoin/figures/009_Figure_9.jpg]]
*Figure 9: Left: The complete and break shape may not intersect. Right: Restorations may be small predicted in the wrong location*

### 实验公平性说明

所有基线方法共享相同的预处理管线：使用 PointNet++ 分类器（测试准确率 97.1%）自动识别并移除断裂区域的面片，确保输入一致性。ESSC 受限于 $32^3$ 体素分辨率以匹配其原始设定，Marching Cubes 转换可能引入精度损失——这在一定程度上解释了其较低的 NC (0.289) 和较高的 NFRE (0.152)。基线方法的连通组件过滤虽缓解了表面伪影，但无法根除，这从侧面验证了 DeepJoin 从表示层面解决伪影问题的有效性。

## 定位与知识库关联

DeepJoin 在形状修复（shape repair）任务中改变了两个关键槽位，使其与现有方法形成本质差异。

**槽位一：形状表示**。现有基线方法采用单一隐式函数表示——**DeepSDF**（Park et al., 2019）仅使用SDF，**ONet**（Mescheder et al., 2019）仅使用占用网络，而DeepJoin提出联合预测占用（Occupancy）、符号距离（SDF）和法向场（NF）三种特征。这一改变的因果机制在于：单独的SDF表示无法稳定学习断裂面（消融实验证实仅SDF的变体完全无法生成修复形状），而联合表示中占用值充当了选择性组合器——它决定了在断裂面附近哪些区域采用断裂面的SDF/NF，哪些区域采用完整形状的值。消融实验（Table 1）给出了清晰的证据链：Occ单独使用收敛率低（NE%仅89.4%），加入SDF后（Occ+SDF）将NE%提升至98.9%，再加入NF（Occ+SDF+NF）在保持高NE%（98.8%）的同时将CD从0.074进一步降至0.062，表明NF提升了修复形状的表面保真度。

**槽位二：修复形状生成方式**。现有方法（如**ESSC**，Zhang et al., 2018）采用减法逻辑——先从断裂形状补全出完整形状，再减去断裂形状得到修复件。这种"补全再减去"的范式容易在断裂边界产生表面伪影。DeepJoin通过CSG（构造实体几何）形式化，将断裂形状显式分解为完整形状C与断裂面B的交集（$F = C \cap B$），修复形状则为C与B补集的交集（$R = C \cap B'$）。网络同时预测C和B的三种场值，然后通过CSG公式直接计算出修复形状的SDF并提取等值面，避免了减法操作引入的边界伪影。这一改变在NFRE指标上体现得尤为显著：DeepJoin的NFRE为0.038，而DeepSDF为0.181（降低79%），ONet为0.634（降低94%），ESSC为0.152（降低75%），直接验证了方法在非断裂区域几乎不产生表面伪影的优势。

**知识库挂载点**：本工作应挂载到两个知识节点下。（1）**隐式神经表示（Implicit Neural Representations）**：作为DeepSDF和ONet的后续发展，DeepJoin证明了将多种互补的隐式场（Occ/SDF/NF）联合建模并通过CSG逻辑组合，可以处理比单一形状补全更复杂的"形状分解与选择性修复"问题。其自解码器（autodecoder）架构和编码优化推理流程直接继承自DeepSDF，但在输出头设计上从单一场扩展为三场联合预测。（2）**三维形状分析与修复（3D Shape Analysis and Repair）**：相对于依赖对称性检测或完整代理的修复方法，DeepJoin首次将断裂形状修复形式化为"完整形状-断裂面"的双路分解问题，为后续的多部件断裂装配、凹形断裂处理等方向提供了新的问题建模框架。

**适用边界**：（1）方法假设断裂是单组件的，无法处理多部件断裂装配场景——这是相对多部件装配方法（如基于相对变换估计的方法）的明确边界。（2）断裂面采用薄板样条（thin-plate spline）表示，无法准确表示凹形断裂，这限制了方法在复杂断裂几何上的适用性。（3）在约1.2%的案例中方法无法生成修复形状（NE%未达100%），主要发生在断裂面预测位置偏离实际断裂区域时——此时系统可回退到仅用完整形状的减法修复作为fallback。（4）当断裂区域较小时，可能预测出比真实修复件更小或位置错误的修复形状（Fig. 9）。

**后续启发**：（1）将断裂面表示从薄板样条升级为更通用的形式（如NURBS），可处理凹形断裂，扩展方法的几何适用范围。（2）同时估计多部件间的相对变换，可将当前单组件修复扩展为多断裂装配与修复。（3）在断裂面附近引入局部变形优化，可实现3D打印修复件与原始断裂面的精密水密连接，直接服务于数字制造流程。（4）构建包含真实物理断裂物体3D扫描的大规模数据集，可推动方法从合成断裂向真实断裂场景的迁移——当前在Google Scanned Objects（CD 0.117）和QP Cultural Heritage（CD 0.144）上的初步结果已显示出泛化潜力，但性能仍低于合成数据（CD 0.062）。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/DeepJoin_Learning_a_Joint_Occupancy_Signed_Distance_and_Normal_Field_Function_for_Shape_Repair.pdf]]