---
title: "InterGen: Diffusion-based Multi-human Motion Generation under Complex Interactions"
type: paper
paper_level: A
venue: IJCV
year: 2024
pdf_ref: paperPDFs/IJCV_2024/InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Interactions.pdf
code_link: null
project_link: https://tr3e.github.io/intergen-page
aliases:
- InterGen
tags:
- IJCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入合作去噪网络（权重共享+互注意力机制）并结合非规范世界坐标系表示与带阻尼调度的交互正则化损失（距离图损失和相对朝向损失），有效编码并保留双人空间关系且平衡运动能力。
primary_logic: 两人交互在交换身份后语义不变，基于此对称性可采用共享权重的合作去噪网络，同时在世界坐标系直接表示全局轨迹避免了累计漂移，并通过空间交互损失显式约束相对位置与朝向。
claims:
- InterGen在InterHuman测试集上取得最优R Precision Top1 0.371、FID 5.918，显著超越所有基线
- 消融实验：移除权重共享使Top1 R Precision从0.371降至0.153，FID从5.918升至8.059
- 消融实验：移除距离图（DM）损失使Top1降至0.293，FID升至6.653
- 消融实验：移除相对朝向（RO）损失使Top1降至0.310，FID升至6.311
---

# InterGen: Diffusion-based Multi-human Motion Generation under Complex Interactions

