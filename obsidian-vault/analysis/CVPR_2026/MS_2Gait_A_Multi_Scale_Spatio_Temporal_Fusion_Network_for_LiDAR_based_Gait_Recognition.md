---
title: "MS^2Gait: A Multi-Scale Spatio-Temporal Fusion Network for LiDAR-based Gait Recognition"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MS_2Gait_A_Multi_Scale_Spatio_Temporal_Fusion_Network_for_LiDAR_based_Gait_Recognition.pdf
project_link: null
code_link: null
aliases:
- M2
- M2MSSTFNLBGR
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 多尺度跨区域交互和基于运动一致性的自适应时序加权。
primary_logic: 通过引入四种互补的空间交互策略以及基于余弦相似度的多尺度时序聚合，能够有效捕捉远距离身体部位的协调运动，并自适应处理步态时间异质性。
claims:
- MS2Gait在SUSTech1K和Free-Gait上分别达到93.5%和83.1%的Rank‑1准确率，均超越先前最优方法。
- 在SUSTech1K正常子集上，MS2Gait比LidarGait++的Rank‑1准确率提升2.4个百分点。
- 消融实验表明，Inter‑Set Mixing带来的增益最大，可反向传播信息以恢复被遮挡点的特征。
- MS2Gait在帧丢失实验中性能退化远小于LidarGait++，证明其对时间异质性的鲁棒性。
---

# MS^2Gait: A Multi-Scale Spatio-Temporal Fusion Network for LiDAR-based Gait Recognition

> [!tip] 核心洞察
> 通过引入四种互补的空间交互策略以及基于余弦相似度的多尺度时序聚合，能够有效捕捉远距离身体部位的协调运动，并自适应处理步态时间异质性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MS^2Gait：面向激光雷达步态识别的多尺度时空融合网络 |
| 英文题名 | MS^2Gait: A Multi-Scale Spatio-Temporal Fusion Network for LiDAR-based Gait Recognition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_MS2Gait_A_Multi-Scale_Spatio-Temporal_Fusion_Network_for_LiDAR-based_Gait_Recognition_CVPR_2026_paper.html) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | MS^2Gait |
| Dataset | SUSTech1K, Free‑Gait |

> [!tip] 效果简介
> - SUSTech1K (normal subset) 上，Rank‑1 accuracy (%) 93.5 vs 91.1 (LidarGait++) (+2.4)。
> - Free‑Gait 上，Rank‑1 accuracy (%) 83.1 vs prior best (e.g., LidarGait++) (outperforms previous methods)。

## 概要

步态识别在远距离、非受控场景下具有独特优势，但现有激光雷达步态方法存在双重瓶颈：**空间上**，传统逐点聚合策略无法建模身体不同区域间的远距离语义关联；**时间上**，简单的最大/平均池化难以应对步态序列的时间异质性——同一序列内不同步态阶段的信息密度差异巨大，直接压缩会丢失关键判别信息。

针对上述问题，本文提出 **MS²Gait**，一个面向原始点云步态序列的多尺度时空融合框架。其核心调控手段包括两方面：一是通过**四种互补的空间交互策略**（Intra‑Set、Inter‑Set、Intra‑Layer、Inter‑Layer Mixing）实现跨区域语义交互，使被遮挡部位能够通过反向信息传播恢复结构特征；二是通过**基于运动一致性的自适应时序加权**，利用多样性驱动的关键帧选择与多尺度余弦相似度聚合，对不同步态阶段赋予差异化权重。

实验表明，MS²Gait 在 **SUSTech1K** 正常子集上达到 **93.5%** 的 Rank‑1 准确率，较先前最优方法 **LidarGait++**（Shen et al., CVPR 2025）提升 **2.4 个百分点**；在 **Free‑Gait** 数据集上达到 **83.1%** 的 Rank‑1 准确率，超越所有已有方法。消融实验进一步揭示，四种 Mixing 策略贡献了最大增益，其中 **Inter‑Set Mixing** 的增益最为显著，在服装和雨伞等遮挡子集上分别带来 **+10.7%** 和 **+7.7%** 的提升。帧丢失鲁棒性实验中，MS²Gait 的性能退化幅度远小于 LidarGait++，验证了其对时间异质性的强鲁棒性。

