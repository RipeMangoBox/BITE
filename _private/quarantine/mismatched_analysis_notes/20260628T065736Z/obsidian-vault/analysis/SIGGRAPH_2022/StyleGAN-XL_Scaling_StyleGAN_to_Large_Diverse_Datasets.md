---
title: "StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/StyleGAN_XL_Scaling_StyleGAN_to_Large_Diverse_Datasets.pdf
project_link: "https://youtu.be/G06dEcZ-QTg"
code_link: "https://github.com/tkarras/progressive\\_growing\\_of\\_gans"
aliases:
- PGG
- StyleGAN-XL
tags:
- SIGGRAPH_2022
- topic/benchmarks_datasets_evaluation
core_operator: 渐进式增长（Progressive Growing）——从低分辨率开始，随着训练逐步增加层数来建模更精细的细节。
primary_logic: 通过逐步增加分辨率，让网络先学习大尺度结构再逐步细化细节，形成一种隐式课程学习，既稳定了训练又加速了收敛。
claims:
- 通过渐进式增长，生成器和判别器从低分辨率开始，逐步增加层，可大幅提升训练稳定性和图像质量。
- 渐进式增长使模型收敛到更好的最优解，并将总训练时间缩短约一半。
- 隐式课程学习解释了渐进式增长的改进：低分辨率层先收敛，随后网络只需逐步细化细节。
- 结合所有提出的改进（渐进增长、minibatch标准差、均衡学习率、像素级归一化）后，SWD从9.28降至2.96，图像质量显著提升。
---

# StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets

> [!tip] 核心洞察
> 通过逐步增加分辨率，让网络先学习大尺度结构再逐步细化细节，形成一种隐式课程学习，既稳定了训练又加速了收敛。

| 字段 | 内容 |
|------|------|
| 中文题名 | 生成对抗网络的渐进增长：提升质量、稳定性和多样性 |
| 英文题名 | StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://sites.google.com/view/stylegan-xl/) · [Project](https://youtu.be/G06dEcZ-QTg) · [Code](https://github.com/tkarras/progressive\_growing\_of\_gans) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | Progressive Growing of GANs |
| Dataset | CELEBA 128x128, CIFAR-10, LSUN BEDROOM, CELEBA-HQ 1024x1024 |

> [!tip] 效果简介
> - CELEBA 128x128 (非最终收敛) 上，SWD Avg (×10^3) 2.96 vs 9.28 (-6.32 (降低68%))。
> - CIFAR-10 (unsupervised) 上，Inception Score 8.80 vs 7.90 (先前最佳无监督结果) (+0.90)。
> - LSUN BEDROOM (256x256) 上，视觉质量对比 更清晰、更真实的卧室图像 vs Gulrajani et al. (2017) 等先前方法 (显著提升)。

## 概要

高分辨率生成对抗网络（GAN）的训练面临根本性不稳定：分辨率升高使得真假样本更易区分，同时内存限制迫使使用更小的minibatch，导致梯度波动和模式崩塌。本文提出**渐进式增长（Progressive Growing）**方法——生成器与判别器均从4×4低分辨率开始，训练过程中逐步添加新层以建模越来越精细的细节，新层通过平滑淡入（fade-in）过渡以避免冲击已训练层。这一策略构成隐式课程学习：低分辨率层先收敛到大尺度结构，后续层仅需逐步细化，从而显著稳定训练并加速收敛。

辅助技术包括：**minibatch标准差层**（将minibatch统计量作为判别器额外特征图以增强生成多样性）、**像素级特征向量归一化**（防止生成器信号幅度失控）以及**均衡学习率**（运行时缩放权重以替代He初始化中的尺度校正）。

在CELEBA 128×128上，完整方案将Sliced Wasserstein距离（SWD）从基线9.28降至2.96；在CIFAR-10无监督设置下取得Inception Score 8.80的纪录；在CELEBA-HQ上首次实现1024×1024分辨率的高质量人脸生成。该方法定位为训练策略层面的通用改进，可与WGAN-GP或LSGAN等不同损失函数组合使用。

