---
title: A Provable Energy-Guided Test-Time Defense Boosting Adversarial Robustness of Large Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/A_Provable_Energy_Guided_Test_Time_Defense_Boosting_Adversarial_Robustness_of_Large_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- EGTTTE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过最小化输入图像基于分类器logit定义的能量函数（Energy Minimization），可以将对抗样本拉回正确流形，从而恢复正确预测。这一能量引导的测试时变换是提升鲁棒性的核心操作。
primary_logic: 将标准softmax分类器视为能量模型（EBM），其输出的负LogSumExp即为样本能量。对抗攻击使样本能量升高（偏离自然流形），而ET3在测试时通过梯度下降极小化该能量，可以引导对抗样本回到低能量区域，即自然分布，从而提升分类准确性。这一过程无需额外训练，计算开销低，且对二元分类器具有理论可证明性。
claims:
- ET3 is a lightweight, training-free defense that enhances robustness by minimizing the energy of the input samples.
- ET3 consistently enhances robust accuracy on adversarially robust models (TeCoA and FARE) across 14 datasets under attacks with ε_a = 4/255.
- Under the defense-unaware setting, ET3 consistently improves the robustness across all base models while preserving performance on clean data.
- ET3 improves worst-case robust accuracy under adaptive attack by +2.74.
---

# A Provable Energy-Guided Test-Time Defense Boosting Adversarial Robustness of Large Vision-Language Models

> [!tip] 核心洞察
> 将标准softmax分类器视为能量模型（EBM），其输出的负LogSumExp即为样本能量。对抗攻击使样本能量升高（偏离自然流形），而ET3在测试时通过梯度下降极小化该能量，可以引导对抗样本回到低能量区域，即自然分布，从而提升分类准确性。这一过程无需额外训练，计算开销低，且对二元分类器具有理论可证明性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一种可证明的能量引导测试时防御以提升大视觉语言模型的对抗鲁棒性 |
| 英文题名 | A Provable Energy-Guided Test-Time Defense Boosting Adversarial Robustness of Large Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Mirza_A_Provable_Energy-Guided_Test-Time_Defense_Boosting_Adversarial_Robustness_of_Large_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Energy-Guided Test-Time Transformation (ET3) |
| Dataset | Zero-shot classification, Fine-grained classification, LVLM tasks, ImageNet |

> [!tip] 效果简介
> - Zero-shot classification (14 datasets, e.g. ImageNet, CIFAR10, CIFAR100, etc.) 上，Robust accuracy (AutoAttack, ε_a=4/255) TeCoA+ET3 / FARE+ET3 vs TeCoA / FARE (no defense) (Avg. improvement from +0.4 to +10.98 across models and datasets)。
> - Fine-grained classification (8 datasets) 上，Robust accuracy (PGD-100, ε=4/255) TeCoA+ET3 (standalone & combined with augmentations) vs TPT, C-TPT, MTA, R-TPT, TTC, etc. (Improvement up to +11.62 (standalone), matches/exceeds SOTA when combined)。
> - LVLM tasks (COCO, Flickr30k captioning; TextVQA, VQAv2 QA) 上，CIDEr (captioning) / VQA accuracy LLaVA 1.5-7B with standard/robust CLIP + ET3 vs Same LLaVA models without ET3 (Robust accuracy increases consistently (see Table 3 for detailed values))。

## 概要

大视觉语言模型（LVLM）在图像描述、视觉问答等下游任务中展现出强大能力，但其依赖的视觉编码器（如CLIP）极易受到对抗扰动攻击——微小的像素级扰动即可导致模型预测完全错误，并进一步污染语言生成过程。这一视觉编码器的脆弱性是当前LVLM鲁棒性的核心瓶颈。

本文提出**能量引导的测试时变换（Energy-Guided Test-Time Transformation, ET3）**，一种轻量级、无需训练的测试时防御方法。其核心洞察在于：将标准softmax分类器视为能量模型（EBM），分类器输出logit的负LogSumExp即为样本的“能量”——低能量对应自然数据分布，而对抗扰动会使样本能量升高、偏离自然流形。ET3在测试时通过梯度下降极小化该能量，将对抗样本逐步拉回低能量区域，从而恢复正确预测。

具体而言，ET3对输入图像在ε球内执行投影梯度下降，以减小基于ImageNet-21k代理类计算的能量函数。优化后的图像通过CLIP视觉编码器提取特征，直接传递给LVLM的投影层，后续语言生成过程完全不变。该方法即插即用，无需重训练模型，推理开销极低（单步防御仅增加约2.3%的推理时间）。

ET3的关键特性包括：
- **训练无关**：直接作用于预训练分类器或视觉编码器，无需对抗训练或微调。
- **理论可证明**：对于满足局部线性假设和梯度范数比条件的二元分类器，ET3能保证正确分类（Theorem 4.1）。
- **广泛有效**：在14个零样本分类数据集上，ET3一致提升鲁棒模型（TeCoA、FARE）的对抗准确率；在细粒度分类、图像描述和视觉问答等LVLM任务上同样显著增强鲁棒性，同时保持干净数据上的性能。
- **防御自适应鲁棒性**：即使在攻击者知晓防御机制的自适应攻击下，ET3仍能将最坏情况鲁棒准确率提升+2.74。

