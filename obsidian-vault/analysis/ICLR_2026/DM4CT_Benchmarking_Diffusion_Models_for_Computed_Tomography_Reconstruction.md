---
title: "DM4CT: Benchmarking Diffusion Models for Computed Tomography Reconstruction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DM4CT_Benchmarking_Diffusion_Models_for_Computed_Tomography_Reconstruction.pdf
project_link: null
code_link: https://github.com/DM4CT/DM4CT
openreview_forum_id: YE5scJekg5
aliases:
- DM4CT
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "数据一致性步骤中的步长参数η（或优化迭代次数），它直接影响先验与测量数据之间的平衡，是决定扩散模型重建成功与否的关键控制变量。"
primary_logic: "通过系统的基准测试，揭示了扩散模型在CT重建中的三个关键发现：(1) 数据一致性策略（梯度引导 vs 优化步骤 vs 伪逆）决定了先验引入的程度与重建保真度的权衡；(2) 早期中止训练的扩散模型即可提供强大的结构先验，大幅降低训练成本；(3) 实际CT中的噪声模型不匹配会严重削弱扩散方法的性能，而像素空间扩散在效率和鲁棒性上优于潜在空间扩散。"
claims:
- "扩散方法在PSNR/SSIM上普遍优于经典和MBIR方法，但往往不及监督学习方法SwinIR。"
- "数据一致性步长η增加最初提升性能，但过大导致模型崩溃"
- "基于梯度引导的方法（如DPS）在噪声测量下比强制数据一致性的优化步骤方法（如ReSample）产生更高质量的视觉结果"
- "早期阶段（25 epoch）训练的扩散模型重建精度（PSNR 30.68/0.75）优于完全训练模型（28.71/0.73）"
---

# DM4CT: Benchmarking Diffusion Models for Computed Tomography Reconstruction

