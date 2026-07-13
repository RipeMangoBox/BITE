---
title: Test-Time Alignment of Text-to-Image Diffusion Models via Null-Text Embedding Optimisation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Test_Time_Alignment_of_Text_to_Image_Diffusion_Models_via_Null_Text_Embedding_Optimisation.pdf
project_link: null
code_link: "https://github.com/LAION-AI/aesthetic-predictor"
aliases:
- NTTTANT
- TTATIDMNTEO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 无条件（空文本）嵌入 φ（null-text embedding）在分类器自由引导（CFG）中作为生成分布的锚点，其优化可直接控制生成分布的方向。
primary_logic: 将测试时对齐的优化变量从非结构化的潜在/噪声空间转移到语义结构化的文本嵌入空间，通过对空文本嵌入进行正则化的奖励最大化，能够在语义流形内引导生成分布向目标奖励移动，同时保持去噪轨迹的局部一致性，从而防止奖励黑客并保持跨奖励的泛化能力。
claims:
- Null-TTA 通过优化空文本嵌入而非潜在变量进行对齐，确保优化位于语义一致流形上并防止奖励黑客。
- 空文本嵌入作为 CFG 的锚点，直接操纵模型的生成分布而非仅调整样本。
- 最终目标通过奖励项与基于 KL 散度的去噪轨迹一致性正则项和嵌入先验项联合优化。
- 在非可微奖励下，采用零阶梯度估计（式26）同样能有效优化空文本嵌入。
---

# Test-Time Alignment of Text-to-Image Diffusion Models via Null-Text Embedding Optimisation

