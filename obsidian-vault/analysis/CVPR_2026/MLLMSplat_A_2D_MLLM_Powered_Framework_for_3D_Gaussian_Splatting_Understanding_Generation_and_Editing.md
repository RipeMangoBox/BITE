---
title: "MLLMSplat: A 2D MLLM-Powered Framework for 3D Gaussian Splatting Understanding, Generation, and Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MLLMSplat_A_2D_MLLM_Powered_Framework_for_3D_Gaussian_Splatting_Understanding_Generation_and_Editing.pdf
project_link: null
code_link: null
aliases:
- MLLMSplat
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 关键调节点为：(1) 设计训练无关的 3DGS tokenizer，通过反渲染将 2D 特征聚合为视图一致的 3D 表征；(2) 引入双旋转位置编码（DRoPE）和双流解码器，将相机几何信息无损地注入 2D 扩散模型，保留预训练能力的同时提升 3D 一致性；(3) 通过联合训练与采样以及替代任务（新视角外推）实现高效的编辑，无需 3D 编辑数据集。
primary_logic: 通过将 3D 几何编码为相对位置嵌入（GaPE）并结合反渲染聚合的 tokenizer，可以以最小侵入性将 2D MLLM 强大的理解与生成能力扩展到 3DGS 场景，实现多任务统一框架。
claims:
- 消融实验显示，移除 DRoPE（改用拼接 Plücker 坐标）会大幅降低生成性能，证明几何信息注入的必要性。
- 在 3DGS 生成任务上，MLLMSplat 在 RealEstate10K 和 DL3DV-10K 的 FID 和 CLIPScore 上均显著超越现有方法（Director3D、SplatFlow、Prometheus）。
- ScanQA validation 上 CIDEr = 93.71
- SQA3D test 上 EM = 53.49
---

# MLLMSplat: A 2D MLLM-Powered Framework for 3D Gaussian Splatting Understanding, Generation, and Editing

> [!tip] 核心洞察
> 通过将 3D 几何编码为相对位置嵌入（GaPE）并结合反渲染聚合的 tokenizer，可以以最小侵入性将 2D MLLM 强大的理解与生成能力扩展到 3DGS 场景，实现多任务统一框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | MLLMSplat：基于 2D 多模态大语言模型的 3D 高斯泼溅理解、生成与编辑框架 |
| 英文题名 | MLLMSplat: A 2D MLLM-Powered Framework for 3D Gaussian Splatting Understanding, Generation, and Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xiu_MLLMSplat_A_2D_MLLM-Powered_Framework_for_3D_Gaussian_Splatting_Understanding_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MLLMSplat |
| Dataset | ScanQA validation, SQA3D test, RealEstate10K, DL3DV-10K |

> [!tip] 效果简介
> - ScanQA validation 上，CIDEr 93.71 vs – (LLaVA-Video-7B 原生 tokenizer) (显著提升)。
> - SQA3D test 上，EM 53.49 vs – (显著提升)。
> - RealEstate10K (validation) 上，FID 50.07 vs – (Director3D, SplatFlow, Prometheus 中最佳) (大幅领先)。

## 概要

**问题与瓶颈**：3D Gaussian Splatting（3DGS）在高效新视角合成上取得了显著成功，但现有研究大多局限于低层次感知、低质量生成与低效率编辑，无法像 2D 多模态大语言模型（MLLM）那样进行高层次语言推理与内容操控。核心瓶颈在于缺乏一种通用的机制，能将 2D MLLM 强大的理解与生成能力高效迁移到 3DGS 场景中，同时保留多视图一致性与预训练先验。

**方法与核心洞察**：MLLMSplat 提出了一套统一框架，通过两个关键组件——3DGS tokenizer 与 3DGS de-tokenizer——将 2D MLLM 适配到 3DGS 场景的理解、生成与编辑任务中。其核心洞察在于：通过反渲染将 2D 特征聚合为视图一致的 3D 表征，并以最小侵入性的方式将 3D 几何信息注入 2D 扩散模型，从而在保留预训练能力的同时实现多任务统一。

**关键技术定位**：
- **3DGS tokenizer**：通过 alpha 权重关联、最远点采样（FPS）与 Z-order 序列化，将多视图 2D 特征转换为视图一致的 3D 表征，馈入 MLLM 语言模型，显著提升 3D 场景理解能力。
- **双旋转位置编码（DRoPE）**：在扩散 Transformer 中引入几何感知位置编码（GaPE），利用相机投影矩阵的逆编码视角间相对几何变换，无损注入相机信息，保留预训练先验。
- **双流 3DGS 解码器**：冻结的 U-Net 分支提取多尺度特征，ViT 分支通过自注意力集成多视图信息，二者通过交叉注意力融合，将潜变量解码为 3D 高斯参数。
- **前馈式编辑**：通过替代任务（新视角外推）将 MLLM 的图像编辑能力迁移到 3DGS，实现单次前向的高效编辑，无需 3D 编辑数据集。

