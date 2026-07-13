---
title: COLLAGE Collaborative Human Agent Interaction Generation using Hierarchical Latent Diffusion and Language Models
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/COLLAGE_Collaborative_Human_Agent_Interaction_Generation_using_Hierarchical_Latent_Diffusion_and_Language_Models.pdf
project_link: null
code_link: null
aliases:
- CCHAIGUHLDLM
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用大语言模型（LLM）生成层次化运动规划线索，并通过潜在空间扩散模型的条件引导，将语义推理与运动生成相结合，从而在少量数据下实现控制性强、多样化的交互生成。
primary_logic: 通过分层VQ-VAE提取不同抽象层次的运动特征，并结合LLM提供的语义规划线索，扩散模型能够逐步细化运动序列，使得高层语义（如任务类型）影响早期扩散步骤，而细粒度细节影响后期，实现高效且可控的协同交互生成。
claims:
- COLLAGE在CORE-4D文本条件生成任务上达到FID 6.890，优于移除层次结构的基线（FID 7.452）
- COLLAGE在InterHuman数据集上达到R-Precision Top1 0.383，FID 0.778，优于InterGen、MotionGPT、T2M-GPT等现有方法
- 消融实验表明，移除层次化VQ-VAE、LLM引导或时间调制均导致性能显著下降
- LLM规划线索使扩散模型在15步DDIM采样下即可生成高质量运动，推断速度比MDM快65%
---

# COLLAGE Collaborative Human Agent Interaction Generation using Hierarchical Latent Diffusion and Language Models

> [!tip] 核心洞察
> 通过分层VQ-VAE提取不同抽象层次的运动特征，并结合LLM提供的语义规划线索，扩散模型能够逐步细化运动序列，使得高层语义（如任务类型）影响早期扩散步骤，而细粒度细节影响后期，实现高效且可控的协同交互生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | COLLAGE：基于分层潜在扩散和语言模型的协同人-代理交互生成 |
| 英文题名 | COLLAGE Collaborative Human Agent Interaction Generation using Hierarchical Latent Diffusion and Language Models |
| 会议/期刊 | arXiv 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | COLLAGE |
| Dataset | CORE-4D |

> [!tip] 效果简介
> - CORE-4D (Object-conditioned, S1) 上，RR.Je(mm,↓) 131.2 vs 138.0 (MDM) (-6.8)。
> - CORE-4D (Object-conditioned, S2) 上，RR.Ve(mm,↓) 198.7 vs 208.2 (MDM) (-9.5)。
> - CORE-4D (Text-conditioned) 上，FID 6.890 vs 7.452 (w/o Hierarchy) (-0.562)。

## 概要

协同人-物-人交互生成（collaborative human-object-human interaction generation）面临两大瓶颈：**多智能体协调与长期规划的极高复杂性**，以及**高质量交互动作捕捉数据的稀缺**。现有方法（如 InterGen、MDM 等）或专注于两人交互，或缺乏对物体参与的协同建模，难以在少量数据下生成可控、多样且物理合理的协同运动。

COLLAGE 的核心洞察在于：**将大语言模型（LLM）的语义推理能力与层次化潜在扩散模型相结合**，通过分层 VQ-VAE 提取不同抽象级别的运动特征，并利用 LLM 生成的规划线索（planning cues）在扩散过程中进行条件引导——高层语义（如任务类型、角色分工）影响早期去噪步骤，细粒度运动细节影响后期步骤，从而实现高效且可控的生成。

方法定位上，COLLAGE 属于 **LLM 引导的潜在扩散生成**范式，在以下维度对现有框架进行了关键改造：将单层 VQ-VAE 扩展为 6 层层次化架构，引入 GPT-4 生成的规划线索并通过对比学习与码本关联，设计时间依赖调制函数动态控制各级线索在扩散过程中的影响力，以及将离散潜码聚合为连续表示直接输入扩散解码器。

实验表明，COLLAGE 在 CORE-4D 文本条件生成任务上达到 **FID 6.890**，优于移除层次结构的基线（FID 7.452）；在 InterHuman 数据集上达到 **R-Precision Top1 0.383、FID 0.778**，显著优于 InterGen、MotionGPT、T2M-GPT 等方法。消融研究证实，移除层次化 VQ-VAE、LLM 引导或时间调制均导致性能明显下降。此外，LLM 规划线索使扩散模型仅需 **15 步 DDIM 采样**即可生成高质量运动，推断速度比 MDM 快约 65%。

主要局限包括：缺乏显式物理建模可能导致穿透或不自然接触，CORE-4D 数据集规模有限（998 个序列）对泛化性构成挑战，以及当前不支持细粒度运动编辑。



### 问题背景：协同人-物-人交互生成

