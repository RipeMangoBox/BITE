---
title: Disentangled Hierarchical VAE for 3D Human-Human Interaction Generation
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Disentangled_Hierarchical_VAE_for_3D_Human_Human_Interaction_Generation_86bc618f301e.pdf
project_link: null
code_link: "https://github.com/ZenGengChin/dhvae-official"
aliases:
- DDHVA
- DHV3HHIG
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 通过引入解耦层次潜在变量（个体动作 z_a、z_b 和全局交互 z_o）并结合对比学习，显式分离个体运动与全局交互，从而在潜在空间中增强交互语义建模和物理一致性。
primary_logic: 显式解耦个体动作和全局交互为独立的潜在变量，利用 CoTransformer 进行双向感知编码，并通过对比学习约束全局交互潜变量 z_o，可以有效提升生成运动的文本对齐度、动作保真度和物理合理性。
claims:
- 将 DHVAE 替换为扁平 VAE (MLD-VAE) 后，重建 FID 从 0.503 大幅上升至 1.024，证明解耦层次潜在空间的关键作用。
- 移除对比学习导致全局交互潜变量 z_o 的歧化，生成的手部无法正确接触，物理合理性显著下降。
- 缺少 CoTransformer 或 z_o 时，重建与生成指标均大幅下降，确认层次化交互建模的必要性。
- InterHuman 上 FID ↓ = 5.015 ± .085
---

# Disentangled Hierarchical VAE for 3D Human-Human Interaction Generation

