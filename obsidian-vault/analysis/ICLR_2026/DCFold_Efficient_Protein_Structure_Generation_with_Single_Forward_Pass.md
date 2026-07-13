---
title: "DCFold: Efficient Protein Structure Generation with Single Forward Pass"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DCFold_Efficient_Protein_Structure_Generation_with_Single_Forward_Pass.pdf
project_link: null
code_link: null
openreview_forum_id: LMsdys7t1L
aliases:
- DCFold
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "双重一致性训练（扩散一致性与Pairformer一致性）结合时间测地线匹配（TGM）调度器，同时消除扩散和循环的迭代开销。"
primary_logic: "通过将一致性学习应用于扩散模块和Pairformer，并利用基于Fisher信息的测地线调度来稳定变长序列的训练，DCFold实现了单步生成且精度不降。"
claims:
- "DCFold在Posebusters V2上取得了与AlphaFold3相当的精度，同时推理速度提升15倍。"
- "TGM调度器通过配对时间步的测地线距离稳定训练，在结构预测中显著优于传统一致性模型。"
- "双重一致性训练有效收紧输出分布，改善了最差情况下的RMSD，提高了预测可靠性。"
- "DCFold在binder设计任务中展现出更高的成功率，验证了其在下游应用中的实用性。"
---

# DCFold: Efficient Protein Structure Generation with Single Forward Pass

> [!tip] 核心洞察
> 通过将一致性学习应用于扩散模块和Pairformer，并利用基于Fisher信息的测地线调度来稳定变长序列的训练，DCFold实现了单步生成且精度不降。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DCFold：单步正向高效生成蛋白质结构 |
| 英文题名 | DCFold: Efficient Protein Structure Generation with Single Forward Pass |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=LMsdys7t1L) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DCFold |
| Dataset | Posebusters V2, Recent PDB (Monomer) |

> [!tip] 效果简介
> - Posebusters V2 上，Best RMSD <1Å (%) 为 58.10，对比 67.14 (AlphaFold3)，变化 -9.04。
> - Posebusters V2 上，Best RMSD <5Å (%) 为 94.29，对比 93.81 (AlphaFold3)，变化 +0.48。
> - Posebusters V2 上，Worst RMSD <2Å (%) 为 71.43，对比 70.00 (AlphaFold3)，变化 +1.43。

## 概要

### 问题瓶颈

AlphaFold3（Abramson et al., 2024）在蛋白质结构预测中取得了高精度，但其推理效率受限于两个迭代过程：扩散模块需要约200步去噪采样，Pairformer模块默认执行4次循环。这种迭代架构导致单次推理耗时较长（短序列约93秒），严重制约了在高通量虚拟筛选、大规模蛋白质组学注释等场景中的应用。

### 核心方法

DCFold提出**双重一致性训练**（Dual Consistency）框架，将一致性学习同时应用于扩散模块和Pairformer模块，将多步迭代压缩为单步：

- **扩散一致性**：通过最小化扩散模块在不同时间步输出之间的MSE，使模型学会从噪声直接映射到干净结构，实现单步去噪。
- **Pairformer一致性**：通过最小化连续循环中pair和single表示之间的MSE，使Pairformer仅需1次循环即可达到多循环的精度。

为稳定变长序列的一致性训练，DCFold引入**时间测地线匹配**（Temporal Geodesic Matching, TGM）调度器。TGM基于时间Fisher信息定义扩散时间流形上的黎曼度量，按测地线距离配对训练时间步，替代传统一致性模型采用的固定欧氏间隔策略。理论分析表明，该测地线距离在局部与KL散度的平方根等价，为配对策略提供了信息几何基础。

### 核心结论

在Posebusters V2和Recent PDB基准上，DCFold以单步生成实现了与AlphaFold3相当的精度：

- **精度保持**：最佳RMSD<5Å达94.29%（AlphaFold3为93.81%），最差RMSD<2Å达71.43%（AlphaFold3为70.00%），TM-score在单体上达0.850。
- **推理加速**：短序列（≤255 tokens）推理时间从92.63秒降至3.76秒，加速约24倍；长序列仍保持7.7倍以上加速。
- **下游验证**：在binder设计任务中，DCFold在六个靶点上的平均成功率（物理约束/模型约束：0.29/0.78）优于BindCraft基线（0.26/0.69），验证了单步模型在生成式蛋白质设计中的实用性。

### 方法定位

DCFold属于基于蒸馏的一致性模型方法，需依赖预训练的AlphaFold3作为教师模型。其在方法谱系中的定位如下：