在方法谱系上，ET3区别于现有的测试时提示调优（如TPT、C-TPT、R-TPT）和测试时数据增强（如MTA、TTC）等方法——它不修改文本提示，也不依赖多视图增强聚合，而是直接优化输入图像的能量，从根源上缓解视觉编码器的对抗脆弱性。与需要重训练的对抗训练范式相比，ET3提供了一种更灵活、计算成本更低的替代方案。

**局限与展望**：ET3的有效性依赖于网络的局部线性假设，在高度非线性区域可能效果减弱；防御半径ε需预先设定，对极大扰动可能无法完全恢复；当前仅针对视觉编码器，未覆盖文本或其他模态。未来方向包括：主动训练网络以满足ET3所需条件（如增大局部线性半径），将方法推广至视频、文本生成等多模态场景，以及在更大规模开源LVLM上验证一致性。

### 大视觉语言模型的对抗脆弱性瓶颈

大视觉语言模型（LVLM）在图像描述、视觉问答等跨模态任务中展现出强大能力，但其视觉编码器（如 CLIP）对对抗扰动高度敏感。攻击者只需在输入图像上添加人眼不可察觉的微小扰动，即可使视觉编码器产生错误特征，进而导致下游语言生成任务出现严重偏差。这一脆弱性根植于视觉编码器本身的分类边界缺陷——对抗样本被推离自然数据流形，落入高能量区域，使得模型以高置信度输出错误预测。

当前主流的对抗防御范式是**对抗训练**，即在训练阶段注入对抗样本以强化模型鲁棒性。然而，对抗训练需要重新训练模型，计算成本高昂，且对未见过的攻击类型泛化能力有限。更重要的是，对于已部署的大规模 LVLM（如 LLaVA），重新训练整个模型通常不切实际。这催生了对**测试时防御**方法的需求——在不修改模型参数的前提下，于推理阶段对输入进行变换以提升鲁棒性。

### 现有测试时防御方法的局限

近年来涌现了多种针对视觉-语言任务的测试时防御方法，可归纳为两类：

**提示调优类方法**通过优化文本提示来适应测试样本。**TPT**（Shu et al., NeurIPS 2022）通过最小化预测熵来调整提示嵌入；**C-TPT**（Yoon et al., ICLR 2024）引入校准项提升文本特征分散度；**R-TPT**（Sheng et al., CVPR 2025）专门针对对抗鲁棒性进行提示优化。这些方法需要多步优化，推理延迟较高，且仅作用于文本侧，未直接修复被扰动的视觉特征。

**输入变换类方法**直接修改图像或聚合多视图特征。**MTA**（Zanella et al., CVPR 2024）通过均值漂移聚合多个增强视图的嵌入；**TTC**（Xing et al., CVPR 2025）基于梯度最大化对抗样本与干净样本嵌入的距离。然而，MTA 依赖多次前向传播，计算开销显著；TTC 需要已知干净样本的嵌入分布作为参考，在开放场景中难以获取。

上述方法的共同缺口在于：**缺乏一种轻量、训练无关、且能从根本上将对抗样本拉回正确流形的测试时变换策略**。

### 本文动机：能量视角下的测试时防御

本文的核心洞察源于将标准 softmax 分类器重新诠释为**能量模型（EBM）**。在 EBM 框架下，分类器输出的负 LogSumExp 即为样本的能量函数：

$$E(\mathbf{x}) = -\log\Big(\sum_{k=1}^{K}\exp\big(f_{\theta}(\mathbf{x})_k\big)\Big)$$

自然数据分布于低能量区域，而对抗扰动使样本偏离流形，能量升高。基于这一认识，本文提出**能量引导的测试时变换（Energy-Guided Test-Time Transformation, ET3）**：在测试时通过梯度下降直接最小化输入图像的能量，将对抗样本投影回自然分布的低能量区域，从而恢复正确分类。

ET3 的设计遵循三个原则：（1）**训练无关**——无需修改或重训练视觉编码器，即插即用；（2）**计算高效**——仅需 1-2 步梯度下降，推理延迟增加低至 2.3%；（3）**理论可证明**——在局部线性假设下，ET3 对二元分类器具有正确分类的保证。该方法不仅适用于 CLIP 的零样本分类，还能通过共享视觉编码器将鲁棒性传递至 LLaVA 等下游 LVLM，实现跨任务的统一防御。

## 核心方法与创新机理

### 1. 从被动防御到主动能量引导的范式转换

当前大视觉语言模型（LVLM）在对抗攻击下的脆弱性根源在于视觉编码器（如 CLIP）对不可察觉扰动的极度敏感——攻击者只需在图像上施加微小扰动，即可使下游任务（图像描述、视觉问答）的性能大幅下降。现有防御方案要么需要昂贵的对抗训练（如 **TeCoA** (Mao et al., ICLR 2023)、**FARE** (Schlarmann et al., ICML 2024)），要么在测试时采用提示调优或多视图增强，推理延迟高且缺乏理论保障。

