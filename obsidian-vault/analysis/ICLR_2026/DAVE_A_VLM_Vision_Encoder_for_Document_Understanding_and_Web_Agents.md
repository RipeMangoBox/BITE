---
title: "DAVE: A VLM Vision Encoder for Document Understanding and Web Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DAVE_A_VLM_Vision_Encoder_for_Document_Understanding_and_Web_Agents.pdf
openreview_forum_id: kgk0NqjsoW
aliases:
- DAVE
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "提出DAVE（Document and web Agents Vision Encoder），通过两阶段预训练（自监督MAE学习结构和空间先验，监督自回归预训练学习解析和定位）、权重合并（多文本解码器预训练+蒸馏系数合并）和集成训练（融合通用编码器SigLIP2），创建专门针对文档/网页的视觉编码器，并兼容多种VLM架构。"
primary_logic: "从大量无标签文档和Web截图中通过自监督MAE获取低层结构和空间特征，同时集成通用编码器保留高层语义，并利用多解码器合并实现解码器无关性，从而在文档理解和Web代理任务上显著超越通用和专用编码器。"
claims:
- "DAVE在Llama-3.2-3B设置下，8个文档和Web基准上平均比SigLIP2提升10.5%。"
- "DAVE在文档分割（DocLayNet mAP 74.1）和文档识别（DocBank mAP 56.9）上全面超越基线。"
- "文档/网页图像具有极低的patch间方差，导致标准MAE训练发散，改用像素重建损失稳定训练。"
- "学习合并系数在Doc/Web基准上明显优于平均合并和Fisher合并。"
---

# DAVE: A VLM Vision Encoder for Document Understanding and Web Agents

