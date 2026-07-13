---
title: "NextStep-1: Toward Autoregressive Image Generation with Continuous Tokens at Scale"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/NextStep_1_Toward_Autoregressive_Image_Generation_with_Continuous_Tokens_at_Scale.pdf
project_link: https://stepfun-ai.github.io/NextStep-1/nextstep_1p1_blog/
code_link: https://github.com/stepfun-ai/NextStep-1
openreview_forum_id: Ndnwg9oOQO
aliases:
- N1
- NextStep-1
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "图像标记器的逐令牌归一化（token-wise normalization）和受控噪声注入（noise perturbation），这两个设计直接正则化隐空间，使自回归Transformer在任意CFG引导下均能稳定生成。"
primary_logic: "自回归图像生成的成功不仅依赖于高重建质量，更关键的是构建一个正则化良好的隐空间：通过逐令牌归一化和噪声正则化，可以显著提高标记器隐空间的分散性和对扰动的鲁棒性，从而使大型语言模型可以通过简单的流匹配头执行高质量的逐块生成。"
claims:
- "在高CFG(3.0)下，无归一化时逐令牌均值与方差显著漂移，导致图像质量退化；加入逐令牌归一化后分布保持稳定。"
- "流匹配头大小（40M到528M）对生成指标（GenEval, GenAI-Bench, DPG-Bench）影响极小，表明Transformer主干而非流匹配头承担核心生成建模。"
- "在标记器训练中引入更高噪声（γ=0.5）虽然增加生成损失，却显著提升生成图像保真度，表明噪声正则化对生成有利。"
- "NextStep-1的VAE隐分布更接近标准正态分布，反映正则化效果，相比Flux.1-dev VAE和NextStep-1 VAE w/o Noise。"
---

# NextStep-1: Toward Autoregressive Image Generation with Continuous Tokens at Scale

