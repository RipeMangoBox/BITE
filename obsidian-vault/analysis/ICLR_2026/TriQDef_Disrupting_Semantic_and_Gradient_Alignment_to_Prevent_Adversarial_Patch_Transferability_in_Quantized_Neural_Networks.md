---
title: "TriQDef: Disrupting Semantic and Gradient Alignment to Prevent Adversarial Patch Transferability in Quantized Neural Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TriQDef_Disrupting_Semantic_and_Gradient_Alignment_to_Prevent_Adversarial_Patch_Transferability_in_Quantized_Neural_Networks.pdf
aliases:
- TriQDef
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "通过引入特征不对齐惩罚（FDP）和梯度感知不协调惩罚（GPDP），在训练时主动破坏中间特征图和输入梯度在不同量化级别之间的边缘结构和纹理相似性，并配合比特宽度感知的课程训练（BACT）稳定优化，从而切断补丁的跨比特迁移路径。"
primary_logic: "对抗性补丁的可迁移性不仅源于梯度方向的相似性，更重要的是跨比特模型在感知结构层面的对齐——低水平的梯度方向余弦相似度掩盖了高水平的边缘和纹理相似性，而这些结构性感知对齐才是补丁迁移的真正推手。"
claims:
- "在高比特宽度生成的补丁可以成功迁移到2比特量化模型，例如LAVAN在ResNet-56 2位上仍保持73.08%的攻击成功率（ASR）。"
- "基于补丁的对抗训练（PBAT）在面对未见过的补丁比特宽度时泛化能力差，例如在QAT 2位未见补丁上ASR高达78.34%，远高于可见补丁。"
- "尽管跨比特模型之间的梯度方向余弦相似度很低（例如fp↔5b为0.05），但梯度图的感知结构相似度（HOG余弦）却很高（0.81），揭示了隐藏的迁移脆弱性。"
- "TriQDef在CIFAR-10上将GAP攻击的ASR从PBAT的37.9%降至17.2%（2比特），并且在未见补丁设置下将ASR从75.3%降至32.5%。"
---

# TriQDef: Disrupting Semantic and Gradient Alignment to Prevent Adversarial Patch Transferability in Quantized Neural Networks

> [!tip] 核心洞察
> 对抗性补丁的可迁移性不仅源于梯度方向的相似性，更重要的是跨比特模型在感知结构层面的对齐——低水平的梯度方向余弦相似度掩盖了高水平的边缘和纹理相似性，而这些结构性感知对齐才是补丁迁移的真正推手。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TriQDef：破坏语义与梯度对齐以防御量化神经网络中对抗性补丁的可迁移性 |
| 英文题名 | TriQDef: Disrupting Semantic and Gradient Alignment to Prevent Adversarial Patch Transferability in Quantized Neural Networks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=acQP99PU8y) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | TriQDef |
| Dataset | CIFAR-10 (ResNet-56), ImageNet (ResNet-50) |

> [!tip] 效果简介
> - CIFAR-10 (ResNet-56) 上，ASR (LAVAN, 6x6 patch, 2-bit) 为 17.2%，对比 37.9% (PBAT)，变化 -20.7%。
> - CIFAR-10 (ResNet-56) 上，ASR (GAP, unseen patches, 32-bit) 为 32.5%，对比 75.3% (PBAT)，变化 -42.8%。
> - ImageNet (ResNet-50) 上，Robust Accuracy (LA-VAN, 32-bit) 为 78.3%，对比 ~40-45% (PBAT/PBCAT/DiffPure/JEDI)，变化 >30% improvement。

## 概述

对抗性补丁对量化神经网络（QNN）构成严重威胁：即使模型被量化至极低比特宽度，在不同量化级别上生成的补丁仍能保持高攻击成功率（例如 LAVAN 在 2 比特 ResNet-56 上攻击成功率达 73.08%）。现有防御方法（如基于补丁的对抗训练 PBAT）仅在训练时见过的补丁配置下有效，一旦补丁的量化比特宽度或尺寸未被见过，攻击成功率便急剧上升（如在 QAT 2 比特未见补丁上 ASR 高达 78.34%），暴露出极度脆弱的泛化能力。根本原因并非简单的梯度方向对齐——跨比特模型之间的梯度余弦相似度极低（fp ↔ 5b 仅 0.05），但梯度图中的边缘结构（Edge IoU）和纹理方向（HOG 余弦相似度）在感知层面仍保持高度一致（fp ↔ 5b 的 HOG 余弦相似度达 0.81），这种隐藏的语义与梯度感知结构对齐才是补丁跨比特迁移的真正推手。

