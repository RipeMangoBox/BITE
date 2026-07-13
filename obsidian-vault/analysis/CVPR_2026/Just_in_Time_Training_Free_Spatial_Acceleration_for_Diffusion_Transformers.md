---
title: "Just-in-Time: Training-Free Spatial Acceleration for Diffusion Transformers"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Just_in_Time_Training_Free_Spatial_Acceleration_for_Diffusion_Transformers.pdf
project_link: "https://wenhao-sun77.github.io/JiT/"
code_link: null
aliases:
- JTJ
- Just-in-Time
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过动态选择稀疏的锚点token（anchor tokens）进行Transformer计算，并用外推插值算子将速度场扩展到全空间，从而在早期阶段大幅减少计算量；同时引入确定性微流（DMF）确保新增token的平滑激活与统计一致性，避免因空间降维带来的结构断裂与噪声不匹配。
primary_logic: 利用扩散模型由粗到细的生成特性，将空间计算资源按需分配：早期仅对少量关键token计算并外推全场速度，后期逐步激活细节区域，结合一致性保证的SAG-ODE与无缝的DMF转换，实现训练无关、高加速比且几乎无损的图像生成。
claims:
- JiT在FLUX.1-dev上实现7倍加速，且性能几乎无损。
- SAG-ODE在锚点token上的动力学是精确的，外推近似不影响锚点区域。
- 消融实验证明去除空间近似项（SAG-ODE）会导致生成质量灾难性崩溃。
- DMF通过构造合适的初始目标状态和有限时间ODE，有效防止了阶段转换产生的artifacts。
---

# Just-in-Time: Training-Free Spatial Acceleration for Diffusion Transformers