ET3 的核心范式转换在于：**将标准 softmax 分类器重新解释为能量模型（EBM），通过测试时梯度下降主动将对抗样本“拉回”自然数据流形**。具体而言，分类器输出 logit 的负 LogSumExp 被定义为样本的能量函数：

$$E(\mathbf{x}) = -\log\Big(\sum_{k=1}^{K}\exp\big(f_{\theta}(\mathbf{x})_k\big)\Big)$$

对抗攻击迫使样本偏离自然分布，导致其能量升高；ET3 在测试时以该能量为目标函数，在输入空间的 $\ell_2$ 球内执行投影梯度下降，逐步降低样本能量，使其回归低能量区域（即自然分布）。这一过程无需任何模型重训练，是一种即插即用的测试时防御。

### 2. 关键设计要素：changed slots 分析

与现有测试时方法相比，ET3 在三个核心维度上实现了根本性改变：

| 设计维度 | 基线方案 | ET3 方案 | 创新本质 |
|---------|---------|---------|---------|
| **测试时防御策略** | 无防御（直接使用预训练模型），或基于提示调优/多视图增强的方法（如 TPT、C-TPT、MTA、TTC） | 以能量最小化为目标的梯度下降优化输入，将对抗样本投影回自然流形 | 从“适应模型参数或聚合多视图”转向“直接修正输入分布”，操作对象从模型内部转向输入空间 |
| **对抗防御范式** | 对抗训练（需重训练模型）或随机化/纯化（缺乏目标引导） | 训练无关、即插即用的测试时变换，仅需极小优化步骤 | 将防御与训练完全解耦，使任何预训练视觉编码器均可直接受益 |
| **计算开销** | 测试时提示调优需多步优化（TPT 需多次前向传播），多视图增强需处理多个增强副本 | 仅需 2 步梯度下降，甚至单步即可提供明显增益，推理时间增加仅 2.3% | 在保持防御效果的同时，将推理延迟降至接近零开销的水平 |

### 3. 能量引导机制的精妙之处

ET3 的能量引导策略具有三个深层优势：

**其一，利用代理类集实现任务无关的防御**。能量计算使用 ImageNet-21k 的文本标签作为代理类集，而非下游任务的具体标签。这意味着 ET3 的优化过程完全不依赖下游任务信息，却能普遍提升各类任务（零样本分类、细粒度分类、图像描述、VQA）的鲁棒性。消融实验证实，使用大规模代理类集（ImageNet-21k）相比仅使用任务相关标签，能带来略微的鲁棒性提升。

**其二，对干净样本的“无害性”**。对于干净输入，ET3 的梯度下降要么保持原始预测不变，甚至可能提升模型置信度——因为干净样本本身已处于低能量区域，进一步的能量最小化不会将其推离正确类别。这解决了防御方法常见的“干净精度下降”困境。

**其三，对二元分类器的理论可证明性**。Theorem 4.1 证明，在局部线性和梯度范数比率条件的假设下，ET3 单步变换即可保证对抗样本被正确分类。这一理论保障在现有测试时防御方法中极为罕见，为方法的可靠性提供了坚实基础。

### 4. 与同类方法的本质区别

ET3 与现有测试时方法的区别不仅是技术路线不同，更是对“鲁棒性来源”这一根本问题的不同回答：

- **TPT/C-TPT/R-TPT** 等提示调优方法认为鲁棒性瓶颈在于文本提示与图像的匹配度，通过最小化预测熵来优化提示。然而，当视觉编码器本身已被对抗扰动“欺骗”时，仅调整文本侧的提示无法从根本上恢复正确的视觉特征。
- **MTA** 等方法通过多视图增强的均值漂移聚合来提升鲁棒性，本质上是利用数据增强的统计平滑效应，但缺乏针对性的优化目标。
- **TTC** 虽然也使用基于梯度的测试时变换，但其目标是最大化对抗样本与干净样本嵌入的距离，需要参考干净样本的嵌入，这在仅给定对抗样本的实际场景中不可行。

ET3 的回答是：**鲁棒性来源于将样本拉回自然分布的低能量区域**。这一回答不仅统一了分类与生成视角下的防御逻辑（能量模型天然桥接判别与生成），也为未来研究指明了方向——训练网络以主动满足 ET3 所需的条件（如增大局部线性半径或能量梯度比率），可进一步提升防御效果。

ET3（Energy-Guided Test-Time Transformation）构建了一条“能量计算—梯度优化—特征传递”的轻量级测试时防御流水线。其核心思路是将预训练分类器重新解释为能量模型（EBM），通过极小化输入图像的能量将其从对抗样本所在的高能区域拉回自然分布的低能区域。整个过程无需额外训练，仅依赖预训练好的视觉编码器，且优化后的图像特征可直接传递给下游的大视觉语言模型（LVLM）。

### 流水线模块与数据流

ET3 的完整流水线由三个紧密衔接的模块构成，如图 Figure 2 所示：

