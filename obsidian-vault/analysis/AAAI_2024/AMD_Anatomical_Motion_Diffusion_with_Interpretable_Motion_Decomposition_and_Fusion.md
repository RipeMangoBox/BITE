---
title: AMD Anatomical Motion Diffusion with Interpretable Motion Decomposition and Fusion
type: paper
paper_level: A
venue: AAAI
year: 2024
pdf_ref: paperPDFs/AAAI_2024/AMD_Anatomical_Motion_Diffusion_with_Interpretable_Motion_Decomposition_and_Fusion.pdf
project_link: null
code_link: null
aliases:
- AAMD
- AAMDIMDF
tags:
- AAAI_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入大语言模型（LLM）将复杂文本分解为解剖脚本，并构建双分支扩散模型：一个分支保持原始文本保真度，另一分支利用解剖脚本和检索到的参考运动增加多样性，再通过可调参数 λ 自适应融合两者。
primary_logic: 借用LLM的解剖知识，将长难文本转化为简单解剖脚本的组合，同时用检索增强和双分支扩散在保真度与多样性之间取得平衡，从而有效应对复杂长文本动作生成。
claims:
- AMD使用微调的ChatGPT-3.5将文本分解为解剖脚本。
- 采用双分支扩散模型：一个分支以原始文本为条件保证保真度，另一个分支以解剖脚本和参考动作为条件增加多样性，并用融合模块平衡两者。
- 在复杂文本数据集SLCD1上，AMD的FID为0.116，比次优模型MDM的0.828大幅降低0.712。
- 消融实验表明，去除文本分解（NTD）或去除参考动作信息（NTDS）均会导致FID、Multimodal Dist等指标明显恶化。
---

# AMD Anatomical Motion Diffusion with Interpretable Motion Decomposition and Fusion

> [!tip] 核心洞察
> 借用LLM的解剖知识，将长难文本转化为简单解剖脚本的组合，同时用检索增强和双分支扩散在保真度与多样性之间取得平衡，从而有效应对复杂长文本动作生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | AMD：具有可解释运动分解与融合的解剖运动扩散模型 |
| 英文题名 | AMD Anatomical Motion Diffusion with Interpretable Motion Decomposition and Fusion |
| 会议/期刊 | AAAI 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | AMD (Adaptable Motion Diffusion) |
| Dataset | SLCD1 |

> [!tip] 效果简介
> - SLCD1 上，FID↓ 0.116±.011 vs 0.828±.061 (MDM) (0.712)；Multimodal Dist↓ 4.296±.012 vs 4.927±.059 (MDM) (0.631)。

## 概要

### 问题瓶颈
现有文本到运动（Text-to-Motion）生成模型普遍将任意长度和复杂度的自然语言描述压缩为单一固定长度向量。这种简化导致模型难以处理罕见或包含复杂长序列的动作描述——例如“scorpion”等专业动作因训练语料不足而无法合成，但其详细文本描述中却包含充足的解剖指令。核心瓶颈在于：**语言复杂性被过度简化，单一编码器无法捕捉细粒度运动语义**。

### 核心思路
AMD（Adaptable Motion Diffusion）引入两条关键路径破解上述瓶颈：
1. **解剖知识注入**：利用微调的ChatGPT-3.5将复杂文本分解为一系列简洁的解剖脚本（anatomical scripts），将长难描述转化为简单动作基元的组合。
2. **双分支扩散与自适应融合**：构建两个扩散分支——规范扩散（以原始文本为条件，保证保真度）和参考扩散（以解剖脚本及检索到的参考动作为条件，增加多样性），并通过可调参数λ自适应融合两者输出。

### 方法定位
AMD属于**基于扩散模型的文本驱动运动生成方法**，其核心创新在于将大语言模型的解剖知识引入运动生成管线，并通过检索增强与双分支融合机制在保真度与多样性之间取得平衡。与MDM（Tevet et al., arXiv 2022）、MotionDiffuse（Zhang et al., arXiv 2022）、T2M-GPT（Zhang et al., arXiv 2023）等单分支基线相比，AMD在文本条件处理上从“单一编码”转变为“分解-检索-融合”的多阶段架构。