> [!tip] 核心洞察
> 通过系统的基准测试，揭示了扩散模型在CT重建中的三个关键发现：(1) 数据一致性策略（梯度引导 vs 优化步骤 vs 伪逆）决定了先验引入的程度与重建保真度的权衡；(2) 早期中止训练的扩散模型即可提供强大的结构先验，大幅降低训练成本；(3) 实际CT中的噪声模型不匹配会严重削弱扩散方法的性能，而像素空间扩散在效率和鲁棒性上优于潜在空间扩散。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DM4CT: 计算机断层扫描重建的扩散模型基准测试 |
| 英文题名 | DM4CT: Benchmarking Diffusion Models for Computed Tomography Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=YE5scJekg5) · [GitHub](https://github.com/DM4CT/DM4CT) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | DM4CT |
| Dataset | Medical CT (config i: 40 projs, noise-free), Medical CT (config iii: 80 projs, stronger noise), Industrial CT (config ii: 20 projs, mild noise), Real-world Synchrotron CT (60 projs) |

> [!tip] 效果简介
> - Medical CT (config i: 40 projs, noise-free) 上，PSNR / SSIM 为 DDS 31.43 / 0.84，对比 SIRT 30.40 / 0.80，变化 +1.03 / +0.04。
> - Medical CT (config iii: 80 projs, stronger noise) 上，PSNR / SSIM 为 DPS 27.81 / 0.74，对比 SIRT 24.48 / 0.32，变化 +3.33 / +0.42。
> - Industrial CT (config ii: 20 projs, mild noise) 上，PSNR / SSIM 为 SwinIR 19.51 / 0.55，对比 SIRT 16.67 / 0.30，变化 +2.84 / +0.25。

## 概要

计算机断层扫描（CT）重建本质上是一个线性逆问题 $y = A x$，但实际成像中噪声、伪影和非线性预处理使该问题高度病态。扩散模型作为强大的生成先验，近年来在CT重建中展现出显著潜力，然而其方法设计空间碎片化——不同方法在数据一致性策略、先验引入方式和操作空间上差异巨大，缺乏统一的系统性理解。

**DM4CT** 构建了首个面向CT重建的扩散模型基准框架，在医学CT、工业CT和真实同步辐射CT三个数据集上，系统评估了涵盖像素空间与潜在空间、梯度引导与优化步骤、伪逆引导与变分推断等策略的十余种扩散方法，并与经典重建（FBP、SIRT）、模型驱动迭代重建（ADMM-PDTV、FISTA-SBTV）、隐式先验（DIP、INR）和监督学习（SwinIR）等基线方法进行全面对比。

该基准揭示了三个核心发现：

1. **数据一致性策略决定先验-保真度权衡**。梯度引导方法（如DPS）在噪声测量下产生更高质量的视觉结果，而强制数据一致性的优化步骤方法（如ReSample）在无噪声场景下表现更优。关键控制变量是数据一致性步长 $\eta$：适中值提升PSNR与数据拟合，过大则破坏反向扩散过程导致重建崩溃。

2. **早期中止训练的扩散模型即可提供强大结构先验**。仅训练25个epoch的像素扩散模型重建精度（PSNR 30.68/0.75）优于完全训练模型（28.71/0.73），表明先验强度而非生成质量是逆问题成功的关键，大幅降低训练成本。

3. **噪声模型不匹配严重削弱扩散方法性能**。当方法假设高斯似然而实际测量服从泊松噪声时（如DDS），重建质量显著下降。像素空间扩散在效率和鲁棒性上整体优于潜在空间扩散。

在定量结果上，扩散方法在PSNR/SSIM上普遍优于经典和MBIR方法，但往往不及监督学习方法SwinIR。例如在医学CT（40投影、无噪声）配置下，DDS达到31.43/0.84，而SIRT为30.40/0.80；在真实同步辐射数据（60投影）上，SwinIR以32.41/0.70领先，SIRT为27.92/0.52。

计算机断层扫描（CT）重建在数学上可建模为线性逆问题 $\pmb{y} = \pmb{A} \pmb{x}$，其中 $\pmb{A}$ 为系统矩阵。然而，实际CT成像面临远超理想线性模型的复杂挑战：泊松噪声经对数变换后变为非平稳高斯噪声、非线性预处理步骤、以及环形伪影和射束硬化等多种伪影，使得从欠定或含噪测量中恢复高质量图像变得极为困难。

传统重建方法长期依赖启发式先验，如全变分（TV）正则化，通过交替方向乘子法（**ADMM-PDTV**, Boyd et al., 2011）或快速迭代收缩阈值算法（**FISTA-SBTV**, Beck & Teboulle, 2009）求解。这些基于模型的迭代重建（MBIR）方法虽在特定条件下表现稳定，但其手工设计的先验表达能力有限，难以捕捉复杂的解剖结构纹理。近年来，数据驱动先验成为主流方向，包括利用配对稀疏/稠密视图图像训练深度网络的监督学习方法（如基于Transformer的**SwinIR**, Liang et al., 2021），以及不依赖训练数据的隐式先验方法，如深度图像先验（**DIP**, Ulyanov et al., 2018）和隐式神经表示（**INR/SIREN**, Sitzmann et al., 2020）。

扩散模型作为生成式先验在各类逆问题中展现出巨大潜力，多个方法已被快速引入CT重建领域。然而，这些方法在数据一致性策略、先验强度控制、噪声模型假设等方面存在显著差异，缺乏系统性的对比和诊断。具体而言，扩散方法引入测量条件的方式可大致分为三类：基于梯度的软约束引导（如**DPS**, Chung et al., 2023）、通过优化步骤强制数据一致性（如**DDS**, Chung et al., 2024 和 **ReSample**, Song et al., 2024）、以及基于伪逆残差的引导（如**MCG**, Chung et al., 2022 和 **PGDM**, Song et al., 2023a）。此外，部分方法在像素空间操作，另一些则采用潜在空间扩散（如**PSLD**, Rout et al., 2023），两者在计算效率和重建保真度上的权衡尚不明确。更重要的是，实际CT中的泊松噪声特性与多数扩散方法假设的高斯噪声模型之间存在根本性不匹配，这一差距对重建质量的影响程度缺乏定量评估。

上述方法碎片化与评估标准不统一的现状，构成了DM4CT基准测试的核心动机：在统一的CT正向模型和共享扩散先验下，系统揭示不同数据一致性策略、先验强度与噪声鲁棒性之间的因果机制，为扩散模型在医学与工业CT重建中的实际部署提供可操作的指导。

## 核心方法与创新机理

DM4CT 本身是一个系统性基准测试框架，而非提出单一重建算法。其核心创新在于**首次对扩散模型在 CT 重建中的设计空间进行系统解耦与实证分析**，揭示了三个关键洞察，这些洞察直接指向现有扩散重建方法的瓶颈与控制变量。

### 1. 数据一致性策略的分类与权衡机制

DM4CT 提出了一套统一的分类体系（Table 1），将现有扩散重建方法按数据一致性引入方式分为三类：**梯度引导（DC-grad）**、**优化步骤（DC-step）** 和**伪逆残差引导**。这一分类并非简单的罗列，而是揭示了先验强度与测量保真度之间的因果权衡：

- **DC-grad 方法**（如 **DPS**, Chung et al., 2023）通过梯度项 $\pmb{g}_t := \nabla_{\pmb{x}_t} \mathcal{L}(\pmb{A} \hat{\pmb{x}}_0 - \pmb{y})$ 以步长 $\eta$ 进行软约束引导，允许先验在零空间中贡献更多内容（Figure 4 中零空间能量占比更高），在噪声环境下反而产生更高质量的视觉结果（Figure 16, Section A.14）。
- **DC-step 方法**（如 **ReSample**, Song et al., 2024）通过 $\pmb{x}_t^* := \arg\min_{\pmb{x}_t} \mathcal{L}(\pmb{A} \pmb{x}_t - \pmb{y})$ 强制数据一致性，零空间分量更小，但在噪声测量下容易过拟合噪声。
- **步长 $\eta$ 是关键控制变量**：Figure 3a 显示，$\eta$ 增加初期同时提升 PSNR 和数据拟合，但过大时破坏反向扩散过程导致模型崩溃——这一定量关系是此前工作中未被系统刻画的。

### 2. 早期中止训练的扩散先验即足够强大

一个反直觉的发现是：**仅训练 25 epoch 的像素扩散模型，其 CT 重建 PSNR 达到 30.68/0.75，优于完全训练模型的 28.71/0.73**（Table 9, Figure 15）。这意味着扩散模型的**先验结构强度**而非**生成质量**是逆问题性能的决定因素。这一洞察大幅降低了扩散重建的训练成本，并暗示过拟合的扩散模型可能产生过于刚性的先验，反而限制了数据一致性的有效注入。

### 3. 噪声模型不匹配是实际部署的核心瓶颈

DDS 方法假设高斯似然（$\mathcal{L}(\pmb{x}) = \frac{\gamma}{2} \| \pmb{y} - \pmb{A} \pmb{x} \|_2^2 + \frac{1}{2} \| \pmb{x} - \hat{\pmb{x}}_0 \|_2^2$），在与实际泊松噪声不匹配时重建质量严重下降（Figure 11, Section A.9）。这揭示了当前扩散重建方法从仿真向真实场景迁移的根本障碍：对数变换后的泊松噪声方差为 $\mathrm{Var}(-\log(y/I_0)) \approx \frac{e^{(\pmb{A} \pmb{x})_i}}{I_0}$，具有信号依赖性，而高斯假设无法捕捉这一特性。论文进一步给出了使用逆协方差矩阵 $\pmb{R}$ 的通用化数据保真项作为解决方向，但未在基准中实现自适应噪声建模。

### 4. 像素空间扩散在效率与鲁棒性上优于潜在空间扩散

与自然图像领域的趋势不同，DM4CT 的实验表明：**像素空间扩散模型在重建时间和显存上普遍优于潜在空间方法**（Figure 7a），且潜在空间中通过解码器反向传播梯度进行数据一致性引导更为困难（Section 4）。这一发现对 CT 重建领域的模型设计选择具有直接的指导意义。

---

**需注意**：上述创新均为 DM4CT 基准测试所揭示的**领域洞察**，而非 DM4CT 自身提出的新算法。DM4CT 的贡献在于通过统一的实验平台（共享扩散主干、统一正向算子、公平超参数调优）使这些洞察得以被可靠地量化与比较。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_YE5scJekg5/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the DM4CT benchmark. (a) The reconstruction pipeline, where representative diffusion and baseline methods are applied to measured sinograms using the same forward model. (b) The datasets used in the benchmark, including two simulated CT datasets (medical and industrial) and one real-world dataset acquired at a synchrotron facility. (c) The five simulation configurations used to evaluate robustness to limited views, noise, and ring artifacts. Two example FBP reconstructions under noise and ring artifact conditions are shown. (d) The evaluation metrics, including both qualitative (visual) and quantitative (image quality and computational efficiency) criteria*

DM4CT 构建了一个统一的 CT 重建基准测试框架，其核心设计目标是在完全公平的条件下，系统比较不同扩散方法与经典/学习基线在稀疏角度和噪声条件下的重建能力。框架由四个紧密耦合的模块组成：数据集生成与采集、扩散模型主干训练、统一重建流水线，以及多维度评估协议。

### 框架总览

整个基准测试的运作逻辑如 Figure 1 所示：给定含噪正弦图（sinogram），所有方法共享同一个可微 CT 正向算子进行重建，随后在定性和定量两个层面进行统一评估。这种设计的核心优势在于消除了正向模型和先验模型差异对比较结果的干扰——所有扩散方法使用完全相同的像素空间或潜在空间扩散模型作为先验主干。

### 数据集构建

框架覆盖三类 CT 数据，构成从仿真到真实的递进验证链：

**模拟医学 CT** 基于 2016 Low Dose CT Grand Challenge 数据集，利用 Beer-Lambert 模型 $I^* = I_0 \exp(-\gamma \pmb{y}_0)$ 和泊松噪声模型 $\hat{I} \sim \mathrm{Poisson}(I_0 \exp(-\gamma \pmb{y}_0))$ 生成含噪投影，并通过 $\pmb{y} = -\frac{1}{\gamma} \log\left(\frac{\hat{I}}{I_0}\right)$ 恢复噪声测量。环形伪影则通过在部分探测器列加入固定模式高斯噪声 $\pmb{y} = \pmb{y}_0 + \pmb{M} \cdot \mathcal{N}(\mathbf{0}, \sigma^2 \pmb{I})$ 来模拟。

**模拟工业 CT** 使用 LoDoInd 数据集，包含 15 种材料的 3500 张切片（3000 训练/500 测试），采用与医学数据相同的仿真管线。

**真实同步辐射 CT** 在同步辐射设施中对岩石样本进行高分辨率平行束扫描获取，提供了真实实验条件下的噪声、伪影和系统不完美性，是验证仿真结论泛化能力的关键环节。

### 扩散模型主干

每个数据集分别训练一个像素空间扩散模型和一个潜在空间扩散模型，作为所有扩散方法的共享先验。潜在空间模型采用 VQ-VAE 将图像压缩到低维空间后再训练扩散模型。这种共享主干的设计确保了不同扩散方法之间的差异仅来自数据一致性策略，而非先验质量的不同。

### 统一重建流水线

所有方法通过基于 ASTRA Toolbox 构建的 PyTorch 兼容可微 CT 正向算子进行重建。输入为含噪正弦图，输出为重建切片，中间通过统一的线性值域映射 $v_{\mathrm{tar}} = a \cdot v_{\mathrm{norm}} + b$ 对齐训练和测试图像的值域。方法特定的超参数通过网格搜索在留出的 10 张训练图像上以 MSE 最小化为目标进行调优（搜索范围与选定值详见 Table 15）。

### 评估协议

评估从四个维度展开：
- **重建精度**：PSNR 和 SSIM 作为主要指标，LPIPS 衡量感知质量
- **数据一致性**：通过 $L_2$ 范数 $\lVert A \hat{\pmb{x}} - \widetilde{\pmb{y}} \rVert_2$ 衡量重建投影与含噪测量的拟合程度
- **先验-数据平衡**：利用范围-零空间分解 $\pmb{x} = \pmb{A}^{\dagger} \pmb{A} \pmb{x} + (\pmb{I} - \pmb{A}^{\dagger} \pmb{A}) \pmb{x}$ 将重建分解为数据一致的范围分量和先验驱动的零空间分量，揭示不同策略引入先验信息的程度
- **计算效率**：记录重建时间和 GPU 显存占用

### 方法分类体系

Table 1 将 11 种扩散方法按两个维度组织：**实现技术**（像素空间 vs 潜在空间、DDPM vs DDIM 采样）和**重建策略**（数据一致性梯度引导 DC-grad、优化步骤 DC-step、伪逆引导、即插即用先验、变分贝叶斯）。这一分类体系揭示了方法设计的核心分叉点——如何在反向扩散过程中引入测量信息，直接决定了先验强度与数据保真度之间的权衡。

### 3.1 CT测量模型与逆问题形式化

CT重建在理论上是一个线性逆问题，其正向过程由Beer-Lambert定律描述。经过对数变换后，测量过程可形式化为线性系统：

$$\pmb{y} = \pmb{A} \pmb{x}$$

其中 $\pmb{y}$ 为含噪正弦图（投影数据），$\pmb{A}$ 为系统矩阵（编码投影几何与线积分），$\pmb{x}$ 为待重建图像。实际CT中，光子计数服从泊松噪声模型：

$$\hat{I} \sim \mathrm{Poisson}(I_0 \exp(-\gamma \pmb{y}_0))$$

从含噪光子计数恢复噪声投影的过程为：

$$\pmb{y} = -\frac{1}{\gamma} \log\left(\frac{\hat{I}}{I_0}\right)$$

该对数变换使噪声特性复杂化，是扩散方法在实际数据中面临噪声模型不匹配问题的根源（见Section A.9中DDS在泊松噪声下的退化分析）。

---

### 3.2 扩散模型作为先验

DM4CT基准采用方差保持随机微分方程（VP-SDE）描述扩散过程。无条件正向扩散为：

$$d \pmb{x} = -\frac{\beta_t}{2} \pmb{x} + \sqrt{\beta_t} d\pmb{w}$$

对应的无条件反向去噪SDE为：

$$d \pmb{x} = \left[-\frac{\beta_t}{2} \pmb{x} - \beta_t \nabla_{\pmb{x}_t} \log p(\pmb{x}_t)\right] dt + \sqrt{\beta_t} d\pmb{\bar{w}}$$

其中 $\nabla_{\pmb{x}_t} \log p(\pmb{x}_t)$ 为得分函数，由扩散模型学习。为将扩散先验用于CT重建，需在反向过程中引入测量条件 $\pmb{y}$，得到条件反向SDE：

$$d \pmb{x} = \left[-\frac{\beta_t}{2} \pmb{x} - \beta_t \left(\nabla_{\pmb{x}_t} \log p(\pmb{x}_t) + \nabla_{\pmb{x}_t} \log p(\pmb{y}|\pmb{x}_t)\right)\right] dt + \sqrt{\beta_t} d\pmb{\bar{w}}$$

核心挑战在于 $\nabla_{\pmb{x}_t} \log p(\pmb{y}|\pmb{x}_t)$ 不可直接计算，因为 $\pmb{x}_t$ 是含噪潜变量。所有扩散重建方法的本质差异在于如何近似该项，DM4CT的**核心洞察**是：这一近似的实现策略直接决定了先验强度与测量一致性之间的平衡，是扩散模型在CT重建中成功与否的控制变量。

---

### 3.3 数据一致性策略分类

DM4CT将所评测的扩散方法按数据一致性实现策略分为三类（Table 1），其关键公式如下：

#### 3.3.1 梯度引导（DC-grad）

通过Tweedie公式从 $\pmb{x}_t$ 估计干净图像 $\hat{\pmb{x}}_0(\pmb{x}_t)$，然后计算数据拟合损失对当前迭代的梯度：

$$\pmb{g}_t := \nabla_{\pmb{x}_t} \mathcal{L}(\pmb{A} \hat{\pmb{x}}_0 - \pmb{y})$$

利用步长 $\eta$ 进行引导更新：

$$\pmb{x}_t \gets \pmb{x}_t - \eta \pmb{g}_t$$

代表方法：**DPS**（Chung et al., 2023）。该方法施加软约束，允许更多零空间内容由先验填充（Figure 4）。$\eta$ 是核心控制变量：增大 $\eta$ 最初同时提升PSNR和数据拟合，但过大则破坏反向扩散过程导致模型崩溃（Figure 3a）。

#### 3.3.2 优化步骤（DC-step）

在去噪迭代间插入完整的数据一致性优化步骤，直接强制测量一致性：

$$\pmb{x}_t^* := \arg\min_{\pmb{x}_t} \mathcal{L}(\pmb{A} \pmb{x}_t - \pmb{y})$$

代表方法：**DDS**（Chung et al., 2024）、**ReSample**（Song et al., 2024）、**DMPlug**（Wang et al., 2024）。DDS的具体目标函数为：

$$\mathcal{L}(\pmb{x}) = \frac{\gamma}{2} \| \pmb{y} - \pmb{A} \pmb{x} \|_2^2 + \frac{1}{2} \| \pmb{x} - \hat{\pmb{x}}_0 \|_2^2$$

通过共轭梯度求解正规方程：

$$(\gamma \pmb{A}^T \pmb{A} + \pmb{I}) \pmb{x} = \hat{\pmb{x}}_0 + \gamma \pmb{A}^T \pmb{y}$$

DC-step方法强制更严格的数据一致性，导致零空间分量更小（Figure 4），但在噪声条件下可能过拟合噪声（Figure 16）。

#### 3.3.3 伪逆引导

使用伪逆残差替代直接数据拟合梯度：

$$\pmb{g}_t := \nabla_{\pmb{x}_t} \mathcal{L}(\pmb{A}^{\dag} \pmb{A} \hat{\pmb{x}}_0 - \pmb{A}^{\dag} \pmb{y}), \quad \pmb{x}_t \gets \pmb{x}_t - \eta \pmb{g}_t$$

其中 $\pmb{A}^{\dag}$ 为Moore-Penrose伪逆，在CT中用FBP或SIRT近似。代表方法：**MCG**（Chung et al., 2022）、**PGDM**（Song et al., 2023a）。

---

### 3.4 通用化数据保真项

为处理噪声模型不匹配问题，DDS可扩展为带逆噪声协方差矩阵的通用形式：

$$\mathcal{L}(\pmb{x}) = \frac{\gamma}{2} (\pmb{y} - \pmb{A} \pmb{x})^T \pmb{R} (\pmb{y} - \pmb{A} \pmb{x}) + \frac{1}{2} \| \pmb{x} - \hat{\pmb{x}}_0 \|_2^2$$

对数变换后泊松噪声方差的近似为：

$$\mathrm{Var}(-\log(y/I_0)) \approx \frac{e^{(\pmb{A} \pmb{x})_i}}{I_0}$$

当 $\pmb{R}$ 设为单位矩阵（即假设高斯噪声）而实际为泊松噪声时，DDS重建质量严重下降（Figure 11），这是扩散方法在实际CT数据中性能退化的关键瓶颈。

---

### 3.5 范围-零空间分解

为量化先验与数据一致性的贡献，采用信号分解：

$$\pmb{x} = \pmb{A}^{\dagger} \pmb{A} \pmb{x} + (\pmb{I} - \pmb{A}^{\dagger} \pmb{A}) \pmb{x}$$

其中范围分量由测量数据约束，零空间分量完全由先验填充。零空间分量的相对L2能量百分比直接反映先验引入程度——DC-grad方法（DPS）通常产生更大零空间分量，DC-step方法（ReSample）则更小（Figure 4, Figure 16）。

---

### 3.6 共享扩散模型主干

为消除先验差异对比较的影响，每个数据集分别训练一个像素空间和一个潜在空间扩散模型，作为所有扩散方法的共享主干（Section 3.3）。这一设计确保了方法间性能差异仅源于数据一致性策略，而非先验质量。消融实验进一步揭示：早期中止训练（25 epoch）的扩散模型重建精度（PSNR 30.68/0.75）优于完全训练模型（28.71/0.73），表明**先验强度而非生成质量**是逆问题中的关键因素（Table 9）。

## 实验与关键发现

### 整体性能格局：扩散方法在定量指标上的优势与上限

Table 2 汇总了医学CT、工业CT和同步辐射CT三种数据集在多种稀疏角度和噪声配置下的重建PSNR/SSIM。核心结论如下：

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_YE5scJekg5/figures/003_Table_2.jpg]]
*Table 2: Reconstruction performance (PSNR / SSIM) of different methods under various configurations for medical, industrial and synchrotron CT datasets. The highest score among diffusion-based methods is shown in bold, and the second highest is underlined. A dash (–) indicates that the method exceeded the 40 GB GPU memory limit for single-slice reconstruction and is therefore not executed*

