---
title: ScaMo Exploring the Scaling Law in Autoregressive Motion Generation Model
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Model.pdf
project_link: https://shunlinlu.github.io/ScaMo/
code_link: null
aliases:
- SSMGF
- SESLAMGM
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用有限标量量化（FSQ）替代VQ，消除了码本坍塌，使词汇量可任意扩展；同时构建大规模数据集MotionUnion，并设计文本前缀自回归模型（冻结T5-XL + 前缀双向注意力），使模型尺寸和训练计算均可按需缩放。
primary_logic: 通过在运动生成中首次应用FSQ并建立大规模数据与可扩展架构，验证了运动生成模型同样遵循缩放定律：归一化测试损失与计算预算（FLOPs）呈对数线性关系；非词汇参数、词汇参数、数据量分别与FLOPs满足幂律关系，且大模型与大词汇量呈强幂律耦合。
claims:
- 归一化测试损失 L_u 与 FLOPs C 符合对数定律，拟合公式为 L_u = -1.062 log10(C) + 13.839。
- "词汇参数 N_v 与非词汇参数 N_nv 满足幂律关系 N_v = 10^{-5.604} N_nv^{1.467} (R^2=0.95)，验证大模型需要大词汇。"
- FSQ 在重建精度、码本利用率、熵（编码均匀性）上全面优于 VQ，且随码本增大性能稳定提升，而 VQ 出现严重码本坍塌。
- 前缀注意力与 T5-XL 编码器显著优于 CLIP 无前缀方案，FID 从 0.226 降至 0.104。
---

# ScaMo Exploring the Scaling Law in Autoregressive Motion Generation Model

> [!tip] 核心洞察
> 通过在运动生成中首次应用FSQ并建立大规模数据与可扩展架构，验证了运动生成模型同样遵循缩放定律：归一化测试损失与计算预算（FLOPs）呈对数线性关系；非词汇参数、词汇参数、数据量分别与FLOPs满足幂律关系，且大模型与大词汇量呈强幂律耦合。

| 字段 | 内容 |
|------|------|
| 中文题名 | ScaMo：探索自回归运动生成模型中的缩放定律 |
| 英文题名 | ScaMo Exploring the Scaling Law in Autoregressive Motion Generation Model |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://shunlinlu.github.io/ScaMo/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ScaMo (Scalable Motion Generation Framework) |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.104 (ScaMo-343M, codebook 65536, T5-XL prefix) vs 0.226 (CLIP without prefix) (-0.122 (lower is better))；FID 0.104 (ScaMo-343M, codebook 65536) vs 0.166 (LargeMotionModel LLaMA-2-13B) (-0.062)；Top-1 R-Precision 0.510 (ScaMo-343M, codebook 65536) vs 0.402 (CLIP without prefix) (+0.108)。

## 概要

文本驱动的人体运动生成领域长期面临一个根本性瓶颈：无法验证缩放定律（Scaling Law）。与语言或视觉领域不同，运动生成模型的性能是否随模型规模、数据量和计算预算的增大而可预测地提升，此前一直是悬而未决的问题。这一困境源于三重障碍：**数据规模小且质量参差不齐**（主流基准HumanML3D仅约14k序列）、**传统向量量化（VQ）在增大码本时遭遇严重的码本坍塌**（codebook collapse），以及**模型架构扩展性不足**——直接套用大语言模型（LLM）或使用句子级CLIP嵌入均难以有效释放规模红利。

ScaMo针对上述瓶颈提出了系统性的解决方案，首次在运动生成领域验证了缩放定律的存在。其核心洞察在于：**通过有限标量量化（FSQ）取代VQ以消除码本坍塌，构建大规模运动-文本数据集MotionUnion（超260小时、约150k序列），并设计冻结T5-XL词级嵌入作为前缀的自回归Transformer架构**，三者协同使得模型尺寸、词汇量和训练计算可按需缩放。

实验揭示了清晰的缩放行为：归一化测试损失 $L_u$ 与计算预算 $C$（FLOPs）呈对数线性关系，拟合公式为 $L_u = -1.062 \log_{10}(C) + 13.839$（Figure 3(b)）。同时，词汇参数 $N_v$ 与非词汇参数 $N_{nv}$ 满足幂律关系 $N_v = 10^{-5.604} N_{nv}^{1.467}$（$R^2=0.95$），验证了“大模型需要大词汇”的强幂律耦合（Figure 3(a)）。此外，非词汇参数、词汇参数、数据量分别与FLOPs满足各自的幂律最优分配关系（Figure 7）。

