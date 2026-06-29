---
title: Theory of Human Tetrachromatic Color Experience and Printing
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Theory_of_Human_Tetrachromatic_Color_Experience_and_Printing.pdf
project_link: null
code_link: null
aliases:
- ITICPP
- THTCEP
tags:
- SIGGRAPH_2024
- topic/graphics_fabrication_design
- topic/vision_multimodal_applications
core_operator: 利用n维物体颜色理论推导出理想的四色墨水套件（CVPY），并开发原型四色打印机，以制造三色视者无法区分的同色异谱颜色，从而在野外揭示四色视觉。
primary_logic: 将三色颜色理论推广到n维后，可计算出四色视者的色度球体和理想墨水反射函数；据此制作的四色打印系统能产生仅四色视者可分辨的颜色，使功能性四色视觉的筛查成为可能。
claims:
- 首次完整计算了四色视者的物体颜色固体、三维色度球体和二维色调球体（色相球面），预测了互补色keef和litz。
- 推导出理想的四色墨水套件CVPY（Cyan, Violet, Pink, Yellow），其反射函数能够覆盖完整的四色域（理想情况）。
- 原型四色打印机可以打印出色调球面上52%的点（254/486），而传统CMY打印机仅能打印一条一维线上的颜色。
- 制作的真实等色板经光谱测量验证，对三色视者同色异谱，但对假设的四色视者（第4锥体）有显著不同的反应，展示了筛查四色视者的可行性。
---

# Theory of Human Tetrachromatic Color Experience and Printing

> [!tip] 核心洞察
> 将三色颜色理论推广到n维后，可计算出四色视者的色度球体和理想墨水反射函数；据此制作的四色打印系统能产生仅四色视者可分辨的颜色，使功能性四色视觉的筛查成为可能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 人类四色视觉体验与打印理论 |
| 英文题名 | Theory of Human Tetrachromatic Color Experience and Printing |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://imjal.github.io/theory-of-tetrachromacy/) |
| Topic | #topic/graphics_fabrication_design #topic/vision_multimodal_applications |
| Method | Ideal Tetrachromatic Inkset (CVPY) and Prototype Printer |
| Dataset | Ideal Tetrachromatic Gamut, Tetrachromatic Hue Sphere Sampling, Q‑axis Gamut Width, Isochromatic Plate Visibility |

> [!tip] 效果简介
> - Ideal Tetrachromatic Gamut (volume) 上，fraction of ideal gamut volume 4.17% vs 0% (CMY cannot cover any tetrachromatic volume) (+4.17%)。
> - Tetrachromatic Hue Sphere Sampling (486 points) 上，percentage of points printable inside gamut 52% (254/486) vs ~0% (CMY only prints a line on the sphere) (+52%)。
> - Q‑axis Gamut Width 上，width of gamut along the Q cone axis relative to object color solid 29.9% vs 44% (CMY along L axis, for reference) (— (different axis))。

## 概要

超过50%的女性携带四色视觉基因，但因缺乏四色颜色环境与检测工具，功能性四色视者极少被识别。本文首次将n维物体颜色理论推广至人类四色视觉，完整计算了四色视者的物体颜色固体、三维色度球体与二维色调球面，预测了互补色keef和litz。在此基础上，推导出理想的四色墨水套件CVPY（Cyan, Violet, Pink, Yellow），并构建原型四色打印机。实验表明，该打印机可覆盖色调球面上52%的点（254/486），而传统CMY打印机仅能打印一维线上的颜色；制作的等色板经光谱验证对三色视者同色异谱，但对假设的四色视者Q锥体响应显著不同，首次展示了野外筛查四色视者的可行性。

## 核心方法与创新机理

### 问题瓶颈与理论突破口

本工作的核心瓶颈在于：尽管遗传学研究表明超过50%的女性携带四色视基因，但功能性四色视者极少被识别。根本原因有二：其一，环境中缺乏四色颜色（即三色视者无法区分的同色异谱色），使潜在的四色视者无从发现自身能力；其二，缺乏相应的检测工具和理论框架来描述四色视觉的色彩结构。传统色彩理论、印刷系统和色觉测试均建立在三色视觉（d=3）基础上，无法直接推广到四色（d=4）情形。

本文的突破在于将n维物体颜色理论系统性地应用于人类四色视觉，首次完整计算出四色视者的关键色彩结构，并据此推导出理想的四色墨水套件，制造原型打印机，最终产生仅四色视者可分辨的颜色，为在野外大规模筛查功能性四色视觉提供了理论基础和工程原型。

