---
title: "A Style is Worth One Code: Unlocking Code-to-Style Image Generation with Discrete Style Space"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/A_Style_is_Worth_One_Code_Unlocking_Code_to_Style_Image_Generation_with_Discrete_Style_Space.pdf
project_link: "https://kwai-kolors.github.io/CoTyle/"
code_link: null
aliases:
- A_Style_is_Worth
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 数值风格代码作为紧凑风格控制信号，经离散风格码本和自回归风格生成器映射为风格嵌入，驱动扩散模型生成。
primary_logic: 将风格信息量化为离散码本并用自回归模型学习其分布，使数值代码成为风格唯一标识；将风格嵌入从文本分支注入以捕捉语义级风格特征，更符合人类感知。
claims:
- 训练离散风格码本时使用对比损失，使同风格嵌入相近、不同风格嵌入远离。
- 添加重建损失可防止码本坍塌，并保持风格嵌入与VLM图像嵌入一致。
- 自回归风格生成器在码本索引上训练，能生成全新的风格嵌入，实现代码到风格生成。
- 从文本分支注入风格信息比视觉分支更好地保留语义内容，提升风格一致性。
---

# A Style is Worth One Code: Unlocking Code-to-Style Image Generation with Discrete Style Space

> [!tip] 核心洞察
> 将风格信息量化为离散码本并用自回归模型学习其分布，使数值代码成为风格唯一标识；将风格嵌入从文本分支注入以捕捉语义级风格特征，更符合人类感知。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一个风格值一个代码：通过离散风格空间解锁代码到风格图像生成 |
| 英文题名 | A Style is Worth One Code: Unlocking Code-to-Style Image Generation with Discrete Style Space |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.10555) · [Project](https://kwai-kolors.github.io/CoTyle/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CoTyle |
| Dataset | 代码到风格生成（500个风格代码） |

> [!tip] 效果简介
> - 代码到风格生成（500个风格代码） 上，风格一致性 (CSD) 0.6007 vs 0.4734 (Midjourney) (+0.1273)；风格多样性 (1-CSD) 0.7764 vs 0.8088 (Midjourney) (-0.0324)。
> - 图像条件风格生成（500对） 上，风格一致性 (CSD) 0.5791 vs 0.5753 (InstantStyleXL) (+0.0038)；Aesthetics 0.7178 vs 0.7636 (Flux-Kontext) (-0.0458)；CLIP-T 0.3230 vs 0.3331 (USO) (-0.0101)。

## 概要

**问题瓶颈**：现有风格生成方法——无论是文本描述、参考图像还是 LoRA——都难以同时满足高一致性、创造性与可复现性这三个核心需求。文本提示难以精确描述风格细节，参考图像限制了风格迁移的自由度，而 LoRA 则依赖繁琐的微调且无法生成全新风格。风格表示本身的复杂性使得“创造新风格”成为一个尚未被有效解锁的能力。

**核心洞察**：CoTyle 提出将风格信息压缩为**数值风格代码（numerical style code）**，使其成为风格的唯一标识符。这一设计的因果机制在于：通过离散风格码本将连续的风格特征量化为有限词汇表，再利用自回归变换器学习码本索引的分布，从而将“生成新风格”转化为“采样新的代码序列”。风格嵌入从 VLM 的文本分支注入扩散模型，而非传统的视觉分支，使模型能捕捉更符合人类直觉的语义级风格特征。

**方法定位**：CoTyle 由三个模块构成——（1）**离散风格码本**，用对比损失与重建损失从图像对中提取风格嵌入；（2）**条件文本到图像扩散模型**，接受风格嵌入与文本提示生成风格化图像；（3）**自回归风格生成器**，在码本索引上以 next-token prediction 方式学习风格分布，实现从随机代码到全新风格的映射。推理时引入高频索引抑制策略以增强多样性。

**主要结果**：在代码到风格生成任务上，CoTyle 的风格一致性（CSD）达到 0.6007，显著优于 Midjourney 的 0.4734（+0.1273），但风格多样性略低（0.7764 vs 0.8088）。在图像条件风格生成上，CoTyle 与 InstantStyleXL 的一致性相当（0.5791 vs 0.5753）。消融实验证实：文本分支注入优于视觉分支（一致性 +0.0485），对比损失是风格学习的关键（移除后一致性降至 0.4890），高频抑制有效提升多样性（+0.0276）。



### 风格生成的核心瓶颈

文本到图像（T2I）扩散模型已在图像生成领域取得巨大成功，但**风格控制**仍是一个尚未充分解决的难题。风格是一种高度抽象且难以形式化的视觉属性，它不同于物体类别或空间布局，无法通过简单的文本描述精确捕捉。现有方法在指定和生成风格时面临一个根本性的三难困境：

- **文本描述**（如“油画风格”“赛博朋克风”）虽然使用便捷，但语言的粗糙粒度无法传达风格的微妙细节，且不同用户对同一描述的理解存在偏差，导致生成结果不可复现。
- **参考图像**（如 StyleStudio、CSGO、USO、InstantStyleXL、Flux-Kontext 等基于图像条件的风格迁移方法）能提供更精确的风格信息，但需要用户事先拥有一张恰好体现目标风格的图像，这限制了创造性——用户无法生成一种“尚未存在”的全新风格。
- **LoRA 微调**虽然能高度一致地复现特定风格，但每次适配新风格都需要额外的训练开销和模型存储，且同样无法创造新风格。

如图 Figure 2 所示，现有方案在**一致性**（Consistency）、**创造性**（Creativity）和**可复现性**（Reproducibility）三个维度上难以兼得：文本描述可复现但缺乏一致性与创造性；参考图像具有一致性但缺乏可复现性与创造性；LoRA 一致且可复现但完全不具备创造性。这一缺口构成了风格生成领域的核心瓶颈。

### 核心洞察：风格可被量化为离散代码

本工作提出一个关键洞察：**风格信息可以被压缩为一组紧凑的离散数值代码**，就像自然语言中的词汇一样，每个代码对应风格空间中的一个“原子”属性。如果能够构建一个离散的风格码本（style codebook），将任意图像的风格映射为固定长度的代码序列，并学习这些代码的联合分布，那么：

1. **一个风格值一个代码**：每个风格由一个唯一的数值代码标识，用户只需修改代码即可精确复现或切换风格，无需复杂的文本描述、参考图像或模型微调。
2. **代码到风格生成**：通过学习风格代码的分布，可以从随机种子出发自回归地采样全新的代码序列，从而生成训练数据中从未出现过的全新风格，解锁创造性维度。
3. **语义级风格注入**：将风格嵌入通过视觉语言模型（VLM）的文本分支注入扩散模型，而非传统的视觉分支，使模型能够捕捉与人类直觉更一致的语义级风格特征。

### CoTyle 的定位

基于上述洞察，本文提出 **CoTyle**（Code-to-Style Generation），首次将风格生成问题形式化为“代码到风格”的映射任务。CoTyle 的核心贡献在于构建了一个完整的离散风格表示与生成框架，使数值风格代码成为风格的唯一标识和操控接口，从而在一致性、创造性和可复现性三个维度上实现突破。



## 核心方法与创新机理

CoTyle 的核心创新在于将“风格”这一高维、模糊的感知属性**量化为一个紧凑的数值代码**，并构建了一个完整的“代码到风格”（code-to-style）生成范式。这与现有方法形成了根本性的区别：传统方法依赖复杂的文本描述、参考图像或定制化的 LoRA 权重来传递风格，而 CoTyle 仅需一个离散的数值代码即可作为风格的唯一标识，兼具高一致性、创造性和可复现性（Figure 2）。

为实现这一范式，CoTyle 引入了三个相互协同的关键机制，分别对应风格表示、风格注入和新风格生成这三个核心环节。

**1. 离散风格码本：将风格压缩为紧凑代码**

CoTyle 设计了一个**离散风格码本**（Vocabulary=1024, dim=64），将视觉基础模型（VLM）提取的图像特征量化为离散的风格嵌入。这是整个框架的基石。

其训练机制是保证风格表示质量的关键：
- **对比损失**：强制同风格、不同内容的图像在嵌入空间中彼此靠近，而不同风格的图像相互远离，使码本学会分离风格与内容。
- **重建损失**：防止码本训练坍塌，并强制风格嵌入与 VLM 图像编码器的输出保持接近，保留语义信息。
- **向量量化损失**：完成从连续特征到离散码本索引的映射。

训练完成后，一张风格参考图像被编码为一组离散的码本索引序列，这些索引即成为该风格的“代码”。

**2. 文本分支风格注入：语义级风格控制**

CoTyle 将风格嵌入视为一种**文本形式的输入**，通过 VLM 的文本分支注入扩散 Transformer（DiT），而非沿袭主流方法将风格条件注入视觉分支。

这一设计基于一个核心洞察：通过文本模态注入风格信息，模型能更好地捕捉与人类直觉一致的语义级风格特征，同时更忠实地保留提示词中的内容语义。消融实验证实了该设计的有效性——从文本分支注入风格比视觉分支获得了更高的风格一致性（CSD：0.5791 vs 0.5306），且视觉分支注入更容易导致内容信息的丢失（Figure 5, Table 2）。

**3. 自回归风格生成器：从代码到全新风格**

CoTyle 在离散码本索引序列上训练了一个**自回归风格生成器**（基于 Qwen2-0.5B），以“下一个索引预测”的方式学习风格码本索引的分布。推理时，用户只需提供一个风格代码作为随机种子，生成器即可自回归地预测出完整的风格索引序列，映射为一个全新的风格嵌入。

这一机制使 CoTyle 首次实现了真正意义上的“代码到风格”生成——无需任何参考图像或文本描述，仅凭一个数值代码就能创造出独特的、从未见过的风格。

**4. 高频索引抑制：增强风格多样性**

CoTyle 发现，风格码本中存在一些被高频选中的索引，它们并不编码具体的风格属性，而是充当“无风格占位符”——仅使用这些高频索引生成的图像与无风格条件的普通 T2I-DM 输出几乎一致（Figure 7）。

为提升生成风格的多样性和强度，CoTyle 在推理时引入**高频索引抑制策略**：对频率超过阈值 τ 的索引，将其 logits 乘以一个指数衰减的抑制系数 $s(i) = e^{-k (f(i) - \tau)}$，从而降低这些无意义索引被采样的概率。消融实验表明，该策略将风格多样性从 0.7488 提升至 0.7764（Table 4）。



CoTyle 的核心设计理念是将“风格”抽象为一个紧凑的**数值风格代码**（numerical style code），使风格指定脱离复杂的文本描述、参考图像或 LoRA 适配器（Figure 2）。整个框架由三个依次训练、推理时协同工作的模块构成，其训练与推理流程如 Figure 3 所示。

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/002_Figure_2.jpg]]
*Figure 2: Different to previous methods, CoTyle uses a numerical style code to represent a style, eliminating the need for complex prompts, images, or LoRAs, and allowing easy creation of unique styles just modifying the code. “Creativity”, “Consistency”, and “Reproducibility” refer to a model’s ability to (1) generate novel styles, (2) produce multiple images in the same style consistently, and (3) reproduce styles using simple, user-friendly style definitions*

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/003_Figure_3.jpg]]
*Figure 3: Overview of CoTyle. (a) We first train a style codebook and an image generation model conditioned on style images. (b) Then, we use the corresponding codebook indices of the style images to train an autoregressive style generator. (c) During inference, a style code is used to randomly sample the first index and autoregressively predict the rest*

