---
title: "DiffGrasp: Whole-Body Grasping Synthesis Guided by Object Motion Using a Diffusion Model"
type: paper
paper_level: A
venue: AAAI
year: 2025
pdf_ref: paperPDFs/AAAI_2025/DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a_Diffusion_Model.pdf
project_link: https://iscas3dv.github.io/DiffGrasp/
code_link: null
aliases:
- DiffGrasp
tags:
- AAAI_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将分阶段/分部件建模替换为单个条件扩散模型联合建模身体、双手与物体运动，并引入接触感知损失（接触感知重建损失与交互损失）以及推理阶段的三种数据驱动引导（抓取稳定性引导、手-物体接触引导、脚步穿透引导），从而实现了端到端的精细全身抓取序列生成。
primary_logic: 单一扩散模型足以捕捉高自由度全身姿态与物体运动之间的复杂联合分布；接触感知损失使网络在训练中就能感知物体空间位置并学习自然抓取姿态；推理阶段不必引入昂贵的显式接触损失训练，而是通过基于重建引导的轻量级优化即可大幅提升接触真实性与稳定性。
claims:
- DiffGrasp在GRAB数据集上的Hands JPE降低到20.99（vs OMOMO的31.28），F1分数提升至0.784（vs OMOMO的0.009），MPJPE和MPVPE也大幅领先，同时在ARCTIC数据集上同样全面超越所有OMOMO变体。
- 消融实验表明，增加接触感知重建损失可使所有指标显著提升，而接触感知交互损失进一步提升F1分数（0.5319 vs 0.3861）；加入三种引导后，最终模型达到最佳Hands JPE=20.99和F1=0.7840。
- 定性结果显示，DiffGrasp生成的抓取姿态更自然、穿透更少，而基线方法在物体远距离移动时难以保持抓取。
- GRAB 上 Hands JPE (cm) ↓ = 20.99
---

# DiffGrasp: Whole-Body Grasping Synthesis Guided by Object Motion Using a Diffusion Model

