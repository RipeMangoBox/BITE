---
title: "Motion Mamba: Efficient and Long Sequence Motion Generation"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation.pdf
project_link: https://steve-zeyu-zhang.github.io/MotionMamba
code_link: null
aliases:
- MM
- MMELSMG
tags:
- ECCV_2024
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "引入选择性状态空间模型（Mamba）作为替代Transformer的核心骨架，并通过层次化时序扫描（HTM）和双向空间扫描（BSM）两个专用模块，在保持线性复杂度的同时提升长序列运动生成的精度与效率。"
primary_logic: "Mamba的线性时间复杂度和硬件感知设计可高效捕获长距离依赖；层次化扫描在不同抽象层调整SSM扫描次数，增强时序一致性；双向扫描促进潜在空间中的通道信息交换，提升空间细节建模；二者结合使运动生成在质量与速度上达到全新SOTA。"
claims:
- "在HumanML3D数据集上，Motion Mamba的FID达到0.281，较之前最优的扩散方法MLD（0.473）降低40.5%。"
- "推理速度比MLD快4倍，平均每条文本描述仅需0.058秒（MLD为0.217秒）。"
- "在专为长序列设计的HumanML3D‑LS上，FID为0.668，显著优于对比方法。"
- "消融实验证实层次化时序扫描与块级双向空间扫描均对生成质量至关重要。"
---

# Motion Mamba: Efficient and Long Sequence Motion Generation

> [!tip] 核心洞察
> Mamba的线性时间复杂度和硬件感知设计可高效捕获长距离依赖；层次化扫描在不同抽象层调整SSM扫描次数，增强时序一致性；双向扫描促进潜在空间中的通道信息交换，提升空间细节建模；二者结合使运动生成在质量与速度上达到全新SOTA。

