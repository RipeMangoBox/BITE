---
title: "NFL: Neural LiDAR Fields for Novel View Synthesis"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/NFL_Neural_LiDAR_Fields_for_Novel_View_Synthesis.pdf
aliases:
- NNLF
- NFL
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将物理启发的LiDAR传感模型（双向透射率、高斯光束发散、脉冲波形）直接集成到可微神经体渲染框架中，并辅以截断体渲染处理二次回波。"
primary_logic: "通过直接优化神经场来匹配LiDAR的主动传感物理过程，能够比先重建后模拟的方法产生更逼真的新视角扫描，尤其是准确再现光束发散引起的范围偏差、二次回波和射线丢弃现象。"
claims:
- "NFL在TownClean、TownReal、Waymo等多个数据集上，第一回波范围误差（MAE）显著低于基线方法LiDARsim、i-NGP、DS-NeRF和URF。"
- "提出的主动传感体渲染方程（双向透射率权重）在消融实验中始终提升范围精度。"
- "发散光束建模改善了双回波射线的第一和第二回波范围估计，误差分布更集中。"
- "NFL合成的LiDAR扫描能缩小域差距，提升下游点云配准和语义分割的性能。"
---

# NFL: Neural LiDAR Fields for Novel View Synthesis

> [!tip] 核心洞察
> 通过直接优化神经场来匹配LiDAR的主动传感物理过程，能够比先重建后模拟的方法产生更逼真的新视角扫描，尤其是准确再现光束发散引起的范围偏差、二次回波和射线丢弃现象。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | NFL: 用于新视角合成的神经LiDAR场 |
| 英文题名 | NFL: Neural LiDAR Fields for Novel View Synthesis |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2305.01643); [Project](https://research.nvidia.com/labs/toronto-ai/nfl/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | NFL (Neural LiDAR Fields) |
| Dataset | TownClean, TownReal, Waymo Interp., Waymo NVS |

> [!tip] 效果简介
> - TownClean 上，MAE (cm) 为 32.0，对比 159.6 (LiDARsim)，变化 -127.6。
> - TownReal 上，MAE (cm) 为 39.2，对比 162.8 (LiDARsim)，变化 -123.6。
> - Waymo Interp. 上，MAE (cm) 为 30.8，对比 116.3 (LiDARsim)，变化 -85.5。

## 概述

### 问题瓶颈

LiDAR新视角合成（Novel View Synthesis, NVS）旨在从一组已采集的LiDAR扫描中，生成在新传感器位姿下的逼真扫描。现有方法主要分为两类：一是**显式重建+射线投射模拟**（如LiDARsim），其依赖理想表面重建和射线投射，引入离散化误差，且未建模光束发散和多次回波等物理效应，导致合成扫描的真实性不足；二是**基于NeRF的隐式重建方法**（如DS-NeRF、URF），它们直接使用面向被动视觉的标准体渲染方程，忽略了LiDAR作为主动传感器的独特物理过程——双向透射、光束发散、脉冲波形以及二次回波与射线丢弃现象。这些简化使得合成扫描存在系统性范围偏差，尤其在高入射角和大距离场景下更为显著。

### 核心方法

**NFL（Neural LiDAR Fields）** 提出了一种物理启发的神经场框架，将LiDAR的主动传感模型直接集成到可微体渲染中。其核心创新包括：

- **主动传感体渲染方程**：将标准NeRF的单向透射率 $T_\zeta$ 替换为双向透射率 $T_\zeta^2$，推导出适用于LiDAR的体渲染权重 $w_j = 2\alpha_{\zeta_j} \prod (1 - 2\alpha_{\zeta_k})$，准确建模了激光往返衰减。
- **高斯光束发散建模**：用37根子射线离散近似高斯发散光束，捕捉光束足迹内的几何变化，从而纠正由发散引起的范围估计偏差。
- **截断体渲染处理二次回波**：在估计第一回波后重置透射率，对剩余介质执行二次体渲染，实现对二次回波的显式建模。
- **可学习射线丢弃概率**：通过神经场预测每点的丢弃概率，并结合体渲染积分得到整条射线的回波存在概率。

### 核心结论

**NFL在多个数据集上显著优于所有基线方法**，且合成扫描的逼真度提升直接转化为下游任务的性能增益：

- **范围估计精度**：在TownClean、TownReal和Waymo数据集上，第一回波范围MAE分别达到32.0 cm、39.2 cm和32.6 cm，相比LiDARsim降低超过120 cm，比i-NGP、DS-NeRF等NeRF类方法也有大幅领先。
- **点云质量**：倒角距离（CD）在TownClean上仅为9.0 cm，而LiDARsim为23.5 cm。
- **物理效应建模**：发散光束建模改善了双回波射线的第一和第二回波范围误差分布；主动传感体渲染在消融实验中始终提升精度。
- **下游任务增益**：NFL合成的扫描缩小了与真实扫描的域差距，在点云配准（Rec@5提升显著）和语义分割任务上均取得更好性能。

### 方法定位

NFL位于**神经渲染与物理传感器建模的交叉点**。它继承了NeRF的隐式场景表征和可微渲染范式，但通过引入LiDAR主动传感的物理方程，将神经场从“被动色彩场”扩展为“主动物理场”。与LiDARsim等“先重建后模拟”的显式管线不同，NFL通过端到端优化直接匹配传感物理过程，避免了中间几何重建的误差累积。该方法为自动驾驶和机器人领域的LiDAR仿真提供了一条高保真、数据驱动的新路径。

## 背景与动机

### LiDAR新视角合成的核心挑战

LiDAR传感器通过发射激光脉冲并测量回波时间来获取场景的精确三维几何信息，是自动驾驶和机器人感知系统的关键组件。然而，真实LiDAR扫描的采集成本高昂且受限于特定传感器配置，这催生了LiDAR新视角合成（Novel View Synthesis, NVS）的需求——即从已有的稀疏扫描中生成新视角下的LiDAR点云。

现有LiDAR新视角合成方法（如**LiDARsim**）遵循“先重建后模拟”的范式：先从多帧扫描中显式重建场景表面网格，再通过理想射线投射模拟新视角的扫描过程。这一范式存在根本性局限：**显式表面重建引入离散化误差，且理想射线模型忽略了LiDAR主动传感的物理特性**——包括光束发散、双向透射衰减、多次回波和射线丢弃等现象。这些被忽略的物理效应导致合成扫描与真实传感器数据之间存在显著的域差距（domain gap），表现为范围估计偏差、回波模式失真和点云分布不真实。

### 现有方法的缺口

近年来，神经辐射场（NeRF）在被动视觉的新视角合成中取得了突破性进展，其核心优势在于通过可微体渲染直接优化连续场景表征，避免了显式几何重建的中间误差。部分工作尝试将NeRF扩展到LiDAR数据，例如：

- **DS-NeRF** 和 **URF** 利用稀疏LiDAR深度监督来增强RGB视角合成，但其渲染方程仍基于被动传感器的单向透射率假设；
- **i-NGP** 等快速NeRF变体虽然加速了训练，但同样未适配LiDAR的主动传感物理。

这些方法将LiDAR回波简单地视为深度值或强度值，忽略了LiDAR作为**主动传感器**的本质：激光脉冲需要经历双向传播（发射和返回），其接收功率取决于往返路径上的累积透射率和目标反射率。标准NeRF的单向体渲染方程无法正确建模这一过程，导致范围估计存在系统性偏差。

### 物理建模的必要性

LiDAR传感器的测量过程受多种物理效应影响，这些效应在合成扫描中必须被精确复现才能保证真实性：

1. **双向透射率**：激光脉冲从传感器到目标表面再返回，经历两次衰减。忽略这一双向特性会导致对遮挡边界和半透明表面的错误建模。
2. **光束发散**：实际激光光束具有高斯发散角，在远距离处光斑直径可达数厘米。发散光束可能同时击中多个表面，产生二次回波，且会引入与入射角相关的范围偏差。
3. **二次回波**：当光束部分击中前景物体、部分穿透并击中背景时，传感器会记录两个回波。这对感知透明或穿孔结构（如栅栏、植被）至关重要。
4. **射线丢弃**：当光束未击中任何有效表面（如指向天空）或回波信号过弱时，传感器不返回有效测量。这一现象的建模直接影响合成点云的分布密度。

### 本文动机

基于上述分析，本文提出**NFL（Neural LiDAR Fields）**，核心动机是：**将物理启发的LiDAR传感模型直接集成到可微神经体渲染框架中，通过端到端优化神经场来匹配LiDAR的主动传感物理过程**。与“先重建后模拟”的范式相比，这种“直接优化”策略避免了显式几何重建的中间误差累积，能够更逼真地再现LiDAR扫描的物理特性——尤其是光束发散引起的范围偏差、二次回波和射线丢弃现象。通过缩小合成扫描与真实扫描之间的域差距，NFL有望提升下游任务（如点云配准和语义分割）的性能。

## 核心创新

NFL 的核心创新在于**将物理启发的 LiDAR 主动传感模型直接嵌入可微神经体渲染框架**，从而跳过了传统“先重建后模拟”管线中引入的离散化误差和物理近似不足。具体而言，NFL 在以下五个关键维度上对基线方法进行了系统性改造：

### 1. 从被动到主动的体渲染方程

标准 NeRF 及其变体（i-NGP、DS-NeRF、URF）采用被动传感的体渲染，透射率 $T_\zeta$ 仅建模光路从场景点到传感器的单向衰减。NFL 指出，LiDAR 作为主动传感器，激光脉冲需经历**往返衰减**——从传感器到场景点再返回传感器的完整路径。因此，NFL 将体渲染的核心权重重新推导为**双向透射率形式**：

$$w_j = 2\alpha_{\zeta_j} \cdot \prod_{k=1}^{j-1} (1 - 2\alpha_{\zeta_k})$$

其中 $\alpha_{\zeta_j}$ 为第 $j$ 个采样段的吸收率。这一改动使得体渲染方程能够正确反映主动传感的能量传输物理，是 NFL 在所有数据集上范围精度大幅领先基线的**核心因果旋钮**。消融实验（Table 3）证实，仅将标准体渲染替换为主动传感体渲染，TownClean 上的 MAE 即可降低 2.1 cm，CD 降低 3.9 cm。

### 2. 高斯光束发散建模

基线方法（包括 LiDARsim）通常将每条 LiDAR 射线视为理想几何射线，忽略光束随距离发散的特性。NFL 引入**高斯光束发散模型**，将每条射线扩展为由 37 根子射线组成的锥形光束，辐照度分布为：

$$E(\zeta, \gamma) = \frac{2 I_0}{\pi (\gamma_0 \zeta)^2} \exp\left(-2 \frac{\gamma^2}{\gamma_0^2}\right)$$

其中 $\gamma_0$ 为发散半角，$\gamma$ 为子射线偏离中心的角度。这一建模直接解释了 LiDAR 在高入射角和大距离下的**系统性范围高估**现象（Figure 2），并显著改善了双回波射线的第一和第二回波范围估计误差分布（Figure 4）。

### 3. 截断体渲染与二次回波估计

现有方法未显式建模二次回波。NFL 提出**截断体渲染**：在检测到第一回波峰值后，重置透射率并从第一回波位置之后重新执行体渲染，以估计第二回波的范围。同时引入可学习的二次回波掩码预测，使模型能够判断哪些射线会产生双回波。这一设计使 NFL 成为首个能够**同时准确估计第一和第二回波范围**的神经渲染方法。

### 4. 两阶段粗到细范围估计

与标准 NeRF 直接沿射线积分求期望深度不同，NFL 采用**峰值检测 + 局部细化**的两阶段策略：首先在粗采样权重 $\{w_j^c\}$ 中定位最高峰值位置 $\zeta_p$，然后在该峰值附近进行细粒度重采样，通过加权求和得到精确范围 $\zeta_f = \sum w_j^f \cdot \zeta_j$。这一设计更贴近真实 LiDAR 的峰值检测机制，避免了直接积分在稀疏回波场景下的偏差。

### 5. 可学习射线丢弃概率

LiDAR 射线在未命中任何表面时不会产生回波（射线丢弃）。NFL 为每个空间点预测一个可学习的丢弃概率 $p_d$，并通过体渲染积分得到整条射线的丢弃概率。这使 NFL 能够**端到端地学习场景中哪些区域会产生有效回波**，而无需像 LiDARsim 那样依赖独立的射线丢弃学习模块。

### 创新总结

| 改造维度 | 基线方案 | NFL 方案 | 证据锚点 |
|---------|---------|---------|---------|
| 体渲染方程 | 单向透射率 $T_\zeta$ | 双向透射率 $T_\zeta^2$，权重 $w_j = 2\alpha_j \prod (1-2\alpha_k)$ | Eq. 10-14, Table 3 |
| 光束模型 | 单根理想射线 | 高斯发散光束（37 根子射线） | Eq. 5, Section 4.3 |
| 二次回波 | 无显式建模 | 截断体渲染 + 可学习掩码 | Section 4.3, Fig. 1(b) |
| 范围估计 | 直接加权求和 | 粗到细峰值检测 + 局部细化 | Section 4.3, Fig. 1(a) |
| 射线丢弃 | 无或独立学习 | 可学习丢弃概率 + 体渲染积分 | Section 4.3, Fig. 1(c) |

这些创新共同构成了 NFL 相对于 LiDARsim、i-NGP、DS-NeRF 和 URF 等基线的**系统性优势**：NFL 不再将 LiDAR 视为“有深度的相机”，而是从传感器物理第一性原理出发，直接优化神经场以匹配主动传感的完整物理过程。

## 整体框架

NFL（Neural LiDAR Fields）的整体pipeline围绕一个核心设计展开：**将物理启发的LiDAR主动传感模型直接嵌入可微神经体渲染框架**，从而端到端地学习场景的几何与辐射属性，并合成逼真的新视角LiDAR扫描。其输入为多帧LiDAR扫描数据（包含射线原点、方向、回波范围和反射率），输出为新视角下的第一回波范围、反射率、射线丢弃概率及二次回波范围。

### 模块关系与数据流

整个框架由四个主要模块串联构成，形成“场景表征→物理渲染→信号解码→监督优化”的闭环：

1. **神经场景表征（Neural Scene Representation）**：以三维空间坐标 $\mathbf{x}$ 和视线方向 $\mathbf{d}$ 为输入，使用哈希编码（hash encoding）提取位置特征 $\mathbf{f}_{\mathrm{pos}} \in \mathbb{R}^{32}$，并将方向投影到球谐函数的前16个系数上。四个轻量MLP分别预测体密度 $\sigma$、反射率 $\rho$、射线丢弃概率 $p_d$ 和二次回波掩码 $p_s$（Section 4.1）。这一模块为后续渲染提供了连续、可微的场景属性场。

2. **LiDAR体渲染（LiDAR Volume Rendering）**：这是NFL区别于标准NeRF的核心创新。给定一条射线（或发散光束中的子射线），沿射线采样 $N$ 个点，计算每个采样点处的**双向透射率权重**：
   $$w_j = 2\alpha_{\zeta_j} \cdot \prod_{k=1}^{j-1} (1 - 2\alpha_{\zeta_k})$$
   其中 $\alpha_{\zeta_j}$ 为采样点处的吸收率。总接收辐射功率通过加权有效反射率求和得到：
   $$P = \sum_{j=1}^{N} w_j \rho_{\zeta_j}'$$
   这一方程（Eq. 13-14, Section 4.2）显式建模了激光脉冲往返传播的双向衰减特性，是合成逼真LiDAR回波信号的物理基础。

3. **光束组合与范围估计（Beam Combination & Range Estimation）**：对于发散光束，通过37根子射线离散近似高斯光束剖面（Eq. 5），每条子射线独立执行体渲染后聚合总功率。范围估计采用**两阶段粗到细策略**：先在粗采样权重 $\{w_j^c\}$ 中检测峰值位置 $\zeta_p = \arg\max_j \{w_j^c\}$，再在峰值邻域进行细采样并加权求和得到精化范围 $\zeta_f = \sum_{j=1}^{N^f} w_j^f \cdot \zeta_j$（Section 4.3）。对于二次回波，执行**截断体渲染**：在首次回波位置后重置透射率，重新估计第二回波范围（Figure 1(b)）。射线丢弃概率则通过对采样点的 $p_d$ 进行体渲染积分得到。

4. **训练损失（Training Loss）**：多任务损失函数联合优化所有输出：
   $$\mathcal{L} = \mathcal{L}_{\mathrm{range}} + \lambda_e \mathcal{L}_e + \lambda_d \mathcal{L}_d + \lambda_s \mathcal{L}_s$$
   其中 $\mathcal{L}_{\mathrm{range}}$ 为粗、细两个阶段的范围损失，$\mathcal{L}_e$ 为反射率L2损失，$\mathcal{L}_d$ 为射线丢弃分类损失（BCE + Lovasz），$\mathcal{L}_s$ 为二次回波分割损失（Section 4.4）。

### 关键设计选择

- **双向透射率 vs 单向透射率**：标准NeRF使用单向透射率 $T_\zeta$，适用于被动传感（光仅从场景到达传感器）；LiDAR作为主动传感器，激光需往返传播，因此NFL采用 $T_\zeta^2$ 形式的双向透射率（Eq. 10, Section 4.2）。消融实验证实这一改变始终提升范围精度（Table 3）。

- **发散光束建模**：实际LiDAR光束随距离发散，形成有限大小的足迹。NFL用37根子射线近似高斯光束剖面，使模型能够捕捉光束部分照射不同表面时产生的二次回波和范围偏差（Figure 2, Figure 4）。

- **射线丢弃处理**：当光束未击中任何表面时，传感器收不到有效回波。NFL通过学习每点丢弃概率 $p_d$ 并沿射线积分，预测整条射线的丢弃概率，而非依赖显式几何判断（Section 4.3）。

这些模块协同工作，使得NFL能够从稀疏的LiDAR扫描中学习连续的场景表征，并从任意新视角合成包含第一回波、二次回波、反射率和射线丢弃掩码的完整LiDAR扫描——这是传统“先重建后模拟”方法（如LiDARsim）难以实现的。

## 核心模块与公式推导

### 3.1 神经场景表征

NFL采用哈希编码与球谐函数的混合表征策略，将场景属性编码为连续函数 $F:(\mathbf{x},\mathbf{d})\mapsto(\sigma,\rho,p_d,p_s)$。具体而言，空间坐标 $\mathbf{x}$ 通过哈希编码映射为32维位置特征 $\mathbf{f}_{pos}$，视线方向 $\mathbf{d}$ 投影到前16个球谐系数上构成方向特征。四个独立的MLP分别预测：

- **体密度** $\sigma$：控制介质对光束的衰减与散射；
- **反射率** $\rho$：表面在LiDAR波长下的有效反射强度；
- **射线丢弃概率** $p_d$：光束未击中任何表面而无法返回可检测信号的概率；
- **二次回波掩码** $p_s$：光束是否产生第二回波的二分类预测。

这种统一表征使得所有物理量可在同一可微框架内联合优化，无需显式表面重建。

### 3.2 主动传感体渲染方程

LiDAR与被动相机存在根本差异：激光脉冲需往返传播，因此透射率需经历两次衰减。NFL的核心创新在于将这一物理过程直接嵌入体渲染框架。

**概率辐射功率**。在距离 $\zeta$ 处，由密度 $\sigma_\zeta$ 和反射率 $\rho_\zeta$ 的粒子散射回传感器的概率辐射功率为：

$$P_\zeta = C \frac{T_\zeta^2 \cdot \sigma_\zeta \rho_\zeta}{\zeta^2} \cos(\theta)$$

其中 $C$ 为系统常数，$T_\zeta$ 为从传感器到 $\zeta$ 的单向透射率，$T_\zeta^2$ 即为往返双向透射率。$\zeta^{-2}$ 项刻画光束随距离的几何衰减，$\cos(\theta)$ 为入射角修正。

**离散化体渲染**。沿射线采样 $N$ 个点，假设每个采样段内介质均匀，则传感器接收的总辐射功率为：

$$P = \sum_{j=1}^{N} w_j \rho_{\zeta_j}'$$

其中 $\rho_{\zeta_j}'$ 为变换后的有效反射率，权重 $w_j$ 由双向透射率推导：

$$w_j = 2\alpha_{\zeta_j} \cdot \prod_{k=1}^{j-1} (1 - 2\alpha_{\zeta_k})$$

这里 $\alpha_{\zeta_j} = 1 - \exp(-\sigma_{\zeta_j}\delta_j)$ 为第 $j$ 段的吸收率，$\delta_j$ 为采样间隔。与标准NeRF的权重 $w_j^{\text{passive}} = \alpha_j \prod_{k=1}^{j-1}(1-\alpha_k)$ 相比，因子2的出现源于往返路径的双向衰减。该方程将LiDAR的主动传感物理精确编码为可微算子，是NFL相较基线方法取得显著提升的因果杠杆（消融实验证实该设计在所有设置下均提升范围精度，见Table 3）。

### 3.3 高斯光束发散建模

真实LiDAR光束随距离发散，其光斑半径由发散半角 $\gamma_0$ 和距离 $\zeta$ 决定。NFL将光束建模为高斯截面，在距离 $\zeta$、偏离中心角 $\gamma$ 处的辐照度为：

$$E(\zeta, \gamma) = \frac{2 I_0}{\pi (\gamma_0 \zeta)^2} \exp\left(-2 \frac{\gamma^2}{\gamma_0^2}\right)$$

为在体渲染中集成该模型，NFL将每束发散光离散为37条子射线，每条子射线独立执行前述体渲染，最终将各子射线的辐射功率加权聚合。该设计使NFL能够解释光束部分击中表面边缘时的范围偏差现象——这是LiDAR在高入射角下系统性地高估距离的物理根源（Figure 2）。

### 3.4 截断体渲染与二次回波

当发散光束同时击中两个不同距离的表面时，部分能量穿透第一表面后继续传播并产生二次回波。NFL通过**截断体渲染**处理这一现象：

1. **二次回波掩码预测**：MLP分支 $p_s$ 判断当前光束是否可能产生二次回波；
2. **第一回波估计**：按标准流程执行体渲染，通过粗到细峰值检测获得第一回波范围 $\zeta_1$；
3. **透射率重置**：在第一回波位置 $\zeta_1$ 之后，将透射率重置为初始值，相当于假设第一表面仅部分遮挡光束；
4. **第二回波估计**：对 $\zeta > \zeta_1$ 的区域重新执行体渲染，获得第二回波范围 $\zeta_2$。

该设计使NFL成为首个在神经渲染框架中显式建模多次回波的方案，Figure 4证实发散光束建模改善了双回波射线的范围误差分布。

### 3.5 范围估计与射线丢弃

**两阶段范围估计**。NFL不采用简单的加权求和，而是执行粗到细的峰值检测：

- **粗阶段**：在均匀采样点上计算权重 $\{w_j^c\}$，取最大权重位置作为粗峰值 $\zeta_p = \arg\max_j\{w_j^c\}$；
- **细阶段**：在 $\zeta_p$ 邻域内密集采样，以权重加权求和得到精细化范围 $\zeta_f = \sum_{j=1}^{N^f} w_j^f \cdot \zeta_j$。

**射线丢弃概率**。对于未击中任何表面的光束，NFL预测逐点丢弃概率 $p_d$，并通过体渲染积分得到整条射线的丢弃概率。该概率通过二元交叉熵和Lovasz损失进行监督，使模型学会识别天空、远处等无回波区域。

### 3.6 训练损失

总损失函数为四项的加权组合：

$$\mathcal{L} = \mathcal{L}_{\text{range}} + \lambda_e \mathcal{L}_e + \lambda_d \mathcal{L}_d + \lambda_s \mathcal{L}_s$$

- $\mathcal{L}_{\text{range}}$：粗、细两阶段的范围L1损失；
- $\mathcal{L}_e$：反射率（强度）的L2损失；
- $\mathcal{L}_d$：射线丢弃的BCE + Lovasz损失；
- $\mathcal{L}_s$：二次回波掩码的BCE + Lovasz损失。

该多任务损失设计使NFL在优化几何精度的同时，保持对LiDAR特有物理现象（射线丢弃、二次回波）的建模能力。

## 实验与分析

### 主实验结果

NFL在多个数据集和评估协议下均显著优于现有LiDAR新视角合成方法。Table 2报告了第一回波范围估计的核心结果：

- **TownClean数据集**：NFL的MAE为32.0 cm，LiDARsim为159.6 cm，误差降低127.6 cm（约80%）。倒角距离（CD）从23.5 cm降至9.0 cm。
- **TownReal数据集**：NFL的MAE为39.2 cm，LiDARsim为162.8 cm，误差降低123.6 cm。
- **Waymo Interp.（插值）**：NFL的MAE为30.8 cm，LiDARsim为116.3 cm，误差降低85.5 cm。
- **Waymo NVS（新视角合成）**：NFL的MAE为32.6 cm，LiDARsim为160.2 cm，误差降低127.6 cm。

在Waymo Interp.的全面射线测量评估中（Table 1），NFL在射线丢弃预测（精度、召回率）、双回波分割（IoU、召回率）以及第一/第二回波范围误差等指标上均优于i-NGP、DS-NeRF、URF和LiDARsim。定性结果（Figure 3）显示，NFL合成的扫描在射线丢弃模式（左侧，有/无回波射线着色）和强度值分布（右侧，0-0.25色阶）上与真实扫描高度一致。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/003_Figure.jpg]]
*Figure: (a) First return mask (b) Second return mask (c) LiDAR scans coloured by intensity values*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/008_Figure.jpg]]
*Figure: (b) 64 32 beam; → θ = θ0 − 2*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results of LiDAR novel view synthesis on Waymo Interp. dataset. On the left, we color-code rays with and without return. On the right side, LiDAR intensity values are color-coded as :0 0.25. Table 1. Comprehensive ray measurement evaluation of LiDAR novel view synthesis on Waymo Interp. dataset*