生成逼真且可控的多人-多物协同交互运动是计算机视觉与图形学中的核心挑战，其应用涵盖机器人协作、虚拟现实、人机交互等领域。与单人运动生成不同，协同交互生成需要同时建模多个智能体（人类或机器人）与物体之间的空间-时序耦合关系，这要求生成的每一帧运动不仅满足个体的运动学合理性，还必须保持跨实体的语义一致性与物理接触真实性。

该问题的形式化定义如下：给定文本描述或物体轨迹条件，生成 $n$ 个人类智能体运动序列 $\{X^i\}_{i=1}^n$ 与 $m$ 个物体运动序列 $\{Y^j\}_{j=1}^m$，使得各实体间的交互行为符合高层任务语义（如“两人协作搬运桌子”）并保持细粒度的时空协调。

### 现有方法缺口

当前主流方法在协同交互生成方面存在三个根本性瓶颈：

**第一，数据稀缺性约束。** 协同人-物-人交互的高质量动作捕捉数据集极为有限。例如，CORE-4D数据集仅包含998个运动序列，覆盖5个物体类别。这种数据匮乏使得依赖大规模训练的标准生成模型难以捕捉交互行为的全部多样性，尤其对于长尾交互模式几乎无法泛化。

**第二，多智能体协调的复杂建模缺口。** 现有方法多聚焦于单人运动生成或两人交互生成。例如，**InterGen**（Wang et al., CVPR 2023）仅处理双人交互，**MDM**（Tevet et al., arXiv 2022）虽支持扩散生成但缺乏对多实体交互的显式建模。这些方法在扩展至多人-多物场景时，面临组合爆炸和协调一致性难以保证的困境。

**第三，长期规划与语义控制不足。** 基于VQ-VAE的方法如**T2M-GPT**（Guo et al., ECCV 2022）和**MotionGPT**（Zhang et al., arXiv 2023）虽能生成多样化的运动，但缺乏对协同任务的高层语义推理能力，难以将“协作搬运”这样的抽象任务描述转化为具有时序逻辑的运动序列。扩散模型虽具备高质量生成能力，但纯数据驱动的方式在数据稀缺时无法有效学习任务级语义约束。

### 核心动机：融合语言模型的语义推理与层次化运动表征

本文的出发点在于突破上述瓶颈，核心思路是利用大语言模型（LLM）的语义推理与规划能力来弥补运动数据匮乏带来的学习困难，同时通过层次化运动表征实现从粗粒度任务语义到细粒度运动细节的渐进式生成。

具体而言，COLLAGE框架的设计动机源于以下观察：人类协同行为天然具有层次结构——高层决定“做什么任务”，中层规划“如何协调”，底层实现“具体动作”。这一结构与扩散模型的去噪过程天然契合：早期去噪步骤可受高层语义引导确定任务类型，后期步骤则受细粒度线索约束以生成精确的关节运动。通过将LLM生成的规划线索注入扩散过程的各个层次，模型能够在极少训练数据下实现强控制性与高多样性的协同交互生成。



## 核心方法与创新机理

COLLAGE 的核心创新在于将**大语言模型的语义推理能力**与**分层潜在扩散模型**相结合，解决了协同人-物-人交互生成中长期存在的两个瓶颈：多智能体协调的复杂性和高质量交互数据的稀缺性。其创新体系可归纳为三个相互耦合的 changed slots。

### 1. 分层 VQ-VAE 架构：多抽象层次的运动表征

现有方法（如 **T2M-GPT** (Guo et al., ECCV 2022)）采用单层 VQ-VAE 将运动序列压缩为离散潜码，再通过自回归先验生成。这种扁平化表征难以解耦高层语义（如任务类型、交互意图）与低层细节（如关节速度、接触时机）。

COLLAGE 提出 **6 层层级化 VQ-VAE**（L=6），每层捕捉不同抽象级别的运动特征。其关键设计包括：

- **逐层编码**：每层编码器以上一层的潜表示作为输入，逐步抽象。对于人体运动，$\mathbf{Z}_H^{i,(l)} = E_H^{(l)}(\mathbf{Z}_H^{i,(l-1)})$，其中 $\mathbf{Z}_H^{i,(0)} = \mathbf{X}^i$ 为原始运动序列；物体轨迹同理。
- **多实体交互建模**：在每层编码后，通过多头注意力机制捕捉所有人体-人体、人体-物体对之间的交互关系，使潜表示显式编码协同信息。
- **解耦正则化**：引入分层解耦损失 $\mathcal{L}_{\mathrm{disent}}$，通过最小化相邻层潜码的协方差 Frobenius 范数，强制不同层关注互不冗余的运动特征。

