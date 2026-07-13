---
title: "MotionDreamer: One-to-Many Motion Synthesis with Localized Generative Masked Transformer"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Masked_Transformer.pdf
project_link: https://motiondreamer.github.io/
code_link: null
aliases:
- MotionDreamer
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过缩小Transformer的感受野，引入滑动窗口局部注意力（SlidAttn）和码本分布正则化，强制模型聚焦于局部运动token的依赖关系，从而在保留局部模式的同时实现多样性。
primary_logic: 在量化离散隐空间中对运动局部模式进行显式分类分布建模，结合滑动窗口局部注意力以限制感受野，既能忠实保留参考运动的局部模式，又能生成多样化且新颖的运动序列。
claims:
- 在SinMotion数据集上，MotionDreamer的谐波平均值达到0.43，比最佳基线SinMDM的0.36提高19%（0.07）。
- 去除码本分布正则化损失L_token后，谐波平均值从0.43下降到0.34，覆盖率从93.47%下降到87.26%，VQ困惑度也从28.13降至24.56。
- 使用标准Transformer块（无SlidAttn）导致严重过拟合，谐波平均值仅0.07；引入SlidAttn并配合可微反量化后谐波均值提升至0.43。
- 用户研究显示，MotionDreamer在覆盖度、多样性和自然度三个维度均获得最高平均评分。
---

# MotionDreamer: One-to-Many Motion Synthesis with Localized Generative Masked Transformer

