---
title: "WaveBlender: Practical Sound-Source Animation in Blended Domains"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/WaveBlender_Practical_Sound_Source_Animation_in_Blended_Domains.pdf
aliases:
- WaveBlender
tags:
- SIGGRAPH_ASIA_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "引入β‑混合域离散方案：在FDTD更新中直接对两个连续键帧的离散化进行β加权混合，并使用三次平滑阶梯函数β(t)控制过渡，从而消除界面突变引起的不连续性。"
primary_logic: "将混合操作从连续方程层面移至离散方程层面，以w_β = β直接控制速度更新平滑度，配合“β‑介质”声学特性分析，既保留了原始FDTD的显式GPU友好结构，又实现了动态界面的鲁棒、低噪声声学仿真。"
claims:
- "WaveBlender的β‑混合方案在移动单极子源测试中显著减少栅格伪影，优于朴素FDTD和Aerophones方案。"
- "在粗网格（Δx=12.5mm）的“玻璃倾倒”动画中，WaveBlender消除了Wang et al. 2018反复出现的低频popping伪影。"
- "在相同条件下单机串行对比，WaveBlender比Wang et al. 2018的CPU求解器快约1000倍。"
- "辅助β场能够有效捕获糖果填充容器过程中动态共振特性的变化，无辅助场时仅显示空容器共振。"
---

# WaveBlender: Practical Sound-Source Animation in Blended Domains