> [!tip] 核心洞察
> 两人交互在交换身份后语义不变，基于此对称性可采用共享权重的合作去噪网络，同时在世界坐标系直接表示全局轨迹避免了累计漂移，并通过空间交互损失显式约束相对位置与朝向。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterGen: 基于扩散模型的复杂交互双人运动生成 |
| 英文题名 | InterGen: Diffusion-based Multi-human Motion Generation under Complex Interactions |
| 会议/期刊 | IJCV 2024 |
| Links |  [Project](https://tr3e.github.io/intergen-page)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | InterGen |
| Dataset | InterHuman test set |

> [!tip] 效果简介
> - InterHuman test set 上，R Precision Top1 0.371 vs see Table 2 (best baseline lower) (best)；FID 5.918 vs see Table 2 (best baseline higher) (best)；MM Dist 5.108 vs see Table 2 (best baseline higher) (best)。

## 概要

### 问题瓶颈

现有文本驱动的人体运动生成研究主要聚焦于单人场景，其模型与数据集均无法有效建模双人交互中的两个核心挑战：**空间关系编码**与**运动能力对称性**。具体而言，传统规范表示将关节位置与速度变换至根坐标系，导致两人之间的全局空间关系（如相对距离、朝向）在表示层面被破坏；同时，独立或非共享的去噪架构忽略了“两人交互在交换身份后语义不变”这一基本对称性，导致生成结果缺乏真实交互性，容易产生漂移与模式坍塌。

### 核心方法

**InterGen** 通过三个关键技术设计解决上述瓶颈：

1. **非规范运动表示**：直接在世界坐标系中记录全局关节位置与速度，避免坐标变换带来的空间信息丢失与累计积分漂移。
2. **合作去噪网络**：采用两个权重共享的Transformer去噪器，并通过互注意力机制进行信息交换。其理论基础是双人交互分布的身份交换对称性 $p(\mathbf{x}_a, \mathbf{x}_b) \equiv p(\mathbf{x}_b, \mathbf{x}_a)$，共享权重使网络天然保持该对称性。
3. **交互正则化损失与阻尼调度**：引入掩码关节距离图损失（DM loss）约束空间干涉、相对朝向损失（RO loss）约束正面朝向关系，并仅在扩散时间步低于阈值时施加正则化，在高噪声阶段保留生成多样性。

### 主要结果

在InterHuman测试集上，InterGen取得最优性能：**R Precision Top1 0.371**、**FID 5.918**、**MM Dist 5.108**，显著超越所有基线方法（TEMOS、T2M、MDM及ComMDM）。消融实验进一步验证了各设计的决定性作用——移除权重共享使Top1 R Precision从0.371骤降至0.153，FID从5.918升至8.059；移除DM损失和RO损失也分别导致指标明显恶化，证实了空间约束对真实交互生成不可或缺。

### 方法定位

在方法谱系中，InterGen属于**基于扩散模型的文本驱动多人生成**范式。相较于单人生成基线（如MDM（Tevet et al., ICLR 2023）、T2M（Guo et al., CVPR 2022）、TEMOS（Petrovich et al., ECCV 2022））和基于MDM微调的双人基线ComMDM（Shafir et al., 2023），InterGen的核心区分点在于：以共享权重的合作架构显式建模交互对称性，以世界坐标系表示直接保留空间关系，并以物理启发的交互损失进行结构化约束。该方法同时支持人-人生成、轨迹控制与交互中间帧生成等扩展应用。



### 问题背景：从单人运动到双人交互的生成鸿沟

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列。近年来，基于扩散模型（diffusion models）的单人运动生成取得了显著进展，代表性工作包括 **MDM**（Tevet et al., ICLR 2023）、**T2M**（Guo et al., CVPR 2022）和 **TEMOS**（Petrovich et al., ECCV 2022）。这些方法在单人场景下能够生成高质量、多样化的运动，但当任务扩展到双人交互时，面临根本性的困难。

核心瓶颈在于：**现有单人生成模型与数据集无法建模双人交互中的空间关系与运动能力对称性**。具体表现为两个层面的缺失：

1. **空间关系建模缺失**：单人模型仅关注个体运动学，缺乏对两人之间相对位置、距离、朝向等空间约束的显式编码。当简单地将单人模型独立应用于两个人物时，生成的运动会缺乏真实的交互性——两人可能穿透彼此、朝向错误、或运动节奏完全不协调。

2. **运动能力对称性缺失**：两人交互存在天然的对称性——交换两人身份后，交互语义保持不变（例如“A拥抱B”与“B拥抱A”在运动层面是对称的）。然而，独立建模两个人物会破坏这种对称性，导致生成结果出现漂移与模式坍塌（mode collapse）。

### 现有方法的局限

直接沿用单人生成范式处理双人交互存在以下具体缺陷：

- **表示层面的不足**：传统方法采用规范表示（canonical representation），将关节位置和速度相对于根关节坐标系进行变换。这种表示丢弃了全局世界坐标系中的空间关系信息，使得两人之间的相对位置需要事后推断，容易产生累积漂移。
- **架构层面的不足**：现有扩散模型使用单一去噪网络，缺乏对双人运动联合分布的结构化建模。即使将两个独立的去噪器组合使用，由于权重不共享，也无法保证交换对称性。
- **监督信号的不足**：仅使用简单的扩散损失（$\mathcal{L}_{simple}$）无法显式约束两人的空间交互关系，导致生成的交互动作缺乏物理合理性。

此外，**数据层面同样存在瓶颈**：现有运动数据集（如HumanML3D、KIT）主要包含单人运动，缺乏大规模、高质量的双人交互动作捕捉数据，限制了模型的学习能力。

### 本文动机与核心思路

针对上述挑战，InterGen 提出了一套系统性的解决方案，其核心洞察在于：**两人交互在交换身份后语义不变，基于此对称性可采用共享权重的合作去噪网络**。具体而言，本文从三个层面突破现有方法的局限：

- **非规范运动表示**：直接在世界坐标系中表示全局关节位置和速度，显式保留两人的空间关系，避免规范表示带来的累积积分漂移。
- **合作去噪架构**：设计两个共享权重的Transformer去噪器，通过互注意力机制（mutual attention）实现信息交互，天然满足交互对称性 $p(\mathbf{x}_a, \mathbf{x}_b) \equiv p(\mathbf{x}_b, \mathbf{x}_a)$。
- **交互正则化损失**：引入掩码关节距离图损失（DM loss）和相对朝向损失（RO loss），在扩散去噪的低噪声阶段显式约束两人的空间干涉和正面朝向关系，并采用截断式调度（truncated schedule）避免高噪声阶段的错误约束。

通过上述设计，InterGen 首次实现了基于扩散模型的高质量双人交互运动生成，在定量指标和定性效果上均显著超越现有基线方法。



## 核心方法与创新机理

InterGen 的核心创新在于首次将双人交互生成建模为一个**对称合作扩散过程**，通过三个相互耦合的 changed slots 突破现有方法的瓶颈。

### 1. 非规范世界坐标系运动表示

现有单人生成模型（如 **MDM** (Tevet et al., ICLR 2023)、**T2M** (Guo et al., CVPR 2022)）普遍采用规范表示——将关节位置和速度变换到根节点局部坐标系。这种做法在单人生成中可行，但在双人交互场景下会**丢失两人之间的全局空间关系**，且根轨迹的累积积分漂移会随时间放大误差。

InterGen 提出**非规范表示**，直接在世界坐标系中编码全局关节位置和速度：

$$x^{i} = [\mathbf{j}_{g}^{p}, \mathbf{j}_{g}^{v}, \mathbf{j}^{r}, \mathbf{c}^{f}]$$

其中 $\mathbf{j}_{g}^{p}$ 和 $\mathbf{j}_{g}^{v}$ 分别是世界坐标系下的关节位置和速度，$\mathbf{j}^{r}$ 为局部旋转，$\mathbf{c}^{f}$ 为脚部接触特征。这一表示**显式保留了两人在同一世界坐标系中的绝对轨迹和空间关系**，从根本上避免了漂移问题。

消融实验证实，将非规范表示替换回规范表示会导致性能显著恶化（Table 3），验证了全局世界坐标系信息对多人生成的关键作用。

### 2. 权重共享的合作去噪网络

双人交互存在一个关键对称性：**交换两人身份后，交互语义保持不变**，即 $p(\mathbf{x}_{a}, \mathbf{x}_{b}) \equiv p(\mathbf{x}_{b}, \mathbf{x}_{a})$（Eq. 5）。

基于此洞察，InterGen 设计了两套**共享全部权重的合作 Transformer 去噪器**，并通过**互注意力机制**使两个去噪过程相互感知。合作去噪损失为：

$$\mathcal{L}_{simple} = \mathbb{E}_{\mathbf{x}, t, \epsilon}[\lambda_{t}||\mathbf{x}_{a} - D_{\theta}(\mathbf{x}_{a}+\sigma_{t}\epsilon_{a}, \mathbf{x}_{b}+\sigma_{t}\epsilon_{b}, t, c)||_{2}^{2} + \lambda_{t}||\mathbf{x}_{b} - D_{\theta}(\mathbf{x}_{b}+\sigma_{t}\epsilon_{b}, \mathbf{x}_{a}+\sigma_{t}\epsilon_{a}, t, c)||_{2}^{2}]$$

这与基线方法形成鲜明对比：**ComMDM** (Shafir et al., 2023) 仅对 MDM 进行微调，缺乏专门的交互架构；单人去噪器独立运行则无法建模两人运动能力对称性。

消融实验提供了决定性证据：**移除权重共享后，R Precision Top1 从 0.371 暴跌至 0.153，FID 从 5.918 升至 8.059**（Table 3），证明了对称性建模是生成质量的核心保障。

### 3. 带阻尼调度的交互正则化损失

仅靠扩散损失无法显式约束双人空间关系，容易产生穿透、朝向错误等伪影。InterGen 引入两类交互正则化损失：

- **掩码关节距离图损失（DM Loss）**：仅在两人距离较近时激活，强制学习空间干涉关系：

$$\mathcal{L}_{DM} = || (M(\hat{\mathbf{x}}_{a}, \hat{\mathbf{x}}_{b}) - M(\mathbf{x}_{a}, \mathbf{x}_{b})) \odot I(M_{xz}(\mathbf{x}_{a}, \mathbf{x}_{b}) < \bar{M}) ||_{2}^{2}$$

- **相对朝向损失（RO Loss）**：计算两人正面朝向的二维相对角度差，引导正确交互朝向：

$$\mathcal{L}_{RO} = || O(IK(\hat{\mathbf{x}}_{a}), IK(\hat{\mathbf{x}}_{b})) - O(IK(\mathbf{x}_{a}), IK(\mathbf{x}_{b})) ||_{2}^{2}$$

关键设计在于**基于扩散时间步的截断调度**：仅当 $t \leq \bar{t}$ 时才施加正则化损失，在高噪声阶段不施加约束以保持多样性：

$$\mathcal{L} = \mathcal{L}_{simple} + \lambda_{reg} \mathbb{E}_{t}[ I(t \leq \bar{t}) \cdot \mathcal{L}_{reg}^{(t)} ]$$

消融实验表明，移除 DM 损失使 Top1 降至 0.293、FID 升至 6.653；移除 RO 损失使 Top1 降至 0.310、FID 升至 6.311（Table 3）。$t \leq 0.7T$ 的截断设置取得最佳总体指标（Table 4），验证了阻尼调度的有效性。

### 创新总结

三个 changed slots 形成因果闭环：非规范表示提供空间关系的基础编码，合作去噪网络利用对称性高效学习交互流形，交互正则化损失显式约束关键空间量。三者缺一不可，共同将双人交互生成从“独立生成后拼接”推进到“协同生成”范式。



InterGen 的整体 pipeline 围绕“以扩散模型为核心、以对称性为约束、以世界坐标系为空间锚点”的设计理念展开。系统接收一段描述双人交互的自然语言文本，输出两个人物在三维空间中同步运动的长序列。整个流程由四个紧密耦合的阶段构成：**文本条件编码 → 噪声化初始运动 → 合作去噪重建 → 交互正则化约束**。

### 输入与表示层

输入为自由形式的文本提示（如 “Two people are boxing…”），经冻结的 **CLIP-ViT-L/14 文本编码器** 映射为固定维度的条件向量 $c$，作为后续去噪过程的条件信号。

运动数据采用 **非规范表示**（non-canonical representation），直接在同一个世界坐标系中记录两人的全局关节位置 $\mathbf{j}_g^p$、全局关节速度 $\mathbf{j}_g^v$、相对于各自根关节的局部旋转 $\mathbf{j}^r$ 以及脚部接触标签 $\mathbf{c}^f$：

$$x^{i} = [\mathbf{j}_{g}^{p}, \mathbf{j}_{g}^{v}, \mathbf{j}^{r}, \mathbf{c}^{f}]$$

这与传统单人生成中使用的规范表示（将关节位置和速度变换到根坐标系）形成根本差异。规范表示依赖对根关节速度的积分来恢复全局轨迹，在双人场景中会因误差累积导致两人的相对位置发生严重漂移，且无法显式编码“两人之间的空间关系”——这正是已有方法在双人交互上失败的核心原因之一。非规范表示将全局位置作为原始特征保留，使去噪网络能够直接感知和预测两人在世界空间中的绝对坐标，从根本上避免了积分漂移问题。

### 扩散过程与对称性建模

运动生成被建模为条件扩散的逆过程。前向过程逐步向真实运动数据 $x_a, x_b$ 注入高斯噪声，得到噪声样本 $x_a^{(t)}, x_b^{(t)}$；逆向过程则从纯噪声出发，利用分数函数 $\nabla_{\mathbf{x}} \log p_t(\mathbf{x})$ 逐步去噪重建：

$$d\mathbf{x} = [\mathbf{f}(\mathbf{x}, t) - \sigma_t^{2} \nabla_{\mathbf{x}} \log p_t(\mathbf{x})] dt + \sigma_t d\mathbf{w}$$

分数函数通过去噪网络 $D_\theta$ 来近似，其训练目标是最小化对干净运动的条件期望重建误差。

InterGen 的核心架构创新在于 **合作去噪网络**。系统使用两个 Transformer 风格的去噪器，分别负责预测人物 A 和人物 B 的运动。这两个去噪器 **共享全部权重**，并通过 **互注意力机制**（mutual attention）在每一层交换对方的中间特征。这一设计的理论基础是双人交互的交换对称性：

$$p(\mathbf{x}_a, \mathbf{x}_b) \equiv p(\mathbf{x}_b, \mathbf{x}_a)$$

即“A 对 B 出拳，B 防守”与“B 对 A 出拳，A 防守”在交互语义上是等价的。共享权重强制两个去噪器学习同一个运动流形，保证两人在运动能力上的对称性；互注意力则让两个去噪过程在每一步都能感知对方的当前状态，从而协调生成具有真实交互性的动作对。消融实验表明，移除权重共享会导致 R Precision Top1 从 0.371 骤降至 0.153，FID 从 5.918 升至 8.059，验证了对称性建模的决定性作用。

### 损失函数与阻尼调度

训练损失由三部分构成。基础损失 $\mathcal{L}_{simple}$ 为合作去噪的重建误差，对两人分别计算并求和：

$$\mathcal{L}_{simple} = \mathbb{E}_{\mathbf{x}, t, \epsilon}[\lambda_t \|\mathbf{x}_a - D_\theta(\mathbf{x}_a + \sigma_t\epsilon_a, \mathbf{x}_b + \sigma_t\epsilon_b, t, c)\|_2^2 + \lambda_t \|\mathbf{x}_b - D_\theta(\mathbf{x}_b + \sigma_t\epsilon_b, \mathbf{x}_a + \sigma_t\epsilon_a, t, c)\|_2^2]$$

骨骼长度损失 $\mathcal{L}_{BL}$ 约束生成的关节位置满足人体骨架的刚性结构：

$$\mathcal{L}_{BL} = \| B(\hat{\mathbf{x}}_a) - B(\mathbf{x}_a) \|_2^2 + \| B(\hat{\mathbf{x}}_b) - B(\mathbf{x}_b) \|_2^2$$

交互正则化损失包含两个关键项：**掩码关节距离图损失** $\mathcal{L}_{DM}$ 在两人距离较近时激活，强制学习空间干涉关系（如握手时手部关节的精确空间对应）；**相对朝向损失** $\mathcal{L}_{RO}$ 约束两人正面朝向的角度差，引导正确的交互朝向（如面对面交谈 vs. 背对背）。消融实验分别验证了二者的必要性：移除 DM 损失使 Top1 降至 0.293，移除 RO 损失使 Top1 降至 0.310。

这些正则化损失并非在所有扩散时间步上施加，而是采用 **截断式阻尼调度**：仅在扩散时间步 $t \leq \bar{t}$（即噪声水平较低、运动结构已初步成形时）才激活：

$$\mathcal{L} = \mathcal{L}_{simple} + \lambda_{reg} \mathbb{E}_t[ \mathbb{I}(t \leq \bar{t}) \cdot \mathcal{L}_{reg}^{(t)} ]$$

这一设计的直觉是：在高噪声阶段，运动样本几乎为纯噪声，此时施加空间约束不仅无效，还会限制生成多样性；当去噪进行到后半程，运动的大致形态已经显现，此时引入交互约束可以精细调整两人的相对位置与朝向，而不损害整体多样性。实验表明 $t \leq 0.7T$ 的截断策略取得了最优综合指标。

### 输出与推理

推理时，系统从随机高斯噪声出发，通过合作去噪网络迭代采样，最终输出两个人物在全局世界坐标系中的关节位置序列。这些序列可以直接驱动 SMPL 模型进行可视化渲染。得益于非规范表示，输出天然包含两人的全局轨迹，无需后处理积分即可获得无漂移的相对运动关系。

### 补充图表

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/006_Figure_5.jpg]]
*Figure 5: The overview of our InterGen. We contribute three primary technical designs. First, we propose an efficient twoperson interaction motion representation. Second, we introduce two cooperative transformer-style weights-sharing networks with mutual attention to interactively perform denoising. Lastly, we introduce an effective loss function that significantly improves the quality of two-person interaction generation*

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/001_Figure_1.jpg]]
*Figure 1: InterGen is capable of generating high-quality and diverse motions under complex interactions. It models the twoperson symmetry with cooperative diffusion denoisers sharing the same motion manifold*



