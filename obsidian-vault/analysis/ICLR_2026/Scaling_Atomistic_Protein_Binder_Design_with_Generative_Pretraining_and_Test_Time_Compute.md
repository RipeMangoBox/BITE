---
title: "Scaling Atomistic Protein Binder Design with Generative Pretraining and Test-Time Compute"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Scaling_Atomistic_Protein_Binder_Design_with_Generative_Pretraining_and_Test_Time_Compute.pdf
project_link: https://research.nvidia.com/labs/genair/proteina-complexa/
code_link: null
openreview_forum_id: qmCpJtFZra
aliases:
- PNCC
- SAPBDGPTTC
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过统一的流匹配生成基础模型（在合成蛋白二聚体数据集Teddymer上预训练）与灵活的测试时优化（波束搜索、费曼-卡茨转向、蒙特卡洛树搜索等）相结合，利用生成先验引导搜索过程。"
primary_logic: "将预训练的原子级流匹配生成器与测试时优化统一，打破了生成与幻觉之间的错误二分法；大规模合成数据（Teddymer）和分阶段预训练赋予了模型强大的生成能力，而推理时搜索进一步将生成先验转化为超越纯生成与纯幻觉方法的性能。"
claims:
- "Complexa在蛋白质及小分子靶点的计算机结合成功标准上显著超越所有先前生成模型。"
- "Teddymer合成数据集与翻译噪声对模型实际性能至关重要；去除任何一项均会导致唯一结合剂数量大幅下降。"
- "在归一化计算预算下，Complexa的测试时优化方法（如波束搜索、费曼-卡茨转向）在困难靶点上显著优于纯幻觉方法BindCraft和BoltzDesign。"
- "Complexa在酶设计基准上大幅领先RFDiffusion2，在41个任务中的38个取得更优唯一成功率。"
---

# Scaling Atomistic Protein Binder Design with Generative Pretraining and Test-Time Compute

