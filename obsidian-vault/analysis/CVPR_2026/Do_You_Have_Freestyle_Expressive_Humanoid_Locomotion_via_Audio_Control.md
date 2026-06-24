---
title: Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Audio_Control.pdf
project_link: null
code_link: null
aliases:
- DYHFEHLAC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将原始音频作为隐式风格信号，通过音频-运动对齐模块注入运动学先验，并直接条件化扩散策略生成动作，从而绕过运动重定向步骤。
primary_logic: 运动可分解为内容（高层语义描述）与风格（音频信号），通过教师-学生框架在潜在空间中融合两者，实现高效、低延迟的音频到动作映射。
claims:
- RoboPerform在BEAT2和FineDance数据集上均取得了较高的任务成功率，同时关节和关键点误差较低。
- ∆MoE教师策略相比普通MoE在所有基准上均显著提升跟踪准确性。
- 音频适配器成功对齐音频与运动，大幅提升跟踪成功率和节奏对齐。
- BEAT2 (IsaacGym) 上 Succ ↑ = 0.99
---

# Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control

> [!tip] 核心洞察
> 运动可分解为内容（高层语义描述）与风格（音频信号），通过教师-学生框架在潜在空间中融合两者，实现高效、低延迟的音频到动作映射。

| 字段 | 内容 |
|------|------|
| 中文题名 | 你有即兴风格吗？通过音频控制的富有表现力的人形机器人运动 |
| 英文题名 | Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.23650) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RoboPerform |
| Dataset | BEAT2, FineDance |

> [!tip] 效果简介
> - BEAT2 (IsaacGym) 上，Succ ↑ 0.99 vs 0.98 (+0.01)；E_mpjpe ↓ 0.05 vs 0.07 (-0.02)。
> - FineDance (IsaacGym) 上，Succ ↑ 0.93 vs 0.88 (+0.05)；E_mpjpe ↓ 0.18 vs 0.24 (-0.06)。
> - BEAT2 (MuJoCo) 上，Succ ↑ 0.96 vs 0.94 (+0.02)。

## 概述

**核心问题**：现有音频驱动人形机器人管线依赖“显式运动生成→重定向→策略跟踪”的级联架构。这一范式引入多重误差累积、高推理延迟，且声学信号与物理执行之间耦合松散，难以实现即兴、节奏对齐的全身表现力运动。

**核心洞察与因果机制**：RoboPerform 将运动分解为**内容**（高层语义，如“一个人在跳舞”）与**风格**（音频信号本身），通过教师-学生框架在潜在空间中融合两者。关键因果调节变量是**绕过显式重定向**——以对齐后的音频潜在变量作为隐式风格信号，直接条件化扩散策略生成关节动作，从而切断级联误差链。

**方法定位**：
- **方法名**：RoboPerform
- **方法谱系**：属于**音频条件化的隐式运动生成+扩散策略**范式，区别于传统的“生成-重定向-跟踪”管线（如 EMAGE / FineNet → 重定向 → MLP 策略）。
- **知识库定位**：在**全身表现力运动合成**、**音频-运动跨模态对齐**、**混合专家策略蒸馏**三个方向的交叉点上引入新机制。

**主要结果**（仿真环境）：
- 在 BEAT2 (IsaacGym) 上，成功率 **0.99**，平均关节位置误差 **0.05**，均优于基线（0.98 / 0.07）。
- 在 FineDance (IsaacGym) 上，成功率 **0.93**，平均关节位置误差 **0.18**，较基线（0.88 / 0.24）提升显著。
- 在 MuJoCo 环境下同样保持优势，FineDance 成功率从 0.61 提升至 **0.67**。

**消融关键发现**：
- ∆MoE（残差混合专家）教师策略在所有基准上一致优于普通 MoE（Table 3）。
- 音频适配器是对齐音频与运动模态的关键组件，移除后性能大幅下降（Table 5）。
- 内容潜在变量的引入显著改善跟踪性能，验证了内容-风格分解的有效性（Table 4）。

