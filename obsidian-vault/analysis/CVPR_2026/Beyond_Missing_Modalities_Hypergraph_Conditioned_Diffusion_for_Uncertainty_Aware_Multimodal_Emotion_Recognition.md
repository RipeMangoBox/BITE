---
title: "Beyond Missing Modalities: Hypergraph Conditioned Diffusion for Uncertainty-Aware Multimodal Emotion Recognition"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Beyond_Missing_Modalities_Hypergraph_Conditioned_Diffusion_for_Uncertainty_Aware_Multimodal_Emotion_Recognition.pdf
project_link: null
code_link: null
aliases:
- HDEFBERH
- BMMHCDUAMER
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 以掩码超图注意力网络（MHGAT）捕捉高阶多变量关系作为条件，指导扩散模型进行语义一致的缺失模态恢复，并通过双重证据融合同时解耦特征源和判别层的不确定性。
primary_logic: 超图结构能够同时编码模态内、模态间及对话上下文的高阶交互；将其作为条件嵌入扩散模型，并配合细粒度的双重不确定性估计，可在缺失模态下实现鲁棒且可解释的融合。
claims:
- HyperEF 在所有缺失率下均超过现有方法，尤其是在 IEMOCAP6 缺失率 0.6 时精度提升 4.0%。
- MHGAT 条件扩散恢复的特征与原始特征在分布上更一致（MMD 更低）且恢复误差更小。
- 基于熵的判别层不确定性作为第二解耦方向，显著优于其他解耦策略，并带来最高精度。
- IEMOCAP6 (κ=0.2) 上 准确率 (Accuracy %%) = 64.1
---

# Beyond Missing Modalities: Hypergraph Conditioned Diffusion for Uncertainty-Aware Multimodal Emotion Recognition

> [!tip] 核心洞察
> 超图结构能够同时编码模态内、模态间及对话上下文的高阶交互；将其作为条件嵌入扩散模型，并配合细粒度的双重不确定性估计，可在缺失模态下实现鲁棒且可解释的融合。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越缺失模态：面向不确定性感知多模态情感识别的超图引导扩散 |
| 英文题名 | Beyond Missing Modalities: Hypergraph Conditioned Diffusion for Uncertainty-Aware Multimodal Emotion Recognition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Qiu_Beyond_Missing_Modalities_Hypergraph_Conditioned_Diffusion_for_Uncertainty-Aware_Multimodal_Emotion_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Hypergraph Diffusion and Evidence Fusion based Emotion Recognition (HyperEF) |
| Dataset | IEMOCAP6, MELD, IEMOCAP4 |

> [!tip] 效果简介
> - IEMOCAP6 (κ=0.2) 上，准确率 (Accuracy %%) 64.1 vs 61.2 (该设置下最强基线，见表1) (+2.9)。
> - MELD (κ=0.2) 上，准确率 (Accuracy %%) 69.3 vs 67.1 (该设置下最强基线，见表1) (+2.2)。
> - IEMOCAP4 (κ=0.1) 上，准确率 (Accuracy %%) 82.1 vs 78.6 (SDR-GNN, Table 1) (+3.5)。

## 概要

多模态情感识别在真实场景中常因设备故障、隐私限制或传输丢包而面临模态缺失，导致语义不一致与多维不确定性建模不足，严重削弱识别性能。现有方法或依赖常规图神经网络进行补全，或采用无引导的生成式恢复，难以捕捉模态间、模态内及对话上下文的高阶依赖关系，且缺乏对融合过程中不确定性的细粒度解耦。

本文提出 **HyperEF (Hypergraph Diffusion and Evidence Fusion based Emotion Recognition)**，核心思路是：以掩码超图注意力网络（MHGAT）捕捉高阶多变量关系作为条件，指导扩散模型进行语义一致的缺失模态恢复，并通过双重证据融合同时解耦特征源和判别层的不确定性。超图结构能够同时编码模态内、模态间及对话上下文的高阶交互；将其作为条件嵌入扩散模型，并配合细粒度的双重不确定性估计，可在缺失模态下实现鲁棒且可解释的融合。