针对这一瓶颈，TriQDef 提出一种训练阶段的防御框架，通过主动破坏跨比特感知对齐来阻断补丁迁移路径。方法的核心包含三项互补设计：**特征不对齐惩罚（FDP）** 在中间特征图层面计算不同比特宽度分支之间的边缘结构和纹理相似性，并以可微分方式（SoftDice + SoftHOG）强制它们分叉；**梯度感知不协调惩罚（GPDP）** 在对抗输入上直接惩罚不同比特宽度输入梯度的结构重叠与方向纹理一致性；**比特宽度感知课程训练（BACT）** 则从高精度开始逐步激活低比特量化器，稳定多分支联合优化。整个框架使用一个共享骨干网络搭配多个可切换的比特宽度特定量化模块，训练时引入 1.47–1.60 倍的额外墙钟时间，但推理阶段完全无额外开销，相比基于预处理的后验防御（如 DiffPure 需数秒延迟）更具部署优势。

实验结果表明，TriQDef 在保持干净精度竞争力的前提下，大幅提升了跨比特、跨配置的鲁棒性。在 CIFAR‑10 上，它将 GAP 攻击在 2 比特下的 ASR 从 PBAT 的 37.9% 压缩至 17.2%，在未见补丁设置下 32 比特的 ASR 由 75.3% 骤降至 32.5%；在 ImageNet 上，2 比特量化时的鲁棒准确率从基线方法的不足 40% 提升至 65.8%，32 比特时更达 78.3%。消融实验证实 FDP 与 GPDP 各自独立且互补地贡献了防御性能，且方法在一系列主流架构（VGG、ResNet、MobileNetV2、DenseNet 等）和多种攻击形态（LAVAN、GAP、PatchAttack、DRP）下均表现出一致的有效性，避免了过度定制。

## 背景与动机

对抗性补丁通过将精心构造的局部扰动粘贴到输入图像上，可在不改变图像全局语义的前提下诱导模型误分类，对安全关键场景构成严重威胁。随着深度神经网络在资源受限设备上的部署需求日益增长，量化（将权重和激活从32位浮点降至低比特整数）已成为标配压缩手段。然而，量化是否天然能遏制补丁攻击的迁移，始终缺乏系统分析。现有认知倾向于认为量化引入的离散化噪声会破坏补丁的泛化能力，因此低成本量化可成为一种隐式防御。真实情况却恰恰相反：补丁在跨比特宽度模型中展现出惊人的可迁移性，而现有防御在面对多精度部署出现的**未见补丁变体**时，鲁棒性急剧崩塌。

以CIFAR-10上的实验为例（Table 1），LAVAN攻击从全精度模型迁移到QAT训练的2比特ResNet-56时，攻击成功率（ASR）仍高达73.08%。即便采用旨在消除补丁的补丁对抗训练（PBAT），其获得的防御高度依赖于训练时所见补丁的比特宽度（Table 2）：当面对2比特量化模型上训练中未见过的补丁尺寸时，ASR从可见补丁的57.86%飙升至78.34%。这表明，PBAT仅习得了对固定补丁模式的过拟合，未能破坏支撑跨比特迁移的根本机制。

对这一现象的进一步拆解揭示了问题的核心瓶颈：**补丁的可迁移性并非主要源于不同比特模型之间的梯度方向一致性，而是源于它们在感知结构层面持久的高对齐。** 如表3所示，全精度与5比特模型之间输入梯度的余弦相似度仅0.05，但梯度图的HOG余弦相似度高达0.81，边缘交并比（Edge IoU）亦保持可观水平。这意味着，尽管离散化显著偏转了梯度方向，其空间结构——边缘位置、纹理走向——却几乎未受影响。当攻击者基于全精度模型计算梯度时，捕获的正是这种跨比特稳定的感知模式，从而使补丁能够无视量化差异而迁移。图2进一步可视化了该现象：从浮点到2比特，中间特征图的Edge IoU与HOG余弦相似性在多层网络中保持高热力值，在对抗输入下亦未消解。

这一发现表明，仅依赖传统的梯度混淆或像素级对抗训练已不足以防御补丁迁移，因为攻击信号牢固嵌入在深层特征的**边缘和纹理结构**之中。现有缺口可归纳为两点：（1）以PBAT为代表的补丁特化防御无法泛化到未见比特宽度或补丁配置，因为它们只压低了特定模式下的损失，而未切断感知层面的对齐通路；（2）量化自身虽然压制了梯度方向相似度，但这一压制是“对表面现象的掩盖”，竟让高水平的感知结构相似性更加隐蔽地存续，形成一种**隐藏的迁移脆弱性**。

由此，我们需要一种全新的防御思路：**主动破坏跨比特模型在中间特征和输入梯度上的感知结构对齐**，从根源上让不同精度的推理过程对同一输入产生分叉的敏感区域，使攻击者无法通过单一代理模型构造出泛化到目标模型的补丁。这正是TriQDef的设计动机——通过**特征失配惩罚（FDP）**强制不同精度模型在同一输入下呈现迥异的边缘和纹理表示，同时借助**梯度感知不协调惩罚（GPDP）**扰动梯度图的空间结构，从而切断补丁的跨比特迁移路径。

