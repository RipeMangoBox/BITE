---
title: Efficient Training for Human Video Generation with Entropy-Guided Prioritized Progressive Learning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Efficient_Training_for_Human_Video_Generation_with_Entropy_Guided_Prioritized_Progressive_Learning.pdf
project_link: null
code_link: null
aliases:
- EGPPLEP
- ETHVGEGPPL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过条件熵膨胀（CEI）量化各网络块对条件生成的重要性，据此制定优先级渐进解冻顺序，并利用自适应渐进调度根据收敛效率动态调整每个训练阶段解冻的块数，从而将有限资源集中分配给关键模块。
primary_logic: 并非所有网络模块对条件视频生成的贡献相同；跳过不同块时条件熵的增加量（CEI）可作为有效的重要性度量，优先训练高CEI块能加速收敛并节省资源。
claims:
- Ent-Prog achieves up to 2.2× training speedup and 2.4× GPU memory reduction without compromising generative performance.
- On TikTok dataset, removing CEI training priority causes FID-VID to increase from 32.15 to 37.43.
- Ent-Prog surpasses full training on Bilibili video generation with FVD 120.35 vs 168.17 (28% lower).
- On UBC-Fashion, Ent-Prog achieves 1.69× speedup and retains only 63.0% GPU memory compared to full training.
---

# Efficient Training for Human Video Generation with Entropy-Guided Prioritized Progressive Learning

> [!tip] 核心洞察
> 并非所有网络模块对条件视频生成的贡献相同；跳过不同块时条件熵的增加量（CEI）可作为有效的重要性度量，优先训练高CEI块能加速收敛并节省资源。

| 字段 | 内容 |
|------|------|
| 中文题名 | 熵引导优先级渐进学习的高效人体视频生成训练 |
| 英文题名 | Efficient Training for Human Video Generation with Entropy-Guided Prioritized Progressive Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21136) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Entropy-Guided Prioritized Progressive Learning (Ent-Prog) |
| Dataset | Bilibili, TikTok, UBC-Fashion |

> [!tip] 效果简介
> - Bilibili (video) 上，FVD 120.35 vs 168.17 (-47.82 (28%↓))。
> - Bilibili (image) 上，FID 44.09 vs 45.71 (-1.62 (3.5%↓))。
> - TikTok 上，FVD 264.03 vs 385.64 (-121.61 (46.1%相对提升))。

## 概要

训练高分辨率、多帧人体视频扩散模型面临一个核心瓶颈：现有方法对所有网络参数进行均等更新，忽略了不同模块对条件生成任务的贡献差异，导致计算资源与显存消耗巨大且训练效率低下。针对这一问题，本文提出**熵引导优先级渐进学习（Entropy-Guided Prioritized Progressive Learning，Ent-Prog）**框架，其核心洞察是：并非所有网络模块对条件视频生成的贡献相同；跳过不同块时条件熵的增加量可作为有效的重要性度量，优先训练高重要性块能够加速收敛并节省资源。

Ent-Prog 通过**条件熵膨胀（Conditional Entropy Inflation, CEI）**量化各网络块对条件生成的重要性，据此制定优先级渐进解冻顺序，并利用**自适应渐进调度**根据收敛效率动态调整每个训练阶段解冻的块数，从而将有限资源集中分配给关键模块。

在三个不同的人体视频生成数据集上，Ent-Prog 实现了最高 **2.2 倍训练加速**和 **2.4 倍 GPU 显存节省**，且生成性能不降反升。例如，在 Bilibili 视频生成任务上，Ent-Prog 的 FVD 达到 120.35，相比全参数训练的 168.17 降低了 28%；在 TikTok 数据集上，移除 CEI 优先级后 FID-VID 从 32.15 恶化至 37.43，验证了优先级机制对训练质量的关键作用。

### 问题背景

人体视频生成旨在根据参考图像和姿态序列等条件，合成逼真、可控的人体动作视频。扩散模型已成为该领域的主流范式，但其训练过程对计算资源的需求极为庞大。随着视频分辨率、帧数和条件复杂度的提升，标准训练流程需同时更新扩散网络中所有参数，导致显存占用和训练时间急剧膨胀。这一瓶颈严重制约了高保真人体视频生成模型的研发与迭代效率。