在方法谱系上，MS²Gait 继承了激光雷达步态识别中直接处理原始点云的范式（区别于基于剪影的 **GaitSet**（Chao et al., AAAI 2019）和深度图投影方法 **SimpleView**（Goyal et al., ICML 2021）），并在空间建模上超越了 **PointNet++**（Qi et al., NeurIPS 2017）的局部聚合范式，在时序建模上取代了 **LidarGait++** 的池化压缩策略，为点云步态识别建立了新的多尺度时空融合基线。



### 步态识别：从二维到三维的演进

步态识别旨在通过个体的行走模式进行身份鉴别，具有远距离、非侵入、难以伪装等独特优势。长期以来，该领域由二维模态主导——基于轮廓的方法（如 **GaitSet**，Chao et al., AAAI 2019；**GaitBase**，Fan et al., CVPR 2023）在受控环境下取得了显著进展。然而，二维方法对光照变化、衣着遮挡和视角偏移高度敏感，其跨场景泛化能力存在根本性瓶颈。

随着深度传感技术的成熟，三维点云因显式编码几何结构而成为克服上述局限的有力替代。点云步态识别能够直接利用人体的三维表面信息，天然对光照和外观变化鲁棒。早期工作将点云投影为深度图像后借用二维分类器（如 **SimpleView**，Goyal et al., ICML 2021），或采用经典点云骨干网络 **PointNet++**（Qi et al., NeurIPS 2017）进行逐帧处理。**GaitCloud**（Zhang et al., WACV 2025）提出True-3D表示，进一步推动了端到端点云步态识别的发展。当前最先进的方法 **LidarGait++**（Shen et al., CVPR 2025）在SUSTech1K正常子集上达到91.1%的Rank‑1准确率，标志着点云步态识别已进入实用化探索阶段。

### 现有方法的两个结构性缺口

尽管取得了上述进展，现有方法在空间和时间两个维度上仍存在深层缺陷，制约了性能的进一步提升。

**空间维度：跨区域语义交互的缺失。** 步态的本质是全身多部位协调运动——手臂的摆动与对侧腿的迈步之间存在稳定的相位耦合，躯干的旋转补偿着下肢的推进。然而，现有方法的空间特征提取遵循“局部聚合-逐层抽象”的层级范式：每个点仅与其空间近邻交互，通过MLP+MaxPooling（式(2)）逐层压缩特征。这种设计虽然高效，但将信息流严格限制在局部邻域内，无法显式建模远距离身体部位之间的语义关联。当部分身体区域因自遮挡或外部遮挡而缺失时，孤立的空间处理无法利用其他区域的上下文信息来恢复被遮挡点的特征，导致判别力显著下降。

**时间维度：时序异质性的粗粒度处理。** 步态序列天然具有时间异质性——不同行走速度下步态周期长度不同，同一周期内不同相位（支撑相、摆动相）的信息密度也存在差异。现有方法普遍采用简单的最大池化或平均池化对整个序列进行等权压缩，这种“一刀切”的策略将关键帧与冗余帧、正常帧与异常帧混为一谈，既无法突出最具判别力的步态相位，也难以抑制噪声帧的干扰。当序列不完整或存在帧丢失时，这种粗粒度时序建模的性能退化尤为严重。

### 本文动机与核心思路

针对上述两个结构性缺口，本文提出 **MS^2Gait**——一个面向原始点云步态序列的多尺度时空融合框架。其核心思路可概括为两个层面：

1. **空间层面**：设计层次化空间特征提取器（HSFE），在传统SGM块的基础上引入四种互补的跨区域交互策略（Intra-Set、Inter-Set、Intra-Layer、Inter-Layer Mixing），使特征能够在不同身体区域之间流动，显式捕获远距离协调运动模式。同时，通过几何感知的多分辨率特征融合模块（GMFF）将不同尺度的特征对齐到统一的点分布，保留三维结构信息。

2. **时间层面**：提出基于相似度的时序增强Transformer（STET），以多样性驱动的关键帧选择替代均匀采样，以多尺度余弦相似度聚合替代等权池化，使模型能够自适应地聚焦于信息丰富的步态相位，并抑制异常帧的影响。

Figure 1 对比了传统方法与MS^2Gait在空间和时间特征提取上的本质差异：传统方法的空间交互局限于局部邻域，时间建模采用粗粒度池化；MS^2Gait则通过跨区域信息传播和自适应时序加权，实现了对步态时空结构的精细刻画。



