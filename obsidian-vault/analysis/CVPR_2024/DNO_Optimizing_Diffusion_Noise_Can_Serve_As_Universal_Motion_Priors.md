---
title: "DNO: Optimizing Diffusion Noise Can Serve As Universal Motion Priors"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/DNO_Optimizing_Diffusion_Noise_Can_Serve_As_Universal_Motion_Priors.pdf
project_link: https://korrawe.github.io/dno-project/
code_link: null
aliases:
- DNOD
- DNO
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 扩散模型的初始噪声向量 x_T（即扩散过程的起点）。通过优化该噪声向量并利用预训练去噪模型，可以控制生成的运动以满足任意可微的目标函数。
primary_logic: 将运动生成视为一个在预训练扩散模型潜在空间中的优化问题：在扩散噪声 x_T 上执行梯度下降，通过反向传播整个 ODE 求解器来直接优化最终运动输出，从而无需重新训练模型即可应对多种运动编辑、补全和去噪任务。
claims:
- 通过优化预训练文本运动模型的扩散潜在噪声，DNO 无需针对每个新任务重新训练模型。
- DNO 通过完整的去噪链反向传播目标函数梯度，从而在最终运动上精确计算准则，消除了引导方法中普遍存在的近似误差。
- DNO 在一系列运动编辑任务上全面超越了 GMD，显著提高了内容保留度并实现了零目标误差。
- 运动编辑（4种动作：跳、跳远、抬臂行走、爬行） 上 内容保留度 (Content Preservation) = 0.92-0.95
---

# DNO: Optimizing Diffusion Noise Can Serve As Universal Motion Priors