**证据强度**：Table 2的MAE和CD指标来自四个数据集，置信度0.95。Table 1的多指标评估进一步验证了NFL在射线丢弃和双回波建模上的优势。

### 消融实验

#### 主动传感体渲染 vs. 标准体渲染

Table 3的消融实验验证了双向透射率权重（Eq. 14）的核心贡献。将NFL的主动传感体渲染替换为标准NeRF单向透射率渲染后：

- TownClean上MAE从32.0 cm升至34.1 cm（+2.1 cm），CD从9.0 cm升至12.9 cm（+3.9 cm）。
- 在所有数据集和指标上均观察到一致的性能下降。

这表明双向透射率建模是范围精度提升的关键因果旋钮，而非网络容量或训练策略的附带效应。

#### 发散光束建模的影响

Figure 4展示了发散光束建模对双回波射线范围估计的影响。引入发散光束后：

- 双回波射线的第一回波和第二回波范围误差分布更集中，大误差样本减少。
- 但第一回波整体MAE略有上升（从32.8 cm到36.1 cm，Table 1），表明发散光束在改善双回波建模的同时，对单回波射线的范围估计引入了轻微干扰。

这种权衡是合理的：发散光束使能量分布更接近真实物理过程，对双回波场景（如透过树叶扫描建筑物）的改善尤为显著。

