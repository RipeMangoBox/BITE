---
title: "LuxDiT: Lighting Estimation with Video Diffusion Transformer"
type: paper
paper_level: A
venue: NeurIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/LuxDiT_Lighting_Estimation_with_Video_Diffusion_Transformer.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/LuxDiT/
code_link: null
aliases:
- LuxDiT
tags:
- NEURIPS_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过将视频扩散Transformer（DiT）用于条件生成HDR环境地图，并引入大规模合成数据预训练与真实HDR全景图的LoRA微调相结合的策略，使模型能够学习物理光照线索并提升语义对齐。"
primary_logic: "光照估计可转化为条件生成任务：利用DiT的全局自注意力从间接视觉线索（阴影、反射）推断非局部光照信息；双色调映射表示解决了标准VAE无法编码高动态范围内容的难题；合成数据提供了物理上准确的监督信号，而LoRA低秩适配在保持预训练能力的同时实现了语义对齐。"
claims:
- "Token-level conditioning 相比通道级联显著降低角度误差，证明全局注意力条件机制对非空间对齐的光照估计至关重要。"
- "移除合成数据预训练导致跨域（Laval Indoor）性能严重下降，表明合成数据是学习泛化光照先验的关键。"
- "LoRA微调显著提升语义对齐并从语义不匹配中恢复，定量表现为更高LoRA权重带来更低的角度误差。"
- "在Laval Outdoor数据集上，LuxDiT将峰值角度误差（PAE）减少近50%，证实了方向精度的大幅提升。"
---

# LuxDiT: Lighting Estimation with Video Diffusion Transformer

