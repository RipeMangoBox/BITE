---
title: "GDPO-SR: Group Direct Preference Optimization for One-Step Generative Image Super-Resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GDPO_SR_Group_Direct_Preference_Optimization_for_One_Step_Generative_Image_Super_Resolution.pdf
project_link: null
code_link: "https://github.com/Joyies/GDPO"
aliases:
- GSGDPOOSSR
- GDPO-SR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过向单步扩散模型的潜在空间注入可控噪声，引入输出多样性；随后利用群体相对优势进行在线偏好优化，指导模型优先学习高奖励样本所对应的优势模式。
primary_logic: 将GRPO的群体相对优势与DPO的像素级隐式似然约束相结合，同时设计属性感知的奖励函数动态平衡保真度与感知质量，使模型能够在无需大量离线偏好数据的情况下，在真实场景ISR中实现更清晰、更丰富的纹理重建。
claims:
- 引入噪声感知的一步扩散模型（NAOSD）为单步ISR带来了多样性输出，为强化学习优化奠定基础。
- 不等时步策略通过解耦噪声添加和扩散时步，在引入噪声的同时避免了性能下降。
- GDPO通过在线生成的样本组计算群体相对优势，并利用像素级约束进行策略优化，有效结合了DPO的精度与GRPO的效率。
- RealSR 上 PSNR↑ = 25.48
---

# GDPO-SR: Group Direct Preference Optimization for One-Step Generative Image Super-Resolution

> [!tip] 核心洞察
> 将GRPO的群体相对优势与DPO的像素级隐式似然约束相结合，同时设计属性感知的奖励函数动态平衡保真度与感知质量，使模型能够在无需大量离线偏好数据的情况下，在真实场景ISR中实现更清晰、更丰富的纹理重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | GDPO-SR: 用于单步生成式图像超分辨率的群体直接偏好优化 |
| 英文题名 | GDPO-SR: Group Direct Preference Optimization for One-Step Generative Image Super-Resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.16769) · [Code](https://github.com/Joyies/GDPO) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GDPO-SR (Group Direct Preference Optimization for One-Step Super-Resolution) |
| Dataset | RealSR, DRealSR |

> [!tip] 效果简介
> - RealSR 上，PSNR↑ 25.48 vs 25.25 (NAOSD) (+0.23 dB)；MANIQA↑ 0.6615 vs 0.6459 (NAOSD) (+0.0156)；MUSIQ↑ 69.42 vs 69.06 (NAOSD) (+0.36)。
> - DRealSR 上，PSNR↑ 28.18 vs 27.97 (NAOSD) (+0.21 dB)；FID↓ 138.87 vs 140.37 (NAOSD) (-1.50)；PSNR↑ 28.18 vs 23.95 (DP2O-SR) (+4.23 dB)。

## 概述

**问题瓶颈**：单步生成式真实图像超分辨率（Real-ISR）模型因其确定性映射特性，缺乏输出多样性与随机性，导致基于偏好的强化学习（RL）方法难以直接应用。现有RL算法在ISR任务中各有局限：DPO依赖离线有限的偏好对，难以覆盖丰富的在线样本分布；GRPO仅优化全局图像似然，忽略局部纹理细节。

**核心思路**：GDPO-SR通过**向单步扩散模型的潜在空间注入可控噪声**来引入输出多样性，并在此基础上提出**群体直接偏好优化（GDPO）**策略——将GRPO的群体相对优势与DPO的像素级隐式似然约束相结合，同时设计属性感知的奖励函数（ARF）动态平衡保真度与感知质量，使模型在无需大量离线偏好数据的情况下，通过在线生成样本组进行偏好学习。

**方法定位**：GDPO-SR属于**基于强化学习的单步生成式ISR方法**，其基模型为噪声感知的一步扩散模型（NAOSD）。与多步扩散方法（如StableSR、DiffBIR、SeeSR）相比，GDPO-SR保持了单步推理的高效性；与同样引入偏好优化的DP2O-SR（Wu et al., NeurIPS 2025）相比，GDPO-SR采用在线群体优化而非离线偏好对，在保真度指标上显著领先（DRealSR上PSNR高出4.23 dB）。

**主要结果**：在RealSR和DRealSR等真实场景数据集上，GDPO-SR相较于基模型NAOSD在全参考指标（PSNR提升0.21–0.23 dB）和无参考感知指标（MANIQA、MUSIQ）上均取得一致提升；相较于OSEDiff等单步方法，FID降低11.36，LPIPS降低0.0246，展现出更优的纹理重建质量与感知真实感。

## 背景与动机

图像超分辨率（Super-Resolution, SR）旨在从低分辨率（LR）输入重建高分辨率（HR）图像。随着Stable Diffusion等大规模预训练扩散模型的发展，基于扩散的真实图像超分辨率（Real-ISR）方法在生成逼真纹理方面取得了显著进展。然而，这类方法通常依赖多步迭代去噪，推理速度慢、计算开销大，严重制约了实际部署。

为克服效率瓶颈，**一步扩散模型**（如OSEDiff）应运而生，通过将多步去噪压缩为单步推理，大幅降低了延迟。但这类确定性映射方法存在一个根本性缺陷：输出缺乏随机性与多样性，模型对同一LR输入仅能产生唯一结果。这种“一对一的映射”使得基于采样的偏好优化技术难以直接应用——强化学习（RL）算法需要多样化的候选样本来计算相对优势并指导策略更新。

与此同时，现有的RL优化方法在ISR任务中也面临各自的局限。**Diffusion-DPO**将直接偏好优化（DPO）扩展到扩散模型，通过像素级约束实现精细的偏好对齐，但它依赖预先构建的离线偏好对，不仅数据采集成本高，而且无法利用在线生成样本的多样性进行探索。**GRPO**（Group Relative Policy Optimization）则采用群体相对优势进行在线优化，效率更高，但其仅计算全局图像似然，忽略局部细节分布，导致在ISR任务中保真度指标（如PSNR）反而退化。

上述困境揭示了一个核心瓶颈：**单步生成式ISR模型缺乏可控的输出多样性，而现有RL算法在精度与效率之间难以兼顾**。这引出了一个关键研究问题：能否在保持一步推理效率的前提下，为模型注入可控的随机性，并设计一种同时利用像素级约束与群体相对优势的偏好优化策略，使模型在真实场景ISR中实现更清晰、更丰富的纹理重建？

## 核心创新

GDPO-SR 的核心创新在于为单步生成式真实图像超分辨率（Real-ISR）引入了一套完整的在线偏好优化方案，从根源上解决了两个相互关联的瓶颈：**单步模型的输出确定性**与**现有RL方法在ISR任务上的适配缺陷**。

### 瓶颈与因果机制

单步扩散ISR模型（如OSEDiff）通常将LR到HR的映射建模为确定性函数，这虽然带来了推理效率，却剥夺了模型的输出多样性——而多样性恰恰是基于偏好的强化学习（如DPO、GRPO）发挥作用的前提。另一方面，现有RL算法直接迁移至ISR任务时存在结构性缺陷：**Diffusion-DPO**依赖离线收集的固定偏好对，不仅数据获取成本高，还受限于偏好对的规模与质量；**GRPO**虽能通过在线生成样本组进行优化，但其目标函数仅计算全局图像似然比，忽略了像素级的局部细节约束，这对于需要精细纹理重建的ISR任务尤为不利。

GDPO的因果逻辑链条可概括为：**向潜在空间注入可控噪声→产生多样化候选样本→利用群体相对优势进行像素级偏好优化→引导模型倾向高奖励样本的生成模式**。这一链条中的每个环节都对应一个关键的“changed slot”，下面逐一剖析。

### Changed Slot 1：从确定性映射到多样化输出（NAOSD架构）

基线单步模型将ISR视为一个确定性映射 $I_{LR} \rightarrow I_{SR}$，同一张LR图像始终产生完全相同的SR结果。GDPO-SR通过**噪声感知的一步扩散模型（NAOSD）** 打破了这一限制：在VAE编码器将LR图像映射到潜在空间后，向潜在特征注入可控的高斯噪声：

$$\tilde{z} = \sqrt{\alpha_{t_{add}}} z_{LR} + \sqrt{\beta_{t_{add}}} \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I})$$