## 核心创新

TriQDef 的核心突破在于首次揭示并切断了量化神经网络（QNN）跨比特宽度的**感知结构对齐**这一补丁可迁移性的隐性通道。现有防御（如 PBAT）仅仅在输入–输出梯度方向上对抗扰动，却忽略了如下关键事实：尽管不同比特模型之间的梯度余弦相似度极低（fp↔5b 仅为 0.05），其梯度图的**边缘结构**（Edge IoU）和**纹理方向**（HOG 余弦）仍保持高度一致（HOG 余弦达 0.81，Table 3）。这种隐蔽的感知共识才是对抗补丁从全精度向低比特成功迁移（ASR 仍 >73%，Table 1）的根本推手。针对这一机理缺陷，TriQDef 引入了三个相互协同的创新模块，从特征表示、梯度信号和训练调度三个层面主动制造“分叉”，使跨比特模型在感知结构上不再对齐，从而系统性地阻断迁移路径。

**1. 特征不对齐惩罚（Feature Disalignment Penalty，FDP）**  
在中间卷积层上，FDP 通过可微分的**软边缘二值化 SoftDice 和可微 HOG 描述器**，直接度量并惩罚不同比特宽度特征图之间的边缘结构相似性与纹理相似性（Eq. 2, Section 3.2）。与以往单纯约束分类 logits 或梯度方向的防御不同，FDP 从**内部表示**层面强制语义分叉——SoftDice 对边缘掩膜的惩罚鼓励模型的边缘关注区域随比特变化而位移，HOG 惩罚则打破纹理一致性。这一设计等价于在特征空间施加对比损失，破坏“相似表示导致相似决策”的迁移前提（Appendix B.1）。实验表明，移除 FDP 会使 2-bit 下的 ASR 从 26.2% 飙升至 55.9%（Table 7），验证了特征分叉的决定性作用。

**2. 梯度感知不协调惩罚（Gradient Perceptual Dissonance Penalty，GPDP）**  
FDP 仅作用于特征层，并未显式约束输入梯度。GPDP 则在对抗输入上，直接对**不同比特模型的输入梯度图**施加与 FDP 同构的感知惩罚：利用 Sobel 边缘的 SoftDice 和 SoftHOG 的余弦相似性，强制梯度在空间结构和纹理上的差异（Section 3.3）。这弥补了 FDP 在梯度层面的缺口，两者形成“特征–梯度”双杀防线。移除 GPDP 会使 ASR 上升超过 10 个百分点（Table 7），且 GPDP 仅在对抗样本上计算，不影响清洁准确率。

**3. 比特宽度感知课程训练（Bit-width-Aware Curriculum Training，BACT）**  
不同于固定单比特或同时训练所有量化器的方式，BACT 采用**从高到低的课程式调度**：训练初期仅激活 32/8-bit 量化器，随后逐步激活 5/4/2-bit 量化器（Section 3.4, Figure 1）。这使得低比特量化器能在高比特特征已有一定“分叉”的基础上进一步优化，避免了同时训练多分支可能引起的梯度冲突与不稳定。BACT 与 FDP/GPDP 配合，在仅带来 1.47–1.60 倍训练时间和 1.17–1.23 倍显存开销的情况下，实现了在 2-bit 极端量化下清洁准确率几乎无损（Table 4）。

**与基线方法的根本差异**  
PBAT 等基于补丁的对抗训练仅在单一比特宽度或全精度模型上生成补丁进行训练，导致对未见补丁比特宽度的泛化极度脆弱（ASR 从 ~40% 跃升至 78.34%，Table 2）。TriQDef 则**不绑定任何特定补丁比特宽度**，通过迫使不同量化模型表征的持续失配，从根本上提升跨比特防御的泛化性——在未见补丁设置下，CIFAR‑10 上 GAP 攻击的 ASR 从 PBAT 的 75.3% 降至 32.5%，在 2‑bit 下进一步降至 17.2%（Table 5）。在更大规模的 ImageNet 上，TriQDef 在 2‑bit 下的鲁棒准确率仍保持 65.8%，远超 PBAT（<40%）及推理时预处理防御（如 DiffPure 的数秒级延迟），同时**推理阶段零额外开销**（Table 6, Table 18）。消融与可视化（Figure 3）进一步证实，FDP/GPDP 未引入语义漂移，模型注意力始终聚焦于正确语义区域。

综上，TriQDef 的 changed slots 可归纳为：(i) 训练目标函数从单一的交叉熵扩展为包含 FDP 与 GPDP 的感知失配复合损失；(ii) 训练调度从固定比特宽度转变为 BACT 课程式激活多量化器。二者共同实现了从被动抗补丁到主动破坏跨比特感知共识的范式转换。

## 整体框架