> [!tip] 核心洞察
> 在量化离散隐空间中对运动局部模式进行显式分类分布建模，结合滑动窗口局部注意力以限制感受野，既能忠实保留参考运动的局部模式，又能生成多样化且新颖的运动序列。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionDreamer：基于局部生成掩码Transformer的一对多运动合成 |
| 英文题名 | MotionDreamer: One-to-Many Motion Synthesis with Localized Generative Masked Transformer |
| 会议/期刊 | ICLR 2025 |
| Links | [Project](https://motiondreamer.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionDreamer |
| Dataset | SinMotion |

> [!tip] 效果简介
> - SinMotion 上，Harmonic Mean 0.43 vs 0.36 (SinMDM) (+0.07)；Coverage (%) 93.47 vs 91.82 (SinMDM) (+1.65)；Global Diversity 1.33 vs 1.31 (SinMDM) (+0.02)。

## 概要

**问题瓶颈**：在单参考运动（one-to-many motion synthesis）设定下，标准生成掩码Transformer因采用全局自注意力，倾向于过拟合整个序列的全局模式，无法有效学习运动内部局部模式的分布，导致生成多样性严重不足甚至模型坍塌。

**核心因果机制**：MotionDreamer通过两个关键调控“旋钮”解决上述问题——（1）引入**滑动窗口局部注意力（SlidAttn）**缩小Transformer的感受野，强制模型聚焦于局部运动token的依赖关系；（2）加入**码本分布正则化损失**（$\mathcal{L}_{\mathrm{token}}$），通过最小化KL散度促使离散码本条目的使用趋向均匀，防止码本坍缩。二者协同，在量化离散隐空间中对运动局部模式进行显式分类分布建模，既能忠实保留参考运动的局部模式，又能生成多样化且新颖的运动序列。

**方法定位**：MotionDreamer属于基于单实例学习的生成式运动合成方法，区别于基于GAN的**Ganimator**、基于扩散模型的**SinMDM**以及基于非参数优化的**GenMM**。其核心架构为**局部生成掩码Transformer（Local-M）**，在VQ-VAE离散隐空间上通过掩码预测建模运动token的局部分类分布，并采用可微反量化（sparsemax）实现端到端训练。

**主要结果**：在SinMotion数据集上，MotionDreamer的谐波均值（Harmonic Mean）达到0.43，较最佳基线SinMDM的0.36提升19%（+0.07）；覆盖度（Coverage）达93.47%，全局多样性（Global Diversity）为1.33，均优于已有方法。用户研究进一步表明，MotionDreamer在覆盖度、多样性和自然度三个感知维度上均获得最高平均评分。

**证据强度**：上述结论由多项消融实验强力支撑——移除$\mathcal{L}_{\mathrm{token}}$后谐波均值从0.43骤降至0.34（Table 2）；将SlidAttn替换为标准全局自注意力导致模型严重过拟合，谐波均值仅0.07（Table 3）。这些结果表明，感受野约束与码本正则化是该方法有效性的必要条件。



### 问题背景：单参考运动的一对多合成

在计算机动画与角色运动生成领域，从单个参考运动序列出发，生成一组在保持参考运动局部模式的同时又具备足够多样性的新运动，被称为**一对多运动合成**（one-to-many motion synthesis）。这一任务在游戏角色动画、影视特效、群体模拟等场景中具有广泛的应用需求：动画师通常仅提供一段示范运动，系统需要自动生成大量“看起来像同一类动作但又不完全重复”的变体，以丰富视觉表现力或适配不同交互情境。

该任务的核心挑战在于一个内在的**保真度–多样性权衡**（fidelity–diversity trade-off）：一方面，生成的运动必须忠实保留参考运动中的关键局部模式（如街舞中的“后空翻”衔接、“倒立”姿态）；另一方面，生成结果之间又必须有足够的差异，避免简单复制或微小扰动。早期的运动合成方法，如基于运动图（motion graph）或运动匹配（motion matching）的拼接式策略，虽然能保证局部模式的精确性，但生成的多样性受限于数据库中可用的片段组合，难以产生真正新颖的运动序列。近年来，深度生成模型——特别是生成对抗网络（GAN）、扩散模型（diffusion model）和生成式Transformer——为这一任务提供了端到端的参数化方案，但在单参考运动的极端数据稀缺条件下，这些方法普遍面临**过拟合**与**模式坍塌**（mode collapse）的困境。

### 现有方法缺口：全局感受野导致的过拟合与多样性不足

从生成建模的角度审视，一对多运动合成的难点在于：模型需要从**仅一条**运动序列中学习其内部模式的分布。现有基于Transformer的生成式掩码模型（generative masked transformer）通常采用标准的多头自注意力机制，其全局感受野使每个位置的token可以关注序列中的所有其他位置。这种设计在数据充足的场景下有利于捕获长程依赖，但在单序列学习时却成为致命的弱点——模型倾向于记忆整个序列的全局模式，而非学习可泛化的局部模式组合方式，导致以下两个关键失败模式：

1. **过拟合到参考序列**：模型退化为对输入序列的“复制–粘贴”，仅能生成与参考运动高度相似的序列，无法产生有意义的变体。定量上，这表现为全局多样性（Global Diversity）和局部多样性（Local Diversity）指标极低。
2. **模式坍塌**：在向量量化（VQ）的离散隐空间中，码本（codebook）的条目利用极度不均衡——少数几个码本条目被频繁使用，而大量条目处于“死亡”状态。这严重压缩了运动token的组合空间，使模型缺乏表达不同模式组合的能力。

在MotionDreamer出现之前，针对单实例运动合成的主流方法包括：**Ganimator**（基于GAN，通过多尺度金字塔判别器生成运动变体）、**SinMDM**（基于扩散模型，在单运动序列上训练去噪扩散过程）、以及**GenMM**（基于非参数的运动匹配与混合优化）。这些方法虽然在特定指标上各有优势，但均未从**感受野约束**和**离散隐空间分布建模**的角度系统性地解决上述过拟合与模式坍塌问题。尤其是基于Transformer的生成式方案，其全局自注意力机制本身就成为多样性生成的瓶颈。

### 本文动机：缩小感受野以学习局部模式分布

MotionDreamer的核心动机源于一个关键的观察：**运动序列的多样性主要来源于其内部局部模式的不同组合方式，而非全局结构的改变**。一段“地板动作组合”（floor combo）由若干原子模式（如旋转、支撑、过渡姿态）按特定时序拼接而成；生成多样化的变体，本质上是在保持这些原子模式质量的前提下，重新排列或替换其中的部分片段。因此，模型真正需要建模的，是这些局部模式在离散隐空间中的**分类分布**（categorical distribution），而非整个序列的全局联合分布。

基于这一洞察，MotionDreamer提出了一条与现有方法截然不同的技术路径：**通过策略性地缩小Transformer的感受野，强制模型聚焦于运动token的局部依赖关系，从而在离散隐空间中学习局部模式的显式分类分布**。具体而言，该方法引入了三个相互协同的机制：

- **滑动窗口局部注意力（SlidAttn）**：替代标准的全局自注意力，将运动token序列展开为重叠的局部窗口，每个窗口内独立计算注意力。这使得每个位置的预测仅依赖于其邻近的局部上下文，有效防止模型“看到”整个序列而过拟合到全局模式。
- **码本分布正则化（Codebook Distribution Regularization）**：在VQ码本训练阶段，额外引入基于KL散度的正则化损失 $\mathcal{L}_{\mathrm{token}}$，促使码本条目的使用分布接近均匀分布，从而最大化离散隐空间的表达能力，缓解单序列训练时的码本坍塌。
- **可微反量化与重叠注意力融合（Sparsemax Dequantization & AttnFuse）**：通过sparsemax替代不可微的argmax操作，使梯度可以从重建损失回传至Local-M Transformer；同时，AttnFuse模块对齐并融合重叠窗口区域的注意力输出，保证局部模式之间的平滑过渡。

这一设计哲学可以概括为：**在量化离散隐空间中，对运动局部模式进行显式分类分布建模，结合滑动窗口局部注意力以限制感受野，既能忠实保留参考运动的局部模式，又能生成多样化且新颖的运动序列**。后续的实验系统性地验证了这一假设：当使用标准Transformer块（无SlidAttn）时，模型严重过拟合，谐波均值（Harmonic Mean）仅0.07；引入SlidAttn并配合可微反量化后，谐波均值跃升至0.43，充分证明了感受野约束在单实例运动生成中的关键作用。



## 核心方法与创新机理

MotionDreamer 的核心创新在于将标准生成掩码 Transformer 的**全局自注意力**替换为**滑动窗口局部注意力（SlidAttn）**，并辅以**码本分布正则化**与**可微反量化**，从而在单参考运动合成中同时实现高保真局部模式保留与高多样性生成。

### 瓶颈与因果机制

标准生成掩码 Transformer 在单参考运动合成时，由于采用全局自注意力，模型倾向于过拟合到整个序列的全局模式，无法有效学习运动内部局部模式的分布，导致生成多样性差或模型坍塌。MotionDreamer 通过以下因果路径解决该问题：

1. **缩小感受野以强制局部学习**：引入 SlidAttn 层，将运动 Token 序列展开为重叠的局部窗口，在每个窗口内使用可学习查询和相对位置编码计算注意力（式 8），使模型只能访问局部上下文，从而被迫学习局部运动模式的依赖关系。
2. **码本分布正则化防止码本坍缩**：在 VQ 训练阶段额外引入基于 KL 散度的正则化损失 $\mathcal{L}_{\mathrm{token}} = KL(P_{post}, P_{prior})$（式 4），促使码本条目使用分布接近均匀分布，避免单序列训练时码本利用率不足。
3. **可微反量化打通梯度流**：将传统 VQ 的 argmax 操作替换为 **sparsemax** 激活函数，使 Token 选择过程可微，梯度能从重建损失反向传播至 Local-M Transformer，实现端到端优化。
4. **重叠注意力融合（AttnFuse）**：在对齐相邻窗口的注意力输出后，对重叠区域进行投票融合，替代标准平均池化，以更有效地保留模式并产生平滑过渡。

### 与基线方法的关键差异

| 技术组件 | 基线方法 | MotionDreamer |
|---------|---------|---------------|
| 注意力机制 | 标准全局自注意力 | 滑动窗口局部注意力（SlidAttn），配合可学习查询和相对位置编码 |
| 码本训练正则化 | 仅 VQ 承诺损失 + EMA | 额外加入 $\mathcal{L}_{\mathrm{token}}$（KL 散度正则化） |
| 反量化方式 | argmax（不可微） | sparsemax（可微反量化） |
| 窗口输出融合 | 标准平均池化 | AttnFuse（对齐并投票融合重叠区域） |

### 决定性证据

消融实验（Table 3）直接验证了核心创新的因果效应：使用标准 Transformer 块（无 SlidAttn）导致严重过拟合，谐波均值仅 0.07；引入 SlidAttn 并配合可微反量化后，谐波均值跃升至 0.43。此外，移除码本正则化损失 $\mathcal{L}_{\mathrm{token}}$ 后，谐波均值从 0.43 降至 0.34，VQ 困惑度从 28.13 降至 24.56（Table 2），证实了正则化对码本利用率和生成质量的关键作用。

### 设计理念

MotionDreamer 的核心洞察在于：在量化离散隐空间中对运动局部模式进行显式分类分布建模，结合滑动窗口局部注意力以限制感受野，既能忠实保留参考运动的局部模式，又能生成多样化且新颖的运动序列。这一设计使得模型在 SinMotion 数据集上取得了 0.43 的谐波均值，相比最佳基线 SinMDM 的 0.36 提升 19%。



MotionDreamer 的整体 pipeline 围绕“在量化离散隐空间中显式建模运动内部模式的分类分布”这一核心思想构建，由两个阶段组成：**运动Token化（VQ阶段）** 与 **局部掩码生成建模（Local-M Transformer阶段）**。

### 阶段一：运动Token化

给定一段参考运动序列 $\mathbf{\sigma}^{m_{1:L}}$，首先通过**1D卷积编码器 $E$** 将其映射为特征向量序列：

$$z_{1:N} = E(m_{1:L})$$

随后，通过**向量量化（VQ）** 将每个特征向量映射到可学习码本 $\mathcal{C}$ 中最近的条目，得到离散的运动Token序列：

$$\mathbf{c}_{1:N} = Q(z_{1:N}; \mathcal{C})$$

最后，**1D卷积解码器 $D$** 将Token序列重建为运动序列：

$$\hat{m}_{1:L} = D(\mathbf{c}_{1:N})$$

该阶段的训练损失由三部分组成：

$$\mathcal{L}_{\mathrm{VQ}} = \mathcal{L}_{\mathrm{rec}} + \beta_q \mathcal{L}_q + \beta_k \mathcal{L}_{\mathrm{token}}$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为重建损失，$\mathcal{L}_q$ 为VQ承诺损失。关键创新在于引入了**码本分布正则化损失** $\mathcal{L}_{\mathrm{token}}$，通过最小化后验Token分布与均匀先验之间的KL散度，防止单序列训练时的码本坍缩：

$$\mathcal{L}_{\mathrm{token}} = KL(P_{post}, P_{prior}) = -\sum_{k=1}^{K} p_k \log\left(\frac{1/K}{p_k}\right)$$

### 阶段二：局部掩码生成建模

在获得运动Token序列后，**Local-M Transformer ($p_\phi$)** 通过掩码预测的方式，显式建模运动Token的局部分类分布。其核心组件为**滑动窗口局部注意力层（SlidAttn）**，通过将Token序列展开为重叠的局部窗口，并在每个窗口内使用可学习查询和相对位置编码计算注意力，从而将感受野限制在局部范围内：

$$\mathbf{Attn}_t = \mathrm{softmax}\left(\frac{\mathbf{q}_t \mathbf{K}_W + \mathbf{r}}{\sqrt{d_k}}\right) \mathbf{V}_W$$

重叠窗口的注意力输出通过**重叠注意力融合（AttnFuse）** 进行对齐和投票融合，以保留模式并产生平滑过渡。此外，采用**Sparsemax可微反量化**替代传统的argmax操作，使梯度能从重建损失反向传播至Transformer。Local-M的总损失为：

$$\mathcal{L}_{\mathrm{M}} = \mathcal{L}_{\mathrm{mask}} + \lambda_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}}$$

