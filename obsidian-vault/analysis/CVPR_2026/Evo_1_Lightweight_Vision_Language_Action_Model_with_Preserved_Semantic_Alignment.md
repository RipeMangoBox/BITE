---
title: "Evo-1: Lightweight Vision-Language-Action Model with Preserved Semantic Alignment"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Evo_1_Lightweight_Vision_Language_Action_Model_with_Preserved_Semantic_Alignment.pdf
project_link: null
code_link: "https://github.com/MINT-SJTU/Evo-1"
aliases:
- E1
- Evo-1
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用轻量级原生多模态VLM（InternVL3-1B）作为骨干，并通过两阶段训练策略（先冻结VLM仅训练动作模块，再全局微调）有效保留VLM的语义空间，从而在不使用任何机器人数据预训练的条件下实现高性能。
primary_logic: 通过轻量级原生多模态视觉语言模型和两阶段训练保留VLM的内在语义对齐，可以在不依赖大规模机器人预训练数据的情况下，大幅降低计算开销，并达到甚至超越大型模型的操控性能。
claims:
- Evo-1在Meta-World基准上取得80.6%平均成功率，超过先前最佳模型SmolVLA（68.2%）12.4个百分点，且参数仅0.77B。
- Evo-1在RoboTwin双机械臂基准上达到37.8%成功率，超过先前最佳π0（30.9%）6.9个百分点。
- 在四个真实世界操控任务中总成功率达78%，同时推理频率16.4 Hz、GPU内存占用仅2.3 GB（RTX 4090d），在效率与性能之间达到最佳平衡。
- 两阶段训练范式在Meta-World所有难度级别上均优于单阶段联合训练，且保留的语义注意力图（Figure 7）表明语义空间未被破坏。
---

# Evo-1: Lightweight Vision-Language-Action Model with Preserved Semantic Alignment

