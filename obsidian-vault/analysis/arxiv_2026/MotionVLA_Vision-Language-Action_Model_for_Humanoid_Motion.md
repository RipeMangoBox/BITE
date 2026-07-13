---
title: "MotionVLA: Vision-Language-Action Model for Humanoid Motion"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/MotionVLA_Vision-Language-Action_Model_for_Humanoid_Motion.pdf
project_link: "https://aigeeksgroup.github.io/MotionVLA"
code_link: "https://github.com/AIGeeksGroup/MotionVLA"
aliases:
- MotionVLA
tags:
- arxiv_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过频率域分析人为分离Base（位置/旋转，低频）和Phys（速度，高频）双流，并独立应用不同截断的DCT+BPE进行量化与建模。
primary_logic: 关节位置以低频为主（前5个DCT系数捕获93%能量），关节速度以高频为主（仅捕获37%能量）；双流解耦后可为低频语义和高频物理分别保留充分的表示能力，消除传统统一码本的结构性偏差。
claims:
- 五个DCT系数捕获关节位置93%的能量，但仅捕获关节速度37%的能量。
- 单流分词器生成的运动会累积时间上的漂移和关节不稳定，而双流方法能全程跟踪真实值。
- MBench 上 Motion-Condition Consistency = 0.55
- MBench 上 Foot Sliding = 0.0049
---

# MotionVLA: Vision-Language-Action Model for Humanoid Motion