其中 $t_{add}$ 控制噪声注入的强度。扰动后的潜在特征随后在扩散时步 $t_{diff}$ 下经UNet去噪，得到恢复的潜在特征 $z_{SR}$。这一设计的关键洞察在于：当 $t_{add} \neq t_{diff}$ 时，即使UNet给出理想的噪声预测，$z_{SR}$ 的近似解中仍会保留一个额外的噪声项 $\frac{\sqrt{\beta_{t_{add}}} - \sqrt{\beta_{t_{diff}}}}{\sqrt{\beta_{t_{diff}}}} \epsilon$，这正是输出多样性的来源。

### Changed Slot 2：不等时步策略解耦噪声添加与去噪

直接向潜在空间注入噪声虽然带来了多样性，却可能导致保真度的显著下降——因为噪声扰动会破坏LR图像中本应保留的低频结构信息。GDPO-SR通过**不等时步策略（unequal-timestep strategy）** 巧妙化解了这一矛盾：设置 $t_{add} > t_{diff}$（例如 $t_{add}=250, t_{diff}=100$），使得噪声添加时步远大于去噪时步。较大的 $t_{add}$ 扩展了采样空间，保证了足够的多样性；而较小的 $t_{diff}$ 则使去噪过程更为保守，稳定了输出对原始LR内容的保真度。消融实验（Table 10）证实，通过调整 $t_{add}$ 可以在生成能力与保真度之间进行连续控制：$t_{add}$ 越大，无参考感知指标越好，但PSNR等保真度指标有所下降。

### Changed Slot 3：从离线DPO/全局GRPO到群体相对优势驱动的像素级优化（GDPO损失）

这是GDPO-SR最核心的算法创新。Diffusion-DPO的损失函数为：

$$L(\theta) = -\mathbb{E}_{(x_0^w, x_0^l) \sim \mathcal{D}} \log \sigma\left( -\omega \left( \|\epsilon^w - \pi_\theta(x_t^w, t)\|_2^2 - \|\epsilon^w - \pi_{ref}(x_t^w, t)\|_2^2 - (\|\epsilon^l - \pi_\theta(x_t^l, t)\|_2^2 - \|\epsilon^l - \pi_{ref}(x_t^l, t)\|_2^2) \right) \right)$$

其优点在于通过一步去噪过程实现了像素级的隐式似然约束，能够精细地捕捉局部细节；缺点是需要预先收集“胜-负”偏好对，且优化信号仅来自两个样本的比较。GRPO则通过在线生成一组候选样本并计算群体相对优势来驱动优化，无需离线偏好数据，但其目标函数仅考虑全局轨迹似然比，缺乏像素级的细粒度约束。

