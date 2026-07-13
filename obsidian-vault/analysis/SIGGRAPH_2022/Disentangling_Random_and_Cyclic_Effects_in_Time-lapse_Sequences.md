---
title: Disentangling Random and Cyclic Effects in Time-lapse Sequences
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Disentangling_Random_and_Cyclic_Effects_in_Time_lapse_Sequences.pdf
project_link: null
code_link: "https://github.com/harskish/tlgan"
aliases:
- TCCG
- DRCETLS
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 基于时间戳的傅里叶特征条件输入与隐空间解耦：通过将时间分解为日/年正弦分量和线性趋势分量，并采用条件噪声增强策略，迫使模型将随机性归入潜在变量而将确定性变化归入条件输入。
primary_logic: 将GAN隐空间用于承载随机变化（如天气），而将周期性和趋势性变化通过傅里叶特征编码的条件输入进行控制；通过风格调制机制和判别器时间戳扰动，模型无需回归到特定训练图像，而是学习在给定条件下生成多样但合理的图像，从而实现各类变化因素的解耦。
claims:
- 隐向量控制天气状态，时间信号控制昼夜与季节，二者相互解耦，如Figure 6所示，同一时间戳不同隐码可生成不同天气的图像。
- 移除时间戳噪声增强会导致模型坍缩，仅生成少数模板帧，随机变化消失（Figure 12）。
- 消融实验表明，所提风格调制条件机制（Ablation A）能够更好实现趋势与周期解耦，而拼接条件（Ablation B/C）容易导致纠缠（Figures 14, 15）。
- 所提方法在增加控制能力的同时未牺牲图像质量，与无条件StyleGAN2的FID相当（Table 2）。
---

# Disentangling Random and Cyclic Effects in Time-lapse Sequences

> [!tip] 核心洞察
> 将GAN隐空间用于承载随机变化（如天气），而将周期性和趋势性变化通过傅里叶特征编码的条件输入进行控制；通过风格调制机制和判别器时间戳扰动，模型无需回归到特定训练图像，而是学习在给定条件下生成多样但合理的图像，从而实现各类变化因素的解耦。

