---
title: "Hearing the Room Through the Shape of the Drum: Modal-Guided Sound Recovery from Multi-Point Surface Vibrations"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Hearing_the_Room_Through_the_Shape_of_the_Drum_Modal_Guided_Sound_Recovery_from_Multi_Point_Surface_Vibrations.pdf
project_link: null
code_link: null
aliases:
- MGSR
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过从多点二维振动数据中估计物体的模态频率和模态形状梯度，建立从声压到散斑位移的物理正向模型，并反向优化恢复原始声源信号。
primary_logic: 物体的振动模态构成一组正交基，已知模态频率和形状即可近似反转物体的时空传递函数，从而在抑制共振失真的同时融合多个测点信号，恢复干净、均衡的声音。
claims:
- 不同表面点对同一频率的振动存在相位反转，简单平均会抵消某些频率成分（图2b）。
- 方程式(8)建立了从声源信号到多点散斑位移的显式物理模型，通过模态形状梯度和模态脉冲响应连接。
- 优化式(12)同时完成反向滤波和去噪，能从多点信号中恢复接近原始声源的平坦频谱。
- 定量实验表明，所提方法在所有指标上均显著优于单点、平均和延迟求和基线，且与有监督的校准基线相当（表1-4，图7）。
---

# Hearing the Room Through the Shape of the Drum: Modal-Guided Sound Recovery from Multi-Point Surface Vibrations

> [!tip] 核心洞察
> 物体的振动模态构成一组正交基，已知模态频率和形状即可近似反转物体的时空传递函数，从而在抑制共振失真的同时融合多个测点信号，恢复干净、均衡的声音。

| 字段 | 内容 |
|------|------|
| 中文题名 | 听鼓辨室：基于模态引导的多点表面振动声音恢复 |
| 英文题名 | Hearing the Room Through the Shape of the Drum: Modal-Guided Sound Recovery from Multi-Point Surface Vibrations |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.26678) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Modal-Guided Sound Recovery |
| Dataset | 多物体测试集（鼓、相框、笔记本电脑、垃圾桶、吉他、活页夹、金属板、瑜伽砖、理疗球、气球等11种） |

> [!tip] 效果简介
> - 多物体测试集（鼓、相框、笔记本电脑、垃圾桶、吉他、活页夹、金属板、瑜伽砖、理疗球、气球等11种） 上，ViSQOLAudio-NSIM（原始感知相似度，↑） 0.39 vs 0.27 (DnS) (+0.12)。
> - 同上 上，ViSQOLAudio-MOS（平均意见分，↑） 2.01 vs 1.53 (DnS) (+0.48)；尺度不变多分辨率STFT距离（↓） 3.40 vs 3.55 (Single) (-0.15)；感知加权尺度不变多分辨率STFT距离（↓） 3.02 vs 3.43 (Single) (-0.41)。

## 概要

**问题瓶颈**：传统基于激光散斑的光学振动传感方法在“听振辨声”任务中存在根本性局限——单点测量仅能捕获物体表面单个位置的振动信号，而不同表面点对同一频率成分的响应存在相位反转和幅度差异（Figure 2b）。简单地对多点信号取平均会抵消特定频率成分，延迟求和（delay-and-sum）则无法处理不同模态引入的不同相位延迟，导致恢复的音频信号噪声大、频谱严重受物体共振特性染色，音色失真。

**核心思路**：本文提出 **Modal-Guided Sound Recovery**——一种基于物理正向模型与逆向优化的声音恢复方法。其核心洞察是：物体的振动模态构成一组正交基，一旦估计出模态频率和模态形状梯度，就可以近似反转物体的时空传递函数，从而在抑制共振失真的同时融合多个测点的振动信号，恢复出干净、均衡的原始声源。具体而言，方法从多点二维散斑位移数据中估计物体的模态频率和模态形状梯度，建立从声压到散斑位移的显式物理正向模型（Eq. 8），再通过带平滑正则化的梯度下降优化（Eq. 12）反向求解原始音频信号。

**方法定位**：相较于仅使用单点 x 轴振动信号的先前方法（如 Sheinin et al., CVPR 2018），以及简单平均和延迟求和等信号处理基线，本文首次将薄板/膜振动方程的模态叠加理论引入视觉声音恢复任务，实现了无监督的物理驱动信号融合与频谱均衡。与需要额外参考 chirp 信号进行逐点逆滤波器校准的监督基线相比，所提方法无需任何参考信号即可达到接近的恢复保真度（Figure 7）。

**主要结果**：在包含鼓、相框、笔记本电脑、垃圾桶、吉他、金属板、瑜伽砖等 11 种不同材质和形状物体的测试集上，所提方法在 ViSQOLAudio-NSIM（+0.12）、ViSQOLAudio-MOS（+0.48）、多分辨率 STFT 距离（−0.15）和感知加权 STFT 距离（−0.41）四项指标上均显著优于所有无监督基线（Tables 1–4）。定性结果表明，方法能有效恢复高频成分并抑制噪声，在不同材料和几何形状的日常物体上均表现出鲁棒性（Figures 5, 8）。



### 问题背景：从表面振动中恢复声音

物体的表面振动携带着周围声场的丰富信息。当声波作用于物体表面时，物体会发生微小的机械振动，通过光学手段（如激光散斑干涉）可以非接触地测量这些振动，进而反向推断声源信号。这种“视觉麦克风”范式在远程窃听、工业监测、声学取证等场景中具有重要应用价值。

