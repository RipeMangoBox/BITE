---
title: Unified Number-Free Text-to-Motion Generation Via Flow Matching
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unified_Number_Free_Text_to_Motion_Generation_Via_Flow_Matching.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Huang_Unified_Number-Free_Text-to-Motion_Generation_Via_Flow_Matching_CVPR_2026_paper.html
project_link: https://githubhgh.github.io/umf/
code_link: null
aliases:
- UMFU
- UNFTMGFM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用多令牌潜空间统一异构数据，金字塔流匹配（P-Flow）根据噪声层级分配分辨率以降低计算开销，半噪声流匹配（S-Flow）联合优化反应变换与上下文重构以缓解误差累积。
primary_logic: 将无人数约束的运动生成分解为单次先验生成与多次反应生成两阶段，利用异构数据集在统一潜空间中训练，并通过层级式流匹配和联合概率路径设计分别提升效率与鲁棒性。
claims:
- UMF在InterHuman数据集上FID达到4.772，相比FreeMotion FID降低29%、Top3 R-Precision提高28%，证明了无人数约束生成的有效性。
- 移除S-Flow的Context Adapter或重构损失导致FID显著上升（7.038 / 5.765），验证了联合概率路径对缓解误差累积的关键作用。
- P-Flow通过层级分辨率设计在保持FID 4.772的同时，将FLOPs降低至74.7G（UMF-Fast），相比全分辨率方案显著提升效率。
- InterHuman 上 Top3 R-Precision↑ = 0.694
---

# Unified Number-Free Text-to-Motion Generation Via Flow Matching

