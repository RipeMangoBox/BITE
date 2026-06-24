---
title: "PhysHO: Physics-Based Dynamic 3D Gaussian Human and Object from Monocular Video"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PhysHO_Physics_Based_Dynamic_3D_Gaussian_Human_and_Object_from_Monocular_Video.pdf
project_link: "https://suezjiang.github.io/physho/"
code_link: null
aliases:
- PhysHO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将SMPL驱动的LBS作为可解释的驱动先验，结合MPM仿真器传播力；通过PD控制器和可学习的LBS影响因子（ω）实现针对性的内部驱动（仅作用于人体内部粒子），防止对物体的错误驱动。
primary_logic: 利用LBS定位人体内部力的来源，并通过MPM在物理约束下将力通过接触传播至物体，从而实现人-物交互的物理真实重建。
claims:
- PhysHO在LPIPS指标上显著优于非物理基线（GART、4D-Gaus），尤其在完整序列和较大变形子序列上表现突出（见表1）。
- 消融实验表明，物理感知微调、LBS影响因子和神经残余本构模型均对渲染质量和IoU有显著提升（见表2和表3）。
- 定性结果（图5、图6）显示PhysHO在重构和未来预测中产生更物理真实的运动和掩码精度。
- 自建人-物交互数据集（方形枕头、布包、C形枕头） 上 LPIPS = 0.1079 / 0.0804 / 0.0676 / 0.0651
---

# PhysHO: Physics-Based Dynamic 3D Gaussian Human and Object from Monocular Video

