---
title: "StyleBin: Stylizing Video by Example in Stereo"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/StyleBin_Stylizing_Video_by_Example_in_Stereo.pdf
project_link: null
code_link: null
aliases:
- StyleBin
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
core_operator: 基于引导通道的块合成框架中，引入视差适配的辅助通道（左右视图版本），在纹理、引导和时序等能量项中明确加入立体一致性约束，实现左右视图的联合优化与合成。
primary_logic: 通过从风格范本中选取并拼接块以保持风格元素的平面性，同时利用视差传播与视差引导的合成策略，使得左右视图在空间（视差）和时间上均保持一致，从而在立体显示中获得有语义意义且无闪烁的风格化视频。
claims:
- 本方法将单目目标视频转换为由原始风格关键帧无缝拼接块组成的一对风格化序列，确保风格元素的平面性。
- 用户研究中参与者立即注意到清晰的立体效果，无人报告不适或对场景深度理解产生困惑。
- 与 stylize-and-warp 和 warp-and-stylize 基线相比，本方法能更忠实地再现风格并实现更好的立体一致性。
- 立体视频风格化质量定性比较 上 风格保真度与立体一致性 = StyleBin
---

# StyleBin: Stylizing Video by Example in Stereo

> [!tip] 核心洞察
> 通过从风格范本中选取并拼接块以保持风格元素的平面性，同时利用视差传播与视差引导的合成策略，使得左右视图在空间（视差）和时间上均保持一致，从而在立体显示中获得有语义意义且无闪烁的风格化视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | StyleBin：基于示例的立体视频风格化 |
| 英文题名 | StyleBin: Stylizing Video by Example in Stereo |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://dcgi.fel.cvut.cz/home/sykorad/stylebin) |
| Topic | #topic/vision_multimodal_applications |
| Method | StyleBin |
| Dataset | 用户研究（8名参与者） |

> [!tip] 效果简介
> - 立体视频风格化质量定性比较 上，风格保真度与立体一致性 StyleBin vs stylize-and-warp / warp-and-stylize (本方法更忠实地保留笔触和平面结构，立体伪影更少)。
> - 用户研究（8名参与者） 上，立体感感知与观看舒适度 StyleBin vs N/A (所有参与者立即感受到立体效果，无人报告不适或3D理解困难)。

## 概要

**问题瓶颈**：现有神经风格迁移方法在将艺术风格范本中的笔触、画布纹理等平面结构转移到视频时，难以同时保持风格元素的几何保真度与双目视差一致的立体效果——单目风格化后直接做视差变形（stylize-and-warp）或先变形再分别风格化（warp-and-stylize）都会引入立体伪影和风格失真。

**方法**：StyleBin 将立体视频风格化建模为一个联合优化问题。以**Jamriška et al. 2019**的单目引导块合成框架为基础，引入视差适配的辅助通道（光流、颜色、边缘、位置）的左右视图版本，并在纹理、引导和时序等能量项中显式加入立体一致性约束，使得左右视图在空间（视差）和时间上均保持一致。核心思路是从风格范本中选取并拼接块以保持风格元素的平面性，同时利用视差传播与视差引导的合成策略处理去遮挡区域。

**主要结果**：与 stylize-and-warp 和 warp-and-stylize 基线相比，StyleBin 更忠实地再现了风格范本的笔触和平面结构，立体伪影更少。8 名参与者的用户研究表明，所有参与者立即感受到清晰的立体效果，无人报告不适或对场景深度理解产生困惑。

**定位**：本方法将单目引导块合成框架的合成输出从单目视频扩展为具有立体一致性的左右视图序列，核心改动在于辅助通道的视差移位与补全，以及在块差异度量中引入视差调整后的跨视图一致性项。

## 核心方法与创新机理

### 问题瓶颈与核心思路