> [!tip] 核心洞察
> 从大量无标签文档和Web截图中通过自监督MAE获取低层结构和空间特征，同时集成通用编码器保留高层语义，并利用多解码器合并实现解码器无关性，从而在文档理解和Web代理任务上显著超越通用和专用编码器。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DAVE：面向文档理解与网络代理的视觉语言模型视觉编码器 |
| 英文题名 | DAVE: A VLM Vision Encoder for Document Understanding and Web Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=kgk0NqjsoW); [GitHub](https://github.com/Brandon3964/DAVE) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | DAVE |
| Dataset | DocVQA (Llama-3.2-3B), OCRBench (Llama-3.2-3B), WebSRC (Llama-3.2-3B), Mind2Web Cross-Task Element Acc. (Llama-3.2-3B) |

> [!tip] 效果简介
> - DocVQA (Llama-3.2-3B) 上，Accuracy 为 82.1，对比 72.1 (SigLIP2)，变化 +10.0。
> - OCRBench (Llama-3.2-3B) 上，Accuracy 为 62.2，对比 51.5 (SigLIP2)，变化 +10.7。
> - WebSRC (Llama-3.2-3B) 上，Accuracy 为 82.6，对比 67.8 (SigLIP2)，变化 +14.8。

## 概述

**问题瓶颈**：现有视觉语言模型（VLM）依赖的通用视觉编码器（如 SigLIP2、DinoV2）虽能捕获高层语义，却缺乏文档、网页截图、图表等结构化图像所必需的低层结构与空间先验。这类图像具有极低的 patch 间方差，导致标准 MAE 训练发散，进一步加剧了底层特征表示能力的不足。

**核心方法**：DAVE（Document and web Agents Vision Encoder）通过两阶段预训练解决上述瓶颈：
1. **自监督阶段**：在 20M 无标签文档/网页图像上，采用修改后的直接像素重建损失（MAE-pixel）替代标准归一化损失，稳定地学习结构与空间先验。
2. **监督自回归阶段**：在约 2M 高质量标注数据上进行多任务训练（OCR、布局提取、Web 定位），同时通过**权重合并**（多文本解码器预训练 + 蒸馏学习合并系数）创建解码器无关的编码器，并通过**集成训练**冻结通用编码器 SigLIP2 并将其特征与专用编码器级联，保留高层语义。

**核心洞察**：从海量无标签文档/网页中通过自监督 MAE 获取低层结构特征，同时集成通用编码器保留高层语义，并利用多解码器合并实现解码器无关性，从而在文档理解和 Web 代理任务上显著超越通用和专用编码器。

**方法定位**：DAVE 属于**专用视觉编码器**，与通用编码器（DinoV2、SigLIP2、AIMv2）和文档专用模型（DiT、Pix2Struct、Dolphin）形成互补。其权重合并策略借鉴了 model soup（Wortsman et al., 2022）的思想，但通过蒸馏损失学习合并系数，实现了更优的特征对齐。

**主要结果**（Llama-3.2-3B 设置）：
- 8 个文档和 Web 基准上平均比 SigLIP2 提升 **10.5%**（Table 1）。
- WebSRC 准确率从 67.8 提升至 **82.6**（+14.8），OCRBench 从 51.5 提升至 **62.2**（+10.7）。
- 文档分割（DocLayNet mAP **74.1**）和文档识别（DocBank mAP **56.9**）全面超越基线（Table 3）。
- Web 代理任务 Mind2Web 上，元素准确率比最强基线 Dolphin 提升 **6.8%**（Table 2）。

**证据强度**：上述核心结论均有高置信度实验支撑（Table 1/2/3，置信度 0.95–0.99）。消融实验证实了像素重建损失的必要性（Figure 3/4）、学习合并系数的优势（Table 4a）以及集成通用编码器的贡献（Table 10）。

**局限与开放问题**：在语义重的任务（如 RICO-SCA 屏幕分类）上略低于 SigLIP2，可能与嵌入维度翻倍导致单层 MLP 预测头难以有效池化有关；训练成本较高（32 块 H200 GPU）；未针对任意分辨率和纵横比优化；Web 代理设置中未融入历史动作信息。

## 背景与动机

### 文档理解与Web代理的视觉编码瓶颈

视觉语言模型（VLM）在通用视觉问答和自然图像理解上取得了显著进展，但在文档理解与Web代理任务中仍面临根本性挑战。这类任务涉及对PDF、图表、用户界面截图和网页等结构化图像的理解，要求模型不仅识别图像中的文字和对象，还需精确感知其**空间位置、布局结构和层次关系**。然而，现有VLM广泛采用的视觉编码器（如SigLIP2、DinoV2）主要针对自然图像设计，其提取的特征表示在低层结构和空间信息方面存在天然缺陷。

这一瓶颈的根源在于：自然图像以纹理、颜色和语义内容为主导，而文档和Web图像则以稀疏的文本行、表格边框、UI组件和几何图形为核心。**现有通用编码器缺乏对这类结构化图像的归纳偏置**，导致VLM在文档布局分割、表格结构识别、Web元素定位等任务上表现不佳。

### 现有方法的局限

当前针对文档和Web任务的视觉编码方案可分为三类，各有明显短板：

- **通用编码器直接使用**：SigLIP2（Tschannen et al., 2025）、DinoV2（Oquab et al., 2023）等在大规模自然图像上预训练的编码器，虽具备丰富的高层语义表示，但缺乏对文档/Web图像中细粒度空间关系的建模能力。在DocVQA、WebSRC等基准上，这类编码器的VLM性能显著低于任务需求。

- **专用文档编码器**：DiT（Li et al., 2022a）等针对文档任务设计的编码器，在特定任务上有所改善，但通常与特定解码器强耦合，缺乏跨架构泛化能力。Pix2Struct（Lee et al., 2023）和Dolphin（Feng et al., 2025）等编码器-解码器模型虽在文档任务上表现较好，但无法灵活集成到不同的VLM架构中。

- **直接微调通用编码器**：在文档/Web数据上微调SigLIP2等通用编码器，由于自然图像与文档图像在统计特性上的本质差异（详见下文），训练过程不稳定，性能提升有限。

### 文档图像的低方差特性与训练挑战

DAVE研究揭示了一个此前未被充分认识的关键现象：**文档和Web图像的patch间标准差极低**（见Figure 3），远低于自然图像。标准MAE（Masked Autoencoder）采用按patch归一化的像素重建损失（Eq. 1）：

$$\mathcal{L}_{\mathrm{MAE}} = \frac{1}{|\mathcal{M}|} \sum_{i \in \mathcal{M}} \left\| f_{\theta}(\tilde{x})_i - \frac{x_i - \mu(x_i)}{\sqrt{\sigma^2(x_i) + \epsilon}} \right\|_2^2, \quad \epsilon = 10^{-6}$$

当patch内方差 $\sigma^2(x_i)$ 接近零时，归一化操作会放大数值噪声，导致训练发散（见Figure 4）。这一发现解释了为何直接在大规模文档图像上应用标准MAE训练无法获得有效的结构和空间先验。

### 本文动机与核心思路

针对上述瓶颈，DAVE提出以下核心动机：

1. **从无标签数据中学习结构和空间先验**：利用大量未标注的文档和Web截图，通过自监督学习获取低层特征表示，弥补通用编码器的不足。

2. **解码器无关的编码器设计**：通过多文本解码器联合预训练和权重合并策略，使视觉编码器不被特定语言模型绑定，实现跨VLM架构的即插即用。

3. **专用与通用特征的有机融合**：在保留通用编码器高层语义理解能力的同时，注入文档/Web专用的结构和空间特征，实现两类信息的互补。

这些动机驱动了DAVE的两阶段预训练框架：第一阶段在20M无标签图像上使用改进的MAE-pixel损失进行自监督训练；第二阶段在约2M高质量标注数据上进行监督自回归预训练，同时集成通用编码器特征并进行多解码器权重合并。

## 核心创新

### 根本瓶颈：通用视觉编码器缺乏文档与界面所需的结构和空间先验

当前视觉语言模型（VLM）普遍采用面向自然图像的通用视觉编码器（如 SigLIP2、DinoV2），这些编码器在文档理解与 Web 代理任务中暴露出一个核心缺陷：**低层特征对文档、UI 和图表等结构化图像的表示能力严重不足**。这类图像与自然图像存在本质差异——文档和网页截图的 patch 间方差极低（见 Figure 3），导致标准 MAE 的归一化像素损失训练发散（见 Figure 4），使得通用编码器难以习得精确的空间定位和结构解析能力。这一瓶颈直接制约了 VLM 在文档问答、Web 元素定位等下游任务上的性能上限。

### 创新杠杆：三管齐下的专用编码器构建范式

DAVE 通过三个相互协同的技术槽位，系统性地解决了上述瓶颈：

**槽位一：自监督训练目标的针对性修改**

标准 MAE 采用按 patch 归一化的 L2 重建损失（Eq. 1），在文档/网页图像上因方差过低导致训练不稳定。DAVE 将其替换为**直接像素重建损失** MAE-pixel（Eq. 2）：

$$\mathcal{L}_{\mathrm{MAE-pixel}} = \frac{1}{|\mathcal{M}|} \sum_{i \in \mathcal{M}} \| f_{\theta}(\tilde{x})_i - x_i \|_2^2$$

这一修改消除了归一化操作，在 20M 无标签文档和 Web 截图上稳定训练，使编码器从大规模无监督数据中获取了强结构和空间先验。

**槽位二：多解码器预训练与蒸馏式权重合并**

传统做法使用单一文本解码器训练编码器，导致编码器与该解码器强绑定，限制了跨 LLM 的泛化性。DAVE 提出**多文本解码器同时预训练**（Granite、Qwen、Phi 等），随后通过蒸馏损失学习合并系数 $\alpha_i^{(j)}$，将多个编码器权重加权求和：

$$\theta_{\mathrm{merge}}^{(j)} = \sum_{i=1}^{n} \alpha_i^{(j)} \theta_i^{(j)}, \quad \alpha_i^{(j)} \in [0,1]$$

蒸馏损失最小化合并编码器输出特征与各教师编码器特征之间的均方误差（Eq. 蒸馏损失），最终生成**解码器无关的视觉编码器**。消融实验（Table 4a）表明，学习合并系数在 Doc/Web 基准上明显优于平均合并和 Fisher 合并；合并的 LLM 数量越多，性能持续提升（Table 4b）。

**槽位三：通用编码器特征的集成融合**

专用编码器虽擅长结构和空间特征，但可能丢失高层语义信息。DAVE 将**冻结的通用编码器（SigLIP2）特征与专用编码器特征在通道维度级联**，进行集成训练。这一设计使编码器同时保留低层结构先验和高层语义表征，在 RICO-SCA 屏幕分类任务上准确率从 90.7 提升至 92.3（Table 10），验证了语义信息的有效补充。

### 关键证据链

上述三个创新槽位形成了完整的因果链条：**修改 MAE 目标 → 稳定学习结构/空间先验 → 多解码器合并 → 解码器无关性 → 集成通用特征 → 保留高层语义**。决定性证据来自 Table 1：在 Llama-3.2-3B 设置下，DAVE 在 8 个文档和 Web 基准上平均比 SigLIP2 提升 10.5%；在 Web 代理任务 Mind2Web 上，比最强基线 Dolphin 提升 6.8 个百分点的元素准确率（Table 2）。Figure 2 的消融轨迹进一步显示，逐步叠加自监督预训练、集成训练和权重合并，文档 VQA 性能单调递增，证实了各组件独立且协同的贡献。

### 与基线的本质差异

DAVE 并非简单组合现有编码器。与直接级联 SigLIP2 和其他专用编码器（如 SigLIP2+DiT、SigLIP2+Pix2Struct）相比，DAVE 的集成训练和合并策略在 Doc/Web 基准上具有显著优势（Table 4c）；与直接 finetune SigLIP2 相比，DAVE 的两阶段预训练范式也带来明显增益（Table 4d）。这表明 DAVE 的创新在于**训练范式的系统性重构**，而非简单的特征拼接。

## 整体框架

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/001_Figure_1.jpg]]
*Figure 1: DAVE Overview. Stage 1 trains the vision encoder with a decoder using MAE, learning strong structural and spatial priors from unlabeled data. Stage 2 performs autoregressive pretraining on diverse tasks with different text decoders and fuses the high-level semantic features from SigLIP 2. After that, different encoders are combined into a single one by learning a merge coefficient using unsupervised representation alignment, while keeping the encoders frozen*