> [!tip] 核心洞察
> 利用LBS定位人体内部力的来源，并通过MPM在物理约束下将力通过接触传播至物体，从而实现人-物交互的物理真实重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhysHO：基于物理的单目视频人-物动态3D高斯重建 |
| 英文题名 | PhysHO: Physics-Based Dynamic 3D Gaussian Human and Object from Monocular Video |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Jiang_PhysHO_Physics-Based_Dynamic_3D_Gaussian_Human_and_Object_from_Monocular_CVPR_2026_paper.html) · [Project](https://suezjiang.github.io/physho/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PhysHO |
| Dataset | 自建人-物交互数据集（方形枕头、布包、C形枕头） |

> [!tip] 效果简介
> - 自建人-物交互数据集（方形枕头、布包、C形枕头） 上，LPIPS 0.1079 / 0.0804 / 0.0676 / 0.0651 vs GART、4D-Gaus（均更高） (显著更低（更好）)。

## 概述

从单目视频重建人-物交互的动态三维场景是计算机视觉中的一个核心挑战。现有方法要么依赖纯数据驱动的外观拟合，缺乏物理约束，导致运动不真实且无法泛化到新姿态；要么采用基于物理的仿真，但通常假设物体由均匀、各向同性的理想弹塑性材料构成，且仅使用重力等简单外力，无法建模人体内部肌肉驱动力和异质各向异性材料，从而限制了人-物动态的物理真实重建与预测能力。

针对上述瓶颈，本文提出 **PhysHO**，一个将可解释的人体驱动先验与连续介质物理仿真紧密结合的框架。其核心洞察在于：利用 SMPL 驱动的线性混合蒙皮（LBS）定位人体内部力的来源，并通过物质点法（MPM）在物理约束下将力通过接触传播至物体，从而实现人-物交互的物理真实重建。具体而言，PhysHO 通过可学习的 LBS 影响因子（$\omega$）实现针对性内部驱动——仅作用于人体内部粒子，防止对物体的错误驱动；同时引入基于专家模型的神经残余本构律，以每粒子潜在变量为条件，增强对异质各向异性材料的表达能力。

实验结果表明，PhysHO 在自建人-物交互数据集上显著优于非物理基线方法 **GART**（Lei et al., CVPR 2024）和 **4D-Gaus**（Wu et al., CVPR 2024）。在 LPIPS 指标上，PhysHO 在完整序列及较大变形子序列上均取得显著更低的数值（例如完整序列上 0.0651–0.1079，而基线方法均更高），表明其在渲染质量和物理真实性上的优势。消融实验进一步验证了物理感知微调、LBS 影响因子和神经残余本构模型等关键设计对重建精度和渲染质量的显著提升作用。定性结果也显示，PhysHO 在重构和未来预测中产生了更物理真实的运动和掩码精度。

在方法谱系上，PhysHO 位于基于模板的 3D 高斯人体重建与物理仿真驱动的动态建模的交叉地带。与纯运动学方法（如 GART、4D-Gaus）相比，它引入了连续介质力学约束；与既有物理驱动方法相比，它首次将 LBS 驱动的 PD 控制器与可学习的影响因子结合，实现了对人体内部驱动的精准建模，并通过残差本构模型突破了均匀材料假设的限制。

## 背景与动机

### 动态人-物交互重建的挑战

从单目视频中重建动态的人-物交互是计算机视觉与图形学中的核心难题。与静态场景或孤立人体重建不同，人-物交互场景涉及两个关键复杂性：**人体自身的非刚性运动**与**人-物之间的物理接触**。传统方法通常将人体与物体分开建模，或依赖纯数据驱动的方式拟合观测帧，缺乏对底层物理过程的理解。这导致两个突出问题：（1）重建结果在遮挡或快速运动区域产生非物理的形变与穿模；（2）无法泛化到训练分布之外的新颖姿态或未来帧预测。

### 现有物理驱动方法的瓶颈

近年来，基于物理的仿真方法被引入动态重建，试图通过物质点法（Material Point Method, MPM）等连续介质力学求解器来约束运动。然而，这些方法存在一个根本性瓶颈：**无法建模人体内部的驱动力和异质各向异性材料特性**。

具体而言，现有物理驱动重建方法面临以下缺口：

1. **驱动力缺失**：人体运动源于内部肌肉力，但现有方法通常仅施加全局重力或基于学习的隐式速度控制，缺乏可解释的内部驱动先验。这导致人体运动完全依赖外部观测信号驱动，在遮挡或模糊区域产生漂移。

2. **材料建模不足**：现有方法普遍采用理想弹性-塑性本构模型，假设材料是各向同性且均匀的。然而，人体组织（肌肉、脂肪、骨骼）和交互物体（布料、枕头等）具有显著的异质各向异性——不同部位硬度不同，不同方向响应各异。统一的本构模型无法捕捉这种差异，导致形变失真。

3. **人-物耦合困难**：当人体与物体接触时，力需要通过接触界面传播。若驱动力的作用范围不加区分地施加于人体和物体，会导致物体被错误地“驱动”而非通过接触被动响应，破坏交互的物理真实性。

### 本文动机与核心洞察

针对上述瓶颈，PhysHO 提出一个核心洞察：**利用 SMPL 驱动的线性混合蒙皮（Linear Blend Skinning, LBS）作为可解释的内部驱动先验，并通过 MPM 仿真器在物理约束下将力通过接触传播至物体**。

这一洞察的关键在于角色分工：
- **LBS 提供“意图”**：基于 SMPL 骨骼变换的 LBS 轨迹反映了人体的运动意图，可作为目标驱动的参考信号。
- **MPM 提供“物理”**：物质点法仿真器保证运动满足动量守恒和材料本构约束，确保形变物理真实。
- **接触传播“耦合”**：力仅作用于人体内部粒子，物体通过与人体粒子的接触自然响应，避免了对物体的错误驱动。

基于此，PhysHO 在三个层面突破现有瓶颈：（1）引入基于 PD 控制器的目标驱动机制，配合可学习的 LBS 影响因子实现空间定位的内部驱动；（2）在专家弹塑性模型之上叠加神经残余本构律，以每粒子潜变量为条件建模异质各向异性材料；（3）通过结构保持的 3D 流监督和渐进式训练调度，使物理仿真在单目训练中稳定收敛。

## 核心创新

PhysHO 的核心创新在于将**可解释的人体驱动先验**与**物理仿真器**深度耦合，解决了现有物理驱动重建方法无法建模人体内部驱动力和异质各向异性材料的关键瓶颈。其相对于非物理基线（**GART**, Lei et al., CVPR 2024；**4D-Gaus**, Wu et al., CVPR 2024）和传统物理方法的改进主要体现在以下三个 changed slots：

### 1. 人体内部驱动建模：从全局外力到局部目标驱动

传统物理仿真方法通常仅依赖重力或基于学习的全局速度场来驱动人体运动，无法区分人体主动运动与被动物体响应。PhysHO 提出了一种**基于 LBS 轨迹的 PD 控制器 + 可学习 LBS 影响因子（ω）**的目标驱动机制：

- **驱动源定位**：利用 SMPL 驱动的 LBS 为每个人体内部粒子提供参考轨迹 $\mu_{lbs}^{i,n}$ 和参考速度 $v_{lbs}^{i,n}$，作为 PD 控制器的跟踪目标：
  $$f_{PD}^{i,n} = k_{p}(\mu_{lbs}^{i,n} - x^{i,n}) + k_{d}(v_{lbs}^{i,n} - v^{i,n})$$
- **空间选择性驱动**：通过可学习的每粒子影响因子 $\omega^i$ 调制驱动力 $f_{ex}^{i,n} = \omega^{i} f_{PD}^{i,n}$，使驱动力**仅作用于 SMPL 体积内部的人体粒子**，防止对物体产生虚假驱动。这一设计确保了人体运动由内部肌肉力驱动，而物体运动仅通过 MPM 物理仿真中的接触力传播产生（见 Figure 3）。

该机制的核心洞察在于：LBS 提供了人体骨骼运动的可解释先验，而 MPM 仿真器负责在物理约束下将力通过接触传播至物体，从而实现人-物交互的物理真实重建。

### 2. 材料本构模型：从均匀各向同性到异质各向异性

传统 MPM 仿真通常采用理想弹性-塑性模型，假设材料均匀各向同性，难以表达人体组织与不同物体的差异化物理属性。PhysHO 提出**基于专家模型的神经残余本构律**：

$$\pmb{\sigma} = \pmb{\mathcal{E}}(\pmb{F},\pmb{E},\pmb{\nu}) + \pmb{\mathcal{E}}_{\theta}(\pmb{F},\pmb{l}_{e}), \qquad \pmb{F} = \pmb{\mathcal{P}}(\pmb{F}^{trial}) + \pmb{\mathcal{P}}_{\theta}(\pmb{F}^{trial},\pmb{l}_{p})$$

- **残差形式**：应力与变形梯度表示为专家模型（如 Neo-Hookean 弹性、von Mises 塑性）与神经残差网络之和，以每粒子潜在变量 $\pmb{l}_e, \pmb{l}_p$ 为条件。
- **异质各向异性**：每粒子潜在变量允许网络学习空间变化的杨氏模量、泊松比及各向异性响应，从而区分人体皮肤、衣物和不同物体的材料特性。
- **实现细节**：残差网络受 **NeuMA** 启发，在预训练 NCLaw 网络上添加 LoRA 层作为残差项，保持专家模型的物理基础同时增强表达能力。

### 3. 单目训练监督：从纯 RGB 损失到结构保持 3D 流监督

单目视频缺乏显式 3D 监督，仅靠 RGB 损失难以约束物理仿真的粒子运动。PhysHO 引入**结构保持 3D 流监督 + 渐进式损失平衡训练调度**：

- **3D 流监督**：通过优化每帧粒子位置，联合最小化 RGB 渲染损失、光流损失和 ARAP（As-Rigid-As-Possible）正则项：
  $$\mathcal{L}_{SP-Flow} = \lambda_{rgb} \mathcal{L}_{rgb} + \lambda_{flow} \mathcal{L}_{flow} + \lambda_{arap} \mathcal{L}_{arap}$$
  ARAP 项保持局部刚性结构，防止粒子在缺乏视觉约束的区域发生非物理变形。
- **端到端对齐**：最终损失将 RGB 渲染损失与优化后的 3D 流位置对齐：
  $$\mathcal{L}_{E2E} = \lambda_{rgb} \mathcal{L}_{rgb} + \lambda_{3Dflow} \| \pmb{x}_{n+1} - \pmb{x}_{n+1}' \|_1$$
- **渐进式训练**：从小片段开始训练，逐步扩展帧范围，并根据每帧损失动态分配迭代次数，确保单目训练的稳定性和收敛性。

消融实验（Table 2、Table 3）验证了上述三个创新点的有效性：物理感知微调将 PSNR 从 25.42 提升至 27.30，LPIPS 从 0.0854 降至 0.0681；移除 LBS 影响因子或神经残余本构模型均导致重建 IoU 和渲染质量显著下降。

## 整体框架

PhysHO 的整体设计围绕一个核心耦合展开：将 **SMPL 驱动的线性混合蒙皮（LBS）** 作为可解释的人体驱动先验，与 **物质点法（MPM）物理仿真器** 紧密融合，从而在物理约束下重建单目视频中的人-物动态交互。

### 输入-输出流

系统以**单目人-物交互视频**为输入，输出具有物理真实感的动态 3D 高斯表示，并支持对未来帧的物理仿真预测（Figure 1）。整个流程可概括为以下阶段：

1. **规范空间重建**：基于 SMPL 骨骼和固定蒙皮权重，在规范空间构建 3D 高斯表示，每个高斯粒子同时作为 MPM 粒子，质量固定不变。
2. **物理感知微调**：通过零应力 MPM 仿真计算变形梯度，利用变形梯度更新高斯协方差矩阵，使渲染参数适配物理变形。
3. **目标驱动仿真**：以 LBS 轨迹为参考，通过 PD 控制器生成驱动力，并由可学习的每粒子影响因子 $\omega^i$ 进行调制，确保力**仅作用于 SMPL 体积内部的人体粒子**，物体则通过接触力被动响应。
4. **材料建模增强**：在专家弹塑性本构模型之上叠加神经残差网络，以每粒子潜变量为条件，建模异质各向异性材料。
5. **训练监督**：采用结构保持的 3D 流监督（RGB + 光流 + ARAP）与渐进式损失平衡训练调度，实现单目视频的稳定优化。

### 模块关系

Figure 2 展示了各模块的协同关系。核心耦合体现在两个层面：

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_PhysHO_Physics_B/figures/002_Figure_2.jpg]]
*Figure 2: PhysHO framework. We couple SMPL-driven LBS with an MPM simulator, where LBS provides a localized actuation prior inside the human and MPM propagates forces through contact to objects under physical constraints. Residual neural constitutive laws model heterogeneous and anisotropic materials. Training uses a structure-preserving 3D flow prior and progressive loss-balanced optimization*

