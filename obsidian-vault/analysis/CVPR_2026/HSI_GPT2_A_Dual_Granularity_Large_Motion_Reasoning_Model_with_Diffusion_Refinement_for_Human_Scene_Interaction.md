---
title: "HSI-GPT2: A Dual-Granularity Large Motion Reasoning Model with Diffusion Refinement for Human-Scene Interaction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HSI_GPT2_A_Dual_Granularity_Large_Motion_Reasoning_Model_with_Diffusion_Refinement_for_Human_Scene_Interaction.pdf
project_link: null
code_link: null
aliases:
- HG
- HSI-GPT2
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过双粒度运动分词器（DMoTok）解耦语义与物理细节、用扩散解码器替代单一的VQVAE解码器、以及引入MoCoT思维链数据引擎与GRPO强化学习优化，共同构成克服瓶颈的关键实现路径。
primary_logic: 将LLM作为高层次语义规划器与扩散模型作为低层次运动合成器分离，同时借助可验证奖励驱动的强化学习让模型学会分解指令、执行长期组合推理，从而在理解与生成任务中同时获得语义对齐与物理真实性的提升。
claims:
- HSI-GPT2在HumanML3D文本到运动生成中将FID从HSI-GPT的0.187降至0.139，并取得了最高的R-Precision Top1 0.545。
- 在HUMANISE数据集上，Goal Distance从0.182降至0.143，Contact Rate从92.31%提升至97.98%。
- 消融实验表明，双粒度码本结合连续输入设计能将FID从0.193降至0.160，GRPO优化进一步将FID降至0.139（Table 6, 7）。
- HumanML3D (text-to-motion) 上 FID ↓ = 0.139 ± .002
---

# HSI-GPT2: A Dual-Granularity Large Motion Reasoning Model with Diffusion Refinement for Human-Scene Interaction

> [!tip] 核心洞察
> 将LLM作为高层次语义规划器与扩散模型作为低层次运动合成器分离，同时借助可验证奖励驱动的强化学习让模型学会分解指令、执行长期组合推理，从而在理解与生成任务中同时获得语义对齐与物理真实性的提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | HSI-GPT2：面向人-场景交互的双粒度大运动推理模型及扩散精炼 |
| 英文题名 | HSI-GPT2: A Dual-Granularity Large Motion Reasoning Model with Diffusion Refinement for Human-Scene Interaction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_HSI-GPT2_A_Dual-Granularity_Large_Motion_Reasoning_Model_with_Diffusion_Refinement_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | HSI-GPT2 |
| Dataset | HumanML3D, HUMANISE |

> [!tip] 效果简介
> - HumanML3D (text-to-motion) 上，FID ↓ 0.139 ± .002 vs 0.187 ± .004 (HSI-GPT) / 0.269 ± .001 (MotionCLR) (降低至HSI-GPT的74%，远优于其他方法)；R-Precision Top 1 ↑ 0.545 ± .002 vs 0.495 ± .002 (HSI-GPT) / 0.544 ± .001 (MotionCLR) (高出HSI-GPT 5个百分点，与最佳方法持平或略优)。
> - HUMANISE (text-conditioned HSI generation) 上，Goal Distance ↓ 0.143 vs 0.182 ± .008 (HSI-GPT) / 0.156 ± .006 (Afford@2) (较HSI-GPT降低21.4%)。
> - HumanML3D (motion captioning) 上，R-Precision Top 1 ↑ 0.583 vs 0.551 (HSI-GPT) / 0.573 (MotionGPT-3) (显著优于所有对比方法)。

## 概要

人-场景交互（HSI）的统一建模面临一个根本性瓶颈：现有方法依赖**单粒度运动码本**，过度强调低层次运动细节，却丢失了高层次运动语义；同时，**运动解码器能力有限**，难以生成高保真的场景交互动作；此外，仅靠**监督微调（SFT）**无法赋予模型组合推理与语义对齐的能力。

HSI-GPT2 的核心思路是将**LLM作为高层语义规划器**与**扩散模型作为低层运动合成器**解耦，通过三个关键设计打破上述瓶颈：

1. **双粒度运动分词器（DMoTok）**：将3D人体运动同时编码为语义token（经CLIP对比学习与文本对齐）和细节token（保留物理细节），从表示层面分离“做什么”与“怎么做”。
2. **LLM-扩散混合解码**：以MLD潜空间扩散解码器替代传统VQVAE解码器，以LLM输出的语义/细节token和场景查询为条件迭代去噪，大幅提升运动保真度。
3. **MoCoT思维链数据引擎 + GRPO强化学习**：通过自动化流水线生成带思维链的监督数据冷启动，再引入格式奖励、语义奖励、保真度奖励进行组相对策略优化（GRPO），使模型学会分解指令并执行长期组合推理。