DAVE 的整体设计围绕一个核心洞察展开：**文档与网页图像具有极低的 patch 间方差**（Figure 3），这使得标准 MAE 的归一化像素损失训练发散，而通用视觉编码器又缺乏此类结构化图像所需的低层空间与结构先验。为此，DAVE 构建了一个三阶段流水线，依次解决“稳定学习结构先验”、“融合高层语义并实现解码器无关”、“生成可嵌入任意 VLM 的最终编码器”三个子问题。

### 流水线总览

DAVE 的完整训练与推理流程如 Figure 1 所示，包含三个关键阶段：

1.  **阶段一：自监督 MAE 预训练（结构先验获取）**
    在 20M 无标签文档/网页图像上，使用修改后的 **MAE-pixel 损失** 训练 ViT 编码器-解码器。该阶段不依赖任何文本标注，目标是让编码器学会 patch 间的空间关系和局部结构特征。关键改动是将标准 MAE 的 patch 内归一化损失替换为直接像素重建损失，以解决文档/网页图像因大面积空白导致训练发散的问题。

2.  **阶段二：监督自回归预训练与集成训练（语义融合与多解码器适配）**
    在约 2M 高质量标注数据上进行多任务监督训练，任务涵盖 OCR、布局提取、图表解析和 Web 元素定位。此阶段同时引入两个关键机制：
    -   **集成训练**：冻结通用编码器 **SigLIP2**，将其输出特征与 DAVE 专用编码器特征在通道维度级联，再送入文本解码器（LLM）。这保留了 SigLIP2 的高层语义理解能力，同时注入 DAVE 的结构与空间特征。
    -   **多解码器预训练**：使用多个不同的 LLM（如 Granite、Qwen、Phi）作为文本解码器分别训练，得到多个与特定解码器绑定的编码器副本。