- **LBS-MPM 耦合**：LBS 提供人体内部力的来源定位，MPM 负责在物理约束下将力通过接触传播至物体。这一设计解决了现有方法无法建模人体内部驱动力的问题。
- **神经-物理耦合**：神经残余本构模型以残差形式叠加在专家模型之上（$\pmb{\sigma} = \pmb{\mathcal{E}} + \pmb{\mathcal{E}}_{\theta}$），既保留了物理先验的稳定性，又增强了材料异质各向异性的表达能力。

每帧更新流程（Algorithm 2）为：计算目标驱动力 → MPM 子步积分（Algorithm 1）→ 塑性修正 → 变形梯度更新高斯参数 → 渲染与损失计算。

## 核心模块与公式推导

### 4.1 基于LBS的规范高斯重建与物理感知微调

**场景表示。** PhysHO将场景表示为一组质量保持的固定数量3D高斯，这些高斯同时充当MPM粒子。规范空间的高斯通过SMPL骨骼与固定蒙皮权重驱动，利用线性混合蒙皮（LBS）变换到姿态空间：

$$
\mu_{lbs}^{i} = A_{rot}^{i}\mu_{c}^{i} + A_{t}^{i}, \quad R_{lbs}^{i} = A_{rot}^{i}R_{c}^{i}, \quad A^{i}(\theta) = \sum_{k} W_{k}^{i} B_{k}(\theta)
$$