> [!tip] 核心洞察
> 将无人数约束的运动生成分解为单次先验生成与多次反应生成两阶段，利用异构数据集在统一潜空间中训练，并通过层级式流匹配和联合概率路径设计分别提升效率与鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无人数限制的统一文本-动作流匹配生成 |
| 英文题名 | Unified Number-Free Text-to-Motion Generation Via Flow Matching |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Huang_Unified_Number-Free_Text-to-Motion_Generation_Via_Flow_Matching_CVPR_2026_paper.html) · [Project](https://githubhgh.github.io/umf/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Unified Motion Flow (UMF) |
| Dataset | InterHuman, InterHuman-AS |

> [!tip] 效果简介
> - InterHuman 上，Top3 R-Precision↑ 0.694 vs FreeMotion (≈0.542) (+28%)；FID↓ 4.772 vs FreeMotion (≈6.719) (-29%)；FID↓ 4.772 vs InterMask (≈5.131) (-7%)。
> - InterHuman-AS 上，Top3 R-Precision↑ 0.530±0.006 vs ReGenNet (+30%)；FID↓ 2.577±0.024 vs ReGenNet (显著提升)。

## 概要

现有文本驱动的人体动作生成方法面临两个核心瓶颈：**固定人数约束**与**自回归误差累积**。标准方法（如 **MDM** (Tevet et al., arXiv 2022)、**TEMOS** (Petrovich et al., arXiv 2022)）只能生成预设人数的动作序列，无法泛化到可变人数的开放场景；而自回归方法（如 **FreeMotion** (Fan et al., ECCV 2024)）虽将生成解耦为先验与反应两阶段，却因确定性条件网络引入误差累积，导致生成质量随人数增加而显著下降。

针对上述问题，本文提出 **Unified Motion Flow (UMF)**——一个无人数限制的统一文本-动作生成框架。UMF 的核心思路是：将无人数约束的运动生成分解为**单次先验生成**与**多次反应生成**两个阶段，并利用异构数据集在统一潜空间中联合训练。具体而言，UMF 包含三项关键设计：

1. **统一运动 VAE**：通过多令牌潜空间和 Latent Adapter，将来自 HumanML3D 和 InterHuman 等异构数据集的运动数据编码到统一表示，弥合分布差异。
2. **金字塔流匹配（P-Flow）**：根据噪声层级动态调整潜空间分辨率，在保持高保真生成的同时大幅降低多令牌表示的计算开销。
3. **半噪声流匹配（S-Flow）**：设计联合概率路径，同时学习反应变换与上下文重建，从根本上缓解自回归生成中的误差累积问题。

在 InterHuman 双人交互基准上，UMF 取得了 **FID 4.772** 的领先性能，相比 FreeMotion 的 FID 降低 29%、Top3 R-Precision 提高 28%；在 InterHuman-AS 动作-反应合成任务上，UMF 同样显著超越 **ReGenNet** (Xu et al., CVPR 2024) 等专用方法。消融实验进一步验证：移除 S-Flow 的 Context Adapter 或重建损失会导致 FID 分别升至 7.038 和 5.765，证实了联合概率路径对抑制误差累积的关键作用；P-Flow 的层级分辨率设计则将 FLOPs 降至 74.7G，实现了效率与质量的平衡。

UMF 的局限性在于：当前设计以主角色为中心，仅适用于约 10 人规模的中等群体交互，尚无法直接扩展到密集人群动态（≈100 人）。如何借助大规模视频扩散模型的视觉先验突破这一规模限制，是未来的开放方向。



### 问题背景：从固定人数到无人数约束的文本-动作生成

文本驱动的三维人体运动生成旨在根据自然语言描述合成逼真的动作序列。这一任务在电影制作、游戏开发、虚拟现实和人机交互等领域具有广泛的应用前景。然而，现实场景中的交互往往涉及**可变数量**的参与者——从单人独舞到双人搏击，再到多人群体协作——这对生成模型的泛化能力提出了严峻挑战。

现有方法在处理这一需求时暴露了两个核心瓶颈。其一，**固定人数限制**：标准方法（如 **MDM**（Tevet et al., arXiv 2022）、**TEMOS**（Petrovich et al., arXiv 2022））将生成过程限定在预设的参与者数量上，无法泛化到训练时未见的人数配置。其二，**自回归误差累积**：以 **FreeMotion**（Fan et al., ECCV 2024）为代表的自回归方法将多人运动生成解耦为先验生成与后续反应生成两个阶段，但反应生成通常依赖确定性条件网络（如 ControlNet），导致前序阶段的误差在自回归链中逐级放大，最终严重影响生成质量。

### 现有方法缺口

图 1 系统性地展示了三类方法的设计差异与固有局限：

- **标准方法**（图 1a）：将多人运动视为固定维度的联合分布进行建模，一旦人数发生变化，模型结构即失效，缺乏灵活性。
- **自回归方法**（图 1b）：虽然通过解耦策略实现了人数可变，但反应生成阶段的条件网络仅接收确定性输入，无法建模上下文与反应之间的联合概率分布，导致误差单向传播且难以纠正。
- **数据异构性挑战**：单人运动数据集（如 HumanML3D）与多人交互数据集（如 InterHuman）在运动表示、动作分布和标注粒度上存在显著差异，现有方法难以在统一框架下有效利用这些异构数据。

### 本文动机：流匹配驱动的两阶段统一框架

针对上述缺口，本文提出 **Unified Motion Flow (UMF)**，核心动机在于将无人数约束的运动生成重新表述为流匹配框架下的两阶段过程：

1. **单次先验生成**：利用异构数据集在统一潜空间中训练，生成高质量的运动先验，作为后续反应生成的灵活起点。
2. **多次反应生成**：基于已生成的上下文，通过联合概率路径学习反应变换，从根本上缓解自回归误差累积。

这一设计的因果调节变量在于：**用流匹配的概率路径替代确定性条件映射**，使反应生成阶段能够同时考虑反应变换与上下文重建，从而在概率层面实现误差的自纠正。图 1c 示意了这一两阶段设计如何将异构运动先验作为反应流路径的自适应起点，从而打破确定性条件网络的单向误差传播链条。



## 核心方法与创新机理

UMF的核心创新在于将“无人数约束”的运动生成重新表述为一个**两阶段流匹配问题**，并通过三个相互协同的机制突破现有方法的瓶颈：**统一多令牌潜空间**弥合异构数据分布鸿沟，**金字塔流匹配（P-Flow）** 在保持高保真度的前提下大幅降低多令牌表示的计算开销，**半噪声流匹配（S-Flow）** 通过联合概率路径设计缓解自回归生成中的误差累积。

### 1. 问题分解：从固定人数到无人数约束

现有方法面临两大瓶颈：固定人数架构无法泛化到可变人数场景（如**TEMOS**、**MDM**），而自回归方法（如**FreeMotion**，Fan et al., ECCV 2024）虽解耦了先验生成与反应生成，却受困于确定性条件网络带来的误差累积和低效的逐人串行生成。UMF的核心洞察在于：**将无人数约束的运动生成分解为一次先验生成与多次反应生成**，但关键区别在于，反应生成并非简单地将先验作为确定性条件输入，而是将其作为流匹配概率路径的自适应起点，从而从根本上改变了误差传播的动力学。

### 2. 表示空间：统一多令牌潜空间

**Changed Slot: 表示空间**  
- Baseline：原始运动空间，不同数据集（单人HumanML3D、双人InterHuman）使用异构骨骼表示，难以联合训练。  
- UMF：构建统一运动VAE，将所有运动转换到统一的非规范SMPL骨架（22个关节点），并通过**Latent Adapter**将异构数据编码到共享的**多令牌潜空间** $\mathcal{Z}$ 中。

这一设计的因果机制在于：多令牌分词器（Multi-token Tokenizer）将每条运动表示为 $N$ 个潜令牌，使得单人运动（$N$ 个令牌）和多人运动（$M \times N$ 个令牌）可以在同一Transformer架构中处理。训练损失函数为：

$$\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_{\mathrm{geometric}} + \mathcal{L}_{\mathrm{reconstruction}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}$$

其中几何损失约束局部关节旋转与全局位置，KL散度正则化潜空间。消融实验（Table 3）证明，异构先验（HP）、Latent Adapter（LA）和多令牌分词器（MT）三者缺一不可，共同支撑了跨数据集的知识迁移。

### 3. 先验生成：金字塔流匹配（P-Flow）

**Changed Slot: 先验生成方式**  
- Baseline：标准流匹配在全分辨率潜空间上执行常微分方程求解，计算量随令牌数线性增长。  
- UMF：P-Flow根据噪声层级**动态调整分辨率**，将流匹配轨迹分解为 $K$ 个时间窗口，每个窗口在递进的降采样尺度上操作。

其核心机制是**层级式概率路径**：在第 $k$ 个时间窗口 $[s_k, e_k]$ 内，起始点与结束点分别定义为：

$$\hat{z}_{s_k} = s_k \cdot Up(Down(z_1, 2^k)) + (1 - s_k)\epsilon$$

$$\hat{z}_{e_k} = e_k \cdot Down(z_1, 2^{k-1}) + (1 - e_k)\epsilon$$

即从低分辨率（$2^k$ 降采样）逐步过渡到高分辨率（$2^{k-1}$ 降采样）。窗口切换时，通过重缩放与加噪方案保证概率路径的连续性：

$$\hat{z}_{s_{k-1}} = \frac{s_{k-1}}{e_k} Up(\hat{z}_{e_k}) + \alpha n', \quad n' \sim \mathcal{N}(0, \Sigma')$$

训练目标为回归条件向量场：

$$\mathcal{L}_{\mathrm{P-Flow}} = \mathbb{E}_{k, t, \hat{z}_{e_k}, \hat{z}_{s_k}} \left\| G_\theta^P(\hat{z}_t; t, c) - (\hat{z}_{e_k} - \hat{z}_{s_k}) \right\|^2$$

**证据强度**：Table 4显示，2阶段金字塔结构（UMF）在保持FID 4.772的同时，将FLOPs降至74.7G（UMF-Fast），相比全分辨率方案（UMF w/o Pyramid, FLOPs 149.4G）效率提升约50%，且FID仅轻微上升（4.772→4.984），验证了层级设计在效率-质量权衡中的优越性。

### 4. 反应生成：半噪声流匹配（S-Flow）

**Changed Slot: 反应生成机制**  
- Baseline：确定性条件网络（如ControlNet）将已生成动作作为固定条件输入，误差随生成人数累积。  
- UMF：S-Flow联合优化两条概率路径——**反应变换路径**与**上下文重建路径**，将误差累积问题转化为分布匹配问题。

S-Flow的核心创新在于**Context Adapter**：将已生成动作集合 $\mathcal{Z}_{gen}$ 通过Transformer编码器映射为上下文表示 $C_i = TranEnc(\mathcal{Z}_{gen})$。反应变换损失学习从上下文 $C$ 到目标反应 $W$ 的向量场：

$$\mathcal{L}_{\mathrm{trans}} = \mathbb{E}_{t, w_1, w_0} \| G_\theta^S(w_t^{\mathrm{react}}, t, c) - (W - C) \|_2^2$$

上下文重建损失则迫使模型从噪声中重建上下文，形成正则化约束：

$$\mathcal{L}_{\mathrm{recon}} = \mathbb{E}_{t, w_0, \epsilon} \| G_\theta^S(w_t^{\mathrm{cont}}, t, c) - (C - \epsilon) \|_2^2$$

**证据强度**：Table 5的消融实验提供了因果链条的关键证据——移除Context Adapter使FID从4.772升至7.038（+47%），移除重构损失 $\mathcal{L}_{\mathrm{recon}}$ 使FID升至5.765（+21%），而使用ControlNet替代联合概率路径设计使FID升至6.868（+44%）。这些结果表明，**联合概率路径通过双向约束（反应变换+上下文重建）有效抑制了误差累积**，而确定性条件网络无法提供同等的鲁棒性。

### 5. 推理阶段的非对称预算分配

UMF在推理时采用**非对称步数分配**策略：P-Flow获得充足的推理预算（如50步），以生成高质量的运动先验；S-Flow仅需极少的推理步数（如10步），因为高质量先验为反应生成提供了良好的自适应起点。这种设计进一步放大了两阶段解耦的效率优势。

### 局限性

UMF当前以主角色为中心，适用于中等规模群体交互（约10人），尚无法直接扩展到密集人群动态（约100人）。如何利用大规模视频扩散模型的视觉先验突破这一规模限制，是论文提出的开放问题。



UMF 将“无人数限制”的运动生成分解为两个核心阶段：**单次运动先验生成**与**多次反应生成**，并在统一的潜空间中完成异构数据的联合训练。其整体 pipeline 由三个关键模块串联而成，形成从原始运动编码到最终多人运动序列的完整生成链路。

### 数据预处理与统一表示

为消除不同数据集的骨骼拓扑差异，UMF 首先将所有个体运动转换为统一的非规范 SMPL 骨架表示（22 个关节点）。这一预处理步骤使得来自 HumanML3D 和 InterHuman 等异构数据集的动作可以在同一空间中处理，为后续的统一潜空间编码奠定基础。

### 模块一：统一运动 VAE（Unified Motion VAE）

该模块负责将异构运动数据压缩到统一的多令牌潜空间。其核心设计包含两个关键组件：

- **多令牌分词器（Multi-token Tokenizer）**：将每个运动序列编码为多个潜令牌，而非单一的全局向量，从而保留更丰富的空间-时间细节，并支持可变长度的运动表示。
- **潜适配器（Latent Adapter）**：桥接不同数据集在潜空间中的分布差异，使来自单人数据集（HumanML3D）和双人交互数据集（InterHuman）的潜表示能够对齐到同一分布下。

训练损失函数为：
$$\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_{\mathrm{geometric}} + \mathcal{L}_{\mathrm{reconstruction}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}$$

该损失结合了几何损失、重建损失和 KL 散度，确保潜空间既具有表达能力又保持规整性。消融实验（Table 3）表明，同时使用异构先验、潜适配器和多令牌分词器时，模型在 HumanML3D 和 InterHuman 两个基准上均取得最优性能，验证了统一潜空间设计的必要性。

### 模块二：P-Flow 运动先验生成（Pyramid Motion Flow）

P-Flow 接收文本条件，在统一潜空间中生成第一个角色的运动先验。其核心创新在于**根据噪声层级动态调整分辨率**：在生成早期（高噪声阶段），模型在低分辨率下工作以降低计算开销；随着去噪推进，逐步切换到更高分辨率以恢复细节。

具体而言，P-Flow 将流匹配轨迹 $[0, 1]$ 划分为 $K$ 个时间窗口，每个窗口内插值于不同分辨率之间。第 $k$ 个窗口的起点和终点分别定义为：
$$\hat{z}_{s_k} = s_k \,\text{Up}(\text{Down}(z_1, 2^k)) + (1 - s_k)\epsilon$$
$$\hat{z}_{e_k} = e_k \,\text{Down}(z_1, 2^{k-1}) + (1 - e_k)\epsilon$$

窗口切换时，通过重缩放与加噪方案保证概率路径的连续性：
$$\hat{z}_{s_{k-1}} = \frac{s_{k-1}}{e_k} \text{Up}(\hat{z}_{e_k}) + \alpha n', \quad n' \sim \mathcal{N}(0, \Sigma')$$

这种层级式设计使 P-Flow 在保持生成质量（FID 4.772）的同时，将 FLOPs 降至 74.7G（UMF-Fast 变体），相比全分辨率方案显著提升了效率（Table 4）。

### 模块三：S-Flow 反应运动生成（Semi-Noise Motion Flow）

S-Flow 基于已生成的上下文运动，为后续角色逐一生成反应运动。其核心设计是**联合优化两条概率路径**：

1. **反应变换路径**：学习从上下文 $C$ 到目标反应 $W$ 的向量场，损失函数为：
   $$\mathcal{L}_{\mathrm{trans}} = \mathbb{E}_{t, w_1, w_0} \| G_\theta^S(w_t^{\mathrm{react}}, t, c) - (W - C) \|_2^2$$

2. **上下文重建路径**：学习从噪声重建上下文 $C$ 的向量场，损失函数为：
   $$\mathcal{L}_{\mathrm{recon}} = \mathbb{E}_{t, w_0, \epsilon} \| G_\theta^S(w_t^{\mathrm{cont}}, t, c) - (C - \epsilon) \|_2^2$$

上下文适配器（Context Adapter）将已生成的动作集合 $\mathcal{Z}_{gen}$ 编码为上下文表示 $C_i = \text{TranEnc}(\mathcal{Z}_{gen})$，作为 S-Flow 的条件输入。

消融实验（Table 5）揭示了这一设计的因果机制：移除 Context Adapter 导致 FID 从 4.772 升至 7.038；移除重构损失使 FID 升至 5.765；使用 ControlNet 替代上下文适配器则使 FID 升至 6.868。这表明**联合概率路径通过同时学习“如何反应”和“上下文是什么”**，有效缓解了自回归生成中的误差累积问题。

### 推理流程与资源分配

推理时，UMF 采用非对称的推理预算分配策略（Algorithm 1）：P-Flow 获得充足的推理步数（如 50 步）以生成高质量的运动先验；S-Flow 则仅需极少的推理步数（如 10 步），因为高质量的先验为反应生成提供了可靠的起点。两阶段均使用 Euler ODE 求解器进行采样。

### 输入输出流总结

- **输入**：文本描述 $c$（可描述任意人数的交互场景）
- **阶段一**：P-Flow 在统一潜空间中生成第一个角色的运动先验 $\hat{z}$
- **阶段二**：S-Flow 以已生成的动作集合为上下文，通过 Context Adapter 编码后，逐角色生成反应运动
- **输出**：解码后的多人运动序列，人数由文本描述动态决定，无需预设

### 补充图表

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unified_Number_F/figures/001_Figure_1.jpg]]
*Figure 1: Core contribution of UMF. We show dual-agent cases here for simplicity. (a) Standard methods [51, 57] are restricted to a fixed number of agents. (b) Autoregressive methods [12] decouple generation into a motion prior and subsequent reaction. The reaction is typically guided by the prior using a conditioning network. (c) Our UMF leverages a heterogeneous motion prior as the adaptive start point of the reaction flow path, mitigating error accumulation*



UMF 将无人数约束的运动生成分解为三个核心模块：统一运动 VAE、金字塔流匹配（P-Flow）先验生成、半噪声流匹配（S-Flow）反应生成。其理论基础建立在流匹配（Flow Matching）框架之上。

### 流匹配基础

流匹配的核心思想是通过常微分方程描述从源分布到目标分布的连续变换：

$$\frac{d x_t}{d t} = v_t(x_t)$$

其中 $v_t$ 为速度场，驱动样本 $x_t$ 沿概率路径演化。训练时，通过回归模型预测的速度场与条件向量场之间的差异来优化参数：

$$\mathcal{L}_{\mathrm{FM}}(\theta)=\mathbb{E}_{t,p_{t}(x),q(x_{1})}\left\|v_{t}(x_{t};\theta)-u_{t}(x_{t}|x_{1})\right\|^{2}$$

条件概率路径采用线性插值形式 $x_{t}=t x_{1}+(1-t)x_{0}$，在噪声 $x_0$ 和数据 $x_1$ 之间建立连续映射。该框架的灵活性在于可扩展到高斯分布以外的任意分布间插值，这为 UMF 同时处理先验生成和反应生成提供了统一的理论基础。

### 统一运动 VAE

统一运动 VAE 负责将异构运动数据（如单人数据集 HumanML3D 和双人交互数据集 InterHuman）编码到统一的多令牌潜空间中。首先将个体运动统一转换为非规范化的 SMPL 骨架表示（22 个关节点），随后通过 VAE 编码器生成多令牌潜变量 $Z$。VAE 的优化目标为：

$$\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_{\mathrm{geometric}} + \mathcal{L}_{\mathrm{reconstruction}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}$$

其中 $\mathcal{L}_{\mathrm{geometric}}$ 约束几何一致性，$\mathcal{L}_{\mathrm{reconstruction}}$ 保证重建质量，$\mathcal{L}_{\mathrm{KL}}$ 正则化潜空间分布。Latent Adapter 在此过程中起到关键作用——消融实验（Table 3）表明，移除 Latent Adapter 会显著降低跨数据集的泛化能力，验证了其在弥合异构数据分布差异中的必要性。

### P-Flow：金字塔流匹配先验生成

P-Flow 的核心创新在于根据噪声层级动态调整分辨率，以降低多令牌表示的计算开销。它将流匹配轨迹 $[0,1]$ 分解为 $K$ 个时间窗口，每个窗口在不同分辨率上操作。对于第 $k$ 个时间窗口，起始点和结束点分别定义为：

$$\hat{z}_{s_k} = s_k Up(Down(z_1, 2^k)) + (1 - s_k)\epsilon$$

$$\hat{z}_{e_k} = e_k Down(z_1, 2^{k-1}) + (1 - e_k)\epsilon$$

其中 $Down(\cdot, 2^k)$ 表示 $2^k$ 倍降采样，$Up(\cdot)$ 为上采样操作。在低噪声阶段（$t$ 接近 1）使用高分辨率，高噪声阶段（$t$ 接近 0）使用低分辨率，从而在保持生成质量的同时大幅降低计算量。P-Flow 的训练目标为：

$$\mathcal{L}_{\mathrm{P-Flow}} = \mathbb{E}_{k, t, \hat{z}_{e_k}, \hat{z}_{s_k}} \left\| G_\theta^P(\hat{z}_t; t, c) - (\hat{z}_{e_k} - \hat{z}_{s_k}) \right\|^2$$

其中 $G_\theta^P$ 为金字塔流 Transformer，$c$ 为文本条件。当阶段切换时，采用跳跃更新方案保证概率路径的连续性：

$$\hat{z}_{s_{k-1}} = \frac{s_{k-1}}{e_k} Up(\hat{z}_{e_k}) + \alpha n', \quad n' \sim \mathcal{N}(0, \Sigma')$$

消融实验（Table 4）证实，这种层级式分辨率设计在保持 FID 4.772 的同时，将 FLOPs 降至 74.7G（UMF-Fast 配置），相比全分辨率方案显著提升效率。

### S-Flow：半噪声流匹配反应生成

S-Flow 是 UMF 缓解自回归误差累积的关键模块。它通过联合优化两条概率路径来生成反应运动：反应变换路径和上下文重建路径。Context Adapter 首先将已生成的动作集合 $\mathcal{Z}_{gen}$ 编码为上下文表示：

$$C_i = TranEnc(\mathcal{Z}_{gen})$$

在此基础上，反应变换损失学习从上下文 $C$ 到目标反应 $W$ 的向量场：

$$\mathcal{L}_{\mathrm{trans}} = \mathbb{E}_{t, w_1, w_0} \| G_\theta^S(w_t^{\mathrm{react}}, t, c) - (W - C) \|_2^2$$

同时，上下文重建损失学习从噪声重建上下文 $C$ 的向量场：

$$\mathcal{L}_{\mathrm{recon}} = \mathbb{E}_{t, w_0, \epsilon} \| G_\theta^S(w_t^{\mathrm{cont}}, t, c) - (C - \epsilon) \|_2^2$$

两条路径共享同一个 Transformer 主干 $G_\theta^S$，但通过不同的输入构造实现功能分化。这种联合概率路径设计的优势在于：反应变换路径提供了从先验到反应的直接映射，而上下文重建路径则作为一种隐式正则化，迫使模型保持对上下文的敏感性，从而缓解多轮生成中的误差累积。消融实验（Table 5）提供了强有力的证据：移除 $\mathcal{L}_{\mathrm{recon}}$ 使 FID 从 4.772 升至 5.765；用 ControlNet 替代 Context Adapter 则使 FID 升至 6.868，效果远差于联合概率路径设计。此外，共享 P-Flow 与 S-Flow 的 Transformer 主干导致收敛困难（FID 升至 6.206），验证了两阶段独立建模的必要性。

### 推理阶段的非对称预算分配

推理时（Algorithm 1），P-Flow 和 S-Flow 均采用 Euler ODE 求解器进行采样。S-Flow 的单步更新为：

$$\hat{w}_{t_{m+1}} \gets \hat{w}_{t_m} + (t_{m+1} - t_m) G_{\theta}^{S}(\hat{w}_{t_m}, t_m, c)$$

值得注意的是，UMF 采用非对称的推理预算分配策略：P-Flow 获得充足的推理步数（如 50 步）以生成高质量运动先验，而 S-Flow 仅需极少的推理步数（如 10 步）即可完成反应生成。这种设计源于高质量先验降低了反应生成的难度，使得 S-Flow 在轻量推理下仍能保持鲁棒性。



## 实验与关键发现

### 主实验结果

UMF 在两个核心基准上均取得最优性能：多人生成基准 InterHuman 和动作‑反应合成基准 InterHuman‑AS。

**多人生成 (InterHuman)。** 如 Table 1 所示，UMF 在 FID 指标上达到 4.772，相比通用无人数限制基线 **FreeMotion** (Fan et al., ECCV 2024) 的 FID 降低 29%、Top‑3 R‑Precision 提升 28%；同时优于双人交互特化方法 **InterMask** (Javed et al., arXiv 2024)，FID 降低 7%。这表明统一潜空间与两阶段流匹配设计在无人数约束场景下具有显著优势。

**动作‑反应合成 (InterHuman‑AS)。** 如 Table 2 所示，UMF 在 FID 上达到 2.577±0.024，显著优于 **ReGenNet** (Xu et al., CVPR 2024)；Top‑3 R‑Precision 达到 0.530±0.006，相对提升约 30%。该结果验证了 S‑Flow 的联合概率路径在缓解自回归误差累积方面的有效性。

### 消融实验

消融实验围绕三个核心模块展开：统一运动 VAE 的先验设计、P‑Flow 的层级分辨率策略、S‑Flow 的联合概率路径。

**先验消融 (Table 3)。** 同时使用异构先验 (HP)、Latent Adapter (LA) 和多令牌分词器 (MT) 时，模型在 HumanML3D 和 InterHuman 上均取得最优 FID。移除任一组件均导致性能下降，验证了统一潜空间对桥接异构数据分布差距的关键作用。

**P‑Flow 消融 (Table 4)。** UMF 采用 2 阶段时间金字塔结构，通过层级分辨率设计将 FLOPs 降至 74.7G (UMF‑Fast)，同时保持 FID 4.772。相比全分辨率方案，P‑Flow 在维持生成质量的前提下显著降低计算开销。推理步数分配实验进一步表明，非对称推理预算（P‑Flow 50 步、S‑Flow 10 步）是效率与质量的最佳平衡点。

**S‑Flow 消融 (Table 5)。** 移除 Context Adapter 导致 FID 从 4.772 升至 7.038；移除重构损失 $L_{\text{recons}}$ 使 FID 升至 5.765。使用 ControlNet 替代上下文适配器（FID 6.868）或采用噪声无关路径（FID 5.617）均劣于 S‑Flow 的联合概率路径设计。共享 P‑Flow 与 S‑Flow 的 Transformer 主干导致收敛困难（FID 6.206）。这些结果共同验证了半噪声流匹配中反应变换与上下文重建联合优化的必要性。

### 失败模式与局限性

定性对比 (Figure 3) 显示，UMF 在双人及多人场景下生成质量整体优于 FreeMotion，但在以下情况仍存在局限：
- **群体规模限制**：UMF 以主角色为中心，仅适用于中等规模群体交互（约 10 人），无法直接扩展到密集人群动态（≈100 人）。
- **自回归误差累积**：尽管 S‑Flow 有效缓解了误差累积，但在极端长序列或超多轮反应生成中，累积效应仍可能逐渐显现。

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unified_Number_F/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison (zoom into see it better) between FreeMotion [12] and UMF. Red circles demonstrate successful cases, while Blue circles show failure cases*

### 重要图表结论

- **Figure 1** 阐释了 UMF 的核心贡献：相比固定人数的标准方法和依赖条件网络的自回归方法，UMF 利用异构运动先验作为反应流路径的自适应起点，从根本上缓解误差累积。
- **Figure 2** 展示了三阶段架构：统一运动 VAE 将异构数据编码到多令牌潜空间，P‑Flow 层级式生成运动先验，S‑Flow 基于上下文适配器联合学习反应变换与上下文重建。
- **Figure 4** 的用户研究表明，UMF 在真实感、交互合理性和文本匹配度三个维度上均优于 FreeMotion，进一步佐证了定量指标的提升具有感知层面的实际意义。

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unified_Number_F/figures/008_Figure_4.jpg]]
*Figure 4: The UMF number-free zero-shot generation user study. We asked users to compare our UMF (Blue Bar) to the FreeMotion (Red Bar) in a side-by-side view. The dashed line marks 50%. UMF outperforms FreeMotion in all three aspects of generation*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unified_Number_F/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Unified Motion Flow (UMF) architecture. The UMF framework consists of three stages. (A) Unified motion VAE: A motion VAE with latent adapters encodes raw motions from heterogeneous datasets (e.g., HumanML3D [13], InterHuman [32]) into a regularized multi-token latent representation (Z). (B) P-Flow motion prior generation: The Pyramid Flow Transformer synthesizes the latent motion prior (Zˇ) based on noisy latent motion and text conditions. The P-Flow operates hierarchically based on the timestep*

