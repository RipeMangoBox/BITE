---
title: "UDAPose: Unsupervised Domain Adaptation for Low-Light Human Pose Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UDAPose_Unsupervised_Domain_Adaptation_for_Low_Light_Human_Pose_Estimation.pdf
code_link: "https://github.com/VMIL/UDAPose"
aliases:
- UDAPose
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过DHF保留并重定中心高频细节，结合LCIM多尺度注入低光特性，合成出既保留结构又富含真实噪声的低光训练数据；同时引入DCA，自适应地为每个关键点分配图像线索与姿态先验的权重，抑制不可靠视觉信息，强化学习到的姿态先验。
primary_logic: 利用未配对低光参考图像的高频信息，在稳定扩散解码过程中进行内容感知的精细注入，生成高度逼真的低光增强样本；并构建逐关键点的竞争性注意力融合，使模型能够根据当前视觉质量动态调整信息来源，从而在极端低光下依然保持姿态的解剖学一致性。
claims:
- 在ExLPose-test的LL-H子集上，UDAPose最终达到28.0 AP，比最佳基线CycleGAN的17.9 AP提升10.1 AP，相对提升高达56.4%。
- 在跨数据集验证EHPT-XC上，UDAPose取得31.0 AP，相比ELLA的23.6 AP提升7.4 AP，相对提升31.4%。
- 消融实验证实，单独加入LCIM使得LL-H上的AP从7.2提升至20.7，加入DHF再提升至25.3，最终加入DCA后达到28.0，各模块均贡献显著。
- "ExLPose-test (LL-A - all low-light) 上 mAP @.50:.95 = 27.0"
---

# UDAPose: Unsupervised Domain Adaptation for Low-Light Human Pose Estimation

