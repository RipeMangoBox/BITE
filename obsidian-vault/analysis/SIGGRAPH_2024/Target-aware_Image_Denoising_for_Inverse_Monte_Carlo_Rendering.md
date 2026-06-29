---
title: Target-aware Image Denoising for Inverse Monte Carlo Rendering
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Target_aware_Image_Denoising_for_Inverse_Monte_Carlo_Rendering.pdf
project_link: null
code_link: "https://github.com/CGLab-GIST/target-aware-denoising"
aliases:
- TAID
- TAIDIMCR
tags:
- SIGGRAPH_2024
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 去噪权重的计算策略：从仅依赖场景内部G-buffer（如位置、法线、反照率、深度）的交叉双边权重，转变为融合目标图像信息的目标感知权重——通过目标图像像素颜色的对数变换差异构建相似度核，并利用局部线性回归动态调整权重，使得去噪在降低噪声的同时，能自适应地保留与目标图像一致的细节结构。
primary_logic: 将“目标图像”作为逆渲染特有的先验知识引入图像去噪过程，利用目标图像的颜色变化指导去噪权重的分配：在局部窗口内用目标颜色的线性函数近似未知的真实图像，通过加权最小二乘回归求解去噪结果。这一策略使得去噪器在图像空间梯度上实现边缘保持的平滑，从而在加速逆渲染优化的同时，避免了收敛到过度平滑的局部极小。
claims:
- 在材质估计（Veach-ajar场景）、体积参数推断（Janga场景）等多种逆渲染任务中，本文方法相比不使用去噪的基线，显著降低了L1误差（例如Veach-ajar场景误差降低11.46倍，Janga场景降低3.96倍）。
- 消融实验（Table 1）表明，在4个样本每像素（spp）下，本文方法的L1误差（0.00224）已低于基线在256 spp下的误差（0.00359），证明去噪能够大幅减少所需样本数及优化时间。
- 定量偏差分析（Fig. 9）显示，对于非L2损失（如L1损失），本文去噪器产生的图像空间梯度估计偏差远小于基线，这解释了为何我们的方法能够避免直接使用现有去噪器引起的细节丢失和过度模糊。
- Veach-ajar scene (material estimation) 上 L1 error = 11.46× lower than baseline
---

# Target-aware Image Denoising for Inverse Monte Carlo Rendering

> [!tip] 核心洞察
> 将“目标图像”作为逆渲染特有的先验知识引入图像去噪过程，利用目标图像的颜色变化指导去噪权重的分配：在局部窗口内用目标颜色的线性函数近似未知的真实图像，通过加权最小二乘回归求解去噪结果。这一策略使得去噪器在图像空间梯度上实现边缘保持的平滑，从而在加速逆渲染优化的同时，避免了收敛到过度平滑的局部极小。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向逆向蒙特卡洛渲染的目标感知图像去噪 |
| 英文题名 | Target-aware Image Denoising for Inverse Monte Carlo Rendering |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://cglab.gist.ac.kr/sig24target/) · [Code](https://github.com/CGLab-GIST/target-aware-denoising) |
| Topic | #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Target-Aware Image Denoising |
| Dataset | Veach-ajar scene, Janga scene, Curtain scene |

> [!tip] 效果简介
> - Veach-ajar scene (material estimation) 上，L1 error 11.46× lower than baseline vs Baseline (no denoising) (11.46× reduction)。
> - Janga scene (volume parameter inference) 上，L1 error 3.96× smaller than baseline vs Baseline (no denoising) (3.96× reduction)。
> - Curtain scene (albedo texture, 4 spp) 上，L1 error 0.00224 (ours, b^I=0.1) vs 0.01639 (no denoising) (0.01415 decrease)。

## 概要

逆向蒙特卡洛渲染通过可微渲染与梯度下降优化场景参数，但梯度中固有的蒙特卡洛噪声导致优化收敛缓慢。直接对渲染图像应用现有去噪器（如基于G-buffer的交叉双边滤波）虽然能降低噪声，却引入了与目标图像不一致的过度平滑偏差，使优化陷入局部极小值，产生模糊或错误的场景参数。

