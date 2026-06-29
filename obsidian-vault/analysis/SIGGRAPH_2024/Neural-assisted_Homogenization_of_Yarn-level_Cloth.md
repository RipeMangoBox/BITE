---
title: Neural-assisted Homogenization of Yarn-level Cloth
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Neural_assisted_Homogenization_of_Yarn_level_Cloth.pdf
project_link: null
code_link: null
aliases:
- NAH
- NAHYLC
tags:
- SIGGRAPH_2024
- topic/graphics_physical_simulation
core_operator: 采用神经网络表示超弹性本构模型，利用sigmoid激活函数的固有平滑性和三阶导数惩罚正则化，获得具有平滑二阶导数的应变能函数，从而保证隐式仿真的稳定性；训练后将网络“烘焙”为解析的Hermite插值函数以消除运行时推理开销。
primary_logic: 神经网络作为通用函数逼近器，无需精心选择解析函数即可天然保证应变能函数的高阶平滑性，突破传统插值方法在导数连续性上的局限，实现大时间步长下的稳定仿真。
claims:
- 二次展开误差E比HYLC模型降低20%-80%，表明本模型的应变能函数在泰勒展开时振荡更小。
- "增大三阶导数损失权重w^C（从0至10^{-3}）可将最大稳定时间步长从1/5000 s提升到1/30 s。"
- 在球体撞击和旗帜风吹场景中，本模型以Δt=1/30 s稳健运行，而HYLC模型在Δt=1/1000 s时即失败。
- 仿真针织T恤（14K顶点）达到15 FPS，相比HYLC模型实现至少两个数量级的加速。
---

# Neural-assisted Homogenization of Yarn-level Cloth

> [!tip] 核心洞察
> 神经网络作为通用函数逼近器，无需精心选择解析函数即可天然保证应变能函数的高阶平滑性，突破传统插值方法在导数连续性上的局限，实现大时间步长下的稳定仿真。

| 字段 | 内容 |
|------|------|
| 中文题名 | 神经辅助的纱线级布料均匀化 |
| 英文题名 | Neural-assisted Homogenization of Yarn-level Cloth |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://rullec.github.io/) |
| Topic | #topic/graphics_physical_simulation |
| Method | Neural-Assisted Homogenization |
| Dataset | T-shirt simulation, Stretching stockinette fabric strip, Quadratic expansion error, Hanging fabric stability |

> [!tip] 效果简介
> - T-shirt simulation (14K vertices) 上，FPS 15 FPS (@ Δt=1/30s) vs ≪1 FPS (HYLC 需要极小时间步长) (至少两个数量级加速)。
> - Stretching stockinette fabric strip (5cm×12cm) 上，Hausdorff distance to ground truth 0.69 cm (course) / 0.72 cm (wale) vs >1.0 cm (HYLC) (误差降低约30%以上)。
> - Quadratic expansion error (10K random samples) 上，Error E (lower is better) 6.28×10⁻⁴ (Basket); 4.05×10⁻⁴ (Stockinette) vs 1.31×10⁻³ (Basket); 2.67×10⁻³ (Stockinette) [HYLC] (降低52%~85%)。

## 概要

现有纱线级布料均匀化方法（如HYLC）采用Hermite插值构建应变能密度函数，其插值节点处二阶导数不连续，导致牛顿求解器在大时间步长下数值失稳，仿真步长被限制在约10⁻⁴ s量级，难以用于交互式应用。本文提出**神经辅助均匀化方法**，核心思路是用神经网络替代解析插值函数来表示超弹性本构模型：利用sigmoid激活函数的固有平滑性，辅以三阶导数惩罚正则化，获得具有平滑二阶导数的应变能函数，从而保证隐式仿真的数值稳定性；训练后将网络“烘焙”为解析Hermite插值函数以消除运行时推理开销。同时引入扇区并行热启动策略加速训练数据生成，并构建C²连续二次外推的安全机制处理域外应变。

实验表明，本模型可将最大稳定时间步长从HYLC的约1/1000 s提升至1/30 s（约33倍），在14K顶点的针织T恤仿真中达到15 FPS，相比HYLC实现至少两个数量级的加速；二次展开误差降低52%–85%，拉伸测试中与ground truth的Hausdorff距离降至约0.7 cm。方法定位上，本工作将均匀化流程中**应变能密度函数的表示**从手工设计的Hermite插值替换为可学习的神经网络，再通过烘焙回归解析形式，属于神经本构建模与经典仿真器的融合范式。

