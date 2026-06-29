---
title: "MIPNet: Neural Normal-to-Anisotropic-Roughness MIP mapping"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/MIPNet_Neural_Normal_to_Anisotropic_Roughness_MIP_mapping.pdf
project_link: null
code_link: null
aliases:
- MIPNet
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_rendering_materials
core_operator: 将简单的各通道独立线性平均（Box滤波器）替换为可学习的级联多层感知器（cascaded MLP）下采样滤波器，该滤波器联合处理法线与粗糙度图块，并通过可微渲染管线以渲染损失端到端训练，从而学会将高频法线信息迁移到粗糙度张量中（含各向异性）。
primary_logic: 采用基于张量的各向异性粗糙度表示（与三线性插值和梯度优化兼容），以级联MLP架构配合可微渲染损失进行训练，使网络能够在生成mipmap各级时自动将法线图中的几何信息转化为粗糙度与各向异性的改变，从而在不同观察距离下保持材质外观，同时作为现有实时渲染引擎的直接替代方案（drop-in replacement），无需引擎修改。
claims:
- 三种BRDF模型（GGX、Beckmann、Ashikhmin-Shirley）上MIPNet在ILIP、L1、MSE三个指标上均显著优于标准线性mipmap基线
- MIPNet能够从各向同性SVBRDF参数中自动生成包含各向异性粗糙度的mip级别，展示了法线到粗糙度的信息迁移能力
- 在Ashikhmin-Shirley、GGX和Beckmann三种模型上，MIPNet的渲染结果比基线更接近groundtruth，高光形状和位置更准确
- 推理阶段对整个4096×4096 SVBRDF生成完整mipmap金字塔仅需不到1秒，比逐材质优化方法（NeuMIP、AutoLoD）快3–4个数量级
---

# MIPNet: Neural Normal-to-Anisotropic-Roughness MIP mapping

> [!tip] 核心洞察
> 采用基于张量的各向异性粗糙度表示（与三线性插值和梯度优化兼容），以级联MLP架构配合可微渲染损失进行训练，使网络能够在生成mipmap各级时自动将法线图中的几何信息转化为粗糙度与各向异性的改变，从而在不同观察距离下保持材质外观，同时作为现有实时渲染引擎的直接替代方案（drop-in replacement），无需引擎修改。

| 字段 | 内容 |
|------|------|
| 中文题名 | MIPNet: 基于神经网络的各向异性粗糙度MIP映射方法 |
| 英文题名 | MIPNet: Neural Normal-to-Anisotropic-Roughness MIP mapping |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://perso.telecom-paristech.fr/boubek/papers/MIPNet/) |
| Topic | #topic/graphics_rendering_materials |
| Method | MIPNet |
| Dataset | GGX BRDF测试集（100个最具挑战性材质）, Beckmann BRDF测试集（100个最具挑战性材质）, Ashikhmin-Shirley BRDF测试集（100个最具挑战性材质） |

> [!tip] 效果简介
> - GGX BRDF测试集（100个最具挑战性材质） 上，ILIP (×10⁻³) / L1 (×10⁻³) / MSE (×10⁻³) ILIP 64.55, L1 14.69, MSE 1.54 vs Standard mipmap: ILIP 67, L1 15.3, MSE 1.93 (ILIP降低2.45, L1降低0.61, MSE降低0.39; 亦优于SSGT (ILIP 65.98, L1 15.04, MSE 1.77))。
> - Beckmann BRDF测试集（100个最具挑战性材质） 上，ILIP (×10⁻³) / L1 (×10⁻³) / MSE (×10⁻³) ILIP 72.07, L1 17.19, MSE 2.12 vs Standard mipmap: ILIP 75.23, L1 18.37, MSE 2.94 (ILIP降低3.16, L1降低1.18, MSE降低0.82; 亦优于LEADR (ILIP 74.2, L1 17.78, MSE 2.69))。
> - Ashikhmin-Shirley BRDF测试集（100个最具挑战性材质） 上，ILIP (×10⁻³) / L1 (×10⁻³) / MSE (×10⁻³) ILIP 76.33, L1 17.52, MSE 2.3 vs Standard mipmap: ILIP 78.64, L1 18.32, MSE 2.78 (ILIP降低2.31, L1降低0.80, MSE降低0.48)。

