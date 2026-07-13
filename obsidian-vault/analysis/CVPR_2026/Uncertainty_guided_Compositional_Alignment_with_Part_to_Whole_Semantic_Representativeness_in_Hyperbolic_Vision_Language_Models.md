---
title: Uncertainty-guided Compositional Alignment with Part-to-Whole Semantic Representativeness in Hyperbolic Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Uncertainty_guided_Compositional_Alignment_with_Part_to_Whole_Semantic_Representativeness_in_Hyperbolic_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/jeeit17/UNCHA.git"
aliases:
- UUGCHA
- UGCAPWSRHVL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过双曲不确定性量化部分到整体的语义代表性，并将不确定性自适应地融入对比损失和蕴含损失中，从而调节各部分对整体对齐的贡献强度。
primary_logic: 在双曲空间中，嵌入点到原点的距离（双曲半径）可反映概念的抽象性或不确定性，更靠近原点的部分具有更高的不确定性（即对整体代表性低）；利用这一特性设计不确定性引导的对比损失和蕴含损失，可使模型更精确地捕捉部分-整体层次结构，提升组合理解能力。
claims:
- 不确定性估计与部分到整体语义相似度之间存在强负相关（r = -0.739），验证了不确定性的语义代表性。
- 在零样本图像分类、检索、层次分类、多对象表示等任务上，UNCHA一致优于先前方法。
- 消融实验表明每个组件（不确定性对比损失、不确定性校准、熵正则化）都必不可少，移除任一组件均导致性能显著下降。
- UNCHA使双曲嵌入中部分和整体分布分离更明显，部分更靠近原点，而整体更远，形成更合理的层次结构。
---

# Uncertainty-guided Compositional Alignment with Part-to-Whole Semantic Representativeness in Hyperbolic Vision-Language Models

