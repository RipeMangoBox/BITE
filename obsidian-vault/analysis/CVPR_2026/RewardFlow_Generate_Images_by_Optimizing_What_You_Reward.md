---
title: "RewardFlow: Generate Images by Optimizing What You Reward"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RewardFlow_Generate_Images_by_Optimizing_What_You_Reward.pdf
project_link: "https://plan-lab.github.io/rewardflow"
code_link: null
aliases:
- RewardFlow
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 因果调节变量是提示感知自适应策略（prompt-aware adaptive policy）动态调制的多奖励朗之万引导信号。该策略解析语义基元、推断编辑意图，并按照去噪时间步动态调整各项可微分奖励的权重和步长，从而精确控制生成轨迹。
primary_logic: 通过将多种可微分奖励（包括新颖的SAM2引导的目标一致性奖励和VQA语义奖励）融合到朗之万动力学中，并设计一个提示感知自适应控制器来协调这些信号，可以在纯推理、无需反转的情况下实现局部精确、语义一致且保持身份的编辑与生成。
claims:
- RewardFlow在PIE-Bench上实现了最先进的编辑保真度，Flux+RewardFlow将Distance从8.39降至7.78 (↓7.3%)，Whole Accuracy从28.21提升至29.44 (↑4.4%)。
- 在T2I-COMPBENCH上，RewardFlow为Flux和Qwen Image分别带来约12.5%和12.8%的整体组合生成精度提升。
- 消融实验表明，移除KL tether导致最严重的退化：PSNR降低2.11，SSIM降低1.89，验证了身份保持正则项的关键作用。
- 梯度可视化显示，融合全部奖励将梯度精确集中在目标语义区域，消除了语义泄漏。
---

# RewardFlow: Generate Images by Optimizing What You Reward