> [!tip] 核心洞察
> 将混合操作从连续方程层面移至离散方程层面，以w_β = β直接控制速度更新平滑度，配合“β‑介质”声学特性分析，既保留了原始FDTD的显式GPU友好结构，又实现了动态界面的鲁棒、低噪声声学仿真。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WaveBlender：混合域中实用的声源动画 |
| 英文题名 | WaveBlender: Practical Sound-Source Animation in Blended Domains |
| 会议/期刊 | SIGGRAPH Asia 2024 |
| Links | [paper](https://research.nvidia.com/labs/prl/xue2024waveblender/waveblender.pdf) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | WaveBlender |
| Dataset | 2016 Pouring Faucet (single machine), Cup Phone (low-res) |

> [!tip] 效果简介
> - 2016 Pouring Faucet (single machine) 上，speedup 为 WaveBlender GPU (serial)，对比 Wang et al. 2018 CPU (serial)，变化 ~1000× faster。
> - Cup Phone (low-res) 上，Real-time Factor (core-only) 为 0.73× (5.82 s for 8 s audio)，对比 Wang et al. 2018 (parallel-in-time, not real-time)，变化 real-time feasible on single GPU。

## 概述

动画声源仿真在视觉计算中长期面临一个瓶颈：当发声物体的几何界面随时间移动或变形时，传统时域有限差分（FDTD）声学求解器在离散化切换瞬间会产生严重的“popping”伪影，且稀疏矩阵求解结构不利于GPU并行化。现有方案要么牺牲声学质量，要么依赖多机CPU并行而难以实时。**WaveBlender**（SIGGRAPH Asia 2024）针对这一瓶颈，提出了一种β‑混合域离散方案：直接在FDTD速度更新方程中对两个连续键帧的离散化进行β加权混合，以三次平滑阶梯函数β(t)控制过渡，从而消除界面突变引起的不连续性。该方法将混合操作从连续方程层面移至离散方程层面，既保留了原始FDTD显式、GPU友好的结构，又实现了动态界面的鲁棒、低噪声声学仿真。

核心结论包括：
- 在粗网格“玻璃倾倒”场景中，WaveBlender完全消除了Wang et al.（SIGGRAPH 2018）反复出现的低频popping伪影（Figure 2）。
- 在移动单极子源测试中，WaveBlender的波形质量显著优于朴素FDTD和Aerophones方案（Figure 5）。
- 在相同条件下单机串行对比，WaveBlender比Wang et al. 2018的CPU求解器快约1000倍（Table 1）。
- 辅助β场可有效捕获糖果填充容器过程中动态共振特性的变化，而无辅助场时仅呈现空容器共振（Figure 9）。

方法上，WaveBlender在均匀交错网格上运行，支持多种声源着色器（刚体模态、薄壳、气泡水声、点源加速度噪声等），采用单向源耦合和阶梯近似边界处理，以精度换取统一的显式GPU并行结构。其流水线涵盖栅格化、β‑混合FDTD求解、声源着色、逐批次开销处理与CUDA并行化等模块。主要局限包括仅支持单向耦合、边界为阶梯近似、栅格化等部分仍在CPU执行，以及尚未包含壁面损耗与衍射等复杂边界效应。

## 背景与动机

计算机图形学中的声学仿真长期面临一个核心矛盾：高保真度的波动求解器需要精细的几何离散化，而动画场景中的物体却在持续移动和变形。当声源界面在离散网格上发生突变时——例如一个振动的薄壳从一个网格单元跳变到相邻单元——声场求解器会引入严重的不连续性，在可听频谱中表现为刺耳的“popping”伪影（Figure 2）。这一问题在粗网格、长时间仿真中尤为突出，严重制约了动画声音合成的实用化。

### 现有FDTD方案的瓶颈

时域有限差分法（FDTD）因其显式结构和天然的GPU并行友好特性，成为动画声学仿真的主流选择。标准FDTD在交错MAC网格上更新压力和粒子速度：

$$
p^{n+1} = p^n - \rho_0 c_0^2 (\tilde{\nabla} \cdot \mathbf{v}^{n+1/2}) \Delta t, \quad \mathbf{v}^{n+1/2} = \mathbf{v}^{n-1/2} - \frac{1}{\rho_0} (\tilde{\nabla} p^n) \Delta t
$$

并在固‑气边界面上施加Neumann边界条件 $\mathbf{v} \cdot \hat{\mathbf{n}} = v_b$ 来驱动声波。然而，当动画键帧切换时，栅格化后的固体/空气单元标记瞬间改变，导致声场状态与新的边界配置之间失去连续性。**Wang et al. 2018**（SIGGRAPH 2018）的并行时间CPU求解器代表了此前的最先进水平，但其在每个键帧处直接切换栅格化状态的做法，在粗网格下会产生反复出现的低频popping伪影（Figure 2），且稀疏矩阵求解的串行特性使其难以充分利用GPU的大规模并行能力。

### 混合方案的前期探索与不足

**Allen and Raghuvanshi 2015**（SIGGRAPH 2015）在时变完美匹配层（PML）的工作中提出了混合几何体的思路，其速度更新采用半隐式方案：

$$
\mathbf{v}^{n+1/2} = \frac{(1-\beta)\mathbf{v}^{n-1/2} - (1-\beta)^2 (\tilde{\nabla} p^n / \rho_0) \Delta t}{(1-\beta) + \beta \Delta t} + w_\beta \mathbf{v}_b^{n+1/2}, \quad w_\beta = \frac{\beta \Delta t}{(1-\beta) + \beta \Delta t}
$$

这一“Aerophones方案”在连续方程层面进行混合，但其权重函数 $w_\beta$ 在混合窗口末端急剧变化（Figure 4），导致速度更新不平滑。更重要的是，该方案最初为PML吸收边界设计，在处理连续变形界面和Neumann边界条件时表现不佳——这正是动画声源（如振动薄壳、气泡水声）的核心需求。

### 核心动机：从连续混合到离散混合

WaveBlender的动机源于一个关键洞察：**将混合操作从连续方程层面下沉到离散方程层面**。与其在偏微分方程中引入复杂的半隐式混合项，不如直接在FDTD的离散更新方程中以混合参数 $\beta$ 为权重，对动量项和边界条件进行显式线性插值。这一设计转变带来了三重优势：

1. **平滑性**：$\beta(t)$ 采用三次平滑阶梯函数（$3t^2 - 2t^3$），直接控制速度更新的过渡平滑度，消除了末端权重突变的问题（Figure 4）。
2. **GPU友好**：保留了原始FDTD的完全显式结构，无需求解稀疏线性系统，天然适配GPU的大规模并行计算。
3. **鲁棒性**：通过在两个连续键帧的离散化之间连续改变 $\beta$ 场，将界面突变转化为平滑过渡，从根本上消除了popping伪影的产生机制。

Figure 1 以“糖果在手中摇动”的场景直观展示了这一混合域概念：给定两个60Hz动画帧的栅格化结果（“Begin”和“End”），WaveBlender在两者之间连续混合离散化状态，同时解析糖果碰撞产生的加速度噪声在变化的手部空腔中的散射和共振——这是传统逐帧切换方案无法实现的。

## 核心创新

WaveBlender 的核心创新在于将动态界面的离散化过渡从连续方程层面**下沉到离散方程层面**，从而在不破坏 FDTD 显式结构的前提下，消除了界面突变引起的声场不连续性。这一设计选择直接回应了现有方法的核心瓶颈，并形成了三个紧密耦合的关键创新点。

### 瓶颈洞察：界面离散化突变是“popping”伪影的根源

在动画声学仿真中，声源物体（如振动薄壳、移动刚体）的几何形状随动画帧变化。现有 FDTD 求解器（如 **Wang et al. 2018** 的 wavesolver，SIGGRAPH 2018）在每个动画键帧瞬间切换栅格化状态——即某些网格单元从“空气”突变为“固体”，或反之。这种离散化的不连续性在声场中引入了强烈的“popping”伪影，尤其在粗网格下表现为低频爆音（Figure 2）。此外，Wang et al. 2018 的求解器基于 CPU 稀疏矩阵运算，难以充分利用 GPU 的并行能力，导致仿真速度极慢。

### 创新一：离散层面的 β‑混合方案

WaveBlender 的核心操作是将“混合”从连续 PDE 的系数插值改为**对两个连续键帧的离散 FDTD 更新方程进行加权混合**。具体而言，标准 FDTD 的速度更新方程为：

$$\mathbf{v}^{n+1/2} = \mathbf{v}^{n-1/2} - \frac{\tilde{\nabla} p^n}{\rho_0} \Delta t$$

WaveBlender 将其修改为：

$$\mathbf{v}^{n+1/2} = (1-\beta) \left( \mathbf{v}^{n-1/2} - \frac{\tilde{\nabla} p^n}{\rho_0} \Delta t \right) + \beta \mathbf{v}_b^{n+1/2}$$

其中 $\beta \in [0,1]$ 是混合参数，$\mathbf{v}_b$ 是边界条件指定的法向速度。这一公式可以重排为：

$$\mathbf{v}^{n+1/2} = \mathbf{v}^{n-1/2} + \beta (\mathbf{v}_b^{n+1/2} - \mathbf{v}^{n-1/2}) - (1-\beta) \frac{\tilde{\nabla} p^n}{\rho_0} \Delta t$$

该形式清晰地展示了混合机制：$\beta$ 直接控制边界条件修正注入动量更新的程度。当 $\beta=0$ 时，退化为自由场 FDTD；当 $\beta=1$ 时，速度完全由边界条件驱动。在两个键帧之间，$\beta$ 从 0 连续变化到 1，使得一个键帧的栅格化状态平滑过渡到下一个键帧的栅格化状态。

### 创新二：三次平滑阶梯函数 $\beta(t)$ 消除末端突变

混合权重函数的选择至关重要。先前 **Allen and Raghuvanshi 2015**（SIGGRAPH 2015）的时变 PML 方案（Aerophones 方案）采用半隐式混合，其有效权重为：

$$w_\beta = \frac{\beta \Delta t}{(1-\beta) + \beta \Delta t}$$

该权重在混合窗口末端急剧变化（Figure 4），导致声场仍存在可察觉的伪影。WaveBlender 将权重直接设为 $w_\beta = \beta$，并采用**三次平滑阶梯函数** $3t^2 - 2t^3$ 及其镜像来定义 $\beta(t)$ 的时变曲线。这使得整个混合窗口内的速度更新保持平滑，从根本上消除了界面过渡带来的不连续性。

### 创新三：“β‑介质”声学特性保证物理一致性

将混合操作移至离散层面后，WaveBlender 分析了混合域对应的等效连续介质声学参数。从重排后的速度更新方程可导出混合域内的有效动量方程：

$$\frac{\partial \mathbf{v}}{\partial t} = -\frac{(1-\beta)}{\rho_0} \nabla p$$

由此得到混合域的有效密度、声速和阻抗分别为：

$$\rho_\beta = \frac{\rho_0}{1-\beta}, \quad c_\beta^2 = (1-\beta) c_0^2, \quad z_\beta = \frac{\rho_0 c_0}{\sqrt{1-\beta}}$$

当 $\beta \to 1$ 时，阻抗 $z_\beta \to \infty$，保证了对声波的完美反射，与固体边界条件一致。这一“β‑介质”解释确保了混合方案在物理上的自洽性，同时保留了原始 FDTD 的显式、GPU 友好结构。

### 辅助创新：模糊面边界速度指定与运行时空腔检测

除核心混合方案外，WaveBlender 还引入了两项增强鲁棒性的机制：

1. **模糊面边界速度指定**：当单元面不位于当前固‑气边界时，设置 $\mathbf{v}_b = \mathbf{v}^{n-1/2}$（即保持上一时刻的速度），而非强制指定零或其他值。这避免了混合域中模糊面（Figure 6 中的点状面）引入的阻抗突变。
2. **运行时空腔检测**：通过 flood fill 算法检测与听者位置不连通的空腔区域，将其视为固体并在空腔重新打开时排除新鲜单元压力外推，从而防止空腔开闭瞬间的伪影。

这些创新共同构成了 WaveBlender 的核心贡献：**在保持显式 FDTD 的 GPU 并行优势的同时，通过离散层面的 β‑混合方案实现了动态界面的鲁棒、低噪声声学仿真**，在粗网格下消除了 Wang et al. 2018 反复出现的低频 popping 伪影（Figure 2），并在相同条件下实现了约 1000 倍的单机串行加速（Table 1）。

## 整体框架

![[assets/figures/papers/paper_list_l20_https_research_nvidia_com_labs_prl_xue2024waveblender_waveblender_pdf/figures/004_Figure_4.jpg]]
*Figure 4: Velocity update weight ???? plotted against normalized blending time ?? shows that our method smoothly blends in the boundary conditions, whereas the original “Aerophones scheme” (FDTD step rate at 128 kHz, blending over 10 ms windows) suffers from rapid changes near the end*

WaveBlender 提出了一套面向动态动画声源的实用声学仿真管线，其核心设计围绕三个原则展开：**离散域混合**消除界面突变伪影、**均匀交错网格**保证 GPU 友好性、**单向源耦合**简化声源集成。整个管线可分解为六个功能模块，按执行顺序构成从前处理到音频输出的完整流程。

### 管线总览

给定一段包含移动/变形物体的动画序列，WaveBlender 首先将动画按固定时间窗口切分为若干批次（batch），每批次覆盖时间区间 $[t_1, t_2)$。对每个批次，管线依次执行以下步骤：

1. **栅格化模块**：使用保守的三角形‑盒子重叠测试，将批次首尾两个关键帧的声源物体分别栅格化到均匀交错 MAC 网格上，标记空气单元、固体单元以及固‑气边界面的位置。
2. **混合域 FDTD 求解器**：在整个计算域上应用 β‑混合的 FDTD 更新方程（式 8a, 8b），以三次平滑阶梯函数 $\beta(t)$ 为权重，在两个栅格化状态之间连续过渡，计算压力场和速度场的时空演化。
3. **声源着色器**：根据声源类型（刚体模态、薄壳振动、气泡水声、预录音频等）计算边界法向速度 $v_b$，单向注入 FDTD 求解器的边界条件。
4. **点源模块**：对微小刚体的加速度噪声（如颗粒碰撞的咔嗒声），通过等效波场强制力直接修改动量方程，绕过边界速度指定。
5. **逐批次开销处理**：处理批次切换时的状态初始化，包括新鲜单元压力外推、着色器速度重新对齐、运行时空腔检测（flood fill）以及 PML 吸收边界更新。
6. **GPU 并行化**：基于 CUDA 实现均匀网格上的显式 FDTD 时间步进，利用合并内存访问和线程束级 PML 计算，最大化吞吐量。

### 模块间数据流

管线的数据依赖关系清晰且单向。栅格化模块的输出是每个批次首尾关键帧的离散化状态（固体/空气标记与边界面列表），这些状态作为混合域 FDTD 求解器的几何输入。声源着色器和点源模块则独立于栅格化运行：着色器根据物体表面运动学数据（模态振幅、顶点加速度、气泡体积变化率等）计算边界速度 $v_b$，点源模块根据刚体加速度计算等效体力 $\mathbf{F}$。两者均单向耦合到 FDTD 求解器的速度更新中，求解器不向声源反馈声场信息。

批次切换时，逐批次开销模块负责桥接相邻批次的状态不连续性：新鲜单元（本批次出现但上批次不存在的空气单元）的压力通过局部 Neumann 边界条件外推（式 $p_f - p_i = -\rho_0 \mathbf{a}_n \cdot (\mathbf{x}_f - \mathbf{x}_i)$）；着色器边界速度与当前全局速度场重新对齐（式 $\mathbf{v}_b(\mathbf{x}, t) \leftarrow [\mathbf{v}_b(\mathbf{x}, t) - \mathbf{v}_b(\mathbf{x}, t_1)] + \mathbf{v}(\mathbf{x}, t_1)$）；运行时空腔检测通过 flood fill 识别与听者位置不连通的网格区域，将其视为固体并在重新开放时跳过新鲜单元外推，从而避免空腔瞬时开闭引起的伪影。

### 与基线方法的结构性差异

相较于 **Wang et al. (SIGGRAPH 2018)** 的 CPU 求解器，WaveBlender 在三个关键环节上做出了结构性改变：

- **界面处理**：Wang et al. 在每个动画关键帧瞬间切换栅格化状态，导致声场不连续和低频“popping”伪影；WaveBlender 通过 β‑混合在两个关键帧之间连续过渡离散化状态，从根本上消除了界面突变。
- **混合方案**：**Allen and Raghuvanshi (SIGGRAPH 2015)** 的时间变化 PML 方案在半隐式框架下混合，其速度更新权重 $w_\beta = \beta\Delta t/((1-\beta)+\beta\Delta t)$ 在混合窗口末端急剧变化，且对连续变形界面和 Neumann 边界条件表现不佳；WaveBlender 将混合操作从连续方程层面移至离散方程层面，直接设置 $w_\beta = \beta$，配合三次平滑阶梯函数，使速度更新在整个混合窗口内平滑过渡。
- **并行化策略**：Wang et al. 依赖时间并行在多台机器上分布式求解，单机串行性能有限；WaveBlender 的均匀网格显式 FDTD 天然适合 GPU 并行，在相同条件下单机串行对比可获得约 1000 倍加速（Table 1, “2016 Pouring Faucet”）。

### 关键设计取舍

WaveBlender 的实用性建立在明确的取舍之上：采用阶梯近似边界和一阶精度换取均匀网格的简单性和完全显式时间步进；仅支持单向源耦合，放弃薄壳振动对声场的反馈，但大幅简化了声源集成和多物理场耦合的复杂度；栅格化和部分几何处理保留在 CPU 上执行，在快速界面运动时可能成为瓶颈（Figure 7），但避免了复杂的 GPU 几何算法开发。这些取舍使得 WaveBlender 在保持鲁棒性和低噪声输出的同时，首次将动态场景声学仿真推进到接近实时的性能水平。

## 核心模块与公式推导

### 1. 问题瓶颈与核心洞察

动画声源的FDTD仿真面临一个根本性瓶颈：当物体移动或变形时，传统的逐帧栅格化方案会在离散网格上产生界面突变，导致声场不连续，表现为严重的“popping”伪影。**Allen and Raghuvanshi**（SIGGRAPH 2015）提出的时变PML方案尝试通过混合处理几何变化，但其原始连续方程层面的混合公式在持续变形的界面和Neumann边界条件下表现不佳——其速度更新权重 $w_\beta = \frac{\beta \Delta t}{(1-\beta) + \beta \Delta t}$ 在混合末端急剧变化，引入新的不连续性。

WaveBlender的核心洞察是**将混合操作从连续方程层面移至离散方程层面**。通过直接在FDTD更新方程中以 $\beta$ 为权重进行线性插值，使得 $\beta(t)$ 的平滑性直接控制速度更新的平滑度，从而在保留原始FDTD显式、GPU友好结构的同时，实现动态界面的鲁棒、低噪声声学仿真。

### 2. 混合域FDTD求解器

#### 2.1 标准FDTD背景

在均匀交错MAC网格上，声学波动方程的标准FDTD离散化为：

$$p^{n+1} = p^n - \rho_0 c_0^2 (\tilde{\nabla} \cdot \mathbf{v}^{n+1/2}) \Delta t \tag{4a}$$

$$\mathbf{v}^{n+1/2} = \mathbf{v}^{n-1/2} - \frac{1}{\rho_0} (\tilde{\nabla} p^n) \Delta t \tag{4b}$$

其中压力 $p$ 定义在单元中心，粒子速度 $\mathbf{v}$ 定义在单元面上。固-气边界上施加Neumann边界条件，通过指定法向边界速度 $\mathbf{v}_b$ 来驱动声波。

#### 2.2 WaveBlender β-混合更新方程

WaveBlender在离散层面直接混合动量项与边界条件项，核心更新方程为：

$$p^{n+1} = p^n - \rho_0 c_0^2 (\tilde{\nabla} \cdot \mathbf{v}^{n+1/2}) \Delta t \tag{8a}$$

$$\mathbf{v}^{n+1/2} = (1-\beta) \left(\mathbf{v}^{n-1/2} - \frac{\tilde{\nabla} p^n}{\rho_0} \Delta t\right) + \beta \mathbf{v}_b^{n+1/2} \tag{8b}$$

其中 $\beta \in [0,1]$ 为混合参数：$\beta=0$ 时恢复自由场FDTD更新；$\beta=1$ 时速度完全由边界条件 $\mathbf{v}_b$ 决定。压力更新（8a）保持与标准FDTD一致，无需修改。

为理解其工作机制，可将速度更新重排为：

$$\mathbf{v}^{n+1/2} = \mathbf{v}^{n-1/2} + \beta (\mathbf{v}_b^{n+1/2} - \mathbf{v}^{n-1/2}) - (1-\beta) \frac{\tilde{\nabla} p^n}{\rho_0} \Delta t \tag{9}$$

该形式揭示了β-混合的本质：将边界条件修正项 $\beta(\mathbf{v}_b - \mathbf{v}^{n-1/2})$ 注入动量更新，同时以 $(1-\beta)$ 因子缩放压力梯度项。

#### 2.3 混合权重函数设计

与**Aerophones方案**（Allen and Raghuvanshi, SIGGRAPH 2015）不同，WaveBlender直接设置 $w_\beta = \beta$，因此 $\beta(t)$ 的选择直接决定速度更新的平滑性。WaveBlender采用**三次平滑阶梯函数**：

$$\beta(t) = 3t^2 - 2t^3$$

及其镜像 $1 - \beta(t)$，在两个连续键帧之间平滑过渡（见Figure 4）。这种设计避免了Aerophones方案在混合末端权重急剧变化的问题。

#### 2.4 β-介质的声学特性

混合域可被解释为一种“β-介质”，其等效声学参数为：

$$\frac{\partial \mathbf{v}}{\partial t} = -\frac{(1-\beta)}{\rho_0} \nabla p$$

由此导出有效密度 $\rho_\beta = \frac{\rho_0}{1-\beta}$、有效声速平方 $c_\beta^2 = (1-\beta)c_0^2$ 和有效阻抗 $z_\beta = \frac{\rho_0 c_0}{\sqrt{1-\beta}}$。当 $\beta \to 1$ 时，阻抗趋于无穷，保证完美反射，与固壁边界条件一致。

#### 2.5 模糊面边界速度处理

在混合域中，某些单元面可能不位于当前键帧的固-气边界上，此时 $\mathbf{v}_b$ 的选择存在歧义（见Figure 6）。WaveBlender的处理策略是：对于这些模糊面，设置 $\mathbf{v}_b = \mathbf{v}^{n-1/2}$，以保持局部阻抗一致并避免突变。这一处理确保了混合域内声学特性的连续过渡。

### 3. 声源着色器

WaveBlender采用单向源耦合架构，通过多种“声源着色器”计算边界速度 $\mathbf{v}_b$，与FDTD求解器解耦运行。

#### 3.1 刚体模态声源

对于振动刚体，预计算模态分析得到模态矩阵 $\mathbf{U}$，将其投影到边界面上形成“模态-边界”传递矩阵，并在键帧之间线性插值。边界速度由模态振幅的加权和给出。

#### 3.2 薄壳声源

使用预计算的顶点加速度：对每个边界面，定位其到物体表面网格的最近点，取该三角形顶点加速度的平均值，通过梯形法则数值积分得到边界速度。

#### 3.3 气泡水声源

将气泡视为点源，边界速度由气泡体积加速度 $\dot{v}_{\mathrm{bub}}(t)$ 的空间分布因子决定：

$$\mathbf{v}_b(\mathbf{x}, t) = \frac{(\mathbf{x} - \mathbf{x}_{\mathrm{bub}}) \cdot \hat{\mathbf{n}}}{4\pi \|\mathbf{x} - \mathbf{x}_{\mathrm{bub}}\|^3} \dot{v}_{\mathrm{bub}}(t) = A_{\mathrm{bub}}(\mathbf{x}) \dot{v}_{\mathrm{bub}}(t)$$

其中 $A_{\mathrm{bub}}(\mathbf{x})$ 在边界面上预计算。

### 4. 点源模块：加速度噪声

对于远小于网格尺寸的微小刚体（如颗粒、碎片），WaveBlender通过等效波场强制力建模其加速度噪声，而非直接在边界上指定速度。动量方程增广为：

$$\frac{\partial \mathbf{v}}{\partial t} = -\frac{1}{\rho_0} \nabla p + \frac{1}{\rho_0} \mathbf{F}$$

对于半径为 $r$、体积为 $V_r$ 的小球，等效点力为：

$$\mathbf{f}(t) = 2\pi \rho_0 r^3 \mathbf{a}(t) = \frac{3}{2} \rho_0 V_r \mathbf{a}(t)$$

该力被分布到邻近网格的速度更新中。对于非球形小物体，以物体实际体积替代 $V_r$ 作为近似。

### 5. 逐批次开销处理

WaveBlender将仿真划分为固定长度的批次，每个批次内执行以下关键处理：

- **新鲜单元压力外推**：当空腔打开时，新暴露的空气单元压力通过相邻空气单元和法向加速度线性外推：
  $$p_f - p_i = -\rho_0 \mathbf{a}_n \cdot (\mathbf{x}_f - \mathbf{x}_i)$$

- **着色器速度重新对齐**：在批次起点，将着色器边界速度与当前全局速度场对齐：
  $$\mathbf{v}_b(\mathbf{x}, t) \leftarrow [\mathbf{v}_b(\mathbf{x}, t) - \mathbf{v}_b(\mathbf{x}, t_1)] + \mathbf{v}(\mathbf{x}, t_1)$$

- **运行时空腔检测**：通过flood fill检测与听音位置不连通的网格区域，将其视为固体，并在重新打开时排除在新鲜单元外推之外，避免空腔开闭瞬间的伪影。

- **PML吸收边界**：采用**Liu and Tao 1997**的分裂场PML公式，所有示例使用8个单元宽度的PML层。GPU实现中仅对穿透PML的线程束计算分裂场，以优化性能。

## 实验与分析

### 主实验结果

**整体性能对比。** WaveBlender在统一网格上实现了GPU加速的FDTD声学求解，其核心优势在于将混合操作从连续方程层面移至离散方程层面，从而在保留显式GPU友好结构的同时，显著提升了动态界面声学仿真的鲁棒性和计算效率。表1汇总了WaveBlender与**Wang et al.**（SIGGRAPH 2018）在多个示例上的运行时间对比。在“2016 Pouring Faucet”示例中，两者使用相同的单元尺寸、时间步长率和相似的区域尺寸，且均在单台机器上串行运行——WaveBlender的GPU实现比Wang et al.的CPU求解器快约**1000倍**。在“Cup Phone（低分辨率）”示例中，WaveBlender的核心运行时仅为5.82秒（对应8秒音频），实时因子达到**0.73×**，意味着在单GPU上已接近实时性能。相比之下，Wang et al.的方法依赖时间并行策略在多台机器上分发批次，无法在单机上实现实时。

**伪影消除的定性验证。** 图2展示了在粗网格（Δx = 12.5 mm）条件下“玻璃倾倒”动画的声谱图对比：Wang et al.的结果在低频段出现反复的“popping”伪影（图中高亮标注），而WaveBlender的β‑混合方案即使在几何欠分辨的情况下也能有效消除这些不连续性。这一结果直接验证了核心因果机制——通过β(t)的三次平滑阶梯函数控制离散化过渡，可以从根本上抑制界面突变引起的声场不连续。


![[assets/figures/papers/paper_list_l20_https_research_nvidia_com_labs_prl_xue2024waveblender_waveblender_pdf/figures/002_Figure_2.jpg]]
*Figure 2: Avoiding Popping Artifacts: A procedural “Glass Pour” animation is simulated using coarse cells (Δ?? = 12.5 mm) with both the [Wang et al. 2018] wavesolver and WaveBlender. While the [Wang et al. 2018] result suffers from repeated “popping” artifacts visible in the spectrogram’s low frequencies (here, a few instances are highlighted), WaveBlender’s ??-blending scheme helps avoid discontinuities even when geometry is under-resolved*

**声源着色器性能分解。** 图7给出了不同声源着色器的计算时间分解。当混合速率较低时（如“2016 Pouring Faucet”和“Cup Phone”），GPU端的FDTD时间步进是主要瓶颈；而当界面运动较快时（如“Spolling Bowl”、“Cymbal”和“Talk Fan”），CPU端的栅格化、逐批次开销以及着色器评估和内存管理的成本显著增加。逐批次开销主要由新鲜单元速度的CPU端QR求解主导。


![[assets/figures/papers/paper_list_l20_https_research_nvidia_com_labs_prl_xue2024waveblender_waveblender_pdf/figures/010_Figure_7.jpg]]
*Figure 7: Timing Breakdowns: Different acoustic shaders feature unique performance considerations. Here, “Overhead” refers to per-batch overhead (§6.2) and is largely dominated by fresh cell velocity QR solves on CPU, while “Misc.” refers to miscellaneous example-specific data I/O and pre-processing costs excluded from the “core” WaveBlender timings. In examples where the blend rate is low (e.g., “2016 Pouring Faucet” and “Cup Phone”), GPU-based FDTD timestepping is the bottleneck. For other examples, rapid interface movements (such as in “Spolling Bowl”, “Cymbal”, and “Talk Fan”) necessitate increased CPU-based rasterization and overhead costs, as well as more frequent shader evaluation and memory m...*

### 消融研究

**β‑混合方案的核心作用。** 图5的移动单极子源测试提供了对β‑混合方案的直接消融证据。在该测试中，一个2单元宽的小立方体以1 kHz脉动并以1 m/s的速度平移，每0.01秒栅格化一次。朴素FDTD在边界不连续切换时产生严重的栅格伪影；直接应用**Allen和Raghuvanshi**（SIGGRAPH 2015）的原始“Aerophones方案”（式7）同样产生伪影，部分原因在于该方法并非为支持移动声源而设计。WaveBlender的β‑混合方案显著减轻了这些伪影，这得益于其速度更新权重$w_\beta = \beta$的设计（式8b），使得$\beta(t)$直接控制速度更新的平滑度，避免了Aerophones方案中权重在末端急剧变化的问题（见图4）。

**辅助β‑场的动态共振捕获。** 图9的“糖果填充容器”场景展示了辅助β‑场的消融效果。264颗硬糖落入管状混凝土容器，产生366832个接触脉冲，被近似为点状加速度噪声源。当使用辅助β‑场模拟堆积糖果对空腔形状的改变时，声谱图呈现出随填充过程动态变化的容器共振特性；而无辅助β‑场时，声谱图仅显示空容器的固定共振模式。这一对比表明，辅助β‑场机制能够在不增加网格复杂度的情况下有效捕获时变几何对声学响应的影响。

**运行时空腔检测的鲁棒性提升。** 逐批次处理中的flood fill空腔检测（第6.2.3节）防止了空腔瞬间开闭引起的伪影。该机制将不与听音位置连通的网格区域视为固体，并在其重新打开时排除在新鲜单元压力外推之外，代之以零初始条件。结合β‑混合方案，这一设计使得WaveBlender在长时间仿真中比先前方法具有更强的鲁棒性和更少的popping伪影。

### 公平性说明

与Wang et al.（SIGGRAPH 2018）的所有对比均使用相同的单元尺寸、时间步长率和相似的区域尺寸（表1）。“2016 Pouring Faucet”的1000倍加速比是在单台机器上串行运行两个求解器获得的。WaveBlender采用与Wang et al.一致的单向源耦合假设，不涉及双向耦合，因此性能对比是公平的。需注意的是，Wang et al.的原始时间并行方案可将批次分发到多台机器（表1中括号内标注机器数量），而WaveBlender的串行单机实现已能在多个示例上接近或达到实时性能。


![[assets/figures/papers/paper_list_l20_https_research_nvidia_com_labs_prl_xue2024waveblender_waveblender_pdf/figures/008_Table_1.jpg]]
*Table 1: Example Statistics: Using identical cell sizes, step rates, and similar dimensions as [Wang et al. 2018], we compare our WaveBlender GPU timings with their original parallel-in-time CPU timings. The parallel-in-time method splits a simulation temporally into batches and distributes the batches across multiple machines, each running a CPU wavesolver instance; the number of machines is shown in parentheses (fourth-to-last column). In contrast, our WaveBlender implementation runs serially on a single machine. We show the full runtime, including example-specific data I/O and pre-processing costs (e.g., loading vertex accelerations from disk for thin shells and computing coupled-bubble velocitie...*

### 失败模式与局限性

尽管WaveBlender在动态声源仿真中表现出色，仍存在以下已知局限：

1. **单向耦合限制**：仅支持源对声场的单向耦合，无法模拟薄壳振动等对声场的反馈作用，这限制了其在复杂流固耦合场景中的应用。
2. **阶梯近似与一阶精度**：边界处理采用阶梯近似和一阶精度，对细薄结构的几何分辨率有限，可能在高频或精细几何场景中引入额外的数值误差。
3. **CPU端瓶颈**：栅格化和部分几何处理仍在CPU上执行。当界面运动较快时（如图7所示），CPU端的栅格化和逐批次开销成为性能瓶颈，尚未完全GPU化。
4. **均匀网格限制**：目前仅适用于均匀网格，无法自适应地跟踪移动的声源兴趣区域，对于大场景中局部声源的计算资源分配不够高效。
5. **简化边界效应**：未包含壁面损耗、频率相关吸收和衍射等复杂边界效应，可能影响高保真度应用中的声音真实感。
6. **点源模型精度**：点源模型假设声源物体远小于网格尺寸，对接近网格尺度的物体精度可能不足。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_research_nvidia_com_labs_prl_xue2024waveblender_waveblender_pdf/figures/011_Figure_8.jpg]]
*Figure 8: Reference images for comparisons with [Wang et al. 2018]. See the supplementary video for other examples. Fig. 9. Fill’er Up! A rigid-body simulation of 264 hard candies falling into a tube-like concrete container (3cm × 3cm × 20cm) generates 366832 contact impulses that are approximated as point-like acceleration-noise sources. Our WaveBlender acoustic wave simulation framework approximates such scenes on uniform grids but represents the changing air-domain shape using an auxiliary ?? field, which can be used to model auxiliary scene geometry (in blue) in addition to the container. WaveBlender timesteps modified finite-difference time-domain (FDTD) equations and boundary conditions to appr...*

