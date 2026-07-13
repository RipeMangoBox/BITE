---
title: "ID-Crafter: VLM-Grounded Online RL for Compositional Multi-Subject Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ID_Crafter_VLM_Grounded_Online_RL_for_Compositional_Multi_Subject_Video_Generation.pdf
project_link: "https://angericky.github.io/ID-Crafter"
code_link: null
aliases:
- IC
- ID-Crafter
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过三阶段层次化身份保持注意力（主体内、主体间、跨模态）分离特征交互，并引入预训练VLM提供精细语义理解，最后利用在线GRPO直接优化身份保真度与视频质量的复合奖励。
primary_logic: 三阶段注意力逐步解耦主体内细节、主体间交互与跨模态语义对齐；VLM将多模态输入转化为空间布局信号；在线GRPO通过群体优势估计稳定多目标优化，三者协同缓解身份与运动冲突。
claims:
- 在OpenS2V-Nexus基准上，ID-CRAFTER-1.3B (base+RL) 以Total Score 55.16%显著优于Phantom-1.3B的50.71% (Table 1)。
- 移除层次化注意力导致FaceSim从58.12%下降至51.34%（↓11.7%），验证层次注意力对身份保持的关键作用 (Table 2)。
- 在线RL使FaceSim相对提升13.7% (58.12% → 66.10%)，同时Aesthetics提升14.9% (Table 3)。
- 人类偏好研究中，ID-CRAFTER在身份一致性维度获得60%的偏好，显著优于竞争模型 (Figure S.13)。
---

# ID-Crafter: VLM-Grounded Online RL for Compositional Multi-Subject Video Generation

> [!tip] 核心洞察
> 三阶段注意力逐步解耦主体内细节、主体间交互与跨模态语义对齐；VLM将多模态输入转化为空间布局信号；在线GRPO通过群体优势估计稳定多目标优化，三者协同缓解身份与运动冲突。