本文提出**目标感知图像去噪**（Target-Aware Image Denoising），首次将逆渲染特有的先验知识——目标图像——融入去噪过程。核心思路是：用目标图像像素颜色的对数变换差异构建相似度核，替代传统依赖场景内部G-buffer的交叉双边权重；并在局部窗口内以目标颜色的线性函数近似未知真实图像，通过加权最小二乘回归求解去噪结果。这一策略使去噪器在图像空间梯度上实现边缘保持的平滑，从而加速优化并避免收敛到过度模糊的局部极小。

实验表明，在材质估计、体积参数推断等多种逆渲染任务中，本文方法相比不使用去噪的基线，L1误差显著降低（Veach-ajar场景降低11.46倍，Janga场景降低3.96倍）。消融实验证实，在4 spp下本文方法的误差已低于基线在256 spp下的误差，大幅减少了所需样本数与优化时间。定量偏差分析进一步揭示，对于非L2损失，本文去噪器产生的图像空间梯度估计偏差远小于基线，从而在优化过程中保持了与目标图像一致的高频细节。

## 核心方法与创新机理

### 问题定位：逆渲染优化中的噪声-偏差困境

逆向蒙特卡洛渲染通过可微渲染与梯度下降优化场景参数 $\pi$，使渲染图像 $f(\pi)$ 逼近用户提供的目标图像 $I$。其核心损失函数为：

$$\mathcal{L} = \frac{1}{m} \| f(\pi) - I \|_p^p$$

其中 $m$ 为像素数乘以颜色通道数。梯度 $\partial\mathcal{L}/\partial\pi$ 通过链式法则 $\frac{\partial\mathcal{L}}{\partial f(\pi)} \frac{\partial f(\pi)}{\partial\pi}$ 计算，但渲染过程本身依赖蒙特卡洛采样，导致 $f(\pi)$ 及其梯度包含大量随机噪声。这一噪声使优化收敛极为缓慢——朴素基线即使运行大量迭代，L1误差仍几乎停留在初始水平（Fig. 2(c)）。

![[assets/figures/papers/paper_list_l37_https_cglab_gist_ac_kr_sig24target/figures/002_Figure_2.jpg]]
*Figure 2: Optimization results where we infer the textures (within the red box) from the initial guess (a constant texture (a)) so that rendering results using the inferred textures match the user-provided target image (b). We test a gradient-based optimizer that uses noisy gradients without denoising (the baseline (c)) and less noisy gradients with image denoising (a cross-bilateral filter (d) and ours (e)). Once their texture inferences are complete, we render the scene with their inferred parameters using a large sample count for the visualization. The baseline (c) does not effectively reduce the*

直接对含噪渲染图像 $\tilde{f}(\pi)$ 应用现有去噪器（如基于G-buffer的交叉双边滤波）看似能降低噪声、加速收敛，却引入了新的致命问题：**过度平滑偏差**。这类去噪器依赖场景内部信息（像素位置、法线、反照率、深度）构建权重，无法感知目标图像的高频细节结构。结果，去噪图像 $\hat{f}(\pi)$ 虽噪声减少，却丢失了与 $I$ 一致的关键纹理信息，导致优化陷入局部极小值，输出模糊甚至错误的场景参数（Fig. 2(d)）。这构成了逆渲染特有的**噪声-偏差困境**：减少噪声的同时，去噪偏差会将优化引向错误方向。

### 核心洞察：目标图像作为去噪先验

本文的关键洞察在于：**逆向渲染拥有一个独特的信息源——目标图像 $I$，它正是我们希望渲染结果逼近的“真实答案”**。虽然未知的真实渲染 $f(\pi)$ 不可得，但 $I$ 提供了关于 $f(\pi)$ 的强先验：在局部窗口内，$f(\pi)$ 的颜色变化应当与 $I$ 的颜色变化高度相关。因此，可以用 $I$ 的局部结构指导去噪权重的分配，使平滑操作在降低噪声的同时，自适应地保留与目标图像一致的细节。

这一思想将去噪从“仅依赖当前场景状态的内部平滑”转变为“以目标图像为锚点的外部引导平滑”，从根本上改变了去噪偏差的方向：偏差不再朝向模糊的局部均值，而是朝向与目标图像结构一致的保边平滑。

### 方法框架：目标感知局部线性回归去噪