传统的光学振动传感方法——如基于激光散斑的单点振动测量——已经能够从薄膜、纸张等振动响应良好的物体上恢复出可懂的声音信号。然而，现实世界中的物体（如墙壁、门板、桌面、金属外壳）往往是厚度较大、刚度较高的固体结构，它们的振动行为远比薄膜复杂：**同一物体上不同空间位置的振动信号之间存在频率依赖的相位延迟和幅度差异**。

### 核心瓶颈：频率依赖的耦合与信号融合困境

图2(b)揭示了一个关键现象：在鼓面上两个不同测点（红色和绿色），当声源频率为198 Hz时，两点的振动信号反相；而当频率为411 Hz时，两点振动同相。这意味着，**简单地对多点信号取平均会抵消某些频率成分**（如198 Hz分量被抑制），导致恢复的声音频谱严重失真。

此外，图2(c)展示了另一个难题：靠近模态形状峰值或谷值的测点（如蓝色点），由于表面位移的空间梯度在该处趋于零，该点对特定模态频率的振动响应极弱——换句话说，**单个测点天然地“听不见”某些频率成分**。

这些现象共同构成了本领域的核心瓶颈：

1. **单点测量信噪比低**：对于弱响应或高共振的固体物体，单个测点的信号往往被噪声淹没，且无法覆盖所有频率成分。
2. **简单融合策略失效**：平均法（Avg）因相位抵消而损失频率成分；延迟求和法（DnS）虽能补偿全局时延，但无法处理不同模态引入的不同相位延迟（见图4(c)）。
3. **共振失真难以消除**：物体的固有共振频率会在恢复信号中产生强烈的频谱峰，导致音色严重偏离原始声源。

### 核心洞察：模态作为正交基

本文的核心洞察在于：**物体的振动模态构成一组空间上的正交基**。对于线弹性薄板/膜结构，其表面位移 $u(\mathbf{x}, t)$ 可以展开为模态形状 $\phi_k(\mathbf{x})$ 与模态坐标 $q_k(t)$ 的叠加：

$$u ( \mathbf { x } , t ) = \sum _ { k = 1 } ^ { K } \phi _ { k } ( \mathbf { x } ) q _ { k } ( t )$$

每个模态坐标满足一个由声压 $p(t)$ 驱动的二阶微分方程：

$$\ddot { q } _ { k } ( t ) + 2 \zeta _ { k } \omega _ { k } \dot { q } _ { k } ( t ) + \omega _ { k } ^ { 2 } q _ { k } ( t ) = \alpha _ { k } p ( t ) + \eta _ { k } ( t )$$

这意味着：**一旦知道物体的模态频率 $\omega_k$ 和模态形状 $\phi_k(\mathbf{x})$，就可以近似反转物体对声源的时空传递函数**——在抑制共振失真的同时，融合多个测点的信号，恢复出干净、均衡的声音。

### 本文动机与目标

基于上述洞察，本文提出**模态引导的声音恢复（Modal-Guided Sound Recovery）**方法，旨在解决以下问题：

- **建立物理正向模型**：从声压到多点散斑位移的显式映射关系，通过模态形状梯度和模态脉冲响应连接（见公式(8)）。
- **实现无监督逆向求解**：无需额外的参考信号或校准过程，仅从多点振动数据中估计模态参数，并通过优化反演原始声源信号。
- **实现频谱均衡**：通过模态传递函数的逆向调整，压制共振峰，恢复平坦、自然的音频频谱（见图4(d)）。

该方法在11种不同材料、形状的日常物体上进行了验证，结果表明其在多项感知音频质量指标上显著优于单点、平均和延迟求和基线，且与需要参考信号的监督校准基线性能相当。



## 核心方法与创新机理

本工作针对“从物体表面振动中恢复场景声音”这一任务，提出了**模态引导的声音恢复（Modal-Guided Sound Recovery）** 方法。其核心创新在于将传统“单点/简单融合”的信号处理范式，转变为**基于物理正向模型与逆向优化的模态分解与均衡框架**。以下从四个关键维度（changed slots）展开对比分析。

### 1. 输入信号：从单点单轴到多点双轴散斑位移

传统激光散斑振动测量方法仅采集单个表面点的单轴（通常为x轴）振动信号（如 Sheinin et al., CVPR 2018 等工作）。这种单点测量对振动响应良好的薄膜物体尚可，但对于弱响应或高共振的固体物体，单点信号信噪比低，且无法获取物体振动的空间分布信息。

本方法将输入扩展为**二维网格上N个点的双轴散斑位移信号** $\mathbf{v}(\mathbf{x}_n, t) \in \mathbb{R}^2$（见 Figure 1）。这一改变是后续所有物理建模的基础——只有获取了空间分布的双轴振动，才能估计模态形状的梯度场，进而建立声源到多点测量的正向映射。

### 2. 信号融合策略：从简单平均/延迟求和方法到物理逆向优化

基线方法对多点信号的融合停留在信号处理层面：
- **Naive Averaging (Avg)**：直接对所有测点信号取平均。如图2(b)所示，不同表面点对同一频率的振动存在**相位反转**（如198 Hz处红绿两点反相振荡，411 Hz处则同相），简单平均会抵消特定频率成分，导致频谱失真。
- **Delay-and-Sum (DnS)**：估计全局时延后求和。但不同模态频率诱导的相位延迟各异，单一全局时延无法补偿频率依赖的相位差异，高频模态尤其受损（Figure 4(c)）。

本方法的核心突破在于**通过模态分解建立了从声源到多点散斑位移的显式物理正向模型**（Eq. (8)）：

$$\mathbf { v } ( \mathbf { x } _ { n } , t ) \approx \gamma \beta \sum _ { k = 1 } ^ { K } \nabla \phi _ { k } ( \mathbf { x } _ { n } ) \left( s ( t ) * g _ { k } ( t ) \right) + \eta ( \mathbf { x } _ { n } , t )$$