> [!tip] 核心洞察
> 通过轻量级原生多模态视觉语言模型和两阶段训练保留VLM的内在语义对齐，可以在不依赖大规模机器人预训练数据的情况下，大幅降低计算开销，并达到甚至超越大型模型的操控性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | Evo-1：具有保留语义对齐的轻量级视觉-语言-动作模型 |
| 英文题名 | Evo-1: Lightweight Vision-Language-Action Model with Preserved Semantic Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.04555) · [Code](https://github.com/MINT-SJTU/Evo-1) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Evo-1 |
| Dataset | Meta-World, LIBERO, RoboTwin, Real-World Tasks |

> [!tip] 效果简介
> - Meta-World 上，Average Success Rate (%) 80.6 vs 68.2 (SmolVLA) (+12.4)。
> - LIBERO 上，Average Success Rate (%) 94.8 vs 94.2 (π0) (+0.6)。
> - RoboTwin 上，Average Success Rate (%) 37.8 vs 30.9 (π0) (+6.9)。

## 概要

**问题瓶颈**：当前视觉-语言-动作（VLA）模型参数规模普遍在数十亿级别，推理计算开销高昂，难以在消费级GPU上实现实时部署。更关键的是，常规端到端训练会严重破坏视觉-语言骨干网络原有的预训练语义表征，导致模型过拟合且泛化能力显著下降。此外，现有高性能VLA模型通常依赖大规模机器人数据预训练，数据收集成本极高。

**核心方法**：Evo-1采用轻量级原生多模态视觉语言模型InternVL3-1B（0.5B语言解码器 + 0.3B视觉编码器）作为感知骨干，并引入两阶段训练范式——先冻结VLM仅训练动作模块，再全局微调——有效保留VLM的内在语义对齐。动作生成端采用交叉调制扩散Transformer（Cross-modulated DiT），通过流匹配范式产生连续动作序列。

**决定性证据**：
- 在Meta-World基准上取得80.6%平均成功率，超过先前最佳模型SmolVLA（68.2%）12.4个百分点，参数仅0.77B（Table 1）。
- 在RoboTwin双机械臂基准上达到37.8%成功率，超越大型模型π0（3.5B）6.9个百分点（Table 1）。
- 四个真实世界操控任务总成功率达78%，同时推理频率16.4 Hz、GPU内存占用仅2.3 GB（RTX 4090d），在效率与性能之间达到最佳平衡（Table 2）。
- 两阶段训练在Meta-World所有难度级别上均优于单阶段联合训练，且保留的语义注意力图证实语义空间未被破坏（Figure 7, Figure 8(b)）。

**方法定位**：Evo-1属于轻量级模块化VLA架构，其核心贡献在于证明了通过保留预训练语义对齐，可以在完全不使用机器人预训练数据的前提下，以极小的模型体量达到甚至超越大型模型的操控性能。



### 视觉-语言-动作模型的规模化困境

机器人操控领域正经历从传统模仿学习向视觉-语言-动作（VLA）模型的范式转移。VLA模型将视觉感知、语言理解与动作生成统一于单一神经网络，使机器人能够根据自然语言指令和视觉观测直接输出连续动作序列。然而，当前领先的VLA模型普遍面临**参数规模与部署可行性之间的尖锐矛盾**。

以**OpenVLA**（7B参数）、**π0**（3.5B参数）为代表的大型VLA模型虽然展现出强大的任务泛化能力，但其推理过程需要数十GB的GPU内存和秒级的推理延迟，难以在消费级GPU上实现实时闭环控制。即便是轻量化的**SmolVLA**（2.25B参数），在RTX 4090d上的推理频率仍难以满足高速操控任务的需求。这一瓶颈的根源在于：现有VLA模型大多采用**大规模视觉语言模型（VLM）作为骨干**，而这些VLM本身即为数十亿参数的语言模型，其计算开销天然限制了VLA的实时性。

### 语义退化：端到端训练的隐性代价

更为隐蔽的问题在于**预训练语义表征的破坏**。VLM骨干通常在大规模图文数据上预训练，其内部表征蕴含丰富的语义对齐信息——例如，视觉注意力图能够准确聚焦于与语言指令相关的物体区域。然而，当VLA模型采用端到端联合训练时，动作监督信号会反向传播至整个VLM骨干，导致其注意力模式逐渐偏离预训练时的语义结构。

Figure 2 的对比直观呈现了这一现象：**OpenVLA**（Prismatic-7B骨干）经过端到端操控训练后，其视觉-语言注意力图出现明显的空间弥散和语义失焦；而**Evo-1**（InternVL3-1B骨干）通过两阶段训练策略，保留了清晰且语义一致的注意力分布。这种语义退化直接损害模型的泛化能力——当机器人面对未见过的物体、背景或目标位置时，语义表征的混乱会导致动作预测失败。

### 机器人预训练的数据高墙

现有VLA模型的另一结构性依赖是**大规模机器人数据预训练**。**OpenVLA**在Open X-Embodiment数据集上预训练，**π0**依赖海量多任务机器人轨迹，**GR00T N1**同样需要机器人领域的大规模预训练语料。这种预训练范式带来了双重成本：一方面，收集涵盖多种机器人形态、场景和任务的预训练数据需要极高的时间和经济投入；另一方面，预训练数据与下游任务的分布偏移可能导致负迁移，反而降低特定任务上的性能。

### Evo-1的核心动机

上述三个困境——**计算开销过高、语义表征退化、机器人预训练数据依赖**——共同构成了当前VLA研究的核心瓶颈。Evo-1的设计动机正是从这三个维度同时切入：

1. **轻量级原生多模态VLM**：采用InternVL3-1B（视觉编码器300M + 语言解码器500M），总参数量仅0.77B，从根本上降低计算开销。
2. **两阶段训练范式**：第一阶段冻结VLM仅训练动作模块，第二阶段全局微调，确保VLM的语义空间不被破坏。
3. **零机器人预训练**：完全放弃机器人领域预训练，仅依赖VLM的通用视觉-语言理解能力，通过任务域内的少量演示数据（每任务50-100条）实现高效适应。

这一设计哲学的核心洞察在于：**通过轻量级原生多模态VLM和语义保持训练策略，可以在不依赖大规模机器人预训练数据的前提下，大幅降低计算开销，并达到甚至超越大型模型的操控性能**。



## 核心方法与创新机理

Evo-1的核心创新围绕一个中心命题展开：**轻量级VLA模型能否在不依赖大规模机器人预训练数据的前提下，达到甚至超越大型模型的操控性能？** 回答这一命题的关键，在于同时解决“计算效率”与“语义保持”两个相互制约的瓶颈。Evo-1通过三个紧密耦合的设计变更（changed slots）和一种新的训练范式，构建了从感知到动作的高效通路。

### 1. 轻量级原生多模态VLM骨干：以语义对齐换取参数效率

现有VLA模型普遍采用大型视觉语言模型作为骨干，例如OpenVLA使用**Prismatic-7B**（7B参数），π0使用**3.5B**参数模型。这些大型VLM虽然在通用视觉语言理解上表现强大，但将其直接用于机器人操控面临两个根本性问题：

- **推理开销巨大**：数十亿参数的模型难以在消费级GPU上实现实时推理，限制了实际部署。
- **语义表征脆弱**：端到端微调会破坏预训练的视觉-语言语义对齐，导致过拟合和泛化能力下降。

Evo-1的应对策略是采用**InternVL3-1B**作为视觉语言骨干——这是一个原生多模态VLM，由**InternViT-300M**视觉编码器和**Qwen2.5-0.5B**语言解码器组成，总参数仅约0.8B。这一选择的深层逻辑在于：原生多模态VLM在预训练阶段已经建立了更强的跨模态语义对齐，使得即使在轻量级参数规模下，也能保持高质量的融合多模态表征。如Figure 2所示，Evo-1的注意力图在训练后保持空间一致和语义对齐，而OpenVLA（Prismatic-7B）的注意力图则呈现明显的语义退化。

此外，Evo-1仅保留语言分支的前14层，因为中间层已被经验证明具有更强的跨模态对齐能力。这一裁剪进一步降低了计算开销，同时确保传递给动作专家的多模态表征$z_t$富含任务相关信息。

### 2. 交叉调制扩散Transformer：精简而高效的动作专家

传统VLA模型（如π0、SmolVLA）的动作专家通常采用交替的自注意力和交叉注意力层设计，这种结构虽然灵活，但引入了额外的计算复杂度和参数量。Evo-1提出**交叉调制扩散Transformer（Cross-modulated DiT）**，其核心设计是：**仅堆叠交叉注意力层，完全移除自注意力层**。

这一设计的合理性在于：动作序列的去噪过程主要依赖于条件信息（视觉语言表征和机器人状态）的引导，而非动作序列内部的全局自注意。通过将融合表征$z_t$与机器人状态$s_t$拼接后作为交叉注意力的键值输入，DiT的每一层都能直接访问多模态条件信息，从而以更少的参数实现高效的条件去噪。

动作生成基于流匹配（flow matching）范式：通过线性插值$A_t^\tau = \tau A_t + (1-\tau)\epsilon$生成带噪动作序列，动作专家学习预测时间相关的速度场，最终通过常微分方程求解器从噪声中恢复干净的动作序列$\hat{A}_t$。

### 3. 中层交叉注意力集成模块：在正确的位置融合信息

多模态信息如何从VLM传递到动作专家，是VLA架构设计的关键决策点。Evo-1系统性地探索了四种集成模块设计（Figure 6），并最终选择了**Module A：中层交叉注意力**（Figure 8(a)消融实验验证其最优性）。

Module A的设计哲学是“在语义最丰富的位置融合，并保持信息的原始完整性”：
- **中层提取**：从VLM的第14层（中间层）提取融合多模态表征$z_t$，而非使用最终输出层。中间层已被证明具有更强的跨模态对齐，能提供更丰富的语义信息。
- **拼接而非投影**：将$z_t$与机器人状态$s_t$直接拼接，而非将它们投影到共享嵌入空间。这避免了投影过程中的信息损失，保留了原始表征的完整性。
- **统一条件注入**：拼接后的特征作为所有DiT层交叉注意力的键值输入，确保每一层去噪步骤都能访问完整的条件信息。

相比之下，Module B（交错式交叉自注意力）和Module C/D（逐层交叉注意力或联合键值设计）在LIBERO-Long基准上均表现不如Module A，表明“中层提取+拼接注入”的组合是连接轻量级VLM与动作专家的最优方案。

### 4. 两阶段训练范式：渐进式语义保持

这是Evo-1最具方法论价值的创新。传统VLA训练采用单阶段端到端联合训练，即同时更新VLM骨干和动作专家。这种做法虽然简单，但会导致VLM的预训练语义空间被动作学习的目标函数“拉扯”，造成灾难性遗忘和语义退化（Figure 7(a)）。

Evo-1提出**两阶段训练范式**，将训练过程解耦为：

- **第一阶段：动作专家对齐**。冻结整个VLM骨干，仅训练动作专家和集成模块。这一阶段的目标是让动作专家学会如何利用VLM提供的“冻结”语义表征来预测动作，而不干扰VLM的语义空间。
- **第二阶段：全局联合微调**。解冻VLM骨干，以较小的学习率对整个模型进行微调。此时动作专家已经建立了稳定的输入-输出映射，VLM的微调仅需进行适应性调整，而非从头重建语义表征。

Figure 7的注意力图对比直观地展示了这一范式的效果：单阶段训练后的注意力图呈现语义混乱和焦点分散，而两阶段训练后的注意力图保持了清晰、语义一致的目标聚焦区域。Figure 8(b)的消融实验进一步量化了这一优势：两阶段训练在Meta-World所有难度级别上均优于单阶段训练，验证了渐进式语义保持在机器人操控中的关键作用。

### 创新协同效应

上述四个创新并非孤立存在，而是形成了正向协同：轻量级原生多模态VLM提供了高效的语义基础，交叉调制DiT以精简结构承接条件信息，中层集成模块在最优位置完成信息传递，而两阶段训练范式则确保整个过程中语义空间不被破坏。这一协同使得Evo-1在仅0.77B参数、不使用任何机器人预训练数据的条件下，在Meta-World上达到80.6%的平均成功率（超越2.25B的SmolVLA达12.4个百分点），同时保持16.4 Hz的推理频率和2.3 GB的GPU内存占用，在性能与效率之间取得了当前最优的平衡点。



Evo-1 采用模块化视觉-语言-动作（VLA）架构，将感知、推理与控制统一在一个计算高效的框架内。整个系统由三个核心模块级联构成：**视觉-语言骨干（Vision-Language Backbone）**、**集成模块（Integration Module）** 和 **交叉调制扩散Transformer（Cross-modulated Diffusion Transformer）**，形成从多模态感知到连续动作生成的端到端映射。

### 端到端映射关系

给定时间步 $t$ 的多视图 RGB 图像 $\{I_{t}^{i}\}_{i=1}^{N}$、语言指令 $L_{t}$ 和机器人本体状态 $s_{t}$，Evo-1 输出连续动作向量 $a_{t}$：

$$a_{t} = f_{\mathrm{Evo-1}}\big(\{I_{t}^{i}\}_{i=1}^{N}, L_{t}, s_{t}; \theta\big)$$

这一映射的核心瓶颈在于：现有 VLA 模型通常采用数十亿参数的大型 VLM 骨干，推理计算开销极高，难以在消费级 GPU 上实时部署；同时，常规端到端联合训练会破坏视觉-语言骨干的预训练语义表征，导致过拟合和泛化能力下降。Evo-1 通过轻量级原生多模态 VLM 和两阶段训练策略，直接针对这一瓶颈进行了系统性设计。

### 模块关系与数据流

**视觉-语言骨干**（InternVL3-1B）首先接收多视图图像和语言指令，通过原生多模态融合机制生成融合表征 $z_{t}$：

$$z_{t} = f_{\mathrm{VLM}}\big(\{I_{t}^{i}\}_{i=1}^{N}, L_{t}\big)$$

该骨干由 InternViT-300M 视觉编码器和 Qwen2.5-0.5B 语言解码器组成，总参数量仅约 0.8B。为增强跨模态对齐，仅保留语言分支的前 14 层输出作为融合表征，因为中间层被经验性地发现具有更强的跨模态对齐能力。

**集成模块**随后将融合表征 $z_{t}$ 与机器人本体状态 $s_{t}$ 进行对齐。具体而言，该模块从 VLM 的第 14 层提取融合多模态特征，将其与机器人状态拼接，作为动作专家的条件输入。与将两者投影到共享嵌入空间的常见做法不同，Evo-1 直接采用拼接操作，保留了各自特征的完整性。

**交叉调制扩散Transformer**作为动作专家，接收融合表征、机器人状态和带噪动作序列 $A_{t}^{\tau}$，基于流匹配范式预测未来动作序列 $\hat{A}_{t}$：

$$\hat{A}_{t} = f_{\mathrm{AE}}\big(z_{t}, s_{t}, A_{t}^{\tau}\big)$$

该模块仅堆叠交叉注意力层，以拼接后的多模态特征作为键-值输入，带噪动作序列作为查询输入，通过条件去噪过程生成连续动作。与 π0、SmolVLA 等基线中交替使用自注意力和交叉注意力层的设计不同，这种纯交叉注意力结构在保持轻量化的同时实现了高效的多模态条件建模。

### 两阶段训练范式

Evo-1 的训练分为两个阶段，这是保留 VLM 语义空间的关键设计：

- **第一阶段（动作专家对齐）**：冻结整个视觉-语言骨干，仅训练动作专家和集成模块。这确保 VLM 的预训练语义表征不被破坏，动作模块逐步学会将感知表征与动作空间对齐。
- **第二阶段（全局微调）**：解冻所有参数，对整个模型进行端到端微调，使各模块协同优化，进一步提升任务性能。

消融实验（Figure 8(b)）表明，两阶段训练在 Meta-World 所有难度级别上均优于单阶段联合训练。注意力图可视化（Figure 7）进一步证实：单阶段训练后 VLM 的语义注意力模式出现明显退化，而两阶段训练保留了清晰且语义一致的关注区域。

### 补充图表

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/001_Figure_1.jpg]]
*Figure 1: Architecture of Evo-1. The input RGB observations and language instructions are first encoded by a compact vision-language backbone. Their fused representations are aligned with the robot state through an optimized integration module and then processed by a cross-modulated diffusion transformer to generate actions. The right side shows results across three simulation benchmarks*



