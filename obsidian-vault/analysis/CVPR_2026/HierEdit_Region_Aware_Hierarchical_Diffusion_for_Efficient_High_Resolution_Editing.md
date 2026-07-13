---
title: "HierEdit: Region-Aware Hierarchical Diffusion for Efficient High-Resolution Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HierEdit_Region_Aware_Hierarchical_Diffusion_for_Efficient_High_Resolution_Editing.pdf
project_link: null
code_link: null
aliases:
- HierEdit
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过低分辨率代理编辑生成语义引导和编辑遮罩，将高分辨率生成限制在局部窗口内，仅对修改区域施加注意力与去噪，从而将计算复杂度与图像分辨率解耦。
primary_logic: 低分辨率编辑代理能提供高质量的编辑区域定位和中间去噪初始化，使高分辨率生成仅需处理局部窗口；同时未修改区域作为条件输入可被缓存重用，实现了高效且分辨率无关的局部编辑。
claims:
- HierEdit 在 1K 分辨率编辑中比竞争方法快 6 倍以上，且随编辑区域减小增益更大。
- HierEdit 是唯一能在 4K 分辨率下成功完成文本引导编辑、修补和主题引导编辑的方法，其他方法因设计限制或内存不足而失败。
- 在 CompBench、EmuEdit、ImgEdit 和 I2EBench 等多个编辑基准上，HierEdit 取得了有竞争力的质量指标（CLIP 20.6, SSIM 0.949, DINO 0.833）。
- 消融实验表明，移除局部窗口注意力（LWA）会使速度下降 12.4 倍，移除特征缓存（FC）和联合 token 整合（TI）也会显著增加推理时间。
---

# HierEdit: Region-Aware Hierarchical Diffusion for Efficient High-Resolution Editing

> [!tip] 核心洞察
> 低分辨率编辑代理能提供高质量的编辑区域定位和中间去噪初始化，使高分辨率生成仅需处理局部窗口；同时未修改区域作为条件输入可被缓存重用，实现了高效且分辨率无关的局部编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | HierEdit：面向高效高分辨率编辑的区域感知层级扩散模型 |
| 英文题名 | HierEdit: Region-Aware Hierarchical Diffusion for Efficient High-Resolution Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_HierEdit_Region-Aware_Hierarchical_Diffusion_for_Efficient_High-Resolution_Editing_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | HierEdit |
| Dataset | 1K 分辨率编辑速度（50% 编辑区域）, 4K 分辨率编辑（文本引导编辑、修补、主题引导修补）, CompBench, EmuEdit, ImgEdit, I2EBench |

> [!tip] 效果简介
> - 1K 分辨率编辑速度（50% 编辑区域） 上，推理时间（秒） 2.34 s (完整模型) vs 竞争方法通常 > 14 s (提升约 6.0 倍)。
> - 4K 分辨率编辑（文本引导编辑、修补、主题引导修补） 上，生成成功率 / 图像质量 成功生成高质量 4K 编辑结果 vs GPT-Image-1 无法输出高于 1K 的图像；ACE++ 在 96GB GPU 上无法完成 4K 推理 (唯一可行的 4K 方案)。
> - CompBench, EmuEdit, ImgEdit, I2EBench 上，CLIP / SSIM / DINO / ImgEdit Composite 等 CLIP 20.6, SSIM 0.949, DINO 0.833, ImgEdit 3.51 vs 其他先进编辑方法（具体数值见原文 Table 1） (达到有竞争力的质量水平)。

## 概要

### 问题瓶颈

高分辨率图像编辑面临的核心瓶颈在于**密集注意力机制的计算与内存开销随分辨率呈二次增长**。传统扩散模型对整幅图像进行全局自注意力计算，复杂度为 $O(N^2)$，其中 $N$ 为图像标记（token）数量。当分辨率从 1K 提升至 4K 时，$N$ 增加约 16 倍，导致计算量和显存需求激增，使得现有方法要么无法完成推理，要么速度极慢。此外，多数编辑任务仅涉及局部区域的修改，对未修改区域进行完整的去噪和注意力计算是冗余的。现有方法缺乏有效的**编辑区域定位机制**，无法将计算资源聚焦于真正需要修改的局部窗口。

### 核心方法

**HierEdit** 提出了一套**层级化、区域感知的扩散编辑框架**，通过三个关键设计将计算复杂度与图像分辨率解耦：

1. **低分辨率代理编辑与遮罩精炼**：将高分辨率输入下采样至标准分辨率（如 256×256），利用现成编辑模型生成低分辨率编辑参考，并通过像素级比较自动推导精炼的编辑遮罩 $\tilde{M}$，准确定位需修改的局部区域。