该模型揭示了三个关键物理量之间的耦合关系：
- **模态形状梯度** $\nabla \phi_k(\mathbf{x}_n)$：描述第k阶模态在测点n处的空间灵敏度，解释了为何某些点对特定频率“失聪”（梯度为零的模态峰/谷处信号能量微弱，见 Figure 2(c)）。
- **模态脉冲响应** $g_k(t)$：对应二阶线性振荡器的传递函数（Eq. (5)），刻画了物体对声源的频率选择性放大/衰减。
- **声源信号** $s(t)$：待恢复的未知量。

基于此正向模型，声音恢复被形式化为一个**逆向优化问题**（Eq. (12)）：

$$\operatorname* { argmin } _ { s ( t ) , \alpha _ { k } } \biggl \| \mathbf { v } ( \mathbf { x _ { n } } , t ) - \sum _ { k = 1 } ^ { K } \nabla \hat { \phi } _ { k } ( \mathbf { x } _ { n } ) \left( s ( t ) * \hat { g } _ { k } ( t ) \right) \biggl \| _ { 2 } ^ { 2 } + \lambda \| \dot { s } ( t ) \| _ { 2 } ^ { 2 }$$

该优化以未知声源 $s(t)$ 和模态耦合系数 $\alpha_k$ 为变量，同时最小化测量与模型预测的误差，并加入平滑正则化项抑制噪声。通过梯度下降求解，**隐式地完成了对物体共振传递函数的逆向滤波**，从而在融合多点信号时自动补偿频率依赖的相位延迟和幅度差异。

### 3. 频谱均衡：从保留共振失真到“等化”物体声学

传统方法（单点、平均、延迟求和）直接输出振动信号的某种组合，其结果完整保留了物体的共振特性——共振频率被过度放大，形成“音色失真”（Figure 4(a)-(c)中可见尖锐的共振峰）。

本方法通过逆向优化**主动压制共振峰**：模态传递函数 $G_k(\omega)$（Eq. (5)）在共振频率 $\omega_k$ 处具有高增益，优化过程通过调整 $s(t)$ 来抵消这一增益，使得恢复信号的频谱趋于平坦（Figure 4(d)）。这一“等化”效应是方法能够输出干净、均衡声音的关键，也是其与校准基线（Chirp inverse filter）性能接近的根本原因（Figure 7）。

### 4. 表面物理模型：从无显式模型到模态叠加理论

基线方法未对物体表面振动建立物理模型，隐含假设各测点信号独立或仅存在简单时延关系。

本方法构建了完整的**薄板/膜振动模态叠加理论**作为正向模型的基础：
- 从一般波动方程（Eq. (1)）出发，通过模态展开 $u(\mathbf{x}, t) = \sum \phi_k(\mathbf{x}) q_k(t)$（Eq. (2)）将连续体振动离散化为模态坐标的二阶微分方程（Eq. (3)）。
- 利用散斑位移与表面梯度成正比的关系 $\mathbf{v} = \beta \nabla_{\mathbf{x}} u$（Eq. (7)），将声压驱动下的模态动力学映射到可测量的散斑位移。
- 模态频率通过多点频谱标准差 $\sigma(\omega) = \mathrm{std}_n(|\mathbf{V}_n(\mathbf{x}_n, \omega)|)$ 检测（Eq. (13)），并经相关性筛选和总变差检验进行鲁棒估计（Figure 3），无需事先知晓物体的材料参数或几何形状。

这一物理模型使得方法能够**从数据中自适应地提取物体的“声学指纹”（模态频率与形状梯度）**，并用其反转物体的时空传递函数，从而在多种材料（木、金属、塑料、橡胶）和形状（平面、曲面、不规则）的日常物体上均取得优于基线的效果（Figure 5, Figure 8）。

### 创新总结

| 维度 | 先前方法基线 | 本方法（模态引导） | 关键机理 |
|------|-------------|-------------------|---------|
| 输入信号 | 单点单轴振动 | 多点双轴散斑位移 | 获取空间梯度信息 |
| 融合策略 | 平均/延迟求和 | 物理正向模型+逆向优化 | 频率依赖相位补偿 |
| 频谱处理 | 保留共振失真 | 逆向等化共振峰 | 模态传递函数反转 |
| 物理模型 | 无 | 模态叠加理论 | 数据驱动的模态提取 |

本方法的本质洞见在于：**物体的振动模态构成一组正交基，已知模态频率和形状即可近似反转物体的时空传递函数**，从而在抑制共振失真的同时融合多个测点信号，恢复干净、均衡的场景声音。



本文提出**模态引导的声音恢复**（Modal-Guided Sound Recovery）方法，其核心pipeline由四个紧密耦合的模块构成，形成“测量→模态估计→正向建模→逆向求解”的闭环。

### 1. 多点多轴散斑振动采集

系统使用激光散斑成像装置，在物体表面投射并采集 $N$ 个网格点的时变散斑图案。每个测点 $\mathbf{x}_n$ 输出双轴位移信号 $\mathbf{v}(\mathbf{x}_n, t) \in \mathbb{R}^2$，分别对应 $x$ 和 $y$ 方向的表面梯度响应（**Figure 1**）。与以往仅使用单点单轴信号的方法（如 **Sheinin et al., CVPR 2018**）相比，多点双轴采集为后续的模态分解和信号融合提供了空间冗余和方向信息。

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/001_Figure_1.jpg]]
*Figure 1: We introduce a novel approach for sound recovery from multi-point, speckle-based vibration measurements. Our system captures a grid of speckle-based vibration signals across an object’s surface. We derive a novel vibration forward model connecting the multi-point two-axis measurements to the underlying scene sound source. The model relies on extracting the object’s vibrational modes from the data. Then, we invert the model to estimate the scene sound source via optimization, yielding superior sound recoveries*

