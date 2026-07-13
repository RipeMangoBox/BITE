---
title: "A tale of two tails: Preferred and anti-preferred natural stimuli in visual cortex"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_tale_of_two_tails_Preferred_and_anti_preferred_natural_stimuli_in_visual_cortex.pdf
project_link: null
code_link: null
aliases:
- LRLLMTTVRP
- TTTPAPNSVC
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/neuroscience_cognitive_science
core_operator: "在估计神经元调谐函数时，将反偏好图像（anti-preferred images）与偏好图像（preferred images）同时纳入训练集，以揭示反偏好刺激是否是塑造调谐的必要组成部分。通过数据剪枝实验操控训练集中是否包含反偏好图像，观察对神经元响应预测泛化能力的影响（即R²的变化）。"
primary_logic: "V4神经元对自然图像的反应并非传统上认为的单尾分布，而是显著的双尾分布（偏度κ≈0.87），表明它们同时具有明确的偏好刺激和反偏好刺激。这些反偏好刺激并非无特征的灰屏，而是具有丰富视觉特征的图像，能够将神经元活动抑制到基线以下。更重要的是，反偏好图像是神经元调谐不可或缺的部分：仅使用偏好图像无法准确预测神经元的响应，而同时使用偏好和反偏好图像可以显著提升预测性能。此外，偏好特征与反偏好特征在图像统计上无法区分，且在不同神经元间不共享，这意味着每个V4神经元通过编码两个独立的视觉特征，实际上使群体的特征选择性容量加倍。这种双尾编码机制在现有的深度神经网络中并不存在，揭示了一个重要的表征差距。"
claims:
- "V4神经元对自然图像的响应分布呈现双尾特性，偏度中位数κ=0.87，显著低于深度网络单元的κ=2.06（p<0.002），表明V4神经元同时编码偏好和反偏好刺激。"
- "用数据驱动的V4模型神经元预测的偏好图像在真实神经元上诱发的响应位于随机图像响应分布的90%分位数以上（q=0.985），而反偏好图像诱发的响应则位于10%分位数以下（q=0.055），实验证实了反偏好刺激的抑制性功能。"
- "在数据剪枝实验中，使用偏好和反偏好图像联合训练的效果优于随机选择图像，且单独使用偏好或反偏好图像的训练泛化性能均显著下降，证明两者都是估计V4调谐所必需的。"
- "人类被试在心理物理学任务中，当同时看到偏好和反偏好图像时，预测V4模型神经元响应的平均准确率达到80.5%，表明反偏好信息对人类理解神经元调谐至关重要。"
---

# A tale of two tails: Preferred and anti-preferred natural stimuli in visual cortex

> [!tip] 核心洞察
> V4神经元对自然图像的反应并非传统上认为的单尾分布，而是显著的双尾分布（偏度κ≈0.87），表明它们同时具有明确的偏好刺激和反偏好刺激。这些反偏好刺激并非无特征的灰屏，而是具有丰富视觉特征的图像，能够将神经元活动抑制到基线以下。更重要的是，反偏好图像是神经元调谐不可或缺的部分：仅使用偏好图像无法准确预测神经元的响应，而同时使用偏好和反偏好图像可以显著提升预测性能。此外，偏好特征与反偏好特征在图像统计上无法区分，且在不同神经元间不共享，这意味着每个V4神经元通过编码两个独立的视觉特征，实际上使群体的特征选择性容量加倍。这种双尾编码机制在现有的深度神经网络中并不存在，揭示了一个重要的表征差距。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 两条尾巴的故事：视觉皮层中偏好与反偏好的自然刺激 |
| 英文题名 | A tale of two tails: Preferred and anti-preferred natural stimuli in visual cortex |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=RZ8esDBqMJ) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/neuroscience_cognitive_science |
| Method | Linear-ReLU-Linear (LRL) mapping for two-tailed V4 response prediction |
| Dataset | V4神经元对自然图像响应分布（n=219）, 实验验证：V4模型神经元选择的偏好和反偏好图像在真实V4记录中的响应, 人类心理物理学任务：预测V4模型神经元响应, 群体特征选择性容量（压缩比） |

> [!tip] 效果简介
> - V4神经元对自然图像响应分布（n=219） 上，中位数偏度 κ 为 V4神经元 κ = 0.87，对比 ResNet50 DNN单元 κ = 2.06，变化 显著更低（p<0.002）。
> - 实验验证：V4模型神经元选择的偏好和反偏好图像在真实V4记录中的响应 上，响应分位数（相对于随机图像） 为 偏好图像 q = 0.985，反偏好图像 q = 0.055，对比 随机图像分布（90%密度区间），变化 偏好图像显著高于上界，反偏好图像显著低于下界（permutation test, p<0.001）。
> - 人类心理物理学任务：预测V4模型神经元响应 上，平均正确率 为 同时提供偏好和反偏好图像时正确率为80.5%。

## 概要

传统视觉编码模型──无论是经典的线性-非线性级联，还是深度网络中以ReLU为代表的处理单元──都默认神经元只对“偏好刺激”产生正响应，响应分布呈单尾，反偏好（anti‑preferred）刺激被视作无信息的零响应或噪声。这一简化导致模型无法完整描述灵长类视觉皮层，尤其是V4区神经元的真实调谐特性，成为当下计算模型生物逼真度的核心瓶颈。

