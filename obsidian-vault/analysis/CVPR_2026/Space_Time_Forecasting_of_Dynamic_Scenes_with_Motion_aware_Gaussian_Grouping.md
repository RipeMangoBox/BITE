---
title: Space-Time Forecasting of Dynamic Scenes with Motion-aware Gaussian Grouping
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Space_Time_Forecasting_of_Dynamic_Scenes_with_Motion_aware_Gaussian_Grouping.pdf
project_link: "https://slime0519.github.io/mogaf"
code_link: null
aliases:
- MGAGFM
- STFDSMAGG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 运动感知高斯分组与分组优化，通过在物体级别强制刚性与非刚性运动约束，获得物理一致的运动模式。
primary_logic: 将高斯分组为不同运动特征的物体组，并对刚性组施加共享SE(3)变换、对非刚性组施加局部运动平滑性，能显著提升长期场景外推的物理一致性和时间稳定性。
claims:
- 在iPhone和D-NeRF数据集上，MoGaF在多个观察比例下均取得更高的光度保真度。
- 移除分组优化和分组预测导致3D跟踪误差显著增加（HC配置下EPE从0.245升至0.296）。
- 运动感知高斯分组相比朴素静态分组扩展（Gaga-4D）显著提升预测性能（mPSNR 15.51 vs 15.31）。
- "iPhone 上 mPSNR = 15.58"
---

# Space-Time Forecasting of Dynamic Scenes with Motion-aware Gaussian Grouping

