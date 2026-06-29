---
title: Object-level Scene Deocclusion
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Object_level_Scene_Deocclusion.pdf
project_link: "https://liuzhengzhe.github.io/Deocclude-Any-Object.github.io/"
code_link: null
aliases:
- OLSD
tags:
- SIGGRAPH_2024
- topic/other_unclear
core_operator: 采用并行变分自编码器（Parallel VAE）将多物体编码为统一全视图特征图，并训练可见到完整的潜在扩散生成器，实现单次扩散并行补全多个物体（结合分层策略），从而同时提升生成质量与推理效率。
primary_logic: 将场景去遮挡重新表述为一个条件潜在扩散任务：从部分可见物体的特征图与文本提示出发，生成包含所有物体完整信息的全视图特征图，再利用交叉注意力解码恢复每个物体的完整外观，避免了逐物体建模和掩码依赖。
claims:
- 在COCOA验证集上，PACO相比SSSD在amodal mask IoU上提升1.93（89.52 vs 87.59），FID降低1.12（13.93 vs 15.05），遮挡顺序准确率提升0.6（90.0 vs 89.4）。
- 分层去遮挡策略将平均扩散过程从7.19次降至2.50次（减少65%），而FID仅轻微增加0.14（13.93 vs 13.79）。
- PACO在真实照片、OOD图像和跨域场景（ADE20k）上均能生成高质量且身份一致的补全，明显优于SSSD与修补基线。
- COCOA 验证集 上 amodal mask IoU = 89.52
---

# Object-level Scene Deocclusion