本文的核心发现是：V4神经元对自然图像的响应并非单尾，而是显著双尾的，中位偏度κ≈0.87（深度网络单元κ=2.06，p<0.002）。这意味着神经元同时编码明确的偏好刺激和反偏好刺激──反偏好图像不仅不是无特征的灰屏，反而是具有丰富视觉特征的自然图像，能够将神经元活动抑制到基线以下。更为关键的是，偏好与反偏好在图像统计上几乎无法区分，且不同神经元之间的偏好/反偏好集合不具有共享关系，表明每个V4神经元实际上独立编码两种不同视觉特征。因此，在群体层面，反偏好选择性使神经元的特征容量大约翻倍（群体压缩比达2.5）。这一双尾编码机制在现有任何深度网络中均不存在，揭示出当前模型与生物视觉系统之间一个至关重要的表征差距。

为了系统揭示并验证这一机制，研究构建了一条从建模到行为实验的完整验证链。首先，利用清醒猴V4电生理记录训练数据驱动的深度网络模型（V4 model neuron），并引入线性-ReLU-线性（LRL）映射，使模型能够从预激活特征中同时捕捉偏好与反偏好信息。随后，通过数据剪枝实验证明：仅用偏好图像或仅用反偏好图像训练时，学生网络的泛化预测R²均显著低于两者联合使用，表明反偏好刺激是估计V4调谐不可或缺的组成部分。在人类心理物理学任务中，当被试同时看到偏好与反偏好图像时，预测V4模型神经元响应的平均正确率达到80.5%，进一步证实反偏好信息对人类理解神经元编码的重要性。此外，团队开发了ImageBeagle搜索工具，基于大规模近邻图，仅需评估约1万张图像即可逼近3000万自然图像池中的最优偏好与反偏好刺激，实现了高效的闭环刺激搜索。主要实验结果表明：模型预测的偏好图像在真实V4神经元上引发的响应位于随机图像分布90%分位数以上（q=0.985），而反偏好图像响应则低于10%分位数（q=0.055），直接证实了反偏好刺激的抑制性功能。

本研究的局限性在于：分析主要集中于V4区，尚未在整个视觉层级上系统验证双尾编码的普遍性；人类行为实验中被试数量有限，任务简化；ImageBeagle依赖ResNet特征空间，可能在部分图像类型上搜索质量下降。尽管如此，上述发现清楚地表明，反偏好刺激是视觉编码的“另一条尾巴”，将完整编码机制带入视野，也为改进下一代神经拟态网络提供了明确的生物学约束。



理解灵长类视觉皮层如何编码自然视觉刺激是计算神经科学的核心目标。传统的线性-非线性模型和深度神经网络单元通常假设神经元主要通过偏好刺激来编码信息——即那些能最大程度激活神经元的刺激。这种单尾响应分布意味着反偏好刺激仅被视作无信息的背景活动。

然而，这种模型与生物视觉系统之间存在显著的**表征差距**。对恒河猴V4区219个神经元的分析显示，其自然图像响应分布呈现显著的双尾特性：偏度中位数κ仅为0.87，远低于ResNet50单元的2.06（Figure 1c, p<0.002）。这一差距也存在于V1区（κ=1.17，Figure 1d），表明双尾编码可能贯穿视觉层级，而当前深度网络尚无法复现该特性。

双尾分布意味着V4神经元不仅能被偏好图像强烈激活，还能被反偏好图像显著抑制到基线以下——这些反偏好图像并非无特征的灰屏，而是具有丰富视觉特征的图像。更重要的是，**数据剪枝实验**揭示了反偏好刺激是完整刻画神经元调谐函数的必要条件：仅用偏好图像训练时，模型对神经元响应的泛化预测性能显著下降；同时使用偏好与反偏好图像才能获得最优的预测精度（Figure 3b）。这一发现挑战了仅用偏好刺激建模神经元调谐的主流做法，提示**缺失半边分布会导致对编码机制的片面理解**。

值得关注的是，偏好特征与反偏好特征在图像统计上几乎无法区分，且在不同神经元之间不共享（Figure 5a-b, Supp. Figure 7），这暗示每个V4神经元通过编码两个相对独立的视觉特征，使群体的特征选择性容量约翻倍（压缩比=2.5，Figure 5h）。这种编码策略在当前深度神经网络的ReLU激活架构中天然缺失，揭示了人工系统与生物系统在表征效率上的关键差异。

本文的动机在于系统量化、实验验证与机制阐明V4神经元的反偏好编码现象，填补现有模型无法完整捕捉视觉神经元调谐特性的这一关键缺口。



## 核心方法与创新机理

本研究的核心创新在于发现并验证了灵长类视觉皮层V4区神经元对自然图像存在**双尾响应分布**，并提出了**Linear-ReLU-Linear (LRL) 映射**以捕捉这种编码机制。

### 瓶颈：传统模型的单尾局限

传统线性-非线性模型（LN）和深度神经网络单元（如ResNet的ReLU层）对自然图像的响应分布呈现显著的**单尾特性**：神经元主要被偏好刺激激活，对反偏好刺激（anti-preferred stimuli）的响应被ReLU非线性截断为零，无法形成低于基线的抑制性调制。数据显示，DNN单元（ResNet50）的响应偏度中位数 $\kappa=2.06$，远高于V4神经元的 $\kappa=0.87$（p<0.002，Figure 1c）。这导致传统模型无法完整捕捉V4神经元的真实调谐函数，从根本上限制了预测精度和生物逼真度。

### 因果机制：反偏好刺激是调谐的必要组分