整体框架如 Fig. 3 所示，包含前向去噪与反向梯度传播两个模块。

![[assets/figures/papers/paper_list_l37_https_cglab_gist_ac_kr_sig24target/figures/003_Figure_3.jpg]]
*Figure 3: The overview of an inverse rendering framework with our denoising. In the forward phase, denoted by green arrows, our denoiser takes a noisy image*

#### 前向去噪模块

对于含噪渲染图像 $\tilde{f}(\pi)$ 中的每个像素 $c$，在其邻域 $\Omega_c$ 内，用目标图像 $I$ 的线性函数局部近似未知的真实图像 $f(\pi)$（一阶泰勒多项式）：

$$f_i(\pi) \approx f_c(\pi) + f'_c(\pi)(I_i - I_c) \tag{7}$$

基于此近似，通过加权最小二乘回归估计 $f_c(\pi)$ 和 $f'_c(\pi)$：

$$[\hat{\alpha}_c, \hat{\beta}_c] = \underset{\alpha_c, \beta_c}{\mathrm{argmin}} \sum_{i \in \Omega_c} w_{i|c} \| \tilde{f}_i(\pi) - \alpha_c - \beta_c(I_i - I_c) \|^2 \tag{8}$$

其中 $\hat{\alpha}_c$ 即为去噪后的像素值 $\hat{f}_c(\pi)$。

**核心创新——目标感知权重**：权重 $w_{i|c}$ 不再依赖G-buffer，而是基于目标图像像素颜色的对数变换差异构建高斯核：

$$w_{i|c} = \exp\left( - \frac{\| \log_e(I_i + 1) - \log_e(I_c + 1) \|^2}{2 (b^I)^2} \right) \tag{9}$$

对数变换压缩了高动态范围，使权重对暗部和亮部区域的差异具有更均衡的敏感度。全局带宽 $b^I$ 控制平滑程度，本文统一设为 $b^I = 0.1$。这一权重设计使得：当邻域像素 $i$ 与中心像素 $c$ 在目标图像中颜色相近时，权重较大，参与回归的贡献更强；颜色差异大时（如跨边缘），权重趋近于零，有效阻止了跨边缘平滑。因此，去噪操作自动在目标图像的颜色边缘处停止平滑，保留了这些关键结构。

#### 去噪器作为线性平滑器

加权最小二乘回归的闭式解可表示为含噪输入的线性组合：

$$\hat{f}_c(\pi) = \hat{\alpha}_c = e_1^T (X^T W X)^{-1} X^T W Y = \sum_{i \in \Omega_c} l_{i|c} \tilde{f}_i(\pi) \tag{11}$$

其中 $X$ 为设计矩阵（第一列全1，第二列为 $I_i - I_c$），$W$ 为对角权重矩阵，$Y$ 为含噪像素值向量，$l_{i|c}$ 为等效的平滑权重。这一线性特性对梯度反向传播至关重要。

#### 反向梯度传播模块

由于去噪器是线性平滑器，损失对含噪图像的梯度可通过平滑权重的转置高效计算：

$$\frac{\partial \hat{\mathcal{L}}}{\partial \tilde{f}_i(\pi)} = \sum_{c \in \Omega_i} \frac{\partial \hat{\mathcal{L}}}{\partial \hat{f}_c(\pi)} l_{i|c} \tag{12}$$

即损失对含噪像素 $i$ 的梯度，等于所有以 $i$ 为中心的邻域内去噪像素 $c$ 的损失梯度与平滑权重 $l_{i|c}$ 的加权和。这一反向传播路径完全避免了去噪器辅助输入（如G-buffer）的梯度项，因为目标图像 $I$ 是固定的外部参考，不依赖场景参数 $\pi$，从而简化了链式法则并避免了额外噪声。

最终，场景参数梯度由图像空间梯度与渲染Jacobian相乘得到，传递给梯度下降优化器更新 $\pi$。

### 偏差分析：为何一阶线性模型优于常数模型

去噪偏差的期望可近似为：

$$E[\hat{f}_c(\pi)] - f_c(\pi) \approx \frac{f_c''(\pi)}{2} \sum_{i \in \Omega_c} l_{i|c} (I_i - I_c)^2 \tag{16}$$

