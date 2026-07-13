---
title: "GaussianDWM: 3D Gaussian Driving World Model for Unified Scene Understanding and Multi-Modal Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GaussianDWM_3D_Gaussian_Driving_World_Model_for_Unified_Scene_Understanding_and_Multi_Modal_Generation.pdf
project_link: null
code_link: "https://github.com/dtc111111/GaussianDWM"
aliases:
- GaussianDWM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在3D高斯原语中直接嵌入语言特征实现早期模态对齐，并通过任务感知语言引导采样移除冗余高斯，将紧凑的3D空间token注入LLM，最终产生可引导多模态场景生成的高层世界知识。
primary_logic: 通过构建语言增强的3D高斯场景统一表征，并结合任务感知采样，使LLM能高效理解复杂驾驶场景并输出可条件化多模态生成的高层语义，从而统一场景理解与生成。
claims:
- GaussianDWM在NuInteract数据集上平均指标达到59.23，相对于先前最优方法DriveMonkey提升了13.6%。
- 在消融研究中，引入3D高斯表征和混合采样策略后，平均得分从无高斯模型的53.32显著提升至59.23，验证了其有效性。
- 双条件生成（高层语言+低层图像）在RGB-D新视角合成中优于仅使用低层条件，尤其在长时序预测中（FID从45.14降至44.5）。
- NuInteract 上 Avg. (RDP+2D VG+3D VG+Plan) = 59.23
---

# GaussianDWM: 3D Gaussian Driving World Model for Unified Scene Understanding and Multi-Modal Generation