## 核心方法与创新机理

MS²Gait 的核心创新围绕两个瓶颈展开：**空间上跨区域语义关联缺失**与**时间上步态异质性处理不足**。传统方法（如 LidarGait++，Shen et al., CVPR 2025）采用 MLP + MaxPooling 提取局部空间特征，各分辨率独立处理，时间维度则依赖简单最大/平均池化压缩整个序列。这种“孤立提取 + 均匀压缩”范式无法建模远距离身体部位的协调运动，也对遮挡、帧率变化等时间异质性敏感。

MS²Gait 通过三个关键设计（changed slots）系统性解决了上述问题：

### 1. 空间特征聚合：从硬池化到软注意力 + 四种互补交互

传统 SGM 模块使用 MaxPooling 对邻域点特征进行硬选择：

$$f_{i}^{\prime} = \operatorname*{maxpool}\bigl(g(p_{j} - p_{i}, f_{j})\bigr)$$

MS²Gait 将其替换为自适应 Softmax 加权聚合。对每个中心点 $i$，在候选集 $\mathcal{M}_i$ 上计算注意力分数：

$$s_{j} = g_{2}\big([g_{1}(f_{i} - f_{j}); \delta(p_{i} - p_{j})]\big)$$

$$f_{i}^{\prime} = \sum_{j \in \mathcal{M}_{i}} \operatorname{softmax}(s_{j}) \cdot g_{3}(f_{j})$$

其中 $\delta(p_i - p_j)$ 编码相对几何位置，使聚合权重同时依赖于语义差异和空间结构。这一软选择机制是后续跨区域交互的基础。

在此基础上，HSFE 引入四种互补交互策略（Figure 3）：
- **Intra-Set Mixing**：在同一集合内扩展邻域范围，增强局部上下文
- **Inter-Set Mixing**：跨集合信息传递，允许特征在人体不同部位间流动
- **Intra-Layer Mixing**：同分辨率层内交互
- **Inter-Layer Mixing**：跨分辨率层间交互

消融实验表明，**Inter-Set Mixing 贡献最大**——它通过反向信息传播恢复被遮挡点的特征（Figure 4 展示了下肢特征从脚部经腿部传播至髋部的混合链）。在 SUSTech1K 的服装子集和雨伞子集上，四种 Mixing 策略合计带来 **+10.7%** 和 **+7.7%** 的显著增益。

### 2. 多分辨率融合：从独立提取到几何感知对齐

传统方法各分辨率独立提取特征后直接拼接，忽略了不同尺度特征的空间对应关系。MS²Gait 的 **Geometry-Aware Multi-Resolution Feature Fusion (GMFF)** 模块将前两层的稀疏特征通过 3-近邻反距离插值对齐到第三层输出的统一点分布（Figure 5）：

$$w_{ij} = \frac{1}{d_{ij} + \varepsilon} \Bigg/ \sum_{l \in \mathcal{T}_{i}} \frac{1}{d_{il} + \varepsilon}$$

这种基于欧氏距离倒数的插值权重保留了三维几何结构，使多分辨率特征在统一的几何坐标系下融合，而非简单的通道拼接。

### 3. 时序建模：从均匀池化到多样性驱动的多尺度相似度聚合

传统方法对整个序列做最大/平均池化，无法应对步态的时间异质性（如帧丢失、速度变化）。MS²Gait 的 **Similarity-based Temporal Enhancement Transformer (STET)** 通过三个机制实现自适应时序建模：

**自适应关键帧选择**：根据序列长度 $T$ 动态确定关键帧数量：

$$K = \max(K_{\min}, \min(K_{\max}, \lfloor \alpha \cdot T \rfloor))$$

其中 $\alpha \in [0.5, 0.8]$。随后以贪心最大-最小策略选择多样性最强的帧：

$$i_k = \arg\min_{i \in \mathcal{R}_{k-1}} \max_{j \in S_{k-1}} \langle \bar{f}_i, \bar{f}_j \rangle$$

该策略确保选出的关键帧在特征空间中彼此最不相似，覆盖完整的步态周期变化。

**多尺度余弦相似度聚合**：对每个关键帧 $i_m$，在其局部和中程邻域内，按余弦相似度对原始帧加权聚合（Figure 6）：

