---
title: Evidential Neural Radiance Fields
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Evidential_Neural_Radiance_Fields.pdf
project_link: null
code_link: "https://github.com/KerryDRX/EvidentialNeRF"
aliases:
- ENRFEN
- ENRF
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 将像素辐射的均值与方差视为随机变量，并由高阶证据分布（NIG）统治，使得NeRF可直接预测并传播偶然和认知不确定性，从而无需回归证据参数。
primary_logic: 通过在点级别直接输出偶然不确定性、认知不确定性与形状得分，并利用渲染权重的平方将两者从点级别加和传播至像素级别，Evidential NeRF将证据学习无缝嵌入体积渲染，同时保持了计算效率与渲染质量。
claims:
- Evidential NeRF在三个标准化基准上实现了最先进的场景重建保真度和不确定性估计质量
- 在所有图像重建和不确定性量化指标中，该方法始终位于前三，且多次排名第一
- 像素级别的不确定性可通过点级别不确定性的加权和（权重为渲染权重的平方）精确计算
- 随着训练数据增加，测试AU上升而测试EU下降，验证了两种不确定性对数据量的不同响应
---

# Evidential Neural Radiance Fields

> [!tip] 核心洞察
> 通过在点级别直接输出偶然不确定性、认知不确定性与形状得分，并利用渲染权重的平方将两者从点级别加和传播至像素级别，Evidential NeRF将证据学习无缝嵌入体积渲染，同时保持了计算效率与渲染质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 证据增强的神经辐射场 |
| 英文题名 | Evidential Neural Radiance Fields |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23574) · [Code](https://github.com/KerryDRX/EvidentialNeRF) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Evidential Neural Radiance Fields (Evidential NeRF) |
| Dataset | LF, LLFF, RobustNeRF, Speed |

> [!tip] 效果简介
> - LF 上，PSNR↑ 29.9679 vs 29.3779 (Ensembles) (+0.5900)；LPIPS↓ 0.0359 vs 0.0411 (Ensembles) (-0.0052)。
> - LLFF 上，NLL↓ 0.6765 vs 9.7273 (DANE) (-9.0508)。
> - RobustNeRF 上，PSNR↑ 26.2292 vs 26.1953 (Ensembles) (+0.0339)。

## 概要

三维场景重建的核心挑战之一，不仅在于渲染出高保真的图像，更在于让模型“知道自己的无知”：哪些区域的误差源于观测数据本身的噪声（偶然不确定性），哪些区域则是模型因训练视角不足而缺乏知识（认知不确定性）。现有神经辐射场（NeRF）的不确定性量化方法——从蒙特卡洛Dropout、深度集成到闭式似然模型——普遍存在一个根本性瓶颈：**难以在单次前向传播中同时分离两类不确定性，且常以牺牲渲染质量或大幅增加计算开销为代价**。例如，朴素集成方法需训练多个独立模型，推理速度显著下降；而基于正态分布的似然模型仅能捕获偶然不确定性，对认知不确定性无能为力。

针对这一瓶颈，本文提出**Evidential Neural Radiance Fields (Evidential NeRF)**，其核心因果机制在于将概率建模提升至高阶层次：**不再将像素辐射的均值与方差视为确定性的点估计，而是将其视为由Normal-Inverse-Gamma (NIG) 证据分布统治的随机变量**。这一范式转换使模型能够直接在点级别输出偶然不确定性、认知不确定性与形状得分，并利用渲染权重的平方将两者从点级别加和传播至像素级别，从而将证据学习无缝嵌入体积渲染管线，无需回归证据参数，保持了计算效率与渲染质量。

方法的关键洞察可概括为一条简洁的传播规则：像素级偶然不确定性 $U^{\mathrm{alea}} = \sum_{i=1}^N w_i^2 U_i^{\mathrm{alea}}$，认知不确定性 $U^{\mathrm{epis}} = \sum_{i=1}^N w_i^2 U_i^{\mathrm{epis}}$。在NIG先验下，像素颜色的边际分布退化为Student-t分布，模型通过最大化该边际似然并结合证据正则项进行训练，正则项惩罚高置信度下的预测误差，从而抑制错误预测的过度自信。

实验证据表明，Evidential NeRF在三个标准化基准（LF、LLFF、RobustNeRF）上实现了最先进的场景重建保真度和不确定性估计质量，在所有图像重建和不确定性量化指标中始终位于前三，且多次排名第一。具体而言，在LF数据集上，PSNR达到29.97 dB，较集成方法提升0.59 dB；在LLFF上，NLL降至0.6765，较DANE降低9.05。在推理速度上，该方法仅比最快方法慢0.04 FPS（4.67 vs. 4.71），却显著优于集成方法。消融实验进一步验证了两种不确定性对数据量的差异化响应——随训练样本增加，测试偶然不确定性上升而认知不确定性下降——以及基于认知不确定性的主动学习、基于偶然不确定性的漂浮物移除等下游应用的有效性。

在方法谱系上，Evidential NeRF建立在nerfacto骨干网络之上，与**Dropout**（贝叶斯MC dropout）、**Normal**（闭式正态似然）、**MoL**（Laplace混合似然）、**Ensembles**（朴素深度集成）及**DANE**（密度感知集成）等基线方法形成系统对比。其核心改动仅在于输出层增加三个神经元以预测点级不确定性，并将损失函数从正态负对数似然替换为Student-t边际似然加证据正则项，体现了“最小改动、最大增益”的设计哲学。

该工作仍存在若干局限：当前框架仅对辐射度进行不确定性建模，尚未捕获场景几何（深度、密度）的不确定性；推导依赖沿射线点颜色独立的假设；正则化系数需针对不同场景手动调节。这些开放问题指向了未来将证据框架拓展至3D高斯泼溅、显式建模点间依赖关系、以及纳入几何不确定性的研究方向。

神经辐射场（NeRF）已成为三维场景重建与新颖视图合成的核心范式。其基本流水线为：从相机射线采样空间点，由神经网络预测点的颜色与密度，再通过体积渲染合成像素颜色。然而，标准NeRF仅输出确定性预测，无法提供预测的可信度度量。在现实应用中——如机器人导航、自动驾驶和医疗影像——缺乏不确定性估计可能导致模型在未知或高噪声区域做出过度自信的错误预测，带来严重安全风险。

不确定性通常被分解为两类：**偶然不确定性**（aleatoric uncertainty）源于数据本身的固有噪声（如光照变化、瞬态遮挡物、镜面反射），即使增加数据也无法消除；**认知不确定性**（epistemic uncertainty）则反映模型知识的不足（如训练视角未覆盖的区域），理论上可通过增加训练数据来降低。有效分离并量化这两类不确定性，对于下游任务（如主动学习、分布外检测、场景清洁）具有关键价值。

现有NeRF不确定性量化方法可大致归为三类。**贝叶斯方法**（如Monte Carlo dropout、深度集成）通过对网络权重进行多次采样来估计认知不确定性，但计算开销大、推理速度慢，且难以显式分离两类不确定性。**闭式似然方法**（如Normal NeRF、MoL NeRF）直接预测像素颜色的概率分布参数，仅能捕获偶然不确定性，缺乏对模型知识状态的建模。**混合方法**（如DANE）在集成框架中引入密度感知机制，但仍未实现单一前向传播下的两类不确定性分离。总体而言，现有方法面临一个核心瓶颈：**难以在保持渲染质量与计算效率的前提下，同时分离并量化偶然与认知不确定性**。

Evidential NeRF的提出正是为了填补这一空白。其核心动机是：将证据深度学习（evidential deep learning）的思想引入NeRF的概率建模框架，使网络能够在一个前向传播中直接输出两类不确定性，而无需采样、集成或额外的证据回归头。这一设计旨在实现三个目标：（1）保持与基础NeRF相当的计算效率；（2）提供可解释的、分离的偶然与认知不确定性图；（3）不牺牲场景重建的保真度。

## 核心方法与创新机理

Evidential NeRF 的核心创新在于将证据深度学习范式无缝嵌入神经辐射场的体积渲染管线，构建了一个能够**同时且高效地分离偶然不确定性（aleatoric uncertainty, AU）与认知不确定性（epistemic uncertainty, EU）** 的概率框架。与现有方法相比，其关键突破体现在以下三个维度的结构性改变上。

### 1. 从“预测不确定性参数”到“直接预测不确定性”的范式转换

传统概率NeRF（如Normal NeRF）将点颜色建模为以预测均值与方差为参数的正态分布，其方差仅能捕获偶然不确定性。Evidential NeRF 在此基础上引入更高阶的证据分布——Normal-Inverse-Gamma（NIG）先验，将像素辐射的均值与方差本身视为随机变量。这一理论跃迁的工程实现极为简洁：**模型输出层仅新增三个神经元**，直接预测每点的偶然不确定性 $U_i^{\mathrm{alea}}$、认知不确定性 $U_i^{\mathrm{epis}}$ 和形状得分 $\tilde{\alpha}_i$（见Eq. 9），而非回归证据分布的参数。这避免了在训练中显式拟合复杂的NIG参数，使得模型架构几乎与基础NeRF保持一致，却获得了分离两类不确定性的能力。

### 2. 点级不确定性向像素级的精确传播机制

在点颜色独立的假设下，Evidential NeRF 推导出像素级两类不确定性可由点级不确定性通过渲染权重的平方加权求和得到：

$$U^{\mathrm{alea}} = \sum_{i=1}^N w_i^2 U_i^{\mathrm{alea}}, \quad U^{\mathrm{epis}} = \sum_{i=1}^N w_i^2 U_i^{\mathrm{epis}}$$

这一传播规则（Eq. 12-13）具有严格的概率基础：像素颜色的条件方差在点独立性假设下恰好分解为点级条件方差的平方加权和。该设计使得不确定性可以像颜色一样在体积渲染中自然累积，无需额外的前向或反向传播，也无需维护多个模型副本（如深度集成方法）。

### 3. 基于Student-t边际似然的统一训练目标

在NIG先验下，像素颜色的边际分布退化为Student-t分布（Eq. 21），其负对数似然 $\mathcal{L}_{\mathrm{nll}}$ 天然地同时驱动均值预测精度与不确定性校准。为抑制错误预测的高置信度，方法引入证据正则项 $\mathcal{L}_{\mathrm{reg}} = |c^{\mathrm{gt}} - \gamma| (2\nu + \alpha)$，该正则项以预测误差乘以虚拟观测数（$2\nu + \alpha$）的形式惩罚过于自信的预测。完整的训练损失为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{nll}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}$$

