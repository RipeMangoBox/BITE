---
title: "Ecoclimates: Climate-response Modeling of Vegetation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Ecoclimates_Climate_response_Modeling_of_Vegetation.pdf
project_link: "https://storage.googleapis.com/pirk.io/projects/ecoclimates/index.html"
code_link: null
aliases:
- Ecoclimates
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 通过建立一个耦合连续PDE（土壤水文、大气云形成）和离散图（植被生长）的混合模型，并利用水蒸气图和降水图动态交换反馈信息，从而实现植被-土壤-大气之间的局部双向耦合。
primary_logic: 将个体植物几何生长、土壤水文循环和大气云动力学显式耦合，使得水、温度和光照的局部梯度能够驱动自组织植被模式，从而涌现出丰富的生态气候现象。
claims:
- 加入微气候反馈后，模型能够重现生态学文献中观察到的空间植被模式（如间隙、条带和斑点），与 Meron 2019 的分析研究一致。
- 森林砍伐实验表明，移除植被会减少局部云量，而植被恢复后云量回升，证实了植被-大气反馈循环的存在。
- 与 Makowski et al. 2019 的基线相比，在微气候启用时，物种沿高程梯度分布并出现合作现象，而基线模型仅产生均匀生长，未能捕捉地形效应。
- 不同气候条件下的森林消亡与恢复（Half Dome scene） 上 植被分布模式（定性） = 降低宏观水蒸气导致带条状结构和严重森林消亡
---

# Ecoclimates: Climate-response Modeling of Vegetation

> [!tip] 核心洞察
> 将个体植物几何生长、土壤水文循环和大气云动力学显式耦合，使得水、温度和光照的局部梯度能够驱动自组织植被模式，从而涌现出丰富的生态气候现象。

| 字段 | 内容 |
|------|------|
| 中文题名 | 生态气候：植被的气候响应建模 |
| 英文题名 | Ecoclimates: Climate-response Modeling of Vegetation |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://storage.googleapis.com/pirk.io/projects/ecoclimates/index.html) · [Project](https://storage.googleapis.com/pirk.io/projects/ecoclimates/index.html") |
| Topic | #topic/other_unclear |
| Method | Ecoclimates: Climate-response Modeling of Vegetation |
| Dataset | 不同气候条件下的森林消亡与恢复（Half Dome scene）, 与 Makowski et al. 2019 的微气候比较 |

> [!tip] 效果简介
> - 不同气候条件下的森林消亡与恢复（Half Dome scene） 上，植被分布模式（定性） 降低宏观水蒸气导致带条状结构和严重森林消亡 vs 恒定气候下的密集松林 (涌现出气候导致的森林结构变化)。
> - 森林砍伐与植被-大气反馈（热带雨林） 上，积云形成（定性） 砍伐后云量减少，恢复后云量回升 vs 未砍伐的雨林有积云 (证实双向反馈)。
> - 与 Makowski et al. 2019 的微气候比较 上，植被空间模式真实性 微气候启用：物种沿高程梯度分布，出现合作现象 vs 微气候禁用：均匀生长，无地形效应 (显著提高生态合理性)。

## 概要

传统植被模拟仅在宏观气候尺度上驱动生长，忽略了植被与局部天气的双向反馈（微气候效应），因而无法涌现森林边缘效应、焚风效应和空间植被斑图等复杂生态现象。本文提出**生态气候（Ecoclimates）模型**，将基于模块的植物几何生长、土壤水文循环和大气云动力学显式耦合，通过水蒸气图和降水图在离散图与连续PDE之间动态交换反馈信息，实现植被-土壤-大气之间的局部双向耦合。实验表明，启用微气候反馈后，模型能够重现生态学文献中观察到的间隙、条带和斑点状空间植被模式，并在森林砍伐实验中验证了植被-云量反馈循环的存在。与Makowski et al. 2019的基线相比，微气候使物种沿高程梯度分布并涌现合作现象，而基线仅产生均匀生长。该方法以交互式速率支持超过50万株植物的个体几何模拟，为图形学领域提供了首个能够捕捉局部水-温-光梯度驱动自组织植被模式的生态气候建模框架。

## 核心方法与创新机理

### 问题瓶颈：从宏观气候到微气候反馈的缺失

