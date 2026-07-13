---
title: "UniRain: Unified Image Deraining with RAG-based Dataset Distillation and Multi-objective Reweighted Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniRain_Unified_Image_Deraining_with_RAG_based_Dataset_Distillation_and_Multi_objective_Reweighted_Optimization.pdf
project_link: "https://lowlevelcv.com/"
code_link: "https://github.com/QianfengY/UniRain"
aliases:
- UniRain
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过基于RAG的数据集蒸馏从海量公开数据中筛选出高质量混合训练样本，并引入多目标重加权优化策略动态平衡不同雨型的收敛速度，配合非对称MoE架构提升多退化特征建模能力。
primary_logic: 将数据集蒸馏（利用真实世界参考和视觉语言模型评估数据质量）与自适应多目标优化（基于收敛斜率估计动态调整各类型损失权重）相结合，可以从数据质量和训练动态两个层面解决统一图像去雨中的核心挑战。
claims:
- 直接合并所有数据集反而因质量干扰导致PSNR下降，如图1b所示。
- RAG蒸馏流水线在RainRAG四种雨型上取得了最高的平均PSNR（28.93 dB），明显优于直接合并或简单筛选。
- 多目标重加权优化相比固定权重和持续学习策略，在RainRAG上平均PSNR提升1.69 dB，且收敛过程更稳定。
- 非对称MoE架构（软编码器＋硬解码器）相比对称设计或单一专家，在所有退化类型上均获得一致的性能增益。
---

# UniRain: Unified Image Deraining with RAG-based Dataset Distillation and Multi-objective Reweighted Optimization

