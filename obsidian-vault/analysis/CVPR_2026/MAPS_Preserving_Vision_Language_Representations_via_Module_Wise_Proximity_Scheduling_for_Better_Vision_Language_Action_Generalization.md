---
title: "MAPS: Preserving Vision-Language Representations via Module-Wise Proximity Scheduling for Better Vision-Language-Action Generalization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MAPS_Preserving_Vision_Language_Representations_via_Module_Wise_Proximity_Scheduling_for_Better_Vision_Language_Action_Generalization.pdf
project_link: "https://mapsvla.github.io"
code_link: "https://github.com/Stanford-ILIAD/openvla-mini"
aliases:
- MMWPS
- MAPS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 各模块参数相对于预训练初始化的偏离幅度（邻近度）及其调整速率。
primary_logic: 基于VLM组件对泛化的重要性层次，将固有的统一邻近度约束替换为从视觉到语言线性递减的层级化调度，使底层视觉层强保留预训练表征，而高层语言层灵活适应动作空间，从而在无额外开销的同时显著提升分布外泛化。
claims:
- 冻结视觉层（尤其DINOv2）可显著提升SimplerEnv和LIBERO的OOD性能，而冻结语言层则导致性能骤降至近零。
- 直接应用统一λ的鲁棒微调（RFT）在VLA上仅带来微弱提升，表明需要模块差异化约束。
- MAPS使用线性调度时，DINOv2的L2偏离最小，SigLIP居中，语言层最大，验证了层级化约束的实现。
- 线性调度（v=0.5）在LIBERO-90上取得ID 88 / OOD 4.75，优于余弦和常量调度。
---

# MAPS: Preserving Vision-Language Representations via Module-Wise Proximity Scheduling for Better Vision-Language-Action Generalization