InterGen 的核心架构围绕三个技术支柱构建：**非规范运动表示**、**合作去噪网络**和**交互正则化损失**，其整体框架如 Fig. 5 所示。以下逐模块展开推导。

### 4.1 非规范运动表示

传统单人生成方法（如 MDM）采用规范表示，将关节位置与速度变换至根关节坐标系，再通过积分恢复全局轨迹。这种设计在多人场景下会导致累积漂移和空间关系丢失。InterGen 提出**非规范表示**，直接在世界坐标系中编码全局关节位置与速度：

$$
x^{i} = [\mathbf{j}_{g}^{p}, \mathbf{j}_{g}^{v}, \mathbf{j}^{r}, \mathbf{c}^{f}]
$$

其中：
- $\mathbf{j}_{g}^{p} \in \mathbb{R}^{J \times 3}$：世界坐标系下的全局关节位置
- $\mathbf{j}_{g}^{v} \in \mathbb{R}^{J \times 3}$：世界坐标系下的全局关节速度
- $\mathbf{j}^{r} \in \mathbb{R}^{J \times 6}$：根坐标系下的局部旋转（6D 连续表示）
- $\mathbf{c}^{f} \in \mathbb{R}^{4}$：脚部接触标签特征

相比规范表示（Eq. 1）需额外维护根角速度、线速度、高度等变量并通过积分恢复轨迹，非规范表示直接将两人的绝对空间位置编码在同一世界帧中，避免了积分误差累积，且无需显式定义相对旋转与平移特征。

