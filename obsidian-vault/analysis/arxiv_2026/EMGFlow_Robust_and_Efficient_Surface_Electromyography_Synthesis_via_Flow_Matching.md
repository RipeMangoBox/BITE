---
title: EMGFlow Robust and Efficient Surface Electromyography Synthesis via Flow Matching
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/EMGFlow_Robust_and_Efficient_Surface_Electromyography_Synthesis_via_Flow_Matching.pdf
project_link: null
code_link: https://github.com/Open-EXG/EMGFlow
aliases:
- ERESESFM
tags:
- arxiv_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 使用Flow Matching进行条件sEMG生成，通过自适应条件归一化、logit-normal时间采样、分类器自由引导和高阶ODE求解器的选择来调控生成动态，实现质量、覆盖率和效率的平衡。
primary_logic: Flow Matching首次应用于sEMG合成，直接学习连续传输动力学，支持灵活数值求解器，在完全依靠合成数据训练的TSTR设置下展现出更强的独立实用性和效率优势，揭示了sEMG生成中保真度与下游效用之间的早期权衡。
claims:
- EMGFlow在大多数数据集-骨干组合中达到最佳或并列最佳的增强性能，并在配对Wilcoxon检验下显著优于所有常规增强基线、PatchEMG和WGAN-GP（p<0.001）。
- EMGFlow在TSTR设置下在所有六个数据集-骨干组合中均优于加速DDIM基线，并在五个组合中优于全步DDPM。
- 更强的分类器自由引导（CFG）虽然提升了类别判别性指标（IS、CAS），但降低了覆盖率（Recall、Coverage）和下游效用（TSTR、增强准确率）。
- logit-normal时间采样在所有评估指标上均优于均匀采样，尤其在TSTR准确率上增益最大。
---

# EMGFlow Robust and Efficient Surface Electromyography Synthesis via Flow Matching