**扩散方法普遍优于经典重建和MBIR方法，但往往不及全监督学习方法SwinIR。** 在医学CT无噪声配置（40投影）下，扩散方法中最优的DDS达到31.43/0.84，超过SIRT（30.40/0.80）和ADMM-PDTV（30.92/0.82），但低于SwinIR（32.45/0.88）和INR（33.21/0.86）。在强噪声配置（80投影）下，扩散方法的相对优势扩大：DPS取得27.81/0.74，相比SIRT的24.48/0.32提升显著（+3.33/+0.42），但仍不及SwinIR的29.40/0.80。

**真实世界数据的性能普遍低于仿真数据。** 在同步辐射CT（60投影）上，最优扩散方法MCG仅取得27.43/0.57，明显低于SwinIR的32.41/0.70。这一差距揭示了扩散模型在面临真实测量中的复杂噪声特性、非线性预处理和系统误差时的退化——这是后文将深入分析的“噪声模型不匹配”问题的直接体现。

**像素空间扩散在效率和鲁棒性上优于潜在空间扩散。** 从Table 2的“–”标记（超出40 GB显存）来看，潜在空间方法（PSLD、Resample、DiffStateGrad）在单切片重建中频繁触及显存上限，而像素空间方法普遍可运行。Figure 7a进一步量化了这一差距：像素扩散方法的重建时间和显存开销整体低于潜在扩散方法，唯一的例外是DMPlug，尽管基于像素空间，其显存消耗反而是所有方法中最高的。