> [!tip] 核心洞察
> 通过构建语言增强的3D高斯场景统一表征，并结合任务感知采样，使LLM能高效理解复杂驾驶场景并输出可条件化多模态生成的高层语义，从而统一场景理解与生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | GaussianDWM：面向统一场景理解与多模态生成的3D高斯驾驶世界模型 |
| 英文题名 | GaussianDWM: 3D Gaussian Driving World Model for Unified Scene Understanding and Multi-Modal Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.23180) · [Code](https://github.com/dtc111111/GaussianDWM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GaussianDWM |
| Dataset | NuInteract, NuScenes NVS |

> [!tip] 效果简介
> - NuInteract 上，Avg. (RDP+2D VG+3D VG+Plan) 59.23 vs DriveMonkey (52.12) (+7.11 (相对提升13.6%))；2D VG mAP 34.95 vs DriveMonkey (19.47) (+15.48)。
> - NuScenes NVS (Spatial, Shift ±1m) 上，FID 10.12 vs 最优重建基线 (具体数值未显式提供) (SOTA)。

## 概要

### 问题背景

当前驾驶世界模型（Driving World Models, DWM）面临一个根本瓶颈：现有方法普遍缺乏对3D场景的深层理解能力。基于点云或BEV（Bird’s-Eye-View）特征的空间表示难以实现文本信息与底层3D场景的精确对齐，导致语言引导的场景理解与多模态生成之间存在鸿沟。这一局限使得模型在需要精细空间推理的任务（如2D/3D视觉定位）中表现受限，同时也制约了从高层语义到低层视觉信号的生成一致性。

### 核心思路

GaussianDWM 提出以**语言增强的3D高斯场景表征**作为统一基座，将场景理解与多模态生成纳入同一框架。其核心因果机制包含三个关键环节：

1. **早期模态对齐**：直接在3D高斯原语中嵌入丰富的语言特征，构建“3D高斯语言场”，使文本语义与3D空间结构在表征层面即实现耦合，而非传统的后置特征对齐。
2. **任务感知语言引导采样**：设计混合采样策略（Top-k + 均匀采样 + 相似性采样），根据当前查询从冗余的3D高斯中筛选最相关的空间token注入大语言模型（LLM），在保留关键空间信息的同时克服token长度限制。
3. **双条件生成**：LLM不仅输出文本回答，同时提取封装了世界知识的高层语言特征 $C_L$，与低层图像/深度条件共同引导扩散模型，实现时空一致的场景生成。

这一设计使LLM能够高效理解复杂驾驶场景，并将高层语义知识可条件化地传递给生成模块，从而统一场景理解与生成。

### 主要结果

在 NuInteract 数据集上，GaussianDWM 的平均得分达到 **59.23**，相较于先前最优方法 DriveMonkey（52.12）**相对提升 13.6%**，在 2D 视觉定位（mAP 34.95 vs. 19.47）等子任务上优势尤为显著。消融实验证实，引入3D高斯表征与混合采样策略使平均得分从无高斯模型的 53.32 跃升至 59.23；双条件生成机制在长时序预测中相较仅使用低层条件显著降低 FID（45.14 → 44.5），移除高层世界知识则导致生成失败。在 nuScenes 空间新视角合成任务上，该方法亦达到 SOTA 水平（FID 10.12 @ ±1m 偏移）。

### 方法谱系与知识库定位

GaussianDWM 处于**3D场景理解、驾驶世界模型与多模态生成**的交叉点。在场景理解维度，其对比基线涵盖通用视觉-语言模型（**LLaVA1.5**, Liu et al., CVPR 2024; **MiniCPM-V 2**; **InternVL2-8B**）和驾驶专用世界模型（**DriveMonkey**, Zhao et al., arXiv 2025）；在3D感知维度，涉及 **BEVFormer**（Li et al., IEEE TPAMI 2024）、**PETR**（Liu et al., ECCV 2022）和 **CAPE**（Xiong et al., CVPR 2023）；在场景重建与生成维度，参照 **PVG**、**StreetGaussian**（Yan et al., ECCV 2024）及 **DiST-4D**（Guo et al., arXiv 2025）。该方法区别于现有工作的核心在于：以3D高斯原语为媒介实现语言与空间的早期融合，并通过任务感知采样将紧凑的3D token注入LLM，最终产生可引导多模态生成的高层世界知识——这一“表征-采样-生成”闭环在现有文献中尚属首次。



自动驾驶系统依赖对复杂驾驶场景的深度理解与未来状态预测来实现安全决策。现有驾驶世界模型（Driving World Models, DWMs）虽在场景理解或场景生成方面取得了显著进展，但二者长期处于割裂状态：理解模型难以支撑高质量的场景生成，生成模型则缺乏对场景语义的深层把握。

**核心瓶颈在于空间表征的局限性。** 当前主流方法普遍采用BEV（鸟瞰视图）特征或点云特征作为场景表示，这类表示存在两个结构性缺陷。其一，它们将文本信息与底层3D场景进行特征级对齐，缺乏在几何原语层面的早期模态绑定，导致语言描述与空间实体之间出现语义漂移。其二，当需要将3D空间信息注入大语言模型（LLM）时，冗余的空间token既超出了LLM的上下文窗口限制，又淹没了与当前任务最相关的场景线索——随机采样或简单降采样策略无法区分不同高斯原语对特定查询的信息贡献度。

上述瓶颈在生成侧同样突出。现有场景生成方法通常仅依赖低层图像条件（如参考帧RGB和深度），缺乏对场景高层语义的显式建模。当视点偏移增大或预测步长延长时，模型因缺少世界知识指导而难以维持时空一致性，生成质量急剧下降。

**GaussianDWM的动机正是弥合这一鸿沟。** 该工作提出首个基于3D高斯场景表征的统一世界模型框架，核心思路是：在3D高斯原语中直接嵌入语言特征，实现早期模态对齐；通过任务感知的语言引导采样策略，将紧凑且信息密集的3D空间token注入LLM；LLM在完成场景理解的同时，输出封装了世界知识的高层语言特征，作为多模态生成的条件信号。这一设计使得场景理解与生成共享同一套3D高斯表征，高层语义从理解端自然流向生成端，从而在统一框架内同时提升两项任务的表现。



## 核心方法与创新机理

GaussianDWM 的核心创新在于将 **3D 高斯原语** 从单纯的视觉重建载体升级为 **语言增强的统一场景表征**，并围绕这一表征构建了从感知到生成的完整闭环。相对于现有的驾驶世界模型，该方法在四个关键维度上实现了系统性改变：

**1. 场景表征：从 BEV/点云特征到 3D 高斯语言场**

现有方法（如 **DriveMonkey**（Zhao et al., arXiv 2025）、**BEVFormer**（Li et al., IEEE TPAMI 2024））依赖 BEV 或点云特征作为 LLM 的输入，这类扁平化的空间表示难以准确对齐文本信息与底层 3D 场景。GaussianDWM 直接在 3D 高斯原语中嵌入 CLIP 语言特征，并通过场景级语言自编码器压缩维度以降低内存开销。这使得每个高斯椭球体同时携带几何、纹理和语义信息，形成“语言增强的 3D 高斯场景表征”，实现了早期模态对齐（Sec. 3.1）。

**2. 语言对齐方式：从特征级对齐到早期嵌入**

传统方法通常在特征提取后通过投影层进行跨模态对齐，语言与 3D 空间的耦合发生在较晚的阶段。GaussianDWM 将语言特征直接渲染到像素空间——通过 alpha 合成公式 $F(v) = \sum_{i \in \mathcal{N}} f_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)$ 计算每个像素位置的语言嵌入，再与 3D 高斯的位置编码 $\gamma(x_i)$ 融合。这种早期嵌入使得语言信息与 3D 几何结构在表征层面深度绑定，为后续 LLM 理解空间语义提供了更精确的输入。