**主要结果**：在 3DGS 理解任务上，MLLMSplat 的 tokenizer 在 ScanQA 验证集上达到 CIDEr 93.71，在 SQA3D 测试集上 EM 达到 53.49，显著优于 MLLM 内置的 2D tokenizer。在 3DGS 生成任务上，于 RealEstate10K 和 DL3DV-10K 数据集上，FID 与 CLIPScore 均大幅领先 Director3D、SplatFlow、Prometheus 等现有方法。在 3DGS 编辑任务上，相比基于迭代优化的 DGE 方法，在五种编辑操作上均取得更高的 CLIP 相似度与方向相似度，同时推理时间从数分钟降至约 25 秒。消融实验验证了 DRoPE、双流解码器与速度修正（VelRe）等各组件的关键贡献。

**3D 高斯泼溅（3DGS）** 已成为高质量实时新视角合成的主流显式表征，凭借其可微分光栅化管线，在场景重建、动态建模等领域取得了显著进展。然而，现有 3DGS 研究主要聚焦于**低层次感知**（如场景重建与视角插值）、**低质量生成**（文本到 3D 场景的生成保真度有限）以及**低效率编辑**（依赖逐视图迭代优化，耗时且缺乏 3D 编辑数据），始终未能像 2D 多模态大语言模型（MLLM）那样，实现对场景的高层次语义理解与灵活内容操控。

核心瓶颈在于：**缺乏一个通用机制，能将 2D MLLM 强大的语言推理与生成先验高效迁移到 3DGS 场景**。具体而言，这一迁移面临两个关键挑战：第一，如何使 2D 视觉 tokenizer 具备 3D 感知能力，以支撑多视图一致的场景理解；第二，如何在保留 2D 预训练生成先验和条件可控性的同时，注入相机几何信息以增强 3D 一致性，实现高质量的 3DGS 生成。

针对上述缺口，本文提出 **MLLMSplat**——首个将 2D MLLM 统一适配到 3DGS 理解、生成与编辑的综合框架。其核心洞察在于：通过将 3D 几何编码为相对位置嵌入（Geometry-aware Positional Encoding, GaPE），并配合基于反渲染聚合的 3DGS tokenizer，能够以**最小侵入性**的方式将 2D MLLM 的能力扩展到 3DGS 场景，实现多任务统一。框架包含三项关键设计：(1) **3DGS tokenizer**——通过 alpha 权重关联、最远点采样（FPS）和 Z-order 序列化，将多视图 2D 特征聚合为视图一致的 3D 表征；(2) **3DGS de-tokenizer**——包含基于双旋转位置编码（DRoPE）的潜空间生成器和双流 VAE 解码器，在保留预训练先验的同时提升多视图一致性；(3) **替代任务（新视角外推）**——以训练无关的前馈方式实现高效 3DGS 编辑，规避了对 3D 编辑数据集的依赖。

## 核心方法与创新机理

MLLMSplat 的核心创新在于以最小侵入性的方式，将 2D 多模态大语言模型（MLLM）的强大能力迁移到 3D 高斯泼溅（3DGS）场景，构建了首个统一的理解、生成与编辑框架。其关键在于设计了一套训练无关的 3DGS tokenizer 和基于双旋转位置编码（DRoPE）与双流解码器的 de-tokenizer，解决了多视图一致性与预训练先验保留两大瓶颈。

### 关键创新点

**1. 训练无关的 3DGS Tokenizer：从 2D 特征到视图一致的 3D 表征**

现有方法直接将多视图渲染图像的 2D token 送入 MLLM，完全忽略了 3D 空间结构。MLLMSplat 提出了一种无需训练的 3DGS tokenizer，通过三个步骤将 2D 视觉特征转化为视图一致的 3D 表征：

- **特征关联**：利用 alpha 混合渲染中的贡献权重 $w_{ik}$，将多视图的 2D 视觉特征加权聚合到每个高斯上，得到视图一致的高斯特征 $g_i$（公式 2）。
- **最远点采样（FPS）**：设计了一种结合马氏距离（经 RBF 核变换）与特征余弦相似度的距离度量（公式 3），对高斯进行重采样以降低计算开销，同时保留场景的几何与语义结构。
- **Z-order 序列化**：采用 Z-order 空间填充曲线将 3D 高斯序列化为 1D token 序列，以保持空间局部性，便于 MLLM 的语言模型处理。

这一 tokenizer 可无缝集成到任意 MLLM 中，无需微调，在 ScanQA 和 SQA3D 基准上显著提升了 3D 场景理解性能（CIDEr 达 93.71，EM 达 53.49）。