- **相对于AlphaFold3**：将扩散采样步数从~200步压缩为1步，Pairformer循环从4次压缩为1次，同时修改采样器（关闭噪声注入、固定缩放因子）以稳定单步采样。
- **相对于一致性模型基线**（CD、sCM、ECM）：TGM调度器在Posebusters V2上达到77.5%成功率，显著优于其他调度策略，且训练梯度更稳定。
- **相对于BindCraft**：在binder幻觉设计中展现出更高的计算效率（平均GPU时间105秒 vs 138秒）和更优的设计成功率。

### 主要局限

1. DCFold需要基于AlphaFold3进行蒸馏，无法从头训练。
2. 对于长序列，Pairformer的计算占比上升，加速比有所下降。
3. 双重一致性训练轻微降低了结构多样性，需通过其他策略补偿。
4. 目前仅在蛋白质和蛋白-配体复合物上验证，尚未推广到核酸等其他生物分子。



蛋白质结构预测是计算生物学中的核心问题，其目标是从氨基酸序列出发，确定蛋白质在三维空间中的折叠构象。近年来，以 **AlphaFold3**（Abramson et al., 2024）为代表的深度学习模型在该领域取得了突破性进展，不仅能够高精度预测蛋白质单体结构，还支持蛋白质-配体复合物、蛋白质-蛋白质相互作用等多种生物分子体系的建模。

然而，AlphaFold3 的推理效率成为其在高通量应用场景中的关键瓶颈。这一瓶颈根源于其架构中的两个迭代过程：

1. **扩散模块的迭代采样**：AlphaFold3 采用基于扩散的生成框架，需要约 200 步去噪采样才能从噪声分布逐步收敛到干净的结构输出，每一步都涉及完整的前向传播计算。
2. **Pairformer 的循环精炼**：AlphaFold3 默认使用 4 次 Pairformer 循环来迭代更新蛋白质内部表示（pair 和 single 表示），每次循环均需重新计算 16 层 Transformer 块。

这两个迭代过程的叠加导致单次结构预测的推理时间达到数十秒甚至上百秒的量级，严重限制了 AlphaFold3 在大规模虚拟筛选、蛋白质组学注释以及需要大量采样的蛋白质设计（如 binder 设计）等任务中的应用。直接减少采样步数或循环次数（如 AF3 ODE 的单步采样）会导致预测精度显著下降，表明简单的步数压缩无法在精度与效率之间取得平衡。

针对上述效率瓶颈，本文提出 **DCFold**，一个单步生成的蛋白质结构预测模型。其核心动机在于：**能否通过训练策略的革新，将 AlphaFold3 的多步迭代推理过程压缩为单步前向传播，同时保持预测精度不降？** 为实现这一目标，DCFold 引入了双重一致性训练（Dual Consistency）框架，联合解决扩散迭代和 Pairformer 循环两个效率瓶颈，并结合时间测地线匹配（Temporal Geodesic Matching, TGM）调度器来稳定变长序列的训练过程。最终，DCFold 在 Posebusters V2 等基准上实现了与 AlphaFold3 相当的精度，并将推理速度提升约 15 倍。



## 核心方法与创新机理

DCFold 的核心创新在于通过**双重一致性训练**（Dual Consistency）框架，将 AlphaFold3 的迭代式扩散过程和循环式 Pairformer 同时压缩为单步执行，并引入**时间测地线匹配**（TGM）调度器来稳定变长序列的训练。这一设计直接回应了 AlphaFold3 推理效率的核心瓶颈：扩散模块约 200 步采样与 Pairformer 4 次循环带来的高计算成本。

### 关键创新点

| 创新维度 | AlphaFold3 基线 | DCFold 方案 | 机制与效果 |
|:---|:---|:---|:---|
| **扩散采样步数** | ~200 步 | 1 步 | 扩散一致性损失将多步去噪压缩为单步概率流 ODE 积分 |
| **Pairformer 循环次数** | 4 次 | 1 次 | Pairformer 一致性损失强制连续循环的 pair/single 表示趋于一致 |
| **采样器噪声注入** | 开启（γ₀ > 0） | 关闭（γ₀ = 0） | 消除随机性扰动，配合固定缩放因子 λ=1 和归一化步长 η=1，稳定单步采样 |
| **训练损失** | 仅置信度损失 | 扩散一致性 + Pairformer 一致性 + 置信度 | 两阶段训练：阶段一训练扩散模块（L_diffusion + L_confidence），阶段二训练 Pairformer（L_pairformer + L_confidence） |
| **一致性调度器** | 标准 CM（固定欧氏间隔）或 ECM | TGM（基于时间 Fisher 信息的测地线距离） | TGM 将时间步配对建立在信息流形的测地线距离上，训练梯度更稳定 |

### 双重一致性机制