> [!tip] 核心洞察
> 显式解耦个体动作和全局交互为独立的潜在变量，利用 CoTransformer 进行双向感知编码，并通过对比学习约束全局交互潜变量 z_o，可以有效提升生成运动的文本对齐度、动作保真度和物理合理性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 解耦层次变分自编码器用于3D人体交互生成 |
| 英文题名 | Disentangled Hierarchical VAE for 3D Human-Human Interaction Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=53eIDko6N5) · [Code](https://github.com/ZenGengChin/dhvae-official) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | DHVAE (Disentangled Hierarchical Variational Autoencoder) |
| Dataset | InterHuman, InterX |

> [!tip] 效果简介
> - InterHuman 上，FID ↓ 5.015 ± .085 vs 5.153 ± .061 (InterMask) (-0.138)；R‑Prec@1 ↑ 0.496 ± .004 vs 0.449 ± .004 (InterMask) (+0.047)；接触比率 (Contact) ↑ 0.581 vs 0.468 (InterMask) (+0.113)。
> - InterX 上，FID ↓ 0.339 ± .026 vs 1.295 ± .038 (InterMask) (-0.956)。

## 概要

三维人体-人体交互（HHI）生成旨在根据文本描述合成双人协同运动序列。现有方法——无论是基于原始运动空间的扩散模型（如 **InterGen**、**TIMotion**）还是潜在扩散模型（如 **InterLDM**、**InterMask**）——普遍将所有运动信息压缩到**单一扁平潜在表示**中。这一设计存在根本性瓶颈：个体身份与交互上下文被不可分地纠缠，导致细粒度动作丢失、语义不对齐，并频繁产生穿透、接触缺失等物理不真实现象。

本文提出 **DHVAE（Disentangled Hierarchical Variational Autoencoder）**，核心思路是**显式解耦个体运动与全局交互**为三个潜在变量：个体运动潜变量 $\mathbf{z}_a$、$\mathbf{z}_b$ 和全局交互潜变量 $\mathbf{z}_o$。通过 CoTransformer 交叉注意力模块实现双向感知的交互建模，并引入**对比学习三元组损失**约束 $\mathbf{z}_o$ 的潜在空间，使其编码物理合理的接触语义。

在 InterHuman 和 InterX 两个基准数据集上，DHVAE 在 FID、R-Precision、Multimodal Distance 等主要指标上达到最优性能。具体而言，在 InterHuman 上 FID 降至 5.015，R-Prec@1 提升至 0.496；在更具挑战的 InterX（SMPLX 表示）上，FID 从 InterMask 的 1.295 大幅降至 0.339。物理合理性方面，接触比率从 0.468 提升至 0.581，穿透体积显著降低。消融实验证实：将解耦层次潜在空间替换为扁平 VAE 后，重建 FID 从 0.503 恶化至 1.024，生成 FID 从 5.015 升至 6.433，验证了解耦设计的决定性作用。



### 3D 人体交互生成的任务定义与挑战

3D 人体交互生成旨在根据文本描述，生成两个或多个人物在三维空间中协调运动的序列。与单人运动生成不同，交互生成面临双重难题：(1) **个体运动的自然性**——每个人物的动作本身必须符合人体运动学规律；(2) **交互的语义一致性与物理合理性**——两人之间的接触、空间关系和时序协调必须与文本描述对齐，且避免穿透、错失接触等物理失真。

现有方法在处理这一任务时暴露出一个核心瓶颈：**将所有运动信息压缩到单一潜在表示中，无法解耦个体身份与交互上下文**。例如，InterLDM (Li et al., 2025) 和 InterMask (Javed et al., 2025) 均采用扁平潜在空间，将两人运动统一编码为一个整体潜变量（见 Figure 1(a)(b)）。这种扁平化策略导致细粒度个体动作信息丢失，语义不对齐，以及穿透、接触缺失等物理不真实现象。

### 现有方法的局限

**扁平潜在空间的固有问题。** 在单一潜在表示中，个体运动特征与全局交互信息相互纠缠。解码器很难同时恢复两人的独立动作和精确的交互语义，尤其在接触密集型场景（如握手、拥抱、打斗）中，模型容易产生穿透或“假接触”。

**交互建模的不足。** 部分方法（如 InterGen）仅通过简单的距离惩罚来约束两人的空间关系，缺乏对交互语义的深层建模；而基于扩散模型的方法（如 ComMDM、TIMotion）虽然生成质量较高，但并未显式分离个体与交互的表示层次，导致生成结果在复杂交互场景下仍存在 artifacts（见 Figure 7）。

**物理合理性缺乏显式约束。** 现有工作普遍缺少对接触质量、穿透程度的显式建模或后处理机制。即使生成的运动在运动学指标上表现良好，物理合理性（如穿透体积、接触比率）仍远未达到实用水平。

### 本文动机与核心思路

针对上述问题，本文提出 **DHVAE (Disentangled Hierarchical Variational Autoencoder)**，其核心动机是：**显式解耦个体动作与全局交互为独立的潜在变量，从而在潜在空间中增强交互语义建模和物理一致性**。

具体而言，DHVAE 引入三个关键设计：

1. **解耦层次潜在空间**：将交互运动的潜在表示分解为个体动作潜变量 $z_a$、$z_b$ 和全局交互潜变量 $z_o$，从根本上避免信息纠缠（见 Figure 1(c)）。
2. **CoTransformer 交互建模**：通过交叉注意力机制融合两个体的嵌入，在保持个体身份的同时注入双向感知，生成富含交互上下文的全局潜变量 $z_o$。
3. **对比学习约束**：在 $z_o$ 上施加三元组损失，基于接触检测构造正负样本，促使潜在空间编码物理合理的交互模式，从而在生成阶段减少穿透和接触缺失。

通过这一设计，DHVAE 在 InterHuman 和 InterX 两个主流基准上取得了新的最优性能，并在物理合理性指标上显著超越现有方法。



## 核心方法与创新机理

现有文本驱动人体交互（HHI）生成方法——无论是基于原始运动空间的扩散模型（如 **InterGen** (Liang et al., 2024)、**InterMask** (Javed et al., 2025)），还是基于潜在扩散的方法（如 **InterLDM** (Li et al., 2025)）——均采用**扁平单一潜在表示**，将所有运动信息（包括个体动作与交互上下文）压缩至同一个潜变量中。这种设计导致个体身份模糊、细粒度动作丢失，并在交互边界（如握手、拥抱）产生穿透、接触缺失等物理不真实现象。DHVAE 的核心创新在于从**潜在空间结构**、**交互建模机制**和**物理合理性约束**三个维度对上述瓶颈进行系统性改造。

### 1. 解耦层次潜在空间：从扁平到结构化

DHVAE 将传统 VAE 的单一潜变量替换为**三个解耦的潜在变量**：个体运动潜变量 $\mathbf{z}_a$、$\mathbf{z}_b$ 和全局交互潜变量 $\mathbf{z}_o$（Figure 1, Figure 2）。这一设计的直接效果是：个体运动编码器（Transformer Encoder）分别独立提取两人的运动特征，保证了个性化动作细节的保真度；而全局交互编码（MLP）则专门负责捕获跨个体的时空协调关系。证据下界（ELBO）也相应地从单一项扩展为包含个体似然项与全局交互 KL 散度的结构化形式：

$$
\log p(\mathbf{x}_a, \mathbf{x}_b) \geq \mathcal{L}_{\mathrm{ELBO}} = \mathbb{E}_{q(\mathbf{z}_a, \mathbf{z}_b, \mathbf{z}_o|\mathbf{x})}\Big[ \log p(\mathbf{x}_a|\mathbf{z}_o, \mathbf{z}_a) + \log p(\mathbf{x}_b|\mathbf{z}_o, \mathbf{z}_b) \Big] - D_{\mathrm{KL}}\Big[ q(\mathbf{z}_a|\mathbf{x}_a) \| p(\mathbf{z}_a) \Big] - D_{\mathrm{KL}}\Big[ q(\mathbf{z}_b|\mathbf{x}_b) \| p(\mathbf{z}_b) \Big] - D_{\mathrm{KL}}\Big[ q(\mathbf{z}_o|\mathbf{z}_a, \mathbf{z}_b) \| p(\mathbf{z}_o) \Big]
$$

消融实验直接验证了这一创新的决定性作用：将 DHVAE 替换为扁平 VAE（MLD-VAE）后，重建 FID 从 0.503 大幅上升至 1.024，生成 FID 从 5.015 恶化至 6.433（Table 5），证明解耦层次潜在空间是性能提升的核心因果杠杆。

### 2. CoTransformer 双向感知交互建模

传统方法（如 InterGen）仅通过简单的距离惩罚或统一潜在空间隐式建模交互，缺乏对双向感知的显式捕获。DHVAE 引入 **CoTransformer 模块**：在个体运动编码器提取 $\mathbf{z}_a$、$\mathbf{z}_b$ 后，CoTransformer 通过**交叉注意力**融合两个体的嵌入，在保持个体身份的同时注入全局感知，生成交互感知的融合特征，进而由 MLP 压缩为 $\mathbf{z}_o$（Figure 2）。该设计使得 $\mathbf{z}_o$ 能够显式编码“A 如何响应 B 的动作”以及“B 如何响应 A 的动作”的双向语义。移除 CoTransformer 和 $\mathbf{z}_o$ 后，重建 FID 升至 0.561，生成 FID 升至 5.289，R‑Prec@1 降至 0.486（Table 5），确认了层次化交互建模的必要性。

### 3. 对比学习驱动的物理合理潜空间

即使有了结构化的 $\mathbf{z}_o$，若缺乏显式约束，该潜变量仍可能编码物理不合理的交互（如手部未接触的“握手”）。DHVAE 在 $\mathbf{z}_o$ 上施加**对比学习三元组损失**，基于接触检测构造正负样本对：

$$
\mathcal{L}_{\mathrm{triplet}} = \max(0, d(\mathbf{z}_o, \mathbf{z}_o^+) - d(\mathbf{z}_o, \mathbf{z}_o^-) + m)
$$

该损失拉近物理合理交互的潜表示（正样本对），推远不合理交互的潜表示（负样本对），从而在潜在空间中形成按物理合理性组织的流形结构。Figure 9 的可视化消融表明，移除对比学习后，生成的手部无法正确接触，物理合理性显著下降。当接触阈值 $\sigma_c=0.05$ 和 $\sigma_u=0.30$ 时，模型获得最佳接触率（0.581）和最低穿透体积（Table 4, Table 7）。

### 4. 扩散去噪器的适配设计

为配合结构化潜在空间，DHVAE 的去噪器采用了**跳跃连接 AdaLN‑zero 三参数 Transformer**，结合分段位置编码（SPE）和令牌缩放（Token Scaling），以稳定训练并提升对层次化潜变量的去噪能力。消融显示，移除 SPE 或 Token Scaling 均导致 R‑Precision 和 FID 显著恶化（Table 5）。

**总结**：DHVAE 的三项核心创新——解耦层次潜在空间、CoTransformer 双向交互建模、对比学习物理合理性约束——构成了一个闭环的因果链条：结构化潜变量提供表达能力，CoTransformer 注入交互语义，对比学习确保物理一致性。三者协同作用，使得 DHVAE 在 InterHuman 和 InterX 双基准上全面超越 SOTA（Table 1），并在接触比率上比 InterMask 提升 11.3 个百分点（0.581 vs. 0.468, Table 4）。



DHVAE 的整体 pipeline 围绕一个核心设计原则展开：**将双人交互运动显式解耦为个体运动与全局交互的层次化潜在表示**，并在此结构化潜在空间中进行扩散生成。整个框架由两大阶段串联构成——**DHVAE 变分自编码器**负责学习紧凑的解耦潜在表示，**潜在扩散模型**在该潜在空间中进行条件生成。

### 1. 数据流与模块关系

系统的输入为双人运动序列 $\mathbf{x}_a, \mathbf{x}_b$（分别对应人物 A 和人物 B 的关节旋转/位置序列）以及文本描述 $c$。数据流经历以下关键模块：

1.  **个体运动编码器**：两个结构对称的 Transformer Encoder 分别处理 $\mathbf{x}_a$ 和 $\mathbf{x}_b$，通过可学习的查询令牌 $\mathbf{u}_a, \mathbf{u}_b$ 将个体运动压缩为个体潜在变量 $\mathbf{z}_a, \mathbf{z}_b$。这一设计确保了个体运动细节的独立保留。

2.  **CoTransformer 交互融合模块**：个体编码器的中间层嵌入被送入 CoTransformer。该模块通过**交叉注意力机制**实现双向感知——人物 A 的嵌入作为 Query 关注人物 B 的嵌入，反之亦然，同时引入跳跃连接以保留个体身份信息。CoTransformer 的输出经过一个 MLP 生成全局交互潜在变量 $\mathbf{z}_o$，其服从高斯分布，捕获双人之间的时空协调与语义关系。

3.  **DHVAE 解码器**：从三元组 $(\mathbf{z}_o, \mathbf{z}_a, \mathbf{z}_b)$ 出发，通过交叉注意力分别解码出人物 A 和人物 B 的运动序列。解码过程中，$\mathbf{z}_o$ 为两个个体解码器提供共享的交互上下文，确保生成运动的**时间同步与语义一致性**。

4.  **潜在扩散去噪器**：在 DHVAE 学习到的结构化潜在空间中进行 DDIM 扩散。去噪器采用 **AdaLN-zero Transformer** 架构（13 层），融合文本条件 $c$ 和时间步 $t$。其关键设计包括：
    -   **跳跃连接**：在对称的 Transformer 层之间建立跳跃连接，使浅层低层特征能够直接流向深层，稳定训练并提升重建质量。
    -   **分段位置编码 (SPE)**：为潜在序列的各个分段（如个体 A、个体 B、全局交互）赋予结构化的位置信息。
    -   **令牌缩放 (Token Scaling)**：对不同语义的潜在令牌进行尺度归一化，防止某一类令牌主导梯度更新。

5.  **分类器自由引导 (CFG)**：推理时，去噪器同时接收条件预测 $\epsilon_{\boldsymbol{\theta}}(\mathbf{z}_t, t, c)$ 和无条件预测 $\epsilon_{\boldsymbol{\theta}}(\mathbf{z}_t, t)$，通过引导强度 $\omega$ 进行插值：
    $$\epsilon_{\mathrm{guided}} = (1+\omega) \cdot \epsilon_{\boldsymbol{\theta}}(\mathbf{z}_t, t, c) - \omega \cdot \epsilon_{\boldsymbol{\theta}}(\mathbf{z}_t, t)$$
    这允许用户在生成多样性与文本对齐度之间进行权衡。

### 2. 训练目标与约束

DHVAE 的训练并非仅依赖标准的 ELBO，而是引入多重损失以强化潜在空间的结构：

-   **DHVAE ELBO**：显式分离个体似然项与全局交互项，包含三个 KL 散度正则项，分别约束 $\mathbf{z}_a, \mathbf{z}_b, \mathbf{z}_o$ 靠近先验分布。
-   **关节点位置损失 $\mathcal{L}_{\mathrm{joint}}$**：对解码出的关节点位置施加 L1 损失，提供细粒度的运动监督。
-   **对比学习三元组损失 $\mathcal{L}_{\mathrm{triplet}}$**：这是框架实现物理合理性的关键。基于接触检测算法构造正负样本对，对全局交互潜变量 $\mathbf{z}_o$ 施加三元组损失：
    $$\mathcal{L}_{\mathrm{triplet}} = \max(0, d(\mathbf{z}_o, \mathbf{z}_o^+) - d(\mathbf{z}_o, \mathbf{z}_o^-) + m)$$
    该损失迫使具有相似交互模式（如握手）的 $\mathbf{z}_o$ 在潜在空间中靠近，而将物理不合理的交互（如穿透、错位）推远，从而使 $\mathbf{z}_o$ 成为一个**交互语义感知且物理合理的潜在空间**。

总体训练目标为：
$$\mathcal{L}_{\mathrm{DHVAE}} = \mathcal{L}_{\mathrm{ELBO}} + \lambda_{\mathrm{joint}} \mathcal{L}_{\mathrm{joint}} + \lambda_{\mathrm{triplet}} \mathcal{L}_{\mathrm{triplet}}$$

### 3. 框架的核心优势

与将双人运动压缩为单一扁平潜在向量的方法（如 InterLDM、InterMask）相比，DHVAE 的层次化解耦设计带来了三个结构性优势：

-   **个体保真度**：$\mathbf{z}_a, \mathbf{z}_b$ 独立编码个体运动，避免了个体细节在压缩过程中被全局信息淹没。
-   **交互语义建模**：CoTransformer 和 $\mathbf{z}_o$ 显式建模双向交互，而非依赖隐式的距离惩罚。
-   **物理合理性**：对比学习直接作用于 $\mathbf{z}_o$，为潜在空间注入了接触感知的先验，从根源上减少了穿透和接触缺失。

消融实验（Table 5）强有力地验证了这一框架：将 DHVAE 替换为扁平 VAE 后，重建 FID 从 0.503 急剧上升至 1.024，生成 FID 从 5.015 升至 6.433；移除 CoTransformer 与 $\mathbf{z}_o$ 同样导致所有指标显著恶化。这确认了解耦层次潜在空间是性能提升的**决定性瓶颈**。

### 补充图表

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/001_Figure_1.jpg]]
*Figure 1: (a) InterLDM Li et al. (2025), (b) InterMask Javed et al. (2025) encode all motion information into a single latent. (c) Our encodes individual motions and interactions into separate disentangled latents*

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of our DHVAE to encode the structured latent representation*



