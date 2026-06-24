---
title: "Adaptive Shells for Efficient Neural Radiance Field Rendering"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2023/Adaptive_Shells_for_Efficient_Neural_Radiance_Field_Rendering.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/adaptive-shells/
aliases:
- AS
- ASENRFR
tags:
- SIGGRAPH_ASIA_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "空间自适应核大小（spatially-varying kernel size）引导的显式窄带壳（adaptive shell）提取与壳内渲染采样策略。"
primary_logic: "场景中的不同区域应使用不同的渲染方式：模糊几何（如毛发、叶子）需要体渲染以处理半透明和复杂形状，而实表面可以用单次采样精确表示。基于此，提出学习一个空间变化的核大小，自动适应区域复杂度，并据此提取显式的窄带壳体，在壳体内进行采样：实表面区域仅需1个样本，模糊区域自适应增加样本数，从而在提升或保持图像质量的同时大幅减少计算量，实现实时渲染。"
claims:
- "自适应核大小使实表面区域仅需单样本，模糊区域最多32样本，而NeuS固定384样本，大幅加速并提升质量。"
- "在Shelly数据集上，本方法PSNR达到36.02，比Instant NGP的33.48高2.54 dB，且SSIM 0.954，LPIPS 0.079均优于所有基线。"
- "窄带渲染将样本数减少最多3倍，帧率提高5倍（例如Shelly上262.69 FPS vs Instant NGP 85.16 FPS），同时保持或提高视觉质量。"
- "Shelly 上 PSNR ↑ = 36.02"
---

# Adaptive Shells for Efficient Neural Radiance Field Rendering

