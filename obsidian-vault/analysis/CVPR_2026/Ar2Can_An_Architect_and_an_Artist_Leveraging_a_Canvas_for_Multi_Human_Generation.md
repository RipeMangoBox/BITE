---
title: "Ar2Can: An Architect and an Artist Leveraging a Canvas for Multi-Human Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Ar2Can_An_Architect_and_an_Artist_Leveraging_a_Canvas_for_Multi_Human_Generation.pdf
project_link: "https://qualcomm-ai-research.github.io/ar2can/"
code_link: null
aliases:
- Ar2Can
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 显式的空间布局规划（Architect）与身份保持渲染（Artist）的解耦，以及基于匈牙利匹配的质心对齐奖励信号。
primary_logic: 将多人生成分解为空间布局预测和身份保持渲染两个阶段，利用GRPO强化学习和组合奖励（计数、HPSv3美学质量、匈牙利面部匹配、姿态对齐）训练Artist模型，同时通过token共享机制处理遮挡并加速推理，从而在保持高画质的同时大幅提升身份一致性和计数准确性。
claims:
- 两阶段框架解耦空间规划与身份渲染，显著降低了身份混叠和计数错误。
- 基于匈牙利匹配的质心面部匹配奖励有效防止复制粘贴伪影，提升身份相似度。
- Ar2Can在MultiHuman-Testbench上计数准确率90.2%，Multi-ID 68.2，远超现有最佳方法。
- MultiHuman-Testbench 上 Count Accuracy = 90.2 (Arch-A)
---

# Ar2Can: An Architect and an Artist Leveraging a Canvas for Multi-Human Generation