### 先验与数据一致性的核心权衡：步长η的调控作用

Figure 3a揭示了扩散CT重建中最关键的调控变量——数据一致性步长η的行为。以DPS方法为例，当η从零开始增加时，PSNR和数据拟合L2范数同时改善，表明适度的数据一致性引导有助于纠正去噪过程中的偏差。然而，当η超过某个临界值后，PSNR急剧下降，重建图像从“先验主导”过渡到“噪声主导”，最终导致反向扩散过程崩溃。这一现象的本质在于：过大的η破坏了去噪步骤的马尔可夫结构，使采样轨迹偏离学习到的数据流形。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_YE5scJekg5/figures/005_Figure_3.jpg]]
*Figure 3: (a) Impact of data consistency step size η (Equation 7) on PSNR and data fit in DPS. Moderate values improve both, while large η disrupts denoising and causes collapse. Visual examples in the plot highlight the transition from prior-dominated to noise-dominated reconstructions. (b) Mean and standard deviation of ten MCG reconstructions conditioned on the same real measurement. Note that the real measurement used in (b) is different from the one used for (a)*

**这一发现的实际意义是：扩散重建的成功高度依赖于η的精细调优，且最优值随噪声水平和稀疏度变化。** 在DM4CT中，所有方法的超参数均通过留出训练集上的网格搜索确定（Table 15），但最优性仅保证在搜索范围内。