> [!tip] 核心洞察
> 将运动生成视为一个在预训练扩散模型潜在空间中的优化问题：在扩散噪声 x_T 上执行梯度下降，通过反向传播整个 ODE 求解器来直接优化最终运动输出，从而无需重新训练模型即可应对多种运动编辑、补全和去噪任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | DNO：优化扩散噪声可作为通用运动先验 |
| 英文题名 | DNO: Optimizing Diffusion Noise Can Serve As Universal Motion Priors |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2024/html/Karunratanakul_Optimizing_Diffusion_Noise_Can_Serve_As_Universal_Motion_Priors_CVPR_2024_paper.html) · [Project](https://korrawe.github.io/dno-project/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Diffusion Noise Optimization (DNO) |
| Dataset | 运动编辑（4种动作：跳、跳远、抬臂行走、爬行）, 噪声运动精化（5cm噪声，HumanML3D） |

> [!tip] 效果简介
> - 运动编辑（4种动作：跳、跳远、抬臂行走、爬行） 上，内容保留度 (Content Preservation) 0.92-0.95 vs 0.59-0.79 (GMD) (平均提升约 0.33)。
> - 运动编辑（同4种动作） 上，目标误差 (Objective Error) 0.00 vs 0.15-0.22 (GMD) (降至零误差)。
> - 噪声运动精化（5cm噪声，HumanML3D） 上，MPJPE (cm) 7.0 (DNO-GMD) vs 25.7 (GMD) (-18.7)。

## 概要

**问题瓶颈：** 现有运动扩散模型在合成自然运动方面展现出强大能力，但难以直接充当通用运动先验。为每个新任务（如运动编辑、补全、去噪）训练专用模型成本高昂，而基于引导的方法在编辑或控制时往往无法同时保留原始运动内容并精确满足目标约束，存在固有的近似误差。

**核心方法：** DNO（Diffusion Noise Optimization）将运动生成重新定义为在预训练扩散模型潜在空间中的优化问题。其关键操作变量是扩散过程的初始噪声向量 $\mathbf{x}_T$——通过该噪声向量的梯度下降，并利用反向传播穿越整个 ODE 求解器，直接在最终运动输出上精确计算任意可微的目标函数，从而无需重新训练模型即可应对多种运动任务。

**方法定位：** DNO 属于扩散模型潜在空间优化的范式，与 GMD（Karunratanakul et al., ICCV 2023）等基于引导的方法形成对比。其核心差异在于：优化变量从中间去噪步骤的期望输出 $\hat{\mathbf{x}}_0$ 转变为初始噪声 $\mathbf{x}_T$，目标函数评估从近似估计升级为完整去噪链后的精确计算，梯度处理则引入单位范数归一化以稳定优化过程。

**主要结果：** 在运动编辑任务上，DNO 的内容保留度（0.92–0.95）较 GMD（0.59–0.79）平均提升约 0.33，目标误差降至零（GMD 为 0.15–0.22）。在噪声运动精化任务上（5 cm 噪声），DNO 将 MPJPE 从 25.7 cm 降至 7.0 cm，FID 从 6.91 降至 0.10，实现了数量级的性能提升。

**局限性：** 反向传播整个 ODE 求解器带来显著的内存开销和推理延迟（每次编辑需 300–1000 次优化迭代），难以满足实时交互需求。此外，目前仅在 HumanML3D 人形运动数据集上验证，对稀疏观测条件下的鲁棒性及向其他运动形态的泛化能力尚待检验。



### 问题背景：运动生成与扩散模型

人体运动生成是计算机视觉与图形学中的核心任务，广泛应用于动画制作、虚拟现实、机器人学习等领域。近年来，扩散模型在运动生成任务上取得了显著进展，尤其是基于文本提示的文本-运动扩散模型（text-to-motion diffusion model），能够根据自然语言描述生成多样化且物理合理的人体运动序列。这类模型通过学习从纯噪声 $x_T$ 到干净运动 $x_0$ 的迭代去噪过程，隐式地编码了丰富的人体运动先验知识。

然而，现有运动扩散模型的价值通常局限于“从文本生成运动”这一单向任务。将其作为通用运动先验（universal motion prior）来支持运动编辑、运动补全、运动去噪等更广泛的下游应用，仍然是一个尚未充分解决的问题。

### 现有方法缺口：专用模型与引导方法的局限

当前利用扩散模型进行运动编辑或控制的方法主要分为两类，各自存在显著局限：

**专用模型路线**要求针对每个新任务重新训练或微调一个扩散模型。例如，若需要实现“跳跃时改变手部位置”的编辑功能，通常需要收集配对数据并训练一个条件生成模型。这种方式成本高昂，缺乏通用性，难以应对实际应用中多样且多变的需求。

**引导方法路线**以 **GMD**（Karunratanakul et al., ICCV 2023）为代表，试图在不重新训练模型的情况下，通过在去噪过程中注入额外梯度信号来实现运动编辑。然而，这类方法存在两个根本性问题：

1. **近似误差**：引导方法在每个去噪步骤 $t$ 上，基于对最终运动 $\hat{x}_0$ 的局部估计来计算目标函数的梯度。由于该估计并非真实的最终输出，梯度信号存在系统性偏差，导致编辑结果难以精确满足目标约束。

2. **内容破坏**：在逐步注入引导信号的过程中，原始运动的内容特征（如节奏、风格、肢体协调性）容易被逐步侵蚀。实验表明，GMD 在跳跃、跳远、抬臂行走、爬行等动作上的内容保留度仅为 0.59–0.79，远低于理想水平。

上述缺口的核心瓶颈在于：**现有方法无法在保留原始运动内容的同时，精确满足任意可微的目标约束**。这直接限制了预训练运动扩散模型作为通用运动先验的潜力。

### 本文动机：将运动生成重新定义为潜在空间优化问题

本文的出发点是提出一个根本性的视角转换：**不再将运动编辑视为对去噪过程的引导，而是将其视为在扩散模型潜在空间中的直接优化问题**。

关键洞察在于：预训练扩散模型的去噪过程可以看作一个确定性的映射函数 $f: x_T \rightarrow x_0$（例如通过 DDIM-ODE 求解器），该函数将任意初始噪声向量 $x_T$ 映射为对应的干净运动 $x_0$。由于扩散模型已在大量运动数据上训练，$f$ 的输出空间几乎处处对应合理的人体运动。因此，只需在 $x_T$ 上执行梯度下降，通过反向传播整个 ODE 求解器来优化最终运动输出，即可在不重新训练模型的前提下，灵活应对多种运动编辑、补全和去噪任务。

这一思路将扩散模型真正转化为一个**即插即用的运动先验**：用户只需定义任务特定的可微损失函数 $\mathcal{L}(x_0)$（如目标关节位置、障碍物约束、内容保持等），DNO 即可自动优化 $x_T$ 以生成满足要求且保持运动自然性的结果。



## 核心方法与创新机理

DNO 的核心创新在于将运动生成重新定义为**在预训练扩散模型潜在空间中的直接优化问题**，而非传统的引导采样或针对特定任务重新训练模型。这一范式转换通过三个关键的“changed slots”实现，从根本上解决了现有方法在运动编辑与控制中难以同时保留原始内容并精确满足目标约束的瓶颈。

### 优化变量的重新选择：从中间估计到初始噪声

现有引导方法（如 **GMD**，Karunratanakul et al., ICCV 2023）通常在去噪过程的每个中间步骤 $t$ 对期望输出 $\hat{\mathbf{x}}_0$ 的估计进行优化，或对直接解码的隐空间变量进行操作。这种方式本质上是在一个不完整的、尚未充分去噪的中间状态上进行干预，导致优化目标与最终输出之间存在偏差。

DNO 做出了根本性的改变：**直接优化扩散过程的初始噪声向量 $\mathbf{x}_T$**。这一选择基于一个关键认知——在扩散模型中，$\mathbf{x}_T$ 是生成过程的唯一随机性来源，通过确定性 ODE 求解器（DDIM-ODE），$\mathbf{x}_T$ 与最终运动 $\mathbf{x}_0$ 之间存在确定的映射关系：

$$\mathbf{x}_{T}^{*} = \arg\min_{\mathbf{x}_{T}} \mathcal{L}(\mathrm{ODESolver}(d(\cdot), \mathbf{x}_{T}))$$

由于 $\mathbf{x}_T$ 空间中的任一点几乎处处可解码为合理运动（这是扩散模型作为运动先验的核心特性），在该空间中进行优化天然保证了生成结果的物理合理性，无需额外的约束项来维持运动质量。

### 目标函数评估方式的根本改进：从近似到精确

引导方法的一个固有缺陷是**在去噪中间步骤的期望运动上近似计算损失函数** $\mathcal{L}(\hat{\mathbf{x}}_0)$。由于 $\hat{\mathbf{x}}_0$ 仅是对最终输出的粗略估计，这种近似不可避免地引入误差，导致优化方向偏离真实目标。

DNO 通过**完整的去噪链反向传播**彻底消除了这一近似误差。具体而言，优化过程首先通过 ODE 求解器从当前 $\mathbf{x}_T$ 生成完整的最终运动 $\mathbf{x}_0$，然后在该输出上精确计算任务特定的损失函数 $\mathcal{L}(\mathbf{x}_0)$，最后将梯度通过整个 ODE 求解器反向传播至 $\mathbf{x}_T$。正如原文所述：“For DNO, the criterion is exactly computed on $\mathbf{x}$ after the full-chain denoising which eliminates the approximation error.” 这一设计使得优化器能够“看到”其更新对最终输出的真实影响，从而实现零目标误差的精确编辑。

### 梯度处理策略的优化：归一化与稳定收敛

通过完整 ODE 链反向传播梯度带来了新的挑战：梯度范数可能在优化过程中剧烈波动，导致收敛不稳定。DNO 提出**对梯度进行单位范数归一化**，这一简单而有效的策略显著提升了优化速度与精度。消融实验表明，归一化梯度将噪声运动精化任务的 MPJPE 从 30.2 cm 降至 8.7 cm（Table 3），证明了该设计的关键作用。

此外，DNO 采用 Adam 优化器配合线性预热与余弦学习率衰减策略（学习率 0.05，50 步预热），进一步稳定了优化过程。与依赖单步梯度或不经归一化的引导方法相比，这一完整的优化框架使 DNO 能够在 300-1000 次迭代内收敛到高质量解。

### 创新带来的能力跃升

这三个 changed slots 的协同作用使 DNO 获得了超越基线方法的显著能力：

- **零目标误差编辑**：在运动编辑任务中，DNO 的目标误差降至 0.00，而 GMD 为 0.15-0.22（Table 1），验证了精确损失计算的有效性。
- **高保真内容保留**：内容保留度从 GMD 的 0.59-0.79 提升至 0.92-0.95，平均提升约 0.33，表明优化 $\mathbf{x}_T$ 并约束其偏离参考噪声的策略能有效保留原始运动特性。
- **通用任务适应性**：通过简单组合不同的可微损失函数（姿态损失、障碍物损失、内容保持损失、去相关损失），同一框架可无缝应用于运动编辑、噪声精化、运动补全等多种任务，无需任何模型重训练或架构修改。

### 与相关工作的本质区别

DNO 受 **DOODL** 启发，但做出了关键改进：DOODL 要求 ODE 可逆以进行潜在空间优化，而 DNO 发现**可逆 ODE 并非必需**——直接优化 $\mathbf{x}_T$ 并正向通过 ODE 求解器即可，这使得方法更简单且适用范围更广。相较于在图像领域探索潜在优化的工作，DNO 首次系统性地将这一范式引入人体运动生成，并针对运动数据的时序特性设计了专门的损失函数（如去相关损失 $\mathcal{L}_{\mathrm{decorr}}$ 以抑制足部滑步）和优化策略。

**需要手动验证的点**：文中未明确给出 DNO 与 DOODL 在收敛速度或内存开销上的定量对比，仅提及“improved optimization algorithm that speeds up optimization”，该声明的具体幅度需查阅原始实验数据确认。



DNO 的整体 pipeline 围绕一个核心思想展开：**将预训练运动扩散模型作为黑箱运动先验，通过优化其初始噪声向量来实现任意可微目标的运动生成与控制**。该框架无需针对每个新任务重新训练或微调模型，仅需定义任务特定的损失函数即可驱动优化过程。

### 核心优化回路

DNO 的优化回路由三个关键模块串联构成，形成一个端到端的可微分管道：

1. **潜在变量初始化**  
   优化变量被设定为扩散过程的初始噪声 $\mathbf{x}_T \sim \mathcal{N}(0, \mathbf{I})$。对于运动编辑任务，首先通过扩散反演（DDIM-ODE 逆过程）将参考运动 $\mathbf{x}_{\text{ref}}$ 映射回噪声空间，得到 $\mathbf{x}_{T\text{ref}}$ 作为优化的起点，从而在编辑时保留原始运动的内容特征。

2. **ODE 求解器解码**  
   在每次优化迭代中，当前噪声 $\mathbf{x}_T$ 通过确定性 ODE 求解器（DDIM-ODE）完整运行去噪过程，生成对应的干净运动序列 $\mathbf{x}_0 = \text{ODESolver}(d(\cdot), \mathbf{x}_T)$。这一步保证了解码结果始终落在预训练模型所定义的合理运动流形上。

3. **损失计算与梯度反向传播**  
   在解码后的运动 $\mathbf{x}_0$ 上精确计算任务特定损失 $\mathcal{L}(\mathbf{x}_0)$，然后通过整个 ODE 求解器反向传播梯度到 $\mathbf{x}_T$。梯度经过单位范数归一化后，由 Adam 优化器更新 $\mathbf{x}_T$。这一设计消除了引导方法中在中间去噪步骤近似计算损失所带来的误差。

### 优化目标形式化

整个优化过程可形式化为：

$$\mathbf{x}_{T}^{*} = \arg\min_{\mathbf{x}_{T}} \mathcal{L}(\text{ODESolver}(d(\cdot), \mathbf{x}_{T}))$$

其中 $d(\cdot)$ 为预训练扩散模型的去噪函数，$\mathcal{L}$ 为任务特定的可微损失函数。该目标直接优化最终运动输出，而非中间表示。

### 任务适配机制

DNO 的通用性体现在损失函数的模块化组合上。针对不同应用场景，框架复用相同的优化核心，仅切换损失函数：

- **运动编辑**：组合姿态损失 $\mathcal{L}_{\text{pose}}$、障碍物损失 $\mathcal{L}_{\text{obs}}$ 与内容保持损失 $\mathcal{L}_{\text{cont}}$，后者通过约束 $\|\mathbf{x}_{T\text{ref}} - \mathbf{x}_T\|_2$ 来保留原始运动特征。
- **运动精化与补全**：组合姿态损失与去相关损失 $\mathcal{L}_{\text{decorr}}$，后者在潜在空间的多尺度表示上惩罚连续帧的相关性，以抑制足部滑步等伪影。

### 优化配置

所有任务共享统一的优化器设置：Adam 优化器，学习率 0.05，前 50 步线性预热，随后余弦衰减至零。梯度归一化是保证优化稳定性的关键设计——消融实验表明，移除归一化后 MPJPE 从 8.7 cm 恶化至 30.2 cm。DDIM 采样步数设为 10 步，以平衡生成质量与反向传播的内存开销。

### 输入输出流

- **输入**：参考运动（编辑任务）或带噪声/部分观测的运动（精化/补全任务），以及任务定义（目标关节位置、障碍物 SDF、可观测关节集合等）。
- **输出**：经过优化的完整运动序列，以相对根表示（263 维特征，M 帧）呈现，可直接映射回全局关节位置用于可视化或下游应用。



### 3.1 问题形式化：将运动生成视为潜在空间优化

DNO 的核心思想是将运动编辑与精化任务统一为在预训练扩散模型的潜在空间上的优化问题。给定一个预训练的运动扩散模型，其去噪函数为 $d(\cdot)$，DNO 选择扩散过程的初始噪声 $\mathbf{x}_T$ 作为优化变量。这一选择的依据是：扩散模型训练完成后，从任意高斯噪声 $\mathbf{x}_T \sim \mathcal{N}(0, \mathbf{I})$ 出发，通过 ODE 求解器均可解码出合理的运动，因此 $\mathbf{x}_T$ 构成一个“几乎处处可解码为有效运动”的表达性潜在空间。

优化目标的形式化定义如下：

$$
\mathbf{x}_{T}^{*} = \arg\min_{\mathbf{x}_{T}} \mathcal{L}(\mathrm{ODESolver}(d(\cdot), \mathbf{x}_{T}))
$$

其中，$\mathrm{ODESolver}(d(\cdot), \mathbf{x}_{T})$ 表示以 $\mathbf{x}_T$ 为起点、使用去噪函数 $d(\cdot)$ 通过 ODE 求解器（具体为 DDIM-ODE）生成最终运动 $\mathbf{x}_0$ 的过程；$\mathcal{L}(\cdot)$ 是定义在输出运动上的可微任务损失函数。通过优化 $\mathbf{x}_T$ 而非直接操作 $\mathbf{x}_0$，DNO 确保优化过程中的每一步更新都保持在“可解码为合理运动”的流形上。

### 3.2 核心优化算法

DNO 的优化流程（Algorithm 1）由以下关键步骤构成：

1. **前向解码**：在每次优化迭代中，通过 ODE 求解器从当前 $\mathbf{x}_T$ 解码出完整运动 $\mathbf{x}_0$。
2. **损失计算**：在解码后的运动 $\mathbf{x}_0$ 上精确计算任务损失 $\mathcal{L}(\mathbf{x}_0)$。这与引导方法（如 GMD）形成本质区别——GMD 仅在去噪中间步骤的期望运动上近似计算损失，而 DNO 消除了这一近似误差。
3. **反向传播**：将损失梯度通过整个 ODE 求解器反向传播至 $\mathbf{x}_T$，获得 $\nabla_{\mathbf{x}_T} \mathcal{L}$。
4. **梯度归一化与更新**：对梯度进行单位范数归一化（$\nabla / \|\nabla\|$），然后使用 Adam 优化器更新 $\mathbf{x}_T$。梯度归一化是 DNO 优化稳定性的关键设计，消融实验表明，移除归一化后 MPJPE 从 8.7 cm 急剧恶化至 30.2 cm（Table 3）。
5. **可选扰动**：可向更新后的 $\mathbf{x}_T$ 添加高斯噪声 $\gamma \mathcal{N}(0, 1)$ 以增强探索，但实验发现 $\gamma > 0$ 均导致 FID 恶化，故最终选择 $\gamma = 0$。

### 3.3 任务损失函数设计

DNO 的通用性体现在其损失函数可根据任务自由组合。论文定义了以下核心损失项：

**姿态损失**（$\mathcal{L}_{\mathrm{pose}}$）：约束生成运动中特定关节在特定关键帧的位置与目标位置一致：

$$
\mathcal{L}_{\mathrm{pose}}(\mathbf{x}, O) := \frac{1}{|O|} \sum_{(j,k) \in O} \left\| \hat{\mathbf{c}}_j^k(\mathbf{x}) - \mathbf{c}_j^k \right\|_1
$$

其中 $O$ 为观测集合，包含关节索引 $j$ 和关键帧 $k$ 的配对；$\hat{\mathbf{c}}_j^k(\mathbf{x})$ 为生成运动中关节 $j$ 在帧 $k$ 的 3D 位置（通过前向运动学从运动表征计算）；$\mathbf{c}_j^k$ 为目标位置。

**障碍物损失**（$\mathcal{L}_{\mathrm{obs}}$）：使运动规避场景中的障碍物，无需显式指定目标关键帧：

$$
\mathcal{L}_{\mathrm{obs}}(\mathbf{x}) := \sum_{j,k} -\min\left[ \mathrm{SDF}^k(\hat{\mathbf{c}}_j^k(\mathbf{x})), \tau \right]
$$

其中 $\mathrm{SDF}^k(\cdot)$ 为帧 $k$ 时刻障碍物的有符号距离函数（SDF），关节在障碍物内部时 SDF 为负值；$\tau$ 为安全距离阈值。该损失仅当关节进入或靠近障碍物时施加惩罚。

**内容保持损失**（$\mathcal{L}_{\mathrm{cont}}$）：在运动编辑中保留原始运动的特性。首先通过扩散反演（DDIM-ODE 逆向求解）从参考运动 $\mathbf{x}_{\mathrm{ref}}$ 获得其对应的噪声 $\mathbf{x}_{T\mathrm{ref}}$，然后在优化过程中约束 $\mathbf{x}_T$ 不偏离 $\mathbf{x}_{T\mathrm{ref}}$ 过远：

$$
\mathcal{L}_{\mathrm{cont}}(\mathbf{x}_T) := \| \mathbf{x}_{T\mathrm{ref}} - \mathbf{x}_T \|_2
$$

**去相关损失**（$\mathcal{L}_{\mathrm{decorr}}^m$）：针对运动精化任务中常见的足部滑步问题，受 StyleGAN2 启发，在潜在空间的多尺度上惩罚连续帧之间的相关性：

$$
\mathcal{L}_{\mathrm{decorr}}^m(\mathbf{x}_T) = \frac{1}{mD} \sum_{i=1}^{m} \mathbf{x}_{T,m}(i)^{\top} \mathbf{x}_{T,m}(i+1)
$$

其中 $\mathbf{x}_{T,m}$ 为 $\mathbf{x}_T$ 按尺度 $m$ 下采样后的表示，$D$ 为运动表征维度（263）。该损失在多个下采样尺度上求和使用。

### 3.4 面向不同应用的损失组合

**运动编辑**的总损失组合为：

$$
\mathcal{L}(\cdot) = \mathcal{L}_{\mathrm{pose}}(\mathbf{x}) + \lambda_{\mathrm{obs}} \mathcal{L}_{\mathrm{obs}}(\mathbf{x}, O) + \lambda_{\mathrm{cont}} \mathcal{L}_{\mathrm{cont}}(\mathbf{x}_T)
$$

其中 $\lambda_{\mathrm{obs}}$ 和 $\lambda_{\mathrm{cont}}$ 为权重系数。优化从反演噪声 $\mathbf{x}_{T\mathrm{ref}}$ 初始化。

**运动精化与补全**的总损失组合为：

$$
\mathcal{L}(\cdot) = \mathcal{L}_{\mathrm{pose}}(\mathbf{x}, O) + \lambda_{\mathrm{decorr}} \sum_m \mathcal{L}_{\mathrm{decorr}}^m(\mathbf{x}_T)
$$

运动精化时，$O$ 包含所有关节和所有帧（即约束生成运动逼近含噪声的输入运动）；运动补全时，$O$ 仅包含输入运动中已有的关节和帧，优化从随机噪声 $\mathbf{x}_T \sim \mathcal{N}(0, \mathbf{I})$ 初始化。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2024_html_Karunratanakul_Optimiz/figures/002_Figure.jpg]]
*Figure: (a) At each optimization step, DNO maintains the output motion equality by making a step in the latent space xT , which is decodable to a realistic motion almost everywhere*