Evo-1 的端到端映射遵循统一的函数形式：

$$a_{t} = f_{\mathrm{Evo-1}}\big(\{I_{t}^{i}\}_{i=1}^{N}, L_{t}, s_{t}; \theta\big)$$

其中 $a_t$ 为当前时刻预测的连续动作向量，$\{I_{t}^{i}\}_{i=1}^{N}$ 为 $N$ 个视角的 RGB 图像，$L_t$ 为语言指令，$s_t$ 为机器人本体状态，$\theta$ 为全部可学习参数。该映射通过三个核心模块级联实现。

### 视觉-语言骨干：InternVL3-1B

骨干网络负责将多视图视觉感知与语言指令融合为统一的多模态表征：

$$z_{t} = f_{\mathrm{VLM}}\big(\{I_{t}^{i}\}_{i=1}^{N}, L_{t}\big)$$

Evo-1 选用 **InternVL3-1B** 作为原生多模态 VLM，其视觉编码器为 InternViT-300M（约 0.3B 参数），语言解码器为 Qwen2.5-0.5B。为强化跨模态对齐，仅保留语言分支的前 14 层——实证表明中间层具有更强的跨模态对齐能力。融合表征 $z_t$ 作为后续动作专家的核心条件输入，其语义质量直接决定下游操控性能。

