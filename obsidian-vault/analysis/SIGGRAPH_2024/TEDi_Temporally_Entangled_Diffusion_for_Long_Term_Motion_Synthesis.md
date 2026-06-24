---
title: TEDi Temporally Entangled Diffusion for Long Term Motion Synthesis
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis.pdf
project_link: https://threedle.github.io/TEDi
aliases:
- TTED
- TTEDLTMS
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将扩散过程的时间轴与运动序列的时间轴进行纠缠：在训练时引入随时间变化的噪声调度（随机调度和单调调度混合），在推理时维护一个具有单调递增噪声的运动缓冲区，实现自回归式的逐帧生成与缓冲区滑动。
primary_logic: 通过使扩散模型适应帧级变化噪声水平，可以利用扩散过程的逐步去噪机制来持续产生新的干净运动帧，同时缓冲区中的噪声帧承载了未来运动的隐含信息，从而实现无限长、高质量的运动序列合成。
claims:
- TEDi通过注入随时间变化的噪声水平（随机和单调调度）扩展了标准DDPM框架，在训练时使用混合调度（p=2/3），使模型能够处理帧级噪声变化。
- TEDi的推理缓冲区递归生成机制（弹出干净帧，推入噪声帧）能够连续生成任意长度运动序列，避免了现有方法的缝合伪影和退化问题。
- 感知研究表明，TEDi在运动多样性和质量上均显著优于MDM、ACRNN和Motion VAE，用户偏好计数TEDi多样性34/质量33，MDM为12/17。
- 消融实验证实，若无随机噪声调度（仅使用单调调度），模型生成的运动会崩溃，多样性和长期稳定性显著下降。
---

# TEDi Temporally Entangled Diffusion for Long Term Motion Synthesis