> [!tip] 核心洞察
> 将数据集蒸馏（利用真实世界参考和视觉语言模型评估数据质量）与自适应多目标优化（基于收敛斜率估计动态调整各类型损失权重）相结合，可以从数据质量和训练动态两个层面解决统一图像去雨中的核心挑战。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniRain：基于RAG数据集蒸馏与多目标重加权优化的统一图像去雨 |
| 英文题名 | UniRain: Unified Image Deraining with RAG-based Dataset Distillation and Multi-objective Reweighted Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.03967) · [Project](https://lowlevelcv.com/) · [Code](https://github.com/QianfengY/UniRain) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UniRain |
| Dataset | Real-world public benchmarks, WeatherBench |

> [!tip] 效果简介
> - Real-world public benchmarks (SPA-Data, GT-Rain, LHP-Rain, etc.) 上，PSNR 29.42 vs URIR (27.69) (+1.73)。
> - WeatherBench (all-in-one weather restoration) 上，PSNR 26.01 vs TransWeather (数值未显式给出) (N/A)。

## 概要

图像去雨是低层视觉恢复中的核心任务之一，但现有方法大多针对单一雨型（如白天的雨线或雨滴）设计，难以泛化到包含白天/夜晚、雨线/雨滴等多种组合的真实复杂场景。直接合并所有公开数据集看似能扩大数据规模，却因数据质量参差不齐反而导致模型性能下降（见 Figure 1b）；同时，不同雨型在联合训练中的损失收敛速度存在显著差异，简单加权会造成严重的不平衡，使模型偏向简单退化而忽略复杂退化（见 Figure 1c–d）。

针对上述瓶颈，本文提出 **UniRain**——一个统一的图像去雨框架，核心思路是从数据质量和训练动态两个层面协同解决问题：

1. **基于 RAG 的数据集蒸馏**：利用检索增强生成（Retrieval-Augmented Generation）流水线，从海量公开数据中筛选出与真实雨图分布接近的高质量样本，形成蒸馏数据集 RainRAG，为混合训练提供可靠的数据基础。
2. **多目标重加权优化**：通过滑动窗口最小二乘估计各雨型的收敛斜率，动态计算类型平衡分数（TBS）、类型稳定性分数（TSS）和自适应因子（AF），生成每个雨型的损失权重，实现多目标训练的均衡收敛。
3. **非对称 MoE 架构**：编码器采用 soft-MoE（连续路由，融合多专家信息），解码器采用 hard-MoE（Top-k 稀疏路由，专注纹理重建），以异构设计提升多退化特征的建模能力。

在方法谱系中，UniRain 区别于 **Restormer**（Zamir et al., CVPR 2022）等通用恢复基线、**URIR**（Yan, AAAI 2025）等统一去雨方法，以及 **PromptIR**（Potlapalli et al., NeurIPS 2023）等基于提示学习的范式。其关键创新在于将数据集层面的质量筛选与优化层面的自适应加权相结合，而非仅依赖网络架构的改进。

实验表明，UniRain 在提出的 RainRAG 数据集上取得平均 PSNR 28.93 dB，在多个真实世界公开基准上达到 29.42 dB，相比 URIR 提升 1.73 dB（Table 1 & Table 2）。消融实验进一步验证了 RAG 蒸馏流水线、多目标重加权策略和非对称 MoE 架构各自对性能的显著贡献（Table 4–6）。此外，该方法在驾驶、无人机、海事等场景下展现出良好的泛化能力，并可扩展到全天候恢复任务（雨、雪、雾），在 WeatherBench 上取得 26.01 dB 的平均 PSNR（Table 7）。



图像去雨是低层视觉领域的重要任务，旨在从受雨况退化的图像中恢复干净背景。近年来，深度学习方法在该任务上取得了显著进展，涌现出多种专门化架构。然而，现有方法大多针对单一雨型设计——例如仅处理白天的雨线（rain streaks）或雨滴（raindrops），难以泛化到包含多种真实雨况的场景。这一局限性的根源在于真实世界中的雨况退化具有高度多样性：白天与夜晚的光照条件迥异，雨线与雨滴的物理形态和遮挡效应也截然不同。直接训练一个统一模型面临两个核心瓶颈：

**数据瓶颈：质量参差不齐。** 公开可用的去雨数据集数量庞大，但质量差异显著。如图1a所示，不同数据集的样本在图像清晰度、退化真实感和标注精度上存在明显差距。一个直观的思路是将所有可用数据集直接合并以扩大训练规模，但实验表明（图1b），这种简单合并反而导致PSNR下降——低质量数据中的噪声和伪影干扰了模型收敛，稀释了高质量样本的指导信号。

**优化瓶颈：多目标训练不平衡。** 当模型同时学习多种雨型时，不同类型的损失函数收敛速度存在显著差异。如图1c所示，白天雨线（DRS）、白天雨滴（DRD）、夜间雨线（NRS）和夜间雨滴（NRD）的损失曲线下降速率各不相同。简单联合训练会导致模型偏向收敛较快的简单退化类型（如白天雨线），而忽视收敛较慢的复杂退化（如夜间雨滴），最终造成不同雨型间的PSNR偏差（图1d）。

上述两个瓶颈相互耦合：数据质量的干扰加剧了优化过程中的不平衡，而优化策略的缺陷又放大了数据筛选不当的负面影响。因此，实现统一的图像去雨需要同时从数据层面和训练动态层面进行系统性改进。UniRain正是基于这一认知，通过基于检索增强生成（RAG）的数据集蒸馏从海量公开数据中筛选高质量混合训练样本，并引入多目标重加权优化策略动态平衡不同雨型的收敛速度，从而在数据质量和训练动态两个维度上协同解决统一去雨的核心挑战。



## 核心方法与创新机理

UniRain 的核心创新围绕“统一图像去雨”的三个关键矛盾展开，分别从数据、优化和架构三个维度引入 changed slots，形成系统性解决方案。

### 1. 数据维度：基于 RAG 的数据集蒸馏

**现状瓶颈**：现有去雨方法大多针对单一雨型（如仅白天雨线）设计，直接合并所有公开数据集虽能扩大数据量，但不同来源的数据质量参差不齐（合成数据与真实数据之间存在显著的分布偏差），反而干扰模型收敛，导致 PSNR 下降（见 Figure 1b）。

**创新机制**：提出基于检索增强生成（RAG）的数据集蒸馏流水线，从百万级公开数据中自动筛选高质量混合训练样本。该流水线分为两个阶段：

- **检索阶段**：采用分层相似度匹配，依次计算语义相似度（CLIP 文本嵌入的 L2 距离，Eq.1）、视觉特征相似度（余弦相似度，Eq.2）和结构相似度（SSIM，Eq.3），从真实雨图数据库中检索与查询图像最匹配的参考样本。
- **生成阶段**：集成三个视觉语言模型（VLM）对查询图像的质量进行二元评估，采用多数投票机制（Eq.5）决定是否保留该样本。最终形成“数据质量金字塔”：顶层为真实雨图，中层为蒸馏出的高质量可靠样本，底层为被过滤的低质量数据。

**关键证据**：完整的 RAG 蒸馏流水线在 RainRAG 四种雨型上取得最高平均 PSNR（28.93 dB），显著优于直接合并或仅使用部分组件的策略（Table 1 & Table 4）。

### 2. 优化维度：多目标重加权优化

**现状瓶颈**：不同雨型（白天/夜晚、雨线/雨滴）的损失收敛速度存在显著差异（见 Figure 1c），简单联合训练会导致模型偏向简单退化而忽略复杂退化，造成严重的不平衡。

**创新机制**：提出自适应多目标重加权优化策略，通过动态调整各雨型的损失权重来平衡收敛过程。核心组件包括：

- **收敛斜率估计**（Eq.6）：在滑动窗口内对归一化损失进行最小二乘线性拟合，斜率 $\alpha$ 反映局部收敛速率（负值表示收敛）。
- **类型平衡分数 TBS**（Eq.7）：基于收敛斜率计算，收敛慢的类型获得更高权重，促使所有类型同步优化。
- **类型稳定性分数 TSS**（Eq.8）：利用历史斜率评估每个类型的内部稳定性，发散的类型得分低，抑制其权重。
- **自适应因子 AF**（Eq.9）：根据全局最大发散程度动态混合 TBS 和 TSS，早期由 TBS 主导，后期逐渐引入 TSS。
- **动态损失权重** $\omega_i(t)$（Eq.10）：将 AF 与 TBS、TSS 线性组合，生成每个雨型的最终权重。

**关键证据**：该策略相比固定权重和持续学习策略，在 RainRAG 上平均 PSNR 提升 1.69 dB，且收敛过程更稳定（Table 5, Figure 7）。将该策略应用到 PromptIR 可带来 0.97 dB 的 PSNR 增益，验证了其可迁移性。

### 3. 架构维度：非对称 MoE 架构

**现状瓶颈**：标准编码器-解码器或单一 MoE 架构难以同时兼顾多退化特征的充分提取与精细纹理重建。

**创新机制**：设计非对称混合专家（MoE）架构，编码器和解码器采用不同的路由策略：

- **Soft-MoE 编码器**（Eq.11–12）：对全局平均池化后的输入添加高斯噪声，经线性投影和 softmax 生成连续路由权重，加权组合所有专家输出，保留丰富的退化信息。
- **Hard-MoE 解码器**（Eq.13–14）：使用 Top-k 函数选择 softmax 输出中最大的 k 个权重，其余置零，实现稀疏专家激活，专注于精细纹理重建。

**关键证据**：非对称设计（软编码器 + 硬解码器）在四种雨型上均优于仅使用 soft-MoE 或 hard-MoE 的对称设计，验证了异构架构的必要性（Table 6）。

### 创新总结

三个 changed slots 形成闭环：RAG 蒸馏从源头保证训练数据质量，多目标重加权优化在训练过程中动态平衡不同退化的学习难度，非对称 MoE 架构为多退化特征建模提供结构支撑。三者协同使得 UniRain 在统一去雨任务上取得一致且显著的性能增益。



UniRain 的整体设计围绕一个核心矛盾展开：现有去雨方法大多针对单一雨型（如白天雨线或白天雨滴）设计，而真实场景中雨况复杂多样，直接合并所有公开数据集反而因数据质量参差不齐导致模型性能下降（Figure 1b）。同时，不同雨型的损失收敛速度存在显著差异，简单联合训练会使模型偏向简单退化而忽略复杂退化（Figure 1c–d）。为系统性地解决这两个瓶颈，UniRain 将**数据质量筛选**与**训练动态平衡**统一到一个端到端框架中。

Figure 2 给出了完整的流水线架构，由三大模块级联构成：

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of UniRain. (Left) The RAG-based dataset distillation pipeline retrieves real rainy references consistent with the query image via multi-level similarity search and employs vision language models to evaluate its quality, thereby distilling reliable samples from public datasets. (Right) The asymmetric MoE architecture consists of soft-MoE encoder and hard-MoE decoder, optimized via the multi-objective reweighted strategy to achieve balanced learning and robust performance across multiple rain degradation types*

---

### 1. RAG 数据集蒸馏流水线（数据准备阶段）

该模块的目标是从百万级公开数据中蒸馏出一个高质量、覆盖四种目标雨型（白天雨线 DRS、白天雨滴 DRD、夜间雨线 NRS、夜间雨滴 NRD）的混合训练集 **RainRAG**。流水线分为检索和生成两个阶段：

- **检索阶段**：对每张查询雨图，在真实雨图参考数据库中执行分层相似度匹配，依次计算语义相似度 $s_{txt}$（CLIP 文本嵌入的 L2 距离，Eq.1）、视觉特征相似度 $s_{vis}$（余弦相似度，Eq.2）和结构相似度 $s_{perc}$（SSIM，Eq.3），召回最相关的真实参考样本。
- **生成阶段**：将查询图像、检索到的参考集和提示模板送入三个视觉语言模型（VLM），各自输出可靠性判断 $R_q$（Eq.4），最终通过多数投票决定是否保留该样本（Eq.5）。被接受的样本进入数据质量金字塔的中间层——蒸馏后的高质量可靠数据，与顶层真实雨图共同构成 RainRAG 训练集。最终 RainRAG 仅保留了原始数据量的约 2.6%（52,869 对），但覆盖了四种目标雨型的高质量分布。

---

### 2. 非对称 MoE 架构（特征提取与重建）

在获得蒸馏数据集后，UniRain 采用非对称混合专家架构进行统一的图像去雨：

- **Soft-MoE 编码器**：对输入特征进行全局平均池化后添加高斯噪声，经线性投影和 softmax 生成连续路由权重 $\mathcal{R}_{soft}$（Eq.11），所有专家输出按该权重加权融合。软路由保留了丰富的退化信息，适合编码阶段的多类型特征提取。
- **Hard-MoE 解码器**：对解码器输入采用 Top-k 稀疏路由 $\mathcal{R}_{hard}$（Eq.13），仅激活最相关的少数专家进行纹理重建。硬路由使解码器能专注于精细细节恢复，避免不同退化类型之间的特征干扰。

消融实验（Table 6）表明，这种“软编码器 + 硬解码器”的非对称设计在所有四种雨型上均优于仅使用 soft-MoE 或 hard-MoE 的对称架构，验证了异构设计的必要性。

---

### 3. 多目标重加权优化（训练动态调控）

在训练过程中，该模块动态调整四种雨型的损失权重，以解决收敛不平衡问题。其核心机制如下：

1. **收敛斜率估计**：在滑动窗口内对各雨型的归一化损失进行最小二乘线性拟合，得到局部收敛斜率 $\alpha$（Eq.6），负值表示收敛，正值表示发散。
2. **类型平衡分数 TBS**（Eq.7）：基于收敛斜率计算，收敛慢的类型获得更高权重，促使所有类型同步优化。
3. **类型稳定性分数 TSS**（Eq.8）：利用历史斜率评估各类型的内部稳定性，发散的类型得分被抑制。
4. **自适应因子 AF**（Eq.9）：根据全局最大发散程度动态调整 TBS 和 TSS 的混合比例——训练早期由 TBS 主导以快速拉平各类型进度，后期逐渐引入 TSS 以抑制不稳定类型。
5. **动态损失权重**：最终权重 $\omega_i(t)$ 由 AF 对 TBS 和 TSS 进行线性组合得到（Eq.10），用于加权各雨型的重建损失。

消融实验（Table 5）显示，该策略相比固定权重和持续学习策略在 RainRAG 上平均 PSNR 提升 1.69 dB，且收敛过程更稳定（Figure 7）。

---

### 数据流总览

整个框架的数据流可以概括为：**公开多源雨图 → RAG 蒸馏流水线 → RainRAG 高质量混合训练集 → 非对称 MoE（Soft-MoE 编码 → Hard-MoE 解码）→ 多目标重加权损失优化 → 统一去雨输出**。三个模块协同工作，分别从数据质量、架构容量和优化动态三个维度解决统一图像去雨的核心挑战。



UniRain 围绕三个核心模块构建：**基于RAG的数据集蒸馏流水线**、**多目标重加权优化策略**以及**非对称MoE架构**。三者分别从数据质量筛选、训练动态平衡和异构特征建模三个层面，协同解决统一图像去雨中数据质量参差与多退化收敛不平衡的瓶颈。

### 3.1 基于RAG的数据集蒸馏

该模块的目标是从海量公开数据中筛选出与真实雨况分布接近的高质量样本，形成蒸馏数据集 RainRAG。流水线分为检索阶段和生成阶段。

**检索阶段**采用分层相似度匹配，依次计算三种相似性：

- **语义相似度**：利用 CLIP 文本编码器 $\phi_T$ 对查询图像 $q$ 和参考图像 $r$ 的文本描述 $T_q$、$T_r$ 进行编码，取 L2 距离：

$$s_{txt}(q,r) = \| \phi_T(T_q) - \phi_T(T_r) \|_2 \quad \text{(Eq.1)}$$

- **视觉特征相似度**：基于视觉特征嵌入 $f_q$、$f_{r'}$ 的余弦相似度，评估外观一致性：

$$s_{vis}(q,r') = \frac{f_q^\intercal f_{r'}}{\|f_q\|_2 \|f_{r'}\|_2} \quad \text{(Eq.2)}$$

- **结构相似度**：直接使用 SSIM 度量查询图像 $I_q$ 与候选参考图像 $I_{r''}$ 的感知一致性：

$$s_{perc}(q,r'') = SSIM(I_q, I_{r''}) \quad \text{(Eq.3)}$$

**生成阶段**引入视觉语言模型（VLM）进行质量评估。VLM $\mathcal{V}$ 结合查询图像 $I_q$、检索到的参考集 $S(q)$ 和提示模板 $P$ 生成响应：

$$R_q = \mathcal{V}(I_q, S(q), P) \quad \text{(Eq.4)}$$

随后集成三个 VLM 的二元预测，采用多数投票决定样本是否可靠（1 表示保留）：

$$\hat{R}_q = \begin{cases} 1 & \text{if } \sum_{i=1}^3 \mathbb{I}(R_q^i = 1) \geq 2, \\ 0 & \text{otherwise} \end{cases} \quad \text{(Eq.5)}$$

最终形成数据质量金字塔：顶层为真实雨图，中层为蒸馏出的高可靠样本，底层为被过滤的低质量数据。蒸馏后的 RainRAG 数据集仅保留原始数据的 2.6%（52,869 对），但质量显著提升。

### 3.2 多目标重加权优化

直接联合训练四种雨型（白天/夜晚的雨线和雨滴）时，不同退化的损失收敛速度差异显著（见 Figure 1c），导致模型偏向简单退化。为此，UniRain 引入自适应重加权策略，动态生成各雨型的损失权重 $\omega_i(t)$。

**收敛斜率估计**：在滑动窗口内对归一化损失进行最小二乘线性拟合，斜率 $\alpha$ 反映局部收敛速率（负值表示收敛）：

$$\alpha = \frac{\sum_{k=1}^N (k - \bar{k})(y_k - \bar{y})}{\sum_{k=1}^N (k - \bar{k})^2}, \quad \beta = \bar{y} - \alpha \bar{k} \quad \text{(Eq.6)}$$

**类型平衡分数（TBS）**：基于收敛斜率计算，收敛慢的类型获得更高权重，促使所有类型同步优化：

$$\mathrm{TBS}_i(t) = \mathrm{softmax}_i \left( K \frac{\alpha_i(t)}{\sum_{i=1}^K |\alpha_i(t)|} \right) \quad \text{(Eq.7)}$$

**类型稳定性分数（TSS）**：利用历史收敛斜率评估每个类型的内部稳定性，发散的类型得分低，抑制其权重：

$$\mathrm{TSS}_i(t) = \mathrm{softmax}_i \left( -N \frac{\alpha_i(t)}{\sum_{k=t-N+1}^t |\alpha_i(k)|} \right) \quad \text{(Eq.8)}$$

**自适应因子（AF）**：根据全局最大发散程度动态调整 TBS 和 TSS 的混合比例，早期由 TBS 主导加速收敛，后期逐渐引入 TSS 抑制震荡：

$$\mathrm{AF}(t) = \min \left( t \cdot \mathrm{softmax}_t \left( - \frac{\tau t \cdot \alpha_{\max}(t)}{\sum_{i=1}^t \alpha_{\max}(i)} \right), 1 \right) \quad \text{(Eq.9)}$$

**最终动态权重**由 AF 线性组合 TBS 和 TSS 得到：

$$\omega_i(t) = \mathrm{AF}(t) \mathrm{TBS}(t) + (1 - \mathrm{AF}(t)) \mathrm{TSS}(t), \quad i \in [1, K] \quad \text{(Eq.10)}$$

消融实验（Table 5）表明，该策略相比固定权重和持续学习策略在 RainRAG 上平均 PSNR 提升 1.69 dB，且收敛过程更稳定（Figure 7）。

### 3.3 非对称MoE架构

UniRain 采用编码器-解码器结构，但编码器和解码器使用不同的专家路由策略，形成非对称 MoE 设计。

**Soft-MoE 编码器**：对全局平均池化后的输入 $\varphi(x_{en})$ 添加高斯噪声 $\epsilon \sim \mathcal{N}(0, \sigma^2)$，经线性投影 $\mathcal{W}$ 和 softmax 生成连续路由权重，加权聚合所有专家输出：

$$\mathcal{R}_{soft} = \sigma(\mathcal{W}(\varphi(x_{en} + \epsilon))) \quad \text{(Eq.11)}$$

软路由使每个输入特征通过多个专家的加权组合进行融合，保留丰富的退化信息。

**Hard-MoE 解码器**：使用 Top-k 函数 $\mathcal{T}_k$ 选择 softmax 输出中最大的 $k$ 个权重，其余置零，实现稀疏专家激活：

$$\mathcal{R}_{hard} = \mathcal{T}_k(\sigma(\mathcal{W}(\varphi(x_{de} + \epsilon)))) \quad \text{(Eq.13)}$$

硬路由使解码器专注于最相关的专家，有利于精细纹理重建。消融实验（Table 6）验证了软编码器+硬解码器的异构设计在所有雨型上均优于对称设计，证明了非对称架构的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/001_Figure_1.jpg]]
*Figure 1: Overview of motivation. (a) Rainy image samples from public datasets, illustrating the noticeable differences in data quality. (b) Directly merging existing synthetic and real datasets enlarges data volume, yet quality disparity hinders performance, as shown by PSNR results. (c) The loss curves of DRS, DRD, NRS, and NRD (denoting daytime/nighttime rain streaks and raindrops) show different convergence rates, leading to imbalance in unified training. (d) The PSNR curves indicate that the model tends to favor simpler degradations but struggles with complex ones*



## 实验与关键发现

### 主实验结果

#### RainRAG 蒸馏数据集上的性能

在提出的 RainRAG 数据集上，UniRain 在四种雨型（白天雨线 DRS、白天雨滴 DRD、夜间雨线 NRS、夜间雨滴 NRD）上均取得领先性能，平均 PSNR 达到 **28.93 dB**，如表 1 所示。与通用恢复基线 **Restormer**（Zamir et al., CVPR 2022）相比，UniRain 在 DRD 子集上 PSNR 提升 1.35 dB；与 **NeRD-Rain**（Chen et al., CVPR 2024）相比提升 1.41 dB。该结果直接验证了 RAG 蒸馏数据集的质量优势和多目标优化策略的有效性。

#### 真实世界公开基准上的泛化性能

在多个真实世界公开基准（SPA-Data, GT-Rain, LHP-Rain 等）上，UniRain 取得平均 PSNR **29.42 dB**，相比统一去雨方法 **URIR**（Yan, AAAI 2025）的 27.69 dB 提升 **+1.73 dB**（表 2）。值得注意的是，在 WeatherBench 真实世界基准上，UniRain 恢复的图像细节清晰，甚至在某些样本上去除了 GT 图像中残留的雨滴，超越了参考真值（图 4）。

#### 扩展到全天候恢复

UniRain 在 WeatherBench 多天气退化基准（雨、雪、雾）上取得平均 PSNR **26.01 dB**（表 7），验证了该方法在更广泛退化类型上的迁移能力。雾天和雪天输入的视觉对比（图 8）进一步表明，UniRain 恢复结果在纹理保真度和退化去除方面均优于对比方法。

#### 模型复杂度

在 256×256 输入下，UniRain 的 FLOPs 和参数量与主流方法相当（表 3），在性能大幅领先的前提下保持了可接受的计算开销。

---

### 消融实验

#### RAG 数据集蒸馏的消融

表 4 系统消融了 RAG 蒸馏流水线的各组件。完整的检索+生成流水线在 RainRAG 上取得最高 PSNR/SSIM，而仅使用检索筛选或仅使用 VLM 生成均导致性能下降。直接合并所有公开数据集（无蒸馏）的性能最差，与图 1b 的动机分析一致——数据量的简单堆叠因质量参差不齐反而损害模型收敛。

#### 多目标重加权优化的消融

表 5 对比了不同优化策略。所提多目标重加权优化相比固定权重和持续学习策略（如 ），在 RainRAG 上平均 PSNR 提升 **1.69 dB**。将该优化策略应用到 **PromptIR**（Potlapalli et al., NeurIPS 2023）可带来 0.97 dB 的 PSNR 增益；在相同优化策略下，UniRain 比 PIGWM 高 2.23 dB，表明优化策略具有模型无关的通用性，且与 UniRain 架构形成正向协同。

图 7 展示了不同优化策略变体（固定权重、仅 TBS、TBS+TSS、完整方案）的损失和 PSNR 曲线。完整方案（TBS+TSS+AF）使四种雨型的损失下降更加均衡，收敛过程稳定；而固定权重或仅使用单一项时，部分类型的损失出现发散或停滞，验证了自适应因子 AF 在训练早期由 TBS 主导、后期逐步引入 TSS 的动态调节机制的必要性。

#### 非对称 MoE 架构的消融

表 6 的消融表明，软编码器+硬解码器的非对称设计在四种雨型上均优于仅使用 soft-MoE 或 hard-MoE 的对称架构。软编码器通过连续路由保留丰富的退化特征，硬解码器通过 Top-k 稀疏激活专注于精细纹理重建，二者异构协同是实现统一高性能去雨的关键。

---

### 关键图表结论

- **图 1**：揭示了统一去雨的核心瓶颈——不同公开数据集质量差异大，直接合并导致 PSNR 下降（图 1b）；四种雨型损失收敛速度不同，简单联合训练引发严重不平衡（图 1c），模型偏向简单退化而忽视复杂退化（图 1d）。
- **图 2**：完整呈现了 UniRain 框架——左侧 RAG 蒸馏流水线通过多级相似度检索和 VLM 集成投票筛选高质量样本；右侧非对称 MoE 架构配合多目标重加权优化实现平衡学习。
- **图 3**：RainRAG-NRS 和 RainDS-real-RD 上的视觉对比显示，UniRain 在去除雨线/雨滴的同时更好地保留了背景纹理，伪影明显少于对比方法。
- **图 5**：驾驶、无人机、海事等多场景泛化结果验证了方法的鲁棒性，UniRain 在所有场景下均取得最佳恢复效果。
- **图 6**：不同数据集组合策略的特征分布统计分析表明，RAG 蒸馏后的数据分布更接近真实雨图，为训练提供了更高质量的特征空间。

---

### 公平性说明

所有比较方法均使用相同的 RainRAG 蒸馏数据集、300k 训练迭代、相同的数据增强和余弦退火学习率调度（从头训练），确保比较的公平性。训练在 4 块 NVIDIA RTX 4090 GPU 上进行，使用 AdamW 优化器，初始学习率 $2 \times 10^{-4}$，最终学习率 $1 \times 10^{-6}$，批量大小 8，随机裁剪至 128×128 补丁。

### 补充图表

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/003_Table_1.jpg]]
*Table 1: Quantitative evaluations on the proposed RainRAG dataset, where DRS, DRD, NRS, and NRD denote daytime rain streaks, daytime raindrops, nighttime rain streaks, and nighttime raindrops, respectively. The best and second-best values are bold and underlined*

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/005_Table_2.jpg]]
*Table 2: Quantitative evaluations on the real-world public benchmarks. The best and second-best values are bold and underlined*

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/010_Table_4.jpg]]
*Table 4: Ablation analysis for RAG-based dataset distillation*

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/012_Table_5.jpg]]
*Table 5: Ablation analysis on various models using different optimizers, including our adaptive reweighting optimization strategy*

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/011_Table_6.jpg]]
*Table 6: Ablation analysis of asymmetric MoE architecture. Experiments are conducted on the proposed RainRAG dataset*

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/014_Figure_7.jpg]]
*Figure 7: Loss and PSNR of the optimization strategy variants*

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/004_Figure_3.jpg]]
*Figure 3: Visual comparison of image deraining results on the RainRAG-NRS and RainDS-real-RD datasets. Zoom in for a better view*

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/013_Table_7.jpg]]
*Table 7: Extension to all-in-one weather restoration on the WeatherBench dataset [14], which contains real-world multi-weather degradations (rain, snow, and haze). Average results are reported*

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/008_Table_3.jpg]]
*Table 3: Comparisons of model complexity against state-of-the-art methods. The size of the test image is 256 × 256 pixels*

