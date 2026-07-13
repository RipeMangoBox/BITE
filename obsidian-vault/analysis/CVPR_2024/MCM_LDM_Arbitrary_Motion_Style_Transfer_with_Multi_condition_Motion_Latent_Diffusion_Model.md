---
title: MCM LDM Arbitrary Motion Style Transfer with Multi condition Motion Latent Diffusion Model
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Latent_Diffusion_Model.pdf
project_link: null
code_link: https://github.com/
aliases:
- MCMLDMML
- MLAMSTMCMLDM
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 多条件运动潜在扩散模型（MCM-LDM）中的三元组条件解耦（内容、轨迹、风格）及多条件去噪器的优先级引导机制（内容为主条件，轨迹与风格为辅条件）。
primary_logic: 将运动显式分解为内容、轨迹和风格三个独立因素，并以扩散模型为框架，通过多条件引导将轨迹和风格作为辅助条件动态注入内容流，既能保留运动的核心叙述，又能无缝融合风格并避免轨迹丢失。
claims:
- MCM-LDM在HumanML3D测试集上取得了最优的FMD (27.69) 和SRA (58.00)，次优的CRA (35.75)，并保持了均衡的TSI (0.40) 和FSF (1.28)，证明其在运动质量和风格转移上的综合优势（表1）。
- 消融实验表明，移除StyleRemover导致SRA从58.00骤降至16.88而CRA激增至93.43，证明内容-风格解耦的必要性；移除轨迹条件导致TSI从0.40升至0.93，显著破坏轨迹保持；替换预训练MotionCLIP为随机初始化则全面崩溃（FMD 138.55），证实风格提取器的关键作用（表2）。
- 用户研究显示，MCM-LDM在真实感（4.48）、内容保留（4.45）和风格表现（4.43）上的平均评分均高于对比方法，且ANOVA检验证实差异显著（p<0.01），表明人类偏好（表4）。
- 将运动显式分解为内容、轨迹和风格三个独立因素，并以扩散模型为框架，通过多条件引导将轨迹和风格作为辅助条件动态注入内容流，既能保留运动的核心叙述，又能无缝融合风格并避免轨迹丢失。
---

# MCM LDM Arbitrary Motion Style Transfer with Multi condition Motion Latent Diffusion Model