> [!tip] 核心洞察
> 利用未配对低光参考图像的高频信息，在稳定扩散解码过程中进行内容感知的精细注入，生成高度逼真的低光增强样本；并构建逐关键点的竞争性注意力融合，使模型能够根据当前视觉质量动态调整信息来源，从而在极端低光下依然保持姿态的解剖学一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | UDAPose：面向低光照人体姿态估计的无监督域自适应 |
| 英文题名 | UDAPose: Unsupervised Domain Adaptation for Low-Light Human Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.10485) · [Code](https://github.com/VMIL/UDAPose) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UDAPose |
| Dataset | ExLPose-test, ExLPose-OCN, EHPT-XC |

> [!tip] 效果简介
> - ExLPose-test (LL-A - all low-light) 上，mAP @.50:.95 27.0 vs 19.6 (CycleGAN) (+7.4 (37.8% rel.))。
> - ExLPose-test (LL-H - hard subset) 上，AP @.50:.95 28.0 vs 17.9 (CycleGAN) / 17.2 (ELLA) (+10.1 (56.4% rel.))。
> - ExLPose-test (LL-E - extreme subset) 上，AP @.50:.95 11.7 vs 3.4 (ELLA) (+8.3 (244% rel.))。

## 概述

低光照条件下，人体姿态估计面临视觉信息严重退化的瓶颈：现有域自适应方法难以准确再现真实低光的高频噪声特性，而主流单阶段姿态估计器（如ED-Pose）在解码器中采用刚性残差求和机制，使模型过度依赖不可靠的图像线索，导致性能骤降。

**UDAPose** 针对上述瓶颈，提出两条因果路径：在数据层面，通过**DHF（Direct-Current-based High-Pass Filter）**保留并重定中心高频细节，结合**LCIM（Low-Light Characteristics Injection Module）**多尺度注入低光特性，利用未配对低光参考图像在稳定扩散解码过程中合成既保留结构又富含真实噪声的低光训练数据；在模型层面，引入**DCA（Dynamic Control of Attention）**模块，自适应地为每个关键点分配图像线索与姿态先验的竞争权重，抑制不可靠视觉信息，强化学习到的姿态先验。

在 **ExLPose-test** 基准上，UDAPose在LL-H（困难低光子集）上达到28.0 AP，相较最佳基线CycleGAN的17.9 AP提升10.1 AP（相对提升56.4%）；在LL-E（极端低光子集）上达到11.7 AP，相较ELLA的3.4 AP提升244%。跨数据集验证 **EHPT-XC** 上取得31.0 AP，较ELLA的23.6 AP提升7.4 AP（31.4%）。消融实验证实，LCIM、DHF和DCA三个模块各自贡献显著：单独加入LCIM将LL-H上的AP从7.2提升至20.7，加入DHF再提升至25.3，最终加入DCA后达到28.0。

方法定位上，UDAPose区别于传统的图像增强预处理（如DarkIR、QuadPrior）和非配对图像翻译（如CycleGAN、UNIT），后者无法忠实再现低光噪声的高频统计特性；也不同于ELLA等仅依赖数据增强的低光姿态估计方法，UDAPose通过DCA实现了逐关键点的图像线索与姿态先验动态平衡，在极端低能见度下仍保持解剖学一致性。

## 背景与动机

### 低光人体姿态估计的核心挑战

人体姿态估计是高层视觉理解的基础任务，在自动驾驶、夜间监控、运动分析等场景中具有关键应用价值。然而，当光照严重不足时，视觉信息急剧退化——图像信噪比骤降、纹理细节淹没、关键点轮廓模糊——导致现有姿态估计器的性能出现断崖式下跌。这一退化并非简单的亮度降低，而是伴随复杂的高频噪声模式（如传感器读出噪声、光子散粒噪声），这些噪声与信号在频域高度混叠，难以通过常规去噪或增强手段分离。

问题的本质在于：**低光条件下，姿态估计模型面临“视觉线索不可靠”与“姿态先验不充分”的双重困境**。一方面，基于图像特征的查询向量（image cues）在低能见度区域携带大量噪声，若被解码器过度信任，会直接破坏关键点定位；另一方面，纯姿态先验（pose priors）虽不受光照影响，但缺乏对当前实例的适应性，在复杂姿态或严重遮挡下同样力不从心。

### 现有范式的结构性缺陷

当前应对低光姿态估计的策略可归纳为三条技术路线，但各自存在根本性瓶颈：

**（1）图像增强预处理（如QuadPrior、DarkIR、LightenDiff）。** 这类方法将低光图像作为独立预处理阶段进行增强，再送入姿态估计器。其核心问题是：增强目标（人眼视觉质量）与下游任务目标（关键点定位精度）之间存在错位。增强过程可能引入过曝、伪影或过度平滑，反而抹去了对姿态估计有用的高频边缘信息。更关键的是，增强模型通常在高斯白噪声假设下设计，无法准确再现真实低光传感器的非高斯、空间相关噪声特性。

**（2）域自适应图像翻译（如CycleGAN、UNIT、EnCo、StyleID）。** 这类方法通过学习从良好光照域到低光域的映射来合成训练数据，无需配对监督。然而，通用翻译模型倾向于生成“平均化”的低光外观，丢失了真实低光图像中特有的高频噪声纹理和局部退化模式（见图2）。这种“过于干净”的合成数据使姿态估计器在训练时从未见过真实低光的极端退化，导致测试时泛化失败——在ExLPose-test的极端低光子集（LL-E）上，最强基线ELLA仅取得3.4 AP。

**（3）ELLA的教师-学生蒸馏框架。** ELLA通过多教师蒸馏将良好光照模型的知识迁移到低光学生模型，在常规低光场景取得进展。但其数据增强部分仍依赖手工设计的退化模拟，无法精确复现真实低光的高频特性；且其解码器采用刚性残差求和（$Q = Q_{image} + Q_{pose}$），在关键点完全不可见时，噪声主导的图像线索仍被等权融合，限制了极端低光下的性能上限。

### 瓶颈诊断与本文动机

上述方法的共同盲点可归结为两个层面：

- **数据层面：合成低光图像的“真实性鸿沟”。** 现有方法无法同时满足两个要求——（a）保留良好光照图像的结构与姿态标注，（b）注入真实低光参考图像的高频噪声特性。手工增强缺乏真实噪声模式，通用翻译模型则丢失结构保真度或噪声细节。
- **模型层面：解码器中信息融合的“刚性假设”。** 单阶段姿态估计器（如ED-Pose）在Transformer解码器中通过交叉注意力融合图像特征与可学习查询，但标准实现将两者简单相加，隐含假设所有关键点的图像线索同等可靠。在低光条件下，这一假设完全失效——脚踝、手腕等远端关键点往往完全淹没在噪声中，而躯干关键点仍保留部分视觉线索。

本文的核心洞察是：**解决低光姿态估计需要同时在数据合成管线中实现“内容感知的高频噪声注入”，并在姿态解码器中引入“逐关键点的自适应信息源选择”**。前者确保训练数据覆盖真实低光的退化分布，后者使模型学会在视觉线索不可靠时自动退回到姿态先验，从而在极端低光下保持解剖学一致性。

## 核心创新

UDAPose 的核心创新并非单一算法，而是一套**协同设计的域自适应管线**，针对低光人体姿态估计中两个相互纠缠的瓶颈——**数据域鸿沟**与**模型融合缺陷**——分别提出了对应的因果性解决方案。

### 瓶颈一：现有域自适应方法无法再现真实低光的高频噪声特性

现有方法（如图像增强和通用非配对图像翻译）合成的低光图像往往丢失真实低光场景中的高频噪声和局部退化模式（见 Figure 2）。CycleGAN、StyleID 等方法倾向于生成“平滑”的低光外观，导致训练出的姿态估计器对真实低光图像中的不可靠视觉线索缺乏鲁棒性。

**创新点：基于 DHF + LCIM 的内容感知低光特性注入**

UDAPose 提出了一套两阶段的低光训练数据合成机制，从根本上改变了数据增强的方式（changed slot: 低光训练数据合成机制）：

1. **DHF (Direct-Current-based High-Pass Filter)**：从非配对低光参考图像中提取高频细节。该模块通过频域高通滤波得到 $I_{HP}$（Eq.1），再通过重定中心操作 $I_{DHF} = I_{HP} + (\mathrm{mean}(I_{LL}) - \mathrm{mean}(I_{HP}))$（Eq.2）将高频细节的亮度分布对齐到原始参考图像的均值，避免后续裁剪造成信息丢失。这一设计的关键在于**保留全动态范围的高频信息**，而非直接使用高通滤波结果。

2. **LCIM (Low-Light Characteristics Injection Module)**：将 DHF 提取的高频特征多尺度地注入到 Stable Diffusion 的 VAE 解码器中。具体而言，LCIM 对 DHF 产生的多尺度中间特征 $\{z_1, z_2, z_3, z_4\}$ 进行轻量卷积处理，在高斯解码的各卷积块之后逐级注入（Eq.3-4），实现从粗到精的低光特性转移。训练 LCIM 的复合损失函数（Eq.5-7）同时约束空间域和频率域，其中频率域损失采用正弦加权 $\mathcal{W}(u,v) = \sin(\frac{\pi |2u-M|}{2M}) + \sin(\frac{\pi |2v-N|}{2N})$ 强调中高频成分的保真度。

**因果机制**：DHF 解决了“高频信息丢失”问题，LCIM 解决了“如何将高频特性精细注入而不破坏原图结构”的问题。两者协同使得合成图像既保留了良好光照图像的结构与低频外观（由预训练 SD 保证），又逼真再现了参考低光图像的噪声特性。消融实验证实了这一因果链：单独加入 LCIM 将 LL-H 的 AP 从 7.2 提升至 20.7；加入 DHF 后进一步提升至 25.3（Table 5）。

### 瓶颈二：单阶段姿态估计器的刚性融合机制使模型过度依赖不可靠图像线索

单阶段姿态估计器（如 ED-Pose）在 Transformer 解码器中采用**刚性残差求和**（$Q_{image} + Q_{pose}$）来融合图像线索与姿态先验。在低光条件下，当关键点视觉特征不可靠时，这种固定权重的融合方式使图像线索仍占据主导地位，导致姿态预测出现解剖学不一致（如关节错位、肢体断裂）。

**创新点：DCA 逐关键点竞争性注意力融合**

UDAPose 提出 **DCA (Dynamic Control of Attention)** 模块（changed slot: 解码器中图像线索与姿态先验的融合方式），替代原有的刚性加和。DCA 的核心操作如下：

1. 在通道维度拼接姿态先验查询 $Q_{pose}$ 和图像线索查询 $Q_{image}$：$Q_{cat} = \mathrm{Concat}(Q_{pose}, Q_{image})$（Eq.8）
2. 通过两层 MLP 和 Softmax 为**每个关键点**生成两个竞争的标量权重：$(w_{pose}, w_{image}) = \mathrm{softmax}(\mathrm{MLP}(Q_{cat}))$（Eq.9）
3. 加权融合：$Q = w_{pose} \odot Q_{pose} \oplus w_{image} \odot Q_{image}$（Eq.10）

**因果机制**：DCA 使模型能够根据当前视觉质量**自适应地调整每个关键点的信息来源**。当某个关键点的图像线索不可靠（如被遮挡或处于极暗区域）时，DCA 自动降低 $w_{image}$、提高 $w_{pose}$，使模型更多地依赖从良好光照数据中学习到的姿态先验来保持解剖学一致性。Figure 4 的量化分析证实了这一机制：在低能见度关键点上，$Q_{image}$ 与 $Q_{pose}$ 的 Frobenius 范数比显著降低，表明 DCA 有效抑制了不可靠的图像线索。消融实验显示，DCA 在 LCIM+DHF 基础上进一步带来 LL-H +2.7 AP、LL-E +2.3 AP 的提升（Table 5），且在关键点大量可见时增益尤为显著。

### 辅助创新：AIN 自适应强度归一化

作为数据合成管线的预处理步骤，UDAPose 还引入了 **AIN (Adaptive Intensity Normalization)**（changed slot: 输入图像强度归一化）。该模块通过 $I_{LL}' = I_{LL} \times \frac{\delta}{\mu_{I_{LL}}}$（Eq.15，其中 $\delta=0.449$ 为 ImageNet 均值）实现内容自适应亮度缩放，保持通道比并避免过曝/欠曝。消融实验（Table 10）表明，AIN 优于直接输入、固定因子缩放和 z-score 标准化，在 LL-H 上达到 23.2 AP（DEKR 骨干）。

### 方法谱系与知识库定位

UDAPose 位于**低光人体姿态估计 × 无监督域自适应 × 扩散模型条件生成**的交叉点：

- **相对于图像增强方法**（如 **RFormer**、**DarkIR**、**QuadPrior**）：UDAPose 不直接增强测试图像，而是通过合成逼真的低光训练数据来提升姿态估计器的鲁棒性，避免了增强过程引入的伪影对下游任务的影响。
- **相对于通用域自适应方法**（如 **CycleGAN**、**UNIT**、**EnCo**）：UDAPose 利用扩散模型的生成先验和任务特定的高频注入机制，生成的低光图像更忠实地保留了真实低光的噪声特性，而非简单的风格迁移。
- **相对于低光姿态估计 SOTA**（**ELLA**）：UDAPose 在不使用蒸馏教师-学生框架的情况下，通过 DCA 模块实现了更精细的图像线索与姿态先验平衡。与 ELLA 完整框架的全面对比（Table 9）进一步验证了 UDAPose 的优越性。
- **相对于扩散条件生成方法**（如 **ControlNet**、**IP-Adapter**）：UDAPose 的 LCIM 是任务特定的轻量注入模块，在无需配对训练数据的情况下优于需要配对监督的通用条件机制（Table 13）。

### 局限性

1. **退化类型泛化受限**：当前框架（DHF + LCIM + DCA）专门针对光照不足引起的退化设计，难以直接泛化至其他低能见度场景（如浓雾、暴雨、严重运动模糊），需要设计新的模块合成相应退化。
2. **计算开销大**：依赖大规模扩散模型（SD-2.1-base）导致合成管线 GPU 内存消耗高、生成时间长，限制了对新环境的快速适配。未来可探索一致性模型或蒸馏扩散模型以降低资源消耗。

## 整体框架

UDAPose 采用“数据合成—姿态估计”两阶段解耦框架，核心思路是：**在数据侧**，利用未配对的真实低光参考图像，通过稳定扩散（Stable Diffusion）模型将良好光照图像合成为高度逼真的低光训练样本，从而继承良好光照图像的精确姿态标注；**在模型侧**，通过在姿态估计器的 Transformer 解码器中引入动态控制注意力（DCA）机制，使模型能够自适应地平衡不可靠的图像线索与学习到的姿态先验。整体流程如 Figure 3 所示。

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the UDAPose framework. During augmentation, the LCIM uses extracted low-light features from unpaired low-light images*

### 数据合成管线

数据合成管线由三个关键组件构成：

1. **DHF（Direct-Current-based High-Pass Filter，直流偏置高频滤波器）**  
   从真实低光参考图像 $I_{LL}$ 中提取高频细节。首先通过频域高通滤波获得 $I_{HP}$（Eq.1），再将其重定中心至参考图像的均值亮度，得到 $I_{DHF}$（Eq.2）。这一“重定中心”操作是 DHF 区别于普通高通滤波的核心——它保留了高频信息的完整动态范围，避免了后续 VAE 编码过程中的信息裁剪。

2. **LCIM（Low-Light Characteristics Injection Module，低光特性注入模块）**  
   对 $I_{DHF}$ 经 VAE 编码器产生的多尺度中间特征 $\{z_1, z_2, z_3, z_4\}$ 进行轻量卷积处理，生成低光特征 $\{f_1, f_2, f_3, f_4\}$（Eq.3），并在稳定扩散解码器的各卷积块末尾逐级注入，实现从粗到精的低光特性转移（Eq.4）。LCIM 采用复合损失函数训练，由像素级 MSE 和频率域加权损失组成（Eq.5-7），其中正弦加权函数 $\mathcal{W}(u,v)$ 为中高频分量分配更高权重，引导模型精确再现低光噪声的频谱特性。

3. **AIN（Adaptive Intensity Normalization，自适应强度归一化）**  
   在数据输入稳定扩散之前，将低光图像按照其均值与目标均值 $\delta$（ImageNet 均值 0.449）的比值进行内容感知缩放（Eq.15），保持通道间比例关系，避免固定因子缩放导致的过曝或欠曝。

合成过程可概括为：良好光照图像 $I_{WL}$ 经稳定扩散的 VAE 编码后，在解码阶段被注入来自未配对低光参考图像的 LCIM 多尺度特征，最终生成合成低光图像 $\hat{I}_{LL}$。该合成图像保留了 $I_{WL}$ 的场景结构和姿态标注，同时获得了 $I_{LL}$ 的低光视觉特性。

### 姿态估计管线

姿态估计器基于 **ED-Pose** 的单阶段集合预测框架（Swin-T 骨干网络），使用匈牙利损失进行端到端训练。UDAPose 在此基础上的核心改进是 **DCA（Dynamic Control of Attention，动态控制注意力）** 模块，嵌入于每个 Transformer 解码器层中。

DCA 的工作机制为（Figure 6）：将姿态先验查询 $Q_{pose}$ 与图像线索查询 $Q_{image}$ 在通道维拼接（Eq.8），通过两层 MLP 和 Softmax 为每个关键点生成一对竞争的标量权重 $(w_{pose}, w_{image})$（Eq.9），最终以加权和的方式融合两类查询（Eq.10）：

$$Q = w_{pose} \odot Q_{pose} \oplus w_{image} \odot Q_{image}$$

这一设计取代了 ED-Pose 原有的刚性残差求和（$Q_{image} + Q_{pose}$），使模型能够在低能见度关键点上自动抑制图像线索、强化姿态先验，从而维持预测的解剖学一致性。

### 训练与推理流程

训练阶段，仅使用合成低光图像及其继承的良好光照标注进行姿态估计器训练，无需任何真实低光标注或配对数据。推理阶段，训练好的模型直接应用于真实低光图像，无需额外的增强或翻译步骤。这种“合成训练—真实推理”的域自适应策略，使得 UDAPose 在保持部署简洁性的同时，显著提升了对真实低光退化的鲁棒性。

## 核心模块与公式推导

UDAPose 由两条协同管线构成：**内容感知的低光数据合成管线**（基于 Stable Diffusion 的 DHF + LCIM）和 **动态注意力融合的姿态估计管线**（基于 ED-Pose 的 DCA）。以下逐模块展开其核心公式与设计逻辑。

### 1. DHF：直流偏置高频滤波器

现有方法从低光参考图像提取高频细节时，常因像素值被裁剪至 [0,1] 区间而丢失大量信息。DHF 的核心思路是：**在频域提取高频成分后，将其亮度分布重定中心至原始参考图像的均值水平**，从而保留完整的动态范围。

**步骤一：频域高通滤波**

$$
I_{HP} = \mathrm{iFFT}(\mathrm{FFT}(I_{LL}) \odot M)
$$

其中 $I_{LL}$ 为低光参考图像，$M$ 为高通滤波器掩码，$\odot$ 表示逐元素乘法。该操作在傅里叶域抑制低频分量，仅保留高频细节 $I_{HP}$。

**步骤二：直流重定中心**

$$
I_{DHF} = I_{HP} + (\mathrm{mean}(I_{LL}) - \mathrm{mean}(I_{HP}))
$$

将 $I_{HP}$ 的均值平移至与 $I_{LL}$ 的均值对齐。这一“加直流”操作使高频细节的整体亮度与原始低光图像保持一致，避免后续 VAE 编码时因数值范围不匹配造成的信息截断。消融实验表明，DHF 在 LCIM 基础上为 LL-H 子集带来 **+4.6 AP** 的增益（Table 5），证实了保留全动态范围高频信息的关键作用。

### 2. LCIM：低光特性注入模块

LCIM 的任务是将 DHF 提取的高频低光特征 $I_{DHF}$，以**多尺度、从粗到精**的方式注入 Stable Diffusion 的 VAE 解码器中，使生成图像在保留良好光照结构的同时，获得逼真的低光噪声特性。

**多尺度特征提取**

VAE 编码器将 $I_{DHF}$ 映射为四个不同分辨率的中间特征 $\{z_1, z_2, z_3, z_4\}$（从低层结构到高层语义）。LCIM 对每一级特征使用轻量卷积层进行处理：

$$
\{ f_1, f_2, f_3, f_4 \} = \mathrm{LCIM}(\{ z_1, z_2, z_3, z_4 \})
$$

**逐级解码注入**

处理后的多尺度特征在 VAE 解码器的对应层级末尾注入：

$$
\hat{I}_{LL}' = d_{final}( d_4( d_3( d_2( d_1(z_0) + f_1 ) + f_2 ) + f_3 ) + f_4 )
$$

其中 $z_0$ 为良好光照图像经 VAE 编码后的潜在表示，$d_1$ 至 $d_4$ 为解码器的四个卷积块，$d_{final}$ 为最终输出层。这种**粗到精的融合策略**使低频结构由 $z_0$ 主导，而高频噪声和局部退化由 $f_1$ 至 $f_4$ 逐步叠加。消融实验证实，融合全部四级特征比仅使用 $z_0$ 的基线在 A7M3 传感器子集上 **AP 提升 15.0**（Table 11）。

**复合训练损失**

LCIM 通过重建损失进行训练，损失函数由空间域 MSE 和频率域加权 MSE 组成：

$$
\mathcal{L}_{\mathcal{D}} = \mathcal{L}_{\mathrm{MSE}}(I, \hat{I}) + \lambda \mathcal{L}_{\mathrm{freq}}(I, \hat{I})
$$

其中频率域损失显式约束傅里叶幅度谱的保真度：

$$
\mathcal{L}_{\mathrm{freq}} = \frac{1}{MN} \sum_{u=0}^{M-1} \sum_{v=0}^{N-1} \mathcal{W}(u,v) |\mathcal{F}_I(u,v) - \mathcal{F}_{\hat{I}}(u,v)|^2
$$

权重函数 $\mathcal{W}(u,v)$ 采用正弦加权，为中高频分量分配更高的惩罚：

$$
\mathcal{W}(u,v) = \sin\left(\frac{\pi |2u-M|}{2M}\right) + \sin\left(\frac{\pi |2v-N|}{2N}\right)
$$

这一设计使 LCIM 在学习低光特性时，优先匹配噪声纹理和边缘退化等中高频信息，同时避免对低频结构的过度约束。超参数 $\lambda$ 的敏感性分析见 Figure 7(a)。

### 3. DCA：动态控制注意力

单阶段姿态估计器 ED-Pose 的解码器原本采用**刚性残差求和**融合图像线索 $\mathbf{Q}_{image}$ 与姿态先验 $\mathbf{Q}_{pose}$。在低光条件下，不可靠的图像线索会主导融合结果，导致姿态预测崩溃。DCA 将这一刚性融合替换为**逐关键点的竞争性软加权**。

**拼接与权重生成**

首先在通道维度拼接两类查询向量：

$$
\mathbf{Q}_{cat} = \mathrm{Concat}(\mathbf{Q}_{pose}, \mathbf{Q}_{image})
$$

随后通过两层 MLP 和 Softmax 为每个关键点生成两个竞争的标量权重：

$$
(w_{pose}, w_{image}) = \mathrm{softmax}(\mathrm{MLP}(\mathbf{Q}_{cat}))
$$

**加权融合**

最终融合查询由哈达玛积加权求和得到：

$$
\mathbf{Q} = w_{pose} \odot \mathbf{Q}_{pose} \oplus w_{image} \odot \mathbf{Q}_{image}
$$

其中 $\odot$ 表示逐元素乘法，$\oplus$ 表示逐元素加法。

**机制分析**

Figure 4 量化了 DCA 生效前后的 Frobenius 范数比 $\|\mathbf{Q}_{image}\|_2 / \|\mathbf{Q}_{pose}\|_2$：对于低能见度关键点（如被遮挡的腕部、踝部），DCA 显著降低图像线索的权重，使模型转而依赖从良好光照数据中学到的解剖学姿态先验。消融实验表明，DCA 在 LL-N、LL-H、LL-E 子集上分别带来 **+3.4、+2.7、+2.3 AP** 的提升（Table 5），且其逐关键点竞争机制优于通用注意力模块 SE-Block 和 CBAM（EHPT-XC 上分别高出 4.3 和 4.0 AP，Table 12）。

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/004_Figure_4.jpg]]
*Figure 4: Ratio of Frobenius Norm of*