> [!tip] 核心洞察
> 将预训练的原子级流匹配生成器与测试时优化统一，打破了生成与幻觉之间的错误二分法；大规模合成数据（Teddymer）和分阶段预训练赋予了模型强大的生成能力，而推理时搜索进一步将生成先验转化为超越纯生成与纯幻觉方法的性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 利用生成式预训练与测试时计算扩展原子级蛋白质结合蛋白设计 |
| 英文题名 | Scaling Atomistic Protein Binder Design with Generative Pretraining and Test-Time Compute |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=qmCpJtFZra) · [Project](https://research.nvidia.com/labs/genair/proteina-complexa/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Proteína-Complexa (Complexa) |
| Dataset | 19蛋白质靶点（含简单与困难）, 4小分子靶点（SAM, FAD, IAI, OQO）, 蛋白质靶点推理时缩放（简单/困难各12/7个）, 酶设计基准（AME，41个催化位置重构任务） |

> [!tip] 效果简介
> - 19蛋白质靶点（含简单与困难） 上，# Unique Successes (MPNN) 为 平均14.4（独家生成序列评估约9.1），对比 RFDiffusion等所有先前模型均显著低于Complexa（具体值见表10），变化 断层式领先，为最优方法的40%以上。
> - 4小分子靶点（SAM, FAD, IAI, OQO） 上，# Unique Successes 为 IAI: 19；FAD: 17；OQO: 6；SAM: 10（自生成序列），对比 RFDiffusion-AllAtom（依赖LigandMPNN重新设计）成功数远低于Complexa，例如IAI约6.47，变化 平均成功数提升2-3倍。
> - 蛋白质靶点推理时缩放（简单/困难各12/7个） 上，Unique Success Rate 为 在固定GPU小时预算下，Complexa的最佳N、波束搜索、MCTS等策略超出BindCraft和BoltzDesign数倍，尤其在困难靶点上优势更明显。，对比 BindCraft（纯幻觉）和BoltzDesign（梯度优化幻觉）在相同计算资源下成功率极低，变化 在困难靶点上成功率至少高一个数量级。

## 概要

蛋白质结合剂（binder）的从头设计是药物发现与合成生物学的核心挑战。现有方法在此问题上形成了两个割裂的范式：**生成式模型**（如 RFDiffusion、Protopardelle）一次性采样结构，缺乏对生成过程的在线引导；**幻觉方法**（如 BindCraft、BoltzDesign）则完全依赖结构预测模型的梯度优化，无法利用生成先验进行高效搜索。这一错误二分法导致在有限计算预算下，两类方法均难以在困难靶点上取得可靠的成功率。

本文提出 **Proteína-Complexa (Complexa)**，首次将强生成先验与灵活的测试时优化统一于同一框架。其核心瓶颈突破在于：**预训练的原子级流匹配生成器提供了高质量的候选分布，而推理时搜索算法（波束搜索、费曼-卡茨转向、蒙特卡洛树搜索）则利用结构预测模型作为奖励函数，在生成轨迹上引导采样，从而将生成先验转化为远超纯生成与纯幻觉方法的实际性能。**

**方法定位**：Complexa 基于 La-Proteína 的部分潜在流匹配架构，通过三个关键创新实现结合剂设计——（1）构建大规模合成二聚体数据集 Teddymer（从 AFDB 结构域互作中提取约 350 万簇），赋予模型对蛋白-蛋白界面的生成能力；（2）引入潜在目标条件机制与全局翻译噪声，使模型在生成过程中持续推理结合剂相对于靶点的空间定位；（3）集成多种测试时扩展算法，在归一化 GPU 小时预算下显著提升样本质量与多样性。

**主要结果**：
- 在 19 个蛋白质靶点上，Complexa 的纯生成模式（不经优化）即**断层式领先**所有先前生成模型，唯一成功数平均达 14.4（MPNN 重设计），较最优基线提升 40% 以上。
- 在 4 个小分子靶点上，Complexa 自生成序列的成功数达到 **RFdiffusion-AllAtom 的 2-3 倍**。
- 在归一化计算预算下，Complexa 的测试时优化策略在困难靶点上的成功率**比 BindCraft 和 BoltzDesign 高出一个数量级**。
- 在酶设计基准（AME，41 个催化位置重构任务）中，Complexa 在 **38/41 任务上优于 RFDiffusion2**，且自生成序列模式下实现 41/41 任务全部成功。

**关键消融**：Teddymer 合成数据集与翻译噪声是模型性能的基石——移除 Teddymer 导致唯一成功数从 14.4 骤降至 3.84（MPNN 评估），且在 19 个靶点上无一次胜出；去除翻译噪声同样显著降低性能。这表明**大规模合成训练数据与空间定位能力对于原子级结合剂设计至关重要**。

**重要局限**：所有评估均基于计算指标（ipAE、pLDDT 等），尚未经湿实验验证；对极难靶点（如 TNF-α、H1）仍需数百至上千 GPU 小时才能获得足量唯一结合剂；当前框架仅针对蛋白质和小分子靶点演示，尚未扩展至 DNA、RNA 等其他模态。

蛋白质结合蛋白（protein binder）的从头设计是蛋白质工程的核心挑战之一，其目标是为给定的靶点分子生成能够高亲和力、高特异性结合的蛋白质序列与结构。这一能力在治疗性抗体开发、生物传感器设计、酶工程等领域具有广泛的应用前景。近年来，随着深度生成模型和结构预测模型的快速发展，计算驱动的结合蛋白设计取得了显著进展，但现有方法仍面临根本性的瓶颈。

### 现有方法的二元分裂

当前的计算结合蛋白设计方法大致可归为两类范式：

**生成式方法（Generative Methods）** 直接学习从靶点条件到结合蛋白结构的映射。代表性工作包括 **RFDiffusion**（Watson et al., Nature 2023），它利用条件扩散模型生成蛋白质骨架，随后通过 ProteinMPNN 进行序列设计；其全原子扩展 **RFDiffusion-AllAtom**（Krishna et al., 2024）进一步支持小分子等非蛋白质靶点。此外，**Protopardelle**（Chu et al., 2024; Lu et al., 2025）和 **APM**（Chen et al., 2025）等模型也探索了全原子蛋白质生成。这类方法的优势在于能够快速采样大量候选分子，但其生成质量受限于训练数据的分布，难以针对特定靶点进行精细优化。

**幻觉方法（Hallucination Methods）** 则从一个随机的蛋白质序列出发，利用结构预测模型（如 AlphaFold2、Boltz-1）的梯度信号迭代优化序列，使其“幻觉”出与靶点结合的构象。代表方法包括 **BindCraft**（Pacesa et al., 2025），它基于 AlphaFold2 评分进行梯度优化；**BoltzDesign**（Cho et al., 2025）使用 Boltz-1 结构预测器扩展至多种靶点模态；以及 **AlphaDesign**（Jendrusch et al., 2025），它采用遗传算法替代梯度优化。这类方法的优势在于能够针对特定靶点进行深度优化，但其搜索过程缺乏有效的先验引导，在计算资源受限时效率低下，且容易陷入局部最优。

### 核心瓶颈：生成先验与优化搜索的割裂

上述两类范式之间存在一个错误的二分法：生成式方法拥有强大的先验知识但缺乏灵活的优化能力，幻觉方法具备优化灵活性但缺乏生成先验的引导。这一割裂导致了两个关键问题：

1. **纯生成方法无法利用推理时的额外计算资源来提升特定靶点的成功率**——一旦模型训练完成，其生成质量就固定了，无法针对困难靶点进行“更深度的思考”。
2. **纯幻觉方法在有限的推理计算预算下效率极低**——由于缺乏对可行结合蛋白空间的先验认知，其搜索过程从随机起点出发，需要大量迭代才能偶然发现有效解，尤其在困难靶点上成功率极低。

这种二元分裂的根本原因在于，现有方法未能将生成式预训练与测试时优化统一为一个连贯的框架。一个理想的结合蛋白设计系统应当能够：利用大规模预训练数据习得结合蛋白空间的丰富先验，同时在推理时灵活地利用结构预测模型的反馈信号进行定向搜索，从而在给定的计算预算下最大化成功率。

### 本文的动机与核心思路

针对上述瓶颈，本文提出 **Proteína-Complexa (Complexa)**，一个将强生成先验与灵活测试时优化相统一的结合蛋白设计框架。其核心洞察在于：预训练的原子级流匹配生成器与测试时优化并非互斥的两种范式，而是可以协同工作的互补组件。具体而言，Complexa 在以下三个层面打破了生成与幻觉之间的错误二分法：

- **统一的生成基础模型**：在 La-Proteína 流匹配架构的基础上，引入潜在目标条件机制和翻译噪声训练目标，并在大规模合成二聚体数据集 Teddymer 上进行预训练，赋予模型强大的条件生成能力。
- **灵活的测试时优化**：将波束搜索、费曼-卡茨转向、蒙特卡洛树搜索等推理时缩放技术适配到流匹配生成框架中，利用结构预测模型的界面评分作为奖励信号引导采样过程。
- **生成与幻觉的混合策略**：允许先由生成模型初始化候选结构，再通过幻觉方法进行序列精修，实现两种范式的优势互补。

这一统一框架使得 Complexa 在归一化的计算预算下，能够显著超越纯生成方法和纯幻觉方法，为蛋白质结合蛋白的从头设计提供了新的技术路径。

## 核心方法与创新机理

Complexa的核心创新在于**打破生成式建模与幻觉优化的错误二分法**，将预训练的流匹配生成基础模型与灵活的测试时优化统一为单一框架。这一统一并非简单的工程拼接，而是通过三个相互依赖的机制层面变革实现的。

### 从单体生成到目标条件生成：潜在目标条件与翻译噪声

Complexa构建于La-Proteína（Geffner et al., 2026）之上，但其关键改造在于引入**潜在目标条件机制**。原始La-Proteína仅支持单体生成，而Complexa将靶点表示为Atom37特征、氨基酸身份与热点标记的拼接，与噪声化的结合剂表示一同输入Transformer，实现条件生成（Figure 5）。该设计的精巧之处在于：编码器与解码器在条件训练期间保持冻结，仅需训练去噪网络，从而保留了预训练自编码器对蛋白结构的压缩能力。

与条件机制同等重要的是**全局翻译噪声**的引入。训练时，结合剂的Cα坐标被施加标量随机平移 $d \sim \mathcal{N}(0, 0.2^2)$（单位：nm），迫使模型在生成过程中持续推理结合剂相对于靶点的正确空间位置。这一看似简单的设计（Eq. 1）解决了生成模型在推理时面临的全局定位模糊问题——消融实验表明，去除翻译噪声导致唯一成功数显著下降（Table 6, Figure 13）。

### 数据驱动生成先验：Teddymer合成数据集

Complexa生成能力的另一支柱是**Teddymer**——一个从AlphaFold数据库（AFDB）预测单体结构中提取域-域互作构建的大规模合成二聚体数据集（Figure 3, Figure 4）。其构建流程为：将AFDB多域单体拆分为独立域，提取空间邻近的二聚体，经CAT注释完整性与聚类去重后，获得约350万簇。Teddymer的规模远超PDB（约22.5万条目），且其界面特征与真实多聚体结构具有分布重叠，为模型提供了丰富的结合剂-靶点互作训练信号。

消融实验揭示了Teddymer的决定性作用：移除Teddymer导致MPNN评估的平均唯一成功数从14.4骤降至3.84，自生成序列评估更是从9.10降至0.15，且在全部19个蛋白质靶点上无一次胜出（Table 6, Table 7, Figure 13）。这一结果说明，大规模合成数据赋予了模型超越PDB有限样本的泛化能力。

### 分阶段预训练策略

Complexa采用**三阶段训练流程**将上述数据与架构整合：
1. **自编码器预训练**：在AFDB单体上训练VAE，随后在PDB结构上微调；
2. **流匹配模型预训练**：在编码后的AFDB Foldseek聚类代表上预训练去噪网络；
3. **目标条件微调**：在Teddymer/PDB多聚体混合数据上微调，赋予模型结合剂-靶点条件生成能力。

对于小分子靶点，额外使用LoRA（Hu et al., 2022）避免在小型PLINDER数据集上过拟合。这一分阶段策略确保了模型在接触条件任务前已习得稳健的蛋白结构先验。

### 生成先验引导的测试时优化

Complexa的推理框架将生成模型视为**可操纵的搜索先验**，集成四种测试时扩展算法：
- **最佳N采样**：直接筛选ipAE < 7.0的样本；
- **波束搜索**：每K步从候选集中选取奖励之和最高的N个状态（Eq. 2）；
- **费曼-卡茨转向**：通过指数加权奖励实现重要性采样，逼近倾斜分布（Eq. 3）；
- **蒙特卡洛树搜索**：平衡利用与探索的选择准则（Eq. 4）。

这些算法均以结构预测模型（AlphaFold2或RosettaFold-3）的界面置信度（$f_{\text{ipAE}}$）或氢键能量（$f_{\text{H-Bond}}$）作为奖励信号。与纯幻觉方法（如BindCraft、BoltzDesign）的根本区别在于：Complexa的搜索从生成先验出发，而非从随机初始化开始优化，从而在归一化计算预算下实现数量级的成功率提升（Figure 7, Figure 8, Figure 22）。

### 创新机制间的因果依赖

上述创新并非独立生效，而是形成因果链条：Teddymer提供训练信号→翻译噪声迫使空间推理→分阶段训练稳定习得→生成先验赋能高效搜索。消融实验中去除任一环节均导致性能崩塌，验证了这一依赖关系。此外，“生成+幻觉”混合策略（以生成模型初始化BindCraft）在简单靶点上优于纯幻觉方法，但在困难靶点上仍不及内置搜索算法（Figure 16-18），进一步证明生成先验与搜索算法的深度耦合是突破性能瓶颈的关键。

### 设计动机与统一范式

蛋白质结合剂（binder）设计的核心挑战在于生成能够高亲和力、高特异性结合靶点蛋白或小分子的氨基酸序列与三维结构。现有方法将这一任务割裂为两个独立范式：**生成式模型**（如RFDiffusion、Protopardelle）直接从噪声采样候选结构，缺乏在推理阶段利用结构预测信号进行定向优化的能力；**幻觉方法**（如BindCraft、BoltzDesign）则从随机序列出发，通过梯度优化使结构预测模型“看到”期望的结合模式，但无法借助生成先验缩小搜索空间。这种二分法导致幻觉方法在困难靶点上计算效率极低，而纯生成方法虽速度快却难以突破成功率天花板。

Complexa（Proteína-Complexa）的核心洞见在于打破这一错误二分法：**将预训练的流匹配生成模型与灵活的测试时优化统一在同一框架下**。生成模型在合成二聚体数据集Teddymer上获得强大的结合剂先验，推理时通过波束搜索、费曼-卡茨转向等搜索算法，以结构预测分数为奖励引导采样过程，将生成先验转化为超越纯生成与纯幻觉方法的实际性能。

### 三阶段流水线概览

Complexa的整体框架由三个耦合模块构成，形成“编码—条件生成—解码”的完整闭环（图1顶部概述了目标条件生成流程）：

```
输入: 靶点结构 (蛋白/小分子)
  │
  ▼
┌─────────────────────────────────────┐
│  模块1: 自动编码器 (VAE)            │
│  · 仅编码结合剂链                   │
│  · 输出: Cα坐标 + 连续潜在变量 z    │
│  · 解码器: z → 全原子结构           │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│  模块2: 部分潜在流匹配模型 (Denoiser)│
│  · 接收靶点条件特征                 │
│  · 从高斯噪声逐步变换为潜在表示     │
│  · 强制推理全局平移定位             │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│  模块3: 测试时优化器                 │
│  · 结构预测模型评分 (AF2/RF3)       │
│  · 搜索算法引导采样                 │
│  · 输出: 高质量结合剂候选            │
└─────────────────────────────────────┘
```

#### 模块1：自动编码器（VAE）

Complexa继承并冻结了La-Proteína（Geffner et al., 2026）的自动编码器组件。该VAE将结合剂的原子坐标与序列信息压缩为两部分表示：**Cα坐标**（显式空间信息）与**逐残基连续潜在变量 z**（编码侧链构型与氨基酸身份）。关键设计在于，VAE仅需编码结合剂链，对任意靶点共享，无需适配——靶点信息仅在后续流匹配阶段注入。训练采用三阶段策略：先在AFDB单体上预训练VAE，再在PDB结构上微调。

#### 模块2：部分潜在流匹配模型（Denoiser）

这是Complexa的条件生成核心。模型在潜在空间中执行流匹配：接收靶点条件特征，将高斯噪声逐步变换为结合剂的Cα坐标与潜在变量。其架构为带成对偏置注意力的Transformer，输入由三部分拼接而成：

- **噪声化的结合剂表示**：当前时间步的Cα坐标与潜在变量
- **靶点条件特征**：采用Atom37方案编码靶点的全原子结构，结合氨基酸身份特征与二元热点标记（hotspot tokens）
- **时间步嵌入**：Cα坐标与潜在变量使用独立的时间调度

**全局翻译噪声**是关键的训练设计。在训练目标中，向结合剂的Cα坐标添加标量随机全局平移 $d \sim \mathcal{N}(0, 0.2^2)$（单位：nm），迫使模型在生成过程中持续推理结合剂相对于靶点的正确空间定位，而非记忆绝对坐标。完整训练目标为：

$$\min_{\phi} \mathbb{E}_{t_x, t_z, (\mathbf{x}, \mathbf{c}^{\mathrm{target}}) \sim p^{\mathrm{data}}, \mathbf{x}_0^{C_\alpha} \sim p_0^{C_\alpha}, \mathbf{z}_0 \sim p_0^{z}, d \sim p_0^{d}} \left[ \| \mathbf{v}_z^{\phi}(\mathbf{x}_{t_x}^{C_\alpha}, \mathbf{z}_{t_z}, \mathbf{c}^{\mathrm{target}}, t_x, t_z) - (\mathcal{E}(\mathbf{x}) - \mathbf{z}_0) \|^2 + \| \mathbf{v}_x^{\phi}(\mathbf{x}_{t_x}^{C_\alpha}, \mathbf{z}_{t_z}, \mathbf{c}^{\mathrm{target}}, t_x, t_z) - (\mathbf{x}^{C_\alpha} - [\mathbf{x}_0^{C_\alpha} + d\mathbf{1}]) \|^2 \right]$$

分阶段预训练流程为：先在AFDB单体上预训练流匹配模型，再在Teddymer/PDB混合数据上微调；对小分子靶点额外使用LoRA（Hu et al., 2022）避免PLINDER数据量小导致的过拟合。

#### 模块3：测试时优化器

推理阶段，Complexa将生成模型视为可操控的“生成先验”，集成多种测试时扩展算法：

- **最佳N采样（Best-of-N）**：生成N个样本，选取ipAE < 7.0者
- **波束搜索（Beam Search）**：维持N条去噪轨迹，每K步评估候选状态并保留奖励之和最高的N个，更新公式为：

$$\mathcal{B}_{t_x+\Delta t_x^K, t_z+\Delta t_z^K} = \underset{\mathcal{T} \subseteq \mathcal{C}, |\mathcal{T}| = N}{\arg\max} \sum_{i \in \mathcal{T}} R\big((\mathbf{x}_{t_x+\Delta t_x^K}^{C_\alpha}, \mathbf{z}_{t_z+\Delta t_z^K})_i\big)$$

- **费曼-卡茨转向（Feynman-Kac Steering, FKS）**：通过对奖励进行指数加权的重要性采样逼近倾斜分布，采样概率为：

$$p\big((\mathbf{x}_{t_x+\Delta t_x^K}^{C_\alpha}, \mathbf{z}_{t_z+\Delta t_z^K})_i\big) \propto \exp\{\beta R\big((\mathbf{x}_{t_x+\Delta t_x^K}^{C_\alpha}, \mathbf{z}_{t_z+\Delta t_z^K})_i\big)\}$$

其中 $\beta$ 为逆温度参数控制选择强度。

- **蒙特卡洛树搜索（MCTS）**：在状态树中平衡利用与探索，选择准则为：

$$i = \arg\max_i \frac{R(\ldots)}{V(\ldots)} + C \sqrt{\frac{\ln(V(\mathrm{parent}))}{V(\ldots)}}$$

奖励函数使用结构预测模型（AlphaFold2-Multimer或RosettaFold-3）的界面预测对齐误差（ipAE）或界面氢键能量；也可将两者组合使用。此外，Complexa还支持“生成+幻觉”（Generate & Hallucinate）混合策略：先用生成模型初始化结合剂候选，再通过BindCraft框架优化序列。

### 输入输出流与模块耦合

整个框架的数据流是单向且模块间松耦合的：VAE编码器与解码器在条件生成训练期间保持冻结，靶点条件仅注入流匹配模型；测试时优化器作为独立模块，以生成模型的中间状态为输入，以结构预测分数为反馈信号，通过修改采样路径来提升最终输出质量。这种设计使得生成先验与搜索优化可以灵活组合——简单靶点可直接采样，困难靶点则投入更多计算资源进行引导搜索。

### 部分潜在流匹配框架

Complexa 的核心生成框架建立在 La-Proteína（Geffner et al., 2026）的部分潜在流匹配（partially latent flow matching）之上。该方法在连续时间中同时演化两个耦合变量：残基的 Cα 坐标 $\mathbf{x}^{C_\alpha}$ 和每个残基的连续潜在变量 $\mathbf{z}$。潜在变量由预训练的自动编码器（VAE）从全原子结构中编码得到，负责捕获除骨架 Cα 轨迹外的全部结构细节（侧链构象、序列信息等）。

流匹配的核心机制是将简单先验分布（高斯噪声）通过常微分方程（ODE）逐步变换为数据分布。训练时，模型学习一个向量场 $\mathbf{v}^\phi$ 来近似真实的速度场，该速度场定义了从噪声到数据的概率路径。Complexa 采用整流流（rectified flow）的线性插值方案：

$$\mathbf{x}_t = t \mathbf{x}_1 + (1-t) \mathbf{x}_0$$

其中 $\mathbf{x}_1$ 为目标数据，$\mathbf{x}_0$ 为噪声。Cα 坐标和潜在变量使用独立的时间调度 $t_x$ 和 $t_z$，允许对两者的去噪过程进行精细控制。

### 带平移噪声的训练目标

Complexa 对 La-Proteína 的训练目标进行了关键修改，引入全局平移噪声以强制模型在生成过程中持续推理结合剂相对于靶点的空间定位。完整训练目标为：

$$
\begin{aligned}
\min_{\phi} \mathbb{E}_{t_x, t_z, (\mathbf{x}, \mathbf{c}^{\mathrm{target}}) \sim p^{\mathrm{data}}, \mathbf{x}_0^{C_\alpha} \sim p_0^{C_\alpha}, \mathbf{z}_0 \sim p_0^{z}, d \sim p_0^{d}} 
\bigg[ 
&\| \mathbf{v}_z^{\phi}(\mathbf{x}_{t_x}^{C_\alpha}, \mathbf{z}_{t_z}, \mathbf{c}^{\mathrm{target}}, t_x, t_z) - (\mathcal{E}(\mathbf{x}) - \mathbf{z}_0) \|^2 \\
+ &\|\mathbf{v}_x^{\phi}(\mathbf{x}_{t_x}^{C_\alpha}, \mathbf{z}_{t_z}, \mathbf{c}^{\mathrm{target}}, t_x, t_z) - (\mathbf{x}^{C_\alpha} - [\mathbf{x}_0^{C_\alpha} + d\mathbf{1}]) \|^2 
\bigg]
\end{aligned}
$$

**变量含义：**
- $\phi$：去噪网络（denoiser）的可学习参数
- $t_x, t_z$：Cα 坐标和潜在变量的独立时间步
- $\mathbf{x}$：完整的结合剂结构（含全原子坐标）
- $\mathbf{c}^{\mathrm{target}}$：靶点条件特征（Atom37 表示、氨基酸身份、热点标记）
- $\mathbf{x}_0^{C_\alpha} \sim p_0^{C_\alpha}$：Cα 坐标的先验噪声
- $\mathbf{z}_0 \sim p_0^{z}$：潜在变量的先验噪声
- $d \sim \mathcal{N}(0, c_d^2)$：标量全局平移噪声，$c_d = 0.2$ nm
- $\mathcal{E}(\mathbf{x})$：冻结的编码器将全原子结构映射到潜在空间
- $\mathbf{v}_z^{\phi}, \mathbf{v}_x^{\phi}$：模型预测的潜在变量和 Cα 坐标的速度场

**设计原理：** 第一项为潜在变量的流匹配损失，目标是将噪声 $\mathbf{z}_0$ 推向编码器输出 $\mathcal{E}(\mathbf{x})$。第二项为 Cα 坐标的流匹配损失，关键差异在于目标端添加了全局平移 $d\mathbf{1}$——这意味着模型不能简单地将 Cα 坐标去噪到绝对位置，而必须学习推断结合剂相对于靶点的正确空间关系。消融实验证实，移除该平移噪声会导致唯一成功结合剂数量显著下降（Table 6, Figure 13）。

### 潜在目标条件机制

Complexa 的条件生成架构（Figure 5）在不修改预训练 VAE 的前提下实现靶点条件化。具体实现：

1. **靶点表示：** 使用 Atom37 方案编码靶点的全原子结构，拼接氨基酸身份特征和二元热点标记（指示靶点上哪些残基允许与结合剂相互作用）。

2. **条件注入：** 将靶点特征与噪声化的结合剂表示（Cα 坐标 + 潜在变量）在序列维度拼接，输入基于成对偏置注意力（pairwise bias attention）的 Transformer 去噪网络。该网络同时处理结合剂内部相互作用和结合剂-靶点跨链相互作用。

3. **编码器/解码器冻结：** VAE 的编码器和解码器在条件训练阶段保持冻结，仅训练去噪网络。这确保了潜在空间的语义一致性，同时允许去噪网络学习靶点条件下的生成先验。

### 测试时优化：搜索算法核心公式

Complexa 在推理阶段将结构预测模型（AlphaFold2 或 RosettaFold-3）的评分作为奖励信号，引导生成过程。三种核心搜索策略的数学表述如下：

**波束搜索（Beam Search）更新准则：**

$$\mathcal{B}_{t_x+\Delta t_x^K, t_z+\Delta t_z^K} = \underset{\mathcal{T} \subseteq \mathcal{C}, |\mathcal{T}| = N}{\arg\max} \sum_{i \in \mathcal{T}} R\big((\mathbf{x}_{t_x+\Delta t_x^K}^{C_\alpha}, \mathbf{z}_{t_z+\Delta t_z^K})_i\big)$$

- $\mathcal{B}$：波束集合，包含 $N$ 个候选状态
- $\mathcal{C}$：从当前波束中每个状态扩展 $\dot{L}$ 个候选后形成的候选池，$|\mathcal{C}| = N \times \dot{L}$
- $\Delta t_x^K, \Delta t_z^K$：每 $K$ 步去噪后评估一次
- $R(\cdot)$：奖励函数（通常为 $f_{\mathrm{ipAE}}$ 的负值或界面氢键能量）
- 操作含义：从候选池中选择奖励之和最大的 $N$ 个状态作为新波束

**费曼-卡茨转向（Feynman-Kac Steering）采样概率：**

$$p\big((\mathbf{x}_{t_x+\Delta t_x^K}^{C_\alpha}, \mathbf{z}_{t_z+\Delta t_z^K})_i\big) \propto \exp\{\beta R\big((\mathbf{x}_{t_x+\Delta t_x^K}^{C_\alpha}, \mathbf{z}_{t_z+\Delta t_z^K})_i\big)\}$$

- $\beta$：逆温度参数，控制奖励对采样分布的影响强度
- 与波束搜索的确定性选择不同，FKS 通过重要性采样从倾斜分布中随机采样，在保持多样性的同时偏向高奖励区域

**蒙特卡洛树搜索（MCTS）选择准则：**

$$i = \arg\max_i \left[ \frac{R(\ldots)}{V(\ldots)} + C \sqrt{\frac{\ln(V(\mathrm{parent}))}{V(\ldots)}} \right]$$

- $V(\ldots)$：节点 $i$ 的访问次数
- $R(\ldots)/V(\ldots)$：平均奖励（利用项）
- $C$：探索常数，控制 UCB（上置信界）探索项的权重
- 该公式平衡了对已知高奖励路径的利用和对未充分探索路径的探索

### 分阶段训练策略

Complexa 采用三阶段训练流程以实现稳定的条件生成能力：

1. **阶段一（VAE 预训练）：** 在 AFDB 单体结构上训练自动编码器，随后在 PDB 结构上微调，确保潜在空间捕获蛋白质结构的基本特征。

2. **阶段二（流匹配预训练）：** 在编码后的 AFDB Foldseek 聚类代表单体上预训练去噪网络，建立无条件的蛋白质生成先验。

3. **阶段三（条件微调）：** 在 Teddymer 合成二聚体和 PDB 多聚体混合数据上微调，引入靶点条件机制和平移噪声。对于小分子靶点，额外使用 LoRA（低秩适配）在 PLINDER 数据集上微调，以避免小数据集导致的过拟合。

这种分阶段策略的核心优势在于：模型先在大量单体数据上学习通用的蛋白质结构生成能力，再通过相对较小的结合剂-靶点配对数据将这一能力转化为条件生成。消融实验表明，跳过 Teddymer 预训练或移除平移噪声均会导致性能崩溃（Table 6），验证了各模块的必要性。

## 实验与关键发现

### 核心实验设计

所有实验采用统一评估管道以保证公平比较：蛋白质靶点使用ProteinMPNN进行8次序列重新设计并选取最佳结果，小分子靶点使用LigandMPNN单次设计。成功标准严格统一——蛋白质靶点要求ipAE<7、complex pLDDT>0.9、binder scRMSD<1.5 Å；小分子靶点要求min ipAE<2、binder Cα scRMSD<2 Å、ligand scRMSD<5 Å。靶点按难度分类（基于固定样本预算基准），避免简单靶点造成幻觉方法的虚假优势。所有方法均在单个NVIDIA A100 GPU上以4小时为归一化计算预算进行对比。

### 主结果

#### 蛋白质靶点：生成性能断层式领先

在不使用任何推理时优化的情况下，Complexa的基础生成模型已在19个蛋白质靶点上展现出断层式领先（Table 2, Table 10）。以MPNN重新设计评估，Complexa平均产生14.4个唯一成功结合剂，而所有先前模型（RFDiffusion、Protopardelle、APM等）均显著低于此值，最优基线方法的成功数不足Complexa的60%。当使用模型自身生成的序列直接评估（不经ProteinMPNN重设计），Complexa仍平均产生约9.1个唯一成功结合剂，表明其联合生成序列与结构的能力远超仅生成骨架再依赖外部序列设计的方法。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_qmCpJtFZra/figures/007_Table_2.jpg]]
*Table 2: Complexa’s generative performance for protein targets without optimization vs. baselines. Self denotes model sequence evaluation, MPNN full backbone-based re-design, and MPNN-FI the same with fixed interface amino acids. Note that RFDiffusion and Protpardelle only generate backbones and not their own sequences. Complete results in Sec. I. If methods tie on unique and absolute successes, we do not count this, see Sec. F*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_qmCpJtFZra/figures/035_Table_10.jpg]]
*Table 10: De novo binder design performance for all protein targets. Unique successes for different models and three sequence redesign methods per target*