| 字段 | 内容 |
|------|------|
| 中文题名 | ID-Crafter：面向组合式多主体视频生成的VLM引导在线强化学习 |
| 英文题名 | ID-Crafter: VLM-Grounded Online RL for Compositional Multi-Subject Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.00511) · [Project](https://angericky.github.io/ID-Crafter) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | ID-CRAFTER |
| Dataset | OpenS2V-Nexus |

> [!tip] 效果简介
> - OpenS2V-Nexus (180 subject-text pairs) 上，Total Score 55.16% (Ours-1.3B Base + RL) vs 50.71% (Phantom-1.3B) (+4.45%)。
> - OpenS2V-Nexus 上，FaceSim 66.10% (Ours-1.3B Base + RL) vs 48.55% (Phantom-1.3B) (+17.55%)；Total Score 57.05% (Ours-14B) vs 52.32% (Phantom-14B) (+4.73%)。

## 概要

多主体视频生成面临一个核心瓶颈：在同时保持多个独立身份的一致性与整体时序连贯性之间存在固有矛盾，导致不同主体间出现语义冲突和身份退化。现有方法——无论是基于注意力特征注入的**Phantom**、基于注意力编辑的**VACE**，还是商业系统如**Sora**（OpenAI, 2023）和**Kling**（2024）——通常将多主体特征与文本令牌拼接后注入标准交叉注意力，难以解耦主体内细节、主体间交互与跨模态语义对齐，使得身份漂移和“复制粘贴”伪影成为普遍问题。

ID-CRAFTER 针对这一瓶颈提出了三个因果性设计，形成协同效应：

1. **三阶段层次化身份保持注意力**：将特征交互分解为主体内 Self Attention、门控主体间 Cross Attention 和跨模态 Attention，逐步解耦身份细节、主体间关系与语义对齐。消融实验表明，移除该模块导致 FaceSim 从 58.12% 骤降至 51.34%（↓11.7%），Total Score 下降 7.8%（Table 2）。

2. **VLM 语义理解模块**：引入预训练视觉语言模型 **Qwen2.5-VL-7B-Instruct** 作为双编码器架构的一部分（与 T5 配合），将多模态输入转化为精细的空间布局和语义指导。用单一 T5 替换 VLM 编码器会使 Q-Align 从 0.351 降至 0.287（↓18.2%），严重损害文本-视频对齐（Table 2）。

3. **在线 GRPO 后训练**：首次将在线强化学习应用于多主体视频生成，通过群组相对策略优化（GRPO）直接优化由身份保真度（权重 0.6）和视频质量（权重 0.4）组成的复合奖励。相比 SFT 基线，在线 RL 使 FaceSim 相对提升 13.7%（58.12% → 66.10%），Aesthetics 提升 14.9%（42.50% → 48.85%）（Table 3）。

在 OpenS2V-Nexus 基准（180 个主体-文本对）上，ID-CRAFTER-1.3B（base+RL）以 Total Score 55.16% 显著优于 Phantom-1.3B 的 50.71%（+4.45%），FaceSim 领先幅度达 +17.55%（Table 1）。人类偏好研究中，ID-CRAFTER 在身份一致性维度获得 60% 的偏好，在运动自然度维度获得 65% 的偏好，全面超越竞争模型（Figure S.13）。

**方法定位**：ID-CRAFTER 基于 Rectified Flow 视频扩散 Transformer 骨干（Wan-Video, 2024），在注意力机制、文本编码器和后训练优化三个关键维度进行了系统性改进。其核心贡献在于证明了层次化解耦注意力 + VLM 语义引导 + 在线 RL 的组合能够有效缓解身份保持与运动流畅性之间的张力，为多主体视频生成建立了新的技术范式。



扩散模型驱动的内容生成已在图像和视频领域取得显著进展，然而**多主体视频生成**仍面临一个根本性瓶颈：在同时保持多个独立主体的身份一致性与整体时序连贯性之间，存在着固有的矛盾。现有方法在处理单主体场景时尚可维持身份保真度，但当场景涉及两个或以上交互主体时，不同主体间的语义特征容易发生冲突，导致身份退化、主体混淆或“复制-粘贴”式的生硬拼接效果。

这一瓶颈的深层原因在于，当前主流方法通常将所有主体参考图像与文本提示简单拼接后送入统一的交叉注意力层，缺乏对**主体内细节、主体间交互、跨模态语义对齐**的分层解耦。例如，开源方法 **Phantom** 基于注意力特征注入实现多主体生成，但在复杂交互场景下仍难以避免身份漂移；商业系统如 **Sora**（OpenAI, 2023）、**Kling**（快手, 2024）和 **Pika**（Pika Labs, 2024）虽能生成高质量视频，但其技术细节未公开，且在多主体身份保持上的可控性有限。

从因果机制来看，问题核心在于：生成过程必须在同一潜空间内同时满足“每个主体与参考图像高度相似”和“所有主体在动态场景中自然交互”这两个相互制约的目标。前者要求强身份约束，后者要求运动自由度——二者在标准注意力机制下天然存在张力。因此，亟需一种能够**解耦身份保持与运动生成**、并引入**精细语义指导**的新框架。

本文提出 **ID-CRAFTER**，通过三项关键设计协同应对上述挑战：（1）**三阶段层次化身份保持注意力**，逐步分离主体内特征聚合、主体间门控交互和跨模态语义对齐；（2）引入预训练视觉语言模型（VLM）**Qwen2.5-VL-7B-Instruct** 作为语义编码器，将多模态输入转化为空间布局与关系信号；（3）首次将**在线GRPO（群组相对策略优化）**应用于多主体视频生成，利用复合身份-质量奖励直接优化生成策略。三者协同，从注意力结构、语义理解和策略优化三个层面缓解身份与运动的冲突。



## 核心方法与创新机理

ID-CRAFTER 针对多主体视频生成中身份一致性与运动流畅性之间的固有矛盾，提出了三项系统级创新，构成“架构解耦—语义注入—策略优化”的协同管线。

### 1. 三阶段层次化身份保持注意力

现有方法（如 Phantom）采用标准交叉注意力，将所有主体和文本令牌拼接后统一处理，导致不同主体间的特征相互干扰，引发身份退化与语义冲突。ID-CRAFTER 将注意力机制重构为三个递进阶段：

- **Stage 1 — 主体内自注意力（Intra-Subject Self-Attention）**：各主体的视觉令牌独立执行自注意力，精细建模主体自身的细节特征，避免跨主体信息过早混合。
- **Stage 2 — 门控主体间交叉注意力（Gated Inter-Subject Cross-Attention）**：通过门控机制选择性融合不同主体间的交互信息，在保持身份独立性的前提下捕捉主体间空间关系。
- **Stage 3 — 跨模态注意力（Cross-Modal Attention）**：将前两阶段的主体特征与 VLM 语义令牌进行跨模态对齐，实现文本语义到视觉主体的精准映射。

这一层次化设计从机制层面解耦了“主体内保真”与“主体间交互”两个冲突目标。消融实验（Table 2）显示，移除该模块后 FaceSim 从 58.12% 骤降至 51.34%（↓11.7%），Total Score 下降 7.8%，验证了层次注意力对身份保持的关键作用。进一步分析（Table S.5）表明，Stage 3 对语义对齐最为关键——移除后 NexusScore 从 45.1% 跌至 38.7%。

### 2. VLM 语义理解模块

传统方法仅依赖单一 T5 文本编码器，缺乏对多主体间复杂语义关系（如空间布局、相对位置、交互动作）的细粒度理解。ID-CRAFTER 引入双编码器架构：保留 T5 编码基础文本特征的同时，增加预训练视觉语言模型 **Qwen2.5-VL-7B-Instruct** 作为语义编码器。VLM 同时接收文本提示与多张参考图像，经推理后输出结构化的语义令牌，为视频扩散 Transformer 提供空间布局信号与主体间关系约束。

消融实验（Table 2）证实，将 VLM 替换为单一 T5 编码器后，文本-视频对齐指标 Q-Align 从 0.351 降至 0.287（↓18.2%），严重损害语义一致性。这表明 VLM 的多模态推理能力是实现精准语义对齐的瓶颈突破点。

### 3. 在线 GRPO 后训练与复合奖励

现有方法通常止步于流匹配监督训练（SFT）或采用离线 DPO，难以直接优化身份保真度与视频质量这类感知层面的复合目标。ID-CRAFTER 首次将在线强化学习引入多主体视频生成，具体设计包括：

- **策略形式化**：将流匹配的确定性生成过程改造为随机策略——在每步流积分中注入噪声，使模型可采样多样化的生成轨迹。
- **GRPO 优化**：采用群组相对策略优化（Group Relative Policy Optimization），对同一条件采样一组输出，以组内均值作为基线估计优势函数，避免训练价值模型的额外开销，并稳定多目标优化过程。
- **复合奖励函数**：总奖励 $\mathcal{R}_{\mathrm{total}} = w_{\mathrm{fid}}\mathcal{R}_{\mathrm{fid}} + w_{\mathrm{qual}}\mathcal{R}_{\mathrm{qual}}$，其中保真度奖励（权重 0.6）衡量身份一致性，质量奖励（权重 0.4）结合美学分数与自然度分数，由 VLM 评估视频是否符合物理规律与常识。

Table 3 显示，在线 GRPO 相比 SFT 基线，FaceSim 从 58.12% 提升至 66.10%（↑13.7%），Aesthetics 从 42.50% 提升至 48.85%（↑14.9%），同时显著优于离线 DPO。值得注意的是，从复合奖励中移除自然度成分（$\mathcal{R}_{\mathrm{nat}}$）后，Q-Align 下降但 FaceSim 与 Aesthetics 微升，提示存在奖励黑客现象，验证了多维度奖励设计的必要性。

### 创新协同逻辑

三项创新并非孤立存在，而是形成因果闭环：层次化注意力在架构层面解耦主体特征，为 VLM 语义令牌提供清晰的注入接口；VLM 则将多模态输入转化为可被各注意力阶段消费的空间-语义信号；在线 GRPO 利用复合奖励直接优化端到端生成策略，使架构设计与语义注入的优势在感知层面充分释放。三者协同，从根本上缓解了多主体视频生成中身份保持与运动质量之间的长期冲突。



ID-CRAFTER 的整体 pipeline 围绕一个核心矛盾展开：**在同时保持多个主体的身份一致性与视频时序连贯性时，不同主体间的语义冲突和身份退化**。为解决这一问题，系统将生成过程分解为三个协同阶段：层次化身份保持注意力、VLM 语义编码、以及在线强化学习微调。Figure 2 给出了架构总览。

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/002_Figure_2.jpg]]
*Figure 2: ID-CRAFTER Overview. Our model incorporates a hierarchical identity-preserving attention mechanism and a VLM that performs reasoning on the multimodal input into a video DiT to enable multi-subject video generation. An online RL stage further refines the concept alignment*