3.  **阶段三：权重合并（解码器无关化）**
    通过蒸馏学习一组可学习的合并系数 $\alpha_i^{(j)}$，将阶段二产出的多个编码器权重进行加权求和：
    $$\theta_{\mathrm{merge}}^{(j)} = \sum_{i=1}^{n} \alpha_i^{(j)} \theta_i^{(j)}, \quad \alpha_i^{(j)} \in [0,1]$$
    蒸馏损失最小化合并编码器的 patch 特征与各教师编码器特征之间的均方误差：
    $$\mathcal{L}_{\mathrm{distill}} = \frac{1}{n} \sum_{i=1}^{n} \| \hat{\mathbf{z}}_i - \mathbf{z}_i \|_2^2$$
    最终得到一个与具体 LLM 解耦的、可直接嵌入任意 VLM 的视觉编码器 $\phi_{\mathrm{DAVE}}^{\mathrm{final}}$。

### 关键模块关系与数据流

-   **编码器架构**：DAVE 编码器基于 ViT，在阶段一使用 MAE 解码器进行自监督重建；阶段二丢弃解码器，将编码器输出的 patch 特征与冻结的 SigLIP2 特征级联后，经投影层送入 LLM。
-   **损失函数演进**：阶段一使用 $\mathcal{L}_{\mathrm{MAE-pixel}}$（直接像素 L2 损失），阶段二使用标准自回归交叉熵损失，阶段三使用特征蒸馏 MSE 损失。
-   **数据流**：输入图像经 DAVE 编码器和 SigLIP2 分别提取特征 → 通道级联 → 线性投影 → 与文本 token 拼接 → LLM 自回归生成。在 Web 代理设置中，输入为网页截图与任务指令，输出为元素定位与动作预测。

### 设计决策的因果逻辑

整个框架的设计由一条因果链驱动：**低 patch 方差 → 修改 MAE 损失 → 获得稳定结构先验 → 集成通用编码器补偿语义 → 多解码器训练 + 权重合并实现解码器无关**。消融实验（Figure 2）验证了这一递进关系：从随机初始化文本解码器开始，逐步加入预训练 LLM、集成训练、权重合并，每个步骤都带来一致的性能提升。

## 核心模块与公式推导