### 数据流总览

整个pipeline的数据流为：**参考运动 → 1D卷积编码 → 向量量化（码本映射）→ 运动Token序列 → Local-M Transformer（SlidAttn + AttnFuse + Sparsemax反量化）→ 生成Token → 解码器重建 → 多样化运动输出**。Figure 2(a) 完整展示了这一架构，Figure 2(b) 可视化了Local-M对内部模式分类分布的显式建模能力——模型为每个掩码位置预测多个候选Token，从而实现对局部模式组合的多样化表达。

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/002_Figure_2.jpg]]
*Figure 2: (a) Overview of MotionDreamer based on localized generative masked transformer. The single reference motion*

### 补充图表

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/011_Figure_8.jpg]]
*Figure 8: (a) Inference pipeline illustration. (b) Single Motion-Beat Tokenization for beat-aligned dance synthesis*

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the one-to-many motion synthesis. A single reference motion with arbitrary skeletons can be applied to generate natural and diverse novel motions while preserving the reference local motion patterns. Above shows the diverse generations from MotionDreamer of a girl doing breakdance (upper); a jaguar attacking (bottom)*



### 3.1 运动Token化与码本学习

MotionDreamer 的第一阶段是将连续的参考运动序列映射为离散的运动Token序列，该过程通过向量量化（VQ）实现。