### 补充图表

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unified_Number_F/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on the InterHuman test sets. ± indicates a 95% confidence interval and → means the closer to ground truth the better. Boldface indicates the best result, while underline refers to the second best*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unified_Number_F/figures/005_Table_2.jpg]]
*Table 2: Comparison to state-of-the-art for human action-reaction synthesis on the InterHuman-AS dataset. ± indicates 95% confidence interval, → means that closer to Real is better. Bold indicates best result and underline indicates second best*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unified_Number_F/figures/006_Table_5.jpg]]
*Table 5: Ablation study of Semi-Noise Flow on the InterHuman dataset*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unified_Number_F/figures/007_Table_3.jpg]]
*Table 3: Ablation study of individual priors on the HumanML3D and InterHuman datasets. HP: Heterogeneous Priors; LA: Latent Adapter; MT: Multi-token Tokenizer*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unified_Number_F/figures/009_Table_4.jpg]]
*Table 4: Ablation study of Pyramid Flow on the InterHuman dataset. UMF has a 2-stage temporal pyramid structure. We report FLOPs(G) and AITS (Average Inference Time in Seconds)*



## 定位与知识库关联

### 1. 领域瓶颈与UMF的切入点

现有文本到运动生成方法面临两个核心瓶颈：**人数泛化能力不足**与**自回归误差累积**。标准方法（如 **MDM** (Tevet et al., arXiv 2022)、**T2M** (Guo et al., CVPR 2022)）受限于固定人数，无法生成可变规模的多人交互场景。自回归方法（如 **FreeMotion** (Fan et al., ECCV 2024)）虽然解耦了先验生成与反应生成，但其确定性条件网络（如ControlNet范式）在级联生成中容易传播早期误差，导致后续动作质量退化。

