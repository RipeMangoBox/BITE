---
title: "Vision Transformers Are Good Mask Auto-Labelers"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/Vision_Transformers_Are_Good_Mask_Auto_Labelers.pdf
project_link: null
code_link: https://github.com/NVlabs/mask-auto-labeler
aliases:
- MALM
- VTAGMAL
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "设计一个两阶段框架，在仅使用边界框监督的条件下自动生成高质量掩码伪标签，从而训练出与全监督模型性能接近的实例分割模型。"
primary_logic: "将掩码自动标注与实例分割训练解耦为两个阶段，第一阶段以RoI裁剪图像为输入，利用标准Vision Transformer (ViT) 作为图像编码器，配合基于注意力的掩码解码器、边界框扩展采样策略、多示例学习 (MIL) 损失及条件随机场 (CRF) 损失，生成极高质量的掩码伪标签，其质量有时甚至超越人工标注，从而显著提升第二阶段实例分割模型的性能。"
claims:
- "实例分割模型使用MAL生成的掩码训练，性能可保留全监督模型的97.4%"
- "最佳模型在COCO test-dev 2017上达到44.1% mAP，远超之前方法"
- "注意力解码器设计使MAL掩码AP达42.3%，保留率94.4%，而查询式解码器几乎失败"
- "COCO val2017 上 Mask AP = 43.3"
---

# Vision Transformers Are Good Mask Auto-Labelers