> [!tip] 核心洞察
> 将高斯分组为不同运动特征的物体组，并对刚性组施加共享SE(3)变换、对非刚性组施加局部运动平滑性，能显著提升长期场景外推的物理一致性和时间稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于运动感知高斯分组的动态场景时空预测 |
| 英文题名 | Space-Time Forecasting of Dynamic Scenes with Motion-aware Gaussian Grouping |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21668) · [Project](https://slime0519.github.io/mogaf) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Motion Group-aware Gaussian Forecasting (MoGaF) |
| Dataset | iPhone, D-NeRF |

> [!tip] 效果简介
> - iPhone 上，mPSNR 15.58 vs 14.99 (GSPred-SoM) (+0.59)；mLPIPS 0.4227 vs 0.4482 (GSPred-SoM) (-0.0255)。
> - D-NeRF 上，PSNR 23.37 vs 21.78 (GSPred) (+1.59)。

## 概要

动态场景的时空预测旨在从有限的观测帧中推断未来时刻的视觉内容，在自动驾驶、机器人交互与视频生成等领域具有关键价值。现有基于3D高斯泼溅（3DGS）的预测方法面临一个核心瓶颈：高斯原语独立运动，缺乏物体级别的运动一致性约束，导致长期外推时出现空间运动不连贯与轨迹漂移。

针对这一问题，本文提出**运动感知高斯分组预测**（Motion Group-aware Gaussian Forecasting, **MoGaF**）。其核心洞察在于：将场景高斯聚类为具有不同运动特征的物体组，并对刚性组施加共享SE(3)变换、对非刚性组施加局部运动平滑性，能显著提升长期场景外推的物理一致性与时间稳定性。方法围绕三个关键模块展开：（1）**运动感知高斯分组**，通过时空区域生长与关键帧配准将高斯聚类为刚性/非刚性物体组；（2）**分组约束优化**，根据刚性标注施加组级运动约束以精炼4DGS表示；（3）**分组运动预测**，为每个运动组训练轻量级Transformer编码器，结合掩码运动建模与自回归滚动预测外推未来轨迹。

实验表明，MoGaF在iPhone与D-NeRF数据集上均取得领先的光度保真度与运动跟踪精度。在iPhone数据集80%观测比下，MoGaF的mPSNR达15.58，较重新实现到SoM骨干的**GSPred-SoM**提升0.59 dB；在D-NeRF数据集60%观测比下，PSNR达23.37，较**GSPred**提升1.59 dB。消融实验进一步验证了分组优化与分组预测的关键作用：移除分组优化后，3D跟踪误差EPE从0.245升至0.296；运动感知分组相比朴素静态分组扩展（**Gaga-4D**）将mPSNR从15.31提升至15.51。方法的主要局限在于依赖预训练4DGS的重建质量，且当前框架未建模物体组间的碰撞与交互。

> **项目页面**：https://slime0519.github.io/mogaf

### 动态场景时空预测的核心挑战

从单目视频中预测动态场景的未来状态是计算机视觉与图形学中长期存在的难题。任务要求模型不仅理解场景的几何结构与外观，还要捕捉物体在时间维度上的运动规律，并在未观测的未来时间步上生成物理一致、视觉逼真的渲染结果。近年来，基于神经辐射场（NeRF）和3D高斯泼溅（3DGS）的隐式与显式表示在静态场景重建和新视角合成中取得了突破性进展，但将其直接推广到动态场景的时空外推时，面临一个根本性瓶颈：**表示单元的运动独立性导致空间运动不连贯与长期轨迹漂移**。

具体而言，主流的4D高斯泼溅（4DGS）方法——如**SoM**——将动态场景建模为大量独立的高斯原语，每个高斯在规范空间与变形空间之间通过各自的运动系数进行变换。这种“无结构”的参数化虽然提供了极高的表达能力，却缺乏对物体级别运动一致性的显式约束。当模型仅基于有限的观测帧学习运动模式时，独立优化的高斯容易产生物理上不合理的运动轨迹：属于同一刚性物体的高斯可能朝不同方向漂移，非刚性区域的形变也可能缺乏局部平滑性。随着预测时间窗的延长，这些误差会累积放大，导致渲染结果出现撕裂、模糊或几何坍塌。

### 现有方法的缺口

目前动态场景预测的方法大致可分为两类。第一类基于**神经隐式表示**，如D-NeRF、TiNeuVox等，通过条件辐射场在时间维度上插值或外推。这类方法受限于隐式表示的渲染效率，且对复杂运动的建模能力有限。第二类基于**显式高斯表示**，如**GSPred**和**ODE-GS**，通过图神经网络（GCN）或神经常微分方程（ODE）预测每个高斯的未来运动。然而，这些方法存在两个关键缺陷：

1. **运动建模粒度过细**：预测器直接操作每个独立高斯的运动参数，忽略了物体作为整体的刚性运动或局部非刚性形变的规律性。这不仅增加了预测模块的学习难度，也使得预测结果容易偏离物理真实。
2. **缺乏分组运动约束**：在4DGS重建阶段，高斯的运动系数是通过逐像素光度损失独立优化的，没有引入任何物体级别的运动一致性先验。即使预测模块能够准确外推每个高斯的运动，底层表示本身就可能包含不连贯的运动伪影。

此外，将静态3DGS的分割方法简单扩展到4D场景——如**Gaga-4D**所代表的朴素静态分组扩展——仅依赖单帧掩码或逐帧区域生长，无法有效利用时间维度上的运动线索来关联跨帧的高斯，导致分组结果碎片化、物体边界不完整（见Figure 3对比）。

### 本文动机与核心思路

本文的出发点是：**如果能在4DGS表示中显式地引入物体级别的运动分组，并在重建与预测两个阶段分别施加分组约束，就能从根本上提升动态场景时空外推的物理一致性与长期稳定性**。

基于这一洞察，MoGaF提出了三个关键设计：

- **运动感知高斯分组**：通过交替的时空区域生长与关键帧高斯注册，将场景中的高斯聚类为具有连贯运动模式的物体组，并为每组标注刚性/非刚性标签。这使得模型能够区分“整体平移旋转的刚性物体”与“局部形变的非刚性区域”，为后续约束提供结构基础。
- **分组约束优化**：在4DGS重建阶段，对刚性组施加共享SE(3)变换锚定损失，强制组内所有高斯共享同一刚体运动；对非刚性组施加局部运动平滑损失，鼓励相邻高斯的运动系数保持一致。这种“自适应约束”在保持非刚性区域表达能力的同时，消除了刚性物体的运动碎片化。
- **分组运动预测**：为每个运动组训练独立的轻量级Transformer编码器，而非使用单一全局预测器。结合掩码运动建模训练策略和自回归滚动预测，模型能够以物体为单位外推未来运动轨迹，显著降低预测复杂度并提升长期稳定性。

通过将“运动分组”作为连接重建与预测的桥梁，MoGaF在物理一致性与光度保真度之间取得了更优的平衡，为动态场景的长期时空预测提供了新的范式。

## 核心方法与创新机理

MoGaF 的核心创新在于将动态场景预测从**无结构的独立高斯运动**提升为**物体级运动感知的分组建模**。该方法在 4DGS 表示（基于 **SoM** 骨干）之上，通过三个关键环节实现了这一转变：

### 1. 运动感知高斯分组（Changed Slot：高斯表示）

传统 4DGS 方法将场景建模为独立运动的高斯原语集合，每个高斯拥有各自学习的运动系数。MoGaF 的**运动感知高斯分组**（Section 4.1）打破了这一范式，将高斯聚类为具有连贯运动模式的物体组，并对每组标注为刚性或非刚性。

分组策略采用混合方法：交替进行时空区域生长和关键帧高斯配准，结合 grounded 2D 分割先验。与朴素扩展（如将 3DGS 静态分组直接投影到动态场景，或仅基于单帧掩码的区域生长）相比，该混合方法能产生更完整、更可靠的运动感知分组（Figure 3）。每个高斯组 $G^{(k)}$ 获得一个刚性标签 $\tau^{(k)} \in \{0, 1\}$，为后续的约束优化提供结构先验。

### 2. 分组约束运动优化（Changed Slot：运动优化）

基于分组结构，MoGaF 将运动优化的粒度从**每高斯独立**提升为**分组约束**（Section 4.2）：

- **刚性组**（$\tau^{(k)} = 1$）：组内所有高斯共享一个 SE(3) 变换 $\Phi_t^{(k)} = [\mathbf{R}_{ct}^{(k)} | \mathbf{t}_{ct}^{(k)}]$，通过刚性运动锚定损失强制一致性：

$$\mathcal{L}_{\mathrm{rigid}}^{(k)} = \sum_{t} \sum_{g \in G^{(k)}} \big\| \pmb{\mu}_{t,g} - \pmb{\Phi}_t^{(k)}(g) \big\|_2^2$$

该损失衡量每个高斯的学习运动与组级刚性变换之间的偏差，迫使组内运动在物理上保持一致。

- **非刚性组**（$\tau^{(k)} = 0$）：通过局部运动平滑损失约束，鼓励规范空间中相邻高斯的运动系数 $\pmb{w}_g$ 保持一致：

$$\mathcal{L}_{\mathrm{nr}}^{(k)} = \sum_{g \in G^{(k)}} \sum_{g' \in \mathrm{NN}(g)} \| \pmb{w}_g - \pmb{w}_{g'} \|_2^2$$

总体运动约束损失根据刚性标签自适应组合二者：

$$\mathcal{L}_{\mathrm{motion}} = \sum_{k=1}^{K} \left[ \tau^{(k)} \mathcal{L}_{\mathrm{rigid}}^{(k)} + (1 - \tau^{(k)}) \mathcal{L}_{\mathrm{nr}}^{(k)} \right]$$

### 3. 分组轻量运动预测（Changed Slot：运动预测模块）

MoGaF 将运动预测从**单一全局预测器**（如 GSPred 的 GCN 或 ODE-GS 的神经 ODE）替换为**分组轻量 Transformer 编码器**（Section 4.3）。每个运动组独立训练一个浅层 Transformer，外推未来时刻的高斯运动变换。

训练中引入**掩码运动建模**策略（灵感源自 NLP 中的掩码语言建模），对输入的运动序列施加连续时间段的掩码，增强预测器对运动时序的鲁棒性。消融实验表明，移除掩码训练会导致 D-NeRF 上预测质量下降（PSNR 从 25.87 降至 24.68，Table 3b）。预测损失结合加速度正则化，惩罚预测均值的不平滑加速度：

$$\mathcal{L}_{\mathrm{acc}}^{(k)} = \frac{1}{|G^{(k)}|} \sum_{g \in G^{(k)}} \big\| \hat{\pmb{\mu}}_{T,g} - 2\pmb{\mu}_{T-1,g} + \pmb{\mu}_{T-2,g} \big\|_2^2$$

分组训练目标为：

$$\mathcal{L}_{\mathrm{group}}^{(k)} = \mathcal{L}_{\mathrm{pred}}^{(k)} + \lambda_{\mathrm{acc}} \mathcal{L}_{\mathrm{acc}}^{(k)}$$

### 创新因果链

三个 changed slot 形成因果闭环：**运动感知分组**提供物体级结构先验 → **分组约束优化**在物体级别强制刚性与非刚性运动一致性 → **分组轻量预测器**在物理一致的运动表示基础上进行外推。这一设计直接回应了核心瓶颈——独立高斯运动导致的长期预测中空间运动不连贯与轨迹漂移。消融实验证实了该因果链的有效性：移除分组优化和分组预测后，3D 跟踪误差显著增加（EPE 从 0.245 升至 0.296，Table 7a）。

MoGaF 的整体管线构建于 4DGS 表示之上，包含三个核心阶段，如图 2 所示。给定一段动态视频，方法首先从 4DGS 重建中获取规范空间的高斯原语及其运动基系数，随后依次执行：**运动感知高斯分组**、**分组约束优化**、**分组运动预测**，最终渲染出未来时刻的新视角图像。

### 输入输出与模块关系

整个框架的输入为多视角视频序列，输出为观测窗口之外未来时刻的预测图像。三个模块形成级联依赖：

1. **4DGS 骨干（SoM）** 负责将动态场景重建为规范空间高斯与运动基参数化表示，为后续阶段提供几何与运动的初始载体。
2. **运动感知高斯分组** 接收 SoM 的高斯原语，将其聚类为具有连贯运动的物体组，并为每组标注刚性/非刚性标签（详见第 4.1 节）。
3. **分组约束优化** 利用分组信息，对刚性组施加共享 SE(3) 变换锚定损失，对非刚性组施加局部运动平滑性损失，精炼 4DGS 表示的运动一致性（详见第 4.2 节）。
4. **分组运动预测** 为每个运动组训练轻量级 Transformer 编码器，结合掩码运动建模与自回归滚动预测，外推未来高斯运动轨迹，最终通过高斯泼溅渲染生成预测帧（详见第 4.3 节）。

### 关键设计动机

该管线的核心因果机制在于：独立高斯原语的运动优化缺乏物体级别的运动一致性约束，导致长期预测中出现空间运动不连贯与轨迹漂移。通过在优化与预测两个阶段均引入分组结构——刚性组共享 SE(3) 变换、非刚性组保持局部运动平滑——MoGaF 在物体级别强制物理一致的运动模式，从而显著提升长期场景外推的稳定性与光度保真度。

### 证据支撑

- **Table 1**：在 iPhone 数据集 80% 观测比例下，MoGaF 的 mPSNR 达到 15.58，相比在 SoM 骨干上重新实现的 GSPred-SoM（14.99）提升 0.59 dB；mLPIPS 从 0.4482 降至 0.4227。
- **Table 2**：在 D-NeRF 数据集 60% 观测比例下，MoGaF 的 PSNR 达到 23.37，显著优于 GSPred 的 21.78。
- **Table 7a**：移除分组优化和分组预测后，3D 跟踪误差（EPE）从 0.245 升至 0.296，验证了分组结构对运动估计质量的关键作用。
- **Table 7b**：运动感知高斯分组相比朴素静态分组扩展（Gaga-4D）将 mPSNR 从 15.31 提升至 15.51，表明分组质量直接影响预测性能。

> 注：GSPred-SoM 与 ODE-GS-SoM 是将原始 GSPred 的 GCN 预测架构和 ODE-GS 的神经 ODE 预测器重新实现到 SoM 骨干上的公平比较基线，因为原始版本未使用深度、点跟踪等数据驱动先验。

MoGaF 的整体管线建立在 4DGS 表示之上，由三个核心模块串行构成：(1) 运动感知高斯分组，(2) 分组约束优化，(3) 分组运动预测。以下逐一展开各模块的关键公式与变量含义。

### 4DGS 骨干表示

MoGaF 采用 SoM 作为动态高斯重建骨干。每个高斯原语定义在规范空间（canonical space），其均值 $\pmb{\mu}_{\mathrm{c}}$ 和旋转 $\mathbf{R}_{\mathrm{c}}$ 通过时间相关的 SE(3) 运动变换映射到时刻 $t$ 的变形空间：

$$\pmb{\mu}_t = \mathbf{R}_{ct} \pmb{\mu}_{\mathrm{c}} + \mathbf{t}_{ct}, \quad \pmb{R}_t = \mathbf{R}_{ct} \mathbf{R}_{\mathrm{c}}$$

其中 $\mathbf{R}_{ct}$ 和 $\mathbf{t}_{ct}$ 构成规范空间到时刻 $t$ 的旋转与平移。该运动变换由 $B$ 个共享运动基的加权和合成：

$$\mathbf{T}_{ct} = \sum_{b=1}^{B} w^{(b)} \mathbf{T}_{ct}^{(b)}$$

每个高斯的权重系数 $w^{(b)}$ 在优化中学习，构成了后续分组与预测的核心运动参数化对象。

投影到 2D 图像平面时，高斯均值和协方差经相机内外参变换：

$$\pmb{\mu}^{2D} = \pmb{\Pi}(\pmb{K} \pmb{E} \pmb{\mu}), \quad \pmb{\Sigma}^{2D} = \pmb{J} \pmb{E} \pmb{\Sigma} \pmb{E}^{\top} \pmb{J}^{\top}$$

其中 $\pmb{K}$ 为相机内参，$\pmb{E}$ 为外参，$\pmb{J}$ 为投影变换的雅可比近似。像素颜色通过 $N$ 个有序高斯的 alpha 混合得到：

$$C_p = \sum_{i=1}^{N} c_i \alpha_i T_i \mathcal{N}(\pmb{x}_p | \pmb{\mu}^{2D}, \pmb{\Sigma}^{2D})$$

### 模块一：运动感知高斯分组

该模块将高斯聚类为具有连贯运动的物体组，并为每组标注刚性（$\tau^{(k)}=1$）或非刚性（$\tau^{(k)}=0$）标签。分组策略采用交替的时空区域生长与关键帧高斯配准，而非简单的静态掩码投影。朴素扩展方案直接将 2D 掩码与投影位置关联：

$$G_{t}^{(k)} = \{ g \in \mathcal{G} \mid \operatorname{Proj}(g_t) \in M_t^{(k)} \}$$

但这种方式忽略了运动一致性，导致分组不完整。MoGaF 的混合方法通过引入运动一致性约束和跨帧配准，产生更完整的运动感知分组（见 Figure 3）。

### 模块二：分组约束优化

在获得分组后，MoGaF 对刚性组和非刚性组施加差异化的运动约束。

**刚性组**：组内所有高斯共享一个 SE(3) 变换 $\Phi_t^{(k)} = [\mathbf{R}_{ct}^{(k)} | \mathbf{t}_{ct}^{(k)}]$，将规范空间高斯映射到变形空间：

$$\Phi_t^{(k)}(g) = \mathbf{R}_{ct}^{(k)} \pmb{\mu}_{\mathrm{c},g} + \mathbf{t}_{ct}^{(k)}$$

刚性运动锚定损失衡量每个高斯学习到的运动与组级刚性变换之间的偏差：

$$\mathcal{L}_{\mathrm{rigid}}^{(k)} = \sum_{t} \sum_{g \in G^{(k)}} \big\| \pmb{\mu}_{t,g} - \Phi_t^{(k)}(g) \big\|_2^2$$

**非刚性组**：通过局部运动平滑性约束，鼓励规范空间中相邻高斯的运动系数保持一致：

$$\mathcal{L}_{\mathrm{nr}}^{(k)} = \sum_{g \in G^{(k)}} \sum_{g' \in \mathrm{NN}(g)} \| \pmb{w}_g - \pmb{w}_{g'} \|_2^2$$

其中 $\mathrm{NN}(g)$ 表示高斯 $g$ 在规范空间中的最近邻，$\pmb{w}_g$ 为运动基权重系数。

**总体运动约束损失**根据每组刚性标签自适应组合：

$$\mathcal{L}_{\mathrm{motion}} = \sum_{k=1}^{K} \left[ \tau^{(k)} \mathcal{L}_{\mathrm{rigid}}^{(k)} + (1 - \tau^{(k)}) \mathcal{L}_{\mathrm{nr}}^{(k)} \right]$$

该损失与光度重建损失联合优化，精炼 4DGS 表示。

### 模块三：分组运动预测

为每个运动组训练一个轻量级 Transformer 编码器，外推未来高斯运动。预测器以观测时间窗内的运动基系数序列为输入，输出未来时刻的运动变换。

**运动预测损失**最小化预测变换 $\hat{\mathbf{T}}_{T,g}$ 与真实变换 $\mathbf{T}_{T,g}$ 之间的 L2 误差：

$$\mathcal{L}_{\mathrm{pred}}^{(k)} = \frac{1}{|G^{(k)}|} \sum_{g \in G^{(k)}} \big\| \mathbf{T}_{T,g} - \hat{\mathbf{T}}_{T,g} \big\|_2^2$$

**加速度正则化**惩罚预测高斯均值的不平滑加速度，促进物理上平滑的运动轨迹：

$$\mathcal{L}_{\mathrm{acc}}^{(k)} = \frac{1}{|G^{(k)}|} \sum_{g \in G^{(k)}} \big\| \hat{\pmb{\mu}}_{T,g} - 2 \pmb{\mu}_{T-1,g} + \pmb{\mu}_{T-2,g} \big\|_2^2$$

**分组训练目标**为上述两项的加权和：

$$\mathcal{L}_{\mathrm{group}}^{(k)} = \mathcal{L}_{\mathrm{pred}}^{(k)} + \lambda_{\mathrm{acc}} \mathcal{L}_{\mathrm{acc}}^{(k)}$$

训练中引入掩码运动建模策略（受 NLP 掩码语言建模启发），对运动序列施加连续时间跨度的掩码，增强预测器对不完整观测的鲁棒性（消融实验表明移除掩码训练会导致 D-NeRF 上 PSNR 从 25.87 降至 24.68）。推理阶段采用自回归滚动预测，逐步外推未来帧的高斯运动参数。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2602_21668/figures/013_Figure_9.jpg]]
*Figure 9: Overview of the forecaster. (a) Training stage: The forecaster is trained for each Gaussian group*

