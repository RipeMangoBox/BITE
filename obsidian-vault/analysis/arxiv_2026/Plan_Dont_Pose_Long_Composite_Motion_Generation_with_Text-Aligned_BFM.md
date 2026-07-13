---
title: "Plan, Don't Pose: Long Composite Motion Generation with Text-Aligned BFM"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/Plan,_Don't_Pose:_Long_Composite_Motion_Generation_with_Text-Aligned_BFM.pdf"
project_link: null
code_link: null
aliases:
- PDTPLCMGTAB
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将运动生成置于紧凑的行为规划空间中，而非直接生成姿态，从而将语义规划与物理执行解耦，并利用预训练的行为基础模型作为可执行的运动先验。
primary_logic: 通过文本对齐的变分行为瓶颈，将策略潜在轨迹压缩为紧凑的、可语言区分的行为规划，然后仅需一个轻量的流匹配生成器来产生语义一致的运动规划，而物理执行由冻结的BFM策略保证。
claims:
- 在HumanML3D和KIT-ML数据集上，Text2BFM的R-Precision Top-3分别达到0.876和0.901，MultiModal Distance分别为2.498和2.658，均优于所有对比方法。
- 在长复合提示评估中，Text2BFM-Compose在N=3和N=4时达到更高的顺序准确率(0.671和0.509)和更低的过渡分数。
- HumanML3D 上 R-Precision Top-3 = 0.876±.005
- HumanML3D 上 MultiModal Distance = 2.498±.061
---

# Plan, Don't Pose: Long Composite Motion Generation with Text-Aligned BFM

> [!tip] 核心洞察
> 通过文本对齐的变分行为瓶颈，将策略潜在轨迹压缩为紧凑的、可语言区分的行为规划，然后仅需一个轻量的流匹配生成器来产生语义一致的运动规划，而物理执行由冻结的BFM策略保证。

| 字段 | 内容 |
|------|------|
| 中文题名 | 规划而非姿态：基于文本对齐BFM的长复合运动生成 |
| 英文题名 | Plan, Don't Pose: Long Composite Motion Generation with Text-Aligned BFM |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2605.29906) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Text2BFM |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-3 0.876±.005 vs 0.807 (MoMask) (+0.069)；MultiModal Distance 2.498±.061 vs 2.958 (MoMask) (-0.460)。
> - KIT-ML 上，R-Precision Top-3 0.901±.008 vs 0.781 (MoMask) (+0.120)；MultiModal Distance 2.658±.074 vs 2.779 (MoMask) (-0.121)。

## 概要

现有文本到运动生成方法将语义理解、长程时序组织和低层物理实现耦合在单一模型中，导致长时域复合提示下动作语义缺失、时序错乱和物理不合理。本文提出 **Text2BFM**，核心思路是将运动生成从直接合成姿态序列转变为在紧凑的行为规划空间中生成可执行的行为程序。具体而言，Text2BFM 利用一个预训练且冻结的行为基础模型（BFM）作为可执行的运动先验，通过文本对齐的变分行为瓶颈（Variational Behavioral Bottleneck）将 BFM 的策略潜在序列压缩为紧凑的、可语言区分的行为规划，再以轻量流匹配生成器在该紧凑流形中生成语义一致的运动规划，最终由冻结的 BFM 策略 rollout 产生物理合理的运动。

在 HumanML3D 和 KIT-ML 数据集上，Text2BFM 的 R-Precision Top-3 分别达到 0.876 和 0.901，MultiModal Distance 分别为 2.498 和 2.658，均显著优于 **MoMask** 等现有方法。在长复合提示评估中，Text2BFM-Compose 在 N=3 和 N=4 时达到更高的顺序准确率（0.671 和 0.509）和更低的过渡分数，验证了其在长时域语义一致性上的优势。然而，由于冻结 BFM 策略基于特定环境和动作空间训练，生成运动的 FID 值显著劣于直接在姿态空间生成的模型，存在分布质量上的权衡。此外，该方法对稀有动作、杂技动作和物体依赖交互的处理能力有限，且当前仅支持单人物运动生成。