> [!tip] 核心洞察
> 通过将多种可微分奖励（包括新颖的SAM2引导的目标一致性奖励和VQA语义奖励）融合到朗之万动力学中，并设计一个提示感知自适应控制器来协调这些信号，可以在纯推理、无需反转的情况下实现局部精确、语义一致且保持身份的编辑与生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | RewardFlow：通过优化奖励引导图像生成 |
| 英文题名 | RewardFlow: Generate Images by Optimizing What You Reward |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.08536) · [Project](https://plan-lab.github.io/rewardflow) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RewardFlow |
| Dataset | PIE-Bench, T2I-COMPBENCH, GENEVAL |

> [!tip] 效果简介
> - PIE-Bench 上，Distance (↓ ×10³) 7.78 (Flux+RewardFlow) / 7.64 (Qwen+RewardFlow) vs 8.39 (EF, best prior Flux-based) (-7.3% / -8.9%)；Whole Acc. (↑) 29.44 (Flux+RewardFlow) / 29.78 (Qwen+RewardFlow) vs 28.21 (KV-Edit) (+1.23 / +1.57)。
> - T2I-COMPBENCH 上，Color Acc. (↑) 0.91 (Qwen+RewardFlow) vs 0.83 (Qwen Image) (+0.08)。
> - GENEVAL 上，Overall score (↑) 0.91 (Qwen+RewardFlow) vs 0.83 (Qwen Image) (+0.08)。

## 概要

现有的反转自由（inversion-free）图像编辑和生成方法虽然避免了耗时的潜变量反转，却普遍面临一个核心瓶颈：**缺乏细粒度的空间控制与身份保持**，导致内容漂移、语义泄漏以及弱对象定位。这类方法丢失了原始图像的忠实潜在表示，仅依赖粗糙或单一的奖励信号，无法协调多种异质目标。

**RewardFlow** 针对上述问题提出了一个纯推理阶段的解决方案。其核心因果机制是**提示感知自适应策略动态调制的多奖励朗之万引导信号**——该策略解析语义基元、推断编辑意图，并按照去噪时间步动态调整各项可微分奖励的权重和步长，从而精确控制生成轨迹。通过将多种可微分奖励（包括新颖的 SAM2 引导的目标一致性奖励和 VQA 语义奖励）融合到朗之万动力学中，RewardFlow 在无需反转的情况下实现了局部精确、语义一致且保持身份的编辑与生成。

在方法谱系上，RewardFlow 属于训练自由、奖励引导的扩散/流匹配模型推理优化框架。与依赖固定权重或无调度的现有奖励方法（如 **ReNO**）不同，RewardFlow 引入了分层多奖励集合与自适应调度策略；相较于 **EF**、**P2P**、**FlowEdit** 等训练自由编辑方法，RewardFlow 通过干净潜空间 KL tether 实现了更强的身份保持。

实验结果表明：
- 在 **PIE-Bench** 上，Flux+RewardFlow 将 Distance 从 8.39 降至 7.78（↓7.3%），Whole Accuracy 从 28.21 提升至 29.44（↑4.4%），达到最先进的编辑保真度。
- 在 **T2I-COMPBENCH** 上，RewardFlow 为 Flux 和 Qwen Image 分别带来约 12.5% 和 12.8% 的整体组合生成精度提升。
- 消融实验证实，移除 KL tether 导致最严重的退化（PSNR −2.11，SSIM −1.89），而融合全部奖励可将梯度精确集中在目标语义区域，消除语义泄漏。

方法的主要局限在于 VQA 模型在细粒度推理（如精确计数）上的不足会直接导致奖励信号失效，且 KL tether 在极端编辑指令下仍可能出现布局扭曲。



扩散模型与流匹配模型已在文本条件图像生成领域取得了显著进展，催生了 DALL·E 2 、DALL·E 3 等代表性系统。然而，在实际应用中，用户往往需要在已有图像基础上进行局部编辑，而非从零生成——例如替换特定物体的颜色、调整空间关系或添加新元素。这要求模型具备**精确的空间控制**与**可靠的身份保持**能力。

现有训练自由的图像编辑方法大致可分为两条技术路线。一类依赖**DDIM 反演**（如 DI 、P2P ），将输入图像映射回扩散模型的潜在空间，再以编辑后的条件引导反向去噪。这类方法的编辑质量高度受限于反演精度，反演误差会直接导致内容漂移和背景失真。另一类**反演自由**方法（如 EF 、FlowEdit 、FlowChef 、KV-Edit ）试图绕过反演步骤，直接在去噪过程中注入编辑信号。尽管简化了流程，但它们普遍缺乏对编辑区域的细粒度空间约束，容易产生**语义泄漏**——编辑效果溢出到无关区域，破坏背景结构。

更深层的问题在于，现有方法通常依赖**单一或粗糙的奖励信号**（如 CLIP 全局相似度），难以同时协调语义准确性、空间定位精度、目标一致性以及人类偏好等多个异质目标。当编辑指令涉及复杂属性绑定或多对象关系时，单一信号无法提供足够的监督粒度，导致弱对象定位、身份丢失和指令遵循失败。

RewardFlow 正是针对上述瓶颈提出的一种**反演自由、多奖励引导**的推理时优化框架。其核心思想是将多种可微分奖励——包括全局语义、感知相似度、区域掩码一致性、人类偏好以及基于视觉问答的细粒度语义奖励——融合为统一的朗之万动力学引导信号，并通过**提示感知自适应策略**动态协调各奖励的权重与步长，从而在纯推理阶段实现对生成轨迹的精确控制。这一设计使得 RewardFlow 能够在无需任何训练或反演的条件下，同时达成局部精确编辑、语义一致性与身份保持。



## 核心方法与创新机理

RewardFlow 的核心创新在于将**多奖励朗之万动力学**与**提示感知自适应策略**深度融合，构建了一个无需反转（inversion-free）、纯推理时优化的图像编辑与生成框架。与现有方法相比，RewardFlow 在三个关键维度上实现了突破性变革。

### 1. 从单一全局奖励到分层多奖励集合

现有基于奖励的方法（如 ReNO）通常仅依赖单一全局对齐信号，缺乏对局部语义和空间结构的细粒度控制，导致编辑过程中出现语义泄漏和弱对象定位。RewardFlow 从根本上改变了奖励信号的设计范式，构建了一个包含六个层次的可微分奖励集合：

- **全局语义奖励**：基于 SigLIP 编码器的图像-文本余弦相似度，确保整体语义对齐；
- **感知质量奖励**：评估生成图像的感知自然度；
- **区域奖励**：提供空间定位信号；
- **目标一致性奖励**：利用 SAM2 文本引导的可微分掩码，强制编辑区域与目标掩码一致并惩罚目标区域外的泄漏；
- **人类偏好奖励**：引入人类偏好模型的评分信号；
- **VQA 语义奖励**：通过视觉问答模型对生成图像进行细粒度语义验证，使用归一化交叉熵加间隔损失（公式 4）提供可微分的语义监督信号。

梯度可视化（Figure 2）提供了决定性证据：融合全部奖励后，图像空间梯度精确集中在目标语义区域，彻底消除了单一奖励常见的语义泄漏问题。

### 2. 从固定权重到提示感知自适应调度

传统方法对奖励信号采用固定权重或无调度策略，无法根据编辑意图和去噪阶段动态调整优化目标。RewardFlow 设计了**提示感知自适应策略**，这是实现精确控制的核心因果调节变量：

- **语义基元提取**：采样前一次性解析提示，提取原子编辑概念（如对象、属性、关系），据此推断编辑意图类型；
- **动态权重分配**：根据当前时间步和各奖励的满足状态，自适应调整每个奖励的权重系数 $w_i(t_k)$；
- **奖励感知步长控制**：采用逻辑斯蒂映射 $\eta_k = \eta_{\min} + (\eta_{\max} - \eta_{\min}) \cdot \sigma(-\gamma_\eta (R_{\text{tot}}^{(k)} - r_0))$，在高奖励时小步精调、低奖励时大步探索，实现效率与精度的平衡。

消融实验验证了这一创新的关键作用：移除动态加权后，PSNR 降低 1.32，SSIM 降低 0.84；移除语义基元后，Distance 从 7.64 升至 9.03，Whole Accuracy 下降 2.33（Table 3）。这表明固定权重无法适应奖励满足度的动态变化，而语义基元对于防止目标间干扰至关重要。

### 3. 从弱正则到干净潜空间 KL Tether

现有反转自由方法通常缺乏专门的身份保持机制，在编辑过程中容易发生内容漂移。RewardFlow 引入了**干净潜空间 KL tether** 作为身份保持正则项：

$$g_{\mathrm{KL},k} = -\lambda_{\mathrm{KL}} J_{\mathrm{Den}}(z^{(k)}, t_k, p)^\top (\tilde{z}^{(k)} - z_0)$$

该机制通过最小化当前预测干净潜变量 $\tilde{z}^{(k)}$ 与原始潜变量 $z_0$ 之间的 KL 散度，将生成轨迹锚定在输入图像的流形附近。消融实验表明，移除 KL tether 导致最严重的性能退化（PSNR -2.11，SSIM -1.89），并产生明显的结构漂移（Table 3），验证了身份保持正则项在框架中的核心地位。

### 创新点的协同效应

三个创新点并非孤立运作，而是通过统一的朗之万动力学框架产生协同效应：

$$z^{(k+1)} = z^{(k)} + \eta_k \bigl( f_k + g_{R_{\mathrm{tot}},k} + g_{\mathrm{KL},k} \bigr) + \xi_k$$

其中 $f_k$ 为骨干模型漂移，$g_{R_{\mathrm{tot}},k}$ 为自适应加权的多奖励梯度，$g_{\mathrm{KL},k}$ 为 KL tether 梯度。全组件启用时，RewardFlow 在 PIE-Bench 上达到最佳 Distance 7.64、PSNR 32.09、SSIM 90.21（Table 4），且梯度精确集中在目标物体轮廓（Figure 5），证明了多奖励引导、自适应调度与身份保持三者缺一不可的协同关系。



RewardFlow 是一种推理时、无需训练的生成与编辑框架，其核心思想是将扩散/流匹配模型的反向去噪过程重新解释为一系列测试时优化步骤，每一步都通过可微分奖励的梯度来引导潜变量的演化。整个流水线围绕四个关键模块构建，形成从语义理解到精确潜变量更新的闭环。

### 输入与预处理

给定输入图像 $I_0$（编辑任务）或纯噪声（生成任务）、文本提示 $p$ 以及可选的源掩码，框架首先对提示进行一次性语义解析。一个轻量级的提示感知自适应策略从 $p$ 中提取**语义基元 (Semantic Primitives, SPs)**——即编辑或生成指令中的原子概念，并推断编辑意图（如添加、替换、移除、属性修改等）。这一解析结果将驱动后续所有奖励的权重分配与步长调度。

### 核心循环：多奖励朗之万动力学

RewardFlow 的核心是一个离散化的反向朗之万动力学循环。在每个去噪时间步 $t_k$，流程执行以下操作：

1. **中间图像解码**：当前潜变量 $z^{(k)}$ 通过骨干模型的解码器映射为中间图像 $\tilde{I}^{(k)}$，使所有奖励可以在像素空间直接评估。

2. **多奖励评估与梯度计算**：框架在 $\tilde{I}^{(k)}$ 上计算一组分层可微分奖励，包括全局语义对齐奖励（SigLIP 余弦相似度）、感知质量奖励、SAM2 引导的目标一致性奖励、人类偏好奖励以及 VQA 细粒度语义奖励。每个奖励产生图像空间的梯度 $g_{I,i}^{(k)}$。

3. **梯度映射至潜空间**：通过解码器与去噪器的雅可比矩阵，将图像空间梯度映射为潜空间漂移项：
   $$g_{R_i,k} = \lambda_R J_{\mathrm{Den}}(z^{(k)}, t_k, p)^\top J_{\mathrm{Dec}}(\tilde{z}^{(k)})^\top g_{I,i}^{(k)}$$

4. **自适应融合与步长控制**：提示感知策略根据当前时间步、语义基元匹配状态以及各奖励的满足程度，动态计算每个奖励的时变权重 $w_i(t_k)$ 和自适应步长 $\eta_k$。步长通过逻辑斯蒂映射调节：
   $$\eta_k = \eta_{\mathrm{min}} + \left( \eta_{\mathrm{max}} - \eta_{\mathrm{min}} \right) \cdot \sigma \big( -\gamma_{\eta} \big( R_{\mathrm{tot}}^{(k)} - r_0 \big) \big)$$
   高奖励时以小步精调，低奖励时以大步探索。

5. **朗之万更新与身份保持**：将骨干模型漂移 $f_k$、加权融合的总奖励梯度 $g_{R_{\mathrm{tot}},k}$ 以及 KL tether 梯度 $g_{\mathrm{KL},k}$ 结合，执行朗之万更新：
   $$z^{(k+1)} = z^{(k)} + \eta_k \bigl( f_k + g_{R_{\mathrm{tot}},k} + g_{\mathrm{KL},k} \bigr) + \xi_k, \quad \xi_k \sim \mathcal{N}(0, 2\gamma_k \eta_k I)$$
   其中 KL tether 通过拉近当前预测的干净潜变量与原始潜变量之间的距离来防止身份漂移。

### 输出与关键特性

循环从高噪声时间步推进至低噪声时间步，最终输出编辑或生成后的图像。整个流程无需对源图像进行 DDIM 反演，也无需微调骨干模型权重，仅通过奖励信号在推理时塑造生成轨迹。梯度可视化（Figure 2）证实，融合全部奖励后梯度精确集中在目标语义区域，消除了单一奖励常见的语义泄漏问题。

### 补充图表

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/013_Figure_9.jpg]]
*Figure 9: Overview of the RewardFlow framework*