通过数据剪枝实验，研究明确了一个因果结论：**反偏好图像是估计V4调谐函数不可或缺的组成部分**。当训练集仅包含偏好图像（pref-only）或仅包含反偏好图像（anti-pref-only）时，学生网络对V4模型神经元响应的泛化 $R^2$ 显著低于随机选择图像训练（Figure 3b）。而偏好与反偏好图像联合训练（pref+anti-pref）的性能最优，超过同等数量的随机图像，证明这两种图像类型在信息上互补且不可相互替代。

### 关键架构改变：LRL映射替代post-ReLU线性映射

| 对比维度 | Baseline：post-ReLU 线性映射 | Proposed：LRL 映射 |
|---------|--------------------------|-------------------|
| **特征来源** | ReLU激活后的DNN特征（保留偏好，丢弃反偏好信息） | Pre-ReLU特征（同时保留激发与抑制性信息） |
| **架构** | 单一线性映射（Ridge回归） | 1×1卷积（通道间线性组合）→ ReLU → 最终线性映射 |
| **双尾表达能力** | 仅形成单尾分布 | 允许高低值共同塑造输出，支持双尾预测 |

核心操作在于：先对pre-ReLU特征进行**通道级别的线性重组**（1×1卷积，输出通道数等于输入通道数），再将重组后的信号通过ReLU激活，最后接一个线性映射预测V4响应。这一结构使模型能够重新定义“偏好”与“反偏好”的特征组合方式，而非被动接受DNN原始通道的定义。实验表明，该映射使pre-ReLU特征的预测能力从低于post-ReLU基线提升至与其相当的水平（Figure 2a，model iv vs. model i），且当随机翻转特征符号时，LRL映射依然能够自适应调整（Supplementary Figure 1d,e）。

### 核心洞察：双尾编码使群体特征容量翻倍

偏好图像与反偏好图像在颜色、纹理等底层统计上几乎无法区分，且不同V4模型神经元的偏好/反偏好集合之间不存在线性共享关系（Figure 5a,b；Supplementary Figure 7）。这意味着每个V4神经元编码了两个**独立的视觉特征**。量化分析表明，若将V4模型神经元的响应分布截断为单尾（仅保留偏好尾），需要约2.5倍数量的单元才能在下游物体识别任务中恢复原有精度（Figure 5h，压缩比=2.5），而pre-ReLU DNN单元的压缩比仅为1.6。这证明双尾编码使群体特征选择性容量实现了近两倍的提升，揭示了一种现有DNN中不存在的表征策略。



![[assets/figures/papers/iclr26_0004_RZ8esDBqMJ_A_tale_of_two_tails_Preferred_and_anti-preferred/figures/016_Figure_6.jpg]]
*Figure 6: ImageBeagle searches the natural image manifold to efficiently find preferred and anti-preferred stimuli. a. A V4 model neuron’s responses to preferred and anti-preferred images after searching through a subsample of K images. Dashed-lines: linear fits; x-axis is log-scale. Right: Top preferred and anti-preferred images for each K as well as synthesized images. b. ImageBeagle navigates the natural image manifold via a nearest neighbor graph. c. Runs of Image-Beagle (orange traces) versus random selection (black traces) searching for the preferred (top) and anti-preferred (bottom) image. Dashed lines: optimal out of 30M images. d. ImageBeagle tuning curve for a V4 model neuron*

本研究围绕“V4 神经元不仅编码偏好刺激，还编码反偏好刺激（anti‑preferred stimuli）”这一核心发现，构建了一套从量化表征、建模验证、信息剪枝到人类行为与群体容量分析的完整分析流程。整体管线以清醒狨猴的 V4 电生理记录为中心，将自然图像与响应对作为输入，逐步揭示双尾调谐特性，最终提供可高效搜索偏好/反偏好图像的工具。

管线的逻辑链和模块关系可概括如下：

**1. 双尾响应分布的量化（Figure 1）**  
对 V4 神经元在大量自然图像上的重复平均发放计数，计算偏度 $κ$ 以刻画响应分布的单尾/双尾程度。这一模块提供核心量化事实：V4 神经元偏度中位数为 0.87，显著低于深度网络单元（2.06），确证了其双尾性质，而 DNN 的 ReLU 非线性导致分布近似单尾。

**2. 预测性映射与 LRL 架构**  
此模块解决“前激活特征能否完整捕获双尾信息”的问题。常规做法是使用 post‑ReLU 特征线性回归预测 V4 响应，但该方法丢弃了抑制性信号。为此提出 Linear‑ReLU‑Linear (LRL) 映射：先对 pre‑ReLU 特征进行 $1\times1$ 卷积（通道间线性组合），再经过 ReLU，最后接线性预测。该架构使 pre‑ReLU 特征的预测性能与 post‑ReLU 相当，表明双尾信息确实蕴含在前激活空间中（Figure 2a, model iv vs. i）。LRL 不是最终模型神经元，而是验证预激活信息可用性的桥梁。

**3. 数据驱动的 V4 模型神经元训练**  
利用已知图像‑响应对训练深度神经网络（仿生 V4 模型神经元），使其逼近真实神经元的响应函数（Methods A.1）。这些模型神经元是后续合成、搜索偏好/反偏好图像、数据剪枝以及心理物理学实验的“教师”或靶标。它们的响应范围可正可负，能够再现双尾分布（例如一个模型神经元对合成偏好和反偏好图像的预测响应为 $r_{\mathrm{max}}=6.5$，$r_{\mathrm{min}}=-3.5$）。

