---
title: "Toward Optimized VR/AR Ergonomics: Modeling and Predicting User Neck Muscle Contraction"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/Toward_Optimized_VR_AR_Ergonomics_Modeling_and_Predicting_User_Neck_Muscle_Contraction.pdf
project_link: null
code_link: "https://github.com/NYU-ICL/xr-ergonomics-neck-comfort"
aliases:
- MT
- TOVAEMPUNMC
tags:
- SIGGRAPH_2023
- topic/benchmarks_datasets_evaluation
core_operator: 头部姿态（pitch/yaw角度）与头部运动的角加速度是决定颈部肌肉收缩水平的核心运动学因素。
primary_logic: 通过生物物理启发的扭矩平衡方程将MCL与头部运动关联，并用数据驱动方法学习其中的未知函数，可以从已知或预测的头部轨迹准确估计肌肉收缩水平，从而在运动发生前即可预测潜在不适，为界面优化提供定量指标。
claims:
- MCLNet在后验估计中取得12.39% NRMSE和9.54% NMAE，证明从头部姿态和加速度精确预测MCL的可行性。
- 结合TrajectoryNet的预预测MCL实现16.76% NRMSE，首次实现仅凭目标位置预测肌肉负荷。
- 用户研究表明模型引导的优化条件（MIN）显著降低不适感（MAX 86.1% vs MIN 13.1%被选为更不适，p<.001）。
- Collected pilot study dataset (63 anchors × 8 targets, 8 subjects, seated VR) 上 NRMSE (%) = MCLNet (post-hoc estimation)
---

# Toward Optimized VR/AR Ergonomics: Modeling and Predicting User Neck Muscle Contraction

> [!tip] 核心洞察
> 通过生物物理启发的扭矩平衡方程将MCL与头部运动关联，并用数据驱动方法学习其中的未知函数，可以从已知或预测的头部轨迹准确估计肌肉收缩水平，从而在运动发生前即可预测潜在不适，为界面优化提供定量指标。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向优化VR/AR人体工学的颈部肌肉收缩建模与预测 |
| 英文题名 | Toward Optimized VR/AR Ergonomics: Modeling and Predicting User Neck Muscle Contraction |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://www.immersivecomputinglab.org/publication/toward-optimized-vr-ar-ergonomics-modeling-and-predicting-user-neck-muscle-contraction/) · [Code](https://github.com/NYU-ICL/xr-ergonomics-neck-comfort) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | MCLNet + TrajectoryNet (生物物理启发的颈部肌肉收缩预测框架) |
| Dataset | Collected pilot study dataset, Same dataset, pre-hoc prediction scenario |

> [!tip] 效果简介
> - Collected pilot study dataset (63 anchors × 8 targets, 8 subjects, seated VR) 上，NRMSE (%) MCLNet (post-hoc estimation) vs EMG measurement (ground truth) (12.39 ± 4.74%)。
> - Same dataset, pre-hoc prediction scenario 上，NRMSE (%) TrajectoryNet + MCLNet (pre-hoc prediction) vs EMG measurement (ground truth) (16.76 ± 6.05%)。

## 概要

VR/AR头戴设备的使用加重了用户的颈部肌肉负担，但现有实践中缺乏一种能够在设计阶段量化评估并预测颈部不适的计算工具。本文提出一个生物物理启发的计算框架，首次从头部运动学数据直接建模并预测颈部肌肉收缩水平（MCL）。该框架包含两个核心模块：**MCLNet** 从头部姿态与角加速度序列中估计瞬时MCL；**TrajectoryNet** 则仅凭起始与目标头部姿态预测运动轨迹，从而在运动实际发生前即可预估整体肌肉负荷。在采集自8名受试者的坐姿VR数据上，MCLNet的后验估计达到12.39%的NRMSE；结合TrajectoryNet的预预测MCL达到16.76%的NRMSE。用户研究进一步验证了模型的有效性：基于模型优化的低负荷界面条件（MIN）在86.1%的对比中被判定为更舒适（p<.001）。该方法为VR/AR界面的人体工学优化提供了可量化的预测指标，填补了从运动预测到肌肉负荷评估的计算空白。

## 核心方法与创新机理

### 问题瓶颈与核心因果机制