| 字段 | 内容 |
|------|------|
| 中文题名 | 解开时间推移序列中的随机与周期效应 |
| 英文题名 | Disentangling Random and Cyclic Effects in Time-lapse Sequences |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2207.01413) · [Code](https://github.com/harskish/tlgan) · [paper](https://arxiv.org/abs/2207.01413") |
| Topic | #topic/other_unclear |
| Method | TLGAN (Cyclic Conditioning GAN) |
| Dataset | 自数据集（AMOS + 自建植物生长集）, Mielipidepalsta数据集（与Martin-Brualla et al. 2015对比） |

> [!tip] 效果简介
> - 自数据集（AMOS + 自建植物生长集） 上，FID 3.51 ~ 11.11（详见Table 2，如Valley 3.83, Two Medicine 4.76） vs 无条件StyleGAN2（相近值） (图像质量无系统性下降（Table 2声明）)。
> - Mielipidepalsta数据集（与Martin-Brualla et al. 2015对比） 上，定性清晰度 移动物体（如植物、椅子）显著更清晰 vs Martin-Brualla et al. 2015产生模糊结果 (定性显著提升)。

## 概要

原始延时摄影序列中，天气、遮挡等随机变化与昼夜、季节等确定性周期变化及长期趋势相互纠缠，导致视觉闪烁且无法单独控制。本文提出**TLGAN**，一种基于条件生成对抗网络的时间推移序列解耦方法。其核心思路是：将GAN的隐空间用于承载随机变化（如天气），而将日周期、年周期和全局趋势通过傅里叶特征编码为条件信号，以**风格调制**方式注入StyleGAN2生成器，迫使模型将随机性归入隐变量、将确定性变化归入条件输入。训练中引入时间戳去量化和判别器时间戳扰动，防止模型坍缩为少数模板帧。在多个自建延时数据集上，TLGAN实现了图像质量与无条件StyleGAN2相当（FID无系统性下降），同时首次将时间推移序列中的随机、周期和趋势变化因素有效解耦，支持独立控制昼夜、季节和天气效果。该方法为每段序列单独训练模型，依赖手工预处理对齐，尚未实现端到端学习。

## 核心方法与创新机理

### 问题瓶颈与设计动机

原始延时摄影序列中存在三类外观变化的深度纠缠：**随机变化**（天气、遮挡、光照瞬变）、**确定性周期变化**（昼夜循环、季节更替）与**长期趋势**（植物生长、建筑施工）。传统方法难以将这些因素解耦——直接对时间戳进行条件生成的GAN容易将随机变化归因于时间信号，导致生成结果闪烁或缺乏多样性；而去闪烁方法（如Martin-Brualla et al., TOG 2015）虽能稳定画面，却会抹除移动内容，产生模糊。核心瓶颈在于：**如何让模型理解“同一时刻可以有不同的天气”，同时让昼夜与季节变化被确定性地控制**。

TLGAN的核心洞察是：**将GAN的隐空间分配给随机变化承载，而将周期性/趋势性变化通过精心设计的条件机制进行确定性控制**。这一分工通过三个关键设计实现：傅里叶特征编码、风格调制条件注入、以及时间戳噪声增强策略。

### 条件信号编码：从标量时间到解耦的傅里叶特征

原始时间戳仅是一个标量，无法显式表达不同时间尺度的周期性。TLGAN将每个训练帧的时间戳分解为三个独立分量——**日时间** $t_d$（归一化到[0,1)）、**年时间** $t_y$（归一化到[0,1)）、**全局趋势** $t_g$（以年为单位的时间偏移）——并通过傅里叶特征将其编码为高维条件向量：

$$
\mathbf{c}(t_d, t_y, t_g) = \begin{bmatrix} \sin(2\pi f_0 t_d) \\ \cos(2\pi f_0 t_d) \\ \sin(2\pi f_1 t_y) \\ \cos(2\pi f_1 t_y) \\ t_g \cdot k \\ 1 \end{bmatrix}
$$

其中 $f_0=1$ 对应日周期，$f_1=1$ 对应年周期，$k=10^{-2}$ 是趋势分量的缩放因子。正弦/余弦对的引入使得相邻时刻的条件向量在环面上连续，而非在欧氏空间中跳跃，这对学习周期性变化至关重要。趋势分量仅使用线性项，并通过极小的 $k$ 值抑制其幅值，防止全局趋势主导条件信号而导致隐变量失效。

### Changed Slot 1：条件注入机制——从拼接到风格调制

传统条件GAN（Mirza & Osindero, 2014）将条件向量与隐变量拼接后输入网络，这容易导致条件信号与隐空间信息相互纠缠。TLGAN提出**逐层风格调制**机制，改变了条件信号的作用方式：

在StyleGAN2生成器的每一层 $i$，条件向量 $\mathbf{c}$ 通过一个可学习的线性变换 $L_i$ 映射为尺度向量 $\mathbf{k}_i = L_i \mathbf{c}$，然后对原始风格向量 $\mathbf{s}_i$ 进行逐元素调制（Hadamard乘积）：

$$\mathbf{s}'_i = \mathbf{k}_i \odot \mathbf{s}_i$$

这一设计的关键优势在于：**条件信号仅通过乘性缩放来控制风格的“强度”，而非直接决定风格的内容**。这使得模型可以学习到——例如，日周期信号主要调制光照相关特征的强度，年周期信号调制植被颜色，而隐变量 $\mathbf{z}$ 则自由控制天气等随机因素。消融实验（Figure 14, 15）证实，拼接条件机制会导致年周期与趋势纠缠，或日周期错误地控制了本应由趋势处理的变化，而风格调制则实现了清晰解耦。

### Changed Slot 2：训练正则化——时间戳去量化与判别器扰动

为防止模型将训练帧视为孤立样本而坍缩为记忆化生成，TLGAN引入了两项关键的训练正则化策略：

**时间戳去量化**：对于第 $j$ 帧，在将其时间戳输入生成器前，添加高斯噪声 $\varepsilon \sim \mathcal{N}(0, \max(T_{j+1}-T_j, T_j-T_{j-1})/2)$。噪声标准差正比于该帧与相邻帧的时间距离——稀疏采样区域的帧获得更大的时间不确定性。这迫使生成器理解：给定一个大致的时间戳，存在多种合理的图像（不同天气、不同瞬时条件），从而将随机变化归入隐变量。

**判别器时间戳扰动**：在判别器端，对年时间分量 $t_y$ 和趋势分量 $t_g$ 分别添加独立高斯噪声（$\sigma_g \in \{1.5\text{年}, 2\text{年}\}$，依数据集而定）。这一操作使得判别器无法通过精确匹配时间戳来区分真假，从而阻止生成器将随机变化“编码”到条件信号中。如论文所述，这等价于“膨胀”训练数据——单个时刻对应一个更大的合理图像集合，这些图像与给定的日/年时间大致一致。

Figure 12的消融实验提供了决定性证据：**移除时间戳噪声增强后，隐变量的方差趋于零，模型坍缩为仅生成少数模板帧**，完全丧失随机变化表达能力。

### 完整训练与推理路径

**训练流程**：
1. 从延时序列中采样真实图像及其时间戳 $(t_d, t_y, t_g)$
2. 对时间戳进行去量化扰动后，编码为傅里叶特征向量 $\mathbf{c}$
3. 从标准正态分布采样隐变量 $\mathbf{z}$，经映射网络得到风格向量 $\mathbf{s}$
4. 在每一层，通过 $L_i$ 将 $\mathbf{c}$ 转换为尺度向量 $\mathbf{k}_i$，对 $\mathbf{s}_i$ 进行调制
5. 生成器合成图像，判别器接收图像及扰动后的条件向量进行真假判断
6. 判别器输出为 $D(x) = \text{normalize}(M(\mathbf{c})) \cdot D'(x)$，其中 $M(\mathbf{c})$ 是条件向量的可学习嵌入，$D'(x)$ 是判别器最后一层特征

**推理路径**：
- **控制天气**：固定时间戳，改变隐变量 $\mathbf{z}$，生成同一时刻不同天气的图像（Figure 6）
- **控制昼夜/季节**：固定隐变量，独立变化 $t_d$ 或 $t_y$，生成清晰的日循环或年循环序列（Figure 7）
- **控制趋势**：变化 $t_g$，驱动植物生长、建筑施工等长期变化（Figure 10）
- **稳定化时间推移**：选定一个隐变量，仅推进时间戳，生成无天气闪烁的平滑序列

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2207_01413/figures/007_Figure_6.jpg]]
*Figure 6: We synthesize a frame from Barn dataset at four different timestamps (rows), using four latent codes (columns). The latent codes express the weather consistently across timestamps. On each row, all differences between the images are caused by the latent codes*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2207_01413/figures/008_Figure_7.jpg]]
*Figure 7: In these six datasets, we change only the time-of-day (top 3 rows) or time-of-year (bottom 3 rows) conditioning signal. The input data shows the time-lapse image for that particular day or year, respectively. While the inputs have reasonably constant weather over a day, the same is not at all true for the whole year. When we sweep the time-of-day signal, the synthesized time-lapse images show a clear day cycle, as desired. Similarly, the time-of-year causes the time-lapse image to cycle through the seasons (note that winter is in the middle). We furthermore visualize our results using 3 different latent codes, chosen separately for each dataset to demonstrate approximately clear sky, some c...*