**4. 偏好与反偏好图像的实验验证（Figure 2b–d）**  
用训练好的 V4 模型神经元在大型自然图像池中搜索响应最大和最小的图像，随后在新的清醒猴记录中直接回验这些图像。结果表明模型预测的偏好图像诱发的响应均值位于随机图像响应的 98.5% 分位数以上，反偏好图像则位于 5.5% 分位数以下，证实了反偏好刺激可在体内可靠地抑制基线发放。该模块完成了从模型预测到生物验证的闭环。

**5. 数据剪枝分析（Figure 3）**  
为了量化偏好与反偏好图像在调谐估计中的信息贡献，采用数据剪枝范式：仅用偏好图像、仅用反偏好图像、二者结合或随机子集训练学生网络来拟合 V4 模型神经元的输出。联合训练的效果最优，而单一训练集的泛化能力显著下降（Figure 3b），说明两类刺激都是 V4 调谐函数不可或缺的组成部分。该模块同样用于评估 DNN 单元，揭示其 pre‑ReLU 特征仍需两类训练样本才能逼近真实生物单元的信息使用模式。

**6. 人类心理物理学与在线分类器（Figure 4）**  
设计“图像二选一”任务，让人类被试推断 V4 模型神经元的调谐函数，同时训练递归最小二乘（RLS）在线分类器作为对照。实验显示，同时提供偏好和反偏好图像时，被试的平均正确率可达 80.5%，而缺少反偏好信息时正确率显著下降。RLS 分类器（基于预训练视觉特征）可在线模拟人类学习过程，表明人类可在有限试次内有效利用反偏好信号进行神经元调谐的推断。

**7. 特征选择性翻倍分析（Figure 5）**  
通过将 V4 模型神经元响应截断为单尾（仅保留偏好或反偏好侧），测定下游线性分类器在物体识别任务上的精度损失。结果发现，为恢复原始精度所需单尾单元数约为原始双尾单元数的 2.5 倍（压缩比），即双尾编码使群体的特征选择性容量翻倍。偏好与反偏好图像在可解释视觉特征上无法区分，且不同模型神经元的偏好集合不共享，进一步证明这种容量增益并非来自简单图像统计的冗余。

**8. ImageBeagle：自然图像流形的高效搜索工具（Figure 6, Table 1）**  
为支持上述闭环实验中的快速图像搜索，开发 ImageBeagle 工具。它基于 3000 万张多源自然图像（包含数据集、网络爬取和人工刺激，详见 Table 1）的 ResNet50 近邻图，交替进行全局核心集搜索与局部爬山遍历。该方法能在评估约 1 万张图像后找到与全量 3000 万张图像最优响应接近的偏好/反偏好图像，比随机搜索效率大幅提升。ImageBeagle 是前述模块（尤其是实验验证和模型神经元的图像选择）的关键使能技术。

**整体输入输出流**概括为：  
- **输入**：自然图像刺激集合；清醒弥猴 V4 区多电极 spike 记录（重复平均计数作为单次试验响应）。  
- **中间表示**：偏度 $κ$；V4 模型神经元的响应预测；LRL 映射权重；偏好/反偏好图像列表；人类行为数据。  
- **输出**：实验验证的分位数度量、数据剪枝的泛化 $R^{2}$、人类正确率、群体压缩比、以及 ImageBeagle 搜索到的近似最优刺激。  

这些模块层层递进：先证实现象存在，再建立可操控的模型，继而通过剪枝和人类实验确认信息必要性，最后量化群体层面的容量增益并提供实用工具。整体框架呈现出“数据驱动建模 → 闭环实验验证 → 信息分解 → 容量分析”的串行与反馈环路。需要注意的是，部分分析（如人类心理物理学被试人数有限，以及 ImageBeagle 搜索性能受限于 ResNet50 嵌入空间）存在边界条件，具体解释需结合实际实验设置进行判断。



本文将V4神经元的双尾响应特性解析为若干可操作的模块，并配合关键量化指标与映射策略，构建了从现象发现到机制验证的完整分析链。以下聚焦各模块的驱动力和控制变量，以及核心公式的变量含义。

### 1. 响应分布双尾性量化模块
**机制**：计算V4神经元与DNN单元对大量自然图像的响应分布偏度κ，直接揭示传统线性‑非线性模型与深度网络缺失的反偏好信号。V4神经元对自然图像的分布呈显著双尾（中位数κ≈0.87），而ResNet50的ReLU单元呈典型单尾（中位数κ≈2.06）。  
**因果杆杠**：通过同一图像集上的偏度对比（Figure 1c），配合置换检验（p<0.002），证明双尾特征并非图像采样偏差，而是神经元自身调谐特性。  
**证据锚点**：Figure 1c, d。

### 2. 线性‑ReLU‑线性（LRL）映射模块
**背景与瓶颈**：直接使用DNN预激活（pre‑ReLU）特征的线性回归保留双尾信息，但预测V4响应的能力弱于后激活（post‑ReLU）映射（Figure 2a, model i vs. ii），说明简单线性解码无法充分提取双尾编码。  
**LRL映射设计**：在pre‑ReLU特征后插入一个**通道间线性组合（1×1卷积，输出通道数同输入）**，后接ReLU激活，再通过一个最终线性层预测V4响应。  
**核心变化**：从 `pre‑ReLU → Ridge` 变为 `pre‑ReLU → Conv1×1 → ReLU → Linear`。该结构允许模型自适应地重组通道，将负激活转化为后续ReLU可通过的正值，从而恢复反偏好特征的线性解码能力，使pre‑ReLU特征的预测性能达到与post‑ReLU相当的水平（Figure 2a, model iv）。该映射还具备符号翻转鲁棒性（Supplementary Figure 1）。  
**证据锚点**：Figure 2a (models i–v), Supplementary Figure 1。