现有神经风格迁移方法在将艺术风格应用到视频时，面临一个根本性困境：要保持风格范本中笔触、画布纹理等平面结构的几何保真度，就难以同时生成双目视差一致的立体视频。因为风格化过程往往会破坏场景的深度线索，导致左右眼视图在空间上不一致，产生闪烁或深度感知混乱。StyleBin 的核心洞察是：**通过从风格范本中选取并拼接块（patch），保持风格元素的平面性；同时利用视差传播与视差引导的合成策略，使左右视图在空间（视差）和时间上均保持一致**，从而在立体显示中获得有语义意义且无闪烁的风格化视频。

### 基础框架与变更槽位

StyleBin 建立在 **Jamriška et al. 2019** 的单目视频引导块合成框架之上。该方法将目标视频转换为由风格关键帧中无缝拼接块组成的序列，通过最小化纹理、颜色、边缘、位置等引导通道的差异来选择最优源块。StyleBin 在此基础上进行了三个关键槽位的变更：

1. **合成输出**：从单目风格化视频扩展为具有立体和时间一致性的左右视图风格化序列 $O^L$ 和 $O^R$。
2. **辅助通道**：原有的光流 $F$ 和引导通道 $G$（颜色、边缘、位置）根据视差 $D$ 移位至左眼版本 $C^L$ 和右眼版本 $C^R$，并利用视差引导的块合成填补去遮挡区域。
3. **纹理相似项**：在块差异度量中增加立体一致性项，对比当前视图像素与另一视图经视差调整后的像素，确保左右视图风格一致。

### 方法流水线与模块因果关系

StyleBin 的完整流水线包含四个顺序模块，模块间存在明确的因果依赖：

**模块1：视差传播（Disparity Propagation）**
用户为关键帧 $T_k$ 提供视差图 $D_k$（可通过深度估计或手工标注获得）。StyleBin 将 $D_k$ 作为“风格范本”，利用 Jamriška et al. 2019 的引导块合成框架，以目标帧的辅助通道为引导，将视差信息传播至整个序列的所有帧，生成与每帧对齐的视差图序列 $D$。这一步骤是整个立体合成的基础，后续所有视差相关的移位和一致性约束都依赖于此。

**模块2：辅助通道生成与视差移位（Auxiliary Channel Generation and Disparity Shifting）**
为每帧生成辅助通道集合 $C = \{F, G_{\text{color}}, G_{\text{edge}}, G_{\text{pos}}\}$，其中：
- $F$ 为相邻帧间的光流
- $G_{\text{color}}$ 为帧的颜色信息
- $G_{\text{edge}}$ 通过 $G_{\text{edge}}(T_i) = T_i - N_\sigma \circ T_i$ 计算，即帧减去高斯滤波后的帧，提取边缘特征
- $G_{\text{pos}}$ 为像素位置编码

随后，根据视差 $D$ 将这些通道分别移位至左眼 $C^L$ 和右眼 $C^R$ 版本。视差移位导致部分区域因前景移动而暴露原本被遮挡的背景（去遮挡区域），这些区域在移位后的通道中表现为空洞。

**模块3：去遮挡填补（Disocclusion Filling）**
利用视差引导的块合成填补移位后产生的空洞区域。该步骤最小化能量函数 $E_D$：

$$E_D(C^S, C^V) = \sum_{\hat{t} \in C^V} \min_{\hat{s} \in C^S} Q(\hat{s}, \hat{t})$$

其中 $C^S$ 为原始单目通道（源），$C^V$ 为移位后的辅助通道（目标）。块差异度量 $Q$ 定义为：

$$Q(\hat{s}, \hat{t}) = \sum_{s \in \hat{s}, t \in \hat{t}} w_{\text{dis}} |D^S(s) - D^V(t)|^2 + w_{\text{val}}(s,t) |C^S(s) - C^V(t)|^2 + w_{\text{uni}} \Omega(s)$$

该度量组合了三项：
- **视差差异项**：确保填补块的深度与周围区域一致
- **通道值差异项**：保证填补内容的视觉连续性，其权重 $w_{\text{val}}$ 为视差依赖函数：

$$w_{\text{val}}(s,t) = \exp(-|D^S(s) - D^V(t)|^2 / \sigma^2)$$