文本到运动生成（text-to-motion generation）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，扩散模型和自回归模型在该领域取得了显著进展，代表性工作包括 **MDM**、**MLD**、**MotionDiffuse**、**T2M-GPT**、**ReMoDiffuse** 和 **MoMask** 等。然而，这些方法存在一个根本性的架构瓶颈：**语义理解、长程时序组织和低层物理执行被耦合在单一生成模型中**。

具体而言，现有方法通常直接在姿态序列空间或运动token空间中进行生成。这种端到端的范式在处理短时域、单一动作的简单提示时表现尚可，但面对长时域复合提示（如“一个人向前跑，然后左转，快速出拳，接着向右踢腿，之后向前走，举起双臂庆祝，最后开心地挥手”）时，会暴露出三个层面的系统性缺陷：

1. **语义缺失**：长提示中的某些动作阶段被遗漏或错误替换，生成的运动无法完整覆盖文本描述的所有语义单元。
2. **时序错乱**：动作的执行顺序与文本描述不一致，模型难以在长时域上保持精确的阶段顺序。
3. **物理不合理**：动作之间的过渡生硬、不自然，缺乏物理合理性，尤其是在需要协调多个动作的复合场景中。

造成上述问题的深层原因在于：**姿态空间本身并不适合承载高层语义规划**。姿态序列是高维、连续且高度冗余的表示，其中大部分变化与语义无关（如个人风格、速度微调等）。当生成模型被迫在这样一个信息密集的空间中同时完成语义理解和运动合成时，长程语义结构容易被局部物理细节淹没。

这一洞察引出了本文的核心动机：**将运动生成从姿态空间提升到行为规划空间**。如果能够将“做什么动作、以什么顺序做”的高层规划与“如何执行每个动作”的低层物理实现解耦，那么生成模型只需专注于前者——一个更紧凑、语义更明确的规划问题；而后者可以交给一个预训练好的、具备物理合理性的行为基础模型（Behavioral Foundation Model, BFM）来完成。这种“规划而非姿态”（Plan, Don't Pose）的范式转换，是本文方法设计的根本出发点。



## 核心方法与创新机理

### 问题瓶颈：耦合式生成导致长时域语义崩溃

现有文本到运动生成方法——包括 **MDM**、**MLD**、**MotionDiffuse**、**T2M-GPT**、**ReMoDiffuse** 和 **MoMask**——将语义理解、长程时序组织和低层物理实现耦合在单一生成模型中。这种耦合在短提示场景下尚可工作，但在长时域复合提示（如“先跑步，然后左转，出拳，再踢腿，最后挥手”）下暴露出系统性缺陷：动作语义缺失、时序顺序错乱、物理合理性下降。根本原因在于，直接生成高维姿态序列要求模型同时解决“做什么”和“怎么做”两个层次的问题，而这两个层次的表征需求和时序粒度存在根本性冲突。

### 核心思路：规划而非姿态

Text2BFM 的核心创新可以概括为一句原则：**将运动生成置于紧凑的行为规划空间中，而非直接生成姿态**。这一思路通过三个关键设计实现：

**1. 生成目标的根本转变（Changed Slot: 生成目标）**

传统方法直接生成姿态序列或潜在姿态，Text2BFM 则将生成目标转变为**紧凑行为程序**（compact behavioral programs）。具体而言，模型首先将预训练行为基础模型（BFM）的策略潜在序列 $z_{1:T_z}$ 通过变分行为瓶颈压缩为更短的运动程序 $m_{1:T_m}$（$T_m < T_z$），然后仅在这个低维行为流形上进行生成。这种设计将语义规划与物理执行解耦——生成器只需关注“做什么”，而“怎么做”由后续的冻结BFM策略保证。

**2. 运动表示空间的迁移（Changed Slot: 运动表示空间）**

