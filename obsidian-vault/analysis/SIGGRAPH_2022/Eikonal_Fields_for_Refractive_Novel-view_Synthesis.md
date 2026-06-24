---
title: Eikonal Fields for Refractive Novel-view Synthesis
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Eikonal_Fields_for_Refractive_Novel_view_Synthesis.pdf
project_link: "https://eikonalfield.mpi-inf.mpg.de/"
code_link: null
aliases:
- EFRNVS
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入可学习的3D渐变折射率场（IoR），并根据程函方程使光线在折射区域内沿折射率空间梯度弯曲，通过伴随方法实现微分反向传播，从而将物理光学弯曲效应纳入学习过程。
primary_logic: 将场景分解为非折射背景（用NeRF建模，排除折射区域）与折射物体（在包围盒内学习IoR场并用程函方程弯曲光线），利用渐进式高斯模糊的背景多级体素网格稳定训练，首次实现了从一组2D图像学习包含折射与全内反射的3D场，用于高质量折射效应新视角合成。
claims:
- Our method optimizes for a field of 3D-varying index of refraction and traces light that bends toward spatial gradients according to eikonal light transport.
- The eikonal-only model changes light direction according to gradient of IoR without emission/absorption, enabling refractive bending.
- "A user study with 73 participants shows our method significantly closer to the reference: e.g., for Ball scene, NeRF was preferred only 0.27% of the time against ours."
- Ball scene (user study) 上 Preference rate (higher is better) = 99.73%
---

# Eikonal Fields for Refractive Novel-view Synthesis

> [!tip] 核心洞察
> 将场景分解为非折射背景（用NeRF建模，排除折射区域）与折射物体（在包围盒内学习IoR场并用程函方程弯曲光线），利用渐进式高斯模糊的背景多级体素网格稳定训练，首次实现了从一组2D图像学习包含折射与全内反射的3D场，用于高质量折射效应新视角合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 折射新视角合成的程函场 |
| 英文题名 | Eikonal Fields for Refractive Novel-view Synthesis |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://eikonalfield.mpi-inf.mpg.de/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Eikonal Fields |
| Dataset | Ball scene, Glass scene, Pen scene, WineGlass scene |

> [!tip] 效果简介
> - Ball scene (user study) 上，Preference rate (higher is better) 99.73% vs 0.27% (NeRF) (+99.46pp)。
> - Glass scene (user study) 上，Preference rate 96.17% vs 3.83% (NeRF) (+92.34pp)。
> - Pen scene (user study) 上，Preference rate 90.42% vs 9.58% (NeRF) (+80.84pp)。

## 概要

现有基于神经辐射场（NeRF）的新视角合成方法假设光线沿直线传输，仅考虑吸收-发射模型，无法处理折射和全内反射，导致对透明/折射物体合成新视角时出现模糊、重影及错误几何。本文提出**Eikonal Fields**，首次将程函（eikonal）光传输引入可学习的3D场框架：在折射物体包围盒内学习空间变化的折射率（IoR）场，并依据程函方程使光线沿折射率梯度弯曲，通过神经ODE伴随方法实现可微反向传播。背景区域则保留NeRF的直光线吸收-发射模型，并通过渐进式高斯模糊的多级体素网格稳定训练。用户研究表明，在Ball、Glass、Pen、WineGlass等折射场景上，本方法的视觉偏好率显著优于NeRF（最高达99.73% vs. 0.27%），首次实现了从2D图像学习包含折射与全内反射的3D场，用于高质量的折射效应新视角合成。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有新视角合成方法，特别是以NeRF为代表的神经辐射场，基于直光线的吸收-发射模型。该模型假设光沿直线传播，仅通过沿射线路径累积发射与吸收来合成颜色，无法表达光在透明/折射介质中的弯曲行为。因此，当场景中包含玻璃、透镜等折射物体时，NeRF会产生模糊、重影以及错误的几何重建，难以真实再现折射和全内反射等物理光学效应。本文的核心洞察在于：**将场景分解为非折射背景与折射物体两个可分离部分，在折射区域内引入一个可学习的3D渐变折射率场（IoR），并依据程函方程使光线沿折射率空间梯度方向弯曲，从而将物理光学弯曲效应纳入学习过程**。这一思路的关键在于，程函方程仅改变光线方向而不改变辐射度强度（无吸收/发射），与背景区域的吸收-发射模型在物理上形成互补。

### 方法总览与模块顺序

Eikonal Fields的完整流程分为五个串行模块，如图3所示：

