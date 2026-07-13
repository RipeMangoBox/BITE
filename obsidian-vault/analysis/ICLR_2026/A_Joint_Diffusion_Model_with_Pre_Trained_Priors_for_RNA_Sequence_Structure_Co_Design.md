---
title: "A Joint Diffusion Model with Pre-Trained Priors for RNA Sequence-Structure Co-Design"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Joint_Diffusion_Model_with_Pre_Trained_Priors_for_RNA_Sequence_Structure_Co_Design.pdf
project_link: null
code_link: null
aliases:
- JDMPTPRSSCD
- RiboDiff
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/genetics_cell_biology_health_etc
core_operator: "将预训练的跨分子结构预测模型RoseTTAFold2NA (RF2NA)作为去噪网络嵌入到联合扩散框架中，利用其丰富的先验知识提升数据效率。"
primary_logic: "利用预训练生物分子模型（RF2NA）作为扩散模型的去噪器，通过微调而非从头训练，可以显著缓解RNA结构数据稀缺带来的瓶颈，实现高质量的序列-结构联合生成。"
claims:
- "RiboDiff在单RNA设计任务上成功率达97.38%，scRMSD为3.43 Å，而从头训练的MMDiff成功率为0%，scRMSD为35.7 Å。"
- "联合扩散（序列和结构同时去噪）比交替扩散（序列和结构分别去噪）学习更快，scRMSD在几百步内降至4 Å，而交替扩散停滞在更高值。"
- "不使用预训练先验的训练极不稳定，出现长平台期和高方差，而使用预训练先验的联合扩散稳定且快速收敛。"
- "在蛋白质条件RNA设计任务中，完整RF2NA条件化（GT-RMSD 13.2, GT-SeqRec 56.3）优于仅序列条件化（16.2, 33.5）、仅结构条件化（15.1, 45.9）和模块化条件化基线（15.5, 38.2）。"
---

# A Joint Diffusion Model with Pre-Trained Priors for RNA Sequence-Structure Co-Design

> [!tip] 核心洞察
> 利用预训练生物分子模型（RF2NA）作为扩散模型的去噪器，通过微调而非从头训练，可以显著缓解RNA结构数据稀缺带来的瓶颈，实现高质量的序列-结构联合生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于预训练先验的RNA序列-结构联合扩散模型 |
| 英文题名 | A Joint Diffusion Model with Pre-Trained Priors for RNA Sequence-Structure Co-Design |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=cpc63YrVWN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/genetics_cell_biology_health_etc |
| Method | RiboDiff |
| Dataset | 单RNA设计 (RNASolo), RNA-蛋白质复合物设计 |

> [!tip] 效果简介
> - 单RNA设计 (RNASolo) 上，成功率 (%) ↑ 为 97.38 ± 4.86，对比 0.00 (MMDiff)，变化 +97.38。
> - 单RNA设计 (RNASolo) 上，scRMSD (Å) ↓ 为 3.43 ± 0.51，对比 35.7 (MMDiff)，变化 -32.27。
> - 单RNA设计 (RNASolo) 上，scTM-score ↑ 为 0.71 ± 0.04，对比 0.12 (MMDiff)，变化 +0.59。

## 概要

RNA序列-结构联合设计面临的核心瓶颈是实验结构数据极度稀缺，导致从头训练的生成模型性能受限。RiboDiff的核心洞察在于：将预训练的跨分子结构预测模型RoseTTAFold2NA (RF2NA)作为扩散模型的去噪网络嵌入到联合扩散框架中，通过微调而非从头训练，利用其丰富的先验知识显著缓解数据稀缺问题。该方法耦合了离散扩散（处理核苷酸序列）和SE(3)-等变连续扩散（处理全原子刚性框架的平移与旋转），并设计了包含序列交叉熵、FAPE结构损失、RMSD损失、几何损失和Lennard-Jones碰撞损失在内的组合训练目标。