**局限与待验证点**：
- 当前验证仅限于 Unitree G1 人形机器人，跨形态泛化性未知。
- 音频适配器依赖配对数据训练，对域外音频风格的泛化能力需进一步检验。
- 实时部署中 18–30ms 的通信延迟可能制约极高动态动作的响应速度。

## 背景与动机

### 问题背景

赋予人形机器人富有表现力的全身运动能力，使其能够像人类一样随音乐起舞或伴随语音做出自然手势，是具身智能领域的长期目标。这一能力不仅要求机器人产生物理上可行的动作，还要求动作在时间上与音频节拍精确对齐，在风格上与音频的情感或节奏特征保持一致。然而，现有方法在实现这一目标时面临根本性瓶颈。

### 现有方法的级联误差困境

当前主流的音频驱动人形机器人管线采用显式多阶段流水线：首先使用预训练模型（如 **EMAGE** 或 **FineNet** ）从音频生成显式人体运动序列，然后通过运动重定向（retargeting）将人体运动映射到目标机器人构型，最后训练一个 MLP 策略来跟踪这些重定向后的运动目标。

这一范式存在三个核心缺陷：

1. **级联误差积累**：音频生成运动、运动重定向、策略跟踪三个环节各自引入误差，且误差在管线中逐级放大。运动生成模型可能产生物理不可行的动作，重定向过程进一步引入关节映射偏差，最终导致跟踪策略无法准确执行。

2. **高推理延迟**：显式管线需要在每个环节进行前向推理，特别是运动生成和重定向步骤增加了显著的延迟，难以满足实时交互需求。

3. **声学与执行的松散耦合**：音频信号仅用于生成初始运动目标，一旦运动序列生成完毕，音频的节奏和风格信息便不再参与后续的动作执行过程。这意味着当面对未见过的音频时，系统无法即兴调整动作风格以匹配音频特征，缺乏“即兴风格”（freestyle）能力。

### 核心动机：从显式重建到隐式风格控制

本文的动机源于一个关键观察：**运动可分解为内容与风格**。其中，“内容”指运动的高层语义描述（如“一个人正在跳舞”），而“风格”则由音频信号提供——音乐的节拍、旋律、能量，或语音的韵律、情感等特征。现有方法将音频视为运动生成的内容输入，试图从音频中重建完整运动；但更本质的视角是将音频作为风格信号，直接调制运动表达。

基于这一洞察，RoboPerform 提出绕过显式运动生成和重定向步骤，将原始音频作为隐式风格控制信号，通过音频-运动对齐模块注入运动学先验，并直接条件化扩散策略生成机器人关节动作。这一范式转换从根本上消除了级联误差的积累路径，同时实现了低延迟、节奏对齐的即兴表演能力。

## 核心创新

RoboPerform 的核心创新在于**将音频从显式运动生成的中间产物重新定义为隐式风格控制信号**，从而绕过了传统管线中“音频→显式运动生成→重定向→策略跟踪”的级联结构。这一转变由三个紧密耦合的 *changed slots* 实现，它们共同构成了一个低延迟、高节奏对齐的音频驱动人形机器人运动框架。

### 1. 音频到动作的直接生成模式

**Baseline** 采用常规管线：先用预训练模型（如 **EMAGE** 、**FineNet** ）从音频生成显式人体运动序列，再将运动重定向到目标机器人（Unitree G1），最后由一个基于 MLP 的策略进行跟踪执行。这一流程存在三个固有瓶颈：① 级联误差在生成、重定向、跟踪三个阶段逐步积累；② 推理延迟高，难以满足实时交互需求；③ 声学信号与最终执行之间耦合松散，即兴表现力受限。

**RoboPerform** 则完全取消了显式运动生成与重定向步骤。其核心思路是训练一个**音频-运动适配器**（Audio-Motion Adaptor），通过 InfoNCE 对比损失（Equation 1）将音频潜在变量 $l_{\mathrm{audio}}$ 对齐到运动潜在空间：

$$\mathcal{L}_{\mathrm{InfoNCE}} = -\frac{1}{N} \sum_{i=1}^{N} \log \frac{\exp(\sin(l_{\mathrm{audio}}^{(i)}, l_{\mathrm{motion}}^{(i)}))}{\sum_{j=1}^{N} \exp(\sin(l_{\mathrm{audio}}^{(i)}, l_{\mathrm{motion}}^{(j)}))}$$