在生成质量上，ScaMo-343M配合65536码本在HumanML3D基准上取得了FID 0.104的成绩，显著优于基于CLIP的无前缀方案（FID 0.226）以及基于LLaMA-2-13B的LargeMotionModel（FID 0.166）。FSQ在重建精度、码本利用率和编码均匀性上全面领先于VQ，且随码本增大性能稳定提升，而VQ在码本超过2048时即出现严重坍塌（Figure 6）。

**方法定位**：ScaMo属于运动离散化+自回归生成的范式，但其关键创新在于将FSQ引入运动量化、以T5-XL词级前缀替代句子级条件，并在大规模数据上系统性地研究缩放行为，而非简单地将LLM架构迁移到运动域。



文本驱动的人体运动生成旨在根据自然语言描述合成真实、多样且语义一致的三维人体动作序列，在动画制作、虚拟人交互、游戏开发等领域具有广泛的应用前景。近年来，受大型语言模型（LLM）成功的启发，研究者尝试将LLM直接引入运动生成任务，例如 **MotionGPT**、**MotionLLM**、**AvatarGPT** 和 **LargeMotionModel** 等工作分别基于 LLaMA-13B、Gemma-2b、LLaMA-13B 和 LLaMA-2-13B 等架构进行运动建模。然而，这类直接迁移LLM的方案面临一个根本性的瓶颈：**运动生成领域长期无法验证缩放定律（scaling law）**，即模型性能是否随计算预算、模型规模和数据规模的增大而可预测地提升。

造成这一困境的原因可归结为三个相互耦合的层面：

**数据瓶颈**：现有运动-文本数据集规模有限且质量参差不齐。主流基准 HumanML3D 仅包含约14k个运动序列，远不足以支撑大规模模型的训练。数据规模的匮乏直接限制了模型容量的扩展空间，使得缩放效应的观测缺乏必要的“燃料”。

**量化瓶颈**：自回归运动生成通常依赖向量量化（VQ）将连续运动序列离散化为离散token序列。然而，传统 VQ-VAE（如 **T2M-GPT** 所采用的方案）在增大码本尺寸时遭遇严重的**码本坍塌（codebook collapse）**——`arg min` 操作导致码本使用极不均匀，大部分码本条目在训练中从未被激活。这使得词汇量无法有效扩展，成为模型容量增长的硬性约束。

**架构瓶颈**：现有方法在文本条件建模上存在明显不足。基于 CLIP 句子级嵌入的自回归生成器（如标准方案）仅提供全局语义条件，缺乏细粒度的词级对齐能力；而直接引入LLM的方案虽具备强大的语言理解能力，但其架构并非为运动模态的离散token预测而设计，扩展效率低下。

上述三重瓶颈形成了一个“死锁”：没有大规模高质量数据，就无法训练大模型；没有可扩展的量化方法，大模型的容量优势无法通过大词汇量释放；没有适配的架构设计，文本与运动之间的细粒度对齐难以实现。打破这一僵局，需要在数据、量化和架构三个维度上同时进行系统性创新，这正是 ScaMo 工作的核心动机——**首次在运动生成领域建立可验证的缩放定律**，揭示模型性能与计算预算之间的定量关系，为未来更大规模的运动生成模型提供理论指导和实践路径。



## 核心方法与创新机理

### 瓶颈突破：从码本坍塌到可扩展词汇

文本驱动运动生成中长期无法验证缩放定律，根源在于三重瓶颈：

1. **数据瓶颈**：现有数据集（如 HumanML3D 仅 ~14k 序列）规模小且质量有限，不足以支撑大规模模型训练。
2. **量化瓶颈**：传统向量量化（VQ）依赖 arg min 操作匹配码本，随着码本增大出现严重的**码本坍塌**（codebook collapse）——大量码字闲置、编码熵降低、重建质量恶化，导致词汇量无法扩展。
3. **架构瓶颈**：直接引入 LLM 或使用句子级 CLIP 嵌入作为条件，均难以有效利用扩展后的模型容量和词汇量。

ScaMo 的核心突破在于**同时解决上述三个瓶颈**，形成可协同扩展的系统：大规模数据集 MotionUnion 提供数据基础，有限标量量化（FSQ）消除码本坍塌使词汇量可任意扩展，文本前缀自回归架构使模型尺寸和训练计算均可按需缩放。

### 关键方法槽位变更

#### 槽位一：量化方法 — 从 VQ 到 FSQ