> [!tip] 核心洞察
> 将多人生成分解为空间布局预测和身份保持渲染两个阶段，利用GRPO强化学习和组合奖励（计数、HPSv3美学质量、匈牙利面部匹配、姿态对齐）训练Artist模型，同时通过token共享机制处理遮挡并加速推理，从而在保持高画质的同时大幅提升身份一致性和计数准确性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Ar2Can：基于画布架构与艺术家解耦的多人生成框架 |
| 英文题名 | Ar2Can: An Architect and an Artist Leveraging a Canvas for Multi-Human Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.22690) · [Project](https://qualcomm-ai-research.github.io/ar2can/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Ar2Can |
| Dataset | MultiHuman-Testbench, MultiID-Test |

> [!tip] 效果简介
> - MultiHuman-Testbench 上，Count Accuracy 90.2 (Arch-A) vs GPT-Image-1 87.9 (+2.3)；Multi-ID Similarity 68.2 (Arch-B) vs MH-OmniGen 54.5 (+13.7)；HPSv2 Quality 30.8 (Arch-B) vs GPT-Image-1 30.3 (+0.5)。
> - MultiID-Test 上，Multi-ID (Ref) 54.3 vs WithAnyone 50.1 (+4.2)。

## 概要

**问题症结**：现有扩散模型在生成多人场景时，将空间布局规划与身份特征渲染耦合在单阶段流程中，导致身份混叠、人脸丢失、人数计数错误等系统性问题。随着人数增加，这种耦合引发的失败呈指数级放大。

**核心思路**：Ar2Can 将多人生成解耦为两个阶段——**Architect** 负责根据文本提示生成显式的空间布局（边界框与可选姿态），**Artist** 负责在该布局约束下渲染身份保持的逼真多人图像。这种解耦使模型无需在生成像素的同时隐式推理空间关系，从根本上降低了身份混淆和计数偏差。

**方法定位**：在训练范式上，Ar2Can 引入 **GRPO 强化学习** 替代传统的监督微调，通过组合奖励信号（计数准确性、HPSv3 美学质量、匈牙利质心面部匹配、姿态对齐）优化 Artist 模型。在数据层面，利用 DisCo 生成的合成多人场景与真实参考人脸构建训练样本，规避了对稀缺真实多人图像数据的依赖。在推理效率上，通过 token 丢弃与重叠区域共享 RoPE 编码，在保持质量的同时将推理时间压缩约 2 倍。

**主要结果**：在 MultiHuman-Testbench 基准上，Ar2Can 的计数准确率达到 **90.2%**，Multi-ID 身份相似度达到 **68.2**，统一评分 **72.4**，分别超越现有最佳方法 2.3、13.7 和 10.8 个百分点。用户偏好研究中，Ar2Can 在提示对齐、身份相似度和图像质量三个维度均显著优于对比方法。

扩散模型在文本到图像生成领域取得了显著进展，但在**参考图像引导的多人场景生成**这一任务上仍面临根本性瓶颈。当用户提供多张参考人脸图像并要求生成包含这些特定人物的合照时，现有方法普遍出现**身份混叠**（不同人物的面部特征相互融合）、**人脸丢失**（部分参考人物未出现在生成图像中）以及**人数计数错误**（生成人数与提示要求不符）等问题。

这些问题的根源在于：现有方法将**空间布局规划**与**身份特征渲染**耦合在单一的端到端生成过程中。无论是基于区域条件的模型（如 **WithAnyone**）、基于身份补丁的方法（如 **ID-Patch**），还是通用多人生成框架（如 **MH-OmniGen**、**DreamO**、**UMO-UNO**），都缺乏对“每个人应该出现在哪里”的显式空间推理，导致模型在生成时难以协调多个身份的空间分配，进而产生身份冲突和计数偏差。

此外，训练数据的匮乏加剧了这一困境。真实世界中带有精确身份标注的多人图像稀缺，而现有方法大多依赖监督微调或直接推理，缺乏有效的奖励信号来引导模型学习身份保持与空间布局之间的平衡。

Ar2Can 的核心动机正是针对上述瓶颈：**将多人场景生成显式地分解为空间布局预测和身份保持渲染两个解耦阶段**，并引入基于强化学习的组合奖励机制来优化身份一致性和图像质量。这一思路借鉴了人类绘画的认知过程——先由“建筑师”规划构图，再由“艺术家”精细渲染——从而在保持高画质的同时，大幅提升身份一致性和计数准确性。

## 核心方法与创新机理

Ar2Can 的核心创新在于将多人生成任务**解耦为空间布局规划与身份保持渲染两个独立阶段**，并通过**强化学习驱动的组合奖励机制**和**高效的 token 处理策略**，系统性地解决了现有方法中身份混叠、人脸丢失和计数错误等瓶颈问题。

### 1. 两阶段解耦范式：Architect + Artist

现有扩散模型（如 **GPT-Image-1**、**MH-OmniGen**、**OmniGen** 等）将空间布局规划与身份特征渲染耦合在单阶段端到端生成中，导致模型难以同时兼顾空间准确性和身份保真度。Ar2Can 将这一过程显式分解为两个阶段（Figure 1）：

- **Architect 模块**：根据文本提示 $p$ 预测结构化的空间布局 $\mathcal{L} = \{b_1, \ldots, b_N\}$，其中 $b_i = (x_i, y_i, w_i, h_i)$ 为每个人的边界框，可选地包含姿态信息。该模块负责“在哪里放置人物”的规划任务，将空间推理从像素生成中剥离。
- **Artist 模块**：接收布局 $\mathcal{L}$、文本提示 $p$ 和参考人脸 $\{I_{\text{ref}}\}$，渲染出身份保持的逼真多人图像 $x \sim \pi_\theta(x \mid p, \mathcal{L}, \{I_{\text{ref}}\})$。该模块专注于“如何渲染身份”的生成任务。

这一解耦的核心优势在于：**每个模块只需专注于其子任务**，避免了耦合模型中空间约束与身份特征之间的冲突。实验表明，该范式使计数准确率达到 90.2%，Multi-ID 相似度达到 68.2，远超现有最佳方法（Table 1）。

### 2. GRPO 强化学习与组合奖励

Ar2Can 摒弃了传统的监督微调范式，转而采用**组相对策略优化（GRPO）**训练 Artist 模型。GRPO 的核心机制是对同一提示采样一组 $M$ 个图像，利用组内标准化优势函数 $A_i = (r(x_i, p) - \mu_G) / (\sigma_G + \epsilon)$ 进行策略优化：

$$\mathcal{L}_{\mathrm{GRPO}} = \mathbb{E}_{p, G} \left[ \sum_{i=1}^{M} A_i \log \frac{\pi_{\theta}(x_i \mid p)}{\pi_{\mathrm{ref}}(x_i \mid p)} - \beta_{\mathrm{KL}} \mathrm{KL}(\pi_{\theta} \parallel \pi_{\mathrm{ref}}) \right]$$

Artist 训练使用四种组合奖励（Eq. 4）：

$$r_{\mathrm{Artist}}(x, p, \mathcal{L}) = \alpha \cdot r_{\mathrm{count}} + \beta \cdot r_{\mathrm{hps}} + \zeta \cdot r_{\mathrm{face}} + \eta \cdot r_{\mathrm{pose}}$$

其中关键创新在于 **$r_{\mathrm{face}}$ 面部匹配奖励**的设计：传统方法通常按位置顺序简单匹配参考人脸与生成人脸，容易导致“复制粘贴”伪影。Ar2Can 引入**基于匈牙利匹配的质心对齐机制**——首先在质心距离成本矩阵上执行匈牙利匹配建立空间对应关系，然后计算匹配对的 ArcFace 余弦相似度：

$$s_i = \frac{e_i^{\mathrm{ref}} \cdot e_{\pi^*(i)}^{\mathrm{gen}}}{\|e_i^{\mathrm{ref}}\| \|e_{\pi^*(i)}^{\mathrm{gen}}\|}$$

消融实验证实，匈牙利质心匹配（HCM）取代简单位置匹配后，Multi-ID 从 55.2 提升至 60.3，HPS 从 27.6 恢复至 30.9（Table 3），有效防止了身份错配和伪影。

### 3. Token 共享与丢弃机制

多人场景中，画布区域的大部分 token 不包含有效信息，且人脸重叠区域的 token 冗余严重。Ar2Can 提出两项 token 优化策略（Figure 5）：

- **非信息 token 丢弃**：丢弃画布中不含人脸区域的 token，减少无效计算。
- **重叠区域 RoPE 共享**：当多个人脸边界框重叠时，为重叠区域分配**相同的 RoPE 位置编码**，即 $\mathrm{RoPE}(\mathrm{tokens}(b_i)) = \mathrm{RoPE}(\mathrm{tokens}(b_j))$。这一设计向模型传递了“空间竞争”信号，使其能够学习自然的遮挡和深度排序，而非简单地叠加人脸。

该策略使推理时间减少约 2 倍（15s vs 28s），同时保持统一评分最高（72.4），在质量-延迟权衡上显著优于无优化的基线（Figure 7a）。

### 4. 数据构建与课程学习

Ar2Can 不依赖真实多人图像数据集，而是利用 **DisCo** 生成合成多人场景，并与真实参考人脸配对构建混合训练样本（Section 3.2）。训练采用**课程学习策略**，根据训练进程 $t$ 动态调整人数 $N$ 的采样概率：

$$p(N \mid t) = \begin{cases} 1/2 & N \in \{2,3\}, t \le \tau \\ 1/6 & \text{otherwise} \end{cases}$$

即训练初期集中采样 2-3 人的简单场景，随后均匀扩展到 2-7 人。消融实验表明，课程学习使完整模型计数准确率达 86.9%，Multi-ID 达 68.2（Table 3），验证了渐进式难度提升对复杂多人场景泛化的必要性。

### 创新总结

| 创新维度 | 基线方法 | Ar2Can 方案 | 关键效果 |
|---------|---------|------------|---------|
| 生成范式 | 单阶段端到端 | 两阶段 Architect + Artist 解耦 | 计数 +2.3，Multi-ID +13.7 |
| 训练方法 | 监督微调/直接推理 | GRPO + 四维组合奖励 | 统一评分 +10.8 |
| 面部匹配 | 简单位置对应 | 匈牙利质心匹配 | Multi-ID +5.1 |
| Token 处理 | 全画布输入 | 丢弃 + RoPE 共享 | 推理加速 2× |
| 数据依赖 | 真实多人图像 | 合成场景 + 真实人脸 | 无需真实多人标注 |

Ar2Can 提出一种**两阶段解耦框架**，将多人生成任务分解为空间布局规划与身份保持渲染两个独立阶段，以解决现有扩散模型将布局与身份耦合所导致的身份混叠、人脸丢失和计数错误问题。

### Pipeline 总览

整个生成流程遵循“先规划，后渲染”的原则，由两个核心模块串联构成（图1）：

1. **Architect（布局规划器）**：接收文本提示 $p$，预测结构化的空间布局 $\mathcal{L} = \{b_1, \ldots, b_N\}$，其中每个 $b_i = (x_i, y_i, w_i, h_i)$ 定义一个人的边界框位置与尺寸。Architect 提供两种实现变体：
   - **Architect-A**：基于轻量级大语言模型 Qwen-2.5 (0.5B) 的自回归布局生成器，通过扩展的特殊 token（`<SoL>`、`<EoL>`、`<C>`）输出结构化布局序列。
   - **Architect-B**：基于 Flux-Schnell 的文生图模型，通过 GRPO 强化学习微调，直接生成布局草图作为空间规划。

2. **Artist（身份渲染器）**：接收文本提示 $p$、布局 $\mathcal{L}$ 以及一组参考人脸 $\{I_i^{\text{ref}}\}$，合成最终的多人真实感图像 $x \sim \pi_\theta(x \mid p, \mathcal{L}, \{I_i^{\text{ref}}\})$。Artist 基于 Kontext（Flux-Kontext）模型，通过 GRPO 强化学习与组合奖励函数进行训练。

### 数据构建管线

由于缺乏大规模真实多人图像数据集，Ar2Can 采用合成数据策略构建训练样本（图 C.1）：
- 利用 **DisCo** 模型根据文本提示生成合成多人场景图像；
- 将合成场景中的人脸替换为来自多源数据集（如多视角参考集 $\mathcal{D}_1$）的真实参考人脸；
- 构建包含画布（canvas）、参考人脸、文本提示和空间布局的完整训练样本。

### 输入输出流

| 阶段 | 输入 | 输出 |
|------|------|------|
| Architect | 文本提示 $p$ | 空间布局 $\mathcal{L}$（边界框集合，可选姿态） |
| Artist | 文本提示 $p$、布局 $\mathcal{L}$、参考人脸 $\{I_i^{\text{ref}}\}$ | 最终多人图像 $x$ |

### 关键设计决策

**解耦的核心动机**在于：单阶段模型将“谁在哪里”的空间推理与“长什么样”的身份渲染混在同一去噪过程中，导致注意力机制在多人脸区域产生混淆。通过显式分离布局规划，Artist 只需专注于在给定空间约束下保持身份一致性的渲染任务，大幅降低了优化难度。

**Token 共享与丢弃机制**进一步优化推理效率：对于画布中不包含人脸的空白区域，直接丢弃其 token；对于多人脸重叠区域，分配**相同的 RoPE 位置编码**，使模型将重叠区域视为空间竞争信号，从而自然学习遮挡与深度排序关系。该策略使推理 token 数量平均减少约 2 倍（推理时间从 28s 降至 15s），同时保持生成质量（图7a）。

> **注意**：Architect 与 Artist 的具体训练目标、奖励函数设计及消融分析详见后续“核心方法”与“实验与分析”章节。

![[assets/figures/papers/paper_list_l983_https_arxiv_org_abs_2511_22690/figures/001_Figure_1.jpg]]
*Figure 1: Ar2Can Framework Overview. Our two-stage approach decomposes multi-human generation into spatial planning (Architect) and identity-preserving rendering (Artist)*

![[assets/figures/papers/paper_list_l983_https_arxiv_org_abs_2511_22690/figures/016_Figure.jpg]]
*Figure: a) Total Loss b) Cross-Entropy Loss c) Co-Ordinate Loss Figure D.1. Training curves of Architecture-A (LLM-based) with and without data sorting. After 2000 steps, training is dominated by the optimization of bounding-box coordinate regression. A clear gap emerges between sorted and unsorted data: sorting leads to more stable learning and faster convergence in the coordinate regression stage under the same number of training iterations*