> [!tip] 核心洞察
> 利用扩散模型由粗到细的生成特性，将空间计算资源按需分配：早期仅对少量关键token计算并外推全场速度，后期逐步激活细节区域，结合一致性保证的SAG-ODE与无缝的DMF转换，实现训练无关、高加速比且几乎无损的图像生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 即时生成：扩散Transformer的训练无关空间加速框架 |
| 英文题名 | Just-in-Time: Training-Free Spatial Acceleration for Diffusion Transformers |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.10744) · [Project](https://wenhao-sun77.github.io/JiT/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Just-in-Time (JiT) |
| Dataset | FLUX.1-dev ~4× 加速对比, FLUX.1-dev ~7× 加速对比 |

> [!tip] 效果简介
> - FLUX.1-dev ~4× 加速对比 上，CLIP-IQA ↑ 0.6166 vs 0.6139 (FLUX.1-dev 50 NFE) (+0.0027)；Image Reward ↑ 1.017 vs 1.004 (FLUX.1-dev 50 NFE) (+0.013)；TFLOPs ↓ 706.17 vs 2990.96 (FLUX.1-dev 50 NFE) (-76.4%)。
> - FLUX.1-dev ~7× 加速对比 上，CLIP-IQA ↑ 0.5397 vs 0.4134 (FLUX.1-dev 7 NFE) (+0.1263)；GenEval ↑ 0.6457 vs 0.5629 (FLUX.1-dev 7 NFE) (+0.0828)。

## 概要

扩散Transformer（Diffusion Transformer, DiT）已成为高分辨率图像与视频生成的主流骨干，但其在推理阶段对所有空间token施加均匀的Transformer计算，忽视了扩散模型由粗到细的生成特性——早期步骤主要构建全局低频结构，细节信息仅在后期才逐步涌现。这一空间冗余导致大量计算被浪费在非关键区域，成为制约DiT高效部署的核心瓶颈。

针对上述问题，本文提出**Just-in-Time (JiT)**，一个训练无关、即插即用的空间加速框架。JiT的核心思想是：在生成过程中动态选择稀疏的**锚点token**进行Transformer计算，并通过外推插值算子将速度场扩展到全空间，从而在早期阶段大幅减少计算量；同时引入**确定性微流（Deterministic Micro-Flow, DMF）**确保新增token的平滑激活与统计一致性，避免因空间降维带来的结构断裂与噪声不匹配。

JiT框架由三个关键机制构成：（1）**空间近似生成ODE（SAG-ODE）**，仅对稀疏锚点token计算Transformer速度场，并利用增强提升算子外推全场演化；（2）**重要性引导的token激活（ITA）**，依据速度场局部分差动态选择高信息密度区域优先激活；（3）**确定性微流（DMF）**，在阶段转换时通过有限时间ODE将新token从插值状态平滑驱动到统计正确的目标状态。三者协同，实现了按需分配空间计算资源、由粗到细的生成策略。

实验表明，JiT在**FLUX.1-dev**模型上可实现**最高约7倍加速**，且性能几乎无损：在~4×加速设置下，CLIP-IQA达到0.6166，略高于全计算基线的0.6139，ImageReward从1.004提升至1.017；在~7×加速设置下，CLIP-IQA（0.5397 vs. 0.4134）和GenEval（0.6457 vs. 0.5629）均显著优于等NFE的朴素加速基线。消融实验进一步验证了SAG-ODE的空间近似项、ITA的动态激活策略以及DMF的目标构建对生成质量的关键作用——移除任一组件的会导致结构崩塌、语义错误或噪声伪影。此外，JiT在Qwen-image和HunyuanVideo-1.5上的跨模型泛化实验初步展示了该方法在图像与视频生成领域的广泛适用性。

**方法定位**：JiT属于扩散模型推理加速中的**空间稀疏计算**路线，与时间域加速方法（高阶求解器、蒸馏、缓存重用）正交互补。相较于Bottleneck Sampling、RALU等空间加速基线，JiT无需额外训练或架构修改，且通过SAG-ODE的精确锚点动力学保证和DMF的阶段转换一致性，在高加速比下仍能维持语义完整性与细节保真度。

### 扩散Transformer的空间冗余困境

扩散模型已成为视觉生成的主流范式，而基于Transformer架构的扩散骨干网络（Diffusion Transformer, DiT）凭借其强大的扩展性和生成质量，正逐步取代传统的U-Net架构。然而，DiT的高质量生成伴随着高昂的计算代价：在每一个去噪时间步，Transformer需要对**全部空间token**进行自注意力计算，导致计算量与token数量的平方成正比。以FLUX.1-dev为例，标准50步采样需消耗近3000 TFLOPs的计算量，严重制约了实际部署效率。

现有加速策略主要沿两个方向展开：**时间域加速**（如减少采样步数、高阶ODE求解器、蒸馏）和**缓存复用**（如跨步特征重用）。这些方法虽然有效，却忽视了一个关键的结构性冗余——**空间冗余**。

### 由粗到细的生成本质：被忽视的时空不对称性

扩散模型的生成过程天然遵循**由粗到细**的动力学：在早期去噪阶段，模型主要建立全局低频结构（如物体轮廓、空间布局），细节纹理在后期才逐步显现。这意味着，早期对所有空间token施加均匀的Transformer计算是高度冗余的——大量token在全局结构尚未确立时，其局部细节计算对最终生成质量贡献甚微。

这一观察揭示了一个根本性的**时空不对称性**：时间域上的粗粒度（早期噪声大、结构模糊）与空间域上的细粒度（全分辨率token计算）之间存在严重错配。现有空间加速尝试（如**Bottleneck Sampling**的低分辨率隐式编码、**RALU**的金字塔升采样策略）虽然触及了这一问题，但普遍依赖显式的上下采样操作和分布校正步骤，难以在加速比与生成质量之间取得理想平衡，且缺乏对锚点token演化一致性的理论保证。

### 核心瓶颈与本文动机

本文的核心判断是：扩散Transformer加速的瓶颈不在于“能否少算”，而在于“**如何在不破坏生成动力学的条件下少算**”。具体而言，挑战来自三个层面：

1. **一致性保证**：对未激活token的速度场进行近似时，必须确保锚点token自身的演化不被污染，否则将导致结构断裂与误差累积。
2. **无缝阶段转换**：当新增token被激活以扩展空间维度时，如何将其状态平滑融入当前演化轨迹，避免噪声水平不匹配和视觉artifacts。
3. **自适应资源分配**：如何根据内容复杂度动态决定哪些空间区域需要优先激活，而非依赖静态的均匀网格划分。

基于上述分析，本文提出**Just-in-Time (JiT)** 框架——一种训练无关的空间加速方法，其核心思想是：**利用扩散模型由粗到细的生成特性，将空间计算资源按需分配，早期仅对少量关键token计算并外推全场速度，后期逐步激活细节区域，实现高加速比且几乎无损的图像生成**。

## 核心方法与创新机理

JiT框架的核心创新在于**首次将扩散模型“由粗到细”的生成特性系统性地转化为空间计算资源的动态调度机制**，实现了对扩散Transformer（DiT）的训练无关、高加速比且几乎无损的加速。其关键突破可归结为三个紧密耦合的“changed slots”：

### 1. 空间近似生成ODE（SAG-ODE）：稀疏锚点驱动全场演化

传统DiT在每一步对全部 $N$ 个token执行Transformer计算以获得全场速度场 $\mathbf{u}_{\theta}(\mathbf{y}(t), t)$。JiT的核心洞察是：**早期生成阶段主要建立全局低频结构，此时对全空间施加均匀计算存在严重冗余**。SAG-ODE将这一观察形式化为一个空间近似的生成ODE：

$$\frac{\mathrm{d}\mathbf{y}(t)}{\mathrm{d}t} = \Pi_{k} \mathbf{u}_{\theta}( \mathbf{S}_{k}^{\top} \mathbf{y}(t), t )$$

其中 $\mathbf{S}_{k}^{\top}$ 仅选取当前阶段 $k$ 的 $m_k$ 个锚点token输入Transformer，增强提升算子 $\Pi_{k}$ 再将稀疏速度嵌入全空间：

$$\Pi_{k} \mathbf{u}_{\theta} := \mathbf{S}_{k} \mathbf{u}_{\theta} + \mathcal{T}_{k}(\mathbf{u}_{\theta})$$

这里 $\mathcal{T}_{k}$ 通过最近邻插值与可控高斯模糊将锚点速度外推至未激活token区域。该设计的**决定性优势**在于其数学一致性——锚点token自身的动力学完全由Transformer精确给出（$\mathbf{S}_{k}^{\top}(\Pi_{k}\mathbf{u}_{\theta}) = \mathbf{u}_{\theta}$），外推近似仅作用于非锚点区域，从根源上避免了误差向关键token的扩散。

### 2. 重要性引导的Token激活（ITA）：内容感知的资源分配

传统方法对所有空间区域不加区分地均匀处理。JiT引入ITA策略，**依据速度场的局部分差动态识别高信息密度区域**，优先为其分配计算资源。重要性图的计算基于速度预测在时间窗口内的方差：

$$\mathbf{I}(t) = \mathbb{E}_{\mathcal{W}}[\mathbf{u}_{\theta}\odot\mathbf{u}_{\theta}] - (\mathbb{E}_{\mathcal{W}}[\mathbf{u}_{\theta}])\odot(\mathbb{E}_{\mathcal{W}}[\mathbf{u}_{\theta}])$$

这一设计使得token激活从“静态规则化”转变为“内容自适应”：纹理复杂、结构变化剧烈的区域被优先激活，而平坦均匀区域的计算被推迟至后期阶段。消融实验证实，移除ITA（改用静态激活模式）会导致复杂纹理区域出现artifacts和锐度损失。

### 3. 确定性微流（DMF）：无缝的阶段转换机制

当从稀疏token集切换到更密集的token集时，传统方法依赖显式的上采样/下采样算子配合分布校正步骤，容易引入结构断裂与噪声水平不匹配。JiT的DMF通过一个**有限时间ODE**在极短时间窗口 $[T_k-\delta, T_k]$ 内将新激活token从插值状态平滑驱动至统计正确的目标状态：

$$\mathbf{Q}_{k}\dot{\mathbf{y}}(t) = \frac{\mathbf{y}_{k}^{\star} - \mathbf{Q}_{k}\mathbf{y}(t)}{T_{k} - t}$$

其中目标状态 $\mathbf{y}_{k}^{\star}$ 融合了结构先验（由已激活token预测的干净图像经插值得到）与正确的噪声水平，确保新token在激活瞬间即具备结构连贯性和统计一致性。消融实验表明，移除DMF目标构建（直接使用插值值）会导致噪声水平不匹配，生成质量明显下滑。

### 创新耦合与系统效应

上述三个changed slots并非孤立运作，而是形成了一条完整的因果链：**SAG-ODE定义了稀疏计算下的演化规则，ITA决定了“在哪里”以及“何时”增加计算密度，DMF保证了密度切换时的状态连续性**。三者共同实现了JiT的核心理念——将扩散模型固有的由粗到细生成过程，转化为一个训练无关、可按需配置的空间加速框架。在FLUX.1-dev上，这一设计实现了最高7倍的加速，且性能几乎无损。

JiT框架的核心思想是利用扩散Transformer由粗到细的生成特性，将空间计算资源按需分配：在生成早期仅对少量关键token进行精确的Transformer计算，并通过外推算子将速度场扩展到全空间；随着生成推进，逐步激活更多token以刻画细节。该框架由三个核心模块串联构成，形成一条完整的训练无关加速pipeline。

**输入与输出流**：给定一个预训练的DiT模型（如FLUX.1-dev）和一个文本prompt，JiT的输入是初始噪声隐变量 $\mathbf{y}(0) \sim \mathcal{N}(0, \mathbf{I})$，输出是经过ODE数值积分得到的最终隐变量 $\mathbf{y}(1)$，随后通过标准VAE解码器还原为图像。整个过程无需对DiT模型进行任何微调或蒸馏。

**模块关系与数据流**：

1. **空间近似生成ODE（SAG-ODE）** 是驱动隐变量演化的核心引擎。在每一阶段 $k$，SAG-ODE仅将当前激活的锚点token子集 $\mathbf{S}_k^\top \mathbf{y}(t)$ 送入Transformer计算速度场 $\mathbf{u}_\theta$，再通过增强提升算子 $\Pi_k$ 将速度外推至全空间：
   $$\frac{\mathrm{d}\mathbf{y}(t)}{\mathrm{d}t} = \Pi_k \mathbf{u}_{\theta}( \mathbf{S}_k^\top \mathbf{y}(t), t )$$
   其中 $\Pi_k \mathbf{u}_\theta := \mathbf{S}_k \mathbf{u}_\theta + \mathcal{T}_k(\mathbf{u}_\theta)$，$\mathbf{S}_k \mathbf{u}_\theta$ 保留锚点token的精确速度，$\mathcal{T}_k$ 通过插值算子为未激活token生成近似速度。该设计保证了锚点token的动力学完全由Transformer精确给出（$\mathbf{S}_k^\top(\Pi_k\mathbf{u}_\theta) = \mathbf{u}_\theta$），从而在稀疏计算下维持结构一致性。

2. **重要性引导的token激活（ITA）** 负责在阶段转换时决定哪些新token被激活。ITA通过计算速度场的局部方差来量化各空间区域的信息密度：
   $$\mathbf{I}(t) = \mathbb{E}_{\mathcal{W}}[\mathbf{u}_{\theta}\odot\mathbf{u}_{\theta}] - (\mathbb{E}_{\mathcal{W}}[\mathbf{u}_{\theta}])\odot(\mathbb{E}_{\mathcal{W}}[\mathbf{u}_{\theta}])$$
   选择方差最大的 $m_{k-1} - m_k$ 个token加入激活集，确保计算资源优先分配给动态变化最剧烈的区域。

3. **确定性微流（DMF）** 在阶段转换的极短时间窗口 $[T_k-\delta, T_k]$ 内运行，将新激活token从插值状态平滑驱动到统计正确的目标状态 $\mathbf{y}_k^\star$：
   $$\mathbf{Q}_k\dot{\mathbf{y}}(t) = \frac{\mathbf{y}_k^\star - \mathbf{Q}_k\mathbf{y}(t)}{T_k - t}$$
   其中目标状态 $\mathbf{y}_k^\star$ 融合了结构先验（通过插值算子 $\Phi_k$ 从当前预测的干净图像 $\hat{\mathbf{y}}(1)$ 中提取）与正确的噪声水平（通过时间步 $T_k$ 加权混合高斯噪声 $\boldsymbol{\epsilon}$），有效防止了阶段转换产生的artifacts和噪声不匹配。

**整体调度逻辑**：JiT采用嵌套的token索引层次结构 $\Omega_K \subset \Omega_{K-1} \subset \cdots \subset \Omega_0 = \{1,2,\ldots,N\}$，配合Beta分布扭曲的时间步调度（$\alpha=1.4, \beta=0.42$），将计算偏置于早期全局结构建立阶段。默认的3阶段调度在加速比与质量之间取得了最优平衡——早期以约35%的token建立全局低频结构，中期扩展至约62%刻画主要细节，最后阶段激活全部token进行精细完善。完整的采样流程如Algorithm 1所示，交替执行SAG-ODE积分、ITA激活和DMF转换，最终以显著降低的FLOPs（如4×加速下仅706.17 TFLOPs，相比基线2990.96 TFLOPs降低76.4%）实现几乎无损的生成质量。

### 核心设计理念

扩散Transformer在生成过程中对所有空间区域施加均匀计算，忽视了扩散模型由粗到细的生成特性——早期主要建立全局低频结构，细节在后期才逐渐出现。JiT框架的核心洞察在于：**将空间计算资源按需分配**，早期仅对少量关键token进行Transformer计算并外推全场速度，后期逐步激活细节区域，从而实现训练无关的高加速比生成。

### 空间近似生成ODE (SAG-ODE)

SAG-ODE是JiT驱动隐变量演化的核心模块。传统流动匹配框架中，token化隐变量 $\mathbf{y}(t)$ 的演化由全场ODE控制：

$$\frac{\mathrm{d}\mathbf{y}(t)}{\mathrm{d}t} = \mathbf{u}_{\theta}(\mathbf{y}(t), t), \quad t \in [0,1]$$

其中 $\mathbf{u}_{\theta}$ 是Transformer预测的速度场。JiT将其改造为仅依赖稀疏锚点token计算的空间近似版本：

$$\frac{\mathrm{d}\mathbf{y}(t)}{\mathrm{d}t} = \Pi_{k} \mathbf{u}_{\theta}( \mathbf{S}_{k}^{\top} \mathbf{y}(t), t )$$

其中 $\mathbf{S}_{k}$ 是第 $k$ 阶段的选择矩阵，仅提取 $m_k$ 个锚点token送入Transformer；$\Pi_k$ 是增强提升算子（Augmented Lifter），负责将锚点速度嵌入全空间并外推至未激活token：

$$\Pi_{k} \mathbf{u}_{\theta} := \mathbf{S}_{k} \mathbf{u}_{\theta} + \mathcal{T}_{k}(\mathbf{u}_{\theta})$$

$\mathcal{T}_k$ 是插值算子，利用最近邻插值+可控高斯模糊将锚点token的速度场扩展到全场，保留锚点位置的精确值，平滑过渡区域。

**关键性质**：SAG-ODE在锚点token上的动力学是精确的：

$$\mathbf{S}_{k}^{\top}(\Pi_{k}\mathbf{u}_{\theta}) = \mathbf{u}_{\theta}$$

这意味着锚点token的演化完全由Transformer精确给出，不受插值近似影响。消融实验证实，移除空间近似项（即将未激活token速度设为零）会导致生成质量灾难性崩溃——未激活区域无法形成连贯结构。

### 确定性微流 (DMF)

当采样进入新阶段、需要激活更多token时，隐状态维度从 $m_{k-1}$ 扩展到 $m_k$。直接使用插值值初始化新token会导致噪声水平不匹配和结构断裂。JiT提出**确定性微流**（Deterministic Micro-Flow），在极短时间窗口 $[T_k - \delta, T_k]$ 内，通过有限时间ODE将新激活token从插值状态平滑驱动至统计正确的目标状态。

新token的目标状态 $\mathbf{y}_k^{\star}$ 融合结构先验与正确噪声水平：

$$\mathbf{y}_{k}^{\star} = \mathbf{Q}_{k}\left(T_{k}\Phi_{k}( \mathbf{S}_{k}^{\top}\hat{\mathbf{y}}(1) ) + (1-T_{k})\boldsymbol{\epsilon}\right)$$

其中 $\mathbf{Q}_k = \mathbf{P}_{k-1} - \mathbf{P}_k$ 是投影到新激活token子空间的算子，$\Phi_k$ 是插值算子，$\hat{\mathbf{y}}(1)$ 是预测的干净数据隐变量，$\boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$ 是标准高斯噪声，$T_k$ 是当前时间步。该目标在 $T_k$ 较大（早期）时偏向结构先验，在 $T_k$ 较小（后期）时偏向噪声，自然匹配扩散过程的噪声调度。

DMF的演化ODE为：

$$\mathbf{Q}_{k}\dot{\mathbf{y}}(t) = \frac{\mathbf{y}_{k}^{\star} - \mathbf{Q}_{k}\mathbf{y}(t)}{T_{k} - t}, \quad t \in [T_{k}-\delta, T_{k}]$$

该ODE在 $t \to T_k$ 时驱动 $\mathbf{Q}_k\mathbf{y}(t) \to \mathbf{y}_k^{\star}$，保证阶段转换无缝且无artifact。消融实验表明，移除DMF目标构建（直接使用插值值）会导致噪声水平不匹配，质量明显下滑。

### 重要性引导的Token激活 (ITA)

ITA负责在阶段转换时动态选择应激活的新token。其核心依据是速度场的局部方差——高方差区域对应信息密度高、结构变化剧烈的空间位置，应优先分配计算资源。

重要度图 $\mathbf{I}(t)$ 通过对近期速度预测窗口 $\mathcal{W}$ 计算方差得到：

$$\mathbf{I}(t) = \mathbb{E}_{\mathcal{W}}[\mathbf{u}_{\theta}\odot\mathbf{u}_{\theta}] - (\mathbb{E}_{\mathcal{W}}[\mathbf{u}_{\theta}])\odot(\mathbb{E}_{\mathcal{W}}[\mathbf{u}_{\theta}])$$

其中 $\odot$ 表示逐元素乘积。新激活token的索引集 $\mathcal{R}_k$ 通过选取 $\mathbf{I}(T_k)$ 中得分最高的 $m_{k-1} - m_k$ 个位置确定。消融实验证实，移除ITA（改用静态规则化激活模式）会导致复杂纹理区域出现artifact和锐度损失。

### Beta分布时间步调度

JiT采用Beta分布的逆CDF将均匀时间进度映射为非均匀时间步：

$$t_i = F^{-1}(s_i; \alpha, \beta)$$

其中 $\alpha=1.4, \beta=0.42$。该调度将更多计算步骤偏置于早期噪声阶段，此时全局结构的建立最为关键，与JiT“早期稀疏、后期密集”的空间分配策略形成互补。

### 嵌套Token子集链

整个多阶段调度建立在嵌套的token索引集层次结构上：

$$\Omega_K \subset \Omega_{K-1} \subset \cdots \subset \Omega_1 \subset \Omega_0 = \{1,2,\ldots,N\}$$

其中 $\Omega_k$ 是第 $k$ 阶段激活的锚点token索引集，满足 $|\Omega_k| = m_k$，且 $m_K < m_{K-1} < \cdots < m_0 = N$。对应的选择矩阵 $\mathbf{S}_k$ 和投影算子 $\mathbf{P}_k = \mathbf{S}_k\mathbf{S}_k^{\top}$ 分别用于提取锚点token和投影到激活子空间。

## 实验与关键发现

### 主实验结果

JiT在FLUX.1-dev上实现了**近乎无损的显著加速**。如表1所示，在约4倍加速设置下（18 NFE，706.17 TFLOPs），JiT的CLIP-IQA达到0.6166，**超越**了50 NFE全计算基线（0.6139），Image Reward也从1.004提升至1.017，表明空间近似不仅未损害质量，反而可能因噪声正则化带来微弱增益。在约7倍加速设置下（11 NFE，423.26 TFLOPs），JiT的CLIP-IQA为0.5397，GenEval为0.6457，相较同等NFE的朴素加速基线（7 NFE）分别**提升0.1263和0.0828**，说明单纯减少时间步会导致质量崩溃，而JiT的空间选择性计算有效维持了语义与结构完整性。

与现有加速方法的对比进一步验证了JiT的优越性。在~4×加速层级，JiT在所有自动指标（CLIP-IQA、Image Reward、HPSv2.1、GenEval、T2I-CompBench）上均取得最优或次优结果，且计算量（TFLOPs）显著低于缓存类方法如TeaCache。在~7×加速层级，JiT的优势更加突出——缓存方法因误差累积导致语义错误和细节丢失，而JiT凭借无上采样的空间近似和确定性微流（DMF）实现了artifact-free的状态转换。

人类偏好盲测（表2）进一步确认了这一优势：在~4×加速下，评估者对JiT的偏好率相较Bottleneck Sampling达85.6%，相较RALU达90.3%；在~7×加速下，相较FLUX.1-dev朴素加速基线高达93.1%，充分说明人眼对JiT生成质量的认可。

### 消融实验

消融实验揭示了JiT各组件的因果贡献（表3，图4）：

- **移除SAG-ODE的空间近似项**（即将未激活token的速度置零）导致**灾难性的质量崩溃**：HPSv2.1从26.90骤降至24.18，T2I-CompBench从0.3727跌至0.3414。未激活区域无法形成连贯结构，验证了外推速度场对于维持全场演化一致性的必要性。

- **移除ITA（重要性引导的token激活）**，改用静态、规则化的激活模式，HPSv2.1降至26.51，T2I-CompBench降至0.3670。复杂纹理区域出现明显的artifacts和锐度损失，说明内容感知的动态资源分配对于保护高频细节至关重要。

- **移除DMF目标构建**（直接使用插值值作为新token初始状态），HPSv2.1降至26.04，T2I-CompBench降至0.3602。噪声水平不匹配导致阶段转换处产生可见的结构断裂，验证了DMF将新token平滑驱动至统计正确目标状态的必要性。

### 调度策略分析

阶段数量与token稀疏度的选择对加速-质量平衡有显著影响（图6，图7）。3阶段调度在加速比与质量间取得最优折中：2阶段调度加速不足，4阶段调度因过晚切换到全分辨率而引入持久噪声。token分配方面，激进策略（20%→50%）损害语义完整性，保守策略（50%→75%）加速收益降低，JiT采用的平衡策略（35%→62%）提供了最佳权衡。

### 跨模型与跨模态泛化

JiT展现出良好的泛化能力。在Qwen-image模型上，~4×加速设置下仍能生成高质量图像（图8）；在HunyuanVideo-1.5视频生成骨干上，~4×和~7×加速设置下均能保持语义一致性和时序连贯性（图9），验证了空间近似策略在时空域的适用性。

### 失败模式与局限性

尽管JiT在多数场景下表现优异，仍需注意以下边界情况：
- 在极端稀疏设置下，若初始锚点token未能充分捕获全局结构信息，错误可能随阶段推进而累积，需谨慎选择初始稀疏度。
- 当前阶段调度和token稀疏度依赖人工设定的超参数（表4），尚未实现全自动优化。
- 方法主要在流动匹配框架下的DiT模型上验证，在其他架构上的效果有待进一步评估。

![[assets/figures/papers/paper_list_l2527_https_arxiv_org_abs_2603_10744/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison with other methods. The optimal result is represented in bold, and the sub-optimal result is represented in underlining. FLOPs are measured via torch.profiler and the Speed is calculated based on the FLOPs reduction relative to the base model FLUX.1-dev(50)*

![[assets/figures/papers/paper_list_l2527_https_arxiv_org_abs_2603_10744/figures/005_Table_2.jpg]]
*Table 2: Human preference rates for our JiT method in blind pairwise comparisons*

![[assets/figures/papers/paper_list_l2527_https_arxiv_org_abs_2603_10744/figures/006_Table_3.jpg]]
*Table 3: Ablation study of each component with JiT*

![[assets/figures/papers/paper_list_l2527_https_arxiv_org_abs_2603_10744/figures/007_Figure_4.jpg]]
*Figure 4: Visual ablation study of each component within JiT*

![[assets/figures/papers/paper_list_l2527_https_arxiv_org_abs_2603_10744/figures/010_Figure_6.jpg]]
*Figure 6: Visual ablation on the number of stages for a fixed total NFE of 18. (a) A 2-stage schedule offers limited acceleration. (b) Our default 3-stage schedule yields the best trade-off. (c) A 4-stage schedule introduces persistent noise due to a late transition to full resolution. This validates that a 3-stage approach offers a superior balance between speed and quality*

![[assets/figures/papers/paper_list_l2527_https_arxiv_org_abs_2603_10744/figures/001_Figure_1.jpg]]
*Figure 1: Visual showcases of our JiT framework applied to the FLUX.1-dev model. Our method produces high-fidelity and visually compelling images even at significant acceleration factors of 4× and 7×*

## 定位与知识库关联

### 核心洞察与问题定位

扩散Transformer（DiT）在生成过程中对所有空间token施加均匀计算，忽视了扩散模型由粗到细的生成特性——早期步骤主要建立全局低频结构，细节信息在后期才逐步涌现。这一空间冗余导致大量计算被浪费在非关键区域，构成了当前DiT推理效率的根本瓶颈。

JiT的核心洞察在于：**将空间计算资源按需分配**。早期仅对少量关键锚点token进行Transformer计算并外推全场速度，后期逐步激活细节区域，从而在不牺牲生成质量的前提下大幅降低总计算量。

### 与现有加速范式的本质差异

当前扩散模型加速方法主要沿三条技术路线展开，JiT与它们存在根本性的机制差异：

**时间域加速方法**（如高阶ODE求解器、蒸馏、缓存重用）通过减少时间步数或重用跨步特征来降低计算量，但每个时间步内仍对所有空间token进行完整计算。JiT在空间维度上做近似，与时间域方法**正交互补**——理论上可叠加使用以获得复合加速效果。

**缓存式加速方法**（如**TaylorSeer**和**TeaCache**）利用相邻时间步之间Transformer特征的时序冗余，通过缓存和选择性重用来跳过部分层的计算。这类方法受限于特征漂移问题，在高加速比下容易出现细节丢失和语义错误。JiT不依赖跨步特征重用，而是通过空间稀疏化从根本上减少每次前向传播的token数量，避免了累积误差。

**空间加速方法**（如**Bottleneck Sampling**和**RALU**）通过低分辨率编码或金字塔升采样策略减少空间维度。但这类方法需要显式的上/下采样算子和分布校正步骤，容易引入结构断裂和噪声不匹配。JiT的**免上采样设计**直接利用DiT内在的多尺度知识，通过增强提升算子（augmented lifter）在原始token空间中外推速度场，避免了显式分辨率变换带来的信息损失。

### 方法谱系中的定位

JiT属于**训练无关的空间稀疏加速**范式，其核心贡献在于首次将空间近似系统性地引入流动匹配框架下的DiT生成过程。与现有方法的本质区别体现在三个层面：

1. **计算图层面**：JiT动态改变Transformer的输入token数量（通过选择矩阵S_k实现），而非修改模型权重或重用中间特征。这使其与蒸馏、量化、剪枝等模型压缩方法完全正交。

2. **动力学层面**：SAG-ODE保证了锚点token的演化由Transformer精确给出（$\mathbf{S}_k^{\top}(\Pi_k\mathbf{u}_\theta) = \mathbf{u}_\theta$），外推近似仅影响未激活token。这一**一致性性质**是JiT在极高加速比下仍保持质量的关键，也是现有空间近似方法所不具备的理论保证。

3. **状态转换层面**：DMF通过构造合适的初始目标状态（融合结构先验与正确噪声水平）和有限时间ODE，在极短时间窗口内将新激活token平滑驱动至统计正确的状态。这避免了传统上采样方法中常见的分布偏移和artifacts问题。

### 适用边界与局限

尽管JiT在FLUX.1-dev上展示了显著的加速效果，其适用边界仍需谨慎界定：

**架构依赖性**：当前验证集中在流动匹配框架下的DiT模型（FLUX.1-dev、Qwen-image、HunyuanVideo-1.5）。在U-Net架构上的效果未经评估——U-Net的层级式特征处理可能天然具有类似的空间稀疏性，JiT的收益空间可能有限。

**超参数敏感性**：阶段调度（阶段数、token稀疏度、转换时间点）依赖人工设定（如Table 4中的配置），尚未实现自动化优化。消融实验表明，激进的稀疏分配（20%→50%）会损害语义完整性，保守分配（50%→75%）则降低加速收益，最优配置需要在加速比与质量之间仔细权衡。

**初始结构质量依赖**：在极端稀疏设置下，如果初始锚点token未能充分捕获全局信息，SAG-ODE的外推可能产生错误累积。Figure 6显示4阶段调度因过晚转换到全分辨率而引入持久噪声，验证了这一风险。

**条件生成场景的鲁棒性未充分验证**：当前评测主要基于通用T2I基准（GenEval、T2I-CompBench），在需要精确文本控制或复杂场景组合的任务中，空间近似是否始终可靠仍是一个开放问题。

### 开放问题与未来方向

1. **复合加速潜力**：JiT的空间加速策略与时间域方法（高阶求解器、蒸馏）在机制上正交，二者的结合能否实现乘性加速效果？这需要系统性的实验验证。

2. **自适应调度**：如何根据输入prompt的复杂度自动确定最优的阶段数、token稀疏度和转换时间点，以避免当前繁琐的手动调参？基于prompt特征或中间激活的元学习策略可能是一个有前景的方向。

3. **跨架构泛化**：JiT的核心思想——动态选择关键token进行精确计算并外推全场——是否可拓展到其他需要空间token处理的Transformer架构，如视频理解、多模态模型或自回归视觉生成？HunyuanVideo-1.5上的初步结果（Figure 9）显示了在时空域的泛化潜力，但更广泛的验证仍是必要的。

4. **理论分析深化**：SAG-ODE的近似误差界及其与最终生成质量的定量关系尚未建立。这一理论缺口使得超参数选择缺乏原则性指导，也限制了对方法失败模式的系统性理解。

## 原文 PDF

![[paperPDFs/CVPR_2026/Just_in_Time_Training_Free_Spatial_Acceleration_for_Diffusion_Transformers.pdf]]