双重一致性的核心洞察是：AlphaFold3 的输出质量依赖于扩散模块的多步精炼和 Pairformer 的循环迭代，但两者本质上都在逼近同一个目标分布。通过一致性学习，模型被训练为在任意中间状态直接预测最终结果，从而将多步过程折叠为单步。

- **扩散一致性损失**（式 2）最小化扩散模块在时间步 $t$ 和参考时间步 $r$ 输出的 MSE：
  $$\mathcal{L}_{\mathrm{diffusion}} = \mathbb{E}_{\boldsymbol{x}, t, \boldsymbol{r}, \epsilon} \left[ w(t) \mathbf{MSE} \left( f_{\theta}(\boldsymbol{x}_t, t) - f_{\mathrm{sg}(\theta)}(\boldsymbol{x}_r, \boldsymbol{r}) \right) \right]$$

- **Pairformer 一致性损失**（式 3）最小化连续循环 $i$ 和 $i+1$ 的 pair 表示 $z$ 和 single 表示 $s$ 的 MSE：
  $$\mathcal{L}_{\mathrm{pairformer}} = \sum_{i=1}^{N-1} \left( \mathbf{MSE}(z_i, z_{i+1}) + \mathbf{MSE}(s_i, s_{i+1}) \right)$$

消融实验证实两个组件均有益：扩散一致性提升了单步采样性能，Pairformer 一致性在此基础上进一步提高了精度（见 Figure 3 的 lDDT 提升）。双重一致性还重塑了输出分布，显著改善了最差情况 RMSD——在 Posebusters V2 上，DCFold 的 Worst RMSD < 2Å 达到 71.43%，高于 AlphaFold3 的 70.00%（Table 2）。

### TGM 调度器的关键作用

传统一致性模型（CD、sCM）在蛋白质结构预测中表现不佳，甚至损害性能。ECM 虽有改进，但训练动态呈现阶梯状模式，梯度方差大（Figure 5）。TGM 通过以下设计解决了这一问题：

1. **时间 Fisher 信息作为黎曼度量**：定义 $g(t) := \mathcal{I}(t) = \mathbb{E}_{p_t(x)} \left[ \left( \frac{\partial}{\partial t} \log p_t(x) \right)^2 \right]$，将扩散时间轴视为信息流形。
2. **测地线距离配对**：选择训练对 $(t, r)$ 使得 $d_g(t, r) = \int_r^t \sqrt{\mathcal{I}(\tau)} d\tau = C(u)$，其中 $C(u)$ 随训练进度 $u$ 单调递减。
3. **局部度量-KL 等价性**（命题 1）：$d_g(t, r) = \sqrt{2} D_{\mathrm{KL}}(p_r(x) \| p_t(x))^{\frac{1}{2}} + \mathcal{O}((\Delta t)^3)$，确保配对时间步的信息距离可控。

TGM 在 Posebusters V2 上达到 77.5% 成功率，显著优于 ECM（75.7%）和 CD/sCM（Table 6），且训练梯度始终保持平衡，有效抵消了变长序列引入的不利影响。

### 与基线方法的差异定位

- **vs. AF3 ODE**（单步采样 + 单次循环的 AlphaFold3，未重新训练）：DCFold 通过双重一致性蒸馏重新训练，在 Recent PDB 单体 TM-score 上领先 0.020，蛋白-蛋白复合物成功率领先 5.2 个百分点（Table 3）。
- **vs. AF3 TGM**（仅应用 TGM 扩散一致性蒸馏）：DCFold 额外加入 Pairformer 一致性，进一步压缩了循环开销。
- **vs. Protenix-Mini**（轻量级 AlphaFold3 重实现，135M 参数，2 步 ODE）：DCFold 在更少步数下取得更高精度。
- **vs. BindCraft**（binder 幻觉设计基线）：DCFold 在六个靶点上平均 in silico 成功率更高（物理约束 0.29 vs. 0.26，模型约束 0.78 vs. 0.69，Table 5）。

### 限制说明

双重一致性训练依赖预训练的 AlphaFold3 进行蒸馏，无法从头训练。此外，对于长序列（>255 tokens），Pairformer 的计算占比上升，加速比从 24× 降至约 7.7×（Table 7）。双重一致性训练也轻微降低了结构多样性（Table 4），但可通过其他策略补偿。