> [!tip] 核心洞察
> 在双曲空间中，嵌入点到原点的距离（双曲半径）可反映概念的抽象性或不确定性，更靠近原点的部分具有更高的不确定性（即对整体代表性低）；利用这一特性设计不确定性引导的对比损失和蕴含损失，可使模型更精确地捕捉部分-整体层次结构，提升组合理解能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超曲面视觉语言模型中不确定性引导的部分到整体语义代表性组合对齐 |
| 英文题名 | Uncertainty-guided Compositional Alignment with Part-to-Whole Semantic Representativeness in Hyperbolic Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22042) · [Code](https://github.com/jeeit17/UNCHA.git) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UNCHA (UNcertainty-guided Compositional Hyperbolic Alignment) |
| Dataset | ImageNet 零样本分类, VOC 多标签分类, COCO 多标签分类 |

> [!tip] 效果简介
> - ImageNet 零样本分类 上，Top-1 准确率 48.8 (ViT-B/16) vs HyCoCLIP 45.8 (ViT-B/16) (+3.0)。
> - ImageNet 零样本检索 上，R@1 48.8 (ViT-B/16) vs CLIP 40.6 (ViT-B/16)。
> - VOC 多标签分类 上，mAP 82.14 vs 最佳基线 80.50 (约)。

## 概要

现有双曲视觉语言模型（VLMs）在建模部分与整体之间的语义关系时，通常假设所有局部区域对整体场景的语义贡献是等同的。然而，这一假设与实际情况存在显著偏差：不同局部图像对整体场景的代表性存在天然差异（Figure 1）。**MERU**（Desai et al., ICML 2023）首次将图文蕴含关系引入双曲空间，但其仅关注跨模态的整体-整体对齐；**HyCoCLIP**（Pal et al., ICLR 2024）进一步引入了模态内的部分-整体蕴含，但仍未区分各部分对整体的差异化语义贡献。这一瓶颈导致部分-整体关系建模不够精确，双曲嵌入空间的层次表达能力未被充分利用。

针对上述问题，本文提出 **UNCHA**（UNcertainty-guided Compositional Hyperbolic Alignment），其核心思路是：**利用双曲空间中的嵌入半径来量化部分到整体的语义代表性，并将该不确定性自适应地融入对比损失与蕴含损失中**。具体而言，UNCHA 首先通过双曲半径的平滑单调变换为每个部分嵌入赋予一个不确定性度量 $u(\mathbf{x}) = \log(1 + \exp(-\|\mathbf{x}\|_2))$——更靠近双曲原点的部分具有更高的不确定性，即对整体场景的代表性更低。该不确定性随后被用于两个关键机制：（1）**不确定性引导的对比损失**，根据各部分的不确定性自适应缩放全局-局部对比损失的温度，使高代表性部分在对比学习中贡献更大的梯度；（2）**不确定性校准的蕴含损失**，在改进的连续蕴含损失基础上引入不确定性校准项与熵正则化，防止不确定性分布退化为均匀分布，从而更精细地刻画部分-整体的层次蕴含关系。

实验表明，UNCHA 在零样本图像分类、检索、层次分类、多对象表示及多标签分类等任务上均一致优于先前方法。例如，在 ImageNet 零样本分类中，UNCHA（ViT-B/16）达到 48.8% Top-1 准确率，较 HyCoCLIP 提升 **+3.0** 个百分点。消融研究进一步证实，不确定性引导的对比损失、不确定性校准与熵正则化三个组件均不可或缺，移除任一组件均导致性能显著下降。此外，对双曲嵌入分布的可视化分析显示，UNCHA 使部分嵌入与整体嵌入在双曲空间中形成更明显的层次分离，部分更靠近原点而整体更远，印证了方法对双曲空间利用效率的提升。

视觉语言模型（VLMs）在图像文本对齐任务上取得了显著进展，以 **CLIP**（Radford et al., ICML 2021）为代表的欧氏空间方法通过大规模对比学习实现了强大的零样本泛化能力。然而，欧氏嵌入空间在建模概念间的层次结构和部分-整体关系方面存在天然局限：欧氏空间无法有效表征“部分蕴含于整体”的非对称语义依赖，而这正是组合理解的核心。

为突破这一限制，研究者将目光投向具有负曲率的双曲空间。双曲几何的树状特性使其天然适合编码层次关系，部分嵌入可被约束在整体嵌入的“蕴含锥”内，从而显式建模部分-整体的蕴含结构。**MERU**（Desai et al., ICML 2023）首次将双曲空间引入VLMs，建立了跨模态的图文蕴含关系；**HyCoCLIP**（Pal et al., ICLR 2024）进一步扩展至模态内的部分-整体蕴含，使图像局部与全局场景、文本片段与完整描述之间的层次依赖得以建模。**ATMG**（Ramasinghe et al., CVPR 2024）则从角度对齐的角度改进了双曲VLMs的训练。

### 现有方法的根本瓶颈

尽管上述方法在双曲空间中对齐了部分与整体，但它们隐含了一个关键假设：**所有局部图像（或文本片段）对整体场景的语义贡献是等同的**。这一假设与视觉场景的真实构成严重不符——在任意场景中，不同局部区域对整体语义的代表性差异巨大：主体对象区域对场景理解至关重要，而背景、模糊或遮挡区域则贡献微弱甚至引入噪声。

现有双曲VLMs在建模部分-整体蕴含时，对所有部分施加统一的约束强度，导致两个直接后果：

1. **语义噪声被等权放大**：低代表性的部分（如无关背景块）与高代表性部分（如核心物体）在蕴含损失和对比损失中享有相同的权重，使模型被迫将噪声也“蕴含”进整体表示，污染了嵌入空间的结构。
2. **嵌入空间利用低效**：由于缺乏对部分差异化的建模信号，部分嵌入和整体嵌入的分布趋于重叠，未能形成清晰的层次分离，双曲空间的容量优势未被充分发挥。

### 核心动机与直觉

本文的核心洞察在于：**双曲空间中嵌入点到原点的距离（双曲半径）天然蕴含了概念的抽象性或不确定性信息**。在洛伦兹模型中，更靠近原点的点具有更高的“温度”或不确定性，这一几何特性恰好可用于量化部分到整体的语义代表性——语义上更模糊、与整体关联更弱的局部区域，其嵌入应更接近原点（高不确定性）；反之，与整体高度相关的部分则应远离原点（低不确定性）。

基于这一直觉，本文提出 **UNCHA（Uncertainty-guided Compositional Hyperbolic Alignment）**，旨在通过双曲不确定性显式建模部分到整体的语义代表性差异，并将这种不确定性自适应地融入对比损失和蕴含损失中，从而实现更精确的部分-整体层次对齐。UNCHA不改变基础编码器架构，而是通过损失函数层面的创新，使模型学会区分不同部分的贡献强度，最终在嵌入空间中形成部分靠近原点、整体远离原点的清晰层次结构。

## 核心方法与创新机理

UNCHA 的核心创新在于**首次将双曲不确定性显式建模为部分到整体的语义代表性度量**，并将其同时注入对比学习与蕴含推理两条路径，从而突破了现有双曲视觉语言模型（VLMs）对“所有部分对整体贡献均等”的隐含假设。

### 瓶颈洞察：部分代表性差异被忽视

现有双曲 VLMs（如 **MERU** (Desai et al., ICML 2023)、**HyCoCLIP** (Pal et al., ICLR 2024)）虽然利用双曲空间的层次偏置来建模部分-整体蕴含关系，但它们隐含地假设所有局部图像块对整体场景的语义贡献相同。然而，实际场景中不同部分对整体的代表性差异显著——语义相关的部分（如“狗的脸”）应强关联于整体（“狗”），而背景或遮挡部分则关联微弱。这一差异在先前工作中未被显式建模，导致部分-整体对齐不精确，双曲嵌入空间利用效率受限。

### 因果旋钮：双曲半径作为不确定性代理

UNCHA 的核心洞察在于：**在双曲空间中，嵌入点到原点的距离（双曲半径）可自然地反映概念的抽象性或不确定性**。更靠近原点的嵌入具有更大的蕴含锥孔径，对应更宽泛、更不确定的语义；而远离原点的嵌入则更具体、更确定。基于这一几何特性，UNCHA 定义了一个平滑的不确定性度量：

$$u(\mathbf{x}) = \log(1 + \exp(-\|\mathbf{x}\|_2))$$

该度量将双曲半径映射为 [0, 1) 区间的不确定性值：半径越小（靠近原点），不确定性越高，表示该部分对整体的语义代表性越低。实验验证了这一设计的有效性——在 ImageNet 子集上，部分到整体的语义相似度与不确定性之间呈现强负相关（r = -0.739），证实不确定性确实捕获了语义代表性。

### 创新槽位一：不确定性引导的对比损失

**Baseline**：现有方法（MERU、HyCoCLIP）在全局-局部对比损失中使用固定温度 $\tau$，对所有部分图像/文本一视同仁。

**UNCHA 的改进**：将估计的不确定性自适应地融入对比损失的温度缩放中：

$$\tau_{\mathrm{un}, i}^{I} = \exp(u(\mathbf{i}_i^{\mathrm{part}}) / 2) \tau_{gl}, \quad \tau_{\mathrm{un}, i}^{T} = \exp(u(\mathbf{t}_i^{\mathrm{part}}) / 2) \tau_{gl}$$

其机制是：**高不确定性（低代表性）的部分获得更大的温度值，从而在对比损失中被“软化”，降低其对整体对齐的贡献强度**；反之，低不确定性的代表性部分则获得更小的温度，被“锐化”以加强对齐信号。这一设计使模型能够自动区分不同部分的语义重要性，避免了无关部分对全局表征的干扰。

### 创新槽位二：不确定性校准的蕴含损失

**Baseline**：原始蕴含损失仅包含最大边际项 $\max(0, \phi - \eta\omega)$，要求部分嵌入严格落入整体嵌入的蕴含锥内，且对所有部分施加相同的几何约束。

**UNCHA 的改进**包含三个递进层次：

1. **连续角松弛**：在原始最大边际项基础上增加角项 $\alpha\phi(\mathbf{p}, \mathbf{q})$，形成 Leaky-ReLU 式的连续损失：
   $$L_{\mathrm{ent}}^{*}(\mathbf{p}, \mathbf{q}) = \max(0, \phi(\mathbf{p}, \mathbf{q}) - \eta\omega(\mathbf{p})) + \alpha\phi(\mathbf{p}, \mathbf{q})$$
   这使得即使部分嵌入已满足蕴含约束（锥内），仍保留梯度以鼓励更精细的对齐，同时保持优化连续性。

2. **不确定性校准**：将不确定性显式引入蕴含损失：
   $$L_{\mathrm{ent}}^{\mathrm{cal}}(\mathbf{p}, \mathbf{q}) = \lfloor L_{\mathrm{ent}}^{*}(\mathbf{p}, \mathbf{q})\rfloor e^{-u(\mathbf{p})} + u(\mathbf{p}) + \mathcal{H}(\tilde{u}(\mathbf{p}))$$
   其中 $\lfloor\cdot\rfloor$ 表示停止梯度。核心机制是：**高不确定性的部分，其蕴含损失被指数衰减 $e^{-u(\mathbf{p})}$ 削弱，同时 $u(\mathbf{p})$ 项鼓励模型降低不确定性**。这形成了一种自校准循环——模型既要满足蕴含约束，又要主动降低自身的不确定性。

3. **熵正则化**：对不确定性分布施加熵约束 $\mathcal{H}(\tilde{u}(\mathbf{p}))$，防止所有部分退化为相同的均匀不确定性，确保嵌入空间在不同不确定性水平上得到均衡利用。

### 方法谱系与知识库定位

UNCHA 处于双曲表示学习与视觉语言对齐的交叉点，其方法谱系可追溯为：

- **CLIP** (Radford et al., ICML 2021)：欧氏空间中的全局对比学习基线，缺乏层次建模能力。
- **MERU** (Desai et al., ICML 2023)：首次将图文对齐引入双曲空间，提出跨模态蕴含损失，但仅建模全局图像-文本蕴含。
- **HyCoCLIP** (Pal et al., ICLR 2024)：扩展 MERU，增加模态内部分-整体蕴含，但仍假设所有部分贡献均等。
- **ATMG** (Ramasinghe et al., CVPR 2024)：基于角度的双曲对齐方法，未涉及不确定性建模。
- **UNCHA**（本方法）：在 HyCoCLIP 的基础上，**首次引入不确定性引导的自适应加权机制**，将双曲半径的几何意义转化为语义代表性度量，同时改造对比损失和蕴含损失，形成统一的不确定性感知框架。

消融实验（Table 4）严格验证了每个创新槽位的必要性：移除不确定性感知对比损失（w/o contrastive）、移除不确定性校准（w/o uncertainty，Geeeer 分类从 68.98 降至 64.57）、移除熵正则化（w/o entropy）均导致一致的性能下降，证明三个组件相互补充、缺一不可。

UNCHA（**UN**certainty-guided **C**ompositional **H**yperbolic **A**lignment）的整体框架围绕一个核心洞察构建：在双曲空间中，部分图像/文本对整体场景的语义代表性存在显著差异，而这种差异可以通过双曲半径自然量化。如图 2 所示，与先前方法 MERU（Desai et al., ICML 2023）仅建模跨模态整体蕴含、HyCoCLIP（Pal et al., ICLR 2024）进一步引入模态内部分-整体蕴含不同，UNCHA 新增了一条不确定性感知路径，使模型能够自适应地调节各部分对整体对齐的贡献强度。

### 输入与特征提取

框架接受图文对作为输入。视觉侧采用 ViT 编码器提取整体图像特征 $\mathbf{i}$ 和局部图像特征 $\mathbf{i}^{\text{part}}$，文本侧采用 Transformer 编码器提取整体文本特征 $\mathbf{t}$ 和局部文本特征 $\mathbf{t}^{\text{part}}$。所有特征随后通过指数映射投影到洛伦兹流形 $\mathbb{L}^n$ 上，在双曲空间中完成后续的对齐与层次建模。

### 不确定性估计模块

不确定性估计器是整个框架的关键组件。对于任意双曲嵌入 $\mathbf{x}$，其不确定性定义为基于双曲半径的平滑单调变换：

$$u(\mathbf{x}) = \log(1 + \exp(-\|\mathbf{x}\|_2))$$

该设计的直觉在于：双曲空间中嵌入点到原点的距离（双曲半径）反映了概念的抽象性或不确定性——更靠近原点的部分具有更高的不确定性，即对整体场景的代表性更低。图 4 的实验验证了这一设计的合理性：部分到整体的语义相似度与不确定性之间存在强负相关（r = -0.739），语义代表性越高的部分，其不确定性越低。

### 不确定性引导的对比损失模块

该模块接收不确定性估计器的输出，对全局-局部对比损失进行逐元素温度缩放。具体而言，对于每个部分图像嵌入 $\mathbf{i}_i^{\text{part}}$ 和部分文本嵌入 $\mathbf{t}_i^{\text{part}}$，其对应的温度被自适应调节：

$$\tau_{\text{un},i}^{I} = \exp\left(u(\mathbf{i}_i^{\text{part}})/2\right) \tau_{gl}, \quad \tau_{\text{un},i}^{T} = \exp\left(u(\mathbf{t}_i^{\text{part}})/2\right) \tau_{gl}$$

高不确定性的部分获得更大的温度值，在对比损失中的梯度贡献被削弱；低不确定性的代表性部分则获得更小的温度，被赋予更高的对齐权重。完整的对比损失 $\mathcal{L}_{\text{con}}^{\text{un}}$ 由三部分组成：不确定性引导的全局-局部对比项、标准全局对比项和局部对比项（见 Eq. 11）。

### 不确定性校准的蕴含损失模块

该模块对传统的蕴含损失进行了两项关键改进。首先，引入角项 $\alpha\phi(\mathbf{p}, \mathbf{q})$ 形成 Leaky-ReLU 式松弛（Eq. 14），使嵌入在蕴含锥外时仍保留梯度信号，实现平滑优化。其次，添加不确定性校准项：

$$L_{\text{ent}}^{\text{cal}}(\mathbf{p}, \mathbf{q}) = \lfloor L_{\text{ent}}^{*}(\mathbf{p}, \mathbf{q})\rfloor e^{-u(\mathbf{p})} + u(\mathbf{p}) + \mathcal{H}(\tilde{u}(\mathbf{p}))$$

其中 $\mathcal{H}(\tilde{u}(\mathbf{p}))$ 为熵正则项（Eq. 16），对不确定性分布施加约束，防止其退化为均匀分布，确保双曲嵌入空间在不同不确定性水平和模态间得到均衡利用。

### 联合优化

最终训练目标将两个核心模块的输出进行加权组合：

$$L = \mathcal{L}_{\text{con}}^{\text{un}} + \lambda_{ent} \mathcal{L}_{\text{ent}}^{\text{un}}$$

其中 $\mathcal{L}_{\text{ent}}^{\text{un}}$ 整合了跨模态蕴含、模态内蕴含以及不确定性校准项（Eq. 17）。整个框架通过端到端训练，使模型在保持图文语义对齐的同时，精确捕捉部分到整体的层次结构。图 5 显示，UNCHA 的嵌入分布相比 HyCoCLIP 更加分散且层次分离更明显，验证了框架对双曲空间的高效利用。

### 3.1 双曲几何基础：洛伦兹模型

UNCHA 建立在洛伦兹双曲空间之上。给定曲率 $-\kappa$（$\kappa > 0$），$n$ 维洛伦兹流形定义为：

$$\mathbb{L}^{n} = \left\{ \mathbf{p} \in \mathbb{R}^{n+1} \mid \langle \mathbf{p}, \mathbf{p} \rangle_{\mathbb{L}} = -\frac{1}{\kappa}, \kappa > 0 \right\}$$

其中洛伦兹内积为：

$$\langle \mathbf{p}, \mathbf{q} \rangle_{\mathbb{L}} = -p_{\mathrm{time}} q_{\mathrm{time}} + \langle \mathbf{p}_{\mathrm{space}}, \mathbf{q}_{\mathrm{space}} \rangle$$

流形上两点间的测地距离由下式给出：

$$d_{\mathbb{L}}(\mathbf{p}, \mathbf{q}) = \sqrt{1/\kappa} \cosh^{-1}\left(-\kappa \langle \mathbf{p}, \mathbf{q} \rangle_{\mathbb{L}}\right)$$

在双曲空间中，嵌入点到原点的距离（双曲半径）天然反映了概念的抽象层级：更靠近原点的点对应更抽象、更不确定的概念。UNCHA 正是利用这一几何特性，将部分到整体的语义代表性建模为不确定性。

### 3.2 不确定性估计器

给定任意嵌入 $\mathbf{x}$（可以是图像部分 $\mathbf{i}^{\mathrm{part}}$、文本部分 $\mathbf{t}^{\mathrm{part}}$ 或整体表示），其不确定性定义为双曲半径的平滑单调变换：

$$u(\mathbf{x}) = \log\left(1 + \exp\left(-\|\mathbf{x}\|_2\right)\right)$$

**变量含义**：$\|\mathbf{x}\|_2$ 越大（嵌入越远离原点），$u(\mathbf{x})$ 越小，表示该部分对整体的语义代表性越高；反之，$\|\mathbf{x}\|_2$ 越小（嵌入越靠近原点），$u(\mathbf{x})$ 越大，表示该部分代表性越低。

这一设计的有效性得到了实证验证：在 ImageNet 子集上，部分到整体的语义相似度与不确定性之间呈现强负相关（$r = -0.739$），即语义代表性越高的部分，其不确定性越低（见 Figure 4）。

![[assets/figures/papers/paper_list_l796_https_arxiv_org_abs_2603_22042/figures/004_Figure_4.jpg]]
*Figure 4: Analysis of uncertainty modeling. (a) Randomly cropped parts are sorted by uncertainty (low→high). Semantically representative parts show low uncertainty, while blurred or less representative crops show high uncertainty. (b) On an ImageNet [56] subset, part-to-whole similarity vs. uncertainty shows a strong negative correlation*

### 3.3 不确定性引导的对比损失模块

UNCHA 的对比损失由三部分组成：全局对比损失、局部对比损失，以及核心的**不确定性引导的全局-局部对比损失**。

基础对比损失采用基于洛伦兹测地距离的 InfoNCE 形式（以图像到文本方向为例）：

$$L_c^{*}(\mathbf{i}, \mathbf{t}; \tau) = -\sum_i \log \frac{\exp\left(-d_{\mathbb{L}}(\mathbf{i}_i, \mathbf{t}_i)/\tau\right)}{\sum_{k \neq i} \exp\left(-d_{\mathbb{L}}(\mathbf{i}_i, \mathbf{t}_k)/\tau\right)}$$

**关键创新**在于全局-局部对比损失的温度参数不再固定，而是根据部分嵌入的不确定性进行自适应缩放：

$$\tau_{\mathrm{un}, i}^{I} = \exp\left(u(\mathbf{i}_i^{\mathrm{part}})/2\right) \tau_{gl}, \quad \tau_{\mathrm{un}, i}^{T} = \exp\left(u(\mathbf{t}_i^{\mathrm{part}})/2\right) \tau_{gl}$$

**机制解释**：当某个部分图像或文本的不确定性 $u$ 较高时，$\exp(u/2)$ 增大，对应的温度 $\tau_{\mathrm{un}}$ 升高，从而降低该部分在对比损失中的梯度贡献强度；反之，代表性高的部分获得更低的温度、更强的对齐信号。这一机制解决了“一个整体场景文本对应多个部分图像”时，部分图像代表性参差不齐导致的对齐噪声问题。

完整的**不确定性引导对比损失**为：

$$\mathcal{L}_{\mathrm{con}}^{\mathrm{un}} = \underbrace{L_c^{*}\left(\mathbf{i}^{\mathrm{part}}, \mathbf{t}; \tau_{\mathrm{un}}^{T}\right) + L_c^{*}\left(\mathbf{t}^{\mathrm{part}}, \mathbf{i}; \tau_{\mathrm{un}}^{I}\right)}_{\text{不确定性引导的全局-局部}} + \underbrace{L_c^{*}\left(\mathbf{i}, \mathbf{t}; \tau_g\right) + L_c^{*}\left(\mathbf{t}, \mathbf{i}; \tau_g\right)}_{\text{全局}} + \underbrace{L_c^{*}\left(\mathbf{i}^{\mathrm{part}}, \mathbf{t}^{\mathrm{part}}; \tau_l\right) + L_c^{*}\left(\mathbf{t}^{\mathrm{part}}, \mathbf{i}^{\mathrm{part}}; \tau_l\right)}_{\text{局部}}$$

### 3.4 不确定性校准的蕴含损失模块

双曲空间中，部分-整体关系通过**蕴含锥**建模：部分嵌入 $\mathbf{p}$ 定义了一个锥体，整体嵌入 $\mathbf{q}$ 应落入该锥内。锥体的孔径由下式给出：

$$\omega(\mathbf{p}) = \sin^{-1}\left(2K / \left(\sqrt{-\kappa} \|\mathbf{p}\|\right)\right)$$

其中 $\phi(\mathbf{p}, \mathbf{q})$ 为 $\mathbf{p}$ 与 $\mathbf{q}$ 间的测地角，用于判断 $\mathbf{q}$ 是否在 $\mathbf{p}$ 的蕴含区域内（见 Figure 3）。

![[assets/figures/papers/paper_list_l796_https_arxiv_org_abs_2603_22042/figures/003_Figure_3.jpg]]
*Figure 3: Entailment geometry in hyperbolic space. The term*

**原始蕴含损失**仅包含最大边际项：

$$\mathcal{L}_{\mathrm{orig}} = \max\left(0, \phi(\mathbf{p}, \mathbf{q}) - \eta \omega(\mathbf{p})\right)$$

UNCHA 将其改进为带连续角项的 **Leaky-ReLU 式蕴含损失**：

$$L_{\mathrm{ent}}^{*}(\mathbf{p}, \mathbf{q}) = \max\left(0, \phi(\mathbf{p}, \mathbf{q}) - \eta \omega(\mathbf{p})\right) + \alpha \phi(\mathbf{p}, \mathbf{q})$$

**改进动机**：原始形式在 $\mathbf{q}$ 已落入锥内时梯度为零，无法进一步优化细粒度对齐。添加角项 $\alpha \phi(\mathbf{p}, \mathbf{q})$ 后，即便满足蕴含约束，仍保留梯度以推动更紧密的语义对齐。

在此基础上，UNCHA 进一步引入**不确定性校准**：

$$L_{\mathrm{ent}}^{\mathrm{cal}}(\mathbf{p}, \mathbf{q}) = \left\lfloor L_{\mathrm{ent}}^{*}(\mathbf{p}, \mathbf{q}) \right\rfloor e^{-u(\mathbf{p})} + u(\mathbf{p}) + \mathcal{H}(\tilde{u}(\mathbf{p}))$$

**三项含义**：
- **$\lfloor L_{\mathrm{ent}}^{*} \rfloor e^{-u}$**：对蕴含损失进行 stop-gradient 后，用不确定性加权。低不确定性（高代表性）的部分获得更大的蕴含校准强度。
- **$u(\mathbf{p})$**：直接最小化不确定性，鼓励部分嵌入向更具代表性的方向优化。
- **$\mathcal{H}(\tilde{u}(\mathbf{p}))$**：熵正则项，防止不确定性分布退化为均匀分布：

$$\mathcal{H}(\tilde{u}(\mathbf{p})) = -\sum_i \tilde{u}(\mathbf{p}_i) \log(\tilde{u}(\mathbf{p}_i))$$

完整的**不确定性校准蕴含损失**整合了跨模态和模态内的蕴含约束：

$$\mathcal{L}_{\mathrm{ent}}^{\mathrm{un}} = \underbrace{L_{\mathrm{ent}}^{*}(\mathbf{t}^{\mathrm{part}}, \mathbf{i}^{\mathrm{part}}) + L_{\mathrm{ent}}^{*}(\mathbf{t}, \mathbf{i})}_{\text{跨模态蕴含}} + \lambda_1 \underbrace{\left(L_{\mathrm{ent}}^{*}(\mathbf{t}^{\mathrm{part}}, \mathbf{t}) + L_{\mathrm{ent}}^{*}(\mathbf{i}^{\mathrm{part}}, \mathbf{i})\right)}_{\text{模态内蕴含}} + \lambda_2 \underbrace{\left(L_{\mathrm{ent}}^{\mathrm{cal}}(\mathbf{t}^{\mathrm{part}}, \mathbf{t}) + L_{\mathrm{ent}}^{\mathrm{cal}}(\mathbf{i}^{\mathrm{part}}, \mathbf{i})\right)}_{\text{不确定性校准}}$$

### 3.5 训练目标

最终总损失为不确定性引导对比损失与不确定性校准蕴含损失的加权和：

$$L = \mathcal{L}_{\mathrm{con}}^{\mathrm{un}} + \lambda_{ent} \mathcal{L}_{\mathrm{ent}}^{\mathrm{un}}$$

其中 $\lambda_{ent}$ 为平衡两项损失的超参数。联合优化使模型在对比对齐中自适应调节各部分贡献，同时通过蕴含约束和不确定性校准精确捕捉部分-整体的层次结构。

## 实验与关键发现

### 零样本图像分类

Table 1 报告了 UNCHA 在 16 个零样本图像分类数据集上的 Top-1 准确率。以 ViT-B/16 为视觉骨干时，UNCHA 在 ImageNet 上达到 48.8%，相较最强双曲基线 **HyCoCLIP**（Pal et al., ICLR 2024）的 45.8% 提升 3.0 个百分点，且在所有数据集上一致优于 **MERU**（Desai et al., ICML 2023）和 **ATMG**（Ramasinghe et al., CVPR 2024）。ViT-S/16 架构下同样保持领先，验证了不确定性引导的组合对齐对类别级语义判别能力的增强效果。

![[assets/figures/papers/paper_list_l796_https_arxiv_org_abs_2603_22042/figures/005_Table_1.jpg]]
*Table 1: Zero-shot image classification evaluation. UNCHA (Ours) consistently demonstrates strong zero-shot classification performance across both architectures. Bold numbers denote the best performance within each architecture. † denotes ATMG trained on the GRIT [51]*

### 零样本检索与层次分类

Table 2 汇总了 ImageNet 上的零样本检索（R@1）和层次分类指标。UNCHA 在检索任务上显著超越欧氏空间基线 **CLIP**（Radford et al., ICML 2021）和此前最优的双曲方法，表明不确定性引导的对比损失有效提升了跨模态对齐精度。层次分类指标上的优势则说明，不确定性校准的蕴含损失使双曲嵌入更好地保留了部分-整体的层级结构。

### 部分级别对齐与难负样本

Table 3 展示了带难负样本的部分级别对齐评测。在最具挑战性的“All Pick5”和“All-Hard Negative”设置下，UNCHA 相较先前方法取得显著增益，证明模型对细粒度组合语义的理解能力更强——不确定性机制使模型能够区分代表性高低不同的部分，避免非代表性局部对整体对齐产生噪声干扰。

![[assets/figures/papers/paper_list_l796_https_arxiv_org_abs_2603_22042/figures/007_Table_3.jpg]]
*Table 3: Comparison on part-level alignment evaluation with hard negatives. Ours achieves substantial performance gains under the most challenging scenario of [63], demonstrating its strong ability for fine-grained compositional understanding*

### 多对象表示与多标签分类

Table 5 分别报告了 ComCo/SimCo 多对象配置下的零样本 mAP 以及 VOC/COCO 多标签分类的 mAP。UNCHA 在不同对象数量设定下均优于所有基线（VOC 上 mAP 达 82.14，COCO 上达 59.43），说明不确定性引导的部分-整体对齐在复杂多对象场景中同样鲁棒，能够更准确地建模多个局部与整体场景之间的语义关系。

![[assets/figures/papers/paper_list_l796_https_arxiv_org_abs_2603_22042/figures/009_Table_5.jpg]]
*Table 5: Comparison across Multi-object Representation and Classification tasks. Left: zero-shot mAP comparison across multiobject configurations on ComCo and SimCo datasets. Right: zero-shot multi-label classification (Cls.) on VOC and COCO datasets (mAP only). Our method consistently achieves higher mAP across both tasks*

### 消融实验

Table 4 的系统消融揭示了各组件的独立贡献：

- **移除不确定性引导的对比损失（w/o contrastive）**：分类和检索性能均明显下降，验证了基于不确定性自适应缩放全局-局部对比温度的必要性。
- **移除不确定性校准（w/o uncertainty）**：分类基准 Geeeer 从完整的 68.98 骤降至 64.57，表明蕴含损失中的不确定性校准项对层次关系建模至关重要。
- **移除熵正则化（w/o entropy）**：嵌入空间利用效率降低，性能同步退化，说明熵约束有效防止了不确定性分布退化为均匀分布，保障了双曲空间的结构化利用。

### 不确定性建模的语义验证

Figure 4 从实证角度验证了不确定性度量的语义合理性：(a) 随机裁剪的部分图像按不确定性升序排列，语义代表性强的裁剪（包含核心物体）呈现低不确定性，而模糊或无关裁剪呈现高不确定性；(b) 在 ImageNet 子集上，部分到整体的语义相似度与不确定性之间呈现强负相关（r = -0.739），直接支持了“双曲半径编码语义代表性”的核心假设。

### 双曲嵌入空间分析

Figure 5 对比了 UNCHA 与 HyCoCLIP 的双曲嵌入分布。HyCoCLIP 的嵌入聚集在较窄范围内，而 UNCHA 的嵌入分布更为分散，部分嵌入更靠近原点（高不确定性），整体嵌入更远离原点（低不确定性），形成了更清晰的层次分离。这一结构化分布印证了不确定性校准损失和熵正则化对双曲空间利用效率的改善。

### 补充实验

补充材料中的 Table S.6 进一步消融了双曲半径的计算方式：将本文使用的欧氏范数代理替换为显式双曲半径后，分类和检索性能均轻微下降，表明当前的不确定性定义在数值稳定性和优化特性上具有实用优势。Table S.9 和 Table S.10 分别报告了零样本分割（VOC21 mIoU）和框级别分类（COCO/LVIS/OpenImages Top-1/Top-5）的结果，UNCHA 在所有设置下一致超越先前方法，进一步验证了方法的泛化能力。

![[assets/figures/papers/paper_list_l796_https_arxiv_org_abs_2603_22042/figures/011_Table_S.6.jpg]]
*Table S.6: Ablation study on hyperbolic radius. Replacing our Euclidean-norm surrogate with the explicit hyperbolic radius slightly degrades both classification and retrieval performance. Bold numbers indicate the best within each task group*

## 定位与知识库关联

### 1. 与基线方法的关系

UNCHA 建立在双曲视觉语言模型（VLMs）的演进脉络之上，其核心改进直指现有方法在部分-整体关系建模中的“等权假设”瓶颈。

**CLIP**（Radford et al., ICML 2021）作为欧氏空间基线，通过全局对比学习建立了图文对齐的范式，但欧氏空间的平坦几何无法自然编码概念间的层次蕴含关系。**MERU**（Desai et al., ICML 2023）首次将双曲空间引入 VLMs，利用洛伦兹流形的负曲率特性建模跨模态的图文蕴含（image-text entailment），使整体场景嵌入自然地“包含”其组成部分。然而，MERU 仅处理了跨模态的全局蕴含，未涉及模态内部的部分-整体层次结构。

**HyCoCLIP**（Pal et al., ICLR 2024）在此基础上向前推进了一步：它在 MERU 的跨模态蕴含之外，额外引入了模态内的部分-整体蕴含损失（intra-modal entailment），迫使部分图像嵌入落入整体图像嵌入的蕴含锥内，部分文本嵌入落入整体文本嵌入的蕴含锥内。这一扩展使得双曲 VLMs 首次具备了显式的组合层次建模能力。但 HyCoCLIP 的关键缺陷在于：**它假设所有部分对整体的语义贡献是均等的**——无论是高度相关的核心物体区域，还是模糊的背景碎片，在对比损失和蕴含损失中都被赋予相同的权重。这种“一刀切”的处理方式导致：（1）低代表性部分产生的噪声信号污染了嵌入空间；（2）双曲空间的层次编码潜力未被充分利用。

**UNCHA 的突破点**在于引入“语义代表性”这一维度。通过将双曲半径转化为不确定性度量 $u(\mathbf{x}) = \log(1 + \exp(-\|\mathbf{x}\|_2))$，UNCHA 为每个部分自适应地分配权重：语义代表性高的部分（低不确定性）在对比损失中获得更小的温度 $\tau_{\mathrm{un}}$，从而产生更强的梯度信号；代表性低的部分（高不确定性）则被“降温”处理，减少其对整体对齐的干扰。这一机制在对比损失层面（Eq. 11）和蕴含损失的不确定性校准项（Eq. 15）中同时生效，形成双重约束。

**ATMG**（Ramasinghe et al., CVPR 2024）则代表了双曲对齐的另一技术路线——基于角度的度量学习。与 UNCHA 基于距离和蕴含锥的方法不同，ATMG 侧重于角度空间的优化，但缺乏对部分-整体语义代表性的显式建模。

**方法演进总结**：

| 方法 | 对齐空间 | 跨模态蕴含 | 模态内部分-整体蕴含 | 部分语义代表性建模 |
|------|----------|------------|---------------------|---------------------|
| CLIP | 欧氏 | ✗ | ✗ | ✗ |
| MERU | 双曲 | ✓ | ✗ | ✗ |
| HyCoCLIP | 双曲 | ✓ | ✓ | ✗（等权假设） |
| ATMG | 双曲（角度） | ✓ | ✗ | ✗ |
| **UNCHA** | 双曲 | ✓ | ✓ | ✓（不确定性引导） |

### 2. 核心改进的因果机制

UNCHA 的三个关键修改槽位构成了一个因果闭环：

1. **不确定性引导的温度缩放**（Eq. 10）：将全局-局部对比损失中的固定温度 $\tau_{gl}$ 替换为逐样本自适应温度 $\tau_{\mathrm{un},i} = \exp(u/2) \cdot \tau_{gl}$。这一修改的因果逻辑是：高不确定性部分 → 大温度 → 对比损失梯度减小 → 模型不被低质量部分“带偏”。消融实验中移除该组件（w/o contrastive）导致分类和检索性能显著下降，验证了这一因果链。

2. **蕴含损失的结构性增强**（Eq. 14）：在原始的最大边际项 $\max(0, \phi - \eta\omega)$ 基础上添加角项 $\alpha\phi$，形成 Leaky-ReLU 式松弛。其因果意图是：即使部分嵌入已落入整体嵌入的蕴含锥内（满足 $\phi < \eta\omega$），角项仍提供梯度信号，推动部分嵌入向锥中心进一步靠拢，实现更精细的层次对齐。

3. **不确定性校准与熵正则化**（Eq. 15-16）：将蕴含损失与不确定性耦合，通过 $\lfloor L_{\mathrm{ent}}^* \rfloor e^{-u} + u + \mathcal{H}(\tilde{u})$ 的形式，使得高不确定性部分的蕴含约束被放松（$e^{-u}$ 项衰减），同时熵正则化 $\mathcal{H}(\tilde{u})$ 防止不确定性分布退化为均匀分布，确保双曲嵌入空间在不同不确定性水平上被均衡利用。

### 3. 适用边界与局限

**适用场景**：
- 需要显式建模部分-整体层次结构的组合理解任务（如场景图解析、多对象关系推理）
- 零样本条件下需要区分不同局部区域对全局语义贡献差异的场景
- 双曲空间嵌入的自然适用领域（层次分类、蕴含推理）

**已知局限**（基于论文证据）：
- 论文未明确报告在极端低资源或域外分布（OOD）场景下的性能表现，该边界需手动验证。
- 不确定性估计的可靠性依赖于双曲半径与语义代表性的相关性（$r = -0.739$），这一相关性虽强但非完美，存在部分-整体语义相似但半径异常的边界案例。
- 方法在 ViT-S/16 和 ViT-B/16 两个架构上验证，更大规模模型（如 ViT-L）上的可扩展性尚未在证据中体现。

**开放问题**：
- 不确定性估计器 $u(\mathbf{x})$ 的单调变换形式是否为最优选择？是否存在更适合特定数据分布的非线性变换？
- 熵正则化系数 $\lambda_2$ 的敏感性如何？不同数据集间是否需要自适应调整？
- 该不确定性框架能否推广到视频时序片段对全局视频的代表性建模？

## 原文 PDF

![[paperPDFs/CVPR_2026/Uncertainty_guided_Compositional_Alignment_with_Part_to_Whole_Semantic_Representativeness_in_Hyperbolic_Vision_Language_Models.pdf]]