UMF的切入点在于将无人数约束生成重新表述为**两阶段流匹配问题**：单次先验生成 + 多次反应生成。这一分解的关键洞见是，反应生成不应仅依赖确定性条件注入，而应通过联合概率路径同时学习“反应变换”与“上下文重建”，从而在流匹配框架内主动缓解误差累积。

### 2. 与基线方法的关系定位

**FreeMotion** (Fan et al., ECCV 2024) 是UMF最直接的可比基线，同为通用无人数限制方法。UMF在InterHuman基准上的FID达到4.772，相比FreeMotion降低29%，Top3 R-Precision提升28%（Table 1）。这一提升的因果机制在于：FreeMotion采用自回归条件生成，反应质量高度依赖先验精度；UMF的S-Flow通过半噪声概率路径设计，使反应生成同时具备“从上下文变换”和“从噪声重建”两条路径，有效截断了误差传播链。

**InterMask** (Javed et al., arXiv 2024) 是双人交互生成的特化方法，在InterHuman上FID约为5.131。UMF以通用框架超越该特化方法7%（FID 4.772 vs. ≈5.131），验证了统一潜空间与异构数据联合训练的有效性。

**ReGenNet** (Xu et al., CVPR 2024) 专注人类动作-反应合成。在InterHuman-AS数据集上，UMF的Top3 R-Precision达到0.530±0.006，相比ReGenNet提升约30%，FID降至2.577±0.024（Table 2）。这表明S-Flow的联合概率路径设计在动作-反应合成场景中显著优于ReGenNet的确定性条件机制。