消融实验证实了这一设计的决定性作用：移除层次结构（w/o Hierarchy）导致 CORE-4D 数据集上 FID 从 6.890 升至 7.452，InterHuman 数据集上 FID 从 0.778 激增至 5.582。此外，增加层次级别和码本大小可提升潜在空间的互信息间隙（MIG）分数，表明解耦度增强。

### 2. LLM 语义规划引导：从文本到层次化运动线索

传统方法仅使用文本嵌入作为全局条件，缺乏对运动序列的细粒度语义指导。COLLAGE 引入 **GPT-4 生成的分层规划线索**，将 LLM 的常识推理注入扩散过程。

具体机制如下：
- **规划线索生成**：给定文本提示，GPT-4 生成描述各抽象层次运动特征的规划文本，例如高层描述“两人协同搬运桌子”，低层描述“左手抓握桌沿，脚步向左侧移动”。这些文本通过 CLIP ViT-B/32 编码为嵌入向量 $\mathbf{e}_l$。
- **关联对比学习**：通过对比损失 $\mathcal{L}_{\mathrm{assoc}}^{(l)}$ 将规划线索嵌入与 VQ-VAE 码本中的潜码对齐，使语义概念与运动模式建立显式映射。实验表明，选择 7-8 个最相关潜码与规划线索关联可获得最佳性能。
- **时间依赖调制**：在扩散去噪网络的每个 MM-Block 中，通过交叉注意力融合规划线索，并引入时间依赖调制函数 $\gamma_l(t)$。高层线索在早期扩散步骤影响大（决定整体运动结构），低层细节在后期步骤影响大（细化局部动作）。这一设计使扩散模型仅需 **15 步 DDIM 采样**即可生成高质量运动，推断速度比 **MDM** (Tevet et al., arXiv 2022) 快 **65%**。

消融实验表明，移除 LLM 引导（w/o LLM）导致 R-Precision 显著下降；用固定权重替换时间调制（w/o Time Modulation）同样使 FID 升高，验证了该模块的必要性。

### 3. 连续潜空间扩散：替代自回归先验

不同于 T2M-GPT 等基于 VQ-VAE 的方法使用自回归 Transformer 逐 token 生成离散潜码序列，COLLAGE 将所有层的量化潜码聚合为**连续表示**，直接输入潜在扩散模型的 U-Net 去噪网络。这一改变带来两重优势：

- **全局一致性**：扩散模型在连续潜空间中一次性去噪整个序列，避免自回归方法的误差累积。
- **高效条件注入**：LLM 规划线索通过交叉注意力无缝集成到去噪过程的每个 MM-Block 中，实现语义引导的渐进式细化。

去噪网络扩展了 U-Net 架构以处理时空图数据，包含 4 个 MM-Block，每个 Block 组合时序卷积网络（TCN）和图注意力网络（GAT），分别捕捉时间依赖和空间交互关系。训练目标为简化的扩散损失 $\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{\mathbf{x}_0, \epsilon, t} \left[ \| \epsilon - \epsilon_\theta(\mathbf{x}_t, t, \mathcal{G}, \mathbf{E}_L) \|^2 \right]$，预测所添加的噪声。

### 创新耦合效应

上述三个 changed slots 并非孤立改进，而是形成因果闭环：分层 VQ-VAE 提供多尺度运动表征空间，LLM 规划线索为各尺度注入语义先验，时间调制确保语义与细节在扩散过程中分阶段生效，连续潜空间扩散则统一优化全局运动序列。这一耦合使得 COLLAGE 在仅 998 个训练序列的 CORE-4D 数据集上，仍能生成物理合理、语义准确的协同交互，FID 达到 6.890，显著优于移除任一模块的消融基线。



COLLAGE 的整体管线由三个核心阶段串联构成：**层次化 VQ-VAE 运动表征学习** → **LLM 规划线索生成与关联** → **潜空间扩散生成**。其设计目标是在有限的动作捕捉数据下，实现文本条件或物体条件下的协同人-物-人交互生成。

### 阶段一：层次化 VQ-VAE 编码

系统首先将多人运动序列 $X^i$（$i=1,\dots,n$）与物体轨迹 $Y$ 送入一个 $L=6$ 层的层次化 VQ-VAE。每一层编码器以上一层的潜表示作为输入，逐层提取从粗粒度语义（如任务类型、交互意图）到细粒度细节（如关节速度、接触模式）的运动特征：

$$Z_H^{i,(l)} = E_H^{(l)}(Z_H^{i,(l-1)}; \theta_H^{(l)}), \quad Z_O^{(l)} = E_O^{(l)}(Z_O^{(l-1)}; \theta_O^{(l)})$$