> [!tip] 核心洞察
> 将场景去遮挡重新表述为一个条件潜在扩散任务：从部分可见物体的特征图与文本提示出发，生成包含所有物体完整信息的全视图特征图，再利用交叉注意力解码恢复每个物体的完整外观，避免了逐物体建模和掩码依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | 对象级场景去遮挡 |
| 英文题名 | Object-level Scene Deocclusion |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2406.07706) · [Project](https://liuzhengzhe.github.io/Deocclude-Any-Object.github.io/) |
| Topic | #topic/other_unclear |
| Method | PACO |
| Dataset | COCOA 验证集 |

> [!tip] 效果简介
> - COCOA 验证集 上，amodal mask IoU 89.52 vs 87.59 (+1.93)；FID (外观保真度) 13.93 vs 15.05 (-1.12)；遮挡顺序准确率 90.0 vs 89.4 (+0.6)。

## 概要

现有场景去遮挡方法面临双重瓶颈：生成保真度不足，且逐物体扩散推理效率过低，难以处理包含多个被遮挡物体的真实场景。本文提出 **PACO**（PArallel object-level COmpletion），将场景去遮挡重新表述为条件潜在扩散任务。核心思路是训练一个并行变分自编码器（Parallel VAE），将多个物体编码为统一的全视图特征图，再通过可见到完整的潜在扩散生成器，从部分可见特征图与文本提示出发，单次扩散并行补全多个物体。推理时结合分层去遮挡策略，利用深度信息将场景按遮挡关系分层，同层物体在同一扩散过程中完成补全。

在 COCOA 验证集上，PACO 相比主要基线 **SSSD**（Zhan et al., CVPR 2020）在非模态掩码 IoU 上提升 1.93（89.52 vs 87.59），FID 降低 1.12（13.93 vs 15.05）；分层策略将平均扩散过程从 7.19 次降至 2.50 次（减少 65%），而生成质量仅轻微下降。方法定位上，PACO 以并行编码替代单物体独立建模，以分层并行扩散替代逐物体推理，属于对象级场景补全的新范式。

## 核心方法与创新机理

PACO将场景去遮挡重新定义为一个**条件潜在扩散生成任务**，其核心创新在于将多物体补全从逐物体独立建模转变为统一的并行潜在空间生成。整个框架由两个训练阶段和一种分层推理策略构成，形成了从物体编码、潜在生成到最终解码的完整因果链路。

### 问题瓶颈与核心机制

现有场景去遮挡方法的根本瓶颈在于生成保真度与推理效率的双重不足。以SSSD为代表的逐物体扩散方法需要为每个被遮挡物体单独执行一次完整的扩散推理过程，不仅计算开销随物体数量线性增长，而且每次独立生成缺乏对场景全局结构的感知，容易产生与目标物体身份不一致的补全内容。修补模型（如Stable Diffusion Inpainting）虽然生成质量较高，但依赖已知的非模态掩码，且在遮挡区域可能混淆遮挡物与被遮挡物的归属关系，甚至凭空生成新物体（见Figure 2）。

PACO的关键洞察是：**将多物体的完整信息压缩到一个统一的全视图特征图（full-view feature map）中，然后从部分可见的观测出发，通过单次扩散过程生成该特征图，再利用交叉注意力解码恢复每个物体的完整外观**。这一设计同时解决了三个问题：避免了逐物体建模的冗余计算、消除了对预知掩码的依赖、通过全局特征图保证了物体间的空间一致性。

### 核心Changed Slots

相比现有基线，PACO在以下关键维度上进行了根本性改变：

**1. 物体编码方式：从独立编码到并行堆叠编码**

基线方法（如SSSD、VINV）对每个物体进行独立编码和补全，各物体之间缺乏信息交互。PACO引入并行变分自编码器（Parallel VAE），将场景中所有物体的完整图像堆叠后，通过编码器E1提取各自特征，再经特征图求和（early-fusion）聚合为单一的全视图特征图。这一设计使得特征图天然包含所有物体的空间布局和相互遮挡关系。

**2. 去遮挡推理方式：从逐物体扩散到分层并行扩散**

SSSD需要为每个物体执行一次完整的扩散去噪过程，COCOA场景平均需要7.19次扩散。PACO采用分层策略（Layer-wise Deocclusion），利用深度信息将场景按遮挡关系分为若干深度层，同一层内的多个物体在单次扩散中同时补全，将平均扩散次数降至2.50次（减少65%）。

**3. 生成条件：从仅可见图像到多模态条件融合**

PACO的可见到完整潜在生成器接收的条件不仅包括部分视图特征图，还融合了类别文本提示（通过GPT-4V获取）、边缘图和物体掩码。文本提示使模型能够利用预训练扩散模型中的类别先验知识，在严重遮挡情况下仍能保持物体身份的完整性。

### 模块架构与因果链路

PACO框架包含五个核心模块，按训练和推理的因果顺序组织如下：

**阶段一：Parallel Variational Autoencoder (E1, D1)**

编码器E1接收堆叠的完整物体图像，通过卷积提取特征后求和得到全视图特征图 $f$。解码器D1的核心创新在于其交叉注意力查询机制：对于每个物体 $O_i$，以其部分可见掩码 $m_i$ 作为查询（Query），从全视图特征图 $f$ 中提取该物体专属的特征图 $f_i$：

$$f_i = \mathrm{softmax}\left( \frac{ W_Q(m_i) W_K(f)^T }{ \sqrt{c} } \right) W_V(f)$$

这一设计的因果逻辑是：**使用掩码而非可见物体图像作为查询，迫使解码器必须从全视图特征图中检索信息，而非简单复制输入**。这保证了即使物体大部分被遮挡，解码器仍能从特征图的全局上下文中恢复其完整外观。阶段一的总损失函数为：

$$\mathcal{L} = L_{\mathrm{r}} + \lambda_1 L_{\mathrm{p}} + \lambda_2 L_{\mathrm{avd}} + \lambda_3 L_{\mathrm{kl}} + \lambda_4 L_{\mathrm{m}}$$

其中回归损失 $L_{\mathrm{r}} = \sum_i \sum_j || R_{i,j} - I_{i,j} ||_2^2$ 确保像素级重建精度，感知损失 $L_{\mathrm{p}}$ 保持语义一致性，对抗损失 $L_{\mathrm{avd}}$ 提升真实感，KL散度损失 $L_{\mathrm{kl}}$ 正则化潜在空间，掩码损失 $L_{\mathrm{m}}$ 监督非模态掩码预测。

**阶段二：Visible-to-Complete Latent Generator (E2, D2, E2c)**

该模块采用类ControlNet架构，在冻结的预训练扩散U-Net基础上添加可训练的复制编码器E2c。其输入为噪声化的完整特征图 $f_t$ 与零卷积处理的部分视图特征图 $\mathcal{Z}_1(f_p)$ 之和：$f_t + \mathcal{Z}_1(f_p)$。解码器D2的初始层输入融合了冻结编码器E2的输出和E2c的输出：

$$E_2(f_t) + \mathcal{Z}_2(E_{2c}(f_t + \mathcal{Z}_1(f_p)))$$

训练目标为标准去噪损失：

$$L_{\mathrm{v2c}} = \mathbb{E}_{t, C_0, \varepsilon} \left[ || \varepsilon - \varepsilon_\theta(f_t, t, f_\phi, T, E, m_o) ||^2 \right], \quad \varepsilon \sim \mathcal{N}(0, I)$$

其中条件包括部分视图特征 $f_\phi$、文本提示 $T$、边缘图 $E$ 和物体掩码 $m_o$。冻结E2的策略保留了Stable Diffusion在海量数据上习得的丰富先验，而仅微调D2和E2c则使模型快速适应从部分视图到完整特征图的映射任务。

**阶段间的因果关系**：阶段一训练出的Parallel VAE提供了两个关键能力——将完整物体编码为全视图特征图的能力（为阶段二提供训练目标），以及从全视图特征图中通过掩码查询恢复单个物体的能力（为推理时解码提供工具）。阶段二学习的可见到完整生成器，本质上是在阶段一构建的潜在空间中执行条件生成，弥合了部分观测与完整场景之间的信息鸿沟。

**推理路径**：给定输入图像，首先通过SAM获取实例分割掩码，GPT-4V提供类别文本提示。深度估计确定物体间的遮挡层次。对于每一深度层，将该层所有物体的部分视图编码为部分特征图，输入可见到完整生成器，经扩散去噪生成全视图特征图。最后，解码器D1利用各物体的部分掩码从全视图特征图中交叉注意力查询，恢复每个物体的完整外观和非模态掩码。

**训练数据生成：Object Ensemble Dataset**

为支持自监督训练，PACO设计了物体集成数据集生成器。从COCO数据集的85,000个物体实例中随机采样2-8个物体，通过随机缩放、旋转和叠加合成场景图像，同时自然产生遮挡关系和完整的非模态掩码真值。这一合成策略使训练完全无需人工标注，且物体组合的多样性（500k图像）保证了模型的泛化能力。

### 分层去遮挡策略的因果机制

分层策略（Figure 5）是连接模型设计与实际推理效率的关键。其因果逻辑在于：**同一深度层内的物体之间不存在相互遮挡，它们的补全可以共享同一全视图特征图，因此可以在单次扩散中并行处理**。实验表明（Table 2），分层策略将平均扩散过程从逐物体方法的7.19次降至2.50次（减少65%），而外观保真度FID仅从13.79轻微上升至13.93，证明该策略在几乎不损失质量的前提下大幅提升了效率。这一结果验证了全视图特征图确实能够同时编码多个物体的完整信息，而不会产生物体间的特征干扰。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2406_07706/figures/005_Figure_5.jpg]]
*Figure 5: Illustration of the layer-wise deocclusion strategy. Given an image, we first determine the occlusion relation among the objects using a depth estimation technique. Then, for each depth layer, we deocclude all objects in the same depth layer simultaneously in a unified diffusion pass*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2406_07706/figures/002_Figure_2.jpg]]
*Figure 2: Inpainting models, e.g., SD Inpainting [Rombach et al. 2022], are not ready for the scene deocclusion task, even with the ground-truth amodal mask. The blue arrows mark the object to be deoccluded and the transparent white regions mark the missing areas to inpaint. Left: to inpaint the occluded region, the model can be confused with whether the missing region belongs to the occluder (hockey stick) or the occludee (front bear), failing to complete the target object (hand of front bear). Right: to inpaint regions behind all the occluders after removing them, the model may create unexpected new objects (a new bear) rather than deoccluding the target occludee behind*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2406_07706/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our PACO framework. (a) In the first training stage, we train the Parallel Variational Autoencoder*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2406_07706/figures/004_Figure_4.jpg]]
*Figure 4: Detailed architecture of our visible-to-complete latent generator*