| 维度 | 基线方案 | ScaMo 方案 |
|------|----------|------------|
| 量化机制 | 向量量化（VQ）：arg min 匹配码本，配合 EMA 更新和码本重置 | 有限标量量化（FSQ）：对编码器输出的有界潜在向量直接舍入（round），无需学习码本 |
| 训练损失 | 重建损失 + 承诺损失（commitment loss） | 仅重建损失，通过直通估计器（straight-through estimator）传递梯度 |
| 码本坍塌 | 码本 > 2048 时利用率骤降、熵降低、重建变差 | 码本从 256 至 65536 均保持高利用率和稳定熵，重建精度持续提升 |

FSQ 的核心公式为：

$$\hat{\mathbf{z}} = \mathcal{Q}(\mathbf{z}) = \mathtt{round}(f(\mathbf{z}))$$

其中 $f$ 为 sigmoid 函数，将潜在向量映射到有界区间后直接舍入为离散整数。重建损失为：

$$\mathcal{L} = \|\mathbf{m} - \mathrm{Dec}(f(z) + \mathbf{sg}(\mathtt{round}(f(z))) - f(z))\|_2^2$$

这一设计从根本上规避了 VQ 中 arg min 导致的码字分配不均问题。实验证据（Figure 6, Table 5）显示：FSQ 在 HumanML3D 和 MotionUnion 两个数据集上，重建 L1 损失、MPJPE（平均关节位置误差）、码本利用率和编码熵四项指标全面优于 VQ，且随码本增大性能稳定提升，而 VQ 在大码本下严重退化。

#### 槽位二：文本编码与注意力模式 — 从 CLIP 到 T5-XL 前缀

| 维度 | 基线方案 | ScaMo 方案 |
|------|----------|------------|
| 文本编码器 | CLIP，输出句子级嵌入 | 冻结的 T5-XL，输出词级嵌入序列 |
| 注意力模式 | 无前缀设计，或仅句子级条件注入 | 文本部分使用双向注意力，运动部分使用因果注意力 |
| 条件粒度 | 粗粒度（单向量） | 细粒度（词级序列前缀） |

具体而言，ScaMo 将 T5-XL 编码的词级嵌入作为**前缀**（prefix）置于运动 token 序列之前。在自回归 Transformer 内部，前缀部分的注意力为双向（允许词间交互），运动 token 部分为因果注意力（保证自回归生成）。损失仅计算在运动 token 上：

$$\mathcal{L} = -\sum_{t=1}^{n} \log p(\hat{m}_t | m_{<t}, S, V)$$

其中 $S$ 为文本前缀，$V$ 为词汇表。消融实验（Table 2）显示该设计效果显著：FID 从 CLIP 无前缀方案的 0.226 降至 0.104，Top-1 R-Precision 从 0.402 升至 0.510。

#### 槽位三：训练数据规模 — 从 HumanML3D 到 MotionUnion

| 维度 | 基线方案 | ScaMo 方案 |
|------|----------|------------|
| 数据来源 | HumanML3D | Motion-X、CombatMotion、100-Style 及内部数据集 |
| 数据规模 | ~14k 序列 | ~150k 序列，超 260 小时 |
| 数据质量 | 存在静态运动问题 | 经筛选，动捕数据占主体（Figure 4） |

MotionUnion 的大规模高质量数据是缩放定律验证的前提——小数据集无法支撑从 44M 到 3B 参数的多尺度模型训练。

### 核心洞察：运动生成的缩放定律

通过上述三个槽位的协同变更，ScaMo 首次在运动生成领域验证了缩放定律的存在：

1. **大模型需要大词汇**：词汇参数量 $N_v$ 与非词汇参数量 $N_{nv}$ 满足幂律关系 $N_v = 10^{-5.604} \cdot N_{nv}^{1.467}$（$R^2=0.95$），小模型（如 44M）在增大码本时损失上升甚至发散，大模型（>775M）则持续受益。

2. **归一化测试损失与计算预算呈对数线性关系**：$\mathcal{L}_u = -1.062 \times \log_{10}(C) + 13.839$，其中归一化损失 $\mathcal{L}_u = -\frac{1}{T}\sum_{1}^{T} \log \frac{p(m_t | m_{<t}, S, V)}{p(m_t | S, V)}$ 消除了词汇量对损失尺度的影响，使不同配置可公平比较。

3. **最优配置的幂律分配**：词汇参数、非词汇参数、数据量分别与 FLOPs $C$ 满足 $N_v \propto C^{0.75}$、$N_{nv} \propto C^{0.57}$、$D \propto C^{0.43}$，为任意计算预算下的资源配置提供了定量指导。

这些发现表明，运动生成模型同样遵循与语言模型类似的缩放规律，而 FSQ 消除码本坍塌是使词汇量成为可扩展维度的关键使能技术。