### 集成模块：中层交叉注意力与状态拼接

集成模块负责将 VLM 输出的融合表征 $z_t$ 与机器人本体状态 $s_t$ 对齐。Evo-1 采用 **Module A（中层交叉注意力）** 设计：从 VLM 的第 14 层提取 $z_t$，将其与 $s_t$ 拼接后作为键值（key-value）输入，馈入动作专家的所有 DiT 层。该设计避免了将异构特征投影到共享嵌入空间可能带来的信息损失，消融实验（Figure 8(a)）表明其在 LIBERO-Long 上优于交错式、逐层式和联合键值式等替代方案。

### 动作专家：交叉调制扩散 Transformer

动作专家 $f_{\mathrm{AE}}$ 基于流匹配范式，从带噪动作序列中迭代恢复干净动作：

$$\hat{A}_{t} = f_{\mathrm{AE}}\big(z_{t}, s_{t}, A_{t}^{\tau}\big)$$

其中 $A_{t}^{\tau}$ 为通过线性插值生成的带噪动作序列：

$$A_{t}^{\tau} = \tau A_{t} + (1 - \tau) \epsilon$$

$\tau \in [0,1]$ 为时间步，$\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声。训练目标为流匹配损失：

$$\mathcal{L}^{\tau}(\theta) = \mathbb{E}_{p(A_{t}\mid z_{t}, s_{t}), q(A_{t}^{\tau}\mid A_{t})} \left[ \| \mathbf{v}_{\theta}(A_{t}^{\tau}, z_{t}, s_{t}) - \mathbf{u}(A_{t}^{\tau}\mid A_{t}) \|^{2} \right]$$