该权重在视差连续处鼓励平滑过渡，在视差不连续处（如物体边界）允许突变，从而保持深度边缘的锐利度。
- **出现频次惩罚项** $\Omega(s)$：避免重复使用同一源块

**模块4：最终立体合成（Final Stereo Synthesis）**
在获得完整的左右视图辅助通道后，StyleBin 联合优化左右视图的风格化输出，最小化能量 $E_S$：

$$E_S(S_k, O_i^L, O_i^R) = \sum_{\hat{t}^L \in O_i^L} \min_{\hat{s}^L \in S_k} \mathcal{M}^L(\hat{s}^L, \hat{t}^L) + \sum_{\hat{t}^R \in O_i^R} \min_{\hat{s}^R \in S_k} \mathcal{M}^R(\hat{s}^R, \hat{t}^R)$$

其中综合块差异度量 $\mathcal{M}^V$ 加权组合了六个子项：

$$\mathcal{M}^V(\hat{s}, \hat{t}) = \sum_{s \in \hat{s}, t \in \hat{t}} w_{\text{tex}} M_{\text{tex}}^V(s,t) + w_{\text{color}} M_{\text{color}}^V(s,t) + w_{\text{pos}} M_{\text{pos}}^V(s,t) + w_{\text{edge}} M_{\text{edge}}^V(s,t) + w_{\text{temp}} M_{\text{temp}}^V(s,t) + w_{\text{uni}} \Omega(s)$$

**关键的立体一致性创新体现在纹理项和引导项中**。纹理与立体一致性项 $M_{\text{tex}}^V$ 定义为：

$$M_{\text{tex}}^V(s,t) = |S_k(s) - O_i^V(t)|^2 + w_{\text{stereo}} |S_k(s) - O_i^{-V}(t \pm D_i^V(t))|^2$$

第一项衡量风格范本 $S_k$ 与当前视图 $O_i^V$ 的纹理相似度（与单目方法相同）；第二项是新增的立体一致性约束：对比风格范本与另一视图 $O_i^{-V}$ 中经视差调整后的对应像素。这意味着当为左视图选择某个源块时，该块也必须与右视图中视差偏移后的内容一致，从而确保左右眼看到的是同一风格元素在空间中的正确位置。

引导项的立体一致性采用相同模式：

$$M_{\text{guide}}^V(s,t) = |G_k^S(s) - G_i^V(t)|^2 + w_{\text{stereo}} |G_k^S(s) - G_i^{-V}(t \pm D_i^V(t))|^2$$

时序一致性项 $M_{\text{temp}}^V$ 利用光流变形前一帧输出来保证时间连贯性：

$$M_{\text{temp}}^V(s,t) = |S_k(s) - F_i^V[O_{i-1}^V](t)|^2$$

### 推理路径与优化策略

StyleBin 的推理过程分为两个阶段：首先传播视差并完成辅助通道的移位与填补（模块1-3），然后进行最终的立体合成优化（模块4）。两个阶段的优化均采用 PatchMatch 算法加速最近邻检索，以降低计算开销。整个系统使用 C++ 实现。

### 方法创新机理总结

StyleBin 的核心创新在于将**平面风格保真**与**立体空间一致**这两个看似矛盾的目标统一在同一个块合成框架中。通过视差传播建立场景的深度基础，通过视差移位使辅助通道适配立体视角，通过在能量函数中显式加入立体一致性项，使得块选择过程同时考虑单视图风格匹配和跨视图空间一致性。这种设计避免了先风格化再变形（stylize-and-warp）可能破坏风格笔触的问题，也避免了先变形再风格化（warp-and-stylize）可能导致左右视图风格不一致的问题，从机制层面保证了风格元素的平面性在立体显示中得以保持。

![[assets/figures/papers/paper_list_l91_https_dcgi_fel_cvut_cz_home_sykorad_stylebin/figures/001_Figure_1.jpg]]
*Figure 1: An overview of the inputs and outputs of our method. The user provides a target sequence*