> [!tip] 核心洞察
> 基于VLM组件对泛化的重要性层次，将固有的统一邻近度约束替换为从视觉到语言线性递减的层级化调度，使底层视觉层强保留预训练表征，而高层语言层灵活适应动作空间，从而在无额外开销的同时显著提升分布外泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | MAPS：模块化邻近度调度保持视觉-语言表征以提升VLA泛化 |
| 英文题名 | MAPS: Preserving Vision-Language Representations via Module-Wise Proximity Scheduling for Better Vision-Language-Action Generalization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19878) · [Project](https://mapsvla.github.io) · [Code](https://github.com/Stanford-ILIAD/openvla-mini) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MAPS (Module-Wise Proximity Scheduling) |
| Dataset | SimplerEnv, LIBERO, Real-world Franka |

> [!tip] 效果简介
> - SimplerEnv 上，Average OOD success rate 35.8 vs 8.9 (+26.9)。
> - LIBERO (OOD average) 上，Success rate 4.75 vs 0.0 (+4.75)。
> - Real-world Franka 上，Average OOD success rate 52.5 vs 22.5 (+30.0)。

## 概要

**核心问题**：当前视觉-语言-动作（VLA）模型在动作微调阶段普遍采用全参数更新，导致预训练视觉-语言模型（VLM）中关键的视觉几何先验和语义对齐被破坏，引发灾难性遗忘与分布外（OOD）泛化能力的严重退化。

**核心发现**：VLM内部不同模块对泛化的贡献存在显著层次差异——底层视觉编码器（如DINOv2）需要强保留，而高层语言层则可以灵活适应动作空间。冻结视觉层可大幅提升OOD性能，而冻结语言层则导致性能骤降至接近零（Table 1, Table 2）。

**方法定位**：MAPS（Module-Wise Proximity Scheduling）是一种零额外参数、零额外数据的即插即用正则化策略。它在现有基于投影的选择性微调框架基础上，将统一的邻近度约束替换为从视觉到语言线性递减的层级化调度，使底层视觉层紧贴预训练权重，高层语言层自由适应，从而在保持分布内（ID）性能的同时显著提升OOD泛化。

**主要结果**：
- **SimplerEnv**：MAPS将OOD平均成功率从8.9%提升至35.8%（+26.9%，Table 3）。
- **LIBERO**：OOD平均成功率从0.0%提升至4.75%（+4.75，Table 7）。
- **真实机器人Franka**：OOD平均成功率从22.5%提升至52.5%（+30.0%，Table 5）。
- **CALVIN长程任务**：MiniVLA-OFT平均完成长度提升0.7（Figure 5）。

MAPS的核心优势在于：无需修改模型架构、不增加训练数据或参数量，仅通过模块感知的正则化调度即可实现一致的ID保持与OOD增益，且计算效率优于双编码器等替代方案。



### 视觉-语言-动作模型的泛化困境

视觉-语言-动作（VLA）模型通过在大规模视觉-语言模型（VLM）预训练权重上进行动作微调，将语义理解与物理交互能力相融合。典型的VLA策略可形式化为 $\pi_{\theta}(a_t \mid o_t, x)$，其中观测 $o_t$ 经视觉编码器 $f_v$ 提取特征，语言指令 $x$ 经语言编码器 $f_l$ 编码，两者通过多模态融合模块 $f_m$ 生成策略嵌入 $z_t = f_m([f_v(o_t), f_l(x)])$，最终由动作头映射为具体动作。

然而，现有VLA在分布外（OOD）场景下的泛化能力严重不足。其根本瓶颈在于：**动作微调阶段的全参数更新不加区分地扭曲了预训练VLM中不同模块的表征结构，导致灾难性遗忘与泛化退化**。预训练VLM的早期视觉层（如DINOv2）编码了关键的几何与空间先验，中间层（如SigLIP）提供了视觉-语义对齐，而高层语言层则负责指令理解与推理。全参数微调将所有这些先验统一推向动作分布，破坏了预训练表征的泛化基础。

### 现有方法的局限

针对上述问题，已有工作主要沿两条路径展开：

**参数冻结策略**通过选择性冻结部分模块来保留预训练知识。然而，冻结实验揭示了VLM组件的层次化重要性：冻结视觉层（尤其是DINOv2）可显著提升SimplerEnv和LIBERO的OOD性能，而冻结语言层则导致性能骤降至接近零（见Table 1、Table 2）。这暗示简单的“冻结/不冻结”二元决策无法捕捉模块间精细的差异化保护需求。

**鲁棒微调方法**（如L2-SP）通过在损失函数中加入对预训练权重的统一L2惩罚 $\mathcal{L}_{\mathrm{L2-SP}} = \mathcal{L}(\theta_t) + \frac{\lambda_{\mathrm{reg}}}{2} \|\theta_t - \theta_0\|_2^2$ 来约束参数偏离。选择性投影衰减（SPD）进一步引入动态投影机制，当梯度-位移一致性信号 $c_t := - g_t^\top (\theta_{t-1} - \theta_0) < 0$ 时，将参数投影回预训练权重附近的L2球内。但直接应用统一 $\lambda$ 的鲁棒微调在VLA上仅带来微弱提升，因为全局约束忽略了不同模块对泛化的差异化贡献——视觉层需要强保护，语言层则需要充分适应动作空间。

### MAPS的核心动机

上述分析揭示了一个关键矛盾：**预训练VLM的组件对泛化的重要性呈层次化分布，但现有方法要么采用粗糙的冻结策略，要么施加无差别的统一约束**。MAPS的核心洞察在于：将固有的统一邻近度约束替换为从视觉到语言线性递减的层级化调度，使底层视觉层强保留预训练表征，而高层语言层灵活适应动作空间。这一设计无需额外参数或数据，可无缝集成到现有VLA训练流程中，在保持分布内（ID）性能的同时显著提升OOD泛化能力（最高达+30%）。



## 核心方法与创新机理

MAPS 的核心创新在于**将 VLA 动作微调中的统一邻近度约束替换为模块级、从视觉到语言线性递减的层级化调度**，从而在无额外参数、无数据增广的前提下，显著提升了模型的分布外泛化能力。

### 1. 问题诊断：VLA 微调中的灾难性遗忘具有模块异质性

VLA 模型通常由预训练 VLM（如 DINOv2 + SigLIP + 语言模型）与动作头组成。全参数微调（Vanilla FFT）会不加区分地更新所有模块，导致预训练阶段习得的视觉几何先验与语义对齐被破坏，引发灾难性遗忘与 OOD 性能退化。

MAPS 的关键洞察在于：**不同 VLM 组件对泛化的贡献存在层次差异**。冻结实验（Table 1, Table 2）揭示了这一层次结构：
- **冻结视觉编码器（尤其 DINOv2）**：在 SimplerEnv 上 ID 提升 7–17%，OOD 提升 7–25%；在 LIBERO 上同样显著改善 OOD 性能。
- **冻结语言层**：在 SimplerEnv 上性能骤降至近零（Avg. ID 0.0 / Avg. OOD 1.2），表明语言层需要充分适应动作空间，不能过度约束。

这一发现确立了因果调节变量：**各模块参数相对于预训练初始化的偏离幅度（邻近度）及其调整速率**。底层视觉层应强保留预训练表征，而高层语言层应灵活适应下游任务。

### 2. 方法设计：从统一约束到模块级线性调度

现有鲁棒微调方法（如 **L2-SP**、**SPD**）对所有模块施加统一的邻近度约束超参数 $\lambda$，忽略了上述模块异质性。实验表明，直接将统一 $\lambda$ 的鲁棒微调（RFT）应用于 VLA 动作微调仅带来微弱提升（Table 1, Table 2），验证了需要模块差异化约束。

MAPS 的核心改动（changed slots）如下：

| 设计维度 | 基线方法 | MAPS |
|---------|---------|------|
| **邻近度约束 $\lambda$ 的设定** | 单一全局超参数应用于所有模块 | 模块级线性衰减调度 $\lambda_k = \lambda_{\max} \left(1 - \frac{k-1}{\|\mathcal{L}\|-1}\right)$，视觉层 $\lambda$ 大，语言层 $\lambda = 0$ |
| **正则化触发策略** | 基于 $c_t < 0$ 触发，使用全局 $\lambda$ 执行投影 | 同样基于 $c_t < 0$ 触发，但投影强度乘以层特定 $\lambda_k$ |

具体而言，MAPS 沿用了 SPD 的梯度-位移一致性信号 $c_t := - g_t^\top (\theta_{t-1} - \theta_0)$ 作为触发条件：当梯度方向与当前位移方向不一致（$c_t < 0$）时，说明更新正在偏离预训练权重，需要投影回预训练初始化附近的 L2 球内。MAPS 的关键修改在于将投影强度由全局 $\lambda$ 替换为层特定 $\lambda_k$：

$$\theta_t = \widetilde{\theta}_t - \lambda_k r_t (\widetilde{\theta}_t - \theta_0)$$

其中 $\lambda_k$ 按照线性调度从视觉层向语言层递减。**DINOv2 层获得最强约束（$\lambda_k \approx \lambda_{\max}$），SigLIP 层次之，语言层约束最弱（$\lambda_k \approx 0$，等价于全微调）**。这一设计使视觉表征得以强保留，而语言层可充分适应动作空间。

Figure 3 通过微调后权重与预训练权重的 L2 距离分布验证了这一设计的效果：MAPS 产生了平滑的、模块感知的偏离衰减——DINOv2 偏离最小，SigLIP 居中，语言层最大；而统一 RFT 对所有层施加相同约束，RFT-V+FFT-L 则对 DINOv2 强约束但对 SigLIP 和语言层几乎无约束，均不如 MAPS 的层级化调度合理。

### 3. 关键优势：零额外开销与即插即用

MAPS 的创新性还体现在其极致的轻量化：
- **无额外参数**：仅修改正则化调度，不引入辅助网络或额外模块。
- **无数据增广**：不依赖额外预训练数据或任务特定损失修改。
- **架构无关**：可适配任何视觉编码器、语言模型或动作分词策略，已验证支持 MiniVLA-OFT、OpenVLA-OFT、MiniVLA-VQ 等多种 backbone。

消融实验（Table 6）进一步验证了线性调度的优越性：在 $\lambda_{\max}=0.5$ 时，线性调度在 LIBERO-90 上取得 ID 88 / OOD 4.75，优于余弦调度和常量调度。与双编码器方法（Dual-Encoder）和权重插值相比，MAPS 在无额外参数的情况下获得了最高的 ID 和 OOD 性能（Table 7）。



MAPS 的整体设计围绕一个核心矛盾展开：VLA 模型在动作微调阶段，需要同时保留预训练 VLM 的泛化表征，又必须适应特定的机器人操控任务。全参数微调导致各模块权重无差别地偏离预训练初始化，造成灾难性遗忘——视觉几何先验和语义对齐被破坏，分布外（OOD）泛化能力急剧退化。MAPS 的解决思路是将这一矛盾转化为一个可控的调度问题：**让不同模块以不同的“邻近度”贴近其预训练权重**。

### 架构组成与信息流

MAPS 本身不修改 VLA 的底层架构，而是作为一种**即插即用的正则化策略**叠加在现有 VLA 的训练流程之上。典型的 VLA 模型由以下模块串联构成（Figure 1 蓝色虚线框内）：

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/001_Figure_1.jpg]]
*Figure 1: Module-Wise Proximity Scheduling (MAPS). MAPS is applied on pretrained VLM components during the action finetuning stage. MAPS (blue dash line) enforces strong preservation on early vision layers while progressively relaxing constraints toward higherlevel language layers. In contrast, vanilla finetuning (green dash line) distorts the VLM representation completely away from its pretrained weights (black solid line), and uniform SPD (orange dash/dot line) applies the same constraint everywhere*