**编码器 (E)**：一个1D卷积编码器接收参考运动序列 $m_{1:L}$，输出特征向量序列：

$$z_{1:N} = E(m_{1:L})$$

**向量量化 (Q)**：将每个特征向量 $z_i$ 映射到可学习码本 $\mathcal{C} = \{e_k\}_{k=1}^K$ 中距离最近的条目，得到离散Token序列：

$$\mathbf{c}_{1:N} = Q(z_{1:N}; \mathcal{C})$$

**解码器 (D)**：1D卷积解码器将运动Token序列重建为运动序列：

$$\hat{m}_{1:L} = D(\mathbf{c}_{1:N})$$

**码本分布正则化损失**：在单序列训练场景下，标准VQ极易出现码本坍缩（codebook collapse），即仅少数码本条目被频繁使用。MotionDreamer 引入基于KL散度的码本分布正则化损失 $\mathcal{L}_{\mathrm{token}}$，强制码本条目的使用分布 $P_{post}$ 接近均匀先验 $P_{prior}$：

$$\mathcal{L}_{\mathrm{token}} = KL(P_{post}, P_{prior}) = -\sum_{k=1}^{K} p_k \log\left(\frac{1/K}{p_k}\right)$$

其中 $p_k$ 为第 $k$ 个码本条目的使用频率，$K$ 为码本大小。该损失是解决单实例运动合成中码本利用不足的关键调控手段。