**3. 3D 标记注入 LLM：从无/随机采样到任务感知语言引导采样**

3D 高斯数量庞大，直接注入 LLM 会导致 token 长度爆炸。GaussianDWM 提出了 **任务感知语言引导采样策略**，包含三个互补机制：① 根据文本查询与 3D 高斯的相似度选择 top-k 相关高斯；② 均匀采样保留全局空间覆盖；③ 相似性采样仅应用于需要聚焦关注的任务（如 2D/3D 视觉定位）。消融实验证实，该混合策略将平均得分从无高斯模型的 53.32 显著提升至 59.23（Tab. 2），验证了其在高斯冗余去除与空间信息保留之间的有效平衡。

**4. 生成条件：从单条件到双条件（高层语言 + 低层图像/深度）**

现有生成方法通常仅依赖低层图像条件或无条件生成。GaussianDWM 利用 LLM 输出的高层语言特征 $C_L$ 作为世界知识，与低层图像/深度条件 $C_I, C_D$ 共同注入扩散 UNet，形成双条件生成机制。消融实验表明，在长时序预测中移除高层世界知识会导致生成失败（Tab. 4 中以“–”标注），而双条件设置将 FID 从 45.14 降至 44.5，证实了高层语义对时空一致性的关键作用。

**因果机制总结**：GaussianDWM 的核心因果链路可概括为——通过语言增强的 3D 高斯表征实现早期模态对齐 → 任务感知采样将紧凑的 3D 空间 token 注入 LLM → LLM 输出文本回答与高层语言特征 → 高层特征作为世界知识条件化多模态生成模型。这一闭环使得场景理解与生成在统一的 3D 高斯框架内相互增强，而非彼此独立。



GaussianDWM 构建了首个以 **3D 高斯原语为统一场景表征** 的驾驶世界模型框架，同时支撑场景理解与多模态场景生成。整个流水线由五个核心模块串联构成，形成“编码—投影—采样—理解—生成”的闭环。

### 流水线总览

框架的输入为多视图图像与对应的文本查询，输出包括文本回答、高层语言特征以及未来帧的 RGB-D 序列。其模块关系与数据流如 Figure 2 所示，核心路径如下：

![[assets/figures/papers/paper_list_l2495_https_arxiv_org_abs_2512_23180/figures/002_Figure_2.jpg]]
*Figure 2: System Overview. We propose the first unified 3D Gaussian-based world model framework that simultaneously supports both scene understanding and scene generation. We first employ a scene encoder to align the language information with the 3D Gaussians, resulting in language-augmented 3D Gaussian representations. Then, a designed Gaussian projector aligns the 3D Gaussian tokens, 2D image tokens, and text tokens into a unified latent space. Subsequently, a task-aware hybrid sampling strategy is applied to select the most relevant 3D Gaussian tokens for the current query, which are then fed into the LLM. The LLM produces both textual answers and high-level language features that encapsulate worl...*