值得注意的是，Complexa的单次采样时间仅约15.6秒，远快于RFDiffusion和APM（Table 2），这为后续推理时搜索提供了计算效率基础。

#### 小分子靶点：成功数提升2-3倍

在4个小分子靶点（SAM、FAD、IAI、OQO）上，Complexa同样大幅超越RFDiffusion-AllAtom（Table 1, Table 11）。以自身序列评估，Complexa在IAI上产生19个、FAD上17个、OQO上6个、SAM上10个唯一成功结合剂。相比之下，RFDiffusion-AllAtom依赖LigandMPNN重新设计序列，在IAI上仅约6.47个成功结合剂，Complexa的平均成功数提升2-3倍。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_qmCpJtFZra/figures/008_Table_1.jpg]]
*Table 1: Complexa’s generative performance for small molecule targets without optimization. RFDiffusion-AllAtom uses LigandMPNN, we evaluate sequences produced by Complexa*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_qmCpJtFZra/figures/036_Table_11.jpg]]
*Table 11: De novo binder design performance of models for all small molecule targets. RFdiffusionAA only produces backbones and as a result can only be evaluated under full LigandMPNN re-design. We report the number of FoldSeek clusters out of the successful subset of 200 samples of length 100*

#### 推理时缩放：在困难靶点上超越纯幻觉方法一个数量级

