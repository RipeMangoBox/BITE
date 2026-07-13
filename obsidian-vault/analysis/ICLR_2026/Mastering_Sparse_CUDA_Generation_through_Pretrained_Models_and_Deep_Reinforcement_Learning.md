---
title: "Mastering Sparse CUDA Generation through Pretrained Models and Deep Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Mastering_Sparse_CUDA_Generation_through_Pretrained_Models_and_Deep_Reinforcement_Learning.pdf
project_link: null
code_link: https://github.com/QiWu-NCIC/SparseRL
openreview_forum_id: VdLEaGPYWT
aliases:
- MSCGTPMDRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将生成问题从监督微调转为深度强化学习，引入基于编译、测试、执行效率和内存使用的分层奖励函数，并使用稀疏矩阵行列索引的正弦嵌入替代自然语言提示，从而直接优化代码的正确性与性能。"
primary_logic: "将预训练语言模型视为随机策略，通过强化学习从编译器与执行器反馈中学习，可以使模型生成语法正确且运行高效的CUDA代码；而利用正弦嵌入编码稀疏矩阵的非零元素位置，能有效捕获矩阵结构信息，消除模态差异。"
claims:
- "SparseRL在SpMV任务上编译率提升20%，生成代码平均运行速度快30%"
- "SparseRL在SuiteSparse矩阵上相比cuSPARSE平均性能提升1.42倍（V100）"
- "结合预训练、SFT和PPO的完整流程获得最佳pass@1000（49.25）"
- "正弦稀疏矩阵嵌入显著优于其他嵌入策略"
---

# Mastering Sparse CUDA Generation through Pretrained Models and Deep Reinforcement Learning