> [!tip] 核心洞察
> 自回归图像生成的成功不仅依赖于高重建质量，更关键的是构建一个正则化良好的隐空间：通过逐令牌归一化和噪声正则化，可以显著提高标记器隐空间的分散性和对扰动的鲁棒性，从而使大型语言模型可以通过简单的流匹配头执行高质量的逐块生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | NextStep-1：面向大规模连续令牌自回归图像生成 |
| 英文题名 | NextStep-1: Toward Autoregressive Image Generation with Continuous Tokens at Scale |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Ndnwg9oOQO) · [GitHub](https://github.com/stepfun-ai/NextStep-1) · [Project](https://stepfun-ai.github.io/NextStep-1/nextstep_1p1_blog/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | NextStep-1 |
| Dataset | OneIG-Bench (Overall), GenAI-Bench Basic, GEdit-Bench-EN (G.O), WISE Overall |

> [!tip] 效果简介
> - OneIG-Bench (Overall) 上，平均分数 为 0.417，对比 Emu3: 0.311，变化 +0.106。
> - GenAI-Bench Basic 上，准确率 为 0.90 (with Self-CoT)，对比 Janus-Pro-7B: 0.86，变化 +0.04。
> - GEdit-Bench-EN (G.O) 上，GPT-4.1评分 为 6.58，对比 OmniGen2: 6.41，变化 +0.17。

## 概要

**NextStep-1** 是一个 14B 参数的自回归模型，搭配一个 157M 的流匹配头，在离散文本令牌和连续图像令牌上以“下一令牌预测”目标进行训练。该工作直面自回归图像生成的一个关键瓶颈：基于 VAE 的连续自回归模型在高分类器自由引导（CFG）尺度下容易出现灰度斑块等视觉伪影，其根本原因是逐令牌的统计分布漂移，而非 1D 位置嵌入的不连续性。

**核心洞察**在于：自回归图像生成的成功不仅依赖于高重建质量，更关键的是构建一个正则化良好的隐空间。通过**逐令牌归一化**（token-wise normalization）和**受控噪声注入**（noise perturbation），可以显著提高标记器隐空间的分散性和对扰动的鲁棒性，从而使大型语言模型能够通过简单的流匹配头执行高质量的逐块生成。

**方法定位**上，NextStep-1 采用因果 Transformer（从 Qwen2.5-14B 初始化解码器）处理文本与图像令牌序列，图像令牌由经过逐令牌归一化和噪声正则化的 NextStep-VAE 编码为 16 通道连续隐变量。生成头是一个轻量级的流匹配 MLP（157M），将 Transformer 隐藏状态转换为连续令牌的速度向量。该设计区别于离散自回归模型（如 **Emu3**, Wang et al., 2024b；**Janus-Pro-7B**, Chen et al., CVPR 2025b）的 VQ 标记方案，也不同于混合架构（如 **BAGEL**, Deng et al., 2025）的 LLM+扩散组合。

**主要结果**：NextStep-1 在 OneIG-Bench 上以 0.417 的平均分数显著超过 Emu3（0.311）；在 GenAI-Bench Basic 上达到 0.90（使用 Self-CoT），优于 Janus-Pro-7B 的 0.86；在 GEdit-Bench-EN 图像编辑任务上获得 6.58 分，超过 OmniGen2 的 6.41；在 WISE 世界知识推理上以 0.54 的正确率优于 BAGEL 的 0.52。消融实验表明，流匹配头大小（40M 至 528M）对生成指标影响极小，证实 Transformer 骨干承担了核心生成建模；逐令牌归一化在高 CFG 下稳定了分布；标记器训练中更高的噪声强度虽降低重建指标，却显著提升生成保真度。

**局限性**：高维连续令牌可能产生局部噪声和网格状伪影；自回归解码的串行性导致推理延迟较高；高分辨率训练收敛慢；SFT 在小数据集上易过拟合。

### 自回归图像生成的范式演进

图像生成领域长期由扩散模型主导，但自回归模型在语言建模中的成功正推动其向视觉生成延伸。自回归生成的核心思想是将多模态序列分解为条件概率的连乘：

$$p ( x ) = \prod _ { i = 1 } ^ { n } p ( x _ { i } \mid x _ { < i } )$$

这一框架天然支持文本与图像的统一建模，使大型语言模型（LLM）能够同时处理离散文本令牌和图像令牌。然而，现有自回归图像生成方法在令牌表示上存在根本分歧。

### 离散令牌路线的局限

以 **Emu3**（Wang et al., 2024b）和 **Janus-Pro-7B**（Chen et al., CVPR 2025b）为代表的离散自回归模型，依赖矢量量化（VQ）将图像压缩为离散令牌。这种方案虽可直接复用LLM的交叉熵训练范式，但面临两个结构性瓶颈：一是VQ训练中的码本坍塌和梯度近似问题导致训练不稳定；二是离散化过程不可避免的信息损失限制了高保真重建的上限。

### 连续令牌路线的未解难题

连续自回归模型绕过离散化瓶颈，直接在连续隐空间中进行逐令牌预测，理论上能保留更丰富的视觉信息。然而，这一路线在实践中遭遇严重障碍：

**核心瓶颈：高CFG下的分布漂移与视觉伪影。** 分类器自由引导（CFG）是提升生成质量的关键技术，但在连续自回归模型中，当CFG尺度增大时，逐令牌的统计分布会发生显著漂移——均值偏离0、方差偏离1，直接导致图像中出现灰度斑块等视觉退化。这一现象的根源并非1D位置嵌入的不连续性，而是逐令牌预测过程中缺乏对隐空间分布的显式约束。

**隐空间正则化的缺失。** 现有图像标记器（如Flux.1-dev VAE）在训练时仅关注重建质量，其隐空间缺乏结构化的正则化。这导致两个后果：一是隐分布偏离标准正态分布，使后续的自回归Transformer难以学习稳定的条件分布；二是隐空间对噪声扰动敏感，微小的预测误差会在逐块生成过程中累积放大。

### 本文的核心洞察

NextStep-1的出发点是：**自回归图像生成的成功不仅取决于高重建质量，更关键的是构建一个正则化良好的隐空间。** 具体而言，通过在图像标记器中引入两个简单但关键的设计——逐令牌归一化（token-wise normalization）和受控噪声注入（noise perturbation）——可以显著提高隐空间的分散性和对扰动的鲁棒性。这使得大型语言模型仅需搭配一个轻量级的流匹配头，即可执行高质量的逐块图像生成，而无需复杂的扩散解码器或精心设计的2D位置编码。

这一洞察将问题焦点从“如何设计更强的生成架构”转向“如何为自回归模型准备更友好的表示空间”，为连续令牌自回归图像生成开辟了新的技术路径。

## 核心方法与创新机理

NextStep-1的核心创新在于系统性地重构了连续令牌自回归图像生成的隐空间设计，而非简单地替换生成头或扩大模型规模。其关键洞察是：**自回归图像生成的成功不仅依赖于高重建质量，更关键的是构建一个正则化良好的隐空间**。基于此，NextStep-1提出了三个紧密耦合的设计变更，直接针对现有连续自回归模型在高CFG下的视觉伪影和生成不稳定问题。

### 1. 逐令牌归一化：消除高CFG下的分布漂移

传统VAE标记器采用全局归一化或不做归一化，导致自回归Transformer在高分类器自由引导（CFG）尺度下出现逐令牌统计分布的显著漂移，表现为灰度斑块等视觉伪影。NextStep-1在标记器输出端引入**沿通道维度的逐令牌归一化**（token-wise normalization），核心操作如Algorithm 1所示：

$$\mu = X.mean(\mathrm{dim=-1}, \mathrm{keepdim=True}); \sigma = X.std(\mathrm{dim=-1}, \mathrm{keepdim=True}, \mathrm{unbiased=False}); X_{\mathrm{norm}} = (X - \mu) / (\sigma + \mathrm{eps})$$

这一设计强制每个令牌的隐向量在通道维度上保持零均值、单位方差。消融实验（Figure 3, Section 5.2）提供了决定性证据：在CFG=3.0时，无归一化的模型逐令牌均值与方差发生剧烈漂移，导致图像质量退化；加入逐令牌归一化后，所有CFG设置下隐分布均保持稳定。这从根本上解决了连续自回归模型在强引导下的生成崩溃问题，而非此前文献推测的1D位置嵌入不连续性所致。

### 2. 受控噪声注入：以重建代价换取生成鲁棒性

单纯归一化虽稳定了分布，但标记器隐空间仍缺乏对扰动的鲁棒性。NextStep-1在归一化后注入随机缩放的高斯噪声：

$$\tilde{z} = \operatorname{Normalization}(z) + \alpha \cdot \varepsilon , \quad \alpha \sim \mathcal{U}[0, \gamma] \ \mathrm{and} \ \varepsilon \sim \mathcal{N}(0, I)$$

这一设计与传统VAE训练形成鲜明对比——传统方法追求重建精度最大化，而NextStep-1**主动接受更高的重建损失以换取隐空间的分散性和鲁棒性**。Figure 4的实验清晰展示了这一权衡：标记器训练时采用更高噪声强度（γ=0.5）虽然导致rFID上升、PSNR/SSIM下降，却显著提升了最终生成图像的保真度。Figure A3进一步证实，NextStep-1的VAE隐分布相比Flux.1-dev VAE和NextStep-1 VAE w/o Noise更接近标准正态分布，反映噪声正则化有效增强了隐空间的规整性。这一发现挑战了“重建质量至上”的传统标记器设计范式。

### 3. 轻量流匹配头：将生成建模归还Transformer骨干

NextStep-1采用仅157M参数的MLP作为流匹配头（Flow Matching Head），远小于完整扩散模型或VQ解码器。该头基于Transformer隐藏状态预测目标图像块的速度向量，用于流匹配训练和采样。关键消融实验（Table 5, Section 5.1）表明，流匹配头大小从40M到528M变化时，GenEval、GenAI-Bench、DPG-Bench等生成指标影响极小。Figure 2的定性对比进一步印证了这一结论。这揭示了NextStep-1架构的核心分工：**Transformer骨干承担条件分布$p(x_i | x_{<i})$的核心生成建模，流匹配头仅作为轻量采样器**，类似于语言模型中的LM头。这一设计使得模型可以充分利用预训练LLM（Qwen2.5-14B）的建模能力，同时保持生成头的极简性。

### 设计协同与基线对比

上述三个创新并非孤立存在，而是形成因果闭环：逐令牌归一化确保隐空间统计稳定性，噪声注入增强隐空间对生成过程中扰动的鲁棒性，轻量流匹配头则使Transformer骨干专注于核心生成建模。与现有方法对比：
- 相比**Emu3**（Wang et al., 2024b）等离散自回归模型，NextStep-1避免了VQ的信息损失，同时通过隐空间正则化解决了连续令牌的不稳定问题。
- 相比**BAGEL**（Deng et al., 2025）等混合架构，NextStep-1保持了纯自回归框架的简洁性，无需额外的扩散组件。
- 相比**Flux.1-dev**和**Stable Diffusion 3.5 Large**等扩散模型，NextStep-1证明了自回归模型在统一多模态生成上的潜力，同时保持了1D RoPE的简单有效，未引入2D或多模态位置编码的复杂性。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Ndnwg9oOQO/figures/011_Figure.jpg]]
*Figure: A1: Overview of NextStep-1 in high-fidelity image generation, diverse image editing, and complex free-form manipulation*