> [!tip] 核心洞察
> 场景中的不同区域应使用不同的渲染方式：模糊几何（如毛发、叶子）需要体渲染以处理半透明和复杂形状，而实表面可以用单次采样精确表示。基于此，提出学习一个空间变化的核大小，自动适应区域复杂度，并据此提取显式的窄带壳体，在壳体内进行采样：实表面区域仅需1个样本，模糊区域自适应增加样本数，从而在提升或保持图像质量的同时大幅减少计算量，实现实时渲染。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 自适应壳体用于高效的神经辐射场渲染 |
| 英文题名 | Adaptive Shells for Efficient Neural Radiance Field Rendering |
| 会议/期刊 | SIGGRAPH Asia 2023 |
| Links | [paper](https://arxiv.org/abs/2311.10091); [Project](https://research.nvidia.com/labs/toronto-ai/adaptive-shells/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Adaptive Shells |
| Dataset | Shelly, DTU |

> [!tip] 效果简介
> - Shelly 上，PSNR ↑ 为 36.02，对比 33.48 (Instant NGP)，变化 +2.54。
> - Shelly 上，LPIPS ↓ 为 0.079，对比 0.125 (Instant NGP)，变化 -0.046。
> - Shelly 上，FPS ↑ 为 262.69，对比 85.16 (Instant NGP)，变化 ~3.1x。

## 概述

神经辐射场（NeRF）通过体积渲染实现了逼真的新视角合成，但其核心瓶颈在于：传统方法对所有空间区域进行统一密集采样，导致大量计算浪费在实表面区域。即使采用空体素跳过等加速策略，占据区域仍需多次采样，且网格加速结构带来显著内存开销。此外，MLP的平滑偏差使其难以学习尖锐的密度函数，进一步限制了效率与质量的平衡。

本文提出 **Adaptive Shells**，核心思想是：场景中不同区域应采用不同的渲染方式——模糊几何（如毛发、叶子）需要体积渲染处理半透明和复杂形状，而实表面仅需单次采样即可精确表示。方法的关键因果调节变量是 **空间自适应核大小**（spatially-varying kernel size），通过学习一个随位置变化的核函数 $s(\mathbf{x})$，自动适应区域复杂度：在模糊区域核变大，在实表面区域核坍缩为脉冲函数。基于此核大小，方法通过水平集演化从SDF中提取显式的窄带壳体（adaptive shell），并在壳体内进行采样——实表面区域仅需1个样本，模糊区域自适应增加至最多32个样本。

实验表明，该方法在 **Shelly** 数据集上达到 **36.02 PSNR**，比 Instant NGP（33.48）高 **2.54 dB**，LPIPS降至 **0.079**；同时帧率提升约 **3.1 倍**（262.69 vs 85.16 FPS）。在 **DTU** 数据集上，PSNR达到 **33.37**，同样优于所有基线。在 **MipNeRF360** 室外场景上，质量与基线可比但速度快约 **5 倍**。消融实验证实，空间变化核相比全局核提升约1.7 dB PSNR，自适应壳相比固定SDF阈值壳获得更好的质量-速度权衡。

方法在方法谱系中定位于 **NeRF加速与表面-体积混合表示** 的交汇点：它继承 NeuS 的SDF-密度转换框架，但通过空间变化核和显式壳提取，将体积渲染限制在窄带内，实现了从纯体积渲染到近表面渲染的平滑过渡。与 MobileNeRF、BakedSDF 等烘焙方法不同，本方法无需预计算纹理，保持了神经表示的连续性和可微性。

## 背景与动机

神经辐射场（NeRF）及其变体在新视角合成与场景重建领域取得了突破性进展，但其核心瓶颈在于体积渲染的计算效率：传统方法对所有空间区域进行统一密集采样，导致大量计算浪费在对渲染贡献极小的区域。尽管已有加速方案（如空体素跳过）能够减少无效采样，但在占据区域内仍需多次采样才能获得准确结果，且基于网格的加速结构内存开销显著。更根本地，现有方法难以同时高效处理场景中两类截然不同的区域——具有清晰几何的实表面（如皮肤、家具）和具有模糊几何的半透明结构（如毛发、叶子）。

**实表面与模糊几何的渲染冲突**。纯表面表示（如基于SDF的NeuS）在实表面上表现良好，但难以表达半透明和复杂几何；纯体积表示（如NeRF、Instant NGP）可以处理任意几何，但即使在实表面区域也需要多次采样才能获得准确的颜色积分。NeuS通过一个全局核大小 $s$ 将SDF值映射为密度，该核大小控制着从表面到体积的过渡宽度：小核适合实表面，大核适合模糊区域。然而，全局核大小在面对包含多种几何类型的复杂场景时不可避免地收敛到一个折中值——对体积区域太小、对实表面太大（图7），导致两类区域均无法达到最优表示。

**现有加速方案的局限**。Instant NGP（Müller et al., 2022）通过多分辨率哈希编码和多层感知机实现了快速训练和推理，但其体积渲染仍需每像素数百个样本（如384个），在实表面区域存在大量冗余计算。MobileNeRF（Chen et al., 2023）和BakedSDF（Yariv et al., 2023）将辐射场烘焙到代理几何上以加速渲染，但这些代理几何是固定的，无法自适应场景的局部复杂度。空体素跳过策略（图2左）虽然避免了在空白区域的采样，但在占据体素内仍需多次采样，未能从根本上解决实表面区域的冗余问题。

**核心洞察**。场景中不同区域应当采用不同的渲染方式：模糊几何需要体渲染以处理半透明和复杂形状，而实表面可以用单次采样精确表示。基于此，本文提出学习一个空间变化的核大小，自动适应区域复杂度，并据此提取显式的窄带壳体，在壳体内进行自适应采样——实表面区域仅需1个样本，模糊区域自适应增加样本数，从而在提升或保持图像质量的同时大幅减少计算量，实现实时渲染。

## 核心创新

Adaptive Shells 的核心创新在于将**空间自适应核大小（spatially-varying kernel size）** 与**显式窄带壳提取**结合，形成一种从体积渲染到表面渲染平滑过渡的混合表示。这一设计直接回应了传统神经辐射场的根本瓶颈：统一密集采样策略在实表面区域造成大量冗余计算，而现有加速方法（如 Instant NGP 的空体素跳过）仍无法在占据区域内减少样本数。

### 关键因果调节变量：空间自适应核 $s(\mathbf{x})$

方法的核心调节变量是将 NeuS（Wang et al., 2021）中的**全局常量核大小 $s$** 替换为**空间变化神经网络输出 $s(\mathbf{x})$**（Section 3.2）。这一改变的因果机制在于：

- **全局核的两难困境**：NeuS 通过 SDF 到密度的 sigmoid 映射 $\Phi_s(f) = (1 + \exp(-f/s))^{-1}$ 控制几何模糊程度。全局 $s$ 在所有区域取折中值，导致体积区域（如毛发、叶子）核过小而丢失半透明细节，实表面区域核过大而无法精确表示尖锐边界（Figure 7）。
- **自适应核的收敛行为**：网络自动学习在模糊几何区域输出大核，使密度函数平滑延展以支持体渲染；在实表面区域输出小核，使密度函数趋近于脉冲函数，为单样本表面渲染提供理论依据。这一行为无需显式分类监督，完全由颜色重建损失驱动。

### 改变的渲染范式：从全光线采样到窄带壳采样

基于自适应核，方法改变了三个关键环节（Table 1, Section 3.4）：

1. **壳提取替代空体素跳过**：现有加速方法（Instant NGP）通过跳过空体素减少样本，但占据区域内仍需多次采样。Adaptive Shells 通过水平集演化从 SDF 和 $s(\mathbf{x})$ 提取显式的内/外壳网格，将渲染严格限制在窄带区间内（Figure 2, Figure 4）。

2. **采样数自适应分配**：实表面区域壳极薄，仅需 1 个中点样本即可精确近似表面；模糊区域壳较宽，自适应增加至最多 32 个等距样本。相比之下，NeuS 固定使用 384 样本/像素（Figure 7）。

3. **两阶段训练策略**：第一阶段全光线训练 SDF 和核大小，确保几何和核的全局一致性；第二阶段在提取的壳内微调辐射场并关闭正则化（Eikonal、核平滑、法向预测），使网络自由补偿壳提取引入的微小误差（Section 3.5, Table 4）。

### 效果验证

这一创新带来的决定性证据包括：
- 在 Shelly 数据集上，PSNR 达到 36.02，比 Instant NGP 的 33.48 高 **+2.54 dB**，LPIPS 降低至 0.079（Table 2）。
- 帧率从 Instant NGP 的 85.16 FPS 提升至 **262.69 FPS**（约 3.1 倍），样本数减少最多 3 倍（Table 1）。
- 消融实验证实，空间变化核相比全局核在 PSNR 上提升约 **1.7 dB**（34.26 → 36.02），且自适应壳相比固定 SDF 阈值壳获得更好的质量-速度权衡（Table 4）。

## 整体框架

Adaptive Shells 的完整管线分为两大阶段：**第一阶段**在全光线体积渲染下联合训练几何网络与辐射场，同时学习一个空间自适应的核大小场；**第二阶段**基于学到的 SDF 与核大小场，通过水平集演化提取显式的窄带壳体网格，随后在壳内进行高效的窄带渲染与微调（见 Figure 3 概览）。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed approach. We demonstrate high-fidelity, eficient neural implicit scene reconstruction by eficiently-sampling volumetric rendering inside of an explicit thin shell, which is automatically fit from visual objectives*

### 第一阶段：全光线联合训练

输入为多视图 RGB 图像及对应的相机参数。对每条射线，首先在近远平面间进行分层采样，对每个采样点执行以下前向流程：

1. **哈希编码**：将 3D 坐标 $\mathbf{x}$ 输入多分辨率哈希编码 $\Psi(\mathbf{x})$（14 层，每层哈希表大小为 $2^{22}$，与 Instant NGP（Müller et al., 2022）一致），得到紧凑的特征向量。
2. **几何网络**：MLP $\mathrm{NN}_{\theta}^{\mathrm{geo}}$ 接收哈希编码与原始坐标的拼接 $[\Psi(\mathbf{x}), \mathbf{x}]$，输出四个量：
   $$(f, 1/s, \mathbf{f}_{\mathrm{geo}}, \mathbf{n}) = \mathrm{NN}_{\theta}^{\mathrm{geo}}([\Psi(\mathbf{x}), \mathbf{x}])$$
   其中 $f$ 为带符号距离函数（SDF）值，$s$ 为空间变化的核大小（网络输出其倒数 $1/s$），$\mathbf{f}_{\mathrm{geo}}$ 为几何潜特征，$\mathbf{n}$ 为预测的法向。
3. **密度映射**：通过 NeuS（Wang et al., 2021）的 SDF-to-density 映射将 $f$ 与 $s$ 转换为体密度 $\sigma$：
   $$\sigma = \max\left(-\frac{\frac{d\Phi_s}{d\tau}(f)}{\Phi_s(f)}, 0\right), \quad \Phi_s(f) = (1 + \exp(-f/s))^{-1}$$
   与原始 NeuS 的关键区别在于，此处的 $s$ 不再是全局常量，而是由几何网络逐点预测的空间变化量 $s(\mathbf{x})$。
4. **辐射网络**：MLP $\mathrm{NN}_{\theta}^{\mathrm{rad}}$ 接收编码后的视线方向 $\gamma(\mathbf{d})$、几何潜特征 $\mathbf{f}_{\mathrm{geo}}$、预测法向 $\mathbf{n}$ 和坐标 $\mathbf{x}$，输出颜色 $\mathbf{c}$：
   $$\mathbf{c} = \mathrm{NN}_{\theta}^{\mathrm{rad}}([\gamma(\mathbf{d}), \mathbf{f}_{\mathrm{geo}}, \mathbf{n}, \mathbf{x}])$$
5. **体渲染积分**：沿射线对采样点进行数值积分得到像素颜色：
   $$\mathbf{c}(\mathbf{r}) = \sum_{i=1}^{N_r} \exp\left[-\sum_{j=1}^{i-1} \sigma_j \delta_j\right] (1 - \exp(-\sigma_i \delta_i)) \mathbf{c}(\mathbf{r}, \mathbf{d})_i$$

第一阶段的总损失函数为：
$$\mathcal{L} = \mathcal{L}_{\mathbf{c}} + \lambda_e \mathcal{L}_e + \lambda_s \mathcal{L}_s + \lambda_{\mathbf{n}} \mathcal{L}_{\mathbf{n}}$$
其中 $\mathcal{L}_{\mathbf{c}}$ 为像素级 L1 颜色损失，$\mathcal{L}_e$ 为 Eikonal 正则化（鼓励 $||\nabla f||_2 = 1$），$\mathcal{L}_s$ 为核大小平滑损失（鼓励 $\log s(\mathbf{x})$ 在局部邻域内平滑），$\mathcal{L}_{\mathbf{n}}$ 为法向预测损失（使网络预测法向与 SDF 梯度法向一致）。

### 壳体提取：从隐式场到显式网格

第一阶段收敛后，得到 SDF 场 $f(\mathbf{x})$ 和核大小场 $s(\mathbf{x})$。壳体提取的目标是构造两个显式三角网格——**内边界** $\mathcal{M}_-$ 和**外边界** $\mathcal{M}_+$，它们界定了对渲染有显著贡献的空间区域。

提取过程基于约束正则化的水平集演化方程：
$$\frac{\partial f}{\partial t} = -|\nabla f| \bigg( \mathbf{v}(f_0, s) + \lambda_{\mathrm{curv}} \nabla \cdot \frac{\nabla f}{|\nabla f|} \bigg) \omega(f)$$
其中 $\omega(f)$ 为软衰减窗口，将演化限制在零水平集附近：
$$\omega(f) = \frac{1}{2} \big( 1 + \cos(\pi \operatorname{clamp}(f / \zeta, -1, 1)) \big)$$

- **膨胀**：以速度 $v_{\mathrm{dilate}}(f_0, s)$ 向外推演 SDF，速度正比于局部密度 $\sigma(f_0, s)$（当密度高于阈值 $\sigma_{\mathrm{min}}$ 时），生成 $\mathrm{SDF}_+$，提取 $\mathrm{SDF}_+ = 0$ 作为外边界 $\mathcal{M}_+$。
- **侵蚀**：以速度 $v_{\mathrm{erode}}(f_0, s)$ 向内推演 SDF，速度反比于局部密度（上限 $v_{\mathrm{max}}$），生成 $\mathrm{SDF}_-$，提取 $\mathrm{SDF}_- = 0$ 作为内边界 $\mathcal{M}_-$。

最终通过 clamping 确保内边界不超出原始零水平面、外边界不缩入原始零水平面，并用 Marching Cubes 提取网格。Figure 5 在 2D 切片上可视化了这一过程：模糊区域（如毛发）对应较大的 $s$ 值，壳体较厚；实表面区域对应极小的 $s$ 值，壳体坍缩为紧贴表面的薄层。

### 第二阶段：窄带渲染与微调

提取壳体后，渲染流程从“全光线密集采样”切换为“窄带采样”：

1. 为 $\mathcal{M}_+$ 和 $\mathcal{M}_-$ 构建光线追踪加速结构。
2. 对每条射线，与两网格求交，得到一系列区间（射线进入 $\mathcal{M}_+$ 到离开 $\mathcal{M}_-$ 的段落）。
3. 在每个区间内等距采样，采样数由目标样本数与区间宽度共同决定。实表面区域壳体极薄，通常仅需 **1 个样本**；模糊区域壳体较厚，自适应增加至最多 32 个样本。这相比 NeuS 固定的 384 样本/像素大幅减少了计算量（Figure 7）。

在窄带内进行第二阶段微调时，**关闭所有正则化项**，仅保留颜色损失 $\mathcal{L}_{\mathbf{c}}$。消融实验（Table 4）表明，禁用正则化使网络能够更自由地补偿壳体近似带来的误差，从而进一步提升视觉质量。

### 输入输出总览

| 阶段 | 输入 | 输出 | 关键操作 |
|------|------|------|----------|
| 第一阶段 | 多视图 RGB 图像 + 相机参数 | SDF $f$、核大小 $s$、辐射场 | 全光线体渲染 + 联合损失优化 |
| 壳体提取 | $f(\mathbf{x})$, $s(\mathbf{x})$ | 内/外壳网格 $\mathcal{M}_-$, $\mathcal{M}_+$ | 水平集侵蚀/膨胀 + Marching Cubes |
| 第二阶段 | $\mathcal{M}_-$, $\mathcal{M}_+$ + 训练图像 | 微调后的辐射场 | 窄带采样 + 仅颜色损失微调 |
| 推理 | $\mathcal{M}_-$, $\mathcal{M}_+$ + 微调网络 | 渲染图像 | 光线-网格求交 + 壳内等距采样 |

该管线的核心因果链条为：**空间自适应核大小 → 自适应壳体宽度 → 窄带采样 → 计算量大幅降低 + 质量保持/提升**。在 Shelly 数据集上，该方法以 262.69 FPS 的速度实现 36.02 PSNR，相比 Instant NGP（85.16 FPS, 33.48 PSNR）实现了约 3.1 倍加速和 +2.54 dB 的质量提升（Table 1, Table 2）。

## 核心模块与公式推导

### 3.1 体积渲染基础

Adaptive Shells 建立在标准体积渲染方程之上。沿光线 $\mathbf{r}$ 的期望颜色由积分给出：

$$\mathbf{c}(\mathbf{r}) = \int_{\tau_n}^{\tau_f} \exp\Big[ \int_{\tau_n}^{\tau} -\sigma(\mathbf{r}(z)) dz \Big] \sigma(\mathbf{r}(\tau)) \mathbf{c}(\mathbf{r}(\tau), \mathbf{d}) d\tau$$

其中 $\sigma$ 为体积密度，$\mathbf{c}$ 为发射颜色，$\mathbf{d}$ 为光线方向。实际计算中采用离散数值积分近似：

$$\mathbf{c}(\mathbf{r}) = \sum_{i=1}^{N_r} \exp\Big[ -\sum_{j=1}^{i-1} \sigma_j \delta_j \Big] (1 - \exp(-\sigma_i \delta_i)) \mathbf{c}(\mathbf{r}, \mathbf{d})_i$$

传统方法（如 Instant NGP）在全光线上均匀密集采样（典型 $N_r=384$），导致大量计算浪费在实表面区域。

### 3.2 空间自适应核大小

核心创新在于将 NeuS 的全局核大小 $s$ 推广为空间变化的神经网络输出 $s(\mathbf{x})$。SDF 值 $f$ 通过 sigmoid 映射为密度：

$$\sigma = \operatorname*{max}\left( -\frac{\frac{d\Phi_s}{d\tau}(f)}{\Phi_s(f)}, 0 \right), \qquad \Phi_s(f) = \big(1 + \exp(-f/s)\big)^{-1}$$

当 $s \to 0$ 时，$\Phi_s$ 趋近于阶跃函数，密度退化为表面上的脉冲——此时仅需单样本即可精确渲染实表面；当 $s$ 较大时，密度在 SDF 零水平集附近平缓过渡，适合模糊几何（毛发、叶子）。网络自动学习 $s(\mathbf{x})$ 以适应局部几何复杂度（Figure 7）。

### 3.3 自适应壳提取

给定训练好的 SDF $f$ 和核大小 $s$，通过约束正则化的水平集演化提取显式窄带壳。演化方程为：

$$\frac{\partial f}{\partial t} = -|\nabla f| \bigg( \boldsymbol{v}(f_0, s) + \lambda_{\mathrm{curv}} \nabla \cdot \frac{\nabla f}{|\nabla f|} \bigg) \omega(f)$$

其中 $\boldsymbol{v}$ 为速度场，$\lambda_{\mathrm{curv}}$ 为曲率正则化权重，$\omega(f)$ 为软衰减窗函数：

$$\omega(f) = \frac{1}{2} \big( 1 + \cos(\pi \cos(f / \zeta, -1., 1.) ) \big)$$

该窗函数将演化限制在零水平集附近宽度 $\zeta$ 的窄带内，防止远场区域被扰动。

**膨胀速度**由密度驱动，密度高于阈值 $\sigma_{\mathrm{min}}$ 时与密度成正比：

$$v_{\mathrm{dilate}}(f_0, s) = \begin{cases} \beta_d \sigma(f_0, s) & \sigma(f_0, s) > \sigma_{\mathrm{min}} \\ 0 & \sigma(f_0, s) \le \sigma_{\mathrm{min}} \end{cases}$$

**侵蚀速度**反比于密度，并设上限 $v_{\mathrm{max}}$：

$$v_{\mathrm{erode}}(f_0, s) = \operatorname*{min} \big( v_{\mathrm{max}}, \beta_e \frac{1}{\sigma(f_0, s)} \big)$$

演化后通过 clamping 保证侵蚀仅收缩、膨胀仅扩张：$\text{SDF}_- \leftarrow \max(f_0, \text{SDF}_-)$，$\text{SDF}_+ \leftarrow \min(f_0, \text{SDF}_+)$。最终用 Marching Cubes 提取 $\text{SDF}_- = 0$ 和 $\text{SDF}_+ = 0$ 作为内/外壳网格 $M_-$、$M_+$。实表面区域核大小趋近于零，壳极薄；模糊区域核较大，壳相应增厚（Figure 5）。

### 3.4 窄带渲染采样

渲染时对 $M_+$ 和 $M_-$ 构建光线追踪加速结构，每条光线与网格求交得到一系列区间 $[t_{\text{in}}, t_{\text{out}}]$。在每个区间内等距采样，采样数由区间宽度和预设步长决定。实表面区域壳极薄，往往仅需1个网络评估；模糊区域自适应增加至最多32个样本，而 NeuS 固定使用384个样本。

### 3.5 两阶段训练

**第一阶段**：全光线训练 SDF 和核大小，总损失为：

$$\mathcal{L} = \mathcal{L}_{\mathbf{c}} + \lambda_e \mathcal{L}_e + \lambda_s \mathcal{L}_s + \lambda_{\mathbf{n}} \mathcal{L}_{\mathbf{n}}$$

其中：
- **颜色损失**：像素级 L1 损失 $\mathcal{L}_{\mathrm{c}} = \frac{1}{|\mathcal{R}|} \sum_{\mathbf{r} \in \mathcal{R}} |\mathbf{c}(\mathbf{r}) - \mathbf{c}_{\mathrm{gt}}(\mathbf{r})|$
- **Eikonal 正则化**：$\mathcal{L}_e = \frac{1}{|\boldsymbol{X}|} \sum_{\mathbf{x} \in \boldsymbol{X}} \left( ||\nabla f(\mathbf{x})||_2 - 1 \right)^2$，鼓励 SDF 梯度为单位长度
- **核平滑损失**：$\mathcal{L}_s = \frac{1}{\chi} \sum_{\mathbf{x} \in \mathcal{X}} ||\log[s(\mathbf{x})] - \log[s(\mathbf{x} + N(0, \varepsilon^2))]||_2$，鼓励 $s(\mathbf{x})$ 空间平滑
- **法向预测损失**：$\mathcal{L}_{\mathbf{n}} = \frac{1}{|\mathcal{X}|} ||\mathbf{n}(\mathbf{x}) - \frac{\nabla f(\mathbf{x})}{||\nabla f(\mathbf{x})||_2}||_2$，使网络预测法向与 SDF 梯度一致

**第二阶段**：固定壳网格，在窄带内仅用 $\mathcal{L}_{\mathbf{c}}$ 微调辐射场，关闭所有正则化。消融实验（Table 4）表明，关闭正则化后视觉质量进一步提升——网络获得更大自由度以补偿壳提取引入的微小几何误差。

### 4.1 网络架构

几何网络以多分辨率哈希编码 $\Psi(\mathbf{x})$（14层，每层哈希表大小 $2^{22}$）和坐标 $\mathbf{x}$ 为输入：

$$( f , 1 / s , \mathbf{f}_{\mathrm{geo}} , \mathbf{n} ) = \mathrm{NN}_{\theta}^{\mathrm{geo}} ( [ \Psi ( \mathbf{x} ) , \mathbf{x} ] )$$

输出 SDF 值 $f$、逆核大小 $1/s$、几何潜特征 $\mathbf{f}_{\mathrm{geo}}$ 和法向 $\mathbf{n}$。辐射网络以编码后的视角方向 $\gamma(\mathbf{d})$、几何潜特征、法向和位置为输入，预测颜色：

$$\mathbf{c} = \mathrm{NN}_{\theta}^{\mathrm{rad}} ( [ \gamma ( \mathbf{d} ) , \mathbf{f}_{\mathrm{geo}} , \mathbf{n} , \mathbf{x} ] )$$

## 实验与分析

### 核心定量结果

Adaptive Shells 在四个数据集上进行了系统评估，涵盖物体级场景（Shelly、DTU、NeRF Synthetic）与无界户外场景（Mip-NeRF 360）。所有性能测量均在 RTX 4090 GPU、1080p 分辨率、无 GUI 开销的条件下进行，确保对比公平。

**Shelly 数据集**：该方法在所有指标上均显著优于基线。PSNR 达到 **36.02**，比 Instant NGP（33.48）高 **+2.54 dB**，比 Mip-NeRF（34.55）高 +1.47 dB，比 MobileNeRF（32.01）高 +4.01 dB（Table 2）。LPIPS 降至 **0.079**，显著低于 Instant NGP 的 0.125 和 MobileNeRF 的 0.113。SSIM 达到 **0.954**，同样领先所有基线。逐场景细粒度结果见补充材料 Table 1–3。

**DTU 数据集**：PSNR 为 **33.37**，比 Instant NGP（31.38）高 **+1.99 dB**，比 Mip-NeRF（31.91）高 +1.46 dB（Table 2；逐场景见 Supplement Table 5）。需注意 Instant NGP 在 DTU 上的性能受大量背景采样拖累——这是其均匀采样策略的固有缺陷，而 Adaptive Shells 通过显式壳自动聚焦前景区域，不受此影响（Table 1 注释）。

**NeRF Synthetic 数据集**：PSNR 为 33.72，与 Instant NGP（33.18）和 Mip-NeRF（33.09）可比，但显著快于两者（Table 2；逐场景见 Supplement Table 7）。该数据集场景相对简单、几何清晰，自适应壳的优势主要体现在速度而非质量上。

**Mip-NeRF 360 户外数据集**：PSNR 为 **23.17**，略低于 Instant NGP 的 23.90（-0.73 dB），但推理速度快约 5 倍（Table 3 和 Table 1）。在 Bicycle 场景上 PSNR 为 22.74 vs Instant NGP 的 22.51，Garden 场景为 25.06 vs 25.19，整体质量可比。需注意 Flowers 和 Treehill 两个场景因许可问题被排除。

### 推理性能与采样效率

Table 1 展示了推理性能的核心优势。在 Shelly 数据集上，Adaptive Shells 达到 **262.69 FPS**，而 Instant NGP 仅为 85.16 FPS，加速约 **3.1 倍**。在 DTU 上为 268.80 FPS vs 42.53 FPS（约 6.3 倍），在 NeRF Synthetic 上为 280.16 FPS vs 128.75 FPS（约 2.2 倍），在 Mip-NeRF 360 上为 40.99 FPS vs 8.77 FPS（约 4.7 倍）。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/012_Table_1.jpg]]
*Table 1: Performance comparisons on all four data sets, measured at 1080p without GUI overhead using an RTX 4090 GPU. Our adaptive sample placement and mesh-based empty-space skipping technique allows us to outperform Instant NGP without compromising visual fidelity. Note that Instant NGP’s performance on the DTU data set was hindered by a large number of background samples, and is therefore not necessarily indicative of a real use case: the user may specify a tighter scene bounding box to focus the samples on the main scene contents*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/016_Table_3.jpg]]
*Table 3: antitative results on the MipNeRF360 data set. We report the PSNR, LPIPS and SSIM results for each object and compare them to baselines. Our method achieves a performance comparable to the baselines while being significantly faster during inference (see Table 1). In our comparison, we exclude the two scenes with license issues: Flowers, Treehill*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/020_Table_1.jpg]]
*Table 1: Per-scene quantitative PSNR comparison on Shelly data set*