> [!tip] 核心洞察
> 关节位置以低频为主（前5个DCT系数捕获93%能量），关节速度以高频为主（仅捕获37%能量）；双流解耦后可为低频语义和高频物理分别保留充分的表示能力，消除传统统一码本的结构性偏差。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionVLA: 面向人形运动的视觉-语言-动作模型 |
| 英文题名 | MotionVLA: Vision-Language-Action Model for Humanoid Motion |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2606.15142) · [Project](https://aigeeksgroup.github.io/MotionVLA) · [Code](https://github.com/AIGeeksGroup/MotionVLA) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MotionVLA |
| Dataset | MBench, HumanML3D |

> [!tip] 效果简介
> - MBench 上，Motion-Condition Consistency 0.55 vs 0.53 (ViMoGen) (+0.02 (3.8% improvement))；Foot Sliding 0.0049 vs 0.0051 (ViMoGen-light) (-0.0002)。
> - HumanML3D 上，Diversity (closeness to Real) 9.548 (gap 0.045) vs Real 9.503 (Diversity gap reduced by over 50% compared to typical baselines)。

## 概要

人形运动生成面临一个根本性瓶颈：单一共享码本将异质运动信号（关节位置与速度）强制压缩至同一量化空间，固有偏向低频姿态语义，导致高频物理动态（速度）大量信息丢失。MotionVLA 通过频率域分析人为分离 **Base（位置/旋转，低频）** 和 **Phys（速度，高频）** 双流，并独立应用不同截断的 DCT+BPE 进行量化与建模，从而消除传统统一码本的结构性偏差。

核心发现是：关节位置以低频为主（前 5 个 DCT 系数捕获 93% 能量），而关节速度以高频为主（同样 5 个系数仅捕获 37% 能量）。双流解耦后，可为低频语义和高频物理分别保留充分的表示能力。定性对比中，依赖单流分词器的 ViMoGen 在长序列上出现时间漂移和关节不稳定，而 MotionVLA 能全程跟踪真实值。

MotionVLA 将运动生成形式化为统一的自回归序列建模问题，在 Qwen3.5 骨干上通过相位感知的 logit mask 强制先生成 Base 令牌、再生成 Phys 令牌。在 MBench 上，Motion-Condition Consistency 从 0.53 提升至 0.55（+3.8%）；在 HumanML3D 上，Diversity 与真实数据的差距缩小超过 50%。人类偏好研究中，MotionVLA 以 64.0% 的 GSB 偏好率显著优于 ViMoGen。

**方法定位**：MotionVLA 属于离散自回归运动生成范式，与 T2M-GPT、MoMask、MotionCraft 等方法同源，但通过双流频率分词器（DSFT）和多模态条件（场景图像+文本）实现了差异化。其核心创新在于将频谱解耦引入 VQ-VAE 分词阶段，而非在生成器层面做改进。

**局限性**：流划分与截断长度（$K_b=5$, $K_p=25$）为固定选择，可能未覆盖所有运动类型的频谱极端情况；模型容量缩放受限于当前数据规模和令牌表示的信息量，更大骨干未带来持续显著增益；跨数据集和跨场景的泛化能力未经验证。

### 运动生成中的频谱偏差：低频语义与高频物理的失衡

人体运动信号由两类性质迥异的维度构成：描述姿态语义的**关节位置/旋转**（低频主导），以及描述物理动态的**关节速度**（高频主导）。一个被长期忽视的事实是，现有运动分词器普遍采用**单一共享码本**（single-stream codebook）将全部运动维度压缩至同一量化空间。这种设计隐含地偏向能量占优的低频分量，导致高频物理信息在压缩过程中大量丢失。

定量证据来自频率域分析：对运动序列施加离散余弦变换（DCT）后，仅前 **5 个 DCT 系数**即可捕获关节位置 **93%** 的能量，但同样 5 个系数仅能捕获关节速度 **37%** 的能量。这意味着，当统一码本以低频信号的压缩效率为目标时，高频的速度信息被系统性牺牲。

这一结构性偏差的直接后果是**时间累积漂移与关节不稳定**。如 Figure 1 所示，依赖单流分词器的 ViMoGen 在生成长序列时，运动轨迹随时间逐渐偏离真实值（GT），关节位置出现可观察的漂移（白色圆圈标注）。相比之下，MotionVLA 的双流方法能在序列的 30%、60%、90% 时间点全程紧密跟踪真实运动。

### 现有方法的缺口

当前运动生成方法可按范式分为三类：

- **扩散模型**（如 MDM、MotionDiffuse）：通过迭代去噪生成运动，但推理速度慢，且缺乏对运动频谱结构的显式建模。
- **自回归离散生成**（如 T2M-GPT、MoMask、MotionCraft）：将运动量化为离散 token 后逐帧预测，但 tokenizer 设计未区分低频语义与高频物理。
- **多路径/多专家量化**（如 GenM3、DisCoRD）：尝试改进码本容量或量化精度，但仍将异质运动维度混合压缩，未从根本上解决频谱偏差。

核心瓶颈可归结为：**单一共享码本将异质运动信号（关节位置与速度）强制压缩至同一量化空间，固有偏向低频姿态语义，导致高频物理动态信息大量丢失。**

### MotionVLA 的核心动机

MotionVLA 提出一个直接而关键的因果操作：通过频率域分析**人为分离** Base（位置/旋转，低频）和 Phys（速度，高频）两个独立流，并对每个流分别施加不同截断长度的 DCT 与 BPE 量化。这一解耦策略使得：

- **Base 流**以少量 DCT 系数（$K_b=5$）高效保留姿态语义；
- **Phys 流**以更长的截断（$K_p=25$）保留物理动态所需的高频分量。

双流设计消除了传统统一码本的结构性偏差，为低频语义和高频物理分别保留了充分的表示能力。在生成层面，MotionVLA 将 Base 和 Phys token 组织为统一的 autoregressive 序列，并引入**相位感知的 logit mask** 强制先生成 Base 后生成 Phys，确保语义姿态先行、物理动态随后。

这一动机在实验中得到了直接验证：在 HumanML3D 上，MotionVLA 将 **Diversity 指标与真实数据的差距缩小超过 50%**；在 MBench 上，**Motion-Condition Consistency 从 0.53 提升至 0.55（+3.8%）**，且 Foot Sliding 从 0.0051 降至 0.0049。人类偏好研究中，MotionVLA 在 64.0% 的比较中被领域专家优选，而 ViMoGen 仅被优选 14.0%（Table 7）。

## 核心方法与创新机理

MotionVLA 的核心创新在于**将异质运动信号从单一共享码本的压缩瓶颈中解放出来**，通过频率域的结构性分离，为低频姿态语义和高频物理动态分别保留充分的表示能力。

### 瓶颈发现：统一码本的结构性偏差

现有的离散运动分词方法（如 ViMoGen 等单流分词器）将关节位置、旋转、速度等所有运动维度统一压缩至同一个量化空间中。这种设计存在一个被忽视的结构性偏差：**关节位置以低频为主，前5个 DCT 系数即可捕获 93% 的能量；而关节速度以高频为主，同样的5个系数仅能捕获 37% 的能量**（Figure 4）。当共享码本的截断长度偏向低频时，高频物理动态信息大量丢失，导致生成的运动随时间累积出现漂移和关节不稳定（Figure 1 中白色圆圈标注）。

### 因果机制：双流频率分词器 DSFT

针对上述瓶颈，MotionVLA 提出了 **DSFT (Dual-Stream Frequency Tokenizer)**，包含两个关键的 changed slots：

**Slot 1: 分词策略——从单流统一码本到双流独立量化**

| 对比维度 | Baseline（单流） | MotionVLA（双流 DSFT） |
|---------|-----------------|----------------------|
| 流划分 | 所有运动维度共享一个 DCT+BPE 截断 | 显式分离为 Base 流（位置/旋转，$D_b$ 维）和 Phys 流（速度，$D_p$ 维） |
| DCT 截断 | 统一截断长度 | Base 流 $K_b=5$，Phys 流 $K_p=25$ |
| BPE 码本 | 单一码本 | 两个流独立训练 BPE 码本 |

形式化地，运动序列 $\mathbf{M}$ 首先被分解为：

$$\mathbf{M}_{\mathrm{base}} \in \mathbb{R}^{T \times D_b}, \quad \mathbf{M}_{\mathrm{phys}} \in \mathbb{R}^{T \times D_p}$$

然后分别进行 DCT 变换并独立截断：

$$\mathbf{C}_{\mathrm{base}} = \mathrm{DCT}(\mathbf{M}_{\mathrm{base}})_{[:K_b]}, \quad \mathbf{C}_{\mathrm{phys}} = \mathrm{DCT}(\mathbf{M}_{\mathrm{phys}})_{[:K_p]}$$

这一设计的动机源于 Figure 3 的频率域聚类分析：运动维度在低频比率上呈现一致的双峰分布，天然分离为低频主导的 Base 维度和高频主导的 Phys 维度。双流解耦后，低频语义流可以用极少系数高效压缩，而高频物理流则保留足够的系数（$K_p=25$）来维持动态细节。

**Slot 2: 解码控制——从无约束自回归到相位感知的生成顺序**

| 对比维度 | Baseline | MotionVLA |
|---------|----------|-----------|
| 生成顺序 | 无流顺序约束 | 强制先 Base 后 Phys |
| 控制机制 | 标准自回归 | 相位感知 logit mask |

MotionVLA 将双流令牌组织为统一的自回归序列：

$$\mathbf{s} = [M_{\mathrm{BOS}}, b_1, \dotsc, b_N, M_{\mathrm{SEP}}, p_1, \dotsc, p_M, M_{\mathrm{EOS}}]$$

在推理时，通过相位感知的 logit mask 强制执行生成顺序：在 $M_{\mathrm{SEP}}$ 生成之前，仅允许预测 Base 令牌和 $M_{\mathrm{SEP}}$；$M_{\mathrm{SEP}}$ 生成后，仅允许预测 Phys 令牌和 $M_{\mathrm{EOS}}$。这一设计确保物理动态令牌的预测始终以已生成的姿态语义令牌为条件，形成因果一致的生成管线。

### 关键证据强度

- **能量覆盖差异**（Figure 4）：$K=5$ 时 Base 流能量覆盖 93%，Phys 流仅 37%，证据确凿（confidence 0.98），直接支撑双流独立截断的必要性。
- **定性可视化**（Figure 1）：单流方法 ViMoGen 在长序列中表现出时间漂移和关节不稳定，而双流方法全程紧密跟踪真值，直观验证了解耦的有效性（confidence 0.95）。
- **消融验证**（Table 6）：增大 $K_p$ 持续提升物理能量覆盖和重建质量，但 $K_p=30$ 时部分指标开始下降，$K_p=25$ 提供最佳平衡，确认了截断长度选择的有效性（confidence 0.9）。

### 遗留问题

当前 Base/Phys 的流划分和截断长度（$K_b=5, K_p=25$）为固定选择，可能未覆盖所有运动类型的频谱极端情况。能否通过数据驱动的方法自动学习每个运动维度的流分配，以适应不同运动风格的频谱变化，仍是一个开放问题。

MotionVLA 将条件运动生成建模为一个统一的**自回归序列预测问题**，其核心流水线由两个关键组件构成：**DSFT 双流频率分词器**（Dual-Stream Frequency Tokenizer）和一个基于 **Qwen3.5** 的自回归 Transformer 骨干网络。

### 输入-输出流

系统的输入为多模态条件：一段**场景图像**（scene image）和一条**文本指令**（text instruction）。这些条件通过一个多模态编码器（基于 Qwen3.5 的视觉-语言编码器）转换为上下文表示，注入自回归骨干网络。输出为一段与条件对齐的**人体运动序列**，表示为 SMPL-X 关节位置和旋转参数。

### DSFT 双流分词器

DSFT 是整个框架的核心创新。它将连续运动序列 $\mathbf{M} \in \mathbb{R}^{T \times D}$ 分解为两个互补的令牌流（Figure 2a）：

- **Base 流** $\mathbf{M}_{\mathrm{base}} \in \mathbb{R}^{T \times D_b}$：包含关节位置和旋转相关维度，主要编码低频的姿态语义。
- **Phys 流** $\mathbf{M}_{\mathrm{phys}} \in \mathbb{R}^{T \times D_p}$：包含关节速度相关维度，主要编码高频的物理动态。

两个流分别经过**离散余弦变换（DCT）**并独立截断，保留不同数量的 DCT 系数（Base 流 $K_b=5$，Phys 流 $K_p=25$），再通过各自的 BPE 码本量化为离散令牌。这种解耦设计直接回应了核心瓶颈：单一共享码本固有地偏向低频姿态语义，导致高频物理动态信息大量丢失。频率域分析（Figure 3）证实，运动维度在频域呈现稳定的双峰分离——Base 维度以低频为主，Phys 维度以高频为主。

### 统一自回归序列与相位感知解码

训练时，Base 令牌和 Phys 令牌被排列为统一序列（Figure 2b）：

$$\mathbf{s} = [M_{\mathrm{BOS}}, b_1, \dotsc, b_N, M_{\mathrm{SEP}}, p_1, \dotsc, p_M, M_{\mathrm{EOS}}]$$

其中 $M_{\mathrm{BOS}}$、$M_{\mathrm{SEP}}$、$M_{\mathrm{EOS}}$ 为三个结构标记。总词汇量扩展为 $V = V_{\mathrm{LM}} + V_{\mathrm{motion}} + 3$，其中 $V_{\mathrm{motion}} = V_{\mathrm{base}} + V_{\mathrm{phys}}$ 为运动令牌词汇。

骨干网络以自回归方式逐令牌预测，但施加**相位感知的 logit 掩码**以强制执行生成顺序：在生成 $M_{\mathrm{SEP}}$ 之前，仅允许 Base 令牌和 $M_{\mathrm{SEP}}$；$M_{\mathrm{SEP}}$ 生成后，仅允许 Phys 令牌和 $M_{\mathrm{EOS}}$。这确保了“先 Base 后 Phys”的因果结构，使模型在预测物理动态时已具备完整的姿态语义上下文。

训练损失仅在运动令牌和结构标记上计算交叉熵：

$$\mathcal{L}_{\mathrm{train}} = \mathrm{CE}(\mathbf{z} + \mathbf{m}, \mathbf{y})$$

其中 $\mathbf{m}$ 为掩码，使语言令牌不参与损失。

### 推理与解码

推理时（Figure 2c），用户提供目标运动长度 $T$，模型在文本和场景图像条件下自回归生成完整的统一令牌序列。生成的 Base 和 Phys 令牌分别通过逆 BPE 和逆 DCT（IDCT）解码为连续流，最终拼接重构为完整运动序列。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MotionVLA. (a) DSFT performs dual-stream frequency tokenization by decomposing motion into Base and Phys components and converting them into discrete tokens. (b) During training, MotionVLA learns to autoregressively predict the unified motion token sequence under text and scene-image conditioning, supervised by DSFT tokens derived from ground-truth motion. (c) At inference time, the model generates Base and Phys tokens conditioned on multimodal inputs, which are then decoded and recombined to reconstruct the final motion sequence*

MotionVLA 的核心架构由两个关键模块构成：**DSFT 双流频率分词器**（Dual-Stream Frequency Tokenizer）和基于 **Qwen3.5 的自回归骨干网络**。DSFT 负责将连续运动序列转换为离散的 Base 和 Phys 双流令牌，骨干网络则在多模态条件（场景图像和文本指令）下自回归地预测统一的运动令牌序列。

### 2.1 运动分解：Base 流与 Phys 流

核心瓶颈在于：传统单一共享码本将异质运动信号（关节位置与速度）强制压缩至同一量化空间，固有偏向低频姿态语义，导致高频物理动态信息大量丢失。MotionVLA 通过频率域分析人为分离双流来解决这一问题。

给定运动序列，首先按维度将其分解为基础姿态流和物理动态流：

$$\mathbf{M}_{\mathrm{base}} \in \mathbb{R}^{T \times D_b}, \quad \mathbf{M}_{\mathrm{phys}} \in \mathbb{R}^{T \times D_p}$$

其中 $\mathbf{M}_{\mathrm{base}}$ 包含位置和旋转相关维度（主要编码姿态语义），$\mathbf{M}_{\mathrm{phys}}$ 包含速度相关维度（主要编码物理动态）。$T$ 为时间帧数，$D_b$ 和 $D_p$ 分别为两流的维度数。

### 2.2 频率域截断：DCT 与独立压缩

对两个流分别应用离散余弦变换（DCT）并在频率域进行差异化截断：

$$\mathbf{C}_{\mathrm{base}} = \mathrm{DCT}(\mathbf{M}_{\mathrm{base}})_{[:K_b]}, \quad \mathbf{C}_{\mathrm{phys}} = \mathrm{DCT}(\mathbf{M}_{\mathrm{phys}})_{[:K_p]}$$

**关键发现**：关节位置以低频为主，前 $K_b=5$ 个 DCT 系数即可捕获 93% 的能量；而关节速度以高频为主，同样 5 个系数仅能捕获 37% 的能量。因此 Phys 流需要更大的截断长度 $K_p=25$ 来保留足够的物理细节。这种差异化截断是双流方法消除统一码本结构性偏差的核心机制。

### 2.3 统一自回归序列建模

截断后的系数分别通过独立的 BPE（Byte Pair Encoding）进行令牌化，形成 Base 令牌 $\{b_1, \dots, b_N\}$ 和 Phys 令牌 $\{p_1, \dots, p_M\}$。MotionVLA 将运动生成形式化为统一的自回归序列建模问题：

$$\mathbf{s} = [M_{\mathrm{BOS}}, b_1, \dotsc, b_N, M_{\mathrm{SEP}}, p_1, \dotsc, p_M, M_{\mathrm{EOS}}]$$

序列中引入三个结构标记：$M_{\mathrm{BOS}}$（序列起始）、$M_{\mathrm{SEP}}$（流分隔）和 $M_{\mathrm{EOS}}$（序列结束）。生成时通过**相位感知的 logit 掩码**强制执行“先 Base 后 Phys”的顺序约束：在生成 $M_{\mathrm{SEP}}$ 之前只允许 Base 令牌和 $M_{\mathrm{SEP}}$；$M_{\mathrm{SEP}}$ 产生后只允许 Phys 令牌和 $M_{\mathrm{EOS}}$。

### 2.4 词汇表扩展与训练目标

骨干网络基于 Qwen3.5 语言模型，通过 LoRA 进行参数高效微调。总词汇量扩展为：

$$V = V_{\mathrm{LM}} + V_{\mathrm{motion}} + 3, \qquad V_{\mathrm{motion}} = V_{\mathrm{base}} + V_{\mathrm{phys}}$$

其中 $V_{\mathrm{LM}}$ 为原始语言模型词汇，$V_{\mathrm{base}}$ 和 $V_{\mathrm{phys}}$ 分别为两流 BPE 码本的词汇量，额外 3 个位置留给结构标记 $\{M_{\mathrm{BOS}}, M_{\mathrm{SEP}}, M_{\mathrm{EOS}}\}$。

训练仅对运动令牌和结构标记计算交叉熵损失：

$$\mathcal{L}_{\mathrm{train}} = \mathrm{CE}(\mathbf{z} + \mathbf{m}, \mathbf{y})$$

其中 $\mathbf{z}$ 为模型 logits，$\mathbf{m}$ 为掩码（文本令牌位置置零，运动与结构标记位置置一），$\mathbf{y}$ 为目标令牌。多模态编码器将场景图像和文本指令编码为上下文表示，注入自回归解码过程。

### 2.5 解码与运动重建

推理时，模型在多模态条件下生成统一的令牌序列，解码过程逆向执行：对 Base 和 Phys 令牌分别进行逆 BPE 和逆 DCT（IDCT），恢复两流连续表示后拼接为完整运动序列。目标运动长度 $T$ 由外部提供，模型据此生成对应时间跨度的 DSFT 令牌。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/003_Figure_3.jpg]]
*Figure 3: Frequency-domain clustering of motion dimensions. (a) Per-dimension low-frequency ratio on HumanML3D. (b) Corresponding histogram on HumanML3D. (c/d) Corresponding plots on ViMoGen. Both datasets exhibit a consistent bimodal separation between low-frequency Base dimensions and high-frequency Phys dimensions*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/004_Figure_4.jpg]]
*Figure 4: Energy coverage of the Base and Phys streams under different DCT truncation lengths. (a,b) Results on HumanML3D. (c,d) Corresponding results on ViMoGen. The Base stream is highly compressible with small K, whereas the Phys stream requires substantially larger K to preserve its energy*

