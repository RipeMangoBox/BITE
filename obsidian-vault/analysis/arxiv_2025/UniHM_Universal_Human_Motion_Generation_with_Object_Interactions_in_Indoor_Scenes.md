---
title: "UniHM: Universal Human Motion Generation with Object Interactions in Indoor Scenes"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/UniHM_Universal_Human_Motion_Generation_with_Object_Interactions_in_Indoor_Scenes.pdf
project_link: null
code_link: null
aliases:
- UniHM
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过引入混合运动表示（连续6DoF与离散局部标记结合）并采用免查找量化VAE（LFQ-VAE），从标记化层面消除码本限制并扩大词汇量，同时利用扩散模型在连续空间中预测稀疏航点，有效协调全局运动规划和局部细节生成。
primary_logic: 将运动生成分解为稀疏航点规划（通过扩散模型处理连续6DoF）和密集标记生成（通过LFQ-VAE处理局部运动），并融合场景多模态信息，使得模型在保持场景约束的同时生成更真实、多样且物理合理的运动。
claims:
- LFQ-VAE在生成FID上随词汇量增大而持续优于VQ-VAE，而VQ-VAE的gFID反而上升（恶化）。
- 引入航点引导在场景感知Text-to-Motion中将碰撞分数从0.017降至0.010，在Text-to-HOI中将FID从1.232降至0.826，接触从0.855提升至0.945。
- 去除航点生成模块导致场景感知Text-to-HOI的碰撞分数从0.021恶化至0.120，接触分数从0.855降至0.630。
- OMOMO (Text-to-HOI) 上 FID↓ = 0.582
---

# UniHM: Universal Human Motion Generation with Object Interactions in Indoor Scenes

> [!tip] 核心洞察
> 将运动生成分解为稀疏航点规划（通过扩散模型处理连续6DoF）和密集标记生成（通过LFQ-VAE处理局部运动），并融合场景多模态信息，使得模型在保持场景约束的同时生成更真实、多样且物理合理的运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniHM：面向室内场景物体交互的通用人体运动生成 |
| 英文题名 | UniHM: Universal Human Motion Generation with Object Interactions in Indoor Scenes |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2406.11838) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | UniHM |
| Dataset | OMOMO, Lingo, HumanML3D |

> [!tip] 效果简介
> - OMOMO (Text-to-HOI) 上，FID↓ 0.582 vs CHOIS (更佳，具体数值未报告) (低于CHOIS（更优）)；Contact↑ 0.847 vs CHOIS (具体数值未报告) (与CHOIS可比)。
> - Lingo (Text-to-Motion in Scene) 上，Collision_s↓ 0.017 vs ARDHOI (具体数值未报告) (显著降低碰撞)。
> - HumanML3D (Text-to-Motion) 上，R-Precision (Top-1) 优于T2M-GPT vs T2M-GPT (更高)。

## 概要

**UniHM** 面向室内场景中文本驱动的人体运动生成与物体交互（HOI）任务，提出一种通用框架。其核心动机在于解决现有运动生成方法的两难困境：**纯连续表示**虽能保留精确的6DoF轨迹信息，却难以进行高效的概率建模；**离散标记化**（如VQ-VAE）虽便于自回归生成，却在量化过程中损失连续的全局运动信息，且高频微运动在有限码本中产生大量冗余表示，导致码本利用率低下与生成质量退化。

针对上述瓶颈，UniHM做出了两项关键设计：

1. **混合运动表示**：将运动分解为**稀疏的连续6DoF航点**（表达全局轨迹与物体交互位置）和**密集的离散局部运动标记**（表达关节级细节），从表示层面解耦全局规划与局部生成。
2. **免查找量化VAE（LFQ-VAE）**：取代传统VQ-VAE的有限码本机制，采用二进制潜在空间直接索引，消除了码本容量限制，并在词汇量增大时持续提升生成FID（gFID），而VQ-VAE的gFID反而恶化（Fig. 5）。

在生成流程上，UniHM先将场景体素、物体点云与文本条件融合为上下文运动嵌入（CME），再由一个轻量MLP扩散去噪器从噪声中预测干净的6DoF航点，最后通过自回归Transformer基于航点生成完整的局部运动序列。这一层次化设计使得模型在保持场景空间约束的同时，生成真实、多样且物理合理的人-物交互运动。

**主要实验结果**：
- 在**OMOMO**（Text-to-HOI）基准上，UniHM的FID降至0.582，优于CHOIS（Li et al., arXiv 2023）；接触分数（Contact）达0.847，与CHOIS可比（TABLE I）。
- 在**Lingo**（场景感知Text-to-Motion）上，碰撞分数（Collision_s）降至0.017，显著低于ARDHOI（Geng et al., arXiv 2025）（TABLE II）。
- 在**HumanML3D**（通用Text-to-Motion）上，UniHM的R-Precision（Top-1）优于T2M-GPT（Zhang et al., CVPR 2023），但FID仍不及后者，提示混合表示可能引入额外复杂性或训练尚不充分。