> [!tip] 核心洞察
> 通过使扩散模型适应帧级变化噪声水平，可以利用扩散过程的逐步去噪机制来持续产生新的干净运动帧，同时缓冲区中的噪声帧承载了未来运动的隐含信息，从而实现无限长、高质量的运动序列合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | TEDi：用于长时运动合成的时序纠缠扩散 |
| 英文题名 | TEDi Temporally Entangled Diffusion for Long Term Motion Synthesis |
| 会议/期刊 | SIGGRAPH 2024 |
| Links |  [Project](https://threedle.github.io/TEDi)|
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TEDi (Temporally-Entangled Diffusion) |
| Dataset | Perceptual study |

> [!tip] 效果简介
> - Perceptual study (user preference survey, n=35 participants) 上，Diversity score (respondent count preferring each method) 34 vs 12 (MDM) (+22)；Quality score (respondent count preferring each method) 33 vs 17 (MDM) (+16)。

## 概述

**瓶颈**：现有的基于扩散的运动生成模型（如MDM）仅能一次性生成固定长度的短序列，无法直接合成长时间运动。将多个短序列进行拼接会产生明显的缝合伪影，而基于循环神经网络（RNN）的自回归方法（如ACRNN）在长时生成中容易出现遗忘和退化，导致输出质量随序列增长而急剧下降。

**核心思路**：TEDi（Temporally-Entangled Diffusion）提出将扩散过程的时间轴与运动序列的时间轴进行“纠缠”。具体而言，在训练阶段引入随时间变化的噪声调度——以概率混合使用随机调度和单调调度——使模型学会处理帧级变化的噪声水平；在推理阶段，维护一个噪声水平单调递增的运动缓冲区，通过“去噪→弹出干净帧→推入新噪声帧”的自回归循环，实现无限长运动序列的连续生成。这一机制使得扩散模型的逐步去噪能力被转化为持续产出新运动帧的能力，同时缓冲区中的噪声帧隐式编码了未来运动的信息。

**方法定位**：TEDi对标准DDPM框架进行了三处关键改造：（1）将固定的时间不变噪声替换为帧级变化的噪声调度；（2）将一次性生成范式改为基于运动缓冲区的自回归生成范式；（3）在训练损失中联合优化扩散损失、基于前向运动学的位置损失和足部接触损失，以提升生成运动的物理合理性。

**主要结果**：在包含35名参与者的感知研究中，TEDi在运动多样性（34票 vs MDM的12票）和运动质量（33票 vs MDM的17票）上均显著优于MDM、ACRNN和Motion VAE等基线方法。消融实验证实，随机噪声调度是避免运动生成崩溃和维持长期多样性的关键因素——若仅使用单调调度，生成运动的方差会大幅下降。TEDi还支持运动引导生成和轨迹控制等扩展应用，能够根据给定的关键姿态或路径约束合成自然的长时运动。

## 背景与动机

### 问题背景

生成逼真且多样化的人体运动序列是计算机图形学与具身人工智能领域的核心挑战之一，其应用涵盖动画制作、虚拟角色控制、机器人运动规划等。近年来，扩散模型（Diffusion Models）在图像、视频和运动生成任务中展现出强大的表现力，逐步成为运动合成的主流范式。然而，现有基于扩散的运动生成方法存在一个根本性局限：**它们被设计为一次性生成固定长度的短序列，无法直接合成任意长度的长时运动**。

当需要生成长时运动时，现有方法通常采用两种策略：一是将多个短序列进行拼接，但这会在拼接边界产生明显的**缝合伪影（stitching artifacts）**，破坏运动的连贯性；二是借助循环神经网络（RNN）等自回归模型进行逐帧外推，但RNN方法在长时生成中容易出现**遗忘与退化输出**，导致运动质量随时间推移而急剧下降。

### 现有方法缺口

具体而言，当前运动生成方法面临以下瓶颈：

1. **固定长度限制**：标准扩散模型（如DDPM）在整个序列上施加同一噪声水平，生成过程要求所有帧共享相同的扩散时间步，因此只能输出预设长度的运动，无法灵活扩展。

2. **拼接伪影**：基于in-painting的扩展方案（如**MDM**，Tevet et al., 2022）试图通过局部修复来衔接短序列，但边界处仍存在明显的不连续性（见Fig. 10），难以保证全局运动一致性。

3. **自回归退化**：自回归RNN方法（如**ACRNN**，Zhou et al., ICLR 2018）在长序列生成中会逐渐累积误差，导致足部悬浮、关节穿透等退化现象，且运动多样性随时间衰减。

4. **VAE方法的局限**：基于VAE的运动生成方法（如**Motion VAE**，Ling et al., TOG 2020）同样受限于固定长度的潜在空间编码，难以直接扩展至无限长序列生成。

### 核心动机

本文的核心动机源于对扩散过程本质的重新审视：**扩散模型的去噪过程本身是渐进的**——从纯噪声出发，经过多个时间步逐步恢复出干净信号。这一渐进特性与长时运动序列的时序展开具有天然的对应关系。如果能够将**扩散过程的时间轴与运动序列的时间轴进行纠缠（entangle）**，使得运动序列中的每一帧对应不同的噪声水平，那么就可以利用扩散模型的逐步去噪机制，持续产生新的干净运动帧，从而实现无限长、高质量的运动序列合成。

基于这一洞察，本文提出了**TEDi（Temporally-Entangled Diffusion）**框架，通过引入**时序变化的噪声调度**和**运动缓冲区递归生成机制**，从根本上突破了现有方法在生成长度、运动质量和多样性方面的瓶颈。

## 核心创新

TEDi 的核心创新在于将扩散过程的时间轴与运动序列的时间轴进行**时序纠缠（Temporally-Entangled Diffusion）**，从而突破了现有扩散运动生成模型只能生成固定长度短序列的根本限制。这一设计通过三个关键“changed slots”区别于 baseline 方法：

### 1. 帧级变化噪声注入模式

标准 DDPM 框架对所有帧施加**同一噪声水平**的高斯噪声，生成过程是一次性的、全局的。TEDi 将其扩展为**随时间变化的噪声调度**（temporally-varying noise schedule），使每一帧拥有独立的噪声水平（见 Fig. 2）。

训练时采用**混合调度策略**：以概率 $p = 2/3$ 使用随机调度 $[\beta_{t_1}, \beta_{t_2}, ..., \beta_{t_K}], t_i \sim \mathcal{U}(0, T)$，使模型学会处理任意帧级噪声组合；其余时间使用单调调度 $[\beta_{t_1}, \beta_{t_2}, \ldots, \beta_{t_K}], t_i = i$，为推理时的递进噪声缓冲区做准备。消融实验（Fig. 9）证实，**若去掉随机调度仅使用单调调度，模型生成的运动会崩溃**，平均运动方差大幅下降——随机调度是维持运动多样性和长期稳定性的必要条件。

### 2. 自回归运动缓冲区生成范式

baseline 方法（如 **MDM** Tevet et al., 2022）一次性生成全部运动帧，拼接长序列时产生**缝合伪影**（stitching artifacts）；**ACRNN**（Zhou et al., ICLR 2018）等自回归 RNN 方法则在长时生成中快速遗忘并退化。

TEDi 提出**运动缓冲区递归生成**机制（Fig. 3）：维护一个噪声水平单调递增的运动缓冲区，每步对整个缓冲区去噪后，**弹出首个干净帧**作为输出，同时在缓冲区末尾**推入新的纯噪声帧**，循环往复即可生成任意长度的运动序列。缓冲区内递增的噪声帧承载了未来运动的隐含信息，使模型能够“预见”并规划后续动作，从根本上避免了拼接伪影和 RNN 退化问题。

### 3. 物理感知的联合训练损失

标准扩散模型仅优化去噪损失 $\mathcal{L}_{\text{diff}}$（预测干净信号与真实信号的 L2 距离）。TEDi 额外引入两个物理合理性约束：

- **位置损失** $\mathcal{L}_{\text{pos}}$：通过前向运动学（FK）将预测的旋转和根位移映射为关节位置，惩罚预测位置与真实位置的 L2 距离。这有效缓解了旋转误差沿运动链的累积放大效应。
- **足部接触损失** $\mathcal{L}_{\text{contact}}$：以足部接触标签为权重，惩罚应有接触时足部关节的速度（即滑动），通过 sigmoid 函数平滑权重边界。

总损失为三者的加权组合 $\mathcal{L} = \lambda_{\text{diff}} \mathcal{L}_{\text{diff}} + \lambda_{\text{pos}} \mathcal{L}_{\text{pos}} + \lambda_{\text{contact}} \mathcal{L}_{\text{contact}}$，在保持生成质量的同时显著提升了运动的物理合理性（详见 4.5.2 节感知研究，TEDi 质量得分 33 vs. MDM 17）。

---

**因果枢纽总结**：时序纠缠的本质是通过让扩散模型适应帧级变化噪声水平，将扩散的逐步去噪机制转化为持续产生新干净帧的引擎。三个 changed slots 中，帧级噪声注入是**使能条件**，缓冲区递归生成是**推理机制**，物理感知损失是**质量保障**——三者协同实现了无限长、高质量、物理合理的运动合成。

## 整体框架

TEDi（Temporally-Entangled Diffusion）的核心思想是将扩散过程的去噪时间轴与运动序列的时间轴进行纠缠，从而突破传统扩散模型只能生成固定长度短序列的限制。其整体框架由训练和推理两条协同设计的流程构成，共享同一个去噪网络，但噪声调度策略和生成范式截然不同。

### 运动表示

框架的输入输出均采用统一的运动表示。一个长度为 $K$ 的运动序列被编码为张量：

$$\mathbf{M} \equiv [\mathbf{O}_{xz}, \mathbf{O}_y, \mathbf{R}, \mathbf{L}] \in \mathbb{R}^{K \times (JQ + C + 3)}$$

其中 $\mathbf{O}_{xz} \in \mathbb{R}^{K \times 2}$ 为根关节在 xz 平面的位移，$\mathbf{O}_y \in \mathbb{R}^{K}$ 为根关节高度，$\mathbf{R} \in \mathbb{R}^{K \times JQ}$ 为各关节的 6D 旋转特征（$J$ 个关节，$Q=6$），$\mathbf{L} \in \mathbb{R}^{K \times C}$ 为足部接触标签（$C$ 个接触点）。这种表示将运动学信息与接触语义统一编码，为后续的扩散建模和物理约束提供了完整的信息基础。

### 训练流程：时序变化噪声注入

训练流程如图 2 所示。与标准 DDPM 对所有帧施加同一噪声水平不同，TEDi 在每次迭代中从数据集采样 $K$ 帧干净运动序列 $[f_1, f_2, \ldots, f_K]$，然后根据噪声调度 $[\beta_{t_1}, \beta_{t_2}, \ldots, \beta_{t_K}]$ 对每一帧施加不同强度的噪声。

训练时的噪声调度采用**混合策略**：
- **随机调度**（以概率 $p=2/3$）：$t_i \sim \mathcal{U}(0, T)$，即每帧的噪声水平独立地从均匀分布中采样
- **单调调度**（以概率 $1/3$）：$t_i = i$，即噪声水平沿时间轴单调递增

这种混合调度的设计是框架的关键因果调控旋钮：随机调度迫使模型学习处理任意帧级噪声组合，赋予其泛化到推理时单调递增噪声缓冲区的能力；而单调调度则让模型接触推理时的真实噪声分布模式，起到桥接训练与推理的作用。消融实验证实，若去掉随机调度（仅使用单调调度），模型生成的运动会崩溃，运动方差大幅下降（Fig. 9）。

去噪网络接收噪声运动序列，预测对应的干净运动 $\mu_\theta(m_t, t)$，训练目标为最小化预测干净信号与真实信号的 L2 损失：

$$\operatorname*{min}_{\theta} L(\theta) := \operatorname*{min}_{\theta} \mathbb{E}_{m_0 \sim q(m_0), w \sim \mathcal{N}(0, I), t} \| m_0 - \mu_{\theta}(m_t, t) \|_2^2$$

### 损失函数：扩散损失与物理约束的联合优化

TEDi 的总训练损失由三项加权组成：

$$\mathcal{L} = \lambda_{\mathrm{diff}} \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\mathrm{contact}} \mathcal{L}_{\mathrm{contact}}$$