## 实验与关键发现

### 核心瓶颈与实验逻辑

MoGaF 要解决的根本问题是：在动态 3D 高斯表示中，高斯原语独立运动，缺乏物体级别的运动一致性，导致长期预测中出现空间运动不连贯与轨迹漂移。实验设计围绕三个因果旋钮展开——运动感知高斯分组、分组约束优化、分组运动预测——通过消融实验逐层验证每个模块对运动连贯性和预测稳定性的贡献。

### 主实验结果

#### iPhone 数据集

Table 1 展示了 iPhone 数据集上的预测结果。在 80% 观察比例下，MoGaF 取得 **mPSNR 15.58**，相比重新实现到 SoM 骨干上的 **GSPred-SoM**（14.99）提升 +0.59；**mLPIPS 0.4227** 对比 0.4482 降低 0.0255。在更严苛的 60% 观察比例（预测剩余 40% 帧）下，MoGaF 仍保持领先（mPSNR 15.51，mSSIM 0.6143，mLPIPS 0.4245）。Table 4 补充了更多观察比例下的完整结果。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2602_21668/figures/005_Table_1.jpg]]
*Table 1: Forecasting results on the iPhone dataset. We forecast frames beyond the observed time window and evaluate the predicted frames rendered from held-out test viewpoints. The leftmost column (Obs. ratio) indicates the fraction of input training frames used by each model; 80% and 60% correspond to forecasting the remaining 20% and 40% of frames, respectively. † denotes methods that are re-implemented for the SoM-based 4DGS representation and retain their original forecasting scheme*

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2602_21668/figures/014_Table_4.jpg]]
*Table 4: Forecasting results on the iPhone dataset. We forecast frames beyond the observed time window and evaluate the predicted frames rendered from held-out test viewpoints. The leftmost column (Obs. ratio) indicates the fraction of input training frames used by each model*