ScaMo 的整体框架由两个核心模块级联构成：**Motion FSQ‑VAE** 与 **Text‑Prefix Autoregressive Transformer**，二者分别承担运动离散化与文本条件自回归生成的角色，形成“先压缩后预测”的流水线（Figure 5）。

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/005_Figure_5.jpg]]
*Figure 5: Overview of ScaMo architecture. (a) FSQ: Motion FSQ-VAE. We use one code quantization and d = L = 3 as an example. The feature of other frames is quantized in the same way. (b) (c) Text-prefix Autoregressive Transformer: The text tokens are applied with bidirectional attention and the motion tokens are applied with causal attention. Motion tokens can attend all text tokens*

### 1. 运动离散化：Motion FSQ‑VAE

运动序列首先通过一个编码器‑量化器‑解码器结构被转换为离散 token 序列。与传统 Motion VQ‑VAE 不同，ScaMo 采用**有限标量量化（FSQ）** 替代向量量化（VQ）。FSQ 通过有界舍入操作 `round(f(z))`（其中 `f` 为 sigmoid 函数）将连续潜在向量映射为一组整数索引，仅依赖重建损失 `L = ||m − Dec(f(z) + sg(round(f(z)) − f(z)))||²₂` 进行优化，通过直通估计器传递梯度（Eq. 3–4）。

这一设计的因果机制在于：VQ 中的 `arg min` 匹配操作在码本增大时会导致严重的**码本坍塌**——大部分码字从未被激活，码本利用率骤降。FSQ 以确定性舍入取代最近邻搜索，从根本上消除了该坍塌问题，使词汇量（码本大小）可任意扩展至数万级别，为后续缩放实验提供了稳定的离散表示基础（Figure 5(a)）。

### 2. 文本条件自回归生成：Text‑Prefix Autoregressive Transformer

生成阶段采用一个标准的 Transformer 解码器架构，但引入了**文本前缀**机制。具体而言：

- **文本编码**：输入文本由冻结的 T5‑XL 编码器编码为词级嵌入序列，作为“前缀”拼接到运动 token 序列之前。
- **差异化注意力**：文本前缀部分使用**双向注意力**，允许词级嵌入充分交互；运动 token 部分使用**因果注意力**，保证自回归生成的时序因果性（Figure 5(b–c)）。
- **训练目标**：模型仅在运动 token 部分计算交叉熵损失 `L = −∑ log p(m̂ₜ | m_{<t}, S, V)`，其中 `S` 为文本条件，`V` 为词汇表（Eq. 5）。

这一设计的关键优势在于：词级前缀 + 双向注意力使模型能更细粒度地利用文本语义，相较于仅使用句子级 CLIP 嵌入的无前缀方案，在 HumanML3D 上 FID 从 0.226 降至 0.104，Top‑1 R‑Precision 从 0.402 升至 0.510（Table 2）。同时，冻结 T5‑XL 避免了文本编码器随模型缩放带来的额外训练开销，使计算预算可集中分配于运动生成模型本身的扩展。

### 3. 数据流与缩放闭环

整个流水线的数据流为：**原始运动序列 → Motion FSQ‑VAE 编码/量化 → 离散运动 token 序列**；同时 **文本 → 冻结 T5‑XL → 词级嵌入前缀**。二者拼接后输入 Text‑Prefix Autoregressive Transformer 进行自回归预测。在推理时，给定文本前缀，模型逐 token 生成运动序列，再由 FSQ‑VAE 解码器还原为连续运动。

这种模块化解耦使得三个可缩放维度——**模型参数量（非词汇参数 N_nv）、词汇量（N_v）、训练数据量（D）**——均可独立调节，为后续缩放定律的系统探索提供了架构基础。



ScaMo 框架由两个核心模块构成：**Motion FSQ‑VAE**（运动有限标量量化变分自编码器）与**文本前缀自回归 Transformer**。前者将连续运动序列离散化为整数 token 序列，后者以冻结文本编码器产生的词级嵌入为前缀，自回归地预测运动 token。两个模块的协同设计直接解除了传统方案在数据规模、量化稳定性和架构扩展性上的三重瓶颈。

### 4.1 Motion FSQ‑VAE：从 VQ 坍塌到 FSQ 稳定量化

传统运动生成普遍采用向量量化（VQ‑VAE）将编码器输出 $ \mathbf{z} $ 映射到码本 $ \mathcal{C} $ 中最近邻的嵌入向量：

$$ \hat{\mathbf{z}} = \mathcal{Q}(\mathbf{z}; \mathcal{C}) = \underset{\mathbf{e}_k}{\arg\min} \lVert \mathbf{z} - \mathbf{e}_k \rVert_2^2 \tag{1} $$

训练损失由重建项与承诺损失构成：

