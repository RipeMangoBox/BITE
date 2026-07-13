---
title: "Towards Distribution-Agnostic Generalized Category Discovery"
type: paper
paper_level: A
venue: NeurIPS
year: 2023
pdf_ref: paperPDFs/NEURIPS_2023/Towards_Distribution_Agnostic_Generalized_Category_Discovery.pdf
code_link: https://github.com/JianhongBai/BaCon
project_link: https://github.com/JianhongBai/BaCon
aliases:
- SBCACFB
- TDAGCD
tags:
- NEURIPS_2023
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: "自平衡协同建议机制：通过对比学习分支动态估计数据分布来正则化伪标签分支，并通过伪标签分支的去偏采样和soft对比损失将知识回传给对比分支，形成互增强的闭环。"
primary_logic: "利用对比学习分支的无监督聚类能力实时估计类别分布，并以此正则化伪标签分支以避免分类器偏斜；同时伪标签分支的去偏输出与采样策略为对比分支提供更平衡且包含新类别的正样本对，从而在无先验分布的条件下学习到一致、平衡的特征表示。"
claims:
- "BaCon在四个长尾数据集上均大幅超越所有基线方法，尤其在CIFAR-100-LT上新类别准确率提升17.5%（BaCon-S vs 最佳基线）。"
- "现有GCD方法在长尾数据上相比平衡数据性能显著下降，表明数据不平衡是主要瓶颈。"
- "消融实验表明，同时使用对比分支分布估计、去偏采样和soft对比损失三个组件获得最佳性能。"
- "CIFAR-10-LT 上 Overall Accuracy (All) = 91.1"
---

# Towards Distribution-Agnostic Generalized Category Discovery

> [!tip] 核心洞察
> 利用对比学习分支的无监督聚类能力实时估计类别分布，并以此正则化伪标签分支以避免分类器偏斜；同时伪标签分支的去偏输出与采样策略为对比分支提供更平衡且包含新类别的正样本对，从而在无先验分布的条件下学习到一致、平衡的特征表示。