> [!tip] 核心洞察
> 将测试时对齐的优化变量从非结构化的潜在/噪声空间转移到语义结构化的文本嵌入空间，通过对空文本嵌入进行正则化的奖励最大化，能够在语义流形内引导生成分布向目标奖励移动，同时保持去噪轨迹的局部一致性，从而防止奖励黑客并保持跨奖励的泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过空文本嵌入优化的文本到图像扩散模型测试时对齐 |
| 英文题名 | Test-Time Alignment of Text-to-Image Diffusion Models via Null-Text Embedding Optimisation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20889) · [Code](https://github.com/LAION-AI/aesthetic-predictor) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | Null-Text Test-Time Alignment (Null-TTA) |
| Dataset | PickScore 目标对齐（SD-v1.5, 100 步）, HPSv2 目标对齐（SD-v1.5, 100 步）, PickScore 目标对齐（SDXL, 100 步）, JPEG 压缩性目标（非可微）SD-v1.5 |

> [!tip] 效果简介
> - PickScore 目标对齐（SD-v1.5, 100 步） 上，PickScore↑ / HPSv2↑ / Aesthetic↑ / ImageReward↑ 0.315 / 0.294 / 5.431 / 0.946 (n_max=55) vs 0.218 / 0.279 / 5.236 / 0.338 (SD-v1.5 vanilla) (+0.097 / +0.015 / +0.195 / +0.608)。
> - HPSv2 目标对齐（SD-v1.5, 100 步） 上，HPSv2↑ 0.428 (n_max=115) vs 0.279 (SD-v1.5 vanilla) (+0.149)。
> - PickScore 目标对齐（SDXL, 100 步） 上，PickScore↑ / HPSv2↑ / Aesthetic↑ / ImageReward↑ 0.282 / 0.293 / 5.613 / 1.276 (n_max=45) vs 0.218 / 0.279 / 5.236 / 0.338 (SDXL vanilla) (+0.064 / +0.014 / +0.377 / +0.938)。

## 概要

文本到图像扩散模型在测试时对齐（Test-Time Alignment, TTA）中面临一个核心瓶颈：现有的对齐方法多在非结构化的潜在变量或噪声空间中优化，容易导致欠优化或过度优化（奖励黑客），难以在语义一致的方向上移动生成分布，从而无法有效平衡目标奖励与跨奖励泛化能力。

针对这一问题，本文提出 **Null-Text Test-Time Alignment (Null-TTA)**，其核心思想是将测试时对齐的优化变量从非结构化的潜在/噪声空间转移到语义结构化的文本嵌入空间。具体而言，Null-TTA 通过优化分类器自由引导（CFG）中的无条件（空文本）嵌入 $\phi$，直接操纵模型的生成分布，而非仅调整单个样本。由于文本嵌入空间具有结构化的语义特性，这一优化过程自然位于语义一致的流形上，从而有效防止奖励黑客，并保持去噪轨迹的局部一致性。

方法上，Null-TTA 构建了一个正则化的奖励最大化目标，联合优化目标奖励项、基于 KL 散度的去噪轨迹一致性正则项以及嵌入先验项，并辅以轻量级贪婪粒子滤波机制以进一步提升生成质量。对于非可微奖励函数，该方法支持零阶梯度估计，保持了方法的通用性。

实验结果表明，Null-TTA 在多个奖励目标（PickScore、HPSv2、Aesthetic）上均实现了最优的测试时对齐性能，同时在跨奖励泛化方面显著优于现有基线方法，持续将帕累托前沿向外推移。该方法在 SD-v1.5 和 SDXL 上均验证了有效性，并展现出对非可微目标（如 JPEG 压缩性）的适应能力。

文本到图像扩散模型（如 Stable Diffusion）已展现出强大的生成能力，但其输出与人类偏好之间仍存在显著偏差。测试时对齐（Test-Time Alignment, TTA）旨在无需重新训练的情况下，在推理阶段引导模型生成更符合特定奖励函数（如美学评分、图文匹配度）的图像，因而成为灵活且低成本的偏好注入手段。

现有 TTA 方法的核心瓶颈在于**优化空间的选择**。主流方案——无论是基于引导的方法如 **DNO**（Tang et al., ICML 2025）、**InitNO**、**DPS**（Chung et al., CVPR 2023）和 **MPGD**（He et al., 2024），还是基于采样的 **DAS**（Wu et al., NeurIPS 2023）或基于搜索的 **DSearch**——均在非结构化的潜在变量 $z_t$ 或注入噪声 $\varepsilon_t$ 空间中执行优化。这种选择带来了两个根本性问题：

1. **奖励黑客（Reward Hacking）**：非结构化空间允许模型通过利用与语义无关的噪声模式来提升奖励分数，而非真正改善图像内容。这导致目标奖励虚高，但生成质量实际下降。
2. **过优化与泛化崩溃**：在噪声空间中沿奖励梯度移动时，缺乏语义约束，极易偏离自然图像流形，使模型在未见过的跨奖励指标上表现急剧恶化——即优化一个奖励时，其他奖励指标崩塌。

上述问题在帕累托前沿视角下尤为清晰：现有方法在“目标奖励优化”与“跨奖励泛化”之间构成一条折衷曲线（见 Figure 1），任何方法都难以同时突破两者的上限。

本文的核心动机源于对**分类器自由引导（Classifier-Free Guidance, CFG）**机制的重新审视。CFG 通过外推无条件预测与条件预测来增强文本遵循度：

$$\tilde{\epsilon}_\theta(x_t, t, c, \phi) = \epsilon_\theta(x_t, t, \phi) + s \big( \epsilon_\theta(x_t, t, c) - \epsilon_\theta(x_t, t, \phi) \big)$$

其中无条件（空文本）嵌入 $\phi$ 充当生成分布的**锚点**——它定义了模型在没有条件信号时的基础行为，从而间接决定了 CFG 外推的方向和幅度。这一观察揭示了一个此前未被利用的因果调控旋钮：**优化 $\phi$ 可以直接操纵模型的生成分布本身，而非仅仅调整单次采样的样本**。

更重要的是，$\phi$ 位于文本编码器（CLIP）输出的语义结构化嵌入空间中，而非无结构的像素或噪声空间。这意味着对 $\phi$ 的优化天然受到语义流形的约束，有望在追求奖励最大化的同时，保持生成内容的语义连贯性和跨奖励泛化能力。

基于上述洞察，本文提出 **Null-Text Test-Time Alignment (Null-TTA)**，将测试时对齐的优化变量从非结构化的潜在/噪声空间转移到语义结构化的空文本嵌入空间，通过正则化的奖励最大化，在语义流形内引导生成分布向目标奖励移动，从根本上解决奖励黑客和泛化崩溃问题。

## 核心方法与创新机理

### 优化变量的范式转移：从非结构化噪声到语义嵌入

现有测试时对齐（TTA）方法的核心瓶颈在于优化空间的选择。以 **DNO**（Tang et al., ICML 2025）为代表的基于引导的方法直接在注入噪声 $ε_t$ 或潜在变量 $z_t$ 上执行优化，**DPS**（Chung et al., CVPR 2023）在每一步通过近似奖励后验引导采样，**MPGD**（He et al., 2024）则试图在数据流形内约束引导方向。然而，这些方法的共同缺陷在于：噪声空间和潜在空间缺乏语义结构，优化过程容易偏离有意义的生成方向，导致两种典型失败模式——**欠优化**（无法有效提升目标奖励）或**过度优化/奖励黑客**（通过利用非语义的噪声模式欺骗奖励函数，但丧失跨奖励泛化能力）。

Null-TTA 的**关键变量替换**是将优化对象从非结构化的潜在/噪声变量转移到**无条件（空文本）嵌入 $φ'$**。这一转移的因果机制根植于分类器自由引导（CFG）的数学结构：

$$\tilde{\epsilon}_\theta(x_t, t, c, \phi) = \epsilon_\theta(x_t, t, \phi) + s \big( \epsilon_\theta(x_t, t, c) - \epsilon_\theta(x_t, t, \phi) \big)$$

其中 $φ$ 是空文本嵌入，$c$ 是条件文本嵌入，$s$ 为引导强度。在 CFG 框架下，无条件预测 $ε_θ(x_t, t, φ)$ 充当生成分布的**锚点**——它定义了模型在没有条件信号时的“默认”生成行为。优化 $φ$ 等价于在语义空间内系统性地移动这个锚点，从而**直接操纵模型的生成分布本身**，而非仅仅调整单次采样的噪声实现。由于文本编码器输出的嵌入空间具有天然的语义连续性，优化轨迹被约束在语义一致的流形上，从根本上抑制了奖励黑客的发生。

### 正则化目标函数：去噪轨迹一致性约束

仅将优化变量迁移到嵌入空间仍不足以保证生成质量。Null-TTA 的第二个关键创新在于其**KL 散度闭式正则化**的目标函数设计。完整目标为：

$$\operatorname*{max}_{\phi'} \Big( \lambda_1 \mathbb{E}_{p(x_0|\phi')}[R(x_0)] - \lambda_2 \sum_{t=1}^{T} \frac{1-\alpha_t}{2\alpha_t(1-\bar{\alpha}_t)} \| \tilde{\epsilon}(x_t,\phi') - \tilde{\epsilon}(x_t,\phi) \|^2 - \frac{\lambda_2}{2\sigma_\phi^2} \| \phi' - \phi \|^2 \Big)$$