### 数据一致性策略的分化：梯度引导 vs 优化步骤 vs 伪逆

Figure 4通过范围-零空间分解（range-null space decomposition）揭示了不同数据一致性策略的根本差异。将重建信号分解为$\pmb{x} = \pmb{A}^{\dagger}\pmb{A}\pmb{x} + (\pmb{I} - \pmb{A}^{\dagger}\pmb{A})\pmb{x}$，范围分量对应测量约束的部分，零空间分量对应先验引入的内容。

**基于梯度引导的方法（DC-grad，如DPS）施加软约束，允许更多零空间内容。** 在Figure 4中，DPS的零空间能量占比显著高于其他方法，表明其重建中保留了更多由扩散先验驱动的结构细节。**相比之下，基于优化步骤的方法（DC-step，如ReSample）严格强制数据一致性，零空间分量较小。** 这种差异在视觉上表现为：DPS倾向于产生更自然的纹理但可能偏离测量约束，而ReSample更忠实于投影数据但可能丢失先验带来的细节增强。

在噪声测量条件下，这一差异进一步放大。Figure 16（工业数据，噪声+环形伪影）显示，DPS在噪声下仍能保持合理的零空间结构，而强制数据一致性的方法（如ReSample）在噪声情况下容易将噪声“刻入”重建，导致范围分量中出现伪影。**这解释了为什么基于梯度引导的方法在噪声测量下产生更高质量的视觉结果：软约束机制天然具有抗噪声过拟合的能力。**