### 4.2 合作去噪网络与对称性

双人交互具有天然的**交换对称性**：交换两人身份后，交互语义保持不变。形式化地：

$$
p(\mathbf{x}_{a}, \mathbf{x}_{b}) \equiv p(\mathbf{x}_{b}, \mathbf{x}_{a})
$$

基于此，InterGen 设计两个**共享权重的 Transformer 去噪器** $D_{\theta}$，并通过**互注意力机制**在去噪过程中交换信息。扩散逆过程由逆向 SDE 描述：

$$
d\mathbf{x} = [\mathbf{f}(\mathbf{x}, t) - \sigma_{t}^{2} \nabla_{\mathbf{x}} \log p_{t}(\mathbf{x})] dt + \sigma_{t} d\mathbf{w}
$$

其中分数函数 $\nabla_{\mathbf{x}} \log p_{t}(\mathbf{x})$ 通过噪声样本的条件期望近似：

$$
\nabla_{\mathbf{x}^{(t)}} \log p_{t}(\mathbf{x}^{(t)}) = (\mathbb{E}[\mathbf{x} | \mathbf{x}^{(t)}] - \mathbf{x}^{(t)}) / \sigma_{t}^{2}
$$

合作去噪损失同时预测两人运动，体现对称性：

$$
\mathcal{L}_{simple} = \mathbb{E}_{\mathbf{x}, t, \epsilon}[\lambda_{t}||\mathbf{x}_{a} - D_{\theta}(\mathbf{x}_{a}+\sigma_{t}\epsilon_{a}, \mathbf{x}_{b}+\sigma_{t}\epsilon_{b}, t, c)||_{2}^{2} + \lambda_{t}||\mathbf{x}_{b} - D_{\theta}(\mathbf{x}_{b}+\sigma_{t}\epsilon_{b}, \mathbf{x}_{a}+\sigma_{t}\epsilon_{a}, t, c)||_{2}^{2}]
$$