2. **层级局部窗口 MMDiT（Local-Window MMDiT）**：将高分辨率潜变量划分为非重叠窗口（窗口大小 $l=16$），仅对遮罩内的窗口应用局部注意力，复杂度降至 $O(N \cdot l^2)$。同时，将未编辑区域作为条件标记进行特征缓存重用，仅对被编辑区域执行去噪，序列长度从 $2N$ 压缩至 $N$。

3. **中间流初始化与推理加速**：将上采样并锐化的低分辨率参考作为高分辨率采样的起点，从中间时间步开始去噪，将去噪步数从 $T=28$ 缩减至 $T'=10$，结合 Flash Sparse Attention 内核优化，进一步降低推理耗时。

### 主要结果

- **显著加速**：在 1K 分辨率、50% 编辑区域的设置下，HierEdit 完整模型的推理时间仅为 **2.34 秒**，比竞争方法快 **6 倍以上**；消融实验表明，移除局部窗口注意力会使速度下降 **12.4 倍**（Table 4）。
- **唯一可行的 4K 编辑方案**：在 4K 分辨率下，HierEdit 是唯一能够成功完成文本引导编辑、修补和主题引导修补的方法；GPT-Image-1 设计上不支持高于 1K 的输出，ACE++ 在 96GB GPU 内存下无法运行 4K 推理（Figure 6）。
- **有竞争力的编辑质量**：在 CompBench、EmuEdit、ImgEdit 和 I2EBench 等多个基准上，HierEdit 取得了与先进方法可比的质量指标（CLIP 20.6, SSIM 0.949, DINO 0.833），证明了效率提升并未以牺牲编辑质量为代价（Table 1）。

### 方法定位与知识库定位

HierEdit 属于**高效高分辨率图像编辑**方法，其技术路线融合了**稀疏注意力机制**与**编辑区域自适应定位**。与依赖手工遮罩的传统修补方法或对全图重渲染的指令编辑方法不同，HierEdit 通过低分辨率代理自动定位编辑区域，并将扩散模型的注意力计算限制在局部窗口内。该方法建立在 Rectified Flow 框架和 MMDiT 架构之上，通过 LoRA 微调适配新的注意力模式，无需 4K 训练数据即可泛化至超高分辨率。在方法谱系中，HierEdit 与以下工作形成对比：

- **GPT-Image-1**：指令编辑模型，但设计上不支持高于 1K 的分辨率输出，限制了其在高分辨率场景的应用。
- **ACE++**（Mao et al., arXiv 2025）：指令编辑方法，在 96GB GPU 内存下无法完成 4K 推理，受限于密集注意力的内存开销。
- 传统修补方法（如 FLUX-based inpainting）：通常需要用户提供精确遮罩，且对高分辨率输入的计算效率较低。

HierEdit 的核心贡献在于**首次实现了分辨率无关的局部编辑效率**，使得在消费级 GPU 上进行 4K 图像编辑成为可能，同时保持了与全分辨率方法可比的编辑质量。

### 高分辨率图像编辑的计算瓶颈

图像编辑技术近年来取得了显著进展，基于扩散模型的方法在文本引导编辑、图像修补等任务上展现出强大的生成能力。然而，当编辑分辨率从常规的 1K（约 1024×1024）提升至 2K、4K 乃至更高时，现有方法面临根本性的计算障碍。

这一瓶颈的核心在于**密集注意力机制的二次复杂度**。当前主流的扩散 Transformer 架构（如 FLUX 系列）在去噪过程中对整个图像的所有空间标记执行全局自注意力。对于分辨率为 $H \times W$ 的图像，注意力计算的复杂度为 $O(N^2)$，其中 $N = H \times W$ 为标记数量。当分辨率从 1K 提升至 4K 时，标记数量增长约 16 倍，计算与内存开销则呈二次方膨胀，使得高分辨率编辑在消费级 GPU 上几乎不可行。

更关键的是，这种全图密集处理策略存在**本质上的计算冗余**。在典型的局部编辑场景中——例如替换图像中的某个物体、修改特定区域的纹理或颜色——用户仅期望图像的一小部分发生变化，而大部分区域应保持原样。然而，现有方法仍然对整幅图像施加完整的注意力与去噪过程，将大量计算资源浪费在无需修改的区域上。

### 现有方法的局限

当前高分辨率图像编辑的应对策略主要分为两类，但均存在明显不足：