$$ \mathcal{L} = \lVert \mathbf{m} - \mathrm{Dec}(\mathcal{Q}(\mathbf{z}; \mathcal{C})) \rVert_2^2 + \alpha \lVert \mathbf{z} - \mathrm{sg}(\hat{\mathbf{z}}) \rVert_2^2 \tag{2} $$

其中 $ \mathrm{sg}(\cdot) $ 为停止梯度算子。该方案的根本缺陷在于 $ \arg\min $ 操作：当码本增大时，只有极少数码字被频繁选中，其余码字因梯度更新不足而被“废弃”，导致**码本坍塌**——码本利用率骤降、熵急剧减小、重建质量反而退化。

ScaMo 以**有限标量量化（FSQ）** 替代 VQ。FSQ 将潜在向量 $ \mathbf{z} $ 的每一维通过有界函数 $ f(\cdot) $（通常为 sigmoid）压缩到 $ [0,1] $，再按预设量化级数直接舍入到离散整数：

$$ \hat{\mathbf{z}} = \mathcal{Q}(\mathbf{z}) = \mathtt{round}(f(\mathbf{z})) \tag{3} $$

梯度通过直通估计器（straight‑through estimator）回传，整个量化器仅依赖单一重建损失：

$$ \mathcal{L} = \lVert \mathbf{m} - \mathrm{Dec}\big(f(z) + \mathrm{sg}(\mathtt{round}(f(z))) - f(z)\big) \rVert_2^2 \tag{4} $$

FSQ 的设计消除了 $ \arg\min $ 带来的竞争性选择，使每个码字都能获得均匀的梯度信号。实验证据（Figure 6, Table 5）表明：FSQ 在码本大小从 256 增至 65536 的全程中，码本利用率与熵均保持高位且稳步上升，而 VQ 在码本超过 2048 后出现严重坍塌；FSQ 的重建 L1 损失与 MPJPE 也持续优于 VQ，且大码本优势更为显著。这一性质使得词汇量可随模型规模任意扩展，是后续缩放定律成立的关键前提。

### 4.2 文本前缀自回归 Transformer：双向文本 + 因果运动

生成模型采用**冻结 T5‑XL** 将输入文本 $ S $ 编码为词级嵌入序列，作为前缀拼接到运动 token 序列 $ m_{<t} $ 之前。注意力模式如图 5(b)(c) 所示：文本部分使用**双向注意力**以充分捕获词间上下文，运动部分使用**因果注意力**以维持自回归生成的时序约束。

模型仅在运动 token 上以交叉熵损失进行优化：

$$ \mathcal{L} = -\sum_{t=1}^{n} \log p(\hat{m}_t \mid m_{<t}, S, V) \tag{5} $$

其中 $ V $ 为 FSQ 定义的离散词汇表。消融实验（Table 2）证实，T5‑XL 前缀方案相较 CLIP 无前缀方案将 FID 从 0.226 降至 0.104，Top‑1 R‑Precision 从 0.402 提升至 0.510，表明词级前缀与双向注意力能显著增强文本‑运动的细粒度对齐。

### 4.3 归一化测试损失：公平比较不同词汇量的基础

由于原始交叉熵损失随词汇量 $ |V| $ 增大而自然增大，直接比较不同码本大小的模型将产生系统性偏差。为此，ScaMo 引入**归一化测试损失** $ \mathcal{L}_u $，从条件概率中减去词汇先验：

$$ \mathcal{L}_u = -\frac{1}{T} \sum_{t=1}^{T} \log \frac{p(m_t \mid m_{<t}, S, V)}{p(m_t \mid S, V)} \tag{8} $$

该指标消除了词汇量对损失尺度的影响，使不同配置下的性能可被公平比较，并成为后续所有缩放定律拟合的因变量。

### 4.4 缩放定律优化问题

在给定计算预算 $ C $（FLOPs）的约束下，ScaMo 将词汇参数 $ N_v $、非词汇参数 $ N_{nv} $ 与训练数据量 $ D $ 的联合优化形式化为：

$$ (N_v^{\mathrm{opt}}, N_{nv}^{\mathrm{opt}}, D^{\mathrm{opt}}) = \arg\min_{N_v, N_{nv}, D} \mathcal{L}(N_v, N_{nv}, D) \quad \text{s.t.} \quad \mathrm{FLOPs}(N_v, N_{nv}, D) \leq C \tag{9} $$

通过 IsoFLOP 实验拟合得到的三组幂律关系（Eq. 10–13）以及归一化损失与 FLOPs 的对数定律（Eq. 14），为任意计算预算下的最优资源配置提供了定量预测工具，详见实验分析部分。