加速的根本原因在于样本数的大幅减少。该方法在 Shelly 上平均仅需 **4.90 样本/像素**，DTU 上 4.40，NeRF Synthetic 上 4.82，Mip-NeRF 360 上 12.42（Table 1 及 Supplement Table 4, 6, 11）。相比之下，Instant NGP 使用固定 384 样本/像素。窄带壳将采样严格限制在对渲染有实质贡献的区域内，实表面区域仅需 1 个样本，模糊区域自适应增加到最多 32 个样本（Figure 7）。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/015_Table_4.jpg]]
*Table 4: Ablating our method on the Shelly data set. SV Kernel denotes the spatially varying kernel as introduced in Section 3.2. Band, fixed denotes the shell is not adaptive but extracted for a given SDF threshold*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/023_Table_4.jpg]]
*Table 4: Per-scene sample count of our method on Shelly data set*

### 消融实验

Table 4 在 Shelly 数据集上消融了三个关键设计选择：

**空间变化核 vs 全局核**：将空间变化核（SV Kernel）替换为全局常量核（如原始 NeuS），PSNR 从 36.02 降至 34.26（**-1.76 dB**），LPIPS 从 0.079 升至 0.092，SSIM 从 0.954 降至 0.942。这验证了自适应核大小对场景局部复杂度的适应能力是质量提升的核心驱动力——全局核在模糊区域过小、在锐利表面过大，无法同时兼顾（Figure 7）。