> [!tip] 核心洞察
> Flow Matching首次应用于sEMG合成，直接学习连续传输动力学，支持灵活数值求解器，在完全依靠合成数据训练的TSTR设置下展现出更强的独立实用性和效率优势，揭示了sEMG生成中保真度与下游效用之间的早期权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | EMGFlow：基于流匹配的鲁棒高效表面肌电信号合成 |
| 英文题名 | EMGFlow Robust and Efficient Surface Electromyography Synthesis via Flow Matching |
| 会议/期刊 | arXiv 2026 |
| Links | [Code](https://github.com/Open-EXG/EMGFlow) · [paper](https://arxiv.org/abs/2604.13685) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | EMGFlow |
| Dataset | Ninapro DB7, Ninapro DB4 |

> [!tip] 效果简介
> - Ninapro DB7 (EMGHandNet) 上，Accuracy 78.26 ± 3.95 vs 77.73 ± 4.24 (DDPM) (+0.53)。
> - Ninapro DB7 (WaveFormer) 上，Macro-F1 79.90 ± 3.68 vs 79.84 ± 3.83 (DDPM) (+0.06)。
> - Ninapro DB4 (EMGHandNet) 上，Accuracy 70.44 ± 4.74 vs 69.94 ± 5.12 (DDPM) (+0.50)。

## 概要

表面肌电信号（sEMG）手势识别面临**数据稀缺与受试者多样性有限**的双重瓶颈：采集高质量多通道sEMG数据成本高昂，且现有生成式增强方法中，GAN存在训练不稳定和模式坍塌，扩散模型则因迭代采样导致推理效率低下，使得合成数据的独立实用性不足。

针对上述问题，本文提出 **EMGFlow**——首个将**流匹配（Flow Matching）**应用于条件sEMG生成的框架。其核心洞察在于：流匹配直接学习从噪声到数据的连续传输动力学，支持灵活的数值求解器选择，在完全依靠合成数据训练的严格设定（TSTR）下展现出更强的独立实用性和效率优势，同时揭示了sEMG生成中**保真度与下游效用之间的早期权衡**。

在方法定位上，EMGFlow通过四个关键设计调控生成动态：
- **自适应条件归一化（AdaGN）**：替代简单的加法或拼接条件注入，在保真度与分布覆盖间取得最佳平衡；
- **logit-normal时间采样**：强调流轨迹的中间段，在所有评估指标上优于均匀采样；
- **分类器自由引导（CFG）**：推理时调节生成强度，但更强的引导虽提升类别判别性，却会降低覆盖率和下游效用；
- **高阶ODE求解器（Heun/RK4）**：在匹配函数评估次数（NFE）下，Heun求解器始终优于扩散模型的DDIM采样。

主要实验结果：
- **增强性能**：在Ninapro DB7/DB4/DB2三个数据集上，EMGFlow在大多数数据集-骨干组合中达到最佳或并列最佳的增强准确率，并在配对Wilcoxon检验下显著优于所有常规增强基线、PatchEMG和WGAN-GP（p<0.001）。
- **TSTR独立实用性**：在所有六个数据集-骨干组合中均优于加速DDIM基线，并在五个组合中优于全步DDPM。
- **效率优势**：FM配合Heun求解器在10 NFE时已在FID和CAS上超过DDIM的50 NFE表现，同时计算量（FLOPs）和吞吐量均显著优于DDPM。

**局限与待验证方向**：当前实验采用被试内交叉验证协议，尚未验证跨被试或跨会话泛化效果；仅在三个Ninapro基准数据集上评估；生成限定于固定长度窗口，未扩展到完整试次级别。未来工作可探索更低NFE的蒸馏采样、跨被试泛化、以及在其他生理时间序列（EEG、ECG）中的适用性。

表面肌电信号（sEMG）手势识别是人机交互与康复工程中的核心技术。然而，sEMG数据的采集成本高昂，受试者内与受试者间的信号变异性大，导致实际可用的标注数据规模有限，严重制约了深度学习模型的泛化能力。数据增强是缓解这一瓶颈的常用手段，但传统的手工扰动增强（如抖动、缩放、时间掩码等）仅对信号施加浅层变换，难以模拟sEMG中复杂的生理与采集噪声结构，对下游识别性能的提升幅度有限。

生成式增强方法试图从数据分布层面学习合成逼真的sEMG样本，从而提供更丰富的训练信号。当前主流的生成范式存在两难困境：生成对抗网络（GAN）虽推理速度快，但在sEMG生成中面临训练不稳定和模式坍塌问题，导致合成样本的多样性不足；去噪扩散概率模型（DDPM）虽能生成高质量样本，但其迭代采样过程需要数百至上千步函数评估，推理效率低下，严重限制了实际部署的可行性。加速采样方法（如DDIM）虽可减少采样步数，但在低步数下保真度退化明显，且扩散模型对采样器设计的依赖性强，灵活性受限。

连续归一化流（Continuous Normalizing Flows）和流匹配（Flow Matching, FM）框架为生成建模提供了新的路径。FM直接学习数据与噪声之间连续传输动力学的速度场，支持任意显式ODE求解器进行积分，从而在推理效率与生成质量之间提供了更灵活的权衡空间。然而，FM在结构化生理时间序列（尤其是多通道sEMG）中的适用性、条件注入机制的设计，以及合成数据在下游任务中的独立实用性，此前均未被系统研究。

针对上述缺口，本文提出EMGFlow——首个基于流匹配的条件sEMG生成框架。EMGFlow通过自适应条件归一化（AdaGN）、logit-normal时间采样和分类器自由引导等设计选择，在统一的评估协议下（涵盖特征空间保真度、分布几何和下游效用）系统探索了FM在sEMG合成中的质量-效率权衡，并首次揭示了sEMG生成中保真度与下游实用性之间的早期权衡关系。

## 核心方法与创新机理

EMGFlow的贡献不在于提出全新的生成范式，而在于首次将**流匹配（Flow Matching, FM）**引入sEMG合成领域，并通过一系列精心设计的“**变更槽位（changed slots）**”在质量、覆盖率和效率之间建立了独特的平衡。相对于扩散基线（DDPM/DDIM），其核心创新可归结为以下四个关键设计选择。

### 1. 生成范式切换：从随机微分方程到常微分方程

传统扩散模型依赖随机微分方程（SDE）的逐步去噪，而EMGFlow直接学习从噪声到数据的**连续传输动力学**，将生成过程建模为常微分方程（ODE）的求解：

$$x_t = (1 - t) x_0 + t x_1$$

其目标速度场为常数差 $dx_t/dt = x_1 - x_0$，训练目标简化为均方误差损失：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E} \Big[ || \nu_{\theta}(x_t, t, y) - (x_1 - x_0) ||_2^2 \Big]$$

这一范式转换带来了两个直接优势：（1）**推理灵活性**——可自由选择ODE求解器（Euler、Heun、RK4）及其函数评估次数（NFE），在质量与速度之间动态权衡；（2）**训练稳定性**——避免了GAN的模式坍塌和扩散模型对采样步数的强依赖。证据显示，FM配合Heun求解器在10 NFE时已在FID和CAS上超过DDIM的50 NFE表现（Table 6），且训练初期FID下降更快（Figure 6）。

### 2. 条件接口：自适应GroupNorm（AdaGN）

相对于基线常用的BatchNorm + 加法/拼接条件注入，EMGFlow采用**GroupNorm + 自适应GroupNorm（AdaGN）**作为条件接口。消融实验（Table 8, Table 9）表明：
- **GN+add**（加法条件）在FID上与默认模型接近（2.03 vs. 2.12, p=0.07），但IS和CAS显著下降（p<0.005），说明简单加法可部分保持全局分布对齐，却削弱了类别感知结构建模；
- **GN+concat**（拼接条件）在FID、IS、CAS上全面恶化（p<10⁻⁴），表明朴素拼接在此设置下是较差的条件接口；
- **GN+AdaGN**在增强和TSTR下游任务上均取得最佳性能，同时在保真度和分布覆盖（PRDC几何指标）上达到最优平衡。

这一发现揭示了条件注入机制对生成数据下游效用的实质性影响，而非仅仅是实现细节。

### 3. 时间采样策略：logit-normal采样

扩散模型通常采用均匀时间采样 $t \sim \mathcal{U}(0,1)$，而EMGFlow采用**logit-normal采样**：