**VQ阶段总损失**：

$$\mathcal{L}_{\mathrm{VQ}} = \mathcal{L}_{\mathrm{rec}} + \beta_q \mathcal{L}_q + \beta_k \mathcal{L}_{\mathrm{token}}$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为重建损失，$\mathcal{L}_q$ 为标准VQ承诺损失，$\beta_q$ 和 $\beta_k$ 为权重系数。

### 3.2 Local-M Transformer：局部生成掩码建模

第二阶段，MotionDreamer 使用 Local-M Transformer $p_\phi$ 对运动Token序列的局部分类分布进行显式建模。其核心瓶颈在于：标准生成掩码Transformer采用全局自注意力，在单参考运动场景下会过拟合到整个序列的全局模式，无法有效学习运动内部局部模式的分布，导致生成多样性差或模型坍塌。

**因果调节变量**：通过缩小Transformer的感受野，引入滑动窗口局部注意力（SlidAttn）和码本分布正则化，强制模型聚焦于局部运动Token的依赖关系。

**Local-M总损失**：

$$\mathcal{L}_{\mathrm{M}} = \mathcal{L}_{\mathrm{mask}} + \lambda_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}}$$

其中 $\mathcal{L}_{\mathrm{mask}}$ 为掩码预测损失，$\mathcal{L}_{\mathrm{rec}}$ 为重建损失，$\lambda_{\mathrm{rec}}$ 为权重系数。