## 方法谱系与知识库定位

### 1. 方法谱系

WaveBlender 的提出直接回应了动画声学仿真中一个长期存在的瓶颈：现有 FDTD 求解器在处理动态移动或变形界面时，由于每个动画键帧瞬间切换栅格化状态，导致声场不连续，产生严重的“popping”伪影。这一问题的根源在于离散化界面的突变破坏了声学连续性，在长时间仿真中尤为突出，且传统稀疏矩阵求解方式不利于 GPU 并行。

**与 Wang et al. 2018 的关系**。Wang et al.（SIGGRAPH 2018）的工作代表了此前动画声学仿真的先进水平，其基于 CPU 的 FDTD 求解器支持多种声源类型，但采用逐帧切换栅格化的方式，在粗网格下反复出现低频 popping 伪影（Figure 2），且受限于 CPU 串行或时间并行（parallel-in-time）架构，计算开销巨大。WaveBlender 在其基础上做出了根本性改进：将离散化切换替换为连续 β‑混合过渡，同时将求解器全面迁移至 GPU 均匀网格。在相同单元尺寸、时间步长率和相似区域尺寸的公平对比下，WaveBlender 在单机串行运行时比 Wang et al. 2018 的 CPU 求解器快约 1000 倍（Table 1），并消除了 popping 伪影。