其中 $Z_H^{i,(0)} = X^i$，$Z_O^{(0)} = Y$。在每一层内部，**多头注意力机制**被用于捕捉所有实体对（$n$ 个人与 $m$ 个物体之间）的交互关系。随后，人类与物体分别通过独立的码本 $\mathcal{C}_H^{(l)}$ 和 $\mathcal{C}_O^{(l)}$（每层码本尺寸 $512 \times 512$，潜维度 512）进行向量量化，得到离散潜码 $\bar{Z}_H^{i,(l)}$ 和 $\bar{Z}_O^{(l)}$。解码器则从所有层的量化潜码中聚合连续表示，重建原始运动。

训练阶段通过联合优化重建损失 $\mathcal{L}_{\text{recon}}$、承诺损失 $\mathcal{L}_{\text{commit}}$、接触损失 $\mathcal{L}_{\text{contact}}$、速度平滑损失 $\mathcal{L}_{\text{smooth}}$ 以及层次化解耦损失 $\mathcal{L}_{\text{disent}}$ 来训练 VQ-VAE，确保不同层捕获互补的运动特征。

### 阶段二：LLM 规划线索生成与关联

给定文本提示，系统调用 **GPT-4** 生成层次化的运动规划线索——这些线索以自然语言描述不同抽象层次的动作意图（例如高层描述“两人合作搬运箱子”，低层描述“左手接触箱体左边缘”）。每条线索通过 **CLIP ViT-B/32** 文本编码器嵌入为向量 $\mathbf{e}_l$。

为了将这些语义线索与 VQ-VAE 的潜码空间对齐，系统在每一层引入**关联对比损失** $\mathcal{L}_{\text{assoc}}^{(l)}$，将规划线索嵌入与码本中最相关的 $7\sim8$ 个潜码拉近，与其余码字推远。这一对齐过程使得 LLM 的语义推理能力能够直接作用于运动生成的控制信号。

### 阶段三：潜空间扩散生成

扩散模型在 VQ-VAE 学到的连续潜空间上运行，采用扩展的 **U-Net** 架构，包含 $M=4$ 个 **Motion Modeling Block（MM-Block）**。每个 MM-Block 依次应用时序卷积网络（TCN，核尺寸 $\{3,5,7\}$）和图注意力网络（GAT）来建模运动序列的时空依赖关系。

LLM 规划线索通过**时间依赖的交叉注意力**注入去噪过程：

$$\mathbf{H}_i^l = \text{CrossAttn}(\mathbf{H}_i, \gamma_l(t) \cdot \tilde{\mathbf{E}}_L)$$

其中 $\gamma_l(t)$ 是时间步 $t$ 的调制函数，其核心机制在于：**高层线索在扩散早期（大 $t$）影响力大，决定整体动作语义；低层细节线索在扩散后期（小 $t$）主导，精调关节运动。** 这一策略使模型仅需 15 步 DDIM 采样即可生成高质量运动，推理速度比 MDM 快约 65%。

训练目标为简化的去噪损失：

$$\mathcal{L}_{\text{simple}} = \mathbb{E}_{\mathbf{x}_0, \epsilon, t} \left[ \| \epsilon - \epsilon_\theta(\mathbf{x}_t, t, \mathcal{G}, \mathbf{E}_L) \|^2 \right]$$

其中 $\mathcal{G}$ 为实体交互图，$\mathbf{E}_L$ 为 LLM 规划线索嵌入。

### 管线输入输出流总结

1. **输入**：文本提示（如“两人合作搬运一把椅子”）或物体条件轨迹。
2. **LLM 规划**：GPT-4 生成层次化规划线索 → CLIP 嵌入。
3. **扩散生成**：随机噪声 $\mathbf{x}_T$ 在潜空间中经 $T$ 步去噪，每一步通过交叉注意力融合时间调制的规划线索，最终输出潜表示。
4. **解码**：VQ-VAE 解码器将潜表示重建为多人运动序列与物体轨迹。

消融实验验证了这一管线设计的必要性：移除层次化 VQ-VAE（退化为单层）导致 CORE-4D 上 FID 从 6.890 升至 7.452，InterHuman 上 FID 从 0.778 升至 5.582；移除 LLM 引导或时间调制同样造成性能显著下降。

### 补充图表