### 3. 数据剪枝分析模块
**机制**：以训练好的V4模型神经元作为教师，用不同训练子集（仅偏好图像、仅反偏好图像、二者组合、随机挑选）训练5层学生CNN，评估其在独立自然图像上的泛化R²。  
**控制变量**：直接操纵反偏好图像是否存在于训练集，观察它对调谐函数估计的必要性。  
**关键发现**：`pref+anti-pref` 联合训练的性能显著优于随机选择（`random`），而单独使用任一尾的图像导致泛化性能下降，证明反偏好与偏好图像都是准确估计V4调谐所必需的 (Figure 3b)。  
**证据锚点**：Figure 3。

### 4. 偏好/反偏好图像实验验证模块
**实验链路**：使用数据驱动的V4模型神经元在大图像池中搜索使预测响应最大（偏好）和最小（反偏好）的自然图像，随后在恒河猴V4电生理记录中验证这些图像的真实调控效果（Figure 2b）。  
**关键公式**

- **偏好（或反偏好）图像响应分位数**：用于量化特定图像在随机自然图像响应分布中的位置，反映其激发或抑制强度。
  $$ q_{\mathrm{pref}} = \frac{1}{N} \sum_{i=1}^{N} \mathcal{I}(r_{\mathrm{pref}} > r_i) $$
  其中，$r_{\mathrm{pref}}$为偏好图像的中位响应，$r_i$为第$i$张随机自然图像的响应，$\mathcal{I}(\cdot)$为指示函数。类似定义用于反偏好图像$q_{\mathrm{antipref}}$。

- **双尾响应跨度示例**：一个V4模型神经元对合成偏好和反偏好图像的预测响应极值，直观展现双尾分布的活动幅度。
  $$ r_{\max} = 6.5, \quad r_{\min} = -3.5 $$

**实验结果**：偏好图像的中位响应位于随机图像分布的$q_{\mathrm{pref}} = 0.985$（高于90%密度区间上界），反偏好图像位于$q_{\mathrm{antipref}} = 0.055$（低于下界），置换检验p<0.001（Figure 2b）。自然搜索图像比合成图像产生更强的反偏好抑制（Supplementary Figure 5b）。  
**证据锚点**：Figure 2b, d; Supplementary Figure 5; Methods A.1。

### 5. 特征选择性翻倍分析模块
**机制**：将V4模型神经元的响应分布人工截断为单尾（仅保留偏好尾或反偏好尾），训练下游线性分类器执行物体识别，测量达到原双尾精度所需的单尾单元数量。  
**核心指标**：压缩比 = 原始双尾单元数 / 所需等效单尾单元数。V4模型神经元的压缩比高达2.5，远超出pre‑ReLU DNN单元的1.6 (Figure 5h)，表明偏好与反偏好特征相互独立，使群体特征选择性容量约翻倍。  
**证据锚点**：Figure 5。

### 6. ImageBeagle自然图像搜索工具
**机制**：基于3000万张图像的ResNet50特征构建近邻图，交替进行全局核心集搜索与局部爬山，高效搜寻最大化/最小化模型神经元响应的自然图像。  
**效率体现**：仅需评估约10k图像即可接近30M图像池的理论最优响应（Figure 6c, 橙色 vs. 黑色曲线），为闭环电生理实验提供实时图像合成了基础。  
**证据锚点**：Figure 6; Methods A.6, A.7。

以上模块共同将反偏好刺激从一种现象固化为V4编码的独立功能维度，LRL映射提供了从预激活特征中恢复双尾信息的可行方案，分位数公式则将双尾响应操作化，支撑了闭合式实验验证。



## 实验与关键发现

### 主结果：V4神经元的双尾响应特性

本研究首先量化了灵长类视觉皮层V4区神经元对大规模自然图像集的响应分布特性。以219个V4神经元的重复平均放电计数（刺激起始后100 ms窗口）为对象，计算偏度κ来刻画分布的双尾程度。结果显示，V4神经元的中位数偏度仅为κ=0.87，而深度网络单元（ResNet50）的中位数偏度高达κ=2.06（p<0.002，排列检验，Figure 1c）。这一对比直接揭示出传统线性-非线性模型和DNN单元响应分布的瓶颈：它们普遍呈现单尾分布（κ接近2），即仅编码偏好刺激而忽略反偏好刺激；真实V4神经元则表现出显著的双尾分布（κ接近0），表明其调谐函数同时包含偏好与反偏好两个分量。扩展分析进一步表明，颞叶更前部的V1区域同样表现出双尾选择性（κ=1.17），而不同DNN层级的偏度均维持在较高水平（Figure 1d）。