### 模块一：自监督 MAE 预训练（Stage 1）

DAVE 的第一阶段在约 2000 万张无标签文档和网页截图图像上进行掩码自编码器（MAE）预训练，目标是让视觉编码器从大量无标注数据中习得低层结构和空间先验。然而，直接沿用标准 MAE 的训练目标会导致训练不稳定。

标准 MAE 使用的损失函数对每个 patch 进行局部归一化：

$$ \mathcal{L}_{\mathrm{MAE}} = \frac{1}{\left|\mathcal{M}\right|} \sum_{i \in \mathcal{M}} \left\| f_{\theta}(\tilde{x})_i - \frac{x_i - \mu(x_i)}{\sqrt{\sigma^2(x_i) + \epsilon}} \right\|_2^2, \quad \epsilon = 10^{-6} $$

其中 $\mathcal{M}$ 为被掩码的 patch 索引集合，$f_{\theta}(\tilde{x})_i$ 为编码器对掩码图像 $\tilde{x}$ 第 $i$ 个 patch 的重建输出，$x_i$ 为原始 patch 像素值，$\mu(x_i)$ 和 $\sigma^2(x_i)$ 分别为该 patch 的均值和方差。

**瓶颈分析**：文档和网页图像具有极低的 patch 间方差（见 Figure 3），这意味着归一化项 $\sigma^2(x_i)$ 趋近于零，导致损失函数在训练过程中发散（见 Figure 4 的训练曲线尖峰）。DAVE 将此归因于结构化图像中大面积纯色背景或重复纹理区域缺乏足够的局部统计变化。

**解决方案**：DAVE 将损失函数修改为直接像素重建损失，移除 patch 内归一化步骤：

$$ \mathcal{L}_{\mathrm{MAE-pixel}} = \frac{1}{|\mathcal{M}|} \sum_{i \in \mathcal{M}} \| f_{\theta}(\tilde{x})_i - x_i \|_2^2 $$

该修改的核心逻辑是：直接最小化重建像素与原始像素之间的均方误差，避免因低方差 patch 导致的数值不稳定。实验证据表明，这一改动使得在文档/网页数据上的 MAE 训练能够稳定收敛，且后续下游任务性能显著优于使用归一化损失的版本。

---

### 模块二：监督自回归预训练与集成特征融合（Stage 2）

第二阶段在约 200 万高质量标注数据上进行多任务监督训练，涵盖 OCR、布局提取、Web 元素定位等任务。该阶段包含两个关键设计：

**集成特征融合**：将冻结的通用视觉编码器（SigLIP2）的特征与 DAVE 专用编码器的特征在通道维度进行级联。设 $\phi_{\mathrm{gen}}$ 为冻结的通用编码器，$\phi_{\mathrm{spec}}$ 为 DAVE 专用编码器，则送入文本解码器的视觉特征为：

$$ \mathbf{z} = [\phi_{\mathrm{gen}}(x); \phi_{\mathrm{spec}}(x)] $$

这一设计的因果逻辑是：通用编码器保留了从大规模自然图像中习得的高层语义表示，而专用编码器通过 Stage 1 的 MAE 预训练获得了文档/网页特有的结构和空间特征，二者级联后形成互补表示。消融实验（Table 10）显示，集成 SigLIP2 特征后 RICO-SCA 屏幕分类准确率从 90.7 提升至 92.3，验证了高层语义的贡献。

---

### 模块三：权重合并蒸馏

监督预训练阶段使用多个不同的文本解码器（LLM）同时训练，产生多个与特定解码器绑定的编码器版本。为消除这种耦合，DAVE 采用基于蒸馏的权重合并方案。

**合并权重定义**：对于 $n$ 个编码器，其第 $j$ 层参数的合并权重通过可学习系数 $\alpha_i^{(j)}$ 加权求和得到：

$$ \theta_{\mathrm{merge}}^{(j)} = \sum_{i=1}^{n} \alpha_i^{(j)} \theta_i^{(j)}, \quad \alpha_i^{(j)} \in [0,1] $$

**蒸馏损失**：合并系数通过最小化合并编码器与各教师编码器输出特征之间的均方误差来学习：

$$ \mathcal{L}_{\mathrm{distill}} = \frac{1}{n} \sum_{i=1}^{n} \| \hat{\mathbf{z}}_i - \mathbf{z}_i \|_2^2 $$

其中 $\hat{\mathbf{z}}_i$ 为合并编码器对输入图像输出的 patch 特征，$\mathbf{z}_i$ 为第 $i$ 个教师编码器的对应输出。蒸馏过程在无标签文档和网页图像上进行 20 个 epoch，所有编码器参数保持冻结，仅优化合并系数 $\alpha_i^{(j)}$。