> [!tip] 核心洞察
> 将掩码自动标注与实例分割训练解耦为两个阶段，第一阶段以RoI裁剪图像为输入，利用标准Vision Transformer (ViT) 作为图像编码器，配合基于注意力的掩码解码器、边界框扩展采样策略、多示例学习 (MIL) 损失及条件随机场 (CRF) 损失，生成极高质量的掩码伪标签，其质量有时甚至超越人工标注，从而显著提升第二阶段实例分割模型的性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视觉Transformer是优秀的掩码自动标注器 |
| 英文题名 | Vision Transformers Are Good Mask Auto-Labelers |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2301.03992) · [GitHub](https://github.com/NVlabs/mask-auto-labeler) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Mask Auto-Labeler (MAL) |
| Dataset | COCO val2017, COCO test-dev 2017, LVIS v1 |

> [!tip] 效果简介
> - COCO val2017 上，Mask AP 为 43.3，对比 35.0 (DiscoBox with same backbone)，变化 +8.3。
> - COCO test-dev 2017 上，Mask AP 为 44.1，对比 40.0 (BoxTeacher)，变化 +4.1。
> - LVIS v1 上，Mask AP (w/ ResNeXt-101-64x4d) 为 24.5，对比 25.8 (fully supervised Mask R-CNN)，变化 -1.3 (Ret. 95.0%)。

## 概要

**问题瓶颈**：全监督实例分割依赖昂贵的人工掩码标注——COCO数据集中79%的标注时间耗费在掩码上。仅使用边界框监督训练实例分割模型虽成本低廉，但其性能与全监督方法之间存在显著差距。

**核心方案**：本文提出**Mask Auto-Labeler (MAL)**，一个两阶段框架，将掩码自动标注与实例分割训练解耦。第一阶段以RoI裁剪图像为输入，利用标准Vision Transformer (ViT) 编码器和基于注意力的掩码解码器，结合多示例学习 (MIL) 损失与条件随机场 (CRF) 损失，仅从边界框监督生成高质量掩码伪标签；第二阶段使用这些伪标签训练标准实例分割模型。

**关键发现**：
- 使用MAL生成的掩码训练实例分割模型，性能可**保留全监督模型的97.4%**。
- 最佳模型在COCO test-dev 2017上达到**44.1% mAP**，显著超越此前最优的边界框监督方法（BoxTeacher 40.0%）。
- 在LVIS v1上，MAL掩码训练的模型达到全监督**Mask R-CNN的95.0%保留率**（24.5% vs 25.8%）。
- 基于注意力的解码器是成功关键：其掩码AP达42.3%，保留率94.4%；而查询式解码器几乎完全失败（掩码AP仅1%）。

**方法定位**：MAL属于边界框监督实例分割的伪标签生成范式，区别于BBTP、BoxInst、DiscoBox等端到端方法。其核心创新在于将任务解耦、引入标准ViT作为图像编码器，并设计注意力解码器与RoI输入策略。生成的高质量掩码伪标签有时**比人工标注更锐利、更贴合边界**，但在严重遮挡场景下仍不及人工标注。



实例分割需要为图像中的每个目标实例预测像素级掩码，而全监督训练依赖大量精确的人工掩码标注。这一标注过程极其昂贵且耗时——以COCO数据集为例，**79%的标注时间花费在掩码绘制上**，边界框标注则相对廉价。因此，一个自然的研究方向是：能否仅用边界框监督来训练实例分割模型，从而大幅降低标注成本？

现有边界框监督实例分割方法（如BBTP、BoxInst、BoxLevelSet、DiscoBox、BoxTeacher等）尝试在端到端框架中同时学习检测与分割。然而，这些方法的性能与全监督模型之间仍存在明显差距，说明仅靠边界框先验直接训练分割模型面临根本性困难：**边界框提供的空间约束过于粗糙，难以精确界定目标轮廓**。

本文的核心洞察在于：与其让一个模型在边界框监督下同时完成检测和分割，不如**将掩码生成与实例分割训练解耦为两个阶段**。第一阶段专注于利用边界框监督生成高质量掩码伪标签，第二阶段则使用这些伪标签以标准全监督方式训练实例分割模型。这一设计的关键瓶颈在于第一阶段——如何仅凭边界框生成足以替代人工标注的掩码？

为此，本文提出**Mask Auto-Labeler (MAL)**，一个基于Transformer的掩码自动标注框架。MAL以RoI裁剪图像为输入，采用标准Vision Transformer (ViT) 作为图像编码器，配合基于注意力的掩码解码器、边界框随机扩展采样策略、多示例学习（MIL）损失以及条件随机场（CRF）损失，在仅使用边界框监督的条件下生成极高质量的掩码伪标签。实验表明，这些伪标签的质量有时甚至超越人工标注，使得第二阶段训练的实例分割模型能够**保留全监督模型97.4%的性能**，最佳模型在COCO test-dev 2017上达到**44.1% mAP**，显著超越此前方法。



## 核心方法与创新机理

### 两阶段解耦：从端到端到“先标注、后训练”

现有边界框监督实例分割方法（如 **BoxInst**、**DiscoBox**、**BoxTeacher** 等）普遍采用端到端框架，在单个网络中同时学习检测与分割，导致掩码质量受限于联合优化的折衷。MAL 的核心架构创新在于将问题**解耦为两个独立阶段**（Figure 2）：

- **第一阶段（掩码自动标注）**：专注于从边界框监督中生成高质量掩码伪标签，不受后续分割模型约束；
- **第二阶段（实例分割训练）**：将生成的伪标签直接替换人工标注，训练任意的全监督实例分割模型。

这一解耦设计的关键收益是使两个网络各司其职：第一阶段网络专注于掩码生成质量，第二阶段网络专注于分割精度。实验证明，这种解耦使得 MAL 生成的掩码训练出的实例分割模型可**保留全监督模型性能的 97.4%**，最佳模型在 COCO test-dev 2017 上达到 **44.1% mAP**，显著超越此前最优方法（BoxTeacher 40.0%）。

### 输入形式变革：RoI 裁剪 + 边界框随机扩展

传统方法以整图作为输入，小物体因分辨率不足而掩码质量低下。MAL 改为**以 RoI 裁剪图像为输入**（Figure 3），无论物体原始尺寸如何，裁剪区域均被放大至固定分辨率，天然解决了小物体分割难题。

更关键的是**边界框随机扩展策略**：对每个边界框进行随机扩展（扩展率 $\theta$ 控制），将背景像素纳入输入。这一设计防止了掩码预测退化为“全框填满”的平凡解——若仅使用紧盒内像素，模型可能简单地将所有像素预测为前景即可降低损失。扩展边界框后，MIL 损失中的负包（negative bags）从扩展区域的行/列中选取，迫使模型学习区分前景与背景。消融实验（Table 5）表明，$\theta = 1.2$ 时获得最佳 Mask AP 42.3% 和保留率 94.4%。

### 编码器选择：标准 ViT 的反直觉优势

在图像分类任务上，ConvNeXt 和 Swin Transformer 显著优于 DeiT，但 MAL 的实验揭示了**标准 ViT 在掩码自动标注任务上的反直觉优势**（Table 4）：

- ViT-DeiT-Small 的 Mask AP 和保留率均优于 ConvNeXt-Base 和 Swin-Base；
- 经 MAE 预训练的 ViT-Base 和 ViT-Large 达到最佳性能（Mask AP 42.3，保留率 94.4）。

作者通过**聚类分数**（Clustering Score）对这一现象给出了机制性解释（Table 6）：标准 ViT 的归一化特征向量与前景/背景聚类中心的平均平方距离显著小于 Swin 和 ConvNeXt，表明其全局自注意力机制天然具备更强的**前后景区分能力**。ViT-MAE-Large 的聚类分数低至 0.301，与最优自动标注性能高度相关。Figure 6 的多头自注意力可视化进一步显示，标准 ViT 的深层注意力图能够清晰聚焦于物体边界区域。

### 掩码解码器：注意力机制的关键作用

MAL 比较了四种解码器设计（Figure 4）：全连接解码器、全卷积解码器、基于注意力的解码器、查询式解码器。消融实验（Table 3）揭示了一个重要发现：

- **基于注意力的解码器**（受 YOLACT 启发，由实例感知头 $K$ 和像素级头 $V$ 组成，输出 $D(E(I)) = K(E(I)) \cdot V(E(I))$）取得 42.3% Mask AP 和 94.4% 保留率；
- **查询式解码器**（类似 DETR 的设计）在边界框监督下几乎完全失败（Mask AP 仅 1%），尽管在全监督实例分割中表现优异。

这一对比表明，在缺乏精确掩码监督的条件下，基于查询的交叉注意力机制难以收敛，而基于内积的注意力解码器通过显式建模实例感知特征与像素级特征的对应关系，更适配弱监督场景。

### 损失函数设计：MIL + CRF 的协同机制

MAL 的损失函数由两项协同构成：

$$\mathcal{L} = \alpha_{\mathrm{mil}} \mathcal{L}_{\mathrm{mil}} + \alpha_{\mathrm{crf}} \mathcal{L}_{\mathrm{crf}}$$

- **MIL 损失**：将每行/列视为一个“包”（bag），通过最大池化聚合包内像素预测，再计算 Dice 损失。这一设计施加了**紧盒先验**——每一行/列至少应有一个像素属于前景，同时通过扩展框中的负包抑制背景区域。
- **CRF 损失**：以教师网络（EMA 更新）的平均掩码预测作为一元势，结合 8 邻域像素颜色差异的成对势，通过平均场算法细化掩码，再以细化结果作为伪标签进行自训练。CRF 的平滑约束使生成的掩码边界更加贴合物体轮廓。

Figure 8 的敏感性分析显示，MAL 对损失权重和 CRF 超参数在合理范围内具有较好的鲁棒性。

### 方法谱系与知识库定位

MAL 在弱监督实例分割领域做出了以下定位贡献：

| 维度 | 此前方法 | MAL 的变革 |
|------|---------|-----------|
| 框架结构 | 端到端联合训练（BoxInst, DiscoBox, BoxTeacher） | 两阶段解耦：掩码自动标注 → 实例分割训练 |
| 输入形式 | 整图输入 | RoI 裁剪 + 随机边界框扩展 |
| 图像编码器 | CNN（ResNet）或层次化 Transformer（Swin） | 标准 ViT + MAE 预训练，利用全局自注意力进行前后景区分 |
| 掩码解码器 | 全卷积或查询式 | 基于注意力的内积解码器（实例感知头 × 像素级头） |
| 监督信号 | MIL 损失或投影损失 | MIL + CRF 协同损失，结合 EMA 教师自训练 |
| 性能上限 | COCO test-dev ~40% mAP（BoxTeacher） | COCO test-dev 44.1% mAP，保留率 97.4% |

MAL 的一个独特贡献在于揭示了**标准 ViT 的全局自注意力天然适配掩码自动标注任务**——这一发现与图像分类领域“层次化 Transformer 优于标准 ViT”的共识形成鲜明对比，为视觉 Transformer 的架构选择提供了新的任务依赖性视角。同时，MAL 生成的掩码伪标签在部分场景下边界质量甚至超越人工标注（Figure 7 左侧），但在严重遮挡场景仍不及人工标注（Figure 7 右侧），指明了后续改进方向。



![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2301_03992/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the two-phase framework of boxsupervised instance segmentation. For the first phase, we train Mask Auto-Labeler using box supervision and conditionally generate masks of the cropped regions in training images (top). We then train the instance segmentation models using the generated masks (bottom)*

MAL 采用**两阶段解耦框架**，将掩码自动标注与实例分割训练分离为两个独立阶段，如图 Figure 2 所示。这一设计的核心动机在于：现有端到端的边界框监督实例分割方法将检测与分割耦合训练，难以充分利用边界框监督信号生成高质量掩码。通过解耦，第一阶段可以专注于掩码伪标签的生成，第二阶段则专注于利用这些高质量伪标签训练实例分割模型。

### 第一阶段：掩码自动标注

第一阶段以**RoI裁剪图像**为输入，而非整图。具体而言，给定原始图像及其边界框标注，MAL 首先对边界框进行随机扩展（扩展率 θ 控制，最优值为 1.2），以包含必要的背景像素，防止模型产生平凡解——即简单地将整个框内区域预测为前景。扩展后的边界框用于裁剪出 RoI 图像，这些图像被统一缩放至固定尺寸后送入掩码自动标注网络。

MAL 的自动标注网络由两个**对称结构的子网络**组成：任务网络（Task Network）和教师网络（Teacher Network），如 Figure 3 所示。每个子网络包含：
- **图像编码器 E**：采用标准 Vision Transformer (ViT)，优先使用 MAE 预训练权重。ViT 的全局自注意力机制天然适合捕获 RoI 图像中的前后景特征差异。
- **掩码解码器 D**：采用基于注意力的解码器设计，由实例感知头 K 和像素级头 V 组成，通过内积运算 $D(E(I)) = K(E(I)) \cdot V(E(I))$ 生成掩码预测。

教师网络通过**指数移动平均 (EMA)** 从任务网络更新权重，其作用是稳定训练过程并提供平滑的掩码预测，用于后续的 CRF 自训练。

损失函数由两部分加权组成：
$$\mathcal{L} = \alpha_{\mathrm{mil}} \mathcal{L}_{\mathrm{mil}} + \alpha_{\mathrm{crf}} \mathcal{L}_{\mathrm{crf}}$$

- **MIL 损失**：将每行和每列像素视为一个“包”，对包内像素进行最大池化后计算 Dice 损失，施加紧盒先验约束。
- **CRF 损失**：利用条件随机场对任务网络和教师网络的平均预测进行细化，将细化后的掩码作为伪标签进行自训练，进一步提升掩码边界质量。

训练完成后，MAL 对训练集中的所有 RoI 图像生成掩码伪标签。这些伪标签的质量有时甚至超越人工标注——在边界粘附性和清晰度方面表现更优（见 Figure 7），但在严重遮挡场景下仍逊于人工标注。

### 第二阶段：实例分割训练

第二阶段将第一阶段生成的掩码伪标签作为监督信号，训练标准的全监督实例分割模型。该阶段完全复用现有的实例分割架构，仅需将真实掩码替换为 MAL 生成的伪标签。论文验证了多种主流架构的兼容性，包括：
- ConvNeXt 搭配 Cascade R-CNN
- Swin Transformer 搭配 Mask2Former
- ResNet/ResNeXt 搭配 SOLOv2

这种设计使得 MAL 可以作为即插即用的掩码标注器，为任意实例分割模型提供训练数据。

### 输入输出流总结

| 阶段 | 输入 | 核心模块 | 输出 |
|------|------|----------|------|
| 第一阶段 | 原始图像 + 边界框 → RoI裁剪图像 | ViT编码器 + 注意力解码器 + EMA教师 + MIL/CRF损失 | 掩码伪标签 |
| 第二阶段 | 原始图像 + 掩码伪标签 | 标准实例分割模型（如Mask2Former） | 实例分割模型 |

该两阶段框架的关键优势在于：第一阶段生成的掩码伪标签质量极高，使得第二阶段训练的实例分割模型能保留全监督模型性能的 **94%–97%**（以保留率衡量），最佳模型在 COCO test-dev 2017 上达到 **44.1% mAP**，显著超越此前最优的边界框监督方法 BoxTeacher（40.0% mAP）。



### 3.1 RoI输入生成与边界框扩展

MAL的输入并非整张图像，而是依据边界框裁剪的RoI（Region-of-Interest）图像。这一设计带来两个关键优势：其一，无论目标尺寸多小，RoI图像都会被放大至固定分辨率，天然缓解了小目标分割的低分辨率难题；其二，裁剪后的图像使网络能够专注于单个实例的分割，而非同时处理整张图像中的多个目标。

然而，仅使用精确边界框裁剪会导致一个严重问题——模型可能学到“将框内所有像素预测为前景”的平凡解。为打破这一退化，MAL引入了**边界框随机扩展**策略。给定原始边界框 $b = (x_0, y_0, x_1, y_1)$ 及其中心 $(x_c, y_c)$，扩展后的边界框定义为：

$$b' = (x_c + \beta_x (x_0 - x_c),\; y_c + \beta_x' (y_0 - y_c),\; x_c + \beta_y (x_1 - x_c),\; y_c + \beta_y' (y_1 - y_c))$$

其中 $\beta_x, \beta_x', \beta_y, \beta_y' \sim U(1, \theta)$ 是独立采样的扩展因子，$\theta$ 为扩展率超参数。扩展后，框内新增的背景像素为MIL损失提供了天然的负样本包（negative bags），迫使模型学习区分前景与背景。消融实验（Table 5）表明，$\theta = 1.2$ 时取得最优结果（Mask AP 42.3，保留率 94.4%）。

### 3.2 双网络架构：任务网络与教师网络

MAL由两个结构完全对称的网络组成：**任务网络**（Task Network）和**教师网络**（Teacher Network）。每个网络均包含一个图像编码器 $E$（或 $E^t$）和一个掩码解码器 $D$（或 $D^t$）。教师网络的权重通过指数移动平均（EMA）更新：

$$\theta^t \leftarrow \lambda \theta^t + (1 - \lambda) \theta$$

引入教师网络的核心动机在于稳定训练过程——标准ViT的优化本身具有挑战性，直接训练容易出现损失爆炸（loss explosion），而EMA教师提供的平滑目标有效缓解了这一问题。

### 3.3 图像编码器：标准Vision Transformer

MAL采用标准ViT（Standard ViT）作为图像编码器 $E$，而非层次化设计（如Swin Transformer）或卷积架构（如ConvNeXt）。标准ViT在整个特征提取过程中保持统一的特征图尺寸，其多头自注意力（MHSA）机制能够捕获全局上下文。实验发现，即使标准ViT在ImageNet分类任务上不及Swin和ConvNeXt，其在掩码自动标注任务上却表现出显著优势。进一步地，MAE（Mask Autoencoder）预训练可将掩码质量提升至最佳水平——ViT-MAE-Base和ViT-MAE-Large在Table 4中分别取得42.3和42.7的Mask AP，远超ConvNeXt-Base（41.2）和Swin-Base（40.7）。

### 3.4 基于注意力的掩码解码器

掩码解码器 $D$ 的设计是MAL成功的关键要素之一。在比较了四种解码器架构（Figure 4）后，基于注意力的解码器脱颖而出（Table 3：Mask AP 42.3，保留率94.4%），而查询式解码器（Query-based Decoder）几乎完全失败（Mask AP仅1%）。

注意力解码器的核心思想借鉴了YOLACT的实例分割头设计，将解码过程分解为两个并行分支：

- **实例感知头** $K(E(I))$：生成一组实例感知的注意力权重，捕获“哪个区域属于该实例”的全局信息。
- **像素级头** $V(E(I))$：生成像素级的特征响应，保留精细的空间细节。

最终掩码预测由两者的内积得到：

$$D(E(I)) = K(E(I)) \cdot V(E(I))$$

这种分解使得模型能够同时关注“实例整体”和“局部细节”，在仅使用边界框监督的条件下仍能生成边界粘合的高质量掩码。相比之下，全连接解码器缺乏空间归纳偏置，全卷积解码器难以捕获全局上下文，而查询式解码器在缺乏密集掩码监督时无法学习有意义的查询向量。

### 3.5 损失函数设计

MAL的优化目标由两项损失加权组成：

$$\mathcal{L} = \alpha_{\mathrm{mil}} \mathcal{L}_{\mathrm{mil}} + \alpha_{\mathrm{crf}} \mathcal{L}_{\mathrm{crf}} \tag{1}$$

#### 3.5.1 多示例学习损失（MIL Loss）

MIL损失施加“紧盒先验”（tight-box prior），即对于边界框内的每一行和每一列，至少存在一个像素属于前景。具体而言，将预测掩码的每一行和每一列视为一个“包”（bag），对每个包内的像素预测值取最大池化，然后与真实的行/列标签计算Dice损失：

$$\mathcal{L}_{mil} = 1 - \frac{2 \sum_i g_i \cdot \max\{B_i\}^2}{\sum_i \max\{B_i\}^2 + \sum_i g_i^2} \tag{2}$$

其中 $B_i$ 表示第 $i$ 个包内的像素预测集合，$g_i \in \{0, 1\}$ 是该包的真实标签（前景包为1，背景包为0）。背景包来自扩展边界框后新增的行和列。这一机制迫使模型在每个前景行/列中至少激活一个像素，同时抑制背景区域的所有像素。

#### 3.5.2 条件随机场损失（CRF Loss）

MIL损失仅提供粗粒度的行/列级别监督，无法约束掩码的边界质量。为此，MAL引入CRF损失进行自训练式的掩码细化。具体流程为：首先对任务网络和教师网络输出的平均掩码 $m^a$ 进行CRF后处理，得到细化掩码 $l$；然后将 $l$ 作为伪标签，与任务网络的原始预测 $m$ 计算Dice损失。

CRF的能量函数定义为：

$$E(l|m^a, X^c) = \mu(X|m^a, I^c) + \psi(X|I^c) \tag{3}$$

其中一元势 $\mu(X|m^a, I^c)$ 鼓励像素标签 $X$ 与平均掩码 $m^a$ 保持一致；成对势 $\psi(X|I^c)$ 基于8邻域像素的颜色差异施加平滑约束：

$$\psi(\pmb{X}|\pmb{I}^c) = \sum_{\substack{i \in \{0..N-1\} \\ j \in \mathcal{N}(i)}} \omega \exp\left(\frac{-|\pmb{I}_i^c - \pmb{I}_j^c|^2}{2\zeta^2}\right) [\pmb{X}_i \neq \pmb{X}_j] \tag{4}$$

其中 $\omega$ 和 $\zeta$ 控制平滑强度与颜色敏感度。通过平均场算法求解CRF后，得到细化掩码 $l$，进而计算CRF Dice损失：

$$\mathcal{L}_{crf} = 1 - \frac{2 \sum_i l_i m_i}{\sum_i l_i^2 + m_i^2} \tag{5}$$

CRF损失的关键作用在于：它利用颜色一致性先验在像素级细化掩码边界，并将细化结果作为自训练信号回传，使模型逐步学会生成边界更精确的掩码。消融实验（Figure 8）显示，CRF损失对最终性能有显著贡献，且对超参数 $\omega$ 和 $\zeta$ 在合理范围内不敏感。

### 3.6 聚类分数：编码器能力的量化度量

为解释不同图像编码器在掩码自动标注上的性能差异，MAL提出了一种**聚类分数**（Clustering Score）度量。具体做法是：提取编码器最后一层的特征图，利用真实掩码将特征向量划分为前景（FG）和背景（BG）集合，分别计算两者的聚类中心，然后度量所有归一化特征向量与其对应聚类中心的平均平方距离：

$$S = \frac{1}{N} \sum_{i}^{N} \left( \frac{f_i^E}{|f_i^E|} - \frac{f_{\gamma(i)}'}{|f_{\gamma(i)}'|} \right)^2$$

其中 $f_i^E$ 是第 $i$ 个特征向量，$f_{\gamma(i)}'$ 是其所属类别（前景或背景）的聚类中心。聚类分数越低，表明编码器对前景和背景的区分能力越强。Table 6显示，ViT-MAE-Large的聚类分数最低（0.301），与其最佳自动标注性能高度相关——这从机制层面解释了标准ViT优于Swin和ConvNeXt的原因：其全局自注意力机制天然适合前景/背景分离任务。



## 实验与关键发现

### 核心定量结果

MAL在COCO和LVIS两个基准上均显著超越了先前最优的边界框监督方法，且性能高度逼近全监督模型。

**COCO实例分割**（Table 1）：MAL搭配Mask2Former/Swin-Small在val2017上达到43.3% Mask AP，在test-dev 2017上达到44.1% Mask AP，比此前最优方法BoxTeacher（40.0%）高出4.1个百分点。当使用与DiscoBox相同的SOLOv2/ResNeXt-101骨干时，MAL在val2017和test-dev上分别领先1.6%和1.3%。更关键的是，MAL训练的模型保留了全监督模型性能的**94.5%**（ConvNeXt-Base Cascade R-CNN）至**97.4%**（最高记录），表明伪标签质量已极为接近人工标注。


![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2301_03992/figures/005_Table_1.jpg]]
*Table 1: Main results on COCO. Ret means the retention rate of box-supervised mask APsupervised mask AP . MAL with SOLOv2/ResNeXt-101 outperforms DiscoBox with SOLOv2/ResNeXt-101 by 1.6% on val2017 and 1.3% on test-dev. Our best model (Mask2former/Swin-Small) achieves 43.3% AP on val and 44.1% AP on test-dev*

**LVIS v1**（Table 2）：MAL搭配ViT-MAE-Base和ResNeXt-101-64x4d-FPN达到24.5% Mask AP，保留全监督Mask R-CNN的95.0%。值得注意的是，MAL在COCO上训练后直接在LVIS上生成伪标签，仅比在LVIS上训练损失约0.35% mAP，展现出良好的开放词汇迁移能力。


![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2301_03992/figures/007_Table_2.jpg]]
*Table 2: Main results on LVIS v1. Training data means the dataset we use for training MAL. We also finetune it on COCO and then generate pseudo-labels of LVIS v1. Compared with trained on LVIS v1 directly, MAL finetuned on COCO only caused around 0.35% mAP drop on the final results, which indicates the great potential of the open-set ability of MAL. Ret means the retention rate of box-supervised mask APsupervised mask AP*