**关键发现**：一阶线性模型的偏差仅依赖于真实图像 $f(\pi)$ 的**二阶导数** $f_c''(\pi)$ 和目标图像差异的加权平方和。相比之下，常数回归模型（零阶）的偏差依赖于**一阶导数** $f_c'(\pi)$。在纹理丰富的区域，一阶导数通常远大于二阶导数，因此线性模型的偏差显著更小。Fig. 4 的消融实验直观验证了这一点：常数模型虽优于无去噪基线，但仍产生可见的纹理模糊；线性模型则更准确地恢复了纹理细节。

这一偏差特性也解释了为何本文方法能避免现有去噪器的过度平滑陷阱：当目标图像 $I$ 与真实图像 $f(\pi)$ 在局部呈近似线性关系时（大多数自然图像满足此条件），去噪偏差极小，优化得以沿着正确的梯度方向收敛。

### Changed Slots：与基线的关键差异

1. **去噪权重的计算依据**：从基于场景内部G-buffer的交叉双边权重（Eq. 6），转变为基于目标图像像素颜色对数变换差异的目标感知权重（Eq. 9）。这一改变使去噪器能够“看到”目标图像的细节结构，从而在平滑噪声时保留与目标一致的边缘和纹理。

2. **局部近似模型的阶数**：从零阶常数模型或基于G-buffer的一阶模型，转变为一阶线性模型（Eq. 7），且自变量为目标图像颜色 $I$ 而非G-buffer。这一改变使去噪偏差从依赖一阶导数降至依赖二阶导数，在纹理区域显著降低偏差。

### 与现有去噪器的本质区别

现有去噪器（交叉双边滤波、G-buffer线性回归、OIDN）的共同问题在于：它们的权重完全由当前场景参数 $\pi$ 决定，而优化初期 $\pi$ 与真实场景相差甚远，其G-buffer或渲染特征无法捕捉目标图像中的高频细节。因此，这些去噪器在降低噪声的同时，也抹去了优化所需的关键梯度信号。本文方法通过引入独立于 $\pi$ 的目标图像 $I$ 作为权重依据，解耦了“去噪平滑方向”与“当前场景状态”，使去噪偏差始终朝向与目标一致的结构保持方向。

![[assets/figures/papers/paper_list_l37_https_cglab_gist_ac_kr_sig24target/figures/010_Figure_9.jpg]]
*Figure 9: Comparisons of the biases in the estimated image-space gradients with and without our method when using the*

![[assets/figures/papers/paper_list_l37_https_cglab_gist_ac_kr_sig24target/figures/001_Figure_1.jpg]]
*Figure 1: Optimization results where we use a gradient-based optimizer that infers the scene parameters (i.e., textures within the yellow box) from its initial (a reddish one) so that the rendered image with the inferred textures is close to the target image. We compare the images rendered using the parameters inferred by the inverse rendering optimization without and with image denoising, i.e., the baseline and two denoisers (a cross-bilateral filter and our denoiser). Adopting an existing denoiser (i.e., the cross-bilateral filter) allows faster convergence than the baseline without image denoising, but the optimization goes into an undesirable local minimum, i.e., over-blurred textures. On the oth...*

## 实验与关键发现

### 主结果：逆渲染任务中的定量与定性对比

本文在多种逆渲染任务上进行了等时比较，验证了目标感知去噪器在加速收敛与保持细节方面的双重优势。

在 **Veach-ajar 场景的材质估计**任务中，本文方法在相同优化时间内获得的 L1 误差相比不使用去噪的基线降低了 **11.46 倍**（Fig. 7）。渲染结果可视化表明，基线方法由于梯度噪声过大，优化进程缓慢，推断的纹理与目标图像存在显著偏差；而本文方法能够恢复出与目标图像高度一致的材质参数。

在 **Janga 场景的体积参数推断**任务中，本文方法的 L1 误差相比基线降低了 **3.96 倍**（Fig. 7）。该场景涉及参与介质的散射参数估计，梯度空间噪声更为复杂，但目标感知去噪依然展现出稳定的加速效果。