1. **能量计算模块**
   给定输入图像 $\mathbf{x}$（可能是干净样本或对抗样本），利用预训练 CLIP 视觉编码器 $f_{\theta}$ 的输出 logit 计算该图像的能量：
   $$E(\mathbf{x}) = -\log\Big(\sum_{k=1}^{K}\exp\big(f_{\theta}(\mathbf{x})_k\big)\Big)$$
   该定义将标准 softmax 分类器的负 LogSumExp 作为能量函数：低能量对应高置信度的自然样本，高能量则表征偏离数据流形的对抗样本。为获得稳定且通用的能量估计，ET3 统一采用 ImageNet-21k 的文本标签集作为代理类别来计算 logit，而非仅使用任务相关的少量标签。这一设计使得能量信号能捕捉更丰富的语义偏离，消融实验表明其带来略微的鲁棒性增益。

2. **梯度下降优化模块**
   以输入图像 $\mathbf{x}$ 为起点，在半径为 $\epsilon$ 的 $\ell_2$ 球内执行投影梯度下降，逐步极小化能量函数：
   $$\mathbf{x}^{(t)} = \Pi_{\mathcal{B}_\epsilon(\mathbf{x})}\Big(\mathbf{x}^{(t-1)} - \alpha\nabla_{\mathbf{x}}E\big(\mathbf{x}^{(t-1)}\big)\Big)$$
   其中 $\Pi_{\mathcal{B}_\epsilon(\mathbf{x})}$ 表示将更新后的图像投影回以原始输入为中心的 $\epsilon$ 球内，$\alpha$ 为步长。对于干净样本，能量本已较低，优化过程几乎不改变图像，甚至可能进一步提升模型置信度；对于对抗样本，梯度下降引导图像离开高能区域，向正确的分类流形移动。该模块仅需极少的优化步数：默认使用 2 步迭代即可获得显著鲁棒性提升，甚至单步优化（$T=1$）也能提供有效防御，且推理延迟仅增加约 2.3%。

3. **视觉编码器特征传递模块**
   优化完成后，将精炼后的图像 $\tilde{\mathbf{x}}$ 重新送入 CLIP 视觉编码器，提取视觉嵌入。这些嵌入随后有两种使用路径：
   - **零样本分类路径**：视觉嵌入直接与文本标签嵌入计算余弦相似度，完成分类。此时 ET3 作为一个即插即用的防御层，保护 CLIP 模型免受对抗攻击。
   - **LVLM 保护路径**：视觉嵌入传递给下游大视觉语言模型（如 LLaVA 1.5-7B）的投影层，后续的语言生成过程完全不变。值得注意的是，LVLM 本身不参与能量优化过程——ET3 仅在视觉编码器端操作，优化后的图像通过共享的视觉编码器内部表示自然迁移到 LVLM，从而提升图像描述、视觉问答等下游任务的鲁棒性。

### 输入输出规范

- **输入**：单张图像 $\mathbf{x} \in \mathbb{R}^{H \times W \times C}$，可以是干净图像或遭受 $\ell_\infty$ 对抗扰动（如 PGD、AutoAttack）的攻击样本。
- **超参数**：防御半径 $\epsilon$（控制允许的最大变换幅度）、优化步数 $T$、步长 $\alpha$。这些参数在测试时预设，无需根据具体攻击动态调整。
- **输出**：优化后的图像 $\tilde{\mathbf{x}}$，满足 $\|\tilde{\mathbf{x}} - \mathbf{x}\|_2 \leq \epsilon$，可直接替代原始图像输入到任意依赖 CLIP 视觉编码器的下游模型。
- **计算开销**：主要开销来自 $T$ 次前向-反向传播以计算能量梯度。默认 $T=2$ 时推理时间增加极低；单步模式（$T=1$）下仅增加 2.3% 的延迟，远低于需要多步优化或多视图增强的测试时提示调优方法（如 TPT、C-TPT）和测试时增强方法（如 MTA、TTC）。

### 与现有测试时防御的关系

ET3 在防御范式上区别于两类主流方法：
- **对抗训练类方法**（如 TeCoA、FARE）：需要在训练阶段注入对抗样本重训练模型，而 ET3 是训练无关的，可直接应用于任何预训练好的视觉编码器。
- **测试时提示/增强类方法**（如 TPT、C-TPT、R-TPT、MTA、TTC）：这些方法或通过多步优化文本提示、或通过多视图增强聚合来提升鲁棒性，通常需要多次前向传播，推理延迟较高。ET3 直接优化输入图像的能量函数，仅需极少的梯度步，且优化过程完全在视觉编码器端完成，不涉及文本编码器或 LVLM 的修改。

这种“能量引导的测试时变换”策略将防御的核心操作从“模型重训练”或“提示工程”转移到了“输入空间的能量最小化”，实现了训练无关、即插即用、计算高效的对抗鲁棒性提升。

### 能量计算模块

ET3 的核心操作是将标准 softmax 分类器重新解释为能量模型（EBM）。给定一个视觉编码器 $f_{\theta}$ 输出的 $K$ 类 logit，图像 $\mathbf{x}$ 的能量定义为负 LogSumExp：