### 关键消融发现

#### 掩码解码器设计决定成败

Table 3比较了四种解码器架构，结果差异悬殊：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2301_03992/figures/008_Table_3.jpg]]
*Table 3: Ablation study of box expansion. We use Standard ViT-MAE-Base as the image encoder of MAL in phase 1 and Cascade RCNN with ConvNext-Small as the instance segmentation models in phase 2. The numbers are reported in % Mask mAP. Among different designs, the attention-based decoder performs the best. We can not obtain reasonable results with Query-based Decoder*

- **基于注意力的解码器**（MAL采用）达到42.3% Mask AP，保留率94.4%；
- 全卷积解码器（37.3%，保留率83.3%）和全连接解码器（34.9%，保留率77.9%）性能明显下降；
- **查询式解码器完全失败**，Mask AP仅1%。

这一结果揭示了边界框监督与全监督在优化特性上的本质差异：查询式解码器依赖密集的真值掩码信号来学习有意义的查询向量，而MIL损失和CRF损失提供的稀疏/弱监督信号不足以驱动此类架构收敛。注意力解码器的成功可归因于其显式的像素-实例内积机制，使模型能在弱监督下更有效地建立特征与掩码的对应关系。

#### 标准ViT是掩码自动标注的最佳编码器

Table 4的系统对比揭示了一个反直觉的发现：在ImageNet分类上表现不及ConvNeXt和Swin Transformer的标准ViT（DeiT-Small），在掩码自动标注上反而优于两者。进一步使用MAE预训练的ViT-Base和ViT-Large达到最佳性能（42.3% Mask AP），而Swin-Base和ConvNeXt-Base分别仅为40.9%和39.6%。