基于上述发现，数据驱动的V4模型神经元所搜索到的偏好与反偏好自然图像在后继电生理记录中得到了严格验证。将模型预测的偏好和反偏好图像呈现给真实V4神经元，其诱发的响应分别位于随机自然图像响应分布的90%分位数以上（偏好图像分位数q≈0.985）和10%分位数以下（反偏好图像分位数q≈0.055），两者均显著超出随机图像响应的90%密度区间（排列检验p<0.001，Figure 2b）。这一实验证据确认了反偏好图像具有真实的抑制功能，能够将神经元活动压低至基线以下。注意到模型合成图像与自然搜索图像在偏好端诱发的响应无显著差异（p=0.514），但在反偏好端，自然图像诱发的响应显著低于合成图像（p<0.02，Supp. Fig. 5），意味着自然图像池中包含比合成刺激更强的抑制信号。


![[assets/figures/papers/iclr26_0004_RZ8esDBqMJ_A_tale_of_two_tails_Preferred_and_anti-preferred/figures/014_Figure_5.jpg]]
*Figure 5: Anti-preferences double a V4 population’s capacity for feature selectivity. a. Visual features differ between preferred and anti-preferred images. b. Mean differences in features that were normalized between 0 and 1. Lines: medians, dots: V4 model neurons. c. Simulated preferred and anti-preferred orientations for a population of V1 neurons. Shuffling these preferences breaks specific relationships. d. Neighbor overlap for predicting the anti-preferred features using preferred features for simulated V1 neurons for each condition in c. e. Same as d but with V4 model neurons using interpretable visual features. f. We assess the extent to which different tailed response distributions perform o...*

### 关键消融实验

#### 特征映射架构与预激活信息的利用

为了探究双尾信息在预测中的可用性，以预激活（pre-ReLU）ResNet50特征出发构建了六种线性映射模型的对比（Figure 2a）。直接将pre-ReLU特征进行岭回归（model i）或取负后通过ReLU仅保留反偏好特征（model iii）的预测性能均低于标准的后激活（post-ReLU）线性映射（model ii）。本研究提出的Linear-ReLU-Linear (LRL)结构——先对pre-ReLU特征进行1×1卷积（通道数等于输入通道数），再通过ReLU激活，最后接线性映射——使pre-ReLU特征的预测R²与post-ReLU持平，有效弥补了两者之间的差距（Figure 2a，模型iv vs. 模型i–ii）。重要的是，当随机翻转特征符号时，LRL映射凭借其通道线性组合的灵活性，仍能维持预测性能，而标准后激活映射则完全失效（Supp. Fig. 1d–e）。这一消融证明了编码反偏好信息所需的并非简单的线性保留，而是需要可学习的通道重组机制来分离偏好与反偏好特征分量。

#### 训练数据剪枝：反偏好图像的不可或缺性

数据剪枝分析是检验反偏好信息因果必要性的关键操作。以V4模型神经元作为教师模型，用不同训练子集——仅偏好图像（pref-only）、仅反偏好图像（anti-pref-only）、偏好与反偏好联合（pref+anti-pref）、随机选择（random）及非偏好图像（exclude pref）——训练5层CNN学生网络来估计调谐函数，评估其在独立测试集上的泛化R²（Figure 3b）。结果表明：仅使用偏好图像或仅使用反偏好图像训练的泛化R²均低于随机选择子集，而偏好与反偏好联合训练的性能在所有条件下最优。这一效应在训练图像数量从1k扩大到300k时保持稳健（Supp. Fig. 2），证实反偏好图像并非可以被忽略的噪声尾部，而是构成神经元调谐函数的必要信息组分。相比之下，对ResNet50 post-ReLU单元施加同样的数据剪枝时，偏好与反偏好联合训练的优势明显减弱，进一步确认了DNN单元表征中反偏好信息的缺失（Figure 3c）。


![[assets/figures/papers/iclr26_0004_RZ8esDBqMJ_A_tale_of_two_tails_Preferred_and_anti-preferred/figures/005_Figure_2.jpg]]
*Figure 2: Experimental evidence that V4 neurons have anti-preferred images. a. Predicting V4 responses to randomly-chosen images from a linear mapping of ResNet-50 features. Each dot denotes the median, and error bars denote 1 s.e.m. b. Experimental validation of preferred and anti-preferred images as predicted by V4 model neurons. Each dot is the repeat-averaged V4 response to one image; gray bands denote 90% percentiles of responses to randomly-chosen natural images. Insets: Model-chosen images for the 3 V4 neurons with largest baseline responses. c. Top: Repeat-averaged temporal response of an example V4 neuron (PSTH). Bottom: Normalized response to preferred, anti-preferred, and following blank i...*

#### 人类推断实验：反偏好信息的行为价值

心理物理学任务为反偏好图像的信息贡献提供了行为层面的验证（Figure 4）。在二选一任务中，人类被试需要判断哪张图像能诱发V4模型神经元更强的响应。当同时获知偏好和反偏好图像作为先验（both condition）时，被试对V4模型神经元的预测正确率达到平均80.5%（Figure 4c）；而仅获知偏好图像时正确率显著下降，对DNN单元的预测正确率同样更低（Figure 4d）。作为计算参照，基于视觉特征的递归最小二乘在线分类器在获得均等先验信息时呈现出与人类相似的正确率曲线（Figure 4e）。


![[assets/figures/papers/iclr26_0004_RZ8esDBqMJ_A_tale_of_two_tails_Preferred_and_anti-preferred/figures/013_Figure_4.jpg]]
*Figure 4: Humans use anti-preferred images to infer V4 tuning. a. Psychophysics task. b. Performance for one example user with or without prior information. Each trace is the running difference between the number of correct and incorrect choices for one V4 model neuron. c-d. Human performance predicting V4 model neurons (c) and ResNet50 DNN units (d). e-f. Task performance in a for an online classifier trained on visual features (e) or on CLIP embeddings (f). Lines: mean, shade: 1 s.e.m*