RewardFlow 在推理阶段将去噪过程转化为多奖励测试时优化，其核心由四个模块级联构成：**多奖励梯度映射**、**提示感知自适应策略**、**身份保持 KL tether** 以及**朗之万动力学更新**。以下逐一展开关键公式与机制。

### 多奖励梯度映射

在每一个去噪时间步 $t_k$，当前潜变量 $z^{(k)}$ 首先通过解码器得到中间图像 $\tilde{x}^{(k)} = \mathrm{Dec}(\tilde{z}^{(k)})$，其中 $\tilde{z}^{(k)}$ 是 $z^{(k)}$ 的干净预测。随后在该图像上计算一组可微分奖励 $R_i$ 的图像空间梯度 $\nabla_{\tilde{x}^{(k)}} R_i$。为了将该梯度转化为潜空间的漂移项，RewardFlow 通过解码器和去噪器的雅可比矩阵进行链式映射：

$$g_{R_i,k} = \lambda_R \, J_{\mathrm{Den}}(z^{(k)}, t_k, p)^{\top} \, J_{\mathrm{Dec}}(\tilde{z}^{(k)})^{\top} \, g_{I,i}^{(k)}$$

其中 $g_{I,i}^{(k)} = \nabla_{\tilde{x}^{(k)}} R_i$ 为图像空间梯度，$J_{\mathrm{Dec}}$ 和 $J_{\mathrm{Den}}$ 分别为解码器与去噪器在当前状态下的雅可比，$\lambda_R$ 为全局奖励缩放因子。该映射将多源奖励信号统一为潜空间的漂移项，是后续融合与更新的基础。