传统方法在姿态序列或运动token空间中操作，Text2BFM 则将整个生成流程迁移到**BFM策略潜在空间**。这里的BFM策略（基于MetaMotivo训练流程，在HY-Motion数据集上预训练）是一个冻结的行为基础模型，提供潜在条件动作 $a_t \sim \pi_{\mathrm{BFM}}(a_t \mid s_t, z_t)$。策略潜在 $z_t$ 编码了局部运动意图，通过环境动态 $s_{t+1} \sim p_{\mathrm{env}}(s_{t+1} \mid s_t, a_t)$ 展开即可产生物理合理的运动。这种将BFM策略作为“可执行运动先验”的做法，使得生成器不再需要隐式地学习物理约束。

**3. 文本对齐的变分行为瓶颈（核心机制）**

这是连接语义规划与物理执行的关键桥梁。变分行为瓶颈（VBB）由三个损失函数联合训练：

$$\mathcal{L}_{\mathrm{VBB}} = \mathcal{L}_{\mathrm{rec}} + \beta \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{sem}} \mathcal{L}_{\mathrm{sem}}$$

- **重建损失** $\mathcal{L}_{\mathrm{rec}}$ 确保压缩后的行为程序能准确恢复原始策略潜在序列，包括潜在向量的MSE和策略动作分布的KL散度；
- **KL正则** $\mathcal{L}_{\mathrm{KL}}$ 将行为程序分布约束到标准高斯先验，为后续流匹配生成提供良好基础；
- **语义对齐损失** $\mathcal{L}_{\mathrm{sem}}$ 通过双向对比学习将紧凑行为程序与文本表示对齐，使得行为程序具有语言可区分性。

### 与基线方法的本质差异

| 维度 | 传统方法 | Text2BFM |
|------|----------|-----------|
| 生成目标 | 姿态序列或潜在姿态 | 紧凑行为程序 |
| 运动表示空间 | 姿态空间或运动token | BFM策略潜在空间 |
| 运动执行 | 生成网络直接输出姿态 | 冻结BFM策略rollout |
| 语义-物理耦合 | 耦合在单一模型 | 解耦为规划+执行 |

这种“规划而非姿态”的设计使得 Text2BFM 在长复合运动生成上具有天然优势：每个动作阶段通过局部可执行潜在表示，更容易保持动作的语义身份和时序顺序。实验验证了这一设计——在 N=3 和 N=4 的复合提示评估中，Text2BFM-Compose 的顺序准确率分别达到 0.671 和 0.509，显著优于直接生成方法（Table 2）。



Text2BFM 的核心设计理念是将文本到运动生成从**姿态空间**迁移到**行为规划空间**，从而实现语义理解与物理执行的解耦。整体框架由三个关键阶段构成：预训练行为基础模型（BFM）的潜在提取、文本对齐变分行为瓶颈（VBB）的构建，以及流匹配生成器的条件生成。

### 推理流程

给定一段文本描述，系统首先通过**文本适配器**将其编码为条件信号，随后在紧凑行为程序空间中，由**流匹配生成器**从高斯噪声出发，求解常微分方程生成文本一致的行为程序 $m_{1:T_m}$。该程序经 VBB 解码器恢复为策略潜在序列 $\hat{z}_{1:T_z}$，最终驱动**冻结的 BFM 策略**在物理仿真环境中 rollout，产生完整的运动序列。整个过程可概括为：

1. **文本编码**：文本适配器将自然语言指令映射为条件表示 $Y$。
2. **行为程序生成**：流匹配生成器在紧凑行为流形中从噪声生成 $m_{1:T_m}$。
3. **潜在解码**：VBB 解码器将行为程序展开为策略潜在序列 $\hat{z}_{1:T_z}$。
4. **运动执行**：冻结的 BFM 策略以 $\hat{z}_t$ 为条件，在环境中逐步生成动作 $a_t$ 并更新状态 $s_{t+1}$：

$$a_t \sim \pi_{\mathrm{BFM}}(a_t \mid s_t, \hat{z}_t), \qquad s_{t+1} \sim p_{\mathrm{env}}(s_{t+1} \mid s_t, a_t)$$

### 训练流程

