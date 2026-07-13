---
title: "BLADE: Block-Sparse Attention Meets Step Distillation for Efficient Video Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BLADE_Block_Sparse_Attention_Meets_Step_Distillation_for_Efficient_Video_Generation.pdf
project_link: http://ziplab.co/BLADE-Homepage/
code_link: null
aliases:
- BBSAMSDEVG
- BLADE
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "BLADE jointly trains adaptive block-sparse attention inside trajectory distribution matching step distillation for video diffusion transformers."
primary_logic: "A sparse student generator denoises with ASA masks, a fake score model estimates the student distribution, and TDM aligns it with the teacher under sparse constraints."
claims:
- "ASA dynamically keeps salient KV blocks using block sampling, Gilbert reordering, and thresholded importance scores."
- "Sparse-aware distillation reduces both denoising step count and per-step attention cost."
- "The note reports up to 14.10x end-to-end speedup on Wan2.1-1.3B while preserving VBench quality."
---

# BLADE: Block-Sparse Attention Meets Step Distillation for Efficient Video Generation

> [!tip] 核心洞察
> 将动态稀疏注意力直接嵌入步长蒸馏的联合训练过程，而非作为后处理步骤，可以在数据无关的条件下同时实现步数压缩和每步计算量降低，且稀疏感知的蒸馏能让学生模型在稀疏约束下学习到更紧凑的生成轨迹。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BLADE：面向高效视频生成的块稀疏注意力与步长蒸馏联合框架 |
| 英文题名 | BLADE: Block-Sparse Attention Meets Step Distillation for Efficient Video Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=O9J20MsmRl) · [Project](http://ziplab.co/BLADE-Homepage/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | BLADE (Block-sparse Attention Meets step Distillation for Efficient video generation) |
| Dataset | VBench-2.0, Wan2.1-1.3B (H20), CogVideoX-5B |

> [!tip] 效果简介
> - VBench-2.0 上，Total Score 为 0.569，对比 0.534，变化 +0.035。
> - VBench-2.0 上，Total Score 为 0.570，对比 0.563，变化 +0.007。
> - Wan2.1-1.3B (H20) 上，End-to-End Speedup 为 14.10×，对比 1×，变化 +13.10×。

## 概要

BLADE（Block-sparse Attention Meets step Distillation for Efficient video generation）是一个完全数据无关（data-free）的联合训练框架，旨在解决扩散Transformer在视频生成中的推理效率瓶颈。该框架的核心创新在于将自适应块稀疏注意力（Adaptive Block-Sparse Attention, ASA）直接嵌入基于轨迹分布匹配（Trajectory Distribution Matching, TDM）的步长蒸馏过程中，从而同时实现推理步数压缩和每步计算量降低。

实验结果表明，BLADE在Wan2.1-1.3B上实现了14.10×的端到端推理加速，在CogVideoX-5B上实现了8.89×的加速。在VBench-2.0基准测试上，BLADE将CogVideoX-5B的得分从0.534提升至0.569，将Wan2.1-1.3B的得分从0.563提升至0.570。



扩散Transformer在视频生成中的推理瓶颈来自两方面：迭代去噪过程需要大量步数（如50步），以及长序列上的二次复杂度注意力计算。现有方法通常分别处理这两个问题——步长蒸馏（如TDM）压缩推理步数，稀疏注意力降低每步计算量——但二者独立优化时存在次优性：稀疏注意力作为后处理步骤无法感知蒸馏目标，而蒸馏过程也未考虑稀疏约束下的生成轨迹特性。

BLADE的核心洞察在于：将动态稀疏注意力直接嵌入步长蒸馏的联合训练过程，而非作为后处理步骤，可以在数据无关的条件下同时实现步数压缩和每步计算量降低，且稀疏感知的蒸馏能让学生模型在稀疏约束下学习到更紧凑的生成轨迹。



## 核心方法与创新机理

BLADE的核心创新包含两个紧密耦合的组件：

1. **自适应块稀疏注意力（ASA）**：一种动态、内容感知、硬件友好的注意力机制，能够即时生成稀疏掩码，将计算聚焦于显著特征。ASA包含两个变体：训练无关的ASA和基于蒸馏的ASA_G（使用全局Token预测实现端到端训练）。

2. **稀疏感知的步长蒸馏**：基于TDM范式，将稀疏性直接纳入蒸馏损失计算，使学生生成器在稀疏注意力约束下学习与教师模型轨迹分布对齐。

核心调控旋钮是注意力阈值τ（attention threshold），它直接控制保留的KV块比例，从而在计算量与生成质量之间进行权衡。



![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_O9J20MsmRl_BLADE_Block-S/figures/001_Figure_1.jpg]]
*Figure 1: The training mechanism of BLADE within a single distillation interval [ $t _ { i - 1 } , t _ { i }$ ) . The Sparse Generator $\left( G _ { \theta } \right$) denoises the input $\mathbf { x } _ { t _ { 1 } }$ i to produce the sample $\mathbf { x } _ { t _ { i - 1 } }$ . Crucially, this output is then re-corrupted with Gaussian noise to create an intermediate sample $\mathbf { x } _ { t _ { i } }$ . A dedicated Fake Score model evaluates this re-noised sample. Its output is contrasted with the score from the Real Score model (which is the pre-trained teacher model) to compute the Distribution Matching Loss ( $\nabla _ { \boldsymbol { \theta } } D _ { K L }$ ) . This loss directly updates the st...