**最终编码器**：优化完成后，DAVE 的最终视觉编码器由最优合并系数 $\alpha_i^{\star}$ 构成：

$$ \phi_{\mathrm{DAVE}}^{\mathrm{final}} = \phi_{\mathrm{merge}}(\{\alpha_i^{\star}\}_{i=1}^{n}) $$

消融实验（Table 4a）表明，学习合并系数（Learned Coef）在文档和 Web 基准上显著优于无合并、平均合并和基于 Fisher 信息的启发式合并方法。此外，合并的 LLM 数量越多（从仅 Granite 到 Granite+Qwen+Phi），性能持续提升（Table 4b），验证了多解码器知识融合的有效性。

## 实验与分析

### 核心瓶颈与因果机制

现有视觉语言模型（VLM）在文档理解和Web代理任务上的根本瓶颈在于：通用视觉编码器缺乏对结构化图像（文档、UI界面、图表）至关重要的低层结构和空间信息。文档和网页图像具有极低的patch间方差（Figure 3），导致标准MAE的归一化像素损失训练发散（Figure 4），无法有效学习布局和空间先验。DAVE通过两阶段因果干预解决此问题：**阶段一**采用直接像素重建损失（MAE-pixel）在20M无标签文档/网页图像上稳定学习结构和空间特征；**阶段二**通过多任务监督自回归预训练学习解析和定位能力，同时集成通用编码器SigLIP2保留高层语义，并通过蒸馏合并多解码器权重实现解码器无关性。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/006_Figure_3.jpg]]
*Figure 3: Inter-patch standard deviation across different data sources*

### 主实验结果

**文档与Web理解基准**（Table 1）：在Llama-3.2-3B设置下，DAVE在8个文档和Web基准上平均超越SigLIP2 **10.5%**。关键结果包括：DocVQA 82.1（+10.0）、OCRBench 62.2（+10.7）、WebSRC 82.6（+14.8）。在Qwen-2.5-7B设置下趋势一致，DAVE在AI2D、InfoVQA、ChartQA、MMMU、VisualWeb、Screenspot-V2、WebSRC上均取得最优或次优结果，验证了方法对解码器规模的鲁棒性。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/002_Table_1.jpg]]
*Table 1: The DAVE’s performance on Document understanding, general VQA, and Web understanding benchmarks with two VLM architectures using different LLMs. The best result per row is highlighted in bold and the second best with underline. Higher values represent better performance*

**Web代理任务**（Table 2）：在Mind2Web的三个子任务（Cross-Task/Cross-Website/Cross-Domain）上，DAVE的Element Accuracy达到30.8，超越最强基线Dolphin（24.0）**+6.8个百分点**，Step Success Rate同样全面领先。这表明DAVE学习的空间定位特征直接转化为代理接地能力的提升。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/003_Table_2.jpg]]
*Table 2: Results on Web Agent. Performance on Mind2Web with three splits (Cross-Task, Cross-Website, Cross-Domain). We report the stepwise accuracy (correct grounding) and the element accuracy (correct grounding and action) for each task*

**经典文档任务**（Table 3）：在文档分割（DocLayNet）上，DAVE以74.1 mAP超越AIMv2（70.5）；在文档识别（DocBank）上以56.9 mAP超越SigLIP2（51.7）。但在语义重的RICO-SCA屏幕分类上，DAVE（92.3）略低于SigLIP2（93.3），这一失败模式将在下文分析。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/004_Table_3.jpg]]
*Table 3: Performance comparison on classic document tasks. DocLayNet and DocBank use mAP, while RICO-SCA uses classification accuracy*

### 消融实验与关键设计验证

**训练策略消融**（Figure 2）：逐步增加设计组件——从随机初始化解码器到预训练LLM解码器，再到集成训练和权重合并——文档VLM性能持续提升，验证了每个组件的独立贡献。

**合并方法消融**（Table 4a）：学习合并系数（Learned Coef）在Doc/Web基准上分别达到63.4/68.2，显著优于平均合并（62.8/67.7）和Fisher合并（59.2/65.0），更大幅领先无合并（55.6/53.0）。蒸馏损失直接优化特征空间对齐，而非依赖启发式重要性估计，是性能差距的因果根源。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/007_Table_4.jpg]]
*Table 4: vision encoder capable of handling such data. Additional implementation details are provided in Appendix E. (a) Comparison of Different Merge Methods*