### 提示感知自适应策略

为协调多种异质奖励信号，RewardFlow 引入了一个轻量级提示感知自适应策略。该策略在采样前一次性解析提示 $p$，提取语义基元（Semantic Primitives, SPs），将编辑指令分解为原子概念。在去噪过程中，策略根据当前时间步和语义基元动态输出两项控制量：

1. **时变奖励权重** $w_i(t_k)$：根据各奖励的当前满足程度与语义基元匹配关系，自适应分配各奖励信号的权重。
2. **自适应步长** $\eta_k$：基于当前总奖励 $R_{\mathrm{tot}}^{(k)}$ 进行逻辑斯蒂映射：

$$\eta_k = \eta_{\mathrm{min}} + \left( \eta_{\mathrm{max}} - \eta_{\mathrm{min}} \right) \cdot \sigma\big( -\gamma_{\eta} ( R_{\mathrm{tot}}^{(k)} - r_0 ) \big)$$

其中 $\sigma$ 为 sigmoid 函数，$\gamma_{\eta}$ 控制灵敏度，$r_0$ 为参考阈值。当总奖励较低时，步长接近 $\eta_{\mathrm{max}}$，鼓励大步探索；当奖励趋于饱和时，步长收缩至 $\eta_{\mathrm{min}}$，实现精细调优。该机制使 RewardFlow 能根据优化进程自动调节探索与利用的平衡。