在HumanML3D文本到运动生成任务上，HSI-GPT2将FID从HSI-GPT的0.187降至**0.139**，R-Precision Top1达到**0.545**；在HUMANISE场景交互生成中，Goal Distance从0.182降至**0.143**，Contact Rate从92.31%提升至**97.98%**。消融实验证实，双粒度码本与连续输入设计将FID从0.193降至0.160，GRPO多奖励优化进一步降至0.139，验证了表示解耦与可验证奖励驱动推理的有效性。

在方法谱系中，HSI-GPT2延续了统一HSI模型（**HSI-GPT**, Wang et al., CVPR 2025）的LLM框架，但在运动表示、解码器架构和训练范式三个维度进行了系统性升级，同时与LLM-based运动生成方法（**MotionGPT**, Jiang et al., NeurIPS 2023; **MotionGPT-2**, Wang et al., Arxiv 2024; **MotionCLR**, Chen et al., NeurIPS 2025）和场景感知方法（**Afford-Motion**, Wang et al., CVPR 2024）形成差异化竞争。



### 问题背景

人-场景交互（Human-Scene Interaction, HSI）的建模与生成是计算机视觉与图形学中的核心挑战，其目标是在三维场景中合成语义合理、物理真实的人体运动。该任务横跨运动理解与运动生成两大方向：理解任务要求模型从运动序列中提取高层次的语义描述，生成任务则需根据文本指令或场景上下文合成符合物理约束的人体动作。近年来，以大型语言模型（LLM）为骨干的统一框架逐渐兴起，试图将理解与生成纳入同一模型体系，**HSI-GPT**（Wang et al., CVPR 2025）即是这一方向的代表性工作。

然而，现有统一HSI模型在实际部署中暴露出三个相互耦合的瓶颈，制约了其在复杂场景下的表现。

### 现有方法缺口

**瓶颈一：单粒度码本过度强调低层次运动细节，忽略高层次运动语义。** 现有方法（如MotionGPT、HSI-GPT）普遍采用单一粒度的VQVAE码本对运动序列进行离散化编码。这类码本以重建为导向，天然倾向于保留关节角度、速度曲线等细粒度物理细节，却无法有效捕获“行走”“转身”“坐下”等抽象运动语义。由此产生的运动token与自然语言之间存在语义鸿沟，LLM难以建立跨模态的对齐关系，导致在运动理解与文本驱动生成任务中出现语义漂移。

**瓶颈二：运动解码器能力有限，限制了高保真的人-场景交互。** 统一框架通常依赖VQVAE解码器直接从离散token重建运动序列。该解码器在单粒度码本约束下，其重建能力受限于码本容量与离散化误差，难以同时兼顾运动的平滑性、接触约束与场景几何的精确匹配。在HUMANISE等场景感知生成任务中，这一不足直接体现为目标距离（Goal Distance）偏高、接触率（Contact Rate）偏低。

**瓶颈三：仅依赖监督微调（SFT）无法捕捉高级语义与逻辑推理能力。** 现有LLM-based运动模型通常仅通过监督微调学习从文本到运动token的映射。这种训练范式缺乏对推理过程的显式建模，模型难以处理多步骤组合指令（如“先走向椅子，再坐下，最后交叉双腿”），也无法在生成过程中自我纠错或权衡语义对齐与物理保真度之间的冲突。

### 本文动机

针对上述三重瓶颈，本文提出**HSI-GPT2**，核心动机在于将高层次语义规划与低层次运动合成解耦，并引入可验证奖励驱动的强化学习范式，使模型具备组合推理与自我优化的能力。具体而言，HSI-GPT2的设计围绕三个关键机制展开：

1. **双粒度运动分词器（DMoTok）**：通过语义码本与细节码本解耦，语义分支经CLIP对比学习对齐文本，使LLM能够在语义层面进行推理规划，同时保留物理细节用于高保真合成。
2. **LLM–扩散混合解码框架**：以LLM输出的语义/细节token为条件，采用基于MLD的潜空间扩散解码器替代传统的VQVAE解码器，迭代去噪生成物理真实的人体运动。
3. **MoCoT思维链数据引擎与GRPO强化学习**：构建自动化思维链数据生成流水线，以格式奖励、语义奖励、保真度奖励等多方面可验证信号驱动组相对策略优化（GRPO），使模型学会分解复杂指令并执行长期组合推理。