NextStep-1 是一个面向多模态生成的统一自回归框架，其核心设计理念是将离散文本与连续图像统一在同一个因果Transformer中进行逐令牌建模。

**整体架构** 由三个紧密协作的模块构成：

1. **图像标记器（NextStep-VAE）**：将输入图像编码为 $32\times32\times16$ 的连续隐变量。该标记器从Flux.1-dev VAE微调而来，关键创新在于对每个令牌沿通道维度执行逐令牌归一化（token-wise normalization），并注入缩放高斯噪声 $\alpha \cdot \varepsilon$（其中 $\alpha \sim \mathcal{U}[0, \gamma]$，$\varepsilon \sim \mathcal{N}(0, I)$），以正则化隐空间、防止方差坍塌。这一设计是后续自回归生成稳定性的基础。

2. **因果Transformer主干**：基于 **Qwen2.5-14B** 初始化解码器，采用标准1D RoPE位置编码，自回归地处理由文本令牌和连续图像令牌交错组成的多模态序列。Transformer负责学习序列中所有令牌的条件依赖关系，是生成建模的核心承担者。

3. **双头预测层**：
   - **语言建模头**：对文本令牌输出离散分布，以交叉熵损失 $\mathcal{L}_{\text{text}}$ 进行优化。
   - **流匹配头（157M MLP）**：基于Transformer输出的隐藏状态，预测目标图像块的速度向量 $v_\theta$，以流匹配损失 $\mathcal{L}_{\text{visual}}$ 进行训练。

