---
title: Rethinking the Spatial Inconsistency in Classifier-Free Diffusion Guidance
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Rethinking_the_Spatial_Inconsistency_in_Classifier_Free_Diffusion_Guidance.pdf
project_link: null
code_link: https://github.com/SmilesDZgk/S-CFG
aliases:
- SACFGSC
- RSICFDG
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/benchmarks_datasets_evaluation
core_operator: 各语义区域的自适应CFG尺度，通过归一化分类器得分使不同语义区域的引导强度达到统一水平。
primary_logic: 利用U-net的交叉注意力与自注意力图，可以在去噪过程中对潜在图像进行无训练语义分割，从而为每个语义单元独立定制CFG强度，解决空间不一致问题。
claims:
- 全局CFG尺度造成语义区域间分类器得分显著差异，导致空间质量不一致。
- S-CFG通过自适应尺度将不同语义区域的分类器得分缩放至统一水平，显著减少类间差异。
- S-CFG在FID-30K与CLIP Score的trade-off上全面超越原始CFG，并在人类评估中获得压倒性偏好（图像质量73.22%，图文对齐76.80%）。
- 消融实验表明，自注意力细化和自适应尺度是S-CFG性能提升的关键组件，缺一不可。
---

# Rethinking the Spatial Inconsistency in Classifier-Free Diffusion Guidance