### 2. 鲁棒模态频率估计

从多点频谱中自动检测物体的振动模态频率，是整个pipeline的关键前置步骤。该模块分三阶段进行（**Figure 3**）：

- **候选检测**：计算所有测点频谱幅值的标准差 $\sigma(\omega)$（式13），在平滑后的 $\sigma(\omega)$ 曲线上检测局部峰值作为候选模态频率。其物理直觉是：在模态频率处，不同表面点的振动幅度差异最大。
- **空间相关性剪枝**：对候选模态按频率升序逐一检验，若当前候选模态的形状梯度与已接受模态高度空间相关，则判定为重复或谐波伪影并剔除。
- **总变差（TV）离群值剔除**：计算剩余候选模态形状梯度的空间总变差。根据物理规律，模态空间复杂度应随频率单调递增；违反此趋势的模态被标记为离群值并移除。

最终输出一组鲁棒的模态频率估计 $\{\hat{\omega}_k\}_{k=1}^{K}$。

### 3. 模态形状梯度提取

在检测到的每个模态频率 $\hat{\omega}_k$ 处，利用各测点双轴频域信号的相对幅度和相位，提取归一化的模态形状梯度 $\nabla\hat{\phi}_k(\mathbf{x}_n)$（式11）。该步骤直接为正向模型提供空间基函数，无需预先知道物体的几何或材料参数。

### 4. 正向模型与逆向优化求解

**正向模型**（式8）建立了从场景声源信号 $s(t)$ 到多点散斑位移 $\mathbf{v}(\mathbf{x}_n, t)$ 的显式物理映射：

$$\mathbf{v}(\mathbf{x}_n, t) \approx \gamma\beta \sum_{k=1}^{K} \nabla\phi_k(\mathbf{x}_n) \left( s(t) * g_k(t) \right) + \eta(\mathbf{x}_n, t)$$

其中 $g_k(t)$ 为第 $k$ 阶模态的脉冲响应（对应二阶线性振荡器，式5），$\nabla\phi_k(\mathbf{x}_n)$ 为模态形状梯度，$\eta$ 为噪声项。该模型的核心洞察是：**测量信号是声源经过各模态传递函数滤波后，再按模态形状梯度在空间上加权叠加的结果**。

**逆向求解**（式12）将声音恢复形式化为优化问题：

$$\operatorname*{argmin}_{s(t), \alpha_k} \left\| \mathbf{v}(\mathbf{x}_n, t) - \sum_{k=1}^{K} \nabla\hat{\phi}_k(\mathbf{x}_n) \left( s(t) * \hat{g}_k(t) \right) \right\|_2^2 + \lambda \|\dot{s}(t)\|_2^2$$

以未知声源 $s(t)$ 和模态耦合系数 $\alpha_k$ 为优化变量，最小化测量信号与模型预测之间的残差，同时加入声源导数的 $\ell_2$ 正则化以抑制噪声。通过梯度下降联合优化，该过程同时实现了三个目标：**（1）反转物体的共振传递函数，实现频谱均衡；（2）利用模态形状梯度隐式编码的频率依赖相位关系，融合多点信号；（3）通过正则化进行去噪**。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| 振动采集 | 物体表面激光散斑图像序列 | $N$ 点双轴时变位移 $\mathbf{v}(\mathbf{x}_n, t)$ |
| 模态频率估计 | 多点位移信号的频谱 | 鲁棒模态频率集合 $\{\hat{\omega}_k\}$ |
| 形状梯度提取 | 模态频率处的频域信号 | 归一化模态形状梯度 $\nabla\hat{\phi}_k(\mathbf{x}_n)$ |
| 逆向优化 | 测量信号 + 模态参数 | 恢复的声源信号 $\hat{s}(t)$ |

整个pipeline无需任何参考信号或监督训练，仅依赖一段宽带激励（如偶然拍手声）即可完成模态标定，随后对任意新声源进行恢复。



### 正向物理模型：从声压到散斑位移

本方法的核心在于建立了一个显式的物理正向模型，将场景中的未知声源信号 $s(t)$ 映射到物体表面 $N$ 个测点处测量到的双轴散斑位移 $\mathbf{v}(\mathbf{x}_n, t)$。该模型的推导分为三个层次：

**第一层：表面位移的模态展开。** 对于薄、线弹性表面，其横向位移 $u(\mathbf{x}, t)$ 满足波动方程（Eq. 1），并可展开为 $K$ 阶模态的叠加：

$$u(\mathbf{x}, t) = \sum_{k=1}^{K} \phi_k(\mathbf{x}) q_k(t)$$

其中 $\phi_k(\mathbf{x})$ 为第 $k$ 阶模态形状，$q_k(t)$ 为对应的模态坐标。每个模态坐标由声压 $p(t)$ 驱动的二阶阻尼振荡方程描述（Eq. 3），其频域传递函数为一个二阶线性振荡器：

$$G_k(\omega) = \frac{\alpha_k}{-\omega^2 + j 2\zeta_k \omega_k \omega + \omega_k^2}$$

其中 $\omega_k$ 为模态频率，$\zeta_k$ 为阻尼比，$\alpha_k$ 为模态耦合系数（表征声压对该模态的激发效率）。

**第二层：散斑位移与表面梯度。** 激光散斑测振系统测量的散斑位移正比于表面位移的空间梯度，而非位移本身：