Figure 4 的定性对比显示，MoGaF 在预测帧中保持了更清晰的物体边界和更少的运动模糊，尤其在涉及刚体位移（如人手移动物体）的场景中，基线方法出现明显的几何扭曲和伪影，而 MoGaF 的预测更接近真实帧。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2602_21668/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results on iPhone dataset. We present forecasted frames from test camera views. (a) and (b) correspond to settings where the first 80% and 60% of frames are used for training, and the remaining 20% and 40% are forecasted, respectively*

#### D-NeRF 数据集

Table 2 报告了 D-NeRF 数据集上 60% 观察比例的结果。MoGaF 取得 **PSNR 23.37**，显著优于 **GSPred**（21.78，+1.59）；SSIM 0.9147 vs 0.9011，LPIPS 0.0746 vs 0.0919。Table 5 补充了 80% 观察比例下的结果，趋势一致。Figure 5 的定性结果验证了 MoGaF 在合成场景中对非刚性形变（如人物姿态变化）的预测更加稳定。

#### 长期预测

Figure 6 展示了 iPhone 数据集上的长期外推结果。在观察窗口结束后，MoGaF 能够持续生成物理上合理的未来帧，而基线方法随时间推移迅速累积漂移误差。Figure 11 提供了更多长期预测的定性示例。

