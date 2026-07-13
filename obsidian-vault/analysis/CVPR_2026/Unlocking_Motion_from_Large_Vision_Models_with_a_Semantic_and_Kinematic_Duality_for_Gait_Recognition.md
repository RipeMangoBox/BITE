---
title: Unlocking Motion from Large Vision Models with a Semantic and Kinematic Duality for Gait Recognition
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unlocking_Motion_from_Large_Vision_Models_with_a_Semantic_and_Kinematic_Duality_for_Gait_Recognition.pdf
project_link: "https://zbhuang.com/gait-max"
code_link: null
aliases:
- UMFLVMSKDGR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 高斯位置嵌入（GauPE）为注意力机制提供部位位置、形状和方向的几何先验，从而实现对长程部位轨迹的精确建模；条件去相关损失（CDLoss）利用文本描述显式迫使步态嵌入与扰动因素统计去相关。
primary_logic: 将语义总结与运动学过程统一在一个双分支框架中：运动学分支持续跟踪身体部位的时空轨迹，并通过GauPE注入形状与位置信息；同时利用CDLoss和GCaption提供的自然语言描述，在嵌入空间中解耦身份与外观变化，实现鲁棒性大幅提升。
claims:
- GaitMax在多个数据集上显著超越现有最佳方法，尤其在跨域场景下（如CASIA-B上CL条件比BigGait提升+12.6%），表明运动学建模和扰动解耦的共同作用。
- 消融实验证实GauPE比RoPE带来+3.1%的平均Rank-1提升，CDLoss在所有属性下提升+11.0%，验证了每个组件的贡献。
- CCPG (in-domain) 上 Mean Rank-1 accuracy (%) = 89.6 (GaitMax)
- CCGR MINI (in-domain) 上 Rank-1 / mAP / mINP = 83.6 / 74.2 / 62.2 (GaitMax)
---

# Unlocking Motion from Large Vision Models with a Semantic and Kinematic Duality for Gait Recognition