在单RNA从头设计任务上，RiboDiff实现了97.38%的成功率（scRMSD < 5Å），scRMSD为3.43 Å，scTM-score为0.71；相比之下，从头训练的MMDiff成功率为0%，scRMSD为35.7 Å，scTM-score为0.12。在RNA-蛋白质复合物设计任务中，RiboDiff的scRMSD为7.43 Å，scTM-score为0.422，而MMDiff分别为28.4 Å和0.08。在蛋白质条件RNA设计任务中，RiboDiff在GT-RMSD（13.20 vs 16.2）和GT-SeqRec（56.26% vs 28.0%）上均显著优于RNAFlow。消融研究证实：联合扩散（序列和结构同时去噪）学习速度远快于交替扩散（分别去噪），scRMSD在几百步内降至4 Å；不使用预训练先验的训练极不稳定，出现长平台期和高方差；去除全局RMSD损失对性能影响最大（成功率从97.38%降至30.08%），表明其对全局正确折叠至关重要。



RNA的序列与三维结构共同决定了其生物学功能（如催化、调控、蛋白质相互作用），因此功能性RNA设计需要同时优化序列和结构——即序列-结构联合设计（co-design）。然而，该任务面临一个根本性的瓶颈：**实验测定的RNA结构数据极度稀缺**。与蛋白质结构数据库（PDB）中超过20万个结构条目相比，RNA结构条目仅有数千个，且长度分布不均、构象多样性有限。这种数据稀缺性导致从头训练的生成模型（如基于扩散的MMDiff、基于流匹配的RiboGen）在训练中极不稳定，收敛缓慢且生成质量低下。例如，MMDiff在单RNA设计任务上的成功率为0%，自洽RMSD（scRMSD）高达35.7 Å，几乎无法产生任何有意义的构象（Table 1）。

现有方法的另一个缺口在于，它们将序列生成和结构生成视为分离或弱耦合的过程。两阶段方法（如RNA-FrameFlow生成骨架 + gRNAde逆折叠）先独立生成结构再推断序列，割裂了序列与结构之间的协同约束，导致生成的结构与序列不匹配（scRMSD 17.59 Å，成功率19.34%，Table 10）。而简单的联合扩散（序列和结构同时去噪但无先验）也因缺乏足够的训练信号而失败，scRMSD学习曲线呈现长平台期和高方差，无法收敛到低误差区域（Figure 5）。

本文的动机正是针对上述瓶颈——**能否利用大规模预训练的跨分子结构预测模型所蕴含的先验知识，来弥补RNA结构数据稀缺带来的训练困难，从而实现稳定的序列-结构联合生成？** 核心洞察在于：RoseTTAFold2NA（RF2NA）已经在蛋白质-核酸复合物结构预测任务上学习了丰富的分子间相互作用模式、几何约束和序列-结构对应关系，这些先验知识可以通过微调的方式迁移到生成任务中，避免从头学习带来的数据需求。具体而言，本文提出的RiboDiff将RF2NA的主干网络作为扩散模型的去噪器，仅添加轻量级的扩散输出头（序列logits头、平移噪声头、SO(3)旋转速度头），在联合扩散框架下进行微调。这种设计使得模型在极少的训练步数内就能稳定收敛——联合扩散的scRMSD在几百步内降至4 Å以下，而无预训练先验的联合扩散则停滞在20 Å以上（Figure 5）。这一因果机制——**用预训练先验替代大量训练数据**——构成了RiboDiff的核心创新，使其在单RNA设计上达到97.38%的成功率和3.43 Å的scRMSD，远超所有从头训练的基线。



## 核心方法与创新机理

RiboDiff的核心创新在于**将预训练的跨分子结构预测模型RoseTTAFold2NA (RF2NA)作为去噪网络嵌入到联合扩散框架中**，通过微调而非从头训练，显著缓解了RNA结构数据稀缺带来的瓶颈。这一设计直接改变了去噪网络的初始化方式——从随机初始化变为使用RF2NA预训练权重，并添加序列、平移和旋转三个扩散头进行微调（证据锚点：“We reuse the pretrained RF2NA trunk as the shared representation and add diffusion heads including sequence head that outputs categorical logits, translation head that outputs per-residue translational noise, and rotation head that outputs per-nucleotide tangent velocities on SO(3).”）。

相比现有baseline，RiboDiff在以下关键槽位（changed slots）上实现了系统性改进：

1. **去噪网络初始化**：从随机初始化（MMDiff、RiboGen等从头训练基线）变为RF2NA预训练权重初始化。这是最关键的改变——不使用预训练先验的训练极不稳定，出现长平台期和高方差，而使用预训练先验的联合扩散稳定且快速收敛（Figure 5）。