**2. 双旋转位置编码（DRoPE）：将相机几何无损注入扩散 Transformer**

传统的相机条件化方式（如沿通道拼接 Plücker 坐标）会破坏预训练模型的输入分布，导致生成质量下降。MLLMSplat 提出了 DRoPE，将位置编码空间分解为两个正交分量：

- **视角内分量**：沿用标准 RoPE，保持预训练先验。
- **视角间分量**：引入几何感知位置编码（GaPE），通过相机投影矩阵的逆表示相对几何变换，使注意力计算编码了不同视角间的相对相机位姿（公式 5）：

$$\langle q_i^{\mathrm{GaPE}}, k_j^{\mathrm{GaPE}} \rangle = q_i^{\top} P_i P_j^{-1} k_j$$

这种设计无需引入额外参数，在保留预训练能力的同时有效提升了多视图一致性。消融实验证实，移除 DRoPE 会“大幅降低生成性能”。

**3. 双流 3DGS 解码器：融合多尺度先验与多视图信息**

传统单流 VAE 解码器仅修改首末卷积层，难以充分利用预训练 VAE 的鲁棒特征。MLLMSplat 设计了双流架构：

- **U-Net 分支**：冻结的预训练 VAE 编码器，提取多尺度图像先验特征。
- **ViT 分支**：利用自注意力集成多视图信息，并通过交叉注意力（Read 模块）周期性地从 U-Net 分支融合多尺度特征。

最终通过 DPT 头预测 splatter images（3D 高斯参数）。消融实验表明，移除双流设计会“导致性能明显降低”。

**4. 基于替代任务的前馈式 3DGS 编辑**

现有 3DGS 编辑方法（如 DGE）依赖基于 InstructPix2Pix 的迭代逐视图编辑与优化，耗时且缺乏 3D 编辑数据。MLLMSplat 创新性地将 MLLM 的图像编辑能力通过**替代任务**（新视角外推）迁移到 3DGS：联合训练时，模型学习从编辑后的参考视角外推新视角下的 3D 一致场景。编辑时仅需单次前向传播，平均耗时 25 秒，较迭代方法（数分钟）速度提升显著，且 CLIP 相似度与方向相似度均更高（Table 3）。

### 创新总结

| 设计维度 | 现有方法 | MLLMSplat 创新 |
|---------|---------|---------------|
| 3DGS 理解 tokenization | 直接使用 2D token，忽略 3D 结构 | 训练无关的 3DGS tokenizer（特征关联→FPS 重采样→Z-order 序列化） |
| 扩散 Transformer 位置编码 | 拼接 Plücker 坐标，破坏预训练分布 | DRoPE（RoPE + GaPE），无损注入相机几何 |
| VAE 解码器架构 | 单流架构，仅修改首末层 | 双流架构（冻结 U-Net + ViT + 交叉注意力融合） |
| 编辑策略 | 迭代逐视图编辑 + 3DGS 优化 | 前馈式编辑，通过新视角外推替代任务迁移 2D 编辑能力 |

这些创新共同构成了一个以 2D MLLM 为基础、以 3DGS tokenizer/de-tokenizer 为桥梁的统一框架，实现了从低层次感知到高层次语言推理与内容操控的跨越。

MLLMSplat 是一个将 2D 多模态大语言模型的能力迁移至 3D 高斯泼溅场景的统一框架，涵盖高层次理解、高质量生成与高效率编辑三大任务。其核心设计思想是以最小侵入性将 3D 几何信息注入 2D MLLM 的既有流程，从而保留预训练先验的同时获得多视图一致性。

框架由三个关键模块构成闭环：**3DGS Tokenizer** 负责将多视图渲染图像转化为视图一致的 3D 表征，供 MLLM 语言模型进行场景理解；**Latent Generator** 在 MLLM 的潜空间中生成多视图一致的潜变量，作为生成的中间表示；**3DGS Decoder** 则将潜变量解码为显式的 3D 高斯参数，并通过可微分渲染输出新视角图像。生成与解码模块共同构成“3DGS de-tokenizer”，使 MLLM 具备 3D 内容输出能力。

在理解任务中，给定一个 3DGS 场景，首先从多个预设视角渲染图像，经 MLLM 内置的 2D 视觉 tokenizer 提取逐像素特征。3DGS Tokenizer 利用 alpha 混合权重将这些 2D 特征关联回每个高斯，经最远点采样下采样后，按 Z-order 空间填充曲线序列化为一维 token 序列，直接馈入 MLLM 的语言模型进行问答推理。该 tokenizer 是训练无关的，可无缝接入任意 MLLM。

