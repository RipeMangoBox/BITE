---
title: Gaussian-Mixture Latent Flow for Stochastic 3D Human Motion Prediction
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Gaussian_Mixture_Latent_Flow_for_Stochastic_3D_Human_Motion_Prediction.pdf
project_link: null
code_link: null
aliases:
- GMLF
- GMLFS3HMP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 潜空间先验分布的选择：从单模态标准高斯切换到数据驱动的多模态高斯混合分布，直接决定模型能否解耦多样化运动模式并提升预测合理性与不确定性估计。
primary_logic: 利用无监督EM算法学习高斯混合潜空间先验，结合可逆流模型和基于ODE的流匹配框架，既能自然解耦运动语义、提升预测合理性，又能通过精确似然计算实现原则性的不确定性估计。
claims:
- 在Human3.6M和AMASS数据集上，FDE分别相对先前SOTA降低8.5%和13%，同时ADE、MMADE、MMFDE等指标均达到或接近最优。
- 消融实验表明，使用可学习的高斯混合先验显著优于固定混合先验或标准高斯先验；移除多模态先验后，准确性和合理性指标全面下降。
- 高斯混合潜空间模型在Human3.6M和AMASS上均取得最佳对数似然（LL），证明其对复杂运动分布建模的有效性；而施加过于简单的先验甚至不如无先验的纯流匹配。
- Human3.6M 上 FDE = 0.399
---

# Gaussian-Mixture Latent Flow for Stochastic 3D Human Motion Prediction

> [!tip] 核心洞察
> 利用无监督EM算法学习高斯混合潜空间先验，结合可逆流模型和基于ODE的流匹配框架，既能自然解耦运动语义、提升预测合理性，又能通过精确似然计算实现原则性的不确定性估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向随机3D人体运动预测的高斯混合潜流模型 |
| 英文题名 | Gaussian-Mixture Latent Flow for Stochastic 3D Human Motion Prediction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ma_Gaussian-Mixture_Latent_Flow_for_Stochastic_3D_Human_Motion_Prediction_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Gaussian-Mixture Latent Flow |
| Dataset | Human3.6M, AMASS |

> [!tip] 效果简介
> - Human3.6M 上，FDE 0.399 vs 先前SOTA (-8.5%)；ADE 0.333 vs 先前SOTA (达到最优)；MMADE 0.471 vs 先前SOTA (排名第二或第三)。
> - AMASS 上，FDE 0.474 vs 先前SOTA (-13%)；ADE 0.461 vs 先前SOTA (达到最优)；MMADE 0.540 vs 先前SOTA (排名最优)。

## 概述

3D人体运动预测（3D Human Motion Prediction, HMP）的核心挑战在于：给定一段历史运动观测，未来运动存在多种物理上合理的可能性。现有随机预测方法普遍使用**单模态先验**（如标准高斯分布），导致不同行为模式在潜空间中语义纠缠，预测结果物理不合理且缺乏可解释的不确定性量化。

本文提出**Gaussian-Mixture Latent Flow**，核心思路是**将潜空间先验从单模态标准高斯切换为数据驱动的多模态高斯混合分布**，从根本上解耦多样化运动模式。具体而言，方法利用无监督EM算法学习高斯混合潜空间先验，结合可逆Part-aware流模型和基于ODE的流匹配框架，在保持精确似然计算能力的同时，实现原则性的不确定性估计。

在Human3.6M和AMASS两个基准数据集上，该方法在准确性和合理性指标上均达到或接近最优：FDE分别相对先前SOTA降低**8.5%**和**13%**，ADE达到最优。消融实验进一步验证，可学习的高斯混合先验是性能提升的关键——移除多模态先验或退化为标准高斯先验后，各项指标全面下降。此外，高斯混合潜空间在两组数据集上均取得最佳对数似然（LL），证明其对复杂运动分布建模的有效性。

## 背景与动机

3D人体运动预测（3D Human Motion Prediction, HMP）旨在根据观测到的历史姿态序列，生成未来一段时间的合理运动轨迹。该任务在自动驾驶、人机交互、运动合成等领域具有重要应用价值。然而，人类运动本质上是多模态的——相同的观测历史可能对应多种不同的未来行为（如“行走”后可能接“站立”或“转弯”），这使得确定性预测方法难以满足实际需求，随机预测逐渐成为主流范式。