![[assets/figures/papers/iclr26_0013_acQP99PU8y_TriQDef_Disrupting_Semantic_and_Gradient_Alignme/figures/003_Figure_1.jpg]]
*Figure 1: TriQDef overview. A single shared backbone θ is paired with multiple quantizers $\{ Q _ { b } \}$ (e.g., 32/8/2-bit). Clean and adversarial inputs produce bit-specific views whose intermediate features (for $L _ { \mathrm { F D P } }$ ) and input gradients (for $L _ { \mathrm { G P D P } }$ ) are contrasted across bit-widths. Losses are aggregated into $L _ { \mathrm { t o t a l } }$ and used to update θ and $\{ Q _ { b } \}$ under a BACT schedule. Inference uses a single forward pass with the deployed $Q _ { b }$ (no runtime overhead)

TriQDef的核心设计目标是通过在训练阶段主动打破不同量化比特宽度之间内部特征与输入梯度的感知结构对齐，从而切断对抗性补丁的跨比特迁移通道。该框架围绕三个互补组件构建：**特征不对齐惩罚（FDP）**、**梯度感知不协调惩罚（GPDP）**，以及**比特宽度感知的课程训练调度（BACT）**。三者共同作用于一个**共享骨干网络搭配可切换量化器**的架构之上，形成统一的训练时防御（Figure 1；Section 3.1）。

**架构与多视图生成**  
TriQDef使用一个参数为 \theta 的共享骨干网络，并在标准量化节点处插入一组比特宽度特定的量化模块 \{Q_b\}（例如 32/8/5/4/2 比特）。一次前向传播中，根据当前激活的比特宽度集合 \mathcal{B}，同一输入（干净或对抗）会生成多个比特特定的特征视图 \smash{f_{b}^{(l)}(x)} 及对应的 logits。这种设计允许以极小的参数增量（仅量化器参数）获取跨精度表示，且推理时仅需加载单一量化器，实现**零额外部署开销**（Section 3.4；Table 18）。

**训练流水线**  
每一次训练迭代的完整数据流如下：

1. **补丁生成**：使用离线对抗补丁池或在线 EOT（期望变换）方式，从全精度模型上产生补丁 P，并以随机位置和几何抖动应用于输入，得到对抗样本 x_{\text{adv}}（Section 3 页；Patch generation）。  
2. **多视图前向**：将 x_{\text{adv}}（以及干净样本）同时送入共享骨干及所有激活的量化器，得到各比特宽度下的中间特征图与分类 logits（Figure 1 左侧流）。  
3. **特征不对齐损失 \mathcal{L}_{\text{FDP}}**：在选定的早期‑中层卷积层上，对不同比特宽度特征图计算基于 SoftDice（边缘结构）和 SoftHOG（纹理方向）的感知相似度，并作为惩罚项加入总损失，强迫特征表示分叉（Eq. 2；Section 3.2）。  
4. **梯度感知不协调损失 \mathcal{L}_{\text{GPDP}}**：对每个比特宽度模型计算输入 x_{\text{adv}} 的梯度 \smash{\nabla_x^{b}}，而后在不同比特宽度之间计算其 Sobel 边缘的 SoftDice 以及 SoftHOG 余弦相似度，惩罚这些梯度图的感知一致性（Section 3.3；GPDP formulation）。  
5. **总损失与参数更新**：总损失为  
   \mathcal{L}_{\text{total}} = \mathcal{L}_{\text{CE}} + \lambda_{\text{FDP}} \mathcal{L}_{\text{FDP}} + \lambda_{\text{GPDP}} \mathcal{L}_{\text{GPDP}}，  
   其中 \mathcal{L}_{\text{CE}} 为标准分类损失。反向传播同时更新骨干参数 \theta 和活跃量化器参数（Section 3.1）。  
6. **BACT 调度**：训练过程中，BACT 调度器控制量化器的激活时序——从高精度（如 32 位）开始，逐步引入更低比特的量化器，使模型在稳定阶段逐步面对更剧烈的不对齐惩罚，避免训练初期崩溃（Section 3.4）。

**FDP 与 GPDP 的协同机制**  
FDP 直接作用于**特征空间**，破坏中间层表示在不同比特宽度间的边缘结构和纹理相似性（即图中 L_{\text{FDP}} 分支），从感知层面消除补丁可迁移的结构基础。GPDP 则作用于**梯度空间**，通过惩罚输入梯度的感知对齐（边缘 IoU 与 HOG 纹理一致性）进一步施加干扰，弥补单纯依靠梯度方向余弦相似度无法捕捉的高阶结构脆弱性（Section 3.3；Table 3）。两者结合，形成特征‑梯度双层的语义与感知不对齐，使得在一个比特宽度上精心制作的补丁在其他量化模型上不再保持相同的误导能力。

**推理流程**  
训练完成后，对于任意部署的比特宽度 b，仅需加载对应的量化器 Q_b，执行一次标准前向传播即可得到预测结果，无需任何额外的预处理或梯度计算（Figure 1 右下推理分支；Section 4.4）。这相比 DiffPure 等需要数秒级扩散纯化、或 Jedi 需要额外内存的推理时防御，具有明确的实用性优势（Table 18）。

