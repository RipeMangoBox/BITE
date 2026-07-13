---
title: "TANGO: Text-Anchored Guided Optimization for Robust Fine-tuning Vision-Language Models under Label Noise"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TANGO_Text_Anchored_Guided_Optimization_for_Robust_Fine_tuning_Vision_Language_Models_under_Label_Noise.pdf
project_link: null
code_link: null
aliases:
- TTAGO
- TANGO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用冻结文本编码器生成多描述性提示的不可变语义锚点，构建类别纯正的固定参考系，将分类决策与样本精炼直接锚定于此外部真值，切断噪声标签的自我强化。
primary_logic: 视觉语言模型的文本模态不仅能检测噪声，更能通过多样化文本描述构建一个不变的、类别纯正的语义参考系；将视觉编码器的优化从对噪声标签的被动纠错转变为朝向该干净语义参考系的主动跨模态对齐，从而在标签噪声下保持鲁棒性。
claims:
- TANGO在CIFAR-100N真实噪声下达到83.83%准确率，超越最强VLM专用方法DeFT 4.79个百分点。
- 在CIFAR-100 60%对称噪声下，TANGO取得87.89%最佳准确率，达到该基准最高水平。
- 消融实验证实，去除文本锚点分类器或纯视觉方案均导致性能大幅下降，证明TAC和跨模态精炼的关键作用。
- 在锚点被90%噪声污染的压力测试中，TANGO仍保持82.51%准确率，显示锚点质量的高度鲁棒性。
---

# TANGO: Text-Anchored Guided Optimization for Robust Fine-tuning Vision-Language Models under Label Noise

> [!tip] 核心洞察
> 视觉语言模型的文本模态不仅能检测噪声，更能通过多样化文本描述构建一个不变的、类别纯正的语义参考系；将视觉编码器的优化从对噪声标签的被动纠错转变为朝向该干净语义参考系的主动跨模态对齐，从而在标签噪声下保持鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | TANGO：面向标签噪声下稳健微调视觉语言模型的文本锚定引导优化 |
| 英文题名 | TANGO: Text-Anchored Guided Optimization for Robust Fine-tuning Vision-Language Models under Label Noise |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ma_TANGO_Text-Anchored_Guided_Optimization_for_Robust_Fine-tuning_Vision-Language_Models_under_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TANGO (Text-ANchored Guided Optimization) |
| Dataset | CIFAR-100, Tiny-ImageNet, CIFAR-100N, WebVision |

> [!tip] 效果简介
> - CIFAR-100 (Sym. 60%) 上，Test Accuracy (%) 87.89 (Best) / 87.83 (Last) vs State-of-the-art (具体基准值见表1，TANGO均优于所有对比方法) (–)。
> - Tiny-ImageNet (Sym. 60%) 上，Test Accuracy (%) 82.10 (Best) / 82.00 (Last) vs State-of-the-art (见表2) (–)。
> - CIFAR-100N (Real-world Noise) 上，Test Accuracy (%) 83.83 vs DeFT 79.04 (基于提升4.79%推算) (+4.79)。

## 概要

**问题瓶颈**：在标签噪声下微调视觉语言模型（VLMs）时，传统方法存在根本性的自我循环缺陷——它们依赖模型自身的预测（如小损失准则、高置信度伪标签）来检测或纠正噪声，这会产生确认偏差并逐步扭曲语义空间。即使近期的跨模态方法（如 **DeFT**，Wei et al., NeurIPS 2024）也仅将文本用于噪声检测，而未将其作为独立于噪声标签的外部真实参照。因此，视觉编码器的优化始终被噪声标签所支配。

**核心洞察**：视觉语言模型的文本模态不仅能检测噪声，更能通过多样化的文本描述构建一个**不变的、类别纯正的语义参考系**。TANGO 的核心思想是将视觉编码器的优化，从对噪声标签的被动纠错，转变为朝向这个干净语义参考系的主动跨模态对齐——从而在标签噪声下从根本上保持鲁棒性。

**方法定位**：TANGO 提出了一种**文本锚定引导优化**框架，通过三个关键组件实现上述思想：（1）利用冻结文本编码器预计算多描述性提示的**语义锚点**，形成不可变的干净参考系；（2）以无参数的**文本锚定分类器（TAC）** 替代传统线性分类器，使分类决策始终锚定于文本真值；（3）通过**锚点引导的样本精炼**机制，将样本选择与标签校正从纯视觉模态提升为跨模态语义验证与真值注入。

