---
title: "UniPR: Unified Object-level Real-to-Sim Perception and Reconstruction from a Single Stereo Pair"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniPR_Unified_Object_level_Real_to_Sim_Perception_and_Reconstruction_from_a_Single_Stereo_Pair.pdf
project_link: "https://xingyoujun.github.io/unipr"
code_link: null
aliases:
- UniPR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过Pose-Aware Shape Representation (PASR) 将姿态与形状在观测空间中联合编码，结合立体几何约束消除尺度模糊，实现端到端的多目标并行重建。
primary_logic: 在观测空间中统一编码对象的姿态与几何信息（PASR），并利用立体几何约束，可使单一前向网络同时检测多目标并生成具有真实比例和尺度的3D形状，无需类别规范空间。
claims:
- UniPR在重建指标（CD, F-Score, SPE）上大幅超越Trellis和Hunyuan2.1，全场景推理速度提升100×。
- 在LVS6D数据集上，UniPR在所有子集均显著优于Coders，Hard子集AP从0.070提升至0.752。
- 消融实验表明PASR和立体设计对重建精度至关重要，去除PASR导致Hard子集ACD增加近10倍。
- LVS6D 50-object subset 上 CD↓ = 0.0083 (UniPR)
---

# UniPR: Unified Object-level Real-to-Sim Perception and Reconstruction from a Single Stereo Pair

