---
title: "ManifoldGD: Training-Free Hierarchical Manifold Guidance for Diffusion-Based Dataset Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ManifoldGD_Training_Free_Hierarchical_Manifold_Guidance_for_Diffusion_Based_Dataset_Distillation.pdf
project_link: null
code_link: "https://github.com/AyushRoy2001/ManifoldGD"
aliases:
- ManifoldGD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过局部估计扩散流形的切空间，将模式引导向量投影到切空间，消除法向分量，从而约束生成轨迹保持在数据流形上。
primary_logic: 在VAE潜在空间进行层次分裂聚类构建多尺度IPC质心，并在每个去噪步通过局部近邻协方差估计扩散流形的切空间与法空间，将模式引导修正为切向分量，实现语义吸引与几何保真度的统一。
claims:
- ManifoldGD在所有IPC设置下均优于现有无训练方法，并在部分情况下超越基于训练的方法。
- 消融实验证明层次分裂聚类和流形投影各自提升性能，结合后退火进一步优化。
- ManifoldGD生成的样本具有更低的FID、更高的代表性和多样性。
- ManifoldGD在ImageNet-1k的极端低IPC下仍保持优势。
---

# ManifoldGD: Training-Free Hierarchical Manifold Guidance for Diffusion-Based Dataset Distillation