#### 3.2.1 滑动窗口局部注意力（SlidAttn）

SlidAttn 是 Local-M Transformer 的核心模块，通过限制注意力计算范围来强制模型学习局部模式依赖。具体地，运动Token序列被展开为重叠的局部窗口，每个窗口大小为 $W$，步长为 $S$。在每个局部窗口内，使用可学习的查询向量 $\mathbf{q}_t$ 和相对位置编码 $\mathbf{r}$ 计算注意力：

$$\mathbf{Attn}_t = \mathrm{softmax}\left(\frac{\mathbf{q}_t \mathbf{K}_W + \mathbf{r}}{\sqrt{d_k}}\right) \mathbf{V}_W$$

其中 $\mathbf{K}_W$ 和 $\mathbf{V}_W$ 分别为窗口内的键和值矩阵，$d_k$ 为键的维度。

#### 3.2.2 重叠注意力融合（AttnFuse）

由于滑动窗口之间存在重叠区域，同一Token可能在不同窗口中获得多个注意力输出。AttnFuse 通过对齐并投票融合重叠区域的注意力输出，替代标准平均池化聚合，以更有效地保留局部模式并产生平滑的模式间过渡。

#### 3.2.3 可微反量化（Sparsemax）

标准VQ使用不可微的argmax操作选择码本条目，阻碍梯度从重建损失反向传播至Local-M Transformer。MotionDreamer 采用sparsemax激活函数实现可微反量化，使梯度能够畅通地流经Token选择过程，从而端到端优化生成质量。

### 补充图表

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/008_Figure_5.jpg]]
*Figure 5: Ablation study on codebook distribution regularization technique based on optimizing Ltoken. Color closer to green representing higher per-frame similarity while color closer to orange referring to lower similarity*

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/009_Figure_6.jpg]]
*Figure 6: Ablation study on overlap attention fusion (AttnFuse). “Ours w/o. AttnFuse” refers to applying standard average pooling aggregation as the alternative baseline to AttnFuse. “backflip”, “handstand” pattern and transition between two patterns are marked. For generated motions, color closer to the pattern colors indicates higher per-frame similarity with the corresponding pattern, while color closer to orange indicates lower similarity*



## 实验与关键发现

### 核心实验设置

MotionDreamer 在 SinMotion 数据集上进行评估，该数据集包含 30 个来自 Mixamo 的运动序列和 30 个来自 Truebone‑ZOO 的运动序列，其中 30 个为长序列（>600 帧），30 个为短序列（≤600 帧）。评估指标覆盖多个维度：覆盖率（Coverage）、全局多样性（Global Diversity）、局部多样性（Local Diversity）、类间多样性（inter diversity）、类内多样性差异（intra diversity diff），并以谐波均值（Harmonic Mean, HE）作为综合评价指标，其定义为：

$$HE = \frac{H}{\frac{1}{x_1} + \frac{1}{x_2} + \dots + \frac{1}{x_H}}$$

其中 $x_i$ 为各指标的标准化分数，$H$ 为指标数量。所有对比方法对每个参考运动随机生成 20 个样本以确保公平比较。

### 主实验结果

Table 1 展示了 MotionDreamer 与现有单实例运动合成方法的定量对比。MotionDreamer 在谐波均值上达到 **0.43**，相比最强基线 SinMDM 的 0.36 提升了 **19%（+0.07）**，在所有方法中取得最优综合性能。在覆盖率方面，MotionDreamer 达到 93.47%，优于 SinMDM 的 91.82%；全局多样性为 1.33，同样略高于 SinMDM 的 1.31。这表明 MotionDreamer 在保持参考运动局部模式的同时，能够生成更多样化的运动序列。

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods on SinMotion dataset. Bold marks the best result, and underline notes the second best*