### 补充图表

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/003_Figure_3.jpg]]
*Figure 3: Scaling laws of ScaMo. (a) Power law between*

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/006_Figure.jpg]]
*Figure: Codebook Size (a) HumanML3D. (b) MotionUnion*

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/008_Figure_7.jpg]]
*Figure 7: Power laws of vocabulary parameters, non-vocabulary parameters, and data with respect to FLOPs*



## 实验与关键发现

### 记号器对比：FSQ 全面优于 VQ

论文首先在运动重建任务上系统对比了有限标量量化（FSQ）与向量量化（VQ）的性能差异，从重建精度和码本利用率两个维度揭示了 VQ 的失效模式。

**重建精度**：在 HumanML3D 和 MotionUnion 两个数据集上，FSQ 在小码本（如 256）时已取得与 VQ 相当的重建 L1 损失和 MPJPE；当码本增大至 2048 以上时，VQ 的重建误差显著上升，而 FSQ 持续改善（Figure 6、Table 5）。这表明 VQ 的 `arg min` 操作在大码本下导致码本坍塌，大量码字闲置，有效容量不增反降。

**码本利用率与熵**：FSQ 的码本使用率（Codebook Usage）和指数熵（Exponential Entropy）在 256 至 65536 码本范围内均保持高位，编码分布均匀；VQ 在码本超过 2048 后利用率骤降、熵急剧下降，确认了严重的码本坍塌（Figure 6、Table 5）。

> **关键机制**：FSQ 通过有界舍入（`round(f(z))`）替代 `arg min` 匹配，消除了码本坍塌的根源，使词汇量可任意扩展，为后续缩放定律验证提供了必要基础。

### 架构消融：文本前缀与编码器选择

Table 2 报告了架构消融的核心结果。在 HumanML3D 测试集上，使用冻结 T5-XL 作为文本编码器并采用前缀注意力（文本双向、运动因果）的方案，相比使用 CLIP 句子嵌入且无前缀的标准自回归生成器，取得了显著提升：

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/009_Table_2.jpg]]
*Table 2: Ablation experiments of the architecture*

- **FID** 从 0.226 降至 **0.104**（↓54%）
- **Top-1 R-Precision** 从 0.402 升至 **0.510**（↑27%）
- **Matching Score** 从 3.422 改善至 **3.021**（越低越好）

这一结果表明，词级文本嵌入与双向前缀注意力能更精细地建模文本-运动对齐关系，而 CLIP 的句子级嵌入丢失了细粒度语义信息。

### HumanML3D 基准主结果

Table 6 展示了 ScaMo 与现有方法的对比。ScaMo-343M（码本 65536、T5-XL 前缀）在 HumanML3D 上取得 FID **0.104**，显著优于基于 LLM 的方法：

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/016_Table_6.jpg]]
*Table 6: Test results of different models on HumanML3D Benchmark. We take the results of MotionGPT* from Wang et al. [59]*

- 对比 **LargeMotionModel**（LLaMA-2-13B，FID 0.166），ScaMo-343M 以仅 2.6% 的参数量实现了 37% 的 FID 降低。
- 对比 **MotionGPT**（LLaMA-13B）等 LLM 方法，ScaMo 在更小模型尺寸下取得更优或相当的生成质量。

> **公平性说明**：论文指出 FID 等传统指标依赖预训练特征提取器，可能对过拟合模型给出过于乐观的分数。因此缩放定律分析中采用归一化测试损失 $\mathcal{L}_u$（Eq.8）作为主要指标，以消除词汇量大小对损失尺度的偏差。

### 缩放定律验证

论文通过系统控制模型尺寸（44M 至 3B）和码本大小（256 至 65536），在 MotionUnion 数据集上验证了三条核心缩放定律。

#### 1. 大模型需要大词汇（幂律耦合）

Figure 3(a) 和 Eq.(10) 揭示了词汇参数量 $N_v$ 与非词汇参数量 $N_{nv}$ 之间的强幂律关系：

$$N_v = 10^{-5.604} \cdot N_{nv}^{1.467}$$

拟合优度 $R^2=0.95$，指数 1.467 > 1 表明词汇需求随模型增大呈超线性增长。Figure 8 的损失曲线进一步佐证：小模型（如 44M）在码本增大时损失上升甚至发散，而大模型（>775M）则随码本增大持续降低测试损失。

#### 2. 最优参数与计算预算的幂律关系

Figure 7 和 Eq.(11)-(13) 给出了最优词汇参数、非词汇参数、数据量随 FLOPs 的幂律分配：

$$N_v = 10^{-5.29} \cdot C^{0.75}$$