**位置损失** $\mathcal{L}_{\mathrm{pos}}$ 通过前向运动学（FK）将预测的旋转和根位移转换为关节位置，与真实关节位置计算 L2 距离：

$$\mathcal{L}_{\mathrm{pos}} = \frac{1}{K J} \sum_{t=1}^{K} \left\| \mathrm{FK}_{\mathrm{S}}(\hat{\mathbf{R}}_t, \hat{\mathbf{O}}_t) - \mathrm{FK}_{\mathrm{S}}(\mathbf{R}_t, \mathbf{O}_t) \right\|_2^2$$

该损失直接惩罚关节位置误差，能有效缓解旋转误差沿运动链累积导致的末端效应器漂移问题。

**足部接触损失** $\mathcal{L}_{\mathrm{contact}}$ 利用接触标签作为权重，惩罚足部关节在应有接触时的滑动：

$$\mathcal{L}_{\mathrm{contact}} = \frac{1}{K C} \sum_{j} \sum_{t=1}^{K-1} \left\| \mathrm{FK}_{\mathrm{S}}(\mathbf{R}_{t+1}, \mathbf{O}_{t+1})_{j} - \mathrm{FK}_{\mathrm{S}}(\mathbf{R}_{t}, \mathbf{O}_{t})_{j} \right\|_2^2 \cdot s(\mathbf{L}_{tj})$$