其中 $\mu_{c}^{i}$、$R_{c}^{i}$ 为规范空间高斯的位置与旋转，$A_{rot}^{i}$、$A_{t}^{i}$ 为骨骼变换的旋转与平移分量，$W_{k}^{i}$ 为粒子 $i$ 对骨骼 $k$ 的固定蒙皮权重，$B_{k}(\theta)$ 为姿态 $\theta$ 下的骨骼变换矩阵。

**物理感知微调。** 为弥合运动学LBS与物理驱动变形之间的鸿沟，引入物理感知微调阶段：通过零应力MPM仿真计算变形梯度 $F^{i,n}$，据此更新高斯协方差矩阵，使渲染参数适应物理变形：

$$
\Sigma^{i,n} = F^{i,n} R_{lbs}^{i,0} S_{lbs}^{i,0} (S_{lbs}^{i,0})^{\top} (R_{lbs}^{i,0})^{\top} (F^{i,n})^{\top}
$$

该步骤保持粒子集质量守恒且数量固定。粒子速度通过中心差分从LBS位置估计：

$$
\mathbf{v}_n = \frac{\mathbf{x}_{n+1} - \mathbf{x}_{n-1}}{2 \cdot \Delta t}
$$

### 4.2 LBS集成的目标驱动动力学