VR/AR头戴显示设备（HMD）的附加重量会显著增加用户颈部肌肉的静态与动态负荷，长期使用可能导致颈部不适甚至慢性损伤。然而，当前缺乏能够**量化评估并预先预测**颈部肌肉收缩水平（Muscle Contraction Level, MCL）的计算模型，使得界面设计者无法在设计阶段预见并优化用户的人体工学体验。本工作的核心瓶颈在于：**EMG测量虽能直接反映肌肉激活状态，但佩戴繁琐且仅能进行事后测量，无法在运动发生前提供预测信号**。

解决这一瓶颈的因果调节旋钮（causal knob）在于：头部姿态（pitch/yaw角度）与头部运动的角加速度是决定颈部肌肉收缩水平的**核心运动学因素**。当头部偏离自然姿态时，被动组织（韧带、椎间盘等）产生被动扭矩 $\mathcal{T}_{\mathfrak{p}}(\mathbf{r})$；运动过程中，主动肌肉扭矩 $\mathcal{T}_{\mathbf{a}}$ 与被动扭矩共同平衡惯性力矩 $I \times \pmb{\alpha}$。这一力学关系构成了从可观测运动到不可直接测量的肌肉收缩水平之间的因果桥梁。

核心创新洞察在于：**通过生物物理启发的扭矩平衡方程将MCL与头部运动关联，并用数据驱动方法联合学习方程中的未知函数，可以从已知或预测的头部轨迹准确估计肌肉收缩水平，从而在运动发生前即可预测潜在不适**。这一框架首次实现了从“事后测量”到“事前预测”的范式转换，为界面优化提供了定量指标。

### 方法框架与模块链路

整体框架包含四个关键模块，形成从原始EMG信号到预预测MCL的完整链路：

1. **EMG信号处理管道**：将4通道原始EMG信号转换为归一化的整体MCL真值。
2. **MCLNet**：后验估计模型，从已知头部运动序列预测瞬时MCL。
3. **TrajectoryNet**：轨迹预测模型，从起止姿态预测高斯角速度曲线参数。
4. **条件生成算法**：基于MCL预测优化目标布局的用户研究工具。

模块间的因果关系链为：EMG管道提供监督信号 → MCLNet学习运动-MCL映射 → TrajectoryNet提供预测性运动轨迹 → 联合管道实现仅凭目标位置的MCL预预测。

### Changed Slot 1：从直接EMG测量到MCLNet后验估计

**基线状态**：传统方法直接通过EMG传感器测量肌肉电活动，无法从头部运动计算MCL，不具备预测能力。

**提出的变更**：MCLNet——一个1D CNN模型，接收头部运动序列和角加速度，输出瞬时MCL值。其核心创新在于将生物物理先验嵌入网络架构，**联合学习**转动惯量 $I$、被动扭矩函数 $\mathcal{T}_{\mathfrak{p}}(\cdot)$ 和扭矩-MCL映射函数 $\mathcal{E}(\cdot)$ 这三个未知量。

**生物物理建模基础**：颈部转动的力学平衡方程为：

$$\mathcal{T}_{\mathfrak{p}}(\mathbf{r}) + \mathcal{T}_{\mathbf{a}}(\mathbf{r}, \pmb{\alpha}) = I \times \pmb{\alpha}$$

其中 $\mathbf{r} \triangleq (p, y)$ 为头部pitch和yaw姿态角，$\pmb{\alpha} \triangleq (\pmb{\alpha}_p, \pmb{\alpha}_y)$ 为对应方向的角加速度。被动扭矩 $\mathcal{T}_{\mathfrak{p}}$ 仅依赖于头部姿态（由被动组织弹性决定），主动扭矩 $\mathcal{T}_{\mathbf{a}}$ 由肌肉收缩产生且与MCL成正比。

由此可导出MCL的力学表达：

$$\mathrm{MCL} = (\mathcal{E} \circ \mathcal{T}_{\mathbf{a}})(\mathbf{r}, \pmb{\alpha}) = \mathcal{E}\left(I \times \pmb{\alpha} - \mathcal{T}_{\mathfrak{p}}(\mathbf{r})\right)$$

该公式揭示了MCL的两个决定因素：角加速度项 $I \times \pmb{\alpha}$（动态分量）和被动扭矩补偿项 $-\mathcal{T}_{\mathfrak{p}}(\mathbf{r})$（静态分量）。当头部处于极端姿态时，被动扭矩增大，需要更多主动扭矩来平衡，从而增加MCL。