### 1. 离散风格码本

第一阶段训练一个**离散风格码本**（Style Codebook），词汇量 $V = 1024$，嵌入维度 $d = 64$。码本以成对风格图像作为输入，利用 VLM 的图像编码器提取 ViT 特征，通过向量量化（VQ）将连续视觉特征压缩为离散的风格嵌入。训练损失由三项加权构成：

$$
\mathcal{L}_{\mathrm{style}} = \mathcal{L}_{\mathrm{contrast}} + \alpha \mathcal{L}_{\mathrm{recon}} + \beta \mathcal{L}_{\mathrm{vq}}
$$

其中**对比损失** $\mathcal{L}_{\mathrm{contrast}}$ 强制同风格图像对的嵌入在余弦空间中靠近、不同风格对远离，使码本学习到语义级的风格区分能力；**重建损失** $\mathcal{L}_{\mathrm{recon}}$ 强制量化后的风格嵌入与原始 ViT 特征保持高余弦相似度，防止码本坍塌并确保嵌入不偏离 VLM 的图像语义空间；$\mathcal{L}_{\mathrm{vq}}$ 为标准 VQ 的码本学习损失。码本训练完成后，任意风格图像均可被编码为一组离散的码本索引序列，成为该风格的紧凑标识。

### 2. 条件文本到图像扩散模型

