---
title: "MatAnyone 2: Scaling Video Matting via a Learned Quality Evaluator"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MatAnyone_2_Scaling_Video_Matting_via_a_Learned_Quality_Evaluator.pdf
aliases:
- M2
- M2SVMLQE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入一个无需真实标签的像素级抠图质量评估器（MQE），在学习过程中同时提供在线训练引导和离线数据筛选，为视频抠图提供有效的边界和语义监督。
primary_logic: MQE 能利用分割掩膜继承非边界区域的可靠语义标签，并结合 DINOv3 编码器感知边界细节，从而在没有真值的情况下准确评估预测 α 遮罩的可靠性。这种评估能力使得大规模真实视频抠图数据集（VMReal）的自动构建成为可能，并与在线损失一起显著提升语义精度和边界保真度。
claims:
- MQE 接收 RGB 帧、预测 α 遮罩和分割掩膜，输出二元评估图，标定可靠与错误像素，无需真实 α 遮罩。
- 在线引导损失 L_eval 鼓励降低错误概率，为边界区域提供比先前弱无监督损失更有效的信号。
- 通过双分支标注流水线构建的 VMReal 数据集包含 28K 真实视频片段、2.4M 帧，是此前最大合成数据集的约 35 倍。
- 参考帧训练策略使模型能处理长视频中未见区域的大幅外观变化，且不增加显存负担。
---

# MatAnyone 2: Scaling Video Matting via a Learned Quality Evaluator