对齐后的音频潜在变量直接作为条件输入到扩散学生策略中，去噪生成最终的关节动作。这一设计使得音频信号从“生成运动目标”变为“直接驱动动作”，从根本上消除了重定向误差和级联延迟（Section 3.3, 4.3）。

### 2. 风格控制注入方式：内容-风格分解

**Baseline** 将音频仅用于生成初始运动目标，策略本身并不直接感知音频的时序特征。

**RoboPerform** 则提出了“运动 = 内容 + 风格”的分解视角。**内容**由文本描述（如 “a person is dancing”）通过 LaMP-T2M 内容编码器提取为固定潜在变量 $l_{\mathrm{motion}}$，提供运动的高层语义（如“跳舞”或“说话手势”）；**风格**则由对齐后的音频潜在变量 $l_{\mathrm{audio}}$ 承载，包含节奏、节拍、重音等时序调制信息。

在扩散去噪过程中，音频风格信号以**逐层注入**的方式调制运动表达：

$$\mathbf{o}_i = \mathrm{Layer}_i(\mathbf{o}_{i-1}, l_{\mathrm{motion}}) + \alpha l_{\mathrm{audio}}$$

这种设计使得同一内容潜在变量可以搭配不同音频风格，生成节奏各异但语义一致的动作序列，实现了即兴风格迁移（Section 3.4）。消融实验（Table 4）证实，加入内容潜在变量后，跟踪成功率与关节误差均显著改善，验证了内容-风格分解的有效性。

### 3. ∆MoE 教师策略：残差混合专家架构

**Baseline** 使用普通 MLP 策略或标准 MoE 架构，专家之间缺乏结构化的互补机制。

**RoboPerform** 提出的 **∆MoE**（残差混合专家）通过两个关键设计实现互补学习：

- **嵌套条件子空间划分**：将条件空间按“无音频→仅内容→内容+音频”的层次嵌套划分，使专家逐步学习从无条件先验到全条件表达的增量。
- **残差融合**：门控网络动态加权各专家的**残差分量**而非绝对值：

$$\mathbf{a} = w_1 \mathbf{a}_1 + \sum_{i=2}^{4} w_i (\mathbf{a}_i - \mathbf{a}_{i-1})$$

其中 $\mathbf{a}_1$ 为无条件先验，$\mathbf{a}_i - \mathbf{a}_{i-1}$ 为第 $i$ 个专家相对于前一条件的增量贡献。这一设计可视为 Classifier-Free Guidance 在连续、多维条件空间上的结构化推广（Section 3.2）。

T-SNE 可视化（Figure 4）显示，∆MoE 的各残差分量在特征空间中相互独立、聚类清晰，而普通 MoE 的专家输出高度重叠。定量上，∆MoE 在所有基准上均显著优于普通 MoE（Table 3），例如在 FineDance 数据集上，成功率从 0.88 提升至 0.93，关节误差 $E_{\mathrm{mpjpe}}$ 从 0.24 降至 0.18。

---

**创新总结**：RoboPerform 的三个 *changed slots* 并非孤立改进，而是形成了一条因果链——音频适配器将声学信号注入运动空间，内容-风格分解赋予扩散策略即兴泛化能力，∆MoE 教师则为学生策略提供高质量的特权监督。三者协同，使得人形机器人首次能够以低延迟、高节奏对齐的方式，对任意音频输入做出富有表现力的全身运动响应。

## 整体框架

RoboPerform 提出一种两阶段教师-学生框架，将原始音频作为**隐式风格信号**直接条件化运动生成，从而绕过传统管线中显式运动生成、重定向和跟踪的级联误差（Figure 2）。其核心架构包含三个关键组件：**∆MoE 教师策略**、**音频-运动对齐模块**和**扩散学生策略**。

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/002_Figure_2.jpg]]
*Figure 2: Overview of RoboPerform. We propose a two-stage approach: train an adaptor to inject kinematic information into audio modality, then a ∆MoE teacher policy is trained with RL and a diffusion-based student policy is trained to denoise actions conditioned on audio latent. We propose that motion=content+style. Thus, we fix the motion latent as a constant condition and leverage different audio signals as style modulation signals to generate actions adaptive to diverse rhythms*

