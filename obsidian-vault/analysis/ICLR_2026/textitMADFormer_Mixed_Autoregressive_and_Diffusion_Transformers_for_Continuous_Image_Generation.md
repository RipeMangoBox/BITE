---
title: "$\\textit{MADFormer}$: Mixed Autoregressive and Diffusion Transformers for Continuous Image Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/textitMADFormer_Mixed_Autoregressive_and_Diffusion_Transformers_for_Continuous_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- TMMADTCIG
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "Transformer层中AR层与扩散层的比例分配（即扩散深度D）以及图像块的自回归粒度（AR长度L）。"
primary_logic: "在推理计算受限时，优先分配更多层给AR建模（AR-heavy）能显著提升FID（最高达60-75%）；当计算充足时，扩散层更多的配置（diffusion-heavy）能达到更高保真度。AR提供全局结构先验，扩散负责局部细节精修，两者互补。"
claims:
- "在低NFE（受限计算）下，AR-heavy配置（如3:1 AR:Diffusion，d=7）的FID比diffusion-heavy配置（d=28）降低60-75%。"
- "增加扩散深度（d从7增至28）在FFHQ上FID从20.2降至15.9，在ImageNet上从34.0降至27.4。"
- "FFHQ上最优AR长度为16块（FID 17.8），ImageNet上最优为1块（FID 28.4）。"
- "同时使用clean blocks和AR condition比单独使用任一组件效果更好（FFHQ: 17.8 vs 20.1/19.7）。"
---

# $\textit{MADFormer}$: Mixed Autoregressive and Diffusion Transformers for Continuous Image Generation

> [!tip] 核心洞察
> 在推理计算受限时，优先分配更多层给AR建模（AR-heavy）能显著提升FID（最高达60-75%）；当计算充足时，扩散层更多的配置（diffusion-heavy）能达到更高保真度。AR提供全局结构先验，扩散负责局部细节精修，两者互补。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MADFormer：用于连续图像生成的混合自回归与扩散Transformer |
| 英文题名 | $\textit{MADFormer}$: Mixed Autoregressive and Diffusion Transformers for Continuous Image Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9zUJbyR62q) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MADFormer |
| Dataset | FFHQ-1024, ImageNet 256x256 |

> [!tip] 效果简介
> - FFHQ-1024 上，FID 为 17.8，对比 20.2 (d=7)，变化 -2.4。
> - ImageNet 256x256 上，FID 为 30.0，对比 34.0 (d=7)，变化 -4.0。
> - FFHQ-1024 上，FID (低NFE) 为 ~20 (AR-heavy, d=7, NFE=10)，对比 ~50 (diffusion-heavy, d=28, NFE=10)，变化 60-75% improvement。

## 概要

MADFormer针对现有混合自回归（AR）与扩散（Diffusion）图像生成模型缺乏系统性设计指导的根本瓶颈，提出了一种在Transformer深度轴和图像token轴上同时进行范式混合的架构。其核心发现是：**AR层与扩散层的比例分配（扩散深度D）以及图像块的自回归粒度（AR长度L）是控制生成质量与计算效率权衡的关键因果旋钮**。

在方法定位上，MADFormer并非追求某个基准的全面超越，而是旨在建立一个可系统化分析AR-扩散混合设计空间的框架。与Transfusion、ACDiT、MAR和DiT等基线相比，MADFormer的关键改动包括：1) 将Transformer解码器明确划分为前N-D层（AR条件模块，提供全局结构先验）和后D层（扩散去噪模块，负责局部细节精修）；2) 将图像划分为粗粒度块，块间进行AR建模，块内进行扩散去噪；3) 通过U-Net下采样器将时间步信息直接编码到图像潜变量中，而非注入每一层；4) 为文本、干净图像块和噪声图像块使用独立的参数集（text tower, clean tower, noise tower）；5) 在损失函数中增加隐藏损失（hidden loss）和干净塔损失（clean tower loss）。

