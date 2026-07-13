---
title: "M2D2M: Multi Motion Generation from Text with Discrete Diffusion Models"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/M2D2M_Multi_Motion_Generation_from_Text_with_Discrete_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- MMMDDM
- M2D2M
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 核心调节因素为：① 基于运动标记码本距离与扩散步长的动态转移概率；② 联合采样-独立采样的两阶段去噪策略。
primary_logic: 通过让扩散模型在去噪早期依据标记距离进行更广泛探索（高转移概率给远距离标记），后期逐渐收敛到近距离标记，从而生成连续运动；两阶段采样利用共享去噪步骤融合多动作上下文，再独立精化，在不增加训练参数的前提下实现平滑过渡与个体动作准确性。
claims:
- 动态转移概率显著提升多运动生成的 FID 和平滑度 (Jerk)，消融实验证明 β(d,t) 优于 β(t)。
- 两阶段采样 (TPS) 相比 Handshake 和 SLERP，在保持个体动作 FID 的同时，实现了更接近真实单一运动的 Jerk 值，避免了过度平滑。
- 在 HumanML3D 和 KIT-ML 数据集上，M2D2M 在单运动生成任务中取得了最佳 FID 和 R-Top3，证明动态转移概率也有助于单运动质量。
- TPS 使得仅使用单运动训练的模型能够生成任意长度的多运动序列，无需额外训练或超参数，如 Algorithm 1 所述。
---

# M2D2M: Multi Motion Generation from Text with Discrete Diffusion Models

> [!tip] 核心洞察
> 通过让扩散模型在去噪早期依据标记距离进行更广泛探索（高转移概率给远距离标记），后期逐渐收敛到近距离标记，从而生成连续运动；两阶段采样利用共享去噪步骤融合多动作上下文，再独立精化，在不增加训练参数的前提下实现平滑过渡与个体动作准确性。

| 字段 | 内容 |
|------|------|
| 中文题名 | M2D2M：基于离散扩散模型的多动作文本驱动人体运动生成 |
| 英文题名 | M2D2M: Multi Motion Generation from Text with Discrete Diffusion Models |
| 会议/期刊 | ECCV 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | M2D2M (Multi Motion Discrete Diffusion Model) |
| Dataset | HumanML3D Multi-Motion, HumanML3D Single-Motion, KIT-ML Single-Motion |

> [!tip] 效果简介
> - HumanML3D Multi-Motion (N=4) 上，FID (Individual Motion) ↓ 0.253 ± 0.016 vs T2M-GPT 0.342 ± 0.019 (-0.089)；Jerk (Transition 40 frames) → 1.238 ± 0.008 vs Ground Truth (Single) 1.192 ± 0.005 (+0.046)。
> - HumanML3D Single-Motion 上，FID ↓ 0.087 ± 0.004 vs T2M-GPT 0.116 ± 0.004 (-0.029)。
> - KIT-ML Single-Motion 上，R-Top3 ↑ 0.753 ± 0.006 vs T2M-GPT 0.737 ± 0.006 (+0.016)。

## 概要

**问题瓶颈**：文本驱动的多动作人体运动生成面临两大核心挑战。其一，传统离散扩散模型采用均匀转移概率，在去噪过程中对所有运动标记一视同仁，忽略了码本标记间的语义距离，导致不同动作之间的过渡生硬、缺乏连贯性。其二，现有方法（如 Handshake、SLERP）依赖后处理拼接独立生成的单运动序列，需要手动设定过渡长度等超参数，难以同时保证动作边界的平滑性与个体运动的保真度。

**核心思路**：M2D2M 从两个层面解决上述问题。在扩散机制层面，引入**动态转移概率** $\beta(t, d)$——转移概率不再是均匀的，而是依据运动标记在码本中的距离 $d$ 与当前扩散步长 $t$ 进行 softmax 调制：早期去噪阶段赋予远距离标记更高的转移概率以鼓励探索，后期逐渐收敛至近距离标记以保证生成质量。在生成策略层面，提出**两阶段采样（TPS）**：先对所有动作序列进行联合去噪以融合多动作上下文，再切换至独立去噪以精化每个动作的语义准确性，全程无需额外训练或超参数调节。

**方法定位**：M2D2M 建立在 Motion VQ-VAE 与条件去噪 Transformer 之上，属于离散扩散模型在人体运动生成领域的应用。与 **T2M-GPT** 等自回归方法不同，它利用扩散模型的非自回归特性进行并行去噪；与 **MDM + Handshake** 等 Cartesian 空间扩散方法不同，它在离散标记空间中操作，并通过动态转移概率显式建模标记间语义关系。

**主要发现**：
- 在 HumanML3D 多运动生成（N=4）中，M2D2M 的个体运动 FID 达到 0.253，显著优于 T2M-GPT 的 0.342；过渡区域 Jerk 指标接近真实单运动拼接水平。
- 消融实验证实，动态转移概率 $\beta(d,t)$ 相比均匀 $\beta(t)$ 能同时改善 FID 和平滑度，且两阶段采样中联合去噪步数 $T_s=90$ 时达到最佳平衡。
- 在单运动生成任务上，M2D2M 同样在 HumanML3D 和 KIT-ML 数据集上取得了最优 FID 和 R-Top3，表明动态转移概率对单运动质量亦有正向作用。
- TPS 使仅用单运动数据训练的模型能够生成任意长度的多运动序列，无需多运动联合监督或后处理超参数，如 Algorithm 1 所述。