其中 $\mathbf{v}_{\theta}$ 为模型预测的速度场，$\mathbf{u}$ 为真实速度场。动作专家的架构核心是**交叉调制扩散 Transformer（Cross-modulated DiT）**，仅堆叠交叉注意力层（摒弃交替的自注意力与交叉注意力设计），以 $z_t$ 和 $s_t$ 的拼接特征作为条件，对带噪动作序列进行逐层去噪，最终输出预测动作序列 $\hat{A}_t$。

### 补充图表

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/010_Figure_6.jpg]]
*Figure 6: Integration Module Designs. Architectures of four different modules (A-D) for connecting the VLM and the action expert*

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/011_Figure_7.jpg]]
*Figure 7: Comparison of vision-language attention maps after training. (a) The single-stage paradigm shows disrupted attention with reduced semantic coherence. (b) Our two-stage paradigm preserves clear and semantically consistent focus regions*

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of vision-language attention maps after training. (a) Evo-1 (InternVL3-1B) yields spatially consistent and semantically aligned activations. (b) OpenVLA (Prismatic-7B) shows degraded coherence in attention maps*

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/009_Figure.jpg]]
*Figure: (a) Attention maps using single-stage training paradigm (b) Attention maps using two-stage training paradigm (ours)*



## 实验与关键发现

