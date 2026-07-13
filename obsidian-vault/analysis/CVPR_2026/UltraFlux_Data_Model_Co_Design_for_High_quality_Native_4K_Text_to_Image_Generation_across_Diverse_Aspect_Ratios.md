---
title: "UltraFlux: Data-Model Co-Design for High-quality Native 4K Text-to-Image Generation across Diverse Aspect Ratios"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UltraFlux_Data_Model_Co_Design_for_High_quality_Native_4K_Text_to_Image_Generation_across_Diverse_Aspect_Ratios.pdf
project_link: "https://w2genai-lab.github.io/UltraFlux/"
code_link: "https://github.com/W2GenAI-Lab/UltraFlux"
aliases:
- UltraFlux
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过数据–模型协同设计，同时调控以下关键因子：① 使用 Resonance 2D RoPE 将频率对齐到训练窗口整数周期，并引入 YaRN 实现频带和宽高比感知的外推；② 对 F16 VAE 进行非对抗式后训练，提升 4K 重建保真度；③ 采用 SNR-Aware Huber 小波损失重新平衡不同时间步和频带的梯度；④ 采用阶段性美学课程学习（SACL）将...
primary_logic: 原生 4K 多宽高比生成需要从数据到模型的联合设计。单独改进位置编码、VAE 或损失函数均无法充分发挥数据潜力，只有将大规模、多宽高比、VLM 筛选的高质量数据集（MultiAspect-4K-1M）与训练窗口/频率/宽高比感知的位置编码、高保真 VAE 重构和频域-时间步平衡的优化目标相结合，才能实现稳定且细节丰富的原生 4K 合成。
claims:
- 2×2 数据-模型协同消融显示，同时使用 MultiAspect-4K-1M 数据集和 UltraFlux 方法（包含所有组件）相比仅更换数据或仅使用模型改进有非加性增益，FID 从 152.09 降至 145.81。
- 消融实验证实 SNR-Aware Huber Wavelet（SNR-HW）损失带来一致提升，SACL 进一步改善人类偏好和美学分数，而加入 Resonance 2D RoPE 和 YaRN 后达到最佳配置。
- Gemini-2.5-Flash 偏好评估中，UltraFlux 在视觉吸引力上被偏好比例为 70–82%，在提示对齐上为 60–89%，显著优于开源基线。
- Aesthetic-Eval@4096 (4096×4096) 上 FID ↓ = 143.11
---

# UltraFlux: Data-Model Co-Design for High-quality Native 4K Text-to-Image Generation across Diverse Aspect Ratios