> [!tip] 核心洞察
> 将预训练语言模型视为随机策略，通过强化学习从编译器与执行器反馈中学习，可以使模型生成语法正确且运行高效的CUDA代码；而利用正弦嵌入编码稀疏矩阵的非零元素位置，能有效捕获矩阵结构信息，消除模态差异。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于预训练模型与深度强化学习的稀疏CUDA代码生成 |
| 英文题名 | Mastering Sparse CUDA Generation through Pretrained Models and Deep Reinforcement Learning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=VdLEaGPYWT) · [GitHub](https://github.com/QiWu-NCIC/SparseRL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SparseRL |
| Dataset | SuiteSparse SpMV (400测试矩阵), SuiteSparse SpMV 在 V100 上, SuiteSparse SpMM (col=8) 在 A100 上 |

> [!tip] 效果简介
> - SuiteSparse SpMV (400测试矩阵) 上，pass@1000 为 49.25 (SparseRL+Qwen2.5-14B)，对比 36.50 (CodeRL+CodeT5-770M)，变化 +12.75。
> - SuiteSparse SpMV (400测试矩阵) 上，编译率 (CR) 为 57.50 (SparseRL+Qwen2.5-14B)，对比 39.50 (CodeRL+CodeT5-770M)，变化 +18.00。
> - SuiteSparse SpMV 在 V100 上 上，平均 GFLOPS 相对 cuSPARSE 的加速比 为 1.42×，对比 1× (cuSPARSE)，变化 +42%。

## 概要

稀疏矩阵运算（如稀疏矩阵-向量乘 SpMV）是科学计算与图神经网络的核心算子，但其不规则的内存访问模式使得手工编写高性能 CUDA 内核极为困难。现有代码生成方法面临三重瓶颈：（1）稀疏数据的不规则性导致执行模式动态变化，需要针对不同矩阵结构定制实现；（2）监督学习的 token 级匹配目标无法区分语义正确但性能迥异的实现，缺乏对执行效率的奖励信号；（3）稀疏矩阵的结构化索引输入与自然语言提示之间存在模态鸿沟。

SparseRL 将预训练语言模型视为**随机策略**，将代码生成步骤视为**动作**，从编译器与执行器反馈中获取奖励信号，通过深度强化学习直接优化生成代码的正确性与执行效率。其核心设计包括：用稀疏矩阵非零元素行列索引的**正弦嵌入**替代自然语言提示，消除模态差异；构建**分层奖励函数**（编译正确性 ±0.5、功能测试 ±0.5、以 cuSPARSE 为基线的效率缩放奖励、共享内存超额惩罚）；以及**三阶段训练流程**（CUDA 代码增强预训练 → 监督微调 → PPO 强化学习）。

在 SuiteSparse 矩阵集的 SpMV 任务上，SparseRL 相比现有方法编译率提升 20%，生成代码平均运行速度提升 30%；相比 NVIDIA 官方库 cuSPARSE 在 V100 上平均性能提升 **1.42 倍**（A100 上 1.44 倍）。消融实验证实预训练阶段贡献约 8.5 个 pass@1000 点，RL 阶段贡献约 3.75 点，正弦嵌入显著优于线性投影和可学习嵌入策略。方法在 SpMM 任务上也展现出泛化能力，在 A100 上相比 Sputnik 取得 **2.32 倍**加速比。



稀疏矩阵运算——尤其是稀疏矩阵-向量乘法（SpMV）和稀疏矩阵-矩阵乘法（SpMM）——是科学计算、图分析和深度学习等领域的核心计算瓶颈。与稠密矩阵不同，稀疏矩阵的非零元素分布极不规则，导致其执行模式高度依赖输入数据的结构特征。为每一种稀疏模式手工编写高性能CUDA内核不仅耗时巨大，而且难以泛化，因此自动化生成稀疏CUDA代码成为一个极具吸引力的研究方向。

然而，现有代码生成方法在这一任务上面临三重根本性困难。**第一，监督学习的目标函数与性能目标错位。** 主流的监督微调（SFT）方法以最小化token级交叉熵损失为目标，其本质是最大化参考代码的似然。这种目标函数无法区分语义正确但执行效率迥异的不同实现——一段通过编译且计算结果正确的代码，其运行时间可能相差数倍，但交叉熵损失对此完全无感知。**第二，稀疏矩阵的模态鸿沟。** 稀疏矩阵的结构化信息（非零元素的行列索引）与自然语言提示之间存在根本的表示差异。将稀疏模式简单地转换为文本描述会丢失关键的拓扑信息，使模型难以捕获非零元素的分布规律和内存访问模式。**第三，执行效率缺乏反馈信号。** 传统的监督学习流程在训练时仅依赖静态的代码-注释对，完全隔离于编译器与执行器的运行时反馈，导致模型无法感知生成代码在实际硬件上的性能表现。

针对上述缺口，现有工作进行了初步探索。**CodeRL**（Le et al., 2022）和**PPOCoder**（Shojaee et al., 2023）将强化学习引入代码生成，但它们的奖励信号主要来自编译正确性和功能测试，缺乏对执行效率的直接优化，且仍依赖自然语言提示作为输入。**cuSPARSE**（Naumov et al., 2010）作为NVIDIA官方稀疏计算库，通过手工优化实现了可靠的性能，但其覆盖的稀疏模式有限，无法为任意矩阵结构提供定制化内核。**TVM-S**（Chen et al., 2018）通过编译器自动调优生成稀疏代码，但其搜索空间受限于预定义的调度模板，难以发现超越手工设计的优化策略。

本文的核心动机在于：**将预训练语言模型视为一个可优化的随机策略，通过深度强化学习直接从编译器与执行器的反馈中学习，使模型能够同时优化代码的正确性与执行效率。** 这一思路的关键洞见是：编译结果（通过/失败）、功能测试（正确/错误）和执行时间（相对基线的加速比）构成了一个天然的奖励信号源，可以弥合训练目标与部署性能之间的鸿沟。同时，通过用稀疏矩阵非零元素行列索引的正弦嵌入替代自然语言提示，可以消除模态差异，使模型直接感知稀疏结构，从而生成针对特定矩阵模式定制的高效CUDA内核。



## 核心方法与创新机理

SparseRL 的核心创新在于将稀疏 CUDA 代码生成从传统的监督学习范式彻底转向**深度强化学习范式**，并通过三个关键设计突破现有方法的瓶颈。

### 从 Token 匹配到执行反馈：强化学习驱动的性能优化

现有代码生成方法（如 CodeRL、PPOCoder）采用监督微调，其交叉熵损失函数仅优化 token 级别的匹配概率，无法区分语义正确但执行效率迥异的实现。SparseRL 将预训练语言模型视为**随机策略**，代码生成步骤作为动作，从编译器与执行器（环境）中获取反馈信号。这一范式转换的关键在于**分层奖励函数**的设计：

- **正确性奖励**：$R_{\mathrm{correctness}} = R_{\mathrm{compile}} + \mathbb{I}_{\mathrm{compile}} \cdot R_{\mathrm{test}}$，其中编译成功获得 ±0.5 奖励，测试通过额外获得 ±0.5 奖励（仅在编译成功时计算）。
- **效率奖励**：$R_{\mathrm{efficiency}} = r_{\mathrm{eff}} \times \left( \frac{t_{\mathrm{base}}(X)}{t(\hat{Y}, X)} - 1 \right) \cdot \mathbb{I}_{\mathrm{test}}$，以 cuSPARSE 为基线计算加速比，仅在功能正确时生效。
- **最终奖励**：$R_{\mathrm{final}}(\hat{Y}, X) = R_{\mathrm{correctness}} + R_{\mathrm{efficiency}} - r_{\mathrm{penalty}} \cdot \mathbb{I}_{\mathrm{memory}}$，引入共享内存超额惩罚，约束生成的核函数资源使用。

这一奖励结构使得模型直接从执行效率中学习，而非间接模仿训练数据中的代码模式。消融实验证实，仅使用 SFT 的 pass@1000 为 45.50，而加入 RL 阶段后提升至 49.25（Table 2），验证了执行效率奖励的关键作用。

### 模态鸿沟的消除：正弦稀疏矩阵嵌入

传统方法将稀疏矩阵的行列索引作为自然语言文本输入模型，忽略了矩阵结构的连续性和位置关系。SparseRL 采用**正弦位置编码**将每个非零元素的行索引 $r_i$ 和列索引 $c_i$ 分别编码为 $d_{model}$ 维向量：

$$PE_{(ind, 2j)} = \sin\left(ind / 10000^{2j/d_{model}}\right), \quad PE_{(ind, 2j+1)} = \cos\left(ind / 10000^{2j/d_{model}}\right)$$

然后将行列编码向量拼接为 $e_i = [e_{r_i} | e_{c_i}]$，通过额外的线性层映射至模型维度。在 SFT 和 RL 阶段，**完全移除自然语言提示**，模型仅根据稀疏矩阵的结构化嵌入直接生成 CUDA 代码。这一设计消除了稀疏数据与自然语言之间的模态差异，使模型能够捕获非零元素的分布模式与局部结构。

消融实验（Table 3）表明，正弦嵌入在 SpMV pass@1000 上达到 48.75（SparseRL+CodeT5-770M），显著优于线性投影和可学习嵌入策略，证实了该设计的有效性。

### 动态解码控制：语法感知的生成终止

SparseRL 在解码过程中集成了**CUDA 语法/语义动态验证机制**：当生成的代码片段出现语法错误或违反 CUDA 编程约束时，提前终止当前序列的生成。这一机制避免了无效代码的完整生成，节省了解码预算，同时为 RL 训练提供了更精确的负反馈信号。该设计与分层奖励函数形成闭环——编译失败直接获得负奖励并终止，编译成功则继续评估测试正确性与执行效率。

### 三阶段训练管线

上述创新通过**预训练 → 监督微调 → 强化学习**的三阶段管线协同作用：

1. **CUDA 代码增强预训练**：使用大量 CUDA 代码对预训练语言模型进行领域适应，注入并行编程与 GPU 硬件优化知识。
2. **稀疏矩阵嵌入与监督微调**：引入正弦嵌入并逐步去除自然语言提示，使模型建立从矩阵结构到 CUDA 代码的映射能力。
3. **PPO 强化学习优化**：以分层奖励为优化目标，通过 PPO 算法进一步优化模型，直接追求编译正确性与执行效率。

消融实验（Table 2）表明，三阶段完整流程获得最佳 pass@1000（49.25），而去掉预训练阶段降至 40.75，去掉 RL 阶段降至 45.50，验证了各阶段的必要性。



![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method to optimize pretrained LMs for sparse CUDA code generation. (a) At pre-training stage, additional CUDA code is used to augment the LM. (b) At supervised finetuning (SFT) stage, the LM is finetuned for the Sparse CUDA code generation. (c) At RL stage, the actor and critic networks are first initialized from the finetuned LM, and then updated based on the reward of RL. The reward function is composed of correctness and efficiency rewards*

SparseRL 将稀疏 CUDA 代码生成重新定义为强化学习问题，其核心思想是：**将预训练语言模型视为随机策略**，代码生成的每一步作为动作，编译器与执行器构成环境，通过执行反馈的奖励信号直接优化代码的正确性与运行效率。图 2 展示了完整的三阶段训练流水线。

### 输入输出流

系统的输入为稀疏矩阵的非零元素行列索引序列：

$$X = ((r_1, c_1), (r_2, c_2), \ldots, (r_N, c_N))$$

其中 $r_i$ 和 $c_i$ 分别表示第 $i$ 个非零元素的行索引和列索引。输出为完整的 CUDA 核函数代码 $\hat{Y}$，需满足三个条件：

$$\left\{ \begin{array}{ll} \mathrm{Compile}(\hat{Y}) = \mathrm{True} \\ \mathrm{Correct}(\hat{Y}, X) = \mathrm{True} \\ E(\hat{Y}|X) \leq E(Y_i|X), \forall Y_i \in \mathcal{Y} \end{array} \right.$$

即生成的代码必须编译通过、计算结果正确，且执行时间不超过任何参考实现。

### 三阶段训练流水线

**阶段一：CUDA 代码增强预训练。** 使用大量 CUDA 代码对预训练语言模型进行领域适应，注入并行编程模式与 GPU 硬件优化知识。这一阶段不涉及稀疏矩阵输入，仅增强模型对 CUDA 语法和优化原语的掌握。

**阶段二：稀疏矩阵嵌入与监督微调。** 引入正弦嵌入将稀疏矩阵的行列索引映射为连续向量。对于第 $i$ 个非零元素，其嵌入向量由行列编码拼接而成：

$$PE_{(ind,2j)} = \sin\left(ind / 10000^{2j/d_{model}}\right), \quad PE_{(ind,2j+1)} = \cos\left(ind / 10000^{2j/d_{model}}\right)$$

$$e_i = [e_{r_i} \| e_{c_i}]$$

这些嵌入向量经额外线性层映射至模型维度后，替代自然语言提示直接作为模型输入。监督微调阶段逐步去除文本提示，使模型学会直接从矩阵结构生成 CUDA 代码，优化目标为交叉熵损失：

$$\mathcal{L}_{ce}(\theta) = -\sum_t \log p_\theta(\hat{y}_t|\hat{y}_{1:t-1}, X)$$

**阶段三：分层奖励 PPO 强化学习。** 将微调后的模型作为 Actor（策略网络），同时初始化 Critic（价值网络），通过 PPO 算法在编译器与执行器构成的环境中进一步优化。奖励函数由三个层次构成：

- **正确性奖励**：$R_{\mathrm{correctness}} = R_{\mathrm{compile}} + \mathbb{I}_{\mathrm{compile}} \cdot R_{\mathrm{test}}$，编译成功得 $+0.5$，功能测试通过再得 $+0.5$。
- **效率奖励**：$R_{\mathrm{efficiency}} = r_{\mathrm{eff}} \times \left( \frac{t_{\mathrm{base}}(X)}{t(\hat{Y}, X)} - 1 \right) \cdot \mathbb{I}_{\mathrm{test}}$，以 cuSPARSE 为基线计算加速比，仅在功能正确时生效。
- **最终奖励**：$R_{\mathrm{final}}(\hat{Y}, X) = R_{\mathrm{correctness}} + R_{\mathrm{efficiency}} - r_{\mathrm{penalty}} \cdot \mathbb{I}_{\mathrm{memory}}$，额外引入共享内存超额使用惩罚。

解码过程中还集成了动态 CUDA 语法/语义检查机制，检测到错误时提前终止生成，避免无效采样浪费计算资源。

### 关键设计决策

框架在三个关键维度上区别于现有方法：

| 设计维度 | 基线方法 | SparseRL |
|---------|---------|----------|
| 输入表示 | 自然语言提示 + 稀疏矩阵索引文本 | 稀疏矩阵行列索引的正弦嵌入（去除语言提示） |
| 训练目标 | 交叉熵损失（token 级匹配） | 分层奖励下的 PPO 训练 |
| 解码控制 | 标准自回归解码 | 动态语法/语义检查，错误时提前终止 |

这种设计将优化目标从“模仿参考代码”转变为“生成高效代码”，使模型能够探索监督学习中无法触及的性能空间。



### 3.1 任务形式化与监督微调目标

SparseRL 将稀疏 CUDA 代码生成形式化为一个条件生成问题。给定稀疏矩阵的输入序列 $X = ((r_1, c_1), \dots, (r_N, c_N))$（其中 $r_i$、$c_i$ 分别为第 $i$ 个非零元素的行、列索引），目标是生成满足以下三个条件的 CUDA 代码 $\hat{Y}$：

$$
\left\{ \begin{array}{ll} \mathrm{Compile}(\hat{Y}) = \mathrm{True} \\ \mathrm{Correct}(\hat{Y}, X) = \mathrm{True} \\ E(\hat{Y}|X) \leq E(Y_i|X), \forall Y_i \in \mathcal{Y} \end{array} \right.
$$

即生成的代码必须编译通过、计算结果正确，且执行时间不超过任何正确实现。在监督微调阶段，优化目标为最小化交叉熵损失：

$$
\mathcal{L}_{ce}(\theta) = -\sum_t \log p_\theta(\hat{y}_t|\hat{y}_{1:t-1}, X)
$$

然而，该 token 级匹配目标无法区分语义正确但性能不同的实现，且缺乏对执行效率的奖励信号——这正是引入强化学习的核心动机。

### 3.2 稀疏矩阵的正弦嵌入

为消除稀疏矩阵结构化输入与自然语言模态之间的鸿沟，SparseRL 采用正弦位置编码将行、列索引映射为连续向量。对于索引 $ind$（行索引或列索引），其第 $2j$ 和 $2j+1$ 维的编码为：

$$
PE_{(ind,2j)} = \sin\left(ind / 10000^{2j/d_{model}}\right), \quad PE_{(ind,2j+1)} = \cos\left(ind / 10000^{2j/d_{model}}\right)
$$

其中 $d_{model}$ 为模型隐藏维度。对于第 $i$ 个非零元素，将其行编码向量 $e_{r_i}$ 与列编码向量 $e_{c_i}$ 拼接，形成输入向量 $e_i = [e_{r_i} \mid e_{c_i}]$。该嵌入通过一个额外的线性层映射至模型维度。在 SFT 和 RL 阶段，自然语言提示被完全移除，模型仅接收稀疏矩阵的正弦嵌入作为输入。

### 3.3 分层奖励函数设计

SparseRL 的核心创新在于将预训练语言模型视为随机策略，通过 PPO 从编译器与执行器反馈中学习。奖励函数由三个层次构成：

**正确性奖励**：编译奖励 $R_{\mathrm{compile}}$ 与测试奖励 $R_{\mathrm{test}}$ 之和（测试奖励仅在编译成功时计算）：

$$
R_{\mathrm{correctness}} = R_{\mathrm{compile}} + \mathbb{I}_{\mathrm{compile}} \cdot R_{\mathrm{test}}
$$

其中 $R_{\mathrm{compile}}$ 和 $R_{\mathrm{test}}$ 分别设为 $\pm 0.5$（成功为 $+0.5$，失败为 $-0.5$），$\mathbb{I}_{\mathrm{compile}}$ 为编译成功的指示函数。

**效率奖励**：以 cuSPARSE 为基线的缩放加速比，仅在功能测试通过时计算：

$$
R_{\mathrm{efficiency}} = r_{\mathrm{eff}} \times \left( \frac{t_{\mathrm{base}}(X)}{t(\hat{Y}, X)} - 1 \right) \cdot \mathbb{I}_{\mathrm{test}}
$$

其中 $t_{\mathrm{base}}(X)$ 为 cuSPARSE 在矩阵 $X$ 上的执行时间，$t(\hat{Y}, X)$ 为生成代码的执行时间，$r_{\mathrm{eff}}$ 为效率奖励缩放因子，$\mathbb{I}_{\mathrm{test}}$ 为测试通过的指示函数。

**最终奖励**：整合正确性、效率与内存约束：

$$
R_{\mathrm{final}}(\hat{Y}, X) = R_{\mathrm{correctness}} + R_{\mathrm{efficiency}} - r_{\mathrm{penalty}} \cdot \mathbb{I}_{\mathrm{memory}}
$$

其中 $r_{\mathrm{penalty}}$ 为内存超额惩罚系数，$\mathbb{I}_{\mathrm{memory}}$ 在生成代码使用的共享内存超过硬件上限时激活。

### 3.4 动态解码控制

在 RL 阶段，SparseRL 集成了动态 CUDA 语法/语义检查机制：解码过程中实时验证生成代码的语法正确性，一旦检测到错误（如未闭合的括号、无效的 CUDA 关键字等）即提前终止生成，避免在无效序列上浪费计算资源。该机制不仅加速了 RL 的探索效率，也间接提升了有效样本的生成比例。



## 实验与关键发现

### 核心瓶颈与因果机制

现有代码生成方法在稀疏 CUDA 场景下失效的根因可归结为三个相互强化的瓶颈。首先，稀疏矩阵的不规则非零分布导致执行模式高度动态——同一 SpMV 算法在不同稀疏模式下的内存访问模式、warp 利用率差异可达数量级，迫使实现必须针对矩阵结构定制化。其次，监督微调（SFT）的 token 级交叉熵目标存在根本性错配：它能区分语法正误，却无法区分“语义正确但性能迥异”的两种实现，更无从获取执行效率的反馈信号。第三，稀疏矩阵的结构化索引与自然语言之间存在模态鸿沟，文本提示难以有效传达矩阵的拓扑信息。

SparseRL 的核心干预是**将生成问题从监督学习重构为深度强化学习**：将预训练语言模型视为随机策略，生成步骤作为动作，从编译器与执行器构成的“环境”中获取分层奖励信号。这一重构的因果效果体现在两方面——编译与测试奖励直接优化代码正确性，而效率奖励（以 cuSPARSE 为基线的加速比缩放值）驱动模型探索更高性能的实现。同时，用稀疏矩阵行列索引的正弦嵌入替代自然语言提示，消除了模态差异，使模型直接感知矩阵结构。

### 主要实验结果

**Table 1** 汇总了各方法在 SuiteSparse SpMV 和 SpMM 任务上的正确性与编译率。SparseRL+Qwen2.5-14B 在 SpMV 上取得 pass@1000 = 49.25、编译率（CR）= 57.50，相较 CodeRL+CodeT5-770M 的 36.50 / 39.50 分别提升 +12.75 和 +18.00 个百分点。值得注意的是，SparseRL 即使搭载较小的 CodeT5-770M 骨干，其 pass@1000（48.75）和 CR（56.50）仍显著超过参数量大得多的开源模型（如 Qwen3-14B 的 28.75 / 47.50），表明框架设计而非模型容量是性能提升的主因。


![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/003_Table_1.jpg]]
*Table 1: Correct functionality (pass@k) and Compilation Rates (CR) under k = 1000*

**Figure 3** 展示了 SpMV 在 V100 和 A100 上的 GFLOPS 分布。SparseRL 在 V100 上相对 cuSPARSE 取得平均 1.42× 加速比，相对 TVM-S 为 1.82×；在 A100 上分别为 1.44× 和 1.86×。箱线图显示 SparseRL 的性能优势在中等稀疏度矩阵上尤为突出，但在极高稀疏度（>99.9% 零值）的尾部分布中，cuSPARSE 手工优化核仍保持优势（详见失败模式分析）。与同为 RL-based 方法的 CodeRL 和 PPOCoder 相比，SparseRL 在 V100 上分别实现 3.27× 和 3.42× 的 GFLOPS 提升，验证了分层奖励与稀疏嵌入的联合效应。


![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/004_Figure_3.jpg]]
*Figure 3: Performance (GFLOPs) of SpMV across SuiteSparse Matrices on (a) V100 (b) A100 GPUs*

**Figure 4** 将评估扩展至 SpMM 任务（稀疏矩阵-稠密矩阵乘法）。在 column=8 设置下，SparseRL 在 A100 上相对 Sputnik 取得平均 2.32× 加速比，相对 CodeRL 达 6.80×；column=32 时加速比分别为 1.22× 和 4.50×。column 数增大时加速比收窄，可能因为稠密矩阵列维度增加后，计算密集度上升，掩盖了稀疏访存优化的相对收益。

### 消融实验

**Table 2** 系统拆解了三阶段训练流程的贡献。完整流程（Pretrain+SFT+PPO）的 SpMV pass@1000 为 49.25，去掉预训练后骤降至 40.75（-8.50），编译率从 57.50 降至 48.75，证实 CUDA 代码增强预训练对注入并行编程与硬件优化先验知识不可或缺。仅 SFT 而无 RL 的配置 pass@1000 为 45.50（-3.75），说明 RL 阶段的执行效率奖励信号能进一步推动模型超越监督模仿的上限。仅 RL 而无 SFT 的配置 pass@1000 仅 30.25，表明 SFT 提供的“暖启动”策略对稳定 RL 探索至关重要。


![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/006_Table_2.jpg]]
*Table 2: Ablation comparison between the three phases (Pre-training/SFT/RL)*

**Table 3（及 Table 11）** 对比了三种稀疏矩阵嵌入策略。正弦嵌入在 SparseRL+CodeT5-770M 上取得 pass@1000 = 48.75，显著优于线性投影（44.50）和可学习嵌入（43.25）。正弦嵌入的优势源于其归纳偏置——通过三角函数捕获行列索引的连续位置关系，使模型能泛化到训练中未见过的矩阵维度范围，而可学习嵌入在索引值外推时失效。


![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/007_Table_3.jpg]]
*Table 3: Ablation study of sparse matrix embedding on correct functionality (pass@k) and Compilation Rates (CR) under k = 1000*