## 实验与关键发现

### 主实验：COCOA 验证集定量对比

PACO 在 COCOA 验证集上对去遮挡任务的两个核心维度——模态完整性（amodal mask IoU）与外观保真度（FID）——均取得显著提升。与主要基线 **SSSD**（Zhan et al., CVPR 2020）相比（Table 1）：

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2406_07706/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison on the COCOA validation set*

| 指标 | PACO | SSSD | 提升 |
|------|------|------|------|
| Amodal Mask IoU | **89.52** | 87.59 | +1.93 |
| FID ↓ | **13.93** | 15.05 | -1.12 |
| 遮挡顺序准确率 | **90.0** | 89.4 | +0.6 |

这三项指标分别衡量：物体被遮挡部分的几何形状恢复精度、生成外观与真实物体的分布距离、以及多物体场景中遮挡关系的推理正确性。PACO 在三个维度上同时超越 SSSD，表明并行 VAE 编码与可见到完整潜在扩散生成器的联合设计，不仅提升了单物体的补全质量，也增强了对场景级遮挡结构的理解能力。

### 分层去遮挡策略的消融

Table 2 对比了两种推理策略：逐物体（One-by-One）去遮挡与分层（Layer-wise）去遮挡。逐物体策略需对每个物体单独执行扩散推理，在 COCOA 验证集上平均扩散过程次数为 7.19 次；分层策略利用深度信息将同层物体并行处理，次数降至 2.50 次，**减少 65% 的扩散推理开销**。FID 仅从 13.79 轻微上升至 13.93（+0.14），外观保真度几乎无损。这一消融直接验证了并行编码器在全视图特征图中同时编码多物体信息的有效性：单次扩散即可为同层多个物体生成完整的潜在特征，解码器再通过交叉注意力按掩码查询恢复各自外观。