其中 $s(\cdot)$ 为 sigmoid 函数，将接触标签平滑化为连续权重，使得损失在接触概率高时对足部滑动施加更强的惩罚。

### 推理流程：运动缓冲区递归生成

推理流程是 TEDi 实现无限长运动生成的核心机制，如图 3 所示。其关键数据结构是一个**运动缓冲区**（motion buffer），其中维护着 $K$ 帧运动，噪声水平沿时间轴单调递增（采用单调调度 $t_i = i$）。

生成过程分为三步循环：
1. **去噪**：将整个运动缓冲区输入去噪网络，得到去噪后的运动序列
2. **弹出**：将缓冲区首帧（噪声水平最低、最接近干净的帧）作为生成结果输出
3. **推入**：在缓冲区末尾推入一帧纯噪声运动，保持缓冲区长度不变

这一机制的精妙之处在于：缓冲区中噪声递增的帧承载了未来运动的隐含信息——噪声水平越高的帧编码越远未来的运动先验，而扩散模型的逐步去噪能力则将这些隐含信息逐帧“显式化”为干净运动。通过循环执行这三步，TEDi 能够自回归地生成任意长度的运动序列，且无需拼接操作，从根本上避免了传统方法的缝合伪影。

初始运动缓冲区可以使用一段干净的运动引导序列（primer）来填充：将引导帧按噪声水平递增的方式注入噪声后放入缓冲区，为后续生成提供运动上下文。

### 去噪网络：1D U-Net

框架的去噪网络采用 1D U-Net 架构，沿时间维度进行卷积操作，内部包含注意力块和跳跃连接。网络接收噪声运动缓冲区并预测干净运动序列。具体的层数、通道数和注意力头数等架构细节在原文中未完全展开，其对长时生成质量和效率的影响仍是一个开放问题。

### 模块间数据流总结

整个框架的数据流可概括为：
1. 原始运动数据 → **运动表示编码** → 统一张量格式 $\mathbf{M}$
2. 训练时：$\mathbf{M}$ → **前向噪声注入**（混合调度）→ 噪声运动 → **1D U-Net** → 预测干净运动 → **损失函数组合**（$\mathcal{L}_{\mathrm{diff}} + \mathcal{L}_{\mathrm{pos}} + \mathcal{L}_{\mathrm{contact}}$）→ 反向传播
3. 推理时：初始引导序列 → **运动缓冲区初始化** → 循环执行（**1D U-Net 去噪** → 弹出干净帧 → 推入噪声帧）→ 无限长运动序列输出

### 补充图表

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/001_Figure_1.jpg]]
*Figure 1: Inspired by the gradual nature of the diffusion process along a diffusion time-axis (left), our approach (right) entangles the temporal-axis of motion with the time-axis of the diffusion process (right), enabling a new mechanism for synthesizing arbitrarily long motion sequences*

## 核心模块与公式推导

TEDi 的核心贡献在于将标准 DDPM 中全局统一的时间步噪声，替换为**沿运动时间轴逐帧变化的噪声调度**，从而将扩散过程的“去噪时间轴”与运动序列的“时序轴”纠缠在一起。这一设计使得模型能够学习从任意噪声水平组合中恢复干净运动，进而支撑自回归式的无限长序列生成。

### 运动表示

运动序列被编码为一个长度为 $K$ 的张量，每帧包含以下分量：

$$
\mathbf{M} \equiv [\mathbf{O}_{xz}, \mathbf{O}_y, \mathbf{R}, \mathbf{L}] \in \mathbb{R}^{K \times (JQ + C + 3)}
$$

其中 $\mathbf{O}_{xz} \in \mathbb{R}^{K \times 2}$ 为根关节在 xz 平面的位移，$\mathbf{O}_y \in \mathbb{R}^K$ 为根关节高度，$\mathbf{R} \in \mathbb{R}^{K \times JQ}$ 为所有关节的 6D 旋转特征（$J$ 个关节，$Q=6$），$\mathbf{L} \in \mathbb{R}^{K \times C}$ 为足部接触标签（$C$ 个接触点）。这种表示将运动学信息与接触语义统一为可微分的张量形式，为后续损失函数的设计提供了基础。

### 扩散框架的时序纠缠扩展