在归一化GPU小时预算下，Complexa的测试时优化策略展现出显著优势。在12个简单靶点和7个困难靶点的聚合分析中（Figure 7, Figure 21, Figure 22），Complexa的最佳N采样、波束搜索、费曼-卡茨转向（FKS）和蒙特卡洛树搜索（MCTS）在固定计算资源下均大幅超越纯幻觉方法BindCraft和BoltzDesign。在困难靶点上，Complexa的成功率至少高出纯幻觉方法一个数量级。

以VEGFA多链靶点为例（Figure 8），Complexa的波束搜索和MCTS在推理时计算扩展中持续产生更多唯一成功结合剂，而BindCraft和BoltzDesign在相同预算下几乎无法产生有效设计。在极难靶点（TNF-α、H1、IL17A）上（Figure 19），虽然仍需要极高的GPU小时预算（数百甚至上千小时），但Complexa的搜索方法仍是唯一能持续产出成功结合剂的方案。

#### 小分子靶点的推理时优化

在小分子靶点上（Figure 9, Figure 23），Complexa的推理时缩放方法同样远优于仅使用BoltzDesign进行梯度优化的方案。然而，当前使用的奖励函数（基于min ipAE）不能完全捕捉配体RMSD的失败模式，可能导致优化偏向不理想结构，这是该方法在小分子场景下的已知局限。

