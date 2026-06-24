---
title: "HOIAnimator: Generating Text-prompt Human-object Animations using Novel Perceptive Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel_Perceptive_Diffusion_Models.pdf
aliases:
- HOIAnimator
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过解耦人类与物体的扩散过程并引入交互接触场（ICF）作为生成指导信号，利用感知消息传递（PMP）实现双向通信，从而显式建模人与物的交互动态。
primary_logic: 将HOI动画生成分解为人类和物体两条扩散流，并通过感知消息传递（PMP）与交互接触场（ICF）实现双向适配与物理约束，让模型从文本中更忠实地还原动态交互。
claims:
- "HOIAnimator uses dual Perceptive Diffusion Models (PDM): a human-centric model and an object-centric model."
- A Perceptive Message Passing (PMP) mechanism enables communication between the two diffusion models.
- Interaction Contact Field (ICF) implicitly captures HOI essence by assessing proximity informed by a learned probabilistic distribution.
- PMP adaptively learns weight and bias of object clues embedded into human motion flow.
---

# HOIAnimator: Generating Text-prompt Human-object Animations using Novel Perceptive Diffusion Models

> [!tip] 核心洞察
> 将HOI动画生成分解为人类和物体两条扩散流，并通过感知消息传递（PMP）与交互接触场（ICF）实现双向适配与物理约束，让模型从文本中更忠实地还原动态交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | HOIAnimator：使用新型感知扩散模型生成文本驱动的人-物交互动画 |
| 英文题名 | HOIAnimator: Generating Text-prompt Human-object Animations using Novel Perceptive Diffusion Models |
| 会议/期刊 | CVPR 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | HOIAnimator |
| Dataset | BEHAVE |

> [!tip] 效果简介
> - BEHAVE 上，Top-3 Precision 0.781 vs 0.734 (InterGen) (+0.047)；FID 0.623 vs 0.717 (InterGen) (-0.094)；Penetration 0.643 vs 0.613 (InterGen) (+0.030)。

## 概述

**问题瓶颈**：文本驱动的人-物交互（HOI）动画生成面临着双重挑战——既要精确建模人体运动与物体动态，又要保证两者间的接触与力交互具有物理真实感。现有方法通常将人与物视为单一整体进行建模，难以解耦并协调这两类截然不同的运动模式，导致生成的动画缺乏可信的接触关系和交互协调性。

**核心方法**：HOIAnimator 提出了一种**新型感知扩散模型（Perceptive Diffusion Models, PDM）**，将 HOI 动画生成分解为**人类中心扩散模型**与**物体中心扩散模型**两个并行分支，并通过**感知消息传递（Perceptive Message Passing, PMP）** 机制实现双向信息交换。同时，引入**交互接触场（Interaction Contact Field, ICF）** 作为生成指导信号，该场通过学习接触概率分布，综合物体可供性、人类意图和人体工程学信息，显式约束人与物之间的空间关系。

**主要结果**：在 BEHAVE 数据集上，HOIAnimator 在 Top-3 精度上达到 0.781（较 InterGen 的 0.734 提升 4.7 个百分点），FID 降至 0.623（降低 9.4 个百分点），顶点距离降至 0.118（降低 40.5 个百分点），显著优于现有基线方法。消融实验进一步证实，PDM 双分支架构、PMP 消息传递与 ICF 接触场三者联合使用才能取得最优性能，任一模块的移除都会导致穿透失真或交互动态缺失。

**方法定位**：HOIAnimator 属于**解耦式双流扩散生成**范式，与单一人-物共享 Transformer 的扩散基线（如 MDM, Tevet et al., ICLR 2023）形成鲜明对比，其核心创新在于通过显式的跨实体通信机制和接触场先验，将物理约束融入扩散去噪过程。

## 背景与动机

### 人-物交互动画生成的核心瓶颈

生成逼真的人-物交互（Human-Object Interaction, HOI）动画是计算机视觉与图形学中的一项基础性挑战。其关键难点在于：一段可信的交互动画必须同时精确建模三个相互耦合的要素——**人体的运动轨迹**、**物体的动态响应**，以及两者之间**微妙且符合物理规律的接触与力交互**。现有方法往往只能孤立地处理人或物，缺乏对交互动态的显式建模，导致生成的动画出现穿透、滑步或交互语义错位等失真现象。

具体而言，传统文本驱动动画生成方法面临以下结构性缺口：

1. **人-物运动解耦困难**：人类运动与物体运动遵循不同的物理约束和时序模式，但两者在交互过程中又高度耦合。单一扩散模型难以同时捕捉这两种异质动态。
2. **接触与力交互缺失**：现有方法通常仅依赖距离阈值进行碰撞检测，缺乏对接触概率、物体可供性（affordance）和人体工程学约束的显式建模，导致交互缺乏物理真实感。
3. **跨实体信息流断裂**：人类与物体的运动生成过程之间缺少有效的双向通信机制，使得模型无法根据物体状态动态调整人体姿态，反之亦然。