### 现有方法缺口

当前扩散模型的训练策略普遍采用“全参数平等更新”的方式，即从训练起始阶段便解冻所有网络块，并以统一的学习率进行优化。然而，这一做法忽略了两个关键事实：

1. **不同网络块对条件生成任务的贡献存在显著差异**。如图 1 所示，冻结不同数量的网络块会对模型最终收敛性能产生截然不同的影响；更重要的是，训练最具影响力的 10 个块与最不重要的 10 个块时，前者展现出明显更快的收敛速度和更优的模型性能。
2. **条件依附程度在不同模块间分布不均**。当随机跳过 8 至 23 个块时，各块对应的损失和条件熵膨胀（Conditional Entropy Inflation, CEI）呈现高度异质性——跳过某些块仅引起微小的条件熵变化，而跳过另一些块则导致条件熵急剧上升，表明后者对条件生成至关重要。

现有的高效训练方法（如渐进式解冻、子网络训练等）虽尝试减少训练负荷，但普遍缺乏对“哪些块应优先训练”的量化判断依据，也未能根据实际收敛效率动态调整训练计划，导致资源分配仍存在大量浪费。

### 核心动机

本文的核心动机源于一个关键洞察：**并非所有网络模块对条件视频生成的贡献相同**。若能准确量化每个网络块对条件生成任务的重要性，并据此制定差异化的训练优先级，则有望将有限的计算资源集中分配给关键模块，从而在不牺牲甚至提升生成质量的前提下，大幅降低训练开销。

基于上述动机，本文提出 **熵引导优先级渐进学习（Entropy-Guided Prioritized Progressive Learning, Ent-Prog）** 框架，其设计目标为：

- 通过 **条件熵膨胀（CEI）** 量化跳过某块时预测噪声条件熵的增加量，以此作为该块对条件生成重要性的度量；
- 基于 CEI 优先级排序，制定 **优先级渐进学习（PPL）** 策略，优先解冻高重要性块；
- 引入 **自适应渐进调度**，通过嵌套扩散超网在每阶段初一次性评估候选解冻块数的收敛效率，动态选择最优解冻数量，实现性能与效率的平衡。

实验表明，Ent-Prog 在三个不同的人体视频生成数据集上实现了最高 2.2 倍训练加速和 2.4 倍 GPU 显存节省，且生成质量不降反升。

## 核心方法与创新机理

本工作针对高分辨率多帧人体视频扩散模型训练中的根本瓶颈——现有方法对所有网络参数均等更新，未考虑不同模块对条件生成任务的贡献差异，导致计算资源与显存消耗巨大且训练低效——提出了**熵引导优先级渐进学习（Entropy-Guided Prioritized Progressive Learning, Ent-Prog）**框架。其核心创新围绕两个紧密耦合的 changed slots 展开：

### 1. 训练策略：从均等更新到基于条件熵膨胀的优先级渐进解冻

**Baseline 策略**（Full Training）在训练伊始即将所有网络块全部解冻并平等更新，忽略了不同模块对条件依附程度的异质性。Ent-Prog 引入**条件熵膨胀（Conditional Entropy Inflation, CEI）**作为块重要性的量化度量：

$$
\Delta \mathcal{H}_{cond}(b, c) = \mathcal{H}\big(\hat{\epsilon} \mid x_{\tau}, \tau; \mathrm{skip}(b), c\big) - \mathcal{H}(\hat{\epsilon} \mid x_{\tau}, \tau; c)
$$

该公式衡量跳过块 $b$ 后预测噪声条件熵的增加量：CEI 越高，表明该块对条件生成的贡献越大。在高斯假设下，优先级分数可简化为跳过前后预测噪声标准差之比的对数：

$$
\pi(b) = \log \frac{\sigma_{\mathrm{skip}(b)}(\hat{\epsilon})}{\sigma(\hat{\epsilon})}
$$

基于此，**优先级渐进学习（Prioritized Progressive Learning, PPL）**在每阶段 $k$ 按优先级总和最大化原则选择解冻子网络：