> [!tip] 核心洞察
> 在观测空间中统一编码对象的姿态与几何信息（PASR），并利用立体几何约束，可使单一前向网络同时检测多目标并生成具有真实比例和尺度的3D形状，无需类别规范空间。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniPR：基于单立体像对的统一对象级真实到仿真感知与重建 |
| 英文题名 | UniPR: Unified Object-level Real-to-Sim Perception and Reconstruction from a Single Stereo Pair |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.19616) · [Project](https://xingyoujun.github.io/unipr) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | UniPR |
| Dataset | LVS6D 50-object subset, LVS6D |

> [!tip] 效果简介
> - LVS6D 50-object subset 上，CD↓ 0.0083 (UniPR) vs 0.0644 (Hunyuan2.1) (-0.0561)；F-Score↑ 0.883 (UniPR) vs 0.553 (Hunyuan2.1) (+0.330)；SPE↓ 0.109 (UniPR) vs 0.320 (Hunyuan2.1) (-0.211)。
> - LVS6D (Hard subset) 上，AP↑ 0.752 (UniPR) vs 0.070 (Coders) (+0.682)；APE↓ 1.248 (UniPR) vs 2.230 (Coders) (-0.982)。

## 概要

真实场景中的对象级感知与三维重建是机器人操作与具身智能的关键能力。传统方法依赖**检测—分割—形状重建—姿态估计**的多模块顺序流水线，各模块独立优化导致**误差累积**，且逐对象串行处理带来**计算低效**。同时，主流图像到3D生成模型（如Trellis、Hunyuan3D）需要预定义的2D边界框与分割掩码，且因单目输入的尺度模糊性，难以恢复物体的真实物理尺寸与形状比例。

针对上述瓶颈，UniPR提出**首个端到端统一框架**，直接从单帧立体图像对出发，在单一前向网络中并行完成多目标的检测、6D姿态估计与保比例三维形状重建。其核心创新是**Pose-Aware Shape Representation（PASR）**——在观测空间中联合编码物体的姿态与几何信息，配合立体几何约束消除尺度歧义，使网络无需类别规范空间即可生成具有真实尺度的三维形状。

在LVS6D数据集上，UniPR相较图像到3D模型Trellis与Hunyuan2.1取得压倒性优势：Chamfer Distance（CD）降低约87%（0.0083 vs 0.0644），F-Score提升约60%（0.883 vs 0.553），全场景推理速度提升约**100倍**（0.63秒 vs 43.08秒）。在类别级6D姿态估计任务上，UniPR在LVS6D Hard子集的Average Precision（AP）从Coders的0.070跃升至**0.752**，位置误差（APE）从2.230降至1.248。消融实验进一步证实，PASR与立体设计是性能的关键支柱：移除PASR后Hard子集ACD激增近10倍（1.224→12.363），替换为单目输入则AP骤降至0.270。

UniPR以端到端并行架构、PASR表示与立体几何约束，在**真实尺度保持、形状比例精度与推理效率**三个维度同步突破现有方法，为对象级真实到仿真感知提供了新的基线范式。



对象级真实到仿真（Real-to-Sim）感知与重建是机器人、具身智能和增强现实等领域的核心任务。其目标是从真实世界的传感器观测中，同时检测场景中的多个物体，并恢复它们在三维空间中的精确位置、姿态和几何形状，从而构建可供下游仿真引擎直接使用的数字孪生。这一任务面临三重根本性挑战：**多目标并行处理**、**真实尺度恢复**，以及**形状比例的准确保持**。

当前主流方法采用模块化流水线架构，将任务拆解为检测、分割、形状重建和姿态估计四个独立阶段，再通过后处理将各模块的输出拼合（Figure 2）。这种设计导致三个系统性缺陷：

1. **误差累积**：各模块独立优化，上游的检测框偏移或分割掩码误差会直接传导至下游重建，造成形状畸变和姿态偏差。尤其在遮挡场景中，分割模块的失效会完全阻断后续流程。
2. **计算低效**：形状重建和姿态估计通常逐对象串行执行，全场景推理时间随物体数量线性增长，难以满足实时仿真需求。
3. **信息隔离**：各模块仅能访问局部裁剪区域，丧失了全局场景上下文，导致重建的物体间缺乏空间一致性，比例关系失真。

在形状表示层面，现有方法或依赖**类别规范空间**（如NOCS），要求为每个类别预定义统一的朝向和尺度基准，这限制了开放类别场景的泛化能力；或采用**图像到3D生成模型**（如**Trellis**和**Hunyuan3D**系列），从单目图像直接推理3D几何。后者虽摆脱了类别模板的束缚，但单目输入固有的尺度模糊性使其无法恢复物体的真实物理尺寸，且生成的形状比例常与观测不一致——例如，一个在图像中因透视而显得细长的物体，生成模型可能将其重建为异常拉伸的形态。

从系统效率看，现有图像到3D模型仍需依赖外部的2D检测器和分割器提供精确的边界框与掩码，本质上仍是模块化流程的延伸，且每个物体的重建需独立执行完整的前向推理，全场景处理耗时可达数十秒甚至数分钟。

上述瓶颈共同指向一个核心矛盾：**模块化设计割裂了感知与重建的信息流，使得网络无法利用立体几何约束和全图上下文来联合优化检测、姿态与形状**。因此，构建一个统一的端到端框架，直接从原始立体图像对中并行输出多个物体的真实尺度3D形状与6D姿态，成为突破现有方法上限的关键方向。这正是UniPR工作的核心动机——通过将姿态与形状在观测空间中联合编码，利用立体几何消除尺度模糊，实现单次前向传播即可完成全场景的感知与重建。



## 核心方法与创新机理

UniPR 的核心创新在于将传统模块化流水线（检测→分割→重建→姿态估计）重塑为一个统一的端到端单前向网络，通过**姿态感知形状表示（Pose-Aware Shape Representation, PASR）**与**立体几何约束**的深度融合，从根本上解决了误差累积、尺度模糊与形状比例失真三大瓶颈。

### 1. 从模块化流水线到端到端单前向网络

传统方案遵循“先检测分割，再逐对象重建”的串行范式（Figure 2 左）。这一架构存在两个致命缺陷：一是各模块独立优化，上游误差向下游逐级放大；二是逐对象顺序处理导致推理时间随场景物体数量线性增长，无法实现并行化。

UniPR 将整个流程压缩为**单一前向传播网络**（Figure 2 右，Figure 3）。输入为标定立体图像对，输出为场景中所有物体的语义标签、3D 位置、物理尺度及姿态感知形状，无需任何预定义 2D 框、分割掩码或类别规范空间。信息在全网络内端到端流动，使网络能够利用全图上下文处理遮挡并保持真实形状比例。

**推理效率的质变**：在 LVS6D 50 物体子集上，UniPR 的全场景推理时间仅为 **0.63 秒**，而 Trellis 需 **43.08 秒**（约 100× 加速），Hunyuan2.1 更长达 370.78 秒（Table 1）。这一加速来源于 Transformer 解码器中可学习对象查询（object queries）的并行多目标提取机制，使得推理时间与场景中物体数量近乎解耦。

### 2. Pose-Aware Shape Representation (PASR)：在观测空间中统一姿态与形状

这是 UniPR 最核心的方法创新。传统方法将形状重建与姿态估计解耦：形状在类别规范空间（如 NOCS）中定义，姿态则作为独立的后处理步骤预测。这种分离导致两个问题：

- **规范空间歧义**：几何结构相似的类别（如不同方向的杯子与碗）可能被映射到歧义的规范空间，导致旋转预测混乱（Figure 5）。
- **形状比例失真**：从单目图像直接生成 3D 形状时，由于缺乏尺度约束，生成模型常产生比例失真的几何体（Figure 4）。

PASR 的解决方案是**直接在观测空间中联合编码物体的姿态与几何信息**。其技术实现分三层：

**（1）球形体素空间中的旋转不变编码**：将旋转后的物体表面点云通过交叉注意力压缩为单个对象嵌入 $z_{\mathrm{object}}$（Eq. 1），再经重参数化采样得到形状隐变量 $z_{\mathrm{sampled}} = \mu + \sigma \cdot \epsilon$（Eq. 2）。解码时，查询点嵌入 $z_{\mathrm{query}}$ 经交叉注意力从恢复的隐式表面表示中获取（Eq. 3），最终通过 MLP $\phi$ 预测占用概率 $\mathcal{O}(x, y, z) = \phi(z_{\mathrm{query}}(x, y, z))$（Eq. 4）。球形体素空间的选择（Table 5 消融实验证实）增强了训练稳定性，Hard 子集 AP 从 0.677 提升至 0.752。

**（2）姿态与形状的联合分布学习**：网络不直接预测确定性形状，而是预测形状嵌入的高斯分布参数 $(\hat{\mu}, \hat{\sigma}^2)$，并通过 KL 散度损失 $\mathcal{L}_{kl}$（Eq. 8）与真值分布对齐。这使得 PASR 具备了生成能力——同一物体的形状嵌入可在潜在空间中插值，实现姿态与形状的平滑过渡（Figure 6c）。

**（3）立体几何约束消除尺度模糊**：单目方案固有的尺度模糊性通过立体输入被根本解决。Tri‑Plane View（TPV）编码器将左右视图的 DINOv2 特征通过立体交叉注意力聚合到全局 UVD 坐标系（Eq. 5），为 PASR 提供了度量级的几何先验。

**消融实验的强证据**（Table 4）：去除 PASR（即回归规范空间形状）导致 Hard 子集 ACD 从 **1.224 飙升至 12.363**（近 10 倍恶化），充分证明 PASR 对大规模多类别重建是不可或缺的。将立体输入替换为单目后，Hard AP 从 0.752 骤降至 0.270，ACD 从 1.224 恶化至 2.444，验证了立体约束对几何精度恢复的关键作用。

### 3. Changed Slots 全景对比

| 设计维度 | 基线方案 | UniPR 创新 | 证据锚点 |
|---------|---------|-----------|---------|
| **Pipeline 架构** | 多模块顺序流水线（检测→分割→重建→姿态估计） | 统一端到端单前向网络，同时检测与重建 | Abstract, Figure 2 |
| **形状表示** | 类别规范空间（NOCS）或从图像直接生成 | PASR 在观测空间中联合编码姿态与形状 | Section 3.1, Figure 2(c) |
| **输入模态** | 单目图像（尺度模糊）或需预定义边界框 | 立体图像对，无需预定义框或分割掩码 | Abstract, Section 1 |
| **推理效率** | 逐对象顺序处理 | 并行全场景处理，单次前向传播 | Section 1, Table 1 |
| **姿态处理** | 独立的后处理模块 | 嵌入在 PASR 的联合表示中，消除规范空间歧义 | Figure 5, Table 4 |

### 4. 与最接近工作的本质差异

- **vs. Trellis / Hunyuan3D**：这些图像到 3D 生成模型需要 GT 2D 框和分割掩码作为输入，且生成形状常比例失真。UniPR 在无任何先验的端到端条件下，CD 达 0.0083（Trellis 0.1096，Hunyuan2.1 0.0644），SPE 达 0.109（Trellis 0.371，Hunyuan2.1 0.320），形状比例精度提升约 3 倍（Table 1）。即使为 Trellis 提供立体 GT 裁剪（Trellis‑stereo），UniPR 仍全面占优（Table 8），表明架构创新而非仅仅立体输入带来主要增益。

- **vs. Coders**：Coders 是基于立体视觉的类别级 6D 姿态估计方法，依赖预定义规范空间。在 LVS6D Hard 子集上，Coders 的 AP 仅为 0.070，而 UniPR 达到 **0.752**，APE 从 2.230 降至 1.248（Table 2）。这一巨大差距直接源于 PASR 对规范空间歧义的消除。

### 5. 创新边界与待验证方向

尽管创新显著，UniPR 仍存在明确边界：① 无内置纹理生成模块，需依赖外部模型（Hunyuan3D-Paint-v2.1）进行纹理合成；② 对拓扑高度复杂的物体（如 mug 的手柄）需额外部分感知细化步骤（Table 9），未完全实现端到端；③ 依赖标定立体相机，单目分支性能显著下降（Table 4），限制了在单目传感器上的直接应用。当前训练和主要评测基于合成数据集 LVS6D，真实场景泛化能力虽在少数示例中验证（Figure 12），但缺乏大规模真实数据评估，这一点需要读者注意。



UniPR 是一个端到端的统一前向网络，直接从单张立体图像对中并行检测多个物体并重建其具有真实尺度的 3D 几何。与传统的“检测→分割→形状重建→姿态估计”模块化流水线（Figure 2）不同，UniPR 将感知与重建统一在一个网络中，使信息可以在各组件间无缝流动，从根本上消除了模块间误差累积的问题。

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/002_Figure_2.jpg]]
*Figure 2: Comparison between our end-to-end approach and the classical pipeline. Our method enables information to flow seamlessly across all components, allowing the network to leverage the full-image context for shape reconstruction. This end-to-end design effectively handles occlusion and significantly improves the preservation of true shape proportions compared to classical, modular pipelines*