在生成任务中，Latent Generator 基于扩散 Transformer 架构，接收文本条件与相机几何信息，在 MLLM 的潜空间中生成多视图潜变量。其关键创新在于**双旋转位置编码**：视角内采用标准 RoPE，视角间则采用几何感知位置编码，通过相机投影矩阵的逆将查询和键变换到统一空间，使注意力计算自然编码了视角间的相对几何变换。随后，3DGS Decoder 采用双流架构——冻结的 U-Net 分支提取多尺度鲁棒特征，ViT 分支通过自注意力集成多视图信息，两者通过交叉注意力交互，最终由 DPT 头预测 splatter images（即 3D 高斯参数图）。训练时联合优化潜空间 MSE 损失与渲染损失，采样时通过自优化循环进一步增强多视图一致性。

在编辑任务中，框架利用**替代任务**策略规避 3D 编辑数据的缺失：将 MLLM 的图像编辑能力通过新视角外推任务迁移到 3DGS 场景。具体而言，给定输入视角图像和编辑指令，Latent Generator 生成目标视角的编辑后潜变量，再由 3DGS Decoder 解码为编辑后的高斯场，单次前向即可完成，无需迭代优化。

图 1 展示了框架的整体数据流：理解时，3D 场景经 tokenizer 进入 MLLM 输出文本；生成与编辑时，文本/图像指令经 de-tokenizer 输出 3DGS 场景。图 2 进一步揭示了模块内部的冻结（蓝色）、新增（红色）与微调（蓝红渐变）策略，体现了“最小侵入”的设计哲学。

![[assets/figures/papers/paper_list_l2171_https_openaccess_thecvf_com_content_CVPR2026_html_Xiu_MLLMSplat_A_2D_MLL/figures/001_Figure_1.jpg]]
*Figure 1: We propose MLLMSplat, a novel framework that adapts 2D MLLMs for high-level understanding, high-quality generation, and high-efficiency editing of 3DGS scenes. Our framework introduces two key components to the MLLM: a 3DGS tokenizer to enhance its 3DGS understanding and a 3DGS de-tokenizer to enable its 3DGS generation. Collectively, they unlock the capability for 3DGS editing*

MLLMSplat 框架的核心由三个关键模块构成：**3DGS Tokenizer**（3DGS 理解）、**Latent Generator**（潜空间生成器）和 **3DGS Decoder**（3DGS 解码器），后两者共同实现 3DGS 生成与编辑。以下逐一剖析各模块的设计逻辑与关键公式。

---

### 3DGS Tokenizer：训练无关的多视图特征聚合与序列化

**设计目标**：将 2D MLLM 原生的视觉 tokenizer 输出的多视图 2D 特征，转化为视图一致的 3D 高斯表征，从而提升 MLLM 对 3D 场景的高层次理解能力。该模块**无需训练**，可无缝集成到任意 MLLM 中。

**核心流程**（见 Figure 2 左半部分）：

1. **特征关联**：对于输入 3DGS 场景，渲染 $K$ 个视角的图像。通过 alpha 混合渲染方程，建立每个高斯 $G_i$ 与各视角像素之间的贡献权重 $w_{ik}$：

   $$C_{k} = \sum_{i=1}^{N} c_{i} \alpha_{i k} \prod_{j=1}^{i-1} (1 - \alpha_{j k}) = \sum_{i=1}^{N} c_{i} w_{i k} \tag{1}$$

   其中 $c_i$ 为高斯颜色，$\alpha_{ik}$ 为视角 $k$ 下的 alpha 值，$w_{ik}$ 为高斯 $i$ 对视角 $k$ 中对应像素的贡献权重。

2. **特征聚合**：利用 $w_{ik}$ 作为权重，对 2D 视觉 tokenizer 提取的逐像素特征 $f_k$ 进行跨视角加权平均，获得每个高斯的视图一致特征 $g_i$：

   $$g_{i} = \frac{\sum_{k=1}^{K} w_{i k} f_{k}}{\sum_{k=1}^{K} w_{i k}} \tag{2}$$

   这一操作使原本分散在多视图 2D 空间中的特征信息被“反渲染”聚合到 3D 高斯上，形成对场景几何结构的隐式编码。

3. **重采样与序列化**：为控制送入 MLLM 语言模型的 token 数量并保留空间局部性，采用**最远点采样（FPS）** 对高斯进行下采样。采样所用的距离度量融合了马氏距离（经 RBF 核化）与特征余弦相似度：

   $$d(G_{i}, G_{j}) = 2 - \mathrm{RBF}\left(\Delta \mu^{\top} \Sigma^{-1} \Delta \mu\right) - \frac{g_{i}^{\top} g_{j}}{\|g_{i}\| \|g_{j}\|} \tag{3}$$

   其中 $\Delta \mu$ 为两高斯中心的位移向量，$\Sigma^{-1}$ 为协方差逆矩阵。采样后的高斯特征按 **Z-order 空间填充曲线**进行 1D 序列化，以最大程度保留空间邻接关系。