> [!tip] 核心洞察
> MQE 能利用分割掩膜继承非边界区域的可靠语义标签，并结合 DINOv3 编码器感知边界细节，从而在没有真值的情况下准确评估预测 α 遮罩的可靠性。这种评估能力使得大规模真实视频抠图数据集（VMReal）的自动构建成为可能，并与在线损失一起显著提升语义精度和边界保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | MatAnyone 2：通过学习质量评估器扩展视频抠图 |
| 英文题名 | MatAnyone 2: Scaling Video Matting via a Learned Quality Evaluator |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.11782) · [Project](https://pq-yang.github.io/projects/MatAnyone2/) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MatAnyone 2 |
| Dataset | VideoMatte, YoutubeMatte, CRGNN |

> [!tip] 效果简介
> - VideoMatte (1920×1080) 上，MAD↓ 4.10 vs 4.24 (MatAnyone) (-0.14)；Grad↓ 4.00 vs 4.00 (MatAnyone) (0.00 (但本文整体趋势更低，参见低分辨率下 27.1% 下降))。
> - YoutubeMatte (1920×1080) 上，MAD↓ 1.61 vs 1.99 (MatAnyone) (-0.38)；Grad↓ 7.13 vs 8.91 (MatAnyone) (-1.78)。
> - CRGNN (real‑world) 上，MAD↓ 4.24 vs 5.76 (MatAnyone) (-1.52)。

## 概述

视频抠图（Video Matting）旨在从视频序列中精确分离前景与背景，生成逐像素的 α 遮罩，是视觉特效、实时会议等应用的核心技术。然而，该领域长期受困于一个根本瓶颈：**现有视频抠图数据集规模极小且均为合成数据，缺乏真实场景下的边界监督**。合成数据的前景-背景融合难以复现真实世界的复杂光照、运动模糊与发丝级细节，导致模型在边界区域丢失高频细节，在语义区域产生类似分割的粗糙掩膜。

针对这一瓶颈，**MatAnyone 2** 提出了一个关键因果旋钮——**学习一个无需真实 α 标签的像素级抠图质量评估器（Matting Quality Evaluator, MQE）**。MQE 接收 RGB 帧、预测 α 遮罩与分割掩膜三元组，输出二元评估图，标定每个像素的可靠与错误区域（Figure 3）。其核心洞察在于：MQE 可利用分割掩膜继承非边界区域的可靠语义标签，并借助 DINOv3 编码器感知边界细节，从而在没有真值的情况下准确评估预测 α 遮罩的可靠性。这一评估能力带来了双重收益：

- **在线训练引导**：MQE 的错误概率图构成引导损失 $\mathcal{L}_{eval} = \| P_{eval}^{(0)} \|_1$，在训练中直接惩罚低质量区域，为边界提供比先前弱无监督损失更有效、更稳定的学习信号。
- **离线数据筛选**：MQE 作为质量仲裁器，驱动双分支自动标注流水线（视频抠图分支 $B_V$ 与图像抠图分支 $B_I$ 融合），构建了大规模真实视频抠图数据集 **VMReal**——包含约 28K 视频片段、2.4M 帧，约为此前最大合成数据集的 35 倍。

此外，MatAnyone 2 引入**参考帧训练策略**，从序列前部采样长程参考帧作为额外记忆，结合随机遮挡增强，使模型能处理长视频中未见区域的大幅外观变化，且不增加显存负担。

实验结果表明，MatAnyone 2 在多个基准上全面超越先前方法。在合成测试集 YouTubeMatte（1920×1080）上，MAD 从 MatAnyone 的 1.99 降至 **1.61**，Grad 从 8.91 降至 **7.13**；在真实数据集 CRGNN 上，MAD 从 5.76 降至 **4.24**，Grad 从 15.55 降至 **11.74**。消融实验验证了 MQE 在线引导、VMReal 数据集与参考帧策略的互补有效性。定性结果（Figure 1, Figure 6）进一步展示了该方法在风动头发、逆光等挑战场景下，对细节保留与语义准确性的显著提升。

**方法谱系与知识库定位**：MatAnyone 2 属于 mask-guided 视频抠图范式，直接继承自 MatAnyone 的分割-抠图联合训练框架。与 auxiliary-free 方法（如 **MODNet**、**RVM**、**RVM-Large**）相比，它利用首帧掩膜引导获得更强的语义准确性；与扩散式方法 **GVM**（CVPR 2024）相比，它以纯 CNN 架构实现了更清晰的边界细节；与需要逐帧实例掩膜的 **MaGGIe** 相比，它仅需首帧掩膜，部署更轻量。其核心增量在于**将质量评估从人工标注转移到学习模型**，从而打通了大规模真实数据自动构建与在线训练反馈的闭环。

**局限性**：当前自动标注流水线的质量受限于所使用的图像与视频抠图模型的上限，仍可能继承其错误。论文未实施迭代精炼的“数据-模型飞轮”，进一步提升需要大量工程投入。MQE 在非人像视频、多目标场景及透明物体上的泛化能力尚待验证。

## 背景与动机

视频抠图（Video Matting）旨在从视频序列中逐帧分离前景与背景，生成精确的 α 遮罩，是视觉特效、视频会议和内容创作中的核心任务。与图像抠图不同，视频抠图不仅要求单帧的边界精度和语义正确性，还要求跨帧的时序一致性。然而，这一任务长期受制于一个根本性瓶颈：**高质量视频抠图数据的极度匮乏**。

现有视频抠图数据集（如 VideoMatte、YouTubeMatte）均为合成数据，规模有限，且缺乏真实场景下的边界监督信号。这导致模型在真实视频中容易产生两类典型退化：一是边界细节丢失，发丝等精细结构被模糊或截断；二是语义区域误判，前景核心区域被错误地标记为背景，使得抠图结果退化为类似分割的粗糙掩膜。以 **MatAnyone** 为代表的 mask-guided 方法通过引入分割掩膜作为辅助输入，在一定程度上缓解了语义监督不足的问题，但其依赖的弱无监督损失（基于图像先验）对边界区域的引导能力有限，难以从根本上解决细节保真度不足的困境。

扩散模型在图像生成领域展现了强大的先验建模能力，**GVM**（CVPR 2024）将其引入视频抠图，试图利用预训练先验弥补数据不足。然而，扩散模型的随机采样特性导致其输出的 α 遮罩往往在物体边界处产生模糊和不自然的过渡，反而引入了新的伪影。

上述困境的核心矛盾在于：**缺乏真实标注的 α 遮罩作为监督信号，模型无法学习到准确的边界和语义对应关系**。人工标注视频 α 遮罩成本极高——以 CRGNN 真实数据集为例，每 10 帧才进行一次人工标注——这使得大规模真实数据集的构建几乎不可行。

本文的动机正是打破这一僵局：**能否学习一个无需真实 α 遮罩的抠图质量评估器，使其既能在线引导模型训练，又能离线筛选和构建大规模真实视频抠图数据集？** 这一思路的关键洞察在于，分割掩膜可以继承非边界区域的可靠语义标签，而预训练的视觉编码器（如 DINOv3）能够感知边界细节的精细程度，二者结合便可在没有真值的情况下评估预测 α 遮罩的可靠性。基于这一评估能力，本文提出了 **MatAnyone 2**，通过三个关键创新实现视频抠图的规模化突破：

1. **学习式质量评估器（MQE）**：输入 RGB 帧、预测 α 遮罩和分割掩膜，输出像素级二元评估图，标定可靠与错误像素，无需真实 α 遮罩。
2. **双分支自动标注流水线**：利用 MQE 融合视频抠图分支的时序稳定性和图像抠图分支的边界精细度，自动构建包含约 28K 片段、2.4M 帧的 **VMReal** 真实视频抠图数据集，规模约为此前最大合成数据集的 35 倍。
3. **参考帧训练策略**：在训练时引入长程参考帧及随机遮挡增强，使模型能处理长视频中未见区域的大幅外观变化，且不增加显存负担。

通过这些设计，MatAnyone 2 在多个合成和真实基准上全面超越了包括 MatAnyone、GVM、RVM 在内的主流方法，在 YouTubeMatte 1080p 上将 MAD 从 1.99 降至 1.61，Grad 从 8.91 降至 7.13，并在真实场景中展现出更强的边界保真度和语义鲁棒性。

## 核心创新

MatAnyone 2 的核心创新围绕一个核心发现展开：**现有视频抠图模型之所以在边界细节和语义准确性上退化，根源并非网络容量不足，而是缺乏有效的监督信号**。合成数据集规模小且无真实边界，分割掩膜虽能提供非边界区域的可靠语义标签，却无法触及精细的过渡区域。本文通过引入一个**无需真实 α 遮罩的像素级抠图质量评估器（MQE）**，将这一瓶颈转化为可控变量，并围绕 MQE 构建了一套从训练到数据的完整增强体系。

### 从弱无监督到学习式质量引导

MatAnyone 依赖弱无监督损失来约束边界区域，但这种基于图像先验的信号既不稳定，也无法感知语义错误。**MatAnyone 2 的核心 changed slot 在于将边界监督信号从“手工设计的先验约束”替换为“学习到的 MQE 在线引导损失”**。

MQE 接收三元组输入——视频帧 $I_{rgb}$、预测 α 遮罩 $\hat{\alpha}$ 和分割掩膜 $M^{seg}$——输出像素级二元评估图 $M^{eval} \in \{0,1\}^{H \times W}$，标定可靠与错误像素（图3）。其关键能力在于：通过分割掩膜继承非边界区域的可靠语义标签，同时利用 DINOv3 编码器感知边界细节，从而在没有真值的情况下准确判断预测质量（图4）。

基于此，在线引导损失定义为：

$$\mathcal{L}_{eval} = \| P_{eval}^{(0)} \|_1$$

其中 $P_{eval}^{(0)}$ 为 MQE 预测的错误概率图。该损失直接惩罚错误区域的置信度，为边界区域提供比先前弱无监督损失“更有效且更稳定的学习信号”（消融实验证实，仅添加 $\mathcal{L}_{eval}$ 即可使 YouTubeMatte 1080p 上的 MAD 从 1.99 降至 1.90，Grad 从 8.91 降至 8.20）。

### 从合成数据到大规模真实数据

MQE 的另一重角色是作为**离线数据筛选的质量仲裁器**，使得大规模真实视频抠图数据集 VMReal 的自动构建成为可能。通过双分支标注流水线（图5），视频抠图分支 $B_V$ 提供时序稳定的语义预测，图像抠图分支 $B_I$ 提供精细的边界细节，MQE 则通过融合掩膜：

$$M^{fuse} = M_I^{eval} \odot (1 - M_V^{eval})$$

在像素级识别各分支的可靠区域，最终合成标注 α 遮罩：

$$\alpha = \alpha_V \odot (1 - M^{fuse}) + \alpha_I \odot M^{fuse}$$

这一流水线产出的 VMReal 数据集包含约 28K 视频片段、2.4M 帧，是此前最大合成数据集的约 35 倍。训练时，抠图损失 $\mathcal{L}_{mat}^{M}$ 仅在 $M^{eval}=1$ 的高置信度区域计算，避免低质量标注污染模型。消融实验表明，在 $\mathcal{L}_{eval}$ 基础上引入 VMReal 训练后，MAD 进一步降至 1.76，Grad 降至 7.65，dtSSD 也有明显改善。

### 从局部记忆到长程参考帧

MatAnyone 仅在局部训练窗口（8 帧）内传播记忆，无法处理长视频中新出现区域的大幅外观变化。MatAnyone 2 提出**参考帧训练策略**：从序列前部采样数帧作为额外记忆引入训练窗口，并结合随机遮挡增强（random dropout augmentation），在不增加显存负担的前提下扩展时序上下文（图2b）。该策略使模型能够覆盖长时外观突变，消融实验中全部组件启用后达到最优 MAD 1.61、Grad 7.13。

### 创新总结

三项 changed slots 构成递进关系：**MQE 提供了质量评估能力**，使在线引导损失成为可能；**该评估能力进一步驱动 VMReal 的自动构建**，将训练数据从合成域迁移到真实域；**参考帧策略则解决了长视频建模的时序覆盖问题**。三者共同作用，使 MatAnyone 2 在多个基准上全面超越 MatAnyone——在 CRGNN 真实数据集上 MAD 从 5.76 降至 4.24，Grad 从 15.55 降至 11.74，验证了从监督信号到数据规模再到时序建模的系统性改进效果。

## 整体框架

MatAnyone 2 的整体流水线围绕一个核心洞察构建：**无需真实 α 遮罩，即可对抠图质量进行像素级评估**。这一能力由可学习的 **Matting Quality Evaluator（MQE）** 提供，并贯穿训练、数据构建与推理三个环节，形成统一的闭环框架。

### 核心模块与数据流

系统的输入端为视频帧序列 $I_{rgb}$ 及首帧的实例分割掩膜 $M^{seg}$。数据流经以下关键模块：

1. **Video Matting Backbone（基于 MatAnyone 架构）**  
   继承 MatAnyone 的记忆传播机制，以逐帧方式生成预测 α 遮罩 $\hat{\alpha}$。该骨干网络在训练时接收三元组 $\langle I_{rgb}, \alpha, M^{eval} \rangle$，其中 $M^{eval}$ 是 MQE 输出的像素级可靠性图，**抠图损失仅在 $M^{eval}=1$ 的可靠区域计算**，避免低质量伪标签的干扰。

2. **Matting Quality Evaluator（MQE）**  
   MQE 是框架的“质量仲裁器”。其输入为三元组 $(I_{rgb}, \hat{\alpha}, M^{seg})$，输出二元评估图 $M^{eval} \in \{0,1\}^{H \times W}$（1 表示可靠，0 表示错误）。MQE 的核心设计在于：
   - **非边界区域**：继承分割掩膜 $M^{seg}$ 的语义标签作为可靠监督源；
   - **边界区域**：利用 DINOv3 编码器感知的细粒度特征判别细节质量。
   
   这一设计使 MQE 无需真实 α 遮罩即可同时捕捉语义错误与边界退化（Figure 4）。

3. **Online Guidance Loss（$\mathcal{L}_{eval}$）**  
   在训练过程中，MQE 不仅用于数据筛选，还作为在线反馈信号。损失函数定义为：
   $$\mathcal{L}_{eval} = \| P_{eval}^{(0)} \|_1$$
   其中 $P_{eval}^{(0)}$ 是 MQE 预测的错误概率图。该损失推动网络降低错误区域的置信度，为边界区域提供比 MatAnyone 中弱无监督损失更有效且稳定的学习信号（Table 3(b)）。

4. **Dual-Branch Annotation Pipeline（离线数据构建）**  
   为突破合成数据的规模与真实性瓶颈，框架包含一条自动标注流水线（Figure 5）：
   - **视频抠图分支（$B_V$）**：利用时序一致性生成语义稳定但边界粗糙的 α 遮罩；
   - **图像抠图分支（$B_I$）**：逐帧独立处理，保留精细边界但时序不稳定；
   - **MQE 融合**：MQE 分别评估两分支的可靠性，生成融合掩膜 $M^{fuse} = M_I^{eval} \odot (1 - M_V^{eval})$，进而通过加权融合得到高质量标注 α：
     $$\alpha = \alpha_V \odot (1 - M^{fuse}) + \alpha_I \odot M^{fuse}$$
   
   该流水线构建了 **VMReal 数据集**，包含约 28K 视频片段、2.4M 帧，规模约为此前最大合成数据集的 35 倍。

5. **Reference-Frame Training Strategy（长视频建模）**  
   针对长视频中未见区域（如新出现的手臂、手持物体）的外观突变，引入参考帧训练策略：从序列前部采样数帧作为额外记忆，结合随机遮挡增强（random dropout augmentation），在不增加显存开销的前提下扩展时序上下文（Figure 2(b)）。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of MatAnyone and MatAnyone 2. (a) MatAnyone [42] compensates for limited VM data by leveraging segmentation supervision, which provides reliable core-region guidance*

### 训练与推理闭环

整体训练损失为：
$$\mathcal{L}_{mat}^{total} = \mathcal{L}_{mat}^{M} + 0.1 \mathcal{L}_{eval}$$
其中 $\mathcal{L}_{mat}^{M}$ 是在可靠像素上的遮罩化 L1 损失：
$$\mathcal{L}_{l1}^{M} = \frac{\| R_t \odot (\hat{\alpha}_t - \alpha_t) \|_1}{\| R_t \|_1 + \epsilon}$$

推理时，MQE 不参与前向计算，仅骨干网络基于记忆传播与参考帧信息逐帧输出 α 遮罩。这一设计使推理效率与 MatAnyone 持平，但语义精度和边界保真度显著提升——在 YouTubeMatte 1080p 上 MAD 从 1.99 降至 1.61，Grad 从 8.91 降至 7.13（Table 3(d)）。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/015_Figure_9.jpg]]
*Figure 9: Illustration of our dual-branch annotation pipeline on a video sequence. For the video-based branch*