### 身份保持 KL tether

为防止奖励引导导致潜变量偏离原始图像的身份特征，RewardFlow 引入 KL tether 正则项。其核心是将当前干净预测 $\tilde{z}^{(k)}$ 与原始潜变量 $z_0$ 之间的 KL 散度最小化，梯度形式为：

$$g_{\mathrm{KL},k} = -\lambda_{\mathrm{KL}} \, J_{\mathrm{Den}}(z^{(k)}, t_k, p)^{\top} \, (\tilde{z}^{(k)} - z_0)$$

其中 $\lambda_{\mathrm{KL}}$ 控制正则强度。该梯度将当前预测拉回原始潜变量附近，有效抑制结构漂移和身份特征丢失。消融实验表明，移除 KL tether 会导致 PSNR 下降 2.11、SSIM 下降 1.89，是所有组件中退化最严重的（Table 3）。

### 朗之万动力学更新

融合以上所有信号后，RewardFlow 采用离散化朗之万动力学进行潜变量更新：

$$z^{(k+1)} = z^{(k)} + \eta_k \bigl( f_k + g_{R_{\mathrm{tot}},k} + g_{\mathrm{KL},k} \bigr) + \xi_k$$

$$t_{k+1} = t_k - \eta_k, \quad \xi_k \sim \mathcal{N}(0, 2\gamma_k \eta_k I)$$

其中 $f_k$ 为骨干模型（扩散或流匹配）的确定性漂移项，$g_{R_{\mathrm{tot}},k} = \sum_i w_i(t_k) \, g_{R_i,k}$ 为加权融合的多奖励梯度，$g_{\mathrm{KL},k}$ 为 KL tether 梯度，$\xi_k$ 为与步长适配的高斯噪声项。该更新对应于一个以提示倾斜密度为目标的朗之万 SDE 的有效离散化，在纯推理阶段无需任何训练或反演即可实现精确的奖励引导生成。