1. **早期视觉编码器（DINOv2）**：提取图像中的几何与空间先验，是 VLM 泛化能力的根基。
2. **视觉-语言对齐模块（SigLIP）**：将视觉特征映射到与语言模型兼容的语义空间，提供跨模态理解。
3. **多模态融合桥接层（Bridge / Multimodal Transformer）**：融合视觉与语言表征，生成统一的策略嵌入。
4. **语言模型（如 Qwen2.5 / LLaMA）**：处理语言指令，将多模态信息转化为动作相关的上下文表征。
5. **动作头（Action Head）**：将最终的策略嵌入解码为具体的机器人动作。

整个前向过程可形式化为：

$$z_t = f_m([f_v(o_t), f_l(x)])$$

$$\pi_{\theta}(a_t \mid o_t, x) = \text{ActionHead}(z_t)$$

其中 $o_t$ 为当前观测，$x$ 为语言指令，$f_v$ 和 $f_l$ 分别代表视觉和语言编码路径，$f_m$ 为多模态融合。

### 核心调度机制

MAPS 的核心操作发生在反向传播与参数更新阶段。传统微调使用统一的正则化强度 $\lambda$ 约束所有参数（如 L2-SP 或 SPD），而 MAPS 将其替换为**模块级的线性衰减调度**：

$$\lambda_k = \lambda_{\max} \left(1 - \frac{k-1}{|\mathcal{L}|-1}\right)$$

其中 $k$ 为模块在 VLM 层级中的索引（从视觉底层到语言高层递增），$|\mathcal{L}|$ 为总模块数。这意味着：
- **DINOv2 层**（$k$ 小）获得最大的 $\lambda_k$，被强制保持在预训练权重附近；
- **SigLIP 层**获得中等约束；
- **语言层**（$k$ 大）的 $\lambda_k$ 趋近于 0，允许充分适应动作空间。