## 核心方法与创新机理

### 问题瓶颈：均匀化本构模型的导数不连续性

纱线级布料仿真能够捕捉织物细观结构（如针织、梭织图案）带来的各向异性力学行为，但其计算代价极高。均匀化方法将纱线级力学响应压缩为连续介质尺度的应变能密度函数，使宏观仿真器能以粗网格高效运行。然而，现有均匀化方法存在根本性缺陷：以 **HYLC**（Sperl et al., 2020）为代表的方案采用Hermite插值构建应变能密度函数，该插值在节点处仅保证C¹连续——其二阶导数（即刚度矩阵/Hessian）在节点处不连续，表现为分段常数函数的跳跃。

这一缺陷对隐式时间积分的牛顿求解器造成致命影响：当时间步长增大时，牛顿迭代需要在应变空间中跨越多个插值区间，不连续的Hessian导致迭代方向剧烈振荡，求解器发散。因此HYLC的时间步长被限制在约10⁻⁴秒量级，无法用于交互式应用（通常要求Δt ≥ 1/30秒）。**核心瓶颈**可概括为：解析插值函数无法同时保证能量函数的表达精度和高阶导数平滑性。

### 核心洞察：神经网络作为天然平滑函数逼近器

本方法的核心洞察在于：神经网络（特别是使用sigmoid激活函数的多层感知机）作为通用函数逼近器，其无限次可微的特性天然保证了应变能函数的高阶平滑性。无需精心设计解析函数形式，仅通过引入对三阶导数的显式惩罚，即可获得具有平滑Hessian的应变能密度函数，从而从根本上解决了牛顿求解器的数值稳定性问题。训练完成后，再将网络“烘焙”为解析的Hermite插值函数，消除运行时的神经网络推理开销，实现精度、稳定性与效率的三重统一。

### 框架总览：从纱线仿真到连续介质仿真的完整管线

方法包含五个顺序模块，形成从数据生成到实时仿真的完整闭环：

1. **纱线图案仿真（数据生成）**：对给定周期性纱线图案，通过受约束优化生成不同宏观应变下的纱线平衡构型，提取应变能密度作为训练数据。
2. **神经网络训练**：使用多损失函数训练MLP逼近1D和2D应变能分量。
3. **网络烘焙**：将训练好的网络转换为解析Hermite插值函数，消除推理开销。
4. **安全外推机制**：对训练域外应变值构建C²连续的二次扩展函数。
5. **连续介质布料仿真器**：基于隐式欧拉积分的宏观仿真器，直接使用烘焙后的本构模型。

### 关键Changed Slot 1：应变能密度函数表示——从Hermite插值到神经网络

这是本方法最核心的改变。HYLC将应变能密度函数Ψ(s)表示为定义在规则网格上的Hermite插值函数，而本方法将其替换为三层MLP（sigmoid激活函数），训练后再烘焙回Hermite插值形式。

**应变能分解策略**：为避免直接学习6D应变能函数带来的维度灾难，沿用HYLC的分解方案，将总应变能密度表示为常数项、拉伸项、1D弯曲项和2D弯曲项的组合：

$$\Psi(\mathbf{s}) = \Psi_0 + \Psi^{\mathrm{stretch}}(\mathbf{s}) + \Psi_{1D}^{\mathrm{bend}}(\mathbf{s}) + \Psi_{2D}^{\mathrm{bend}}(\mathbf{s})$$

其中宏观应变向量 **s** 由中间面的第一、第二基本形式定义：

$$\mathbf{s} = \left[ \sqrt{I_0} - 1 \quad \frac{I_1}{\sqrt{I_0 I_2}} \quad \sqrt{I_2} - 1 \quad \lambda_1 \quad \lambda_2 \quad c^2 \right]$$

每个1D和2D分量由独立的小型神经网络表示，训练数据来自纱线级仿真。

**训练损失函数设计**：总损失由四项加权组合：