**全图重渲染方案**直接在高分辨率下运行完整的扩散去噪过程。这类方法（如基于 FLUX.1-Fill-dev 的修补模型）虽然能够生成高质量结果，但推理速度极慢，且内存消耗随分辨率急剧增长。实验表明，在 96GB GPU 内存环境下，部分方法甚至无法完成 4K 分辨率的推理（见 Table 3 中标记为“—”的条目）。

**级联式超分方案**则采用“先低分辨率编辑，再超分辨率放大”的策略。这类方法虽然降低了计算成本，但超分过程往往引入模糊、伪影或语义偏移，难以保持编辑区域与原始高分辨率背景之间的精确一致性。此外，超分模型本身也需要额外的训练数据和计算资源。

一个更深层的结构性问题在于，现有方法**缺乏有效的编辑区域定位机制**。大多数方法要么依赖用户手工提供精确遮罩（增加交互负担），要么对全图进行无差别处理（造成计算浪费）。即便部分方法尝试利用注意力图或交叉注意力来推断编辑区域，其定位精度往往不足以支撑高质量的局部编辑。

### HierEdit 的核心动机

针对上述问题，HierEdit 提出了一条根本性的解决路径：**将高分辨率编辑的计算复杂度与图像分辨率解耦**。其核心洞察可以概括为两点：

1. **低分辨率代理编辑足以提供高质量的编辑语义引导**。通过将高分辨率输入下采样至标准分辨率（如 256×256），利用现成的编辑模型生成低分辨率编辑参考，可以同时获得编辑区域的精确定位和中间去噪结果的初始化。这一洞察打破了“必须在高分辨率下进行全部推理”的固有假设。

2. **高分辨率生成仅需处理被编辑的局部窗口**。利用低分辨率代理生成的编辑遮罩，可以将高分辨率图像划分为非重叠窗口，仅对遮罩覆盖的窗口施加注意力与去噪操作。未修改区域的特征可以作为条件输入被缓存重用，从而将注意力复杂度从 $O(N^2)$ 降至 $O(N \cdot l^2)$（$l=16$ 为窗口大小）。

这一设计使得 HierEdit 在 1K 分辨率下比竞争方法快 6 倍以上，且成为唯一能在 96GB GPU 上成功完成 4K 分辨率文本引导编辑、修补和主题引导编辑的方法（见 Figure 6）。同时，在 CompBench、EmuEdit、ImgEdit 等多个编辑质量基准上，HierEdit 保持了有竞争力的质量指标（CLIP 20.6, SSIM 0.949, DINO 0.833），证明了效率提升并非以牺牲质量为代价。

## 核心方法与创新机理

HierEdit 的核心创新在于通过**层级式编辑代理 + 局部窗口注意力**将高分辨率图像编辑的计算复杂度与图像分辨率解耦，从而在保持编辑质量的同时实现显著加速。与现有方法对全图进行密集注意力计算不同，HierEdit 将编辑过程拆分为低分辨率语义规划与高分辨率局部精炼两个阶段，仅对需要修改的区域施加计算资源。

### 关键创新点与 Changed Slots

**1. 编辑区域自动定位（从手工遮罩到低分辨率代理推导）**

传统方法依赖用户提供精确的编辑遮罩，或对整幅图像进行重渲染。HierEdit 引入**低分辨率代理编辑**机制：将高分辨率输入下采样至标准分辨率（如 1K→256），利用现成编辑模型生成低分辨率编辑参考图像 $X_{Lr}'$，通过逐像素比较 $X_{Lr}'$ 与原始低分辨率输入 $X_{Lr}$ 的差异，自动推导出精炼编辑遮罩 $\tilde{M}$（见 Figure 7）。该遮罩不仅定位编辑区域，还避免了手工标注的不精确性导致的阴影错误等伪影（Section 3.2）。

**2. 注意力机制（从密集全局自注意力到层级局部窗口注意力）**

基线方法采用密集全局自注意力，计算复杂度为 $O(N^2)$，其中 $N$ 为图像标记数，在高分辨率下计算量与内存消耗呈二次增长。HierEdit 的 **Local-Window MMDiT** 将高分辨率潜变量划分为非重叠窗口（窗口大小 $l=16$），仅对被编辑遮罩覆盖的窗口计算局部注意力，复杂度降至 $O(N \cdot l^2)$（Section 3.3）。消融实验表明，移除局部窗口注意力（LWA）会使推理速度下降 **12.4 倍**（从 2.34 s 增至 29.12 s），验证了稀疏局部注意力是加速的核心要素（Table 4）。