### 输入与潜空间编码

系统的输入包括一段文本提示和多张主体参考图像。视频生成基于 Rectified Flow 范式：VAE Encoder 先将输入视频压缩到潜空间，Video Diffusion Transformer (DiT) 随后在潜空间中预测从数据到噪声的恒定速度场。其训练目标为：

$$\mathcal{L}_{\mathrm{RF}} = \mathbb{E}_{t, \mathbf{z}_0, \epsilon} \left[ w(t) \left| \left| \mathbf{v}_{\pmb{\theta}} ( \mathbf{z}_t, t, \mathbf{C}_{\mathrm{ctx}} ) - ( \epsilon - \mathbf{z}_0 ) \right| \right|_2^2 \right]$$

其中 $\mathbf{z}_t = (1 - t) \mathbf{z}_0 + t \mathbf{\epsilon}$ 定义了线性插值轨迹，$\mathbf{C}_{\mathrm{ctx}}$ 为条件上下文。

### 核心模块与信息流

ID-CRAFTER 在 DiT 骨干上引入了两个关键模块，形成“感知-生成-优化”闭环：

1.  **层次化身份保持注意力**：替代标准交叉注意力（将所有主体和文本令牌简单拼接），采用三阶段逐步解耦特征交互：
    - **Stage 1（主体内 Self Attention）**：独立建模每个主体的细节特征，防止身份信息在早期融合中被稀释。
    - **Stage 2（门控主体间 Cross Attention）**：通过门控机制控制不同主体间的特征交互，缓解语义冲突。
    - **Stage 3（跨模态 Attention）**：将视觉主体特征与 VLM 提供的语义令牌对齐，实现跨模态语义绑定。