## 实验与关键发现

### 运动编辑：精确目标控制与内容保留的突破

DNO 在运动编辑任务上展现出压倒性优势。与基于引导扩散的运动编辑方法 **GMD**（Karunratanakul et al., ICCV 2023）相比，DNO 在四种典型动作（跳、跳远、抬臂行走、爬行）上实现了质变性的提升。

**内容保留度**方面，DNO-MDMEdit 达到 0.92–0.95，而 GMD 仅为 0.59–0.79，平均提升约 0.33（Table 1）。这意味着 DNO 在编辑目标关节位置的同时，几乎完整保留了原始运动的风格、节奏和其余身体部位的运动特征，而 GMD 往往导致运动整体变形。

**目标误差**方面，DNO 实现了零目标误差（0.00），而 GMD 的误差在 0.15–0.22 之间（Table 1）。这一差异的根本原因在于梯度路径的不同：GMD 在去噪中间步骤的期望运动上近似计算损失，引入系统性偏差；DNO 则在完整去噪后的输出运动上精确计算损失，并通过整个 ODE 求解器反向传播梯度，从而消除了近似误差。

**运动质量指标**上，DNO 的 Jitter（运动抖动）为 0.32–1.34，显著低于 GMD 的 0.51–4.10，表明优化后的运动更加平滑自然。唯一的例外是爬行动作的 Foot skating ratio，DNO 略高于 GMD，这是去相关损失权重在全局统一设置下未能针对特定动作充分调优所致。