DHVAE 的核心设计围绕一个结构化潜变量三元组展开：个体运动潜变量 $\mathbf{z}_a$、$\mathbf{z}_b$ 和全局交互潜变量 $\mathbf{z}_o$。该设计的根本动机来自现有方法的瓶颈——将所有运动信息压缩到单一扁平潜变量中，导致个体身份模糊、交互语义丢失和物理不合理（如穿透、接触缺失）。DHVAE 通过解耦层次化编码显式分离个体运动与全局交互，从而在潜空间结构层面解决了这一问题。

### DHVAE 编码器：从个体编码到交互融合

编码过程分为两个阶段。首先，两个独立的 Transformer 编码器分别处理个体 A 和 B 的运动序列 $\mathbf{x}_a$、$\mathbf{x}_b$，通过可学习令牌 $\mathbf{u}_a$、$\mathbf{u}_b$ 提取个体运动特征，并参数化个体潜变量的后验分布 $q(\mathbf{z}_a|\mathbf{x}_a)$ 和 $q(\mathbf{z}_b|\mathbf{x}_b)$。这一设计确保了个体运动信息的独立性和完整性。

随后，CoTransformer 模块对两个个体的嵌入进行双向交叉注意力融合，建模交互上下文。CoTransformer 的输出经过一个 MLP 生成全局交互潜变量 $\mathbf{z}_o$ 的后验分布 $q(\mathbf{z}_o|\mathbf{z}_a,\mathbf{z}_b)$。这里的关键在于 $\mathbf{z}_o$ 的生成以 $\mathbf{z}_a$ 和 $\mathbf{z}_b$ 为条件，使得全局交互编码能够感知两个个体的运动状态，而非独立于个体信息进行建模。