**网络实现**：MCLNet采用1D CNN架构，输入为头部运动序列（含姿态和角加速度），输出为瞬时MCL。网络内部隐式学习 $I$、$\mathcal{T}_{\mathfrak{p}}(\cdot)$ 和 $\mathcal{E}(\cdot)$，无需分别标注这些中间量。训练使用L2损失函数，以EMG管道处理得到的MCL作为监督信号。

**训练与推理路径**：
- **训练**：使用前导研究中采集的配对数据（头部运动轨迹 + 对应EMG信号），经EMG管道处理后得到MCL真值，以L2损失端到端训练MCLNet。
- **推理**：给定完整的头部运动轨迹（姿态序列和角加速度序列），MCLNet直接输出每个时刻的MCL估计值。

### Changed Slot 2：从运动后估计到运动前预预测

**基线状态**：MCLNet只能在运动完成后、已知完整轨迹的条件下进行后验估计，无法在用户开始移动前提供预测。

**提出的变更**：TrajectoryNet + MCLNet联合管道，实现仅凭起始姿态 $\mathbf{r}_s$ 和目标姿态 $\mathbf{r}_e$ 即可预测整个运动过程的累积MCL。

**轨迹建模**：关键观察是，pitch和yaw方向的角速度曲线可被近似为**单峰高斯函数**：

$$\omega_t^i(\mathbf{r}_s, \mathbf{r}_e) \triangleq A^i(\mathbf{r}_s, \mathbf{r}_e) \, e^{-\frac{(t - \mu^i(\mathbf{r}_s, \mathbf{r}_e))^2}{2\sigma^i(\mathbf{r}_s, \mathbf{r}_e)^2}}$$

其中 $i \in \{p, y\}$ 分别表示pitch和yaw方向，$A^i$ 为幅度，$\mu^i$ 为峰值时间，$\sigma^i$ 为宽度参数。

TrajectoryNet是一个MLP模型，输入起始和目标头部姿态对，输出两个方向的高斯参数。为确保预测的角速度积分后恰好等于目标姿态偏移，施加积分约束：

$$\mathbf{r}_s + \int_{t=0}^{t_e} \omega_t(\mathbf{r}_s, \mathbf{r}_e) \, dt = \mathbf{r}_e$$

该约束确定了运动结束时间 $t_e$，并保证了轨迹的物理一致性。

**MCL预预测**：获得预测的角速度曲线后，通过积分MCLNet的瞬时输出来计算整体MCL：

$$\mathrm{H}_c(\mathbf{r}_s, \mathbf{r}_e) = \int_{t=t_s}^{t_e} \mathcal{H}_m\left(\mathcal{E}, \mathcal{T}_{\mathbf{p}}, I, \mathbf{r}_t(\mathbf{r}_s, \mathbf{r}_e), \dot{\pmb{\omega}}_t(\mathbf{r}_s, \mathbf{r}_e)\right) dt$$

其中 $\mathbf{r}_t$ 由预测的角速度积分得到，$\dot{\pmb{\omega}}_t$ 为角加速度（高斯函数的导数）。该公式将MCLNet的瞬时预测能力与TrajectoryNet的轨迹预测能力串联，实现了**仅凭目标位置即可预测肌肉负荷**的完整链路。

**训练与推理路径**：
- **TrajectoryNet训练**：使用采集数据中的真实起止姿态对和对应的角速度曲线，以L2损失训练MLP预测高斯参数。
- **联合推理**：给定 $\mathbf{r}_s$ 和 $\mathbf{r}_e$ → TrajectoryNet预测高斯参数 → 重构角速度曲线 → 积分得到头部姿态序列 → 计算角加速度 → MCLNet输出瞬时MCL → 时间积分得到整体MCL预测值。

### 条件生成与界面优化应用

为验证模型在实际界面优化中的效用，设计了基于MCL预测的条件生成算法。该算法在给定当前头部姿态 $\mathbf{r}_c$ 的情况下，从候选目标姿态集合中选择使预测MCL最小的下一个目标 $\mathbf{r}^*$，从而生成优化的扫描路径。这构成了MAX（最大MCL路径）、MIN（最小MCL路径）和RND（随机路径）三种实验条件，用于用户研究验证。

### 关键创新总结