训练在4块NVIDIA V100 GPU上进行，1024×1024分辨率约需60小时（512×512约30小时），通常在约600万真实图像后收敛。R1正则化参数在512分辨率下为4.0，1024分辨率下为16.0，批大小为32。

### 模块间因果关系

各模块之间存在明确的因果链路：**傅里叶特征编码**提供了时间维度的结构化表示，使得日/年周期和趋势在向量空间中自然分离；**风格调制机制**决定了条件信号以何种方式影响生成——乘性调制而非加性拼接，使得条件信号控制“多少”而非“什么”；**时间戳噪声增强**则作为正则化器，强制模型将无法由时间解释的变化归入隐变量，从而完成随机与确定性的解耦。三者缺一不可：缺少傅里叶编码则周期信号难以学习；缺少风格调制则解耦不彻底；缺少噪声增强则模型坍缩。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2207_01413/figures/005_Figure_4.jpg]]
*Figure 4: StyleGAN2 architecture with our cyclic conditioning mechanism highlighted using red. Our conditioning first transforms a timestamp*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2207_01413/figures/013_Figure_12.jpg]]
*Figure 12: On rare occasions our models can start memorizing the input data, leading to a collapsed state where the time axis is reduced to a few template frames, and all random variation disappears, seen as the variance of the latent approaching zero. We have found that including timestamp noise (Section 4.2.2) and reducing the linear component scale (Equation 2) fixes the issue*