整个框架由五个核心模块串联构成（Figure 3）：

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Our Proposed UniPR. We present UniPR, a single-forward network capable of simultaneously processing multiple unknown objects. Taking stereo image pairs as input, UniPR first encodes the scene into Tri-Plane View features that comprehensively capture spatial and geometric information. Within the transformer decoder, object queries are employed to extract instance-specific features from these TPV embeddings, enabling the network to reason about multiple objects in parallel. The resulting object embeddings are then fed into specialized prediction heads to infer each object’s semantic label, 3D position, physical scale, and pose-aware shape representation*

1. **立体特征提取 (Stereo Feature Extraction)**  
   以校准后的立体图像对为输入，使用 **DINOv2** 作为骨干网络提取左右视图的 2D 特征图。这一步为后续的三维空间聚合提供稠密的视觉描述子。

2. **Tri‑Plane View 编码器 (Triplane Encoder)**  
   将立体 2D 特征聚合到全局 UVD 坐标系下的 Tri‑Plane View (TPV) 体素特征中。通过立体交叉注意力机制，在左右视图上采样特征并更新 TPV 体素：
   $$\mathbf{T}(u, v, d) = \mathcal{F}(\mathbf{T}(u, v, d), \mathbf{F}_{l}(u_{l}, v_{l}), \mathbf{F}_{r}(u_{r}, v_{r}))$$
   该模块将稀疏的 2D 观测提升为场景级的空间-几何表示，为后续多目标并行推理提供共享的 3D 上下文。