主要结果表明，AR与扩散的互补角色在推理计算受限时尤为关键。**在低NFE（受限计算）下，AR-heavy配置（如3:1 AR:Diffusion，d=7）的FID比diffusion-heavy配置（d=28）降低60-75%**（Figure 4）。当计算充足时，增加扩散深度（d从7增至28）在FFHQ上FID从20.2降至15.9，在ImageNet上从34.0降至27.4（Table 1），但收益递减。最优AR长度呈现数据集依赖性：FFHQ上为16块（FID 17.8），ImageNet上为1块（FID 28.4）（Table 2）。同时使用clean blocks和AR condition比单独使用任一组件效果更好（FFHQ: 17.8 vs 20.1/19.7）（Table 3）。隐藏损失系数为0.1时，FID从19.4降至17.8（Section 4.6）。需要说明的是，ImageNet上的FID（30.0）较高是由于训练epoch数远少于基线（50 vs 400/800）且未使用classifier-free guidance (CFG)，作者明确表示这是为了控制变量分析设计空间而非追求SOTA。



连续图像生成的主流范式分为自回归（AR）模型与扩散模型，但两种范式在结构先验与局部细节精修上存在天然互补性。AR模型通过逐token预测捕获全局依赖，但在高分辨率场景下推理步数随序列长度线性增长；扩散模型通过迭代去噪生成精细纹理，但低步数下结构一致性差。现有混合AR-扩散模型（如Transfusion, ACDiT）虽然尝试融合两者，但缺乏系统性的设计指导，不清楚如何在两种范式之间分配模型容量以平衡生成质量与计算效率——这是当前领域的关键瓶颈。

MADFormer的核心动机正是填补这一空白：通过解耦Transformer深度方向上的AR层与扩散层比例，以及token轴上的图像块划分粒度，系统性地探索“AR提供全局结构先验，扩散负责局部细节精修”这一互补机制的最优配置。其因果控制旋钮有两个：（1）扩散深度D，即Transformer解码器后半部分用于扩散去噪的层数；（2）AR长度L，即图像被划分为粗粒度块的数量，块间AR建模、块内扩散去噪。

实验证据清晰地揭示了计算约束下的最优分配规律：在低NFE（推理步数受限）场景下，AR-heavy配置（如AR:扩散=3:1，d=7）的FID比diffusion-heavy配置（d=28）降低60-75%（Figure 4）；而当计算充足时，扩散层更多的配置能达到更高保真度（FFHQ上d从7增至28，FID从20.2降至15.9；ImageNet上从34.0降至27.4，Table 1）。此外，FFHQ上最优AR长度为16块（FID 17.8），ImageNet上最优为1块（FID 28.4，Table 2），表明最优粒度与数据集的结构复杂度相关。

现有基线（Transfusion, ACDiT, MAR, DiT）均未系统探索这一层分配与块划分的设计空间。MADFormer的独特设计包括：将时间步信息通过U-Net下采样器直接编码到图像潜变量中（而非每层adaLN注入），以及为文本、干净图像块、噪声图像块使用独立的参数集（text tower, clean tower, noise tower）。这些设计选择并非随意堆砌——消融实验（Table 3, Table 6）表明，同时使用clean blocks和AR条件比单独使用任一组件效果更好（FFHQ: 17.8 vs 20.1/19.7），隐藏损失系数0.1时FID从19.4降至17.8，说明辅助损失对训练动态有实质改善。

需要指出的是，该工作的动机强度受限于实验范围：所有实验在1.3B/2.1B模型规模下进行，未探索规模对AR-扩散权衡的影响；ImageNet上FID 30.0远低于SOTA（训练epoch仅50 vs 400-800，且未使用CFG），作者明确说明这是为了控制变量分析设计空间而非追求SOTA。因此，当前证据强有力地支持“计算受限时优先分配AR层”这一设计原则，但该原则在不同模型规模、不同数据集（特别是文本到图像场景）下的泛化性仍需手动验证。



## 核心方法与创新机理

MADFormer的核心创新在于将Transformer的深度轴和图像token的序列轴同时进行混合建模，并通过系统性的消融实验揭示了AR与扩散范式之间容量分配的计算权衡规律。