### 两阶段流程

**第一阶段**训练音频-运动适配器，将运动学先验注入音频模态。具体而言，音频编码器（音乐使用 librosa，语音使用 TCN）提取原始音频特征，运动 VAE 从参考运动中编码运动潜在变量，随后通过基于 Transformer 加时间注意力的适配器，使用 InfoNCE 对比损失将音频潜在变量对齐到运动潜在空间：

$$\mathcal{L}_{\mathrm{InfoNCE}} = -\frac{1}{N} \sum_{i=1}^{N} \log \frac{\exp(\sin(l_{\mathrm{audio}}^{(i)}, l_{\mathrm{motion}}^{(i)}))}{\sum_{j=1}^{N} \exp(\sin(l_{\mathrm{audio}}^{(i)}, l_{\mathrm{motion}}^{(j)}))}$$

该损失鼓励适配器将匹配的音频-运动对拉近，同时将不匹配的对推开，从而在嵌入空间中建立跨模态对应关系。

**第二阶段**采用教师-学生蒸馏范式。∆MoE 教师策略使用 PPO 强化学习训练，输入包含特权信息（如参考运动、机器人与环境交互的完整状态）和运动参考，通过残差混合专家架构输出目标动作。扩散学生策略则使用 DAgger 训练，以运动内容潜在变量（由 LaMP-T2M 从文本描述编码）为主条件，以对齐后的音频潜在变量为风格注入信号，通过去噪过程生成最终关节动作。

### 核心设计理念：运动 = 内容 + 风格

RoboPerform 的核心洞察在于将运动分解为**内容**与**风格**两个维度。内容由高层语义描述（如"一个人在跳舞"）编码为固定的内容潜在变量，提供运动的基本语义框架；风格则由音频信号提供，作为调制信号逐层注入扩散去噪过程：

$$\mathbf{o}_i = \mathrm{Layer}_i(\mathbf{o}_{i-1}, l_{\mathrm{motion}}) + \alpha l_{\mathrm{audio}}$$

这种分解使得同一内容潜在变量可以搭配不同音频风格，生成节奏各异但语义一致的动作序列，实现了即兴且节奏对齐的表现力运动。

### ∆MoE 教师策略

∆MoE（残差混合专家）是教师策略的核心创新（Figure 3）。与普通 MoE 不同，∆MoE 采用**嵌套条件子空间划分**和**残差增量学习**机制，其最终动作由无条件先验与各专家条件增量的加权和构成：

$$\mathbf{a} = w_1 \mathbf{a}_1 + \sum_{i=2}^{4} w_i (\mathbf{a}_i - \mathbf{a}_{i-1})$$

其中 $w_i$ 由门控网络动态生成，$\mathbf{a}_i - \mathbf{a}_{i-1}$ 表示第 $i$ 个专家相对于前一条件子空间的残差增量。这种设计可解释为 Classifier-Free Guidance 在连续多维度条件设置下的结构化推广，使各专家在不同运动模式上形成互补而非冗余的专业化分工。T-SNE 可视化（Figure 4）证实，∆MoE 的各残差分量在聚类空间中相互独立，而普通 MoE 的专家输出则高度重叠。

### 输入输出流

推理时，整体管线如下：
1. **音频编码**：原始音频（音乐或语音）经编码器提取特征，通过训练好的适配器注入运动学先验，生成运动对齐的音频潜在变量；
2. **内容编码**：固定文本描述经 LaMP-T2M 编码为内容潜在变量；
3. **扩散去噪**：内容潜在变量作为主条件，音频潜在变量作为风格注入信号，扩散学生策略通过 DDIM 确定性采样（在推理速度和成功率之间达到最佳平衡）去噪生成目标关节动作；
4. **执行**：生成的动作直接驱动机器人关节，无需显式运动重定向步骤。

该框架在 Unitree G1 人形机器人上实现，推理延迟为 18-30ms，支持音乐到舞蹈和语音到手势两种任务的统一控制。