3. **Transformer 解码器与物体查询 (Transformer Decoder with Object Queries)**  
   借鉴 **DETR** 的架构，引入一组可学习的物体查询 (object queries)，通过多层交叉注意力从 TPV 特征中并行提取各个实例的专属嵌入。这种设计使得网络能够同时推理场景中所有物体，而不需要依赖于预先给定的 2D 边界框或分割掩码。

4. **预测头 (Prediction Heads)**  
   从每个物体嵌入中并行预测：语义标签、3D 位置、物理尺度，以及姿态感知的形状表示分布参数 $(\mu, \sigma^2)$。这些预测头共享物体嵌入，但各自独立优化，训练时采用联合损失：
   $$\mathcal{L}_{\text{detection}} = \mathcal{L}_{\text{position}} + \mathcal{L}_{\text{scale}} + \lambda_{\text{shape}} \times \mathcal{L}_{\text{shape}}$$

5. **姿态感知形状 VAE (Pose‑Aware Shape VAE, PASR)**  
   PASR 是框架的核心创新，它在观测空间中联合编码物体的姿态与几何信息，而非依赖类别规范空间（如 NOCS）。具体流程为：
   - 将旋转后的物体表面点云通过交叉注意力压缩为紧凑的对象嵌入 $z_{\text{object}}$；
   - 通过重参数化 $z_{\text{sampled}} = \mu + \sigma \cdot \epsilon$ 采样形状隐变量；
   - 利用交叉注意力从隐式表面表示中获取查询点嵌入，经 MLP 预测球形体素空间中的占用值 $\mathcal{O}(x, y, z)$；
   - 训练时使用 BCE 重建损失 $\mathcal{L}_{\text{recon}}$ 和 KL 散度损失 $\mathcal{L}_{\text{kl}}$（衡量预测分布与真值分布之间的差异）联合优化。

整个流程的输入仅为一张立体图像对，输出为场景中所有物体的类别、6D 姿态、真实尺度和高质量 3D 网格，无需任何预定义的边界框、分割掩码或姿态真值。这种端到端设计使得 UniPR 在全场景推理速度上相比逐对象处理的模块化基线（如 Trellis）可实现约 100 倍的加速（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/019_Figure_10.jpg]]
*Figure 10: Illustration of SAM 3D Object test result*



UniPR 是一个单次前向网络，直接以立体图像对为输入，并行推理场景中多个物体的位置、物理尺度和姿态感知的 3D 形状。其核心架构由五个模块级联构成，每个模块解决“统一感知与重建”中的一个关键子问题。

### 3.1 Pose-Aware Shape VAE（姿态感知形状变分自编码器）

传统方法将物体形状定义在类别规范空间（如 NOCS）中，导致不同类别的旋转定义不一致，且无法在观测空间中直接表达姿态。UniPR 的核心创新在于 **Pose-Aware Shape Representation (PASR)**——在观测空间中联合编码物体的姿态与几何信息，使形状隐变量天然携带旋转信息，从而消除规范空间带来的歧义。

PASR 通过一个 VAE 结构实现。给定旋转后的物体表面点云，编码器首先将表面点映射为表面嵌入，再通过交叉注意力压缩为单个物体嵌入：

$$z_{\mathrm{object}} = \mathrm{CrossAttn}(z_{\mathrm{object}}, z_{\mathrm{surface}}) \quad \text{(Eq. 1)}$$

编码器进一步预测该嵌入的高斯分布参数——均值 $\mu$ 和方差 $\sigma^2$。通过重参数化技巧从该分布中采样形状隐变量：

$$z_{\mathrm{sampled}} = \mu + \sigma \cdot \epsilon \quad \text{(Eq. 2)}$$

其中 $\epsilon \sim \mathcal{N}(0, I)$。解码器接收采样的隐变量，将其解码为球形体素空间中的占用场。具体而言，对于任意查询点 $(x, y, z)$，解码器通过交叉注意力从恢复的隐式表面表示中获取查询嵌入：

$$z_{\mathrm{query}} = \mathrm{CrossAttn}(z_{\mathrm{query}}, \hat{z}_{\mathrm{points}}) \quad \text{(Eq. 3)}$$

随后通过 MLP $\phi$ 将该嵌入映射为占用概率：

$$\mathcal{O}(x, y, z) = \phi(z_{\mathrm{query}}(x, y, z)) \quad \text{(Eq. 4)}$$