**自适应壳 vs 固定阈值壳**：将基于核大小提取的自适应壳替换为基于固定 SDF 阈值提取的壳，PSNR 降至 35.19（-0.83 dB），LPIPS 升至 0.086。固定壳无法根据局部几何复杂度调整宽度，在模糊区域可能截断有效密度，在实表面区域则浪费样本。

**微调阶段正则化**：在壳内微调阶段禁用 Eikonal 和法向正则化（仅用 $\mathcal{L}_{\mathbf{c}}$），相比保留正则化进一步提升了视觉质量（Table 4 中 Regularization 行）。原因是正则化约束了网络表达高频细节的能力，而微调阶段的核心目标是在窄带内补偿壳提取引入的微小几何误差。

**样本数消融**：Figure 11 展示了样本数对质量与速度的权衡。在 Shelly 和 Mip-NeRF 360 的六个场景上，将默认样本数减半导致 PSNR 下降约 0.1–0.3 dB，但运行时性能提升约 40–50%；将样本数加倍则 PSNR 提升约 0.05–0.15 dB，但速度相应下降。默认超参数在质量-速度曲线上处于高效拐点。

### 定性分析

Figure 8 展示了 Shelly 数据集上的渲染画廊，该方法在毛发、植物叶片等模糊几何区域保持了丰富的体积细节，同时在皮肤、家具等实表面上产生清晰的边缘。Figure 6 特别展示了自适应壳在松鼠尾巴（模糊）和皮肤（锐利）上的差异化处理：纯表面表示无法捕捉尾巴的半透明体积感，而自适应壳在尾巴区域使用最多 16 个样本，在皮肤区域仅需 1 个样本。