## 实验与关键发现

### 核心瓶颈验证：单流 vs 双流

MotionVLA 的设计动机源于一个明确的频谱瓶颈：**单一共享码本将异质运动信号（关节位置与速度）强制压缩至同一量化空间，固有偏向低频姿态语义，导致高频物理动态信息大量丢失**。定量证据显示，五个 DCT 系数即可捕获关节位置 93% 的能量，但仅能捕获关节速度 37% 的能量。这意味着在统一码本下，速度维度的信息在压缩过程中被系统性牺牲。

Figure 1 的定性对比直观展示了这一瓶颈的后果：依赖单流分词器的 ViMoGen 在长序列生成中随时间累积漂移和关节不稳定（白色圆圈标注），而 MotionVLA 的双流方法能在全序列（30%、60%、90% 帧位置）紧密跟踪真值。这一现象的根本原因在于，单流分词器无法同时为低频语义和高频物理保留充分的表示容量。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/001_Figure_1.jpg]]
*Figure 1: Given a text description and a scene video as input, MotionVLA generates motions that closely track the ground truth (GT) across the full sequence (frames at 30%, 60%, and 90% shown). ViMoGen [13], which relies on a single-stream tokenizer, exhibits temporal drift and joint instability that accumulate over time (highlighted in white circles)*