**主要结果**：TANGO 在合成噪声和真实世界噪声场景下均取得最优性能。在 CIFAR-100 60% 对称噪声下达到 **87.89%** 的测试准确率；在真实噪声数据集 CIFAR-100N 上达到 **83.83%**，超越最强 VLM 专用方法 DeFT **4.79 个百分点**；在 WebVision、ILSVRC2012、Animal-10N、Food101N 等五个真实噪声基准上同样取得领先结果。消融实验和压力测试进一步证实，TAC 与跨模态精炼机制是性能提升的关键，且方法对锚点质量和超参数均具有高度鲁棒性。

### 标签噪声下的视觉语言模型微调困境

视觉语言模型（VLMs）如CLIP在开放世界视觉任务中展现了强大的泛化能力。然而，当其在下游任务上微调时，一个关键瓶颈浮现：**训练数据中的标签噪声**会严重损害模型性能。传统微调策略在噪声标签上直接训练线性分类器，导致模型学习到错误的视觉-类别映射关系。

问题的核心在于**自我循环的确认偏差**（confirmation bias）。现有方法——无论是经典的半监督学习策略（如**DivideMix**, Li et al., ICLR 2020），还是VLM专用去噪方法（如**DeFT**, Wei et al., NeurIPS 2024）——本质上仍依赖模型自身对样本的预测来进行噪声检测或标签校正。这种“以己之矛攻己之盾”的方式，使得初始噪声标签引发的错误预测会不断强化自身，最终扭曲整个语义空间。

### 现有方法的缺口：文本模态的未充分利用

VLM的独特优势在于其**跨模态对齐能力**——文本编码器和视觉编码器共享同一语义空间。然而，现有方法对这一特性的利用存在明显局限：

- **纯视觉方法**（如LSL, Kim et al., CVPR 2024）完全忽略文本模态，仅依赖视觉特征的k-NN邻居或小损失准则进行样本筛选，在噪声邻居的干扰下容易失效。
- **跨模态方法**（如DeFT）虽引入文本生成正负提示来构建噪声检测器，但文本仅被用作**噪声检测的辅助工具**，而非独立于噪声标签的**外部真值参照**。其优化目标仍是通过过滤后的噪声标签驱动视觉编码器，未能从根本上切断噪声的自我强化链路。

### TANGO的核心动机：将文本锚定为不变真值

本文的核心洞察在于：**VLMs的文本模态不仅能检测噪声，更能通过多样化的文本描述构建一个不变的、类别纯正的语义参考系**。这一参考系天然独立于训练数据中的标签噪声，因此可以作为优化过程中的“北极星”。

TANGO（Text-ANchored Guided Optimization）的动机正是将视觉编码器的优化，从对噪声标签的被动纠错，转变为朝向干净语义参考系的**主动跨模态对齐**。通过将分类决策和样本精炼直接锚定于冻结文本编码器生成的语义锚点，TANGO切断了噪声标签的自我强化循环，使模型在标签噪声下保持鲁棒性。

## 核心方法与创新机理

TANGO的核心创新在于将视觉语言模型（VLM）的**文本模态从辅助噪声检测工具升级为不可变的外部真值参照系**，从而切断传统标签噪声学习方法中普遍存在的“自我循环”确认偏差。具体而言，TANGO在三个关键环节上完成了对标准微调范式的根本性改造：

### 1. 从可学习线性分类器到无参数文本锚定分类器（TAC）

标准微调流程在视觉编码器之上附加一个可学习的线性分类矩阵 $\mathbf{W}$，其参数完全依赖（可能含噪的）标签信号进行优化，极易在噪声环境中产生确认偏差。TANGO用**无参数的文本锚定分类器（Text-Anchored Classifier, TAC）** 彻底替换了这一结构：预计算每个类别 $K$ 个描述性提示的文本嵌入作为**固定语义锚点**，分类时直接计算图像特征与所有锚点的加权余弦相似度，并通过锚点标签的加权求和产生 logits：

$$l_i = \alpha_i^T \mathbf{Y}_A$$

其中 $\alpha_i$ 是图像 $i$ 与所有锚点的指数化相似度向量，$\mathbf{Y}_A$ 是锚点的干净 one-hot 标签矩阵。这一设计使分类决策**始终锚定于冻结文本编码器提供的语义真值**，从根本上杜绝了噪声标签对分类边界的污染。

### 2. 从纯视觉样本选择到跨模态语义验证

传统方法依赖视觉 $k$-NN 投票或小损失准则判断样本洁净度，当噪声样本在特征空间中形成密集簇时，这些纯视觉信号会系统性失效。TANGO引入**跨模态语义验证机制**，将视觉邻居投票分数 $\mathbf{p}_i^{\text{vis}}$ 与基于锚点邻居的语义一致性信号 $\mathbf{p}_i^{\text{sem}}$ 进行加权融合：