## 核心模块与公式推导

### 抠图质量评估器（MQE）

MQE 是 MatAnyone 2 的核心创新模块，其设计目标是**在没有任何真实 α 遮罩的情况下，对预测遮罩进行像素级可靠性评估**。如图 3 所示，MQE 接收三元组输入 `(I_rgb, α̂, M^seg)`，即视频帧、预测 α 遮罩和分割掩膜，输出一个二元评估图 `M^eval ∈ {0,1}^{H×W}`，其中 1 表示可靠像素，0 表示错误像素。

MQE 能够实现无真值评估的关键在于其**双源监督信号的融合**：
- **非边界区域**：分割掩膜 `M^seg` 提供了核心区域的可靠语义标签，模型继承这些区域的监督信号。
- **边界区域**：利用 DINOv3 编码器感知图像的细粒度边界特征，结合预测 α 遮罩与分割掩膜之间的差异，定位边界细节错误。

MQE 的训练被形式化为一个**二值分割任务**，采用 Focal Loss 来处理可靠/错误像素之间的严重类别不平衡，使训练重点集中在难以识别的错误区域。图 4 展示了 MQE 在边界细节（如发丝模糊）和语义核心区域（如错误分类的前景块）上的准确识别能力。定量分析表明，MQE 的预测概率与真实误差之间存在强单调相关性（Pearson r = 0.87），验证了其评估的可靠性。

