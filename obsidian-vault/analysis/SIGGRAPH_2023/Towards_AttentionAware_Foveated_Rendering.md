---
title: Towards Attention–Aware Foveated Rendering
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/Towards_Attention_Aware_Foveated_Rendering.pdf
project_link: null
code_link: null
aliases:
- AACSM
- TAAFR
tags:
- SIGGRAPH_2023
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过调节中央凹RSVP任务难度（低、中、高）来控制分配给周边视野的注意力资源，从而改变周边对比度阈值和注视点模糊可接受程度。
primary_logic: 当用户注意力集中在中央凹任务时，周边视野的对比度敏感性显著下降（中注意力下阈值升高约2-3倍，高注意力下升高达4倍），这允许在不可感知范围内施加更强的注视点模糊，从而显著节省渲染带宽。
claims:
- 在中等注意力条件下，对比度阈值随离心率显著增加，7°处升高约2倍，21°处升高超过3倍。
- 高注意力条件下对比度阈值增加高达4倍，且三种注意力状态间差异显著（p<0.01）。
- 在注视点模糊研究中，中注意力和高注意力下的MAR斜率显著高于低注意力（p<0.001），表明用户可容忍更强的模糊。
- 使用我们所提出的注意力感知预测器预测的MAR斜率误差显著低于原始FovVideoVDP（p<0.01），验证了模型在注视点渲染中的有效性。
---

# Towards Attention–Aware Foveated Rendering

> [!tip] 核心洞察
> 当用户注意力集中在中央凹任务时，周边视野的对比度敏感性显著下降（中注意力下阈值升高约2-3倍，高注意力下升高达4倍），这允许在不可感知范围内施加更强的注视点模糊，从而显著节省渲染带宽。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向注意力感知的注视点渲染 |
| 英文题名 | Towards Attention–Aware Foveated Rendering |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://www.computationalimaging.org/publications/attention-aware/) |
| Topic | #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Attention–Aware Contrast Sensitivity Model |
| Dataset | Foveation MAR slope, Contrast threshold at 21° eccentricity |

> [!tip] 效果简介
> - Foveation MAR slope (across 4 images: Tulips, City, Mountain, Forest) 上，Mean MAR slope (higher ⇒ more blur tolerated) High attention: 0.0596 vs Low attention: 0.0198 (+0.0398 (3× increase))。
> - Contrast threshold at 21° eccentricity 上，Contrast threshold High attention: 0.1368 (approx) vs Low attention: 0.0314 (~4.4× increase)。

## 概要

现有注视点渲染依赖的对比度敏感度模型（如 StelaCSF）仅考虑离心率，忽视了注意力分配对周边视觉的显著影响，导致渲染带宽节省策略过于保守。本文首次通过心理物理学实验揭示：当用户注意力集中于中央凹任务时，周边视野的对比度阈值可升高 2–4 倍，且可容忍更强的注视点模糊。

核心方法为：通过中央凹 RSVP 任务难度（低、中、高）调控注意力资源，利用 QUEST 自适应阶梯法测量不同离心率下的对比度辨别阈值，进而构建注意力感知的对比度敏感度函数 $S_a(e, \cdots) = S(e, \cdots) \cdot 1/g_a(e)$，其中 $g_a(e)$ 为注意力增益。将该模型集成至 FovVideoVDP 质量预测器后，所预测的注视点模糊斜率（MAR slope）与实测值更吻合（p<0.01），验证了模型有效性。带宽分析表明，高注意力条件下渲染计算量可节省数倍于传统方法。

该方法将视觉注意力作为可控维度引入注视点渲染管线，为自适应图形系统提供了新的优化空间。

## 核心方法与创新机理

### 问题瓶颈与核心调节变量

现有注视点渲染技术依赖离心率依赖的对比度敏感度函数（CSF）模型，如 **StelaCSF**（Mantiuk et al., 2022），但这些模型基于受试者在周边视野投入高注意力的心理物理学实验数据。在实际应用场景中，用户注意力往往集中在中央凹任务上，导致周边视野的对比度敏感度显著下降。这一差异使得现有模型在预测可接受的注视点模糊程度时过于保守，未能充分挖掘渲染带宽节省的潜力。