$$\tilde{\mathbf{q}}_i = (1 - \beta) \cdot \mathbf{p}_i^{\text{vis}} + \beta \cdot \mathbf{p}_i^{\text{sem}}$$

语义信号通过构建图像-锚点二分图，聚合每个样本的锚点近邻标签得到，为洁净度判断注入了**独立于训练标签分布的外部真值信息**，有效对抗视觉空间中噪声样本的干扰。

### 3. 从自举伪标签到真值注入标签校正

传统标签校正依赖模型自身高置信度预测生成伪标签，本质上仍是噪声标签的自我强化。TANGO提出**真值注入（Truth Injection）** 策略：通过语义-视觉二分图的转置，将锚点的干净标签直接传播至训练样本，形成语义软伪标签矩阵：

$$\mathbf{Y}^{\text{sem}} = \mathbf{D}^{-1} (\mathbf{A}^{sv})^{\top} \mathbf{Y}_{\mathcal{A}}$$

该矩阵与视觉传播软标签融合后，为所有样本提供**包含外部真值信息的校正软伪标签**，使监督信号不再完全受制于原始噪声标签的质量。

这三个改造槽位（changed slots）共同实现了TANGO的核心洞察：将视觉编码器的优化目标从“对噪声标签的被动纠错”转变为“朝向干净语义参考系的主动跨模态对齐”。消融实验（Table 4）证实，移除任一组件均会导致性能大幅下降，验证了每个改造槽位的不可或缺性。

TANGO 的整体 pipeline 围绕一个核心设计展开：**将冻结文本编码器生成的语义锚点作为不可变的外部真值参考系，贯穿分类决策与样本精炼的全过程**，从而切断噪声标签的自我强化循环。

### 框架总览

TANGO 的输入包括一个预训练的视觉语言模型（默认 CLIP ViT-B/16）、一个噪声标签数据集，以及每个类别 $K$ 条描述性文本提示（如 CuPL 提示）。框架由三个关键模块构成闭环，如 Figure 1 所示：

![[assets/figures/papers/paper_list_l786_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_TANGO_Text_Anchored/figures/001_Figure_1.jpg]]
*Figure 1: A conceptual illustration of TANGO’s core principle. (Left) Conventional uni-modal supervision relies solely on a sample’s neighbors, which can be noisy and thus provide a corrupted supervisory signal. (Right) TANGO introduces robust cross-modal supervision. By leveraging a set of clean Semantic Anchors, it provides a semantic signal that guides the learning process, actively counteracting the influence from noisy neighbors*

1. **语义锚点构建（一次性预计算）**：使用冻结的文本编码器 $f_t$ 将所有类别的 $K$ 条文本提示编码为固定锚点特征向量，形成类别纯正的语义参考系 $\mathcal{A}_c = \{t_{c,k} \mid t_{c,k} = f_t(\mathbf{p}_{c,k})\}_{k=1}^{K}$。
2. **文本锚定分类器（TAC）**：替代传统可学习线性分类器，通过计算图像嵌入 $\mathbf{v}_i$ 与所有锚点 $\mathbf{t}_j$ 的加权余弦相似度直接产生 logits $\mathbf{l}_i = \alpha_i^T \mathbf{Y}_A$，使预测始终锚定于干净文本真值。
3. **锚点引导样本精炼**：在每个 epoch 前，利用跨模态语义验证进行样本选择与标签校正——融合视觉 $k$-NN 投票与锚点邻居一致性分数来选择洁净样本，并通过锚点-图像二分图传播将干净标签注入训练样本。

这三个模块以**交替优化循环**的方式运行：epoch 级的样本精炼为 batch 级的视觉编码器训练提供高质量监督信号，训练损失由洁净样本上的硬标签交叉熵 $\mathcal{L}_{\text{clean}}$ 和全样本上的锚点增强软伪标签正则化 $\mathcal{L}_{\text{reg}}$（结合 Mixup 增强）共同构成。

### 与传统 pipeline 的本质差异

传统 VLM 微调在标签噪声下存在结构性缺陷：分类器（线性矩阵 $\mathbf{W}$）与样本选择（小损失准则或纯视觉 $k$-NN）均依赖模型自身预测，形成**自我循环**，易产生确认偏差并扭曲语义空间。即使跨模态方法（如 **DeFT**，Wei et al., NeurIPS 2024）也仅将文本用于噪声检测，而未将其作为独立于噪声标签的外部真值参照。