> [!tip] 核心洞察
> 单一扩散模型足以捕捉高自由度全身姿态与物体运动之间的复杂联合分布；接触感知损失使网络在训练中就能感知物体空间位置并学习自然抓取姿态；推理阶段不必引入昂贵的显式接触损失训练，而是通过基于重建引导的轻量级优化即可大幅提升接触真实性与稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiffGrasp：基于扩散模型与物体运动引导的全身抓取合成 |
| 英文题名 | DiffGrasp: Whole-Body Grasping Synthesis Guided by Object Motion Using a Diffusion Model |
| 会议/期刊 | AAAI 2025 |
| Links | [Project](https://iscas3dv.github.io/DiffGrasp/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DiffGrasp |
| Dataset | GRAB, ARCTIC |

> [!tip] 效果简介
> - GRAB 上，Hands JPE (cm) ↓ 20.99 vs 31.28 (OMOMO) (-10.29)；MPJPE (cm) ↓ 12.24 vs 17.57 (OMOMO) (-5.33)；MPVPE (cm) ↓ 10.09 vs 13.80 (OMOMO) (-3.71)。
> - ARCTIC 上，Hands JPE (cm) ↓ 19.96 vs 25.95 (OMOMO) (-5.99)；F1 score ↑ 0.8067 vs 0.0775 (OMOMO) (+0.7292)。

## 概要

**问题瓶颈**：现有全身抓取生成方法存在结构性割裂——以 **OMOMO**（Li et al., 2023）为代表的两阶段/三阶段管线（OMOMO-V2、OMOMO-V3）先预测手部位置再生成身体姿态，或分离身体与手指姿态建模，导致生成的抓取序列缺乏精细的手指-物体接触、时间连续性和身体-手部协调性；而单帧抓取方法（如COOP）则完全丢失运动时序。核心矛盾在于：高自由度全身姿态与物体运动之间的联合分布无法在分阶段框架中被有效捕捉。

**核心方法**：**DiffGrasp** 用一个**单阶段条件扩散模型**替代分阶段建模，联合预测全身SMPL-X参数与双手腕部相对于物体的平移量（Figure 2）。关键创新包括：（1）**接触感知损失函数**——接触感知重建损失利用接触标签加权手部关节与腕部的L2误差，接触感知交互损失以距离指数衰减权重优化手-物体空间关系，使网络在训练中就能感知物体位置并学习自然抓取姿态；（2）**推理阶段数据驱动引导**——基于重建引导的梯度优化（抓取稳定性引导、手-物体接触引导、脚步穿透引导），无需昂贵显式接触损失训练即可大幅提升接触真实性与稳定性。

**核心结论**：在GRAB数据集上，DiffGrasp将手部关节位置误差（Hands JPE）从OMOMO的31.28 cm降至**20.99 cm**，F1接触分数从0.009提升至**0.784**（Table 1）；在ARCTIC数据集上同样全面超越所有OMOMO变体。消融实验证实，接触感知重建损失是运动精度的主要驱动力，交互损失显著提升接触质量，三种推理引导进一步将综合性能推至最优（Table 2）。定性结果显示DiffGrasp生成的抓取姿态更自然、穿透更少（Figure 4）。

**方法定位**：DiffGrasp属于**条件扩散模型驱动的全身人体-物体交互生成**范式，与两阶段扩散管线（OMOMO系列）形成直接对比，同时区别于单帧抓取生成（COOP）和纯身体运动生成（IMoS）等方法。其技术路线体现了“联合建模替代分治建模”的设计哲学，并通过接触感知损失与推理引导的协同，在有限训练数据下实现了精细接触生成。



在虚拟现实、具身智能与人机交互等应用中，生成自然、真实的全身抓取运动序列是一个关键且极具挑战的问题。理想的抓取生成系统需要同时满足三个层面的要求：**时间连续性**（运动序列在时序上平滑连贯）、**接触真实性**（手部与物体之间形成精确且稳定的接触）以及**身体-手部协调性**（身体姿态与双手动作在空间上协调一致）。

现有方法在这三个维度上存在结构性缺陷。以 **OMOMO**（Li et al., 2023）为代表的两阶段方法将生成过程拆解为“先预测手部位置，再生成全身姿态”的流水线——其后续变体 OMOMO-V2 和 OMOMO-V3 虽分别扩展了手部姿态输出和独立的手部姿态预测网络，但本质上仍是分阶段、分部件的分离建模范式。这种设计导致两个核心问题：其一，身体与双手的运动分布在训练中被割裂，模型无法捕捉两者之间的联合依赖关系，生成的抓取序列在身体-手部协调性上表现薄弱；其二，OMOMO 系列方法**完全忽略手指姿态的建模**，仅输出手部全局位置而缺乏精细的手指-物体接触，使得生成的抓取在接触真实性上严重不足——在 GRAB 数据集上，OMOMO 的 F1 分数仅为 0.0090，几乎无法形成有效接触。另一类方法如 **COOP** 则聚焦于单帧静态抓取姿态生成，在给定物体运动序列的条件下缺乏时间连续性，无法直接应用于动态抓取场景。

上述方法暴露出的根本瓶颈在于：**现有框架无法在统一模型内同时建模身体与双手在两个空间尺度（全身尺度与手指尺度）上的复杂运动**，导致生成的抓取序列在时间连续性、接触真实性和身体-手部协调性三者之间难以兼得。

针对这一瓶颈，**DiffGrasp** 提出了一种根本性的范式转换：将分阶段/分部件的建模策略替换为**单个条件扩散模型联合建模身体、双手与物体运动**。其核心洞察在于，单一扩散模型足以捕捉高自由度全身姿态与物体运动之间的复杂联合分布，从而在端到端的框架内一次性生成包含精细手指姿态的全身抓取序列。这一设计从结构上消除了分离建模带来的信息割裂问题，为同时实现时间连续性、接触真实性与身体-手部协调性提供了统一的生成基础。



## 核心方法与创新机理

DiffGrasp 的核心创新在于将此前分离建模的全身运动与精细手指抓取统一到**单一条件扩散模型**中，并围绕这一统一框架设计了训练和推理两阶段的接触感知机制，从而在保持时间连续性的同时大幅提升手-物体接触的真实性与稳定性。

### 1. 从多阶段分离建模到单阶段联合生成

现有方法在处理全身抓取任务时普遍采用分阶段或分部件的策略。主要基线 **OMOMO**（Li et al., 2023）采用两阶段条件扩散模型：第一阶段生成手部位置，第二阶段基于手部位置生成全身姿态，且完全不包含手指姿态。其扩展版本 OMOMO-V2 在第二阶段额外输出手部姿态参数，而 OMOMO-V3 则进一步增加一个网络根据物体运动轨迹和手部位置预测手部姿态，形成三阶段流水线。这些方法的共同缺陷在于，身体运动与精细手部姿态的生成被割裂为不同的子问题，导致模型无法捕捉身体-双手-物体三者之间的联合分布，生成的抓取序列缺乏内在协调性。

DiffGrasp 的**建模管线**发生了根本性改变：以单阶段条件扩散模型同时预测全身 SMPL-X 参数（包括身体姿态、双手姿态和全局位移）以及双手腕部相对于物体的平移量 $\kappa$，一次性生成所有运动参数。这一设计使模型能够直接学习高维人体-物体运动空间中的联合分布 $p(\mathbf{H}, \kappa \mid \text{condition})$，从根源上消除了分离建模带来的信息割裂。

### 2. 接触感知损失函数的设计

仅使用标准扩散重建损失 $\mathcal{L}_{diff}$ 训练的统一模型虽然能生成合理的全身运动，但手部与物体的空间关系仍然松散——这是高自由度姿态空间中扩散模型难以仅凭 MSE 损失精确捕捉接触细节的瓶颈所在。

DiffGrasp 在训练阶段引入了两类**接触感知损失**：

- **接触感知重建损失** $\mathcal{L}_{recon}$：利用数据集中提供的接触标签 $\tau$ 对发生接触的手施加加权的 L2 损失，同时监督手部关节位置 $\hat{J}$ 和腕部世界坐标 $\hat{v}$。这迫使网络在训练中感知物体的空间位置，学习将手部精确放置在物体附近。

- **接触感知交互损失** $\mathcal{L}_{inter}$：基于距离指数衰减的权重 $w_k = \tau \exp(-\alpha \cdot d(J_k, O_m))$，对靠近物体的手部关节施加更强的距离监督，鼓励网络建立手-物体之间的空间关系。

消融实验（Table 2）揭示了这两类损失的作用机制：在仅使用扩散损失时，F1 分数仅为 0.3861；加入接触感知重建损失后，F1 提升至 0.5319，同时 Hands JPE 从 25.80 降至 22.35；进一步加入交互损失后，F1 在仅含损失的变体中达到最高的 0.5543。这表明重建损失主要改善运动精度，而交互损失则专门促进手-物体接触的形成。

### 3. 数据驱动的推理阶段引导

传统方法若要在推理时优化接触质量，通常需要训练显式的接触损失函数，计算代价高昂且泛化性受限。DiffGrasp 的核心洞察在于：**推理阶段不必引入昂贵的显式接触损失训练，而是可以通过基于重建引导的轻量级梯度优化大幅提升接触真实性与稳定性**。

具体而言，在扩散采样的每一步，模型利用预测的干净数据 $\hat{x}_0$ 计算三种引导目标函数的梯度，并通过 $\tilde{x}_0 = \hat{x}_0 - \eta \Sigma_n \nabla_{\hat{x}_n} \mathcal{G}(\hat{x}_0)$ 进行修正：

- **抓取稳定性引导** $\mathcal{G}_{GS}$：在接触段内，将初始帧的腕部相对位置根据物体旋转和平移变换到后续帧，消除因物体运动导致的腕部滑动，确保抓取在时序上保持稳定。

- **手-物体接触引导** $\mathcal{G}_{HO} = \lambda_{ho} D_{pene} + (1 - \lambda_{ho}) D_{cont}$：同时惩罚手部顶点穿透物体内部（通过负的有符号距离 $D_{pene}$ 度量）和鼓励接触手顶点贴近物体表面（通过 $D_{cont}$ 度量），在减少穿透的同时增强接触。

- **脚步穿透引导** $\mathcal{G}_{Feet}$：惩罚身体顶点穿越地面（$z < 0$），提升全身姿态的物理合理性。

消融实验证实，在完整损失函数基础上加入三种引导后（即最终 DiffGrasp 模型），Hands JPE 降至 20.99，F1 达到 0.7840，均显著优于仅使用损失的变体。定性结果（Figure 4）进一步显示，引导后的抓取姿态更自然，手部穿透明显减少，而基线方法在物体远距离移动时难以保持抓取。

### 4. 创新点之间的关系

上述三个创新点构成了一个递进的因果链条：**统一扩散模型**提供了学习全身-物体联合分布的基础能力；**接触感知损失**在训练阶段将物体的空间信息注入网络，使其初步具备感知接触的能力；**推理阶段引导**则在不增加训练负担的前提下，对生成结果进行轻量级优化，弥补扩散模型在接触细节上的不足。三者共同作用，使 DiffGrasp 在 GRAB 数据集上将 Hands JPE 从 OMOMO 的 31.28 降至 20.99，F1 分数从 0.0090 提升至 0.7840，实现了全身抓取合成性能的跨越式提升。



DiffGrasp 的核心设计是将“身体运动—双手抓取—物体运动”三个高自由度组件统一在一个条件扩散模型内联合建模，替代以往方法中分阶段、分部件的预测管线。整体管线由**条件编码、Transformer 去噪、SMPL‑X 重建和推理阶段引导**四个模块串联而成，形成端到端的全身抓取序列生成框架（Figure 2）。

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/002_Figure_2.jpg]]
*Figure 2: Overview of DiffGrasp Framework. In our conditional diffusion model, we use the given sequence of object motion, object shape and the SMPL-X identity as conditions. After specially designed positional encodings, these embedded conditions are inputted into a transformer-encoder-based condition encoder. Then, a transformer decoder as denoising network predicts a sequence of clean whole-body pose of SMPL-X as well as the wrist joints translations relative to the object centroid. During the inference stage, we reconstruct the SMPL-X pose sequence into a human mesh sequence. Based on carefully designed guidance functions, we control and optimize our predicted results for more stable hand grasping*

