---
title: Two in One Unified Multi Person Interactive Motion Generation by Latent Diffusion Transformer
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Two_in_One_Unified_Multi_Person_Interactive_Motion_Generation_by_Latent_Diffusion_Transformer.pdf
project_link: null
code_link: null
aliases:
- ITOUF
- TOUMPIMGBLDT
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将两人交互动作视为一个整体数据点，通过VAE压缩到统一潜在空间，并使用单个潜在扩散Transformer以文本条件生成整体动作序列。
primary_logic: 统一潜在空间能够保留完整的个体动作与交互信息，使得单个生成模型能够直接从同一文本条件中同时捕捉对称或非对称的复杂交互。
claims:
- 在InterHuman测试集上，InterLDM的R-Precision、FID、MM Dist和Diversity均全面超越所有基线方法。
- 定性可视化显示，InterLDM能正确生成非对称交互动作，而InterGen倾向于生成相似动作。
- InterLDM的生成速度比InterGen快约4倍，且生成质量更高。
- InterHuman test set 上 R Precision Top1 = 0.427±0.004
---

# Two in One Unified Multi Person Interactive Motion Generation by Latent Diffusion Transformer

> [!tip] 核心洞察
> 统一潜在空间能够保留完整的个体动作与交互信息，使得单个生成模型能够直接从同一文本条件中同时捕捉对称或非对称的复杂交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | 二合一：基于潜在扩散Transformer的统一多人交互动作生成 |
| 英文题名 | Two in One Unified Multi Person Interactive Motion Generation by Latent Diffusion Transformer |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2209.14916) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | InterLDM (Two-in-One Unified Framework) |
| Dataset | InterHuman test set |

> [!tip] 效果简介
> - InterHuman test set 上，R Precision Top1 0.427±0.004 vs 0.371±0.010 (InterGen) (+0.056)；FID 5.619±0.091 vs 5.918±0.079 (InterGen) (-0.299)；MM Dist 1.862±0.007 vs 5.108±0.014 (InterGen) (-3.246)。

## 概要

多人交互动作生成的核心瓶颈在于：现有方法（如 **InterGen**，Liang et al., IJCV 2024）将双人运动分离为两个独立分支建模，虽通过交叉注意力或通信模块进行交互，却从根本上割裂了个体动作与交互信息的完整性，导致非对称双人动作（如一人劈叉、另一人辅助下压）难以准确生成。

本文提出 **InterLDM（二合一统一框架）**，其核心洞察是：将双人交互动作视为一个整体数据点，通过交互变分自编码器（InterVAE）压缩至统一潜在空间，再由单个潜在扩散Transformer（DiT）以文本为条件直接生成完整动作序列。这一设计使得生成模型能够从同一文本条件中同时捕捉对称与非对称的复杂交互，从根本上避免了分支分离带来的信息丢失。

在 InterHuman 测试集上，InterLDM 全面超越所有基线方法：R-Precision Top1 达到 0.427（InterGen 为 0.371），FID 降至 5.619（InterGen 为 5.918），MM Dist 大幅降至 1.862（InterGen 为 5.108），Diversity 提升至 7.888（InterGen 为 7.387）。同时，得益于统一潜在空间的紧凑表示与 DPMSolver++ 快速采样器（25步去噪），InterLDM 的推理速度比 InterGen 快约 4 倍，在相同 Tesla A100 上实现了质量与效率的双重优势。定性可视化进一步验证，InterLDM 能正确生成非对称交互动作，而 InterGen 倾向于产生相似动作。

**局限与开放问题：** 当前框架仅支持双人交互，无法扩展至任意人数。相同文本条件下的生成多样性（MModality）低于 InterGen 等基线，可能限制同一指令下的动作变化。论文未讨论在极度不对称或复杂物理接触场景下的生成稳定性。如何将统一框架推广至任意人数的交互动作生成，是后续研究的关键方向。

### 问题背景

文本驱动的多人交互动作生成是计算机视觉与人机交互领域的关键任务，其目标是根据自然语言描述生成两个或多个角色之间的协调运动序列。该技术在虚拟现实、机器人规划、动画制作等场景中具有广泛的应用前景。与单人动作生成不同，多人交互动作生成面临独特的挑战：模型不仅要捕捉每个个体的运动模式，还必须建模角色之间的时空耦合关系，包括物理接触、空间协调与意图响应。