条件向量 $c$ 由冻结的 **CLIP-ViT-L/14** 文本编码器提供。权重共享确保两人共享同一运动流形，互注意力则使去噪过程显式感知对方状态。

### 4.3 交互正则化损失与阻尼调度

仅靠 $\mathcal{L}_{simple}$ 无法保证生成运动的物理合理性和交互真实性，因此引入三项辅助损失，如 Fig. 6 所示。

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/007_Figure_6.jpg]]
*Figure 6: (Left) visualize our proposed interactive losses, where the relative orientation loss is the angular separation between the frontal orientations of the two people. And the partial joint distance map of the heel joint is truncated with the region of the*

**骨骼长度损失**约束生成骨架的结构一致性：

$$
\mathcal{L}_{BL} = || B(\hat{\mathbf{x}}_{a}) - B(\mathbf{x}_{a}) ||_{2}^{2} + || B(\hat{\mathbf{x}}_{b}) - B(\mathbf{x}_{b}) ||_{2}^{2}
$$

其中 $B(\cdot)$ 从全局关节位置计算骨骼长度。

**掩码关节距离图损失**仅在两人距离较近时激活，强制学习空间干涉关系（如握手、拥抱时的接触距离）：

$$
\mathcal{L}_{DM} = || (M(\hat{\mathbf{x}}_{a}, \hat{\mathbf{x}}_{b}) - M(\mathbf{x}_{a}, \mathbf{x}_{b})) \odot I(M_{xz}(\mathbf{x}_{a}, \mathbf{x}_{b}) < \bar{M}) ||_{2}^{2}
$$