2. **扩散过程类型**：从单一的连续扩散或离散扩散，变为离散扩散（序列）+ SE(3)-等变连续扩散（结构）的联合双扩散。消融实验表明，联合扩散（序列和结构同时去噪）比交替扩散学习更快，scRMSD在几百步内降至4 Å，而交替扩散停滞在更高值（Figure 5）。

3. **训练损失函数**：从简单的噪声预测损失变为组合损失，包括序列交叉熵、FAPE结构损失、全局RMSD损失、几何损失和Lennard-Jones碰撞损失。损失项消融实验（Table 9）揭示：去除全局RMSD损失影响最大（成功率从97.38%降至30.08%，scRMSD从3.43升至16.72），表明该损失项对全局正确折叠至关重要；去除结构对齐损失也显著降低性能（成功率降至58.64%，scRMSD升至5.85），说明RF2NA引导的结构先验对鲁棒的序列-结构共一致性至关重要。

4. **推理增强**：引入基于值的推理时重要性采样（SVDD），从M个候选状态中选择最优。Table 4显示SVDD在多个奖励函数下均能提升生成质量。

RiboDiff的pipeline由四个模块构成：RF2NA主干网络（提供跨分子先验知识）、序列扩散头（输出核苷酸类别logits）、平移扩散头（输出每个残基的平移噪声）、旋转扩散头（输出每个核苷酸在SO(3)上的切向速度），以及推理时RL增强模块SVDD。

**核心证据强度**：Table 1显示，在单RNA设计任务上，RiboDiff成功率97.38%、scRMSD 3.43 Å，而从头训练的MMDiff成功率为0%、scRMSD 35.7 Å——这一>10倍的scRMSD降低直接验证了预训练先验策略的有效性。Table 2在RNA-蛋白质复合物设计任务上同样显示RiboDiff的scRMSD为7.43 Å，远优于MMDiff的28.4 Å。Table 3在蛋白质条件RNA设计任务中，RiboDiff的GT-SeqRec达到56.26%，显著优于RNAFlow的28.0%。

**需要手动验证的点**：Figure 5的学习曲线虽然提供了联合扩散vs交替扩散vs无预训练先验的对比，但文中未明确说明这些曲线的计算方式（是否在同一随机种子下多次运行取平均），建议手动确认实验设置的公平性。



![[assets/figures/papers/iclr26_0003_cpc63YrVWN_A_Joint_Diffusion_Model_with_Pre-Trained_Priors/figures/001_Figure_1.jpg]]
*Figure 1: (a) Overview of RiboDiff*

RiboDiff 的核心创新在于将预训练的跨分子结构预测模型 RoseTTAFold2NA (RF2NA) 作为去噪网络，嵌入到一个联合双扩散框架中。该框架耦合了针对离散核苷酸序列的离散扩散过程和针对全原子坐标的 SE(3)-等变连续扩散过程（包括框架的平移和旋转）。其根本动机在于解决 RNA 设计面临的严重实验结构数据稀缺问题：从头训练的生成模型（如 MMDiff）性能受限，而利用 RF2NA 丰富的先验知识可以显著提升数据效率。

**Pipeline 模块关系与输入输出流：**

1.  **输入与表示构建**：输入为带噪的序列-结构对。首先，从每个核苷酸的三个原子（C4', C1', N1/N9）通过 Gram-Schmidt 过程构建局部坐标系（框架），将结构表示为 SE(3) 框架的集合。
2.  **前向扩散过程**：对序列应用离散扩散，对结构应用 SE(3)-等变扩散（平移使用高斯扩散，旋转使用 SO(3) 上的各向同性高斯扩散），逐步向数据添加噪声。
3.  **预训练去噪网络（RF2NA 主干）**：这是整个框架的核心。复用预训练的 RF2NA 主干网络作为共享表示提取器，其强大的结构先验知识能够从带噪的序列-结构对中预测出干净的序列和结构。
4.  **扩散头**：在 RF2NA 主干之上添加三个专门的扩散头，用于输出不同的去噪预测：
    -   **序列头**：输出每个位置的核苷酸类别 logits，用于指导离散扩散的逆向过程。
    -   **平移头**：输出每个残基的平移噪声。
    -   **旋转头**：输出每个核苷酸在 SO(3) 上的切向速度。