主要结果方面，HyperEF 在所有缺失率下均超过现有方法，尤其是在 IEMOCAP6 缺失率 0.6 时精度提升 4.0%（Table 1）；MHGAT 条件扩散恢复的特征与原始特征在分布上更一致，MMD 更低且恢复误差更小（Table 3）；基于熵的判别层不确定性作为第二解耦方向，显著优于其他解耦策略并带来最高精度（Table 4）。在方法谱系中，HyperEF 区别于 **GCNet**（Lian et al., TPAMI 2023）的图补全、**IMDer**（Wang et al., NeurIPS 2023）的无引导扩散恢复、**SDR-GNN**（Fu et al., KBS 2025）的谱域重建以及 **MMIN**（Zhao et al., ACL/IJCNLP 2021）的缺失模态想象，通过超图条件扩散与双重证据融合实现了缺失模态下更强的鲁棒性。

多模态情感识别（Multimodal Emotion Recognition, MER）旨在融合文本、语音和视觉等多源信号以实现精准的情感推断，是构建共情式对话系统的核心技术之一。然而，真实场景中模态缺失普遍存在——摄像头遮挡、语音噪声、文本转录失败等因素导致某一或多个模态不可用，严重破坏语义一致性并引入多维不确定性，使传统融合方法性能急剧退化。

现有缺失模态处理方法可归为三类：(1) **缺失模态想象**，如 **MMIN**（Zhao et al., ACL/IJCNLP 2021）直接生成缺失特征，但缺乏对高阶语义关系的显式建模；(2) **图补全网络**，如 **GCNet**（Lian et al., TPAMI 2023）利用图结构传播信息，但图结构仅能编码成对关系，难以捕捉模态内、模态间及对话上下文的复杂多元交互；(3) **扩散模型恢复**，如 **IMDer**（Wang et al., NeurIPS 2023）借助扩散过程重建缺失模态，但采用无引导生成，恢复结果与对话语义的一致性不足。此外，现有方法在融合阶段普遍采用等权策略或仅基于空位（vacuity）的简单不确定性估计，未能同时解耦特征源和判别层的不确定性，导致模态冲突难以有效缓解。

上述缺口指向一个核心瓶颈：**缺失模态导致语义不一致与多维不确定性建模不足，严重削弱多模态情感识别性能**。本文提出 **HyperEF**（Hypergraph Diffusion and Evidence Fusion based Emotion Recognition），以超图引导的条件扩散与双重证据融合两大机制应对该挑战。其核心洞见在于：超图结构能够同时编码模态内、模态间及对话上下文的高阶交互；将其作为条件嵌入扩散模型，并配合细粒度的双重不确定性估计，可在缺失模态下实现鲁棒且可解释的融合。

## 核心方法与创新机理

HyperEF 围绕缺失模态下多模态情感识别面临的两个核心瓶颈——语义不一致与多维不确定性建模不足——提出了三条紧密耦合的创新路径。

**瓶颈与可调因果旋钮。** 当部分模态缺失时，传统方法仅依赖剩余模态进行推断或执行无引导的特征生成，容易引入语义漂移。HyperEF 将“高阶多变量关系的建模与条件化引导”作为核心因果旋钮：通过掩码超图注意力网络（MHGAT）捕捉模态内、模态间及对话上下文的复杂交互，并将其作为条件嵌入扩散模型，指导缺失模态特征在潜在空间中的语义一致恢复。在此基础上，双重证据融合（DCEF）进一步解耦特征源与判别层的不确定性，使融合过程能够自适应地抑制不可靠信息。

**changed slots：三个关键维度上的结构性创新。** 下表将 HyperEF 相对于基线方法的核心改动归纳为三个 changed slots，每个 slot 对应一个明确的基线做法与改进后的方案。