$$
\psi_k = \underset{\psi \subseteq \mathcal{B}}{\arg\max} \sum_{b \in \psi} \pi_b \quad \mathrm{s.t.} \quad |\psi| = m_k
$$

这一 changed slot 的因果机制在于：将有限的计算与显存资源集中分配给高 CEI 块，使模型优先学习对条件生成最关键的表征，从而在减少训练负荷的同时加速收敛。**Figure 1** 提供了该设计的动机证据——冻结更多块导致收敛性能明显下降，而高 CEI 块的训练动态显著优于低 CEI 块。

### 2. 调度决策：从固定计划到基于收敛效率的自适应渐进调度

**Baseline 调度**采用固定训练计划，无动态负荷调整。Ent-Prog 引入**自适应渐进调度（Adaptive Progressive Schedule）**，使每阶段的解冻块数 $m_k$ 能够根据实际收敛动态进行优化。具体而言，每阶段初通过**嵌套扩散超网（Nested Diffusion Supernet）**一次性评估多个候选解冻数量 $m \in \mathcal{M}_k$ 的收敛效率：

$$
\mathrm{CE}(m) = -\frac{\sum_{s=2}^{S} \left(\ell_m^{(s)} - \ell_m^{(s-1)}\right)}{\sum_{s=2}^{S} \left(T_m^{(s)}\right)}
$$

该指标衡量候选解冻数对应的平均损失下降速率（单位时间内的损失改善）。超网通过参数嵌套实现权重共享，使得单次训练即可评估所有候选方案，搜索开销极低。随后选取 $\mathrm{CE}(m)$ 最高的 $m_k^*$ 继续本阶段剩余训练。

这一 changed slot 的核心价值在于实现了性能与效率的动态平衡：训练初期自动选择能快速收敛的较小解冻集以节省资源，后期逐步增加解冻块数以精调细节，避免了固定调度可能导致的训练不足或资源浪费。

### 创新耦合与整体优势

两个 changed slots 形成闭环：CEI 提供静态的块重要性排序（决定“哪些块优先训练”），自适应调度提供动态的解冻规模决策（决定“每阶段训练多少块”）。消融实验（Table 5）验证了这一耦合的必要性——移除 CEI 优先级后 FID-VID 从 32.15 恶化至 37.43，移除自适应调度后所有指标均下降；定性结果（Figure A）进一步显示，移除自适应调度导致背景保真度显著降低，移除 CEI 则造成细节严重退化。整体上，Ent-Prog 在 Bilibili、TikTok、UBC-Fashion 三个数据集上实现了最高 2.2× 训练加速和 2.4× 显存节省，且生成质量不降反升（如 Bilibili 视频生成 FVD 从 168.17 降至 120.35，降幅约 28%）。

Ent-Prog 的整体训练框架围绕一个核心洞察展开：扩散模型中不同网络块对条件视频生成的贡献并不均等。基于此，方法将高效训练分解为三个协同工作的模块，形成一个“评估优先级→渐进解冻→动态调度”的闭环。

**输入输出流**：框架的输入包括一个预训练的人体视频扩散模型 $\phi(\omega)$、目标条件生成任务的数据集，以及一个预设的渐进训练阶段序列。输出是一个经过高效微调的模型，其训练过程在显存占用和收敛速度上均显著优于全参数训练。

**Pipeline 模块关系**：

1. **条件熵膨胀（CEI）** 作为优先级评估器，在训练开始前对网络中所有块进行一次重要性量化。具体而言，对于每个网络块 $b$，CEI 计算跳过该块时预测噪声条件熵的增加量 $\Delta\mathcal{H}_{cond}(b, c)$，并将其转化为优先级分数 $\pi(b) = \log \frac{\sigma_{\mathrm{skip}(b)}(\hat{\epsilon})}{\sigma(\hat{\epsilon})}$。分数越高的块，对条件依附的贡献越大，训练优先级越高。

2. **优先级渐进学习（PPL）** 根据 CEI 产出的优先级排序，在每阶段 $k$ 选择优先级总和最大的 $m_k$ 个块组成解冻子网络 $\psi_k$：$$\psi_k = \underset{\psi \subseteq \mathcal{B}}{\arg\max} \sum_{b \in \psi} \pi_b \quad \mathrm{s.t.} \quad |\psi| = m_k$$ 这一机制确保有限的计算资源始终集中于对条件生成最关键的网络组件。