### VQA 语义奖励

在奖励集合中，VQA 奖励承担细粒度语义监督的角色。给定一个由提示自动生成的问答对 $\{q_t, a_t^\star\}_{t=1}^T$，VQA 奖励定义为负的长度归一化交叉熵加间隔损失：

$$R_{\mathrm{vqa}} = -\frac{1}{T}\sum_{t=1}^{T}\Big[ \log p_t[a_t^\star] + \lambda_m \max\big(0, m - \ell_t[a_t^\star] + \max_{u\neq a_t^\star}\ell_t[u]\big) \Big]$$

其中 $p_t[a_t^\star]$ 为 VQA 模型对正确答案的 softmax 概率，$\ell_t[\cdot]$ 为对应 logit，$m$ 为间隔超参数，$\lambda_m$ 控制间隔损失权重。该设计同时优化答案置信度和判别边界，使梯度信号能精确反映语义正确性。

### 补充图表

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/002_Figure_2.jpg]]
*Figure 2: Gradient localization of our differentiable rewards. We visualize the image-space gradient*

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/008_Figure_5.jpg]]
*Figure 5: Gradient localization across reward combinations. Including all rewards concentrates gradients to accurate object contours and eliminates leakage*



## 实验与关键发现

### 核心定量结果

RewardFlow 在两个主流基准上均取得最先进的编辑与生成精度。

在 **PIE-Bench** 图像编辑基准上，RewardFlow 在编辑保真度和空间定位上全面超越现有训练自由方法。Flux+RewardFlow 将 Distance 指标从 8.39 降至 7.78（↓7.3%），Whole Accuracy 从 28.21 提升至 29.44（↑4.4%）；Qwen Image+RewardFlow 进一步将 Distance 降至 7.64（↓8.9%），SSIM 达到 90.21 的最佳水平（Table 1）。PSNR 方面，RewardFlow 相较最佳 Flux 基线提升 5.3%（31.21 vs. 29.63），SSIM 提升 2.6%（89.67 vs. 87.44），而 LPIPS 仅比最佳方法高出 6.0%（40.55 vs. 38.27），表明在显著提升编辑精度的同时，感知质量保持竞争力。

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/003_Table_1.jpg]]
*Table 1: PIE-BENCH image editing results. RewardFlow consistently improves edit fidelity and spatial localization across all metrics while maintaining competitive runtime. Best results are in bold and strong baselines are underlined*

在 **T2I-COMPBENCH** 组合生成基准上，RewardFlow 为不同骨干模型带来一致且显著的增益：Flux 骨干的整体精度提升约 12.5%，Qwen Image 骨干提升约 12.8%。细粒度属性绑定（颜色、形状、纹理）、空间与非空间关系以及复杂组合等子项均有改善（Table 2）。例如，Qwen+RewardFlow 的颜色精度从 0.83 提升至 0.91（+0.08）。

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/006_Table_2.jpg]]
*Table 2: T2I compositional generation on T2I-COMPBENCH. Accuracy across fine-grained attribute binding (color, shape, texture), object relationships (spatial and non-spatial), and complex compositions. RewardFlow consistently improves all base models (PixArt-α, Flux, and Qwen Image). Best results are in bold*

在 **GENEVAL** 基准上，Qwen+RewardFlow 的整体得分从 0.83 提升至 0.91（+0.08），进一步验证了该方法在组合文本到图像生成任务上的泛化能力（Table 5）。

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/015_Table_5.jpg]]
*Table 5: T2I generation on GENEVAL*

### 消融实验

消融实验揭示了 RewardFlow 各组件的因果贡献，结果汇总于 Table 3 和 Table 4。

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/007_Table_3.jpg]]
*Table 3: Ablation on key RewardFlow components*

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/011_Table_4.jpg]]
*Table 4: Ablation on reward components. Each column indicates whether the corresponding reward is enabled (✓) or disabled (✗)*