## 实验与关键发现

TLGAN在12个时间推移数据集上进行了系统评估，覆盖了从512×512到1024×1024的分辨率，训练时长约60小时（4× NVIDIA V100 GPU，1024分辨率）或30小时（512分辨率），通常需要约600万真实图像的训练量才能使FID稳定且条件信号的角色收敛。

### 图像质量保持

核心结论是：**在显著增加控制能力的同时，TLGAN并未牺牲生成图像的质量**。Table 2报告了所提方法与无条件StyleGAN2在等时长训练下的FID对比。以Valley数据集为例，TLGAN的FID为3.83，而StyleGAN2为3.51；Two Medicine数据集上TLGAN为4.76，StyleGAN2为4.11。尽管存在轻微波动，但论文明确指出“未观察到系统性的图像质量下降”，说明风格调制条件机制和判别器时间戳扰动并未引入额外的训练不稳定或模式崩塌。

### 解耦控制验证

**天气-时间解耦**：Figure 6展示了核心解耦能力的直接证据。在Barn数据集的四个不同时间戳（行）上，使用四个不同的隐码（列），隐码一致地控制天气状态（如晴朗、多云），而时间戳控制昼夜和季节变化。这意味着随机变化（天气）被成功归入潜在变量z，而确定性周期变化被条件信号捕获。

**周期信号独立控制**：Figure 7在六个数据集上分别单独变化日时间信号（上半部分）或年时间信号（下半部分），生成了清晰的昼夜循环和季节循环。Figure 5进一步展示了模型能够复现日长随季节的自然变化——同时变化24小时周期和年周期时，夏季白昼更长、冬季白昼更短的现象被准确建模。Figure 8还揭示了模型自动学习到的关联：在Normandy数据集中，日时间信号同时控制了潮汐变化，说明傅里叶特征编码能够捕捉数据中真实存在的物理关联。

**趋势信号分离**：Figure 10通过方差图可视化展示了趋势信号t_g主要控制植物生长和建筑施工等长期变化，其影响区域被高亮显示。训练动力学曲线（Figure 11）表明，隐码z、日时间t_d和年时间t_y最终各贡献约30%的输出方差，而趋势t_g贡献不足10%，这与各因素在真实世界中的影响比例相符。

### 消融实验：条件机制与训练策略

**风格调制 vs. 拼接条件**：消融实验A和B使用单标量时间输入，对比了所提风格调制机制与Mirza & Osindero（2014）的拼接条件方法。Figure 14显示，Ablation A（风格调制）仅用趋势条件就能实现趋势解耦，而Ablation B（拼接条件）导致年周期与趋势相互纠缠。更关键的Ablation C（Figure 15）使用完整循环信号，拼接条件机制错误地让日周期控制了本应由趋势处理的变化，而风格调制机制则保持了各信号的独立角色。这证实了**逐层Hadamard乘积调制**是实现解耦的关键设计选择。