![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2301_03992/figures/009_Table_4.jpg]]
*Table 4: Ablation study of different backbones. All models are pre-trained on ImageNet-1k. ConvNeXt and Swin Transformer outperform DeiT on image classification, but standard ViT-Small [16] (ViT-DeiT-Small) outperforms ConvNeXt-base and Swin-Base on mask Auto-labeling. Standard ViT-Base (ViT-MAE-Base) and Standard ViT-Large (ViT-MAE-Large) pretrained via MAE achieve the best performance on mask Auto-labeling*

为解释这一现象，作者引入**聚类分数**（Table 6）来量化编码器区分前景/背景特征的能力——分数越低表示特征可分性越强。ViT-MAE-Large的聚类分数最低（0.301），与最优自动标注性能高度相关。Figure 6中的注意力可视化进一步显示，标准ViT的多头自注意力层能自然地聚焦于物体区域，无需层次化归纳偏置即可实现精确的前后景区分。



![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2301_03992/figures/010_Figure_6.jpg]]
*Figure 6: Attention visualization of two RoI images produced by MAL. In each image group, the left-most image is the original image. We visualize the attention map output by the 4th, 8th, 12th MHSA layers of the Standard ViTs in MAL*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2301_03992/figures/014_Table_6.jpg]]
*Table 6: Clustering scores for different image encoders. The smaller clustering scores imply a better ability to distinguish foreground and background features*

