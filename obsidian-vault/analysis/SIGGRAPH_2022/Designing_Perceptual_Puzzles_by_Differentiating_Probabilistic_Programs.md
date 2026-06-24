---
title: Designing Perceptual Puzzles by Differentiating Probabilistic Programs
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Designing_Perceptual_Puzzles_by_Differentiating_Probabilistic_Programs.pdf
project_link: "https://people.csail.mit.edu/kach/dpp-dpp/"
code_link: "https://github.com/kach/designing-perceptual-puzzles-by-differentiating-probabilistic-programs"
aliases:
- DPP
- DPPBDPP
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 通过哈密尔顿蒙特卡洛（HMC）推理实现端到端可微分，使得梯度下降能够直接优化输入以操控贝叶斯感知模型的后验分布。
primary_logic: 将人类视觉感知建模为贝叶斯推理过程，并利用可微分概率编程语言对推理过程进行反向传播，从而能够系统性地搜索引发特定感知行为的对抗性刺激。
claims:
- CNN对抗样本不会迁移到人类，无法生成类似‘The Dress’的鲁棒错觉
- 本文提出可微分概率编程语言，将MCMC推理作为一等可微函数
- 该方法能自动为颜色恒常性、尺寸恒常性和人脸感知生成错觉
- 颜色恒常性错觉人类实验 上 报告颜色的色调分散度 = 幻觉图像引起显著多样且高信心的不同颜色感知
---

# Designing Perceptual Puzzles by Differentiating Probabilistic Programs

