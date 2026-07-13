---
title: "TLControl: Trajectory and Language Control for Human Motion Synthesis"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis.pdf
project_link: null
code_link: null
aliases:
- TLControl
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在分体式 VQ‑VAE 学习到的紧凑、结构良好的潜在空间中进行测试时优化（以 MTT 粗预测为起点），从而能够精确且灵活地控制任意关节轨迹。
primary_logic: 将人体运动分解为多个身体部位的离散潜在表示，使得轨迹跟随优化可以在不破坏整体运动语义的前提下进行，从而在保证精度的同时维持自然运动。
claims:
- 在 HumanML3D 数据集上控制全部六个关节时，TLControl 的 Traj.Err. 和 Loc.Err. 均为 0.00%，而 OmniControl 分别为 75.59% 和 12.30%。
- TLControl 的 Avg.Err.（1.57 cm）远低于 OmniControl（23.67 cm），同时 FID 从 2.614 降至 0.032。
- TLControl 的推理速度（0.015 s/frame）比 OmniControl（0.606 s/frame）快 40 倍以上，也远快于 MDM 和 GMD。
- 消融实验表明，分体式 VQ‑VAE 相比统一 VQ‑VAE，控制所有关节时的平均误差从 2.51 cm 降至 1.57 cm，且运行时降低 27.3%。
---

# TLControl: Trajectory and Language Control for Human Motion Synthesis

> [!tip] 核心洞察
> 将人体运动分解为多个身体部位的离散潜在表示，使得轨迹跟随优化可以在不破坏整体运动语义的前提下进行，从而在保证精度的同时维持自然运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | TLControl：轨迹与语言控制的人体运动合成 |
| 英文题名 | TLControl: Trajectory and Language Control for Human Motion Synthesis |
| 会议/期刊 | ECCV 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TLControl |
| Dataset | HumanML3D, KIT, Runtime |

> [!tip] 效果简介
> - HumanML3D (test set) 上，Traj.Err.↓ (50 cm, %) 0.00 vs 75.59 (OmniControl) (-75.59%)；Avg.Err.↓ (cm) 1.57 vs 23.67 (OmniControl) (-22.10 cm)；FID↓ / R‑precision↑ (Top‑3) 0.032 / 0.794 vs 2.614 / 0.606 (OmniControl) (-2.582 / +0.188)。
> - KIT (test set) 上，Avg.Err.↓ (cm) on Pelvis control 2.76 vs 7.59 (OmniControl) (-4.83 cm)。
> - Runtime (per frame) 上，Time (s/frame)↓ 0.015 vs 0.606 (OmniControl) (≈ 40× faster)。

## 概要

**核心问题**：在人体运动合成中，现有基于扩散模型的方法（如 **MDM** (Tevet et al., arXiv 2022)、**PriorMDM** (Shafir et al., arXiv 2023)、**GMD** (Karunratanakul et al., ICCV 2023) 及 **OmniControl** (Xie et al., arXiv 2023)）面临一个根本性瓶颈——难以在精确跟随多关节部分轨迹的同时，保持语言描述所指定的运动语义。此外，扩散模型的多步迭代采样耗时严重，无法满足交互式应用对实时性的需求。

**核心思路**：TLControl 将人体运动分解为多个身体部位的离散潜在表示（分体式 VQ‑VAE），并在此紧凑、结构良好的潜在空间中进行测试时优化。这一设计使得轨迹跟随优化可以在不破坏整体运动语义的前提下进行，从而在保证精度的同时维持自然运动。

**方法定位**：TLControl 属于“神经生成 + 优化精化”的混合范式，与纯扩散引导或特征注入方法形成对比。其方法谱系可定位于：
- **运动离散表示**：将人体按 Head、Left arm、Right arm、Left leg、Right leg、Root 六个部位独立编码为离散码本，获得紧凑且结构化的潜在空间。
- **粗粒度初始预测**：使用 Masked Trajectory Transformer（MTT）结合连续轨迹掩码和关节级掩码，一次性预测初始潜在代码。
- **测试时优化精化**：以 MTT 输出为起点，在潜在空间中以 L‑BFGS 进行少量迭代优化，最小化生成关节位置与目标轨迹之间的欧氏距离。

**主要结果**：在 HumanML3D 数据集上控制全部六个关节时，TLControl 的轨迹误差（Traj.Err.）和位置误差（Loc.Err.）均为 0.00%，而 OmniControl 分别为 75.59% 和 12.30%；平均关节误差从 23.67 cm 降至 1.57 cm，FID 从 2.614 降至 0.032。推理速度达到 0.015 s/frame，比 OmniControl（0.606 s/frame）快约 40 倍。消融实验证实，分体式 VQ‑VAE 设计相比统一 VQ‑VAE 将平均误差从 2.51 cm 降至 1.57 cm，且运行时间降低 27.3%。



### 问题背景