| 字段 | 内容 |
|------|------|
| 中文题名 | 迈向分布无关的广义类别发现 |
| 英文题名 | Towards Distribution-Agnostic Generalized Category Discovery |
| 会议/期刊 | NeurIPS 2023 |
| Links | [paper](https://arxiv.org/abs/2310.01376) · [GitHub](https://github.com/JianhongBai/BaCon) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | Self-Balanced Co-Advice contrastive framework (BaCon) |
| Dataset | CIFAR-10-LT, CIFAR-100-LT, ImageNet-100-LT, Places-LT |

> [!tip] 效果简介
> - CIFAR-10-LT 上，Overall Accuracy (All) 为 91.1，对比 75.1，变化 +16.0。
> - CIFAR-100-LT 上，Overall Accuracy (All) 为 67.2，对比 62.2，变化 +5.0。
> - ImageNet-100-LT 上，Overall Accuracy (All) 为 83.7，对比 78.9，变化 +4.8。

## 概要

**问题瓶颈**：广义类别发现（GCD）旨在从部分标注数据中同时识别已知类别与发现新类别，但现有方法隐含假设数据分布是类别平衡的。当训练集呈现长尾分布时，模型对少数类产生严重偏差，且缺乏对新类别的有效监督信号。实验显示，SimGCD 在平衡 CIFAR-100 上的总体准确率为 71.3%，而在长尾版本上骤降至 52.8%（Table 2），揭示了数据不平衡是 GCD 的核心瓶颈。在分布先验未知的开放环境中，这一冲突进一步加剧。

**核心思路**：本文提出**自平衡协同建议对比框架 BaCon**（Self-Balanced Co-Advice contrastive framework），通过对比学习分支与伪标签分支的闭环互增强机制，在无先验分布条件下实现平衡、一致的特征学习。其关键洞察是：利用对比分支的无监督聚类能力实时估计训练集的类别分布，并以此正则化伪标签分支以避免分类器偏斜；同时，伪标签分支的去偏输出与采样策略为对比分支提供更平衡且包含新类别的正样本对，形成互增强闭环。

**方法定位**：BaCon 属于双分支半监督对比学习框架，其改进体现在三个层面：（1）**分布估计与正则化**——由对比分支 k-means 聚类估计类别分布，通过 KL 散度正则化伪标签分支的平均预测（Eq. 2）；（2）**伪标签去偏与采样**——基于估计分布对 logits 进行后处理调整（Eq. 4），并按类别频率逆比例采样以平衡训练（Eq. 5）；（3）**软对比损失**——引入基于伪标签相似度的软权重，替代传统硬监督对比损失（Eq. 6），使特征相似度与正性评分成比例。

**主要结果**：在四个长尾图像识别数据集（CIFAR-10/100-LT、ImageNet-100-LT、Places-LT）上，BaCon 均大幅超越所有基线方法。以 CIFAR-100-LT 为例，BaCon-S 在新类别准确率上超越最佳基线 17.5%，总体准确率提升 5.0%（Table 3）。消融实验证实，分布正则化、去偏采样和软对比损失三个组件协同作用才能获得最优性能（Table 6）。在不同不平衡率、已知类别数量及标注比例下，BaCon 均保持一致的性能优势（Tables 5, 9, 10）。



### 问题背景：广义类别发现中的数据分布挑战

广义类别发现（Generalized Category Discovery, GCD）旨在从部分标注数据中同时识别已知类别和发现未知类别，是开放世界学习中的核心任务。然而，现有GCD方法普遍假设数据类别分布是均匀的——这一假设在现实场景中几乎从不成立。真实世界的数据天然呈现长尾分布：少数头部类别占据大量样本，而大量尾部类别仅有极少样本。当长尾分布与开放集类别发现相遇时，形成了本工作定义的新任务——**分布无关的广义类别发现**（Distribution-Agnostic Generalized Category Discovery, DA-GCD）。

DA-GCD的训练集包含两部分：已知类别中有少量标注样本和大量未标注样本，新类别则完全以未标注形式存在。关键挑战在于，整个数据集的类别分布是**未知且长尾的**，模型无法获得任何先验分布信息。这一设定与鲁棒半监督学习、分布外检测、传统GCD、长尾半监督学习等相近设置存在本质区别（Table 1），DA-GCD是首个同时要求处理开放集新类别发现和未知长尾分布的任务。

### 现有方法的瓶颈

现有GCD方法在面对长尾数据时暴露出严重缺陷。实验证据表明（Table 2），在CIFAR-100-LT基准上，代表性方法从平衡数据切换到长尾数据后性能急剧下降：**GCD**从68.5%降至62.2%，而基于参数化分类器的**SimGCD**更是从71.3%暴跌至52.8%。这一退化揭示了一个深层瓶颈：

> **长尾数据分布与开放集类别发现之间存在内在冲突。** 模型在缺乏分布先验的条件下，分类器会自然地偏向头部类别，导致对少数类产生严重偏差；同时，新类别由于完全缺乏监督信号，在长尾环境中更容易被淹没在头部类的特征空间中。

具体而言，现有方法面临三重困境：
1. **伪标签偏差**：在半监督学习中，模型倾向于为头部类生成高置信度伪标签，而尾部类和新类别的伪标签质量极低，形成恶性循环。
2. **对比学习失衡**：标准对比损失在长尾数据下，头部类样本作为负样本的概率远高于尾部类，导致特征空间被头部类主导。
3. **无分布先验**：与长尾半监督学习不同，DA-GCD中模型无法获取数据分布信息，传统的重采样或重加权策略因缺乏分布参考而失效。

### 本文动机与核心思路

针对上述瓶颈，本文提出**自平衡协同建议对比框架BaCon**（Self-Balanced Co-Advice contrastive framework）。其核心洞察在于：

> **利用对比学习分支的无监督聚类能力实时估计类别分布，并以此正则化伪标签分支以避免分类器偏斜；同时，伪标签分支的去偏输出与采样策略为对比分支提供更平衡且包含新类别的正样本对，从而在无先验分布的条件下学习到一致、平衡的特征表示。**

BaCon由两个协同工作的分支构成（Figure 2）：
- **对比学习分支**：通过k-means聚类动态估计训练集的类别分布，为伪标签分支提供分布正则化信号。
- **伪标签分支**：基于估计分布进行logits去偏和类别平衡采样，生成高质量伪标签，再通过soft对比损失将知识回传给对比分支。

两个分支形成互增强的闭环：对比分支提供分布估计来校准伪标签分支，伪标签分支提供平衡化监督来优化对比分支。这一设计使得BaCon无需任何先验分布信息，即可在长尾开放环境中同时准确分类已知类并发现新类。



## 核心方法与创新机理

BaCon的核心创新在于构建了一个**自平衡协同建议对比框架**，通过对比学习分支与伪标签分支的双向交互，在无先验分布的条件下解决长尾开放类别发现问题。其关键创新点可归纳为三个相互耦合的**changed slots**：

### 1. 分布估计与正则化：从“无正则化”到“对比分支驱动的KL对齐”

现有GCD方法（如GCD、SimGCD）在训练伪标签分支时，要么不施加任何分布正则化，要么依赖已知的平衡先验，导致分类器在长尾数据上严重偏斜。BaCon的突破在于**利用对比学习分支的无监督聚类能力实时估计训练集的类别分布**，并将其作为正则化信号反馈给伪标签分支。

具体而言，训练过程中定期对对比分支的特征进行k-means聚类，统计各簇的样本占比得到估计分布 $\pi_e$。随后，通过KL散度将伪标签分支在一个batch上的平均预测强制对齐到该估计分布：

$$\mathcal{L}_{reg} = \mathrm{KL}\left[ \frac{1}{|\mathbf{B}|} \sum_{i \in B} \mathrm{softmax}(f_{cls}(\mathbf{x}_i)) \ \big|\big| \ (\mathrm{align}(\boldsymbol{\pi}_e))^p \right]$$

这一设计的因果逻辑在于：对比分支通过无监督聚类天然地对所有类别（包括新类）一视同仁，其估计的分布比伪标签分支自估计更接近真实分布（消融实验证实了这一点，见Table 6a）。该正则化项作为软约束，避免了分类器在头部类上过度自信，为后续去偏和采样提供了准确的分布先验。

### 2. 伪标签处理策略：从“直接使用”到“去偏+类别平衡采样”

传统方法直接使用伪标签分支的原始输出作为监督信号，在长尾场景下会导致两个问题：一是logits本身存在头部类偏差；二是高置信度伪标签集中在头部类，新类别（通常属于尾部）难以获得有效监督。

BaCon的应对策略包含两个递进步骤：

- **Logits去偏**：利用估计分布 $\pi_e$ 对伪标签分支的原始logits进行后处理调整，消除长尾偏差：
  $$\widetilde{p_i} = \mathrm{softmax}(f_{cls}(\mathbf{x}_i) - \kappa \cdot \mathbf{log}\ \boldsymbol{\pi}_e)$$
  该操作等价于将分类器的输出从“判别概率”校正为“类别条件概率”，使得尾部类的预测分数得到提升。

- **类别平衡采样**：根据估计分布为每个类别计算采样率，对当前batch内已出现的类别和未出现的新类别分别采用不同的逆频率加权强度（$\alpha$和$\beta$参数控制）：
  $$\mathrm{SR}^c = \begin{cases}
  (\frac{\pi_e^c}{\min(\pi_e)})^{-\alpha}, & c \in \mathcal{V}_B, \\
  (\frac{\pi_e^c}{\min(\pi_e)})^{-\beta}, & \mathrm{otherwise}
  \end{cases}$$
  这一策略确保每个类别都有机会贡献高置信度伪标签，尤其是为新类别补充了宝贵的监督信号。消融实验（Table 6b）表明，去偏和采样联合使用才能获得最佳性能，单独使用任一组件都会导致已知类或新类准确率的显著下降。

### 3. 对比损失设计：从“硬监督对比”到“软对比损失”

标准监督对比损失将伪标签视为硬标签，构造二元的正/负样本对。然而，在开放类别发现场景下，伪标签本身存在噪声，硬标签方式会放大错误伪标签的负面影响。

BaCon引入了**基于伪标签相似度的软对比损失**，将伪标签分支输出的概率分布转化为样本对之间的“正性评分” $w_{ij}$：

$$w_{ij} = \mathrm{Sim}(\widetilde{p}_i, \widetilde{p}_j)$$

该评分替代了传统对比损失中二元的正/负指示函数，使得损失函数变为：

$$\mathcal{L}_{\mathrm{CL}}^{soft}(\mathcal{D}) = \frac{1}{|\mathcal{D}|} \sum_{i \in \mathcal{D}} \left[ \frac{1}{\sum_{j \in A(i)} w_{ij}} \sum_{j \in A(i)} - w_{ij} \cdot \log \frac{\exp(z_i \cdot z_j / \tau)}{\sum_{a \in A(i)} \exp(z_i \cdot z_a / \tau)} \right]$$

这一设计的深层洞察在于：**特征空间的相似度应与伪标签空间的正性程度成比例**。即使两个样本不属于同一硬伪标签，只要它们的预测分布高度相似，也应被鼓励在特征空间中靠近。这种“软”处理方式既传递了伪标签分支的分类知识，又保留了对伪标签噪声的容忍度。消融实验（Table 6c）证实，软对比损失相比硬监督对比损失在新类别准确率上提升显著，因为它避免了将不确定样本强行归入错误的正样本对。

### 创新闭环：双向协同建议机制

上述三个changed slots并非孤立存在，而是构成了一个**双向协同的闭环**：

- **对比分支 → 伪标签分支**：通过分布估计正则化和去偏所需的分布先验，约束分类器避免偏斜；
- **伪标签分支 → 对比分支**：通过去偏输出和平衡采样，为对比分支提供更均衡且包含新类别的正样本对，再通过软对比损失传递分类知识。

这种“自平衡协同建议”机制使得两个分支在训练中相互增强，无需任何先验分布假设即可学习到一致、平衡的特征表示。在CIFAR-100-LT上，BaCon-S在新类别准确率上超越最佳基线17.5%，验证了这一创新闭环的有效性。



BaCon 采用双分支协同结构，由一个**对比学习分支 (contrastive-learning branch)** 和一个**伪标签分支 (pseudo-labeling branch)** 组成，两者共享并冻结 ViT-B/16 骨干网络（仅微调最后一个 block），通过交互式监督共同应对分布无关的广义类别发现问题。

**核心交互闭环**：对比学习分支利用其无监督聚类能力，定期对整个训练集的特征进行 k-means 聚类以**估计类别分布**，该分布估计一方面通过 KL 散度正则化伪标签分支的平均预测输出，另一方面用于对伪标签分支的 logits 进行**去偏调整**。伪标签分支则根据估计分布进行**类别平衡采样**，筛选高置信度伪标签，并将这些包含新类别监督信息的伪标签以**软对比损失 (soft contrastive loss)** 的形式回传给对比学习分支，从而形成互增强的闭环。

**数据流**：输入图像经过共享骨干提取特征后，分别送入两个分支。对比学习分支输出归一化嵌入 $z$，用于计算无监督对比损失、有监督对比损失（基于有标签数据）以及软对比损失（基于有标签数据和伪标签数据）；伪标签分支输出类别概率，计算有监督交叉熵损失、无监督熵正则化损失以及分布正则化损失。训练时两分支联合优化，推理时仅使用对比学习分支的骨干特征进行 k-means 聚类获得最终预测。

### 补充图表

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/005_Figure_2.jpg]]
*Figure 2: Overview of the self-balanced co-advice contrastive framework (BaCon)*