**深度轴上的AR-扩散分层混合。** 与Transfusion、ACDiT等基线将所有层同时用于AR和扩散不同，MADFormer将Transformer解码器堆栈明确划分为两个阶段：前N-D层作为AR条件模块，单向处理已生成的图像块以计算全局结构先验；后D层作为扩散去噪模块，在条件表示和噪声块输入上执行迭代精修。这一设计将AR的全局结构建模能力与扩散的局部细节修复能力在深度维度上解耦。核心发现（Figure 4）是：在推理计算受限（低NFE）时，AR-heavy配置（如AR:扩散=3:1，d=7）的FID比扩散-heavy配置（d=28）降低60-75%；而计算充足时，扩散-heavy配置能达到更高保真度。这表明AR层提供高效的全局结构先验，扩散层则负责精细纹理修复，两者互补。

**token轴上的粗粒度块划分。** 与逐token的AR建模（如MAR）或全局扩散（如DiT）不同，MADFormer将图像潜变量划分为粗粒度块（如FFHQ 1024×1024上划分为16个块，每块256×256个patch），块间进行AR建模，块内应用扩散目标。消融实验（Table 2）显示最优AR长度高度依赖数据集：FFHQ上16块最优（FID 17.8），ImageNet上1块（即无块划分）最优（FID 28.4）。这暗示块划分策略与图像的结构化程度相关——人脸具有强全局结构，需要更多AR步骤来捕获空间依赖；而ImageNet的多样化类别可能受益于更少的块间约束。

**创新的时间步信息注入方式。** 与DiT通过adaLN或cross-attention将时间步注入每个Transformer层不同，MADFormer通过U-Net下采样器将时间步信息直接编码到图像潜变量中。这避免了在每一层重复注入时间信息，减少了计算开销，但论文未提供直接消融实验证明该设计相对于adaLN的优势。

**独立参数集与辅助损失设计。** 所有模态共享Transformer骨干，但文本、干净图像块、噪声图像块使用独立的FFN、QKVO投影和层归一化参数（text tower, clean tower, noise tower）。消融（Table 4）显示该设计在FFHQ上无影响，在ImageNet上略有改善（FID 30.4 vs 30.0）。更关键的是损失函数创新：在标准文本NLL和图像MSE之外，增加了隐藏损失（hidden loss）和干净塔损失（clean tower loss）。隐藏损失迫使AR条件表示逼近真实图像块，系数0.1时FID从19.4降至17.8（Table 6）。此外，消融（Table 5）表明序列级因果注意力在扩散层中不可替代——替换为MLP导致ImageNet FID从30.0急剧恶化至96.5。

**与基线的关键差异总结。** 相对Transfusion（全层混合AR-扩散）、DiT（纯扩散）、MAR（纯AR），MADFormer的changed slots包括：（1）层分配：从全部层用于单一范式变为前N-D层AR、后D层扩散；（2）图像块处理：从全局扩散或逐token AR变为块间AR+块内扩散；（3）时间步注入：从每层adaLN变为U-Net下采样器直接编码；（4）参数集：从全共享变为模态独立参数集；（5）损失函数：增加隐藏损失和干净塔损失。这些设计的核心瓶颈在于缺乏系统性的AR-扩散容量分配指导——MADFormer通过消融实验首次揭示了这一权衡的定量规律。



![[assets/figures/papers/iclr26_0001_9zUJbyR62q_textitMADFormer_Mixed_Autoregressive_and_Diffusi/figures/001_Figure_1.jpg]]
*Figure 1: High-level overview of the MADFormer architecture. A single Transformer processes all modalities as a unified sequence. Text tokens follow a next-token prediction objective, while image tokens are grouped into blocks trained autoregressively with a diffusion objective. We use separate parameters (FFNs, QKVO projections, and layer norms) for each modality. The Transformer is divided into two stages: early layers produce conditions from text and image blocks; later layers denoise noisy image blocks. Each block attends to itself and preceding clean blocks*

MADFormer的整体pipeline将图像生成建模为一个统一序列上的混合过程，其核心设计沿两个正交轴划分模型容量：**token轴**上的粗粒度块划分与**深度轴**上的AR/扩散层分配。

**输入与编码阶段。** 文本输入经由Llama 3分词器转换为离散token序列。图像通过Stable Diffusion VAE映射到连续潜空间，然后被划分为粗粒度块（例如，对1024×1024的潜变量网格划分为16个块，每块包含256×256个patch）。时间步信息通过U-Net下采样器直接编码到图像潜变量中，而非像DiT那样通过adaLN注入每一层。