## 核心模块与公式推导

RoboPerform 的整体架构围绕“运动 = 内容 + 风格”这一核心洞察构建，通过教师-学生两阶段框架实现从原始音频到人形机器人关节动作的直接映射。其关键模块包括 ∆MoE 教师策略、音频-运动适配器以及扩散学生策略。

### ∆MoE 教师策略

∆MoE（残差混合专家）是教师策略的核心架构。与普通 MoE 不同，∆MoE 采用嵌套条件子空间划分与残差增量学习机制：专家按条件空间从弱到强逐层嵌套，每个专家学习相对于前一专家输出的残差增量，而非独立预测完整动作。

最终动作通过门控网络对各残差分量进行加权融合得到：

$$\mathbf{a} = w_1 \mathbf{a}_1 + \sum_{i=2}^{4} w_i (\mathbf{a}_i - \mathbf{a}_{i-1})$$

其中，$\mathbf{a}_1$ 为无条件先验输出，$(\mathbf{a}_i - \mathbf{a}_{i-1})$ 为第 $i$ 个专家相对于前一专家的条件增量，$w_i$ 为门控网络输出的动态权重。该设计可被解释为 Classifier-Free Guidance 在连续、多维条件空间上的结构化推广，通过残差融合消除专家间的冗余，强化互补性。教师策略使用 PPO 进行强化学习训练，输入包含特权信息和运动参考。

### 音频-运动适配器

适配器的目标是将音频潜在变量对齐到运动潜在空间，使音频能够作为有效的风格控制信号。具体而言，首先通过音频编码器（音乐使用 librosa 特征，语音使用 TCN）提取音频特征，运动 VAE 从参考运动中编码运动潜在变量。适配器采用 Transformer 加时间注意力机制，将音频潜在变量映射到运动潜在空间，并注入运动学先验。

训练适配器使用 InfoNCE 对比损失，鼓励配对的音频-运动潜在变量在嵌入空间中靠近，同时推开不相关的样本：

$$\mathcal{L}_{\mathrm{InfoNCE}} = -\frac{1}{N} \sum_{i=1}^{N} \log \frac{\exp(\sin(l_{\mathrm{audio}}^{(i)}, l_{\mathrm{motion}}^{(i)}))}{\sum_{j=1}^{N} \exp(\sin(l_{\mathrm{audio}}^{(i)}, l_{\mathrm{motion}}^{(j)}))}$$

其中 $l_{\mathrm{audio}}^{(i)}$ 和 $l_{\mathrm{motion}}^{(i)}$ 分别为第 $i$ 对音频和运动的潜在变量，$\sin(\cdot,\cdot)$ 为余弦相似度。该损失直接优化音频到运动的检索性能，在 BEAT2 和 FineDance 测试集上取得了显著的跨模态对齐效果（Table 1）。

### 扩散学生策略与音频注入

学生策略采用扩散模型架构，以运动内容潜在变量 $l_{\mathrm{motion}}$ 为主要条件，以对齐后的音频潜在变量 $l_{\mathrm{audio}}$ 为风格调制信号。内容潜在变量由 LaMP-T2M 编码器从文本描述（如“一个人在跳舞”）中提取，提供运动的高层语义约束。

音频风格信号通过逐层注入的方式调制扩散去噪过程：

$$\mathbf{o}_i = \mathrm{Layer}_i(\mathbf{o}_{i-1}, l_{\mathrm{motion}}) + \alpha l_{\mathrm{audio}}$$

其中 $\mathbf{o}_i$ 为扩散骨干网络第 $i$ 层的输出，$\mathrm{Layer}_i$ 为以运动内容为条件的变换层，$\alpha$ 为风格注入强度系数。该设计使得同一内容潜在变量在不同音频信号的调制下可生成节奏、节拍各异的动作序列，实现“即兴风格”能力。学生策略使用 DAgger 进行蒸馏训练，推理时采用 DDIM 确定性采样以在速度和成功率间取得最优平衡。

### 补充图表

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/003_Figure_3.jpg]]
*Figure 3: Overview of ∆MoE*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/004_Figure_4.jpg]]
*Figure 4: T-SNE visualization results of each component for ∆MoE and vanilla MoE*