### 两阶段生成框架

Ar2Can将多人图像生成解耦为两个独立阶段：**Architect** 负责空间布局规划，**Artist** 负责身份保持渲染。给定文本提示 $p$ 和参考人脸集合 $\{I_{\text{ref}}\}$，Architect模块 $\psi$ 首先预测空间布局 $\mathcal{L} = \{b_1, \ldots, b_N\}$，其中每个边界框 $b_i = (x_i, y_i, w_i, h_i)$ 定义了第 $i$ 个人的空间位置，质心为 $c_i = (x_i + w_i/2, \; y_i + h_i/2)$。随后Artist模块 $\pi_\theta$ 基于布局、提示和参考人脸合成最终图像 $x \sim \pi_\theta(x \mid p, \mathcal{L}, \{I_{\text{ref}}\})$。

这一解耦设计的核心因果机制在于：将空间规划与身份渲染分离，使每个模块专注于各自子任务，从根本上避免了端到端生成中空间布局与身份特征耦合导致的身份混叠和计数错误。

### Architect模块

Architect提供两种实现变体。**Architect-A** 基于自回归语言模型构建，采用Qwen-2.5（0.5B）作为基座，扩展tokenizer引入布局结构token：`<SoL>`（布局起始）、`<EoL>`（布局结束）和`<C>`（坐标占位符）。其训练损失为交叉熵token预测损失与坐标回归损失的组合：