$$N_{nv} = 10^{-0.52} \cdot C^{0.57}$$

$$D = 10^{-0.05} \cdot C^{0.43}$$

词汇参数量对计算预算的弹性（指数 0.75）高于非词汇参数（0.57）和数据量（0.43），再次确认词汇扩展是缩放的关键杠杆。

#### 3. 性能预测：对数缩放定律

Figure 3(b) 和 Eq.(14) 显示归一化测试损失 $\mathcal{L}_u$ 与 FLOPs $C$ 呈精确的对数线性关系：

$$\mathcal{L}_u = -1.062 \times \log_{10}(C) + 13.839$$

该公式可用于预测任意计算预算下的模型性能，为资源分配提供定量指导。论文指出，在当前数据规模下尚未观察到涌现能力，更大规模的高质量运动-文本数据是进一步验证缩放定律外推性的关键。

### 局限与开放问题

1. **数据瓶颈**：MotionUnion 虽已扩展至约 150k 序列、260 小时，但部分数据源于视频动作捕捉，质量受限；训练中尚未观察到涌现能力。
2. **缩放外推**：当前最优配置（3B 模型、64k 码本）是否为全局最优，以及所拟合定律在更高计算预算下是否成立，仍需更大规模实验验证。
3. **量化扩展**：FSQ 的组量化或残差量化扩展是否能进一步提升运动重建与生成质量，论文未作探索。

### 补充图表

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/014_Table_5.jpg]]
*Table 5: Tokenizer numerical results. The Entropy is Exponential Entropy*

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/002_Figure_2.jpg]]
*Figure 2: We plot the relationship between normalized test loss and FLOPs for observing the scaling behavior. Overall, the larger model and larger vocabulary size can get better performances*

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/001_Figure_1.jpg]]
*Figure 1: The generation results of ScaMo-3B with a text input. Our model could deal with abstract sentences and long sentences*

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/004_Figure_4.jpg]]
*Figure 4: The frames statistics of MotionUnion dataset. Motion capture data accounts for the majority*

![[assets/figures/papers/paper_list_l1863_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Mode/figures/007_Figure_6.jpg]]
*Figure 6: Reconstuction results of different tokenizers on HumanML3D and MotionUnion. Reconstruction: L1 loss and MPJPE. Codebook Utilization: Codebook Usage and Entropy*



## 定位与知识库关联

### 1. 与现有运动生成范式的对比

ScaMo 的核心定位在于首次在文本驱动运动生成领域系统性地验证了缩放定律。此前的运动生成模型虽然在生成质量上取得了进展，但始终未触及缩放行为的系统性研究。ScaMo 通过三个关键维度的创新实现了这一突破：

**与基于 LLM 的运动生成方法对比。** 近期多篇工作尝试将运动生成纳入大语言模型框架，如 **MotionGPT**（基于 LLaMA-13B）、**MotionLLM**（基于 Gemma-2b）、**AvatarGPT**（基于 LLaMA-13B）以及 **LargeMotionModel**（基于 LLaMA-2-13B）。这些方法直接复用预训练 LLM 的架构与权重，虽然受益于语言模型的规模化能力，但存在两个根本性问题：其一，运动 token 与文本 token 的语义鸿沟使得 LLM 的预训练知识难以有效迁移；其二，LLM 的词汇表大小固定，无法根据运动数据的复杂度灵活扩展。实验结果表明，ScaMo-343M 在 HumanML3D 上的 FID 达到 0.104，显著优于 LargeMotionModel（LLaMA-2-13B）的 0.166，以不到 3% 的参数量实现了更优的生成质量（Table 6），验证了为运动生成专门设计可扩展架构的必要性。

**与传统 VQ-VAE 运动生成方法的对比。** 以 **T2M-GPT** 为代表的传统运动向量量化方法依赖 VQ-VAE 进行运动离散化，配合 EMA 更新和码本重置策略缓解码本坍塌。然而，VQ 中 `arg min` 操作的固有缺陷导致码本利用率随码本增大而急剧下降——当码本从 2048 扩展至 65536 时，VQ 的码本使用率和熵均出现严重衰减，重建误差反而上升（Figure 6, Table 5）。ScaMo 采用有限标量量化（FSQ）替代 VQ，通过舍入操作 `round(f(z))` 将潜在向量直接映射为离散整数，从根本上消除了码本坍塌问题。FSQ 仅需简单的重建损失即可训练，且随码本增大性能稳定提升，这使得词汇量可以按需扩展，为缩放定律的验证提供了前提条件。