1. **World Tokenizer（场景编码器 + 语言自编码器）**  
   首先，将 CLIP 语言特征直接嵌入每个 3D 高斯原语，实现语言信息与 3D 几何的早期模态对齐。随后通过一个场景级语言自编码器对渲染后的语言嵌入进行压缩，降低内存开销，得到语言增强的 3D 高斯表征。

2. **3D Gaussian Projector（高斯投影器）**  
   对每个 3D 高斯原语，拼接其位置傅里叶编码、尺度、旋转四元数、不透明度、球谐系数以及压缩后的语言特征，经可学习投影映射到统一特征空间，生成一组 **3D 高斯场景 token**，与 2D 图像 token、文本 token 处于同一潜在空间。

3. **Task-aware Language-guided Sampling（任务感知语言引导采样）**  
   为克服 3D 高斯 token 的冗余性并适配 LLM 的上下文窗口限制，该模块根据当前文本查询与各高斯 token 的相似度，执行混合采样策略：选取 top-k 最相关高斯，辅以均匀采样保留全局空间信息。对于需要聚焦关注的 2D/3D 视觉定位任务，额外引入相似度偏置以进一步提升定位精度。

4. **LLM（Qwen3-8B）**  
   采样后的紧凑高斯 token 与文本指令一同注入 LLM。LLM 以自回归方式生成文本回答，同时输出最后一层隐藏状态作为 **高层语言特征** $C_L$，该特征封装了对场景的语义理解与世界知识。

5. **Multi-modal Generation（去噪 UNet + 冻结 VAE）**  
   生成模块采用双条件机制：低层条件（当前帧 RGB 图像 $C_I$ 与深度图 $C_D$）提供像素级空间约束，高层语言特征 $C_L$ 注入语义与时空演化先验。VAE 将 RGB 与深度编码至统一潜在空间后，UNet 在扩散过程中同时接收两类条件，生成未来帧的 RGB 与深度序列。训练使用 v-预测损失（Eq. 5）。

### 训练策略

训练分三阶段进行：
- **第一阶段**：独立训练 3D 高斯 tokenizer、投影器及采样策略，随后与 LLM 联合微调；
- **第二阶段**：训练多模态生成模块（UNet + VAE）；
- **第三阶段**：端到端联合优化全部组件。

计算资源为 16×A100 GPU，场景理解实验设置严格遵循 DriveMonkey，生成实验遵循 DiST-4D 设定。

### 设计动机与关键创新

现有驾驶世界模型普遍依赖 BEV 或点云特征，缺乏对 3D 空间结构的显式建模，且文本信息与底层场景的对齐发生在特征级，导致 LLM 难以准确理解空间关系。GaussianDWM 的核心创新在于：
- **表征层面**：以 3D 高斯原语替代 BEV/点云，直接在原语中嵌入语言特征，实现早期模态对齐；
- **采样层面**：任务感知的语言引导采样取代随机或无采样策略，使 LLM 能高效聚焦于查询相关的空间区域；
- **生成层面**：引入高层世界知识作为生成条件，使生成模型不仅依赖低层像素信息，还能遵循场景语义与时空演化规律。

这一设计使框架能够将场景理解中提取的高层世界知识直接转化为生成模型的引导信号，从而统一了理解与生成两个任务。



GaussianDWM 的核心架构由三个紧密耦合的模块构成：**World Tokenizer（世界分词器）**、**任务感知语言引导采样**、以及**多模态生成模块**。其设计瓶颈在于：传统驾驶世界模型缺乏 3D 场景理解能力，且基于 BEV 或点云的特征表示无法将文本信息与底层 3D 场景精确对齐。GaussianDWM 通过在 3D 高斯原语中直接嵌入语言特征，实现了早期模态对齐，并将紧凑的 3D 空间 token 注入 LLM，最终产生可引导多模态场景生成的高层世界知识。

### World Tokenizer：语言增强的 3D 高斯表征

World Tokenizer 负责将原始多视图图像与文本信息编码为语言增强的 3D 高斯场景表征。其核心操作分为三步：