#### 二次回波分割特征消融

Table 7分析了光束特征和范围特征对二次回波分割的影响。结合光束特征（beam features）和范围特征（range features）可将二次回波分割召回率提升至82.1%，并改善第二回波范围估计精度。单独使用任一特征均导致性能下降，验证了两类特征信息的互补性。

#### 位移量鲁棒性

Table 6评估了NFL在不同新视角位移量下的鲁棒性。随着位移增大，所有方法的误差均上升，但NFL始终优于LiDARsim和i-NGP+L2基线，且大位移下优势更明显。这表明NFL的物理建模使其对视角外推具有更强的泛化能力。

### 下游任务验证

Table 4和Table 5分别报告了点云配准和语义分割的结果：

- **点云配准**：在TownClean、TownReal和Waymo三个数据集上，使用NFL合成扫描训练的配准模型，其配准精度均优于使用LiDARsim合成扫描训练的模型，缩小了与真实扫描训练的模型之间的域差距。
- **语义分割**：在Waymo Interp.数据集上，NFL合成数据训练的语义分割模型性能优于LiDARsim合成数据训练的模型，进一步验证了NFL合成扫描的真实性对感知任务的增益。

**证据强度**：下游任务结果置信度0.9，需要手动验证具体的配准误差数值和分割mIoU指标。