![[assets/figures/papers/paper_list_l2710_https_arxiv_org_abs_2603_03967/figures/015_Figure_8.jpg]]
*Figure 8: Visual comparison of all-in-one weather restoration results (e.g., hazy input (first row) and snowy input (second row))*



## 定位与知识库关联

### 1. 与现有方法的关系

UniRain 并非孤立地提出一个全新的网络架构，而是在**数据构建策略**、**多目标训练动态**和**架构设计**三个层面上对现有统一图像恢复范式进行了系统性改进。理解其定位，需要分别考察它在每个层面与 baseline 工作的继承与差异。

**（1）数据层面：从“合并所有数据”到“蒸馏高质量数据”**

在 UniRain 之前，统一去雨（或更广泛的统一天气恢复）方法在训练数据上的典型做法是直接合并多个公开数据集，或者仅使用单一类型的数据集进行训练。例如 **TransWeather**（Valanarasu et al., CVPR 2022）和 **URIR**（Yan, AAAI 2025）等统一恢复方法，其训练数据构建策略本质上仍属于“简单合并”或“按类型分别训练”的范畴。UniRain 的作者通过实验明确指出，直接合并所有可用数据反而会因为数据质量参差不齐而导致 PSNR 下降（见 Figure 1b），这一发现构成了 RAG 蒸馏流水线的直接动机。