**时间戳噪声增强的必要性**：Figure 12揭示了训练稳定性方面的决定性发现。当移除时间戳去量化（timestamp dequantization）和判别器时间戳扰动时，模型会发生坍缩——隐向量的方差趋近于零，模型仅记忆少数模板帧，丧失了所有随机变化能力。这一消融直接验证了噪声增强策略的因果作用：通过将单帧训练样本“膨胀”为与给定时间戳一致的可能图像集合，迫使模型将随机性归入潜在变量。

**趋势分量尺度**：论文指出将线性趋势分量乘以小尺度因子k=1e-2有助于稳定训练，防止全局趋势过强导致潜在变量失效。这一超参数选择来自经验观察，缺乏系统的敏感性分析。

### 与现有方法的对比

在Mielipidepalsta数据集上与Martin-Brualla et al.（TOG 2015）的对比中（Figure 13），TLGAN在包含移动内容的场景下展现出显著更清晰的生成结果。Martin-Brualla方法产生的图像中，移动物体（如生长的植物、移动的椅子）呈现明显模糊，而TLGAN能够生成锐利的细节。这一优势源于GAN生成范式本身——通过学习数据分布而非帧间插值或融合，避免了传统时间推移去闪烁方法的运动模糊问题。

### 失败模式与适用边界

**数据缺失的边界**：Figure 9展示了模型在极端数据缺失下的表现。Teton 2016年数据中近半数缺失（红色条纹标记），加上曝光问题导致多天数据不可用（黄绿色列），模型仍能合成合理的时间推移图像。然而，论文明确指出，若训练数据中**完全缺失某些时段**（如无任何夜景图像），模型无法合成该时段的图像——这是条件GAN的本质限制，而非方法缺陷。

**对齐误差的纠缠**：Figure 16(a)展示了一个重要的失败模式：预处理中残留的图像对齐误差会被模型作为“变化信号”学习。例如，相机对齐变化导致建筑弯曲，模型可能将这种伪影与时间条件信号错误关联。Figure 16(b)显示相机自动亮度调整也会引入非期望的纠缠，说明方法对输入预处理质量存在依赖。

**泛化限制**：每个时间推移序列需要单独训练一个模型，无法泛化到新场景。这一限制源于方法设计——模型学习的是特定场景的视觉分布，而非通用的时间变化规律。

**时间连续性缺失**：生成帧之间未显式强制时间连续性约束，可能产生帧间伪影。论文将此列为开放问题，但未提供定量评估或具体示例。

**数据需求**：方法需要覆盖至少一个完整年周期的数据才能有效学习年周期变化，对于短期数据集（仅数月），年周期信号的解耦效果可能受限。论文未对此进行系统消融。

### 证据强度总结

- **强证据**：解耦控制（Figures 6, 7, 10）、训练稳定性消融（Figure 12）、风格调制机制优势（Figures 14, 15）均有可视化结果直接支撑。
- **中等证据**：FID对比（Table 2）仅与无条件StyleGAN2比较，缺乏与其他条件GAN变体的定量对比；训练超参数（如k=1e-2）的选择缺乏消融。
- **需手动验证**：方差分解分析（Figure 11）的数值声称（各约30%）依赖于附录中的归一化方差公式，其统计显著性未经验证；时间连续性缺失的严重程度缺乏定量度量。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2207_01413/figures/017_Table_2.jpg]]
*Table 2: FIDs from equal-time training runs of our method and StyleGAN2 (unconditional). Despite the increased control provided by our method, we do not see a systematic decrease in image quality*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2207_01413/figures/015_Figure_14.jpg]]
*Figure 14: Two ablations with a single scalar time input. Ablation A: with our proposed style modulation conditioning mechanism, the input controls only trends, with all other variation ending up in the latent space. This results in seemingly broken time-lapse images that display only trend changes, and random samples that have completely random time of day and season. Ablation B: using the concatenation method of Mirza and Osindero [2014], the conditioning ends up controlling trends and time of year together, with the latent space controlling the day cycle. This results in random samples that are consistent w.r.t. the year cycle, but have inconsistent time of day*