5.  **逆向生成过程**：利用 RF2NA 主干和扩散头的预测，通过逆向扩散步骤进行联合去噪。序列的逆向步骤使用基于贝叶斯定理的后验转移概率，结构的逆向步骤使用基于预测干净结构的得分函数。
6.  **训练损失**：模型通过一个组合损失函数进行微调，以平衡序列准确性、结构精度和物理有效性：
    `L_total = λ_seq * L_seq + λ_str * L_str + λ_rmsd * L_rmsd + λ_geom * L_geom + λ_lj * L_lj`
    其中，`L_rmsd`（全局 RMSD 损失）对保证全局正确折叠至关重要，`L_str`（结构对齐损失）对鲁棒的序列-结构共一致性至关重要。
7.  **推理增强（SVDD）**：在推理时，引入基于值的推理时重要性采样模块。该模块从 M 个候选状态中选择最优的生成路径，通过权衡奖励和 log 概率来提升生成质量。



### 问题形式化与框架构建

RiboDiff将RNA序列-结构共设计形式化为一个联合优化问题。给定序列 **s** 和全原子结构 **X**，目标是最大化概率与设计目标函数的乘积：

$$\mathbf { s } ^ { * } , \mathbf { X } ^ { * } = \arg \operatorname* { m a x } _ { ( \mathbf { s } , \mathbf { X } ) \in \mathcal { V } } p ( \mathbf { s } , \mathbf { X } ) \cdot f _ { \mathrm { o b j e c t i v e } } ( \mathbf { s } , \mathbf { X } )$$

其中 $p(\mathbf{s}, \mathbf{X})$ 是联合分布，$f_{\mathrm{objective}}$ 是任务相关的设计目标函数。该框架的核心创新在于将预训练的RoseTTAFold2NA (RF2NA) 作为去噪网络嵌入到双扩散过程中，利用其丰富的跨分子先验知识来缓解RNA结构数据稀缺的瓶颈。

### 结构表示：核苷酸局部坐标系

每个核苷酸的结构通过一个刚性框架表示，该框架由三个原子（C4', C1', N1/N9）通过Gram-Schmidt过程构建：

$$\begin{array} { r l } & { { \bf v } _ { 1 } = { \bf x } _ { C 1 ^ { \prime } } - { \bf x } _ { C 4 ^ { \prime } } , \quad { \bf e } _ { 1 } = { \bf v } _ { 1 } / \| { \bf v } _ { 1 } \| } \\\\ & { { \bf v } _ { 2 } = { \bf x } _ { N 1 / N 9 } - { \bf x } _ { C 4 ^ { \prime } } , \quad { \bf u } _ { 2 } = { \bf v } _ { 2 } - ( { \bf v } _ { 2 } \cdot { \bf e } _ { 1 } ) { \bf e } _ { 1 } } \\\\ & { { \bf e } _ { 2 } = { \bf u } _ { 2 } / \| { \bf u } _ { 2 } \| , \quad { \bf e } _ { 3 } = { \bf e } _ { 1 } \times { \bf e } _ { 2 } } \\\\ & { { \bf R } _ { i } = [ { \bf e } _ { 1 } , { \bf e } _ { 2 } , { \bf e } _ { 3 } ] , \quad { \bf t } _ { i } = { \bf x } _ { C 4 ^ { \prime } } } \end{array}$$

其中 $\mathbf{R}_i \in SO(3)$ 是旋转矩阵，$\mathbf{t}_i \in \mathbb{R}^3$ 是平移向量，共同构成第 $i$ 个核苷酸的刚性框架 $\mathcal{F}_i = (\mathbf{R}_i, \mathbf{t}_i)$。

### 双扩散过程

RiboDiff耦合了两个并行但交互的扩散过程：序列的离散扩散和结构的SE(3)-等变连续扩散。

**结构扩散** 包含平移和旋转两个独立的前向过程。平移部分使用标准高斯扩散：