### 输入与条件构造

模型接收三类条件输入：**物体运动序列**（各帧的 6‑DoF 刚体变换）、**物体形状**（通过 Basis Point Set 编码为 256 维特征）以及**人体身份**（SMPL‑X 的体型参数）。三者分别经三个 MLP 映射为等长的 256 维特征向量，再与逐帧位置编码和分部分位置编码相加，构成条件序列 $c_{\text{raw}}$。分部分位置编码 $PE^p$ 是本文引入的关键设计，它使 Transformer 能够区分不同条件部分（物体形状、物体运动、人体身份）以及帧内位置，从而提升条件理解能力（消融实验表明移除 $PE^p$ 会导致几乎所有指标轻微下降，Table 2）。

### 条件编码器（Transformer Encoder）

条件序列 $c_{\text{raw}}$ 送入一个 8 层 Transformer‑Encoder 作为条件编码器，输出紧凑的条件特征 $c$。该编码器的作用是将多源条件信息融合为去噪网络可高效利用的上下文表示。

### 去噪网络（Transformer Decoder）

去噪网络采用 8 层 Transformer‑Decoder，其输入包括：噪声数据 $x_n$（对干净全身运动数据 $x_0$ 按扩散调度加噪得到）、噪声步 $n$ 以及条件特征 $c$。去噪网络直接预测干净数据 $\hat{x}_0$，该数据包含两大部分：