1. **生物物理-数据驱动混合建模**：不依赖纯黑箱学习，而是将扭矩平衡方程作为归纳偏置嵌入模型，使MCLNet在有限数据下也能学习到物理上合理的映射关系。
2. **两阶段预测范式**：先预测运动轨迹（TrajectoryNet），再预测肌肉负荷（MCLNet），将困难的端到端预测分解为两个可分别验证的子问题。
3. **高斯轨迹近似**：用单峰高斯函数参数化角速度曲线，大幅降低轨迹预测的复杂度，同时保持了对自然头部运动特征的合理捕捉。
4. **闭环优化能力**：模型输出可直接用于界面布局的定量优化，形成了从测量、建模、预测到优化的完整工具链。

![[assets/figures/papers/paper_list_l5_https_www_immersivecomputinglab_org_publication_toward_optimized_vr_ar_e/figures/001_Figure_1.jpg]]
*Figure 1: Predicting the neck muscle contraction and discomfort levels of VR users. (a) A VR user chooses between two candidate head motion trajectories of seemingly similar muscular workload for a visual task. (b) Our computational model predicts the user’s potential neck muscle contraction level and thus perceived neck muscle discomfort before the movements happen. 3D asset credits to Mixall, Bizulka, RootMotion at Unity, and shockwavegamez01, joseVG at Sketchfab*

![[assets/figures/papers/paper_list_l5_https_www_immersivecomputinglab_org_publication_toward_optimized_vr_ar_e/figures/002_Figure_2.jpg]]
*Figure 2: Pilot study illustration and results. (a) illustrates the major muscles controlling head movements, with highlighted EMG sensor attachment regions. (b) shows our experimental setup with EMG sensors annotated. (c) The top row shows an example raw EMG sequence (light green curve and right Y-axis) and its corresponding normalized MCL (dark green curve and left Y-axis). The bottom row shows the total MCL integrated across all 4 channels. (d) visualizes the user-aggregated MCL for stationary viewing. (e) shows the movement-induced ΔMCL for dynamic viewing. Each*

![[assets/figures/papers/paper_list_l5_https_www_immersivecomputinglab_org_publication_toward_optimized_vr_ar_e/figures/003_Figure_3.jpg]]
*Figure 3: MCLNet illustration and example MCL estimation results. (a) illustrates the architectural design of MCLNet for jointly learning*

## 实验与关键发现

### 数据集与前导研究

研究团队采集了**8名参与者**（年龄23–31岁，3名女性）在坐姿VR环境下的颈部肌电与头部运动数据。实验设置中，参与者依次注视63个锚点姿态与8个目标姿态之间的视觉刺激，EMG传感器附着于双侧胸锁乳突肌（SCM）与头夹肌（SC）——上斜方肌因信号显著较弱而被排除。原始EMG信号经过去趋势、带通滤波、整流、通道间平衡、归一化与积分处理后，输出单一归一化肌肉收缩水平（MCL）值。

前导研究揭示了两个关键现象：**静态注视**时，头部姿态本身即产生基线MCL——正视前方姿态（r=(0,0)）的平均MCL最低（0.17±0.02），而极端姿态则显著升高，整体静态MCL均值为0.32±0.12；**动态运动**中，头部角加速度引发额外的ΔMCL，其幅度与运动幅度和速度密切相关。这一发现确立了头部姿态与角加速度作为MCL预测核心运动学变量的因果地位。

### 后验估计：MCLNet性能

在已知完整头部运动轨迹的条件下，MCLNet对瞬时MCL的后验估计取得了**12.39±4.74% NRMSE**和**9.54±4.14% NMAE**（Figure 6）。该结果基于留一条件交叉验证（leave-one-condition-out），即模型在未见过的锚点-目标姿态对上评估，证明学习到的惯性参数I、被动扭矩函数T_p(·)和扭矩-MCL映射E(·)能够有效泛化。

![[assets/figures/papers/paper_list_l5_https_www_immersivecomputinglab_org_publication_toward_optimized_vr_ar_e/figures/006_Figure_6.jpg]]
*Figure 6: Performance of MCLNet for neck MCL estimation when complete head motion trajectories are known*

Figure 3b展示了模型预测与硬件实测MCL的逐帧对比：MCLNet成功捕捉了运动起始时的MCL陡增、运动过程中的持续收缩水平以及运动终止后的回落趋势。然而，在**高角加速度阶段**，预测值存在系统性低估——这暗示单峰高斯角速度近似可能未能充分建模某些参与者的多阶段加速模式。

### 预预测：TrajectoryNet+MCLNet联合管道