> [!tip] 核心洞察
> 原生 4K 多宽高比生成需要从数据到模型的联合设计。单独改进位置编码、VAE 或损失函数均无法充分发挥数据潜力，只有将大规模、多宽高比、VLM 筛选的高质量数据集（MultiAspect-4K-1M）与训练窗口/频率/宽高比感知的位置编码、高保真 VAE 重构和频域-时间步平衡的优化目标相结合，才能实现稳定且细节丰富的原生 4K 合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | UltraFlux：面向原生4K多宽高比高质量文本-图像生成的数据-模型协同设计 |
| 英文题名 | UltraFlux: Data-Model Co-Design for High-quality Native 4K Text-to-Image Generation across Diverse Aspect Ratios |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18050) · [Project](https://w2genai-lab.github.io/UltraFlux/) · [Code](https://github.com/W2GenAI-Lab/UltraFlux) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UltraFlux |
| Dataset | Aesthetic-Eval@4096, 4096×2048, 2048×4096, 5120×2880 |

> [!tip] 效果简介
> - Aesthetic-Eval@4096 (4096×4096) 上，FID ↓ 143.11 vs 144.17 (Sana) (-1.06)；HPSv3 ↑ 11.47 vs 10.83 (Sana) (+0.64)；ArtiMuse ↑ 68.36 vs 63.72 (Sana) (+4.64)。
> - 4096×2048 (2:1) 上，FID ↓ 147.53 vs 150.35 (Sana) (-2.82)。
> - 2048×4096 (1:2) 上，FID ↓ 143.71 vs 149.41 (Sana) (-5.70)。

## 概要

UltraFlux 是一个面向原生 4K 分辨率、多宽高比文本到图像生成的统一模型。其核心挑战在于：位置编码、VAE 压缩和优化目标在 4K 分辨率及多宽高比下形成**耦合失败模式**——2D RoPE 无法适应训练窗口外的分辨率与宽高比变化，高倍率 VAE 压缩丢失高频细节，标准 L2 损失对高频误差梯度过低，三者相互放大，导致生成图像出现几何漂移、细节模糊和纹理丢失。

为此，UltraFlux 提出**数据–模型协同设计**范式，从四个关键维度同时调控：

1. **数据**：构建 MultiAspect-4K-1M，一个覆盖多种宽高比、含 VLM 美学/质量评分的百万级 4K 双语数据集。
2. **位置编码**：Resonance 2D RoPE 将频率对齐到训练窗口的整数周期，YaRN 实现频带和宽高比感知的外推，消除相位错位与条纹伪影。
3. **VAE 重建**：对 F16 VAE 进行非对抗式后训练，在 16× 压缩下显著提升 4K 重建保真度。
4. **训练目标**：SNR-Aware Huber Wavelet 损失在小波域结合 Pseudo-Huber 惩罚与 SNR 依赖阈值，阶段性美学课程学习（SACL）将高美学监督集中于高噪声步，平衡不同时间步和频带的梯度。

核心洞察在于：**单独改进位置编码、VAE 或损失函数均无法充分发挥数据潜力**，只有将大规模、多宽高比、VLM 筛选的高质量数据集与训练窗口/频率/宽高比感知的位置编码、高保真 VAE 重构和频域-时间步平衡的优化目标相结合，才能实现稳定且细节丰富的原生 4K 合成。

在 Aesthetic-Eval@4096 基准上，UltraFlux 在 FID、HPSv3 和 ArtiMuse 等指标上全面优于 Sana 等开源方法，并在 2:1、1:2、16:9、2.39:1 等多种宽高比下保持领先。Gemini-2.5-Flash 偏好评估中，UltraFlux 在视觉吸引力上被偏好比例为 70–82%，在提示对齐上为 60–89%。消融实验和 2×2 数据-模型协同消融进一步证实了各组件的非加性增益。



### 原生 4K 多宽高比生成的核心瓶颈

文本到图像生成模型在 1K 分辨率下已取得显著进展，但将生成分辨率直接提升至原生 4K 并同时支持多种宽高比时，面临一系列耦合性失败模式。这些模式并非孤立存在，而是由位置编码、变分自编码器（VAE）压缩和优化目标三者的相互作用共同导致：

- **位置编码的泛化失效**：标准 2D RoPE 的频率谱在训练窗口内是固定的，当推理分辨率或宽高比超出训练分布时，旋转位置编码的相位无法在窗口边界处闭合，引发几何漂移、重影和条纹伪影。全局 NTK 因子缩放虽能部分缓解，但缺乏对频带和宽高比的感知能力。
- **VAE 高倍压缩的高频丢失**：主流扩散模型通常采用 16× 压缩的 VAE（F16 VAE），在 4K 分辨率下，潜变量空间对高频细节的表达能力严重不足，导致重建图像出现纹理模糊和细节丢失。未经微调的 F16 VAE 在 4K 重建任务上的保真度远不能满足高质量生成的需求。
- **优化目标对高频误差的低敏感度**：标准 Flow Matching 的 L2 损失在高频区域的梯度过低，无法有效驱动模型学习精细纹理。同时，不同时间步（噪声水平）的梯度分布不均，进一步加剧了细节平滑问题。

上述三个因素相互放大：位置编码的相位错位产生几何伪影，VAE 压缩丢失高频信息，而 L2 损失又无法纠正这些高频误差，最终导致生成图像在结构一致性和纹理细节上的双重退化。

### 现有方法的局限

针对高分辨率生成，现有方法可大致分为两类：

- **训练无关的推断缩放方法**：如 **ScaleCrafter** 和 **FouriScale** 等，通过在推理阶段对预训练 1K 模型进行频率域或注意力机制的调整来实现高分辨率生成。这类方法无需额外训练，但受限于基础模型的容量和训练分布，在宽高比泛化和细节保真度上存在根本性瓶颈。
- **原生 4K 训练方法**：如 **Sana**（Su et al., NeurIPS 2024）采用线性注意力 DiT 架构进行原生 4K 生成，**Diffusion-4K** 则通过小波损失进行 4K 微调。这些方法虽有所改进，但大多仅从模型或数据的单一维度进行优化，未能系统性地解决位置编码、VAE 重建和优化目标的耦合问题。闭源商业模型如 **Seedream 4.0**（ByteDance, 2025）在多宽高比 4K 生成上表现优异，但其技术细节未公开，且需要大量工程化处理。

### 本文动机：数据–模型协同设计

UltraFlux 的核心洞察在于：**原生 4K 多宽高比生成需要从数据到模型的联合设计**。单独改进位置编码、VAE 或损失函数均无法充分发挥数据潜力，只有将大规模、多宽高比、VLM 筛选的高质量数据集与训练窗口/频率/宽高比感知的位置编码、高保真 VAE 重构和频域-时间步平衡的优化目标相结合，才能实现稳定且细节丰富的原生 4K 合成。

为此，UltraFlux 提出了一套完整的协同设计方案，涵盖以下关键组件：

1. **MultiAspect-4K-1M 数据集**：构建覆盖多种宽高比的百万级 4K 图像数据集，提供 VLM 美学/质量评分和双语标注，为模型训练提供高质量的监督信号。
2. **Resonance 2D RoPE + YaRN**：将每轴频率对齐到训练窗口的整数周期（共振模式），并利用 YaRN 实现频带和宽高比感知的外推，从根本上消除相位错位。
3. **非对抗式 VAE 后训练**：基于高频筛选的子集对 F16 VAE 解码器进行微调，仅使用小波、感知和 L2 损失，提升 4K 重建的高频保真度。
4. **SNR-Aware Huber Wavelet 损失**：在小波域计算 Pseudo-Huber 残差，结合 SNR 依赖阈值和 Min-SNR 时间步重加权，平衡不同频带和噪声水平下的梯度。
5. **阶段性美学课程学习（SACL）**：分两阶段训练，在高噪声步集中使用最高美学子集，提升整体观感而不牺牲低频结构。

通过这一协同设计范式，UltraFlux 在开源 4K 生成模型中取得了领先性能，并在与闭源商业系统的对比中展现出竞争力。



## 核心方法与创新机理

UltraFlux 的核心创新在于一次**数据–模型协同设计**，同时重塑了 4K 多宽高比生成的四个关键环节：训练数据、位置编码、VAE 压缩保真度与优化目标。这四个“changed slots”并非孤立改进，而是围绕一个共同瓶颈——位置编码、VAE 压缩和优化目标在 4K 分辨率及多宽高比下的耦合失败——进行联合调控，从而在单一 DiT 骨干上实现原生 4K 合成。

### 1. 数据槽位：MultiAspect-4K-1M 数据集

与现有 4K 数据集相比，MultiAspect-4K-1M 在三个维度上进行了系统性补强（见 Table 1 与 Figure 4）：
- **宽高比覆盖**：涵盖从 1:2 到 2.39:1 的多种宽高比，分布显著宽于其他 4K 数据集，使模型在训练阶段即接触多宽高比下的空间结构。
- **监督质量刷新**：采用 VLM 驱动的美学与质量评分（Q-Align 与 ArtiMuse），辅以平坦度与信息熵等经典 IQA 信号，替代单一美学模型，减少评分偏差。
- **分布去偏**：通过双语标注与人物标签，缓解数据集中特定内容或风格的过拟合风险。

该数据集包含约 100 万张图像，平均分辨率 4,521×4,703，平均 ArtiMuse 评分 64.59，平均标注长度 125.1 tokens，且提供双语标注（Table 1）。这一数据设计为后续模型改进提供了必要的高质量、多宽高比 4K 先验。

### 2. 位置编码槽位：Resonance 2D RoPE + YaRN

标准 2D RoPE 在训练窗口外的分辨率和宽高比下会产生相位错位，导致几何漂移与条纹伪影。UltraFlux 的解决方案分两步（见 Eq. (1)–(8)）：

- **Resonance 2D RoPE**：将每轴频率 $\omega_k^{(a)}$ 替换为共振频率 $\hat{\omega}_k^{(a)}$，使每个频带在训练窗口长度 $L_a$ 内完成整数个周期（Eq. (5)）。这消除了因非整数周期累积引起的相位错位，从根源上抑制重影与条纹。
- **YaRN 频带感知外推**：基于共振周期数 $\hat{r}_k^{(a)}$ 决定每个频带的外推策略——低周期频带采用线性位置插值缩放，高周期频带保持原频率（Eq. (7)–(8)）。这使得外推过程同时感知训练窗口、频带与宽高比，避免了全局 NTK 因子对所有频带的一刀切处理。

消融实验证实，同时启用 Resonance 2D RoPE 与 YaRN 可获得最佳整体配置（FID 146.93, HPSv3 10.91, ArtiMuse 68.13），显著优于仅使用其中一项或标准 RoPE。

### 3. VAE 槽位：非对抗式 VAE 后训练

Flux 原生 F16 VAE 在 4K 分辨率下会丢失高频细节，限制了 DiT 的上限。UltraFlux 对 VAE 解码器进行轻量后训练（约 4k 步），关键设计选择是：
- **显式目标高频**：将小波重建损失应用于高频子带（LH, HL, HH），结合特征空间感知损失，而非依赖对抗损失或纯像素级损失。
- **非对抗式**：最终配方仅保留小波、感知与 L2 损失，省略对抗项，避免引入额外训练不稳定性和伪影。

在 Aesthetic-4K@4096 评测集上，后训练 VAE 的重建指标显著优于未微调的 F16 VAE（Table 8），为 DiT 提供了更保真的潜变量空间。

### 4. 优化目标槽位：SNR-Aware Huber Wavelet 损失 + SACL

标准 Flow Matching L2 损失在 4K 潜变量上存在双重缺陷：对高频误差梯度过低导致细节模糊，且不同时间步的梯度不平衡使训练信号被低噪声步主导。UltraFlux 的解决方案包含两个互补组件：

- **SNR-Aware Huber Wavelet 损失**（Eq. (9)–(14)）：在小波域计算 Pseudo-Huber 残差，阈值 $c(t)$ 随 SNR 变化——低 SNR（高噪声）时阈值较小，提供鲁棒性；高 SNR（低噪声）时阈值增大，逼近 L2 精度。同时采用 Min-SNR 时间步重加权 $\omega(t)$，平衡不同噪声水平的梯度贡献。
- **阶段性美学课程学习（SACL）**：分两阶段训练——第一阶段在全数据上学习通用 4K 先验；第二阶段将计算资源集中于高噪声步（模型先验主导阶段），并使用最高美学子集进行监督，提升整体观感而不牺牲低频结构。

消融实验表明，SNR-HW 损失在所有指标上相较标准 L2 带来一致改善；叠加 SACL 后，HPSv3 与 ArtiMuse 等人类偏好指标进一步提升；最终联合 Resonance 2D RoPE + YaRN 达到最优。

### 协同效应的决定性证据

2×2 数据–模型协同消融（Table 7）直接验证了协同设计的必要性：
- 仅更换数据（配置 B）或仅使用模型/损失改进（配置 C）均无法达到全协同配置（配置 D）的性能。
- 全协同配置将 FID 从基线 152.09 降至 145.81，增益具有非加性特征，证明数据与模型改进之间存在相互放大效应。

这一协同效应源于四个槽位的耦合关系：高质量多宽高比数据为位置编码外推提供了训练窗口感知的基础；高保真 VAE 重构使 DiT 的优化目标能有效作用于高频细节；而 SNR-Aware Huber Wavelet 损失则确保这些细节在训练中不被 L2 损失的梯度偏向所平滑。单独改进任一槽位都会因其他槽位的瓶颈而无法充分发挥潜力。



UltraFlux 采用**数据–模型协同设计（data–model co-design）**范式，将大规模高质量多宽高比 4K 数据集构建与模型侧的位置编码、VAE 后训练、优化目标及训练策略进行联合优化，以解决原生 4K 多宽高比文本到图像生成中的耦合失败模式。其核心洞察在于：单独改进位置编码、VAE 或损失函数均无法充分发挥数据潜力，只有将各组件协同设计才能实现稳定且细节丰富的原生 4K 合成。

整体 pipeline 由以下模块串联构成：

1. **MultiAspect-4K-1M 数据集构建**  
   从多源 4K 图像中筛选出约 100 万张图像，覆盖多种宽高比，并通过 VLM 驱动的质量/美学评分（Q-Align、ArtiMuse）及经典 IQA 信号（平坦度、信息熵）进行过滤与标注。数据集提供双语描述与人物标签，用于条件训练与分层采样。该模块为后续所有训练提供数据基础（Figure 2）。

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/002_Figure_2.jpg]]
*Figure 2: Data Pipeline overview*

