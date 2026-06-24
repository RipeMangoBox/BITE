---
title: Learning Surgical Robotic Manipulation with 3D Spatial Priors
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Surgical_Robotic_Manipulation_with_3D_Spatial_Priors.pdf
project_link: null
code_link: null
aliases:
- SSTS
- LSRM3SP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过从立体内窥镜图像中直接学习三维空间先验（端到端微调的几何变换器），并将其与机器人动作空间精确对齐，能够显著提升操作的成功率与泛化能力。
primary_logic: 利用大规模合成数据集Surgical3D微调一个强大的几何变换器（基于MASt3R），提取出富含三维几何线索的潜在嵌入；再通过一种轻量级的多级空间特征连接器（MSFC）将不同层次的嵌入高效融合，送入内窥镜中心策略解码器，从而使手术机器人仅凭标准立体视觉即可实现精准的仿人操作。
claims:
- SST在真实手术机器人的取钉、打结、胆囊解剖三个任务上均达到最优或可比肩现有最好方法的成功率。
- 在Surgical3D数据集上微调几何变换器是成功的关键：取消微调后，取钉任务的成功率从10/10骤降至2/10和0/10。
- 所提出的多级空间特征连接器（MSFC）显著优于仅使用最后一层特征或独立多层连接的设计。
- 微调后的几何变换器无需任务特定训练，即可从内窥镜图像中准确提取三维结构信息。
---

# Learning Surgical Robotic Manipulation with 3D Spatial Priors

> [!tip] 核心洞察
> 利用大规模合成数据集Surgical3D微调一个强大的几何变换器（基于MASt3R），提取出富含三维几何线索的潜在嵌入；再通过一种轻量级的多级空间特征连接器（MSFC）将不同层次的嵌入高效融合，送入内窥镜中心策略解码器，从而使手术机器人仅凭标准立体视觉即可实现精准的仿人操作。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于三维空间先验的手术机器人操作学习 |
| 英文题名 | Learning Surgical Robotic Manipulation with 3D Spatial Priors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.03798) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Spatial Surgical Transformer (SST) |
| Dataset | Peg Pickup, Knot Tying, Ex-vivo Gallbladder Dissection |

> [!tip] 效果简介
> - Peg Pickup (Test1) 上，Success Rate 10/10 vs SOTA (SRT/SRT-H) (优于)。
> - Peg Pickup (Test2) 上，Success Rate 8/10 vs SOTA (SRT/SRT-H) (优于)。
> - Knot Tying (Grasp) 上，Success Rate 10/10 vs SOTA (SRT/SRT-H) (优于或相当)。

## 概述

手术机器人操作面临一个根本性瓶颈：缺乏有效的三维空间感知能力。传统方法要么依赖显式三维重建——步骤繁琐、误差累积且无法端到端优化，要么借助临床不实用的腕部摄像头获取额外视角。更关键的是，手术场景的三维标注数据严重匮乏，使得策略难以推广到复杂多变的真实环境中。

本文提出 **Spatial Surgical Transformer (SST)**，一种端到端的视觉运动策略，通过从立体内窥镜图像中直接学习三维空间先验来赋予手术机器人空间智能。其核心思路是：利用大规模合成立体视觉数据集 **Surgical3D** 微调一个强大的几何变换器（基于 MASt3R），提取富含三维几何线索的潜在嵌入；再通过轻量级的 **多级空间特征连接器（MSFC）** 将不同层次的嵌入高效融合，送入以内窥镜坐标系为中心的策略解码器，从而仅凭标准立体视觉即可实现精准的仿人操作。

在真实手术机器人上，SST 在取钉、打结和离体胆囊解剖三个任务上均达到或超越了现有最优方法（如 **SRT** (Kim et al., arXiv 2024)、**SRT-H** (Kim et al., Science Robotics 2025)）的成功率。消融实验表明，在 Surgical3D 上微调几何变换器是成功的关键：取消微调后取钉任务成功率从 10/10 骤降至 2/10；所提出的 MSFC 设计也显著优于仅使用最后一层特征或独立多层连接器的方案。此外，微调后的几何变换器无需任务特定训练即可从内窥镜图像中准确提取三维结构信息，验证了空间先验学习的有效性。