### 证据下界 (ELBO) 的层次化分解

DHVAE 的训练目标基于变分推断的证据下界。与扁平 VAE 将联合运动 $\mathbf{x}$ 压缩到单一潜变量 $\mathbf{z}$ 不同，DHVAE 的 ELBO 显式分离了个体似然项和全局交互项：

$$
\begin{aligned}
\log p(\mathbf{x}_a, \mathbf{x}_b) \geq \mathcal{L}_{\mathrm{ELBO}} = &\ \mathbb{E}_{q(\mathbf{z}_a, \mathbf{z}_b, \mathbf{z}_o|\mathbf{x})}\Big[ \log p(\mathbf{x}_a|\mathbf{z}_o, \mathbf{z}_a) + \log p(\mathbf{x}_b|\mathbf{z}_o, \mathbf{z}_b) \Big] \\
&- D_{\mathrm{KL}}\Big[ q(\mathbf{z}_a|\mathbf{x}_a) \| p(\mathbf{z}_a) \Big] \\
&- D_{\mathrm{KL}}\Big[ q(\mathbf{z}_b|\mathbf{x}_b) \| p(\mathbf{z}_b) \Big] \\
&- D_{\mathrm{KL}}\Big[ q(\mathbf{z}_o|\mathbf{z}_a, \mathbf{z}_b) \| p(\mathbf{z}_o) \Big]
\end{aligned}
$$