**GDPO损失函数**将二者的优势进行了有机融合：

$$\mathcal{L}_{GDPO} = - \mathbb{E}_{x_0 \sim \mathcal{D}, x_t \sim q(x_t|x_0)} \log \sigma \left( -\omega \sum_{i=1}^G A_i \left( \|\epsilon - \pi_\theta(x_t, t)\|_2^2 - \|\epsilon - \pi_{ref}(x_t, t)\|_2^2 \right) \right)$$

其中群体相对优势 $A_i$ 由组内候选样本的奖励经标准化得到：

$$\mathcal{A}_i = \frac{R_i - \mathrm{mean}(\{R_j\}_{j=1}^G)}{\mathrm{std}(\{R_j\}_{j=1}^G)}$$

这一设计的精妙之处在于：**高奖励样本获得正优势权重，驱动策略模型增大其隐式似然；低奖励样本获得负优势权重，驱动策略模型抑制其生成概率**。与Diffusion-DPO相比，GDPO利用在线生成的样本组替代了离线偏好对，大幅降低了数据依赖；与GRPO相比，GDPO保留了像素级去噪差异的约束，能够更有效地学习局部纹理细节。消融实验（Table 5）证实，GDPO在RealSR数据集上同时优于Diffusion-DPO和DanceGRPO，实现了全参考与无参考指标更均衡的提升。

### Changed Slot 4：属性感知的奖励函数（ARF）

奖励函数定义了“什么是好的SR结果”，直接决定了偏好优化的方向。简单的单一指标或静态加权组合无法适应不同图像内容的需求：平滑区域（如天空、墙面）更关注保真度，而纹理丰富区域（如织物、文字）更需要感知质量的提升。

GDPO-SR的**属性感知奖励函数（ARF）** 通过分析HR图像的局部方差，将图像划分为平滑区域和纹理区域，并根据二者的面积占比 $\rho_s$ 和 $\rho_d$ 动态调整保真度指标（PSNR）与感知指标（MANIQA、MUSIQ）的权重：

$$R_i = \rho_s \sum_{f \in \mathcal{G}_{FR}} \frac{s_i^f}{|\mathcal{G}_{FR}|} + \rho_d \sum_{f \in \mathcal{G}_{NR}} \frac{s_i^f}{|\mathcal{G}_{NR}|}$$

当图像以平滑区域为主时，$\rho_s$ 较大，PSNR获得更高权重，模型更注重保真度；当纹理区域占主导时，$\rho_d$ 增大，MANIQA和MUSIQ的权重提升，模型更注重感知质量。消融实验（Table 6）表明，ARF相比仅使用全参考指标或仅使用无参考指标，均能取得更好的综合性能。

### 创新点的协同效应

上述四个changed slot并非孤立存在，而是构成了一个紧密耦合的创新体系：NAOSD为偏好优化提供了必要的输出多样性（没有它，GDPO将退化为对单一样本的无效优化）；不等时步策略在引入多样性的同时守住了保真度的下限（没有它，噪声注入将导致性能退化）；GDPO损失函数将群体相对优势与像素级约束结合，实现了高效且精细的偏好学习（没有它，优化信号要么依赖离线数据，要么缺乏局部细节）；ARF则为整个优化过程提供了内容自适应的奖励信号（没有它，优化方向可能偏离人类感知偏好）。这一协同效应使得GDPO-SR在无需大量离线偏好数据的情况下，在真实场景ISR中实现了更清晰、更丰富的纹理重建。

## 整体框架

GDPO-SR 的整体框架由两个核心阶段构成：**优势计算（Advantage Calculation）** 与 **策略优化（Policy Optimization）**。两个阶段协同工作，使单步生成式真实图像超分辨率模型能够在不依赖大量离线偏好数据的情况下，通过在线生成的多样化样本进行偏好学习。

### 阶段一：优势计算

该阶段的目标是为同一张低分辨率（LR）输入图像生成一组多样化的超分辨率（ISR）候选样本，并计算每个样本的群体相对优势。

具体流程如下：

1. **多样化样本生成**：以预训练的噪声感知一步扩散模型（NAOSD）作为参考模型，通过向潜在空间注入不同的随机噪声，为同一 LR 图像生成一组 $G$ 个 ISR 候选样本。噪声注入由参数 $t_{add}$ 控制，其公式为：

   $$\tilde{z} = \sqrt{\alpha_{t_{add}}} z_{LR} + \sqrt{\beta_{t_{add}}} \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I})$$

   扰动后的潜在特征 $\tilde{z}$ 随后在扩散时步 $t_{diff}$ 下经 UNet 去噪，得到恢复的潜在特征 $z_{SR}$：

   $$z_{SR} = \frac{ ( \tilde{z} - \sqrt{\beta_{t_{diff}}} ~ \mathrm{UNet}(\tilde{z}, c_t, t_{diff}) ) }{ \sqrt{\alpha_{t_{diff}}} }$$

2. **属性感知奖励计算**：对每个候选样本，使用属性感知奖励函数（ARF）计算其奖励值。ARF 根据图像中平滑区域和纹理区域的比例（$\rho_s$ 和 $\rho_d$），自适应地组合全参考指标（PSNR）和无参考指标（MANIQA、MUSIQ）：

   $$R_i = \rho_s \sum_{f \in \mathcal{G}_{FR}} \frac{s_i^f}{|\mathcal{G}_{FR}|} + \rho_d \sum_{f \in \mathcal{G}_{NR}} \frac{s_i^f}{|\mathcal{G}_{NR}|}$$

   其中 $\mathcal{G}_{FR}$ 和 $\mathcal{G}_{NR}$ 分别为全参考与无参考指标集合。平滑与纹理区域的划分通过图4所示的流程计算得到。