定性结果（Figure 3）进一步印证了定量发现：DNO 能够在保持整体运动特征的前提下，精确地将指定关节移动到目标位置，或使运动轨迹绕过新增障碍物，而无需显式指定目标关键帧。

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2024_html_Karunratanakul_Optimiz/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results from motion editing task. Each line indicates the starting and target location of the selected joint at a specific keyframe*

### 噪声运动精化：从不可用到高度逼真

在噪声运动精化任务上，DNO 将严重退化的运动恢复至接近真实数据的水平。当向 HumanML3D 数据集子集的运动添加标准差 5 cm 的高斯噪声后：

- **MPJPE**（平均关节位置误差）：DNO-GMD 降至 **7.0 cm**，较 GMD 的 25.7 cm 降低了 18.7 cm，甚至略优于专用运动精化方法 **HuMoR**（Rempe et al., ICCV 2021）的 7.2 cm（Table 2）。
- **FID**（分布质量）：DNO-GMD 达到 **0.10**，远低于 GMD 的 6.91 和 HuMoR 的 0.87，表明精化后的运动分布与真实运动分布几乎无法区分（Table 2）。值得注意的是，Real 行的 FID 为 0.04，DNO 的结果已极为接近这一理论上限。

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2024_html_Karunratanakul_Optimiz/figures/006_Table_2.jpg]]
*Table 2: Noisy motion refinement results (noise std. 5 cm) on a subset of HumanML3D [18] dataset. All experiments were run with N = 300. FIDs are computed against Real except Real’s FIDs which are computed against a holdout set from the dataset. HuMoR* means we exclude the sequence when its optimization fails. DNO-MLD* runs with 1,000 optimization steps*