VAE 的训练损失包含两部分：重建损失 $\mathcal{L}_{\mathrm{recon}}$ 采用二进制交叉熵（BCE）监督占用预测；KL 正则化损失 $\mathcal{L}_{\mathrm{kl-reg}}$ 约束隐变量分布接近标准高斯分布：

$$\mathcal{L}_{\mathrm{recon}} = \mathrm{BCE}(\mathcal{O}(\mathbf{\hat{X}}), \mathcal{O}(\mathbf{X})) \quad \text{(Eq. 6)}$$

$$\mathcal{L}_{\mathrm{kl-reg}} = \frac{1}{C_{\mathrm{kl}}} \sum_{j=1}^{C_{kl}} \frac{1}{2} (\hat{\mu}^{2} + \hat{\sigma}^{2} - \log \hat{\sigma}^{2}) \quad \text{(Eq. 7)}$$

### 3.2 Stereo Feature Extraction 与 Triplane Encoder

UniPR 采用预训练的 DINOv2 作为立体图像特征提取骨干，从左右视图分别提取 2D 特征图。为将稀疏的 2D 特征聚合到统一的 3D 观测空间，模型引入 **Tri-Plane View (TPV)** 机制：在全局 UVD 坐标系中维护三个正交平面的体素特征 $\mathbf{T}(u, v, d)$，通过立体交叉注意力将左右视图的特征采样并融合到 TPV 中：

$$\mathbf{T}(u, v, d) = \mathcal{F}(\mathbf{T}(u, v, d), \mathbf{F}_{l}(u_{l}, v_{l}), \mathbf{F}_{r}(u_{r}, v_{r})) \quad \text{(Eq. 5)}$$

其中 $\mathbf{F}_l, \mathbf{F}_r$ 分别为左右视图的特征图，$(u_l, v_l)$ 和 $(u_r, v_r)$ 由立体几何投影关系确定。这一设计使 TPV 特征全面捕获场景的空间与几何信息，为后续多目标并行解码提供统一的 3D 场景表示。

### 3.3 Transformer Decoder 与 Prediction Heads

UniPR 采用 DETR 风格的 Transformer 解码器结构，包含 $L$ 层解码层。一组可学习的 **object queries** 通过交叉注意力从 TPV 特征中并行提取各实例的专属嵌入，使网络能够同时推理场景中的多个物体。

从解码器输出的物体嵌入被送入三个专门的预测头：
- **位置预测头**：输出物体的 3D 中心位置；
- **尺度预测头**：输出物体的物理尺度；
- **形状预测头**：预测 PASR 隐变量的分布参数（$\hat{\mu}, \hat{\sigma}^2$），即形状嵌入的均值和方差。

### 3.4 训练损失

检测管线的总损失由位置损失、尺度损失和形状损失加权组合：

$$\mathcal{L}_{detection} = \mathcal{L}_{position} + \mathcal{L}_{scale} + \lambda_{shape} \times \mathcal{L}_{shape} \quad \text{(Eq. 9)}$$

其中形状损失 $\mathcal{L}_{shape}$ 采用 KL 散度，衡量预测分布 $(\hat{\mu}, \hat{\sigma}^2)$ 与真值分布 $(\mu, \sigma^2)$ 之间的差异：

$$\mathcal{L}_{kl} = \frac{1}{C_{kl}} \sum_{j=1}^{C_{kl}} \frac{1}{2} \left( \frac{(\hat{\mu} - \mu)^{2} + \hat{\sigma}^{2}}{\sigma^{2}} - \log \hat{\sigma}^{2} + \log \sigma^{2} \right) \quad \text{(Eq. 8)}$$

该 KL 监督使网络能够有效利用预训练 VAE 的形状先验，将图像观测映射到有意义的形状隐空间。消融实验（Table 7）证实，移除 KL 监督后 Hard 子集 AP 下降约 0.077，ACD 从 1.224 恶化至 2.947，表明其对利用预训练 VAE 至关重要。

### 3.5 球形体素空间

PASR 解码器在球形体素空间而非传统立方体素空间中预测占用值。这一设计选择增强了训练稳定性：球体坐标系天然适配旋转物体的表示，避免了立方体素空间在物体旋转时产生的边界伪影。消融实验（Table 5）表明，球形体素空间使 Hard 子集 AP 从 0.677 提升至 0.752。

### 补充图表

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative pose-aware shape reconstruction results on LVS6D dataset. The results highlight the key role of PASR in simplifying rotation prediction, as it eliminates the ambiguity caused by different canonical definitions for categories with similar geometry*



## 实验与关键发现

### 核心重建性能对比

UniPR在LVS6D 50-object子集上对主流图像到3D生成模型实现了显著超越。如Table 1所示，UniPR以端到端方式直接从立体图像对推理，而基线方法Trellis和Hunyuan2.1均需提供完美的2D边界框、分割掩码及姿态作为输入。在Chamfer Distance（CD↓）指标上，UniPR达到0.0083，相比Hunyuan2.1的0.0644降低约87%，相比Trellis的0.1096降低约92%。在形状比例误差（SPE↓）上，UniPR为0.109，远低于Hunyuan2.1的0.320和Trellis的0.385。F-Score↑同样从Hunyuan2.1的0.553大幅提升至0.883。