### 问题背景：文本驱动的多动作人体运动生成

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列。随着扩散模型在连续域图像与运动生成中的成功，研究者开始探索其在离散空间中的潜力。然而，现有工作主要聚焦于单一动作的生成——即给定一句描述（如“一个人向前走”），模型输出一段对应的运动序列。现实应用往往需要生成包含多个连续动作的长时间运动，例如“一个人向前走，然后转身，最后坐下”。将多个独立生成的单运动简单拼接，会在动作边界处产生不自然的跳变，破坏运动的连贯性。

### 现有方法的瓶颈

当前处理多动作序列生成的方法可归为两类，各自存在明显局限：

**后处理拼接策略**：代表性方法包括 **Handshake**（PriorMDM）和 **SLERP**。这些方法先生成独立的单运动片段，再通过手工设计的规则（如线性插值、球面线性插值）在过渡区域进行平滑。其缺陷在于：(1) 需要预设过渡长度这一敏感的超参数；(2) 平滑操作是独立于生成过程的启发式后处理，无法利用文本语义来指导过渡，容易导致动作失真或过度平滑，牺牲个体运动的保真度。

**自回归生成策略**：如 **T2M-GPT** 采用自回归方式逐个生成运动标记，理论上可生成任意长度序列。但自回归模型在生成长序列时面临误差累积问题，且缺乏对多动作间全局上下文的显式建模，过渡区域的质量难以保证。

更深层的问题在于，离散扩散模型通常采用**均匀转移概率**：在正向扩散过程中，所有标记对被赋予相同的概率转移到其他标记或掩码。这一设计忽略了运动标记之间的语义距离——在运动码本中，表示“行走”的标记与“跑步”的标记在语义上相近，而“行走”与“坐下”则相距较远。均匀转移概率无法利用这种结构信息，导致去噪过程在动作边界处缺乏对运动连续性的引导。

### 本文动机与核心思路

针对上述瓶颈，M2D2M 提出两个互补的创新机制：

1. **动态转移概率**：将运动标记间的语义距离引入扩散过程的转移矩阵。在去噪早期，赋予远距离标记更高的转移概率以鼓励全局探索；随着去噪推进，逐渐收缩到近距离标记，实现从粗到细的运动生成。这一设计使扩散模型天然具备生成平滑过渡的能力，无需后处理。

2. **两阶段采样（TPS）**：将多运动生成视为一个统一的去噪过程。首先在联合采样阶段，将多个动作的掩码标记合并，通过共享去噪步骤融合多动作上下文，形成粗粒度的连贯序列轮廓；随后在独立采样阶段，各动作分别精细化，保证个体运动的语义准确性。TPS 无需额外训练或超参数，仅利用单运动训练的模型即可生成任意长度的多运动序列。

这两种机制协同工作：动态转移概率为去噪过程提供了基于标记距离的探索-利用平衡，而两阶段采样则在此基础上实现了多动作上下文的融合与个体保真度的保持。消融实验（Table 5）证实，二者的协同对于收敛到最优解至关重要。

## 核心方法与创新机理

M2D2M 的核心创新在于将离散扩散模型应用于多动作文本驱动的人体运动生成，并针对该范式下的两个关键瓶颈——**动作过渡生硬**与**多运动序列拼接依赖手工后处理**——提出了两项相互协同的 changed slots。

### 创新 1：基于语义距离感知的动态转移概率

传统离散扩散模型（如 VQ-Diffusion）在正向过程中采用均匀转移概率 $\beta_t$，即所有非掩码标记对之间具有相同的转换概率。这一设计忽略了运动标记在码本空间中的语义距离：在去噪早期，模型需要广泛探索以形成动作的粗轮廓，而均匀概率限制了探索范围；在去噪后期，模型应优先收敛到语义相近的标记以保证动作连贯性，而均匀概率无法提供这种约束。

M2D2M 提出动态转移概率 $\beta(t, d)$，将转移概率建模为扩散步长 $t$ 与标记间距离 $d$ 的联合函数：

$$\beta(t, d) = (1 - \gamma_t - \alpha_t) \cdot \mathrm{softmax}_d\left(\eta \cdot \frac{t}{T} \cdot \frac{d}{K}\right)$$

其核心机制为：在去噪早期（$t$ 较大），softmax 分布趋于均匀，允许模型以较高概率跳转到距离较远的标记，实现**广泛探索**；随着 $t$ 减小，softmax 逐渐收缩，高转移概率集中于距离较近的标记，模型进入**精细利用**阶段。这一设计使得扩散过程能够生成语义连贯且平滑的运动序列，而无需额外训练参数。