### 主要结果
在复杂文本数据集SLCD1上，AMD的FID达到0.116±.011，比次优模型MDM的0.828±.061大幅降低0.712；Multimodal Dist也由4.927±.059降至4.296±.012。消融实验证实，去除文本分解（NTD）或去除参考动作信息（NTDS）均导致各指标明显恶化，验证了解剖分解与参考运动检索的关键作用。参数λ可有效调节保真度与多样性的权衡：λ→0时多样性上升，λ→1时保真度上升且FID快速下降。

文本到运动生成旨在将自然语言描述转化为逼真的三维人体运动序列，其在动画制作、虚拟现实和具身智能等领域具有广泛应用前景。近年来，扩散模型在该任务上取得了显著进展，涌现出**MDM**（Tevet et al., arXiv 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）、**T2M-GPT**（Zhang et al., arXiv 2023）和**ReMoDiffuse**（Zhang et al., arXiv 2023）等一系列代表性工作。

然而，现有方法存在一个核心瓶颈：它们过度简化了语言的复杂性。主流方案通常使用单一文本编码器（如CLIP）将任意长度或复杂度的文本描述映射为一个固定长度的特征向量。这种压缩式编码策略在处理简短、常规的动作描述时表现尚可，但面对罕见或包含复杂长序列的动作描述时则力不从心。例如，“scorpion”这类专业动作因训练数据中样本稀缺而难以被模型正确理解和合成，但其详细描述中却往往包含充足的解剖指令信息，这些信息在单一向量编码过程中被丢失或混淆。

这一瓶颈的因果机制在于：固定长度向量无法有效承载长文本中的细粒度语义结构，尤其是当文本涉及多个身体部位、时序动作组合或专业动作术语时，编码器倾向于保留高频共现模式而丢弃低频但关键的动作细节。

为应对上述挑战，AMD（Adaptable Motion Diffusion）提出了一种新的解决思路：借助大语言模型（LLM）的解剖知识，将复杂的长文本描述分解为一系列简洁、可解释的解剖脚本，从而绕过自然语言编码的复杂性。具体而言，AMD使用微调后的ChatGPT-3.5将输入文本解析为解剖脚本序列，并构建双分支扩散模型——一个分支基于原始文本保持生成保真度，另一分支基于解剖脚本和检索到的参考运动增加多样性，最后通过可调参数自适应融合两者，在保真度与多样性之间取得平衡。

## 核心方法与创新机理

### 问题瓶颈：长复杂文本到运动生成的表征坍缩

现有文本到运动（Text-to-Motion）方法普遍采用单文本编码器，将任意长度、任意复杂度的自然语言描述映射为一个固定长度的语义向量。当面对包含罕见动作、长序列、多解剖部位协调的复杂描述时，这种“压缩”会丢失关键信息。典型失败案例如“scorpion”这类专业动作——训练集中出现频率极低，模型无法合成；但若将动作拆解为“身体趴下、双腿抬起、双手撑地”等简单解剖指令，则每个子动作均有充足训练样本。核心矛盾在于：**语言复杂性与表征容量之间存在根本性张力**，现有方法缺乏将复杂文本显式分解为可执行子任务的能力。

### 核心调控变量：LLM 解剖分解 + 双分支扩散融合

AMD 引入两个互为补充的调控变量来打破上述瓶颈：

1. **大语言模型驱动的文本解剖分解**：使用微调后的 ChatGPT-3.5 将任意复杂动作描述解析为多个简洁的“解剖脚本”（anatomical scripts），每个脚本描述单一身体部位的动作。这一分解将“罕见复杂动作”转化为“常见简单动作的组合”，从根本上缓解了长尾动作的训练不足问题。
2. **双分支扩散与自适应融合**：构建两个扩散模型分支——规范扩散（Origin Motion Diffusion, OMD）以原始文本为条件保证保真度，参考扩散（Reference Motion Diffusion, RMD）以解剖脚本和检索到的参考动作为条件增加多样性。两者通过伯努利分布参数 λ 自适应融合，实现保真度与多样性的可控权衡。

### 相对 Baseline 的关键改变（Changed Slots）

| 方法维度 | Baseline 做法 | AMD 做法 |
|---------|-------------|---------|
| **文本条件处理** | 单文本编码器将完整描述压缩为固定向量 | 微调 ChatGPT-3.5 分解为解剖脚本，Sentence-BERT all-MiniLM-L6-v2 计算语义嵌入 |
| **扩散模型结构** | 单分支，仅以原始文本为条件 | 双分支：OMD（原始文本条件）+ RMD（解剖脚本 + 检索参考动作条件） |
| **运动生成融合** | 无融合，直接输出单分支结果 | 基于 Transformer 编码器层与残差连接的融合模块，伯努利分布 λ 控制输出频率 |