### 现有方法的瓶颈

当前主流的多人交互动作生成方法普遍采用**分离分支架构**。以最具代表性的工作**InterGen**（Liang et al., IJCV 2024）为例，该方法为每个个体分配独立的扩散生成分支，并通过交叉注意力模块实现分支间的信息交换。类似的思路也出现在**ComMDM**（Shafir et al., arXiv 2023）和**FreeMotion**（Fan et al., arXiv 2024）等工作中，前者依赖通信模块进行分支交互，后者则采用顺序生成策略。

这类分离式设计的根本性缺陷在于：**交互信息在建模过程中被结构性地割裂**。当两个个体的运动被分配到不同的潜在空间或生成分支时，模型难以完整保留交互的本质特征——尤其是非对称交互场景下，两个角色执行截然不同且相互依赖的动作（如一人做劈叉、另一人协助按压）。分离分支倾向于生成对称或相似的动作，导致交互的真实感和多样性受到严重制约。

### 核心动机与思路

针对上述瓶颈，本文提出一个根本性的视角转换：**将双人交互动作视为一个不可分割的整体数据点**。这一设计选择的关键因果逻辑在于：只有当交互对在统一的表示空间中作为一个整体被建模时，个体动作与交互信息的完整性才能得到天然保留。

基于这一动机，InterLDM框架采用两阶段方案：
- **阶段一**：通过交互变分自编码器（InterVAE）将拼接的双人运动序列压缩为统一的潜在表示 $z \in \mathcal{R}^{f \times 256}$，其中 $f$ 为压缩后的标记长度。
- **阶段二**：在统一潜在空间上训练单个潜在扩散Transformer（DiT），以文本条件直接生成完整的双人交互序列，从根本上避免了多分支架构带来的信息割裂问题。

这种“二合一”的统一框架使得单个生成模型能够从同一文本条件中同时捕捉对称或非对称的复杂交互，同时显著简化了模型结构——参数量的减少直接带来了约4倍的推理加速。

## 核心方法与创新机理

InterLDM 的核心创新在于**将双人交互动作视为一个不可分割的整体数据点**，通过统一的潜在空间和单一生成模型，从根本上改变了多人交互动作的建模范式。这一设计直接针对现有方法的瓶颈：分离式建模（如双分支扩散架构）在交互信息传递上存在结构性缺陷，难以捕捉非对称、强耦合的交互模式。

### 瓶颈与因果机制

**真实瓶颈**：现有方法（如 InterGen，Liang et al., IJCV 2024）将两个个体的运动分别编码到独立分支，再通过交叉注意力或通信模块进行交互。这种“先分离、后交互”的设计导致交互信息在编码阶段即被割裂，模型倾向于生成对称或相似的双人动作，在面对“一人做劈叉、另一人辅助下压”等非对称指令时表现不佳（见 Fig. 2）。

**因果旋钮**：InterLDM 将两人运动序列拼接为一个整体数据点，通过交互变分自编码器（InterVAE）压缩到统一的潜在空间 $z \in \mathcal{R}^{f \times 256}$，再由单个潜在扩散 Transformer（InterLDM DiT）以文本为条件直接生成完整的交互动作。统一潜在空间在压缩阶段即保留了完整的个体动作与交互信息，使得生成模型无需额外的分支间通信即可同时捕捉对称或非对称的复杂交互。

### 关键 Changed Slots

| 设计维度 | 基线方法（以 InterGen 为代表） | InterLDM 方案 | 证据锚点 |
|---------|-------------------------------|---------------|---------|
| **数据表示** | 对每个个体运动独立编码，各自一个分支 | 将两人运动作为一个整体数据点，通过 InterVAE 压缩为统一潜在序列 | “we propose treating two-person motions as a single data point and then employing a Variational AutoEncoder (VAE) to compress each data point into one latent space” |
| **生成架构** | 两个独立的扩散分支，通过交叉注意力交互 | 单个潜在扩散 Transformer（DiT），直接在统一潜在空间中基于文本条件生成完整双人交互 | “we propose learning a single diffusion generative network based on this unified latent space while using input text as condition to guide the entire two-person motions” |