$$\mathbf{v}(\mathbf{x}_n, t) = \beta \nabla_{\mathbf{x}} u(\mathbf{x}_n, t)$$

其中 $\beta$ 为系统增益常数。这一关系是方法的关键约束：在模态形状的峰/谷处（梯度为零），即使位移很大，测量信号也几乎为零（见图 2(c) 中蓝色点缺乏 411 Hz 附近频谱成分的现象）。

**第三层：正向模型的完整形式。** 将模态展开代入梯度关系，并引入声源信号 $s(t)$（假设声压 $p(t) \propto s(t)$），得到正向模型：

$$\mathbf{v}(\mathbf{x}_n, t) \approx \gamma\beta \sum_{k=1}^{K} \nabla\phi_k(\mathbf{x}_n) \left( s(t) * g_k(t) \right) + \eta(\mathbf{x}_n, t)$$

其中 $\gamma$ 为声压-力耦合系数，$g_k(t)$ 为模态脉冲响应（$G_k(\omega)$ 的时域形式），$\eta$ 为测量噪声。该模型揭示了**频率依赖的空间耦合**机制：不同测点对同一频率成分的响应由模态形状梯度 $\nabla\phi_k(\mathbf{x}_n)$ 加权，导致某些测点间可能反相，简单平均会抵消特定频率成分（图 2(b) 中红绿点在 198 Hz 反相、411 Hz 同相的现象）。

### 模态频率估计

从多点振动数据中鲁棒地检测模态频率是方法的关键前置步骤。流程分三步（图 3）：

**候选频率检测。** 计算各测点频谱幅值在空间上的标准差 $\sigma(\omega)$：

$$\sigma(\omega) = \mathrm{std}_n \left( |\mathbf{V}_n(\mathbf{x}_n, \omega)| \right)$$

在模态频率处，不同测点因位于模态形状不同位置而呈现显著的能量差异，使得 $\sigma(\omega)$ 出现峰值。通过平滑后检测峰值获得候选频率 $\{\hat{\omega}_k\}$。

**空间相关性筛选。** 对候选频率按能量降序处理，计算当前候选的模态形状梯度与已接受模态的空间相关性。若相关性过高（表明为同一模态的谐波或虚假峰），则剔除该候选（图 3(b) 红色标记）。

**总变差（TV）异常值剔除。** 根据物理规律，模态空间复杂度应随频率单调增加。对剩余候选计算其模态形状梯度的总变差，剔除违反单调递增规律的异常值（图 3(c) 青色标记），最终得到鲁棒的模态频率集合。

### 模态形状梯度提取

在检测到的模态频率 $\hat{\omega}_k$ 处，利用双轴频域信号的相对幅度和相位提取归一化的模态形状梯度：

$$\nabla\hat{\phi}_k(\mathbf{x}_n) = \mathrm{Re}\left\{ \frac{\mathbf{V}(\mathbf{x}_n, \hat{\omega}_k) \cdot \mathbf{V}_1(\mathbf{x}_0, \hat{\omega}_k)^{*}}{\mathbb{E}_{n,a}[|\mathbf{V}(\mathbf{x}_n, \hat{\omega}_k)|] \cdot |\mathbf{V}_1(\mathbf{x}_0, \hat{\omega}_k)|} \right\}$$

该式以参考点 $\mathbf{x}_0$ 的 x 轴分量为基准，对幅度做全局归一化，从而获得无量纲的模态形状梯度分布。这些梯度向量构成了正向模型中连接各测点的空间权重。

### 逆向优化恢复声源

给定估计的模态频率 $\hat{\omega}_k$ 和模态形状梯度 $\nabla\hat{\phi}_k(\mathbf{x}_n)$，声源恢复转化为以 $s(t)$ 和模态耦合系数 $\alpha_k$ 为变量的优化问题：

$$\operatorname*{argmin}_{s(t), \alpha_k} \left\| \mathbf{v}(\mathbf{x}_n, t) - \sum_{k=1}^{K} \nabla\hat{\phi}_k(\mathbf{x}_n) \left( s(t) * \hat{g}_k(t) \right) \right\|_2^2 + \lambda \|\dot{s}(t)\|_2^2$$

目标函数的第一项最小化模型预测与实测散斑位移的误差，第二项为声源信号导数的 $\ell_2$ 正则化（抑制高频噪声）。该优化通过梯度下降求解，**同时完成三项任务**：(1) 利用模态形状梯度融合 $N$ 个测点的信号；(2) 通过模态传递函数的逆向调整压制共振峰，实现频谱“等化”；(3) 正则化项提供去噪。

### 关键变量含义对照

| 符号 | 含义 |
|------|------|
| $s(t)$ | 待恢复的场景声源信号 |
| $\mathbf{v}(\mathbf{x}_n, t)$ | 位置 $\mathbf{x}_n$ 处的双轴散斑位移测量 |
| $\phi_k(\mathbf{x})$ | 第 $k$ 阶模态形状 |
| $\nabla\phi_k(\mathbf{x}_n)$ | 第 $k$ 阶模态形状在 $\mathbf{x}_n$ 处的空间梯度 |
| $\omega_k, \zeta_k, \alpha_k$ | 第 $k$ 阶模态的频率、阻尼比、耦合系数 |
| $g_k(t)$ | 第 $k$ 阶模态的脉冲响应 |
| $\gamma, \beta$ | 声压-力耦合系数、散斑系统增益常数 |
| $\sigma(\omega)$ | 多点频谱幅值的空间标准差，用于检测模态频率 |