**关键组件消融（Table 3）**：
- **移除 KL tether** 导致最严重的退化：PSNR 降低 2.11，SSIM 降低 1.89，图像出现明显的结构漂移和身份特征丢失，验证了身份保持正则项在防止轨迹偏离中的核心作用。
- **移除动态奖励加权** 后，PSNR 降低 1.32，SSIM 降低 0.84，表明固定权重无法根据奖励满足度的时变状态自适应调整，导致优化效率下降。
- **移除语义基元（SPs）** 后，Distance 从 7.64 升至 9.03，Whole Accuracy 下降 2.33，说明 SP 对防止不同编辑目标间的语义干扰至关重要。

**奖励组件消融（Table 4）**：
- 全奖励组合（所有可微分奖励启用）在 PIE-Bench 上达到最佳性能：Distance 7.64，PSNR 32.09，SSIM 90.21。
- 梯度可视化（Figure 5）进一步证实，融合全部奖励后，梯度精确集中在目标物体轮廓上，消除了单一奖励下常见的语义泄漏现象。
- 移除任一奖励组件均导致语义泄漏增加，目标区域外的梯度扩散加剧（Figure 6），验证了多奖励协同定位机制的必要性。

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/010_Figure_6.jpg]]
*Figure 6: Effect of removing reward components. (✗ RC, SAM, LLM, HPS, and PE) denote excluding*

### 失败模式与局限性

尽管 RewardFlow 在多数场景下表现优异，仍存在以下已知局限：

1. **VQA 模型的推理瓶颈**：VQA 奖励在细粒度推理任务（如精确计数）上的不足会直接导致奖励信号失效，使相应编辑目标无法正确实现。该问题在 Figure 15 的失败案例中有具体展示。
2. **奖励模型质量依赖**：RewardFlow 的性能受限于底层可微分奖励模型的质量，包括 SAM2 的掩码准确性、人类偏好模型的偏差等。VLM 消融实验（Table 6）表明，不同视觉语言模型对 VQA 奖励的有效性存在差异。
3. **极端编辑下的身份保持**：KL tether 虽然能有效抑制漂移，但在极端编辑指令下仍可能出现布局扭曲或身份特征丢失，需要进一步验证。
4. **推理开销**：额外的奖励梯度反向传播步骤引入一定计算开销，但得益于自适应步长调度，RewardFlow 所需采样步数比传统优化编辑器少约 60–80%，在精度与效率之间取得了有利平衡。

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/025_Figure_15.jpg]]
*Figure 15: RewardFlow counting failure case*

### 重要图表结论

- **Figure 2**：多奖励梯度定位可视化表明，RewardFlow 的奖励设计能防止语义泄漏，梯度精确集中于目标语义区域，这是空间精确编辑的基础。
- **Figure 3**：图像编辑定性对比显示，RewardFlow 在语义准确性和空间定位上一致优于基线方法，同时更好地保留背景结构、光照和身份特征。
- **Figure 11**：奖励随采样时间步的变化曲线显示各奖励稳定上升，验证了朗之万动力学引导的收敛性。
- **Figure 7**：方法组件消融的视觉结果进一步证实，所有组件（动态加权、语义基元、自适应步长、KL tether）共同作用才能达到最佳的一致性，缺少任一组件均导致明显的编辑质量下降。

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/009_Figure_7.jpg]]
*Figure 7: Ablations illustrating the effect of removing key components. RewardFlow (all components) achieves the best visual consistency and instruction alignment*

![[assets/figures/papers/paper_list_l2701_https_arxiv_org_abs_2604_08536/figures/014_Figure_11.jpg]]
*Figure 11: Reward progression over time*



## 定位与知识库关联

### 与现有训练自由编辑方法的关系

RewardFlow 定位于**训练自由、纯推理时引导**的图像编辑与生成方法谱系中。与依赖 DDIM 反转的主流编辑方法（如 **P2P**、**DI**、**InfEdit**、**TurboEdit**、**FlowEdit** 等）不同，RewardFlow 完全放弃了反转步骤，转而通过多奖励朗之万动力学直接在潜空间引导采样轨迹。这一设计使其天然规避了反转方法中常见的“可编辑性-重建质量”权衡，同时避免了因不精确反转导致的语义泄漏和内容漂移。