### 主实验结果

**MBench 基准（Table 2）**：MotionVLA 在 Motion-Condition Consistency 上达到 0.55，较 ViMoGen 的 0.53 提升 3.8%；Foot Sliding 降至 0.0049，优于 ViMoGen-light 的 0.0051。在 Motion Generalizability 和 Jitter Degree 上取得次优。值得注意的是，MotionVLA 使用轻量 2B 骨干即达成此结果，而部分基线方法使用了更大模型。

**HumanML3D 文本到运动生成（Table 3）**：MotionVLA 的 Diversity 得分 9.548，与真实数据 9.503 的差距仅 0.045，较典型基线方法将 Diversity gap 缩小超过 50%。同时，MModality 达到 2.821，在生成方法中最高。这验证了双流解耦后，模型既能保留丰富的运动变化，又能维持与文本的语义对齐。

**人类偏好研究（Table 7）**：在 100 个 prompt × 5 位匿名领域专家的双盲随机化评估中，MotionVLA 在整体质量、文本对齐、物理合理性、场景一致性和运动多样性五个维度上均被显著偏好。评估采用 GSB 界面（Figure 5），专家仅观看并比较骨骼动画片段，未收集个人信息，无需 IRB 审批。

### 分词器重建质量分析

Table 4 对比了 DSFT 与单流 DCT+BPE 基线在 HumanML3D 上的重建质量。DSFT（$K_p=25$）的 rFID 为 0.1868，远低于单流基线的 0.9461，同时 Tok./Frame 更紧凑（2.57 vs 3.06）。这直接归因于双流独立截断策略：Base 流仅需 $K_b=5$ 个 DCT 系数即可充分表示低频姿态语义，而 Phys 流使用 $K_p=25$ 保留高频物理动态。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/008_Table_4.jpg]]
*Table 4: DSFT tokenizer reconstruction analysis on HumanML3D. Smaller Tok./Frame indicates a more compact tokenization; lower rRMSE, MPJPE, and rFID are better*