BLADE采用学生-教师范式，整体架构包含以下模块：

- **教师模型 f_φ**：预训练的高质量多步扩散模型，提供真实数据分数 s_φ。
- **学生生成器 G_θ**：与教师共享DiT架构，但将标准自注意力替换为ASA，通过K步去噪生成样本。
- **假分数模型 f_ψ**：同时训练的神经网络，用于近似学生模型的不可解分数函数 s_ψ。
- **ASA掩码生成器**：包含Gilbert曲线重排、块采样、低分辨率注意力计算和阈值二值化，动态生成稀疏掩码。

训练过程遵循TDM范式：在每个蒸馏区间内，学生生成器对输入进行去噪，输出被重新加噪后由假分数模型评估，其输出与真实分数模型（教师）的分数对比，计算分布匹配损失直接更新学生生成器。



### 5.1 前向扩散与分数函数

前向扩散加噪过程定义为：

$$\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \epsilon$$

其中高斯噪声ε污染干净样本x0，得到时间步t的噪声样本xt，α_t和σ_t控制信噪比。

分数函数估计为：

$$s_\theta(\mathbf{x}_t, t) = \nabla_{\mathbf{x}_t} \log p_{\mathrm{real}, t}(\mathbf{x}_t) \approx -\frac{\mathbf{x}_t - \alpha_t \pmb{\mu}_\theta(\mathbf{x}_t, t)}{\sigma_t^2}$$

### 5.2 轨迹分布匹配（TDM）

假分数模型通过以下损失训练：

$$\mathcal{L}(\psi) = \sum_{i=0}^{K-1} \mathbb{E}_{\mathbf{x}_{t_i} \sim p_{\theta,t_i}} \mathbb{E}_{\mathbf{x}_j \sim q(\mathbf{x}_j \mid \mathbf{x}_{t_i})} \| f_\psi(\mathbf{x}_j, j) - \mathbf{x}_{t_i} \|_2^2$$

学生生成器的KL散度损失为：

$$\mathcal{L}(\theta) = \sum_{i=0}^{K-1} \lambda_i D_{\mathrm{KL}}(p_{\theta,t_i}(\mathbf{x}) \Vert p_{\phi,t_i}(\mathbf{x}))$$

其梯度近似为：

$$\nabla_\theta \mathcal{L}(\theta) \approx \sum_{i=0}^{K-1} \sum_{j=t_i}^{t_{i+1}} \lambda_j [ s_\psi(\mathbf{x}_j, j) - s_\phi(\mathbf{x}_j, j) ] \frac{\partial \mathbf{x}_{t_i}}{\partial \theta}$$

### 5.3 ASA掩码生成