$M(\cdot)$ 计算两人所有关节对在 XZ 平面上的距离图，指示函数 $I(\cdot)$ 仅在距离小于阈值 $\bar{M}$ 时激活损失。

**相对朝向损失**正则化两人的正面朝向关系，计算两人正面方向（由逆运动学 $IK(\cdot)$ 推导）的二维角度差：

$$
\mathcal{L}_{RO} = || O(IK(\hat{\mathbf{x}}_{a}), IK(\hat{\mathbf{x}}_{b})) - O(IK(\mathbf{x}_{a}), IK(\mathbf{x}_{b})) ||_{2}^{2}
$$

为避免高噪声阶段（$t$ 较大时）施加正则化导致多样性下降，采用**截断式损失调度**：仅当扩散时间步 $t \leq \bar{t}$ 时激活正则化项，总损失为：

$$
\mathcal{L} = \mathcal{L}_{simple} + \lambda_{reg} \mathbb{E}_{t}[ I(t \leq \bar{t}) \cdot \mathcal{L}_{reg}^{(t)} ]
$$

消融实验表明 $\bar{t} = 0.7T$ 时取得最佳总体指标（Table 4），验证了阻尼调度的有效性。



## 实验与关键发现

### 核心定量结果

InterGen 在 InterHuman 测试集上对所有基线方法取得了一致且显著的最优结果。在文本-运动匹配精度（R Precision Top1）上达到 **0.371**，生成质量（FID）降至 **5.918**，多样性-质量平衡指标（MM Dist）为 **5.108**，均大幅领先已有方法（Table 2）。对比的基线包括单人文生运动模型 **TEMOS**（Petrovich et al., ECCV 2022）、**T2M**（Guo et al., CVPR 2022）、扩散运动生成模型 **MDM**（Tevet et al., ICLR 2023），以及基于 MDM 微调的双人交互基线 **ComMDM**（Shafir et al., 2023）。为确保公平性，所有模型均采用相同的非规范运动表示，且评测指标均运行多次并报告 95% 置信区间。

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparisons on the InterHuman test set. We run all the evaluations 20 times except MModality runs 5 times. ± indicates the 95% confidence interval. Bold indicates best result. ComMDM* indicates the ComMDM model fine-tuned in the original few-shot setting with 10 training samples and ComMDM (without *) indicates fine-tuned on our entire InterHuman training set. All the models employ the same non-canonical representation*

ComMDM 在全量 InterHuman 训练集上微调后，R Precision Top1 仅达到 0.204，FID 为 7.231，远逊于 InterGen。这一差距揭示了单纯将单人生成模型扩展到双人场景的局限性：缺乏对交互空间关系与运动能力对称性的显式建模会导致生成质量严重退化。

### 消融实验：关键设计的因果验证

Table 3 的消融实验逐一验证了 InterGen 三个核心设计的独立贡献，每个设计的移除均导致性能的显著跌落。

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/011_Table_3.jpg]]
*Table 3: Quantitative evaluation of our key designs. The performance drop-off highlights our technical contributions*