## 概要

标准MIP映射对SVBRDF各通道独立进行线性平均，但材质属性（尤其是法线与粗糙度）与渲染结果之间存在固有非线性关系——当观察距离增加时，法线图中的微几何细节本应转化为粗糙度的增加并产生各向异性，而简单的逐通道Box滤波无法捕捉这种信息迁移，导致远距离下高光形状错误、各向异性丢失及材质外观退化。

本文提出**MIPNet**，一种基于级联多层感知器（MLP）的可学习下采样滤波器，替代传统的线性平均算子。核心创新在于：将各向异性粗糙度编码为对称2×2张量表示（兼容三线性插值与梯度优化），通过联合处理法线与粗糙度图块的级联MLP架构，配合可微渲染管线以渲染损失端到端训练，使网络在生成mipmap各级时自动将高频法线信息迁移到粗糙度张量中，从而在不同观察距离下保持材质外观。

在GGX、Beckmann和Ashikhmin-Shirley三种BRDF模型上，MIPNet在ILIP、L1、MSE指标上均显著优于标准线性mipmap基线及各自领域的专用方法（SSGT、LEADR）。推理阶段对4096×4096 SVBRDF生成完整mipmap金字塔仅需不到1秒，比NeuMIP和AutoLoD等离线预处理方法快3–4个数量级。该方法可作为现有实时渲染引擎的直接替代方案，无需引擎修改。

## 核心方法与创新机理

### 问题瓶颈：独立通道线性平均的信息丢失

标准MIP映射的核心操作是对SVBRDF的各个通道独立执行4-to-1线性平均（Box滤波器）以生成低分辨率级别。这一逐通道线性平均策略的根本缺陷在于：材质属性（尤其是法线与粗糙度）与最终渲染结果之间存在固有的非线性关系。具体而言，当观察距离增加时，法线图中的高频微几何细节理应转化为粗糙度的增加，并可能产生各向异性——例如，细长的划痕在远距离下应表现为沿划痕方向的各向异性高光。然而，简单的线性平均无法捕捉这种跨通道的信息迁移，导致远距离渲染出现高光形状错误、各向异性丢失以及材质外观退化。

MIPNet的核心洞察是：将这一逐通道独立线性平均替换为**可学习的级联MLP非线性下采样滤波器**，该滤波器联合处理法线与粗糙度图块，并通过可微渲染管线以渲染损失端到端训练，从而学会将高频法线信息迁移到粗糙度张量中（含各向异性）。

### 关键表示变更：从标量粗糙度到张量粗糙度

MIPNet的第一个关键设计变更是粗糙度的表示方式。基线方法使用逐像素标量粗糙度值（或粗糙度+各向异性角度）作为独立通道进行线性滤波，但标量表示无法在滤波过程中自然保持各向异性结构。MIPNet将各向异性粗糙度编码为对称2×2张量：

$$A := R_{\gamma} \begin{pmatrix} \alpha_b & 0 \\ 0 & \alpha_t \end{pmatrix} R_{\gamma}^T := \begin{pmatrix} a & c \\ c & b \end{pmatrix}$$

其中$\alpha_b$和$\alpha_t$分别为沿两个正交方向的线性感知粗糙度，$\gamma$为旋转角度，$R_\gamma$为对应的旋转矩阵。三个通道$(a, b, c)$直接作为网络输入和输出通道，具有以下优势：
- **线性滤波兼容性**：张量表示在线性插值下行为良好，与三线性插值兼容，可直接嵌入现有实时渲染引擎作为替代方案（drop-in replacement）；
- **梯度优化友好**：避免了特征值分解，后者在极端张量值配置下会导致伪影；
- **物理合理性可约束**：通过投影操作确保输出张量满足物理合理的粗糙度约束。