$$\mathcal{L}_{\text{Arch-A}} = \mathcal{L}_{\text{CE}} + \lambda_{\text{coord}} \mathcal{L}_{\text{coord}}$$

其中 $\mathcal{L}_{\text{CE}}$ 为token级别的交叉熵损失，$\mathcal{L}_{\text{coord}}$ 结合gIoU和L1损失对边界框坐标进行回归，$\lambda_{\text{coord}}$ 为平衡系数。SFT训练将Architect-A的计数准确率从15.2%提升至97.7%。

**Architect-B** 采用Flux-Schnell作为基座文生图模型，通过布局草图方式生成空间规划。其训练使用GRPO（Group Relative Policy Optimization）强化学习，奖励函数为：

$$r_{\text{Arch-B}}(x, p) = \alpha \cdot r_{\text{count}}(x) + \beta \cdot r_{\text{hps}}(x, p)$$

其中 $r_{\text{count}}$ 评估生成图像中的人数与提示的匹配程度，$r_{\text{hps}}$ 基于HPSv3评估文本对齐和美学质量。Architect-B通过RFT（Reinforcement Fine-Tuning）将计数准确率从59.9%提升至93.2%。

### Artist模块与GRPO训练

Artist模块的训练采用GRPO强化学习框架。对于每个提示 $p$，采样一组 $M$ 个图像构成组 $G$，计算组内标准化优势函数：