### 失败模式与局限性

1. **二次回波掩码预测精度有限**：精度55.6%，IoU 49.8%，表明模型在判断射线是否产生二次回波时仍有较大提升空间。这可能导致第二回波范围估计在部分场景下不可靠。

2. **发散光束的计算开销**：发散光束建模使每帧渲染时间从约2.4 ms增加到约4.1 ms（约1.7倍），在实时应用场景中可能成为瓶颈。

3. **射线丢弃的泛化性**：射线丢弃概率通过数据驱动方式学习，缺乏完整的物理模型支撑，在传感器参数或场景类型变化时可能泛化不足。

4. **静态场景假设**：NFL未显式建模动态物体，在包含移动车辆或行人的真实场景中可能产生伪影。

5. **极端天气未评估**：未在雨、雾等衰减效应显著的条件下测试，物理模型在这些场景下的有效性未知。

### 关键图表结论

- **Figure 1**：展示了NFL对LiDAR回波特性（单回波、双回波、射线丢弃）的建模机制，是理解方法设计的核心图示。
- **Figure 2**：揭示了光束发散和波形离散化导致的范围过估计效应，在高入射角和高距离区间尤为显著，为物理建模提供了动机。
- **Figure 4**：消融分析直接证明了发散光束建模对双回波射线范围精度的改善，误差分布的可视化对比清晰有力。
- **Figure 5**：展示了NFL在不同传感器参数（仰角、位置、光束数）下的新视角合成能力，验证了模型的灵活性和可控性。
- **Figure 6**：定性对比第一回波范围估计，高亮区域（误差>100 cm）直观展示了NFL相对于基线方法在大误差区域的显著减少。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/002_Figure_2.jpg]]
*Figure 2: The range accuracy of the LiDAR sensor is affected by waveform discretization and beam divergence. The LiDAR sensor has a tendency to overestimate range in high incidence angle regime, which becomes increasingly pronounced at higher range regimes (left). This is also reflected on TownReal dataset (right)*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/007_Figure_4.jpg]]
*Figure 4: Beam divergence modeling improves range accuracy of rays with dual returns. This is evident in the improved error distribution of the first (left) and second return range (right)*