这一设计的因果依据来自冻结实验（Section 4.2，Table 1、Table 2）：冻结视觉编码器可显著提升 OOD 性能（SimplerEnv 上 OOD 从 8.9 提升至 15.0），而冻结语言层则导致性能骤降至接近零。这表明视觉表征是泛化的瓶颈，语言层则需要灵活性来适配任务。

### 参数更新流程

MAPS 在每次梯度更新时执行以下步骤：

1. **计算无约束更新**：$\tilde{\theta}_t = \theta_{t-1} - \eta g_t$，其中 $g_t$ 为当前梯度。
2. **计算梯度-位移一致性信号**：
   $$c_t := - g_t^\top (\theta_{t-1} - \theta_0)$$
   当 $c_t < 0$ 时，表示当前梯度方向与参数偏离预训练权重的方向一致，需要触发投影。
3. **模块级投影**：对于每个模块 $k$，若 $c_t < 0$，则按层特定强度将参数拉回：
   $$\theta_t = \widetilde{\theta}_t - \lambda_k r_t (\widetilde{\theta}_t - \theta_0)$$
   其中 $r_t$ 为投影半径相关的缩放因子。若 $c_t \geq 0$，则不做投影，直接接受无约束更新。

Figure 3 的权重偏离分布验证了这一机制的有效性：MAPS 微调后的 DINOv2 层与预训练权重的 L2 距离最小，SigLIP 居中，语言层最大，形成了平滑的模块感知衰减。相比之下，统一 SPD 对所有层施加相同约束，无法实现这种差异化保护。

### 与基线的关键区别

- **Vanilla 全参数微调**：无任何邻近度约束，所有模块可自由偏离预训练权重，导致视觉表征被破坏（Figure 1 绿色虚线）。
- **L2-SP / 统一 SPD**：使用单一全局 $\lambda$，对所有模块一视同仁，无法体现 VLM 组件的层次化重要性（Figure 1 橙色点划线）。
- **MAPS**：将 $\lambda$ 从一个全局超参数扩展为**模块索引的线性函数**，在无额外参数、无额外数据的前提下，实现了从视觉到语言的递减保护梯度。



### 问题形式化：VLA 动作微调中的灾难性遗忘

VLA 模型将视觉观测 $o_t$ 与语言指令 $x$ 映射为动作 $a_t$，其策略可形式化为：

$$\pi_{\theta}(a_t \mid o_t, x)$$

其中多模态融合得到的策略嵌入为：

$$z_t = f_m([f_v(o_t), f_l(x)])$$

在动作微调阶段，全参数更新（Vanilla full fine-tuning）会使 $\theta$ 偏离预训练 VLM 的初始化 $\theta_0$，导致视觉几何先验和语义对齐被破坏，引发灾难性遗忘与 OOD 泛化退化。MAPS 的核心目标是在微调中**差异化地约束各模块参数偏离 $\theta_0$ 的幅度**，从而保留关键的预训练表征。

### 基础约束范式：L2-SP 与 TPGM 投影

MAPS 建立在两类邻近度约束方法之上：

**L2-SP（L2 惩罚）** 在标准微调损失上直接加入对预训练权重距离的二次惩罚：

$$\mathcal{L}_{\mathrm{L2-SP}} = \mathcal{L}(\theta_t) + \frac{\lambda_{\mathrm{reg}}}{2} \|\theta_t - \theta_0\|_2^2$$

其中 $\lambda_{\mathrm{reg}}$ 为全局正则化强度。然而，该方法的约束是**静态且全局统一**的，无法区分不同模块对预训练表征的依赖程度。

**TPGM（Trust Region Gradient Projection Method）** 将问题转化为约束优化：

$$\min \mathcal{L}(x,y;\theta_t), \quad \mathrm{s.t.} \quad \|\theta_t - \theta_0\|_2 \leq \gamma$$

其投影操作为：

$$\theta_t = \theta_0 + \frac{1}{\max\left(1, \frac{\|\tilde{\theta}_t - \theta_0\|_2}{\gamma}\right)} (\tilde{\theta}_t - \theta_0)$$

当无约束更新 $\tilde{\theta}_t$ 超出半径 $\gamma$ 的 L2 球时，将其投影回球内。SPD（Selective Projection Decay）在此基础上引入**触发机制**：仅当梯度方向与当前位移不一致时执行投影，信号量 $c_t$ 定义为：

$$c_t := - g_t^\top (\theta_{t-1} - \theta_0)$$

当 $c_t < 0$ 时，表明更新方向背离预训练权重，触发投影回拉。

### MAPS 关键创新：模块级邻近度调度

上述方法的共同瓶颈在于**使用单一全局超参数 $\lambda$ 或 $\gamma$ 约束所有模块**，忽略了 VLM 各组件的层次化重要性。冻结实验（Table 1, Table 2）已揭示：冻结视觉层（尤其 DINOv2）显著提升 OOD 性能，而冻结语言层则导致性能骤降至近零——说明视觉层需要强保留，语言层需要灵活适应。

MAPS 将统一的邻近度约束替换为**从视觉到语言线性递减的层级化调度**。对于 VLM 的 $|\mathcal{L}|$ 个模块，第 $k$ 层的邻近度权重为：