传统植被模拟方法（如 **Makowski et al. 2019**）仅在宏观气候尺度上驱动植物生长——使用全局月平均温度和降水作为输入，植被被动响应这些均匀的气候信号。这种单向驱动模式忽略了一个关键的生态学事实：植被与局部天气之间存在双向反馈，即**微气候效应**。当植被通过蒸腾向大气释放水汽、通过冠层阴影改变地表温度、通过根系促进土壤水渗透时，局部的水、热和光照梯度会发生显著改变，进而反向影响植被自身的生长和分布。忽略这一反馈循环，导致传统模型无法涌现出生态学文献中广泛记载的复杂现象，包括森林边缘效应、焚风效应、空间植被斑图（间隙、条带、斑点）以及物种沿地形梯度的合作与竞争。

本文的核心洞察在于：**将个体植物几何生长、土壤水文循环和大气云动力学进行显式耦合**，使得水、温度和光照的局部梯度能够驱动自组织植被模式，从而涌现出丰富的生态气候现象。这一耦合并非简单的模型拼接，而是通过精心设计的时空映射机制，在连续PDE（描述流体和土壤物理）与离散图（描述植物生长）之间建立双向信息通道。

### 框架总览：三模型耦合架构

Ecoclimates框架由三个核心模型组成，通过水循环实现闭环反馈（图2、图6）：

1. **植被模型（Vegetation Model）**：基于模块的植物生长模型，扩展自Makowski et al. 2019，响应局部光照、温度和土壤水，输出植物几何结构和蒸腾量。
2. **土壤模型（Soil Model）**：土壤水文模型，处理地表水渗透、土壤水扩散、植物水分吸收和径流，实现植被-土壤耦合。
3. **大气模型（Atmosphere Model）**：基于扩展的Kessler方案（Hädrich et al. 2020）的天气模型，模拟云形成、降水和水汽输运，接收植被的蒸腾反馈。

三个模型运行在**两个时间尺度**上（图7）：植被生长和土壤水循环以**月**为步长（$\Delta t_E = 1$月），而天气模拟以**10秒**为步长运行若干天，生成月平均降水量图和水汽图。这种双时间尺度设计使得计算成本可控，同时保留了天气动力学的关键特征。

### 数学空间与耦合机制

框架使用四种数学空间实现不同模型间的信息交换（图5）：

- **生态系统连续空间**：嵌入地形表面和植被网格，用于3D渲染。
- **生态系统体素空间**：分辨率1.5m的3D网格，存储温度和光照信息，为植被生长提供局部环境参数。
- **水汽图和降水图**：2D网格，作为植被/土壤模型与天气模型之间的数据交换中介。
- **天气体素空间**：分辨率20m的3D网格，用于云动力学计算。

**耦合的核心通道**是水汽图和降水图（图9）。每个生态模拟月，系统首先从植被模型计算水汽图（蒸腾贡献），输入天气模型；天气模型运行数天后生成降水量图，反馈给土壤模型更新土壤水；土壤水再被植被模型读取，影响下一个月的生长决策。这一循环实现了完整的植被-土壤-大气反馈。

### 关键Changed Slots与创新机理

#### Slot 1：气候适应参数的局部化（从全局到局部）

基线方法（Makowski et al. 2019）使用全局月平均温度$T_A$和降水$P_A$来计算气候适应参数，决定植物的播种间隔。本文将其替换为来自**生态系统体素空间**的局部值：

$$o = \frac{N_T(T) \cdot N_P(q_w)}{N_T(T_A) \cdot N_P(P_A)}$$

其中$T$为植物所在体素的局部温度，$q_w$为局部土壤水含量，$N_T$和$N_P$分别为温度和土壤水的归一化函数。这一改变使得同一地形上不同位置的植物接收到不同的气候信号，从而能够响应地形引导的微气候梯度。

#### Slot 2：蒸腾反馈通道（从无反馈到双向耦合）

基线中天气模型单向驱动植被，植被不向大气返回水汽。本文引入**蒸腾反馈**：植物根据其模块总质量$M_m$计算水汽贡献：

$$M_m = \sum_{u \in U} \sum_{c \in C_b} \ell_b (2 d_b)^2 \pi \rho$$