### 4. AIN：自适应强度归一化

为稳定 Stable Diffusion 对低光输入的处理，UDAPose 引入自适应强度归一化：

$$
I_{LL}' = I_{LL} \times \frac{\delta}{\mu_{I_{LL}}}
$$

其中 $\mu_{I_{LL}}$ 为输入图像的通道均值，$\delta = 0.449$ 为 ImageNet 数据集的平均亮度。该操作根据图像自身亮度进行**内容感知缩放**，在保持通道比例的前提下将整体亮度对齐至预训练模型的期望分布，避免固定因子缩放导致的过曝或欠曝。Table 10 的消融证实，AIN 在 LL-H 子集上优于直接输入、固定缩放和 z-score 标准化。

### 补充图表

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/012_Figure_6.jpg]]
*Figure 6: The architecture of our DCA module*

## 实验与分析

### 主实验结果

UDAPose在多个基准上一致优于现有图像增强和域自适应方法。所有方法均采用ED-Pose作为姿态估计骨干，仅使用增强/合成图像及对应的良好光照标注进行训练，不使用低光真实标注或配对数据。

**ExLPose-test 数据集。** 如 Table 1 所示，UDAPose在LL-A（全低光子集）上达到27.0 AP，比CycleGAN的19.6 AP提升7.4 AP（相对提升37.8%），比ELLA的17.2 AP提升9.8 AP。在最具挑战性的LL-H（困难子集）上，UDAPose取得28.0 AP，相对CycleGAN（17.9 AP）提升56.4%；在LL-E（极端子集）上达到11.7 AP，而ELLA仅3.4 AP，相对提升高达244%。值得注意的是，UDAPose在良好光照子集上也达到67.3 AP，超过ELLA的61.5 AP，表明合成数据训练未损害正常光照下的性能。Table 2的mAR结果与AP趋势一致，UDAPose在LL-A上取得36.5 AR。