TANGO 的因果杠杆在于：**将视觉编码器的优化目标从“拟合噪声标签”重新定义为“朝向干净语义锚点的跨模态对齐”**。文本锚点作为不可变参考系，使分类决策始终锚定于外部真值；跨模态精炼则利用这一参考系同时校正样本选择与标签，切断了噪声标签的自我强化路径。

### 输入输出流

- **输入**：噪声训练集 $\{(\mathbf{x}_i, \tilde{y}_i)\}$、每类 $K$ 条文本提示、预训练 VLM（视觉编码器 $f_v$ + 冻结文本编码器 $f_t$）。
- **预计算**：语义锚点集合 $\mathcal{A}$ 及其 one-hot 标签矩阵 $\mathbf{Y}_A$。
- **每 epoch 精炼**：输出洁净样本子集与校正软伪标签矩阵 $\tilde{\mathbf{Y}}$。
- **每 batch 训练**：更新视觉编码器 $f_v$ 参数。
- **推理**：直接使用 TAC 进行预测，无需额外分类头。

这一设计使 TANGO 在保持端到端可微性的同时，将跨模态对齐从预处理步骤提升为学习目标的核心本质。

TANGO的核心设计理念是用**冻结文本编码器生成的语义锚点**构建一个不可变、类别纯正的参考系，将视觉编码器的优化从“对噪声标签的被动纠错”转变为“朝向干净语义参考系的主动跨模态对齐”。整个框架由四个关键模块构成，呈交替优化循环。

### 3.1 稳定跨模态语义锚点

锚点是TANGO的基石。对于每个类别 $c$，利用冻结的预训练文本编码器 $f_t$ 将 $K$ 个描述性文本提示（如CuPL提示）编码为固定的特征向量集合：

$$\mathcal { A } _ { c } = \{ t _ { c , k } ~ | ~ t _ { c , k } = f _ { t } ( \mathbf { p } _ { c , k } ) \} _ { k = 1 } ^ { K }$$

其中 $\mathbf{p}_{c,k}$ 是类别 $c$ 的第 $k$ 个文本提示，$t_{c,k}$ 是其编码后的锚点特征向量。所有类别的锚点拼接为全局锚点集合 $\mathcal{A}$，其对应的one-hot标签矩阵记为 $\mathbf{Y}_{\mathcal{A}}$。这一过程是**一次性预计算**，在整个训练过程中保持冻结，为后续所有模块提供不可变的干净语义参照。

### 3.2 文本锚定分类器（TAC）

传统微调使用可学习的线性分类器 $\mathbf{W}$ 将图像特征 $\mathbf{v}_i$ 映射为logits：$\mathbf{l}_i = \mathbf{W} \mathbf{v}_i$。TANGO将其替换为**无参数的文本锚定分类器**，使分类决策始终锚定于文本真值。

首先计算图像特征 $\mathbf{v}_i$ 与每个锚点 $\mathbf{t}_j$ 的亲和度向量：

$$( \alpha _ { i } ) _ { j } = \exp \left( \mathtt { s i m } ( \pmb { v } _ { i } , \pmb { t } _ { j } ) \right)$$

其中 $\mathtt{sim}(\cdot,\cdot)$ 为余弦相似度，指数化后形成对锚点的软注意力权重。分类logits通过亲和度加权求和干净锚点的one-hot标签得到：

$$l _ { i } = \alpha _ { i } ^ { T } {\bf Y } _ { A }$$

**关键机制**：TAC不学习任何类别相关的参数，其预测完全由图像与固定文本锚点的语义邻近度决定。这切断了噪声标签通过可学习分类器权重进行自我强化的路径——即使视觉编码器在训练初期产生有偏特征，分类决策的参照系始终是干净锚点。

### 3.3 锚点引导样本精炼

在每个epoch开始前，TANGO执行跨模态样本精炼，包含两个子模块。

**语义验证用于样本选择**。传统方法依赖纯视觉近邻投票判断样本洁净度，在噪声环境下易受污染邻居影响。TANGO引入**校正一致性分数**，融合视觉信号与语义验证信号：

$$\tilde { \pmb q } _ { i } = ( 1 - \beta ) \cdot \pmb { p } _ { i } ^ { \mathrm { v i s } } + \beta \cdot \pmb { p } _ { i } ^ { \mathrm { s e m } }$$

其中 $\mathbf{p}_i^{\mathrm{vis}}$ 是视觉k-NN投票分数，$\mathbf{p}_i^{\mathrm{sem}}$ 是语义验证信号。语义验证信号通过构建**视觉-语义二分图**计算：将图像特征作为一侧节点，锚点作为另一侧节点，边权重为图像-锚点相似度。锚点邻居的干净标签经二分图聚合到每个样本：