消融实验证实了航点模块的决定性作用：去除航点生成后，场景感知Text-to-HOI的碰撞分数从0.021骤升至0.120，接触分数从0.855降至0.630（TABLE III）。引入航点引导还将场景感知Text-to-Motion的碰撞分数从0.017进一步降至0.010（TABLE IV）。

**方法定位**：UniHM属于“离散标记+连续航点”混合范式，其LFQ-VAE从标记化层面突破了VQ-VAE的码本瓶颈，扩散航点去噪器则在连续空间中实现了稀疏全局规划。该方法在场景约束下的运动真实性与物理合理性上展现出优势，但在通用运动生成的FID指标上仍有提升空间，且对全新场景布局的泛化能力及计算效率尚未充分验证。

生成符合场景约束、物理合理且自然的人体运动，是计算机视觉与图形学中长期存在的挑战。该任务的核心在于同时满足**全局轨迹规划**与**局部运动细节**的双重要求：人体不仅需要在室内场景中沿合理路径移动，还需与物体（如椅子、桌子）产生精确的交互接触，同时保持运动本身的流畅性与多样性。

现有方法在处理场景感知运动生成时，面临一个根本性的瓶颈：**运动标记化过程中的信息损失**。当前主流方案通常依赖 VQ-VAE 将连续运动序列压缩为离散标记，但这一过程不可避免地丢失了连续的 6 自由度（6DoF）运动信息，使得模型难以同时表达全局轨迹与局部细节。此外，高频微运动（如手指颤动、细微重心调整）在量化空间中会生成大量冗余的离散表示，导致码本利用率低下，进而损害生成质量与多样性。

从方法层面看，现有工作存在以下结构性缺口：
- **纯离散标记方法**（如 T2M-GPT，Zhang et al., CVPR 2023）在通用文本到运动生成上表现优异，但缺乏对场景几何约束的显式建模，难以处理物体交互任务。
- **场景感知方法**（如 CHOIS，Li et al., arXiv 2023；ARDHOI，Geng et al., arXiv 2025）虽然引入了场景条件，但其运动表示仍受限于 VQ-VAE 的离散码本，在全局轨迹精度与局部运动保真度之间存在固有权衡。
- **航点规划与运动生成的解耦不足**：多数方法要么完全忽略稀疏航点的引导作用，要么将航点预测视为确定性回归问题，缺乏对运动不确定性的建模。

UniHM 的提出正是为了填补上述缺口。其核心动机在于：**通过混合运动表示与免查找量化机制，从标记化层面消除码本容量限制，同时利用扩散模型在连续空间中建模航点分布，实现全局规划与局部生成的有效协同**。这一设计使得模型能够在保持场景约束的前提下，生成更真实、多样且物理合理的人-物交互运动。

## 核心方法与创新机理

UniHM 的核心创新在于从运动表示的根本层面入手，通过“混合表示 + 免查找量化 + 层次化航点规划”三重设计，解决了现有场景感知运动生成中全局轨迹与局部细节难以兼顾、码本利用不充分的核心瓶颈。

### 1. 混合运动表示：连续 6DoF 与离散局部标记的协同

传统方法要么采用纯离散标记（如 **T2M-GPT**，Zhang et al., CVPR 2023），导致连续 6DoF 运动信息在量化过程中损失；要么使用纯连续参数，难以高效建模运动的离散模式。UniHM 提出**混合运动表示**，将人体与物体的运动分解为两个互补的层次：

- **连续 6DoF 航点**：以 1 秒为窗口，表达人体和物体的全局位姿轨迹（位置与朝向），保留连续空间的精确性。
- **离散局部运动标记**：通过 LFQ-VAE 对局部运动细节进行压缩编码，捕捉运动的离散模式。

这种分解使得全局运动规划与局部细节生成可以在各自的优势空间中独立优化，再通过生成管线进行融合。消融实验证实了这一设计的必要性：**去除航点生成模块后，场景感知 Text-to-HOI 的碰撞分数从 0.021 骤升至 0.120，接触分数从 0.855 降至 0.630**（TABLE III），表明混合表示中的连续航点对维持场景约束和交互精度至关重要。

### 2. 免查找量化 VAE（LFQ-VAE）：突破码本瓶颈

传统 VQ-VAE 依赖有限的学习码本进行向量量化，在高频微运动的量化空间中产生大量冗余表示，导致码本利用不充分，生成质量随码本增大反而恶化。UniHM 引入 **Look-Up Free Quantization VAE（LFQ-VAE）**，将量化过程改为二进制潜在空间中的免查找索引：