这一设计使得HSI-GPT2在HumanML3D文本到运动生成中将FID从HSI-GPT的0.187降至**0.139**，R-Precision Top 1提升至**0.545**；在HUMANISE数据集上，Goal Distance从0.182降至**0.143**，Contact Rate从92.31%提升至**97.98%**（Table 1, Table 3）。消融实验进一步证实，双粒度码本与GRPO优化各自贡献了显著的性能增益（Table 6, Table 7）。



## 核心方法与创新机理

HSI-GPT2 的核心创新并非单一模块的替换，而是围绕“语义规划与物理合成解耦”这一思想，对现有统一人-场景交互（HSI）模型的三个关键瓶颈进行了系统性改造。相对于以 **HSI-GPT** (Wang et al., CVPR 2025) 为代表的基线方法，HSI-GPT2 在运动表示、解码能力和推理范式三个维度上引入了实质性的 changed slots。

### 1. 从单粒度到双粒度的运动表示

现有方法（如 HSI-GPT、**MotionGPT** (Jiang et al., NeurIPS 2023)）普遍采用单粒度 VQVAE 码本对运动进行离散化，其优化目标以重建为导向，导致码本过度关注低层次运动细节，而忽略高层次运动语义。HSI-GPT2 提出的 **双粒度运动分词器 (DMoTok)** 从根本上改变了这一范式：

- **语义码本与细节码本解耦**：DMoTok 分别学习一个语义码本 $\mathcal{C}_{\mathrm{sem}}$ 和一个细节码本 $\mathcal{C}_{\mathrm{det}}$。语义分支经 CLIP 风格的对比学习与文本对齐，使得量化后的语义 token $\mathcal{T}_{\mathrm{sem}}$ 能够捕获“行走”、“转身”等高层运动概念；细节分支则保留关节角度、速度等物理细节，生成细节 token $\mathcal{T}_{\mathrm{det}}$。
- **连续输入/离散输出设计**：LLM 接收的是连续的语义特征 $\mathcal{Z}_{\mathrm{sem}}$ 而非离散 token，这抑制了量化误差对语义理解的干扰；LLM 输出的是离散的语义/细节 token，供后续扩散解码器使用。消融实验（Table 6）表明，双粒度码本结合连续输入设计将 FID 从 0.193 降至 0.160，R-Precision 从 0.788 提升至 0.809，验证了语义与细节分离的有效性。

### 2. 从 VQVAE 解码器到扩散解码器的生成能力升级

基线方法（如 HSI-GPT、**MotionCLR** (Chen et al., NeurIPS 2025)）通常使用 VQVAE 解码器直接从离散 token 重建运动，其解码能力受限于 VAE 的表达瓶颈，难以生成高保真且物理合理的人-场景交互运动。HSI-GPT2 用 **基于 MLD 的运动扩散解码器** 替代了传统的 VQVAE 解码器：

- **LLM–Diffusion 混合框架**：LLM 充当高层次语义规划器，负责将文本指令分解为可执行的动作序列，输出语义/细节 token；扩散解码器以这些 token 和场景查询为条件，在潜空间迭代去噪生成运动。这一分离使得语义规划与物理合成各司其职。
- **保真度提升的因果机制**：扩散模型的迭代精炼能力使其能够生成更平滑、更符合物理约束的运动。在 HUMANISE 数据集上，Goal Distance 从 HSI-GPT 的 0.182 降至 0.143，Contact Rate 从 92.31% 提升至 97.98%（Table 3），直接体现了扩散解码器在交互精度上的优势。

### 3. 从 SFT 到 GRPO 强化学习的推理能力注入

统一 HSI 模型的传统训练范式仅依赖监督微调（SFT），模型缺乏对复杂指令的分解推理能力。HSI-GPT2 引入了 **MoCoT 思维链数据引擎** 与 **GRPO 强化学习** 的组合：