| 字段 | 内容 |
|------|------|
| 中文题名 | Motion Mamba：高效长序列运动生成模型 |
| 英文题名 | Motion Mamba: Efficient and Long Sequence Motion Generation |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.07487) · [Project](https://steve-zeyu-zhang.github.io/MotionMamba) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | Motion Mamba |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID ↓ 为 0.281，对比 0.473 (MLD)，变化 −40.5%。
> - HumanML3D 上，R Precision Top‑1 ↑ 为 0.502，对比 0.481 (MLD)，变化 +4.4%。
> - HumanML3D 上，Average Inference Time (seconds) ↓ 为 0.058，对比 0.217 (MLD)，变化 −73.3% (4× faster)。

## 概要

**核心问题**：现有基于Transformer的扩散运动生成模型（如MLD、MDM）在处理长时序人体运动时，自注意力机制带来二次计算复杂度，导致推理速度慢且难以有效捕获长距离帧间依赖，成为制约运动生成质量与效率的关键瓶颈。

**核心方案**：Motion Mamba提出以选择性状态空间模型（Mamba）替代Transformer作为扩散去噪器的主干网络，并设计两个专用模块——层次化时序扫描（Hierarchical Temporal Mamba, HTM）与双向空间扫描（Bidirectional Spatial Mamba, BSM）——在保持线性时间复杂度的同时，分别增强时序一致性与空间细节建模能力。

**方法定位**：Motion Mamba属于基于潜在扩散的文本驱动运动生成方法，沿用了MLD（Chen et al., CVPR 2023）的VAE压缩-重建框架与CLIP文本编码器，但将去噪U-Net中的自注意力核心替换为Mamba驱动的HTM与BSM模块，形成一种“状态空间扩散”新范式。

**主要结果**：
- 在HumanML3D数据集上，Motion Mamba的FID达到**0.281**，较此前最优扩散方法MLD（0.473）降低**40.5%**（Table 1）。
- 推理速度比MLD快**4倍**，平均每条文本描述仅需**0.058秒**（MLD为0.217秒），在FID-AIT散点图上显著优于所有对比方法（Figure 4）。
- 在专为长序列设计的HumanML3D‑LS上，FID为**0.668**，显著优于对比方法，验证了其在长序列建模上的优势（Table 3）。
- 消融实验证实层次化时序扫描与块级双向空间扫描均对生成质量至关重要（Table 4）。

**方法谱系与知识库定位**：
- **上游继承**：潜在扩散框架与Motion VAE直接复用自**MLD**（Chen et al., CVPR 2023）；文本嵌入采用冻结的CLIP ViT‑B/32；运动评估编码器沿用**T2M**（Guo et al., ECCV 2022）的预训练模型。
- **核心创新**：将**Mamba**（Gu & Dao, 2023）选择性状态空间模型首次引入运动生成领域，并通过HTM的层次化扫描分配策略与BSM的双向潜在空间扫描实现时序与空间建模的协同优化。
- **下游影响**：为长序列运动生成、实时人机交互等场景提供了高效且高质量的基线，其“状态空间+扩散”的组合范式可推广至其他时序生成任务（如手势、舞蹈、动作预测）。

### 问题背景：文本驱动的人体运动生成

文本驱动的人体运动生成（Text-to-Motion）旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实、人机交互等领域具有重要应用价值。该任务的核心挑战在于：运动序列天然具有高维时空结构——每一帧包含多个关节的旋转/位置信息，而不同帧之间又存在复杂的时序依赖关系。一个有效的运动生成模型必须同时捕获**帧内的空间细节**（各关节的协调运动）和**帧间的时序一致性**（动作的连贯过渡）。

### 现有方法缺口：Transformer扩散模型的效率瓶颈

近年来，基于扩散模型（Diffusion Models）的运动生成方法取得了显著进展，代表性工作包括：

- **MDM**（Tevet et al., ICLR 2023）：直接在原始运动空间进行扩散去噪，采用Transformer作为去噪骨干网络；
- **MLD**（Chen et al., CVPR 2023）：引入运动VAE将运动序列压缩至低维潜在空间，在潜在空间执行扩散过程，大幅提升了生成效率，成为此前的最优方法；
- **MotionDiffuse**（Zhang et al., TPAMI 2024）：提出文本驱动的多层级扩散策略，进一步丰富了生成多样性。

上述方法的共同特征是以**Transformer的自注意力机制**作为去噪网络的核心组件。然而，自注意力的计算复杂度随序列长度呈**二次增长**（$\mathcal{O}(L^2)$，其中$L$为帧数），这带来了两个根本性瓶颈：

1. **长序列建模困难**：当运动序列超过一定长度时，自注意力的计算开销变得难以承受，限制了模型对长时序依赖关系的有效捕获。而HumanML3D等主流数据集的序列长度呈**长尾分布**（见Figure 3），大量动作序列超过190帧，对长序列建模能力有真实需求。

2. **推理速度受限**：即使MLD通过潜在空间压缩缓解了部分计算压力，其Transformer去噪器在推理时仍需逐帧执行自注意力计算，导致每句描述的平均推理时间达0.217秒，难以满足实时或大规模生成场景的需求。

### 核心动机：以选择性状态空间模型替代Transformer

针对上述瓶颈，**Motion Mamba**的核心动机是：**引入选择性状态空间模型（Mamba）作为扩散去噪器的骨干网络，从根本上将时序建模的计算复杂度从二次降为线性**。

Mamba模型（选择性SSM）具有两个关键优势使其天然适合长序列运动生成：

- **线性时间复杂度**：通过状态空间模型的递归/卷积形式，序列处理的计算成本与序列长度呈线性关系（$\mathcal{O}(L)$），消除了Transformer的二次瓶颈；
- **硬件感知设计**：Mamba的并行扫描算法和IO感知实现使其在GPU上具有极高的实际运行效率，推理速度显著优于同等规模的Transformer。

然而，直接将标准Mamba应用于运动生成的潜在扩散框架面临两个挑战：其一，如何在不同抽象层级有效捕获多尺度时序依赖；其二，如何在潜在空间内部增强不同通道（对应不同运动维度）之间的信息交互。Motion Mamba通过**层次化时序扫描（Hierarchical Temporal Mamba, HTM）**和**双向空间扫描（Bidirectional Spatial Mamba, BSM）**两个专用模块来应对这些挑战，在保持线性复杂度的同时实现了生成质量与推理速度的双重突破。

## 核心方法与创新机理

Motion Mamba 的核心创新在于**用选择性状态空间模型（Mamba）彻底替换扩散去噪器中的 Transformer 骨架**，从根本上解决了现有方法在处理长序列运动生成时面临的二次计算复杂度瓶颈。围绕这一骨架替换，论文设计了两个高度特化的模块——层次化时序扫描（HTM）与双向空间扫描（BSM）——分别在时序依赖建模和空间细节刻画两个维度上释放 Mamba 的线性复杂度优势。

### 1. 骨架替换：从 Transformer 到 Mamba

现有基于扩散的运动生成方法，如 **MLD**（Chen et al., CVPR 2023）与 **MDM**（Tevet et al., ICLR 2023），其去噪网络核心均采用多头自注意力机制。自注意力在序列长度 $T$ 上的计算复杂度为 $O(T^2)$，当处理 HumanML3D 数据集中大量超过 190 帧的长序列运动时（见 Figure 3 的长尾分布），推理速度和显存占用成为显著瓶颈。Motion Mamba 将去噪器 $\epsilon_\theta(x)$ 的骨架替换为基于 Mamba 的 U-Net 结构（Equation 3）：

$$\epsilon_\theta(x) \equiv \{E_{1\ldots N}, M, D_{1\ldots N}\}$$

其中 $N$ 个编码器块 $E_i$ 与 $N$ 个解码器块 $D_j$ 均由 HTM 和 BSM 两个模块构成，中间由基于 Transformer 的注意力混合器 $M$ 桥接。Mamba 的离散化状态更新（Equation 1）与全局卷积实现（Equation 2）保证了 $O(T)$ 的线性时间复杂度，同时其硬件感知的并行扫描设计使得实际推理速度大幅领先于自注意力方案。

### 2. 关键模块一：层次化时序扫描（HTM）

HTM 的设计直击时序一致性问题：不同抽象层对时序依赖的感知粒度不同，浅层需要细粒度帧间关系，深层则需要粗粒度的长程语义。HTM 通过**层次化分配扫描次数**来实现这一差异。

具体而言，HTM 定义了一个从高到低排列的扫描次数序列（Equation 4）：

$$K = \{S_{2N-1}, S_{2(N-1)-1}, \ldots, S_1\}$$

编码器第 $i$ 层和解码器第 $j$ 层分别按对称策略分配扫描次数（Equation 5-6）。编码器首层和解码器末层获得最多的 $S_{2N-1}$ 次扫描，中间层扫描次数逐层递减，最深层的编码器末层与解码器首层仅执行 $S_1$ 次扫描。这种对称分配确保了编码器-解码器架构中信息流动的平衡性。每层内部，多个独立的 SSM 扫描结果通过线性投影聚合，形成该层的时序表示。

消融实验（Table 4）证实，这种层次化扫描策略显著优于均匀扫描配置，是 FID 从基线提升至 0.281 的关键因素之一。

### 3. 关键模块二：双向空间扫描（BSM）

BSM 解决的是潜在空间内部的空间信息交换问题。在潜在扩散框架中，运动序列被 VAE 压缩至低维潜在表示，其通道维度编码了丰富的空间结构信息。BSM 首先将输入张量从 $(T, B, C)$ 重排为 $(C, B, T)$，即交换时序维度与通道维度，使 Mamba 的 SSM 扫描沿通道方向进行。随后，BSM 执行前向与后向两次扫描，并将双向结果融合，从而促进通道间的信息流动。

消融实验（Table 4）表明，**块级双向扫描**（block-based BiScan）在 BSM 中取得了最优 FID 0.281，优于单向扫描和其他双向变体。这一设计使得模型在保持时序一致性的同时，能够更精确地刻画单帧内的姿态细节。

### 4. 潜在维度选择的意外发现

一个值得注意的设计选择是**潜在维度设为 2**（而非直觉上的维度 1）。消融实验（Table 4）明确显示，维度 2 的 FID 为 0.281，显著优于维度 1 的表现。论文未对此提供详细理论解释，但这一发现暗示：在 Mamba 的 SSM 扫描框架下，适当扩展潜在表示的通道容量有助于 BSM 模块更有效地进行空间信息交换，而不会引入 Transformer 式的计算膨胀。

### 创新点小结

Motion Mamba 的创新可归纳为三个 **changed slots**：

| 模块 | 基线方案（MLD/MDM） | Motion Mamba 方案 | 证据锚点 |
|------|---------------------|-------------------|----------|
| **去噪器骨架** | Transformer（多头自注意力） | Mamba-based（HTM + BSM 块） | Section 3.2, Figure 2 |
| **时序建模策略** | 标准帧间自注意力 | 层次化时序扫描（HTM），每层分配不同 SSM 扫描次数 | Section 3.2, Equations (4)-(6) |
| **空间建模策略** | 同自注意力覆盖关节/通道维度 | 双向空间扫描（BSM），沿潜在维度执行前向+后向扫描 | Section 3.2, Figure 2 |

三者协同作用使 Motion Mamba 在 HumanML3D 上以 0.281 的 FID 刷新 SOTA，同时推理速度达到 MLD 的 4 倍（0.058s vs 0.217s，Figure 4），在长序列数据集 HumanML3D-LS 上亦取得 0.668 的 FID（Table 3），验证了线性复杂度骨架在长序列运动生成场景中的决定性优势。

Motion Mamba 的整体 pipeline 延续了潜在扩散模型（Latent Diffusion）的基本范式，但在去噪骨干网络上进行了根本性的替换。其核心流程如下：给定一条文本描述，首先通过冻结的 **CLIP 文本编码器**（ViT‑B/32）提取文本嵌入；同时，一段运动序列经由复用的 **Motion VAE** 编码器压缩到低维潜在空间，得到潜在表示 $z_0$。扩散过程在该潜在空间中对 $z_0$ 逐步加噪，生成噪声潜在变量 $z_t$；随后，**去噪 U‑Net** 以 $z_t$、时间步 $t$ 和文本嵌入为条件，预测所添加的噪声，从而逐步恢复出干净的潜在运动表示。最后，Motion VAE 解码器将该潜在表示重建为完整的运动序列。

上述流程中，最关键的创新在于去噪 U‑Net 的内部结构。该网络由 $N$ 个编码器块 $\{E_1, \dots, E_N\}$、一个基于 Transformer 的注意力混合器 $M$ 和 $N$ 个解码器块 $\{D_1, \dots, D_N\}$ 组成（见公式 3）：

$$\epsilon_{\theta}(x) \equiv \{E_{1\ldots N}, M, D_{1\ldots N}\}$$

每个编码器块和解码器块内部均包含两个专用模块——**层次化时序 Mamba（HTM）块**和**双向空间 Mamba（BSM）块**，分别负责时序依赖建模与空间细节增强。编码器逐层提取特征并下采样，混合器 $M$ 在瓶颈层整合文本条件信息，解码器则对称地上采样并恢复运动细节，其间通过跳跃连接与对应编码器层相连，形成标准的 U‑Net 拓扑。

**输入输出流**可概括为：文本描述 → CLIP 文本嵌入；运动序列 → VAE 编码 → 潜在变量 $z_0$ → 扩散加噪 → $z_t$；$z_t$ + 文本嵌入 + 时间步 $t$ → 去噪 U‑Net（HTM + BSM 交替处理）→ 预测噪声 → 去噪得 $\hat{z}_0$ → VAE 解码 → 生成运动序列。这一设计将 Mamba 的线性复杂度优势引入扩散生成框架，使得长序列运动生成在效率与质量之间取得了显著平衡。

![[assets/figures/papers/paper_list_l12_Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation/figures/002_Figure_2.jpg]]
*Figure 2: This figure illustrates the architecture of the proposed Motion Mamba model. Each of encoder and decoder blocks consists of a Hierarchical Temporal Mamba block (HTM) and a Bidirectional Spatial Mamba (BSM) block, which possess hierarchical scan and bidirectional scan within SSM layers respectively. This symmetric distribution of scans ensure a balanced and coherence framework across the encoder-decoder architecture*

### 状态空间模型预备

Motion Mamba 的核心骨架建立在选择性状态空间模型（SSM）之上。SSM 通过一阶微分方程将输入序列 $x(t) \in \mathbb{R}$ 映射为输出序列 $y(t) \in \mathbb{R}$，经由隐藏状态 $h(t) \in \mathbb{R}^N$ 传递信息。为适配深度学习中的离散序列处理，需将连续参数 $\mathbf{A}, \mathbf{B}, \mathbf{C}$ 离散化。离散化后的状态更新方程为：

$$h_t = \overline{\mathbf{A}} h_{t-1} + \overline{\mathbf{B}} x_t, \quad y_t = \mathbf{C} h_t$$

其中 $\overline{\mathbf{A}}$ 和 $\overline{\mathbf{B}}$ 由零阶保持（ZOH）规则从连续参数导出。该递推形式可进一步重写为全局卷积，以实现高效的并行训练：

$$\overline{\mathbf{K}} = (\mathbf{C} \overline{\mathbf{B}}, \mathbf{C} \overline{\mathbf{A}} \overline{\mathbf{B}}, \ldots, \mathbf{C} \overline{\mathbf{A}}^{M-1} \overline{\mathbf{B}}), \quad \mathbf{y} = \mathbf{x} * \overline{\mathbf{K}}$$

Mamba 将 $\overline{\mathbf{B}}, \mathbf{C}$ 参数化为输入相关的函数，使模型具备选择性信息处理能力，同时保持线性时间复杂度。这一特性构成了 Motion Mamba 替代 Transformer 自注意力的理论基础。

### 去噪网络架构

Motion Mamba 的去噪网络 $\epsilon_\theta(x)$ 采用对称的 U-Net 结构，由 $N$ 个编码器块、一个注意力混合器 $M$ 和 $N$ 个解码器块组成：

$$\epsilon_{\theta}(x) \equiv \{E_{1\ldots N}, M, D_{1\ldots N}\}$$

每个编码器块 $E_i$ 和解码器块 $D_j$ 内部均包含两个核心模块：**层次化时序 Mamba（HTM）块**和**双向空间 Mamba（BSM）块**。HTM 负责沿时间轴建模帧间依赖，BSM 则在潜在空间维度上进行通道间的信息交换。

### 层次化时序扫描机制

HTM 的核心设计在于为 U-Net 不同深度分配不同数量的 SSM 扫描次数。其直觉是：浅层需要更多扫描以捕获细粒度时序细节，深层则聚焦于高层语义，所需扫描次数递减。扫描次数集合 $K$ 定义为从高到低的序列：

$$K = \{S_{2N-1}, S_{2(N-1)-1}, \ldots, S_1\}$$

编码器第 $i$ 层的扫描次数 $E_i(S)$ 分配规则为：

$$E_i(S) = \begin{cases} S_{2N-1} & \text{for } i=1 \\ S_{2(N-i)-1} & \text{for } i=2,\ldots,N-1 \\ S_1 & \text{for } i=N \end{cases}$$

解码器第 $j$ 层的扫描次数 $D_j(S)$ 与编码器呈对称分布：

$$D_j(S) = \begin{cases} S_{2N-1} & \text{for } j=N \\ S_{2(N-j)-1} & \text{for } j=N-1,\ldots,2 \\ S_1 & \text{for } j=1 \end{cases}$$

这种对称分配确保了编码器-解码器框架内时序建模的一致性与连贯性。每层内，HTM 块将输入序列沿时间维度展开，经过指定次数的独立 SSM 扫描后，通过线性投影聚合多个扫描结果得到最终输出。

### 双向空间扫描机制

BSM 块旨在增强潜在空间中的通道信息流动。其关键操作是维度重排：将输入张量从 $(T, B, C)$（时间、批次、通道）变换为 $(C, B, T)$，即将通道维度与时间维度交换。随后，在重排后的序列上分别执行前向和后向两次 SSM 扫描，以双向捕获空间依赖关系。消融实验（Table 4）证实，块级双向扫描（block-based BiScan）在 BSM 中取得了最优 FID 0.281，验证了该设计选择的有效性。

### 模块协同与训练目标

HTM 与 BSM 在编码器/解码器的每个层级中串联工作：HTM 首先处理时序一致性，BSM 随后精炼空间细节。注意力混合器 $M$ 位于瓶颈层，采用标准 Transformer 注意力实现跨模态信息融合。整个潜在扩散模型的训练目标是最小化潜在空间中真实噪声与预测噪声之间的均方误差（MSE），与 MLD（Chen et al., CVPR 2023）的训练范式保持一致。

## 实验与关键发现

### 主实验结果

Motion Mamba在标准文本驱动运动生成基准上取得全面领先。在HumanML3D数据集上，模型FID降至**0.281**，较此前最优扩散方法**MLD**（Chen et al., CVPR 2023）的0.473降低40.5%（Table 1）。R Precision Top‑1达到0.502，较MLD的0.481提升4.4%。在KIT‑ML数据集上同样展现出竞争力（Table 2）。

![[assets/figures/papers/paper_list_l12_Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation/figures/003_Table_1.jpg]]
*Table 1: Comparison of text-conditional motion synthesis on HumanML3D [17]. These metrics are evaluated by the motion encoder from [17]. Empty MModality indicates the non-diverse generation methods. We employ real motion as a reference and sort all methods by descending FIDs. The right arrow → means that the closer to the real motion, the better. Bold and underline indicate the best and second best result*

![[assets/figures/papers/paper_list_l12_Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation/figures/004_Table_2.jpg]]
*Table 2: We involve KIT-ML [38] dataset and evaluate the SOTA methods on the text-to-motion task*

![[assets/figures/papers/paper_list_l12_Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation/figures/007_Table_4.jpg]]
*Table 4: Evaluation of text-based motion synthesis on HumanML3D [17]: we use metrics in Table 1 and provides real reference, we evaluate the various HTM and BSM design choices, the dimension of the latent input, the different number of layer of Motion Mamba model*

效率方面，Motion Mamba平均每条文本描述的推理时间仅**0.058秒**，而MLD需0.217秒，加速约4倍（Figure 4）。这一速度优势来源于Mamba骨架的线性时间复杂度，使模型在保持高生成质量的同时大幅降低计算开销。

在专为长序列设计的**HumanML3D‑LS**数据集（仅包含超过190帧的运动序列）上，Motion Mamba的FID为0.668，显著优于对比方法（Table 3），验证了层次化时序扫描对长距离依赖的有效捕获。

![[assets/figures/papers/paper_list_l12_Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation/figures/005_Table_3.jpg]]
*Table 3: In order to evaluate the models’ capability in long sequence motion generation, we compared our method with an existing approach on the recently introduced HumanML3D-LS dataset. This dataset comprises motion sequences longer than 190 frames from the original evaluation set. Our model demonstrates superior performance compared to other methods*

### 消融实验

Table 4系统评估了HTM与BSM的设计选择、潜在维度及网络层数的影响。

**BSM设计**：块级双向扫描（block‑based BiScan）取得最优FID 0.281，优于单块扫描或标准双向扫描方案，证实分块处理在潜在空间通道信息交换中的关键作用。

**HTM设计**：层次化扫描次数分配（编码器从$S_{2N-1}$递减至$S_1$，解码器对称反向）优于均匀扫描分配，说明在不同抽象层差异化地投入SSM扫描资源对时序一致性的重要性。

**潜在维度**：维度2的FID为0.281，显著优于维度1的设置。这与传统VAE或SSM设计中偏好低维的直觉相悖，其内在机制尚待理论解释。

**网络层数**：11层配置取得最优FID 0.281和R Precision Top‑3 0.792，层数过少或过多均导致性能下降，可能分别源于表示能力不足与过拟合。

### 失败模式与局限

论文未单独讨论失败案例。当前评估限于HumanML3D和KIT‑ML两个标准数据集，对更复杂运动类型（如多人交互、精细手部动作）或真实应用场景的泛化能力尚待验证。模型依赖MLD的VAE结构进行运动压缩与重建，这可能限制了对其他运动表示格式的可迁移性。此外，块级双向扫描的内部工作机制缺乏详细理论分析，层次扫描次数的选择仍为手工预定义，是否可自适应学习是开放问题。

### 图表关键结论

- **Figure 1**：Motion Mamba在长序列建模与生成效率上显著优于MLD、MotionDiffuse（Zhang et al., TPAMI 2024）和MDM（Tevet et al., ICLR 2023）。
- **Figure 2**：展示编码器‑解码器对称架构中HTM与BSM模块的协作方式，层次化扫描与双向扫描分别作用于时序与空间维度。
- **Figure 4**：AIT‑FID散点图显示Motion Mamba以0.058秒推理时间和0.281 FID占据最优位置，实现质量与速度的双重突破。
- **Table 1**：HumanML3D上全面超越扩散与非扩散方法，MModality达3.060，表明生成多样性良好。
- **Table 3**：HumanML3D‑LS上FID 0.668，证实模型对长序列运动的建模优势。
- **Table 4**：消融实验确认块级双向扫描、层次化扫描分配、潜在维度2和11层网络为最优配置。

![[assets/figures/papers/paper_list_l12_Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation/figures/001_Figure_1.jpg]]
*Figure 1: Motion Mamba has achieved significantly superior performance on long squence modeling and motion generation efficiency compared with other well-designed state-of-the-art methods such as MLD [6], MotionDiffuse [54], and MDM [49]*

## 定位与知识库关联

### 核心瓶颈与因果杠杆

现有基于扩散模型的文本驱动运动生成方法，如 **MLD** (Chen et al., CVPR 2023) 和 **MDM** (Tevet et al., ICLR 2023)，普遍采用 Transformer 作为去噪骨干网络。Transformer 的自注意力机制在处理长序列时面临二次计算复杂度，导致两个关键瓶颈：其一，推理速度随序列长度急剧下降，难以满足实时或交互式应用需求；其二，长距离时序依赖关系的建模能力受限于计算资源，在长序列运动生成场景中表现退化。Motion Mamba 的核心因果杠杆在于将选择性状态空间模型（Mamba）引入扩散去噪过程，以线性时间复杂度替代自注意力，同时通过层次化时序扫描（HTM）和双向空间扫描（BSM）两个专用模块，在保持效率优势的前提下补偿 SSM 在时序一致性和空间细节建模上的潜在不足。

### 与基线方法的继承与变革关系

Motion Mamba 在整体框架上直接继承了 **MLD** (Chen et al., CVPR 2023) 的潜在扩散架构：使用冻结的 CLIP ViT‑B/32 提取文本嵌入，复用 MLD 的 Motion VAE（编码器‑解码器）进行运动序列的压缩与重建，并在潜在空间中执行扩散去噪。这一继承关系确保了与先前最优方法的公平可比性——所有实验采用相同的数据集划分、预处理流程和评估协议，均在单张 NVIDIA V100 GPU 上运行。

变革集中在去噪网络内部，体现在三个关键槽位的替换：

| 槽位 | 基线方案 (MLD/MDM) | Motion Mamba 方案 | 证据锚点 |
|------|-------------------|-------------------|----------|
| 去噪骨干网络 | Transformer（多头自注意力） | Mamba‑based（HTM + BSM 块） | Section 3.2, Figure 2 |
| 时序建模策略 | 标准逐帧自注意力 | 层次化时序扫描（HTM），每层分配不同数量的 SSM 扫描 | Section 3.2, Equations (4)–(6) |
| 空间建模策略 | 同一自注意力覆盖关节/通道维度（若有） | 双向空间扫描（BSM），在潜在维度上执行前向+后向扫描 | Section 3.2, Figure 2 |

与 **MotionDiffuse** (Zhang et al., TPAMI 2024) 等其他文本驱动扩散方法相比，Motion Mamba 的差异化优势在于其完全摒弃了 Transformer 组件，转而构建纯 Mamba 驱动的去噪 U‑Net。这种架构选择使其在长序列场景下的效率优势尤为突出——在专为长序列设计的 HumanML3D‑LS 数据集上，FID 达到 0.668，显著优于对比方法（Table 3）。

### 流水线模块与功能分工

Motion Mamba 的完整流水线由四个功能模块构成：

1. **CLIP 文本编码器**：将自然语言描述映射为固定维度的文本嵌入，作为扩散过程的条件信号。
2. **Motion VAE**（复用自 MLD）：将原始运动序列压缩至低维潜在空间（最优潜在维度为 2），并在推理阶段将去噪后的潜在表示解码回运动序列。
3. **去噪 U‑Net**：由 $N$ 个编码器块 $\{E_{1\ldots N}\}$、一个基于 Transformer 的注意力混合器 $M$ 和 $N$ 个解码器块 $\{D_{1\ldots N}\}$ 组成（Equation 3），每个编/解码器块内部包含一个 HTM 块和一个 BSM 块。
4. **HTM 与 BSM 块**：HTM 块以层次化递减的扫描次数处理时序信息——编码器首层分配 $S_{2N-1}$ 次扫描，逐层递减至末层的 $S_1$；解码器呈镜像对称分布（Equations 4–6）。BSM 块则将输入维度从 $(T, B, C)$ 重排为 $(C, B, T)$，在通道维度上执行双向 SSM 扫描，以促进潜在空间中的信息交换。

### 适用边界与泛化能力

当前验证范围限于 HumanML3D 和 KIT‑ML 两个标准基准数据集，涵盖文本条件运动合成任务。论文未提供在以下场景的实验证据：

- 更复杂的运动类型（如多人交互、物体操作、舞蹈编排）；
- 动作标签条件或音乐条件等非文本驱动模态；
- 真实应用场景（如动画制作、机器人控制）中的部署表现。

模型对 MLD 的 VAE 结构存在结构性依赖，这意味着运动表示的可迁移性受限于该 VAE 的压缩能力与泛化范围。若替换为其他运动表示（如 SMPL 参数、关节角度），需重新训练或适配 VAE，当前论文未提供相关分析。

### 开放问题与理论缺口

尽管实验证据充分（置信度 ≥ 0.9），以下问题仍缺乏深入的理论解释或实验探索：

1. **BSM 的空间信息编码机制**：块级双向扫描如何在潜在空间中编码空间信息流？其内部工作机制缺乏详细的理论分析，仅通过消融实验（Table 4）证实了块级双向扫描优于单向扫描和全局扫描，但未解释其信息流动的动力学原理。
2. **潜在维度的反直觉选择**：最优潜在维度为 2（FID 0.281），显著优于维度 1。这一发现与传统 VAE 或 SSM 的设计直觉相悖——通常更高维度提供更丰富的表示能力。为何维度 2 构成表示瓶颈与信息充分性的最优平衡点，论文未给出理论依据。
3. **层数与性能的非单调关系**：最优网络层数为 11（FID 0.281，R Precision Top‑3 0.792），但层数增减导致性能变化的具体原因（如过拟合、梯度消失或表示容量饱和）未予深入探讨。
4. **扫描次数的自适应学习**：层次扫描中每层的扫描次数 $\{S_{2N-1}, \ldots, S_1\}$ 当前为手工预定义。这些扫描次数是否可通过可微分搜索或元学习自适应确定，是一个值得探索的方向。
5. **长序列泛化的上限**：HumanML3D‑LS 仅包含超过 190 帧的序列，更极端长度（如 500+ 帧）下的性能退化模式尚未刻画。线性复杂度理论上支持任意长度，但实际感受野和状态记忆容量可能存在隐式约束。

### 知识库定位总结

Motion Mamba 在方法谱系中处于**潜在扩散运动生成**与**状态空间序列建模**的交叉点。它从 MLD 继承了完整的潜在扩散框架，但将核心去噪网络从 Transformer 替换为 Mamba 变体，实质上开创了“SSM 驱动的运动扩散”这一子方向。其层次化扫描和双向扫描的设计策略为后续工作提供了两个可独立改进的模块化组件——HTM 可被其他时序扫描策略替代，BSM 可被其他空间信息交换机制替换。论文未讨论局限性章节，上述开放问题需后续研究或手动验证加以填补。

## 原文 PDF

![[paperPDFs/ECCV_2024/Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation.pdf]]