$$\lambda_k = \lambda_{\max} \left(1 - \frac{k-1}{|\mathcal{L}|-1}\right)$$

其中 $\lambda_{\max}$ 为最大约束强度（消融实验表明 $\lambda_{\max}=0.5$ 时最优），$k=1$ 对应最早视觉层（DINOv2），$k=|\mathcal{L}|$ 对应最后语言层。该调度使 DINOv2 受到最强约束（$\lambda_1 = \lambda_{\max}$），SigLIP 居中，语言层约束递减至 $\lambda_{|\mathcal{L}|}=0$。

当 $c_t < 0$ 触发投影时，MAPS 的逐层参数更新为：

$$\theta_t = \widetilde{\theta}_t - \lambda_k r_t (\widetilde{\theta}_t - \theta_0)$$

其中 $r_t$ 为投影比率，$\lambda_k$ 为层特定强度。与统一 SPD 相比，MAPS 仅将全局 $\lambda$ 替换为模块级 $\lambda_k$，**不引入额外参数、数据或架构修改**。

### 调度设计的经验支撑

线性调度的合理性由以下证据链支撑：

1. **冻结实验**（Table 1, Table 2）：冻结 DINOv2+SigLIP 在 SimplerEnv 上使 OOD 从 8.9 提升至 15.0，而冻结语言层使性能归零，验证了“视觉强保留、语言灵活适应”的层次化需求。

2. **权重偏离可视化**（Figure 3）：MAPS 产生平滑的模块感知偏离衰减——DINOv2 的 L2 偏离最小，SigLIP 居中，语言层最大；而统一 RFT 对所有层施加同等约束，RFT-V+FFT-L 则对 SigLIP 约束不足，均无法同时兼顾 ID 保持与 OOD 泛化。

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/005_Figure_3.jpg]]
*Figure 3: We calculate the*

3. **调度器消融**（Table 6）：线性调度（$v=0.5$）在 LIBERO-90 上取得 ID 88 / OOD 4.75，优于余弦调度和常量调度，验证了线性递减形式的有效性。

### 方法边界与未决问题

MAPS 的线性调度虽简洁有效，但**并非最优调度形式的理论保证**。当前 $\lambda_{\max}$ 需针对不同 backbone 单独调节，自动化程度有限。更复杂的动态调度函数（如基于梯度信号的逐层自适应）仍是开放方向。此外，MAPS 在饱和任务（如 Laptop ID）上提升不显著，表明当任务过简单时，强约束可能限制必要的适应能力。



## 实验与关键发现

### 瓶颈诊断：VLA微调中的灾难性遗忘

MAPS 的设计动机源于一个核心发现：VLA 模型在动作微调阶段，若不加区分地更新所有参数，会严重破坏预训练 VLM 中蕴含的视觉几何先验与语义对齐，导致灾难性遗忘和泛化退化。为量化这一现象，作者对 VLA 架构进行组件级分解——DINOv2（早期视觉编码器）、SigLIP（视觉-语言对齐模块）、早期语言层和后期语言层——并系统性地评估了不同冻结配置在 SimplerEnv 和 LIBERO 上的表现。

**关键证据**（Table 1, Table 2）：
- **冻结视觉编码器显著提升 OOD 性能**：在 SimplerEnv 上，冻结 DINOv2+SigLIP 使 ID 成功率从全参数微调的 13.5 提升至 20.0，OOD 从 8.9 提升至 15.0（+7–17% ID，+7–25% OOD）。
- **冻结语言层导致性能骤降**：冻结早期和后期语言层使 SimplerEnv 的 ID 和 OOD 成功率均降至接近零（ID 0.0 / OOD 1.2），表明语言层对动作空间的适应至关重要。
- **直接应用统一 λ 的鲁棒微调（RFT）效果有限**：在 SimplerEnv 和 LIBERO 上，统一 RFT 仅带来微弱提升，说明 VLA 不同模块需要差异化约束。

这一冻结实验揭示了 VLM 组件在泛化中的**重要性层次**：视觉层（尤其 DINOv2）的预训练表征对 OOD 泛化起决定性作用，应强保留；语言层则需要灵活适应动作空间。MAPS 正是基于这一发现，将统一的邻近度约束替换为从视觉到语言线性递减的层级化调度。

### 主实验结果

MAPS 作为轻量级即插即用方法，不引入额外参数、辅助网络或数据，可无缝集成到现有 VLA 架构中。其在三个关键基准上均展现出显著的 OOD 泛化增益，同时保持或提升 ID 性能。

**SimplerEnv**（Table 3）：
- MiniVLA-OFT + MAPS 在 OOD 平均成功率上从基线的 8.9 提升至 35.8（**+26.9**），ID 性能持平（13.5 vs 14.3）。
- OpenVLA-OFT + MAPS 在 OOD 上提升 8.4 个百分点，ID 性能同样保持稳定。
- 这一结果表明 MAPS 对不同规模 backbone 的 VLA 均有效。

**LIBERO**（Table 4, Table 7）：
- MiniVLA-VQ + MAPS 在 LIBERO-90 上取得 ID 88 / OOD 4.75，而基线 MiniVLA-VQ 的 OOD 为 0.0（**+4.75**）。
- 与双编码器（Dual-Encoder）和权重插值等需要额外参数的方法相比，MAPS 在无额外开销下获得最高 ID 和 OOD 性能。