当仅给定起始与目标头部姿态（运动发生前）时，TrajectoryNet首先预测pitch和yaw方向的**高斯角速度曲线参数**（幅度A、均值μ、标准差σ），随后MCLNet沿预测轨迹积分得到整体MCL。联合管道取得了**16.76±6.05% NRMSE**和**14.71±5.96% NMAE**（Figure 7c）。

从后验估计的12.39% NRMSE到预预测的16.76% NRMSE，约4.4个百分点的性能退化主要源于**轨迹预测误差的传播**。Figure 7a-b分别展示了TrajectoryNet在pitch和yaw方向上的角速度预测性能：yaw方向的预测精度略低于pitch方向，这可能与颈部在水平旋转时更复杂的肌肉协同模式有关。尽管如此，16.76% NRMSE意味着模型仅凭目标位置即可在运动发生前提供有意义的肌肉负荷预估，这是此前任何方法均未实现的能力。

### 用户研究：模型引导优化的有效性验证

为验证MCL预测对实际不适感的优化效果，研究团队设计了**12名参与者**的2AFC用户研究。基于条件生成算法（Figure 10），为每位参与者生成三组视觉目标布局：

- **MAX条件**：贪婪最大化预测MCL的扫描路径
- **MIN条件**：贪婪最小化预测MCL的扫描路径
- **RND条件**：随机生成的目标布局

参与者佩戴VR头显依次执行各条件下的视觉搜索任务，随后在18轮2AFC比较中判断哪种条件更不适。结果显示（Figure 5c）：**MAX条件在86.1%的比较中被选为更不适，MIN条件仅13.1%，RND条件为50.7%**。重复测量ANOVA表明条件间差异极显著（F(2,22)=89.46, p<.001），Tukey HSD事后检验确认所有两两比较均显著（p<.001）。

Table 1的个体层面数据显示，12名参与者中有11人在MAX vs. MIN比较中**100%选择MAX为更不适**，仅1名参与者在18轮比较中有1次例外。这一高度一致的个体间模式表明模型预测的MCL与主观不适感之间存在稳健的映射关系，而非仅反映群体平均趋势。

### 定性分析与个体差异

Figure 8展示了6名评估数据贡献者的定性预测结果。多数参与者的预测MCL序列与实测值在趋势上高度吻合，但在**峰值幅度和持续时间**上存在个体差异：部分参与者表现出更尖锐的MCL峰值和更快的衰减，而另一些则呈现更平缓的收缩模式。这些差异可能与个体的运动策略（如是否采用分阶段加速）和肌肉募集模式有关，而当前的单峰高斯轨迹近似无法充分捕捉此类变化。

### 适用边界与失败模式

1. **姿态维度限制**：模型仅建模pitch和yaw方向的运动，未考虑roll维度。当任务涉及头部倾斜（如侧头观察倾斜界面）时，MCL预测可能低估实际肌肉负荷，因为胸锁乳突肌在头部侧倾时也有显著激活。

2. **坐姿固定假设**：所有数据采集于坐姿、躯干固定场景。站立或行走状态下，躯干的补偿性运动可能改变颈部肌肉的负荷分布，模型在此类场景中的泛化能力未经验证。

3. **单峰轨迹假设**：TrajectoryNet将角速度近似为单峰高斯曲线，这适用于简单的指向运动，但在包含**中途修正、多目标连续扫描或避障路径**的复杂任务中可能失效。Figure 4的示例显示，部分实际轨迹存在非对称或双峰特征，预测曲线在这些情况下会产生系统性偏差。

4. **人群覆盖局限**：8名训练参与者均为23–31岁、颈部状况正常的年轻人。老年用户、颈部疾病患者或不同体型人群的被动扭矩特性和肌肉募集策略可能存在显著差异，模型在这些群体上的表现需要进一步验证。

5. **设备依赖性**：模型未显式建模头戴设备的质量分布参数。不同HMD的重量和重心位置会改变颈部肌肉的负荷基线，当前模型需针对特定设备重新校准或采集数据。

6. **长期效应缺失**：模型预测的是瞬时或单次运动的MCL，未考虑肌肉疲劳的累积效应。在长时间VR/AR使用场景中，疲劳导致的肌肉激活模式变化可能使预测精度随时间衰减。

