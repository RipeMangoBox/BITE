---
title: Blue Noise for Diffusion Models
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Blue_Noise_for_Diffusion_Models.pdf
project_link: "https://xchhuang.github.io/bndm/"
code_link: "https://github.com/xchhuang/bndm"
aliases:
- TVNDMB
- BNDM
tags:
- SIGGRAPH_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 噪声的空间相关性类型（高斯白噪声、高斯蓝噪声）及其随扩散时间步变化的混合调度γ_t；训练时小批次内噪声与图像的配对方式（纠正映射）。
primary_logic: 利用扩散模型从粗到精（低频到高频）的生成特性，在训练早期使用高斯白噪声建立低频结构，后期引入高频蓝噪声以增强细节生成，从而提升生成质量。
claims:
- 在所有评估数据集上，本文方法相比IADB取得了更低的FID分数。
- 时变噪声的影响在扩散过程约t=75时开始显现，本文方法生成更逼真的细节。
- 消融实验显示，混合高斯白噪声和高斯蓝噪声的组合取得了最佳的FID和精度/召回率。
- 在LSUN-Church超分辨率任务中，本文方法的SSIM和PSNR均高于IADB。
---

# Blue Noise for Diffusion Models

> [!tip] 核心洞察
> 利用扩散模型从粗到精（低频到高频）的生成特性，在训练早期使用高斯白噪声建立低频结构，后期引入高频蓝噪声以增强细节生成，从而提升生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扩散模型中的蓝噪声 |
| 英文题名 | Blue Noise for Diffusion Models |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://xchhuang.github.io/bndm/) · [Code](https://github.com/xchhuang/bndm) · [Project](https://xchhuang.github.io/bndm/") |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Time-varying Noise Diffusion Model (BNDM) |
| Dataset | AFHQ-Cat 64×64, CelebA 64×64, LSUN-Church 64×64, CelebA 128×128 |

> [!tip] 效果简介
> - AFHQ-Cat 64×64 上，FID (lower is better) 7.95 vs 9.19 (IADB) (-1.24)。
> - CelebA 64×64 上，FID 7.05 vs 7.53 (IADB) (-0.48)。
> - LSUN-Church 64×64 上，FID 10.16 vs 13.12 (IADB) (-2.96)。

## 概要

现有扩散模型在训练全程使用无空间相关的高斯白噪声，未针对去噪网络在不同扩散阶段对频率成分的差异化需求进行优化，限制了生成图像细节质量。本文提出**时变噪声扩散模型（BNDM）**，核心思想是：在扩散早期用高斯白噪声建立低频结构，后期切换为富含高频的**高斯蓝噪声**以增强细节生成。方法基于确定性扩散框架IADB，通过Cholesky分解预计算蓝噪声相关矩阵，实现训练时**即时生成相关噪声掩码**（额外开销仅约0.0002秒），并设计**时变混合调度**$\gamma_t$控制白/蓝噪声的过渡。

在AFHQ-Cat、CelebA、LSUN-Church等多个数据集上，BNDM相比IADB取得一致的FID改善（如CelebA 128²上FID从20.71降至16.38），在超分辨率任务上SSIM和PSNR均有提升。消融实验证实混合白/蓝噪声优于单一噪声类型，且蓝噪声相比白噪声在更高噪声幅值下更好地保留细节。该方法属于**训练噪声设计**的技术路线，通过改变噪声空间相关性而非网络架构来提升生成质量。

## 核心方法与创新机理

### 问题背景与核心瓶颈

扩散模型通过逐步向数据添加噪声并学习逆向去噪来生成图像。现有确定性扩散模型（如 **IADB** (Heitz et al., SIGGRAPH 2023)）在整个扩散过程中统一使用各向同性的高斯白噪声 $\epsilon \sim \mathcal{N}(0, I)$，其协方差矩阵为单位阵，各像素间无空间相关性。这种设计存在一个被忽视的瓶颈：扩散模型具有从粗到精（低频到高频）的生成特性——早期步骤建立图像的整体结构，后期步骤则负责细节重建。然而，高斯白噪声在所有时间步提供均匀分布的频率成分，并未针对去噪网络在不同扩散阶段对频率信息的需求进行差异化供给，从而限制了生成图像在细节层面的质量上限。