**ExLPose-OCN 真实夜间数据集。** 如 Table 3 所示，UDAPose在真实夜间低光图像上达到51.4 AP和65.1 AR，相比ELLA（46.0 AP）提升5.4 AP（11.7%），验证了方法对真实低光场景的泛化能力。

**EHPT-XC 跨数据集验证。** 为评估方法在不同数据分布下的泛化性，在EHPT-XC上进行跨数据集测试（Table 4）。UDAPose取得31.0 AP，相比ELLA的23.6 AP提升7.4 AP（31.4%），证明合成数据训练的策略具有良好的迁移能力。

**与完整ELLA框架的对比。** 补充材料中提供了与ELLA完整蒸馏框架（含教师-学生模型）的全面对比（Table 9）。UDAPose仍展现出竞争力，且在多数指标上保持优势。

**定性分析。** Figure 5展示了从正常到极端低光条件下的姿态估计可视化对比。在极端低光场景中，图像增强方法（如QuadPrior）和域自适应方法（如CycleGAN）往往产生严重错位或缺失的关键点，而UDAPose能够输出完整且解剖学上连贯的姿态。Figure 9进一步展示了更多定性对比，UDAPose在极端低光下依然保持姿态的结构完整性。

### 消融实验

**核心模块消融。** Table 5系统消融了LCIM、DHF和DCA三个核心组件。基线（仅用良好光照图像训练）在LL-H上仅7.2 AP，LL-E为0 AP。单独加入LCIM后，LL-H提升至20.7 AP（+13.5），LL-E提升至7.8 AP，证实低光特性注入是性能提升的关键驱动力。进一步加入DHF后，LL-H再提升至25.3 AP（+4.6），LL-E提升至9.4 AP（+1.6），表明保留全动态范围的高频细节对合成逼真低光样本至关重要。最终加入DCA后，LL-H达到28.0 AP（+2.7），LL-E达到11.7 AP（+2.3），LL-N也提升3.4 AP，验证了动态融合图像线索与姿态先验的有效性。在跨数据集EHPT-XC上，完整UDAPose（31.0 AP）相比仅用LCIM的配置（24.0 AP）提升7.0 AP。

