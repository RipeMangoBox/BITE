---
title: Clustered Vector Textures
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Clustered_Vector_Textures.pdf
project_link: "https://phtu-cs.github.io/cvt-sig22/"
code_link: null
aliases:
- CVT
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 在迭代的搜索-分配优化框架中显式地对样本进行聚类优化（包括聚类合并、分裂和样本切换），并将聚类信息融入邻域相似性计算，从而保持元素的完整性。
primary_logic: 将每个向量元素表示为一个样本聚类，并在合成过程中将其作为优化变量，通过链接能量（样本相关性）和形状能量（形状相似性）共同引导聚类配置的优化，扩展了优化问题的可行域，使得合成结果能更好地保持结构化图案的局部交互和形状多样性。
claims:
- 明确加入聚类步骤，并在邻域相似性计算中融入聚类信息（形状上下文特征），显著提高了合成图案的结构完整性。
- 通过将聚类作为优化变量，并设计包含链接能量和形状能量的目标函数，使得输出图案能保持输入图案的元素形状和交互关系。
- 消融实验表明，移除聚类信息（w_f=0）会导致结果随机化，移除链接/形状能量则产生空洞和断裂。
- 与 Ma et al. 2011、Hsu et al. 2020、Tu et al. 2020 的比较显示，本文方法在生成多样化结构化向量图案方面具有明显优势。
---

# Clustered Vector Textures

> [!tip] 核心洞察
> 将每个向量元素表示为一个样本聚类，并在合成过程中将其作为优化变量，通过链接能量（样本相关性）和形状能量（形状相似性）共同引导聚类配置的优化，扩展了优化问题的可行域，使得合成结果能更好地保持结构化图案的局部交互和形状多样性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 聚类向量纹理 |
| 英文题名 | Clustered Vector Textures |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://phtu-cs.github.io/cvt-sig22/) · [Project](https://phtu-cs.github.io/cvt-sig22/") |
| Topic | #topic/other_unclear |
| Method | Clustered Vector Textures |
| Dataset | 聚类对比基线（Improved Tu et al. 2020 + 谱聚类） |

> [!tip] 效果简介
> - 多样化向量图案示例（如花卉、装饰、几何图案） 上，视觉质量（元素完整性、局部交互、无断裂） 本文方法（聚类优化） vs Ma et al. 2011, Hsu et al. 2020, Tu et al. 2020 (显著改善，能生成结构更复杂、形状更多样的图案)。
> - 聚类对比基线（Improved Tu et al. 2020 + 谱聚类） 上，视觉质量 本文方法 vs Improved Tu et al. 2020 (更好保持形状和结构，避免断裂)。

## 概要

本文针对基于样本的向量图案合成中**元素易断裂、合并或变形**的核心瓶颈，提出**聚类向量纹理（Clustered Vector Textures）**方法。关键创新在于将每个向量元素显式表示为一组样本的**聚类**，并将聚类配置作为优化变量融入迭代的搜索-分配框架中——通过在邻域相似性计算中引入形状上下文特征，并设计包含链接能量（样本相关性）与形状能量（形状相似性）的聚类目标函数，使合成过程能同时保持元素的形状完整性与局部交互关系。实验表明，相较于 Ma et al. 2011、Hsu et al. 2020 及 Tu et al. 2020 等先前方法，本方法能生成结构更复杂、形状更多样的向量图案；消融实验证实移除聚类信息或能量项将导致结果随机化或出现空洞断裂。该方法定位于基于样本的纹理合成与向量图形生成交叉领域，为结构化图案的自动合成提供了新的聚类优化范式。

## 核心方法与创新机理

### 问题背景与核心瓶颈

传统的基于样本的向量图案合成方法（如 Ma et al. 2011、Tu et al. 2020）遵循搜索-分配（Search-Assign）的迭代优化框架：将输入图案采样为离散样本集，通过最小化输入与输出邻域之间的距离来优化输出样本的空间分布。然而，这些方法存在一个根本性瓶颈：**它们缺乏对多样本元素形状和复杂局部交互的显式建模**。具体而言，每个向量元素（如一片花瓣、一片叶子）在采样后仅作为一组独立样本存在，优化过程中样本之间的元素归属关系不被维护，导致合成结果中元素容易断裂、合并或发生非自然变形。

### 核心创新：聚类作为优化变量