UniRain 提出的 RAG-based 数据集蒸馏流水线，其核心创新在于将**检索增强生成（RAG）** 的思想从自然语言处理领域迁移到低层视觉的数据筛选中：利用真实世界雨天图像作为参考，通过语义-视觉-结构三层相似度检索和 VLM 集成投票，从百万级公开数据中筛选出高质量样本。这一策略与 PromptIR（Potlapalli et al., NeurIPS 2023）等基于提示学习的方法在理念上有本质区别——后者通过可学习的提示来适应不同退化类型，而 UniRain 选择从数据源头解决问题。

**（2）优化层面：从固定权重到收敛斜率驱动的自适应重加权**

多任务学习中的损失加权是一个经典问题。在统一图像恢复中，现有方法大多采用固定权重或简单的手动调节策略。UniRain 的多目标重加权优化策略在思路上借鉴了动态权重调整的通用框架，但其具体实现——通过滑动窗口最小二乘估计收敛斜率 $\alpha$，进而计算类型平衡分数（TBS）、类型稳定性分数（TSS）和自适应因子（AF）——是针对图像去雨中多种雨型收敛速度不一致这一特定瓶颈的原创设计。消融实验表明，该策略相比固定权重和持续学习策略在 RainRAG 上平均 PSNR 提升了 1.69 dB（Table 5），且收敛过程更加稳定（Figure 7）。