### 核心性能：仿真基准与真实世界

Evo-1 在三个主流仿真基准和真实世界任务上均展现出显著的性能优势，且模型参数仅 0.77B，未使用任何机器人预训练数据。Table 1 汇总了仿真基准结果：

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/003_Table_1.jpg]]
*Table 1: Simulation benchmark results on Meta-World, LIBERO, and RoboTwin. We evaluate Evo-1 against representative baselines on three widely used simulation benchmarks. Params denotes model size (in billions); Robo-Pretrain shows whether the model is pretrained on robot data; Bold marks the best result, and underline denotes the second best*

- **Meta-World**：Evo-1 平均成功率达 **80.6%**，较先前最佳轻量模型 SmolVLA（2.25B, 68.2%）提升 **12.4 个百分点**，较大型模型 π0（3.5B, 47.9%）提升 32.7 个百分点。该基准涵盖 50 个任务、按难度分组，Evo-1 在所有难度级别上均保持领先。
- **LIBERO**：Evo-1 平均成功率达 **94.8%**，与大型模型 π0（94.2%）持平，略优于 SmolVLA（90.2%）。在 LIBERO-Long 长序列子集上同样表现稳健（见消融部分 Figure 8(a)）。
- **RoboTwin**：双机械臂基准上，Evo-1 达 **37.8%**，超过 π0（30.9%）**6.9 个百分点**，验证了轻量架构在复杂协调任务上的有效性。

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/012_Figure_8.jpg]]
*Figure 8: Comparison results of integration modules and training paradigms. (a) Success rates of four integration modules on the LIBERO-Long benchmark. (b) Performance comparison on Meta-World between a single-stage and our two-stage training paradigm*

真实世界实验（Figure 4）在四个操控任务上进行，每任务收集 100 条遥操演示。Evo-1 总成功率达 **78%**，高于 π0（73%）。Figure 3 展示了各任务的逐步执行过程，模型在抓取、放置、移动等步骤中表现稳定。

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/006_Figure_4.jpg]]
*Figure 4: Results of Real-World experiments. Success rates of four real-world evaluation tasks (left four subplots) and the overall average success rate across tasks (rightmost subplot)*

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/004_Figure_3.jpg]]
*Figure 3: Task progress of Real-World Experiments. Step-bystep sequences for the real-world tasks. Each row shows the detailed progression of a task from start to completion*

### 推理效率：性能与开销的最佳平衡

Table 2 对比了各模型在 RTX 4090d 消费级 GPU 上的推理效率。Evo-1 的 GPU 内存占用仅 **2.3 GB**，推理频率达 **16.4 Hz**，同时真实世界成功率 78%。相比之下，π0 需 4.0 GB 内存、频率仅 3.6 Hz，成功率 73%；SmolVLA 内存 2.7 GB、频率 8.4 Hz，成功率 66%。Evo-1 在效率与性能之间实现了最佳平衡，证明了轻量级原生多模态 VLM 骨干（InternVL3-1B）与交叉调制 DiT 的联合设计优势。

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/008_Table_2.jpg]]
*Table 2: Inference efficiency comparison. Comparison of model size, inference efficiency, and real-world performance on an RTX 4090d GPU. Params (B): number of parameters (in billions); GPU Mem.(GB): average memory usage during inference; Infer. Freq.(Hz): average inference frequency; Success (%): overall success rate on real-world tasks*

### 泛化能力：视觉干扰下的鲁棒性

Table 3 报告了真实世界泛化实验的成功率，在四种扰动条件下对比 SmolVLA（Figure 5 展示了扰动设置）。Evo-1 在基础场景下成功率 95%，在未见干扰物、背景颜色变化、目标位置变化、目标高度变化下分别保持 80%、75%、70%、65%，整体显著优于 SmolVLA。这表明两阶段训练保留的语义对齐（Figure 7）有助于模型在视觉分布偏移时维持稳定的注意力聚焦。

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/007_Table_3.jpg]]
*Table 3: Success rates for generalization experiments. Comparison of success rates between SmolVLA and Ours under different disturbance conditions in real-world task generalization experiments*