> [!tip] 核心洞察
> 将人类视觉感知建模为贝叶斯推理过程，并利用可微分概率编程语言对推理过程进行反向传播，从而能够系统性地搜索引发特定感知行为的对抗性刺激。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过可微分概率编程设计感知谜题 |
| 英文题名 | Designing Perceptual Puzzles by Differentiating Probabilistic Programs |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2204.12301) · [Project](https://people.csail.mit.edu/kach/dpp-dpp/) · [arXiv](https://arxiv.org/abs/2012) · [Code](https://github.com/kach/designing-perceptual-puzzles-by-differentiating-probabilistic-programs) |
| Topic | #topic/other_unclear |
| Method | 可微分概率编程（Differentiable Probabilistic Programming） |
| Dataset |  |

> [!tip] 效果简介
> - 颜色恒常性错觉人类实验 上，报告颜色的色调分散度 幻觉图像引起显著多样且高信心的不同颜色感知 vs 对照图像引起紧密聚集、低多样性的颜色感知 (定性显著，幻觉的色调变化远大于对照)。
> - 尺寸恒常性错觉定性展示 上，人类直觉是否被愚弄（定性） 生成的图像使模型和人类观察者均产生错误的距离/尺寸感知 vs 无显式基线，仅展示生成结果 (定性成功)。
> - 人脸感知错觉生成 上，令人信服的错觉占生成结果的比例 约10%的优化结果产生明显的人脸表情错觉 vs 无显式基线 (10%)。

## 概要

传统对抗样本无法可靠迁移至人类视觉，难以系统生成类似“The Dress”的鲁棒错觉。本文提出**可微分概率编程**，将人类视觉感知形式化为贝叶斯推理过程，并通过哈密尔顿蒙特卡洛（HMC）推理的可微化，使梯度下降能够直接优化输入以操控感知模型的后验分布。具体地，作者设计了一种将MCMC采样作为一等可微函数的概率编程语言，并利用逆动力学实现内存高效的反向传播。该方法成功为颜色恒常性、尺寸恒常性及人脸表情感知三类视觉现象自动生成了错觉：人类实验证实颜色错觉引发显著多样的色调报告，尺寸错觉同时愚弄模型与人类直觉，人脸表情错觉的生成产率约10%。方法定位上，本文在贝叶斯感知建模与对抗样本生成之间建立了全新连接，将优化目标从分类器决策边界迁移至概率推理的后验期望，开辟了可微分概率编程在认知科学中的应用方向。

## 核心方法与创新机理

### 问题背景与唯一瓶颈

人类视觉系统会自发产生错觉——同一幅图像可能被不同观察者感知为截然不同的颜色、尺寸或表情。然而，**系统性地设计能够稳定欺骗人类感知的视觉刺激**一直是一个开放难题。传统方法主要依赖针对深度卷积神经网络的对抗攻击，但近十年的研究表明，这些对抗样本**无法可靠地迁移到人类感知系统**（Sinz et al., 2019）。其根本瓶颈在于：CNN 的对抗样本利用的是特定网络架构的梯度脆弱性，而非人类视觉所依赖的概率推理机制。因此，要生成鲁棒的人类感知错觉，必须直接建模并操控人类视觉的**贝叶斯推理过程**。

### 核心洞察与创新机理

本文的核心洞察是：**将人类视觉感知形式化为贝叶斯推理，并利用可微分概率编程语言（Differentiable Probabilistic Programming Language, DPPL）对推理过程进行端到端反向传播，从而通过梯度下降系统性地搜索引发特定感知行为的对抗性刺激。**

这一思路的关键创新在于将 MCMC 推理（具体为哈密尔顿蒙特卡洛，HMC）提升为**一等可微函数**。传统概率编程中，推理过程是一个黑箱——给定观测，输出后验样本——其内部随机游走无法传递梯度。本文通过以下机制打破了这一障碍：

1. **物理模拟视角**：将 HMC 的每一步随机游走视为一个具有连续动力学的物理模拟过程。
2. **自动微分穿透**：对该物理模拟直接应用自动微分，使梯度能够穿过采样步骤。
3. **可逆学习**：通过时间反转的物理模拟在反向传播时动态重计算中间值，解决内存爆炸问题。

### Changed Slots：推理可微性的根本转变

本文相对于传统概率编程方法，在**推理可微性**这一关键槽位上实现了根本性改变：

| 槽位 | 基线方法 | 本文方法 |
|------|---------|---------|
| 推理可微性 | 非可微的 MCMC 推理，无法通过梯度下降优化输入 | 利用自动微分与逆动力学实现可微的 HMC 推理，支持端到端梯度下降 |

传统概率编程语言（如 Church、Anglican）虽然能表达复杂的生成模型并执行 MCMC 推理，但推理过程对输入参数不可微。这意味着无法计算“改变输入图像会如何影响后验期望”的梯度。本文通过将 HMC 轨迹视为可微的确定性物理模拟（随机性仅来自初始动量采样），使得 `∂(后验期望)/∂(输入图像)` 成为可计算量。这一改变使得**梯度下降优化输入以操控后验分布**成为可能。

### 方法框架与模块顺序

整个方法由四个核心模块构成，形成一条端到端的可微优化管线：

#### 模块一：生成模型定义（Probabilistic Generative Model）

使用 DPPL 提供的两个核心原语表达视觉感知的贝叶斯生成模型：

- **`sample`**：从给定分布中生成一个新的独立样本，对应先验采样。
- **`observe`**：将生成过程条件化于某个观测值，对应似然约束。

以颜色恒常性为例，生成模型表达为：

$$P(\text{Light}, \text{Color} \mid \text{Image}) \propto P(\text{Light}, \text{Color}) \cdot P(\text{Image} \mid \text{Light}, \text{Color})$$

其中先验 $P(\text{Light}, \text{Color})$ 编码了关于光源和物体颜色的统计知识（如光源颜色倾向于中性、物体颜色在自然场景中的分布），似然 $P(\text{Image} \mid \text{Light}, \text{Color})$ 则描述了给定场景参数后图像的生成过程（通过渲染器实现）。用户通过组合 `sample` 和 `observe` 原语来定义这一联合分布。

#### 模块二：HMC 推理（Differentiable MCMC Inference）

DPPL 提供 `hmc_sample` 函数，接受 HMC 超参数（步长、步数、采样数）并返回后验期望的蒙特卡洛估计。HMC 的核心是模拟一个在势能函数（负对数后验）引导下的粒子运动：

- 随机采样初始动量。
- 通过蛙跳积分（leapfrog integration）模拟哈密尔顿动力学。
- 使用 Metropolis-Hastings 接受/拒绝步骤保证渐近正确性。

由于蛙跳积分的每一步都是可微的确定性操作，整个 HMC 轨迹对输入参数可微。这一性质是后续梯度优化的基础。

#### 模块三：逆动力学反向传播（Reversible Learning Backpropagation）

直接存储 HMC 轨迹的所有中间值进行反向传播会导致内存爆炸——对于包含渲染器的生成模型，单次前向传播可能涉及数百万次操作。本文的解决方案是**可逆学习**：

> Rather than storing intermediate values, we recompute them dynamically during backpropagation by running the physical simulation in reverse, backwards through time.

具体而言，蛙跳积分是时间可逆的：给定末状态，可以通过反向积分精确恢复初状态。在反向传播时，系统从轨迹末端开始，反向运行物理模拟以重计算所需的中间激活值，然后计算梯度。这使得**内存消耗与轨迹长度解耦**，仅需存储最终状态和少量检查点。

#### 模块四：梯度下降优化（Gradient Descent Optimization）

在可微推理的基础上，定义损失函数并通过梯度下降搜索错觉刺激。以颜色恒常性为例，损失函数为：

```
def loss(light, true_color1, true_color2):
    perceived_color1, perceived_color2 = infer(render(light, true_color1, true_color2))
    return -length(true_color1 - perceived_color1) + -length(true_color2 - perceived_color2)
```

该损失函数最大化真实颜色与模型推断颜色之间的差异。梯度从 `infer`（即 `hmc_sample`）反向传播，穿过 HMC 轨迹、渲染器，最终到达输入参数（光源颜色、物体真实颜色等）。优化过程自动发现那些使后验期望偏离物理真实的对抗性输入。

### 模块间因果关系

四个模块之间的因果链路如下：

1. **生成模型定义**提供概率图结构，决定了哪些变量可被优化以及后验的几何性质。模型的结构直接约束了可生成的错觉类型——例如，颜色恒常性模型中的光源变量是优化的关键自由度。
2. **HMC 推理**将生成模型转化为可微的“后验期望估计器”。推理的质量（采样数、步长）影响梯度估计的方差，进而影响优化的稳定性。
3. **逆动力学反向传播**是使整个管线可扩展的关键使能技术。若无此模块，内存需求将随 HMC 步数线性增长，使得包含渲染的模型无法优化。
4. **梯度下降优化**利用前三个模块提供的梯度信号，在输入空间中搜索局部最优的错觉刺激。损失函数的设计直接决定了优化目标的语义——是最大化感知分歧（颜色错觉）、最小化推断距离（尺寸错觉），还是最大化光照方向对表情的影响（人脸错觉）。

### 关键公式与变量含义

**贝叶斯推理框架**（通用形式）：

$$P(\text{Scene} \mid \text{Image}) \propto P(\text{Image} \mid \text{Scene}) \cdot P(\text{Scene})$$

- $\text{Scene}$：场景参数（光源、物体颜色、几何、材质等）。
- $\text{Image}$：观测到的图像。
- $P(\text{Scene})$：先验分布，编码视觉系统对世界的统计假设。
- $P(\text{Image} \mid \text{Scene})$：似然，由渲染器定义。
- $P(\text{Scene} \mid \text{Image})$：后验分布，对应“给定图像后观察者对场景的信念”。

**颜色恒常性特化**：

$$P(\text{Light}, \text{Color} \mid \text{Image}) \propto P(\text{Light}, \text{Color}) \cdot P(\text{Image} \mid \text{Light}, \text{Color})$$

- $\text{Light}$：光源的光谱分布或 RGB 颜色。
- $\text{Color}$：物体表面的真实反射率。

**示例模型联合密度**（用于教学性说明）：

$$p(t, m) = p(t) \cdot p(m \mid t) = \Phi\left(\frac{t - 70}{5}\right) \cdot \Phi\left(\frac{m - t}{2}\right)$$

- $t$：真实温度。
- $m$：温度计测量值。
- $\Phi$：标准正态分布的累积分布函数，编码高斯先验和测量噪声。

### 训练/推理路径

**推理路径（前向传播）**：
1. 输入：待优化的刺激参数（如光源颜色、物体几何、相机参数）。
2. 渲染：通过可微渲染器生成图像。
3. MCMC 推理：运行 HMC 采样，从后验分布中抽取样本。
4. 后验期望：对样本求平均，得到模型对场景的“感知”估计。
5. 损失计算：比较感知估计与目标值，计算损失。

**训练路径（反向传播）**：
1. 损失梯度：计算损失对后验期望的梯度。
2. 穿过 MCMC：通过逆动力学反向传播，将梯度从后验期望传递到 HMC 轨迹的每一步，最终到达渲染图像。
3. 穿过渲染器：梯度继续反向传播到场景参数。
4. 参数更新：使用梯度下降（如 Adam）更新刺激参数。

这一路径的核心特征是**梯度穿过了随机采样过程**——不是通过重参数化技巧，而是通过将整个 MCMC 轨迹视为可微的确定性映射（条件于初始动量）。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2204_12301/figures/001_Figure_1.jpg]]
*Figure 1: Illusion synthesis: We find scenes where different people perceive different colors (top), where most people infer incorrect geometry (left), and where changing the lighting causes a face to change expression (right). To search for these scenes, we perform gradient descent optimization over Bayesian models of human visual perception, which are implemented in our differentiable probabilistic programming language*

