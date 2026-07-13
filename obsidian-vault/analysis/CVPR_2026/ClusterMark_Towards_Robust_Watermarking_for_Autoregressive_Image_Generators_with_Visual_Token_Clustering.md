---
title: "ClusterMark: Towards Robust Watermarking for Autoregressive Image Generators with Visual Token Clustering"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ClusterMark_Towards_Robust_Watermarking_for_Autoregressive_Image_Generators_with_Visual_Token_Clustering.pdf
project_link: null
code_link: null
aliases:
- ClusterMark
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过对码本token进行聚类，使语义/几何相似的token共享相同的红/绿集合分配，从而在图像扰动后重建的token仍有较大概率落入同一集合。
primary_logic: 将水印的token级随机分组转换为聚类级分组，利用码本向量相似性将相似token绑定在同一集合中，大幅提升了对常见图像扰动的鲁棒性，且无需修改生成模型结构，训练免费版本即可显著改善。
claims:
- 聚类水印（训练免费）相比无聚类基线，在高斯模糊（Gauss. Blur R3）下AUC从0.621提升至0.951（LlamaGen GPT-B）。
- 消融实验表明降低聚簇数量k可提升鲁棒性，但k<64时生成质量（FID）显著下降，验证了聚类对鲁棒性与图像质量的权衡。
- LlamaGen GPT-B 256x256 - Gaussian Blur radius 3 上 AUC = 0.951 (Ours Clustering, k=64, training-free)
- LlamaGen GPT-L 384x384 - Gaussian noise std 0.2 上 AUC = 0.996 (Ours Clustering, k=64)
---

# ClusterMark: Towards Robust Watermarking for Autoregressive Image Generators with Visual Token Clustering

> [!tip] 核心洞察
> 将水印的token级随机分组转换为聚类级分组，利用码本向量相似性将相似token绑定在同一集合中，大幅提升了对常见图像扰动的鲁棒性，且无需修改生成模型结构，训练免费版本即可显著改善。

| 字段 | 内容 |
|------|------|
| 中文题名 | ClusterMark：基于视觉标记聚类的自回归图像生成鲁棒水印 |
| 英文题名 | ClusterMark: Towards Robust Watermarking for Autoregressive Image Generators with Visual Token Clustering |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lukovnikov_ClusterMark_Towards_Robust_Watermarking_for_Autoregressive_Image_Generators_with_Visual_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ClusterMark |
| Dataset | LlamaGen GPT-B 256x256 - Gaussian Blur radius 3, LlamaGen GPT-L 384x384 - Gaussian noise std 0.2 |

> [!tip] 效果简介
> - LlamaGen GPT-B 256x256 - Gaussian Blur radius 3 上，AUC 0.951 (Ours Clustering, k=64, training-free) vs 0.621 (Ours No Clustering) (+0.330)。
> - LlamaGen GPT-L 384x384 - Gaussian noise std 0.2 上，AUC 0.996 (Ours Clustering, k=64) vs 0.055 (Ours No Clustering) (+0.941)。

## 概要

自回归（AR）图像生成模型（如LlamaGen、RAR）通过将图像量化为离散token序列，在生成质量与效率上展现出巨大潜力。然而，为这类模型嵌入鲁棒水印面临一个根本性瓶颈：直接将大语言模型（LLM）中成熟的token级KGW水印（Kirchenbauer et al.）移植到AR图像模型时，图像扰动（如JPEG压缩、高斯模糊、噪声）会导致VQ-VAE编码器重建的token与原始生成token差异巨大，使得水印的红/绿集合分配被打乱，检测鲁棒性急剧下降——例如在LlamaGen GPT-B上，高斯模糊（半径3）下的AUC仅0.621。

ClusterMark的核心洞察在于**将水印的token级随机分组转换为聚类级分组**：利用码本向量的语义/几何相似性，通过k-means将词汇表划分为k个聚类，使相似token绑定在同一红/绿集合中。这样，即使扰动后重建的token发生漂移，只要漂移落在同一聚类内，水印信号便得以保留。这一设计无需修改生成模型结构，在训练免费（training-free）设置下即可将上述高斯模糊场景的AUC从0.621提升至0.951（LlamaGen GPT-B）；结合可选的token/cluster分类器微调后，鲁棒性进一步提升。

在方法谱系上，ClusterMark属于**生成时水印**，与后处理水印（如DWT-DCT-SVD、RivaGAN、TrustMark）和近期AR图像水印工作IndexMark形成对比。其关键创新在于将红/绿集合划分的哈希输入从“前一个token”改为“前一个token的聚类索引”，并将绿色集合构造从“随机选取token”改为“随机选取聚类后合并其token”。这一改动使得水印对常见图像扰动的鲁棒性大幅增强，同时保持极低的生成开销（LlamaGen GPT-B仅增加0.06秒）和毫秒级验证速度。