**关键洞察**：该 tokenizer 的核心价值在于以**零训练成本**将 3D 几何信息注入 MLLM 的输入空间，使语言模型能够直接“感知”高斯的空间分布与外观特征，从而显著提升 3D 场景问答等理解任务性能（见 Table 1）。

---

### Latent Generator：双旋转位置编码与几何感知注意力

**设计目标**：在 MLLM 的潜空间中生成多视图一致的潜变量，作为后续 3DGS 解码的输入。核心挑战在于如何将相机几何信息注入扩散 Transformer，同时**不破坏预训练模型的先验分布**。

**DRoPE（双旋转位置编码）** 是此模块的关键创新。标准扩散 Transformer 使用 RoPE 编码 token 序列位置，但无法处理多视图间的相机几何关系。MLLMSplat 引入双旋转位置编码空间：

- **视角内分量**：沿用标准 RoPE，编码同一视角内 token 的位置关系。
- **视角间分量**：采用**几何感知位置编码（GaPE）**，通过相机的 4×4 投影矩阵编码视角间的相对几何变换。对于相机 $i$，其投影矩阵定义为：

  $$P_{i} = \begin{bmatrix} K_{i} R_{i} & K_{i} t_{i} \\ 0 & 1 \end{bmatrix} \tag{4}$$

  其中 $K_i$ 为内参矩阵，$R_i$ 和 $t_i$ 为外参旋转与平移。GaPE 的核心在于利用投影矩阵的逆，将查询和键变换到统一的规范空间后再计算注意力：

  $$\langle q_{i}^{\mathrm{GaPE}}, k_{j}^{\mathrm{GaPE}} \rangle = \langle P_{i}^{\top} q_{i}, P_{j}^{-1} k_{j} \rangle = q_{i}^{\top} P_{i} P_{j}^{-1} k_{j} \tag{5}$$

  这意味着注意力权重天然编码了视角 $i$ 和 $j$ 之间的相对相机变换 $P_i P_j^{-1}$，使模型能够推理不同视角间的几何对应关系。

**设计优势**：与简单拼接 Plücker 坐标等相机条件化方式不同，DRoPE 通过旋转位置编码的形式注入几何信息，**不改变 token 维度**，从而保留预训练扩散模型对输入分布的期望。消融实验（Table 4）证实，移除 DRoPE 会“破坏预训练模型的输入分布”，导致生成质量大幅下降。

**训练目标**：Latent Generator 采用 Rectified Flow 框架。给定噪声 $x_0$ 和目标潜变量 $x_1$，中间潜变量通过线性插值构建：

$$x_{t} = t x_{1} + (1 - t) x_{0} \tag{6}$$

真实速度场为 $v_t = x_1 - x_0$，模型学习预测该速度。整体训练损失联合优化潜空间 MSE 损失与渲染损失：

$$\mathcal{L} = \mathbb{E}_{t} [ \mathcal{L}_{\mathrm{latent}}(u_{t}, v_{t}) + \omega(t) \mathcal{L}_{\mathrm{render}}(\hat{I}, I) ] \tag{10}$$

其中 $\omega(t)$ 为时变权重，$\mathcal{L}_{\mathrm{render}}$ 监督解码后渲染图像与真实图像的一致性。

---

### 3DGS Decoder：双流架构与多视图特征融合

**设计目标**：将 Latent Generator 生成的多视图潜变量解码为 3D 高斯参数（以 splatter images 形式输出），并通过可微分渲染生成新视角图像。

**双流架构**（见 Figure 2 右半部分）是此模块的核心设计：

- **U-Net 分支（冻结）**：复用预训练 VAE 的 U-Net 编码器-解码器结构，提取多尺度鲁棒特征。冻结该分支可保留预训练先验，避免过拟合。
- **ViT 分支（可训练）**：利用自注意力机制集成多视图信息，增强跨视角一致性。
- **交叉注意力融合**：两分支通过周期性的 Read 块进行交互，ViT 分支以交叉注意力方式查询 U-Net 的多尺度特征，实现预训练先验与多视图几何信息的融合。
- **DPT 头**：最终通过 DPT（Dense Prediction Transformer）头预测 splatter images，即逐像素的高斯参数图。

**渲染监督**：解码得到的高斯场在输入视角 $\{V_i\}$ 和新视角 $\{V_n\}$ 下渲染：

$$\hat{I} = [\hat{I}_{i}, \hat{I}_{n}] = \mathcal{R}(\mathcal{D}(z_{1}, V_{i}), [V_{i}, V_{n}]) \tag{9}$$

其中 $\mathcal{D}$ 为解码器，$\mathcal{R}$ 为可微分渲染器。渲染损失同时约束输入视角的重建质量和新视角的 3D 一致性。