本文的核心调节变量是**分配给周边视野的注意力资源**。通过控制中央凹 RSVP（快速序列视觉呈现）任务的难度（低、中、高三个水平），研究者系统性地调制了受试者对周边对比度辨别任务的注意力分配，从而测量不同注意力状态下的对比度阈值变化。

### 方法框架总览

整个方法体系由两条交织的管线构成：**心理物理学建模管线**与**注视点渲染应用管线**。前者通过受控用户实验测量注意力对周边对比度敏感度的调制效应，并构建解析模型；后者将注意力感知 CSF 集成到现有注视点渲染质量预测器 **FovVideoVDP**（Mantiuk et al., 2021）中，验证模型在实际渲染带宽节省中的有效性。

### 心理物理学实验设计

实验采用 **2AFC（双选项强制选择）自适应阶梯法**，基于 QUEST（Watson and Pelli, 1983）设计测量对比度辨别阈值。刺激为 Gabor 斑块，呈现在中央凹注视点左侧或右侧的指定离心率位置。关键设计要素包括：

- **离心率采样**：选择 7°、14°、21° 三个离心率点，覆盖显示器可用视场范围。
- **刺激参数选择**：在 21° 离心率处设置 Gabor 斑块直径为 5°，空间频率为 2 cpd，然后利用**皮层放大因子**（cortical magnification factor）按比例缩放 7° 和 14° 处的参数，以保持皮层表征的一致性。
- **注意力调制**：在中央凹呈现 RSVP 字母序列任务，受试者需检测目标字母 T。任务难度通过改变字母呈现速率和目标出现概率来控制，形成低、中、高三个注意力水平。难度越高，受试者需要投入越多注意力资源到中央凹，从而减少分配到周边辨别任务的注意力。

### 核心建模：从离散条件到连续函数

#### 逐条件拟合

对每个注意力条件，测量得到的对比度阈值 $t_a(e)$ 与离心率 $e$ 的关系拟合为平方根函数：

$$t_a(e) = p_0 \sqrt{e} + p_1$$

其中 $p_0$ 为斜率参数，$p_1$ 为截距参数。Table 2 给出了各条件的拟合参数及确定系数 $R^2$（低注意力：0.705，中注意力：1.000，高注意力：0.956），表明模型在中等和高注意力条件下拟合极佳。

![[assets/figures/papers/paper_list_l6_https_www_computationalimaging_org_publications_attention_aware/figures/004_Table_2.jpg]]
*Table 2: Fitted parameters of our attention-aware contrast threshold model*

#### 注意力增益函数

注意力增益 $g_a(e)$ 定义为各注意力条件下的阈值相对于低注意力基线的比值：

$$g_a(e) = \frac{t_a(e)}{t_{\mathrm{low}}(e)}$$

这一增益函数量化了注意力从周边撤离时对比度阈值的升高倍数。实验结果表明，在 21° 离心率处，中等注意力下增益约 3 倍，高注意力下增益可达 4 倍以上。

#### 注意力感知 CSF

将注意力增益作为正交缩放因子集成到现有 CSF 模型中：

$$S_a(e, \cdots) = S(e, \cdots) \cdot \frac{1}{g_a(e)}$$

其中 $S(e, \cdots)$ 为 StelaCSF 等现有模型，$S_a(e, \cdots)$ 为注意力感知的对比度敏感度。这一设计的核心假设是注意力增益与 CSF 的其他维度（空间频率、时间频率、亮度等）正交，即注意力调制可以作为一个独立的乘法因子施加。

#### 统一连续模型

为将离散的注意力水平（低、中、高）推广到连续注意力状态，研究者引入注意力系数 $a_c \in [0, 1]$，并通过伽马曲线插值各离散水平的斜率和截距参数：

$$t(e, a_c) = \Psi(s_0, s_1, a_c^{\gamma_s}) \cdot (\sqrt{e} - \sqrt{7}) + \Psi(i_0, i_1, a_c^{\gamma_i})$$

其中 $\Psi$ 为线性插值函数，$s_0, s_1$ 和 $i_0, i_1$ 分别为斜率和截距在低、高注意力下的取值，$\gamma_s$ 和 $\gamma_i$ 控制插值曲线的形状。该统一模型的自由度调整后 $R^2$ 达到 0.973，表明其能够以连续参数化方式准确描述注意力对对比度阈值的调制。

### 正交性验证