1. **全身姿态参数** $H$：基于 SMPL‑X 模型，包括全局平移、根关节旋转以及身体各关节的 6D 连续旋转表示。
2. **双手腕部相对平移** $\kappa$：左右手腕相对于物体质心的平移向量，用于在物体运动过程中保持手‑物体的空间关系。

这种“一次性输出全身姿态 + 腕部相对位移”的设计，是 DiffGrasp 区别于两阶段基线（如 OMOMO 先预测手部位置再生成身体姿态）的结构性改变。

### SMPL‑X 重建与接触感知损失

根据预测的 SMPL‑X 参数 $\hat{H}$ 和腕部平移 $\hat{\kappa}$，通过 SMPL‑X 前向过程重建全身网格，并从中提取双手关节位置 $\hat{J}$ 及腕部世界坐标 $\hat{v}$。这些几何量直接参与两类接触感知损失的计算：

- **接触感知重建损失** $\mathcal{L}_{\text{recon}}$：利用接触标签 $\tau$ 加权，仅在发生接触的手上施加手部关节和腕部位置的 L2 损失，迫使网络在接触阶段精确重建手‑物体空间关系。
- **接触感知交互损失** $\mathcal{L}_{\text{inter}}$：以指数衰减的距离权重 $w_k$ 对每个手部关节到物体质心的距离误差进行加权，使网络对靠近物体的关节更加敏感，从而主动学习手‑物体接近行为。

训练总损失为扩散损失 $\mathcal{L}_{\text{diff}}$、$\mathcal{L}_{\text{recon}}$ 和 $\mathcal{L}_{\text{inter}}$ 的加权和（Eq. 8）。消融实验证实，加入 $\mathcal{L}_{\text{recon}}$ 后 F1 分数从 0.3861 跃升至 0.5319，而 $\mathcal{L}_{\text{inter}}$ 在所有仅含损失的变体中取得最高 F1（0.5543），表明两者分别从空间精度和接触激励两个角度互补地提升抓取质量（Table 2）。

### 推理阶段引导

推理采样过程中，DiffGrasp 在每一步去噪后对预测的 $\hat{x}_0$ 施加基于梯度的重建引导，无需额外训练。引导由三项组成：

- **抓取稳定性引导** $\mathcal{G}_{\text{GS}}$：将接触段初始帧的腕部相对位置根据物体旋转和平移变换到后续各帧，修正因物体运动导致的腕部滑动。
- **手‑物体接触引导** $\mathcal{G}_{\text{HO}}$：在采样率最高的手部顶点上同时惩罚穿透（负 SDF 值之和）并鼓励接触（绝对 SDF 值之和），以 $\lambda_{ho}$ 平衡两者。
- **脚步穿透引导** $\mathcal{G}_{\text{Feet}}$：惩罚身体顶点穿越地面（$z<0$），使生成结果保持脚‑地面接触。

三者组合 $\mathcal{G} = \mathcal{G}_{\text{Feet}} + \mathcal{G}_{\text{GS}} + \mathcal{G}_{\text{HO}}$ 通过梯度下降优化 $\hat{x}_0$，实现轻量级但效果显著的推理时修正。最终模型（Full loss + Guidance）在 GRAB 上取得 Hands JPE 20.99 cm、F1 0.7840 的综合最优结果（Table 2）。

### 数据流总结

整体数据流可概括为：**物体运动/形状/人体身份 → 条件编码 → Transformer 去噪预测全身姿态与腕部平移 → SMPL‑X 重建 → 接触感知损失监督训练 + 推理引导优化**。这一闭环设计使 DiffGrasp 能够在一个统一的扩散框架内同时捕捉身体运动、双手精细操作和物体运动之间的复杂联合分布，从而生成具有时间连续性、接触真实性和身体‑手部协调性的全身抓取序列。

### 补充图表




DiffGrasp 将全身抓取序列生成建模为一个**条件扩散模型**，其核心由三个功能模块构成：条件编码器、Transformer 去噪器以及推理阶段的三种数据驱动引导。整个框架以统一的扩散过程一次性预测全身 SMPL-X 姿态参数和双手腕部相对物体的平移量，从而替代传统方法的多阶段分离建模。

### 条件编码

模型接收三类条件输入：物体运动序列、物体形状表示和人体身份。物体形状通过 Basis Point Set（BPS）编码器映射为 256 维特征，物体运动和人体身份则分别由两个 MLP 映射为等长特征。为增强条件的时间与语义区分，作者引入了**逐帧位置编码**与**分部分位置编码**的组合，使网络能更精细地感知不同帧和不同条件部分。编码后的条件序列经 8 层 Transformer 编码器压缩为条件特征 $c$，供后续去噪过程使用。

### 扩散过程与去噪网络

前向扩散过程遵循标准 DDPM 形式，逐步向干净数据 $x_0$ 注入高斯噪声：

$$q(x_n | x_{n-1}) = \mathcal{N}(x_n; \sqrt{1-\beta_n} x_{n-1}, \beta_n I) \tag{1}$$