**真实世界 Franka 机器人**（Table 5, Figure 6）：
- MAPS 在 Franka 平台上将 OOD 平均成功率从 22.5 提升至 52.5（**+30.0**），ID 成功率从 42.5 提升至 55.0。
- 细粒度分析显示，MAPS 在 Blocks 和 Cups 任务的 Easy/Hard 子任务上均一致优于基线，且平均尝试次数更少，表明策略更稳健。

**CALVIN 长程任务**（Figure 5）：
- MAPS 在所有动作跨度上均提升成功率（MiniVLA-OFT +25%，OpenVLA-OFT +3%），平均完成长度分别增加 0.7 和 0.1，验证了层级化约束在长序列任务中的优势。

### 消融实验与机制验证

**调度器对比**（Table 6）：
线性调度（MAPS 默认）在 LIBERO-90 上取得 ID 88 / OOD 4.75，优于余弦调度和常量调度。当 λ_max=0.5 时达到最佳 OOD 性能，λ_max 过小则约束不足、过大则过度限制语言层适应。

**权重偏离程度验证**（Figure 3）：
- MAPS 产生的模块级 L2 偏离呈现平滑递减：DINOv2 偏离最小（强保留），SigLIP 居中，语言层最大（灵活适应）。
- 仅对视觉栈应用 RFT（RFT-V+FFT-L）虽能强约束 DINOv2，但 SigLIP 和语言层几乎不受约束，偏离模式不连续。
- 统一 RFT 对所有层施加相同约束，无法体现模块间的重要性差异。

这一可视化直接验证了 MAPS 的层级化约束机制的有效实现。

### 失败模式与局限性

1. **饱和任务提升有限**：在过于简单的 ID 任务（如某些 Laptop 场景）上，MAPS 的性能提升不显著，可能因任务过简单导致模型易过拟合，邻近度约束的边际收益降低。
2. **λ_max 需手动调节**：首次部署时需为不同 backbone 单独调节 λ_max，自动化程度有限。虽然作者提供了各模型-基准的推荐配置（Table 8），但最优值的搜索仍需人工介入。
3. **调度函数未穷尽探索**：当前线性调度虽优于常量和余弦，但更复杂的动态调度（如基于梯度的自适应调度）可能进一步提升性能，尚待探究。
4. **跨形态泛化未验证**：实验集中在视觉-语言-动作的 VLA 架构，MAPS 的层级化调度思想能否推广到其他 VLM 架构或更多模态（如触觉、力觉）的机器人任务，仍需进一步验证。

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/016_Table_8.jpg]]
*Table 8: Configurations for Each Model and Benchmark*

### 补充图表

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/003_Table_1.jpg]]
*Table 1: Comparison of freezing or robust fine-tuning (RFT) different parts of VLA on SimplerEnv’s ID and OOD tasks (details in Sec. 5.1). Early L and Last L denote early and the last language layers. and \ represent freeze and full fine-tune*

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/004_Table_2.jpg]]
*Table 2: Comparison of freezing different parts of VLA on LIBERO. Early L and Last L denote early and the last language layers. and \ represent freeze and full fine-tune*

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/006_Table_3.jpg]]
*Table 3: SimplerEnv Results. ID includes 4 tasks following SimplerEnv-Bridge setup. OOD evaluation suites include Visual, Novel Object, and Novel Category. ∗ model checkpoints borrowed from original papers. † models pretrained from scratch on SimplerEnv*

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/009_Table_4.jpg]]
*Table 4: LIBERO Results. ∗ models borrowed from [17]. † models pretrained from scratch on LIBERO-90. ‡ models finetuned on LIBERO-90*

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/010_Table_5.jpg]]
*Table 5: Franka Results*

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/015_Table_7.jpg]]
*Table 7: Dual Encoders vs. MAPS on LIBERO using MiniVLA-VQ*

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/008_Figure_5.jpg]]
*Figure 5: CALVIN Results. MAPS improves success rates across all action horizons (25% for MiniVLA-OFT and 3% for OpenVLA-OFT) and average length (+0.7 for MiniVLA-OFT and +0.1 for OpenVLA-OFT)*

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/011_Figure_6.jpg]]
*Figure 6: Franka Detailed Results. Top Left: Success rates for the Blocks ID Easy/Hard tasks. Top Right: Success rates for the Blocks OOD Easy/Hard tasks. Bottom Left: Average number of tries per success across all Franka tasks. Bottom Right: Success rates for the Cups ID/OOD tasks*