### 补充图表

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/010_Table_4.jpg]]
*Table 4: Point cloud registration results on three datasets*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/018_Table_11.jpg]]
*Table 11: Point cloud registration results on three datasets. Table 12. Semantic segmentation results on Waymo NVS dataset*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/021_Figure_10.jpg]]
*Figure 10: Visualisation of Town dataset. Employing a diverged beam profile in range simulation results in an overestimation of range in the high range regime (-16 16 cm). Such range difference is also reflected on delicate structures, as evidenced by the point cloud view*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/005_Table_2.jpg]]
*Table 2: Results of LiDAR novel view synthesis for the first range*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/006_Table_3.jpg]]
*Table 3: Ablation study of volume rendering for active sensing*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/012_Table_6.jpg]]
*Table 6: Varying the displacement on Waymo NVS dataset. Numbers are reported as MedAE / CD [cm]*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2305_01643/figures/014_Figure_11.jpg]]
*Figure 11: Waymo dataset We use the following 4 scenes (cf . Fig. 11) that are mostly static from Waymo [48] dataset*

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

LiDAR新视角合成（Novel View Synthesis, NVS）面临一个根本性瓶颈：**现有方法依赖显式表面重建与理想射线投射，未能建模LiDAR主动传感的物理过程**。以LiDARsim为代表的“先重建后模拟”范式，首先通过多帧聚合构建稠密点云或网格，再在目标视角执行射线投射以生成模拟扫描。该管线引入两类系统性误差：（1）重建阶段的离散化与配准误差，导致几何代理不精确；（2）模拟阶段将LiDAR简化为理想针孔射线，忽略了光束发散、脉冲波形展宽和双向透射衰减等物理效应。这些简化使得合成扫描与真实扫描之间存在显著的域差距（domain gap），表现为范围估计偏差、二次回波缺失和射线丢弃模式不真实。