2. **VAE 后训练**  
   基于高频筛选的子集对 Flux F16 VAE 解码器进行非对抗式微调（仅使用小波重建损失、感知损失和 L2 损失），提升 4K 重建的高频细节保真度，使 DiT 在 16× 压缩下仍能保留纹理信息。

3. **Resonance 2D RoPE + YaRN 位置编码**  
   将标准 2D RoPE 的频率对齐到训练窗口的整数周期（共振模式），消除分数周期累积导致的相位错位与条纹伪影；再通过 YaRN 依据各频带在训练窗口内的周期数进行频带感知和宽高比感知的外推，使模型在训练窗口外的分辨率与宽高比下仍保持几何一致性。

4. **SNR-Aware Huber Wavelet 损失**  
   在小波域计算 Pseudo-Huber 残差，结合 SNR 依赖的动态阈值和 Min-SNR 时间步重加权，平衡不同噪声水平与频带的梯度，避免高频细节被 L2 损失过度平滑。

5. **阶段性美学课程学习（SACL）**  
   分两阶段训练 DiT：第一阶段在全数据上学习通用 4K 先验；第二阶段在高噪声步（模型先验主导阶段）集中使用最高美学子集进行监督，提升整体观感而不牺牲低频结构。

输入输出流为：文本提示 → 文本编码器 → DiT（含 Resonance 2D RoPE + YaRN）在潜空间进行 Flow Matching 去噪 → 后训练 F16 VAE 解码器 → 原生 4K 多宽高比图像。训练过程中，SNR-Aware Huber Wavelet 损失作用于小波域，SACL 控制不同训练阶段的数据分布与时间步采样策略。