#### 酶设计基准：41个任务中38个获胜

在AME酶设计基准的41个催化位置重构任务中（Figure 10, Figure 25, Table 12），Complexa在38个任务上的唯一成功数优于RFDiffusion2。更关键的是，在自生成序列模式下（不经ProteinMPNN重设计），Complexa实现了41/41任务全部成功，而RFDiffusion2的自生成序列无法直接产生全原子结构，其最佳唯一成功任务仅30/41。指标翻倍以上的优势表明，Complexa的联合序列-结构生成能力在需要精确原子排布的任务中具有本质优势。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_qmCpJtFZra/figures/043_Table_12.jpg]]
*Table 12: Enzyme Design Benchmark—Detailed Quantitative Results. “All” indicates total number of successes produced by the model (we produce 100 samples per task), while “Unique” indicates number of unique successes, obtained by clustering all successes. The method with the most unique successes for 8 sequence re-designs (LigandMPNN(8)) is highlighted in blue and for single sequence methods is highlighted in red*

### 消融研究

#### Teddymer数据集：决定性贡献

Teddymer合成二聚体数据集是Complexa性能的核心支柱。移除Teddymer后（Table 6, Table 7, Figure 13），MPNN评估的平均唯一成功数从14.4骤降至3.84，自身序列评估更是从9.10暴跌至0.15，且在全部19个靶点上无一次胜出。使用Boltz-2（Figure 14, Table 8）和RosettaFold-3（Figure 15, Table 9）进行替代评估也确认了这一结论——缺失Teddymer导致性能全面崩溃。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_qmCpJtFZra/figures/021_Table_6.jpg]]
*Table 6: Translation noise and Teddymer ablation studies. average unique successes and the number of times each method ranks best across 19 targets. Results are shown for Complexa, and variants without Teddymer data and without translation noise*