> [!tip] 核心洞察
> 利用U-net的交叉注意力与自注意力图，可以在去噪过程中对潜在图像进行无训练语义分割，从而为每个语义单元独立定制CFG强度，解决空间不一致问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 重新思考无分类器引导扩散中的空间不一致性 |
| 英文题名 | Rethinking the Spatial Inconsistency in Classifier-Free Diffusion Guidance |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2404.05384) · [Code](https://github.com/SmilesDZgk/S-CFG) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/benchmarks_datasets_evaluation |
| Method | Semantic-aware Classifier-Free Guidance (S-CFG) |
| Dataset | MS COCO validation set, Human evaluation, ControlNet tasks, T2I-CompBench |

> [!tip] 效果简介
> - MS COCO validation set 上，FID-30K / CLIP Score S-CFG (SD-v1.5, γ=7.5, DPMSolver++): FID-30K 12.059, CLIP Score 0.3226 vs CFG (SD-v1.5, γ=7.5, DPMSolver++): FID-30K 12.466, CLIP Score 0.3223 (FID降低0.407，CLIP Score提升0.0003)。
> - Human evaluation (side-by-side comparison) 上，Preference rate (%) S-CFG: 图像质量73.22%，图文对齐76.80% (SD-v1.5) vs CFG: 图像质量26.78%，图文对齐23.20% (SD-v1.5) (S-CFG在图像质量上领先46.44%，在图文对齐上领先53.60%)。
> - ControlNet tasks (Canny, HED) 上，FID / CLIP Score S-CFG: Canny FID 8.382, CLIP 0.3019 vs CFG: Canny FID 8.670, CLIP 0.3006 (FID降低0.288，CLIP提升0.0013)。

## 概要

**问题瓶颈**：标准无分类器引导（CFG）在扩散模型生成中采用全局统一的引导尺度，导致不同语义区域接收到的分类器得分强度存在显著差异——语义简单的区域（如背景）往往被过度引导，而语义复杂的区域（如前景主体）引导不足。这种空间不一致性最终表现为生成图像中不同语义单元的质量不均，部分区域纹理过饱和或细节缺失。

**核心方法**：本文提出**语义感知的无分类器引导（Semantic-aware Classifier-Free Guidance, S-CFG）**，在不引入额外训练的前提下，通过挖掘U-net去噪骨干网络中的交叉注意力与自注意力图，实现对潜在图像的语义分割，并为每个语义单元独立定制自适应的CFG尺度，从而将不同区域的分类器得分范数缩放至统一水平，消除空间引导强度的不一致。

**方法定位**：S-CFG属于扩散模型推理阶段的引导策略改进，不修改模型权重，不增加训练开销。其语义分割模块完全依赖预训练U-net内部已有的注意力表示，通过交叉注意力空间重归一化与自注意力迭代细化完成掩码提取；自适应尺度模块则基于各语义区域分类器得分范数与基准区域的比值动态计算逐像素引导强度。该方法可即插即用于Stable Diffusion、DeepFloyd IF等主流文生图模型，并与ControlNet、DreamBooth等下游应用兼容。

**主要结果**：
- 在MS COCO验证集上，S-CFG（SD-v1.5, γ=7.5, DPMSolver++）的FID-30K降至12.059，CLIP Score提升至0.3226，在FID-CLIP权衡曲线上全面优于原始CFG。
- 人类评估中，S-CFG在图像质量维度获得73.22%的偏好率，在图文对齐维度获得76.80%的偏好率，分别领先CFG 46.44和53.60个百分点。
- 消融实验证实，自注意力细化与自适应尺度缩放是性能提升的两个关键组件，缺一不可。
- 推理时间仅增加约2%，几乎不影响生成效率。



扩散模型已成为文本到图像生成的主流范式，其核心优势之一在于**无分类器引导（Classifier-Free Guidance, CFG）**机制——通过一个全局统一的引导尺度 $\gamma$ 融合条件与无条件扩散得分，显著提升生成样本的质量与文本对齐度。然而，这一看似简洁有效的策略背后隐藏着一个被长期忽视的深层问题：**空间不一致性**。

### 全局统一尺度的隐性代价

在标准 CFG 框架中，组合扩散得分由下式给出：

$$\hat{\epsilon}_\theta(x_t, c, t) = \epsilon_\theta(x_t, t) + \gamma (\epsilon_\theta(x_t, c, t) - \epsilon_\theta(x_t, t))$$

其中 $\gamma$ 是一个全局固定的标量。这意味着无论图像中的语义单元是前景主体还是背景区域，它们都接收完全相同强度的引导信号。问题的根源在于：不同语义区域对引导的“响应程度”存在天然差异。分类器得分 $\nabla_{x_t} \log p(c|x_t)$（即条件与无条件得分之差）在不同语义区域的范数可以相差数倍——前景区域（如“宇航员”）通常具有较大的分类器得分范数，而背景区域（如“天空”）的范数则小得多。这种差异直接导致：**在相同的全局 $\gamma$ 下，不同语义区域实际接收到的引导强度严重失衡**，最终表现为生成图像中前景过饱和、背景欠细化等空间质量不均的现象。

Figure 1 清晰地揭示了这一机制：左侧 CFG 生成的“宇航员骑马”图像中，不同语义区域（地面、天空、马、宇航员）的分类器得分范数曲线存在显著差异；而右侧 S-CFG 通过自适应尺度将这些曲线调整至统一水平，图像的细节质量和空间一致性得到明显改善。

### 现有方法的缺口

在 S-CFG 提出之前，已有工作从不同角度尝试解决扩散生成中的控制问题：

- **注意力操控**：通过修改交叉注意力图来强化特定 token 的响应，但这类方法侧重于语义绑定而非空间质量均衡。
- **区域引导**：部分方法允许用户指定区域掩码进行局部控制，但需要额外输入且不具备自动语义感知能力。
- **多阶段细化**：利用多个扩散阶段逐步改善细节，但计算开销大且未从根本上解决空间不一致。

上述方法的共同局限在于：它们要么**无法自动感知图像的语义结构**，要么**缺乏对不同语义区域引导强度的差异化调节机制**。核心瓶颈可以归纳为：**如何在无需训练、无需外部监督的条件下，对潜在图像进行语义分割，并为每个语义单元定制合适的引导强度？**

### 本文动机与核心洞察

本文的核心洞察在于：**U-net 去噪骨干网络中的交叉注意力与自注意力图，天然蕴含了丰富的语义信息，可以作为训练无关的语义分割依据**。具体而言：

1. **交叉注意力图**揭示了每个图像 patch 与文本 token 之间的对应关系，通过空间重归一化可以将每个 patch 分配给注意力最强的 token，形成初始语义掩码。
2. **自注意力图**反映了图像 patch 之间的结构相似性，可用于对初始掩码进行迭代传播与细化，填补空洞并完善边界。
3. 基于上述语义分割结果，可以**计算每个语义区域的分类器得分范数，并据此动态缩放 CFG 尺度**，使所有区域接收到统一水平的引导强度。

这一设计将空间不一致问题转化为一个**可微、可嵌入去噪循环的语义感知引导框架**，无需额外训练或标注数据，仅利用 U-net 前向传播中已有的注意力图即可实现。由此诞生的 **Semantic-aware Classifier-Free Guidance (S-CFG)** 方法，从根本上重新思考了 CFG 的空间公平性问题，为扩散模型的高质量生成提供了新的控制维度。



## 核心方法与创新机理

### 问题诊断：全局CFG尺度的空间不一致性

标准无分类器引导（CFG）采用全局统一的引导尺度 $\gamma$ 作用于整幅图像，其组合扩散得分定义为：

$$\hat{\epsilon}_\theta(x_t, c, t) = \epsilon_\theta(x_t, t) + \gamma (\epsilon_\theta(x_t, c, t) - \epsilon_\theta(x_t, t))$$

然而，这一全局策略隐含假设所有语义区域对引导的需求强度相同。本文通过分析去噪过程中各语义区域的**分类器得分范数**（classifier score norm，即条件与无条件预测之差 $\eta_t = \epsilon_\theta(x_t, c, t) - \epsilon_\theta(x_t, t)$ 的范数），揭示了一个关键瓶颈：**不同语义区域的分类器得分范数存在显著差异**，导致某些区域被过度引导（产生伪影或纹理过饱和），而另一些区域引导不足（细节模糊、语义丢失）。如 Figure 1 所示，在提示词“a photo of an astronaut riding a horse”的生成过程中，CFG 生成的图像中“马”和“宇航员”区域的分类器得分范数远高于“天空”和“地面”区域，这种空间不均衡直接反映为生成质量的空间不一致——前景主体与背景之间存在明显的质量断层。

### 核心洞察：语义级自适应引导

针对上述瓶颈，本文的核心创新在于将 CFG 的引导尺度从**全局统一**转变为**语义级自适应**。其因果机制可概括为：

> **利用 U-net 预训练注意力图实现训练无关的语义分割，进而为每个语义单元独立计算自适应 CFG 尺度，将不同区域的分类器得分范数缩放至统一水平，消除空间不一致。**

这一设计的理论依据是：若能将各语义区域的分类器得分范数归一化到相同的基准水平，则每个区域接收到的引导强度将趋于均衡，从而在保持全局引导效果的同时，避免局部过引导或欠引导。

### Changed Slots：两个关键维度的创新

相较于标准 CFG，S-CFG 在两个核心“插槽”上进行了系统性改造：

| 插槽 | 基线（CFG） | S-CFG 方案 | 证据锚点 |
|------|------------|-----------|---------|
| **引导尺度** | 全局单一固定值 $\gamma$ | 各语义区域自适应计算的 $\gamma_{t,i}$，基于分类器得分范数动态缩放 | Equation 13; Section 4.2.1 |
| **语义分割** | 无（整幅图像统一处理） | 基于交叉注意力重归一化与自注意力完成的训练无关语义分割 | Section 4.1; Equation 9 |

#### 创新点一：训练无关的潜在图像语义分割

S-CFG 不依赖任何额外训练或外部分割模型，而是直接利用扩散模型 U-net 中已有的注意力图完成语义分割。具体流程包括两个步骤：

1. **交叉注意力重归一化**：对 U-net 第 $k$ 层的交叉注意力图 $C_t^k$ 进行空间维度重归一化，消除不同 token 间的尺度偏差，并将每个 patch 分配给注意力最大值对应的 token，得到初始语义掩码：
   $$\hat{C}_t[s,i] = \frac{C_t[s,i]}{\sum_{s'=1}^{HW} C_t[s',i]}, \quad i_s = \arg\max_i \hat{C}_t[s,i]$$

2. **自注意力细化**：由于交叉注意力图通常存在空洞和边界模糊问题，S-CFG 利用自注意力转移矩阵的幂迭代对交叉注意力掩码进行传播和平滑：
   $$\overline{C}_t^k = \frac{1}{R} \sum_{r=1}^R (S_t^k)^r C_t^k$$
   这一操作利用自注意力图中像素间的亲和关系，将语义信息从高置信度区域传播至邻域，有效填补空洞并完善边界（如 Figure 3 所示，加入自注意力细化后分割质量显著提升）。

#### 创新点二：自适应 CFG 尺度计算

在获得各语义区域的掩码 $m_{t,i}$ 后，S-CFG 的关键创新在于为每个语义单元计算独立的引导尺度，而非使用全局统一值。S-CFG 的组合扩散得分定义为：

$$\hat{\epsilon}_\theta(x_t, c, t) = \epsilon_\theta(x_t, t) + \sum_{i=1}^M \gamma_{t,i} m_{t,i} \odot (\epsilon_\theta(x_t, c, t) - \epsilon_\theta(x_t, t))$$

其中自适应尺度 $\gamma_{t,i}$ 的计算公式为：

$$\gamma_{t,i} = \gamma \frac{|m_{t,b} \odot \eta_t|}{|m_{t,i} \odot \eta_t|} \frac{|m_{t,i}|}{|m_{t,b}|}$$

该公式的设计逻辑是：选定一个基准区域 $b$（通常为前景，通过 `<START>` token 定义），计算其分类器得分范数 $|m_{t,b} \odot \eta_t|$ 作为参考水平。对于任意语义区域 $i$，将其分类器得分范数缩放至与基准区域一致，从而保证所有区域接收到的引导强度处于统一水平。因子 $\frac{|m_{t,i}|}{|m_{t,b}|}$ 用于补偿不同区域面积差异带来的范数偏差。

### 创新性验证：消融实验的关键证据

消融实验（Figure 6, Table 8）严格验证了两个创新组件的必要性：

- **去除自注意力细化（S-CFG w/o sa）** 导致 FID-30K 从 12.059 上升至 12.102，CLIP Score 从 0.3226 下降至 0.3222（$\gamma=7.5$），证实了自注意力传播对语义分割质量的关键作用。
- **将自适应尺度替换为简单均值归一化（S-CFG-mean）** 造成更严重的性能退化（FID 11.204, CLIP 0.3213），证明了基于分类器得分范数的自适应缩放策略不可替代。

### 方法谱系与知识库定位

S-CFG 属于**推理时引导策略优化**的研究脉络，与以下工作形成差异化的技术定位：

- 相较于标准 **CFG**（Ho & Salimans, NeurIPS 2021）的全局统一尺度，S-CFG 首次从语义空间一致性角度提出自适应引导，填补了该方向的方法空白。
- 与基于交叉注意力控制生成布局的方法（如 **Prompt-to-Prompt** 等）不同，S-CFG 不修改注意力图本身，而是利用注意力图作为语义分割的信号源，进而调控引导强度，保持了生成过程的完整性。
- 相较于需要额外训练或微调的引导策略（如 **Dynamic CFG** 等），S-CFG 完全训练无关，可直接应用于任意预训练扩散模型，具有即插即用的优势。



S-CFG 的核心设计动机源于对标准无分类器引导（CFG）中**空间不一致性**的揭示：全局统一的 CFG scale $γ$ 导致不同语义区域所接收的引导强度存在显著差异，最终使生成图像中不同语义单元的质量参差不齐（见 Figure 1）。为从根本上解决这一问题，S-CFG 提出了一条完整的语义感知引导管线，其核心思想是：在去噪过程的每一步，对潜在图像进行**无训练的语义分割**，进而为每个语义单元**独立定制自适应 CFG 尺度**，使各区域的分类器得分范数被缩放至统一水平。

### 管线总览

S-CFG 的整体框架如 Figure 2 所示，由四个紧密衔接的模块构成：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of our S-CFG method. At each denoising step in diffusion models, the U-net backbone estimates both diffusion score*

1. **U‑net 主干与注意力提取**：在每个去噪步 $t$，U‑net 同时接收纯噪声输入和文本条件输入，分别估计无条件扩散得分 $ε_θ(x_t, t)$ 和条件扩散得分 $ε_θ(x_t, c, t)$，二者的差值即为分类器得分 $η_t = ε_θ(x_t, c, t) - ε_θ(x_t, t)$。与此同时，U‑net 内部的自注意力层和交叉注意力层分别输出自注意力图 $S_t^k$ 和交叉注意力图 $C_t^k$，为后续语义分割提供空间线索。

2. **基于交叉注意力的语义分割**：对交叉注意力图 $C_t$ 进行空间维度的重归一化，将每个 patch 分配给注意力最大值对应的文本 token，得到初始语义掩码 $\{m_{t,i}\}_{i=1}^{M}$。这一过程完全训练无关，仅依赖 U‑net 已有的注意力表示。

3. **自注意力细化**：利用自注意力图 $S_t^k$ 的转移特性对交叉注意力掩码进行迭代传播（$\overline{C}_t^k = \frac{1}{R} \sum_{r=1}^R (S_t^k)^r C_t^k$），有效填补语义区域内的空洞并完善边界，显著提升分割质量（消融实验中去除该步骤导致 FID 上升和 CLIP Score 下降，验证了其关键作用）。

4. **自适应 CFG scale map 计算与组合得分**：以选定的基准区域（通常为前景）的分类器得分范数为参考，通过 $\gamma_{t,i} = \gamma \frac{|m_{t,b} \odot \eta_t|}{|m_{t,i} \odot \eta_t|} \frac{|m_{t,i}|}{|m_{t,b}|}$ 为每个语义单元动态计算自适应尺度 $\gamma_{t,i}$，并组合成空间变化的 scale map。最终，S-CFG 的组合扩散得分为：

$$\hat{\epsilon}_{\theta}(x_t, c, t) = \epsilon_{\theta}(x_t, t) + \sum_{i=1}^{M} \gamma_{t,i} m_{t,i} \odot (\epsilon_{\theta}(x_t, c, t) - \epsilon_{\theta}(x_t, t))$$

该公式将全局统一的引导信号替换为逐语义区域加权求和的形式，使前景与背景等不同语义单元获得均衡的引导强度。

### 关键设计决策

- **语义单元的独立性假设**：S-CFG 将图像视为若干相对独立语义单元的集合，允许为每个单元独立定制 CFG 尺度。原文指出该假设在实践中可能不完全严格成立，但实验表明其足以支撑显著的质量改善。
- **基准区域选择**：自适应尺度的归一化基准固定选为由 `<START>` token 定义的前景区域。对于多主体或无明显前景的复杂构图，该策略可能不够灵活，构成方法的一个已知局限。
- **计算开销**：S-CFG 仅需从 U‑net 的现有注意力层中提取特征并进行轻量级后处理，推理时间增加约 2%（Table 3），在不显著牺牲效率的前提下实现了空间一致性的本质提升。



S-CFG 的核心由两个紧密耦合的模块构成：**训练无关的语义分割**（Section 4.1）与**自适应 CFG 尺度计算**（Section 4.2）。前者从 U-net 的注意力图中提取各语义单元的掩码，后者为每个语义区域定制独立的引导强度，二者共同实现空间一致的无分类器引导。

### 4.1 基于注意力的语义分割

标准 CFG 使用全局统一的引导尺度 $\gamma$，其组合扩散得分（Equation 7）为：

$$\hat{\epsilon}_\theta(x_t, c, t) = \epsilon_\theta(x_t, t) + \gamma (\epsilon_\theta(x_t, c, t) - \epsilon_\theta(x_t, t))$$

该公式中条件得分与无条件得分的差值（即分类器得分）对所有像素施加相同权重，忽略了不同语义单元对引导强度需求的差异。S-CFG 的核心思路是将该差值按语义区域拆解，为每个区域分配独立的 $\gamma_{t,i}$。

#### 4.1.1 交叉注意力重归一化

U-net 的交叉注意力层在去噪过程中建立了文本 token 与图像 patch 之间的对应关系。对于第 $k$ 层，自注意力图 $S_t^k$ 和交叉注意力图 $C_t^k$ 分别由以下形式计算：

$$S_t^k = \mathrm{Softmax}\left(\frac{Q_s(z_t^k) K_s(z_t^k)^T}{\sqrt{d}}\right), \quad C_t^k = \mathrm{Softmax}\left(\frac{Q_c(z_t^k) K_c(e)^T}{\sqrt{d}}\right)$$

其中 $z_t^k$ 为图像特征，$e$ 为文本嵌入。直接使用 $C_t^k$ 进行语义分割存在空间偏置问题——某些 token 的注意力值天然偏低，导致对应区域被淹没。为此，S-CFG 对交叉注意力进行空间维度重归一化：

$$\hat{C}_t[s,i] = \frac{C_t[s,i]}{\sum_{s'=1}^{HW} C_t[s',i]}, \quad i_s = \arg\max_i \hat{C}_t[s,i]$$

其中 $s$ 为空间位置索引，$i$ 为 token 索引，$HW$ 为总 patch 数。重归一化后，每个 patch 被分配给 $\hat{C}_t$ 中最大值对应的 token，形成初始语义掩码。该操作消除了不同 token 注意力幅值的天然差异，使各语义单元在分割中处于公平地位。

#### 4.1.2 自注意力细化

仅依赖交叉注意力的分割结果存在空洞和边界模糊问题——交叉注意力倾向于聚焦于语义区域的中心，边缘响应较弱。S-CFG 利用自注意力图的传播特性进行修复：自注意力 $S_t^k$ 编码了 patch 间的特征相似性，可通过幂迭代将高响应区域的信号传播至相邻低响应区域。细化后的交叉注意力为：

$$\overline{C}_t^k = \frac{1}{R} \sum_{r=1}^R (S_t^k)^r C_t^k$$

其中 $R$ 为迭代次数。$(S_t^k)^r$ 作为转移矩阵，将 $C_t^k$ 中每个 token 的注意力值沿特征相似路径扩散，填补语义区域内部的空洞并平滑边界。Figure 3 展示了不同去噪步骤下，纯交叉注意力分割与加入自注意力细化后的对比，后者显著改善了语义掩码的完整性和边界准确性。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/003_Figure_3.jpg]]
*Figure 3: The latent image segmentation based on attention maps at different denoising steps. The first column shows the predicted image*