在奖励引导方法中，RewardFlow 与 **ReNO** 等基于单一全局对齐奖励的方法形成对比。ReNO 仅使用 CLIP 风格的全局相似度作为引导信号，缺乏空间定位能力；RewardFlow 则引入了分层多奖励集合，包括全局语义对齐、感知质量、区域掩码一致性、人类偏好以及 VQA 细粒度语义监督，并通过提示感知自适应策略协调这些异质信号。

### 核心差异化机制

RewardFlow 的关键差异化变量体现在三个层面：

1. **奖励信号类型**：从单一全局对齐扩展为分层多奖励集合。其中，基于 **SAM2** 的文本引导目标一致性奖励提供了可微分的空间定位信号，VQA 奖励则通过归一化交叉熵加间隔损失实现细粒度语义监督。梯度可视化（Figure 2, Figure 5）表明，全奖励组合将梯度精确集中在目标语义区域，消除了单奖励方法中常见的语义泄漏。

2. **奖励调度策略**：提示感知自适应策略（Section 3.2, Algorithm 1）解析语义基元、推断编辑意图，并根据去噪时间步和当前奖励满足度动态调整各奖励的权重与步长。消融实验证实，移除动态加权后 PSNR 降低 1.32、SSIM 降低 0.84，验证了固定权重无法适应奖励状态变化。

3. **身份保持机制**：KL tether（Section 3.4）通过最小化当前预测干净潜变量与原始潜变量之间的 KL 散度来防止轨迹漂移。消融实验表明，移除 KL tether 导致最严重的性能退化（PSNR -2.11, SSIM -1.89），验证了该正则项在身份保持中的关键作用。

### 适用边界与局限

**适用场景**：
- 局部精确编辑（如替换、添加、删除特定物体），要求空间定位准确且背景保持
- 组合文本到图像生成，需要精确绑定属性、空间关系和非空间关系
- 需要身份保持的编辑任务，如人物属性修改而不改变面部特征

**已知局限**：
1. **VQA 模型瓶颈**：VQA 奖励的性能受限于底层视觉语言模型的细粒度推理能力。在精确计数等任务上，VQA 模型的不足直接导致奖励信号失效，使相应编辑目标无法正确实现（Figure 15）。
2. **奖励模型依赖性**：整体性能受限于各项可微分奖励模型的质量，包括 SAM2 的掩码准确性、人类偏好模型的偏差等。若奖励信号本身存在系统性偏差，RewardFlow 将忠实地优化这些有偏目标。
3. **极端编辑的漂移风险**：KL tether 虽能抑制漂移，但在极端编辑指令（如大幅改变物体形状或布局）下仍可能出现布局扭曲或身份特征丢失。
4. **计算开销**：额外的推理时优化步骤（反向传播奖励梯度）引入一定计算开销，但步数少于传统优化编辑器（约 60-80% 更少的采样步数）。

### 开放问题

1. **自适应融合权重的优化**：当前自适应策略基于启发式设计，如何在时间步和语义基元之间取得最优平衡？是否存在可学习的调度策略或基于强化学习的权重预测器？
2. **无条件生成中的多样性保持**：KL tether 在编辑任务中有效抑制漂移，但在无条件文本生成任务中可能过度约束样本多样性。如何设计替代机制以在保持语义对齐的同时维持生成多样性？
3. **多模态扩展**：当前框架针对文本引导的图像编辑与生成设计，是否可推广至视频编辑（需处理时序一致性）或多模态条件（如音频、草图、深度图）编辑场景？朗之万动力学框架在理论上支持任意可微分奖励的融合，但实际部署需解决跨模态奖励的同步与权重协调问题。
4. **VQA 奖励的鲁棒性提升**：如何提高 VQA 奖励对组合性和计数的鲁棒性？可能的路径包括集成更强的视觉推理模型、设计专门的计数奖励模块，或通过多轮 VQA 验证增强信号可靠性。
5. **与基于优化的编辑器的融合**：RewardFlow 的奖励框架是否可与需要额外优化的编辑器（如基于文本嵌入优化的方法）协同工作，以结合两者的优势？



## 原文 PDF

![[paperPDFs/CVPR_2026/RewardFlow_Generate_Images_by_Optimizing_What_You_Reward.pdf]]