本文的核心洞察是：**将每个向量元素表示为一个样本聚类（Cluster），并将聚类配置本身作为优化变量纳入迭代优化过程**。这一设计将合成问题从单纯的样本空间分布优化扩展为样本分布与聚类配置的联合优化，显著扩展了优化问题的可行域。具体而言，方法在传统搜索-分配循环中新增了一个**聚类步骤（Clustering Step）**，通过设计包含链接能量和形状能量的目标函数，显式地优化哪些样本属于同一个元素（聚类），从而在合成过程中保持元素的完整性和形状多样性。

### 方法框架与模块顺序

整体流水线包含以下顺序模块，形成多层级的迭代优化循环：

1. **输入表示：采样与聚类**（Section 4.2）  
   将输入向量图案的每个元素表示为一个聚类，并在元素边界内部进行泊松圆盘采样，生成带有聚类 ID 的样本集。每个样本 $s$ 记录以下信息：
   
   $$\mathbf{U}(s) = (\mathbf{S}(s), \mathbf{A}(s))$$
   
   其中 $\mathbf{S}(s)$ 为空间参数（位置、朝向、缩放），$\mathbf{A}(s)$ 为外观属性（聚类 ID、置信度、z-index 深度值、形状上下文特征向量 $\mathbf{f}$）。

2. **初始化**（Section 6.2）  
   通过随机复制输入 patch 或随机撒点两种策略初始化输出样本集，样本的初始聚类 ID 从对应输入样本继承。

3. **搜索步骤（Search Step）**（Section 6.3）  
   为每个输出样本 $s_o$ 寻找最相似的输入邻域。关键创新在于**邻域相似性计算中融入了聚类信息**：样本间距离不仅包含相对位置差，还包含基于聚类的形状上下文特征的卡方距离：
   
   $$d_s(s_o', s_i') = \|\hat{\mathbf{p}}(s_o', s_o) - \hat{\mathbf{p}}(s_i', s_i)\| + \frac{w_{\mathbf{f}}}{2} \sum_{q=1}^{N_{\mathbf{f}}} \frac{(\mathbf{f}^q(s_o') - \mathbf{f}^q(s_i'))^2}{\mathbf{f}^q(s_o') + \mathbf{f}^q(s_i')}$$
   
   其中 $\hat{\mathbf{p}}$ 为相对于邻域中心的归一化位置，$\mathbf{f}$ 为形状上下文特征向量，$w_{\mathbf{f}}$ 为权重系数。这一设计使得相似性比较能够感知样本所属元素的形状信息，而非仅依赖空间位置。

4. **分配步骤（Assignment Step）**（Section 6.4）  
   根据搜索步骤找到的匹配关系，更新输出样本的空间位置、存在性（通过置信度阈值过滤低质量样本）以及深度顺序。深度排序采用概率成对排序函数 $f_s(s_o, s_o')$ 和 "Order-By-Preferences" 算法，从匹配邻域中投票推断元素之间的前后遮挡关系。

5. **聚类步骤（Clustering Step）**（Section 6.5）——**核心创新模块**  
   通过贪婪优化更新输出样本的聚类配置 $\{C_o^k\}$，目标函数为：
   
   $$E(\{C_o^k\}) = w_l E_l(\{C_o^k\}) + w_s E_s(\{C_o^k\})$$
   
   其中 $w_l=1$, $w_s=4$。该目标函数由两项组成：
   
   - **链接能量 $E_l$**（样本相关性）：基于邻域匹配投票计算输出样本对 $(s_o, s_o')$ 的链接置信度 $l(s_o, s_o')$，即两者应属于同一聚类的概率。对每对样本施加奖励/惩罚：
     
     $$E_l'(s_o, s_o') = \begin{cases} 1 - 2l(s_o, s_o') & \text{if } \mathbf{i}(s_o) = \mathbf{i}(s_o') \\ 2l(s_o, s_o') - 1 & \text{if } \mathbf{i}(s_o) \neq \mathbf{i}(s_o') \end{cases}$$
     
     若链接置信度高但两样本被分到不同聚类，则施加惩罚；反之亦然。
   
   - **形状能量 $E_s$**（形状相似性）：衡量每个输出聚类 $C_o$ 与其匹配的输入聚类 $C_i$ 之间的形状差异，通过最优样本匹配和聚类大小惩罚项实现：
     
     $$d_{\mathcal{C}}(C_i, C_o) = \min_m \frac{1}{\epsilon} \left( \sum_{\substack{s_o \in C_o \\ s_i = m(s_o) \in C_i}} \|\mathbf{p}(s_o) - \mathcal{T}_r(\mathbf{p}(s_i), C_i, C_o)\| + \epsilon \cdot \mathbf{abs}(|C_o| - |C_i|) \right)$$
     
     其中 $\mathcal{T}_r$ 为刚性变换对齐，$\epsilon$ 平衡形状匹配与大小一致性。
   
   聚类优化通过三种局部操作符实现：**样本切换**（将样本从一个聚类移至另一个）、**聚类合并**（将两个聚类合并为一个）和**聚类分裂**（将一个聚类拆分为两个）。这些操作符按比例在不同层级中执行（Table 1），逐步优化聚类配置。