2.  **VLM 语义编码器**：采用双编码器架构（T5 + Qwen2.5-VL-7B-Instruct），由预训练 VLM 对文本和参考图像进行联合推理，输出精细的空间布局信号和主体间关系描述。该模块替代了单一 T5 编码器，为 DiT 提供更丰富的语义条件。

### 后训练优化与数据支撑

在监督训练（SFT）完成后，系统进入**在线 GRPO 阶段**。此时生成过程被随机化（在流积分每一步注入噪声），模型针对复合奖励进行策略优化：

$$\mathcal{R}_{\mathrm{total}}(\mathbf{V}) = w_{\mathrm{fid}} \mathcal{R}_{\mathrm{fid}}(\mathbf{V}, \mathcal{Z}) + w_{\mathrm{qual}} \mathcal{R}_{\mathrm{qual}}(\mathbf{V})$$

其中保真度奖励（$w_{\mathrm{fid}}=0.6$）衡量身份保持，质量奖励（$w_{\mathrm{qual}}=0.4$）综合美学分数与物理合理性。GRPO 通过组内比较估计优势函数，稳定多目标优化。

训练数据方面，系统采用**策划数据集**替代原始视频-主体配对数据，通过合成跨主体组合与融合示例（Figure 3）增强模型对复杂多主体场景的泛化能力。整个 pipeline 最终输出身份一致、时序连贯且文本对齐的多主体视频。



### 3.1 视频扩散Transformer与Rectified Flow基础

ID-CRAFTER的视频生成骨干基于**Rectified Flow**框架，在潜空间中学习从数据到噪声的线性插值轨迹。给定数据样本 $\mathbf{z}_0$ 和噪声 $\epsilon$，轨迹定义为：

$$\mathbf{z}_t = (1 - t) \mathbf{z}_0 + t \mathbf{\epsilon}, \quad t \in [0,1]$$

核心目标是训练一个视频扩散Transformer $\mathbf{v}_{\pmb{\theta}}$ 预测该轨迹上的恒定速度场 $\epsilon - \mathbf{z}_0$，训练损失为：

$$\mathcal{L}_{\mathrm{RF}} = \mathbb{E}_{t, \mathbf{z}_0, \epsilon} \left[ w(t) \left| \left| \mathbf{v}_{\pmb{\theta}} ( \mathbf{z}_t, t, \mathbf{C}_{\mathrm{ctx}} ) - ( \epsilon - \mathbf{z}_0 ) \right| \right|_2^2 \right]$$

其中 $\mathbf{C}_{\mathrm{ctx}}$ 为条件上下文信息，$w(t)$ 为时间加权函数。该框架为后续多主体生成提供了稳定的扩散动力学基础。

### 3.2 层次化身份保持注意力机制

多主体视频生成的核心矛盾在于：不同主体的身份特征需要独立保持，同时又必须在同一时空场景中协调交互。ID-CRAFTER通过**三阶段层次化注意力**逐步解耦这一冲突：

- **Stage 1 — 主体内自注意力（Intra-Subject Self-Attention）**：对每个主体独立执行自注意力，捕获其专属的外观细节和身份特征，避免主体间特征相互污染。
- **Stage 2 — 门控主体间交叉注意力（Gated Inter-Subject Cross-Attention）**：通过可学习的门控机制控制主体间的信息流动，在保持身份独立性的前提下建模主体间空间关系和交互语义。
- **Stage 3 — 跨模态注意力（Cross-Modal Attention）**：将前两阶段聚合的主体特征与VLM编码的语义令牌进行跨模态融合，实现精细的文本-视频语义对齐。

该设计的关键因果机制在于：**逐阶段分离特征交互粒度**——先锁定个体身份（Stage 1），再协调群体关系（Stage 2），最后注入全局语义（Stage 3）。消融实验（Table 2）证实，移除整个层次化注意力模块导致FaceSim从58.12%骤降至51.34%（↓11.7%），而单独移除Stage 3则使NexusScore从45.1%跌至38.7%（Table S.5），验证了跨模态阶段对语义对齐的决定性作用。

### 3.3 VLM语义编码模块