$$E_{\hat{p}} = \tau \sum_{u \in U} M_{m,u}$$

其中$\ell_b$为枝段长度，$d_b$为枝段直径，$\rho$为木材密度，$\tau$为蒸腾系数。所有模块的水汽贡献被投影到2D水汽图上，作为天气模型中水汽输运方程的源项：

$$\mathsf{D}_t q_v = -C_c + E_c + E_r + E_{\hat{p}} + E_M$$

云水输运方程为：

$$\mathrm{D}_t q_c = C_c - E_c - A_c - K_c$$

其中$C_c$为凝结率，$E_c$为蒸发率，$A_c$为自动转化率，$K_c$为碰并率，$E_M$为宏观气候水汽输入。这一反馈通道是涌现微气候效应的关键——植被的生物量直接影响局部云量和降水分布。

#### Slot 3：土壤渗透的植被促进效应

土壤模型引入植物密度促进渗透的机制。土壤水变化方程包含植被促进渗透项：

$$\Delta q_w = \text{rainfall} - \text{evapotranspiration} - q_o + \text{infiltration enhancement}$$

其中渗透增强项与局部植物密度正相关。降水量图$R$由天气模型的雨水总量投影得到：

$$R = \sum_{q_r \in Q_r} q_r$$

这一设计使得植被不仅消耗土壤水，还通过改善土壤结构促进降水渗透，形成正反馈——植被越多，土壤保水能力越强，进一步支持更多植被生长。这一机制是涌现空间斑图和物种合作现象的基础。

### 模块间的因果链与涌现逻辑

三个模型的因果链可以概括为：

1. **植被→大气**：植物生物量通过蒸腾系数$\tau$转化为水汽图$E_{\hat{p}}$，作为天气模型的水汽源项，影响云形成和降水分布。
2. **大气→土壤**：天气模型输出的降水量图$R$驱动土壤模型的地表水输入，影响渗透和土壤水含量$q_w$。
3. **土壤→植被**：局部土壤水$q_w$和温度$T$通过气候适应参数$o$影响植物的播种和生长决策，决定生物量分布。
4. **植被→土壤（正反馈）**：植物密度促进土壤渗透，增加有效土壤水，形成自增强循环。

这一因果链使得系统能够涌现出丰富的空间模式：当宏观水汽$E_M$降低时，降水减少，土壤水下降，植被稀疏化，蒸腾减弱，进一步减少局部降水——形成干旱化正反馈，导致森林带状枯死（图12）。反之，在湿润条件下，植被-降水正反馈可以维持茂密森林。这种非线性动力学与Meron 2019的分析模型预测的斑图转变（间隙→条带→斑点）定性一致（图20）。

### 方法边界与简化假设

需要指出，本方法的目标是**轻量级、交互式的生态气候建模**，而非高保真物理仿真。因此做了以下简化：
- 忽略昼夜温度循环和精确辐照度模式，仅使用月平均温度。
- 仅考虑单一土壤类型，不涉及土壤分层和复杂地下水流。
- 天气体素分辨率为20m，可能忽略细粒度湍流效应。
- 蒸腾系数$\tau$为全局常数，未区分不同物种的蒸腾策略差异。

这些简化使得系统能够在交互速率下模拟超过50万株具有独立几何的植物（表2），但限制了日尺度微气候模拟的真实性。

![[assets/figures/papers/paper_list_l33_https_storage_googleapis_com_pirk_io_projects_ecoclimates_index_html/figures/002_Figure_2.jpg]]
*Figure 2: Framework overview: we employ models for vegetation, soil, and weather to simulate ecoclimates. Our system operates at interactive rates and thereby allows users to efficiently explore configurations and parameters settings for plant species, terrain, and climate*

![[assets/figures/papers/paper_list_l33_https_storage_googleapis_com_pirk_io_projects_ecoclimates_index_html/figures/006_Figure_6.jpg]]
*Figure 6: Detailed overview of our ecoclimate model. Our model can be distinguished by a vegetation (a), soil (b), and weather model (c). We explicitly describe the water cycle which mediates the feedback between the three models. While the weather model describes dynamic cloud formation over time scales of seconds the vegetation and soil model describe phenomena occurring on time scales of months. A user provides input in the form of a set of plant species, a digital elevation model and data describing macroclimatic variation over time. A description of the processes that our model is able describe and the underlying hypotheses expressed by our ecoclimate model is given in Section 5.3*