6. **重建与过滤**（Section 6.6）  
   从优化后的聚类重建向量元素形状，并根据重建误差过滤低质量元素（误差超过阈值的元素被丢弃，Figure 2f 中以黄色标示）。

7. **多层优化**（Section 6.7）  
   采用层级采样策略：从粗到细逐步增加样本数量，每一层级内迭代执行搜索-分配-聚类步骤（通常每层 7 次迭代），将上一层的优化结果作为下一层的初始化。

### 关键 Changed Slots 与因果链路

相对于基线方法，本文方法在以下关键槽位上进行了替换：

| 槽位 | 基线值 | 本文方案 | 因果作用 |
|------|--------|----------|----------|
| **样本聚类表示** | 固定元素 ID 或无聚类 | 聚类作为优化变量，动态调整 | 使元素归属关系在优化中可维护、可修正 |
| **邻域相似性** | 仅位置和图形信息 | 加入形状上下文特征 $\mathbf{f}$ | 使搜索步骤感知元素形状，避免匹配到形状不一致的邻域 |
| **聚类目标函数** | 无 | 链接能量 + 形状能量 | 从样本相关性和形状相似性两个维度引导聚类优化 |
| **深度排序** | 不考虑或简单层序 | 概率成对排序 + Order-By-Preferences | 保持元素间的前后遮挡关系 |

这些槽位之间的因果关系链为：**聚类表示**为优化提供了可操作的变量空间 → **邻域相似性中的形状特征**使搜索步骤能够区分不同形状的元素，为聚类优化提供准确的匹配信号 → **聚类目标函数**利用这些匹配信号，通过链接能量维护样本归属一致性，通过形状能量保持元素形态 → **深度排序**在元素层面保持遮挡关系 → 最终**重建与过滤**输出结构完整的向量图案。消融实验（Figure 14）验证了这一因果链：移除形状特征（$w_f=0$）导致合成结果随机化；移除链接或形状能量则产生空洞和断裂。

![[assets/figures/papers/paper_list_l2_https_phtu_cs_github_io_cvt_sig22/figures/008_Figure_7.jpg]]
*Figure 7: Illustration of cluster shape energy computation. (a) shows an output cluster*

## 实验与关键发现

### 主结果：与先前方法的定性对比

本文在多样化的向量图案示例上进行了系统评估，涵盖花卉、装饰纹样、几何图案等类别。由于向量图案合成领域缺乏公认的客观定量指标，评估主要依赖视觉质量——元素完整性、局部交互保持和无断裂变形。

与三类代表性基线方法的对比（Figure 3、Figure 13、Figure 24）显示了本文聚类优化策略的显著优势：

![[assets/figures/papers/paper_list_l2_https_phtu_cs_github_io_cvt_sig22/figures/003_Figure_3.jpg]]
*Figure 3: Comparison with previous methods. Given an input exemplar (a), our method samples a clustered sample distribution (b), synthesizes clustered output samples (f ), and reconstructs the final patterns (g). Clusters are visualized in colors. We compare our method against prior vector pattern synthesis methods [Ma et al. 2011] (c), [Hsu et al. 2020] (d), and [Tu et al. 2020] (e). As shown, while Ma et al. [2011] can generate broken structures and Hsu et al. [2020] can only place elements uniformly, our method can preserve diverse structures from the exemplars. Since [Tu et al. 2020] can only handle Bézier curve patterns via graph synthesis which could not be reconstructed as general shapes, we o...*