第二阶段训练一个以风格嵌入为条件的**文本到图像扩散模型**（T2I-DM）。关键设计选择是**将风格嵌入作为文本模态输入，通过 VLM 的文本分支注入 DiT**，而非沿视觉分支（如噪声特征拼接）注入。论证依据是：文本分支的语义抽象能力使模型捕捉到更符合人类直觉的风格属性，在保持内容语义完整性方面显著优于视觉分支注入（Figure 5, Table 2）。该模型在训练时以风格图像作为条件，学会将码本输出的风格嵌入映射为具有一致风格的生成图像。

### 3. 自回归风格生成器

第三阶段训练一个**自回归风格生成器**，基于 Qwen2-0.5B 架构，以码本索引序列为监督信号，在“下一个索引预测”目标下学习风格码本索引的联合分布。训练数据来自第二阶段所用风格图像经码本编码得到的索引序列。该生成器是解锁“代码到风格生成”的关键——推理时，给定一个随机种子作为初始风格代码，生成器自回归地预测完整的索引序列，再经码本解码为风格嵌入，驱动扩散模型生成具有**全新风格**的图像。此过程无需任何参考图像，仅依靠数值代码即可创造训练集中未见过的风格。

### 推理采样策略

推理时，自回归风格生成器从风格代码中随机采样第一个索引，并逐令牌预测剩余序列。为提升生成风格的多样性与强度，引入**高频码本索引抑制策略**：对训练集中出现频率超过阈值 $\tau$ 的码本索引施加指数衰减系数 $s(i) = e^{-k(f(i) - \tau)}$，降低其在采样中的 logit 权重。实验证实，高频索引本身不编码具体风格属性，仅作为占位符存在——仅用高频索引生成的图像与无风格条件的 T2I-DM 输出几乎一致（Figure 7），抑制它们可迫使生成器探索更具风格辨识度的索引组合（Table 4：多样性从 0.7488 提升至 0.7764）。