![[assets/figures/papers/paper_list_l1667_COLLAGE_Collaborative_Human_Agent_Interaction_Generation_using_Hierarchi/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed COLLAGE framework for collaborative human-object interaction generation. The hierarchical VQ-VAE encoder captures motion-specific characteristics at different levels of abstraction. The latent diffusion model operates in the learned latent space and incorporates LLM-generated motion planning cues to guide the denoising process, enabling the generation of prompt-specific interactions with enhanced control and diversity as in Fig 1*



COLLAGE 框架由三个紧密耦合的核心模块构成：**层级化 VQ-VAE**、**LLM 规划线索生成与关联**，以及**潜空间扩散模型**。三个模块通过分层抽象、语义对齐和条件引导形成闭环，共同解决协同人-物-人交互生成中的多智能体协调与长期规划难题。

### 层级化 VQ-VAE

层级化 VQ-VAE 是 COLLAGE 的特征提取骨干，负责将原始运动序列和物体轨迹压缩为多个抽象层次的离散潜表示。设输入包含 $n$ 个人体运动序列 $X^i \in \mathbb{R}^{T \times D_H}$ 和 $m$ 个物体轨迹 $Y \in \mathbb{R}^{T \times D_O}$，编码器以层级递进方式提取特征：

$$Z_H^{i,(l)} = E_H^{(l)}(Z_H^{i,(l-1)}; \theta_H^{(l)}), \quad Z_O^{(l)} = E_O^{(l)}(Z_O^{(l-1)}; \theta_O^{(l)})$$

其中 $Z_H^{i,(0)} = X^i$，$Z_O^{(0)} = Y$，$l \in \{1, \dots, L\}$（论文设置 $L=6$）。每一层编码后，通过多头注意力机制捕捉人-人、人-物、物-物之间的交互关系，随后使用独立的码本 $\mathcal{C}_H^{(l)}$ 和 $\mathcal{C}_O^{(l)}$（尺寸 $512 \times 512$，潜维度 $512$）进行向量量化，得到离散潜码 $\bar{Z}_H^{i,(l)}$ 和 $\bar{Z}_O^{(l)}$。解码过程对称地将各层潜码聚合为连续表示后重建原始运动。

层级化设计的核心在于**解耦不同抽象层次的运动特征**。为强化这一特性，引入层级解耦损失，通过最小化相邻层潜码的协方差来迫使不同层捕捉互补信息：

$$\mathcal{L}_{\mathrm{disent}} = \sum_{l=1}^{L-1} \sum_{i=1}^{n} \| \mathrm{Cov}(\bar{Z}_{H}^{i,(l)}, \bar{Z}_{H}^{i,(l+1)}) \|_{F}^{2} + \| \mathrm{Cov}(\bar{Z}_{O}^{(l)}, \bar{Z}_{O}^{(l+1)}) \|_{F}^{2}$$

VQ-VAE 的整体训练目标由重建损失、承诺损失、接触损失和速度平滑损失加权组合而成。其中重建损失为原始运动与重建运动之间的 L2 距离：

$$\mathcal{L}_{\mathrm{recon}} = \sum_{i=1}^{n} \| X^{i} - \hat{X}^{i} \|_{2}^{2} + \| Y - \hat{Y} \|_{2}^{2}$$

承诺损失鼓励编码器输出靠近量化后的码字：

$$\mathcal{L}_{\mathrm{commit}}^{(l)} = \sum_{i=1}^{n} \| \hat{Z}_{H}^{i,(l)} - \mathrm{sg}(\bar{Z}_{H}^{i,(l)}) \|_{2}^{2} + \| \hat{Z}_{O}^{(l)} - \mathrm{sg}(\bar{Z}_{O}^{(l)}) \|_{2}^{2}$$

接触损失 $\mathcal{L}_{\mathrm{contact}}$ 和速度平滑损失 $\mathcal{L}_{\mathrm{smooth}}$ 作为软约束，分别促进合理的人-物接触和运动平滑性，但论文明确指出这些损失无法完全替代显式物理建模。

### LLM 规划线索与关联对比学习

COLLAGE 利用 GPT-4 为每个运动序列生成层次化规划描述文本，并通过 CLIP ViT-B/32 嵌入为向量 $\mathbf{e}_l$。这些规划线索需要与 VQ-VAE 码本中的潜码建立语义关联，以便在扩散过程中提供条件引导。

关联通过对比学习实现。对于第 $l$ 层，将规划线索嵌入 $\mathbf{e}_l$ 与码本中所有码字进行对比，使语义相关的码字与线索嵌入在特征空间中靠近：

$$\mathcal{L}_{\mathrm{assoc}}^{(l)} = - \sum_{(c, \mathbf{e}_l)} \log \frac{\exp(\cos(\phi_c^{(l)}(c), \phi_e^{(l)}(\mathbf{e}_l)) / \tau)}{\sum_{c' \in \mathcal{C}^{(l)}} \exp(\cos(\phi_c^{(l)}(c'), \phi_e^{(l)}(\mathbf{e}_l)) / \tau)}$$

其中 $\phi_c^{(l)}$ 和 $\phi_e^{(l)}$ 分别为码字和线索嵌入的投影网络，$\tau$ 为温度参数。消融实验表明，选择 7-8 个最相关潜码与规划线索关联可获得最佳性能（Fig. 3(a)）。

### 潜空间扩散模型与时间依赖调制