![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Dual Consistency framework (top: AlphaFold3; bottom: DCFold)*

DCFold 的整体架构建立在对 AlphaFold3 的**双重一致性蒸馏**之上，其核心目标是将 AlphaFold3 的迭代式推理流程压缩为单步前向生成，同时保持预测精度。图 2 对比了 AlphaFold3 与 DCFold 的架构差异：AlphaFold3 需要多步扩散去噪（约 200 步）和多次 Pairformer 循环（默认 4 次），而 DCFold 将两者均压缩为单次执行。

### 输入输出流

DCFold 的输入输出规范与 AlphaFold3 保持一致：输入包括蛋白质序列、配体 SMILES、MSA 和模板等特征，输出为三维原子坐标以及 pLDDT、PAE 等置信度度量。关键差异在于推理流程的简化——输入经单次 Pairformer 循环处理后，由扩散模块在单步内将噪声样本直接映射为干净结构。

### 模块组成与关系

DCFold 的 pipeline 由以下核心模块串联构成：

1. **Pairformer（16 blocks, 1 cycle）**：处理蛋白质内部表示，仅执行单次循环。通过 Pairformer 一致性损失（公式 3）约束连续循环的 pair 表示 $z_i$ 和 single 表示 $s_i$ 趋于一致，从而消除多次循环的必要性。

2. **Diffusion Module（one-step）**：接收 Pairformer 输出和噪声样本，在单步内完成去噪。扩散一致性损失（公式 2）强制模型在不同时间步 $t$ 和参考时间步 $r$ 上输出一致，使多步采样压缩为单步成为可能。

3. **TGM Scheduler**：在训练阶段负责选择时间步对 $(t, r)$。不同于传统一致性模型使用固定欧氏间隔，TGM 基于时间信息流形上的测地线距离 $d_g(t, r) = \int_r^t \sqrt{\mathcal{I}(\tau)} d\tau$ 进行配对（公式 5），其中 $\mathcal{I}(t)$ 为时间 Fisher 信息（公式 4），用作黎曼度量张量。TGM 通过保持训练对之间的测地线距离恒定（随训练进度 $u$ 单调递减），稳定了变长序列下的训练梯度。

4. **Confidence Head**：输出 pLDDT、PDE、resolved 和 PAE 等置信度度量，其损失函数 $\mathcal{L}_{\mathrm{confidence}}$ 继承自 AlphaFold3。

5. **ODE Sampler（modified）**：单步概率流 ODE 积分器，通过关闭噪声注入（$\gamma_0 = 0$）、固定缩放因子（$\lambda = 1$）和归一化步长（$\eta = 1$）实现稳定单步采样。

### 训练流程

训练分为两个阶段（Table 1 给出了各损失项的权重）：

- **阶段一**：训练单步采样器。仅更新 Diffusion Module，优化目标为 $\mathcal{L}_{\mathrm{confidence}} + \mathcal{L}_{\mathrm{diffusion}}$。此阶段使扩散模块具备单步去噪能力。
- **阶段二**：施加 Pairformer 一致性。仅更新 16-block Pairformer，优化目标为 $\mathcal{L}_{\mathrm{confidence}} + \mathcal{L}_{\mathrm{pairformer}}$。此阶段使 Pairformer 的单次循环输出逼近多次循环的结果。

两个阶段均使用 TGM 调度器选择训练时间对，以稳定梯度并平衡不同长度序列的学习难度（TGM 将数据维度 $D$ 纳入调度以应对变长序列的挑战）。



### 双重一致性训练框架

DCFold的核心架构建立在双重一致性（Dual Consistency）训练框架之上，该框架将一致性学习同时应用于扩散模块和Pairformer模块，从而将多步迭代过程压缩为单步前向传播。训练分为两个阶段（Table 1）：

**第一阶段：单步采样器训练。** 仅更新扩散模块，训练目标由置信度损失 $\mathcal{L}_{\mathrm{confidence}}$ 和扩散一致性损失 $\mathcal{L}_{\mathrm{diffusion}}$ 组成。同时修改采样器以稳定单步采样：关闭噪声注入（设噪声因子 $\gamma_0 = 0$）、固定缩放因子 $\lambda = 1$、归一化步长 $\eta = 1$。

**第二阶段：Pairformer一致性训练。** 仅更新16-block的Pairformer，训练目标由 $\mathcal{L}_{\mathrm{confidence}}$ 和 $\mathcal{L}_{\mathrm{pairformer}}$ 组成。此阶段将Pairformer的循环次数从默认的4次压缩为1次。

### 扩散一致性损失

扩散一致性损失强制扩散模块在不同时间步上输出一致的结构预测，从而将多步去噪压缩为单步。其形式为：

$$\mathcal{L}_{\mathrm{diffusion}} = \mathbb{E}_{\boldsymbol{x}, t, \boldsymbol{r}, \epsilon} \left[ w(t) \mathbf{MSE} \left( f_{\theta}(\boldsymbol{x}_t, t) - f_{\mathrm{sg}(\theta)}(\boldsymbol{x}_r, \boldsymbol{r}) \right) \right]$$

其中 $f_{\theta}$ 为扩散模块，$\boldsymbol{x}_t$ 和 $\boldsymbol{x}_r$ 分别为时间步 $t$ 和参考时间步 $r$ 的噪声样本，$\mathrm{sg}(\cdot)$ 表示停止梯度操作，$w(t)$ 为权重函数（实验中发现其影响可忽略，设为1）。

### Pairformer一致性损失

Pairformer一致性损失最小化连续循环之间pair表示 $z_i$ 和single表示 $s_i$ 的均方误差，迫使单次循环的输出逼近多次循环的结果：

$$\mathcal{L}_{\mathrm{pairformer}} = \sum_{i=1}^{N-1} \left( \mathbf{MSE}(z_i, z_{i+1}) + \mathbf{MSE}(s_i, s_{i+1}) \right)$$

其中 $N=4$ 为AlphaFold3默认的循环次数，$z_i$ 和 $s_i$ 分别为第 $i$ 次循环后的pair表示和single表示。

### 置信度损失

置信度损失继承自AlphaFold3的置信度头，用于预测pLDDT、PAE等质量度量：

$$\mathcal{L}_{\mathrm{confidence}} = \mathcal{L}_{\mathrm{plddt}} + \mathcal{L}_{\mathrm{pde}} + \mathcal{L}_{\mathrm{resolved}} + \alpha_{\mathrm{pae}} \cdot \mathcal{L}_{\mathrm{pae}}$$

### TGM调度器：时间测地线匹配

TGM（Temporal Geodesic Matching）是DCFold的关键创新，解决了变长序列训练中一致性模型不稳定的问题。其核心思想是在时间信息流形上按测地线距离配对训练时间步。

**时间Fisher信息**定义为扩散时间流形上的黎曼度量张量：

$$g(t) := \mathcal{I}(t) = \mathbb{E}_{p_t(x)} \left[ \left( \frac{\partial}{\partial t} \log p_t(x) \right)^2 \right]$$

**测地线距离**为两点间沿该度量的积分：

$$d_g(t, r) = \int_r^t \sqrt{\mathcal{I}(\tau)} d\tau$$

TGM的核心机制是：每个时间步 $t$ 与参考点 $r$ 配对，使得 $d_g(t, r) = C(u)$，其中 $C(u)$ 是随训练进度 $u$ 单调递减的函数。这一设计确保网络的学习难度始终与其当前能力保持固定距离，有效抵消了变长序列引入的不利影响。

**局部度量-KL等价性**（Proposition 1）表明，对于小时间步，测地线距离与KL散度的平方根成正比：

$$d_g(t, r) = \sqrt{2} D_{\mathrm{KL}}(p_r(x) \| p_t(x))^{\frac{1}{2}} + \mathcal{O}((\Delta t)^3)$$

在EDM框架下，TGM使用简化的Fisher信息形式：

$$\mathcal{I}(t) = \frac{2D \cdot p \left( s_{\mathrm{max}}^{1/p} - s_{\mathrm{min}}^{1/p} \right)}{s_{\mathrm{max}}^{1/p} + (1-t) \left( s_{\mathrm{min}}^{1/p} - s_{\mathrm{max}}^{1/p} \right)}$$

其中 $D$ 为数据维度，被纳入训练调度以平衡不同长度序列的学习难度差异。

### 关键消融证据

- **双重一致性的两个组件均有增益**：扩散一致性提升单步采样性能，Pairformer一致性进一步提高精度（Figure 3 lDDT改善）。
- **TGM调度器显著优于基线**：在Posebusters V2上，TGM成功率达77.5%，优于ECM（75.7%）、sCM和CD（Table 6）。且TGM的训练梯度保持平衡，而ECM呈现阶梯状不稳定模式（Figure 5）。
- **采样器修改是单步稳定性的必要条件**：关闭噪声注入和固定缩放因子使单步ODE积分成为可能。



## 实验与关键发现

### 核心性能：Posebusters V2 基准

DCFold 在 Posebusters V2 蛋白质-配体复合物结构预测基准上与 AlphaFold3 进行了系统对比。核心发现是：**DCFold 以单步扩散和单次 Pairformer 循环，在关键指标上达到或超越了全配置 AlphaFold3 的性能**（Table 2）。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/004_Table_2.jpg]]
*Table 2: Posebusters V2 RMSD benchmark results. We report the percentage of predictions with RMSD below different thresholds*