### 与修补模型的定性对比

Figure 14 展示了 PACO 与两类修补基线在给定 GT 非模态掩码下的对比：
- **LAMA Inpainting**（Suvorov et al., 2022）：虽能填充区域，但常生成与目标物体身份无关的内容，如错误纹理或模糊结构。
- **Stable Diffusion Inpainting**（Rombach et al., CVPR 2022）：在 Figure 2 中进一步暴露两个典型失败模式：① 当遮挡区域同时涉及遮挡物与被遮挡物时，模型混淆归属，将遮挡物部分错误补全到目标物体上；② 移除所有遮挡物后修补背景区域时，模型可能凭空生成新物体（如新增一只熊），而非恢复被遮挡的目标物体。

PACO 通过类别文本提示与可见到完整潜在生成器的条件控制，避免了上述身份混淆与新物体幻觉问题。Figure 6 的定性对比进一步显示，PACO 补全的物体在纹理延续性、边缘一致性和类别语义保持上均明显优于 SSSD。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2406_07706/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative comparison with SSSD [Zhan et al. 2020]. The arrows indicate the target object to be deoccluded and the completed object parts*

### 跨域泛化与 OOD 场景

PACO 在真实照片、OOD 图像及跨域场景（ADE20k）上均能生成高质量且身份一致的补全结果（Figure 11），表明训练所用的自监督合成数据集（Object Ensemble Dataset）并未导致过拟合于合成分布。并行 VAE 的全视图特征图编码与基于 ControlNet 的扩散生成器，借助预训练 LDM 的先验知识，具备跨域迁移能力。

### 失败模式与适用边界

论文明确指出了以下限制：