#### 群体特征容量翻倍：双尾编码的计算优势

调节响应分布尾数对下游识别任务的影响量化了双尾编码的群体计算优势（Figure 5f–h）。将V4模型神经元的响应分布截断为仅保留偏好尾后，基于该群体响应的线性分类器在物体识别上的精度显著下降。恢复原始精度需要约2.5倍数量的单尾单元（V4模型神经元压缩比=2.5），而pre-ReLU DNN单元的压缩比仅为1.6（Figure 5h）。这表明偏好特征与反偏好特征在群体层面近似独立编码，使每个神经元的有效特征选择性容量接近翻倍。在图像统计层面，偏好与反偏好图像的颜色、纹理等可解释视觉特征无法显著区分（Figure 5a–b，Supp. Fig. 7）；且不同V4模型神经元的偏好图像集合不共享（Supp. Fig. 7c），利用偏好图像的最邻近特征预测反偏好图像亦近乎随机水平（Supp. Fig. 8），排除了该双重选择性由共享底层统计驱动的可能。

### 实验工具：自然图像流形的高效搜索

闭环实验对高效搜索偏好与反偏好刺激的需求催生了ImageBeagle搜索工具（Figure 6）。该工具基于3000万张图像构建近邻图（ResNet50特征空间，Supp. Fig. 3），交替执行全局核心集探索（全局搜索）与局部爬山式近邻遍历（局部搜索）。在不使用合成优化的情况下，ImageBeagle仅需评估约10k张图像即可逼近30M图像池中最优偏好与反偏好图像，显著优于随机搜索（Figure 6c中橙色 vs. 黑色曲线）。搜索效率的基准对比及调谐曲线示例见图6c–d。