![[assets/figures/papers/paper_list_l2234_https_arxiv_org_abs_2511_04555/figures/005_Figure_5.jpg]]
*Figure 5: Disturbance settings of generalization experiments. We evaluate model generalization under four variations: (1) unseen distractor object, (2) background color variation, (3) target position variation, and (4) target height variation*

### 消融实验：集成模块与训练范式

**集成模块设计**（Figure 8(a)）在 LIBERO-Long 上对比了四种方案（架构见 Figure 6）。Module A（中层交叉注意力 + 拼接机器人状态）成功率最高，验证了以下设计选择的有效性：从 VLM 第 14 层提取融合表征 $z_t$，与机器人状态 $s_t$ 拼接后作为所有 DiT 层的键值输入。交错式（Module B）、逐层式（Module C）和联合键值式（Module D）设计均导致性能下降，说明简单的拼接策略在保留语义信息的同时避免了模态间的干扰。

**训练范式**（Figure 8(b)）在 Meta-World 所有难度级别上对比了单阶段联合训练与两阶段训练。两阶段训练（先冻结 VLM 仅训练动作专家，再全局微调）在所有难度上均优于单阶段，尤其在 Hard 和 Very Hard 任务上优势明显。Figure 7 的注意力图对比进一步揭示了因果机制：单阶段训练的注意力图语义一致性被破坏，而两阶段训练保留了清晰的、语义对齐的聚焦区域，验证了“保留 VLM 语义空间”这一核心设计动机。

### 失败模式与局限

尽管整体性能优异，Evo-1 仍存在以下已知局限（需结合原始论文进一步确认具体失败案例）：
- 真实世界评估仅覆盖四个任务，场景多样性有限，在全新环境或不同机械臂形态上的泛化尚待验证。
- 每任务仍需 50–100 条遥操演示，数据采集成本不可忽略。
- 模型设计针对短时序操控（动作预测长度 H ≤ 50），在长期规划或多阶段任务上的表现未经测试。
- 轻量级 VLM 的视觉语言理解能力在极端视觉变化或复杂指令下可能不足，泛化实验中的性能下降（如目标高度变化下仅 65%）暗示了这一瓶颈。



## 定位与知识库关联

### 1. 在VLA模型谱系中的位置

Evo-1处于**轻量级端到端视觉-语言-动作（VLA）模型**这一细分方向，其核心定位是在不依赖大规模机器人预训练数据的前提下，通过保留视觉-语言骨干的语义对齐来实现高效操控。与现有工作的关系可沿两条轴梳理：

**（1）模型规模轴——从大型VLA到轻量VLA**

大型VLA模型以**OpenVLA**（7B参数，Prismatic-7B骨干）、**π0**（3.5B参数）和**GR00T N1**为代表，通常需要数十亿参数和昂贵的推理硬件。轻量级路线则以**SmolVLA**（2.25B参数）和**TinyVLA-H**为先行者，试图在保持可部署性的同时压缩模型规模。Evo-1将这一趋势推向极致：仅0.77B参数（InternViT-300M视觉编码器 + Qwen2.5-0.5B语言解码器截断至14层），在RTX 4090d消费级GPU上仅占用2.3 GB显存、达到16.4 Hz推理频率（Table 2），同时以78%的真实世界成功率超越π0（73%）和SmolVLA（63%）。这一效率-性能的帕累托前沿改进，直接回应了大型VLA"推理计算开销高、难以实时部署"的瓶颈。

**（2）预训练数据轴——从机器人预训练到零机器人预训练**

OpenVLA和π0均依赖大规模机器人数据集（如Open X-Embodiment）进行预训练，数据收集成本极高。SmolVLA同样需要机器人预训练。Evo-1的关键突破在于**完全不使用任何机器人预训练数据**，仅依靠原生多模态VLM（InternVL3-1B）在互联网规模图文数据上获得的语义表征，配合两阶段训练策略（先冻结VLM训练动作专家，再全局微调），在Meta-World上达到80.6%平均成功率，超过SmolVLA（68.2%）12.4个百分点（Table 1）。这证明**保留VLM预训练语义空间**可以替代昂贵的机器人域内预训练。

### 2. 架构设计的知识贡献

Evo-1的架构创新可分解为三个可迁移的设计选择，每个都有明确的消融证据支撑：

**（1）集成模块设计：中层交叉注意力 + 状态拼接（Module A）**

