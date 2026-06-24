---
title: "Robust motion in-betweening"
type: paper
paper_level: A
venue: TOG
year: 2020
pdf_ref: paperPDFs/TOG_2020/Robust_motion_in_betweening.pdf
aliases:
- TC
- RMB
tags:
- TOG_2020
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "在RNN的潜在表示中加入两个可加式嵌入修饰符——时间到达嵌入（z_tta）和调度目标噪声（z_target），并通过对抗训练强化真实性。"
primary_logic: "可加式嵌入修饰符比拼接更有效，因为网络难以忽略对潜在空间的强制偏移。时间到达嵌入提供连续、平滑、有界的到达时间表示，使循环层明确剩余步数；调度目标噪声在训练初期扭曲目标信息，迫使生成器学习鲁棒性，同时支持在固定关键帧下采样多样过渡。"
claims:
- "时间到达嵌入使过渡末尾的L2Q误差显著低于简单插值和标量时间拼接，且过渡更平滑。"
- "调度目标噪声成功增加过渡多样性，而普通拼接噪声被生成器忽略。"
- "TG_complete在Human3.6M和LaFAN1的所有过渡长度上均取得最佳L2Q、L2P和NPSS，超越重建基线TG_rec和插值。"
- "Human3.6M walking subset (transition generation, up to 100 frames) 上 L2Q AVG = 0.82"
---

# Robust motion in-betweening

> [!tip] 核心洞察
> 可加式嵌入修饰符比拼接更有效，因为网络难以忽略对潜在空间的强制偏移。时间到达嵌入提供连续、平滑、有界的到达时间表示，使循环层明确剩余步数；调度目标噪声在训练初期扭曲目标信息，迫使生成器学习鲁棒性，同时支持在固定关键帧下采样多样过渡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 鲁棒运动插帧 |
| 英文题名 | Robust motion in-betweening |
| 会议/期刊 | TOG 2020 |
| Links | [paper](https://doi.org/10.1145/3386569.3392480) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | TG_complete（基于可加式嵌入修饰符的对抗循环过渡生成器） |
| Dataset | Human3.6M walking subset (transition generation, up to 100 frames), LaFAN1 (transition generation, 5 frames), 30 frames) |

> [!tip] 效果简介
> - Human3.6M walking subset (transition generation, up to 100 frames) 上，L2Q AVG 为 0.82，对比 TG-Q (without modifiers)，变化 best (lower)。
> - Human3.6M walking subset (transition generation, up to 100 frames) 上，NPSS AVG 为 0.3950，对比 TG-Q (without modifiers)，变化 best (lower)。
> - LaFAN1 (transition generation, 5 frames) 上，L2Q 为 0.17，对比 0.22 (Interpolation)，变化 -0.05。

## 概述

运动插帧（motion in-betweening）是动画制作中的核心任务：给定少量关键帧，自动生成中间过渡运动。现有基于循环神经网络（RNN）的运动预测方法在引入目标关键帧条件后，面临三重瓶颈——**缺乏过渡时长感知**导致不同长度过渡质量不稳定；**确定性生成**无法为固定关键帧提供多样化的合理运动；**简单拼接条件**使网络易于忽略目标信息，在过渡末端产生停顿、跳跃或模糊的平均姿态。

本文提出 **TG_complete**，一种基于对抗循环网络的过渡生成器。其核心创新在于向RNN的潜在表示中注入两个**可加式嵌入修饰符**（additive embedding modifiers）：**时间到达嵌入**（$z_{tta}$）和**调度目标噪声**（$z_{target}$）。时间到达嵌入通过正弦位置编码为每个时间步提供连续、平滑、有界的剩余步数表示，使循环层明确感知到达目标的距离；调度目标噪声按分段线性衰减策略扭曲目标关键帧信息，迫使生成器学习对目标扰动的鲁棒性，同时在固定关键帧下支持多样采样。可加式设计（而非拼接）是关键——网络难以忽略对潜在空间的强制偏移，从而保证修饰符真正生效。在此基础上，引入双时间尺度判别器的LSGAN框架，进一步强化过渡运动的真实感。

在Human3.6M和LaFAN1数据集上的实验表明，TG_complete在所有过渡长度上均取得最优的局部四元数误差（L2Q）、全局位置误差（L2P）和归一化功率谱相似度（NPSS），并成功泛化至训练时未见过的更长过渡。消融实验证实，时间到达嵌入是降低过渡末端误差最有效的改进，调度目标噪声则成功产生可控的运动多样性。该方法已集成至MotionBuilder插件，在实际生产环境中实现高效交互式运动插帧。

## 背景与动机