#### 边界框扩展策略至关重要

Table 5显示，扩展率θ=1.2时获得最优结果（42.3% Mask AP）。无扩展（θ=1.0）时性能显著下降，因为模型缺乏背景像素信息，容易产生全框填充的平凡解。过大的扩展率（θ=1.4）同样损害性能，可能因引入过多干扰背景。这一设计是MAL防止崩溃的关键——通过在扩展区域采样负包（negative bags），MIL损失获得了必要的前景/背景对比信号。


![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2301_03992/figures/013_Table_5.jpg]]
*Table 5: Ablation on box expansion ratio. We use Standard ViT-Base pretrained via MAE (ViT-MAE-Base) and Cascade R-CNN (ConvNeXt-Small) for phase 1 and 2*

### 损失函数与超参数敏感性

Figure 8展示了损失权重和CRF超参数的敏感性分析。MIL损失权重α_mil和CRF损失权重α_crf在较宽范围内均表现稳定，表明两阶段训练框架对超参数选择具有较好的鲁棒性。CRF的平滑项参数ω和ζ同样表现出合理的容忍区间，但极端值会导致性能下降——过强的平滑会模糊边界，过弱则无法有效抑制噪声。



### 伪标签质量分析

Figure 7的横向对比揭示了MAL伪标签与人工标注的互补特性：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2301_03992/figures/012_Figure_7.jpg]]
*Figure 7: The lateral comparison between MAL-generated pseudo-labels (top) and GT masks (bottom) on COCO val2017. On the left, we observe that MAL-generated pseudo-labels are sharper and more boundary-sticky than GT masks in some cases. On the right, we observe that in highly occluded situations, human-annotated masks are still better*