主要实验结果（Table 1）表明：在LlamaGen GPT-B 256×256上，ClusterMark（k=64，训练免费）在多种扰动下AUC均显著优于无聚类基线——高斯噪声（std 0.2）下AUC从0.055跃升至0.996；结合cluster classifier后，JPEG压缩（质量20）AUC达0.982，椒盐噪声（0.1）AUC达1.000。消融实验进一步揭示了聚类数k对鲁棒性与图像质量的权衡：降低k可提升鲁棒性，但k<64时FID显著恶化，且均匀区域的token重复会引发水印误检——这一问题通过前缀调优（Prefix Tuning）得到缓解。

自回归（Autoregressive, AR）图像生成模型近年来取得了显著进展，其核心范式是将图像离散化为视觉标记（token）序列，并通过自回归Transformer建模标记间的依赖关系。给定类别条件 $s$，图像 $x$ 的标记序列 $\{q_i\}$ 的联合分布被分解为：

$$\prod_{i}^{h \cdot w} p_{\theta}(q_i | q_{1:i-1}, s)$$

这一范式与大型语言模型（LLM）高度同构，因此自然引发了一个问题：能否将LLM领域成熟的生成时水印技术直接迁移到AR图像模型中？

**直接迁移的失败。** 在LLM水印中，KGW（Kirchenbauer et al.）方案是代表性方法：生成每一步基于前一个token的哈希将词汇表随机划分为红/绿集合，并通过在绿色token的logits上施加偏置 $\delta$ 来嵌入水印。检测时，统计生成序列中绿色token的比例，若显著偏离随机期望 $\gamma$，则判定含水印。然而，当这一token级水印被直接应用于AR图像模型时，面临根本性障碍：图像在传输过程中经历压缩、模糊、噪声等扰动后，VQ-VAE编码器重建的token序列与原始生成时的token序列**差异巨大**。由于红/绿集合分配完全依赖于前一个token的精确值，token的重建错误会导致集合分配被打乱，使得水印检测的鲁棒性急剧下降。实验表明，在LlamaGen GPT-L 384×384模型上，面对标准差0.2的高斯噪声，无聚类水印的AUC仅为0.055，几乎等同于随机猜测。

**现有水印方案的局限。** 当前图像生成模型的水印方案主要分为两类。后处理水印（如**DWT-DCT-SVD**、**RivaGAN**、**TrustMark**、**SSL**）在图像生成后嵌入水印，与生成过程解耦，但通常需要额外的编码器-解码器训练，且对强扰动的鲁棒性有限。生成时水印则在水印嵌入与生成过程耦合方面具有天然优势，但针对AR图像模型的工作极少——最近的**IndexMark**（Jovanovic et al., NeurIPS 2025）虽探索了这一方向，却未系统解决token扰动导致的鲁棒性瓶颈。

**核心洞察。** 本文的关键观察是：图像扰动虽然会改变VQ-VAE重建的具体token，但**语义或几何相似的token往往在码本空间中彼此接近**。因此，若能基于码本向量的相似性将token预先聚类，使同一聚类内的token共享相同的红/绿集合归属，那么即使扰动导致token在聚类内部漂移，其红/绿属性仍得以保持，从而大幅提升检测鲁棒性。这一思路将水印的token级随机分组转换为**聚类级分组**，无需修改生成模型结构，在训练免费（training-free）设置下即可显著改善鲁棒性，并可进一步结合微调的token/聚类分类器以应对更强扰动。

## 核心方法与创新机理

### 问题瓶颈：Token级水印在图像扰动下的脆弱性

将大语言模型（LLM）中成熟的KGW token级水印直接移植到自回归图像生成模型时，面临一个根本性失效模式。KGW水印在每一步生成时，基于前一个token的哈希值将词汇表随机划分为红/绿集合，并通过偏置绿色token的logits嵌入水印信号。验证时，从图像中通过VQ-VAE编码器重建token序列，统计绿色token比例进行二项分布检验。

然而，图像一旦经历常见的扰动（如高斯模糊、JPEG压缩、高斯噪声），VQ-VAE编码器重建出的token序列与原始生成时的token序列会产生巨大偏差。这种偏差导致验证时计算的红/绿集合分配与生成时完全不一致——原本被偏置为绿色的token在重建后可能被分配到红色集合，反之亦然。**因果瓶颈在于：token级的红/绿集合划分对图像扰动高度敏感，使得水印信号在物理信道中几乎完全丢失。** 实验证据表明，在LlamaGen GPT-B上，直接应用token级水印（Ours No Clustering）在高斯模糊（半径3）下AUC仅为0.621，几乎等同于随机猜测。

### 核心洞察：从Token级随机分组到聚类级语义绑定