Teddymer的关键在于其与真实多聚体界面具有分布重叠（Figure 3），提供了大规模、多样化的界面互作模式，使模型能学习到可泛化的结合几何先验。

#### 翻译噪声：空间定位能力的关键

去除训练时的全局翻译噪声同样显著降低性能（Table 6, Figure 13），但下降幅度小于缺失Teddymer。这一结果验证了核心设计假设：在训练目标中向结合剂Cα坐标添加标量随机全局平移d~N(0,0.2²)，迫使模型在生成过程中持续推理结合剂相对于靶点的正确空间位置，是获得可靠空间定位能力的关键机制。

#### 生成+幻觉混合策略

将Complexa生成的结构骨架与BindCraft序列优化结合（Generate & Hallucinate）在简单靶点上优于纯BindCraft（Figure 16, Figure 17），但在困难靶点上仍不及内置搜索算法（波束搜索、MCTS）（Figure 18）。这表明生成先验提供了良好的初始化，但对于困难靶点，需要在生成过程中就进行引导，而非仅在生成后优化序列。

### 奖励函数与优化策略分析

波束搜索结合不同奖励函数的实验（Table 3）揭示了折叠评分（f_ipAE）与氢键能量（f_H-Bond）的互补性。单独使用折叠评分已能有效引导搜索，而加入界面氢键能量奖励可进一步产生具有更广泛互作界面的结合剂（Figure 11），但可能以牺牲唯一成功数为代价（Figure 24）。界面氢键数量与ipAE之间存在负相关（Figure 28），表明更强的极性互作倾向于伴随更低的预测对齐误差，但这一关系并非单调，需要在优化中权衡。