### 4.2 语义感知的无分类器引导

#### 4.2.1 自适应尺度计算

S-CFG 的核心创新在于为每个语义单元 $i$ 计算自适应 CFG 尺度 $\gamma_{t,i}$，使得不同区域的分类器得分范数达到统一水平。给定语义掩码 $m_{t,i} \in \{0,1\}^{HW}$ 和分类器得分 $\eta_t = \epsilon_\theta(x_t, c, t) - \epsilon_\theta(x_t, t)$，自适应尺度定义为：

$$\gamma_{t,i} = \gamma \frac{|m_{t,b} \odot \eta_t|}{|m_{t,i} \odot \eta_t|} \frac{|m_{t,i}|}{|m_{t,b}|}$$

其中 $m_{t,b}$ 为基准区域掩码（通常选前景区域，通过 `<START>` token 对应区域检测），$|\cdot|$ 表示逐元素乘积后的 $\ell_2$ 范数。该公式的分子 $|m_{t,b} \odot \eta_t|$ 为基准区域的分类器得分范数，分母 $|m_{t,i} \odot \eta_t|$ 为目标区域的分类器得分范数；比值 $\frac{|m_{t,i}|}{|m_{t,b}|}$ 为面积归一化因子，消除区域大小对范数的影响。整体效果是：若某语义区域的分类器得分天然偏低，则 $\gamma_{t,i}$ 被放大，使其引导强度与基准区域对齐；反之亦然。