值得注意的是，该优化策略具有一定的**模型无关性**：当将其应用到 PromptIR 上时，同样带来了 0.97 dB 的 PSNR 增益（Table 5），说明多目标重加权优化的价值不局限于 UniRain 自身的架构。

**（3）架构层面：非对称 MoE 与通用恢复 backbone 的对比**

UniRain 的非对称 MoE 架构——编码器采用 soft-MoE（连续路由，所有专家加权融合），解码器采用 hard-MoE（Top-k 稀疏路由）——与当前主流的通用图像恢复 backbone 形成了互补而非替代的关系。

- 与 **Restormer**（Zamir et al., CVPR 2022）相比：Restormer 基于标准 Transformer 编码器-解码器，没有专家混合机制。UniRain 在相同训练条件下在所有四种雨型上均优于 Restormer（Table 1），这表明 MoE 架构在多退化建模中具有优势。
- 与 **NeRD-Rain**（Chen et al., CVPR 2024）和 **MSDT**（Chen et al., AAAI 2024）相比：这些方法是针对特定雨型设计的专用方法，缺乏对多种雨型的统一处理能力。UniRain 在 DRD 子集上分别高出 1.41 dB 和 1.35 dB（Table 1）。
- 与 **URIR**（Yan, AAAI 2025）相比：URIR 是同期提出的统一去雨基准方法，UniRain 在多个真实世界公开基准上平均 PSNR 领先 1.73 dB（Table 2），且在模型复杂度相当的情况下取得了更优的性能（Table 3）。