$$\mathrm{Index}(\mathbf{z}) = \sum_{i=1}^{\log_2 K} 2^{i-1} \mathbb{1}\{z_i > 0\}$$

这一设计从结构上消除了对显式码本的依赖，词汇量可随潜在维度指数增长而不受码本容量限制。实验证据直接支持这一优势：**随着词汇量增大，VQ-VAE 的生成 FID（gFID）反而上升（恶化），而 LFQ-VAE 的 gFID 持续降低（改善）**（Fig. 5）。这证明 LFQ-VAE 从根本上解决了传统量化方法在高维运动空间中的码本崩溃问题。

### 3. 层次化扩散航点生成：从噪声中精炼全局轨迹

不同于直接回归航点的方案，UniHM 采用**基于扩散模型的层次化航点生成**：先估计粗粒度的全局航点，再将其精炼为细粒度的局部位置和朝向。扩散去噪器（轻量 MLP）从噪声中直接预测干净的 6DoF 航点 $w_0$：

$$\mathcal{L}_{\mathrm{6DoF}} = \mathbb{E}_{(w_{0}, \epsilon) \sim q} \left[ | f_{\theta}(w_{t}, t) - w_{0} |^{2} \right]$$

这一机制在场景约束下展现出显著的协调能力：**引入航点引导后，场景感知 Text-to-Motion 的碰撞分数从 0.017 降至 0.010，Text-to-HOI 的 FID 从 1.232 降至 0.826，接触分数从 0.855 提升至 0.945**（TABLE IV）。扩散过程的随机采样特性使航点生成具备多样性，而层次化精炼确保了全局规划的物理合理性。

### 4. 接触几何损失：显式约束人-物交互

在生成损失层面，UniHM 在交叉熵损失和 6DoF 去噪损失之外，引入**接触几何损失**，显式约束预测的人-物空间关系：

$$\mathcal{L}_{\mathrm{contact}} = \frac{1}{mn} \sum_{i=1}^{n} \sum_{j=1}^{m} || \mathrm{dist}(\mathcal{O}_i, J_j) - \mathrm{dist}(\hat{O}_i, \hat{J}_j) ||$$

该损失通过计算物体采样点与人体网格预定义关节点之间的成对距离，强制预测的接触模式与真实标注保持一致。这一设计将物理交互约束直接注入训练目标，弥补了传统损失函数对接触精度监督不足的缺陷。

### 创新点总结

| 改变维度 | 基线方案 | UniHM 方案 | 关键证据 |
|---------|---------|-----------|---------|
| 运动标记化 | VQ-VAE（学习码本） | LFQ-VAE（免查找二进制量化） | Fig. 5：gFID 随词汇量增大持续改善 |
| 运动表示 | 纯离散或纯连续 | 混合表示（6DoF 航点 + 离散标记） | TABLE III：去除航点后碰撞分数恶化 5.7 倍 |
| 航点生成 | 无显式航点 / 直接回归 | 扩散模型层次化精炼 | TABLE IV：航点引导使碰撞分数降低 41% |
| 损失函数 | 交叉熵损失 | + 6DoF 去噪损失 + 接触几何损失 | TABLE I/II：整体指标显著优于基线 |

这些创新并非孤立存在，而是形成了一条因果链：LFQ-VAE 提供高质量的离散运动标记，混合表示将全局规划与局部生成解耦，扩散航点生成在连续空间中实现物理合理的轨迹规划，接触损失则进一步强化交互精度。三者协同使得 UniHM 在保持场景约束的同时，生成更真实、多样且物理合理的运动。

UniHM 是一个面向室内场景物体交互的通用人体运动生成框架。其核心设计思路是将运动生成分解为**稀疏航点规划**与**密集标记生成**两个阶段，并通过**混合运动表示**与**免查找量化变分自编码器（LFQ-VAE）** 解决传统离散标记化带来的连续 6DoF 信息损失问题。

### 输入与条件编码

框架接收三类条件输入，分别由专用编码器处理：

- **文本**：通过 **CLIP 文本编码器** 提取文本提示的特征向量，作为运动语义的条件信号。
- **场景**：通过 **ViT-VAE 场景编码器** 将室内场景体素压缩为潜在嵌入，为运动生成提供空间约束。
- **物体**：通过 **PointNet++ 物体编码器** 编码物体点云为特征，用于文本到人-物交互（Text-to-HOI）任务。

### 运动标记化：LFQ-VAE

运动序列首先经过 **LFQ-VAE 运动标记器** 压缩为离散标记。与传统的 VQ-VAE 不同，LFQ-VAE 采用二进制潜在空间，通过免查找量化机制消除了对学习码本的依赖，从而避免了码本利用不充分和高频微运动冗余表示的问题。量化后的标记索引由下式计算：