**消融验证**：移除双流架构（简化为单流）会导致性能明显下降，因为“无法有效利用预训练 VAE 的鲁棒特征”（Section 4.5, Table 4）。

---

### 编辑策略：替代任务与前馈式编辑

MLLMSplat 的编辑能力通过**替代任务（Surrogate Task）** 实现，避免了对 3D 编辑数据集的依赖。具体而言，将 MLLM 原生的 2D 图像编辑能力通过**新视角外推**任务迁移到 3DGS：给定源视角的编辑后图像作为条件，Latent Generator 在 DRoPE 的几何约束下生成多视图一致的潜变量，再由 3DGS Decoder 一次性解码为编辑后的 3D 场景。整个过程为**单次前馈**，无需迭代优化，编辑速度（约 25 秒）远超基于 InstructPix2Pix 的迭代方法（数分钟），且 CLIP 相似度与方向相似度均更优（Table 3）。

---

### 联合采样与速度修正

在推理采样阶段，为进一步增强多视图一致性，引入**速度修正（Velocity Refinement）** 自优化循环：将中间潜变量解码为 3DGS 并渲染回输入视角，用渲染图像重新编码为潜变量，以此修正速度预测。消融实验（Table 4）表明，移除速度修正会导致多视图一致性和渲染质量下降。

![[assets/figures/papers/paper_list_l2171_https_openaccess_thecvf_com_content_CVPR2026_html_Xiu_MLLMSplat_A_2D_MLL/figures/002_Figure_2.jpg]]
*Figure 2: Details of MLLMSplat framework. Blue, red, and blue-to-red gradient indicate frozen, added, and finetuned modules, respectively. The 3DGS tokenizer associates features from the 2D visual tokenizer with Gaussians, filters (and downsamples) them, and finally applies Z-order serialization before feeding them to the language model. The latent generator employs a dual rotary positional encoding space, where “Ro” and “Ga” are short for RoPE and GaPE, respectively; cells filled with “Ga$\Ro$” indicate their equivalence. The reference latent is provided as input only for editing. The 3DGS decoder features two parallel branches that periodically interact via Read blocks*

## 实验与关键发现

### 3DGS 理解任务

为验证 3DGS tokenizer 对场景理解能力的提升，本文在 ScanQA 验证集和 SQA3D 测试集上，将基于 LLaVA-Video-7B 内置 2D 视觉 tokenizer 的基线，与插入本文 Gaussian tokenizer 后的变体进行对比（Table 1）。Gaussian tokenizer 是训练无关的模块，可无缝嵌入任意 MLLM，无需微调。实验设定为从输入 3DGS 渲染 16 幅 640×480 的多视图图像，经 tokenizer 聚合为视图一致的 3D 表征后馈入语言模型。

![[assets/figures/papers/paper_list_l2171_https_openaccess_thecvf_com_content_CVPR2026_html_Xiu_MLLMSplat_A_2D_MLL/figures/003_Table_1.jpg]]
*Table 1: Experimental results of 3DGS Understanding on the validation set of ScanQA [1] and the test set of SQA3D [33]*

结果显示，Gaussian tokenizer 在所有指标上均带来显著提升：ScanQA 上 CIDEr 达到 93.71，SQA3D 上精确匹配（EM）达到 53.49，EM-R 达到 56.19。这表明，通过 alpha 权重关联、FPS 重采样和 Z-order 序列化构建的 3D 表征，能够比直接使用 2D token 更有效地向 MLLM 传递 3D 空间结构与语义信息，从而提升高层场景理解能力。

### 3DGS 生成任务

3DGS 生成实验在 RealEstate10K 和 DL3DV-10K 的验证集上进行，评估指标为 FID 和 CLIPScore。对比方法包括 Director3D（Li et al., NeurIPS 2024）、SplatFlow 和 Prometheus。如 Table 2 所示，MLLMSplat 在两个数据集上均以显著优势领先所有基线：在 RealEstate10K 上 FID 为 50.07，CLIPScore 为 25.79；在 DL3DV-10K 上 FID 为 53.67，CLIPScore 为 27.68。定性结果（Figure 3）进一步表明，本方法生成的多视图图像在几何一致性和纹理细节上均明显优于对比方法，而 Director3D、SplatFlow 和 Prometheus 在不同程度上存在模糊、伪影或视图不一致的问题。

![[assets/figures/papers/paper_list_l2171_https_openaccess_thecvf_com_content_CVPR2026_html_Xiu_MLLMSplat_A_2D_MLL/figures/004_Table_2.jpg]]
*Table 2: Experimental results of 3DGS Generation on the validation sets of RealEstate10K [73] and DL3DV-10K [32]*