推理效率方面，UniPR实现全场景并行处理，单场景推理仅需0.63秒，而Trellis需43.08秒（约68×加速），Hunyuan2.1需370.78秒（约589×加速）。这一效率优势源于UniPR通过Transformer解码器中的可学习对象查询同时提取多目标实例嵌入，避免了传统流水线逐对象顺序处理的瓶颈。

### 6D姿态估计与形状重建精度

在LVS6D数据集的三个难度子集上，UniPR全面超越基于立体视觉的类别级方法Coders（Table 2）。Coders依赖预定义的类别规范空间进行姿态估计与形状重建，而UniPR通过PASR在观测空间中联合编码姿态与形状，消除了规范空间带来的歧义。关键指标表现如下：

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparisons on LVS6D dataset. Here, AP refers to the Average Precision of 3DIoU with a threshold of 50%. APE denotes the Average Position Error, and ACD represents the Average Chamfer distance. The results demonstrate that UniPR outperforms Coders across all dataset subsets, with particularly strong improvements observed in the Hard subset with high intra-class variations*

- **Hard子集**：AP（3D IoU@50%）从Coders的0.070跃升至0.752，提升近10倍；APE从2.230降至1.248；ACD从2.999降至1.224。
- **Medium子集**：AP从0.504提升至0.866，ACD从0.871降至0.553。
- **Easy子集**：AP从0.704提升至0.908，ACD从0.569降至0.278。

Hard子集包含几何结构复杂、类内差异大的物体（如不规则形状的容器和工具），UniPR在该子集上的显著优势直接验证了PASR在处理大规模多类别重建时的鲁棒性。

在公开立体数据集TOD和SS3D上（Table 3），UniPR同样展现出竞争力的6D姿态估计能力，进一步验证了PASR解码精确物体姿态的有效性。

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/009_Table_3.jpg]]
*Table 3: Comparison on public stereo datasets. The results highlight the effectiveness of the proposed PASR and its capability to decode accurate 6D object poses*

### 消融实验与机制验证

**PASR的核心作用**（Table 4）：去除Pose-Aware Shape Representation后，Hard子集ACD从1.224急剧恶化至12.363（增加近10倍），AP从0.752降至0.457。这表明PASR对于大规模词汇量目标检测和姿态感知形状重建至关重要——在观测空间中联合编码姿态与形状，使网络无需学习复杂的类别规范空间映射，从而显著降低学习难度。

**立体几何约束的必要性**（Table 4）：将立体输入替换为单目后，Hard子集AP从0.752骤降至0.270，ACD从1.224升至2.444。单目配置无法恢复真实尺度，且失去了立体视差提供的几何约束，导致形状比例和位置估计均显著退化。这一结果说明，UniPR的性能优势并非仅来自架构设计，立体几何约束是不可或缺的组件。

**模态公平性验证**（Table 8）：为排除“立体输入本身带来优势”的质疑，作者进行了公平性比较：即使为Trellis提供立体GT裁剪（Trellis-stereo），UniPR在CD、F-Score、SPE上仍全面占优；同时，UniPR的单目版本（UniPR-mono）同样远超Trellis。这证实架构创新（端到端设计+PASR）而非仅输入模态是性能提升的主要驱动力。

**球形体素空间**（Table 5）：将形状解码器的体素空间从立方体改为球形体素后，Hard子集AP从0.677提升至0.752。球形体素空间与PASR中物体绕原点旋转的表示方式自然对齐，增强了训练稳定性。

**KL监督机制**（Table 7）：移除KL散度监督后，AP下降约0.077，ACD从1.224恶化至2.947。KL监督使预测的形状隐变量分布对齐预训练VAE的分布，是有效利用预训练先验的关键。

**部分感知细化**（Table 9）：在TOD数据集的mug类别上，增加部分感知细化后，总体5°2cm精度从63.2%提升至69.1%，超越Coders的64.8%。这表明对于拓扑高度复杂的物体（如带把手的杯子），额外的结构先验仍有必要。

### 定性分析与可视化

Figure 4展示了与图像到3D模型的定性形状重建对比。UniPR生成的形状准确保持了物体的真实比例，而Trellis和Hunyuan2.1常出现比例失真——这是因为后者从单目图像直接生成3D，缺乏立体几何约束来恢复物理尺度。

Figure 5突出展示了PASR在姿态感知重建中的关键作用。对于几何结构相似但规范空间定义不同的类别（如不同朝向的瓶子和罐子），PASR通过观测空间中的联合编码消除了旋转歧义，使网络无需推断类别特定的规范姿态。

Figure 6从三个维度验证了PASR的生成能力：(a) 同类别形状生成展现嵌入空间的语义连续性；(b) 不同物体朝向下的重建保持几何一致性；(c) 姿态-形状插值表明隐空间具有良好的平滑性和解耦性。

### 失败模式与局限性

1. **拓扑复杂物体**：对于mug等具有复杂拓扑结构的物体，纯端到端处理精度不足，需额外的部分感知细化步骤（Table 9），未完全实现统一的端到端处理。