1.  **语言嵌入渲染**：对于每个 3D 高斯原语，除了常规的几何与外观属性外，额外嵌入一个语言特征向量。在任意像素位置 $v$，通过 alpha 合成渲染得到该位置的语言嵌入：

    
$$
F(v) = \sum_{i \in \mathcal{N}} f_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)
$$

    其中 $f_i$ 是第 $i$ 个高斯的语言特征，$\alpha_i$ 是其透明度，$\mathcal{N}$ 是沿光线排序的高斯集合。这一公式将 3D 高斯 splatting 的渲染机制直接迁移到语言特征域，使得 2D 图像空间中的每个像素都携带了来自 3D 场景的语义信息。

2.  **场景级语言自编码器压缩**：直接使用高维 CLIP 嵌入会带来巨大的显存开销。为解决此问题，引入一个场景级语言自编码器 $E$，将渲染后的高维语言嵌入 $F(v) \in \mathbb{R}^D$ 压缩为低维隐向量 $H(v) = E(F(v)) \in \mathbb{R}^d$，其中 $d \ll D$。这一压缩步骤是后续将 3D 高斯 token 注入 LLM 的关键效率保证。

3.  **3D 高斯投影器**：为让 LLM 理解 3D 空间结构，需要对每个高斯原语的 3D 坐标进行位置编码。采用傅里叶位置编码：

    
$$
\gamma(x_i) = \left[ \sin(2^k \pi x_i), \cos(2^k \pi x_i) \right]_{k=0}^{L-1}
$$

    其中 $x_i$ 是第 $i$ 个高斯的 3D 坐标，$L=10$。编码后的位置特征与压缩后的语言特征、外观特征拼接，通过一个可学习的投影器映射到 LLM 的 token 嵌入空间，形成最终的 3D 高斯场景 token $\mathcal{G}$。

### 任务感知语言引导采样

直接将所有 3D 高斯 token 输入 LLM 会超出上下文长度限制，且大量冗余高斯会引入噪声。GaussianDWM 设计了任务感知的混合采样策略：

-   **Top-k 采样**：根据用户文本查询 $\mathcal{T}$ 与每个高斯语言特征的相似度，选择最相关的 top-k 高斯。
-   **均匀采样**：为避免仅关注局部区域，同时从场景中均匀采样一部分高斯，保留全局空间上下文。
-   **相似性采样**：仅应用于需要聚焦关注的 2D/3D 视觉定位任务，进一步提升定位精度。

采样后的紧凑高斯 token 集合 $\mathcal{G}_i$ 与文本指令 $\mathcal{T}_i$ 一同送入 LLM（Qwen3-8B），LLM 自回归生成文本回答 $t_i$ 和高层语言特征 $C_i^l$：

$$
\{ t_i, C_i^l \} = LLM(\mathcal{G}_i, \mathcal{T}_i)
$$

训练采用前缀语言建模损失：

$$
\mathcal{L}(\theta, \mathcal{B}) = -\sum_{\{t_{\mathrm{prefix}}, t_{\mathrm{gt}}\} \in \mathcal{B}} \sum_{i=1}^{|t_{\mathrm{gt}}|} \log p_{\theta}\left(t_{\mathrm{gt}}^{(i)} \mid t_{\mathrm{gt}}^{(<i)}, t_{\mathrm{prefix}}\right)
$$

其中 $t_{\mathrm{prefix}}$ 是高斯 token 与用户指令拼接的前缀，$t_{\mathrm{gt}}$ 是目标回答续写。

### 多模态生成：双条件扩散模型

生成模块以 LLM 输出的高层语言特征 $C_L$ 和低层图像/深度特征 $C_I, C_D$ 为双条件，通过去噪 UNet 和冻结的预训练 VAE 生成 RGB 和深度序列。训练采用仿真自由的 rectified flow 与 v-预测损失：

$$
\mathcal{L} = \mathbb{E}_{d, \epsilon, t, s} \left\| \mathcal{F}_{\theta}(d_t, d_{\mathrm{ref}}, C_I, C_D, C_L, s) - \mathbf{v}_t \right\|_2^2
$$