### 在线引导损失

基于 MQE 的评估能力，本文设计了在线引导损失 `L_eval`，在训练过程中直接优化抠图网络：

$$ \mathcal{L}_{eval} = \| P_{eval}^{(0)} \|_1 $$

其中 `P_eval^(0)` 是 MQE 预测的**错误概率图**（即像素被分类为“不可靠”的概率）。该损失对错误概率图取 L1 范数，**推动抠图网络降低被 MQE 判定为错误区域的置信度**，从而在训练过程中形成闭环反馈。

与 MatAnyone 中使用的弱无监督损失（依赖图像先验，如梯度一致性）相比，`L_eval` 提供了更有效且稳定的边界监督信号。消融实验证实，仅添加此损失即可在 YouTubeMatte 1080p 上将 MAD 从 1.99 降至 1.90，Grad 从 8.91 降至 8.20。

### 双分支标注流水线与融合公式

为构建大规模真实视频抠图数据集 VMReal，本文设计了双分支自动标注流水线（图 5），包含：
- **视频抠图分支 B_V**：利用时序信息提供语义稳定但边界粗糙的 α 预测 `α_V`。
- **图像抠图分支 B_I**：独立处理每帧，提供精细边界但时序可能不稳定的 α 预测 `α_I`。

MQE 作为质量仲裁器，分别评估两个分支的可靠性，生成 `M_V^eval` 和 `M_I^eval`。融合掩膜定义为图像分支可靠而视频分支不可靠的区域：