- **MoCoT 冷启动**：自动化流水线融合视频渲染与多模态 LLM，将运动描述分解为结构化的动作序列，生成带思维链的监督数据，为模型提供初始的推理行为模板。
- **多奖励 GRPO 优化**：在 MoCoT 冷启动后，引入组相对策略优化（GRPO），结合格式奖励 $r_{\mathrm{form}}$、语义对齐奖励 $r_{\mathrm{sem}}$ 和保真度奖励 $r_{\mathrm{fid}}$。格式奖励引导模型输出结构化 token，语义奖励确保文本-运动语义对齐，保真度奖励约束物理真实性。
- **消融证据**：Table 7 显示，仅使用 SFT 微调 CoT 轨迹而不引入奖励指导时，性能明显弱于 GRPO 方案；同时加入语义奖励和保真度奖励使 FID 从 0.185 降至 0.139，Contact Rate 从 92.52% 升至 97.98%，验证了多奖励设计的必要性。训练曲线（Figure 7）进一步揭示，格式奖励在约 70 步达到峰值后，优化重心自动转向语义和保真度奖励，体现了 GRPO 的动态权衡能力。

### 创新总结

上述三个 changed slots 构成了一个因果闭环：DMoTok 提供了语义与细节解耦的表示基础，扩散解码器释放了从离散 token 到连续运动的高保真生成潜力，而 GRPO 强化学习则赋予模型将复杂指令分解为可执行动作序列的推理能力。三者的协同使得 HSI-GPT2 在 HumanML3D 文本到运动生成中将 FID 降至 0.139（较 HSI-GPT 的 0.187 降低约 26%），在 HUMANISE 场景交互生成中将 Goal Distance 降至 0.143（降低 21.4%），同时在运动描述任务中取得了最高的 R-Precision Top 1 0.583（Table 2）。



HSI-GPT2 的整体架构围绕一个核心设计原则展开：**将 LLM 作为高层次语义规划器，将扩散模型作为低层次运动合成器，二者通过双粒度运动分词器（DMoTok）实现解耦与协同**。如图 Figure 2 所示，系统由四个关键模块串联构成：

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the proposed HSI-GPT2. (a) DMoTok jointly encodes both fine-grained physical details and high-level motion semantics. (b) The unified MLLM framework supports both HSI-related understanding and generation tasks. (c) The latent diffusion refiner decodes discrete tokens into high-fidelity and text-aligned motions in 3D scene. (d) An interleaved scene-motion-language representations*

1. **双粒度运动分词器（DMoTok）**：接收 3D 人体运动序列，通过语义编码器和细节编码器分别提取文本对齐的语义特征与保留物理细节的特征，再经两个独立码本量化为离散的语义 token 和细节 token。这一设计直接回应了“单粒度码本过度强调低层次细节”的瓶颈。
2. **统一多模态大语言模型（MLLM）**：以 Qwen 等 LLM 为骨干，扩展词表以容纳运动语义/细节 token 和场景 token。LLM 接收文本指令、场景点云特征和连续运动特征，输出离散的运动 token 序列及文本响应，承担语义规划与任务路由的角色。
3. **运动扩散解码器（MLD）**：替代传统 VQVAE 解码器，以 LLM 输出的语义/细节 token 和场景查询为条件，在潜空间执行迭代去噪，生成高保真 3D 人体运动。这解决了“运动解码器能力有限”的瓶颈。
4. **MoCoT 思维链数据引擎 + GRPO 强化学习**：MoCoT 引擎通过视频渲染与多模态 LLM 自动将运动描述分解为可执行的动作序列，生成带思维链的冷启动数据；随后 GRPO 利用格式、语义、保真度等多方面可验证奖励进行策略优化，使模型习得分解指令与长期组合推理的能力。

**输入输出流**：对于文本到运动生成任务，用户文本指令送入 MLLM，MLLM 输出语义/细节 token 序列，扩散解码器据此合成 3D 运动；对于运动理解任务，运动经 DMoTok 编码后送入 MLLM 生成文本描述。场景感知的 HSI 生成则额外引入场景点云编码，LLM 进行可操作区域感知的语义规划，扩散解码器在 3D 场景约束下完成物理真实的运动合成。

### 补充图表

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/002_Figure_1.jpg]]
*Figure 1: Overview of the Motion Chain-of-Thought (MoCoT) and training pipeline of our HSI-GPT2. The SFT initialization on curated cold-start data, then refined with RL tuning, HSI-GPT2 achieves leading performance across HSI-centric generation and understanding tasks*



HSI-GPT2 的技术架构围绕三个关键模块展开：**双粒度运动分词器（DMoTok）**、**统一多模态大语言模型（Unified MLLM）** 以及 **运动扩散解码器（Motion Diffusion Decoder）**。三者协同工作，将高层次语义推理与低层次物理运动合成解耦，并通过强化学习优化实现端到端的语义对齐与物理保真。