> [!tip] 核心洞察
> 光照估计可转化为条件生成任务：利用DiT的全局自注意力从间接视觉线索（阴影、反射）推断非局部光照信息；双色调映射表示解决了标准VAE无法编码高动态范围内容的难题；合成数据提供了物理上准确的监督信号，而LoRA低秩适配在保持预训练能力的同时实现了语义对齐。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LuxDiT：基于视频扩散变换器的光照估计 |
| 英文题名 | LuxDiT: Lighting Estimation with Video Diffusion Transformer |
| 会议/期刊 | NeurIPS 2025 |
| Links | [paper](https://arxiv.org/abs/2509.03680) · [Project](https://research.nvidia.com/labs/toronto-ai/LuxDiT/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | LuxDiT |
| Dataset | Laval Outdoor, Poly Haven, Laval Outdoor (sunny), PolyHaven-Peak videos |

> [!tip] 效果简介
> - Laval Outdoor 上，Scale-invariant RMSE (Diffuse) 为 0.068，对比 0.083 (DiffusionLight)，变化 -0.015。
> - Poly Haven 上，Angular Error (Diffuse) 为 1.235，对比 2.199 (DiffusionLight)，变化 -0.964。
> - Laval Outdoor (sunny) 上，Peak Angular Error Mean 为 23.7，对比 44.4 (DiffusionLight)，变化 -20.7。

## 概要

光照估计是视觉计算中的关键任务，其目标是从有限视场的图像或视频中恢复完整的HDR环境光照，以支持真实感虚拟物体插入等应用。现有方法面临的核心瓶颈在于：真实HDR环境地图数据稀缺、预训练扩散模型无法直接生成高动态范围输出且缺乏任务特定微调，导致估计结果在动态范围、方向精度和语义一致性上存在不足。

LuxDiT 将光照估计重新定义为条件生成任务，通过微调视频扩散Transformer（DiT）从视觉输入生成HDR环境地图。其核心洞察在于：DiT的全局自注意力机制能够从阴影、反射等间接视觉线索中推断非局部光照信息；双色调映射表示解决了标准VAE无法编码高动态范围内容的难题；大规模合成数据提供物理上准确的监督信号，而LoRA低秩适配则在保持预训练能力的同时实现语义对齐。

在方法谱系中，LuxDiT 区别于基于铬球修复的 **DiffusionLight**（Phongthawee et al., CVPR 2024）和基于StyleGAN的 **StyleLight**（Wang et al., arXiv 2022）等近期工作。其关键改进包括：以完全基于注意力的token条件机制取代通道级联，使条件信号与噪声潜变量通过全局自注意力交互；采用大规模合成渲染数据（随机几何、材质、光照）预训练结合真实HDR/LDR数据LoRA微调的两阶段训练策略；以及通过双色调映射（Reinhard映射与归一化对数强度）加轻量MLP重建的HDR表示方案。

实验结果表明，LuxDiT 在多个基准上取得显著提升：在 Laval Outdoor 数据集上，峰值角度误差（PAE）降低近50%（均值从44.4降至23.7）；在 Poly Haven 上角度误差降低约44%（1.235 vs. 2.199）；虚拟物体插入用户研究中获得68%的偏好率。消融实验进一步证实，token级条件机制和合成数据预训练是性能提升的决定性因素。

### 问题背景

光照估计是计算机视觉与图形学中长期存在的核心问题，其目标是从单张或序列低动态范围（LDR）图像中恢复完整的HDR环境光照信息。准确的环境光照对于虚拟物体插入、增强现实和场景重光照等应用至关重要——不匹配的光照方向、强度和颜色会立即破坏视觉真实感。

传统方法主要分为两类：基于逆渲染的优化方法通过显式估计几何、材质和光照参数来重建场景，精度较高但依赖多视图输入和复杂优化流程，难以泛化到野外单张图像；基于学习的方法直接从图像回归光照参数（如**Hold-Geoffroy et al.**，CVPR 2017），速度快但受限于低维参数空间（如球谐系数），无法捕捉高频光照细节。

### 现有方法缺口

近年来，生成式模型为光照估计带来了新的可能性。**StyleLight**（Wang et al., arXiv 2022）利用StyleGAN生成全景图，但输出分辨率有限且缺乏物理约束。**DiffusionLight**（Phongthawee et al., CVPR 2024）通过预训练扩散模型对虚拟铬球进行修复来估计光照，虽然利用了扩散先验，但存在三个根本性局限：

1. **HDR动态范围瓶颈**：标准VAE无法直接编码高动态范围内容，导致DiffusionLight依赖多曝光融合等后处理步骤，无法端到端生成HDR输出。
2. **非任务特定架构**：直接借用预训练图像扩散模型，缺乏针对光照估计任务设计的条件机制和训练策略，方向精度不足。
3. **数据稀缺与域偏差**：真实HDR全景图数据极为稀缺，仅靠预训练模型内嵌的先验难以学习物理上准确的光照线索，在跨域场景下泛化能力有限。

这些缺口在定量上表现为显著的方向误差：DiffusionLight在Laval Outdoor晴天场景上的峰值角度误差均值高达44.4°，远不能满足精细虚拟物体插入的要求。

### 本文动机

针对上述瓶颈，本文提出**LuxDiT**，核心动机是将光照估计重新定义为条件生成任务，并系统性地解决三个关键挑战：

- **架构层面**：利用视频扩散变换器（DiT）的全局自注意力机制，使模型能够从阴影、反射等间接视觉线索中推断非局部光照信息，而非依赖空间对齐的局部特征。
- **表示层面**：设计双色调映射表示，将HDR全景图分解为两个互补的LDR图像，使标准VAE能够编码，再通过轻量MLP融合重建完整动态范围。
- **数据层面**：构建大规模合成渲染数据集（随机几何、材质、光照）提供物理上准确的监督信号，并通过LoRA低秩适配在真实HDR全景图上微调，实现语义对齐而不破坏预训练能力。

这一设计使得LuxDiT在方向精度上实现近50%的误差降低（Laval Outdoor峰值角度误差从44.4°降至23.7°），同时在用户研究中以68%的偏好率显著优于DiffusionLight。

## 核心方法与创新机理

LuxDiT 的核心创新在于将光照估计重新定义为**条件生成任务**，并通过三个关键机制突破现有方法的瓶颈：**注意力驱动的条件嵌入**、**合成数据驱动的物理先验学习**、以及**低秩适配的语义对齐**。

### 1. 注意力驱动的条件嵌入：从通道拼接走向全局交互

现有方法（如 DiffusionLight）通常将条件信号（输入图像特征）与带噪潜变量通过**通道级联**（channel concatenation）拼接后送入去噪网络。LuxDiT 彻底改变了这一范式，采用**完全基于注意力的 token 级条件机制**：条件 token 和噪声 token 被联合送入 DiT 的全局自注意力层，通过独立的 AdaLN 模块分别处理。

这一设计的核心洞察在于，光照估计是一个**非局部推理任务**——光源可能位于画面之外，其位置、强度、颜色需要通过阴影、反射等间接线索推断。通道级联将条件与目标


LuxDiT 将光照估计建模为一个**条件生成任务**：给定单张图像或视频序列 $\mathbf{I}$，生成高动态范围（HDR）环境图 $\mathbf{E}$。其整体 pipeline 由四个核心环节构成，形成从视觉输入到 HDR 光照的端到端映射。

### 1. 双色调映射表示

标准 VAE 无法直接编码 HDR 内容，因此 LuxDiT 将目标 HDR 全景图 $\mathbf{E}$ 分解为两个互补的 LDR 表示（Equation 2）：

- **$\mathbf{E}_{\mathrm{ldr}}$**：Reinhard 色调映射，保留高光细节和整体亮度分布；
- **$\mathbf{E}_{\mathrm{log}}$**：归一化对数强度，捕获极端动态范围信息。

同时，模型注入**方向性嵌入图** $\mathbf{E}_{\mathrm{dir}}$，提供逐像素的光照方向向量，以提升角度连续性。

### 2. VAE 潜空间编码

视觉输入 $\mathbf{I}$ 通过 VAE 编码器转换为**条件潜变量 token**；双色调映射的 $\mathbf{E}_{\mathrm{ldr}}$ 和 $\mathbf{E}_{\mathrm{log}}$（连同 $\mathbf{E}_{\mathrm{dir}}$）则被编码为**带噪目标潜变量** $\mathbf{z}_t = [\mathbf{z}_t^{\mathrm{ldr}}, \mathbf{z}_t^{\mathrm{log}}]$。所有 token 在潜空间中统一表示，为后续 Transformer 处理奠定基础。

### 3. 扩散 Transformer 条件去噪

这是 pipeline 的**核心推理引擎**。视频扩散 Transformer（DiT）在潜空间执行条件去噪：条件 token 和噪声 token 被联合送入自注意力层，通过**全局自注意力机制**传播间接光照线索（如阴影、反射），从非局部视觉信号中推断环境光照。与传统的通道级联不同，LuxDiT 采用**完全基于注意力的 token 条件机制**，使用独立的 AdaLN 模块分别处理条件 token 和噪声 token，使模型能够建立跨空间位置的语义关联。

### 4. HDR 重建

DiT 输出去噪后的 $\hat{\mathbf{E}}_{\mathrm{ldr}}$ 和 $\hat{\mathbf{E}}_{\mathrm{log}}$，经 VAE 解码器恢复为像素空间图像。随后，一个轻量级 MLP $\psi$ 对两者进行逐像素融合，重建完整的 HDR 环境图（Equation 3）：

$$\hat{\mathbf{E}} = \psi(\mathbf{E}_{\mathrm{ldr}}, \mathbf{E}_{\mathrm{log}})$$

### 5. 训练策略

训练分两阶段进行：

- **第一阶段**：在大规模合成渲染数据（随机几何、材质、光照）上预训练，学习物理上准确的光照先验。损失函数为标准噪声预测损失（Equation 4）；
- **第二阶段**：在筛选的真实 HDR 全景图上使用 LoRA 低秩适配微调，注入少量可学习参数 $\Delta\theta$（Equation 5），在保持预训练能力的同时提升输入场景与预测光照之间的语义对齐。

这种“合成预训练 + LoRA 语义适配”的策略，使得模型既能从合成数据中学习泛化的物理光照线索，又能通过真实数据适应语义场景。

### 3.1 双色调映射表示

HDR环境图的高动态范围使得标准VAE无法直接编码。LuxDiT将HDR全景图 $\mathbf{E}$ 分解为两个互补的LDR表示：

$$
\mathbf{E}_{\mathrm{ldr}} = \frac{\mathbf{E}}{1 + \mathbf{E}} \cdot \left(1 + \frac{\mathbf{E}}{M_{\mathrm{ldr}}^2}\right); \qquad \mathbf{E}_{\mathrm{log}} = \frac{\log(1 + \mathbf{E})}{\log(1 + M_{\mathrm{log}})}
$$

其中 $\mathbf{E}_{\mathrm{ldr}}$ 为Reinhard色调映射，保留高光细节；$\mathbf{E}_{\mathrm{log}}$ 为归一化对数强度，保留暗部信息。$M_{\mathrm{ldr}}$ 和 $M_{\mathrm{log}}$ 分别为两个映射的归一化常数。这一设计使标准VAE能够编码HDR内容，同时保持光照的物理精度。

### 3.2 HDR重建MLP

VAE解码器输出两个LDR图像后，通过一个轻量级逐像素MLP $\psi$ 融合重建完整HDR环境图：

$$
\hat{\mathbf{E}} = \psi\left(\mathbf{E}_{\mathrm{ldr}}, \mathbf{E}_{\mathrm{log}}\right)
$$

消融实验（Table 12）表明，简单的MLP融合与CNN或基于规则的方法精度相当，且能更好地处理数值不一致和范围溢出问题。

### 3.3 条件去噪扩散Transformer

模型将光照估计形式化为条件去噪任务。在潜空间中，扩散Transformer（DiT）联合处理条件token（来自输入图像的VAE编码）和噪声token（来自目标环境图的VAE编码），通过全局自注意力传播间接光照线索（阴影、反射等）。

**第一阶段训练损失**（合成数据预训练）：

$$
\mathcal{L}_{\mathrm{I}}(\theta) = \mathbb{E}_{\mathbf{z}_0, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}), t \sim \mathcal{U}(T)} \left[ \lVert \epsilon - \pmb{\mu}_{\theta}(\mathbf{z}_t, \mathbf{c}, t) \rVert_2^2 \right]
$$