## 实验与关键发现

本文通过三类感知错觉的生成实验验证了所提方法的有效性，并辅以人类行为实验和定性分析。以下从主结果、消融与失败模式、适用边界三个层面展开。

### 颜色恒常性错觉：人类实验定量验证

颜色恒常性是本文最核心的实验验证场景。作者将生成模型定义为一个贝叶斯推断问题：给定图像，推断场景中的光源颜色和物体真实反射色。优化目标为最大化模型推断颜色与真实颜色之间的差异（`loss` 函数见 Section 4.1），从而搜索能引发多义感知的对抗性刺激。

**实验设计**：通过在线平台招募参与者，收集了 35 份有效响应（剔除注意力检查失败者后）。参与者被要求观看生成的错觉图像和对照图像，并报告所感知到的橡皮擦颜色。对照图像采用相同场景但无对抗性光照的条件。

**主结果**（Figure 2）：报告颜色在色调上的分散度是核心指标。对于错觉图像，参与者报告的颜色在色调上差异极大，不同观察者对同一块橡皮擦感知到截然不同的颜色；而对照图像的报告颜色则在感知相近的色调区域内紧密聚集。这一差异是定性显著的——错觉引起的色调变化远大于对照条件，直接验证了“不同人看到不同颜色”的错觉目标。