### 训练阶段的反直觉发现：早期模型优于收敛模型

Table 9和Figure 15呈现了一个反直觉的结果：**训练仅25 epoch的像素扩散模型在CT重建中达到PSNR 30.68/0.75，优于训练至收敛的模型（28.71/0.73）和中期模型（28.46/0.72）。** 然而，从无条件生成质量来看，后期模型的生成样本明显更逼真（Figure 15）。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_YE5scJekg5/figures/027_Table_9.jpg]]
*Table 9: Comparison of CT reconstruction using early stage, mid stage and final stage trained pixel diffusion models*

这一“生成质量与重建质量脱钩”的现象指向一个深层机理：**扩散模型在逆问题中充当结构化先验，其有效性取决于先验强度而非生成逼真度。** 早期模型学习的分布更宽泛、模式覆盖更全面，在数据一致性约束下更容易被“引导”到与测量兼容的解；而过度训练的模型分布过于尖锐，当测量约束与学习分布不一致时，采样过程难以找到同时满足两者的折中点。

**这一发现具有重要的实践意义：对于CT重建等逆问题应用，无需训练扩散模型至完全收敛，大幅降低了训练成本。** 结合Figure 7b中扩散模型训练耗时（像素扩散约12小时，潜在扩散因需训练VQ-VAE而更久），早期中止策略可节省50%以上的训练时间。

### 噪声模型不匹配：扩散方法的致命弱点

Figure 11（Section A.9）揭示了扩散方法在实际CT中最严重的失效模式。实验构造了高斯噪声和泊松噪声两种场景，使FBP基线达到相近的PSNR/SSIM。DDS在高斯噪声下能够恢复精细结构，但在泊松噪声下重建质量严重退化——无论是视觉细节还是定量指标。

**根源在于DDS的数据保真项显式假设了高斯似然**，其目标函数为$\mathcal{L}(\pmb{x}) = \frac{\gamma}{2} \| \pmb{y} - \pmb{A}\pmb{x} \|_2^2 + \frac{1}{2} \| \pmb{x} - \hat{\pmb{x}}_0 \|_2^2$。当实际噪声为泊松分布（如CT中光子计数经对数变换后）时，高斯假设导致数据一致性步骤将泊松噪声的异方差特性错误地视为均匀误差，从而在低计数区域过度拟合噪声。

**这一发现解释了真实同步辐射数据上扩散方法性能下降的原因**（Table 2中扩散方法与SwinIR的差距远大于仿真数据），也指出了扩散CT重建走向临床部署的核心障碍：需要显式建模实际噪声特性。Section A.9给出了使用逆噪声协方差矩阵$\pmb{R}$的广义数据保真项$\mathcal{L}(\pmb{x}) = \frac{\gamma}{2} (\pmb{y} - \pmb{A}\pmb{x})^T \pmb{R} (\pmb{y} - \pmb{A}\pmb{x}) + \frac{1}{2} \| \pmb{x} - \hat{\pmb{x}}_0 \|_2^2$，以及对数变换后泊松方差的近似$\mathrm{Var}(-\log(y/I_0)) \approx e^{(\pmb{A}\pmb{x})_i}/I_0$，但这一方向尚未在基准测试中系统评估。

### 优化迭代次数的消融：像素与潜在空间的非对称行为

Table 8探索了像素空间和潜在空间优化迭代次数对重建质量的影响。**在高噪声条件下，增加潜在空间优化迭代（200次）比像素空间迭代（100次）更能提升PSNR/SSIM**（28.40/0.78 vs 低迭代配置）。Figure 14展示了这一行为的视觉对应：过少的迭代导致过度平滑，过多的迭代则导致噪声过拟合，最优设置通常出现在两种状态的过渡区域。

这一非对称性源于潜在空间扩散的结构特点：VQ-VAE编码器将图像压缩到低维潜在空间，优化在该空间中进行时，解码器的平滑效应天然提供了一定的正则化，允许更多优化迭代而不立即过拟合噪声。然而，这也意味着潜在空间方法在无噪声或少噪声场景下可能因过度正则化而丢失细节——这是Figure 5中潜在方法在无噪声配置下表现不如像素方法的原因之一。

### 计算效率的实用考量

Figure 7从重建和训练两个维度量化了计算开销。**在重建阶段**，像素扩散方法（除DMPlug外）的重建时间集中在30-120秒/切片，显存消耗在10-25 GB；潜在扩散方法普遍需要更长时间（60-200秒）和更多显存（20-40+ GB）。DMPlug的异常高显存消耗源于其Plug-and-Play框架中维护的额外优化状态。**在训练阶段**，潜在扩散的总训练成本显著高于像素扩散，因为VQ-VAE编码器的训练时间（约12小时）已与完整像素扩散模型的训练时间相当，还需额外训练潜在空间扩散模型。

### 语义分割的下游任务评估