$$L_{I}^{\mathrm{final}}(\mathbf{s}_{I};\epsilon) = w^{Z} L_{I}^{Z}(\mathbf{s}_{I}) + w^{F} L_{I}^{F}(\mathbf{s}_{I};\epsilon) + w^{C} L_{I}^{C}(\mathbf{s}_{I};\epsilon) + w^{S} L_{I}^{S}(\mathbf{s}_{I})$$

- **零阶预测损失** L^Z：网络预测能量与真实采样能量之间的均方误差：

$$L_{I}^{Z}(\mathbf{s}_{I}) = \frac{1}{M} \sum_{d=0}^{M} \left( \Psi_{I}^{d} - \hat{\Psi}_{I}(\mathbf{s}_{I}^{d}) \right)^{2}$$

- **一阶预测损失** L^F：通过有限差分近似一阶导数（即应力），惩罚网络梯度与真实梯度的偏差，确保参考构型（零应变处应力为零）的正确性。

- **三阶导数平滑损失** L^C：这是保证稳定性的关键创新。对1D函数，使用中心有限差分近似三阶导数并惩罚其幅度：

$$L_i^C(s_i; \epsilon) = \frac{1}{2\epsilon^3} \left| \hat{\Psi}_i(s_i+2\epsilon) - 2\hat{\Psi}_i(s_i+\epsilon) + 2\hat{\Psi}_i(s_i-\epsilon) - \hat{\Psi}_i(s_i-2\epsilon) \right|$$

该损失直接抑制能量函数的高频振荡，使Hessian平滑变化，从而保证牛顿求解器的收敛性。消融实验（Figure 4c）证实：将权重w^C从0提高到10⁻³，最大稳定时间步长从1/5000秒跃升至1/30秒。

- **应变集中损失** L^S：惩罚训练域外应变能函数的非单调下降，防止仿真中应变异常集中。

### 关键Changed Slot 2：数据收集——扇区并行热启动策略

纱线级仿真作为数据生成器，需要在大量宏观应变采样点上求解受约束优化问题。朴素方法对每个采样点从零开始仿真，计算代价极高。HYLC采用广度优先传播（BFS）策略，沿应变空间逐步传播解，但传播路径串行，效率有限。

本方法提出**基于极坐标的扇区并行热启动策略**（Figure 3）：将2D应变采样点按极坐标角度划分为多个扇区，每个扇区内按预定顺序逐步增加应变进行仿真，扇区之间完全并行。仿真每个新应变点时，使用同扇区内相邻已仿真点的纱线构型作为初始猜测（热启动），大幅减少优化迭代次数。该方法带来约一个数量级（~10×）的加速。

![[assets/figures/papers/paper_list_l26_https_rullec_github_io/figures/003_Figure_3.jpg]]
*Figure 3: Strain sample sectors. As shown in (a), we categorize 2D strain samples into multiple sectors.Within each sector, we gather training data by executing yarn pattern simulation.This process involves progressively increasing strains in a specific pre-defined sequence,as shown in (b)*

### 关键Changed Slot 3：域外应变处理——C²连续安全外推

神经网络仅在训练数据覆盖的应变域内有定义，而宏观仿真中应变可能超出训练范围。若不做处理，仿真将崩溃。本方法构建了**安全外推机制**：对训练域外的应变值，采用二次函数延拓，通过匹配边界点处的函数值、一阶导数和二阶导数，保证能量函数在整个应变空间内的C²连续性。

以1D函数为例，安全扩展函数定义为：

$$S_{1D,i}(s_i) = \begin{cases} a_{\min} s_i^2 + b_{\min} s_i + c_{\min}, & s_i < s_i^{\min} \\ a_{\max} s_i^2 + b_{\max} s_i + c_{\max}, & s_i > s_i^{\max} \\ \hat{\Psi}_i(s_i), & \text{otherwise} \end{cases}$$

其中系数通过匹配边界值、一阶导和二阶导确定，例如左边界系数：

$$a_{\min} = \frac{1}{2} h_i^{\min}, \quad b_{\min} = g_i^{\min} - 2 a_{\min} s_i^{\min}, \quad c_{\min} = f_i^{\min} - a_{\min} (s_i^{\min})^2 - b_{\min} s_i^{\min}$$

该策略确保即使应变超出训练域，Hessian矩阵仍保持连续，牛顿求解器不会因域外应变而发散。

### 网络烘焙：消除运行时推理开销