$$p ^ { \mathrm { s e m } } = { \frac { 1 } { | { \mathcal { A } } | / C } } { \mathbf { A } } ^ { v s } { \mathbf { Y } } _ { { \mathcal { A } } }$$

其中 $\mathbf{A}^{vs}$ 是视觉-语义二分图的邻接矩阵，$C$ 为类别数。该分数反映了样本与各锚点的语义一致性——若某样本的视觉近邻混杂噪声，但其语义锚点近邻高度一致，则 $\mathbf{p}_i^{\mathrm{sem}}$ 可纠正视觉判断的偏差。

**真值注入用于标签校正**。对筛选出的候选噪声样本，TANGO不依赖模型自身预测生成伪标签，而是通过**语义-视觉二分图**将锚点的干净标签直接传播给训练样本。首先构建二分图邻接矩阵 $\mathbf{A}^{sv}$，计算锚点聚合标签分数：

$$\mathbf { S } = ( \mathbf { A } ^ { s v } ) ^ { \top } \mathbf { Y } _ { \mathcal { A } }$$

行归一化后得到每个样本的语义软伪标签：

$$\mathbf { Y } ^ { \mathrm { s e m } } = \mathbf { D } ^ { - 1 } \mathbf { S } = \mathbf { D } ^ { - 1 } ( \mathbf { A } ^ { s v } ) ^ { \top } \mathbf { Y } _ { \boldsymbol { A } }$$

其中 $\mathbf{D}$ 是度矩阵。最终融合伪标签矩阵为：

$$\tilde { \mathbf { Y } } = ( 1 - \beta ) \cdot \mathbf { Y } ^ { \mathrm { v i s } } + \beta \cdot \mathbf { Y } ^ { \mathrm { s e m } }$$

$\mathbf{Y}^{\mathrm{vis}}$ 是视觉传播软标签，$\mathbf{Y}^{\mathrm{sem}}$ 是语义真值注入。混合权重 $\beta$ 控制语义锚点的影响力。

### 3.4 交替优化循环

TANGO采用**epoch级样本精炼 + batch级模型训练**的交替优化策略：

- **Epoch级样本精炼**：每个epoch开始前，利用当前视觉编码器提取的特征，执行锚点引导样本精炼，更新洁净样本集和校正软伪标签。
- **Batch级模型训练**：训练损失由两部分组成——仅对洁净样本计算硬标签交叉熵 $\mathcal{L}_{\mathrm{clean}}$，以及对全样本施加锚点增强软伪标签正则化 $\mathcal{L}_{\mathrm{reg}}$（结合Mixup增强）。

这种设计使得视觉编码器始终朝着与固定语义锚点对齐的方向优化，而非拟合可能含噪的标签分布。锚点的不可变性提供了稳定的优化目标，跨模态精炼则持续提升监督信号的质量。

## 实验与关键发现

### 核心实验设置

TANGO 采用 CLIP ViT-B/16 作为视觉编码器，在合成噪声和真实世界噪声两个维度上系统评估。合成噪声实验覆盖 CIFAR-100 和 Tiny-ImageNet，噪声类型包括对称噪声（Sym.）、非对称噪声（Asym.）和实例依赖噪声（Inst.），噪声比例从 20% 到 60%。真实世界噪声实验覆盖 CIFAR-100N、WebVision、ILSVRC2012、Animal-10N 和 Food-101N 五个基准。关键超参数固定为每类锚点数量 $K=40$、语义一致性权重 $\beta=0.5$，所有实验采用 CuPL 提示模板生成锚点。

### 合成噪声主结果

在 CIFAR-100 的 60% 对称噪声条件下，TANGO 达到 **87.89%** 的 Best 准确率和 87.83% 的 Last 准确率，在所有对比方法中位列第一（Table 1）。在 Tiny-ImageNet 的相同噪声设置下，TANGO 取得 **82.10%** Best / 82.00% Last 的准确率，同样达到最优（Table 2）。值得关注的是，TANGO 在多种噪声类型（对称、非对称、实例依赖）和不同噪声比例（20%、40%、60%）下均保持领先，表明跨模态锚点机制对噪声类型和强度具有广泛适应性。

![[assets/figures/papers/paper_list_l786_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_TANGO_Text_Anchored/figures/002_Table_1.jpg]]
*Table 1: Test accuracy (%) on CIFAR-100 with various synthetic noise types. “Best” and “Last” denote the highest accuracy and the accuracy of the final epoch, respectively*