$$E(\mathbf{x}) = -\log\Big(\sum_{k=1}^{K}\exp\big(f_{\theta}(\mathbf{x})_k\big)\Big)$$

**变量含义**：$f_{\theta}(\mathbf{x})_k$ 表示视觉编码器对第 $k$ 类的输出 logit；$K$ 为类别总数。该能量函数的直觉是：自然分布内的样本对应低能量区域，而对抗扰动会将样本推向高能量区域（偏离自然流形）。为保持通用性，ET3 在所有任务中统一使用 ImageNet-21k 文本标签集作为代理类来计算能量，消融实验表明这比仅使用任务相关标签能带来略微的鲁棒性提升。

### 梯度下降优化模块

ET3 通过投影梯度下降在测试时最小化上述能量函数，将对抗样本拉回低能量区域。给定输入图像 $\mathbf{x}$（可能是对抗样本），在 $\epsilon$ 半径的 $\ell_2$ 球内执行迭代优化：

$$\mathbf{x}^{(t)} = \Pi_{\mathcal{B}_\epsilon(\mathbf{x})}\Big(\mathbf{x}^{(t-1)} - \alpha\nabla_{\mathbf{x}}E\big(\mathbf{x}^{(t-1)}\big)\Big)$$

**变量含义**：$\mathbf{x}^{(t)}$ 为第 $t$ 步优化后的图像；$\Pi_{\mathcal{B}_\epsilon(\mathbf{x})}$ 表示向以原始输入 $\mathbf{x}$ 为中心、半径为 $\epsilon$ 的 $\ell_2$ 球做投影；$\alpha$ 为步长。优化从 $\mathbf{x}^{(0)} = \mathbf{x}$ 开始，通常仅需 $T=2$ 步迭代即可收敛。消融实验证实，即使单步优化（$T=1$）也能提供明显的鲁棒性增益，且推理延迟增加极小（仅约 2.3%）。

### 视觉编码器特征传递模块

优化后的图像通过 CLIP 视觉编码器提取视觉嵌入，这些嵌入直接传递给下游 LVLM（如 LLaVA）的投影层，后续的语言生成过程保持不变。该模块的关键特性是：**VLM 本身不参与能量优化过程**，ET3 仅通过视觉编码器的内部表征实现对抗防御的迁移。这意味着 ET3 可即插即用地保护任何使用该视觉编码器的多模态模型，无需修改 VLM 架构或进行额外训练。

### 能量梯度的结构分析

为理解 ET3 为何有效，可将能量梯度展开为各类别梯度的 softmax 加权组合。在二元分类情形下（Theorem 4.1 的分析基础）：

$$\nabla_{\mathbf{x}}E(\mathbf{x}) = -\operatorname{SoftMax}(f_{\theta}(\mathbf{x}))^{\top} \nabla_{\mathbf{x}}f_{\theta}(\mathbf{x}) = -e_{-1}\mathbf{g}_{-1} - e_1\mathbf{g}_1$$

其中 $e_1$、$e_{-1}$ 分别为真实类和错误类的 softmax 概率，$\mathbf{g}_1$、$\mathbf{g}_{-1}$ 为对应类别的 logit 梯度。ET3 沿负能量梯度方向更新输入，等价于沿真实类梯度方向移动，从而增大正确类的 logit 并抑制错误类。

### 局部线性假设下的理论保证

Theorem 4.1 在局部线性假设下给出了 ET3 正确分类的充分条件。假设模型在防御邻域 $B_\epsilon(\mathbf{x})$ 内局部线性，变换 $\mathbf{z}$ 对 logit 的影响可表示为：

$$f_i(\mathbf{x}+\mathbf{z}) = f_i(\mathbf{x}) + \mathbf{z}^{\top}\mathbf{g}_i$$

当真实类加权梯度的范数远大于错误类时（即 $C \| e_{\hat{y}_t} \mathbf{g}_{\hat{y}_t} \| < \| e_{y_t} \mathbf{g}_{y_t} \|$），ET3 可通过单步变换保证正确分类。Figure 3（右）的散点图在 ImageNet 鲁棒分类器上验证了该条件在多数样本上成立。

## 实验与关键发现

### 核心实验设计

ET3 的实验验证覆盖三个维度：(1) 零样本分类的鲁棒性提升，(2) 细粒度分类与现有测试时方法的对比，(3) 大视觉语言模型（LVLM）下游任务的迁移效果。所有实验默认使用 ImageNet-21k 文本标签作为代理类计算能量，防御半径 $\epsilon$ 与攻击预算 $\epsilon_a$ 保持一致（通常为 $4/255$），优化步数 $T=2$。

**防御非感知（defense-unaware）设定**是主要评估场景：攻击者不知道 ET3 的存在，仅针对基础模型生成对抗样本。**防御感知（defense-aware）设定**则模拟最坏情况，攻击者通过可微代理绕过防御，用于检验 ET3 的理论保真性。

---

### 零样本分类鲁棒性（Table 1）