## 核心方法与创新机理

### 问题瓶颈：高分辨率GAN训练的本质困境

GAN在高分辨率图像生成中面临一个根本性矛盾：分辨率越高，真假样本的分布差异越容易被判别器捕捉，导致梯度消失或爆炸；同时，受GPU内存限制，高分辨率训练必须使用更小的minibatch，这进一步加剧了梯度估计的不稳定性，使得模式崩塌（mode collapse）成为常态。这一瓶颈并非简单的超参数调整所能解决，而是高维生成空间与有限训练信号之间的结构性冲突。

### 核心机制：渐进式增长（Progressive Growing）

针对上述瓶颈，本文的核心创新是**渐进式增长策略**——让生成器（Generator）和判别器（Discriminator）从极低分辨率（4×4）开始训练，随着训练推进逐步添加新层，以建模越来越精细的细节。这一策略的本质是将高分辨率生成这一困难问题分解为一系列逐渐增难的子任务，形成一种**隐式课程学习（implicit curriculum learning）**。

渐进式增长的因果链条如下：
1. **低分辨率阶段**：网络仅需学习图像的大尺度结构和全局布局，此时真假样本的分布差异较小，判别器梯度稳定，生成器可快速收敛到合理的流形区域。
2. **分辨率翻倍时**：新层通过**平滑淡入（fade-in）**机制引入，而非直接插入。具体而言，新增的高分辨率分支输出与上采样的低分辨率输出通过一个从0到1线性增长的权重α进行混合：输出 = (1-α) × 上采样旧层输出 + α × 新层输出。这一设计避免了新层初始随机权重对已训练低分辨率层的冲击，确保了训练连续稳定。
3. **高分辨率阶段**：网络在已有的大尺度结构基础上，仅需学习残差式的细节补充，这大大降低了优化难度，加速了收敛。

实验证据表明，仅添加渐进式增长（无其他改进），SWD指标就从9.28降至4.28（Table 1，行(a) vs 行(b)），且训练时间缩短约一半（Figure 4），在1024×1024分辨率下更实现了约5.4倍的加速。

![[assets/figures/papers/paper_list_l7_https_sites_google_com_view_stylegan_xl/figures/005_Figure_4.jpg]]
*Figure 4: Effect of progressive growing on training speed and convergence. The timings were measured on a single-GPU setup using NVIDIA Tesla P100. (a) Statistical similarity with respect to wall clock time for Gulrajani et al. (2017) using CELEBA at 128 × 128 resolution. Each graph represents sliced Wasserstein distance on one level of the Laplacian pyramid, and the vertical line indicates the point where we stop the training in Table 1. (b) Same graph with progressive growing enabled. The dashed vertical lines indicate points where we double the resolution of G and D. (c) Effect of progressive growing on the raw training speed in 1024 × 1024 resolution*

![[assets/figures/papers/paper_list_l7_https_sites_google_com_view_stylegan_xl/figures/003_Table_1.jpg]]
*Table 1: Sliced Wasserstein distance (SWD) between the generated and training images (Section 5) and multi-scale structural similarity (MS-SSIM) among the generated images for several training setups at*

### 关键模块与架构设计

#### 1. 生成器归一化：像素级特征向量归一化（Pixelwise Normalization）

传统GAN生成器普遍使用批量归一化（Batch Normalization），但本文发现BN在高分辨率生成中会引入不希望的耦合效应。替代方案是**像素级特征向量归一化**：在生成器的每个卷积层之后，将每个空间位置(x,y)处的特征向量归一化到单位长度：

$$b_{x,y} = a_{x,y} / \sqrt{ \frac{1}{N} \sum_{j=0}^{N-1} (a_{x,y}^j)^2 + \epsilon }$$

其中N为特征图数量，ε=10⁻⁸防止除零。这一操作防止了信号幅度在深层网络中不受控地爆炸（这是GAN训练中常见的失败模式），同时不引入跨样本的依赖关系，保持了训练的局部稳定性。