PhysHO的核心创新在于将LBS作为可解释的驱动先验，通过PD控制器实现人体内部力的来源定位，再经由MPM在物理约束下将力通过接触传播至物体。目标驱动机制（图3）包含两层设计：

**PD控制器。** 以LBS轨迹为参考，对每个粒子施加比例-微分力：

$$
f_{PD}^{i,n} = k_{p}(\mu_{lbs}^{i,n} - x^{i,n}) + k_{d}(v_{lbs}^{i,n} - v^{i,n})
$$

其中 $k_{p}$、$k_{d}$ 为控制增益，$\mu_{lbs}^{i,n}$、$v_{lbs}^{i,n}$ 为LBS参考位置与速度，$x^{i,n}$、$v^{i,n}$ 为当前仿真状态。

**LBS影响因子。** 为防止驱动力错误作用于物体，引入可学习的每粒子影响因子 $\omega^{i}$ 调制外部力：

$$
f_{ex}^{i,n} = \omega^{i} f_{PD}^{i,n}
$$

仅位于SMPL体积内部的粒子接收直接驱动，物体则通过接触间接受力。这一设计实现了**最小化、空间定向的内部驱动**，是PhysHO人-物交互物理真实性的关键保障。

### 4.3 神经残余本构模型

传统MPM仿真采用理想弹塑性模型（各向同性、均匀），无法表达人体与物体的异质各向异性材料特性。PhysHO提出在专家模型之上叠加神经残差：

$$
\pmb{\sigma} = \pmb{\mathcal{E}}(\pmb{F},\pmb{E},\pmb{\nu}) + \pmb{\mathcal{E}}_{\theta}(\pmb{F},\pmb{l}_{e}), \qquad \pmb{F} = \pmb{\mathcal{P}}(\pmb{F}^{trial}) + \pmb{\mathcal{P}}_{\theta}(\pmb{F}^{trial},\pmb{l}_{p})
$$