#### 4.2.2 组合扩散得分

将自适应尺度与语义掩码结合，S-CFG 的最终扩散得分由各语义区域的加权和构成：

$$\hat{\epsilon}_\theta(x_t, c, t) = \epsilon_\theta(x_t, t) + \sum_{i=1}^M \gamma_{t,i} m_{t,i} \odot (\epsilon_\theta(x_t, c, t) - \epsilon_\theta(x_t, t))$$

其中 $M$ 为语义单元数量，$\odot$ 表示逐元素乘法。与原始 CFG 的全局单一尺度相比，该公式将分类器得分按语义区域拆解，每个区域接受独立的自适应引导。Figure 1 的动机示例直观展示了这一机制的效果：CFG 生成图像中不同语义区域的分类器得分范数存在显著差异（曲线高度不一），而 S-CFG 通过自适应缩放将这些曲线拉至统一水平，消除了空间不一致性。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/001_Figure_1.jpg]]
*Figure 1: A motivation example. The first line shows images generated by Stable Diffusion with CFG and S-CFG, where the prompt is*

### 关键公式汇总

| 公式 | 变量含义 | 作用 |
|------|----------|------|
| $\hat{C}_t[s,i] = \frac{C_t[s,i]}{\sum_{s'} C_t[s',i]}$ | $C_t$：交叉注意力图；$s$：空间位置；$i$：token 索引 | 空间重归一化，消除 token 间注意力幅值偏差 |
| $\overline{C}_t^k = \frac{1}{R} \sum_{r=1}^R (S_t^k)^r C_t^k$ | $S_t^k$：自注意力图；$R$：迭代次数 | 利用自注意力传播填补语义区域空洞 |
| $\gamma_{t,i} = \gamma \frac{\|m_{t,b} \odot \eta_t\|}{\|m_{t,i} \odot \eta_t\|} \frac{\|m_{t,i}\|}{\|m_{t,b}\|}$ | $\eta_t$：分类器得分；$m_{t,b}$：基准区域掩码；$m_{t,i}$：目标区域掩码 | 按基准区域范数缩放，实现各语义单元引导强度统一 |
| $\hat{\epsilon}_\theta = \epsilon_\theta + \sum_{i=1}^M \gamma_{t,i} m_{t,i} \odot \eta_t$ | $\gamma_{t,i}$：自适应尺度；$m_{t,i}$：语义掩码；$\eta_t$：分类器得分 | 语义感知的扩散得分组合，替代全局 CFG |