#### 2. 均衡学习率（Equalized Learning Rate）

传统初始化方案（如He初始化）试图通过精心设计的权重缩放来保证各层的学习动态一致，但在GAN这种动态博弈中往往失效。本文采用更直接的方案：所有权重用标准正态分布N(0,1)初始化，**在运行时显式缩放权重**：ŵᵢ = wᵢ / c，其中c是He初始化中的逐层归一化常数。这一设计确保所有可学习参数的动态范围和更新速度一致，避免了某些层学习过快或过慢导致的训练失衡。

#### 3. 多样性增强：Minibatch标准差层（Minibatch Standard Deviation Layer）

模式崩塌是GAN的核心顽疾。传统方法通过minibatch discrimination（在判别器中注入样本间相似度特征）来鼓励多样性，但实现复杂且效果有限。本文提出一个极简替代方案：**在判别器中计算minibatch内各特征图在各空间位置的标准差，将其作为额外特征图拼接回去**。具体而言：
- 对minibatch中每个特征图的每个空间位置计算标准差
- 对所有特征图和空间位置取平均，得到一个标量
- 将该标量复制为与空间分辨率相同的单通道特征图
- 拼接到判别器的中间特征层

这一操作以极低的计算代价为判别器提供了“当前minibatch的多样性水平”这一全局统计信息，使生成器有动力覆盖更多模式。消融实验证实，该层比传统minibatch discrimination更有效（Table 1，行(e) vs 行(e*)）。

### 训练管线与模块协同

完整的训练管线按以下顺序运作：

1. **初始化**：生成器和判别器均从4×4分辨率开始，权重用N(0,1)初始化。
2. **前向传播**：
   - 生成器：潜在向量z → 全连接层 → 4×4卷积块（含像素级归一化）→ 逐步上采样至更高分辨率
   - 判别器：输入图像 → 逐步下采样 → minibatch标准差层（在末端某层）→ 真/假判断
3. **损失计算**：使用WGAN-GP损失，梯度罚项为：
   $$\mathbb{E}_{\hat{\mathbf{x}} \sim \mathbb{P}_{\hat{\mathbf{x}}}} [(||\nabla_{\hat{\mathbf{x}}} D(\hat{\mathbf{x}})||_2 - \gamma)^2 / \gamma^2]$$
   其中γ控制Lipschitz约束强度（CIFAR-10实验中γ=750）。
4. **权重更新**：所有层均使用均衡学习率的RMSProp优化器。
5. **渐进调度**：当当前分辨率训练充分后，通过平滑淡入引入新层，分辨率翻倍。

### 创新机理总结

本方法的核心贡献在于**改变了GAN训练的难度分布**：将“一次性学习高分辨率映射”这一极难问题，转化为“先学粗结构、再学细节”的课程序列。渐进式增长是这一转化的操作手段，像素级归一化和均衡学习率是确保每个阶段稳定训练的保障机制，minibatch标准差层则是贯穿始终的多样性守护者。三者协同，使得高分辨率GAN训练从“几乎不可能”变为“可稳定复现”。

## 实验与关键发现

### 核心定量结果

论文通过一系列消融实验和基准测试，系统验证了渐进式增长及配套技术对GAN训练的改进效果。最核心的定量证据来自CELEBA 128×128分辨率下的消融实验（Table 1），以Sliced Wasserstein Distance（SWD，×10³）为主要评估指标。

**完整方案 vs. 基线：** 将渐进式增长、minibatch标准差层、均衡学习率和像素级归一化全部组合后，SWD从基线（WGAN-GP，固定分辨率训练）的9.28降至2.96，降幅约68%。这一改进在视觉质量上表现为图像清晰度和真实感的显著提升（Figure 3 (a) vs. (h)）。值得注意的是，MS-SSIM指标在同一过程中几乎未变化（0.2854 → 0.2828），说明MS-SSIM无法捕捉生成质量的改善，这一发现本身也构成了对常用评估指标的警示。