为验证注意力增益与其他 CSF 维度正交的关键假设，研究者设计了验证实验，使用 4 组与主实验不同的刺激参数（不同的空间频率、Gabor 尺寸和适应亮度，见 Table 1 下半部分），测量各注意力条件下的对比度阈值，并比较直接测量值与通过注意力增益缩放 StelaCSF 预测值之间的误差。

![[assets/figures/papers/paper_list_l6_https_www_computationalimaging_org_publications_attention_aware/figures/002_Table_1.jpg]]
*Table 1: Parameters of tested Gabor patches. For measuring the model (shown above the divider), we chose a diameter of*

结果表明：
- 对于大多数刺激条件，注意力感知模型的预测误差显著低于原始 StelaCSF（Fig. 4c），验证了正交性假设在多数情况下的合理性。
- 然而，注意力增益随适应亮度升高而降低——在 116 cd/m² 下，中等注意力的增益从 3.03 降至 2.15（p < 0.05），提示正交性在高亮度条件下可能不完全成立。

### 注视点渲染应用管线

#### 质量预测器修改

将注意力感知 CSF 集成到 FovVideoVDP 中，作为 CSF 分量的正交缩放因子。FovVideoVDP 的原始实现使用 StelaCSF 计算视觉差异图和质量分数；修改后的版本在 CSF 计算阶段引入 $1/g_a(e)$ 缩放，使得周边区域的敏感度预测随注意力状态调整。

#### MAR 斜率建模

注视点模糊的可接受程度通过**最小分辨角（MAR）**随离心率的线性增长模型描述：

$$\omega(e) = m e + \omega_0$$

其中 $m$ 为 MAR 斜率，$\omega_0$ 为中央凹基础 MAR 值。斜率 $m$ 越大，表示可容忍的周边模糊越强。实验通过 2AFC 范式测量受试者在不同注意力条件下对注视点模糊的辨别阈值，估计各条件的 MAR 斜率。

#### 计算增益分析

基于测得的 MAR 斜率，利用简化注视点渲染模型（Guenter et al., 2012 的算法）分析带宽节省潜力。计算增益定义为原始像素采样密度与注视点渲染后保留的像素采样密度之比：

$$\Psi(\mathrm{FOV}) = \left( \int_{\mathrm{FOV}} 1 \, dx \right) \cdot \left( \int_{\mathrm{FOV}} \max\left( \frac{\omega(x)}{\omega_s}, 1 \right)^{-2} dx \right)^{-1}$$

其中 $\omega_s$ 为显示器的峰值 MAR，$\omega(x)$ 为位置 $x$ 处的局部 MAR 阈值。该公式的核心逻辑是：在满足局部感知阈值约束的前提下，尽可能降低周边区域的采样密度，从而减少总体渲染计算量。

### 模块间因果关系

整个方法链的因果逻辑如下：

1. **注意力调制**（RSVP 任务难度）→ 周边注意力资源分配减少 → **对比度阈值升高**（心理物理学实验测量）
2. 对比度阈值升高 → **注意力增益 $g_a(e)$ 增大** → CSF 敏感度 $S_a$ 降低（通过 $1/g_a(e)$ 缩放）
3. CSF 敏感度降低 → **可容忍的 MAR 斜率 $m$ 增大** → 注视点模糊可施加更强
4. MAR 斜率增大 → **局部采样密度可降低更多** → 渲染带宽节省增加

这一因果链的核心创新在于将注意力状态作为注视点渲染的可控变量引入，使得渲染系统可以根据用户当前的注意力分配动态调整模糊程度，而非依赖固定的离心率依赖曲线。

![[assets/figures/papers/paper_list_l6_https_www_computationalimaging_org_publications_attention_aware/figures/003_Figure_2.jpg]]
*Figure 2: Photograph of the user study setup. The inset shows an enlarged illustration of the stimulus on the screen; the central RSVP letter task with the Gabor patches centered at ?? to the left and right. The brightness of the letter T has been exaggerated for visibility*

![[assets/figures/papers/paper_list_l6_https_www_computationalimaging_org_publications_attention_aware/figures/009_Figure_6.jpg]]
*Figure 6: Computational gain analysis as a fraction of original and retained pixel sampling density depending on pixel size and the covered visual field (horizontal axis). Note the difference in the gain axes scales*

## 实验与关键发现

### 核心实验框架