在 **Curtain 场景的反照率纹理优化**中，使用 4 spp 进行渲染时，本文方法（带宽 $b^I = 0.1$）的 L1 误差为 **0.00224**，而同等条件下不使用去噪的基线误差为 0.01639（Table 1），误差降低约 7.3 倍。值得注意的是，**本文方法在 4 spp 下的误差（0.00224）已经低于基线在 256 spp 下的误差（0.00359）**，这意味着目标感知去噪能够以约 64 倍少的样本数达到更优的推断精度，显著减少了单次迭代的渲染时间。

![[assets/figures/papers/paper_list_l37_https_cglab_gist_ac_kr_sig24target/figures/007_Table_1.jpg]]

Fig. 6 的等时比较进一步表明，直接使用现有去噪器（交叉双边滤波、基于 G-buffer 的线性回归、OIDN）虽然能降低噪声，但均导致优化收敛到过度模糊的局部极小值，丢失了纹理细节。本文方法是唯一能够在降噪的同时保持细节、避免过度平滑的方案。

### 关键消融实验

**（1）带宽 $b^I$ 的鲁棒性分析**

Table 1 报告了在 Curtain 场景下，不同带宽 $b^I$ 对推断精度的影响。在 $b^I \in [0.05, 0.4]$ 范围内，4 spp 时的 L1 误差保持在 0.00223–0.00233 之间，波动幅度极小；即使在 1 spp 的极端低采样条件下，误差也仅在 0.00288–0.00310 之间变化。这表明方法对全局带宽选择**不敏感**，无需针对不同场景进行精细调参即可获得稳定性能。

**（2）局部近似模型阶数的选择**

Fig. 4 对比了常数回归（零阶）与线性回归（一阶）两种局部近似模型。两者均利用了目标图像信息来调整去噪权重，但线性回归模型获得了更准确的纹理推断结果。理论分析（Eq. 16）解释了这一差异：常数模型的去噪偏差依赖于真实图像的一阶导数，在纹理区域偏差较大；而线性模型的偏差仅依赖于**二阶导数**，在目标图像与真实图像局部线性相关的区域偏差显著更小。

Table 2 进一步探索了更高阶泰勒多项式（三阶、五阶）的效果。在 Tire 和 Curtain 两个场景中，一阶、三阶、五阶模型的 L1 误差无显著差异（例如 Tire 场景：0.01927 / 0.01895 / 0.01913），表明在当前逆渲染任务中，**一阶线性近似已足够**，增加模型复杂度不会带来额外收益。

![[assets/figures/papers/paper_list_l37_https_cglab_gist_ac_kr_sig24target/figures/008_Table_2.jpg]]

**（3）图像空间梯度的偏差分析**

Fig. 9 展示了在 L1 损失下，基线方法与本文方法估算的图像空间梯度 $\partial \hat{\mathcal{L}} / \partial \tilde{f}(\pi)$ 的偏差平方和对比。本文去噪器产生的梯度估计偏差远小于基线，这归因于去噪过程有效抑制了蒙特卡洛噪声，同时目标感知权重避免了过度平滑。这一结果从梯度偏差的角度解释了为何本文方法能够避免收敛到模糊的局部极小值——更准确的梯度引导优化器朝着保留细节的方向更新参数。

Fig. 5 提供了图像空间梯度的可视化对比：交叉双边滤波虽然降低了梯度中的噪声，但严重模糊了细节（因为其依赖的 G-buffer 无法捕捉来自目标图像的高频信息）；本文方法则在显著降噪的同时，完好保留了与目标图像一致的细节结构。

### 与路径重用技术的组合验证

Fig. 8 展示了本文方法与两种路径重用技术的组合效果：在 Janga 场景中与递归控制变量（R-CV, Nicolet et al., 2023）结合，在 Tire 场景中与参数空间 ReSTIR（P-ReSTIR, Chang et al., 2023）结合。结果表明，组合方法**优于任一单独组件**，验证了目标感知去噪与时间/空间方差降低技术的兼容性与互补性——前者作用于图像空间梯度，后者作用于参数空间梯度，两者可协同加速逆渲染优化。

### 适用边界与失效模式

尽管本文方法在多种任务中展现了显著优势，但存在以下明确边界：