### 整体框架

BaCon 采用双分支结构（Figure 2），共享一个冻结的 ViT-B/16 骨干（仅微调最后一个 block）。两个分支分别为：

- **对比学习分支** $f_{con}$：负责学习特征表示，并用于分布估计和训练 soft 对比损失。
- **伪标签分支** $f_{cls}$：输出分类概率，生成伪标签。

两个分支通过“自平衡协同建议”机制相互增强：对比分支提供分布估计来正则化伪标签分支，伪标签分支通过去偏采样和 soft 对比损失将知识回传给对比分支。

### 分布估计与正则化

**核心思路**：利用对比学习分支的无监督聚类能力实时估计训练集的类别分布，并以此正则化伪标签分支的平均预测，防止分类器向头部类偏斜。

具体地，定期对对比分支的特征进行 k-means 聚类，统计各类别样本比例得到估计分布 $\boldsymbol{\pi}_e$。然后通过 KL 散度将伪标签分支在一个 batch 上的平均预测拉向该估计分布：

$$\mathcal{L}_{reg} = \mathrm{KL}\left[ \frac{1}{|\boldsymbol{B}|} \sum_{i \in B} \mathrm{softmax}(f_{cls}(\pmb{x}_i)) \ \big|\big| \ (\mathrm{align}(\pmb{\pi}_e))^{p} \right] \tag{2}$$