3. **自适应渐进调度** 负责动态决定每阶段应解冻的块数 $m_k$。在每阶段开始时，框架构建一个嵌套扩散超网 $\Phi(\hat{\omega})$，通过单次训练（one-shot supernet epoch）同时评估多个候选解冻数量 $m$ 的收敛效率 $\mathrm{CE}(m) = -\frac{\sum_{s=2}^{S} (\ell_m^{(s)} - \ell_m^{(s-1)})}{\sum_{s=2}^{S} T_m^{(s)}}$，然后选择收敛效率最高的 $m_k^*$ 继续该阶段剩余训练。超网参数直接继承到选定的子网络，避免了重复训练的开销。

三个模块形成的信息流是单向且高效的：CEI 一次性产出全局优先级排序，PPL 据此在每阶段构建候选子网络，自适应调度则通过超网快速筛选最优解冻规模。这种设计使得 Ent-Prog 在 Bilibili、TikTok 和 UBC-Fashion 三个数据集上均实现了最高 2.2× 的训练加速和 2.4× 的显存节省，且生成质量不降反升。

### 3.1 优先级渐进学习框架 (PPL)

Ent-Prog 的核心思路是将扩散模型的网络块集合 $\mathcal{B}$ 按重要性排序，在训练过程中逐步解冻。给定一个包含 $K$ 个阶段的渐进调度 $\Psi = (\psi_k)_{k=1}^{K}$，每个阶段 $k$ 解冻的子网络 $\psi_k$ 通过最大化所选块的优先级总和来确定：

$$
\psi _ { k } = \underset { \psi \subseteq \mathcal { B } } { \arg \operatorname* { m a x } } \sum _ { b \in \psi } \pi _ { b } \quad \mathrm { s . t . } \quad | \psi | = m _ { k }
$$

其中 $\pi_b$ 是块 $b$ 的训练优先级分数，$m_k$ 是阶段 $k$ 解冻的块数。该公式保证了在每阶段有限的计算预算下，优先将资源分配给对条件生成任务贡献最大的模块。

### 3.2 条件熵膨胀 (CEI)

CEI 是 Ent-Prog 的核心度量，用于量化每个网络块对条件生成的重要性。其理论基础是条件互信息：

$$
\mathcal { I } ( \hat { \epsilon } ; c \mid x _ { \tau } , \tau ) = \mathcal { H } ( \hat { \epsilon } \mid x _ { \tau } , \tau ) - \mathcal { H } ( \hat { \epsilon } \mid x _ { \tau } , \tau , c )
$$

该式刻画了预测噪声 $\hat{\epsilon}$ 与条件 $c$（如参考图像、姿态）之间的依赖强度。CEI 进一步定义为跳过某块 $b$ 时条件熵的增加量：

$$
\Delta \mathcal { H } _ { c o n d } ( b , c ) = \mathcal { H } \big ( \hat { \epsilon } \mid x _ { \tau } , \tau ; \mathrm { s k i p } ( b ) , c \big ) - \mathcal { H } ( \hat { \epsilon } \mid x _ { \tau } , \tau ; c )
$$

直观上，跳过某块后条件熵膨胀越大，说明该块对条件信息的提取和利用越关键。在高斯假设下，CEI 可简化为可计算的优先级分数：

$$
\pi ( b ) = \log \frac { \sigma _ { \mathrm { s k i p } ( b ) } ( \hat { \epsilon } ) } { \sigma ( \hat { \epsilon } ) }
$$

其中 $\sigma(\hat{\epsilon})$ 和 $\sigma_{\mathrm{skip}(b)}(\hat{\epsilon})$ 分别为完整模型和跳过块 $b$ 后预测噪声的标准差。$\pi(b)$ 越大，块 $b$ 的重要性越高，应在渐进训练中优先解冻。

### 3.3 自适应渐进调度