训练分为两个独立阶段。**第一阶段**训练文本对齐的变分行为瓶颈：从运动数据中通过后向映射和 lookahead 窗口推断 BFM 策略潜在序列 $z_{1:T_z}$，随后 VBB 编码器将其压缩为紧凑行为程序 $m_{1:T_m}$，解码器再恢复为 $\hat{z}_{1:T_z}$。训练目标由三部分构成：

$$\mathcal{L}_{\mathrm{VBB}} = \mathcal{L}_{\mathrm{rec}} + \beta \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{sem}} \mathcal{L}_{\mathrm{sem}}$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 包含潜在向量的 MSE 与策略动作分布的 KL 散度，$\mathcal{L}_{\mathrm{KL}}$ 为正则化项，$\mathcal{L}_{\mathrm{sem}}$ 为双向对比损失，对齐行为程序与文本表示。

**第二阶段**固定 VBB 模块，在行为程序空间上训练流匹配生成器。采用线性插值路径 $m(r) = (1 - r) \epsilon + r m$，训练向量场 $v_{\eta}$ 预测恒定流：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{\epsilon, m, r, Y} \left[ \left\| v_{\eta}(m(r), r, Y) - (m - \epsilon) \right\|_2^2 \right]$$

推理时求解 ODE $\frac{d m(r)}{d r} = v_{\eta}(m(r), r, Y)$ 从噪声生成行为程序。

### 模块关系与数据流

Figure 2 展示了完整的训练与生成管线。各模块职责如下：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_29906/figures/002_Figure_2.jpg]]
*Figure 2: Text2BFM method and its principal diagram components. Shown are the training (steps 1 and 2) and the generation (3) pipelines*

- **BFM 策略（MetaMotivo）**：预训练冻结，在 HY-Motion 数据集上训练，提供潜在条件动作空间，是运动的物理执行器。
- **BFM 潜在提取**：利用后向映射从未来状态窗口推断策略潜在 $z_t^i = \mathrm{Proj}_z\left(\frac{1}{H_t} \sum_{k=0}^{H_t-1} B(s_{t+1+k}^i)\right)$，其中 $H_t = \min(L, T-t)$。
- **变分行为瓶颈（VBB）**：编码器-解码器结构，实现策略潜在序列的时间压缩与语义对齐，压缩比通过 $T_m < T_z$ 控制。
- **流匹配生成器**：在紧凑行为程序空间中进行条件生成，仅需 16 步采样。
- **文本适配器**：架构参数为宽度 768、深度 2、注意力头数 8（见 Table 6），将文本编码为条件信号。

### 复合运动生成

对于长复合提示，Text2BFM-Compose 将提示分解为子句 $Y_{\mathrm{comp}} = Y^{(1)} \text{ then } Y^{(2)} \text{ then } \cdots \text{ then } Y^{(N)}$，逐子句生成行为程序，解码后拼接策略潜在序列 $\hat{z}_{1:T}^{\mathrm{comp}} = \hat{z}_{1:T_1}^{(1)} \oplus \hat{z}_{1:T_2}^{(2)} \oplus \dots \oplus \hat{z}_{1:T_N}^{(N)}$，并在子句边界处混合 $O$ 个潜在步以平滑过渡。



Text2BFM 的核心架构由三个解耦的模块串联而成：冻结的行为基础模型（BFM）策略、文本对齐的变分行为瓶颈（VBB），以及流匹配生成器。整体流程遵循“规划而非姿态”的范式——先在紧凑的行为规划空间中生成可执行的程序，再交由 BFM 策略完成物理执行。

### 3.1 冻结 BFM 策略与潜在轨迹推断

运动生成不再直接输出关节姿态，而是通过一个冻结的 BFM 策略 $\pi_{\mathrm{BFM}}$ 在潜在条件 $z_t$ 下 rollout 产生动作与环境交互：

$$a_t \sim \pi_{\mathrm{BFM}}(a_t \mid s_t, z_t), \qquad s_{t+1} \sim p_{\mathrm{env}}(s_{t+1} \mid s_t, a_t)$$