角色动画中的运动过渡（in-betweening）是计算机动画的核心问题：给定起始帧和目标关键帧，生成一段自然、平滑的中间运动。传统上，这项工作依赖动画师手动设置关键帧和调整插值曲线，耗时且难以保证物理合理性。随着深度学习在运动预测领域的进展，研究者开始探索用神经网络自动生成过渡，但现有方法存在根本性缺陷。

**核心瓶颈**在于：现有的运动预测循环神经网络（RNN）缺乏对过渡时长的感知能力和随机建模机制。仅仅在RNN输入中拼接目标关键帧条件，无法生成平滑、多样且长度可变的过渡。具体表现为三类典型失败模式：（1）过渡末端出现停顿或跳跃，无法平滑抵达目标；（2）生成的运动趋于模糊的平均姿态，缺乏多样性；（3）网络无法泛化到训练时未见过的更长过渡长度。

**因果机制**上，上述失败源于两个结构性问题。第一，传统RNN对时间步的感知仅依赖隐状态递推，当过渡长度变化时，网络无法明确获知“还剩多少步到达目标”，导致时序控制失准。第二，普通拼接式噪声（如将随机向量拼接到输入）会被生成器轻易忽略——网络学会绕过噪声通道直接依赖确定性输入，无法产生可控的运动变化。

**本文动机**正是针对这两个缺口，提出两个可加式嵌入修饰符（additive embedding modifiers），通过强制偏移潜在表示的方式，使网络无法忽略时间信息和随机扰动。具体而言，时间到达嵌入（$z_{tta}$）为每个时间步提供连续、平滑、有界的剩余步数表示；调度目标噪声（$z_{target}$）在训练初期扭曲目标信息，迫使生成器学习对目标扰动的鲁棒性，同时支持在固定关键帧下采样多样过渡。配合对抗训练，系统能够生成高质量、可变长度且可采样的运动过渡，并已在MotionBuilder插件中实现工业级部署。

## 核心创新

本工作的核心创新在于为循环过渡生成器引入两个**可加式嵌入修饰符**（additive embedding modifiers），以解决现有RNN在运动插帧（motion in-betweening）中缺乏过渡时长感知和随机性的瓶颈。与简单拼接条件信息不同，可加式嵌入通过对潜在表示的强制偏移，使网络无法忽略这些信号，从而从根本上改变生成行为。

### 瓶颈分析

现有运动预测RNN（如**TP-RNN**（Chiu et al., WACV 2019）和**VGRU-d/rl**（Gopalakrishnan et al., CVPR 2019））在直接添加目标关键帧条件后，仍面临三个核心问题：
- **时长模糊**：网络不知道当前帧距离目标关键帧还有多少步，导致过渡末尾出现停顿、跳跃或模糊的平均姿态。
- **缺乏多样性**：给定固定上下文，生成器只能产生单一的确定性过渡。
- **目标扰动脆弱**：对关键帧的微小修改缺乏鲁棒性，无法支持用户交互式调整。

### 创新一：时间到达嵌入（$z_{tta}$）

**基线做法**：无时间感知（TG-Q）或拼接标量剩余时间。

**创新机制**：将基于到达时间（time-to-arrival, $tta$）的正弦位置编码以**可加方式**注入所有输入潜在表示，维度为256：

$$\mathbf{z}_{tta, 2i} = \sin\left(\frac{tta}{basis^{2i/d}}\right) \quad \mathbf{z}_{tta, 2i+1} = \cos\left(\frac{tta}{basis^{2i/d}}\right)$$

其中 $basis=10000$，$d=256$。该嵌入提供连续、平滑、有界的时间表示，使LSTM循环层在每个时间步都明确知晓剩余步数。

**关键证据**（Fig. 3, Table 2）：消融实验表明，$z_{tta}$ 是降低过渡末端L2Q误差最有效的改进，远超标量时间拼接和简单插值。添加 $z_{tta}$ 后，生成的过渡在末尾明显更平滑，解决了停顿和跳跃问题。

### 创新二：调度目标噪声（$z_{target}$）

**基线做法**：无噪声（确定性生成）或拼接噪声（$z_{concat}$）。

**创新机制**：从球面高斯 $\mathcal{N}(0, I \cdot \sigma_{target})$ 采样噪声向量，以**可加方式**注入拼接后的偏移-目标嵌入。噪声强度由分段线性衰减调度 $\lambda_{target}$ 控制：

$$\lambda_{target} = \begin{cases} 1 & \text{if } tta \geq 30 \\ \frac{tta-5}{25} & \text{if } 5 \leq tta < 30 \\ 0 & \text{if } tta < 5 \end{cases}$$

该调度在过渡初期（$tta \geq 30$）保持全强度噪声，迫使生成器学习对目标扰动的鲁棒性；在过渡末期（$tta < 5$）完全关闭噪声，确保平滑到达目标关键帧。