其中 $d_t$ 是噪声化的潜变量，$d_{\mathrm{ref}}$ 是参考帧，$s$ 是时间步条件。高层世界知识 $C_L$ 的引入使得生成模型能够在长时序预测中保持时空一致性——消融实验表明，移除 $C_L$ 会导致生成失败（Tab. 4）。



## 实验与关键发现

### 场景理解主结果

GaussianDWM 在 NuInteract 数据集上进行了全面的场景理解评估，涵盖区域描述与感知（RDP）、2D 视觉定位（2D VG）、3D 视觉定位（3D VG）和规划（Planning）四个子任务。如 Table 1 所示，GaussianDWM 取得了 59.23 的平均得分，相较于先前最优的统一世界模型 **DriveMonkey**（Zhao et al., arXiv 2025）的 52.12，绝对提升 +7.11，**相对提升 13.6%**。这一显著提升的核心驱动力在于 3D 高斯场景表征的引入——它使得 LLM 能够直接获取与文本对齐的 3D 空间信息，而非依赖 BEV 或点云特征等间接表示。

![[assets/figures/papers/paper_list_l2495_https_arxiv_org_abs_2512_23180/figures/003_Table_1.jpg]]
*Table 1: The comparison between our GaussianDWM and other state-of-the-art models on the NuInteract dataset [77]. The scene understanding task includes four subtasks: region description and perception, 2D visual grounding, 3D visual grounding, and planning. Our method achieves state-of-the-art average performance across all four tasks, which fully demonstrates the effectiveness of introducing a 3D Gaussian scene representation for enhancing the LLM’s capability to understand 3D spatial information*

在细粒度任务上，GaussianDWM 的优势尤为突出。在 2D 视觉定位任务中，GaussianDWM 的 mAP 达到 34.95，远超 DriveMonkey 的 19.47（+15.48），表明语言增强的 3D 高斯原语能有效建立文本查询与图像区域之间的精确对应关系。相比之下，传统视觉-语言基线如 **LLaVA1.5**（Liu et al., CVPR 2024）、**MiniCPM-V 2** 和 **InternVL2-8B** 由于缺乏显式的 3D 空间建模，在需要空间推理的 3D VG 和规划任务上表现明显不足。

### 消融实验：3D 高斯表征与采样策略

Table 2 的消融实验系统性地验证了各组件的贡献。基线设置（无 3D 高斯模型，仅使用 2D 图像 token）的平均得分为 53.32。引入 3D 高斯场景表征后，即便采用随机采样策略，平均得分即跃升至 58.93，**验证了 3D 高斯语言场作为场景表征的核心价值**。进一步引入 Top-k + Uniform 混合采样策略后，得分提升至 59.09；再叠加任务感知的相似性采样（similarity-based sampling）后，达到最终的 59.23。

![[assets/figures/papers/paper_list_l2495_https_arxiv_org_abs_2512_23180/figures/004_Table_2.jpg]]
*Table 2: We conduct ablation studies to validate the effectiveness of each proposed component, including the 3D Gaussian scene representation, the top-k and uniform sampling strategies, and the similarity–based sampling module. Note that the similarity sampling strategy is applied only to grounding tasks requiring focused attention (e.g., 2DVG and 3DVG)*

值得注意的是，相似性采样模块被设计为仅应用于需要聚焦关注的任务（2D VG 和 3D VG），其贡献在定位指标上更为显著。这一设计揭示了任务感知采样策略的因果机制：通过文本查询与 3D 高斯语言特征的相似度计算，模型能够从冗余的高斯原语中筛选出与当前任务最相关的空间 token，从而在有限的 LLM 上下文窗口内最大化信息密度。

### 多模态生成：双条件机制的消融

Table 4 检验了双条件生成机制的有效性。生成模型以高层语言特征 $C_L$（来自 LLM 的世界知识）和低层图像/深度条件 $C_I, C_D$ 作为联合输入。在 RGB-D 新视角合成的长时序预测场景中，完整的双条件设置取得了最优的 FID 指标（44.5）。当移除高层世界知识条件时，FID 劣化至 45.14；若进一步移除低层条件，模型将完全无法生成有效输出（标记为“–”）。这表明 **LLM 提取的高层语义特征为生成模型提供了不可或缺的时序一致性和场景先验**，而低层条件则负责保持像素级的纹理和几何细节。