> [!tip] 核心洞察
> 将语义总结与运动学过程统一在一个双分支框架中：运动学分支持续跟踪身体部位的时空轨迹，并通过GauPE注入形状与位置信息；同时利用CDLoss和GCaption提供的自然语言描述，在嵌入空间中解耦身份与外观变化，实现鲁棒性大幅提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用语义与运动学双重性从大规模视觉模型中解锁运动用于步态识别 |
| 英文题名 | Unlocking Motion from Large Vision Models with a Semantic and Kinematic Duality for Gait Recognition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Huang_Unlocking_Motion_from_Large_Vision_Models_with_a_Semantic_and_CVPR_2026_paper.html) · [Project](https://zbhuang.com/gait-max) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GaitMax |
| Dataset | CCPG, CCGR MINI, CASIA-B, SUSTech1K |

> [!tip] 效果简介
> - CCPG (in-domain) 上，Mean Rank-1 accuracy (%) 89.6 (GaitMax) vs 89.5 (DenoisingGait) / 87.2 (BigGait) (+0.1 / +2.4)。
> - CCGR MINI (in-domain) 上，Rank-1 / mAP / mINP 83.6 / 74.2 / 62.2 (GaitMax) vs 80.7 / 65.8 / 59.8 (BigGait) (+2.9 / +8.4 / +2.4)。
> - CASIA-B (out-of-domain, trained on CCPG) 上，Rank-1 accuracy (%) per condition: NM / BG / CL / Mean 85.6 / 86.9 / 46.2 / 72.9 (GaitMax) vs 77.4 / 71.5 / 33.6 / 60.8 (BigGait) (+8.2 / +15.4 / +12.6 / +12.1)。

## 概要

步态识别在远距离身份认证中具有独特优势，但现有方法长期受困于两种范式的割裂：**语义范式**（如GaitSet、BigGait）对帧序列进行顺序不变的全局池化，虽能捕获结构上下文，却彻底丢弃了步态作为时序过程的运动学动态；**运动学范式**（如基于光流的方法）虽保留了时序信息，却易受噪声干扰且缺乏长程建模能力。两者均难以同时捕获全局上下文与细粒度时空动态，且容易过拟合到衣着、视角等扰动因素，导致跨域泛化能力不足。

针对这一瓶颈，本文提出 **GaitMax**——一个统一语义与运动学双重性的步态识别框架。其核心洞察在于：将语义总结与运动学过程统一在一个双分支框架中，运动学分支持续跟踪身体部位的时空轨迹，通过**高斯位置嵌入（GauPE）**注入部位的位置、尺度和方向几何先验；同时利用**条件去相关损失（CDLoss）**与**GCaption**数据集提供的自然语言描述，在嵌入空间中显式解耦身份与外观变化。

实验结果表明，GaitMax在多个基准上显著超越现有最佳方法。在域内评估中，CCPG上达到89.6%的平均Rank-1准确率，CCGR MINI上mAP提升+8.4%；在跨域泛化场景下优势更为突出——CASIA-B上CL条件相比BigGait提升**+12.6%**，SUSTech1K上提升**+11.3%**，验证了运动学建模与扰动解耦的共同作用对鲁棒性的关键贡献。消融实验进一步证实，GauPE相比标准RoPE带来+3.1%的平均提升，CDLoss在同时使用多个扰动属性时提升**+11.0%**。

步态识别旨在通过个体的行走模式进行身份辨识，因其远距离、非侵入的特性在安防监控等领域具有重要应用价值。然而，现实场景中衣着变化、携带物品、视角差异等扰动因素的存在，使得步态识别系统的鲁棒性面临严峻挑战。当前主流的步态识别方法可归纳为两大范式，二者均存在结构性缺陷。

**语义范式**是目前占据主导地位的方法路线，以 **GaitSet**、**GaitPart**、**GaitGL** 以及 **BigGait**（Ye et al., CVPR 2024）等为代表。这类方法将逐帧的运动线索编码为顺序不变的全局嵌入，通过时序池化丢弃帧间顺序，从而捕获整体结构上下文。其核心优势在于对帧率变化和序列长度的鲁棒性，但代价是**完全丧失了细粒度的时序动态信息**——行走过程中肢体运动的节奏、加速度、协调模式等运动学特征被平均化抹去。

**运动学范式**则试图通过显式建模时序依赖来弥补上述缺陷，典型方法如 **DenoisingGait**（Jin et al., CVPR 2025）和 **MultiGait++**（Jin et al., AAAI 2025），它们依赖光流或去噪机制提取运动线索。然而，光流本身对噪声高度敏感，且缺乏长程时空建模能力，难以捕获跨越数秒的完整步态周期动态。

**核心瓶颈**在于：语义范式丢弃运动学动态，运动学范式缺乏全局上下文与抗噪能力，两者均无法同时实现全局结构理解与细粒度运动过程建模。更严重的是，两种范式都容易过拟合到衣着、视角等扰动因素，导致跨域泛化性能急剧下降。

针对上述缺口，本文提出 **GaitMax**，其核心动机是通过**语义与运动学的双重性**统一两大范式：一方面保留语义分支的全局上下文捕获能力，另一方面引入人体中心化的运动学分支，持续跟踪身体部位的时空轨迹，实现长程精确运动理解。同时，为抑制扰动因素的干扰，GaitMax 利用自然语言描述显式解耦步态嵌入与外观变化，从而在跨域场景下实现鲁棒性的大幅提升。

## 核心方法与创新机理

GaitMax 的核心创新在于通过**双分支统一框架**同时捕获全局语义与细粒度运动学动态，并引入**条件去相关损失**实现步态嵌入与扰动因素的显式解耦。相对于现有方法，GaitMax 在以下四个关键维度上实现了范式性突破。

### 1. 双分支语义-运动学统一表示

现有步态识别方法长期分裂为两个互不兼容的范式。**语义范式**（如 **GaitSet**、**GaitPart**、**GaitGL**、**BigGait** (Ye et al., CVPR 2024)）通过时序均值池化将帧级运动线索压缩为顺序不变的全局嵌入，能捕获整体结构上下文，但彻底丢弃了步态作为时序过程的动态信息。**运动学范式**（如 **DenoisingGait** (Jin et al., CVPR 2025)、**MultiGait++** (Jin et al., AAAI 2025)）依赖光流等显式运动表征，虽能建模时序变化，却易受噪声干扰且缺乏长程建模能力。

GaitMax 的**双分支架构**从根本上弥合了这一鸿沟：
- **语义分支**（Figure 2 蓝色区域）保留顺序不变的全局上下文编码，通过时序均值池化与水平金字塔池化产生语义表示 $\mathbf{R}_s$；
- **运动学分支**（Figure 2 红色区域）持续跟踪身体部位的时空轨迹，通过逐部位时序建模与联合感知模块产生运动学表示 $\mathbf{R}_k$；
- 最终步态嵌入 $\mathbf{R}$ 由两者拼接而成，使模型同时掌握“整体结构”与“动态过程”。

这一统一设计使得 GaitMax 在域内 CCPG 数据集上超越先前最佳的 RGB 方法 BigGait 达 +2.4%（Mean Rank-1），在多模态方法 MultiGait++ 基础上再提升 +2.2%（Table 2）。更关键的是，在跨域评估中（Table 3），GaitMax 在 CASIA-B 的 CL 条件下比 BigGait 提升 **+12.6%**，在 SUSTech1K 的 CL 条件下提升 **+11.3%**，充分验证了运动学建模对泛化能力的决定性贡献。

### 2. 高斯位置嵌入（GauPE）：形状与方向的几何先验

传统位置编码（如 RoPE）仅编码 token 的绝对或相对位置，无法为注意力机制提供关于**部位形态**的信息。GaitMax 提出的 **GauPE** 通过力矩匹配将注意力图参数化为高斯协方差椭圆，从中提取三类几何信息：
- **质心坐标** $(\mu_x, \mu_y)$：编码部位空间位置；
- **方差** $(\sigma_x^2, \sigma_y^2)$：编码部位尺度；
- **协方差** $\sigma_{xy}$：编码部位方向。

这些参数经旋转变换后注入部位特征，形成几何增强嵌入 $\bar{\mathbf{m}}$（Eq. 5）。Figure 3 的可视化直观展示了注意力图与高斯椭圆之间的对应关系——椭圆中心、长轴、短轴精确刻画了部位的定位与形变。

消融实验（Table 6）证实，GauPE 相比 RoPE 带来 **+3.1%** 的平均 Rank-1 提升，证明形状与方向信息对长程部位轨迹建模不可或缺。

### 3. 条件去相关损失（CDLoss）：嵌入空间的扰动解耦

现有方法仅依赖身份标签监督（交叉熵 + 三元组损失 $\mathcal{L}_{\mathrm{id}}$），缺乏对衣着、视角、携带物等扰动因素的显式约束，导致嵌入空间容易被外观变化污染，跨域性能急剧下降。

CDLoss 的核心机制是**在嵌入空间中强制步态表示与扰动因素统计独立**。具体而言，给定步态嵌入对的距离 $\mathcal{D}(\mathbf{R}^i, \mathbf{R}^j)$ 与扰动文本嵌入对的相似度 $\mathcal{S}(\mathbf{N}^i, \mathbf{N}^j)$，CDLoss 最小化两者标准化后的乘积平方和（Eq. 8）：

$$\mathcal{L}_{\mathrm{cd}} = \sum_{i,j} \left( \frac{\mathcal{D}(\mathbf{R}^i, \mathbf{R}^j) - \mu_{\mathrm{r}}}{\sigma_{\mathrm{r}}} \cdot \frac{\mathcal{S}(\mathbf{N}^i, \mathbf{N}^j) - \mu_{\mathrm{N}}}{\sigma_{\mathrm{N}}} \right)^2$$

这一设计直接抑制步态空间与扰动空间之间的**二阶统计相关性**，而非简单地对扰动类别进行分类。消融实验（Table 7）显示，同时使用衣着、视角、携带物三个属性时，CDLoss 相比不使用任何去相关损失提升 **+11.0%** 的平均准确率，证明上下文解耦对鲁棒性的关键作用。

### 4. GCaption：大规模自然语言标注驱动解耦

CDLoss 的有效性依赖于丰富的扰动因素文本描述。GaitMax 构建了 **GCaption** 标注流水线（Figure 2 棕色区域），通过两阶段策略实现高质量序列级标注：
- **第一阶段**：使用最优 VLM（Gemini）对 8 帧独立标注，捕获多视角的外观属性；
- **第二阶段**：通过嵌入空间均值聚合保证序列级一致性——选取文本嵌入最接近均值向量的帧标注作为整段序列的代表。

Figure 4 展示了 GCaption 的标注样例，涵盖主体相关（衣着、性别等）与环境相关（背景、光照等）属性。Figure 5 的嵌入相似度热力图验证了 VLM 生成标注与人工标注的高度一致性（Gemini-2-Flash-Lite 平均相似度达 93.7%），为 CDLoss 提供了可靠的监督信号。

### 创新点之间的因果耦合

上述四个创新并非孤立存在，而是形成紧密的因果链条：**双分支架构**提供运动学建模的载体，**GauPE** 为运动学分支注入精确的几何先验，**GCaption** 为解耦提供语言监督，**CDLoss** 利用该监督在嵌入空间实现扰动因素的统计去相关。这一耦合机制解释了 GaitMax 在跨域场景下的大幅领先——运动学建模捕获身份相关的动态特征，CDLoss 抑制身份无关的外观变化，两者协同实现了“关注该关注的，忽略该忽略的”。

### 局限性

尽管创新显著，GaitMax 仍存在两个值得关注的局限：
1. **融合策略简单**：语义与运动学分支采用直接拼接融合，消融实验（Table 5）显示在 CL 条件下运动学单分支反而高出融合方案 +2.2%，表明简单拼接并非最优，缺乏自适应融合机制；
2. **GCaption 覆盖不足**：标注主要覆盖静态外观属性，未充分描述步速、过渡姿态等时序动态变化，可能限制 CDLoss 对动态干扰的抑制能力。

GaitMax 的核心设计动机源于现有步态识别中两种范式的根本性对立：**语义范式**（如 GaitSet、BigGait）通过时序池化获得顺序不变的全局结构表示，但丢弃了运动学动态过程；**运动学范式**（如基于光流的方法）虽能捕获时序动态，却易受噪声干扰且缺乏长程建模能力。GaitMax 的关键洞察在于，这两种范式并非互斥，而是互补——语义总结提供全局上下文，运动学过程提供细粒度时空轨迹，二者的统一是突破鲁棒性瓶颈的因果路径。

### 双分支架构总览

GaitMax 的整体框架由四个协同区域构成（Figure 2）：

![[assets/figures/papers/paper_list_l1084_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unlocking_Motion/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of GaitMax. [Blue Region] Semantic representation branch encodes global context of motion (§3.2.1). [Red Region] Kinematic representation branch models part-wise spatiotemporal dynamics (§3.2.2). [Brown Region] GCaption overview pipeline (§3.4). [Purple Region] Conditional decorrelation loss disentangles gait embedding from factors description (§3.3)*

1. **语义分支（蓝色区域）**：负责提取顺序不变的全局运动上下文。
2. **运动学分支（红色区域）**：负责建模身体部位级别的时空动态轨迹。
3. **GCaption 标注流水线（棕色区域）**：为扰动解耦提供自然语言描述。
4. **条件去相关损失（紫色区域）**：在嵌入空间中显式解耦身份与扰动因素。

### 输入输出流

**输入**：一段包含 $T$ 帧的 RGB 步态序列 $\{ \mathbf{V}_t \}_{t=1}^T$。

**特征提取**：使用冻结的 DINOv3 作为骨干网络 $\psi_p$，逐帧提取语义特征图。冻结大视觉模型（LVM）的策略确保了预训练知识的完整迁移，同时避免了步态数据规模不足导致的过拟合。

**语义分支处理**：对逐帧特征图施加时序均值池化 $\mathcal{P}_t$，消除时序顺序以获取顺序不变表示；随后通过水平金字塔池化 $\mathcal{P}_s$ 将空间特征划分为 $n_1$ 个水平条带，产生全局语义表示 $\mathbf{R}_s$。

**运动学分支处理**：该分支是 GaitMax 区别于所有语义基线方法的核心创新。它通过三个子模块实现从“整体外观”到“部位轨迹”的范式转换：

- **部位定位**：使用 $n_2$ 个可学习查询，通过温度增强的交叉注意力定位不同身体部位，并施加多样性损失 $\mathcal{L}_{\mathrm{div}}$ 确保部位注意力图正交，避免部位重叠。
- **GauPE 几何注入**：将注意力图通过力矩匹配参数化为高斯协方差椭圆，提取中心坐标（位置）、方差（尺度）和协方差（方向），经旋转变换后注入部位特征，形成几何增强的部位嵌入 $\bar{\mathbf{m}}$。
- **多部位时空感知**：按部位分组形成时序序列 $\mathbf{M}_p$，先对每个部位独立建模时序依赖 $\psi_t$，再由联合感知模块 $\psi_u$ 聚合所有部位的动态信息，得到运动学表示 $\mathbf{R}_k$。

**融合与最终嵌入**：将语义表示 $\mathbf{R}_s$ 与运动学表示 $\mathbf{R}_k$ 拼接，得到综合步态嵌入 $\mathbf{R} \in \mathbb{R}^{n \times d}$。

### 训练目标

总损失函数由三个分量组成：

$$\mathcal{L}_{\mathrm{tot}} = \gamma_{\mathrm{id}} \mathcal{L}_{\mathrm{id}} + \gamma_{\mathrm{cd}} \mathcal{L}_{\mathrm{cd}} + \mathcal{L}_{\mathrm{div}}$$

其中 $\mathcal{L}_{\mathrm{id}} = \mathcal{L}_{\mathrm{ce}} + \mathcal{L}_{\mathrm{tri}}$ 为标准身份判别损失，$\mathcal{L}_{\mathrm{cd}}$ 为条件去相关损失，$\mathcal{L}_{\mathrm{div}}$ 为部位多样性损失。$\gamma_{\mathrm{id}}$ 和 $\gamma_{\mathrm{cd}}$ 均设为 1，三元组损失的 margin 从 0.2 逐步增加至 0.4。

### 设计哲学

GaitMax 的双分支设计并非简单的多流融合，而是对“运动表征”这一根本问题的重新定义。语义分支通过抛弃时序来获得对衣着、视角等静态扰动的不变性；运动学分支则通过 GauPE 注入精确的几何先验，在保留长程动态的同时避免了对噪声敏感的光流估计。两条路径在嵌入空间中的互补性，使得模型能够同时应对“外观变化”和“动态变化”两类干扰——这正是跨域场景下性能大幅提升（如 CASIA-B 上 CL 条件比 BigGait 提升 +12.6%）的根本原因。

### 3.1 总体学习目标

GaitMax 将步态识别建模为一个联合优化问题。给定一段包含 $T$ 帧的 RGB 步态序列，模型的目标是学习一个嵌入空间，使得身份判别损失 $\mathcal{L}_{\mathrm{id}}$ 与条件去相关损失 $\mathcal{L}_{\mathrm{cd}}$ 同时被最小化。总体目标函数为：

$$\theta^{*} = \underset{\theta}{\arg\min} \left[ \mathcal{L}_{\mathrm{id}}(\mathbf{R}, y) + \lambda \mathcal{L}_{\mathrm{cd}}(\mathbf{R}, \mathcal{N}) \right]$$

其中 $\mathbf{R}$ 为步态嵌入，$y$ 为身份标签，$\mathcal{N}$ 为扰动因素的文本描述集合，$\lambda$ 为平衡系数。这一设计将身份判别与扰动解耦统一在一个端到端的框架中。

### 3.2 双分支框架：语义与运动学的统一

GaitMax 的核心架构由语义分支与运动学分支组成，二者并行处理同一组帧级特征，最终通过拼接得到综合步态嵌入。

#### 3.2.1 语义分支：全局上下文编码

语义分支遵循顺序不变的范式。首先使用冻结的 **DINOv3** 骨干网络逐帧提取语义特征图 $\mathbf{V}_t$，然后通过时序均值池化 $\mathcal{P}_t$ 消去时间维度，再经水平金字塔池化 $\mathcal{P}_s$ 将特征图划分为 $n_1$ 个水平条带，得到全局语义表示：

$$\mathbf{R}_s = \mathcal{P}_s \left[ \mathcal{P}_t \left( \{ \psi_p(\mathbf{V}_t) \}_{t=1}^T \right) \right]$$

该分支捕获了与顺序无关的全局结构信息，但完全丢弃了时序动态。

#### 3.2.2 运动学分支：部位级时空轨迹建模

运动学分支从三个层次构建细粒度动态表示。

**(a) 部位定位。** 引入 $n_2$ 个可学习查询向量，通过温度增强的交叉注意力在每帧特征图上定位不同的身体部位。对于第 $t$ 帧，查询 $\mathbf{q}$ 与特征 $\mathbf{v}_t$ 之间的注意力图 $\mathbf{a}$ 及部位潜在特征 $\mathbf{m}$ 为：

$$\mathbf{a} = \mathrm{Softmax} \left( (\mathbf{q} W_q) (\mathbf{v}_t W_v)^\top / \tau \sqrt{d} \right), \quad \mathbf{m} = \mathbf{a} (\mathbf{v}_t W_v')$$

其中 $\tau$ 为温度参数，控制注意力分布的锐度。为保证不同查询关注不同部位，引入多样性损失：

$$\mathbf{A} = [\mathbf{a}_1, \ldots, \mathbf{a}_{n_2}]^\top, \quad \mathcal{L}_{\mathrm{div}} = \mathbf{1}^\top (A A^\top) \mathbf{1} - \mathrm{tr}(A A^\top)$$

该损失最小化注意力图之间的重叠，促进部位的正交性。

**(b) 高斯位置嵌入（GauPE）。** 这是运动学分支的核心创新。普通的旋转位置编码（RoPE）仅编码绝对位置，而 GauPE 通过**力矩匹配**将注意力图参数化为一个高斯协方差椭圆，同时注入部位的位置、尺度和方向信息。

具体而言，对注意力图 $\mathbf{a}$ 进行力矩匹配，提取质心坐标 $(\mu_x, \mu_y)$、方差 $(\sigma_x^2, \sigma_y^2)$ 和协方差 $\sigma_{xy}$。这些参数分别编码了部位的中心位置、空间延展范围和方向。几何增强后的部位特征为：

$$\bar{\mathbf{m}} = [\sigma, \mathcal{R}(\omega_i \mu_x) \mathbf{m}^{(x)}, \mathcal{R}(\omega_i \mu_y) \mathbf{m}^{(y)}]$$

其中 $\sigma = [\sigma_x^2, \sigma_y^2, \sigma_{xy}]$ 为形状参数，$\mathcal{R}$ 为旋转变换编码，$\omega_i$ 为可学习的频率参数，$\mathbf{m}^{(x)}$ 和 $\mathbf{m}^{(y)}$ 为沿两个空间轴分解的部位特征。这一设计使注意力机制获得了对部位几何形态的显式感知能力（见 Figure 3）。

![[assets/figures/papers/paper_list_l1084_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unlocking_Motion/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of GauPE. Brightness indicates the response intensity of the attention map, while the ellipse visualizes the coverage of the Gaussian covariance ellipse. The pink dot, and the purple and green line denote the ellipse center, long axis, and short axis, respectively*

**(c) 多部位时空感知。** 将各帧中同一部位的特征按时间顺序排列，形成时序序列 $\mathbf{M}_p$。对每个部位独立进行时序建模 $\psi_t$ 后，由联合感知模块 $\psi_u$ 聚合所有部位的动态信息，得到运动学表示：

$$\mathbf{R}_k = \psi_u \left( \{ \psi_t (\mathbf{M}_p) \}_{p=1}^{n_2} \right)$$

最终，语义表示 $\mathbf{R}_s$ 与运动学表示 $\mathbf{R}_k$ 拼接，形成综合步态嵌入 $\mathbf{R} \in \mathbb{R}^{n \times d}$。

### 3.3 条件去相关损失（CDLoss）

传统方法仅依赖身份判别损失：

$$\mathcal{L}_{\mathrm{id}} = \mathcal{L}_{\mathrm{ce}} + \mathcal{L}_{\mathrm{tri}}$$

其中 $\mathcal{L}_{\mathrm{ce}}$ 为交叉熵损失，提供标签监督；$\mathcal{L}_{\mathrm{tri}}$ 为三元组损失，增强类内紧凑性与类间可分性。然而，这种损失函数无法显式抑制衣着、视角、携带物等扰动因素对嵌入空间的污染。

CDLoss 的核心思想是**强制步态嵌入空间与扰动文本嵌入空间在统计上独立**。给定一批样本，计算步态嵌入对之间的标准化距离与对应扰动文本嵌入对之间的标准化相似度的逐元素乘积，并最小化其平方和：

$$\mathcal{L}_{\mathrm{cd}} = \sum_{i,j} \left( \frac{\mathcal{D}(\mathbf{R}^i, \mathbf{R}^j) - \mu_{\mathrm{r}}}{\sigma_{\mathrm{r}}} \cdot \frac{\mathcal{S}(\mathbf{N}^i, \mathbf{N}^j) - \mu_{\mathrm{N}}}{\sigma_{\mathrm{N}}} \right)^2$$

其中 $\mathcal{D}(\cdot,\cdot)$ 为步态嵌入距离度量，$\mathcal{S}(\cdot,\cdot)$ 为扰动文本嵌入的相似度，$\mu_{\mathrm{r}}, \sigma_{\mathrm{r}}$ 和 $\mu_{\mathrm{N}}, \sigma_{\mathrm{N}}$ 分别为各自空间的均值和标准差。通过最小化该损失，模型被引导学习与扰动因素无关的步态表示。

最终训练目标为三项损失的加权和：

$$\mathcal{L}_{\mathrm{tot}} = \gamma_{\mathrm{id}} \mathcal{L}_{\mathrm{id}} + \gamma_{\mathrm{cd}} \mathcal{L}_{\mathrm{cd}} + \mathcal{L}_{\mathrm{div}}$$

实验设置中 $\gamma_{\mathrm{id}} = \gamma_{\mathrm{cd}} = 1$，三元组损失的 margin 从 0.2 逐步增至 0.4。

### 3.4 GCaption：扰动因素的自然语言标注

CDLoss 的运作依赖于对扰动因素的文本描述。为此，作者构建了 **GCaption** 数据集，利用最优 VLM（Gemini-2-Flash-Lite）逐帧标注衣着、视角、携带物等属性。为保证序列级一致性，采用嵌入空间聚合机制：对同一序列的 8 帧独立标注后，计算文本嵌入的均值向量，选择嵌入最接近该均值的帧标注作为整段序列的标注。评估表明，VLM 生成标注与人工标注的平均嵌入相似度达 93.7%（Figure 5），验证了标注质量。

## 实验与关键发现

### 核心实验设置

GaitMax 采用冻结的 DINOv3 作为视觉骨干，在所有实验中保持一致的训练协议。域内评估时，模型在 CCPG 和 CCGR MINI 上分别训练和测试；跨域评估时，所有模型均在 CCPG 上训练，直接在 CASIA-B 和 SUSTech1K 上测试，无任何微调，确保对比公平。身份损失权重 $\gamma_{\mathrm{id}}$ 和条件去相关损失权重 $\gamma_{\mathrm{cd}}$ 均设为 1，三元组损失 margin 从 0.2 逐步增加到 0.4。GCaption 标注流水线经 VLM 对齐评估，Gemini-2-Flash-Lite 与人工标注的平均嵌入相似度达 93.7%，消融实验基于该标注进行。

### 域内评估：语义与运动学融合的初步验证

在 CCPG 数据集上，GaitMax 以 89.6% 的平均 Rank-1 准确率略优于多模态方法 **DenoisingGait**（Jin et al., CVPR 2025）的 89.5%，并显著超越此前最佳的纯 RGB 方法 **BigGait**（Ye et al., CVPR 2024）的 87.2%（+2.4%）。在更具挑战性的 CCGR MINI 上，GaitMax 的优势更为明显：Rank-1 达 83.6%（+2.9% vs BigGait），mAP 达 74.2%（+8.4%），mINP 达 62.2%（+2.4%）。值得注意的是，GaitMax 仅使用 RGB 输入便超越了需要轮廓、解析图和光流等多模态输入的 **MultiGait++**（Jin et al., AAAI 2025），平均 Rank-1 提升 +2.2%，表明运动学分支从 RGB 中提取的细粒度动态信息有效替代了显式光流建模。

### 跨域泛化：运动学建模与扰动解耦的协同效应

跨域评估是检验模型鲁棒性的关键试金石。在 CASIA-B 上，GaitMax 相比 BigGait 在所有条件下均取得大幅提升：NM +8.2%，BG +15.4%，CL +12.6%，平均 +12.1%。尤其在最具挑战性的 CL（携带物变化）条件下，46.2% 的准确率揭示了运动学分支对局部时序动态的捕捉能力——携带物主要改变身体部位的局部运动轨迹，而 GauPE 提供的部位位置和形状先验恰好能精确建模这些变化。

在规模更大、场景更复杂的 SUSTech1K 上，GaitMax 同样展现出卓越的跨域鲁棒性：CL 条件下 +11.3%，NM +6.4%，BG +5.6%，UM +4.2%，平均 +5.0%。CL 条件下的一致大幅提升（两个数据集均超过 +11%）强有力地证明：CDLoss 通过文本描述显式解耦步态嵌入与外观扰动，使模型习得的身份表征对携带物变化不敏感，而非简单记忆训练域的外观模式。

### 效率分析：轻量运动学建模

尽管引入了额外的运动学分支，GaitMax 的参数量（26.6M）和每帧计算量（12.7GFLOPs）仅略高于 BigGait（21.5M / 11.0G），远低于多模态方法。运动学建模模块本身仅增加约 5.1M 参数和 1.7GFLOPs，证明基于可学习查询的部位跟踪和 GauPE 是高效的运动学建模方案。

### 消融实验：各组件的因果贡献

**运动表征范式消融**揭示了一个关键发现：语义与运动学分支的简单拼接融合并非在所有场景下最优。在 CL 条件下，纯运动学分支（87.6%）反而比融合模型（85.4%）高出 +2.2%。这表明当前融合策略在极端外观变化下可能引入语义分支的噪声——语义分支的顺序不变特性使其容易过拟合到衣着纹理等静态外观线索，当这些线索在跨域测试中失效时，反而干扰了运动学分支的鲁棒表征。这一失败模式直接指向了论文自身识别的局限性：缺乏自适应融合机制。

**位置编码消融**证实了 GauPE 的核心价值。相比标准 RoPE，GauPE 在平均 Rank-1 上提升 +3.1%（89.8% vs 86.7%）。RoPE 仅编码 token 位置，而 GauPE 通过力矩匹配将注意力图参数化为高斯协方差椭圆，注入了部位的中心坐标（位置）、方差（尺度）和协方差（方向）三重几何信息。这 +3.1% 的增益可归因于：方向信息使模型能区分部位的运动朝向，尺度信息提供了部位大小的上下文，两者共同提升了长程轨迹建模的精度。

**条件去相关损失消融**展示了扰动解耦的显著效果。当同时使用衣着、视角、携带物三个属性时，CDLoss 相比不使用任何属性平均准确率提升 +11.0%（75.5% vs 64.5%）。逐属性分析表明，单一属性即可带来显著增益，而多属性联合使用产生叠加效应，验证了 CDLoss 在嵌入空间中有效抑制了步态距离与扰动文本相似度之间的二阶统计相关性。

### 泛化性验证：向动作识别的迁移

将 GaitMax 的运动学分支集成到标准动作识别骨干网络后，在 Diving48 数据集上取得了 consistent 的性能提升。这表明 GauPE 驱动的部位时空跟踪能力具有任务无关的通用性——潜水动作识别同样需要精确建模身体部位的细粒度时序动态，GaitMax 的运动学先验恰好满足了这一需求。

### 失败模式与改进方向

尽管整体表现优异，实验揭示了两个值得关注的失败模式。其一，语义分支在 CL 条件下可能成为干扰源，融合模型不如纯运动学分支，说明需要设计场景自适应的融合策略（如基于不确定性估计的动态权重）。其二，GCaption 主要提供静态外观属性标注，未覆盖步速变化、过渡姿态等时序动态干扰因素，这可能限制了 CDLoss 对动态扰动的抑制能力——在 SUSTech1K 的 UM（不同步行速度）条件下，GaitMax 的提升（+4.2%）明显小于 CL 条件（+11.3%），暗示时序维度的扰动解耦仍有提升空间。

![[assets/figures/papers/paper_list_l1084_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unlocking_Motion/figures/005_Table_2.jpg]]
*Table 2: In-domain evaluation. We compare GaitMax with SoTA on the CCPG [26] and CCGR [81] datasets. All models are trained and evaluated within the same domain. Metrics include Rank-1 accuracy under nuisance conditions for CCPG, and three standard metrics for CCGR. Some baselines could not be reproduced on CCGR due to the absence of required input modalities and are denoted by ‘–’. [Key: Best, Second best]*

![[assets/figures/papers/paper_list_l1084_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unlocking_Motion/figures/007_Table_5.jpg]]
*Table 5: Ablation on motion representation*

![[assets/figures/papers/paper_list_l1084_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unlocking_Motion/figures/009_Table_6.jpg]]
*Table 6: Ablation on positional embedding*

![[assets/figures/papers/paper_list_l1084_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Unlocking_Motion/figures/011_Table_7.jpg]]
*Table 7: Ablation on conditional decorrelation loss*

## 定位与知识库关联

### 1. 步态识别的两种范式及其瓶颈

步态识别方法长期沿两条路线演进，分别对应不同的表征哲学与技术瓶颈。

**语义范式（Semantic Paradigm）** 将步态视为一组顺序无关的静态姿态集合，通过时序池化（如均值池化、集合池化）将帧级特征压缩为全局描述子。代表性工作包括 **GaitSet**（集合池化）、**GaitPart**（部位级先验）、**GaitGL**（全局-局部聚合）以及 **BigGait**（Ye et al., CVPR 2024，此前最优的RGB输入方法）。这类方法的优势在于对帧序扰动鲁棒，能够捕获全局结构上下文；但其根本缺陷在于丢弃了时序动态信息——步态作为周期性运动过程的核心特征被抹去，导致对衣着、携带物等外观扰动的过拟合。

**运动学范式（Kinematic Paradigm）** 试图通过光流等显式运动信号建模时序依赖，如 **DenoisingGait**（Jin et al., CVPR 2025，多模态轮廓+RGB+光流+去噪）和 **MultiGait++**（Jin et al., AAAI 2025，轮廓+解析+光流融合）。这类方法能够捕获细粒度动态，但光流对噪声敏感、缺乏长程时序建模能力，且多模态输入增加了部署成本。

GaitMax 的核心定位是**统一这两种互补范式**：保留语义分支的全局上下文能力，同时引入运动学分支对部位级时空轨迹进行长程建模，从而同时捕获“步态是什么”（全局结构）和“步态如何运动”（动态过程）。

### 2. 关键设计差异：与主要基线的对比

| 设计维度 | BigGait (Ye et al., CVPR 2024) | DenoisingGait (Jin et al., CVPR 2025) | **GaitMax (本文)** |
|---------|------|------|------|
| 输入模态 | RGB | 轮廓+RGB+光流 | RGB |
| 表征范式 | 仅语义（顺序不变池化） | 运动学（光流+去噪） | **语义+运动学双分支** |
| 位置编码 | 无 | 无 | **GauPE（高斯位置嵌入）** |
| 扰动建模 | 无显式机制 | 去噪（隐式） | **CDLoss（显式统计去相关）** |
| 文本监督 | 无 | 无 | **GCaption标注+文本嵌入空间解耦** |

**GaitMax 与 BigGait 的关系**：BigGait 是此前最优的纯RGB步态方法，但其仅依赖语义分支。GaitMax 在其基础上新增运动学分支，并通过 GauPE 注入部位位置、尺度和方向信息，使模型能够追踪身体部位的时空轨迹。在跨域评估中（Table 3），GaitMax 在 CASIA-B 的 CL 条件下比 BigGait 提升 **+12.6%** Rank-1，在 SUSTech1K 的 CL 条件下提升 **+11.3%**，证明运动学建模对衣着变化的鲁棒性至关重要。

**GaitMax 与多模态方法的对比**：DenoisingGait 和 MultiGait++ 依赖光流和解析等多模态输入，在域内 CCPG 上 DenoisingGait 达到 89.5% Mean Rank-1，GaitMax 以 89.6% 略优（+0.1%），但 GaitMax 仅使用 RGB 输入，部署成本更低。在跨域场景下（Table 3），多模态方法的优势消失，GaitMax 显著领先。

### 3. 核心技术创新点

**GauPE（高斯位置嵌入）** 是运动学分支的关键使能技术。传统位置编码（如 RoPE）仅编码绝对或相对位置，而 GauPE 通过力矩匹配将注意力图参数化为高斯协方差椭圆，同时注入部位的**位置**（质心坐标 μ_x, μ_y）、**尺度**（方差 σ_x², σ_y²）和**方向**（协方差 σ_xy）。消融实验（Table 6）显示，GauPE 相比 RoPE 带来 **+3.1%** 的平均 Rank-1 提升，验证了形状与方向信息对运动建模的决定性作用。

**CDLoss（条件去相关损失）** 从表示学习的角度解决扰动过拟合问题。不同于传统的身份判别损失（交叉熵+三元组），CDLoss 显式最小化步态嵌入空间与扰动文本嵌入空间之间的二阶统计相关性（Eq. 8），迫使模型学习与衣着、视角、携带物等因素统计独立的身份表征。消融实验（Table 7）显示，同时使用所有属性时 CDLoss 带来 **+11.0%** 的平均准确率提升。

**GCaption 标注流水线** 为 CDLoss 提供了丰富的自然语言监督信号。该流水线使用最优 VLM（Gemini）逐帧标注，并通过嵌入空间均值聚合保证序列级一致性。与人工标注的嵌入相似度达 93.7%（Fig. 5），为文本驱动的扰动解耦提供了可靠基础。

### 4. 适用边界与局限

**融合策略的次优性**：消融实验（Table 5）揭示了一个重要发现：语义与运动学分支的简单拼接融合并非在所有条件下最优。在 CL（衣着变化）条件下，运动学单分支反而比融合分支高出 +2.2%，说明当前融合策略在极端外观扰动下可能引入语义分支的噪声。这指向一个开放问题：如何设计自适应融合机制，使模型能根据场景动态调整两分支权重。

**GCaption 的覆盖范围**：GCaption 主要提供静态外观属性（衣着颜色/类型、携带物、视角等），未充分覆盖时间维度的动态变化（如步速、过渡姿态、关节角度变化）。这可能限制 CDLoss 对动态干扰因素的抑制能力。扩展 GCaption 以包含时序动态描述，是提升运动学建模和扰动解耦的潜在方向。

**计算效率的权衡**：Table 4 显示，GaitMax 的参数量（26.6M）和计算量（12.7G FLOPs）与 BigGait（21.5M / 11.0G）处于同一量级，但运动学建模分支单独占 5.1M 参数和 1.7G FLOPs。在资源受限场景下，可考虑仅使用运动学分支（尤其在 CL 条件下性能更优），但需根据具体部署条件权衡。

### 5. 开放问题与未来方向

1. **自适应融合**：如何设计门控机制或注意力融合策略，使模型能根据输入序列的特点（如衣着变化程度、视角偏移）动态调节语义与运动学分支的贡献比例？

2. **时序动态标注扩展**：GCaption 能否扩展为包含肢体运动速度、关节角度变化、步态周期相位等时序描述，以进一步提升运动学建模的细粒度和 CDLoss 对动态干扰的抑制？

3. **跨任务迁移**：GaitMax 的运动学分支持续跟踪部位轨迹的能力，能否迁移到动作识别、姿态估计等其他需要细粒度时空建模的任务？Table 8 在 Diving48 上的初步实验显示了一定泛化性，但需更系统的验证。

4. **去相关范式的推广**：CDLoss 的显式统计去相关范式是否可推广到域泛化、公平性学习等其他需要解耦的表示学习场景？该范式的理论性质和收敛保证值得进一步研究。

5. **VLM 标注的可靠性边界**：GCaption 依赖 VLM 的零样本标注能力，在极端光照、遮挡或非典型外观下的标注质量需要更系统的评估和校准机制。

## 原文 PDF

![[paperPDFs/CVPR_2026/Unlocking_Motion_from_Large_Vision_Models_with_a_Semantic_and_Kinematic_Duality_for_Gait_Recognition.pdf]]