### 消融实验

**骨干规模消融（Table 5）**：模型从 0.8B 放大到 2B 带来最大性能增益（Motion-Condition Consistency 从 0.51 升至 0.55），但进一步放大至 4B 和 9B 收益递减。这表明在当前数据规模和令牌表示的信息带宽下，2B 已接近容量饱和点。

**Phys 流截断长度消融（Table 6）**：增大 $K_p$ 能持续提升物理能量覆盖和重建质量，但 $K_p=30$ 时部分指标开始下降，$K_p=25$ 提供了物理细节保留与序列效率的最佳平衡。这验证了高频流需要更长截断的核心假设，同时也揭示了过度截断可能引入噪声。

### 失败模式与局限性

1. **固定流划分与截断长度**：$K_b=5$、$K_p=25$ 为人工设定，可能未覆盖极端运动类型（如快速旋转、冲击性动作）的频谱分布。
2. **容量缩放瓶颈**：更大骨干未带来持续显著增益，说明当前令牌表示的信息带宽限制了模型容量的有效利用。
3. **泛化能力未验证**：跨数据集和跨场景的物理合理性可能存在偏差，未见环境下的接触约束满足度需要进一步检验。
4. **固定生成顺序**：“先 Base 后 Phys”的相位感知掩码虽保证了结构一致性，但可能不适用于需要交错生成的交互式或在线运动补全任务。