这两个 changed slots 构成了“二合一”统一框架的核心：数据表示的统一消除了交互信息在编码阶段的损失，生成架构的统一则避免了多分支协调带来的复杂性和推理开销。

### 创新带来的性能增益

统一框架在 InterHuman 测试集上取得了全面的性能提升（Table I）：
- **R Precision Top1** 达到 0.427，较 InterGen 的 0.371 提升 +0.056，表明文本-动作匹配精度显著提高；
- **FID** 降至 5.619（InterGen 为 5.918），生成质量更优；
- **MM Dist** 从 5.108 大幅降至 1.862（−3.246），说明生成的动作分布与真实分布更为接近；
- **Diversity** 提升至 7.888（+0.501），生成的动作多样性更好。

在推理效率方面，统一框架同样带来显著优势。InterLDM 仅需单个 DiT 去噪器，配合 DPMSolver++ 调度器将去噪步数降至 25 步，在 Tesla A100 上的平均推理时间约为 InterGen 的 1/4（Fig. 3），同时参数量更少、FID 更低。

### 统一潜在空间的压缩率设计

InterVAE 的潜在标记长度 $f$ 是平衡压缩效率与生成质量的关键超参数。消融实验（Table II）表明，$f=24$ 达到最佳平衡点（FID=5.619，推理时间 0.487s）：更高的压缩率（更小的 $f$）虽能加速推理，但会损害重建质量；更低的压缩率则会导致生成性能下降。这一发现为统一潜在空间的设计提供了明确的工程指导。

### 局限与开放问题

当前框架仅支持双人交互，论文明确指出无法直接扩展到任意人数。此外，在相同文本条件下，InterLDM 的生成多样性指标（MModality）低于 InterGen 等基线，可能限制同一指令下的动作变化。如何将统一框架扩展到支持任意人数的交互动作生成，是论文提出的核心开放问题。

InterLDM 提出了一种“二合一”（Two-in-One）的统一生成框架，其核心设计在于将双人交互动作视为一个整体数据点，而非两个独立个体的运动之和。整个 pipeline 由三个关键阶段串联而成：**交互变分自编码器（InterVAE）压缩**、**文本条件编码** 和 **潜在扩散 Transformer（InterLDM）生成**。

### 1. 数据流与模块关系

**输入**：一段描述双人交互的文本（如“一人做劈叉，另一人协助下压”）和一段双人运动序列。

**阶段一：统一潜在压缩（InterVAE）**
框架首先将两人的运动数据拼接为一个整体数据点，送入交互变分自编码器。InterVAE 由一个 Transformer 编码器 $E$ 和一个 Transformer 解码器 $D$ 组成。编码器将拼接后的交互运动序列映射到低维潜在空间，输出潜在变量 $z \in \mathcal{R}^{f \times 256}$，其中 $f$ 为压缩后的标记长度，256 为特征维度。解码器则以潜在变量为条件，从零交互运动序列的头部开始重构完整的双人动作。这一设计确保了完整的个体动作信息与交互信息在压缩过程中得以保留，而非在分离分支中丢失。

**阶段二：文本条件编码**
文本描述被同时送入两个冻结的预训练文本编码器——**CLIP-ViT-L-14** 和 **T5-small**，分别提取词级和句子级特征，作为后续生成的条件信号。

**阶段三：潜在扩散生成（InterLDM）**
在推理时，随机采样的高斯噪声 $z_T$ 在统一的潜在空间中经过条件去噪过程逐步恢复为有意义的潜在表示 $z_0$。去噪器采用 **扩散 Transformer（DiT）** 架构，以文本条件 $c$ 和当前时间步 $t$ 为输入，预测添加的噪声 $\epsilon_\theta(z_t, t, c)$。训练目标为最小化预测噪声与真实噪声的 $L_2$ 距离：

$$L_{\mathrm{LDM}} = \mathbb{E}_{\epsilon, t, c \sim \mathcal{N}(0,1)} [||\epsilon - \epsilon_{\theta}(z_t, t, c)||_2^2]$$

**输出**：去噪后的潜在变量 $z_0$ 经 InterVAE 解码器重构为完整的双人交互运动序列。

### 2. 训练与推理策略