### 理论框架：从三色到四色的维度推广

#### 物体颜色固体与色度空间

论文首先建立了d维观察者的通用色彩理论框架。设观察者具有d种锥体光谱敏感度函数 $S_1(\lambda), \dots, S_d(\lambda)$，光谱轨迹定义为单色光在d维空间中的曲线：

$$\mathcal{L} = \{ (S_1(\lambda), \dots, S_d(\lambda)) \in \mathbb{R}^d \mid \lambda \in \Lambda \} \tag{1}$$

给定照明体 $I(\lambda)$ 和物体反射率 $R(\lambda)$，观察者的颜色响应为：

$$\vec{S}(R) = \left( \int_\Lambda S_1 I R \, d\lambda, \dots, \int_\Lambda S_d I R \, d\lambda \right) \tag{2}$$

物体颜色固体 $\mathcal{O}$ 定义为所有可能反射率（$0 \le R(\lambda) \le 1$）产生的颜色集合：

$$\mathcal{O} := \{ \vec{S}(R) \mid R \in \mathbb{L}^\infty, 0 \le R(\lambda) \le 1 \} \subset \mathbb{R}^d \tag{3}$$

对于三色视者（d=3），$\mathcal{O}$ 是一个三维凸体，其色度空间（归一化锥体响应比）为二维圆盘。对于四色视者（d=4），$\mathcal{O}$ 是四维凸体，色度空间变为三维球体——这是维度提升带来的根本性拓扑变化。

#### 边界生成与最优原色基

物体颜色固体的边界点由半平面割线生成。对于非零向量 $H \in \mathbb{R}^d$，定义反射函数：

$$R_H(\lambda) = \begin{cases} 1 & H \cdot \mathcal{L}(\lambda) > 0 \\ 0 & H \cdot \mathcal{L}(\lambda) < 0 \end{cases} \tag{Theorem 3.1}$$

该函数在光谱轨迹被半平面分割处发生0-1跳变，生成的 $\vec{S}(R_H)$ 即为 $\mathcal{O}$ 的边界点。遍历所有 $H$ 方向即可重建整个物体颜色固体。

在此基础上，论文推导了最优原色基（Max Basis）。对于d维观察者，需要d个原色反射函数来张成完整的颜色空间。最优原色基通过最大化d个分区反射向量所张平行多面体的体积来确定：

$$\lambda_1^*, \dots, \lambda_{d-1}^* := \underset{\lambda_1,\dots,\lambda_{d-1}}{\arg\max} \, \det\big( \mathcal{L} \cdot \mathrm{Part}(\lambda_1,\dots,\lambda_{d-1}) \big) \tag{11}$$

其中 $\mathrm{Part}(\lambda_1,\dots,\lambda_{d-1})$ 是在波长切点处将白色光谱划分为d个分区的矩阵。对于三色视者，最优切点产生经典的青（C）、品红（M）、黄（Y）原色；对于四色视者，最优切点产生青（Cyan）、紫（Violet）、粉（Pink）、黄（Yellow）四原色——即CVPY墨水套件。

### 核心创新：四色色彩结构的完整计算

#### 色调球体与互补色

三色视者的色调空间是一个圆环（hue circle），每个色调仅有两个邻居。四色视者的色调空间拓扑等价于球面 $S^2$，每个色调拥有一个圆形邻域的邻居（Fig. 6）。这一拓扑差异意味着四色视者具有更丰富的色彩体验：色调球面上存在互补色对keef和litz（类似于三色视觉中的红-绿、蓝-黄对立），但四色互补色是球面上的对跖点。

论文计算了四色物体颜色固体的Ostwald切片（Fig. 4），展示了色调球面上每个色调方向上的明度-饱和度截面。这些切片揭示了四色色彩空间的完整几何结构，为后续的色觉测试设计提供了理论基础。

![[assets/figures/papers/paper_list_l40_https_imjal_github_io_theory_of_tetrachromacy/figures/005_Figure_4.jpg]]
*Figure 4: Complementary Hue Slices of the Object Color Solid. These are also known as Ostwald slices. Within the ??-dimensional object color solid, for Version 1.1, 1/23every hue vector ??®*

#### 全色与离散色调格子