![[assets/figures/papers/iclr26_0004_RZ8esDBqMJ_A_tale_of_two_tails_Preferred_and_anti-preferred/figures/008_Figure_3.jpg]]
*Figure 3: Anti-preferred images contribute to V4 tuning. a. Response distributions for different training sets for a data pruning analysis; R2 is always computed with the same held-out natural images. b. We train a 5-layer DNN (see Methods A.3) to predict responses of individual V4 model neurons (219 in total), varying the number of training images up to 10k (see Supp. Fig. 2 for results with > 10k images). Response distributions were over 500k images; we also considered a distribution for 1 million (1M) images. c. We perform a data pruning analysis for 219 ResNet50 units (2k training images), either pre-ReLU (left) or post-ReLU (right), as well as ReLU thresholds equal to different quantiles (e.g.,...*

### 局限与待验证问题

本研究集中于V4区域，尚未系统验证反偏好编码贯穿整个视觉层级（V1、IT初步分析结果外推需谨慎）。人类心理物理学实验的被试数量及任务复杂度有限，推断行为与真实神经元调谐过程之间的差距仍须审慎解读。ImageBeagle的近邻质量完全依赖ResNet50嵌入空间，对未能被该空间良好区分的图像类型可能失效。此外，V4模型神经元虽能较好预测响应，但作为黑盒模型，其内部表征与真实生物机制的对齐程度有待进一步追踪实验验证。关于双尾编码与高效编码理论、稀疏编码假说的关系，以及是否可通过脉冲时序依赖可塑性等学习规则自发形成此类配对选择性，仍为开放问题。

### 补充图表

![[assets/figures/papers/iclr26_0004_RZ8esDBqMJ_A_tale_of_two_tails_Preferred_and_anti-preferred/figures/004_Figure_1.jpg]]
*Figure 1: V4 neurons have two-tailed response distributions. a. Response distributions for a linear-nonlinear filter (top), DNN unit (middle), and a real neuron from visual area V4 (bottom). b. Anti-preferred and preferred images of an example V4 neuron. c. Skewness κ of response distributions for V4 neurons and DNN units. d. Skewness κ of response distributions for different visual areas in macaque (top), and DNN layers (bottom). Dashed lines: medians*




## 定位与知识库关联

### 与基线方法的关系

本研究揭示V4神经元的响应分布具有显著的双尾特征（偏度$\kappa = 0.87$，图1c），这直接挑战了传统线性‑非线性（LN）模型与标准深度卷积网络（如ResNet‑50）中隐含的单尾假设。基线方法——即从ReLU激活后的特征到V4响应的直接线性映射（post‑ReLU linear mapping）——隐含地假定神经元的调谐仅由正激活的“偏好”特征决定，因此天然无法捕捉反偏好（抑制性）信息。本工作提出的Linear‑ReLU‑Linear（LRL）映射（图2a, model iv）为此提供了一个关键的方法论转折：它在ReLU之前插入了一个通道间的线性组合（1×1卷积），使得预激活特征能够被“重新混合”并形成新的、既可正也可负的有效分量，从而保留双尾信息，最终预测V4响应的性能与使用post‑ReLU特征相当，同时允许模型明确表达抑制性调谐。这一设计表明，**反偏好刺激并非前馈通路中不可使用的信号残余，而是可以通过合适的特征重组织来等价表达的**，填补了从预激活特征到生物响应之间的表征鸿沟。

与同时考察的其他基线对比更能突显LRL的定位：
- **pre‑ReLU线性映射**（model i）：直接对预激活特征执行线性回归，尽管保留了双尾信息，但预测噪声显著高于post‑ReLU，说明原始预激活特征中的符号分布并不直接对应生物抑制的结构。
- **negated‑ReLU线性映射**（model iii）：仅保留预激活特征的负值并通过ReLU，与仅使用偏好信息的post‑ReLU形成互补；二者分别代表单尾信息的两个极端，联合使用才组成双尾完整信息，但性能仍不及LRL的联合表达。
- **剪枝实验**（图3b）进一步巩固了这一结论：仅用偏好图像或仅用反偏好图像训练的模型泛化性能均低于随机采样，而两者联合则显著最优，证明**反偏好图像不是调谐的冗余副产物，而是构成精确调谐的必要成分**。

因此，本工作在方法谱系中的位置是：**在已有的预激活特征线性映射和分离式单尾映射之间，引入了一个可学习的双尾映射（LRL），使得深层网络的预激活单元能够直接作为V4双尾调谐的替代表征，而不需要显式建模两个独立的前馈通路**。

### 适用边界

本研究的方法与结论主要建立在对两只清醒猕猴V4区电生理数据的分析之上，并部分地通过公开数据集复现（Cadena et al. 2019; Majaj et al. 2015）。其适用边界由以下因素界定：

1. **脑区特异性**：偏度分析和实验验证的中心是V4。虽然图1d暗示V1也有一定的双尾倾向（$\kappa = 1.17$），但尚未在整条腹侧通路（特别是更高层的IT）开展系统的实验验证与数据剪枝。因此，反偏好刺激作为调谐必要成分的结论是否泛化到全皮层，仍需要直接证据。
2. **模型依赖性**：所构建的V4模型神经元本质上是数据驱动的深度网络暗箱（5层CNN、ResNet‑50基特征），其对反偏好特征的编码方式可能与真实生物环路存在偏差。例如，合成图像（图2d）的抑制效果弱于从自然图像池中选出的反偏好图像（见补充材料图5b），说明模型未能穷尽自然刺激空间中的抑制特征。
3. **图像搜索空间的局限**：ImageBeagle工具依赖ResNet‑50特征构建的近邻图来遍历自然图像流形。此嵌入空间虽然能有效捕获视觉相似性，但对于超出该空间表征能力的图像类型（如某些纹理、抽象构图），其搜索性能可能下降，导致无法找到真实的全局最优刺激。
4. **特征独立性检验的不完备性**：用于证明偏好与反偏好特征独立性的可解释视觉特征集合（34维或CLIP嵌入）可能遗漏某些高阶统计量（如高阶相关性）。若存在此遗漏，则“两套特征完全不共享”的结论可能低估了它们之间的潜在耦合。

### 局限与待验证问题

尽管本文的证据链相当严密（从分布量化到实验验证、剪枝分析、人类行为再到群体容量增益），以下几处仍需要手动审慎评估或由后续工作补全：

- **人类实验的被试规模与生态效度**：心理物理学任务（图4）被试数量有限，且任务简化为一维调谐推断。尽管80.5%的预测正确率令人印象深刻，但真实场景中人类推断神经元表征的能力是否同样依赖反偏好信息，尚无法从当前设计强推断。
- **双尾编码的因果功能**：研究展示了双尾编码使群体表征容量翻倍（图5h，压缩比2.5），但这建立在将响应分布截断为单尾的下游分类任务上。真实识别过程中，高级皮层（如IT）是如何读取并利用V4群体的抑制性维度的，这一点并未给出机制性答案。换句话说，双尾编码的**下游解码算法**仍是一个开放问题。
- **学习起源**：双尾调谐是先天结构还是通过特定可塑性规则（如STDP）涌现的？预激活单元的双尾特征是否可以经由在网络训练中引入新的约束（例如强制响应分布的对称性）而获得？当前分析未能回答。

### 开放问题与知识库定位

本研究在神经科学与机器学习交叉点上打开了一组核心问题，使其自然成为后续工作的出发点：

- 双尾响应分布与高效编码、稀疏编码理论的关系：脑是否通过配对偏好与反偏好特征来最大化刺激辩识的Fisher信息或最小化能量消耗？这一问题的解决可能需要联结本研究与早期的抑制‑共轭编码假说。
- 能否在深度网络架构中显式引入“双尾激活”（例如可学的负斜率ReLU，或对预激活特征进行符号感知的压缩），使网络自发形成类似V4的选择性，从而缩小表征差距？现有的LRL映射只是后验证明双尾信息可用，并非训练范式上的导入。
- 偏好与反偏好图像在视觉统计上几不可区分（图5a,b，补充图7），说明它们编码了更高阶的语义或结构特征。如何从海量特征中系统发现这些特征的归纳偏置，将直接推动可解释人工智能的发展。
- ImageBeagle的搜索框架能否被推广到其他感觉模态（如听觉、体感），用于快速定位神经元的刺激响应峰值与谷值？其成功与否也将反向检验“自然刺激流形假设”的普适性。

综上，本工作确立了一条明晰的知识库线索：**V4神经元的双尾调谐不仅是一个现象，更是一个迫使重新思考前馈模型和表征容量的支点**。它桥接了传统的单尾调谐模型与未来可区分的双尾编码模型，并将该问题的后续进展建立在对抑制性特征的计算本质的理解之上。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_tale_of_two_tails_Preferred_and_anti_preferred_natural_stimuli_in_visual_cortex.pdf

![[paperPDFs/ICLR_2026/A_tale_of_two_tails_Preferred_and_anti_preferred_natural_stimuli_in_visual_cortex.pdf]]