1. **阴影处理不足**：物体上的阴影（如滑雪板上的黑色伪影）未得到有效建模，补全结果可能出现光照不一致。
2. **依赖外部标注**：推理流程依赖 SAM 进行实例分割、GPT-4V 获取类别文本提示，限制了全自动化部署。
3. **跨边界物体**：部分超出图像边界的物体难以处理，需额外预处理。
4. **背景补全受限**：背景去遮挡依赖 LAMA 修补模型，其性能上限制约了整体重组质量。
5. **缺乏 3D 感知**：补全后的物体在空间重组时可能出现不合理重叠，因模型未显式建模 3D 几何关系。

### 阶段性能验证

Table 3 在合成验证集上分别评估了阶段一（并行 VAE）与阶段二（可见到完整潜在生成器）的性能。阶段一的并行 VAE 在重建指标上验证了交叉注意力查询机制的有效性——使用可见掩码而非可见图像作为查询，迫使解码器从全视图特征图中提取信息，避免了直接复制可见区域。阶段二的去噪生成器在此基础上进一步提升了补全质量，证实了将去遮挡任务重新表述为条件潜在扩散的有效性。

**需要人工验证的点**：Table 3 的具体数值未在提供的分析中完整给出，建议查阅原文补充阶段一与阶段二在各指标上的绝对数值与相对增益。

## 定位与知识库关联

PACO 的核心定位是将场景去遮挡（scene deocclusion）从**逐物体独立补全**的范式，迁移到**统一潜在空间下的并行条件生成**范式。这一转变对应着方法链中多个关键 slot 的根本性替换，也决定了其与现有知识库的挂载方式。

### 相对于已有方法的本质差异与 slot 变更

**Slot 1：物体编码方式——从独立编码到并行统一编码**

现有去遮挡方法（如 **SSSD**，Zhan et al., CVPR 2020）和修补基线（如 **LAMA**，Suvorov et al., 2022；**Stable Diffusion Inpainting**，Rombach et al., CVPR 2022）均以单个物体为处理单元：要么逐物体进行扩散去遮挡，要么需要已知的非模态掩码（amodal mask）来限定修补区域。这些方法的根本局限在于，它们缺乏对场景中多物体间空间关系和遮挡结构的统一建模能力——修补模型容易混淆遮挡物与被遮挡物的边界（Figure 2 展示了 SD Inpainting 在给定 GT amodal mask 时仍会生成新物体或错误归属遮挡区域）。

PACO 将这一 slot 替换为**并行变分自编码器（Parallel VAE）**：编码器 E1 将场景中所有物体的完整外观堆叠编码为一张统一的全视图特征图（full-view feature map），解码器 D1 通过交叉注意力机制，以各物体的部分可见掩码作为查询，从该统一特征图中选择性提取每个物体的完整特征。这一设计的关键因果机制在于：**统一特征图迫使模型在潜在空间中隐式建模物体间的遮挡关系与空间布局**，而非孤立地处理每个物体。对应的知识库挂载点是“多物体场景的联合潜在表示学习”——这与单物体 VAE（如 VQ-VAE）和多物体检测/分割的融合编码（如 DETR 的 object query）有本质区别，前者关注重建质量，后者关注检测精度，而 PACO 的 Parallel VAE 服务于“从部分观测恢复完整外观”这一生成目标。

**Slot 2：去遮挡推理方式——从逐物体扩散到分层并行扩散**

SSSD 对场景中每个物体独立执行一次扩散去遮挡过程，推理成本随物体数量线性增长。PACO 引入**分层去遮挡策略（Layer-wise Deocclusion）**：利用深度估计确定物体间的遮挡层次，将同一深度的多个物体在一次扩散过程中并行补全。实验表明，这一策略将平均扩散过程次数从 7.19 次降至 2.50 次（减少 65%），而外观保真度（FID）仅从 13.79 轻微上升至 13.93（Table 2）。这一 slot 变更的深层意义在于：**将场景去遮挡的计算复杂度从 O(N) 降至 O(L)，其中 L 为深度层数（通常远小于物体数 N）**，使方法可实际应用于包含多个被遮挡物体的真实场景。

**Slot 3：生成条件——从纯视觉输入到多模态条件引导**