### 现有方法的局限

以 **MDM**（Tevet et al., ICLR 2023）为代表的文本驱动运动扩散模型，虽然在单一人体运动生成上取得了显著进展，但其架构本质上假设输入为单一实体的运动序列。当直接扩展至HOI场景时，这类方法将人与物体的运动参数拼接为统一向量，交由共享的Transformer扩散模型处理。这种“扁平化”策略忽略了人与物在运动学结构、动态特性和交互约束上的本质差异。

后续工作如 **InterGen**（Liang et al., arXiv 2023）尝试处理多人交互生成，但仍未显式建模人与物体之间的接触场和力传递。**PriorMDM**（Shafir et al., arXiv 2023）则侧重于利用扩散模型作为运动先验，同样缺乏对交互接触的专门设计。这些方法在BEHAVE等标准基准上暴露出明显不足：语义匹配精度有限，且生成结果中普遍存在不真实的穿透和空间关系错误。

### 本文动机

针对上述瓶颈，本文提出 **HOIAnimator**，核心动机是通过**解耦-通信-约束**的三阶段设计范式，从根本上重塑HOI动画的生成流程：

- **解耦**：将HOI动画生成分解为人类中心扩散模型与物体中心扩散模型两个分支，使各自专注于自身运动模式的建模。
- **通信**：引入感知消息传递（Perceptive Message Passing, PMP）机制，实现双分支间的双向信息交换，让人类运动感知物体状态，物体运动响应人类动作。
- **约束**：设计交互接触场（Interaction Contact Field, ICF），以概率分布的形式显式建模接触可能性，综合物体可供性、人类意图和人体工程学信息，为生成过程提供物理层面的引导信号。

这一设计使得模型能够从文本描述中更忠实地还原动态交互，而非仅仅生成“看起来合理”的并置运动。

## 核心创新

HOIAnimator 的核心创新在于将文本驱动的人-物交互动画生成从“单一共享模型”范式推进到“解耦感知与物理约束协同”的新范式。其创新并非简单的模块堆砌，而是围绕一个核心洞察展开：**将HOI动画生成分解为人类和物体两条扩散流，并通过感知消息传递（PMP）与交互接触场（ICF）实现双向适配与物理约束，让模型从文本中更忠实地还原动态交互。**

这一洞察直接回应了现有方法的瓶颈——难以同时精确建模人类运动、物体动态以及两者间的接触与力交互。以下从三个关键的 changed slots 剖析其创新点。

### 1. 从单一扩散到双感知扩散模型（PDM）

**基线状态**：现有方法（如 **MDM**，Tevet et al., ICLR 2023）采用单一Transformer扩散模型，将人与物体的运动序列统一编码、统一去噪。这种共享架构隐含假设人与物体的运动模式服从相同的分布特性，但实质上人类运动具有高度铰接性和意图性，而物体运动则受限于刚体动力学和可供性，二者的生成需求存在本质差异。

**创新方案**：HOIAnimator 提出 **Perceptive Diffusion Models (PDM)**，将生成过程解耦为**人类中心扩散模型**（$G^H$）与**物体中心扩散模型**（$G^O$）两个专门化分支。每个分支以文本条件和扩散步数为输入，独立预测各自序列的去噪输出：

$$\hat{\boldsymbol{x}}_{obj} = \boldsymbol{G}^O \big( E_{hoi}(x_{obj}), E_{text}(text) + E_{step}(t) \big)$$
$$\hat{\boldsymbol{x}}_{hum} = \boldsymbol{G}^H \big( E_{hoi}(x_{hum}), E_{text}(text) + E_{step}(t) \big)$$

这种解耦使模型能够为人与物分别学习适配的运动先验，而非强制共享一个折中的表示空间。消融实验（Table 2）证实，将PDM替换为单一扩散模型（w/o PDM）后，整体性能显著下降，验证了双分支架构的必要性。

### 2. 从无通信到感知消息传递（PMP）

**基线状态**：即使部分工作采用多分支架构，跨实体的信息交换通常缺失或仅依赖隐式的共享编码器。这导致人类与物体的生成过程彼此孤立，缺乏对交互动态的协同感知。

**创新方案**：HOIAnimator 设计了 **Perceptive Message Passing (PMP)** 机制，实现人类与物体扩散模型间的**双向、自适应通信**。PMP 包含两个关键操作：

- **对象通道（Object Passage）**：利用物体隐编码动态调节人类隐编码，通过可学习的权重和偏置实现条件特征变换：
  $$\mathbf{h}' = F_{obj}(\mathbf{h}|\varphi, \phi), \quad \varphi = L_w(\mathbf{o}) \cdot \mathbf{h} + L_b(\mathbf{o})$$
  这使得物体状态（如位置、朝向）能够显式地“告知”人类模型当前的交互上下文。