对于d维观察者，存在 $2^d$ 个由0-1反射函数生成的离散颜色格子点（Full Colors）。三色视者有8个全色（黑、白、红、绿、蓝、青、品红、黄），四色视者有16个全色。这些全色构成了色调流形下的离散骨架，为理解四色色彩命名和分类提供了结构基础（Fig. 5）。

### 工程实现：从理论到原型打印机

#### 理想墨水套件推导

基于Max Basis理论，论文推导出四色理想墨水反射函数CVPY（Fig. 9）。理想青（C）在短波处反射、长波处吸收；理想紫（V）在中短波处反射；理想粉（P）在中长波处反射；理想黄（Y）在长波处反射。这四种反射函数通过减法混合理论上可覆盖完整的四色域。

![[assets/figures/papers/paper_list_l40_https_imjal_github_io_theory_of_tetrachromacy/figures/011_Figure_10.jpg]]
*Figure 10: Simulated and Real Prints Sampling Hue Spaces for Tri- and Tetrachromacy. The prints are a prototype towards fabrication of color vision tests for tetrachromacy that are based on two-dimensional hue ordering (see 3.6). Box 1: first, an example in trichromacy of a linear sampling of the hue circle, with example reflectance functions. 1.A shows a simulated print with the idealized inks for trichromacy shown in Fig. 9-A1. 1.B shows a simulated print using reflectances for real inks shown in Fig. 9-C1. 1.C shows a photograph of a physical print, with spectrally measured reflectance functions as shown. Box 2 shows the analogous examples for the tetrachromatic case, showing a 2D sampling of the h...*

#### 墨水库构建与色域模拟

为寻找接近理想反射函数的真实墨水，作者收集并光谱表征了52种钢笔水（Fig. 8）。在四色色度空间中，每种墨水被投影为一个点。通过Kubelka-Munk模型和Yule-Nielsen修正的Neugebauer方程模拟减法混合：

$$R(\lambda) = \left( \sum_{i=1}^{2^k} w_i \, \big( R_i(\lambda) \big)^{1/\eta} \right)^{\eta} \tag{14}$$

其中 $w_i$ 是 $2^k$ 种墨水叠加状态的面积权重，$\eta$ 是Yule-Nielsen修正因子。该模型用于预测任意墨水组合的反射率，从而评估色域覆盖。

#### 原型打印机构建

基于色域模拟，最终选定的四色墨水为：Epson Cyan、Platinum Violet、Diamine Peach Haze和Noodler's Orange。打印机平台为多通道Epson EcoTank喷墨打印机，通过多次打印实现四色叠加。

### 广义色觉测试设计

#### 二维色调排序测试

传统Farnsworth-Munsell 100色调测试在一维色调圆上采样。论文将其推广到二维色调球面：在球面上采用立方体贴图（cubemap）采样486个点，每个点对应一个特定色调方向的颜色样本。受试者需要将打乱的样本按球面邻域关系排序。对于三色视者，这些样本应呈现为混乱排列；对于四色视者，应能感知到球面上的连续色调变化。

#### 四色等色板

仿照石原色盲检测图的设计原理，论文制作了四色等色板（Fig. 11, 12）。等色板由两种反射率不同的颜色组成，它们对L、M、S锥体产生相同的响应（对三色视者同色异谱），但对Q锥体产生显著不同的响应。三色视者看到均匀灰色，而四色视者能看到隐藏的数字（如"89"）。光谱测量验证了这一同色异谱性质（Fig. 12）。

### 关键Changed Slots

相比传统三色色彩系统，本文在以下维度上进行了根本性改变：

1. **印刷原色数量**：从3（CMY）增加到4（CVPY），使减法混合系统能够覆盖四维色彩空间。
2. **色彩空间维度**：从三维（色度圆盘）提升到四维（色度球体），色调从一维圆环变为二维球面。
3. **色调测试采样**：从一维色调圆采样推广到二维色调球面立方体贴图采样。
4. **筛查测试混淆色**：从二色视者混淆线（如红-绿）推广到Q锥体混淆色（对L/M/S同色异谱，对Q不同）。

这些改变构成了从三色到四色色彩系统的完整理论-工程闭环：理论推导→墨水设计→原型制造→测试验证，每一步都依赖于维度推广带来的新几何结构。

## 实验与关键发现

本文的实验验证围绕两个核心目标展开：一是检验理论推导的理想四色墨水套件（CVPY）在实际打印系统中的可实现程度，二是展示所制作的色样能否成为筛查功能性四色视者的有效工具。由于目前缺乏实验室确认的功能性四色视者群体，感知验证仍停留在基于模拟四色视者光谱响应的客观测量阶段。