其中 $\mathrm{align}(\pmb{\pi}_e)$ 将估计分布与分类器输出维度对齐（处理新旧类别对应关系），$p$ 为平滑指数。

伪标签分支的总损失为：

$$\mathcal{L}_{cls} = \mathcal{L}_{s} + \eta_{1} \mathcal{L}_{u} + \eta_{2} \mathcal{L}_{reg} \tag{3}$$

其中 $\mathcal{L}_{s}$ 为有标签数据的监督交叉熵损失，$\mathcal{L}_{u}$ 为无标签数据的半监督损失，$\eta_{1}, \eta_{2}$ 为平衡系数。

### 去偏与平衡采样

**核心思路**：利用估计分布对伪标签 logits 进行后处理去偏，并按类别频率的逆比例进行采样，以平衡训练并补充新类别的监督信号。

**Logits 去偏**：给定估计分布 $\boldsymbol{\pi}_e$，对伪标签分支的输出 logits 进行调整：

$$\widetilde{p_i} = \mathrm{softmax}(f_{cls}(\pmb{x}_i) - \pmb{k} \cdot \mathbf{log} \pmb{\pi}_e) \tag{4}$$

其中 $\pmb{k}$ 为缩放因子。该操作基于长尾识别中的 post-hoc logits adjustment 思想，通过减去对数先验来消除分类器对头部类的偏向。