## 实验与分析

### 核心实验设置

RoboPerform 在两个大规模音频-运动数据集上验证：**BEAT2**（音乐驱动舞蹈）和 **FineDance**（语音驱动手势）。仿真环境覆盖 **IsaacGym** 和 **MuJoCo** 两个物理引擎，机器人平台为 Unitree G1 人形机器人。基线方法采用常规管线：音频→显式运动生成（音乐用 EMAGE，语音用 FineNet ）→运动重定向到 G1→MLP 策略跟踪执行。

### 主实验结果

Table 2 展示了完整的运动跟踪性能对比。RoboPerform 在两个数据集和两个仿真环境中均实现了一致的性能提升：

- **BEAT2 (IsaacGym)**：成功率从 0.98 提升至 **0.99**，平均关节位置误差 (E_mpjpe) 从 0.07 降至 **0.05**，关键点误差 (E_mpkpe) 从 0.06 降至 **0.04**。
- **FineDance (IsaacGym)**：成功率从 0.88 提升至 **0.93**，E_mpjpe 从 0.24 降至 **0.18**，E_mpkpe 从 0.22 降至 **0.16**。
- **BEAT2 (MuJoCo)**：成功率从 0.94 提升至 **0.96**，E_mpjpe 从 0.13 降至 **0.10**。
- **FineDance (MuJoCo)**：成功率从 0.61 提升至 **0.67**，E_mpjpe 从 0.29 降至 **0.26**。

FineDance 在 MuJoCo 环境下成功率整体偏低（0.67），反映出语音驱动手势任务在更高物理精度仿真中面临更大的控制挑战。

### ∆MoE 教师策略消融

Table 3 对比了 ∆MoE 与普通 MoE 的跟踪性能。∆MoE 在所有基准上均显著优于普通 MoE：在 BEAT2 IsaacGym 中，成功率从普通 MoE 的 0.98 提升至 0.99，E_mpjpe 从 0.06 降至 0.05；在 FineDance IsaacGym 中，成功率从 0.90 提升至 0.93，E_mpjpe 从 0.20 降至 0.18。Figure 4 的 T-SNE 可视化进一步揭示了 ∆MoE 的优势机制：其残差分量 {a₁, a₂-a₁, ..., a₄-a₃} 在嵌入空间中形成相互独立的聚类，而普通 MoE 的各专家输出高度重叠。这验证了嵌套条件子空间划分和残差增量学习设计有效消除了专家间的冗余，实现了真正的互补学习。

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/009_Table_3.jpg]]
*Table 3: Ablation study on vanilla MoE and ∆MoE across both BEAT2 and FineDance datasets*

### 内容-风格分解消融

Table 4 验证了“运动=内容+风格”的核心假设。固定内容潜在变量（通过 LaMP-T2M 从文本描述“a person is dancing”编码）作为条件时，跟踪性能显著提升。在 BEAT2 IsaacGym 中，加入内容潜在变量使 E_mpjpe 从 0.07 降至 0.05，E_mpkpe 从 0.06 降至 0.04；在 FineDance IsaacGym 中，E_mpjpe 从 0.22 降至 0.18。这证明音频主要作为风格调制信号，塑造节奏和节拍模式等时序结构，而非规定精细运动学细节。内容潜在变量提供高层语义锚点，音频风格信号在此基础上进行时序调制，二者协同实现高效的动作生成。

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/010_Table_4.jpg]]
*Table 4: Ablation study on whether to incorporate content information. Herein, the content for both tasks is fixed, with the same content latent used in each inference*

### 音频适配器消融