**核心因果旋钮**在于：将物理启发的LiDAR传感模型——双向透射率、高斯光束发散、脉冲波形——直接集成到可微神经体渲染框架中，使网络在优化场景表征的同时，隐式地学习匹配真实LiDAR的测量过程。这一设计使得NFL能够绕过显式几何重建的中间表示，从原始扫描数据端到端地学习场景的密度场和反射率场，从而产生更逼真的新视角扫描。

### 2. 方法谱系：从NeRF到主动传感体渲染

NFL的方法论定位处于**神经辐射场（NeRF）**与**物理LiDAR模拟**的交叉地带。其技术谱系可沿两条轴线追溯：

**轴线一：神经场景表征与体渲染。** NeRF（Mildenhall et al., ECCV 2020）建立了通过可微体渲染从多视图图像优化神经辐射场的范式。后续工作将这一思想扩展到不同传感器模态：DS-NeRF（Deng et al., CVPR 2022）利用稀疏深度监督增强几何一致性；URF（Rematas et al., CVPR 2022）将NeRF适配于城市场景的LiDAR深度监督。然而，这些方法均沿用**被动传感器体渲染方程**，即假设每条射线仅经历单向透射衰减 $T_\zeta$。NFL的关键突破在于识别出LiDAR作为**主动传感器**的本质差异：激光脉冲必须往返传播，因此透射率项应为 $T_\zeta^2$（双向透射率），对应的离散权重变为 $w_j = 2\alpha_{\zeta_j} \cdot \prod_{k=1}^{j-1} (1 - 2\alpha_{\zeta_k})$（Eq. 14）。这一修正在消融实验中被证明是NFL性能提升的核心来源（Table 3：TownClean上MAE降低2.1 cm，CD降低3.9 cm）。