## 背景与动机

### 手术机器人自主操作的核心瓶颈

让手术机器人在真实临床场景中自主完成精细操作，是医疗AI领域的长期目标。近年来，模仿学习在手术机器人操作中展现出巨大潜力，但其泛化能力始终受限于一个根本性问题：**缺乏有效的三维空间感知能力**。手术操作的本质是在三维空间中精确控制器械与组织的交互关系——抓取点的深度、缝合针的朝向、解剖层面的曲率，这些三维几何线索直接决定了动作的成败。

然而，现有方法在获取三维信息方面存在显著不足。传统方案通常依赖显式三维重建流程，从立体内窥镜图像中恢复组织表面几何，再将重建结果输入策略网络。这条路径存在三个致命缺陷：其一，重建步骤繁琐且误差会在流水线中逐级累积；其二，整个流程无法端到端优化，重建目标与操作目标之间存在天然鸿沟；其三，手术场景中纹理稀疏、镜面反射、组织变形等因素使得高质量三维重建本身就是一个未解决的难题。

另一类方法试图绕过三维重建，直接让策略从二维图像中隐式学习空间关系。例如，**SRT**（Surgical Robot Transformer, Kim et al., arXiv 2024）和 **SRT-H**（Kim et al., Science Robotics 2025）等端到端模仿学习策略虽然取得了进展，但它们通常需要依赖腕部摄像头（wrist-mounted camera）提供额外的近距离视角来弥补空间感知的不足。这种设置在临床实践中并不实用：腕部摄像头会占用宝贵的器械通道，增加系统复杂度，且在实际手术中难以部署。

### 三维标注数据的匮乏

更根本的制约在于数据层面。手术机器人领域的三维标注数据极度稀缺——获取真实手术场景的精确深度图或点云标注需要昂贵的设备和繁琐的标定流程，这导致大多数方法只能在少量二维标注数据上训练，难以学到鲁棒的三维空间表征。缺乏大规模、高质量的三维训练数据，是制约手术机器人空间智能发展的关键瓶颈。

### 本文的核心思路

本文的核心洞察是：**如果能让策略直接从立体内窥镜图像中提取出富含三维几何信息的潜在表征，并将其与机器人的动作空间精确对齐，就有可能在仅依赖标准立体视觉的条件下实现精准的仿人操作**。这意味着不需要显式重建完整的三维场景，也不需要额外的腕部摄像头，而是让策略“内化”三维空间理解能力。

为实现这一目标，本文提出 **Spatial Surgical Transformer (SST)**，其核心思路是两步走：首先，构建一个大规模合成立体视觉数据集（Surgical3D），利用其精确的三维标注来微调一个强大的几何变换器（基于MASt3R），使其学会从内窥镜图像中提取多尺度的三维潜在嵌入；然后，通过一个轻量级的多级空间特征连接器（MSFC）将这些嵌入高效融合，送入以内窥镜坐标系为中心的策略解码器，直接预测相对动作序列。这种设计使得三维空间先验的学习与操作策略的训练解耦但又协同——几何变换器负责“看懂”三维结构，策略解码器负责“用好”三维信息。

## 核心创新

SST的核心创新在于将**三维空间先验**系统性地引入手术机器人模仿学习，通过三个紧密耦合的Changed Slot解决了现有方法在空间感知上的根本缺陷。

### 瓶颈与因果机制

现有手术机器人策略（如**SRT** (Kim et al., arXiv 2024) 和 **SRT-H** (Kim et al., Science Robotics 2025)）通常依赖二维CNN编码内窥镜图像，缺乏对三维场景结构的显式理解。这迫使它们要么依赖临床不实用的腕部摄像头获取额外视角，要么进行繁琐的显式三维重建——后者步骤多、误差易累积且无法端到端优化。更深层的问题是：手术场景的三维标注数据极度匮乏，使得策略难以学习到可泛化的空间表征。