具体而言，在最佳 RMSD < 5Å 的比例上，DCFold 达到 94.29%，略高于 AlphaFold3 的 93.81%。更值得注意的是最差情况 RMSD 的改善：DCFold 在最差 RMSD < 2Å 的比例为 71.43%（AlphaFold3 为 70.00%），在最差 RMSD < 3Å 的比例为 80.00%（AlphaFold3 为 78.10%）。这一提升直接验证了双重一致性训练"收紧输出分布"的核心设计意图——DCFold 并非简单追求最佳情况精度，而是通过强制扩散模块和 Pairformer 在不同时间步/循环间输出一致，有效抑制了极端偏差样本的产生。

然而，DCFold 在最佳 RMSD < 1Å 的指标上为 58.10%，落后于 AlphaFold3 的 67.14%，表明在追求极致原子级精度时，单步采样仍存在一定信息损失。作为参照，未经重训练的 AF3 ODE（单步采样、单次循环）仅为 51.43%，说明双重一致性蒸馏恢复了大部分精度损失。

### Recent PDB 泛化能力

在按同源性划分的 Recent PDB 数据集上（Table 3），DCFold 在所有蛋白质类别上均超越了 AF3 ODE 基线。单体蛋白的 TM-score 从 0.830 提升至 0.850（+0.020），蛋白-蛋白复合物的成功率从 87.0% 提升至 92.2%（+5.2 个百分点）。这一跨类别的一致性提升表明双重一致性训练学到的单步映射具有良好的泛化性，并非对特定结构类型的过拟合。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/005_Table_3.jpg]]
*Table 3: TM-score and Success Rate (SR) on different protein categories in the Homology Recent PDB dataset. Values in parentheses denote the absolute improvement relative to AF3 ODE*