ASA掩码生成包含以下关键步骤：

1. **Gilbert曲线重排**：在分块前对Token进行重排以保持空间局部性。
2. **块采样**：从每个块中采样k个代表性Token（k < b），计算低代价注意力图。
3. **块重要性归一化**：

$$\tilde{P}_{\mathrm{imp}}(i,j) \gets \frac{P_{\mathrm{imp}}(\iota, \jmath)}{\sum_k P_{\mathrm{imp}}(i,k)}$$

4. **阈值选择**：找到最小的m，使得排序后的归一化分数累积和达到阈值τ：

$$\sum_{j=1}^m s_j \ge \tau$$

5. **全局Token增强**：在训练时，将K与均值池化版本拼接，池化区域接收固定加性掩码ln n，在不破坏稀疏性的前提下软性引导注意力。



## 实验与关键发现

### 6.1 主实验结果

**Table 1: Video Quality Evaluation on VBench-2.0.**

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_O9J20MsmRl_BLADE_Block-S/figures/003_Table_1.jpg]]
*Table 1: Video Quality Evaluation on VBench-2.0. Note: Baseline refers to the official 50 steps baseline. All methods except the Baseline are distilled to 8 steps using TDM.*

| 方法 | 模型 | Total | Creativity | Commonsense | Controllability | Human | Physics | Speedup |
|------|------|-------|------------|-------------|-----------------|-------|---------|---------|
| Baseline-50 | CogVideoX-5B | 0.534 | 0.510 | 0.488 | 0.340 | 0.792 | 0.574 | 1× |
| FA2-8 | CogVideoX-5B | 0.539 | 0.514 | 0.492 | 0.342 | 0.794 | 0.578 | 7.93× |
| STA-8 | CogVideoX-5B | 0.528 | 0.502 | 0.480 | 0.330 | 0.788 | 0.570 | 8.12× |
| ASA_G-8 | CogVideoX-5B | **0.569** | **0.546** | **0.514** | **0.367** | **0.802** | **0.618** | 8.89× |
| Baseline-50 | Wan2.1-1.3B | 0.563 | 0.468 | 0.526 | 0.308 | 0.912 | 0.610 | 1× |
| FA2-8 | Wan2.1-1.3B | 0.580 | 0.480 | 0.540 | 0.316 | 0.920 | 0.622 | 9.37× |
| STA-8 | Wan2.1-1.3B | 0.528 | 0.440 | 0.496 | 0.290 | 0.896 | 0.576 | 10.53× |
| ASA_G-8 | Wan2.1-1.3B | **0.570** | **0.472** | **0.532** | **0.312** | **0.918** | **0.617** | **14.10×** |

**Table 2: Efficiency analysis on Wan2.1-1.3B (test on an H20).**

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_O9J20MsmRl_BLADE_Block-S/figures/004_Table_2.jpg]]
*Table 2: Efficiency analysis on Wan2.1-1.3B (test on an H20). Note: The number suffix (e.g. FA2-50) indicates the number of inference steps used in each model.*

| 方法 | Kernel Time (ms) | Kernel Speedup | E2E Time (s) | E2E Speedup |
|------|-----------------|----------------|--------------|-------------|
| FA2-50 | 73.25 | 1× | 338.40 | 1× |
| FA2-8 | 73.25 | 1× | 36.11 | 9.37× |
| ASA-8 | **22.21** | **3.30×** | **24.00** | **14.10×** |

ASA在Wan2.1-1.3B上以0.8稀疏率实现3.30×注意力核加速（22.21 ms vs 73.25 ms），端到端加速1.504×（相对于FA2-8基线）。

### 6.2 训练无关稀疏注意力对比

**Table 3: Comparison of training-free sparse attention methods on Wan2.1-1.3B (8-step distilled model).**

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_O9J20MsmRl_BLADE_Block-S/figures/005_Table_3.jpg]]
*Table 3: Comparison of training-free sparse attention methods on Wan2.1-1.3B (8-step distilled model).*