**轴线二：LiDAR物理建模。** LiDARsim（Manivasagam et al., CVPR 2020）代表了显式重建后模拟的基线，其射线投射引擎考虑了表面反射率，但未建模光束发散和多次回波。NFL在此基础上引入了三个物理建模层次：
- **高斯光束发散**：将LiDAR光束建模为具有发散角 $\gamma_0$ 的高斯分布，通过37根子射线离散近似光束足迹（Eq. 5: $E(\zeta, \gamma) = \frac{2 I_0}{\pi (\gamma_0 \zeta)^2} \exp(-2 \frac{\gamma^2}{\gamma_0^2})$）。这使得NFL能够解释高入射角下的范围高估现象（Figure 2）。
- **截断体渲染（Truncated Volume Rendering）**：在估计首次回波后，重置透射率并在剩余区间执行第二次体渲染，以捕获二次回波（Figure 1b）。
- **射线丢弃概率**：通过可学习的每点丢弃概率 $p_d$，经体渲染积分得到每条射线的丢弃概率，替代LiDARsim中依赖数据驱动的学习式射线丢弃。

### 3. 与基线方法的关键差异

| 维度 | LiDARsim | i-NGP / DS-NeRF / URF | NFL (本文) |
|------|----------|----------------------|------------|
| **场景表征** | 显式网格/点云 | 神经辐射场（密度+颜色） | 神经场（密度+反射率+丢弃概率+二次回波掩码） |
| **渲染物理** | 理想射线投射 | 标准体渲染（单向 $T_\zeta$） | 主动传感体渲染（双向 $T_\zeta^2$） |
| **光束模型** | 单根理想射线 | 单根理想射线 | 高斯发散光束（37根子射线） |
| **二次回波** | 未建模 | 未建模 | 截断体渲染 |
| **射线丢弃** | 学习式 | 未建模 | 可学习概率+体渲染积分 |
| **范围估计** | 射线-表面交点 | 深度加权求和/L2优化 | 粗到细峰值检测+局部细化 |