**Figure 5** 进一步消融了 SparseRL 内部组件。base（仅基础模型）、base+op1（加入 RL 优化但无效率奖励）、base+op1+op2（完整 SparseRL）的 GFLOPS 逐步递增，在 nemeth22 和 ga2010 两个代表性矩阵上完整配置取得最高性能。效率奖励（op2）的加入使模型从“生成正确代码”进化到“生成正确且高效的代码”。

**Table 4 和 Table 5** 考察了关键超参数的敏感度。效率奖励缩放因子 $r_{\mathrm{eff}}$ 在 0.5–2.0 范围内，pass@1000 波动不超过 2 个点，最优值为 1.0；内存惩罚系数 $r_{\mathrm{penalty}}$ 在 0.1–0.5 范围内表现稳健，0.3 时取得最佳编译率与性能平衡。这组结果表明奖励函数设计具有良好的超参数鲁棒性。


![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/009_Table_4.jpg]]
*Table 4: Impact of Varying $r _ { \mathrm { e f f } }$ (Fixed $r _ { \mathrm { p e n a l t y } }$ = 0 . 3 )

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/010_Table_5.jpg]]
*Table 5: Impact of Varying $r _ { \mathrm { p e n a l t y } }$ (Fixed $r _ { \mathrm { e f f } }$ = 1 . 0 )