**证据强度**：该实验具有明确的可量化对比（错觉 vs. 对照），且人类行为数据收集通过了注意力检查，可靠性较高。但由于报告的是定性差异而非统计检验量，精确的效应量需人工核实。

### 尺寸恒常性错觉：模型与人类直觉的双重验证

尺寸恒常性实验的目标是搜索使模型错误推断物体距离/尺寸的场景。优化目标为最小化模型推断的第一张桌子位置与其真实位置之间的差异（`loss` 函数见 Section 4.2），从而生成使物体“看起来更近/更大”的刺激。

**主结果**（Figure 3a, 3b）：生成的图像在模型层面成功“欺骗”了贝叶斯感知模型——模型推断的桌子位置与真实位置存在系统性偏差。更重要的是，作者报告“我们的模型和人类直觉都被这些图像愚弄了”（Both our model, and human intuitions, are ‘fooled’ by these images），表明生成的错觉对人类观察者也有效。Figure 3a 通过摄像机运动揭示了真实场景结构，与观察者感知形成对比；Figure 3b 展示了另外两个自动生成的尺寸恒常性错觉示例。

**证据强度**：该实验为定性展示，未提供大规模人类实验的定量数据。模型层面的成功有明确的优化指标支撑，但人类直觉的验证依赖于作者的主观判断。置信度为 0.9。