其中 $\mathbf{z}_t$ 为加噪后的潜变量，$\mathbf{c}$ 为视觉条件token，$\pmb{\mu}_{\theta}$ 为DiT预测的噪声。

### 3.4 Token级条件嵌入机制

与通道级联（channel concatenation）不同，LuxDiT采用完全基于注意力的token条件机制：条件token和噪声token分别通过独立的AdaLN（自适应层归一化）模块处理，随后在Transformer层中通过自注意力交互。消融实验（Table 7）证实，通道级联变体在所有球面评估上角度误差显著升高（Laval Indoor Diffuse从4.08升至7.09，Poly Haven Diffuse从1.24升至7.09），验证了全局注意力条件机制对非空间对齐的光照估计至关重要。

### 3.5 LoRA语义适配

第二阶段在真实HDR全景图上进行参数高效微调，仅优化注入的低秩参数 $\varDelta\theta$：

$$
\mathcal{L}_{\mathrm{II}}(\varDelta\theta) = \mathbb{E}_{\mathbf{z}_0, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}), t \sim \mathcal{U}(T)} \left[ \left\| \epsilon - \mu_{\theta + \varDelta\theta}(\mathbf{z}_t, \mathbf{c}, t) \right\|_2^2 \right]
$$

LoRA适配器注入于Transformer层中，在保持预训练物理先验的同时提升输入场景与预测光照之间的语义对齐。Table 4显示，提高LoRA缩放因子可单调降低Poly Haven上的角度误差，但过大的LoRA尺度可能导致前景内容泄漏到环境图中（Table 13）。