生成性能的大幅领先源于两个关键设计。**DRoPE** 将相机几何信息以最小侵入性注入扩散 Transformer：视角内分量沿用标准 RoPE，视角间分量采用 GaPE，通过投影矩阵的逆编码相对相机变换（$q_i^\top P_i P_j^{-1} k_j$），既保留了预训练先验，又增强了 3D 一致性。**双流解码器**则通过冻结的 U-Net 分支提取多尺度鲁棒特征，ViT 分支利用自注意力集成多视图信息，二者通过交叉注意力融合，最终以 DPT 头预测 splatter images，避免了单流架构对预训练 VAE 特征的浪费。

### 3DGS 编辑任务

编辑任务在 10 个场景上评估五种编辑操作（如物体增删、风格迁移等），对比方法为基于迭代优化的 DGE（包含 GaussianEditor 和 Editsplat）。如 Table 3 所示，MLLMSplat 在 CLIP 相似度（26.91）和 CLIP 方向相似度（22.40）上均优于 DGE，且平均推理时间仅需 25 秒，而 DGE 需数分钟。定性对比（Figure 4）显示，本方法在编辑精度和视图一致性上表现更优，而 DGE 在部分操作上存在细节丢失或跨视图不一致。

![[assets/figures/papers/paper_list_l2171_https_openaccess_thecvf_com_content_CVPR2026_html_Xiu_MLLMSplat_A_2D_MLL/figures/007_Figure_4.jpg]]
*Figure 4: Visual comparison of 3DGS Editing results across DGE [6] and our method on five types of editing operations*

编辑能力的关键在于**替代任务**设计：由于缺乏 3D 编辑数据集，本文通过新视角外推任务，将 MLLM 的图像编辑能力迁移到 3DGS 场景，实现单次前馈编辑，无需迭代优化。在推理时，参考潜变量作为条件输入 Latent Generator，引导生成编辑后的多视图一致表征。

### 消融实验

为验证各组件的贡献，在 3DGS 生成任务上进行了消融实验（Table 4），移除以下三个关键设计：

![[assets/figures/papers/paper_list_l2171_https_openaccess_thecvf_com_content_CVPR2026_html_Xiu_MLLMSplat_A_2D_MLL/figures/008_Table_4.jpg]]
*Table 4: Ablation results for 3DGS Generation on the validation sets of RealEstate10K [73] and DL3DV-10K [32]*

- **w/o DRoPE**：将 DRoPE 替换为 MRoPE 并沿通道拼接 Plücker 坐标以提供相机信息。该变体性能大幅下降，因为简单拼接相机嵌入破坏了预训练模型期望的输入分布，导致生成质量恶化。这证实了 GaPE 以几何变换形式注入相机信息的必要性。
- **w/o DualS（双流解码器）**：将解码器简化为单流架构，仅修改首末卷积层以适配输入输出。性能明显降低，因为单流架构无法有效利用预训练 VAE 的鲁棒多尺度特征，多视图信息集成能力不足。
- **w/o VelRe（速度修正）**：在联合采样过程中移除自优化循环，即不再通过渲染-重编码步骤修正速度预测。该变体导致多视图一致性和渲染质量下降，验证了速度修正对增强跨视角一致性的关键作用。

以上消融结果一致表明，DRoPE、双流解码器和速度修正三个组件各自对最终性能有不可替代的贡献，任意一个的缺失都会导致生成质量显著退化。

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

现有 3D 高斯泼溅（3DGS）研究主要停留在三个低层次维度：**低层次感知**（如语义分割、目标检测）、**低质量生成**（受限于 3D 数据规模）和**低效率编辑**（依赖迭代优化，耗时数分钟）。这些方法无法像 2D 多模态大语言模型（MLLM）那样进行高层次语言推理与内容操控。核心瓶颈在于缺乏将 2D MLLM 的能力高效迁移到 3DGS 场景的通用机制，尤其是**多视图一致性**与**预训练先验的保留**这两个关键约束难以同时满足。

### 2. 与基线方法的关系

#### 2.1 3DGS 理解基线

直接使用 MLLM 内置的 2D 视觉 tokenizer 处理多视图渲染图像（如 **LLaVA-Video-7B**）是直观的基线方案。但该方案将每帧图像独立编码，完全忽略 3D 空间结构，导致 token 序列冗长且缺乏视图间关联。MLLMSplat 提出的 **3DGS tokenizer** 通过反渲染将 2D 特征关联到高斯原语，利用最远点采样（FPS）和 Z-order 曲线序列化，形成紧凑且视图一致的 3D 表征，且无需任何训练即可接入任意 MLLM。

#### 2.2 3DGS 生成基线