这一损失函数将渲染质量优化与不确定性量化统一在单阶段训练中，无需像集成方法那样进行多次独立训练，也无需像Dropout方法那样在推理时执行多次随机前向传播。

### 与基线方法的关键差异总结

| 改变维度 | 基线方法（Normal NeRF） | Evidential NeRF |
|---------|----------------------|-----------------|
| **输出层** | 仅预测点颜色均值、方差与密度 | 额外输出每点的 $U_i^{\mathrm{alea}}$、$U_i^{\mathrm{epis}}$、$\tilde{\alpha}_i$ |
| **概率建模层次** | 点估计的均值与方差（仅捕获AU） | 均值与方差为随机变量，由NIG分布控制（同时捕获AU与EU） |
| **损失函数** | 基于正态分布的负对数似然 | 基于Student-t边际分布的负对数似然 + 证据正则项 |
| **不确定性分离** | 无法分离 | 在单次前向传播中同时输出AU与EU |
| **计算开销** | 基准水平 | 推理速度仅比最快方法慢0.04 FPS，显著优于集成方法 |

这些创新使得Evidential NeRF在保持计算效率与渲染质量的同时，首次实现了对NeRF场景重建中两类不确定性的精确、高效分离，为后续的不确定性感知应用（如主动学习、场景清洁）提供了统一的概率基础。