**Transformer主干与双阶段处理。** 整个解码器堆栈被概念性地分为两个阶段（Figure 1）。前N-D层构成**AR条件模块**：这些层以自回归方式运行，处理已生成的图像块（及其位置编码嵌入），为下一个待生成块计算条件表示 $\mathbf{z}_{\mathrm{cond}}$。后D层构成**扩散去噪模块**：接收加噪的潜变量 $\mathbf{z}_{\mathrm{noisy}}$（由 $\mathbf{z}_{\mathrm{image}}$ 经扩散前向过程采样得到）与条件表示 $\mathbf{z}_{\mathrm{cond}}$ 的加和作为输入，执行递归去噪。这种设计使AR层提供全局结构先验（一次前向通过即可），而扩散层负责局部细节精修（需要迭代计算）。

**模态特定的参数集。** 所有模态共享同一个Transformer骨干，但使用独立的参数集进行处理：文本塔（text tower）、干净图像块塔（clean tower）和噪声图像块塔（noise tower）。每个塔包含独立的FFN、QKVO投影和层归一化。这种设计允许不同模态学习各自的特征表示，消融实验（Table 4）显示其在ImageNet上略有改善（FID 30.4→30.0），在FFHQ上无影响。

**输出与损失函数。** 去噪后的潜变量经U-Net上采样器映射回图像空间。总损失为四项的加权和：文本NLL（交叉熵）、图像MSE（预测噪声与真实噪声）、隐藏损失（条件表示与真实图像的MSE）和干净塔损失（干净塔输出与真实图像的MSE）。隐藏损失系数为0.1时效果最佳（FID从19.4降至17.8，Table 6），干净塔损失在当前配置下权重设为0。

**推理流程。** 推理时，模型按块顺序生成：对于每个新块，AR条件模块基于所有已生成块计算条件表示，然后扩散去噪模块从纯噪声开始迭代去噪（默认250步，线性beta调度0.0001→0.02）。不同AR/扩散层比例导致不同的计算-质量权衡——AR-heavy配置在低NFE（受限计算）下FID降低60-75%，而diffusion-heavy配置在计算充足时达到更高保真度（Figure 4）。



### 1. 整体架构：双轴混合设计

MADFormer的核心创新在于沿两个正交轴混合自回归（AR）与扩散建模：

- **深度轴（Depth Axis）**：将Transformer解码器堆栈划分为前 `N-D` 层的AR条件模块与后 `D` 层的扩散去噪模块。AR层对已生成的图像块进行一次性前向处理，为下一块计算全局条件先验；扩散层在条件表示和噪声块输入上执行迭代去噪。
- **标记轴（Token Axis）**：将图像在潜空间划分为粗粒度块（例如，对于1024×1024潜变量图像，划分为16个256×256块的块）。块间采用AR建模（逐块生成），块内采用扩散目标。

这种设计的关键洞察是：AR提供全局结构先验，扩散负责局部细节精修，两者互补。推理计算受限时，优先分配更多层给AR建模（AR-heavy）能显著提升FID（最高达60-75%）；当计算充足时，扩散层更多的配置（diffusion-heavy）能达到更高保真度（Figure 4）。

### 2. 核心公式体系

#### 2.1 基础范式公式

**自回归分解**（Section 2.1）：
$$p(x) = \prod_{i=1}^n p(x_i | x_{1:i-1})$$
图像序列的联合概率分解为逐token的条件概率乘积。

**扩散前向过程采样**（Section 2.2）：
$$x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, I)$$
从干净数据 $x_0$ 直接采样 $t$ 时刻的噪声潜变量，其中 $\bar{\alpha}_t = \prod_{s=1}^t (1 - \beta_s)$ 是噪声调度的累积乘积。

**扩散训练损失**（Section 2.2）：
$$\mathbb{E}_{t, x_0, \varepsilon} \| \varepsilon_\theta(x_t, t, z) - \varepsilon \|^2$$
预测噪声与真实噪声之间的均方误差，以可选条件 $z$ 为输入。

**反向扩散**（Section 2.2）：
$$p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t, z), \sigma_t^2 I)$$
以条件 $z$ 为输入的高斯反向步。

#### 2.2 MADFormer特定公式