扩散模型在 VQ-VAE 的连续潜空间中执行去噪过程。去噪网络采用扩展 U-Net 架构，包含 $M=4$ 个 Motion Modeling Block（MM-Block），每个 Block 内部依次通过时序卷积网络（TCN，核大小 $\{3, 5, 7\}$）和空间图注意力网络（GAT）处理时空图数据。

LLM 规划线索通过交叉注意力机制注入每个 MM-Block，并引入**时间依赖调制函数** $\gamma_l(t)$ 控制不同抽象层次线索在去噪各阶段的影响力：

$$\mathbf{H}_i^l = \mathrm{CrossAttn}(\mathbf{H}_i, \gamma_l(t) \cdot \tilde{\mathbf{E}}_L)$$

这一设计的核心直觉是：高层语义线索（如任务类型）在扩散早期（大 $t$）影响更大，主导运动整体结构；低层细节线索在扩散后期（小 $t$）影响更大，细化局部动作。消融实验证实，用固定权重替换该调制机制会导致 FID 升高（Table I bottom）。

扩散模型的训练采用简化的噪声预测目标：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{\mathbf{x}_0, \epsilon, t} \left[ \| \epsilon - \epsilon_\theta(\mathbf{x}_t, t, \mathcal{G}, \mathbf{E}_L) \|^2 \right]$$

其中 $\mathcal{G}$ 为人-物交互图结构，$\mathbf{E}_L$ 为各层规划线索嵌入的集合。最终通过线性投影将去噪后的节点特征映射回原始潜空间维度 $\mathbb{R}^{F \times V \times K}$，得到预测噪声 $\hat{\boldsymbol{\epsilon}}$。推理时采用 DDIM 采样，得益于 LLM 规划线索的强引导作用，仅需 15 步即可生成高质量运动，推断速度比 MDM 快约 65%（Fig. 3(c)）。



## 实验与关键发现

### 主实验结果

COLLAGE在CORE-4D和InterHuman两个数据集上进行了文本条件交互生成和物体条件交互合成的全面评估。

**文本条件交互生成**（Table I）：在CORE-4D数据集上，COLLAGE取得FID 6.890，优于移除层次结构的基线（FID 7.452）。在InterHuman数据集上，COLLAGE达到R-Precision Top1 0.383和FID 0.778，显著优于InterGen、MotionGPT、T2M-GPT等现有方法。Diversity指标同样表现优异，证明生成结果兼具真实性和多样性。

**物体条件交互合成**（Table II）：在CORE-4D的S1场景下，COLLAGE的关节位置误差RR.Je为131.2 mm，相比MDM的138.0 mm降低6.8 mm；在S2场景下，顶点误差RR.Ve为198.7 mm，相比MDM的208.2 mm降低9.5 mm。这验证了分层潜空间和LLM引导对精确交互建模的有效性。

### 消融实验

Table I底部报告了系统性的消融结果，揭示各组件的因果贡献：

- **层次化VQ-VAE的移除**（w/o Hierarchy）：CORE-4D上FID从6.890升至7.452，InterHuman上FID从0.778急剧恶化至5.582，表明层次化潜空间是生成质量的核心支撑。层次结构使模型能够在不同抽象级别捕捉运动特征，缺失时低层细节与高层语义混杂，导致生成退化。

- **LLM引导的移除**（w/o LLM）：R-Precision显著下降，说明LLM生成的规划线索对语义对齐至关重要。LLM提供的层次化运动描述使扩散模型在去噪过程中获得明确的语义方向，缺失后模型难以从文本精确还原交互意图。

- **时间依赖调制的移除**（w/o Time Modulation）：用固定权重替换γ_l(t)调制函数后FID升高。这验证了高层线索在早期扩散步骤影响大、低层细节在后期步骤影响大的设计合理性——固定权重无法实现这种渐进式细化。

- **加速推断**（Fig. 3(a)和Fig. 3(c)）：LLM规划线索使扩散模型仅需15步DDIM采样即可生成高质量运动，推断时间相对MDM降低65%（0.35x vs 1.0x）。规划线索为去噪过程提供了强先验，大幅减少所需采样步数。

![[assets/figures/papers/paper_list_l1667_COLLAGE_Collaborative_Human_Agent_Interaction_Generation_using_Hierarchi/figures/005_Figure_3.jpg]]
*Figure 3: Ablation Studies*

- **层次级别与码本大小**（Fig. 3(b)和Fig. 3(d)）：增加VQ-VAE层次级别和码本大小可提升潜空间解耦度（MIG分数上升），并在CORE-4D上提高R-Precision Top1。选择7-8个最相关潜码与规划线索关联可获得最佳性能（Fig. 3(a)），过多或过少均导致性能下降。

### 失败模式与局限性

尽管COLLAGE在定量指标上表现优异，仍存在以下不足：