### 与其他方法的对比

**Table 6–8** 将 SparseRL 与开源模型、闭源模型及 LLM4EFFI 等竞争工作进行了多维度对比。在 pass@5 设定下，SparseRL 生成正确代码的相对 cuSPARSE 加速比（1.42×）显著优于 Qwen3-14B（0.89×）和 DeepSeek-R1（0.95×），说明通用 LLM 即使具备推理能力，仍缺乏稀疏计算的领域知识。与 LLM4EFFI 的对比（Table 8）进一步表明，SparseRL 在 pass@1 的正确率与加速比上均占优。



![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/013_Table_7.jpg]]
*Table 7: Correct functionality (pass@k) and performance (Speedup vs. cuSPARSE) comparison for correct generated program on pass@5*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/012_Table_6.jpg]]
*Table 6: Correct functionality (pass@k) and Performance (Speedup vs. cuSPARSE) comparison for correct generated program on pass@5*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/014_Table_8.jpg]]
*Table 8: Results of correct functionality (pass@k) and performance evaluated by speedup. Correctly generated code on pass@1 is used to evaluate the speedup compared with cuSPARSE*

**Table 9** 在 DLMC 数据集上验证了跨数据分布的泛化能力，SparseRL 的 GFLOPS 持续领先 TVM-S 和 cuSPARSE。**Table 10** 展示了 SparseRL 框架在不同 LLM 骨干（CodeT5、Qwen2.5-14B、LLaMA 3 70B）上的即插即用能力，其中 Qwen2.5-14B 取得最佳综合表现。