现有随机HMP方法普遍依赖**单模态潜空间先验**。无论是基于变分自编码器（VAE）的方法（如**DLow**），还是基于扩散模型的方案（如**BeLFusion**、**SkeletonDiff**、**CoMusion**、**TransFusion**），其潜变量通常被假设服从标准高斯分布 $\mathcal{N}(0, I)$。这一假设带来了两个核心缺陷：

1. **语义纠缠**：单模态先验强制将所有运动模式压缩到同一高斯分布下，导致“行走”和“跑步”等不同行为模式在潜空间中边界模糊、相互重叠，解码后容易产生物理不合理的姿态。
2. **不确定性量化缺失**：标准高斯先验无法提供原则性的不确定性估计，模型无法区分“高度确定的简单步态”与“高度不确定的复杂转向”，限制了其在安全关键场景中的应用。

另一个被忽视的问题是**生成模型骨干的选择**。VAE和基于SDE的扩散模型虽然灵活，但前者存在后验坍塌风险，后者训练不稳定且难以进行精确似然计算。这进一步削弱了模型对复杂运动分布的建模能力和可解释性。

针对上述瓶颈，本文提出**高斯混合潜流模型（Gaussian-Mixture Latent Flow）**，核心动机是：**将潜空间先验从单模态标准高斯切换为数据驱动的多模态高斯混合分布**。这一设计通过无监督EM算法自动学习运动模式的聚类结构，在潜空间中自然解耦不同行为语义，提升预测合理性。同时，采用可逆流模型作为编码-解码骨干，结合基于ODE的流匹配框架，使模型具备精确似然计算能力，从而为不确定性估计提供原则性基础。

简言之，本文试图回答一个关键问题：**能否通过改进潜空间先验的结构，从根本上解决随机运动预测中的语义纠缠与不确定性量化难题？**

## 核心创新

本工作围绕随机3D人体运动预测中的**潜空间先验选择**这一核心因果旋钮，提出了一套系统性创新方案。现有方法普遍采用单模态标准高斯分布作为潜空间先验，导致多样化运动模式在潜空间中语义纠缠，预测结果的物理合理性不足且缺乏可解释的不确定性量化。本文的 **Gaussian-Mixture Latent Flow** 方法通过以下四个关键 changed slots 实现了突破。

### 1. 潜空间先验：从单模态高斯到数据驱动高斯混合

最核心的创新在于将潜空间先验从标准高斯分布替换为**基于无监督EM算法学习的数据驱动高斯混合分布（Gaussian Mixture Model）**。具体而言，潜变量分布定义为：

$$q_z(\mathbf{Z}) = \sum_{i=1}^{K} \beta_i \mathcal{N}(\pmb{\mu}_i, \pmb{\sigma}_i)$$

其中 $K$ 个高斯分量及其权重 $\beta_i$、均值 $\pmb{\mu}_i$、标准差 $\pmb{\sigma}_i$ 均通过E步与M步交替优化无监督学习得到，无需动作类别标签即可自然解耦不同运动行为模式。这一设计直接回应了核心瓶颈：多模态先验能够有效减少语义纠缠，使不同运动模式在潜空间中占据不同分量，从而提升预测的物理合理性与多样性。

### 2. 生成模型骨干：从VAE/扩散到可逆流模型 + ODE流匹配

方法将生成模型骨干从VAE或基于SDE的扩散模型替换为**可逆Part-aware流模型 + ODE流匹配框架**。流模型的可逆性使得同一模型可通过前向和逆向过程分别充当编码器和解码器，无需额外训练解码网络。在潜空间预测阶段，采用条件流匹配损失训练速度场 $v_{\theta}$：

$$\mathbb{E}_{\mathbf{Z}_1 \sim p_{\mathrm{data}}, \hat{\mathbf{Z}}_0 \sim p_{\mathbf{Z}_0}, t \sim [0,1]} \| (\mathbf{Z}_1 - \hat{\mathbf{Z}}_0) - v_{\theta}(\mathbf{Z}_t, t) \|_2^2$$

该框架将SDE训练替换为ODE训练，利用连续归一化流的即时变量替换公式，可沿轨迹积分计算潜变量对数似然：

$$\log p(\hat{\mathbf{Z}}_1) = \log p(\hat{\mathbf{Z}}_0) + \int_0^1 -\mathrm{tr}(\boldsymbol{\nabla}_{\mathbf{Z}_t} v_{\theta}(\mathbf{Z}_t, t)) \mathrm{d}t$$

