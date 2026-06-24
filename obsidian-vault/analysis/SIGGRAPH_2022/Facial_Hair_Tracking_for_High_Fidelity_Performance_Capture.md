---
title: Facial Hair Tracking for High Fidelity Performance Capture
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Facial_Hair_Tracking_for_High_Fidelity_Performance_Capture.pdf
project_link: "https://studios.disneyresearch.com/2022/07/24/facial-hair-tracking-for-high-fidelity-performance-capture/"
code_link: null
aliases:
- DFHCP
- FHTHFPC
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 提出了一种交替优化面部皮肤与毛发重建的流程：首先从多帧中性旋转视频累积构建稠密参考发型，然后利用光流与空间正则化进行刚性发型跟踪，最后通过非刚性时空细化与拉普拉斯变形约束，联合迭代优化皮肤和毛发的形状，实现动态面部毛发与底层皮肤的联合高保真捕捉。
primary_logic: 通过将静态面部毛发重建方法（Beeler et al. 2012）扩展到时间域，并耦合皮肤和毛发跟踪，利用累积多帧中性表情的多视角信息来构建高质量的参考发型，从而实现对复杂表演中面部毛发和底层皮肤的联合高保真捕捉。
claims:
- 首次提出能够同时重建与跟踪密集三维面部毛发以及底层皮肤表面的表演捕捉管线。
- 通过注册多帧准刚性运动下的稀疏毛发重建，获得高质量的中性三维参考发型。
- 参考发型在整个表演的动作序列中被跟踪，其变形用于约束下方皮肤表面的跟踪。
- 发型跟踪阶段移除ICP项，仅依赖光流和空间正则化，以避免逐帧重建噪声。
---

# Facial Hair Tracking for High Fidelity Performance Capture

> [!tip] 核心洞察
> 通过将静态面部毛发重建方法（Beeler et al. 2012）扩展到时间域，并耦合皮肤和毛发跟踪，利用累积多帧中性表情的多视角信息来构建高质量的参考发型，从而实现对复杂表演中面部毛发和底层皮肤的联合高保真捕捉。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向高保真表演捕捉的面部毛发跟踪 |
| 英文题名 | Facial Hair Tracking for High Fidelity Performance Capture |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://studios.disneyresearch.com/2022/07/24/facial-hair-tracking-for-high-fidelity-performance-capture/) |
| Topic | #topic/other_unclear |
| Method | Dynamic Facial Hair Capture Pipeline |
| Dataset | 面部表演序列（2位演员，多种胡须风格） |

> [!tip] 效果简介
> - 面部表演序列（2位演员，多种胡须风格） 上，定性视觉质量（毛发密度、时间一致性、皮肤还原度） 稠密跟踪的三维面部毛发与动态无毛发皮肤表面 vs Beeler et al. 2012（静态稀疏毛发与皮肤重建） (首次实现动态面部毛发跟踪，毛发密度显著提高，皮肤表面更合理)。
> - 参考发型密度比较 上，定性密度与逼真度 多帧累积构建的稠密参考发型 vs 单帧静态重建（Beeler et al. 2012） (更稠密、更忠实于真实发型)。

## 概要

现有面部表演捕捉管线依赖多视角立体匹配，但在胡须、眉毛等面部毛发区域会产生收缩包裹伪影，无法正确重建底层皮肤表面，迫使演员在捕捉前剃须，牺牲角色外观真实性与制作灵活性。本文提出首个动态面部毛发跟踪管线，在完整表演序列中同时重建稠密三维面部毛发及其下方皮肤表面。核心思路是将静态毛发重建方法（Beeler et al., SIGGRAPH 2012）扩展至时间域：先从中性头部旋转视频累积多帧稀疏毛发重建，经 ICP 与光流联合对齐构建高质量稠密参考发型；再通过光流驱动与邻域正则化的刚性跟踪，配合非刚性时空细化，实现参考发型在表情变化序列中的稳定跟踪；最后以跟踪毛发约束皮肤网格的拉普拉斯变形，交替优化毛发与皮肤形状。实验表明，该方法首次获得动态稠密面部毛发重建，毛发密度与时间一致性显著优于静态基线，皮肤表面估计更加合理，并支持艺术编辑的时序传播。方法依赖14相机多视角设置与均匀光照，对极长胡须或与肤色接近的毛发仍有局限。

