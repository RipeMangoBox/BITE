---
title: "DreamMotion: Space-Time Self-Similarity Score Distillation for Zero-Shot Video Editing"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/DreamMotion_Space_Time_Self_Similarity_Score_Distillation_for_Zero_Shot_Video_Editing.pdf
project_link: https://hyeonho99.github.io/dreammotion
code_link: null
aliases:
- DreamMotion
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "使用分数蒸馏采样（SDS/DDS）代替祖先采样进行编辑优化，同时引入时空自相似性匹配（空间自相似性保持结构、时间自相似性平滑时序）以控制结构-运动偏差。"
primary_logic: "通过视频差分去噪分数（V-DDS）从预训练T2V模型中蒸馏外观梯度，并利用扩散U-Net中间特征的自相似性作为监督信号对准原始视频与编辑视频的空间结构和时间连贯性，从而实现零样本视频编辑中的外观注入与运动保持的平衡。"
claims:
- "DreamMotion using Score Distillation Sampling avoids the standard reverse diffusion process that struggles with motion preservation."
- "Spatial self-similarity alignment preserves structure and motion integrity while modifying appearance."
- "Temporal self-similarity alignment facilitates effective temporal smoothing, preventing distortions."
- "Joint optimization of V-DDS, S-SSM, and T-SSM generates optimal output videos as shown by ablation."
---

# DreamMotion: Space-Time Self-Similarity Score Distillation for Zero-Shot Video Editing