**3. 去噪标记序列构造（从双序列拼接到联合整合序列）**

传统方法将条件图像序列与噪声图像序列独立拼接，序列长度为 $2N$，注意力内存消耗为 4 倍。HierEdit 采用**联合去噪整合标记序列**：未编辑区域作为条件标记被缓存重用（特征缓存 FC），仅被编辑区域作为噪声标记参与去噪，序列长度缩减为 $N$。该设计配合联合 token 整合（TI），显著降低了冗余计算（Section 3.3，Figure 3）。消融显示，同时移除 FC 和 TI 会明显降低推理效率（Table 4）。

**4. 去噪初始化与步数（从纯噪声冷启动到中间流初始化）**

基线方法从纯噪声开始完整去噪（如 $T=28$ 步）。HierEdit 利用**中间流初始化**：将低分辨率参考上采样至目标尺寸，经锐化后加噪至中间时间步 $t$，作为高分辨率采样的起点，从而跳过早期去噪步骤，采样步数减少至 $T'=10$。初始化公式为 $X_{\mathrm{hr}}^{t} = \alpha X_{\mathrm{hr}}^{1} + (1 - \alpha) X_{\mathrm{ref}}^{t}$，其中 $X_{\mathrm{hr}}^{1}$ 为高斯噪声，$X_{\mathrm{ref}}^{t}$ 为带噪低分辨率参考（Section 3.4）。这一设计使高分辨率生成仅需处理局部窗口，进一步加速推理。

### 方法瓶颈与因果机制

**真实瓶颈**：高分辨率图像编辑中，密集注意力导致计算与内存开销呈二次增长，传统方法对整幅图像进行冗余处理，无法高效定位并仅修改局部编辑区域。

**因果调节变量**：通过低分辨率代理编辑生成语义引导和编辑遮罩，将高分辨率生成限制在局部窗口内，仅对修改区域施加注意力与去噪，从而将计算复杂度与图像分辨率解耦。

**核心洞察**：低分辨率编辑代理能提供高质量的编辑区域定位和中间去噪初始化，使高分辨率生成仅需处理局部窗口；同时未修改区域作为条件输入可被缓存重用，实现了高效且分辨率无关的局部编辑。

HierEdit 的整体设计遵循一个清晰的层级代理-精炼范式：将高分辨率编辑的高昂计算成本下沉到低分辨率空间完成语义规划与区域定位，再通过稀疏局部注意力将高分辨率生成严格限制在需要修改的局部窗口内。图 2 给出了框架的完整示意图。

**输入与下采样代理编辑。** 给定一张高分辨率图像 $X_{Hr}$ 和编辑指令（文本或参考图像），系统首先将 $X_{Hr}$ 下采样至标准分辨率（如 1K→256），得到低分辨率输入 $X_{Lr}$。随后，利用现成的编辑模型对 $X_{Lr}$ 执行代理编辑，生成低分辨率编辑参考 $X_{Lr}'$。这一步是整个流程的语义锚点——它既提供了编辑“应该是什么样”的视觉参考，又是后续遮罩生成的依据。

**区域精炼与遮罩生成。** 通过像素级比较 $X_{Lr}$ 与 $X_{Lr}'$ 的差异，系统自动推导出一个精炼的编辑遮罩 $\widetilde{M}$，用于准确定位需要修改的局部区域。与直接使用包围盒或手工遮罩不同，这种基于代理编辑的遮罩精炼能够捕捉到阴影、反射等细微的语义变化区域（见 Figure 7），从而避免因遮罩不精确导致的伪影。

**层级局部窗口扩散生成。** 高分辨率潜变量被划分为非重叠窗口（窗口大小 $l=16$），仅对 $\widetilde{M}$ 覆盖的窗口施加注意力与去噪操作。具体而言，系统将未编辑区域作为条件标记（特征缓存重用），仅将被编辑区域作为噪声标记参与去噪，形成联合整合的 token 序列，将序列长度从传统的 $2N$ 压缩至 $N$。这一设计由 Local-Window MMDiT 实现，其注意力复杂度从 $O(N^2)$ 降至 $O(N \cdot l^2)$，实现了计算开销与图像分辨率的解耦。

**中间流初始化加速。** 为进一步减少推理步数，系统将低分辨率参考 $X_{Lr}'$ 上采样至目标分辨率，经锐化后加噪至中间时间步 $t$，作为高分辨率采样的起点。这使得去噪步数从完整流程的 $T=28$ 步缩减至 $T'=10$ 步，显著压缩了推理时间。