其中，前两项期望项分别度量个体 A 和 B 的重建质量，解码器以全局交互潜变量 $\mathbf{z}_o$ 和对应个体潜变量为条件，通过交叉注意力实现时间同步和语义一致的运动重建。后三项 KL 散度分别正则化三个潜变量的后验分布，使其接近标准高斯先验。这种分解使得潜空间具有明确的语义分工：$\mathbf{z}_a$、$\mathbf{z}_b$ 编码个体运动风格，$\mathbf{z}_o$ 编码交互模式。

### 对比学习约束与总损失

仅靠 ELBO 无法保证 $\mathbf{z}_o$ 编码物理合理的交互语义。为此，DHVAE 引入基于三元组损失的对比学习约束，作用于全局交互潜变量 $\mathbf{z}_o$：

$$
\mathcal{L}_{\mathrm{triplet}} = \max(0, d(\mathbf{z}_o, \mathbf{z}_o^+) - d(\mathbf{z}_o, \mathbf{z}_o^-) + m)
$$

正负样本的构造基于接触检测：正样本对来自具有相似物理接触模式的交互片段，负样本对来自接触模式显著不同的片段。该损失拉近正样本对在 $\mathbf{z}_o$ 空间中的距离，推远负样本对，从而促使 $\mathbf{z}_o$ 学习一个物理合理的交互潜空间。消融实验（Figure 9）显示，移除对比学习后，生成的手部无法正确接触，物理合理性显著下降。

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/015_Figure_9.jpg]]
*Figure 9: Visualization ablation study for Contrastive learning*