**类别级采样率**：根据估计分布为每个类别设定采样率，频率越低的类别采样率越高：

$$\mathrm{SR}^{c} = \begin{cases}
\left( \frac{\pi_e^{c}}{\min(\pi_e)} \right)^{-\alpha}, & c \in \mathcal{V}_B, \\
\left( \frac{\pi_e^{c}}{\min(\pi_e)} \right)^{-\beta}, & \text{otherwise}
\end{cases} \tag{5}$$

其中 $\mathcal{V}_B$ 为当前 batch 内出现的类别，$\alpha$ 和 $\beta$ 分别控制 batch 内和 batch 外类别的采样强度。当 $\beta=1$ 时，采样率与类别样本数成反比。采样后仅保留高置信度的伪标签参与后续训练。

### Soft 对比损失

**核心思路**：将伪标签分支输出的类别概率相似度作为正对软权重，引导对比学习分支的特征空间与分类语义对齐，避免硬伪标签带来的噪声放大。

定义样本对 $(i, j)$ 的正性评分 $w_{ij}$ 为二者去偏伪标签概率的相似度：

$$w_{ij} = \mathrm{Sim}(\widetilde{p}_i, \widetilde{p}_j)$$

将其融入对比损失，得到 soft 对比损失：

$$\mathcal{L}_{\mathrm{CL}}^{soft}(\mathcal{D}) = \frac{1}{|\mathcal{D}|} \sum_{i \in \mathcal{D}} \left[ \frac{1}{\sum_{j \in A(i)} w_{ij}} \sum_{j \in A(i)} - w_{ij} \cdot \log \frac{\exp(z_i \cdot z_j / \tau)}{\sum_{a \in A(i)} \exp(z_i \cdot z_a / \tau)} \right] \tag{6}$$

其中 $z_i$ 为样本 $i$ 的归一化特征嵌入，$A(i)$ 为 anchor 集，$\tau$ 为温度参数。该损失鼓励特征空间相似度与伪标签语义相似度成比例，使得分类信息能够以软约束的形式传递到对比分支。

### 对比分支总损失

对比学习分支的最终训练目标结合了三部分：

$$\mathcal{L}_{con} = \mathcal{L}_{\mathrm{CL}}^{u}(\mathcal{D}) + \gamma_{1} \mathcal{L}_{\mathrm{CL}}^{s}(\mathcal{D}_l) + \gamma_{2} \mathcal{L}_{\mathrm{CL}}^{soft}(\mathcal{D}_l \cup M(\mathcal{D}_u)) \tag{7}$$

- $\mathcal{L}_{\mathrm{CL}}^{u}(\mathcal{D})$：对整个训练集的无监督对比损失（Eq. 1），正对来自数据增强。
- $\mathcal{L}_{\mathrm{CL}}^{s}(\mathcal{D}_l)$：对有标签数据 $\mathcal{D}_l$ 的监督对比损失，正对来自相同 ground-truth 标签。
- $\mathcal{L}_{\mathrm{CL}}^{soft}$：对有标签数据与高置信度伪标签数据并集的 soft 对比损失，$M(\mathcal{D}_u)$ 为经过采样筛选的无标签数据子集。

$\gamma_{1}$ 和 $\gamma_{2}$ 为平衡系数。该设计使得对比分支既能从少量有标签数据中获取可靠监督，又能通过 soft 损失从伪标签中吸收新类别信息，同时保持无监督聚类能力以支撑分布估计。

### 推理阶段

测试时仅使用对比学习分支的骨干网络提取特征，通过 k-means 聚类获得最终预测。伪标签分支在训练完成后被丢弃。



## 实验与关键发现

### 实验设置

#### 数据集与协议

本工作构建了四个长尾图像识别基准：**CIFAR-10-LT**、**CIFAR-100-LT**、**ImageNet-100-LT** 和 **Places-LT**。所有数据集均按指数衰减长尾分布采样，默认不平衡率 $\rho=100$（即最多数类样本量是最少数类的100倍）。训练集中，50%的类别作为已知类（其中10%的样本有标签），其余50%作为新类（完全无标签）。数据集详细统计见 **Table 7**，默认训练集设置见 **Table 8**。

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/014_Table_7.jpg]]
*Table 7: Statistics of datasets*

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/015_Table_8.jpg]]
*Table 8: The default setting of DA-GCD’s training set*

#### 骨干网络与训练细节

所有方法均使用 **DINO预训练的ViT-B/16** 作为共享骨干，仅微调最后一个Transformer块。训练采用200个epoch的余弦退火学习率调度，批量大小为128。BaCon的对比学习分支和伪标签分支共享同一骨干，但各自拥有独立的投影头/分类头。对比分支的分布估计通过每 $r$ 个epoch对整个训练集执行一次k-means聚类完成。