Evidential NeRF 构建了一个三级概率化范式，将证据学习无缝嵌入神经辐射场的体积渲染管线。其核心流程可概括为四个串联模块：**点级证据预测 → 点-像素不确定性传播 → 像素级 NIG 参数重构 → Student-t 边际似然训练**。

### 概率化层次演进

Figure 2 展示了 NeRF 流水线从确定性到完全证据化的三级跃迁：

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/002_Figure_2.jpg]]
*Figure 2: Evolution of NeRF pipeline across three levels of probabilistic formulations. N points sampled along the camera ray give N pairs of spatial location and viewing direction, which are passed to the NeRF model for prediction. Level 1: Vanilla NeRF predicts only point density and color, resulting in a deterministic pixel color without any uncertainty estimate. Level 2: Normal NeRF assumes the point and pixel colors follow normal distributions, quantifying aleatoric uncertainty of rendered color. Level 3: Evidential NeRF assumes the pixel color has random mean and variance following an evidential distribution, quantifying both aleatoric and epistemic uncertainties*

- **Level 1 (Vanilla NeRF)**：沿射线采样点仅输出颜色与密度，经体积渲染得到确定性像素颜色，不提供任何不确定性度量。
- **Level 2 (Normal NeRF)**：将点颜色建模为正态分布 $c_i \mid \mu_i, \sigma_i^2 \sim \mathcal{N}(\mu_i, \sigma_i^2)$，在点独立假设下像素颜色亦服从正态分布，其方差仅捕获偶然不确定性——即数据本身的固有噪声，但无法区分模型知识不足导致的认知不确定性。
- **Level 3 (Evidential NeRF)**：将像素颜色的均值与方差本身视为随机变量，由高阶 Normal-Inverse-Gamma (NIG) 证据分布统治。这使得模型能够在单次前向传播中同时输出两类不确定性，且无需回归证据参数。

### 模块化管线

**模块一：点级证据 NeRF 预测**

Evidential NeRF 在骨干网络（nerfacto）的最后一层增加三个输出神经元，使模型直接预测每个采样点的五元组：

$$(\bar{c}_i, U_i^{\mathrm{alea}}, U_i^{\mathrm{epis}}, \tilde{\alpha}_i), \rho_i = f(\mathbf{x}_i, \mathbf{d})$$