### 双粒度运动分词器（DMoTok）

DMoTok 的核心设计思想是将 3D 人体运动同时编码为两种互补的离散令牌：语义令牌与细节令牌。语义分支通过 CLIP 风格的对比学习与文本对齐，捕获运动的高层次语义（如“走路”、“坐下”）；细节分支则保留关节角度、速度等细粒度物理信息。

具体而言，给定运动序列 $m$，语义编码器 $\mathcal{E}_{\mathrm{sem}}$ 和细节编码器 $\mathcal{E}_{\mathrm{det}}$ 分别提取特征 $\mathcal{Z}_{\mathrm{sem}}$ 和 $\mathcal{Z}_{\mathrm{det}}$。随后，两个特征分别通过可学习码本 $\mathcal{C}_{\mathrm{sem}}$ 和 $\mathcal{C}_{\mathrm{det}}$ 进行向量量化：

- **语义量化**：将文本对齐的语义特征离散化到语义码本中（Equation 1）：

$$\hat{\mathcal{Z}}_{\mathrm{sem}}, \mathcal{T}_{\mathrm{sem}} = \operatorname{argmin}_{k \in \{1, \dots, K\}} \| \mathcal{Z}_{\mathrm{sem}} - \mathcal{C}_{\mathrm{sem}}[k] \|$$

- **细节量化**：将物理细节特征离散化到细节码本中（Equation 2）：

$$\hat{\mathcal{Z}}_{\mathrm{det}}, \mathcal{T}_{\mathrm{det}} = \operatorname{argmin}_{k \in \{1, \dots, K\}} \| \mathcal{Z}_{\mathrm{det}} - \mathcal{C}_{\mathrm{det}}[k] \|$$

其中 $\mathcal{T}_{\mathrm{sem}}$ 和 $\mathcal{T}_{\mathrm{det}}$ 分别为量化后的语义令牌与细节令牌，$\hat{\mathcal{Z}}_{\mathrm{sem}}$ 和 $\hat{\mathcal{Z}}_{\mathrm{det}}$ 为对应的量化特征。

向量量化的训练目标 $\mathcal{L}_{\mathrm{vq}}$ 包含三项（Equation 3）：

$$\mathcal{L}_{\mathrm{vq}} = \mathrm{Sim}(\hat{m}, m) + \| \mathrm{sg}[\mathcal{Z}] - \hat{\mathcal{Z}} \|_2^2 + \beta \| \mathcal{Z} - \mathrm{sg}[\hat{\mathcal{Z}}] \|_2^2$$

- 第一项 $\mathrm{Sim}(\hat{m}, m)$ 为重建运动 $\hat{m}$ 与原始运动 $m$ 的相似度损失；
- 第二项为码本损失，强制码本向量 $\hat{\mathcal{Z}}$ 接近编码器输出 $\mathcal{Z}$（$\mathrm{sg}[\cdot]$ 表示停止梯度算子）；
- 第三项为承诺损失，以权重 $\beta$ 约束编码器输出不偏离码本向量过远。

### 统一 MLLM 与扩散解码器

LLM 骨干网络（基于 Qwen 等模型）接收离散的语义/细节令牌、场景令牌及文本指令，输出高层次的语义规划结果——包括新的语义令牌和细节令牌。这些离散令牌随后作为条件信号，馈入基于 **MLD**（Motion Latent Diffusion）的扩散解码器。

扩散解码器在潜空间中进行迭代去噪。其前向扩散过程为马尔可夫加噪过程（Equation 4）：

$$q(\mathcal{Z}_t \mid \mathcal{Z}_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} \mathcal{Z}_{t-1}, (1-\alpha_t) I)$$

其中 $\mathcal{Z}_t$ 为第 $t$ 步的噪声潜变量，$\alpha_t$ 为噪声调度参数。逆向过程以 LLM 输出的语义/细节令牌和场景查询为条件，逐步从纯噪声 $\mathcal{Z}_T$ 去噪得到干净的潜变量 $\mathcal{Z}_0$，最终解码为高保真人体运动序列。该设计将低层次运动合成完全交由扩散模型处理，使 LLM 专注于语义规划，从而在生成质量与推理能力之间取得平衡。

### GRPO 强化学习优化

在 MoCoT 思维链数据引擎冷启动后，HSI-GPT2 采用 **组相对策略优化（GRPO）** 进行强化学习微调。GRPO 目标函数为（Equation 5）：