### 补充图表

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/002_Figure_2.jpg]]
*Figure 2: Frequency-dependent coupling of speckle shifts across surface points. We measure drum membrane vibrations in response to a logarithmic chirp using a 10×10 speckle grid. Different audio frequencies produce distinct vibration patterns. (a) Two-axis speckle shifts at two resonant frequencies (top) and their corresponding integrated mode shapes (bottom). (b) Speckle shifts are frequency-coupled: the red and green points oscillate out of phase at 198 Hz but in phase at 411 Hz, so averaging them suppresses 198 Hz components. (c) Points near mode-shape peaks or valleys (where gradients vanish) show weak signal energy at that mode, e.g., the blue point lacks spectral content near 411 Hz*

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/003_Figure_3.jpg]]
*Figure 3: Robust mode estimation. (a) Initial mode candidates are obtained by detecting peaks on the smoothed vibration spectrum*



## 实验与关键发现

### 主实验结果

论文在11种日常物体（鼓、相框、笔记本电脑、垃圾桶、吉他、活页夹、金属板、瑜伽砖、理疗球、气球等）上进行了系统评估，以原始声源信号为参考，对比了四种方案：单点信号（Single）、简单平均（Avg）、延迟求和（DnS）和所提模态引导方法（Ours）。

**核心发现：所提方法在所有四项指标上均显著优于所有无监督基线，且与有监督的校准基线相当。**

- **ViSQOLAudio-NSIM**（原始感知相似度，↑）：Ours 达到 **0.39**，DnS 为 0.27，Single 为 0.23（Table 1）。该指标在映射到 MOS 之前度量耳蜗图块之间的结构相似性，提升幅度表明恢复信号与原始声源在感知结构上更接近。
- **ViSQOLAudio-MOS**（平均意见分，↑）：Ours 达到 **2.01**，DnS 为 1.53，Single 为 1.47（Table 2）。该指标将耳蜗图相似度映射为听觉主观质量预测，Ours 的提升说明听感质量有实质改善。
- **尺度不变多分辨率 STFT 距离**（↓）：Ours 为 **3.40**，Single 为 3.55，DnS 为 3.58（Table 3）。该指标衡量频谱距离，Ours 取得最优值。
- **感知加权 STFT 距离**（↓）：Ours 为 **3.02**，Single 为 3.43，DnS 为 3.49（Table 4）。加入感知加权后，Ours 的优势进一步扩大（相对 Single 降低 0.41），说明恢复信号在听觉敏感频段更接近原始声源。

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/009_Table_1.jpg]]
*Table 1: ViSQOLAudio-NSIM [22, 23] (higher is better). The raw perceptual similarity index used inside ViSQOLAudio before Mean Opinion Score (MOS) mapping. It measures structural similarity between cochleagram patches of the reference and degraded signals and is not tied to speech-specific MOS training. Higher values indicate closer perceptual similarity*

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/010_Table_2.jpg]]
*Table 2: ViSQOLAudio-MOS [23] (higher isbetter). Perceptual audio-quality metric based on the ViSQOLAudio model. It compares a reference and degraded signal using a cochleagram frontend and patch-based similarity, then maps the result to a Mean Opinion Score (MOS) prediction. Originally trained on generalaudio listening tests, it approximates subjective quality*

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/011_Table_3.jpg]]
*Table 3: Scale Invariant, Multi Resolution STFT distance [41, 52] (lower is better). A distance metric between recovered signal and reference source signal. The measure is a scale invariant, multi resolution STFT distance*

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/012_Table_4.jpg]]
*Table 4: Scale Invariant, Multi Resolution STFT distance (Perceptual weighting) [41, 52] (lower is better). A distance metric between recovered signal and reference source signal. The measure is a scale invariant, multi resolution STFT distance with perceptual weighting*

值得注意的是，简单平均（Avg）在多数指标上反而劣于单点（Single），验证了 Figure 2(b) 揭示的瓶颈：不同表面点在同一频率上可能反相振荡，直接平均会抵消该频率成分，导致信息丢失。延迟求和（DnS）通过估计全局时延部分改善了低频对齐，但无法处理不同模态引入的不同相位延迟，因此在高频段仍表现不佳。

### 消融实验

**1. 模态频率来源的影响（Figure 6a-b）**

实验对比了两种模态频率提取方式：从一段偶然拍手声（clap）中提取，与直接从目标录音中提取。两者重建的音频质量和音色特征相当，说明方法对激励源的类型不敏感——只要激励信号具有足够的宽带能量以激发各阶模态，即可获得有效的模态频率估计。这一特性降低了实际部署的门槛。

**2. 模态频率准确性的影响（Figure 6c）**

通过人为扰动模态频率集合来检验鲁棒性：
- **随机丢弃 20% 的模态频率**：重建音频的清晰度略有下降，但总体音色特征得以保留；
- **随机添加 20% 的虚假频率**：重建音频引入明显的非自然共振和可听伪影。

这一对比揭示了方法的非对称敏感性：遗漏真实模态的代价相对温和（仅损失部分频率成分），而引入虚假模态的代价更为严重（产生不存在的共振峰）。该发现指向一个关键改进方向——模态频率检测的精确率（减少虚假峰）比召回率（检测所有真实模态）对最终恢复质量更为关键。

**3. 与校准基线的对比（Figure 7）**

论文还构建了一个有监督的校准基线：使用一段已知的参考 chirp 信号，通过最小二乘求解每个测点通道的逆滤波器（Eq. 15），然后将逆滤波后的多通道信号平均。所提方法无需任何额外参考信号或监督，即可重建出大部分频率成分，保真度接近校准基线。这表明基于物理模型的逆向优化能够有效逼近通过显式校准获得的逆传递函数。