其中 $\beta_n$ 为固定方差调度。反向过程由一个 8 层 Transformer 解码器作为去噪网络 $f_\theta$，以噪声数据 $x_n$、噪声步 $n$ 和条件 $c$ 为输入，直接预测干净数据 $\hat{x}_0$（包含全身姿态 $H$ 和双手腕部相对平移 $\kappa$）。训练目标为预测值与真实值的均方误差：

$$\mathcal{L}_{diff} = \mathbb{E}_{n \sim [1,N]} \| f_\theta(x_n, n, c) - x_0 \|_2^2 \tag{4}$$

### 接触感知损失函数

为引导网络学习精细的手-物体空间关系，DiffGrasp 在扩散损失之上引入两个关键损失项。

**接触感知重建损失**利用接触标签 $\tau$ 加权，仅在发生接触的手上施加手部关节和腕部位置的 L2 损失：

$$\mathcal{L}_{recon} = \tau_0(\| J_l - \hat{J}_l \|_2 + \lambda_{wrist} \| v_l - \hat{v}_l \|_2) + \tau_1(\| J_r - \hat{J}_r \|_2 + \lambda_{wrist} \| v_r - \hat{v}_r \|_2) \tag{5}$$

其中 $J_l, J_r$ 为左右手关节位置，$v_l, v_r$ 为腕部世界坐标。该损失使网络在训练中即能感知物体空间位置，从而生成更准确的手部姿态。

**接触感知交互损失**通过指数衰减权重放大靠近物体的关节的重要性：

$$w_k = \tau \exp(-\alpha \cdot d(J_k, O_m)) \tag{6}$$

其中 $d(J_k, O_m)$ 为关节 $J_k$ 到物体质心的欧氏距离。最终交互损失为加权的手-物体距离误差：

$$\mathcal{L}_{inter} = \sum_{k=1}^{K} w_k \| d(\hat{J}_k, O_m) - d(J_k, O_m) \|_2 \tag{7}$$

总训练损失为三项的加权和：

$$\mathcal{L} = \lambda_{diff} \mathcal{L}_{diff} + \lambda_{recon} \mathcal{L}_{recon} + \lambda_{inter} \mathcal{L}_{inter} \tag{8}$$

### 推理阶段引导

推理阶段通过**重建引导**对预测的干净数据 $\hat{x}_0$ 进行梯度优化，无需额外训练：

$$\tilde{x}_0 = \hat{x}_0 - \eta \Sigma_n \nabla_{\hat{x}_n} \mathcal{G}(\hat{x}_0) \tag{9}$$

其中 $\mathcal{G}$ 为引导目标函数，$\eta$ 为学习率。DiffGrasp 设计了三种引导：

- **抓取稳定性引导** $\mathcal{G}_{GS}$：在接触段内将初始帧的腕部相对位置根据物体旋转平移变换到后续帧，消除相对滑动，优化腕部位置使其贴合修正后的轨迹。
- **手-物体接触引导** $\mathcal{G}_{HO}$：对高接触率的手部采样顶点计算穿透距离 $D_{pene}$ 和接触距离 $D_{cont}$，同时惩罚穿透并鼓励接触。
- **脚步穿透引导** $\mathcal{G}_{Feet}$：惩罚身体顶点穿越地面（$z<0$），保证脚-地面接触。

三种引导组合使用：$\mathcal{G} = \mathcal{G}_{Feet} + \mathcal{G}_{GS} + \mathcal{G}_{HO}$。消融实验证实，加入引导后模型在 Hands JPE、F1 等综合指标上达到最优（Table 2），且定性上姿态更自然、穿透更少。

### 补充图表

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of Grasp Stabilization Guidance*



## 实验与关键发现

### 实验设置与评估协议

DiffGrasp在两个主要的全身抓取数据集上进行评估：**GRAB**（Taheri et al. 2020）和**ARCTIC**（Fan et al. 2023）。评估采用基于受试者（subject-based）的数据划分，所有方法使用相同的输入条件（物体运动序列、BPS形状表示、人体身份），并采用统一的训练归一化流程，确保公平比较。模型参数量处于可比范围：DiffGrasp为33.0M，OMOMO为23.5M，OMOMO-V2为23.9M，OMOMO-V3为36.2M，未使用不公平的额外参数优势。

评估指标覆盖运动精度、接触质量和物理合理性三个维度：
- **运动精度**：Hands JPE（双手关节位置误差，cm）、MPJPE（平均关节位置误差，cm）、MPVPE（平均顶点位置误差，cm）
- **接触质量**：F1 score（接触分类F1，阈值5mm）、Contact distance（接触距离，cm）
- **物理合理性**：Foot sliding（脚步滑动，cm）、Collision %（手-物体穿透比例）、Collision depth（穿透深度，cm）

基线方法OMOMO系列未使用其原始论文中的接触后处理（防止后续释放），因为该后处理会与包含释放和换手动作的训练数据冲突，避免了对基线的不利影响。

### 主要定量结果

**Table 1** 展示了DiffGrasp与OMOMO系列变体在GRAB和ARCTIC数据集上的全面对比。在GRAB数据集上，DiffGrasp在所有指标上均大幅领先：