$$q ( \mathbf { t } _ { t } | \mathbf { t } _ { 0 } ) = \mathcal { N } ( \mathbf { t } _ { t } ; \sqrt { \bar { \alpha } _ { t } ^ { \mathrm { t r a n s } } } \mathbf { t } _ { 0 } , ( 1 - \bar { \alpha } _ { t } ^ { \mathrm { t r a n s } } ) \mathbf { I } _ { 3 } )$$

其中 $\bar{\alpha}_t^{\mathrm{trans}}$ 是累积噪声调度参数。旋转部分在SO(3)流形上使用各向同性高斯扩散：

$$q ( \mathbf { R } _ { t } | \mathbf { R } _ { 0 } ) = \mathcal { I } \mathcal { G } _ { S O ( 3 ) } ( \mathbf { R } _ { t } ; \mathbf { R } _ { 0 } , \kappa _ { t } )$$

其中 $\kappa_t$ 是浓度参数，控制旋转噪声的扩散程度。

**序列扩散** 使用离散马尔可夫链，每个核苷酸类别独立地在4个碱基（A, U, G, C）之间进行转移。

### 逆向去噪过程

逆向过程中，预训练的RF2NA作为去噪网络，预测干净的序列和结构。序列的逆向步骤通过后验转移概率计算：

$$p _ { \theta } \big ( \mathbf { s } _ { t - 1 } | \mathbf { s } _ { t } , \mathbf { X } _ { t } \big ) = \sum _ { \mathbf { s } _ { 0 } } q ( \mathbf { s } _ { t - 1 } | \mathbf { s } _ { t } , \mathbf { s } _ { 0 } \big ) \cdot p _ { \theta } \big ( \mathbf { s } _ { 0 } | \mathbf { s } _ { t } , \mathbf { X } _ { t } \big )$$

其中 $p_\theta(\mathbf{s}_0 | \mathbf{s}_t, \mathbf{X}_t)$ 是网络预测的干净序列分布。结构的逆向步骤使用预测的干净结构计算均值：

$$p_\theta(\mathbf{X}_{t-1}|\mathbf{X}_t,\mathbf{s}_t) = \mathcal{N}(\mathbf{X}_{t-1}; \mu_\theta(\mathbf{X}_t,\mathbf{s}_t,t), \boldsymbol{\Sigma}_t)$$

### 预训练去噪网络架构

RF2NA采用三轨道神经网络架构，同时处理并更新三种互补的表示：
- **序列轨道**：处理1D特征 $\mathbf{h}^{(1D)} \in \mathbb{R}^{L \times d_{\mathrm{seq}}}$，捕获位置和进化信息
- **配对轨道**：维护成对表示 $\mathbf{h}^{(2D)} \in \mathbb{R}^{L \times L \times d_{\mathrm{pair}}}$，编码残基间关系
- **结构轨道**：通过SE(3)-Transformer更新3D坐标和框架：

$$\mathbf { h } ^ { ( 3 D ) } , \{ \mathcal { F } _ { i } \} = \mathrm { S E 3 - T r a n s f o r m e r } ( \mathbf { h } ^ { ( 3 D ) } , \{ \mathcal { F } _ { i } \} , \mathbf { E } )$$

RiboDiff复用预训练的RF2NA主干作为共享表示，并添加三个扩散头：输出类别logits的序列头、输出每个残基平移噪声的平移头、以及输出每个核苷酸在SO(3)上切向速度的旋转头。这些头与RF2NA模型一起使用预训练权重初始化并进行微调。

### 训练损失函数

总训练损失由五个项组成，平衡序列准确性、结构精度和物理有效性：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{seq}} * \mathcal{L}_{\mathrm{seq}} + \lambda_{\mathrm{str}} * \mathcal{L}_{\mathrm{str}} + \lambda_{\mathrm{rmsd}} * \mathcal{L}_{\mathrm{rmsd}} + \lambda_{\mathrm{geom}} * \mathcal{L}_{\mathrm{geom}} + \lambda_{\mathrm{lj}} * \mathcal{L}_{\mathrm{lj}}$$