其中 $s_t$ 为环境状态，$a_t$ 为动作，$z_t$ 为局部策略潜在变量。该 BFM 策略基于 MetaMotivo 训练流程在 HY-Motion 数据集上预训练，全程冻结不参与后续训练。

为从运动数据中提取策略潜在序列 $z_{1:T}$，Text2BFM 利用后向映射 $B(\cdot)$ 和 lookahead 窗口进行推断：

$$z_t^i = \mathrm{Proj}_z\left(\frac{1}{H_t} \sum_{k=0}^{H_t-1} B(s_{t+1+k}^i)\right), \quad H_t = \min(L, T-t)$$

该公式的核心思路是：从未来 $L$ 帧的状态信息中，通过后向映射和窗口平均反推当前时刻的策略潜在，从而将原始运动数据转化为可被后续模块处理的潜在轨迹。

### 3.2 变分行为瓶颈（VBB）

VBB 模块承担两个关键任务：将长时域策略潜在序列 $z_{1:T_z}$ 压缩为紧凑的行为程序 $m_{1:T_m}$（$T_m < T_z$），同时通过语义对比损失使该程序与文本对齐。

**编码-解码结构**：编码器将策略潜在序列压缩为紧凑表示，解码器将其恢复为可执行的潜在序列 $\hat{z}_{1:T_z}$。重建损失由两部分组成：

$$\mathcal{L}_{\mathrm{rec}} = \frac{1}{T_z} \sum_{t=1}^{T_z} \|z_t - \hat{z}_t\|_2^2 + \frac{\lambda_{\pi}}{T_z} \sum_{t=1}^{T_z} D_{\mathrm{KL}}\left(\pi_{\mathrm{BFM}}(\cdot \mid s_t, \hat{z}_t) \parallel \pi_{\mathrm{BFM}}(\cdot \mid s_t, z_t)\right)$$

第一项为潜在向量的 MSE，第二项为策略动作分布的 KL 散度——确保重建的潜在变量在冻结 BFM 策略下诱导出与原始运动一致的动作分布。

**语义对齐**：通过双向对比损失 $\mathcal{L}_{\mathrm{sem}} = \frac{1}{2}(\mathcal{L}_{mY} + \mathcal{L}_{Ym})$ 将紧凑行为程序与文本 token 对齐，使程序空间成为语言可区分的表示。

**总损失**：

$$\mathcal{L}_{\mathrm{VBB}} = \mathcal{L}_{\mathrm{rec}} + \beta \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{sem}} \mathcal{L}_{\mathrm{sem}}$$

其中 $\mathcal{L}_{\mathrm{KL}}$ 为变分 KL 正则项，约束潜在空间服从先验分布；$\beta$ 和 $\lambda_{\mathrm{sem}}$ 为权重超参数。

### 3.3 流匹配生成器

在 VBB 学习到的紧凑行为程序空间中，Text2BFM 采用流匹配（Flow Matching）而非扩散模型进行生成。流匹配使用线性插值路径连接噪声和目标程序：

$$m(r) = (1 - r) \epsilon + r m, \quad r \sim \mathcal{U}(0,1)$$

其中 $\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声，$m$ 为目标行为程序。向量场 $v_{\eta}$ 被训练为预测恒定流：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{\epsilon, m, r, Y} \left[ \left\| v_{\eta}(m(r), r, Y) - (m - \epsilon) \right\|_2^2 \right]$$

其中 $Y$ 为通过文本适配器编码的条件信号（适配器配置：宽度 768、深度 2、注意力头数 8）。推理时，从噪声出发求解 ODE 生成文本一致的行为程序：

$$\frac{d m(r)}{d r} = v_{\eta}(m(r), r, Y), \quad r \in [0,1]$$

生成的行为程序经 VBB 解码器恢复为策略潜在序列 $\hat{z}_{1:T_z}$，最终驱动冻结的 BFM 策略 rollout 产生完整运动。流匹配相比扩散模型的关键优势在于：仅需 16 步采样即可获得更优的 FID 和 MM-Dist（见 Table 5），推理效率显著提升。