消融实验（Table 5, Table 7）证实，$\beta(t,d)$ 相较于均匀 $\beta(t)$ 在多运动生成中显著改善了 FID 和 Jerk 指标，且随着尺度因子 $\eta$ 减小，Jerk 更接近真实运动水平。此外，在 HumanML3D 和 KIT-ML 的单运动生成任务中，M2D2M 取得了最佳 FID 和 R-Top3（Table 8, Table 9），表明动态转移概率对单运动质量同样具有增益。

### 创新 2：无需手工后处理的两阶段采样策略

现有多运动生成方法（如 **PriorMDM** 的 Handshake 算法、SLERP 球面线性插值）依赖手工设计的后处理规则来拼接独立生成的单运动序列。这类方法存在两个根本缺陷：（1）需要预设过渡长度等超参数，对不同动作组合缺乏适应性；（2）在去噪完成后进行拼接，无法利用扩散过程的上下文信息来协调动作间的过渡。

M2D2M 提出**两阶段采样**，将多运动生成内化到扩散去噪过程中：

- **联合采样阶段**（前 $T_s$ 步）：将多个动作的掩码标记合并，通过共享的去噪 Transformer 进行集体去噪。此阶段使各动作段落在扩散早期即获得彼此的上下文信息，形成平滑的过渡轮廓。
- **独立采样阶段**（剩余 $T - T_s$ 步）：将合并序列拆分，各动作段独立完成剩余去噪步骤。此阶段保证每个动作的语义准确性和个体保真度，避免因过度共享上下文而导致动作特征模糊。

TPS 的关键优势在于：（1）无需任何后处理或超参数调节，模型仅需单运动数据训练即可生成任意长度的多运动序列；（2）联合与独立阶段的边界 $T_s$ 控制着过渡平滑性与动作保真度之间的权衡。消融实验（Table 5）表明，$T_s = 90$ 时达到最佳的过渡 FID 和平滑度；$T_s$ 过大会降低个体动作保真度，过小则过渡生硬。

与 Handshake 和 SLERP 的对比（Table 6, Fig. 5）进一步显示，TPS 在保持个体动作 FID 的同时，实现了更接近真实单一运动的 Jerk 值，避免了后处理方法的过度平滑问题。Fig. 3 从算法层面揭示了 TPS 与后处理方法的本质差异：TPS 是单阶段生成算法，而 Handshake/SLERP 需要先完成独立运动生成再进行拼接。

### 两项创新的协同效应

动态转移概率与两阶段采样并非孤立改进，而是形成正向协同：动态转移概率在联合采样阶段促进跨动作标记的语义探索，使过渡轮廓更加自然；在独立采样阶段则约束标记收敛到语义近邻，保持动作准确性。消融实验（Table 5）明确指出，两者的协同对于收敛到最优解至关重要。

M2D2M 的整体 pipeline 围绕“离散扩散生成 + 多动作上下文融合”这一核心思路构建，由四个关键模块串联而成：**运动 VQ-VAE**、**动态转移概率**、**去噪 Transformer** 和**两阶段采样 (TPS)**。系统输入为自然语言动作描述，输出为连续人体运动序列；在多动作场景下，输入被分解为若干动作短句，分别作为条件注入生成过程。

### 1. 运动 VQ-VAE：连续运动 → 离散标记

首先，一个 **Motion VQ-VAE** 将连续人体运动序列压缩到离散码本空间。编码器将运动数据 $\mathbf{x}$ 映射为潜在向量 $\mathbf{z}$，通过最近邻查找替换为码本中的离散标记 $\mathbf{z}_q$，解码器再从这些标记重建运动 $\hat{\mathbf{x}}$。训练目标为三项损失之和：

$$
\mathcal{L}_{\mathrm{VQ}} = \|\mathbf{x} - \hat{\mathbf{x}}\|_2 + \|\mathbf{z}_q - \mathrm{sg}[\mathbf{z}]\|_2 + \lambda_{\mathrm{VQ}} \|\mathrm{sg}[\mathbf{z}_q] - \mathbf{z}\|_2
$$

这一离散化步骤（Fig. 2(a)）为后续的离散扩散建模提供了可操作的标记序列，码本中标记间的语义距离（Fig. 4(a) 的 PCA 可视化）是后续动态转移概率设计的基础。

![[assets/figures/papers/paper_list_l1870_M2D2M_Multi_Motion_Generation_from_Text_with_Discrete_Diffusion_Models/figures/002_Figure_2.jpg]]
*Figure 2: Overview of M2D2M. We train a (a) VQ-VAE to obtain motion tokens, which is subsequently used to train a (b) Denoising Transformer for the discrete diffusion model. In generating human motion, we follow the (c) standard denoising process for single-motion generation and (d) employ Two-Phase Sampling (TPS) for multimotion generation. A \<MASK> token is denoted as ‘M’ in the figure*

### 2. 动态转移概率：标记距离驱动的扩散探索

标准离散扩散模型使用均匀转移概率 $\beta_t$，即任何标记对都以相同概率相互转换。M2D2M 将其替换为**基于标记距离与扩散步长的动态转移概率** $\beta(t, d)$：

$$
\beta(t, d) = (1 - \gamma_t - \alpha_t) \cdot \mathrm{softmax}_d\left(\eta \cdot \frac{t}{T} \cdot \frac{d}{K}\right)
$$