**训练目标** 为两者的加权和：
$$\mathcal{L}_{\text{total}} = \lambda_{\text{text}} \mathcal{L}_{\text{text}} + \lambda_{\text{visual}} \mathcal{L}_{\text{visual}}$$

**推理流程** 采用逐块自回归生成：因果Transformer每次基于已生成的文本和图像令牌预测下一个图像块的隐藏状态，流匹配头以此为条件，通过多步采样将噪声逐步引导为目标图像块。该过程可结合无分类器引导（CFG）以增强条件控制：
$$\tilde{v}(x|y) = (1 - w) \cdot v_\theta(x|\mathcal{D}) + w \cdot v_\theta(x|y)$$

**后训练阶段** 通过监督微调（SFT，约5M样本）和直接偏好优化（DPO）对齐人类偏好，增强指令遵循与编辑能力。NextStep-1-Edit即在此基础上用1M编辑数据微调得到。

框架的关键洞察在于：**生成建模的核心由Transformer主干承担，流匹配头仅作为轻量级采样器**——消融实验表明，将流匹配头从40M扩展到528M对GenEval、GenAI-Bench、DPG-Bench等指标影响极小（Table 5），这证实了架构分工的有效性。

### 图像标记器（NextStep-VAE）

NextStep-VAE 是从 **Flux.1-dev** VAE 微调而来的连续图像标记器，仅使用重建损失和感知损失进行训练。其核心设计包含两个关键操作：

**逐令牌归一化（Token-wise Normalization）**：沿通道维度对每个隐令牌进行独立归一化，使每个令牌的均值归零、方差归一。核心代码逻辑如下（Algorithm 1）：

```
μ = X.mean(dim=-1, keepdim=True)
σ = X.std(dim=-1, keepdim=True, unbiased=False)
X_norm = (X - μ) / (σ + eps)
```

该操作直接解决了高 CFG 下逐令牌统计分布漂移导致灰度斑块等视觉伪影的问题（Figure 3）。

**受控噪声注入（Stochastic Perturbation）**：在归一化后的隐变量上添加随机缩放的高斯噪声：

$$\tilde{z} = \operatorname{Normalization}(z) + \alpha \cdot \varepsilon , \quad \alpha \sim \mathcal{U}[0, \gamma] \ \mathrm{and} \ \varepsilon \sim \mathcal{N}(0, I)$$

其中 $\gamma$ 控制噪声强度的上界，NextStep-1 采用 $\gamma = 0.5$。该设计在标记器训练阶段正则化隐空间，使其分布更接近标准正态分布（Figure A3），尽管会降低重建指标（rFID 上升、PSNR/SSIM 下降），却显著提升下游生成图像的保真度（Figure 4）。