### 关键图表结论汇总

- **Figure 3**：HumanML3D 和 ViMoGen 两个数据集的运动维度在频率域均呈现一致的双峰分离，低频 Base 维度和高频 Phys 维度自然聚类，为双流划分提供了数据驱动的合理性依据。
- **Figure 4**：Base 流在极小 $K$ 下即可达到高能量覆盖，而 Phys 流需要显著更大的 $K$ 才能保留能量，直接支撑了独立截断的必要性。
- **Table 10**：提供了 ViMoGen 276 维和 HumanML3D 263 维运动向量到 Base（位置/旋转）和 Phys（速度）流的逐域划分细节，确保实验可复现。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/014_Table_10.jpg]]
*Table 10: Per-field breakdown of the ViMoGen 276-dim and HumanML3D 263-dim motion vectors into Base*

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/007_Table_3.jpg]]
*Table 3: Text-to-motion results on HumanML3D. ↑: higher is better; ↓: lower is better; →: closer to real is better. For Diversity, best and second best are determined by the distance to the Real score. ‡: GenM3 uses a retrained evaluator on 30 FPS data; GenM3∗ uses only HumanML3D text pairs. §: DisCoRD is applied on top of MoMask; Diversity is not reported in the original paper*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/009_Table_5.jpg]]
*Table 5: Backbone scale ablation on MBench. †: default configuration used in main experiments. ↑/↓: higher/lower is better*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/010_Table_6.jpg]]
*Table 6: DSFT*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/011_Table_7.jpg]]
*Table 7: Human preference study (%) on 100 prompts*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_15142/figures/018_Figure_7.jpg]]
*Figure 7: Real-robot deployment of MotionVLA on a Unitree G1 EDU humanoid robot. Each row shows three exocentric frames from one text-conditioned motion execution, captured at different time steps*