为提供超越简单文本描述的精细语义指导，ID-CRAFTER引入**双编码器架构**：保留T5编码器处理基础文本，同时集成预训练的**Qwen2.5-VL-7B-Instruct**作为视觉语言模型（VLM）编码器。VLM接收文本提示和所有参考图像作为多模态输入，通过视觉推理生成结构化的语义令牌，这些令牌携带了主体属性、空间布局、交互关系等细粒度信息，经Stage 3的跨模态注意力注入扩散Transformer。

消融实验（Table 2）表明，用单一T5替换VLM编码器导致文本-视频对齐指标Q-Align从0.351降至0.287（↓18.2%），严重损害语义一致性。这验证了VLM提供的空间布局信号和主体关系理解是单纯文本编码器无法替代的。

### 3.4 在线GRPO后训练与复合奖励

为在身份保真度和视频自然度之间取得最优平衡，ID-CRAFTER首次将**在线群组相对策略优化（GRPO）**引入多主体视频生成。GRPO通过采样一组输出并计算组内相对优势来稳定策略更新，其目标函数为：

$$\mathcal{I}_{GRPO}(\theta) = \mathbb{E}_{ \{ \sigma_i \}_{i=1}^G \sim \pi_{\theta_{old}} } \frac{1}{G} \sum_{i=1}^G \frac{1}{|\sigma_i|} \sum_{t=1}^{|\sigma_i|} \min[ r_t^i(\theta) \hat{A}_{i,t}, \text{clip}(r_t^i(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_{i,t} ] - \beta D_{KL}(\pi_{\theta} || \pi_{ref})$$

其中 $G$ 为群组大小，$\hat{A}_{i,t}$ 为组内标准化后的优势估计，KL散度项约束策略不偏离参考模型过远。

**复合奖励函数**由保真度项和质量项加权构成：

$$\mathcal{R}_{\mathrm{total}}(\mathbf{V}) = w_{\mathrm{fid}} \mathcal{R}_{\mathrm{fid}}(\mathbf{V}, \mathcal{Z}) + w_{\mathrm{qual}} \mathcal{R}_{\mathrm{qual}}(\mathbf{V})$$

其中 $w_{\mathrm{fid}}=0.6$，$w_{\mathrm{qual}}=0.4$。保真度奖励 $\mathcal{R}_{\mathrm{fid}}$ 衡量生成视频 $\mathbf{V}$ 与参考主体集 $\mathcal{Z}$ 的身份一致性；质量奖励 $\mathcal{R}_{\mathrm{qual}}$ 进一步分解为：

$$\mathcal{R}_{\mathrm{qual}} := (1 - \beta) \mathcal{R}_{\mathrm{aes}} + \beta \mathcal{R}_{\mathrm{nat}}, \quad \beta=0.4$$

$\mathcal{R}_{\mathrm{aes}}$ 评估美学质量，$\mathcal{R}_{\mathrm{nat}}$ 通过VLM评判视频是否遵循物理规律和常识（NaturalScore），用于惩罚不自然的形变和运动伪影。

**关键发现**：在线GRPO相比监督微调（SFT）基线，FaceSim相对提升13.7%（58.12% → 66.10%），Aesthetics提升14.9%（42.50% → 48.85%）（Table 3）。然而，从复合奖励中移除自然度成分 $\mathcal{R}_{\mathrm{nat}}$ 后，Q-Align下降但FaceSim与Aesthetics微升，提示**奖励黑客现象**——模型可能通过牺牲物理合理性来优化可量化指标，验证了多维度奖励设计的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/003_Figure_3.jpg]]
*Figure 3: Data curation pipeline of ID-CRAFTER*



## 实验与关键发现

### 主实验：OpenS2V-Nexus 基准量化对比

ID-CRAFTER 在 OpenS2V-Nexus 基准（180 组主体-文本配对）上与现有方法进行了系统对比。如表 1 所示，ID-CRAFTER-1.3B（Base + RL）以 **Total Score 55.16%** 显著优于 Phantom-1.3B 的 50.71%（+4.45%），在身份保持指标 FaceSim 上的优势更为突出：**66.10% vs. 48.55%**（+17.55%）。放大到 14B 参数规模后，ID-CRAFTER-14B 以 **Total Score 57.05%** 继续领先 Phantom-14B 的 52.32%（+4.73%），验证了方法在不同模型规模下的稳健性。

定性对比（Figure 4）进一步展示了 ID-CRAFTER 在身份保持、时序连贯性和文本对齐三个维度上的综合优势——基线模型（如 Phantom）在多主体场景中容易出现身份混淆或退化，而 ID-CRAFTER 能维持各主体的独立身份特征。

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Comparison with State-of-the-Art Methods. Our method, ID-CRAFTER, demonstrates superior performance in identity preservation, temporal consistency, and alignment with the textual prompt compared to existing open-source and proprietary models*