**关键设计选择**  
- 共享骨干保证不同比特宽度模型的底层特征迁移性不会被独立参数抵消，从而让 FDP/GPDP 能够直接针对跨精度对齐的根本原因施加惩罚。  
- 采用软二值化（SoftDice）与可微分 HOG 使整个训练流保持端到端可导，避免硬指标（如原始 Edge IoU）的不可微问题（Section 3.2；Appendix C.1）。  
- 损失仅施加在对抗输入上（GPDP 仅针对 x_{\text{adv}}），以保护干净精度不受损害（Section 3.3）。  
- BACT 课程训练解决了在极低比特（如 2 位）上直接施加强烈不对齐惩罚可能导致的优化困难，使防御效果与模型精度得以平衡（Section 3.4）。

综上，TriQDef 的 pipeline 以**共享主干 + 多量化器**为硬件基础，以**FDP 破坏特征对齐**、**GPDP 破坏梯度感知对齐**为防御机制，以**BACT 课程调度**为训练策略，构建起一套训练时完全可见、但推理时零开销的量化鲁棒防御体系。

## 核心模块与公式推导

TriQDef 通过训练时引入跨比特宽度的**感知结构失配惩罚**，从特征表示和输入梯度两个层面切断对抗性补丁的迁移路径，其综合训练目标为  

$$
\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{CE}} + \lambda_{\text{FDP}} \cdot \mathcal{L}_{\text{FDP}} + \lambda_{\text{GPDP}} \cdot \mathcal{L}_{\text{GPDP}}
$$

其中 $\mathcal{L}_{\text{CE}}$ 为标准分类交叉熵，$\mathcal{L}_{\text{FDP}}$ 与 $\mathcal{L}_{\text{GPDP}}$ 分别对应下述核心模块，$\lambda_{\text{FDP}},\lambda_{\text{GPDP}}$ 为平衡系数（实验中常用 0.8 与 0.5，参见 Table 13）。

### 1. 共享骨干、可切换量化器与课程调度 (BACT)
TriQDef 使用单一骨干网络 $\theta$ 搭配一组比特宽度特定的量化模块 $\{Q_b\}$（例如 32/8/2 比特）。前向传播时，按活跃比特集合 $\mathcal{B}$ 生成对应的量化视图。训练采用**比特宽度感知的课程训练 (BACT)**：从高精度开始，逐渐激活更低比特的量化器，损失仅在活跃比特上计算。这种调度稳定了低比特的优化过程，并使 FDP 和 GPDP 的跨比特比较始终在一致的参数空间内进行。

### 2. 特征不对齐惩罚 (FDP)
分析表明，跨比特模型在中间特征图上保持较高的感知结构对齐（高 Edge IoU 和 HOG 余弦相似度），这是补丁迁移的关键瓶颈。FDP 通过显式惩罚不同量化级别特征图之间的边缘结构和纹理相似性，迫使语义表示产生分化。其可微分形式为

$$
\mathcal{L}_{\mathrm{FDP}} = \sum_{l \in \mathcal{L}} \sum_{\substack{b_i, b_j \in \mathcal{B} \\ b_i \neq b_j}} 
\Big[ \alpha \cdot \mathrm{SoftDice} \big( S( E ( f_{b_i}^{(l)}(x_{\mathrm{adv}}) ) ),\, S( E ( f_{b_j}^{(l)}(x_{\mathrm{adv}}) ) ) \big) 
+ \beta \cdot \cos \big( H( f_{b_i}^{(l)}(x_{\mathrm{adv}}) ),\, H( f_{b_j}^{(l)}(x_{\mathrm{adv}}) ) \big) \Big] ,
$$

其中  

- $\mathcal{L}$：选定的中间层集合（以捕捉早期到中期的结构信息）；  
- $f_{b}^{(l)}(x_{\mathrm{adv}})$：在比特宽度 $b$ 下第 $l$ 层的特征图（输入为对抗样本 $x_{\mathrm{adv}}$）；  
- $E(\cdot)$：Sobel 边缘检测算子；  
- $S(A;\tau,k) = \sigma\big(k \cdot (A - \tau)\big)$：基于分位数的软二值化函数，将边缘幅度转为软掩膜。$\tau = \text{quantile}(A, q{=}85)$，锐度 $k{=}100$，$\sigma$ 为 sigmoid；  
- $\mathrm{SoftDice}$：散料 Dice 系数，衡量软掩膜间的空间重叠；  
- $H(\cdot)$：可微分 HOG 描述子，捕获纹理方向统计；  
- $\cos$：余弦相似度，量化纹理一致性；  
- $\alpha, \beta$：边缘结构项与纹理项的相对权重。

该损失作用于对抗输入，强制不同比特宽度的特征图在边缘位置和梯度直方图上尽可能不相似，从根源上破坏特征层的跨比特对齐。