$$ M^{fuse} = M_I^{eval} \odot (1 - M_V^{eval}) $$

最终标注 α 遮罩通过融合掩膜选择性引入图像分支的细粒度边界信息：

$$ \alpha = \alpha_V \odot (1 - M^{fuse}) + \alpha_I \odot M^{fuse} $$

该流水线使得 VMReal 数据集的自动构建成为可能，最终包含约 28K 视频片段、2.4M 帧，是此前最大合成数据集的约 35 倍。

### 掩膜化抠图损失

在训练阶段，所有数据样本被统一为三元组 `⟨I_rgb, α, M^eval⟩`。抠图损失仅在 `M^eval = 1` 的可靠区域计算，避免低质量标注区域对模型产生误导：

$$ \mathcal{L}_{l1}^{M} = \frac{\| R_t \odot (\hat{\alpha}_t - \alpha_t) \|_1}{\| R_t \|_1 + \epsilon} $$

其中 `R_t` 为可靠区域掩膜（即 `M^eval = 1` 的区域），`ε` 为防止除零的小常数。

### 整体训练目标

最终训练损失结合掩膜化抠图损失与 MQE 在线引导损失：

$$ \mathcal{L}_{mat}^{total} = \mathcal{L}_{mat}^{M} + 0.1 \mathcal{L}_{eval} $$