## 实验与关键发现

### 标准文本到运动生成基准

在HumanML3D和KIT-ML两个标准数据集上，Text2BFM在语义对齐指标上展现出显著优势。如Table 1所示，Text2BFM在HumanML3D上取得R-Precision Top-3 0.876和MultiModal Distance 2.498，在KIT-ML上取得R-Precision Top-3 0.901和MultiModal Distance 2.658，均优于包括**MoMask**、**ReMoDiffuse**、**MLD**、**MDM**在内的所有对比方法。这表明在冻结BFM策略的潜在空间中生成运动，并通过文本对齐的变分行为瓶颈进行语义压缩，能够有效提升文本与运动之间的语义一致性。

然而，这种语义优势伴随着分布质量的权衡。Text2BFM在HumanML3D上的FID为1.172，显著高于直接在姿态空间生成的扩散模型（如MoMask的0.433）。这一差距源于冻结BFM策略本身的域限制——该策略基于特定的物理环境与动作空间训练，其生成的运动分布不可避免地偏离了纯运动学数据集的统计特性。这并非方法设计缺陷，而是“规划-执行”解耦范式下固有的分布质量-语义一致性权衡。

### 长复合运动生成评估

针对长时域复合提示的评估揭示了Text2BFM在时序语义保持上的核心优势。Table 2展示了在N≥3阶段复合提示上的表现：Text2BFM-Compose变体将提示分解为子句并分别生成紧凑行为程序，在N=3和N=4时分别达到0.671和0.509的顺序准确率，同时保持更低的过渡分数。

这一优势的因果机制在于：Text2BFM将每个动作阶段表示为局部可执行潜在序列，使得单个动作的身份和顺序得以在紧凑行为程序层面被显式保留。相比之下，直接生成姿态的方法将语义理解与长程时序组织耦合在单一生成过程中，当提示复杂度增加时，后续动作的语义信息容易被前序动作的生成过程“淹没”。Figure 3的定性对比直观展示了这一差异——Text2BFM在“跑步-左转-出拳-右踢-行走-举手-挥手”七阶段复合提示上，能够准确保持动作的顺序和身份，而对比方法出现了动作遗漏或顺序错乱。

### 变分行为瓶颈消融

Table 3的消融实验验证了文本对齐的变分行为瓶颈（VBB）各组件的作用。对比三种压缩方案：

- **平均池化**：将策略潜在序列压缩为无序摘要，丢失了时序结构，导致MM-Dist和R-Precision显著下降。
- **纯重构瓶颈**：通过编码器-解码器架构保留时序信息，但缺乏语义对齐，语义指标居中。
- **文本对齐VBB（完整方案）**：在重构损失基础上加入KL正则化和双向语义对比损失，在FID（1.172）、MM-Dist（2.498）和R-Precision（0.877）三个指标上均取得最优。

这表明语义对比损失 $\mathcal{L}_{\mathrm{sem}}$ 不仅提升了文本-运动对齐，还通过将紧凑行为程序拉向语言可区分的表示空间，间接改善了生成质量。

### 时间压缩与行为保真度

Table 4考察了时间压缩率对BFM潜在重构和行为保真度的影响。4倍和8倍时间压缩在潜在重构MSE和Action KL上保持较低水平，表明压缩后的行为程序仍能忠实恢复原始策略潜在序列并诱导相似的策略动作分布。然而，16倍压缩导致Action KL显著增加，说明过度压缩会破坏行为程序的时序粒度，使得解码后的潜在序列无法精确驱动冻结BFM策略产生目标行为。这一发现为行为程序的时间压缩率选择提供了实用指导。

### 生成器选择

Table 5对比了在相同行为瓶颈空间下，流匹配生成器与扩散模型的性能。流匹配在FID和MM-Dist上均优于扩散模型，且仅需16步采样即可完成生成，而扩散模型通常需要更多去噪步骤。这验证了流匹配在紧凑行为程序空间中的高效性——该空间的维度远低于原始姿态空间，线性插值路径足以建模从噪声到目标程序的变换。