SST的因果调节器（Causal Knob）在于：**通过从立体内窥镜图像中直接学习三维空间先验，并将其与机器人动作空间精确对齐**。这一调节器通过三个Changed Slot的协同设计实现，每个Slot都针对特定瓶颈提供了解决方案。

### Changed Slot 1：从二维CNN到微调的几何变换器

**Slot名称**：视觉编码器

**Baseline**：二维CNN（如ResNet-18）或标准多视角编码器，仅提取二维外观特征，不含三维结构先验。

**Proposed**：在Surgical3D数据集上微调的MASt3R几何变换器，输出富含三维几何信息的潜在嵌入。

**创新本质**：这一替换是SST成功的基础。MASt3R本身是一个前馈三维重建模型，能从立体图像对中直接推断稠密三维点云，无需相机参数或特征匹配。但原始MASt3R在手术场景中表现不佳（Figure 3b）：无法重建手术器械（PSM）和器官表面。SST通过在**Surgical3D**——一个利用NVIDIA Omniverse构建的大规模合成立体视觉数据集——上对其进行微调，使几何变换器学会从内窥镜图像中提取手术场景特有的三维结构线索。消融实验（Table 2）提供了决定性证据：取消Surgical3D微调后，取钉任务的成功率从10/10骤降至2/10和0/10，证实了该Slot是性能的关键。

### Changed Slot 2：从单层特征到多级空间特征连接器（MSFC）

**Slot名称**：特征连接器

**Baseline**：仅使用几何变换器最后一层输出的特征连接器（Last-Layer Feature Connector, LFC）。

**Proposed**：多级空间特征连接器（MSFC），融合多个Transformer解码层的三维潜在嵌入，并与动作空间对齐。

**创新本质**：几何变换器的不同解码层编码了不同粒度的三维信息——浅层捕捉精细的局部几何细节，深层包含全局场景结构。MSFC通过将四个解码层的潜在嵌入分别投影到低维空间后沿特征维度拼接，再经MLP与动作特征空间对齐，实现了多尺度三维线索的高效融合。Table 3的消融表明，MSFC在所有任务上均显著优于LFC和独立多层连接器（MSC），验证了多级融合而非简单堆叠的重要性。

### Changed Slot 3：以内窥镜为中心的相对位姿动作空间

**Slot名称**：动作空间

**Baseline**：机器人关节空间或绝对末端执行器位姿。

**Proposed**：以内窥镜坐标系为中心的相对位姿动作空间，采用动作分块并施加指数衰减权重。

**创新本质**：这一设计将动作预测与视觉观测统一在同一坐标系下，使从几何变换器提取的三维空间先验能与动作空间自然对齐。相对位姿动作通过相邻帧末端执行器位姿的差异计算：平移直接相减，旋转转换为欧拉角以利于学习（Eq. 3）。动作分块策略（预测未来多步动作）配合指数衰减权重，提高了策略的时间一致性和执行稳定性。

### 创新协同效应

三个Changed Slot并非孤立改进，而是形成了一条完整的因果链：**Surgical3D微调的几何变换器**提供了可靠的三维空间先验来源；**MSFC**确保了这些多尺度三维信息被有效提取和压缩；**内窥镜中心动作空间**则使这些空间先验能直接指导动作生成。Figure 5的中间三维重建结果从定性角度佐证了这一点：微调后的几何变换器无需任务特定训练，即可从内窥镜图像中准确提取三维结构信息，为下游策略提供了坚实的空间基础。

## 整体框架

SST 的整体流水线分为两个阶段：**三维空间先验的获取**与**基于先验的策略学习**。

**第一阶段**在离线的 Surgical3D 合成数据集上，以三维重建为目标对几何变换器（基于 MASt3R 的 ViT-Large）进行微调，使其从立体内窥镜图像中学会提取富含三维几何线索的潜在嵌入。该阶段完成后，几何变换器的权重被冻结，不再参与后续策略训练的梯度更新。