该目标包含三个组件：

1. **奖励项** $λ_1 \mathbb{E}[R(x_0)]$：驱动生成分布向高奖励区域移动。
2. **去噪轨迹一致性项**：以闭式 KL 散度形式约束优化后模型与原模型在每个去噪步的噪声预测偏差。其系数 $\frac{1-α_t}{2α_t(1-\bar{α}_t)}$ 随 $t$ 自适应缩放——在噪声较大的早期步骤给予更强约束，在接近干净的后期步骤放宽限制。
3. **嵌入先验项** $\frac{λ_2}{2σ_φ^2} \|φ' - φ\|^2$：防止嵌入偏离原始空文本嵌入过远，维持语义锚点的基本功能。

在实际执行中，该目标被分解为**逐步优化**形式（式25），在每个去噪步 $t$ 利用 Tweedie 公式估计干净图像 $\hat{x}_0$ 并计算奖励，同时约束当前步的噪声预测偏差。正则化权重 $λ_2$ 随去噪进程**退火衰减**（由退火系数 $γ$ 控制），优化步数从 $n_{\min}$ 递增至 $n_{\max}$，形成“后期精细对齐、前期保守约束”的策略。

### 轻量级粒子滤波：反向过程的奖励感知增强

作为对嵌入优化的补充，Null-TTA 在反向过程中引入了一个**贪婪粒子滤波机制**：在每一步从 DDPM 转移核采样 $K$ 个候选潜在变量 $x_{t-1}^{(k)}$，利用 Tweedie 公式估计对应的干净图像 $\hat{x}_0^{(k)}$ 并计算奖励，然后**确定性选择**奖励最高的候选进入下一时间步。这一机制不同于 **DAS**（Wu et al., NeurIPS 2023）使用的完整 SMC 采样或 **DSearch** 的 MCTS 搜索——它仅需极少额外计算（实验表明 $K=3$ 即可达到最佳平衡），且与嵌入优化共享相同的奖励信号，形成协同效应。

### 非可微奖励的零阶梯度扩展

当奖励函数不可微时（如 JPEG 压缩率），Null-TTA 采用零阶梯度估计：

$$\hat{\nabla}_\phi J(\phi) \approx \frac{1}{K\mu} \sum_{k=1}^{K} \big[ J(\phi + \mu \mathbf{v}_k) - J(\phi) \big] \mathbf{v}_k$$

通过在嵌入空间内施加高斯扰动并查询奖励函数来估计梯度方向。与在像素或潜在空间进行零阶搜索的方法不同，该估计仍然发生在**语义结构化的嵌入空间**内，因此搜索方向仍保持语义一致性。实验证据（Table 7）表明，在 JPEG 压缩性目标上，Null-TTA 将压缩率从 -81.5 kB 提升至 -33.7 kB，同时维持了可接受的跨奖励泛化能力（PickScore 仅从 0.218 降至 0.204）。

### 计算效率的结构性优势

由于优化变量仅限于空文本嵌入 $φ'$（维度通常为 768 或 1024），反向传播仅需通过 U-Net 的**交叉注意力层**而非整个网络。与 DNO 等需要对完整 U-Net 进行反向传播的方法相比，Null-TTA 在 GPU 内存占用和推理时间上均具有显著优势（Table 2），使其在实际部署中更具可行性。

---

**需要手动验证的点**：空文本嵌入优化的理论保证（如收敛到目标分布 $p_{\text{tar}}(x) \propto p_{\text{pre}}(x) \exp(r(x)/α)$ 的证明）在提供的分析材料中未充分展开，建议查阅原文 Section 3.3 的推导细节以确认其严格性。

Null-TTA 的核心思想是将测试时对齐（Test-Time Alignment, TTA）的优化变量从非结构化的潜在/噪声空间迁移到语义结构化的文本嵌入空间。整个 pipeline 围绕**分类器自由引导（CFG）中的无条件（空文本）嵌入 φ** 展开，将其作为操纵模型生成分布的“锚点”。框架由四个关键模块串联构成，形成“嵌入优化→去噪引导→粒子筛选→解码输出”的闭环。

### 输入输出流

- **输入**：文本提示 $y$、预训练扩散模型（含 U-Net $\epsilon_\theta$、CLIP 文本编码器 $f_{\text{CLIP}}$、VAE 解码器 $D$）、目标奖励函数 $R(\cdot)$。
- **输出**：对齐后的图像 $x_0$，在最大化目标奖励的同时保持跨奖励泛化能力。