### 理想墨水套件与实际墨水色域

理论推导的理想四色原色为Cyan、Violet、Pink、Yellow（CVPY），其反射函数通过最大化四色物体颜色固体内的平行多面体体积得到（Max Basis优化，Eq. 11）。为寻找接近理想反射函数的实际墨水，作者建立了包含52种钢笔水的墨水库，并在四色色度空间中对其进行可视化（Fig. 8）。最终选定的四色墨水组合为Epson Cyan、Platinum Violet、Diamine Peach Haze和Noodler’s Orange。

Fig. 9对比了三色和四色视者理想与实际打印机墨水的色域。对于三色视者，传统CMY墨水的色域覆盖了理想三色域的大部分；而对于四色视者，实际CVPY墨水仅覆盖理想四色域体积的**4.17%**。这一数值虽看似微小，但需注意传统CMY打印机在四色空间中的色域体积为**0%**——因为三色墨水只能在四色空间中生成一个退化的三维子空间，无法覆盖任何四色体积。因此，4.17%的覆盖代表了从无到有的质变。

### 色调球体采样与打印覆盖率

四色视者的色调空间是一个二维球面（hue sphere），而非三色视者的一维色调圆环。为系统评估原型打印机的色域覆盖，作者在色调球面上均匀采样了**486个点**（通过立方体贴图展开），对每个点计算其对应的理想反射函数，并判断该颜色是否落在实际打印机的色域内。

结果显示，原型CVPY打印机能够打印出色调球面上**52%的点（254/486）**（Fig. 10）。相比之下，传统CMY打印机仅能打印球面上的一条一维曲线（约0%的覆盖率）。Fig. 10展示了模拟和实际打印的色调球面展开图，可见CVPY打印品在球面的大部分区域都有覆盖，但在某些色调区域存在明显缺失。这一覆盖率的局限主要源于实际墨水反射函数与理想阶跃函数的偏差，以及减色混合过程中不可避免的色域压缩。

![[assets/figures/papers/paper_list_l40_https_imjal_github_io_theory_of_tetrachromacy/figures/001_Figure_10.jpg]]
*Figure 10: In a main contribution of this paper, we compute the analogous geometry for tetrachromacy, predicting a hue space (C) that is topologically equivalent to a sphere (S ). We analyze how this higher dimensional topology predicts a fundamentally richer color experience (Sec. 4) for tetrachromats. For example, the flattened cubemap of the hue sphere in (D) highlights an interesting pair of tetrachromatic hues, which we call keef and litz, that both appear gray to a trichromat but are complementary hues to a tetrachromat (as distinct as blue and yellow). An important note (*) is that the underlying colors in (C) and (D) are spectral functions, all unique to a tetrachromat, but these colors are vi...*

### Q轴色域宽度

为进一步量化四色打印机的色域沿第四锥体（Q锥）方向的扩展能力，作者测量了打印色域在Q轴方向上的宽度，并与物体颜色固体的理论最大宽度进行比较。原型打印机的Q轴色域宽度达到理论最大值的**29.9%**。作为参照，传统CMY打印机沿L锥体轴的色域宽度约为理论最大值的44%，但这是在三色空间中的表现，与四色Q轴不可直接比较。29.9%的Q轴覆盖率表明，原型系统确实能够在第四锥体方向上产生有意义的信息差异，为后续的等色板设计提供了物理基础。

### 四色等色板的设计与验证

等色板（isochromatic plates）是筛查色觉异常的标准工具，其核心原理是设计对目标观察者同色异谱（metameric）而对异常观察者可区分的颜色对。本文将这一原理推广到四色视者的筛查：设计对三色视者（L、M、S锥体）同色异谱、但对假设的四色视者（额外Q锥体）产生不同响应的颜色组合。

Fig. 11展示了理想四色等色板的设计，隐藏数字“89”由两种反射函数构成，它们在三色视者的LMS响应空间中完全相同，但在Q锥响应上存在显著差异。Fig. 12展示了实际制作的原型等色板及其光谱测量验证结果。测量数据确认：两种颜色的反射光谱不同，但对L、M、S锥体的积分响应几乎一致（三色同色异谱成立），而对Q锥体的积分响应则有明显差异。这一定量验证表明，该等色板在物理层面具备区分四色视者与三色视者的潜力。

### 实验局限与适用边界