这为原则性的不确定性估计提供了精确似然计算能力，是相对于扩散模型（仅能近似估计似然）的重要优势。

### 3. 条件机制：从隐式重建到显式历史条件

方法将观测历史从“重建目标”提升为**显式条件信号**，融入潜变量演化过程。在流匹配框架中，速度场 $v_{\theta}$ 显式接受观测序列作为条件输入，强化历史与未来的因果依赖。消融实验证实，移除观测条件（w/o Condition）后，多样性与准确性均显著下降，验证了显式条件建模的必要性。

### 4. Tokenization与注意力：从姿态级到关节点级 + 骨架感知

方法独有地将tokenization粒度从姿态级（空间tokenization）下沉到**关节点级（关节时间轨迹tokenization）**，并在速度场网络中采用关节点维度上的缩放点积自注意力：

$$\mathrm{Attention}(\mathbf{Q}_i, \mathbf{K}_i, \mathbf{V}_i) = \mathrm{softmax}(\frac{\mathbf{Q}_i^T \mathbf{K}_i}{\sqrt{d_k}}) \mathbf{V}_i$$

这种骨架感知Transformer显式建模人体关节间的空间依赖性，将骨架结构先验注入潜动力学建模。消融实验表明，替换为空间tokenization后，准确性与合理性指标均大幅退化，验证了关节级建模的关键作用。

### 创新协同效应

上述四个 changed slots 形成协同闭环：高斯混合先验解耦运动语义，可逆流模型提供精确似然计算，显式条件机制强化历史依赖，关节点注意力注入骨架先验。在Human3.6M和AMASS数据集上，FDE分别相对先前SOTA降低8.5%和13%，同时ADE达到最优。消融实验进一步证实，可学习的高斯混合先验显著优于固定混合先验或标准高斯先验，且高斯混合潜空间在两大数据集上均取得最佳对数似然（LL），验证了其对复杂运动分布建模的优越性。

## 整体框架

本文提出的**高斯混合潜流模型（Gaussian-Mixture Latent Flow）**构建了一个端到端的随机人体运动预测框架，其核心设计围绕两个关键瓶颈展开：（1）用数据驱动的多模态高斯混合先验替代传统单模态标准高斯分布，解耦多样化运动模式；（2）以可逆流模型结合基于ODE的流匹配框架替代VAE或SDE扩散骨干，实现精确似然计算与原则性不确定性估计。整体pipeline由五个紧密耦合的模块构成，形成“编码—先验学习—潜动力学演化—解码”的闭环。

### 输入输出流

框架的输入为观测历史运动序列，输出为多条合理的未来运动预测样本。具体而言，给定一段长度为 $T_{\text{obs}}$ 的观测姿态序列，模型首先将其与复制最后一帧填充至完整长度 $T_{\text{full}}$，经频域变换后映射到潜空间获得初始潜代码 $\mathbf{Z}_0$；随后在潜空间中沿学习到的速度场通过ODE求解器演化得到未来潜代码 $\hat{\mathbf{Z}}_1$；最终经可逆解码器重建为未来运动序列。多条预测通过从高斯混合先验的不同分量中采样实现，天然对应不同的行为模式。

### 模块关系与数据流

**模块一：DCT频域预处理与低通滤波**。输入运动序列首先通过离散余弦变换（DCT）投影到频域，并施加低通滤波保留低频分量。这一步在平滑运动的同时实现降维，为后续潜空间建模提供紧凑表示。其变换公式为：

$$\tilde{\mathbf{X}} = \mathrm{DCT}(\mathbf{X}) = D_{L_1} \mathbf{X} G_{L_2}$$

$$\mathbf{X} = \mathrm{iDCT}(\tilde{\mathbf{X}}) = D_{L_1}^T \tilde{\mathbf{X}} G_{L_2}^T$$

其中 $D_{L_1}$ 和 $G_{L_2}$ 分别沿时间维度和通道维度进行压缩。

**模块二：Part-aware流模型**。该模块作为统一的编码器/解码器，利用可逆归一化流将滤波后的运动序列映射到潜空间，并通过其逆过程实现无损重建。与VAE或自编码器不同，流模型的双向可逆性使得单一模型同时承担编码与解码功能，且保持关节语义结构。编码过程将观测序列 $\mathbf{X}$ 映射为潜代码 $\mathbf{Z} = f_{\boldsymbol{\theta}}(\mathbf{X})$，解码过程则为 $\hat{\mathbf{X}} = f_{\boldsymbol{\theta}}^{-1}(\mathbf{Z})$。