#### 评估指标

报告三个核心指标：已知类准确率（Old）、新类别准确率（New）和总体准确率（All）。此外，通过各类准确率的标准差（Std↓）衡量类别平衡性。

#### 基线方法

比较方法涵盖三类：**广义类别发现方法**（GCD、SimGCD）、**开放世界方法**（ORCA、OpenCon）和**鲁棒半监督学习方法**（TRSSL、ABC、DARP）。所有基线均使用相同的预训练骨干和训练协议重新运行，确保公平比较。

---

### 主要结果

#### 长尾数据对现有GCD方法的冲击

**Table 2** 展示了现有方法在CIFAR-100-LT平衡版本与长尾版本上的性能对比。GCD从68.5%骤降至62.2%，SimGCD更是从71.3%暴跌至52.8%，同时类别平衡性标准差从11.1飙升至31.9。这清晰地揭示了**长尾分布是现有GCD方法的核心瓶颈**——参数化分类器（SimGCD）在无分布先验时严重偏向多数类，而纯对比方法（GCD）虽有更好的平衡性但整体判别力不足。

#### 跨数据集综合性能

**Table 3** 汇总了四个长尾基准上的主要结果。BaCon在所有数据集上均取得最优总体准确率：

| 数据集 | 最佳基线 | BaCon | 提升幅度 |
|--------|---------|-------|---------|
| CIFAR-10-LT | 75.1 | **91.1** | +16.0 |
| CIFAR-100-LT | 62.2 | **67.2** | +5.0 |
| ImageNet-100-LT | 78.9 | **83.7** | +4.8 |
| Places-LT | 26.2 | **29.9** | +3.7 |

尤为突出的是，**BaCon在新类别上的表现远超所有基线**：在CIFAR-100-LT上，BaCon-S的新类别准确率达到62.9%，比最佳基线（GCD的45.4%）高出17.5个百分点。这表明自平衡协同机制有效解决了新类别在长尾分布中被淹没的问题。

#### 细粒度分析与平衡性

**Table 4** 报告了CIFAR-100-LT上按已知/新类别划分的准确率及平衡性。BaCon不仅在新类别上大幅领先，其类别准确率标准差（Std）也显著低于所有基线，说明模型对少数类和新类别均保持了均衡的识别能力。

#### 不同不平衡率下的鲁棒性

**Table 5** 展示了在CIFAR-100-LT上改变不平衡率 $\rho$ 的结果。随着 $\rho$ 从10增加到200（极端长尾），所有方法性能均下降，但BaCon的衰减幅度最小：在 $\rho=200$ 时，BaCon仍保持62.1%的总体准确率，而最佳基线GCD降至57.1%。这验证了分布估计正则化在不同长尾程度下的稳定收益。

---

### 消融实验

**Table 6** 系统拆解了BaCon各组件的作用，默认设置以橙色标注。

#### 正则化项设计

**Table 6(a)** 对比了三种正则化策略：
- **无正则化**：新类别准确率骤降，说明缺乏分布约束时分类器严重偏斜；
- **平衡先验正则化**（假设均匀分布）：比无正则化有改善，但错误地假设了分布形态；
- **伪标签分支自估计正则化**：利用分类器自身预测估计分布，存在“自我强化偏差”；
- **对比分支k-means估计正则化（默认）**：取得最佳性能，验证了**无监督聚类提供的分布估计比分类器自估计更可靠**。

#### 去偏与采样策略

**Table 6(b)** 分析了logits去偏（Eq.4）和类别平衡采样（Eq.5）的效果。单独使用去偏或采样均带来提升，但**两者联合使用产生协同效应**——去偏修正了预测概率的分布偏移，而采样确保高置信度伪标签覆盖少数类和新类别，两者互补使得伪标签质量和覆盖率同时提升。

#### 损失函数设计

**Table 6(c)** 对比了三种对比损失：
- **无监督对比损失**：仅使用无监督对比，缺乏类别监督信号；
- **硬监督对比损失**：将伪标签作为硬标签构造正负对，噪声伪标签导致错误传播；
- **Soft对比损失（默认）**：基于伪标签相似度加权正负对，新类别准确率显著高于硬监督版本。软权重机制使模型能够利用伪标签中的不确定性信息，而非强制二值化判断。

#### 分布重估计间隔

**Table 6(d)** 显示，每5个epoch重新估计一次分布（默认）取得最佳效果。间隔过短（1 epoch）导致估计不稳定，间隔过长（10+ epochs）则无法及时跟踪训练过程中的分布变化。

#### 相似度函数选择