各损失项的作用通过消融实验得到验证：
- **$\mathcal{L}_{\mathrm{seq}}$**：序列交叉熵损失，衡量核苷酸类别预测的准确性
- **$\mathcal{L}_{\mathrm{str}}$**：FAPE结构对齐损失，由RF2NA引导的结构先验对鲁棒的序列-结构共一致性至关重要（去除后成功率从97.38%降至58.64%，scRMSD升至5.85）
- **$\mathcal{L}_{\mathrm{rmsd}}$**：全局RMSD损失，对全局正确折叠至关重要（去除后成功率骤降至30.08%，scRMSD升至16.72）
- **$\mathcal{L}_{\mathrm{geom}}$**：几何损失，确保键长、键角等几何约束
- **$\mathcal{L}_{\mathrm{lj}}$**：Lennard-Jones碰撞损失，避免原子间空间冲突

### 推理时强化学习增强（SVDD）

为提升推理时的生成质量，RiboDiff引入了基于值的推理时重要性采样。该方法从标准逆向过程中采样 $M$ 个候选状态：

$$( \mathbf { X } _ { t - 1 } ^ { ( m ) } , \mathbf { s } _ { t - 1 } ^ { ( m ) } ) \sim p _ { \theta } ( \cdot | \mathbf { X } _ { t } , \mathbf { s } _ { t } , t ) , \quad m = 1 , \ldots , M$$

然后基于奖励和log概率的权衡选择最优候选：

$$m^* = \arg\max_m [r^{(m)}(\mathbf{X}_0^{(m)},\mathbf{s}_0^{(m)}|\mathbf{X}_{t-1}^{(m)},\mathbf{s}_{t-1}^{(m)}) + \tau \log p_\theta(\mathbf{X}_{t-1}^{(m)},\mathbf{s}_{t-1}^{(m)}|\mathbf{X}_t,\mathbf{s}_t,t)]$$

其中 $r$ 是奖励函数，$\tau$ 是温度参数控制探索-利用平衡。该方法在保持多样性的同时有效提升了生成质量。



## 实验与关键发现

### 主结果

RiboDiff 在三个 RNA 设计任务上均显著超越了所有从头训练的基线方法。在单 RNA 从头设计基准（RNASolo）上，RiboDiff 的成功率（scRMSD < 5 Å 的样本比例）达到 **97.38%**，而最强基线 MMDiff 的成功率为 0%（Table 1）。scRMSD 从 MMDiff 的 35.7 Å 降至 **3.43 Å**，降幅超过 10 倍；scTM-score 从 0.12 提升至 **0.71**，提升约 6 倍。对于 RNA-蛋白质复合物设计，RiboDiff 的 scRMSD 为 7.43 Å，scTM-score 为 0.422，而 MMDiff 分别为 28.4 Å 和 0.08（Table 2）。在更具挑战性的蛋白质条件 RNA 设计任务中，RiboDiff 在 RF2NA 预训练划分上的 GT-RMSD 为 **13.20 Å**，GT-SeqRec 为 **56.26%**，大幅优于 RNAFlow 的 16.2 Å 和 28.0%（Table 3）。

![[assets/figures/papers/iclr26_0003_cpc63YrVWN_A_Joint_Diffusion_Model_with_Pre-Trained_Priors/figures/003_Table_1.jpg]]
*Table 1: Comparison across methods on single RNA task. Success rate is the percentage of samples with scRMSD \< 5Å. qTMclust diversity uses TM-cutoff 0.45. Average value and standard deviation are reported for all metrics. For MMDIFF, we rerun its official implementation under our setting*

![[assets/figures/papers/iclr26_0003_cpc63YrVWN_A_Joint_Diffusion_Model_with_Pre-Trained_Priors/figures/004_Table_2.jpg]]
*Table 2: Comparison across methods on RNA-protein complex. Average value and standard deviation are reported for all metrics*

![[assets/figures/papers/iclr26_0003_cpc63YrVWN_A_Joint_Diffusion_Model_with_Pre-Trained_Priors/figures/005_Table_3.jpg]]
*Table 3: Comparison across methods on conditional RNA co-design. For MMDiff and RNAFlow, we rerun their official implementation. Note that RMSD is calculated for all atoms*

### 消融研究

消融实验揭示了四个关键设计选择的重要性：

1.  **联合扩散 vs. 交替扩散**: Figure 5 的学习曲线显示，联合扩散（序列和结构同时去噪）在几百步内将 scRMSD 降至约 4 Å，而交替扩散（序列和结构分别去噪）停滞在更高的值，从未达到同等性能。这证明了联合建模对序列-结构共一致性的协同效应。