1. **参数空间噪声的上限约束**：本文方法仅对图像空间梯度 $\partial \hat{\mathcal{L}} / \partial \tilde{f}(\pi)$ 进行去噪，无法减少参数空间梯度 $\partial \tilde{f}(\pi) / \partial \pi$ 中的噪声。当渲染 Jacobian 本身包含较大噪声时（例如复杂几何或高维参数的场景），优化提升的上限受限于该部分噪声。Fig. 8 中与 P-ReSTIR 的组合实验部分印证了这一点——参数空间方差降低技术能够弥补本文方法的这一盲区。

2. **全局固定带宽的局部适应性不足**：方法采用全局统一的带宽 $b^I$ 和固定的线性回归阶数，未进行逐像素自适应优化。虽然 Table 1 显示方法对带宽不敏感，但在图像结构变化剧烈（如同时包含平坦区域和高频纹理）的场景中，全局带宽可能导致局部欠平滑或过平滑。

3. **对目标图像质量的依赖**：目标感知权重的构建依赖于目标图像的颜色变化信息。若目标图像本身存在噪声或压缩伪影，权重计算的准确性将受到影响，这是方法的内在假设——目标图像是用户提供的“干净”参考。

## 定位与知识库关联

### 核心定位：将目标图像作为逆渲染先验引入去噪权重计算

本文在逆向蒙特卡洛渲染优化管线中，针对**图像空间梯度去噪**这一特定环节，提出了一个全新的权重计算策略。相对于已有方法，本文改变的**关键 slot** 是：**去噪权重的计算依据从场景内部 G-buffer（位置、法线、反照率、深度）切换为目标图像像素颜色的对数变换差异**。

传统图像去噪器（无论是基于 G-buffer 的交叉双边滤波 **Li et al., 2012; Sen and Darabi, 2012**、基于 G-buffer 的局部线性回归 **Moon et al., 2014**，还是预训练的神经网络去噪器 OIDN **Áfra, 2023**）在设计时均假设去噪器的输入信息完全来自当前渲染的含噪图像及其辅助 G-buffer。这些 G-buffer 仅反映当前场景参数 $\pi$ 下的几何与材质属性，无法感知目标图像 $I$ 中的高频细节。当这些去噪器被直接嵌入逆渲染优化循环时，虽然能降低图像空间梯度的噪声方差，但会引入与目标图像不一致的过度平滑偏差——去噪器抹平了那些在当前场景参数下尚未恢复、但存在于目标图像中的细节结构，导致优化器收敛到模糊的局部极小值（Fig. 1, Fig. 2, Fig. 6）。

本文的核心洞察在于：**逆渲染任务天然具备一个其他去噪场景所没有的先验——目标图像 $I$**。通过将目标图像的颜色信息纳入去噪权重的计算，去噪器能够在降低蒙特卡洛噪声的同时，自适应地保留与目标图像一致的边缘和纹理结构。这一思想在知识库中的挂载点是**可微渲染逆优化中的图像空间梯度估计**环节，具体表现为将去噪器重新形式化为一个以目标图像为条件的局部线性回归问题。

### 与已有方法的本质差异

| 方法 | 去噪权重依据 | 局部近似模型 | 在逆渲染中的表现 |
|------|-------------|-------------|-----------------|
| 无去噪基线 | — | — | 梯度噪声大，收敛极慢 |
| 交叉双边滤波 (Li et al., 2012) | G-buffer 差异（位置/法线/深度等） | 零阶常数 | 加速收敛但细节过度模糊，陷入局部极小 |
| G-buffer 线性回归 (Moon et al., 2014) | G-buffer 差异 | 一阶（基于 G-buffer） | 同上，无法利用目标图像信息 |
| OIDN (Áfra, 2023) | 预训练网络权重（冻结） | 隐式非线性 | 同上有过度模糊问题（Fig. 6f） |
| **本文方法** | **目标图像对数颜色差异** | **一阶（基于目标图像）** | **加速收敛且保持与目标一致的细节** |