当仅观测部分关节（如仅下半身）时，DNO-GMD 的 MPJPE 为 4.8 cm，仍显著优于 GMD 的 8.0 cm 和 HuMoR 的 6.1 cm，证明 DNO 在稀疏观测条件下同样具有鲁棒的精化能力。DNO-MLD 在 1000 步优化后也取得了有竞争力的结果（MPJPE 7.4 cm，FID 0.35），但收敛速度明显慢于基于 MDM 的变体。

### 消融实验：梯度归一化是核心使能技术

消融实验（Table 3，噪声标准差 1 cm）揭示了 DNO 各组件的贡献：

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2024_html_Karunratanakul_Optimiz/figures/007_Table_3.jpg]]
*Table 3: Ablation study on the noisy motion refinement task (std. 1 cm) results on a subset of HumanML3D [18]. All experiments were run with N = 3 0 0 . FIDs are computed against Real except Real’s FIDs which are computed against a holdout set from the dataset*

| 配置 | MPJPE (cm) ↓ | FID ↓ | Foot Skating ↓ | Jitter ↓ |
|------|-------------|-------|----------------|----------|
| DNO-GMD（完整） | **8.7** | 0.09 | 0.07 | 0.33 |
| 无梯度归一化 | 30.2 | 0.08 | 0.07 | 0.34 |
| 无去相关损失 | 6.8 | 0.08 | 0.10 | 0.40 |