- **双流聚合（Dual Flow）**：在对象通道之后，对人类与物体特征进行双向自注意力与残差集成：
  $$<\hat{\mathbf{h}}, \hat{\mathbf{o}}> = F_{dual}(<{\mathbf{o}}', {\mathbf{h}}'>, <{\mathbf{h}}', {\mathbf{o}}'>) \oplus <{\mathbf{o}}', {\mathbf{h}}'>$$
  双流设计确保信息不是单向流动，而是形成闭环——人类运动影响物体响应，物体状态反作用于人类动作。

消融实验（Figure 5, Table 2）表明，移除PMP后，虽然人与物体的空间排布尚可，但**缺乏真实的交互动感**，生成的动画沦为静态摆放而非动态协同。这证明PMP是赋予动画“交互生命力”的关键组件。

### 3. 从无接触模型到交互接触场（ICF）

**基线状态**：传统方法要么完全忽略接触建模，要么仅依赖简单的距离阈值或碰撞检测，缺乏对“何处可能接触、以何种方式接触”的概率性理解。

**创新方案**：HOIAnimator 引入 **Interaction Contact Field (ICF)**，这是一个从文本条件学习接触概率分布的显式物理先验模块。ICF 的核心设计体现在三个层面：

- **接触表示**：通过计算人类与物体采样顶点间的最近距离场 $\mathbf{D}_{<h,o>}$，隐式编码接触、穿透和邻近信息：
  $$C_h[j] = \parallel v_h[j] - v_o[i] \parallel_2, \quad C_o[i] = \parallel v_o[i] - v_h[j] \parallel_2$$

- **概率化建模**：ICF 并非硬性规定接触点，而是综合**物体可供性、人类意图和人体工程学**学习一个接触概率分布。这使得模型能够预测“手可能握住杯柄”而非“手穿透杯壁”的合理交互区域。

- **生成引导**：预训练的ICF扩散模型 $G^I$ 从文本生成预测接触场 $\hat{\mathbf{D}}_h, \hat{\mathbf{D}}_o$，随后通过交叉注意力机制将其嵌入HOI动画生成的隐变量中：
  $$\mathbf{o} = Attn(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = softmax(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}})\mathbf{V}, \quad \mathbf{Q} = \mathbf{W}^Q \hat{\mathbf{D}}_o$$

消融实验（Table 2, Figure 5）提供了决定性证据：移除ICF后，生成的动画出现**明显的不真实穿透**。这验证了ICF在约束物理合理性方面的不可替代性。

### 创新协同效应

三个 changed slots 并非孤立创新，而是形成因果闭环：**PDM 提供解耦的生成空间，PMP 建立跨实体通信，ICF 注入物理约束**。完整配置在 BEHAVE 数据集上取得了 Top-3 精度 0.781、FID 0.623 的最优结果（Table 2），且穿透度指标（0.643）相比 InterGen（0.613）提升 3%，证明联合创新在语义匹配、运动质量和物理真实性三个维度均带来增益。

## 整体框架

HOIAnimator 的整体框架围绕一个核心洞察展开：**将文本驱动的人-物交互（HOI）动画生成分解为两条独立的扩散流，并通过显式的感知通信与接触场引导实现双向适配**。如图3所示，pipeline 由两大关键组件构成：感知扩散模型（Perceptive Diffusion Models, PDM）和交互接触场（Interaction Contact Field, ICF）。

### 统一表示与输入流

框架首先将 HOI 动画建模为一个统一的参数化表示。对于每一帧 i，动画状态定义为一个 175 维向量：

$$x_{1:i} = \{\beta, \theta, \tau, \gamma\}, \quad x_i \in \mathbb{R}^{175}$$

其中 $\beta \in \mathbb{R}^{10}$ 为人体形状参数，$\theta \in \mathbb{R}^{159}$ 为人体姿态参数，$\tau \in \mathbb{R}^3$ 为物体的平移参数，$\gamma \in \mathbb{R}^3$ 为物体的旋转参数。这一统一表示作为整个 pipeline 的输入，同时承载人类运动和物体动态的信息。

### 双分支感知扩散模型（PDM）

PDM 是框架的生成核心，包含两个专门化的扩散模型分支：

- **物体中心扩散模型**（Object Centric Diffusion Model, $G^O$）：负责从噪声中恢复物体的运动序列。
- **人类中心扩散模型**（Human Centric Diffusion Model, $G^H$）：负责从噪声中恢复人类的运动序列。

两个分支均以文本嵌入和扩散步数编码作为共享条件。具体而言，HOI 编码器 $E_{hoi}$ 将原始动画序列映射为隐变量，文本编码器 $E_{text}$（冻结的 CLIP ViT-B/32 + 2 层 Transformer）提取语义特征，扩散步数编码器 $E_{step}$ 注入当前去噪阶段信息。两个分支的干净动画预测可形式化为：