### 失败模式与局限性

**Table 17** 揭示了 SparseRL 的主要失效场景：对于极度不规则且稀疏度极高（>99.9% 零值）的矩阵（如 va2010、az2010），cuSPARSE 手工优化核仍保持性能优势。这类矩阵的非零元素分布极不均匀，手工核针对特定稀疏模式进行了 warp 级负载均衡和共享内存预取优化，而 SparseRL 生成的通用模板代码难以匹敌这种领域专家级的微观调优。

训练成本方面（**Table 18**），RL 阶段总耗时约 120 小时（5 天 × 8 GPUs），其中执行时间反馈占比高达 35%，因为每次奖励计算需实际编译、运行并计时。当非零元素数量极大时，需对输入索引进行采样以控制序列长度，可能损失部分结构信息。此外，增量领域预训练对 70B+ 模型仍需可观计算资源，虽然通过并行策略控制在数天内。

### 关键图表索引

- **Table 1**: 主结果——各方法在 SpMV/SpMM 上的 pass@k 与编译率
- **Figure 3**: SpMV 性能箱线图（V100/A100 GFLOPS 分布）
- **Figure 4**: SpMM 性能箱线图（column=8/32 的 TFLOPs）
- **Table 2**: 三阶段消融（预训练/SFT/RL 的独立贡献）
- **Table 3 / Table 11**: 稀疏矩阵嵌入策略消融
- **Figure 5**: 组件消融（base/op1/op2 的 GFLOPS 对比）
- **Table 4–5**: 超参数敏感度（$r_{\mathrm{eff}}$ 和 $r_{\mathrm{penalty}}$）
- **Table 6–8**: 与开源/闭源模型及竞争工作的对比
- **Table 17**: 失败案例（高度不规则矩阵上 cuSPARSE 仍占优）