![[assets/figures/papers/paper_list_l5_https_www_immersivecomputinglab_org_publication_toward_optimized_vr_ar_e/figures/005_Figure_5.jpg]]
*Figure 5: Stimuli and results of our neck discomfort user study. (a) shows the stimuli. (b) visualizes the visual targets’ angular distributions of 3 example conditions. Color gradients indicate the temporal order of appearance. All 3 conditions share the same total head rotations with full visual field coverage. (c) summarizes the voting distribution of the 3 comparisons on which condition being more uncomfortable. Individual votes per condition are detailed in Table 1. 3D asset credits to Mixall at Unity*

![[assets/figures/papers/paper_list_l5_https_www_immersivecomputinglab_org_publication_toward_optimized_vr_ar_e/figures/007_Figure.jpg]]
*Figure: (a) performance of TrajectoryNet for angular velocity prediction (pitch) with target head poses only (b) performance of TrajectoryNet for angular velocity prediction (yaw) with target head poses only (c) performance of MCLNet coupled with TrajectoryNet for neck MCL prediction with target head poses only*

## 定位与知识库关联

### 1. 改变了什么 Slot？

本工作改变了两个关键技术槽位：

**Slot 1：从“事后测量”到“事后估计”的 MCL 获取方式。**
传统 VR/AR 人体工学研究对颈部肌肉负荷的评估完全依赖 EMG 传感器的直接测量（如先导研究中使用 4 通道 EMG 设备采集信号后经过去趋势、带通滤波、整流、通道平衡、归一化和积分处理得到归一化 MCL）。这种方式的根本局限在于：（a）传感器佩戴繁琐且成本高，限制日常应用；（b）只能在运动发生后测量，无法在设计阶段提供反馈。本工作提出的 **MCLNet** 将这一槽位从“物理测量”替换为“计算预测”——通过生物物理启发的扭矩平衡方程 $ \mathcal { T } _ { \mathfrak { p } } \left( \mathbf { r } \right) + \mathcal { T } _ { \mathbf { a } } \left( \mathbf { r } , \pmb { \alpha } \right) = I \times \pmb { \alpha } $ 建立头部运动学（姿态 $ \mathbf{r} $、角加速度 $ \pmb{\alpha} $）与肌肉主动扭矩之间的力学关联，再用 1D CNN 联合学习其中三个未知函数（转动惯量 $ I $、被动扭矩函数 $ \mathcal{T}_{\mathfrak{p}}(\cdot) $、扭矩-MCL 映射 $ \mathcal{E}(\cdot) $），从而仅凭头部运动序列即可估计瞬时 MCL。这是从“传感器依赖”到“纯运动学驱动”的范式转换。

**Slot 2：从“事后估计”到“事前预测”的 MCL 可用时机。**
MCLNet 虽然摆脱了 EMG 传感器，但仍需已知完整头部运动轨迹——这在界面设计阶段无法获得。本工作进一步引入 **TrajectoryNet**，将 MCL 的可用时机从“运动发生后”推进到“运动发生前”。TrajectoryNet 是一个 MLP 模型，接收起始头部姿态 $ \mathbf{r}_s $ 和目标头部姿态 $ \mathbf{r}_e $，输出单峰高斯角速度曲线的参数（幅度 $ A^i $、均值 $ \mu^i $、标准差 $ \sigma^i $），通过积分约束 $ \mathbf { r } _ { s } + \int _ { t = 0 } ^ { t _ { e } } \omega _ { t } ( \mathbf { r } _ { s } , \mathbf { r } _ { \mathbf { e } } ) \mathrm { d } t = \mathbf { r } _ { \mathbf { e } } $ 保证重构轨迹的终点一致性，再将预测的角速度曲线送入 MCLNet 按 $ \mathrm { H } _ { c } ( \mathbf { r _ { s } } , \mathbf { r _ { e } } ) = \int _ { t = t _ { s } } ^ { t _ { e } } \mathcal { H } _ { m } \left( \cdots \right) \mathrm { d } t $ 积分得到整体 MCL。这使得仅凭目标位置即可在运动发生前预测肌肉负荷，为界面布局的自动优化提供了定量指标。

### 2. 知识库挂载点

本工作在以下知识节点上与现有文献形成可挂载的连接：