![[assets/figures/papers/paper_list_l786_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_TANGO_Text_Anchored/figures/003_Table_2.jpg]]
*Table 2: Test accuracy (%) on Tiny-ImageNet under various synthetic noise conditions*

### 真实世界噪声主结果

在真实噪声数据集上，TANGO 展现出更强的优势。CIFAR-100N 上达到 **83.83%**，超越 VLM 专用去噪方法 **DeFT**（Wei et al., NeurIPS 2024）4.79 个百分点（Table 3）。在 WebVision 验证集上取得 87.44%，ILSVRC2012 测试集上取得 86.44%，均达到最优水平。在 Animal-10N 和 Food-101N 上分别达到 93.62% 和 91.83%，进一步验证了方法在不同领域的泛化能力。

![[assets/figures/papers/paper_list_l786_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_TANGO_Text_Anchored/figures/006_Table_3.jpg]]
*Table 3: Test accuracy (%) on five real-world noisy dataset benchmarks*

### 消融实验

Table 4 的消融实验揭示了各组件的因果贡献。移除文本锚定分类器（TAC）回退到标准线性分类器时，CIFAR-100 合成噪声和 CIFAR-100N 真实噪声上的性能均大幅下降，证实 TAC 作为不可变语义参考系的核心作用。仅使用视觉模态的样本精炼（去除语义验证信号）同样导致性能退化，说明跨模态一致性评分的独立贡献。完整框架（TAC + 跨模态精炼）在所有设置下均显著优于各变体，验证了锚点引导与跨模态融合的双向协同效应。

![[assets/figures/papers/paper_list_l786_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_TANGO_Text_Anchored/figures/007_Table_4.jpg]]
*Table 4: Ablation study of TANGO’s components on CIFAR-100 (synthetic noise) and CIFAR-100N (real noise, R40%)*

### 锚点鲁棒性分析

压力测试（Table 7）表明，即使将 90% 的锚点替换为噪声锚点，TANGO 在 CIFAR-100N 上仍保持 **82.51%** 的准确率，仅比全干净锚点下降约 1.3 个百分点。这一结果揭示了锚点机制的关键特性：分类决策依赖于图像与锚点集合的整体语义邻近度，而非单一锚点，因此对锚点污染具有天然的容错能力。

### 超参数敏感性

Figure 2 的敏感性分析显示，每类锚点数量 $K \geq 10$ 时性能即趋于稳定，语义一致性权重 $\beta$ 在 0.3 至 0.7 的宽泛范围内均保持鲁棒。这表明方法对超参数选择不敏感，无需针对不同数据集精细调参。

### 特征空间可视化

Figure 3 的 t-SNE 可视化对比了 Animal-10N 测试集上微调前后的特征分布。原始 CLIP 空间中，各类别的视觉特征簇边界模糊且存在交叉。经 TANGO 微调后，视觉特征簇显著更紧凑，且与对应类别的语义锚点（三角标记）高度对齐。这一可视化直接验证了方法的跨模态对齐效应——视觉编码器被成功引导向干净的语义参考系靠拢，而非拟合噪声标签。

![[assets/figures/papers/paper_list_l786_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_TANGO_Text_Anchored/figures/004_Figure_3.jpg]]
*Figure 3: t-SNE visualization of the feature space on the Animal-10N test set. Circles represent image features and triangles represent semantic anchors. (Left) The original CLIP space. (Right) After fine-tuning with TANGO, visual clusters become significantly more compact and align with their corresponding semantic anchors*

### 主干网络泛化性

Table 5 在 ViT-B/32 和 SigLIP 等不同 VLM 主干上验证了 TANGO 的泛化能力。在 CIFAR-100N 上，TANGO 在所有主干上均保持性能优势，表明锚点引导优化机制不依赖于特定的视觉-语言预训练架构。

### 失败模式与局限

尽管 TANGO 在通用图像分类基准上表现优异，其有效性依赖于两个前提条件。第一，语义锚点的质量取决于文本描述对视觉多样性的覆盖程度；当任务领域高度专业化（如医学影像、遥感图像）且通用文本提示难以刻画细粒度视觉差异时，锚点的代表性可能下降。第二，视觉-语义二分图的构建依赖基础 VLM 的跨模态对齐质量；若预训练模型的跨模态空间本身对齐较弱，锚点引导的样本精炼效果可能受限。目前方法仅在图像分类任务上验证，尚未扩展到检测、分割等更复杂的视觉任务。

## 定位与知识库关联

### 1. 问题定位：标签噪声下VLM微调的范式瓶颈