**模块间的数据流关系。** 整个 pipeline 的依赖链清晰：低分辨率代理编辑的输出同时驱动遮罩生成和中间流初始化，而遮罩又决定了 Local-Window MMDiT 中注意力窗口的选择范围。特征缓存与 Flash Sparse Attention 内核优化则贯穿高分辨率生成阶段，确保未编辑区域的 Key/Value 投影仅计算一次并被所有窗口重用。

![[assets/figures/papers/paper_list_l884_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HierEdit_Region/figures/002_Figure_2.jpg]]
*Figure 2: Schematic of the HierEdit framework. We employ editing of a downsampled input image and region bounding to identify the edited patches and obtain the low-resolution proxy. We then proceed to input concatenation, re-permutation, and positional encoding. Finally, we pass this input to our hierarchical local-window MMDiT model, which generates the high resolution edited results with less denoising steps as upsampled low-resolution proxy can serve as intermediate denosing result*

HierEdit 的核心设计围绕一个关键洞察展开：高分辨率图像编辑的计算瓶颈并非来自分辨率本身，而是密集注意力对全图的无差别处理。通过将编辑区域定位、注意力范围与去噪过程三者解耦，HierEdit 实现了仅对修改区域施加计算、未修改区域作为条件缓存重用的高效架构。

### 3.1 预备知识：整流流与多模态注意力

HierEdit 建立在整流流（Rectified Flow）框架之上。给定数据样本 $X_0$ 与参考分布 $X_1$，整流流通过一个学习到的速度场 $V$ 定义连续变换：

$$\frac{d Z_t}{d t} = V(Z_t, t)$$

其核心约束是将中间状态限定为线性路径：

$$Z_t = (1 - t) X_0 + t X_1$$

这一约束使采样轨迹笔直且稳定，所需积分步数极少，为后续的中间流初始化加速奠定了基础。

在空间编码方面，模型采用 RoPE（旋转位置编码）对每个空间标记 $X_{i,j}$ 施加位置依赖的旋转变换：

$$X_{i,j} = X_{i,j} \cdot \operatorname{Rot}(i, j)$$

多模态交互则通过多模态注意力（MMA）实现，在文本标记 $C_T$ 与图像标记 $X$ 的拼接序列上执行标准自注意力：

$$\mathrm{MMA}([C_T; X]) = \mathrm{Softmax}\left(\frac{Q K^\top}{\sqrt{d}}\right) V$$

在传统方法中，条件图像序列与噪声图像序列独立拼接，导致序列长度达到 $2N$，注意力内存消耗增至 $4\times$。这正是 HierEdit 着力解决的核心效率瓶颈。

### 3.2 低分辨率代理编辑与区域精炼

HierEdit 的第一个关键模块是**低分辨率引导的区域精炼**。其工作流程如下：

1. **下采样与代理编辑**：将高分辨率输入图像 $X_{Hr}$ 下采样至标准分辨率（如 $1024 \times 1024 \to 256 \times 256$），利用现成的编辑模型生成低分辨率编辑参考 $X_{Lr}'$。
2. **遮罩精炼**：通过像素级比较 $X_{Lr}'$ 与原始低分辨率图像 $X_{Lr}$，推导出精炼的编辑遮罩 $\tilde{M}$。这一步骤解决了简单边界框定位可能导致的阴影错误等伪影问题（见 Figure 7）。

精炼遮罩 $\tilde{M}$ 的作用是精准定位需要修改的局部区域，使后续的高分辨率生成仅聚焦于这些窗口。低分辨率代理编辑的质量直接影响遮罩精度和最终结果的语义对齐，若代理模型失败，整个流程会受到影响——这是 HierEdit 的一个已知局限。

### 3.3 层级局部窗口 MMDiT

这是 HierEdit 最核心的架构创新——**局部窗口 MMDiT（Local-Window MMDiT）**，它从注意力机制和标记序列构造两个维度实现了计算复杂度的根本性降低。

#### 局部窗口注意力

传统密集全局自注意力的复杂度为 $O(N^2)$，其中 $N$ 是图像标记总数。HierEdit 将高分辨率潜变量 $\dot{\boldsymbol{X}} \in \mathbb{R}^{H \times W}$ 划分为 $l \times l$ 的非重叠窗口（$l=16$），仅对被精炼遮罩 $\tilde{M}$ 标记为“已编辑”的窗口应用局部注意力。

窗口总数 $i = \frac{\mathcal{H}}{l} \times \frac{\mathcal{W}}{l}$，每个窗口内注意力复杂度为 $O((l^2)^2) = O(l^4)$，因此总体复杂度降至：