现有文本到 3DGS 场景生成方法可归为两类：
- **直接 3D 生成方法**：如 **Director3D**（Li et al., NeurIPS 2024）、**SplatFlow** 和 **Prometheus**。这些方法通常从零开始设计 3D 生成架构，未能充分利用 2D 扩散模型的强大预训练先验，导致生成质量受限。
- **2D 先验迁移方法**：MLLMSplat 的关键创新在于以**最小侵入性**将 2D 扩散 Transformer 适配到多视图 3DGS 生成。具体而言，**双旋转位置编码（DRoPE）** 将相机几何信息编码为相对位置嵌入（GaPE），通过投影矩阵的逆变换保持与预训练 RoPE 的数学等价性，避免破坏预训练模型的输入分布。消融实验证实，若移除 DRoPE 并改用拼接 Plücker 坐标的 MRoPE，会“破坏预训练模型期望的输入分布”（Section 4.5），导致生成质量大幅下降。

#### 2.3 3DGS 编辑基线

现有文本驱动 3DGS 编辑方法（如 **DGE**，含 GaussianEditor / Editsplat）基于 InstructPix2Pix 进行迭代优化：逐视图编辑图像后反复优化 3DGS 场。该范式存在两个根本缺陷：**耗时**（数分钟级别）且**缺乏 3D 编辑数据**，难以学习真正的 3D 编辑操作。MLLMSplat 另辟蹊径，将编辑问题转化为**替代任务**——新视角外推：通过联合训练潜空间生成器和 3DGS 解码器，使 MLLM 学会从参考视角外推编辑后的新视角，单次前馈即可完成编辑（约 25 秒），且无需任何 3D 编辑数据集。

### 3. 方法谱系中的坐标定位

MLLMSplat 在以下技术维度上占据独特位置：

| 技术维度 | 传统 3DGS 方法 | 2D MLLM 直接应用 | MLLMSplat |
|---------|---------------|-----------------|-----------|
| 3D 感知机制 | 显式 3D 体素/点云 | 无（逐帧 2D 编码） | 反渲染聚合 + GaPE 几何编码 |
| 生成先验来源 | 从零训练 3D 生成器 | 2D 扩散模型（无 3D 一致性） | 2D 扩散模型（DRoPE 保留先验 + 多视图一致性） |
| 编辑效率 | 迭代优化（数分钟） | 逐帧编辑 + 3D 重建 | 单次前馈（25 秒） |
| 训练数据需求 | 大规模 3D 数据 | 2D 数据 | 2D 数据 + 多视图渲染（无需 3D 编辑数据） |

### 4. 适用边界与局限

**适用场景**：
- 静态 3DGS 场景的高层次语言理解（如空间关系问答、场景描述）
- 文本到 3DGS 场景的生成（室内外场景均适用）
- 五种常见编辑操作（物体替换、材质修改、风格迁移等）的前馈式编辑

**已知局限**（论文未明确列出，需从方法设计推断）：
- 3DGS tokenizer 依赖多视图渲染，对单视图 3DGS 场景的适用性未经验证
- 生成质量受限于底层 2D 扩散模型的能力边界（如 Flux 的文本理解偏差会传导至 3D 生成）
- 编辑操作的类型受限于替代任务（新视角外推）所能泛化的范围，极端几何变形可能超出能力边界
- 序列化采用 Z-order 曲线，对非均匀空间分布的高斯场可能存在局部性损失

### 5. 开放问题

论文明确提出了两个开放问题，指向该方向的未来工作：

1. **无监督 3D 感知 tokenization**：能否设计一种训练无关且模型无关的方法，使任意 2D tokenizer 获得 3D 感知能力？当前 3DGS tokenizer 虽然无需微调 MLLM，但仍需访问高斯的几何属性（位置、协方差）和 alpha 权重，对黑盒 2D tokenizer 不适用。

2. **生成先验的无损迁移**：能否在保持条件可控性和 3D 一致性的同时，将 2D 生成模型的先验**完全无损**地迁移到 3DGS 生成？当前 DRoPE 方案虽大幅保留了预训练先验，但双流解码器和联合训练仍引入了额外的可学习模块，可能造成一定程度的先验偏移。

### 6. 证据强度评估

- **高置信度证据**（confidence ≥ 0.95）：DRoPE 的消融实验（Table 4）、3DGS 生成的定量对比（Table 2）、3DGS 理解的 tokenizer 对比（Table 1）均提供了明确的量化支撑，且消融设计合理（逐组件移除）。
- **中置信度证据**（confidence 0.9）：编辑任务的定量对比（Table 3）仅在 10 个场景上评估，样本量偏小，且 DGE 基线的具体实现细节未完全披露，需手动验证公平性。
- **需注意的缺失**：论文未报告 3DGS 理解的消融实验（如不同采样策略、序列化方法的影响），也未在更具挑战性的动态场景或大规模开放场景上评估生成能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/MLLMSplat_A_2D_MLLM_Powered_Framework_for_3D_Gaussian_Splatting_Understanding_Generation_and_Editing.pdf]]