其中 $\bar{c}_i$ 为点颜色预测均值，$U_i^{\mathrm{alea}}$ 为偶然不确定性（期望条件方差），$U_i^{\mathrm{epis}}$ 为认知不确定性，$\tilde{\alpha}_i$ 为正值形状得分，$\rho_i$ 为密度。网络其余结构保持不变，保证了计算效率。

**模块二：点级向像素级不确定性传播**

在沿射线采样点独立的假设下，像素级颜色与不确定性通过渲染权重的平方加权求和得到：

$$\bar{c} = \sum_{i=1}^N w_i \bar{c}_i,\quad U^{\mathrm{alea}} = \sum_{i=1}^N w_i^2 U_i^{\mathrm{alea}},\quad U^{\mathrm{epis}} = \sum_{i=1}^N w_i^2 U_i^{\mathrm{epis}}$$

这一传播机制的因果关键在于：偶然不确定性（数据噪声）与认知不确定性（模型知识不足）在点级别被独立预测，并通过渲染权重 $w_i$ 的平方从点级加和传播至像素级，使得两类不确定性在像素空间保持可分离性。

**模块三：像素级 NIG 参数重构**

传播后的不确定性与形状得分被逆推为 NIG 分布的四个参数：

$$\gamma = \bar{c},\quad \nu = \frac{U^{\mathrm{alea}}}{U^{\mathrm{epis}}},\quad \alpha = 1 + \sum_{i=1}^N \tilde{w}_i \tilde{\alpha}_i,\quad \beta = U^{\mathrm{alea}} (\alpha - 1)$$

其中 $\gamma$ 为位置参数（预测颜色），$\nu$ 为偶然与认知不确定性之比（衡量相对置信度），$\alpha$ 为形状参数（由点级形状得分聚合的虚拟观测数），$\beta$ 为尺度参数。在此参数化下，两类不确定性可闭合表达为 $U^{\mathrm{alea}} = \beta/(\alpha-1)$ 和 $U^{\mathrm{epis}} = \beta/((\alpha-1)\nu)$。

**模块四：Student-t 边际似然训练**

在 NIG 先验下，像素颜色的边缘分布退化为 Student-t 分布：

$$c \sim t\left( \gamma, \frac{\beta (\nu+1)}{\alpha \nu}, 2\alpha \right)$$

模型通过最小化负对数似然训练，并辅以证据正则项 $\lambda_{\mathrm{reg}} |c^{\mathrm{gt}} - \gamma| (2\nu + \alpha)$，惩罚预测误差与虚拟观测数的乘积，抑制错误预测的高置信度。正则化系数 $\lambda_{\mathrm{reg}}$ 需针对不同场景手动调节（见 Table 3），这是当前方法的一个实践瓶颈。

### 输入输出流总结

整个管线以相机射线上的采样点 $(\mathbf{x}_i, \mathbf{d})$ 为输入，经单次前向传播输出像素颜色 $\bar{c}$、偶然不确定性 $U^{\mathrm{alea}}$ 和认知不确定性 $U^{\mathrm{epis}}$。与集成方法（需多次推理）相比，Evidential NeRF 的推理速度仅比最快方法慢 0.04 FPS（4.67 vs 4.71），同时显著优于所有集成基线（Table 2）。

### 概率化层次演进

Evidential NeRF 的核心创新在于将 NeRF 的概率建模提升至第三层次。如 Figure 2 所示，传统 NeRF（Level 1）仅输出确定性的点颜色与密度，无法提供任何不确定性估计。Normal NeRF（Level 2）将点颜色建模为正态分布 $c_i \mid \mu_i, \sigma_i^2 \sim \mathcal{N}(\mu_i, \sigma_i^2)$，在点独立性假设下，像素颜色也服从正态分布：

$$c \mid \mu, \sigma^2 \sim \mathcal{N}(\mu, \sigma^2),\quad \mu = \sum w_i \mu_i,\quad \sigma^2 = \sum w_i^2 \sigma_i^2$$

然而，该层次仅捕获偶然不确定性（aleatoric uncertainty），无法分离认知不确定性（epistemic uncertainty）。

Evidential NeRF（Level 3）将像素颜色的条件均值 $\mu$ 与方差 $\sigma^2$ 本身视为随机变量，由高阶证据分布——Normal-Inverse-Gamma（NIG）分布——统治：

$$\mu, \sigma^2 \sim \mathrm{NIG}(\gamma, \nu, \alpha, \beta)$$

这一建模选择使得模型能够通过单次前向传播同时量化两类不确定性。

---

### 点级证据预测模块

Evidential NeRF 对骨干网络的改动极小：仅在最后一层增加三个输出神经元，直接预测每点的偶然不确定性 $U_i^{\mathrm{alea}}$、认知不确定性 $U_i^{\mathrm{epis}}$ 和形状得分 $\tilde{\alpha}_i$，同时保留密度 $\rho_i$ 与均值颜色 $\bar{c}_i$ 的输出：