3. **群体相对优势标准化**：将组内所有候选样本的奖励值进行标准化，得到每个样本的群体相对优势 $\mathcal{A}_i$：

   $$\mathcal{A}_i = \frac{R_i - \mathrm{mean}(\{R_j\}_{j=1}^G)}{\mathrm{std}(\{R_j\}_{j=1}^G)}$$

   高奖励样本获得正优势，低奖励样本获得负优势，从而在后续优化中引导模型向高奖励方向对齐。

### 阶段二：策略优化

该阶段利用阶段一生成的样本组及计算出的相对优势 $\mathcal{A}$ 来更新策略模型（即待优化的 UNet）的参数。

核心机制是将 GRPO 的群体相对优势思想融入 Diffusion-DPO 的像素级隐式似然约束中，形成 GDPO 损失函数：

$$\mathcal{L}_{GDPO} = - \mathbb{E}_{x_0 \sim \mathcal{D}, x_t \sim q(x_t|x_0)} \log \sigma \left( -\omega \sum_{i=1}^G A_i \left( \|\epsilon - \pi_\theta(x_t, t)\|_2^2 - \|\epsilon - \pi_{ref}(x_t, t)\|_2^2 \right) \right)$$

该损失的直观含义是：对于优势为正的高奖励样本，模型被鼓励降低其去噪误差；对于优势为负的低奖励样本，模型被鼓励增加其去噪误差。通过像素级的去噪差异约束，GDPO 能够比仅依赖全局似然的 GRPO 更有效地学习局部细节。

### 模块关系与数据流

整个框架的模块组成与数据流可概括如下：

1. **VAE 编码器** 将 LR 图像映射到潜在空间：$z_{LR} = E(I_{LR})$。
2. **复合提示提取模块**（DAPE + CLIP 文本编码器）提取语义引导作为条件嵌入 $c_t$。
3. **噪声注入模块** 向 $z_{LR}$ 注入可控高斯噪声，产生扰动潜在特征 $\tilde{z}$。
4. **UNet 去噪模块** 在时步 $t_{diff}$ 对 $\tilde{z}$ 进行去噪，得到 $z_{SR}$。
5. **VAE 解码器** 将 $z_{SR}$ 映射回图像空间，得到 ISR 输出 $I_{SR}$。
6. **GDPO 优势计算模块** 为每组候选样本计算群体相对优势 $\mathcal{A}_i$。
7. **GDPO 策略优化模块** 利用 $\mathcal{L}_{GDPO}$ 更新策略 UNet 的参数，参考模型参数保持冻结。

这种设计使得 GDPO-SR 在继承 Diffusion-DPO 像素级精度优势的同时，获得了 GRPO 在线群体优化的效率，无需预先收集大量偏好对即可在真实场景 ISR 中实现更清晰、更丰富的纹理重建。

### 补充图表

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/002_Figure_2.jpg]]
*Figure 2: The framework of GDPO, which consists of two core stages: (a) advantage calculation and (b) policy optimization. Firstly, we employ a pre-trained one-step Real-ISR model as the reference model to generate a group of diverse outputs by injecting different random noises. Subsequently, we compute the advantage A for each sample by evaluating its reward with our designed attribute-aware reward functions and converting these rewards into group-relative advantages. In the policy optimization stage, we feed these samples along with noises into both the policy model and the reference ISR model, and update the parameters of the policy ISR model by minimizing the proposed GDPO loss, steering it to fa...*

## 核心模块与公式推导

### 噪声感知一步扩散模型（NAOSD）

GDPO-SR 的核心基座是一个**噪声感知一步扩散模型（Noise-Aware One-Step Diffusion, NAOSD）**，其设计目标是打破确定性一步超分辨率模型“输入 LR → 固定输出 HR”的映射模式，为后续的偏好优化提供**输出多样性**这一关键前提。

NAOSD 的推理管线由五个模块串联构成：

1. **VAE 编码器**：将低分辨率图像 $I_{LR}$ 映射到潜在空间，得到 $z_{LR} = E(I_{LR})$。
2. **复合提示提取模块**：整合 DAPE 和 CLIP 文本编码器，提取语义引导嵌入 $c_t$。
3. **噪声注入模块**：向潜在特征注入可控高斯噪声，扰动强度由时步参数 $t_{add}$ 决定：

   $$\tilde{z} = \sqrt{\alpha_{t_{add}}} \, z_{LR} + \sqrt{\beta_{t_{add}}} \, \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I}) \tag{3}$$

4. **UNet 去噪模块**：在扩散时步 $t_{diff}$ 对扰动后的潜在特征进行一步去噪：

   $$z_{SR} = \frac{\tilde{z} - \sqrt{\beta_{t_{diff}}} \, \mathrm{UNet}(\tilde{z}, c_t, t_{diff})}{\sqrt{\alpha_{t_{diff}}}} \tag{4}$$

5. **VAE 解码器**：将恢复的潜在特征 $z_{SR}$ 映射回图像空间，得到超分辨率输出 $I_{SR}$。

#### 不等时步策略：多样性与保真度的解耦