![[assets/figures/papers/paper_list_l2_https_phtu_cs_github_io_cvt_sig22/figures/013_Figure_13.jpg]]
*Figure 13: Comparisons against improved [Tu et al. 2020] with baseline clustering. The improved version of [Tu et al. 2020] uses spectral clustering [Von Luxburg 2007] as the basic clustering algorithm; each input element is represented as a fully connected graph, and the output edge confidences in [Tu et al. 2020] are used as the weights for the weighted similarity graphs in [Von Luxburg 2007]. In addition, clusters are used during neighborhood search, as in Equations (2) and (3). The final shapes are reconstructed as described in Section 6.6*

- **Ma et al. 2011**（基于离散元素的示例合成）：该方法固定样本集进行合成，缺乏对元素形状的显式建模，在复杂结构化图案上容易产生元素断裂和结构破碎。
- **Hsu et al. 2020**（基于规则打包的图案合成）：仅能均匀放置元素，无法再现输入示例中丰富的局部交互和形状多样性。
- **Tu et al. 2020**（连续贝塞尔曲线纹理合成）：该方法通过图合成处理贝塞尔曲线图案，但无法重建为通用形状，只能展示样本级合成结果。

相比之下，本文方法通过将聚类作为优化变量，在搜索-分配-聚类迭代框架中动态调整聚类配置，生成的图案能够保持输入示例的结构特征和元素形状完整性，同时产生合理的局部交互。

为进一步验证聚类策略的有效性，作者构建了改进基线 **Improved Tu et al. 2020 + Spectral Clustering**（Figure 13）：在 Tu et al. 2020 的合成结果上应用谱聚类进行后处理，再按 Section 6.6 的方法重建形状。该基线虽能识别部分元素分组，但因聚类与合成过程解耦，无法在合成中纠正样本错配，导致重建形状出现断裂和变形。本文的联合优化策略则使聚类信息反馈到邻域相似性计算中，形成闭环，从而更好地保持形状和结构。

Figure 11 展示了 12 种不同风格示例的自动合成结果画廊，覆盖花卉、叶饰、几何纹样等多种图案类型，验证了方法的通用性。Figure 25 进一步展示了 4×4 倍的大规模扩充结果，表明方法可生成高分辨率无缝向量图案。

![[assets/figures/papers/paper_list_l2_https_phtu_cs_github_io_cvt_sig22/figures/011_Figure_11.jpg]]
*Figure 11: Automatic synthesis results with a variety of exemplar patterns. Within each group, the input is on the left and our result is on the right. Copyrights: (a) galyna_p (b) leavector (c) Alona Khadzhyoglo (d) olga_milagros (e) galyna_p (f ) hoverfly (g) Olgastocker (h) hoverfly (i) hoverfly (j) Meganathan (l) natalyon (stock.adobe.com), and (k) keeeny.am (vecteezy.com)*

### 关键消融实验

消融实验（Figure 14）逐一验证了各核心组件的因果贡献：

| 消融条件 | 效果 | 因果解释 |
|---------|------|---------|
| 移除聚类特征（$w_f = 0$） | 合成结果趋于随机化 | 邻域相似性计算失去形状上下文信息，搜索步骤无法区分不同形状的样本，导致匹配质量下降 |
| 移除链接能量（$E_l = 0$） | 输出出现空洞区域 | 聚类步骤失去样本相关性引导，无法将属于同一元素的样本正确聚合 |
| 移除形状能量（$E_s = 0$） | 元素出现断裂 | 聚类配置失去形状相似性约束，无法保持元素几何形态的完整性 |

聚类操作符组合的消融（Figure 23）进一步表明，缺少样本切换、聚类合并或分裂中的任一操作符，都会导致合成失败——输出图案出现空洞或断裂区域。这验证了三类操作符在贪婪优化中的互补性：样本切换实现局部调整，合并和分裂实现全局聚类结构的重组。

Table 1 统计了不同层级中三类聚类操作的比例：样本切换操作数量远超聚类合并/分裂（因每个聚类包含多个样本），但合并和分裂操作对聚类结构的全局调整不可或缺。

### 超参数鲁棒性

方法对关键超参数在一定范围内表现鲁棒（Figure 21、Figure 22）：

- **形状特征权重 $w_f$**：在 $w_f = 10$ 附近取得最佳效果；过小导致聚类信息不足，过大则压制位置信息。
- **形状能量权重 $w_s$**：在 $w_s = 4$ 附近取得最佳效果；过小导致形状约束不足，过大则限制聚类灵活性。

