---
title: "VCP-Attack: Visual-Contrastive Projection for Transferable Black-Box Targeted Attacks on Large Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VCP_Attack_Visual_Contrastive_Projection_for_Transferable_Black_Box_Targeted_Attacks_on_Large_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- VA
- VCP-Attack
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 多正负样本对比损失与动态PCA子空间投影的双重机制：对比损失重塑优化目标为多参考点互关系约束，PCA子空间滤除低方差非语义方向，提高语义对齐与泛化。
primary_logic: 对比监督迫使扰动满足语义簇分布对齐，PCA投影匹配优化容量与语义证据量，协同作用显著提升黑盒场景下的目标攻击可迁移性。
claims:
- VCP-Attack在开源LVLM上平均ASR达94.2%，相比最强基线提升23.3%；在闭源模型上平均ASR达83.1%，提升16.8%。
- 去除PCA子空间投影导致平均ASR显著下降（至90.5%），维度取10时性能最优（96.7%）。
- Top-k=10, Top-m=10采样配置在平衡相关性与多样性上优于其他策略，验证了选择性对比监督的有效性。
- 开源LVLM（7个模型） 上 ASR (%) = 94.2
---

# VCP-Attack: Visual-Contrastive Projection for Transferable Black-Box Targeted Attacks on Large Vision-Language Models

> [!tip] 核心洞察
> 对比监督迫使扰动满足语义簇分布对齐，PCA投影匹配优化容量与语义证据量，协同作用显著提升黑盒场景下的目标攻击可迁移性。

| 字段 | 内容 |
|------|------|
| 中文题名 | VCP-Attack：面向大视觉语言模型的可迁移黑盒目标攻击的视觉对比投影方法 |
| 英文题名 | VCP-Attack: Visual-Contrastive Projection for Transferable Black-Box Targeted Attacks on Large Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_VCP-Attack_Visual-Contrastive_Projection_for_Transferable_Black-Box_Targeted_Attacks_on_Large_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VCP-Attack |
| Dataset | 开源LVLM（7个模型）, 闭源LVLM（GPT-4o, Claude-3.7, Gemini-2.5）, InternVL3-14B, GPT-4o |

> [!tip] 效果简介
> - 开源LVLM（7个模型） 上，ASR (%) 94.2 vs 71.8 (M-Attack) (+22.4)。
> - 闭源LVLM（GPT-4o, Claude-3.7, Gemini-2.5） 上，ASR (%) 83.1 vs 66.3 (M-Attack) (+16.8)。
> - InternVL3-14B 上，ASR (%) 96.7 vs 87.7 (M-Attack) (+9.0)。

## 概述

### 问题瓶颈

现有面向大视觉语言模型（LVLM）的黑盒目标攻击方法普遍依赖逐点余弦相似度最大化来优化对抗扰动。这种单一信号缺乏结构化语义监督，导致梯度噪声大且优化过程易过拟合于替代模型，严重制约了跨模型迁移性。此外，原始高维CLIP特征空间中存在大量与语义无关的方差方向，进一步放大了替代模型特异性过拟合的风险。

### 核心方法

**VCP-Attack**（Visual-Contrastive Projection Attack）通过双重机制系统性解决上述瓶颈：

1. **多正负样本对比损失**：将优化目标从单点相似度重塑为多参考点间的互关系约束。具体而言，对每个对抗样本构建50个正样本和50个负样本构成的监督集，在特征空间中同时拉近与正样本簇的距离、推远与负样本簇的距离，并引入间隔正则化保证语义边界。
2. **动态PCA子空间投影**：在每次优化迭代中，对当前特征进行主成分分析，仅保留前d个主成分构成的低维子空间，将对比监督约束于其中。该操作滤除了高维空间中的非语义噪声方向，使优化容量与语义证据量相匹配，从而抑制替代模型特异性过拟合。

两种机制协同工作：对比监督迫使扰动满足语义簇分布对齐，PCA投影则防止优化过程在非语义方向上浪费扰动预算，共同显著提升了黑盒场景下的目标攻击可迁移性。

### 主要结果

在固定扰动预算 $\epsilon = 16/255$ 的公平评估设置下，VCP-Attack在7个开源LVLM上取得**平均ASR 94.2%**，相比最强基线M-Attack（71.8%）提升22.4个百分点；在GPT-4o、Claude-3.7、Gemini-2.5等闭源模型上取得**平均ASR 83.1%**，提升16.8个百分点。其中，在InternVL3-14B上达到96.7%，在GPT-4o上达到95.6%，验证了方法在异构模型间的强迁移能力。