可控人体运动合成是计算机视觉与图形学中的核心问题，其目标是根据用户提供的控制信号生成自然、多样且符合语义的人体运动序列。近年来，文本驱动的运动生成取得了显著进展，基于扩散模型的方法（如 **MDM**（Tevet et al., arXiv 2022））能够从自然语言描述中生成高质量的运动。然而，纯文本控制存在固有的模糊性——同一句描述可对应无数种空间实现，难以满足需要精确空间约束的应用场景（如 VR 角色导航、电影预演、游戏交互）。

轨迹控制作为一种互补的模态，通过指定关键关节（如手腕、脚踝、骨盆）在空间中的运动路径，提供了精确的空间引导。将语言语义与轨迹控制相结合，既能保证运动的语义合理性，又能实现细粒度的空间操控，是通向实用化运动生成的关键路径。

### 现有方法的瓶颈

当前支持空间控制的运动生成方法主要存在以下瓶颈：

**精度与语义的冲突。** 以 **OmniControl**（Xie et al., arXiv 2023）为代表的扩散模型方法，通过在采样过程中注入空间引导信号来实现轨迹跟随。然而，扩散模型的连续潜在空间缺乏对人体运动结构的显式建模，导致轨迹跟随精度与运动语义保持之间存在根本性冲突——强化空间约束往往以牺牲运动自然度为代价。在 HumanML3D 测试集上，当控制全部六个关节时，OmniControl 的轨迹误差高达 75.59%，平均关节位置误差达 23.67 cm，同时 FID 恶化至 2.614（Table 1）。

**推理效率的严重不足。** 扩散模型依赖多步迭代去噪（通常需要数十至上百步），每帧推理时间达到 0.606 s（OmniControl），远不能满足交互式应用对实时性的要求。即使 **GMD**（Karunratanakul et al., ICCV 2023）和 **PriorMDM**（Shafir et al., arXiv 2023）等方法在控制维度上有所简化，其效率瓶颈依然存在。

**多关节控制的灵活性缺失。** 现有方法在同时控制多个身体部位时性能急剧退化。这源于它们缺乏对身体部位间运动解耦的显式建模——当多个关节的轨迹约束同时施加时，扩散模型的引导信号相互干扰，导致优化陷入局部不自然解。

### 本文动机

上述瓶颈的本质在于：现有方法在**连续、非结构化的运动表示空间**中进行轨迹控制，缺乏对人体运动固有组合结构的利用。人体运动天然具有部位级的分化特性——手臂、腿部、头部等部位的运动在保持整体协调的同时具有局部独立性。

TLControl 的核心动机是：**将人体运动分解为多个身体部位的离散潜在表示，在紧凑且结构良好的潜在空间中进行轨迹跟随优化**。这一设计使得轨迹控制可以在不破坏整体运动语义的前提下进行——每个部位的潜在代码独立编码其运动模式，优化时仅需调整受控部位的代码，其他部位自动保持语义一致性。同时，离散潜在空间的紧凑性使得测试时优化仅需少量迭代即可收敛，从根本上突破了扩散模型多步采样的效率瓶颈。



## 核心方法与创新机理

TLControl 的核心创新在于**将人体运动生成从连续扩散采样范式迁移到分体式离散潜在空间中的测试时优化范式**，从而在轨迹控制精度、语言语义保真度与推理效率三个维度同时实现突破性提升。

### 瓶颈诊断：扩散模型的“精度-语义-效率”不可能三角

现有基于扩散模型的方法（如 **MDM**（Tevet et al., arXiv 2022）、**PriorMDM**（Shafir et al., arXiv 2023）、**GMD**（Karunratanakul et al., ICCV 2023）以及并发工作 **OmniControl**（Xie et al., arXiv 2023））面临一个结构性困境：要在扩散采样过程中施加精确的空间控制，通常需要解析梯度引导或特征注入，但这会破坏扩散模型原本学习到的运动分布，导致生成运动的语义质量（FID、R‑precision）急剧下降。与此同时，扩散模型的多步迭代采样（通常几十到上百步）带来严重的计算开销，难以满足交互式应用需求。Table 1 的数据清晰地揭示了这一困境：OmniControl 在控制全部六个关节时，轨迹误差高达 75.59%，FID 恶化至 2.614，而推理速度仅 0.606 s/frame。

### 核心洞察：分体式离散潜在空间作为控制与语义的解耦界面

TLControl 的关键洞察是：**将人体运动按身体部位分解为多个独立的离散潜在表示，可以构造一个“控制-语义解耦”的优化界面**。在这一紧凑、结构良好的潜在空间中，轨迹跟随优化可以在不破坏整体运动语义的前提下进行——优化仅调整局部关节的潜在代码，而其他部位和运动的时间结构得以保持。

具体而言，TLControl 通过以下三个 **changed slots** 实现了这一范式转换：

**1. 运动潜在表示：从统一连续空间到分体式离散 VQ‑VAE 空间**

基线方法依赖扩散模型的连续潜在空间或统一的全身体 VQ‑VAE 潜在空间，控制信号在其中的传播缺乏结构约束。TLControl 将人体运动划分为六个关节组（Head, Left arm, Right arm, Left leg, Right leg, Root），为每个部位训练独立的编码器与码本（Sec. 3.1, Fig. 2）：