**权重共享的合作去噪网络**是最关键的设计。移除权重共享（即两个去噪器独立训练）后，R Precision Top1 从 0.371 骤降至 **0.153**，FID 从 5.918 升至 **8.059**。这一剧烈退化直接验证了交互对称性假设：$p(\mathbf{x}_a, \mathbf{x}_b) \equiv p(\mathbf{x}_b, \mathbf{x}_a)$ 是双人交互的基本属性，共享权重强制两个去噪器在同一个运动流形上学习，避免了独立训练时的模式坍塌与语义漂移。

**非规范世界坐标系表示**的消融进一步证实了全局空间信息的重要性。将其替换为传统的规范表示（局部关节位置相对于根坐标系）后，Top1 降至 0.221，FID 升至 7.014。规范表示在双人场景中会因根关节的独立积分而累积漂移误差，使两人的相对位置随时间发散；而非规范表示直接在世界坐标系中编码全局关节位置，从根本上规避了这一问题。

### 交互正则化损失与阻尼调度的作用

Table 3 同时揭示了两个交互正则化损失的必要性。移除**掩码关节距离图损失（DM loss）**后，Top1 降至 0.293，FID 升至 6.653；移除**相对朝向损失（RO loss）**后，Top1 降至 0.310，FID 升至 6.311。DM loss 仅在两人距离较近时激活，强制模型学习空间干涉关系（如握手时手掌的精确相对位置）；RO loss 则约束两人正面朝向的角距离，确保交互语义的正确性（如面对面交谈 vs 背对背行走）。两者分别从空间距离和朝向角度两个维度显式编码了交互约束，弥补了简单扩散损失在交互建模上的不足。

Table 4 验证了**基于扩散时间步截断的阻尼调度**策略的有效性。当正则化损失仅在扩散时间步 $t \leq 0.7T$ 时施加，可获得最佳总体指标。在高噪声阶段（$t > 0.7T$），运动结构尚未成型，过早施加空间约束会限制生成多样性；而在低噪声阶段施加正则化，则能在保持多样性的同时精细调整交互细节。Figure 9 的定性结果直观展示了各消融变体的生成效果差异。

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/012_Table_4.jpg]]
*Table 4: Quantitative evaluation of our regularization loss schedule training scheme. The strategy of different treatments for different noise levels improves the performance significantly*

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/013_Figure_9.jpg]]
*Figure 9: Qualitative results of ablation study. The top of the figure displays text prompts, while the lower illustrates the results of different ablation experiments and our best result. For quantitative comparisons of experimental results, please refer to Tab. 3*

### 失败模式与局限性

尽管 InterGen 在定量指标上表现优异，分析其生成结果仍可识别出以下失败模式：

1. **近距离接触的穿透与抖动**：在拳击、摔跤等紧密接触动作中，生成的 SMPL 模型偶尔出现肢体穿透或高频抖动。这是因为 DM loss 仅在距离图层面施加软约束，缺乏严格的物理碰撞检测与接触力建模。引入物理仿真作为后处理或训练约束是潜在的改进方向。

2. **多人扩展的计算瓶颈**：当前架构仅支持双人交互。扩展到 N 人场景时，合作去噪网络的互注意力计算复杂度将呈 $O(N^2)$ 增长，且训练数据需覆盖指数级增长的交互组合。论文未提供此方向的实验证据。

3. **数据集偏差**：InterHuman 数据集基于脚本表演采集，可能无法覆盖真实生活中自由、随机的交互模式。对于训练集未见的全新交互文本（如特定文化礼仪或罕见运动），模型的泛化能力有限。

4. **文本编码器的适配性**：InterGen 采用冻结的 CLIP-ViT-L/14 作为文本编码器，但未探索更适合运动领域的文本-运动联合表示空间。不同文本编码器（如 LLaMA）对结果的影响已在论文中被提及但未深入分析。

### 补充图表

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative comparison with previous state-of-the-art works. The inputs to the model are listed at the top and middle, while the outputs of different models (Petrovich et al., 2022; Guo et al., 2022a; Tevet et al., 2022b; Shafir et al., 2023) are listed below. Intersecting portions of the motions are highlighted with red dashed circles*

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative results generated by our InterGen model. We showcase two different samples per text prompt, which demonstrate the high quality and diversity of our interaction generation*

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/004_Table_1.jpg]]
*Table 1: Dataset comparisons. We compare our InterHuman dataset with existing human motion datasets. Motions refers to the total number of motion clips. Vocab. shows the number of distinct words used in the annotations, while Descriptions summarizes the total number of textual descriptions*

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/014_Figure_10.jpg]]
*Figure 10: Person-to-person generation. The above five motions are generated with the premise of freezing the motion of one person (represented by a semi-transparent SMPL model) while generating the motion of the other person (represented by an opaque SMPL model)*

![[assets/figures/papers/paper_list_l1788_InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Int/figures/015_Figure_11.jpg]]
*Figure 11: Trajectory control. The curve beneath the peoples’ feet represents their motion trajectories. The skeleton representation displays the position and motion of each frame over time, with the SMPL model (Loper et al., 2015) indicating a specific frame of motion. The text input for each motion is provided above the respective persons*