### 关键组件消融

Table 2 报告了核心架构组件的消融结果，揭示了三个关键设计的作用机制：

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/006_Table_2.jpg]]
*Table 2: Ablation studies on the key components of ID-CRAFTER. We compare the full model against variants removing hierarchical attention, the VLM encoder, and the curated dataset*

**层次化身份保持注意力**：将其替换为标准交叉注意力（所有主体与文本令牌直接拼接）后，FaceSim 从 58.12% 骤降至 51.34%（↓11.7%），Total Score 下降 7.8%。这表明三阶段注意力（主体内 Self Attention → 门控主体间 Cross Attention → 跨模态 Attention）对解耦主体特征、防止身份退化至关重要。

**VLM 语义编码器**：用单一 T5 编码器替代双编码器架构（T5 + Qwen2.5-VL-7B-Instruct）后，Q-Align 从 0.351 降至 0.287（↓18.2%），文本-视频对齐严重受损。VLM 提供的细粒度语义理解——特别是对复杂主体间关系的空间布局信号——是普通文本编码器无法替代的。

**策划数据集**：移除合成跨主体组合与融合示例后，生成结果出现明显的“复制粘贴”伪影（Figure 5 左），主体与背景的融合自然度显著下降，验证了数据策划管道对训练质量的基础性作用。

### 层次注意力的阶段贡献分析

Table S.5 进一步拆解了层次注意力各阶段的功能。完整三阶段模型性能最优，其中 **Stage 3（跨模态注意力到 VLM）** 对语义对齐最为关键：移除该阶段后，NexusScore 从 45.1% 降至 38.7%。Stage 1（主体内注意力）主要贡献于身份保真度，Stage 2（主体间注意力）则协调多主体交互，三者形成递进式特征聚合链路。

### 在线 RL 优化分析

Table 3 对比了在线 GRPO、离线 DPO 和标准 SFT 基线。在线 GRPO 相对 SFT 基线实现双重提升：FaceSim 从 58.12% 提升至 **66.10%**（↑13.7%），Aesthetics 从 42.50% 提升至 **48.85%**（↑14.9%），验证了在线 RL 在平衡身份保真度与视觉质量方面的有效性。

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/009_Table_3.jpg]]
*Table 3: Analysis of the online RL optimization. We compare our online GRPO approach with offline DPO and a standard SFT baseline. We also ablate the components of our composite reward function*

**复合奖励的组件贡献**：从总奖励中移除自然度成分（$R_{nat}$）后，Q-Align 下降但 FaceSim 与 Aesthetics 微升——这是典型的**奖励黑客（reward hacking）** 现象：模型通过牺牲物理合理性和常识一致性来追逐身份和美学指标。这印证了多维度奖励设计的必要性：保真度奖励（$w_{fid}=0.6$）与质量奖励（$w_{qual}=0.4$）的加权组合（含自然度惩罚）是防止指标间零和博弈的关键。

**GRPO 的群体优势估计机制**：与离线 DPO 相比，在线 GRPO 通过组内相对比较估计优势函数，避免了离线方法中奖励分布偏移导致的优化不稳定问题。Figure S.7 的训练曲线显示，FaceSim、Aesthetics 和文本对齐指标在 800 步内同步提升，未出现相互侵蚀。

### 人类偏好验证

Figure S.13 的人类偏好研究为自动指标提供了主观验证。在身份一致性维度上，ID-CRAFTER 获得 **60%** 的偏好率，显著优于竞争模型；在运动自然度维度上也保持领先。这缓解了自动评估指标（如 FaceSim）与 RL 奖励函数间潜在循环性的担忧——主观评估独立确认了模型的综合优势。

### 失败模式与局限

尽管整体性能领先，分析揭示了两个值得关注的局限：

1. **奖励黑客风险**：如 Table 3 所示，去除自然度奖励后部分指标异常上升，表明单一维度奖励容易被模型“钻空子”。当前通过多维度加权缓解，但更鲁棒的奖励设计仍是开放问题。

2. **计算开销**：层次注意力模块在前 20 层引入了额外计算（Sec E.1），虽总体影响较小，但在资源受限场景下需权衡；GRPO 后训练需要额外的一次性计算成本。

3. **模型规模敏感性**：1.3B 到 14B 的 Total Score 提升幅度（55.16% → 57.05%）小于 Phantom 同规模提升（50.71% → 52.32%），提示层次注意力的收益可能随模型容量增大而边际递减，需更大规模验证。