### 补充图表

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/011_Figure_6.jpg]]
*Figure 6: PPO diagnostics (KL, entropy, value loss, reward) over training*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_VdLEaGPYWT/figures/028_Table.jpg]]
*Table: 1. SparseRL on Closed-Source Outputs. Feeding GPT-5/Claude-Sonnet-4 kernels into SparseRL’s RL loop (reward: efficiency + correctness by off-policy GRPO) improves runtime by 28–35% on 100 test matrices: 2. Controlled Open-Source Comparison. On LLaMA 3 70B (matching closed-source scale)*



## 定位与知识库关联

### 方法定位与核心差异

SparseRL 处于**代码大语言模型（Code LLM）与系统性能优化**的交叉地带。其方法谱系可沿两条轴线展开：一是代码生成的训练范式演进，二是稀疏计算的内核生成传统。

**从训练范式看**，SparseRL 将预训练代码模型的优化从监督学习的“token 级模仿”推进到强化学习的“执行反馈驱动”。传统代码生成方法——无论是通用 Code LLM（如 **CodeT5** (Wang et al., 2021)、**Qwen3** (Hui et al., 2024; Yang et al., 2025)）还是面向代码的 RL 方法（如 **CodeRL** (Le et al., 2022)、**PPOCoder** (Shojaee et al., 2023)）——均以交叉熵损失为训练目标。这一目标的根本缺陷在于：它无法区分“语义正确但性能迥异”的两种实现，因为 token 序列的似然与运行时效率之间不存在单调映射。SparseRL 的关键突破是将训练目标替换为**分层奖励函数**，该函数直接编码了编译正确性（$R_{\mathrm{compile}} = \pm 0.5$）、功能测试通过性（$R_{\mathrm{test}} = \pm 0.5$）以及以 cuSPARSE 为基线的执行加速比（$R_{\mathrm{efficiency}} = r_{\mathrm{eff}} \times (t_{\mathrm{base}} / t - 1)$），并辅以共享内存超额惩罚。这一设计使得优化信号从“像不像参考代码”转变为“跑得快不快、对不对”，从而将模型视作随机策略，通过 PPO 从编译器与执行器的真实反馈中学习。