![[assets/figures/papers/paper_list_l2402_https_arxiv_org_abs_2511_19878/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative comparison of freezing configurations for LIBERO-90 task ”put the bowl on the plate” (left to right: full finetuning (FFT), freeze VLM, freeze language, freeze vision). FFT fails most, targetting the cabinet instead of the bowl. Freezing VLM/language/vision preserves 2D localization of the bowl but impairs depth reasoning. When vision is frozen, the policy can grasp the bowl but fails to accurately place it on the plate*



## 定位与知识库关联

### 1. 核心问题定位：VLA 微调中的灾难性遗忘

视觉-语言-动作（VLA）模型在机器人操作任务上的标准范式是：先在大规模图文数据上预训练一个视觉-语言模型（VLM），再在机器人动作数据上进行微调，使模型输出动作指令。然而，这一微调阶段面临一个关键瓶颈：**全参数更新会破坏预训练 VLM 中已建立的视觉几何先验和语义对齐**，导致灾难性遗忘——模型在训练分布外的场景（OOD）中泛化能力急剧退化。

MAPS 的因果调节变量被识别为：**各模块参数相对于预训练初始化的偏离幅度（邻近度）及其调整速率**。核心洞察在于：VLM 的不同组件对泛化的贡献存在天然的层次结构——底层视觉层（如 DINOv2）承载了关键的几何与空间先验，需要强保护；高层语言层则更灵活，可以适应动作空间的分布偏移。基于此，MAPS 提出将统一的邻近度约束替换为从视觉到语言线性递减的层级化调度，使底层视觉层强保留预训练表征，而高层语言层灵活适应动作空间，从而在无额外参数开销的同时显著提升 OOD 泛化。

### 2. 方法谱系：从冻结研究到邻近度调度

MAPS 的方法设计建立在对现有 VLA 微调策略的系统性诊断之上，其演进路径可归纳为三个递进阶段。

#### 2.1 冻结研究：揭示模块重要性层次

MAPS 首先通过系统性的冻结实验，量化了 VLA 各组件对 ID 和 OOD 性能的差异化贡献。实验将 VLA 架构分解为四个组件——DINOv2、SigLIP、早期语言层、晚期语言层——并在 SimplerEnv 和 LIBERO 两个基准上评估不同冻结配置。

**关键发现**（Table 1, Table 2）：冻结视觉编码器（尤其是 DINOv2）可显著提升 OOD 性能，在 SimplerEnv 上冻结 DINOv2+SigLIP 使 OOD 平均成功率从全微调的 8.9 提升至 15.0，ID 从 13.5 提升至 20.0；而冻结语言层则导致性能骤降至接近零（0.0–1.2）。这一非对称效应确立了**视觉层对泛化的重要性远高于语言层**的层次结构，为后续的层级化约束设计提供了经验基础。

值得注意的是，定性分析（Figure 2）进一步揭示了冻结视觉与冻结语言的失败模式差异：全微调在“将碗放到盘子上”任务中完全失败，目标错误地指向柜子；冻结 VLM 或语言层保留了碗的 2D 定位能力，但深度推理受损；仅冻结视觉时，策略能抓取碗但无法准确放置。这表明视觉先验的保留是泛化的必要条件，但并非充分条件——语言层的适度适应同样不可或缺。

#### 2.2 统一正则化的局限：L2-SP 与 SPD 的不足

在冻结研究揭示模块重要性差异后，MAPS 进一步考察了现有的鲁棒微调方法。L2-SP 通过在微调损失中加入对预训练权重的 L2 惩罚项 $\mathcal{L}_{\mathrm{L2-SP}} = \mathcal{L}(\theta_t) + \frac{\lambda_{\mathrm{reg}}}{2} \|\theta_t - \theta_0\|_2^2$ 来约束参数偏离，但其使用**单一全局超参数** $\lambda_{\mathrm{reg}}$ 对所有模块施加相同的约束强度。类似地，基于投影的 SPD 方法通过梯度-位移相关性信号 $c_t := - g_t^\top (\theta_{t-1} - \theta_0)$ 触发投影，将参数拉回预训练权重附近的 L2 球内，但其投影强度同样由全局 $\lambda$ 控制。

**实验证据**（Table 1, Table 2）：直接将统一 $\lambda$ 的鲁棒微调（RFT）应用于 VLA 动作微调，在 SimplerEnv 和 LIBERO 上仅带来微弱提升。这一结果表明，**统一约束无法捕捉 VLA 不同模块对保护强度的差异化需求**——视觉层需要强约束以防止几何先验被破坏，而语言层需要弱约束以灵活适应动作空间。

#### 2.3 MAPS 的创新：模块级邻近度线性调度

MAPS 的核心创新在于将 SPD 的全局邻近度超参数 $\lambda$ 替换为**层级的、架构感知的线性调度**：

$$\lambda_k = \lambda_{\max} \left(1 - \frac{k-1}{|\mathcal{L}|-1}\right)$$

其中 $k$ 为模块索引（从视觉层到语言层递增），$|\mathcal{L}|$ 为模块总数，$\lambda_{\max}$ 为最大邻近度权重。该调度使 DINOv2 层获得最强的保护（$\lambda_k \approx \lambda_{\max}$），SigLIP 层居中，语言层则完全不受约束（$\lambda_k = 0$）。当梯度-位移相关性 $c_t < 0$ 时，参数更新按层特定强度投影回预训练权重：

$$\theta_t = \widetilde{\theta}_t - \lambda_k r_t (\widetilde{\theta}_t - \theta_0)$$

Figure 3 的权重偏离分析验证了该调度的实际效果：MAPS 产生平滑的、模块感知的偏离衰减——DINOv2 的 L2 偏离最小，SigLIP 居中，语言层最大。相比之下，仅在视觉栈上应用 RFT（RFT-V+FFT-L）虽能强约束 DINOv2，但 SigLIP 和语言层几乎不受约束；统一 $\lambda$ 的 RFT 则对所有层施加同等约束。

### 3. 与基线方法的关系

#### 3.1 与冻结策略的关系

MAPS 可视为冻结策略的**软推广**。冻结策略通过硬性阻止参数更新来保护预训练表征，但丧失了模块间的适应性；MAPS 则通过邻近度权重实现**连续的保护强度**——视觉层接近冻结（$\lambda_k$ 大），语言层完全自由（$\lambda_k = 0$），中间层则获得适度的约束。这种软约束既保留了冻结策略对视觉先验的保护效果，又避免了硬冻结对语言层适应能力的限制。

#### 3.2 与 L2-SP / SPD 的关系

MAPS 直接继承自 SPD 的投影机制和触发策略（基于 $c_t < 0$），但将**全局 $\lambda$ 替换为层特定调度**。这一改动看似简单，却从根本上改变了约束的语义：从“所有模块同等重要”转变为“视觉层需要强保护，语言层可以自由适应”。消融实验（Table 6）证实，线性调度（$\lambda_{\max}=0.5$）在 LIBERO-90 上取得 ID 88 / OOD 4.75，显著优于余弦调度和常量调度，验证了层级化约束的优越性。

#### 3.3 与双编码器方法的关系

双编码器方法通过引入额外的视觉编码器来增强表征保留，但增加了参数量和计算开销。Table 7 的对比显示，MAPS 在无额外参数的情况下，在 LIBERO 上使用 MiniVLA-VQ 取得了最高的 ID 和 OOD 性能，表明**层级化约束比增加模型容量更有效地保留了预训练表征**。

### 4. 适用边界与局限

MAPS 的适用边界和局限性需要在以下维度审慎评估：

**架构兼容性**：MAPS 的设计假设 VLA 的视觉-语言层次结构与泛化重要性呈线性递减关系。这一假设在 DINOv2+SigLIP 视觉塔和 LLaMA/Qwen2.5 语言模型的组合上得到了验证，但**尚未在更复杂的 VLM 架构（如多视觉塔、多模态融合层）上进行测试**。对于视觉-语言交互更紧密的架构（如交叉注意力融合），简单的线性调度可能无法准确反映模块重要性。

**超参数敏感性**：MAPS 引入了 $\lambda_{\max}$ 作为唯一的新超参数，但其最优值依赖于具体的 backbone 组合。论文在 MiniVLA 上使用 $\lambda_{\max}=0.5$，在 OpenVLA 上使用 $\lambda_{\max}=0.3$，表明**首次部署时需要针对不同 backbone 单独调节**，自动化程度有限。此外，线性调度本身可能并非最优——消融实验仅比较了线性、余弦和常量三种调度，更复杂的动态调度（如基于梯度的自适应调度）尚未探索。

**任务饱和效应**：MAPS 的性能提升在饱和任务（如 Laptop ID）上不显著。这可能是因为过简单的任务本身容易过拟合，层级化约束无法提供额外的正则化收益。在更困难的 OOD 场景中，MAPS 的优势才得以充分体现。

**规模与多样性验证不足**：现有实验在 SimplerEnv、LIBERO、CALVIN 和 Franka 真实机器人上进行，但**未在更大规模预训练数据集或更复杂的跨形态机器人任务上验证**。在更极端的 OOD 环境（如剧烈光照变化、背景替换、全新物体类别）下，MAPS 的鲁棒性上限尚不明确。

### 5. 开放问题

基于上述分析，MAPS 打开了以下值得进一步探索的方向：

1. **层级化调度的泛化性**：MAPS 的线性递减调度是否可推广到其他 VLM 架构（如不同视觉塔组合、多模态融合策略）？模块重要性的层次结构是否具有跨架构的普适性，还是需要针对每种架构重新诊断？

2. **调度函数的优化空间**：线性调度是当前的最简形式。是否可以通过元学习或基于梯度的自适应机制，在训练过程中动态调整各层的 $\lambda_k$？更复杂的调度函数（如指数衰减、分段常数）是否能在特定任务上取得更好效果？

3. **与数据层面策略的协同**：邻近度调度能否与数据增强、课程学习等策略结合，进一步缓解过拟合？例如，在训练初期使用强约束保护视觉先验，随着训练推进逐步放宽约束，可能与课程学习形成互补。

4. **反向指导预训练**：MAPS 揭示的模块重要性层次（DINOv2 > SigLIP > 语言层）是否可以反向用于指导 VLA 预训练过程？例如，在预训练阶段就对视觉层施加更强的表征学习目标，可能使下游微调更加鲁棒。

5. **更广泛的 OOD 鲁棒性边界**：在更极端的分布偏移（如仿真到真实的大幅域间隙、全新机器人形态）下，MAPS 的层级化约束是否仍然有效？视觉先验的保留是否存在一个“保护过度”的临界点，超过该点反而会限制模型对新视觉特征的适应？



## 原文 PDF

![[paperPDFs/CVPR_2026/MAPS_Preserving_Vision_Language_Representations_via_Module_Wise_Proximity_Scheduling_for_Better_Vision_Language_Action_Generalization.pdf]]