$$\mathcal{I}_{\mathrm{GRPO}} = \mathbb{E}\bigl[ \frac{1}{G} \sum_{i=1}^{G} \min ( \frac{\pi_{\theta}(o_i)}{\pi_{\mathrm{old}}(o_i)} \hat{A}_i, \mathrm{clip}( \frac{\pi_{\theta}(o_i)}{\pi_{\mathrm{old}}(o_i)}, 1-\varepsilon, 1+\varepsilon) \hat{A}_i ) - \beta D_{\mathrm{KL}}(\pi_{\theta} \parallel \pi_{\mathrm{ref}}) \bigr]$$

其中 $\pi_{\theta}$ 和 $\pi_{\mathrm{old}}$ 分别为当前策略与旧策略，$\hat{A}_i$ 为组内相对优势估计，$\varepsilon$ 为裁剪阈值，$D_{\mathrm{KL}}$ 为与参考策略 $\pi_{\mathrm{ref}}$ 的 KL 散度惩罚项，$\beta$ 控制惩罚强度。

奖励信号由三部分组成：格式奖励 $r_{\mathrm{form}}$ 确保输出结构符合预期；语义对齐奖励 $r_{\mathrm{sem}}$ 和保真度奖励 $r_{\mathrm{fid}}$ 分别以余弦相似度形式衡量生成运动与文本的语义一致性及与真实运动的物理相似性（Equation 6）：

$$r_{\mathrm{fid}} = \frac{\Psi(\hat{m}) \cdot \Psi(m)}{\|\Psi(\hat{m})\| \cdot \|\Psi(m)\|}, \quad r_{\mathrm{sem}} = \frac{\phi(\hat{m}) \cdot \phi(T)}{\|\phi(\hat{m})\| \cdot \|\phi(T)\|}$$

其中 $\Psi(\cdot)$ 为预训练的运动细节编码器，$\phi(\cdot)$ 为 CLIP 风格的语义编码器，$T$ 为输入文本。训练曲线（Figure 7）显示，格式奖励在约 70 步时率先达到峰值，随后优化重心自动转移至语义奖励和保真度奖励，验证了多奖励设计的协同效应。



## 实验与关键发现

### 核心性能突破

HSI-GPT2 在文本到运动生成、人-场景交互生成及运动理解任务上均取得显著领先。在 HumanML3D 文本到运动生成基准上，HSI-GPT2 将 FID 从 HSI-GPT 的 0.187 降至 **0.139**（Table 1），降幅达 25.7%；R-Precision Top 1 达到 **0.545**，高出 HSI-GPT 五个百分点，与 MotionCLR 持平或略优。在 HUMANISE 数据集的人-场景交互生成中，Goal Distance 从 0.182 降至 **0.143**，Contact Rate 从 92.31% 提升至 **97.98%**（Table 3），验证了模型在物理真实性和语义对齐上的双重提升。

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/008_Table_1.jpg]]
*Table 1: Quantitative results on the HumanML3D test set. † denotes the text-based motion generation method based on LLM. ± represents a 95% confidence interval following [14]. → indicates that metrics improve as they get closer*

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/009_Table_3.jpg]]
*Table 3: Quantitative performance of text-conditioned HSI generation. † marks our reproduced results on HUMANISE [54] dataset. Displacement Error (FDE) [36, 66] assess motion precision*

在运动理解任务上，HSI-GPT2 在 HumanML3D 运动描述任务中取得 R-Precision Top 1 **0.583**，显著优于 HSI-GPT（0.551）和 MotionGPT-3（0.573）（Table 2）。定性对比显示，HSI-GPT2 生成的描述在概念和语义层面更为丰富（Figure 3），在泛化评估集上相较 HSI-GPT 展现出更强的组合推理能力（Figure 4）。

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/007_Table_2.jpg]]
*Table 2: Results of motion captioning on HumanML3D [14] and general motion completion tasks on AMASS [37]. Best viewed in color*

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/005_Figure_3.jpg]]
*Figure 3: Comparisons on the motion captioning task. HSI-GPT2 generates conceptually and semantically rich motion descriptions*

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/006_Figure_4.jpg]]
*Figure 4: Visual qualitative analysis comparing HSI-GPT [53] and our HSI-GPT2 performance on the generalization evaluation set*

### 消融实验：关键设计验证