固定解冻块数 $m_k$ 无法适应不同训练阶段的收敛动态。Ent-Prog 引入自适应调度，在每阶段开始时通过**嵌套扩散超网**一次性评估多个候选解冻数量。超网 $\Phi(\hat{\omega})$ 将所有候选解冻选择的参数嵌套在共享权重空间 $\hat{\omega}$ 中，仅需训练一个 epoch 即可获得各候选的损失曲线。

收敛效率 $\mathrm{CE}(m)$ 定义为候选解冻数 $m$ 对应的平均损失下降率：

$$
\mathrm { C E } ( m ) ~ = ~ - \frac { \sum _ { s = 2 } ^ { S } \left( \ell _ { m } ^ { ( s ) } - \ell _ { m } ^ { ( s - 1 ) } \right) } { \sum _ { s = 2 } ^ { S } \left( T _ { m } ^ { ( s ) } \right) }
$$

其中 $\ell_m^{(s)}$ 是第 $s$ 步的损失，$T_m^{(s)}$ 是第 $s$ 步的耗时。超网训练结束后，选择 $\mathrm{CE}(m)$ 最高的 $m_k^*$ 作为当前阶段解冻块数，并从超网继承对应参数继续训练，实现性能与效率的动态平衡。

## 实验与关键发现

### 核心效率与性能权衡

Ent-Prog 的核心主张是在不牺牲生成质量的前提下显著压缩训练开销。该主张在 Bilibili、TikTok 和 UBC-Fashion 三个数据集上均得到验证。在 Bilibili 视频生成任务上，Ent-Prog 在 100k 步时 FVD 达到 120.35，相较全量训练的 168.17 降低 28%；同时训练加速最高达 2.17×（200k 步）。在 TikTok 数据集上，Ent-Prog 的 FVD 为 264.03，而全量训练为 385.64，相对提升 46.1%，训练加速 1.52×。在 UBC-Fashion 上，Ent-Prog 实现 1.69× 加速，GPU 显存占用降至全量训练的 63.0%（Table 3）。图像生成任务上，Bilibili 数据集的 FID 从 45.71 降至 44.09，TikTok 和 UBC-Fashion 的对应指标同样优于全量训练（Table 2、Table 4）。

![[assets/figures/papers/paper_list_l976_https_arxiv_org_abs_2511_21136/figures/009_Table_2.jpg]]
*Table 2: Results comparison of pose-guided human dance image generation on Bilibili dataset*

![[assets/figures/papers/paper_list_l976_https_arxiv_org_abs_2511_21136/figures/011_Table_3.jpg]]
*Table 3: Results on human video generation. Video quality comparison on the Tiktok and UBC-Fashion dataset*

![[assets/figures/papers/paper_list_l976_https_arxiv_org_abs_2511_21136/figures/012_Table_4.jpg]]
*Table 4: Results of pose-guided image generation on the Tiktok and UBC-Fashion dataset. Comparison of the results between Ent-Prog and Full training in the first two stages of imageconditioned modeling*

值得关注的是，Ent-Prog 在多个任务上不仅未损失性能，反而**超越**了全量训练。Table 1 显示，在 100k 步时 Ent-Prog 的 SSIM 为 0.781，全量训练为 0.772；LPIPS 从 0.197 降至 0.191。Figure 5 的定性对比进一步揭示：全量训练生成的视频出现不合理伪影和面部细节缺失，而 Ent-Prog 在这些区域表现更连贯、逼真。Figure 7 中，全量训练在 TikTok 数据上丢失了服装 Logo 并扭曲面部细节，Ent-Prog 则准确还原了参考图像中的细粒度信息。Figure 8 的 UBC-Fashion 案例更极端：全量训练出现了“三只脚”等违反物理规律的伪影，Ent-Prog 则保持了肢体连贯性。

![[assets/figures/papers/paper_list_l976_https_arxiv_org_abs_2511_21136/figures/008_Table_1.jpg]]
*Table 1: Results comparison of efficient training on the Bilibili dataset. The reported training time speedup corresponds to the wall time of the training process*

