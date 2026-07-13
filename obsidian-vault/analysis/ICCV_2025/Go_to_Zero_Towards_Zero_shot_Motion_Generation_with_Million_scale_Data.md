---
title: Go to Zero Towards Zero shot Motion Generation with Million scale Data
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Go_to_Zero_Towards_Zero_shot_Motion_Generation_with_Million_scale_Data.pdf
project_link: null
code_link: https://github.com/VankouF/
aliases:
- GZTZSMGMSD
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过构建大规模、高质量、高多样性的动作-文本数据集（MotionMillion，>2000 小时，2M+ 序列），并配合可扩展的模型架构（从 1B 扩展到 7B 参数），解锁涌现的零样本能力。
primary_logic: 采用有限标量量化（FSQ）结合小波变换（wavelet transform）进行高效动作编码，显著抑制了离散编码引起的高频信息丢失和动作抖动；并设计混合注意力（文本双向、动作因果）的自回归 Transformer，实现可扩展且文本对齐的动作生成。
claims:
- MotionMillion 模型在自动指标上大幅超越 ScaMo（FID：10.3 vs. 89.0，R@1：0.79 vs. 0.67）
- 在 MotionMillion-Eval 的人类评估中，7B 模型在文本对齐、物理合理性和动作平滑性上均显著优于 ScaMo-3B
- 定性结果显示，模型能够生成长时间、复杂组合动作（如武术、日常交互），展现出强大的零样本指令遵循能力
- MotionMillion 测试集 上 FID = 10.3 (7B)
---

# Go to Zero Towards Zero shot Motion Generation with Million scale Data