SSSD 仅以可见物体图像作为条件进行去遮挡。PACO 将生成条件扩展为：可见物体图像 + 类别文本提示（由 GPT-4V 获取）+ 边缘图 + 部分掩码。这一变更使得可见到完整潜在生成器（Visible-to-Complete Latent Generator）能够利用预训练基础模型（Stable Diffusion）中的丰富语义先验，从而在物体身份保持和外观生成质量上显著优于纯视觉条件方法。知识库挂载点为“文本引导的图像补全”——但与传统文本引导修补（如 SD Inpainting）不同，PACO 的文本条件作用于**潜在特征图层面**而非像素层面，且与多物体并行编码机制协同工作。

**Slot 4：训练数据——从人工标注到自监督合成**

SSSD 等基线依赖人工标注的非模态掩码进行训练。PACO 构建了**物体集合数据集生成器（Object Ensemble Dataset Generator）**，通过随机叠加 COCO 物体并模拟遮挡关系，自动生成 50 万张包含 2-8 个物体的合成图像，无需任何人工标注。这一自监督数据生成策略使方法摆脱了对昂贵标注的依赖，知识库挂载点为“合成数据驱动的自监督学习”——与域随机化（domain randomization）和程序化场景生成（如 CLEVR）的思路相通，但 PACO 的合成策略专门针对遮挡关系的多样性设计。

### 知识库挂载点与适用边界

PACO 在知识库中的主要挂载点可归纳为：
1. **条件潜在扩散模型**：继承自 Latent Diffusion（Rombach et al., CVPR 2022），但将条件从像素空间移至特征图空间，且条件形式从单一图像/文本扩展为多模态组合。
2. **ControlNet 架构**：可见到完整潜在生成器采用冻结编码器 + 可训练复制编码器（trainable copy encoder）的 ControlNet 式设计，但控制信号从边缘/深度图变为部分视图特征图。
3. **场景去遮挡评估基准**：在 COCOA 数据集上进行评测，与 SSSD、VINV（Zheng et al., IJCV 2021）等共享评估框架。

**适用边界**方面，PACO 存在以下明确限制：
- **依赖外部感知模块**：需要 SAM 提供高质量实例分割、GPT-4V 提供物体类别文本描述，限制了全自动化部署。在分割失败或文本描述不准确的场景下，去遮挡质量会显著下降。
- **跨边界物体处理不足**：当物体部分超出图像边界时，Parallel VAE 的全视图特征图无法完整编码其外观，导致补全失败。
- **全局光照一致性缺失**：物体上的阴影（如滑雪板的黑色伪影）和场景级光照效果未被建模，重组后的场景可能出现视觉不一致。
- **背景去遮挡受限**：背景区域的补全依赖于 LAMA 等修补模型，其性能上限约束了整体场景重建质量。
- **缺乏 3D 感知**：仅依赖 2D 深度分层，无法保证物体在三维空间中的合理布局，可能产生空间冲突。

### 后续启发与开放方向

PACO 为场景去遮挡领域提供了几个关键启发：
1. **统一潜在空间作为多物体信息瓶颈**：Parallel VAE 的设计表明，将多物体信息压缩到统一特征图并通过交叉注意力选择性解码，是处理多物体遮挡场景的有效范式。这一思路可推广至其他需要多物体联合推理的任务（如场景编辑、物体重排）。
2. **分层并行推理的效率优势**：Layer-wise 策略证明了利用深度信息进行推理批量化可大幅提升效率，为实时场景理解应用提供了可行路径。
3. **自监督合成数据的规模化潜力**：Object Ensemble Dataset Generator 表明，通过程序化合成可生成足够多样化的遮挡训练数据，减少对人工标注的依赖。

开放方向包括：如何将 PACO 与 3D 感知模块（如单目深度估计或 NeRF）结合，以解决空间冲突和跨边界物体问题；如何实现端到端的全自动去遮挡，减少对 SAM 和 GPT-4V 的依赖；以及如何将阴影和全局光照一致性纳入生成过程，提升重组场景的真实感。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Object_level_Scene_Deocclusion.pdf]]