其中 $d$ 为码本中两标记间的距离（消融实验表明 L2 Rank 距离效果最佳），$t$ 为当前扩散步数，$\eta$ 为尺度因子。该设计使得：**早期扩散步**（$t$ 较大）赋予远距离标记更高的转移概率，鼓励模型在语义空间中进行广泛探索；**后期扩散步**（$t$ 较小）则收缩到近距离标记，使生成的运动趋于连续平滑。转移矩阵随之变为：

$$
\mathbf{Q}_t = \begin{bmatrix} \frac{\hat{\mathbf{Q}}_t}{\gamma_t \cdot \mathbf{1}^\top} & \mathbf{1} \end{bmatrix},\quad \hat{\mathbf{Q}}_t = \alpha_t \mathbf{I} + \beta_{(t, d_{i,j})} \mathbf{1}\mathbf{1}^\top
$$

这一机制（Fig. 4(b)）是解决多动作过渡生硬问题的关键因果旋钮。

### 3. 去噪 Transformer：条件生成核心

去噪网络采用 **Denoising Transformer** 架构（Fig. 2(b)），集成自适应层归一化 (AdaLN)、相对位置编码 (RPE)、交叉注意力（接收文本条件）以及无分类器引导。训练时，模型学习从带噪标记 $z_t$ 预测干净标记 $z_0$，损失函数为变分下界损失与去噪损失的加权和：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{vlb}} + \lambda \mathbb{E}_{z_t \sim q(z_t|z_0)}[-\log p_\theta(z_0 | z_t, y)]
$$

推理时，通过预测干净标记分布并边缘化后验 $q(z_{t-1}|z_t, z_0)$ 来逐步去噪，并采用无分类器引导以增强文本条件控制：

$$
\log p_\theta(z_{t-1}|z_t, y) = (s+1)\log p_\theta(z_{t-1}|z_t, y) - s\log p_\theta(z_{t-1}|z_t, \varnothing)
$$

### 4. 两阶段采样 (TPS)：多动作生成无需后处理

多动作生成的核心瓶颈在于：独立生成各动作再拼接会导致过渡生硬，而现有后处理方法（如 Handshake、SLERP）依赖超参数调节过渡长度。M2D2M 的 **Two-Phase Sampling**（Fig. 2(d), Algorithm 1）将去噪过程分为两个阶段：

- **联合采样阶段**（前 $T_s$ 步）：将多个动作的掩码标记合并，由去噪 Transformer 集体去噪。此时不同动作的标记共享去噪上下文，模型在粗粒度上协调动作间的过渡区域。
- **独立采样阶段**（剩余 $T - T_s$ 步）：将标记按动作拆分，各自独立完成去噪。这保证了每个动作的语义准确性和个体运动保真度，避免过度平滑。

TPS 使得仅用单运动数据训练的模型能够生成任意长度的多运动序列，无需额外训练或手工设定过渡超参数。消融实验表明，$T_s=90$ 时过渡 FID 和平滑度达到最佳平衡（Table 5）。

### 输入输出流总结

1. **输入**：自然语言动作描述（多动作场景下先分解为动作动词再重构为条件句，见 Appendix Fig. 1）。
2. **编码**：文本条件经交叉注意力注入去噪 Transformer；运动经 VQ-VAE 编码为离散标记。
3. **生成**：从全掩码标记出发，经 $T$ 步逆向扩散（单运动为标准去噪，多运动为 TPS）逐步恢复干净标记。
4. **解码**：最终标记序列由 VQ-VAE 解码器重建为连续人体运动序列。

整个 pipeline 的模块关系清晰：VQ-VAE 提供离散表示空间，动态转移概率在该空间内调控探索-利用平衡，去噪 Transformer 执行条件生成，TPS 在不增加参数的前提下实现多动作的平滑拼接。

### 1. 运动离散化：Motion VQ‑VAE

连续人体运动序列 $\mathbf{x}$ 首先通过一个 VQ‑VAE 映射到离散码本空间，得到标记序列 $\mathbf{z}_q$。训练目标由三项组成（Eq. 6）：

$$
\mathcal{L}_{\mathrm{VQ}} = \|\mathbf{x} - \hat{\mathbf{x}}\|_2 + \|\mathbf{z}_q - \mathrm{sg}[\mathbf{z}]\|_2 + \lambda_{\mathrm{VQ}} \|\mathrm{sg}[\mathbf{z}_q] - \mathbf{z}\|_2
$$

- 第一项：重建损失，保证解码器 $\hat{\mathbf{x}}$ 与原始运动一致；
- 第二项：码本损失，推动码本向量向编码器输出 $\mathbf{z}$ 靠拢；
- 第三项：承诺损失，约束编码器输出不偏离已选码本向量过远，$\lambda_{\mathrm{VQ}}$ 控制权重。

该模块为后续离散扩散模型提供语义紧凑的离散运动标记，是单运动与多运动生成的共同基础（Fig. 2(a)）。

### 2. 离散扩散前向过程与原始转移矩阵