![[assets/figures/papers/paper_list_l33_https_storage_googleapis_com_pirk_io_projects_ecoclimates_index_html/figures/004_Figure_4.jpg]]
*Figure 4: We use the monthly average temperature (red) and precipitation (blue) as input to our framework. Two different temperature and precipitation graphs for San Diego and Juno shown as example inputs*

## 实验与关键发现

### 主要结果：微气候反馈驱动空间植被模式

系统的核心实验围绕“微气候反馈是否产生生态学上合理的自组织植被模式”展开。作者首先在 **Half Dome 地形**上进行了气候变化模拟（Fig. 12）。初始条件下，场景生长为密集松林；当宏观水蒸气输入降低后，植被并非均匀衰退，而是涌现出**带状枯死结构（ribbon-like dieback）**，最终演变为稀疏的干旱景观。这种空间异质性在传统全局气候驱动的模型中无法出现，其成因链为：局部水蒸气减少 → 降水下降 → 土壤水梯度分化 → 植被沿地形等高线差异化衰退 → 植被蒸腾反馈进一步放大局部干旱。

在**热带雨林砍伐实验**中（Fig. 16），作者保持宏观气候恒定，仅移除大片植被。砍伐后，被砍伐区域上空的积云形成显著减少；随着植被逐步恢复，云量逐渐回升至原有水平。该实验直接证实了**植被→蒸腾→云形成**的反馈循环的存在，是全文最具因果说服力的证据。其定量意义在于：即便宏观气候参数不变，局部植被结构变化也能通过水汽通量（Eq. 5 中的 $E_{\hat{p}}$）改变大气边界条件，进而影响云动力学。

![[assets/figures/papers/paper_list_l33_https_storage_googleapis_com_pirk_io_projects_ecoclimates_index_html/figures/016_Figure_16.jpg]]
*Figure 16: Our method models the feedback between vegetation, soil, and weather. To illustrate this, we conduct a deforestation experiment while keeping the macroclimate in our weather model constant. In (a) we show a tropical rainforest with cumulus clouds. In (b) we remove a large portion of the rainforest thereby modifying the vapor emission from the terrain. Consequently, fewer cumulus clouds form, especially over the deforested area. After continuing ecosystem growth cloud formation increases slightly (c). Only after significant portions of the rainforest have regrown, cumulus cloud formation is restored (d). Please note that clouds in the images are rendered at low altitudes for visualization pu...*

### 与基线方法的对比

与 **Makowski et al. 2019** 的对比是关键的消融实验（Fig. 15）。该基线使用全局月平均温度和降水驱动植被生长，不包含任何局部反馈。实验设置了一个包含耐旱绿叶物种和黄叶物种的混合生态系统，在相同地形上分别启用和禁用微气候：

![[assets/figures/papers/paper_list_l33_https_storage_googleapis_com_pirk_io_projects_ecoclimates_index_html/figures/015_Figure_15.jpg]]
*Figure 15: Comparison to [Makowski et al. 2019]: Temporal progression of a developing ecosystem composed of a drought-adapted green-leaved and a yellowleaved species generated with microclimates (a-d) and without microclimates (e-h). The inclusion of microclimates allows for more realistic patterning of vegetation at the slopes of the terrain capturing geomorphic effects. Additionally, patterns of self-organization emerge as the yellow-leaved species establishes itself primarily in the valleys of the terrain after water infiltration is sufficiently improved through the presence of the green-leaved species (top row): a case of plant cooperation (d and h, inset)*

- **微气候启用**（Fig. 15a-d）：绿叶物种率先在山坡定殖，通过根系促进水分渗透（Eq. 7 中的植被促进渗透项），改善山谷土壤水条件，随后黄叶物种在山谷中建立种群——这是一个典型的**植物合作（plant cooperation）**涌现现象。物种沿高程梯度呈现清晰的空间分异。
- **微气候禁用**（Fig. 15e-h）：两个物种均匀混合生长，无法反映地形引导的分布，也无合作涌现。