其中 $\pmb{\mathcal{E}}$、$\pmb{\mathcal{P}}$ 为专家弹塑性模型的应力与塑性投影算子，$\pmb{\mathcal{E}}_{\theta}$、$\pmb{\mathcal{P}}_{\theta}$ 为以每粒子潜变量 $\pmb{l}_{e}$、$\pmb{l}_{p}$ 为条件的神经残差网络。该设计受NeuMA启发，以LoRA层作为残差项叠加到预训练NCLaw网络之上，使模型能够学习空间变化的杨氏模量与泊松比，从而建模异质各向异性材料。

### 4.4 结构保持3D流监督与渐进训练

单目训练缺乏多视图几何约束，PhysHO引入结构保持3D流监督以优化每帧粒子位置：

$$
\mathcal{L}_{SP-Flow} = \lambda_{rgb} \mathcal{L}_{rgb} + \lambda_{flow} \mathcal{L}_{flow} + \lambda_{arap} \mathcal{L}_{arap}
$$

其中 $\mathcal{L}_{rgb}$ 为RGB渲染损失，$\mathcal{L}_{flow}$ 为光流一致性损失，$\mathcal{L}_{arap}$ 为尽可能刚性（ARAP）正则项，共同约束粒子运动的几何一致性。端到端训练损失结合RGB渲染与对齐优化后3D流位置的L1距离：

$$
\mathcal{L}_{E2E} = \lambda_{rgb} \mathcal{L}_{rgb} + \lambda_{3Dflow} \| \pmb{x}_{n+1} - \pmb{x}_{n+1}' \|_1
$$

训练采用渐进式损失平衡调度器：先从小片段开始训练，逐步扩展帧范围，根据每帧损失动态分配迭代次数，以稳定单目训练过程。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_PhysHO_Physics_B/figures/003_Figure_3.jpg]]
*Figure 3: Targeted actuation. LBS reference motion drives a PD controller whose forces are modulated per particle by the LBSimpact factor*

## 实验与分析

### 评估基准与对比基线

PhysHO 在一个自建的人-物交互数据集上进行评估，该数据集包含方形枕头（Square Pillow）、布包（Cloth Bag）和 C 形枕头（C-shape Pillow）等多个序列，每个序列由旋转阶段（spin stage）和动态交互阶段（dynamic stage）组成（见 Figure 4）。对比基线包括两类代表性方法：

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_PhysHO_Physics_B/figures/004_Figure_4.jpg]]
*Figure 4: Part of our dataset. Each sequence consists of a spin stage and a dynamic stage*

- **GART**（Lei et al., CVPR 2024）：基于模板的 3D 高斯人体重建方法，不引入物理约束。
- **4D-Gaus**（Wu et al., CVPR 2024）：动态 3D 高斯重建方法，同样不依赖物理仿真。

评估指标涵盖 LPIPS、PSNR、SSIM 等渲染质量指标，以及重建掩码的 IoU。

### 主实验结果

**Table 1** 报告了动态重建与未来预测的定量对比。PhysHO 在感知质量指标 LPIPS 上一致优于非物理基线，尤其在完整序列和较大变形子序列上表现突出：

- 方形枕头完整序列：LPIPS 0.1079（GART 和 4D-Gaus 均更高）
- 布包完整序列：LPIPS 0.0804
- C 形枕头序列：LPIPS 0.0676 / 0.0651

这一优势源于物理仿真器对接触力传播的真实建模——LBS 提供的人体内部驱动通过 MPM 在物理约束下传递至物体，而非物理基线则缺乏此类力学约束，导致渲染伪影和运动失真。