DHVAE 的总体训练目标将上述组件整合：

$$
\mathcal{L}_{\mathrm{DHVAE}} = \mathcal{L}_{\mathrm{ELBO}} + \lambda_{\mathrm{joint}} \mathcal{L}_{\mathrm{joint}} + \lambda_{\mathrm{triplet}} \mathcal{L}_{\mathrm{triplet}}
$$

其中 $\mathcal{L}_{\mathrm{joint}}$ 是关节点位置的 L1 损失，用于显式约束重建精度。

### 层次潜空间上的扩散去噪

DHVAE 训练完成后，在学到的结构化潜空间上进行潜在扩散。前向过程遵循 DDIM 的高斯变换：

$$
q(\mathbf{z}_t|\mathbf{z}_{t-1}) = \mathcal{N}(\mathbf{z}_t; \sqrt{1-\beta_t}\mathbf{z}_{t-1}, \beta_t\mathbf{I})
$$

通过重参数化，可直接从初始潜变量和噪声采样任意时间步的 $\mathbf{z}_t$：

$$
\mathbf{z}_t = \sqrt{\bar{\alpha}_t}\mathbf{z}_0 + \sqrt{1-\bar{\alpha}_t}\epsilon, \quad \epsilon \sim \mathcal{N}(0,\mathbf{I})
$$

去噪器采用 13 层 AdaLN-zero Transformer，结合跳跃连接、分段位置编码 (SPE) 和令牌缩放 (Token Scaling) 以稳定训练。推理时使用分类器自由引导 (CFG) 平衡生成多样性和文本对齐：

$$
\epsilon_{\mathrm{guided}} = (1+\omega) \cdot \epsilon_{\boldsymbol{\theta}}(\mathbf{z}_t, t, c) - \omega \cdot \epsilon_{\boldsymbol{\theta}}(\mathbf{z}_t, t)
$$

其中 $c$ 为文本条件，$\omega$ 为引导强度。消融实验（Table 5）表明，移除 SPE 或令牌缩放均导致 FID 和 R-Precision 显著恶化，验证了这些结构设计对去噪过程的重要性。

### 补充图表

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/014_Figure_8.jpg]]
*Figure 8: PCA projections of the interaction latent*

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/016_Figure_10.jpg]]
*Figure 10: T-SNE projections of latents on the InterHuman test set*



## 实验与关键发现

### 主实验结果

DHVAE 在两个主流双人交互基准 InterHuman 和 InterX 上均达到 SOTA 性能。Table 1 报告了与 InterMask、TIMotion、InterGen、MoMat-MoGen、ComMDM 等方法的全面对比，所有指标均运行 20 次取均值±标准差。

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/003_Table_1.jpg]]
*Table 1: Comparisons on InterHuman and InterX datasets. The best results are in bold, and the second-best are underlined. Methods with * are implemented by us. All results are run 20 times. For a fair comparison, we set the latent size of MLD to be the same as ours, i.e*

在 InterHuman 数据集上，DHVAE 取得 **FID 5.015 ± 0.085**（对比 InterMask 的 5.153 ± 0.061），**R‑Prec@1 0.496 ± 0.004**（InterMask 为 0.449 ± 0.004），Multimodal Distance 和 MModality 同样最优。在 InterX 数据集上优势更为显著：**FID 0.339 ± 0.026**，远低于 InterMask 的 1.295 ± 0.038，降幅达 0.956，显示解耦层次潜在空间在复杂 SMPLX 表示下的泛化能力。

Table 2 的重建质量对比进一步验证了 DHVAE 的紧凑表达能力：重建 FID (rFID) 显著优于 InterLDM 等基于先验的方法，MPJPE 和 L1 损失同样最低，说明层次化解耦并未牺牲重建精度，反而通过分离个体与交互信息提升了压缩效率。

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/004_Table_2.jpg]]
*Table 2: Reconstruction results for prior-based and SOTA models, best results in bold*

Table 3 的计算效率比较表明，DHVAE 在参数量和推理延迟上均具有竞争力，未因结构化潜在设计引入显著计算开销。

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/005_Table_3.jpg]]
*Table 3: Computational cost of models including latency and size*

### 物理合理性分析