$$z \sim N(\mu, \sigma^2), \quad t = \mathrm{sigmoid}(z) = \frac{1}{1 + e^{-z}}$$

该分布在0和1附近密度较低，在中间区域密度较高，强调流轨迹的中间部分。消融实验（Figure 8）显示，logit-normal采样在**所有评估指标**上均优于均匀采样，尤其在TSTR准确率上增益最大。这表明强调中间轨迹提供了更有用的训练偏置，迫使网络更精细地学习传输动力学的关键阶段。

### 4. 推理时引导与求解器选择

EMGFlow引入**分类器自由引导（CFG）**作为推理时的调控旋钮：

$$\hat{\nu}_{\theta}(x_t, t, y) = \nu_{\theta}(x_t, t, \emptyset) + w \left( \nu_{\theta}(x_t, t, y) - \nu_{\theta}(x_t, t, \emptyset) \right)$$

默认 $w=1$ 对应标准条件生成。然而，Figure 3揭示了一个关键的**保真度-效用权衡**：增大 $w$ 会单调提升类别判别性指标（IS、CAS），但持续降低覆盖率（Recall、Coverage）和下游效用（TSTR、增强准确率）。这一发现表明，更强的类别引导虽然使生成样本在特征空间中更“清晰可分”，却以牺牲多样性和实际可用性为代价。

在求解器方面，EMGFlow默认使用20步Heun采样，并在匹配NFE下始终优于Euler（Figure 7）。高阶积分（Heun、RK4）更好地利用了学习到的连续向量场，在中等NFE预算下实现更低的FID和更高的CAS。

### 创新边界与未验证空间

需要指出，EMGFlow的贡献集中在**被试内交叉验证**协议下的固定窗口生成，以下方向尚未验证：
- 跨被试或跨会话泛化能力；
- 低于10 NFE的极端低预算采样策略（如蒸馏）；
- 自适应或任务感知的引导机制设计；
- 非均匀时间采样的更优参数化（$\mu$ 和 $\sigma$ 的选择）是否具有普遍指导意义。

EMGFlow 将条件 sEMG 生成形式化为一个连续时间传输问题：从易于采样的先验分布（高斯噪声）出发，学习一条通向特定手势类别的真实多通道 sEMG 窗口分布的连续轨迹。整个流水线由四个耦合模块构成，形成从原始信号到可部署合成数据的闭环。

**模块一：数据采集与滑动窗口预处理。** 原始多通道 sEMG 信号首先被分割为固定长度 200 ms、步长 50 ms 的滑动窗口，随后对每个通道独立进行 z-score 归一化。每个窗口被表示为一个张量 $\boldsymbol{x} \in \mathbb{R}^{C \times L}$，并携带对应的手势标签 $\boldsymbol{y} \in \{1, \dots, K\}$。该模块的输出是标准化的窗口-标签对，为后续条件生成提供监督信号。

**模块二：条件流匹配训练。** 训练的核心目标是学习一个速度场网络 $\nu_\theta$，使其能够预测从噪声到数据的最优传输方向。具体而言，对于每个真实窗口 $x_1$，从高斯先验中采样噪声 $x_0 \sim \mathcal{N}(0, I)$，并沿线性插值路径 $x_t = (1 - t) x_0 + t x_1$ 构造中间状态。目标速度场为常数差 $x_1 - x_0$，损失函数为均方误差：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E} \Big[ || \nu_{\theta}(x_t, t, y) - (x_1 - x_0) ||_2^2 \Big], \quad t \sim p(t)$$

训练时采用 logit-normal 时间采样（$\mu=0, \sigma=1$）替代传统的均匀采样，使训练焦点偏向路径的中间阶段。条件信息 $y$ 通过自适应 GroupNorm（AdaGN）注入网络，而非简单的加法或拼接。扩散基线使用完全相同的 1D U-Net 骨干、训练步数（20k）、优化器（Adam，lr=5e-4）、批大小（128）和指数移动平均，确保比较的公平性。

**模块三：合成 EMG 生成。** 推理时从随机噪声 $x(0) = x_0$ 出发，通过求解常微分方程生成指定类别的样本：

$$\frac{d x_t}{d t} = \nu_{\theta}(x_t, t, y)$$

默认采用 20 步 Heun 二阶求解器进行数值积分。同时引入分类器自由引导（CFG）以调节生成强度：

$$\hat{\nu}_{\theta}(x_t, t, y) = \nu_{\theta}(x_t, t, \emptyset) + w \left( \nu_{\theta}(x_t, t, y) - \nu_{\theta}(x_t, t, \emptyset) \right)$$

其中 $w=1$ 对应标准条件生成，$w>1$ 增强类别判别性但会牺牲覆盖率和下游效用（见 Figure 3）。该模块的输出是任意数量的、携带指定手势标签的合成 sEMG 窗口。