### 模块关系与数据流

1. **文本编码器（CLIP）**  
   将提示文本 $y$ 和空文本 $\varnothing$ 分别编码为条件嵌入 $c = f_{\text{CLIP}}(y)$ 和无条件（空文本）嵌入 $\phi$。$\phi$ 是后续优化的唯一变量，其所在的语义结构化空间是防止奖励黑客的关键——优化被约束在文本编码器定义的语义流形内，而非无结构的像素或噪声空间。

2. **扩散模型 U-Net（$\epsilon_\theta$）与 CFG 噪声预测**  
   在每个去噪步 $t$，U-Net 接收当前潜在变量 $x_t$、时间步 $t$、条件嵌入 $c$ 和空文本嵌入 $\phi$，通过 CFG 综合无条件与条件预测：
   $$\tilde{\epsilon}_\theta(x_t, t, c, \phi) = \epsilon_\theta(x_t, t, \phi) + s \big( \epsilon_\theta(x_t, t, c) - \epsilon_\theta(x_t, t, \phi) \big)$$
   其中 $s$ 为引导强度。优化 $\phi$ 直接改变 CFG 的“基线”预测，从而整体平移生成分布，而非仅调整单一样本。

3. **空文本嵌入优化器**  
   这是框架的核心。在每个去噪步 $t$，优化器通过梯度上升最大化以下正则化目标（式25）：
   $$\max_{\phi'} \Big( \lambda_1 R(\hat{x}_0(x_t,\phi')) - \frac{\lambda_2(1-\alpha_t)}{2\alpha_t(1-\bar{\alpha}_t)} \|\tilde{\epsilon}(x_t,\phi') - \tilde{\epsilon}(x_t,\phi)\|^2 - \frac{\lambda_2}{2\sigma_\phi^2} \|\phi' - \phi\|^2 \Big)$$
   该目标包含三项：奖励项推动生成结果向高奖励方向移动；去噪轨迹一致性项（KL 散度的闭式近似）约束优化后的噪声预测不偏离原始模型太远，保持局部去噪轨迹的连贯性；嵌入先验项防止 $\phi'$ 过度偏离原始空文本嵌入。  
   - **可微奖励**：直接通过奖励函数反向传播梯度至 $\phi'$。  
   - **非可微奖励**：采用零阶梯度估计（式26），对 $\phi$ 施加高斯扰动 $\mu \mathbf{v}_k$ 并查询奖励函数来近似梯度，保持搜索仍在语义空间内进行。

4. **粒子滤波器（可选）**  
   为进一步提升对齐质量，引入轻量级贪婪粒子滤波。从 DDPM 转移核采样 $K$ 个候选 $x_{t-1}^{(k)}$，利用 Tweedie 公式估计对应的干净图像 $\hat{x}_0^{(k)}$ 并评分，选取奖励最高的候选作为下一时间步的潜在变量。该步骤以极小的计算开销（仅需通过交叉注意力层反向传播）增强了采样的稳定性。

5. **解码器（VAE decoder）**  
   将最终去噪后的潜在变量 $z_0$ 解码为输出图像 $x_0 = D(z_0)$。

### 优化调度

优化强度随去噪进程动态调整：正则化权重 $\lambda_2$ 随 $t \to 0$ 自适应退火（由退火系数 $\gamma$ 控制），每步优化迭代数从 $n_{\min}$ 递增至 $n_{\max}$。这种调度在早期去噪步保持较强的分布约束，后期则释放更多自由度以精细对齐目标奖励。

### 关键设计优势

- **语义流形约束**：优化发生在 CLIP 文本嵌入空间，天然阻止模型利用非语义噪声模式进行奖励黑客。
- **分布级操控**：通过 CFG 的锚点 $\phi$ 直接平移生成分布，而非逐样本调整，保证了跨奖励的泛化能力。
- **计算高效**：梯度仅需通过 U-Net 的交叉注意力层反向传播，无需遍历整个网络，GPU 内存占用和推理时间均优于主流基线方法（如 DNO，Tang et al., ICML 2025）。