2×2 数据–模型协同消融（Table 7）证实了该 pipeline 的非加性增益：仅更换数据（B）或仅使用模型/损失改进（C）均无法达到全协同配置（D）的性能（FID 从 152.09 降至 145.81），验证了数据与模型联合设计的必要性。



UltraFlux 的核心技术方案围绕四个关键模块展开，它们共同构成了数据–模型协同设计的骨架：① 非对抗式 VAE 后训练，提升 4K 潜变量重建保真度；② Resonance 2D RoPE + YaRN 位置编码，消除多宽高比外推时的相位错位；③ SNR-Aware Huber Wavelet 训练目标，在频域和噪声水平两个维度上平衡梯度；④ 阶段性美学课程学习（SACL），将高美学监督集中于模型先验主导的高噪声步。

### 非对抗式 VAE 后训练

F16 VAE（16× 压缩）在 4K 分辨率下会丢失高频细节，直接限制 DiT 的上限。UltraFlux 从 MultiAspect-4K-1M 数据集中筛选高频内容丰富的子集，对 Flux F16 解码器进行约 4k 步的微调。关键设计在于**显式去除对抗损失**，仅保留小波重建损失（施加于高频子带）、特征空间感知损失和 L2 损失的组合。这一非对抗方案避免了 GAN 训练的不稳定性，同时在小波域针对高频子带施加重建损失，有效恢复了纹理和边缘细节。

### Resonance 2D RoPE + YaRN 位置编码

标准 2D RoPE 的频率定义在训练窗口外会产生非整数周期，导致相位错位和条纹伪影。UltraFlux 的解决方案分两步：