**4. 跨材料与几何形状的泛化（Figure 5, Figure 8）**

方法在木材、金属、塑料、橡胶等多种材料，以及平面、曲面、不规则形状的物体上均取得优于基线的效果。即使在表面覆盖不完全或形状不规则的条件下（如垃圾桶、吉他），方法仍能输出去噪且频谱均衡的重建信号。唯一的例外是薯片袋（chips bag）——单点信号本身已表现良好，因为该物体振动响应较为均匀，多点融合的增益有限。

### 失败模式与局限性

论文明确讨论了以下局限和失效场景：

1. **线性假设的边界**：正向模型基于薄板/膜的线性小变形假设（Eq. 1），对于非线性大变形或强耦合振动场景不适用。当物体振动幅度过大或材料非线性显著时，模态叠加框架将失效。

2. **高频模态检测受限**：受限于空间采样密度（激光散斑网格的分辨率）和振动幅度随频率升高而衰减的物理规律，高频模态可能检测不全或信噪比不足。这在高频信息对音色感知重要的场景（如金属撞击声）中可能影响恢复质量。

3. **虚假模态峰的敏感性**：如消融实验所示，模态频率检测对虚假峰敏感，可能引入可听伪影。当前的鲁棒估计流程（Figure 3）通过空间相关性和总变差筛选来抑制虚假峰，但无法完全消除该风险。

4. **物体假设**：方法假设所有测点属于同一物体且物体表面静止。对于多物体耦合振动或物体整体运动的场景，当前模型无法直接适用。

5. **激励需求**：需要一段较长时间的宽带激励以充分激发各阶模态。在仅有窄带或瞬态激励的条件下，部分模态可能未被激发，导致模态频率估计不完整。

### 关键图表结论

- **Figure 4**：在鼓面场景中，单点信号噪声大且频谱受共振峰支配；简单平均因反相抵消丢失频率成分；延迟求和无法对齐高频模态的相位差异；所提方法在抑制噪声的同时有效均衡了频谱，恢复了接近原始声源的宽带信号。
- **Figure 5/Figure 8**：跨物体定性结果验证了方法的泛化能力。频谱图显示，所提方法恢复的信号在时频结构上与原始声源高度一致，而基线方法通常残留明显的共振条纹或噪声。
- **Table 1-4**：定量指标一致表明 Ours > DnS ≈ Single > Avg 的排序，且 Ours 与校准基线的差距远小于与无监督基线的差距。

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/004_Figure_4.jpg]]
*Figure 4: Sound recovery from a drumhead. We capture the speckle vibrations of a drumhead excited by a speaker using a 10×10 speckle point grid. (a) The drumhead membrane has a poor and highly resonant reaction to the speaker’s sound, yielding individual noisy measurements. (b) Averaging all measured vibrations suppresses important frequencies due to their temporal misalignment. (c) Estimating a global temporal delay between the signals prior to averaging fails to keep high-frequency modes, as different modes induce different phase delays between the points. (d) Our result takes into account the physics of the vibrating surface and recovers higher frequencies while significantly suppressing noise. (e...*

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/005_Figure_5.jpg]]
*Figure 5: Results across objects having various geometries and materials. The top row (chips bag) serves as a reference– where a single point already performs well. All subsequent objects present greater challenges due to diverse materials, thicknesses, and shapes. Despite limited or irregular surface coverage, our method yields denoised reconstructions. The final example (drum) further demonstrates robustness under dual sound sources*

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/008_Figure_8.jpg]]
*Figure 8: Results across objects having various geometries and materials. All objects present challenges due to diverse materials, thicknesses, and shapes. Despite limited or irregular surface coverage, our method yields denoised reconstructions*

### 补充图表

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/006_Figure_6.jpg]]
*Figure 6: The experiment compares reconstructions whose modefrequencies were obtained from different sources or from sources perturbed by random omission/addition. Inaccurate frequency detection introduces audible artifacts*

![[assets/figures/papers/paper_list_l2084_https_arxiv_org_abs_2604_26678/figures/007_Figure_7.jpg]]
*Figure 7: Comparison between our model-based sound recovery and a calibrated baseline using a reference chirp signal. Our method reconstructs most of the frequency content with high fidelity, closely matching the calibrated result without using any additional intervening signals or supervision*



## 定位与知识库关联

### 1. 问题定位：从“看”振动到“听”声音

本文解决的核心问题是**通过物体表面振动反向恢复场景声源**，属于计算成像与声学感知的交叉领域。传统激光散斑振动测量方法（如 **Sheinin et al., CVPR 2018**；**Davis et al., SIGGRAPH 2014**）通过分析散斑图案的时变位移，从单一表面点的单轴振动信号中恢复声音。这类方法在振动响应良好的薄膜物体（如薯片袋）上表现尚可，但面对弱响应或高共振的固体物体时，单点测量信噪比低，且恢复的音频被物体共振频率严重染色，音色失真。

本工作的核心洞察在于：**物体的振动模态构成一组正交基，已知模态频率和形状即可近似反转物体的时空传递函数**。这一思想将问题从“信号处理”提升到“物理建模”层面——不是简单地增强或融合信号，而是建立从声压到多点散斑位移的显式物理正向模型，再通过优化逆向求解恢复原始声源。

### 2. 与基线的关键差异：四个维度的方法论跃迁

与已有方法相比，本文在四个关键维度上实现了结构性改变：