| 改动维度 | 基线方法 | HyperEF 方案 | 证据锚点 |
|---|---|---|---|
| **关系建模网络** | 常规 GNN 或 Transformer（如 **GCNet** (Lian et al., TPAMI 2023)、**SDR-GNN** (Fu et al., KBS 2025)） | Masked Hypergraph Attention (MHGAT)，以超边同时编码模态内与模态间高阶关系，并引入掩码机制区分可用/缺失模态 | Sec 3.1.1 |
| **缺失模态恢复方式** | 直接扩散或无引导生成（如 **IMDer** (Wang et al., NeurIPS 2023)） | MHGAT 条件扩散：超图提取的高阶语义信息作为条件 $C$ 贯穿 U-Net 去噪过程，并采用无分类器引导调整条件强度 | Sec 3.1.2 |
| **不确定性融合机制** | 等权融合或仅基于空位（vacuity）的证据融合 | Dual Channel Evidence Fusion (DCEF)：同时从特征源（重建误差 $m_s(\Omega)$）和判别层（熵 $m_d(\Omega)$）估计不确定性，双重证据质量组合后执行迭代 DST 融合 | Sec 3.2 |

**MHGAT 条件扩散：从高阶关系建模到语义一致恢复。** MHGAT 构建的超图包含上下文超边（捕捉对话序列中的说话人转换与语境流）和多模态超边（连接同一话语的文本、视觉、声学节点）。其注意力机制在节点→超边和超边→节点两个方向上自适应加权，使模型能够识别不同粒度下的关键信息。消融实验表明，MHGAT 仅使用 Transformer 编码器约 23% 的参数量即可达到相当或略优的准确率（Table 2, Sec 4.5）。在扩散阶段，MHGAT 输出的节点表示沿模态维度拼接为条件 $C \in \mathbb{R}^{N \times 3d}$，通过 U-Net 中的交叉注意力层注入去噪过程。训练时采用随机丢弃条件 $p$ 的无分类器引导策略，采样时以权重 $w$ 调节条件强度：

$$\hat{\epsilon}_\theta(\mathbf{x}_t, C) = \epsilon_\theta(\mathbf{x}_t, \mathcal{O}) + w \cdot (\epsilon_\theta(\mathbf{x}_t, C) - \epsilon_\theta(\mathbf{x}_t, \mathcal{O}))$$

这一设计使恢复特征与原始特征在分布上高度一致——在 MELD 和 IEMOCAP 上，HyperEF 恢复特征的 MMD 显著低于 IMDer，MSE 也更小（Table 3）。

**双重证据融合：解耦不确定性来源。** DCEF 将不确定性拆解为两个正交维度。特征源不确定性基于扩散模型最后一时间步的噪声预测均方误差 $u = \| \epsilon - \epsilon_{\theta}(\mathbf{x}_t, T, C) \|_2^2$，经 Sigmoid 映射得到 $m_s(\Omega)$，反映恢复特征本身的可靠程度。判别层不确定性则通过归一化熵 $m_d(\Omega) = \frac{-\sum_{k=1}^K P_k \log(P_k)}{\log K}$ 捕捉分类决策的模糊性。两者组合为通用集质量 $m(\Omega) = \gamma \cdot m_d(\Omega) + m_s(\Omega)$，再按 Dempster-Shafer 理论迭代融合各模态证据。消融实验证实，基于熵的判别层不确定性作为第二解耦方向在所有候选策略中取得最高准确率（63.78%，Table 4），而移除 vacuity 不确定性损失会导致 MELD 准确率骤降至 50.40%（Table 5），说明双重不确定性建模对维持足够证据量至关重要。

**创新协同效应。** 三条创新并非孤立——MHGAT 提取的高阶语义条件不仅指导扩散模型生成语义一致的特征，其输出的节点表示同时服务于后续的 DCEF 融合；DCEF 中的特征源不确定性直接依赖扩散模型的恢复质量，形成从恢复到评估的闭环。这一协同设计使 HyperEF 在所有缺失率下均超过现有方法，尤其在 IEMOCAP6 缺失率 0.6 时精度提升 4.0%（Table 1）。

HyperEF 的整体 pipeline 由四个核心模块串联构成：**单模态特征提取 → 掩码超图注意力条件扩散 → 双重证据融合 → 情感分类**。图 Figure 2 给出了端到端的结构示意，左侧为整体框架，右侧展开各模块的数学符号与数据流。

![[assets/figures/papers/paper_list_l840_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Beyond_Missing_Mod/figures/002_Figure_2.jpg]]
*Figure 2: The detailed structure of the HyperEF. The leftmost box shows the overall framework, while the right side presents the details of each module. Mathematical symbols in the illustration are in line with the formulas in paper text*