$$O\left(\frac{H}{l} \cdot \frac{W}{l} \cdot l^4\right) = O(N \cdot l^2)$$

当 $l=16$ 时，$l^2 = 256$，远小于高分辨率下的 $N$（例如 $1024 \times 1024$ 分辨率下 $N$ 可达数万），实现了计算量与图像分辨率的有效解耦。该注意力通过 Flash Sparse Attention 内核实现，进一步优化了实际运行效率。

#### 联合去噪整合标记序列

传统方法将条件图像序列与噪声图像序列独立拼接，序列长度为 $2N$。HierEdit 通过编辑遮罩将标记从 $2N$ 裁剪至 $N$：未编辑区域作为条件标记（其特征可被缓存重用），仅被编辑区域作为噪声标记参与去噪。所有标记拼接在一起，条件标记和低分辨率参考通过 LoRA 微调层处理，图像潜变量则使用原始权重。

训练采用标准流匹配损失，旨在让模型学习新的注意力模式。LoRA 仅适配注意力投影层，保持了对预训练权重的最大化复用。

### 3.4 中间流初始化

传统扩散模型从纯噪声开始完整去噪（步数 $T=28$）。HierEdit 利用低分辨率代理编辑结果进行**中间流初始化**，大幅减少所需去噪步数。

具体而言，将低分辨率参考 $X_{ref}$ 放大至目标分辨率，并加噪至中间时间步 $t$，然后与高斯噪声 $X_{hr}^1$ 混合：

$$X_{hr}^t = \alpha X_{hr}^1 + (1 - \alpha) X_{ref}^t$$

这一混合信号作为高分辨率采样的起点，使模型从中间时间步开始采样，去噪步数从 $T=28$ 减少至 $T'=10$，实现了显著的推理加速。锐化操作和预设步数 $T'=10$ 是当前设计的超参数，可能对不同类型的编辑任务敏感，需进一步调优。

### 3.5 特征缓存与内核优化

为进一步提升效率，HierEdit 引入了两项工程优化：

- **特征缓存（Feature Caching, FC）**：未编辑区域的条件标记的 Key/Value 投影在推理过程中保持不变，可被缓存并跨去噪步重用，避免重复计算。
- **内核级优化**：局部窗口注意力通过 Flash Sparse Attention 内核实现，充分利用 GPU 的稀疏计算能力。

消融实验（Table 4）验证了这些设计的必要性：移除局部窗口注意力（LWA）会使推理速度下降 12.4 倍（从 2.34s 增至 29.12s）；同时移除特征缓存（FC）和联合 token 整合（TI）也会显著降低效率。完整模型在 1K 分辨率、50% 编辑区域下仅需 2.34s，比竞争方法快 6 倍以上。

## 实验与关键发现

### 主实验结果

HierEdit 在一系列编辑基准上取得了有竞争力的质量表现，同时在推理效率上实现了显著突破。在 CompBench、EmuEdit、ImgEdit 和 I2EBench 等多个文本引导编辑基准上，HierEdit 取得了 CLIP 20.6、SSIM 0.949、DINO 0.833 以及 ImgEdit Composite 3.51 的综合指标（Table 1），与当前先进的编辑方法处于同一质量水平。

在修补（inpainting）任务中，HierEdit 在保真度、感知质量和效率指标上均展现出优势（Table 2），特别是在保持未修改区域完整性的同时实现编辑内容的自然融合（Figure 5）。