$$(\bar{c}_i, U_i^{\mathrm{alea}}, U_i^{\mathrm{epis}}, \tilde{\alpha}_i), \rho_i = f(\mathbf{x}_i, \mathbf{d})$$

其中：
- $\bar{c}_i := \mathbb{E}[c_i] = \mathbb{E}[\mu_i]$：点颜色的预测均值
- $U_i^{\mathrm{alea}} := \mathbb{E}[\sigma_i^2]$：点颜色的期望条件方差，即偶然不确定性
- $U_i^{\mathrm{epis}}$：点级别的认知不确定性，反映模型对点颜色均值 $\mu_i$ 的知识不足
- $\tilde{\alpha}_i > 0$：形状得分，编码该点对 NIG 先验中虚拟观测数量的贡献

这一设计的关键在于：模型无需回归 NIG 参数本身，而是直接输出物理意义明确的不确定性量，随后通过传播与重构间接获得完整的证据分布参数。

---

### 点级到像素级的不确定性传播模块

在点颜色条件独立的假设下，像素级不确定性可通过渲染权重的平方将点级量加权求和得到：

$$\bar{c} = \sum_{i=1}^N w_i \bar{c}_i$$

$$U^{\mathrm{alea}} = \sum_{i=1}^N w_i^2 U_i^{\mathrm{alea}}, \quad U^{\mathrm{epis}} = \sum_{i=1}^N w_i^2 U_i^{\mathrm{epis}}$$

其中 $w_i$ 为标准的体积渲染权重。**权重取平方**的原因在于：方差传播遵循二次形式，而非线性加权。这一传播规则使得偶然不确定性与认知不确定性在像素级别保持可分离性，是 Evidential NeRF 将证据学习无缝嵌入体积渲染管线的核心机制。

---

### NIG 参数重构模块

传播后的像素级不确定性 $U^{\mathrm{alea}}$、$U^{\mathrm{epis}}$ 以及聚合的形状得分需转化为 NIG 分布的四个参数，以闭合形式表达两类不确定性。重构规则为：

$$\gamma = \bar{c}, \quad \nu = \frac{U^{\mathrm{alea}}}{U^{\mathrm{epis}}}$$

$$\alpha = 1 + \sum_{i=1}^N \tilde{w}_i \tilde{\alpha}_i, \quad \beta = U^{\mathrm{alea}} (\alpha - 1)$$

各参数含义：
- $\gamma$：NIG 的位置参数，即像素颜色均值的预测值
- $\nu$：控制认知不确定性与偶然不确定性的相对比例——$\nu$ 越大，认知不确定性越小
- $\alpha$：形状参数，由点级形状得分加权求和后加 1 得到，编码虚拟观测数量
- $\beta$：尺度参数，由偶然不确定性与 $\alpha$ 共同决定

在 NIG 参数化下，两类不确定性具有简洁的闭合形式：

$$U^{\mathrm{alea}} = \frac{\beta}{\alpha - 1}, \quad U^{\mathrm{epis}} = \frac{\beta}{(\alpha - 1) \nu}$$

---

### Student-t 边际似然与训练损失

在 NIG 先验下，像素颜色的边缘分布退化为 Student's t 分布：

$$c \sim t\left( \gamma, \frac{\beta (\nu + 1)}{\alpha \nu}, 2\alpha \right)$$

其中 $\gamma$ 为位置参数，$\frac{\beta (\nu + 1)}{\alpha \nu}$ 为尺度参数，$2\alpha$ 为自由度。模型通过最大化该边际似然进行训练，损失函数由负对数似然与证据正则项组成：

$$\mathcal{L} = -\log p(c^{\mathrm{gt}} \mid \gamma, \nu, \alpha, \beta) + \lambda_{\mathrm{reg}} |c^{\mathrm{gt}} - \gamma| (2\nu + \alpha)$$

正则项 $|c^{\mathrm{gt}} - \gamma| (2\nu + \alpha)$ 的核心作用：当预测误差较大时，惩罚项增大，迫使模型降低虚拟观测数 $(2\nu + \alpha)$，从而抑制错误预测的高置信度。正则化系数 $\lambda_{\mathrm{reg}}$ 需要针对不同场景手动调节（见 Table 3），这是当前方法的一个已知局限。

## 实验与关键发现

### 实验设置与公平性保障

所有对比方法均采用相同的 **nerfacto** 骨干网络，在统一的场景级数据划分、批大小、优化器与学习率调度下训练，并基于各场景收敛速度确定相同的迭代次数。这一设计将不确定性量化（UQ）方法本身的影响与骨干网络、训练策略等因素隔离开来，确保对比的公平性。

### 主实验结果