**Table 6(e)** 比较了余弦相似度和点积相似度用于计算soft对比损失权重。余弦相似度略优于点积，因其对特征尺度不敏感，更适合衡量概率分布间的语义一致性。

---

### 可视化分析

**Figure 3** 展示了CIFAR-10测试集特征的t-SNE可视化。相比SimGCD和GCD，BaCon的特征空间中：
- 同类样本更紧凑，类间边界更清晰；
- 少数类和新类别未出现被多数类“吞并”的现象；
- 整体聚类结构均匀，验证了自平衡机制有效防止了特征空间的类别偏斜。

---

### 失败模式与局限性

1. **类别数依赖**：BaCon需要预知总类别数 $K$。虽然论文指出可通过现有方法估计，但在类别数完全未知的开放场景下，分布估计和伪标签分配均会受到影响。**Table 9** 显示，当已知类数量偏离真实值时，性能有所下降，但BaCon仍优于基线。

2. **标注比例敏感性**：**Table 10** 表明，当标注比例 $r_l$ 极低（如1%）时，BaCon的优势缩小。这是因为分布估计和伪标签质量均依赖于少量有标签样本的初始引导。

3. **标注/未标注数据分布不一致**：**Table 11** 展示了当已标注数据不平衡率 $\rho_l=100$ 而未见数据不平衡率 $\rho_u$ 变化时的结果。当两者分布差异较大时，性能有所下降，说明分布估计模块对分布偏移有一定敏感性。

4. **计算开销**：定期对整个训练集执行k-means聚类的计算成本随数据规模线性增长，在超大规模数据集上可能成为瓶颈。

5. **任务范围限制**：当前方法仅针对图像分类设计，尚未扩展到目标检测、实例分割等更复杂的视觉任务。

### 补充图表

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/008_Figure_3.jpg]]
*Figure 3: t-SNE visualization on the test set of CIFAR-10*

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/011_Table.jpg]]
*Table: (a) Regularization Term. (b) Debiasing and Sampling. (d) Re-estimate Interval r. (e) Similarity Function*

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/004_Table_1.jpg]]
*Table 1: Comparison of DA-GCD with other similar settings*

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/006_Table_2.jpg]]
*Table 2: Test accuracy (%) and balancedness (Std↓) of existing methods on CIFAR-100-LT*

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/007_Table_3.jpg]]
*Table 3: Test accuracy (%) on four generic long-tailed image recognition datasets. (bold: best performance among all methods, underline: best performance among the baseline methods.)*

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/009_Table_4.jpg]]
*Table 4: Test accuracy (%) and balancedness (Std↓) on CIFAR-100-LT*

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/010_Table_5.jpg]]
*Table 5: Test accuracy (%) on CIFAR-100-LT with different imbalance ratio ρ*

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/012_Table.jpg]]
*Table: (c) Loss Design*

![[assets/figures/papers/paper_list_l1500_https_arxiv_org_abs_2310_01376/figures/013_Table_6.jpg]]
*Table 6: BaCon ablation experiments. For each ablation, we report test accuracy (%) of known, novel and all classes, denote as ‘Old’, ‘New’, and ‘All’. Our default settings are marked in orange*



## 定位与知识库关联

### 1. 任务定义与相关设置的边界

本文提出的分布无关广义类别发现（DA-GCD）处于开放世界识别与长尾学习的交叉地带。Table 1 系统比较了 DA-GCD 与 Robust SSL、OOD Detection、GCD、LT-SSL、OLTR 等相近设置在数据分布先验、开放集类别、标注比例等维度的差异。DA-GCD 的核心约束是：训练集类别服从未知的长尾分布，同时包含已知类（有少量标注）和新类（完全无标注），要求模型在半监督条件下同时准确分类两类样本。

与标准 GCD 相比，DA-GCD 取消了“训练数据类别平衡”的隐含假设。Table 2 的实证证据表明，这一假设的打破对现有方法是致命的：在 CIFAR-100-LT 上，GCD 从平衡数据的 68.5% 降至长尾数据的 62.2%，SimGCD 更是从 71.3% 骤降至 52.8%。这种性能崩塌揭示了现有方法的核心瓶颈——伪标签分支的分类器在长尾分布下严重偏斜，而对比学习分支缺乏对少数类的有效正样本对监督。

### 2. 与基线方法的关系与改进

BaCon 继承了两条技术路线，并对其关键组件进行了针对性改造：