Figure 9 和 Figure 10 分别展示了 DTU 和 Mip-NeRF 360 上的定性结果。在 DTU 的扫描物体上，该方法重建的几何细节与 Instant NGP 和 Mip-NeRF 相当或更优。在 Mip-NeRF 360 的户外场景中，自适应壳成功捕捉了草地、树叶等模糊区域，但在远距离背景区域偶尔出现漂浮几何伪影（见下文失败模式）。

### 失败模式与局限性

1. **极薄结构遗漏**：自适应壳可能无法捕获极薄的结构（如铁丝网、细栏杆），因为这些结构在训练阶段的密度积分贡献微弱，SDF 和核大小可能未充分表达它们，导致壳提取时被侵蚀掉。文中明确指出这一局限性。

2. **无界场景的背景退化**：在 Mip-NeRF 360 等无界场景中，背景区域的质量和速度仍有提升空间。远距离背景的 SDF 估计可能不准确，导致壳提取产生漂浮几何伪影，且背景区域需要更多样本（Mip-NeRF 360 平均 12.42 样本/像素 vs Shelly 的 4.90）。

3. **稀疏视角退化**：方法依赖多视图输入以学习准确的 SDF 和核大小。在 DTU 的前向拍摄设置下，视角覆盖有限，壳提取可能出现退化，尽管定量结果仍优于基线。