Figure 3 的 lDDT 对比进一步支持了这一结论：DCFold 在 Pairformer 循环数（NFE）和扩散步数（NFE）均压缩至 1 的条件下，lDDT 仍接近 AlphaFold3 水平，显著优于 Protenix-Mini 等轻量级替代方案。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/006_Figure_3.jpg]]
*Figure 3: lDDT performance on the Recent PDB dataset*

### 推理效率

Table 7 按 token 数量分箱报告了推理时间。对于短序列（≤255 tokens），DCFold 平均推理时间仅为 3.76 秒，而 AlphaFold3 为 92.63 秒，加速比约 24×。随着序列增长，Pairformer 在总计算中的占比上升，加速比逐步下降：在 1024-1279 token 区间，DCFold 为 24.94 秒，AlphaFold3 为 192.44 秒，加速比约 7.7×。这一趋势与 Pairformer 的 $O(L^2)$ 复杂度一致，也是方法局限性的直接体现——当 Pairformer 本身成为瓶颈时，仅压缩扩散步数的边际收益递减。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/015_Table_7.jpg]]
*Table 7: Average inference time of AlphaFold3 and DCFold across token bins*

### 消融研究：双重一致性的两个组件

消融实验明确验证了扩散一致性和 Pairformer 一致性的独立贡献。仅应用扩散一致性蒸馏（AF3 TGM）已能显著提升单步采样性能；在此基础上加入 Pairformer 一致性（即完整 DCFold）进一步提高了 lDDT 和 TM-score（Section 4.1, Figure 3）。这证实了两个组件并非冗余：扩散一致性解决的是去噪过程的多步依赖，Pairformer 一致性解决的是循环精炼的迭代依赖，二者作用于模型的不同模块，效果叠加。

### 消融研究：TGM 调度器

Table 6 对比了四种一致性模型调度器在 Posebusters V2 上的成功率。传统的一致性蒸馏（CD）和 sCM 未能提升性能，甚至有所下降。ECM 将成功率提升至 75.7%，而 TGM 达到最高的 77.5%，且推理时间与 ECM 相同（11.6 s/step）。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/009_Table_6.jpg]]
*Table 6: Success Rates of Different Consistency Models on Posebusters V2*

TGM 的优势根源于其训练稳定性。Figure 5 的梯度范数和损失曲线揭示了关键差异：ECM 的训练动态呈现明显的阶梯状模式，伴随较大的梯度方差，表明网络在不同训练阶段面临的学习难度不均衡；而 TGM 始终保持平衡的梯度，验证了其核心设计——通过测地线距离 $d_g(t, r) = C(u)$ 将训练对的难度固定在网络当前能力的等距面上，有效抵消了变长序列训练引入的不稳定性。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/012_Figure_5.jpg]]
*Figure 5: Gradient norm and loss curve during training for ECM and TGM*

Figure 4 进一步分析了 TGM 中欧拉求解器的近似误差：训练早期相对误差较大，但随着训练推进逐步减小，后期阶段估计更精确。这说明 TGM 的调度策略具有自校正特性，早期容忍一定误差以快速探索，后期精度提升以精细优化。

### 结构多样性与置信度