**第一步：共振频率对齐。** 对每轴（高度/宽度 $a$）的每个频带 $k$，计算其在训练窗口长度 $L_a$ 内的周期数：

$$r_{k}^{(a)} = \frac{L_{a}}{\lambda_{k}^{(a)}} = \frac{L_{a}\omega_{k}^{(a)}}{2\pi}$$

将其舍入到最近的非零整数：

$$\hat{r}_{k}^{(a)} = \max\bigl(1, \lfloor r_{k}^{(a)} + \frac12 \rfloor\bigr)$$

得到共振频率，保证在训练窗口内形成驻波：

$$\hat{\omega}_{k}^{(a)} = \frac{2\pi \hat{r}_{k}^{(a)}}{L_{a}}$$

这一操作使频谱显式感知训练窗口，从根源上抑制了分数周期累积导致的鬼影和条纹。

**第二步：YaRN 频带感知外推。** 基于共振周期数 $\hat{r}_{k}^{(a)}$ 设计线性斜坡函数：

$$\gamma(r; \alpha, \beta) = \begin{cases} 0, & r < \alpha \\ \frac{r-\alpha}{\beta-\alpha}, & \alpha \leq r \leq \beta \\ 1, & r > \beta \end{cases}$$

对每个频带，根据其周期数决定外推策略——低频带（周期数少）进行线性位置插值缩放，高频带（周期数多）保持原频率：

$$\omega_{k,\mathrm{yarn}}^{(a)} = \bigl(1 - \gamma(\hat{r}_{k}^{(a)}; \alpha, \beta)\bigr) \frac{\hat{\omega}_{k}^{(a)}}{s_{a}} + \gamma(\hat{r}_{k}^{(a)}; \alpha, \beta) \hat{\omega}_{k}^{(a)}$$

其中 $s_a$ 为轴 $a$ 的外推因子。这种频带感知机制使得不同宽高比下的位置编码能够自适应调整，避免了全局 NTK 因子对所有频带“一刀切”的粗糙处理。

### SNR-Aware Huber Wavelet 训练目标

标准 Flow Matching 的 L2 损失在 4K 潜变量上存在双重失衡：低 SNR（高噪声步）时梯度被异常值主导，高 SNR（低噪声步）时对高频细节的梯度不足。UltraFlux 将训练目标重构为小波域的 Pseudo-Huber 损失，并引入 SNR 依赖的阈值调度和时间步重加权。

**Flow Matching 插值**采用直路径：

$$z_{t} = (1-t)z + t\varepsilon$$

由速度场 $v_{\theta}$ 预测干净潜变量：

$$\hat{z}_{\theta}(z_{t}, t) = z_{t} - t v_{\theta}(z_{t}, t)$$

**时间步权重**结合直路径因子和 Min-SNR 重加权，平衡不同噪声水平的梯度贡献：

$$\omega(t) = \frac{t}{1-t} \min\{\mathrm{SNR}(t), \gamma\}^{\beta}$$

其中 $\mathrm{SNR}(t) = (1-t)^2 / t^2$。

**Pseudo-Huber 阈值**随 SNR 动态调整——低 SNR 时阈值较小，损失函数更接近 L1 以抑制异常值影响；高 SNR 时阈值增大，损失函数趋近 L2 以保留精细梯度：

$$c(t) = c_{\mathrm{min}} + (c_{\mathrm{max}} - c_{\mathrm{min}}) \bigl( \frac{\min\{\mathrm{SNR}(t), \gamma\}}{\gamma} \bigr)^{\alpha}$$

**小波域损失**在正交小波系数上逐像素计算 Pseudo-Huber 惩罚：

$$\ell_{\mathrm{Huber}}(R_{\theta}; c(t)) = \frac{1}{N} \sum_{p=1}^{N} \rho_{c(t)}(R_{\theta,p})$$

最终训练目标整合时间步权重与小波域鲁棒损失：

$$\mathcal{L}(\theta) = \mathbb{E}_{z,\varepsilon,t} \bigl[ \omega(t) \ell_{\mathrm{Huber}}(R_{\theta}; c(t)) \bigr]$$

这一设计同时实现了三个维度的平衡：频域上通过小波分解显式区分高低频子带，噪声水平上通过 SNR 依赖阈值自适应调节鲁棒性，时间步上通过 Min-SNR 权重避免高噪声步被低噪声步淹没。

### 阶段性美学课程学习（SACL）

SACL 将训练分为两个阶段。第一阶段在全量 MultiAspect-4K-1M 数据上学习通用 4K 先验分布，建立低频结构和语义基础。第二阶段将剩余计算量集中于高噪声步（$t$ 接近 1，模型先验主导生成方向），仅使用最高美学评分的子集进行监督。这一策略避免了在全时间步上使用高美学数据可能导致的分布偏移，同时将美学信号的优化集中在最能影响整体观感的噪声区间。消融实验证实，在 SNR-HW 损失基础上加入 SACL 可进一步提升 HPSv3 和 ArtiMuse 等人类偏好相关指标。

### 模块间耦合关系