训练分为两个阶段。首先，InterVAE 在重构任务上预训练，其总损失函数为：

$$L_{\mathrm{VAE}} = L_{mse} + L_{kl} + L_{vel} + L_{bone} + L_{fc}$$

该损失结合了均方误差、KL 散度、速度损失、骨骼长度损失和脚部接触损失，以获取对高密度交互运动合理的低维潜在表示。随后，潜在扩散模型在该固定潜在空间上进行训练，去噪器采用无分类器引导（classifier-free guidance）方法，在训练时随机遮蔽 10% 的文本描述内容，以同时学习条件分布和无条件分布。

推理时，采用 **DPMSolver++** 作为噪声调度器，仅需 25 步去噪即可完成生成。无分类器引导的推理公式为：

$$\epsilon_{\theta}(z_t, t, c) = s \epsilon_{\theta}(z_t, t, c) + (1 - s) \epsilon_{\theta}(z_t, t, \emptyset)$$

其中引导尺度 $s$ 用于平衡生成多样性与文本保真度。去噪完成后，潜在变量经 InterVAE 解码器一次性重构为两人的完整交互动作序列。

### 3. 与双分支范式的关键区别

图 1（左）展示了 InterLDM 的统一框架，图 1（右）则对比了当时最优的双分支方法 **InterGen**（Liang et al., IJCV 2024）。InterGen 为每个个体分配独立的扩散分支，通过交叉注意力进行交互建模。这种分离设计倾向于生成对称或相似的双人动作，难以捕捉非对称的复杂交互。InterLDM 的单分支统一设计从根本上避免了这一问题——由于两人的运动在潜在空间中作为一个整体被建模和生成，交互信息在压缩和去噪全过程中始终保持耦合，使得模型能够从同一文本条件中同时捕捉对称或非对称的复杂交互模式。

![[assets/figures/papers/paper_list_l1673_Two_in_One_Unified_Multi_Person_Interactive_Motion_Generation_by_Latent/figures/001_Figure_1.jpg]]
*Figure 1: Left: Our proposed framework, which uses an interaction Variational AutoEncoder (InterVAE) to encode two-person motions into a unified latent space and uses a conditional interaction latent diffusio(InterLDM) generate the latents. Right: InterGen is the state-of-the-art work using two-branch framework with cross-attention interactions to generate motions*

InterLDM 的整体架构由两个核心模块串联构成：**交互变分自编码器（InterVAE）** 负责将双人交互动作压缩到统一潜在空间，**条件交互潜在扩散模型（InterLDM）** 在该潜在空间中基于文本条件生成完整的双人动作序列。

### 2.1 交互变分自编码器（InterVAE）

InterVAE 的核心设计思想是将两人运动视为一个整体数据点，而非两个独立个体的简单拼接。其结构由 Transformer 编码器 E 和解码器 D 组成：编码器将拼接后的两人运动序列映射为低维潜在变量 z，解码器则从 z 重构出完整的交互运动。

训练 InterVAE 的总损失函数为：

$$L_{\mathrm{VAE}} = L_{mse} + L_{kl} + L_{vel} + L_{bone} + L_{fc}.$$

其中各分量含义如下：
- **$L_{mse}$**：重构运动与原始运动之间的均方误差，保证运动轨迹的逐帧还原。
- **$L_{kl}$**：潜在分布与标准正态分布之间的 KL 散度，约束潜在空间的规整性。
- **$L_{vel}$**：速度损失，约束相邻帧之间的位移一致性，避免生成动作出现抖动。
- **$L_{bone}$**：骨骼长度损失，保证重构后人体各肢体的骨骼长度保持恒定，防止肢体拉伸畸变。
- **$L_{fc}$**：脚部接触损失，约束足部与地面的接触状态，提升动作的物理合理性。

潜在变量的维度为 $z \in \mathcal{R}^{f \times 256}$，其中 $f$ 为压缩后的标记长度，256 为特征维度。$f$ 的取值直接影响压缩率：较小的 $f$ 带来更快的推理速度，但可能损害重构质量；较大的 $f$ 保留更多细节，但会增加扩散模型的生成负担。

### 2.2 文本编码器

为了将文本条件引入生成过程，InterLDM 采用双编码器策略：
- **CLIP-ViT-L-14**：提取词级特征，捕捉细粒度语义信息。
- **T5-small**：提取句子级特征，提供全局语义上下文。