## 实验与关键发现

### 5.1 主实验结果

LuxDiT 在三个标准基准数据集上与现有方法进行了全面对比，评估协议沿用先前工作统一的三球渲染方案（灰色漫反射球、银色哑光球、镜面球），度量指标包括尺度不变 RMSE（si-RMSE）、角度误差（AE）和归一化 RMSE（n-RMSE）。

**Table 1** 汇总了主要定量结果。在 Laval Outdoor 数据集上，LuxDiT 的漫反射球尺度不变 RMSE 达到 **0.068**，显著优于 **DiffusionLight**（Phongthawee et al., CVPR 2024）的 0.083（Δ = -0.015）。在 Poly Haven 数据集上，LuxDiT 的漫反射球角度误差为 **1.235**，相比 DiffusionLight 的 2.199 降低了 0.964。在 Laval Indoor 数据集上，LuxDiT 同样在多数指标上取得最优或次优结果。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_03680/figures/003_Table_1.jpg]]
*Table 1: Comparison of our method with baselines on three benchmark datasets. The results are reported in terms of scale-invariant RMSE, angular error, and normalized RMSE. Table 3: Quantitative comparison with video input. Peak angular error (PAE) is used to evaluate PolyHaven-Peak videos. Angular error (AE) on is used to evaluate WEB360 LDR videos*