**关键证据**（Fig. 4）：拼接噪声（$z_{concat}$）被生成器完全忽略，而调度目标噪声（$z_{target}$）成功产生可控的过渡多样性。同一上下文下多次采样可观察到明显的运动变化，且变化幅度可通过噪声强度调节。

### 创新三：对抗训练与双时间尺度判别器

**基线做法**：仅使用重建损失（$L_{rec}$）。

**创新机制**：引入LSGAN框架，使用两个时间尺度判别器：
- **$C_1$（长期判别器）**：对10帧滑动窗口评分，惩罚异常全局运动模式。
- **$C_2$（短期判别器）**：对2帧滑动窗口评分，惩罚瞬时伪影和不连续。

两个判别器均为三层全连接网络（512→256→1），使用ReLU激活。在过渡起止处，判别器以真实上下文帧为条件，增强对过渡边界真实性的判断。

**关键证据**（Table 2）：逐步添加 $L_{pos}$、$z_{tta}$、$z_{target}$ 及对抗损失 $L_{gen}$ 后，L2Q、L2P和NPSS指标持续提升。完整的TG_complete在所有过渡长度上均取得最佳结果，并成功泛化至训练时未见的更长序列（训练≤50帧，评估≤100帧）。

### 设计原则：为何可加式优于拼接

可加式嵌入修饰符的核心设计原则在于：网络**难以忽略**对潜在空间的强制偏移。拼接方式允许网络选择性关注或忽略特定维度，实验证实生成器完全学会了忽略拼接噪声（$z_{concat}$）。而可加式嵌入直接偏移所有潜在表示，迫使网络在生成过程中始终响应这些信号，从而保证时间感知和多样性控制的有效性。

## 整体框架