### 方法谱系与知识库定位

VCP-Attack属于**基于迁移的黑盒目标攻击**范式，其核心贡献在于将对比学习范式引入对抗攻击优化过程。相较于以下代表性基线工作：

- **AttackVLM**（Zhao et al., NeurIPS 2023）：仅使用单一目标图像与ViT-B/32替代模型进行逐点对齐，缺乏多参考点结构化监督；
- **AdvDiffVLM**（Guo et al., IEEE TIFS 2024）：通过扩散模型生成无限制扰动，但优化过程未显式建模语义对比关系；
- **AnyAttack**（Zhang et al., CVPR 2025）：基于LAION-400M预训练的自监督对抗生成器，标签无关但缺乏目标导向的对比约束；
- **M-Attack**（Li et al., arXiv 2025）：引入局部裁剪对齐注入语义线索，但仍依赖点对点相似度优化；
- **FOA-Attack**（Jia et al., arXiv 2025）：对patch和CLS标记进行闭式特征对齐，监督信号仍限于单一目标。

VCP-Attack通过“对比监督+PCA子空间”的双重设计，在损失函数层面从点相似度升级为多参考点对比损失，在特征空间层面从原始高维空间收缩至动态PCA子空间，实现了对上述方法的结构性改进。该方法的技术路线可追溯至对比学习（如SimCLR、CLIP）中的多正负样本判别思想，并将其首次系统性地应用于LVLM对抗攻击的优化动力学中。

## 背景与动机

大视觉语言模型（LVLM）在图像描述、视觉问答等多模态任务中展现出强大能力，但其安全脆弱性问题随之凸显。对抗攻击——通过对输入图像施加人眼不可察觉的微小扰动，即可诱导模型输出攻击者指定的错误内容——已成为评估和提升LVLM鲁棒性的关键手段。在现实黑盒场景中，攻击者无法访问模型参数或梯度，必须依赖替代模型生成对抗样本并迁移至受害者模型。然而，现有黑盒目标攻击方法的迁移性仍远未满足实际威胁评估的需求。

当前主流方法的核心瓶颈在于**监督信号的贫瘠与优化空间的无结构**。以 **AttackVLM**（Zhao et al., NeurIPS 2023）为代表的早期工作仅使用单张目标图像与对抗样本之间的逐点余弦相似度作为优化目标；后续方法如 **M-Attack**（Li et al., arXiv 2025）引入局部裁剪对齐、**FOA-Attack**（Jia et al., arXiv 2025）利用patch与CLS token的闭式特征对齐，虽在语义注入上有所改进，但本质上仍依赖点对点的相似度最大化。这类逐点优化策略存在两个结构性缺陷：其一，单一目标样本无法刻画语义类别的分布边界，导致梯度方向噪声大、易陷入局部最优；其二，在高维CLIP特征空间中，大量维度承载的是非语义的冗余变化，优化过程在这些方向上浪费扰动预算，却难以形成跨模型的泛化信号。

此外，**AdvDiffVLM**（Guo et al., IEEE TIFS 2024）尝试通过扩散模型生成无约束扰动，**AnyAttack**（Zhang et al., CVPR 2025）则依赖大规模预训练的自监督生成器，但这些方法或牺牲了扰动的不可察觉性，或引入了与替代模型强耦合的归纳偏置，在黑盒迁移场景下增益有限。

本文提出 **VCP-Attack**（Visual-Contrastive Projection Attack），核心动机在于以**结构化对比监督**替代逐点对齐，以**动态子空间约束**替代全空间优化。具体而言，VCP-Attack引入多正负样本构成的监督集，通过对比损失将优化目标重塑为“对抗特征与正样本簇对齐、与负样本簇分离”的分布级约束，缓解过拟合；同时，利用动态PCA投影将扰动更新限制在低维语义子空间内，滤除高维噪声方向，使有限的扰动预算集中于对迁移性真正有贡献的语义维度。这一双重机制协同作用，旨在显著提升黑盒目标攻击的跨模型迁移能力。

## 核心创新