$$\omega_{i_m, t}^{(s)} = \frac{\exp(\langle \bar{f}_{i_m}, \bar{f}_t \rangle)}{\sum_{j \in \mathcal{N}_{i_m}^{(s)}} \exp(\langle \bar{f}_{i_m}, \bar{f}_j \rangle)}$$

运动一致的帧获得高权重，异常帧被抑制。多尺度聚合结果通过残差门控融合：

$$\hat{f}_m = f_{i_m} + \sigma(\mathrm{MLP}(f_{i_m})) \odot f_m^{\mathrm{enhanced}}$$

**Transformer 编码**：融合后的关键帧特征加入位置编码后送入 Transformer，捕获长程时序依赖。

帧丢失实验（Figure 8）验证了 STET 对时间异质性的鲁棒性：在不同丢失率下，MS²Gait 的性能退化幅度均显著小于 LidarGait++。

### 创新总结

三个 changed slots 形成因果链路：**软注意力 + 跨区域交互**使空间特征包含远距离身体部位的协调信息；**几何感知对齐**确保多尺度特征在统一空间坐标系下融合；**多样性驱动的多尺度时序聚合**自适应处理步态周期的时间异质性。这一设计使 MS²Gait 在 SUSTech1K 正常子集上达到 **93.5%** Rank-1 准确率（较 LidarGait++ 提升 **+2.4%**），在 Free-Gait 上达到 **83.1%**，均超越先前最优方法。



MS^2Gait 的整体流程可形式化为一个端到端的映射：输入一帧原始点云步态序列 $P_o$，输出用于识别的最终特征 $F_{\mathrm{final}}$。其核心计算图由三个模块级联构成：

$$F_{\mathrm{final}} = \mathcal{T}\left(\mathcal{G}\left(\left[\mathcal{H}_i(P_o)\right]_{i=1}^4\right)\right)$$

其中 $\mathcal{H}_i$ 表示第 $i$ 个层次的空间特征提取器，$\mathcal{G}$ 为几何感知的多分辨率特征融合模块，$\mathcal{T}$ 为基于相似度的时序增强 Transformer。整个框架遵循“层次化人体部位聚类 → 多尺度空间交互 → 几何对齐融合 → 自适应时序聚合”的计算范式。

**输入与表征。** 网络直接接受原始点云序列，无需投影为深度图或轮廓图。输入序列经过层次化下采样，形成四个空间分辨率递减的点集，分别对应从细粒度局部几何到粗粒度身体部位的不同语义层次。

**空间特征提取（HSFE）。** 层次化空间特征提取器在每个分辨率层级上运行一个 SGM-Block，但与传统 SGM 的“MLP + MaxPooling”不同，MS^2Gait 将其替换为“MLP + Softmax 加权”的自适应聚合机制，并引入四种互补的交互策略——Intra-Set Mixing、Inter-Set Mixing、Intra-Layer Mixing 和 Inter-Layer Mixing——以显式捕获跨区域的远距离语义依赖。这些策略使信息能够在不同邻域集合和不同层级之间流动，从而恢复被遮挡部位的结构信息并建模身体部位的协调运动。

**多分辨率融合（GMFF）。** 四个层级提取的多尺度特征在空间分辨率和点分布上并不一致。几何感知多分辨率特征融合模块通过 3-近邻反距离插值，将前两层的特征对齐到第三层输出的统一点分布上，保留三维几何结构，随后将各分辨率特征拼接并池化，形成空间维度的紧凑表示。

**时序建模（STET）。** 空间融合后的逐帧特征送入基于相似度的时序增强 Transformer。该模块首先根据序列长度自适应确定关键帧数目 $K = \max(K_{\min}, \min(K_{\max}, \lfloor \alpha \cdot T \rfloor))$，再通过贪心最大-最小多样性选择策略挑选最具代表性的 $K$ 帧。随后，在局部和中程两个时间尺度上，以余弦相似度为权值对邻域内的原始帧进行加权聚合，生成增强特征。最后，经残差门控融合与位置编码后，由 Transformer 编码器捕获长程时序依赖，输出序列级步态表征用于识别。