$$A_i = \frac{r(x_i, p) - \mu_G}{\sigma_G + \epsilon}$$

其中 $\mu_G$ 和 $\sigma_G$ 分别为组内奖励的均值和标准差。GRPO损失函数为：

$$\mathcal{L}_{\text{GRPO}} = \mathbb{E}_{p, G}\left[\sum_{i=1}^{M} A_i \log \frac{\pi_\theta(x_i \mid p)}{\pi_{\text{ref}}(x_i \mid p)} - \beta_{\text{KL}} \text{KL}(\pi_\theta \parallel \pi_{\text{ref}})\right]$$

其中 $\pi_\theta$ 为当前策略，$\pi_{\text{ref}}$ 为参考策略，KL散度项约束策略更新幅度。

Artist的组合奖励函数包含四个维度：

$$r_{\text{Artist}}(x, p, \mathcal{L}) = \alpha \cdot r_{\text{count}}(x) + \beta \cdot r_{\text{hps}}(x, p) + \zeta \cdot r_{\text{face}}(x, \mathcal{L}) + \eta \cdot r_{\text{pose}}(x, \mathcal{L})$$

各奖励项的作用机制如下：
- **计数奖励** $r_{\text{count}}$：评估生成图像中的实际人数与布局指定人数的匹配度，是解决计数错误的核心信号。
- **美学质量奖励** $r_{\text{hps}}$：基于HPSv3模型评估文本-图像对齐和整体美学质量。消融实验表明，移除该奖励会导致生成图像出现平坦照明和不自然色彩。
- **面部匹配奖励** $r_{\text{face}}$：通过匈牙利匹配建立参考人脸与生成人脸的空间对应关系，然后计算余弦相似度。对于第 $i$ 个参考人脸，其匹配相似度为：

$$s_i = \begin{cases} \dfrac{e_i^{\text{ref}} \cdot e_{\pi^*(i)}^{\text{gen}}}{\|e_i^{\text{ref}}\| \|e_{\pi^*(i)}^{\text{gen}}\|} & \text{if } i \text{ has valid match} \\ 0 & \text{otherwise} \end{cases}$$