VCP-Attack的核心创新在于将**结构化对比监督**与**动态PCA子空间投影**双重机制引入黑盒目标攻击的扰动优化过程，从根本上重塑了扰动的生成范式。现有方法（如AttackVLM、M-Attack等）的瓶颈在于仅依赖逐点余弦相似度最大化，优化目标缺乏对语义结构的显式建模，导致梯度噪声大且易过拟合于替代模型的高维特征空间，限制了跨模型迁移性。VCP-Attack通过以下两个关键“changed slots”突破了这一瓶颈：

### 1. 损失函数：从逐点对齐到多正负样本对比监督

**基线方案**：现有黑盒目标攻击方法（如AttackVLM、M-Attack）采用逐点余弦相似度最大化，即仅将对抗样本特征与单个目标图像特征对齐。这种单点监督方式无法捕捉目标语义的分布特性，梯度方向易受替代模型特异性噪声干扰。

**VCP-Attack方案**：引入多正负样本对比损失，将优化目标重塑为对抗样本特征与正样本集合对齐、同时远离负样本集合的结构化约束。具体而言：
- 构建包含50个正样本和50个负样本的监督集，正样本根据目标语义从ImageNet-1K选取，负样本根据源语义选取；
- 采用top-k正样本加权损失与最大正样本辅助损失的凸组合（$\mathcal{L}_{pos} = \alpha \cdot \mathcal{L}_{pos}^{top-k} + (1-\alpha) \cdot \mathcal{L}_{pos}^{max}$），平衡多样性与稳定性；
- 引入top-m硬负样本惩罚（$\mathcal{L}_{neg}$）和间隔损失（$\mathcal{L}_{margin}$），确保最相似负样本与最相似正样本之间保持至少$\gamma$的余弦相似度间隔。

这一设计的关键因果机制在于：对比监督迫使扰动满足**语义簇分布对齐**，而非单点匹配。多参考点的互关系约束提供了更丰富的梯度信号，有效抑制了替代模型特异性方向的过拟合。消融实验证实，top-k=10、top-m=10的配置在相关性与多样性之间达到最优平衡，正损失权重$\alpha=0.8$时ASR最高。

### 2. 特征空间：从原始高维空间到动态PCA子空间投影

**基线方案**：现有方法直接在CLIP等编码器的原始高维特征空间（如ViT-L/14的768维或1024维）中进行优化。高维空间中存在大量与语义无关的低方差方向，这些方向在替代模型上可能产生有效梯度，但在受害者模型上缺乏泛化性。

**VCP-Attack方案**：在每次迭代中动态计算当前特征的PCA主成分，将对比监督约束在仅保留top-d主成分的低维子空间内（$\tilde{z} = U_k^\top z$），梯度经投影回原空间后更新扰动（$\nabla_{z} = U_k \cdot \nabla_{\tilde{z}}$）。这一机制的核心作用是**滤除低方差非语义方向**，使优化容量与语义证据量相匹配，从而抑制替代模型特异性过拟合。

消融实验提供了决定性证据：维度$d=10$时平均ASR达到96.7%的最高值，而去除PCA投影后ASR显著下降至90.5%，验证了子空间约束对迁移性的关键贡献。

### 双重机制的协同效应

对比监督与PCA投影并非独立作用，而是形成协同增强：对比损失提供了多参考点的结构化语义约束，PCA子空间则滤除了这些约束中与语义无关的噪声分量。论文分析指出，对比监督通过重塑优化目标来改善迁移性，其机制与PCA的容量控制作用“根本不同但互补”。这一协同设计使得VCP-Attack在开源LVLM上平均ASR达94.2%（超越最强基线M-Attack达22.4个百分点），在闭源模型上平均ASR达83.1%（超越16.8个百分点），在GPT-4o上更达到95.6%的单模型最高ASR。

## 整体框架

VCP-Attack 的整体 pipeline 围绕一个核心矛盾展开：**黑盒目标攻击需要结构化语义监督，而现有方法仅依赖逐点余弦相似度，导致梯度噪声大且易过拟合于替代模型**。为此，框架将攻击过程重构为“监督集构建—特征提取—PCA 子空间投影—对比损失优化—扰动更新”五个紧密耦合的模块，如图 3 所示。

### 输入与输出流