### 人脸表情错觉：产率与失败模式

人脸感知实验的目标是搜索一个面部网格和光照方向，使得当光照方向关于原点翻转时，模型感知到的面部表情发生显著变化。优化目标为最大化两种光照条件下模型推断表情的差异（`loss` 函数见 Section 4.3）。

**主结果**（Figure 3c）：在大量优化运行中，约 **10%** 的结果产生了令人信服的人脸表情错觉。Figure 3c 展示了排名前三的错觉示例，每对图像展示同一网格在两种不同光照方向下的渲染结果，观察者可感知到明显的表情变化。

**失败模式分析**：在剩余 90% 的失败案例中，最常见的失败模式是**模型与典型人类面部感知之间的不匹配**（mismatch between typical human face perception and our model）。这表明当前贝叶斯感知模型的先验分布未能充分捕捉人类面部感知的特性，导致优化找到了模型“认为”是错觉但人类不认可的刺激。这一发现直接揭示了方法的瓶颈：**错觉的产率和泛化能力受限于感知模型的保真度**。

**证据强度**：10% 产率是基于作者主观判断的估计，未提供系统性的评估标准。失败模式的分析具有启发性，但缺乏对人类感知不匹配的具体量化。

### 关键消融：可逆学习的必要性

虽然不是传统意义的消融实验，但作者明确指出了不使用可逆学习（reversible learning）的严重后果：**标准自动微分需要存储所有中间值，在包含渲染的生成模型中会导致内存爆炸，无法扩展到实际场景**（Section 2.4）。本文的解决方案是通过时间反转的物理模拟在反向传播时动态重新计算中间值，这一设计是实现端到端可微分 MCMC 推理的关键工程贡献。没有这一技术，整个方法将因内存限制而不可行。

### 适用边界与限制

1. **离散随机变量不可用**：当前方法仅支持连续随机变量，无法生成需要离散变量的错觉类型（如图形-背景反转）。这直接限制了可生成错觉的种类范围。
2. **渲染模型简化**：所有实验仅使用单眼线索渲染，未考虑阴影或物理环境光遮挡。这意味着生成的错觉图像在物理上可能无法精确复现，限制了从数字刺激到物理实体的转化。
3. **先验单一性**：所有实验在单一固定先验的模型上进行，未利用人类感知先验的多样性。这可能是面部表情错觉产率低（10%）的根本原因之一。
4. **人类验证有限**：除颜色恒常性实验外，尺寸恒常性和人脸表情错觉的人类验证主要依赖作者定性判断，缺乏大规模受控实验的统计支撑。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2204_12301/figures/002_Figure_2.jpg]]
*Figure 2: Color constancy illusions created by our method (Section 4.1). Each plot shows the image we presented to participants in our study, along with swatches representing the colors that they reported for the two kinds of erasers. The size of each half-square is proportional to the participant’s self-reported confidence in that color response. Selected high-confidence responses (≥ 7/10 for both colors) are shown in circled insets, re-lit in neutral light as the participants themselves saw in the guide display when picking colors. For controls, we selected the most distant pairs in CIELAB space; for illusions, we handpicked responses to represent significant perceptual modes. The reported colors f...*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2204_12301/figures/003_Figure.jpg]]