- **优势场景**：MAL生成的掩码在某些情况下比人工标注**更锐利、更贴合边界**，这可能得益于CRF损失对边缘的显式建模；
- **劣势场景**：在高度遮挡的情况下，人工标注仍然明显优于MAL，这是该方法的主要失败模式。

Figure 9进一步显示，使用MAL伪标签训练的Mask2Former与使用真值掩码训练的版本在定性上高度一致，仅在细节边界和极端遮挡处有细微差距。

### 额外应用：掩码监督提升目标检测

Table 7验证了MAL伪标签的通用价值：在LVIS v1上，添加MAL掩码监督使检测模型获得约1% AP的提升，与添加真值掩码监督的效果相当。在COCO val2017上同样观察到一致但较小的提升，且该提升在不同随机种子下保持稳定。这表明MAL生成的掩码不仅可用于训练分割模型，还可作为通用的辅助监督信号。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2301_03992/figures/015_Table_7.jpg]]
*Table 7: Results of detection by adding different mask supervision. The models are evaluated on COCO val2017 and LVIS v1. By adding mask supervision using ground-truth masks or mask pseudo-labels, we can get around 1% improvement on different AP metrics on LVIS v1. On COCO val2017, the detection performance also benefits from mask pseudo-labels. Although the improvement is less than COCO’s, the improvement is consistent over different random seeds*