![[assets/figures/papers/paper_list_l2757_https_openaccess_thecvf_com_content_CVPR2026_html_Mirza_A_Provable_Energ/figures/004_Table_1.jpg]]
*Table 1: Zero-shot robustness of ET3 across 14 benchmark datasets in the defense-unaware setting. Comparison of clean and robust accuracy for baseline models versus same models augmented with ET3. Robustness is evaluated against Auto-Attack (AA) at*

Table 1 报告了 ET3 在 14 个标准数据集上对两个鲁棒 CLIP 变体（TeCoA 和 FARE）的增强效果，攻击方式为 Auto-Attack（$\epsilon_a = 4/255$）。核心发现：

- **一致提升**：ET3 在所有数据集上均提升鲁棒准确率，平均增益从 +0.4 到 +10.98 不等，取决于基础模型和数据集。
- **干净精度保持**：ET3 对干净样本的准确率几乎无影响，部分情况下甚至略有提升——能量最小化将干净样本推向更高置信度区域。
- **跨模型泛化**：无论视觉编码器是 TeCoA（对抗训练）还是 FARE（无监督对抗微调），ET3 均有效，表明其不依赖于特定的鲁棒训练范式。

**机制解释**：对抗攻击使样本能量升高，偏离自然流形；ET3 通过梯度下降将样本拉回低能量区域，恢复正确分类。Table 1 的数据验证了这一假设——鲁棒模型本身已具备一定的局部线性特性，ET3 在此基础上进一步利用能量梯度方向进行修正。

---

### 细粒度分类与测试时方法对比（Table 2）

![[assets/figures/papers/paper_list_l2757_https_openaccess_thecvf_com_content_CVPR2026_html_Mirza_A_Provable_Energ/figures/005_Table_2.jpg]]
*Table 2: Robustness of ET3 on fine-grained classification in the defense-unaware setting. Comparison against test-time adaptation techniques across eight fine-grained datasets. All defenses are applied to a TeCoA pre-trained CLIP-ViT-B/32 model and evaluated against*

Table 2 在 8 个细粒度数据集上对比 ET3 与五类测试时方法：TPT（Shu et al., NeurIPS 2022）、C-TPT（Yoon et al., ICLR 2024）、R-TPT（Sheng et al., CVPR 2025）、MTA（Zanella et al., CVPR 2024）和 TTC（Xing et al., CVPR 2025）。所有方法均应用于 TeCoA 预训练的 CLIP-ViT-B/32，攻击为 PGD-100（$\epsilon = 4/255$）。

关键结论：

- **独立使用最优**：ET3 作为独立防御时，鲁棒准确率提升最高达 +11.62，超越所有对比方法。
- **可组合性**：ET3 与 MTA 等增强方法结合后，进一步超越现有 SOTA，表明能量最小化与基于增强的防御具有互补性。
- **效率优势**：TPT 和 C-TPT 需要多步优化文本提示，推理延迟显著；ET3 仅需 2 步图像空间梯度下降，单步推理时间增加仅 2.3%。

**失败模式提示**：对于某些细粒度类别（如鸟类品种），代理标签集（ImageNet-21k）可能缺乏足够的判别粒度，此时能量最小化的引导方向不够精确。该场景下 ET3 的增益相对有限，需要人工验证具体退化样本。

---

### LVLM 下游任务迁移（Table 3）

![[assets/figures/papers/paper_list_l2757_https_openaccess_thecvf_com_content_CVPR2026_html_Mirza_A_Provable_Energ/figures/006_Table_3.jpg]]
*Table 3: Evaluation of ET3 on LLaVA 1.5-7B with different vision encoders in defense-unaware setting. Clean and*

Table 3 评估 ET3 对 LLaVA 1.5-7B 在图像描述（COCO、Flickr30k，指标为 CIDEr）和视觉问答（TextVQA、VQAv2，指标为准确率）上的鲁棒性提升。视觉编码器分别使用标准 CLIP 和两种鲁棒变体（TeCoA/FARE，训练扰动 $\epsilon_t = 2/255$ 和 $4/255$）。

核心发现：

- **即插即用迁移**：ET3 仅优化视觉编码器的输入图像，优化后的视觉嵌入直接传递给 LLaVA 的投影层，无需修改语言模型。在所有编码器配置下，ET3 均一致提升鲁棒性能。
- **干净性能保持**：与分类任务一致，ET3 对干净图像的描述质量和问答准确率无负面影响。
- **鲁棒编码器协同**：使用鲁棒 CLIP 作为视觉骨干时，ET3 的增益更为显著，说明鲁棒预训练与测试时防御存在正向协同效应。

**机制验证**：Figure 2 的下半部分直观展示了这一迁移流程——对抗样本经过 ET3 优化后，视觉编码器输出的嵌入更接近干净样本的嵌入，从而保护下游语言生成过程不受污染。

---

### 防御感知自适应攻击（Table 4 & Table 5）

![[assets/figures/papers/paper_list_l2757_https_openaccess_thecvf_com_content_CVPR2026_html_Mirza_A_Provable_Energ/figures/007_Table_4.jpg]]
*Table 4: Defense-aware worst-case robustness on ImageNet. Clean and*