$$
\mathrm{Index}(\mathbf{z}) = \sum_{i=1}^{\log_2 K} 2^{i-1} \mathbb{1}\{z_i > 0\}
$$

LFQ-VAE 的训练总损失为：

$$
\mathcal{L}_{\mathrm{lfq}} = \lambda_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{commit}} \mathcal{L}_{\mathrm{commit}} + \lambda_{\mathrm{entropy}} \mathcal{L}_{\mathrm{entropy}}
$$

其中重建损失 $\mathcal{L}_{\mathrm{recon}} = \mathbb{E}_{x \sim D}\left[||x - \hat{x}||_2^2\right]$ 保证运动保真度，承诺损失 $\mathcal{L}_{\mathrm{commit}} = ||\mathbf{sg}[z] - \bar{z}||_2^2$ 防止潜在向量波动过大，熵损失 $\mathcal{L}_{\mathrm{entropy}} = \mathbb{E}[H(q(\mathbf{z}))] - H[\mathbb{E}(q(\mathbf{z}))]$ 鼓励码本多样化利用。LFQ-VAE 每 8 帧压缩为一个二进制表示，使用 3 个下采样层，每层下采样率为 2。

### 两阶段生成流程

#### 第一阶段：稀疏航点生成

**因果 Transformer 编码器（CME 生成器）** 融合多模态嵌入（文本、场景、物体），生成上下文运动嵌入（Contextual Motion Embedding, CME）作为运动先验。随后，一个轻量级 **MLP 扩散航点去噪器** 从噪声中预测干净的 6DoF 航点，实现稀疏航点采样。航点表示人体和物体在约 1 秒窗口内的连续 6DoF 运动，其生成采用层次化结构：先估计粗粒度的全局航点，再细化为细粒度的局部位置和朝向。

#### 第二阶段：全序列生成

**全序列生成 Transformer** 基于第一阶段生成的稀疏航点和上下文嵌入，自回归地生成完整运动序列的局部运动标记。最终通过 LFQ-VAE 解码器将离散标记重建为连续运动序列。

### 损失函数

全序列生成阶段的训练结合了三种损失：

- **交叉熵损失** $\mathcal{L}_{\mathrm{CE}} = - \sum_{t} \sum_{k} p_{t}(k) \log \hat{p}_{t}(k)$：用于预测运动标记。
- **6DoF 去噪损失** $\mathcal{L}_{\mathrm{6DoF}} = \mathbb{E}_{(w_{0}, \epsilon) \sim q} \left[ | f_{\theta}(w_{t}, t) - w_{0} |^{2} \right]$：直接预测干净样本而非噪声，用于航点轨迹去噪。
- **接触几何损失** $\mathcal{L}_{\mathrm{contact}} = \frac{1}{mn} \sum_{i=1}^{n} \sum_{j=1}^{m} || \mathrm{dist}(\mathcal{O}_i, J_j) - \mathrm{dist}(\hat{O}_i, \hat{J}_j) ||$：保持预测的人-物距离与真实接触模式一致，通过对部分随机替换的运动标记解码后计算成对距离得到。

### 关键设计决策

UniHM 的架构将全局轨迹规划（连续 6DoF 航点）与局部细节生成（离散运动标记）解耦，使得扩散模型在连续空间中处理稀疏航点，而 Transformer 在离散空间中生成密集标记。这种混合表示有效协调了场景约束下的全局运动合理性与局部运动保真度。

### 补充图表

![[assets/figures/papers/paper_list_l1697_UniHM_Universal_Human_Motion_Generation_with_Object_Interactions_in_Indo/figures/003_Figure_2.jpg]]
*Figure 2: UniHM architecture and Look-up Free Quantization Variational Autoencoder*

UniHM 的运动生成管线可拆解为三个核心功能模块：**运动标记化（LFQ‑VAE）**、**稀疏航点生成（扩散去噪器）** 与**全序列自回归生成（因果 Transformer）**。各模块通过混合运动表示衔接——连续 6DoF 航点负责全局轨迹规划，离散局部标记负责肢体细节。

### 1. 运动标记化：LFQ‑VAE

传统 VQ‑VAE 依赖可学习码本将连续运动映射为离散标记，但码本容量受限且高频微运动在量化空间中产生大量冗余表示，导致重建与生成质量下降。UniHM 采用免查找量化变分自编码器（Look‑up Free Quantization VAE, LFQ‑VAE），将潜在向量直接二值化，完全消除码本依赖。

**量化机制**：编码器输出 $ \mathbf{z} \in \mathbb{R}^{\log_2 K} $，通过符号函数二值化后，按位加权求和得到离散标记索引：

$$ \mathrm{Index}(\mathbf{z}) = \sum_{i=1}^{\log_2 K} 2^{i-1} \mathbb{1}\{z_i > 0\} $$