2. **单目退化**：单目分支性能显著下降（Hard AP从0.752降至0.270），框架依赖校准的立体相机，难以直接应用于单目传感器或非结构化拍摄场景。

3. **纹理缺失**：UniPR无内置纹理生成模块，需依赖外部模型（Hunyuan3D-Paint-v2.1）进行纹理合成，完整的real-to-sim管线仍非完全自包含。

4. **真实场景泛化**：训练和主要评测基于合成数据集LVS6D，虽在少量真实场景示例中验证（Figure 12），但缺乏大规模真实数据评估，真实场景下的鲁棒性尚需进一步验证。

5. **场景范围限制**：当前仅针对桌面级物体操作场景，未扩展到大规模环境或动态场景。

### 补充图表

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on reconstruction. Both Trellis and HunYuan2.1 require perfect 2D bounding boxes, segmentation masks, and poses as inputs, whereas our method operates in an end-to-end manner directly from stereo images. Here, CD denotes the Chamfer Distance, SPE refers to the Shape Proportion Error, and inference time is measured in seconds per object and per scene*

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/008_Table_4.jpg]]
*Table 4: Ablation study results. The results underscore the critical role of PASR in enabling large-vocabulary object detection and pose-aware shape reconstruction, as well as the importance of the stereo design for achieving accurate geometric recovery*

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative shape reconstruction results compared with image-to-3D models. The results demonstrate the accurate preservation of shape proportions achieved by our proposed UniPR across various objects in the LVS6D dataset*

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/015_Table_8.jpg]]
*Table 8: Fairness comparison on input modalities and reconstruction metrics. Our method demonstrates superior geometric consistency and shape proportion accuracy compared to Trellis, regardless of the input modality*

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/010_Table_5.jpg]]
*Table 5: Ablation on spherical voxel space. We conduct this experiment with shape decoder utilizing spherical and cubic voxel space. This experiment is conducted only on the hard subset of LVS6D, as most re-normalized objects are included in this subset*

![[assets/figures/papers/paper_list_l2618_https_arxiv_org_abs_2603_19616/figures/014_Table_7.jpg]]
*Table 7: The ablation of KL-based supervision. The results demonstrate the importance of KL-based supervision for utilizing the pretrained VAE model*



## 定位与知识库关联

### 1. 核心问题定位：从模块化流水线到统一端到端

现有对象级真实到仿真（Real-to-Sim）感知与重建系统普遍采用**模块化顺序流水线**：先检测2D边界框与分割掩码，再基于裁剪区域进行形状重建与6D姿态估计。这一范式存在三个结构性瓶颈：

1. **误差累积与信息断裂**：各模块独立优化，上游检测误差不可逆地传播至下游重建与姿态估计，且裁剪操作割裂了对象与全局场景的上下文关联（Figure 2）。
2. **尺度模糊与比例失真**：单目图像到3D生成模型（如 **Trellis** 与 **Hunyuan3D** 系列）缺乏立体几何约束，无法恢复真实物理尺度，且重建形状常出现比例漂移。
3. **计算低效**：逐对象串行处理导致全场景推理时间随物体数量线性增长，难以满足实时仿真需求。

UniPR 通过**Pose-Aware Shape Representation (PASR)** 在观测空间中联合编码姿态与形状信息，将检测、重建与姿态估计统一为单次前向传播，从根本上切断了上述误差链。

### 2. 与基线工作的结构性对比

#### 2.1 与图像到3D生成模型的对比

**Trellis** 和 **Hunyuan2.1** 代表当前图像到3D生成的主流范式：给定单目图像及预定义的2D框与分割掩码，生成类别规范空间或任意姿态下的3D网格。其核心局限在于：

- **输入依赖**：需要完美的2D先验（框、掩码、甚至姿态真值），实际部署中这些先验本身即来自不可靠的检测模块。
- **尺度无约束**：单目输入天然缺乏深度信息，生成形状的绝对尺度与比例仅由训练数据统计决定，无法保证物理一致性。
- **串行处理**：每个对象独立推理，全场景耗时随对象数线性累积。

**UniPR 的结构性优势**（Table 1, Table 8）：
- 直接从立体图像对端到端输出，无需任何2D先验。
- 立体几何约束提供真实尺度恢复能力，Shape Proportion Error (SPE) 从 Hunyuan2.1 的 0.320 降至 0.109（↓65.9%）。
- 全场景并行推理仅需 0.63s，相较 Trellis 的 43.08s 实现约 **68× 加速**，相较 Hunyuan2.1 的 370.78s 实现约 **588× 加速**。

**公平性验证**（Table 8）：即使将 Trellis 扩展为 Trellis‑stereo 并提供立体 GT 裁剪输入，UniPR 在 CD、F-Score、SPE 上仍全面占优；UniPR‑mono 版本同样远超 Trellis，表明**架构创新（PASR + 统一检测重建）而非仅仅立体输入**是性能提升的主要来源。

#### 2.2 与类别级6D姿态估计方法的对比

**Coders** 是基于立体视觉的类别级6D姿态估计与形状重建方法，其核心设计依赖**预定义的类别规范空间（如NOCS）**。这一设计在以下场景中暴露根本性缺陷：