**梯度归一化**是最关键的组件。移除归一化后，MPJPE 从 8.7 cm 飙升至 30.2 cm，增幅超过 3 倍。这是因为扩散潜在空间的尺度与运动空间的尺度存在显著不匹配，未归一化的梯度会导致优化过程在潜在空间中步长极度不均，难以收敛到精确解。归一化到单位范数后，优化器在潜在空间中每一步的移动幅度保持一致，显著加速收敛并提升最终精度。

**去相关损失** $L_{decorr}$ 在运动质量与重建精度之间存在权衡。引入该损失后，Foot skating ratio 从 0.10 降至 0.07，Jitter 从 0.40 降至 0.33，表明运动变得更加自然、足部滑步减少；但 MPJPE 从 6.8 cm 微增至 8.7 cm。这一权衡在实际应用中可根据需求调整损失权重 $\lambda_{decorr}$。

**随机扰动**（$\gamma > 0$）在所有测试值下均导致 FID 恶化，尽管对优化误差影响微小。因此最终配置选择 $\gamma = 0$，即不添加随机噪声扰动。

**DDIM 采样步数**的影响表现为：步数从 5 增至 10 时，MPJPE 从 9.8 cm 降至 8.7 cm；继续增至 20 时进一步降至 7.9 cm，但内存开销和计算时间线性增长。最终选择 10 步以平衡质量与资源消耗。