### 补充图表

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/001_Figure_1.jpg]]
*Figure 1: Given a text prompt and multiple reference images, ID-CRAFTER generates subject-consistent videos and achieves impressive subject ID preservation (e.g., face score) compared with the previous state-of-the-art methods, such as Phantom [29]*

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison against existing methods for the open-domain subject-to-video benchmark. Total score is the normalized weighted sum of other scores. “↑” indicates that higher is better*

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/011_Table_S.5.jpg]]
*Table S.5: Ablation of Hierarchical Attention. We analyze the contribution of each stage in our hierarchical attention mechanism. The full three-stage model provides the best performance, with Stage 3 (cross-modal attention to VLM) being the most critical component for semantic alignment*

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/008_Figure_6.jpg]]
*Figure 6: Applications in Controllable Video Editing. ID-CRAFTER enables zero-shot editing of existing videos, including subject replacement and background modification, while preserving identity and temporal consistency*

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/010_Table_S.4.jpg]]
*Table S.4: Detailed configuration of our model’s primary architectural components. The VLM, VAE, and DiT modules are designed to handle multimodal understanding, spatial compression, and latent diffusion, respectively*

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/013_Table_S.7.jpg]]
*Table S.7: Ablation on Fidelity Reward*

![[assets/figures/papers/paper_list_l2192_https_arxiv_org_abs_2511_00511/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative Ablation Study. The left panel highlights the importance of our curated dataset, demonstrating improved coherence and realism in subject integration (e.g., mitigating ‘copy-paste’ artifacts) compared to a model trained without it. Meanwhile, the right panel illustrates the effectiveness of our online reinforcement learning stage, which significantly enhances visual quality and subject consistency*



## 定位与知识库关联

### 1. 问题定位：多主体视频生成的身份-运动冲突

当前多主体视频生成面临的核心瓶颈在于**身份一致性与时序连贯性之间的固有矛盾**。现有方法在处理多个参考主体时，往往难以同时保持每个主体的独立身份特征和整体视频的运动流畅性，导致不同主体间出现语义冲突和身份退化。这一问题在开放域场景中尤为突出——当文本提示涉及复杂的多主体交互（如“一个男人和一个女人在公园散步”）时，模型容易混淆主体特征，产生“复制粘贴”式的生硬合成效果。

ID-CRAFTER 正是针对这一瓶颈设计的统一框架，其核心思路是通过**层次化注意力机制**解耦主体特征交互，利用**预训练视觉语言模型（VLM）**提供精细语义理解，并引入**在线强化学习**直接优化身份保真度与视频质量的复合奖励，从而缓解身份保持与运动生成之间的张力。

### 2. 与现有方法的关系

#### 2.1 基底架构继承

ID-CRAFTER 建立在**视频扩散 Transformer（DiT）**和 **Rectified Flow** 的生成范式之上。其骨干网络基于 **Wan-Video**（2024），采用潜空间视频扩散架构：VAE 编码器将输入视频压缩到潜空间，DiT 在潜空间上预测 Rectified Flow 的速度场。这一选择继承了扩散模型在视频生成中的高质量输出能力，同时利用 Rectified Flow 的直线轨迹特性（$\mathbf{z}_t = (1 - t) \mathbf{z}_0 + t \mathbf{\epsilon}$）实现高效的采样。

#### 2.2 与现有身份保持方法的对比

在身份保持机制上，现有方法主要分为两类：

- **基于注意力特征注入的方法**：如 **Phantom**（开源多主体视频生成）和 **VACE**（基于注意力编辑的视频生成），它们通过将参考主体特征注入到生成过程的交叉注意力层中来保持身份。这类方法的核心局限在于将所有主体和文本令牌简单拼接后送入标准交叉注意力，缺乏对主体间交互的精细建模，容易导致身份混淆。
- **基于参考图像条件的方法**：如 **SkyReels-A2** 等，通过额外的编码器将参考图像作为条件输入。这些方法在单主体场景下表现尚可，但在多主体场景中难以有效解耦不同主体的特征。

ID-CRAFTER 的关键改进在于将上述方法中的**标准交叉注意力**替换为**三阶段层次化身份保持注意力**：
1. **主体内自注意力（Stage 1）**：在每个主体的特征内部进行自注意力，精细化该主体的细节表征；
2. **门控主体间交叉注意力（Stage 2）**：在不同主体特征之间进行门控交叉注意力，建模主体间的空间关系与交互；
3. **跨模态注意力（Stage 3）**：将主体特征与 VLM 语义令牌进行交叉注意力，实现跨模态语义对齐。

这一层次化设计从根本上改变了特征交互的方式——从“所有信息混合处理”转向“由内而外、逐步融合”，从而有效解耦了身份保持与运动生成之间的冲突。

#### 2.3 与 VLM 增强方法的关系

近年来，利用预训练视觉语言模型增强生成任务已成为趋势。ID-CRAFTER 采用**双编码器架构**（T5 + **Qwen2.5-VL-7B-Instruct**），将 VLM 作为语义理解模块。与仅使用单一 T5 编码器的基线相比，VLM 能够对多模态输入（文本提示 + 参考图像）进行联合推理，输出包含空间布局和主体关系信息的语义令牌，为视频生成提供更精细的指导。消融实验表明，移除 VLM 编码器会导致文本-视频对齐指标 Q-Align 从 0.351 降至 0.287（↓18.2%），验证了 VLM 在语义对齐中的关键作用。

#### 2.4 与 RL 优化方法的关系

在生成模型的后训练优化方面，现有工作多采用**监督微调（SFT）**或**离线偏好优化（DPO）**。ID-CRAFTER 首次将**在线群组相对策略优化（GRPO）**引入多主体视频生成。与离线方法相比，在线 GRPO 的优势在于：
- 通过**群组内相对比较**估计优势函数，避免了训练独立价值模型的成本；
- 直接优化不可微的**复合感知奖励**（身份保真度 + 视频质量），而非依赖固定偏好数据集；
- 在训练过程中持续采样新生成结果，使策略能够适应奖励函数的细微偏好。

实验表明，在线 GRPO 相比 SFT 基线使 FaceSim 从 58.12% 提升至 66.10%（↑13.7%），Aesthetics 从 42.50% 提升至 48.85%（↑14.9%），同时显著优于离线 DPO 方法。

### 3. 适用边界与局限

#### 3.1 适用场景

ID-CRAFTER 在以下场景中展现出显著优势：
- **多主体（2个以上）视频生成**：层次化注意力能够有效解耦多个主体的特征，避免身份混淆；
- **需要精细身份保持的应用**：如虚拟角色动画、个性化视频内容创作等，FaceSim 指标可达 66.10%；
- **复杂文本-视觉对齐**：VLM 模块使模型能够理解主体间的空间关系和语义交互；
- **零样本视频编辑**：如主体替换和背景修改（Figure 6 所示），无需额外训练。

#### 3.2 已知局限

1. **计算开销**：层次注意力模块在前 20 层增加了少许计算成本，GRPO 后训练需额外的一次性计算（详见原文 Sec E.1）。虽然总体影响较小，但在资源受限场景下需权衡。

2. **奖励黑客风险**：自动奖励函数设计存在被策略利用的可能。消融实验显示，从复合奖励中去除自然度成分（$\mathcal{R}_{\text{nat}}$）后，Q-Align 下降但 FaceSim 与 Aesthetics 微升，提示策略可能通过牺牲自然度来优化其他指标。这要求奖励函数设计需多维度平衡。

3. **评估循环性**：自动评估指标（如 FaceSim）可能与 RL 奖励函数存在潜在循环性——模型可能学会生成在特定指标上得分高但未必更优的视频。虽然人类偏好研究（Figure S.13）验证了主观优势，但评估体系的独立性仍需持续关注。

4. **训练数据依赖**：策划数据集包含合成跨主体组合与融合示例，数据质量直接影响模型对复杂主体交互的泛化能力。数据策划管道的覆盖度决定了模型的上限。

### 4. 开放问题与未来方向

1. **奖励函数的泛化设计**：当前复合奖励由保真度（权重 0.6）和质量（权重 0.4）加权组成，权重选择依赖经验。如何设计自适应的奖励权重机制，使模型在不同场景下自动平衡身份保持与运动质量，是一个开放问题。

2. **层次注意力的可扩展性**：三阶段注意力在主体数量增加时的计算复杂度如何变化？是否可以通过稀疏注意力或主体聚类进一步降低开销，以支持更多主体的场景？

3. **VLM 与生成模型的深度融合**：当前 VLM 仅作为语义编码器提供条件输入，其推理能力未被充分利用。是否可以让 VLM 参与生成过程的中间步骤（如动态调整注意力权重、检测并修正身份退化），实现更深层次的协同？

4. **跨域泛化**：ID-CRAFTER 在人物主体上表现突出，但在非人物主体（如动物、物体）上的身份保持能力是否同样有效？层次注意力的设计是否需要对不同主体类型进行调整？

5. **评估体系的完善**：当前评估依赖自动指标和有限的人类偏好研究。建立更全面、独立的多主体视频生成评估基准，涵盖更多维度的质量指标（如主体交互合理性、长期时序一致性），仍是领域内的共同挑战。



## 原文 PDF

![[paperPDFs/CVPR_2026/ID_Crafter_VLM_Grounded_Online_RL_for_Compositional_Multi_Subject_Video_Generation.pdf]]