### 消融实验

#### 分组优化与分组预测的贡献

Table 3（上）在 iPhone 数据集上评估了跟踪性能。移除分组优化和分组预测后，**EPE 从 0.245 升至 0.296**（HC 配置），表明分组约束对 3D 运动跟踪精度有显著贡献。Table 7a 进一步拆分了分组优化、分组预测和编码器容量的影响：单独移除分组优化或分组预测均导致 EPE 增加，验证了两者协同作用的必要性。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2602_21668/figures/011_Table_3.jpg]]
*Table 3: Ablation results. (Top) Tracking performance on iPhone dataset. (Bottom) Masking performance on D-NeRF dataset*

#### 运动感知分组 vs 朴素静态分组

Table 7b 将 MoGaF 的运动感知高斯分组与朴素静态分组扩展 **Gaga-4D** 进行对比。MoGaF 的 mPSNR 为 **15.51 vs 15.31**，mSSIM 0.6143 vs 0.6101，mLPIPS 0.4245 vs 0.4315，验证了运动感知分组对预测质量的提升。Figure 3 从视觉上对比了三种分组策略：简单 3DGS 分组扩展、单帧掩码区域生长、以及 MoGaF 的混合方法，后者产生了更完整和可靠的运动感知高斯组。

#### 掩码运动建模的作用