### 数据流总结

**训练流**：风格图像对 → 码本训练（$\mathcal{L}_{\mathrm{style}}$）→ 风格嵌入 → 注入 T2I-DM 文本分支训练；同时，风格图像经训练后码本编码为索引序列 → 训练自回归风格生成器。

**推理流**：风格代码（随机种子）→ 自回归风格生成器（含高频抑制）→ 风格索引序列 → 码本解码 → 风格嵌入 → 注入 T2I-DM 文本分支 → 风格化图像。该框架同时兼容图像条件输入：直接将参考图像经码本编码为风格嵌入，跳过自回归生成步骤即可。



CoTyle 围绕“风格即代码”这一核心思想，由三个紧密协作的模块构成：**风格码本**、**条件文本到图像扩散模型**以及**自回归风格生成器**。其设计瓶颈在于，如何将连续、复杂的视觉风格信息压缩为一个紧凑的离散表示，并使其既能被扩散模型有效利用，又能被生成模型采样以创造全新风格。

### 风格码本：从图像对中解耦风格

风格码本的目标是从成对的风格图像中提取出与内容无关、仅表征风格的离散嵌入。其训练流程如下：对于一组来自同一风格的图像对 $(\mathbf{I}_1, \mathbf{I}_2)$，首先通过冻结的视觉语言模型图像编码器提取特征 $\mathbf{v}_1$ 和 $\mathbf{v}_2$。随后，$\mathbf{v}_1$ 经过码本 $\mathcal{F}$ 进行向量量化，得到量化后的风格嵌入 $\mathcal{F}(\mathbf{v}_1)$。该嵌入被期望与 $\mathbf{v}_2$ 在风格维度上高度一致。

为了达成这一目标，码本训练引入了**对比损失**与**重建损失**的双重约束。

**对比损失** $\mathcal{L}_{\mathrm{contrast}}$ 负责塑造风格空间的结构：它强制同风格图像对的嵌入彼此靠近，而不同风格图像对的嵌入相互远离。其形式为：

$$
\mathcal{L}_{\mathrm{contrast}} = \frac{1}{B} \sum_{i=1}^{B} \left[ y_i \cdot (1 - s_i)^2 + (1 - y_i) \cdot \left( \mathrm{ReLU}(s_i - m) \right)^2 \right]
$$