4. **内存与流程开销**：显式壳网格的存储增加了内存开销，且水平集演化提取流程（侵蚀+膨胀+Marching Cubes）增加了训练后处理步骤的复杂度。对于需要频繁更新的动态场景，这一开销可能成为瓶颈。

### 应用验证

Figure 12 展示了该方法在下游应用中的潜力。显式壳网格使表示天然适合动画和物理模拟：通过对壳网格施加蒙皮变形，辐射场可随之变换，在变形后仍保持模糊区域（毛发、叶片）的视觉质量。这为神经辐射场在交互式应用中的部署提供了新路径。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/019_Figure_11.jpg]]
*Figure 11: Ablating the efect of sample count on image quality and runtime performance. We vary the sample count, and plot the PSNR change (le ) and relative runtime performance (right) compared to the default hyperparameters denoted as “1× sample count”. We experiment with six scenes from the Shelly (fernvase, khady, ki en) and MipNeRF360 (bicycle, garden, room) data sets*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/013_Table_2.jpg]]
*Table 2: antitative results on Shelly data set, DTU data set and NeRFSynthetic data set. We report PSNR, LPIPS and SSIM. Our method achieves be er results across all metrics on Shelly and DTU and comparable results on NeRFSynthetic. Real-time denotes methods that achieve >30FPS at 1080p. On Shelly and DTU, we run NeRF and Mip-NeRF with Nerfstudio [Tancik et al. 2023], and use oficial implementation for other methods. Baselines of NeRFSynthetic are from the original papers. Detailed results for each object/scene are provided in the Supplement*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/021_Table_2.jpg]]
*Table 2: Per-scene quantitative LPIPS comparison on Shelly data set*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/022_Table_3.jpg]]
*Table 3: Per-scene quantitative SSIM comparison on Shelly dataset*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2311_10091/figures/024_Table_5.jpg]]
*Table 5: Per-scene quantitative results on DTU data set. We report the PSNR, LPIPS and SSIM results for each scene and compare them with baselines*