**CIFAR-10无监督记录：** 在CIFAR-10数据集上，该方法取得了8.80的Inception Score（Table 3），超过此前最佳无监督结果的7.90。论文指出，通过将WGAN-GP梯度罚项中的γ参数从默认值调整为750，Inception Score得以进一步提升，但该技巧的通用性仍属开放问题。

**高分辨率生成：** 在CELEBA-HQ 1024×1024分辨率下，最终模型达到SWD平均5.44、FID 7.30（Figure 11），生成了当时分辨率最高、质量最好的GAN人脸图像。

### 消融实验：各组件的贡献

Table 1的逐行消融清晰揭示了每个改进组件的因果贡献：

1. **渐进式增长（PG）单独作用：** 在WGAN-GP基线上仅添加渐进式增长（从固定分辨率改为4×4逐步增长至128×128），SWD从9.28降至4.28（Table 1 (a) → (b)）。这是单一项改进中幅度最大的提升，直接验证了渐进式增长作为核心因果杠杆的有效性。

2. **小minibatch的破坏性影响：** 将minibatch尺寸从64降至16时，SWD飙升至46.23（Table 1 (c)），生成图像出现明显异常。这从反面证实了高分辨率训练中minibatch尺寸的关键约束——分辨率越高，真假样本越容易区分，小minibatch导致梯度估计方差增大，训练崩溃。

3. **Minibatch标准差层的增益：** 在渐进式增长基础上加入minibatch标准差层后，SWD进一步从4.28改善（Table 1 (b) → (d) → (e)）。论文特别对比了minibatch标准差层与传统的minibatch discrimination方法，前者在SWD和视觉质量上均更优（Section 6.1 (e) vs. (e\*)），且实现更简洁。

4. **均衡学习率与像素归一化的叠加效果：** 在已有渐进式增长和minibatch标准差层的基础上，加入均衡学习率使SWD继续下降（Table 1 (f)），再加入像素级归一化后达到最终的2.96（Table 1 (h)）。这两个组件主要解决训练过程中的信号幅度控制问题——均衡学习率防止不同层之间学习速率失配，像素归一化防止生成器中特征向量幅度的恶性膨胀。

### 训练效率的实证分析

Figure 4提供了渐进式增长对训练动态影响的定量证据：

- **收敛质量提升：** 在相同训练配置下，渐进式增长不仅收敛到更优的SWD值，且收敛曲线更加稳定（Figure 4(a) vs. (b)）。
- **训练时间减半：** 渐进式增长将总训练时间缩短约一半。论文将此归因于隐式课程学习效应——低分辨率层先收敛到大尺度结构，后续高分辨率层只需微调细节，避免了从零开始训练高分辨率网络的低效探索。
- **超高分辨率的加速比：** 在1024×1024分辨率下，渐进式增长达到640万张图像吞吐量所需的时间仅为固定分辨率训练的1/5.4（Figure 4(c)），加速效果随目标分辨率升高而愈加显著。

### 多样性验证：模式覆盖测试

为验证方法对生成多样性的影响，论文在MNIST-1K离散模式测试上进行了评估（Table 4）。该测试使用两个微型判别器（K/4和K/2，架构来自Metz et al., 2016），统计生成样本覆盖的模式数量和KL散度。结果表明，渐进式增长配合minibatch标准差层能有效覆盖更多模式，KL散度更接近均匀分布，验证了minibatch统计信息注入对缓解模式崩塌的正面作用。