**Figure 5** 的定性对比进一步印证了上述结论：PhysHO 在动态重建和未来预测中生成的运动轨迹更符合物理直觉，物体变形和接触边界更加自然；相比之下，GART 和 4D-Gaus 在人体与物体接触区域出现明显的几何穿透和运动不协调。**Figure 6** 的掩码精度对比显示，PhysHO 在重建与预测的边界区域（图中灰色虚线处）保持了更高的掩码一致性，说明物理约束有效抑制了非物理形变带来的轮廓漂移。

### 消融实验

消融实验从三个关键设计维度验证了各模块的贡献。

**物理感知微调（Physics-Aware Fine-Tuning）**：**Table 2** 的渲染质量消融表明，引入物理感知微调后，PSNR 从 25.42 提升至 27.30，LPIPS 从 0.0854 降至 0.0681。该模块通过在零应力 MPM 仿真中计算变形梯度来微调高斯参数，弥合了运动学 LBS 与物理驱动变形之间的差异，使渲染参数适应真实的力学变形。

**LBS 影响因子与神经残余本构模型**：**Table 3** 的重建精度消融显示，移除 LBS 影响因子（ω）或神经残余本构模型均导致重建 IoU 和渲染质量下降。LBS 影响因子通过可学习的每粒子权重调制 PD 控制器的驱动力，确保仅 SMPL 体积内部的人体粒子接收直接驱动，防止对物体的错误施力（见 Figure 3 的目标驱动机制）。神经残余本构模型在专家弹塑性模型之上叠加每粒子条件残差网络，增强了材料异质各向异性的表达能力，这对于准确建模人体软组织与不同材质物体的交互至关重要。

**结构保持 3D 流监督与渐进训练**：论文指出，结构保持 3D 流监督（RGB + 光流 + ARAP 联合损失）和渐进式损失平衡训练调度对单目训练的稳定性和准确性有显著贡献（见 Sec. 4.4）。渐进训练从小片段开始，逐步扩展帧范围，并根据每帧损失动态分配迭代次数，有效缓解了长序列训练中的漂移问题。

### 失败模式与局限性

当前分析材料中未提供明确的失败案例或局限性讨论。从方法设计推断，潜在风险包括：LBS 驱动先验依赖 SMPL 姿态估计精度，在严重遮挡或快速运动场景下可能引入驱动误差；神经残余本构模型的泛化能力受限于训练数据的材质多样性；MPM 仿真步长需要在精度与计算效率之间权衡。以上推断需结合原文局限性章节进行手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_PhysHO_Physics_B/figures/010_Table_2.jpg]]
*Table 2: Quantitative evaluation of rendering quality*

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_PhysHO_Physics_B/figures/011_Table_3.jpg]]
*Table 3: Quantitative evaluation of reconstruction accuracy*

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_PhysHO_Physics_B/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of dynamic reconstruction and future prediction with GART [30] and 4D-Gaus [63]*

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_PhysHO_Physics_B/figures/008_Figure_6.jpg]]
*Figure 6: Comparison of mask accuracy. The gray dashed line marks the boundary between reconstruction and prediction*

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_PhysHO_Physics_B/figures/007_Figure_7.jpg]]
*Figure 7: Qualitative evaluation of rendering quality*

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_PhysHO_Physics_B/figures/009_Figure_8.jpg]]
*Figure 8: Qualitative evaluation of reconstruction accuracy*

## 方法谱系与知识库定位

### 1. 与现有基线的关系

PhysHO 在单目人-物交互重建这一交叉领域，与两类基线形成明确对比：

**（1）非物理的动态高斯重建方法**

- **GART**（Lei et al., CVPR 2024）：基于模板的 3D 高斯人体重建，完全依赖外观损失驱动变形，缺乏物理约束。在 PhysHO 的实验中，GART 在 LPIPS 指标上显著落后，尤其在较大变形子序列上，其纯视觉驱动无法维持物理合理性（见 Table 1、Figure 5）。
- **4D-Gaus**（Wu et al., CVPR 2024）：动态 3D 高斯重建方法，同样不引入物理先验。在 PhysHO 的对比中，4D-Gaus 的掩码精度和未来预测能力明显弱于物理驱动方案（Figure 6）。