**第二阶段**将冻结的几何变换器作为视觉骨干，接入策略学习流水线。立体内窥镜的左右视图分别经过几何变换器，各自输出多个解码层的潜在嵌入。这些多级嵌入随后进入**多级空间特征连接器（MSFC）**：先将各层嵌入投影到低维空间以保持紧凑性，再沿特征维度拼接，最后由一个 MLP 将其对齐到机器人动作特征空间。融合后的空间特征与机器人本体感知状态（如当前末端执行器位姿）一同送入**内窥镜中心策略解码器**——一个 12 层、隐藏维度 768 的 Transformer 解码器——预测以内窥镜坐标系为参考的相对动作序列。动作采用分块预测，并施加指数衰减权重以强调近期动作的精度。

整个框架的输入为立体内窥镜图像与本体感知状态，输出为左右手术器械的相对位姿动作，无需腕部摄像头、显式三维重建或外部跟踪设备。图 2 给出了完整的流水线示意。

### 补充图表

![[assets/figures/papers/paper_list_l2640_https_arxiv_org_abs_2603_03798/figures/001_Figure_1.jpg]]
*Figure 1: We present Spatial Surgical Transformer (SST), a visuomotor policy that empowers surgical robots with spatial intelligence through learned 3D spatial priors. The policy leverages a geometry transformer finetuned on the proposed Surgical3D Dataset to extract robust 3D latent embeddings from stereo endoscopic inputs, coupled with a multi-level spatial feature connector that integrates multi-level 3D latent embeddings capturing both fine-grained details and global context into the policy decoder. We implement SST on a real surgical robot equipped with a stereo endoscopic camera manipulator (ECM) and two patient-side manipulators (PSMs), and evaluate it across three distinct real-world surgical...*