### 3. 梯度感知不协调惩罚 (GPDP)
尽管不同比特模型之间的输入梯度方向余弦相似度极低（如 fp↔5 bit 仅为 0.05），但梯度图的感知结构指标（Edge IoU 与 HOG 余弦）仍保持高度一致（HOG 余弦达 0.81，Table 3），这为补丁迁移提供了隐藏通路——可迁移性不仅取决于方向，更依赖空间结构和纹理层面的感知共识：

$$
\mathcal{T}(b_i \to b_j) \propto
\underbrace{\cos(\nabla_x^{b_i}, \nabla_x^{b_j})}_{\text{directional}}
+ \underbrace{\mathrm{EdgeIoU}(\nabla_x^{b_i}, \nabla_x^{b_j})}_{\text{spatial structure}}
+ \underbrace{\cos(\mathrm{HOG}(\nabla_x^{b_i}), \mathrm{HOG}(\nabla_x^{b_j}))}_{\text{textural similarity}} .
$$

GPDP 直接针对此瓶颈，惩罚不同量化模型对输入梯度的结构‑纹理相似性：

$$
\mathcal{L}_{\mathrm{GPDP}} = \sum_{b_i, b_j \in \mathcal{B},\, b_i \neq b_j} 
\Big[ \alpha \cdot \mathrm{SoftDice}\big(\mathrm{Sobel}(\nabla_x^{b_i}), \mathrm{Sobel}(\nabla_x^{b_j})\big)
+ \beta \cdot \cos\big(\mathrm{SoftHOG}(\nabla_x^{b_i}), \mathrm{SoftHOG}(\nabla_x^{b_j})\big) \Big] .
$$

变量说明：  

- $\nabla_x^{b}$：比特宽度 $b$ 模型对对抗输入 $x$ 的梯度图；  
- $\mathrm{Sobel}$：对梯度图施加的 Sobel 边缘检测；  
- $\mathrm{SoftDice}$：量化边缘图之间的结构重叠；  
- $\mathrm{SoftHOG}$：对梯度方向场提取的软 HOG 特征；  
- $\cos$：纹理层面的余弦相似度。

GPDP 仅在对抗样本上计算，因此不侵蚀洁净准确率。它与 FDP 形成互补——FDP 在特征空间打破语义连贯性，GPDP 在梯度空间粉碎感知对齐——从而协同切断补丁的跨比特迁移通路。消融实验显示，移除任一组件都会使攻击成功率急剧上升（Table 7），且 FDP 与 GPDP 各自的贡献在统计上显著且高度互补。

## 实验与分析

### 1. 攻击脆弱性与防御动机实证

隐蔽的结构对齐是量化对抗补丁可迁移性的真正推手。**Table 1** 展示全精度模型生成的 LAVAN 和 GAP 补丁可轻松迁移至极低位宽量化模型：例如 LAVAN 在 2 比特 ResNet-56 上攻击成功率（ASR）仍高达 73.08%，证明量化本身无法阻断补丁的跨比特迁移。基于补丁的对抗训练（PBAT）仅在已知补丁比特宽度下有效，面对未见过的补丁比特宽度时 ASR 急剧反弹——**Table 2** 中 QAT 2 比特未见补丁的 ASR 高达 78.34%，相比可见补丁增加了超过 20 个百分点。这暴露出 PBAT 仅在有限补丁分布上过拟合，无法从根本上消除迁移路径。

![[assets/figures/papers/iclr26_0013_acQP99PU8y_TriQDef_Disrupting_Semantic_and_Gradient_Alignme/figures/001_Table_1.jpg]]
*Table 1: ASR (%) of LAVAN and GAP (6x6 patches) transferred from full-precision models to QAT-trained QNNs on CIFAR-10*

迁移性的内在根源在于跨比特模型在感知结构层面保持高度一致。**Table 3** 和 **Figure 2** 揭示：尽管不同位宽模型间的梯度方向余弦相似度极低（例如 fp↔5b 仅 0.05），但梯度图的 HOG 纹理余弦相似度和边缘 IoU 却远高于随机水平（HOG 余弦 0.81，Edge IoU 0.14）。这种低层方向相似度背后的高层结构对齐，使得补丁攻击者可依赖稳定的边缘和纹理线索，绕过普通的梯度混淆防御。TriQDef 即专为切断这种对齐而设计。

![[assets/figures/papers/iclr26_0013_acQP99PU8y_TriQDef_Disrupting_Semantic_and_Gradient_Alignme/figures/005_Table_3.jpg]]
*Table 3: Gradient similarity across bit-width models using different metrics. Despite low cosine similarity, perceptual metrics (HOG Cosine and Edge IoU) reveal strong structural alignment*

### 2. 主实验结果

#### 清洁准确率保持