现有VLA模型的多模态融合方式多样：π0和SmolVLA采用交错式自注意力和交叉注意力层（类似Module B），OpenVLA使用逐层交叉注意力（类似Module C），而联合键值投影（Module D）是另一种常见选择。Evo-1的Module A从VLM第14层（中间层，经验上具有更强的跨模态对齐）提取融合表征$z_t$，与机器人状态$s_t$直接拼接后作为DiT所有Transformer块的键值输入。消融实验（Figure 8a）显示，Module A在LIBERO-Long上显著优于交错式、逐层式和联合键值式设计。这一发现为VLA中"何时以及如何将VLM表征注入动作专家"提供了明确的设计指南。

**（2）动作专家架构：纯交叉注意力DiT**

不同于π0和SmolVLA在动作专家中交替使用自注意力和交叉注意力层，Evo-1的Cross-modulated Diffusion Transformer仅堆叠交叉注意力层。这一简化设计建立在流匹配（flow matching）范式之上，以条件速度场$\mathbf{v}_\theta(A_t^\tau, z_t, s_t)$预测去噪方向。其有效性在Meta-World和RoboTwin上的SOTA结果中得到验证，但消融实验中未单独对比"纯交叉注意力 vs. 交替注意力"这一变量，该设计选择的独立贡献需要手动核实。

**（3）两阶段训练范式**

单阶段端到端联合训练是VLA的主流做法，但会导致VLM的预训练语义表征被破坏（Figure 7a注意力图显示语义焦点分散）。Evo-1的两阶段策略——第一阶段冻结VLM仅训练动作专家和集成模块，第二阶段全局微调——在Meta-World所有难度级别上均优于单阶段训练（Figure 8b），且保留的注意力图（Figure 7b）证实语义空间未被破坏。这一训练范式可推广到其他需要保留预训练表征的下游任务，但其在导航、移动操控等场景的有效性仍是开放问题。

### 3. 适用边界与局限

**（1）任务范围边界**

Evo-1目前仅在**单步/短时序操控任务**上验证：Meta-World和LIBERO为桌面物体操控，RoboTwin为双机械臂协调，真实世界实验仅覆盖4个任务（Figure 4）。模型设计针对动作序列长度$H \leq 50$，尚未验证在需要长期规划或多阶段推理的任务（如"先打开抽屉再取出物品"）上的表现。能否将架构扩展到更长时序或分层策略，是明确的开放问题。

**（2）数据效率边界**

尽管无需机器人预训练，Evo-1仍需要每任务50-100条遥操演示（Meta-World每任务50条共2500条，真实世界每任务100条）。在数据更稀缺的场景（如每任务仅5-10条演示），模型能否保持性能尚不可知。与**Diffusion Policy**和**ACT**等模仿学习基线在低数据区间的对比未在论文中给出。

**（3）泛化边界**

泛化实验（Table 3）显示，Evo-1在未见干扰物（80%）、背景颜色变化（90%）、目标位置变化（85%）和目标高度变化（90%）条件下保持较高成功率，但所有扰动均在**同一任务框架内**施加。对于全新机械臂形态、完全不同的环境布局或跨任务迁移，泛化能力未经测试。轻量VLM（0.5B语言解码器）的视觉语言理解能力在极端视觉变化或复杂指令下可能弱于大型模型，这一推断需要手动验证。

**（4）VLM骨干的依赖性**

Evo-1的性能与InternVL3-1B的原生多模态设计深度绑定。Figure 2显示，InternVL3-1B的注意力图保持空间一致和语义对齐，而Prismatic-7B（OpenVLA骨干）的注意力图则出现退化。这意味着Evo-1的架构优势部分来源于骨干选择——若替换为其他轻量VLM（如SmolVLM-2），语义保持效果是否同样显著，是待验证的开放问题。

### 4. 知识库定位总结

Evo-1在VLA知识库中的核心贡献是**证明"轻量级原生多模态VLM + 两阶段语义保留训练"可以替代大规模机器人预训练，在消费级硬件上实现超越大型模型的操控性能**。其可迁移的知识点包括：中层交叉注意力集成设计、纯交叉注意力DiT的可行性、以及两阶段训练对语义空间的保护作用。主要知识空白在于：长时序任务扩展、跨形态泛化、以及骨干VLM选择的鲁棒性。



## 原文 PDF

![[paperPDFs/CVPR_2026/Evo_1_Lightweight_Vision_Language_Action_Model_with_Preserved_Semantic_Alignment.pdf]]