![[assets/figures/papers/paper_list_l91_https_dcgi_fel_cvut_cz_home_sykorad_stylebin/figures/004_Figure_4.jpg]]
*Figure 4: An overview of terms consisting of patch dissimilarity metrics*

## 实验与关键发现

### 主结果：风格保真度与立体一致性

StyleBin 在六个风格化序列上进行了定性评估（Figure 5 与 Figure 6），覆盖 Lili、Jana、Knights、Selfie、Lynx、Alchemist 等不同场景与风格范本。与两个基线策略——**stylize-and-warp**（先对单目视频风格化，再利用视差变形生成左右视图）和 **warp-and-stylize**（先将单目视频变形为左右视图，再分别风格化）——相比，StyleBin 在风格保真度与立体一致性两个维度上均表现出明显优势。论文明确指出：*“They clearly demonstrate that our approach reproduces the style more faithfully and achieves better stereo consistency.”*（补充材料中提供了与基线的并排比较视频，但正文未给出定量指标如 PSNR 或视差误差。）

![[assets/figures/papers/paper_list_l91_https_dcgi_fel_cvut_cz_home_sykorad_stylebin/figures/005_Figure_5.jpg]]
*Figure 5: A collection of three different sequences stylized using our approach—Lili Fig. 5.1, Jana Fig. 5.2, and Knights Fig. 5.3. From Lili’s and Jana’s input sequences (1d & 2d) a single keyframe was selected (1a & 2a) for which a stylized counterpart was prepared by an artist (1b & 2b) and also a depth map specified (1c & 2c). Our method then produced the final binocular sequences (1e & 2e) of which anaglyph examples are shown in (1f & 2f). In the case of Knights. the input sequence (3d) was already stylized by an artist, and the aim here is to add a stereoscopic effect (3e). To do that, our method propagates depth information (3b) from a set of keyframes (3a) to the entire sequence and synthesiz...*

![[assets/figures/papers/paper_list_l91_https_dcgi_fel_cvut_cz_home_sykorad_stylebin/figures/006_Figure_6.jpg]]
*Figure 6: StyleBin applied to three different sequences—Selfie Fig. 6.1, Lynx Fig. 6.2, and Alchemist Fig. 6.3. From Selfie’s and Lynx’s input sequences (1g & 2g) the user will pick two keyframes (1a, 1d, 2a, 2d), prepare their stylized variants (1b, 1e, 2b, 2e), and provide an estimate of depth in the scene*

**风格保真度**方面，stylize-and-warp 策略在视差变形阶段会扭曲风格范本中的笔触和画布纹理，导致风格元素的平面结构被拉伸或撕裂；warp-and-stylize 策略则因左右视图独立风格化而产生不一致的块选择，破坏了风格范本中笔触的连贯性。StyleBin 通过从原始风格关键帧中直接选取并拼接块，确保了风格元素的平面性——每一帧由风格范本中无缝拼接的块组成，而非对风格化结果进行后处理变形。

**立体一致性**方面，两个基线方法均无法在左右视图之间保持块选择的一致性：stylize-and-warp 的视差变形会在去遮挡区域产生模糊或重复纹理；warp-and-stylize 则因左右视图独立优化而产生视差冲突的块拼接。StyleBin 在纹理、引导和时序能量项中明确加入了立体一致性约束（$w_{\mathrm{stereo}}$ 项），使得左右视图在空间（视差）和时间上均保持一致。

### 用户研究：立体感知与观看舒适度

论文组织了一项小规模非正式用户研究，8 名参与者观看了 StyleBin 生成的立体风格化序列。结果具有启发性但缺乏统计意义：

- **立体感知**：所有参与者无需提示即立即注意到清晰的立体效果（*“Without prompting, they immediately noticed clear stereo effect”*），且在具有动态摄像机的序列中立体感更为生动。
- **观看舒适度**：无参与者报告不适或对场景深度理解产生困惑（*“no participants experienced discomfort or expressed concerns about their 3D interpretation of the scene”*），参与者普遍表示享受观看体验。
- **发现的问题**：两名参与者注意到与新暴露区域时间一致性相关的细微伪影，将其类比为“热浪引起的闪烁”（*“comparing them to a shimmer caused by heat”*）。这一反馈指向去遮挡区域在连续帧之间的块选择稳定性仍有改进空间。