本文的核心洞察在于：**利用扩散模型从低频到高频的生成特性，在训练早期使用高斯白噪声建立低频结构，后期引入富含高频成分的高斯蓝噪声以增强细节生成能力**。这一思路将噪声的空间相关性与扩散时间步耦合，使噪声的频率特性与去噪网络当前阶段的需求相匹配。

### 高斯蓝噪声的生成机制

高斯蓝噪声是一种具有特定空间相关性的噪声，其功率谱在高频区域能量更高，表现为空间上更均匀的分布特性。要生成具有指定协方差矩阵 $\Sigma$ 的相关噪声掩码，本文采用 Cholesky 分解方法：

$$ \mathbf{b} = L \epsilon $$

其中 $L$ 是 $\Sigma$ 的下三角 Cholesky 分解矩阵（$LL^T = \Sigma$），$\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯白噪声。通过预计算蓝噪声协方差矩阵的 Cholesky 分解 $L_b$，可以在训练过程中即时生成高斯蓝噪声掩码 $\mathbf{b}$。

**核心改进一：低分辨率生成与填充平铺。** 直接在高分辨率（如 $128^2$）上计算 Cholesky 分解并生成噪声掩码面临严重的计算瓶颈（图 3 中 $L$ 矩阵尺寸为 $N \times N$，$N$ 为像素总数）。本文提出在低分辨率（如 $64^2$）上生成蓝噪声掩码，然后通过填充（padding）方式平铺到目标高分辨率。这一方法将计算开销降至约 **0.0002 秒**，使得在训练循环中实时生成相关噪声成为可行。

### 时变噪声扩散框架

本文的核心创新在于将噪声的空间相关性与扩散时间步耦合，构建时变噪声扩散模型（Time-varying Noise Diffusion Model）。

#### 噪声混合机制

定义时变噪声矩阵 $L_t$ 为高斯白噪声矩阵 $L_w$ 与高斯蓝噪声矩阵 $L_b$ 的凸组合：

$$ L_t = \gamma_t L_w + (1 - \gamma_t) L_b \quad \text{(Eq. 5)} $$

其中 $\gamma_t \in [0, 1]$ 是时间步 $t$ 的函数，控制两种噪声的混合比例。当 $\gamma_t = 1$ 时，噪声退化为高斯白噪声；当 $\gamma_t = 0$ 时，噪声为纯高斯蓝噪声。$L_w = I$（单位阵），$L_b$ 为预计算的蓝噪声 Cholesky 分解矩阵。

#### 前向扩散过程

给定目标图像 $\mathbf{x}_0$ 和时间步 $t$，前向过程将时变噪声与目标图像进行插值：

$$ \mathbf{x}_t = \alpha_t (L_t \epsilon) + (1 - \alpha_t) \mathbf{x}_0 \quad \text{(Eq. 6)} $$

其中 $\alpha_t$ 是标准的扩散调度系数（随 $t$ 单调递减），$\epsilon \sim \mathcal{N}(0, I)$。与 IADB 的前向过程 $\mathbf{x}_t = \alpha_t \epsilon + (1 - \alpha_t) \mathbf{x}_0$ 相比，本文仅将各向同性噪声 $\epsilon$ 替换为相关噪声 $L_t \epsilon$。

#### 确定性逆向过程

从 IADB 的逆向步骤 $\mathbf{x}_{t-1} = \mathbf{x}_t + (\alpha_t - \alpha_{t-1}) f_{\theta}(\mathbf{x}_t, t)$ 出发，本文推导了时变噪声下的确定性逆向步骤：

$$ \mathbf{x}_{t-1} = \mathbf{x}_t + (\alpha_t - \alpha_{t-1}) (\mathbf{x}_0 - L_t \epsilon) + (\gamma_t - \gamma_{t-1}) \alpha_{t-1} (L_b \epsilon - L_w \epsilon) \quad \text{(Eq. 7)} $$

**因果机制分析**：与 IADB 相比，逆向步骤中新增了第三项 $(\gamma_t - \gamma_{t-1}) \alpha_{t-1} (L_b \epsilon - L_w \epsilon)$。该项仅在 $\gamma_t \neq \gamma_{t-1}$ 时非零，即仅在噪声混合比例发生变化的时间步生效。这意味着：