在视觉语言模型（VLM）的标签噪声学习（Learning with Noisy Labels, LNL）领域，现有方法可归为两大范式，但各自存在根本性瓶颈：

**通用LNL方法的“自我循环”困境。** 以 **DivideMix**（Li et al., ICLR 2020）为代表的经典方法依赖高斯混合模型（GMM）基于小损失准则分离干净/噪声样本，并通过协同训练逐步精炼。这类方法的核心缺陷在于：监督信号完全源自模型自身对噪声标签的拟合，形成“模型预测→样本选择→模型更新”的自我循环。当初始噪声较高时，该循环极易产生确认偏差（confirmation bias），模型会逐步将噪声模式内化为“正确”知识，最终扭曲视觉语义空间。

**VLM专用方法的“单向利用”局限。** 以 **DeFT**（Wei et al., NeurIPS 2024）为代表的跨模态方法虽引入了文本模态，但其使用方式存在结构性约束：文本仅被用作噪声检测的“探针”（通过生成类特定正负提示构建检测器），检测完成后即被丢弃，后续的样本精炼与模型优化仍退回纯视觉模态。换言之，文本扮演的是“外部审计”角色，而非“持续引导”角色——它指出哪些标签可能错误，却未提供“正确标签应该是什么”的独立参照。

**TANGO的范式跃迁。** 本工作提出的TANGO（Text-ANchored Guided Optimization）将上述两种范式的瓶颈统一归因于一个核心缺失：**缺乏独立于噪声标签的外部真值参照系**。其核心洞察在于：VLM的文本编码器天然携带了类别语义的先验知识，通过多样化文本描述（如CuPL提示）可为每个类别构建一组不可变的语义锚点。TANGO的关键创新并非“使用文本”，而是**将文本锚点从辅助工具升格为分类决策与样本精炼的唯一参照系**——分类器不再包含可学习参数，而是直接计算图像与固定锚点的语义邻近度；样本选择与标签校正也不再依赖模型自身的可能已被污染的预测，而是通过跨模态二分图将锚点的干净标签传播至训练样本。这一设计切断了噪声标签的自我强化循环，将优化目标从“拟合噪声标签”转变为“朝向干净语义锚点的跨模态对齐”。

### 2. 方法谱系中的定位

#### 2.1 与通用LNL方法的关系

TANGO与以下通用LNL方法构成直接对比：

- **DivideMix**（Li et al., ICLR 2020）：基于GMM的半监督LNL方法，开创性地将噪声样本作为无标签数据利用。TANGO继承了“样本选择+半监督学习”的框架结构，但将GMM小损失准则替换为跨模态语义验证，使洁净度判断不再依赖模型自身的可能已被噪声污染的预测。
- **LSL**（Kim et al., CVPR 2024）：利用结构标签和反向k-NN进行样本重标注。TANGO的视觉k-NN投票组件与LSL共享“邻居标签传播”的思路，但TANGO通过语义验证信号对视觉投票进行校正，并额外引入锚点→样本的真值注入，形成双向跨模态融合。

TANGO与通用LNL方法的本质差异在于**监督信号的源头**：通用方法的所有监督信号（伪标签、样本权重）最终都源自模型对噪声标签的拟合，而TANGO的监督信号源自冻结文本编码器生成的不可变锚点，从根本上切断了噪声标签的自我强化。

#### 2.2 与VLM专用LNL方法的关系

- **DeFT**（Wei et al., NeurIPS 2024）：当前VLM专用LNL的代表方法，通过生成类特定正负提示构建噪声检测器。TANGO与DeFT的核心差异在于文本模态的使用深度：DeFT将文本用于“检测”后即丢弃，TANGO将文本锚点嵌入分类器结构（TAC）和样本精炼的全流程，实现文本对优化的持续引导。实验结果显示，TANGO在CIFAR-100N真实噪声上以83.83%的准确率超越DeFT 4.79个百分点，验证了“持续引导”优于“一次性检测”。

#### 2.3 与标准微调的关系

标准微调（Standard Finetuning）在噪声标签上直接使用可学习线性分类器训练视觉编码器，其分类决策完全依赖可能已被噪声污染的视觉特征变换。TANGO的文本锚定分类器（TAC）以无参数方式替代线性分类器，将分类logits定义为图像嵌入与所有固定锚点的加权余弦相似度（$l_i = \alpha_i^T Y_A$），使每个预测都直接锚定于文本真值，而非可学习的可能已被污染的权重矩阵。

### 3. 适用边界与条件

TANGO的有效性建立在以下前提之上，这些前提同时界定了其适用边界：