消融实验进一步揭示了非对称设计的必要性：仅使用 soft-MoE 或仅使用 hard-MoE 的对称设计在所有雨型上均不如软硬结合的方案（Table 6），验证了编码器需要保留丰富的退化信息、解码器需要专注于精细纹理重建这一设计直觉。

### 2. 适用边界

根据论文提供的实验证据，UniRain 的适用边界可以从以下几个维度进行界定：

- **退化类型覆盖**：当前版本覆盖四种雨型——白天雨线（DRS）、白天雨滴（DRD）、夜晚雨线（NRS）、夜晚雨滴（NRD）。扩展到全天候恢复（雨、雪、雾）的初步实验表明方法具有一定的泛化潜力（Table 7, Figure 8），但这部分实验的置信度相对较低（0.8），需要更多验证。
- **数据依赖**：RAG 蒸馏流水线依赖于真实世界雨天图像作为参考数据库，以及多个 VLM 的集成推理。在缺乏高质量真实参考或计算资源受限的场景下，蒸馏流水线的有效性可能受到限制。
- **训练成本**：蒸馏流水线需要额外的检索和 VLM 推理阶段，训练使用 4 块 NVIDIA RTX 4090 GPU，总迭代次数 300k。虽然推理阶段的 FLOPs 和参数量与 SOTA 方法相当（Table 3），但训练阶段的数据准备开销是不可忽略的。