> [!tip] 核心洞察
> 将运动显式分解为内容、轨迹和风格三个独立因素，并以扩散模型为框架，通过多条件引导将轨迹和风格作为辅助条件动态注入内容流，既能保留运动的核心叙述，又能无缝融合风格并避免轨迹丢失。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于多条件运动潜在扩散模型的任意运动风格迁移 |
| 英文题名 | MCM LDM Arbitrary Motion Style Transfer with Multi condition Motion Latent Diffusion Model |
| 会议/期刊 | CVPR 2024 |
| Links | [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | Multi-condition Motion Latent Diffusion Model (MCM-LDM) |
| Dataset |  |

> [!tip] 效果简介
> - MCM-LDM在HumanML3D测试集上取得了最优的FMD (27.69) 和SRA (58.00)，次优的CRA (35.75)，并保持了均衡的TSI (0.40) 和FSF (1.28)，证明其在运动质量和风格转移上的综合优势（表1）。
> - 消融实验表明，移除StyleRemover导致SRA从58.00骤降至16.88而CRA激增至93.43，证明内容-风格解耦的必要性；移除轨迹条件导致TSI从0.40升至0.93，显著破坏轨迹保持；替换预训练MotionCLIP为随机初始化则全面崩溃（FMD 138.55），证实风格提取器的关键作用（表2）。
> - 用户研究显示，MCM-LDM在真实感（4.48）、内容保留（4.45）和风格表现（4.43）上的平均评分均高于对比方法，且ANOVA检验证实差异显著（p<0.01），表明人类偏好（表4）。

## 概要

任意运动风格迁移（Arbitrary Motion Style Transfer, AMST）的核心挑战在于：如何在完整保留原始运动内容语义的前提下，自然融入目标风格特征，同时避免因轨迹处理不当导致的“脚滑动”等运动失真。现有方法——如基于1D卷积与AdaIN的无配对迁移（Aberman et al., ACM TOG 2020）、基于时空图卷积的多风格域风格化（Park et al., Proc. ACM CGIT 2021）、以及基于身体部位风格融合的Motion Puzzle（Jang et al., ACM TOG 2022）——普遍采用将内容运动轨迹直接复制到风格化运动上的策略，这从根本上破坏了运动学一致性，导致脚部滑动等伪影。此外，这些方法在训练时依赖配对或隐式特征混合，缺乏对内容、风格、轨迹三者的显式解耦与独立控制。

本文提出**多条件运动潜在扩散模型（MCM-LDM）**，以扩散模型为框架，将运动显式分解为内容、轨迹和风格三个独立因素。其核心设计在于多条件去噪器中的优先级引导机制：内容作为主条件与噪声潜在特征拼接，轨迹与风格作为辅条件通过AdaLN-Zero动态注入每一层。训练采用自重建范式（同一运动同时作为内容和风格输入），配合StyleRemover实现内容-风格解耦，以及Transformer轨迹编码器实现学习式轨迹保留，从根本上解决了轨迹复制带来的失真问题。

在HumanML3D数据集上的定量评估表明，MCM-LDM取得了最优的运动质量（FMD 27.69）和风格准确率（SRA 58.00），次优的内容保留（CRA 35.75），并保持了均衡的轨迹相似度（TSI 0.40）和脚滑动指标（FSF 1.28）。消融实验揭示了关键因果机制：移除StyleRemover导致SRA从58.00骤降至16.88而CRA激增至93.43，证实内容-风格解耦的必要性；移除轨迹条件使TSI从0.40升至0.93，验证了学习式轨迹保留的有效性；替换预训练MotionCLIP为随机初始化则使FMD崩溃至138.55，表明风格提取器的关键作用。用户研究进一步确认了MCM-LDM在真实感、内容保留和风格表现上的人类偏好优势（ANOVA检验p<0.01）。

### 运动风格迁移的现状与瓶颈

运动风格迁移（Motion Style Transfer）旨在将目标运动的风格特征注入源运动的内容序列，同时保留后者的语义叙述。这一任务在角色动画、虚拟现实和游戏开发中具有广泛需求。早期的运动风格迁移方法主要依赖配对数据学习隐式特征融合，例如**Aberman等人**（ACM TOG 2020）提出的基于1D卷积与AdaIN的无配对迁移框架，以及**Holden等人**（ACM TOG 2016）的深度学习运动合成与风格编辑工作。这些方法在特定风格域内取得了可观效果，但面对任意风格迁移（Arbitrary Motion Style Transfer, AMST）时，其泛化能力受到根本性限制。

近年来，研究者尝试突破风格域的限制。**Park等人**（Proc. ACM CGIT 2021）基于时空图卷积实现了多风格域的多样化风格化，**Motion Puzzle**（Jang et al., ACM TOG 2022）则通过身体部位风格融合实现了任意风格迁移。然而，这些方法共享一个深层缺陷：它们对运动轨迹的处理是**硬拷贝式**的——直接将内容运动的根关节轨迹复制到风格化运动上。这种做法忽视了风格与轨迹之间的动态耦合关系，导致严重的**脚滑动（foot sliding）**伪影（参见Figure 2），破坏了运动结果的物理可信度。

### 核心瓶颈：内容-风格-轨迹的三元纠缠

现有AMST方法的根本瓶颈在于**缺乏对运动轨迹的显式建模**。运动本质上可分解为三个独立因素：**内容**（做什么动作，如“行走”）、**风格**（怎么做，如“沮丧地走”）和**轨迹**（在哪里走，如根关节的平移路径）。现有方法要么将轨迹简单复制，要么将其隐式混入内容或风格特征中，导致三个因素相互纠缠。当风格化过程改变运动节奏或姿态时，硬拷贝的轨迹无法自适应调整，造成脚部与地面的接触关系失真。

此外，训练范式的局限加剧了这一纠缠。多数方法采用配对内容-风格数据进行训练，隐式混合特征，使得模型难以学习到干净的内容-风格解耦。**FineStyle**（Song et al., IEEE TVCG 2023）尝试通过双交互流融合实现细粒度风格迁移，**Style-ERD**（Tao et al., CVPR 2022）则探索了响应式在线迁移，但这些方法仍未从根本上解决轨迹保留与风格注入之间的矛盾。

### 本文动机与核心思路

针对上述瓶颈，本文提出**多条件运动潜在扩散模型（Multi-condition Motion Latent Diffusion Model, MCM-LDM）**，其核心动机可概括为三个层面：

1. **显式三元解耦**：将运动系统性地分解为内容、轨迹和风格三个独立条件，分别通过专用编码器提取特征，从根本上避免因素纠缠。

2. **学习式轨迹保留**：不再硬拷贝轨迹，而是通过Transformer轨迹编码器学习轨迹特征，并将其作为辅助条件动态引导扩散过程，使风格化运动在保持内容叙述的同时自适应地遵循给定轨迹，消除脚滑动问题。

3. **优先级引导机制**：在多条件去噪器中，赋予内容条件主导地位（主条件），轨迹和风格作为辅助条件通过AdaLN-Zero机制动态注入，确保内容完整性不被风格化过程侵蚀。

通过将扩散模型的生成能力与多条件引导相结合，MCM-LDM能够在保留运动核心语义的前提下，自然融合任意目标风格，同时忠实遵循给定轨迹。Figure 1的定性效果展示了该方法在风格注入与内容保真度之间的平衡能力。

## 核心方法与创新机理

### 瓶颈定位：轨迹丢失与风格-内容耦合

现有任意运动风格迁移（AMST）方法面临两个相互纠缠的核心瓶颈。其一，**轨迹保留机制存在根本缺陷**：多数方法（如 **Aberman et al.** (ACM TOG 2020) 和 **Motion Puzzle** (Jang et al., ACM TOG 2022)）直接将内容运动的轨迹复制到风格化运动上，这种硬拷贝策略忽略了风格注入后运动学约束的变化，导致“脚滑动”等细节失真（Figure 2）。其二，**风格与内容的隐式耦合**使得模型难以在保留运动核心叙述的同时自然融入目标风格——当风格化程度提升时，内容语义往往被破坏；反之，过度保护内容则导致风格转移不充分。这些瓶颈的根源在于缺乏对运动三要素（内容、轨迹、风格）的显式建模与差异化引导机制。

### 核心洞察：三元组条件解耦与优先级引导

本工作提出的 **Multi-condition Motion Latent Diffusion Model (MCM-LDM)** 基于一个关键洞察：**将运动显式分解为内容、轨迹和风格三个独立因素，并以扩散模型为框架，通过多条件引导将轨迹和风格作为辅助条件动态注入内容流**。这一设计既能保留运动的核心叙述，又能无缝融合风格并避免轨迹丢失。

具体而言，MCM-LDM 包含三个相互关联的创新模块：

1. **多条件提取模块（Multi-condition Extraction）**：通过 Transformer 轨迹编码器（$\mathcal{E}_{tra}$）提取轨迹特征 $f_t$，利用预训练 MotionCLIP 风格提取器（$\mathcal{E}_{sty}$）获取风格特征 $f_s$，并通过带 StyleRemover 的内容编码器（$\mathcal{E}_{con}$）从 VAE 编码特征中剥离风格信息，得到纯净的内容特征 $f_c$（Equ. 1）。StyleRemover 是关键设计——消融实验表明，移除它会导致风格迁移几乎失效（SRA 从 58.00 骤降至 16.88），而内容重建过度（CRA 从 35.75 飙升至 93.43），证实了内容-风格解耦的必要性（Table 2）。

2. **自重建训练范式**：将训练任务从传统的配对内容-风格数据迁移转变为自重建——同一运动同时作为内容和风格输入（Sec. 3.2）。这一设计消除了对配对标注数据的依赖，使模型在重建约束下自然学习三元组条件的解耦表示。

3. **多条件去噪器（Multi-condition Denoiser）与优先级引导**：在扩散去噪过程中，内容特征 $f_c$ 作为主条件与噪声潜在特征 $z_n$ 拼接（Equ. 6），占据主导地位；轨迹特征 $f_t$ 和风格特征 $f_s$ 作为辅条件，通过 AdaLN-Zero 机制动态注入每一层 Transformer（Equ. 7-8）。消融实验验证了这一优先级设计的有效性：将风格或轨迹提升为主条件会导致多项指标下降（Table 3）；而使用 AdaLN-Zero 作为辅条件融合机制，相较于简单串联或 AdaIN 能取得更均衡的风格转移效果（Table 3）。此外，推理阶段采用分类器自由引导（Equ. 5），通过引导尺度 $\lambda = 2.5$ 平衡条件与无条件噪声预测，灵活控制风格化程度。

### 与基线方法的关键差异

| 维度 | 基线方法 | MCM-LDM |
|------|----------|---------|
| **轨迹处理** | 直接复制内容轨迹，导致脚滑动 | Transformer 轨迹编码器学习轨迹特征，作为辅助条件引导扩散过程 |
| **训练范式** | 配对内容-风格数据训练，隐式混合特征 | 自重建训练，显式解耦内容、轨迹和风格条件 |
| **条件集成** | 单条件引导或简单特征融合（串联、AdaIN） | 多条件去噪器：内容为主条件（拼接），轨迹与风格为辅条件（AdaLN-Zero 注入），实现优先级引导 |
| **风格提取** | 依赖任务特定特征提取器 | 预训练 MotionCLIP 提供通用风格表示（随机初始化替换导致 FMD 恶化至 138.55，证实其关键作用） |

### 创新边界与局限性

MCM-LDM 的创新聚焦于**给定轨迹条件下的风格迁移**，轨迹编码器仅在给定轨迹时发挥作用，无法自主生成新轨迹。当前模型未探索文本或音乐驱动的轨迹生成，也未建模环境交互（如物体抓取、地面适应），在复杂场景下可能出现物理不合理性。此外，模型性能受限于 HumanML3D 训练数据的时间范围，对超长序列或分布外动作的泛化能力有待验证。

MCM-LDM 的整体 pipeline 由两大核心组件串联而成：**多条件提取模块（Multi-condition Extraction）** 与 **多条件运动潜在扩散模型（MCM-LDM）**，如 Figure 3 所示。其设计哲学在于将运动显式解耦为内容（content）、轨迹（trajectory）和风格（style）三个独立因素，并以扩散模型为框架，通过优先级引导机制实现三者的协同融合。

### 输入输出流

给定一段内容运动 $x_{1:L}$（提供“做什么”）和一段风格运动（提供“怎么做”），系统首先通过多条件提取模块并行获取三类条件特征：
- **轨迹特征** $f_t$：由基于 Transformer 的轨迹编码器 $\mathcal{E}_{tra}$ 从内容运动的关节轨迹 $t_{1:L}$ 中提取；
- **风格特征** $f_s$：由预训练的 MotionCLIP 风格提取器 $\mathcal{E}_{sty}$ 从风格运动中提取；
- **内容特征** $f_c$：内容运动先经预训练运动 VAE 的编码器 $\mathcal{E}$ 映射至潜在空间，再通过 StyleRemover 剥离风格信息后线性降维得到。

这三类条件随后送入 MCM-LDM 的**多条件去噪器（Multi-condition Denoiser）** $E_\theta$，引导扩散过程在运动潜在空间中将随机噪声逐步去噪为风格化运动的潜在表示，最终由运动 VAE 的解码器重建为风格化运动序列。

### 模块关系与优先级引导

多条件去噪器内部采用了明确的条件优先级策略（Figure 4）：
- **内容作为主条件**：内容特征 $f_c$ 与噪声潜在特征 $z_n$ 直接拼接（$z_n' = \mathrm{Concat}(z_n, f_c)$），构成去噪器的主输入流，确保生成结果忠实于原始运动的叙事结构；
- **轨迹与风格作为辅条件**：轨迹特征 $f_t$ 和风格特征 $f_s$ 分别通过独立的 MLP 生成缩放（$\gamma$）、偏移（$\beta$）和门控（$\alpha$）参数，以 AdaLN-Zero 机制动态注入去噪器的每一层 Transformer 块中——风格条件作用于自注意力层，轨迹条件作用于前馈网络层，实现无缝的风格融合与轨迹保持。

![[assets/figures/papers/paper_list_l2_MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Late/figures/004_Figure_4.jpg]]
*Figure 4: Architecture of Multi-conditon Denoiser. We incorporate the content features $f _ { c }$ as a primary condition by concatenating it with the noisy latent feature $z _ { n }$ , achieving a leading role. In contrast, the trajectory features $f _ { t }$ and style features $f _ { s }$ serve as secondary conditions, embedded into content flow dynamically*

### 训练与推理范式

训练阶段采用**自重建（self-reconstruction）**范式：将同一运动同时作为内容和风格输入，使模型学习在给定自身内容、轨迹和风格的条件下重建原始运动。这一设计将风格迁移任务转化为有监督的重建任务，无需成对的内容-风格数据。

推理阶段引入**分类器自由引导（classifier-free guidance）**机制：
$$E_n^* = \lambda E_\theta(z_n, f_c, f_t, f_s) + (1-\lambda) E_\theta(z_n, f_c, f_t, \emptyset)$$
通过引导系数 $\lambda$（论文中设为 2.5）在条件预测与无条件预测之间插值，控制风格化的强度。这一设计使得模型在保留内容完整性的同时，能够灵活调节风格融入的程度。

### 多条件提取模块

MCM-LDM 的核心设计在于将运动显式分解为内容、轨迹和风格三个独立因素，并通过多条件提取模块分别获取对应的特征表示。给定内容运动序列 $x_{1:L}$ 及其轨迹 $t_{1:L}$，以及风格运动序列，该模块按以下流程提取条件特征（Equ. 1）：

$$
\begin{array}{rl}
& f_t = \mathcal{E}_{tra}(t_{1:L}), \\
& f_s = \mathcal{E}_{sty}(x_{1:L}), \\
& f_c = \mathrm{StyleRemover}(\mathcal{E}(x_{1:L})).
\end{array}
$$

各变量含义如下：
- **$f_t$**：轨迹特征，由基于 Transformer 的轨迹编码器 $\mathcal{E}_{tra}$ 从运动轨迹中提取。此设计替代了以往方法直接复制内容轨迹的做法，通过学习式编码避免了脚滑动等伪影（Figure 2）。
- **$f_s$**：风格特征，由预训练的 **MotionCLIP** 风格提取器 $\mathcal{E}_{sty}$ 从风格运动中提取。消融实验证实，用随机初始化的 Transformer 替代预训练 MotionCLIP 会导致 FMD 从 27.69 骤升至 138.55（Table 2），表明预训练风格提取器对模型性能至关重要。
- **$f_c$**：内容特征，由预训练运动 VAE 的编码器 $\mathcal{E}$ 编码后，经 **StyleRemover** 模块去除风格信息得到。StyleRemover 是实现内容-风格解耦的关键：消融实验显示，移除该模块后 SRA 从 58.00 骤降至 16.88，而 CRA 从 35.75 激增至 93.43（Table 2），证明模型若无此约束将过度依赖内容特征而无法有效迁移风格。

![[assets/figures/papers/paper_list_l2_MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Late/figures/002_Figure_2.jpg]]
*Figure 2: Comparisons of trajectory. Our method (B) learns to preserve motion trajectory during style transfer, while other methods [1, 26, 36] (A) copy content trajectory directly onto stylized motions, resulting in foot sliding issue*

训练采用自重建范式，即同一运动同时作为内容和风格输入，使模型学习在保留内容核心叙述的同时重建自身风格。

### 运动 VAE 与潜在扩散过程

MCM-LDM 在预训练运动 VAE 的潜在空间上进行扩散。VAE 编码器将原始运动压缩为潜在特征 $z_0$，解码器则从去噪后的潜在特征重建最终风格化运动。扩散过程分为前向加噪和反向去噪两个阶段。

**前向扩散**（Equ. 2）逐步向 $z_0$ 添加高斯噪声，经 $N$ 步后逼近标准正态分布：

$$
q(z_n | z_{n-1}) = \mathcal{N}(\sqrt{\alpha_n} z_{n-1}, (1-\alpha_n) \mathbf{I})
$$

其中 $\alpha_n$ 为噪声调度参数，控制每步的噪声注入强度。

**反向去噪**由多条件去噪器 $E_\theta$ 执行，在给定条件特征的前提下从纯噪声逐步恢复目标潜在表示（Equ. 3）：

$$
E_n^* = E_\theta(z_n, n, f_c, f_t, f_s)
$$

训练目标为最小化噪声预测的均方误差（Equ. 4）：

$$
\mathcal{L} = \mathbb{E}_{E,n,(f_c,f_t,f_s)} \left[ \| E - E_\theta(z_n, f_c, f_t, f_s) \|_2^2 \right]
$$

推理时采用**分类器自由引导**（Classifier-Free Guidance）策略（Equ. 5），通过引导尺度 $\lambda$（设为 2.5）平衡条件与无条件噪声预测，控制风格化程度：

$$
E_n^* = \lambda E_\theta(z_n, f_c, f_t, f_s) + (1-\lambda) E_\theta(z_n, f_c, f_t, \emptyset)
$$

其中 $\emptyset$ 表示将风格条件置为空，使模型在“有风格引导”和“无风格引导”之间插值。

### 多条件去噪器与优先级引导

多条件去噪器 $E_\theta$ 是 MCM-LDM 的架构核心（Figure 4），其关键创新在于为不同条件分配差异化优先级，而非简单拼接或融合。

**主条件——内容**：内容特征 $f_c$ 作为主条件，通过拼接直接与噪声潜在特征 $z_n$ 结合（Equ. 6）：

$$
z_n^{\prime} = \mathrm{Concat}(z_n, f_c)
$$

这种硬连接方式确保内容信息在去噪全程占据主导地位，维持运动的核心叙述。

**辅条件——轨迹与风格**：轨迹特征 $f_t$ 和风格特征 $f_s$ 作为辅条件，通过 **AdaLN-Zero** 机制动态注入去噪器的每一层。具体而言，两个独立的 MLP 分别将辅条件特征映射为缩放、偏移和门控参数（Equ. 7）：

$$
\gamma_s, \beta_s, \alpha_s = \mathrm{MLP}_s(f_s), \quad \gamma_t, \beta_t, \alpha_t = \mathrm{MLP}_t(f_t)
$$

这些参数按层分别作用于多头自注意力（MSA）和多层感知机（MLP）子层（Equ. 8）：

$$
\begin{array}{rl}
& \hat{z}_{n,k^{\prime}} = \hat{z}_{n,k-1} + \alpha_s \mathbf{MSA}(\mathbf{LN}(\hat{z}_{n,k-1}) \gamma_s + \beta_s), \\
& \hat{z}_{n,k} = \hat{z}_{n,k^{\prime}} + \alpha_t \mathbf{MLP}(\mathbf{LN}(\hat{z}_{n,k^{\prime}}) \gamma_t + \beta_t).
\end{array}
$$

其中 $\mathbf{LN}$ 为层归一化，$\alpha_s$、$\alpha_t$ 为零初始化的门控参数，使训练初期辅条件影响为零，逐步学习注入。风格参数作用于 MSA 子层以影响全局注意力模式，轨迹参数作用于 MLP 子层以调整局部运动细节。

消融实验验证了此优先级设计的有效性：将风格或轨迹提升为主条件（w Pri. $f_s$ / w Pri. $f_t$）均导致多项指标下降（Table 3）；将辅条件融合机制替换为简单拼接（w Con.）或 AdaIN（w AdaIN）也无法取得同等均衡的风格转移效果。这证实了“内容为主、轨迹与风格为辅”的 AdaLN-Zero 注入策略是实现高质量任意运动风格迁移的关键因果机制。

### 补充图表

![[assets/figures/papers/paper_list_l2_MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Late/figures/003_Figure_3.jpg]]
*Figure 3: Method overview. We have two components: (1) The Multi-condition Extraction obtains content features $f _ { c }$ and trajectory features $f _ { t }$ from the content motion, while the style features $f _ { s }$ are obtained from the style motion. (2) MCM-LDM contains forward process and denosing process. The condition features guide the denoising process through Multi-condition Denoiser*

## 实验与关键发现

### 核心定量结果与综合性能

MCM-LDM在HumanML3D测试集上取得了最优的运动质量与风格表现平衡。如表1所示，该方法在**FMD**（Fréchet Motion Distance, 27.69）和**SRA**（Style Recognition Accuracy, 58.00）两项指标上均达到最优，**CRA**（Content Recognition Accuracy, 35.75）为次优，同时保持了较低的**TSI**（Trajectory Similarity Index, 0.40）和**FSF**（Foot Sliding Factor, 1.28）。这一结果验证了核心设计思路：将运动显式解耦为内容、轨迹、风格三个独立条件，并通过多条件扩散模型进行优先级引导，能够在保留运动内容核心叙述的同时，实现高质量的风格融合与轨迹保持。

对比方法中，**Motion Puzzle**（Jang et al., ACM TOG 2022）在CRA上表现最优（29.60），但其SRA（52.00）和TSI（0.42）均弱于MCM-LDM，表明其在风格转移与轨迹保留之间存在更明显的权衡。**FineStyle**（Song et al., IEEE TVCG 2023）的FMD（31.55）和SRA（54.00）次优，但FSF（1.65）较高，说明其脚滑动问题更为突出。MCM-LDM在五个指标上均未出现极端值，证明多条件引导机制有效缓解了风格迁移中常见的“风格-内容-轨迹”三角权衡。

### 消融实验：多条件提取组件的必要性

消融实验（表2）系统验证了三个关键组件的因果作用：

1.  **移除StyleRemover**：SRA从58.00骤降至16.88，而CRA从35.75激增至93.43。这表明没有StyleRemover时，模型退化为近似内容重建，风格特征几乎无法注入。StyleRemover是内容-风格解耦的瓶颈组件，其作用是抑制内容编码器中的风格信息，迫使模型从独立的风格分支获取风格特征。

2.  **移除轨迹条件 $f_t$**：TSI从0.40升至0.93（越低越好），轨迹保持能力严重退化。与此同时SRA升至65.11，暗示模型在无轨迹约束时倾向于更激进地改变运动以匹配风格，却牺牲了空间位移的准确性。这证实了轨迹条件作为辅助引导对于避免“脚滑动”等伪影的关键作用。

3.  **替换预训练MotionCLIP为随机初始化Transformer**：所有指标全面崩溃，FMD飙升至138.55，SRA降至18.00。这说明风格提取器的质量直接决定了风格迁移的上限——随机初始化的编码器无法提供有意义的风格表征，导致去噪器在噪声空间中迷失方向。

### 消融实验：引导策略与融合机制

表3进一步揭示了去噪器内部条件集成策略的影响：

-   **将风格或轨迹提升为主条件**（w Pri. $f_s$ / w Pri. $f_t$）均导致多项指标下降。当风格作为主条件时，内容保留受损；当轨迹作为主条件时，风格表现受限。这验证了“内容为主、轨迹与风格为辅”的优先级设计是必要的——内容流必须占据主导地位，风格和轨迹应作为动态调节信号注入。

-   **辅条件融合机制对比**：AdaLN-Zero相较于简单串联（Concat）或AdaIN，在风格转移效果上更为均衡。AdaLN-Zero通过门控参数 $\alpha_s, \alpha_t$ 控制风格和轨迹信息注入的强度，避免了串联可能带来的信息淹没或AdaIN可能导致的过度风格化。该机制允许模型在去噪过程中自适应地决定每一层对辅条件的依赖程度。

### 定性分析与可视化验证

图5提供了两组风格迁移案例的定性对比。紫色线条标注脚部与地面的接触情况，放大细节显示MCM-LDM在保持正确脚接触的同时，成功融入了目标风格的身体姿态特征（如手臂摆动幅度、躯干倾斜角度等）。相比之下，基线方法在风格化后常出现脚部悬浮或滑动现象，这与TSI和FSF指标的定量结论一致。

图6的消融可视化进一步印证了表2的结论：移除StyleRemover后，输出运动几乎与内容运动完全一致，风格特征消失；移除轨迹条件后，风格化运动的全局位移路径发生明显偏移，脚部轨迹与原始内容产生显著偏差。

### 用户研究

用户研究（表4）从真实感、内容保留和风格表现三个维度收集了人类偏好评分。MCM-LDM在三项上均获得最高平均分（真实感4.48、内容保留4.45、风格表现4.43），且ANOVA检验表明差异具有统计显著性（$p<0.01$）。这从感知层面确认了自动指标结论的可靠性——用户能够感知到MCM-LDM在避免伪影、保留运动语义和表现风格特征方面的综合优势。

### 失败模式与局限性

尽管MCM-LDM在整体指标上表现优异，但分析揭示了以下边界情况：

1.  **轨迹条件依赖性**：当前方法仅在给定轨迹时发挥作用，无法自主生成新轨迹。对于需要轨迹创造的应用场景（如路径驱动的运动生成），模型缺乏生成能力。
2.  **分布外泛化**：模型在HumanML3D上训练，对于超出训练时长或动作类型的序列，风格迁移质量可能下降。实验未报告在分布外数据上的测试结果，这一点需要手动验证。
3.  **环境交互缺失**：模型未建模与环境的物理交互（如地面反作用力、物体接触），在复杂场景下可能出现物理不合理性。FSF指标虽优于基线，但1.28的绝对值仍表明存在轻微脚滑动，说明轨迹学习式保留尚未完全消除该问题。

### 补充图表

![[assets/figures/papers/paper_list_l2_MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Late/figures/007_Table_2.jpg]]
*Table 2: Ablation study. The results validate the importance of StyleRemover in ${ \mathcal { E } } _ { c o n }$ . , pre-trained MotionCLIP in $\mathcal { E } _ { s t y }$ , and trajectory condition $f _ { t }$ to our approach. Table 3. Experiments of four guidance strategies in $E _ { \theta }$ . ‘w Con.’ and ‘w AdaIN’ represent the fusion mechanisms of concatenation and AdaIN for incorporating the secondary conditions into $E _ { \theta }$ . ‘w Pri. $f _ { s }$ { ' } an$d ^ \ast \mathrm { _ { w } }$ Pri. $f _ { t } ^ { \mathrm { ~ , ~ } }$ respectively represent treating style or trajectory as a primary condition*

![[assets/figures/papers/paper_list_l2_MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Late/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation. ‘↑’ (‘↓’) indicates that the value is better if the metric is larger (smaller); The bold fonts denote best performers. The results demonstrate that our MCM-LDM achieves balanced performance in all metrics*

![[assets/figures/papers/paper_list_l2_MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Late/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of ablation study. We present the visualization results of two ablation experiments: without our StyleRemove and without the trajectory condition. The results showcase their importance*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

任意运动风格迁移（Arbitrary Motion Style Transfer, AMST）的目标是将源运动的内容（如“行走”）与目标运动的风格（如“僵尸步态”）融合，生成既保留原始运动语义又体现目标风格特征的新运动序列。该领域的核心瓶颈在于**内容保留与风格融入之间的根本性张力**：现有方法在强化风格表现时往往损害内容完整性，反之亦然。更深层的症结在于，多数方法缺乏对运动轨迹的显式建模——它们直接将内容运动的轨迹复制到风格化运动上，导致“脚滑动”（foot sliding）等物理不合理的细节失真（Figure 2）。MCM-LDM的因果调控旋钮在于**三元组条件解耦（内容、轨迹、风格）及多条件去噪器的优先级引导机制**，这使其能够在保留运动核心叙述的同时，将轨迹和风格作为辅助条件动态注入内容流。

### 2. 方法谱系与差异化定位

MCM-LDM属于**基于扩散模型的运动风格迁移**范式，其方法谱系可从条件建模、风格提取和训练策略三个维度进行定位。

**与早期无配对风格迁移方法的对比。** **Aberman et al.**（ACM TOG 2020）开创性地将1D卷积与AdaIN结合用于无配对运动风格迁移，但该方法隐式混合内容与风格特征，缺乏显式的解耦机制。**Park et al.**（Proc. ACM CGIT 2021）引入时空图卷积以处理多风格域，但仍依赖单一条件引导。MCM-LDM的核心改进在于：将运动**显式分解**为内容、轨迹和风格三个独立因素，并通过多条件去噪器实现优先级引导——内容作为主条件与噪声潜在特征拼接，轨迹和风格作为辅条件通过AdaLN-Zero注入每层（Figure 4）。这一设计从架构层面解决了内容-风格纠缠问题。

**与细粒度风格迁移方法的对比。** **Motion Puzzle**（Jang et al., ACM TOG 2022）通过身体部位风格融合实现任意风格迁移，但其轨迹处理仍采用直接复制策略。**FineStyle**（Song et al., IEEE TVCG 2023）提出双交互流融合机制，在细粒度层面改善风格表现，但同样未对轨迹进行学习式建模。MCM-LDM通过Transformer轨迹编码器学习轨迹特征，并将其作为辅助条件引导扩散过程，从根本上避免了脚滑动伪影。消融实验证实，移除轨迹条件后TSI从0.40骤升至0.93（Table 2），表明轨迹条件对物理合理性至关重要。

**与在线/实时方法的对比。** **Style-ERD**（Tao et al., CVPR 2022）关注响应式在线风格迁移，采用编码器-循环解码器架构。MCM-LDM则选择扩散模型框架，牺牲了实时性（单次推理需多步去噪），但换取了更高质量的风格融合和更稳定的生成结果。这种取舍在离线应用场景（如动画制作）中是合理的。

**训练范式的根本差异。** 传统方法通常需要配对的内容-风格数据进行训练，隐式学习风格映射。MCM-LDM采用**自重建训练**策略——同一运动同时作为内容和风格输入，将风格迁移任务转化为自重建任务。这一设计的关键在于：它迫使StyleRemover组件从内容编码中剥离风格信息，否则模型将退化为简单的自编码器（CRA从35.75飙升至93.43，SRA从58.00骤降至16.88，Table 2）。这种训练范式使得模型在推理时能够自然地解耦并重组内容与风格。

### 3. 适用边界与局限

MCM-LDM的适用边界受以下因素制约：

**轨迹生成的缺失。** 当前方法聚焦于**给定轨迹条件下的风格迁移**，即轨迹条件仅在输入轨迹可用时发挥作用，无法自主生成具有任意轨迹的动画。这意味着模型不能从零开始创造新的运动路径，而只能对现有轨迹进行风格化。对于需要轨迹创意生成的应用场景（如自动编排舞蹈走位），该方法存在根本性局限。

**时间范围的泛化约束。** 模型性能受限于训练数据（HumanML3D，14,616条序列）的时间分布。对于超出训练时长的运动序列或分布外动作类型，风格迁移质量可能显著下降。这是扩散模型在序列生成任务中的共性问题——去噪过程依赖于训练数据的统计规律，对未见过的运动模式缺乏泛化保证。

**环境交互建模的空白。** 当前方法未对环境交互（如物体抓取、地面适应、障碍物避让等）进行建模。在复杂场景下，风格化运动可能出现物理不合理性，例如脚部穿透地面或手部与物体错位。这一局限源于运动表示的固有约束——MCM-LDM仅在运动学层面操作，缺乏动力学约束和场景感知能力。

**实时性不足。** 扩散模型的多步去噪推理过程（约需数十至数百步）使得该方法难以直接应用于实时交互场景。对于需要低延迟响应的应用（如游戏角色实时控制），需要额外的蒸馏或加速策略。

### 4. 开放问题与未来方向

基于上述局限，以下开放问题值得进一步探索：

**多模态驱动的风格化生成。** 如何将MCM-LDM扩展为文本或音乐驱动的动作生成与风格化？当前方法需要显式的风格运动作为输入，而文本/音乐条件将极大降低使用门槛。这需要设计跨模态条件对齐机制，将语义或节奏信息映射到运动风格空间。

**长序列运动的一致性保障。** 如何提升模型对长时间序列的运动一致性和稳定性？扩散模型在生成长序列时容易出现累积误差，导致运动漂移。可能的解决方向包括引入层次化生成策略、循环一致性约束或基于物理的修正模块。

**数据高效与自监督风格解耦。** 是否可能利用更少的标注数据或自监督方式学习风格解耦？当前方法依赖预训练的MotionCLIP进行风格提取，而MotionCLIP本身需要大量标注数据进行对比学习。探索基于运动增强、时序对比学习或解耦表征学习的自监督策略，有望降低数据依赖。

**细粒度部分身体风格化。** 如何进一步解耦风格与内容，实现更细粒度的部分身体风格化？当前方法对整个身体应用统一的风格变换，但实际应用中可能需要仅对特定身体部位（如手臂摆动风格）进行迁移，而保持其他部位不变。这需要设计部位感知的条件注入机制和空间解耦策略。

**与物理仿真引擎的融合。** 如何将运动学层面的风格迁移与物理仿真引擎结合，以解决环境交互和物理合理性约束？将MCM-LDM的输出作为物理仿真器的参考轨迹，通过在线优化修正不合理的接触力和运动学约束，是提升生成运动物理可信度的潜在路径。

**注意：** 由于部分基线方法（如Park et al.、FineStyle等）未公开源代码，本文的定量对比基于作者根据论文描述进行的复现。不同复现质量可能影响对比的公平性，建议读者在解读具体数值时保持审慎。

## 原文 PDF

![[paperPDFs/CVPR_2024/MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Latent_Diffusion_Model.pdf]]