Table 5 和 Table 11 共同验证了音频适配器的关键作用。移除适配器（即直接使用原始音频特征条件化扩散策略）导致性能大幅下降：在 BEAT2 IsaacGym 中，成功率从 0.99 骤降至 0.89，E_mpjpe 从 0.05 翻倍至 0.10；在 FineDance IsaacGym 中，成功率从 0.93 降至 0.82，E_mpjpe 从 0.18 恶化至 0.25。Table 11 进一步引入节拍对齐分数（BAS, Beat Alignment Score）量化音频-运动时序对齐质量，添加适配器后 BAS 显著提升，证明 InfoNCE 对比学习成功将运动学先验注入音频模态，使音频潜在变量与运动潜在空间对齐。

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/011_Table_5.jpg]]
*Table 5: Ablation study on whether to use adaptor inject kinematic information into audio modality. It can be observed that adaptor successfully aligns the audio and motion, improving the tracking performance and success rate*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/017_Table_11.jpg]]
*Table 11: Ablation study on whether to use adaptor to inject kinematic information into the audio modality. It can be observed that the adaptor successfully aligns the audio and motion, improving the tracking performance and success rate*

### 扩散策略设计选择

Table 14 对比了不同采样策略：DDIM 确定性采样在推理速度与成功率之间达到最佳平衡。Table 15 表明 x₀-prediction 目标比 ε-prediction 在跟踪任务中表现更好。Table 12 显示推理时间随 DDIM 采样步数线性增长，为实时部署提供了延迟参考。Table 16 和 Table 17 分别验证了专家数量（最优为 4）和条件空间划分方式对性能的影响可忽略，表明 ∆MoE 设计具有较好的鲁棒性。

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/020_Table_14.jpg]]
*Table 14: Fine-grained ablation on sampling strategies in the FineDance dataset*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/023_Table_15.jpg]]
*Table 15: Tracking performance across optimization objectives in the FineDance dataset*

### 定性结果与即兴能力

Figure 6 展示了 IsaacGym 和 MuJoCo 中的定性跟踪结果，RoboPerform 生成的舞蹈和手势动作与音频节拍高度对齐。Figure 7 对比了扩散策略与 MLP 策略在相同运动参考下的跟踪表现，以及面对未见音乐时的即兴能力：扩散策略展现出更强的节奏适应性和动作多样性，而 MLP 策略倾向于生成机械重复的动作模式。Figure 8 对比了 PHC 与 GMR 重定向方法的质量差异，进一步说明绕过显式重定向步骤的必要性。

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/024_Figure_7.jpg]]
*Figure 7: Qualitative results in the MuJoCo. The upper half presents the tracking performance of the MLP policy and the diffusion policy on the same motion; the lower half demonstrates their respective freestyle capabilities when confronted with unseen music*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative results in the IsaacGym and MuJoCo. The upper half presents the tracking performance of music-to-locomotion, and the lower half presents that of speech-to-locomotion*

### 失败模式与局限

FineDance MuJoCo 环境下 0.67 的成功率表明，语音驱动手势在更高物理保真度仿真中仍存在显著的 sim-to-real 差距。当前验证仅限于 Unitree G1 平台，框架在其他形态机器人上的迁移能力未知。音频适配器依赖配对数据训练，对域外音频风格（如未见音乐流派或语言）的泛化能力缺乏系统评估。实时部署中 18-30ms 的通信延迟可能制约极高动态动作（如快速连续节拍变化）的响应精度。

### 补充图表

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2512_23650/figures/006_Table_1.jpg]]
*Table 1: Audio-motion alignment performance on the BEAT2 and FineDance test sets*

## 方法谱系与知识库定位

### 与基线方法的本质差异

RoboPerform 的核心突破在于**绕过了传统音频驱动人形机器人管线中的显式运动重建与重定向步骤**。常规方法（如 **EMAGE** 与 **FineNet** ）遵循“音频→显式运动生成→重定向→MLP策略跟踪”的级联流程：先用预训练模型从音频生成人体运动序列，再通过重定向将其映射到目标机器人构型，最后由MLP策略执行跟踪。这一范式存在三个结构性缺陷：(1) 各模块独立优化，误差在级联中累积放大；(2) 推理延迟高，难以满足实时交互需求；(3) 声学信号与机器人执行之间耦合松散，无法实现即兴的风格化表现。

RoboPerform 将音频视为**隐式风格信号**，直接条件化扩散策略生成关节动作，从根本上消除了运动重定向环节。其关键设计在于“运动=内容+风格”的分解范式：内容由文本描述（如“a person is dancing”）通过 LaMP-T2M 编码为高层语义潜在变量，风格则由音频适配器对齐后的音频潜在变量提供。两者在扩散去噪过程中融合，使策略能够根据同一内容锚点、不同音频输入产生节奏对齐的多样化动作。