**与 Allen and Raghuvanshi 2015 的关系**。Allen 和 Raghuvanshi（SIGGRAPH 2015）提出的时变 PML 方案是 WaveBlender 混合思想的直接灵感来源。该方案通过半隐式混合更新（公式 7）在时间上平滑几何变化，但其权重函数 $w_\beta = \beta \Delta t / ((1-\beta) + \beta \Delta t)$ 在混合末端急剧变化（Figure 4），导致在连续变形界面和 Neumann 边界条件下表现不佳。WaveBlender 的核心洞察是将混合操作从连续方程层面移至离散方程层面：直接在 FDTD 速度更新中以 $\beta$ 为权重进行线性插值（公式 8b），使 $\beta(t)$ 直接控制平滑度。这一改动保留了原始 FDTD 的显式、GPU 友好结构，同时显著提升了动态界面的鲁棒性。

**方法定位**。WaveBlender 在方法谱系中处于“均匀网格 FDTD + 显式时间步进 + 单向源耦合”这一支线。它通过 β‑混合域离散方案解决了动态界面连续性问题，但有意牺牲了部分精度以换取 GPU 并行效率：边界处理采用阶梯近似和一阶精度，不涉及自适应网格或高阶格式。在声源建模方面，WaveBlender 集成了多种“声源着色器”（刚体模态、薄壳、气泡水声、预录音频、点源加速度噪声），均通过单向耦合驱动边界速度 $v_b$，与 Wang et al. 2018 的耦合假设一致。