**对比学习路线（GCD、ORCA、OpenCon）**：这些方法依赖无监督或半监督对比损失学习特征表示，但均未显式建模类别分布。GCD 使用标准监督对比损失处理有标注数据，在长尾场景下少数类正样本对稀缺，导致特征空间塌缩。BaCon 保留了对比学习分支作为特征学习的主干，但引入两个关键改造：（1）由对比分支的 k-means 聚类定期估计全局类别分布，用于正则化伪标签分支（Eq. 2）；（2）设计基于伪标签相似度的 soft 对比损失（Eq. 6），以软权重替代硬正负对划分，使少数类样本也能获得非零的正性评分信号。

**参数化分类器路线（SimGCD）**：SimGCD 使用线性分类器输出伪标签，在平衡数据上表现优异，但其分类器在长尾分布下严重偏向头类。BaCon 同样采用伪标签分支，但通过对比分支估计的分布对分类器预测进行后处理去偏（Eq. 4），并按类别频率逆比例调整采样率（Eq. 5），确保少数类和新类的高置信度伪标签能被有效选中参与训练。

其他基线方法提供了组件级参考：TRSSL 和 ABC 针对不平衡半监督学习设计了辅助平衡分类器和去偏策略，但假设类别分布已知或可估计自标注数据，在 DA-GCD 的无分布先验设定下不适用。DARP 通过分布对齐修正伪标签，但其分布估计依赖伪标签分支自身，在初期伪标签质量差时形成错误的正反馈循环。BaCon 的关键差异在于将分布估计与伪标签生成解耦到两个分支，形成“估计—正则化—去偏—回传”的闭环，避免了自举偏差。

### 3. 核心机制与适用边界

BaCon 的自平衡协同建议机制可分解为三个相互增强的组件：

1. **分布估计与正则化**：对比分支 k-means 聚类 → 估计类别分布 $\pi_e$ → KL 散度正则化伪标签分支的平均预测（Eq. 2）。该机制的有效性依赖于对比分支特征的质量，因此需要足够的无监督预训练（本文使用 DINO 预训练 ViT-B/16）作为初始化。

2. **去偏与平衡采样**：根据 $\pi_e$ 对伪标签 logits 进行后处理调整（Eq. 4），并按类别频率的逆比例进行采样（Eq. 5），其中 $\alpha$ 和 $\beta$ 分别控制当前批次内和批次外类别的采样强度。这一设计使模型能够在不引入额外标注的前提下，平衡头类和尾类、已知类和新类的训练信号。

3. **Soft 对比损失**：以伪标签相似度 $w_{ij} = \text{Sim}(\widetilde{p}_i, \widetilde{p}_j)$ 作为对比损失的软权重（Eq. 6），使特征相似度与类别归属的置信度成比例。相比硬监督对比损失，soft 版本对伪标签噪声更鲁棒，且能为“不确定”的样本对保留非零梯度。

**适用边界**：
- 当前方法仅针对图像分类任务设计，Pipeline 中的 k-means 聚类和分布估计模块直接依赖特征空间的欧氏距离结构，尚未扩展到目标检测、实例分割等需要空间定位的任务。
- 方法依赖总类别数 $K$ 的先验（用于 k-means 聚类和分类器维度设置）。Table 9 表明，当已知类数量变化时性能保持稳定，但完全未知 $K$ 的场景需要额外的类别数估计模块。
- 定期对整个训练集进行 k-means 聚类的计算开销随数据集规模线性增长，在超大规模数据集（如完整 ImageNet-21K）上可能成为瓶颈。

### 4. 局限与开放问题

**已识别的局限**：
1. **任务范围受限**：当前仅验证于图像分类，未涉及目标检测、实例分割等更复杂的视觉任务。
2. **类别数先验依赖**：需要预知总类别数 $K$，在完全开放场景下需配合类别数估计算法。
3. **计算开销**：k-means 聚类的周期性全量计算限制了在超大规模数据集上的可扩展性。
4. **极低标注比例**：Table 10 显示，当标注比例 $r_l$ 极低时，所有方法性能均显著下降，BaCon 虽保持优势但绝对准确率仍有限。

**开放问题**：
1. 如何将自平衡协同建议框架扩展到目标检测和实例分割？可能的路径包括将分布估计模块替换为实例级聚类，以及设计空间敏感的 soft 对比损失。
2. 能否通过近似方法（如 mini-batch k-means、在线聚类）加速分布估计以降低计算开销？
3. 在无法提供总类别数先验的条件下，BaCon 能否自适应估计类别数量？这需要聚类算法具备模型选择能力。
4. 如何进一步提升在极低标注比例下的性能？可能的改进方向包括引入主动学习策略选择最有信息量的标注样本，或利用预训练视觉-语言模型的零样本能力提供弱监督。



## 原文 PDF

![[paperPDFs/NEURIPS_2023/Towards_Distribution_Agnostic_Generalized_Category_Discovery.pdf]]
