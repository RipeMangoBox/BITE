---
title: "VINS-120K: Ultra High-Resolution Image Editing with A Large-Scale Dataset"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VINS_120K_Ultra_High_Resolution_Image_Editing_with_A_Large_Scale_Dataset.pdf
project_link: null
code_link: "https://github.com/Breakthrough/PySceneDetect"
aliases:
- HFAPA
- VINS-120K
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入分辨率感知的注意力温度缩放、RoPE 位置编码基数重缩放，以及频率聚焦的辅助监督（FFS），协同缓解长序列信息稀释与高频细节合成不足。
primary_logic: 将长序列建模问题分解为注意力锐化、位置编码内插与频率域动态加权，三者结合可按比例将低分辨率编辑模型泛化至超高分辨率，并保持指令遵徇与纹理真实感。
claims:
- 应用后适应（注意力重缩放+RoPE重缩放+FFS）的 Kontext-dev 在 VINS-4KEval 上将 pFID 从 12.66 降至 9.15，改善显著。
- 消融实验表明，移除注意力重缩放或 RoPE 重缩放使 pFID 急剧上升（如 naive UHR scaling 的 pFID=15.01），证明两模块的必要性。
- 混合数据管理策略（真实视频对+长尾增强+多阶段过滤）相比未整理的 UHR 数据，在 ImageJudge 和 VIEScore 上均带来明显增益。
- VINS-4KEval 上 pFID = 9.15
---

# VINS-120K: Ultra High-Resolution Image Editing with A Large-Scale Dataset

> [!tip] 核心洞察
> 将长序列建模问题分解为注意力锐化、位置编码内插与频率域动态加权，三者结合可按比例将低分辨率编辑模型泛化至超高分辨率，并保持指令遵徇与纹理真实感。