标准 DDPM 的训练目标是最小化预测干净信号与真实信号的 L2 损失：

$$
\operatorname*{min}_{\theta} L(\theta) := \operatorname*{min}_{\theta} \mathbb{E}_{m_0 \sim q(m_0), w \sim \mathcal{N}(0, I), t} \| m_0 - \mu_{\theta}(m_t, t) \|_2^2
$$

其中 $m_t$ 是对干净运动 $m_0$ 施加 $t$ 步高斯噪声后的结果，网络 $\mu_\theta$ 直接预测干净信号而非噪声。TEDi 的关键修改在于：**不再对所有帧使用相同的噪声步 $t$，而是为每一帧独立指定噪声水平**。

具体而言，训练时采用两种噪声调度的混合策略：

**随机调度**：对长度为 $K$ 的运动序列，每帧的噪声步从均匀分布中独立采样：
$$
[\beta_{t_1}, \beta_{t_2}, ..., \beta_{t_K}], \quad t_i \sim \mathcal{U}(0, T)
$$
该调度使模型暴露于任意帧级噪声组合，学习通用的逐帧去噪能力。

**单调调度**：噪声步沿运动时间轴严格递增：
$$
[\beta_{t_1}, \beta_{t_2}, \ldots, \beta_{t_K}], \quad t_i = i
$$
该调度模拟了推理时运动缓冲区的噪声分布模式——靠近“未来”的帧噪声更大，靠近“现在”的帧噪声更小。

训练时以概率 $p = 2/3$ 使用随机调度，$p = 1/3$ 使用单调调度。消融实验（Fig. 9）表明，**若去掉随机调度、仅使用单调调度，模型生成的运动会崩溃**，平均运动方差大幅下降，多样性丧失。随机调度是防止模型过拟合到单一噪声模式、维持生成多样性的关键机制。

### 损失函数设计

TEDi 的损失函数由三项加权组合而成，分别约束信号重建精度、运动学合理性和物理接触一致性：

**扩散损失** $\mathcal{L}_{\text{diff}}$：即上述预测干净信号的 L2 损失，作用于运动表示的所有分量。

**位置损失** $\mathcal{L}_{\text{pos}}$：通过前向运动学（FK）将预测的旋转和根位移映射为关节的三维位置，并与真实位置比较：
$$
\mathcal{L}_{\text{pos}} = \frac{1}{K J} \sum_{t=1}^{K} \left\| \mathrm{FK}_{\mathrm{S}}(\hat{\mathbf{R}}_t, \hat{\mathbf{O}}_t) - \mathrm{FK}_{\mathrm{S}}(\mathbf{R}_t, \mathbf{O}_t) \right\|_2^2
$$
该损失直接惩罚关节位置误差，避免旋转误差沿运动链累积导致的末端效应器漂移。

**足部接触损失** $\mathcal{L}_{\text{contact}}$：利用接触标签 $\mathbf{L}_{tj}$ 作为权重，惩罚足部关节在应有接触时的滑动：
$$
\mathcal{L}_{\text{contact}} = \frac{1}{K C} \sum_{j} \sum_{t=1}^{K-1} \left\| \mathrm{FK}_{\mathrm{S}}(\mathbf{R}_{t+1}, \mathbf{O}_{t+1})_{j} - \mathrm{FK}_{\mathrm{S}}(\mathbf{R}_{t}, \mathbf{O}_{t})_{j} \right\|_2^2 \cdot s(\mathbf{L}_{tj})
$$
其中 $s(\cdot)$ 为 sigmoid 函数，将二值接触标签平滑为连续权重，使梯度能够有效传导。该损失有效抑制了“滑步”伪影。

**总损失**为三项的加权和：
$$
\mathcal{L} = \lambda_{\text{diff}} \mathcal{L}_{\text{diff}} + \lambda_{\text{pos}} \mathcal{L}_{\text{pos}} + \lambda_{\text{contact}} \mathcal{L}_{\text{contact}}
$$
权重 $\lambda_{\text{diff}}$、$\lambda_{\text{pos}}$、$\lambda_{\text{contact}}$ 的具体取值在原文中未明确给出，属于需要手动验证的超参数。

### 推理：运动缓冲区递归生成

推理过程维护一个长度为 $K$ 的运动缓冲区，其噪声水平沿时间轴单调递增（采用单调调度）。生成循环包含三步（Fig. 3）：

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/003_Figure_3.jpg]]
*Figure 3: TEDi Recursive Generation. TEDi is capable of generating an arbitrarily long motion sequence. First, we initialize our motion buffer with a a set of increasingly-noised motion frames. Then (step 1) we denoise the entire motion buffer, (step 2) pop the new, clean frame in the beginning of the motion buffer, and then (step 3) push noise into the end of the motion buffer. This process is repeated recursively*