本文通过两个递进式用户实验建立注意力感知模型的有效性：**主实验**测量不同注意力条件下对比度阈值随离心率的变化，**注视点渲染实验**验证该模型在实际注视点模糊可接受度预测中的增益。两组实验均采用心理物理学标准范式，通过调节中央凹RSVP任务难度（低/中/高）控制注意力分配。

**主实验**使用2AFC QUEST自适应阶梯法测量Gabor斑块的对比度辨别阈值，刺激参数见表1（离心率7°、14°、21°，空间频率2 cpd，直径按皮质放大因子缩放）。**注视点渲染实验**则采用双刺激强制选择范式，让被试判断四幅自然图像（Tulips、City、Mountain、Forest）中哪一侧被施加了注视点模糊，通过QUEST程序搜索不可感知的MAR斜率阈值。

### 主实验结果：注意力对对比度阈值的显著调制

主实验的核心发现是**注意力状态对周边对比度阈值存在显著且离心率依赖的调制效应**。

在中等注意力条件下，对比度阈值随离心率显著升高：7°处升高约2倍，21°处升高超过3倍（Fig. 3a）。高注意力条件下该效应更为剧烈，阈值升高最高达4倍（Fig. 3b）。三种注意力状态间的差异在大多数配对比较中达到统计显著（p < 0.01），且效应量随离心率增大而扩大。

从绝对数值看（Table 3），以刺激3（21°离心率）为例：低注意力下平均阈值为0.0314，高注意力下跃升至0.1368，增幅约4.4倍。这一量级差异直接支撑了核心主张——当用户注意力集中于中央凹任务时，周边视野的对比度敏感性大幅下降，为更激进的注视点模糊提供了感知空间。

### 模型拟合与统一化

基于测量数据，本文对每个注意力条件独立拟合了平方根模型 $t_a(e) = p_0 \sqrt{e} + p_1$（Eq. 1），拟合参数及确定系数见Table 2。低注意力条件的 $R^2 = 0.705$，中注意力 $R^2 = 1.000$，高注意力 $R^2 = 0.956$，表明平方根形式在测量范围内具有良好解释力。

进一步通过插值参数 $\gamma$ 将离散注意力水平统一为连续函数 $t(e, a_c)$（Eq. 4），统一模型的自由度调整后 $R^2 = 0.973$，拟合曲线与实测数据在测量误差范围内吻合（Fig. 3a虚线）。注意力增益 $g_a(e) = t_a(e) / t_{\mathrm{low}}(e)$ 在21°处达到约4.4（高注意力）和约3（中注意力），且增益随离心率单调递增。

### 正交性验证实验

为验证“注意力增益与CSF其他维度正交”这一关键假设，本文在4组新刺激参数（不同空间频率、尺寸、亮度，见Table 1下半部分）上重复测量。结果（Fig. 4c）表明，所提注意力感知模型的阈值预测误差在刺激4和5上显著低于原始StelaCSF（p < 0.05），支持正交缩放策略的有效性。

**但正交性并非完全成立**：在较高适应亮度下（116 cd/m²），中注意力增益从3.03降至2.15（p < 0.05），提示亮度与注意力存在交互作用。这意味着在高动态范围场景中，简单正交缩放可能高估注意力效应，需谨慎外推。

### 注视点渲染实验：MAR斜率与质量预测

注视点渲染实验的核心指标是**MAR斜率** $m$（Eq. 5: $\omega(e) = m e + \omega_0$），斜率越高表示用户可容忍更强的周边模糊。

四幅图像在三种注意力条件下的平均MAR斜率（Table 4）为：
- **低注意力**：0.0198
- **中注意力**：0.0420（约为低注意力的2.1倍）
- **高注意力**：0.0596（约为低注意力的3.0倍）

中注意力和高注意力下的MAR斜率均显著高于低注意力（p < 0.001，Fig. 5d），直接验证了核心假设：注意力集中于中央凹时，用户可接受更强的注视点模糊而不感知质量下降。

### 预测器对比：注意力感知模型 vs. 原始FovVideoVDP

将注意力感知CSF集成到FovVideoVDP后，修改后的预测器在MAR斜率预测上显著优于原始版本（Fig. 5d）。除“Mountain”图像外（p < 0.05），其余三幅图像的预测误差均达到p < 0.01的显著性水平。视觉差异图（Fig. 5c）也显示修改后的预测器产生的JOD分布更接近实测阈值。