**输入与特征提取**：给定一段包含 $N$ 条话语的多模态对话 $U = \{ (u_1, p_1), (u_2, p_2), ..., (u_N, p_N) \}$，每条话语 $u_i$ 包含文本、视觉、声学三个模态的原始信号 $\{u_i^t, u_i^v, u_i^a\}$。首先通过预训练的单模态编码器将各模态信号映射为固定维度的特征向量，作为后续超图构建的节点初始表示。

**MHGAT 条件扩散**：这是框架的核心生成模块，负责在缺失模态场景下恢复语义一致的潜在特征。具体流程为：
1. 基于话语序列构建超图，超边包含 3 条上下文边（分别建模说话人、位置、对话主题的高阶关系）和 $N$ 条多模态边（每条话语的所有模态节点构成一条超边），总计 $N+3$ 条超边。
2. 掩码超图注意力网络（MHGAT）在超图上执行节点-超边-节点的双向注意力聚合，利用掩码机制区分可用模态与缺失模态，捕捉模态内、模态间及对话上下文的高阶多变量依赖，输出更新后的节点表示。
3. 将所有节点表示沿模态维度拼接，形成条件嵌入 $C \in \mathbb{R}^{N \times 3d}$，注入 U-Net 扩散模型的每一层（通过交叉注意力 `CrossAttn`），指导去噪过程从纯噪声逐步恢复缺失模态的潜在特征。训练时以条件 $C$ 和随机丢弃概率 $p$ 训练噪声预测网络，采样时采用无分类器引导策略增强条件一致性。

**双重证据融合（DCEF）**：恢复后的特征与原始可用特征一同进入融合阶段。DCEF 从两个解耦的维度估计不确定性：
- **特征源不确定性** $m_s(\Omega)$：基于扩散模型最后一时间步的噪声预测均方误差 $u = \| \epsilon - \epsilon_\theta(\mathbf{x}_t, T, C) \|_2^2$，经 Sigmoid 缩放后量化恢复特征的质量。
- **判别层不确定性** $m_d(\Omega)$：对各模态分类器输出的概率向量计算归一化熵，反映决策边界的模糊程度。

两者组合为通用集的质量 $m(\Omega) = \gamma \cdot m_d(\Omega) + m_s(\Omega)$，重新分配各类别的信度 $m(k) = (1 - m(\Omega)) P_k$，最终通过迭代的 Dempster-Shafer 理论（DST）规则融合所有模态的证据，输出融合后的情感类别概率。

**关键设计意图**：整个 pipeline 的信息流呈现“恢复—评估—融合”的级联逻辑。MHGAT 条件扩散解决“缺失模态恢复的语义一致性问题”，DCEF 解决“恢复后特征与原始特征之间的冲突与不确定性量化问题”，两者协同使得框架在任意缺失率下都能维持鲁棒的融合决策。

HyperEF 围绕两个核心模块构建：**MHGAT 条件扩散（MHGAT-Conditioned Diffusion）** 负责缺失模态的语义一致性恢复，**双通道证据融合（Dual Channel Evidence Fusion, DCEF）** 负责不确定性感知的多模态融合。以下逐模块展开关键公式与变量含义。

### 3.1 MHGAT 条件扩散

#### 3.1.1 掩码超图注意力网络（MHGAT）

MHGAT 的核心目标是捕捉多模态对话中的高阶多变量依赖，同时通过掩码机制区分可用模态与缺失模态，为后续扩散模型提供富含上下文的条件嵌入。

**超图构建**：对于包含 $N$ 条话语的对话，超边集合 $\mathcal{E}$ 包含上下文超边 $e_i^c$（连接同一话语的所有模态节点）和多模态超边 $e_i^m$（连接所有话语的同一模态节点），总计 $|\mathcal{E}| = N + 3$ 条超边。

**节点到超边的注意力聚合**：第 $l$ 层超边 $e_j$ 的更新表示为：

$$e_j^{l+1} = \sigma\left(\sum_{v_i \in \mathcal{V}_j} \alpha_{ji} W_1 v_i^l\right)$$

其中 $\mathcal{V}_j$ 为超边 $e_j$ 所连接的所有节点集合，$W_1$ 为可学习权重矩阵，$\sigma$ 为激活函数。注意力权重 $\alpha_{ji}$ 计算如下：