| 方法 | Sparsity | PSNR | SSIM |
|------|----------|------|------|
| STA | 0.75 | 16.72 | 0.6190 |
| SVG | 0.75 | 16.68 | 0.6390 |
| ASA | 0.75 | **19.55** | **0.7433** |
| RaA | 0.50 | 22.07 | 0.8191 |
| ASA | 0.50 | **22.20** | **0.8290** |

在训练无关的稀疏注意力对比中，ASA在0.75稀疏率下PSNR 19.55、SSIM 0.7433，显著优于STA（16.72, 0.6190）和SVG（16.68, 0.6390）。

### 6.3 消融实验

**Table 4: Ablation results for the token rearrangement strategy (VBench-1.0 quality score).**

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_O9J20MsmRl_BLADE_Block-S/figures/007_Table_4.jpg]]
*Table 4: Ablation results for the token rearrangement strategy, evaluated with the VBench-1.0 quality score.*

| 策略 | 质量分数 |
|------|---------|
| 无重排 | 0.779 |
| Gilbert曲线重排 | **0.788** |

Gilbert曲线重排策略在CogVideoX-5B上将VBench-1.0质量分数从0.779提升至0.788。

**Table 5: Effect of Global Token (G) and Additive Mask (AM) in ASA on CogVideoX-5B (VBench-2.0).**

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_O9J20MsmRl_BLADE_Block-S/figures/008_Table_5.jpg]]
*Table 5: Effect of Global Token (G) and Additive Mask (AM) in ASA on CogVideoX-5B (VBench-2.0). Note: G = Global Token, AM = Additive Mask. Baseline-50 is the original 50-step FA2 model.*

| 配置 | Total |
|------|-------|
| Baseline-50 | 0.534 |
| ASA（无G, 无AM） | 0.539 |
| ASA_G（有G, 无AM） | 0.559 |
| ASA_G（有G, 有AM） | **0.569** |

全局Token（G）和加性掩码（AM）是ASA的必要组件；ASA_G的VBench-2.0得分为0.569，而移除两者后降至0.539。

**Table 6: Ablation study on block size configuration for ASA on Wan2.1-1.3B (sparsity ratio 0.8).**

| 块大小 | PSNR | SSIM | LPIPS |
|--------|------|------|-------|
| 128×128 | 21.75 | 0.793 | 0.169 |
| 64×64 | **22.24** | **0.818** | **0.144** |

块大小64×64在Wan2.1-1.3B上以0.8稀疏率比128×128的PSNR高0.49、SSIM高0.025。

**Table 7: Ablation study on the attention threshold (τ) in ASA.**

| τ | Sparsity | PSNR | SSIM | LPIPS |
|---|----------|------|------|-------|
| 0.5 | 0.92 | 15.48 | 0.583 | 0.436 |
| 0.6 | 0.88 | 18.12 | 0.702 | 0.278 |
| 0.8 | 0.80 | 22.08 | 0.812 | 0.153 |
| 0.9 | 0.73 | 23.93 | 0.856 | 0.106 |

注意力阈值τ=0.8为最优操作点，实现稀疏率0.80且SSIM > 0.8；τ=0.9获得近稠密质量（PSNR 23.93）但稀疏率仅0.73；τ=0.5导致结构崩溃（PSNR 15.48）。

### 6.4 大规模模型验证

**Table 8: Comparison of training-free sparse attention methods on Wan2.1-14B.**

| 方法 | Sparsity | PSNR | SSIM | LPIPS |
|------|----------|------|------|-------|
| STA | 0.75 | 25.00 | 0.845 | 0.079 |
| SpargeAttention | 0.77 | 24.03 | - | 0.117 |
| ASA | **0.77** | **26.05** | **0.865** | **0.050** |

ASA在Wan2.1-14B上以0.77稀疏率实现PSNR 26.05、SSIM 0.865、LPIPS 0.050，优于STA和SpargeAttention。

### 6.5 极端加速场景

**Table 9: VBench-2.0 comparison of 4-step BLADE models against 50-step baselines.**