其中 `L_eval` 的权重为 0.1，平衡了直接监督与质量引导之间的关系。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/004_Figure_3.jpg]]
*Figure 3: Given an input tuple of video frame*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/003_Figure_4.jpg]]
*Figure 4: Our learned Matting Quality Evaluation (MQE) model accurately identifies: (a) low-quality matting details along the boundary, and (b) semantically wrong regions at core areas, in a pixel-wise manner without requiring ground-truth mattes*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/005_Figure_5.jpg]]
*Figure 5: Our automated dual-branch annotation pipeline. This pipeline enables large-scale construction of real-world VM datasets, resulting in our VMReal dataset. We combine two complementary annotation branches: the temporally stable*

## 实验与分析

### 核心性能：合成基准与真实视频

MatAnyone 2 在四个合成视频抠图基准上均取得最优成绩（Table 1）。以 1920×1080 分辨率为例，在 VideoMatte 上 MAD 从 MatAnyone 的 4.24 降至 4.10，Grad 与 Conn 分别降低 27.1% 和 22.4%；在 YouTubeMatte 上 MAD 从 1.99 降至 1.61，Grad 从 8.91 降至 7.13，降幅分别为 19.1% 和 20.0%。值得注意的是，基于扩散先验的 **GVM**（CVPR 2024）尽管使用了 Stable Video Diffusion 预训练，仍在所有指标上弱于纯 CNN 架构的 MatAnyone 2；而 **MaGGIe** 需要逐帧实例掩膜作为引导，MatAnyone 2 仅需首帧掩膜即可全面超越。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons on different video matting benchmarks from diverse sources. The best and second-best performances are marked in red and orange , respectively. ∗ indicates that GVM [5] is a diffusion-based video matting method that leverages rich Stable Video Diffusion [1] priors, while our method is purely CNN-based. † indicates that MaGGIe [9] requires the instance mask as guidance for each frame, while our method only requires it in the first frame*

在真实视频数据集 CRGNN（每 10 帧人工标注一次，Table 2）上，MatAnyone 2 的 MAD 从 MatAnyone 的 5.76 大幅降至 4.24，Grad 从 15.55 降至 11.74，分别提升 26.4% 和 24.5%，验证了方法在真实场景下的语义精度与边界保真度优势。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/010_Table_2.jpg]]
*Table 2: Quantitative comparisons on the CRGNN real-world dataset [35], where ground-truth alpha mattes are manually annotated every 10 frames on 19 videos. The best and second performances are marked in red and orange , respectively*

### 消融实验：三大模块的贡献

Table 3 在 YouTubeMatte 1080p 上系统拆解了各模块的增益：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/012_Table_3.jpg]]
*Table 3: Ablation study of online guidance*

- **(a) → (b) 引入 MQE 在线引导损失 L_eval**：MAD 从 1.99 降至 1.90，Grad 从 8.91 降至 8.20，dtSSD 也有改善。这表明 MQE 提供的像素级错误概率惩罚比 MatAnyone 中原有的弱无监督损失更有效地约束了边界区域。
- **(b) → (c) 进一步使用 VMReal 数据集训练**：MAD 降至 1.76，Grad 降至 7.65，dtSSD 明显下降。大规模真实数据（28K 片段、2.4M 帧，约为此前最大合成数据集的 35 倍）带来了细节和时序稳定性的显著增益。
- **(c) → (d) 加入参考帧训练策略**：MAD 降至 1.61，Grad 降至 7.13，达到最优。参考帧策略通过引入长程记忆和随机遮挡增强，使模型能处理长视频中未见区域的外观突变，且不增加显存负担。

三个模块互补叠加，证明了 MQE 引导、真实数据规模和长程时序建模各自的不可替代性。

### 失败模式与局限

当前自动标注流水线的质量受限于所使用的图像和视频抠图模型的上限——MQE 虽能识别并融合双分支的优势区域，但若两个分支在相同区域均出错，标注 α 遮罩仍会继承错误。此外，论文指出可进一步构建“数据-模型精炼飞轮”以迭代提升数据集和模型质量，但该闭环需要大量工程与计算资源，本文尚未实施。

### 关键图表结论