**模块四：综合评估。** 合成数据从三个维度接受检验：(1) 基于特征的保真度指标（FID、IS、CAS），使用在真实训练集上单独训练的 EMGHandNet 作为特征提取器；(2) 分布几何分析，包括精确率-召回率-密度-覆盖率（PRDC）和原型集中度；(3) 下游效用，涵盖增强实验（将合成数据混入真实训练集）和更严格的 TSTR 设置（下游分类器仅使用合成数据训练，在真实测试集上评估）。这一多层级协议揭示了 sEMG 生成中保真度与下游效用之间的早期权衡——更强的 CFG 虽然提升类别判别性，却持续降低 TSTR 和增强准确率。

![[assets/figures/papers/paper_list_l10_EMGFlow_Robust_and_Efficient_Surface_Electromyography_Synthesis_via_Flow_motion20/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed EMGFlow pipeline. The framework consists of four stages: (a) sEMG data acquisition and sliding-window preprocessing; (b) conditional flow-matching training with time sampling and AdaGN-based condition injection; (c) synthetic EMG generation via classifier-free guidance and ODE solvers; and (d) comprehensive evaluation through fidelity metrics, train-on-synthetic test-on-real (TSTR), and augmentation experiments*

### 3.1 问题形式化：条件窗口级sEMG生成

EMGFlow将sEMG手势识别中的数据稀缺问题建模为**条件窗口级生成**任务。给定一个真实sEMG样本，表示为多通道窗口及其手势标签：

$$ \boldsymbol{x} \in \mathbb{R}^{C \times L}, \quad \boldsymbol{y} \in \{1, \dots, K\} $$

其中 $C$ 为通道数，$L$ 为窗口长度，$y$ 为对应的手势类别标签。生成器的目标是从随机潜变量 $z$ 和类别条件 $y$ 出发，合成逼真的sEMG窗口：

$$ G(z, y) \to \hat{x} \in \mathbb{R}^{C \times L} $$

这一形式化将生成任务明确为**类别条件映射**，为后续的流匹配训练和分类器引导提供了统一的数学框架。

### 3.2 流匹配核心机制：从插值路径到速度场学习

EMGFlow的核心创新在于**将sEMG生成建模为连续时间传输问题**，而非扩散模型中迭代去噪的离散步骤。其数学基础建立在Flow Matching框架之上，包含三个关键组件。

**线性插值路径。** 在训练时，从高斯噪声 $x_0 \sim \mathcal{N}(0, I)$ 和真实数据 $x_1$ 之间构建一条连续的线性插值轨迹：

$$ x_t = (1 - t) x_0 + t x_1 \quad \text{(Eq. 3)} $$

其中 $t \in [0, 1]$ 为时间参数。该路径在 $t=0$ 时为纯噪声，$t=1$ 时为目标数据，中间状态为二者的凸组合。

**目标速度场。** 沿此路径，状态 $x_t$ 的时间导数为常数差向量：

$$ \frac{d x_t}{d t} = x_1 - x_0 \quad \text{(Eq. 4)} $$

这意味着从噪声到数据的最优传输方向在整条路径上保持不变，为网络学习提供了简洁的回归目标。

**Flow Matching损失函数。** 训练一个速度场网络 $\nu_\theta$，以当前状态 $x_t$、时间 $t$ 和类别条件 $y$ 为输入，预测目标速度：

$$ \mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t \sim p(t),\, x_0 \sim \mathcal{N}(0,I),\, (x_1,y) \sim p_{\text{data}}} \Big[ || \nu_{\theta}(x_t, t, y) - (x_1 - x_0) ||_2^2 \Big] \quad \text{(Eq. 5)} $$

该损失直接回归速度向量，避免了扩散模型中复杂的噪声调度和变分下界推导，是FM训练效率优于DDPM的关键原因之一。

### 3.3 生成过程：ODE求解与分类器自由引导

**生成ODE。** 训练完成后，从随机噪声 $x(0) = x_0$ 出发，通过求解以下常微分方程生成样本：

$$ \frac{d x_t}{d t} = \nu_{\theta}(x_t, t, y), \quad x(0) = x_0 \quad \text{(Eq. 6)} $$

与扩散模型不同，FM支持**灵活选择ODE求解器**，无需固定于特定的采样步骤数或噪声调度。最基本的求解方式为显式Euler法：

$$ x_{t_{k+1}} = x_{t_k} + (t_{k+1} - t_k) \, \nu_{\theta}(x_{t_k}, t_k, y) \quad \text{(Eq. 7)} $$

**高阶求解器。** FM的连续向量场特性允许使用更高阶的Runge-Kutta方法，其一般形式为：

$$ x_{n+1} = x_n + h \sum_{i=1}^{s} b_i \, \nu_{\theta}(\tilde{x}_i, \tilde{t}_i, y) \quad \text{(Eq. 12)} $$

其中 $h$ 为步长，$s$ 为每步的网络评估次数（NFE）。EMGFlow默认采用**Heun方法（20步）**，在匹配NFE下始终优于DDIM的Euler型采样（Table 6），且仅需10 NFE即可在FID和CAS上超越DDIM的50 NFE表现。

**分类器自由引导。** 在推理时，通过混合条件预测与无条件预测来调节生成强度：

$$ \hat{\nu}_{\theta}(x_t, t, y) = \nu_{\theta}(x_t, t, \emptyset) + w \left( \nu_{\theta}(x_t, t, y) - \nu_{\theta}(x_t, t, \emptyset) \right) \quad \text{(Eq. 8)} $$

其中 $w \ge 1$ 为引导权重，$w=1$ 退化为标准条件生成。增大 $w$ 会强化类别判别性特征，但消融实验（Figure 3）揭示了一个关键权衡：更强的引导虽然提升IS和CAS，却持续**降低覆盖率（Recall、Coverage）和下游效用（TSTR、增强准确率）**，表明过强的类别引导会牺牲生成多样性。

### 3.4 时间采样策略：logit-normal分布

训练时的时间点采样分布 $p(t)$ 直接影响模型对传输路径不同阶段的关注程度。标准做法为均匀采样：

$$ t \sim \mathcal{U}(0, 1) \quad \text{(Eq. 9)} $$

EMGFlow创新性地采用**logit-normal采样**，先采样高斯变量再经sigmoid映射：

$$ z \sim \mathcal{N}(\mu, \sigma^2), \quad t = \mathrm{sigmoid}(z) = \frac{1}{1 + e^{-z}} \quad \text{(Eq. 10)} $$

默认参数 $\mu=0, \sigma=1$ 使得 $t$ 的分布向中间区域集中，强调轨迹的中间阶段。消融实验（Figure 8）表明，logit-normal采样在**所有评估指标上均优于均匀采样**，尤其在TSTR准确率上增益最大，说明强调中间轨迹提供了更有用的训练偏置。

### 3.5 条件接口：自适应GroupNorm

EMGFlow采用**GroupNorm + 自适应GroupNorm（AdaGN）**作为条件注入接口，替代了PatchEMG原骨干中的BatchNorm。其核心设计是通过类别和时间条件调制归一化层的缩放与偏移参数，使条件信息在网络各层自适应地影响特征分布。

消融实验（Table 8, Table 9）系统比较了三种条件接口：
- **GN+AdaGN（默认）**：在增强和TSTR下游任务上均取得最佳性能，同时在保真度和分布覆盖上实现最佳平衡；
- **GN+add**：简单加法条件注入，FID接近默认模型但IS和CAS显著下降，表明虽能部分保持全局分布对齐，却弱化了类别感知结构建模；
- **GN+concat**：朴素拼接条件，在FID、IS、CAS上均显著恶化（$p < 10^{-4}$），验证了直接拼接在此场景下是较差的条件接口。

这表明**条件接口的设计并非次要实现细节，而是实质性影响生成数据下游效用的关键架构选择**。

![[assets/figures/papers/paper_list_l10_EMGFlow_Robust_and_Efficient_Surface_Electromyography_Synthesis_via_Flow_motion20/figures/016_Figure_7.jpg]]
*Figure 7: Comparison of Euler, Heun, and RK4 within EMGFlow under matched numbers of function evaluations (NFE) on DB7. When the sampling budget becomes moderately large, Heun and RK4 consistently achieve lower FID and higher CAS than Euler, showing that higher-order integration better exploits the learned continuous vector field. Euler is only comparatively less poor in the extremely low-NFE regime, where the number of effective integration steps is too small for multi-stage solvers to realize their accuracy advantage*

## 实验与关键发现

### 核心实验设置

实验在三个公开的Ninapro基准数据集上进行：**DB2**（40名受试者，49个手势，12通道，2000 Hz）、**DB4**（10名受试者，52个手势，12通道，2000 Hz）和**DB7**（20名受试者，40个手势，12通道，2000 Hz）。所有数据集均采用被试内交叉验证协议，以试验1、3、4、6为训练集，试验2、5为测试集。原始sEMG信号经200 ms滑动窗口（步长50 ms）分割，并进行通道级z-score归一化。

生成模型方面，EMGFlow与扩散基线（DDPM、DDIM）共享相同的紧凑型1D U-Net骨干（从PatchEMG适配，将原BatchNorm替换为GroupNorm），训练步数均为20k，优化器为Adam（lr=5e-4），批大小为128，并应用指数移动平均（EMA）。FM默认采用logit-normal时间采样（μ=0, σ=1）、余弦退火调度和20步Heun采样；DDIM使用50步加速采样，DDPM使用全1000步祖先采样。下游分类器为EMGHandNet和WaveFormer，均以AdamW（lr=1e-3，weight decay=3e-4）训练100轮。

评估体系涵盖三个维度：**基于特征的保真度指标**（FID、IS、CAS，使用独立训练的EMGHandNet作为特征提取器）、**分布几何指标**（PRDC精度/召回率/密度/覆盖率、邻域真实感诊断、原型集中度）以及**下游效用**（增强分类准确率和TSTR准确率）。

### 增强性能：生成式方法优于常规增强

在Ninapro DB7、DB4和DB2三个数据集上，EMGFlow在大多数数据集-骨干组合中达到最佳或并列最佳的增强性能。以DB7为例（Table 2），EMGFlow在EMGHandNet骨干上取得78.26%的准确率，在WaveFormer上取得79.90%的Macro-F1，均优于DDPM（77.73%和79.84%）和DDIM（77.60%和79.79%）。配对Wilcoxon检验表明，EMGFlow在所有三个数据集上均显著优于所有常规增强基线（Replicate、Jitter&Scale、Upsample、Freq-Mask、Mixup、STAug、Freq-Mix）以及生成式基线WGAN-GP和PatchEMG（p<0.001）。

![[assets/figures/papers/paper_list_l10_EMGFlow_Robust_and_Efficient_Surface_Electromyography_Synthesis_via_Flow_motion20/figures/003_Table_2.jpg]]
*Table 2: Performance comparison of conventional and generative augmentation methods on Ninapro DB7 using EMGHandNet and Waveformer. Results are reported as mean ± std (%). Best results are highlighted in bold; second-best are underlined. Overall, learned generative augmentation is consistently stronger than most hand-crafted perturbation baselines, and EMGFlow achieves the best or tied-best performance in most metrics, indicating a favorable accuracy–efficiency trade-off relative to DDIM, DDPM, and WGAN-GP*

值得注意的是，常规增强方法中表现最强的Jitter&Scale在DB7上仅达到77.16%的准确率，而生成式方法普遍高出1-2个百分点，表明学习到的数据分布建模比手工设计的扰动策略更有效。在DB2上，DDPM在EMGHandNet的准确率上略优于EMGFlow（69.94% vs. 70.44%），但这一微小优势伴随着千倍于EMGFlow的采样成本，使其在实际部署中不具竞争力。

### TSTR评估：独立合成数据的实用性

TSTR（Train-on-Synthetic Test-on-Real）设置更为严苛——下游分类器仅用合成数据训练，随后在真实测试集上评估，直接衡量合成数据作为独立训练资源的效用。Table 5显示，EMGFlow在所有六个数据集-骨干组合中均一致优于加速DDIM基线，并在五个组合中优于全步DDPM。以DB7的EMGHandNet为例，EMGFlow的TSTR准确率为68.91%，显著高于DDIM（65.82%）和DDPM（67.45%）。在DB4的WaveFormer上，EMGFlow的优势更为突出（61.24% vs. DDPM 59.87% vs. DDIM 57.33%）。

这一结果揭示了扩散模型在sEMG生成中的一个关键瓶颈：尽管DDPM在增强设置下表现强劲，其全步采样的高质量在TSTR下未能充分转化为独立训练效用，而FM通过连续传输动力学学习到的向量场在低NFE下即能产生对下游任务更有用的样本。

### 保真度与效用的早期权衡

特征空间保真度评估（Figure 2）表明，所有生成式方法在FID、IS和CAS上均与真实数据存在明显差距，但EMGFlow在三个数据集上均达到生成式方法中的最佳整体保真度。t-SNE可视化（Figure 4）进一步证实，EMGFlow生成的样本在特征空间中与真实类别簇高度重叠，但在某些手势类上仍存在轻微的分布偏移和密度差异。

![[assets/figures/papers/paper_list_l10_EMGFlow_Robust_and_Efficient_Surface_Electromyography_Synthesis_via_Flow_motion20/figures/007_Figure_2.jpg]]
*Figure 2: Single-column comparison of feature-based fidelity metrics across datasets. Each panel reports one metric, and the asterisk marks the best learned generator within each dataset. EMGFlow achieves the strongest overall fidelity, while the real-data baseline remains clearly better than all learned generators*

![[assets/figures/papers/paper_list_l10_EMGFlow_Robust_and_Efficient_Surface_Electromyography_Synthesis_via_Flow_motion20/figures/009_Figure_4.jpg]]
*Figure 4: t-SNE visualizations of real (blue) and generated (red) samples for one subject from (a) DB4, (b) DB7, and (c) DB2, where different shades denote different gesture classes. Across all three datasets, the generated points largely overlap the real class clusters, suggesting that EMGFlow captures the coarse class-conditional geometry in feature space. At the same time, several clusters still show mild shifts and density differences, which is consistent with the remaining realism gap indicated by the quantitative fidelity metrics*

一个核心发现是**保真度与下游效用之间的早期权衡**。分类器自由引导（CFG）的消融实验（Figure 3）清晰展示了这一现象：随着引导权重w从1增加到3，IS和CAS单调提升（类别判别性增强），但FID恶化（全局分布对齐减弱），同时下游增强准确率和TSTR准确率持续下降。具体而言，PRDC指标显示精度和密度上升，但召回率和覆盖率下降，表明更强的CFG使生成分布更集中于类别中心，却牺牲了类内多样性和尾部覆盖。这一发现对实际部署具有重要指导意义：**追求极致的类别判别性保真度可能损害合成数据的下游训练效用**。

### 求解器效率：FM以更低NFE超越扩散

求解器效率对比（Table 6）是EMGFlow效率优势的核心证据。在严格匹配NFE（函数评估次数）的条件下，FM配合Heun求解器在整个10-50 NFE范围内始终比DDIM取得更低的FID和更高的CAS。关键数据点：**FM+Heun在仅10 NFE时即在FID（2.066）和CAS上超过DDIM在50 NFE时的表现（FID=2.647）**，意味着FM以五分之一的采样预算实现了更优的样本质量。

![[assets/figures/papers/paper_list_l10_EMGFlow_Robust_and_Efficient_Surface_Electromyography_Synthesis_via_Flow_motion20/figures/012_Table_6.jpg]]
*Table 6: Comparison between DDIM and Heun under matched numbers of function evaluations (NFE) on DB7. Under the same sampling budget, Heun consistently achieves lower FID, higher CAS, and higher IS than DDIM across the entire 10–50 NFE range. Notably, FM with Heun at 10 NFE already surpasses DDIM at 50 NFE on both FID and CAS, highlighting the efficiency advantage of Flow Matching with higher-order ODE solvers*

内部求解器消融（Figure 7）表明，当NFE预算适中时，Heun和RK4等高阶求解器显著优于Euler方法，因为它们能更好地利用FM学习到的连续向量场。Euler仅在极低NFE（<10）时相对不差，此时多阶段求解器的精度优势因积分步数过少而无法体现。

### 时间采样与条件接口的设计选择

**时间采样策略**的消融（Figure 8）表明，logit-normal采样（μ=0, σ=1）在所有评估指标上均优于均匀采样，其中TSTR准确率的增益最为显著。这一结果说明，强调流轨迹的中间部分（而非均匀覆盖整个[0,1]区间）为训练提供了更有用的偏置，可能因为中间阶段对应着从噪声到数据结构的关键过渡。

**条件接口**的消融（Table 8和Table 9）揭示了自适应归一化的重要性。默认的GN+AdaGN设计在增强和TSTR下游任务上均显著优于GN+add和GN+concat变体。从保真度角度看，GN+add在FID上与默认模型接近（2.03 vs. 2.12, p=0.07），但IS和CAS已显著下降（p<0.005），表明简单加性条件注入可部分保持全局分布对齐，但削弱了类别感知的结构建模。GN+concat在FID、IS和CAS上均显著恶化（p<10⁻⁴），说明朴素拼接在此设置下是不良的条件接口。

### 失败模式与局限性

尽管EMGFlow在多数指标上表现优异，以下局限性需要在解读结果时审慎考虑：

1. **跨被试泛化未验证**：所有实验采用被试内交叉验证协议，尚未评估生成式增强在跨被试或跨会话场景下的效果。考虑到sEMG信号的高度受试者特异性，这一局限性可能限制了结论的泛化范围。

2. **数据集覆盖有限**：仅在三个Ninapro基准数据集上评估，更广泛的采集条件（如不同电极配置、采样率、手势类别数）下的有效性仍需验证。

3. **窗口级生成的局限**：生成针对固定长度窗口（200 ms），未扩展到完整试次级别的生成，这可能限制了其在需要时序上下文的连续手势识别中的应用。

4. **保真度指标的依赖性**：所有基于特征的保真度指标依赖于固定的预训练EMGHandNet特征提取器，其绝对值应在该特定协议下解读，不同特征提取器可能导致不同的保真度排序。

5. **TSTR下的绝对性能差距**：即使在最佳设置下，TSTR准确率仍显著低于使用真实数据训练的基线（如DB7上68.91% vs. 78.26%），表明合成数据在完全替代真实数据方面仍有实质性差距。

## 定位与知识库关联

### 1. 方法定位与核心贡献

EMGFlow首次将**流匹配（Flow Matching, FM）**引入表面肌电信号（sEMG）合成领域，构建了一个条件生成框架，用于为手势识别任务生成多通道sEMG窗口。其核心贡献在于将sEMG生成建模为从简单先验分布到类条件数据分布的连续时间传输问题，直接学习速度场而非逐步去噪的分数函数，从而获得推理时求解器的灵活性。这一范式转变在sEMG生成中揭示了**保真度与下游效用之间的早期权衡**：更强的类别判别性生成（通过分类器自由引导实现）虽然提升Inception Score和类别可分性，却可能损害分布覆盖率和下游任务性能。

### 2. 与现有生成式基线的谱系关系

#### 2.1 扩散模型谱系

EMGFlow与扩散模型共享相同的1D U-Net骨干网络（从**PatchEMG**（Xiong et al., TIM 2024）适配而来），但生成机制有本质差异：

- **DDPM**（Ho et al., NeurIPS 2020）通过1000步迭代去噪生成样本，推理成本高昂。实验表明，EMGFlow在TSTR设置下于六个数据集-骨干组合中的五个上优于全步DDPM（Table 5），且计算量大幅降低（Table 7）。
- **DDIM**（Song et al., ICLR 2020）通过50步加速采样在扩散模型中实现了效率提升，但EMGFlow配合Heun求解器在匹配函数评估次数（NFE）下始终优于DDIM。更重要的是，**FM配合Heun在10 NFE时已在FID和CAS上超过DDIM的50 NFE表现**（Table 6），揭示了流匹配在低采样预算下的结构性效率优势。

#### 2.2 GAN谱系

- **WGAN-GP**（Coelho et al., CMBBE 2023）作为sEMG生成的代表性GAN基线，面临训练不稳定和模式坍塌的已知问题。EMGFlow在所有增强实验中均显著优于WGAN-GP（配对Wilcoxon检验，p<0.001），且训练动态更稳定——FID下降曲线显示EMGFlow在更少训练步数内达到低FID稳态（Figure 6）。

#### 2.3 常规增强谱系

EMGFlow与七种常规增强方法进行了系统比较，包括**Jitter&Scale**（Um et al., ICMI 2017）、**Upsample**（Semenoglou et al., PR 2023）、**Freq-Mask**（Chen et al., 2023）、**Mixup**（Zhang et al., ICLR 2018）、**STAug**（Zhang et al., ICASSP 2023）、**Freq-Mix**（Chen et al., 2023）以及Replicate基线。在大多数数据集-骨干组合中，生成式增强（EMGFlow、DDPM、DDIM）一致优于手工设计的扰动增强，而EMGFlow在其中取得最佳或并列最佳性能（Table 2–4）。

### 3. 关键设计选择的知识贡献

#### 3.1 归一化与条件接口

EMGFlow将PatchEMG原有的BatchNorm替换为**GroupNorm + 自适应GroupNorm（AdaGN）**条件调制。消融实验（Table 8, Table 9）表明：
- **GN+add**（加法条件注入）在FID上与AdaGN接近（2.03 vs. 2.12, p=0.07），但IS和CAS已显著下降（p<0.005），说明简单加法条件可部分保持全局分布对齐，但削弱了类别感知的结构建模。
- **GN+concat**（拼接条件注入）在FID、IS、CAS上均显著恶化（p<10⁻⁴），表明朴素拼接在此任务中是较差的条件接口。
- **GN+AdaGN**在保真度和下游效用之间取得了最佳平衡，证明自适应条件归一化对生成数据的实用性有实质性影响，而非次要实现细节。

#### 3.2 训练时间采样策略

**logit-normal时间采样**（μ=0, σ=1）在所有评估指标上均优于均匀采样，尤其在TSTR准确率上增益最大（Figure 8）。这一发现揭示了sEMG生成中的一个重要训练偏置：强调流轨迹的中间部分比均匀覆盖整个路径更有助于学习对下游任务有用的生成动态。

#### 3.3 推理求解器选择

FM框架支持灵活的ODE求解器。在匹配NFE下，**Heun和RK4高阶求解器**始终比Euler取得更低的FID和更高的CAS（Figure 7），表明高阶积分更好地利用了学习到的连续向量场。Euler仅在极低NFE区间相对不差，此时多阶段求解器因有效积分步数过少而无法发挥精度优势。

#### 3.4 分类器自由引导的权衡

分类器自由引导（CFG）权重的消融（Figure 3）揭示了sEMG生成中的核心权衡：增大w单调提升类别判别性指标（IS、CAS）和局部真实感，但持续降低覆盖率（Recall、Coverage）和下游效用（TSTR、增强准确率）。这一发现表明，**更强的类别条件引导虽然使生成样本在特征空间中更聚集于类中心，却以牺牲分布覆盖为代价**，对需要多样性的下游任务产生负面影响。

### 4. 适用边界与局限

1. **评估协议边界**：实验采用被试内交叉验证（cross-trial）协议，尚未验证生成式增强在跨被试或跨会话泛化中的效果。现有结论在此协议范围内成立，但跨域泛化能力仍需独立验证。

2. **数据集覆盖范围**：仅在三个公开的Ninapro基准数据集（DB2、DB4、DB7）上评估，均为12通道、2000 Hz采样率的高密度sEMG采集。更广泛的采集条件（如不同通道数、采样率、电极配置）下的有效性尚未验证。

3. **生成粒度限制**：生成针对固定长度窗口（200ms）进行，未扩展到完整试次级别的生成。对于需要长时依赖建模的应用场景，此粒度可能不足。

4. **保真度度量的依赖性**：所有基于特征的保真度指标依赖于固定的预训练EMGHandNet特征提取器，其绝对值应在该特定协议下解读，不同特征提取器可能产生不同的相对排序。

### 5. 开放问题

1. **跨域泛化**：Flow Matching在跨被试和跨会话设置下能否继续提升泛化能力？条件接口和引导策略是否需要针对域偏移进行调整？

2. **极致效率**：更低NFE或蒸馏采样的策略是否能进一步加速生成，同时保持质量？FM的连续时间特性为步长蒸馏提供了理论可能性。

3. **跨模态迁移**：在EEG、ECG等其他生理时间序列中，类似的保真度-效用权衡和设计选择（AdaGN条件接口、logit-normal时间采样、CFG权重调节）是否成立？这些选择是否具有跨模态的普适性？

4. **自适应引导机制**：如何设计自适应或任务感知的引导机制，以在保持覆盖率的同时提升下游性能？当前的固定CFG权重无法同时优化保真度和效用。

5. **时间采样的最优参数化**：logit-normal采样的μ和σ选择是否具有普遍指导意义？是否存在任务或数据集自适应的采样策略？

6. **与PatchEMG的关系深化**：EMGFlow与PatchEMG共享骨干但范式不同，两者在生成机制上的互补性是否可用于集成或级联框架？

## 原文 PDF

![[paperPDFs/arxiv_2026/EMGFlow_Robust_and_Efficient_Surface_Electromyography_Synthesis_via_Flow_Matching.pdf]]