其中 $K$ 为词汇量大小，$ \mathbb{1}\{\cdot\} $ 为指示函数。该设计使词汇量随潜在维度指数增长，无需存储码本向量，从根本上解决了码本利用不充分的问题。

**损失函数**：LFQ‑VAE 的总损失由三项加权构成：

$$ \mathcal{L}_{\mathrm{lfq}} = \lambda_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{commit}} \mathcal{L}_{\mathrm{commit}} + \lambda_{\mathrm{entropy}} \mathcal{L}_{\mathrm{entropy}} $$

- **重建损失** $\mathcal{L}_{\mathrm{recon}} = \mathbb{E}_{x \sim D}\left[||x - \hat{x}||_2^2\right]$，保证运动序列的逐帧保真度。
- **承诺损失** $\mathcal{L}_{\mathrm{commit}} = ||\mathbf{sg}[z] - \bar{z}||_2^2$，约束编码器输出不要偏离二值化后的向量 $\bar{z}$，其中 $\mathbf{sg}[\cdot]$ 为梯度截断算子。
- **熵损失** $\mathcal{L}_{\mathrm{entropy}} = \mathbb{E}[H(q(\mathbf{z}))] - H[\mathbb{E}(q(\mathbf{z}))]$，最大化码本利用的边际熵，鼓励标记分布多样化。

训练时，$\lambda_{\mathrm{recon}}=1$，$\lambda_{\mathrm{commit}}=1\times10^{-2}$，$\lambda_{\mathrm{entropy}}=1\times10^{-4}$。LFQ‑VAE 采用 3 层下采样（每层步长 2），每 8 帧压缩为一个二值潜在表示。

### 2. 稀疏航点生成：扩散去噪器

航点定义为人体与交互物体在 1 秒窗口内的 6DoF 姿态（全局位置与朝向）。UniHM 使用轻量 MLP 作为扩散去噪器，从噪声中直接预测干净航点样本，而非预测噪声本身。

**去噪损失**：

$$ \mathcal{L}_{\mathrm{6DoF}} = \mathbb{E}_{(w_{0}, \epsilon) \sim q} \left[ | f_{\theta}(w_{t}, t) - w_{0} |^{2} \right] $$

其中 $w_0$ 为真实航点，$w_t$ 为加噪后的航点，$f_\theta$ 为去噪网络，$t$ 为扩散时间步。该损失使模型学习在连续空间中采样稀疏航点，为后续全序列生成提供全局运动先验。

航点生成采用层次化策略：先估计粗粒度全局航点，再细化为细粒度局部位置与朝向，有效协调全局轨迹规划与局部细节生成。

### 3. 全序列生成与接触约束

因果 Transformer 编码器（CME 生成器）融合文本、场景体素、物体点云等多模态嵌入，生成上下文运动嵌入作为先验。随后，全序列生成 Transformer 基于航点和上下文嵌入，自回归预测局部运动标记。

**标记预测损失**（交叉熵）：

$$ \mathcal{L}_{\mathrm{CE}} = - \sum_{t} \sum_{k} p_{t}(k) \log \hat{p}_{t}(k) $$

其中 $p_t(k)$ 为真实标记分布，$\hat{p}_t(k)$ 为预测分布。

**接触几何损失**：为保持人‑物交互的物理合理性，引入基于点对距离的接触损失：

$$ \mathcal{L}_{\mathrm{contact}} = \frac{1}{mn} \sum_{i=1}^{n} \sum_{j=1}^{m} || \mathrm{dist}(\mathcal{O}_i, J_j) - \mathrm{dist}(\hat{O}_i, \hat{J}_j) || $$

其中 $\mathcal{O}_i$ 为物体采样点，$J_j$ 为人体网格预定义关节点，$\mathrm{dist}(\cdot,\cdot)$ 为欧氏距离。该损失约束预测的人‑物距离分布与真实接触模式一致。

**总生成损失**：

$$ \mathcal{L} = \lambda_{\mathrm{CE}} \mathcal{L}_{\mathrm{CE}} + \lambda_{\mathrm{6DoF}} \mathcal{L}_{\mathrm{6DoF}} + \lambda_{\mathrm{contact}} \mathcal{L}_{\mathrm{contact}} $$

三项损失联合优化，使模型在保持场景约束的同时生成真实、多样且物理合理的运动。

### 补充图表

![[assets/figures/papers/paper_list_l1697_UniHM_Universal_Human_Motion_Generation_with_Object_Interactions_in_Indo/figures/010_Figure_5.jpg]]
*Figure 5: Comparison of rFID and gFID for VQ-VAE and LFQ-VAE across different tasks*

## 实验与关键发现

### 核心实验结果

UniHM 在多个基准上展示了统一的运动生成能力，涵盖了通用文本到运动（Text-to-Motion）、场景感知文本到运动（Text-to-Motion in Scene）以及文本到人-物交互（Text-to-HOI）三类任务。