**AR条件嵌入**（Section 3.2, Eq. (1)）：
$$\mathbf{h}_0 = \mathtt{Embed}(\mathbf{z}_{\mathrm{prev}}) + \mathtt{PosEnc}$$
前一块的嵌入加上位置编码，作为AR条件阶段的初始输入。

**AR条件层递归**（Section 3.2, Eq. (2)）：
$$\mathbf{h}_i = \mathtt{DecoderBlock}_i(\mathbf{h}_{i-1}), \quad i = 1, \dots, N-D$$
AR条件阶段的解码器块递归应用，$N$ 为总层数，$D$ 为扩散层数。

**条件表示**（Section 3.2, Eq. (3)）：
$$\mathbf{z}_{\mathrm{cond}} = \mathbf{h}_{N-D}$$
AR条件阶段的输出，作为后续扩散去噪模块的条件先验。

**噪声潜变量注入**（Section 3.2, Eq. (4)）：
$$\mathbf{h}_{N-D} = \sqrt{\bar{\alpha}_t} \mathbf{z}_{\mathrm{image}} + \sqrt{1 - \bar{\alpha}_t} \epsilon + \mathbf{z}_{\mathrm{cond}}$$
加噪的真实潜变量加上条件表示，作为扩散去噪阶段的输入。时间步信息通过U-Net下采样器直接编码到图像潜变量中，而非通过adaLN或cross-attention注入每个Transformer层。

**总损失函数**（Section 3.2, Eq. (6)）：
$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{text}} \cdot (-\log p(\mathbf{y}_{\mathrm{text}} \mid \mathbf{x})) + \lambda_{\mathrm{image}} \cdot \left\| \hat{\mathbf{z}}_{\mathrm{image}} - \mathbf{z}_{\mathrm{image}} \right\|_2^2 + \lambda_{\mathrm{hidden}} \cdot \left\| \mathbf{z}_{\mathrm{condition}} - \mathbf{z}_{\mathrm{image}} \right\|_2^2 + \lambda_{\mathrm{tower}} \cdot \left\| \mathbf{z}_{\mathrm{clean}} - \mathbf{z}_{\mathrm{image}} \right\|_2^2$$

四个损失项的加权和：
- **文本NLL**：文本token的负对数似然
- **图像MSE**：预测图像潜变量与真实值的均方误差
- **隐藏损失**：条件表示与真实图像潜变量的均方误差，迫使条件表示包含更多图像信息
- **干净塔损失**：干净塔输出与真实图像潜变量的均方误差

### 3. 关键消融实验与公式变量含义

#### 3.1 扩散深度 $D$ 的影响（Table 1）

扩散深度 $D$（即后 $D$ 层用于扩散去噪）是核心控制变量：
- 增加 $D$ 持续改善FID：FFHQ上从 $d=7$ 的20.2降至 $d=28$ 的15.9；ImageNet上从34.0降至27.4
- 收益递减：从 $d=7$ 到 $d=14$ 改善最大，从 $d=14$ 到 $d=28$ 改善幅度减小
- 默认配置为 $d=14$（总层数 $N=28$），即AR层与扩散层比例为1:1

#### 3.2 AR长度 $L$ 的影响（Table 2）

AR长度 $L$ 表示图像被划分为多少块（每个块包含256个token）：
- FFHQ上最优为 $L=16$（FID 17.8），即每块256个token
- ImageNet上最优为 $L=1$（FID 28.4），即无块划分，全局扩散
- 这表明最优块划分策略与数据集特征高度相关：高分辨率人脸图像受益于块级AR先验，而多样化的ImageNet类别可能不需要强结构先验

#### 3.3 损失函数系数消融（Table 6）

隐藏损失系数 $\lambda_{\mathrm{hidden}}$ 的最佳值为0.1（FID从19.4降至17.8），过大或过小均有害。干净塔损失系数 $\lambda_{\mathrm{tower}}$ 在FFHQ上设为0.0（无影响），在ImageNet上设为0.1略有改善（FID 30.4 vs 30.0）。

#### 3.4 注意力机制的必要性（Table 5）