$$\hat{x}_{obj} = G^O(E_{hoi}(x_{obj}), E_{text}(text) + E_{step}(t))$$

$$\hat{x}_{hum} = G^H(E_{hoi}(x_{hum}), E_{text}(text) + E_{step}(t))$$

训练时，整体扩散损失为人类和物体序列重建的 L2 损失之和：

$$\mathcal{L} = \mathcal{L}_{human} + \mathcal{L}_{obj} = \mathbb{E}_{t \sim [1:T]}[\|x_{hum} - \hat{x}_{hum}\|_2 + \|x_{obj} - \hat{x}_{obj}\|_2]$$

这种解耦设计的关键优势在于：它允许人类运动和物体运动在各自的表示空间中被精细化建模，而非被强行压缩到一个共享的隐空间中——这正是单一扩散模型基线（如 **MDM**, Tevet et al., ICLR 2023）在处理复杂交互时性能受限的瓶颈所在。

### 感知消息传递（PMP）

两条扩散分支并非独立运行。PMP 机制作为它们之间的通信桥梁，通过两个子模块实现双向信息交换：

1. **对象通道**（Object Passage）：利用物体隐编码 $o$ 动态调节人类隐编码 $h$，通过可学习的权重和偏置实现自适应调制：
   $$\mathbf{h}' = F_{obj}(\mathbf{h}|\varphi, \phi), \quad \varphi = L_w(\mathbf{o}) \cdot \mathbf{h} + L_b(\mathbf{o})$$
   其中 $L_w$ 和 $L_b$ 是从物体隐编码中学习到的线性变换，分别生成权重和偏置。这意味着物体当前的运动状态会直接影响人类运动特征的表达方式。

2. **双流聚合**（Dual Flow）：对人类和物体的隐特征进行双向交叉聚合，并通过残差加法得到最终的融合隐变量：
   $$<\hat{\mathbf{h}}, \hat{\mathbf{o}}> = F_{dual}(<\mathbf{o}', \mathbf{h}'>, <\mathbf{h}', \mathbf{o}'>) \oplus <\mathbf{o}', \mathbf{h}'>$$
   其中 $F_{dual}$ 对两对特征分别执行自注意力后拼接，$\oplus$ 表示逐元素残差加法。双流设计确保了两条分支的信息能够对称地相互影响，而非单向传递。

### 交互接触场（ICF）引导

ICF 为整个生成过程提供物理约束信号。它首先计算人类与物体采样顶点间的最近距离场：

$$\mathbf{D}_{<h,o>} = F_{ICF}(C_{<h,o>}, sample(v_{<o,h>}, N))$$

其中 $C_h[j] = \|v_h[j] - v_o[i]\|_2$ 和 $C_o[i] = \|v_o[i] - v_h[j]\|_2$ 分别刻画了人体顶点到最近物体顶点的距离，以及物体顶点到最近人体顶点的距离。这一距离场隐式地编码了接触与穿透信息。

随后，一个预训练的扩散模型从文本和步数条件中生成预测的交互接触场：

$$<\hat{\mathbf{D}}_h, \hat{\mathbf{D}}_o> = G^I(\mathbf{D}_{<h,o>}, E_{text}(text) + E_{step}(t))$$

最后，通过交叉注意力机制将预测的接触场嵌入到 HOI 动画生成的隐特征中：

$$\mathbf{o} = Attn(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = softmax(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}})\mathbf{V}$$

其中 $\mathbf{Q} = \mathbf{W}^Q \hat{\mathbf{D}}_o$，$\mathbf{K} = \mathbf{W}^K \mathbf{L}$，$\mathbf{V} = \mathbf{W}^V \mathbf{L}$。ICF 的独特之处在于其**概率化建模**——它综合了物体可供性（object affordance）、人类意图（human intent）和人体工程学（ergonomics）信息，学习的是接触的概率分布，而非简单的几何距离阈值。这使得模型能够预测“可能发生交互”的区域，即使这些区域在当前帧中尚未产生直接接触。

### 输出流与端到端流程

整个 pipeline 的端到端流程如下：
1. 输入文本通过冻结的 CLIP 编码器提取语义特征。
2. 随机噪声在人类和物体两条扩散分支中被逐步去噪，PMP 在每一层进行双向特征交换。
3. ICF 从文本中预测接触概率分布，并通过交叉注意力注入去噪过程。
4. 双分支隐解码器将融合后的隐变量解码为最终的动画序列。

消融实验（Table 2）验证了这一框架中各模块的因果作用：完整配置在 Top-3 精度（0.781）、FID（0.623）和穿透度（0.643）三项指标上均取得最优。移除 ICF 导致出现明显的不真实穿透；移除 PMP 后虽能保持人与物体的空间排布，但缺乏真实的交互动感；使用单一扩散模型替代 PDM 则整体性能全面下降。这些证据共同表明，PDM 的解耦设计、PMP 的双向通信和 ICF 的物理引导三者缺一不可。