训练完成的神经网络虽已满足精度和平滑性要求，但在每次牛顿迭代中调用网络前向传播（含自动微分求Hessian）的计算开销不可忽视。网络烘焙模块将训练好的网络在HYLC应变空间的规则网格上采样，重构为Hermite插值函数。烘焙后，应变能及其一阶、二阶导数的计算退化为多项式求值，无需任何神经网络推理。实验表明，烘焙将每帧计算耗时从510 ms降至65 ms（约7.8×加速），使14K顶点的T恤仿真达到15 FPS。

### 因果链路总结

神经网络的无限平滑性 → 三阶导数惩罚抑制振荡 → Hessian平滑连续 → 牛顿求解器在大时间步长下稳定收敛 → 仿真效率两个数量级提升。烘焙机制消除了神经网络推理的运行时代价，而安全外推保证了域外应变的鲁棒处理。三个changed slots分别从函数表示、数据效率和域外安全性三个维度协同作用，共同实现了从“仅能小步长离线仿真”到“大步长实时交互”的跨越。

## 实验与关键发现

### 主要性能结果

本方法在仿真效率上实现了突破性提升。在针织T恤场景（14K顶点）中，模型以Δt=1/30 s的大时间步长稳定运行，达到**15 FPS**的交互帧率（桌面PC，Intel i9-10850K CPU），相比HYLC基线模型实现了**至少两个数量级**的加速。HYLC因数值稳定性限制，必须采用极小时间步长（约10⁻⁴ s量级），无法在类似场景下完成有效仿真（Figure 1, Section 7）。

在精度验证方面，对stockinette织物条（5cm×12cm）进行拉伸测试，以纱线级DER仿真器（Bergou et al., 2008）为ground truth，采用Hausdorff距离度量变形误差。本模型在course方向误差为**0.69 cm**，wale方向为**0.72 cm**，而HYLC模型在相同条件下误差均超过1.0 cm，误差降低约30%以上（Figure 8(a),(b)）。力-拉伸比关系曲线（Figure 8(c)）进一步表明，本模型预测的力学响应与ground truth高度吻合。

### 稳定性核心指标：二次展开误差

二次展开误差E是衡量应变能函数平滑性的关键指标——E值越小，表明函数的三阶导数幅度越小，泰勒展开时振荡越弱，牛顿求解器的收敛性越好。在10K随机采样点上的测试结果（Table 1）显示：

![[assets/figures/papers/paper_list_l26_https_rullec_github_io/figures/005_Table_1.jpg]]
*Table 1: Quadratic expansion error E analysis for Stockinette pattern. This analysis shows our model has a lower quadratic expansion error, i.e., smaller magnitudes of thirdorder derivatives.For the definition of quadratic expansion error E and details on its computation,please refer to the supplementary material*

- **Basket图案**：本模型 E = 6.28×10⁻⁴，HYLC E = 1.31×10⁻³，降低**52%**
- **Stockinette图案**：本模型 E = 4.05×10⁻⁴，HYLC E = 2.67×10⁻³，降低**85%**

这一差异直接解释了为何HYLC在隐式积分中需要极小步长——其Hermite插值在节点处二阶导数不连续，导致牛顿求解器在步长稍大时即发散。

### 时间步长稳定性对比

在悬挂布料场景（20cm×20cm，无回溯线搜索）中，本模型的最大稳定时间步长达到**1/30 s**，而HYLC模型在**1/1000 s**时即失败，差距约**33倍**（Section 7.2, Figure 6）。在动态场景测试中：

- **球体撞击布料**（50cm×50cm）：本模型以Δt=1/30 s稳健运行，HYLC在Δt=1/1000 s失败
- **旗帜迎风飘动**（20cm×50cm）：同样条件下本模型保持稳定，HYLC崩溃

这些结果验证了神经网络表示在保证高阶导数平滑性方面的本质优势——sigmoid激活函数的固有平滑性使得应变能函数的二阶导数连续，从而保证了隐式欧拉积分的数值稳定性。

### 关键消融实验

消融实验基于20cm×20cm悬挂布料场景，系统验证了各损失函数组件的必要性（Figure 4）：