- **Figure 6**（真实视频定性对比）：在风动头发、复杂光照等挑战场景下，MatAnyone 2 相比 RVM、GVM 和 MatAnyone 在细节提取和语义准确性上均有显著优势，避免了分割式粗糙边界和扩散方法常见的模糊过渡。
- **Figure 7**（参考帧策略有效性）：MatAnyone 在长视频中新出现的主体区域容易失效，而 MatAnyone 2 通过参考帧训练策略能够稳健地识别这些区域。
- **Table 4**（数据集规模对比）：VMReal 是首个大规模真实视频抠图数据集，其片段数和总帧数远超现有合成数据集，且输入帧来自真实视频而非前景-背景合成，为训练提供了更贴近实际分布的监督信号。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparisons on real-world videos. Our MatAnyone 2 significantly outperforms leading auxiliary-free (RVM [20]), diffusion-based (GVM [5]), and mask-guided (MatAnyone [42]) approaches in both detail extraction and semantic accuracy under challenging conditions, e.g., wind-blown hair (first row) and complex lighting scenes (last two rows)*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/011_Figure_7.jpg]]
*Figure 7: Effectiveness of the reference-frame strategy. MatAnyone [42] struggles with newly appearing subject regions in long videos, whereas MatAnyone 2, trained with the reference-frame strategy, robustly identifies them*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/013_Table_4.jpg]]
*Table 4: Comparison on Datasets. We compare existing video matting (VM) datasets for training, in terms of the number of video clips, the number of total frames, and whether the input frames are synthesized (foreground-background composition) or from real videos. Whereas prior datasets such as VM108 [50], VideoMatte240K [19], VM800 [42], and SynHairMan [5] are relatively small in scale and are purely synthetic composites of foregrounds and backgrounds, VMReal comprises 28K real-world video clips with a total of 2.4M frames*

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2512_11782/figures/001_Figure_1.jpg]]
*Figure 1: (a) Our MatAnyone 2 significantly outperforms MatAnyone [42] in preserving fine details and avoiding segmentation-like boundaries, while also showing enhanced robustness under challenging lighting conditions, e.g., backlit scenes. (b) As a diffusion-based video matting method, GVM [5] often produces blurry alpha mattes with unnatural transitions along object boundaries, e.g., hair strands. In contrast, MatAnyone 2 generates clear, high-quality alpha mattes with natural boundary details. (Zoom-in for best view)*

## 方法谱系与知识库定位

### 1. 问题瓶颈与核心洞察

现有视频抠图方法面临一个根本性瓶颈：**训练数据规模小且均为合成数据，缺乏真实边界监督**。这导致模型在边界区域丢失细节、在语义区域产生错误，最终退化为类似分割的粗糙掩膜。MatAnyone 试图通过分割-抠图联合训练来缓解这一问题，但分割掩膜仅能提供非边界区域的可靠语义标签，边界监督仍依赖弱无监督损失，信号强度与稳定性不足。

MatAnyone 2 的核心洞察在于：**一个学习到的像素级抠图质量评估器（MQE）可以在没有真实 α 遮罩的情况下，准确评估预测遮罩的可靠性**。MQE 利用分割掩膜继承非边界区域的语义真值，并结合 DINOv3 编码器感知边界细节，从而为边界和语义区域同时提供有效监督。这一能力使得两个关键突破成为可能：(1) 在线训练中提供比弱无监督损失更强的边界引导信号；(2) 离线自动构建大规模真实视频抠图数据集 VMReal（约 28K 片段、2.4M 帧，约为此前最大合成数据集的 35 倍）。

### 2. 在视频抠图谱系中的定位

视频抠图方法可大致分为三类，MatAnyone 2 在每一类中都展现出结构性优势：

**Auxiliary-free 方法**（无需额外引导输入，仅依赖 RGB 帧）：
- **MODNet**、**RVM**、**RVM-Large** 等方法在语义精度和细节保留上均弱于 MatAnyone 2，根本原因在于缺乏对边界区域的显式监督机制。
- **GVM**（CVPR 2024）作为基于扩散的 auxiliary-free 方法，虽然利用了 Stable Video Diffusion 的强先验，但仍产生模糊的 α 遮罩，边界过渡不自然（见 Figure 1(b)）。MatAnyone 2 以纯 CNN 架构在所有指标上超越 GVM，说明**数据质量与针对性监督比模型容量和预训练先验更为关键**。

**Mask-guided 方法**（需要分割掩膜作为引导）：
- **AdaM**、**FTP-VM** 等方法依赖掩膜引导，但缺乏对掩膜本身质量的评估能力。
- **MaGGIe** 需要每帧提供实例掩膜，而 MatAnyone 2 仅需首帧掩膜，输入要求更宽松，却取得了更优性能，说明 MQE 驱动的训练策略能更高效地利用有限的引导信息。
- **MatAnyone** 是本文的直接基线，其分割-抠图联合训练范式为 MatAnyone 2 提供了起点。MatAnyone 2 在此基础上做出了三个关键改进（见第 3 节）。

### 3. 关键改进槽位

