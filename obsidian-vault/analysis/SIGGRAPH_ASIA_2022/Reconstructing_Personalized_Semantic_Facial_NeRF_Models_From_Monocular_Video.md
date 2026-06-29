---
title: Reconstructing Personalized Semantic Facial NeRF Models From Monocular Video
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Reconstructing_Personalized_Semantic_Facial_NeRF_Models_From_Monocular_Video.pdf
project_link: null
code_link: "https://github.com/USTC3DV/NeRFBlendShape-code"
aliases:
- RPSFNMFMV
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_rendering_materials
- topic/graphics_animation_interaction
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将表达系数用于在潜在空间中线性组合多个具有语义意义的多级体素场（哈希表），形成隐式混合形状表示，使局部特征能够被全局修改，从而适应MLP的输入分布。
primary_logic: 隐式线性混合架构（表达系数加权多个语义基哈希表）有效降低了MLP的学习负担，使得仅需10-20分钟的单目视频训练即可重建包含个性化细节（如头发、皱纹）的照片级真实感动态头部模型。
claims:
- Our model learns a dynamic head scene in less than 20 minutes, while the concatenate baseline and NerFACE cannot produce plausible results in that time.
- The implicit blending architecture enables local features to be modified by expression coefficients globally, reducing the learning burden of the MLP.
- Our method achieves the best quantitative results on all metrics compared to FOMM, NerFACE, and NHA on self-reenactment.
- Self-reenactment (Hillary Clinton's video and others) 上 MSE (×10⁻²)↓ = 0.48
---

# Reconstructing Personalized Semantic Facial NeRF Models From Monocular Video

> [!tip] 核心洞察
> 隐式线性混合架构（表达系数加权多个语义基哈希表）有效降低了MLP的学习负担，使得仅需10-20分钟的单目视频训练即可重建包含个性化细节（如头发、皱纹）的照片级真实感动态头部模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从单目视频重建个性化语义面部神经辐射场模型 |
| 英文题名 | Reconstructing Personalized Semantic Facial NeRF Models From Monocular Video |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://ustc3dv.github.io/NeRFBlendShape/) · [Code](https://github.com/USTC3DV/NeRFBlendShape-code) |
| Topic | #topic/graphics_rendering_materials #topic/graphics_animation_interaction #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | NeRFBlendShape |
| Dataset | Self-reenactment |

> [!tip] 效果简介
> - Self-reenactment (Hillary Clinton's video and others) 上，MSE (×10⁻²)↓ 0.48 vs 0.69 (NHA) (-0.21)。
> - Self-reenactment 上，L1 (×10⁻²)↓ 0.70 vs 0.80 (NHA) (-0.10)；PSNR↑ 34.15 vs 32.85 (NHA) (+1.30)；SSIM (×10⁻¹)↑ 9.73 vs 9.69 (NHA) (+0.04)。

## 概要

从单目视频快速重建具有个性化细节的动态头部模型面临核心瓶颈：现有基于NeRF的方法（如NerFACE、AD-NeRF）将表达系数直接与空间特征拼接输入MLP，导致网络难以高效学习表情变化与空间位置的关联，训练缓慢且动态区域（嘴、眼）质量欠佳。

本文提出**NeRFBlendShape**，一种隐式线性混合架构。核心思路是将表达系数用于在潜在空间中线性组合多个具有语义意义的多级体素场（哈希表），形成隐式混合形状表示，使局部特征被全局修改以适配MLP的输入分布，从而显著降低网络学习负担。

仅需10–20分钟的单目视频训练，即可重建包含头发、皱纹等个性化细节的照片级真实感动态头部模型。在自重建任务上，本方法在MSE、PSNR、SSIM、LPIPS等全部指标上均优于FOMM、NerFACE和NHA。该工作将面部混合形状的思想引入NeRF哈希表空间，为动态场景的高效神经表示提供了新路径。

## 核心方法与创新机理

### 问题背景与核心瓶颈

从单目视频重建可驱动的照片级真实感头部模型是计算机视觉和图形学中的长期挑战。传统基于网格的方法（如3D Morphable Model）虽然具有语义可解释性，但受限于几何分辨率，难以捕捉头发、皱纹、皮肤纹理等个性化细节。近年来，基于神经辐射场（NeRF）的动态头部建模方法（如NerFACE、AD-NeRF）虽然提升了渲染质量，却面临一个关键的效率瓶颈：**这些方法将表达系数直接与位置编码或哈希特征在特征空间拼接后输入MLP，导致MLP难以高效学习表达信息与空间位置的关联**。具体而言，拼接操作使得表达系数只能以局部方式影响特征——每个采样点的特征仅被其自身的表达系数修改，MLP需要在深度网络中反复建立表达-空间-外观之间的复杂映射关系。这使得训练过程极其缓慢，尤其在嘴巴、眼睛等高动态区域，模型需要大量迭代才能收敛到可接受的质量。

### 核心创新：隐式混合形状架构

本文提出的NeRFBlendShape方法从根本上改变了表达条件的注入方式。其核心洞察是：**将表达系数用于在潜在空间（体素场空间）中线性组合多个具有语义意义的多级体素场，形成隐式混合形状表示，使局部特征能够被全局修改，从而适应MLP的输入分布，大幅降低MLP的学习负担**。

这一设计的因果链条清晰：传统拼接方法中，MLP必须同时承担“理解表达”和“解码外观”两个任务；而线性混合架构将“理解表达”的任务前置到哈希表组合阶段——表达系数在体素特征层面完成全局性的特征调制，MLP只需处理已经“表达感知”的特征向量，专注于解码密度和颜色。这种任务解耦使得MLP可以从深层（7层）宽体（128神经元）的沉重架构缩减为仅4层、64神经元宽度的轻量级网络，同时获得更快的收敛速度和更好的渲染质量。

### 方法框架与模块顺序

NeRFBlendShape的完整pipeline由以下模块按顺序构成：

**1. 面部追踪预处理**：给定单目RGB视频序列，使用现成的面部追踪器（off-the-shelf face tracker）提取每一帧的表达系数 $\mathbf{w} \in \mathbb{R}^K$、头部姿态和相机内参。表达系数来自网格混合形状模型的低维参数空间，具有语义可解释性，且与身份解耦。

**2. 多基哈希表表示**：模型维护 $K+1$ 个多分辨率哈希表（multi-level voxel fields），其中 $\mathbf{h}_0 \in \mathbb{R}^{L \times T \times F}$ 表示平均形状（neutral shape）的体素场，$\mathbf{H} = \{\mathbf{h}_1, \mathbf{h}_2, ..., \mathbf{h}_K\}$ 表示 $K$ 个表达位移基（expression displacement bases）。每个哈希表采用Instant NGP风格的多分辨率结构（16个层级，哈希表大小 $2^{14}$，特征维度4，最粗分辨率16，最细分辨率1024，如表1所示），在不同空间粒度上编码场景特征。

**3. 线性混合（核心操作）**：对于给定的表达系数 $\mathbf{w}$，通过线性组合得到该表达对应的哈希表：
$$\mathbf{h} = \mathbf{h}_0 + \mathbf{H} \mathbf{w} = \mathbf{h}_0 + \sum_{i=1}^{K} w_i \mathbf{h}_i$$

这一操作在体素空间（latent space）完成，意味着每个空间位置的体素特征被所有表达基按系数权重全局性地修改。与拼接方法中表达系数仅局部作用于单个采样点不同，线性混合使得整个体素场随表达系数平滑变化，形成空间连续的形变场。

**4. 哈希编码与MLP解码**：对于沿相机光线采样的空间点 $\mathbf{x}$，在组合后的哈希表 $\mathbf{h}$ 中进行多分辨率插值查询，得到哈希编码 $\eta(\mathbf{x}; \mathbf{h})$。轻量级MLP $g_\theta$ 将该编码与视线方向 $\gamma(\mathbf{d})$ 映射为密度 $\sigma$ 和颜色 $c$：
$$g_{\theta} : (\eta(\mathbf{x}; \mathbf{h}), \gamma(\mathbf{d})) \mapsto (\sigma, c)$$

MLP仅为4层、每层64个神经元，远小于拼接基线方法的7层128宽MLP。

**5. 体渲染**：沿光线累积密度和颜色，生成最终像素颜色：
$$I(\mathbf{r}) = \int_{0}^{\infty} p(t) c(\mathbf{r}(t)) dt, \quad p(t) = \exp\left(-\int_{0}^{t} \sigma(\mathbf{r}(s)) ds\right) \sigma(\mathbf{r}(t))$$

**6. 表达感知密度网格加速**：为加速光线步进（ray marching），传统Instant NGP使用基于平均形状的静态占用网格跳过空区域。然而，不同表情下头部占据的空间范围可能显著不同（如张嘴时下颌区域扩大），静态网格会导致部分有效区域被错误跳过（如图3所示）。本文提出表达感知密度网格更新策略：为每个表达基 $i$ 计算其在训练数据中的最大权重 $\hat{w}_i = \max_{j \in [1,N]} w_i^j$，构建对应密度网格 $\hat{\mathbf{h}}_i = \mathbf{h}_0 + \hat{w}_i \mathbf{h}_i$。推理时根据当前表达系数选择最匹配的预计算网格，确保覆盖所有可能的表达范围。

### 训练策略与损失函数

训练过程固定表达系数和相机参数，仅优化哈希表参数和MLP权重。总损失函数为三项的加权和：
$$L_{total} = \lambda_1 L_{color} + \lambda_2 L_{mask} + \lambda_3 L_{LPIPS}$$

其中 $L_{color}$ 为颜色重建损失，$L_{mask}$ 为头部掩膜损失（通过预训练的语义分割模型获取），$L_{LPIPS}$ 为感知损失（LPIPS），用于提升渲染图像的感知质量和个性化面部细节。

训练采用三阶段策略：前两个epoch同时使用颜色损失和掩膜损失（$\lambda_1=\lambda_2=1, \lambda_3=0$），快速建立头部几何和大致外观；第2至第7个epoch仅使用颜色损失（$\lambda_2=\lambda_3=0$），精细优化纹理细节；后续阶段引入感知损失（$\lambda_3$ 设为较小权重），进一步提升照片真实感。这种渐进式训练策略确保了几何稳定性与纹理质量的平衡。

### 三个关键Changed Slot

相较于现有的NeRF动态头部建模方法，NeRFBlendShape在以下三个关键设计点上做出了根本性改变：

**Changed Slot 1：表达条件注入机制（从拼接转向线性混合）**

基线方法（如图5所示）将哈希表查询得到的特征向量与表达系数在特征空间拼接后送入MLP。这种设计的根本问题在于：拼接操作使得表达信息与空间特征在MLP输入端处于“并列但未融合”的状态，MLP的前几层必须学习如何将两者有效结合。由于表达系数是全局低维向量（通常几十维），而哈希特征是局部高维向量，两者的信息密度和语义层级严重不匹配，导致MLP需要更深的网络和更多的迭代来建立有效映射。

NeRFBlendShape将表达条件注入从特征空间前移至体素空间：表达系数直接线性组合多个完整的体素场。这一改变使得每个空间位置的体素特征在查询之前就已经被表达信息全局调制——特征本身成为“表达感知”的。MLP接收到的输入已经隐含了表达信息，无需再学习表达-空间的关联，从而可以用更浅的网络实现更快的收敛。图7和图8的实验证据直接支撑了这一因果机制：线性混合架构在仅5分钟训练后即可重建张嘴、闭眼等动态表情，而拼接基线和NerFACE在20分钟内仍无法产生合理结果。

**Changed Slot 2：模型架构（从深宽MLP到多哈希表+浅MLP）**

拼接基线使用单个哈希表加7层128宽的深度MLP，试图通过MLP的容量来弥补表达信息融合的不足。NeRFBlendShape采用 $K+1$ 个独立哈希表（平均形状+ $K$ 个位移基）加4层64宽浅MLP。参数量的重新分配是关键：将表达建模能力从MLP转移到多个哈希表中，每个哈希表专门负责一种表达基的空间特征编码。这种“宽哈希表空间 + 窄MLP”的设计使得表达解耦发生在体素层面，每个基可以学习到语义上有意义的形变模式（如图9所示，学习到的基与网格混合形状在语义上一致，但包含更丰富的照片级细节）。

**Changed Slot 3：密度网格更新策略（从静态到表达感知）**

传统Instant NGP风格的密度网格基于单一静态场景（通常是平均形状）预计算占用信息。在动态头部场景中，不同表情下的空间占用差异显著——例如张嘴时下颌区域的体素在平均形状网格中可能被标记为空。NeRFBlendShape提出为每个表达基计算最大权重下的密度网格，推理时根据当前表达系数动态选择或组合网格。这一改变确保了加速结构始终覆盖当前表情的有效区域，避免了因网格不匹配导致的渲染空洞或几何缺失（如图13消融实验所示）。

### 推理路径与跨身份重演

推理时，给定目标人物的表达系数序列（可来自任意说话者的面部追踪结果），模型通过线性混合组合哈希表基，经MLP解码和体渲染生成对应表情的RGB图像。由于表达系数空间与身份解耦（继承自网格混合形状模型），模型天然支持跨身份重演：使用源人物的表达系数驱动目标人物的模型基，即可生成目标人物做出源人物表情的逼真渲染（如图6所示）。整个推理过程无需任何微调或适配，渲染速度达到每帧数十毫秒量级。

### 关键公式变量含义总结

- $\mathbf{h}_0$：平均形状的多级哈希表，编码中性表情的体素场
- $\mathbf{H} = \{\mathbf{h}_i\}_{i=1}^K$：$K$ 个表达位移基的哈希表集合，每个基编码一种表达变化模式
- $\mathbf{w} \in \mathbb{R}^K$：表达系数向量，低维语义参数
- $\eta(\mathbf{x}; \mathbf{h})$：在组合哈希表 $\mathbf{h}$ 中对点 $\mathbf{x}$ 的多分辨率插值编码
- $\gamma(\mathbf{d})$：视线方向 $\mathbf{d}$ 的位置编码
- $g_\theta$：轻量级MLP（4层，宽度64）
- $\hat{w}_i$：第 $i$ 个表达基在训练数据中的最大系数值，用于构建表达感知密度网格

![[assets/figures/papers/paper_list_l82_https_ustc3dv_github_io_NeRFBlendShape/figures/002_Figure_2.jpg]]
*Figure 2: Our pipeline, we track the RGB sequence and get expression coefficients, poses and intrinsics. Then we use the tracked expression coefficients to combine multiple multi-level hash tables to get a hash table corresponding to a specific expression. Then the sampled point is queried in hash table to get voxel features, we use an MLP to interpret the voxel features as RGB and density. We fix the expression coefficients and optimize the hash tables and MLP to get our head model*

![[assets/figures/papers/paper_list_l82_https_ustc3dv_github_io_NeRFBlendShape/figures/006_Figure_5.jpg]]
*Figure 5: Baseline architecture. The queried feature in hash table is concatenated with expression code as the input of MLP. We use a deeper and wider MLP to demonstrate its representation ability. A 2-layer MLP is used to map the expression coefficients to be concatenated with the queried feature*

## 实验与关键发现

### 主结果：自重建任务上的定量对比

论文在自重建（self-reenactment）任务上对 NeRFBlendShape 与三种代表性方法进行了系统比较：基于图像的人脸重演方法 **FOMM**、基于 NeRF 的面部重演方法 **NerFACE**（Gafni et al., 2021）、以及头部化身方法 **NHA**。所有方法在相同数据划分和评估协议下进行测试。

Table 2 给出了 Hillary Clinton 视频上的完整定量结果。NeRFBlendShape 在所有五个指标上均取得最优：

![[assets/figures/papers/paper_list_l82_https_ustc3dv_github_io_NeRFBlendShape/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluation of our method in comparison to state-ofthe-art facial reenactment methods based on self-reenactment. We compute the mean value and standard deviation of every method*

| 指标 | NeRFBlendShape | NHA（次优） | 相对提升 |
|------|----------------|-------------|----------|
| MSE (×10⁻²)↓ | **0.48** | 0.69 | -30.4% |
| L1 (×10⁻²)↓ | **0.70** | 0.80 | -12.5% |
| PSNR↑ | **34.15** | 32.85 | +1.30 dB |
| SSIM (×10⁻¹)↑ | **9.73** | 9.69 | +0.04 |
| LPIPS (×10⁻²)↓ | **2.67** | 3.37 | -20.8% |

**关键观察**：PSNR 领先 NHA 1.30 dB，LPIPS 感知损失降低 20.8%，表明 NeRFBlendShape 不仅在像素精度上更优，在感知质量上也显著提升。值得注意的是，NerFACE 和 FOMM 在各项指标上均明显弱于 NHA 和本文方法，体现了基于 NeRF 的隐式表示在照片真实感渲染上的结构性优势。

**证据强度**：Table 2 提供了各方法的均值和标准差，数据完整可靠（置信度 0.98）。但需注意，论文仅汇报了单段视频（Hillary Clinton）的定量结果，其他人物视频仅展示了定性比较（Fig. 4），跨身份泛化性需要更多定量证据支撑。

### 定性比较：个性化细节与表达保真度

Fig. 4 展示了与 FOMM、NerFACE、NHA 的定性对比。NeRFBlendShape 在以下方面展现出明显优势：

![[assets/figures/papers/paper_list_l82_https_ustc3dv_github_io_NeRFBlendShape/figures/005_Figure_4.jpg]]
*Figure 4: Comparison with state-of-the-art head modeling and facial reenactment methods. We can see that our model reconstruct high-fidelity expressions and facial details. YouTube ID of Hillary Clinton’s video is -yHgE9W699w*

- **个性化面部细节保留**：皱纹、皮肤纹理等身份相关细节被高保真重建，而 FOMM 和 NHA 倾向于产生模糊或丢失这些细节。
- **动态区域重建质量**：嘴巴张开、闭眼等极端表情下，本文方法仍能保持几何和纹理的合理性。NerFACE 在类似训练时间下无法产生可信结果（Fig. 7）。
- **3D 一致性**：如 Fig. 11 所示，模型支持自由视点合成，从侧面观察时头发、耳朵等结构保持几何合理，这源于 NeRF 固有的 3D 表示能力，而基于 2D 的 FOMM 无法实现。

### 核心消融实验

#### 1. 隐式线性混合 vs. 拼接基线（Fig. 7, Fig. 8）

这是论文最具决定性的消融实验，直接验证了核心因果机制——**隐式线性混合架构有效降低了 MLP 的学习负担**。

实验设置了两组对照：
- **拼接基线（concatenate baseline）**：将表达系数与哈希查询特征拼接后输入 MLP，使用更深的网络（7 层密度 MLP + 1 层颜色 MLP，宽度 128）以证明其表示能力。同时引入 2 层 MLP 将表达系数映射到更高维再拼接，以减少学习难度。
- **NerFACE**：Gafni et al. 的拼接策略，表达系数与位置编码拼接后输入 MLP。

**核心发现**：
- **训练速度**：NeRFBlendShape 在 **5 分钟**训练后即可忠实重建张嘴、闭眼等动态表情，而拼接基线和 NerFACE 在 20 分钟内都无法产生可信结果（Fig. 7）。
- **PSNR 收敛曲线**：Fig. 8 显示，本文方法的 PSNR 随训练时间快速上升并稳定在高位，拼接基线和 NerFACE 的 PSNR 增长缓慢且最终远低于本文方法。
- **因果解释**：拼接策略要求 MLP 自行学习表达信息与空间位置的复杂关联，尤其对嘴巴、眼睛等动态区域，MLP 难以在有限训练时间内解耦这些因素。而隐式混合形状架构在**体素空间**完成表达系数的线性组合（Eq. 2），使得局部特征被全局修改以适应 MLP 的输入分布，大幅降低了 MLP 的学习负担。

**证据强度**：置信度 0.95。实验设计合理，对比清晰，训练时间曲线和定性结果相互印证。

#### 2. 感知损失的作用（Fig. 12）

消融感知损失（LPIPS）的实验表明：
- 去除 LPIPS 后，渲染质量下降，尤其是高频细节（皱纹、皮肤纹理）变得模糊。
- LPIPS 作为感知级监督信号，有效引导模型捕捉个性化面部属性，而仅靠 L1/L2 颜色损失难以恢复这些细节。

**证据强度**：置信度 0.9。论文仅展示了定性对比图，未提供定量指标变化。

#### 3. 表达感知密度网格更新策略（Fig. 13）

标准 Instant-NGP 使用静态中性头部密度网格加速光线采样，但这在处理张嘴等极端表情时存在问题——中性头部的密度网格可能不覆盖张嘴时的口腔区域，导致采样点落在网格外（Fig. 3）。

![[assets/figures/papers/paper_list_l82_https_ustc3dv_github_io_NeRFBlendShape/figures/003_Figure_3.jpg]]
*Figure 3: The density grid of a specific expression may not cover all the expression cases. Heads in some frames may be out of the range*

本文提出**表达感知密度网格**：为每个基计算其最大表达系数权重（Eq. 9），构建覆盖所有训练表情的密度网格。

消融结果显示：
- 使用静态中性密度网格时，张嘴表情的口腔区域出现明显伪影（Fig. 13）。
- 表达感知策略使密度网格覆盖所有可能的表情空间，张嘴等极端表情的重建质量显著改善。

**证据强度**：置信度 0.9。定性对比清晰，但未提供定量指标。

#### 4. 密度网格对训练效率的影响（Fig. 14）

在相同训练时间内，使用密度网格的模型 PSNR 更高。密度网格通过跳过空白区域加速光线采样，使更多计算资源集中于有效区域，从而在固定训练预算下提升渲染质量。

### 失败模式与适用边界

论文明确列出了四个限制条件：

1. **跟踪误差敏感**：方法依赖现有人脸跟踪器提取表达系数和头部姿态。当跟踪出现较大误差时，重建模型会丢失细节。这是管线式方法的固有脆弱性——上游模块的错误会直接传播到下游。

2. **表达系数外推伪影**：当驱动模型的表达系数偏离训练分布较远时，某些局部区域可能出现伪影。这表明隐式混合形状的线性外推能力有限，极端表情的泛化需要更多训练数据覆盖。

3. **快速非刚性头发变形**：如果头发经历快速且剧烈的非刚性变形，头发区域可能出现伪影。这是因为当前架构仅通过表达系数驱动，缺乏对头发独立运动的显式建模。这是一个结构性的能力边界——隐式混合形状假设所有运动由表达系数控制，无法解耦头发的物理运动。

4. **几何表面质量**：从密度场提取的等值面可能存在噪声。论文建议未来工作可结合 SDF 类 NeRF 表面表示以改善几何质量，但需保持训练效率。

### 开放问题与改进方向

- 如何减少表达系数外推时的伪影？可能需要引入正则化或非线性扩展。
- 如何处理快速非刚性头发变形？可能需要引入额外的运动场或物理先验。
- 能否在保持训练效率的前提下提升几何表面质量（如采用 SDF 表示）？
- 隐式线性混合架构能否泛化到头部以外的动态场景重建任务？

### 实验设置要点

- **哈希表配置**（Table 1）：16 级多分辨率哈希表，每表大小 2¹⁴，特征维度 4，最粗分辨率 16，最细分辨率 1024。
- **MLP 架构**：4 层 MLP，宽度 64，远小于拼接基线的 7 层宽度 128 网络。
- **训练策略**：三阶段训练，前两轮使用颜色损失 + 掩膜损失（λ₁=λ₂=1, λ₃=0），第 2-7 轮仅用颜色损失，后续引入 LPIPS 感知损失。
- **训练时间**：10-20 分钟可完成单目视频的模型构建。

![[assets/figures/papers/paper_list_l82_https_ustc3dv_github_io_NeRFBlendShape/figures/004_Table_1.jpg]]
*Table 1: The parameters of hash table*

## 定位与知识库关联

**NeRFBlendShape** 的核心定位是：在单目视频驱动的动态头部 NeRF 建模任务中，将表达系数的注入方式从“特征拼接”改为“隐式线性混合多级体素场”，从而将训练时间从数小时级压缩至 10–20 分钟，同时保留照片级真实感的个性化细节。这一改变触及的是 **表达条件机制（expression conditioning mechanism）** 这一关键 slot。

具体而言，现有基于 NeRF 的动态面部/头部方法（如 **NerFACE** (Gafni et al., 2021) 以及本文自建的 concatenate baseline）的做法是：将表达系数通过一个小 MLP 映射后，与采样点的哈希编码直接拼接，然后送入一个较深的 MLP（baseline 使用 7 层密度 MLP + 1 层颜色 MLP，宽度 128）同时解码密度和颜色。这种设计的瓶颈在于：MLP 必须自行学习表达信息与空间位置之间的复杂关联，而拼接操作并未提供任何归纳偏置来辅助这一学习过程。结果就是，MLP 需要大量的训练迭代才能收敛，且在训练早期对嘴巴、眼睛等动态区域几乎无法产生合理结果（Fig. 7 显示，baseline 和 NerFACE 在 20 分钟内无法获得 plausible 的结果）。

NeRFBlendShape 将这一 slot 替换为 **隐式混合形状（implicit blendshape）架构**：表达系数不再与特征拼接，而是在体素特征的潜在空间中线性组合多个具有语义意义的多级哈希表基（mean shape 基 $\mathbf{h}_0$ 加 $K$ 个表达位移基 $\mathbf{h}_i$），得到对应特定表达的哈希表 $\mathbf{h} = \mathbf{h}_0 + \sum w_i \mathbf{h}_i$。随后，仅需一个轻量级 MLP（4 层，宽度 64）即可将该哈希表的插值特征解码为密度和颜色。这种设计的因果机制在于：线性混合操作使得表达系数能够**全局地**修改所有空间位置的局部特征，使这些局部特征提前适应了 MLP 的输入分布，从而大幅降低了 MLP 的学习负担。这是本文最核心的因果旋钮（causal knob），直接解释了为何模型能在 5 分钟训练后即重建张嘴、闭眼等动态表情（Fig. 7），并在 20 分钟内达到高质量。

**知识库挂载点**：本工作应挂载到动态 NeRF 的条件注入机制这一知识节点上。与之并列的方法包括：
- **拼接注入**（concatenation-based conditioning）：NerFACE (Gafni et al., 2021)、AD-NeRF 等，将条件码与位置编码或中间特征拼接后送入 MLP。
- **特征调制注入**（modulation-based conditioning）：如 FiLM 层或 StyleGAN 风格的 AdaIN，通过缩放/偏移中间特征来注入条件。
- **变形场注入**（deformation-based conditioning）：如 NHA、HyperNeRF 等，通过显式或隐式变形场将观测空间映射到规范空间。

NeRFBlendShape 开辟了第四种路径：**在体素场层面对条件进行线性组合**，本质上是在输入特征层面（而非网络中间层）进行条件驱动的特征重组。这与 3DMM 在网格顶点空间的线性混合形状有概念上的类比，但操作对象从显式几何顶点变为隐式多级体素特征，从而天然具备处理头发、皱纹等个性化外观细节的能力。

**适用边界**：
1. **输入依赖**：方法依赖现成的面部跟踪器提取表达系数和头部姿态。跟踪误差会直接传导至模型质量（论文明确指出大误差会导致细节丢失）。
2. **表达外推**：当驱动系数偏离训练分布较远时，局部区域可能出现伪影。这表明隐式混合形状的线性外推能力有限，与网格混合形状面临类似的泛化边界问题。
3. **非刚性变形**：对于快速、剧烈的非刚性头发变形，当前框架缺乏显式的变形条件，可能产生伪影。这是隐式混合形状无法覆盖的动态效应。
4. **几何表面质量**：基于密度场的表示在提取几何表面时存在噪声，若追求高质量几何，需引入 SDF 类 NeRF 表示，但可能牺牲训练效率。

**后续启发**：
- 隐式线性混合架构可尝试推广到其他动态场景重建任务（如人体、动物），只需将表达系数替换为对应域的低维控制参数。
- 表达基的语义可解释性（Fig. 9 显示基与网格混合形状在语义上一致）意味着该方法有潜力与现有面部动画管线（如 blendshape-based rigging）直接对接，降低内容创作门槛。
- 针对表达外推伪影问题，可探索非线性混合策略或引入先验正则化来约束基的位移幅度。
- 针对几何质量问题，可将密度场替换为 SDF 表示（如 NeuS、VolSDF），同时保留隐式混合形状架构，在维持训练效率的前提下提升表面质量。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Reconstructing_Personalized_Semantic_Facial_NeRF_Models_From_Monocular_Video.pdf]]