标记器将图像编码为 $32 \times 32 \times 16$ 的连续隐空间，在 ImageNet-1K 256×256 上达到 PSNR 30.60、SSIM 0.89 的重建质量（Table 6）。

### 因果 Transformer 主干

NextStep-1 从 **Qwen2.5-14B** 初始化解码器，采用标准 1D RoPE 位置编码处理离散文本令牌和连续图像令牌的交错序列。自回归建模遵循标准分解：

$$p ( x ) = \prod _ { i = 1 } ^ { n } p ( x _ { i } \mid x _ { < i } )$$

训练总损失为文本交叉熵损失与图像流匹配损失的加权和：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{text}} \mathcal{L}_{\mathrm{text}} + \lambda_{\mathrm{visual}} \mathcal{L}_{\mathrm{visual}}$$

其中 $\lambda_{\mathrm{text}} = 0.01$、$\lambda_{\mathrm{visual}} = 1$（预训练第一阶段，Table 1）。文本头输出离散令牌分布计算交叉熵，流匹配头则基于 Transformer 隐藏状态预测连续令牌的速度向量。

### 流匹配头（Flow Matching Head）

流匹配头是一个 157M 参数的轻量 MLP，将 Transformer 的隐藏状态映射为下一图像块的速度预测。其核心功能是建模每个图像块的条件分布，而非承担主要的生成建模——消融实验表明，将流匹配头从 40M 扩展到 528M 对 GenEval、GenAI-Bench、DPG-Bench 等指标影响极小（Table 5），证明 Transformer 主干才是生成建模的核心。

推理阶段采用无分类器引导（Classifier-Free Guidance），通过无条件和条件预测的加权插值实现：

$$\tilde{v}(x|y) = (1 - w) \cdot v_{\theta}(x|\mathcal{D}) + w \cdot v_{\theta}(x|y)$$

其中 $w$ 为引导强度，$v_{\theta}(x|\mathcal{D})$ 和 $v_{\theta}(x|y)$ 分别为无条件和条件速度预测。

## 实验与关键发现

### 主结果：文生图与图像编辑

NextStep-1在文生图图文对齐评测上展现出与主流扩散模型可竞争的性能。在GenEval上达到0.63（使用Self-CoT增强后为0.73），GenAI-Bench Basic准确率达0.88（Self-CoT后0.90），DPG-Bench得分85.28（Table 2）。在OneIG-Bench综合评测中，NextStep-1取得0.417的平均分数，显著优于离散自回归模型**Emu3**（Wang et al., 2024b）的0.311（Table A1）。在世界知识推理评测WISE上，NextStep-1正确率达0.54，略高于混合架构模型**BAGEL**（Deng et al., 2025）的0.52（Table A2）。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Ndnwg9oOQO/figures/003_Table_2.jpg]]
*Table 2: Comparison of image-text alignment on GenEval (Ghosh et al., 2023), GenAI-Bench (Lin et al., 2024), and DPG-Bench (Hu et al., 2024). * result is with rewriting. † result is with Self-CoT*

在图像编辑任务上，基于NextStep-1微调的NextStep-1-Edit在GEdit-Bench-EN上取得6.58的GPT-4.1评分，超过OmniGen2的6.41；在ImgEdit-Bench上取得3.71分（Table 3）。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Ndnwg9oOQO/figures/004_Table_3.jpg]]
*Table 3: Comparison of image editing performance on GEdit-Bench (Full Set) (Liu et al., 2025c) and ImgEdit-Bench (Ye et al., 2025). G SC, G PQ, and G O refer to the metrics evaluated by GPT-4.1 (OpenAI, 2025a). Performance is evaluated based on the NextStep-1-Edit with 1:1 aspect ratio*

**公平性说明**：部分对比方法（如BAGEL）训练数据量远超NextStep-1（5T vs 2T tokens），比较可能不公平。标†的结果使用了Self-CoT推理增强，与不使用推理增强的方法不可直接对比。NextStep-1在GenEval上不及**Janus-Pro-7B**（Chen et al., CVPR 2025b），但在OneIG-Bench等复杂场景指标上更优，反映不同评估维度的侧重差异。

### 消融实验：流匹配头与标记器设计

#### 流匹配头大小的影响