### 教师策略架构的谱系定位

RoboPerform 的 ∆MoE（残差混合专家）教师策略可视为 **Classifier-Free Guidance (CFG)** 在连续、多维条件空间上的结构化推广。CFG 通过在训练时随机丢弃条件来学习条件与无条件分布之间的方向，∆MoE 则通过嵌套条件子空间划分与残差增量学习，将这一思想扩展到多个专家的协同决策中。

具体而言，∆MoE 将动作分解为无条件先验 a₁ 与一系列条件增量 (a₂ − a₁), ..., (a₄ − a₃) 的加权和（见公式 ∆MoE Residual Fusion）。门控网络动态分配权重，使各专家专注于不同运动模式的互补学习。T-SNE 可视化（Figure 4）证实，∆MoE 的各残差分量在特征空间中相互独立，而普通 MoE 的专家输出高度重叠，验证了残差融合消除冗余的有效性。消融实验（Table 3）表明，∆MoE 相比普通 MoE 在所有基准上均显著提升跟踪成功率并降低关节/关键点误差。

### 音频-运动对齐的知识贡献

音频适配器是 RoboPerform 实现跨模态对齐的核心模块。它通过 InfoNCE 对比损失（公式 InfoNCE Loss）将音频潜在变量拉近对应运动潜在变量，同时推远不相关样本，从而将运动学先验注入音频模态。这一设计使音频潜在变量成为有效的风格调节信号，在扩散模型的每一层以加法形式注入（公式 Audio Injection），调制运动表达。

消融实验（Table 5, Table 11）揭示了适配器的决定性作用：移除适配器后，跟踪成功率和节拍对齐分数（BAS）均大幅下降，验证了运动学先验注入对跨模态对齐的必要性。Table 1 的检索指标（Music-Motion R@1: 66.7, Speech-Motion R@1: 64.6）进一步量化了适配器的对齐质量。

### 适用边界与局限

1. **机器人形态泛化性未知**：当前验证仅限于 Unitree G1 人形机器人，未在其他构型（如四足、轮式）或不同自由度的平台上测试。框架的核心假设——运动可分解为内容与风格——是否在更复杂的全身操作任务中成立，仍需验证。

2. **域外音频泛化受限**：音频适配器的训练依赖配对数据（音频-运动对），对于未见过的音乐风格、语言或声学环境，对齐质量和风格迁移能力尚无保证。这一局限源于 InfoNCE 对比学习的本质：它学习训练分布内的相对关系，而非绝对跨域映射。

3. **实时部署的延迟约束**：实际部署中通信延迟为 18–30ms，虽已满足多数舞蹈和手势场景，但对于极高动态动作（如快速连续节拍变化）可能构成响应瓶颈。DDIM 确定性采样在推理速度与成功率之间取得平衡（Table 14），但采样步数的减少会牺牲动作质量。

4. **内容编码器的上限效应**：内容潜在变量的质量由 LaMP-T2M 决定，若文本描述过于模糊或与目标运动语义不匹配，策略的表现将受限于内容编码器提供的先验信息量。Table 4 显示加入内容潜在变量显著改善跟踪性能，但内容编码器本身并非本文贡献，其能力边界构成了系统的隐式上限。

### 开放问题

- **内容潜在变量的质量瓶颈**：当前框架将内容编码器视为固定模块，其输出质量是否构成整体性能的上限？若替换为更强的文本-运动模型，能否进一步释放风格调制的潜力？

- **多机器人协同与全身操作**：内容-风格分解范式能否推广到多机器人协同舞蹈或更复杂的全身操作任务？在这些场景中，“内容”的定义可能超出单一文本描述，需要更结构化的任务表示。

- **无需配对数据的对齐**：音频适配器依赖配对数据训练，能否通过自监督或跨模态循环一致性的方式，实现无需配对的音频-运动对齐？这将显著降低数据采集成本并提升域外泛化能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Audio_Control.pdf]]