![[assets/figures/papers/paper_list_l976_https_arxiv_org_abs_2511_21136/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of two training methods on the Bilibili dataset. The red boxes indicate the defects of the generated images. Ent-Prog surpasses full training in terms of visual coherence and realism, and it also excels in restoring fine-grained details such as facial expressions. The first row highlights the unreasonable artifacts in the results generated by the full training method, which are absent in Ent-Prog. The second row marks the shortcomings of the full training method in restoring facial features*

![[assets/figures/papers/paper_list_l976_https_arxiv_org_abs_2511_21136/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative comparison of two training methods on TikTok dataset. The red boxes indicate the defects of the generated videos. With the original training method, the top-left example shows that the logo on the garment is missing, while other examples show distortions in facial details. In contrast, Ent-Prog accurately restores the detailed information from the reference image*

### 消融实验：CEI 优先级与自适应调度的因果贡献

Table 5 的消融实验直接验证了两个核心组件的因果作用。移除 CEI 训练优先级后，FID-VID 从 32.15 恶化至 37.43，FVD 从 264.03 升至 301.50，表明仅靠渐进解冻而不考虑块重要性会导致条件生成质量显著下降。移除自适应渐进调度后，所有量化指标同样全面下滑，FID 从 37.81 升至 42.67，SSIM 从 0.738 降至 0.721。

定性消融（Figure A）进一步揭示了两种失效模式：移除自适应调度主要导致**背景保真度大幅降低**，说明固定调度无法在效率与质量间取得动态平衡；移除 CEI 模块则导致**细粒度细节严重退化**，印证了 CEI 在识别和优先训练对条件依附关键块上的不可替代性。

### 训练动态与收敛行为

Figure 6 展示了训练过程中的指标演变。在第二阶段每 10 个 epoch 评估一次，Ent-Prog 在 FID、FID-VID、SSIM 和 LPIPS 四个指标上均以更快速度收敛，最终性能与全量训练持平或更优。该图标注的训练加速为 1.45×，与 Table 1 报告的 wall time 加速一致。

### 模型结构鲁棒性

Table I 对比了不同模型结构下的表现，结果显示 Ent-Prog 在不同 backbone 上均保持一致的效率优势，表明该方法对具体网络架构不敏感，具有良好的泛化性。

### 需人工验证的边界

分析中未发现明确的失败模式或局限性声明。论文未报告 Ent-Prog 在极端条件（如极低数据量、极短训练周期）下的退化行为，也未讨论 CEI 估计本身的计算开销是否在极大规模模型上成为新的瓶颈。这些边界条件需在实际部署中进一步验证。

## 定位与知识库关联

### 与全参数训练的关系

Ent-Prog 直接对标的是人体视频扩散模型的**全参数训练（Full Training / Original）**范式。在标准训练流程中，扩散模型的所有网络块从训练开始即全部解冻并平等更新，未考虑不同模块对条件生成任务的贡献差异。Ent-Prog 的核心改进在于引入**条件熵膨胀（CEI）**作为块级重要性度量，将训练转化为一个优先级驱动的渐进解冻过程：高 CEI 的块优先获得训练资源，低 CEI 的块在早期阶段保持冻结，从而在有限的计算预算下实现更高效的收敛。

从因果机制看，这一改进的瓶颈在于：全参数训练将计算均匀分配，而条件视频生成任务中不同网络块对条件信号的依附程度存在显著差异。Figure 1 的实验证据直接支撑了这一判断——冻结不同数量的块会导致模型最终收敛性能明显下降，而随机跳过 8 到 23 个块时，损失和 CEI 的变化趋势表明，选择性跳过低交互块可以加速收敛。这构成了 Ent-Prog 区别于全参数训练的根本逻辑：**并非所有参数对条件生成同等重要**。

### 与渐进训练方法的关系

渐进训练（Progressive Learning）本身并非全新概念，在高效训练领域已有先例。Ent-Prog 的增量贡献在于将渐进训练与**块级重要性排序**和**自适应调度**相结合，形成了三个层次的方法创新：

1. **优先级判定层**：传统渐进训练通常按网络深度或随机顺序解冻，Ent-Prog 则通过 CEI 量化每个块对条件生成的重要性，将渐进顺序与任务相关性显式绑定。CEI 的核心公式为 $\Delta \mathcal{H}_{cond}(b, c) = \mathcal{H}(\hat{\epsilon} \mid x_{\tau}, \tau; \mathrm{skip}(b), c) - \mathcal{H}(\hat{\epsilon} \mid x_{\tau}, \tau; c)$，在高斯假设下退化为优先级分数 $\pi(b) = \log \frac{\sigma_{\mathrm{skip}(b)}(\hat{\epsilon})}{\sigma(\hat{\epsilon})}$，实现了无需额外标注的自动化重要性评估。

2. **调度决策层**：传统渐进训练的每个阶段解冻块数通常是预定义的固定超参数。Ent-Prog 引入**收敛效率 CE(m)** 作为自适应选择指标：$\mathrm{CE}(m) = -\frac{\sum_{s=2}^{S} (\ell_m^{(s)} - \ell_m^{(s-1)})}{\sum_{s=2}^{S} T_m^{(s)}}$，在每个阶段初通过**嵌套扩散超网**一次性评估多个候选解冻数量的收敛效率，选取最优者继续训练。这使训练负荷能够根据实际收敛动态自动调整，而非依赖人工预设。

消融实验（Table 5）为这两层设计提供了强证据：移除 CEI 优先级后，TikTok 数据集上的 FID-VID 从 32.15 恶化至 37.43；移除自适应渐进调度后，所有量化指标均下降，定性结果（Figure A）显示背景保真度显著降低。这表明优先级判定和自适应调度各自贡献了不可替代的性能增益。

### 适用边界与局限

基于论文提供的实验证据，Ent-Prog 的适用边界可从以下几个维度界定：

**任务维度**：论文在三个数据集（Bilibili、TikTok、UBC-Fashion）上验证了人体视频生成和姿态引导图像生成任务，覆盖了条件扩散模型的典型应用场景。然而，论文未涉及无条件生成、文生图/视频、或非人体场景的验证，其跨任务泛化性尚需外部证据支持。

**模型结构维度**：Table I 展示了不同模型结构下的对比，但论文未详细说明 Ent-Prog 对 DiT、UNet 等不同扩散骨干网络的适用性差异。CEI 的计算依赖于网络块的可跳过性，对于具有复杂跳跃连接或共享参数的网络结构，块级粒度的定义可能需要重新设计。

**效率边界**：Ent-Prog 在 TikTok 上实现 1.52× 训练加速和 63.0% 显存占用，在 Bilibili 上实现最高 2.17× 加速。但这些加速比是在特定训练步数（100k/200k steps）下测得的，与全参数训练的收敛终点比较而非等性能比较。Figure 6 显示 Ent-Prog 在第二阶段的评估指标曲线上以 1.45× 的速度达到同等性能，但更长时间尺度下的效率优势是否会衰减，论文未提供证据。

**计算开销**：嵌套扩散超网的单次评估 epoch 本身引入了额外计算开销。论文未量化这一开销在整体加速中的占比，也未讨论当候选解冻数量空间增大时，超网训练的扩展性。这在实际部署中可能成为效率瓶颈。

### 开放问题

1. **CEI 度量的理论完备性**：CEI 在高斯假设下退化为标准差比的对数，但扩散模型预测噪声的实际分布可能偏离高斯假设，尤其在低信噪比阶段。这一近似在多大程度上影响优先级排序的准确性，论文未进行理论分析或实证验证。

2. **优先级排序的稳定性**：CEI 是在训练前的初始模型上计算的，但随着训练推进，各块的重要性可能发生变化。论文未探讨是否需要阶段性重新评估优先级，以及静态优先级在长训练周期下的有效性。

3. **与参数高效微调的关系**：Ent-Prog 的渐进解冻策略与 LoRA、Adapter 等参数高效微调方法在目标上相似（减少可训练参数），但实现路径不同。两者的结合潜力（例如在解冻块内进一步使用低秩适配）尚未被探索。

4. **多条件场景的扩展**：当条件信号包含多种模态（如姿态、文本、参考图像）时，不同块对不同条件的依附程度可能存在差异。CEI 目前仅提供单一条件的重要性度量，如何扩展到多条件加权优先级是一个开放方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Efficient_Training_for_Human_Video_Generation_with_Entropy_Guided_Prioritized_Progressive_Learning.pdf]]