**模块三：EM高斯混合潜分布学习**。这是本方法的核心创新。在潜空间中，模型通过无监督EM算法交替优化流模型参数与高斯混合分布参数，学习一个包含 $K$ 个分量的数据驱动先验：

$$q_z(\mathbf{Z}) = \sum_{i=1}^{K} \beta_i \mathcal{N}(\pmb{\mu}_i, \pmb{\sigma}_i)$$

E步计算每个潜代码属于各分量的后验概率：

$$q(i|\mathbf{Z}) = \frac{\beta_i \mathcal{N}(f_{\boldsymbol{\theta}}(\mathbf{X})|\mu_i,\sigma_i)}{\sum_{j=1}^K \beta_j \mathcal{N}(f_{\boldsymbol{\theta}}(\mathbf{X})|\mu_j,\sigma_j)}$$

M步则更新各分量的均值、方差和混合系数。这一过程无需动作标签，即可自然解耦走、跑、坐等不同运动语义。

**模块四：骨架感知Transformer流匹配速度场**。在潜空间中，未来预测被形式化为从源分布 $p_{\mathbf{Z}_0}$ 到目标分布 $p_{\mathbf{Z}_1}$ 的传输问题。模型训练一个速度场 $v_{\theta}$，通过条件流匹配损失拟合直线路径：

$$\mathbb{E}_{\mathbf{Z}_1 \sim p_{\mathrm{data}}, \hat{\mathbf{Z}}_0 \sim p_{\mathbf{Z}_0}, t \sim [0,1]} \| (\mathbf{Z}_1 - \hat{\mathbf{Z}}_0) - v_{\theta}(\mathbf{Z}_t, t) \|_2^2$$

其中 $\mathbf{Z}_t = t\mathbf{Z}_1 + (1-t)\hat{\mathbf{Z}}_0$。速度场 $v_{\theta}$ 由骨架感知Transformer实现，其关键设计在于**关节点级tokenization**——将每个关节的时间轨迹作为独立token，而非传统方法中的姿态级空间tokenization。在此基础上计算关节内缩放点积注意力：

$$\mathrm{Attention}(\mathbf{Q}_i, \mathbf{K}_i, \mathbf{V}_i) = \mathrm{softmax}(\frac{\mathbf{Q}_i^T \mathbf{K}_i}{\sqrt{d_k}}) \mathbf{V}_i$$

该设计显式建模人体骨架的空间依赖关系，同时观测历史作为条件信号融入，强化历史-未来的一致性约束。

**模块五：ODE求解器（推断）**。推断时，从观测序列编码得到的 $\mathbf{Z}_0$ 出发，沿训练好的速度场 $v_{\theta}$ 通过ODE求解器积分演化得到未来潜代码 $\hat{\mathbf{Z}}_1$，再经流模型解码生成最终运动预测。多条随机预测通过从高斯混合先验的不同分量采样 $\hat{\mathbf{Z}}_0$ 实现，每个分量对应一种运动模式，从而产生语义解耦的多样化输出。

### 关键设计决策的因果链路

框架中四个关键设计决策形成清晰的因果链路：**高斯混合先验** → 运动模式解耦 → 预测合理性与不确定性量化；**可逆流骨干** → 精确似然计算 → 原则性不确定性估计；**显式条件建模** → 历史-未来依赖强化 → 准确性提升；**关节点级注意力** → 骨架先验注入 → 姿态合理性。消融实验证实，移除任一组件均导致性能显著下降：当潜先验退化为标准高斯时，准确性与合理性指标全面恶化；使用空间tokenization替代关节点级tokenization后，准确性和合理性均大幅降低；去除观测条件后，多样性与准确性同步下降。

### 补充图表