**从稀疏计算传统看**，SparseRL 的竞争对手是手工优化的稀疏线性代数库与编译器。**cuSPARSE** (Naumov et al., 2010) 是 NVIDIA 官方库，其内核由领域专家针对特定稀疏模式手工调优，在极度不规则矩阵上仍具统治力。**TVM-S** (Chen et al., 2018) 将 TVM 编译器扩展至稀疏场景，通过自动调度搜索优化实现。SparseRL 与这两者的本质区别在于：它不依赖手工特征工程或显式的搜索空间定义，而是将稀疏矩阵的结构信息通过正弦嵌入注入预训练模型，让模型“学会”从矩阵的非零模式直接推断最优并行化策略。实验表明，SparseRL 在 SuiteSparse 测试集上相对 cuSPARSE 平均加速 1.42×（V100），相对 TVM-S 加速 1.82×（V100），证明学习型方法在多数矩阵上有能力超越手工与编译优化。

### 与相关工作的关系边界

**CodeRL / PPOCoder**：这两者率先将 RL 引入代码生成，但它们的奖励信号仍主要基于功能正确性（如单元测试通过率），未系统性地编码执行效率。SparseRL 在此基础上叠加了效率奖励和内存约束，且针对稀疏 CUDA 领域设计了专用的输入表示（正弦嵌入替代自然语言提示），使得 RL 框架能够感知矩阵结构与运行时性能的耦合关系。实验显示，SparseRL+CodeT5-770M 的 SpMV pass@1000 为 49.25，而 CodeRL+CodeT5-770M 仅为 36.50，编译率差距更达 18 个百分点（57.50 vs. 39.50），表明分层奖励与稀疏嵌入的组合远优于通用 RL 代码生成方案。