方向精度方面，**Table 2** 报告了 Laval Outdoor 晴天场景上峰值亮度光源方向的角度误差。LuxDiT 将峰值角度误差（PAE）均值从 DiffusionLight 的 **44.4°** 降至 **23.7°**，降幅接近 50%（Δ = -20.7），中位数从 32.1° 降至 17.5°，证实了方向估计精度的大幅提升。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_03680/figures/004_Table_2.jpg]]
*Table 2: Angular error on estimated peak luminance light direction on Laval Outdoor sunny scenes*

视频输入场景下，**Table 3** 显示 LuxDiT 在 PolyHaven-Peak 视频上的 PAE 均值仅为 **5.21°**，而 DiffusionLight 为 19.09°（Δ = -13.88）；在 WEB360 LDR 视频上的角度误差为 5.218°。这表明视频输入提供的多帧信息进一步增强了光照估计的稳定性和精度。

**Figure 3** 的定性对比显示，LuxDiT 预测的环境图在光源位置、颜色和强度分布上与真值高度一致，而基线方法常出现光源位置偏移或强度估计偏差。**Figure 5** 的视频定性对比进一步表明，LuxDiT 在动态场景中保持了良好的时间一致性。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_03680/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative comparison with baseline methods on three benchmark datasets. DiPIR Figure 4: Qualitative comparison of virtual object insertion. Table 6: Ablation study on impact of camera elevation*

### 5.2 虚拟物体插入评估

为验证光照估计的下游应用效果，进行了虚拟物体插入的用户研究（Amazon Mechanical Turk）。**Table 8** 显示，68% 的参与者偏好 LuxDiT 的渲染结果，而仅 32% 偏好 DiffusionLight（Δ = +36%），表明 LuxDiT 预测的光照在真实感和语义一致性上具有显著优势。与基于逆渲染的 **DiPIR** 方法相比，LuxDiT 在 RMSE（0.047）和 SSIM（0.990）上达到可竞争水平，同时用户偏好超过 50%。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_03680/figures/010_Table_8.jpg]]
*Table 8: Quantitative evaluation of virtual object insertion. We report the percentage of images where users preferred Ours over baselines. A preference > 50% indicates Ours outperforming baselines*

### 5.3 消融实验

**Table 7** 系统消融了模型设计选择和训练数据策略，所有结果均采用三球协议的角度误差报告。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_03680/figures/007_Table_7.jpg]]
*Table 7: Ablation study on model design choices and training data. We report the angular error with threespheres protocol*

**条件嵌入机制：** 将 token 级条件机制替换为通道级联（channel concatenation）后，Laval Indoor 漫反射角度误差从最优值升至 7.09，Poly Haven 漫反射角度误差升至 7.09，性能显著退化。这证实了基于自注意力的 token 条件机制对非空间对齐的光照估计至关重要——全局注意力能够有效传播阴影、反射等间接光照线索，而通道级联无法实现这种跨空间的信息交互。

**合成数据预训练：** 移除合成渲染数据预训练后，模型在 Poly Haven（域内）上表现尚可，但在 Laval Indoor（跨域）上出现严重退化。这验证了大规模合成数据（随机几何、材质、光照条件）对学习可泛化物理光照先验的不可或缺性——仅靠真实 HDR 全景图无法覆盖足够多样化的光照配置。