### 补充图表

![[assets/figures/papers/paper_list_l1717_HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel/figures/003_Figure_3.jpg]]
*Figure 3: Method overview. We propose the HOIAnimator with two key parts: (1) Perceptive Diffusion Models (PDM). This part combines the movements of both people and objects in the animation, making sure they move together in a realistic way. (2) Interaction Contact Field (ICF). The ICF provides the clues that humans and objects interact and contact each other (Training phase of HOIAnimator)*

## 核心模块与公式推导

### 统一动画表示

HOIAnimator 将人-物交互动画统一表示为一个 175 维的状态向量（Section 3.2），其中包含四个关键参数：

- **人体形状参数** $\beta \in \mathbb{R}^{10}$
- **人体姿态参数** $\theta \in \mathbb{R}^{159}$
- **物体平移参数** $\tau \in \mathbb{R}^3$
- **物体旋转参数** $\gamma \in \mathbb{R}^3$

第 $i$ 帧的动画状态记为 $x_i \in \mathbb{R}^{175}$，完整序列表示为 $x_{1:i} = \{\beta, \theta, \tau, \gamma\}$。这一统一表示使得人体运动与物体动态能够被纳入同一扩散框架中处理。

### 扩散前向过程

系统采用标准的 Markov 加噪过程，逐步向真实 HOI 动画序列添加高斯噪声（Equation 1）：

$$q(x_{1:i}^t | x_{1:i}^{t-1}) = \mathcal{N}(\sqrt{1 - \alpha_t} x_{1:i}^{t-1}, \alpha_t \mathbf{I})$$

其中 $\alpha_t$ 控制第 $t$ 步的噪声强度。该过程将干净动画逐步破坏为纯噪声，为后续的去噪生成提供训练基础。

### 感知扩散模型（PDM）

与传统单一扩散模型不同，HOIAnimator 采用双分支感知扩散模型（Section 3.3），分别处理人体和物体序列：

- **物体中心扩散模型** $G^O$：预测物体动画序列的去噪结果
- **人体中心扩散模型** $G^H$：预测人体运动序列的去噪结果

两个模型均以文本编码和扩散步数编码的加和作为条件输入：

$$\hat{x}_{obj} = G^O(E_{hoi}(x_{obj}), E_{text}(text) + E_{step}(t))$$

$$\hat{x}_{hum} = G^H(E_{hoi}(x_{hum}), E_{text}(text) + E_{step}(t))$$

其中 $E_{hoi}$ 为 HOI 编码器（2 层线性结构，隐空间维度 1024），$E_{text}$ 为文本编码器（冻结 CLIP ViT-B/32 + 2 层 Transformer），$E_{step}$ 为扩散步数编码器。训练损失为人体和物体序列重建 L2 损失的均值（Equation 3）：

$$\mathcal{L} = \mathcal{L}_{human} + \mathcal{L}_{obj} = \mathbb{E}_{t \sim [1:T]} [\|x_{hum} - \hat{x}_{hum}\|_2 + \|x_{obj} - \hat{x}_{obj}\|_2]$$

### 感知消息传递（PMP）

PMP 机制是实现双分支协同的核心（Section 3.3，Figure 4），包含两个关键组件：

![[assets/figures/papers/paper_list_l1717_HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel/figures/004_Figure_4.jpg]]
*Figure 4: Perceptive Message Passing. Between object and human centric diffusion models, we use object passage and dual flow to adjust the features of humans and objects dynamically*

**对象通道（Object Passage）**：利用物体隐编码 $\mathbf{o}$ 动态调节人体隐编码 $\mathbf{h}$（Equation 4）：

$$\mathbf{h}' = F_{obj}(\mathbf{h} | \varphi, \phi), \quad \varphi = L_w(\mathbf{o}) \cdot \mathbf{h} + L_b(\mathbf{o})$$

其中 $L_w$ 和 $L_b$ 为可学习的线性变换，分别从物体隐编码中生成权重和偏置，实现对人体特征的逐元素自适应调制。

**双流聚合（Dual Flow）**：对人体与物体隐特征进行双向特征聚合，并通过残差加法得到最终隐变量（Equation 5）：

$$\langle \hat{\mathbf{h}}, \hat{\mathbf{o}} \rangle = F_{dual}(\langle \mathbf{o}', \mathbf{h}' \rangle, \langle \mathbf{h}', \mathbf{o}' \rangle) \oplus \langle \mathbf{o}', \mathbf{h}' \rangle$$

$F_{dual}$ 对拼接后的特征对执行自注意力操作，$\oplus$ 为逐元素残差加法。这一设计使得人体和物体的隐表示能够双向感知对方的状态，从而在去噪过程中协同演化。

### 交互接触场（ICF）

ICF 是显式建模人-物物理接触的核心模块（Section 3.4），通过概率分布刻画交互接触区域。

**接触距离计算**：首先对人体和物体顶点进行采样，计算最近距离场：