$$\hat{\mathbf{q}}_{t,k} = \arg\min_{\mathbf{c}_{i,k}\in\mathbf{C}_k} \|\mathbf{c}_{i,k} - \mathbf{q}_{t,k}\|_2$$

这一设计的优势在消融实验中得到充分验证：相比统一 VQ‑VAE，分体式设计将控制所有关节时的平均误差从 2.51 cm 降至 1.57 cm，同时运行时间降低 27.3%（Supplementary Table 1, Supplementary Fig. 1）。其因果机制在于：分体式码本使得每个部位的潜在代码在语义上独立可控，优化某一关节的轨迹时不会通过共享的潜在空间干扰其他部位的运动。

**2. 轨迹条件化与初始预测：从扩散引导到 Masked Trajectory Transformer 粗预测**

基线方法在扩散采样过程中施加控制信号，控制精度受限于每一步的去噪动态。TLControl 引入 **Masked Trajectory Transformer（MTT）**，结合连续轨迹掩码和关节级掩码，从文本描述和部分轨迹一次性预测所有部位的离散潜在代码索引（Sec. 3.2, Fig. 2）：

$$\mathcal{L} = \mathbb{E}_{\hat{I}\sim P(I)} [-\log P(\hat{I}|R',L)] + \|\mathcal{D}(\hat{\mathbf{Q}}_0) - \mathbf{J}\|_2$$

MTT 的粗预测为后续优化提供了一个语义合理且已大致对齐的初始点，大幅降低了优化的搜索难度。实验表明，即便在 75% 轨迹被掩码的极端情况下，MTT 输出的 FID 仍远优于 OmniControl 在全轨迹下的表现（Supplementary Fig. 2, Table 3）。

**3. 精化机制：从多步扩散采样到测试时潜在空间优化**

这是 TLControl 效率优势的根本来源。扩散模型需要几十到上百步的迭代去噪，而 TLControl 以 MTT 输出为初始点，在紧凑的离散潜在空间中进行测试时优化（使用 L‑BFGS 算法），仅需少量迭代即可达到精准对齐（Sec. 3.3）：

$$\hat{\mathbf{Q}} = \arg\min_{\mathbf{Q}} \Sigma_j \|\mathcal{P}_j(\mathcal{D}(\mathbf{Q})) - \mathbf{R}'_j\|_2$$

这一设计的决定性证据来自 Table 4：TLControl 的推理速度（0.015 s/frame）比 OmniControl（0.606 s/frame）快约 40 倍，也远快于 MDM 和 GMD。消融实验进一步表明，在潜在空间进行优化（Latent‑Opt）显著优于直接对关节进行 IK 调整（Joint‑IK），后者无法保持运动语义且对缺失帧无能为力（Supplementary Table 3）。

### 创新效果的决定性验证

在 HumanML3D 数据集上控制全部六个关节时（Table 1），TLControl 实现了 **Traj.Err. 和 Loc.Err. 均为 0.00%** 的完美轨迹跟随，而 OmniControl 分别为 75.59% 和 12.30%；平均关节误差从 23.67 cm 降至 1.57 cm；FID 从 2.614 降至 0.032，R‑precision 从 0.606 提升至 0.794。在 KIT 数据集上（Table 2），Pelvis 控制的平均误差从 7.59 cm 降至 2.76 cm。这些结果表明，TLControl 成功打破了扩散模型面临的精度-语义-效率不可能三角。

### 局限与开放问题

TLControl 假设输入的语言描述与轨迹之间不存在冲突，且轨迹在物理上可行。当两者矛盾时（如语言要求“举起右手”而轨迹限制右手向下），模型未提供冲突消解机制。此外，测试时优化在极长序列或控制点稀疏的情况下可能陷入局部最优，导致语义漂移。该方法目前依赖固定骨架结构，扩展到非人形角色需重新训练。尽管如此，TLControl 所开辟的“分体式离散潜在空间 + 测试时优化”范式，为可控运动生成提供了新的方法论基础。



TLControl 的整体框架围绕一个核心洞察构建：**将人体运动分解为多个身体部位的离散潜在表示，可以在不破坏整体运动语义的前提下进行精确的轨迹跟随优化**。为此，该方法采用“神经预测 + 测试时优化”的混合范式，在分体式 VQ‑VAE 学习到的紧凑、结构良好的潜在空间中运作，其 pipeline 如 Fig. 2 所示，分为两个训练阶段和一个测试时优化阶段。

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/002_Figure_2.jpg]]
*Figure 2: Overview of TLControl framework: At training stage I, we train the part-based VQ-VAE in 3.1 for reconstructing human motions. In training stage II, the decoder of the part-based VQ-VAE is frozen and we train the masked trajectory transformer (MTT) in 3.2 for predicting code indices from control inputs. Finally, at test time, the MTT receives text description and partial control trajectories to predict an initial VQ-VAE quantized code seed, which is refined by run-time optimization as in 3.3 before decoding with the VQ-VAE into full body motions.remaking*