在 **OMOMO 基准的 Text-to-HOI 任务**上，UniHM 取得了 **FID 0.582** 的成绩，优于基线方法 **CHOIS**（Li et al., arXiv 2023），同时接触分数（Contact）达到 **0.847**，与 CHOIS 可比（TABLE I）。在 **Lingo 数据集的场景感知 Text-to-Motion** 任务中，UniHM 将碰撞分数（Collision_s）降至 **0.017**，显著优于 **ARDHOI**（Geng et al., arXiv 2025）（TABLE II）。在 **HumanML3D 的通用 Text-to-Motion** 任务上，UniHM 在 R-Precision 和 Multimodal Distance 等指标上优于 **T2M-GPT**（Zhang et al., CVPR 2023），但在 FID 指标上仍落后于 T2M-GPT（TABLE I）。

定性比较（Fig. 3）显示，UniHM 生成的 HOI 序列在物体交互的物理合理性上明显优于 CHOIS，而在场景中生成的行走、坐下等动作也比 ARDHOI 更符合场景约束，避免了穿透墙壁或悬浮等伪影。

![[assets/figures/papers/paper_list_l1697_UniHM_Universal_Human_Motion_Generation_with_Object_Interactions_in_Indo/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative Comparison. The first two rows are for Text-to-HOI, and the 3-rd & the 4-th rows are for Text-to-Motion*

### 消融研究

消融实验系统性地验证了航点生成模块、去噪器以及 LFQ-VAE 标记化方法的关键作用。

**航点生成模块的不可或缺性**：TABLE III 显示，在场景感知 Text-to-HOI 中去除航点生成模块后，碰撞分数从 **0.021 骤升至 0.120**，接触分数从 **0.855 降至 0.630**；在场景感知 Text-to-Motion 中，碰撞分数也从 **0.017 升至 0.064**。这表明稀疏航点规划是维持全局轨迹合理性和场景约束的核心机制。定性消融（Fig. 4）进一步证实，无航点引导时生成的运动会出现穿透物体、远离交互目标等严重失效。

**去噪器的增益**：在无场景的 Text-to-Motion 和 Text-to-HOI 任务中，引入扩散去噪器分别将 FID 从 0.367 改善至 **0.302**，从 0.642 改善至 **0.582**（TABLE V），证明了噪声-信号精炼策略对生成质量的普遍提升作用。

**航点引导的场景内性能**：TABLE IV 显示，在场景感知 Text-to-Motion 中引入航点引导将碰撞分数从 0.017 进一步降至 **0.010**；在场景感知 Text-to-HOI 中，FID 从 1.232 降至 **0.826**，接触分数从 0.855 提升至 **0.945**。这证实了航点作为中间表示能有效协调全局规划与局部细节。

**LFQ-VAE 与 VQ-VAE 的量化对比**：Fig. 5 揭示了关键洞察——随着词汇量增大，LFQ-VAE 的生成 FID（gFID）持续降低（改善），而 VQ-VAE 的 gFID 反而上升（恶化）。这一证据直接支撑了论文的核心主张：传统 VQ-VAE 的码本限制导致高频微运动在量化空间中产生冗余表示，码本利用不充分，而 LFQ-VAE 通过免查找量化和更大的有效词汇量解决了这一瓶颈。

**数据增强的影响**：引入 Lingo 数据集进行增强训练后，多模态距离和 R-Precision 显著提升，但 FID 略有下降（TABLE V），提示数据分布偏移可能对生成多样性造成轻微负面影响。

### 失败模式与局限性

尽管 UniHM 在多数指标上表现优异，但分析揭示了若干值得关注的失效模式和局限：

1. **通用运动生成 FID 落后**：UniHM 在 HumanML3D 的 FID 上不及 T2M-GPT。这可能源于混合运动表示引入的额外复杂性——模型需要同时学习连续 6DoF 和离散局部标记的联合分布，增加了优化难度，或在当前训练配置下尚未充分收敛。此点需要手动验证具体数值差异。

2. **场景泛化能力未经验证**：论文未报告方法在全新室内布局（训练集中未见的场景）上的表现。模型可能过度依赖训练场景的统计分布，对显著不同的空间结构产生不合理的运动。此局限性需要后续工作验证。

3. **物理合理性依赖损失函数而非仿真**：物体交互的物理合理性完全由接触几何损失 $\mathcal{L}_{\mathrm{contact}}$ 驱动，未经过物理仿真引擎验证。这意味着生成的接触模式可能在视觉上合理，但在真实物理约束下并不可行（如手部穿透物体表面但损失值仍可接受）。

4. **计算效率未充分讨论**：扩散去噪过程增加了推理时间，但论文未与纯自回归模型（如 T2M-GPT）进行效率对比。在实际部署中，这可能成为瓶颈。

### 开放问题

1. **混合扩散的内部机制**：扩散模型如何在连续 6DoF 空间和离散标记空间之间桥接？去噪器预测的干净航点如何具体影响后续自回归 Transformer 的标记生成？内部机制尚不明确。

2. **FID 落后的深层原因**：为何 UniHM 在 R-Precision 和 Multimodal Distance 上领先却在 FID 上落后？是混合表示的固有信息瓶颈，还是训练策略（如损失权重 $\lambda_{\mathrm{CE}}$ 与 $\lambda_{\mathrm{6DoF}}$ 的平衡）未达最优？

3. **航点与去噪器的协同机制**：TABLE III 和 TABLE V 显示航点和去噪器各自独立有效，但二者联合作用的内部机理——例如去噪器是否主要修正航点预测误差，还是同时改善了条件嵌入质量——尚未被解剖。

4. **LFQ-VAE 超参数的定量影响**：Fig. 5 展示了词汇量对 gFID 的趋势，但下采样率、潜在维度等其他超参数的敏感性分析缺失，限制了方法的可复现调优。

5. **扩展性边界**：该方法能否处理多人交互场景或动态物体（如移动的椅子）？当前框架假设静态场景和单一交互物体，扩展至多智能体或多物体协调仍是一个开放挑战。

### 补充图表

![[assets/figures/papers/paper_list_l1697_UniHM_Universal_Human_Motion_Generation_with_Object_Interactions_in_Indo/figures/004_Table.jpg]]
*Table: I: Comparison results of Text-to-HOI, and Text-to-HOI without Scene TABLE II: Comparison results of Text-to-Motion, Text-to-Motion in Scene. We add the scene voxel encoded by our ViT-VAE encoder to the variant marked with * as conditions*

![[assets/figures/papers/paper_list_l1697_UniHM_Universal_Human_Motion_Generation_with_Object_Interactions_in_Indo/figures/008_Table.jpg]]
*Table: III: Ablation Study on HSI dataset, waypoint, and denoiser for motion generation in scenes*

![[assets/figures/papers/paper_list_l1697_UniHM_Universal_Human_Motion_Generation_with_Object_Interactions_in_Indo/figures/009_Table.jpg]]
*Table: V: Ablation Study on HSI dataset, waypoint, and denoiser for Text-to-Motion and Text-to-HOI without scene*

## 定位与知识库关联

### 1. 与现有工作的关系与差异化

UniHM 处于**场景感知人体运动生成**与**文本驱动的物体交互运动合成**的交汇点，其方法设计直接回应了现有范式的两重瓶颈：运动标记化的信息损失与全局-局部运动规划的割裂。

**相对于离散标记化范式的超越**。以 **T2M-GPT**（Zhang et al., CVPR 2023）为代表的纯离散标记化方法，依赖 VQ-VAE 将连续运动压缩为有限码本中的离散索引。这一过程不可避免地损失了连续 6DoF 运动信息（特别是全局轨迹与精细接触姿态），且高频微运动在量化空间中产生大量冗余表示，导致码本利用率低下。UniHM 用**免查找量化 VAE（LFQ-VAE）**替换传统 VQ-VAE，从根本上消除了码本大小的限制——LFQ-VAE 的词汇量随潜在维度指数增长（$K = 2^{\log_2 K}$），而 VQ-VAE 需要显式存储和检索码本向量。实验证据（Fig. 5）直接验证了这一设计优势：随着词汇量增大，LFQ-VAE 的生成 FID（gFID）持续降低，而 VQ-VAE 的 gFID 反而上升，表明更大的离散空间在 VQ-VAE 中加剧了码本坍缩问题，而 LFQ-VAE 则能有效利用扩大的表示容量。

**相对于纯连续或纯离散表示的混合设计**。现有方法通常在连续参数化（如直接回归 6DoF 轨迹）与纯离散标记之间二选一。连续方法难以捕捉局部运动模式的组合性，离散方法则丢失全局轨迹的精度。UniHM 的**混合运动表示**——连续 6DoF 航点与离散局部运动标记的结合——将全局轨迹规划与局部姿态生成解耦为两个协同的子问题。这一设计在概念上类似于分层运动规划，但通过扩散模型在连续空间中处理航点，避免了离散化对空间精度的损害。

**相对于场景感知运动生成的改进**。**CHOIS**（Li et al., arXiv 2023）和 **ARDHOI**（Geng et al., arXiv 2025）是场景感知 Text-to-HOI 和 Text-to-Motion 的代表性基线，但它们缺乏显式的航点规划机制。UniHM 通过引入**基于扩散模型的稀疏航点生成**，在场景约束下先规划人体和物体的 6DoF 航点（1 秒窗口），再自回归生成局部运动标记。消融实验（TABLE III）提供了决定性证据：去除航点生成模块后，场景感知 Text-to-HOI 的碰撞分数从 0.021 骤升至 0.120，接触分数从 0.855 降至 0.630；场景感知 Text-to-Motion 的碰撞分数从 0.017 升至 0.064。这表明航点规划对于场景约束下的物理合理性至关重要，而不仅仅是锦上添花的辅助模块。

**损失函数层面的扩展**。相对于仅使用交叉熵损失的纯离散方法，UniHM 引入了**6DoF 去噪损失**（$\mathcal{L}_{\mathrm{6DoF}}$）和**接触几何损失**（$\mathcal{L}_{\mathrm{contact}}$）。接触损失通过计算预测人-物点对距离与真实距离的平均绝对偏差，显式约束交互的几何一致性，这是现有基线中少见的设计。

### 2. 适用边界与局限

**FID 指标的相对劣势**。尽管 UniHM 在多数指标上优于 T2M-GPT，但在 HumanML3D 的 Text-to-Motion FID 上仍不及后者。这一现象可能源于混合表示引入的额外复杂性——LFQ-VAE 的二进制潜在空间和扩散航点去噪器增加了训练难度，且模型可能需要在重建保真度与生成多样性之间重新平衡。此外，TABLE V 显示引入 Lingo 数据集增强后 FID 略有下降，暗示跨数据集泛化时分布偏移对生成质量的影响。

**场景泛化能力未验证**。UniHM 在 OMOMO 和 Lingo 数据集上评估，这些数据集包含特定的室内场景分布。论文未讨论模型对全新场景（未见过的室内布局）的泛化能力，这是一个重要的适用边界。ViT-VAE 场景编码器可能依赖训练集中相似的场景拓扑，在分布外场景中可能产生不可靠的空间约束。

**计算效率的隐忧**。扩散航点去噪器虽然轻量（MLP 结构），但扩散过程本身增加了推理时的采样步骤。论文未与纯自回归模型（如 T2M-GPT）对比推理时间，这在实时应用场景中是一个关键缺失。

**物理合理性的验证深度**。物体交互的物理合理性依赖接触损失和场景碰撞度量（Collision_s），但未进行物理仿真验证（如通过物理引擎检查穿透、滑动、接触力等）。Collision_s 作为代理指标可能无法捕捉所有物理违规情况。

### 3. 开放问题

1. **混合扩散-自回归的桥接机制**。扩散航点去噪器如何将预测的连续 6DoF 航点条件化地注入自回归 Transformer 的局部标记生成？论文描述了“基于航点和上下文嵌入”的生成流程，但信息融合的具体架构设计（如交叉注意力、特征拼接或条件归一化）未充分展开，这限制了该方法向其他混合生成任务的迁移。

2. **FID 劣势的深层原因**。UniHM 在 HumanML3D 的 FID 上落后于 T2M-GPT，但 R-Precision 和 Multimodal Distance 更优。这是否意味着 LFQ-VAE 的重建分布与真实运动分布之间存在系统性偏差？还是航点规划在无场景约束时引入了不必要的正则化，限制了运动多样性？需要更细粒度的逐类运动分析。

3. **航点与去噪器的协同机制**。TABLE III 和 TABLE IV 分别展示了去除航点和引入航点引导的效果，但航点生成与去噪器之间的协同关系尚不明确。去噪器是否通过预测“干净航点”来隐式建模场景几何约束？航点的时间粒度（1 秒窗口）是如何选择的，更细或更粗的粒度会如何影响碰撞-接触权衡？

4. **LFQ-VAE 超参数的敏感性**。Fig. 5 展示了词汇量对 gFID 的影响趋势，但下采样率（3 层，每层步长 2，压缩 8 帧）、潜在维度、熵损失系数等超参数的定量消融未见报告。这些选择是否在特定任务（Text-to-Motion vs. Text-to-HOI）上有不同的最优配置？

5. **多人与动态场景的扩展性**。UniHM 当前处理单人-静态物体交互。扩展到多人协作场景（如两人搬动家具）需要同时建模多人运动协调和动态物体轨迹，当前的航点表示和接触损失是否足以应对？动态场景（如移动障碍物）则需要时序场景编码，ViT-VAE 的静态体素表示可能需要升级为时空编码器。

6. **接触损失的几何完备性**。$\mathcal{L}_{\mathrm{contact}}$ 仅约束人-物点对距离，未显式建模接触法向、切向滑动或接触面积。在需要精细操作的任务中（如抓取小物体），这种简化可能导致视觉上合理但物理上不可行的接触姿态。

## 原文 PDF

![[paperPDFs/arxiv_2025/UniHM_Universal_Human_Motion_Generation_with_Object_Interactions_in_Indoor_Scenes.pdf]]