### 2. 适用边界

WaveBlender 的设计决策定义了其明确的适用边界：

- **适用场景**：需要快速、鲁棒地生成动态场景声学效果的动画应用，尤其是涉及刚体碰撞、颗粒堆积、流体倾倒等界面持续变化的场景。粗网格下也能保持无 popping 伪影的特性使其适合对实时性要求较高的交互式预览。
- **几何假设**：采用阶梯近似边界处理，对细薄结构（如薄壳）的几何分辨率有限。声源物体需能通过保守栅格化（三角形‑盒子重叠测试）映射到均匀网格。
- **声学假设**：仅支持单向源耦合，即声源驱动声场但声场不反作用于声源。这意味着无法模拟薄壳振动对声场的反馈等双向耦合现象。未包含壁面损耗、频率相关吸收和衍射等复杂边界效应。
- **网格假设**：仅适用于均匀网格，无法自适应跟踪移动声源兴趣区域或进行局部细化。

### 3. 局限与开放问题

**已确认的局限**：

1. **单向耦合限制**：无法模拟声场对声源的反作用，限制了在薄壳振动、流固耦合等场景中的应用。
2. **边界处理精度**：阶梯近似和一阶精度对细薄几何的分辨能力不足，在复杂几何附近可能引入额外误差。
3. **CPU 瓶颈**：栅格化和部分几何处理仍在 CPU 上执行，当界面快速运动时（如“Spolling Bowl”“Cymbal”），CPU 端栅格化和逐批次开销成为瓶颈（Figure 7），尚未完全 GPU 化。
4. **均匀网格限制**：无法自适应细化，对多尺度几何场景效率较低。
5. **声学模型简化**：未包含壁面损耗、频率相关吸收和衍射效应，限制了高保真度应用。
6. **点源模型精度**：加速度噪声点源模型假设声源物体远小于网格尺寸，当物体接近网格尺度时精度可能不足。

**开放问题**：

1. **双向耦合集成**：如何将双向耦合引入 WaveBlender 框架，以支持薄壳等交互更复杂的声源类型？
2. **边界效应扩展**：如何扩展边界处理以模拟壁面损耗、频率相关吸收和衍射现象，同时保持显式时间步进的效率？
3. **全 GPU 化**：能否将栅格化和几何预处理全部移植到 GPU，消除当前 CPU 瓶颈，使整个管线在 GPU 上端到端运行？
4. **自适应网格**：能否开发动态自适应网格技术，使模拟域随声源移动而自动调整形状和分辨率？
5. **非均匀网格支持**：如何支持非均匀或自适应细化网格，在复杂几何附近获得更高精度，同时保持 β‑混合方案的简洁性？
6. **实时交互系统**：未来能否将 WaveBlender 发展为实时的动画‑声音集成系统，用于游戏、VR 等交互式应用？

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/WaveBlender_Practical_Sound_Source_Animation_in_Blended_Domains.pdf]]