**输入与输出定义**。系统的输入为一个三元组 $(R', L, \mathbf{J})$，其中 $R'$ 是用户指定的部分关节轨迹（可包含任意关节组合、任意时间长度的控制点），$L$ 是描述运动语义的自然语言文本，$\mathbf{J} \in \mathbb{R}^{T \times M}$ 是目标全身运动序列（仅在训练时可用）。输出为满足轨迹约束且与语言描述语义一致的全身运动 $\hat{\mathbf{J}}$。

**阶段一：分体式 VQ‑VAE 训练（Sec. 3.1）**。框架首先将人体骨架按关节拓扑划分为六个独立部位：Head、Left arm、Right arm、Left leg、Right leg 和 Root。每个部位拥有独立的编码器 $\varepsilon_k$ 和码本 $\mathbf{C}_k$，将对应关节的运动特征 $\mathbf{Q}_k$ 压缩为离散潜在代码。量化过程通过最近邻查找完成：

$$\hat{\mathbf{q}}_{t,k} = \arg\min_{\mathbf{c}_{i,k}\in\mathbf{C}_k} \|\mathbf{c}_{i,k} - \mathbf{q}_{t,k}\|_2$$

训练损失由量化损失、承诺损失和全身重建损失的加权和构成：

$$\mathcal{L} = \Sigma_k (\beta \|\mathbf{sg}[\hat{\mathbf{Q}}_k] - \mathbf{Q}_k\|_2 + \|\hat{\mathbf{Q}}_k - \mathbf{sg}[\mathbf{Q}_k]\|_2) + \|\mathbf{J} - \hat{\mathbf{J}}\|_2$$

其中 $\mathbf{sg}[\cdot]$ 为 stop‑gradient 操作。为防止码本坍缩，训练中采用指数移动平均和码本重置技术。训练完成后，VQ‑VAE 的解码器 $\mathcal{D}$ 被冻结，后续阶段仅在其离散潜在空间中操作。

**阶段二：掩码轨迹 Transformer 训练（Sec. 3.2）**。Masked Trajectory Transformer（MTT）接收文本特征（由冻结的 CLIP‑ViT‑B/32 提取）和部分轨迹 $R'$，通过交叉熵损失预测所有六个部位在每一时间步的码本索引：

$$\mathcal{L} = \mathbb{E}_{\hat{I}\sim P(I)} [-\log P(\hat{I}|R',L)] + \|\mathcal{D}(\hat{\mathbf{Q}}_0) - \mathbf{J}\|_2$$

MTT 同时施加连续轨迹掩码和关节级掩码，使模型学会从稀疏、不完整的轨迹输入中推断合理的全身运动分布，输出一个粗粒度的初始潜在代码 $\hat{\mathbf{Q}}_0$。

**测试时优化（Sec. 3.3）**。推理时，MTT 根据用户提供的 $R'$ 和 $L$ 一次性预测初始潜在代码，随后在该紧凑潜在空间中进行测试时优化（L‑BFGS），直接最小化解码后关节位置与目标轨迹之间的欧氏距离：

$$\hat{\mathbf{Q}} = \arg\min_{\mathbf{Q}} \Sigma_j \|\mathcal{P}_j(\mathcal{D}(\mathbf{Q})) - \mathbf{R}'_j\|_2$$

其中 $\mathcal{P}_j$ 为从全身运动中提取第 $j$ 个受控关节位置的投影算子。由于分体式潜在空间已编码了运动的自然分布，优化仅需少量迭代即可达到亚厘米级精度，同时保持运动语义的连贯性。优化收敛后，$\mathcal{D}(\hat{\mathbf{Q}})$ 即为最终输出的全身运动。

**模块间数据流总结**。训练阶段一：$\mathbf{J} \to$ 分体编码器 $\to \mathbf{Q}_k \to$ 量化 $\to \hat{\mathbf{Q}}_k \to$ 解码器 $\to \hat{\mathbf{J}}$；训练阶段二：$(R', L) \to$ MTT $\to \hat{\mathbf{Q}}_0 \to$ 冻结解码器 $\to \hat{\mathbf{J}}$；测试阶段：$(R', L) \to$ MTT $\to \hat{\mathbf{Q}}_0 \to$ 潜在空间优化 $\to \hat{\mathbf{Q}} \to$ 冻结解码器 $\to \hat{\mathbf{J}}$。整个流程中，VQ‑VAE 的解码器始终作为可微的运动生成器，将离散潜在代码映射回全身运动，从而在优化回路中保持端到端的可微性。



TLControl 的核心架构由三个关键模块构成，分别对应分体式运动压缩、粗粒度轨迹-语言联合预测，以及测试时潜在空间精化。以下逐一阐述其设计逻辑与数学形式。

### 分体式 VQ‑VAE（Part‑based VQ‑VAE）

**设计动机**：现有方法通常将人体运动编码为统一的连续或离散潜在表示，这导致在施加空间控制时，对局部关节轨迹的调整容易破坏整体运动语义。TLControl 的核心洞察在于将人体运动分解为多个身体部位的离散潜在表示，使得轨迹跟随优化可以在不破坏整体运动语义的前提下进行。

**模块结构**：模型将人体骨架划分为六个关节组——头部（Head）、左臂（Left arm）、右臂（Right arm）、左腿（Left leg）、右腿（Right leg）以及根关节（Root）。每个关节组配备独立的编码器 $\varepsilon_k$ 和码本 $\mathbf{C}_k$，其中 $k \in \{\text{Head}, \text{Lhand}, \text{Rhand}, \text{Lfoot}, \text{Rfoot}, \text{Root}\}$。给定某一关节组的运动序列 $\mathbf{J}_k$，编码器首先将其映射为时间特征序列，再通过时间下采样（因子 $s=4$）得到紧凑的潜在特征 $\mathbf{Q}_k$。

**量化过程**：对每个时间步 $t$ 的特征 $\mathbf{q}_{t,k}$，在对应码本中查找最近邻，获得量化后的特征 $\hat{\mathbf{q}}_{t,k}$：

$$\hat{\mathbf{q}}_{t,k} = \arg\min_{\mathbf{c}_{i,k}\in\mathbf{C}_k} \|\mathbf{c}_{i,k} - \mathbf{q}_{t,k}\|_2 \tag{1}$$

所有部位的量化特征拼接后送入统一的解码器 $\mathcal{D}$，重建全身运动 $\hat{\mathbf{J}}$。

**训练损失**：分体式 VQ‑VAE 的优化目标由三部分构成——量化损失（codebook loss）、承诺损失（commitment loss）与全身重建损失：

$$\mathcal{L} = \Sigma_k \left( \beta \|\mathbf{sg}[\hat{\mathbf{Q}}_k] - \mathbf{Q}_k\|_2 + \|\hat{\mathbf{Q}}_k - \mathbf{sg}[\mathbf{Q}_k]\|_2 \right) + \|\mathbf{J} - \hat{\mathbf{J}}\|_2 \tag{2}$$

其中 $\mathbf{sg}[\cdot]$ 表示停止梯度算子，$\beta$ 为承诺损失权重。为防止码本坍塌，训练中采用指数移动平均更新码本向量，并执行码本重置。

### 掩码轨迹 Transformer（Masked Trajectory Transformer, MTT）

**设计动机**：在获得结构良好的离散潜在空间后，需要一个能够从稀疏控制信号（部分轨迹 + 文本描述）中快速预测初始运动种子的生成模型。MTT 的设计目标是一次性预测所有身体部位的码本索引，为后续精化提供粗粒度的起点。

**输入与掩码策略**：MTT 接收两个控制信号——文本描述 $L$（经冻结的 CLIP‑ViT‑B/32 预处理）和部分轨迹 $\mathbf{R}'$。轨迹输入采用两种掩码机制：（1）连续轨迹掩码，模拟用户仅指定部分时间段的轨迹；（2）关节级掩码，模拟用户仅控制部分关节。

**训练损失**：MTT 以交叉熵损失预测各部位各时间步的码本索引 $\hat{I}$，同时辅以重建损失监督解码后的运动质量：

$$\mathcal{L} = \mathbb{E}_{\hat{I}\sim P(I)} [-\log P(\hat{I}|\mathbf{R}', L)] + \|\mathcal{D}(\hat{\mathbf{Q}}_0) - \mathbf{J}\|_2 \tag{3}$$

其中 $\hat{\mathbf{Q}}_0$ 为由预测索引查表得到的初始量化特征，$\mathcal{D}$ 为冻结的 VQ‑VAE 解码器。训练阶段 VQ‑VAE 的解码器参数完全冻结，仅更新 MTT 的 Transformer 参数。

### 测试时潜在空间优化（Test‑time Latent Optimization）

**设计瓶颈**：MTT 的粗预测虽能保持运动语义，但在轨迹精度上存在偏差。传统扩散模型需多步采样（数十至上百步）来逐步对齐控制信号，耗时严重。TLControl 的关键创新在于将精化过程转移到紧致的离散潜在空间中进行测试时优化，以极少的迭代步数实现精确对齐。

**优化目标**：以 MTT 输出 $\hat{\mathbf{Q}}_0$ 为初始点，在连续松弛的潜在空间（通过 Gumbel‑Softmax 可微化离散查表操作）中，最小化解码后关节位置与用户指定轨迹之间的欧氏距离：

$$\hat{\mathbf{Q}} = \arg\min_{\mathbf{Q}} \sum_j \|\mathcal{P}_j(\mathcal{D}(\mathbf{Q})) - \mathbf{R}'_j\|_2 \tag{4}$$

其中 $\mathcal{P}_j$ 为从全身运动中提取第 $j$ 个受控关节位置的投影算子，$\mathbf{R}'_j$ 为对应的目标轨迹。

**优化实现**：采用 L‑BFGS 优化器，仅需少量迭代即可收敛。消融实验表明，提高优化精度标准（如从 $10^{-4}$ 提升至 $10^{-8}$）可将平均关节误差从 6.72 cm 降至 0.54 cm，但相应增加优化时间（Table 5）。与直接在关节空间进行逆运动学调整（Joint‑IK）相比，潜在空间优化在轨迹掩码情况下能显著保持运动语义，且对缺失帧具有天然的补全能力（Supplementary Table 3）。

**效率优势**：由于优化发生在紧凑的潜在空间而非高维关节空间，且以 MTT 的良好初始预测为起点，单帧推理仅需 0.015 s，相比 OmniControl（0.606 s/frame）快约 40 倍（Table 4）。消融实验进一步表明，分体式 VQ‑VAE 相较于统一 VQ‑VAE 将运行时间降低 27.3%（Supplementary Table 1, Supplementary Fig. 1）。



## 实验与关键发现

### 核心实验设置

实验主要在 **HumanML3D**（14,616 个序列，44,970 条文本描述）和 **KIT‑ML**（3,911 个序列，6,278 条文本描述）两个数据集上进行。评估指标沿用 OmniControl 和 MDM 的设定，覆盖运动质量与空间控制精度两个维度：

- **运动质量**：FID↓、R‑precision↑（Top‑3）、Diversity、MModality
- **空间精度**：Traj.Err.↓（50 cm 阈值，%）、Loc.Err.↓（50 cm 阈值，%）、Avg.Err.↓（cm）

所有对比方法均使用官方实现或论文汇报的最佳结果，运行时间比较在相同硬件（RTX 4090）和批量大小（32）下进行。

### 主实验结果

#### HumanML3D 上的量化对比

Table 1 报告了在 HumanML3D 测试集上控制不同关节组合的结果。当控制全部六个关节时，TLControl 展现出压倒性优势：

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/006_Table_1.jpg]]
*Table 1: Quantitative results of comparison with state-of-the-art methods on Humanml3D test set. The best scores are highlighted in red*

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/014_Table_1.jpg]]
*Table 1: Quantitative results of comparison with different embedding design on Humanml3D test set. The best results are highlighted in red*

- **轨迹精度**：Traj.Err. 和 Loc.Err. 均为 **0.00%**，而最强基线 OmniControl 分别为 75.59% 和 12.30%。Avg.Err. 仅 **1.57 cm**，OmniControl 高达 23.67 cm。
- **运动质量**：FID 从 OmniControl 的 2.614 降至 **0.032**，R‑precision（Top‑3）从 0.606 提升至 **0.794**。这表明 TLControl 在精确跟随轨迹的同时，不仅没有破坏运动语义，反而生成了更自然的运动。

当仅控制骨盆（Pelvis）轨迹时，TLControl 同样取得 Traj.Err. 和 Loc.Err. 均为 0.00%，FID 0.031，R‑precision 0.798，全面优于所有基线方法（MDM、PriorMDM、GMD、OmniControl）。

#### KIT 上的泛化表现

Table 2 显示在 KIT 测试集上控制骨盆轨迹时，TLControl 的 Avg.Err. 为 **2.76 cm**，显著低于 OmniControl 的 7.59 cm。FID 从 OmniControl 的 0.831 降至 **0.061**，R‑precision 从 0.716 提升至 **0.799**。这验证了方法在不同数据集和运动分布上的泛化能力。

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/007_Table_2.jpg]]
*Table 2: Quantitative results of comparison with state-of-the-art methods on KIT test set. The best scores are highlighted in red*