**AIN自适应归一化。** Table 10对比了不同输入归一化策略（使用DEKR骨干）。直接输入低光图像仅取得7.6 AP，固定因子缩放为20.4 AP，z-score标准化为21.3 AP，而AIN达到23.2 AP。AIN通过自适应缩放保持通道比，避免了过曝/欠曝问题。

**LCIM多尺度融合策略。** Table 11消融了LCIM中多尺度中间特征融合的影响。仅使用z0（标准SD解码）在A7M3子集上AP较低；逐步融合z1至z4的多尺度特征（从粗到精策略）持续提升性能，融合全部四级特征相比仅用z0在A7M3上AP提升15.0，在RICOH3上提升11.1，证实了多尺度粗到精注入的必要性。

**DCA融合机制对比。** Table 12将DCA与通用注意力机制SE-Block和CBAM进行对比。DCA在EHPT-XC上达到31.0 AP，分别高出SE-Block（26.7 AP）4.3 AP和CBAM（27.0 AP）4.0 AP，验证了逐关键点竞争性软加权的独特优势。Figure 4量化分析了DCA的工作机制：在低能见度关键点（如被阴影遮挡的腕部、踝部）上，图像线索与姿态先验的Frobenius范数比显著降低，DCA有效抑制了不可靠的图像线索。Figure 8的定性消融进一步展示了DCA调整前后各关键点权重和姿态预测的变化。