| 维度 | 先前方法 | 本文方法 | 机制性优势 |
|------|----------|----------|------------|
| **输入信号** | 单个表面点的单轴（通常x轴）振动信号 | 2D网格（N个点）的双轴散斑位移信号 | 捕获空间梯度信息，为模态分解提供几何约束 |
| **信号融合策略** | 简单平均（Avg）或基于全局时延的延迟求和（DnS） | 通过模态分解建立物理正向模型，基于优化逆向求解 | 利用频率依赖的相位关系，避免信号抵消 |
| **频谱均衡** | 无（结果保留物体共振频率，音色失真） | 通过模态传递函数的逆向调整，压制共振峰 | 恢复平坦频谱，实现“等化”效果 |
| **表面物理模型** | 无显式模型（假设振动信号独立或仅依赖时延） | 基于薄板/膜振动方程推导的模态叠加模型 | 将物体声学传递函数参数化为可估计的模态参数 |

**简单平均（Avg）** 的失效机制在 Figure 2(b) 中得到了清晰揭示：不同表面点对同一频率的振动存在**相位反转**——在198 Hz处红点和绿点反相振荡，直接平均会抵消该频率成分；而在411 Hz处两点同相，平均则保留该成分。这种频率依赖的相位耦合使得全局平均必然导致频谱选择性失真。

**延迟求和（DnS）** 试图通过估计全局时延来对齐信号，但如 Figure 4(c) 所示，不同模态诱导不同的点间相位延迟，单一全局时延无法补偿模态间的差异，导致高频模态丢失。

### 3. 方法谱系中的位置：物理驱动 vs. 数据驱动

本文方法在方法论谱系中占据一个独特位置——**物理驱动的无监督逆向求解**。与之形成对比的是：

- **纯信号处理方法**（Avg, DnS）：无需物体模型，但无法处理频率依赖的耦合效应。
- **有监督校准方法**（Chirp inverse filter，本文第5节提出）：通过一段参考chirp信号学习逐点逆滤波器，性能接近本文方法（Figure 7），但需要额外的校准步骤和参考信号，不具备盲恢复能力。
- **纯深度学习方法**（本文未直接对比，但可视为潜在替代路径）：需要大量配对训练数据，泛化到新物体和新声源的能力存疑。

本文方法的物理先验来自**薄板/膜振动理论**：从波动方程（Eq. 1）出发，通过模态展开（Eq. 2）将表面位移表示为模态形状与模态坐标的叠加，每个模态坐标满足二阶微分方程（Eq. 3），其频率响应对应二阶线性振荡器（Eq. 5）。关键创新在于将**散斑位移与表面梯度关联**（Eq. 7: $\mathbf{v}(\mathbf{x}_n, t) = \beta \nabla_{\mathbf{x}} u(\mathbf{x}_n, t)$），从而建立从声源到多点测量值的完整正向模型（Eq. 8）：

$$\mathbf{v}(\mathbf{x}_n, t) \approx \gamma\beta \sum_{k=1}^{K} \nabla\phi_k(\mathbf{x}_n) \left(s(t) * g_k(t)\right) + \eta(\mathbf{x}_n, t)$$

这一模型的逆向优化（Eq. 12）同时完成**反向滤波**（逆转模态传递函数 $g_k(t)$）和**空间去噪**（利用多点测量的冗余性），无需任何参考信号即可恢复接近原始声源的平坦频谱。

### 4. 适用边界与局限

基于论文明确陈述的假设和实验范围，方法的适用边界如下：

**前提条件：**
1. **线性小变形假设**：模型基于线弹性薄板/膜理论，对非线性大变形或强耦合情况不适用。
2. **宽带激励需求**：需要一段较长时间的宽带激励（如偶然拍手声或环境声）以充分激发所有模态，单频或窄带声源可能导致模态检测不全。
3. **空间采样约束**：受限于散斑网格的空间采样密度和振动幅度，高频模态（对应短波长振型）可能因空间奈奎斯特限制而检测不全。
4. **单物体假设**：所有测点需属于同一物体，且物体表面静止（无刚体运动）。

**已知失效模式：**
- **虚假模态峰**：当前基于频谱标准差（Eq. 13）的模态频率检测对虚假峰敏感，随机添加20%虚假频率会引入明显伪影和非自然共振（Figure 6(c)）。
- **高频重建退化**：高频模态振动幅度小，信噪比低，重建的高频成分可能不完整。
- **经验模态的局限**：恢复的模态形状梯度 $\nabla\hat{\phi}_k(\mathbf{x}_n)$ 应理解为从采样点测量的**经验有效模态**，而非物体精确的解析本征函数。这意味着模态估计的质量依赖于测点覆盖范围和密度。

### 5. 开放问题

论文未解决但值得后续探索的方向包括：

1. **高频模态检测与重建**：如何突破空间采样限制，改进高频模态的检测精度？可能的路径包括引入压缩感知或物理驱动的超分辨率方法。

2. **体积物体的扩展**：当前模型针对薄壳结构（膜/板），能否扩展至立体结构（如块状物体）的非薄壳振动？这需要更复杂的弹性力学模型。

3. **实时处理**：当前优化求解需要批量处理整段信号，能否实现流式或在线声音恢复？这对实时监控应用至关重要。

4. **物理先验的增强**：是否可以利用额外的物理先验（如边界条件、材料参数）进一步提升鲁棒性？例如，已知物体为自由边界或固支边界时，模态形状的解析形式可作为更强的约束。

5. **与深度学习的融合**：物理模型提供了可解释的结构，而深度学习擅长处理非线性偏差和噪声模式。两者融合可能突破当前线性假设的局限。



## 原文 PDF

![[paperPDFs/CVPR_2026/Hearing_the_Room_Through_the_Shape_of_the_Drum_Modal_Guided_Sound_Recovery_from_Multi_Point_Surface_Vibrations.pdf]]