- 在扩散早期（$\gamma_t \approx 1$，$\gamma_t - \gamma_{t-1} \approx 0$），第三项消失，模型行为与 IADB 基本一致，专注于全局结构重建。
- 在扩散中后期（$\gamma_t$ 开始下降），第三项被激活，模型需要额外预测蓝噪声与白噪声的差异，从而学习高频细节的生成。

#### 网络输出维度扩展

**核心改进二：6 通道输出。** 为支持时变噪声的逆向过程，去噪网络需要同时预测两项：

1. $\mathbf{x}_0 - L_t \epsilon$：目标图像与当前噪声的差值（对应 Eq. 7 第二项）。
2. $\alpha_{t-1} (L_b \epsilon - L_w \epsilon)$：蓝噪声与白噪声的加权差异（对应 Eq. 7 第三项）。

因此，网络输出从 IADB 的 3 通道（RGB 图像）扩展为 **6 通道**（两个 3 通道预测）。网络架构仍为 U-Net，仅修改输出卷积层的通道数。

#### 复合损失函数

训练损失函数由两项加权平方和组成：

$$ \mathcal{L}_{Ours} = \sum_t \left( (f_{\theta}'(\mathbf{x}_t, t) - (\mathbf{x}_0 - L_t \epsilon))^2 + \frac{\gamma_t - \gamma_{t-1}}{\alpha_t - \alpha_{t-1}} (f_{\theta}''(\mathbf{x}_t, t) - \alpha_{t-1} (L_b \epsilon - L_w \epsilon))^2 \right) \quad \text{(Eq. 8)} $$

其中 $f_{\theta}'$ 和 $f_{\theta}''$ 分别为网络的第一个和第二个 3 通道输出。权重系数 $\frac{\gamma_t - \gamma_{t-1}}{\alpha_t - \alpha_{t-1}}$ 自动调节第二项的重要性：当 $\gamma_t$ 变化剧烈时（噪声类型切换阶段），第二项权重增大，迫使网络更精确地学习蓝噪声的影响；当 $\gamma_t$ 稳定时，第二项权重趋近于零，网络专注于标准去噪任务。

### 噪声调度策略

$\gamma_t$ 函数采用基于 sigmoid 的参数化形式：

$$ \gamma_t = \text{sigmoid}\left(\frac{\text{start} + (\text{end} - \text{start}) \cdot t / T}{\tau}\right) \quad \text{(Eq. 9)} $$

其中 $\text{start}$ 和 $\text{end}$ 控制 sigmoid 的输入范围，$\tau$ 控制过渡的平滑程度，$T$ 为总扩散步数。该调度函数使噪声从早期的高斯白噪声（$\gamma_t \approx 1$）平滑过渡到后期的高斯蓝噪声（$\gamma_t \approx 0$）。实验中设置 $\tau = 0.2$，使得时变噪声的影响在约 $t = 75$（总步数 $T=1000$）时开始显现。

### 纠正映射机制

**核心改进三：小批次内噪声-图像最优配对。** 标准训练中，每个小批次内的噪声 $\epsilon$ 与目标图像 $\mathbf{x}_0$ 之间采用随机映射。本文观察到，当噪声与图像在像素空间中的距离较近时，训练信号更强。为此，提出纠正映射（Rectified Mapping）：在小批次内计算所有噪声与图像之间的成对 $L_2$ 距离，然后通过贪心匹配算法为每个噪声选择距离最近的未配对图像，使整体配对距离最小化。

这一机制在低扩散步数时显著降低 FID（Table 2），因为此时训练更依赖有效的配对信号；在高步数时效果略有减弱，因为模型已有足够容量从随机配对中学习。

![[assets/figures/papers/paper_list_l32_https_xchhuang_github_io_bndm/figures/010_Table_2.jpg]]
*Table 2: Comparing the impact of rectified mapping during training on AFHQ-Cat (642). FID scores (↓) are provided with and without rectified mapping across different step counts. Correlation in the mini-batch results in lower FID at low steps but higher during slow diffusion*

### 模块因果关系总结

整个方法的模块链路与因果关系如下：

1. **蓝噪声矩阵预计算** → 提供 $L_b$，使实时噪声生成成为可能。
2. **即时噪声掩码生成** → 利用 $L_b$ 和 $\epsilon$ 生成 $\mathbf{b} = L_b \epsilon$，计算开销仅 0.0002 秒。
3. **时变噪声混合** → $L_t = \gamma_t L_w + (1 - \gamma_t) L_b$ 将噪声频率特性与时间步耦合。
4. **前向过程** → $\mathbf{x}_t = \alpha_t (L_t \epsilon) + (1 - \alpha_t) \mathbf{x}_0$ 将时变噪声注入训练样本。
5. **6 通道 U-Net** → 同时预测去噪所需的两项，支持时变逆向过程。
6. **复合损失函数** → 通过自适应权重平衡两项学习目标。
7. **逆向过程** → 利用网络预测的两项执行确定性去噪，在后期步骤中引入蓝噪声的高频信息以增强细节。
8. **纠正映射** → 优化小批次内噪声-图像配对，提升训练效率。

**因果链**：$\gamma_t$ 调度 → 噪声频率成分变化 → 网络被迫学习高频细节 → 逆向过程利用蓝噪声信息 → 生成图像细节增强。这一链条的核心在于 $\gamma_t$ 的过渡阶段（$t \approx 75$ 开始），此时网络必须同时处理白噪声的结构信息和蓝噪声的细节信息，从而在生成过程中形成更丰富的频率表达。

![[assets/figures/papers/paper_list_l32_https_xchhuang_github_io_bndm/figures/019_Figure_12.jpg]]
*Figure 12: Image generation comparisons between DDIM, IADB and Ours trained on CelebA (1282) and AFHQ-Cat (1282) datasets, respectively. All methods start with the same initial Gaussian noise during the backward process. Our method generates more realistic content around the hair, eye, mouth regions compared to IADB. Compared to DDIM, our method achieves similar visual quality. The impact of time-varying noise (we use ?? = 0.2 in Eq. (9)) can be seen by comparing IADB and ours starting from around ?? = 75*

## 实验与关键发现

### 主要生成质量对比

本文在多个标准数据集上与确定性扩散模型基线进行了系统对比，所有方法均使用相同的 U-Net 架构、训练步数（T=1000）、测试步数（τ=250）、AdamW 优化器（学习率 0.0001）和硬件环境（4× NVIDIA Quadro RTX 8000），确保比较的公平性。核心基线为 **IADB**（Heitz et al., SIGGRAPH 2023），因为本文方法直接构建于其确定性扩散框架之上。

Table 1 汇总了各模型在 64×64 和 128×128 分辨率下的 FID 分数。本文方法（BNDM）在所有评估数据集上均优于 IADB，且差距在复杂场景下更为显著：

![[assets/figures/papers/paper_list_l32_https_xchhuang_github_io_bndm/figures/009_Table_1.jpg]]
*Table 1: Quantitative FID score comparisons among IHDM [Rissanen et al. 2023], DDPM [Ho et al. 2020], DDIM [Song et al. 2021a], IADB [Heitz et al. 2023], and our method across diverse datasets. Notably, our approach exhibits improvements over IADB on every evaluated dataset. While our method is outperformed by DDIM on only one dataset, it’s worth noting that IADB also performs poorly on the same dataset. Additional metrics are provided in the Supplemental document Sec. 3*

- **AFHQ-Cat 64×64**：FID 从 IADB 的 9.19 降至 **7.95**（Δ = -1.24）
- **CelebA 64×64**：FID 从 7.53 降至 **7.05**（Δ = -0.48）
- **LSUN-Church 64×64**：FID 从 13.12 降至 **10.16**（Δ = -2.96）
- **CelebA 128×128**：FID 从 20.71 降至 **16.38**（Δ = -4.33）

值得注意的是，DDIM 在 CelebA 128² 上取得了 11.92 的 FID，优于本文的 16.38。但 IADB 在同一数据集上也表现不佳（20.71），说明该确定性扩散框架本身在特定高分辨率人脸数据上存在系统性劣势，而非时变噪声引入的问题。

在 **LSUN-Church 超分辨率任务**（32→128）中，本文方法在像素级保真度指标上也优于 IADB：SSIM 从 0.57 提升至 **0.59**，PSNR 从 19.46 提升至 **20.00**。Fig. 6 的可视化对比显示，本文方法生成的结构更符合真实参考图像，减少了幻觉性细节。

![[assets/figures/papers/paper_list_l32_https_xchhuang_github_io_bndm/figures/012_Figure_6.jpg]]
*Figure 6: Image super-resolution comparisons between IADB (SSIM/P-SNR=0.57/19.46) and Ours (SSIM/PSNR=0.59/20.00) on LSUN-Church (322 → 1282). The mean squared error w.r.t the reference is visible in the upper corner with the relative error to IADB. Our method achieves lower error and more plausible details with less hallucination*

在 **潜在扩散模型（LDM）** 的高分辨率生成场景（AFHQ-Cat 512×512）中，本文方法将 FID 从 IADB 的 12.19 降至 **11.45**（Δ = -0.74），尤其在眼部区域减少了伪影（Fig. 9）。

### 时变噪声效应的时序分析

Fig. 12 揭示了时变噪声产生可观察影响的关键时间窗口。在 CelebA 128² 和 AFHQ-Cat 128² 的生成过程中，从相同的初始高斯噪声出发，本文方法与 IADB 的差异约在 **t ≈ 75** 时开始显现（使用 τ=0.2 的 γ_t 调度器）。此后，本文方法在头发纹理、眼部细节和嘴部区域生成了更逼真的内容。这一观察与核心假设一致：扩散后期（低噪声水平阶段）主要重建高频细节，此时引入蓝噪声的空间相关性能够有效引导网络学习更精细的纹理结构。

### 消融实验：噪声类型组合

Table 3 在 AFHQ-Cat 128² 上系统消融了不同噪声类型对生成质量的影响，同时报告了 FID、Precision 和 Recall 三个维度：

![[assets/figures/papers/paper_list_l32_https_xchhuang_github_io_bndm/figures/011_Table_3.jpg]]
*Table 3: Ablation study on different combinations of noises using our framework on AFHQ-Cat (1282). The last two rows mean blending Gaussian noise with Gaussian red or blue noise using the ??-scheduler with ?? = 0.2*

- **仅高斯白噪声**：FID = 10.81，Precision = 0.68，Recall = 0.42
- **仅高斯蓝噪声**：FID = 17.61，Precision = 0.72，Recall = 0.27
- **混合白噪声 + 蓝噪声**（本文方案）：FID = **9.47**，Precision = 0.69，Recall = 0.45
- **混合白噪声 + 红噪声**：FID = 12.65，Precision = 0.60，Recall = 0.43

仅使用蓝噪声严重损害了 Recall（0.27 vs. 0.42），说明纯高频噪声破坏了模型对数据分布整体覆盖的能力。混合方案在三个指标上取得了最佳平衡，验证了“早期白噪声建立低频结构、后期蓝噪声增强高频细节”的分阶段策略的有效性。

高斯红噪声的引入导致 Precision 降至 0.60，且产生可见伪影（Fig. 7），进一步证实了低频相关噪声不适合细节生成阶段。

### 消融实验：纠正映射

Table 2 评估了纠正映射（rectified mapping）在不同扩散步数下的影响。在 AFHQ-Cat 64² 上：

- 低步数（τ=10）时，纠正映射将 FID 从 33.54 降至 **27.32**，效果显著
- 中步数（τ=50）时，FID 从 13.29 降至 **11.64**
- 高步数（τ=250）时，纠正映射反而使 FID 从 8.02 略微升至 **8.50**

这一趋势表明，小批次内的噪声-图像配对优化在快速采样场景下作用更大，因为此时每一步的去噪幅度更大，配对质量直接影响重建精度。而在充分扩散步数下，模型有足够机会修正初始配对偏差，纠正映射的边际收益消失甚至转为轻微负面影响。

### 噪声幅值鲁棒性

Fig. 8 展示了在不同噪声幅值下，高斯蓝噪声相比高斯白噪声的细节保留能力。随着噪声幅值增加，蓝噪声方案更好地维持了图像的细节和内容完整性。当噪声幅值达到 100% 时，两者均退化为完全生成模式，差异缩小。这一特性使得本文方法在需要强噪声扰动的应用场景（如图像编辑中的大幅度修改）中具有潜在优势。

![[assets/figures/papers/paper_list_l32_https_xchhuang_github_io_bndm/figures/013_Figure_8.jpg]]
*Figure 8: Evaluating the impact of noise magnitude on detail enhancement. Our Gaussian blue noise method better preserves fine details even with increased noise magnitude, while maintaining the integrity of the content. With 100% noise, both models fall back to full generative process*

### 失败模式与适用边界

1. **框架依赖性**：本文方法严格建立在 IADB 的确定性扩散框架上。当底层框架本身在特定数据集上表现不佳时（如 CelebA 128² 上 IADB 的 FID 高达 20.71），时变噪声的改进虽显著（降至 16.38），但仍无法弥合与 DDIM（11.92）的差距。这表明时变噪声是对基础框架的增强，而非替代。

2. **高分辨率噪声掩码生成**：蓝噪声掩码通过低分辨率生成后填充平铺至高分辨率的方式实现。虽然计算开销极低（约 0.0002 秒），但填充操作可能引入不可见的接缝伪影。相关矩阵的估计依赖于从现有蓝噪声掩码集合中近似，并非理论最优解。

3. **纠正映射的可扩展性**：当前纠正映射机制仅适用于单 GPU 训练。扩展到多 GPU 分布式训练时，跨 GPU 的全局最优配对需要额外的同步机制，尚未解决。

4. **调度策略的经验性**：γ_t 的 sigmoid 调度器参数（start、end、τ）目前基于经验选择和简单搜索，缺乏针对不同任务的自适应优化方法。论文明确指出“如何更高效地选择 gamma-scheduler 需要未来进一步研究”。

## 定位与知识库关联

### 相对于基线方法的核心改变

本文提出的时变噪声扩散模型（BNDM）直接建立在确定性扩散模型 **IADB**（Heitz et al., SIGGRAPH 2023）的框架之上。IADB 的核心机制是通过确定性前向过程将目标图像与各向同性高斯白噪声进行线性混合，网络学习预测两者之差以实现一步去噪。BNDM 对 IADB 的改造并非架构层面的重构，而是精确定位于**噪声生成槽位**的替换：将 IADB 中恒定的无相关高斯白噪声（协方差矩阵为单位矩阵 $I$）替换为随时间步 $t$ 变化的混合相关噪声 $L_t \epsilon$，其中 $L_t = \gamma_t L_w + (1-\gamma_t) L_b$。这一替换直接触发了三个连锁改变：

1. **网络输出维度的扩展**：由于时变噪声的反向过程需要同时预测两项——去噪结果 $\mathbf{x}_0 - L_t \epsilon$ 和噪声成分变化量 $\alpha_{t-1}(L_b \epsilon - L_w \epsilon)$，网络输出从 IADB 的 3 通道扩展为 6 通道。
2. **损失函数的复合化**：损失函数从单一的均方误差扩展为包含两项加权平方和的复合损失（Eq. 8），权重系数 $(\gamma_t - \gamma_{t-1})/(\alpha_t - \alpha_{t-1})$ 由噪声调度和扩散调度共同决定。
3. **训练批内配对策略的引入**：为充分利用蓝噪声的空间相关性，提出纠正映射（rectified mapping）机制，在小批次内最小化噪声与图像的成对 L2 距离，替代随机配对。

与另一频率控制基线 **IHDM**（Rissanen et al., ICLR 2023）相比，IHDM 通过在频域对噪声进行频谱整形来控制不同频率成分的学习速度，但其噪声本身在空间域仍保持无相关特性。BNDM 则直接在空间域引入相关噪声，且噪声的相关性随时间步平滑过渡，实现了从低频结构到高频细节的渐进式生成引导。与 **DDIM**（Song et al., ICLR 2021）和 **DDPM**（Ho et al., NeurIPS 2020）相比，BNDM 保持了确定性反向过程的简洁性，但通过噪声相关性的时变控制弥补了确定性模型在细节生成上的不足。

### 知识库挂载点

BNDM 在知识图谱中的挂载点可定位为**扩散模型噪声设计**与**蓝噪声采样理论**的交叉节点：

- **扩散模型分支**：BNDM 归属确定性扩散模型子类，其前向/反向过程的数学骨架继承自 IADB 的 $\alpha_t$-混合框架。在知识库中，它应挂载在“扩散模型 > 确定性扩散 > 噪声调度与噪声类型”节点下，与 DDIM、IADB 构成同一分支的演进关系。
- **蓝噪声理论分支**：BNDM 的噪声生成方法依赖蓝噪声的相关矩阵估计和 Cholesky 分解，其理论基础来自计算机图形学中的蓝噪声采样研究。相关矩阵 $\Sigma$ 的估计需要从现有蓝噪声掩码集合中近似，这一步骤在知识库中应链接到“蓝噪声生成 > 相关矩阵估计”节点。
- **训练策略分支**：纠正映射机制将匈牙利算法式的配对思想引入扩散模型训练，属于“训练技巧 > 批内数据配对”节点，与对比学习中的难例挖掘策略存在概念关联。

### 适用边界与限制

BNDM 的适用边界由以下约束定义：

1. **确定性扩散框架依赖**：BNDM 的时变噪声机制深度耦合 IADB 的确定性反向过程，无法直接迁移到 DDPM 等随机扩散模型或基于分数的 SDE 框架。论文明确指出这一限制，且未提供向随机模型的扩展路径。
2. **相关矩阵估计的近似性**：蓝噪声相关矩阵 $\Sigma$ 需从预生成的蓝噪声掩码集合中统计估计，这一近似过程可能引入偏差。论文未系统评估不同相关矩阵估计方法对生成质量的影响。
3. **纠正映射的单 GPU 限制**：纠正映射的全局配对策略依赖整个小批次内的距离计算，在多 GPU 分布式训练场景下需要跨 GPU 同步，论文未给出解决方案。
4. **噪声调度的经验性**：$\gamma_t$ 的 sigmoid 调度函数参数（start、end、$\tau$）基于经验选择，缺乏自动化优化方法。论文在开放问题中承认了这一局限。

在实验覆盖面上，BNDM 在 AFHQ-Cat、CelebA、LSUN-Church 等中小分辨率数据集上验证了有效性，并在潜在扩散模型的 512×512 高分辨率生成中展示了初步结果。但论文未在文本到图像生成、可控生成等更复杂的条件生成任务上进行评估，其在这些场景下的适用性需要进一步验证。

### 后续工作启发

BNDM 的核心洞察——利用扩散模型从粗到精的生成特性，在后期引入高频噪声以增强细节——为后续研究提供了几个可扩展的方向：

1. **噪声类型的泛化**：论文的消融实验（Table 3）显示高斯红噪声严重降低精度，表明并非所有相关噪声都有益。后续工作可探索其他噪声频谱（如绿噪声、粉红噪声）或可学习的噪声相关矩阵，以针对不同任务自适应调整频率偏好。
2. **时变噪声向随机扩散的迁移**：如何将 $L_t$ 的时变机制嵌入 DDPM 的随机反向过程，或与基于分数的生成模型结合，是一个直接的理论扩展方向。
3. **纠正映射的分布式实现**：将批内配对策略推广到多 GPU 训练，可通过局部配对与全局通信的混合策略实现，类似于分布式对比学习的实现思路。
4. **噪声调度的自动化**：将 $\gamma_t$ 调度函数参数化为可学习模块，或通过元学习、神经架构搜索等方法自动优化，可提升方法对不同任务的适应性。
5. **跨模态扩展**：论文在开放问题中提及视频生成和 3D 内容生成，蓝噪声的空间相关性在这些领域中可能有助于提升时空一致性和几何细节。

总体而言，BNDM 通过精确替换扩散模型中的噪声生成槽位，以极小的计算开销（约 0.0002 秒的额外噪声生成时间）实现了生成质量的系统性提升。其在知识库中的定位清晰，适用边界明确，为扩散模型的噪声设计提供了一个可泛化的研究范式。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Blue_Noise_for_Diffusion_Models.pdf]]