- **输入**：一张干净图像 $x_{clean}$、目标语义标签 $y_{tar}$（用于构造正样本集）以及源语义标签（用于构造负样本集）。
- **输出**：对抗样本 $x_{adv} = x_{clean} + \delta$，其中 $\delta$ 受 $L_\infty$ 范数约束（$\|\delta\|_\infty \le \epsilon$），使得黑盒 LVLM $M$ 对 $x_{adv}$ 的输出与 $y_{tar}$ 对齐：$M(x_{adv}, \text{Prompt}) \rightarrow y_{tar}$。

### 模块关系与数据流

1. **监督集构建**：根据目标语义从 ImageNet-1K 中选取 50 个正样本，根据源语义选取 50 个负样本，形成对比监督信号的基础。这一设计将攻击目标从“对齐单张图像”升级为“满足语义簇分布约束”。

2. **特征提取**：使用 $t$ 个冻结的 CLIP 系列编码器（如 ViT、ConvNeXt 变体）分别提取对抗样本、正样本集和负样本集的高维特征。多编码器集成是迁移性的第一重保障。

3. **PCA 子空间投影**：对每个编码器的特征空间动态计算主成分，将特征投影到仅保留 top-$d$ 主成分的低维子空间 $\tilde{z} = U_k^\top z$。这一步是**显式的容量控制机制**——滤除高维空间中的非语义、替代模型特异性方向，迫使优化聚焦于跨模型共享的语义轴。

4. **对比损失计算**：在子空间内计算三项损失：
   - **正样本损失** $\mathcal{L}_{pos}$：top-$k$ 加权项与 max 项的凸组合（$\alpha=0.8$），平衡多样性与稳定性；
   - **负样本损失** $\mathcal{L}_{neg}$：仅惩罚相似度最高的 top-$m$ 硬负样本；
   - **间隔损失** $\mathcal{L}_{margin}$：强制最相似负样本的相似度低于最相似正样本至少 $\gamma$。

   梯度通过 PCA 投影矩阵反向映射回原始特征空间：$\nabla_z = U_k \cdot \nabla_{\tilde{z}}$。

5. **扰动更新与优化**：采用动量迭代 FGSM（MI-PGD）累积梯度方向，后期引入指数移动平均（EMA）平滑以稳定 $\delta$ 并提升迁移性。总损失为所有替代模型上三项损失之和：
   $$\mathcal{L}_{total} = \sum_{i=1}^{t} \big( \mathcal{L}_{pos}^{(i)} + \mathcal{L}_{neg}^{(i)} + \lambda_{margin} \cdot \mathcal{L}_{margin}^{(i)} \big)$$

### 协同机制

PCA 投影与对比损失的协同是框架有效性的关键。消融实验表明：去除 PCA 投影后平均 ASR 从 96.7% 降至 90.5%，验证了子空间约束对抑制过拟合的独立贡献；而对比损失通过多参考点互关系约束重塑优化目标，其作用机制与 PCA 正交——前者控制“在哪个空间优化”，后者定义“优化什么目标”。二者叠加使扰动既满足语义簇分布对齐，又避免在高维空间中发散到非迁移方向。

### 补充图表