**生物力学建模传统。** 将肌肉收缩水平与关节扭矩关联的思路在生物力学中有长期基础（如 Clancy et al. 2011、Paquin and Power 2018、Watanabe and Akima 2009 等关于 EMG-扭矩关系的工作）。本工作的创新在于不显式标定这些关系，而是将其作为可学习函数嵌入神经网络，通过数据驱动方式联合求解惯性、被动扭矩和扭矩-MCL 映射——这是“生物物理模型结构 + 数据驱动参数化”的混合范式，可挂载到更广泛的 physics-informed neural network（PINN）文献节点上。

**VR/AR 人体工学评估。** 现有 VR 人体工学研究主要关注视觉疲劳、晕动症和上肢疲劳，对颈部肌肉负荷的量化评估几乎空白。本工作首次建立了从头部运动学到颈部 MCL 的计算管道，填补了 VR/AR 人体工学中“颈部负荷可计算”这一空白节点。后续研究可在此节点上扩展至其他肌肉群（如肩部斜方肌，先导研究中因信号过弱被排除），或引入不同 HMD 重量分布作为模型输入变量。

**轨迹预测与运动规划。** TrajectoryNet 的单峰高斯角速度近似属于运动原语（movement primitive）建模家族，与 Fitts' Law 指向运动、最小急动度（minimum jerk）轨迹等经典模型共享“用少量参数描述目标导向运动”的哲学。本工作的特殊性在于将轨迹预测的下游任务定义为肌肉负荷积分，而非单纯的运动学精度，这为运动规划的人体工学优化目标提供了新的损失函数设计思路。

### 3. 适用边界

本工作存在明确的适用范围限制，需在知识库中标注：

- **姿态维度受限：** 仅建模 pitch 和 yaw 方向的运动，未考虑 roll 维度。颈部在 roll 方向涉及不同的肌肉协同模式（尤其是胸锁乳突肌和头夹肌的非对称激活），模型无法评估包含头部侧倾的任务。
- **使用情境受限：** 所有数据采集于坐姿、躯干固定场景。站立或移动时躯干的补偿运动会改变颈部肌肉的负荷分布，模型无法直接泛化。
- **人群覆盖受限：** 8 名参与者（23-31 岁，3 名女性，均报告颈部状况正常）无法代表不同年龄段、性别比例和有颈部疾病史的人群。特别是年龄增长导致的颈部肌肉退行性变化可能改变被动扭矩函数 $ \mathcal{T}_{\mathfrak{p}}(\cdot) $ 的形态。
- **轨迹假设受限：** 单峰高斯近似假设目标导向运动的速度曲线为单峰对称形状，这在简单指向任务中合理，但在复杂扫描路径（如多个中途目标、避障运动）中可能失效。
- **设备因素未建模：** 模型未显式纳入 HMD 重量和重心位置作为变量，因此更换不同型号头显时可能需要重新采集训练数据或进行域适应。

### 4. 后续工作启发

从本工作的开放问题和局限出发，可识别以下高价值后续方向：

**多肌肉群联合建模。** 当前框架仅针对颈部肌肉，但交互式 VR/AR 任务常涉及肩部和上背部肌肉的协同负荷。将扭矩平衡方程扩展到多关节链，并用类似的数据驱动方法学习各关节的被动扭矩和扭矩-MCL 映射，可构建全身 VR 人体工学评估工具。

**概率轨迹建模。** 单峰高斯近似是确定性预测，无法捕捉用户间和用户内的运动变异性。引入概率模型（如条件变分自编码器或扩散模型）对 $ \omega_t(\mathbf{r}_s, \mathbf{r}_e) $ 进行分布建模，可输出 MCL 的置信区间而非点估计，对风险敏感的设计决策更有价值。

**实时界面优化。** 本工作已在离线用户研究中验证了模型引导的布局优化能显著降低主观不适感（MAX 条件 86.1% vs MIN 条件 13.1% 被选为更不适，$ F(2,22)=89.46, p<.001 $）。将 MCLNet + TrajectoryNet 集成到实时 VR 渲染管道中，根据用户当前头部姿态动态调整交互元素的空间分布，是实现闭环人体工学优化的关键工程挑战。

**跨设备泛化。** 研究不同 HMD 重量、重心位置和佩戴方式对模型参数（尤其是 $ I $ 和 $ \mathcal{T}_{\mathfrak{p}}(\cdot) $）的影响规律，建立设备参数的显式输入通道或轻量级微调策略，使模型具备跨硬件平台的即插即用能力。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/Toward_Optimized_VR_AR_Ergonomics_Modeling_and_Predicting_User_Neck_Muscle_Contraction.pdf]]