### 核心洞察

AMD 的核心洞察在于**借用 LLM 的解剖先验知识，将“理解复杂语言”的任务转化为“组合简单动作”的任务**。LLM 负责将长难文本拆解为语义清晰的解剖脚本；检索增强则为每个解剖脚本提供来自运动数据库的参考样例；双分支扩散在保真度（原始文本约束）与多样性（解剖脚本 + 参考动作约束）之间取得平衡。这一设计使得模型即使面对训练中从未见过的复杂长文本，也能通过组合已知的简单动作来合成合理运动。

### 关键证据支撑

- **文本分解有效性**：消融实验中，去除文本分解（NTD）导致 FID 从 0.20±.03 恶化至 0.65±.07，Multimodal Dist 从 5.28±.03 升至 5.71±.03（Table 3），验证了解剖分解对处理复杂文本的不可或缺性。
- **参考动作贡献**：进一步去除参考动作信息（NTDS）使 FID 急剧恶化至 1.39±.08（Table 3），表明检索到的参考运动对生成质量有决定性影响。
- **λ 调节机制**：λ→0 时模型多样性上升但偏离真实分布，λ→1 时参考动作主导，FID 快速下降（Figure 7），证实 λ 可有效调节保真度-多样性权衡。

AMD 的整体 pipeline 围绕一个核心思想展开：**将复杂文本动作描述分解为解剖脚本，再通过双分支扩散与自适应融合来平衡保真度与多样性**。图 2 展示了完整的架构流程。

### 输入流与文本分解

给定一个自然语言动作描述 $c_l$，系统首先调用微调后的 **ChatGPT-3.5** 将其解析为一组简洁、可解释的解剖脚本 $c_s$（Figure 2 caption）。这一分解步骤是应对长难文本的核心“因果旋钮”——它将语言复杂性转化为若干简单解剖指令的叠加，从而绕过传统单一文本编码器对罕见或复杂动作描述的映射瓶颈。