### 关键消融：立体一致性约束的作用

虽然论文未提供形式化的消融实验表格，但从方法设计可以推断立体一致性项的核心作用。纹理项 $M_{\mathrm{tex}}^V$（Equation 6）和引导项 $M_{\mathrm{guide}}^V$（Equation 7）中均包含 $w_{\mathrm{stereo}}$ 加权的跨视图一致性项：

$$M _ { \mathrm { t e x } } ^ { V } ( s , t ) = | S _ { k } ( s ) - O _ { i } ^ { V } ( t ) | ^ { 2 } + w _ { \mathrm { s t e r e o } } | S _ { k } ( s ) - O _ { i } ^ { - V } ( t \pm D _ { i } ^ { V } ( t ) ) | ^ { 2 }$$

该设计使得块选择不仅考虑当前视图与风格范本的纹理相似度，还强制要求所选块在另一视图的视差对应位置上也保持纹理一致。若移除 $w_{\mathrm{stereo}}$ 项（退化为独立优化左右视图），将导致 warp-and-stylize 基线中观察到的视差不一致的块拼接。论文通过定性比较间接验证了该约束的必要性，但未提供消融的视觉对比。

### 失败模式与适用边界

**时间一致性伪影**：用户研究中发现的“热浪闪烁”效应揭示了方法的薄弱环节——当场景中存在大幅运动或旋转导致大面积去遮挡时，去遮挡填补（Section 3.3 的 $E_D$ 优化）在连续帧之间可能选择不同的源块，产生时间不连贯。这是因为去遮挡填补仅基于当前帧的辅助通道进行，缺乏显式的跨帧一致性约束。

**风格范本外推能力有限**：论文在讨论部分承认，方法假设风格范本能够覆盖目标序列中出现的所有视觉内容。当目标序列包含风格关键帧中未出现的显著新元素或大幅度视角变化时，块合成可能无法找到合适的源块，导致风格迁移质量下降。论文将“跨更剧烈变化和去遮挡的风格范本外推”列为未来工作方向。

**深度估计依赖**：方法需要用户为关键帧提供视差图 $D_k$，视差传播的质量直接影响最终立体合成的精度。论文指出深度估计本身是一个持续发展的研究领域，StyleBin 的效果会受益于该领域的进步。在深度边界不准确或传播误差累积的场景中，立体一致性可能退化。

**计算开销**：方法采用 PatchMatch 加速最近邻检索以降低 $E^D$ 和 $E^S$ 优化的计算开销，但论文未提供具体的运行时间数据。对于高分辨率视频或长序列，基于块的全局优化仍然可能构成实际应用中的性能瓶颈。

**测试场景有限**：所有实验均在人工制备的视频序列上进行（部分序列由艺术家预先风格化），未见真实世界多样性场景（如复杂光照变化、快速运动、非刚性变形）的广泛测试。方法的泛化能力需要更多验证。

## 定位与知识库关联

StyleBin 的核心定位是将**基于引导通道的块合成视频风格化**从单目视频扩展至立体视频。它所改变的“slot”非常明确：在 **Jamriška et al. 2019** 的单目引导块合成框架中，合成输出是一个风格化视频序列；StyleBin 将该输出槽位替换为**一对空间（视差）和时间上均一致的左右视图风格化序列**。为实现这一改变，辅助通道槽位从单目版本扩展为视差移位的左右视图版本，且在纹理、引导和时序等能量项中引入了立体一致性约束。

### 与基线的本质差异

相对于 **Jamriška et al. 2019** 的单目基础框架，StyleBin 的增量在于三个层面：