四个模块并非独立运作，而是形成互补的级联效应。VAE 后训练提升了潜变量空间的信息保真度上限，使 DiT 的优化目标有更丰富的高频信号可供学习。Resonance 2D RoPE + YaRN 确保多宽高比下的位置编码一致性，防止几何漂移破坏 VAE 重建的细节。SNR-Aware Huber Wavelet 损失在小波域对高低频子带施加差异化梯度，使得 VAE 重建的高频细节能够被有效传递到 DiT 输出。SACL 则在高噪声步集中美学监督，在已有高频细节的基础上进一步提升整体观感。2×2 数据–模型协同消融（Table 7）证实，单独替换数据或单独改进模型/损失均无法达到全协同配置的性能，四者的联合使用带来了非加性增益。

### 补充图表

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/019_Figure_10.jpg]]
*Figure 10: Qualitative effect of Resonance 2D RoPE with YaRN. We compare three positional encodings at native 4K resolution for the same prompts. (a) Flux.1 2D RoPE baseline without any scaling at inference time, which tends to exhibit geometric drift and mild striping or warping artifacts in both foreground objects and backgrounds. (b) 2D RoPE with YaRN scaling, which stabilizes the overall layout but still shows subtle distortions along long contours and in extreme regions of the image. (c) Our proposed Resonance 2D RoPE with YaRN, which yields the most coherent global geometry and sharper, more regular fine structures (e.g., ring edges and tree trunks)*



## 实验与关键发现

### 核心瓶颈与协同设计验证

UltraFlux 的核心假设是：原生 4K 多宽高比生成的瓶颈并非单一模块缺陷，而是位置编码、VAE 压缩与优化目标在 4K 分辨率下形成的**耦合失败模式**——2D RoPE 无法适应训练窗口外的分辨率与宽高比变化，高倍率 VAE 压缩丢失高频细节，标准 L2 损失对高频误差梯度过低，三者相互放大，导致几何漂移、细节模糊和纹理丢失。因此，UltraFlux 采用**数据–模型协同设计**，同时调控数据集、VAE、位置编码和训练目标四个关键因子。

**2×2 数据-模型协同消融**（Table 7）直接验证了这一假设。该实验以原始 Flux 模型为基线（A），分别测试仅替换数据集为 MultiAspect-4K-1M（B）、仅使用 UltraFlux 的模型/损失改进（C）、以及全协同配置（D）。结果如表所示：

| 配置 | 数据 | 模型/损失 | FID ↓ |
|------|------|-----------|-------|
| A (基线) | 原始 | 原始 | 152.09 |
| B (仅数据) | MultiAspect-4K-1M | 原始 | 149.31 |
| C (仅模型) | 原始 | UltraFlux | 148.76 |
| D (全协同) | MultiAspect-4K-1M | UltraFlux | **145.81** |

单独替换数据或模型带来的 FID 改善分别为 2.78 和 3.33，而全协同配置的改善幅度达到 6.28，**超出两者之和**，证实了数据与模型之间存在非加性的协同增益。这一结果为“原生 4K 生成需要从数据到模型的联合设计”这一核心洞察提供了最直接的实证支撑。

### 4K 分辨率主结果

在 Aesthetic-Eval@4096 基准（4096×4096 正方形分辨率）上，UltraFlux 与开源方法进行定量对比（Table 2）。UltraFlux 在 FID、HPSv3 和 ArtiMuse 三项指标上均达到最优：FID 降至 143.11，相较最强开源基线 **Sana**（Su et al., NeurIPS 2024）的 144.17 降低 1.06；HPSv3 达到 11.47（Sana 为 10.83，提升 +0.64）；ArtiMuse 达到 68.36（Sana 为 63.72，提升 +4.64）。这表明 UltraFlux 在分布匹配、人类偏好和美学质量三个维度上全面领先。

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison under 4K res. with open-source methods*

Gemini-2.5-Flash 偏好评估（Figure 5）进一步从感知层面验证了这一优势：在视觉吸引力维度，UltraFlux 被偏好比例为 70–82%；在提示对齐维度，偏好比例为 60–89%，显著优于开源基线。视觉对比（Figure 6、Figure 11–13）显示，UltraFlux 生成的 4K 图像在纹理细节、几何一致性和全局构图方面均优于对比方法。

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/005_Figure_5.jpg]]
*Figure 5: Gemini-2.5-Flash preference comparison*

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/009_Figure_6.jpg]]
*Figure 6: Visual comparison of open-source methods on the Aesthetic-Eval@4096 benchmark at 4096×4096 resolution*

### 多宽高比泛化能力

UltraFlux 的核心设计目标之一是支持多样化宽高比的原生 4K 生成。在非正方形分辨率上的定量对比（Table 3、Table 4）显示：

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison with Sana at 4096×2048 (2:1) and 2048×4096 (1:2) resolutions*

- **4096×2048 (2:1)**：FID 147.53 vs. Sana 150.35（Δ = −2.82）
- **2048×4096 (1:2)**：FID 143.71 vs. Sana 149.41（Δ = −5.70）
- **5120×2880 (16:9)**：FID 142.43 vs. Sana 153.31（Δ = −10.88）
- **5952×2496 (2.39:1)**：FID 151.98 vs. Sana 153.10（Δ = −1.12）