定性对比（Figure 3）以 hiphop 舞蹈样本为例，展示了各方法在复杂模式（Pattern A 和 Pattern B）上的生成效果：MotionDreamer 成功复现了两种困难模式，而 Ganimator、GenMM 和 SinMDM 均存在模式丢失或生成质量下降的问题。

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison on “hiphop dance” sample from Mixamo. Pattern A and B refer to two difficult patterns presented in the reference motion. Patterns that show up in generated motions are framed out marked as either success or failure according to its quality*

用户研究（Figure 4）从覆盖度、多样性和自然度三个维度进行主观评估，MotionDreamer 在所有维度均获得最高平均评分，进一步验证了其生成结果在感知质量上的优势。

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/005_Figure_4.jpg]]
*Figure 4: Score distribution and average score results from user study. The score level ranges from 1 to 5 of assessing Coverage, Diversity and Naturalness. The bars align with the right y-axis referring to percentage of votes of each method in each score level, and the horizontal lines align with left y-axis labeling the average score of each method*

### 消融实验

**码本分布正则化（Table 2）。** 移除码本分布正则化损失 $\mathcal{L}_{\mathrm{token}}$ 后，谐波均值从 0.43 降至 0.34，覆盖率从 93.47% 降至 87.26%，VQ 困惑度从 28.13 降至 24.56。这表明 $\mathcal{L}_{\mathrm{token}}$ 通过 KL 散度约束码本使用分布接近均匀先验，有效缓解了单序列训练时的码本坍缩问题，提升了码本条目的利用率和生成质量。

**Local‑M Transformer 架构（Table 3）。** 使用标准 Transformer 块（无 SlidAttn）导致严重过拟合，谐波均值仅为 0.07；引入滑动窗口局部注意力（SlidAttn）后谐波均值提升至 0.43。进一步配合可微反量化（sparsemax）后，模型在保留局部模式的同时实现了更好的多样性。这验证了缩小感受野是解决单参考运动生成中过拟合问题的关键机制。

**重叠注意力融合（AttnFuse）。** Figure 6 的定性消融显示，相比标准平均池化聚合，AttnFuse 通过对齐并投票融合重叠窗口区域的注意力输出，能更有效地保留“backflip”和“handstand”等局部模式，并在模式间产生更平滑的过渡。

**滑动窗口参数（Table 6）。** 在窗口大小 $W=5$、步长 $S=4$（即窗口重叠为 $W-S=1$）的设置下，谐波均值取得最佳效果，兼顾了多样性与模式保留。

**码本正则化的泛化性（Table 7）。** 将 $\mathcal{L}_{\mathrm{token}}$ 应用于其他基于 VQ 的运动表示方法（如 T2M‑GPT、MoMask）时，同样观察到 VQ 困惑度和重建质量的提升，表明该正则化策略具有一定的通用性。

### 失败模式与局限性

尽管 MotionDreamer 在单参考运动合成上取得了显著提升，其性能高度依赖参考运动的质量：当参考运动包含模糊或不连贯的模式时，生成结果的质量会明显下降。此外，由于模型基于单实例学习，难以泛化到更广泛的运动编辑和条件合成任务。SlidAttn 的设计虽然有效捕获了局部依赖，但对长距离依赖和全局模式的建模能力有限，在需要全局一致性的长序列生成场景中可能存在不足。

### 补充图表

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/006_Table_2.jpg]]
*Table 2: Ablation study on VQ regulatization strategies on SinMotion dataset. Bold text marks the best result*

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/007_Table_3.jpg]]
*Table 3: Ablation study on architecture of Local-M transformer on SinMotion dataset. Bold text marks the best result, and underline notes the second best*

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/014_Table_6.jpg]]
*Table 6: Ablation study for parameter settings. Bold text marks the best result*