离散扩散模型在标记空间上定义前向 Markov 链。从 $z_{t-1}$ 转移到 $z_t$ 的概率由转移矩阵 $\mathbf{Q}_t$ 给出（Eq. 1）：

$$
q(z_t \mid z_{t-1}) = \mathbf{v}^{\top}(z_t) \mathbf{Q}_t \mathbf{v}(z_{t-1})
$$

其中 $\mathbf{v}(z)$ 是标记 $z$ 的独热向量。原始 VQ‑Diffusion 采用掩码‑替换策略，转移矩阵形如（Eq. 2）：

$$
\mathbf{Q}_t = \begin{bmatrix} \frac{\hat{\mathbf{Q}}_t}{\gamma_t \cdot \mathbf{1}^{\top}} & \mathbf{0} \\ \mathbf{1} \end{bmatrix}, \quad \hat{\mathbf{Q}}_t = \alpha_t \mathbf{I} + \beta_t \mathbf{1}\mathbf{1}^{\top}
$$

- $\alpha_t$：保持当前标记的概率；
- $\beta_t$：均匀转移到其他任一标记的概率；
- $\gamma_t$：转移到特殊 `[MASK]` 标记的概率，且 $\alpha_t = 1 - K\beta_t - \gamma_t$（$K$ 为码本大小）。

**瓶颈**：$\beta_t$ 对所有标记对一视同仁，忽略了运动标记之间的语义距离，导致多运动过渡时产生生硬跳变。

### 3. 动态转移概率（核心创新一）

为在扩散过程中注入标记距离先验，M2D2M 将均匀 $\beta_t$ 替换为依赖标记距离 $d$ 和扩散步长 $t$ 的动态概率 $\beta(t, d)$（Eq. 7）：

$$
\beta(t, d) = (1 - \gamma_t - \alpha_t) \cdot \mathrm{softmax}_d\!\left(\eta \cdot \frac{t}{T} \cdot \frac{d}{K}\right)
$$

- $d$：两个运动标记在码本空间中的距离（消融实验表明 L2 Rank 距离效果最优，Table 3 App.）；
- $t/T$：当前扩散步长占比，早期 $t$ 大，softmax 分布趋于均匀，允许远距离标记间的高转移概率，促进全局探索；后期 $t$ 小，分布尖锐化，转移集中在近距离标记，实现局部精化；
- $\eta$：尺度因子，控制 softmax 的锐度。$\eta$ 越小，后期越倾向于近距离转移，Jerk 更接近真实运动（Table 7）；
- $(1 - \gamma_t - \alpha_t)$：保证每步总转移概率质量守恒。

对应的新转移矩阵为（Eq. 8）：

$$
\mathbf{Q}_t = \begin{bmatrix} \frac{\hat{\mathbf{Q}}_t}{\gamma_t \cdot \mathbf{1}^{\top}} & \mathbf{0} \\ \mathbf{1} \end{bmatrix}, \quad \hat{\mathbf{Q}}_t = \alpha_t \mathbf{I} + \beta_{(t, d_{i,j})} \mathbf{1}\mathbf{1}^{\top}
$$

其中 $\beta_{(t, d_{i,j})}$ 根据标记对 $(i,j)$ 的具体距离 $d_{i,j}$ 计算。Fig. 4(b) 展示了不同 $t$ 下 $\beta(t,d)$ 随 $d$ 的变化曲线，直观体现了“先探索、后利用”的机制。

### 4. 训练目标与反向去噪

模型通过预测干净标记 $\tilde{z}_0$ 来参数化反向分布（Eq. 4）：

$$
p_\theta(z_{t-1} \mid z_t, y) = \sum_{\tilde{z}_0=1}^{K} q(z_{t-1} \mid z_t, \tilde{z}_0) \, p_\theta(\tilde{z}_0 \mid z_t, y)
$$

其中可处理后验 $q(z_{t-1} \mid z_t, z_0)$ 由 Eq. 5 给出。训练损失为变分下界与辅助去噪损失的加权和（Eq. 3）：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{vlb}} + \lambda \mathbb{E}_{z_t \sim q(z_t \mid z_0)} [-\log p_\theta(z_0 \mid z_t, y)]
$$

推理时采用无分类器引导（Eq. 9），引导尺度 $s$ 平衡文本条件 $y$ 与无条件 $\varnothing$ 的 log 概率：

$$
\log p_\theta(z_{t-1} \mid z_t, y) = (s+1) \log p_\theta(z_{t-1} \mid z_t, y) - s \log p_\theta(z_{t-1} \mid z_t, \varnothing)
$$

### 5. 两阶段采样 TPS（核心创新二）

针对多运动生成，TPS 将去噪过程分为两个阶段（Algorithm 1，Fig. 2(d)）：

- **联合采样阶段**（前 $T_s$ 步）：将多个动作的 `[MASK]` 标记拼接，通过同一个去噪 Transformer 集体去噪。此阶段利用共享上下文融合动作边界信息，建立平滑过渡轮廓；
- **独立采样阶段**（剩余 $T - T_s$ 步）：将序列按动作边界拆分，各自独立完成剩余去噪。此阶段保证每个动作的语义准确性不受其他动作干扰。