![[assets/figures/papers/paper_list_l965_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Gaussian_Mixture_La/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the framework. We predict future motion within a latent space constructed by a flow model. Owing to the invertibility of normalizing flows, a single model can function as both an encoder and a decoder through its forward and inverse processes, respectively. During latent forecasting, we first pad the observed sequence to the full length using the final observed frame and transform it into the latent space to obtain the starting point*

## 核心模块与公式推导

### 5.1 高斯混合潜表示

#### 5.1.1 DCT频域预处理

原始运动序列首先通过二维离散余弦变换（2D-DCT）投影到频域，并施加低通滤波以保留低频分量。给定运动序列 $\mathbf{X}$，其DCT变换与逆变换定义为：

$$
\tilde{\mathbf{X}} = \mathrm{DCT}(\mathbf{X}) = D_{L_1} \mathbf{X} G_{L_2}
$$

$$
\mathbf{X} = \mathrm{iDCT}(\tilde{\mathbf{X}}) = D_{L_1}^T \tilde{\mathbf{X}} G_{L_2}^T
$$

其中 $D_{L_1}$ 和 $G_{L_2}$ 分别沿时间维度和通道维度进行压缩。这一预处理步骤在平滑运动的同时降低了后续模块的输入维度。

#### 5.1.2 Part-aware流模型

方法采用Part-aware流模型作为潜空间骨干，该模型利用可逆归一化流将运动序列映射到潜空间。得益于归一化流的可逆性，同一模型可通过正向过程编码、逆向过程解码，无需独立的编码器/解码器对。流模型在编码过程中保留关节语义结构，为后续的骨架感知注意力机制奠定基础。

#### 5.1.3 EM高斯混合先验学习

核心创新在于将潜空间先验从传统的单模态标准高斯分布替换为数据驱动的多模态高斯混合分布。潜变量 $\mathbf{Z}$ 的先验定义为 $K$ 个高斯分量的加权混合：

$$
q_z(\mathbf{Z}) = \sum_{i=1}^{K} \beta_i \mathcal{N}(\pmb{\mu}_i, \pmb{\sigma}_i) \tag{8}
$$

其中 $\beta_i$、$\pmb{\mu}_i$、$\pmb{\sigma}_i$ 分别为第 $i$ 个分量的混合系数、均值和协方差。这些参数与流模型参数 $\boldsymbol{\theta}$ 通过无监督EM算法联合优化，无需动作标签即可自然解耦多样化运动模式。

**E步**计算每个潜变量属于第 $i$ 个高斯分量的后验概率：

$$
q(i|\mathbf{Z}) = \frac{\beta_i \mathcal{N}(f_{\boldsymbol{\theta}}(\mathbf{X})|\mu_i,\sigma_i)}{\sum_{j=1}^K \beta_j \mathcal{N}(f_{\boldsymbol{\theta}}(\mathbf{X})|\mu_j,\sigma_j)}
$$

**M步**基于后验概率更新高斯混合参数和流模型参数。通过交替迭代，潜空间自适应地组织为语义解耦的多模态结构，从根本上缓解了单模态先验导致的语义纠缠问题。

### 5.2 潜流匹配

#### 5.2.1 条件流匹配框架

在潜空间中，未来运动预测被形式化为从源分布到目标分布的传输问题。源分布 $p_{\mathbf{Z}_0}$ 设为以观测历史潜编码 $\mathbf{Z}_0$ 为中心的高斯分布 $\mathcal{N}(\mathbf{Z}_0, \mathbf{I})$，目标分布 $p_{\mathbf{Z}_1}$ 建模为狄拉克分布 $\delta(\mathbf{Z}_1)$。采用条件流匹配框架训练速度场 $v_{\theta}$，目标函数为：

$$
\mathbb{E}_{\mathbf{Z}_1 \sim p_{\mathrm{data}}, \hat{\mathbf{Z}}_0 \sim p_{\mathbf{Z}_0}, t \sim [0,1]} \| (\mathbf{Z}_1 - \hat{\mathbf{Z}}_0) - v_{\theta}(\mathbf{Z}_t, t) \|_2^2 \tag{9}
$$

其中 $\mathbf{Z}_t = t\mathbf{Z}_1 + (1-t)\hat{\mathbf{Z}}_0$ 为直线插值路径上的中间状态。该损失训练速度场拟合从源到目标的直线传输方向，相较于基于SDE的扩散模型训练，ODE框架更高效且支持精确似然计算。

#### 5.2.2 骨架感知Transformer速度场

速度场 $v_{\theta}$ 由骨架感知Transformer实现。与传统姿态级tokenization不同，本方法对单个关节的时间轨迹进行tokenization，使注意力机制在关节维度上计算。给定第 $i$ 个关节的查询、键、值向量 $\mathbf{Q}_i, \mathbf{K}_i, \mathbf{V}_i$，关节内注意力定义为：

$$
\mathrm{Attention}(\mathbf{Q}_i, \mathbf{K}_i, \mathbf{V}_i) = \mathrm{softmax}\left(\frac{\mathbf{Q}_i^T \mathbf{K}_i}{\sqrt{d_k}}\right) \mathbf{V}_i \tag{10}
$$

该设计显式建模人体骨架的空间依赖性，将骨架结构先验融入速度场学习。消融实验证实，关节级tokenization相比空间tokenization在准确性和合理性指标上均有显著提升。

### 5.3 推断与不确定性估计

#### 5.3.1 ODE推断

推断阶段，从观测序列编码得到初始潜状态 $\mathbf{Z}_0$，通过ODE求解器沿学习到的速度场积分演化至 $\hat{\mathbf{Z}}_1$：

$$
\hat{\mathbf{Z}}_1 = \mathbf{Z}_0 + \int_0^1 v_{\theta}(\mathbf{Z}_t, t) \mathrm{d}t
$$

随后通过流模型的逆过程将 $\hat{\mathbf{Z}}_1$ 解码为未来运动序列。多次采样源分布 $p_{\mathbf{Z}_0}$ 可生成多样化的预测结果。

#### 5.3.2 精确似然计算

得益于归一化流的可逆性和ODE框架的连续性，模型支持精确的对数似然计算。潜变量 $\hat{\mathbf{Z}}_1$ 的对数似然通过瞬时变量替换公式沿轨迹积分得到：

$$
\log p(\hat{\mathbf{Z}}_1) = \log p(\hat{\mathbf{Z}}_0) + \int_0^1 -\mathrm{tr}(\boldsymbol{\nabla}_{\mathbf{Z}_t} v_{\theta}(\mathbf{Z}_t, t)) \mathrm{d}t
$$

进一步结合流模型的变量替换和混合高斯先验 $q_z(\mathbf{Z})$，可计算观测运动 $\hat{\mathbf{X}}$ 的完整似然。实验表明，高斯混合先验在Human3.6M和AMASS数据集上均取得最优对数似然，证明了其对复杂运动分布建模的优越性。

### 补充图表

![[assets/figures/papers/paper_list_l965_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Gaussian_Mixture_La/figures/001_Figure_1.jpg]]
*Figure 1: Unlike prior approaches, our method (1) introduces a mixed Gaussian prior to effectively disentangle diverse human motion patterns, improving plausibility by reducing semantic entanglement, and (2) incorporates a fully invertible architecture that supports exact likelihood computation, thereby providing a principled means of uncertainty estimation*

## 实验与分析

### 主实验结果

我们在Human3.6M与AMASS两个基准数据集上进行了系统评估，采用Best-of-50协议与现有随机人体运动预测方法进行全面比较。**表1**展示了核心定量结果。

在Human3.6M数据集上，本方法在FDE指标上达到0.399，相较先前最优方法降低8.5%；ADE达到0.333，取得最优水平。在MMADE（0.471）与MMFDE（0.464）上，本方法稳定排名前三。在AMASS数据集上，优势更为显著：FDE达到0.474，相较先前最优降低13%；ADE达到0.461，同样取得最优；MMADE（0.540）排名最优，MMFDE（0.509）排名前三。由于AMASS缺乏动作类别标签，该数据集不评估FID指标。

这些结果表明，数据驱动的高斯混合潜空间先验配合可逆流模型骨干，在预测准确性与物理合理性两个维度上均实现了对现有方法的系统性超越。

### 消融实验分析

为验证各组件的独立贡献，我们设计了系统的消融实验（**表2**），从潜空间构造与潜动力学建模两个层面进行解耦分析。

**潜空间先验的影响。** 将可学习的高斯混合先验替换为固定混合分布后，多数指标出现性能退化；进一步替换为标准高斯先验或完全移除先验，性能退化更为严重。这验证了数据驱动的多模态先验对建模多样化运动模式的关键作用。

**条件机制的必要性。** 移除观测历史条件信号（w/o Condition）后，模型在多样性与准确性上均显著下降。这表明将历史显式作为条件融入潜变量演化，比仅将其视为重建目标能提供更有效的引导。

**Tokenization策略的影响。** 将关节点级tokenization替换为传统的空间（姿态级）tokenization后，准确性与合理性指标大幅退化，退化幅度甚至超过移除显式条件的配置。这验证了骨架感知的关节点内注意力机制对捕捉人体运动空间依赖结构的关键价值。

**对数似然评估。** **表3**展示了不同潜先验配置下的对数似然（LL）对比。本方法采用高斯混合先验在两个数据集上均取得最佳LL，证明其对复杂运动分布具有最强的建模能力。值得注意的是，完全无先验的纯流匹配变体，其LL甚至优于使用标准高斯先验的配置——这揭示了过于简单的先验分布反而会损害模型对真实数据分布的拟合能力。

### 失败模式与局限性

尽管本方法在整体指标上表现优异，分析揭示了若干值得关注的失败模式：

**硬分配导致的重采样问题。** EM算法中E步采用硬分配策略确定潜变量归属的高斯分量。当两个语义相似的运动片段被分配到不同分量时，在重采样阶段可能产生不一致的预测结果，影响生成样本的稳定性。论文指出需要额外的约束机制来缓解这一问题，但具体方案仍有待探索。

**混合分量数的敏感性。** 高斯混合分量数K需预先设定，且EM算法可能收敛到局部最优。对于训练数据中的长尾分布模式，混合分布可能退化为单一模式，丧失多模态建模的优势。如何自适应确定分量数或引入防止退化的正则化，是尚未解决的开放问题。

**模式外推的局限。** 模型训练建立在“未来运动模式与观测历史一致”的假设之上。当测试场景中出现突发性运动模式改变（如从行走突然转为跳跃），模型无法有效捕获这种分布外变化，预测将回归到训练分布的主流模式，导致多样性不足。

### 定性分析

**图3**展示了AMASS数据集上各方法的定性对比。对于每个测试序列，我们可视化10个随机采样预测的最后一帧姿态。本方法生成的预测姿态展现出更高的自然度与物理合理性，能够更好地保持与观测历史语义的一致性。相比之下，基于扩散的基线方法（SkeletonDiff、CoMusion、TransFusion）在部分样本上出现肢体穿透、关节扭曲等物理不合理现象，而BeLFusion的预测多样性虽高但姿态质量波动较大。

### 补充图表

![[assets/figures/papers/paper_list_l965_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Gaussian_Mixture_La/figures/003_Table_1.jpg]]
*Table 1: Quantitative results compared to stochastic baselines adopting Best-of-50 metrics on the Human3.6M and AMASS datasets. As AMASS does not include action labels, FID is not used for evaluation. The best results are highlighted in bold, second best are underlined*

![[assets/figures/papers/paper_list_l965_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Gaussian_Mixture_La/figures/005_Table_2.jpg]]
*Table 2: The results of ablation studies on the Human3.6M and AMASS datasets. Since AMASS does not include action labels, FID is not used for evaluation. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l965_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Gaussian_Mixture_La/figures/006_Table_3.jpg]]
*Table 3: The results of log-likelihood↑ on the Human3.6M and AMASS datasets*