![[assets/figures/papers/paper_list_l2495_https_arxiv_org_abs_2512_23180/figures/009_Table_4.jpg]]
*Table 4: Ablation Study of dual-condition generation mechanism. “–” denotes failure under the setting*

### 新视角合成定性分析

Figure 4 展示了在 2m 大视角偏移下的 RGB-D 新视角合成定性比较。相较于基于重建的方法如 **PVG**、**StreetGaussian**（Yan et al., ECCV 2024）等，GaussianDWM 显著减少了动态物体的伪影，并在大视角变化下保持了时空一致性。这一优势源于生成范式对未见区域的合理推断能力，而非单纯依赖已有观测的外推。

![[assets/figures/papers/paper_list_l2495_https_arxiv_org_abs_2512_23180/figures/010_Figure_4.jpg]]
*Figure 4: Qualitative comparison of RGB-D NVS with 2m shift. Compared with state-of-the-art reconstruction-based methods for spatial NVS [4, 7, 68, 73], our method reduce artifacts of dynamic objects and preserves temporal-spatial consistency across large viewpoint shifts*

### 实验设置与公平性说明

场景理解实验严格遵循 DriveMonkey 的评估协议，生成实验遵循 **DiST-4D**（Guo et al., arXiv 2025）的设定。训练分三阶段进行：第一阶段独立训练 Gaussian tokenizer、projector 和采样策略并与 LLM 联合微调；第二阶段训练多模态生成模型，采用 simulation-free rectified flow 和 v-预测损失；第三阶段进行端到端联合优化。所有实验在 16×A100 GPU 上完成，确保了与基线方法的计算资源可比性。

### 补充图表