![[assets/figures/papers/paper_list_l2640_https_arxiv_org_abs_2603_03798/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of Our Method. Top: The geometry transformer is first finetuned on the proposed Surgical3D dataset using a 3D reconstruction objective, enabling the extraction of robust 3D latent embeddings from endoscopic images. Bottom: The geometry transformer is then frozen, while the remaining components are trained to learn surgical manipulation policies with spatial priors from collected demonstrations. A multi-level spatial feature connector (MSFC) is trained to aggregate 3D latent embeddings from multiple geometry transformer blocks and aligns them with the robot’s action space. An endoscope-centric policy decoder generates relative robot actions in the endoscope frame, guided by the lear...*

## 核心模块与公式推导

### 3.1 几何变换器的微调目标

SST 的视觉前端是一个在 Surgical3D 数据集上微调的几何变换器（以 MASt3R 为原型）。微调的核心目标不是直接预测深度图，而是让网络从立体内窥镜图像中恢复尺度一致的稠密三维点云，并同时输出逐像素的置信度，以应对手术场景中纹理稀疏区域的不确定性。

为此，微调采用了两阶段损失函数。首先定义逐点的回归损失，对左右两个视点的有效像素域 $D^v$ 分别计算：

$$L_{reg}(v,i) = \sum_{v=\{1,2\}} \sum_{i \in D^v} \Vert \frac{1}{z} X_i^{v,1} - \frac{1}{\hat{z}} \hat{x}_i^{v,1} \Vert$$

其中 $X_i^{v,1}$ 与 $\hat{x}_i^{v,1}$ 分别表示真值与预测的三维点坐标，$z$ 与 $\hat{z}$ 为对应的尺度归一化因子，用于消除全局尺度歧义。该损失强制网络学习精确的相对几何结构。

在此基础上，引入置信度感知的联合训练目标：

$$L_{conf} = \sum_{v=\{1,2\}} \sum_{i \in D^v} C_i^{v,1} L_{reg}(v,i) - \alpha \log C^{v,1}$$

其中 $C_i^{v,1}$ 为网络预测的逐像素置信度，$\alpha$ 为平衡系数。该设计的因果机制在于：当某像素的回归误差较大时，网络可以通过降低其置信度 $C_i^{v,1}$ 来减小损失项 $C_i^{v,1} L_{reg}$，但正则项 $-\alpha \log C^{v,1}$ 会惩罚过低的置信度。二者博弈的结果是网络自动学会对纹理稀疏、几何模糊的区域赋予低置信度，而对结构清晰区域保持高置信度——这正是手术内窥镜场景下实现鲁棒三维感知的关键。

### 3.2 多级空间特征连接器（MSFC）

几何变换器微调完成后被冻结，其多个解码器层输出的潜在嵌入包含了不同粒度的三维几何信息：浅层保留更多局部细节，深层则编码全局上下文。MSFC 的设计目标是高效融合这些多级特征，并将其与机器人的动作空间对齐。

具体而言，MSFC 从几何变换器的四个解码器层分别提取潜在嵌入，各自通过一个轻量级投影头映射到低维空间以控制计算开销，随后沿特征维度拼接。拼接后的多级特征再经过一个 MLP 映射到与策略解码器兼容的动作特征空间。这一设计与两种替代方案的因果差异在消融实验中得到验证（Table 3）：

- **LFC（最后一层特征连接器）**：仅使用最后一层嵌入，丢失了浅层的细粒度几何线索，导致操作精度下降。
- **MSC（多层分离连接器）**：对每一层独立处理后再融合，缺乏跨层信息的直接交互，特征整合效率低于 MSFC。

MSFC 的关键优势在于“先投影、再拼接、后对齐”的紧凑流水线，使得不同抽象层次的三维空间先验能够在统一的特征空间中协同作用于动作预测。

### 3.3 内窥镜中心的相对位姿动作空间

SST 的动作表示以内窥镜坐标系为参考，采用相邻帧末端执行器位姿之间的相对变换：

$$a_{t} = \{ E_{t+1}^{i} \ominus E_{t}^{i} \} = \{ (tr_{t+1}^{i} - tr_{t}^{i}, (R_{t}^{i})^{T} R_{t+1}^{i}) \}, i \in \{left, right\}$$

其中 $E_t^i$ 表示第 $i$ 个机械臂在时刻 $t$ 的末端执行器位姿（属于 SE(3)），$tr$ 为平移分量，$R$ 为旋转矩阵。平移部分直接做向量差，旋转部分则通过矩阵乘法得到相对旋转并转换为欧拉角表示，以降低学习难度。

选择内窥镜中心动作空间而非机器人基座坐标系，其因果逻辑在于：手术操作中，内窥镜视角与手术区域的关系相对稳定，以内窥镜为参考的动作表示自然具备对相机位姿变化的鲁棒性。此外，策略采用动作分块（action chunking）预测未来多步动作序列，并对预测序列施加指数衰减权重，使近期动作获得更高的优化优先级。

策略训练使用标准的均方误差损失：

$$L_{MSE} = MSE(\hat{a}_{t}, \pi_{\theta}(o_{t}, x_{t}))$$

其中 $\pi_{\theta}$ 为参数化的策略网络，$o_t$ 为立体内窥镜观测，$x_t$ 为机器人本体感知状态（关节角度等），$\hat{a}_{t}$ 为从演示数据中提取的真值相对动作。整个策略解码器由 12 层 Transformer 解码器层构成（隐藏维度 768），以几何变换器冻结后的潜在嵌入作为交叉注意力的键值对输入。

### 补充图表

![[assets/figures/papers/paper_list_l2640_https_arxiv_org_abs_2603_03798/figures/003_Figure_3.jpg]]
*Figure 3: Left: Samples from our Surgical3D dataset. We utilize diverse 3D surgical assets to generate highly realistic and varied synthetic surgical scenes. Right: The figure illustrates the reconstruction results from MASt3R under three finetuning configurations. (a) One example of a stereo endoscopic image captured in a real in-vivo surgical scene, used as input. (b) The original MASt3R fails to reconstruct both the patient-side manipulator (PSM) and the organ surface. (c) When finetuned solely on synthetic data, the organ reconstruction remains coarse and the PSM geometry is still incomplete. (d) When finetuned on a combination of synthetic and real data, the model achieves more accurate reconstr...*

![[assets/figures/papers/paper_list_l2640_https_arxiv_org_abs_2603_03798/figures/009_Figure_6.jpg]]
*Figure 6: Alternative Designs of Spatial Connectors. (a) Last-Layer Feature Connector. (b) Multi-Layer Separate Connector*

## 实验与分析

### 主实验结果

我们在三组真实手术机器人任务上评估了SST：取钉（Peg Pickup）、打结（Knot Tying）和离体胆囊解剖（Ex-vivo Gallbladder Dissection）。为公平比较，所有方法均采用相同的动作分块变换器解码器与相对位姿动作空间进行重新实现或对齐。

Table 1 报告了各方法的成功率对比。SST在所有任务上均达到或超越了现有最优方法：

- **取钉任务**：SST在Test1区域取得10/10成功率，在Test2区域取得8/10，显著优于依赖腕部摄像头的**SRT**（Kim et al., arXiv 2024）和**SRT-H**（Kim et al., Science Robotics 2025）。值得注意的是，SST仅使用标准立体内窥镜图像，无需额外视角。
- **打结任务**：在抓取子任务上达到10/10，环绕子任务和完整任务均为7/10，与最优基线相当或更优。
- **胆囊解剖任务**：抓取子任务10/10，解剖子任务和完整任务均为6/10，在仅依赖内窥镜图像的条件下保持了稳定表现。

关键结论是：SST仅凭标准立体内窥镜输入即可达到与依赖腕部摄像头的方法相当甚至更优的性能，证明了从图像中直接学习三维空间先验的有效性。

### 消融实验

#### 几何变换器微调的关键作用

Table 2 展示了在Surgical3D数据集上微调几何变换器的决定性影响。以MASt3R为骨干，取消微调（w/o ToS）后，取钉Test1的成功率从10/10骤降至2/10；若进一步将预训练权重替换为DINOv2初始化（w/o ToS & w/o MASt3R），成功率降至0/10。这表明：
1. 手术场景的三维结构信息无法从通用预训练权重中自动迁移获得；
2. 在Surgical3D上的微调是赋予几何变换器手术场景空间感知能力的瓶颈环节。

![[assets/figures/papers/paper_list_l2640_https_arxiv_org_abs_2603_03798/figures/007_Table_2.jpg]]
*Table 2: Effectiveness of Finetuning Geometry Transformer on Surgical3D Dataset. “ToS” indicates that the geometry transformer was trained on the Surgical3D dataset*

#### 多级空间特征连接器的设计选择

Table 3 对比了三种空间连接器架构（参见Figure 6）：
- **LFC**（Last-Layer Feature Connector）：仅使用几何变换器最后一层解码器的输出嵌入；
- **MSC**（Multi-Layer Separate Connector）：独立处理各层嵌入后拼接；
- **MSFC**（Multi-Level Spatial Feature Connector，本文方案）：将四层解码器嵌入投影至低维空间后沿特征维度拼接，再通过MLP与动作空间对齐。

![[assets/figures/papers/paper_list_l2640_https_arxiv_org_abs_2603_03798/figures/008_Table_3.jpg]]
*Table 3: Effectiveness of Multi-Level Spatial Feature Connector. LFC: Last-Layer Feature Connector; MSC: Multi-Layer Separate Connector. MSFC: Multi-Level Spatial Feature Connector*

MSFC在所有任务上均取得最高成功率。LFC因丢失了浅层细粒度几何线索而性能显著下降；MSC虽融合了多层特征，但独立处理各层导致特征交互不足，效果仍逊于MSFC。这验证了多层次三维潜在嵌入的高效融合是连接几何先验与动作策略的关键设计。

#### 几何变换器骨干选择

在推理效率与任务性能的权衡中，MASt3R（推理延迟56.2ms）优于VGGT（140.4ms），在保持竞争力的同时满足手术机器人的实时性要求。

### 中间三维重建的定性分析

Figure 5 展示了微调后的几何变换器在不同任务步骤中生成的中间三维重建结果。通过将潜在嵌入输入DPT头进行解码，可以观察到模型无需任务特定训练即可从当前内窥镜观测中提取出清晰的三维结构线索，包括手术器械的位姿和器官表面的几何形态。这为策略解码器提供了可解释的空间先验，解释了SST在复杂操作中保持稳定表现的原因。

![[assets/figures/papers/paper_list_l2640_https_arxiv_org_abs_2603_03798/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative Results of Intermediate 3D Reconstruction. Subscripts at the lower left of each image indicate the manipulation step. Tokens from the finetuned geometry transformer are fed into DPT heads to generate intermediate 3D reconstructions. The results demonstrate that the geometry transformer effectively extracts 3D cues from current endoscopic observations across various test tasks without task-specific training. More details are provided in the supplementary videos*

### 失败模式与局限性

尽管SST在多数任务上表现优异，但在胆囊解剖完整任务中成功率仅为6/10，表明在长时序、多阶段操作中仍存在改进空间。当前分析未提供具体的失败案例统计，该点需要人工验证。可能的瓶颈包括：
- 组织变形带来的视觉分布偏移；
- 长任务中误差累积效应；
- 合成数据与真实组织纹理之间的域间隙。

此外，本文未报告在活体场景下的评估结果，离体实验到临床部署的泛化能力仍需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2640_https_arxiv_org_abs_2603_03798/figures/005_Figure.jpg]]
*Figure: (a) Peg Pickup (b) Knot Tying (c) Ex-vivo Gallbladder Dissection*

![[assets/figures/papers/paper_list_l2640_https_arxiv_org_abs_2603_03798/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of Experimental Settings. Yellow and blue arrows denote the approximate motion directions of the right and left arms, respectively. Top: Peg pickup task. A total of 180 trajectories were collected, with roughly 120 in the green region and 60 in the blue region for training. Test1 and Test2 correspond to evaluations in these respective areas. Middle: Knot tying task. The suture tail was randomly positioned within the blue region during data collection, and evaluations were performed under the same condition. (b1) and (b3) show the grasping and looping actions. Bottom: Ex-vivo gallbladder dissection task. Grasp points on the gallbladder were sampled from varying positions within...*

## 方法谱系与知识库定位

### 1. 与现有手术机器人策略的关系

SST 直接对标的是当前手术机器人模仿学习领域的两项代表性工作：**SRT**（Kim et al., arXiv 2024）和 **SRT-H**（Kim et al., Science Robotics 2025）。这两者代表了手术机器人端到端策略的不同设计取向——SRT 采用标准的视觉编码器（如 ResNet-18）配合动作分块 Transformer 解码器，而 SRT-H 进一步引入语言条件的分层模仿学习。然而，它们的共同瓶颈在于**视觉编码器缺乏三维空间感知能力**：SRT 依赖临床难以部署的腕部摄像头来补偿视角不足，而 SRT-H 虽然通过语言条件增强了任务泛化，但其二维 CNN 编码器本质上仍无法从标准立体内窥镜图像中提取可靠的三维几何线索。

SST 的突破点在于**将三维空间先验从“显式重建”或“额外传感器”的路径中解放出来**。传统手术机器人获取三维信息的方式主要有两条：一是通过显式三维重建流程（特征匹配、深度估计、点云融合），步骤繁琐且误差逐级累积，无法端到端优化；二是依赖腕部摄像头提供额外视角，但这在临床场景中并不实用。SST 选择了一条不同的路径：通过在大规模合成立体数据集 Surgical3D 上微调几何变换器 MASt3R，使视觉编码器能够**隐式地**从立体内窥镜图像中提取富含三维几何线索的潜在嵌入，无需显式重建即可为下游策略提供空间感知能力。

### 2. 方法谱系中的定位

从技术栈的角度，SST 处于**三维视觉基础模型**与**机器人模仿学习**的交叉地带。

在三维视觉侧，SST 的核心组件——几何变换器——建立在 MASt3R 这一前馈式三维重建模型之上。MASt3R 本身代表了从“特征匹配+优化”范式向“端到端前馈推理”范式的转变：它无需相机参数或显式特征匹配，直接从图像对中推断稠密三维点云。SST 的关键创新在于**将这一重建导向的模型重新定位为空间特征提取器**：通过在 Surgical3D 数据集上微调，几何变换器学会了提取对手术场景具有判别力的三维潜在嵌入，而非仅仅输出点云坐标。这种“预训练-微调-冻结”的使用模式与当前视觉-语言模型（VLM）在机器人领域的应用范式高度一致。

在模仿学习侧，SST 继承了 Action Chunking Transformer（ACT）的动作分块思想，但做了两项关键适配：(1) **动作空间以内窥镜坐标系为中心**，采用相邻帧末端执行器位姿的相对差 $a_{t} = \{ E_{t+1}^{i} \ominus E_{t}^{i} \}$ 作为动作表示，平移直接相减、旋转转换为欧拉角，这比绝对位姿或关节空间动作更适合视觉伺服；(2) **多级空间特征连接器（MSFC）** 的设计表明，简单地将几何变换器的最后一层输出送入策略解码器是次优的——同时融合多个解码器层的潜在嵌入（从细粒度局部几何到全局上下文）才能最大化三维先验的利用效率。

### 3. 适用边界与关键假设

SST 的有效性建立在以下几个关键假设之上，这些假设也划定了其当前的适用边界：

- **立体内窥镜输入的可用性**：SST 假设输入为标定好的立体图像对。尽管立体内窥镜在机器人手术中日益普及，但单目内窥镜场景仍需额外的深度估计模块或领域自适应策略。
- **Surgical3D 数据集对真实场景的覆盖度**：消融实验（Table 2）表明，在 Surgical3D 上的微调是成功的关键——取消微调后取钉任务成功率从 10/10 骤降至 2/10 甚至 0/10。这意味着 SST 的性能高度依赖于合成数据的质量和多样性。如果目标手术场景中的器械类型、组织外观或光照条件与 Surgical3D 的分布差异过大，几何变换器提取的空间先验可能退化。
- **模仿学习的演示依赖性**：SST 的策略解码器仍需从专家演示中学习。对于需要精细力控的任务（如缝合时的张力调节），纯位置控制的模仿学习可能存在根本性局限。
- **推理延迟的权衡**：MASt3R 作为几何变换器在推理延迟（56.2ms）与任务性能之间取得了平衡，优于 VGGT（140.4ms），但对于需要更高控制频率的任务，这一延迟仍需进一步压缩。

### 4. 局限与开放问题

尽管 SST 在三个真实手术任务上取得了最优或可比肩 SOTA 的成功率，论文中仍存在若干值得关注的局限和开放问题：

- **力反馈的缺失**：当前 SST 的动作空间仅包含末端执行器的位姿变化，未涉及力/力矩信息。在打结和胆囊解剖等需要精细组织操作的场景中，纯位置控制可能导致组织损伤或任务失败。如何将三维空间先验与力觉感知融合，是一个重要的扩展方向。
- **动态场景的鲁棒性**：SST 在准静态手术场景中表现优异，但真实手术中常涉及组织变形、出血、烟雾等动态干扰。几何变换器在这些条件下的三维嵌入质量如何变化，论文未给出系统性评估。
- **从合成到真实的泛化上限**：Figure 3 的定性结果显示，仅在合成数据上微调的几何变换器对真实场景的器官重建仍较粗糙，混合真实数据后才显著改善。这暗示 Surgical3D 的域间隙尚未完全弥合，更大规模、更多样化的真实手术数据收集可能是进一步提升泛化能力的必要条件。
- **与基础模型的进一步整合**：SST 目前将三维空间先验与动作预测直接耦合。一个值得探索的方向是将几何变换器提取的空间嵌入与手术语言模型（如手术报告生成、指令理解）结合，实现语言引导的空间推理——这与 SRT-H 的语言条件模仿学习形成互补而非替代关系。

## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Surgical_Robotic_Manipulation_with_3D_Spatial_Priors.pdf]]