其中，$B$ 为批次大小，$y_i \in \{0,1\}$ 为风格标签（1 表示同风格，0 表示不同风格），$m$ 为边界超参数。核心变量 $s_i$ 是量化风格嵌入与第二张图像视觉语言模型特征之间的余弦相似度：

$$
s_i = \frac{\mathcal{F}(\mathbf{v}_{1,i}) \cdot \mathbf{v}_{2,i}}{\|\mathcal{F}(\mathbf{v}_{1,i})\| \|\mathbf{v}_{2,i}\|}
$$

当 $y_i=1$ 时，损失惩罚 $s_i$ 偏离 1；当 $y_i=0$ 时，损失惩罚 $s_i$ 超过边界 $m$。这确保了风格嵌入的判别性。

**重建损失** $\mathcal{L}_{\mathrm{recon}}$ 则扮演“防坍缩”角色。它强制量化后的风格嵌入 $\mathcal{F}(\mathbf{v}_1)$ 与原始图像特征 $\mathbf{v}_1$ 保持接近，避免码本在训练中退化：

$$
\mathcal{L}_{\mathrm{recon}} = \frac{1}{N} \sum_{i=1}^{N} \left[ \frac{\mathcal{F}(\mathbf{v}_{1,i}) \cdot \mathbf{v}_{1,i}}{\|\mathcal{F}(\mathbf{v}_{1,i})\| \|\mathbf{v}_{1,i}\|} \right]^2
$$

最终，风格码本的总损失 $\mathcal{L}_{\mathrm{style}}$ 为上述损失与标准向量量化损失 $\mathcal{L}_{\mathrm{vq}}$ 的加权和：

$$
\mathcal{L}_{\mathrm{style}} = \mathcal{L}_{\mathrm{contrast}} + \alpha \mathcal{L}_{\mathrm{recon}} + \beta \mathcal{L}_{\mathrm{vq}}
$$

通过这一损失组合，码本（词汇量 1024，嵌入维度 64）得以将图像风格凝练为一组离散的、具有语义结构的索引序列。

### 条件扩散模型：从文本分支注入风格

获得风格嵌入后，下一个关键设计是**如何将其注入扩散模型**。CoTyle 选择将风格嵌入视为一种特殊的“文本输入”，通过视觉语言模型的**文本分支**注入扩散变换器。这与先前工作通过视觉分支（如将风格特征与噪声潜变量在通道维度拼接）的做法形成根本区别。消融实验证实，文本分支注入能更好地保留图像的语义内容，并在风格一致性指标上取得显著提升（0.5791 vs. 0.5306），因为文本模态的条件信号更擅长捕捉符合人类直觉的风格属性。

### 自回归风格生成器：从代码到新风格

上述码本只能为已有图像提取风格。为了实现“代码到风格”的创造能力，CoTyle 引入一个基于 Qwen2-0.5B 的自回归变换器作为**风格生成器**。它以码本索引序列为训练目标，在下一个索引预测任务下学习风格索引的联合分布。推理时，用户只需提供一个随机种子作为初始风格代码，生成器便会自回归地预测出完整的风格索引序列，再经码本映射为风格嵌入，驱动扩散模型生成全新风格的图像。

### 高频索引抑制：解锁风格多样性

分析发现，码本中存在大量高频但无具体风格属性的“占位符”索引——仅使用这些索引生成的图像与无风格条件的普通文本到图像模型输出几乎无异。为了提升生成风格的多样性和强度，CoTyle 在推理时对高频索引施加**抑制策略**。对于频率 $f(i)$ 超过阈值 $\tau$ 的索引 $i$，其 logits 会被乘以一个衰减系数 $s(i)$：

$$
s(i) = \begin{cases} 1, & \text{if } f(i) < \tau \\ e^{-k (f(i) - \tau)}, & \text{if } f(i) \geq \tau \end{cases}
$$

其中 $k$ 控制衰减速率。这一简单策略有效压低了无意义索引的采样概率，迫使生成器探索更具风格表征能力的低频索引，从而将风格多样性从 0.7488 提升至 0.7764。