#### 推理效率

Table 4 报告了各方法的每帧推理时间。TLControl 仅需 **0.015 s/frame**，比 OmniControl（0.606 s/frame）快约 **40 倍**，也远快于 MDM（26.241 s/frame）和 GMD（0.022 s/frame，但仅支持根轨迹控制）。这一效率优势源于在紧凑潜在空间中进行测试时优化，避免了扩散模型的多步迭代采样。

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/011_Table_4.jpg]]
*Table 4: Runtime of different methods*

### 消融实验

#### 分体式 VQ‑VAE 的关键作用

Supplementary Table 1 对比了分体式（part‑based）VQ‑VAE 与统一（unsplit）VQ‑VAE 在控制所有关节时的表现。分体式设计将 Avg.Err. 从 2.51 cm 降至 **1.57 cm**，同时 FID 更低、R‑precision 更高。Supplementary Fig. 1 进一步显示，分体式嵌入的每批运行时间减少了 **27.3%**。这表明按身体部位分解潜在空间既提升了控制精度，又降低了优化搜索的复杂度。

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/015_Figure_1.jpg]]
*Figure 1: Per batch running time statistics of our embedding comparing to the unsplit embedding. “Upper Body” includes the joints of the hands and the head joint. “Lower Body” includes the joints of two feet and the joint of the pelvis*