![[assets/figures/papers/paper_list_l1902_MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Mas/figures/015_Table_7.jpg]]
*Table 7: Impact of codebook regularization loss on other VQ methods for motion representation. Bold text marks the best result*



## 定位与知识库关联

### 问题域与核心瓶颈

一对多运动合成（One-to-Many Motion Synthesis）要求仅从单条参考运动生成多样化且自然的新运动序列。该任务的核心瓶颈在于：标准生成掩码Transformer采用全局自注意力，在单序列训练时倾向于过拟合到整个序列的全局模式，无法有效学习运动内部局部模式的分布，导致生成多样性差或模型坍塌。

### 与现有方法的差异化定位

MotionDreamer的方法定位可从以下四个关键维度与基线方法进行区分：

**1. 生成范式：掩码预测 vs. 扩散 vs. 匹配**

现有单实例运动合成方法主要分为三类：基于GAN的**Ganimator**、基于扩散模型的**SinMDM**，以及基于非参数运动匹配与混合的**GenMM**。MotionDreamer采用生成掩码Transformer范式，在量化离散隐空间中对运动Token进行分类分布建模，这与扩散模型的连续去噪过程和匹配方法的显式拼接策略有本质不同。

**2. 感受野控制：局部注意力 vs. 全局注意力**

标准生成掩码Transformer使用全局自注意力，导致模型过拟合（谐波均值仅0.07，见Table 3）。MotionDreamer引入**滑动窗口局部注意力（SlidAttn）**，通过限制感受野强制模型聚焦于局部运动Token依赖关系，这是方法有效性的核心因果旋钮。

**3. 码本训练策略：分布正则化 vs. 标准VQ**

传统VQ仅使用承诺损失和EMA更新码本，在单序列训练时容易出现码本坍缩。MotionDreamer额外引入基于KL散度的码本分布正则化损失$\mathcal{L}_{\mathrm{token}}$，促使码本条目使用接近均匀分布。消融实验（Table 2）表明，移除该损失后VQ困惑度从28.13降至24.56，覆盖率从93.47%降至87.26%，谐波均值从0.43降至0.34。

**4. 反量化策略：可微sparsemax vs. 不可微argmax**

标准VQ使用argmax进行反量化，梯度无法回传至编码器。MotionDreamer采用sparsemax激活函数实现可微反量化，使重建损失梯度能有效反向传播。消融实验（Table 3）证实，仅有SlidAttn而无可微反量化时谐波均值为0.37，两者结合后提升至0.43。

### 适用边界

- **强依赖参考质量**：方法性能高度依赖参考运动的质量，低质量或缺乏明确局部模式的参考运动可能导致生成退化。
- **单实例学习局限**：由于基于单实例学习范式，难以直接泛化到更广泛的运动编辑和条件合成任务（如文本驱动、多模态控制）。
- **长程依赖受限**：滑动窗口局部注意力在捕获长距离依赖和全局模式方面能力有限，对需要全局协调的复杂运动（如长时间舞蹈编排）可能表现不足。

### 局限与开放问题

**已识别局限**：
1. 性能高度依赖参考运动质量；
2. 基于单实例学习，难以泛化到更广泛的运动编辑和条件合成任务；
3. 对长距离依赖和全局模式的捕获能力有限。

**待探索的开放问题**：
1. 如何将MotionDreamer推广到少样本或大规模数据集，同时保持生成质量？
2. 是否可以引入熵正则化或随机采样策略进一步优化码本利用率？
3. 如何设计更鲁棒的注意力机制，以同时捕获局部模式与长程依赖？
4. 滑动窗口局部注意力在处理极长运动序列时的效率与效果如何？



## 原文 PDF

![[paperPDFs/ICLR_2025/MotionDreamer_One_to_Many_Motion_Synthesis_with_Localized_Generative_Masked_Transformer.pdf]]