**Table 1** 汇总了在 LF、LLFF 和 RobustNeRF 三个标准化基准上的场景重建与不确定性量化指标（三次独立运行均值）。Evidential NeRF 在所有图像重建和不确定性量化指标中始终位于前三，且多次排名第一。

在 **LF** 数据集上，该方法取得最佳 PSNR（29.9679）和 LPIPS（0.0359），分别超越集成方法 **Ensembles** 0.59 dB 和 0.0052。在 **LLFF** 数据集上，NLL 指标达到 0.6765，较 **DANE** 的 9.7273 降低逾 9 个单位，表明其概率校准质量显著优于密度感知集成方法。在 **RobustNeRF** 数据集上，PSNR 为 26.2292，略优于 Ensembles（+0.0339），LPIPS 下降 0.0326 至 0.1112。

值得注意的是，Evidential NeRF 在 9 项指标中有 7 项超越计算开销高昂的集成方法，且始终显著优于 Baseline（无 UQ 的 nerfacto）、Dropout、Normal 和 MoL 等闭式似然方法。

**Table 2** 展示了训练时间与推理速度。Evidential NeRF 的单次 30k 步训练耗时约 13.57 分钟，推理速度为 4.67 FPS（A6000 GPU），仅比最快的 Normal 方法慢 0.04 FPS，却大幅领先所有集成方法（如 Ensembles 仅 1.48 FPS）。这验证了该方法在保持高效推理的同时实现 SOTA 不确定性量化质量的核心主张。

**Figure 3** 的定性对比进一步印证了定量结果：Evidential NeRF 的重建误差图与总不确定性图之间的一致性明显优于对比方法，尤其在边缘、高光及遮挡区域表现出更强的误差-不确定性相关性。

### 不确定性分解与行为验证

**Figure 4** 展示了测试集不确定性随训练样本数量的变化趋势。随着训练数据增加，测试偶然不确定性（AU）整体上升，而测试认知不确定性（EU）整体下降。这一行为符合理论预期：更多数据引入更多观测噪声（AU 升高），同时缓解模型知识不足（EU 降低），验证了两种不确定性对数据量的差异化响应。

**Figure 5** 和 **Figure 6** 分别展示了 AU 主导与 EU 主导的典型案例。在展柜高反射表面场景中，AU 显著高于 EU，源于不同视角下光照不一致导致的数据固有噪声。在仅用 5 张正面图像训练的极端稀疏视角场景中，EU 在训练分布外的视角区域急剧升高，准确反映了模型的知识缺失。

**Figure 10** 揭示了瞬态物体场景中的不确定性行为：若模型未能抑制由训练视图中的瞬态物体（如行人）引起的漂浮伪影，则 AU 和 EU 在伪影区域同时升高；若模型成功解决了瞬态问题，仅 AU 在训练瞬态曾出现的区域保持较高水平。这一发现为理解两类不确定性在遮挡与瞬态场景中的耦合/解耦机制提供了关键证据。

### 消融研究与敏感性分析

**Figure 9** 展示了正则化系数 $\lambda_{\text{reg}}$ 对定量指标的敏感性。该系数高度依赖场景：过小导致证据正则不足、高置信度错误预测；过大则过度压制不确定性、损害重建质量。**Table 3** 列出了各场景实际使用的 $\lambda_{\text{reg}}$ 值，表明当前方法缺乏自动化选择机制，需手动调节。

### 下游应用验证

**Figure 7** 展示了基于 AU 的场景清洁后处理：对 AU 超过阈值的点降低密度使其透明化，可有效移除渲染物中的漂浮伪影。降低阈值可消除更多伪影，但需平衡场景完整性。

**Figure 8** 展示了基于 EU 的主动学习实验。在 Horns 场景中，以 EU 为指导选择下一个训练视角，相比随机选择策略获得更高且更稳定的测试 PSNR。这表明认知不确定性能够有效识别信息量最大的未观测区域，为数据高效采集提供可靠依据。

### 局限性

尽管实验验证了 Evidential NeRF 在辐射度不确定性量化上的有效性，该方法仍存在以下局限：① 仅对辐射度建模不确定性，未捕获场景几何（深度、密度）的不确定性；② 推导依赖沿射线点颜色独立的假设，可能与实际统计依赖存在偏差；③ 正则化系数需逐场景手动调节，缺乏自动化机制。