该对比的因果机制明确：微气候启用时，局部温度 $T$ 和土壤水 $q_w$ 来自 Ecosystem Voxel Space 的局部采样（Eq. 1 中的 $o$ 参数），使每株植物的生长适应其微环境；而基线使用全局均值 $T_A$ 和 $P_A$，抹平了所有空间梯度。

### 空间斑图与生态学文献的定性验证

作者进一步将模拟结果与 **Meron 2019** 的分析研究进行了系统对比（Fig. 20）。通过仅改变宏观水蒸气参数 $E_M$，模型成功重现了三种经典空间植被斑图：**间隙（gap）、条带（stripe）和点状（spot）**模式。其物理机制为：$E_M$ 控制大气水汽总量 → 影响降水空间分布 → 改变土壤水梯度 → 植被自组织为不同斑图形态。这一结果与 Meron 的数学分析模型定性吻合，为模型的生态合理性提供了独立验证。

![[assets/figures/papers/paper_list_l33_https_storage_googleapis_com_pirk_io_projects_ecoclimates_index_html/figures/020_Figure_20.jpg]]
*Figure 20: Our results correspond to the recent analytical study performed in ecology research (top row, adapted from [Meron 2019], Fig. 5) which highlights morphological transitions (black and white panels) between gap, stripe and spot patterns (green panels). Our method simulates similar spatial vegetation patterns obtained by different the macroscopic vapor*

此外，在**焚风效应**实验中（Fig. 18-19），迎风面因绝热冷却产生较多降水，冷适应物种占据优势；背风面因焚风增温而干燥，仅出现暖适应物种。这一物种组成差异直接源于风-地形-降水-温度的耦合链，是传统模型无法捕捉的微气候风效应。

### 关键参数消融

**天气采样天数**的消融（Fig. 26 底部）表明：仅采样 1 天天气时，降水量图出现斑块状空洞，部分区域无降水记录；采样天数增加至 30 天后，降水量图趋于平滑且空间梯度连续。这验证了双时间尺度策略（Fig. 7）的必要性——通过多日天气采样取平均，才能为月尺度的生态系统模拟提供稳定的水文输入。计算开销方面（Fig. 26 左上），模拟步长时间随采样天数线性增长，在 65K 植物规模下可保持交互式性能（Table 2 中典型场景的 TS 值在数十秒量级）。

### 失败模式与适用边界

论文明确指出了若干限制。首先，模型**忽略了昼夜温度循环和精确局部辐照度**，这意味着日尺度的微气候动态（如清晨露水形成、午后热应力）无法被捕捉。其次，**仅支持单一均质土壤类型**，未考虑土壤分层、不同质地（砂土/黏土）的水力特性差异，这限制了在复杂土壤景观中的适用性。天气模拟的**体素分辨率为 20 米**，无法解析细粒度湍流和局地对流，可能导致小尺度云形成过程失真。

验证层面，所有对比均为**定性视觉比较**（与生态学文献照片或分析模型图示），缺少大规模定量数据集的统计验证。例如，Fig. 23 展示了模拟结果与尼日尔干旱生态系统、西伯利亚泥炭地的照片并列，但未提供斑图特征（如斑块大小分布、聚集指数）的定量匹配指标。作者明确指出“目标不是高保真物理仿真，而是轻量级、交互式的生态气候建模”，因此这些限制在设计预期之内，但读者在评估模型对特定生态假说的验证能力时应保持审慎。

## 定位与知识库关联

### 相对于已有方法的本质差异与改变的“槽位”

本文的核心贡献在于将传统生态模拟中**单向的宏观气候驱动**替换为**植被-土壤-大气双向耦合的微气候反馈**。具体而言，相对于基线工作，本文改变了以下关键槽位：

1.  **气候适应参数的输入源**：基线方法 **Makowski et al. 2019** (ACM Trans. Graph.) 使用全局月平均温度和降水作为植物生长的气候适应参数输入。本文将其替换为从 **Ecosystem Voxel Space** 中采样的局部温度 $T$ 和土壤水含量 $q_w$，使得每一株植物的生长决策都响应其所在位置的即时微环境（Eq. (1), Sec. 5.5）。这一改变是涌现地形引导的植被分布和空间斑图的根本原因。