![[assets/figures/papers/paper_list_l7_https_sites_google_com_view_stylegan_xl/figures/013_Table_4.jpg]]
*Table 4: Results for MNIST discrete mode test using two tiny discriminators (K/4, K/2) defined by Metz et al. (2016). The number of covered modes (#) and KL divergence from a uniform distribution are given as an average ± standard deviation over 8 random initializations. Higher is better for the number of modes, and lower is better for KL divergence*

### 失败模式与适用边界

论文坦承了若干局限性，这些构成了方法的适用边界：

1. **照片级真实感的差距：** 即使在1024×1024分辨率下，生成图像与真实照片之间仍有明显差距。语义合理性不足——模型可能生成看似合理但违反物理约束的细节（如弯曲的直线物体），说明网络并未真正理解物体的三维结构和语义约束。

2. **微结构质量问题：** 图像的微结构（micro-structure）仍有改进空间，部分区域可能出现不自然的纹理或伪影。

3. **数据集缺陷的忠实复制：** 模型会学习并复制训练数据中的瑕疵。Figure 3的说明明确指出，部分生成图像中的混叠伪影和模糊实际上是CELEBA数据集本身的问题，模型忠实地“学会”了这些缺陷。这提示在使用该方法时，数据集质量对最终生成结果有直接影响。

4. **小分辨率场景的边际收益：** 对于CIFAR-10（32×32）这类极小分辨率图像，渐进式增长的提升不明显。论文指出这并不意外，因为低分辨率图像本身的结构层次有限，渐进式增长的课程学习优势难以体现。但该方法不会对训练造成负面影响，可以安全使用。

5. **超参数敏感性：** WGAN-GP中γ参数从默认值调至750在CIFAR-10上有效，但论文未在其他数据集上验证该技巧的普适性；LSGAN变体需要自适应噪声机制（附录B）来维持训练稳定，表明损失函数选择与训练稳定性之间存在耦合，需要针对具体场景调整。

![[assets/figures/papers/paper_list_l7_https_sites_google_com_view_stylegan_xl/figures/012_Table_3.jpg]]
*Table 3: CIFAR10 inception scores, higher is better*

![[assets/figures/papers/paper_list_l7_https_sites_google_com_view_stylegan_xl/figures/015_Figure_11.jpg]]
*Figure 11: Additional 1024×1024 images generated using the CELEBA-HQ dataset. Sliced Wasserstein Distance (SWD) ×103 for levels 1024, . . . , 16: 7.48, 7.24, 6.08, 3.51, 3.55, 3.02, 7.22, for which the average is 5.44. Frechet Inception Distance (FID) computed from 50K images was 7.30. ´ See the video for latent space interpolations*

## 定位与知识库关联

本文在GAN训练稳定性与高分辨率生成这条线上，做出的核心贡献是**改变了训练分辨率策略这一slot**：将当时主流的一次性固定分辨率训练（如WGAN-GP在128²或更高分辨率上从头训练）替换为从4×4开始、逐步增加层数的渐进式增长方案。这一改变并非简单的工程技巧，而是将GAN训练从“直接求解高维流形的全局最优”转变为“先学习低维骨架、再逐级细化细节”的隐式课程学习过程，从而在根本上缓解了高分辨率下真假分布易分离导致梯度消失/爆炸的瓶颈。

**相对baseline的本质差异**：
- 相对于**WGAN-GP**（Gulrajani et al., 2017），本文不仅引入了渐进式增长，还配套改变了两个辅助slot：生成器归一化（从Batch Normalization替换为像素级特征向量归一化+均衡学习率）和多样性增强机制（从无或minibatch discrimination替换为minibatch标准差层）。消融实验（Table 1）表明，仅渐进式增长一项就将SWD从9.28降至4.28，而三项改进叠加后降至2.96，说明各组件之间存在协同效应——渐进式增长提供了稳定的训练骨架，均衡学习率和像素归一化则防止了新增层带来的信号幅度失控，minibatch标准差层在判别器中注入统计信息以对抗模式崩塌。
- 相对于**LSGAN**（Mao et al., 2016b），本文在Appendix B中展示了LSGAN变体同样可从渐进式增长中获益，但需要自适应噪声机制来防止判别器过强导致的不稳定。这表明渐进式增长并非仅适用于WGAN-GP，而是一种与损失函数选择正交的训练策略改进。

**知识库挂载点**：
1. **课程学习（Curriculum Learning）**：本文的理论解释直接挂载到Bengio et al. (2009)的课程学习框架。渐进式增长本质上是一种网络容量逐渐增加的隐式课程——低分辨率层先收敛到大尺度结构，高分辨率层仅需在已学到的粗粒度表示上添加细节。Figure 4(a)与(b)的对比定量验证了这一机制：渐进式增长不仅收敛到更优的SWD值，还将总训练时间缩短约一半。
2. **GAN训练稳定性**：本文可挂载到WGAN-GP（Gulrajani et al., 2017）的梯度惩罚框架和minibatch discrimination（Salimans et al., 2016）的多样性增强线。minibatch标准差层是对minibatch discrimination的简化改进——不再需要额外的可学习参数，仅将minibatch内各空间位置的特征标准差作为额外特征图拼接，计算开销更小且效果更优（Section 6.1中(e) vs (e*)对比）。
3. **归一化方法**：像素级归一化挂载到Local Response Normalization（Krizhevsky et al., 2012）的变体线，但目的不同——不是为了竞争性归一化，而是显式约束特征向量模长以防止生成器中的信号幅度爆炸。这与均衡学习率形成互补：前者控制前向传播的幅度，后者控制反向传播的梯度尺度。

**适用边界**：
- **分辨率下限**：对于极小分辨率图像（如CIFAR-10的32×32），渐进式增长的提升不明显（但不会有害），因为低分辨率下真假分布的可分性尚未构成主要瓶颈。
- **minibatch尺寸依赖**：渐进式增长虽然缓解了高分辨率下minibatch必须减小的压力，但不能完全消除该依赖。Table 1显示，在128²分辨率下将minibatch从64降至16，SWD从9.28飙升至46.23，说明小batch仍是训练质量的关键限制因素。
- **数据集瑕疵的忠实复制**：模型会学习并复制数据集中的混叠伪影等瑕疵（Figure 3中部分图像不清晰），这是GAN生成式建模的固有问题，渐进式增长并未解决。
- **语义理解缺失**：本文明确指出距离照片级真实感仍有很大差距，模型对语义合理性（如物体应为直线而非曲线）的理解不足，这是GAN框架本身的局限，渐进式增长仅改善了纹理和结构质量。

**后续启发价值**：
1. **StyleGAN系列的基石**：本文的渐进式增长策略直接启发了StyleGAN（Karras et al., CVPR 2019）和StyleGAN2（Karras et al., CVPR 2020）的训练方案。StyleGAN在渐进式增长的基础上进一步将生成器重构为风格调制架构，但训练时仍沿用从低分辨率逐步过渡的策略（StyleGAN2后来改为非渐进式但使用了本文的均衡学习率等技巧）。知识库中可将本文定位为“高分辨率GAN训练的工程基础”，后续工作可沿此线挂载。
2. **训练效率的定量基准**：Figure 4(c)显示渐进式增长在1024²分辨率下提供约5.4×的加速比（达到6.4M图像所需时间），这为后续大规模GAN训练的效率优化提供了可参考的基准数据。
3. **SWD指标的引入**：本文在评估中大量使用Sliced Wasserstein Distance作为主要定量指标，并指出MS-SSIM无法有效区分图像质量改进（Table 1中(a)与(h)的MS-SSIM几乎不变）。这为后续工作选择评估指标提供了经验依据，但SWD与FID等更广泛使用的指标在模式崩塌场景下的一致性仍需验证（论文未给出FID的消融对比，仅在Figure 11中报告了CELEBA-HQ的FID=7.30作为参考值）。
4. **开放问题**：自适应minibatch尺寸与分辨率的依赖关系、WGAN-GP中γ=750对CIFAR-10有效的机制、LSGAN变体的精确配置等问题仍未完全解决，这些为后续研究留下了可探索的空间。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/StyleGAN_XL_Scaling_StyleGAN_to_Large_Diverse_Datasets.pdf]]