1. **相机注册**：使用COLMAP估计输入图像的相机位姿。
2. **初始NeRF训练**：在整场景上训练标准NeRF的吸收-发射模型（$\bar{q}, \bar{\sigma}$），假设直光线。
3. **折射区域半自动掩膜**：用户标记少量2D点，利用NeRF深度图确定折射物体的3D包围盒Π。
4. **非折射背景精炼与网格化**：排除Π后重新训练NeRF，将得到的发射和吸收函数采样到多层渐进高斯模糊的3D网格$\{Q_i, P_i\}$上。
5. **程函训练**：在Π内学习IoR场$n_\psi$，利用neural ODE伴随方法反向传播，求解混合光线传输ODE，匹配背景网格颜色与输入图像。

最终渲染时，使用训练好的IoR场和内部辐射MLP，在512步光线采样下合成新视角。

### 关键Changed Slot 1：光线传输模型——从直光线到混合弯曲模型

标准NeRF的光线传输由两个常微分方程描述：

$$ \frac{\mathrm{d}L}{\mathrm{d}s} = -\sigma(s) L(s) + q(s) \quad \text{(Eq. 3)} $$

$$ \frac{\mathrm{d}\mathbf{p}}{\mathrm{d}s} = \mathbf{v}, \quad \frac{\mathrm{d}\mathbf{v}}{\mathrm{d}s} = 0 \quad \text{(Eq. 4)} $$

其中Eq. 3描述辐射度$L$因吸收$\sigma$和发射$q$沿路径的变化，Eq. 4表明光线方向$\mathbf{v}$恒定不变（直光线）。这一模型完全忽略了折射导致的路径弯曲。

本文提出的混合模型在折射包围盒Π内外采用不同的传输方程。在Π内部，采用**纯程函模型**（eikonal-only），仅改变光线方向而不改变辐射度强度：

$$ \frac{\mathrm{d}L}{\mathrm{d}s} = 0 \quad \text{(Eq. 5)} $$

$$ \frac{\mathrm{d}\mathbf{p}}{\mathrm{d}s} = \frac{\mathbf{v}(s)}{n}, \quad \frac{\mathrm{d}\mathbf{v}}{\mathrm{d}s} = \nabla n(s) \quad \text{(Eq. 6)} $$

这里$n$为折射率，$\nabla n(s)$为折射率空间梯度。Eq. 6源自哈密顿光学中的程函方程，表明光线方向的变化率等于折射率梯度——光线总是向高折射率区域弯曲。Eq. 5则表明在纯折射介质中，辐射度沿路径守恒（无吸收、无发射、无散射）。这一简化是方法可行的关键：它将折射弯曲与辐射度传输解耦，使优化目标集中在IoR场的恢复上。

在Π外部，仍采用标准的吸收-发射直光线模型（Eqs. 3-4）。整个系统的状态ODE在空间位置上切换两种模型：

$$ \mathbf{z}_{\psi}'(s) = \begin{cases} \text{Eqs. 5 and 6 with } n_{\psi} & \text{if } \mathbf{z}_{\psi}(s).\mathbf{p} \in \Pi \\ \text{Eqs. 3 and 4 with } q_{\theta} \text{ and } \sigma_{\phi} & \text{otherwise} \end{cases} \quad \text{(Eq. 12)} $$

其中$\mathbf{z} = (L, \mathbf{p}, \mathbf{v})$为包含辐射度、位置和方向的联合状态向量。这一混合ODE的求解和反向传播通过neural ODE的伴随方法实现，使得IoR场MLP的参数$\psi$可以通过匹配输入图像颜色的L1损失进行端到端优化：