1. **视差传播模块**：将关键帧的视差图通过引导块合成传播至整个目标序列，为后续立体合成提供空间对应关系。
2. **辅助通道的视差移位与去遮挡填补**：对光流 $F$ 和引导通道 $G_{\mathrm{color}}、G_{\mathrm{edge}}、G_{\mathrm{pos}}$ 依据视差 $D$ 进行左右移位，并通过视差引导的块合成（最小化 $E_D$）填补去遮挡空洞，生成完整的左右视图辅助通道 $C^L$ 和 $C^R$。
3. **联合立体合成能量**：在最终合成能量 $E_S$ 中，块差异度量 $M^V$ 的纹理项和引导项均增加了立体一致性项（$w_{\mathrm{stereo}}$ 加权），强制当前视图的像素与另一视图经视差调整后的对应像素保持一致。

与两个朴素基线相比，差异更为根本：
- **stylize-and-warp**：先对单目视频风格化，再利用视差变形生成左右视图。该方法无法处理因视差移位产生的去遮挡区域，且风格化过程未考虑立体一致性，导致左右视图风格元素错位。
- **warp-and-stylize**：先将单目视频变形为左右视图，再分别风格化。该方法在两个视图上独立运行风格化，无法保证左右视图选择相同的风格范本块，导致立体伪影和风格不一致。

StyleBin 通过**在块选择阶段即嵌入立体一致性约束**，从根源上避免了这两种基线的问题。

### 知识库挂载点

StyleBin 可挂载在知识库的以下节点：

- **视频风格化 > 基于块合成的方法**：作为 **Jamriška et al. 2019**（引导块合成视频风格化）的立体扩展。核心继承关系是引导通道机制、PatchMatch 加速近邻检索、以及能量最小化框架；核心扩展是视差通道的引入和立体一致性项的设计。
- **立体视觉合成 > 基于视差的视图合成**：StyleBin 的视差传播和去遮挡填补模块与传统的基于视差的视图合成方法（如深度图像绘制，DIBR）共享问题设定，但其独特之处在于用**块合成而非像素插值**来填补去遮挡区域，且填补过程由视差引导而非纯纹理合成。
- **风格迁移 > 立体风格迁移**：作为该子领域的早期代表性工作之一，StyleBin 提出了“保持风格范本平面性”这一区别于神经风格迁移的设计原则——通过从风格范本中选取并拼接块，而非生成新像素，来保持笔触、画布纹理等平面结构的几何保真度。

### 适用边界与后续启发

**适用边界**：
- 方法假设风格范本和目标视频之间存在足够的块级对应关系；当目标视频中出现风格范本中不存在的语义内容或大面积去遮挡时，合成质量会下降（文中在讨论部分明确提到这一限制）。
- 依赖用户提供关键帧的视差图，视差图的质量直接影响最终立体效果；文中指出深度估计是该方法的瓶颈之一。
- 方法针对的是“由风格关键帧驱动的立体视频风格化”，而非通用的任意风格迁移。风格范本必须是目标视频关键帧的手绘或风格化版本，这限制了应用场景。
- 实验仅在人工制备的视频序列上进行，未见真实世界多样性场景的广泛测试；用户研究规模较小（8人），缺乏统计显著性。

**后续启发**：
- 视差传播模块可替换为更先进的深度估计或视差估计方法，直接提升立体合成质量。
- 去遮挡填补的能量函数 $E_D$ 和块差异度量 $Q$ 中视差依赖权重 $w_{\mathrm{val}}$ 的设计思路（在视差连续处鼓励平滑过渡，在视差不连续处允许突变）可推广至其他需要处理深度边缘的视图合成任务。
- 立体一致性项 $w_{\mathrm{stereo}}$ 的引入方式（在块匹配度量中直接比较另一视图的对应像素）是一种轻量级的立体约束设计，可被后续的神经立体风格化方法借鉴。
- 文中提到未来工作可尝试在更剧烈的视角变化和去遮挡情况下外推风格范本，这指向了将块合成与生成模型结合的方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/StyleBin_Stylizing_Video_by_Example_in_Stereo.pdf]]