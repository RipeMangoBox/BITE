---
title: "Motion Modes: What Could Happen Next?"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Motion_Modes_What_Could_Happen_Next.pdf
aliases:
- MM
- MMWCHN
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "在基于Motion-I2V的去噪过程中，引入四种引导能量函数（静态摄像机引导、物体运动引导、多样性引导、平滑性引导）并最小化能量梯度，直接调控运动向量场的生成。"
primary_logic: "通过训练自由的能量引导，可在预训练的视频扩散模型潜空间中高效搜索，无需额外训练即可分离摄像机运动与物体运动，并迭代采样出具有多样性的物体运动模式。"
claims:
- "用户研究中，96% 的生成运动被认为是合理的，92% 符合观众预期，表明生成质量高。"
- "在与三种基线的用户对比（User Study I）中，我们的方法在合理性、多样性和期望性方面均以显著优势胜出。"
- "消融实验证实，移除任何一种引导能量（静态摄像机、物体运动、多样性或平滑性）均导致相应指标恶化，全模型达到最佳权衡（Ē=0.55）。"
- "28 diverse images (User Study I) 上 用户偏好率 (合理性、多样性、期望性) = Motion Modes"
---

# Motion Modes: What Could Happen Next?

> [!tip] 核心洞察
> 通过训练自由的能量引导，可在预训练的视频扩散模型潜空间中高效搜索，无需额外训练即可分离摄像机运动与物体运动，并迭代采样出具有多样性的物体运动模式。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 运动模式：探索物体的多种可能运动 |
| 英文题名 | Motion Modes: What Could Happen Next? |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.00148); [Project](https://motionmodes.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Motion Modes |
| Dataset | 28 diverse images (User Study I), 28 diverse images (User Study II) |

> [!tip] 效果简介
> - 28 diverse images (User Study I) 上，用户偏好率 (合理性、多样性、期望性) 为 Motion Modes，对比 Prompt Generation, ControlNet, Random Arrows，变化 Motion Modes 在所有属性上均以显著优势被优先选择（95% 置信区间不重叠）。
> - 28 diverse images (User Study II) 上，合理性 (Plausibility) 为 96%，对比 不适用 (无基线对比)，变化 96% 的运动被评估为合理。

## 概述

给定一张静态图像和其中某个物体的掩码，该物体可能发生哪些符合物理规律、但又彼此不同的运动？现有图像到视频生成模型难以自动发现并解耦特定物体的多种运动：生成的运动常与摄像机运动及其他场景变化纠缠在一起，且缺乏多样性。

**Motion Modes** 针对这一瓶颈，提出了一种无需训练的引导式推理方法。其核心思路是：在预训练的图像到视频扩散模型（基于 Motion-I2V）的去噪过程中，引入四种引导能量函数——静态摄像机引导 $E_c$、物体运动引导 $E_o$、多样性引导 $E_d$ 和平滑性引导 $E_s$——并通过最小化能量梯度直接调控运动向量场的生成。这一“训练自由”的能量引导机制，可在潜空间中高效搜索，将摄像机运动与物体运动分离，并迭代采样出具有多样性的物体运动模式。

实验表明，该方法在运动合理性、多样性和符合用户期望等方面显著优于基于提示生成、ControlNet 约束和随机拖拽箭头等基线方法。用户研究中，96% 的生成运动被评估为合理，92% 符合观众预期。消融实验进一步证实，四类引导能量缺一不可：移除任一项均导致相应指标的恶化，全模型在多样性与聚焦性之间达到最佳权衡（$\bar{E}=0.55$）。

## 背景与动机

从单张静态图像预测物体的未来运动，是人类视觉理解中一项基本但极具挑战的能力。给定一张包含笔记本电脑、飘扬的旗帜或跃起的狮子的照片，观察者可以自然地想象出多种合理的运动演化——合上屏幕、旗帜翻卷、狮子落地。然而，让计算模型自动发现并生成这些多样化的运动，至今仍是一个未解决的难题。

### 现有方法的缺口

当前主流的图像到视频生成模型（image-to-video generators）虽然在生成逼真视频方面取得了显著进展，但在探索物体的多种运动模式时面临两个核心瓶颈：

**1. 运动纠缠问题。** 生成的运动往往与摄像机运动、其他场景变化（如光照、背景动态）紧密耦合。模型难以将特定物体的运动从全局场景变化中分离出来，导致生成的物体运动不纯粹、不可控。

**2. 多样性匮乏。** 现有方法通常只能为给定物体生成单一或高度相似的运动轨迹。例如，基于大语言模型生成文本提示的方法（Prompt Generation，使用 GPT-4o + Motion-I2V）虽然可以描述不同的运动意图，但无法有效解耦摄像机运动，且多样性有限；基于 ControlNet 约束运动区域的方法（MotionBrush, Shi et al., SIGGRAPH 2024）倾向于将物体固定在原位，缺乏运动变化；而随机生成拖拽箭头的方法（MotionDrag, Shi et al., SIGGRAPH 2024）虽然为运动提供了方向，但无法确保复杂运动的产生和运动解耦。

### 本文动机

上述瓶颈的根源在于：现有方法缺乏一个显式的机制来**解耦摄像机运动与物体运动**，同时也缺少一个高效的搜索策略来**在巨大的运动空间中采样多样化的运动模式**。

本文的核心动机是：能否在不进行额外训练的前提下，利用预训练视频扩散模型中蕴含的运动先验，通过设计精巧的引导信号，在潜空间中高效搜索并分离出物体的多种合理运动？这一思路的关键洞察在于——训练自由的能量引导（training-free energy guidance）可以在去噪过程中直接调控运动向量场的生成，无需任何标注数据或模型微调。

## 核心创新

Motion Modes 的核心创新在于提出了一种**免训练的引导式运动探索框架**，在预训练的图像到视频扩散模型潜空间中高效搜索，自动发现并解耦特定物体的多种可能运动。该方法通过四个关键机制实现突破：

### 1. 运动与外观的生成解耦

与直接生成像素视频的传统方法不同，Motion Modes 采用 **Motion-I2V**（Shi et al., SIGGRAPH 2024）的流生成模块作为主干网络，将运动表示为与外观分离的时间相关二维向量场 $\mathbf{x} \in \mathbb{R}^{F \times H \times W \times 2}$（Section 3.1）。这一设计使得后续的能量引导可以直接作用于运动向量，而非耦合的像素空间，从根源上降低了摄像机运动与物体运动的纠缠难度。

### 2. 四种引导能量的协同优化

在标准的 DDIM 去噪过程中，Motion Modes 引入了四种可微分的引导能量函数，并通过梯度下降最小化其组合能量（Eq. 4），实现对运动向量场的精细调控：

- **静态摄像机引导** $E_c$：惩罚物体掩码外部的平均运动幅度，强制背景区域保持静止，从而抑制摄像机运动。
- **物体运动引导** $E_o$：通过软逆激活函数鼓励物体区域内部与外部的运动幅度差异，促使指定物体产生显著运动。
- **多样性引导** $E_d$：受粒子引导（particle guidance）启发，对已生成的运动集合施加排斥力，确保新采样的运动与历史运动保持差异。
- **平滑性引导** $E_s$：惩罚相邻帧间的运动突变，鼓励时间维度上的运动连续性。

这四种能量以加权和 $E(\mathbf{x}, \mathbf{m}, \mathcal{X}) := \lambda_d E_d + \lambda_c E_c + \lambda_o E_o + \lambda_s E_s$（权重分别为 $\lambda_d=3.0$, $\lambda_c=0.2$, $\lambda_o=0.025$, $\lambda_s=0.1$）组合，在去噪的前 20 步（共 25 步）中施加引导（Section 3.3, Appendix E）。

### 3. 迭代采样与自适应停止准则

为高效生成多样运动集合，Motion Modes 采用迭代采样策略：每次生成一个运动后，将其加入已生成集合 $\mathcal{X}$，作为后续多样性引导 $E_d$ 的排斥参考。同时引入基于能量的停止准则——当最终运动的组合能量超过阈值 $\rho=5.0$ 时丢弃该运动，连续两次丢弃则终止采样（Section 3.3）。这一机制避免了预设运动数量的限制，使生成数量自适应于场景的物理可能性。

### 4. 与基线方法的关键差异

相较于现有探索物体运动的方法，Motion Modes 在三个关键维度上实现了根本性改进：

| 维度 | 基线方法 | Motion Modes |
|------|---------|-------------|
| **摄像机解耦** | Prompt Generation 无法有效解耦；ControlNet 倾向于固定物体 | 通过 $E_c$ 和 $E_o$ 显式分离摄像机与物体运动 |
| **多样性生成** | Random Arrows 随机采样，多样性有限且效率低 | 通过 $E_d$ 排斥历史运动，配合迭代采样高效探索多样模式 |
| **训练需求** | ControlNet 需要额外条件训练 | 完全免训练，仅在推理时修改去噪轨迹 |

消融实验证实了这一设计的有效性：移除 $E_c$ 导致摄像机运动剧增（$\bar{E}_c$ 升高），移除 $E_o$ 使物体运动幅度极小，移除 $E_d$ 导致多样性显著下降，移除 $E_s$ 不仅降低平滑度还意外损害物体聚焦度。全模型在多样性与聚焦性的权衡指标 $\bar{E} := 0.5(\bar{E}_d + \bar{E}_f)$ 上达到最优值 0.55（Table 2, Table 3）。

## 整体框架

![[assets/figures/papers/paper_list_l23_Motion_Modes_What_Could_Happen_Next/figures/003_Figure_3.jpg]]
*Figure 3: Method Overview. We generate a motion x using a guided denoising approach, where guidance energies encourage smooth object motions that are disentangled from camera motions and distinct from previously generated motions. Iterative sampling gives us a set of diverse motions X*

Motion Modes 的整体 pipeline 围绕一个核心思想展开：在预训练的图像到视频扩散模型的潜空间中，通过训练自由的能量引导，高效搜索并解耦出物体的多种可能运动。其输入是一张静态图像和一个指定目标物体的二值掩码，输出是一组在时间和空间上平滑、且彼此各异的 2D 运动向量场。

流程可分解为四个串联的功能模块：

1. **输入与掩码**：用户提供一张静态图像以及一个二值掩码 $\mathbf{m}$，用于标定需要探索运动的目标物体区域。这是整个 pipeline 的唯二外部输入。

2. **流生成器（基于 Motion-I2V）**：采用 Motion-I2V 的流生成模块作为主干网络，该模块是一个预训练的图像到视频扩散模型，专门生成与外观分离的运动向量场 $\mathbf{x} \in \mathbb{R}^{F \times H \times W \times 2}$（$F$ 为帧数，$H \times W$ 为空间分辨率，每像素对应一个 2D 偏移向量）。在推理时，ControlNet 模块被断开，去噪过程共 25 步，其中前 20 步施加能量引导。

3. **引导能量计算**：在去噪过程的每一步，从当前噪声样本中估计出“干净”运动 $x_\theta^0(\mathbf{x}_t; t, \mathbf{y})$，然后在其上计算四种引导能量：
   - **静态摄像机引导** $E_c$：惩罚掩码外部的平均运动幅度，抑制摄像机运动；
   - **物体运动引导** $E_o$：鼓励物体区域内部与外部的运动幅度差异，促使物体运动；
   - **多样性引导** $E_d$：对已生成的运动集合 $\mathcal{X}$ 施加排斥力，确保新运动与之前不同；
   - **平滑性引导** $E_s$：惩罚相邻帧间的运动突变，保证时间平滑。

   四种能量按权重组合为总引导能量 $E = \lambda_d E_d + \lambda_c E_c + \lambda_o E_o + \lambda_s E_s$（权重分别为 3.0、0.2、0.025、0.1）。

4. **引导去噪推理与迭代采样**：将总能量梯度 $\nabla_{\mathbf{x}_t} E$ 作用于预测的干净运动，修改标准 DDIM 去噪轨迹，实现受控运动生成。每次采样生成一个运动 $\mathbf{x}$，若其总能量超过阈值 $\rho = 5.0$ 则丢弃并重采样；连续两次丢弃则停止迭代。最终输出一个多样化的运动集合 $\mathcal{X}$。

这一 pipeline 的关键设计在于：所有引导能量均在推理时计算并最小化，无需对预训练模型进行任何微调或重训练。通过将摄像机运动解耦、物体运动聚焦、运动多样性探索三者统一在能量最小化框架下，Motion Modes 实现了从单张静态图像到多种合理物体运动的高效映射。

## 核心模块与公式推导

Motion Modes 的核心架构建立在预训练的图像到视频扩散模型 **Motion-I2V** 之上，通过训练自由的能量引导策略，在去噪过程中直接调控运动向量场的生成。整个流程由四个关键模块串联构成，如图 3 所示。

### 1. 输入与掩码

系统接收一张静态图像和一个指定目标物体的二值掩码 $\mathbf{m} \in \{0,1\}^{H \times W}$。掩码用于区分物体区域（值为 1）与背景区域（值为 0），为后续所有引导能量的计算提供空间参照。运动被表示为一个时间相关的二维向量场：

$$\mathbf{x} \in \mathbb{R}^{F \times H \times W \times 2}$$

其中 $F$ 为帧数，$H$ 和 $W$ 为空间分辨率，每个像素存储一个二维偏移向量，描述该点从第一帧到当前帧的位移。

### 2. 流生成器

流生成器直接复用 Motion-I2V 的流生成模块作为主干网络。该模块是一个扩散模型，其核心特点是将运动生成与外观生成分离——它预测的是与图像内容无关的纯运动向量场，而非直接生成视频帧。这种设计天然地将物体/摄像机运动与其他场景变化（如光照、纹理变化）解耦。

在训练和推理中，向干净的运动 $\mathbf{x}$ 添加高斯噪声：

$$\mathbf{x}_t = \sqrt{\alpha(t)} \mathbf{x} + \sqrt{1 - \alpha(t)} \epsilon$$

其中 $\alpha(t)$ 为噪声调度参数，$\epsilon \sim \mathcal{N}(0, \mathbf{I})$ 为标准高斯噪声。模型 $\epsilon_\theta$ 学习从噪声样本 $\mathbf{x}_t$ 中预测所加噪声，进而可估计干净运动：

$$x_\theta^0(\mathbf{x}_t; t, \mathbf{y}) := \frac{1}{\sqrt{\alpha(t)}} \left( \mathbf{x}_t - \sqrt{1-\alpha(t)} \epsilon_\theta(\mathbf{x}_t; t, \mathbf{y}) \right)$$

其中 $\mathbf{y}$ 为条件输入（静态图像）。

### 3. 引导能量计算

这是方法的核心创新模块，定义了四种引导能量函数，在去噪过程中通过梯度下降最小化，从而将运动生成推向期望的特性。

**静态摄像机引导能量 $E_c$**：惩罚掩码外部的平均运动幅度，强制背景区域保持静止，从而抑制摄像机运动。

$$E_c(\mathbf{x}, \mathbf{m}) := \frac{\sum_{k,i,j} \|\mathbf{x}_{k,i,j}\| \cdot (1 - \mathbf{m}_{i,j})}{\sum_{k,i,j} (1 - \mathbf{m}_{i,j})}$$

其中 $\mathbf{x}_{k,i,j}$ 表示第 $k$ 帧位置 $(i,j)$ 的运动向量，分子对背景区域（$1-\mathbf{m}_{i,j}=1$）的运动幅度求和，分母为背景像素总数。$E_c$ 越小，摄像机越趋于静止。

**物体运动引导能量 $E_o$**：通过软逆激活函数 $\phi$ 鼓励物体区域内部与外部之间的运动幅度差异，促使物体产生显著运动。

$$E_o(\mathbf{x}, \mathbf{m}) := \phi\left( |E_c(\mathbf{x}, \mathbf{m}) - E_c(\mathbf{x}, 1 - \mathbf{m})| \right)$$

其中 $E_c(\mathbf{x}, 1-\mathbf{m})$ 计算的是物体区域内部的平均运动幅度。$\phi$ 是一个单调递减函数（如 $\phi(z) = 1/(1+z)$），当内外运动差异越大时 $E_o$ 越小，即鼓励物体运动幅度远超背景。

**多样性引导能量 $E_d$**：对之前已生成的运动集合 $\mathcal{X}$ 施加排斥力，确保新生成的运动与已有运动不同。

$$E_d(\mathbf{x}, \mathbf{m}, \mathcal{X}) := \sum_{\tilde{\mathbf{x}} \in \mathcal{X}} \frac{\sum_{k,i,j} \phi\left( d\left( \mathbf{x}_{k,i,j}, \tilde{\mathbf{x}}_{k,i,j} \right) \right) \mathbf{m}_{i,j}}{\sum_{k,i,j} \mathbf{m}_{i,j}}$$

其中 $d(\cdot, \cdot)$ 度量两个运动向量之间的距离（如欧氏距离），$\phi$ 同样为递减函数。当新运动 $\mathbf{x}$ 与已有运动 $\tilde{\mathbf{x}}$ 在物体区域（$\mathbf{m}_{i,j}=1$）内越相似时，$\phi$ 值越大，$E_d$ 越高，形成排斥效应。该能量受粒子引导（particle guidance）启发，无需显式训练数据即可实现多样性。

**平滑性引导能量 $E_s$**：惩罚相邻帧之间运动向量的突变，鼓励时间维度上的平滑过渡。

$$E_s(\mathbf{x}, \mathbf{m}) := \frac{\sum_{k,i,j} d\left( \mathbf{x}_{k,i,j}, \mathbf{x}_{k+1,i,j} \right) \mathbf{m}_{i,j}}{\sum_{k,i,j} \mathbf{m}_{i,j}}$$

该能量仅作用于物体区域，计算相邻帧运动向量的平均差异。$E_s$ 越小，运动越平滑。

四种能量通过加权组合形成总引导能量：

$$E(\mathbf{x}, \mathbf{m}, \mathcal{X}) := \lambda_d E_d + \lambda_c E_c + \lambda_o E_o + \lambda_s E_s$$

权重设置为 $\lambda_d=3.0$，$\lambda_c=0.2$，$\lambda_o=0.025$，$\lambda_s=0.1$。

### 4. 引导去噪推理

在标准 DDIM 采样的基础上，将能量梯度作用于预测的干净运动，修改去噪轨迹：

$$\mathbf{x}_{t-1} \sim \mathcal{N}\left( a_t \mathbf{x}_t - b_t \epsilon_\theta(\mathbf{x}_t'; t, \mathbf{y}), \sigma_t^2 \mathbf{I} \right)$$

其中关键修改在于：

$$\mathbf{x}_t' := \mathbf{x}_t - \nabla_{\mathbf{x}_t} E\left( x_\theta^0(\mathbf{x}_t; t, \mathbf{y}), \mathbf{m}, \mathcal{X} \right)$$

即先估计当前噪声样本对应的干净运动 $x_\theta^0$，计算该干净运动上的总能量梯度，再用该梯度修正噪声样本 $\mathbf{x}_t$，然后送入去噪网络。流生成器共使用 25 个去噪时间步，其中前 20 步施加引导（Section E）。

### 5. 迭代采样与停止准则

为生成多样运动集合 $\mathcal{X}$，采用迭代采样策略：每次独立采样一个运动，计算其总引导能量 $E$。若 $E > \rho$（阈值 $\rho=5.0$），则丢弃该运动并重新采样；若连续两次被丢弃，则停止迭代。这一准则在多样性与质量之间取得平衡，避免生成低质量或重复的运动。

## 实验与分析

### 定量对比与用户研究

本文在28张多样化图像上对比了Motion Modes与三种基线方法。定量指标直接使用引导能量函数计算：多样性 $\bar{E}_d$ 衡量生成运动集合内部的差异性，聚焦性 $\bar{E}_f = 0.5(\bar{E}_o + \bar{E}_c)$ 衡量运动是否集中在目标物体上且摄像机保持静止。如表1所示，Motion Modes在所有指标上均优于基线——多样性 $\bar{E}_d=1.04$，聚焦性 $\bar{E}_f=0.07$，而Prompt Generation、ControlNet和Random Arrows的聚焦性分别为0.58、0.60和0.23，多样性也明显更差。

![[assets/figures/papers/paper_list_l23_Motion_Modes_What_Could_Happen_Next/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of the diverse and focused property of our output motions to all baselines*

用户研究I（Figure 4）进一步验证了定量结果：在合理性、多样性和期望性三个维度上，Motion Modes被用户优先选择的比率均以显著优势超过所有基线（95%置信区间不重叠）。用户研究II单独评估Motion Modes的生成质量，结果显示96%的运动被判定为合理，92%符合观众预期，另有19%的运动虽超出预期但仍被视为合理——表明方法在保证合理性的同时具备一定的“启发性”输出能力。

**需要注意**：定量指标直接对应本方法优化的能量函数，可能天然倾向于本方法；但独立的用户研究结果与定量趋势一致，增强了结论的可信度。

### 消融实验

消融实验系统性地验证了四种引导能量各自的作用（Table 2与Table 3），以综合权衡指标 $\bar{E} = 0.5(\bar{E}_d + \bar{E}_f)$ 衡量整体性能。

![[assets/figures/papers/paper_list_l23_Motion_Modes_What_Could_Happen_Next/figures/006_Table_2.jpg]]
*Table 2: Ablation of key components with metrics based on diverse, focused metrics and their tradeoff $\bar { E }$ : = 0 . 5 ( $\bar { E } _ { d } + \bar { E } _ { f }$ ) ). Underlined values are closer to the best than to the worst value

- **移除静态摄像机引导 $E_c$**：摄像机运动剧增（$\bar{E}_c$ 升高），背景区域出现大量干扰运动，严重破坏物体运动的可辨识性。
- **移除物体运动引导 $E_o$**：物体运动幅度极小（$\bar{E}_o$ 升高），生成的运动失去焦点，无法有效驱动目标物体。
- **移除多样性引导 $E_d$**：运动集合的多样性显著下降（$\bar{E}_d$ 升高），多个采样结果趋于相似。若用最远点采样（FPS）替代 $E_d$，多样性进一步恶化（$\bar{E}_d=1.49$），表明排斥式能量引导比后处理筛选更有效。
- **移除平滑性引导 $E_s$**：不仅降低了时间平滑度，还意外损害了物体聚焦度——原因在于不连贯的运动倾向于使物体趋于静止以避免突变，反而削弱了 $E_o$ 的激励效果。
- **用ControlNet替代 $E_c$ 和 $E_o$**：物体几乎被固定在原地（$\bar{E}_o$ 高），证实ControlNet的约束方式倾向于抑制而非鼓励运动，无法替代本文的解耦引导策略。

全模型在 $\bar{E}=0.55$ 处达到最佳权衡，移除任一组件均导致该指标恶化，验证了四种能量的互补性。

### 定性分析与应用

Figure 5展示了四组场景下的定性对比：Motion Modes生成的物体运动轨迹（红色端点）清晰聚焦于掩码区域，背景轨迹（紫色）极少，表明摄像机运动被有效抑制；而基线方法要么产生大范围背景漂移，要么物体几乎不动。Figure 6演示了运动补全应用——利用已发现的运动集合 $\mathcal{X}$ 完成用户粗略的拖拽箭头输入，通过公式 $\min_{\mathbf{k}} \|\mathbf{x}_{k,\mathbf{a}} - \overrightarrow{\mathbf{a}\mathbf{b}}\|_2$ 检索最匹配的帧内偏移，为DragonDiffusion或Motion-I2V等下游模型提供精细运动条件，避免了手动指定复杂运动（如旗帜飘动）的困难以及条件歧义导致的失败（如漂浮的火车）。

### 局限性与失败模式

Figure 7揭示了两个主要失败模式：
1. **视频先验导致的形变**：预训练的视频扩散模型可能产生不符合物理规律的形变，例如弯曲的钟表指针或双猫尾，这是由于生成先验对刚性约束的理解不足。
2. **离散采样的局限性**：连续的运动空间只能通过离散迭代采样探索，可能遗漏某些细微或中间的运动模式。当前停止准则（连续两次丢弃则终止）在效率与完备性之间做了折中，但无法保证穷举。

此外，当前方法仅支持静态摄像机场景，无法处理体育、动作镜头等含摄像机运动的输入；运动表示局限于2D向量场，尚未扩展到3D运动或4D序列网格。推理时的峰值内存为21.7GB，单次运动生成耗时约2分35秒，批量化生成仍有优化空间。

### 补充图表

![[assets/figures/papers/paper_list_l23_Motion_Modes_What_Could_Happen_Next/figures/012_Table_3.jpg]]
*Table 3: Extended ablation of key components with metrics based on diverse, focused metrics and their tradeoff $\bar { E }$ : = 0 . 5 ( $\bar { E } _ { d } + \bar { E } _ { f }$ ) Underlined values are closer to the best than to the worst value

## 方法谱系与知识库定位

### 核心思路与问题定位

Motion Modes 瞄准的是一个尚未被充分解决的关键瓶颈：**现有图像到视频生成模型无法自动发现并解耦特定物体的多种可能运动**。预训练的视频扩散模型虽然具备强大的运动先验，但其生成的运动通常与摄像机运动、其他场景变化纠缠在一起，且单次采样只能提供一个确定性结果，缺乏对运动多样性的探索能力。

该方法的核心洞察在于：**通过训练自由的能量引导，可在预训练视频扩散模型的潜空间中高效搜索，无需额外训练即可分离摄像机运动与物体运动，并迭代采样出具有多样性的物体运动模式**。这本质上是一种“从隐式视频先验中蒸馏显式运动模式”的策略——将扩散模型视为一个隐式运动分布，通过精心设计的引导能量在推理时对该分布进行受控采样。

### 与现有方法的关系

#### 视频扩散模型作为运动生成器

Motion Modes 直接构建在 **Motion-I2V**（Shi et al., SIGGRAPH 2024）之上，复用其核心的“流生成器”模块——一个将运动向量场与外观生成解耦的图像到视频扩散模型。Motion-I2V 本身通过 ControlNet 或拖拽箭头来约束运动，但缺乏自动发现多种运动的能力。Motion Modes 的创新在于**将 Motion-I2V 从条件生成器转变为无引导条件的运动探索器**：断开 ControlNet 模块，仅保留流生成器作为运动先验的来源，然后通过能量函数在去噪过程中注入控制信号。

#### 与提示工程方法的对比

**Prompt Generation (GPT-4o + Motion-I2V)** 代表了用大语言模型生成文本描述来引导运动探索的思路。该方法通过 GPT-4o 为每个期望的运动方向生成文本提示，再输入 Motion-I2V 生成视频。其根本局限在于：文本提示无法精细控制摄像机与物体运动的解耦，且语言描述的运动空间远小于实际可能的运动多样性。

#### 与基于控制信号方法的对比

**ControlNet (MotionBrush of Motion-I2V)**（Shi et al., SIGGRAPH 2024）通过 ControlNet 约束运动区域，但倾向于将物体固定在原位，缺乏运动多样性。**Random Arrows (MotionDrag of Motion-I2V)**（Shi et al., SIGGRAPH 2024）随机生成拖拽箭头为运动提供方向，但无法确保摄像机与物体运动的解耦，也难以产生复杂的运动模式。这两种方法都依赖外部条件信号来“指定”运动，而 Motion Modes 通过能量引导“搜索”运动，从机制上更适合多样性探索。

#### 与粒子引导方法的联系

多样性引导能量 $E_d$ 的设计灵感来源于粒子引导（particle guidance）的思想——通过对已生成样本施加排斥力来鼓励新样本的多样性。Motion Modes 将这一思想适配到运动向量场的时序结构中，在掩码区域内对先前生成的运动施加排斥，从而高效采样出差异化的运动模式。

### 方法适用边界

**适用场景**：
- 静态摄像机拍摄的静态图像，需要对指定物体生成多种合理运动
- 物体类型覆盖刚性运动（如笔记本电脑开合）、复杂形变（如旗帜飘动）和关节角色（如狮子、猫）
- 下游应用包括运动补全（将用户粗略拖拽箭头补全为详细运动）、为拖拽式图像编辑器或运动到视频生成器提供条件输入

**不适用或受限场景**：
- **动态摄像机场景**：能量函数 $E_c$ 显式惩罚掩码外部的运动，因此无法处理体育、动作镜头等含有摄像机运动的场景
- **3D 运动生成**：当前方法仅生成 2D 向量场，尚未扩展到 3D 运动或 4D 动态网格序列
- **连续运动空间的离散采样局限**：迭代采样只能探索运动空间的离散点，可能遗漏细微或中间的运动模式

### 已知失效模式

1. **视频先验导致的错误形变**：预训练视频生成模型的质量上限直接约束了运动生成的质量。例如，钟表指针可能弯曲变形，猫可能出现两条尾巴——这些是视频扩散模型自身的幻觉，而非能量引导引入的问题。

2. **平滑性引导的意外副作用**：消融实验显示，移除平滑性引导 $E_s$ 不仅降低时间平滑度，还会意外损害物体聚焦度——因为平滑性约束倾向于避免生成完全静止的物体，间接鼓励了物体运动。

3. **内存与计算开销**：引导去噪的峰值内存为 21.7 GB，单次运动生成耗时约 2 分 35 秒（Appendix E）。迭代采样多个运动时，总时间线性增长，限制了实时交互场景的应用。

### 开放问题

1. **动态摄像机扩展**：如何将方法扩展到包含摄像机运动的场景？这需要重新设计能量函数，使其能区分摄像机运动与物体运动，而非简单惩罚所有背景运动。

2. **从 2D 到 3D/4D**：能否将 2D 运动场扩展为 3D 动态网格，生成动画网格序列？这需要将运动表示从像素空间的 2D 偏移升级到 3D 顶点位移，并与现有的 4D 重建或编辑管线对接。

3. **推理效率优化**：如何在推理时降低内存开销，支持更大批量的并行运动生成？可能的路径包括减少引导步数、采用更轻量的运动表示、或利用一致性模型等少步采样方法。

4. **运动空间的连续参数化**：当前离散采样策略可能遗漏运动空间的连续变化。是否可以通过学习运动空间的低维流形或引入连续插值机制，实现对运动模式更全面的覆盖？

## 原文 PDF

![[paperPDFs/CVPR_2025/Motion_Modes_What_Could_Happen_Next.pdf]]