值得注意的是，原始FovVideoVDP系统性低估了可接受的模糊程度——这与论文的核心论点一致：基于传统CSF（假设周边高注意力）的模型过于保守，无法充分利用注意力集中时的感知冗余。

### 计算增益分析

基于测得的MAR斜率，本文使用简化注视点渲染模型（Eq. 8）估算了带宽节省潜力。在16K显示器、120°视场条件下：
- 低注意力（传统假设）：保留约15%像素
- 高注意力（本文发现）：保留约5%像素

这意味着**注意力感知方法可在传统注视点渲染基础上额外节省约3倍的计算量**。增益随显示器分辨率和视场增大而更加显著（Fig. 6），因为高分辨率下周边采样密度受MAR限制更明显。

### 失败模式与适用边界

本文坦诚报告了若干重要限制：

1. **受试者数量有限**（n=10）：虽符合类似心理物理学研究惯例，但个体差异较大（Fig. 8），群体趋势的泛化性需更大样本验证。

![[assets/figures/papers/paper_list_l6_https_www_computationalimaging_org_publications_attention_aware/figures/011_Figure_8.jpg]]
*Figure 8: Contrast thresholds measured for individual subjects (thin lines) in our main study that were used to fit our model (thick lines). For clarity, the attention levels are plotted together in the first panel and separately in the other panels. Mean thresholds for each plot line were rescaled to match the respective global attention level means in order to remove subject-specific variation of the base sensitivity and highlight the variation among attention levels and eccentricities*

2. **离心率范围受限**（7°–21°）：模型在近中央凹（<7°）和远周边（>21°）的外推缺乏实验支撑。21°以上注意力增益是否继续增长或趋于饱和尚不可知。

3. **正交性假设在特定条件下减弱**：高亮度下注意力增益下降（2.15 vs. 3.03），说明亮度与注意力存在交互，简单缩放可能引入系统偏差。

4. **注视点渲染模拟简化**：实验使用高斯模糊近似注视点渲染，未采用实际渲染管线（如Guenter et al. 2012），且未考察时域效果（运动模糊、刷新率降低等）。

5. **内容依赖性未建模**：不同自然图像的MAR斜率存在差异（Table 4），低注意力下内容特征仍影响感知阈值，本文未提出内容自适应机制。

6. **无实时注意力测量方案**：模型假设已知注意力分布，但实际部署需结合眼动追踪或隐性注意力推测技术，该环节完全留待未来工作。

![[assets/figures/papers/paper_list_l6_https_www_computationalimaging_org_publications_attention_aware/figures/007_Table_1.jpg]]
*Table 1: (same as our model study in Sec. 3.3). (b) Slices of the same models describing dependency on spatial frequency for the conditions used in our validation study (see No. 4–7 in Table 1). The points denote directly measured sensitivities scaled relative to the baseline. The bars are 95% confidence intervals. (c) Corresponding threshold prediction errors of StelaCSF vs. our model (lower is better). The error bars are 95% confidence intervals and significance is indicated at the*

## 定位与知识库关联

本文的核心贡献在于为注视点渲染的视觉感知模型引入了一个此前被忽视的维度——**注意力调制**。其定位不是提出新的渲染算法，而是修正渲染管线的感知准则层，从根本上改变了“可接受模糊量”的上限。

### 改变的插槽：对比度敏感度函数的注意力增益项

在注视点渲染的知识框架中，现有工作依赖的基础视觉模型是**离心率依赖的对比度敏感度函数（CSF）**，典型代表为 **StelaCSF**（Mantiuk et al., 2022）。该模型将对比度敏感度建模为 $S(e, f_s, L, \cdots)$，即仅考虑离心率 $e$、空间频率 $f_s$、亮度 $L$ 等因素，隐含假设了用户对周边视野投入的注意力资源恒定且充足。

本文精确地识别并替换了这一假设：将 CSF 插槽从“注意力恒定的离心率模型”替换为“注意力感知的离心率模型”。具体而言，在现有 StelaCSF 基础上引入一个**注意力增益函数** $g_a(e)$ 作为正交缩放因子：

$$S_a(e, \cdots) = S(e, \cdots) \cdot \frac{1}{g_a(e)}$$