整个流程如 Figure 2 所示：在每个去噪步骤，U-net 骨干网络同时估计扩散得分和条件扩散得分，提取自注意力图与交叉注意力图；交叉注意力经重归一化后产生初始语义分割，自注意力对其进行细化；随后基于各区域分类器得分范数计算自适应 CFG 尺度，最终组合成语义感知的引导信号。所有操作均在去噪过程中在线完成，无需额外训练。



## 实验与关键发现

### 主实验结果

S-CFG在MS COCO验证集上进行了系统的FID-30K与CLIP Score权衡评估。以SD-v1.5为基模型、DPMSolver++采样器（50步）、γ=7.5的设置下，S-CFG取得FID-30K 12.059、CLIP Score 0.3226，相比标准CFG的FID 12.466、CLIP 0.3223，FID降低0.407，CLIP Score提升0.0003（Table 5）。Figure 4展示了三种基模型（SD-v1.5、SD-v2.1、DeepFloyd IF）上的完整权衡曲线，S-CFG的曲线在所有γ取值下均位于CFG曲线的右下方区域，表明方法在保真度与图文对齐的权衡上具有一致优势。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/014_Table_5.jpg]]
*Table 5: The trade-off curve of SD-v1.5, where the best FID-30k and CLIP Score are highlighted*