**合并LLM数量**（Table 4b）：从仅合并Granite编码器到合并Granite+Qwen+Phi三个编码器，Doc/Web性能持续提升（Doc: 59.0→63.4, Web: 63.9→68.2），表明多解码器预训练+合并能有效聚合不同LLM的互补特征偏好。

**集成编码器设计**（Table 4c）：DAVE显著优于简单级联多编码器方案（如SigLIP2+DiT的Doc 50.3/Web 47.6），验证了联合训练专用编码器与冻结通用编码器的必要性——简单拼接无法实现特征空间的深度对齐。

**通用编码器贡献**（Table 10）：集成SigLIP2特征后，RICO-SCA分类准确率从90.7提升至92.3，但仍低于纯SigLIP2的93.3。这表明高层语义特征确有贡献，但DAVE的隐藏维度翻倍（专用+通用特征级联）可能导致单层MLP预测头难以有效池化信息，构成当前设计的结构性限制。

### 失败模式与局限性

1. **语义重任务退化**：在RICO-SCA等依赖高层语义分类的任务上，DAVE略逊于SigLIP2。因果分析指向嵌入维度翻倍后，单层MLP投影头的池化效率不足，而非结构特征本身有害。
2. **训练成本高**：自监督阶段需32块H200 GPU训练120K步，监督阶段需约2M标注样本，对资源受限场景不友好。
3. **分辨率限制**：当前方法依赖固定尺寸平铺，未原生支持任意分辨率和纵横比输入。
4. **代理历史缺失**：Web代理设置中未融入历史动作信息（点击、滚动等），限制了多步推理能力。

### 证据强度总结

| 主张 | 证据锚点 | 置信度 |
|------|---------|--------|
| DAVE平均超越SigLIP2 10.5% | Table 1 | 高（0.98） |
| 学习合并系数优于平均/Fisher合并 | Table 4a | 高（0.95） |
| 低方差导致标准MAE发散 | Figure 3, Figure 4 | 中高（0.90） |
| 集成通用编码器提升语义任务 | Table 10 | 高（0.95） |
| RICO-SCA退化源于维度翻倍 | Table 3, Table 10 | 需进一步验证（推测性） |

### 补充图表

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/008_Table_5.jpg]]
*Table 5: (b) Comparison of Different Merging LLMs*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/009_Table_6.jpg]]

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/010_Table_7.jpg]]

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/011_Table_5.jpg]]
*Table 5: Training hyperparameters for MAE training*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/012_Table_6.jpg]]
*Table 6: Evaluation results on classic document tasks*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_kgk0NqjsoW/figures/014_Table_7.jpg]]
*Table 7: Training hyperparameters for supervised pretraining*

## 方法谱系与知识库定位

### 1. 与通用视觉编码器的关系

DAVE 的出发点在于识别出通用视觉编码器在文档与 Web 场景中的结构性缺陷：低层特征对结构化图像（文档、UI、图表）的表示能力不足，缺乏有效的空间与布局先验。这一判断通过 Figure 3 得到实证支撑——文档和网页图像的 patch 间标准差远低于自然图像，导致标准 MAE 的归一化像素损失训练发散（Figure 4），这构成了方法创新的直接动因。

与主流通用编码器的关系如下：

- **SigLIP2**（Tschannen et al., 2025）：DAVE 将其作为集成训练中的冻结通用分支，负责保留高层语义信息。在 Llama-3.2-3B 设置下，DAVE 在 8 个文档和 Web 基准上平均超越 SigLIP2 达 10.5%（Table 1），但在语义重的 RICO-SCA 屏幕分类任务上略低于 SigLIP2（92.8% vs 93.3%，Table 3），这揭示了专用编码器在纯语义任务上的补偿不足。
- **DinoV2**（Oquab et al., 2023）与 **AIMv2**（Fini et al., 2025）：在 Table 1 和 Table 3 中作为自监督/对比学习基线出现，DAVE 在所有文档和 Web 基准上均显著优于二者。AIMv2 在 DocLayNet 上达到 70.5 mAP，DAVE 为 74.1 mAP（Table 3），差距约 3.6 个百分点。
- **Web-SSL MAE**（Fan et al., 2025）：作为大规模自监督 MAE 基线，DAVE 在经典文档任务上同样全面超越（Table 6），验证了针对性损失修改和多阶段训练的价值。

### 2. 与文档/Web 专用模型的对比

DAVE 与三类专用方案形成竞争关系：

**文档专用编码器**：**DiT**（Li et al., 2022a）是代表性的文档预训练模型。Table 1 显示 DAVE 在 DocVQA 上以 82.1 对 73.2 大幅领先，Table 2 的 Mind2Web 代理任务上 Element Accuracy 为 30.8 对 23.3。关键差异在于 DiT 仅依赖文档数据，而 DAVE 通过两阶段训练同时捕获文档和 Web 的结构先验。