在所有测试的宽高比下，UltraFlux 均一致优于 Sana，尤其在 16:9 宽屏分辨率上优势最为显著（FID 差距超过 10 点）。这验证了 Resonance 2D RoPE + YaRN 对宽高比感知位置编码的有效性——通过将每轴频率对齐到训练窗口整数周期并进行频带感知外推，有效抑制了非训练宽高比下的相位错位和条纹伪影（Figure 10 定性展示）。

### 与闭源商业系统的对比

UltraFlux 与闭源商业模型 **Seedream 4.0**（ByteDance, 2025）进行对比（Table 5）。为公平比较，UltraFlux 使用 GPT-4o 提示精炼器以匹配 Seedream 4.0 的提示风格，而 Seedream 4.0 使用原生提示。在 HPSv3 指标上，UltraFlux（w. Prompt Refiner）达到 12.03，略高于 Seedream 4.0 的 11.98（Δ = +0.05）；在 ArtiMuse 上达到 68.75，同样优于 Seedream 4.0 的 67.50。需要注意的是，由于 Seedream 4.0 为闭源系统且提示处理流程不可控，该对比的公平性存在一定局限，但结果仍表明 UltraFlux 在开源框架下已具备与顶级商业系统竞争的能力。

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/008_Table_5.jpg]]
*Table 5: Quantitative comparison under 4K res. with close-source method*

### 组件消融分析

Table 6 的系统消融实验揭示了各组件对性能的独立贡献：

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/010_Table_6.jpg]]
*Table 6: Ablation study on UltraFlux at 4K resolution training*

1. **SNR-Aware Huber Wavelet（SNR-HW）损失**：将标准 L2 损失替换为 SNR-HW 损失后，在所有指标上均带来一致改善。这验证了该损失函数的设计动机——在小波域使用 Pseudo-Huber 惩罚并结合 SNR 依赖阈值，能有效平衡不同频带和时间步的梯度，避免高频细节的过度平滑。

2. **阶段性美学课程学习（SACL）**：在 SNR-HW 基础上加入 SACL 后，HPSv3 和 ArtiMuse 等人类偏好相关指标进一步提升。这证实了将高美学监督集中于高噪声步（模型先验主导阶段）的策略，能在不牺牲低频结构的前提下提升整体观感。

3. **Resonance 2D RoPE + YaRN**：同时引入 Resonance 2D RoPE 和 YaRN 后，模型达到最佳整体配置（FID 146.93, HPSv3 10.91, ArtiMuse 68.13）。这验证了训练窗口感知、频带感知和宽高比感知的位置编码对 4K 多宽高比生成的关键作用。

### VAE 后训练效果

Table 8 展示了 VAE 后训练对 4K 重建保真度的影响。在 MultiAspect-4K-1M 高频筛选子集上对 F16 VAE 解码器进行非对抗式微调（仅使用小波+感知+L2 损失，约 4k 步）后，重建指标在 Aesthetic-4K@4096 评测集上获得显著提升。这直接支撑了 UltraFlux 的设计决策：在 16× 压缩比下，显式针对高频内容进行 VAE 后训练是 DiT 保有高保真度的必要条件。

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/012_Table_8.jpg]]
*Table 8: Reconstruction metrics of F16 VAEs on the Aesthetic-4K@4096 Eval set [42]*

### 推理效率与局限性

Table 10 报告了 4K 生成的推理时间。尽管 UltraFlux 使用 F16 VAE 和优化的 DiT，50–60 步 4K 生成仍需高端 GPU（约 50GB 显存），延迟相较于 1K 模型显著偏高。这一采样开销与显存占用构成了当前方法的主要工程瓶颈，限制了其在大规模部署场景中的推广。此外，在困难案例中仍可能出现过平滑纹理或微小几何伪影，表明美学质量并非在所有提示与领域都达到顶级水准。

### 开放问题

当前协同设计范围受限于单一大型 DiT 骨干，尚未探索稀疏/低秩注意力、轻量解码器或蒸馏至更小模型等方向。如何将该范式扩展到更参数高效的架构以显著降低显存与延迟，以及该协同设计能否泛化到专业科学图像或医学影像等更广泛的数据域，是后续研究的重要方向。

### 补充图表

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/011_Table_7.jpg]]
*Table 7: 2×2 data–model co-design ablation. A: baseline; B: data only; C: model/loss only; D: full co-design*

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/004_Table_1.jpg]]
*Table 1: Dataset statistical comparisons*

![[assets/figures/papers/paper_list_l2352_https_arxiv_org_abs_2511_18050/figures/003_Figure_4.jpg]]
*Figure 4: Dataset aspect and resolution analysis. All datasets use 10k samples. MultiAspect-4K-1M has a broader aspect ratio distribution*



## 定位与知识库关联

### 1. 与现有方法的关系

UltraFlux 处于原生高分辨率文本-图像生成这一新兴赛道的交叉点上。从技术路线看，现有解决高分辨率生成的方法可分为三类：**训练无关的推断缩放方法**、**基于小波损失的微调方法**和**原生 4K 训练方法**。UltraFlux 属于第三类，但其核心贡献在于提出了一种**数据–模型协同设计范式**，而非单一维度的改进。