ClusterMark的核心创新在于将水印的红/绿集合划分粒度从**单个token**提升到**token聚类**。其关键洞察是：VQ-VAE码本中的token向量本身蕴含语义和几何相似性——相似的视觉模式对应相近的码本向量。通过k-means对码本向量进行聚类，语义/几何相似的token被归入同一聚类。当水印以聚类为单位进行红/绿划分时，即使图像扰动导致重建token发生偏移，只要偏移后的token仍属于同一聚类（或语义相近的聚类），其红/绿属性就保持不变。

这一设计将水印的鲁棒性从脆弱的token恒等匹配，转化为对聚类成员关系的容错匹配——**扰动后重建token只要“落入”正确的聚类邻域，水印信号即可被保留**。

### Changed Slots：方法差异的结构化对比

以下从三个关键设计维度，对比ClusterMark与直接应用KGW token级水印的基线差异：

| 设计维度 | 基线方法（Token级KGW） | ClusterMark（本文方法） |
|---------|----------------------|----------------------|
| **红/绿集合划分方式** | 基于前一个token的哈希，对每个token单独随机分配红/绿属性 | 基于前一个token的**聚类索引**哈希，随机选择γ比例的聚类作为绿色聚类，同一聚类内所有token共享红/绿属性 |
| **哈希输入** | 前一个生成token $q_{i-1}$ | 前一个token的聚类索引 $c(q_{i-1})$ |
| **绿色token集合构造** | 从整个词汇表中随机选取γ比例的token | 随机选取γ比例的聚类，再将这些聚类包含的所有token合并为绿色集合 |

这一改变的因果效应直接体现在鲁棒性上：在LlamaGen GPT-B上，ClusterMark（训练免费，k=64）将高斯模糊（半径3）下的AUC从0.621提升至0.951（Table 1）；在LlamaGen GPT-L上，高斯噪声（std 0.2）下的AUC从0.055跃升至0.996。

### 方法架构与可选增强

ClusterMark的整体流程（Figure 1）包含以下核心模块：

1. **Token聚类（生成前预处理）**：对VQ-VAE码本的所有token向量执行k-means聚类，得到聚类分配函数 $c(\cdot)$，将词汇表划分为k个不相交子集。该步骤仅在生成前执行一次，不引入额外推理开销。

2. **基于聚类的加水印生成**：在自回归生成的每一步，基于前一个token的聚类索引 $c(q_{i-1})$ 计算哈希，随机选择 $\lfloor \gamma \cdot k \rfloor$ 个绿色聚类，偏置这些聚类内所有token的logits（增加惩罚值δ）。生成时间开销极小——LlamaGen GPT-B和GPT-L分别仅增加0.06秒（总3.7秒）和0.3秒（总14.3秒）。

3. **基于聚类哈希的验证**：对给定图像，用VQ-VAE编码器重建token序列，按相同聚类哈希方式计算绿色集合，统计绿色token比例，执行二项分布单侧检验。验证速度极快，仅需10-25毫秒（Table 2），与轻量后处理水印方法相当。

4. **（可选）Token/聚类预测器微调**：为进一步提升鲁棒性，可微调一个token分类器 $\mathcal{M}_T$ 或聚类分类器 $\mathcal{M}_C$，从扰动图像中更准确地预测原始token或聚类索引。损失函数分别为交叉熵：
   - Token分类器：$\mathcal{L}_{\mathrm{TC}} = \mathbb{E}_{(x,\{q_i\}) \sim p_\theta}[\sum_i \mathrm{CE}(\mathcal{M}_T(\phi(x))_i, q_i)]$
   - 聚类分类器：$\mathcal{L}_{\mathrm{CC}} = \mathbb{E}_{(x,\{q_i\}) \sim p_\theta}[\sum_i \mathrm{CE}(\mathcal{M}_C(\phi(x))_i, c(q_i))]$

   实验表明，结合聚类分类器后，在多种扰动下AUC可进一步提升至接近1.000（Table 1）。

### 训练免费版本的显著优势

值得强调的是，ClusterMark的**训练免费版本**（仅使用k-means聚类，不微调任何分类器）已经实现了对基线方法的巨大超越。在LlamaGen GPT-B上，训练免费的聚类水印FID为6.12，与未加水印基线的6.01极为接近，验证了该方法在不牺牲生成质量的前提下大幅提升鲁棒性的能力。这一特性使得ClusterMark可以即插即用地部署于任何已有的自回归图像生成模型，无需修改模型结构或重新训练。

ClusterMark 的整体 pipeline 围绕一个核心洞察展开：**将水印的 token 级随机分组转换为聚类级分组**，利用 VQ-VAE 码本向量的语义/几何相似性，将相似 token 绑定在同一红/绿集合中，从而在图像遭受扰动后，重建的 token 仍有较大概率落入与原始生成时相同的集合。

### 模块关系与数据流

系统由四个主要模块构成，其协作流程如 Figure 1 所示：