> [!tip] 核心洞察
> 在VAE潜在空间进行层次分裂聚类构建多尺度IPC质心，并在每个去噪步通过局部近邻协方差估计扩散流形的切空间与法空间，将模式引导修正为切向分量，实现语义吸引与几何保真度的统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | ManifoldGD：用于基于扩散的数据集蒸馏的无训练层次流形引导 |
| 英文题名 | ManifoldGD: Training-Free Hierarchical Manifold Guidance for Diffusion-Based Dataset Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23295) · [Code](https://github.com/AyushRoy2001/ManifoldGD) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ManifoldGD |
| Dataset | ImageNette, ImageNet-100, ImageWoof, ImageNet-1k |

> [!tip] 效果简介
> - ImageNette 上，$\operatorname{Acc}_{S\to\mathcal{D}}$ (ResNetAP-10) 78.4±1.0 (IPC=50) vs MGD*: 77.5±1.1 (+0.9)。
> - ImageNet-100 上，$\operatorname{Acc}_{S\to\mathcal{D}}$ (ResNetAP-10) 35.3±0.5 (IPC=20) vs MGD*: 33.2±0.5 (+2.1)。
> - ImageWoof 上，$\operatorname{Acc}_{S\to\mathcal{D}}$ (ResNetAP-10) 38.3±0.4 (IPC=10) vs MGD*: 37.0±0.4 (+1.3)。

## 概要

数据集蒸馏旨在将大规模真实数据集压缩为极少量合成样本，同时保持下游模型训练的有效性。近年来，基于扩散模型的无训练蒸馏方法因其免去昂贵优化过程而受到关注，但现有方法（如**MGD**）仅依赖欧几里得空间中的模式引导，将生成轨迹简单吸引向聚类质心，忽略了扩散流形的内在几何结构。这导致合成样本偏离真实数据流形，产生结构异常、语义模糊或多样性不足的生成结果。

**ManifoldGD** 针对上述瓶颈，提出一种无训练的层次流形引导框架。其核心洞察在于：通过局部估计扩散流形的切空间与法空间，将模式引导向量中的法向分量显式移除，使去噪轨迹始终保持在数据流形上，从而在保持语义吸引的同时实现几何保真度。具体而言，该方法在VAE潜在空间内执行层次分裂聚类，构建多尺度IPC质心以捕获从粗粒度语义到细粒度类内变化的完整模式分布；在每个去噪步，利用局部近邻协方差估计当前噪声水平下的流形几何，并将模式引导修正为切向对齐的流形引导。

实验结果表明，ManifoldGD在所有IPC设置下均一致优于现有无训练方法，并在部分场景下超越基于训练的蒸馏方法。在ImageNette（IPC=50）上达到78.4%的分类准确率，较MGD提升0.9个百分点；在ImageNet-100（IPC=20）上达到35.3%，提升2.1个百分点；在更具挑战性的ImageNet-1k全量数据集上，IPC=1时准确率为3.1%，IPC=50时达21.4%，均保持对DiT和MGD的优势。消融研究进一步证实，层次分裂聚类、流形投影校正以及指数退火半径调度各自对性能有显著贡献，且框架对扩散调度器不敏感，在DDIM下同样有效。

### 数据集蒸馏的核心矛盾

数据集蒸馏（Dataset Distillation）的目标是从大规模真实数据集 $\mathcal{D}$ 中合成一个极小的代理数据集 $\mathcal{S}$，使得在 $\mathcal{S}$ 上训练的模型能够逼近在 $\mathcal{D}$ 上训练的模型性能。其形式化目标为：

$$\mathcal{S}^{*} = \arg\min_{\mathcal{S}} \bigg| \mathbb{E}_{(x,y)\sim\mathcal{D}} \ell\big(f_{\theta_{\mathcal{S}}^{*}}(x), y\big) - \mathbb{E}_{(x,y)\sim\mathcal{D}} \ell\big(f_{\theta_{\mathcal{D}}^{*}}(x), y\big) \bigg|$$

这一目标的核心挑战在于：合成样本必须在信息密度和语义覆盖上同时满足“代表性”和“多样性”——既要忠实反映真实数据分布的模式，又要避免冗余和重复。

### 基于扩散的无训练蒸馏范式的兴起

传统数据集蒸馏方法依赖元学习或梯度匹配等训练密集型范式，计算开销巨大。近年来，基于预训练扩散模型的**无训练蒸馏**（training-free distillation）范式因其即插即用的推理效率受到关注。这类方法利用扩散模型已编码的丰富生成先验，在无需额外训练的条件下直接合成蒸馏样本。

其中，**模式引导扩散**（Mode-Guided Diffusion, **MGD**）是无训练范式的代表性工作。MGD将条件得分函数分解为两项：

$$\nabla_{x_t} \log p_t(x_t \mid c) = \underbrace{\nabla_{x_t} \log p_t(x_t)}_{\text{边际去噪}} + \underbrace{\nabla_{x_t} \log p_t(c \mid x_t)}_{\text{模式引导}}$$

其中 $c$ 为选定的IPC（Images Per Class）质心。去噪更新规则为：

$$x_{t-1} = x_t + \eta_t \big[ s_\theta(x_t, t) + g_{\text{mode}}^t \big] + \sqrt{\beta_t} \epsilon_t$$

MGD通过欧几里得空间中的模式引导向量 $g_{\text{mode}}^t$ 将生成轨迹“吸引”向IPC质心，从而在无训练条件下实现可控合成。

### 欧几里得模式引导的几何盲区

尽管MGD在效率上具有优势，但其引导机制存在一个根本性缺陷：**$g_{\text{mode}}^t$ 完全在欧几里得空间中运作，不感知生成流形的几何结构**。扩散模型的数据生成过程天然地约束在一个低维流形上——从纯噪声逐步去噪的过程本质上是沿流形“滑行”回到数据分布。然而，MGD的模式引导向量同时包含：

- **切向分量**：沿流形表面推动生成轨迹，有助于保持语义一致性；
- **法向分量**：将生成轨迹推向流形之外，导致合成样本偏离数据分布支撑集。

这一法向分量的存在直接导致MGD的生成样本出现**低质量、重复模式、语义模糊**等问题——例如生成狗的图像时出现不自然的肢体位置，或建筑物的结构异常（见图2）。定性观察表明，MGD在去噪后期（$t \leq 20$）的几何细化和纹理生成阶段表现尤为不足（见图3）。

### 层次化模式表征的缺失

MGD的另一个局限在于IPC质心的选择策略。MGD采用简单的K-means聚类选取质心，这导致两个问题：

1. **尺度单一**：K-means仅提供单一粒度的模式代表，无法捕获类内从粗粒度语义模式到细粒度视觉变体的多尺度结构；
2. **覆盖不足**：K-means质心倾向于聚集在特征云团的高密度区域，忽略边缘分布，导致合成样本缺乏多样性（见图6）。

### 本文动机

上述分析揭示了无训练扩散蒸馏的两个关键瓶颈：

1. **几何盲引导**：欧几里得模式引导缺乏流形感知能力，法向分量推离生成轨迹，损害合成质量；
2. **扁平模式表征**：单尺度聚类无法充分覆盖类内模式的层次结构，限制代表性和多样性。

本文提出**ManifoldGD**，通过以下两个核心创新同时解决这两个瓶颈：

- **流形校正引导**：在每个去噪步局部估计扩散流形的切空间，将模式引导向量投影到切空间，消除法向分量，使生成轨迹始终保持在数据流形上；
- **层次分裂聚类**：在VAE潜在空间执行自顶向下的分裂层次聚类，构建多尺度IPC质心树，从粗到细遍历选取质心，实现语义模式与类内变体的统一捕获。

通过将流形几何约束与层次模式表征相结合，ManifoldGD在保持无训练推理效率的同时，显著提升了合成样本的质量、代表性和多样性。

## 核心方法与创新机理

ManifoldGD 的核心创新在于**将扩散生成轨迹约束在数据流形上**，从而解决现有无训练扩散蒸馏方法（如 MGD）因忽略流形几何结构而导致的生成样本偏离真实分布的问题。其关键设计围绕三个相互耦合的 changed slots 展开。

### 从欧几里得引导到流形一致引导

现有模式引导方法（MGD）直接在欧几里得空间中计算模式引导向量 $g_{mode}^t$，将生成样本拉向 IPC 质心。然而，这种纯欧几里得吸引忽略了扩散流形的几何结构——当引导向量存在显著的法向分量时，生成轨迹会被推离数据流形，导致样本质量下降（Fig. 1）。

ManifoldGD 的核心因果旋钮在于**局部估计扩散流形的切空间，并将模式引导投影到切空间上**。具体而言，对于每个去噪时间步 $t$，方法通过质心邻域的 K 近邻协方差估计局部切空间 $\mathcal{T}_t$ 和法空间 $\mathcal{N}_t$，然后从模式引导中显式减去法向分量：

$$g_{manifold}^{t}(x_{t};c) = g_{mode}^{t}(x_{t};c) - P_{\mathcal{N}_{t}} g_{mode}^{t}(x_{t};c)$$

这一操作将引导修正为切向对齐的流形引导 $g_{manifold}^t$，实现了**语义吸引与几何保真度的统一**：生成样本既被拉向目标语义模式，又始终保持在数据流形上（Fig. 1）。消融实验确认，流形引导的加入在所有设置下均显著提升性能（Tab. 3）。

### 层次分裂聚类构建多尺度 IPC 质心

传统 K-means 聚类仅能捕捉特征云的中心区域，无法覆盖类内分布的边界和细粒度变异（Fig. 6）。ManifoldGD 改用**分裂层次聚类（Divisive hierarchical clustering）**在 VAE 潜在空间中构建多尺度 IPC 质心。

该方法自顶向下递归二分，生成一棵层次树，每层对应不同粒度的语义模式。在采样时，从层次树中按 coarse-to-fine 遍历选取每层的一个节点作为质心，使引导信号同时包含粗粒度语义锚定和细粒度类内变异信息。这一设计使 IPC 质心能够覆盖特征云的均值区域和轮廓区域，凸包面积比显著优于 K-means（Fig. 6）。消融实验表明，分裂层次聚类（Divisive-levelwise）相比 K-means 和凝聚层次聚类均取得更高准确率（Tab. 3）。

### 指数退火邻域半径调度

局部流形估计依赖于质心邻域 $\mathcal{N}_s$ 的半径选择。固定半径面临两难：大半径在早期去噪阶段能容纳探索，但在后期会引入噪声；小半径则相反。ManifoldGD 引入**指数退火半径调度**，使邻域半径随去噪步递减——早期较大的半径适应流形估计的不确定性，后期逐步收紧以强制执行几何约束。消融实验证实，指数退火调度优于固定半径、线性衰减和余弦衰减策略（Tab. 4）。

### 三个创新点的协同机制

上述三个 changed slots 形成递进协同：层次聚类提供多尺度语义锚点 → 局部邻域构造与退火调度提供可靠的流形估计基础 → 切空间投影将语义引导修正为流形一致的方向。这一协同使得 ManifoldGD 在完全无训练的条件下，生成的样本具有更低的 FID、更高的代表性和多样性（Fig. 5），并在多个 ImageNet 子集上一致优于现有无训练方法（Tab. 1, Tab. 2）。

ManifoldGD 构建了一套**完全免训练、仅推理**的数据集蒸馏流水线，其核心目标是在不更新预训练扩散模型参数的前提下，生成既忠实于数据流形又具备类内多样性的合成样本。整个框架围绕一个关键瓶颈展开：现有免训练模式引导方法（如 MGD）仅依赖欧几里得空间中的吸引力将生成样本拉向类质心，但忽略了扩散流形的几何结构，导致生成轨迹偏离数据流形，产生低质量、重复或语义模糊的样本。ManifoldGD 通过在每个去噪时间步**估计局部流形的切空间并消除法向分量**，将模式引导修正为流形一致的切向引导，从而约束生成过程始终保持在数据流形上。

### 流水线模块与数据流

框架由五个顺序耦合的模块组成，数据从原始图像流向最终的合成蒸馏数据集：

1. **VAE 编码**  
   将原始图像通过预训练的 VAE 编码器映射到潜在空间，得到低维潜在特征 $z = \mathcal{E}(x)$。这一步骤为后续聚类和扩散过程提供了紧凑且语义丰富的表示空间，是整个流水线的基础表示层。

2. **层次聚类与 IPC 质心选择**  
   在每个类别内部，对 VAE 潜在特征执行**分裂式层次聚类**（divisive hierarchical clustering，具体采用 bisecting k-means），构建一棵多尺度聚类树。从该树中按 coarse-to-fine 的层级遍历策略选取 IPC 质心——每层选取一个节点，使得所选质心既能覆盖特征云的均值区域，又能捕捉边缘轮廓（见 Fig. 6），从而形成多尺度核心集（coreset）。这与 MGD 使用的单一 k-means 聚类形成鲜明对比：k-means 质心往往无法完整覆盖特征云，而分裂层次聚类通过层级结构自然地捕获了从粗粒度语义模式到细粒度类内变化的完整谱系。

3. **局部邻域构造与时间对齐流形补丁**  
   为每个选定的质心定义局部半径邻域 $\mathcal{N}_s$（半径 $r$ 采用指数退火调度），对该邻域内的点进行前向扩散，得到与当前去噪时间步 $t$ 噪声水平对齐的流形补丁：
   $$\mathcal{M}_t^{(s)} = \mathcal{N}_s + \epsilon_t, \quad \epsilon_t \sim \mathcal{N}\big(0, (1-\bar{\alpha}_t)I\big)$$
   这一步骤将干净流形的局部几何信息“传输”到噪声空间，为后续几何估计提供与当前采样状态匹配的参考点云。

4. **局部几何估计与流形校正**  
   基于噪声流形补丁 $\mathcal{M}_t^{(s)}$ 中的 $K$ 近邻，通过局部协方差分析估计扩散流形在当前点 $x_t$ 处的切空间 $\mathcal{T}_t$ 和法空间 $\mathcal{N}_t$。将模式引导向量 $g_{\text{mode}}^t$ 投影到法空间并减去，得到切向对齐的流形引导：
   $$g_{\text{manifold}}^t(x_t; c) = g_{\text{mode}}^t(x_t; c) - P_{\mathcal{N}_t} g_{\text{mode}}^t(x_t; c)$$
   这一校正操作是框架的**因果旋钮**：它保留了模式引导的语义吸引力（切向分量），同时消除了将样本推出数据流形的法向偏差，实现了语义吸引与几何保真度的统一。

5. **反向扩散采样**  
   结合预训练扩散模型的得分网络 $s_\theta(x_t, t)$ 与流形引导，构造完整的流形条件得分函数：
   $$s_{\text{manifold}}^t(x_t) = s_\theta(x_t, t) + g_{\text{manifold}}^t$$
   按标准去噪更新规则逐步迭代：
   $$x_{t-1} = x_t + \eta_t \big[s_\theta(x_t, t) + g_{\text{manifold}}^t\big] + \sqrt{\beta_t}\epsilon_t$$
   从随机噪声 $x_T$ 出发，经 $T$ 步去噪后解码回图像空间，得到最终的合成蒸馏样本。

### 关键设计决策与组件耦合

框架中几个设计决策之间存在紧密的因果耦合：

- **层次聚类与多尺度质心选择**为流形校正提供了更丰富的模式覆盖——单一质心仅能提供点对点的欧几里得吸引，而多尺度质心使流形引导能在不同语义粒度上同时施加约束。
- **指数退火半径调度**解决了早期流形估计不确定性与后期几何精度需求之间的矛盾：较大初始半径在流形估计粗糙时允许必要的探索，随着去噪推进逐步收紧半径以强化几何约束。消融实验（Tab. 4）证实指数退火在所有调度策略中取得最佳性能。
- **流形校正的介入时机**由参数 $T_{\text{STOP}}$ 控制：在去噪早期（$t > T_{\text{STOP}}$）仅使用模式引导捕获粗粒度语义结构，在后期（$t \leq T_{\text{STOP}}$）引入流形校正以细化几何和纹理。消融表明 $T_{\text{STOP}}=25$（总步数 50）时在 FID 和准确率上达到最优平衡点（Fig. 8）。

### 输入输出规范

- **输入**：原始训练集 $\mathcal{D}$、预训练扩散模型（含 VAE 和得分网络）、目标 IPC 数、半径调度参数、切空间维度 $d$（最优值 3，见 Tab. 9）。
- **输出**：合成蒸馏数据集 $\mathcal{S}$，其中每类包含 IPC 张图像，可直接用于下游分类器训练。
- **计算特性**：全程无需梯度反传或模型微调，推理时间与准确率的权衡优于 MGD 和 DiT（Fig. 11），框架对扩散调度器不敏感——在 DDIM 下同样保持优势（Tab. 8）。

### 整体框架：无训练扩散蒸馏的流形约束范式

ManifoldGD 的核心瓶颈在于：现有无训练模式引导扩散（如 MGD）仅依赖欧几里得距离吸引生成样本向 IPC 质心靠拢，却忽略了扩散流形的几何结构，导致生成轨迹偏离数据流形，产生低质量、重复或语义模糊的合成样本。ManifoldGD 的因果调节变量是：在每个去噪步，局部估计扩散流形的切空间与法空间，将模式引导向量投影到切空间，消除法向分量，从而将生成过程约束在数据流形上。

整个管线由五个模块串联构成：VAE 编码 → 层次聚类与 IPC 质心选择 → 局部邻域构造与时间对齐流形补丁 → 局部几何估计与流形校正 → 反向扩散采样。以下按模块展开关键公式与机制。

---

### 模块一：VAE 编码

所有操作在预训练 VAE 的潜在空间中进行。给定真实图像 $x$，VAE 编码器 $E$ 将其映射为潜在表示 $z = E(x)$。扩散模型在该潜在空间中执行去噪过程，因此后续的聚类、邻域构造、流形估计均基于 VAE 特征进行。这一选择使得流形几何的估计在语义上有意义的低维空间中完成。

---

### 模块二：层次分裂聚类与 IPC 质心选择

传统 MGD 使用 K-means 聚类选取 IPC 质心，但 K-means 倾向于覆盖特征云的中心区域，遗漏边缘分布，导致生成样本缺乏多样性。ManifoldGD 改用**层次分裂聚类**（divisive hierarchical clustering，具体为 bisecting K-means），在类内 VAE 特征上递归二分，构建一棵层次树。从该树中按 coarse-to-fine 遍历选取多尺度质心：从较粗粒度层（靠近根节点）捕获类级语义模式，到较细粒度层（靠近叶节点）捕获细粒度类内变异。这一策略使 IPC 质心同时覆盖特征云的均值附近和轮廓区域，提升了生成样本的代表性与多样性（Fig. 6 展示了 K-means 与 divisive-levelwise 在凸包面积比上的差异）。

---

### 模块三：局部邻域构造与时间对齐流形补丁

对于每个选定的 IPC 质心 $c$（在 VAE 潜在空间中），定义半径为 $r$ 的局部邻域 $\mathcal{N}_s$，包含该质心周围的 $K$ 个近邻真实样本的潜在表示。为了估计在任意噪声水平 $t$ 下的扩散流形，对这些邻域点施加前向扩散，得到噪声化的局部流形补丁：

$$\mathcal{M}_t^{(s)} = \mathcal{N}_s + \epsilon_t, \quad \epsilon_t \sim \mathcal{N}\big(0, (1-\bar{\alpha}_t)I\big) \tag{5}$$

其中 $\bar{\alpha}_t$ 为扩散过程的累积信噪比参数。这一操作将干净流形的局部几何“提升”到当前噪声尺度，使得后续的切空间估计与当前去噪步的样本 $x_t$ 处于同一噪声水平。

邻域半径 $r$ 采用**指数退火调度**：在去噪早期（高噪声、流形估计不确定）使用较大半径以容纳必要的探索，随着去噪推进逐步收紧半径以强制执行几何约束。消融实验（Tab. 4）表明指数退火优于固定半径和其他衰减策略。

---

### 模块四：局部几何估计与流形校正

这是 ManifoldGD 的核心创新。给定当前去噪样本 $x_t$ 和对应的噪声化流形补丁 $\mathcal{M}_t^{(s)}$，首先基于 $K$ 近邻的样本协方差矩阵估计局部切空间 $\mathcal{T}_t$ 和法空间 $\mathcal{N}_t$。具体而言，对 $\mathcal{M}_t^{(s)}$ 中的点进行中心化后计算协方差矩阵，取前 $d$ 个最大特征值对应的特征向量张成切空间，剩余特征向量张成法空间。消融实验（Tab. 9）表明切空间维度 $d=3$ 时性能最优。

模式引导向量 $g_{\text{mode}}^t$ 定义为去噪样本 $x_t$ 与 IPC 质心 $c$ 之间的核亲和度梯度，驱动 $x_t$ 向质心方向移动。然而，该向量可能包含指向法向的分量，将生成轨迹推离数据流形。ManifoldGD 通过减去法向投影来校正：

$$g_{\text{manifold}}^t(x_t; c) = g_{\text{mode}}^t(x_t; c) - P_{\mathcal{N}_t} g_{\text{mode}}^t(x_t; c) \tag{4}$$

其中 $P_{\mathcal{N}_t}$ 是向法空间 $\mathcal{N}_t$ 的正交投影算子。这一操作将模式引导的语义吸引力约束在数据流形的切方向上，实现了“语义吸引”与“几何保真度”的解耦控制。

完整的流形条件得分函数为：

$$s_{\text{manifold}}^t(x_t) = s_\theta(x_t, t) + g_{\text{manifold}}^t$$

其中 $s_\theta(x_t, t)$ 是预训练扩散模型的得分网络（边际去噪项）。

---

### 模块五：反向扩散采样

最终的去噪更新规则结合了得分网络与流形校正引导：

$$x_{t-1} = x_t + \eta_t \big[s_\theta(x_t, t) + g_{\text{manifold}}^t\big] + \sqrt{\beta_t}\epsilon_t$$

其中 $\eta_t$ 为步长，$\beta_t$ 为噪声调度参数，$\epsilon_t \sim \mathcal{N}(0, I)$ 为标准高斯噪声。通过在所有去噪步上施加流形约束，生成轨迹被持续校正，确保最终样本 $x_0$ 既忠实于数据流形，又受 IPC 质心的语义引导。

---

### 关键公式汇总

| 公式 | 含义 | 锚点 |
|------|------|------|
| $\nabla_{x_t}\log p_t(x_t\mid c) = \nabla_{x_t}\log p_t(x_t) + \nabla_{x_t}\log p_t(c\mid x_t)$ | 条件得分分解为边际去噪项与模式引导项 | Eq. (2) |
| $x_{t-1} = x_t + \eta_t[s_\theta(x_t,t) + g_{\text{mode}}^t] + \sqrt{\beta_t}\epsilon_t$ | 模式引导下的去噪更新（MGD 基线） | Eq. (3) |
| $g_{\text{manifold}}^t(x_t;c) = g_{\text{mode}}^t(x_t;c) - P_{\mathcal{N}_t}g_{\text{mode}}^t(x_t;c)$ | 流形校正引导：减去法向分量 | Eq. (4) |
| $\mathcal{M}_t^{(s)} = \mathcal{N}_s + \epsilon_t, \epsilon_t \sim \mathcal{N}(0, (1-\bar{\alpha}_t)I)$ | 噪声化局部流形补丁构造 | Eq. (5) |

---

### 方法谱系与知识库定位

ManifoldGD 属于**无训练扩散数据集蒸馏**方法，与以下工作形成对比：

- **MGD**（Mode-Guided Diffusion）：仅使用欧几里得模式引导，无流形几何约束，是 ManifoldGD 的直接基线和方法基础。
- **DiT**：扩散变换器，无引导采样，作为无训练下界。
- **D4M / DM / MinMaxDiff**：基于训练的扩散蒸馏方法，需微调扩散模型，ManifoldGD 在部分 IPC 设置下可超越这些方法（Tab. 1）。
- **Herding / IDC-1**：核集选择方法，非生成式，性能通常弱于扩散蒸馏方法。

ManifoldGD 的核心贡献在于将**局部流形几何估计**引入扩散引导过程，通过切空间投影实现训练无关的流形一致性约束，填补了无训练扩散蒸馏中几何保真度的空白。其层次分裂聚类策略则改进了 IPC 质心的覆盖质量，进一步提升了生成样本的多样性与代表性。

## 实验与关键发现

### 主实验结果

ManifoldGD 在多个 ImageNet 子集上以硬标签协议进行了系统评估，涵盖 ImageNette（10 类）、ImageWoof（10 类细粒度犬种）和 ImageNet-100（100 类），IPC 设置覆盖 10、20、50。所有结果均报告均值 ± 标准差，基线方法中标注 * 的版本（如 MGD*、DiT*）为统一重新实现，确保对比公平性。

**ImageNette 与 ImageNet-100（Tab. 1）**：ManifoldGD 在所有 IPC 设置下均优于现有无训练方法。以 ResNetAP-10 评估为例，ImageNette IPC=50 时达到 78.4±1.0，相比 MGD*（77.5±1.1）提升 0.9 个百分点；ImageNet-100 IPC=20 时达到 35.3±0.5，相比 MGD*（33.2±0.5）提升 2.1 个百分点。值得注意的是，ManifoldGD 在部分设置下甚至超越了基于训练的方法——在 ImageNette IPC=50 和 ImageNet-100 IPC=50 上均超过 D4M 和 DM 等微调方法，验证了无训练流形引导的强大竞争力。

**ImageWoof 细粒度分类（Tab. 2）**：在更具挑战的犬种细粒度识别任务上，ManifoldGD 同样保持优势。IPC=10 时 ResNetAP-10 准确率达到 38.3±0.4（MGD* 为 37.0±0.4），IPC=50 时提升至 49.7±0.3（MGD* 为 48.5±0.4）。类别级分析（Tab. 6）进一步揭示，ManifoldGD 在多个易混淆类别（如澳大利亚梗与边境梗）上表现更优，表明流形约束有助于保留更具判别力的类间边界。

**ImageNet-1k 全量数据集（Tab. 10）**：在极端低 IPC 设置下（IPC=1 和 50），ManifoldGD 以 ConvNet-6 评估仍优于 DiT 和 MGD。IPC=1 时达到 3.1±0.9（MGD* 为 2.8±0.9），IPC=50 时达到 12.7±0.4（MGD* 为 12.0±0.4），证明方法在大规模场景下的可扩展性。

**生成质量与分布匹配**：ManifoldGD 在 FID、代表性和多样性三个维度上均取得最优（Fig. 5）。以 ImageNette IPC=50 为例，FID 相比 MGD 下降约 15%，代表性（Rep）和多样性（Div）指标同步提升。ℓ₂ 距离和 MMD 分布距离（Fig. 4）显示 ManifoldGD 生成的合成分布更接近真实数据分布，而 DiT 在这两项指标上表现最差。

**定性对比**：Fig. 2 展示了 DiT、MGD 与 ManifoldGD 的生成样本。DiT 生成图像普遍模糊，MGD 虽能产生清晰图像但存在结构异常（如犬类腿部位置不自然、建筑结构扭曲），而 ManifoldGD 生成的样本在几何合理性和语义一致性上均有显著改善。Fig. 3 的去噪轨迹演变进一步揭示：在早期时间步（t > 25），模式引导捕获粗粒度语义结构；在后期阶段（t ≤ 20），流形约束细化几何与纹理细节，使 ManifoldGD 持续产出更锐利、语义更连贯的生成结果。

### 消融实验

**层次分裂聚类 vs. K-means（Tab. 3）**：在 ImageNette IPC=10 设置下，Divisive-levelwise 层次聚类相比 K-means 聚类提升约 1.5 个百分点准确率。Fig. 6 的 VAE 特征空间可视化揭示了原因：K-means 质心倾向于聚集在特征云的中心区域，而分裂层次聚类的多尺度质心同时覆盖均值附近和特征云的边界轮廓，凸包面积比更大，从而更完整地捕获类内分布。与凝聚层次聚类的对比（Fig. 9）表明，凝聚聚类质心偏向特征云边缘，而分裂聚类质心更接近均值，后者在多数设置下表现更优。

**流形引导的增益**：在层次聚类基础上引入流形校正 $g_{manifold}^t$ 后，性能进一步提升（Tab. 3），验证了切空间投影独立于聚类策略的附加价值。消融还表明，结合退火半径调度后达到最佳性能，三者形成互补。

**半径退火调度（Tab. 4）**：指数退火策略在所有评估设置下均优于固定半径、线性衰减和余弦衰减。这一结果支持了论文的理论直觉——早期较大半径容纳流形估计不确定性时的必要探索，后期逐步收紧强制几何约束。

**去噪终止步 $T_{STOP}$（Fig. 7-8）**：在总步数 50 的设置下，$T_{STOP}=25$ 时 FID 和准确率同时达到最优。Fig. 8 揭示了三个区域：增长区（< 20），流形引导持续改善生成质量；饱和区（20-30），性能保持稳定；下降区（> 30），过强的流形约束抑制了必要的模式内多样性。

**切空间维度 $d$（Tab. 9）**：$d=3$ 时 ConvNet-6 准确率最高，过高或过低的维度均导致轻微性能下降。这表明在 VAE 潜在空间中，局部流形的有效本征维度较低，过度参数化可能引入噪声。

**局部邻域半径 $r$（Tab. 7）**：半径选择需匹配数据集密度特征。ImageNette 偏好较小半径（0.05），而 ImageNet-100 偏好中等半径（0.1-0.2），反映了不同数据集在 VAE 特征空间中的聚散程度差异。

**核函数与调度器鲁棒性（Tab. 5, Tab. 8）**：ManifoldGD 在多种核函数（高斯核、拉普拉斯核等）下均保持优势，证明流形校正框架对具体亲和力度量不敏感。使用 DDIM 调度器时同样优于 MGD，表明方法对扩散采样器的选择具有鲁棒性。

**推理时间权衡（Fig. 11）**：ManifoldGD 的推理时间略高于 MGD 和 DiT，主要源于局部邻域构造与切空间估计的额外计算开销，但换取的准确率增益显著，在精度-效率曲线上占据优势位置。

### 失败模式与局限性

尽管整体表现优异，ManifoldGD 存在以下已知局限：

1. **高曲率流形区域**：局部切空间估计基于线性近似，当数据流形具有高曲率时（如类别边界急剧转折处），法向投影可能不完全准确，导致部分生成样本仍偏离流形。论文未提供曲率敏感性的定量分析，这一问题被列为未来工作。

2. **对预训练先验的依赖**：方法完全依赖预训练扩散模型和 VAE 的质量。若生成先验本身存在偏差（如某些类别在 VAE 潜在空间中表示不佳），流形引导难以完全补偿。ImageNet-1k IPC=1 的绝对准确率（3.1%）仍较低，说明极端压缩场景下信息瓶颈依然严峻。

3. **层次聚类起始层级的手动调节**：$s_{start}$ 参数需要根据数据集的类别重叠程度手动设置（Fig. 10）。ImageNette 等类别数少的数据集偏好较高起始层级，而 ImageNet-100 等类别数多的数据集偏好较低起始层级。缺乏自动选择机制限制了方法的即插即用性。

![[assets/figures/papers/paper_list_l2691_https_arxiv_org_abs_2602_23295/figures/016_Figure_10.jpg]]
*Figure 10: Ablation experiments to find out the level of divisivelayerwise clustering. It can be seen that for datasets with less class (ImageNette) the start level*

4. **推理开销**：相比 MGD，ManifoldGD 增加了局部邻域构造、前向扩散对齐和协方差估计步骤，在 IPC 较大或数据集规模增大时计算成本线性增长。论文未提供大规模场景下的详细效率分析。

5. **投影误差的形式化缺失**：当前工作未对法向投影的误差进行理论界定，也未分析投影误差如何随流形曲率和噪声水平变化。这使得流形校正的可靠性缺乏理论保证。

![[assets/figures/papers/paper_list_l2691_https_arxiv_org_abs_2602_23295/figures/004_Table_1.jpg]]
*Table 1: Performance comparison with state-of-the-art methods on ImageNet subsets, evaluated using the hard-label protocol. Results are based on ResNetAP-10 with average pooling, with the best performance highlighted in bold. Underlined results are the one where ManifoldGD outperforms training-based methods*

![[assets/figures/papers/paper_list_l2691_https_arxiv_org_abs_2602_23295/figures/006_Table_2.jpg]]
*Table 2: Performance comparison with state-of-the-art methods on ImageWoof, evaluated using the hard-label protocol. Results are based on ResNetAP-10, ConvNet-6 and ResNet-18 with average pooling, with the best performance highlighted in bold. Underlined results are the one where ManifoldGD outperforms training-based methods*

![[assets/figures/papers/paper_list_l2691_https_arxiv_org_abs_2602_23295/figures/007_Figure_5.jpg]]
*Figure 5: FID, Representativeness and Diversity comparison of DiT [31], MGD [37], and ManifoldGD. IPC 10,20, and 50 are used for ImageNet-100 and ImageNette. ManifoldGD achieves lower FID (% drop over MGD [37] marked above the bars), higher representativeness and diversity (R=representativeness, D=diversity, % increase over MGD [37] shown in the plot) across all settings*

![[assets/figures/papers/paper_list_l2691_https_arxiv_org_abs_2602_23295/figures/011_Figure_7.jpg]]
*Figure 7: Ablation of diffusion step t and corresponding*

![[assets/figures/papers/paper_list_l2691_https_arxiv_org_abs_2602_23295/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative samples generated by DiT [31], MGD [37], and ManifoldGD. The samples generated by ManifoldGD have better image structure and quality (eg. dog image of MGD is having legs in unusual position, dog image generated by DiT is blurry. Similarly, the buildings have uncommon structure for MGD. The ball image generated by DiT is of poor quality)*

## 定位与知识库关联

### 1. 与现有方法的谱系关系

ManifoldGD 处于**无训练扩散蒸馏**这一新兴分支，其直接前驱是 **MGD**（Mode-Guided Diffusion，无训练基线）。MGD 首次将数据集蒸馏从优化范式迁移到纯推理范式：利用预训练扩散模型的得分网络，将类别质心作为条件模式，通过欧几里得吸引引导生成过程。这一思路绕开了传统蒸馏方法（如 **DM**、**D4M**、**MinMaxDiff**）所需的昂贵内外循环训练，但暴露了一个深层瓶颈——**模式引导仅依赖欧几里得距离，完全忽略扩散流形的几何结构**。

ManifoldGD 的谱系定位可从三个维度理解：

- **相对于 MGD**：继承其无训练框架（预训练扩散模型 + IPC 质心引导），但将引导机制从纯欧几里得吸引升级为**流形一致的切向引导**。这是核心的因果扭结——通过局部估计扩散流形的切空间，将模式引导向量投影到切空间，消除法向分量，从而约束生成轨迹保持在数据流形上。这一改动在保持无训练优势的前提下，系统性地提升了生成样本的几何保真度和语义一致性。

- **相对于基于训练的方法**：**DM**（扩散模型数据集蒸馏）、**D4M**（基于扩散的微调方法）、**MinMaxDiff**（极小极大扩散方法）等依赖合成集上的训练循环来优化生成质量，计算开销大且对超参数敏感。ManifoldGD 以纯推理方式在多个 IPC 设置下达到甚至超越这些方法的性能（Tab. 1），证明了流形约束可以部分替代训练信号的监督作用。

- **相对于核集选择方法**：**Herding** 和 **IDC-1** 从真实数据中选择代表性样本，受限于原始数据的覆盖范围。ManifoldGD 通过扩散生成合成样本，具备超越真实数据分布的表达能力，同时通过流形约束保持生成样本的合理性。

### 2. 方法适用边界与局限

尽管 ManifoldGD 在多个基准上表现出色，其设计假设和实现选择划定了明确的适用边界：

**（1）对预训练生成先验的依赖。** 方法完全依赖预训练扩散模型和 VAE 的质量。若预训练模型在目标域上的生成能力不足，流形引导无法弥补基础先验的缺陷。这在 ImageNet-1k 的极端低 IPC（IPC=1）场景中表现为绝对准确率仍然较低（3.1±0.9），尽管相对 MGD 仍有提升（+0.3）。

**（2）线性切空间近似的局限性。** 流形校正的核心操作是将模式引导投影到局部切空间（Eq. (4)），这基于扩散流形在局部邻域内近似线性的假设。对于高曲率的复杂流形区域（如类别边界附近的尖锐转折），线性近似可能引入投影误差，导致生成样本偏离真实流形。论文明确指出这一局限，并将曲率敏感性的形式化分析列为未来工作。

**（3）层次聚类的起始层级需手动调节。** 分裂层次聚类的起始层级 `s_start` 影响 IPC 质心的多尺度覆盖质量。实验表明（Fig. 10），类别数较少的数据集（如 ImageNette）偏好较高的起始层级，而类别数较多的数据集（如 ImageNet-100）偏好较低的起始层级。当前需要根据数据集的类别重叠程度手动设置，缺乏自动选择机制。

**（4）邻域半径的敏感性与退火调度。** 局部流形估计的质量依赖于邻域半径 `r` 的选择（Tab. 7）：小半径（0.05）适合 ImageNette 的密集特征分布，中等半径（0.1-0.2）适合 ImageNet-100 的稀疏分布。指数退火调度（Tab. 4）提供了一种通用的缓解策略，但初始半径和衰减速率仍需针对数据集特性调整。

**（5）计算开销与推理时间的权衡。** 流形引导在每步去噪中引入局部几何估计（K 近邻协方差计算），增加了推理开销。Fig. 11 展示了推理时间与准确率的权衡：ManifoldGD 相比 MGD 和 DiT 在准确率上取得显著提升，但推理时间有所增加。对于实时或大规模蒸馏场景，这一开销需要纳入考量。

### 3. 开放问题

论文揭示了若干值得进一步探索的方向：

- **无标签条件下的自动层级选择**：当前 `s_start` 依赖数据集的类别重叠程度，如何在无标签或弱监督条件下自动确定最优起始层级，是走向全自动蒸馏的关键一步。

- **流形引导的跨模型泛化**：当前框架建立在扩散模型的基础上，利用其逐步去噪过程提供的自然流形结构。流形校正的思想——将引导向量投影到数据流形的切空间——理论上可推广到其他生成模型（如 GAN 的潜空间遍历），但需要重新设计局部几何估计机制。

- **与复杂条件生成的结合**：ManifoldGD 目前处理的是类别条件生成。将流形约束扩展到更复杂的条件场景（如文本到图像生成），需要解决条件信号与流形几何的联合建模问题——如何在语义引导和几何保真度之间建立统一的约束框架。

- **曲率感知的流形估计**：当前线性切空间近似在高曲率区域可能失效。引入曲率感知的局部几何估计（如基于黎曼度量的二阶近似）有望进一步提升生成样本的几何保真度，但会显著增加计算复杂度。

## 原文 PDF

![[paperPDFs/CVPR_2026/ManifoldGD_Training_Free_Hierarchical_Manifold_Guidance_for_Diffusion_Based_Dataset_Distillation.pdf]]