## 定位与知识库关联

### 1. 在运动生成方法谱系中的位置

MotionVLA 处于**离散自回归运动生成**与**多模态条件运动生成**的交叉点上。从生成范式看，其核心继承自将运动生成建模为离散令牌序列预测的路线，代表性工作包括 **T2M-GPT**、**MoMask**、**FineMoGen**、**MotionCraft** 和 **GenM3** 等。与这些方法不同，MotionVLA 的关键创新不在于自回归框架本身，而在于**分词器层面的频谱解耦设计**——通过将异质运动信号分离为低频语义流（Base）和高频物理流（Phys），并分别进行独立的 DCT 截断与 BPE 编码，消除了传统统一码本对高频动态信息的结构性压制。

从条件模态看，MotionVLA 将文本条件扩展为**文本-场景视觉联合条件**，这是其区别于所有纯文本驱动基线（MDM、MotionDiffuse、MoMask、T2M-GPT 等）的关键维度。在同时具备视觉条件的方法中，**ViMoGen** 是最直接的对比对象——两者共享相同的 ViMoGen-228K 训练数据和 MBench 评估基准，但 ViMoGen 采用单流分词器，这正是 MotionVLA 在长序列跟踪稳定性上形成显著优势的根源（Figure 1 中 ViMoGen 出现累积时间漂移和关节不稳定）。

### 2. 核心因果机制与证据强度

**瓶颈识别**：单一共享码本将关节位置（低频主导）与关节速度（高频主导）强制压缩至同一量化空间，固有偏向低频姿态语义，导致高频物理动态信息大量丢失。这是该方法设计的核心动机。

**因果旋钮**：通过频率域分析人为分离 Base（位置/旋转，$K_b=5$ 个 DCT 系数）和 Phys（速度，$K_p=25$ 个 DCT 系数）双流，并独立应用不同截断的 DCT+BPE 进行量化与建模。