$$\alpha_{ji} = \frac{\exp\left(\mathrm{LeakyReLU}\left(\mathbf{a}_1^\top [W_1 v_i^l \| W_2 e_j^l]\right)\right)}{\sum_{v_k \in \mathcal{V}_j} \exp\left(\mathrm{LeakyReLU}\left(\mathbf{a}_1^\top [W_1 v_k^l \| W_2 e_j^l]\right)\right)}$$

其中 $\mathbf{a}_1$ 为注意力向量，$\|$ 表示拼接操作，$W_2$ 为超边变换矩阵。

**超边到节点的反向聚合**：对称地，节点 $v_i$ 从其所关联的所有超边 $\mathcal{E}_i$ 聚合信息，注意力权重为：

$$\alpha_{ij} = \frac{\exp\left(\mathrm{LeakyReLU}\left(\mathbf{a}_2^\top [W_2 e_j^{l+1} \| W_1 v_i^l]\right)\right)}{\sum_{e_k \in \mathcal{E}_i} \exp\left(\mathrm{LeakyReLU}\left(\mathbf{a}_2^\top [W_2 e_k^{l+1} \| W_1 v_i^l]\right)\right)}$$

经过多层 MHGAT 迭代后，所有节点的最终表示沿模态维度拼接，形成条件嵌入 $C \in \mathbb{R}^{N \times 3d}$，作为扩散模型的条件输入。

#### 3.1.2 条件扩散模型

扩散模型以前向加噪与反向去噪为核心，MHGAT 输出的条件嵌入 $C$ 通过 U-Net 的交叉注意力机制注入去噪过程。

**条件注入方式**：在 U-Net 的第 $l$ 层，条件 $C$ 通过线性投影后与特征图进行交叉注意力融合：

$$\boldsymbol{F}^{(l+1)} = \mathrm{Concat}\left(\boldsymbol{F}^{(l)}, \mathrm{CrossAttn}\left(\boldsymbol{F}^{(l)}, \mathrm{Linear}(\boldsymbol{C})\right)\right)$$

**训练损失**：以随机丢弃概率 $p$ 训练时，目标是最小化预测噪声与真实噪声的均方误差：

$$\mathcal{L} = \mathbb{E}_{\mathbf{x}_0, C, t, \epsilon \sim \mathcal{N}(0, \mathbf{I})} \left[ \| \epsilon_\theta(\mathbf{x}_t, C, p) - \epsilon \|^2 \right]$$

其中 $\mathbf{x}_0$ 为原始特征，$\mathbf{x}_t$ 为第 $t$ 时间步的加噪特征，$\epsilon_\theta$ 为 U-Net 预测的噪声。

**无分类器引导采样**：推理时，通过组合条件预测与无条件预测来增强条件信号：

$$\hat{\epsilon}_\theta(\mathbf{x}_t, C) = \epsilon_\theta(\mathbf{x}_t, \mathcal{O}) + w \cdot \left(\epsilon_\theta(\mathbf{x}_t, C) - \epsilon_\theta(\mathbf{x}_t, \mathcal{O})\right)$$

其中 $\mathcal{O}$ 表示空条件，$w$ 为引导强度权重。最终采样步骤为：

$$\mathbf{x}_{t-1} = \tilde{\mu}_t(\mathbf{x}_t, t, C) + \sigma_t \cdot z, \quad z \sim \mathcal{N}(0, \mathbf{I})$$

### 3.2 双通道证据融合（DCEF）

DCEF 从两个粒度解耦不确定性：**特征源不确定性**（恢复质量）和**判别层不确定性**（分类置信度），并将其统一为证据质量，通过 Dempster-Shafer 理论（DST）进行迭代融合。

#### 3.2.1 双重不确定性估计

**特征源不确定性**：基于扩散模型最后一时间步 $T$ 的噪声预测均方误差，衡量恢复特征与真实特征的偏离程度：

$$u = \| \epsilon - \epsilon_\theta(\mathbf{x}_T, T, C) \|_2^2$$

$$m_s(\Omega) = a \cdot \mathrm{Sigmoid}\left(b \cdot (u - \bar{u})\right)$$