能量曲线（Figure 16）显示，不同初始化策略（随机采样 vs. 基于 patch 的初始化）和不同示例的能量均稳定收敛，表明优化框架具有良好的数值稳定性。多层优化策略（Section 6.7）通过层级采样逐步细化，进一步增强了收敛的可靠性。

### 深度排序效果

深度分配（z-index）的对比实验（Figure 5）表明，通过概率成对排序函数和 "Order-By-Preferences" 算法，本文方法能够较好地保持输入示例中的层叠关系（如花瓣在上、枝叶在下）。无深度分配时，这些层关系会丢失，导致视觉混乱。

![[assets/figures/papers/paper_list_l2_https_phtu_cs_github_io_cvt_sig22/figures/005_Figure_5.jpg]]
*Figure 5: Z-index (depth) assignment. In the input exemplars, the sky blue petals are above other elements (top) and the branches are below the leaves (bottom). Without depth assignment, this layer relationship is not preserved. With depth assignment, the relationship is mostly preserved. Copyright: exemplars from Eva Kali (top), Snejana Sityaeva (bottom) (stock.adobe.com)*

### 计算效率与瓶颈

Table 2 报告了各算法组件在不同层级的总运行时间。搜索步骤是主要计算瓶颈——需要在每次迭代中为每个输出样本寻找最相似的输入邻域。聚类步骤和分配步骤的开销相对较小。多层优化中，样本数量随层级递增，总运行时间随之增长。当前实现尚未达到交互式水平，搜索步骤的并行化或近似加速是未来工作方向。

### 失败模式与适用边界

Figure 15 系统展示了方法的局限性：

![[assets/figures/papers/paper_list_l2_https_phtu_cs_github_io_cvt_sig22/figures/015_Figure_15.jpg]]
*Figure 15: Limitations. Our method is unable to handle patterns with (a) regular or (c) non-local structures due to the inherent limitations of patch-based synthesis method. Our method requires the input to contain sufficient spatial repetitions and could not handle small tiles with little spatial repetitions (e). Our current implementation has yet to consider toroidal boundary conditions and thus the outputs will not tile seamlessly. Copyrights: (c) Eva Kali, (e) Dariia (stock.adobe.com)*

1. **规则/网格结构失效**：方法无法处理具有规则网格排列或非局部对称性的图案。这是基于局部邻域块的合成方法的固有局限——邻域窗口无法捕获长程规则性。
2. **空间重复不足**：要求输入示例包含足够的空间重复模式。对小尺寸或缺乏重复的图块，邻域匹配缺乏有效信息，合成质量下降。
3. **无环面边界条件**：当前实现未考虑环面边界条件，输出图案无法无缝平铺，限制了其在纹理映射等应用中的直接使用。
4. **细长/扭曲元素**：对于细长或高度扭曲的元素，可能出现不自然的交叠，聚类形状能量难以准确约束此类几何形态。
5. **仅限 2D 静态图案**：当前实现仅针对 2D 向量图案，未扩展到 3D 体积纹理或动画序列。

### 实验公平性说明

所有对比方法均使用原文作者提供或推荐的实现，并在相同输入示例上进行比较。由于缺乏客观定量指标，比较主要依赖视觉评估——这也是向量图案合成领域的普遍现状，未来工作可探索引入感知损失或结构相似性等定量指标。

## 定位与知识库关联

### 相对于已有方法的本质差异

本文的核心贡献在于**将向量元素的聚类配置提升为与样本空间分布并列的一阶优化变量**，从根本上改变了基于示例的图案合成框架中“元素”这一概念的建模方式。具体而言，本文相对于已有基线工作改变了以下关键 slot：

| 方法 | 元素表示方式 | 元素在优化中的角色 |
|------|-------------|-------------------|
| **Ma et al. 2011** (TOG 2011) | 固定的离散元素集，每个元素由单个样本或固定样本组表示 | 元素 ID 在合成过程中不变，仅优化样本位置 |
| **Tu et al. 2020** (TOG 2020) | 连续 Bézier 曲线样本，无显式元素分组 | 元素分组在后处理阶段通过图割或聚类重建，不参与优化循环 |
| **Hsu et al. 2020** (TOG 2020) | 基于规则的打包，元素形状和排列由预定义规则决定 | 元素布局由规则驱动，缺乏对示例中局部交互的学习 |
| **本文 Clustered Vector Textures** | 每个元素表示为一个样本聚类，聚类 ID 是样本的属性之一 | 聚类配置在每次迭代中通过专门的聚类步骤（合并、分裂、样本切换）进行优化，与搜索-分配步骤交替执行 |