2.  **预训练先验的必要性**: 不使用预训练 RF2NA 先验的联合扩散训练极不稳定，出现长平台期和高方差，最终性能远低于使用先验的版本（Figure 5）。这直接验证了核心瓶颈——实验结构数据稀缺——以及利用预训练先验作为因果旋钮的有效性。

3.  **损失项贡献**: 对损失项的消融（Table 9）表明，去除全局 RMSD 损失（L_rmsd）影响最大，成功率从 97.38% 骤降至 30.08%，scRMSD 升至 16.72 Å，证实了该损失项对全局正确折叠的关键作用。去除结构对齐损失（L_str）也导致显著下降（成功率 58.64%，scRMSD 5.85 Å），表明 RF2NA 引导的结构先验对鲁棒的共一致性至关重要。去除几何损失（L_geom）和 Lennard-Jones 碰撞损失（L_lj）导致中等程度的性能下降。

4.  **条件化策略**: 在蛋白质条件 RNA 设计中，完整的 RF2NA 条件化（GT-RMSD 13.2, GT-SeqRec 56.3）优于仅序列条件化（16.2, 33.5）、仅结构条件化（15.1, 45.9）和模块化条件化基线（15.5, 38.2）（Table 11），表明复杂耦合提供了可衡量的益处。

### 失败模式与局限性

-   **界面精度瓶颈**: 在蛋白质条件 RNA 设计中，GT-RMSD 为 13.2 Å，仍然较高，表明界面结合精度有待提升。Chai-1 置信度指标中的 iPTM 分数较低（0.166-0.187），也反映了模型对蛋白质-RNA 界面预测的置信度不高（Table 6）。
-   **长 RNA 退化**: 对于长度超过 150 nt 的 RNA，自洽性指标有轻微下降，可能源于累积的扭转噪声和长程共轴堆积效应的建模困难。
-   **两阶段方法失效**: 将骨架生成（RF2NA 扩散）与逆折叠（gRNAde）分离的两阶段流水线，性能远低于 RiboDiff 的联合扩散（成功率 19.34% vs 97.38%，scRMSD 17.59 vs 3.43 Å）（Table 10），证明了序列-结构联合建模的必要性。
-   **计算开销**: 推理时的基于值的强化学习增强（SVDD）虽然有效，但增加了计算成本。

### 补充图表

![[assets/figures/papers/iclr26_0003_cpc63YrVWN_A_Joint_Diffusion_Model_with_Pre-Trained_Priors/figures/006_Table_4.jpg]]
*Table 4: Comparison across rewards with and w/o RL-based inference enhancement. We report the average and standard deviation results under M = 1 0*

![[assets/figures/papers/iclr26_0003_cpc63YrVWN_A_Joint_Diffusion_Model_with_Pre-Trained_Priors/figures/015_Table_5.jpg]]
*Table 5: Results of more self-consistency and diversity metrics on single RNA, RNA-protein complex, and conditional RNA design (RF2NA pre-training split) tasks. Average value and standard deviation are reported for all metrics*



## 定位与知识库关联

RiboDiff 的核心贡献在于将预训练的跨分子结构预测模型 RoseTTAFold2NA (RF2NA) 作为去噪网络嵌入到联合扩散框架中，通过微调而非从头训练来缓解 RNA 结构数据稀缺带来的瓶颈。这一设计选择从根本上改变了生成模型的能力边界。

**与 Baseline 的关系：预训练先验作为因果旋钮**

RiboDiff 与现有方法的关键差异在于去噪网络的初始化方式。从头训练的基线方法（MMDiff、RiboGen）在单 RNA 设计任务上表现极差（MMDiff 成功率为 0%，scRMSD 为 35.7 Å），而 RiboDiff 将成功率提升至 97.38%，scRMSD 降至 3.43 Å。这种数量级的提升并非来自扩散框架本身的创新（RiboDiff 使用的离散+SE(3)等变联合扩散架构与 MMDiff 类似），而是源于 RF2NA 预训练先验的注入。消融实验（Figure 5）明确证实：不使用预训练先验的联合扩散训练极不稳定，出现长平台期和高方差，而使用预训练先验的联合扩散稳定且快速收敛，scRMSD 在几百步内降至 4 Å。这表明预训练先验是 RiboDiff 性能提升的因果旋钮，而非扩散过程设计本身。