Table 6使用SAM对医学CT重建结果进行语义分割，以Dice/IoU评估下游任务影响。SIRT取得最高的分割精度（0.819/0.735），扩散方法中DDS（0.692/0.618）和DPS（0.691/0.619）表现居中。这一结果提示：**更高的PSNR/SSIM并不直接转化为更好的下游任务性能**——SIRT虽然在PSNR上低于扩散方法，但其重建的边界一致性可能更适合分割模型。Figure 12的可视化确认了不同重建方法在解剖结构边界上的差异如何影响分割掩码质量。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_YE5scJekg5/figures/021_Table_6.jpg]]
*Table 6: Segmentation performance (Dice / IoU) on the medical dataset with 40 projections*

### 局限性总结

1. **泛化性未经验证**：所有结论基于三个特定数据集和固定扫描几何（平行束/扇束），对其他CT模态（锥束、螺旋CT）和探测器配置的适用性未知。
2. **超参数敏感性**：重建质量对η、优化迭代次数等超参数高度敏感，网格搜索仅保证局部最优。
3. **评估维度局限**：以PSNR/SSIM/LPIPS为主，缺少任务驱动的临床指标。
4. **真实数据覆盖不足**：仅包含岩石样本，未涉及活体组织的运动伪影和复杂密度分布。
5. **方法覆盖缺口**：未包含流匹配、一致性模型等新兴生成框架，也未系统评估噪声自适应策略。



![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_YE5scJekg5/figures/015_Table_4.jpg]]
*Table 4: Acquisition parameters of the real-world synchrotron CT dataset used in this benchmark. Both rocks are scanned using the same setup under parallel-beam geometry*

## 定位与知识库关联

### 1. 方法分类学与核心策略分化

DM4CT 将当前扩散模型驱动的 CT 重建方法归纳为四类核心策略（Table 1），这一分类构成了理解方法间差异的关键框架：

**数据一致性梯度引导（DC-grad）**：以 **DPS**（Chung et al., CVPR 2023）和 **PSLD**（Rout et al., 2023）为代表。这类方法在反向去噪的每一步中，基于估计的干净图像 $\hat{\pmb{x}}_0$ 计算数据保真损失对当前迭代 $\pmb{x}_t$ 的梯度 $\pmb{g}_t := \nabla_{\pmb{x}_t} \mathcal{L}(\pmb{A} \hat{\pmb{x}}_0 - \pmb{y})$，然后以步长 $\eta$ 进行更新 $\pmb{x}_t \gets \pmb{x}_t - \eta \pmb{g}_t$。其核心特征是施加“软约束”——先验与数据一致性通过梯度项在同一个反向扩散步骤中融合，而非分离处理。

**数据一致性优化步骤（DC-step）**：以 **DDS**（Chung et al., 2024）、**Resample**（Song et al., 2024）和 **DMPlug**（Wang et al., 2024）为代表。这类方法在去噪步骤之间插入完整的数据一致性优化子问题 $\pmb{x}_t^* := \arg\min_{\pmb{x}_t} \mathcal{L}(\pmb{A} \pmb{x}_t - \pmb{y})$，通过共轭梯度等方法求解。与 DC-grad 相比，DC-step 强制更严格的数据拟合，导致重建中零空间分量（由先验驱动的内容）的能量占比显著更小（Figure 4）。DDS 的联合目标函数为 $\mathcal{L}(\pmb{x}) = \frac{\gamma}{2} \| \pmb{y} - \pmb{A} \pmb{x} \|_2^2 + \frac{1}{2} \| \pmb{x} - \hat{\pmb{x}}_0 \|_2^2$，通过求解正规方程 $(\gamma \pmb{A}^T \pmb{A} + \pmb{I}) \pmb{x} = \hat{\pmb{x}}_0 + \gamma \pmb{A}^T \pmb{y}$ 实现。

**伪逆引导**：以 **MCG**（Chung et al., 2022）和 **PGDM**（Song et al., 2023a）为代表。这类方法不直接在测量域计算梯度，而是计算伪逆重建残差 $\pmb{g}_t := \nabla_{\pmb{x}_t} \mathcal{L}(\pmb{A}^{\dag} \pmb{A} \hat{\pmb{x}}_0 - \pmb{A}^{\dag} \pmb{y})$。在 CT 中，$\pmb{A}^{\dag}$ 通过 FBP 或 SIRT 近似实现。该策略的核心优势在于将测量域误差映射回图像域，缓解了直接梯度引导中可能出现的数值不稳定性。

**变分贝叶斯方法**：以 **Reddiff**（Mardani et al., 2024）和 **HybridReg**（Dou et al., 2025）为代表。这类方法将后验分布 $p(\pmb{x}|\pmb{y})$ 近似为参数化高斯分布，通过梯度下降同时优化数据一致性和先验匹配。

### 2. 像素空间与潜在空间的根本分歧

DM4CT 揭示了一个关键发现：**像素空间扩散在 CT 重建中普遍优于潜在空间扩散**，这与生成任务中的趋势相反。其因果机制在于：

1. **梯度传播障碍**：潜在扩散模型（如 PSLD、Resample）的数据一致性梯度必须通过 VQ-VAE 解码器反向传播，该解码器本身可能引入高频信息的不可逆损失（Section 4, Figure 5）。
2. **自编码器质量瓶颈**：论文对自然图像预训练编码器（SDXL AutoencoderKL）进行微调的实验（Table 7）表明，即使微调后的自编码器重建质量有所提升，其 CT 重建性能仍不及专门设计的 VQ-VAE。这说明 CT 灰度图像的统计特性与自然图像存在本质差异，通用编码器难以有效压缩。
3. **计算效率倒挂**：尽管潜在扩散在训练时因低维潜在空间而更快，但其重建阶段因梯度需通过解码器传播而更慢且更耗内存（Figure 7）。唯一的例外是 DMPlug，尽管是像素方法，但其 Plug-and-Play 框架的内存消耗最大。