这一改变的因果链条如下：传统方法（Ma et al. 2011, Tu et al. 2020）在邻域相似性计算中仅使用样本的位置和图形信息，导致优化过程对“哪些样本属于同一个元素”这一结构信息缺乏感知。当输入图案包含形状多样、间距紧密或存在部分遮挡的元素时，优化容易将不同元素的样本混淆，造成输出中的元素断裂、合并或变形。本文通过将聚类信息（形状上下文特征）嵌入邻域相似性计算（Equation 2-3），并在每次迭代中显式优化聚类配置（Equation 9），使得搜索和分配步骤能够感知元素边界，从而在根本上扩展了优化问题的可行域——不仅寻找样本的空间最优分布，同时寻找最优的元素划分。

### 知识库挂载点

本文可挂载到以下知识库节点：

1. **基于样本的纹理合成**（Example-based Texture Synthesis）：继承自 Kwatra et al. 2005 的搜索-分配优化框架，以及 Ma et al. 2011 将其扩展到离散元素图案的工作。本文在该节点上新增了“聚类作为优化变量”的子节点。

2. **向量图形合成与重建**（Vector Graphics Synthesis）：与 Tu et al. 2020 共享从样本重建向量形状的后处理思路，但本文将聚类前移到了优化循环内部，使得重建不再是盲目的后处理，而是受优化过程引导的。

3. **形状匹配与聚类**（Shape Matching and Clustering）：聚类目标中的形状能量（Equation 16）本质上是一种基于最优传输的形状匹配距离，可关联到点云配准和形状对应的工作。链接能量（Equation 12-13）则可视为一种基于邻域投票的谱聚类先验的软约束版本。

4. **深度排序**（Depth Ordering）：本文采用的“Order-By-Preferences”算法（Schapire and Singer 1998）将成对排序概率聚合成全局深度顺序，可关联到基于偏好聚合的排序学习节点。

### 适用边界

本文方法在以下条件下表现良好：
- 输入图案具有**丰富的局部交互和形状多样性**（如花卉、装饰纹样），这正是聚类优化的优势所在；
- 输入包含**足够的空间重复**，使得基于邻域匹配的合成机制有充足的统计信息；
- 图案结构以**局部交互为主**，不依赖全局规则或长程对称性。

本文方法的明确边界包括：
- **无法处理规则网格结构或非局部对称性**（Figure 15a, 15c），这是基于局部邻域匹配的合成方法的固有局限，与聚类优化无关；
- **不支持无缝平铺**，因当前实现未考虑环面边界条件；
- **仅限于 2D 静态矢量图案**，未扩展到 3D 体积或动画序列；
- **计算效率未达交互式水平**，搜索步骤（邻域匹配）是主要瓶颈（Table 2）。

### 后续工作启发

1. **聚类优化的加速与近似**：搜索步骤占运行时间主导（Table 2），可探索基于哈希的近似最近邻搜索或学习到的邻域嵌入来替代穷举匹配，使方法接近交互式应用。

2. **聚类能量与感知质量的桥接**：当前缺乏定量评估指标是领域共性问题。可探索将聚类重建误差或形状能量与人类感知判断相关联，或引入基于深度特征的感知损失作为辅助监督信号。

3. **聚类先验的扩展**：链接能量和形状能量分别编码了样本相关性和形状相似性，这一框架可自然扩展以支持更多先验，如元素间的对称性约束、周期性约束，或用户指定的语义分组。

4. **向动态和 3D 的拓展**：聚类表示本质上与维度无关，将样本推广到时空域（3D 体积或视频帧序列）并设计相应的聚类操作符，是一个有前景的方向。

5. **与生成模型的结合**：聚类配置可视为一种离散隐变量，可探索用变分自编码器或扩散模型来学习聚类配置的先验分布，从而实现可控的图案生成和插值。

> **注意**：本文与 Improved Tu et al. 2020 + Spectral Clustering 的对比（Figure 13）表明，简单地将谱聚类作为后处理步骤远不如将聚类嵌入优化循环有效，这验证了“聚类作为优化变量”而非“聚类作为后处理”的设计选择的关键性。这一洞察对其他需要同时优化分组和空间配置的问题（如场景布局、拼贴画生成）具有方法论层面的启发意义。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Clustered_Vector_Textures.pdf]]