## 核心方法与创新机理

### 问题瓶颈与设计动机

现有高保真面部表演捕捉管线（如基于多视角立体的方法）在处理面部毛发区域时遭遇系统性失败：多视角立体匹配算法难以可靠重建细小的毛发结构，导致重建的3D皮肤表面在胡须、眉毛等区域产生收缩包裹伪影（shrink-wrap artifacts）。这一瓶颈迫使演员在捕捉前必须剃须，不仅增加了制作成本和调度难度，更牺牲了角色外观的真实性。此外，现有方法缺乏对面部毛发的时间一致性重建与跟踪能力，无法在动态表演序列中维持毛发的几何连贯性。本文的核心挑战在于：如何同时重建并跟踪密集的三维面部毛发及其下方的皮肤表面，使得两者在整段表演中保持时空一致。

### 管线总体架构

本文提出了一种交替优化面部皮肤与毛发重建的双通道管线（Fig. 3），将动态面部毛发捕捉问题分解为两个耦合的子问题：**面部皮肤重建与跟踪**（上通道）和**面部毛发纤维重建与跟踪**（下通道）。两条通道的解在多个细化步骤中交替计算，通过毛发跟踪结果约束皮肤表面估计，形成闭环反馈。

![[assets/figures/papers/paper_list_l43_https_studios_disneyresearch_com_2022_07_24_facial_hair_tracking_for_hig/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed dynamic facial hair capture pipeline comprising two main stages: (top) facial skin reconstruction and tracking, and (bottom) facial hair reconstruction and tracking, whose solutions are coupled and computed in alternation, via multiple refinement steps (Section 3.??, as indicated)*

管线包含六个核心模块，按执行顺序为：

1. **多视角立体与稀疏毛发初始化**（§3.1）：对每一帧进行多视角立体重建获得原始面部网格，并利用Beeler et al. 2012的静态毛发重建方法生成逐帧稀疏毛发。
2. **无毛发参考网格生成**（§3.2）：识别并替换被毛发污染的皮肤区域，创建具有标准拓扑的无毛发中性参考网格。
3. **参考发型构建**（§3.4）：从多帧中性头部旋转视频中累积稀疏毛发重建，通过三维毛发注册算法构建稠密、高质量的参考发型。
4. **发型刚性跟踪**（§3.5）：利用预计算光流和空间正则化，对参考发型进行逐帧刚性变换跟踪。
5. **非刚性时空毛发细化**（§3.6）：对每根毛发点进行非刚性变形优化，引入多视角图像约束和时空平滑项。
6. **皮肤网格细化**（§3.7）：根据毛发跟踪对应关系计算稀疏目标点，通过拉普拉斯变形细化毛发下方皮肤表面。

### Changed Slot 1：参考发型构建方式

**Baseline**（Beeler et al. 2012）仅能从单帧静态图像重建稀疏的毛发几何，无法为动态跟踪提供足够稠密且高质量的参考。

**Proposed**：从演员中性表情下缓慢旋转头部的视频中，累积多帧稀疏毛发重建，通过三维毛发注册算法合并构建稠密参考发型。该注册算法求解如下优化问题（Eq. 1）：

$$\min_{\mathbf{t},\mathbf{q}} \lambda_I E_{ICP}(\mathbf{t},\mathbf{q}) + \lambda_f E_{flow}(\mathbf{t},\mathbf{q}) + \lambda_n E_{neigh}(\mathbf{t},\mathbf{q})$$

其中，每根毛发$i$由变换参数$(\mathbf{t}_i, \mathbf{q}_i)$（平移向量和四元数旋转）描述。三个能量项的作用分别为：

- **ICP能量**（Eq. 2）：$E_{ICP}(\mathbf{t},\mathbf{q}) = \sum_{(p_{ij}, p')} \| R(\mathbf{q}_i) p_{ij} + \mathbf{t}_i - p' \|^2$，通过最近点距离约束变换后的毛发点与参考发型点的几何对齐。
- **光流能量**（Eq. 3）：$E_{flow}(\mathbf{t},\mathbf{q}) = \sum_k \sum_{p_{ij}} \psi( \| Q_k ( R(\mathbf{q}_i) p_{ij} + \mathbf{t}_i ) - \hat{x}_{ijk} \|^2 ) V_k(p_{ij})$，利用预计算的光流将毛发点投影到参考帧，最小化重投影误差，其中$\psi$为Huber损失函数以增强对光流离群值的鲁棒性。
- **邻域正则能量**（Eq. 4）：$E_{neigh}(\mathbf{t},\mathbf{q}) = \sum_i \sum_{i' \in N_{ri}} W(i,i') \lambda_{trans} \| \mathbf{t}_i - \mathbf{t}_{i'} \|^2$，鼓励空间邻近的毛发具有相似的刚性变换，保持发型局部结构。

**因果机制**：ICP项提供几何对齐的全局约束，光流项提供图像空间的局部引导，邻域正则项防止因噪声导致的局部错位。消融实验（Fig. 13）证实，单独使用ICP或光流项均导致错误对位，三者联合才能实现高质量对齐。多帧累积策略使得参考发型比单帧静态重建更稠密、更忠实于真实发型（Fig. 15）。

### Changed Slot 2：发型时间跟踪

**Baseline**：Beeler et al. 2012仅支持静态重建，无时间跟踪能力。

**Proposed**：在表演序列中跟踪参考发型时，优化目标简化为（Eq. 5）：

$$\min_{\mathbf{t},\mathbf{q}} \lambda_f E_{flow}(\mathbf{t},\mathbf{q}) + \lambda_n E_{neigh}(\mathbf{t},\mathbf{q})$$

**关键设计决策**：跟踪阶段**移除ICP项**，仅依赖光流和空间正则化。原因是逐帧稀疏毛发重建（来自Beeler et al. 2012）存在噪声和不一致性，若引入ICP项会导致跟踪结果抖动（Section 4.2, supplemental video证实）。邻域正则项在此阶段尤为关键——消融实验（Fig. 14）表明，缺少该正则项时，光流误差会导致毛发飞离原始位置，破坏发型局部结构。

**从刚性到非刚性的细化路径**：刚性跟踪后，进一步进行非刚性时空毛发细化（§3.6），求解逐点变形优化（Eq. 6）：

$$\min_{\mathbf{p}} \sum_t \sum_i \lambda_H E_{HDF}(\mathbf{p}_i^t) + \lambda_P E_{pos}(\mathbf{p}_i^t) + \lambda_{len} E_{len}(\mathbf{p}_i^t) + \lambda_{lap} E_{lap}(\mathbf{p}_i^t) + \lambda_t E_{temp}(\mathbf{p}_i^t)$$

五个能量项的作用：
- **毛发距离场能量**（Eq. 7）：$E_{HDF}(\mathbf{p}_i^t) = \sum_k \sum_j \psi( \| \frac{1}{H_k^t(Q_k \mathbf{p}_{ij}^t) + \epsilon} - 1 \|_2^2 ) V_k(\mathbf{p}_{ij})$，促使毛发点移动至图像中检测到的毛发线条位置，通过倒数HDF值实现——当毛发点投影位于图像毛发线条上时，HDF值趋近于0，该项趋近于0。
- **位置保持项**$E_{pos}$：约束毛发点不过度偏离刚性跟踪结果。
- **长度保持项**$E_{len}$：维持毛发段的原始长度。
- **拉普拉斯光滑项**$E_{lap}$：保持毛发曲线的局部微分属性。
- **时间平滑项**：$E_{temp}(\mathbf{p}_i^t) = \sum_j \| \hat{T}_i^{t-1} \mathbf{p}_{ij}^{t-1} - 2 \hat{T}_i^t \mathbf{p}_{ij}^t + \hat{T}_i^{t+1} \mathbf{p}_{ij}^{t+1} \|_2^2$，基于二阶中心差分约束连续帧间毛发点的变形加速度，减少时间抖动。

Fig. 6展示了刚性跟踪（红色）与非刚性细化（青色）的对比，非刚性细化通过变形跟踪毛发几何显著改善了对输入图像的对齐。

### Changed Slot 3：毛发下方皮肤表面估计

**Baseline**（Beeler et al. 2012）：仅基于发根位置的简单推断，在长胡须情况下效果不佳。

**Proposed**：采用数据驱动的两阶段方法：
1. **无毛发参考网格生成**（§3.2）：利用多视角重建的表面置信度（通过归一化互相关评估光度一致性）识别毛发污染区域，使用PCA面部模型预测被遮挡的皮肤表面，并融合多视角几何信息得到具有标准拓扑的无毛发参考网格。该方法在长胡须情况下显著优于Beeler et al. 2012的表面估计方法。
2. **皮肤网格细化**（§3.7）：在表演跟踪过程中，根据毛发跟踪的帧间对应关系，在参考表面的毛发区域采样稀疏点集，为每个点计算局部变换，得到目标表面点，最后通过拉普拉斯变形（Sorkine et al. 2004）细化毛发下方皮肤表面（Fig. 7, Fig. 11）。

![[assets/figures/papers/paper_list_l43_https_studios_disneyresearch_com_2022_07_24_facial_hair_tracking_for_hig/figures/007_Figure_7.jpg]]
*Figure 7: We sample a sparse set of points in the facial hair region of the reference surface (cyan) and for each point, use the surrounding hair point correspondences between reference and frame ?? to find a local transformation ?? . We use ?? to get the target surface points (red) and apply Laplacian deformation [Sorkine et al. 2004] to arrive at the refined result on the right*

![[assets/figures/papers/paper_list_l43_https_studios_disneyresearch_com_2022_07_24_facial_hair_tracking_for_hig/figures/010_Figure_11.jpg]]
*Figure 11: Our per-frame face mesh refinement step corrects the initial surface estimate using the reconstructed facial hairs. Here we see 1 frame of correction, from left to right: one input image, initial surface estimate with reconstructed hairs, our refined surface with reconstructed hairs, difference between original and refined surface (blue: 0mm to red: 5mm). A zoom-in on the improvement is shown in the bottom row*

**因果链路**：毛发跟踪为皮肤细化提供了关键的对应关系约束——通过毛发在参考帧与当前帧之间的变形场，推断下方皮肤应有的变形，从而修正初始表面估计中的收缩包裹伪影。

### 模块间因果关系总结

整个管线的模块间存在强因果依赖：
- **模块1→模块3**：逐帧稀疏毛发重建是参考发型构建的输入源。
- **模块2→模块5→模块6**：无毛发参考网格为皮肤跟踪提供标准拓扑，毛发跟踪结果（模块4+5）为皮肤细化（模块6）提供变形约束。
- **模块3→模块4→模块5**：参考发型（模块3）是跟踪的初始状态，刚性跟踪（模块4）为非刚性细化（模块5）提供初始解。
- **模块5→模块6**：非刚性细化后的毛发几何为皮肤表面估计提供更准确的空间约束。

这种交替优化与闭环反馈机制，使得皮肤和毛发的重建相互促进，共同收敛到时空一致的解。

## 实验与关键发现

### 核心实验设置

本方法在基于 Riviere et al. (2020) 的标准面部表演捕捉系统上进行验证，该系统包含 14 台视频相机，其中 12 台组织为四个三相机组（每组含一个立体对），另有两台相机专门用于毛发捕捉（Fig. 2）。实验对象为两名具有不同胡须风格的演员，覆盖了从短须到较长胡须的多种面部毛发形态。评估方式以定性视觉质量为主，核心指标包括：三维毛发重建的密度与完整性、时间序列上的跟踪一致性、以及毛发下方皮肤表面的还原合理性。

![[assets/figures/papers/paper_list_l43_https_studios_disneyresearch_com_2022_07_24_facial_hair_tracking_for_hig/figures/002_Figure_2.jpg]]
*Figure 2: We adopt a standard setup for facial performance capture based on Riviere et al. [2020], with 14 video cameras organized into four triplets (each including a stereo pair) and two additional cameras for hair capture*

### 主要结果

**动态面部毛发跟踪能力**。本文首次实现了对密集三维面部毛发在整个表演序列中的跟踪，同时恢复底层皮肤表面。如 Fig. 8 和 Fig. 9 所示，对于两名演员在不同表情下的表演帧，方法能够稳定地重建并跟踪面部毛发（青色叠加显示），生成与输入图像高度一致的三维几何。这一能力是基线方法 **Beeler et al. (2012)** 所不具备的——后者仅能进行单帧静态重建，无法提供时间维度上的毛发对应关系。

**毛发密度与真实感的显著提升**。通过与 Beeler et al. (2012) 的直接对比（Fig. 15），本方法通过多帧中性头部旋转视频累积构建的参考发型，在密度和忠实度上均显著优于单帧静态重建结果。Fig. 15（底部）清晰展示了这一差异：多帧注册合并后的参考发型更加稠密，更接近真实发型的外观。这一提升的因果机制在于：单帧重建受限于特定视角下的可见毛发数量，而多帧累积利用头部旋转过程中的准刚性运动，将不同视角下重建的稀疏毛发对齐并合并，从而突破单帧信息瓶颈。

**皮肤表面细化的有效性**。Fig. 11 展示了逐帧皮肤网格细化步骤的效果。在初始表面估计中，毛发区域的皮肤呈现收缩包裹伪影（shrink-wrap artifacts），而经过本文提出的拉普拉斯变形细化后，皮肤表面被修正到更合理的位置。从差异热力图（蓝色 0mm 至红色 5mm）可见，校正幅度可达数毫米，尤其在较长胡须区域更为显著。这一结果验证了利用重建毛发作为约束来恢复被遮挡皮肤表面的有效性。

### 关键消融实验

**参考发型构建中的能量项消融**（Fig. 13）。在三维毛发注册优化（Eq. 1）中，同时使用光流项 $E_{flow}$ 和 ICP 项 $E_{ICP}$ 是实现高质量对齐的关键。消融实验表明：单独使用光流项会导致毛发点漂移到错误位置，而单独使用 ICP 项则无法正确匹配不同帧间的对应毛发段。只有当两项联合使用时，三根示例毛发才能准确对齐到参考帧中的目标发型位置。这揭示了光流提供帧间对应先验、ICP 提供几何对齐约束的互补机制。

**刚性跟踪中邻域正则项的消融**（Fig. 14）。在表演序列的刚性发型跟踪优化（Eq. 5）中，添加邻域正则项 $E_{neigh}$ 对保持发型局部结构至关重要。消融显示：移除该正则项后，部分毛发因光流误差而“飞离”主体发型区域，产生不自然的断裂和错位；而加入正则项后，邻近毛发共享相似的刚性变换，有效抑制了孤立点的异常运动，保持了发型的整体连贯性。

**跟踪阶段移除 ICP 项的决策依据**。与参考发型构建阶段不同，在表演序列跟踪优化（Eq. 5）中，方法有意移除了 ICP 约束，仅依赖光流项和空间正则项。这一设计决策基于一个关键观察：逐帧稀疏毛发重建（来自 Beeler et al. 2012）存在显著的帧间不一致性和噪声。若在跟踪优化中引入 ICP 项，这些噪声会直接传导至跟踪结果，导致毛发重建出现明显的帧间抖动。补充视频中的对比实验验证了这一现象。

### 与基线方法的系统对比

**与 Beeler et al. (2012) 的对比**（Fig. 15）。除密度提升外，本文方法在皮肤表面估计上也展现出优势。对于较长胡须的情况，Beeler et al. (2012) 的表面估计方法会产生明显的收缩包裹伪影，而本文提出的数据驱动无毛发参考网格创建方法（Section 3.2）——通过 PCA 面部模型预测被遮挡区域——能够生成更合理的皮肤表面。这一定性优势在 Fig. 15 的对比中清晰可见。

**与非刚性点云配准算法 BCPD (Hirose, 2021) 的对比**（Fig. 16）。本文将所提出的面部毛发跟踪方法与非刚性点注册通用算法 BCPD 进行了对比。结果表明，通用配准算法在处理面部毛发这类细长、稀疏且高度可变的结构时，难以保持毛发的拓扑一致性和局部几何特征，而本文专门设计的跟踪框架——结合光流引导、邻域正则化和非刚性时空细化——能够更好地保持毛发结构的完整性。

### 失败模式与适用边界

**股级别对齐精度有限**。尽管方法能够生成视觉上合理的密集毛发重建，但作者明确指出，重建的毛发在股（strand）级别上可能未完全对齐多视角图像，无法保证每一根发丝的精确还原。这意味着该方法适用于需要整体外观一致性的应用场景（如视觉特效），但在需要精确到单根毛发的物理模拟或医学应用中可能存在不足。

**极端长度毛发的未测试状态**。实验仅覆盖了中等长度的胡须，未在极长面部毛发（如长至胸口的胡须）上进行验证。极长胡须可能带来额外的挑战：毛发段的自遮挡更严重、运动模式更复杂、与皮肤的耦合关系更松散，现有方法中的刚性跟踪加非刚性细化的策略可能不足以处理此类情况。

**毛发—皮肤颜色相似性敏感**。方法依赖基于图像对比度的毛发检测与重建（继承自 Beeler et al. 2012），当毛发颜色与肤色过于接近时，多视角立体匹配和光流计算均面临挑战，可能导致毛发检测遗漏或重建质量下降。这是基于传统视觉特征的方法的共性局限。

**发根物理耦合缺失**。当前方法重建的毛发与底层皮肤表面在发根处并未建立物理连接，两者是独立优化后再通过约束关联的。这意味着毛发不会随皮肤拉伸而自然地改变发根位置，在极端表情下可能出现毛发“悬浮”于皮肤之上的不自然现象。

**多视角硬件依赖**。方法依赖 14 台相机的多视角设置和均匀光照条件，这限制了其在轻量级捕捉场景（如单目或双目设置）中的应用。同时，方法继承了 Beeler et al. (2012) 静态毛发重建模块对图像质量和多视角覆盖的要求。

**皮肤纹理恢复缺失**。当前方法仅恢复毛发下方皮肤的三维几何表面，未恢复被遮挡区域的皮肤纹理属性（如漫反射颜色、法线贴图、位移贴图等）。对于需要完整外观重建的应用（如数字角色创建），这需要额外的纹理补全步骤。

### 应用验证

**时间一致性编辑传播**（Fig. 12）。作为跟踪质量的一个间接验证，方法展示了艺术编辑的自动传播能力：由于重建的面部毛发具有时间一致的连接关系，用户对某一帧进行的编辑（如修剪胡须两侧）可以自动传播到整个序列。这一特性不仅验证了跟踪的稳定性，也展示了方法在视觉特效制作流程中的实用价值。

![[assets/figures/papers/paper_list_l43_https_studios_disneyresearch_com_2022_07_24_facial_hair_tracking_for_hig/figures/008_Figure_8.jpg]]
*Figure 8: Several frames of performance with 3D face and facial hair capture for two actors, showing the input images, hair overlay in cyan, and 3D geometry. ACM Trans. Graph., Vol. 41, No. 4, Article 165. Publication date: July 2022*

![[assets/figures/papers/paper_list_l43_https_studios_disneyresearch_com_2022_07_24_facial_hair_tracking_for_hig/figures/009_Figure_9.jpg]]
*Figure 9: Several frames of performance with 3D face and facial hair capture for two actors, showing the input images, hair overlay in cyan, and 3D geometry. ACM Trans. Graph., Vol. 41, No. 4, Article 165. Publication date: July 2022*

## 定位与知识库关联

本文的核心贡献在于将面部毛发重建从**静态单帧**推进到**动态表演全序列**的联合跟踪，改变的关键 slot 是：**时间维度上的毛发跟踪与皮肤—毛发耦合优化**。基线方法 **Beeler et al.** (ACM Trans. Graphics / SIGGRAPH 2012) 首次实现了从多视角图像中静态重建稀疏面部毛发与底层皮肤，但其输出是逐帧独立的，缺乏时间一致性，且毛发密度受限于单帧信息。本文在此基础上，通过三个关键改造实现了质的跃迁：

1. **参考发型构建方式**：从单帧静态重建改为多帧中性头部旋转视频的累积注册，利用 ICP、光流与邻域正则化的联合优化（Eq. 1–4），将稀疏的逐帧重建融合为稠密、高质量的参考发型。这一改造解决了单帧信息不足导致的毛发稀疏与不完整问题。

2. **时间跟踪能力**：引入了基于光流与空间正则化的刚性跟踪（Eq. 5）以及后续的非刚性时空细化（Eq. 6–7），使参考发型能够在整个表演序列中保持时间一致的变形。特别值得注意的是，跟踪阶段**移除了 ICP 项**——因为逐帧稀疏重建本身存在噪声和不一致性，引入 ICP 反而导致抖动。这一设计选择体现了对基线方法输出特性的深刻理解。

3. **皮肤—毛发耦合**：将毛发跟踪的对应关系反馈用于约束下方皮肤表面的拉普拉斯变形（Section 3.7），替代了 Beeler et al. 2012 中基于发根位置的简单推断。这使得被胡须遮挡的皮肤区域能够获得更合理的几何估计。

从知识库关联角度，本文可挂载于以下节点：

- **多视角面部表演捕捉**（如 **Riviere et al.** 2020 的采集设置）：本文沿用了 14 相机多视角系统，但将管线从仅跟踪面部皮肤扩展到了毛发—皮肤的联合跟踪。对于已有类似硬件设施的工作室，本文的方法可作为直接的功能扩展。

- **静态面部毛发重建**（**Beeler et al.** 2012）：本文是该工作的直接继承者，将其从静态快照提升为动态序列，同时改进了毛发密度和皮肤估计质量。后续研究若需处理动态毛发，本文提供了基础的时间跟踪框架。

- **非刚性点云配准**：本文在参考发型构建中使用了 **BCPD**（**Hirose**, IEEE TPAMI 2021）作为对比方法（Fig. 16），表明其毛发注册模块可与通用非刚性配准算法形成互补或替代关系。

**适用边界与局限**：

- 方法依赖 14 台相机的多视角设置和均匀光照，硬件门槛较高。对于更少相机或单目场景的适配尚未探索。
- 未在极长胡须（如长至胸口）上测试，且当毛发颜色与肤色过于接近时，基于图像对比度的毛发检测会失效。
- 重建的毛发在发根处未与皮肤表面建立物理连接，缺乏真实的耦合关系。
- 被毛发遮挡区域的皮肤纹理（颜色、法线等）未恢复，限制了在需要完整纹理贴图的应用中的使用。

**后续启发**：

- 本文的交替优化框架（皮肤跟踪 → 毛发跟踪 → 皮肤细化）为其他“遮挡物—被遮挡表面”联合重建问题提供了可借鉴的范式，例如衣物与人体、头发与头皮等。
- 时间一致性毛发跟踪带来的附加收益是**艺术编辑的自动传播**（Fig. 12）：由于毛发具有时间一致的拓扑连接，对单帧的编辑（如修剪胡须）可自动传播至整个序列，这对影视后期制作具有直接实用价值。
- 开放问题中，如何利用深度学习提高毛发检测的鲁棒性（尤其在低对比度区域）以及如何适配更轻量的采集设置，是向实用化推进的关键方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Facial_Hair_Tracking_for_High_Fidelity_Performance_Capture.pdf]]