**编码器-解码器文档模型**：**Pix2Struct**（Lee et al., 2023）和 **Dolphin**（Feng et al., 2025）均为端到端的文档理解模型。DAVE 作为纯编码器方案，在 Table 1 的多数基准上表现更优，且在 Table 2 的 Web 代理任务上以平均 5% 的优势超越 Dolphin（原文声称的最强基线）。Table 4c 的消融进一步表明，简单的多编码器级联（如 SigLIP2+DiT、SigLIP2+Pix2Struct）远不如 DAVE 的集成训练方案有效。

**多编码器级联方案**：Table 4c 直接对比了 SigLIP2 与其他专用编码器（DiT、Pix2Struct 等）的级联，DAVE 的 Doc/Web 平均分（63.4/68.2）显著高于所有级联方案，证明端到端的集成训练优于事后特征拼接。

### 3. 关键技术贡献的谱系定位

DAVE 的三个核心机制在方法谱系中有明确的技术渊源与创新点：

**损失函数修改**：标准 MAE 的归一化像素损失（Eq.1）源自 He et al.（2022），DAVE 将其替换为直接像素重建损失（Eq.2）。这一修改的技术动机来自文档/网页图像的低方差特性（Figure 3），属于对自监督预训练在特定数据域上的适配性创新，而非全新的训练范式。

**权重合并**：模型融合（model soup）思想可追溯至 Wortsman et al.（2022），DAVE 的贡献在于将其应用于跨文本解码器的编码器合并，并通过蒸馏损失（Eq. distillation loss）端到端学习合并系数。Table 4a 显示，学习合并系数在 Doc/Web 基准上明显优于平均合并和 Fisher 合并，Table 4b 进一步验证合并的 LLM 数量越多（从单一 Granite 到 Granite+Qwen+Phi），性能持续提升。

**集成训练**：冻结通用编码器并与专用编码器特征级联的做法，在思想上与多模态融合的 late fusion 策略相似，但 DAVE 将其嵌入监督预训练阶段而非推理时拼接。Table 10 的消融显示，集成 SigLIP2 特征后 RICO-SCA 分类准确率从 90.7 提升至 92.3，验证了高层语义的贡献。

### 4. 适用边界与局限性

**语义重任务的退化**：DAVE 在 RICO-SCA 上略低于 SigLIP2（Table 3），论文分析认为这是由于嵌入维度翻倍（专用+通用编码器级联）导致单层 MLP 预测头难以有效池化信息。这一局限表明，当前的特征融合方式在纯语义分类场景下可能引入冗余而非增益。

**计算资源需求**：自监督阶段使用 20M 图像、32 块 H200 GPU 训练 120K 步，监督阶段使用约 2M 标注样本（Table 5, Table 7），整体训练成本较高，限制了该方法在资源受限场景下的直接复现。

**输入分辨率与纵横比**：当前方法未针对任意分辨率和纵横比的输入进行专门优化，仅依赖固定尺寸的平铺方式，这继承了 ViT 架构的固有局限。

**Web 代理的历史信息缺失**：在 Mind2Web 设置中，视觉编码器未融入先前的代理动作（如点击、滚动），限制了多步推理能力。Table 2 中 Element Accuracy 的绝对值（30.8）仍然较低，表明 Web 代理任务本身仍有巨大提升空间。

### 5. 开放问题与后续方向

1. **维度压缩与预测头适配**：如何在保持强结构和空间特征的同时降低隐藏维度，以更好地适应单层 MLP 等轻量预测头，是解决 RICO-SCA 类任务退化的关键。

2. **原生多分辨率支持**：能否使视觉编码器原生支持任意分辨率和纵横比的输入，而无需平铺和插值，这直接影响文档和 Web 场景的实用性。

3. **代理动作融入**：如何将先前的代理动作（点击、滚动、表单输入）作为额外输入融入视觉编码器，以提升多步 Web 代理的性能，是通向实用化代理系统的重要一步。

4. **跨域泛化**：该视觉预训练范式是否可以推广到医学影像、工程图纸等视觉语言数据稀缺的其他垂直领域，Table 13 的跨域评估（CMMMU、DTCBench）仅提供了初步证据，需要更系统的验证。

5. **数据与计算效率**：当前方案的数据和计算需求较高，如何在更少的无标签数据和更低的计算预算下获得可比的结构先验，是工程落地的核心挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/DAVE_A_VLM_Vision_Encoder_for_Document_Understanding_and_Web_Agents.pdf]]