Table 4 报告了 Posebusters V2 上的多样性和置信度指标。DCFold 的多样性（以 pairwise RMSD 的标准差衡量）为 0.9701 ± 0.0565，略高于 AlphaFold3 的 0.9642 ± 0.0556（数值越高多样性越低），表明一致性训练轻微压缩了采样多样性。置信度方面，DCFold 的 pLDDT 均值为 94.14 ± 2.97，略低于 AlphaFold3 的 94.67 ± 3.01，差异不显著。这一轻微的多样性损失是分布收紧的必然代价，论文指出可通过其他多样性增强策略补偿。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/007_Table_4.jpg]]
*Table 4: Diversity and confidence metrics on the Posebusters V2 benchmark*

### Binder 设计下游应用

在六个靶点的 binder 设计任务中（Table 5），DCFold 展现出优于 BindCraft（Pacesa et al., 2024）的平均 in silico 成功率。基于物理约束的成功率从 0.26 提升至 0.29，基于模型约束的成功率从 0.69 提升至 0.78。值得注意的是，该评估使用 AlphaFold2 的置信度输出而非 DCFold 自身的置信度，以避免校准偏差——这一设计选择虽然合理，但引入了间接评估的系统性局限，实际湿实验验证仍需进一步确认。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/008_Table_5.jpg]]
*Table 5: In silico success rates across six targets for binder design (values shown as physics-based constraints / model-based constraints)*

### 失败模式与局限

双重一致性训练的分布收紧效应虽改善了最差情况 RMSD，但也导致多样性轻微下降（Table 4）。对于需要探索多种构象的应用场景（如构象系综采样），这一特性可能限制实用性。

长序列场景下加速比衰减是另一个明确瓶颈。当 token 数超过 1024 时，Pairformer 成为主要计算负载，加速比降至 10× 以下（Table 7）。对于大型蛋白复合物或长链蛋白，DCFold 的效率优势部分被稀释。

此外，DCFold 依赖 AlphaFold3 预训练权重进行蒸馏，无法从头训练，这限制了其方法在缺乏强教师模型场景下的推广。目前验证范围限于蛋白质和蛋白-配体复合物，尚未拓展至核酸、翻译后修饰等更广泛的生物分子体系。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/003_Table_1.jpg]]
*Table 1: Training stages and the weights of each term*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/016_Table_8.jpg]]
*Table 8: The total number of generated samples in the binder hallucination experiments*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_LMsdys7t1L/figures/017_Table_9.jpg]]
*Table 9: Detailed information of binder targets in the binder hallucination experiments*




## 定位与知识库关联

### 1. 在蛋白质结构生成谱系中的位置

DCFold 位于蛋白质结构预测的**蒸馏加速**分支，其直接上游是 **AlphaFold3**（Abramson et al., 2024）。AlphaFold3 采用扩散模块（~200 去噪步）与 Pairformer 循环（4 次）的级联架构，虽然精度领先，但推理成本高——这是 DCFold 试图解决的核心瓶颈。

在一致性蒸馏的技术路线上，DCFold 继承了通用一致性模型（Consistency Models, CM）的思想，但将其同时应用于扩散模块和 Pairformer 两个组件，形成“双重一致性”框架。这与现有工作形成对比：

- **AF3 ODE**：仅将 AlphaFold3 的采样步数压缩为单步 ODE 积分、循环减为 1 次，但未重新训练，精度显著下降（Posebusters V2 上 Best RMSD <1Å 从 67.14% 降至 51.43%，Table 2）。
- **AF3 TGM**：仅对扩散模块施加 TGM 一致性蒸馏，未触及 Pairformer，作为消融基线验证了 TGM 调度器的独立贡献。
- **Protenix-Mini**：AlphaFold3 的轻量重实现变体（135M 参数，2 步 ODE 采样），在 Recent PDB 上的 lDDT 低于 DCFold（Figure 3），说明单纯缩小模型规模无法替代一致性训练带来的精度保持。

在 binder 设计这一下游应用中，DCFold 与 **BindCraft**（Pacesa et al., 2024）形成直接对比。BindCraft 基于 AlphaFold2 进行骨架幻觉设计，而 DCFold 则从 AlphaFold3 蒸馏而来，在六个靶点上取得了更高的平均 in silico 成功率（物理约束 0.29 vs 0.26，模型约束 0.78 vs 0.69，Table 5）。

### 2. 核心技术贡献的因果链条

DCFold 的性能提升可分解为三个因果组件，各自有明确的消融证据：

**组件一：扩散一致性（Diffusion Consistency）**
将多步扩散采样压缩为单步。单独施加扩散一致性蒸馏（即 AF3 TGM）已能将 Posebusters V2 成功率从 AF3 ODE 的 51.43% 提升至 77.5%（Table 6），证明一致性学习在蛋白质结构扩散模型上有效。