![[assets/figures/papers/paper_list_l965_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Gaussian_Mixture_La/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative results. We present qualitative comparison results with SkeletonDiff [15], CoMusion [63], TransFusion [66], and BeLFusion [3] on the AMASS dataset. For each method, we visualize the final frame of 10 randomly sampled predictions*

## 方法谱系与知识库定位

### 1. 与现有随机人体运动预测方法的关系

本工作处于**随机3D人体运动预测**这一研究方向，其核心贡献在于对潜空间先验分布与生成模型骨干的重新设计，从而系统性地解决了现有方法中“多模态运动语义纠缠”与“不确定性量化缺失”两大瓶颈。

**相对于基于VAE的方法**：早期随机预测方法如**DLow**（Yuan & Kitani, ECCV 2020）采用条件VAE框架，通过在潜空间中学习多样化采样策略来生成多种可能的未来运动。然而，VAE的标准高斯先验本质上是单模态的，无法有效解耦不同运动行为模式。本工作将VAE的潜空间替换为**可逆Part-aware流模型**，并将单模态先验替换为**数据驱动的高斯混合先验**，从根本上改变了潜空间的几何结构，使得不同运动模式自然分离。

**相对于基于扩散模型的方法**：近年来，扩散模型在运动预测领域取得了显著进展，代表性工作包括**BeLFusion**（Barquero et al., CVPR 2024）在行为空间中进行潜在扩散、**SkeletonDiff**（Chen et al., CVPR 2024）直接在关节空间扩散、**CoMusion**（Li et al., ECCV 2024）专注于一致性随机预测、以及**TransFusion**（Xu et al., CVPR 2025）结合Transformer架构。这些方法普遍依赖基于SDE的扩散过程，虽然能够生成多样化样本，但缺乏精确的似然计算能力，难以进行原则性的不确定性估计。本工作采用**基于ODE的流匹配框架**替代SDE，在保持生成多样性的同时，借助连续归一化流的即时变量替换公式实现了精确的对数似然计算，为不确定性量化提供了理论保障。

**相对于基于SO(3)结构的方法**：**Motron**（Salzmann et al., CVPR 2023）通过在SO(3)流形上建模概率输出来保证预测的物理合理性。本工作虽然未显式建模旋转流形约束，但通过**关节点级tokenization与骨架感知注意力**机制，在Transformer架构中隐式编码了人体运动学先验，从另一条路径提升了预测的物理合理性。

### 2. 适用边界

本方法的设计假设决定了其适用场景与限制：

- **历史依赖性假设**：模型假设未来运动模式与观测历史中的运动模式一致，通过将观测序列作为显式条件信号来引导潜变量的演化。这一假设适用于常规的运动预测场景（如行走、跑步等周期性或准周期性运动），但在面对突发性运动模式改变时可能失效。
- **混合分量数K的预定义**：高斯混合先验的分量数K需要预先指定，这要求对数据集的运动模式多样性有一定先验知识。EM算法的收敛性质意味着不同初始化可能导致不同的局部最优解，对长尾分布数据的建模可能退化。
- **硬分配策略的局限**：EM算法中每个潜变量被硬分配到某个高斯分量，这可能导致“重采样问题”——语义相似的运动因分配不一致而产生预测分歧。这是混合模型固有的离散潜变量设计带来的结构性问题。

### 3. 局限与开放问题

**已识别的局限**：

1. **重采样问题**：硬分配策略缺乏对分配一致性的显式约束，可能导致语义相似的运动序列被分配到不同分量，影响预测的稳定性。论文指出需要额外约束机制来缓解这一问题，但尚未给出具体方案。
2. **分量数K的敏感性**：K的选择直接影响潜空间的语义解耦程度与生成质量。K过小则解耦不充分，K过大则可能导致过拟合或训练不稳定。论文未系统性地探索K的选择策略。
3. **模式突变盲区**：模型假设未来运动模式可从历史中推断，无法处理运动模式的突然改变（如从走路突然变为跳跃）。这是当前多数运动预测方法的共性局限。

**开放问题**：

1. **语义边界与连续性的平衡**：如何构建一个既有清晰语义边界便于分类、又有足够连续性便于生成的潜空间？高斯混合模型在离散分量之间天然存在边界，但运动模式之间的过渡往往是连续的。这是一个根本性的表示学习问题。
2. **长尾分布建模**：如何处理长尾分布数据，防止潜空间混合分布退化为单一模式？当某些运动模式样本极少时，对应的混合分量可能被主模式“吸收”，导致多样性丧失。
3. **超出历史的模式预测**：如何捕获未来运动模式与历史不一致的变化，实现超出历史模式的多模态预测？这可能需要引入外部知识或因果推理机制。
4. **分配一致性的系统化解决**：对分配过程施加何种额外约束（如对比学习、一致性正则化）能够系统性地解决重采样问题，是一个值得深入探索的方向。

### 4. 知识库定位

本工作在随机人体运动预测的知识体系中占据**潜空间先验设计**这一关键节点，其核心洞察——“多模态先验解耦运动语义”与“可逆架构使能精确不确定性”——具有跨任务的迁移潜力：

- **向其他序列预测任务的迁移**：任何面临多模态输出分布建模的序列预测任务（如轨迹预测、手势生成）都可能受益于数据驱动的混合先验设计。
- **与可控生成的结合**：高斯混合分量的语义解耦特性天然适合作为可控生成的条件接口——不同分量可对应不同的运动风格或动作类别，为细粒度控制提供了结构化基础。
- **不确定性量化的基准**：本工作建立的对数似然评估框架为随机预测方法的不确定性量化能力提供了可比较的度量标准，推动了该领域从“生成多样性”向“概率校准”的范式演进。

## 原文 PDF

![[paperPDFs/CVPR_2026/Gaussian_Mixture_Latent_Flow_for_Stochastic_3D_Human_Motion_Prediction.pdf]]