- **类内几何变异**：当同一类别包含形状差异显著的对象时（如 LVS6D Hard 子集中的复杂几何体），规范空间假设失效，Coders 的 AP 仅 0.070。
- **类别间歧义**：几何相似但语义不同的类别（如杯子与碗）在规范空间中难以区分，导致旋转预测歧义。

**UniPR 通过 PASR 实现范式跃迁**（Table 2）：
- PASR 在**观测空间**而非规范空间中编码形状，消除了对预定义规范坐标系的依赖。
- Hard 子集 AP 从 0.070 跃升至 **0.752**（↑0.682），APE 从 2.230 降至 **1.248**（↓44.0%）。
- 在 TOD 和 SS3D 公开数据集上同样超越 Coders（Table 3），验证了跨数据集的泛化能力。

### 3. 方法谱系中的知识贡献

UniPR 在以下知识节点上做出了可验证的贡献：

| 知识维度 | 基线状态 | UniPR 贡献 | 证据强度 |
|---------|---------|-----------|---------|
| **形状表示空间** | 类别规范空间（NOCS）或图像条件生成 | PASR：观测空间中联合编码姿态与形状 | 消融实验：去除 PASR 后 Hard ACD 从 1.224 升至 12.363（Table 4） |
| **输入模态与约束** | 单目（尺度模糊）或需预定义框 | 立体图像对，端到端无先验 | 单目替换导致 Hard AP 从 0.752 降至 0.270（Table 4） |
| **架构范式** | 多模块顺序流水线 | 统一单前向网络 | 全场景推理时间从 43.08s 降至 0.63s（Table 1） |
| **多目标处理** | 逐对象串行 | Transformer Decoder + Object Queries 并行 | 推理时间不随对象数线性增长（Table 1） |
| **形状解码空间** | 立方体素 | 球形体素空间 | Hard AP 从 0.677 提升至 0.752（Table 5） |
| **隐变量正则化** | 标准 VAE 训练 | KL 散度监督连接预训练 VAE 与检测管线 | 移除 KL 监督后 AP 下降 0.077，ACD 从 1.224 恶化至 2.947（Table 7） |

### 4. 适用边界与局限

尽管 UniPR 在统一端到端重建上取得显著突破，其当前设计存在明确的适用边界：

1. **纹理生成的缺失**：UniPR 聚焦于几何重建，无内置纹理生成模块，需依赖外部模型（Hunyuan3D-Paint-v2.1）进行纹理合成。这使其在需要完整外观的仿真场景中仍依赖后处理管线。

2. **拓扑复杂物体的处理**：对于具有复杂拓扑结构的物体（如带手柄的 mug），标准 UniPR 出现重建失效，需引入额外的**部分感知细化（part-aware refinement）**步骤（Table 9）。在 TOD 数据集上，加入该细化后 mug 类 5°2cm 精度从 63.2% 提升至 69.1%，但这一步骤打破了端到端的纯粹性。

3. **立体相机的硬件依赖**：UniPR 依赖校准的立体相机，单目分支性能显著下降（Table 4），难以直接迁移至单目传感器或未校准设备。这限制了其在移动端或消费级设备上的部署。

4. **合成数据训练的泛化鸿沟**：训练和主要评测基于合成数据集 LVS6D（50 类、约 12K 立体对），真实场景验证仅在小规模示例上进行（Figure 8, Figure 12），缺乏大规模真实数据基准的严格检验。

5. **场景规模限制**：当前方法针对桌面级多物体操作场景设计，未扩展到大规模环境（如室内房间级）或动态场景（如移动物体、变化光照）。

### 5. 开放问题与后续方向

基于上述局限，以下开放问题值得后续工作关注：

1. **单目配置的深度先验整合**：能否通过整合大规模单目深度估计基础模型（如 Depth Anything、Marigold）的先验知识，弥补单目配置下的尺度模糊，使 UniPR 框架适配更广泛的传感器？

2. **隐式神经表示与纹理的联合学习**：PASR 当前以体素占用表示形状，能否与隐式神经辐射场（NeRF）或3D高斯泼溅（3DGS）结合，实现几何、纹理与材质的端到端联合重建？

3. **自监督与半监督的域适应**：如何利用自监督学习（如立体光度一致性）或半监督策略，减少对合成数据的依赖，提升在真实场景下的鲁棒性？当前仅有的少量真实场景定性结果（Figure 8, Figure 12）尚不足以支撑这一方向的可行性判断，需进一步验证。

4. **时序扩展与动态场景**：UniPR 处理单帧立体对，能否扩展至多帧序列或视频立体输入，以实现时序一致的3D感知与跟踪？这需要解决跨帧对象关联与运动建模问题。

5. **大规模场景的层次化扩展**：当前基于全局 Tri‑Plane View 的场景编码能否通过层次化或稀疏化策略扩展至房间级甚至建筑级环境，同时保持实时推理能力？



## 原文 PDF

![[paperPDFs/CVPR_2026/UniPR_Unified_Object_level_Real_to_Sim_Perception_and_Reconstruction_from_a_Single_Stereo_Pair.pdf]]