![[assets/figures/papers/paper_list_l804_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_VCP_Attack_Visual/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed VCP-Attack framework. The method constructs a supervision set with positive and negative samples, extracts high-dimensional features via frozen encoders, and performs contrastive optimization in a PCA subspace to update adversarial perturbations*

## 核心模块与公式推导

VCP-Attack 的核心由三个紧密耦合的模块构成：**多正负样本对比损失设计**、**动态PCA子空间投影**，以及**多替代模型集成优化**。三者协同将黑盒目标攻击从逐点相似度最大化重塑为结构化语义对齐问题。

### 3.1 问题形式化与优化目标

给定干净图像 $x_{clean}$ 和目标语义 $y_{tar}$，攻击目标是生成对抗样本 $x_{adv} = x_{clean} + \delta$，使得黑盒LVLM $M$ 的输出与 $y_{tar}$ 对齐：

$$M ( x_{adv} , \mathrm{Prompt} ) \Rightarrow y_{tar} \tag{1}$$

其中 $\|\delta\|_\infty \le \epsilon$。攻击者仅能访问 $t$ 个冻结的替代视觉编码器 $f_{\phi_i}$（如CLIP ViT/ConvNeXt变体），无法获取受害者模型内部参数。优化问题形式化为：

$$\min_{\|\delta\|_\infty \le \epsilon} \sum_{i=1}^{t} \mathcal{L} \big( f_{\phi_i}(x_{clean}+\delta), \{f_{\phi_i}(x_k^+)\}, \{f_{\phi_i}(x_j^-)\} \big) \tag{2}$$

其中 $\{x_k^+\}$ 和 $\{x_j^-\}$ 分别为正、负样本监督集。

### 3.2 多正负样本对比损失

现有方法仅最大化对抗特征与单一目标特征的余弦相似度，缺乏结构化语义约束。VCP-Attack 引入多参考点对比损失，迫使对抗特征在语义簇分布层面实现对齐。

**特征归一化与相似度计算**：将对抗特征 $z_{adv}$ 与参考特征进行L2归一化得到 $\hat{z}$，计算带温度缩放的余弦相似度：

$$s_i^+ = \frac{\langle \hat{z}_{adv}, \hat{z}_i^+ \rangle}{\tau}, \quad s_j^- = \frac{\langle \hat{z}_{adv}, \hat{z}_j^- \rangle}{\tau} \tag{3}$$

其中 $\tau$ 为温度参数，控制相似度分布的锐度。

**对数-softmax分数**：在所有 $N_p + N_n$ 个参考样本上计算对数概率：

$$\ell_k = s_k - \log \sum_{l=1}^{N_p+N_n} \exp(s_l) \tag{4}$$

该归一化将绝对相似度转化为相对排序信号，使优化对尺度变化不敏感。

**Top-k正样本损失**：选取对数概率最大的 $k$ 个正样本进行softmax加权：

$$\mathcal{L}_{pos}^{top\text{-}k} = -\sum_{i=1}^{k} w_i \cdot \ell_{[i]}^+ \tag{5}$$

其中权重 $w_i = \frac{\exp(\ell_{[i]}^+)}{\sum_{j=1}^{k} \exp(\ell_{[j]}^+)}$，使高置信度正样本获得更大梯度。

**最大正样本辅助损失**：为防止梯度被多个正样本稀释，单独强化最强正样本：

$$\mathcal{L}_{pos}^{max} = -\max_{i \in [1,N_p]} \ell_i^+ \tag{7}$$

**凸组合正样本损失**：通过权重 $\alpha$ 平衡多样性与稳定性：

$$\mathcal{L}_{pos} = \alpha \cdot \mathcal{L}_{pos}^{top\text{-}k} + (1-\alpha) \cdot \mathcal{L}_{pos}^{max} \tag{8}$$

实验表明 $\alpha=0.8$ 达到最优ASR（见Figure 6），验证了top-k加权与max项协同的有效性。

**Top-m负样本损失**：仅惩罚相似度最高的 $m$ 个负样本（硬负样本挖掘），避免简单负样本主导梯度：

$$\mathcal{L}_{neg} = \frac{1}{m} \sum_{j=1}^{m} \ell_{[j]}^- \tag{9}$$

**间隔损失**：显式约束最相似负样本与最相似正样本之间的最小间隔：

$$\mathcal{L}_{margin} = \max(0, \max_j s_j^- - \max_i s_i^+ + \gamma) \tag{10}$$

其中 $\gamma$ 为间隔超参数，确保语义边界清晰分离。

### 3.3 动态PCA子空间投影

高维CLIP/SigLIP特征空间（通常512-1024维）中存在大量与语义无关的噪声方向。直接在此空间优化易导致替代模型过拟合，损害迁移性。VCP-Attack 引入动态PCA投影，将对比监督约束在语义信息集中的低维子空间内。

**投影操作**：对当前批次的对抗特征与参考特征计算主成分，取前 $d$ 个主成分构成投影矩阵 $U_k$：

$$\tilde{z} = U_k^\top z \tag{11}$$

所有对比损失在 $d$ 维子空间内计算，滤除低方差非语义方向。

**梯度回传**：子空间内的梯度需映射回原始特征空间以更新扰动：

$$\nabla_z = U_k \cdot \nabla_{\tilde{z}} \tag{12}$$

PCA基在每个优化步动态更新，适应扰动演化过程中的特征分布变化。消融实验（Figure 5）表明，$d=10$ 时平均ASR达96.7%，去除PCA投影后降至90.5%，验证了子空间约束作为显式容量控制机制的关键作用。

![[assets/figures/papers/paper_list_l804_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_VCP_Attack_Visual/figures/008_Figure_5.jpg]]
*Figure 5: Average ASR across seven open-source LVLMs under different PCA subspace dimensionalities*

### 3.4 多模型集成优化与总损失

总损失为所有替代模型上的正、负、间隔损失之和：

$$\mathcal{L}_{total} = \sum_{i=1}^{t} \big( \mathcal{L}_{pos}^{(i)} + \mathcal{L}_{neg}^{(i)} + \lambda_{margin} \cdot \mathcal{L}_{margin}^{(i)} \big) \tag{13}$$

其中 $\lambda_{margin}$ 控制间隔项权重。优化采用**动量迭代FGSM（MI-PGD）**，并在后期阶段施加**指数移动平均（EMA）平滑**以稳定扰动并提升迁移性。梯度经各替代模型的PCA子空间独立回传后，汇总更新共享扰动 $\delta$。

### 3.5 监督集构建

监督集是结构化对比监督的基础。对每个攻击样本，从ImageNet-1K中按目标语义选取50个正样本，按源语义选取50个负样本。正样本确保对抗特征向目标语义簇靠拢，负样本提供排斥边界。Top-k=10、Top-m=10的采样策略（Figure 7）在相关性与多样性间取得最优平衡，验证了选择性对比监督优于全量样本策略。

![[assets/figures/papers/paper_list_l804_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_VCP_Attack_Visual/figures/010_Figure_7.jpg]]
*Figure 7: Average ASR across seven open-source LVLMs under different Top-k and Top-m sampling strategies*

### 补充图表

![[assets/figures/papers/paper_list_l804_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_VCP_Attack_Visual/figures/009_Figure_6.jpg]]
*Figure 6: Average ASR across seven open-source LVLMs under different positive loss weighting coefficients (α)*

## 实验与分析

### 主实验结果

VCP-Attack在开源与闭源LVLM上均展现出显著优于现有基线的目标攻击迁移性。Table 1报告了7个开源LVLM在固定扰动预算ϵ=16/255下的攻击成功率（ASR）。VCP-Attack平均ASR达**94.2%**，相比最强基线M-Attack（71.8%）提升**22.4个百分点**，较AttackVLM（65.5%）和AdvDiffVLM（52.3%）分别提升28.7和41.9个百分点。在InternVL3-14B上，VCP-Attack取得**96.7%**的ASR，较M-Attack（87.7%）高出9.0个百分点。

闭源模型上的迁移性更为关键。Table 2显示，VCP-Attack在GPT-4o、Claude-3.7-Sonnet和Gemini-2.5-Flash上平均ASR达**83.1%**，超出M-Attack（66.3%）16.8个百分点。其中GPT-4o上ASR高达**95.6%**，Gemini-2.5-Flash上达92.6%，Claude-3.7-Sonnet上为61.1%——后者虽绝对数值较低，但仍比M-Attack的53.8%高出7.3个百分点，表明对比监督与子空间投影的协同机制对架构差异较大的闭源模型同样有效。

Figure 1以柱状图直观展示了闭源模型上的ASR对比，VCP-Attack在所有三个商用模型上均取得最高ASR，验证了其黑盒迁移性的鲁棒性。Figure 2提供了定性示例：由VCP-Attack生成的对抗图像在不同LVLM上均输出与目标语义一致的描述，进一步佐证了攻击的语义对齐能力。

### 消融实验

**PCA子空间维度。** Figure 5展示了子空间维度d对平均ASR的影响。当d=10时ASR达到峰值**96.7%**；完全移除PCA投影（即在全维原始空间优化）导致ASR骤降至**90.5%**，降幅达6.2个百分点。这表明PCA投影通过滤除高维空间中的非语义噪声方向，有效抑制了对替代模型的过拟合。维度过小（d<5）时信息损失过大，性能下降；维度过大（d>20）则逐渐退化为全空间优化，过拟合风险回升。

**正样本损失权重α。** Figure 6显示α=0.8时ASR最优。该凸组合平衡了top-k加权损失（捕捉多样正样本结构）与max项（强化最强正信号）。α=1（仅top-k）或α=0（仅max）均导致ASR下降约2-3个百分点，说明单一策略无法同时兼顾语义多样性与优化稳定性。

**Top-k与Top-m采样策略。** Figure 7比较了不同(k, m)配置。**(10, 10)配置始终优于其他组合**，验证了选择性对比监督的有效性：仅聚焦最相关的10个正样本和10个硬负样本，既提供了充分的语义约束，又避免了全量样本引入的噪声。全量采样（50, 50）因包含弱相关样本导致梯度信号稀释，ASR反而低于(10, 10)。

**扰动预算ϵ。** Figure 8显示，ϵ从8/255增至32/255时，ASR从约88%单调上升至**98.2%**，表明更大的扰动空间为对比监督提供了更强的语义对齐能力。但作者未报告SSIM或LPIPS等感知质量指标，仅依赖L∞范数约束，视觉不可感知性需人工核验。

### 失败模式与局限性

尽管VCP-Attack在图像描述任务上表现优异，仍存在以下局限：

1. **任务泛化未验证。** 所有实验仅局限于图像描述（image captioning）任务，尚未在VQA、视觉推理等多模态任务上评估迁移性。对比监督的语义对齐机制是否适用于更复杂的跨模态推理场景，仍需进一步验证。

2. **架构差异敏感性。** Claude-3.7-Sonnet上ASR（61.1%）显著低于GPT-4o（95.6%），揭示出当替代模型与受害者模型的视觉编码器架构差异极大时，PCA子空间的语义对齐能力可能不足。该现象提示子空间投影的线性假设在高度异构的表示空间间可能受限。

3. **攻击场景单一。** 仅考虑单步目标攻击，未探索多轮交互或自适应攻击场景。真实部署环境中，LVLM通常集成内容过滤与多模态防御机制，VCP-Attack在此类条件下的有效性尚不明确。

4. **不可感知性评估缺失。** 仅以L∞范数约束扰动大小，未系统报告SSIM、LPIPS等感知质量指标。Figure 4虽提供了对抗样本与扰动的可视化比较，但定量评估的缺失使得攻击的隐蔽性难以准确判断。

### 补充图表

![[assets/figures/papers/paper_list_l804_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_VCP_Attack_Visual/figures/004_Table_1.jpg]]
*Table 1: Attack success rate (ASR, %) on open-source LVLMs under a fixed perturbation budget of*

![[assets/figures/papers/paper_list_l804_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_VCP_Attack_Visual/figures/005_Table_2.jpg]]
*Table 2: Attack success rate (ASR, %) on closed-source LVLMs under a fixed perturbation budget of*

![[assets/figures/papers/paper_list_l804_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_VCP_Attack_Visual/figures/001_Figure_1.jpg]]
*Figure 1: Our method achieves the highest ASR across proprietary LVLMs. Under a fixed perturbation budget*

![[assets/figures/papers/paper_list_l804_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_VCP_Attack_Visual/figures/007_Figure_8.jpg]]
*Figure 8: Effect of perturbation budget ϵ on average ASR across seven open-source LVLMs*

![[assets/figures/papers/paper_list_l804_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_VCP_Attack_Visual/figures/002_Figure_2.jpg]]
*Figure 2: Targeted adversarial image crafted using VCP-Attack, along with textual descriptions generated by various commercial and open-source MLLMs in response to the prompt: “Briefly describe the content of this image in no more than three sentences.”*

![[assets/figures/papers/paper_list_l804_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_VCP_Attack_Visual/figures/006_Figure_4.jpg]]
*Figure 4: Visual comparison of adversarial examples (left) and corresponding perturbations (right) generated by different methods. Note that the “Target” image shown for our method is only representative—our contrastive supervision is derived from 50 semantically aligned positive samples, not a single target image*

## 方法谱系与知识库定位

### 与现有目标攻击方法的对比定位

VCP-Attack 的核心辨识度在于将**多正负样本对比损失**与**动态PCA子空间投影**耦合为统一的扰动优化框架，这与现有黑盒目标攻击方法存在本质差异。

**逐点对齐范式的局限性。** 以 **AttackVLM**（Zhao et al., NeurIPS 2023）为代表的早期工作，仅通过单张目标图像与对抗样本在CLIP特征空间的余弦相似度最大化来引导扰动方向。这类逐点对齐策略缺乏结构化语义监督，梯度信号受高维特征空间中的非语义方向噪声干扰，容易过拟合于替代模型，导致跨模型迁移性受限。**M-Attack**（Li et al., arXiv 2025）引入了局部裁剪与多区域对齐，但仍未突破“单样本-单方向”的优化范式。

**生成式攻击路径的差异。** **AdvDiffVLM**（Guo et al., IEEE TIFS 2024）利用扩散模型在潜空间生成无约束对抗扰动，**AnyAttack**（Zhang et al., CVPR 2025）则基于LAION-400M预训练自监督对抗生成器。这些方法侧重扰动生成的“自由度”，但缺乏对语义对齐方向的显式约束，在黑盒迁移场景下难以保证目标语义的准确注入。相比之下，VCP-Attack 通过50个正样本和50个负样本构成的监督集，将优化目标重塑为“在多参考点互关系约束下对齐语义簇分布”，而非生成一个看似合理的扰动。

**特征空间利用的升级。** **FOA-Attack**（Jia et al., arXiv 2025）在patch token和CLS token上进行闭式特征对齐，但仍工作在原始高维CLIP空间。VCP-Attack 的PCA子空间投影机制通过仅保留top-d主成分，显式滤除低方差非语义方向，使优化容量与语义证据量匹配。这一设计直接回应了核心瓶颈：高维特征空间中大量维度对语义对齐无贡献，却为替代模型过拟合提供了自由度。

### 方法适用边界

**任务边界。** 当前评估仅局限于图像描述（image captioning）任务。论文明确指出，在VQA、视觉推理等其他视觉-语言任务上的迁移性尚未验证，这构成方法泛化性的核心未解问题。

**架构依赖性。** 攻击有效性依赖于替代模型与受害者模型之间的表示相似性。VCP-Attack 使用八种CLIP变体（ViT/ConvNeXt等）作为替代编码器，当受害者模型采用架构差异极大的视觉骨干（如纯卷积网络、非对比预训练模型）时，PCA子空间的结构假设可能不再成立，迁移率预计下降。

**攻击场景限制。** 方法仅考虑单步目标攻击（single-step targeted attack），未涉及多轮交互或自适应攻击场景。在真实部署环境中，LVLM可能集成内容过滤、多模态防御机制，VCP-Attack 在这些条件下的有效性尚未评估。

**不可感知性权衡。** 方法仅使用 $L_\infty$ 范数约束（$\epsilon=16/255$）控制扰动幅度，未系统报告SSIM、LPIPS等感知质量指标。消融实验表明，将 $\epsilon$ 增大至 $32/255$ 可使ASR提升至98.2%，但视觉质量显著下降，揭示攻击强度与隐蔽性之间的固有张力。

### 局限与开放问题

**局限1：线性子空间假设的语义保真度。** PCA子空间投影基于线性降维假设，在高语义复杂性场景（如细粒度视觉概念、抽象场景理解）中，主成分可能无法捕获关键的语义判别方向。非线性降维方法（如变分自编码器、流形学习）是否能进一步提升语义对齐精度，是值得探索的方向。

**局限2：监督集构造的语义粒度。** 当前正/负样本从ImageNet-1K按类别语义选取，粒度较粗。对于细粒度目标攻击（如“金毛寻回犬”而非“狗”），监督集可能缺乏足够区分性的正负样本，影响对比损失的判别力。

**开放问题1：跨任务迁移性。** 如何将VCP-Attack的结构化对比监督框架扩展到VQA、视频理解等多模态任务？这需要重新定义“目标语义”的表示形式，以及对应的监督集构造策略。

**开放问题2：对抗鲁棒性评估。** 当前实验未涉及受害者模型的对抗训练或防御机制。若LVLM经过对抗训练，PCA子空间的语义结构可能发生偏移，VCP-Attack的迁移性是否仍能保持？这一问题直接关系到方法在安全关键场景中的实际威胁评估。

**开放问题3：真实世界部署的伦理风险。** 在包含内容过滤、多模态防御的真实开放环境中，VCP-Attack的有效性以及潜在的滥用风险（如生成误导性图像描述用于虚假信息传播）需要系统性评估。论文未提供防御方视角的分析或缓解建议。

**开放问题4：子空间动态性的理论解释。** PCA子空间在每次迭代中动态计算，这一设计虽在实验中有效，但其理论性质（如子空间稳定性、收敛性保证）尚未得到形式化分析。理解动态子空间与优化轨迹的交互关系，可能为设计更高效的投影策略提供指导。

## 原文 PDF

![[paperPDFs/CVPR_2026/VCP_Attack_Visual_Contrastive_Projection_for_Transferable_Black_Box_Targeted_Attacks_on_Large_Vision_Language_Models.pdf]]