NAOSD 的核心创新在于引入**不等时步策略（Unequal-Timestep Strategy）**，将噪声添加时步 $t_{add}$ 与去噪时步 $t_{diff}$ 解耦。在理想去噪（UNet 完美预测噪声）的近似条件下，超分辨率潜在特征可表达为：

$$z_{SR} \approx \frac{\sqrt{\alpha_{t_{add}}}}{\sqrt{\alpha_{t_{diff}}}} z_{LR} + \frac{\sqrt{\beta_{t_{add}}} - \sqrt{\beta_{t_{diff}}}}{\sqrt{\beta_{t_{diff}}}} \epsilon \tag{6}$$

当 $t_{add} \neq t_{diff}$ 时，上述表达式中的第二项不为零，这意味着**输出中保留了与注入噪声 $\epsilon$ 相关的额外随机项**，从而赋予模型生成多样化样本的能力。实践中，论文采用 $t_{add} > t_{diff}$ 的设定（如 $t_{add}=250, t_{diff}=100$）——较大的 $t_{add}$ 拓展采样空间以引入多样性，而更保守的 $t_{diff}$ 则稳定保真度，避免噪声注入导致性能退化。

NAOSD 的预训练采用联合损失函数：

$$\mathcal{L}_{onestep} = L_1(I_{SR}, I_{HR}) + \lambda_1 L_{LPIPS}(I_{SR}, I_{HR}) + \lambda_2 L_{VSD}(I_{SR}, I_{HR}) \tag{5}$$

其中 $L_1$ 约束像素级保真度，$L_{LPIPS}$ 提升感知相似性，$L_{VSD}$（变分分数蒸馏）则利用预训练扩散模型的先验知识来稳定一步训练。

---

### GDPO 偏好优化框架

在 NAOSD 提供多样输出能力的基础上，GDPO 框架通过两阶段在线优化来引导模型偏向生成高质量样本。

#### 第一阶段：优势计算（Advantage Calculation）

对于同一张 LR 输入，参考模型（冻结的 NAOSD）通过注入 $G$ 组不同的随机噪声 $\{\epsilon_i\}_{i=1}^G$，生成一组 ISR 候选样本 $\{I_{SR}^i\}_{i=1}^G$。每个候选样本的奖励值由**属性感知奖励函数（Attribute-aware Reward Function, ARF）**计算：

$$R_i = \rho_s \sum_{f \in \mathcal{G}_{FR}} \frac{s_i^f}{|\mathcal{G}_{FR}|} + \rho_d \sum_{f \in \mathcal{G}_{NR}} \frac{s_i^f}{|\mathcal{G}_{NR}|} \tag{7}$$

其中：
- $\mathcal{G}_{FR}$ 为全参考指标集合，仅包含 **PSNR**（衡量像素级保真度）；
- $\mathcal{G}_{NR}$ 为无参考指标集合，包含 **MANIQA** 和 **MUSIQ**（衡量感知质量）；
- $\rho_s$ 和 $\rho_d$ 分别为图像中**平滑区域**和**纹理区域**的面积占比，通过 Canny 边缘检测从 LR 图像中计算得到。这一自适应加权机制使得：平滑区域多的图像更侧重保真度（PSNR 权重更大），纹理丰富的图像更侧重感知质量（MANIQA/MUSIQ 权重更大）。

随后，对组内所有候选样本的奖励值进行标准化，得到**群体相对优势（Group-Relative Advantage）**：

$$\mathcal{A}_i = \frac{R_i - \mathrm{mean}(\{R_j\}_{j=1}^G)}{\mathrm{std}(\{R_j\}_{j=1}^G)} \tag{8}$$

标准化操作使得优势值 $\mathcal{A}_i$ 反映的是样本在组内的相对质量：高于组内均值的样本获得正优势，低于均值的获得负优势。

#### 第二阶段：策略优化（Policy Optimization）

策略模型（待优化的 UNet，参数 $\theta$）和参考模型（冻结的 UNet，参数 $\theta_{ref}$）接收相同的噪声-样本对，GDPO 通过以下损失函数更新策略参数：

$$\mathcal{L}_{GDPO} = - \mathbb{E}_{x_0 \sim \mathcal{D}, x_t \sim q(x_t|x_0)} \log \sigma \left( -\omega \sum_{i=1}^G A_i \left( \|\epsilon - \pi_\theta(x_t, t)\|_2^2 - \|\epsilon - \pi_{ref}(x_t, t)\|_2^2 \right) \right) \tag{9}$$

**公式机理分析**：

- **像素级隐式似然约束**：$\|\epsilon - \pi_\theta(x_t, t)\|_2^2 - \|\epsilon - \pi_{ref}(x_t, t)\|_2^2$ 这一项继承自 Diffusion-DPO（公式1），通过一步去噪过程中的像素级 MSE 差异来隐式地比较策略模型与参考模型在给定样本上的似然。与 GRPO 仅计算全局图像似然不同，这种像素级约束使模型能够更精细地学习局部纹理细节。

- **群体相对优势加权**：每个样本的像素级差异被其群体相对优势 $A_i$ 加权。当样本 $i$ 的奖励高于组内均值时，$A_i > 0$，损失函数会驱动 $\pi_\theta$ 在该样本的噪声预测上向更小的去噪误差方向优化（即提升对该样本的生成偏好）；反之，低奖励样本的 $A_i < 0$ 则产生抑制效果。

- **与现有方法的本质区别**：GDPO 融合了 GRPO 的**在线群体采样效率**（无需预先构建离线偏好对）与 Diffusion-DPO 的**像素级精度**，避免了 GRPO 忽略局部细节和 DPO 依赖有限偏好数据的双重局限。