#### 优化精度与误差的权衡

Table 5 展示了控制所有关节时，优化精度标准（accuracy criteria）对最终关节误差的影响。将精度标准从 $10^{-4}$ 收紧至 $10^{-8}$，Avg. Joint Error 从 6.72 cm 降至 **0.54 cm**，但优化时间相应增加。这为用户提供了精度与速度之间的可调旋钮。

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/013_Table_5.jpg]]
*Table 5: Average Joint Error v.s. Accuracy criteria during optimization when controlling all the joints*

#### 轨迹掩码比例的影响

Table 3 和 Supplementary Fig. 2 报告了不同轨迹掩码比例下的运动多样性（MModality）和质量（FID、R‑precision）。随着掩码比例增加，性能平稳下降，但即便在 **75% 轨迹被掩盖**的极端情况下，FID 仍远优于 OmniControl 在完整轨迹下的表现（FID 2.614）。这证明了 MTT 粗预测与潜在空间优化的组合对不完整轨迹具有强鲁棒性。

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/009_Table_3.jpg]]
*Table 3: The MModality of the generated motions under different trajectory masking rates*

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/019_Table_3.jpg]]
*Table 3: Quantitative results of comparing IK based solution*

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/017_Figure_2.jpg]]
*Figure 2: Influence of different trajectory incompleteness. We simulate the incompleteness by applying random masking. The left vertical axis represents the FID metric, while the right vertical axis indicates the R-precision metric*