![[assets/figures/papers/paper_list_l51_https_doi_org_10_1145_3386569_3392480/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the $\mathbf { T G } _ { c o m p l e t e }$ architecture for in-betweening. Computations for a single timestep are shown. Visual concatenation of input boxes or arrows represents vector concatenation. Green boxes are the jointly trained neural networks. Dashed boxes represent our two proposed embedding modifiers. The "quat norm" and " $\mathsf { F K " }$ red boxes represent the quaternion normalization and Forward Kinematics operations respectively. The ⊕ sign represents element-wise addition and $\phi$ is the sigmoid non-linearity. Outputs are linked to associated losses with dashed lines

### 问题定义

给定过去10帧的运动上下文（包括局部四元数速度 $\dot{\mathbf{q}}_t$、全局根速度 $\dot{\mathbf{r}}_t$、足部接触标签 $\mathbf{c}_t$）和一个目标关键帧 $\mathbf{q}_{target}$，系统需要生成从当前帧到目标帧之间任意长度的过渡运动序列。核心挑战在于：传统RNN仅添加目标条件无法产生平滑、多样且长度可变的过渡，会出现停顿、跳跃或模糊的平均姿态。

### 架构总览

**TG_complete** 采用编码器-循环层-解码器结构，其关键创新在于两个可加式嵌入修饰符——时间到达嵌入（$\mathbf{z}_{tta}$）和调度目标噪声（$\mathbf{z}_{target}$）——它们以元素加法而非拼接的方式注入潜在表示空间。这一设计选择具有因果必然性：拼接噪声容易被网络忽略（生成器学会将其滤除），而可加式嵌入对潜在空间施加强制性偏移，迫使网络做出响应。

整体数据流如下（参见 Fig. 2）：

1. **输入分解**：将当前帧信息拆分为三类向量——
   - 角色状态向量：$\dot{\mathbf{q}}_t$、$\dot{\mathbf{r}}_t$、$\mathbf{c}_t$
   - 偏移向量：当前帧相对于目标帧的根偏移和四元数偏移
   - 目标向量：目标关键帧的四元数 $\mathbf{q}_{target}$

2. **编码器组**：三个独立的前馈编码器（均为512隐藏单元→256输出单元，PLU激活）分别处理上述三类输入，产生三个256维的潜在表示。这种分离设计使得嵌入修饰符能够精准作用于特定语义通道。

3. **可加式嵌入修饰符注入**：
   - **时间到达嵌入 $\mathbf{z}_{tta}$**：基于剩余步数的正弦位置编码（256维），以元素加法注入所有输入潜在表示。它提供连续、平滑、有界的到达时间信号，使循环层明确感知当前时刻距离目标还有多少步。公式为：
     $$\mathbf{z}_{tta, 2i} = \sin\left(\frac{tta}{basis^{2i/d}}\right) \quad \mathbf{z}_{tta, 2i+1} = \cos\left(\frac{tta}{basis^{2i/d}}\right)$$
     其中 $tta$ 为剩余帧数，$basis=10000$，$d=256$。为支持泛化至训练时未见过的更长序列，定义最大持续时间 $T_{max}$，超过该值时嵌入固定不变（Fig. 8）。
   - **调度目标噪声 $\mathbf{z}_{target}$**：从球面高斯 $\mathcal{N}(0, I \cdot \sigma_{target})$ 采样的256维噪声向量，以元素加法注入拼接后的偏移-目标嵌入。噪声强度由分段线性衰减因子 $\lambda_{target}$ 控制：
     $$\lambda_{target} = \begin{cases} 1 & \text{if } tta \geq 30 \\ \frac{tta-5}{25} & \text{if } 5 \leq tta < 30 \\ 0 & \text{if } tta < 5 \end{cases}$$
     该调度在过渡末期（最后5帧）关闭噪声以保证平滑到达，在早期（30帧以外）保持全强度以最大化多样性。

4. **LSTM循环层**：处理拼接后的增强嵌入序列，建模时序动态。其隐状态编码了从起始帧到当前时刻的运动历史。

5. **解码器**：从LSTM隐状态预测下一帧的 $\dot{\mathbf{q}}_{t+1}$、$\dot{\mathbf{r}}_{t+1}$ 和 $\mathbf{c}_{t+1}$。

6. **正向运动学（FK）**：将预测的局部四元数和根位置转换为全局关节位置 $\mathbf{p}_t$，供位置损失计算。四元数在FK前经过归一化处理。

7. **双时间尺度判别器**（Fig. 7）：
   - **C1（长期判别器）**：在10帧滑动窗口上评分，惩罚异常的全局运动模式。
   - **C2（短期判别器）**：在2帧滑动窗口上评分，惩罚瞬时伪影。
   
   两者均为3层全连接网络（512→256→1，ReLU激活），在过渡的起始和末尾包含真实上下文帧作为条件输入。各时间步的标量分数取平均得到最终评分。

### 训练损失

生成器总损失为：
$$L_{total} = L_{quat} + L_{root} + L_{pos} + L_{contacts} + L_{gen}$$

其中各分量均为L1范数（对抗损失 $L_{gen}$ 除外，采用LSGAN形式）。$L_{pos}$ 通过正向运动学在全局关节位置上计算，确保角色在世界空间的位移正确；$L_{contacts}$ 为足部接触预测损失，用于后续IK后处理。

## 核心模块与公式推导

TG_complete 的核心架构由三个功能独立的编码器、两个可加式嵌入修饰符、一个 LSTM 循环层及一个解码器构成（Fig. 2）。输入为 10 帧历史上下文和一个目标关键帧，输出为过渡序列的逐帧四元数速度、全局根速度及脚部接触标签，最后通过正向运动学（FK）还原全局关节位置。

---

### 数据表示

每一帧的动作数据由三类向量组成：
- **局部四元数速度** $\dot{\mathbf{q}}_t \in \mathbb{R}^{j \times 4}$：所有关节相对于父关节的旋转速度，$j$ 为关节数。
- **全局根速度** $\dot{\mathbf{r}}_t \in \mathbb{R}^3$：角色在世界坐标系中的位移速度。
- **接触标签** $\mathbf{c}_t \in \{0,1\}^4$：双脚脚跟与脚尖的地面接触状态。

---

### 编码器

三个编码器均为全连接前馈网络，结构相同：单隐藏层 512 单元，输出层 256 单元，激活函数为分段线性单元（PLU）。

- **角色状态编码器**：输入当前帧的 $\dot{\mathbf{q}}_t$、$\dot{\mathbf{r}}_t$、$\mathbf{c}_t$，输出当前运动状态的潜在表示。
- **偏移编码器**：输入当前姿态相对于目标关键帧的根偏移量及四元数偏移量，编码空间偏差信息。
- **目标编码器**：输入目标关键帧的四元数，编码目标姿态特征。

偏移编码器与目标编码器的输出经拼接后，进入嵌入修饰符的处理阶段。

---

### 核心模块一：时间到达嵌入（$\mathbf{z}_{tta}$）

**瓶颈**：传统 RNN 缺乏过渡时长的感知能力，无法在固定上下文下生成可变长度的平滑过渡，导致末端出现停顿或跳跃。

**设计**：为每个时间步生成一个 256 维的正弦位置编码，直接**逐元素相加**到所有输入潜在表示上（角色状态嵌入、偏移-目标拼接嵌入），而非拼接。可加式设计迫使网络无法忽略时间信息，因为潜在空间被强制偏移。

**公式**：

$$
\mathbf{z}_{tta, 2i} = \sin\left(\frac{tta}{\text{basis}^{2i/d}}\right), \quad
\mathbf{z}_{tta, 2i+1} = \cos\left(\frac{tta}{\text{basis}^{2i/d}}\right)
$$

其中 $tta$ 为当前帧距目标关键帧的剩余帧数，$d=256$ 为嵌入维度，$\text{basis}$ 控制频率范围。该编码具有连续、平滑、有界三个关键性质：剩余步数越小，嵌入变化越剧烈，使 LSTM 能精确感知过渡末端。

**泛化策略**：定义最大过渡时长 $T_{max}$，当 $tta > T_{max}$ 时将嵌入固定为 $\mathbf{z}_{tta}(T_{max})$，避免 LSTM 在推理更长序列时遭遇训练中未见的嵌入值（Fig. 8）。

**消融证据**：Fig. 3 表明，$\mathbf{z}_{tta}$ 在过渡末端的 L2Q 误差显著低于简单插值和标量时间拼接；Table 2 的消融实验确认其是降低 L2Q/L2P/NPSS 最有效的单一改进。

---

### 核心模块二：调度目标噪声（$\mathbf{z}_{target}$）

**瓶颈**：普通拼接噪声（$\mathbf{z}_{concat}$）被生成器完全忽略，无法产生过渡多样性；且生成器对目标关键帧的微小扰动不鲁棒。

**设计**：从球面高斯分布 $\mathcal{N}(0, I \cdot \sigma_{target})$ 采样一个噪声向量，**逐元素相加**到偏移编码器与目标编码器的拼接输出上。噪声在整个过渡序列中保持不变（每序列采样一次），但其幅度由调度因子 $\lambda_{target}$ 控制：

$$
\lambda_{target} = 
\begin{cases}
1 & \text{if } tta \geq 30 \\
\frac{tta - 5}{25} & \text{if } 5 \leq tta < 30 \\
0 & \text{if } tta < 5
\end{cases}
$$

**调度逻辑**：
- $tta \geq 30$：噪声全量注入，迫使生成器在远离目标时对目标信息扰动保持鲁棒。
- $5 \leq tta < 30$：噪声线性衰减，逐步过渡到精确到达。
- $tta < 5$：噪声归零，保证最后 5 帧无噪声平滑到达目标关键帧。

**因果机制**：可加式噪声直接扭曲目标信息，生成器无法通过“忽略”来规避——它必须学会从被扰动后的目标表示中恢复合理的运动轨迹。这种强制偏移在训练初期充当正则化，在推理时则通过重采样 $\mathbf{z}_{target}$ 产生可控的过渡多样性。

**消融证据**：Fig. 4 显示，$\mathbf{z}_{concat}$ 被生成器完全忽略（10 次重采样结果几乎相同），而 $\mathbf{z}_{target}$ 产生明显且可控的运动变化。Table 2 确认添加 $\mathbf{z}_{target}$ 后所有指标持续改善。

---

### 判别器与对抗训练

采用 LSGAN 框架，引入两个时间尺度的判别器（Fig. 7）：

- **C1（长期判别器）**：在 10 帧滑动窗口上评分，惩罚异常全局运动模式。
- **C2（短期判别器）**：在 2 帧滑动窗口上评分，惩罚瞬时伪影（如抖动、滑步）。

两者均为三层全连接网络（512 → 256 → 1），隐藏层使用 ReLU 激活。在过渡的起始和末尾，判别器包含真实上下文帧作为条件输入，使评分聚焦于生成段的质量。

---

### 损失函数

生成器总损失为重建损失与对抗损失的加权组合：

**重建损失**（L1 范数）：
- $L_{quat} = \frac{1}{T} \sum_{t=0}^{T-1} \| \hat{\mathbf{q}}_t - \mathbf{q}_t \|_1$：局部四元数重建。
- $L_{root} = \frac{1}{T} \sum_{t=0}^{T-1} \| \hat{\mathbf{r}}_t - \mathbf{r}_t \|_1$：全局根位置重建。
- $L_{pos} = \frac{1}{T} \sum_{t=0}^{T-1} \| \hat{\mathbf{p}}_t - \mathbf{p}_t \|_1$：通过 FK 计算的全局关节位置损失。
- $L_{contacts} = \frac{1}{T} \sum_{t=0}^{T-1} \| \hat{\mathbf{c}}_t - \mathbf{c}_t \|_1$：接触标签预测损失，用于后续 IK 后处理。

**对抗损失**（生成器侧）：

$$
L_{gen} = \frac{1}{2} \mathbb{E}_{\mathbf{X}_P, \mathbf{X}_f \sim p_{Data}} \left[ (D(\mathbf{X}_{\hat{P}}, G(\mathbf{X}_{\hat{P}}, \mathbf{X}_f), \mathbf{X}_f) - 1)^2 \right]
$$

其中 $\mathbf{X}_P$ 为过去上下文，$\mathbf{X}_f$ 为目标关键帧，$G$ 为生成器，$D$ 为判别器。

**关键设计决策**：$L_{pos}$ 通过 FK 将局部旋转转换为全局位置后计算，直接约束世界空间中的关节轨迹，弥补了纯四元数损失对末端执行器位置约束不足的问题。但 FK 的反向传播计算成本较高，因此偏移表示中未包含位置偏移（仅使用根偏移和四元数偏移），这是已知局限。

## 实验与分析

### 运动预测基线的竞争力验证

在构建过渡生成器之前，作者首先验证了其基础循环架构在无约束运动预测任务上的性能。该预测网络被命名为**ERD-QV**（ERD-Quaternion Velocity network），以四元数速度作为状态编码器的唯一输入，训练损失仅为关节局部四元数的L1范数。在Human3.6M基准上，ERD-QV与当时领先的**TP-RNN**（Chiu et al., WACV 2019）和**VGRU-d/rl**（Gopalakrishnan et al., CVPR 2019）进行了对比（Table 1）。结果显示，ERD-QV在角度误差上优于TP-RNN，并在所有动作类别的NPSS指标上超越了VGRU-d。NPSS指标的引入是为了更好地与人类感知质量对齐，这一结果为后续过渡生成器的设计奠定了可信的基础。

![[assets/figures/papers/paper_list_l51_https_doi_org_10_1145_3386569_3392480/figures/005_Table_1.jpg]]
*Table 1: Unconstrained motion prediction results on Human 3.6M. The VGRU-d/rl models are from [Gopalakrishnan et al. 2019]. The TP-RNN is from [Chiu et al. 2019] and has to our knowledge the best published results on motion prediction for this benchmark. Our model, ERD-QV is competitive with the state-of-the-art on angular errors and improves performance with respect to the recently proposed NPSS metric on all actions*

### 过渡生成的主实验结果

#### Human3.6M基准

Table 2报告了在Human3.6M行走子集上的过渡生成基准测试。模型训练时使用的最大过渡长度为50帧，但评估扩展至100帧（4秒），以检验泛化能力。核心发现如下：

![[assets/figures/papers/paper_list_l51_https_doi_org_10_1145_3386569_3392480/figures/006_Table_2.jpg]]
*Table 2: Transition generation benchmark on Human 3.6M. Models were trained with transition lengths of maximum 50 frames, but are evaluated beyond this horizon, up to 100 frames (4 seconds)*

- **TG_complete在所有过渡长度和所有指标上均取得最优**。与无修饰符的基线TG-Q相比，TG_complete在平均L2Q上从1.16降至0.82，在平均NPSS上从0.5597降至0.3950，L2P同样大幅改善。
- **逐步消融验证了各组件的贡献**：依次添加位置损失（L_pos）、时间到达嵌入（z_tta）、调度目标噪声（z_target）和对抗损失（L_gen），L2Q、L2P和NPSS持续单调下降。其中，z_tta的引入带来了最显著的性能跃升，尤其在过渡末端。
- **泛化至更长序列**：尽管训练时仅见到最长50帧的过渡，TG_complete在60-100帧区间仍保持较低的L2Q误差，验证了时间到达嵌入对未见过渡长度的鲁棒性。

#### LaFAN1基准

Table 3展示了在LaFAN1数据集上的结果。模型训练时最大过渡长度为30帧（1秒），评估覆盖5、15、30和45帧。TG_complete在所有长度和所有指标上均超越插值基线和TG-Q。值得注意的是，在5帧的极短过渡上，TG_complete的L2Q仅为0.17，而插值为0.22；在30帧过渡上，TG_complete的L2Q为0.69，显著低于插值。这表明方法对不同数据集和运动风格具有良好的迁移能力。

![[assets/figures/papers/paper_list_l51_https_doi_org_10_1145_3386569_3392480/figures/007_Table_3.jpg]]
*Table 3: Improving in-betweening on the LaFAN1 dataset. Models were trained with transition lengths of maximum 30 frames (1 second), and are evaluated on 5, 15, 30, and 45 frames*

### 关键消融分析

#### 时间到达嵌入的有效性

Figure 3的消融实验直接比较了四种时间感知策略在过渡生成中的L2Q误差曲线：
- **简单插值**：在过渡中段表现尚可，但末端误差急剧上升，产生不自然的停顿或跳跃。
- **TG-Q（无时间感知）**：整体误差高于插值，说明缺乏时间信息使网络难以规划到达。
- **标量时间拼接**（添加到角色状态或LSTM输入）：改善有限，网络难以有效利用单一标量值。
- **时间到达嵌入（z_tta）**：在整个过渡过程中保持最低的L2Q误差，尤其在末端优势最为明显，生成的过渡比插值更平滑。

这一结果验证了核心设计选择：可加式正弦嵌入比拼接更有效，因为网络难以忽略对潜在空间的强制偏移；连续、平滑、有界的到达时间表示使循环层能够明确感知剩余步数。

#### 调度目标噪声的多样性效果

Figure 4对比了两种噪声注入策略在100帧过渡中段（重新采样10次）的多样性表现：
- **拼接噪声（z_concat）**：10次采样生成的过渡几乎完全重叠，生成器成功学会了忽略该噪声。
- **调度目标噪声（z_target）**：10次采样产生明显可辨的运动变化，变化幅度可通过噪声尺度控制。

![[assets/figures/papers/paper_list_l51_https_doi_org_10_1145_3386569_3392480/figures/004_Figure_4.jpg]]
*Figure 4: Increasing variability with ${ \bf$ z $} _ { t a r g e t }$ . We compare ${ \bf$ z $} _ { c o n c a t }$ (left) against ${ \bf$ z $} _ { t a r g e t }$ (right) midway in a 100-frames transition re-sampled 10 times. The generator successfully learns to ignore ${ \bf$ z $} _ { c o n c a t }$ while ${ \bf$ z $} _ { t a r g e t }$ is imposed and leads to noticeable variations with controllable scale

这证实了可加式嵌入修饰符的另一个关键优势：通过强制偏移目标信息，生成器无法简单地忽略噪声，从而被迫学习对目标扰动的鲁棒性，同时实现了在固定关键帧条件下的可控多样性采样。

#### 对抗训练的贡献

Table 2的消融序列显示，在已包含L_pos、z_tta和z_target的基础上加入对抗损失（L_gen），进一步降低了L2Q（从0.88到0.82）和NPSS（从0.4225到0.3950）。双时间尺度判别器（C1：10帧滑动窗口；C2：2帧滑动窗口）分别惩罚异常全局运动和瞬时伪影，共同提升了过渡的视觉真实性。

### 数据与风格消融

作者还进行了数据消融实验：当从训练集中移除舞蹈数据后，模型在舞蹈类过渡上无法保持风格特征。这表明全量训练数据对风格保留至关重要，也暗示该方法依赖数据覆盖来实现风格一致性，而非显式的风格控制机制。

### 推理性能与生产部署

Table 4报告了MotionBuilder插件的速度性能。在Intel Xeon CPU E5-1650 @ 3.20GHz上，模型推理（含IK后处理）耗时极短，生成10段30帧过渡仅需约0.5秒，内存占用低，满足实时交互式动画编辑的需求。

![[assets/figures/papers/paper_list_l51_https_doi_org_10_1145_3386569_3392480/figures/009_Table_4.jpg]]
*Table 4: Speed performance summary of our MotionBuilder plugin. The model inference also includes the IK postprocess. The last column indicates the time taken to produce a string of 10 transitions of 30 frames. Everything is run on a Intel Xeon CPU E5-1650 @ 3.20GHz*

### 失败模式与局限性

尽管TG_complete在定量和定性评估中表现优异，论文明确指出了若干局限：
1. **极端条件过渡**：方法难以生成训练集外的不现实或极端条件的过渡，泛化受限于训练数据分布。
2. **风格控制缺失**：调度目标噪声允许在一定程度上改变运动风格，但无法提供明确的风格控制接口。
3. **肢体末端伪影**：仅使用位置损失（L_pos）不能保证骨骼方向，常在运动链末端产生伪影。这是由于偏移表示中未包含位置偏移（加入会导致训练反向传播过慢），使得全局位置约束不足。
4. **架构选择未解之谜**：作者尝试了Triangular-Prism RNN架构但未获得增益，原因尚不明确。

这些失败模式为后续研究指明了方向：如何在不断增训练成本的情况下纳入位置偏移信息、如何实现给定固定上下文条件下的显式风格控制，以及如何扩展方法以处理更极端的运动过渡场景。

## 方法谱系与知识库定位

### 问题定位：运动过渡生成中的核心瓶颈

运动插帧（in-betweening）是角色动画制作中的关键环节，其任务是在给定的起始上下文和目标关键帧之间自动生成平滑、逼真的过渡运动。现有方法面临三个根本性瓶颈：

1. **时序感知缺失**：传统RNN运动预测器（如**TP-RNN**, Chiu et al., WACV 2019）缺乏对过渡时长的感知能力。仅将目标关键帧作为条件拼接输入，网络无法判断距离目标还有多少步，导致过渡末端出现停顿、跳跃或模糊的平均姿态。这一瓶颈的因果机制在于：RNN的隐状态在无时间参照的情况下，无法区分“距离目标还有1帧”与“距离目标还有50帧”两种截然不同的生成策略。

2. **多样性缺失**：确定性生成器在固定起始和目标关键帧条件下只能产生单一解，无法为动画师提供可选的过渡变体。普通拼接噪声（$z_{concat}$）策略被证明无效——生成器学会完全忽略这些噪声，因为网络可以通过“捷径”直接从确定性输入中重建输出。

3. **对抗训练的缺失**：纯重建损失（$L_{rec}$）倾向于产生模糊的平均姿态，无法捕捉真实运动的高频细节和自然度。

### 核心因果机制：可加式嵌入修饰符

TG_complete的核心创新在于识别出“可加式嵌入修饰符”这一因果调控旋钮。其关键洞察是：**对潜在表示的可加式偏移比拼接更有效，因为网络难以忽略对潜在空间的强制扰动**。这形成了两个互补的修饰符：

- **时间到达嵌入（$z_{tta}$）**：将剩余过渡步数编码为256维正弦位置嵌入（Equation 2），以逐元素加法的方式注入所有输入潜在表示。该嵌入具有连续、平滑、有界的特性，使LSTM层在每个时间步都能明确感知距离目标的剩余步数。消融实验（Fig. 3）表明，$z_{tta}$是降低过渡末端L2Q误差最有效的改进，其效果远超标量时间拼接和简单插值。

- **调度目标噪声（$z_{target}$）**：从球面高斯采样的噪声向量，按分段线性衰减调度$\lambda_{target}$（Equation 3）缩放后，以加法方式注入拼接的偏移-目标嵌入。调度机制在过渡早期（$tta \geq 30$）保持全量噪声，迫使生成器学习对目标扰动的鲁棒性；在过渡末期（$tta < 5$）将噪声降为零，确保平滑到达。Fig. 4的对比实验证明，$z_{target}$成功产生可控的过渡多样性，而拼接噪声$z_{concat}$被生成器完全忽略——这验证了“可加式强制偏移”这一因果机制的有效性。

### 架构继承与改进

TG_complete的架构基础来自两条技术路线：

1. **运动预测主干**：继承自**TP-RNN**（Chiu et al., WACV 2019）的循环架构，该架构在当时是Human3.6M长时运动预测的状态领先方法。TG_complete保留了其核心LSTM层设计，但将输入重构为三个独立编码器（角色状态编码器、偏移编码器、目标编码器），以便在不同输入部分分别施加嵌入修饰符。

2. **前馈编码器**：借鉴**RTN**（Harvey et al., 2018）的分离编码设计。TG_complete使用三个全连接编码器（512隐藏单元→256输出单元，PLU激活），分别处理角色状态（四元数速度、根速度、接触标签）、偏移（当前姿态相对于目标的根偏移和四元数偏移）和目标关键帧（目标四元数）。

3. **对抗训练框架**：引入LSGAN，使用两个时间尺度判别器——C1（10帧滑动窗口，惩罚异常全局运动）和C2（2帧滑动窗口，惩罚瞬时伪影）。这与运动预测任务中的纯重建训练形成根本区别。

### 适用边界与局限

尽管TG_complete在Human3.6M和LaFAN1上取得显著改进（Table 2, Table 3），其方法存在明确边界：

1. **分布外泛化受限**：方法难以生成训练集外的不现实或极端条件过渡。这是因为对抗训练和重建损失的联合优化本质上约束生成器在训练分布内运作。

2. **风格控制缺失**：调度目标噪声允许在一定程度上改变运动风格，但无法提供明确的风格控制接口。噪声采样是随机的，动画师无法指定“更夸张”或“更保守”的过渡风格。

3. **偏移表示不完整**：当前偏移表示仅使用根偏移和四元数偏移，未包含位置偏移。这可能导致肢体全局位置约束不足。作者指出，加入位置偏移会使训练时的反向传播过慢，这是一个工程权衡。

4. **骨骼方向约束不足**：仅使用位置损失（$L_{pos}$）不能保证骨骼方向，常在运动链末端产生伪影。这需要后续IK修正来弥补。

### 开放问题

论文明确提出了三个未解决的问题：

1. **架构选择之谜**：为何Triangular-Prism RNN架构（Chiu et al., 2019的核心设计）在过渡生成任务中未能提供增益？这可能暗示过渡生成与纯预测任务对循环架构有不同的归纳偏置需求。

2. **位置偏移的工程困境**：如何在不断增训练成本的情况下，将位置偏移纳入表示以改进全局约束？这需要在表示完整性和计算效率之间找到新的平衡点。

3. **可控多样性**：如何在给定固定上下文的条件下实现风格控制？当前$z_{target}$仅提供随机多样性，而动画制作需要可解释的风格参数化。

### 知识库定位

TG_complete在运动生成方法谱系中占据“条件循环生成+对抗训练”的交叉位置。其技术贡献的可迁移性体现在：可加式嵌入修饰符的设计范式——通过强制潜在空间偏移而非拼接来注入条件信息——可推广至其他需要时序感知和可控多样性的序列生成任务。然而，该方法对分布外泛化和风格控制的局限，指向了后续工作（如基于扩散模型或可学习先验的方法）的改进方向。

## 原文 PDF

![[paperPDFs/TOG_2020/Robust_motion_in_betweening.pdf]]