$$C_h[j] = \|v_h[j] - v_o[i]\|_2, \quad C_o[i] = \|v_o[i] - v_h[j]\|_2$$

$$\mathbf{D}_{<h,o>} = F_{ICF}(C_{<h,o>}, sample(v_{<o,h>}, N))$$

其中 $v_h$、$v_o$ 分别为人体和物体顶点，$N$ 为采样点数。该距离场同时捕获接触和穿透信息。

**ICF 扩散预测**：预训练一个独立的扩散模型 $G^I$，从文本和步数生成预测的交互接触场：

$$\langle \hat{\mathbf{D}}_h, \hat{\mathbf{D}}_o \rangle = G^I(\mathbf{D}_{<h,o>}, E_{text}(text) + E_{step}(t))$$

ICF 综合了物体可供性（affordance）、人类意图和人体工程学信息，以概率分布的形式预测潜在交互点。

**ICF 交叉注意力嵌入**：通过交叉注意力将预测的接触场融入 HOI 动画生成的隐特征中（Section 3.4）：

$$\mathbf{o} = Attn(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = softmax\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\mathbf{V}$$

$$\mathbf{Q} = \mathbf{W}^Q \hat{\mathbf{D}}_o, \quad \mathbf{K} = \mathbf{W}^K \mathbf{L}, \quad \mathbf{V} = \mathbf{W}^V \mathbf{L}$$

其中 $\mathbf{W}^Q \in \mathbb{R}^{d_q \times d_k}$、$\mathbf{W}^K, \mathbf{W}^V \in \mathbb{R}^{d_s \times d_k}$ 为可训练投影矩阵，$\mathbf{L}$ 为 HOI 动画生成的隐特征。该机制使 ICF 作为物理约束信号引导生成过程，确保接触区域的几何合理性。

### 模块间协同机制

PDM、PMP 与 ICF 三者形成闭环协同：PMP 实现人体与物体扩散模型间的双向信息交换，使两个分支在去噪过程中保持运动协调；ICF 则以接触概率分布的形式提供物理约束，通过交叉注意力嵌入到隐空间中。消融实验（Table 2）表明，完整配置在 Top-3 精度（0.781）、FID（0.623）和穿透度（0.643）上均取得最优结果，移除任一组件均导致性能下降——移除 ICF 后出现明显的不真实穿透，移除 PMP 后缺乏真实的交互动感，替换为单一扩散模型（w/o PDM）后整体性能降低。

## 实验与分析

### 实验设置

HOIAnimator 在 **BEHAVE** 和 **InterCap** 两个数据集上进行训练与评估。所有动画序列被统一标准化为 30 FPS，时长控制在 6 到 10 秒之间。评估体系涵盖六项指标：**FID**（Fréchet Inception Distance）衡量生成分布与真实分布的距离；**R Precision** 与 **Top-3 Precision** 评估文本-动作的语义匹配精度；**Diversity** 与 **MM Dist**（Multi-Modal Distance）分别度量生成结果的多样性与多模态匹配程度；**Vertex Distance** 计算人体与物体网格最近顶点间的平均距离，反映空间关系的合理性；**Penetration** 则量化人体与物体之间的穿透程度。所有主实验均基于 20 次独立运行的平均值，并报告 95% 置信区间，确保统计可靠性。

### 主实验结果

在 BEHAVE 数据集上的定量对比（Table 1）显示，HOIAnimator 在语义匹配与物理合理性两个维度上均显著优于现有基线。与同期最强的交互生成方法 **InterGen**（Liang et al., arXiv 2023）相比，HOIAnimator 的 Top-3 Precision 从 0.734 提升至 **0.781**（+0.047），FID 从 0.717 降至 **0.623**（-0.094），Vertex Distance 从 0.523 大幅降至 **0.118**（-0.405），表明生成的人-物空间关系更加贴近真实数据。在 Penetration 指标上，HOIAnimator 达到 0.643，优于 InterGen 的 0.613（+0.030），说明穿透现象得到一定程度的缓解。此外，HOIAnimator 在 R Precision（Top-1/Top-2/Top-3）、Diversity 和 MM Dist 等指标上也全面领先于 **MDM**（Tevet et al., ICLR 2023）和 **PriorMDM**（Shafir et al., arXiv 2023）等文本驱动运动生成基线。

![[assets/figures/papers/paper_list_l1717_HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation on BEHAVE [3]. To ensure a fair comparison, we conducted 20 experiments*

这些结果表明，双分支感知扩散模型（PDM）与交互接触场（ICF）的联合设计，使得模型不仅能够准确理解文本语义，还能有效约束人与物体之间的空间接触关系，从而生成更协调的交互动画。

### 消融实验

为验证各组件的独立贡献，论文进行了系统的消融实验（Table 2 与 Figure 5），逐一移除 PDM、PMP 和 ICF，考察对 Top-3 Precision、FID 和 Penetration 三项核心指标的影响。

![[assets/figures/papers/paper_list_l1717_HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel/figures/007_Table_2.jpg]]
*Table 2: Ablation study. We show precision (Top-3), FID, and penetration. Our configuration can achieve the best results*

![[assets/figures/papers/paper_list_l1717_HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel/figures/006_Figure_5.jpg]]
*Figure 5: Ablation study. Our model generates HOI animations from text descriptions. Simultaneously, we apply*

- **完整模型（Ours）** 在所有指标上取得最优结果（Precision: 0.781, FID: 0.623, Penetration: 0.643），验证了三个组件的联合有效性。
- **移除 ICF（w/o ICF）** 后，生成的动画出现明显的不真实穿透。如 Figure 5 中黄色箭头所示，人体与物体之间发生严重的几何交叉，说明 ICF 提供的接触概率场对于维持物理合理性至关重要。
- **移除 PMP（w/o PMP）** 后，虽然人与物体的空间排布尚可，但缺乏真实的交互动感。这意味着 PMP 的双向消息传递机制是驱动动态协调的关键——没有它，模型退化为两个近乎独立的运动生成器。
- **使用单一扩散模型替代 PDM（w/o PDM）** 后，整体性能全面下降。这证实了人类与物体运动模式的本质差异需要由各自专用的扩散分支来处理，单一共享模型难以同时捕捉两者的动态特性。

### 定性分析

Figure 6 展示了 HOIAnimator 与基线方法的定性对比。对于给定的文本描述，只有 HOIAnimator 能够准确描绘人与物体的空间关系和动态交互——例如“弯腰捡起盒子”时手部与盒子的接触区域、身体姿态的自然过渡等。其他基线方法要么无法建立有效的接触，要么产生不自然的姿态偏移。Figure 5 的消融可视化进一步佐证了这一点：移除 ICF 或 PMP 后，交互区域的错误（如手部穿透物体、物体悬空等）显著增加。

![[assets/figures/papers/paper_list_l1717_HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative evaluation. We present zoomed-in details highlighted within black boxes. For any specified text description, only our HOIAnimator is capable of accurately depicting the spatial relationships and the dynamic interactions involved*

### 用户研究

Figure 7 报告了用户研究结果。参与者在观看不同方法生成的动画后，从交互真实感、语义一致性和整体质量三个维度进行评分。HOIAnimator 在各项评分上均获得最高比例的高分评价，进一步验证了其在人-物交互动画生成任务上的主观优势。

![[assets/figures/papers/paper_list_l1717_HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel/figures/008_Figure_7.jpg]]
*Figure 7: User study. The color bars in the figure indicate the percentage of the scores. The X-axis represents the number of participants*

### 失败模式与局限性

尽管 HOIAnimator 在 BEHAVE 基准上取得了领先性能，论文也明确指出以下局限：

1. **复杂动作序列**：当前方法难以处理涉及多个连续子动作的长序列交互（如“拿起杯子→喝水→放下杯子”），模型缺乏对时序因果链的显式建模。
2. **多物体交互**：不支持同一人体同时与多个物体交互的场景，双分支架构在物体数量扩展上存在天然瓶颈。
3. **非刚性物体**：由于缺乏变形先验，HOIAnimator 无法生成涉及布料、液体等非刚性物体的动画，限制了其在更广泛交互场景中的应用。
4. **计算开销**：ICF 的预训练扩散模型与主生成模型的联合推理增加了计算负担，论文未讨论实时性表现，实际部署时可能存在延迟问题。

> **注意**：关于 ICF 在更复杂物理先验下的泛化能力，以及在动态场景数据集上的鲁棒性，论文仅作为开放问题提出，尚无实验证据支持，需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l1717_HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel/figures/001_Figure_1.jpg]]
*Figure 1: Our HOIAnimator excels in turning text descriptions into realistic animations of human-object interactions. It’s adept at depicting a variety of actions, such as bending, lifting boxes, and picking up bags, with believable contact between the human and the objects*

![[assets/figures/papers/paper_list_l1717_HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel/figures/002_Figure_2.jpg]]
*Figure 2: Navigating the complexity of HOIAnimator. (A): the ‘static’ interaction is depicted with a stationary office chair, showcasing a human sitting on the chair. (B): the ‘dynamic’ interaction portrays both the human and the object in motion, exemplified by the act of holding an object. (C): Arrows denote forces and trajectories involved in HOI*

## 方法谱系与知识库定位

### 问题定位与基线关系

HOIAnimator 聚焦于**文本驱动的人-物交互动画生成**这一新兴任务。该任务的核心瓶颈在于：现有方法难以在统一的生成框架内同时精确建模人类运动、物体动态以及两者间的接触与力交互，导致生成的动画缺乏物理真实感和交互协调性。

在方法谱系上，HOIAnimator 直接承袭了**基于扩散模型的运动生成**这一技术路线。其最直接的基线包括：

- **MDM** (Tevet et al., ICLR 2023)：经典的文本到运动扩散模型，采用单一 Transformer 架构处理人体运动序列。HOIAnimator 将其作为单分支扩散模型的代表，在架构上进行了根本性扩展——从单一人体运动建模走向人-物双实体协同建模。
- **PriorMDM** (Shafir et al., arXiv 2023)：基于扩散模型的运动生成先验方法，同样受限于单一实体的运动生成范式。
- **InterGen** (Liang et al., arXiv 2023)：面向多人交互生成的扩散模型，是 HOIAnimator 在 BEHAVE 数据集上的主要对比对象。InterGen 虽然处理交互场景，但其关注点在于多人之间的交互，而非人与物体的动态协调。

HOIAnimator 相对于上述基线的关键改进体现在三个维度：

1. **架构层面**：从单一扩散模型扩展为**双感知扩散模型（PDM）**，分别设有人类中心扩散模型 $G^H$ 和物体中心扩散模型 $G^O$，使两个实体各自拥有专门的生成通路。
2. **通信机制**：引入**感知消息传递（PMP）** 机制，通过对象通道（object passage）和双流（dual flow）实现人类与物体扩散模型间的双向信息交换，这是基线方法中不存在的显式跨实体通信能力。
3. **接触建模**：提出**交互接触场（ICF）**，从文本中学习人与物体的接触概率分布，综合物体可供性、人类意图和人体工程学信息，替代了基线方法中无显式接触模型或仅依赖距离碰撞检测的粗糙做法。

### 适用边界与能力范围

HOIAnimator 在以下条件下展现出较强的生成能力：

- **交互类型**：覆盖静态交互（如坐在椅子上）和动态交互（如拿起箱子），能够生成具有可信接触的人-物动画序列。
- **数据格式**：采用统一的人-物动画表示 $x_{1:i} = \{\beta, \theta, \tau, \gamma\}$，其中人体参数包括形状 $\beta \in \mathbb{R}^{10}$ 和姿态 $\theta \in \mathbb{R}^{159}$，物体参数包括平移 $\tau \in \mathbb{R}^3$ 和旋转 $\gamma$，每帧共计 175 维。
- **数据来源**：基于 BEHAVE 和 InterCap 数据集训练，序列标准化为 30 FPS，时长 6-10 秒。
- **文本编码**：使用冻结的 CLIP ViT-B/32 加 2 层 Transformer 编码器提取文本特征。

### 局限性与已知失效模式

根据论文披露和实验证据，HOIAnimator 存在以下明确局限：

1. **复杂动作序列**：当前方法难以处理包含多个子动作的复杂序列（如连续拿起、放下不同物体），生成能力局限于单次交互。
2. **多物体交互**：不支持多个物体同时与人体交互的场景，模型设计以单一人-物对为基本单元。
3. **非刚性物体**：无法生成涉及非刚性物体（如水流、布料）的动画，缺乏对物体变形的物理先验建模。
4. **计算开销**：交互接触场与扩散模型的联合训练增加了计算复杂度，论文未讨论实时性表现。

消融实验进一步揭示了各组件的失效模式（Table 2, Figure 5）：
- **移除 ICF**：生成的动画出现明显的不真实穿透，表明 ICF 在物理合理性约束中起关键作用。
- **移除 PMP**：虽然人与物体的空间排布尚可，但缺乏真实的交互动感，说明 PMP 是动态协调的核心。
- **使用单一扩散模型（w/o PDM）**：整体性能下降，验证了双分支架构的必要性。

### 开放问题与未来方向

论文提出的开放问题指向以下潜在研究方向：

1. **序列化交互生成**：如何将 HOIAnimator 扩展到复杂交互序列（如连续拿起、放下不同物体）的生成，需要在时序依赖建模和交互状态转移方面进行扩展。
2. **多物体协同交互**：如何支持多物体同时与人体交互，这涉及更复杂的接触场建模和多实体消息传递机制。
3. **非刚性物体集成**：如何集成非刚性物体的物理变形模型（如布料、液体），以扩展交互场景的覆盖范围。
4. **物理先验增强**：ICF 建模的接触概率分布是否可以通过更强的物理先验（如接触力学、摩擦模型）进一步提升真实性。
5. **跨场景鲁棒性**：在更广泛的真实场景数据集（如与动态场景结合）上，方法是否仍能保持鲁棒性，需要更多样化的评测基准来验证。

需要注意的是，上述开放问题均来自论文自身的讨论，目前尚无后续工作直接解决这些局限。若需了解该方向的最新进展，建议追踪基于物理的交互生成和神经辐射场/3D 高斯泼溅与扩散模型结合的相关工作。

## 原文 PDF

![[paperPDFs/CVPR_2024/HOI_Animator_Generating_Text_Prompt_Human_Object_Animations_using_Novel_Perceptive_Diffusion_Models.pdf]]