1. **物理真实性不足**：模型仅使用穿透损失和接触损失作为软约束，缺乏显式物理建模，可能产生穿透或不自然接触。这源于扩散模型在潜空间中以数据驱动方式生成运动，无法保证动力学一致性。

2. **数据规模限制**：CORE-4D仅含998个序列，覆盖5类物体。模型可能偏向数据中的典型交互模式，对稀有交互或全新物体-场景组合的泛化性存疑。InterHuman数据集虽规模较大，但仅涉及双人交互，未包含人-物-人协同场景。

3. **不可编辑性**：当前方法不支持细粒度运动编辑和用户交互式修正。扩散模型以端到端方式生成完整序列，用户无法指定局部修改或约束。

4. **LLM依赖性**：规划线索的质量依赖于GPT-4，其知识可能偏窄或不适用于特定领域（如专业协作任务）。LLM生成的描述存在不准确或过于笼统的风险，可能误导后续生成。

### 公平性说明

所有基线方法均在同一框架下复现或适配，保证比较公平性。训练数据、评估协议和超参数搜索空间保持一致。但由于CORE-4D数据集规模较小，结果的统计显著性需要更大规模验证。

### 补充图表

![[assets/figures/papers/paper_list_l1667_COLLAGE_Collaborative_Human_Agent_Interaction_Generation_using_Hierarchi/figures/003_Table.jpg]]
*Table: I*

![[assets/figures/papers/paper_list_l1667_COLLAGE_Collaborative_Human_Agent_Interaction_Generation_using_Hierarchi/figures/004_Table.jpg]]
*Table: EXPERIMENTAL RESULTS AND ABLATION STUDIES FOR TEXT-CONDITIONED INTERACTION GENERATION ON THE CORE-4D AND INTERHUMAN DATASETS, WHERE ± INDICATES 95% CONFIDENCE INTERVAL AND → MEANS THE CLOSER THE BETTER. BOLD INDICATES BEST RESULTS. TABLE II*

![[assets/figures/papers/paper_list_l1667_COLLAGE_Collaborative_Human_Agent_Interaction_Generation_using_Hierarchi/figures/001_Figure_1.jpg]]
*Figure 1: Text to collaborative motion and generalized motion generation by COLLAGE, based on user-provided text prompts. In the top image, a simulated humanoid robot adapts to the 3D terrain features based on the input text from the human collaborator. In the bottom image, the two human agents collaborate to handle an object using LLM-based planning via our architecture*



## 定位与知识库关联

### 1. 技术脉络与基线关系

COLLAGE 处于**语言引导的协同运动生成**这一交叉地带，其技术基因可追溯至三条相互独立的脉络：

**脉络一：基于 VQ-VAE 的量化潜空间运动生成。** 以 **T2M-GPT**（Guo et al., ECCV 2022）为代表的工作将人体运动压缩为离散码本序列，再通过自回归 Transformer 在码本空间中生成。COLLAGE 继承了“先压缩、后生成”的两阶段范式，但做出了关键转向：（a）将单层 VQ-VAE 扩展为 6 层层级化架构，每层捕捉不同抽象粒度的运动特征；（b）放弃自回归先验，转而将各层潜码聚合为连续表示，直接输入扩散模型解码器。这一转向使得生成过程从逐帧自回归的累积误差中解放出来，同时保留了层级化潜空间提供的解耦表征能力。

**脉络二：扩散模型在人体运动生成中的应用。** **MDM**（Tevet et al., arXiv 2022）首次将去噪扩散概率模型引入运动生成，直接在原始运动数据空间执行扩散与去噪。COLLAGE 将扩散操作移至 VQ-VAE 学习到的潜空间，从而大幅压缩搜索维度并加速推断——实验证据表明，在 15 步 DDIM 采样下即可达到高质量生成，推断速度比 MDM 快约 65%（Fig. 3(c)）。此外，COLLAGE 的去噪网络在 U-Net 架构基础上引入 Motion Modeling Blocks（MM-Blocks），集成图注意力网络（GAT）与时序卷积网络（TCN），专门处理多人-多物交互的空间与时序依赖。

**脉络三：大语言模型辅助的运动理解与生成。** **MotionGPT**（Zhang et al., arXiv 2023）探索了将 LLM 与运动生成结合的可能性，但其方式更偏向于将运动视为“语言”进行统一建模。COLLAGE 对 LLM 的使用则定位在**层次化语义规划线索的生成**上：GPT-4 根据文本提示生成分层的规划描述，经 CLIP ViT-B/32 嵌入后，通过对比学习与 VQ-VAE 各层码本中的潜码建立关联。这些规划线索在扩散去噪过程中以交叉注意力方式注入，且通过时间依赖调制函数 $\gamma_l(t)$ 控制其影响力——高层语义线索在早期扩散步骤主导生成方向，低层细节线索在后期步骤精细调控。