> [!tip] 核心洞察
> 通过视频差分去噪分数（V-DDS）从预训练T2V模型中蒸馏外观梯度，并利用扩散U-Net中间特征的自相似性作为监督信号对准原始视频与编辑视频的空间结构和时间连贯性，从而实现零样本视频编辑中的外观注入与运动保持的平衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DreamMotion：零样本视频编辑的时空自相似性分数蒸馏 |
| 英文题名 | DreamMotion: Space-Time Self-Similarity Score Distillation for Zero-Shot Video Editing |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.12002) · [Project](https://hyeonho99.github.io/dreammotion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DreamMotion |
| Dataset | Custom video editing dataset (Zeroscope) |

> [!tip] 效果简介
> - Custom video editing dataset (Zeroscope) 上，CLIP Text-Alignment (Text-Align) 为 0.8209。
> - Custom video editing dataset (Zeroscope) 上，Frame Consistency (CLIP-based, Frame-Con) 为 0.9726。
> - Custom video editing dataset (Zeroscope) 上，Motion Fidelity (Tracking-based) 为 0.9259。

## 概要

**问题瓶颈**：基于祖先采样的逆扩散过程难以在视频编辑中重现真实世界运动。公开的文本到视频（T2V）扩散模型缺乏足够丰富的时间先验，且逆扩散从噪声出发无法编程复杂运动，导致编辑后的视频出现运动不连贯与结构失真。

**核心方法**：DreamMotion 摒弃标准去噪流程，转而采用分数蒸馏采样（SDS）驱动的优化范式。其核心调控手段是引入时空自相似性匹配——空间自相似性保持结构、时间自相似性平滑时序——以控制结构-运动偏差。具体而言，通过视频差分去噪分数（V-DDS）从预训练 T2V 模型中蒸馏外观梯度，并利用扩散 U-Net 中间特征的自相似性作为监督信号，对齐原始视频与编辑视频的空间结构和时间连贯性，实现零样本视频编辑中外貌注入与运动保持的平衡。

**方法定位**：DreamMotion 属于零样本视频编辑框架，与 **Tune-A-Video**（Wu et al., ICCV 2023）、**ControlVideo**（Zhang et al., arXiv 2023）、**TokenFlow**（Geyer et al., arXiv 2023）、**Gen-1**（Esser et al., arXiv 2023）等基于祖先采样的方法形成根本性差异。其优化策略由三个损失项联合构成：V-DDS（注入目标外观）、S-SSM（空间自相似性匹配保持结构）、T-SSM（时间自相似性匹配实现时序平滑），并辅以掩码梯度过滤避免模糊和过饱和。

**主要结果**：在 Zeroscope 模型上，DreamMotion 取得 CLIP 文本对齐度 0.8209、帧一致性 0.9726、运动保真度 0.9259；在 Show-1 级联模型上同样表现优异。用户研究中，编辑准确度评分 4.14/5，结构与运动保持评分 4.33/5。消融实验证实，联合优化 V-DDS、S-SSM 和 T-SSM 三个损失项产生最优输出。

**局限性**：DreamMotion 强依赖原始视频的结构和运动，在需要大幅度结构变化的编辑任务上能力有限，无法执行显著的几何变形或对象替换。



### 视频编辑的范式瓶颈：从祖先采样到分数蒸馏

文本到视频（T2V）扩散模型的快速发展催生了一系列零样本视频编辑方法，其核心思路是将图像编辑技术迁移到视频域。主流方案——包括 **Tune-A-Video**（Wu et al., ICCV 2023）、**ControlVideo**（Zhang et al., arXiv 2023）、**TokenFlow**（Geyer et al., arXiv 2023）等——普遍采用基于祖先采样的逆向扩散流程：先通过DDIM反演将原始视频映射到噪声空间，再在去噪过程中注入目标文本条件，从而在保留原始结构的同时修改外观。

然而，这一范式存在一个根本性的瓶颈：**公开可用的T2V扩散模型缺乏足够丰富的时间先验，难以在逆向扩散过程中重现真实世界的复杂运动**。如图2所示，当编辑对象涉及大幅度位移、旋转或遮挡等复杂运动时，基于祖先采样的方法会产生运动不连贯、结构失真等严重问题。其因果机制在于：逆向扩散从纯噪声出发，本质上是一个“从无到有”的生成过程，而非“在已有运动基础上修改外观”的编辑过程；预训练T2V模型的时间注意力层虽然能捕捉帧间关系，但其时间先验的丰富程度远不足以精确编程复杂运动轨迹。

### 分数蒸馏采样的机遇与挑战

分数蒸馏采样（Score Distillation Sampling, SDS）为上述问题提供了新的解决思路。与祖先采样不同，SDS通过优化可微分参数（如图像或视频的像素值）来对齐预训练扩散模型的分数函数，从而绕过了从噪声逐步生成的逆向过程。在视频编辑场景中，这意味着**编辑过程可以直接在原始视频的像素空间上进行优化，而非在噪声空间中重建**，从根本上规避了运动信息丢失的风险。

但直接将SDS应用于视频编辑面临两个关键挑战：

1. **外观注入的精度控制**：SDS梯度倾向于产生过饱和和模糊的视觉效果，在视频编辑中这一问题更为突出，因为帧间不一致的梯度更新会放大伪影。
2. **结构-运动的保持**：SDS本身不具备结构保持机制，优化过程中视频的空间结构和时间连贯性会逐渐偏离原始视频，造成运动变形和时序闪烁。

### 核心动机：时空自相似性作为结构-运动锚点

DreamMotion的核心洞察在于：**扩散U-Net中间层特征的自相似性天然编码了视频的空间结构和时间连贯性信息**。具体而言：

- **空间自相似性**：同一帧内不同空间位置的特征之间的余弦相似度反映了该帧的结构布局（如物体边界、部件关系等），这一信息在扩散模型的不同时间步和不同噪声水平下具有高度稳定性。
- **时间自相似性**：不同帧在空间池化后的特征向量之间的相似度刻画了视频的时序演进模式，是运动信息在特征空间中的紧凑表示。

通过在SDS优化过程中强制编辑视频与原始视频的扩散特征保持空间和时间自相似性一致，DreamMotion实现了**外观注入与运动保持的精细平衡**——外观由V-DDS（Video Delta Denoising Score）梯度驱动注入，而结构和运动则由自相似性匹配损失约束在原始视频的流形上。图3的优化过程可视化直观展示了这一机制的效果：仅使用V-DDS会导致结构逐渐漂移，而加入时空自相似性正则化后，编辑视频在获得目标外观的同时稳定保持了原始运动轨迹。



## 核心方法与创新机理

DreamMotion 的核心创新在于**从根本上绕开了传统零样本视频编辑对祖先采样（ancestral sampling）的依赖**，转而构建了一套以分数蒸馏采样（SDS）为骨架、以时空自相似性为约束的优化范式。这一范式通过三个紧密耦合的 changed slots 实现外观注入与运动保持的平衡。

### 从祖先采样到分数蒸馏的范式转换

传统零样本视频编辑方法（如 Tune-A-Video、ControlVideo、TokenFlow 等）普遍依赖 DDIM 反演-去噪的祖先采样管线。该管线的瓶颈在于：公开可用的文本到视频（T2V）扩散模型缺乏足够丰富的时间先验，且逆扩散过程从纯噪声出发难以编程复杂运动，导致编辑视频出现运动不连贯和结构失真（Fig. 2）。DreamMotion **彻底弃用祖先采样**，转而采用基于优化的分数蒸馏策略——通过视频差分去噪分数损失（V-DDS）从预训练 T2V 模型中蒸馏外观梯度，将编辑任务转化为对视频像素变量的直接优化问题。这一转换的因果效应在于：优化过程始终锚定原始视频作为初始解，避免了从噪声重建带来的运动漂移。

### 时空自相似性作为结构-运动约束

仅靠 V-DDS 注入外观会导致结构偏差和时序闪烁。DreamMotion 的核心洞察是：**扩散 U-Net 中间特征的自相似性可以作为无监督的结构与运动监督信号**。具体而言：

- **空间自相似性匹配（S-SSM）**：在每一帧内部，计算 U-Net 关键特征的余弦相似度矩阵，强制编辑视频与原始视频的空间自相似性图对齐（$\mathcal{L}_{\mathrm{S-SSM}}$）。这等价于保持场景的语义结构布局，使外观修改不会破坏物体边界和空间关系。
- **时间自相似性匹配（T-SSM）**：沿时间轴，先通过空间边缘均值（spatial marginal mean）将每帧特征压缩为全局描述子，再计算帧间余弦相似度矩阵，强制编辑视频与原始视频的时间自相似性图对齐（$\mathcal{L}_{\mathrm{T-SSM}}$）。这在不引入额外时序模块的前提下实现了有效的时间平滑，抑制了优化过程中的闪烁伪影。

消融实验（Table 3）定量验证了这一约束的因果作用：同时移除 S-SSM 和 T-SSM 后，运动保真度从 0.9259 骤降至 0.8426，帧间扭曲误差从 0.3042 升至 0.3247。仅移除 T-SSM 也会导致帧一致性显著下降（0.9011 vs. 0.9259），证实了时间自相似性对齐的独立贡献。

### 掩码梯度过滤的保真度增强

在 V-DDS 优化过程中，DreamMotion 引入了**边界框驱动的二值掩码**来选择性过滤梯度更新。这一设计的动机在于：无约束的分数蒸馏梯度会扩散到背景区域，造成模糊和过饱和。掩码梯度过滤（Fig. 6, Fig. 13）将编辑操作限制在目标区域，是维持视觉保真度的关键工程组件。消融表明，移除掩码条件后，运动保真度从 0.9259 降至 0.8653，扭曲误差从 0.3042 升至 0.3416。

### 级联模型的轻量适配

对于级联视频扩散模型（如 Show-1），DreamMotion 将优化**仅作用于关键帧生成阶段**，而非整个级联管线。这一策略在保持编辑质量的同时大幅降低了计算开销，使方法可无缝嵌入现有级联框架。



![[assets/figures/papers/paper_list_l32_DreamMotion_Space_Time_Self_Similarity_Score_Distillation_for_Zero_Shot/figures/001_Figure_1.jpg]]
*Figure 1: Zero-shot video editing results. The second row presents videos produced with our method with a non-cascaded video diffusion model, while those in the bottom row are from a cascaded model. For a full display of results, visit our project page*

DreamMotion 的优化框架以**视频差分去噪分数蒸馏（V‑DDS）**为核心外观注入引擎，并通过**空间‑时间自相似性对齐**构成双正则化支路，共同作用于一个从原始视频初始化的可优化视频变量。

### 输入与初始化

编辑过程从一段原始视频 $\hat{\pmb{x}}^{1:N}$ 和描述目标外观的文本提示 $y$ 出发。DreamMotion 直接将目标视频变量 $\pmb{x}_0^{1:N}(\theta)$ 初始化为原始视频，而非从随机噪声开始采样。这一设计从根本上绕开了传统祖先采样（DDIM 反演与去噪）对预训练文本到视频扩散模型中时间先验的依赖——后者正是导致复杂真实运动无法被准确重现的核心瓶颈（Fig. 2）。

### 三支路优化结构

整个框架的优化策略由三个并行的损失支路构成（Fig. 4），三者共享同一组噪声 $\epsilon$ 和时间步 $t$，以降低计算开销：

1. **V‑DDS 外观注入支路**：将目标视频变量与原始视频分别输入预训练的 T2V 扩散模型 $\epsilon_\phi$，通过差分去噪分数 $\mathcal{L}_{\mathrm{V-DDS}}$ 蒸馏目标提示 $y$ 与原始提示 $\hat{y}$ 之间的外观梯度，驱动视频内容向目标描述演化。

2. **空间自相似性匹配（S‑SSM）支路**：从扩散 U‑Net 中间层提取 Key 特征，逐帧计算空间自相似性图 $SS^n$，并以 L2 距离对齐编辑视频与原始视频的相似性结构，从而在优化过程中保持物体的空间布局与运动轮廓。

3. **时间自相似性匹配（T‑SSM）支路**：对 Key 特征沿空间维度取均值得到全局描述子，沿帧轴构建时间自相似性矩阵 $\pmb{T}S$，通过 $\mathcal{L}_{\mathrm{T-SSM}}$ 对齐编辑前后的时序相关性，抑制因逐帧独立优化引入的闪烁与抖动。

### 梯度掩码过滤

在 V‑DDS 梯度回传阶段，DreamMotion 引入由现成检测模型生成的边界框二值掩码，对梯度进行选择性过滤（Fig. 6）。该操作仅允许目标区域的梯度更新，避免非编辑区域出现模糊和过饱和，从而在保持视觉保真度的同时约束外观注入范围。

### 级联模型适配

对于 Show‑1 等级联视频扩散框架（由关键帧生成、时序插值、空间超分辨率三阶段组成），DreamMotion 将上述优化过程**仅应用于关键帧生成阶段**。这一策略在保持编辑质量的同时大幅降低了计算成本，后续的插值与超分模块沿用原始管线即可完成全分辨率视频合成。



DreamMotion 的核心由三个损失函数和一个梯度过滤策略构成，它们共享同一组噪声 $\epsilon$ 和时间步 $t$，在单次前向传播中完成计算，从而实现高效联合优化。

### 视频差分去噪分数蒸馏（V-DDS）

传统零样本视频编辑依赖于祖先采样（DDIM 反演 + 去噪），但公开的文本到视频（T2V）扩散模型缺乏足够丰富的时间先验，导致生成的视频运动不连贯。DreamMotion 改用分数蒸馏采样（SDS）框架来优化编辑视频，其基础形式为：

$$\mathcal{L}_{\mathrm{SDS}}(\theta; y) = \left\| \epsilon_{\phi}^{w}(\mathbf{x}_{t}(\theta), t, y) - \epsilon \right\|_{2}^{2}$$

其中 $\epsilon_{\phi}^{w}$ 是预训练扩散模型的 Classifier-Free Guidance 去噪输出，$\mathbf{x}_{t}(\theta)$ 是经噪声注入后的可优化视频变量。

为注入目标外观而非从头生成，DreamMotion 引入差分去噪分数（DDS），通过参考分支减去原始视频的噪声方向：

$$\mathcal{L}_{\mathrm{DDS}}(\theta; y) = \left\| \epsilon_{\phi}^{w}(\mathbf{x}_{t}(\theta), t, y) - \epsilon_{\phi}^{w}(\hat{\mathbf{x}}_{t}, t, \hat{y}) \right\|_{2}^{2}$$

将其扩展至视频域，得到 **V-DDS 损失**：

$$\mathcal{L}_{\mathrm{V-DDS}}(\theta; y) = \left\| \epsilon_{\phi}^{w}(\mathbf{x}_{t}^{1:N}(\theta), t, y) - \epsilon_{\phi}^{w}(\hat{\mathbf{x}}_{t}^{1:N}, t, \hat{y}) \right\|_{2}^{2}$$

其中 $\hat{\mathbf{x}}^{1:N}$ 为原始视频，$\hat{y}$ 为原始视频的文本描述，$y$ 为目标编辑文本。V-DDS 的梯度方向引导目标视频向新外观靠拢，同时以原始视频的分数作为基线，避免过度偏离。

### 空间自相似性匹配（S-SSM）

仅靠 V-DDS 注入外观会导致结构变形和运动偏移。DreamMotion 利用扩散 U-Net 中间层 Key 特征的自相似性，强制目标视频与原始视频在空间结构上对齐。

对于第 $n$ 帧，空间自相似性图定义为 Key 特征 $K_i^n$ 的余弦相似度矩阵：

$$SS_{i,j}^n(\mathbf{x}_{t}^{1:N}) = \cos(K_i^n(\mathbf{x}_{t}^{1:N}), K_j^n(\mathbf{x}_{t}^{1:N}))$$

**S-SSM 损失** 对每一帧对齐两个视频的自相似性图：

$$\mathcal{L}_{\mathrm{S-SSM}}(\mathbf{x}_{t}^{1:N}, \hat{\mathbf{x}}_{t}^{1:N}) = \frac{1}{N} \sum_{n=1}^{N} \left\| SS^n(\mathbf{x}_{t}^{1:N}) - SS^n(\hat{\mathbf{x}}_{t}^{1:N}) \right\|_{2}^{2}$$

该损失的因果机制在于：自相似性图编码了帧内各区域之间的相对关系，对齐该关系等价于保持物体的几何结构和空间布局，而不直接约束像素值，从而在注入外观的同时保留结构完整性。

### 时间自相似性匹配（T-SSM）

空间对齐逐帧独立进行，缺乏跨帧约束，容易引入时序闪烁。DreamMotion 引入时间自相似性匹配，将空间特征压缩为全局描述子后沿时间轴构建自相似性矩阵。

首先对每帧的 Key 特征进行空间边缘均值池化：

$$M[K(\mathbf{x}_{t}^{1:N})] = \frac{1}{H \cdot W} \sum_{i=1}^{H \cdot W} K_i(\mathbf{x}_{t}^{1:N})$$

得到 $N$ 帧的全局描述子后，构建时间自相似性矩阵 $TS(\mathbf{x}_{t}^{1:N})$，其元素为帧间全局描述子的余弦相似度。**T-SSM 损失** 对齐两个视频的时间自相似性矩阵：

$$\mathcal{L}_{\mathrm{T-SSM}}(\mathbf{x}_{t}^{1:N}, \hat{\mathbf{x}}_{t}^{1:N}) = \left\| TS(\mathbf{x}_{t}^{1:N}) - TS(\hat{\mathbf{x}}_{t}^{1:N}) \right\|_{2}^{2}$$

该损失通过保持帧间相对关系的稳定性来平滑时序，防止优化过程中的局部失真扩散为全局闪烁。

### 掩码梯度过滤

V-DDS 的梯度在非编辑区域可能引入模糊和过饱和。DreamMotion 利用现成的检测模型获取目标边界框，生成二值掩码，在反向传播时仅保留编辑区域的 V-DDS 梯度，非编辑区域梯度归零。消融实验（Table 3）表明，去除掩码过滤后，Motion-Fidelity 从 0.9259 降至 0.8653，Frame-LPIPS 从 0.3042 恶化至 0.3416，验证了该模块对视觉保真度的关键作用。

### 级联模型适配

对于 Show-1 等级联视频扩散模型（Keyframe Generation → Temporal Interpolation → Spatial Super Resolution），DreamMotion 仅对 Keyframe Generation 阶段施加优化，大幅降低计算开销，后续模块保持不变以继承时间插值和超分能力。



## 实验与关键发现

### 核心瓶颈与验证逻辑

DreamMotion 的实验设计围绕一个核心瓶颈展开：传统基于祖先采样（DDIM 反演+去噪）的零样本视频编辑方法，由于公开文本到视频（T2V）扩散模型缺乏足够丰富的时间先验，且逆扩散过程从噪声出发难以编程复杂运动，导致编辑后视频的运动不连贯和结构失真。实验通过以下因果链条验证所提方法：

1. **用分数蒸馏采样（V-DDS）替代祖先采样**，从预训练 T2V 模型中蒸馏外观梯度，避免逆扩散过程的运动破坏。
2. **引入空间自相似性匹配（S-SSM）**，在扩散 U-Net 中间特征层对齐原始视频与编辑视频的空间结构，抑制结构偏差。
3. **引入时间自相似性匹配（T-SSM）**，通过空间边缘均值压缩后沿帧轴对齐时间相关性，消除闪烁和时序畸变。
4. **掩码梯度过滤**，利用边界框生成的二值掩码选择性过滤 V-DDS 梯度，防止非编辑区域的模糊和过饱和。

实验在两种 T2V 主干模型（非级联的 Zeroscope 和级联的 Show-1）上验证，并通过自动化指标、人类评估、消融实验和局部编辑对比，逐层证明各组件的因果贡献。

### 主实验结果

#### 非级联模型（Zeroscope）上的性能

Table 1 展示了 DreamMotion 在 Zeroscope 上与五个基线方法的定量对比。DreamMotion 在所有七项指标上均取得最优：

![[assets/figures/papers/paper_list_l32_DreamMotion_Space_Time_Self_Similarity_Score_Distillation_for_Zero_Shot/figures/008_Table_1.jpg]]
*Table 1: Quantitative evaluations. DreamMotion with Zeroscope outperforms various video editing methods in all seven features*

- **文本对齐度（Text-Align）**：0.8209，表明分数蒸馏优化有效将目标文本描述的外观注入视频。
- **帧一致性（Frame-Con）**：0.9726，说明 S-SSM 和 T-SSM 联合正则化成功保持了时序平滑。
- **运动保真度（Motion-Fidelity）**：0.9259，基于跟踪的运动评估证实空间自相似性对齐保留了原始视频的运动轨迹。
- **帧级 LPIPS**：0.3042，反映编辑后视频与原始视频在结构层面的偏差被有效约束。
- **人类评估**：编辑准确性 4.14、结构与运动保持 4.33（1-5 评分），用户感知的结构完整性和外观编辑效果均显著优于基线。

基线方法包括 **Tune-A-Video**（Wu et al., ICCV 2023）、**ControlVideo**（Zhang et al., arXiv 2023）、**Control-A-Video**、**TokenFlow**（Geyer et al., arXiv 2023）和 **Gen-1**（Esser et al., arXiv 2023）。这些方法主要依赖注意力注入或 ControlNet 深度/边缘引导，在运动保真度和帧一致性上均落后于 DreamMotion，验证了祖先采样路径在运动保持上的固有缺陷。

#### 级联模型（Show-1）上的性能

Table 2 展示了 DreamMotion 在级联框架 Show-1 上的结果。DreamMotion 仅优化关键帧生成阶段，后续时间插值和空间超分模块保持不变：

![[assets/figures/papers/paper_list_l32_DreamMotion_Space_Time_Self_Similarity_Score_Distillation_for_Zero_Shot/figures/010_Table_2.jpg]]
*Table 2: Quantitative evaluations. DreamMotion utilizing Show-1 surpasses other cascaded baselines across the five features. Other baselines were also implemented using the same video model, ensuring a fair comparison*

- **Text-Align**：0.7747
- **Frame-Con（自动）**：0.9755
- **人类评估**：帧一致性 3.97、编辑准确性 3.74、结构与运动保持 4.30

在所有五项特征上均超越使用同一视频模型的级联基线。这证明空间-时间自相似性正则化可以无缝嵌入级联框架，且仅优化关键帧阶段即可将结构-运动约束有效传播到后续模块。

#### 局部编辑对比

Table 4 将 DreamMotion 与专门针对局部编辑的 **DMT**（Diffusion-Motion-Transfer, Yatim et al., arXiv 2023）和 **Video-P2P**（Liu et al., arXiv 2023）进行对比：

![[assets/figures/papers/paper_list_l32_DreamMotion_Space_Time_Self_Similarity_Score_Distillation_for_Zero_Shot/figures/016_Table_4.jpg]]
*Table 4: Additional quantitative comparison with DMT and Video-P2P*

- **Motion-Fidelity**：DreamMotion 0.9259 vs DMT 0.8697 vs Video-P2P 0.7384
- **Frame-LPIPS**：DreamMotion 0.3042 vs DMT 0.3078 vs Video-P2P 0.3395

DreamMotion 在运动保真度上显著领先，帧级 LPIPS 也最低，表明掩码梯度过滤结合自相似性正则化在局部编辑场景下同样有效，且不会因局部修改破坏全局运动连贯性。

### 消融实验

Table 3 的定量消融和 Fig. 9 的定性消融共同揭示了各组件的因果贡献：

| 配置 | CLIP Score | 时序一致性 | 帧一致性 | Warping Error |
|------|-----------|-----------|---------|--------------|
| Full DreamMotion | 0.8209 | 0.9726 | 0.9259 | 0.3042 |
| 移除 S-SSM + T-SSM | 0.8202 | 0.9648 | 0.8426 | 0.3247 |
| 仅移除 T-SSM | — | — | 0.9011 | 0.3186 |
| 移除掩码条件 | 0.8180 | 0.9695 | 0.8653 | 0.3416 |

**关键发现**：

1. **移除全部自相似性损失**（仅保留 V-DDS）：CLIP Score 几乎不变（0.8202 vs 0.8209），但帧一致性从 0.9259 骤降至 0.8426，Warping Error 从 0.3042 升至 0.3247。这表明 V-DDS 单独可以注入目标外观，但缺乏结构-运动约束会导致严重的时序畸变和运动偏转。

2. **仅移除 T-SSM**：帧一致性降至 0.9011，Warping Error 升至 0.3186，证实 T-SSM 是消除闪烁和时序不连贯的关键组件。定性结果（Fig. 9）显示无 T-SSM 时视频出现明显的运动偏转和闪烁伪影。

3. **移除掩码梯度过滤**：CLIP Score 降至 0.8180，帧一致性降至 0.8653，Warping Error 升至 0.3416。Fig. 13 的定性对比显示，无掩码过滤时非编辑区域出现严重的模糊和过饱和，视觉保真度显著下降。

4. **联合优化最优**：Fig. 9 的定性消融直接展示，$\mathcal{L}_{\mathrm{V-DDS}} + \mathcal{L}_{\mathrm{S-SSM}} + \mathcal{L}_{\mathrm{T-SSM}}$ 联合优化生成的视频在结构完整性、运动连贯性和外观编辑效果上均达到最优。移除空间或时间对齐分别导致结构变形和时序闪烁。

### 失败模式与局限性

Fig. 10 展示了 DreamMotion 的主要失败模式：**无法处理需要大幅度结构变化的编辑任务**。由于 S-SSM 和 T-SSM 强依赖原始视频的空间结构和时间运动作为监督信号，当编辑指令要求显著的几何变形（如改变物体形状）或对象替换时，自相似性对齐会强制编辑视频保持原始结构，导致编辑效果不佳或编辑失败。这是该方法设计哲学的内在约束——以结构保持换取运动连贯性。

### 公平性说明

所有对比实验均在相同预训练视频扩散模型上进行（非级联用 Zeroscope，级联用 Show-1），基线方法使用官方实现和默认超参数。人类评估采用匿名视频和一致界面以避免偏差。

### 补充图表

![[assets/figures/papers/paper_list_l32_DreamMotion_Space_Time_Self_Similarity_Score_Distillation_for_Zero_Shot/figures/003_Figure_3.jpg]]
*Figure 3: Appearance Injection with Space-TimeSelf-Similarity Man→spider-man Fig. 3: Optimization progress visualization. The proposed self-similarity regularization effectively preserves the structure and motion of the original video*

![[assets/figures/papers/paper_list_l32_DreamMotion_Space_Time_Self_Similarity_Score_Distillation_for_Zero_Shot/figures/018_Figure_14.jpg]]
*Figure 14: “Amanisdoingakickflip.”→“Anastronautisdoingakickflip." Fig. 14: Visualization of optimization progress*

![[assets/figures/papers/paper_list_l32_DreamMotion_Space_Time_Self_Similarity_Score_Distillation_for_Zero_Shot/figures/012_Table.jpg]]



## 定位与知识库关联

### 核心瓶颈与设计转向

传统零样本视频编辑方法依赖基于祖先采样的逆向扩散过程（DDIM反演+去噪），其根本瓶颈在于：公开可用的文本到视频（T2V）扩散模型缺乏足够丰富的时间先验，且从噪声出发的逆扩散难以编程复杂运动，导致生成视频的运动不连贯与结构失真（Fig. 2）。DreamMotion 的设计转向是：**完全放弃祖先采样，改用分数蒸馏采样（SDS）驱动的优化范式**。这一转向将视频编辑从“采样生成”重构为“参数优化”，使方法不再受限于逆扩散的运动建模能力。

### 与基线方法的关系

DreamMotion 在零样本视频编辑赛道中与以下方法形成直接对比（Table 1, Table 2）：

- **Tune-A-Video** (Wu et al., ICCV 2023)：通过微调T2I模型的注意力层实现视频编辑，但依赖逐视频训练，且运动保持能力受限于空间注意力的稀疏注入。
- **ControlVideo** (Zhang et al., arXiv 2023) 与 **Control-A-Video**：引入ControlNet深度/边缘引导以保持结构，但额外的条件信号增加了推理复杂度，且对运动连贯性的约束是隐式的。
- **TokenFlow** (Geyer et al., arXiv 2023) 与 **Gen-1** (Esser et al., arXiv 2023)：前者通过token级特征传播维持时序一致性，后者依赖深度估计的结构引导；两者均未显式建模运动的时间自相似性。
- **Video-P2P** (Liu et al., arXiv 2023) 与 **Diffusion-Motion-Transfer (DMT)** (Yatim et al., arXiv 2023)：在局部编辑对比中（Table 4），DreamMotion 的运动保真度（0.9259）显著优于 DMT（0.8697）和 Video-P2P（0.7384），结构相似性（Frame-LPIPS 0.3042）也优于两者。

DreamMotion 相对于上述基线的关键差异在于**三个可替换槽位**（changed slots）：

| 槽位 | 基线做法 | DreamMotion 做法 |
|------|---------|-----------------|
| 优化范式 | 祖先采样（DDIM反演+去噪） | SDS/DDS驱动的梯度优化 |
| 结构保持 | 隐式注意力注入 / ControlNet引导 | 空间自相似性匹配（S-SSM） |
| 时间平滑 | 无显式约束或时序注意力 | 时间自相似性匹配（T-SSM） |

### 方法的知识贡献

DreamMotion 的核心知识贡献并非提出新的扩散模型架构，而是在**优化目标层面**引入了两个互补的正则化项：

1. **空间自相似性匹配（S-SSM）**：利用扩散U-Net中间层key特征的空间自相似性图（$SS_{i,j}^n$），强制编辑视频与原始视频在每帧内部保持相同的结构关系。这本质上是一种**结构蒸馏**，将预训练T2V模型对原始视频的深层结构理解迁移到编辑视频中。

2. **时间自相似性匹配（T-SSM）**：通过空间边缘均值压缩空间维度后，沿时间轴计算帧间自相似性矩阵，强制编辑视频与原始视频的时间相关性模式一致。这提供了一种**无参数的时间平滑机制**，不依赖光流或时序注意力。

此外，**掩码梯度过滤**（Fig. 6）作为实用组件，通过现成的检测模型生成二值掩码，选择性过滤V-DDS梯度，有效抑制了优化过程中的模糊和过饱和现象（消融实验：去除掩码后Frame-LPIPS从0.3042恶化至0.3416）。

### 适用边界与局限

DreamMotion 的适用边界由其核心机制决定：

- **强依赖原始视频的结构和运动**：S-SSM和T-SSM的正则化本质上是“保持原样”的约束，因此方法在需要**大幅度结构变化**（如几何变形、对象替换）的任务上能力有限（Fig. 10）。这是方法设计的固有取舍——优先保证运动连贯性，牺牲结构编辑自由度。

- **对级联模型的适配策略**：在Show-1等级联视频扩散模型中，DreamMotion仅在关键帧生成阶段进行优化，而非全流程。这降低了计算开销，但也意味着后续的时间插值和空间超分模块可能引入未被正则化约束的伪影。

- **依赖预训练T2V模型的质量**：V-DDS的梯度质量直接受限于底层T2V模型的外观先验；若模型对目标文本的理解偏差较大，蒸馏梯度可能引导出不符合预期的外观。

### 开放问题

1. **结构编辑能力的扩展**：如何在保持运动连贯性的前提下，允许可控的结构变化？可能的路径包括：在S-SSM中引入可学习的形变场，或设计分阶段的“先结构后外观”优化策略。

2. **计算效率的优化**：SDS优化需要多步梯度下降，推理时间显著高于单步采样的方法。是否可以通过元学习或蒸馏将优化过程压缩为前向网络，值得探索。

3. **自相似性特征的层级选择**：当前方法使用U-Net特定层的key特征计算自相似性，不同层级对结构和纹理的敏感度不同。系统性研究特征层级的选择策略可能进一步提升效果。

4. **泛化到更复杂的运动模式**：T-SSM基于帧间余弦相似性，对快速运动或大幅度遮挡场景的鲁棒性尚待验证。引入多尺度时间窗口或可变形的时间对齐机制可能是改进方向。



## 原文 PDF

![[paperPDFs/ECCV_2024/DreamMotion_Space_Time_Self_Similarity_Score_Distillation_for_Zero_Shot_Video_Editing.pdf]]
