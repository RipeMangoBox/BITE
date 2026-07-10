---
title: Domain Enhanced Arbitrary Image Style Transfer via Contrastive Learning
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Domain_Enhanced_Arbitrary_Image_Style_Transfer_via_Contrastive_Learning.pdf
project_link: "http://graphics.csie.ncku.edu.tw/deep_saliency"
code_link: null
aliases:
- DIMNCAMR
- DEAISTCL
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 重要性图的准确性和完整性：能否为每个像素提供可靠的能量值，使重定向操作能够优先保护重要物体。
primary_logic: 利用预训练的 VGG-16 网络提取多层特征，通过层融合策略拼接 conv3_3、conv4_3 和 conv5_3 的特征图，再经 1×1 卷积与 Sigmoid 激活生成类似掩膜的精细重要性图，从而更好地指导 seam carving 和 warping 方法。
claims:
- 不够准确的重要性图会导致重定向图像出现收缩，而正确的图能有效保持重要物体的形状。
- 所提重要性图在 seam carving 中避免了梯度图带来的严重失真。
- ARS 客观评分表明，79% 的测试图像中本方法优于对比方法，其余 21% 仍高于 0.8。
- 用 BASNet 显著性图替换本文重要性图会导致 seam carving 或 warping 结果失真。
---

# Domain Enhanced Arbitrary Image Style Transfer via Contrastive Learning