![[assets/figures/papers/paper_list_l2345_https_arxiv_org_abs_2511_20889/figures/001_Figure_1.jpg]]
*Figure 1: Evaluation of reward-optimisation (x-axes) vs over-optimisation (generalisation to held-out rewards on y-axes). Top/Bottom rows correspond to aligning with Aesthetic and HPSv2 target rewards respectively. Each ★ point corresponds to a particular baseline method, which together define the state-of-the-art pareto front (dashed line). For Null-TTA, each ○ point indicates the optimisation intensity (maximum inner steps*

### 问题形式化

Null-TTA 将测试时对齐形式化为在预训练扩散模型约束下最大化奖励函数的优化问题。其目标分布定义为：

$$p_{\mathrm{tar}}(x) = \frac{1}{\mathcal{Z}} p_{\mathrm{pre}}(x) \exp\left(\frac{r(x)}{\alpha}\right)$$

其中 $p_{\mathrm{pre}}(x)$ 为预训练模型的数据分布，$r(x)$ 为奖励函数，$\alpha$ 为温度参数，$\mathcal{Z}$ 为归一化常数。该形式化表明对齐后的分布应在奖励高的区域赋予更大密度，同时保持与预训练分布的整体一致性。

### 核心模块一：空文本嵌入优化器

这是 Null-TTA 的核心创新模块。与现有方法在非结构化的潜在变量 $z_t$ 或注入噪声 $\varepsilon_t$ 空间进行优化不同，Null-TTA 将优化变量转移到文本编码器输出的无条件（空文本）嵌入 $\phi'$。

**设计动机**：空文本嵌入 $\phi$ 在分类器自由引导（CFG）中作为生成分布的锚点，其作用机制为：

$$\tilde{\epsilon}_\theta(x_t, t, c, \phi) = \epsilon_\theta(x_t, t, \phi) + s \big( \epsilon_\theta(x_t, t, c) - \epsilon_\theta(x_t, t, \phi) \big)$$

其中 $c$ 为条件文本嵌入，$s$ 为引导强度。由于 $\phi$ 直接参与噪声预测的线性外推，优化 $\phi$ 等价于操纵模型的生成分布本身，而非仅调整单次采样的结果。更重要的是，$\phi$ 位于 CLIP 文本编码器定义的语义结构化空间中，优化轨迹自然约束在语义一致流形上，从机制层面防止了奖励黑客（即利用非语义噪声模式欺骗奖励函数）。

**优化目标**：在每个去噪步 $t$，优化器执行以下单步目标：

$$\max_{\phi'} \Big( \lambda_1 R(\hat{x}_0(x_t,\phi')) - \frac{\lambda_2(1-\alpha_t)}{2\alpha_t(1-\bar{\alpha}_t)} \|\tilde{\epsilon}(x_t,\phi') - \tilde{\epsilon}(x_t,\phi)\|^2 - \frac{\lambda_2}{2\sigma_\phi^2} \|\phi' - \phi\|^2 \Big)$$