2.  **从植被到大气的蒸腾反馈**：在基线方法中，天气模型单向驱动植被生长，不存在反向通道。本文在植物模块中计算生物量 $M_m$，并乘以蒸腾系数 $\tau$ 生成水汽值 $E_{\hat{p}}$（Eq. (5), Sec. 5.5.1），投影到水蒸气图上，作为天气模型的水汽源项 $E_{\hat{p}}$ 输入（Eq. (10)）。这一**水汽反馈闭环**是涌现森林砍伐后云量减少、恢复后云量回升等双向耦合现象的关键。

3.  **土壤水文中的植被促进渗透**：基线方法通常采用简单的地表径流或无土壤动态。本文引入包含植物密度促进渗透的项（Eq. (7), Sec. 5.6），使得植被的存在能够改善土壤水分入渗，进而形成植物合作涌现的机制——先锋物种改善土壤水分后，其他物种得以在谷地建立。

4.  **天气模型的地面边界条件**：基线天气模型 **Hädrich et al. 2020** (ACM Trans. Graph.) 使用固定或恒定的水汽和热量发射。本文将其替换为从水蒸气图和植被阴影效应动态计算的局部蒸发蒸腾和冷却（Eqs. (10)-(12), Sec. 5.7），实现了地面与大气之间的动态耦合。

### 知识库挂载点

本文的方法架构可挂载到以下知识库节点：

-   **生态模拟与植物建模**：直接继承自 **Makowski et al. 2019** 的基于模块的植物生长模型，保留了其自组织、模块重用和几何生成管线。本文在其上增加了微气候响应层，而非替换原有生长逻辑。
-   **大气科学与云模拟**：天气模型基于 **Hädrich et al. 2020** 扩展的 Kessler 方案，保留了云微物理和降水模拟的核心方程。本文的扩展在于将水蒸气图作为动态下边界条件注入，而非改变云物理本身。
-   **生态学理论**：空间植被斑图的涌现直接与 **Meron 2019** 的分析研究对话。Meron 通过简化数学模型预测了间隙、条带、斑点等斑图形态随水分梯度的转变，本文在基于个体的模拟中重现了这些模式（Fig. 20），为理论提供了计算验证。
-   **图形学中的自然现象模拟**：本文属于 SIGGRAPH/TOG 传统中“基于物理/过程的自然场景生成”脉络，与植被、地形、水体、大气等模拟工作并列。其独特挂载点在于首次将个体植物几何、土壤水文、大气动力学三者显式耦合。

### 适用边界与限制

本文方法适用于**景观尺度的生态气候现象可视化与探索**，而非高保真物理仿真或定量预测。其边界条件包括：

-   **时间尺度**：忽略昼夜循环和日间温度变化，仅以月为步长进行生态模拟，以秒为步长进行天气采样。这限制了日尺度微气候效应（如清晨露水、午后热浪）的模拟真实性。
-   **空间分辨率**：天气体素分辨率为 20 米，无法解析细粒度湍流和局部对流效应。
-   **土壤复杂性**：仅考虑单一土壤类型，未涉及土壤分层、地下水流或冻土过程。
-   **验证方式**：仅通过定性对比生态学文献中的照片和描述进行验证，缺乏大规模定量数据集的基准测试。

### 后续启发与可迁移价值

本文的架构设计为后续工作提供了明确的扩展接口：

1.  **气候适应参数的泛化**：当前的 $o$ 参数仅依赖温度和土壤水，可扩展至包含辐射、风速、养分等更多微气候变量，从而模拟更复杂的生态位分化。
2.  **双向耦合机制的迁移**：水蒸气图和降水图作为中间表示，实现了不同时间尺度和空间分辨率模型之间的解耦通信。这一“地图中介”的耦合策略可迁移至其他多物理场耦合场景（如植被-火、植被-动物迁移）。
3.  **计算生态学的工具化**：本文展示了利用个体植物几何进行微气候模拟的可行性，为测试具体的生态气候假说（如 Janzen-Connell 效应、海拔梯度上的物种边界移动）提供了可交互的计算沙盒。
4.  **与冰冻圈和土壤圈耦合**：作者明确提出的开放问题——将模型与不同土壤类型和冰冻圈结合——直接指向更完整的地球系统模拟，是自然的后续方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Ecoclimates_Climate_response_Modeling_of_Vegetation.pdf]]