**LLM4EFFI 等竞争工作**：论文在 Table 8 中与 LLM4EFFI 进行了直接对比，SparseRL 在 pass@k 和加速比上均占优。但需注意，这些对比基于论文自身报告的实验设置，外部验证数据有限，建议读者关注其附录中的公平性控制实验（模型大小匹配、采样预算匹配）以判断结论的稳健性。

**封闭源模型**：SparseRL 与 GPT-5、Claude-Sonnet-4 等封闭源模型的对比揭示了有趣的现象：即使将这些模型的输出内核送入 SparseRL 的 RL 循环（采用 off-policy GRPO，奖励为效率+正确性），运行时可进一步缩短 28–35%（Table A.27）。这表明 SparseRL 的 RL 框架具有“即插即用”的后优化能力，可叠加于任意代码生成器的输出之上。

### 适用边界

SparseRL 的优势区间集中在**中等稀疏度、具有可学习结构模式的矩阵**。当稀疏度极高（>99.9% 零值）且非零分布极度不规则时，cuSPARSE 的手工优化核仍保持领先。Table 17 明确记录了失败案例：在 va2010、az2010 等高度不规则矩阵上，SparseRL 生成的代码性能落后于 cuSPARSE。论文将此归因于 RL 训练数据中此类极端模式的覆盖不足，以及模型对“无规律可循”的矩阵难以归纳出优于手工启发式策略的并行方案。

此外，SparseRL 目前仅验证于 SpMV 和 SpMM 两类稀疏操作。框架本身对稀疏性的利用方式（正弦嵌入编码非零索引）理论上可推广至任意稀疏张量运算，但这一推广尚未在论文中得到实验支撑，属于开放问题。

### 局限与开放问题

**训练成本**：RL 阶段的总耗时约 120 小时（5 天 × 8 GPUs），其中执行时间反馈占比高达 35%（Table 18）。这一成本使得快速迭代和超大规模扩展受到制约。论文提出的缓解方向是训练代理奖励模型（如 GNN 预测执行时间），但如何在降低反馈成本的同时不显著损害最终性能，仍是未解问题。

**极端不规则矩阵的泛化**：如失败案例所示，SparseRL 在“无规律”矩阵上尚未超越手工核。是否需要更强的 RL 算法（如引入好奇心驱动探索或层次化策略）来突破这一瓶颈，值得进一步研究。

**输入规模限制**：当非零元素数量极大时，需对输入索引进行采样以适配模型上下文窗口，这可能损失部分结构信息（Section A.21）。如何在有限上下文内保留关键稀疏模式，是工程部署中的实际挑战。

**框架推广性**：将 SparseRL 从稀疏 CUDA 推广至其他 HPC 代码优化任务（如稠密矩阵运算、模板计算、图算法）需要重新设计输入表示和奖励函数，其可行性尚未经实验检验。

**RL 算法选择**：论文尝试了 PPO、GRPO 和 Reinforce++，最终选择 PPO 的理由是“性能已经足够好”（Section 5.4）。但 GRPO 的 pass@1000 仅比 PPO 低 0.7%（48.9 vs. 49.3），且 GRPO 无需价值网络，训练开销更低。是否存在更优的 RL 算法组合（如离线 RL 或基于模型的 RL）以进一步压缩训练时间，值得探索。

**可读性与可维护性**：论文在 Appendix A.20 中报告了可读性测试，但未在主文中详细展开。生成代码的可维护性对于实际部署至关重要，这一维度的评估尚不充分。



## 原文 PDF

![[paperPDFs/ICLR_2026/Mastering_Sparse_CUDA_Generation_through_Pretrained_Models_and_Deep_Reinforcement_Learning.pdf]]