其中 $\bar{u}$ 为批次内平均误差，$a, b$ 为可学习缩放参数。$m_s(\Omega)$ 表示分配给“通用集”（即不确定）的证据质量。

**判别层不确定性**：通过归一化预测熵衡量分类决策的模糊程度：

$$m_d(\Omega) = \frac{-\sum_{k=1}^K P_k \log(P_k)}{\log K}$$

其中 $P_k$ 为分类器对第 $k$ 类的预测概率，$K$ 为类别数。

#### 3.2.2 证据质量组合与 DST 融合

将两路不确定性组合为统一的证据质量：

$$m(\Omega) = \gamma \cdot m_d(\Omega) + m_s(\Omega)$$

$$m(k) = (1 - m(\Omega)) P_k$$

其中 $\gamma$ 为平衡系数。最终，各模态的证据通过 Dempster 组合规则进行迭代成对融合：

$$(m_1 \oplus m_2)(A) = \frac{\sum_{B \cap C = A} m_1(B) m_2(C)}{1 - \sum_{B \cap C = \emptyset} m_1(B) m_2(C)}$$

融合完成后取信度最高的类别作为最终预测。

![[assets/figures/papers/paper_list_l840_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Beyond_Missing_Mod/figures/005_Figure_3.jpg]]
*Figure 3: Aggregation process of MHGAT and visualization of attention assigned to each node and edge*

## 实验与关键发现

### 整体性能对比

HyperEF 在三个主流多模态情感识别基准上均表现出显著优势。Table 1 报告了 IEMOCAP4、IEMOCAP6 和 MELD 数据集在缺失率 κ 从 0.0 到 0.7 下的准确率对比。在完全模态（κ=0.0）设置下，HyperEF 在 IEMOCAP4 上达到 82.9%，已超过所有对比方法。随着缺失率增加，性能差距进一步拉大：在 κ=0.1 时 HyperEF 达到 82.1%，较最强基线 **SDR-GNN**（Fu et al., KBS 2025）的 78.6% 提升 3.5 个百分点；在 IEMOCAP6 的 κ=0.2 设置下达到 64.1%，较该设置下最强基线提升 2.9 个百分点；在 MELD 的 κ=0.2 设置下达到 69.3%，提升 2.2 个百分点。值得注意的是，在 IEMOCAP6 缺失率 0.6 的极端条件下，HyperEF 精度提升达 4.0%，验证了方法在高缺失率场景下的鲁棒性。

![[assets/figures/papers/paper_list_l840_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Beyond_Missing_Mod/figures/003_Table_1.jpg]]
*Table 1: Accuracy (%) comparison of methods on IEMOCAP4, IEMOCAP6, and MELD datasets under varying missing modality rates. We bold the highest accuracy and underline the second-best accuracy*

**瓶颈归因**：基线方法（如 **GCNet**（Lian et al., TPAMI 2023）的图补全、**IMDer**（Wang et al., NeurIPS 2023）的无引导扩散恢复、**MMIN**（Zhao et al., ACL/IJCNLP 2021）的缺失模态想象）在缺失率升高时性能退化明显，根源在于它们未能有效建模缺失模态与可用模态之间的高阶语义依赖，且融合阶段缺乏对恢复特征不确定性的细粒度量化。

### 恢复质量分析

Table 3 从恢复误差（MSE）和分布差异（MMD）两个维度量化了缺失模态恢复质量。HyperEF 在所有模态（文本/声学/视觉）上的 MSE 和 MMD 均低于 IMDer，表明 MHGAT 条件扩散恢复的特征不仅在数值上更接近原始特征，在分布层面也与原始特征更一致。Figure 4 的 t-SNE 可视化进一步印证了这一结论：HyperEF 恢复特征的聚类结构与原始特征高度重叠，而 IMDer 恢复特征则呈现明显的分布偏移和类间混淆。这解释了 HyperEF 在后续融合阶段能获得更高精度的原因——语义一致的恢复特征减少了对融合模块的干扰。

![[assets/figures/papers/paper_list_l840_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Beyond_Missing_Mod/figures/009_Figure_4.jpg]]
*Figure 4: t-SNE visualization of recovered and original features from HyperEF and IMDer on two datasets*

### 消融实验