两个编码器在训练和推理过程中均保持冻结状态，其输出特征被拼接后作为条件信号 c 注入扩散去噪器。

### 2.3 条件交互潜在扩散模型（InterLDM）

InterLDM 在 InterVAE 构建的统一潜在空间中进行扩散与去噪。其核心是一个基于 **Diffusion Transformer（DiT）** 的去噪器，以文本条件 c 和时间步 t 为输入，预测添加到潜在变量 $z_t$ 上的噪声。

**前向扩散过程** 逐步向初始潜在变量 $z_0$ 添加高斯噪声：

$$q(z_t | z_{t-1}) = \mathcal{N}(\sqrt{\alpha}_t z_{t-1}, (1 - \alpha_t) I).$$

其中 $\alpha_t$ 为噪声调度参数，控制每步添加的噪声量。

**训练目标** 为最小化预测噪声与真实噪声之间的 L2 距离：

$$L_{\mathrm{LDM}} = \mathbb{E}_{\epsilon, t, c \sim \mathcal{N}(0,1)} [||\epsilon - \epsilon_{\theta}(z_t, t, c)||_2^2].$$

其中 $\epsilon$ 为真实采样的高斯噪声，$\epsilon_{\theta}$ 为 DiT 去噪器预测的噪声。

**推理阶段** 采用无分类器引导（classifier-free guidance），通过引导尺度 $s$ 平衡生成多样性与文本保真度：

$$\epsilon_{\theta}(z_t, t, c) = s \epsilon_{\theta}(z_t, t, c) + (1 - s) \epsilon_{\theta}(z_t, t, \emptyset).$$

训练时以 10% 的概率随机掩码文本描述内容，使模型同时学习条件分布与无条件分布。推理时通过调整 $s$，可在文本对齐度与动作多样性之间进行权衡。

为加速推理，InterLDM 采用 **DPMSolver++** 作为噪声调度器，将去噪步骤压缩至 25 步，在保持生成质量的同时显著降低计算开销。

### 2.4 训练与推理流程

整体训练分为两个阶段：
1. **第一阶段**：独立训练 InterVAE，优化重构任务，获得合理的低维潜在空间。
2. **第二阶段**：冻结 InterVAE，在潜在空间中训练 InterLDM 去噪器，学习文本条件与交互动作嵌入之间的映射关系。

推理时，给定文本描述，InterLDM 从随机噪声出发，经 25 步去噪生成潜在变量 $z_0$，再由 InterVAE 解码器重构为完整的双人交互动作序列。

## 实验与关键发现

### 主实验结果

InterLDM在InterHuman测试集上进行了全面的定量评估，与多个基线方法进行了对比，包括基于VAE的单人生成方法**TEMOS** (Petrovich et al., ECCV 2022)、文本到单一动作生成方法**T2M** (Lin et al., Autonomous Robots 2023)、基于通信的分离分支扩散方法**ComMDM** (Shafir et al., arXiv 2023)、统一框架的顺序生成方法**FreeMotion** (Fan et al., arXiv 2024)以及当前最优的双分支扩散方法**InterGen** (Liang et al., IJCV 2024)。所有方法均在相同的数据划分和预处理流程下训练，推理时间在相同Tesla A100 GPU上统一使用25步DPMSolver++调度器测量，评估指标沿用前人工作标准协议。

如Table I所示，InterLDM在所有关键指标上均取得了最优结果。具体而言：

- **R Precision Top1**达到0.427±0.004，相比InterGen的0.371±0.010提升了5.6个百分点，表明生成动作与文本描述之间具有更强的语义一致性。
- **FID**降至5.619±0.091，优于InterGen的5.918±0.079，说明生成动作的整体分布更接近真实数据分布。
- **MM Dist**大幅降至1.862±0.007，而InterGen为5.108±0.014，降幅达3.246，这反映了生成动作与对应文本在特征空间中的匹配度显著提升。
- **Diversity**达到7.888±0.041，高于InterGen的7.387±0.029，表明统一潜在空间保留了更丰富的动作变化。