**合成数据量影响。** Table 7展示了合成训练数据量从4k增至20k过程中的性能变化。LL-E的AP从5.4持续提升至11.7，EHPT-XC从25.4提升至31.0，但超过20k后收益趋于饱和。

**解剖学一致性评估。** Table 8使用PSNR、SSIM、LPIPS、FID和KL散度评估合成图像质量。UDAPose在所有指标上均优于CycleGAN、UNIT等学习型基线，生成的图像在解剖结构和姿态一致性上更接近真实低光图像（Figure 10提供定性对比）。

### 失败模式与局限性

尽管UDAPose在低光人体姿态估计上取得了显著提升，仍存在以下局限：

1. **极端退化场景的泛化受限。** 当前框架（LCIM、DHF、DCA）专门针对光照不足引起的退化设计。在浓雾、暴雨、严重运动模糊等其他低能见度场景中，高频噪声特性与低光存在本质差异，现有模块难以直接迁移。需要设计新的退化特性提取与注入模块。

2. **DCA在关键点大量缺失时增益减小。** 当可见关节极少时（如极端遮挡），姿态先验本身也受限，DCA的软加权机制带来的收益递减。Figure 7(b)的掩码鲁棒性实验显示，随掩码比例增加，DCA的优势逐渐缩小。

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/020_Figure_7.jpg]]
*Figure 7: (a) Effect of λ. (b) Masking evaluation w/ and w/o DCA*

3. **扩散模型的计算开销。** 依赖大规模Stable Diffusion模型导致合成管线GPU内存消耗高、生成时间长，限制了对新环境的快速适配。未来可探索一致性模型或蒸馏扩散模型以降低资源需求。

### 关键图表结论速览