张量平方$A^2$与$A$具有相同的特征向量，其特征值为$A$特征值的平方，这一性质在后续BRDF公式中用于法线分布函数的计算。

**物理合理性约束**：网络输出的$(a, b, c)$通道需满足以下约束以确保表示有效的粗糙度值：

$$\epsilon_{\alpha} \leq a \leq 1, \quad \epsilon_{\alpha} \leq b \leq 1$$

$$c^2 \leq \min(ab - \epsilon_{\alpha}^2, (1-a)(1-b), (a-\epsilon_{\alpha})(b-\epsilon_{\alpha})) =: c_{\max}^2$$

其中$\epsilon_{\alpha}$为粗糙度下界。投影过程先对$a$和$b$进行$[\epsilon_{\alpha}, 1]$范围内的clamp，再将$c$限制在$[-\sqrt{c_{\max}^2}, \sqrt{c_{\max}^2}]$范围内。

### 级联MLP架构：H_A与H_B下采样块

MIPNet的mipmap生成采用级联架构，由两类MLP下采样块组成：

**H_A块（半分辨率下采样）**：处理2×2材质参数图块，由2个隐藏层（各512维）组成，输出半分辨率残差，与线性下采样版本相加得到$LoD_1$。

**H_B块（四分之一分辨率下采样）**：处理三种分辨率的图块——4×4、2×2和1×1，由3个隐藏层（各1024维）组成，输出四分之一分辨率残差，与$LoD_1$的线性下采样版本相加得到$LoD_2$。

级联关系可形式化表示为：

$$\operatorname{LoD}_k(p) := \mathcal{H}\left(\{\operatorname{LoD}_{k-2}(\mathcal{P}_{k-2}(p)), \operatorname{LoD}_{k-1}(\mathcal{P}_{k-1}(p))\}\right)$$

即第$k$级mipmap的每个纹素由前两级对应区域通过平移不变核$\mathcal{H}$计算得到。$\mathcal{H}$由H_A和H_B的级联实现，其中H_A和H_B各重复4次以覆盖完整的mipmap金字塔。消融实验（Fig. 9）证实：仅使用1次H_A/H_B块时网络无法学习各向异性，而4次重复使各向异性在不同LoD级别上得到有效学习。

**残差连接设计**：网络输出与线性下采样版本相加，而非直接预测绝对值。这一设计使网络专注于学习线性平均无法捕捉的非线性修正项，降低了学习难度并提高了训练稳定性。

**辅助通道处理**：albedo、metallic和height通道保持标准线性下采样，不经过MLP处理。这一设计选择反映了当前方法的边界：仅法线与粗糙度通道受益于联合非线性处理。

### 训练机制：可微渲染驱动的端到端学习

MIPNet的训练不需要预计算数据集，而是采用即时计算groundtruth的策略。

**渲染损失函数**：

$$\mathcal{L}_{\text{total}} := \sum_{k \geq 1} \sum_{p \in \operatorname{LoD}_k} \sum_{\omega_i, \omega_o \in \Omega} \mathcal{L}_k(p, \omega_i, \omega_o)$$

总损失为所有mipmap级别（$k \geq 1$）上所有纹素在所有采样光源和视角方向下的每像素L1渲染损失之和。实验表明，L1损失在FLIP指标上比备选损失函数具有更好的收敛性和各级外观保持能力。

**可微渲染管道**：使用GGX、Beckmann或Ashikhmin-Shirley BRDF模型，以Hammersley序列在半球上采样最多32个光源方向，计算渲染结果与groundtruth之间的差异。groundtruth通过对原始高分辨率材质进行超采样渲染获得，无需预先存储。

**各向异性BRDF计算**：以GGX模型为例，使用张量$A$表示的法线分布函数为：