## 方法谱系与知识库定位

### 核心思想定位

Adaptive Shells 的核心贡献在于提出了一种**空间自适应的渲染策略**：场景中不同区域应使用不同的渲染方式。模糊几何（如毛发、叶子）需要体渲染来处理半透明和复杂形状，而实表面可以用单次采样精确表示。这一洞察直接回应了传统 NeRF 体积渲染的根本瓶颈——对所有区域统一密集采样，导致大量计算浪费在实表面区域。

该方法通过一个可学习的**空间变化核大小**（spatially-varying kernel size）$s(\mathbf{x})$ 自动适应区域复杂度：在实表面区域核大小趋近于零（退化为脉冲函数），在模糊区域核大小自适应增大。基于此核大小，通过水平集演化从 SDF 提取显式的**窄带壳体**（adaptive shell），在壳体内进行采样渲染。

### 方法谱系：从 NeRF 到 Adaptive Shells

#### 体积渲染基础线

Adaptive Shells 建立在以下体积渲染工作的基础之上：

- **NeRF**（Mildenhall et al., 2020）：奠定了神经辐射场的基础框架，通过 MLP 隐式表示场景的密度和颜色，并使用体积渲染积分进行新视角合成。其核心方程为：

  $$\mathbf{c}(\mathbf{r}) = \int_{\tau_n}^{\tau_f} \exp\Big[ \int_{\tau_n}^{\tau} -\sigma(\mathbf{r}(z)) dz \Big] \sigma(\mathbf{r}(\tau)) \mathbf{c}(\mathbf{r}(\tau), \mathbf{d}) d\tau$$

  Adaptive Shells 保留了这一体积渲染框架，但通过窄带采样大幅减少了积分区间。

- **MipNeRF**（Barron et al., 2021）：引入锥形采样和集成位置编码以解决抗锯齿问题。Adaptive Shells 在 NeRFSynthetic 数据集上与 MipNeRF 进行了对比，取得了可比的质量。

- **MipNeRF 360**（Barron et al., 2022）：将 NeRF 扩展到无界场景。Adaptive Shells 在 MipNeRF360 数据集上进行了评估，在室外场景上 PSNR 为 23.17，略低于 Instant NGP 的 23.90，但推理速度快约 5 倍（Table 3, Table 1）。

#### SDF 隐式表面表示线

Adaptive Shells 的核心技术路线直接继承自基于 SDF 的神经隐式表面重建方法：