![[assets/figures/papers/paper_list_l884_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HierEdit_Region/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison of inpainting-based editing methods. The proposed HierEdit demonstrates better performance in preserving unmodified regions while maintaining natural integration of edited content*

![[assets/figures/papers/paper_list_l884_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HierEdit_Region/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison of text-guided and image-guided FLUX-based inpainting methods across fidelity, perceptual, and efficiency metrics on 1K × 1K resolution*

效率方面，HierEdit 在 1K 分辨率编辑中展现出显著的加速效果。当编辑区域占比为 50% 时，完整模型的推理时间仅为 2.34 秒，相比竞争方法通常超过 14 秒的耗时，实现了约 6.0 倍的加速（Table 3）。更重要的是，这一加速增益随编辑区域的减小而进一步扩大，体现了层级局部注意力机制对编辑范围的自适应优势。

![[assets/figures/papers/paper_list_l884_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HierEdit_Region/figures/009_Table_3.jpg]]
*Table 3: Speed comparison of different methods across varying edit ratios and resolutions. Results marked by “—” were unable to run on 96GB of GPU memory with expandable segments*

在超高清编辑场景中，HierEdit 是目前唯一能够成功完成 4K 分辨率文本引导编辑、修补和主题引导修补的方法。对比基线中，GPT-Image-1 在设计上不支持高于 1K 的分辨率输出，而 ACE++（Mao et al., arXiv 2025）在 96GB GPU 内存下无法完成 4K 推理（Figure 6）。这一结果表明，HierEdit 通过将计算复杂度与图像分辨率解耦，真正实现了分辨率无关的局部编辑能力。

![[assets/figures/papers/paper_list_l884_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HierEdit_Region/figures/007_Figure_6.jpg]]
*Figure 6: Comparison at 4K resolution for text guided editing, text-guided inpainting, and subject-guided inpainting. GPT-Image-1 was incapable of generating resolutions higher than 1K by design and ACE++ was unable to run 4K inference with 96GB of GPU memory. Our method succeeded in generating the results while the rest of others failed*

### 消融实验

消融实验系统性地验证了 HierEdit 各核心设计组件对效率的贡献。在 1K 分辨率、50% 编辑区域的设定下（Table 4），移除局部窗口注意力（LWA）会导致推理速度下降 12.4 倍（从 2.34 秒增至 29.12 秒），这直接证明了稀疏局部注意力替代密集全局注意力是计算效率提升的根本瓶颈。LWA 通过将注意力计算限制在编辑遮罩内的非重叠窗口（窗口大小 l=16），将复杂度从 $O(N^2)$ 降至 $O(N \cdot l^2)$，是层级扩散架构的核心创新。

![[assets/figures/papers/paper_list_l884_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_HierEdit_Region/figures/011_Table_4.jpg]]
*Table 4: Ablation of speed (without low-res denoising part) difference on design components of our method on 1K ×1K resolution with 50% edited region. LWA denotes local window attention with Flash Sparse Attention Kernel. The number in the () means how much slower comparing to the full pipeline*

同时移除特征缓存（FC）和联合 token 整合（TI）也会显著增加推理时间。FC 通过缓存未编辑区域条件标记的 Key/Value 投影避免了重复计算，而 TI 将条件标记与噪声标记整合为单一序列（从 2N 降至 N），进一步减少了注意力计算量。这些组件的协同作用共同构成了 HierEdit 的高效推理管线。

完整模型在速度（2.34 秒）、PSNR（19.01）、CLIP-T（0.339）和 CLIP-I（0.931）之间取得了最佳权衡，验证了各设计组件在效率与质量之间实现了有效平衡。

### 失败模式与局限性

尽管 HierEdit 在局部编辑任务中表现出色，但其设计存在若干固有限制。首先，该方法主要针对局部编辑场景设计，对于需要全局风格转换或全图重渲染的编辑类型可能不适用。其次，低分辨率代理编辑的质量直接决定了遮罩精度和最终高分辨率结果的语义对齐——若低分辨率模型在编辑定位或内容生成上失败，整个级联流程将受到影响（Figure 7 展示了不当边界框导致的阴影错误等伪影）。

在架构层面，局部窗口注意力虽然大幅降低了计算量，但窗口大小固定为 l=16，当编辑区域跨越多个窗口边界时可能引入边界伪影。当前通过边界标记交互机制部分缓解了这一问题，但未完全消除。此外，推理加速依赖中间流初始化的锐化操作和预设去噪步数 T'=10，这些超参数可能对不同编辑任务类型敏感，需要进一步针对性调整。

## 定位与知识库关联

### 1. 核心问题定位：高分辨率编辑的效率瓶颈

高分辨率图像编辑的核心瓶颈在于，传统扩散模型依赖密集全局自注意力（dense attention），其计算与内存开销随图像分辨率呈二次增长（复杂度 $O(N^2)$，其中 $N$ 为 token 数量）。现有方法通常对整幅图像进行冗余处理，无法高效定位并仅修改局部编辑区域，导致在 1K 及以上分辨率时推理速度急剧下降，甚至因内存溢出而完全不可行。

HierEdit 的核心洞察在于：**低分辨率代理编辑能够提供高质量的编辑区域定位和中间去噪初始化，使高分辨率生成仅需处理局部窗口；同时未修改区域可作为条件输入被缓存重用，从而将计算复杂度与图像分辨率解耦**。这一思路从根本上改变了高分辨率编辑的推理范式——从“全图重渲染”转向“局部精修”。

### 2. 方法谱系中的位置：层级局部注意力与条件缓存

HierEdit 的方法设计在以下关键维度上与现有工作形成显著差异：

**注意力机制**：现有方法普遍采用密集全局自注意力（如标准 MMDiT 架构），序列长度为 $2N$（条件图像序列与噪声图像序列拼接），注意力内存消耗约为 $4\times$。HierEdit 提出层级局部窗口注意力（Local-Window MMDiT），仅对被编辑的局部窗口计算注意力，复杂度降至 $O(N \cdot l^2)$（其中 $l=16$ 为窗口大小），实现了计算量与分辨率的解耦。

**去噪 token 序列构造**：传统方法将条件图像与噪声图像作为独立序列拼接，导致序列冗余。HierEdit 采用联合整合序列（Jointly Denoising Integrated Token Sequence），将未编辑区域作为条件标记（特征缓存重用），仅被编辑区域作为噪声标记参与去噪，序列长度从 $2N$ 压缩至 $N$。

**去噪初始化与步数**：传统方法从纯噪声开始，需完整去噪步数（如 $T=28$）。HierEdit 利用上采样并锐化的低分辨率参考进行中间流初始化，从中间时间步 $t$ 开始采样，步数减少至 $T'=10$，大幅缩短推理路径。

**编辑区域定位**：现有方法通常依赖用户提供的手工遮罩或对全图重渲染。HierEdit 通过低分辨率代理编辑，比较输入输出图像差值，自动生成精炼的编辑遮罩 $\tilde{M}$，实现了编辑区域的自动定位。

### 3. 与具体基线工作的关系

在对比基线中，**ACE++** (Mao et al., arXiv 2025) 作为指令编辑方法，在 96GB GPU 内存下无法完成 4K 推理，其设计受限于密集注意力的内存需求。**GPT-Image-1** 在设计上不支持生成高于 1K 分辨率的图像，因此无法参与超高清编辑比较。HierEdit 是目前唯一能在 4K 分辨率下成功完成文本引导编辑、修补和主题引导编辑的方法（Figure 6），这一定位使其在超高清编辑场景中具有不可替代性。

在效率维度，HierEdit 在 1K 分辨率、50% 编辑区域的设置下推理时间仅为 2.34 秒，而竞争方法通常超过 14 秒，速度提升约 6.0 倍（Table 3, Table 4）。消融实验进一步表明，移除局部窗口注意力（LWA）会使推理速度下降 12.4 倍（从 2.34 秒增至 29.12 秒），验证了稀疏局部注意力设计的核心贡献（Table 4）。

### 4. 适用边界与局限

HierEdit 的设计主要针对**局部编辑任务**，其效率优势在编辑区域较小时尤为显著（编辑区域越小，增益越大）。但对于需要全局风格转换或全图重渲染的编辑类型，该方法可能不适用，因为其核心假设是大部分图像区域保持不变。

低分辨率代理编辑的质量直接影响遮罩精度和最终高分辨率结果的语义对齐。若低分辨率模型在特定编辑指令上失败，则整个级联流程会受到影响，这一依赖关系构成了系统的单点故障风险。

尽管局部窗口注意力降低了计算量，但窗口大小固定为 $l=16$，当编辑区域跨越多个窗口时可能引入边界伪影。当前通过边界 token 交互缓解此问题，但未完全消除。推理加速依赖中间流初始化的锐化操作和预设步数 $T'=10$，这些超参数可能对不同类型的编辑任务敏感，需要进一步调优。

### 5. 开放问题

1. **时序扩展**：HierEdit 能否扩展至视频编辑或更复杂的时序场景？视频中的运动连续性和时序一致性对局部窗口设计提出了更高要求。

2. **极小编辑区域的语义一致性**：在极小编辑区域（如单个物体）下，局部窗口是否仍能保持全局语义一致性？窗口内的有限上下文可能导致与全局场景的语义割裂。

3. **自适应窗口机制**：是否可以引入动态窗口大小或自适应选择编辑窗口，以在效率与质量之间实现更细粒度的权衡？

4. **与其他高效注意力的结合**：与线性注意力等其他高效注意力机制结合时，能否在保持精度的同时进一步提升速度？这需要在稀疏注意力的局部性与线性注意力的全局近似之间找到平衡。

5. **端到端联合优化**：低分辨率代理的生成能否与高分辨率去噪过程进行更紧密的联合优化，以替代当前的级联方式？这有望减少级联误差传播，但需要解决分辨率差异带来的梯度传播挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/HierEdit_Region_Aware_Hierarchical_Diffusion_for_Efficient_High_Resolution_Editing.pdf]]