![[assets/figures/papers/paper_list_l2495_https_arxiv_org_abs_2512_23180/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative results for scene understanding and scene generation. From top to bottom, we display the multi-view input of the current scene and the 3D Gaussian ellipsoids, the scene understanding results, and the spatial and temporal scene generation results*



## 定位与知识库关联

### 1. 方法图谱与基线关系

GaussianDWM 的核心定位是**统一 3D 场景理解与多模态生成的驾驶世界模型**。其方法谱系可从场景表征、视觉-语言理解、场景生成三条线索追溯。

**场景表征的演进。** 传统驾驶世界模型依赖 BEV 特征（如 **BEVFormer**，Li et al., IEEE TPAMI 2024）或点云特征（如 **PETR**，Liu et al., ECCV 2022；**CAPE**，Xiong et al., CVPR 2023）作为场景表示。这类表示缺乏显式的 3D 结构，难以将文本语义精确锚定到空间位置。GaussianDWM 的关键跃迁在于引入 **3D 高斯语言场**——在 3D 高斯原语中直接嵌入 CLIP 语言特征，通过 alpha 合成渲染实现早期模态对齐（Eq. 1）。这一设计将场景表征从“特征级对齐”升级为“原语级对齐”，使每个高斯椭球同时携带几何、纹理和语义属性。

**视觉-语言理解的基线对比。** 在 NuInteract 数据集上，GaussianDWM 与三类基线展开竞争：通用视觉-语言模型（**LLaVA1.5**，Liu et al., CVPR 2024；**MiniCPM-V 2**；**InternVL2-8B**）和驾驶专用世界模型（**DriveMonkey**，Zhao et al., arXiv 2025）。GaussianDWM 在四项子任务（区域描述与感知 RDP、2D 视觉定位 2D VG、3D 视觉定位 3D VG、规划）的平均得分达到 59.23，相较先前最优方法 DriveMonkey（52.12）提升 13.6%（Tab. 1）。其中 2D VG 的 mAP 从 19.47 跃升至 34.95（+15.48），直接验证了 3D 高斯表征对空间定位能力的增益。消融实验进一步揭示因果链条：移除 3D 高斯表征后平均得分降至 53.32，仅引入随机采样提升有限（Tab. 2），证明**表征质量与采样策略共同构成性能瓶颈**。

**场景生成的双条件机制。** 在生成侧，GaussianDWM 与重建式方法（**PVG**；**StreetGaussian**，Yan et al., ECCV 2024）和生成式方法（**DiST-4D**，Guo et al., arXiv 2025）形成对比。其核心创新在于**双条件生成**：将 LLM 提取的高层语言特征 $C_L$ 与低层图像/深度条件 $C_I, C_D$ 共同注入扩散 UNet（Eq. 5）。消融实验表明，移除高层世界知识会导致长时序预测失败（Tab. 4 中以“–”标注），而双条件设置将 FID 从 45.14 降至 44.5，验证了高层语义对时空一致性的因果作用。

### 2. 适用边界与局限

**适用边界。** GaussianDWM 的设计假设场景可由一组静态 3D 高斯原语充分表征，并通过语言特征嵌入实现语义对齐。这一假设在 nuScenes 和 NuInteract 等结构化驾驶场景中成立，但存在以下边界：

- **动态对象建模。** 当前框架将场景编码为单帧 3D 高斯，未显式建模物体运动轨迹。定性结果（Figure 4）显示其在动态物体区域减少了伪影，但方法本身未引入运动场或时序高斯变形，动态一致性依赖于扩散模型的条件生成能力。
- **语言特征压缩的信息损失。** 为降低内存消耗，方法引入场景级语言自编码器 $E$，将 CLIP 嵌入从 $D$ 维压缩至 $d$ 维（$d \ll D$）。压缩率与语义保真度之间的权衡关系未在消融中量化，可能影响细粒度语义定位任务的上限。
- **采样策略的任务依赖性。** 相似性采样仅对需要聚焦关注的定位任务（2D VG、3D VG）有效（Tab. 2 说明），在全局描述任务中可能引入偏差。这要求实际部署时根据任务类型切换采样策略，增加了系统复杂度。

**已知局限与开放问题。** 论文未显式声明局限性，但以下问题值得关注：

1. **长尾场景的泛化能力。** 实验仅在 nuScenes 和 NuInteract 上进行，这两个数据集以城市结构化道路为主。在极端天气、非结构化道路或罕见交互场景下的性能需要手动验证。
2. **计算资源需求。** 三阶段训练需 16×A100 GPU，限制了方法在资源受限场景下的可复现性。
3. **生成与理解的耦合深度。** 当前框架中，理解与生成通过高层语言特征 $C_L$ 单向连接。是否可以通过生成结果的反馈进一步优化理解（形成闭环）仍是一个开放问题。
4. **多帧时序一致性。** 长时序生成虽优于单条件基线，但 FID 的绝对改善幅度有限（-0.64），暗示高层世界知识的时序建模能力仍有提升空间。

### 3. 在知识库中的位置

GaussianDWM 在驾驶世界模型的知识谱系中占据**表征-理解-生成统一框架**的关键节点：

- **相对于理解侧工作**（LLaVA1.5、DriveMonkey），它首次将 3D 高斯语言场作为 LLM 的空间感知接口，将“看到什么”升级为“空间中有什么”。
- **相对于生成侧工作**（PVG、StreetGaussian、DiST-4D），它将 LLM 提取的世界知识作为生成条件，实现了从“重建/预测外观”到“理解后生成”的范式转变。
- **相对于 3D 高斯表征工作**（3D Gaussian Splatting 系列），它拓展了高斯的语义维度，使其从纯视觉基元进化为多模态基元。

该框架的后续工作可能沿三个方向展开：(1) 引入可学习的时序高斯变形，统一处理动态与静态场景；(2) 探索理解-生成的闭环优化，使生成结果反哺场景理解；(3) 降低计算门槛，推动 3D 高斯世界模型的实际部署。



## 原文 PDF

![[paperPDFs/CVPR_2026/GaussianDWM_3D_Gaussian_Driving_World_Model_for_Unified_Scene_Understanding_and_Multi_Modal_Generation.pdf]]