将扩散层中的序列级因果注意力替换为MLP导致生成质量严重下降：ImageNet上FID从30.0升至96.5，FFHQ上从17.8升至21.2。这表明序列级因果注意力在扩散去噪过程中至关重要，MLP无法捕获块内token间的依赖关系。

### 4. 参数集设计

所有模态共享Transformer骨干网络，但使用独立的参数集（tower）处理不同模态（Section 3.1）：
- **文本塔（text tower）**：处理文本token
- **干净塔（clean tower）**：处理已生成的干净图像块
- **噪声塔（noise tower）**：处理噪声图像块

每个tower包含独立的FFN、QKVO投影和层归一化。消融实验（Table 4）表明，独立参数集在FFHQ上无影响（FID 17.8 vs 17.8），在ImageNet上略有改善（FID 30.0 vs 30.4），说明参数集共享的可行性取决于数据集复杂度。

### 5. 公式变量含义汇总

| 变量 | 含义 | 典型值/范围 |
|------|------|-------------|
| $N$ | Transformer总层数 | 28 |
| $D$ | 扩散去噪层数（后D层） | 7, 14, 28 |
| $L$ | AR块数（每个块256个token） | 1, 4, 8, 16 |
| $\bar{\alpha}_t$ | 噪声调度累积乘积 | 线性调度 0.0001→0.02 |
| $\lambda_{\mathrm{text}}$ | 文本NLL损失权重 | 未明确报告 |
| $\lambda_{\mathrm{image}}$ | 图像MSE损失权重 | 5.0 |
| $\lambda_{\mathrm{hidden}}$ | 隐藏损失权重 | 0.1 |
| $\lambda_{\mathrm{tower}}$ | 干净塔损失权重 | 0.0 (FFHQ), 0.1 (ImageNet) |
| $\mathbf{z}_{\mathrm{cond}}$ | AR条件模块输出 | 维度=1024 |
| $\mathbf{z}_{\mathrm{image}}$ | 真实图像潜变量 | VAE编码输出 |



## 实验与关键发现

### 核心发现：AR与扩散层的计算预算分配

MADFormer的核心瓶颈在于缺乏系统性的设计指导来在自回归（AR）层与扩散层之间分配模型容量，以平衡生成质量与计算效率。实验揭示的关键因果旋钮是Transformer中AR层与扩散层的比例（扩散深度D）以及图像块的自回归粒度（AR长度L）。

**决定性证据**来自Figure 4：在低NFE（受限推理计算，如10步）下，AR-heavy配置（例如AR:扩散层比例为3:1，对应d=7）的FID比diffusion-heavy配置（d=28）降低60-75%。这表明当计算预算紧张时，优先将容量分配给AR建模能显著提升生成质量，因为AR层提供全局结构先验，而扩散层负责局部细节精修，在步数不足时结构先验的缺失比细节缺失更致命。随着计算预算增加（NFE增大），diffusion-heavy配置逐渐反超，达到更高保真度。

### 消融实验：扩散深度与AR长度

Table 1系统性地展示了扩散深度d的影响：在FFHQ-1024上，d从7增至28时FID从20.2降至15.9；在ImageNet 256×256上，FID从34.0降至27.4。收益呈现递减趋势——从d=7到d=14的改善幅度大于从d=14到d=28。这表明存在一个“足够”的扩散深度，超过该点后增加扩散层对质量的边际贡献下降。


![[assets/figures/papers/iclr26_0001_9zUJbyR62q_textitMADFormer_Mixed_Autoregressive_and_Diffusi/figures/007_Table_1.jpg]]
*Table 1: Ablation on diffusion depth. All models in our experiments are trained for and 210k steps on FFHQ, and 250k steps (50 epochs) on ImageNet*

AR长度的消融（Table 2）揭示了数据集依赖的最优配置：FFHQ上最优AR长度为16块（FID 17.8），而ImageNet上最优为1块（即无块划分，FID 28.4）。这一差异的机制在于：FFHQ人脸图像具有高度结构化的全局布局（五官位置相对固定），粗粒度块间AR建模能有效捕获这种结构先验；而ImageNet的200+类别包含多样化的物体形状和布局，过大的块粒度反而限制了模型对局部细节的建模能力。


![[assets/figures/papers/iclr26_0001_9zUJbyR62q_textitMADFormer_Mixed_Autoregressive_and_Diffusi/figures/009_Table_2.jpg]]
*Table 2: Ablation on AR length*