其中 $e_i^{\text{ref}}$ 和 $e_{\pi^*(i)}^{\text{gen}}$ 分别为参考人脸和匹配生成人脸的ArcFace嵌入，$\pi^*(i)$ 为匈牙利算法在质心距离成本矩阵上求得的最优匹配。该奖励有效抑制了“复制粘贴”伪影，消融实验显示将Multi-ID从55.2提升至60.3。
- **姿态奖励** $r_{\text{pose}}$：在姿态控制变体中，评估生成姿态与指定姿态的对齐程度。

### Token共享与丢弃机制

为处理人脸遮挡并加速推理，Ar2Can引入token共享策略。对于非信息性的画布背景token，直接丢弃以减少计算量。对于重叠的人脸区域，分配相同的RoPE位置编码，使模型感知到空间竞争关系，从而学习自然的遮挡和深度排序。该策略使推理时间减少约2倍（从28秒降至15秒），同时保持统一评分最高（72.4）。

### 课程学习策略

训练采用基于人数的课程学习，采样概率随训练进程动态调整：

$$p(N \mid t) = \begin{cases} \dfrac{1}{2} & \text{if } N \in \{2, 3\} \text{ and } t \leq \tau \\ \dfrac{1}{6} & \text{otherwise} \end{cases}$$

其中 $N$ 为生成人数，$t$ 为当前训练轮次，$\tau$ 为课程转换阈值。在 $t \leq \tau$ 阶段，模型专注于2-3人的简单场景；之后均匀采样2-7人的场景。消融实验证实课程学习对最终性能至关重要，完整模型计数准确率达86.9%，Multi-ID达68.2。