| 指标 | DiffGrasp | OMOMO | 提升幅度 |
|------|-----------|-------|----------|
| Hands JPE (cm) ↓ | 20.99 | 31.28 | -32.9% |
| MPJPE (cm) ↓ | 12.24 | 17.57 | -30.3% |
| MPVPE (cm) ↓ | 10.09 | 13.80 | -26.9% |
| F1 score ↑ | 0.7840 | 0.0090 | +86.1倍 |
| Cont. distance (cm) ↓ | 0.04 | 0.19 | -78.9% |

这一对比揭示了当前领域的一个核心瓶颈：OMOMO虽然能够生成全身运动序列，但其F1分数仅为0.0090，表明该方法几乎无法建立有效的手-物体接触。DiffGrasp通过单一扩散模型联合建模身体、双手与物体运动，配合接触感知损失和推理引导，将F1提升至0.7840，实现了质的飞跃。接触距离从0.19cm降至0.04cm，表明生成的抓取姿态不仅接触更准确，而且穿透更少。

在ARCTIC数据集上，DiffGrasp同样全面超越所有OMOMO变体：Hands JPE降至19.96（vs OMOMO的25.95），F1达到0.8067（vs OMOMO的0.0775），验证了方法的跨数据集泛化能力。

### 消融实验：损失函数的关键作用

**Table 2** 系统消融了损失函数组件、位置编码和推理引导的贡献，揭示了接触感知设计的因果机制：

**接触感知重建损失（Contact-aware Reconstruction Loss）** 是运动精度提升的关键驱动力。从基线（Full loss w/o Inter and Recon）到仅添加接触感知重建损失（Full loss w/o Inter），Hands JPE从25.80降至22.35（-13.4%），MPJPE从14.69降至13.03，F1从0.3861提升至0.5319。值得注意的是，若使用不包含接触标签加权的简单重建损失（Full loss w/o Inter w/ Simp Recon），F1仅能达到0.4861，低于接触感知版本的0.5319，证明接触标签τ的加权机制使网络在训练中就能感知物体空间位置，从而学习更精确的手部定位。

**接触感知交互损失（Contact-aware Interaction Loss）** 是接触真实性的主要推动力。仅含交互损失的变体（Full loss w/o Recon）在所有仅含损失的配置中取得最高F1分数0.5543，显著高于仅含重建损失的0.5319。这表明指数衰减的距离感知权重$w_k = \tau \exp(-\alpha \cdot d(J_k, O_m))$有效引导网络关注靠近物体的手部关节，促进手-物体空间关系的学习。然而，交互损失单独使用时运动精度指标（Hands JPE=24.37）不如重建损失，说明两者存在互补关系。

**完整损失函数**（Full loss）结合两者优势，在运动精度和接触质量间取得平衡：Hands JPE=22.44，F1=0.5319。移除分部分位置编码PE^P后几乎所有指标轻微下降，表明该设计帮助网络更好地理解输入条件的帧级和部件级结构。

### 推理引导的叠加效应

在完整损失函数基础上叠加三种数据驱动引导（DiffGrasp最终模型）带来进一步的全面提升：
- Hands JPE从22.44降至20.99（-6.5%）
- F1从0.5319跃升至0.7840（+47.4%）
- Contact distance从0.07降至0.04

这一结果验证了核心洞察：推理阶段不必引入昂贵的显式接触损失训练，而是通过基于重建引导的轻量级优化即可大幅提升接触真实性与稳定性。抓取稳定性引导$G_{GS}$修正了腕部相对物体的滑动，手-物体接触引导$G_{HO}$同时惩罚穿透并鼓励接触，脚步穿透引导$G_{Feet}$确保脚-地面接触。三种引导的梯度通过$\tilde{x}_0 = \hat{x}_0 - \eta \Sigma_n \nabla_{\hat{x}_n} \mathcal{G}(\hat{x}_0)$迭代优化预测的干净数据，无需重新训练网络。

### 定性分析与泛化能力

**Figure 4** 的定性对比显示，DiffGrasp生成的抓取姿态更自然、手-物体接触更丰富、穿透更少，而基线方法在物体远距离移动时难以保持抓取（**Figure A13**）。**Figure 5** 的消融定性结果进一步可视化损失函数的影响：仅含扩散损失的模型手部位置模糊且缺乏接触，逐步添加重建损失和交互损失后，手部逐渐靠近物体并形成合理抓取姿态。

在泛化能力方面，**Table A3** 展示了在未见物体和未见人体身份上的对比结果，DiffGrasp同样保持领先。**Figure A11** 的定性结果显示DiffGrasp对未见物体（不同尺寸和形状）展现出强泛化能力，同时保持全身协调性。**Figure A10** 的人类主观感知研究进一步验证了DiffGrasp生成序列在自然度和接触真实性上获得最高评分。

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/012_Table_1.jpg]]
*Table 1: Table A3: Comparison on GRAB (Taheri et al. 2020) dataset with unseen objects and unseen human identities. The experimental results of unseen human identities are from the Table 1 in the main paper*

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/013_Figure.jpg]]
*Figure: A10: Results of Human Perceptual Study. Comparing with OMOMO and our ablation study, DiffGrasp can generate the grasp sequences with the highest score*

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/014_Figure.jpg]]
*Figure: A11: Qualitative results of unseen objects. Our method (DiffGrasp) demonstrates strong generalization in grasping unseen objects of various sizes and shapes, while also exhibiting excellent full-body coordination*