人类主观评测进一步验证了S-CFG的感知质量优势。双盲投票结果显示，在SD-v1.5基模型上，S-CFG以73.22%对26.78%的压倒性优势胜出图像质量维度，以76.80%对23.20%胜出图文对齐维度（Table 1）。该趋势在SD-v2.1和DeepFloyd IF上同样成立，表明跨架构的鲁棒性。

在可控生成任务中，S-CFG同样有效。以ControlNet的Canny边缘条件为例，S-CFG取得FID 8.382、CLIP Score 0.3019，优于CFG的FID 8.670、CLIP 0.3006（Table 2）。HED条件下的趋势一致。T2I-CompBench的细粒度评估显示，S-CFG在属性绑定、对象关系等子任务上全面超越CFG：以SD-v2.1为例，Color得分从0.549提升至0.5649，Texture从0.5146提升至0.5333，Spatial从0.1512提升至0.1567（Table 4）。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/008_Table_2.jpg]]
*Table 2: Performance comparisons of ControlNet with CFG and S-CFG, where the base model is SD-v1.5, the parameter γ = 3.0 and that sampler is DPMSolver++ with 50 steps*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/012_Table_4.jpg]]
*Table 4: Evaluation on T2I-CompBench, where the γ = 7.5*

### 消融实验

为厘清各组件的贡献，作者设计了系统的消融研究（Figure 6, Table 8）。所有消融实验基于SD-v1.5、DPMSolver++采样器、50步设置。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/005_Figure_6.jpg]]
*Figure 6: The ablation analysis by evaluating the performance of different components in S-CFG*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/017_Table_8.jpg]]
*Table 8: The trade-off curve in the ablation analysis , where the best FID-30k and CLIP Score are highlighted. The experiment is based on SD-v1.5 with 50-step DPMSolver++ Sampler*

**自注意力细化的作用**：移除自注意力细化步骤（S-CFG w/o sa）后，在γ=7.5时FID-30K从12.059升至12.102，CLIP Score从0.3226降至0.3222。该退化表明，仅靠交叉注意力得到的语义分割存在空洞和边界模糊问题，自注意力的信息传播对完善语义区域至关重要。

**自适应尺度的有效性**：将自适应尺度替换为简单均值归一化策略（S-CFG-mean）造成更显著的性能退化。在γ=7.5时，S-CFG-mean的FID-30K为11.204、CLIP Score为0.3213，两项指标均劣于完整S-CFG。该结果验证了基于分类器得分范数的动态缩放策略的有效性——简单均值归一化无法充分弥合不同语义区域间引导强度的差异。