Table 4 报告了穿透指标和接触比率。DHVAE 在穿透体积 (Penetration Volume)、穿透帧比率 (PFR/PDR) 上均优于所有 SOTA 方法，同时 **接触比率 0.581** 显著高于 InterMask 的 0.468（+0.113），证明对比学习约束下的全局交互潜变量 z_o 有效促进了物理合理的接触生成。然而，模型仍存在 artifacts，尤其在 InterX 数据集上更易出现脚滑、微小穿透或接触错失——说明对比学习提供了全局物理先验，但缺乏显式校正细粒度物理瑕疵的机制。

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/006_Table_4.jpg]]
*Table 4: Penetration metrics and contact ratio for state-of-the-art models*

### 消融实验

Table 5 的系统消融揭示了各组件的因果贡献：

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/008_Table_5.jpg]]
*Table 5: Ablation study of DHVAE and Denoiser components. ✓ indicates the component is used. For a fair comparison with MLD, we set the latent size of MLD-VAE to be*

**解耦层次潜在空间的核心作用**：将 DHVAE 替换为扁平 VAE (MLD‑VAE)，重建 FID 从 0.503 急剧上升至 1.024，生成 FID 从 5.015 升至 6.433，R‑Prec@1 从 0.496 降至 0.452。这直接证实了单一潜在表示无法有效解耦个体身份与交互上下文，导致细粒度动作丢失和语义不对齐。

**CoTransformer 与全局交互潜变量 z_o 的必要性**：移除 CoTransformer 和 z_o 后，重建 FID 升至 0.561，生成 FID 升至 5.289，R‑Prec@1 降至 0.486。缺少双向感知融合机制和显式交互建模，模型退化为近似独立个体运动的拼接。

**去噪器组件贡献**：移除分段位置编码 (SPE) 或令牌缩放 (Token Scaling) 导致 R‑Precision 和 FID 显著恶化，验证了结构化分割与尺度一致性对层次潜在空间去噪的重要性。跳跃连接 AdaLN‑zero 设计支撑了深层 Transformer 的稳定训练。

**对比学习的影响**：Figure 9 的可视化消融显示，移除对比学习后生成的手部无法正确接触，物理合理性显著下降。Figure 8 的 PCA 投影进一步揭示，无对比学习时 z_o 的潜在空间呈现歧化分布，正负样本混杂；对比学习使 z_o 形成清晰的物理合理交互流形。Table 7 的阈值消融表明，接触阈值 σ_c=0.05 和 σ_u=0.30 时获得最佳接触率与最低穿透体积。

### 失败模式与局限

尽管 DHVAE 在主要指标上全面领先，以下局限值得关注：

1. **物理瑕疵残留**：模型仍存在 artifacts，尤其在 SMPLX 表示的 InterX 数据集上更易出现脚滑、穿透或接触错误。对比学习提供了全局物理先验，但无法显式校正细粒度物理瑕疵。
2. **双人场景限制**：当前设计仅支持两人交互，无法直接扩展到多人或群体场景。数据集的缺乏是主要瓶颈。
3. **评价指标局限**：现有 FID、R‑Precision 等指标设计于单人任务，可能未能充分反映接触质量、同步性和人类感知真实性。Table 4 的物理指标部分弥补了这一不足，但仍需更全面的 HHI 专用评价协议。
4. **训练成本**：尽管模型已轻量，训练变分自编码器与结构化潜在扩散仍对长序列和高分辨率运动有较高计算需求。

### 补充图表

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/013_Figure_7.jpg]]
*Figure 7: Comparison with TIMotion on InterHuman*

![[assets/figures/papers/paper_list_l52_https_openreview_net_forum_id_53eIDko6N5/figures/017_Table_7.jpg]]
*Table 7: Performance under different*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

现有文本驱动的人-人交互（HHI）运动生成方法普遍采用**扁平单一潜在表示**，将双人运动的所有信息压缩至一个联合潜在变量。这一设计存在根本性瓶颈：个体身份信息与全局交互上下文在潜在空间中高度纠缠，导致细粒度动作丢失、语义不对齐，以及物理不真实（如穿透、接触缺失）。具体表现为：

- **InterLDM**（Li et al., 2025）和 **InterMask**（Javed et al., ICLR 2025）将所有运动信息编码为单一潜在向量，缺乏对个体运动与交互语义的显式分离（见 Figure 1）。
- **InterGen**（Liang et al., 2024）虽引入距离惩罚，但未在潜在层面建模交互语义，物理合理性不足。
- **MoMat-MoGen**（Cai et al., 2024）、**in2IN**（Ruiz-Ponce et al., 2024）等方法同样受限于扁平潜在空间的信息瓶颈。

DHVAE 的核心洞察在于：**显式解耦个体动作和全局交互为独立的潜在变量**，结合 CoTransformer 进行双向感知编码，并通过对比学习约束全局交互潜变量，可以有效提升生成运动的文本对齐度、动作保真度和物理合理性。