## 定位与知识库关联

### 1. 问题定位：边界框监督实例分割的演进脉络

全监督实例分割的性能高度依赖昂贵的人工掩码标注——COCO数据集中约79%的标注时间消耗在掩码绘制上。为降低标注成本，边界框监督实例分割（box-supervised instance segmentation）成为重要研究方向，其目标是在仅使用边界框标注的条件下训练实例分割模型。

该方向已涌现多种代表性方法：
- **BBTP** 利用边界框紧致性先验，通过多实例学习（MIL）约束掩码预测。
- **BoxInst** 引入颜色相似性与边缘感知损失，直接在边界框内优化掩码。
- **BoxLevelSet** 将水平集方法融入边界框监督，通过能量函数演化掩码轮廓。
- **DiscoBox** 提出发现-细化两阶段策略，同时改进边界框与掩码质量。
- **BoxTeacher** 引入教师-学生框架与伪标签自训练机制，在COCO test-dev上达到40.0% Mask AP，为此前最优方法。

然而，这些方法的共同瓶颈在于：它们将掩码学习与实例分割训练耦合在端到端框架中，导致模型难以专注于掩码质量的精细化提升。与全监督模型的性能差距始终显著，保留率（retention rate）难以突破90%。

### 2. MAL的方法论创新与谱系定位

Mask Auto-Labeler (MAL) 的核心创新在于**将掩码自动标注与实例分割训练解耦为两个独立阶段**，从根本上改变了边界框监督实例分割的范式。

**两阶段解耦框架**：第一阶段（掩码自动标注）专注于利用边界框监督生成高质量掩码伪标签；第二阶段（实例分割训练）使用这些伪标签训练任意全监督实例分割模型。这种解耦使得两个阶段可以独立优化，第一阶段可选用最适合掩码生成的架构（标准ViT + 注意力解码器），第二阶段可选用最强的实例分割模型（如Mask2Former、Cascade R-CNN等）。

