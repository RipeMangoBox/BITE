---
title: "MaxMark: High-Capacity Diffusion-Native Watermarking via Robust and Invertible Latent Embedding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MaxMark_High_Capacity_Diffusion_Native_Watermarking_via_Robust_and_Invertible_Latent_Embedding.pdf
project_link: null
code_link: "https://github.com/SeRAlab/MaxMark"
aliases:
- MaxMark
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过分布变换模块（INN）将有水印的潜变量重新映射回标准高斯分布，确保生成过程不受干扰；同时利用INN的可逆性实现精确恢复，并结合符号位鲁棒嵌入和自动ECC调优，在不牺牲图像质量的前提下实现高容量水印。
primary_logic: 利用INN的可逆性和分布匹配能力，将大容量水印嵌入转化为一个分布保持问题，从而在LDM原生潜空间中实现高保真、高容量的水印；符号位作为最可靠的嵌入位置，加上自动参数搜索的Reed-Solomon码，进一步保障了高容量下的恢复鲁棒性。
claims:
- 在Stable Diffusion V1.5上，16,384 bits有效载荷下MaxMark的比特准确率达到95.4%，相对最优基线提升46%。
- 移除分布变换模块后，1,024 bits时FID从42.0急剧升高至388.4，验证了分布保持对图像质量的关键作用。
- Stable Diffusion v1.5 上 Bit Accuracy (clean) @ 16384 bits = 95.4%
- Stable Diffusion v1.5 上 FID @ 16384 bits = 41.8
---

# MaxMark: High-Capacity Diffusion-Native Watermarking via Robust and Invertible Latent Embedding