**与直接竞品 InterGen 的对比。** **InterGen**（Wang et al., CVPR 2023）是专门面向文本条件多人交互生成的基线方法。在 InterHuman 数据集上，COLLAGE 的 R-Precision Top1 达到 0.383，FID 达到 0.778，均显著优于 InterGen（Table I right）。InterGen 未采用层级化潜空间或 LLM 规划引导，其生成过程缺乏对协同交互中多粒度语义的显式建模，这可能是性能差距的结构性原因。

### 2. 适用边界与核心局限

COLLAGE 的设计假设与实验条件划定了其当前的能力边界：

**数据依赖性边界。** CORE-4D 数据集仅包含 998 个运动序列，覆盖 5 个物体类别。模型的层级化 VQ-VAE 和关联对比学习均在该数据上训练，其对稀有交互模式或全新物体类别的泛化能力缺乏实证支撑。验证分析明确指出，模型可能偏向数据中的典型交互模式，对于训练分布外的协同场景（如户外环境、非常规物体操作）性能可能显著退化。

**物理合理性边界。** COLLAGE 未集成显式物理仿真，仅通过接触损失和速度平滑损失作为软约束来鼓励合理的交互。这意味着生成的运动可能出现穿透、不自然接触或违反物理常识的姿态。论文自身将此列为局限性，并指出集成物理仿真是未来的开放问题。

**交互控制粒度边界。** 当前方法不支持细粒度的运动编辑或用户交互式修正。用户只能通过文本提示间接影响生成结果，无法指定局部关节轨迹、接触时机或力交互参数。这限制了其在需要精确运动控制的场景（如机器人操作规划、康复训练评估）中的应用。

**LLM 规划质量边界。** 规划线索的质量完全依赖于 GPT-4 的知识与推理能力。当文本提示涉及特定领域知识（如专业运动技巧、特定工具操作规范）时，LLM 可能生成不准确或不完整的规划描述，进而误导运动生成。论文将此列为开放问题，并提出了“能否完全通过 LLM 推理学习协同规划而无需交互动作捕捉数据”的远期追问。

### 3. 消融实验揭示的结构性洞察

消融实验（Table I bottom）提供了关于各模块因果贡献的直接证据：

- **移除层级化 VQ-VAE**（退化为单层架构）导致 CORE-4D FID 从 6.890 升至 7.452，InterHuman FID 从 0.778 急剧升至 5.582。这表明层级化潜空间对于协同交互生成的质量至关重要，尤其在多人交互场景中，不同抽象层次的运动特征解耦是生成多样且协调运动的关键。
- **移除 LLM 引导**导致 R-Precision 显著下降，说明 LLM 提供的语义规划线索在文本-运动对齐中扮演不可替代的角色。
- **用固定权重替换时间依赖调制**同样导致 FID 升高，验证了“高层语义主导早期、低层细节主导后期”这一设计原则的有效性。
- Fig. 3(d) 显示，增加层级数量和码本大小可提升潜空间的解耦度（MIG 分数），进一步支持了层级化架构的合理性。

### 4. 开放问题与前瞻定位

论文自身提出的开放问题与当前技术趋势的交叉点，标示了 COLLAGE 的未来演化方向：

1. **物理仿真集成。** 如何将物理引擎或可微物理约束嵌入生成框架，在保持生成多样性的同时消除不自然交互，是通向真实世界应用（如机器人仿真训练）的关键一步。
2. **交互式运动编辑。** 在扩散模型的去噪过程中引入用户指定约束（如关键帧、接触点、关节轨迹），使 COLLAGE 从“开环生成”转向“人机协同创作”，将显著拓展其应用场景。
3. **大规模开放物体集泛化。** 突破 CORE-4D 的 5 类物体限制，需要探索零样本或少样本的物体表征迁移机制，或利用基础模型（如 3D 物体编码器）提供物体几何与功能先验。
4. **纯 LLM 驱动的协同规划。** 能否完全绕过交互动作捕捉数据，仅依靠 LLM 的推理能力与基础运动先验生成协同交互，这是一个激进但具有范式意义的方向——若成功，将彻底改变人-物交互数据采集的依赖格局。

**注意：** 论文未提供与更近期方法（如 2024 年后的扩散-Transformer 混合架构或基于视频生成模型的运动合成方法）的直接比较。若需评估 COLLAGE 在当前 SOTA 中的相对位置，建议手动检索 2024-2025 年间在 CORE-4D 或 InterHuman 基准上报告结果的后续工作。



## 原文 PDF

![[paperPDFs/arxiv_2024/COLLAGE_Collaborative_Human_Agent_Interaction_Generation_using_Hierarchical_Latent_Diffusion_and_Language_Models.pdf]]