---

### 关键公式汇总

| 公式编号 | 名称 | 核心作用 |
|:---:|:---|:---|
| (3) | 噪声注入 | $t_{add}$ 控制多样性强度，$\epsilon$ 为随机种子 |
| (4) | 一步去噪 | $t_{diff}$ 控制去噪保守程度，输出 $z_{SR}$ |
| (6) | 近似解 | 揭示 $t_{add} \neq t_{diff}$ 时多样性来源的数学本质 |
| (7) | 属性感知奖励函数 | $\rho_s, \rho_d$ 自适应平衡 PSNR 与 MANIQA/MUSIQ |
| (8) | 群体相对优势 | 组内标准化，正优势驱动学习，负优势抑制 |
| (9) | GDPO 损失函数 | 优势加权像素级去噪差异，联合优化保真度与感知质量 |

### 补充图表

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/003_Figure_3.jpg]]
*Figure 3: The structure of NAOSD, which uses the*

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/004_Figure_4.jpg]]
*Figure 4: The pipeline of calculating smooth and detailed regions*

## 实验与分析

### 4.1 实验设置

GDPO-SR的训练分为两个阶段。第一阶段预训练基模型NAOSD：使用SD2.1-base作为预训练扩散模型，在4块NVIDIA A100 GPU上以批量大小16训练35,000次迭代。第二阶段GDPO偏好优化：在8块NVIDIA A100 GPU上，以批量大小1、群体规模G=6进行在线优化，参考模型为冻结的NAOSD。

评估在真实世界数据集（RealSR、DRealSR）和合成数据集上进行。指标涵盖全参考指标（PSNR、SSIM、LPIPS、DISTS、FID）和无参考指标（MANIQA、MUSIQ、CLIPIQA、AFINE）。所有与基模型NAOSD的比较（Table 1）均馈送相同的噪声以确保公平性，补充材料中还报告了50次随机运行的平均性能以说明随机噪声的方差。

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/005_Table_1.jpg]]
*Table 1: Performance comparison with the base model NAOSD on real-world and synthetic datasets. Metrics with a blue background denote those utilized in the reward function, while yellow-shaded ones correspond to metrics that are excluded from it. Arrows denote if higher (↑) or lower (↓) values represent better performance. The best results are highlighted in red*

### 4.2 与基模型的对比

Table 1展示了GDPO-SR与基模型NAOSD的性能对比。在RealSR数据集上，GDPO-SR在所有参与奖励函数的指标上均取得一致提升：PSNR从25.25dB提升至25.48dB（+0.23dB），MANIQA从0.6459提升至0.6615，MUSIQ从69.06提升至69.42。在DRealSR数据集上，PSNR从27.97dB提升至28.18dB（+0.21dB），FID从140.37降至138.87。值得关注的是，即使未纳入奖励函数的指标（如CLIPIQA、AFINE）也获得提升，表明GDPO的优化方向与人类感知评价具有内在一致性。

### 4.3 与先进方法的对比

Table 2报告了与主流真实图像超分辨率方法的全面对比。在RealSR数据集上，GDPO-SR取得了最优FID（112.13），相比OSEDiff（123.49）降低了11.36，同时DISTS（0.1980）和LPIPS（0.2675）也优于所有对比方法。在DRealSR数据集上，GDPO-SR在PSNR（28.18dB）、SSIM（0.7839）、MUSIQ（65.63）和CLIPIQA（0.7020）四项指标上均排名第一。与基于扩散的多步方法（StableSR、DiffBIR、SeeSR）相比，GDPO-SR以单步推理实现了有竞争力的感知质量。

Table 3专门对比了基于偏好优化的方法DP2O-SR（Wu et al., NeurIPS 2025）。在DRealSR上，GDPO-SR的PSNR达到28.18dB，远超DP2O-SR的23.95dB（+4.23dB），同时MANIQA和MUSIQ也显著领先，验证了群体相对优势与像素级约束结合的有效性。

Table 4比较了模型效率。GDPO-SR的参数量和FLOPs与OSEDiff相当，但推理时间显著短于多步扩散方法（DiffBIR、SeeSR），体现了单步模型在部署上的优势。

### 4.4 消融研究

**偏好优化策略对比（Table 5）。** 在RealSR数据集上，GDPO同时优于Diffusion-DPO和DanceGRPO。Diffusion-DPO受限于离线偏好对的质量和覆盖范围，DanceGRPO仅计算全局似然而忽略局部细节。GDPO通过在线生成样本组并施加像素级约束，在PSNR（25.48dB vs. 25.36dB/25.31dB）和MANIQA（0.6615 vs. 0.6471/0.6492）上均取得最佳。

**属性感知奖励函数（Table 6）。** ARF组合PSNR、MANIQA和MUSIQ，并根据图像中平滑区域与纹理区域的比例（通过Figure 4的流程计算）自适应加权。消融显示：仅使用全参考指标（PSNR-only）导致感知质量下降；仅使用无参考指标（NR-only）则保真度显著退化；ARF在PSNR（25.48dB）和MANIQA（0.6615）之间取得了最佳平衡。

**群体规模（Table 7）。** 群体规模G=6在生成能力与计算开销之间达到最优。G=4时多样性不足导致优化信号较弱，G=8时性能提升趋于饱和但计算成本线性增加。