PhysHO 与这两者的本质区别在于：它将 SMPL 驱动的 LBS 与 MPM 仿真器紧耦合，使变形服从连续介质动量守恒，而非纯数据驱动的外观拟合。这一设计使 PhysHO 在重建精度和未来预测的物理合理性上均取得优势。

**（2）同领域物理驱动方法的对比定位**

PhysHO 与以下物理驱动重建工作的关系值得关注（需手动核实具体论文信息）：

- **NCLaw 系列**（NeuMA 等）：PhysHO 的神经残余本构模型直接受 NeuMA 启发——在预训练 NCLaw 网络上叠加 LoRA 层作为残差项（Sec. 4.4）。但 PhysHO 将这一思想从单一材料扩展到异质各向异性的人-物耦合系统，并引入每粒子潜变量条件化，这是对 NCLaw 框架的重要泛化。
- **基于速度控制的人体驱动方法**：PhysHO 提出的 LBS 驱动 PD 控制器 + 可学习影响因子 ω 的机制，区别于现有工作中无针对性（如仅施加重力）或基于学习速度控制的驱动方式。其核心创新在于：通过 SMPL 体积掩码将驱动力**仅作用于人体内部粒子**，防止对物体的错误驱动，从而提升交互保真度。

### 2. 适用边界

PhysHO 的设计隐含以下适用前提：

1. **单目视频输入**：方法假设输入为单目人-物交互视频，且人体姿态可通过 SMPL 参数化。对于非 SMPL 可表示的人体形态或极端遮挡场景，LBS 驱动先验可能失效。
2. **固定粒子数量与质量保持**：场景由固定数量的 3D 高斯粒子表示，粒子质量在仿真中保持不变（Sec. 4.1）。这意味着方法不能处理拓扑变化（如物体撕裂、分离）。
3. **已知交互对象类别**：神经残余本构模型需要每粒子潜变量条件化，其泛化到未见物体类别的能力未经验证。
4. **旋转阶段初始化**：数据集要求每个序列包含旋转阶段（spin stage）以构建初始几何（Figure 4），这限制了在任意采集条件下的直接应用。

### 3. 局限与开放问题

**已识别的局限：**

- **材料模型的泛化边界**：神经残余本构模型在训练物体上表现良好，但对全新材料（如液体、颗粒物）的零样本泛化能力未经验证。残差网络以每粒子潜变量为条件，其潜空间的语义可解释性尚不明确。
- **驱动力的物理真实性**：PD 控制器以 LBS 轨迹为参考目标，本质上是一种运动学驱动的力模型，而非真正的肌肉-骨骼动力学。当 LBS 轨迹本身不物理（如 SMPL 估计误差较大时），驱动力可能引入非物理伪影。
- **计算开销**：MPM 仿真器在每帧内执行 T 个子步（Algorithm 1），且需要结合渐进式损失平衡训练调度，训练效率在长序列上可能成为瓶颈。

**需手动核实的开放问题：**

- 论文未明确讨论 PhysHO 在**多人与多物体**交互场景下的扩展性。当前框架假设单人与单一物体的交互，粒子归属（人体 vs. 物体）的判定依赖 SMPL 体积掩码，多实例场景需要额外的实例分割与归属分配机制。
- 对**非刚性物体的内部状态估计**（如布料褶皱的应力分布）的定量评估缺失。现有实验仅从渲染质量和掩码精度评估，物理量的真实性（如接触力、应变能）未经验证。
- 方法是否支持**反向优化**（从物理仿真反向修正 SMPL 姿态估计）未讨论，这可能是提升整体鲁棒性的重要方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/PhysHO_Physics_Based_Dynamic_3D_Gaussian_Human_and_Object_from_Monocular_Video.pdf]]