> [!tip] 核心洞察
> 采用有限标量量化（FSQ）结合小波变换（wavelet transform）进行高效动作编码，显著抑制了离散编码引起的高频信息丢失和动作抖动；并设计混合注意力（文本双向、动作因果）的自回归 Transformer，实现可扩展且文本对齐的动作生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 走向零样本：百万级数据驱动的零样本人体动作生成 |
| 英文题名 | Go to Zero Towards Zero shot Motion Generation with Million scale Data |
| 会议/期刊 | ICCV 2025 |
| Links | [Code](https://github.com/VankouF/) · [paper](https://arxiv.org/abs/2507.07095) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MotionMillion |
| Dataset | MotionMillion 测试集, MotionMillion-Eval, HumanML3D |

> [!tip] 效果简介
> - MotionMillion 测试集 上，FID 10.3 (7B) vs 89.0 (ScaMo) (-78.7)；R@1 0.79 (7B) vs 0.67 (ScaMo) (+0.12)。
> - MotionMillion-Eval 上，文本对齐 (Human Eval) 261 (7B) vs 226.6 (ScaMo-3B) (+34.4)。
> - HumanML3D (FSQ重建) 上，MPJPE 41.9 vs 63.3 (ScaMo) (-21.4)。

## 概要

**问题瓶颈**：现有文本驱动的人体动作生成方法严重受限于训练数据规模——主流基准如 HumanML3D、MotionX 仅包含数百小时的动作数据，导致模型过拟合于有限的动作分布，缺乏零样本泛化能力，难以处理分布外（out-of-domain）和复杂组合动作。

**核心调控变量**：本文通过构建大规模、高质量、高多样性的动作-文本数据集 MotionMillion（>2000 小时，2M+ 序列），并配合可扩展的模型架构（从 1B 扩展到 7B 参数），解锁了涌现的零样本动作生成能力。

**方法定位**：MotionMillion 采用有限标量量化（FSQ）结合小波变换进行高效动作编码，有效抑制了离散编码引起的高频信息丢失和动作抖动；设计混合注意力机制的自回归 Transformer——文本端使用双向注意力、动作端使用因果注意力——实现可扩展且文本对齐的动作生成。该方法在方法谱系中属于自回归生成范式，与扩散模型（如 MDM）和 GPT 类方法（如 MotionGPT、T2M-GPT）形成对比，同时在与同类自回归方法 ScaMo-3B 的比较中展现出显著优势。

**主要结果**：
- 在 MotionMillion 测试集上，7B 模型 FID 达到 10.3，相比 ScaMo 的 89.0 大幅降低 78.7；R@1 达到 0.79，提升 0.12（Table 4）。
- 在 MotionMillion-Eval 人类评估中，7B 模型在文本对齐、物理合理性和动作平滑性三个维度上均显著优于 ScaMo-3B（Table 5）。
- 定性结果显示，模型能够生成长时间、复杂组合动作（如武术、日常交互），展现出强大的零样本指令遵循能力（Figure 6）。

**局限性提示**：自动评估指标在模型从 3B 扩展到 7B 时提升趋缓，可能无法全面反映生成质量；人类评估仅与 ScaMo-3B 进行了详细对比，评分者间信度未充分披露；论文未涉及手部和面部动作。

### 问题背景

文本驱动的人体动作生成旨在根据自然语言描述合成逼真的三维人体运动序列，在虚拟人、游戏、影视和具身智能等领域具有广泛应用前景。近年来，基于扩散模型和自回归模型的方法在该任务上取得了显著进展，但现有研究普遍面临一个根本性瓶颈：**训练数据规模严重受限**。

目前主流的动作-文本数据集，如 **HumanML3D** 和 **MotionX**，仅包含数百小时的动捕或伪动捕数据。这种数据稀缺性导致两个关键问题：

1. **模型过拟合**：有限的数据覆盖范围使模型倾向于记忆训练分布，而非学习可泛化的文本-动作映射。
2. **零样本能力缺失**：面对分布外（out-of-domain）和复杂组合动作（如“先向左走两步，然后挥右手，同时单脚跳”）时，现有模型难以生成语义准确且物理合理的运动序列。

### 现有方法缺口

从方法层面审视，现有工作存在以下结构性不足：

- **动作表示依赖逆运动学**：HumanML3D 等主流格式需通过逆运动学（IK）将关节旋转转换为 SMPL 或 BVH 表示，此过程可能引入不可逆的旋转误差，影响动作质量上限。
- **动作分词器的信息损失**：基于 VQ-VAE 或普通有限标量量化（FSQ）的离散编码方案在压缩连续动作时，容易丢失高频细节并引入帧间抖动（jitter），导致生成动作不够平滑。
- **模型架构的可扩展性不足**：多数现有模型采用纯因果注意力机制，文本与动作序列的交互方式未能充分利用双向上下文，限制了复杂语义的理解能力；同时，模型规模通常较小（<3B 参数），未能探索规模扩展带来的涌现能力。
- **评估体系不完善**：自动指标（如 FID、R-precision）在模型规模增大时提升趋缓，可能无法全面反映生成质量，尤其是零样本场景下的文本对齐度和动作物理合理性。

### 本文动机

针对上述瓶颈，本文的核心动机在于：**通过构建大规模、高质量、高多样性的动作-文本数据集，并配合可扩展的模型架构，解锁文本驱动动作生成的零样本涌现能力**。

具体而言，本文提出以下关键思路：

- **数据规模化**：从海量单目视频中自动化提取高质量人体运动，构建包含超过 2000 小时、200 万+ 序列的 **MotionMillion** 数据集，从根本上缓解数据稀缺问题。
- **高效动作编码**：采用有限标量量化（FSQ）结合小波变换（wavelet transform）进行动作分词，在保持离散编码简洁性的同时抑制高频信息丢失和动作抖动。
- **可扩展生成架构**：设计混合注意力机制（文本双向、动作因果）的自回归 Transformer，将模型规模从 1B 扩展到 7B 参数，探索规模对零样本指令遵循能力的影响。

如 **Figure 1** 所示，本文方法旨在处理分布外和复杂组合动作，实现“走向零样本”的动作生成目标。

## 核心方法与创新机理

本文的核心创新围绕“数据—表示—架构”三轴联动展开，旨在突破现有文本驱动动作生成模型因训练数据规模受限而导致的零样本泛化瓶颈。其关键创新点可凝练为以下四个维度：

### 1. 百万级高质量动作-文本数据集 MotionMillion

现有方法长期受限于 HumanML3D、MotionX 等小规模数据集，模型易过拟合且难以处理分布外及复杂组合动作。本文构建了 MotionMillion 数据集，包含超过 **2000 小时**的人体动作片段和 **200 万+** 动作序列，规模远超以往数据集（Table 1）。

数据构建管线（Figure 2）包含六个关键阶段：镜头分割、人体检测、边界框置信度过滤、转场过滤、SMPL 动作估计与动作过滤。其中，动作过滤阶段引入两项关键指标以确保数据质量：
- **方向突变检测**：通过计算连续帧间全局旋转矩阵的轴角变化 $\Delta \theta = Transform(R_i R_{i-1}^{-1})$，过滤镜头方向突变引入的伪影（Eq. 1）。
- **抖动过滤**：引入加速度的时间导数 $jerk = \ddot{J}_i^*$ 作为动作平滑度指标（Eq. 2），MotionMillion 在该指标上显著优于 MotionX 和 HumanML3D（Figure 4），表明其动作更加平滑流畅。

### 2. 修正的动作表示：摆脱逆运动学依赖

传统 HumanML3D 格式依赖逆运动学（IK）过程，可能引入错误旋转。本文提出修正后的动作表示：

$$x^i = \{\dot{r}^x, \dot{r}^z, \dot{r}^a, p^i, v^i, r^i\}$$

该表示直接包含根关节的线速度与角速度、局部关节位置、速度及旋转，无需 IK 即可无损转换为相对旋转表示（Sec. 4.1），从表示层面消除了误差来源。

### 3. FSQ + 小波变换的高效动作分词器

动作分词是离散化生成的关键环节。本文采用有限标量量化（FSQ）替代传统 VQ-VAE，其量化公式为：

$$\hat{\mathbf{z}} = \mathcal{Q}(\mathbf{z}) = \mathrm{round}(f(\mathbf{z}) \cdot (L-1))$$

仅使用重构损失 $\mathcal{L} = \| \mathbf{m} - \mathrm{Dec}(\mathbf{z}_q) \|_2^2$ 训练，无需 VQ-VAE 的辅助损失（Eq. 3-4）。

**关键创新在于将小波变换与 FSQ 结合**：在编码前对连续动作进行小波变换预处理，解码后执行逆小波变换重构。这一设计有效抑制了离散编码引起的高频信息丢失和动作抖动。消融实验（Table 3）表明，使用小波变换后：
- MPJPE 从 46.8 降至 45.5
- 平均加速度误差（Mean Acc）从 6.0 降至 4.0
- 最大加速度误差（Max Acc）从 15.0 降至 12.0

在跨数据集重建评估中，本文的 FSQ 模型在 HumanML3D、MotionX 和 MotionMillion 上的 MPJPE 分别为 41.9、57.4 和 45.5，全面优于 ScaMo 的 63.3、84.1 和 88.9（Table 2）。

### 4. 混合注意力机制与可扩展架构

模型架构（Figure 5）采用自回归 Transformer，其核心创新在于**混合注意力设计**：
- **文本 token**：使用双向注意力，充分捕捉文本语义上下文
- **动作 token**：使用因果注意力，保持自回归生成的时序一致性

损失函数为标准的下一个动作 token 预测交叉熵：

$$\mathcal{L} = -\sum_{i=1}^{n} \log p(\hat{m}_i | \mathbf{m}_{<i}, T_1, ..., T_w)$$

模型从 1B 参数扩展至 7B，展现出涌现的零样本指令遵循能力。在 MotionMillion 测试集上，7B 模型在 FID（10.3 vs. 89.0）和 R@1（0.79 vs. 0.67）上均大幅超越 ScaMo 基线（Table 4）。人类评估进一步证实，7B 模型在文本对齐、物理合理性和动作平滑性三个维度上均显著优于 ScaMo-3B（Table 5）。

### 方法谱系与知识库定位

本文方法可视为对以下技术路线的系统改进：

| 技术组件 | 基线方法 | 本文改进 | 改进机理 |
|---------|---------|---------|---------|
| 动作分词器 | VQ-VAE / 普通 FSQ（如 ScaMo） | FSQ + 小波变换 | 小波变换在频域分离高低频成分，缓解离散化对高频细节的破坏 |
| 注意力机制 | 纯因果注意力（如 T2M-GPT、MotionGPT） | 混合注意力（文本双向 + 动作因果） | 文本双向注意力增强文本-动作对齐，动作因果注意力保持生成连贯性 |
| 模型规模 | ScaMo-3B / 1B 级别 | 扩展至 7B | 规模扩展解锁零样本涌现能力，但 3B→7B 的自动指标提升趋缓 |
| 动作表示 | HumanML3D 格式（依赖 IK） | 直接包含根速度与局部运动学量 | 消除 IK 误差累积，实现无损表示转换 |

**证据强度评估**：
- FSQ+小波变换的有效性有消融实验（Table 3）和跨数据集重建对比（Table 2）双重支撑，证据强度高。
- 混合注意力的消融证据未在提供的分析中明确出现，该点需人工核实原文是否包含注意力机制的独立消融。
- 规模扩展的收益在自动指标（Table 4）和人类评估（Table 5）中均有体现，但 3B→7B 的自动指标提升微小，提示现有自动指标可能无法充分刻画生成质量的提升。

**未解决问题**：
- 小波变换与 FSQ 结合抑制高频丢失的内在机理是否具有普适性，能否推广至其他离散编码场景？
- 模型规模增大对物理合理性和动作平滑性提升不显著，是否需要引入显式物理约束模块？
- 自动指标（FID、R-precision）在模型规模增大时趋于饱和，如何设计更灵敏的零样本动作生成评估指标？

MotionMillion 的整体框架围绕“数据驱动 + 规模扩展”两条主线构建，旨在通过百万级高质量动作-文本数据与可扩展的自回归 Transformer，解锁零样本文本到动作生成的涌现能力。系统由两大核心阶段串联而成：**大规模数据构建管线** 与 **可扩展动作生成模型**。

### 数据构建管线

为突破现有数据集（如 HumanML3D、MotionX）在规模与多样性上的瓶颈，MotionMillion 设计了一套从单目视频中自动提取高质量人体动作的六阶段处理管线（Figure 2）：

![[assets/figures/papers/paper_list_l1882_Go_to_Zero_Towards_Zero_shot_Motion_Generation_with_Million_scale_Data/figures/002_Figure_2.jpg]]
*Figure 2: Data Construction Pipeline of MotionMillion. We can obtain high-quality human motion from a monocular video via our six processing stages, i.e. Shot Segmentation, Human Detection, Video Filtering, SMPL Motion Estimation and Motion Filtering*

1. **镜头分割（Shot Segmentation）**：使用 PySceneDetect 将视频切分为单场景片段，每片段限制最多 200 帧以保证时序连贯性。
2. **人体检测（Human Detection）**：对每个片段进行人体边界框检测。
3. **边界框置信度过滤（Bounding Box Confidence Filtering）**：剔除低置信度检测结果。
4. **转场过滤（Transition Filtering）**：通过计算连续帧间全局旋转矩阵的轴角变化 $\Delta \theta = \mathrm{Transform}(R_i R_{i-1}^{-1})$，检测镜头方向突变并过滤不连贯片段。
5. **SMPL 动作估计（SMPL Motion Estimation）**：从过滤后的视频中估计 SMPL 参数化人体动作。
6. **动作过滤（Motion Filtering）**：引入加速度的时间导数——加加速度（jerk）指标 $\mathrm{jerk} = \ddot{J}_i^*$ 衡量动作平滑度，滤除抖动过大的序列。

经此管线，MotionMillion 数据集包含超过 2000 小时的视频片段、200 万条以上动作序列，在语义多样性与姿态多样性上覆盖广泛的室内外人体动作（Figure 3），且加加速度值显著低于 MotionX 和 HumanML3D（Figure 4），表明其动作更加平滑。

![[assets/figures/papers/paper_list_l1882_Go_to_Zero_Towards_Zero_shot_Motion_Generation_with_Million_scale_Data/figures/003_Figure_3.jpg]]
*Figure 3: Overview of MotionMillion. This dataset exhibits extensive semantic and pose diversity, encompassing a broad spectrum of indoor and outdoor human motions*

### 动作生成模型

生成模型采用“编码-生成”两阶段架构（Figure 5）：

![[assets/figures/papers/paper_list_l1882_Go_to_Zero_Towards_Zero_shot_Motion_Generation_with_Million_scale_Data/figures/006_Figure_5.jpg]]
*Figure 5: Overview of our scalable model architecture, which utilize FSQ as a motion tokenizer and an autoregressive transformer to generate the motion from the given text*

**阶段一：高效动作分词（Efficient Motion Tokenization）**

- **动作表示**：摒弃依赖逆运动学的传统格式，采用直接包含根速度、局部关节位置/速度/旋转的修正表示 $x^i = \{\dot{r}^x, \dot{r}^z, \dot{r}^a, p^i, v^i, r^i\}$，可无损转换为相对旋转。
- **有限标量量化（FSQ）**：将连续动作潜变量 $\mathbf{z}$ 经归一化后离散化为 $L$ 个均匀整数 $\hat{\mathbf{z}} = \mathcal{Q}(\mathbf{z}) = \mathrm{round}(f(\mathbf{z}) \cdot (L-1))$，训练时仅使用重构损失 $\mathcal{L} = \| \mathbf{m} - \mathrm{Dec}(\mathbf{z}_q) \|_2^2$，无需 VQ-VAE 的辅助损失。
- **小波变换增强**：在 FSQ 编码前对动作进行小波变换预处理，解码后进行逆小波变换，有效抑制离散编码引起的高频信息丢失与动作抖动（Table 3 消融实验证实 MPJPE 从 46.8 降至 45.5，平均加速度误差从 6.0 降至 4.0）。

**阶段二：可扩展动作生成（Scalable Motion Generation）**

- **文本编码**：使用 T5-XL 编码器将输入文本编码为词元序列。
- **混合注意力 Transformer**：堆叠多个混合注意力块（HAB），每个块包含 RMS-Norm、混合注意力层和前馈网络。注意力机制采用 **文本双向、动作因果** 的混合策略，使文本 token 之间可双向交互以充分理解语义，动作 token 则保持因果掩码以支持自回归生成。
- **分类头与损失**：最终分类头输出下一个动作 token 的 logits，通过交叉熵损失优化：
  $$\mathcal{L} = -\sum_{i=1}^{n} \log p(\hat{m}_i \mid \mathbf{m}_{<i}, T_1, \dots, T_w)$$

模型规模可从 1B 参数扩展至 7B 参数。在 MotionMillion 测试集上，7B 模型的 FID 达到 10.3（ScaMo 为 89.0），R@1 达到 0.79（ScaMo 为 0.67），展现出显著的性能优势（Table 4）。定性结果显示，模型能够生成长时间、复杂组合动作（如武术、日常交互），具备强大的零样本指令遵循能力（Figure 6）。

### 动作表示

MotionMillion 采用一种无需逆运动学（IK）即可直接与 SMPL/BVH 表示无损转换的动作表示。第 $i$ 帧的姿势定义为：

$$x^{i} = \{\dot{r}^{x}, \dot{r}^{z}, \dot{r}^{a}, p^{i}, v^{i}, r^{i}\}$$

其中：
- $\dot{r}^{x}, \dot{r}^{z}, \dot{r}^{a}$：根节点在 $x$、$z$ 方向的线速度及绕 $y$ 轴的角速度；
- $p^{i}$：局部关节位置；
- $v^{i}$：局部关节速度；
- $r^{i}$：局部关节旋转。

该表示直接编码了根运动信息，避免了 HumanML3D 格式中因逆运动学引入的旋转错误（Sec. 4.1）。

### 高效动作分词：FSQ + 小波变换

模型采用有限标量量化（Finite Scalar Quantization, FSQ）将连续动作离散化为 token 序列。FSQ 的量化过程为：

$$\hat{\mathbf{z}} = \mathcal{Q}(\mathbf{z}) = \mathrm{round}\left(f(\mathbf{z}) \cdot (L-1)\right)$$

其中 $f(\mathbf{z})$ 将潜变量 $\mathbf{z}$ 归一化到 $[0,1]$，$\mathrm{round}$ 操作将其映射到 $L$ 个均匀整数级别。

FSQ 的训练仅使用重构损失，无需 VQ-VAE 中的码本损失或承诺损失：

$$\mathcal{L} = \| \mathbf{m} - \mathrm{Dec}(\mathbf{z}_q) \|_2^2$$

**关键改进：小波变换预处理。** 在 FSQ 编码前对动作序列施加小波变换，解码后施加逆小波变换。消融实验（Table 3）表明，引入小波变换后：
- MPJPE 从 46.8 降至 45.5；
- 平均加速度误差（Mean Acc）从 6.0 降至 4.0；
- 最大加速度误差（Max Acc）从 15.0 降至 12.0。

这表明小波变换有效抑制了离散编码引起的高频信息丢失和动作抖动（Sec. 4.2）。

### 可扩展动作生成：混合注意力自回归 Transformer

生成模型采用自回归 Transformer 架构，核心组件如下：

**文本编码器。** 使用 T5-XL 将输入文本编码为词元序列 $T_1, \dots, T_w$（Sec. 4.3）。

**混合注意力块（Hybrid Attention Block, HAB）。** 每个 HAB 包含 RMS-Norm、混合注意力层和前馈网络。混合注意力的设计是：
- **文本部分**：双向注意力，使文本 token 之间可充分交互；
- **动作部分**：因果注意力，保证自回归生成的时序因果性；
- **跨模态交互**：动作 token 可关注所有文本 token，实现文本-动作对齐。

**分类头与损失函数。** 最终分类头输出下一个动作 token 的 logits，训练目标为交叉熵损失：

$$\mathcal{L} = -\sum_{i=1}^{n} \log p(\hat{m}_i | \mathbf{m}_{<i}, T_1, \dots, T_w)$$

即给定既往动作 token $\mathbf{m}_{<i}$ 和全部文本 token，预测下一动作 token $\hat{m}_i$ 的负对数似然（Eq. 5）。

**模型规模扩展。** 论文将模型从 1B 参数扩展至 7B，自动指标（FID、R@1）持续改善，但 3B 到 7B 的提升趋缓（Table 4），显示自动指标可能无法完全捕捉生成质量的变化。

### 数据构建中的关键公式

在 MotionMillion 数据集的运动过滤阶段，引入了两个关键度量：

**方向突变检测。** 通过连续帧间的全局旋转矩阵计算轴角变化：

$$\Delta\theta = \mathrm{Transform}(R_i R_{i-1}^{-1})$$

用于检测镜头方向突变，过滤不稳定的运动片段（Eq. 1）。

**抖动度量。** 定义 jerk 为加速度的时间导数：

$$\mathrm{jerk} = \ddot{J}_i^*$$

用于量化动作平滑度。MotionMillion 在该指标上显著低于 MotionX 和 HumanML3D（Figure 4），表明其动作更平滑（Eq. 2）。

![[assets/figures/papers/paper_list_l1882_Go_to_Zero_Towards_Zero_shot_Motion_Generation_with_Million_scale_Data/figures/009_Table_3.jpg]]
*Table 3: Ablation on whether to use wavelet transformation during training the FSQ model, where Acc represents the acceleration*

![[assets/figures/papers/paper_list_l1882_Go_to_Zero_Towards_Zero_shot_Motion_Generation_with_Million_scale_Data/figures/008_Table_2.jpg]]
*Table 2: MPJPE of reconstruction comparison across different datasets, where ScaMo’s FSQ model and ours are trained on MotionUnion and MotionMillion, respectively*

## 实验与关键发现

### 核心实验结果

MotionMillion 模型在 MotionMillion 测试集上的自动指标评估结果（Table 4）表明，其生成质量显著超越基线方法 ScaMo。具体而言，7B 参数量的 MotionMillion 模型取得了 **FID 10.3**，而 ScaMo 的 FID 为 89.0，降幅达 78.7，显示出生成分布与真实分布的高度一致性。在检索精度指标上，MotionMillion-7B 的 **R@1 达到 0.79**，较 ScaMo 的 0.67 提升了 0.12，反映出更强的文本-动作对齐能力。

![[assets/figures/papers/paper_list_l1882_Go_to_Zero_Towards_Zero_shot_Motion_Generation_with_Million_scale_Data/figures/007_Table_4.jpg]]
*Table 4: Quantitative comparison of ScaMo and our models of different sizes on MotionMillion*

人类评估进一步验证了上述结论。在 MotionMillion-Eval 的 7 类 126 个提示词上（Table 5），MotionMillion-7B 在**文本对齐**维度上获得 261 分，显著高于 ScaMo-3B 的 226.6 分（提升 34.4）。然而，在物理合理性与动作平滑性两个维度上，7B 模型相对 ScaMo-3B 的优势并不显著，这暗示单纯增大模型规模对这两类质量的提升有限。详细的胜负对比（Table 6）以绿色/黄色/白色单元格标注了 7B 模型在各类别上的胜/平/负情况，直观呈现了其在多数类别上的优势。

定性结果（Figure 6）展示了模型处理复杂组合文本指令的能力，能够生成长时间、连贯的武术及日常交互动作，体现了零样本条件下的指令遵循能力。

### 消融实验与分析

**小波变换对 FSQ 重建质量的影响**（Table 3）：在 FSQ 训练中引入小波变换后，MotionMillion 上的重建 MPJPE 从 46.8 降至 45.5，平均加速度误差（Mean Acc）从 6.0 降至 4.0，最大加速度误差（Max Acc）从 15.0 降至 12.0。这表明小波变换有效抑制了 FSQ 离散编码引入的高频信息丢失和动作抖动，是提升重建平滑性的关键设计。

**FSQ 重建的跨数据集泛化**（Table 2）：MotionMillion 的 FSQ 模型在 HumanML3D、MotionX 和 MotionMillion 三个数据集上的重建 MPJPE 分别为 41.9、57.4、45.5，均显著低于 ScaMo 的 FSQ 模型（63.3、84.1、88.9）。这验证了所提动作表示（无需逆运动学，直接包含根速度、局部关节位置/速度/旋转）和 FSQ 编码方案在重建精度上的整体优势。

**模型规模的扩展效应**（Table 4）：从 1B 扩展到 7B，FID 和 R-precision 持续改善，但 3B 到 7B 的指标提升幅度明显收窄。论文明确指出，自动指标可能无法完全反映生成质量，这一现象在人类评估中得到呼应——规模增大主要提升文本对齐，而对物理合理性和动作平滑性的增益不显著。

### 评估的局限性与公平性说明

人类评估仅与 ScaMo-3B 进行了细粒度对比，未将 MDM、MotionGPT、T2M-GPT 等其他基线纳入相同粒度的比较。此外，评分者间信度和具体评估协议细节在正文中未充分披露，这些因素可能影响人类评估结论的稳健性。读者在引用人类评估结果时需注意上述限制。

自动指标（FID、R-precision）在模型从 3B 扩展到 7B 时提升趋缓，结合人类评估中物理合理性和动作平滑性未显著改善的事实，表明现有自动指标可能对零样本动作生成质量的敏感度不足，需要更鲁棒的评估方案。

## 定位与知识库关联

### 1. 基线对比与谱系定位

MotionMillion 的核心定位是**面向零样本泛化的可扩展自回归动作生成模型**，其方法谱系可沿两条主线展开：**动作分词与表示**，以及**生成架构与规模扩展**。

#### 1.1 动作分词与表示

在动作离散化方面，MotionMillion 直接对标 **ScaMo**（ScaMo-3B），后者同样采用有限标量量化（FSQ）进行动作编码。然而，MotionMillion 在两个关键维度上实现了突破：

- **动作表示修正**：ScaMo 沿用 HumanML3D 格式，依赖逆运动学（IK）获取 SMPL/BVH 表示，该过程可能引入旋转误差。MotionMillion 采用修正后的直接表示 $x^i = \{\dot{r}^x, \dot{r}^z, \dot{r}^a, p^i, v^i, r^i\}$，包含根速度、局部关节位置/速度/旋转，可无损转换为相对旋转，从根本上规避了 IK 误差（Sec. 4.1）。

- **小波变换增强**：针对 FSQ 离散化导致的高频信息丢失和动作抖动问题，MotionMillion 引入小波变换预处理与逆变换（Sec. 4.2, Table 3）。消融实验表明，使用小波变换后 FSQ 重建的 MPJPE 从 46.8 降至 45.5，平均加速度误差从 6.0 降至 4.0，最大加速度误差从 15.0 降至 12.0，有效抑制了抖动现象。

在重建质量上，MotionMillion 的 FSQ 模型在 HumanML3D 数据集上取得 MPJPE 41.9，显著优于 ScaMo 的 63.3（Table 2），验证了上述改进的有效性。早期方法如 **MotionGPT** 和 **T2M-GPT** 同样采用 VQ-VAE 进行动作分词，但受限于码本崩溃和训练不稳定性，MotionMillion 的 FSQ 方案无需辅助损失（Eq. 4），训练更简洁。

#### 1.2 生成架构与规模扩展

在生成范式上，MotionMillion 属于**自回归 Transformer 家族**，与 **T2M-GPT**、**MotionGPT**、**ScaMo** 同源，但与 **MDM** 等扩散模型形成方法分叉。MotionMillion 的架构创新在于：

- **混合注意力机制**：区别于传统自回归模型采用的纯因果注意力，MotionMillion 设计混合注意力块（HAB），对文本序列施加双向注意力，对动作序列保持因果注意力（Fig. 5, Sec. 4.3）。这一设计使文本编码更充分，同时保持动作生成的自回归特性。

- **规模扩展策略**：MotionMillion 将模型参数从 1B 扩展至 7B，是目前动作生成领域已知的最大规模自回归模型。Table 4 显示，FID 从 1B 的 23.4 持续下降至 7B 的 10.3，R@1 从 0.74 提升至 0.79，验证了规模扩展对生成质量的提升作用。然而，3B 到 7B 的自动指标提升趋缓（FID: 12.1 → 10.3），暗示现有指标可能无法充分捕捉生成质量的边际改善。

### 2. 适用边界与局限

#### 2.1 明确适用场景

- **零样本复杂组合动作生成**：MotionMillion 在分布外和复杂组合文本指令上展现出涌现能力（Figure 6），适用于需要理解长文本、多步骤动作描述的场景。
- **大规模数据驱动场景**：得益于 MotionMillion 数据集（>2000 小时，2M+ 序列），模型在数据覆盖度和多样性上具有优势。

#### 2.2 已知局限

1. **动作覆盖范围受限**：论文明确仅关注全身动作，忽略手部和面部表情，限制了其在需要精细交互（如手语、乐器演奏）场景中的应用。

2. **离散编码的信息瓶颈**：尽管小波变换缓解了 FSQ 的抖动问题，但离散编码本身带来的信息丢失可能仍会影响某些高频动作（如快速旋转、击打）的重建精度。

3. **规模扩展的边际效益递减**：Table 5 的人类评估显示，增大模型规模主要提升文本对齐（7B vs ScaMo-3B: 261 vs 226.6），对物理合理性（243.1 vs 238.4）和动作平滑性（242.7 vs 233.3）的提升不显著，提示单纯增加参数可能不足以解决物理约束问题。

4. **评估体系的不足**：自动指标（FID、R-precision）在 3B 到 7B 之间提升趋缓，可能无法全面反映生成质量；人类评估仅与 ScaMo-3B 进行了详细对比（Table 6），未与其他基线（MDM、MotionGPT、T2M-GPT）进行同粒度比较，且评分者间信度未披露。

### 3. 开放问题

1. **小波变换与 FSQ 的结合机理**：小波变换具体如何减轻离散编码中的高频信息丢失？其内在机制是否具有跨任务、跨模态的普适性？能否推广至其他 VQ 类方法？

2. **物理合理性的提升路径**：模型规模增大对物理合理性和动作平滑性提升不显著，是否需要引入显式的物理约束模块（如物理模拟器、接触约束）或专门的损失函数？

3. **面向零样本的评估指标设计**：现有自动指标在多大程度上无法反映零样本生成质量？应如何设计更灵敏、更鲁棒的评估指标，特别是针对组合泛化和指令遵循能力？

4. **数据质量的下游影响**：MotionMillion 数据集虽经过六阶段过滤，但源自网络视频，可能存在未被检测的噪声、标注偏差或文化偏见，这些因素在多大程度上会影响下游任务的公平性和泛化性？

5. **全人体运动生成的扩展**：如何处理手部和面部动作以实现完全的人体运动生成？这可能需要额外的数据来源、更精细的动作表示以及多尺度编码策略。

## 原文 PDF

![[paperPDFs/ICCV_2025/Go_to_Zero_Towards_Zero_shot_Motion_Generation_with_Million_scale_Data.pdf]]