1. **去噪**：将整个缓冲区送入训练好的 1D U-Net，预测干净运动序列。
2. **弹出**：取出去噪后缓冲区的第一帧作为生成的干净帧输出。
3. **推入**：在缓冲区末尾追加一帧纯噪声（$\beta_T$ 对应的高斯噪声），保持缓冲区长度不变。

重复此过程即可自回归地生成任意长度的运动序列。缓冲区中递增的噪声帧实质上编码了“未来运动的隐含信息”——高噪声帧在去噪过程中受到低噪声帧的上下文约束，使模型能够持续产生与已生成内容连贯的新帧。这一机制从根本上避免了拼接短序列带来的缝合伪影，以及 RNN 方法在长时生成中的遗忘与退化问题。

### 去噪网络架构

去噪网络采用 **1D U-Net** 结构，沿运动时间轴执行一维卷积、自注意力和跳跃连接。原文未披露具体的层数、通道数和注意力头数配置，这些细节对生成质量和效率的影响属于开放问题。网络接收噪声运动缓冲区和对应的噪声步信息，输出预测的干净运动序列。

### 补充图表

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/002_Figure_2.jpg]]
*Figure 2: TEDi Training. We train our diffusion-based model to remove temporally-varying noise that is applied to clean sequences during training. In each iteration we fetch a motion sequence of ?? frames*

## 实验与分析

### 感知研究：主客观质量对比

TEDi 的核心实验评估采用感知研究（perceptual study）范式，通过 Amazon Mechanical Turk 招募 35 名参与者，对四种方法生成的运动视频进行偏好投票。比较对象包括基于扩散的 **MDM**（Tevet et al., 2022）、自回归循环网络 **ACRNN**（Zhou et al., ICLR 2018）以及基于 VAE 的 **Motion VAE**（Ling et al., TOG 2020）。

Table 1 汇总了用户偏好计数结果：在运动多样性维度上，TEDi 获得 34 票，远超 MDM（12 票）、ACRNN（8 票）和 Motion VAE（1 票）；在运动质量维度上，TEDi 获得 33 票，MDM 获得 17 票，ACRNN 仅获 5 票。两项指标均表明 TEDi 在长时运动合成任务上具有显著优势。

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/010_Table_1.jpg]]
*Table 1: Perceptual study results for our method and baselines*

TEDi 的优势根源于其时序纠缠扩散机制：运动缓冲区中递增噪声水平的帧承载了未来运动的隐含信息，使得模型在每步去噪时能够“预见”即将到来的运动状态，从而生成连贯、自然的过渡。相比之下，MDM 的 in-painting 策略在拼接边界产生可见的不连续性（Fig. 10 上排），ACRNN 在长时生成中出现足部悬浮和穿透等退化伪影（Fig. 10 下排），Motion VAE 则倾向于生成重复、缺乏多样性的运动模式。

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/012_Figure_10.jpg]]
*Figure 10: Long-term motion synthesis baseline comparisons. Top: We show two pairs of consecutive frames generated through an in-painting implementation with MDM [Tevet et al. 2022]. Classic in-painting shows visible discontinuity that happens along the border of in-painting. Bottom: ACRNN [Zhou et al. 2018] when trained on a large dataset is not stable, as seen by the foot levitation and penetration artifacts*

### 长时生成与定性分析

TEDi 能够生成任意长度的运动序列。Fig. 4 展示了一段 33 秒的运动序列，每 100 帧（约 3 秒）可视化一个姿态，整个序列保持合理的运动连贯性。Fig. 5 进一步展示了 TEDi 生成多样化运动风格的能力，包括拳击、曳步舞和手势动作。

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/004_Figure_4.jpg]]
*Figure 4: Long-term Generation. Our method synthesizes arbitrarily long motion sequences. In the above figure, we summarize 33 seconds of motion by visualizing the pose every 100-frames (≈3 seconds). Our model is able to generate plausible motions throughout the entire motion sequence*

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/006_Figure_5.jpg]]
*Figure 5: Diverse Motions. Our method is capable of producing a wide variety of long motion sequences. From left to right: Boxing, shuffling, and hand-gestures*

得益于扩散模型的随机性，TEDi 还能从同一初始运动片段（primer）生成不同的运动变体。Fig. 6 展示了从单个 primer 出发生成的四种运动，随着时间推移，各变体逐渐分化，体现了模型在保持条件一致性的同时探索运动多样性的能力。

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/007_Figure_6.jpg]]
*Figure 6: Motion Variations. Due to the stochastic nature of diffusion models, our method is able to generate variations using the same motion primer as input. We show four motions generated from a single primer, from left to right, we can see that the motions begins to differ significantly as time goes on*

### 引导生成与轨迹控制