**感知验证缺失**：本文的所有实验验证均基于光谱测量和模拟的锥体响应计算，未在实验室确认的功能性四色视者身上进行实际观察测试。等色板能否真正被四色视者感知为不同颜色，取决于其Q锥的光谱敏感度是否与本文假设的响应函数一致，以及其神经系统的对比度阈值。这一关键环节需要后续的心理物理实验确认。

**色域覆盖不足**：原型打印机仅覆盖52%的色调球面和4.17%的理想色域体积，意味着大量四色颜色无法被打印。这可能导致某些类型的四色视者（如果其Q锥敏感度峰值与现有墨水不匹配）无法通过当前等色板被检测到。更优的墨水选择或更多原色数的打印系统可能改善这一问题。

**环境因素**：同色异谱匹配依赖于特定的照明体。本文的计算基于标准照明体D65，在实际观察中，照明条件的变化可能破坏三色同色异谱的匹配精度，导致假阳性或假阴性结果。

**缺乏感知均匀空间**：当前的色域评估和采样均在线性锥体响应空间中进行，该空间不反映感知均匀性。52%的球面覆盖率在线性空间中可能对应不同的感知覆盖率，这一差异需要建立四色视者的感知均匀色彩空间后才能准确评估。

![[assets/figures/papers/paper_list_l40_https_imjal_github_io_theory_of_tetrachromacy/figures/007_Figure_6.jpg]]
*Figure 6: Every Tetrachromatic Hue has a Circular Continuum of Neighboring Hues. A: first, for comparison, observe that in regular color vision, every hue has exactly two heighbors because of the topology of the hue circle. For example, orange’s neighbors are red and yellow, but not pink or green. B: the situation is different in tetrachromatic color experience: orange neighbors pink, yellow, green and red. Keep in mind (*) that the tetrachromatic hues on the sphere are visualized as they would appear to a trichromat, but to a tetrachromat, all neighboring hues would be equally similar in their color relationship to orange. Spectral reflectance functions are shown for these five colors. This example...*

![[assets/figures/papers/paper_list_l40_https_imjal_github_io_theory_of_tetrachromacy/figures/010_Figure_9.jpg]]
*Figure 9: Comparison of Idealized and Real Printer Inks for Trichromats (Row 1) and Tetrachromats (Row 2). For trichromats, the three required inks for printers are well known to be cyan (C), magenta (M) and yellow (Y). A1 shows our computation of the idealized reflectance functions for C, M and Y, and 1.B shows 304 305 the resulting printer gamut in the 2D trichromatic chromaticity disk. In C1 and D1, the real trichromatic printer is a consumer Epson EcoTank printer, with (M) and yellow (Y) inks. 1.A shows the idealized reflectance functions for these inks, and 1.B shows the resulting printer gamut in the 2D trichromatic measured ink reflectances shown in C1 and simulated gamut shown in D1. Row 2 sh...*

![[assets/figures/papers/paper_list_l40_https_imjal_github_io_theory_of_tetrachromacy/figures/008_Figure_7.jpg]]
*Figure 7: Color blindness and Comparative Dimensionality of Chromaticity Space. Left: Projection of the trichromatic chromaticity disk onto the dichromatic chromaticity line (protanope). The dichromat confuses colors along the ?? cone projection lines, resulting in red-green color blindness and an impoverished sense of hue compared to trichromats. Right: the analogous projection of the tetrachromatic chromaticity ball onto the trichromatic chromaticity disk. Similar to before, the trichromat confuses colors along the ?? cone projection lines, resulting in a similarly fundamental level of color blindness compared to tetrachromats. Keep in mind (*) that the tetrachromatic hues are visualized here as th...*

## 定位与知识库关联

本文的工作在色彩科学的知识体系中占据一个独特的“理论先行、工程验证”的位置：它并非对现有三色视觉系统的增量改进，而是**将色彩再现的维度从3提升到4**，从而开辟了一个此前仅存在于遗传学推测中的四色视觉体验空间。

### 相对已有方法的本质差异与改变的Slot

本文相对于现有基线，改变了四个关键的结构性“插槽”（slot）：

1. **打印原色数量：3 → 4。** 传统彩色打印基于CMY三原色（青、品红、黄），其理论基础是三色视觉的色度圆盘。本文将原色数量扩展为4，提出理想的四色墨水套件**CVPY**（Cyan, Violet, Pink, Yellow），使打印系统能够覆盖四色视者色度空间中的体积，而非仅一条线。这一改变是根本性的——它意味着打印输出的信息维度从三维升至四维。