**MHGAT 的效率与效能**（Table 2）：在 MELD 和 IEMOCAP4 的 κ=0.3 和 κ=0.5 设置下，MHGAT 仅使用 Transformer 编码器约 23% 的参数量，即可达到相当或略优的准确率。这归功于超图结构对模态内、模态间及对话上下文高阶交互的紧凑编码能力，避免了 Transformer 全连接自注意力带来的冗余计算。

**不确定性解耦策略**（Table 4）：在 MELD κ=0.3 设置下，基于熵的判别层不确定性作为第二解耦方向取得 63.78% 的最高准确率，显著优于基于 vacuity、dissonance 或 consonance 的单一不确定性策略。这表明分类决策层的模糊程度（熵）与特征源重建误差捕捉了互补的不确定性信号，二者的解耦与组合是 DCEF 有效性的关键。

**目标函数组件贡献**（Table 5）：移除 vacuity 不确定性损失（即仅保留交叉熵与 KL 正则项）时，MELD 准确率骤降至 50.40%，降幅超过 18 个百分点。vacuity 损失的作用是迫使模型为每个模态维持足够的证据量，避免在缺失模态场景下过早陷入低证据、高置信的错误决策。该结果直接验证了 DCEF 中证据量约束的必要性。

### 关键实验结论

1. **MHGAT 条件扩散是缺失模态恢复的核心使能器**：超图引导的条件信息使扩散模型能捕捉跨模态高阶语义依赖，恢复特征在 MSE 和 MMD 上均优于无引导扩散基线，且 t-SNE 可视化显示分布一致性显著提升。
2. **双重不确定性解耦是鲁棒融合的关键**：特征源不确定性（基于扩散最后时间步的噪声预测误差）与判别层不确定性（基于分类熵）捕获了不同层面的冲突信号，二者的证据级融合在所有解耦策略中取得最优性能。
3. **vacuity 约束不可或缺**：移除 vacuity 损失导致性能崩溃，证实了在缺失模态场景下显式建模证据量对防止过自信错误预测至关重要。

![[assets/figures/papers/paper_list_l840_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Beyond_Missing_Mod/figures/004_Table_2.jpg]]
*Table 2: Performance and cost of MHGAT and Transformer encoder on MDLE and IEMOCAP4 at missing rates 0.3 and 0.5*

![[assets/figures/papers/paper_list_l840_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Beyond_Missing_Mod/figures/008_Table_5.jpg]]
*Table 5: Ablation study on IEMOCAP4 and MELD with a 0.3 missing rate at different target function switches*

## 定位与知识库关联

### 缺失模态恢复的方法谱系

HyperEF 处于**缺失模态恢复**与**不确定性感知融合**两条技术路线的交汇点。在缺失模态恢复一侧，现有方法可大致分为三类：

**（1）基于想象/生成的恢复方法。** **MMIN**（Zhao et al., ACL/IJCNLP 2021）通过级联残差自编码器从可用模态“想象”缺失模态的特征，但缺乏对对话上下文高阶依赖的建模，恢复特征与原始特征在语义空间存在偏移。**IMDer**（Wang et al., NeurIPS 2023）首次将扩散模型引入缺失模态恢复，但采用无引导的生成方式，恢复过程缺乏对多模态语义结构的显式约束，导致恢复特征与原始特征的分布差异较大（见 Table 3 中 MMD 指标）。

**（2）基于图补全的方法。** **GCNet**（Lian et al., TPAMI 2023）利用图卷积网络对不完整多模态数据进行补全，但常规图结构仅能建模成对关系，难以捕捉多模态对话中模态内、模态间及上下文的多元交互。**SDR-GNN**（Fu et al., KBS 2025）在谱域进行图重建，但仍受限于图结构的表达容量。

**（3）基于不确定性建模的方法。** 现有工作多采用等权融合或仅基于空位（vacuity）的证据融合，缺乏对恢复特征质量和判别层模糊性的细粒度解耦。

### HyperEF 的核心创新定位

HyperEF 的关键突破在于将**超图结构建模**与**条件扩散生成**深度耦合，并配合**双重证据融合**形成闭环。具体而言：