![[assets/figures/papers/paper_list_l26_https_rullec_github_io/figures/004_Figure_4.jpg]]
*Figure 4: Ablation studies conducted on the hanging simulationofa 20cm×20cm fabric sample.We demonstrate the crucial roles ofthre specific loses:the first-order predictionloss,the strainconcentrationloss,andthe third-orderderivativeloss. Eachofthese losses contributes uniquelytotheaccuracyandstabilityofthesimulation,highlighting theirimportance inour model*

**一阶预测损失 L^F**：移除该损失项后，网络仅拟合能量值而忽略梯度信息，导致参考构型出现不切实际的扭曲变形（Figure 4(a)）。这表明一阶导数监督对于保持力学平衡态的准确性至关重要。

**应变集中损失 L^B**：移除该损失后，应变能函数在训练域外呈现非单调下降趋势，使得仿真中应变能无法正确引导变形恢复，产生错误结果（Figure 4(b)）。该损失通过惩罚能量函数的非凸性，确保物理合理性。

**三阶导数平滑损失 L^C**（权重w^C）：这是最关键的消融发现。将w^C从0逐步提高到10⁻³，最大稳定时间步长从**1/5000 s**单调提升至**1/30 s**（Figure 4(c)），提升约**167倍**。这直接证明了：通过有限差分近似三阶导数并惩罚其幅度，可以有效抑制应变能函数的数值振荡，是实现大时间步长仿真的核心机制。

**网络烘焙**：在Karate演示场景中，烘焙将每帧计算耗时从**510 ms**降至**65 ms**，加速约**7.8倍**（Section 7.1）。烘焙将神经网络转换为解析的Hermite插值函数，消除了运行时的自动微分开销，同时保持了训练获得的平滑特性。

**扇区热启动策略**：在数据生成阶段，基于极坐标的扇区并行热启动相比从头仿真带来约**一个数量级（~10×）**的加速（Section 4）。该策略利用纱线结构在不同应变下的变形连续性，通过预定义应变序列逐步增大变形，使每个采样点的优化问题能从相邻已解点的解出发，大幅减少迭代次数。

### 失败模式与适用边界

**训练域外行为**：尽管安全外推机制（safeguard）通过C²连续的二次函数延拓保证了应变能函数在训练域外的定义，但当仿真中出现远超训练范围的极端应变时，二次函数的外推精度有限，可能导致物理真实感下降。该机制的设计目标是在不崩溃的前提下提供合理近似，而非精确预测。

**维度分解的局限**：本方法将6D应变能函数分解为常数、拉伸（2D）、一维弯曲和二维弯曲分量的组合，忽略了更高维度的耦合项（如拉伸-弯曲耦合的3D/4D分量）。对于复杂变形模式（如同时发生大拉伸和双向弯曲），这种分解可能导致精度损失。实验中的拉伸测试和悬挂场景尚未充分暴露这一局限。

**数据依赖性**：模型使用合成纱线仿真数据训练，未在真实织物测量数据上验证。当实际织物的纱线材质、摩擦系数或细观结构与仿真假设存在显著差异时，预测精度可能下降。此外，每种新纱线图案都需要完整的“纱线仿真→数据采样→网络训练→烘焙”流程，计算开销较大，不利于快速设计迭代。

**对比基线有限**：实验仅与HYLC（Sperl et al., 2020）进行了系统对比，缺乏与其他数据驱动本构模型或均匀化方法的横向比较，结论的普适性有待进一步验证。

## 定位与知识库关联

本文的核心贡献在于**更换了纱线级布料均匀化管线中“应变能密度函数表示”这一关键模块**，从而解决了长期制约该类方法走向交互式应用的数值稳定性瓶颈。具体而言，基线方法 **HYLC**（Sperl et al., 2020）采用 Hermite 插值函数构建超弹性本构模型，其应变能函数在插值节点处仅保证 C¹ 连续，二阶导数存在跳跃间断。这一看似细微的光滑性缺陷，在隐式欧拉积分的牛顿求解器中会被放大：当时间步长超过约 10⁻⁴ s 量级时，刚度矩阵的剧烈振荡导致求解器发散，迫使仿真以极小步长推进，计算代价高昂。