$$D^{GGX} := \frac{\chi^+(\omega_h \cdot n)}{\pi \det(A) \left( \frac{\omega_h^T \cdot B^T \cdot A^2 \cdot B \cdot \omega_h}{\det(A)^2} + (n \cdot \omega_h)^2 \right)^2}$$

其中$B$为将切线空间向量转换到世界空间的基矩阵。遮蔽-阴影函数$G$采用Heitz（2014）的高度相关形式。Beckmann和Ashikhmin-Shirley模型的各向异性扩展见附录。

**训练效率**：在1104个材质（14个类别）上训练，约3小时/epoch（共40个epoch），显存需求低于2GB。推理阶段对4096×4096 SVBRDF生成完整mipmap金字塔仅需不到1秒，比NeuMIP（约90分钟/材质）快约5400倍，比AutoLoD（约25分钟/材质）快约1500倍。

### 核心因果链总结

1. **输入**：基础分辨率的法线图、粗糙度图（各向同性或各向异性）、albedo、metallic、height。
2. **张量编码**：将粗糙度和各向异性角度转换为$(a, b, c)$张量通道。
3. **级联下采样**：H_A块处理2×2图块生成$LoD_1$残差，H_B块处理多分辨率图块生成$LoD_2$残差，各重复4次构建完整金字塔。
4. **张量投影**：确保输出满足物理合理性约束。
5. **可微渲染评估**：在各LoD级别上渲染并与groundtruth比较，反向传播L1损失。
6. **信息迁移学习**：网络通过最小化渲染差异，隐式学习将法线图中的几何信息转化为粗糙度张量中的各向异性成分。