### 补充图表

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/006_Figure_5.jpg]]
*Figure 5: We compare injecting style through textual branch with the existing method through visual branch. Injecting style from the textual branch better preserves semantic information*

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/011_Figure_7.jpg]]
*Figure 7: Sampling solely from high-frequency indices yields style-less images. Row 1 shows the results of vanilla T2I-DM without any style indices, and Row 2, guided by high-frequency indices, produces results nearly identical to T2I-DM*



## 实验与关键发现

### 主要定量结果

CoTyle 在代码到风格生成和图像条件风格生成两个设定下与多个基线进行了比较，核心指标为风格一致性（CSD）、风格多样性（1-CSD）、美学质量（Aesthetics）和图文对齐（CLIP-T）。完整数据见 Table 1。

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with other methods. “ * ” denotes CoTyle conditioned on reference images. Bold highlights the best score; underlines “ ” indicate the second-highest, omitted in code-to-style evaluation for brevity. CLIP-T measures text-image alignment. For image-conditioned methods, diversity is constrained by the reference image and is neither measurable nor meaningful to evaluate*

在代码到风格生成任务上，CoTyle 的风格一致性达到 0.6007，显著优于 Midjourney 的 0.4734（+0.1273），表明离散风格码本与自回归生成器能够为同一风格代码产生更一致的风格表达。但在风格多样性上，CoTyle 为 0.7764，略低于 Midjourney 的 0.8088（-0.0324），说明闭源商业方案在探索风格空间广度上仍有优势。这一差距的根本原因在于自回归风格生成器是在有限数据集构建的码本索引上训练的，未能充分覆盖人类艺术表达的广泛多样性。

在图像条件风格生成任务上，CoTyle 的风格一致性为 0.5791，与最强的图像条件基线 InstantStyleXL（0.5753）基本持平（+0.0038），证明从文本分支注入风格嵌入的策略在该设定下同样有效。美学质量方面，CoTyle 为 0.7178，低于 Flux-Kontext 的 0.7636（-0.0458）；CLIP-T 为 0.3230，略低于 USO 的 0.3331（-0.0101）。这些差距提示码本量化过程可能损失了部分细粒度风格细节，影响了生成图像的视觉质量。

### 风格注入分支消融

一个关键的设计选择是将风格嵌入从文本分支而非视觉分支注入 DiT。Table 2 的消融实验直接验证了这一选择：文本分支注入的风格一致性为 0.5791，而使用 OminiControl 方式从视觉分支注入（将噪声特征与风格条件特征沿 token 维度拼接）仅获得 0.5306。Figure 5 的视觉效果进一步揭示了两者的本质差异——视觉分支注入倾向于将风格信号施加为全局纹理变换，容易破坏物体的语义结构；而文本分支注入借助 VLM 文本编码器对语义级特征的表征能力，使风格属性与内容语义更好地解耦，从而在保持物体形状和布局的同时传递风格特征。这一发现与论文的核心洞察一致：“conditioning on text enables the model to capture stylistic attributes that better align with human intuition”。

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/007_Table_2.jpg]]
*Table 2: Comparison of injecting style condition to DiT through visual branch and textual branch*

### 风格损失函数消融

风格码本训练中对比损失的负样本部分至关重要。Table 3 显示，移除对比损失中的负样本项后，风格一致性从 0.5791 骤降至 0.4890。这证实了仅靠正样本拉近同风格嵌入不足以建立有判别力的风格空间——负样本的推远机制（通过 ReLU 边界 $m$ 约束）是防止不同风格嵌入坍缩到同一区域的关键。同时，重建损失 $\mathcal{L}_{\mathrm{recon}}$ 的作用也不可忽视：它强制量化后的风格嵌入与原始 VLM 图像特征保持余弦相似，在实验中表现为“adding a reconstruction loss is essential to avoid codebook collapse during training”。

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/008_Table_3.jpg]]
*Table 3: Effect of style loss*

### 高频索引抑制策略