**噪声注入时步（Table 10）。** t_add控制噪声注入强度，进而调节生成多样性。t_add越大，无参考指标越好（MANIQA从0.6462升至0.6675），但PSNR从25.54dB降至25.32dB。这提供了保真度与感知质量之间的可控权衡机制，但当前需要手动调整t_add。

**样本生成方式（Table 11）。** 对比了通过改变注入噪声、CFG参数和t_add三种方式生成多样本。改变注入噪声在PSNR和MANIQA上均带来一致改进，而改变CFG或t_add则导致某一类指标的退化，验证了噪声注入作为多样性来源的优越性。

**全参考指标选择（Table 9）。** 在ARF中，以PSNR作为全参考指标优于SSIM和LPIPS，因为PSNR对像素级保真度的约束更直接，与扩散模型的去噪目标一致。

### 4.5 稳定性分析

Table 8报告了50次随机运行的平均性能。GDPO-SR在PSNR（25.49±0.04dB）和MANIQA（0.6613±0.0007）上均表现出极低的方差，证明噪声注入带来的随机性不会导致输出质量的大幅波动，偏好优化后的模型对噪声具有鲁棒性。

### 4.6 视觉质量分析

Figure 5展示了与基于SD的真实ISR方法的视觉对比。GDPO-SR在砖墙纹理、文字边缘等高频区域重建出更清晰、更规则的细节，而OSEDiff和StableSR的结果存在模糊或伪影。Figure 6与DP2O-SR的对比显示，GDPO-SR在保持结构保真度的同时生成了更自然的纹理。

### 4.7 失败模式与局限性

尽管GDPO-SR在整体指标上表现优异，仍存在以下局限：

1. **奖励函数与人类感知的差距**：当前ARF由PSNR、MUSIQ和MANIQA组合而成，这些指标无法完全捕捉人类对图像质量的偏好。在某些场景下，模型可能生成高指标得分但视觉上不自然的纹理。
2. **计算资源需求**：GDPO训练依赖8块A100 GPU，单步推理的FLOPs与OSEDiff相当，可能限制在边缘设备上的部署。
3. **t_add的手动调节**：生成能力的控制参数t_add需要根据场景手动调整以获得保真度与真实感的最佳平衡，缺乏自适应机制。
4. **退化泛化性**：当前仅在有限种类的真实退化场景上验证，对更复杂、更未见过的退化的泛化能力有待进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison with DP2O-SR on real-world datasets. The best results are highlighted in red*

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/012_Table_5.jpg]]
*Table 5: Ablation studies on GDPO on the RealSR dataset*

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/011_Table_6.jpg]]
*Table 6: Ablation studies on ARF on the RealSR dataset*

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/013_Table_7.jpg]]
*Table 7: Ablation studies on Group Size on the RealSR dataset*

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/009_Table_4.jpg]]
*Table 4: Comparison of mode size, running-time and FLOPs*

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/016_Table_9.jpg]]
*Table 9: Ablation studies on FR metrics on the RealSR dataset*

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/017_Table_10.jpg]]
*Table 10: The impact of*

![[assets/figures/papers/paper_list_l2679_https_arxiv_org_abs_2603_16769/figures/018_Table_11.jpg]]
*Table 11: Ablation study on sample generation methods on the Real-ISR dataset. Arrows denote if higher (↑) or lower (↓) values represent better performance*

## 方法谱系与知识库定位

### 问题定位：单步生成式ISR的多样性困境与偏好优化空白

真实图像超分辨率（Real-ISR）领域长期存在两条技术路线：基于GAN的方法追求感知质量但易产生伪影，基于扩散模型的方法保真度更高但推理成本大。近年来，以**OSEDiff**为代表的单步扩散模型大幅降低了推理开销，却引入了一个被忽视的瓶颈——确定性映射使模型丧失了输出多样性。这种“一对一”的映射不仅限制了生成能力，更关键的是，它阻断了基于偏好的强化学习（RL）方法的直接应用：DPO依赖离线构建的偏好对，而GRPO虽然支持在线群体优化，却仅计算全局图像似然，无法精细建模像素级局部细节。

GDPO-SR正是瞄准这一空白：如何在单步生成式ISR中同时获得**多样性输出**与**精细的偏好优化**？

### 方法谱系：从扩散DPO到群体优势优化

GDPO-SR的方法设计建立在对两条技术路线的融合与改进之上：

**扩散偏好优化路线。** Diffusion-DPO（公式1）将DPO从语言模型扩展到扩散模型，通过一步去噪过程的像素级约束实现偏好学习。其核心优势在于隐式似然计算带来的精度，但劣势同样明显——必须依赖离线收集的偏好对，无法利用在线生成的多样化样本进行探索。

**群体优势优化路线。** GRPO（公式2）通过在线生成一组候选样本，利用组内标准化的相对优势进行策略更新，避免了离线偏好对的依赖。然而，当扩展至流匹配模型时，其目标函数仅对全局轨迹似然进行加权，忽略了像素级的局部细节约束，这在需要精细纹理重建的ISR任务中尤为致命。

**GDPO的融合策略。** GDPO的核心洞察在于将GRPO的群体相对优势机制“嫁接”到Diffusion-DPO的像素级约束框架中（公式9）。具体而言，它通过在线生成一组ISR候选样本，计算每个样本的群体相对优势$A_i$（公式8），然后将该优势作为权重作用于像素级去噪差异。这使得模型能够优先学习高奖励样本对应的去噪模式，既保留了像素级约束的精度，又获得了在线群体探索的效率。消融实验（Table 5）直接验证了这一融合的有效性：GDPO在RealSR数据集上同时优于纯粹的Diffusion-DPO和DanceGRPO。