### 失败模式与局限性

尽管 DNO 在多数场景下表现优异，仍存在以下已知失败模式：

1. **内存瓶颈**：反向传播整个 ODE 求解器需要保存大量中间激活。即使采用梯度检查点技术，内存负担仍显著限制了可使用的扩散采样步数，使得在资源受限环境下难以使用更多步数进一步提升质量。

2. **推理延迟**：每次编辑需 300–1000 次优化迭代，每次迭代均需运行完整 ODE 求解器，总耗时远超实时交互式应用的要求。这是 DNO 走向实际部署的主要障碍。

3. **低覆盖鲁棒性不足**：当可观测关节数量极少（如仅有头部和手部）时，重建精度和运动自然度可能显著下降。文中未对此极端场景进行深入定量分析，需手动验证。

4. **底层模型依赖**：编辑质量的上限受限于所采用的预训练运动扩散模型（MDM）的表达能力与数据集覆盖范围。若基础模型本身无法生成某些合理运动模式，优化过程可能失效或产生不自然的结果。

5. **泛化性未验证**：目前仅在 HumanML3D 人形运动数据集上验证，对其他运动形态（如四足动物、多智能体交互）或复杂场景约束的适用性尚未检验。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openaccess_thecvf_com_content_CVPR2024_html_Karunratanakul_Optimiz/figures/004_Table_1.jpg]]
*Table 1: Motion editing evaluation on specific actions generated from MDM given the text prompts. We focus on actions that can be distinctly classified per frame basis. The Content Preservation scores are computed against the inputs*



## 定位与知识库关联

### 与引导扩散方法的对比与突破

DNO 的核心思想是将预训练扩散模型作为通用运动先验，通过在扩散噪声空间 $x_T$ 上优化任意可微损失函数来生成满足约束的运动。这一思路与现有引导扩散方法（guided diffusion）存在本质差异。

**GMD**（Karunratanakul et al., ICCV 2023）是运动编辑任务中最直接的对比基线。GMD 采用引导扩散范式，在每个去噪步骤 $t$ 对期望输出 $\hat{x}_0$ 的估计进行优化，通过近似计算损失 $\mathcal{L}(\hat{x}_0)$ 来引导采样方向。这种逐步近似策略带来两个固有问题：(1) 中间步骤的 $\hat{x}_0$ 估计存在误差，导致目标函数评估不精确；(2) 引导强度与内容保留之间存在难以调和的权衡——强引导可降低目标误差但会破坏原始运动内容，弱引导则相反。实验数据充分暴露了这一瓶颈：在跳跃、跳远、抬臂行走、爬行四类动作编辑中，GMD 的内容保留度仅为 0.59–0.79，而目标误差仍高达 0.15–0.22。

DNO 通过将优化变量从中间步骤的 $\hat{x}_0$ 移至扩散噪声 $x_T$，并利用完整的 DDIM-ODE 求解器 $f(x_T) = \text{ODESolver}(d(\cdot), x_T)$ 进行端到端反向传播，从根本上消除了近似误差。如原文所述：“For DNO, the criterion is exactly computed on $x$ after the full-chain denoising which eliminates the approximation error.” 这一设计使得 DNO 在运动编辑任务上实现了零目标误差（Objective Error = 0.00），同时将内容保留度提升至 0.92–0.95，平均较 GMD 提高约 0.33。