![[assets/figures/papers/paper_list_l846_https_openaccess_thecvf_com_content_CVPR2026_html_Lukovnikov_ClusterMark/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our proposed cluster-based watermark for AR image generators. Before generation, tokens are clustered based on codebook vector similarity, partitioning the vocabulary into a set of clusters. Additionally, a token or cluster classifier can be trained to further boost robustness (This figure shows the variant with the cluster classifer). At every generation step, the set of clusters is partitioned into green and red sets and sampling is biased towards tokens in green clusters. During verification, if the fraction of green tokens is significantly higher than random chance, the image is considered watermarked*

1. **Token Clustering（生成前预处理）**  
   在生成任何图像之前，对 AR 图像模型的码本向量应用 k-means 聚类，将整个词汇表 $V$ 划分为 $k$ 个互不相交的子集（聚类）$C_1, \ldots, C_k$，得到聚类分配函数 $c(\cdot)$：每个 token $q$ 映射到其所属的聚类索引 $c(q)$。这一步是训练免费的，仅需码本向量即可完成。

2. **Watermarked Generation with Clusters（带聚类的水印生成）**  
   在自回归生成的每一步 $i$，不再像 KGW 基线那样基于前一个 token $q_{i-1}$ 计算哈希，而是**基于前一个 token 的聚类索引 $c(q_{i-1})$** 计算哈希 $o_i = \text{hash}(\kappa, c(q_{i-1}))$。  
   随后，从 $k$ 个聚类中随机选取 $\lfloor \gamma \cdot k \rfloor$ 个作为绿色聚类，将这些聚类包含的所有 token 合并为绿色集合 $G_i$；其余 token 构成红色集合。最后，对绿色 token 的 logits 施加偏置 $\delta$，通过 softmax 得到加水印的下一 token 分布 $p_\theta'(y_i | y_{1:i-1})$，从中采样生成 token。

3. **Verification with Cluster Hash（基于聚类哈希的验证）**  
   给定待检测图像，首先用 VQ-VAE 编码器将其重建为 token 序列。然后按照与生成时完全相同的方式——基于前一个 token 的聚类索引计算哈希、选取绿色聚类、合并绿色 token 集合——统计整张图像中绿色 token 的数量 $N_g$。  
   在零假设 $H_0$（图像未加水印）下，$N_g$ 服从二项分布 $\text{Binomial}[T, \gamma]$，其中 $T$ 为总 token 数。通过单侧二项检验计算 p 值，若绿色 token 比例显著高于随机水平，则判定图像已加水印。

4. **(Optional) Token/Cluster Predictor（可选的鲁棒 token 重建）**  
   为进一步提升对强扰动的鲁棒性，可微调一个 token 分类器 $\mathcal{M}_T$ 或 cluster 分类器 $\mathcal{M}_C$，从扰动图像的 VQ-VAE 特征 $\phi(x)$ 中更准确地预测原始 token 索引或聚类索引。  
   - Token 分类器损失：$\mathcal{L}_{\mathrm{TC}} = \mathbb{E}_{(x,\{q_i\}) \sim p_\theta}\left[\sum_i \mathrm{CE}(\mathcal{M}_T(\phi(x))_i, q_i)\right]$
   - Cluster 分类器损失：$\mathcal{L}_{\mathrm{CC}} = \mathbb{E}_{(x,\{q_i\}) \sim p_\theta}\left[\sum_i \mathrm{CE}(\mathcal{M}_C(\phi(x))_i, c(q_i))\right]$

   这些分类器替换验证阶段的 VQ-VAE 编码器重建，使绿色集合分配更贴近原始生成时的状态，从而大幅提升检测鲁棒性。

### 关键设计决策

- **聚类粒度 $k$ 的权衡**：$k$ 越小，同一聚类内 token 越多，扰动后 token 仍落入正确聚类的概率越高，鲁棒性越强；但 $k < 64$ 时，图像中均匀区域易产生 token 重复，导致未加水印图像的虚假绿色 token 比例升高，生成质量（FID）显著下降。文中默认 $k=64$ 作为平衡点。
- **前缀调优（Prefix Tuning）**：针对小 $k$ 下某些哈希前缀 $\kappa$ 在未加水印图像上产生异常高绿色比例的问题，采用穷举搜索多个 $\kappa$ 值并选择假阳性最低者，有效缓解均匀区域引发的误检。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| 聚类预处理 | 码本向量 | 聚类分配函数 $c(\cdot)$ |
| 水印生成 | 类别条件 $s$、密钥 $\kappa$、参数 $\gamma, \delta, k$ | 加水印的 token 序列及对应图像 |
| 验证 | 待检测图像、密钥 $\kappa$、聚类分配 $c(\cdot)$ | 二值判定（加水印/未加水印）及 p 值 |
| 可选微调 | 原始图像-token 对、扰动函数 $\phi$ | 微调后的 token/cluster 分类器 |

ClusterMark 的核心设计围绕一个关键洞察展开：**将水印的 token 级随机红/绿分组替换为聚类级分组**，利用码本向量的语义/几何相似性，使相似 token 在扰动后仍能保持一致的集合归属。方法包含三个核心模块和一个可选增强模块。

### 3.1 码本 Token 聚类

在生成开始前，对 VQ-VAE 的码本词汇表 $\mathcal{V}$ 执行 k-means 聚类，将 $|\mathcal{V}|$ 个 token 划分为 $k$ 个不相交子集：

$$C_1, C_2, \ldots, C_k \subset \mathcal{V}, \quad \bigcup_{j=1}^{k} C_j = \mathcal{V}$$

聚类依据是码本向量的余弦相似度，因此语义或几何上相近的视觉 token 会被归入同一聚类。聚类分配函数记为 $c(q)$，返回 token $q$ 所属的聚类索引。这一步骤仅需执行一次，不参与生成或验证的在线计算。

**设计动机**：在无聚类基线中，哈希输入为前一个生成 token $q_{i-1}$，红/绿集合的划分对该 token 的精确取值高度敏感。图像经扰动后，VQ-VAE 编码器重建的 token 序列与原始生成 token 差异显著，导致红/绿分配被完全打乱，水印检测失效。聚类将哈希输入从 token 身份提升为聚类身份，使得扰动后重建的 token 即使与原始 token 不同，只要落入同一聚类，仍能保持正确的集合归属。

### 3.2 基于聚类的带水印生成

在自回归生成的每一步 $i$，绿色 token 集合的构造方式如下：

1. **哈希输入替换**：将哈希函数的输入从前一个 token $q_{i-1}$ 替换为其聚类索引 $c(q_{i-1})$：
   $$o_i = \text{hash}(\kappa, c(q_{i-1}))$$
   其中 $\kappa$ 为秘密哈希前缀。

2. **绿色聚类选取**：使用伪随机数生成器 $\text{PRNG}$，以 $o_i$ 为种子，从 $k$ 个聚类中随机选取 $\lfloor \gamma \cdot k \rfloor$ 个作为绿色聚类，其中 $\gamma \in (0, 1)$ 为绿色比例超参数。

3. **绿色 token 集合构造**：将所选绿色聚类包含的所有 token 合并，得到当前步的绿色 token 集合 $G_i$。同一聚类内的所有 token 共享相同的红/绿属性。

4. **Logits 偏置**：对绿色 token 的 logits 增加惩罚项 $\delta > 0$，偏置后的下一个 token 分布为：
   $$p_{\theta}'(y_i | y_{1:i-1}) = \text{softmax}\big(f_{\theta}(y_{1:i-1}) + m_i \cdot \delta\big)$$
   其中 $m_i$ 为指示向量，绿色 token 对应位置为 1，红色为 0。

### 3.3 水印验证

对给定图像，使用 VQ-VAE 编码器重建 token 序列 $\{\hat{q}_i\}$，按与生成时相同的方式（基于 $c(\hat{q}_{i-1})$ 计算哈希、选取绿色聚类）统计绿色 token 数量 $N_g$。在零假设 $H_0$（图像未加水印）下，$N_g$ 服从二项分布：

$$H_0: N_g \sim \text{Binomial}[T, \gamma]$$

其中 $T$ 为 token 序列总长度。通过单侧二项检验计算 p 值，若绿色 token 比例显著高于随机水平 $\gamma$，则判定图像已加水印。

### 3.4 （可选）Token/Cluster 分类器微调

为进一步提升对强扰动的鲁棒性，可微调一个轻量分类器，从扰动图像中更准确地重建原始 token 或聚类索引。分类器 $\mathcal{M}$ 以冻结的 VQ-VAE 编码器特征 $\phi(x)$ 为输入，输出每个位置的 token 或聚类预测。

**Token 分类器损失**：预测原始 token 索引 $q_i$ 的交叉熵：
$$\mathcal{L}_{\mathrm{TC}} = \mathbb{E}_{(x,\{q_i\}) \sim p_{\theta}}\left[\sum_i \mathrm{CE}\big(\mathcal{M}_T(\phi(x))_i, q_i\big)\right]$$

**Cluster 分类器损失**：预测原始聚类索引 $c(q_i)$ 的交叉熵：
$$\mathcal{L}_{\mathrm{CC}} = \mathbb{E}_{(x,\{q_i\}) \sim p_{\theta}}\left[\sum_i \mathrm{CE}\big(\mathcal{M}_C(\phi(x))_i, c(q_i)\big)\right]$$

训练数据通过模型自身生成图像并施加目标扰动来构造，无需外部标注。验证时，用分类器预测的 token 或聚类索引替代 VQ-VAE 编码器的直接重建结果，再执行标准的聚类哈希验证流程。

### 3.5 前缀调优（Prefix Tuning）

当聚簇数 $k$ 较小时，某些哈希前缀 $\kappa$ 可能在未加水印图像的均匀区域中产生虚假的绿色 token 重复模式，导致假阳性率升高。为此，ClusterMark 采用简单的前缀调优策略：在多个候选 $\kappa$ 值上评估未加水印图像的绿色 token 比例分布，选择使水印/非水印分布分离度最大的 $\kappa$。该过程在验证阶段离线完成，不增加在线验证开销。

## 实验与关键发现

### 核心发现：聚类水印的鲁棒性飞跃

实验的核心结论是：**将token级红/绿集合分配升级为聚类级分配，可在不修改生成模型结构、几乎不增加生成开销的前提下，大幅提升水印对常见图像扰动的鲁棒性**。这一结论在LlamaGen（GPT-B 256×256、GPT-L 384×384）和RAR-XL三个自回归图像模型上得到了系统验证。

**Table 1** 汇总了各方法在多种扰动下的AUC和TPR@FPR=1%指标。最关键的对比来自“无聚类基线”（Ours No Clustering）与“训练免费聚类水印”（Ours Clustering, k=64）之间的差距：

- **高斯模糊（Gauss. Blur R3）**：在LlamaGen GPT-B上，无聚类基线的AUC仅0.621，而聚类水印（训练免费）达到0.951，提升**+0.330**；在GPT-L上，聚类水印的AUC更达到0.992。
- **高斯噪声（Gauss. std 0.2）**：在LlamaGen GPT-L上，无聚类基线的AUC骤降至0.055（近乎失效），而聚类水印达到0.996，提升**+0.941**。这一对比直接验证了论文的核心因果机制——图像扰动导致VQ-VAE编码器重建的token与原始生成token差异巨大，token级红/绿分配被打乱；而聚类将语义/几何相似的token绑定在同一集合中，使扰动后重建的token仍有较大概率落入正确的集合。

在更广泛的扰动类型上，**训练免费聚类水印（k=64）** 在LlamaGen GPT-B上对JPEG压缩（JPEG 20）AUC达0.982，对椒盐噪声（Salt&Pepper 0.1）AUC达1.000，对色彩抖动（Color Jitter）AUC达0.985。进一步结合**聚类分类器微调**（Ours Clustering + Cluster Classifier）后，鲁棒性达到最高水平：在GPT-L上对SD1.5再生攻击（Regeneration）的AUC和TPR@FPR=1%均达到1.000。

### 与基线方法的对比

Table 1同时对比了多种后处理水印方法和生成时水印方法：

- **后处理水印**（DWT-DCT-SVD, RivaGAN, TrustMark, SSL）：在强扰动下普遍表现不佳。例如TrustMark（ICCV 2025）在LlamaGen GPT-B的高斯模糊（R3）下AUC仅0.549，远低于聚类水印的0.951。
- **生成时水印IndexMark (+IE)**（Jovanovic et al., NeurIPS 2025）：作为AR图像模型水印的最新工作，其鲁棒性在多数扰动下优于后处理方法，但仍显著弱于ClusterMark。在LlamaGen GPT-B的高斯噪声（std 0.2）下，IndexMark (+IE)的TPR@FPR=1%仅为0.017，而ClusterMark（训练免费）达到0.800，结合聚类分类器后更达到0.990。

**Table 2** 报告了验证速度：ClusterMark的验证仅需**10–25毫秒/图**，与轻量后处理水印（如DWT-DCT-SVD）相当，远快于需要完整生成过程的IndexMark。

### 消融实验：聚簇数量k的权衡

**Figure 3** 和 **Figure 4** 系统消融了聚簇数量k、绿色比例γ和偏置强度δ对鲁棒性与图像质量的影响。

**鲁棒性维度**（Figure 3）：在训练免费设置下，降低k（即更少的聚簇）通常提升鲁棒性。当k=8时，TPR@FPR=1%在多种扰动下达到最高。原因在于：更少的聚簇意味着每个绿色集合覆盖更大的token空间，扰动后token落入正确集合的概率更高。

**图像质量维度**（Figure 4）：然而，当k < 64时，生成质量（FID）显著下降。这是因为过少的聚簇导致绿色token集合过大，生成过程过度偏向某些token，破坏了图像的多样性。**k=64被确定为训练免费设置下的最佳平衡点**：FID与未加水印基线非常接近（LlamaGen GPT-B：6.01 vs 6.12），同时鲁棒性大幅超越无聚类基线。

### 失败模式与前缀调优

**Figure 5** 揭示了一个关键的失败模式：当聚簇数k极低（如k=8）时，未加水印图像中出现了异常高的绿色token比例，导致假阳性率升高。分析表明，这是因为图像中的大面积均匀区域（如天空、背景）会产生重复的token bigram，而这些bigram在某些哈希前缀κ下被伪随机地计为绿色token。

为解决此问题，论文提出了**前缀调优（Prefix Tuning）**：在多个候选κ值中评估未加水印图像的绿色token比例分布，选择使假阳性率最低的κ。Figure 5显示，通过选择表现良好的κ（如κ=42），可以有效抑制均匀区域导致的虚假绿色token，使未加水印图像的绿色比例回归到接近理论值γ=0.25的水平。但该方法采用穷举搜索，需要预先评估多个κ值，并非最优解。

### 生成开销与公平性

生成时水印的开销极小：LlamaGen GPT-B和GPT-L的生成时间分别仅增加**0.06秒**（总3.7秒）和**0.3秒**（总14.3秒）。聚类步骤在生成前一次性完成，不增加每步采样的计算量。验证阶段的token重建使用VQ-VAE编码器，无需完整生成过程，保证了验证的轻量性。

### 需人工核验的要点

- Table 1中RAR-XL模型上的部分后处理基线（如DWT-DCT-SVD）的AUC数值在提供的片段中未完整呈现，建议查阅原文完整表格。
- 前缀调优的具体搜索范围和最优κ选择策略在片段中未详细展开，需参考原文Section 3.4确认细节。
- 聚类分类器微调的训练数据量和扰动增强配置在片段中未明确说明，建议核验Section 3.3及附录。

![[assets/figures/papers/paper_list_l846_https_openaccess_thecvf_com_content_CVPR2026_html_Lukovnikov_ClusterMark/figures/002_Table_1.jpg]]
*Table 1: Main results on a set of challenging perturbations. Detailed perturbation configurations are provided in Appendix A of the Supplementary Material. We report AUC and TPR@FPR=1% across various perturbation and regeneration attacks. For Ours (No Clustering) we set the penalty δ = 5 and the green-token fraction γ = 0.25. For Ours (Clustering) and for our method using the token/cluster classifier we use k = 64 clusters and the same δ and γ. To improve readability, the best and second best entries in each column are highlighted*

![[assets/figures/papers/paper_list_l846_https_openaccess_thecvf_com_content_CVPR2026_html_Lukovnikov_ClusterMark/figures/003_Figure_2.jpg]]
*Figure 2: Examples of images generated by LlamaGen-L (top) and RAR-XL (bottom), shown (column-wise) (1) unwatermarked images, (2) watermarked images without clustering, and (3,4) watermarked images with clustering enabled. Note that while images were generated using the same seed, they differ visually because our watermarking method modifies the generation process rather than applying a post-hoc watermark to given cover images. For more examples, see Section C in the Supplementary Material*

![[assets/figures/papers/paper_list_l846_https_openaccess_thecvf_com_content_CVPR2026_html_Lukovnikov_ClusterMark/figures/004_Table_2.jpg]]
*Table 2: Verification runtime (in milliseconds per image) of our methods against baselines across different models*

![[assets/figures/papers/paper_list_l846_https_openaccess_thecvf_com_content_CVPR2026_html_Lukovnikov_ClusterMark/figures/005_Figure_3.jpg]]
*Figure 3: Empirical TPR@FPR=1% under different perturbations for LlamaGen (GPT-L) and RAR-XL for different numbers of clusters k and penalties δ, with green token fraction γ = 0.25 for the training-free approach. Results are reported over multiple prefixes (8 for RAR-XL and LlamaGen): Lines indicate the average and the shaded area borders the standard deviation*

![[assets/figures/papers/paper_list_l846_https_openaccess_thecvf_com_content_CVPR2026_html_Lukovnikov_ClusterMark/figures/007_Figure_5.jpg]]
*Figure 5: Distribution of green token ratios for watermarked and unwatermarked images across two hashing prefixes κ with a very low number of clusters k = 8. Poorly performing hash prefixes suffer from large uniform regions in unwatermarked images, which produce repetitive token bigrams that are spuriously counted as green*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

自回归（AR）图像生成模型（如LlamaGen、RAR）通过VQ-VAE将图像离散化为token序列，天然适合移植语言模型的水印技术。然而，**直接将LLM的token级KGW水印应用于AR图像模型时，遭遇了根本性瓶颈**：图像扰动（如JPEG压缩、高斯模糊）导致VQ-VAE编码器重建的token序列与原始生成token差异极大，使得基于单个token哈希的红/绿集合分配被打乱，水印检测鲁棒性骤降至接近随机水平。

ClusterMark的核心洞察在于：**将水印的token级随机分组转换为聚类级分组**，利用码本向量的语义/几何相似性将相似token绑定在同一集合中。这样，即使扰动后重建的token发生偏移，仍有较大概率落入同一聚类，从而保持红/绿属性的一致性。

### 2. 方法谱系定位

#### 2.1 后处理水印方法

传统的后处理水印在图像生成后嵌入信号，代表性工作包括：

- **DWT-DCT-SVD**（Al-Haj et al., 2007）：基于频域变换的经典方法，验证速度快但鲁棒性有限。
- **RivaGAN**（Zhang et al., 2019）：基于GAN的鲁棒水印框架。
- **TrustMark**（Bui et al., ICCV 2025）：近期提出的通用水印方案。
- **SSL水印**（Fernandez et al., ICASSP 2022）：基于自监督学习的后处理水印。

这些方法独立于生成过程，可应用于任意图像，但缺乏与生成模型的协同优化。

#### 2.2 生成时水印方法

生成时水印在采样过程中嵌入信号，代表性工作为：

- **IndexMark (+IE)**（Jovanovic et al., NeurIPS 2025）：专门针对AR图像模型的生成时水印，通过索引调制嵌入信息，是ClusterMark最直接的可比工作。
- **KGW token级水印基线**（本文称为Ours No Clustering）：将LLM的KGW水印直接应用于AR图像模型，基于前一个token的哈希进行红/绿集合划分。这是ClusterMark的直接改进对象。

ClusterMark在生成时水印谱系中的定位是：**首次将token级分组提升为聚类级分组**，在不修改生成模型结构的前提下，通过训练免费（training-free）方式显著提升鲁棒性。

#### 2.3 关键差异对比

| 维度 | KGW token级基线 | IndexMark | ClusterMark |
|------|-----------------|-----------|-------------|
| 分组粒度 | 单个token | 索引调制 | 聚类级token组 |
| 哈希输入 | 前一个token $q_{i-1}$ | — | 前一个token的聚类索引 $c(q_{i-1})$ |
| 绿色集合构造 | 从词汇表随机选取 $\gamma$ 比例token | — | 随机选取 $\gamma$ 比例聚类，合并其所有token |
| 扰动鲁棒性来源 | token级一致性 | 索引纠错 | 聚类内token共享红/绿属性 |
| 训练需求 | 无 | 需训练 | 训练免费版本即可，可选微调增强 |

### 3. 适用边界与假设条件

#### 3.1 适用场景

- **类条件AR图像生成模型**：已验证LlamaGen（GPT-B 256×256, GPT-L 384×384）和RAR-XL。
- **常见图像扰动**：JPEG压缩、高斯模糊、高斯噪声、椒盐噪声、颜色抖动等。
- **再生成攻击**：通过Stable Diffusion 1.5的img2img再生成。

#### 3.2 核心假设

1. **码本向量具有语义聚类结构**：k-means聚类能有效捕获token间的相似性，这是方法有效性的前提。
2. **扰动后token偏移在聚类内**：常见扰动导致的token变化倾向于发生在语义/几何相似的token之间，即同一聚类内。
3. **VQ-VAE编码器可用**：验证阶段依赖编码器重建token序列，虽然可选微调分类器可部分缓解编码器误差。

#### 3.3 当前局限

- **极端破坏鲁棒性不足**：强椒盐噪声和严重模糊下仍存在鲁棒性下降。
- **几何攻击未深入处理**：旋转、裁剪等攻击需要额外同步机制（如Sync-Seal），文中未集成。
- **前缀调优策略原始**：采用穷举搜索选择最优$\kappa$值，效率低且需预先评估多个候选。
- **低聚类数陷阱**：当$k < 64$时，图像均匀区域引发token重复，导致未加水印图像的虚假绿色token比例升高（虚假阳性），生成质量（FID）也显著下降。
- **生成范式局限**：仅验证了类条件生成，尚未扩展到文本到图像生成或更高分辨率场景。

### 4. 开放问题

1. **哈希前缀策略优化**：能否设计更优的哈希前缀策略来避免均匀区域导致的虚假绿色token分布，从而无需前缀调优？
2. **文本条件扩展**：方法能否无缝扩展到基于文本条件的AR图像生成模型（如LlamaGen的text-to-image变体）？
3. **对抗安全性**：面对针对性伪造攻击（如针对水印的模型微调或对抗样本攻击）的安全性如何？
4. **自适应聚类数**：聚类数$k$的最优选择是否可以通过自适应方法确定，而非依赖经验搜索？
5. **与后处理水印的融合**：ClusterMark的聚类思想能否与后处理水印方法（如TrustMark）形成互补，构建多层水印方案？

### 5. 知识库定位总结

ClusterMark在AI生成内容水印领域的定位是：**面向AR图像生成模型的生成时鲁棒水印方法**，其核心贡献在于发现了token级水印在图像扰动下的脆弱性根源，并通过码本聚类这一简洁机制实现了训练免费的鲁棒性大幅提升。该方法处于生成时水印与视觉token表征学习的交叉点，为后续研究提供了“分组粒度提升鲁棒性”的范式参考。

## 原文 PDF

![[paperPDFs/CVPR_2026/ClusterMark_Towards_Robust_Watermarking_for_Autoregressive_Image_Generators_with_Visual_Token_Clustering.pdf]]