Table 3（下）在 D-NeRF 数据集上评估了掩码运动建模训练策略。移除掩码训练后，**PSNR 从 25.87 降至 24.68**（-1.19），SSIM 和 LPIPS 也相应退化。Figure 7 定性展示了掩码训练对运动预测鲁棒性的增强效果。

![[assets/figures/papers/paper_list_l45_https_arxiv_org_abs_2602_21668/figures/010_Figure_7.jpg]]
*Figure 7: Effect of masking. Applying contiguous-span masking during training enhances the robustness of motion forecasting*

### 场景插值评估

Table 6 在 iPhone 数据集上比较了 MoGaF 与 **SoM** 骨干的场景插值性能。MoGaF 在保持与 SoM 可比的光度保真度的同时，提供了更精确的 3D 跟踪。Figure 10 展示了测试视角下的定性新视角合成结果，验证了分组约束优化不会损害重建质量。

### 失败模式与局限性

1. **4DGS 重建依赖**：方法建立在预训练的 4DGS 表示之上，预测质量受限于重建保真度。当初始重建无法恢复未观测的几何结构时，后续分组和预测均会受到影响；严重的运动优化失败会级联传播到预测阶段。
2. **物体间交互缺失**：当不同运动组在预测中发生空间重叠时，模型无法推理碰撞或物体间交互，可能导致物理上不合理的穿透或重叠。这一问题在密集多物体场景的长期预测中尤为突出。