- **NeuS**（Wang et al., 2021）：将 SDF 通过 sigmoid 函数映射为密度，实现了高质量的表面重建。其密度转换公式为：

  $$\sigma = \operatorname*{max}\left( -\frac{\frac{d\Phi_s}{d\tau}(f)}{\Phi_s(f)}, 0 \right), \qquad \Phi_s(f) = \big(1 + \exp(-f/s)\big)^{-1}$$

  其中 $s$ 为**全局常量**核大小。Adaptive Shells 的核心创新之一就是将 NeuS 中的全局核大小 $s$ 推广为**空间变化的神经网络输出** $s(\mathbf{x})$（Section 3.2）。这一推广使得核大小可以自动适应场景的局部复杂度：在实表面区域核大小趋近于零，在模糊区域核大小自适应增大（Figure 7）。

  实验表明，空间变化核（SV Kernel）相比全局核在 Shelly 数据集上 PSNR 提升约 1.7 dB（34.26→36.02），且 LPIPS、SSIM 均有改善（Table 4）。

#### 加速渲染线

Adaptive Shells 在加速渲染方面与以下工作形成对比和互补：

- **Instant NGP**（Müller et al., 2022）：通过多分辨率哈希编码和空体素跳过大幅加速 NeRF 训练和推理。Adaptive Shells 采用了相同的哈希编码架构（14 层，每层哈希表大小 $2^{22}$），但在采样策略上有本质区别：Instant NGP 仍需要在占据区域多次采样（固定 384 样本/像素），而 Adaptive Shells 通过窄带渲染将样本数减少最多 3 倍，帧率提高约 5 倍（例如 Shelly 上 262.69 FPS vs Instant NGP 85.16 FPS，Table 1）。

  在图像质量上，Adaptive Shells 在 Shelly 数据集上 PSNR 达到 36.02，比 Instant NGP 的 33.48 高 2.54 dB（Table 2）。

- **MobileNeRF**（Chen et al., 2023）：将 NeRF 烘焙到代理几何（多边形网格）以实现移动端实时渲染。Adaptive Shells 同样提取显式网格，但区别在于：MobileNeRF 使用固定代理几何，而 Adaptive Shells 提取的是**自适应宽度的窄带壳**，能够处理模糊几何。

- **BakedSDF**（Yariv et al., 2023）：将 SDF 烘焙到网格以加速渲染。Adaptive Shells 与 BakedSDF 共享 SDF 表示基础，但 Adaptive Shells 的壳提取基于空间变化核大小而非固定 SDF 阈值，消融实验表明自适应壳相比固定 SDF 阈值壳获得了更好的质量-速度权衡（Table 4, Band row）。

### 关键技术槽位变化

Adaptive Shells 相对于基线方法的关键技术槽位变化如下：

| 技术槽位 | 基线值 | 提出值 | 证据锚点 |
|---------|--------|--------|---------|
| 核大小 | 全局常量 $s$（NeuS） | 空间变化神经网络输出 $s(\mathbf{x})$ | Section 3.2, Figure 7 |
| 渲染采样策略 | 全光线密集采样（Instant NGP 384 样本/像素） | 基于显式壳的窄带渲染：射线与壳体求交，壳内等距采样，实表面可单样本 | Section 3.4, Table 1 |
| 显式几何代理 | 无显式几何（NeuS/NeRF）或固定代理（MobileNeRF/BakedSDF） | 通过水平集演化从 SDF 和 $s(\mathbf{x})$ 提取自适应宽度的内/外壳网格 | Section 3.3, Figure 4, Figure 5 |
| 训练阶段 | 单阶段全光线训练 | 两阶段：第一阶段全光线训练 SDF 和核大小，第二阶段在壳内微调辐射场并关闭正则化 | Section 3.5 |

### 适用边界与局限

1. **薄结构捕获不足**：自适应壳可能无法捕获极薄的结构（如铁丝网），因为这些结构在训练中可能未被充分表达，导致壳提取时被遗漏。

2. **无界场景的挑战**：处理复杂背景和无界场景时，背景区域的质量和速度仍有提升空间，且可能出现漂浮几何伪影。在 MipNeRF360 室外场景上，PSNR 略低于 Instant NGP（23.17 vs 23.90），尽管速度快约 5 倍（Table 3, Table 1）。

3. **多视图依赖**：方法依赖于多视图输入以学习 SDF 和核大小，在稀疏视角或前向拍摄（如 DTU）下壳提取可能退化。

4. **内存开销**：需要额外的显式网格存储（内壳和外壳两个三角形网格），增加了内存开销，且网格提取流程（水平集演化 + Marching Cubes）较为复杂。

### 开放问题

1. **薄结构覆盖保证**：如何保证自适应壳覆盖所有对渲染有贡献的薄结构？当前基于密度阈值的膨胀速度（Eq. 6）可能在极薄结构处失效。

2. **与预计算网格表示的结合**：能否将自适应壳与预计算网格表示（如 MeRF）结合，进一步加速推理？

3. **无界场景背景处理**：如何更好地处理无界场景中的背景，减少漂浮几何并提高速度？当前方法在 MipNeRF360 室外场景上仍有质量差距。

4. **动态场景扩展**：该方法是否适用于动态场景或可变形物体？文中已展示简单蒙皮变形（Figure 12），但更复杂的动态场景（如非刚性变形、拓扑变化）仍需探索。

5. **移动端部署**：能否在移动设备上通过进一步优化（如量化、蒸馏）实现实时渲染？当前帧率（40-300 FPS）在 RTX 4090 上测得，移动端部署需要显著的工程优化。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2023/Adaptive_Shells_for_Efficient_Neural_Radiance_Field_Rendering.pdf]]