### 局限性与失败模式

尽管Text2BFM在语义一致性和复合运动生成上表现突出，但存在以下明确局限：

1. **分布质量权衡**：由于冻结BFM策略基于特定物理环境训练，生成的FID显著劣于直接在姿态空间建模的方法。这是范式层面的固有权衡，需要手动验证是否可通过微调BFM策略来缓解。
2. **稀有动作覆盖不足**：对杂技动作、物体依赖交互等训练数据中不充分或未被BFM策略涵盖的行为，生成质量有限。
3. **单角色限制**：当前框架仅支持单人物运动生成，未扩展至多角色场景。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_29906/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on HumanML3D and KIT-ML datasets. Metrics: R-Precision Top-3 and MultiModality (the higher, the better), FID and MultiModal Distance (the lower, the better). Best values are highlighted in blue*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_29906/figures/005_Table_2.jpg]]
*Table 2: Evaluation on longer compositional prompts with*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_29906/figures/006_Table_3.jpg]]
*Table 3: Ablation on policy-latent sequence compression. All variants use the same frozen BFM policy and the same evaluation protocol. Best values are highlighted in blue*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_29906/figures/007_Table_4.jpg]]
*Table 4: Effect of temporal compression on BFM latent reconstruction and policy-level behavior preservation. Lower is better*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_29906/figures/008_Table_5.jpg]]
*Table 5: Ablation of the choice of the underlying generator. Both variants operate in the learned behavioral bottleneck space*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_29906/figures/009_Table_6.jpg]]
*Table 6: Core architecture and hyperparameters*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2605_29906/figures/011_Figure.jpg]]



## 定位与知识库关联

### 问题定位：从姿态生成到行为程序生成

现有文本到运动生成方法——包括基于VAE的**MotionDiffuse**、基于扩散的**MDM**、基于VQ-VAE的**T2M-GPT**和**MoMask**、基于检索增强扩散的**ReMoDiffuse**等——共享一个根本性瓶颈：它们将语义理解、长程时序组织和低层物理实现耦合在单一模型中，直接生成姿态序列或姿态潜在表示。当面对长时域复合提示（如“先跑，然后左转，快速出拳，再向右踢腿”）时，这种耦合导致三个典型失效模式：（1）部分动作被遗漏或语义混淆；（2）动作顺序错乱；（3）过渡段物理不合理。

Text2BFM的核心洞察是**将生成目标从姿态空间迁移到行为规划空间**。具体而言，它不直接生成关节旋转或位置，而是生成一段紧凑的“行为程序” $m_{1:T_m}$，该程序随后被解码为冻结的行为基础模型（BFM）策略的潜在条件序列 $z_{1:T_z}$，由BFM策略通过物理仿真 rollout 产生最终运动。这一设计将语义规划与物理执行解耦，使生成器只需关注“做什么、何时做”，而“怎么做”由预训练的策略先验保证。

### 方法谱系：行为基础模型与运动生成的交汇

Text2BFM处于两条研究线的交汇点：**通用行为基础模型**和**文本条件运动生成**。

在行为基础模型一侧，该方法直接复用预训练的**MetaMotivo**策略作为可执行的运动先验。BFM策略 $\pi_{\mathrm{BFM}}(a_t \mid s_t, z_t)$ 在HY-Motion大规模运动数据集上训练，学习了一个潜在条件策略空间，其中不同的潜在向量 $z_t$ 诱导不同的运动行为。Text2BFM的关键创新在于**将这一策略潜在空间作为运动生成的“语言”**——不是重新训练策略，而是学习如何用文本控制策略潜在序列。

在文本到运动生成一侧，Text2BFM与现有方法形成清晰的对比维度：

| 维度 | 主流方法（MoMask, MDM, MLD等） | Text2BFM |
|------|-------------------------------|----------|
| 生成空间 | 姿态序列或姿态潜在 | BFM策略潜在序列 |
| 物理执行 | 生成器隐式学习 | 冻结BFM策略显式保证 |
| 长程组织 | 依赖模型隐式学习时序依赖 | 变分行为瓶颈显式压缩并保留行为结构 |
| 文本对齐 | 全局或局部对比学习 | 双向语义对比损失对齐紧凑程序与文本 |