### 公平性说明

为确保公平比较，实验将 **GSPred** 的 GCN 预测架构和 **ODE-GS** 的神经 ODE 预测器重新实现到 SoM 骨干上（得到 GSPred-SoM 和 ODE-GS-SoM），因为原始版本未使用深度、点跟踪等数据驱动先验。所有方法共享相同的 4DGS 重建基础，差异仅在于运动优化和预测策略。

## 定位与知识库关联

**MoGaF** 在动态场景时空预测的脉络中，占据了一个明确的位置：它并非重新设计4DGS重建骨干，而是在现有高质量动态重建（**SoM**）之上，通过**运动感知分组**这一因果性操作，将无结构的独立高斯原语提升为具有物体级运动一致性的结构化表示，从而显著改善长期外推的物理合理性与时间稳定性。

### 与基线方法的关系

本工作直接对标的核心基线是 **GSPred** 和 **ODE-GS**，二者代表了动态场景预测领域的两条典型技术路径：前者基于图卷积网络（GCN）对每高斯运动系数进行全局建模，后者则采用神经常微分方程（Neural ODE）在隐空间连续演化运动状态。为确保公平比较，作者将这两类预测架构重新实现在相同的 **SoM** 4DGS骨干上，得到 **GSPred-SoM** 和 **ODE-GS-SoM**，从而剥离了数据驱动先验（如深度、点跟踪）带来的混淆效应。实验结果表明，即便在统一骨干下，这些基线方法仍受限于独立高斯运动建模的固有缺陷——缺乏物体级运动一致性约束，导致长期预测中出现空间运动不连贯与轨迹漂移。