**LoRA 微调尺度：** **Table 4** 显示，在 Poly Haven 上提高 LoRA 缩放因子可单调降低角度误差：LoRA scale = 0.25 时漫反射角度误差为 1.54°，scale = 1.00 时降至 **1.17°**，验证了 LoRA 微调对语义对齐的有效性。然而 **Table 13** 揭示了一个关键失败模式：在合成前景物体上，过大的 LoRA 尺度反而降低精度，因为它可能将前景内容泄漏到环境图中。这表明 LoRA 尺度需要在语义对齐和内容泄漏之间取得平衡。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_03680/figures/008_Table_4.jpg]]
*Table 4: Ablation study on impact of LoRA scale at inference time. Table 5: Ablation study on impact of camera field-of-view*

**HDR 融合方法：** **Table 12** 对比了 MLP、CNN 和基于规则的 HDR 融合方案，三者精度相当，简单 MLP 略占优势且能处理数值不一致和范围溢出问题。

**相机鲁棒性：** **Tables 5–6** 和 **Figure 14** 显示，在视场角（FOV）和相机仰角变化下，LuxDiT 性能保持稳定，仅在极端视角下出现轻微误差增加，表明模型对相机参数变化具有良好的泛化能力。

### 5.4 补充评估

**Table 9** 报告了室内数组球面协议上的评分，LuxDiT 在多数指标上优于 **Weber et al.**（2022）和 **EMLight** 等室内光照估计基线。**Table 10** 在 Cube++ 数据集上的 SpyderCube 白面渲染评估进一步验证了颜色和强度估计的准确性。**Table 11** 与 NeuS+Mitsuba 在 Objects with Lighting 数据集上的对比表明，LuxDiT 的生成式估计可与基于几何重建的方法相媲美。**Figure 11** 展示了从 NeRF 合成物体估计光照并重渲染的定性结果。

### 5.5 已知限制与失败模式

1. **颜色偏移与伪影：** 预测环境图中偶尔出现轻微颜色偏移（如 NeRF Lego 场景），且在某些纹理区域产生棋盘状伪影。
2. **大视角闪烁：** 虽然视频推理提高了时间一致性，但大视角变化下仍可能出现轻微闪烁。
3. **前景内容泄漏：** LoRA 微调尺度过大时，前景物体信息可能泄漏到环境图中（Table 13），需要在语义对齐和内容保真度之间权衡。
4. **极端光照条件：** 在合成数据未覆盖的极端罕见光照条件下，模型可能产生物理上不合理但语义合理的估计。
5. **推断速度：** 当前模型生成高分辨率输出所需计算资源较高，尚未优化至实时应用。

### 5.6 实验公平性说明

所有对比均采用与先前工作一致的三球渲染协议和评估脚本，确保度量计算的一致性。对于 Laval Indoor 数据集，使用了与 DiffusionLight 完全相同的测试 HDR 环境图和透视裁剪，数据分割无重叠。用户研究采用与先前工作相同的指令和图像对随机化，避免顺序偏差。

## 定位与知识库关联

### 与现有工作的关系

LuxDiT 处于生成式光照估计（generative lighting estimation）与扩散模型（diffusion models）的交叉地带，其核心贡献在于将视频扩散Transformer（DiT）引入 HDR 环境地图的条件生成，并通过合成数据预训练与 LoRA 微调的两阶段策略解决了数据稀缺与语义对齐的双重挑战。

**相对于基于修复的方法**：**DiffusionLight**（Phongthawee et al., CVPR 2024）利用预训练扩散模型对虚拟铬球进行修复来估计光照，其优势在于利用了大规模预训练先验，但受限于多曝光融合的繁琐流程和间接推理路径。LuxDiT 将光照估计直接形式化为条件生成任务，避免了修复过程中的歧义累积，在 Laval Outdoor 数据集上将峰值角度误差（PAE）降低近 50%（Table 2，PAE Mean 从 44.4 降至 23.7），验证了端到端条件生成范式的优越性。