推理时的采样策略对生成风格的多样性有显著影响。分析发现，风格码本的索引频率分布极不均匀（Figure A1），存在大量高频索引。这些高频索引在训练中频繁被选中，但并不编码具体的风格属性——仅用高频索引生成的图像与无条件 T2I-DM 的输出几乎一致（Figure 7），说明它们实质上是“风格无关”的占位符。基于这一发现，CoTyle 在推理时对频率超过阈值 $\tau$ 的索引施加指数衰减抑制系数 $s(i) = e^{-k(f(i)-\tau)}$。Table 4 的消融表明，该策略将风格多样性从 0.7488 提升至 0.7764，同时保持风格一致性基本不变。这一机制确保了自回归生成器在采样时更倾向于选择携带具体风格信息的低频索引，从而增强生成风格的多样性和强度。

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/009_Table_4.jpg]]
*Table 4: Effect of high-frequency suppression s(i)*

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/013_Figure.jpg]]
*Figure: A1. Frequency distribution of style codebook indices. A batch of images is encoded using the style codebook, and the selection frequency of all indices is calculated*

### 定性分析与失败模式

Figure 4 展示了 CoTyle 与 Midjourney 在代码到风格生成上的定性对比。CoTyle 在同一风格代码下生成的图像组（2×3 网格）表现出良好的一致性，但在某些风格类型上（图中红色框标注）一致性欠佳，表现为颜色基调或纹理特征在不同图像间漂移。Figure 6 的图像条件生成对比显示，CoTyle 能够同时忠实遵循输入文本的语义内容和参考图像的风格特征，但在复杂混合风格场景下，码本量化的信息瓶颈可能导致某些细微风格元素被弱化或丢失。

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison with Midjourney [2] on code-to-style generation. Each image set (2×3 grid) is generated from the same style code. Red boxes highlight cases with suboptimal style consistency*

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative comparison. CoTyle is not only capable of generation conditioned on style codes but also supports style images. Our model can faithfully follow the input text while simultaneously generating the specified style*

风格插值是 CoTyle 的一个独特能力（Figure 8）。通过按用户指定权重线性组合多个风格的码本索引子集，模型可以在两个风格之间实现平滑过渡。附录 Figure A3 提供了更多插值结果，Figure A2 则分析了 token 选择策略对插值效果的影响。这一能力源于自回归生成器将每个风格表示为 $N$ 个索引序列的设计，使风格融合退化为索引级别的组合操作。

![[assets/figures/papers/paper_list_l2066_https_arxiv_org_abs_2511_10555/figures/012_Figure_8.jpg]]
*Figure 8: Style interpolation. The leftmost and rightmost images represent two distinct styles. CoTyle enables smooth style interpolation by linearly combining multiple style indices according to user-specified weights. See more results in Appendix*

### 评估局限

需要指出的是，当前评估仅依赖无参考指标 CSD，该指标基于 VLM 特征空间的相似度计算，可能无法完全反映人类对风格感知的细微差异。此外，训练数据的多样性受限可能引入某些风格偏向，导致模型在某些艺术风格类型上表现优于其他类型。这些因素在解读定量结果时需加以注意。



## 定位与知识库关联

### 风格生成的三种范式与CoTyle的定位

风格化图像生成方法可按风格指定方式分为三类：**文本描述**（如“油画风格”）、**参考图像条件**（从给定图片提取风格特征）、以及**参数化风格表示**（如LoRA微调）。CoTyle引入第四种范式——**数值风格代码**，将风格压缩为离散码本中的索引序列，使一个整数序列即可唯一标识并复现一种风格（Figure 2）。

与LoRA方法相比，CoTyle无需为每种风格训练独立的模型权重，避免了风格切换时的存储与切换成本。与图像条件方法相比，CoTyle不依赖参考图像，因此能生成训练数据中未出现的新风格——这是其“创造性”维度的核心优势。

### 与基线方法的关系

在**图像条件风格生成**任务上，CoTyle与以下方法直接可比：

- **InstantStyleXL**：通过解耦交叉注意力实现图像条件风格注入。CoTyle在风格一致性（CSD 0.5791 vs 0.5753）上略优，但美学评分（0.7178 vs 0.7636）低于Flux-Kontext（Table 1）。这提示从文本分支注入风格信息虽然更好地保留了语义级风格特征，但在视觉美感优化上仍有提升空间。

- **CSGO**、**USO**、**StyleStudio**：均为图像条件风格迁移方法，CoTyle在风格一致性上与之相当或略优，但CLIP-T文本对齐指标（0.3230）略低于USO（0.3331），表明风格嵌入的注入可能对文本遵循度产生轻微干扰。