### 失败模式与局限

1. **计算指标与实验活性的鸿沟**：所有成功评估均基于计算指标（ipAE、pLDDT、RMSD），尚未经湿实验验证。这些指标与真实结合活性的关联存在不确定性，是当前计算设计的根本局限。

2. **小分子优化的奖励失配**：推理时优化在小分子靶点上使用的奖励函数（min ipAE）不能完全捕捉配体RMSD的失败模式，可能导致优化偏向不理想结构。

3. **极难靶点的计算成本**：对TNF-α、H1等极难靶点，仍需要极高的GPU小时预算（数百甚至上千小时）才能获得足够数量的唯一结合剂，限制了大规模靶点库筛选的可行性。

4. **模态覆盖范围**：当前框架仅针对蛋白质和小分子靶点进行演示，尚未扩展到DNA、RNA或抗体等其他分子模态。

5. **Teddymer的构建局限**：Teddymer数据集虽与真实多聚体接口具有分布重叠，但基于预测结构（AFDB）构建，可能缺少某些生物物理约束和翻译后修饰信息。

## 定位与知识库关联

### 1. 方法谱系：从扩散生成与幻觉优化到统一框架

Complexa 的提出直接回应了蛋白质结合剂设计中一个长期存在的范式割裂：**生成式建模**与**幻觉优化**被视为两条互不相交的技术路线。

**生成式路线**以 **RFDiffusion**（Watson et al., Nature 2023）为里程碑式代表。该方法采用条件扩散模型生成蛋白质骨架，随后依赖 **ProteinMPNN** 进行序列设计。其后续扩展 **RFDiffusion-AllAtom**（Krishna et al., 2024）将适用范围推广至小分子靶点，但同样遵循“骨架生成→序列填充”的解耦范式。另一类全原子生成模型如 **Protopardelle**（Chu et al., 2024; Lu et al., 2025）和 **APM**（Chen et al., 2025）尝试同时生成序列与结构，但其生成能力受限于训练数据规模和模型架构。

**幻觉路线**则以 **BindCraft**（Pacesa et al., 2025）和 **BoltzDesign**（Cho et al., 2025）为代表。这类方法将结构预测模型（如 AlphaFold2、Boltz-1）作为可微分的“评分器”，通过梯度优化在序列空间中搜索高置信度结合剂。**AlphaDesign**（Jendrusch et al., 2025）则用遗传算法替代梯度优化。幻觉方法的根本瓶颈在于：它们从随机序列出发，缺乏关于蛋白质结构空间的生成先验，导致搜索效率极低——尤其在困难靶点上，大量计算资源被浪费在无效的序列空间探索中。