**与推断缩放方法的区别。** ScaleCrafter 和 FouriScale 等训练无关方法通过在推断阶段对注意力机制或频率域进行干预来实现高分辨率生成，无需重新训练。这类方法虽然灵活，但本质上是在训练分布之外进行外推，容易产生几何漂移和纹理伪影。UltraFlux 选择了一条更彻底的路径——通过大规模 4K 数据集进行原生训练，从根本上避免了分布外推问题。其提出的 Resonance 2D RoPE 与 YaRN 组合正是为了在训练窗口内建立稳定的频率表征，使得模型在 4K 分辨率下不会出现相位错位和条纹伪影（Figure 10 提供了三种位置编码的定性对比）。

**与原生 4K 训练方法的差异。** 在原生 4K 训练阵营中，最直接的对比对象是 **Sana**（Su et al., NeurIPS 2024）和 Diffusion-4K。Sana 采用线性注意力 DiT 架构实现原生 4K 生成，但其位置编码方案未针对多宽高比进行专门设计，导致在非正方形宽高比（如 2:1、1:2）下性能下降明显。UltraFlux 通过 Resonance 2D RoPE + YaRN 实现了频带感知和宽高比感知的外推，在 4096×2048（2:1）上将 FID 从 150.35 降至 147.53，在 2048×4096（1:2）上从 149.41 降至 143.71（Table 3）。Diffusion-4K 虽然引入了小波损失，但 UltraFlux 的 SNR-Aware Huber Wavelet 损失进一步将鲁棒性、频率感知和时间步平衡统一在单一目标中，消融实验证实其相较于标准 L2 损失在所有指标上均有提升。

**与闭源商业系统的对比。** 在闭源阵营中，**Seedream 4.0**（ByteDance, 2025）代表了当前多宽高比原生 4K 生成的最高工程化水平。UltraFlux 在配合 GPT-4o 提示精炼器后，在 HPSv3 上达到 12.03，略超 Seedream 4.0 的 11.98（Table 5），但需注意这一对比的公平性受限于提示处理流程的不完全一致。Gemini-2.5-Flash 偏好评估显示，UltraFlux 在视觉吸引力上被偏好比例为 70–82%，在提示对齐上为 60–89%（Figure 5），表明其在人类主观评价层面已具备与闭源系统竞争的能力。

### 2. 适用边界与局限

尽管 UltraFlux 在多个基准上取得了领先结果，其适用边界和局限性同样明确。

**计算资源门槛高。** 即使使用 F16 VAE 和优化的 DiT，50–60 步的 4K 生成仍需高端 GPU（约 50GB 显存），推理延迟相较于 1K 模型显著偏高（Table 10 提供了推理时间对比）。这限制了其在消费级硬件上的大规模推广，也意味着实时交互式应用场景尚不可行。

**美学质量并非全域最优。** 在困难案例中，UltraFlux 仍可能出现过度平滑的纹理、微小的几何伪影或不如工程化闭源系统精致的构图。阶段性美学课程学习（SACL）虽然在高噪声步集中了高美学监督，但这一策略的有效性依赖于高质量美学数据的覆盖范围，对于数据稀疏的特定领域可能效果有限。

**协同设计范围受限于单一架构。** 当前协同设计完全围绕 Flux 这一大型 DiT 骨干展开，未探索稀疏/低秩注意力、轻量解码器或知识蒸馏等方向。这意味着模型压缩和加速的潜力尚未被充分挖掘，也限制了该方法向更参数高效架构的迁移。

### 3. 开放问题

从 UltraFlux 的协同设计范式出发，以下几个开放问题值得关注：

1. **架构效率的协同扩展。** 如何将数据–模型协同设计扩展到更参数高效的架构（如稀疏注意力、低秩适配），以显著降低显存占用与推理延迟？当前方法在 50GB 显存门槛下的实用性受限，架构层面的协同优化可能带来数量级的效率提升。

2. **跨域泛化能力。** 该协同设计范式是否能够泛化到专业科学图像、医学影像或卫星遥感等更广泛的数据域？这些领域同样面临高分辨率和多宽高比的挑战，但数据分布和美学标准与自然图像显著不同。

3. **模型压缩与蒸馏路径。** 在保持原生 4K 质量的前提下，能否通过蒸馏或模型压缩技术获得可在消费级 GPU 上运行的版本？这需要探索损失函数设计、位置编码策略与压缩技术之间的协同关系。

4. **动态任务的耦合挑战。** 将舞蹈生成、视频生成等动态任务引入类似的多宽高比-高分辨率协同设计框架是否存在额外的耦合挑战？时间维度的引入将使位置编码、VAE 压缩和优化目标三者的相互作用更加复杂。

5. **数据质量与模型能力的协同上限。** 当前 MultiAspect-4K-1M 数据集规模为 100 万张，进一步扩大数据规模或提升数据质量是否能持续带来模型能力的线性增长？还是存在一个由模型架构决定的协同上限？



## 原文 PDF

![[paperPDFs/CVPR_2026/UltraFlux_Data_Model_Co_Design_for_High_quality_Native_4K_Text_to_Image_Generation_across_Diverse_Aspect_Ratios.pdf]]