**数据流概要。** 整体信息流为：原始点云序列 → 四层 HSFE（含跨层/跨集交互） → GMFF 几何对齐与拼接 → 逐帧池化 → STET 多样性选帧与多尺度相似度聚合 → Transformer 编码 → 最终步态嵌入。消融实验表明，四种 Mixing 策略贡献了最大的性能增益，其中 Inter-Set Mixing 通过反向信息传播恢复被遮挡点特征，在服装子集（+10.7%）和雨伞子集（+7.7%）上提升尤为显著；STET 则使模型在帧丢失实验中退化幅度远小于先前最优方法 LidarGait++，验证了其对时间异质性的鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/002_Figure_2.jpg]]
*Figure 2: MS2Gait Network Architecture. The proposed*

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of traditional and MS2Gait’s spatial and temporal feature extraction methods*



MS²Gait 的整体流程可形式化为：

$$F_{\mathrm{final}} = \mathcal{T}\left(\mathcal{G}\left(\left[\mathcal{H}_i(P_o)\right]_{i=1}^4\right)\right)$$

其中 $P_o$ 为输入点云序列，$\mathcal{H}_i$ 为第 $i$ 个层级空间特征提取器（HSFE），$\mathcal{G}$ 为几何感知多分辨率特征融合模块（GMFF），$\mathcal{T}$ 为时序增强模块（STET）。下文依次拆解各模块的数学设计。

### 1. 层级空间特征提取器（HSFE）

HSFE 的核心改造在于将传统 SGM 块中的“MLP + MaxPooling”替换为自适应“MLP + Softmax 加权”。传统聚合方式为：

$$f_i^{\prime} = \operatorname*{maxpool}\bigl(g(p_j - p_i, f_j)\bigr)$$

其中 $g$ 为共享 MLP，$p_j - p_i$ 为相对坐标，$f_j$ 为邻域点特征。这种硬性最大池化丢失了邻域内部的细粒度语义。

**Softmax 加权聚合**：对每个中心点 $i$，在其候选点集 $\mathcal{M}_i$ 上计算注意力分数：

$$s_j = g_2\bigl([g_1(f_i - f_j); \delta(p_i - p_j)]\bigr)$$

其中 $g_1$ 将特征差映射到高维空间，$\delta$ 为相对几何位置编码，$[\cdot;\cdot]$ 表示拼接，$g_2$ 输出标量分数。聚合特征为：

$$f_i^{\prime} = \sum_{j \in \mathcal{M}_i} \operatorname{softmax}(s_j) \cdot g_3(f_j)$$

$g_3$ 为值变换 MLP。该机制使模型自适应地关注信息量更大的邻域点。

**四种互补交互策略**：在 Softmax 加权基础上，HSFE 引入四种 Mixing 操作以捕获跨区域语义关联（参见 Figure 3）：
- **Intra-Set Mixing**：在同一采样集内进行特征传播；
- **Inter-Set Mixing**：跨不同采样集交换信息，消融实验表明其增益最大，可通过反向信息传播恢复被遮挡点的特征；
- **Intra-Layer Mixing**：同一层级内不同区域间的交互；
- **Inter-Layer Mixing**：跨层级的特征混合。

Figure 4 展示了特征传播链：脚部特征经 Mixing 迭代逐步传播至腿部区域，最终到达髋部，实现下肢完整信息交换。

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/004_Figure_4.jpg]]
*Figure 4: Feature mixing chain in HSFE. Mixing iterations propagate foot features through leg regions to the hip, enabling full lower-body information exchange*

### 2. 几何感知多分辨率特征融合（GMFF）

HSFE 输出四个层级的特征，各层点云分辨率不同。GMFF 通过 3-近邻反距离插值将前两层特征对齐到第三层的点分布，保留三维几何结构。插值权重为：

$$w_{ij} = \frac{1}{d_{ij} + \varepsilon} \Bigg/ \sum_{l \in \mathcal{T}_i} \frac{1}{d_{il} + \varepsilon}$$

其中 $d_{ij}$ 为目标点 $i$ 与源点 $j$ 的欧氏距离，$\mathcal{T}_i$ 为 $i$ 的 3 个最近邻源点集合，$\varepsilon$ 防止除零。对齐后的多分辨率特征经拼接和池化后送入时序模块。

### 3. 相似度驱动的时序增强 Transformer（STET）

STET 解决步态序列的时间异质性问题，包含三个阶段。