| 方法 | 模型 | Total | Speedup |
|------|------|-------|---------|
| Baseline-50 | CogVideoX-5B | 0.534 | 1× |
| BLADE-4 | CogVideoX-5B | **0.562** | **15.2×** |
| Baseline-50 | Wan2.1-1.3B | 0.563 | 1× |
| BLADE-4 | Wan2.1-1.3B | **0.570** | **17.6×** |

4步BLADE模型在CogVideoX-5B上实现15.2×加速，在Wan2.1-1.3B上实现17.6×加速，同时VBench总分仍优于50步基线。

### 6.6 人类偏好评估

**Table 10: Human preference: 8-step models vs. 50-step baseline.**

| 方法 | 模型 | Win | Tie | Lose |
|------|------|-----|-----|------|
| ASA_G | Wan2.1-1.3B | 25 (50%) | 15 (30%) | 10 (20%) |
| ASA_G | CogVideoX-5B | 22 (44%) | 16 (32%) | 12 (24%) |
| STA | Wan2.1-1.3B | 0 (0%) | 24 (48%) | 26 (52%) |

人类偏好评估中，ASA_G在Wan2.1-1.3B上以50%胜率、30%平局、20%负率优于50步基线；STA在人类评估中完全被基线压制（0胜、26负、24平）。

### 6.7 运行时分析

**Table 12: Runtime breakdown of Adaptive Sparse Attention (ASA) at two sequence lengths (sparsity 0.8).**

| 阶段 | 18k tokens (ms) | 100k tokens (ms) |
|------|-----------------|------------------|
| 总时间 | 8.07 | 116.99 |
| 块重要性估计 | 1.12 | 5.67 |
| 掩码构建 | 0.89 | 5.00 |
| 块稀疏注意力计算 | 6.06 | 106.32 |

在100k tokens下，ASA实现约3.8×加速（理论极限5×）；在18k tokens下，实现1.63×加速（约33%理论极限），表明短序列下开销占比更高。

### 6.8 公平性说明

- 所有方法（除基线外）均使用TDM蒸馏至8步，确保比较公平。
- 训练使用10,000个文本提示，来自JourneyDB并经Qwen2.5-3B-Instruct增强，不依赖原始视频数据。
- 实验在8×A800(80GB) GPU集群上进行。



## 定位与知识库关联

BLADE位于扩散模型加速与稀疏注意力两个研究方向的交叉点：

- **步长蒸馏**：继承自TDM（Luo et al., 2025）的数据无关蒸馏范式，区别于需要真实数据的渐进式蒸馏（Salimans & Ho, 2022）和一致性模型（Song et al., 2023）。
- **稀疏注意力**：ASA相比静态局部窗口方法（STA）、二值预定义掩码方法（SVG）和能量衰减方法（RaA）具有动态内容感知优势；相比SpargeAttention（Zhang et al., 2025a）在质量-稀疏率权衡上表现更优。
- **架构基础**：基于DiT（Peebles & Xie, 2023）架构，验证于CogVideoX-5B和Wan2.1-1.3B/14B等主流视频生成模型。

**局限性**：
- ASA的Triton实现相比CUDA优化仍有性能提升空间，当前在短序列（18k tokens）上仅实现1.63×加速，远低于理论5×极限。
- 块稀疏注意力核的实际效率受填充、负载不均衡和内存/系统开销影响，与FLOP理论加速存在差距。
- 当前方法主要验证于8步蒸馏场景，4步场景下的质量保持能力尚需进一步验证。
- 方法在分钟级超长视频（数十万token）上的表现尚未充分探索。

**开放问题**：
- ASA的CUDA实现能否缩小与理论加速极限之间的差距？
- 稀疏感知训练作为正则化手段，能否推广到3D内容生成和高分辨率图像合成？
- 在更极端的1-2步蒸馏场景下，BLADE框架是否仍能保持生成质量？
- ASA的动态掩码生成开销在更长序列（如100k tokens以上）中是否会被充分摊销？



## 原文 PDF

![[paperPDFs/ICLR_2026/BLADE_Block_Sparse_Attention_Meets_Step_Distillation_for_Efficient_Video_Generation.pdf]]