为探究“自回归Transformer与流匹配头谁承担核心生成建模”这一问题，论文设计了三种不同规模的流匹配头：Small（40M）、Base（157M）和Large（528M），架构配置详见Table 4。定量消融结果（Table 5）显示，流匹配头大小对GenEval、GenAI-Bench、DPG-Bench三项指标的影响极小——Base配置下分别为0.59/0.77/85.15，Large配置下为0.56/0.77/85.50。定性对比（Figure 2）同样表明不同头大小生成的图像质量无明显差异。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Ndnwg9oOQO/figures/006_Table_4.jpg]]
*Table 4: Configurations for different flow-matching heads*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Ndnwg9oOQO/figures/007_Table_5.jpg]]
*Table 5: Quantitative results for different flow-matching head configurations. All variants are finetuned from the baseline with a newly initialized head*

这一结果强烈暗示：**Transformer骨干承担了条件分布 $p(x_i \mid x_{<i})$ 的核心生成建模，流匹配头仅作为轻量级采样器**，其角色类似于语言模型中的LM Head。

#### 逐令牌归一化与CFG稳定性

在高分类器自由引导（CFG）尺度下，基于VAE的连续自回归模型容易出现灰度斑块等视觉伪影。Figure 3揭示了根本原因：当CFG=3.0时，无归一化条件下逐令牌的均值与方差随采样步数发生显著漂移；而加入逐令牌归一化后，即使在高CFG下分布也保持稳定（均值接近0，方差接近1）。CFG的计算公式为：

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Ndnwg9oOQO/figures/008_Figure_3.jpg]]
*Figure 3: Evolution of per-token mean and variance over sampling steps under two CFG settings. At CFG = 1.5, the mean and variance stay close to 0 and 1, respectively, indicating stability. At CFG = 3.0, they drift significantly, causing image quality degradation. With normalization, the distributions of output latents remain stable across all CFG settings*

$$\tilde{v}(x|y) = (1 - w) \cdot v_{\theta}(x|\mathcal{D}) + w \cdot v_{\theta}(x|y)$$

逐令牌归一化直接解决了高引导强度下的统计分布漂移问题，使自回归Transformer在任意CFG引导下均能稳定生成。

#### 噪声正则化的反直觉效应

标记器训练中的噪声注入呈现出反直觉的规律：更高的噪声强度（$\gamma=0.5$）虽然增加了生成损失（rFID上升，PSNR/SSIM下降），却显著提升了生成图像的保真度（Figure 4）。定量面板显示，随着噪声强度从0增加到0.5，重建指标持续恶化，但定性重建示例表明解码器对隐空间扰动具有更强的鲁棒性。

附录Figure A3进一步佐证了这一发现：NextStep-1 VAE的16通道隐分布比Flux.1-dev VAE和无噪声版本的NextStep-1 VAE更接近标准正态分布，反映噪声正则化使隐空间更加分散。论文最终采用$\gamma=0.5$训练标记器。

#### 标记器重建质量

在ImageNet-1K 256×256上，NextStep-1标记器以32×32×16的隐空间形状取得PSNR 30.60、SSIM 0.89的重建性能（Table 6），为后续自回归生成提供了足够的高保真基础。

### 失败模式与局限性

1. **高维连续令牌伪影**：高维连续令牌可能产生局部噪声、块状伪影、全局噪声和网格状伪影（Figure A4），尽管NextStep-1.1已有所改进，根本原因尚待探究。

2. **推理延迟瓶颈**：自回归解码的串行性导致推理延迟高，LLM解码和流匹配头多步采样是主要瓶颈（Table A3给出了在983 TFLOP/s算力和3.36 TB/s带宽下的延迟分解）。

3. **高分辨率训练困难**：高分辨率训练时收敛慢，难以直接利用扩散模型中成熟的高分辨率策略。

4. **SFT训练不稳定**：SFT在小数据集上容易过拟合目标分布，难以找到保留通用生成能力的最佳检查点。

5. **1D RoPE的空间建模局限**：标准1D RoPE可能导致微弱的网格状伪影，反映空间建模的不足。

## 定位与知识库关联

### 连续自回归范式的定位