**相对于基于 GAN 的方法**：**StyleLight**（Wang et al., arXiv 2022）基于 StyleGAN 生成 LDR/HDR 全景图，但其生成能力受限于 GAN 的模式坍塌倾向和有限的泛化能力。LuxDiT 的扩散框架天然具备更强的模式覆盖能力，且通过 DiT 的全局自注意力机制从阴影、反射等间接视觉线索中推断非局部光照信息，这是局部卷积架构难以实现的能力。

**相对于参数化估计方法**：传统方法如 **Hold-Geoffroy et al.**（CVPR 2017）仅估计户外光照的少量参数（如太阳方向、天空色温），无法捕获复杂的环境光照分布。LuxDiT 直接生成完整 HDR 全景图，在表达能力上存在质的差异。

**相对于基于优化的逆渲染方法**：**DiPIR** 等优化方法通过可微渲染迭代优化光照参数，精度高但计算成本巨大且依赖初始化。LuxDiT 作为前馈生成模型可在单次推理中产生高质量估计，在虚拟物体插入的用户研究中获得 68% 的偏好率（Table 8），表明其输出在实际应用中已具有竞争力。

### 适用边界与局限

LuxDiT 的性能边界主要由训练数据分布和模型设计选择共同定义：

1. **数据覆盖边界**：模型在合成数据未覆盖的极端光照条件下可能产生物理上不合理但语义合理的估计。合成数据虽然覆盖了随机几何、材质和光照的组合，但真实世界中存在罕见的复杂光照场景（如多色动态舞台灯光、水下散射光等），这些场景的估计精度缺乏保障。

2. **跨域泛化能力**：Table 7 的消融实验表明，移除合成数据预训练后，模型在 Laval Indoor 上出现严重域外退化，但在 Poly Haven（与合成数据分布更接近）上表现尚可。这说明合成数据的物理准确性对泛化至关重要，但也意味着模型对训练数据分布的依赖性较强。

3. **语义对齐的权衡**：LoRA 微调显著提升了语义对齐（Table 4，更高 LoRA 权重带来更低角度误差），但过大的 LoRA 尺度可能导致前景内容泄漏到环境图中（Table 13）。这一权衡表明当前的语义适配机制尚未完全解耦场景内容与光照信息。

4. **时间一致性**：虽然视频推理提高了时间一致性，但在大视角变化下仍可能出现轻微闪烁，限制了在动态 AR/VR 场景中的直接应用。

5. **计算资源需求**：推断速度尚未优化至实时应用，生成高分辨率输出所需的 DiT 推理成本仍然较高。

6. **输出保真度问题**：预测的环境图中偶尔出现轻微颜色偏移（如 NeRF Lego 场景）和棋盘状伪影，表明 VAE 编解码与 HDR 融合 MLP 的重建质量仍有提升空间。

### 开放问题

1. **生成式估计与优化式精炼的结合**：如何将 LuxDiT 的生成先验与基于可微渲染的优化方法（如 DiPIR）相结合，以前者提供高质量初始化，以后者进行物理约束下的精炼，从而在精度与效率之间取得更优平衡？

2. **实时推断的可行性**：能否通过知识蒸馏、模型量化或专用推理引擎将 DiT 的推理速度提升至实时（>30 FPS），以满足 AR/VR 应用的需求？

3. **超高分辨率输出**：当前输出分辨率受限于 VAE 潜空间尺寸，如何扩展至全景 4K 或更高分辨率以支持沉浸式应用？

4. **多模态输入的融合**：能否将光照估计扩展至多视角视频、深度图、甚至 LiDAR 点云等多模态输入，从而在动态场景中实现更稳定的时空一致预测？

5. **联合建模光照、几何与材质**：LuxDiT 当前仅估计光照，未联合建模场景几何和材质。如何构建端到端的通用场景重建框架，将光照估计作为逆渲染流水线的一个可学习模块，是通往完整场景理解的关键一步。

6. **不确定性量化**：扩散模型天然支持多次采样以估计预测分布，但 LuxDiT 尚未探索如何量化光照估计的不确定性，这对于安全关键应用（如自动驾驶中的光照感知）具有重要意义。

## 原文 PDF

![[paperPDFs/NEURIPS_2025/LuxDiT_Lighting_Estimation_with_Video_Diffusion_Transformer.pdf]]