TPS 的核心优势在于：无需 Handshake 或 SLERP 等后处理，无需设定过渡长度超参数，且模型仅在单运动数据上训练即可生成任意长度的多运动序列（Fig. 3）。消融实验表明 $T_s=90$ 时过渡 FID 与平滑度达到最佳平衡（Table 5）。

![[assets/figures/papers/paper_list_l1870_M2D2M_Multi_Motion_Generation_from_Text_with_Discrete_Diffusion_Models/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of Multi-Motion Generation Algorithms. Unlike heuristic post-processing methods for combining independent motions such as Handshake [49] and SLERP [6], TPS is a single-stage algorithm for a multi-motion generation that does not require completed individual motions or a hyper-parameter for transition length*

### 6. 过渡平滑性度量：Jerk

为量化过渡的自然程度，引入无量纲急动度 Jerk（Eq. 10）：

$$
\mathrm{Jerk} = \sum_{p} \ln\frac{1}{v_{p,\mathrm{peak}}^2} \int_{t_1}^{t_2} \left\| \frac{d}{dt} \mathbf{a}_p(t) \right\|_2^2 dt
$$

其中 $\mathbf{a}_p(t)$ 为关节 $p$ 的加速度，$v_{p,\mathrm{peak}}$ 为峰值速度，积分区间 $[t_1, t_2]$ 对应过渡帧。该指标衡量加速度变化的剧烈程度，值越低表示过渡越平滑。M2D2M 在该指标上显著优于拼接基线，且接近真实单一运动的 Jerk 水平（Table 1，Fig. 5）。

## 实验与关键发现

### 主实验结果

M2D2M 在多运动与单运动生成任务上均展现出显著优势，核心指标包括 FID（个体运动质量）、R-Top3（文本-运动匹配度）和 Jerk（过渡平滑度）。

#### 多运动生成

在 HumanML3D 多运动测试集（N=4）上，M2D2M 在个体运动 FID 上达到 **0.253 ± 0.016**，显著优于 T2M-GPT（0.342 ± 0.019）和 PriorMDM（0.376 ± 0.024）（Table 1）。在过渡平滑性方面，M2D2M 的 Jerk 值为 **1.238 ± 0.008**，与真值单一运动的 1.192 ± 0.005 最为接近，而 T2M-GPT 的 Jerk 高达 1.310 ± 0.008，表明其过渡更为生硬。值得注意的是，真值拼接（GT concat）的 Jerk 为 1.416 ± 0.005，远高于所有生成方法，这揭示了简单拼接真实运动本身就会引入不自然的加速度突变——因此 Jerk 的“理想值”并非越低越好，而是应逼近独立采样的真实单一运动 Jerk。

在 KIT-ML 数据集上，M2D2M 同样取得最佳个体运动 FID（0.296 ± 0.014）和 R-Top3（0.716 ± 0.005），过渡 FID 也优于所有基线（Table 2）。跨数据集的稳定表现验证了方法的泛化性。

#### 单运动生成

动态转移概率的改进同样惠及单运动生成。在 HumanML3D 上，M2D2M 取得最佳 FID（**0.087 ± 0.004**）和 R-Top3（**0.733 ± 0.005**），全面超越 T2M-GPT（FID 0.116 ± 0.004）和 MDM（FID 0.544 ± 0.044）（Table 8）。在 KIT-ML 上，M2D2M 的 R-Top3 达到 **0.753 ± 0.006**，FID 为 0.159 ± 0.005，均处于最优水平（Table 9）。这表明基于码本距离的动态转移概率不仅有助于多运动过渡，也提升了单运动本身的生成质量。

### 消融实验

#### 动态转移概率 β(d,t) 的关键作用

Table 5 的消融实验直接对比了动态 β(d,t) 与均匀 β(t) 的效果。在 HumanML3D 多运动生成中，使用动态 β(d,t) 将个体运动 FID 从 0.440 ± 0.009 降至 0.253 ± 0.016，过渡 FID 从 0.587 ± 0.009 降至 0.462 ± 0.008，Jerk 从 1.253 ± 0.007 优化至 1.238 ± 0.008。Table 7 进一步表明，随着尺度因子 η 减小（从 1.0 降至 0.1），Jerk 逐渐接近真实运动水平，验证了动态概率函数中 softmax 温度对探索-利用平衡的调控能力。

![[assets/figures/papers/paper_list_l1870_M2D2M_Multi_Motion_Generation_from_Text_with_Discrete_Diffusion_Models/figures/011_Table_5.jpg]]
*Table 5: Ablation studies on multi-motion generation performance on HumanML3D. ‘Individual Motion’ denotes individual motions within our motion boundaries*

![[assets/figures/papers/paper_list_l1870_M2D2M_Multi_Motion_Generation_from_Text_with_Discrete_Diffusion_Models/figures/020_Table_7.jpg]]
*Table 7: Multi-motion generation performance across a different number of independent denoising steps*

#### 两阶段采样 (TPS) 中 T_s 的影响

联合去噪步数 T_s 是 TPS 的核心超参数。Table 5 显示，当 T_s = 90 时，过渡 FID 达到最优（0.462 ± 0.008），Jerk 也最接近真值。T_s 过小（如 10）时，联合上下文不足，过渡 FID 升至 0.478 ± 0.009；T_s 过大（如 170）时，联合去噪过度融合动作特征，个体运动 FID 劣化至 0.274 ± 0.011。这揭示了 TPS 在“平滑过渡”与“动作保真度”之间的折衷机制——联合采样提供多动作上下文以平滑边界，独立采样则防止动作语义被稀释。

#### 距离函数选择

附录 Table 3 对比了不同距离函数对动态转移概率的影响。L2 Rank 距离取得最佳 FID（0.087 ± 0.004），优于直接使用 L2 距离（0.091 ± 0.003）或余弦距离（0.090 ± 0.004）。这表明在离散码本空间中，保持标记间相对排序信息比绝对距离度量更有利于扩散过程的探索。

#### 与后处理方法的对比

Table 6 将 TPS 与 Handshake、SLERP 等后处理平滑方法在 MDM 框架下进行了公平对比。结果显示，TPS 在过渡 FID 和 Jerk 上均优于 Handshake 和 SLERP，且不需要设定过渡长度超参数。SLERP 虽然 Jerk 较低（1.194 ± 0.005），但其个体运动 FID 明显劣化（0.631 ± 0.013），说明球面插值过度平滑了运动细节，牺牲了动作保真度。TPS 则在平滑性与保真度之间取得了更好的平衡。

![[assets/figures/papers/paper_list_l1870_M2D2M_Multi_Motion_Generation_from_Text_with_Discrete_Diffusion_Models/figures/012_Table_6.jpg]]
*Table 6: Multi-motion generation on different smoothing methods on HumanML3D*

### 失败模式与局限

1. **评估指标覆盖不足**：当前使用的 Jerk 指标仅衡量加速度导数的物理平滑性，无法评估过渡动作的语义合理性（例如“走路”到“跳跃”的过渡是否自然）。这是一个开放问题，需要设计更全面的多运动评估体系。

2. **长序列扩展瓶颈**：当动作数量 N 增大时，联合采样阶段需同时处理所有动作的掩码标记，计算量接近线性增长（附录 Fig. 4 展示了推理时间与序列长度的线性关系）。对于 N 极大的场景（如长篇幅动作描述），这仍可能成为效率瓶颈。

3. **码本表达能力边界**：模型依赖 VQ-VAE 的离散码本表示运动。对于码本中未充分覆盖的罕见过渡动作，离散标记可能无法精确表达细微的运动变化。这本质上是 VQ-VAE 压缩率与重建精度之间的权衡问题。

4. **训练数据限制**：模型仅在单运动数据集上训练，未利用多运动数据的联合监督。这可能限制了模型在复杂多动作情境下的表现上限，尤其是在需要理解动作间因果或时序依赖的场景中。

### 重要图表结论

- **Fig. 1**：定性对比显示，M2D2M 在动作过渡区域（绿色框标注）呈现出连贯渐进的姿态变化，而基线方法常出现突变或不自然的停顿，验证了 TPS 在视觉平滑性上的优势。

![[assets/figures/papers/paper_list_l1870_M2D2M_Multi_Motion_Generation_from_Text_with_Discrete_Diffusion_Models/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative Comparison of Multi-Motion Sequences. In the transitions highlighted by the green boxes, our model shows a consistent and gradual progression of poses compared to others. This indicates that our model not only produces more realistic and smooth motions but also maintains the fidelity of each motion segment, aligning accurately with the corresponding action descriptions on top*

- **Fig. 5**：速度与 Jerk 曲线对比表明，M2D2M 生成的过渡在速度变化模式上与真值拼接存在本质差异——真值拼接在边界处出现尖锐的 Jerk 峰值，而 M2D2M 的 Jerk 曲线更为平缓，印证了 TPS 从扩散过程内部实现平滑过渡的机制优势。

- **Table 5**：动态 β(d,t) 与 TPS 的协同作用至关重要——单独使用任一组件的性能均显著劣于完整方法，表明两个创新点存在互补效应：动态转移概率为联合采样提供了更合理的探索空间，而 TPS 则利用该空间实现动作间的平滑衔接。

## 定位与知识库关联

### 1. 方法在领域中的位置

M2D2M 处于**文本驱动人体运动生成**与**离散扩散模型**的交叉点，其核心贡献——动态转移概率与两阶段采样——直接回应了多动作序列生成中长期存在的两个瓶颈：动作过渡的物理平滑性，以及个体运动语义的保真度。

从方法演进脉络看，人体运动生成经历了三个关键阶段：

1.  **连续扩散模型**：以 **MDM** (Tevet et al., ICCV 2023) 为代表，直接在 Cartesian 空间对运动序列进行扩散建模，生成质量高，但缺乏对序列长度的灵活控制，多动作生成依赖 **Handshake** (Shafir et al., ICCV 2023) 等后处理算法，需手动设定过渡长度超参数，且过渡区域易出现物理不自然。
2.  **自回归离散模型**：以 **T2M-GPT** (Zhang et al., CVPR 2023) 为代表，将运动量化到 VQ-VAE 码本空间，利用 GPT 进行自回归生成。该方法天然支持变长序列，但多动作生成仅通过简单拼接令牌实现，缺乏对过渡区域的显式建模，导致动作连接处出现突变。
3.  **离散扩散模型**：M2D2M 继承 VQ-Diffusion (Gu et al., ECCV 2022) 的掩码替换扩散范式，但针对人体运动这一特殊模态进行了两项根本性改造：
    - **转移概率的语义化**：传统离散扩散使用均匀转移概率 $\beta_t$，对所有标记对一视同仁。M2D2M 引入基于码本标记距离 $d$ 的动态转移概率 $\beta(t, d)$（Eq. 7-8），使得扩散过程在早期（$t$ 大）允许标记向语义较远的区域探索，后期（$t$ 小）收敛到语义相近的标记，从而在去噪过程中自然形成连续运动流形。
    - **采样策略的上下文感知**：两阶段采样（TPS, Algorithm 1）将多动作生成从“生成-拼接”范式转变为“联合去噪-独立精化”范式。第一阶段在掩码空间合并多动作标记，通过共享去噪步骤融合上下文信息，建立平滑过渡轮廓；第二阶段独立去噪，确保每个动作的语义准确性不被其他动作污染。

### 2. 与基线方法的本质差异

| 维度 | 基线方法 | M2D2M |
|------|---------|-------|
| **多动作生成机制** | 分别生成单运动后，用 Handshake 或 SLERP 进行后处理拼接，需设定过渡长度超参数 | 单阶段两阶段采样，无需额外超参数，过渡在去噪过程中自然涌现 |
| **转移概率设计** | 均匀 $\beta_t$，所有标记对等概率转移 | 动态 $\beta(t, d)$，基于标记距离的 softmax 调制，实现探索-利用平衡 |
| **过渡平滑性来源** | 手工规则（如 Handshake 的固定帧混合） | 联合去噪阶段的上下文融合，过渡平滑性是扩散过程的涌现属性 |
| **训练数据需求** | 部分方法需多运动数据集联合训练 | 仅使用单运动数据集训练，TPS 使模型泛化到任意长度多运动序列 |

**关键证据**：
- Table 6 显示，在 MDM 上应用 TPS 后，FID 从 0.342 降至 0.253，Jerk 从 1.453 降至 1.238，证明 TPS 的收益独立于底层生成模型。
- Table 5 消融实验表明，同时使用动态转移概率和 TPS 时，个体运动 FID 和过渡 Jerk 均达到最优；单独使用任一组分均导致性能下降，验证了两者的协同效应。

### 3. 适用边界与局限

**适用场景**：
- 文本驱动的多动作人体运动序列生成，动作数量 $N$ 在 2–8 范围内表现出色（Table 4, App.）。
- 单运动生成同样受益于动态转移概率，在 HumanML3D 和 KIT-ML 上取得了最佳 FID 和 R-Top3（Table 8, 9）。

**已知局限**：
1.  **评估指标不完善**：当前使用的 Jerk 指标仅衡量加速度导数的积分，无法全面评估多运动序列的语义一致性、全局连贯性和过渡自然度。论文明确指出该指标“尚不能涵盖所有可能的过渡场景”。
2.  **训练数据限制**：模型仅在单运动数据集上训练，未利用多运动数据集的联合监督。这可能限制其在复杂多动作情境（如动作间存在因果关系或时序依赖）下的表现上限。
3.  **长序列计算瓶颈**：对于动作数量 $N$ 极大的情况，联合采样阶段的计算量几乎线性增长，可能成为生成特长序列的瓶颈。附录 Fig. 4 显示推理时间随序列长度线性增加。
4.  **码本表达能力边界**：基于 VQ-VAE 的离散标记可能不足以表达所有细微运动变化，尤其对于不存在于码本中的罕见过渡动作。这属于离散表示方法的固有局限。

### 4. 开放问题与后续方向

1.  **自适应参数优化**：动态转移概率中的尺度因子 $\eta$ 目前为固定值。能否设计机制使其根据动作类型、序列长度自动调整？两阶段采样的联合/独立边界 $T_s$ 能否根据输入文本自适应确定，而非固定为 90 步？

2.  **多运动评估体系**：亟需设计更全面的多运动评估指标，同时衡量动作语义一致性（每个片段是否准确对应文本描述）、过渡自然度（连接处是否物理合理）和全局连贯性（整体序列是否构成有意义的动作叙事）。

3.  **码本表示增强**：能否通过增大码本容量、引入层次化码本或连续-离散混合表示，提升对罕见过渡动作的表达能力？

4.  **多运动联合训练**：若能构建多运动数据集进行联合训练，模型可能学习到动作间的时序依赖和因果关系，进一步提升复杂多动作情境下的生成质量。

5.  **与其他模态的融合**：当前仅以文本为条件，未来可扩展至音频、场景上下文等多模态条件，实现更丰富的多动作序列控制。

## 原文 PDF

![[paperPDFs/ECCV_2024/M2D2M_Multi_Motion_Generation_from_Text_with_Discrete_Diffusion_Models.pdf]]