![[assets/figures/papers/paper_list_l983_https_arxiv_org_abs_2511_22690/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of the LLM-based Architect-A for layout. Top: response example for spatial layout generation. Bottom: our lightweight LLM extended with special tokens*

![[assets/figures/papers/paper_list_l983_https_arxiv_org_abs_2511_22690/figures/004_Figure_4.jpg]]
*Figure 4: Artist training pipeline with GRPO. Given the input canvas and text prompt, sample a group of images and optimize over compositional rewards: count accuracy, prompt alignment/aesthetic quality (HPSv3), spatially-grounded face matching and pose correction*

## 实验与关键发现

### 主实验结果

Ar2Can在MultiHuman-Testbench上进行了全面的定量评估，结果如Table 1所示。该基准从五个维度衡量多人生成能力：计数准确性（Count）、多人身份相似度（Multi-ID）、美学质量（HPSv2）、动作-场景对齐（Action-S）和动作-角色对齐（Action-C），并通过加权求和得到统一评分（Unified Metric）。

**计数准确性**方面，基于LLM的Architect-A变体达到90.2%，显著超越GPT-Image-1（87.9%）等专有基线，以及MH-OmniGen（75.3%）等开源方法。Architect-B（基于Flux-Schnell的布局草图变体）也达到86.9%，验证了两阶段解耦对人数控制的有效性。

**身份保持**方面，Architect-B变体以68.2的Multi-ID得分领先所有方法，相比MH-OmniGen（54.5）提升13.7个点，相比GPT-Image-1（46.0）提升22.2个点。这一优势源于匈牙利质心匹配奖励机制：通过建立参考人脸与生成人脸的空间对应关系，模型学习在正确位置渲染对应身份，而非简单复制粘贴。

**统一评分**方面，Architect-B以72.4分取得最优综合性能，Architect-A以71.4分紧随其后，均大幅超越MH-OmniGen（61.6）和GPT-Image-1（64.6）。值得注意的是，Ar2Can在保持高身份相似度的同时，美学质量（HPSv2 30.8）与专有方法GPT-Image-1（30.3）相当，未出现常见的身份-质量权衡。

Figure 6的定性对比进一步揭示了现有方法的典型失败模式：GPT-Image-1和Nanobanana等专有方法在多人场景中频繁出现身份混叠和面部丢失；开源方法如MH-OmniGen和UniPortrait虽能保持部分身份，但计数错误和复制粘贴伪影严重。Ar2Can通过显式的空间布局约束，有效避免了这些问题。

在MultiID-2M测试集（Table 2）上，Ar2Can在输入身份相似度（54.3）和真实身份相似度（38.1）两个指标上均优于WithAnyone（50.1/34.4），验证了方法在更大规模身份保持任务上的泛化能力。

### 消融实验

Table 3展示了训练组件逐步叠加的消融结果，揭示了各奖励信号和训练策略的因果贡献。

**基础模型**仅使用计数奖励训练时，计数准确率可达85.4%，但Multi-ID仅为37.5，HPSv2为27.6。这是因为模型缺乏身份约束，倾向于生成任意人脸填充指定位置。

**面部匹配奖励**的引入将Multi-ID从37.5提升至55.2（+17.7），但HPSv2下降至25.8。这反映了身份保持与图像质量的早期权衡：模型为匹配参考人脸牺牲了整体美感。

**匈牙利质心匹配（HCM）**替换简单位置匹配后，Multi-ID进一步提升至60.3（+5.1），HPSv2恢复至30.9。HCM通过解决空间分配歧义，使模型在正确位置渲染正确身份，同时释放了优化自由度以提升画质。Figure E.7的定性对比显示，移除HPSv3奖励会导致平坦照明和不自然色彩，验证了美学奖励的必要性。

**课程学习**策略（Eq. 6）使完整模型计数准确率达86.9，Multi-ID达68.2。通过先学习2-3人场景再扩展到更大群体，模型逐步掌握了密集场景下的空间竞争处理能力。

**Token共享机制**（Figure 5）将重叠区域赋予相同RoPE位置编码，使推理时间从28秒降至15秒（约2倍加速，Table D.4），同时统一评分达到最高的72.4。这表明共享位置编码不仅加速推理，还通过隐式建模遮挡关系提升了渲染质量。

### 失败模式与局限性

尽管Ar2Can在整体指标上表现优异，但分析揭示了若干局限：

1. **大规模群体退化**：当人数超过3人时，个体面部表情和身体姿态的控制力减弱。Figure 7b显示Multi-ID随人数增加而下降，反映了密集场景下身份保持的固有挑战。

2. **复杂动作生成不足**：Action-C指标（Architect-B 71.4）仍有提升空间，表明当前方法在多人交互动作（如拥抱、击掌）的生成上不如静态姿态可靠。

3. **姿态控制变体的伪影**：引入姿态条件后，复制粘贴伪影增加，说明空间约束与身份保持的联合优化需要更精细的平衡策略。

4. **未验证超大规模场景**：实验仅覆盖1-5人场景，8人以上群体的生成能力尚未探索。

### 用户偏好研究

Table 4展示了25名评估者对25个三元组样本的盲评结果。Ar2Can在提示对齐（60.0%胜率）、身份相似度（56.7%）和整体质量（58.7%）三个维度上均获得最高偏好，验证了自动指标与人类感知的一致性。GPT-Image-1在身份相似度上仅获6.7%胜率，反映了专有方法在多人身份保持上的根本性局限。

### 推理效率分析

Table D.4的延迟分解显示，Ar2Can的Architect-A总延迟为15.5秒（Architect 1.5s + Artist 14.0s），相比Architect-B（28.0s）加速约1.8倍。LLM-based布局预测的高效性（仅需1.5秒生成结构化布局）使得整体流程适用于交互式应用场景。

![[assets/figures/papers/paper_list_l983_https_arxiv_org_abs_2511_22690/figures/018_Table_1.jpg]]
*Table 1: Ar2Can achieves the most balanced performance across all MultiHuman-Testbench metrics, demonstrating superior count accuracy and identity preservation while maintaining competitive prompt alignment and action scores. The SOTA methods exhibit clear trade-offs, excelling in some metrics while failing in others*

![[assets/figures/papers/paper_list_l983_https_arxiv_org_abs_2511_22690/figures/011_Table_3.jpg]]
*Table 3: Ablation study on key training components. We progressively add each component to measure its contribution to count accuracy, identity preservation, and image quality*

## 定位与知识库关联

### 1. 与现有工作的关系

Ar2Can 的核心贡献在于将多人生成任务**解耦为两阶段**：空间布局规划（Architect）与身份保持渲染（Artist）。这一设计直接回应了现有扩散模型在多人场景中的根本瓶颈——将布局规划与身份渲染耦合在单阶段生成中，导致身份混叠、人脸丢失和计数错误。

**与单阶段方法的对比。** 当前主流的多人生成方法，无论是专有模型 **GPT-Image-1**、**Nanobanana**，还是开源模型 **OmniGen**、**MH-OmniGen**、**DreamO**、**UMO-UNO**、**UMO-OmniGen2**、**XVerse**，均采用端到端的单阶段生成范式。这些方法缺乏显式的空间约束机制，在面对复杂文本提示和多人身份保持需求时，往往出现人脸融合、计数不准或复制粘贴伪影。Ar2Can 通过引入 Architect 模块自动生成边界框布局，将空间规划从像素生成中剥离，从根本上改变了这一范式。

**与区域条件方法的区别。** **WithAnyone** 和 **ID-Patch** 等方法虽然也使用了空间条件（如边界框或身份补丁），但通常需要用户手动标注布局，且空间条件与身份渲染仍耦合在同一生成过程中。Ar2Can 的 Architect 模块实现了**自动布局预测**，无需人工标注，同时通过 GRPO 强化学习训练 Artist，使身份渲染与空间布局形成松耦合的优化关系。

**与基线 Artist 模型的关系。** Ar2Can 的 Artist 模块基于 **Kontext（Flux-Kontext）** 架构构建，但通过以下关键改进实现了质的飞跃：
- **训练范式升级**：从监督微调转向 GRPO 强化学习，引入组合奖励信号（计数准确性、HPSv3 美学质量、匈牙利面部匹配、姿态对齐），使模型在保持高画质的同时大幅提升身份一致性和计数准确性。
- **Token 处理创新**：引入 token 丢弃与重叠区域共享 RoPE 编码机制，在减少约 2 倍推理时间的同时，使模型能够学习自然的遮挡和深度排序。

### 2. 适用边界

Ar2Can 在以下条件下表现最优：
- **人数范围**：1-5 人的场景生成效果最佳。实验表明，Multi-ID 相似度和 HPSv2 分数在 1-5 人范围内保持稳定，但超过 3 人时对个体面部表情和身体姿态的控制力开始减弱。
- **身份保持**：在基于参考图像的多人身份保持任务上优势最为显著，MultiHuman-Testbench 上 Multi-ID 达到 68.2，远超第二名 MH-OmniGen 的 54.5（+13.7 点）。
- **计数准确性**：Architect-A 变体在计数准确率上达到 90.2%，为当前最优，适用于对人数精确性要求高的场景。
- **数据依赖**：方法利用 DisCo 生成合成多人场景并结合真实参考人脸构建训练数据，不依赖真实多人图像数据集，这降低了数据获取门槛，但也意味着在真实多人交互场景的泛化性上可能存在上限。

### 3. 局限与开放问题

**已识别局限**：
1. **大规模群体控制衰减**：当人数超过 3 人时，对个体面部表情和身体姿态的细粒度控制力减弱，这在 Multi-ID vs. person count 的定量分析中已有体现。
2. **复杂交互动作不足**：在 Action-C（复杂多人姿态和交互）指标上仍有提升空间，当前姿态控制变体甚至增加了复制粘贴伪影。
3. **群体规模上限未验证**：未在 8 人以上大规模群体场景上进行验证，方法的可扩展性边界尚不明确。
4. **姿态控制与身份保真度的权衡**：引入姿态条件后，复制粘贴伪影增加，表明姿态控制与身份自然度之间存在尚未解决的张力。

**开放问题**：
1. **细粒度控制扩展**：如何将面部表情和身体姿态的细粒度控制扩展到更大规模群体（>3 人），同时保持个体可控性？
2. **复杂动作生成**：通过增强姿态条件或引入层次化场景合成策略，能否提升复杂多人交互动作的生成质量？
3. **超大规模群体生成**：探索 8 人以上群体的生成能力，需要在保持个体可控性的同时解决计算效率和空间布局复杂度问题。
4. **伪影消除**：如何进一步减少复制粘贴伪影，提高姿态控制变体的自然度？这可能需要在奖励函数设计或训练数据构建上进行更深入的研究。

**证据强度说明**：上述局限和开放问题均来自论文自身的讨论和实验分析，置信度较高。但关于 8 人以上场景的推断属于论文未覆盖的边界，需在实际应用中进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Ar2Can_An_Architect_and_an_Artist_Leveraging_a_Canvas_for_Multi_Human_Generation.pdf]]