Complexa 的核心贡献在于**打破这一错误二分法**。它构建在 **La-Proteína**（Geffner et al., 2026）的流匹配框架之上，但做出了五项关键改造，将纯粹的生成模型转化为一个**生成先验驱动的推理时搜索平台**：

| 改造维度 | La-Proteína 原始方案 | Complexa 方案 | 证据锚点 |
|---------|---------------------|--------------|---------|
| **目标条件机制** | 仅支持单体生成，无靶点条件 | 引入潜在目标条件：将靶点表示为 Atom37 特征、氨基酸身份与热点标记，与噪声化结合剂表示拼接后通过 Transformer 处理 | Sec. 3.2, Figure 5 |
| **全局翻译噪声** | 训练时无需推理全局定位 | 在训练目标中对 Cα 坐标添加标量随机全局平移 $d \sim \mathcal{N}(0, 0.2^2)$，迫使模型持续推理结合剂相对于靶点的空间位置 | Eq. (1), Sec. 3.2 |
| **训练数据构成** | 仅使用 AFDB 和 PDB 单体/多聚体 | 构建 **Teddymer** 大规模合成二聚体数据集（从 AFDB 结构域互作中提取），与 PDB 多聚体混合训练 | Sec. 3.1, Sec. D |
| **分阶段预训练** | 单阶段训练 | 三阶段流程：AFDB 单体预训练 VAE 和流匹配模型 → Teddymer/PDB 混合数据微调；小分子靶点额外使用 LoRA 避免过拟合 | Sec. 3.2, Sec. G.3.1 |
| **推理时优化** | 无测试时优化，仅直接采样 | 集成最佳-N、波束搜索、费曼-卡茨转向、蒙特卡洛树搜索及“生成+幻觉”混合策略，利用结构预测分数作为奖励引导采样 | Sec. 3.4, Sec. H |

这五项改造形成了一个完整的技术闭环：Teddymer 数据集和分阶段预训练赋予了模型强大的生成先验；翻译噪声和目标条件机制使模型具备空间推理能力；推理时搜索算法则将这一先验转化为超越纯生成与纯幻觉方法的性能。

### 2. 适用边界与关键约束

尽管 Complexa 在计算机评估指标上展现出断层式优势，其适用性受限于以下边界条件：

**模态覆盖范围**：当前框架仅针对蛋白质靶点和小分子靶点进行了演示与验证。对于 DNA、RNA、抗体等其他分子模态，Complexa 的潜在目标条件机制在原理上可扩展，但尚未经过实验验证——这需要额外的训练数据和可能的架构调整。

**评估指标与实验真实性的鸿沟**：所有成功判定均基于计算指标——蛋白质靶点要求 $\text{ipAE} < 7$、$\text{complex pLDDT} > 0.9$、$\text{binder scRMSD} < 1.5$ Å；小分子靶点要求 $\text{min ipAE} < 2$、$\text{binder Cα scRMSD} < 2$ Å、$\text{ligand scRMSD} < 5$ Å。这些指标与真实结合亲和力之间的关联存在不确定性，目前尚无湿实验验证数据支撑。

**小分子优化的奖励函数缺陷**：推理时优化在小分子靶点上使用的奖励函数基于 $\text{min ipAE}$，但该指标无法完全捕捉配体 RMSD 的失败模式，可能导致优化偏向不理想的结构（见 Table 13 中结合亲和力对比的局限性讨论）。

**极难靶点的计算成本**：对 TNF-α、H1、IL17A 等极难靶点，即使使用最优搜索策略，仍需数百甚至上千 GPU 小时才能获得足够数量的唯一结合剂（Figure 19）。这限制了该框架在大规模靶点库筛选中的直接应用。

**Teddymer 数据集的固有偏差**：尽管 Teddymer 与真实多聚体接口具有分布重叠（Figure 3），但其构建基于 AFDB 预测结构，可能缺少某些生物物理约束——如翻译后修饰、界面动力学特征和溶剂效应——这些在真实结合界面中至关重要。

### 3. 局限性与开放问题

**核心局限**：

1. **湿实验验证缺失**：所有性能声明均基于计算指标，尚未经体外或体内实验确认。生成式模型在计算机指标上的优势能否转化为实验成功率，是该方法面临的最大不确定性。

2. **奖励函数的单一性**：当前推理时优化主要依赖结构预测模型的界面置信度（$\text{ipAE}$）和氢键能量（$f_{\text{H-Bond}}$）。更可靠的结合亲和力预测器或其他生物物理属性（如疏水性互补、静电势匹配）尚未被纳入奖励函数。

3. **计算成本与多样性的权衡**：波束搜索和 MCTS 在提升成功率的同时，可能降低生成样本的多样性——这是所有基于奖励的搜索方法的通病，但本文未对此进行系统量化。

4. **序列设计的解耦评估**：主要结果依赖 ProteinMPNN 的 8 次序列重设计（MPNN 模式），而模型自身生成的序列（Self 模式）性能显著较低（Table 2, Table 6）。这表明 Complexa 的序列生成能力仍有提升空间。

**开放问题**：

1. **多模态靶点的统一条件生成**：能否将 Complexa 扩展为统一框架，灵活处理 DNA、RNA、小分子、抗体等多种靶点模态？这需要在训练数据和条件机制上做出系统性设计。

2. **奖励函数的生物物理深化**：如何融入更可靠的结合亲和力预测（如基于自由能微扰的计算）或其他生物物理属性，以引导生成更可能具备实验活性的分子？

3. **闭环实验验证管道**：所生成的大量设计如何高效地通过湿实验筛选？能否构建“生成→实验验证→反馈→再生成”的闭环管道，使模型从实验数据中持续学习？

4. **推理时搜索的效率优化**：在保证生成多样性的前提下，能否进一步降低推理时搜索的计算成本？例如，通过学习搜索策略或蒸馏搜索过程，使其适用于更大规模的靶点库筛选。

5. **Teddymer 数据集的增强方向**：引入翻译后修饰、界面动力学特征或多构象采样，能否进一步提升模型对真实结合界面的泛化能力？

## 原文 PDF

![[paperPDFs/ICLR_2026/Scaling_Atomistic_Protein_Binder_Design_with_Generative_Pretraining_and_Test_Time_Compute.pdf]]