### 补充图表

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/006_Table_2.jpg]]
*Table 2: Average training time per 30k steps and inference FPS of baseline nerfacto and different UQ methods on an A6000 GPU*

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison on two example scenes, with image reconstructions, error maps, and uncertainty maps. Histogram equalization is conducted on the error maps to highlight the error regions. Our method’s uncertainty is total uncertainty. In general, our method achieves better reconstruction accuracy and produces uncertainty maps that are more consistent with prediction errors*

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/007_Figure_5.jpg]]
*Figure 5: A case where AU dominates EU. The highly reflective surface of the display case in the foreground incurs specular reflections. AU arises due to the presence of data noise caused by the inconsistency of light across different training views*

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/008_Figure_6.jpg]]
*Figure 6: A case where EU dominates AU. The model is trained only by 5 images from the front and asked to render the scene from all the viewing angles. EU arises due to the lack of knowledge during training on the views out of the training distribution*

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/009_Figure_7.jpg]]
*Figure 7: Scene cleaning based on aleatoric uncertainty as a postprocessing step for floater removal. Points with AU above a certain threshold have their density reduced to become more transparent. By reducing the threshold, more artifacts can be eliminated*

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/011_Figure_9.jpg]]
*Figure 9: Sensitivity study of regularization coefficient’s effect on all the quantitative metrics of Leaves scene*

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/012_Table_3.jpg]]
*Table 3: The regularization coefficients used in each scene of LF, LLFF, and RobustNeRF datasets*

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/013_Figure_10.jpg]]
*Figure 10: Aleatoric and epistemic uncertainties of scenes with transient objects. The red bounding boxes delineate the erroneous artifacts in test renderings caused by transients in the training views. If the model fails to suppress the floaters, both AU and EU are elevated on the transients; If the model resolves the transience, only AU is higher on the regions where the training transients were once present*

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/005_Figure_4.jpg]]
*Figure 4: Test uncertainties vs. training sample size on Android*

![[assets/figures/papers/paper_list_l2122_https_arxiv_org_abs_2602_23574/figures/010_Figure_8.jpg]]
*Figure 8: Mean and standard derivation of test PSNR of three runs on Horns scene, with two active sampling strategies: EUbased selection and random selection. The samples identified via epistemic uncertainty are more informative for model learning*

## 定位与知识库关联

### 1. 概率化NeRF的三级演进谱系

Evidential NeRF的提出并非孤立的技术创新，而是NeRF概率化建模演进脉络中的第三级跳跃。图2清晰勾勒了这一谱系：

- **Level 1 — Vanilla NeRF**：仅预测点颜色与密度，通过体积渲染得到确定性像素颜色，完全不具备不确定性量化能力。
- **Level 2 — Normal NeRF**：将点颜色建模为正态分布 $c_i \mid \mu_i, \sigma_i^2 \sim \mathcal{N}(\mu_i, \sigma_i^2)$，在点独立假设下，像素颜色同样服从正态分布 $c \mid \mu, \sigma^2 \sim \mathcal{N}(\mu, \sigma^2)$，其中 $\sigma^2 = \sum w_i^2 \sigma_i^2$ 量化了渲染颜色的偶然不确定性（aleatoric uncertainty）。这是当前主流NeRF不确定性量化方法的理论基础，包括本文对比的 **Normal**（闭式正态似然）和 **MoL**（Laplace混合分布）等闭式似然模型。
- **Level 3 — Evidential NeRF**：将像素颜色的均值 $\mu$ 与方差 $\sigma^2$ 本身视为随机变量，并由高阶证据分布（Normal-Inverse-Gamma，NIG）统治。这使得模型能够在一个前向传播中同时输出偶然不确定性（AU）和认知不确定性（EU），无需回归证据参数，也无需集成多个模型。

这一谱系定位揭示了Evidential NeRF的核心创新：它不是对Level 2的修补，而是将概率建模的层次从“一阶”（预测分布参数）提升到“二阶”（预测分布参数的分布），从而在保持计算效率的前提下，实现了对两类不确定性的解耦量化。

### 2. 与基线方法的关系：优势与边界

本文在统一的nerfacto骨干网络上，系统对比了六类不确定性量化方法：

| 方法类别 | 代表方法 | 核心机制 | 局限 |
|----------|----------|----------|------|
| 无UQ基线 | Baseline (nerfacto) | 仅预测颜色与密度 | 无不确定性输出 |
| MC Dropout | Dropout | 多次前向传播采样 | 近似贝叶斯推断，仅捕获认知不确定性；推理速度慢 |
| 闭式似然 | Normal, MoL | 直接输出分布参数 | 仅捕获偶然不确定性；MoL需预测混合参数，计算开销增大 |
| 深度集成 | Ensembles, DANE | 训练多个模型取统计量 | 可同时捕获两类不确定性，但训练与推理成本随集成数线性增长；DANE引入密度感知但计算开销更大 |

**定量对比的核心发现**（Table 1）：
- 在LF数据集上，Evidential NeRF的PSNR（29.9679）超越Ensembles（29.3779）达+0.59 dB，LPIPS（0.0359）优于Ensembles（0.0411）。
- 在LLFF数据集上，NLL指标（0.6765）大幅领先DANE（9.7273），差距达-9.05，表明证据框架下的Student-t边际似然对观测噪声的建模更为精准。
- 在RobustNeRF数据集上，PSNR（26.2292）与Ensembles（26.1953）持平，但LPIPS（0.1112）显著优于Ensembles（0.1438），说明在干扰场景下感知质量更优。