| 字段 | 内容 |
|------|------|
| 中文题名 | VINS-120K：基于大规模数据集的超高清图像编辑 |
| 英文题名 | VINS-120K: Ultra High-Resolution Image Editing with A Large-Scale Dataset |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_VINS-120K_Ultra_High-Resolution_Image_Editing_with_A_Large-Scale_Dataset_CVPR_2026_paper.html) · [Code](https://github.com/Breakthrough/PySceneDetect) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | High-Frequency-Aware Post-Adaptation |
| Dataset | VINS-4KEval |

> [!tip] 效果简介
> - VINS-4KEval 上，pFID 9.15 vs 12.66 (原始 Kontext-dev) (-3.51)；ImageJudge-Avg 4.47 vs 3.98 (naive UHR 缩放) (+0.49)；pFID 9.15 vs 12.82 (Seedream 4.0) (-3.67 (-28.6%))。

## 概要

### 1. 问题背景

图像编辑模型在常规分辨率下已取得显著进展，然而将其直接应用于超高分辨率（Ultra‑High‑Resolution, UHR）图像时面临两个关键瓶颈：

1. **长序列退化**：UHR 图像产生的视觉 token 序列长度远超预训练模型的常规输入，导致注意力分布趋于均匀（熵偏移），特征区分度下降。
2. **高频细节丢失**：标准扩散损失未对高频纹理分量进行显式建模，使得编辑结果在精细纹理区域出现模糊或细节缺失。

现有的“降采样‑编辑‑超分”管线（如 Kontext+SR）虽可绕过序列长度限制，但超分步骤往往引入伪影且无法忠实地遵循编辑指令（见 Figure 1）。因此，如何在保持指令遵徇能力的前提下，将预训练的非高分辨率编辑模型泛化至 UHR 域，是本文要解决的核心问题。

### 2. 核心贡献

本文的贡献围绕**数据**与**方法**两个维度展开：

- **VINS‑120K 数据集**：构建了首个大规模超高清图像编辑数据集，平均分辨率达 4656 × 4138 像素，涵盖 13 种编辑类型。通过“真实 UHR 视频帧对 + 长尾编辑类型增强 + 多阶段质量过滤”的混合管理策略，VINS‑120K 在 ImageJudge‑Avg 上达到 4.45，显著优于现有编辑数据集（Table 1）。

- **高频感知后适应策略（High‑Frequency‑Aware Post‑Adaptation）**：针对长序列退化与高频细节丢失两个瓶颈，提出三项协同模块：
  - **分辨率感知注意力重缩放**：引入温度参数 $\tau = \log\sqrt{N_{\mathrm{UHR}}/N_{\mathrm{NHR}}}$ 锐化注意力分布，缓解长序列熵偏移。
  - **分辨率感知 RoPE 重缩放**：将旋转位置编码的基数按 $b' = b \cdot \sqrt{N_{\mathrm{UHR}}/N_{\mathrm{NHR}}}$ 动态调整，实现位置编码内插。
  - **频率聚焦监督（Frequency‑Focused Supervision, FFS）**：在频率域中根据去噪进度动态加权，显式强化高频分量的重建质量。

### 3. 主要结果

在 **VINS‑4KEval** 基准上，应用后适应策略的 **FLUX.1‑Kontext‑dev** 取得了以下关键结果：

- **感知保真度大幅提升**：pFID 从原始 Kontext‑dev 的 12.66 降至 **9.15**，降幅达 27.7%；相比当前最优 UHR 生成模型 **Seedream 4.0**（Team Seedream, arXiv 2025）的 12.82，pFID 降低 28.6%（Table 2）。
- **指令遵徇与视觉质量同步改善**：ImageJudge‑Avg 从 naive UHR 缩放的 3.98 提升至 **4.47**（Table 3）。
- **消融实验验证模块必要性**：移除注意力重缩放后 pFID 升至 15.01，移除 RoPE 重缩放同样导致质量显著下降；完整的混合数据管理策略相比未整理数据在多项指标上均有明显增益（Table 3）。

### 4. 方法谱系与知识库定位

本工作属于**超高分辨率图像编辑**方向，在方法谱系上定位如下：

- **编辑模型基础**：以 **FLUX.1‑Kontext‑dev**（Black Forest Labs, arXiv 2025）为骨干，属于基于流匹配的指令驱动编辑模型。与之对比的非高分辨率编辑模型包括 **AnyEdit**（Yu et al., CVPR 2025）、**OmniGen2**（Wu et al., arXiv 2025）和 **Step1X‑Edit**（Liu et al., arXiv 2025）。
- **UHR 生成参照**：**Seedream 4.0**（Team Seedream, arXiv 2025）作为当前最优 UHR 生成模型，在本文中作为主要对比对象。
- **技术谱系**：将大语言模型中的长上下文建模技术（注意力温度缩放、RoPE 基数内插）首次**分辨率感知地**引入扩散编辑模型，并与频率域动态监督结合，形成“注意力锐化 + 位置内插 + 频域加权”三位一体的后适应框架。

### 5. 局限与开放问题

- VINS‑120K 的场景与编辑类型多样性仍低于真实世界分布，部分复杂指令（如多对象替换）的编辑质量尚有改善空间。
- 高频感知后适应需要多 GPU 训练，计算开销较高。
- 如何将该策略推广至视频超高清编辑、以更轻量的注意力近似降低长序列计算成本、以及在动态场景下保证时间一致性，是值得进一步探索的开放问题。

### 超高清图像编辑的兴起与瓶颈

图像编辑技术近年来取得了长足进步，以 **FLUX.1-Kontext-dev**（Black Forest Labs, arXiv 2025）、**AnyEdit**（Yu et al., CVPR 2025）、**OmniGen2**（Wu et al., arXiv 2025）和 **Step1X-Edit**（Liu et al., arXiv 2025）为代表的非超高分辨率（NHR）模型，已在 1K 分辨率下展现出令人瞩目的指令遵徇能力与编辑质量。然而，当这些模型被直接应用于 4K 及以上的超高清（UHR）图像时，性能会急剧退化——编辑区域出现模糊、纹理细节丢失，甚至产生与指令不一致的伪影。

这一退化并非简单的分辨率不足问题，而是源于两个深层机制性瓶颈：

1.  **长序列导致的注意力熵偏移**：UHR 图像在扩散 Transformer 中产生的 token 序列长度远超预训练时的规模。标准 softmax 注意力在长序列下趋于均匀化，导致特征区分度下降，模型无法精确定位编辑区域。
2.  **高频纹理细节未被显式建模**：标准扩散损失（如流匹配损失）以像素空间的均方误差为核心，对低频结构天然友好，但对高频纹理的惩罚力度不足，导致合成结果缺乏真实感。

### 现有方案的局限

面对 UHR 编辑的挑战，工业界的主流方案是“降采样-编辑-超分”（Kontext+SR）的级联策略：先将 UHR 输入降采样至 NHR 模型可处理的尺寸，编辑后再用超分辨率模型放大。然而，这一范式存在根本性缺陷——编辑指令在降采样过程中可能丢失关键语义信息，而超分模型引入的纹理往往与编辑意图无关，最终导致“编辑不到位”或“纹理不真实”的双重困境。

另一方面，以 **Seedream 4.0**（Team Seedream, arXiv 2025）为代表的原生 UHR 生成模型虽然能直接产出高分辨率结果，但其编辑能力受限于训练范式，在指令遵徇度和编辑精度上仍落后于专门的 NHR 编辑模型。

### 数据集缺口

上述瓶颈的另一个根源在于数据。现有图像编辑数据集（如 X2Edit、ImgEdit）的分辨率普遍停留在 1K–1.3K，且样本多样性和质量参差不齐。缺乏大规模、高质量的 UHR 编辑数据，使得模型无法在训练阶段接触到超高分辨率下的编辑模式，进一步加剧了泛化困难。

### 本文动机

基于以上分析，本文的核心动机可归纳为三个层面：

1.  **构建首个大规模 UHR 图像编辑数据集**，填补从 1K 到 4K+ 的数据空白，为 UHR 编辑提供训练与评估基础。
2.  **揭示 NHR 模型向 UHR 泛化的关键瓶颈**，即长序列熵偏移与高频细节建模不足，而非简单的参数容量问题。
3.  **提出轻量级后适应策略**，在不重新训练基座模型的前提下，通过分辨率感知的注意力缩放、位置编码内插和频率聚焦监督，将 NHR 编辑模型高效泛化至 UHR 场景。

这一思路的核心洞察在于：**将长序列建模问题分解为注意力锐化、位置编码内插与频率域动态加权三个可控维度，三者协同可按比例将低分辨率编辑模型泛化至超高分辨率，同时保持指令遵徇与纹理真实感。**

## 核心方法与创新机理

本工作的根本瓶颈在于：预训练的非超高清（NHR）编辑模型直接应用于超高分辨率（UHR）图像时，会遭遇**长序列退化**与**高频细节丢失**双重困境。具体而言，UHR 图像产生的长 token 序列导致注意力熵偏移，使得特征区分度下降；同时，标准扩散损失未显式建模高频纹理，造成合成细节模糊。现有的“降采样-编辑-超分”管线（如 Kontext+SR）虽然可以规避分辨率限制，但超分模块往往引入伪影且无法忠实执行编辑指令，本质上是一种有损的妥协方案。

针对上述瓶颈，本文提出**高频率感知后适应（High-Frequency-Aware Post-Adaptation）**策略，其核心洞察是将长序列建模问题分解为三个正交且协同的维度：注意力锐化、位置编码内插与频率域动态加权。三者结合，可按比例将低分辨率编辑模型泛化至超高分辨率，同时保持指令遵从与纹理真实感。

### 关键改动槽位

与基线方法 **FLUX.1-Kontext-dev**（Black Forest Labs, arXiv 2025）相比，后适应策略在以下三个槽位进行了根本性改造：

| 改动槽位 | 基线做法 | 本文方案 | 机制解释 |
|----------|----------|----------|----------|
| **注意力得分计算** | 标准 softmax 注意力 | 引入分辨率感知温度参数 $\tau = \log\sqrt{N_{\mathrm{UHR}}/N_{\mathrm{NHR}}}$ 缩放注意力 logits | 长序列下注意力分布趋于均匀（熵增），$\tau > 1$ 锐化 softmax 输出，恢复特征区分度 |
| **RoPE 位置编码基数** | 固定频率基数 $b$ | 动态缩放 $b' = b \cdot \sqrt{N_{\mathrm{UHR}}/N_{\mathrm{NHR}}}$ | 将超长序列的旋转角度压缩至预训练范围内，实现位置编码的隐式内插 |
| **训练损失函数** | 仅流匹配损失 $\mathcal{L}_{\mathrm{FM}}$ | 额外增加频率聚焦损失 $\lambda \cdot \mathcal{L}_{\mathrm{freq}}$ | 在频率域中根据去噪进度动态加权，对高频分量施加更大惩罚，显式驱动纹理细节合成 |

### 三个协同模块的因果链条

**1. 分辨率感知注意力重缩放（Resolution-aware Attention Rescaling）**

当图像分辨率从 NHR 提升至 UHR，token 数量 $N$ 急剧增大，导致注意力分布熵增加，关键特征的响应被稀释。本文引入温度参数 $\tau$，将注意力权重重新定义为：

$$w_{m,n}' = \frac{ \exp{ \left( \tau \cdot \frac{ q_m^T k_n }{ \sqrt{d} } \right) } }{ \sum_{j=1}^N \exp{ \left( \tau \cdot \frac{ q_m^T k_j }{ \sqrt{d} } \right) } }$$

其中 $\tau = \log\sqrt{N_{\mathrm{UHR}}/N_{\mathrm{NHR}}}$ 随分辨率自适应调整。该设计的精巧之处在于：$\tau$ 并非人为设定的超参数，而是由序列长度比自然导出，使得注意力锐化程度与分辨率提升幅度精确匹配。

**2. 分辨率感知 RoPE 重缩放（Resolution-aware RoPE Rescaling）**

旋转位置编码（RoPE）的基数 $b$ 决定了频率基向量的周期。当序列长度超出预训练范围时，旋转角度会进入模型未曾见过的区间，导致位置编码失效。本文按序列长度比例缩放基数：

$$b' = b \cdot \sqrt{ \frac{ N_{\mathrm{UHR}} }{ N_{\mathrm{NHR}} } }$$

这一操作等价于将超长序列的旋转角度线性压缩回预训练分布内，使得模型无需重新学习位置关系即可适应长序列。与注意力重缩放形成互补：前者解决“特征是否被关注”，后者解决“位置是否被理解”。

**3. 频率聚焦监督（Frequency-Focused Supervision, FFS）**

前两个模块解决了长序列建模的结构性问题，但并未显式处理高频细节的合成质量。FFS 在标准流匹配损失 $\mathcal{L}_{\mathrm{FM}}$ 之外，引入频率域辅助损失：

$$\mathcal{L}_{\mathrm{freq}} = \frac{1}{UV} \sum_{u=1}^{U} \sum_{v=1}^{V} \mathcal{W}(\Delta F_{uv}, \alpha_t) \cdot \Delta F_{uv}$$

其中 $\Delta \boldsymbol{F} = |\mathrm{DFT}(\hat{\pmb y}) - \mathrm{DFT}(\pmb y)|$ 是预测图像与目标图像的频谱差异，$\mathcal{W}(\Delta F, \alpha_t) = (\Delta F + \varepsilon)^{\alpha_t} / \max(\Delta F + \varepsilon)^{\alpha_t}$ 是动态权重函数。$\alpha_t$ 随去噪时间步 $t$ 递减，使得训练早期关注全局结构，后期聚焦高频纹理。这一设计将扩散模型的渐进式生成特性与频率域的先验知识巧妙结合。

### 决定性证据

消融实验（Table 3）严格验证了各模块的必要性：
- 移除注意力重缩放后，pFID 从 **9.15** 急剧上升至 **15.01**，编辑图像出现明显模糊与细节丢失（Figure 8 可视化印证）；
- 移除 RoPE 重缩放同样导致编辑质量显著下降，证明位置适应对长序列至关重要；
- 完整的后适应策略将 Kontext-dev 的 pFID 从 **12.66** 降至 **9.15**，ImageJudge-Avg 从 **3.98** 提升至 **4.47**，且超越了专用 UHR 生成模型 **Seedream 4.0**（pFID=12.82，相对降低 28.6%）。

值得注意的是，这三个模块并非孤立有效——它们共同构成了一条完整的因果链：注意力重缩放确保模型“看得清”长序列中的关键区域，RoPE 重缩放确保模型“知道”这些区域的空间位置，FFS 则确保这些区域被“画得精细”。任一环节缺失，链条即断裂，性能急剧退化。

VINS-120K 提出的核心方法是一条**高频感知后适应（High-Frequency-Aware Post-Adaptation）**管线，旨在将预训练的非超高分辨率（NHR）编辑模型高效泛化至超高分辨率（UHR）场景。整个框架围绕一个关键洞察展开：超长序列建模问题可以分解为注意力锐化、位置编码内插与频率域动态加权三个子问题，三者协同作用，使模型在保持指令遵徇能力的同时合成高保真纹理细节。

### 输入输出流

管线的输入端是一个三元组：**UHR 输入图像**、**编辑指令**以及可选的掩码或辅助条件。输出端是经过编辑的 UHR 图像，其分辨率与输入保持一致。与常见的“下采样—编辑—超分”级联方案（如 Kontext+SR）不同，该框架直接在原生 UHR 分辨率上进行端到端编辑，从根本上避免了超分模块引入的伪影和细节虚构。

### 模块关系与数据流

整个适应过程由三个相互协作的模块构成，它们作用于预训练 NHR 编辑模型（如 **FLUX.1-Kontext-dev**, Black Forest Labs, arXiv 2025）之上，无需从头训练：

1. **分辨率感知注意力重缩放（Resolution-aware Attention Rescaling）**  
   当图像分辨率提升时，视觉 token 序列长度 $N$ 急剧增长，导致标准 softmax 注意力的熵增大，特征区分度下降。该模块引入一个与序列长度耦合的温度参数 $\tau = \log \sqrt{N_{\text{UHR}} / N_{\text{NHR}}}$，对注意力 logits 进行缩放：
   $$w_{m,n}' = \frac{ \exp{ \left( \tau \cdot \frac{ q_m^T k_n }{ \sqrt{d} } \right) } }{ \sum_{j=1}^N \exp{ \left( \tau \cdot \frac{ q_m^T k_j }{ \sqrt{d} } \right) } }$$
   这使得长序列下的注意力分布重新锐化，缓解熵偏移带来的信息稀释。

2. **分辨率感知 RoPE 重缩放（Resolution-aware RoPE Rescaling）**  
   旋转位置编码（RoPE）的基数 $b$ 在预训练时针对固定序列长度 $N_{\text{NHR}}$ 优化。当序列长度扩展至 $N_{\text{UHR}}$ 时，高频旋转角度会超出训练分布范围，导致位置编码失效。该模块将基数按比例缩放：
   $$b' = b \cdot \sqrt{ \frac{ N_{\mathrm{UHR}} }{ N_{\mathrm{NHR}} } }$$
   从而将旋转角度压缩回模型熟悉的区间，实现平滑的位置内插。

3. **频率聚焦监督（Frequency-Focused Supervision, FFS）**  
   标准流匹配损失 $\mathcal{L}_{\mathrm{FM}} = \left| \left| \nu(z_t, c, t) - (\epsilon - y) \right| \right|_2^2$ 对所有频率分量一视同仁，难以显式驱动高频纹理的合成。FFS 模块在频率域计算预测图像与目标图像的频谱差异 $\Delta \boldsymbol{F} = \left| \mathrm{DFT}(\hat{\pmb y}) - \mathrm{DFT}(\pmb y) \right|$，并通过动态权重函数 $\mathcal{W}(\Delta F, \alpha_t)$ 在去噪早期强调高频分量的重建。最终的辅助损失为：
   $$\mathcal{L}_{\mathrm{freq}} = \frac{1}{UV} \sum_{u=1}^{U} \sum_{v=1}^{V} \mathcal{W}(\Delta F_{uv}, \alpha_t) \cdot \Delta F_{uv}$$
   该损失与 $\mathcal{L}_{\mathrm{FM}}$ 联合优化，总损失为 $\mathcal{L}_{\text{total}} = \mathcal{L}_{\mathrm{FM}} + \lambda \cdot \mathcal{L}_{\mathrm{freq}}$。

### 训练数据支撑

上述后适应策略的有效性依赖于高质量 UHR 编辑数据。VINS-120K 数据集通过一条混合数据管理管线构建：首先从真实 UHR 视频中利用 PySceneDetect 切分镜头、提取帧对，经 CLIP Score 和光流过滤获得高保真编辑对；随后融合来自 X2Edit 和 Nano-Consistent 的长尾编辑类型样本，再经多阶段过滤（图像质量、指令一致性、美学评分）保留前 20% 的高质量数据。这一混合策略为后适应提供了兼具分辨率优势与编辑多样性的训练信号。

### 因果瓶颈与证据强度

上述三个模块直接针对分析揭示的双重瓶颈：**长序列注意力熵偏移**与**高频纹理缺乏显式建模**。消融实验提供了强因果证据——移除注意力重缩放使 pFID 从 9.15 升至 15.01（Table 3），移除 RoPE 重缩放同样导致质量急剧下降；完整的后适应策略在 VINS-4KEval 上将 Kontext-dev 的 pFID 从 12.66 降至 9.15（Table 2），并在 ImageJudge-Avg 上从 3.98 提升至 4.47（Table 3），改善幅度显著且一致。

![[assets/figures/papers/paper_list_l806_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_VINS_120K_Ultra_H/figures/001_Figure_1.jpg]]
*Figure 1: Comparison at ultra-high-resolution editing: From left to right are the input image, our edited result, and the edited image from Kontext+SR. Kontext+SR first downsamples the input, edits it using non-high-resolution models (Kontext), and then upsamples with super-resolution techniques. Our approach outperforms by synthesizing fine-grained details and consistently adhering to instructions*

![[assets/figures/papers/paper_list_l806_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_VINS_120K_Ultra_H/figures/004_Figure_4.jpg]]
*Figure 4: Data Filtering Pipeline. We filter images sequentially for corruption, low quality, inconsistent instructions, and poor aesthetics, retaining only 20% of the highest-quality data*

### 问题瓶颈

预训练的非超高分辨率（NHR）编辑模型直接处理超高分辨率（UHR）图像时，面临两个根本性瓶颈：

1. **长序列注意力熵偏移**：UHR 图像产生的 token 序列长度 $N_{\text{UHR}}$ 远超预训练时的 $N_{\text{NHR}}$，导致 softmax 注意力分布趋于均匀化，特征区分度下降。
2. **高频细节建模缺失**：标准扩散损失（如流匹配损失）对低频分量天然具有更高权重，高频纹理细节未被显式驱动，导致合成图像模糊或细节丢失。

本文提出的 **High-Frequency-Aware Post-Adaptation** 策略从注意力锐化、位置编码内插、频率域动态加权三个维度协同解决上述问题。

### 分辨率感知的注意力重缩放

当序列长度从 $N_{\text{NHR}}$ 扩展至 $N_{\text{UHR}}$ 时，注意力 logits 的方差下降，softmax 输出趋于平坦。为此，引入分辨率感知的温度参数 $\tau > 1$ 对注意力分数进行重缩放：

$$w_{m,n}' = \frac{ \exp{ \left( \tau \cdot \frac{ q_m^T k_n }{ \sqrt{d} } \right) } }{ \sum_{j=1}^N \exp{ \left( \tau \cdot \frac{ q_m^T k_j }{ \sqrt{d} } \right) } }$$

其中：
- $q_m, k_n \in \mathbb{R}^d$ 分别为第 $m$ 个查询向量和第 $n$ 个键向量，$d$ 为特征维度；
- $\tau = \log\sqrt{N_{\text{UHR}} / N_{\text{NHR}}}$，按序列长度比例自适应缩放。

**作用机制**：$\tau > 1$ 使注意力 logits 的方差被放大，softmax 输出重新锐化，恢复特征区分度。消融实验（Table 3, Figure 8）表明，移除该模块后 pFID 从 9.15 急剧升至 15.01，编辑图像出现明显模糊和细节丢失。

### 分辨率感知的 RoPE 重缩放

旋转位置编码（RoPE）的旋转角度由基数 $b$ 控制。当序列长度超出预训练范围时，高频旋转角度溢出，位置编码失效。通过动态缩放基数实现位置内插：

$$b' = b \cdot \sqrt{ \frac{ N_{\mathrm{UHR}} }{ N_{\mathrm{NHR}} } }$$

**作用机制**：将长序列的旋转角度按比例压缩回预训练模型的原生范围内，使模型无需重新学习位置关系即可适应超长序列。消融实验（Table 3, Section 5.2）证实，移除 RoPE 重缩放后编辑质量显著下降，说明位置适应对长序列建模不可或缺。

### 频率聚焦监督

标准流匹配损失在空间域计算逐像素误差，对低频分量天然偏重。为显式驱动高频细节合成，引入频率聚焦辅助损失。

**基础流匹配损失**（整流流）：

$$\mathcal{L}_{\mathrm{FM}} = \left| \left| \nu(z_t, c, t) - (\epsilon - y) \right| \right|_2^2$$

其中 $\nu(z_t, c, t)$ 为速度场预测，$\epsilon$ 为噪声，$y$ 为目标图像。

**频率差异**：对预测图像 $\hat{\pmb y}$ 与目标图像 $\pmb y$ 分别进行离散傅里叶变换（DFT），计算频谱幅度差异：

$$\Delta \boldsymbol{F} = \left| \mathrm{DFT}(\hat{\pmb y}) - \mathrm{DFT}(\pmb y) \right| \in \mathbb{R}^{U \times V}$$

**动态频率加权函数**：根据去噪进度 $t$ 自适应调整对不同频率分量的惩罚强度：

$$\mathcal{W}(\Delta F, \alpha_t) = \frac{(\Delta F + \varepsilon)^{\alpha_t}}{\max(\Delta F + \varepsilon)^{\alpha_t}}$$

其中 $\alpha_t$ 随去噪步数递减（早期 $t$ 大时 $\alpha_t$ 较大，强调全局结构；后期 $t$ 小时 $\alpha_t$ 较小，聚焦高频细节），$\varepsilon$ 为数值稳定常数。

**频率聚焦损失**：

$$\mathcal{L}_{\mathrm{freq}} = \frac{1}{UV} \sum_{u=1}^{U} \sum_{v=1}^{V} \mathcal{W}(\Delta F_{uv}, \alpha_t) \cdot \Delta F_{uv}$$

**总损失**：$\mathcal{L} = \mathcal{L}_{\mathrm{FM}} + \lambda \cdot \mathcal{L}_{\mathrm{freq}}$，其中 $\lambda$ 为平衡系数。

**作用机制**：$\mathcal{W}$ 对高频区域（$\Delta F$ 较大处）赋予更高权重，迫使模型在去噪过程中优先还原纹理细节。与注意力重缩放和 RoPE 重缩放协同，三者共同将低分辨率编辑模型按比例泛化至超高分辨率，同时保持指令遵徇与纹理真实感。

### 模块协同逻辑

三个模块形成因果闭环：
- **注意力重缩放**解决长序列带来的特征稀释问题，确保 token 间交互质量；
- **RoPE 重缩放**解决位置编码外推失效问题，确保空间结构正确；
- **频率聚焦监督**在前两者保障全局结构的基础上，显式驱动高频纹理合成。

消融实验（Table 3）的完整后适应配置（注意力重缩放 + RoPE 重缩放 + FFS）在 VINS-4KEval 上取得 pFID=9.15、ImageJudge-Avg=4.47，相较 naive UHR 缩放（pFID=15.01, ImageJudge-Avg=3.98）提升显著，验证了三模块的必要性与协同效果。

![[assets/figures/papers/paper_list_l806_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_VINS_120K_Ultra_H/figures/010_Figure_8.jpg]]
*Figure 8: Ablation on attention-score rescaling. Blue: with rescaling; Purple: without rescaling*

## 实验与关键发现

### 主实验结果

我们在自建的 **VINS-4KEval** 基准上对提出的高频感知后适应方法进行了全面评估。该基准涵盖多种编辑类型，所有对比方法均使用官方推荐设置与预训练权重。

**与基线方法的定量对比。** 表2报告了各方法在 VINS-4KEval 上的核心指标。以 **FLUX.1-Kontext-dev** (Black Forest Labs, arXiv 2025) 为骨干网络，施加完整后适应策略后，模型取得了 **9.15** 的 pFID，相比原始 Kontext-dev 的 12.66 降低了 3.51，改善幅度显著。在编辑质量 (Edit. Qual.) 指标上，适应后的 Kontext-dev 达到 4.70，为开源方法中最高。与当前最先进的超高清生成模型 **Seedream 4.0** (Team Seedream, arXiv 2025) 相比，本文方法在 pFID 上进一步降低 28.6%（9.15 vs. 12.82），验证了后适应策略在编辑任务上相对通用生成模型的优势。

**定性对比。** 图6展示了在 VINS-4KEval 上的可视化对比。本文方法在合成细粒度纹理（如毛发、织物）和保持指令遵徇方面均优于 Kontext+SR 的“降采样-编辑-超分”管线。图7进一步对比了与 Seedream 4.0 的编辑结果，本文方法在细节真实感上表现更优。

### 消融实验

为验证各模块的独立贡献，我们在 VINS-4KEval 上进行了系统的消融研究（表3）。

**后适应模块的必要性。** 当直接对 Kontext-dev 进行朴素的超高清缩放（naive UHR scaling）而不施加任何适应时，pFID 急剧上升至 15.01，ImageJudge-Avg 仅为 3.98。这表明预训练的非超高清模型无法直接泛化到长序列输入。

- **注意力分数重缩放：** 移除该模块后，pFID 升至 15.01，编辑图像出现明显模糊和细节丢失（图8）。注意力分布的熵偏移是导致长序列特征区分度下降的核心瓶颈。
- **RoPE 位置编码重缩放：** 移除该模块同样导致编辑质量显著下降。位置编码超出预训练范围后，模型无法有效利用序列中的空间信息，验证了位置内插对长序列适应的关键作用。

**频率聚焦监督 (FFS) 的增益。** 在注意力重缩放和 RoPE 重缩放基础上增加 FFS 辅助损失，进一步将 ImageJudge-Avg 从基础适应方案的对应值提升至 4.47，pFID 降至 9.15。FFS 通过在频率域中动态加权，显式驱动高频纹理的合成，弥补了标准流匹配损失对高频细节建模的不足。

**数据管理策略的贡献。** 采用完整的 VINS-120K 混合数据集（真实视频对 + 长尾增强 + 多阶段过滤）相比未整理的 UHR 数据，在 ImageJudge 和 VIEScore 上均带来明显增益。表1显示 VINS-120K 以 4.45 的 ImageJudge-Avg 得分位居现有编辑数据集之首，平均图像尺寸达 4656 × 4138 像素，验证了混合管理策略在数据质量和分辨率上的双重优势。

**跨骨干泛化性。** 表3同时报告了后适应策略在其他骨干上的表现，结果表明该方法不限于特定模型架构，具备良好的泛化能力。

### 失败模式与局限性

尽管整体性能优异，本文方法在以下场景仍存在不足：

- **复杂指令编辑：** 多对象替换或涉及精细空间关系的指令时，编辑质量仍有改善空间，部分结果存在对象边界不自然或属性遗漏的问题。
- **场景多样性：** VINS-120K 虽规模较大，但其场景与编辑类型多样性仍低于真实世界分布，在极端光照、复杂遮挡等条件下的泛化能力需进一步验证。
- **计算开销：** 高频感知后适应需要多 GPU 训练，长序列的注意力计算成本较高，限制了在资源受限环境下的部署。

### 关键图表结论

- **表2** 确立了本文方法在 VINS-4KEval 上的领先地位，pFID 9.15 和 Edit. Qual. 4.70 均为最优。
- **表3** 通过消融实验系统证明了注意力重缩放、RoPE 重缩放和 FFS 三个模块的必要性与互补性，以及混合数据管理策略的增益。
- **图6、图7** 从定性角度验证了方法在纹理合成和指令遵徇方面的优势。
- **图8** 直观展示了注意力重缩放对注意力分布锐化与细节保留的关键作用。

![[assets/figures/papers/paper_list_l806_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_VINS_120K_Ultra_H/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on VINS-4KEval. Higher values indicate better performance (↑), except*

![[assets/figures/papers/paper_list_l806_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_VINS_120K_Ultra_H/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparisons on the VINS-4KEval benchmark*

![[assets/figures/papers/paper_list_l806_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_VINS_120K_Ultra_H/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative comparison with Seedream 4.0*

## 定位与知识库关联

### 与现有超高清生成方法的对比

当前超高清（UHR）图像生成的主流方案可分为两类：原生高分辨率生成模型与“降采样-编辑-超分”级联管线。**Seedream 4.0**（Team Seedream, arXiv 2025）是原生方案的典型代表，直接在目标分辨率上训练扩散模型，在 VINS-4KEval 上取得了 pFID=12.82 的强基线。然而，这类方法需要从头预训练，计算成本极高，且难以复用已大量投资的非超高清（NHR）编辑模型。

级联方案（本文记为 Kontext+SR）则先降采样输入图像，用 NHR 编辑模型处理，再通过超分模型上采样恢复分辨率。该方案的致命缺陷在于：降采样操作不可逆地丢弃高频纹理信息，超分模型只能“猜测”细节，无法忠实恢复原始纹理。Figure 1 的定性对比直观展示了这一瓶颈——Kontext+SR 输出的纹理明显模糊，而本文方法合成的细节与输入图像高度一致。

本文提出的**高频率感知后适应**（High-Frequency-Aware Post-Adaptation）开辟了第三条路径：不重新预训练，也不依赖级联超分，而是通过三个协同的模块化修改，将预训练 NHR 编辑模型（**FLUX.1-Kontext-dev**，Black Forest Labs, arXiv 2025）按比例泛化至 UHR 域。这一思路与长上下文语言模型的位置内插技术（如 NTK-aware RoPE scaling）共享核心理念，但本文首次将其系统性地引入扩散图像编辑，并补充了频率域监督以弥合“注意力锐化仍无法保证高频细节”的残差。

### 与现有图像编辑模型的关系

在 NHR 编辑模型谱系中，**AnyEdit**（Yu et al., CVPR 2025）、**OmniGen2**（Wu et al., arXiv 2025）和 **Step1X-Edit**（Liu et al., arXiv 2025）代表了当前指令式编辑的最高水平，但它们均受限于预训练分辨率（通常 ≤ 1024×1024）。VINS-120K 的工作并不试图在 NHR 域内与这些方法竞争，而是提供了一套可插拔的适配层，理论上可应用于任何基于流匹配或扩散损失的 Transformer 编辑骨干。Table 3 的跨骨干实验初步验证了这一泛化性，但需注意当前仅在 FLUX.1-Kontext-dev 上进行了充分验证，对其他骨干的适配效果需进一步确认。

### 数据集贡献的生态位

VINS-120K 在数据层面填补了关键空白。如 Table 1 所示，此前最大的编辑数据集（如 X2Edit、ImgEdit）分辨率上限约为 1K–1.3K，且缺乏面向 UHR 编辑的指令-图像三元组。VINS-120K 的平均图像尺寸达 4656×4138 像素，ImageJudge-Avg 质量评分 4.45，显著高于现有数据集。其混合数据管理策略——从真实 UHR 视频提取帧对、辅以长尾编辑类型的增强样本、再经多阶段质量过滤——为后续 UHR 编辑研究提供了可复现的数据构建范式。

### 适用边界与局限

尽管实验证据充分（pFID 从 12.66 降至 9.15，Table 2），该方法存在以下明确边界：

1. **场景多样性受限**：VINS-120K 虽规模可观，但其 13 种编辑类型的分布和场景覆盖仍低于真实世界需求。在极端长尾编辑类型（如多对象替换）上，编辑质量仍有明显改善空间，这一点在论文局限性陈述中已明确承认。

2. **计算开销**：高频率感知后适应需要多 GPU 训练，且 FFS 损失涉及每步的 DFT 计算，增加了训练时的显存和计算负担。推理阶段的开销主要来自序列长度增长（与分辨率平方成正比），注意力重缩放和 RoPE 重缩放本身不引入额外计算，但长序列的注意力计算仍是瓶颈。

3. **位置编码内插的极限**：RoPE 基数重缩放 $b' = b \cdot \sqrt{ N_{\mathrm{UHR}} / N_{\mathrm{NHR}} }$ 本质上是一种外推-内插策略，当分辨率差距过大时（如 8K 以上），旋转角度的压缩可能导致位置区分度不足。论文未探索该内插策略的失效边界。

4. **证据强度说明**：跨骨干泛化性实验（Table 3）的验证范围有限，对其他编辑模型的适配效果需要更多独立验证。此外，FFS 损失中动态权重参数 $\alpha_t$ 的调度策略选择依据在论文中未充分展开，可能存在进一步优化的空间。

### 开放问题

从该方法论出发，以下问题值得后续探索：

- **视频 UHR 编辑的扩展**：当前后适应策略针对单帧设计，如何将注意力重缩放和频率域监督推广到时序一致的视频编辑，是直接且重要的延伸方向。

- **轻量化长序列注意力**：分辨率提升导致的序列长度平方级增长是根本性计算瓶颈。能否通过稀疏注意力、线性注意力近似或分块处理策略，在保持编辑质量的前提下降低推理成本？

- **动态场景的时间一致性**：VINS-120K 的数据来源（视频帧对）天然蕴含时序信息，但当前方法未显式建模时间一致性约束。在动态场景编辑中，如何保证跨帧的纹理和结构一致性？

## 原文 PDF

![[paperPDFs/CVPR_2026/VINS_120K_Ultra_High_Resolution_Image_Editing_with_A_Large_Scale_Dataset.pdf]]