### 失败模式与局限性

尽管DiffGrasp在定量和定性上均大幅领先基线，仍存在以下失败模式（**Figure 6**）：

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/008_Figure_6.jpg]]
*Figure 6: Limitations. Our method may generate selfpenetration (a) or unrealistic poses (b) in some cases*

1. **人体网格自穿透**：生成结果中可能出现手部穿透身体其他部位的情况。当前引导策略仅约束手-物体接触和脚-地面穿透，缺乏人体自穿透约束。
2. **不真实抓取姿态**：部分情况下手部或手指姿态扭曲，不符合物理合理性。这源于训练数据中缺乏显式的物理约束（如力反馈、稳定性条件）。
3. **身体位移受限**：受现有数据集限制（GRAB和ARCTIC中抓取动作以站立/坐姿为主），DiffGrasp无法在抓取过程中生成行走等大范围身体位移，生成的人体姿态趋向于静态。这一局限性是数据驱动的固有瓶颈，而非方法设计缺陷。

这些失败模式指出了未来工作的方向：如何在推理引导中引入人体自穿透约束，以及如何将物理约束显式纳入训练或引导流程。

### 补充图表

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/004_Table_1.jpg]]
*Table 1: Comparative experimental results on GRAB (Taheri et al. 2020) dataset and ARCTIC (Fan et al. 2023) dataset*

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Results of Comparison Experiments. Our model (DiffGrasp) generates more realistic results, with more hand-object contact and less penetration*

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/006_Table_2.jpg]]
*Table 2: Ablation study results on GRAB (Taheri et al. 2020) dataset*

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative Results of Ablation Study. In this figure, Full is the abbreviation for Full loss, R. is the abbreviation for Recon, and I. is the abbreviation for Inter*

![[assets/figures/papers/paper_list_l1663_DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a/figures/016_Figure.jpg]]
*Figure: A13: Comparison of the ability of different methods to adapt to large movements of objects. Our model (DiffGrasp) can generate more realistic results. The results in this figure are similar to those in Figure S6, highlighting the importance of our proposed two contact-aware loss terms. Additionally, the comparison shows that OMOMOs struggles to grasp objects that are out of reach*



## 定位与知识库关联

### 1. 问题定位：全身抓取合成中的“两级尺度鸿沟”

全身抓取合成（whole-body grasping synthesis）面临一个核心瓶颈：人体运动包含身体级的大范围位移（米级）与手指级的精细接触（毫米级），这两级空间尺度在现有方法中被割裂处理。一方面，全身运动生成方法（如 **OMOMO** 系列，Li et al., 2023）能生成连贯的身体运动序列，但缺乏精细的手指-物体接触建模，导致生成的抓取在接触真实性上严重不足——在 GRAB 数据集上，OMOMO 的 F1 分数仅为 0.0090（Table 1），几乎无法形成有效接触。另一方面，静态抓取生成方法（如 **COOP**）虽能生成单帧的精细手指姿态，但缺乏时间连续性，无法适应物体运动序列条件下的动态抓取需求（Figure A7 显示 COOP 结果缺乏时间连续性，红色虚线框标注了不真实且不连续的抓取结果）。

DiffGrasp 的定位正是在此鸿沟上：**首次在单一条件扩散模型框架内联合建模身体、双手与物体运动**，同时解决时间连续性与接触精细度两个问题。

### 2. 与基线方法的结构性差异

#### 2.1 OMOMO 系列：分阶段建模的局限性

OMOMO（Li et al., 2023）及其变体构成了 DiffGrasp 的主要对比基线，其共同特征是将全身抓取分解为多个阶段：

| 基线方法 | 管线结构 | 关键局限 |
|---------|---------|---------|
| **OMOMO** | 两阶段：第一阶段生成手部位置 → 第二阶段基于手部位置生成全身姿态（不含手指姿态） | 手指姿态完全缺失；手部位置预测与全身姿态生成分离，无法端到端优化接触质量 |
| **OMOMO-V2** | 两阶段扩展：在第二阶段额外输出手部姿态参数 | 仍为分离建模，手指姿态与身体运动缺乏联合约束 |
| **OMOMO-V3** | 三阶段流水线：增加独立网络根据物体轨迹、BPS 表示和手部位置预测手部姿态 | 管线更长但非统一建模，各阶段误差累积 |

这种分阶段策略的深层问题是：**手部位置预测与最终抓取质量之间缺乏梯度通路**。第一阶段的手部位置误差会在后续阶段中被放大，且无法通过接触感知的信号反向优化手部位置生成。

#### 2.2 DiffGrasp 的统一建模策略

DiffGrasp 的核心结构变革是将上述多阶段管线替换为**单阶段条件扩散模型**（Figure 2）：Transformer 解码器以噪声数据 $x_n$、噪声步 $n$ 和条件 $c$ 为输入，直接预测干净数据 $x_0$，其中 $x_0$ 同时包含全身 SMPL-X 姿态参数 $H$ 和双手腕部相对物体的平移量 $\kappa$。这一设计使身体运动、手部位置和手指姿态在统一的生成过程中相互约束。