**多样性驱动的关键帧选择**：首先根据序列长度 $T$ 自适应确定关键帧数目：

$$K = \max(K_{\min}, \min(K_{\max}, \lfloor \alpha \cdot T \rfloor))$$

其中 $\alpha \in [0.5, 0.8]$。随后贪心地选择与已选集合在特征空间中最不相似的帧：

$$i_k = \arg\min_{i \in \mathcal{R}_{k-1}} \max_{j \in S_{k-1}} \langle \bar{f}_i, \bar{f}_j \rangle$$

$\mathcal{R}_{k-1}$ 为剩余候选帧，$S_{k-1}$ 为已选关键帧集合，$\langle\cdot,\cdot\rangle$ 为余弦相似度。该策略保证关键帧覆盖序列中的多样化步态相位。

**多尺度余弦相似度聚合**：对每个关键帧 $i_m$，在局部和中等两个尺度 $s$ 上，对邻域 $\mathcal{N}_{i_m}^{(s)}$ 内的原始帧按余弦相似度加权：

$$\omega_{i_m, t}^{(s)} = \frac{\exp(\langle \bar{f}_{i_m}, \bar{f}_t \rangle)}{\sum_{j \in \mathcal{N}_{i_m}^{(s)}} \exp(\langle \bar{f}_{i_m}, \bar{f}_j \rangle)}$$

聚合特征为 $\phi_m^{(s)} = \sum_{t \in \mathcal{N}_{i_m}^{(s)}} \omega_{i_m, t}^{(s)} f_t$。两尺度特征经 softmax 融合后得到增强特征 $f_m^{\mathrm{enhanced}}$。

**残差门控融合**：通过可学习的门控残差连接保留原始信息：

$$\hat{f}_m = f_{i_m} + \sigma(\mathrm{MLP}(f_{i_m})) \odot f_m^{\mathrm{enhanced}}$$

其中 $\sigma$ 为 sigmoid 函数，$\odot$ 为逐元素乘。最后，增强后的关键帧序列经位置编码和 Transformer 编码器捕获长程时序依赖，输出最终步态表征。

### 补充图表

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/003_Figure_3.jpg]]
*Figure 3: Four complementary interaction strategies in HSFE, jointly boosting cross-scale spatial semantics*

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/005_Figure_5.jpg]]
*Figure 5: Design of the interpolation-based feature alignment module. Features from the first two layers are geometrically aligned to the output of layer 3 after hierarchical sampling*

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/006_Figure_6.jpg]]
*Figure 6: Similarity-based aggregation. Coherent frames within phases receive high weights, while outliers are suppressed, yielding robust representations across varying conditions*



## 实验与关键发现

### 主实验：SUSTech1K 与 Free‑Gait 上的性能对比

MS^2Gait 在两个大规模 LiDAR 步态数据集上均取得最优结果。在 **SUSTech1K** 的 normal 子集上，MS^2Gait 的 Rank‑1 准确率达到 **93.5%**，比此前最优方法 **LidarGait++** (Shen et al., CVPR 2025) 的 91.1% 提升 **2.4 个百分点**（Table 1）。在更具挑战性的 **Free‑Gait** 数据集上，MS^2Gait 同样以 **83.1%** 的 Rank‑1 准确率超越所有先前方法（Table 2）。上述结果表明，多尺度空间交互与自适应时序建模的组合设计在受控场景和开放场景下均能稳定发挥作用。

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/007_Table_1.jpg]]
*Table 1: Comparison on SUSTech1K. Silh: Silhouettes, DIs: Depth Images, PCs: raw Point Clouds, R1: Rank-1, R5: Rank-5*

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/009_Table_2.jpg]]
*Table 2: Comparison on FreeGait. Silh: Silhouettes, DIs: Depth Images, PCs: raw Point Clouds, mAP: mean Average Precision*

### 消融实验：四种 Mixing 策略的贡献

消融实验揭示了空间交互模块中各策略的差异化作用（Table 4）。**四种 Mixing 策略整体贡献了最大幅度的性能提升**，尤其在服装子集（+10.7%）和雨伞子集（+7.7%）等遮挡严重的条件下增益显著。在四种策略中，**Inter‑Set Mixing 提供的增益最大**，其机制在于通过跨集合的信息反向传播，使被遮挡点能够从可见区域恢复有效的结构特征。这一发现直接支撑了论文的核心主张：跨区域语义关联建模是解决 LiDAR 步态识别中遮挡问题的关键因果手段。

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/010_Table_4.jpg]]
*Table 4: Ablation results on SUSTech1K. Note that experiments 9–11 are based on the full-scale HSFE module*