### 2. 关键设计变更与方法谱系

DHVAE 相对于现有工作进行了四个关键设计变更，构成其在方法谱系中的核心定位：

| 设计维度 | 基线做法 | DHVAE 做法 | 变更性质 |
|----------|----------|------------|----------|
| **潜在空间结构** | 单一扁平潜在表示（MLD、InterLDM、InterMask） | 解耦层次潜在表示 {z_o, z_a, z_b}，显式分离全局交互与个体运动 | 结构性创新 |
| **交互建模** | 统一潜在空间或简单距离惩罚（InterGen） | CoTransformer 交叉注意力融合 + 全局交互潜变量 z_o，捕获双向感知 | 机制性创新 |
| **物理合理性约束** | 无显式物理先验或仅固定距离惩罚 | 对比学习三元组损失作用于 z_o，基于接触检测构造正负样本 | 训练策略创新 |
| **扩散去噪器设计** | 标准 Transformer 或两参数 AdaLN（InterGen） | 跳跃连接 AdaLN-zero（三参数）Transformer，结合分段位置编码和令牌缩放 | 架构优化 |

这些变更的因果链条清晰：**解耦潜在空间**是基础，使个体运动与交互语义分离；**CoTransformer** 在此基础上实现双向感知的交互建模；**对比学习**进一步约束 z_o 的语义空间，提升物理合理性；**去噪器优化**则稳定了层次潜在空间上的扩散训练。

### 3. 与 SOTA 方法的关系与边界

**定量定位**：在 InterHuman 和 InterX 两个标准基准上，DHVAE 在 FID、R-Precision、MMDist 等主要指标上全面超越现有 SOTA。与最强基线 **InterMask**（Javed et al., ICLR 2025）相比，InterHuman 上 FID 从 5.153 降至 5.015，R-Prec@1 从 0.449 提升至 0.496；InterX 上 FID 从 1.295 大幅降至 0.339（Table 1）。物理合理性方面，接触比率从 InterMask 的 0.468 提升至 0.581（Table 4）。

**定性差异**：与 **TIMotion**（Wang et al., 2025）的对比（Figure 7）显示，TIMotion 存在明显的 artifacts（如肢体扭曲、接触错位），而 DHVAE 生成的运动在文本对齐度和物理一致性上更优。

**计算效率**：DHVAE 在保持轻量参数量的同时实现了 SOTA 性能（Table 3），说明解耦设计并未引入显著的计算开销。

### 4. 适用边界与局限

尽管 DHVAE 在双人交互生成上取得了显著进展，其适用边界和局限同样明确：

**场景边界**：
- 仅支持**两人交互**（双人场景），无法直接扩展到多人或群体交互。数据集的缺乏是主要瓶颈——现有 HHI 数据集（InterHuman、InterX）均限于双人场景。
- 模型在 **SMPLX 表示的 InterX 数据集**上更易出现脚滑、穿透或接触错误，说明对高自由度参数化人体的泛化仍有不足。

**机制局限**：
- 虽然对比学习提升了物理合理性，但并未提供**显式校正细粒度物理瑕疵**的机制（如微小穿透、错失接触）。接触检测依赖阈值 σ_c 和 σ_u，对阈值敏感（Table 7 显示 σ_c=0.05、σ_u=0.30 时最优）。
- 现有评价指标（FID、R-Precision 等）设计于单人任务，可能**未能充分反映接触质量、同步性和人类感知真实性**。

**训练成本**：
- 尽管模型已轻量，训练变分自编码器与结构化潜在扩散仍对长序列和高分辨率运动有较高计算需求。

### 5. 开放问题与后续方向

基于 DHVAE 的设计逻辑和当前局限，以下开放问题值得关注：

1. **可扩展的多人交互建模**：如何将层次化解耦设计扩展到动态人数的多人场景？是否需要新的 scalable inter-agent 建模机制（如基于图的潜在交互表示）？

2. **显式物理细化**：能否通过事后细化策略（如分类器引导、接触感知判别器、物理先验）显式校正穿透和接触精度？这可以与 DHVAE 的解耦潜在空间形成互补。

3. **HHI 专用评价协议**：如何构建 HHI 专用的评价协议（如接触比率、同步性评分、感知真实度），并结合人工评估或学习型质量评分器？当前指标体系的局限性已在实验中显现。

4. **跨域泛化与效率**：如何通过跨运动域的预训练或参数高效变体降低训练成本并保持泛化能力？这对实际部署至关重要。



## 原文 PDF

![[paperPDFs/ICLR_2026/Disentangled_Hierarchical_VAE_for_3D_Human_Human_Interaction_Generation_86bc618f301e.pdf]]