从方法谱系看，DiffGrasp 的工作属于“**条件扩散模型 + 接触感知损失 + 推理引导**”的技术路线，其关键创新点可分解为三个层面：

1. **建模层面**：将分阶段/分部件建模替换为单一扩散模型联合建模（changed_slot: 建模管线）
2. **训练层面**：引入接触感知重建损失（Eq. 5）和接触感知交互损失（Eq. 7），使网络在训练中感知物体空间位置（changed_slot: 损失函数）
3. **推理层面**：引入三种数据驱动引导——抓取稳定性引导 $G_{GS}$（Eq. 11）、手-物体接触引导 $G_{HO}$（Eq. 15）和脚步穿透引导 $G_{Feet}$（Eq. 17），通过重建引导（Eq. 9）在推理采样过程中迭代优化预测的 $x_0$（changed_slot: 推理优化）

### 3. 关键设计决策的消融证据

Table 2 的消融实验清晰揭示了各组件的作用机制：

**接触感知重建损失的核心作用**：从“Full loss w/o Inter and Recon”（仅扩散损失）到“Full loss w/o Inter”（增加接触感知重建损失），Hands JPE 从 25.80 降至 22.35，F1 从 0.3861 升至 0.5319。这表明**接触标签加权的关节位置监督**是提升手部空间精度的关键——该损失仅在接触发生的手上施加（通过 $\tau_0$、$\tau_1$ 二值标签），迫使网络在接触段内精确建模手部相对于物体的位置。

**接触感知交互损失的互补作用**：“Full loss w/o Recon”（仅含交互损失）在仅含损失的变体中取得最高 F1（0.5543），证明指数衰减的距离感知权重 $w_k = \tau \exp(-\alpha \cdot d(J_k, O_m))$（Eq. 6）能有效促进手-物体接触。该损失不直接监督关节位置，而是监督手部各关节到物体质心的距离，使网络学习手-物体空间关系的整体模式。

**推理引导的增益叠加**：在完整损失基础上加入三种引导后（DiffGrasp），模型达到综合最优（Hands JPE=20.99, F1=0.7840）。这验证了论文的核心洞察：**推理阶段不必引入昂贵的显式接触损失训练，而是通过基于重建引导的轻量级优化即可大幅提升接触真实性与稳定性**。

### 4. 适用边界与泛化能力

#### 4.1 已验证的泛化能力

- **跨数据集泛化**：DiffGrasp 在 GRAB 和 ARCTIC 两个数据集上均全面超越所有 OMOMO 变体（Table 1），在 ARCTIC 上 Hands JPE=19.96（vs OMOMO 25.95），F1=0.8067（vs OMOMO 0.0775）
- **未见物体泛化**：Table A3 和 Figure A11 显示 DiffGrasp 对未见物体具有强泛化能力，能抓取不同尺寸和形状的物体
- **未见人体身份泛化**：Table A3 同时验证了对未见人体身份的泛化能力

#### 4.2 已知局限

1. **人体自穿透**：DiffGrasp 仍可能生成手部穿透身体其他部位的自穿透结果（Figure 6a），这是因为当前引导策略仅约束手-物体接触和脚步-地面接触，未引入人体自穿透约束
2. **不真实抓取姿态**：部分情况下生成的手部或手指姿态扭曲（Figure 6b），表明物理约束（如力反馈、稳定性条件）的缺失
3. **身体位移受限**：受现有数据集限制（GRAB 和 ARCTIC 中缺乏行走抓取样本），DiffGrasp 生成的全身姿态趋向于静态，无法在抓取过程中生成行走等大范围身体位移
4. **引导策略的手工设定**：当前三种引导的学习率、迭代次数等超参数为手工设定，缺乏自适应学习机制

### 5. 在知识库中的定位与开放问题

DiffGrasp 在全身抓取合成领域占据“**统一条件扩散模型**”这一方法节点，其技术贡献可归纳为：证明了单一扩散模型足以捕捉高自由度全身姿态与物体运动之间的复杂联合分布，且接触感知损失与推理引导的组合是实现精细接触的有效路径。

以下开放问题定义了该方向的后续研究空间：

1. **人体自穿透约束**：如何在推理引导中引入人体自穿透约束（如身体各部位的 SDF 检测），避免手部穿透身体？
2. **物理合理性**：如何将物理约束（力反馈、抓取稳定性条件）显式纳入训练或引导，以避免不真实抓取姿态？
3. **动态身体位移**：如何在现有数据集缺乏行走抓取样本的条件下，使模型泛化到同时包含行走的抓取序列？可能需要数据增强或物理仿真辅助
4. **极端形状泛化**：DiffGrasp 对未见物体的泛化已初步验证，但如何进一步增强对形状差异极大物体（如极薄、极不规则物体）的鲁棒性？
5. **自适应引导**：当前引导策略的高度手工设定（学习率、迭代次数）能否由网络自适应学习，减少人工调参负担？

**注**：本文未提供具体的会议/期刊发表信息（venue 和 year 均为 null），上述方法定位基于论文内容本身的技术分析。



## 原文 PDF

![[paperPDFs/AAAI_2025/DiffGrasp_Whole_Body_Grasping_Synthesis_Guided_by_Object_Motion_Using_a_Diffusion_Model.pdf]]