在推理效率方面，InterLDM展现出显著优势。Figure 3的对比表明，InterLDM的生成速度比InterGen快约4倍，同时参数量更少、FID更低。这一效率提升源于两个关键设计：一是将两人运动压缩为统一潜在序列，避免了双分支架构的冗余计算；二是采用DPMSolver++调度器将去噪步数降至25步。

定性可视化结果（Figure 2）进一步验证了统一框架在非对称交互场景下的优势。在“一人做劈叉、另一人辅助下压”的文本条件下，InterLDM正确生成了两人截然不同的角色动作，而InterGen倾向于生成两人相似的对称动作。这印证了核心设计动机：将两人运动视为整体数据点进行统一建模，能够完整保留个体差异与交互信息。

![[assets/figures/papers/paper_list_l1673_Two_in_One_Unified_Multi_Person_Interactive_Motion_Generation_by_Latent/figures/004_Figure_2.jpg]]
*Figure 2: Visualization of generated interactive motions from InterGen [1] and Ours*

### 消融研究

Table II展示了潜在标记长度$f$（即压缩率）对重建质量和生成性能的影响。潜在变量维度为$z \in \mathcal{R}^{f \times 256}$，$f$越小表示压缩率越高。

实验结果表明，$f=24$达到了生成质量与推理速度的最佳平衡：FID为5.619，推理时间仅0.487秒。当$f$进一步减小（如$f=12$）时，虽然推理速度更快，但过高的压缩率损害了VAE的重建能力，导致生成质量下降；当$f$增大（如$f=48$）时，重建质量提升，但生成性能反而恶化，这可能是因为过长的潜在序列增加了扩散模型的建模难度。这一消融揭示了统一潜在空间中压缩率选择的非单调效应：适度的压缩既能保留充分的交互信息，又能为扩散模型提供易于学习的表示。

### 局限性与失败模式

尽管InterLDM在双人交互场景下取得了显著提升，但分析揭示了几个值得关注的局限性：

1. **人数扩展受限**：当前框架仅支持双人交互，无法直接扩展到任意人数场景。这是统一建模策略的固有约束——将多人运动作为整体数据点处理时，潜在空间的维度会随人数线性增长，使得VAE压缩和扩散建模的难度急剧上升。

2. **生成多样性不足**：在MModality指标上，InterLDM的表现低于InterGen等基线方法。这意味着在相同文本条件下，InterLDM倾向于生成较为一致的交互动作，可能限制了同一指令下的动作变化范围。这一现象可能与统一潜在空间的确定性编码方式有关。

3. **极端场景未验证**：论文未讨论在极度不对称或复杂物理接触（如摔跤、复杂舞蹈托举）场景下的生成稳定性。这些场景对交互建模的精度要求更高，统一框架在这些条件下的鲁棒性仍需进一步验证。

### 开放问题

作者明确指出，如何将该统一框架扩展到支持任意人数的交互动作生成是一个重要的开放问题。这需要解决潜在空间维度随人数增长的问题，可能需要引入图结构建模或分层压缩策略。

![[assets/figures/papers/paper_list_l1673_Two_in_One_Unified_Multi_Person_Interactive_Motion_Generation_by_Latent/figures/002_Table.jpg]]
*Table: I: QUANTITATIVE EVALUATION RESULTS ON THE INTERHUMAN TEST SET ± indicates the 95% confidence interval. Bold indicates best result*