**双粒度码本与连续输入。** Table 6 的消融表明，将单粒度码本替换为语义-细节双粒度码本，并结合连续特征输入（而非纯离散 token），使 FID 从 0.193 降至 0.160，R-Precision 从 0.788 提升至 0.809。这证实分离高层语义与低层物理细节的码本设计是性能提升的核心因素之一。

**GRPO 强化学习与多奖励设计。** Table 7 显示，仅使用 SFT 微调思维链轨迹（row d）性能明显弱于引入 GRPO 的方案。当同时加入语义奖励 $r_{\mathrm{sem}}$ 和保真度奖励 $r_{\mathrm{fid}}$ 时，FID 从 0.185 进一步降至 0.139，Contact Rate 从 92.52% 跃升至 97.98%（row g），验证了可验证奖励对强化推理行为与运动质量的关键作用。训练曲线（Figure 7）显示，格式奖励在约 70 步率先收敛，随后优化重心自动转移至语义对齐和保真度奖励，展现出多奖励协同优化的内在调度机制。

**LLM-扩散混合架构泛化性。** Table 4 的跨模型测试表明，HSI-GPT2 的混合架构在不同规模的 Qwen 和 Llama 底座上均能稳定带来增益，证明框架对 LLM 底座具有良好的泛化能力。

### 失败模式与局限

当前实验验证集中于 HumanML3D、HUMANISE 等室内单人交互数据集。模型在户外场景、多人交互或超长序列上的泛化能力尚未得到验证，需要后续工作探索。此外，DMoTok 的语义码本大小 $K$ 和细节码本大小对不同任务性能的权衡关系尚不明确，GRPO 训练中奖励权重的自适应调整策略及其在更大规模 LLM 上的扩展性也值得进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/015_Table_6.jpg]]
*Table 6: Ablation study of the motion tokenizer and input modality*

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/016_Table_7.jpg]]
*Table 7: Ablations of COT and reward during GRPO-based tuning*

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/010_Table_4.jpg]]
*Table 4: Ablation of the hybrid LLM+Diffusion architecture with foundational LLMs. The shaded entries denote the hybrid setup. HSI-GPT2 achieves remarkable generalization across LLMs*

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/013_Figure_7.jpg]]
*Figure 7: Illustration of the training curve of*

![[assets/figures/papers/paper_list_l967_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_HSI_GPT2_A_Dual_G/figures/004_Figure_5.jpg]]
*Figure 5: Visualization comparison with leading text-to-motion methods under multi-step complex instructions on HumanML3D*



## 定位与知识库关联

### 1. 与基线工作的关系

HSI-GPT2 直接继承并重构了 **HSI-GPT**（Wang et al., CVPR 2025）的统一人-场景交互（HSI）框架。HSI-GPT 首次将 LLM 引入 HSI 生成与理解，但其存在三个结构性瓶颈：单粒度运动码本过度强调低层次细节而忽略语义；VQVAE 解码器能力受限，难以保证高保真交互；仅依赖监督微调（SFT）无法捕捉高级语义与逻辑推理能力。HSI-GPT2 通过三项关键改造突破了这些限制：

- **运动分词器**：从单粒度重建导向的 VQVAE 码本，升级为双粒度运动分词器 **DMoTok**，解耦语义码本与细节码本，语义分支经 CLIP 对比学习对齐文本（Equation 1–2，Section 3.1）。
- **运动解码器**：用基于 **MLD**（motion latent diffusion）的扩散解码器替代 VQVAE 直接离散重建，以 LLM 输出的语义/细节 token 为条件迭代去噪，将解码能力从离散重建提升为物理真实运动合成（Section 3.2）。
- **推理与训练范式**：从纯 SFT 扩展为 **MoCoT 思维链数据引擎**冷启动 + **GRPO 强化学习**，引入格式、语义、保真度等多方面可验证奖励（Equation 5–6，Section 3.3–3.4）。

在文本到运动生成任务上，HSI-GPT2 将 HumanML3D 的 FID 从 HSI-GPT 的 0.187 降至 0.139（降低约 26%），R-Precision Top 1 从 0.495 提升至 0.545（Table 1）。在 HUMANISE 数据集上，Goal Distance 从 0.182 降至 0.143（降低 21.4%），Contact Rate 从 92.31% 提升至 97.98%（Table 3）。消融实验进一步验证：双粒度码本结合连续输入设计将 FID 从 0.193 降至 0.160（Table 6），GRPO 中同时加入语义和保真度奖励将 FID 从 0.185 降至 0.139（Table 7）。