### 设计组件消融：关键贡献因素

**Clean blocks与AR condition的协同效应**（Table 3）：同时使用两者比单独使用任一组件效果更好（FFHQ: 17.8 vs 20.1/19.7）。单独移除AR condition（即不使用早期AR层生成的条件表示）导致FID从17.8恶化至20.1，表明AR提供的全局结构先验不可或缺；单独移除clean blocks（即不使用已生成的干净图像块作为注意力参考）导致FID恶化至19.7，说明扩散层需要访问已生成块的干净特征来维持一致性。


![[assets/figures/papers/iclr26_0001_9zUJbyR62q_textitMADFormer_Mixed_Autoregressive_and_Diffusi/figures/008_Table_3.jpg]]
*Table 3: Ablation on clean blocks and AR condition*

**参数集共享策略**（Table 4）：使用独立参数集（text/clean/noise tower）在FFHQ上无影响（FID 17.8 vs 17.8），在ImageNet上略有改善（FID 30.0 vs 30.4）。这表明在数据多样性较低时，共享参数足以建模不同模态；而在数据多样性高时，独立的参数集能更好地处理文本、干净图像块和噪声图像块之间的分布差异。


![[assets/figures/papers/iclr26_0001_9zUJbyR62q_textitMADFormer_Mixed_Autoregressive_and_Diffusi/figures/010_Table_4.jpg]]
*Table 4: Ablation on param sets*

**序列级因果注意力的必要性**（Table 5）：用MLP替换扩散层中的序列级因果注意力导致生成质量严重下降——ImageNet上FID从30.0飙升至96.5。这证明扩散去噪过程中，不同图像块之间的注意力交互是维持全局一致性的关键机制，简单的逐块独立去噪（MLP）无法捕获块间依赖关系。


![[assets/figures/papers/iclr26_0001_9zUJbyR62q_textitMADFormer_Mixed_Autoregressive_and_Diffusi/figures/011_Table_5.jpg]]
*Table 5: Ablation on MLP denoising*

**损失函数设计**（Table 6）：隐藏损失（hidden loss）系数为0.1时效果最佳（FID 17.8），过大或过小均有害。隐藏损失强制AR条件模块的输出与真实图像块在潜空间对齐，为扩散去噪提供更准确的初始条件。干净塔损失（clean tower loss）的贡献较小，说明其与隐藏损失存在功能重叠。

### 失败模式与注意事项

1. **ImageNet上的性能瓶颈**：当前FID为30.0，远高于SOTA（如DiT在完全训练后可达到10以下）。作者明确指出这是由于训练epoch数远少于基线（50 vs 400/800）且未使用classifier-free guidance (CFG)。因此，当前结果反映的是设计空间分析而非模型上限。

2. **推理计算量与训练计算量的权衡**：所有消融实验在相同训练步数下进行，但不同配置的推理计算量（NFE）不同。AR-heavy配置在低NFE下占优，但需要更多训练步数来充分学习AR建模。论文未报告训练计算成本（总FLOPs或训练时间），因此无法判断在固定训练预算下最优配置是否与推理预算下的最优配置一致。

3. **评估范围限制**：实验仅在类条件生成（FFHQ和ImageNet）上进行，未在标准文本到图像（T2I）基准上评估。此外，未与最新的纯扩散模型（如Flux）或纯AR模型（如MAR完全训练后）进行直接比较。

4. **统计可靠性**：消融实验中的FID仅通过最后5个检查点平均来降低噪声，未报告标准差或置信区间，限制了结果的统计显著性判断。


## 定位与知识库关联

### 与基线方法的关系

MADFormer 在混合 AR-扩散生成范式上构建，直接继承自 **Transfusion** (Zhou et al., 2024) 和 **ACDiT** (Hu et al., 2024) 的设计思路，同时引入了来自 **MAR** (Li et al., 2024) 的连续空间自回归思想和 **DiT** (Peebles & Xie, 2022) 的扩散 Transformer 架构。其核心贡献在于揭示了此前混合模型中被忽视的关键设计维度：**Transformer 深度轴上 AR 层与扩散层的比例分配**，以及**图像块的自回归粒度**。