![[assets/figures/papers/paper_list_l1673_Two_in_One_Unified_Multi_Person_Interactive_Motion_Generation_by_Latent/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of inference time, FID and quantity of parameter. All tests are performed on the same Tesla A100*

![[assets/figures/papers/paper_list_l1673_Two_in_One_Unified_Multi_Person_Interactive_Motion_Generation_by_Latent/figures/005_Table.jpg]]
*Table: II: Reconstruction and generation performance with different token length f*

## 定位与知识库关联

### 1. 问题瓶颈与核心思路

多人交互动作生成的核心瓶颈在于：现有方法普遍将多人动作分离为独立的个体分支进行建模，再通过额外的交互机制（如交叉注意力或通信模块）进行协调。这种分离式设计导致交互信息在分支间传递时存在丢失，尤其难以生成非对称的双人动作——例如一人劈叉、另一人辅助按压的场景。

InterLDM 的核心思路是将两人交互动作视为一个**不可分割的整体数据点**。通过交互变分自编码器（InterVAE）将拼接后的完整动作序列压缩到一个统一的潜在空间中，再使用单个潜在扩散 Transformer（DiT）直接从文本条件生成该整体潜在表示。这一设计的因果机制在于：统一潜在空间能够完整保留个体动作与交互信息的耦合关系，使得单个生成模型无需显式交互模块即可同时捕捉对称或非对称的复杂交互模式。

### 2. 与基线方法的关系定位

InterLDM 在方法谱系中处于从“分离建模”到“统一建模”的范式转换节点。以下梳理其与代表性基线方法的关系：

- **TEMOS**（Petrovich et al., ECCV 2022）与 **T2M**（Lin et al., Autonomous Robots 2023）：两者均为单人生成方法，分别基于 VAE 和扩散模型。InterLDM 继承了 VAE 压缩与扩散生成的两阶段框架，但将其从单人域扩展到双人统一域，核心差异在于数据表示从“单个运动序列”变为“拼接后的整体交互序列”。

- **ComMDM**（Shafir et al., arXiv 2023）：采用分离分支扩散加通信模块的架构。InterLDM 的对比点在于：ComMDM 通过显式通信弥补分支间的信息隔离，而 InterLDM 从数据表示层面消除了信息隔离的需求，因此无需通信模块。

- **FreeMotion**（Fan et al., arXiv 2024）：同样采用统一框架，但通过顺序生成的方式逐个生成人物动作。InterLDM 与 FreeMotion 的区别在于生成模式——前者是并行整体生成，后者是自回归顺序生成。并行整体生成在理论上更有利于保持全局交互一致性，但也限制了向任意人数的扩展能力。

- **InterGen**（Liang et al., IJCV 2024）：作为最直接的对比基线，InterGen 采用双分支扩散架构，通过交叉注意力实现分支间的交互。InterLDM 在 Table I 中全面超越 InterGen：R Precision Top1 提升 0.056（0.427 vs 0.371），FID 降低 0.299（5.619 vs 5.918），MM Dist 大幅降低 3.246（1.862 vs 5.108），Diversity 提升 0.501（7.888 vs 7.387）。此外，InterLDM 的推理速度约为 InterGen 的 4 倍（Fig. 3），参数量的效率也更高。

### 3. 适用边界与局限

**适用边界**：
- 当前框架仅针对双人交互设计，数据表示和潜在空间压缩均以两人为固定假设。
- 训练与评估均基于 InterHuman 数据集，该数据集以文本描述的双人交互动作为主，覆盖场景有限。
- 推理使用 DPMSolver++ 调度器，25 步去噪即可完成生成，在 Tesla A100 上单句推理时间约 0.487 秒（f=24 配置下）。

**已知局限**：
- **人数扩展受限**：论文明确指出当前框架无法扩展到任意人数，这是统一整体建模策略的固有代价——将 N 人动作拼接为一个数据点会导致潜在空间维度随人数线性增长，压缩难度和生成难度均会显著上升。
- **生成多样性不足**：在 MModality 指标上，InterLDM 的表现低于 InterGen 等基线方法。这意味着在相同文本条件下，InterLDM 倾向于生成更相似的动作变体，可能限制其在需要多样输出的交互场景中的应用。
- **极端场景未验证**：论文未讨论在极度不对称或复杂物理接触（如摔跤、托举等高精度接触依赖动作）场景下的生成稳定性，这些场景对交互一致性的要求远超数据集中的一般交互动作。

### 4. 开放问题

论文提出的核心开放问题是：**如何将该统一框架扩展到支持任意人数的交互动作生成？** 这一问题直接指向当前“整体数据点”策略的根本瓶颈。可能的解决方向包括：引入可伸缩的潜在编码机制（如基于图网络的条件压缩），或在保持统一生成的前提下解耦人数维度与潜在空间维度的刚性绑定。此外，如何在统一框架内提升生成多样性（MModality）也是值得探索的方向，可能与引导策略或潜在空间的结构化正则化相关。

## 原文 PDF

![[paperPDFs/arxiv_2024/Two_in_One_Unified_Multi_Person_Interactive_Motion_Generation_by_Latent_Diffusion_Transformer.pdf]]