与其他 LLM 基运动生成方法的对比同样显著。**MotionGPT**（Jiang et al., NeurIPS 2023）和 **MotionGPT-2**（Wang et al., arXiv 2024）采用单粒度运动 token 化，在 HumanML3D 上 FID 分别为 0.281 和 0.510，远高于 HSI-GPT2 的 0.139。**MotionCLR**（Chen et al., NeurIPS 2025）虽在 R-Precision 上接近（0.544 vs 0.545），但其 FID 为 0.269，表明 HSI-GPT2 在语义对齐与物理保真度的双重维度上实现了更好的平衡。在场景感知生成方面，**Afford-Motion**（Wang et al., CVPR 2024）的 Goal Distance 为 0.156，HSI-GPT2 进一步降至 0.143。

### 2. 适用边界与泛化能力

HSI-GPT2 的核心设计——LLM 作为高层次语义规划器、扩散模型作为低层次运动合成器——在多个 LLM 底座上表现出稳定的泛化性。Table 4 的跨模型测试表明，该框架在 Qwen 系列和 Llama 系列模型上均能带来一致增益，LLM 底座的选择不影响架构的核心优势。

然而，当前验证范围存在明确边界：

- **场景类型**：所有实验均在 HumanML3D、HUMANISE、AMASS 等以室内交互为主的数据集上进行，尚未覆盖户外场景、多人交互或复杂长序列任务。
- **码本规模**：DMoTok 的语义码本大小 $K$ 和细节码本大小对 FID 与 R-Precision 的权衡关系尚未系统探索，不同任务（如生成 vs 理解）可能要求不同的码本配置。
- **奖励权重**：GRPO 训练中格式奖励 $r_{\text{form}}$、语义奖励 $r_{\text{sem}}$ 和保真度奖励 $r_{\text{fid}}$ 的权重为固定设计（Fig. 7 显示格式奖励在约 70 步达到峰值后优化重心转移），是否需要自适应调整以适应不同 LLM 底座或任务分布，仍是开放问题。

### 3. 局限与开放问题

尽管 HSI-GPT2 在定量指标和定性分析上均取得显著提升，以下问题值得后续研究关注：

1. **场景与交互的复杂性扩展**：当前框架仅在室内单人场景上验证，能否泛化到户外环境、多人协同交互、或更长时序的运动序列，需要新的数据引擎和评估基准支持。
2. **码本设计的任务敏感性**：DMoTok 的双粒度解耦是 FID 降低的关键（Table 6），但语义码本与细节码本的容量分配如何影响不同任务（文本到运动生成、运动描述、运动补全）的性能权衡，尚未给出定量指导。
3. **RL 训练的可扩展性**：GRPO 在 Qwen 和 Llama 上表现稳定，但扩展到更大规模模型（如 70B+）时的训练效率和奖励设计是否需要调整，缺乏实验证据。
4. **推理成本**：LLM–Diffusion 混合架构在推理时需同时运行 LLM 前向传播和扩散迭代去噪，相比纯 VQVAE 解码方案的计算开销和延迟未在论文中量化讨论，可能影响实时应用部署。

### 4. 知识库定位

HSI-GPT2 在人-场景交互领域确立了“LLM 语义规划 + 扩散物理合成”的混合范式，与现有工作形成以下定位关系：

- **相对于纯 LLM 方法**（如 MotionGPT 系列、MotionCLR）：HSI-GPT2 将运动解码从 LLM 的离散 token 预测中剥离，交给专门的扩散解码器，解决了 LLM 在连续运动细节建模上的能力瓶颈。
- **相对于纯扩散方法**（如 MDM、MLD）：HSI-GPT2 通过 LLM 引入语言推理和组合规划能力，使模型能够处理多步骤复杂指令（Fig. 5），而非仅从文本嵌入直接映射到运动。
- **相对于 HSI-GPT**：HSI-GPT2 是其直接升级，三处结构性改造（双粒度分词、扩散解码、GRPO 推理优化）共同构成了从“统一框架”到“推理增强框架”的代际跨越。

该范式为后续研究提供了可复用的技术路径：MoCoT 数据引擎可作为思维链监督数据的通用生成流水线，GRPO 的多奖励设计可推广到其他需要语义对齐与物理保真度平衡的生成任务。



## 原文 PDF

![[paperPDFs/CVPR_2026/HSI_GPT2_A_Dual_Granularity_Large_Motion_Reasoning_Model_with_Diffusion_Refinement_for_Human_Scene_Interaction.pdf]]