**效率维度的关键优势**（Table 2）：
- 推理速度4.67 FPS，仅比最快的Normal方法（4.71 FPS）慢0.04 FPS，而Ensembles方法因多次前向传播导致FPS大幅下降。训练时间（13.57 min/30k steps）虽略高于Normal（12.83 min），但远低于Ensembles（56.10 min）和DANE（55.73 min）。

**适用边界**：
- Evidential NeRF在“无需牺牲渲染质量与推理速度”的前提下，实现了两类不确定性的联合量化，适用于对实时性有要求的场景理解与主动视觉任务。
- 但其正则化系数 $\lambda_{reg}$ 高度依赖具体场景（Figure 9, Table 3），需要手动调节，缺乏自动化选择机制。这在实际部署中增加了调参成本。

### 3. 知识库定位：证据深度学习与NeRF的交叉点

Evidential NeRF处于两条研究脉络的交汇处：

**（1）证据深度学习（Evidential Deep Learning）**
- 经典证据回归通过将目标变量的均值和方差视为NIG分布的随机变量，直接输出证据参数（$\gamma, \nu, \alpha, \beta$），从而在单次前向传播中获取两类不确定性。
- Evidential NeRF的独特贡献在于：它**不直接回归NIG参数**，而是让NeRF在点级别输出AU、EU和形状得分，再通过渲染权重的平方将不确定性从点级传播到像素级（$U^{alea} = \sum w_i^2 U_i^{alea}$，$U^{epis} = \sum w_i^2 U_i^{epis}$），最后重构NIG参数。这种“预测-传播-重构”的三段式设计，使得证据学习能够无缝嵌入体积渲染框架，避免了直接回归NIG参数时因渲染非线性导致的训练不稳定。

**（2）NeRF不确定性量化**
- 现有方法或仅捕获偶然不确定性（Normal, MoL），或依赖多次采样（Dropout）或多模型集成（Ensembles, DANE）来近似认知不确定性。
- Evidential NeRF首次在NeRF中实现了**单模型、单前向传播**的两类不确定性解耦输出，且不牺牲渲染质量。这一范式为后续工作（如3D高斯泼溅的不确定性量化）提供了可迁移的理论框架。

### 4. 局限与开放问题

**已明确的局限**：
1. **仅建模辐射度不确定性**：当前方法仅对颜色/辐射度的不确定性进行量化，尚未捕获场景几何（深度、密度）的不确定性。这意味着模型无法告知“某个表面的位置是否可靠”。
2. **点独立假设的偏差**：推导依赖沿射线点颜色独立的假设（$c_i \perp c_j \mid \mu_i, \sigma_i^2$），虽然该假设在NeRF文献中常用且有效，但实际场景中相邻点的颜色存在统计依赖，可能导致不确定性估计的精度损失。
3. **正则化系数的手动调节**：$\lambda_{reg}$ 需要针对不同场景单独设置（Table 3），缺乏自适应机制，限制了方法在开放场景中的即插即用能力。

**开放问题**：
1. **跨表示泛化**：该证据框架能否拓展至3D高斯泼溅（3DGS）等其他辐射场表示？3DGS的显式几何原语可能为几何不确定性的引入提供天然接口。
2. **点间依赖建模**：能否在点级传播中显式建模相邻采样点间的相关性（如通过条件随机场或注意力机制），以获得更精确的不确定性传播公式？
3. **几何不确定性整合**：是否可以将深度或密度的不确定性自然地纳入NIG先验框架，实现辐射度与几何不确定性的统一量化？
4. **自适应正则化**：能否设计基于场景统计量（如训练视图数、纹理复杂度）的自动化 $\lambda_{reg}$ 选择策略，减少人工调参依赖？

### 5. 证据强度评估

本文的核心声明均有较强的实验与理论支撑：
- **高置信度声明**（confidence ≥ 0.95）：不确定性传播公式（$U^{alea} = \sum w_i^2 U_i^{alea}$）的推导严格基于点独立假设和方差的线性传播性质，数学完备性高；推理速度数据（4.67 FPS）来自标准化硬件测试，可复现性强。
- **需注意的声明**（confidence ≈ 0.9）：“测试AU上升而EU下降”的结论（Figure 4）基于单一场景（Android）的实验，其跨场景泛化性需要更多验证；逐场景的正则化系数选择（Table 3）表明性能对超参数敏感，最优结果的稳定性需进一步消融确认。

## 原文 PDF

![[paperPDFs/CVPR_2026/Evidential_Neural_Radiance_Fields.pdf]]