**与 Follow-up 的关系：联合扩散 vs 交替扩散 vs 两阶段方法**

RiboDiff 的联合扩散策略（序列和结构同时去噪）在多个维度上优于替代方案：
- **联合扩散 vs 交替扩散**：联合扩散的学习曲线（scRMSD）在几百步内降至 4 Å，而交替扩散（序列和结构分别去噪）停滞在更高值（Figure 5）。这表明序列和结构的耦合去噪过程能够相互提供梯度信号，加速收敛。
- **联合扩散 vs 两阶段方法**：RF2NA 骨架扩散 + gRNAde 逆折叠的两阶段管线性能远低于 RiboDiff（成功率 19.34% vs 97.38%，scRMSD 17.59 vs 3.43 Å）（Table 10）。这揭示了序列-结构共设计中的“信息不对称”问题：先独立生成结构再逆折叠序列会丢失结构-序列之间的双向约束，导致生成的结构无法被后续的序列预测模型有效“解码”。

**适用边界与条件化能力**

RiboDiff 在三种任务上均表现出色：单 RNA 设计（成功率 97.38%）、RNA-蛋白质复合物设计（scRMSD 7.43 Å）、蛋白质条件 RNA 设计（GT-SeqRec 56.26%）。然而，其条件化能力存在明确的边界：
- **条件化策略消融**（Table 11）：完整 RF2NA 条件化（GT-RMSD 13.2 Å, GT-SeqRec 56.3）优于仅序列条件化（16.2 Å, 33.5%）、仅结构条件化（15.1 Å, 45.9%）和模块化条件化（15.5 Å, 38.2%）。这表明蛋白质-RNA 界面的精确建模需要同时利用序列和结构信息，任何单一模态的条件化都会导致性能下降。
- **界面精度瓶颈**：尽管 RiboDiff 在自洽性指标上表现优异，但条件 RNA 设计的 GT-RMSD（13.2 Å）仍然较高，且 iPTM 分数（0.166-0.187）较低，表明模型对蛋白质-RNA 界面的置信度预测不高。这说明预训练先验虽然提供了丰富的结构知识，但在从未见过的新型蛋白质-RNA 界面上，模型的泛化能力仍然有限。

**局限与开放问题**

1. **界面精度提升**：如何将 GT-RMSD 从 13.2 Å 降至更低的水平？可能的路径包括：在训练目标中显式加权界面接触损失、引入可微分的界面能量项、或结合界面聚焦的精细采样策略。

2. **长 RNA 处理**：对于 >150 nt 的 RNA，自洽性指标有轻微下降。这可能是由于累积的扭转噪声和长程共轴堆积效应。如何设计更有效的噪声调度或引入层次化生成策略来应对长程依赖？

3. **环境因素缺失**：模型目前未考虑离子、辅因子或溶剂等环境因素。将这些因素纳入模型需要额外的物理建模或数据增强策略。

4. **采样效率与计算开销**：推理时 RL 增强（SVDD）虽然有效（Table 4），但增加了计算开销。如何结合无调度或流-扩散混合方法实现更快的采样？

5. **与湿实验的闭环**：如何将模型输出与湿实验反馈结合，进行不确定性校准和主动学习？这一方向对于实际药物设计应用至关重要。

6. **统一原子生成模型**：如何扩展到覆盖不同化学物质和界面的统一全局原子生成模型？这需要解决不同分子类型的表示对齐问题。

总体而言，RiboDiff 通过预训练先验注入成功突破了 RNA 结构数据稀缺的瓶颈，但其适用边界受限于界面精度、长 RNA 处理和条件化能力。这些开放问题构成了该领域未来研究的主要方向。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Joint_Diffusion_Model_with_Pre_Trained_Priors_for_RNA_Sequence_Structure_Co_Design.pdf

![[paperPDFs/ICLR_2026/A_Joint_Diffusion_Model_with_Pre_Trained_Priors_for_RNA_Sequence_Structure_Co_Design.pdf]]