式中各项含义：
- **奖励项** $\lambda_1 R(\hat{x}_0(x_t,\phi'))$：利用 Tweedie 公式从当前噪声状态 $x_t$ 估计干净图像 $\hat{x}_0$，计算奖励函数值，引导嵌入向高奖励方向更新。
- **去噪轨迹一致性项** $\frac{\lambda_2(1-\alpha_t)}{2\alpha_t(1-\bar{\alpha}_t)} \|\tilde{\epsilon}(x_t,\phi') - \tilde{\epsilon}(x_t,\phi)\|^2$：约束优化后的嵌入产生的噪声预测与原始嵌入的预测之间的偏差。该项源自 KL 散度的闭式推导，保证去噪轨迹的局部一致性，防止优化导致生成分布过度漂移。
- **嵌入先验项** $\frac{\lambda_2}{2\sigma_\phi^2} \|\phi' - \phi\|^2$：惩罚优化后的嵌入偏离原始空文本嵌入，提供额外的正则化，确保优化不脱离预训练模型的先验知识范围。

**完整目标**：上述单步目标是对以下总体目标的逐步近似：

$$\max_{\phi'} \Big( \lambda_1 \mathbb{E}_{p(x_0|\phi')}[R(x_0)] - \lambda_2 \sum_{t=1}^{T} \frac{1-\alpha_t}{2\alpha_t(1-\bar{\alpha}_t)} \| \tilde{\epsilon}(x_t,\phi') - \tilde{\epsilon}(x_t,\phi) \|^2 - \frac{\lambda_2}{2\sigma_\phi^2} \| \phi' - \phi \|^2 \Big)$$

**自适应调度**：正则化权重 $\lambda_2$ 随去噪步 $t \to 0$ 自适应退火，优化步数从 $n_{\min}$ 递增至 $n_{\max}$。退火系数 $\gamma$ 控制优化强度增长和正则化衰减的速率（消融实验显示 $\gamma=0.008$ 在 HPSv2 提升与跨奖励保留之间取得最佳折衷，见 Table 4）。

### 核心模块二：零阶梯度估计（非可微奖励扩展）

当奖励函数不可微时，Null-TTA 采用零阶梯度估计，通过对嵌入施加高斯扰动并查询奖励函数来近似梯度：

$$\hat{\nabla}_\phi J(\phi) \approx \frac{1}{K\mu} \sum_{k=1}^{K} \big[ J(\phi + \mu \mathbf{v}_k) - J(\phi) \big] \mathbf{v}_k$$

其中 $\mathbf{v}_k \sim \mathcal{N}(0, \mathbf{I})$ 为随机扰动方向，$\mu$ 为扰动尺度，$K$ 为扰动采样数（实验中 $K=4$）。该估计器将搜索保持在文本嵌入的语义空间内，避免在像素或噪声空间进行低效的黑箱搜索。在 JPEG 压缩性目标（非可微）上的实验验证了该方法的有效性（Table 7）。

### 核心模块三：贪婪粒子滤波器

为进一步提升生成质量，Null-TTA 引入轻量级的贪婪粒子滤波机制。在从 $t$ 到 $t-1$ 的去噪过渡中：

1. 从 DDPM 转移核采样 $K$ 个候选 $x_{t-1}^{(k)}$（$k=1,\dots,K$）。
2. 利用 Tweedie 公式估计每个候选对应的干净图像：

   $$\hat{x}_0^{(k)} = \frac{1}{\sqrt{\bar{\alpha}_{t-1}}} \left( x_{t-1}^{(k)} - \sqrt{1-\bar{\alpha}_{t-1}} \tilde{\epsilon}(x_{t-1}^k, \phi') \right)$$

3. 计算每个候选的奖励值 $R(\hat{x}_0^{(k)})$，贪婪选择奖励最高的候选作为下一时间步的状态 $x_{t-1}$。

消融实验表明 $K=3$ 在 HPSv2 目标上实现最佳平衡（HPSv2 0.346），过大的 $K$ 反而导致不稳定（Table 3）。

### 计算效率优势

Null-TTA 的高效性源于其设计选择：仅更新空文本嵌入意味着反向传播只需通过 U-Net 的交叉注意力层，而非整个网络。在 HPSv2 目标下的计算开销对比（Table 2）显示，Null-TTA 在 GPU 内存占用和推理时间上均优于 **DNO**（Tang et al., ICML 2025）等基于噪声优化的方法，同时获得更高的目标奖励得分。

## 实验与关键发现

### 核心实验结果

Null-TTA 在多个目标奖励和跨奖励泛化指标上均展现出对现有测试时对齐（TTA）方法的显著优势。其核心机制——在语义结构化的文本嵌入空间而非非结构化的噪声或潜在空间中优化——从根本上改变了优化方向的语义一致性，从而在提升目标奖励的同时有效抑制了奖励黑客（reward hacking）现象。

**PickScore 目标对齐。** 在 Stable Diffusion v1.5（100 步推理）上以 PickScore 为目标奖励时，Null-TTA（n_max=55）取得了 0.315 的 PickScore，较 vanilla 模型的 0.218 提升了 0.097；同时，在三个未参与优化的跨奖励指标上均实现了正向提升：HPSv2 从 0.279 升至 0.294，Aesthetic 从 5.236 升至 5.431，ImageReward 从 0.338 大幅跃升至 0.946（Table 1）。这一跨奖励泛化能力是现有方法难以企及的——对比方法通常在提升目标奖励时伴随其他指标的退化。

**HPSv2 目标对齐。** 以 HPSv2 为目标时，Null-TTA（n_max=115）将 HPSv2 从 0.279 提升至 0.428（+0.149），且在计算开销对比中展现出效率优势：相比 **DNO**（Tang et al., ICML 2025）等基线方法，Null-TTA 使用更少的 GPU 内存和更短的推理时间，同时获得更强的目标奖励性能（Table 2）。这一效率优势源于优化仅需通过交叉注意力层反向传播，而非遍历整个 U-Net。

**SDXL 上的泛化验证。** 在更大规模的 SDXL 模型上，Null-TTA（n_max=45）同样在 PickScore 目标上取得了 0.282 的 PickScore，同时 HPSv2 达 0.293、Aesthetic 达 5.613、ImageReward 达 1.276，均显著优于 vanilla SDXL 的对应指标（Table 6），验证了该方法在不同规模模型上的鲁棒性。

**帕累托前沿的外推。** Figure 1 从全局视角揭示了 Null-TTA 的本质优势：在 Aesthetic 和 HPSv2 两个目标上，现有基线方法（以 ★ 标记）共同构成了一条帕累托前沿（虚线），而 Null-TTA 在不同优化强度下的结果（以 ○ 标记）一致地外推了该前沿。这意味着在任意给定的目标奖励提升幅度下，Null-TTA 均能保持更高的跨奖励泛化水平。这一现象的根本原因在于，空文本嵌入的优化天然约束了更新方向位于语义流形上，阻止了模型利用非语义的噪声模式来欺骗奖励函数。

**非可微目标的优化能力。** 在 JPEG 压缩性这一非可微目标上，Null-TTA 采用零阶梯度估计（式 26）仍能有效对齐：JPEG Reward 从 vanilla 的 -81.496 大幅提升至 -33.741（+47.755），同时视觉质量指标虽有下降（Aesthetic 从 5.236 降至 4.649），但仍保持在合理范围内（Table 7）。这表明 KL 正则化的去噪轨迹一致性约束在梯度信息缺失时依然有效，防止了生成分布的剧烈漂移。

### 消融实验

**粒子数 K 的影响。** Table 3 显示，在 HPSv2 目标上，粒子数 K=3 实现了最佳平衡（HPSv2 0.346），过大的 K 值反而导致性能不稳定。这表明轻量级的贪婪粒子滤波已能有效筛选高质量候选，过多的粒子引入了不必要的方差。

**退火系数 γ 的敏感性。** Table 4 表明，γ=0.008 在 HPSv2 提升与跨奖励保留之间取得了最佳折衷。γ 控制着去噪过程中优化强度的增长速率和正则化强度的衰减速率，过小的 γ 导致优化不足，过大的 γ 则可能引发过度优化。

**奖励/正则化比例的关键作用。** Table 5 揭示了目标函数中 λ₁（奖励权重）与 λ₂（正则化权重）比例对性能的深刻影响。默认配置使 HPSv2 达到 0.346 而 ImageReward 维持 0.741；当比例失衡时，要么目标奖励提升不足，要么跨奖励泛化显著退化。这印证了 KL 正则化项——即去噪轨迹一致性约束和嵌入先验约束——在防止分布漂移中的核心地位。

### 定性分析

Figure 2 展示了六类挑战性提示下的生成样本对比，涵盖计数（"Nine marbles arranged in a perfect square"）、组合性（"A cat riding on a dog's back while holding a tiny flag"）、空间推理、异常颜色、细粒度风格迁移和不可能场景。Null-TTA 在忠实满足提示约束的同时保持了全局连贯性，而其他方法在复杂语义场景下往往出现属性遗漏或结构崩坏。这一现象可归因于优化发生在文本编码器输出的语义结构空间中，而非对像素或潜在变量的无约束扰动。

![[assets/figures/papers/paper_list_l2345_https_arxiv_org_abs_2511_20889/figures/003_Figure_2.jpg]]
*Figure 2: Qualitative comparison on six challenging categories—counting (“Nine marbles arranged in a perfect square”), compositionality (“A cat riding on a dog’s back while holding a tiny*

Figure 3 展示了多目标优化（PickScore 与 HPSv2 的加权组合）的折衷曲线，Null-TTA 在不同权重 w 下均取得了更优的折衷路径，进一步验证了该方法在复杂奖励结构下的灵活性。

![[assets/figures/papers/paper_list_l2345_https_arxiv_org_abs_2511_20889/figures/005_Figure_3.jpg]]
*Figure 3: Multi-objective optimisation using*

### 失败模式与局限

尽管 Null-TTA 在主流文本条件扩散模型上表现优异，其适用性存在明确边界：该方法依赖分类器自由引导（CFG）中的空文本嵌入作为优化锚点，因此仅适用于使用文本条件且具有空文本嵌入的架构（如 Stable Diffusion），对非文本条件或未使用 CFG 的模型无效。此外，零阶梯度估计在极高维奖励函数下可能需要更多查询（实验中 K=4 扰动），更复杂的非可微目标可能需调整扰动策略。超参数（n_max、λ₂、γ）需针对不同奖励函数微调以获得最佳平衡，这在实际部署中增加了调参成本。

![[assets/figures/papers/paper_list_l2345_https_arxiv_org_abs_2511_20889/figures/004_Table_2.jpg]]
*Table 2: Computational comparison of Null-TTA and baseline TTA methods under the HPSv2 target. For each method, we report GPU memory usage, wall-clock time per generated image, and the resulting HPSv2 score. Null-TTA achieves stronger target-reward performance than baselines under similar inference budgets, while also exhibiting the lowest memory consumption*

![[assets/figures/papers/paper_list_l2345_https_arxiv_org_abs_2511_20889/figures/008_Table_4.jpg]]
*Table 4: Comparison of optimised scores for different values of annealing coefficient (γ)*

![[assets/figures/papers/paper_list_l2345_https_arxiv_org_abs_2511_20889/figures/010_Table_7.jpg]]
*Table 7: Quantitative comparison on the non-differentiable JPEG Compressibility target. We report the JPEG Reward (defined as negative file size in kB) as the target metric, alongside crossreward generalization metrics. Higher JPEG Reward indicates smaller file size. Null-TTA*

## 定位与知识库关联

### 测试时对齐的方法谱系

文本到图像扩散模型的测试时对齐（Test-Time Alignment, TTA）旨在不重新训练模型的前提下，使生成分布向特定奖励函数偏移。现有方法可根据优化空间和搜索策略划分为三个主要分支。

**基于引导的方法**直接在去噪过程中注入奖励信号。**DPS**（Chung et al., CVPR 2023）通过近似奖励后验在每一步引导采样，将奖励梯度作用于潜在变量 $x_t$。**MPGD**（He et al., 2024）进一步在数据流形内约束引导方向以保持生成连贯性。然而，这类方法在非结构化的潜在空间中操作，优化方向缺乏语义约束，容易导致奖励黑客（reward hacking）——模型利用非语义的噪声模式而非有意义的视觉特征来提升奖励分数。

**基于噪声优化的方法**将优化变量前置到初始噪声或注入噪声。**DNO**（Tang et al., ICML 2025）在注入噪声空间中进行优化以最大化奖励，**InitNO** 则调节初始噪声以保持语义一致性。这类方法的根本瓶颈在于：噪声空间本身不具备结构化语义，优化过程缺乏对“合理生成方向”的内禀约束，导致欠优化（未能充分提升目标奖励）与过度优化（丧失跨奖励泛化能力）之间的尖锐矛盾。

**基于搜索/采样的方法**将 TTA 视为离散搜索问题。**DAS**（Wu et al., NeurIPS 2023）利用序贯蒙特卡洛（SMC）从奖励对齐后验中采样，**DSearch** 则采用蒙特卡洛树搜索（MCTS）在噪声空间中探索。这些方法通过采样多样性缓解局部最优问题，但计算开销随搜索空间指数增长，且仍然在非结构化空间中操作。

### Null-TTA 的核心差异与定位

Null-TTA 的根本创新在于**优化空间的迁移**：将优化变量从非结构化的潜在/噪声空间转移到文本编码器输出的语义结构化嵌入空间。具体而言，Null-TTA 优化的是分类器自由引导（CFG）中的无条件（空文本）嵌入 $\phi'$，而非 $z_t$、$\epsilon_t$ 或 $x_t$。

这一选择具有深层方法论意义。在 CFG 公式 $\tilde{\epsilon}_\theta(x_t, t, c, \phi) = \epsilon_\theta(x_t, t, \phi) + s(\epsilon_\theta(x_t, t, c) - \epsilon_\theta(x_t, t, \phi))$ 中，空文本嵌入 $\phi$ 作为生成分布的锚点——它定义了模型的“无条件下”行为基线，条件嵌入 $c$ 则在此基础上施加语义偏移。优化 $\phi'$ 等价于直接操纵生成分布的锚点位置，而非仅仅调整单个样本。由于文本嵌入空间由 CLIP 编码器定义，具备天然的语义结构化特性，优化过程被隐式约束在语义连贯的流形上，从根本上抑制了奖励黑客。

在目标函数层面，Null-TTA 将 TTA 形式化为正则化的奖励最大化问题：

$$\operatorname*{max}_{\phi'} \Big( \lambda_1 \mathbb{E}_{p(x_0|\phi')}[R(x_0)] - \lambda_2 \sum_{t=1}^{T} \frac{1-\alpha_t}{2\alpha_t(1-\bar{\alpha}_t)} \| \tilde{\epsilon}(x_t,\phi') - \tilde{\epsilon}(x_t,\phi) \|^2 - \frac{\lambda_2}{2\sigma_\phi^2} \| \phi' - \phi \|^2 \Big)$$

其中第二项为去噪轨迹一致性的 KL 散度闭式解，显式惩罚优化后的去噪轨迹与预训练模型的偏离；第三项为嵌入先验正则，防止 $\phi'$ 过度远离原始空文本嵌入。这种双重正则化设计使得 Null-TTA 在追求目标奖励的同时，天然保持跨奖励泛化能力——这是现有引导类和噪声优化类方法所欠缺的结构性优势。

在推理效率方面，Null-TTA 仅需通过 U-Net 的交叉注意力层反向传播（而非整个网络），配合轻量级贪婪粒子滤波在每步从 $K$ 个候选中选择奖励最高的潜在变量，在 GPU 内存占用和推理时间上均优于 DNO 等主流基线（Table 2）。

### 适用边界与局限

Null-TTA 的适用性受以下条件约束：

1. **架构依赖性**：仅适用于使用文本条件且具备空文本嵌入的扩散模型（如 Stable Diffusion 系列）。对于非文本条件（如纯类别条件）或未采用 CFG 的架构，该方法无法直接迁移。这一约束源于方法对 CFG 中空文本嵌入锚点角色的本质依赖。

2. **零阶优化的查询效率**：当面对不可微奖励函数时，Null-TTA 采用零阶梯度估计 $\hat{\nabla}_\phi J(\phi) \approx \frac{1}{K\mu} \sum_{k=1}^{K} [J(\phi + \mu \mathbf{v}_k) - J(\phi)] \mathbf{v}_k$。实验中使用 $K=4$ 个扰动方向即可在 JPEG 压缩性目标上取得竞争性能（Table 7），但对于极高维或评估代价昂贵的奖励函数，查询效率可能成为瓶颈。

3. **超参数敏感性**：优化强度（$n_{\text{max}}$）、正则化权重 $\lambda_2$、退火系数 $\gamma$ 等超参数需针对不同奖励函数微调。消融实验表明，$\gamma=0.008$ 在 HPSv2 目标上取得最佳折衷（Table 4），$\lambda_1/\lambda_2$ 比例需均衡以同时保持目标奖励和跨奖励表现（Table 5）。这些参数的最优值可能因奖励函数的尺度和特性而异。

4. **粒子滤波的局部最优风险**：贪婪粒子滤波在每一步确定性地选择奖励最高的候选，可能在某些奖励景观下陷入局部最优。当前 $K=3$ 的设置（Table 3）在 HPSv2 目标上表现最佳，但更复杂的奖励函数可能需要更先进的采样策略。

### 开放问题

1. **范式迁移的可能性**：空文本嵌入作为“语义锚点”进行优化的思想，是否可推广至其他生成模型家族？例如，基于流的模型或一致性模型中是否存在类似的语义结构化锚点变量？这需要重新审视不同生成范式中“无条件基线”的表征形式。

2. **冲突奖励的自适应正则化**：当目标奖励之间存在严重冲突时（如同时追求极端风格化与严格语义守恒），固定的 $\lambda_2$ 正则化可能不足以平衡。是否需要根据奖励冲突程度自适应调整正则化强度，或在嵌入空间中引入结构化的约束方向？

3. **粒子滤波策略的进阶设计**：当前贪婪选择策略的局部最优风险提示，可引入更复杂的序贯决策机制——如基于价值的粒子重采样、熵正则化的探索策略，或学习一个轻量级的价值函数来指导候选选择。这些改进是否能进一步提升对齐质量同时控制计算开销，仍有待探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Test_Time_Alignment_of_Text_to_Image_Diffusion_Models_via_Null_Text_Embedding_Optimisation.pdf]]