#### 潜在空间优化 vs. 关节级 IK

Supplementary Table 3 将 TLControl 的潜在空间优化（Latent‑Opt）与直接在关节空间进行逆运动学调整（Joint‑IK）进行了对比。在轨迹掩码场景下，Joint‑IK 无法处理缺失帧，且即使有完整轨迹，其生成的运动也严重破坏语义连贯性。潜在空间优化在所有指标上均显著优于 Joint‑IK，验证了在紧致潜在流形内搜索的必要性。

#### 单一模态兼容性

Supplementary Fig. 4 展示了仅使用语言或仅使用轨迹作为输入时的生成结果。TLControl 在单一模态下仍能生成高质量运动，表明模型并非强制依赖双模态输入，具有良好的兼容性。

### 定性结果

Fig. 3 展示了 TLControl 在用户自定义轨迹下的多关节同时控制能力，以及语言与轨迹的独立控制能力。Fig. 4 展示了 3D 手绘轨迹和楼梯脚步放置等实际应用场景。Fig. 5 和 Fig. 7 的定性对比中，TLControl（黄色）生成的运动在轨迹跟随精度和姿态自然度上均明显优于 OmniControl（绿色）。Fig. 6 展示了相同控制输入下 TLControl 能够生成多样化的运动样本。

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison results with Omnicontrol [62]. Our results are shown in Yellow, while the results of Omnicontrol are depicted in Green. Please refer to our supplementary video for more details of the comparison*