## 定位与知识库关联

本文的核心贡献在于改变了**推理可微性**这一关键slot：将传统概率编程中“不可微的MCMC推理”替换为“可微的HMC推理”，从而使得梯度下降能够直接优化生成模型的输入以操控后验分布。这一改变并非简单地给现有系统添加一个可微层，而是从语言设计（将`hmc_sample`暴露为一等可微函数）到底层实现（逆动力学反向传播）的端到端重构，使得“通过贝叶斯感知模型反向传播梯度”从不可能变为可能。

**相对已有方法的本质差异**：近十年的对抗样本研究已经证明，针对CNN的对抗攻击不会迁移到人类视觉系统（Sinz et al., 2019）。本文并非沿着“寻找更好的CNN对抗样本”这条路径前进，而是完全切换了目标模型——从判别式的CNN切换到生成式的贝叶斯感知模型。这一切换使得搜索空间从“欺骗特定网络分类器”变为“操控人类感知后验分布”，从而能够系统性生成类似“The Dress”现象的鲁棒视觉错觉。与传统的感知错觉设计（依赖艺术家的直觉和手工试错）相比，本文方法将错觉设计形式化为一个可微优化问题，实现了自动化搜索。

**知识库挂载点**：本文可挂载到以下知识节点：
- **可微分概率编程**：将MCMC推理作为可微函数暴露，连接了概率编程语言（如Gen、Pyro）与自动微分框架（如JAX、PyTorch）。其核心创新在于利用HMC的连续动力学特性，通过时间反转的物理模拟实现空间高效的反向传播，解决了“MCMC采样步骤不可微”这一长期瓶颈。
- **贝叶斯感知模型**：本文建立在“视觉感知即贝叶斯推理”这一理论框架之上，具体实现了颜色恒常性、尺寸恒常性和人脸感知三个领域的生成模型。这些模型本身并非原创，但本文首次展示了如何通过可微推理来反向搜索这些模型的对抗性输入。
- **对抗样本与人类感知**：与CNN对抗样本文献形成明确对比，本文证明了当目标模型是贝叶斯感知模型而非CNN时，对抗样本可以可靠地迁移到人类观察者。这为“人类感知的对抗性攻击”开辟了新方向。

**适用边界**：
- **离散变量限制**：当前方法明确不支持离散随机变量（如前景/背景反转所需的二值选择），因为HMC的连续动力学无法处理离散跳跃。这一限制直接排除了图形-背景反转等经典错觉类型的生成。
- **模型-人类对齐**：人脸表情错觉的产率仅约10%，主要失败模式是概率模型与典型人类感知之间的不匹配。这意味着方法的有效性高度依赖于底层贝叶斯模型对人类感知的忠实程度，而当前模型（使用单一固定先验）远未捕捉人类感知先验的多样性。
- **物理可复现性**：渲染仅使用单眼线索，未包含阴影或物理环境光遮挡，因此生成的错觉在物理世界中可能无法直接复现。

**后续启发**：本文为以下研究方向提供了方法论基础：
- **离散变量的可微推理**：扩展可微概率编程以支持离散随机变量（如通过可微松弛或强化学习估计器），将解锁更丰富的错觉类型。
- **感知先验的对齐与个性化**：将贝叶斯感知模型的参数与真实人类感知数据进行拟合，或利用不同人群的先验差异生成“个性化错觉”。
- **超越视觉的认知领域**：该方法可推广到其他已建立贝叶斯模型的认知领域，如直觉物理（欺骗人们对物体运动轨迹的预测）或社会认知（操控对他人意图的推断）。
- **物理错觉制造**：结合更丰富的物理渲染（阴影、全局光照、双目线索），生成可在真实世界中制造和观看的物理错觉装置。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Designing_Perceptual_Puzzles_by_Differentiating_Probabilistic_Programs.pdf]]