**TEMOS** (Petrovich et al., arXiv 2022) 和 **T2M** (Guo et al., CVPR 2022) 代表早期基于VAE或简单生成框架的单人方法，受限于固定人数约束，UMF通过多令牌统一潜空间和异构数据训练突破了这一限制。

### 3. 关键设计选择的谱系分析

**表示空间**：从原始运动空间到多令牌统一潜空间的跃迁是UMF的基础能力来源。统一运动VAE通过Latent Adapter桥接HumanML3D（单人）和InterHuman（双人）的分布差异，使得异构数据可在同一潜空间中联合训练。消融实验（Table 3）表明，移除异构先验或Latent Adapter均导致性能显著下降，验证了统一表示对泛化能力的关键作用。

**先验生成方式**：P-Flow将标准流匹配的全分辨率轨迹重新解释为层级式分段流。这一设计与传统金字塔生成方法（如级联扩散模型）的区别在于，P-Flow在单个Transformer内根据时间步动态切换分辨率，而非训练多个独立模型。Table 4显示，2阶段金字塔结构（UMF-Fast）在保持FID 4.772的同时将FLOPs降至74.7G，相比全分辨率方案显著提升效率。

**反应生成机制**：S-Flow的核心创新在于联合优化两条概率路径——反应变换（$C \to W$）与上下文重建（$\epsilon \to C$）。Table 5的消融实验提供了强因果证据：
- 移除Context Adapter使FID从4.772升至7.038，表明自适应上下文建模不可替代；
- 移除重构损失使FID升至5.765，验证上下文重建路径对训练稳定性的贡献；
- 使用ControlNet替代方案使FID升至6.868，效果差于联合概率路径设计；
- 采用噪声无关路径（Noise-Free path）使FID升至5.617，验证了半噪声设计的必要性。