**多阶段模型的应用策略**：在DeepFloyd IF这类多阶段扩散模型中，消融实验表明同时在两个阶段应用S-CFG达到最佳FID-CLIP权衡（Figure 10），仅在第一阶段或第二阶段单独使用均无法达到同等效果。

### 效率分析

S-CFG引入的计算开销极低。在A100 GPU上，三种基模型下S-CFG相比CFG的每样本平均推理时间增加均不超过3%（Table 3）。该效率优势源于语义分割和自适应尺度计算完全复用U-net已有的注意力图，无需额外网络前传或训练。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/011_Table_3.jpg]]
*Table 3: The analysis on the time cost*

### 定性分析

Figure 5并列展示了三种基模型在相同提示词下使用CFG与S-CFG的生成样本。S-CFG生成的图像在细节纹理和不同语义区域的质量均匀性上表现更优，尤其在包含多个实体的复杂场景中，S-CFG有效缓解了CFG常见的部分区域过曝或欠细节问题。Figure 3展示了不同去噪步骤下潜在图像的语义分割效果：纯交叉注意力分割存在明显的碎片化和空洞，加入自注意力细化后分割区域变得连续完整，为后续自适应引导奠定了可靠基础。

### 公平性说明

所有对比实验均在严格控制下进行：使用相同的采样器（DDIM或DPMSolver++）和步数（50步），在MS COCO验证集上计算标准化指标FID-30K和CLIP Score。方法在三种不同架构的扩散模型上进行了跨模型验证。人类评估采用多名标注者双盲投票，覆盖图像质量和图文对齐两个独立维度。消融研究中所有变体在相同超参数设置下比较。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/004_Figure_4.jpg]]
*Figure 4: The qualitative evaluation results on the trade-off curve of FID-30K VS CLIP Score*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/013_Figure_10.jpg]]
*Figure 10: The ablation analysis of the S-CFG on the diffusion model with multiple stages*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2404_05384/figures/010_Figure_9.jpg]]
*Figure 9: The trade-off curve of FID-10K VS CLIP Score with DDIM sampler*



## 定位与知识库关联

### 1. 问题定位：从全局引导到空间自适应引导

**S-CFG** 的核心动机源于对标准 **Classifier-Free Guidance (CFG)** 空间行为的重新审视。CFG 通过全局统一的尺度 $\gamma$ 融合条件与无条件扩散得分：

$$\hat{\epsilon}_\theta(x_t, c, t) = \epsilon_\theta(x_t, t) + \gamma (\epsilon_\theta(x_t, c, t) - \epsilon_\theta(x_t, t))$$

这一范式隐式假设所有语义单元对引导强度的需求是均质的。然而，本文通过分析扩散过程中各语义区域的分类器得分范数 $\|\nabla_{x_t} \log p(c|x_t)\|$，揭示了一个此前未被系统量化的瓶颈：**不同语义区域（如“宇航员”与“天空”）的分类器得分范数存在显著差异**，导致全局统一的 $\gamma$ 实质上对不同区域施加了不均衡的引导强度，最终造成生成图像中不同语义单元的质量空间不均（Figure 1）。

这一发现将 CFG 的改进方向从“如何选择最优 $\gamma$”推进到“如何为不同语义单元定制 $\gamma$”，属于扩散模型引导策略中**从全局标量控制到空间自适应控制**的范式转换。

### 2. 方法谱系中的坐标

#### 2.1 与注意力引导方法的关系

利用 U-net 交叉注意力图进行图像编辑或布局控制是扩散模型领域的活跃方向。**Prompt-to-Prompt** (Hertz et al., ICLR 2023) 通过操纵交叉注意力图实现文本驱动的图像编辑，**Attend-and-Excite** (Chefer et al., ICCV 2023) 使用注意力图增强被忽略的文本 token 的激活。这些方法证明了交叉注意力图携带了可靠的语义定位信息。

S-CFG 继承了这一洞察，但将其用于一个不同的问题：**不是编辑或属性绑定，而是去噪过程中引导强度的空间均衡化**。具体而言，S-CFG 对交叉注意力图进行空间重归一化：

$$\hat{C}_t[s,i] = \frac{C_t[s,i]}{\sum_{s'=1}^{HW} C_t[s',i]}, \quad i_s = \arg\max_i \hat{C}_t[s,i]$$

并进一步利用自注意力转移矩阵的幂迭代进行语义区域细化：

$$\overline{C}_t^k = \frac{1}{R} \sum_{r=1}^R (S_t^k)^r C_t^k$$

这种“交叉注意力定位 + 自注意力补全”的策略，使得 S-CFG 无需任何训练即可在去噪过程中对潜在图像进行语义分割（Figure 3），这是其区别于依赖外部分割模型或固定布局先验的方法的关键所在。

#### 2.2 与自适应采样方法的关系

在扩散模型的采样效率方面，**DPM-Solver++** 等先进 ODE 求解器通过改进数值积分策略减少采样步数，但未涉及引导强度的空间分配问题。S-CFG 与这些方法正交：它修改的是引导信号的组合方式，而非采样器的步进策略。实验表明 S-CFG 在 DDIM 和 DPMSolver++ 两种采样器下均带来一致的性能提升（Figure 4, Figure 9），验证了这种正交性。