### 基模型与噪声注入：从确定性到可控多样性

GDPO-SR的基模型NAOSD本身就是一个关键创新。传统单步扩散模型在潜在空间中执行确定性映射$z_{LR} \to z_{SR}$，而NAOSD通过向潜在特征注入可控高斯噪声（公式3）打破了这种确定性。其核心设计在于**不等时步策略**（unequal-timestep strategy）：噪声注入的时步$t_{add}$与去噪时步$t_{diff}$解耦，且$t_{add} > t_{diff}$。近似解（公式6）清晰地揭示了这一设计的数学本质——当$t_{add} \neq t_{diff}$时，恢复的潜在特征中存在额外的噪声项$\frac{\sqrt{\beta_{t_{add}}} - \sqrt{\beta_{t_{diff}}}}{\sqrt{\beta_{t_{diff}}}} \epsilon$，这正是输出多样性的来源。同时，更保守的$t_{diff}$又保证了去噪过程的稳定性，避免了噪声注入带来的保真度崩溃。

### 奖励设计：属性感知的保真-感知平衡

与DP2O-SR（Wu et al., NeurIPS 2025）等多步偏好优化方法不同，GDPO-SR的奖励函数设计体现了对ISR任务特性的深入理解。属性感知奖励函数（ARF，公式7）的核心思想是：图像不同区域对保真度和感知质量的要求不同——平滑区域（如天空、墙面）更需要保真度约束，而纹理区域（如砖墙、织物）则更依赖感知质量。ARF通过计算平滑区域比例$\rho_s$和纹理区域比例$\rho_d$（Figure 4展示了该计算流程），动态调整全参考指标（PSNR）和无参考指标（MANIQA、MUSIQ）的权重。消融实验（Table 6）表明，这种自适应加权策略优于仅使用全参考或仅使用无参考指标的静态组合。

### 与相关工作的关系边界

**与多步扩散ISR方法的关系。** StableSR、DiffBIR、SeeSR等基于SD的多步方法在PSNR和SSIM等全参考指标上通常更优，但推理成本高出1-2个数量级。GDPO-SR在单步推理的约束下，通过偏好优化缩小了与多步方法的感知质量差距（Table 2中FID达到112.13，优于OSEDiff的123.49），同时保持了显著的计算效率优势（Table 4）。

**与DP2O-SR的关系。** DP2O-SR（Wu et al., NeurIPS 2025）是另一个将偏好优化引入ISR的工作，但基于多步扩散框架。GDPO-SR与DP2O-SR的关键区别在于：前者在单步模型中通过噪声注入获得多样性，后者依赖多步采样过程；前者的GDPO损失直接作用于一步去噪过程，后者的优化涉及完整的多步轨迹。在DRealSR数据集上，GDPO-SR的PSNR达到28.18 dB，显著高于DP2O-SR的23.95 dB（Table 3）。

**与GAN-based方法的关系。** 在Table 12的补充比较中，GDPO-SR在感知质量指标上展现出与最先进GAN方法的竞争力，同时在保真度指标上保持优势，体现了扩散模型先验与偏好优化的协同效应。

### 适用边界与局限

1. **奖励函数与人类感知的差距。** 当前ARF由PSNR、MANIQA和MUSIQ组合而成，这些指标虽与人类感知相关，但并非完全一致。在复杂纹理或语义敏感场景下，模型可能优化出指标高但视觉不自然的结果。这是整个生成式ISR领域的共性问题，而非GDPO-SR独有。

2. **计算资源门槛。** GDPO训练需要8块A100 GPU，且群体生成增加了训练时的计算开销。虽然推理阶段保持单步效率，但训练成本限制了在资源受限场景下的应用和复现。

3. **噪声控制的手动性。** 生成能力的控制参数$t_{add}$需要手动调整以平衡保真度与真实感（Table 10展示了$t_{add}$对指标的影响），缺乏任务自适应的自动化机制。这在实际部署中增加了调参负担。

4. **退化泛化性未充分验证。** 当前实验主要在RealSR和DRealSR等标准真实退化数据集上进行，对更复杂、更未见过的退化类型（如老照片修复、极端压缩伪影）的泛化能力仍是一个开放问题。

### 开放问题与未来方向

1. **奖励函数的人本化。** 如何设计更接近人类视觉感知的奖励函数，是提升生成质量天花板的关键。可能的路径包括引入视觉-语言模型（VLM）作为判别器，或利用人类反馈数据进行奖励建模。

2. **框架的任务泛化。** GDPO的“噪声注入-群体优化”范式是否可扩展到视频超分辨率、图像修复、去模糊等其它底层视觉任务？这需要验证噪声注入在不同任务潜在空间中的有效性。

3. **样本生成效率的提升。** 当前通过注入不同随机噪声生成群体样本，是否存在更高效的多样性生成策略？例如，在潜在空间中进行结构化扰动或学习多样性先验，可能进一步降低计算开销。

4. **更大规模预训练模型的潜力。** 论文提及利用更大规模、更先进的预训练扩散模型（如FLUX）可能进一步突破性能上限。这涉及一个更根本的问题：更强的生成先验能否降低对偏好优化的依赖，还是两者之间存在互补关系？

## 原文 PDF

![[paperPDFs/CVPR_2026/GDPO_SR_Group_Direct_Preference_Optimization_for_One_Step_Generative_Image_Super_Resolution.pdf]]