**决定性证据**：
- **频谱分离的实证基础**：五个 DCT 系数捕获关节位置 93% 的能量，但仅捕获关节速度 37% 的能量（Figure 4）。这一量化差异直接解释了统一截断为何系统性地牺牲物理动态——若使用 $K=5$ 的统一截断，速度流将丢失约 63% 的能量。
- **双峰分布验证**：在 HumanML3D 和 ViMoGen 两个数据集上，运动维度的低频能量比均呈现一致的双峰分布（Figure 3），表明 Base/Phys 的划分并非特定数据集的偶然现象，而是人体运动频谱的固有结构。
- **定性对比**：Figure 1 提供了直观证据——单流方法（ViMoGen）在长序列生成中随时间累积漂移和关节不稳定，而双流方法能全程跟踪真实值。

这些证据的置信度较高（0.95-0.98），频谱分析和双峰分布在两个独立数据集上得到交叉验证。

### 3. 适用边界与局限

**固定流划分与截断长度**：当前 Base/Phys 的维度划分基于运动向量的语义字段（位置/旋转 vs. 速度），截断长度 $K_b=5$、$K_p=25$ 为固定选择。这一设计可能未覆盖所有运动类型的频谱极端情况——例如，快速爆发性运动（冲刺、跳跃）可能要求更高的 $K_p$，而缓慢仪式性动作可能允许更低的 $K_p$。Table 6 的消融显示 $K_p=30$ 时部分指标开始下降，但这一结论仅基于当前数据分布。

**模型容量缩放瓶颈**：Table 5 表明从 0.8B 放大到 2B 带来最大增益，但进一步放大至 4B 和 9B 收益递减。这暗示当前令牌表示所携带的信息量已接近饱和——更大的骨干网络无法从现有 DSFT 令牌中提取更多有效信息。这是方法层面的一个结构性约束。

**生成顺序的刚性**：双流固定为“先 Base 后 Phys”的生成顺序（通过 phase-aware logit mask 强制），这一设计在离线运动生成场景中合理，但可能不适用于交互式或在线运动补全任务——后者可能需要 Base 和 Phys 令牌的交错生成。

**跨场景泛化未经验证**：所有评估均在 ViMoGen-228K（合成数据为主）和 HumanML3D（实验室动捕）上进行。未见环境下的物理合理性——尤其是足部接触、穿模等物理约束——可能存在偏差。真机部署（Figure 7）仅作为概念验证展示，缺乏系统性的 sim-to-real 评估。

### 4. 开放问题

1. **自适应流分配**：能否通过数据驱动的方法自动学习每个运动维度的流分配，以适应不同运动风格的频谱变化？当前的固定语义划分（位置/旋转 → Base，速度 → Phys）虽然有效，但可能不是最优的——某些旋转维度可能携带高频信息，某些速度维度可能在特定动作中趋于平稳。

2. **3D 几何先验的融入**：如何在保持频谱解耦的同时有效融入场景 3D 几何先验？当前方法仅通过视觉编码器提供场景图像条件，缺乏对场景几何的显式建模，这限制了物理约束（接触、穿模）的满足度。

3. **多人物交互扩展**：该方法能否扩展至交互式多人物运动生成，并支持人物间物理交互的一致性建模？双流设计在单人物场景中验证有效，但多人物的物理交互（如接触力传递、协同平衡）可能要求跨人物的 Phys 流协调。

4. **信息带宽与模型容量的匹配**：若进一步扩大数据规模和令牌表示的信息带宽（如增加 $K_p$ 或引入额外的物理令牌流），是否能在更大骨干模型上获得与推理效率匹配的额外性能提升？当前 2B 的“最佳性价比”结论可能随数据规模和令牌表示能力的提升而改变。

### 5. 知识库定位总结

MotionVLA 的核心知识贡献在于**揭示了人体运动信号的频谱异质性对分词器设计的根本影响**，并提出了双流频率解耦作为解决方案。这一洞察超越了具体的架构选择——无论是 VQ-VAE、BPE 还是其他量化方法，只要涉及统一的码本设计，都可能面临类似的高频信息丢失问题。在运动生成的知识体系中，MotionVLA 将关注点从“如何更好地建模令牌序列”推进到“如何更好地定义令牌本身”，为后续工作提供了分词器层面的设计原则。

## 原文 PDF

![[paperPDFs/arxiv_2026/MotionVLA_Vision-Language-Action_Model_for_Humanoid_Motion.pdf]]