1. **基础VLM的跨模态对齐质量。** TAC的分类决策和跨模态二分图的构建均依赖图像特征与文本锚点的语义邻近度。若基础VLM（如CLIP）的跨模态对齐本身较弱，锚点引导的有效性将受到限制。当前实验均在CLIP系列模型上验证，其对通用视觉概念的强对齐能力是TANGO生效的隐含前提。

2. **文本描述的视觉覆盖度。** 语义锚点的质量取决于文本提示能否充分覆盖类别的视觉多样性。对于通用物体分类（CIFAR-100、Tiny-ImageNet、WebVision等），CuPL等自动生成的描述性提示已足够丰富。但当任务领域高度专业化（如医学图像、遥感、细粒度工业检测）且文本描述难以表征视觉差异时，锚点的代表性可能下降，需要更精细的提示工程或领域知识注入。论文在DTD纹理数据集上的扩展实验（Table 6）初步验证了跨领域泛化性，但该数据集仍属于通用视觉范畴。

3. **分类任务的封闭世界假设。** TANGO当前设计假设类别集合固定且锚点可预计算，适用于封闭世界分类场景。对于开放世界检测、分割等需要处理未知类别的任务，锚点构建策略需要根本性调整。

### 4. 局限分析

基于论文提供的实验证据与设计特性，识别以下局限：

1. **任务范围受限。** 当前验证仅局限于图像分类任务（合成噪声基准CIFAR-100/Tiny-ImageNet，真实噪声基准CIFAR-100N/WebVision/Animal-10N/Food101N）。论文未在检测、分割、检索等更复杂的视觉任务上验证TANGO的有效性，其跨任务泛化性尚待确认。

2. **锚点质量的外部依赖性。** 尽管压力测试（Table 7）显示TANGO在90%锚点被噪声污染时仍保持82.51%准确率，展现出对锚点质量的高度鲁棒性，但该测试仅在CIFAR-100N上进行，且“污染”方式为随机替换锚点标签。在真实场景中，锚点质量下降可能以更复杂的形式出现（如提示描述与视觉内容系统性不匹配），其影响有待进一步研究。

3. **计算开销的未充分讨论。** 每epoch前的样本精炼涉及视觉k-NN搜索和跨模态二分图构建，其计算复杂度随数据集规模增长。论文未提供与基线方法在训练时间或内存消耗上的对比分析，实际部署的可行性需要进一步评估。

4. **公平性分析的缺失。** 论文未分析模型在不同人口群体或敏感属性上的公平性表现，默认关注通用图像分类的聚合准确性。在将TANGO部署于涉及人群的视觉任务时，锚点构建中的文本描述可能引入社会偏见，需谨慎评估。

### 5. 开放问题

基于TANGO的设计逻辑与当前局限，以下开放问题值得后续探索：

1. **专业化领域的锚点增强。** 在语义高度专业化的领域（如医学影像、遥感地物分类）中，通用文本描述难以捕捉类别间的细微视觉差异。能否通过结合领域知识图谱或专家标注的半自动化流程，动态增强视觉-语义对应性以提升锚点质量？

2. **提示策展的自动化。** 当前锚点构建依赖手工设计的提示模板（如CuPL）。能否通过结合LLM生成与质量筛选的自动化流程，使方法更便捷地应用于任意新任务，同时保证锚点的纯正性与多样性？

3. **跨任务范式的扩展。** TANGO的“不可变语义锚点引导”思想能否扩展到对比学习范式（将锚点作为对比学习中的正样本参照）或其他模态（如视频中的时序文本锚点、3D中的多视角语义锚点）下的噪声标签学习？

4. **多模态锚点的混合策略。** 当前锚点仅来自文本模态，保持了“纯正性”但可能牺牲了对极端视觉多样性的覆盖。若将少量经过验证的干净图像样本加入锚点集，形成“文本锚点+视觉锚点”的混合参照系，能否在保持抗噪能力的同时提升对视觉长尾分布的覆盖？这种混合策略需要在“纯正性”与“覆盖度”之间寻找新的平衡点。

5. **理论收敛性分析。** TANGO的交替优化（epoch级样本精炼+batch级编码器训练）在实践中表现稳定，但其收敛性缺乏理论保证。在何种条件下，锚点引导的优化能够收敛到干净数据上的最优解？噪声比例与锚点质量如何影响收敛速率？这些理论问题对理解方法的根本有效性至关重要。

## 原文 PDF

![[paperPDFs/CVPR_2026/TANGO_Text_Anchored_Guided_Optimization_for_Robust_Fine_tuning_Vision_Language_Models_under_Label_Noise.pdf]]