## 定位与知识库关联

### 问题瓶颈与核心思路

现有单人文本-运动生成模型（如 **TEMOS** (Petrovich et al., ECCV 2022)、**T2M** (Guo et al., CVPR 2022)、**MDM** (Tevet et al., ICLR 2023)）在直接应用于双人交互生成时，面临两个根本性瓶颈：

1. **空间关系缺失**：标准规范表示将运动转换到根坐标系，丢弃了两人在世界空间中的绝对位置与相对距离信息，导致生成的交互缺乏真实的空间干涉。
2. **运动能力不对称与模式坍塌**：独立处理两人运动无法保证交互语义的一致性，容易产生漂移、穿透和生成多样性丧失。

InterGen 的核心洞察在于：**两人交互具有身份交换对称性**，即 $p(\mathbf{x}_a, \mathbf{x}_b) \equiv p(\mathbf{x}_b, \mathbf{x}_a)$。基于此，论文提出三个因果调节变量：共享权重的合作去噪网络（编码对称性先验）、非规范世界坐标系运动表示（保留全局空间关系）、以及带阻尼调度的交互正则化损失（显式约束相对位置与朝向）。

### 方法定位与基线关系

InterGen 处于**双人交互扩散生成**这一新兴方向的开创位置。其直接对比的基线可分为两类：

- **单人生成模型直接迁移**：TEMOS、T2M、MDM 均为单人文生运动模型，缺乏交互建模能力。在 InterHuman 测试集上，这些模型生成的两人运动会表现出严重的不协调和空间漂移（见 Fig. 8 的红圈标注区域）。
- **基于 MDM 微调的双人基线**：**ComMDM** (Shafir et al., 2023) 在 MDM 基础上进行双人微调，但其去噪网络不共享权重，且缺乏专门的交互损失。InterGen 在 R Precision Top1 上从 ComMDM 的基线水平提升至 0.371，FID 降至 5.918（Table 2）。

值得注意的是，所有对比方法均采用相同的非规范运动表示以确保公平比较，因此性能差距主要源于去噪架构和交互损失的设计差异。

### 适用边界与局限

尽管 InterGen 在双人交互生成上取得了显著进展，其适用边界受以下因素制约：

1. **人数扩展瓶颈**：合作去噪架构的对称性假设天然适用于两人场景。扩展到 N 人交互（如群体舞蹈、团队运动）时，身份交换对称性不再成立，且互注意力机制的计算复杂度将呈 $O(N^2)$ 增长。论文明确指出这一局限，目前尚无直接的多人生成方案。

2. **物理约束缺失**：交互正则化损失（距离图损失、相对朝向损失）仅在运动学层面约束空间关系，缺乏严格的物理碰撞检测或动量守恒约束。在近距离接触动作（如拳击、拥抱）中，生成结果可能出现轻微穿透和抖动伪影。

3. **数据驱动泛化限制**：InterHuman 数据集基于脚本表演采集，覆盖了武术、舞蹈、日常礼仪等类别，但可能无法完全代表真实生活中自由、随机的交互模式。对于训练集中未见的全新交互文本，模型的泛化能力有限。

4. **文本编码器选择**：论文固定使用 CLIP-ViT-L/14 作为文本编码器，未探索更适配运动领域的文本-运动联合表示模型（如 LLaMA 等大语言模型），这可能限制了跨模态对齐的上限。

### 开放问题与后续方向

从方法谱系角度看，InterGen 打开了以下值得探索的方向：

- **多人交互架构**：如何将合作去噪从双人推广到 N 人？可能的路径包括层次化去噪（先全局后局部）、图神经网络建模人物间关系图、或引入置换等变网络。
- **物理仿真融合**：将物理约束（接触力、动量守恒、碰撞检测）作为后处理步骤或训练时的可微分约束，以减少穿透和抖动，提升生成运动的物理合理性。
- **变长序列与多时间尺度**：当前模型生成固定长度序列，如何支持从短时握手到长时舞蹈等不同时间尺度的交互生成？
- **高层属性控制**：引入用户对交互风格（柔和/激烈）、情绪（友好/敌对）、角色关系（教师-学生、医生-患者）等高层属性的精细控制粒度，其中不对称交互对身份交换对称性提出了新的挑战。
- **更优的文本-运动对齐**：探索更适合运动领域的文本编码器或联合表示空间，以提升跨模态一致性和基于文本的运动编辑能力。



## 原文 PDF

![[paperPDFs/IJCV_2024/InterGen_Diffusion_based_Multi_human_Motion_Generation_under_Complex_Interactions.pdf]]