- **Table 1/Table 2：** UDAPose在ExLPose-test所有子集上均取得最优AP和AR，LL-H上相对CycleGAN提升56.4%，LL-E上相对ELLA提升244%。
- **Table 3：** 在真实夜间数据集ExLPose-OCN上，UDAPose以51.4 AP领先ELLA 5.4 AP。
- **Table 4：** 跨数据集EHPT-XC验证中，UDAPose以31.0 AP领先ELLA 7.4 AP（31.4%）。
- **Table 5：** LCIM是性能提升的核心驱动力，DHF和DCA各自贡献显著增量，三者协同使LL-H从7.2 AP提升至28.0 AP。
- **Table 10：** AIN自适应归一化优于固定缩放和z-score标准化。
- **Table 11：** LCIM的多尺度粗到精融合至关重要，四级全融合相比单尺度基线提升超10 AP。
- **Table 12：** DCA的逐关键点竞争性加权显著优于通用SE-Block和CBAM注意力。

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/005_Table_1.jpg]]
*Table 1: Evaluation mAP on ExLPose-test comparing image enhancement and domain adaptation methods. All methods are trained only on augmented images and well-lit annotations, without using low-light ground truth or paired data. The best is bold. The second best is underlined*

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/009_Table_5.jpg]]
*Table 5: Ablation study of our proposed modules on ExLPose-test, ExLPose-OCN, and EHPT-XC. Well-lit: pose model trained with well-lit images only. HM: pose model adapted with synthetic lowlight images using histogram matching. AIN is a normalization step (see supplementary). The best is bold*

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/008_Table_4.jpg]]
*Table 4: Cross-dataset validation on EHPT-XC [8], using the model weights as in Tab. 1. Best is bold, second best underlined*

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/007_Table_3.jpg]]
*Table 3: Evaluation on ExLPose-OCN, following identical setup as in Tab. 1. The best is bold. The second best is underlined*

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/016_Table_10.jpg]]
*Table 10: Evaluation of the AIN module on ExLPose-test and ExLPose-OCN. Direct input refers to feeding low-light images into SD without AIN. Experiments are conducted using the DEKR pose model [14], with DHF and LCIM enabled for all normalization approaches. The best is bold*

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/017_Table_11.jpg]]
*Table 11: Ablation study of LCIM on ExLPose-test, ExLPose-OCN, and EHPT-XC. z0 refers to baseline SD without any extra intermediate features. z1 to z4 represent low-to-high-frequency information fused in a coarse-to-fine integration strategy. Results are reported with AIN, DHF and DCA. The best is bold*

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/006_Table_2.jpg]]
*Table 2: Evaluation mAR on ExLPose-test comparing image enhancement and domain adaptation methods, following Tab. 1. The best is bold. The second best is underlined*

### 补充图表

![[assets/figures/papers/paper_list_l1037_https_arxiv_org_abs_2604_10485/figures/002_Figure_2.jpg]]
*Figure 2: Limitations of learning-based low-light augmentation. The first two columns show well-lit and paired low-light images from ExLPose [30]. The third and fourth columns present results from CycleGAN [80] and StyleID [9]. The last column shows our result. Low-light images are scaled to an average channel intensity of 0.4 for visualization only*

## 方法谱系与知识库定位

### 问题定位：低光人体姿态估计的瓶颈

低光条件下的人体姿态估计面临双重挑战：**视觉信息的严重退化**与**现有域自适应方法的系统性缺陷**。一方面，低光图像中的关键点往往模糊甚至不可见，导致基于视觉线索的预测高度不可靠；另一方面，现有的数据增强与域自适应策略无法准确再现真实低光场景中的高频噪声特性，使得在良好光照下训练的姿态估计器在低光测试时性能骤降。

本文识别出该问题的核心瓶颈在于两个层面：

1. **数据合成层面**：现有学习型低光增强方法（如 **CycleGAN**、**StyleID**）生成的合成低光图像倾向于产生过度平滑的伪影，丢失真实低光场景中特有的高频噪声模式（见 Figure 2）。手工增强方法（如直方图匹配、高斯白噪声注入）则无法捕捉低光退化的复杂分布。通用扩散模型条件生成方法（如 **ControlNet**、**IP-Adapter**）虽能生成高质量图像，但需要配对训练数据，且缺乏对低光特性的任务特定建模。

2. **模型架构层面**：主流单阶段姿态估计器（如 **ED-Pose**）在解码器中采用刚性残差求和机制（$Q = Q_{image} + Q_{pose}$），使图像线索在低能见度下仍占主导地位。当关键点不可见时，模型被迫依赖不可靠的视觉信息，导致姿态预测出现解剖学不一致（如肢体交叉、关节错位）。

### 方法谱系中的位置

UDAPose 在低光人体姿态估计的方法谱系中占据独特位置，其设计融合了**内容感知的数据合成**与**自适应信息融合**两条技术路线。

**相对于图像增强方法**（如 **RFormer**、**DarkIR**、**LightenDiff**、**QuadPrior**）：这些方法将低光图像预处理为增强图像后再输入姿态估计器，本质上是“先增强、后估计”的两阶段流水线。其局限在于增强过程可能引入额外伪影，且增强目标（人类视觉质量）与姿态估计目标（关键点定位精度）并不完全一致。UDAPose 绕过了对测试图像的增强需求，转而通过合成训练数据使姿态估计器直接学习低光域的特征表示。

**相对于非配对图像翻译方法**（如 **CycleGAN**、**UNIT**、**UNSB**、**EnCo**）：这些方法在良好光照图像与低光图像之间学习全局风格映射，但缺乏对高频细节的内容感知保留能力。如 Figure 2 所示，CycleGAN 生成的合成低光图像丢失了真实低光场景中的噪声纹理。UDAPose 的 DHF + LCIM 机制通过频域高通滤波与多尺度特征注入，实现了对低光高频特性的精细保留。