TEDi 支持通过运动引导（motion guides）实现交互式生成。给定一组目标运动片段 $Q$（Fig. 7 中以黄色标记），模型通过在运动缓冲区中替换对应帧为引导帧的加噪版本，在引导帧之间自动合成合理的过渡运动（蓝色标记）。生成的过渡运动能够“准备和规划”即将到来的引导动作，实现平滑衔接。

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/005_Figure_7.jpg]]
*Figure 7: Guided Generation. Given a set of motion guides Q?? (shown in yellow), we are able to perform them in sequence at desired points while generating plausible motion in the interactively generated frames (blue). From top-left to bottom-right, our method generates an entire motion sequence that contains the desired motion guides and the interactively synthesized motion. The interactively generated motions will “prepare and plan” for the upcoming motion guides. See the supplementary video*

类似地，轨迹控制通过修改运动缓冲区中的根位移和根高度信息实现。Fig. 8 展示了给定期望轨迹 $P \in \mathbb{R}^{3 \times N}$ 后，TEDi 生成的自然运动能够准确遵循指定路径，同时保持动作的物理合理性。

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/008_Figure_8.jpg]]
*Figure 8: Trajectory Control. Similar to guided generation, given the desired trajectory information P (shown in yellow), our method can generate natural motions that adhere to the given trajectory*

### 消融实验：随机噪声调度的关键作用

随机噪声调度是 TEDi 避免运动崩溃的核心设计。消融实验对比了训练时使用混合调度（随机调度与单调调度混合，概率 $p=2/3$）与仅使用单调调度的效果。Fig. 9 展示了 500 帧范围内的平均运动方差：去除随机调度后，运动方差大幅下降，模型生成的运动会迅速崩溃为静态或重复模式。

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/009_Figure_9.jpg]]
*Figure 9: Ablations: Here we show the average motion variance over 500 frames for our method with and without the random schedule. It can be seen that our random schedule helps avoid motion-collapse*

这一现象的因果机制在于：随机调度迫使模型学习在任意帧级噪声水平下进行去噪，从而在推理时能够处理缓冲区中从干净到高噪声的完整噪声谱。若训练时仅使用单调调度，模型从未见过非单调的噪声分布，推理时面对缓冲区的递增噪声模式时泛化能力不足，导致去噪质量退化。

### 训练配置与计算开销

模型在 CMU 运动捕捉数据集上训练，原始 120fps 数据降采样至 30fps。训练使用 500 帧窗口、步长 100 的滑动采样策略，总迭代次数 500k，在 NVIDIA A40 GPU 上耗时约三天。

### 已知局限

TEDi 的主要局限在于推理延迟：从纯噪声生成干净帧需要经过完整的扩散去噪链，单帧生成延迟较高，限制了实时交互场景的应用。论文指出利用 DDIM 等加速采样方法跳过部分去噪步骤是降低延迟的潜在方向，但尚未在本文中实现验证。此外，损失权重 $\lambda_{\text{diff}}$、$\lambda_{\text{pos}}$、$\lambda_{\text{contact}}$ 的选择策略以及 1D U-Net 的具体架构配置对性能的影响仍需进一步探索。

### 公平性说明

感知研究中各基线模型的训练数据集、参数规模和计算资源可能不完全相同，这可能影响结果的绝对公平性。但 TEDi 在多样性和质量上的优势幅度（票数差距超过两倍）表明，时序纠缠机制带来的增益不太可能完全归因于训练配置差异。

### 补充图表

![[assets/figures/papers/paper_list_l26_TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis/figures/011_Figure_12.jpg]]
*Figure 12: Example motions from perceptual study. From top to bottom: Ours, ACRNN, MDM, and Motion VAE*

## 方法谱系与知识库定位

### 1. 核心机制与基线差异

TEDi 的核心创新在于将扩散过程的时间轴与运动序列的时序轴进行**纠缠**，从而突破了现有扩散运动生成模型只能生成固定长度短序列的根本限制。这一设计改变了扩散模型中噪声注入和去噪的基本范式，具体体现在以下三个关键槽位：

| 方法维度 | 基线范式 | TEDi 方案 |
|---------|---------|----------|
| **噪声注入模式** | 固定的时间不变高斯噪声（所有帧共享同一噪声水平） | 随时间变化的噪声调度：训练时混合随机调度与单调调度（概率 p=2/3），推理时使用单调递增噪声缓冲 |
| **生成范式** | 一次性生成固定长度的全部运动帧 | 自回归运动缓冲区生成：维护递增噪声的缓冲区，每步去噪整个缓冲区后弹出首个干净帧并推入新噪声帧 |
| **训练损失** | 仅最小化去噪损失（预测噪声或干净信号） | 联合优化去噪损失、基于前向运动学的位置损失和足部接触损失，加权求和 |

这些槽位的改变直接回应了现有方法的失败模式：拼接短序列产生的缝合伪影，以及循环神经网络方法在长时生成中的遗忘与退化。**MDM**（Tevet et al., 2022）通过 in-painting 策略尝试生成长序列，但如图 10 所示，在拼接边界处产生明显的不连续性；**ACRNN**（Zhou et al., ICLR 2018）作为自回归 RNN 基线，在大型数据集上训练后表现出脚部悬浮和穿透伪影，且迅速退化崩溃。TEDi 通过缓冲区递归机制绕过了这些问题——噪声帧承载未来运动的隐含信息，使模型在去噪时能够"预见"后续动作，从而实现连贯的长时生成。