#### 2.3 与多阶段扩散模型的关系

**DeepFloyd IF** 等级联扩散模型在多个分辨率阶段进行去噪。S-CFG 的消融实验（Figure 10）表明，在两个阶段同时应用 S-CFG 达到最佳的 FID-CLIP Score trade-off，说明空间不一致性在级联模型的各个阶段均存在，且 S-CFG 的语义分割机制在不同分辨率的潜在空间上均有效。

### 3. 适用边界与关键约束

#### 3.1 语义分割对注意力质量的依赖

S-CFG 的语义分割完全依赖 U-net 的交叉注意力与自注意力图，这一训练无关（training-free）特性既是其优势也是其约束。在去噪早期步骤（$t$ 较大），潜在图像仍高度噪声化，注意力图可能未充分收敛，导致分割精度下降（Figure 3 中早期步骤的分割图存在明显噪声）。因此，**S-CFG 在去噪中后期的作用更为可靠**，而在初始步骤中其引导可能引入额外的不确定性。

#### 3.2 语义单元独立性假设

S-CFG 将图像分解为 $M$ 个相对独立的语义单元，并为每个单元分配独立的 $\gamma_{t,i}$。这一独立性假设在实践中可能不完全成立——原文明确指出“the prior assumption may not be strict in practice”。当语义单元之间存在遮挡、透明或强交互关系时，分割边界可能模糊，导致引导信号在边界处出现不连续或错误分配。

#### 3.3 基准区域选择的固定性

自适应尺度的计算依赖于一个基准区域 $b$（通常选为前景，通过 `<START>` token 定义）：

$$\gamma_{t,i} = \gamma \frac{|m_{t,b} \odot \eta_t|}{|m_{t,i} \odot \eta_t|} \frac{|m_{t,i}|}{|m_{t,b}|}$$

这一设计假设前景是引导强度的合理基准。对于没有明确前景或包含多个同等重要主体的复杂构图，固定选择前景作为基准可能不是最优的。例如，在“a cat and a dog playing in the garden”这类提示中，“cat”和“dog”同为前景主体，将其中一个设为基准可能导致另一个的引导强度被不适当地缩放。

#### 3.4 计算开销的边界

尽管 S-CFG 仅引入约 2% 的额外推理时间（Table 3），这在大多数离线生成场景中可忽略不计，但对于实时交互式生成或大规模批量推理，这一开销仍需纳入考量。额外开销主要来自注意力图的提取与自注意力细化中的矩阵乘法。

### 4. 局限性与开放问题

#### 4.1 已识别的局限

1. **语义分割精度上限**：S-CFG 的分割质量受限于基模型 U-net 注意力图的固有质量。若基模型本身对某些 token 的注意力发散或存在大量噪声，S-CFG 无法纠正这些底层缺陷，只能在其基础上进行引导强度的调整。

2. **自动指标的充分性**：FID 和 CLIP Score 等标准指标能否充分反映空间一致性的改善，仍是一个开放问题。消融实验中 S-CFG 相比 S-CFG-sa 的提升在数值上较小（FID 12.102 vs 12.059, CLIP 0.3222 vs 0.3226），但人类评估显示出显著偏好（图像质量 73.22% vs 26.78%），暗示现有自动指标可能低估了空间一致性改善的感知收益。

3. **基模型质量的影响**：实验显示 SD-v2.1 在本文的 MS COCO FID-30K 设置下未能明显优于 SD-v1.5，而 S-CFG 的提升幅度在不同基模型上存在差异。这表明 S-CFG 的收益可能受基模型质量的影响，但其间的因果关系尚未被系统分析。

#### 4.2 开放问题

1. **独立性假设的放宽**：在交叉实体复杂的场景（如遮挡、透明物体、反射）中，语义单元的独立性假设如何放宽？是否可以通过引入图结构或软分割（soft mask）来建模语义单元间的依赖关系？

2. **基准区域的自动选择**：能否根据图像内容自动选择或学习最优的基准区域，而非固定为前景？例如，选择分类器得分范数最稳定的区域作为基准，或通过多基准区域的加权组合来提升鲁棒性。

3. **与蒸馏模型的协同**：S-CFG 的自适应机制能否与蒸馏模型（如 **LCM**）或一致性模型进一步协同优化，在降低采样步数的同时保持空间一致性？这需要验证在极少步数（如 1-4 步）下注意力图是否仍能提供可靠的语义分割。

4. **空间公平性的专用度量**：当前领域缺乏专门评估空间一致性的定量指标。设计能够直接度量不同语义区域生成质量均衡性的指标（如区域级 FID 的方差），将是推动该方向发展的关键。

5. **与其他引导策略的融合**：S-CFG 的空间自适应思想是否可以与 **Perturbed Attention Guidance (PAG)** 等基于注意力扰动的引导方法融合，在空间均衡化的同时进一步增强细节保真度？



## 原文 PDF

![[paperPDFs/CVPR_2024/Rethinking_the_Spatial_Inconsistency_in_Classifier_Free_Diffusion_Guidance.pdf]]