| 改进槽位 | MatAnyone 基线 | MatAnyone 2 方案 | 证据强度 |
|---------|---------------|-----------------|---------|
| 边界监督信号 | 弱无监督损失（依赖图像先验） | 学习到的 MQE 在线引导损失 $\mathcal{L}_{eval} = \| P_{eval}^{(0)} \|_1$，提供像素级错误概率惩罚 | 强：Table 3(a)→(b)，MAD 从 1.99 降至 1.90，Grad 从 8.91 降至 8.20 |
| 训练数据 | 合成抠图数据 + 分割数据联合训练 | 统一使用 VMReal 真实视频抠图数据集（自动标注的 α 遮罩 + 可靠性图），仅在高置信度区域（$M^{eval}=1$）计算损失 | 强：Table 3(b)→(c)，MAD 进一步降至 1.76，Grad 降至 7.65，dtSSD 明显改善 |
| 长视频建模 | 仅在局部训练窗口（8 帧）内传播记忆 | 参考帧训练策略，从序列前部采样数帧作为额外记忆，结合随机丢弃增强，无需增加显存 | 强：Figure 7 定性展示对未见区域的鲁棒性；Table 3(c)→(d) 全组件启用后达到最优 |

这三个改进槽位存在互补关系：MQE 在线引导提供即时的边界反馈，VMReal 数据集提供大规模真实场景的多样性，参考帧策略则扩展了时序上下文。消融实验（Table 3）证实，全部组件启用后达到最优 MAD 1.61、Grad 7.13（YouTubeMatte 1080p）。

### 4. 流水线模块与公式支撑

MatAnyone 2 的核心流水线由以下模块构成：

1. **Matting Quality Evaluator (MQE)**：接收三元组 $(I_{rgb}, \hat{\alpha}, M^{seg})$，输出二元评估图 $M^{eval} \in \{0,1\}^{H \times W}$，标定可靠与错误像素。训练时使用 focal loss 处理类别不平衡。

2. **在线引导损失**：$\mathcal{L}_{eval} = \| P_{eval}^{(0)} \|_1$，对 MQE 预测的错误概率图取 L1 范数，推动网络降低错误区域的置信度。

3. **双分支标注流水线**：视频抠图分支（$B_V$）提供时序稳定的语义，图像抠图分支（$B_I$）提供精细边界。MQE 作为质量仲裁器，通过融合掩膜 $M^{fuse} = M_I^{eval} \odot (1 - M_V^{eval})$ 选择性引入边界细节，生成标注用 α 遮罩：$\alpha = \alpha_V \odot (1 - M^{fuse}) + \alpha_I \odot M^{fuse}$。

4. **参考帧训练策略**：从序列前部采样长程参考帧作为额外记忆，结合随机遮挡增强（random dropout augmentation），在不增加显存负担的前提下覆盖长视频中的外观突变。

5. **整体训练损失**：$\mathcal{L}_{mat}^{total} = \mathcal{L}_{mat}^{M} + 0.1 \mathcal{L}_{eval}$，其中 $\mathcal{L}_{mat}^{M}$ 为仅在 $M^{eval}=1$ 区域计算的遮罩化 L1 损失。

### 5. 适用边界与局限

**适用边界**：
- 当前方法主要针对**人像视频抠图**场景设计和验证，MQE 的训练和 VMReal 数据集的构建均以人像为主。
- 自动标注流水线的质量上限受限于所使用的图像抠图模型和视频抠图模型的性能，可能继承其错误。
- 参考帧策略在极长视频（如数十分钟）上的性能退化与计算成本权衡尚未充分探索。

**已知局限**：
- 论文明确指出，进一步的闭环"数据-模型精炼飞轮"虽能迭代提升数据集质量和模型效果，但需要大量工程投入和计算资源，本文未实施。
- MQE 的评估能力在非人像视频、多目标场景或特殊透明物体上的泛化能力仍是一个开放问题。

### 6. 开放问题

1. **迭代精炼飞轮**：能否将双分支标注升级为迭代精炼过程，由更强的抠图模型不断改善 α 标注，形成一个正反馈循环？这需要解决标注质量评估、模型更新策略和计算成本控制等多个工程挑战。

2. **跨域泛化**：MQE 在非人像视频（如动物、车辆）、多目标场景或半透明物体上的泛化能力如何？当前 MQE 的训练依赖于人像分割掩膜提供的语义真值，扩展到其他域可能需要重新设计语义监督来源。

3. **极长视频建模**：参考帧策略对极长视频的潜在性能退化与计算成本如何权衡？是否需要引入层次化记忆机制或自适应参考帧选择策略？

4. **与基础模型的融合**：当前 MatAnyone 2 采用纯 CNN 架构，而 GVM 等扩散方法虽然边界质量不佳，但展现了基础模型先验的潜力。如何在保持细节精度的前提下，将 MQE 引导的训练范式与更大规模的基础模型相结合，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/MatAnyone_2_Scaling_Video_Matting_via_a_Learned_Quality_Evaluator.pdf]]