**相对于低光姿态估计专用方法**（如 **ELLA**、**UDA-HE**）：ELLA 采用教师-学生蒸馏框架，通过多个教师模型协同增强低光图像，但其数据增强部分仍依赖于手工设计的增强策略。UDAPose 与 ELLA 的主要对比中（Table 1），在仅使用数据增强部分（不含蒸馏）的公平设定下，UDAPose 在 LL-H 子集上以 28.0 AP 显著优于 ELLA 的 17.2 AP；在包含完整蒸馏框架的全面对比中（Table 9），UDAPose 仍保持优势。这表明基于扩散模型的内容感知合成比手工增强策略更有效。

**相对于扩散模型条件生成方法**（如 **ControlNet**、**IP-Adapter**）：这些通用条件机制需要配对训练数据来实现特定退化类型的生成。UDAPose 在仅使用非配对低光参考图像的条件下，通过任务特定的 LCIM 模块实现了更优的低光特性注入（Table 13），证明任务特定模块优于通用条件机制。

### 核心方法论贡献

UDAPose 的方法论贡献可归纳为三个相互协同的组件，各自解决了低光姿态估计中的一个关键子问题：

1. **DHF（直流高频滤波器）**：解决了从低光参考图像中提取高频细节时信息丢失的问题。传统高通滤波后的特征均值趋近于零，在后续归一化或裁剪中容易丢失动态范围。DHF 通过重定中心（$I_{DHF} = I_{HP} + (\mathrm{mean}(I_{LL}) - \mathrm{mean}(I_{HP}))$）将高频细节对齐至参考图像的均值亮度，保留了完整的动态范围信息。

2. **LCIM（低光特性注入模块）**：解决了如何在保留良好光照图像结构的同时逼真注入低光特性的问题。LCIM 在稳定扩散 VAE 解码器的四个尺度层级上逐级注入经过轻量卷积处理的 DHF 特征，实现从粗到精的低光特性转移。其训练采用复合损失函数 $\mathcal{L}_{\mathcal{D}} = \mathcal{L}_{\mathrm{MSE}}(I, \hat{I}) + \lambda \mathcal{L}_{\mathrm{freq}}(I, \hat{I})$，其中的频率域损失 $\mathcal{L}_{\mathrm{freq}}$ 通过正弦加权 $\mathcal{W}(u,v) = \sin(\frac{\pi |2u-M|}{2M}) + \sin(\frac{\pi |2v-N|}{2N})$ 强调中高频成分的保真度，避免过度锐化。

3. **DCA（动态控制注意力）**：解决了低能见度下图像线索与姿态先验的权重分配问题。DCA 通过 MLP + Softmax 为每个关键点生成一对竞争的标量权重 $(w_{pose}, w_{image})$，以加权求和替代刚性加和：$Q = w_{pose} \odot Q_{pose} \oplus w_{image} \odot Q_{image}$。Figure 4 的量化分析表明，DCA 能够自动降低低能见度关键点（如被遮挡的手腕、脚踝）的图像线索权重，使模型更依赖学习到的姿态先验，从而修正解剖学不一致的预测。

### 适用边界与局限

尽管 UDAPose 在低光人体姿态估计上取得了显著提升，其适用边界存在明确限制：

1. **退化类型的专一性**：当前框架（包括 LCIM、DHF、DCA）专门针对光照不足引起的视觉退化设计。DHF 提取的高频特性主要反映低光噪声模式，LCIM 的注入机制也针对此类退化优化。对于其他低能见度场景——如浓雾引起的对比度丧失、暴雨造成的水滴遮挡、严重运动模糊导致的纹理涂抹——该方法难以直接泛化。需要设计新的退化特性提取与注入模块才能覆盖这些场景。

2. **计算资源需求**：依赖大规模扩散模型（Stable Diffusion 2.1-base）作为生成骨干，导致合成管线计算开销较大。单张图像的合成需要完整的扩散解码过程，GPU 内存占用高、生成时间长，限制了对新环境的快速适配。论文指出未来可探索一致性模型或蒸馏扩散模型以降低资源消耗。

3. **极端遮挡下的先验局限**：DCA 模块在关键点大量缺失时增益减小。当可见关节极少时，姿态先验本身也面临高度不确定性，竞争性加权机制的作用空间受限。Table 5 的消融显示，DCA 在 LL-E（极端低光）子集上的增益（+2.3 AP）小于 LL-N（正常低光，+3.4 AP）和 LL-H（困难低光，+2.7 AP），部分反映了这一局限。

4. **训练数据量的饱和效应**：Table 7 显示，合成数据量从 4k 增加到 20k 过程中，LL-E AP 从 5.4 提升至 11.7，EHPT-XC AP 从 25.4 提升至 31.0，但超过 20k 后收益趋于饱和。这表明 LCIM 合成的低光图像在多样性上存在上限。

### 开放问题

论文揭示了若干值得进一步探索的方向：

1. **退化类型的泛化**：能否将基于高频特性注入的生成范式扩展至其他复杂退化类型（雾、雨、运动模糊），并验证其对姿态估计的跨退化提升？这可能需要设计通用的退化特性提取器，或构建多退化联合注入框架。

2. **高效生成模型的应用**：能否利用更高效的条件生成模型（如蒸馏扩散模型、一致性模型）在保持合成质量的同时显著缩短训练数据生成时间？这对于实际部署中的快速域自适应至关重要。

3. **极端遮挡的鲁棒性**：DCA 在关键点大量缺失时增益减小，如何进一步改进以应对极端遮挡场景？可能的路径包括引入更强的解剖学先验（如骨骼长度约束、关节角度限制）或多帧时序信息。

4. **跨任务泛化验证**：该方法是否能够作为通用域自适应框架应用于其他高层视觉任务（如实例分割、目标检测）？DHF + LCIM 的数据合成范式与 DCA 的自适应融合机制在原理上不限于姿态估计，但需要在下游任务上进行系统验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/UDAPose_Unsupervised_Domain_Adaptation_for_Low_Light_Human_Pose_Estimation.pdf]]