NextStep-1 处于基于语言模型的自回归图像生成这一新兴范式，但与主流离散化路线存在根本性分歧。离散路线以 **Emu3** (Wang et al., 2024b) 和 **Janus-Pro-7B** (Chen et al., CVPR 2025b) 为代表，将图像量化为离散 VQ 标记后直接复用标准交叉熵损失；NextStep-1 则坚持连续标记，通过流匹配头实现逐块分布建模。这一选择的直接收益是避免了 VQ 带来的信息瓶颈，代价是需要解决连续隐空间在自回归解码中的统计稳定性问题。

与混合架构 **BAGEL** (Deng et al., 2025) 相比，NextStep-1 的生成建模完全内嵌于自回归框架内——流匹配头仅作为轻量级采样器，而非独立的扩散模型。消融实验（Table 5）表明，流匹配头从 40M 到 528M 的参数变化对 GenEval、GenAI-Bench、DPG-Bench 指标影响极小，说明 Transformer 主干承担了核心的条件分布建模，流匹配头的作用类似于语言模型中的 LM head，仅将隐藏状态映射到输出空间。

### 关键设计决策与因果机制

**瓶颈识别**：论文通过分析高 CFG 下的生成伪影，将问题定位为逐令牌统计分布漂移，而非 1D RoPE 的位置不连续性。Figure 3 给出了直接证据：CFG=3.0 时，未归一化的逐令牌均值和方差随采样步数显著漂移，导致灰度斑块等视觉退化；加入逐令牌归一化后分布保持稳定。

**因果调节变量**：两个设计共同正则化隐空间，构成方法的核心贡献：

1. **逐令牌归一化**（token-wise normalization）：沿通道维度对每个图像令牌执行独立归一化，使隐空间在任意 CFG 引导下均保持零均值、单位方差。这是解决分布漂移的直接机制。

2. **受控噪声注入**（noise perturbation）：向归一化后的隐变量添加缩放高斯噪声 $\tilde{z} = \operatorname{Normalization}(z) + \alpha \cdot \varepsilon$，其中 $\alpha \sim \mathcal{U}[0, \gamma]$。Figure 4 揭示了反直觉的权衡：更高的噪声强度（γ=0.5）虽然恶化重建指标（rFID↑、PSNR↓、SSIM↓），却显著提升生成图像的保真度。Figure A3 进一步表明，噪声正则化使隐分布更接近标准正态分布，增强了分散性和对扰动的鲁棒性。

**基础模型选择**：从 **Qwen2.5-14B** 初始化解码器，而非从头训练，使模型继承了语言理解与推理能力。这一选择与 Emu3 等从头训练的策略形成对比，在训练效率和多模态对齐上具有优势，但也引入了对特定 LLM 架构的依赖性。

### 适用边界与局限

**已确认的局限**：

1. **高维连续令牌伪影**：Figure A4 展示了局部噪声、块状伪影、全局噪声和网格状伪影等失败案例，尽管 NextStep-1.1 已有所改进，但根本原因尚未完全明确。

2. **推理延迟瓶颈**：自回归解码的串行性导致高延迟。Table A3 的延迟分解显示，LLM 解码和流匹配头多步采样是主要瓶颈，难以直接应用扩散模型中成熟的少步采样策略。

3. **高分辨率训练困难**：逐块自回归的特性使高分辨率训练收敛缓慢，论文指出难以直接复用扩散模型的高分辨率策略。

4. **SFT 训练不稳定性**：在小数据集上 SFT 容易过拟合目标分布，难以找到保留通用生成能力的最佳检查点。

5. **空间建模不足**：1D RoPE 可能导致微弱的网格状伪影，反映对 2D 空间结构的建模不够充分。

**公平性注意事项**：部分对比方法（如 BAGEL）的训练数据量远超 NextStep-1（5T vs 2T tokens），可能处于不公平比较。带 † 的指标使用了 Self-CoT 增强，无法与不使用推理增强的方法直接对比。

### 开放问题

论文明确提出的开放问题包括：

- 噪声正则化中，隐空间的鲁棒性和分散性哪个是生成质量提升的关键因素？
- 如何为逐块自回归模型设计高效的高分辨率生成策略？
- 流匹配头能否进一步蒸馏或采用少步采样以显著降低推理延迟？
- 能否将自回归模型与流匹配头的组合扩展到视频或其他模态的统一生成？

这些问题的解答将决定连续自回归范式能否在推理效率和生成质量上与扩散模型全面竞争。

## 原文 PDF

![[paperPDFs/ICLR_2026/NextStep_1_Toward_Autoregressive_Image_Generation_with_Continuous_Tokens_at_Scale.pdf]]