在技术源流上，DNO 受 **DOODL**（图像域中通过可逆 ODE 优化扩散噪声的工作）启发，但做出了两项关键改进：(1) 发现可逆 ODE 并非必要，直接使用 DDIM-ODE 即可，简化了实现并扩展了适用模型范围；(2) 引入梯度单位范数归一化，显著加速收敛。消融实验表明，移除梯度归一化后，噪声运动精化任务的 MPJPE 从 8.7 cm 飙升至 30.2 cm，验证了这一设计的关键性。

### 与运动去噪/精化方法的对比

在运动精化任务上，DNO 与两类传统方法形成对比：

**HuMoR**（Rempe et al., ICCV 2021）是一种基于条件变分自编码器（CVAE）的运动先验模型，通过优化隐变量来精化噪声运动。在 5 cm 噪声标准差条件下，HuMoR 在全部关节观测时达到 MPJPE 7.2 cm，但需排除优化失败的序列（表中标记为 HuMoR*）。DNO-GMD 在相同条件下达到 7.0 cm，且无需排除任何样本，显示出更强的鲁棒性。在运动自然度指标 FID 上，DNO-GMD 达到 0.10，远优于 HuMoR 的 0.87，表明扩散先验在保持运动合理性方面具有显著优势。

**MLD**（Motion Latent Diffusion）作为基于隐空间扩散的运动生成模型，在精化任务上表现较弱：DNO-MLD 需要 1000 步优化才能达到 10.6 cm 的 MPJPE，且 FID 为 1.12。这暗示 DNO 框架的性能与底层扩散模型的质量密切相关——MDM 在像素空间直接建模运动，其先验约束力强于在压缩隐空间建模的 MLD。

### 适用边界与能力范围

DNO 的适用边界由以下因素共同界定：

**任务灵活性**：DNO 通过组合不同的可微损失函数，能够应对运动编辑、精化、补全、障碍物规避等多种任务，无需针对每个任务重新训练模型。这是其作为“通用运动先验”的核心优势。损失函数设计遵循模块化原则——姿态损失 $\mathcal{L}_{\text{pose}}$ 处理关键帧关节约束，障碍物损失 $\mathcal{L}_{\text{obs}}$ 通过 SDF 处理空间约束，内容保持损失 $\mathcal{L}_{\text{cont}}$ 约束优化后的 $x_T$ 接近原始运动的逆推噪声，去相关损失 $\mathcal{L}_{\text{decorr}}$ 减少足部滑步伪影。

**底层模型依赖**：DNO 的编辑质量上限严格受限于所采用的预训练运动扩散模型的表达能力。当前实验基于 MDM（在 HumanML3D 数据集上训练），该模型覆盖的动作品类决定了 DNO 可生成的合理运动范围。若基础模型无法生成某些特定运动模式，优化过程可能收敛到不合理的结果或完全失败。

**数据分布约束**：所有验证均在 HumanML3D 人形运动数据集上完成，对其他运动形态（如四足动物、多智能体交互、物体操作等）的泛化性尚未检验。此外，当可观测关节极为稀疏（如仅头部和双手）时，重建精度和运动自然度可能显著下降，文中未对此边界条件做深入分析。

### 局限性与开放问题

**计算开销**：DNO 的主要局限在于推理效率。每次编辑需 300–1000 次优化迭代，每次迭代均需运行完整 DDIM-ODE 求解器（默认 10 步）并反向传播梯度。即使使用梯度检查点，保存中间激活仍带来显著内存负担，限制了可使用的扩散采样步数。这一特性使 DNO 目前难以满足实时交互式应用的需求。一个值得探索的方向是结合神经网络代理模型或蒸馏采样技术，将优化过程加速至接近实时。

**泛化性验证不足**：当前实验仅覆盖有限的动作类型和编辑模式。对于更复杂的连续动作序列、多角色交互运动、或与动态场景上下文的联合优化，DNO 的有效性仍是开放问题。特别是当没有明确参考运动时，如何通过文本提示或其他弱条件直接初始化优化噪声 $x_T$ 并生成符合要求的运动，文中未给出方案。

**理论收敛性**：梯度归一化策略虽在实验中表现出色，但其对优化收敛性的理论保证尚不明确。该策略在隐式 GAN 或 VAE 等其他生成模型中的适用性也有待验证。

**低覆盖鲁棒性**：当可观测关节数量极少时，运动重建可能退化为不适定问题。是否需要引入额外的结构化先验或专门的损失函数来应对稀疏观测场景，是一个具有实际意义的开放问题。



## 原文 PDF

![[paperPDFs/CVPR_2024/DNO_Optimizing_Diffusion_Noise_Can_Serve_As_Universal_Motion_Priors.pdf]]