**Table 4** 显示，TriQDef 在 CIFAR-10 (ResNet-56) 和 ImageNet (ResNet-34) 上各比特宽度的清洁准确率与标准 QAT 持平或略微下降（例如 32 比特 89.4% vs. QAT 89.4%），远优于 PBAT（88.2%），证明防御训练未损害模型的基本表征能力。

#### 对抗补丁攻击 ASR 对比

**Table 5** 汇总了多种攻击下的 ASR 表现。TriQDef 相比 PBAT 和 DWQ 在可见和不可见补丁设置下均实现大幅降低：
- CIFAR-10 上 GAP 攻击（2 比特）：ASR 从 PBAT 的 37.9% 降至 17.2%（降幅 20.7 pp）。
- 在更严峻的未见补丁设置（32 比特 GAP）下，TriQDef 将 ASR 从 75.3%（PBAT）压制至 32.5%（降幅 42.8 pp）。
- 针对 LAVAN 和 PatchAttack 同样观察到一致的优势，验证了方法对攻击类型的泛化能力。

![[assets/figures/papers/iclr26_0013_acQP99PU8y_TriQDef_Disrupting_Semantic_and_Gradient_Alignme/figures/007_Table_5.jpg]]
*Table 5: ASR (%) under LAVAN (6×6 patches on CIFAR-10, 50×50 patches on ImageNet), GAP, and PatchAttack across bit-widths and patch generalization settings. Lower is better*

#### ImageNet 大规模鲁棒性验证

**Table 6** 展示 ResNet-50 在 ImageNet 上对 LA-VAN 攻击的鲁棒准确率。TriQDef 在 32 比特下达到 78.3%，2 比特下仍保持 65.8%，而 PBAT、DiffPure 等基线在 2 比特时均低于 40%。推理阶段 TriQDef 无额外时间开销（直接部署对应量化器），优于需要数秒预处理时间的 DiffPure（5.58–17.14 s/图），凸显实际部署价值。

![[assets/figures/papers/iclr26_0013_acQP99PU8y_TriQDef_Disrupting_Semantic_and_Gradient_Alignme/figures/008_Table_6.jpg]]
*Table 6: Robust Accuracy (%) under LA-VAN attack on ImageNet (ResNet-50) for different defenses across quantization levels. Higher is better*

### 3. 消融研究

**Table 7** 和 **Table 13** 揭示了各个组件的贡献与互补性。

![[assets/figures/papers/iclr26_0013_acQP99PU8y_TriQDef_Disrupting_Semantic_and_Gradient_Alignme/figures/009_Table_7.jpg]]
*Table 7: Ablation study: ASR (%) of LAVAN attack across bit-widths on CIFAR-10 (ResNet-56) and ImageNet (ResNet-34) under seen and unseen patch settings. Lower is better*

- **FDP 的关键作用**：移除特征不对齐惩罚（FDP）导致 ASR 剧烈上升。在 CIFAR-10 2 比特场景下，ASR 从完整模型的 26.2% 反弹至 55.9%，表明仅靠梯度防御不足以阻断保持结构相似的特征通道。
- **GPDP 的补充效应**：移除梯度感知不协调惩罚使 ASR 上升超过 10 个百分点，证明在梯度层面显式破坏结构和纹理相似性与特征分叉产生正交收益。
- **超参数平衡**：λ_FDP = 0.8、λ_GPDP = 0.5 的组合在清洁准确率与对抗鲁棒性之间取得最佳平衡（**Table 13**），较高权重会轻微牺牲清洁精度。

此外，**Table 12** 定量证实软度量（SoftDice、SoftHOG）与原始硬度量（Edge IoU、HOG Cosine）高度一致（5b↔4b 的 SoftDice 达 0.86），验证了可微近似在训练中的有效性。

### 4. 防御失败模式与局限性

- **PBAT 的泛化失败**：现有补丁对抗训练仅在已见补丁比特宽度上奏效，面对未见的补丁量化等级（如用 8 比特补丁训练却测试 4 比特补丁）时 ASR 骤升，构成严重实际风险。TriQDef 通过破坏跨比特通用特征对齐规避了这一失败模式。
- **TriQDef 的自身局限**：训练期间需同时优化多组量化器，墙钟时间增加 1.47–1.60 倍，峰值 GPU 内存增加 1.17–1.23 倍（**Table 17**），对极端资源受限场景仍有压力。此外，防御依赖全精度模型离线补丁池或在线 EOT 生成，可能无法覆盖未来未知攻击形态；尚未评估专门针对 FDP/GPDP 损失的自适应攻击，且目前仅在分类任务上验证。

### 5. 关键图表结论集成