与基线相比，MADFormer 改变了五个关键槽位：

1. **层分配策略**：从“全部层用于扩散（如 DiT）”或“全部用于 AR”的极端配置，变为“前 N-D 层为 AR 条件模块，后 D 层为扩散去噪模块”的分阶段架构。
2. **图像块处理方式**：从全局扩散或逐 token AR，变为“块间 AR 建模 + 块内扩散去噪”的粗粒度块划分策略。
3. **时间步信息注入**：从通过 adaLN 或 cross-attention 注入每个 Transformer 层，变为通过 U-Net 下采样器直接编码到图像潜变量中。
4. **参数集共享**：从所有模态共享同一参数集，变为文本、干净图像块、噪声图像块使用独立参数集（text tower, clean tower, noise tower）。
5. **损失函数**：从仅文本 NLL + 图像 MSE，增加隐藏损失（hidden loss）和干净塔损失（clean tower loss）。

### 适用边界与条件

MADFormer 的设计空间探索揭示了明确的适用边界条件：

**计算资源约束**：这是最关键的边界。当推理计算受限（NFE 低）时，AR-heavy 配置（如 3:1 AR:Diffusion，d=7）的 FID 比 diffusion-heavy 配置（d=28）降低 **60-75%**（Figure 4）。当计算充足时，扩散层更多的配置能达到更高保真度。这意味着：
- **低计算预算场景**（如移动端、实时推理）：应优先分配更多层给 AR 建模
- **高计算预算场景**（如云端、高质量生成）：应增加扩散层比例

**数据集特性**：最优 AR 长度（块数）高度依赖数据集。FFHQ 上最优为 16 块（FID 17.8），而 ImageNet 上最优为 1 块（即无块划分，FID 28.4）（Table 2）。这暗示：
- 结构规整的数据集（人脸）受益于更细粒度的块划分
- 内容多样的数据集（自然图像）可能不需要块划分

**训练约束**：论文明确指出 ImageNet 上 FID 较高（30.0）是由于训练 epoch 数远少于基线（50 vs 400/800）且未使用 classifier-free guidance (CFG)。当前结果不代表模型上限，而是为了控制变量分析设计空间。

### 局限

1. **评估范围受限**：论文仅在类条件生成任务上评估，未在标准文本到图像（T2I）基准上测试，也未与最新的纯扩散模型（如 Flux）或纯 AR 模型（如 MAR 完全训练后）进行直接比较。
2. **规模探索不足**：所有实验在固定模型大小（1.3B/2.1B）下进行，未探索模型规模参数如何影响最优 AR/扩散比例。
3. **统计严谨性缺失**：消融实验中的 FID 仅通过最后 5 个检查点平均来降低方差，未报告标准差或置信区间。不同配置的推理计算量（NFE）不同，比较时需注意。
4. **训练成本未分析**：未报告不同配置下的总 FLOPs 或训练时间对比，无法判断计算公平性。

### 开放问题

1. **训练预算 vs 推理预算的权衡**：如何根据训练预算（而非仅推理预算）动态调整 AR/扩散层比例？当前框架仅针对推理计算受限场景给出了指导。
2. **块划分策略的泛化性**：块划分策略如何随图像分辨率、架构和数据集特征变化？FFHQ 与 ImageNet 的最优 AR 长度差异表明这一维度需要更系统的研究。
3. **T2I 和 OOD 组合性任务**：将评估扩展到文本到图像和分布外组合性任务，在相同受限计算设置下表现如何？
4. **自适应损失权重**：固定超参数的损失加权能否被自适应策略替代以改善训练动态？
5. **高级采样技术的整合**：将 DPM-Solver 等高级采样技术与本文的容量分配指导相结合，能否在极低 NFE 下达到更好效果？
6. **规模效应**：模型规模（参数数量）如何影响最优 AR/扩散比例？更大模型是否倾向于需要更多扩散层？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/textitMADFormer_Mixed_Autoregressive_and_Diffusion_Transformers_for_Continuous_Image_Generation.pdf

![[paperPDFs/ICLR_2026/textitMADFormer_Mixed_Autoregressive_and_Diffusion_Transformers_for_Continuous_Image_Generation.pdf]]