**关键设计选择与消融证据**：
- **RoI裁剪输入**：MAL以边界框裁剪图像而非整图作为输入，自然解决了小目标分辨率不足的问题，同时使模型聚焦于分割任务本身。这一设计配合边界框随机扩展策略（最佳扩展率θ=1.2，Table 5），有效防止了平凡解的出现。
- **标准ViT编码器**：与主流趋势（使用层次化Transformer如Swin或现代卷积网络如ConvNeXt）不同，MAL发现标准Vision Transformer（尤其是MAE预训练）在掩码自动标注任务上显著优于Swin和ConvNeXt（Table 4：ViT-MAE-Base Mask AP 42.3 vs. Swin-Base 41.2 vs. ConvNeXt-Base 39.9）。聚类分数分析（Table 6）进一步揭示，标准ViT具有更强的前背景特征区分能力（ViT-MAE-Large聚类分数0.301，为所有编码器中最低）。
- **注意力解码器**：MAL采用基于注意力的解码器设计（受YOLACT启发），由实例感知头K和像素级头V的内积生成掩码预测 $D(E(I)) = K(E(I)) \cdot V(E(I))$。消融实验（Table 3）表明，注意力解码器以42.3% Mask AP和94.4%保留率显著优于全连接解码器（40.7% / 90.8%）和全卷积解码器（39.6% / 88.4%），而查询式解码器几乎完全失败（Mask AP仅1%）。这一发现具有重要启示：在边界框监督条件下，基于注意力内积的掩码生成机制比基于可学习查询向量的机制更稳定。
- **MIL损失 + CRF损失**：总损失 $\mathcal{L} = \alpha_{\mathrm{mil}} \mathcal{L}_{\mathrm{mil}} + \alpha_{\mathrm{crf}} \mathcal{L}_{\mathrm{crf}}$ 结合了紧盒先验（通过行列最大池化的Dice损失）和边缘细化（通过CRF平均场算法生成的自训练伪标签），两者互补地提升了掩码质量。
- **EMA教师网络**：引入与任务网络结构相同、通过指数移动平均更新的教师网络，用于稳定标准ViT的训练过程并提供平滑的CRF目标。

### 3. 性能边界与适用条件

**优势边界**：
- 在COCO val2017上，MAL + Mask2Former/Swin-Small达到43.3% Mask AP，最佳模型在test-dev上达到44.1%，显著超越此前最优方法BoxTeacher（40.0%）。
- 保留率高达97.4%，即使用MAL伪标签训练的模型可恢复全监督模型97.4%的性能。对于更重的实例分割模型（如ConvNeXt-Base + Cascade R-CNN），保留率可达94.5%。
- 在LVIS v1长尾数据集上，MAL + ResNeXt-101-64x4d达到24.5% Mask AP，保留率95.0%。
- MAL生成的掩码伪标签在部分场景下甚至比人工标注更锐利、更贴合边界（Figure 7左侧示例）。
- MAL展现出初步的开放词汇能力：在COCO上训练后在LVIS上生成伪标签，仅导致约0.35% mAP下降（Table 2）。

**适用条件与局限**：
- **严重遮挡场景**：在高度遮挡的情况下，MAL生成的掩码质量仍不如人工标注（Figure 7右侧示例），这是当前方法的主要失效模式。
- **模型规模饱和**：从标准ViT-Base扩展到ViT-Large时，性能提升有限，存在明显的饱和现象。更大模型未能持续带来显著增益。
- **计算开销**：第一阶段训练需23小时（COCO）至35小时（LVIS），使用8块V100 GPU。虽可接受但非实时。
- **解码器敏感性**：查询式解码器在边界框监督下严重失败（Mask AP仅1%），其原因尚不明确，暗示当前边界框监督损失函数与某些架构设计存在不兼容性。

### 4. 在知识库中的定位与未解决问题

MAL在边界框监督实例分割领域确立了新的技术范式——**两阶段解耦 + 标准ViT + 注意力解码器**。其核心贡献不在于提出全新的损失函数，而在于揭示了架构选择（标准ViT优于层次化Transformer、注意力解码器优于查询式解码器）对边界框监督掩码生成的深刻影响，以及解耦训练带来的性能飞跃。

**开放问题**：
1. 如何进一步解决严重遮挡情况下的掩码质量下降问题？是否需要在CRF或损失函数中显式建模遮挡关系？
2. 如何突破从ViT-Base到ViT-Large的饱和现象？是否需要针对掩码自动标注任务设计特定的预训练策略或缩放法则？
3. MAL的开放词汇能力在更复杂的真实世界场景（如域偏移、新类别分布）中如何泛化？COCO→LVIS的初步实验仅展示了有限迁移。
4. 查询式解码器为何在边界框监督下严重失败？是否存在改进空间使其适配弱监督条件？这一问题对理解Transformer解码器的工作机制具有理论价值。
5. MAL生成的伪标签在某些情况下优于人工标注（更锐利的边界），这是否暗示可以反过来用MAL优化人工标注的质量？



## 原文 PDF

![[paperPDFs/CVPR_2023/Vision_Transformers_Are_Good_Mask_Auto_Labelers.pdf]]