### 2. 训练范式的因果逻辑

TEDi 的训练策略服务于一个核心目标：**使扩散模型适应帧级变化的噪声水平**。标准 DDPM 的训练目标是最小化预测干净信号与真实信号的 L2 损失：

$$\operatorname*{min}_{\theta} L(\theta) := \operatorname*{min}_{\theta} E_{m_0 \sim q(m_0), w \sim N(0, I), t} \| m_0 - \mu_{\theta}(m_t, t) \|_2^2$$

TEDi 的关键扩展在于噪声调度从单一标量 $t$ 变为帧级向量 $[\beta_{t_1}, \beta_{t_2}, ..., \beta_{t_K}]$。训练时以 $p=2/3$ 的概率使用随机调度（$t_i \sim \mathcal{U}(0, T)$），使模型学习从任意噪声水平组合中恢复干净运动；以 $p=1/3$ 的概率使用单调调度（$t_i = i$），为推理时的缓冲区机制做准备。消融实验（Fig. 9）证实：若去除随机调度，仅使用单调调度，模型生成的运动会崩溃，平均运动方差在 500 帧内显著下降——随机调度是维持运动多样性和长期稳定性的**必要条件**。

### 3. 损失函数设计：物理合理性的注入

TEDi 在标准扩散损失之外引入了两个辅助损失，以缓解旋转误差沿运动链累积的问题：

- **位置损失** $\mathcal{L}_{\mathrm{pos}}$：通过前向运动学 $\mathrm{FK}_{\mathrm{S}}$ 计算关节位置，惩罚预测位置与真实位置的 L2 距离。这直接补偿了旋转表示（6D 特征）的误差放大效应。

- **足部接触损失** $\mathcal{L}_{\mathrm{contact}}$：利用接触标签 $\mathbf{L}$ 作为权重，惩罚足部关节在应有接触时的滑动速度。通过 sigmoid 函数 $s(\cdot)$ 平滑权重，避免硬阈值带来的梯度问题。

总损失为三者的加权组合 $\mathcal{L} = \lambda_{\mathrm{diff}} \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\mathrm{contact}} \mathcal{L}_{\mathrm{contact}}$。这些损失权重的选择（$\lambda_{\mathrm{diff}}, \lambda_{\mathrm{pos}}, \lambda_{\mathrm{contact}}$）是一个开放问题——论文未给出具体数值或调参策略，需要在实践中根据数据集特性进行手动验证。

### 4. 适用边界与局限

**适用场景**：TEDi 在需要无限长、高质量运动序列的场景中表现出色，包括无条件长时生成、运动引导生成（在指定时间点插入目标动作，模型自动生成过渡帧）和轨迹控制生成（给定根位移轨迹，生成符合轨迹的自然运动）。其扩散模型的随机性天然支持从同一初始序列产生多样化变体（Fig. 6）。

**核心局限**：
1. **单帧生成延迟高**：从纯噪声生成一个干净帧需要经过完整的扩散去噪链，这限制了实时交互应用的响应速度。这是扩散模型固有的推理效率问题，TEDi 的缓冲区机制并未加速单帧生成，只是使连续生成成为可能。
2. **训练成本**：在 CMU 运动数据集（降采样至 30fps，500 帧窗口，步长 100）上训练 500k 次迭代需要约 3 天（NVIDIA A40），对于更大规模数据集或更高帧率场景，训练开销可能成为瓶颈。

### 5. 开放问题与未来方向

1. **采样加速**：如何利用 DDIM 或类似加速采样方法减少去噪步骤，实现更低延迟的实时生成？这是将 TEDi 推向交互应用的关键。

2. **文本条件扩展**：当前 TEDi 仅支持无条件生成和运动引导，如何将框架扩展到文本条件下的长时运动生成，并实现高层语义控制（如"行走然后跳跃"）与低层运动引导的有效耦合？

3. **网络架构优化**：1D U-Net 的具体架构配置（层数、通道数、注意力头数）对长时运动生成的质量和效率有何影响？论文未详细披露这些超参数，需要进一步探索。

4. **损失权重自动调优**：$\lambda_{\mathrm{diff}}, \lambda_{\mathrm{pos}}, \lambda_{\mathrm{contact}}$ 的最优选择可能依赖于运动类型和数据集特性，开发自适应权重策略可提升方法的鲁棒性。

5. **感知评估的局限性**：当前主要评估依赖 Amazon Mechanical Turk 上的 35 人感知研究（Table 1），TEDi 在多样性（34 vs MDM 12）和质量（33 vs MDM 17）上均显著领先。但各基线模型的训练数据集、参数规模和计算资源可能不完全相同，这影响了结果的绝对公平性——需要更标准化的基准测试来验证结论的稳健性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/TEDi_Temporally_Entangled_Diffusion_for_Long_Term_Motion_Synthesis.pdf]]