| 改进维度 | 基线方法 | HyperEF 方案 | 证据支撑 |
|---------|---------|-------------|---------|
| 关系建模 | 常规 GNN / Transformer（成对关系） | MHGAT 超图注意力（高阶多元关系 + 掩码机制） | Table 2：仅用 Transformer 23% 参数量达到相当/更优精度 |
| 恢复引导 | 直接扩散或无引导生成 | MHGAT 条件嵌入指导去噪过程 | Table 3：恢复特征 MMD 更低，分布更一致 |
| 不确定性融合 | 等权融合或仅 vacuity | DCEF 双重解耦（特征源 + 判别层） | Table 4：熵解耦策略最优（63.78%） |

MHGAT 的条件嵌入为扩散模型提供了**语义一致的恢复方向**——超图结构同时编码了模态内依赖（通过多模态超边）、模态间交互（通过上下文超边）以及缺失状态（通过掩码机制），使得条件 $C$ 包含了对缺失模态的“预期语义”。这一设计使 HyperEF 区别于 IMDer 等无条件扩散方法，在 IEMOCAP6 缺失率 0.6 时精度提升 4.0%（Table 1）。

DCEF 的双重不确定性解耦是该工作的另一差异化贡献。特征源不确定性 $m_s(\Omega)$ 基于扩散模型最后一时间步的噪声预测均方误差（Equation 12），直接反映恢复质量；判别层不确定性 $m_d(\Omega)$ 基于归一化分类熵（Equation 13），捕捉决策边界的模糊性。两者通过 Dempster-Shafer 理论组合为统一证据质量 $m(\Omega) = \gamma \cdot m_d(\Omega) + m_s(\Omega)$，实现了**恢复质量与决策置信度的联合校准**。Table 5 的消融实验表明，移除 vacuity 不确定性损失后 MELD 准确率骤降至 50.40%，验证了不确定性建模对维持足够证据量的关键作用。

### 适用边界与局限

**适用场景：** HyperEF 的设计天然适用于**多模态对话情感识别**中任意模态随机缺失的场景，其超图结构对对话上下文和说话人切换具有显式建模能力（Figure 1 展示了跨话语的语义推理过程）。方法在缺失率 0.0–0.7 范围内均保持稳定优势（Table 1），表明其对不同程度缺失具有鲁棒性。

**潜在局限（需手动验证）：**

1. **计算开销：** 条件扩散模型的采样过程需要多步去噪，尽管 MHGAT 参数量仅为 Transformer 的 23%，但扩散采样本身的计算成本在实时场景下可能成为瓶颈。论文未提供推理延迟的对比数据，需要实际部署验证。

2. **模态扩展性：** 当前实验仅覆盖文本、视觉、声学三种模态。超图结构理论上可扩展至更多模态，但超边数量的增长（$N+3$ 条超边对应 $N$ 条话语）可能导致注意力计算复杂度上升，扩展性需进一步验证。

3. **缺失模式假设：** 实验采用完全随机缺失（MCAR）模式，但真实场景中缺失往往具有系统性（如视频传输中断导致视觉连续缺失）。HyperEF 对非随机缺失模式的泛化能力尚未验证。

4. **跨数据集迁移：** 论文在 IEMOCAP 和 MELD 上进行了实验，但两个数据集在情感类别分布、对话场景上存在差异。方法对更多样化数据集的迁移能力需要额外验证。

### 开放问题

1. **条件扩散的引导强度：** 无分类器引导权重 $w$（Equation 8）对恢复质量的影响机制尚未深入分析。过强的引导可能导致恢复特征过度依赖条件而丧失多样性，过弱则退化为无引导生成。$w$ 的最优值与缺失率、模态类型的依赖关系值得进一步研究。

2. **不确定性解耦的理论基础：** DCEF 将特征源不确定性与判别层不确定性线性组合，但两者可能存在非线性交互。是否存在更优的组合方式（如基于互信息的加权）是开放问题。

3. **超图结构的动态学习：** 当前超图结构（上下文边 + 多模态边）是预定义的。是否可以通过端到端学习动态构建超边，使图结构自适应于对话内容和缺失模式，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Beyond_Missing_Modalities_Hypergraph_Conditioned_Diffusion_for_Uncertainty_Aware_Multimodal_Emotion_Recognition.pdf]]