从实验证据看，NFL在TownClean、TownReal、Waymo Interp.和Waymo NVS四个数据集上，第一回波范围MAE分别为32.0、39.2、30.8、32.6 cm，而LiDARsim对应为159.6、162.8、116.3、160.2 cm（Table 2），误差降低约**4-5倍**。i-NGP、DS-NeRF和URF等NeRF变体由于缺乏主动传感建模，范围误差普遍在100 cm以上，验证了物理模型集成的必要性。

### 4. 适用边界与局限

NFL的设计假设和实验设置定义了其当前适用边界：

**静态场景假设。** NFL未显式建模动态物体，训练和评估均在静态场景或单帧扫描上进行。对于包含移动车辆和行人的真实交通场景，动态目标会导致密度场的时间不一致，可能产生伪影。扩展到时空神经LiDAR场（spatio-temporal neural LiDAR fields）是一个开放问题。

**二次回波预测的精度瓶颈。** 尽管截断体渲染在概念上优雅，但二次回波掩码预测的性能仍有较大提升空间：精度55.6%，IoU 49.8%（Table 7）。这意味着近半数二次回波射线被误分类，可能限制该方法在需要精确多回波信息的应用（如植被穿透、透明表面检测）中的有效性。

**计算开销。** 发散光束建模将每帧渲染时间从约2.4 ms增加到4.1 ms（约1.7倍），对于实时应用（如自动驾驶仿真中的在线传感器模拟）可能构成瓶颈。如何通过神经网络近似光束积分或自适应子射线采样来降低开销，是工程化的关键问题。

**射线丢弃的泛化性。** 射线丢弃概率 $p_d$ 依赖数据驱动学习，缺乏全物理模型（如考虑目标反射率、距离、大气衰减的联合物理模型）。当部署到与训练数据分布不同的传感器或环境时，丢弃预测可能失准。作者也指出，将光束发散物理耦合到丢弃概率建模中（如通过集成位置编码）是一个值得探索的方向。

**极端条件未评估。** 论文未在雨、雾、雪等恶劣天气条件下进行实验。这些条件下，大气散射和衰减对LiDAR测量有显著影响，NFL的当前物理模型（仅考虑自由空间传播）可能不足以捕获这些效应。

### 5. 开放问题与后续工作方向

基于论文的局限性和方法设计空间，以下开放问题值得关注：

1. **动态场景建模**：如何将NFL扩展到包含动态目标的场景？可能的路径包括引入时间条件神经场、与目标检测/跟踪模块联合优化，或采用4D神经场表示。

2. **光束发散与丢弃的物理耦合**：当前射线丢弃概率是纯数据驱动的。能否将光束发散角、目标反射率和距离等物理量作为输入，构建更具泛化性的丢弃模型？作者建议的“集成位置编码”可能是一个起点。

3. **二次回波的感知价值量化**：二次回波数据缺乏语义标注，使得定量评估其对下游任务（如3D目标检测、语义分割）的贡献变得困难。需要建立包含多回波标注的基准，或设计自监督评估协议。

4. **传感器泛化**：NFL针对特定LiDAR传感器（Waymo数据集使用的64线LiDAR）设计。该方法能否迁移到不同线数、不同波长（如1550 nm vs 905 nm）、不同扫描模式（如固态LiDAR）的传感器？这需要验证物理模型参数的适配性和神经场的迁移能力。

5. **计算效率优化**：发散光束渲染的37根子射线离散近似是计算瓶颈。可能的加速策略包括：基于重要性采样的自适应子射线分配、利用神经网络的轻量级光束积分近似、或预计算光束足迹查找表。

6. **与其他传感模态的融合**：NFL当前仅使用LiDAR数据。结合相机图像的联合优化（类似于多模态NeRF）可能改善反射率估计和几何细节，尤其是在纹理丰富但LiDAR点稀疏的区域。

### 6. 知识库定位总结

NFL在方法谱系中的定位可概括为：**将主动传感物理模型嵌入神经体渲染框架的开创性工作**。它既不是对NeRF的简单适配（如DS-NeRF、URF），也不是对传统LiDAR模拟的增量改进（如LiDARsim）。其核心贡献在于识别并形式化了LiDAR体渲染与被动传感器体渲染的本质差异——双向透射率——并在此基础上系统性地集成了光束发散、多次回波和射线丢弃等物理效应。这一方法论框架为后续工作提供了两个可扩展的维度：（1）更精细的物理模型（如大气散射、目标表面BRDF）的集成；（2）更高效的神经渲染架构（如基于哈希网格的快速推理）的应用。

## 原文 PDF

![[paperPDFs/ICCV_2023/NFL_Neural_LiDAR_Fields_for_Novel_View_Synthesis.pdf]]