在**代码到风格生成**任务上，仅Midjourney提供可比功能（通过`--sref`参数接受随机种子作为风格代码）。CoTyle在风格一致性上显著优于Midjourney（CSD 0.6007 vs 0.4734，+26.9%），但风格多样性略低（1-CSD 0.7764 vs 0.8088，-4.0%）。这一差距的核心原因在于：CoTyle的自回归风格生成器训练数据受限于构建风格码本所用的图像集合，而Midjourney的训练数据规模与多样性远超当前开源方案。

### 技术谱系溯源

CoTyle的技术架构可分解为三条技术线的交汇：

1. **离散表示学习**：风格码本的设计继承自VQ-VAE的向量量化范式，但CoTyle的创新在于将量化对象从像素级重建转向**风格级语义**——通过对比损失使同风格嵌入聚集、不同风格嵌入分离（Equation 1），并通过重建损失防止码本坍塌（Equation 3）。这与VQGAN等面向重建的码本有本质区别。

2. **自回归生成**：风格生成器采用类似ImageGPT的next-token prediction框架，但预测对象不是图像像素token，而是**风格码本索引**。这使得风格空间本身成为可建模的分布，风格代码成为该分布的采样结果。CoTyle选择Qwen2-0.5B作为骨干，体现了利用预训练语言模型的序列建模能力来捕捉风格共现模式的思路。

3. **扩散模型条件注入**：CoTyle将风格嵌入从**文本分支**注入DiT，而非视觉分支。消融实验（Table 2）表明这一选择至关重要：文本分支注入的CSD为0.5791，视觉分支仅为0.5306。其机理在于，VLM文本编码器在预训练中已学会将语义概念映射到结构化表示空间，风格嵌入借此空间进行插值，能更自然地捕捉“风格”这类高层语义属性（Figure 5）。

### 适用边界与局限

**适用场景**：
- 需要大量不同风格、且追求风格可复现性的应用（如游戏资产生成、品牌视觉设计）
- 风格插值与融合（Figure 8）：通过线性组合不同风格的索引子集，可实现平滑的风格过渡
- 作为风格搜索引擎的底层表示：数值代码天然适合索引与检索

**已知局限**：

1. **风格多样性上限**：自回归生成器在有限风格数据上训练，其生成的风格分布受限于训练集。与Midjourney的多样性差距（-4.0%）表明，仅靠码本建模无法弥补训练数据广度不足的问题。

2. **量化损失**：码本将连续的风格特征量化为1024个离散向量（dim=64），这一压缩过程不可避免丢失细节。对于混合风格或微妙风格差异，量化后的表示可能无法完整保留。

3. **缺乏直观控制**：当前用户只能通过随机采样风格代码来探索风格空间，无法指定“更温暖”“更粗犷”等语义属性。风格代码对用户而言是不透明的。

4. **高频索引占位符现象**：实验发现（Figure 7, Figure A1），部分码本索引在训练中被高频使用，但它们不编码具体风格属性——仅用这些索引生成的图像与无条件T2I-DM几乎一致。尽管高频抑制策略（Equation 5）缓解了该问题（多样性从0.7488提升至0.7764），但这一现象本身说明码本容量未被充分利用。

### 开放问题

1. **数据扩展策略**：如何以低成本扩展风格训练数据的多样性？合成数据增强、跨数据集风格迁移、或利用LLM生成风格描述以引导数据收集，是可能的方向。

2. **码本容量与粒度**：增大词汇量（>1024）或引入层次化码本是否能减少量化损失？更大的码本会增加自回归生成器的建模难度，需要在表示精度与生成质量间权衡。

3. **可解释风格空间**：能否在隐空间中建立风格属性轴（如“写实-抽象”、“暖-冷”），使用户能有意义地导航和编辑风格？这可能需要额外的属性标注或解耦表示学习。

4. **跨模态拓展**：该离散风格表示框架是否能迁移到音频风格（如音乐流派）、视频风格（如导演风格）？核心挑战在于其他模态的“内容-风格”解耦是否如视觉领域一样自然。

5. **高频索引的根本解决**：高频索引作为占位符的现象是否源于对比损失的设计缺陷，还是训练数据中“无风格”样本的固有属性？熵正则化或重新加权采样策略是否能从根本上改善码本利用率？



## 原文 PDF

![[paperPDFs/CVPR_2026/A_Style_is_Worth_One_Code_Unlocking_Code_to_Style_Image_Generation_with_Discrete_Style_Space.pdf]]