### 3. 局限与开放问题

论文本身未在显式的“Limitations”章节中讨论方法的不足，但基于方法设计和实验设置可以识别出以下局限和开放问题：

**（1）RAG 蒸馏流水线的效率瓶颈**

当前的蒸馏流水线依赖多个 VLM 的集成推理来进行质量评估，这引入了显著的计算开销。一个自然的开放问题是：**能否用更轻量的无参考图像质量评估（NR-IQA）方法替代 VLM，在保持筛选质量的同时降低对大规模语言模型的依赖？** 论文未对此进行消融对比。

**（2）对新型退化类型的适应性**

多目标重加权优化策略的核心机制——收敛斜率估计和 TBS/TSS/AF 计算——依赖于预定义的雨型类别数量 $K$。当面对训练时未出现的新雨型或混合退化（如雨雪交加、雨雾共存）时，该策略能否在不重新定义类别的前提下自适应地调整权重，目前缺乏实验证据。扩展到 WeatherBench 的实验（Table 7）虽然展示了初步的泛化能力，但该实验的置信度标注为 0.8，且论文未详细分析优化策略在跨天气类型场景下的行为。

**（3）非对称 MoE 设计的理论支撑**

软编码器 + 硬解码器的非对称设计在实验中表现最优，但论文主要从直觉（编码器需要融合、解码器需要聚焦）和经验消融的角度进行论证，缺乏对“为什么这种非对称性在多退化建模中有效”的更深层分析。例如，是否与不同退化类型在特征空间中的可分离性有关，仍有待探索。

**（4）蒸馏数据集的质量上限**

RainRAG 数据集从原始数据中保留了约 2.6% 的样本（52,869 对）。虽然消融实验证明了蒸馏策略优于直接合并，但蒸馏过程本身的质量上限受限于 VLM 的判断能力和参考数据库的覆盖度。如果参考数据库本身存在偏差（例如主要包含某种光照条件下的雨天图像），蒸馏结果可能继承这种偏差。



## 原文 PDF

![[paperPDFs/CVPR_2026/UniRain_Unified_Image_Deraining_with_RAG_based_Dataset_Distillation_and_Multi_objective_Reweighted_Optimization.pdf]]