2. **色彩空间维度：三维色度圆盘 → 四维色度球体。** 三色视觉的色度空间是一个二维圆盘，色调构成一个一维圆环（hue circle）。本文首次完整计算了四色视者的物体颜色固体（Object Color Solid），揭示其色度空间是一个**三维球体**，色调构成一个**二维球面**（hue sphere）。这一拓扑差异导致四色视者每个色调拥有一个圆形的连续邻域，而非三色视者的仅有两个邻居（Fig. 6）。

3. **色调排序测试的采样方式：一维圆环采样 → 二维球面采样。** 经典的Farnsworth-Munsell 100 Hue Test（Farnsworth, 1943）在一维色调圆上采样。本文将其推广为在色调球面上的**二维cubemap采样**（486个点），原型打印机可覆盖其中52%的点（254/486），而传统CMY打印机仅能打印球面上的一条一维线（Fig. 10）。

4. **色盲筛查测试的混淆颜色：二色视者混淆线 → Q锥体混淆色。** 石原色盲测试（Ishihara, 1918）利用二色视者沿L/M锥体投影线的混淆特性设计等色板。本文将其推广到四色维度，设计出对三色视者（L/M/S）同色异谱、但对假设的第四锥体（Q）有显著不同响应的**四色等色板**（Fig. 12），使功能性四色视者的筛查成为可能。

### 知识库挂载点

本文的理论基础直接挂载在以下知识节点上：

- **n维物体颜色理论**：本文是Logvinenko和Levin（2022）提出的n维物体颜色固体理论的首次完整四维实例化计算。论文将Koenderink（2010）的三色Full Colors概念推广到n维，并利用“最大基”（Max Basis）优化方法（Sec. 3.2）推导出四色视者的理想原色反射函数。

- **印刷色彩学**：理想墨水反射函数的推导直接类比三色CMY系统的“分区白”（partition of white）原理。实际打印采用Yule-Nielsen修正的Neugebauer方程（Eq. 14）进行半色调颜色预测，这是印刷色彩再现的标准框架。

- **色觉缺陷筛查**：四色等色板的设计逻辑直接继承自石原测试的“混淆颜色”原理，但将混淆维度从二色视者的锥体缺失推广为三色视者相对于四色视者的“维度缺失”（Fig. 7）。

### 适用边界与局限

本文的工作具有明确的理论和工程边界：

- **理论层面**：所有计算依赖于一个假设的第四锥体光谱敏感度函数（Q锥体），其峰值位于L和M锥体之间。实际功能性四色视者的Q锥体光谱可能因人而异，因此本文的色度球体是**特定假设下的理想化模型**，而非对所有四色视者通用的绝对色彩空间。

- **工程层面**：原型CVPY打印机仅能覆盖理想四色色域体积的4.17%，以及色调球面上约一半的点。这一覆盖率远未达到理想水平，可能不足以区分所有潜在的四色视觉类型。此外，系统仅聚焦反射式打印，未涉及自发光显示器等四色再现方式。

- **感知验证缺失**：本文的视觉测试仅基于少数观察者的主观报告，**未在实验室确认的功能性四色视者身上进行心理物理验证**。实际区分能力仍有待严格的感知实验确认。环境照明和同色异谱效应也可能影响实际观察效果。

- **缺乏感知均匀色彩空间**：论文使用的线性色彩空间不能反映四色视者的感知均匀性，目前尚无类似CIELAB的四色视者感知均匀空间。

### 后续研究启发

本文打开的后续研究方向包括：

1. **大规模四色视者筛查**：利用本文开发的四色等色板和色调球面测试，在野外大规模发现功能性四色视者，这是验证理论的关键一步。

2. **四色感知均匀空间的构建**：通过心理物理实验（如MacAdam椭圆在四维空间的推广），建立四色视者的感知均匀色彩空间，为四色图像处理和再现提供感知基础。

3. **四色显示技术**：探索自发光四色显示器的色彩再现能力和局限，这可能比反射式打印具有更大的色域覆盖。

4. **三色视者对四色体验的理解**：人类三色视者如何通过类比和数学工具理解和想象四色视者的色调球体及其互补色（如keef和litz），这不仅是一个认知科学问题，也是科学传播的挑战。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Theory_of_Human_Tetrachromatic_Color_Experience_and_Printing.pdf]]