其中 $g_a(e) = t_a(e) / t_{\text{low}}(e)$，表示相对于低注意力基线，对比度阈值在离心率 $e$ 处的升高倍数。这一插槽的改变是正交的——作者通过验证实验证明，注意力增益与空间频率、刺激尺寸、亮度等其他 CSF 维度具有较好的独立性（Fig. 4c），因此可作为缩放因子直接集成到现有 CSF 模型中，而无需重新训练整个模型。

随后，该注意力感知 CSF 被集成到注视点渲染质量预测器 **FovVideoVDP**（Mantiuk et al., 2021）中，替换其原始的 StelaCSF 组件，从而将注意力调制效应传递到最终的注视点渲染质量判断和最优 MAR 斜率预测中。

### 知识库挂载点：感知驱动的图形渲染

本文在知识库中的挂载点位于**感知图形学**与**视觉注意**的交叉节点。具体连接路径如下：

1. **上游连接——注视点渲染的感知准则**：注视点渲染技术（如 **Guenter et al., 2012** 的注视点渲染算法）依赖 CSF 模型来确定周边视野可接受的最大模糊程度。本文修正了这一准则层的输入假设，使得渲染带宽节省的上限从“保守的离心率依赖”提升到“注意力状态依赖”。

2. **上游连接——视觉注意的心理物理学**：经典注意研究已证实，对中央凹任务的注意力集中会降低周边视野的感知敏感性。但此前的注视点渲染工作并未将这一效应量化为可嵌入渲染管线的解析模型。本文通过 RSVP 任务操纵注意力负荷，首次建立了 $t(e, a_c)$ 的连续函数映射，填补了从注意理论到图形渲染的工程化空白。

3. **下游影响——渲染带宽节省的重新标定**：基于所测 MAR 斜率（低注意力 0.0198，高注意力 0.0596，约 3 倍提升），本文的计算增益分析（Eq. 8, Fig. 6）表明，在高注意力条件下渲染带宽节省可达低注意力条件的数倍。这为注视点渲染的实际部署提供了新的上限参考。

### 适用边界与局限

本文模型的适用边界需谨慎界定：

- **离心率范围受限**：模型拟合仅基于 7°–21° 的测量数据，外推到更近中央凹或更远周边区域时缺乏实验支撑。
- **刺激参数覆盖有限**：验证实验虽测试了不同空间频率和亮度，但模型的核心参数（主实验）仅使用 2 cpd 空间频率的 Gabor 斑块，对高频纹理或复杂自然场景的泛化性需进一步验证。
- **注意力正交性假设**：在高亮度条件下（116 cd/m²），注意力增益从 3.03 降至 2.15（p<0.05），表明正交性并非完全成立。在极端亮度或特定刺激参数下，注意力与 CSF 其他维度的交互效应可能不可忽略。
- **时域维度缺失**：当前模型仅处理空间对比度敏感度，未涉及注意力对时域敏感度（如闪烁感知、运动模糊）的影响，这限制了其在视频注视点渲染中的应用。
- **注意力测量缺口**：本文未提供实时注意力估计方案。实际部署需结合眼动追踪、瞳孔测量或任务上下文推断等外部机制来获取当前注意力状态——这是一个尚未解决的关键工程问题。

### 后续研究启发

本文为以下研究方向提供了直接的起点：

1. **实时隐性注意力估计**：如何在不干扰用户的前提下，从眼动特征、瞳孔反应或场景显著性中推测当前注意力分配，是将本模型推向实时 VR/AR 系统的首要障碍。

2. **内容自适应扩展**：实验显示不同自然图像的 MAR 斜率存在差异（Table 4），暗示图像内容本身影响注意力的调制效应。将内容特征（如纹理复杂度、语义显著性）纳入模型，有望进一步提升注视点渲染的效率。

3. **时域注意力感知模型**：将当前的空间 CSF 注意力调制框架扩展到时间频率维度，建立统一的时空注意力感知视觉模型，可直接影响注视点刷新率控制和运动模糊管理。

4. **与注视点渲染算法的深度集成**：当前验证使用简化高斯模糊模拟，未来可将注意力感知 CSF 嵌入基于对比度增强或噪声掩蔽的更先进注视点渲染管线中，验证实际渲染质量与带宽节省的联合优化效果。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/Towards_Attention_Aware_Foveated_Rendering.pdf]]