另一个重要的对照点是 **Gaga-4D**，它代表了将静态3DGS分组方法朴素扩展到动态场景的尝试。消融实验（Table 7b）显示，Gaga-4D的静态分组策略在预测性能上显著弱于MoGaF的运动感知分组（mPSNR 15.31 vs 15.51），这直接验证了“分组必须感知运动”这一核心设计选择的必要性。

### 方法适用边界

MoGaF的有效性建立在以下前提之上：

1.  **依赖预训练4DGS表示的质量**：方法以SoM重建的4DGS表示为基础，其分组、优化和预测均在此表示之上进行。若重建保真度不足（例如存在未观测的几何结构或严重的运动优化失败），这些误差将传播至后续所有阶段，且框架本身不具备恢复缺失几何的能力。
2.  **物体级运动可分离假设**：分组策略依赖于2D分割模型提供的物体掩码，以及运动基系数在规范空间中的局部平滑性。对于运动边界模糊、物体间存在显著相互遮挡或非刚性形变极度复杂的场景，分组的准确性可能下降。
3.  **无交互建模**：方法将每个运动组视为独立演化的实体，当预测中不同物体组发生重叠时，模型无法推理碰撞或物体间交互，可能导致物理上不合理的穿透或重叠。

### 局限与开放问题

论文明确指出的局限指向两个关键方向：

1.  **重建依赖的缓解**：当前框架对4DGS重建质量高度敏感。一个开放问题是，能否结合点云补全技术或生成式先验（如视频扩散模型提供的几何线索），在重建不完整的情况下仍能产生合理的预测结果。
2.  **物理交互的引入**：现有分组独立预测的范式无法处理物体间的碰撞与交互。如何扩展框架以加入物理约束（例如基于接触动力学的惩罚项）或构建物理感知的高斯表示，是提升预测物理合理性的重要方向。

此外，从方法谱系的角度看，MoGaF的掩码运动建模策略借鉴了自然语言处理中的掩码语言建模思想（**BERT**），将其适配到时序运动序列上以增强预测器的鲁棒性。这一跨领域迁移在D-NeRF数据集上的消融实验中得到验证（移除掩码训练导致PSNR从25.87降至24.68），但其有效性边界——例如掩码策略在不同运动频率场景下的泛化能力——仍有待进一步探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Space_Time_Forecasting_of_Dynamic_Scenes_with_Motion_aware_Gaussian_Grouping.pdf]]