> [!tip] 核心洞察
> 利用INN的可逆性和分布匹配能力，将大容量水印嵌入转化为一个分布保持问题，从而在LDM原生潜空间中实现高保真、高容量的水印；符号位作为最可靠的嵌入位置，加上自动参数搜索的Reed-Solomon码，进一步保障了高容量下的恢复鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MaxMark：基于鲁棒可逆潜空间嵌入的高容量扩散原生水印 |
| 英文题名 | MaxMark: High-Capacity Diffusion-Native Watermarking via Robust and Invertible Latent Embedding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chang_MaxMark_High-Capacity_Diffusion-Native_Watermarking_via_Robust_and_Invertible_Latent_Embedding_CVPR_2026_paper.html) · [Code](https://github.com/SeRAlab/MaxMark) |
| Topic | #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/generative_models_diffusion/diffusion_image_video |
| Method | MaxMark |
| Dataset | Stable Diffusion v1.5, Stable Diffusion v1.5, multiple payloads |

> [!tip] 效果简介
> - Stable Diffusion v1.5 上，Bit Accuracy (clean) @ 16384 bits 95.4% vs ~49.4% (best baseline) (+46% improvement)；FID @ 16384 bits 41.8 vs comparable to no-watermark baseline (no significant degradation)。
> - Stable Diffusion v1.5, multiple payloads 上，Bit Accuracy improvement over baselines MaxMark vs Gaussian Shading / PRC Watermark (12% / 45% / 46% at 8,192 / 12,288 / 16,384 bits)。

## 概要

**MaxMark** 是发表于 CVPR 2026 的一种高容量扩散原生水印方法，旨在解决现有潜空间水印方案在大容量嵌入时面临的核心瓶颈：对潜噪声的扰动破坏了潜在扩散模型（LDM）的高斯先验分布，导致生成图像质量急剧下降，从而严重限制了有效载荷的提升空间。

**核心洞察**：MaxMark 将高容量水印嵌入重新定义为分布保持问题。其关键因果旋钮在于引入基于可逆神经网络（INN）的分布变换模块，将携带水印的潜变量显式映射回标准高斯分布，确保后续扩散生成过程不受干扰；同时利用 INN 的可逆性实现水印的精确恢复。在此基础上，方法通过仅覆盖潜噪声符号位并施加边缘裕量来增强嵌入鲁棒性，并采用 Reed-Solomon 纠错码配合自动超参数搜索，进一步保障高容量下的恢复精度。

**主要结果**：在 Stable Diffusion V1.5 上，MaxMark 在 16,384 bits 有效载荷下实现 95.4% 的比特准确率，相对最优基线（约 49.4%）提升约 46 个百分点，且图像质量（FID 41.8）与无水印基线相当。消融实验表明，移除分布变换模块后，1,024 bits 时 FID 从 42.0 急剧升高至 388.4，直接验证了分布保持对图像质量的关键作用。

**方法定位**：与 **Gaussian Shading**（Yang et al., CVPR 2024）和 **PRC Watermark**（Gunn et al., 2025）等基于潜空间的基线方法相比，MaxMark 在嵌入策略（符号位覆盖 vs. 通用扰动）、分布保持机制（显式 INN 映射 vs. 无显式变换）和纠错码方案（Reed-Solomon + 自动搜索 vs. 伪随机码/手工设定）三个关键维度上进行了系统性改进。

潜扩散模型（Latent Diffusion Models, LDMs）已成为生成高保真图像的主流范式，其生成内容的溯源与版权保护需求日益迫切。扩散原生水印（Diffusion-Native Watermarking）将水印直接嵌入扩散过程的潜空间中，使水印信息随生成过程自然传播，从而在不改变推理管线的前提下实现内容溯源。然而，现有方法面临一个根本性瓶颈：**大容量嵌入时，对潜空间的扰动破坏了LDM所依赖的高斯先验分布，导致图像质量严重下降**。

具体而言，以 **Gaussian Shading**（Yang et al., CVPR 2024）和 **PRC Watermark**（Gunn et al., 2025）为代表的基于潜空间的水印方法，直接在潜噪声值上叠加扰动来嵌入信息。当水印载荷较小时，这种扰动对高斯分布的偏离尚可容忍；但随着载荷增大——例如从数百比特提升至数千乃至上万比特——扰动幅度和覆盖范围不得不增加，潜变量的统计特性逐渐偏离标准高斯分布。由于LDM的去噪过程被训练为从高斯噪声出发逐步生成图像，这种分布偏移会被扩散过程放大，最终在生成图像中表现为严重的伪影和保真度损失。

这一瓶颈直接限制了水印容量的提升。在需要嵌入多层元数据（如生成时间、模型版本、用户标识、版权声明等）的实际场景中，数百比特的容量远远不够。因此，**如何在不牺牲图像质量的前提下实现高容量水印嵌入，成为扩散原生水印领域的核心挑战**。

本文提出 **MaxMark**，核心洞察在于：将大容量水印嵌入转化为一个**分布保持问题**。通过引入基于可逆神经网络（Invertible Neural Network, INN）的分布变换模块，MaxMark 将有水印的潜变量显式映射回标准高斯分布，确保生成过程不受扰动影响；同时利用 INN 的可逆性实现水印的精确恢复。此外，MaxMark 仅覆盖潜噪声的符号位（sign bit）作为嵌入位置——这是潜变量中对扰动最鲁棒的部分——并结合自动参数搜索的 Reed-Solomon 纠错码，进一步保障高容量下的恢复鲁棒性。

在 Stable Diffusion V1.5 上，MaxMark 在 16,384 bits 有效载荷下实现 95.4% 的比特准确率，相对最优基线提升 46%，且图像质量（FID 41.8）与无水印基线相当。移除分布变换模块后，仅 1,024 bits 时 FID 便从 42.0 急剧升高至 388.4，验证了分布保持对图像质量的关键作用。

## 核心方法与创新机理

MaxMark 的核心创新在于将高容量扩散原生水印重新定义为一个**分布保持问题**，通过三个紧密协作的“changed slots”突破了现有潜空间水印方法在大容量嵌入时图像质量与提取精度不可兼得的瓶颈。

### 瓶颈分析：潜空间扰动与高斯先验的冲突

现有基于潜空间的水印方法（如 **Gaussian Shading** (Yang et al., CVPR 2024) 和 **PRC Watermark** (Gunn et al., 2025)）直接在潜噪声上叠加扰动以嵌入信息。当水印载荷增大时，扰动强度随之增加，导致带水印的潜变量分布严重偏离 LDM 所依赖的标准高斯先验 $\mathcal{N}(0,I)$。这种分布失配在扩散生成过程中被逐级放大，最终造成图像质量的急剧恶化——这是限制水印容量提升的根本瓶颈。MaxMark 的因果调控旋钮正是针对这一瓶颈设计：不再试图“减轻”扰动，而是通过可逆变换将扰动后的分布“拉回”标准高斯，从而在机制层面解耦水印嵌入与图像生成。

### Changed Slot 1：嵌入位置与策略——符号位覆盖与边缘强化

传统方法通常在整个潜噪声值上施加加性或乘性扰动，但不同比特位对扰动的鲁棒性存在显著差异。MaxMark 识别出**符号位是潜空间中信息承载最可靠的位置**，因为符号决定了潜变量的方向，在扩散去噪和图像扰动下具有天然的抗干扰能力。

具体嵌入策略如公式所示：

$$x_{i}^{\prime} = \sigma(s_{i}) x_{i} \pm \beta, \quad \sigma(s_{i}) = 2 s_{i} - 1$$

该操作直接覆盖潜噪声 $x_i$ 的符号位以嵌入水印比特 $s_i$，并引入边缘参数 $\beta$ 将修改后的值推离零值附近，进一步增强对噪声和压缩等攻击的鲁棒性。消融实验（Figure 5）证实，与其他比特位相比，符号位嵌入在保持图像质量的同时实现了最高的提取准确率，验证了该位置选择的最优性。

### Changed Slot 2：分布保持机制——基于 INN 的显式分布变换

这是 MaxMark 最关键的创新。Gaussian Shading 等方法通过精心设计扰动模式来“尽量”维持高斯特性，但缺乏显式的分布校正机制，在大容量时必然失效。MaxMark 引入了一个**基于可逆神经网络（INN）的分布变换模块**，将带水印的潜变量显式地映射回标准高斯分布。

INN 采用非对称耦合块结构，其前向传播为：

$$\begin{array} { r } { s _ { a } ^ { i } , t _ { a } ^ { i } = f _ { a } ^ { i } ( z _ { a } ^ { i - 1 } ) , z _ { b } ^ { i } = \phi ( z _ { b } ^ { i - 1 } , s _ { a } ^ { i } , t _ { a } ^ { i } ) } \\ { s _ { b } ^ { i } , t _ { b } ^ { i } = f _ { b } ^ { i } ( z _ { b } ^ { i } ) , z _ { a } ^ { i } = \phi ( z _ { a } ^ { i - 1 } , s _ { b } ^ { i } , t _ { b } ^ { i } ) } \end{array}$$

其中 $\phi(z, s, t) = z e^s + t$ 为乘性耦合函数，$f_a^i$ 和 $f_b^i$ 为可学习的子网络。训练时通过最大化似然损失与 KL 散度的加权和来匹配目标分布：

$$\mathcal { L } _ { t o t a l } = \mathcal { L } _ { M L E } ( z , J ) + \lambda \mathcal { K } \mathcal { L } _ { d i v } ( z , y )$$

INN 的可逆性带来了双重收益：（1）前向变换保证生成过程接收的是标准高斯分布，图像质量不受水印载荷影响；（2）反向变换（通过 $\phi^{-1}$）在提取阶段实现精确的潜变量恢复，无信息损失。

消融实验（Table 4）提供了决定性证据：移除分布变换模块后，在仅 1,024 bits 载荷下 FID 从 42.0 急剧升高至 388.4，图像质量完全崩溃，同时提取准确率也大幅下降。这直接验证了分布保持是高容量水印的核心使能技术。

### Changed Slot 3：纠错码与超参数调优——从手工设定到自动搜索

Gaussian Shading 未使用显式纠错码，PRC Watermark 采用伪随机纠错码但缺乏系统化的参数优化。MaxMark 采用 **Reed-Solomon (RS) 码** 作为纠错方案，并设计了一套基于误差分布模型的自动超参数搜索流程。

RS 码的优势在于其确定性的纠错能力和灵活的参数配置（可调码率和纠错能力）。自动搜索过程通过建模不同攻击下的比特错误分布，在码率和纠错能力之间寻找最优平衡点，从而在不同载荷下最大化恢复准确率。Table 6 的消融结果表明，随机设定的 ECC 参数效果有限，而自动搜索策略在各载荷下均能可靠地提升恢复能力；Table 5 进一步验证了 RS 码相比其他 ECC 方案的优越性。

### 创新协同与能力边界

三个 changed slots 形成了层次化的协同关系：**符号位嵌入**提供了最可靠的底层信息承载；**INN 分布变换**消除了高容量嵌入对图像质量的负面影响，使容量可以安全地推向潜空间维度上限；**自动 ECC 调优**则在给定容量下最大化恢复鲁棒性。这种协同使得 MaxMark 在 Stable Diffusion V1.5 上实现了 16,384 bits 载荷下 95.4% 的比特准确率，相对最优基线提升 46%，同时 FID 保持在 41.8，与无水印基线相当。

需要注意的是，MaxMark 的水印容量仍受限于潜空间维度（$4 \times 64 \times 64$），且论文仅在 Stable Diffusion V1.4/V1.5/V2.1 上验证了方法，其在不同 LDM 架构（如 SDXL）上的泛化能力仍需进一步验证。此外，针对基于梯度的自适应攻击的鲁棒性尚未评估，这是实际部署中需要关注的安全边界。

MaxMark 的整体 pipeline 由两个协同工作的核心模块构成：**鲁棒水印嵌入模块**与**分布变换模块**。其设计目标是在潜扩散模型的原生潜空间中实现高容量水印嵌入，同时不破坏扩散过程所依赖的高斯先验分布，从而兼顾水印容量与生成图像质量。

### 数据流与模块关系

整个框架的数据流可概括为“嵌入—变换—生成—反演—恢复”五步闭环，如 Figure 3 所示：

![[assets/figures/papers/paper_list_l898_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_MaxMark_High_Cap/figures/003_Figure_3.jpg]]
*Figure 3: The framework of MaxMark. We achieve high-capacity watermarking for LDMs through two cooperating components. The robust watermark embedding module inserts watermark information into reliable regions of the latent noise, enabling accurate watermark extraction. The distribution transformation module then try to map the watermark-bearing latent to a Gaussian distribution (e.g., the balanced latent), mitigating its impact on the generated image. This transformation is implemented using a fully reversible INN, which not only preserves information for precise recovery but also enables efficient training*

1. **秘密消息增强与嵌入**：输入的秘密消息首先经过**秘密密钥编码器**增强，该编码器采用 Reed–Solomon 纠错码与自动超参数搜索机制，将原始比特串扩展为具有纠错能力的增强水印 $s_e$。随后，鲁棒水印嵌入模块从标准高斯分布 $\mathcal{N}(0,I)$ 中采样潜噪声 $x$，并依据 $s_e$ **覆写其符号位**，同时施加边缘参数 $\beta$ 以增强鲁棒性，得到带水印的潜变量 $x'$。这一操作仅修改潜噪声中最可靠的信息载体——符号位，从而在嵌入大容量水印时最小化对潜空间结构的扰动。

2. **分布变换**：带水印的潜变量 $x'$ 不再服从标准高斯分布，若直接送入扩散模型将导致图像质量严重退化。分布变换模块以**可逆神经网络**为骨干，通过前向耦合块将 $x'$ 映射回近似标准高斯分布的“平衡潜变量” $z$。这一变换在保持可逆性的同时，使得后续扩散生成过程不受水印嵌入的干扰。

3. **扩散生成**：平衡潜变量 $z$ 被送入潜扩散模型的去噪过程，生成最终的水印图像。由于 $z$ 的分布与扩散模型的先验分布一致，生成质量得到保障。

4. **水印提取**：在接收端，水印图像通过 DDIM 反演恢复出平衡潜变量 $z'$，再经由 INN 的逆变换得到恢复的带水印潜变量 $\hat{x}'$。最后，从 $\hat{x}'$ 的符号位中提取增强水印 $\hat{s}_e$，并通过 Reed–Solomon 解码器纠正潜在错误，恢复出原始秘密消息。

### 关键设计决策

- **符号位嵌入**：与现有方法直接在潜噪声值上叠加扰动不同，MaxMark 将水印信息仅嵌入符号位。消融实验证实，符号位是潜空间中信息承载最可靠的位置，在保持图像质量的同时达到最高提取准确率。
- **INN 分布保持**：现有方法缺乏显式的分布变换机制，当水印容量增大时，对潜空间的扰动会破坏 LDM 的高斯先验，导致 FID 急剧升高。MaxMark 通过 INN 将分布保持问题显式化，使大容量嵌入下的图像质量与无水印基线可比。
- **Reed–Solomon 与自动超参搜索**：相较于伪随机纠错码或手工设定参数，Reed–Solomon 码结合基于误差分布模型的自动超参数搜索，能够更可靠地最大化恢复准确率，尤其在高容量场景下效果显著。

### 训练与推理流程

INN 的训练仅需前向过程，通过最小化最大似然估计损失与 KL 散度的加权和来匹配标准高斯分布，无需扩散模型的反向传播。推理时，嵌入与提取均依赖 INN 的完全可逆性，保证了信息的精确恢复。

MaxMark由两个协同工作的核心模块构成：**鲁棒水印嵌入模块**与**分布变换模块**，二者共同解决高容量水印嵌入与图像质量保持之间的矛盾。

### 鲁棒水印嵌入模块

该模块的核心设计在于**嵌入位置的选择**与**秘密秘钥的增强**。

**嵌入位置**：模块将水印信息嵌入潜噪声的符号位（sign bits）。论文通过实验验证，符号位是潜空间中承载信息最可靠的位置——它在保持图像质量的同时达到最高的提取准确率（见Figure 5）。具体嵌入方式为：采样一个标准高斯噪声向量 $x \sim \mathcal{N}(0,1)$，根据增强后的水印 $s_e$ 覆盖其符号位，并施加边缘参数 $\beta$ 以将修改后的值推离零点，增强鲁棒性：

$$x_{i}^{\prime} = \sigma(s_{i}) x_{i} \pm \beta, \quad \sigma(s_{i}) = 2 s_{i} - 1$$

其中 $\sigma(s_i)$ 将二值水印比特 $s_i \in \{0,1\}$ 映射为符号方向 $\{-1, +1\}$，$\beta$ 为边缘裕量。

**秘密秘钥增强**：模块采用 **Reed-Solomon (RS) 纠错码**对原始秘密秘钥进行编码增强，并通过一个基于误差分布模型的自动搜索程序选择最优ECC超参数。消融实验表明，无ECC时高容量水印恢复准确率大幅下降，而RS码可显著纠正错误；自动超参数搜索优于随机搜索，能更可靠地最大化恢复准确率（见Table 5和Table 6）。

### 分布变换模块

这是MaxMark解决核心瓶颈的关键模块。现有潜空间水印方法在大容量嵌入时，对潜空间的扰动破坏了LDM的高斯先验分布 $\mathcal{N}(0,I)$，导致图像质量严重下降。分布变换模块通过**可逆神经网络（INN）**将带水印的潜变量显式映射回标准高斯分布，确保生成过程不受干扰。

**INN架构**：模块采用12个非对称耦合块（asymmetric coupling blocks）构建INN。每个耦合块的前向传播为：

$$\begin{array} { r } { s _ { a } ^ { i } , t _ { a } ^ { i } = f _ { a } ^ { i } ( z _ { a } ^ { i - 1 } ) , z _ { b } ^ { i } = \phi ( z _ { b } ^ { i - 1 } , s _ { a } ^ { i } , t _ { a } ^ { i } ) } \\ { s _ { b } ^ { i } , t _ { b } ^ { i } = f _ { b } ^ { i } ( z _ { b } ^ { i } ) , z _ { a } ^ { i } = \phi ( z _ { a } ^ { i - 1 } , s _ { b } ^ { i } , t _ { b } ^ { i } ) } \end{array}$$

其中 $f_a^i$ 和 $f_b^i$ 为子网络，$\phi(z,s,t) = z \odot e^s + t$ 为乘性耦合函数，通过缩放因子 $s$ 和平移因子 $t$ 实现可逆变换。反向传播利用逆变换 $\phi^{-1}$ 精确恢复输入：

$$\begin{array} { r } { s _ { b } ^ { i } , t _ { b } ^ { i } = f _ { b } ^ { i } ( z _ { b } ^ { i ^ { \prime } } ) , z _ { a } ^ { i - 1 ^ { \prime } } = \phi ^ { - 1 } ( z _ { a } ^ { i ^ { \prime } } , s _ { b } ^ { i } , t _ { b } ^ { i } ) } \\ { s _ { a } ^ { i } , t _ { a } ^ { i } = f _ { a } ^ { i } ( z _ { a } ^ { i - 1 ^ { \prime } } ) , z _ { b } ^ { i - 1 ^ { \prime } } = \phi ^ { - 1 } ( z _ { b } ^ { i ^ { \prime } } , s _ { a } ^ { i } , t _ { a } ^ { i } ) } \end{array}$$

**训练损失**：INN的训练目标是将带水印潜变量的分布匹配到标准高斯分布，总损失为最大似然估计损失与KL散度的加权和：

$$\mathcal { L } _ { t o t a l } = \mathcal { L } _ { M L E } ( z , J ) + \lambda \mathcal { L } _ { d i v } ( z , y )$$

其中 $z$ 为变换后的潜变量，$J$ 为雅可比行列式，$y$ 为目标高斯分布，$\lambda=0.1$ 为平衡权重。训练仅需前向过程。

**关键消融验证**：移除分布变换模块后，在1,024 bits载荷下FID从42.0急剧升至388.4（见Table 4），这直接验证了分布保持对图像质量的决定性作用。INN的可逆性同时保证了水印提取阶段通过逆变换精确恢复带水印潜变量，实现信息无损传递。

### 水印提取流程

提取阶段通过DDIM反演从生成图像恢复潜变量，再经逆INN变换得到带水印潜变量，最后从符号位解码出水印信息。整个流程的精确性依赖于INN的可逆性——前向映射到高斯分布保证生成质量，反向映射精确恢复嵌入信息，形成闭环。

## 实验与关键发现

### 主结果：高容量水印的有效性与图像质量

MaxMark在Stable Diffusion V1.5上进行了系统评估，与基于潜空间的水印基线方法**Gaussian Shading**（Yang et al., CVPR 2024）和**PRC Watermark**（Gunn et al., 2025）进行了全面对比。所有方法均基于相同的潜扩散模型，使用相同的DDIM反演步数和提示词数据集，确保公平比较。

**水印有效性**：Table 1报告了不同载荷下的比特准确率。在无攻击的清洁场景下，MaxMark在16,384 bits载荷时达到**95.4%**的比特准确率，相比最佳基线（约49.4%）提升**46%**。在8,192 bits和12,288 bits载荷下，分别提升12%和45%。在对抗攻击场景下（Table 1中"Bit Accuracy under Adversarial"），MaxMark在16,384 bits时仍保持**86.9%**的准确率，展现出显著的鲁棒性优势。

**图像质量**：Table 2显示，MaxMark在16,384 bits载荷下的FID为**41.8**，与无水印基线相当，未出现明显的图像质量退化。相比之下，基线方法在高载荷下普遍面临图像质量与嵌入容量之间的严重权衡——Gaussian Shading和PRC Watermark在追求高容量时均无法同时保持高准确率和高图像质量（Table 3联合分析）。

### 消融实验：关键设计选择验证

**分布变换模块的核心作用**：Table 4揭示了移除分布变换模块（INN）后的性能崩溃。在1,024 bits载荷下，无变换模块时FID从**42.0急剧升高至388.4**，同时提取准确率也出现下降。这验证了论文的核心洞察：对大容量水印嵌入而言，保持潜空间的高斯先验分布是维持图像质量的必要条件，而INN的分布匹配能力正是实现这一目标的关键机制。

**符号位嵌入的最优性**：Figure 5比较了不同嵌入位（fp32的各比特位）对准确率的影响。结果表明，符号位在保持图像质量的同时达到最高准确率，证实了"符号位是潜噪声中最可靠的嵌入位置"这一设计选择。

**ECC的作用与自动调优**：Table 5显示，无ECC时高容量水印恢复准确率大幅下降，而采用Reed-Solomon码可显著纠正错误。Table 6进一步表明，随机设定的ECC参数效果有限，而论文提出的自动超参数搜索过程能在不同载荷下更可靠地最大化恢复准确率，验证了基于误差分布模型的参数优化策略的有效性。

### 跨模态泛化

MaxMark的方法不仅限于图像生成。Table 7和Table 8分别展示了在视频和音频模态上的性能，在不同水印载荷下均保持了较高的比特准确率，表明符号位嵌入与分布变换的核心思想具有跨模态的通用性。

![[assets/figures/papers/paper_list_l898_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_MaxMark_High_Cap/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between MaxMark and baselines across different watermark payload sizes. MaxMark significantly outperforms baselines in both bit accuracy and robustness*

![[assets/figures/papers/paper_list_l898_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_MaxMark_High_Cap/figures/004_Table_1.jpg]]
*Table 1: Comparison with baselines on watermark effectiveness across different watermark payload sizes. Bit accuracy indicates performance on clean data, while bit accuracy under adversarial reflects average performance across attacks. Detailed results for each attack are in Appendix 1. These results demonstrate the significant advantage of our method in embedding high-capacity information*

![[assets/figures/papers/paper_list_l898_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_MaxMark_High_Cap/figures/005_Table_2.jpg]]
*Table 2: Comparison with baselines on image quality across different watermark payload sizes. This result indicates that MaxMark shows comparable performance when compared to baseline methods, without degrading the model’s performance*

![[assets/figures/papers/paper_list_l898_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_MaxMark_High_Cap/figures/008_Table_4.jpg]]
*Table 4: Performance comparison with and without the distribution transformation module across different watermark payload sizes, tested on COCO [22]. The format without/with denotes the two settings. The distribution transformation module consistently improves both image quality and extraction accuracy*

![[assets/figures/papers/paper_list_l898_https_openaccess_thecvf_com_content_CVPR2026_html_Chang_MaxMark_High_Cap/figures/009_Table_5.jpg]]
*Table 5: Bit accuracy(%) with different ECC methods*

## 定位与知识库关联

### 潜空间水印路线的演进与MaxMark的定位

MaxMark处于**扩散原生潜空间水印**这一技术路线，其核心问题是在潜扩散模型（LDM）的生成过程中嵌入可恢复的标识信息。该路线的基本范式如Figure 2所示：水印嵌入潜空间后，经扩散过程传播至生成图像，再通过DDIM反演恢复潜变量以提取水印。

在这一路线中，MaxMark的直接前驱是**Gaussian Shading**（Yang et al., CVPR 2024）和**PRC Watermark**（Gunn et al., 2025）。二者的共同策略是在潜噪声上叠加扰动以嵌入信息，但其瓶颈在于：当水印容量增大时，对潜空间的扰动会破坏LDM所依赖的高斯先验分布 $x \sim \mathcal{N}(0, I)$，导致生成的图像质量急剧下降。这一瓶颈构成了该路线从低容量走向高容量的核心障碍。

MaxMark的突破点在于将问题从“扰动控制”重新定义为**分布保持问题**。其核心因果机制是：引入基于可逆神经网络（INN）的分布变换模块，将带水印的潜变量显式映射回标准高斯分布，从而在生成端“欺骗”扩散模型，使其无法感知水印的存在；在提取端则利用INN的可逆性实现精确恢复。这一设计使得水印容量与图像质量之间的传统权衡被大幅削弱。

### 与基线方法的关键差异

| 维度 | Gaussian Shading / PRC | MaxMark |
|------|----------------------|---------|
| 嵌入位置 | 潜噪声值上叠加扰动（如Gaussian Shading的重排机制） | 仅覆盖潜噪声的**符号位**，并施加边缘 $\beta$ 以增强鲁棒性 |
| 分布保持 | 通过精心设计的扰动尽量保持高斯特性，无显式变换 | 引入**INN分布变换模块**，将带水印潜变量显式映射回 $\mathcal{N}(0,I)$ |
| 纠错码 | 伪随机纠错码（PRC）或手工设定参数 | **Reed-Solomon码** + 基于误差分布模型的自动超参数搜索 |

符号位嵌入的优越性来源于一个关键观察：在浮点表示中，符号位是信息最稳固的载体，对后续图像处理扰动具有天然鲁棒性。消融实验（Figure 5）证实，与其他位相比，符号位在保持图像质量的同时达到最高准确率。嵌入公式为：

$$x_i^{\prime} = \sigma(s_i) x_i \pm \beta, \quad \sigma(s_i) = 2 s_i - 1$$

其中 $\beta$ 作为边缘参数将修改后的值推离零点，进一步增强抗扰动能力。

### 分布变换模块的决定性作用

分布变换模块是MaxMark区别于所有前驱工作的根本创新。消融实验（Table 4）提供了决定性证据：在1,024 bits水印容量下，移除该模块后FID从42.0急剧升高至388.4，同时提取准确率也显著下降。这表明，**没有分布保持机制，即使嵌入容量不高，潜空间扰动也会严重破坏生成质量**。

INN的训练采用总损失函数：

$$\mathcal{L}_{total} = \mathcal{L}_{MLE}(z, J) + \lambda \mathcal{L}_{KL}(z, y)$$

其中MLE损失与KL散度加权组合，目标是使变换后的潜变量匹配标准高斯分布。INN采用12个非对称耦合块构建，训练时仅需前向过程（$\lambda=0.1, \beta=10$），无需反演即可完成。

### 纠错码与超参数搜索的贡献

在纠错码层面，MaxMark放弃了前驱工作的伪随机码方案，转而采用成熟的**Reed-Solomon码**。消融实验（Table 5）表明，无ECC时高容量水印恢复准确率大幅下降，而RS码能显著纠正错误。进一步地，自动ECC超参数搜索（Table 6）优于随机搜索，能更可靠地最大化不同容量下的恢复准确率。这一自动搜索机制基于对攻击后误差分布的建模，而非暴力枚举。

### 适用边界与局限

MaxMark的有效性已在Stable Diffusion v1.4/v1.5/v2.1上得到验证，实验覆盖了COCO提示词数据集和标准图像扰动攻击。然而，以下边界条件需要关注：

1. **水印容量受限于潜空间维度**：当前方案基于 $4 \times 64 \times 64$ 的潜空间，16,384 bits已接近其信息承载上限。能否通过改变INN结构或利用多级潜变量进一步提升容量上限，仍是开放问题。

2. **对LDM架构的依赖程度未充分验证**：分布变换模块的训练与特定LDM的潜空间分布相关。论文未提供在SDXL等不同架构上的泛化实验结果，该问题需要手动验证。

3. **对抗性攻击的覆盖范围有限**：论文评估的攻击类型限于常见图像扰动（JPEG压缩、裁剪、噪声等）。针对更复杂的自适应攻击（如基于梯度的攻击、针对INN的逆向攻击）的鲁棒性，目前缺乏实验证据。

### 跨模态泛化潜力

论文初步探索了MaxMark在视频和音频模态上的适用性（Table 7、Table 8），结果表明其分布保持+符号嵌入的核心思想具有一定的模态无关性。但视频和音频的潜空间结构与图像存在本质差异，该泛化能力是否源于INN的通用分布匹配能力，还是需要针对各模态重新训练，论文未给出明确结论。

### 开放问题

1. 分布变换模块是否完全消除了对特定LDM的依赖？在SDXL等不同架构上的泛化能力如何？
2. 能否通过改变INN结构或利用多级潜变量进一步提升容量上限？
3. 针对基于梯度的自适应攻击的鲁棒性如何？
4. INN的训练是否可以在不访问完整扩散模型的情况下完成，以降低部署门槛？

## 原文 PDF

![[paperPDFs/CVPR_2026/MaxMark_High_Capacity_Diffusion_Native_Watermarking_via_Robust_and_Invertible_Latent_Embedding.pdf]]