本工作将这一模块替换为**神经网络表示**——采用三层 MLP 配合 sigmoid 激活函数，并在训练中显式惩罚三阶导数的有限差分近似（权重 w^C 从 0 提升至 10⁻³）。sigmoid 函数的固有无限可微性，结合三阶导数正则化，使得训练得到的应变能函数在整个定义域内具有平滑的二阶导数（即 C² 连续性）。这一性质直接保障了牛顿求解器在大时间步长下的收敛性，将最大稳定步长从 HYLC 的约 1/1000 s 提升至 1/30 s（约 33 倍），使得 14K 顶点的针织 T 恤仿真达到 15 FPS，相对 HYLC 实现至少两个数量级的加速。

**知识库挂载点**：本工作可定位于“物理仿真中的神经本构模型”这一交叉节点，连接以下三条知识脉络：

1. **计算均匀化理论**（computational homogenization）：继承了 Sperl et al. (2020) 建立的从纱线级周期图案仿真到连续介质本构模型的降阶框架，包括基于第一、第二基本形式的宏观应变描述和应变能密度分解策略（将 6D 函数拆解为 1D/2D 分量以规避维度灾难）。本文未改动这一理论骨架，而是精准替换了其中的函数逼近环节。

2. **神经网络作为函数逼近器**（neural networks as universal function approximators）：利用神经网络的天然平滑性解决传统插值方法在导数连续性上的固有问题。这一思路与材料科学中“神经本构模型”（neural constitutive models）的潮流一致，但本文的独特之处在于将网络“烘焙”（baking）回解析的 Hermite 插值函数，使运行时完全消除自动微分开销（每帧耗时从 510 ms 降至 65 ms），兼顾了训练时的表达灵活性和推理时的计算效率。

3. **隐式仿真的数值稳定性**（numerical stability of implicit simulation）：揭示了本构模型的高阶光滑性与牛顿求解器收敛性之间的因果关系——三阶导数的大小直接决定二次展开误差 E，而 E 越小意味着能量景观越接近二次函数，牛顿迭代越稳健。这一洞察对任何依赖隐式积分的物理仿真系统具有普适参考价值。

**适用边界**：

- 本方法假设布料由周期性的纱线图案构成，适用于平纹、罗纹、蜂巢等规则组织；对于非周期或高度异质的织物结构（如蕾丝、提花），需要扩展均匀化框架。
- 应变能分解仅保留了常数、拉伸、一维弯曲和二维弯曲分量，忽略了更高维度的耦合项（如 6D 全耦合），在极端双轴拉伸-弯曲耦合场景下可能存在精度损失。
- 训练数据来自合成纱线仿真（基于 DER 模型），而非真实织物的力学测量数据，因此模型捕捉的是理想纱线几何的力学行为，对真实纱线材质（棉、涤纶等）和制造公差的泛化能力尚未验证。
- 数据生成和网络训练的计算开销较大（每种新图案需完整走一遍“纱线仿真→数据采样→网络训练→烘焙”流程），不适合需要快速迭代的设计探索场景。

**后续启发**：

1. **真实数据驱动**：将本框架与真实织物的拉伸、弯曲、剪切测试数据对接，用实验数据微调或从头训练网络，有望弥合“合成数据→真实织物”的 sim-to-real 鸿沟，是该方向最直接且有价值的延伸。

2. **更高阶耦合项的低成本建模**：当前 1D/2D 分解是应对维度灾难的实用折中。探索张量分解、低秩近似或物理引导的特征工程，在不引发维度爆炸的前提下纳入关键耦合项（如拉伸-弯曲耦合），是提升模型表达能力的重要方向。

3. **烘焙策略的泛化**：网络烘焙为 Hermite 插值是一种针对 1D/2D 低维函数的特定方案。对于需要保留更高维耦合项的模型，需研究更通用的“网络→解析函数”编译技术（如样条、径向基函数展开），以维持运行时的高效性。

4. **跨材质与跨结构泛化**：当前方法对每种纱线图案独立训练。探索元学习（meta-learning）或条件神经网络（以纱线材质参数、几何参数为输入），使单一模型能覆盖多种织物类型，将大幅降低部署成本。

5. **数值稳定性理论的深化**：本文实证了三阶导数正则化对稳定性的关键作用，但缺乏理论上的收敛性保证。从优化景观分析或非线性数值分析角度，建立“本构模型光滑性→牛顿法收敛半径”的定量关系，可为同类工作提供更坚实的理论基础。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Neural_assisted_Homogenization_of_Yarn_level_Cloth.pdf]]