### 鲁棒性分析：对时间异质性的容忍度

帧丢失实验用于检验时序模块对不完整序列的鲁棒性（Figure 8）。在不同丢帧率下，MS^2Gait 在所有评估指标上的性能退化幅度均显著小于 LidarGait++，证明 **STET 模块的多尺度余弦相似度聚合与多样性驱动关键帧选择能够有效应对步态序列的时间异质性**。这一优势源于 STET 不依赖固定长度的时序压缩，而是通过自适应关键帧数量 $K = \max(K_{\min}, \min(K_{\max}, \lfloor \alpha \cdot T \rfloor))$ 和基于特征空间最大‑最小不相似度的帧选择机制，在序列不完整时仍能保留具有判别力的时序结构。

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/008_Figure_8.jpg]]
*Figure 8: Robustness to Temporal Heterogeneity. Performance under varying frame dropout rates on FreeGait. MS2Gait exhibits smaller degradation across all metrics than LidarGait++, showing superior robustness to incomplete temporal sequences*

### 跨域评估与计算效率

跨域评估（Figure 7）显示，MS^2Gait 在 SUSTech1K 与 Free‑Gait 之间存在点云密度差异的情况下仍表现出相对稳健的性能，表明 GMFF 模块的几何感知多分辨率特征对齐有助于缓解域间密度偏移的影响。计算效率方面（Table 3），尽管 MS^2Gait 引入了多种交互策略和 Transformer 编码，其推理成本仍处于可接受范围，具体数值需查阅原表。

### 可视化分析：特征激活与聚类质量

特征激活可视化（Figure 9）表明，与 PointNet++ 基线相比，MS^2Gait 的注意力逐渐聚焦于与步态相关的判别性身体区域，同时抑制背包等无关物体。特征聚类分析（Figure 11）进一步证实：PointNet++ 的类间分离较差，LidarGait++ 仍有部分类别混淆，而 MS^2Gait 实现了最大的类间间隔和最小的类内散布，将先前纠缠的类别清晰分离。交互区域验证（Figure 10）则直观展示了跨区域信息传播在遮挡场景下对特征恢复的实际效果。

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/014_Figure_11.jpg]]
*Figure 11: Inter-/intra-class distance statistics and t-SNE visualizations. (a) PointNet++: Poor separation. (b) LidarGait++: Suboptimal separation, with poorly distinguished classes. (c) MS2Gait: Maximal inter-class margin and minimal intra-class spread, cleanly separating previously entangled classes*

![[assets/figures/papers/paper_list_l1073_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_MS2Gait_A_Multi_Sca/figures/013_Figure_9.jpg]]
*Figure 9: Feature activation visualization. Compared to Point-Net++ baseline, our method progressively focuses on discriminative gait-relevant regions while suppressing irrelevant objects*



## 定位与知识库关联

### 1. 方法脉络与基线关系

MS^2Gait 定位于**直接作用于原始点云序列的步态识别**路线，其直接对比的前沿方法为 **LidarGait++**（Shen et al., CVPR 2025），后者是此前在 SUSTech1K 和 Free-Gait 两个 LiDAR 步态基准上取得最优性能的方法。LidarGait++ 采用 Set Abstraction 风格的逐层点云特征提取，但空间上缺乏跨区域语义交互，时间上依赖简单池化压缩整段序列。MS^2Gait 正是在这两个维度上做出系统性改进。

在更广泛的方法谱系中，该工作与以下基线形成参照：