### 3. 与经典方法和监督学习的定位关系

**相对经典方法的优势与局限**：扩散方法在 PSNR/SSIM 上普遍优于 FBP、SIRT 以及基于 TV 的 MBIR 方法（ADMM-PDTV、FISTA-SBTV），尤其在强噪声和稀疏角度条件下优势显著（Table 2, config iii: DPS 27.81/0.74 vs. SIRT 24.48/0.32）。然而，当投影角度充足且噪声较低时，性能差距缩小（Figure 6），说明扩散先验的核心价值在于补偿严重欠定条件下的信息缺失。

**相对监督学习的差距**：SwinIR（Liang et al., 2021）在多数配置下保持最高 PSNR/SSIM（如 medical config i: 32.45/0.88），这源于其端到端的监督训练直接学习从稀疏重建到全剂量参考的映射。扩散方法的无监督先验无法匹敌这种任务特定的优化。但值得注意的是，SwinIR 需要成对训练数据，而扩散模型仅需干净图像即可训练先验，这在真实世界场景中具有数据获取优势。

**相对隐式先验方法的互补性**：DIP（Ulyanov et al., 2018）和 INR（Sitzmann et al., 2020）在特定配置下表现突出（如 INR 在 medical config i 达到 33.21/0.86），但其性能高度依赖初始化和优化过程，且每张图像需独立优化，推理效率远低于扩散方法。论文的开放问题之一正是探索扩散先验与 INR 的结合，以兼顾结构保真度和推理效率。

### 4. 关键控制变量与失效模式

**步长 $\eta$ 的临界性**：数据一致性步长 $\eta$ 是决定扩散重建成败的核心控制变量。Figure 3a 揭示了其非单调效应：适中的 $\eta$ 同时提升 PSNR 和数据拟合，但过大的 $\eta$ 会破坏反向扩散的去噪动力学，导致模型崩溃——重建从“先验主导”跳变至“噪声主导”。这一发现表明，扩散重建本质上是一个先验强度与数据一致性的精细平衡问题。

**噪声模型不匹配的脆弱性**：DDS 假设高斯似然，当其应用于实际泊松噪声的 CT 数据时，重建质量严重下降（Figure 11, Section A.9）。论文推导了广义数据保真项 $\mathcal{L}(\pmb{x}) = \frac{\gamma}{2} (\pmb{y} - \pmb{A} \pmb{x})^T \pmb{R} (\pmb{y} - \pmb{A} \pmb{x}) + \frac{1}{2} \| \pmb{x} - \hat{\pmb{x}}_0 \|_2^2$，其中 $\pmb{R}$ 为逆噪声协方差矩阵，并给出了对数变换后泊松方差的近似 $\mathrm{Var}(-\log(y/I_0)) \approx \frac{e^{(\pmb{A} \pmb{x})_i}}{I_0}$。这一分析直接指向开放问题：显式泊松噪声建模的扩散方法能否显著提升真实 CT 性能。

**训练阶段的悖论**：Table 9 揭示了一个反直觉现象——仅训练 25 epoch 的早期扩散模型（PSNR 30.68/0.75）优于完全训练模型（28.71/0.73）。Figure 15 显示，完全训练模型虽能生成更逼真的无条件样本，但其先验在逆问题中反而过于刚性，限制了数据一致性步骤的有效调整。这表明**先验的“强度”而非生成质量**是决定重建成功的关键，过拟合的先验会与测量信息产生对抗。

### 5. 适用边界与未解决问题

**已验证的适用边界**：
- 二维平行束/扇束几何的稀疏角度重建（20-80 投影），在医学 CT、工业 CT 和同步辐射岩石成像三个领域得到验证。
- 噪声条件涵盖无噪声、轻度泊松噪声（$I_0=10^5$）、强泊松噪声（$I_0=10^4$）及环形伪影。
- 所有方法共享相同的扩散模型主干和可微 CT 正向算子（基于 ASTRA Toolbox），消除了先验差异和系统矩阵实现差异的混淆。

**明确的局限与未覆盖场景**：
1. **几何泛化性未验证**：所有实验限于二维切片和扇束/平行束几何，锥束 CT、螺旋 CT 及不同探测器配置下的性能未知。
2. **活体组织缺失**：真实世界数据集仅为岩石样本，缺乏活体组织的复杂密度变化、运动伪影和散射效应。
3. **任务驱动评估缺失**：评估指标限于 PSNR/SSIM/LPIPS，缺少临床任务指标（如病变检测率、诊断准确率）。Table 6 虽然展示了基于 SAM 的语义分割结果，但仅为初步探索。
4. **超参数敏感性**：所有方法的关键超参数通过网格搜索在留出训练集上优化（Table 15），但扩散模型的随机性意味着单次运行的最优参数可能不具有鲁棒性。
5. **更先进生成模型的缺失**：未涵盖流匹配模型（如 FlowDPS）、一致性模型等新兴生成框架，这些方法可能在效率和质量上突破当前扩散方法的瓶颈。

**开放问题**：
- 如何设计 CT 灰度图像专用的自编码器，以缩小潜在扩散与像素扩散之间的性能差距？
- 训练至过拟合的扩散模型为何在逆问题中性能下降——其深层机理是模式坍塌、先验过度约束，还是后验采样的退火路径偏移？
- 噪声模型自适应的扩散方法（如对泊松噪声显式建模）能否在实际临床 CT 数据上实现性能跃升？
- 扩散先验与隐式神经表示（INR）的结合是否能同时利用扩散的强先验和 INR 的结构连续性，提升稀疏角度下的细节保真度？

## 原文 PDF

![[paperPDFs/ICLR_2026/DM4CT_Benchmarking_Diffusion_Models_for_Computed_Tomography_Reconstruction.pdf]]