- **Table 1 + Table 2**：量化本身不加防御，补丁对抗训练泛化性差，构成了 TriQDef 的直接动机。
- **Table 3 + Figure 2**：揭示梯度结构对齐的隐秘性——低余弦掩盖高 HOG 相似度，解释为何攻击迁移不为传统梯度对齐指标所察觉。
- **Figure 3**：Grad-CAM 可视化表明，从全精度到 2 比特，模型一致关注同一语义区域，证明 FDP 未引入语义漂移，防御仅改变补丁的攻击路径而非摧毁模型本质。
- **Table 5–6**：TriQDef 全面压制攻击，尤其在不可见补丁和低位宽下保持明显优势，验证了“切断结构对齐”这一核心策略的效力。

## 方法谱系与知识库定位

TriQDef 处于量化神经网络（QNN）对抗补丁防御的交叉点，它直接回应了现有方法在**跨比特宽度可迁移性泛化**上的核心空白。传统基于补丁的对抗训练（PBAT）仅在训练期间使用的补丁比特宽度上有效，面对未见过的补丁配置时攻击成功率（ASR）急剧上升（Table 2：2‑bit 未见补丁 ASR 达 78.34%），本质原因是 PBAT 并未打破不同量化级别之间内部特征和梯度信号的高度感知对齐。即便在梯度方向余弦相似度极低的情况下，边缘 IoU 和 HOG 余弦相似度仍然保持高位（Table 3：fp↔5b 梯度余弦 0.05，HOG 余弦 0.81），这种**隐蔽的结构性感知对齐**才是补丁可迁移的真正推手。TriQDef 通过在训练目标函数中同时引入特征不对齐惩罚（FDP）和梯度感知不协调惩罚（GPDP），并配合比特宽度感知的课程训练（BACT），主动破坏中间特征图与输入梯度在不同量化视图之间的边缘结构和纹理一致性，从根本上切断补丁的跨比特迁移路径。与面向像素级噪声的鲁棒量化方法（DWQ）不同，TriQDef 专为结构性补丁设计；与推理时预处理防御（DiffPure、JEDI）相比，TriQDef 在训练阶段完成所有正则化，推理阶段**零额外计算开销**，在部署侧极为友好（Table 18）。因此，TriQDef 填补了训练时防御在“多精度泛化”上的缺口，其方法定位为一种**通过感知解耦实现跨比特抗迁移**的训练范式。

### 适用边界与局限

TriQDef 已在图像分类任务（CIFAR‑10、ImageNet）上多种架构（ResNet、VGG、MobileNetV2、DenseNet、Inception v3 及 ViT 变体）和多种补丁攻击（LAVAN、GAP、PatchAttack、DRP）下展示了稳定的强防御能力，显著且一致地降低了 ASR（Table 5、Table 14–16）。然而，其应用仍受若干边界限制：

1. **训练开销**：相对于标准 QAT，TriQDef 增加了 1.47–1.60 倍的墙钟时间和 1.17–1.23 倍的峰值显存（Table 17），在资源极度受限的边缘设备上可能仍显昂贵。  
2. **量化宽度伸缩性**：训练时需联合优化多个比特宽度特定的量化器，激活的宽度越多，计算成本线性增长；目前仅在 {32, 8, 5, 4, 2} 比特等组合下验证，极端低位（如 1 比特）或混合精度设定下的表现未知。  
3. **任务与攻击覆盖**：实验仅限于单标签图像分类；在目标检测、分割等其他视觉任务上尚未建立证据。补丁生成依赖基于全精度模型的离线池或在线 EOT 过程，若攻击者采用专门针对 FDP/GPDP 的**自适应损失设计**，该方法是否仍能保持有效性**需要手动验证**。  
4. **实时自适应攻击未评估**：论文并未分析白盒攻击者是否可以通过最大化特征相似度与梯度对齐来反向击穿 TriQDef，因此其在强定向攻击下的鲁棒性仍为开放问题。

### 开放问题

- **极限低位与动态精度**：BACT 的课程激活策略能否平滑迁移到 1 比特或任意混合精度场景？FDP/GPDP 的权重分配与特征层选择是否需要自动化适配，以保持低比特下的清洁准确率？  
- **多防御协同**：将感知不对齐惩罚与随机量化、动态精度等架构级防御相结合，可能进一步提升鲁棒性，但协同训练时的冲突和收敛特性尚待系统研究。  
- **自动化层感知选择**：当前 FDP 只在手动选定的早期‑中层上施加，若能根据网络结构自识别对齐敏感层，有望在降低计算开销的同时维持甚至增强防御效果。  
- **跨模态推广**：Edge IoU 和 HOG 等感知结构度量能否迁移到 NLP 或语音模型，用于抑制跨精度量化下的对抗样本转移，仍是一个值得探索的方向。  
- **开放验证需求**：由于缺乏在自适应攻击下的实证结果，以及仅在一部分视觉架构上完成评估，上述开放点大多**处于假设阶段**，需要后续工作提供更为系统的实验支撑。

## 原文 PDF

![[paperPDFs/ICLR_2026/TriQDef_Disrupting_Semantic_and_Gradient_Alignment_to_Prevent_Adversarial_Patch_Transferability_in_Quantized_Neural_Networks.pdf]]