![[assets/figures/papers/paper_list_l1881_TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative comparison with Om*

### 失败模式与局限

尽管整体表现优异，TLControl 仍存在以下局限：

1. **输入冲突假设**：方法假设语言描述与轨迹线之间不存在矛盾，且轨迹本身物理可行。当语言要求“举起右手”而轨迹限制右手向下时，系统未定义优先级或折衷策略。
2. **分布外泛化**：模型在训练数据覆盖的运动类型上表现良好，但对极其罕见或分布外的轨迹，优化可能无法收敛到自然运动。
3. **长序列与稀疏控制**：在非常长的序列或控制点极少的情况下，测试时优化可能陷入局部最优，导致语义漂移。
4. **骨架限制**：当前模型基于训练所用的固定骨架（SMPL/CMU 拓扑），直接扩展到非人形角色或不同关节拓扑需要重新训练。
5. **实时性边界**：虽然每帧 0.015 s 已很快，但在 VR 手柄输入等要求毫秒级反馈的场景中，仍需专用加速或进一步优化。



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

现有基于扩散模型的人体运动生成方法（如 **MDM** (Tevet et al., arXiv 2022)、**PriorMDM** (Shafir et al., arXiv 2023)、**GMD** (Karunratanakul et al., ICCV 2023)）面临一个根本性瓶颈：**难以在保持语言语义的同时精确跟随多关节部分轨迹**。这些方法通常在扩散采样过程中通过解析空间引导或特征注入施加控制，但控制精度与运动自然度之间存在难以调和的矛盾——强化轨迹约束往往导致语义丢失或运动失真。此外，扩散模型的多步迭代采样（通常需要数十至上百步）耗时严重，无法满足交互式应用需求。

TLControl 的核心因果机制在于：**将人体运动分解为多个身体部位的离散潜在表示，使得轨迹跟随优化可以在不破坏整体运动语义的前提下进行**。具体而言，该方法通过分体式 VQ‑VAE 学习到的紧凑、结构良好的潜在空间，以 Masked Trajectory Transformer（MTT）的粗预测为起点进行测试时优化，从而能够精确且灵活地控制任意关节轨迹。

### 2. 与已有工作的关系

#### 2.1 扩散模型路线

**MDM** (Tevet et al., arXiv 2022) 是首个基于扩散的运动生成模型，但仅支持文本控制，无法处理空间轨迹输入。**PriorMDM** (Shafir et al., arXiv 2023) 在此基础上引入空间控制信号，通过将轨迹条件注入扩散过程实现有限的关节控制。**GMD** (Karunratanakul et al., ICCV 2023) 则专门针对 2D 根轨迹控制设计，但控制范围局限于根关节，无法灵活扩展到多关节场景。TLControl 与这些工作的根本差异在于：它不依赖扩散模型的迭代采样过程来施加控制，而是将控制问题转化为在离散潜在空间中的优化问题，从而在精度和效率两个维度均实现显著提升。

#### 2.2 并发工作：OmniControl

**OmniControl** (Xie et al., arXiv 2023) 是支持灵活空间控制的并发工作，其设计目标与 TLControl 最为接近。然而，OmniControl 在精度和效率上存在明显不足：在 HumanML3D 数据集上控制全部六个关节时，OmniControl 的轨迹误差（Traj.Err.）高达 75.59%，而 TLControl 为 0.00%；平均关节误差（Avg.Err.）方面，OmniControl 为 23.67 cm，TLControl 仅为 1.57 cm（Table 1, All Joints above）。在运动质量上，TLControl 的 FID 从 OmniControl 的 2.614 降至 0.032，R‑precision（Top‑3）从 0.606 提升至 0.794。推理速度方面，TLControl（0.015 s/frame）比 OmniControl（0.606 s/frame）快约 40 倍（Table 4）。

造成这一差距的关键在于控制机制的差异：OmniControl 在扩散模型的连续潜在空间中进行空间引导，控制信号与运动语义的耦合较弱；而 TLControl 在分体式 VQ‑VAE 的离散潜在空间中进行优化，身体部位的结构化解耦使得局部轨迹调整不会污染其他部位的运动表示。

### 3. 方法的关键技术位点

TLControl 相对于上述基线的方法论创新体现在三个关键技术位点上：

| 技术位点 | 基线方法 | TLControl | 证据锚点 |
|---------|---------|-----------|---------|
| 运动潜在表示 | 基于扩散的连续潜在空间或统一的全身体 VQ‑VAE 潜在空间 | 基于身体部位（6 个独立编码器/码本）的离散 VQ‑VAE 潜在空间，获得紧凑且结构化的表示 | Sec. 3.1, Fig. 2 |
| 轨迹条件化与初始预测 | 在扩散模型的采样过程中通过解析空间引导或特征注入方式施加控制 | 使用 Masked Trajectory Transformer（MTT）结合连续轨迹掩码和关节级掩码，一次性预测粗粒度的潜在代码，并通过 Gumbel‑Softmax 生成初始运动 | Sec. 3.2, Fig. 2 |
| 精化机制 | 扩散模型需进行多步迭代采样（通常几十到上百步） | 以 MTT 输出为初始点，在紧凑潜在空间中进行测试时优化（L‑BFGS），仅需少量迭代即可达到精准对齐，大幅提升效率 | Sec. 3.3, Table 4 |

消融实验证实了分体式 VQ‑VAE 设计的关键作用：相比统一 VQ‑VAE，分体式设计在控制所有关节时将平均误差从 2.51 cm 降至 1.57 cm，且运行时间降低 27.3%（Supplementary Table 1, Supplementary Fig. 1）。

### 4. 适用边界与局限

TLControl 的有效性建立在以下前提假设之上：

1. **输入一致性假设**：模型假设输入的语言描述与轨迹线之间不存在冲突，且轨迹本身在物理上是可行的。实际应用中可能出现矛盾（如语言要求“举起右手”而轨迹限制右手向下），模型对此未做专门处理。

2. **训练分布依赖**：模型在训练数据（HumanML3D、KIT‑ML）所覆盖的运动类型上表现良好，但对极其罕见或分布外的轨迹，优化可能无法收敛到自然运动。

3. **固定骨架约束**：模型支持的身体结构和关节数量目前限于训练所用的固定骨架（典型 SMPL/CMU 骨架），直接扩展到非人形角色或不同拓扑需要重新训练。

4. **长序列与稀疏控制的退化**：测试时优化虽然高效，但在非常长的序列或极少控制点的情况下，可能导致局部最优或语义漂移。

5. **实时性边界**：交互式应用中，虽然每帧 0.015 s 的速度已很快，但若要求实时的反馈（如 VR 中的手柄输入），仍需进一步优化或专用加速。

### 5. 开放问题

1. **冲突处理机制**：如何有效处理语言与轨迹之间的冲突或优先级？例如，当语言描述与轨迹约束矛盾时，系统应如何折衷？这可能需要引入显式的优先级策略或冲突检测模块。

2. **跨骨架泛化**：模型能否在未见过的骨架或物体交互场景下保持精确控制？可否通过微调或零样本泛化扩展到多角色场景？这涉及潜在空间的可迁移性研究。

3. **优化收敛性理论保证**：测试时优化的收敛行为是否在理论上可保证？损失地形的局部最优是否会导致生成不自然的姿态？当前仅依赖经验验证（Table 5 显示提高优化精度标准可显著降低误差），缺乏理论分析。

4. **物理可信性增强**：是否可以将该方法与基于物理的仿真器结合，进一步提升运动的物理可信性？这有望解决当前纯数据驱动方法可能产生的物理不合理运动。

5. **方法泛化性**：能否将 TLControl 的优化框架泛化到其他生成模型（如基于扩散的模型），在保持精度的同时进一步降低训练成本？这涉及测试时优化范式在其他生成架构中的适用性验证。



## 原文 PDF

![[paperPDFs/ECCV_2024/TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis.pdf]]