## 定位与知识库关联

本文提出的 **TLGAN** 在时间推移序列生成任务中引入了一个核心的**方法槽位变更**：将条件GAN中传统的**拼接式条件注入**（如 **Mirza & Osindero, 2014** 的经典条件GAN范式）替换为**基于傅里叶特征的逐层风格调制机制**。这一变更的本质在于，传统拼接条件将时间信号与隐变量在输入端混合，导致模型难以区分“哪些变化应由时间驱动、哪些变化应留给随机潜变量”，从而引发周期变化与随机变化之间的纠缠。TLGAN通过将条件信号编码为日周期、年周期和全局趋势的傅里叶特征，并在生成器每一层通过可学习的线性变换 $L_i$ 将其转化为尺度向量 $\mathbf{k}_i$，对风格向量进行逐元素调制（$\mathbf{s}'_i = \mathbf{k}_i \odot \mathbf{s}_i$），使得条件信号以“风格控制”而非“内容拼接”的方式介入生成过程。

这一设计的关键因果链路在于：**风格调制机制为条件信号提供了逐层、可学习的控制通道**，使得模型能够自动学习将不同时间尺度的变化分配给不同的网络层级；同时，**隐空间（$z$）被解放出来专门承载随机变化**（如天气、遮挡），因为条件信号不再与 $z$ 在输入端竞争信息容量。消融实验（Figures 14, 15）直接验证了这一槽位变更的决定性作用：当将风格调制替换回拼接条件（Ablation B/C）时，年周期与趋势信号发生纠缠，甚至日周期信号错误地控制了本应由趋势处理的变化。

在知识库中，本工作的挂载点位于**条件GAN的条件注入机制设计**和**时间序列解耦表示学习**的交叉节点。相较于 **StyleGAN2**（Karras et al., CVPR 2020）的无条件生成基线，TLGAN在保持FID相当（Table 2）的前提下，新增了对日周期、年周期和长期趋势的独立控制能力，且无需牺牲图像质量。相较于 **Martin-Brualla et al.**（TOG 2015）的时间推移去闪烁方法，TLGAN不依赖于时序平滑或帧间对齐后处理，而是从生成建模的角度直接学习时间变化因素的解耦表征，在包含移动物体的场景中产生了显著更清晰的合成结果（Figure 13）。

**适用边界**需要明确：TLGAN为每段时间推移序列**独立训练一个模型**，无法泛化到新场景——这是与通用图像生成模型（如在大规模数据集上预训练的条件扩散模型）的本质差异。方法的有效性依赖于输入序列具有可明确参数化的周期性信号（如日/年循环），对于缺乏明确周期结构的时间变化（如不规则的施工进度），趋势分量 $t_g$ 的设计虽然提供了灵活性，但其控制力较弱（仅占输出方差不到10%，Figure 11）。此外，模型对输入图像的对齐误差敏感，预处理中残留的配准错误会被作为“变化信号”学习，导致非期望的纠缠（Figure 16）。

**后续启发**可从三个方向展开：（1）**对齐与生成的联合学习**——当前方法依赖手工预处理对齐，若将对齐网络与生成器端到端训练（如利用Alias-Free GAN的抗混叠特性），可消除预处理误差的传播；（2）**时间一致性显式建模**——TLGAN逐帧独立生成，未强制帧间连续性约束，在视频生成任务中引入时序判别器或光流一致性损失是自然的扩展方向；（3）**解耦效果的定量评价**——目前解耦质量主要依赖定性可视化（如单独变化某一条件信号的生成结果）和方差分析，设计标准化的解耦度量指标（如条件信号互信息、属性分类准确率）将有助于该方向的系统化推进。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Disentangling_Random_and_Cyclic_Effects_in_Time_lapse_Sequences.pdf]]