### 4. 适用边界与局限

UMF的当前设计以**主角色为中心的中等规模群体交互**（约10人）为有效边界。方法的核心假设是存在一个明确的“先验角色”，后续角色依次对其做出反应。这一假设在以下场景中可能失效：
- **密集人群动态**（≈100人）：自回归级联的误差累积虽被S-Flow缓解，但在超长序列中仍可能显现；同时，P-Flow的层级分辨率设计未针对极大规模群体优化。
- **对称交互场景**：当不存在明确的主-从角色关系时，先验-反应的两阶段分解可能引入人为偏序。

论文明确指出的开放问题包括：如何利用大规模视频扩散模型的视觉先验将合成能力扩展到密集人群动态，以及在更大规模群体中保持计算效率并避免自回归误差累积。这些问题指向UMF向“人群模拟”方向扩展时需要解决的表示尺度与推理效率挑战。

### 5. 知识库定位总结

UMF在文本到运动生成领域的方法谱系中占据**通用无人数约束框架**的位置，其技术贡献可分解为三个可迁移的模块：
1. **多令牌统一潜空间**：为异构运动数据的联合建模提供了表示层方案，可迁移至其他跨数据集生成任务；
2. **P-Flow层级流匹配**：为多令牌表示的高效生成提供了计算优化范式，适用于任何需要处理变分辨率潜变量的流匹配/扩散模型；
3. **S-Flow半噪声联合路径**：为自回归/级联生成中的误差累积问题提供了概率框架内的解决方案，可推广至其他序列条件生成场景。

与同期工作的关系上，UMF在通用性上超越特化方法（InterMask、ReGenNet），在生成质量上超越同类通用方法（FreeMotion），其核心优势源于对“表示统一”和“概率路径设计”两个维度的联合优化。



## 原文 PDF

![[paperPDFs/CVPR_2026/Unified_Number_Free_Text_to_Motion_Generation_Via_Flow_Matching.pdf]]