![[assets/figures/papers/paper_list_l63_https_perso_telecom_paristech_fr_boubek_papers_MIPNet/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our training process. Mipmap levels*

![[assets/figures/papers/paper_list_l63_https_perso_telecom_paristech_fr_boubek_papers_MIPNet/figures/003_Figure_3.jpg]]
*Figure 3: Simplified, single resolution training pipeline*

## 实验与关键发现

### 定量评估：三种BRDF模型上的跨基线优势

MIPNet在GGX、Beckmann和Ashikhmin-Shirley三种各向异性BRDF模型上均进行了系统的定量评估。训练集包含来自14个类别的1104个不同材质，测试集选取了100个基线误差最大的最具挑战性材质。评估指标采用ILIP（×10⁻³）、L1（×10⁻³）和MSE（×10⁻³）三个渲染损失度量。

**Table 1** 汇总了各模型上的核心对比结果。在GGX模型上，MIPNet取得ILIP 64.55、L1 14.69、MSE 1.54，相较于标准线性mipmap基线（ILIP 67、L1 15.3、MSE 1.93），ILIP降低2.45、L1降低0.61、MSE降低0.39。与GGX专用竞争对手**SSGT**（Patry, 2020）相比，MIPNet在全部三个指标上均表现更优（SSGT: ILIP 65.98、L1 15.04、MSE 1.77）。在Beckmann模型上，MIPNet取得ILIP 72.07、L1 17.19、MSE 2.12，相对基线（ILIP 75.23、L1 18.37、MSE 2.94）分别降低3.16、1.18和0.82，并优于Beckmann专用方法**LEADR**（Dupuy et al., 2013）的ILIP 74.2、L1 17.78、MSE 2.69。在Ashikhmin-Shirley模型上，MIPNet的ILIP 76.33、L1 17.52、MSE 2.3同样全面超越基线（ILIP 78.64、L1 18.32、MSE 2.78），分别降低2.31、0.80和0.48。

值得注意的是，MIPNet在三个BRDF模型上均以单一架构实现，而SSGT和LEADR分别针对GGX和Beckmann进行了专门设计，这验证了MIPNet跨BRDF模型的泛化能力源自其端到端可微渲染训练策略，而非对特定解析分布的适配。

### 定性评估：高光形状与各向异性保持

**Fig. 4** 展示了Ashikhmin-Shirley模型上四个挑战性材质的渲染对比。每两组渲染行中，第一行展示渲染结果，第二行给出逐像素FLIP误差图和当前使用的mipmap级别伪彩图。标准线性mipmap在远距离观察时高光区域明显缩小且形状失真，而MIPNet能够保持与groundtruth高度一致的高光形状、尺寸和各向异性方向。FLIP误差图显示MIPNet的误差主要集中在高光边缘区域，而基线的误差则遍布整个高光区域。

**Fig. 5** 在GGX模型上对比了MIPNet与基线和SSGT在六个挑战性材质上的表现。对于具有强烈各向异性特征的材质（如拉丝金属），SSGT虽然能够通过SGGX框架保持部分各向异性，但在高光强度和方向准确性上仍不及MIPNet。**Fig. 6** 在Beckmann模型上与LEADR的对比进一步确认了这一趋势：MIPNet生成的高光位置和形状更接近groundtruth，LEADR在某些材质上出现了高光过度扩散或方向偏差的问题。

### 推理效率：与离线预处理方法的数量级差异

**Fig. 7** 将MIPNet与离线材质预处理方法**NeuMIP**（Kuznetsov et al., 2021）和**AutoLoD**（Hasselgren et al., 2021）进行了对比。对于一张4096×4096分辨率的完整SVBRDF材质，MIPNet生成完整mipmap金字塔的推理时间不到1秒，而NeuMIP需要约90分钟（约5400倍差距），AutoLoD需要约25分钟（约1500倍差距）。这一效率优势源于MIPNet的级联MLP架构在推理时仅需前向传播，无需逐材质迭代优化。训练阶段每epoch约需3小时，总计40个epoch，显存占用低于2GB，可在单GPU上完成。

### 关键消融：级联深度对信息迁移的决定性作用

**Fig. 9** 展示了H_A和H_B块重复次数对各级mipmap质量的影响。当仅使用单次H_A/H_B块时，网络无法学习到各向异性的生成，各级mipmap的高光表现为各向同性，与标准线性mipmap相似。将重复次数增加到4次后，网络能够在不同mipmap级别上自动学习到各向异性的产生和演化，高光形状随观察距离的变化与groundtruth保持一致。这一消融验证了级联架构的深度是实现法线到粗糙度信息迁移的关键因素：浅层网络缺乏足够的表达能力来捕捉从微几何法线到粗尺度各向异性粗糙度的复杂映射关系。

**Fig. 8** 提供了信息迁移的直接证据。当输入为各向同性SVBRDF参数（基础级别的法线图和标量粗糙度）时，MIPNet生成的各级mipmap自动包含了逐渐增强的各向异性粗糙度张量。这表明网络学会了从法线图中的方向性几何信息推断出等效的粗尺度各向异性分布，而非简单地平均粗糙度值。

### 损失函数选择

消融实验表明，每像素L1损失函数相比备选损失函数具有更好的收敛性和各级外观保持能力（以FLIP指标衡量）。L1损失对高光区域的大梯度变化具有更好的鲁棒性，避免了MSE损失在镜面反射峰值处过度惩罚导致的过平滑问题。

### 失败模式与适用边界

MIPNet存在以下经实验验证的局限性：

1. **albedo通道解耦的基色偏移问题**（**Fig. 10**左上）：当前架构对albedo通道独立进行线性mipmap，未与法线/粗糙度通道耦合。groundtruth渲染显示，随着观察距离增加，材质基色会出现可感知的偏移（源于微几何遮蔽和多次反射的宏观效应），而MIPNet无法重现这一现象。

2. **单波瓣表达力不足**（**Fig. 10**左下）：对于具有复杂微结构的材质（如高度镜面或十字形图案），单个各向异性波瓣无法准确描述粗尺度下出现的复杂辐射分布。**Fig. 5** 中的示例III和IV也展示了这一局限性，这些材质可能需要多个波瓣的线性组合才能完整表达。

![[assets/figures/papers/paper_list_l63_https_perso_telecom_paristech_fr_boubek_papers_MIPNet/figures/006_Figure_5.jpg]]
*Figure 5: Renderings of materials using the GGX model under varying view conditions. We compare our method to the standard linear mipmapping (baseline) and main competitor specialized in GGX material mipmapping (SSGT) on six challenging materials (more in additional material). Every second row shows the pixel-wise FLIP deviation to the groundtruth, as well as a false color image depicting the mipmap LoD used for rendering (with trilinear filtering)*

3. **GGX模型上的极端镜面材质失败**（**Fig. 10**右列）：当粗糙度极小（α < 1×10⁻²）时，groundtruth渲染中产生fireflies（高亮噪点），导致梯度不稳定。在此类材质上，MIPNet表现不及SSGT。这一失败的因果链条是：极低粗糙度→渲染积分方差极大→梯度估计噪声→网络收敛到次优解。

4. **BRDF模型覆盖范围**：当前仅支持GGX、Beckmann和Ashikhmin-Shirley三种各向异性BRDF模型，尚未扩展到sheen、layered或iridescent等更复杂的材质模型。

5. **计算足迹固定**：当前架构的计算足迹固定为4×4 texel（2分辨率架构），对于极端复杂的材质可能需要更大的texel计算足迹才能精确合成各级mipmap。将足迹扩大到8×8（3分辨率）或16×16（4分辨率）是否能进一步提高精度，仍是一个开放问题。

![[assets/figures/papers/paper_list_l63_https_perso_telecom_paristech_fr_boubek_papers_MIPNet/figures/004_Figure_4.jpg]]
*Figure 4: Renderings of materials using the Ashikhmin-Shirley model under varying view conditions. We compare our method to the standard linear mipmapping (baseline) on four challenging materials (more in additional material). Every second row shows the pixel-wise FLIP deviation to the groundtruth, as well as a false color image depicting the mipmap LoD used for rendering (with trilinear filtering)*

![[assets/figures/papers/paper_list_l63_https_perso_telecom_paristech_fr_boubek_papers_MIPNet/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons between the baseline, our method and the competition on each BRDF variant. The train set is composed of 1104 different materials from 14 categories. The test set is composed of 100 materials, identified as the most difficult (given by baseline error). The best result for each comparison is highlighted in bold*

![[assets/figures/papers/paper_list_l63_https_perso_telecom_paristech_fr_boubek_papers_MIPNet/figures/007_Figure_6.jpg]]
*Figure 6: Renderings of materials using the Beckmann model under varying view conditions. We compare our method to the standard linear mipmapping (baseline) and main competitor specialized in Beckmann distributions mipmapping (LEADR) on six challenging materials (more in additional material). Every second row shows the pixel-wise FLIP deviation to the groundtruth, as well as a false color image depicting the mipmap LoD used for rendering (with trilinear filtering)*

## 定位与知识库关联

MIPNet 的核心贡献在于改变了材质 mipmap 生成管线中**下采样算子**这一关键 slot：将传统的逐通道独立线性平均（Box 滤波器，Williams 1983）替换为可学习的级联 MLP 非线性下采样滤波器，同时将**粗糙度表示**从标量/各向异性角度扩展为对称 2×2 张量表示。这一双重替换使得网络能够在生成 mipmap 各级时自动将法线图中的高频几何信息迁移为粗糙度的增加与各向异性的产生，从而解决了标准 mipmap 中法线细节随距离丢失、高光形状错误的根本瓶颈。

**相对已有工作的本质差异：**

与 **SSGT**（Patry, 2020，应用于《对马岛之鬼》）相比，SSGT 基于 SGGX 框架对 GGX 分布进行线性滤波，但其滤波操作仍限定在线性域内，且专门针对 GGX 模型设计。MIPNet 通过可微渲染损失端到端学习非线性下采样核，不仅覆盖 GGX，还统一支持 Beckmann 和 Ashikhmin-Shirley 三种 BRDF，在 GGX 测试集上 ILIP 指标（64.55 vs SSGT 的 65.98）和 L1/MSE 均取得更优结果（Table 1）。

与 **LEADR**（Dupuy et al., 2013）相比，LEADR 在 Beckmann 分布上通过方差图辅助法线滤波来保持高光外观，但其方法依赖手工设计的滤波规则，且仅针对 Beckmann 模型。MIPNet 在 Beckmann 测试集上 ILIP 为 72.07，显著优于 LEADR 的 74.20（Table 1），同时避免了 LEADR 在极端张量值下因特征值分解产生的伪影——MIPNet 的张量投影策略直接约束通道值范围而不进行分解。

与离线材质预处理方法 **NeuMIP**（Kuznetsov et al., 2021）和 **AutoLoD**（Hasselgren et al., 2021）相比，这两类方法需要针对每个材质进行数十分钟到数小时的逐材质优化（NeuMIP 约 90 分钟，AutoLoD 约 25 分钟），而 MIPNet 在推理阶段对 4096×4096 SVBRDF 生成完整 mipmap 金字塔仅需不到 1 秒，速度提升约 3–4 个数量级（Fig. 7）。这一差异源于 MIPNet 学习的是通用的平移不变下采样核，而非为每个材质构建独立的神经表示。

**知识库挂载点：**

MIPNet 在知识图谱中的挂载位置是“实时渲染 > 材质过滤与 mipmap > 神经下采样算子”。其上游依赖包括：基于物理的 BRDF 模型（GGX/Beckmann/Ashikhmin-Shirley 的 microfacet 理论框架）、各向异性粗糙度的张量表示（借鉴了 SGGX 的张量编码思路但避免了特征值分解）、以及可微渲染技术（用于端到端训练）。其下游可连接至：实时渲染引擎中的材质系统（作为 drop-in replacement 无需引擎修改）、多分辨率材质编辑工具、以及更广泛的神经纹理合成方法。

**适用边界：**

MIPNet 的适用性受以下边界条件约束：（1）仅支持 GGX、Beckmann 和 Ashikhmin-Shirley 三种各向异性 BRDF 模型，尚未扩展到 sheen、layered 或 iridescent 等更复杂的材质模型；（2）albedo 和 metallic 通道仍保持独立线性下采样，未与法线/粗糙度通道联合优化，导致无法捕捉基色随距离的偏移现象（Fig. 10 左上）；（3）对于粗糙度极小（< 1e-2）的高度镜面 GGX 材质，groundtruth 渲染中产生的 fireflies 导致梯度不稳定，MIPNet 表现不及专门设计的 SSGT（Fig. 10 右列）；（4）单个各向异性波瓣的表达力对于具有复杂微结构（如十字形图案）的挑战性材质不足（Fig. 10 左下）；（5）计算足迹固定为 2 分辨率架构（4×4 texel 窗口），对于极端复杂的材质可能需要更大的 texel 计算足迹。

**后续启发：**

MIPNet 揭示了一个具有推广价值的设计范式：通过可微渲染损失训练级联 MLP 下采样核，可以实现材质通道间的信息迁移（法线→粗糙度→各向异性），这为其他需要跨通道耦合的材质处理任务提供了方法论参考。后续工作可沿以下方向展开：将 albedo/metallic 通道纳入联合优化框架以捕捉基色偏移；设计多波瓣架构以处理复杂微结构材质；扩展 texel 计算足迹至 8×8 或 16×16 以提升精度；探索先训练重型网络再简化的策略以在保持质量的同时提高推理效率；以及将该方法推广至 layered、sheen 等更广泛的材质模型。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/MIPNet_Neural_Normal_to_Anisotropic_Roughness_MIP_mapping.pdf]]