- **经典点云基线**：**PointNet++**（Qi et al., NeurIPS 2017）作为点云特征学习的通用范式，被用作空间特征提取的基础骨架。论文通过特征激活可视化（Figure 9）表明，PointNet++ 难以聚焦于步态判别性区域，而 MS^2Gait 的 HSFE 模块逐步将注意力集中到人体关键部位并抑制无关物体。
- **2D 步态基线**：**GaitSet**（Chao et al., AAAI 2019）和 **GaitBase**（Fan et al., CVPR 2023）代表了基于剪影的步态识别路线。在 SUSTech1K 上，这些 2D 方法受限于视角变化和外观信息丢失，性能显著低于直接利用三维几何的点云方法。
- **深度图像基线**：**SimpleView**（Goyal et al., ICML 2021）将深度图作为点云分类的投影表示，在步态任务上被用作对比。其性能介于 2D 剪影方法与原始点云方法之间，受投影信息损失制约。
- **点云步态基线**：**GaitCloud**（Zhang et al., WACV 2025）采用 True-3D 表示进行点云步态识别，是除 LidarGait++ 外的另一直接对比对象。MS^2Gait 在 SUSTech1K 和 Free-Gait 上均报告了对其的显著超越。

### 2. 核心改进槽位

MS^2Gait 相对于 LidarGait++ 等基线，在三个关键设计槽位上做出了可验证的替换：

| 设计槽位 | 基线方案 | MS^2Gait 方案 | 证据强度 |
|---------|---------|--------------|---------|
| 空间特征聚合 | MLP + MaxPooling（传统 SGM） | MLP + Softmax 加权 + 四种互补交互策略（Intra-Set / Inter-Set / Intra-Layer / Inter-Layer Mixing） | 消融实验证实四种 Mixing 策略贡献最大提升，其中 Inter-Set Mixing 增益最显著 |
| 多分辨率融合 | 各分辨率独立提取，无跨尺度交互 | Geometry-Aware Multi-Resolution Feature Fusion（GMFF）：通过 3-近邻反距离插值将多分辨率特征对齐到统一点分布 | 作为 HSFE 的必要组成，消融中全尺度 HSFE 配置取得最优结果 |
| 时序建模 | 简单最大/平均池化压缩整个序列 | Similarity-based Temporal Enhancement Transformer（STET）：多样性驱动关键帧选择 + 多尺度余弦相似度聚合 + Transformer 编码 | 帧丢失实验中 MS^2Gait 退化远小于 LidarGait++，证明时序鲁棒性 |

### 3. 适用边界与局限

**适用场景**：该方法在标准步态采集条件（SUSTech1K normal 子集，Rank-1 93.5%）和挑战性条件（Free-Gait，Rank-1 83.1%）下均取得最优，且在服装变化（+10.7%）和持伞（+7.7%）等遮挡场景下增益尤为突出。跨域评估（Figure 7）显示其在点云密度差异下具有相对鲁棒的跨数据集泛化能力。

**已知局限**：当前分析材料中未提取到论文明确声明的局限性或失败模式。以下推断需人工验证：

- 四种 Mixing 策略的迭代传播机制（Figure 4 所示的足部→腿部→髋部特征链）依赖于层次化的人体部位聚类假设，对于严重非刚性形变或非标准姿态（如跌倒、爬行）的泛化能力未经验证。
- STET 的自适应关键帧数量 $K = \max(K_{\min}, \min(K_{\max}, \lfloor \alpha \cdot T \rfloor))$ 依赖序列长度 $T$ 和固定比例 $\alpha \in [0.5, 0.8]$，在极短序列（如 $T < 10$）下关键帧选择空间受限，可能退化为近似全序列处理。
- 计算效率方面，Table 3 报告了与 LidarGait++ 的效率对比，但四种 Mixing 策略和 Transformer 编码引入的额外计算开销在实时部署场景下的可行性需结合具体数值确认。

### 4. 开放问题

分析材料中未提取到论文明确提出的开放问题。从方法设计逻辑可推演出以下值得关注的后续方向（需人工验证是否与原文意图一致）：

- Inter-Set Mixing 通过反向信息传播恢复被遮挡点特征，这一机制在更极端的遮挡条件（如多人交互、大范围环境遮挡）下的有效性边界尚未探明。
- 多样性驱动的关键帧选择（公式 7 的贪心 max-min 策略）在理论上可能偏好异常帧，其对步态周期完整性的保证缺乏理论分析。
- 该方法目前仅在两套 LiDAR 数据集上验证，向其他三维传感器（如 ToF 相机、毫米波雷达点云）的迁移能力未知。



## 原文 PDF

![[paperPDFs/CVPR_2026/MS_2Gait_A_Multi_Scale_Spatio_Temporal_Fusion_Network_for_LiDAR_based_Gait_Recognition.pdf]]