### 关键技术决策及其依据

**决策1：使用冻结BFM而非端到端训练。** 这避免了让生成器同时学习语义和物理的负担。代价是FID指标显著劣于直接在姿态空间生成的模型——因为BFM策略的动作空间和训练域限制了生成运动的分布覆盖。这是一个有意识的权衡：用分布质量换取语义一致性和物理合理性。

**决策2：变分行为瓶颈（VBB）而非简单池化。** 消融实验（Table 3）显示，平均池化将策略潜在序列压缩为无序摘要，导致MM-Dist和R-Precision显著下降；纯重构瓶颈缺乏语义对齐，同样表现不佳。VBB通过三项损失联合优化——重构损失 $\mathcal{L}_{\mathrm{rec}}$（含潜在MSE和策略动作KL散度）、KL先验正则 $\mathcal{L}_{\mathrm{KL}}$、以及双向语义对比损失 $\mathcal{L}_{\mathrm{sem}}$——在压缩率和语义保持之间取得平衡。

**决策3：流匹配而非扩散模型。** 在行为程序空间中，流匹配（Table 5）以更少的采样步数（16步）获得更优的FID和MM-Dist。这是因为紧凑行为程序的分布比姿态序列更平滑，适合用线性插值路径 $m(r) = (1-r)\epsilon + r m$ 建模。

**决策4：复合生成的逐子句分解。** Text2BFM-Compose将复合提示分解为原子子句，为每个子句独立生成紧凑行为程序，再在策略潜在层面拼接并做重叠区平滑。这一设计利用了行为程序的时间局部性——每个程序对应一个语义单元，拼接后由BFM策略自然处理过渡。

### 适用边界与局限

**分布质量的固有权衡。** 冻结BFM策略基于特定环境和动作空间训练，导致生成运动的FID值显著高于直接在姿态空间生成的方法。这是方法设计的结构性代价，无法通过调参消除。当应用场景对运动分布多样性要求极高（如生成稀有风格化动作）时，这一权衡可能不可接受。

**动作覆盖不足。** BFM策略的训练数据决定了可执行动作的上界。稀有动作（如杂技翻转）、精细手部交互、以及物体依赖的交互（如“拿起杯子”）在训练数据中不充分或未被策略潜在空间良好覆盖，导致这些提示下的生成质量下降。

**单角色限制。** 当前框架仅支持单人物运动生成。BFM策略和变分瓶颈均未建模多角色交互动力学，无法直接扩展至双人或群体场景。

**时间压缩的上限。** 消融实验（Table 4）表明，4倍和8倍时间压缩在潜在重构和行为保持上表现可接受，但16倍压缩导致Action KL显著增加，说明行为程序的分辨率存在下限——过度压缩会丢失细粒度行为信息。

### 开放问题

1. **多角色扩展。** 如何将行为程序框架扩展至多角色场景，同时保持角色间的行为一致性和交互协调？可能需要引入角色间条件机制或联合行为程序空间。

2. **域偏差缓解。** 能否通过轻量微调或适配器模块调整BFM策略的行为分布，在不牺牲物理合理性的前提下提升FID？这需要在策略微调和冻结先验之间找到平衡点。

3. **细粒度风格控制。** 当前方法通过文本控制“做什么”，但对“怎么做”（如力度、速度、风格）的控制粒度有限。能否在行为程序空间中引入额外的风格条件维度？

4. **稀有动作泛化。** 如何使框架在遇到训练数据中未见或少见的动作描述时，仍能生成合理的行为程序？这可能需要在行为程序空间中进行组合泛化或few-shot适应。



## 原文 PDF

![[paperPDFs/arxiv_2026/Plan,_Don't_Pose:_Long_Composite_Motion_Generation_with_Text-Aligned_BFM.pdf]]