**组件二：Pairformer 一致性（Pairformer Consistency）**
在扩散一致性基础上进一步压缩 Pairformer 循环。双重一致性使 DCFold 的 Best RMSD <1Å 达到 58.10%，显著高于仅扩散一致性的 AF3 TGM（Table 2）。Figure 3 显示，Pairformer 循环数从 4 降至 1 时，双重一致性的 lDDT 下降远小于未训练模型，验证了该损失项的独立贡献。

**组件三：TGM 调度器（Temporal Geodesic Matching）**
这是稳定变长序列训练的关键。与标准一致性模型调度器（CD、sCM）和 ECM 相比，TGM 在 Posebusters V2 上达到最高成功率 77.5%（Table 6），且训练梯度更平稳——Figure 5 显示 ECM 的梯度范数呈现阶梯状跳跃和较大方差，而 TGM 保持平衡。其机制在于：TGM 基于时间 Fisher 信息 $\mathcal{I}(t)$ 计算测地线距离 $d_g(t, r) = \int_r^t \sqrt{\mathcal{I}(\tau)} d\tau$，使训练时间对的“信息距离”恒定，从而抵消变长序列引入的学习难度差异。

**采样器修改**是使单步采样可行的必要工程条件：关闭噪声注入（$\gamma_0 = 0$）、固定缩放因子（$\lambda = 1$）、归一化步长（$\eta = 1$）。论文明确指出这些修改对稳定单步采样至关重要（Section 3.2），但未提供消融实验量化各修改的独立贡献。

### 3. 适用边界与局限

**蒸馏依赖**：DCFold 需要预训练的 AlphaFold3 作为教师模型，无法从头训练。这意味着其性能上限受限于 AlphaFold3 的能力边界，且无法脱离 AlphaFold3 的架构约束。

**序列长度与加速比衰减**：对于短序列（≤255 tokens），DCFold 的推理加速比达到约 24×（3.76s vs 92.63s，Table 7）。但随着序列增长，Pairformer 的计算占比上升，加速比逐渐降至约 7.7×。这是因为 Pairformer 的 $O(L^2)$ 复杂度在长序列上成为瓶颈，而扩散模块的加速已无法进一步压缩这部分开销。

**多样性轻微下降**：双重一致性训练使输出分布收紧，这虽然改善了最差情况 RMSD（Worst RMSD <2Å 从 70.00% 提升至 71.43%，Table 2），但也导致结构多样性略微降低（Table 4）。论文认为可通过其他多样性增强策略补偿，但未给出具体方案。

**分子类型覆盖有限**：当前验证仅覆盖蛋白质单体和蛋白-配体复合物，未推广到 AlphaFold3 支持的其他生物分子（如核酸、翻译后修饰）。

**binder 评估偏差**：binder 设计实验使用 AlphaFold2 的置信度输出而非 DCFold 自身的置信度（以避免校准偏差），这可能引入系统评估偏差——AlphaFold2 的置信度分布与 AlphaFold3 蒸馏模型生成的结构之间未必完全校准。

### 4. 开放问题

1. **TGM 调度器的跨模态泛化**：TGM 的核心机制——基于时间 Fisher 信息的测地线配对——理论上适用于任何扩散模型。其在图像、音频、视频等领域的有效性尚未验证。

2. **循环一致性的架构泛化**：Pairformer 一致性损失 $\mathcal{L}_{\mathrm{pairformer}} = \sum_{i=1}^{N-1} (\mathbf{MSE}(z_i, z_{i+1}) + \mathbf{MSE}(s_i, s_{i+1}))$ 的思想——强制迭代精炼的中间表示趋于一致——是否可推广到其他迭代架构（如 AlphaFold2 的 Recycling、图神经网络的多次消息传递）？

3. **高通量场景的端到端验证**：DCFold 的 15× 加速在蛋白质组学注释和虚拟筛选中的实际收益需要大规模基准验证，特别是考虑长序列场景下加速比衰减的影响。

4. **单步模型的多样性-精度权衡**：如何在保持单步生成优势的同时，恢复或超越 AlphaFold3 的多样性水平？可能的路径包括 latent space 扰动、温度调节或多头输出策略，但均需实验验证。

5. **TGM 超参数的敏感性**：$C(u)$ 的单调递减函数形式、初始值 $C_0$ 和衰减率 $\beta$ 对训练稳定性和最终精度的影响尚未系统分析，这限制了 TGM 在新任务上的调参指导。



## 原文 PDF

![[paperPDFs/ICLR_2026/DCFold_Efficient_Protein_Structure_Generation_with_Single_Forward_Pass.pdf]]