> [!tip] 核心洞察
> 利用预训练的 VGG-16 网络提取多层特征，通过层融合策略拼接 conv3_3、conv4_3 和 conv5_3 的特征图，再经 1×1 卷积与 Sigmoid 激活生成类似掩膜的精细重要性图，从而更好地指导 seam carving 和 warping 方法。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于深度重要性图的内容感知媒体重定向 |
| 英文题名 | Domain Enhanced Arbitrary Image Style Transfer via Contrastive Learning |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](http://graphics.csie.ncku.edu.tw/Tony/record_new.htm) · [Project](http://graphics.csie.ncku.edu.tw/deep_saliency) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | Deep Importance Map Network for Content-Aware Media Retargeting |
| Dataset | Image importance map generation |

> [!tip] 效果简介
> - Image importance map generation (1024×768 images) 上，计算时间 小于 1 秒 vs 约 45 秒 (Goferman et al. ) (加速 >45×)。
> - 自选图像重定向测试集 上，ARS 得分优胜比例 79% 的图像中 ARS 评分最高 vs 各种对比方法（seam carving, warping, 深度学习方法） (21% 非最高但仍 > 0.8)。

## 概要

传统内容感知媒体重定向方法依赖手工设计的梯度图或传统显著性图来估计像素重要性，但这些图往往无法充分描述重要区域的视觉信息，导致重定向图像出现严重失真或物体收缩。本文提出一种基于预训练 VGG‑16 网络的深度重要性图生成方法，通过融合 conv3_3、conv4_3 和 conv5_3 的多层特征，经 1×1 卷积与 Sigmoid 激活生成精细的重要性图，并将其嵌入 seam carving 和 patch‑based warping 两类重定向操作符中。实验表明，该方法在 1024×768 图像上生成重要性图仅需不到 1 秒，相比传统显著性方法（约 45 秒）加速超过 45 倍；在自选测试集上，79% 的图像 ARS 评分优于对比方法，其余 21% 仍高于 0.8。方法定位为重要性图估计模块的替换，不改动重定向操作符本身，可无缝接入现有重定向流水线。

## 核心方法与创新机理

### 问题瓶颈与核心思路

内容感知媒体重定向的核心挑战在于：如何为图像/视频的每个像素分配一个可靠的重要性值，使重定向操作能够优先保护重要物体，同时牺牲不重要的背景区域。传统方法在此环节存在根本性瓶颈——基于手工特征的梯度图（如 Avidan & Shamir, SIGGRAPH 2007）仅能捕获局部边缘强度，无法区分“重要物体的边缘”与“杂乱背景的边缘”；而传统显著性检测方法（如 Goferman et al., TPAMI 2011）虽能定位显著区域，却往往产生模糊的、边界不精确的热图，无法为像素级操作提供精细引导。如 Figure 6 所示，不够准确的重要性图会导致重定向图像出现严重收缩，而正确的图能有效保持重要物体的形状。

本文的核心洞察在于：**利用预训练深度网络的多层特征融合，生成类似掩膜的高精度重要性图**，从而从根本上提升重定向质量。该方法不改变下游重定向操作符的核心算法，而是替换其“能量/重要性估计”这一关键上游模块，形成一个即插即用的增强方案。

### 系统流水线与模块架构

整体系统由两个主要阶段构成（Figure 3）：第一阶段为“黑盒”式的视觉信息估计，通过所提深度网络生成重要性图；第二阶段为基于该重要性图的重定向操作，支持离散型 seam carving 和连续型 patch-based warping 两种算子。相比前续系统的流水线（Figure 3 黑色箭头），本文的关键改动在于将重要性图生成从手工设计模块替换为可学习的深度网络（红色箭头），同时在下游能量函数中移除了权重因子 α。

![[assets/figures/papers/paper_list_l26_http_graphics_csie_ncku_edu_tw_Tony_record_new_htm/figures/003_Figure_3.jpg]]
*Figure 3: The pipeline of our proposed retargeting system. The black arrow denotes the navigation procedure of the previous system. The red arrow is the navigation procedure of our media retargeting system*

### 第一阶段：深度重要性图网络

#### 特征提取（Truncated VGG-16）

网络骨干采用预训练的 VGG-16，但移除了全连接层和 soft-max 层，仅保留卷积与池化部分。VGG-16 的卷积层被组织为五个块（Figure 4），经过每次最大池化后，特征图的空间尺寸减半：

![[assets/figures/papers/paper_list_l26_http_graphics_csie_ncku_edu_tw_Tony_record_new_htm/figures/004_Figure_4.jpg]]
*Figure 4: The proposed network*

$$(W / 2^i \times H / 2^i \times c), \quad i = 0 \ldots 3$$

其中 $W$、$H$、$c$ 分别为宽度、高度和通道数。不同深度的特征图编码了不同尺度的视觉信息：浅层保留丰富的空间细节但语义模糊，深层具有强语义但空间分辨率低。

#### 层融合策略（Layer-Fusion）

本文的关键技术创新在于**选择性融合三个特定深度的特征图**：conv3_3（第3块末层）、conv4_3（第4块末层）和 conv5_3（第5块末层）。选择这三层的理由是：conv3_3 保留较完整的空间结构，conv5_3 提供高层语义理解，conv4_3 作为中间层起到语义与细节的桥接作用。

融合过程分为两步（Figure 5）：

![[assets/figures/papers/paper_list_l26_http_graphics_csie_ncku_edu_tw_Tony_record_new_htm/figures/005_Figure_5.jpg]]
*Figure 5: The illustration of the fusion process*

**步骤一：特征对齐与初步融合。** 由于不同层的特征图空间尺寸不同，需先进行上采样使尺寸统一，再通过 3×3 卷积（64 通道）进行通道对齐：

$$\hat{F}_i = f_2(F_i)$$

其中 $f_2(\cdot)$ 表示 3×3 卷积加批归一化和 ReLU。随后对相邻层进行拼接：

$$F_c = f_c(\hat{F}_i, \hat{F}_j)$$

具体地，conv5_3 与 conv4_3 拼接得到 $F_{c1}$，conv4_3 与 conv3_3 拼接得到 $F_{c2}$。这种“相邻层优先融合”的设计使得语义信息可以逐层向下传递，逐步细化空间精度。

**步骤二：全局融合与映射。** 对三个分支（$F_{c2}$、$F_{c1}$ 和单独处理的 $F_5$）分别应用 1×1 卷积进行通道压缩，然后再次拼接形成最终的特征张量：

$$F_T = f_1(F_{c2}) \otimes f_1(F_{c1}) \otimes f_1(F_5)$$

其中 $\otimes$ 表示沿通道维度的拼接操作，$f_1(\cdot)$ 为 1×1 卷积。最后，通过一个 1×1 卷积将融合张量映射为单通道，再经 Sigmoid 激活得到 [0,1] 范围的重要性图 $S_p$。

#### 训练损失与监督信号

网络训练使用二值交叉熵损失，以 MSRA 10K 数据集的物体掩膜作为 ground truth：

$$L(S_g, S_p) = -y_i \cdot \log(\hat{y}_i) + (1 - y_i) \cdot \log(1 - \hat{y}_i)$$

其中 $S_g$ 为 ground truth 掩膜，$S_p$ 为预测的重要性图，$y_i$ 和 $\hat{y}_i$ 分别为第 $i$ 个像素的真实标签和预测概率。该损失函数驱动网络输出接近二值掩膜的精细重要性图，而非传统显著性检测产生的模糊热图。

### 第二阶段：基于重要性图的重定向操作

#### Seam Carving 路径

对于离散型重定向，本文沿用 Avidan & Shamir 的 seam carving 框架，但将原始梯度能量图替换为网络生成的重要性图。在第 $i$ 次迭代中：

$$E_i = g(I_i)$$

其中 $g(\cdot)$ 为训练好的重要性图网络，$I_i$ 为当前迭代的图像。基于 $E_i$ 使用动态规划寻找累积能量最小的 seam 并移除。迭代次数由目标尺寸与原始尺寸的差值决定：

$$I_{rs} = \begin{cases} |h - h'|, & \text{if horizontal resizing} \\ |w - w'|, & \text{if vertical resizing} \end{cases}$$

传统 seam carving 使用的梯度能量图定义为：

$$E(I) = \left| \frac{\partial}{\partial x} I \right| + \left| \frac{\partial}{\partial y} I \right|$$

该能量仅响应局部梯度，无法区分物体内部高纹理区域与物体边缘。本文的重要性图则能直接标记整个重要物体区域为高能量，从根本上改变了 seam 的选取策略。

#### Patch-based Warping 路径

对于连续型重定向，本文基于 Lin et al.（TMM 2012, TVCG 2013）的 patch/mesh 变形框架，但做了两处关键修改。

**修改一：重要性图替换。** 将原方法使用的传统显著性图替换为网络生成的重要性图。每个图像块 $p_k$ 的能量定义为其内部 $m$ 个像素重要性值的平均值：

$$\omega_k = \frac{1}{m} \sum_{j=0}^{m} s_j$$

该能量直接驱动网格变形的优化目标——高能量 patch 倾向于保持刚性变换，低能量 patch 允许更大的缩放或变形。

**修改二：移除权重因子 α。** 原方法的总 patch 变换能量包含两项：相似变换能量 $D_{ST}$（保持形状）和线性变换能量 $D_{LT}$（允许缩放），通过权重因子 α 进行加权组合（Lin et al. Eq. 10）：

$$D_{TF}(P) = \sum_{k=1}^{np} \left(\alpha \times D_{ST}(patch_k) + (1-\alpha) \times D_{LT}(patch_k)\right)$$

类似地，视频网格能量（Lin et al. Eq. 11）也包含加权项。本文提出移除 α，改为直接求和：

$$E(P) = \sum_{k=1}^{n} \left(e_t(p_k) + e_s(p_k)\right)$$

$$E(M) = e_{lim}(p_k) + e_{lin}(p_k) + e_{ori}(p_k)$$

移除 α 的逻辑在于：当重要性图足够精确时，每个 patch 的重要性值 $\omega_k$ 已经自然地调节了各项能量的相对贡献——高重要性 patch 的刚性变换能量自然占主导，无需额外引入超参数进行人工平衡。Figure 9 的控制变量实验验证了这一点：使用原 Eq. 10 的结果（Figure 9-c）存在不自然的变形，而使用本文 Eq. 12 的结果（Figure 9-d）产生了更自然的物体形状保持。

### Changed Slots 总结

| 改动槽位 | 基线方案 | 本文方案 | 因果机制 |
|---------|---------|---------|---------|
| 重要性图估计 | 手工梯度图或传统显著性图 | VGG-16 多层特征融合 + 1×1 conv + Sigmoid | 多层融合同时捕获空间细节与语义信息，生成掩膜级精度的重要性图，从根本上避免重要区域被误切割或过度变形 |
| Patch 能量权重因子 α | 加权组合 α×D_ST + (1-α)×D_LT | 移除 α，直接求和 e_t + e_s | 精确的重要性图已通过像素级权重隐式调节各项能量的贡献，消除人工超参数使变形更自然 |

### 推理路径

整个系统的推理流程为：输入图像/视频帧 → 截断 VGG-16 提取 conv3_3、conv4_3、conv5_3 特征 → 上采样对齐 + 3×3 卷积处理 → 相邻层拼接（$F_{c1}$、$F_{c2}$）→ 1×1 卷积压缩 + 全局拼接（$F_T$）→ 1×1 卷积 + Sigmoid → 重要性图 $S_p$ → 送入 seam carving（迭代移除低能量 seam）或 patch-based warping（以 patch 平均能量驱动网格变形优化）→ 重定向结果。对于 1024×768 的输入，重要性图生成耗时小于 1 秒，相比传统方法（约 45 秒）加速超过 45 倍。

![[assets/figures/papers/paper_list_l26_http_graphics_csie_ncku_edu_tw_Tony_record_new_htm/figures/021_Figure_20.jpg]]
*Figure 20: Enlarging images to 25% of the width by our system. In each pair of images, the right image is enlarged from the left one*

![[assets/figures/papers/paper_list_l26_http_graphics_csie_ncku_edu_tw_Tony_record_new_htm/figures/023_Figure_23.jpg]]
*Figure 23: More results on different image attributes in our system. In each pair of images, the left image is original image of the retargeted result on the left*

## 实验与关键发现

### 重要性图生成效率对比

本文方法在重要性图生成速度上相较传统方法具有压倒性优势。对于 1024×768 分辨率的输入图像，所提网络生成一张重要性图的耗时小于 1 秒，而传统显著性检测方法（Goferman et al. ）需要约 45 秒，加速超过 45 倍。这一效率提升使得该方法在迭代式重定向操作（如 seam carving 需逐次移除接缝）中具备实际可用性。

### 消融实验：重要性图质量对重定向的决定性影响

**梯度图 vs. 本文重要性图（seam carving 场景）**

Figure 7 详细展示了梯度图与本文重要性图在 seam carving 中的本质差异。梯度图（Figure 7-a）仅反映像素强度的局部变化，导致接缝（seam）频繁穿过重要物体区域（Figure 7-b），重定向结果出现严重结构失真（Figure 7-c）。相比之下，本文重要性图（Figure 7-e）为前景物体赋予了高能量值，引导接缝避开关键区域（Figure 7-f），重定向图像（Figure 7-g）中重要物体的形状得以完好保留。该实验直接验证了“重要性图准确性是重定向质量的因果瓶颈”这一核心论断。

![[assets/figures/papers/paper_list_l26_http_graphics_csie_ncku_edu_tw_Tony_record_new_htm/figures/007_Figure_7.jpg]]
*Figure 7: Illustrates the difference between our importance map and the gradient map in seam removal. (a) gradient map, (b) the three seams are removed, (c) retargeted result with the energy map (a). (d) visualization of pixel energy in the red rectangle in (a). The dark brown represents for high energy pixel. From left to right: energy map, the removed seams (red strokes), after removing seams. (e) our importance map, (f) the three seams are removed, (g) retargeted result with the energy map (e)*

**传统显著性图 vs. 本文重要性图（warping 场景）**

Figure 6 的对比表明，使用传统显著性图（Goferman et al. ）作为能量引导时，重定向图像出现明显的物体收缩现象（Figure 6-a1）；而替换为本文重要性图后，重要物体的形状得到显著更好的保持（Figure 6-a2）。Figure 8 进一步从网格变形角度揭示了原因：传统显著性热图（Figure 8-a1）在关键区域的信息分布不够精确，导致网格顶点预测坐标偏离理想位置（Figure 8-b1）；本文重要性图（Figure 8-a2）则提供了更可靠的空间约束，使顶点变形更合理（Figure 8-b2）。

**BASNet 显著性图替换实验**

为验证本文重要性图并非简单的显著性检测可替代，作者将重要性图替换为现代显著性检测方法 BASNet（Qin et al., CVPR 2019）的输出。Figure 21 显示，使用 BASNet 显著性图作为能量图时，seam carving 操作符下的重定向图像出现严重失真，warping 方法则产生不一致的变形。这表明本文网络学习到的“重要性”概念超越了显著性检测的范畴——它不仅关注物体是否显著，更关注像素在重定向操作中的“可移除性”与“保护优先级”。

**能量公式中权重因子 α 的消融**

原 patch-based warping 方法（Lin et al. ）的总能量公式为加权组合 $D_{TF}(P) = \sum_{k=1}^{np} (\alpha \times D_{ST}(patch_k) + (1-\alpha) \times D_{LT}(patch_k))$，其中 α 为手动设定的权重因子。本文将其修改为直接求和 $E(P) = \sum_{k=1}^{n} (e_{t}(p_k) + e_{s}(p_k))$（Eq.12）。Figure 9 的控制变量实验表明：移除 α 并使用本文修改能量函数后，变形结果更自然，物体形状保持更好。这一消融说明，当重要性图足够可靠时，复杂的加权机制反而成为冗余——高质量的重要性图本身就隐含了合理的能量分配。

### 主客观综合评估

**ARS 客观评分**

Figure 12 展示了基于 ARS（Aspect Ratio Similarity）指标的定量评估结果。在测试集中，79% 的图像上本文方法取得了最高 ARS 分数；即使在其余 21% 非最优的图像上，ARS 值仍高于 0.8。这一结果表明本文方法在保持重要物体宽高比方面具有稳健优势。但需注意，该评估未使用公开的统一重定向基准数据集，且未报告具体 ARS 数值和统计显著性检验，结论的普适性需要手动验证。

**与各类基线的定性对比**

本文在多个维度与代表性方法进行了系统对比：

- **离散型重定向（seam carving）**：Figure 13 和 Figure 16 显示，本文方法相较 Avidan & Shamir（SIGGRAPH 2007）的梯度图 seam carving 和 Song et al. （CarvingNet, IEEE Access 2018）的编码器-解码器能量图方法，在保护重要物体结构方面均有明显改善。
- **连续型重定向（warping）**：Figure 14 对比了 Lin et al. （IEEE TMM 2012）的 patch-based warping，本文结果在物体形状自然度上更优。
- **深度重定向方法**：Figure 17 与 Tan et al. （Cycle-IR, IEEE TMM 2019）的比较表明，本文即使在仅替换重要性图而未改动重定向操作符的情况下，仍能产生更具竞争力的结果。Figure 18 与 Ahmadi et al. （利用语义分割的显著性重定向方法）的对比也显示出本文方法的优势。
- **视频重定向**：Figure 11 和 Figure 15 展示了视频帧的对比结果，本文系统相较 Lin et al. （IEEE TVCG 2013）在视频帧间一致性和物体保护方面表现更好。

### 失败案例与适用边界

**seam carving 的根本局限**

Figure 22 展示了本文方法的典型失败案例。在宽度缩减 50% 的极端条件下，即使使用本文重要性图，seam carving 操作符仍无法避免部分重要区域被切割。这是因为 seam carving 的离散移除机制存在根本性局限：当目标尺寸缩减过大时，接缝必然穿过某些高能量区域。此时切换到 warping 方法（Figure 22-d）可获得更好的结果。该失败模式并非本文重要性图的缺陷，而是 seam carving 操作符本身的固有边界。

**训练数据的泛化限制**

本文重要性图网络在 MSRA 10K 数据集上训练，该数据集主要包含显著物体，可能限制了对复杂场景（如多物体交错、纹理丰富背景）的泛化能力。作者指出，在某些图像上重要性图不够理想，进而影响了 seam carving 的表现。Figure 23 展示了在“难重定向”图像上的结果，虽然系统仍能保持重要物体形状，但部分细节区域存在可感知的变形。

**实时性与可复现性边界**

尽管重要性图生成时间已压缩至 1 秒以内，但对于高分辨率视频的实时处理仍存在挑战。此外，本文未公开代码和预训练模型，第三方复现困难，限制了方法的实际应用与后续改进。

## 定位与知识库关联

本工作的核心贡献在于**替换了内容感知媒体重定向流程中的“重要性图估计”这一关键模块**，而非重新设计重定向操作符本身。在传统框架（Figure 2）中，重要性图作为重定向操作的能量引导，直接决定了哪些区域被保护、哪些区域被压缩或移除。先前方法在此模块上依赖手工设计的梯度图（**Avidan and Shamir**, ACM SIGGRAPH 2007）或传统显著性检测算法（如 **Goferman et al.**, IEEE TPAMI 2011 的 context-aware saliency ），这些方法缺乏对语义完整性的深层理解，导致重定向结果出现重要物体收缩、接缝切割关键区域等问题。

具体而言，本方法在以下两个 **slot** 上做出了改变：

**Slot 1 — 重要性图生成方法**：将手工设计的梯度图或传统显著性图替换为基于预训练 VGG‑16 的多尺度特征融合网络。该网络通过拼接 conv3_3、conv4_3 和 conv5_3 的特征图（层融合策略），并经由 1×1 卷积与 Sigmoid 激活生成像素级重要性概率图。这一替换的本质是将重要性估计从“底层梯度响应”或“启发式显著性先验”提升为“深层语义特征驱动的掩膜预测”。

**Slot 2 — Patch 变形能量公式中的权重因子**：在 **Lin et al.** (IEEE TMM 2012) 的图像重定向和 **Lin et al.** (IEEE TVCG 2013) 的视频重定向方法中，patch 总能量由刚性变换项和线性缩放项的加权组合构成（含权重因子 α）。本文直接移除了 α，将两项能量简单求和（图像 Eq. 12: $E(P) = \sum_{k=1}^{n} (e_{t}(p_k) + e_{s}(p_k))$；视频 Eq. 13: $E(M) = e_{lim}(p_k) + e_{lin}(p_k) + e_{ori}(p_k)$）。这一修改的因果逻辑在于：当重要性图足够准确时，无需通过权重因子来平衡不同变换类型，直接求和即可获得更自然的变形结果（Figure 9 提供了控制变量证据）。

**与知识库中已有工作的本质差异**：
- 相对于 **Avidan and Shamir** (2007) 的梯度图 seam carving，本方法将能量图的语义感知能力从边缘响应扩展到物体级完整性感知，避免了 seam 穿过重要物体（Figure 7）。
- 相对于 **Lin et al.** (2012, 2013) 的 patch-based warping，本方法不仅替换了重要性图来源（从 的传统显著性到深度重要性图），还简化了能量公式，使系统在两个 slot 上同时获得改进。
- 相对于 **CarvingNet** (**Song et al.**, IEEE Access 2018) 的编码器-解码器能量图生成，本方法采用预训练 VGG‑16 特征融合而非端到端训练专用网络，训练成本更低（仅需微调融合层和 1×1 卷积），且可同时服务于 seam carving 和 warping 两种操作符。
- 相对于 **Cycle-IR** (**Tan et al.**, IEEE TMM 2019) 的循环式端到端重定向，本方法保持了两阶段架构（重要性估计 + 传统操作符），未触及重定向操作符本身的学习，因此保留了离散型操作（seam carving）的可解释性和连续型操作（warping）的数学稳定性。
- 相对于 **BASNet** (**Qin et al.**, CVPR 2019) 等现代显著性检测方法，本文明确指出直接使用显著性图替代重要性图会导致 seam carving 失真或 warping 不一致变形（Figure 21），说明“显著性”与“重定向所需的重要性”之间存在语义鸿沟——前者关注视觉注意力焦点，后者还需考虑背景结构的可压缩性。

**适用边界与局限**：
- 训练数据依赖 MSRA 10K 数据集，该数据集主要包含显著物体，因此重要性图在复杂场景（多物体、纹理背景、非显著结构）上的泛化能力受限，这是导致部分失败案例（Figure 22）的根本原因。
- 本方法未解决 seam carving 操作符的结构性缺陷：当图像宽度缩减 50% 时，即使重要性图正确，seam 仍可能被迫穿过包含重要区域的路径（Figure 22-c），此时 warping 方法表现更好（Figure 22-d）。这说明 slot 1 的改进无法弥补 slot 2（操作符选择）的不当。
- 计算效率方面，1024×768 输入的重要性图生成时间小于 1 秒（对比 的约 45 秒），但全分辨率视频的实时处理仍存在挑战。

**后续启发与知识库挂载点**：
- 本工作可作为“重要性图”模块的即插即用替代方案，挂载到任何依赖像素级能量引导的重定向框架中（seam carving、warping、甚至 cropping 和 scaling 的混合方法）。
- 开放问题“能否设计端到端的深度学习重定向操作符”指向一个更根本的方向：将两个 slot（重要性估计和重定向操作）联合优化，而非分阶段替换。这需要解决离散操作（seam removal）的可微性问题。
- 扩展到立体图像、360° 图像或交互式重定向场景时，重要性图的定义需从 2D 像素能量扩展到几何一致性约束，这是本方法尚未触及的边界。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Domain_Enhanced_Arbitrary_Image_Style_Transfer_via_Contrastive_Learning.pdf]]