![[assets/figures/papers/paper_list_l2757_https_openaccess_thecvf_com_content_CVPR2026_html_Mirza_A_Provable_Energ/figures/009_Table_5.jpg]]
*Table 5: Defense-aware adaptive attack evaluation on LLaVA. Average robust accuracy over four datasets (200 samples). Legend: B = baseline (no defense); N-Ad. = non-adaptive; Ad. = adaptive; blue = ET3 with*

**ImageNet 最坏情况（Table 4）**：在防御感知设定下，攻击者使用可微代理对 ET3 进行自适应攻击。ET3 在最坏情况下仍将鲁棒准确率从基线提升 +2.74（37.70%），验证了 Theorem 4.1 的理论保真性——即使在攻击者知晓防御机制的情况下，ET3 仍能提供可证明的鲁棒性增益。

**LLaVA 自适应攻击（Table 5）**：在 4 个数据集（各 200 样本）上，ET3 的 $\ell_2$ 投影和 $\ell_\infty$ 投影变体均在非自适应和自适应攻击下显著提升鲁棒准确率。$\ell_\infty$ 投影在某些场景下表现更优，因为视觉编码器通常在 $\ell_\infty$ 威胁模型下训练，投影空间与训练时一致。

---

### 攻击强度敏感性分析（Figure 4）

![[assets/figures/papers/paper_list_l2757_https_openaccess_thecvf_com_content_CVPR2026_html_Mirza_A_Provable_Energ/figures/008_Figure_4.jpg]]
*Figure 4: Robust accuracy across increasing attack strengths in the defense-unaware setting. Average zero-shot accuracy of CLIP over 14 benchmark datasets, showing that ET3 consistently improves the robustness of the TeCoA models trained with different defense strengths (ωt) as the attack strength (ωa) increases*

Figure 4 展示了 ET3 在不同攻击强度（$\epsilon_a$）下的鲁棒准确率变化曲线。横轴为攻击强度，纵轴为 14 个数据集的平均零样本准确率，不同曲线对应不同防御强度（$\omega_t$）训练的 TeCoA 模型。

关键趋势：

- **跨强度一致增益**：ET3 在所有攻击强度下均提升鲁棒准确率，且随着攻击强度增大，提升幅度更为明显。
- **训练-测试协同**：使用更高防御强度（$\omega_t$）训练的模型，其局部线性特性更强，ET3 的增益也更大——这为“训练以主动满足 ET3 条件”提供了实验依据。

---

### 消融实验

**代理标签集选择**：使用完整的 ImageNet-21k 标签集计算能量，相比仅使用任务相关标签子集，带来略微的鲁棒性提升。原因在于更大的标签集提供了更密集的能量景观，梯度方向更具判别性。

**优化步数**：即使单步优化（$T=1$）也能提供明显的鲁棒性增益，且推理延迟增加极小（2.3%）。两步优化（$T=2$）在增益与开销之间取得最佳平衡。更多步数（$T \geq 5$）的边际收益递减。

---

### 失败模式与局限性

1. **局部线性假设违例**：对于高度非线性的网络区域（如决策边界附近的尖锐转折），ET3 的梯度方向可能无法有效引导样本回到正确流形，导致防御失败。Figure 3 右图的散点显示，当梯度范数比 $C < 1$ 时，ET3 变换后的 logit margin 可能仍为负值。

2. **防御半径敏感性**：$\epsilon$ 需预先设定并与攻击预算匹配。对于 $\epsilon_a$ 远大于 $\epsilon$ 的强攻击，ET3 无法在受限的投影球内完全恢复正确预测。

3. **模态局限性**：当前方法仅针对视觉编码器的对抗鲁棒性，未涉及文本编码器或多模态融合层的防御。对于针对语言生成过程的攻击，ET3 无法提供保护。

4. **实时应用延迟**：虽然单步优化的开销极小（2.3%），但在资源极度受限的边缘设备上，每次推理的梯度计算仍可能成为瓶颈。

## 定位与知识库关联

### 测试时防御的范式演进

大视觉语言模型（LVLM）的对抗鲁棒性研究长期聚焦于对抗训练范式，例如 **TeCoA**（Mao et al., ICLR 2023）和 **FARE**（Schlarmann et al., ICML 2024）分别通过文本可控对抗训练和无监督对抗微调来强化CLIP视觉编码器的鲁棒性。然而，这类方法需要重新训练模型，且对未见过的攻击类型泛化能力有限。

ET3代表了一种根本不同的防御范式——**训练无关、即插即用的测试时变换**。与对抗训练相比，ET3直接操作预训练模型，无需任何额外训练（*“ET3 requires no additional model training. It operates directly on a pre-trained classifier or visual encoder”*），这使得它能够灵活地部署在任意现成的视觉编码器之上。

### 与现有测试时方法的对比

在测试时防御这一分支中，现有方法可大致分为两类：