![[assets/figures/papers/paper_list_l1814_AMD_Anatomical_Motion_Diffusion_with_Interpretable_Motion_Decomposition/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method architecture: Given a motion text prompt*

### 语义嵌入与参考检索

文本 $c_l$ 和解剖脚本 $c_s$ 随后被送入 MLP $F_t$，与时间步 $t$ 一起投影为 token $z_{tk}^l$ 和 $z_{tk}^s$。系统使用 **Sentence-BERT all-MiniLM-L6-v2** 计算语义嵌入，并基于解剖相似性从运动数据库中检索参考动作 $m^{1:R}$（Figure 2 caption）。这些参考动作为后续的多样性生成提供了结构化先验。

### 双分支扩散结构

AMD 构建了两个并行的扩散模型分支：

1. **规范扩散模块（Origin Motion Diffusion, OMD）**：以原始文本 $c_l$ 为条件，通过标准逆扩散过程 $p_{\theta_1}(x_{t-1}^{1:N} | x_t^{1:N}, c)$ 生成保真度高的运动。该分支使用 $F_l^2$ 调整 $x_t^{1:N}$ 的维度，与 $z_{tk}^l$ 一同送入编码器 $E_l$，提取规范文本特征与扩散运动特征。

2. **参考扩散模块（Reference Motion Diffusion, RMD）**：以解剖脚本 $c_s$ 和检索到的参考动作 $m^{1:R}$ 为条件，通过 $p_{\theta_2}(x_{t-1}^{1:N} | x_t^{1:N}, c, m^{1:R})$ 生成多样性更高的运动。该分支使用 $F_s$ 调整参考动作维度，与 $z_{tk}^s$ 一同送入编码器 $E_s$，提取分解文本特征与参考动作特征。

### 特征融合与输出选择

**特征融合模块（Feature Fusion Module）** 基于 Transformer 编码器层构建，并引入残差连接。它将来自 OMD 的规范文本特征和扩散运动特征，与来自 RMD 的分解文本特征和参考动作特征，经过位置编码和交叉注意力机制处理后，输入融合块，输出 $p_{\theta_2}$。同时，$x_t^{1:N}$ 经 $F_l^1$ 调整维度后与 $z_{tk}^l$ 直接送入融合块，输出 $p_{\theta_1}$（Figure 2 caption）。

最终，系统通过伯努利分布的参数 $\lambda$ 控制 $p_{\theta_1}$ 和 $p_{\theta_2}$ 的输出频率：

$$f(p_\theta, \lambda) = \begin{cases} 1-\lambda & \text{if } p_{\theta_1} \\ \lambda & \text{if } p_{\theta_2} \end{cases}$$

当 $\lambda \to 1$ 时，参考扩散分支 $p_{\theta_2}$ 主导输出，保真度上升、FID 快速下降；当 $\lambda \to 0$ 时，规范扩散分支 $p_{\theta_1}$ 主导，多样性上升但可能偏离数据分布（Figure 7）。这一可调节的融合机制使 AMD 能够在保真度与多样性之间灵活权衡，是其应对复杂长文本动作生成的关键设计。

### 1. 解剖文本分解模块 (Anatomical Motion Text Decomposition)

该模块是AMD方法的核心前置步骤，旨在解决现有文本到运动模型中单一文本编码器无法有效处理复杂、长文本描述的瓶颈。AMD利用微调后的ChatGPT-3.5大语言模型，将输入的动作文本提示解析为一组简洁、可解释的解剖脚本。例如，一个复杂的动作描述会被分解为多个简单原子动作的组合，每个原子动作对应一个身体部位的明确运动指令。随后，使用Sentence-BERT模型 `all-MiniLM-L6-v2` 分别计算原始文本和解剖脚本的语义嵌入，为后续的双分支扩散提供条件信号。

### 2. 规范扩散模块 (Canonical Diffusion / Origin Motion Diffusion, OMD)

规范扩散模块遵循标准的扩散模型框架，以原始文本 $c$ 为条件生成运动序列，主要目标是保证生成结果的**保真度**。

**前向过程**：逐步向真实运动序列 $x_0^{1:N}$ 添加高斯噪声，生成一系列噪声样本 $x_t^{1:N}$。该过程定义为：

$$q(x_t^{1:N} | x_{t-1}^{1:N}) = \mathcal{N}(x_t^{1:N}; \sqrt{1-\beta_t} x_{t-1}^{1:N}, \beta_t I)$$

其中，$\beta_t$ 是控制噪声添加幅度的预定义方差调度参数，$N$ 表示运动序列的帧数。

**逆向过程**：从纯噪声开始，以原始文本 $c$ 为条件，逐步去噪重建运动序列。该过程由一个可学习的神经网络 $p_{\theta_1}$ 参数化：

$$p_{\theta_1}(x_{t-1}^{1:N} | x_t^{1:N}, c) = \mathcal{N}(x_{t-1}^{1:N}; \mu_\theta(x_t^{1:N}, c, t), \Sigma_\theta(x_t^{1:N}, c, t))$$

其中，$\mu_\theta$ 和 $\Sigma_\theta$ 是网络预测的均值和方差，$t$ 是扩散时间步。该分支的输出记为 $p_{\theta_1}$。

### 3. 参考扩散模块 (Reference Motion Diffusion, RMD)

参考扩散模块是AMD方法提升**多样性**的关键。该模块在逆向扩散过程中，不仅以文本 $c$ 为条件，还额外引入了从运动数据库中检索到的参考运动序列 $m^{1:R}$。检索过程基于解剖脚本的语义相似度，为当前文本描述找到最相关的简单动作参考。其逆向过程定义为：

$$p_{\theta_2}(x_{t-1}^{1:N} | x_t^{1:N}, c, m^{1:R}) = \mathcal{N}(x_{t-1}^{1:N}; \mu_\theta(x_t^{1:N}, c, m^{1:R}, t), \Sigma_\theta(x_t^{1:N}, c, t))$$

通过引入参考运动，该分支能够生成更丰富、更多样的动作变体，其输出记为 $p_{\theta_2}$。

### 4. 特征融合与输出选择模块 (Feature Fusion & Output Selection)

为了在保真度和多样性之间取得平衡，AMD设计了一个基于Transformer编码器层和残差连接的特征融合模块。该模块接收来自OMD和RMD的中间特征，以及原始文本和解剖脚本的嵌入，通过交叉注意力机制进行交互融合，最终生成融合后的输出。

在最终的运动序列生成阶段，AMD通过一个受伯努利分布控制的随机选择机制，动态地决定每一步是采用OMD的输出 $p_{\theta_1}$ 还是RMD的输出 $p_{\theta_2}$。该机制由可调参数 $\lambda \in [0, 1]$ 控制：

$$f(p_\theta, \lambda) = \begin{cases} 1-\lambda & \text{if } p_{\theta_1} \\ \lambda & \text{if } p_{\theta_2} \end{cases}$$

其中，$\lambda$ 表示选择 $p_{\theta_2}$ 的概率。

**参数 $\lambda$ 的作用机制**：该参数是调节生成行为的关键旋钮。当 $\lambda \to 0$ 时，模型几乎总是选择OMD的输出，生成结果严格遵循原始文本描述，保真度最高，但多样性降低；当 $\lambda \to 1$ 时，模型倾向于选择RMD的输出，参考动作的引导作用增强，生成结果的多样性显著提升，但可能偏离原始文本的精确语义。实验表明，随着 $\lambda$ 增大，FID指标会先快速下降后趋于平缓，验证了该融合策略的有效性。

## 实验与关键发现

### 核心实验设置

AMD 在四个数据集上进行评估：专门构建的复杂文本数据集 **SLCD1** 与 **SLCD2**，以及广泛使用的通用基准 **HumanML3D** 和 **KIT**。SLCD1/SLCD2 的文本长度分布显著长于 HumanML3D（见 Figure 4），专为检验模型处理长难描述的能力而设计。所有方法均使用真实运动长度，评估运行 20 次（Multimodality 运行 5 次），报告 95% 置信区间。对比基线包括 **MDM**（Tevet et al., arXiv 2022）、**TM2T**（Guo et al., ECCV 2022）、**MotionDiffuse**（Zhang et al., arXiv 2022）、**T2M-GPT**（Zhang et al., arXiv 2023）和 **ReMoDiffuse**（Zhang et al., arXiv 2023）。

### 主实验结果

**复杂文本场景（SLCD1/SLCD2）**：Table 1 展示了 AMD 在长难文本上的压倒性优势。在 SLCD1 上，AMD 的 FID 达到 **0.116±.011**，比次优模型 MDM 的 0.828±.061 降低了 **0.712**，降幅高达 86%。Multimodal Dist 同样大幅领先，AMD 为 4.296±.012，MDM 为 4.927±.059，差距为 0.631。在 SLCD2 上趋势一致，AMD 的 FID 为 0.146±.014，MDM 为 0.796±.065，差距为 0.650。这表明 LLM 驱动的解剖分解与双分支融合策略在应对复杂长文本时具有根本性优势——传统单编码器方法将任意复杂度的描述压缩为固定向量，必然丢失细粒度运动信息。

**通用基准（HumanML3D/KIT）**：Table 2 显示 AMD 在 HumanML3D 上保持竞争力，FID 为 0.515±.034，接近 ReMoDiffuse 的 0.495±.028，优于 MDM 的 0.544±.044。但在 KIT 上 AMD 表现低于预期（FID 1.243±.082），落后于 ReMoDiffuse 的 0.622±.045。论文将其归因于 KIT 数据集的文本相对简单，AMD 的解剖分解优势无法充分发挥，而额外的双分支结构可能引入不必要的复杂度。这一失败模式揭示了方法的适用边界：**当文本复杂度不足以触发分解收益时，双分支架构的额外自由度反而成为负担**。

### 消融实验

Table 3 系统验证了各模块的因果贡献（以 λ=0.5 为基线）：

- **去除文本分解（NTD）**：直接使用完整文本替代解剖脚本作为参考扩散分支的条件。FID 从 0.20±.03 恶化至 0.65±.07（上升 225%），Multimodal Dist 从 5.28±.03 升至 5.71±.03。这确证了解剖分解是处理复杂文本的核心机制——将长难描述拆解为简单解剖指令的组合，使扩散模型能更精准地定位每个身体部位的运动模式。

- **去除参考动作信息（NTDS）**：在参考扩散分支中移除检索到的参考运动，仅保留解剖脚本条件。FID 急剧恶化至 1.39±.08（上升 595%），Multimodal Dist 升至 5.83±.04。这表明检索增强为解剖脚本提供了关键的具身先验——脚本描述了“做什么”，而参考运动提供了“怎么做”的运动模式模板，二者缺一不可。

- **λ 参数调节（Figure 7）**：λ 控制两个扩散分支的输出频率。λ→0 时参考扩散分支主导，Diversity 上升但 FID 恶化，运动偏离真实分布；λ→1 时规范扩散分支主导，FID 快速下降后趋于平缓，Multimodality 降低。这一连续可调的保真度-多样性权衡机制是 AMD 的独特优势，用户可根据应用场景灵活配置。

![[assets/figures/papers/paper_list_l1814_AMD_Anatomical_Motion_Diffusion_with_Interpretable_Motion_Decomposition/figures/009_Figure_7.jpg]]
*Figure 7: As the λ value decreases, changes in the indicators*

### 定性分析

Figure 3 展示了 AMD 处理两类困难文本的能力：左侧为超长时序描述（包含多个连续子动作），右侧为语义丰富但非标准的描述（如“scorpion”动作）。AMD 生成的序列在时间连贯性和身体部位协调性上均表现良好，而基线方法（如 MDM）在类似输入上常出现动作缺失或语义错位。Figure 5 和 Figure 6 进一步展示了 AMD 在运动插值和运动编辑（固定下肢、编辑上肢）上的扩展能力，表明解剖分解带来的部位级可控性可迁移至其他任务。

![[assets/figures/papers/paper_list_l1814_AMD_Anatomical_Motion_Diffusion_with_Interpretable_Motion_Decomposition/figures/007_Figure_5.jpg]]
*Figure 5: In-between. The blue is the generate frames and the red is the input frames*

![[assets/figures/papers/paper_list_l1814_AMD_Anatomical_Motion_Diffusion_with_Interpretable_Motion_Decomposition/figures/010_Figure_6.jpg]]
*Figure 6: Motion editing. The lower limbs are fixed and only the upper limbs are edited*

### 关键局限

论文明确指出，AMD 的性能**严重受限于运动数据库的广度**。参考运动检索依赖于数据库中是否存在与解剖脚本匹配的高质量参考动作；小型或不均衡的数据库可能提供低质量参考，直接损害生成效果。这一瓶颈在 KIT 数据集上的相对弱势中已有体现——KIT 的动作类别有限，检索到的参考动作可能缺乏足够多样性。未来方向包括从长视频中自动蒸馏简单动作以降低数据收集成本，但该方案的实际可行性尚需验证。

![[assets/figures/papers/paper_list_l1814_AMD_Anatomical_Motion_Diffusion_with_Interpretable_Motion_Decomposition/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on the SLCD1 and SLCD2 test sets: All methods use the real motion length from the ground truth. → means results are better if the metric is closer to the real distribution. We ran all the evaluations 20 times (except MultiModality, which ran 5 times), and ± indicates the 95% confidence interval. Red indicates the best result, while Blue indicates the second-best result*

![[assets/figures/papers/paper_list_l1814_AMD_Anatomical_Motion_Diffusion_with_Interpretable_Motion_Decomposition/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison of AMD and baselines on HumanML3D and KIT datasets.(Guo et al.→Guo et al. (2022a),MDF→MotionDiffuse,ReMDF→ReMoDiffuse,MMD→Multimodality)*

## 定位与知识库关联

### 文本到运动生成的技术脉络

AMD 处于文本驱动人体运动生成这一快速发展的研究线上。该领域的主流范式长期依赖单一文本编码器将自然语言描述映射为固定长度的条件向量，再通过生成模型（VAE、GAN、扩散模型等）合成运动序列。代表性工作包括 **MDM** (Tevet et al., arXiv 2022)、**TM2T** (Guo et al., ECCV 2022)、**MotionDiffuse** (Zhang et al., arXiv 2022)、**T2M-GPT** (Zhang et al., arXiv 2023) 以及 **ReMoDiffuse** (Zhang et al., arXiv 2023)。这些方法的共同瓶颈在于：当面对长文本、语义丰富或包含罕见专业动作（如“scorpion”）的描述时，单一编码器难以充分捕获细粒度运动指令，导致生成质量急剧下降。

AMD 的核心突破在于**将问题从“编码复杂文本”转化为“分解文本并组合简单运动”**。它引入大语言模型（微调 ChatGPT-3.5）作为解剖知识源，将任意复杂度的文本描述拆解为一组解剖脚本（anatomical scripts），从而将长难文本生成问题降维为多个简单子运动的组合。这一思路与传统的“端到端编码-生成”范式形成根本性差异。

### 方法定位：双分支扩散与检索增强的融合

在扩散模型框架内，AMD 的设计可视为对标准条件扩散模型的**双分支扩展**。标准扩散模型（如 MDM）仅以原始文本 $c$ 为条件进行逆向去噪：

$$p_{\theta_1}(x_{t-1}^{1:N} | x_t^{1:N}, c) = \mathcal{N}(x_{t-1}^{1:N}; \mu_\theta(x_t^{1:N}, c, t), \Sigma_\theta(x_t^{1:N}, c, t))$$

AMD 在此基础上增设第二分支，同时以文本 $c$ 和检索到的参考运动 $m^{1:R}$ 为条件：

$$p_{\theta_2}(x_{t-1}^{1:N} | x_t^{1:N}, c) = \mathcal{N}(x_{t-1}^{1:N}; \mu_\theta(x_t^{1:N}, c, m^{1:R}, t), \Sigma_\theta(x_t^{1:N}, c, t))$$

两分支分别负责**保真度**（规范扩散，仅依赖原始文本）和**多样性**（参考扩散，依赖解剖脚本与检索运动），再通过伯努利分布参数 $\lambda$ 控制输出频率：

$$f(p_\theta, \lambda) = \begin{cases} 1-\lambda & \text{if } p_{\theta_1} \\ \lambda & \text{if } p_{\theta_2} \end{cases}$$

这种融合机制使 AMD 在保真度与多样性之间建立了**可调节的权衡**：$\lambda \to 0$ 时多样性上升但可能偏离真实分布，$\lambda \to 1$ 时保真度主导且 FID 快速下降（Figure 7）。这与 ReMoDiffuse 的检索增强思路有相似之处，但 AMD 的创新在于将检索与文本分解深度耦合，而非简单地将检索作为辅助条件。

### 适用边界

AMD 的优势场景明确集中于**长文本、语义复杂或包含罕见动作描述**的运动生成。在专门构建的复杂文本数据集 SLCD1 上，AMD 的 FID 达到 0.116，比次优模型 MDM（0.828）降低 0.712（Table 1）；在 SLCD2 上同样取得显著优势（FID 0.146）。此外，AMD 在标准数据集 HumanML3D 和 KIT 上也展现出竞争力（Table 2），表明其方法并未牺牲常规场景的性能。

然而，AMD 的适用边界同样清晰：
- **性能严重受限于运动数据库的广度**：参考扩散分支的质量直接取决于检索到的参考运动。若数据库规模不足或覆盖不全，低质量参考将损害生成效果。
- **对 LLM 分解质量的依赖**：解剖脚本的准确性是方法有效性的前提。对于 LLM 难以理解的极专业领域术语或模糊描述，分解质量可能下降，进而影响后续生成。

### 局限与开放问题

AMD 的主要局限在于**参考运动数据库的构建成本**。当前方法需要预先收集并标注简单动作片段，这在实际扩展中面临数据收集困难。论文提出的缓解方向是从长视频中蒸馏简单动作，但自动化蒸馏的可行性尚未验证。

消融实验（Table 3）进一步揭示了各组件的关键性：去除文本分解（NTD）导致 FID 从 0.20 升至 0.65，去除参考动作信息（NTDS）更使 FID 恶化至 1.39，表明两个核心设计均不可或缺。

值得关注的开放问题包括：
1. **解剖相似性的计算方式**：论文提到基于 Sentence-BERT（all-MiniLM-L6-v2）计算语义嵌入用于检索，但具体的相似度度量（余弦相似度？阈值选择？）未详细说明，需要进一步确认。
2. **数据库规模的定量影响**：目前缺乏对运动数据库大小与生成质量关系的系统实验，这限制了实际部署时的资源规划。
3. **自动化动作蒸馏**：能否从长视频中无监督地提取简单动作片段，摆脱人工标注依赖，是该方法走向大规模应用的关键。
4. **KIT 数据集性能异常**：论文提到在 KIT 上的表现低于预期（Table 2），原因尚不明确，可能与 KIT 的文本分布特征或数据库覆盖偏差有关，需进一步分析。

## 原文 PDF

![[paperPDFs/AAAI_2024/AMD_Anatomical_Motion_Diffusion_with_Interpretable_Motion_Decomposition_and_Fusion.pdf]]