**与基于 CLIP 的自回归生成方法对比。** 传统自回归运动生成通常使用 CLIP 提取句子级文本嵌入作为条件信号。ScaMo 的消融实验（Table 2）表明，将文本编码器从 CLIP 替换为冻结的 T5-XL，并采用词级嵌入作为前缀（prefix），配合文本部分双向注意力、运动部分因果注意力的混合注意力模式，FID 从 0.226 降至 0.104，Top-1 R-Precision 从 0.402 升至 0.510。这一改进的本质在于：词级前缀提供了更细粒度的文本-运动对齐信号，而双向注意力使文本 token 之间可充分交互，增强了条件表示的丰富性。

### 2. 技术贡献的因果链条

ScaMo 的缩放定律验证并非偶然，而是三条技术路线形成因果闭环的结果：

1. **数据瓶颈的突破**：构建 MotionUnion 数据集（约 150k 序列，260 小时数据），将数据规模从 HumanML3D 的约 14k 序列提升一个数量级，为大规模训练提供了物质基础。
2. **量化瓶颈的突破**：FSQ 消除了 VQ 的码本坍塌，使词汇量可从 256 扩展至 65536 甚至更高，且码本利用率始终维持在高水平。
3. **架构瓶颈的突破**：文本前缀自回归架构配合冻结 T5-XL，使模型尺寸可系统性地从 44M 扩展至 3B，且性能随规模单调提升。

这三条路线的交汇点在于**大模型与大词汇的幂律耦合关系**：拟合结果表明，最优词汇参数量 $N_v$ 与非词汇参数量 $N_{nv}$ 满足 $N_v = 10^{-5.604} \cdot N_{nv}^{1.467}$（$R^2=0.95$），这意味着模型越大，所需的词汇量呈超线性增长。这一发现解释了此前基于 LLM 的方法（固定词汇表）难以充分受益于模型规模增长的原因。

### 3. 适用边界与局限

尽管 ScaMo 在 HumanML3D 上取得了领先的 FID（0.104），但在评估方法和泛化性方面存在若干局限：

**评估指标的可靠性问题。** 论文自身指出，FID 等传统生成质量指标依赖预训练特征提取器，可能对过拟合模型给出过于乐观的分数。这也是 ScaMo 选择归一化测试损失 $L_u$ 作为主要缩放指标的原因。$L_u$ 通过除以词汇表大小的均匀分布熵来消除词汇量对损失尺度的混淆效应，使得不同词汇量下的模型可以公平比较。然而，$L_u$ 与实际生成质量之间的对应关系尚未被严格验证，这限制了缩放定律预测结果的实际指导意义。

**数据规模与多样性的上限。** MotionUnion 虽较 HumanML3D 扩大了一个数量级，但相较于语言模型的训练数据（万亿 token 级别）仍然微小。论文明确指出训练中尚未观察到涌现能力，部分数据来源于视频动作捕捉，其质量受限。这意味着当前拟合的缩放定律可能仅适用于中等数据规模区间，在外推到更大计算预算时可能出现偏差。

**全局最优配置的不确定性。** 论文通过 IsoFLOP 分析拟合了最优参数分配曲线，但受限于实验成本，仅探索了有限的计算预算范围。当前最优配置（3B 模型、64k 码本）是否为全局最优，以及缩放定律在更高 FLOPs 下是否仍保持对数线性关系，均需进一步验证。

### 4. 开放问题与后续方向

ScaMo 为运动生成的缩放研究打开了若干值得深入的方向：

1. **数据规模化路径**：如何收集或生成更大量、高质量且多样化的运动-文本数据，是观测涌现能力并外推缩放定律的前提。可能的路径包括从视频中自动提取运动-文本对、利用运动增强技术扩充现有数据集等。
2. **量化方法的进一步扩展**：FSQ 当前采用单码量化，论文提出了组量化或残差量化扩展的可能性。这些扩展是否能进一步提升重建精度，同时保持码本利用率的高水平，值得探索。
3. **缩放定律的外推验证**：所拟合的对数定律 $L_u = -1.062 \log_{10}(C) + 13.839$ 是否在更高计算预算下成立，需要更大规模的实验验证。这不仅是运动生成领域的问题，也是所有小领域缩放研究的共性挑战。
4. **跨领域泛化**：ScaMo 的缩放定律在 HumanML3D 和 MotionUnion 上得到了验证，但这些数据以人体运动为主。该框架是否适用于其他运动模态（如动物运动、机械臂操作），以及缩放定律的系数是否具有跨领域不变性，尚待研究。
5. **评估体系的完善**：建立独立于特征提取器的、与人类感知更一致的生成质量评估指标，对于准确衡量缩放带来的实际收益至关重要。



## 原文 PDF

![[paperPDFs/CVPR_2025/ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Model.pdf]]