$$ \psi^* = \arg\min_{\psi} \mathbb{E}_i[ |\mathrm{odeSolve}(s_0, s_1, \mathbf{z}, \mathbf{z}', \psi).L - z_i.L| ] \quad \text{(Eq. 13)} $$

### 关键Changed Slot 2：折射率场——从常数到可学习空间场

标准NeRF隐式假设场景折射率为常数1（真空），不存在折射效应。本文在折射包围盒Π内引入一个MLP $n_\psi(\mathbf{p})$，将空间位置$\mathbf{p}$映射为标量折射率值。该MLP的参数$\psi$是程函训练阶段的主要优化对象。

IoR场的物理约束来自两方面：
- **内部约束**：通过Eq. 6，IoR场的梯度$\nabla n_\psi$决定光线弯曲的幅度和方向。MLP必须学习一个折射率分布，使得弯曲后的光线路径在穿越Π后，能够与背景网格中存储的非折射场景颜色一致。
- **边界约束**：光线在Π边界处的进入和退出位置由ODE求解器自动确定（图4），无需显式处理折射/反射界面。这避免了传统图形学中复杂的界面求交和斯涅尔定律计算，将折射建模转化为一个连续场中的梯度驱动弯曲问题。

### 关键Changed Slot 3：背景表示——从隐式MLP到渐进高斯模糊3D网格

在标准NeRF中，背景的发射和吸收由MLP隐式表示，每次查询需网络推理。本文在非折射背景精炼阶段，将排除Π后重新训练的NeRF的发射函数$q$和吸收函数$\sigma$采样到显式3D网格上：

$$ Q_i(\mathbf{p}) = \mathbb{E}_{\mathbf{y}} \left[ \mathbb{E}_{\omega} [ q(\mathbf{y},\omega) \kappa_i(|\mathbf{p} - \mathbf{y}|) ] \right] \quad \text{(Eq. 10)} $$

$$ P_i(\mathbf{p}) = \mathbb{E}_{\mathbf{y}} [ \sigma(\mathbf{y}) \kappa_i(|\mathbf{p} - \mathbf{y}|) ] \quad \text{(Eq. 11)} $$

其中$\kappa_i$为第$i$级的高斯模糊核。这一改变的因果逻辑链如下：

1. **计算效率**：程函训练需要在每次迭代中求解ODE，该ODE在Π外部需频繁查询背景的发射和吸收值。若每次查询都调用MLP，计算开销巨大。预计算到网格上可将查询变为$O(1)$的三线性插值。
2. **训练稳定性**：直接使用MLP背景与程函场联合训练会导致梯度信号复杂耦合，训练不稳定。网格化将背景“冻结”，使程函训练仅需优化IoR场MLP。
3. **渐进式模糊的核心作用**：实验表明，直接使用高分辨率网格求解程函方程会导致训练不稳定和收敛困难。本文采用**渐进式网格策略**：从强高斯模糊（归一化频率带宽0.08周期/样本）的低频网格开始，每1000次迭代将带宽翻倍，逐步增加细节。这一策略使IoR场先从粗糙的折射效果学起，再逐步细化，是方法成功的关键消融发现。

### 训练与推理路径

**训练路径**分为两个阶段：
- **阶段一（非程函步骤）**：训练标准NeRF获得$\bar{q}, \bar{\sigma}$ → 用户辅助定义Π → 排除Π后重新训练NeRF → 将$q, \sigma$采样到渐进高斯模糊3D网格$\{Q_i, P_i\}$。网格分辨率为$128^3$，NeRF训练约150k迭代，在NVIDIA 1080Ti上耗时约12小时。
- **阶段二（程函步骤）**：在Π内初始化IoR场MLP $n_\psi$ → 从输入图像采样射线 → 使用neural ODE伴随方法求解Eq. 12的混合ODE → 通过Eq. 13的L1损失反向传播更新$\psi$。渐进式网格随训练迭代切换，从低频到高频逐步引入背景细节。

**推理路径**：给定新视角相机参数 → 发射射线 → 在512步采样下求解Eq. 12的ODE → 输出最终辐射度$L$作为像素颜色。Π内部的辐射度由内部辐射MLP $q_\theta$提供（在Π内Eq. 5保持$L$不变，但最终渲染时需考虑介质自身的微弱发射）。

### 方法边界与简化假设

本文方法基于以下关键简化假设，这些假设定义了其适用边界：
1. **折射介质无吸收/发射/散射**：Π内采用纯程函模型（Eq. 5），忽略介质的吸收、发射和散射。这适用于透明玻璃等介质，但不适用于有色或浑浊折射体。
2. **无部分反射/折射**：光线在Π边界处不分裂为反射和折射分量，仅沿弯曲路径穿越。这忽略了菲涅尔效应，无法再现部分反射。
3. **折射物体需被3D包围盒界定**：依赖用户手动指定Π，未能实现全自动的折射区域检测。
4. **背景需直接可见**：非折射背景必须在输入视图中被充分直接观测到，无法重建仅通过折射或反射可见的场景部分。

![[assets/figures/papers/paper_list_l38_https_eikonalfield_mpi_inf_mpg_de/figures/001_Figure_1.jpg]]
*Figure 1: Novel-view synthesis using neural radiance field (top) and our eikonal approach (bottom) for a real refractive scene*

![[assets/figures/papers/paper_list_l38_https_eikonalfield_mpi_inf_mpg_de/figures/002_Figure_2.jpg]]
*Figure 2: Emission-absorption (left) and eikonal light transport (right). Light is the yellow arrow, its thickness indicates strength. We show three discrete steps. In emissionabsorption, direction remains unaltered. In the eikonal formuation, direction changes according to the gradient of the IoR, ∇??. In the eikonal case, strength remains unaffected*

![[assets/figures/papers/paper_list_l38_https_eikonalfield_mpi_inf_mpg_de/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the pipeline enabling final eikonal training: We start by estimating camera poses [Schönberger and Frahm 2016]. We ask NeRF to explain the scene using emission-absorption and straight rays. In a semi-automated process, we identify a 3D box region not explained and consider this the refractive volume which we exclude from a second NeRF fit. We then grid the view-independent part of this fit to enable the final progressive training using eikonal equations and curved rays*

## 实验与关键发现

### 评估设置与基准

论文在四个真实折射场景上评估 Eikonal Fields：**Ball**（玻璃球）、**Glass**（厚玻璃块）、**Pen**（笔状玻璃棒）和 **WineGlass**（红酒杯）。所有场景均包含强折射和全内反射效应。对比方法包括：

- **NeRF**（Mildenhall et al., ECCV 2020）：标准吸收-发射模型，光线沿直线传播，无折射能力。
- **Trivial**：朴素遮罩方案——在折射包围盒内将发射和吸收设为零，但光线仍沿直线传播，无程函弯曲。

评估采用三项自动指标（PSNR、SSIM、LPIPS）和一项用户主观偏好测试。用户研究招募73名参与者，每次同时展示参考图像、Eikonal Fields 结果和一个对比方法的结果，要求选择哪个更接近参考。偏好率低于50%即表明 Eikonal Fields 显著优于对比方法（p < 0.01）。

### 主要定量结果

**Table 1** 汇总了全部定量对比。Eikonal Fields 在所有场景和指标上均大幅领先：

| 场景 | 方法 | PSNR ↑ | SSIM ↑ | LPIPS ↓ | 用户偏好率（对比方） |
|------|------|--------|--------|---------|---------------------|
| Ball | Ours | **26.720** | **0.951** | **0.057** | — |
| | NeRF | 22.465 | 0.885 | 0.089 | 0.27% |
| | Trivial | 18.828 | 0.833 | 0.108 | — |
| Glass | Ours | **26.525** | **0.922** | **0.070** | — |
| | NeRF | 24.361 | 0.896 | 0.078 | 3.83% |
| | Trivial | 20.561 | 0.843 | 0.103 | — |
| Pen | Ours | **27.803** | **0.935** | **0.066** | — |
| | NeRF | 25.298 | 0.903 | 0.078 | 9.58% |
| | Trivial | 22.127 | 0.846 | 0.108 | — |
| WineGlass | Ours | **27.789** | **0.940** | **0.072** | — |
| | NeRF | 25.673 | 0.914 | 0.081 | 24.93% |
| | Trivial | 23.642 | 0.880 | 0.107 | — |

**关键差异解读**：

- **Ball 场景**折射最强（球体聚焦效应），NeRF 完全失效，用户偏好率仅 0.27%（即 99.73% 的比较中用户选择 Eikonal Fields 更接近参考），PSNR 差距达 +4.26 dB。这直接验证了程函弯曲对强折射的必要性。
- **WineGlass 场景**相对简单（薄壁、折射路径短），NeRF 偏好率升至 24.93%，但仍远低于 50%，PSNR 差距 +2.12 dB。说明即使折射较弱，忽略光线弯曲也会导致可感知的失真。
- **Trivial 方法**在所有场景中 PSNR 最低（比 Ours 低 4–8 dB），证明仅遮罩折射区域而不建模光线弯曲不仅无益，反而因背景信息缺失而恶化结果。

### 消融实验：渐进式高斯模糊的关键作用

论文报告了一项决定性消融：**直接使用原始清晰背景网格训练程函方程会导致训练不稳定和收敛失败**。核心机制在于：折射光线在包围盒内的出射位置对 IoR 场的微小变化高度敏感，形成病态优化景观。解决方案是**渐进式多级体素网格**：

- 将掩码后的背景发射 $q$ 和吸收 $\sigma$ 采样到多个 3D 网格 $\{Q_i, P_i\}$ 上，每个网格使用不同带宽的高斯核 $\kappa_i$ 进行模糊。
- 初始阶段使用大带宽（归一化频率带宽 0.08 cycles/sample），产生极度模糊的背景，使 IoR 场先学习粗粒度的折射趋势。
- 每 1000 次迭代将带宽加倍，逐步引入高频细节，最终收敛到清晰背景。

该消融虽未以独立表格呈现，但论文明确指出“直接求解程函方程极具挑战性”，渐进式策略是训练成功的前提。这一发现揭示了将物理光学约束与神经网络优化结合时的核心困难：物理方程的高灵敏度要求精心设计的课程学习。

### 定性结果与视觉证据

**Figure 5** 提供了系统的视觉对比，包含三个维度：

1. **IoR 横截面恢复**（左块）：沿测试视图中白点标记的扫描线，展示 Eikonal Fields 恢复的折射率空间分布。Ball 场景呈现中心高、边缘低的球对称模式，符合实心玻璃球的物理预期。
2. **新视角细节对比**（中块）：不同视角下三种方法的局部放大。NeRF 产生模糊和重影（光线错误地直线穿过折射体），Trivial 出现空洞和错误颜色（背景被遮罩但光线未弯曲），Eikonal Fields 清晰再现折射变形和焦散状亮度变化。
3. **伪极线轨迹**（右块）：沿连续相机轨迹的合成视图序列。Eikonal Fields 的折射变形随视角平滑变化，NeRF 则出现跳变和不一致。

**Figure 6** 进一步将恢复的 IoR 横截面与真实值（通过独立测量获得）对比，橙色曲线（Ours）与蓝色曲线（Ground Truth）在趋势和数值上高度吻合，验证了程函场学习的物理准确性。

### 失败模式与适用边界

论文明确列出四项关键限制，构成方法的适用边界：

1. **手动包围盒依赖**：折射物体必须由用户通过 2D 点选和 NeRF 深度图半自动确定 3D 包围盒 $\Pi$。这限制了全自动场景重建的应用，且对复杂形状的折射体（如分形或凹形）包围盒近似会引入系统误差。

2. **无部分反射/折射**：模型假设折射介质内无吸收、无散射、无部分反射（仅全内反射）。在连续变化折射率介质中，实际物理过程包括菲涅尔反射和透射的能量分配，当前模型将这些效应全部归入背景或忽略，可能导致能量不守恒的伪影。

3. **背景直接可见性要求**：非折射背景必须在至少部分输入视图中被直接观测到（不被折射体遮挡）。仅通过折射或全内反射可见的场景部分无法重建，因为背景 NeRF 训练阶段需要这些区域的直接视线观测。

4. **静态场景假设**：当前方法仅处理固定照明下的静态场景，未涉及动态物体、时变照明或可重光照场景。

### 训练成本与计算开销

论文报告了实际训练成本：非程函 NeRF 阶段需约 150k 迭代、在 NVIDIA 1080Ti 上约 12 小时；程函训练阶段涉及 neural ODE 求解与伴随反向传播，计算开销更高但未给出精确时间。背景网格分辨率为 $128^3$，最终渲染每条光线采样 512 步。这些数字表明方法目前离实时应用尚有距离，但作为首个从 2D 图像学习折射场的方法，计算成本在可接受范围内。

![[assets/figures/papers/paper_list_l38_https_eikonalfield_mpi_inf_mpg_de/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of different methods (rows) using different scenes and metrics (columns). The numbers in the User column say how often in our user study the method was considered closer to the reference than ours. As these numbers are significantly (?? \< 0.01) smaller than the chance level 50%, our method was for all scenes considered closest to the reference in the majority of the comparisons shown to the users*

![[assets/figures/papers/paper_list_l38_https_eikonalfield_mpi_inf_mpg_de/figures/006_Figure_5.jpg]]
*Figure 5: The left block shows the cross section of recovered IoR by our method for a scanline between the white dots shown in the reconstructed test view in the second block. The third block shows insets taken from novel views produced by three different methods (rows) for different view points (columns). The right block shows a pseudo-epipolar view using a continuous camera trajectory, again for all methods*

![[assets/figures/papers/paper_list_l38_https_eikonalfield_mpi_inf_mpg_de/figures/007_Figure_6.jpg]]
*Figure 6: IoR cross section of our method (orange) and ground truth (blue) for a scanline along the pixel marked with dot in each inset*

## 定位与知识库关联

**Eikonal Fields** 的核心定位在于对神经渲染中**光线传输模型**这一关键 slot 的根本性替换。现有基于神经辐射场的方法，以 **NeRF**（Mildenhall et al., ECCV 2020）为代表，假设光线沿直线传播且仅发生吸收-发射交互（$d\mathbf{v}/ds = 0$），这使得它们在面对透明/折射物体时，只能将折射导致的视差和焦散错误地“烘焙”为模糊的伪几何或错误的颜色场，无法再现真实的折射与全内反射效果。Eikonal Fields 将这一 slot 从“直光线吸收-发射”替换为“混合程函弯曲光线模型”：在折射物体包围盒 $\Pi$ 内，光线方向依据可学习的折射率场 $n_\psi$ 的空间梯度发生弯曲（$d\mathbf{v}/ds = \nabla n$），且无吸收-发射；在盒外则保留传统 NeRF 的直线传输与吸收-发射。这一改变使得物理光学的弯曲效应首次被纳入基于图像的三维场学习中。

相对已有方法的本质差异体现在三个层面。**第一，物理建模的粒度**：传统 NeRF 及其变体（如 Ref-NeRF 等）通过改进方向编码或表面反射模型来处理镜面反射，但始终未触及光线路径本身的弯曲。Eikonal Fields 直接操作程函方程（Hamilton 方程），将折射率空间梯度作为光线弯曲的驱动力，从传输机制上区别于所有仅修改辐射度表达的工作。**第二，场景分解策略**：方法将场景显式分解为非折射背景与折射物体，背景通过排除折射盒 $\Pi$ 的 NeRF 重建并烘焙到多级高斯模糊网格 $\{Q_i, P_i\}$ 上，折射物体则由独立的 IoR MLP 在 $\Pi$ 内建模。这种“背景网格化 + 前景程函场”的异构表征，与端到端的单一 NeRF 模型形成架构级差异。**第三，训练信号与稳定性**：直接优化程函 ODE 极易发散，Eikonal Fields 通过渐进式高斯模糊背景网格（带宽从 0.08 cycles/sample 起，每 1k 迭代加倍）提供由粗到精的监督，这一训练策略是使弯曲光线学习收敛的关键工程创新。

**知识库挂载点**：本工作可挂载在计算机图形学与视觉知识库的以下节点上。(1) **神经渲染与神经辐射场**：作为 NeRF 族方法在“非散射参与介质传输”方向的扩展，核心贡献是将程函光线追踪与神经场优化结合。(2) **物理光学仿真**：与经典的光线追踪（ray tracing）和程函求解器（如基于 Fermat 原理的路径优化）形成互补——传统方法依赖已知的折射率分布，而本工作从图像反演折射率场。(3) **神经 ODE 与可微物理**：方法依赖 Neural ODE 的伴随方法（adjoint method）实现穿过 ODE 求解器的反向传播，与 **Neural ODE**（Chen et al., NeurIPS 2018）在 PyTorch 实现上直接关联。(4) **3D 场景理解与重建**：半自动折射区域掩膜策略（用户标记 2D 点，利用 NeRF 深度图确定 3D 包围盒）连接了交互式重建与自动场景解析的中间地带。

**适用边界**：方法当前有明确的边界条件。它假设折射介质无散射、无部分反射/折射，仅处理全内反射和纯折射（无吸收-发射），因此不适用于半透明、浑浊或连续变化折射率介质中的部分反射场景。背景区域必须在输入视图中被充分直接观测到，无法重建仅通过折射或反射可见的场景部分。此外，方法依赖用户手动指定折射物体的 3D 包围盒，未能实现全自动的折射区域检测与联合学习，且训练分为背景 NeRF 与程函场两个分离阶段，非端到端。当前仅处理静态场景和固定照明。

**后续启发**：本工作为三个方向打开了空间。(1) **完整折射辐射传输方程的学习**：将当前简化的程函-only 模型扩展至包含吸收-发射乃至散射项的完整 RTE（Eq. 1），以处理更复杂的参与介质。(2) **端到端联合优化**：将包围盒检测、背景表征与 IoR 场学习整合到单一可微循环中，消除两阶段分离带来的次优性。(3) **对相机位姿误差的鲁棒性**：弯曲光线对位姿误差敏感，将位姿参数纳入联合优化（类似 BARF 或 NeRF-- 的思路）是提升实用性的自然延伸。同时，如何将部分反射（Fresnel 效应）纳入程函学习框架，是连接本工作与完整物理渲染的关键理论挑战。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Eikonal_Fields_for_Refractive_Novel_view_Synthesis.pdf]]