**基于提示调优的方法**：**TPT**（Shu et al., NeurIPS 2022）通过最小化预测熵来优化文本提示，**C-TPT**（Yoon et al., ICLR 2024）引入校准项提升文本特征分散度，**R-TPT**（Sheng et al., CVPR 2025）则专门针对对抗鲁棒性进行提示优化。这些方法操作的是文本端，需要多步优化且推理延迟较高。

**基于图像变换的方法**：**TTC**（Xing et al., CVPR 2025）通过最大化对抗样本与干净样本嵌入的距离来进行测试时反击，**MTA**（Zanella et al., CVPR 2024）则通过鲁棒的均值漂移聚合多增强视图的嵌入。这些方法操作图像端，但通常需要多个增强视图或复杂的优化目标。

ET3的关键区别在于：
- **操作对象**：直接优化输入图像像素，而非文本提示或嵌入聚合
- **优化目标**：最小化基于分类器logit的能量函数（Energy Minimization），将对抗样本拉回自然流形
- **计算效率**：仅需2步梯度下降甚至单步，推理时间增加仅2.3%（*“ET3 introduces minimal overhead with increase in inference time by as little as 2.3% in single-step defense”*）

### 能量模型的视角创新

ET3的核心洞察在于将标准softmax分类器重新解释为能量模型（EBM）。传统上，能量模型用于生成建模，而ET3创造性地利用分类器输出的负LogSumExp作为样本能量：

$$E(\mathbf{x}) = -\log\Big(\sum_{k=1}^{K}\exp\big(f_{\theta}(\mathbf{x})_k\big)\Big)$$

这一能量定义使得对抗攻击的效果可以被统一解释：对抗扰动将样本推向高能量区域（偏离自然流形），而ET3通过梯度下降极小化该能量，引导样本回到低能量区域（自然分布）。这种视角将分类鲁棒性与能量模型的分布匹配联系起来，为测试时防御提供了新的理论工具。

### 理论可证明性的边界

ET3的理论保证（Theorem 4.1）建立在两个关键假设之上：
1. **局部线性假设**：分类器在防御邻域$B_\epsilon(\mathbf{x})$内近似线性，即$f_i(\mathbf{x}+\mathbf{z}) = f_i(\mathbf{x}) + \mathbf{z}^{\top}\mathbf{g}_i$
2. **梯度范数比率条件**：$C \| e_{\hat{y}_t} \mathbf{g}_{\hat{y}_t} \| < \| e_{y_t} \mathbf{g}_{y_t} \|$，即真实标签类的加权梯度范数大于错误类的加权梯度范数

当这些条件满足时，ET3能够保证将对抗样本恢复为正确分类。然而，这些假设也划定了方法的适用边界：对于高度非线性的网络区域，局部线性假设可能不成立；对于某些对抗样本，梯度范数比率条件可能不满足。论文通过实验（Figure 3右）验证了在ImageNet上大多数样本确实满足$C>1$的条件，且ET3变换后logit margin为正，但这一验证限于特定模型和数据集。

### 适用边界与局限

**视觉编码器中心性**：ET3当前仅针对视觉编码器的对抗鲁棒性，未涉及文本编码器或其他模态的防御。在LVLM场景中，它通过优化图像输入来保护下游任务，但文本端的脆弱性（如提示注入攻击）不在其保护范围内。

**防御半径的预设定**：防御半径$\epsilon$需要预先设定，且与攻击预算相关。对于超出防御半径的极大攻击扰动，ET3可能无法完全恢复正确预测。Figure 4显示随着攻击强度增加，ET3仍能提供增益，但增益幅度可能递减。

**代理标签的依赖性**：能量计算依赖于ImageNet-21k代理标签集，虽然消融实验表明使用大规模代理标签优于仅使用任务相关标签（*“yielding slightly improved robustness”*），但代理标签的选择策略对不同任务的泛化性仍需进一步验证。

**实时应用的延迟考量**：尽管计算开销低（2.3%推理时间增加），但在资源受限的实时应用中，每次推理进行梯度优化仍可能引入不可忽视的延迟。

### 开放问题

1. **网络架构的主动适配**：能否通过训练策略主动塑造网络特性，使其更满足ET3的理论条件（如增大局部线性半径或优化梯度范数比率），从而进一步提升防御效果？这指向了对抗训练与测试时防御的协同设计。

2. **多模态扩展**：ET3能否推广到视频理解、文本生成等其他模态？与最新的多模态对抗训练方法（如针对LVLM的端到端对抗训练）如何结合，是一个值得探索的方向。

3. **更大规模模型的验证**：当前实验主要在CLIP ViT-B/32和LLaVA 1.5-7B上进行。在更大规模的开源LVLM（如Qwen-VL、Open-Flamingo）上，ET3是否仍能保持一致的鲁棒性提升，需要进一步验证。

4. **自适应攻击的极限**：Table 4显示在防御感知的自适应攻击下，ET3仍能提升鲁棒性（+2.74），但这一提升幅度是否能在更强的自适应攻击策略下保持，是一个开放问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/A_Provable_Energy_Guided_Test_Time_Defense_Boosting_Adversarial_Robustness_of_Large_Vision_Language_Models.pdf]]