差异的因果链条如下：
1. **权重层面**：本文使用 $w_{i|c} = \exp\left(-\frac{\|\log_e(I_i+1) - \log_e(I_c+1)\|^2}{2(b^I)^2}\right)$（式 9）替代基于 G-buffer 的交叉双边权重（式 6）。目标图像中颜色相近的像素在去噪时获得更高权重，使得平滑操作沿目标图像的等色线方向进行，而非仅沿场景几何边界。
2. **局部模型层面**：本文采用一阶线性近似 $f_i(\pi) \approx f_c(\pi) + f'_c(\pi)(I_i - I_c)$（式 7），使得去噪偏差仅依赖于真实图像 $f(\pi)$ 的**二阶导数**（式 16），而零阶常数模型的偏差依赖于**一阶导数**。在纹理丰富区域，一阶导数值较大，常数模型会产生显著偏差，而线性模型的偏差则小得多（Fig. 4 提供了定性验证）。
3. **梯度传播层面**：去噪器被表达为线性平滑器 $\hat{f}_c(\pi) = \sum_{i \in \Omega_c} l_{i|c} \tilde{f}_i(\pi)$（式 11），使得损失梯度可以通过 $\frac{\partial \hat{\mathcal{L}}}{\partial \tilde{f}_i(\pi)} = \sum_{c \in \Omega_i} \frac{\partial \hat{\mathcal{L}}}{\partial \hat{f}_c(\pi)} l_{i|c}$（式 12）高效反向传播。这一线性性质同时使得偏差分析成为可能（式 16–17），从理论上解释了为何本文方法在非 L2 损失（如 L1 损失）下产生的图像空间梯度估计偏差远小于基线（Fig. 9）。

### 适用边界与局限

1. **仅作用于图像空间梯度**：本文方法只减少 $\partial \hat{\mathcal{L}} / \partial \tilde{f}(\pi)$ 中的噪声，无法降低渲染 Jacobian $\partial \tilde{f}(\pi) / \partial \pi$ 中的参数空间噪声。当参数空间噪声占主导时（例如高维体积散射参数或复杂几何），优化提升的上限受限于该部分噪声。这一边界在论文的 limitation 部分被明确承认。
2. **全局固定带宽**：当前实现使用全局统一的带宽 $b^I=0.1$，虽在消融实验中表现出对该参数不敏感（Table 1, $b^I \in [0.05, 0.4]$ 内误差稳定在 0.00223–0.00233），但在局部纹理变化剧烈的场景中，固定带宽可能导致某些区域欠平滑（噪声残留）或过平滑（细节丢失）。
3. **固定一阶模型**：消融实验（Table 2）表明，在当前测试场景中三阶、五阶泰勒多项式与一阶模型无显著差异，但该结论可能不适用于具有强非线性颜色变化的场景（如焦散、复杂折射）。
4. **方法实现为经典回归**：当前方法基于局部线性回归，尚未与神经网络去噪器结合。论文指出未来可探索将目标感知思想融入可微神经网络去噪器。

### 知识库挂载点与后续启发

**挂载点**：本文方法可挂载到可微渲染逆优化管线的“图像空间梯度估计”模块，作为蒙特卡洛梯度估计与场景参数优化器之间的一个即插即用去噪层。该层不修改采样过程，仅对已渲染的含噪图像进行后处理，因此可与现有的方差降低技术正交组合——论文已通过实验验证了与 **递归控制变量 (R-CV, Nicolet et al., 2023)** 和 **参数空间 ReSTIR (P-ReSTIR, Chang et al., 2023)** 的组合效果（Fig. 8），组合方法优于任一单独技术。

**后续启发**：
1. **自适应带宽与阶数选择**：如何根据图像局部结构（如目标图像的梯度幅值）自动选择每像素的带宽 $b^I_i$ 和回归阶数，以最小化局部去噪偏差。
2. **参数空间扩展**：能否将目标感知的思想从图像空间扩展到参数空间，即利用目标图像信息指导 $\partial \tilde{f}(\pi) / \partial \pi$ 的降噪，从而同时解决两个噪声源。
3. **神经目标感知去噪器**：设计一个以目标图像和含噪渲染图像为输入的可微神经网络去噪器，通过端到端训练学习更复杂的去噪策略，同时保持线性平滑器的梯度传播效率。
4. **跨任务泛化**：目标感知去噪的核心思想——利用任务特定的参考信号指导去噪权重分配——可能适用于其他需要保边平滑的逆问题（如计算摄影中的去模糊、医学影像重建等），其中参考信号可以是测量数据或先验图像。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Target_aware_Image_Denoising_for_Inverse_Monte_Carlo_Rendering.pdf]]