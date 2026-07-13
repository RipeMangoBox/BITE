---
title: "SLARM: Streaming and Language-Aligned Reconstruction Model for Dynamic Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SLARM_Streaming_and_Language_Aligned_Reconstruction_Model_for_Dynamic_Scenes.pdf
project_link: "https://kevinchiu19.github.io/SLARM/"
code_link: null
aliases:
- SLARM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过高阶运动建模（三阶泰勒展开）实现无监督场景流学习，并利用语言对齐语义蒸馏（LSeg）赋予高斯原语语义查询能力，同时采用窗口因果注意力实现常数延迟流式推理。
primary_logic: 动态场景重建的关键瓶颈在于运动表示的表达能力；将运动建模提升至加速度/加加速度层次并仅依靠渲染损失进行自监督学习，可同时提升几何精度和语义一致性，而语义特征的引入又能作为时序正则化进一步改善运动估计。
claims:
- SLARM 在 WOD 数据集上 PSNR 达到 27.49 dB，比 STORM 提高 1.63 dB
- 高阶运动模型在三阶（jerk）时性能达到最优
- 语义损失 L_sem 显著降低 Flow EPE，额外引入 L_cls 进一步提高性能
- SLARM-W 实现线性推理时间和稳定内存消耗，支持长序列流式推理
---

# SLARM: Streaming and Language-Aligned Reconstruction Model for Dynamic Scenes

> [!tip] 核心洞察
> 动态场景重建的关键瓶颈在于运动表示的表达能力；将运动建模提升至加速度/加加速度层次并仅依靠渲染损失进行自监督学习，可同时提升几何精度和语义一致性，而语义特征的引入又能作为时序正则化进一步改善运动估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | SLARM：面向动态场景的流式与语言对齐重建模型 |
| 英文题名 | SLARM: Streaming and Language-Aligned Reconstruction Model for Dynamic Scenes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22893) · [Project](https://kevinchiu19.github.io/SLARM/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | SLARM |
| Dataset | Waymo Open Dataset (WOD) - Full Image, Waymo Open Dataset, NuScenes, Argoverse2 |

> [!tip] 效果简介
> - Waymo Open Dataset (WOD) - Full Image 上，PSNR ↑ 27.49 (SLARM-F) vs 25.86 (STORM*) (+1.63 dB)；SSIM ↑ 0.828 (SLARM-F) vs 0.804 (STORM*) (+0.024)；Depth RMSE ↓ 4.57 (SLARM-F) vs 5.47 (STORM*) (-0.90)。
> - Waymo Open Dataset (WOD) 上，mIoU ↑ (semantic segmentation) 0.6663 (SLARM) vs 0.4876 (LSeg) (+0.1787)；EPE3D ↓ (scene flow) 0.240 (SLARM-F) vs 0.304 (STORM) (-0.064)。
> - NuScenes 上，PSNR ↑ 26.71 (SLARM-F) vs 26.25 (STORM) (+0.46 dB)。

## 概要

SLARM 是一个面向动态场景的**流式、语言对齐的前馈重建模型**，其核心目标是解决现有方法在复杂非均匀运动建模、语义理解与实时推理部署三个维度上的根本性瓶颈。以 **STORM** (Yang et al., arXiv 2024) 为代表的前馈式动态重建方法依赖恒定速度假设，难以精确捕捉真实场景中行人的步态、车辆的变速等非均匀运动；同时，这些方法缺乏语义感知能力，且采用离线批量推理模式，无法满足自动驾驶等对延迟和内存敏感的实时应用需求。

SLARM 的关键洞察在于：**动态场景重建的性能瓶颈本质上受限于运动表示的表达能力**。通过将运动建模从一阶（恒定速度）提升至三阶泰勒展开（包含速度、加速度与加加速度），并仅依靠可微分渲染损失进行自监督学习，模型能够同时提升几何精度与语义一致性；而语义特征的引入又作为时序正则化，进一步改善了运动估计的质量。

在方法定位上，SLARM 继承了 **LGM** (Tang et al., ECCV 2024) 和 **GS-LRM** (Zhang et al., ECCV 2024) 等前馈 3D 高斯重建框架，并在三个关键维度上进行了根本性改造：**高阶运动模型**替代恒定速度假设，**LSeg 语义蒸馏**赋予高斯原语语言对齐的语义查询能力，**窗口因果注意力**实现常数延迟的流式推理。这使得 SLARM 成为首个同时输出场景流、度量深度与语言对齐语义的前馈 4D 重建模型。

实验结果表明，SLARM 在 Waymo Open Dataset (WOD) 上达到 **27.49 dB PSNR**，比 STORM 提高 **1.63 dB**；深度误差 (Depth RMSE) 降至 **4.57**，降低 0.90；场景流误差 (EPE3D) 降至 **0.240**，相对降低 21%；语义分割 mIoU 达到 **0.6663**，比 LSeg 提高约 18 个百分点。在 NuScenes 和 Argoverse2 数据集上的跨域泛化实验进一步验证了方法的鲁棒性。消融研究证实，三阶运动建模达到性能最优，语义损失显著降低流估计误差，而流式推理模式在保持线性时间复杂度与稳定内存占用的同时，实现了与离线模式接近的重建质量。



动态场景的实时三维重建与理解是自动驾驶与具身智能的核心技术。近年，以 3D Gaussian Splatting（3DGS）为代表的前馈式通用重建模型在静态场景上取得了快速且逼真的新视角合成效果，代表性工作如 **LGM**（Tang et al., ECCV 2024）与 **GS-LRM**（Zhang et al., ECCV 2024）。然而，当场景中包含运动物体时，这些方法面临根本性挑战：现实世界中的运动往往是非均匀、非线性的——例如行人的步态包含复杂的加速与减速过程，而现有方法对此建模能力严重不足。

**STORM**（Yang et al., arXiv 2024）是将 3DGS 扩展至动态场景的代表性前馈方法，但其运动模型建立在**恒定速度假设**之上，仅能描述一阶线性运动。这一简化导致两个关键瓶颈：其一，无法精确建模真实场景中的加速度与加加速度，造成运动估计与几何重建的误差；其二，缺乏对场景语义的理解，重建结果仅包含外观与几何信息，无法直接支撑下游的语义查询与场景解析任务。此外，STORM 采用离线批量处理模式，需要缓存完整序列后才能推理，难以满足自动驾驶等场景对**流式在线推理**的低延迟与恒定内存需求。

上述瓶颈可归结为一个核心问题：**动态场景前馈重建的表达能力受限于运动模型的阶次与语义信息的缺失**。一方面，运动模型从一阶提升至高阶，有望在无需显式光流监督的条件下，仅依靠可微渲染损失自监督地学习更精细的场景流；另一方面，若能将语言对齐的语义特征蒸馏至高斯基元，不仅赋予重建结果语义理解能力，语义一致性本身也可作为时序正则化信号，反向改善运动估计的精度。

基于此，SLARM 提出三个关键改进方向：引入**高阶泰勒展开运动建模**以捕获非均匀运动；通过蒸馏 **LSeg 语言对齐特征**实现语义重建；设计**窗口因果注意力机制**以实现常数延迟的流式推理。这三个方向分别对应运动表达能力、语义理解能力与在线部署能力的系统性提升。



## 核心方法与创新机理

SLARM 在现有前馈式动态重建方法的基础上，从运动建模、语义表征和推理模式三个维度进行了系统性改进，以解决真实场景中复杂非均匀运动的精确建模问题，并赋予模型语义理解与实时流式推理能力。

**运动模型：从恒定速度到高阶泰勒展开**

现有方法（如 **STORM**，Yang et al., arXiv 2024）采用恒定速度假设，即仅使用一阶运动模型描述场景动态。这一简化在处理行人步态等非均匀运动时产生显著误差（见 Figure 5(a)）。SLARM 将运动建模提升至三阶泰勒展开，同时预测速度、加速度和加加速度（jerk），使位移函数具备对复杂轨迹的表达能力：

$$m_l = s_l \cdot \frac{\mathbf{v}_l}{\|\mathbf{v}_l\|_2}$$

$$\Gamma(\Delta t) = \sum_{l=0}^{L-1} \frac{m_l \cdot (\Delta t)^{l+1}}{(l+1)!}$$

其中 $L=3$ 对应三阶运动。该运动模型完全通过可微渲染损失进行自监督学习，无需真实场景流标注。消融实验（Figure 5(c)）表明，从一阶提升至三阶后重建质量和流估计误差持续下降，三阶达到最优，更高阶不再带来明显收益——这验证了加加速度层次的运动信息对动态场景建模具有关键作用。

**语义特征：语言对齐的 4D 语义蒸馏**

此前的前馈式重建方法（如 **LGM**，Tang et al., ECCV 2024；**GS-LRM**，Zhang et al., ECCV 2024）仅输出几何与外观信息，缺乏语义理解能力。SLARM 引入语义头，通过蒸馏 **LSeg** 的语言对齐特征，为每个高斯原语赋予 512 维语义嵌入。训练时采用双重语义监督：

- 自监督蒸馏损失 $\mathcal{L}_{\mathrm{sem}} = \|\tilde{\mathbf{F}}_{t+\Delta t} - \hat{\mathbf{F}}_{t+\Delta t}'\|_2^2$，将渲染特征与 LSeg 提取的 2D 特征对齐；
- 有监督分类损失 $\mathcal{L}_{\mathrm{cls}}$，将渲染特征与 CLIP 文本嵌入做内积后计算交叉熵，温度 $\tau=0.07$。

语义特征的引入不仅赋予模型开放词汇查询能力（mIoU 从 LSeg 的 0.4876 提升至 0.6663，Table 2），更作为时序正则化器反向改善运动估计：语义一致性约束迫使具有相同语义身份的目标沿平滑物理轨迹运动，从而降低 Flow EPE（Figure 5(b) 与 Sec. 4.5）。

**推理模式：窗口因果注意力实现流式推理**

现有方法采用批量帧处理的离线模式，不适用于自动驾驶等实时应用。SLARM 设计窗口因果注意力机制，使模型仅依赖过去和当前帧进行推理，实现常数延迟的流式 4D 重建。通过将高斯原语划分为静态子集与动态子集（基于运动幅度阈值 $\tau_m$），模型在流式推理时仅需反向传播动态高斯的状态，而静态部分可直接复用：

$$\mathcal{G}^{\mathrm{static}} = \{g \in \mathcal{G} \mid \|\Gamma_g(\Delta t)\| \leq \tau_m\}, \quad \mathcal{G}^{\mathrm{dynamic}} = \mathcal{G} \setminus \mathcal{G}^{\mathrm{static}}$$

这一设计使 SLARM-W 在保持与离线模式 SLARM-F 接近的重建质量（PSNR 27.30 vs. 27.49，Table 1）的同时，实现线性推理时间和稳定内存消耗，支持长序列流式处理（Figure 5(d)）。

三个改进维度形成协同效应：高阶运动模型提供精确的几何基础，语义蒸馏赋予场景理解能力并反向正则化运动估计，流式推理则将上述能力部署到实时应用场景。



SLARM 的总体设计遵循“编码—融合—解码—语义/运动增强—流式传播”的前馈式流水线，其核心结构如 Figure 2 所示。模型以多帧 RGB 图像序列作为输入，输出一个显式的 4D 高斯泼溅（4D Gaussian Splatting, 4DGS）表示，该表示同时携带几何、光度、运动与语言对齐的语义信息。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of our SLARM model for streaming 4D Gaussian reconstruction. The SLARM model begins by extracting image tokens using a shared-weight Vision Transformer (ViT), and then appending special tokens to these image tokens. These tokens then undergo Frame Attention and Global Attention mechanisms, before being fed into the corresponding decoders to output the parameters*

**输入与图像编码。** 给定时间窗口内的连续帧，SLARM 首先使用一个权重共享的 Vision Transformer（ViT）将每帧图像独立编码为一组 patch 特征 token，并在 token 序列中附加特殊标记以携带全局上下文信息。

**交替注意力时空融合。** 图像 token 随后进入一个交替注意力 Transformer（Alternating-Attention Transformer），该模块在帧注意力（Frame Attention）与全局注意力（Global Attention）之间交替执行：帧注意力沿时间轴建模同一空间位置的运动对应关系，全局注意力则在所有 token 间建立长程依赖，从而高效融合时空信息。

**多路并行解码。** 融合后的 token 被送入三个并行的解码头：
- **Gaussian Decoder**：为每个像素回归一组 3D 高斯参数，包括 3D 位置 $\pmb{\mu}$（由射线原点 $\pmb{o}$、预测深度 $\pmb{d}$ 和射线方向 $\pmb{r}$ 通过 $\pmb{\mu} = \pmb{o} + \pmb{d} \cdot \pmb{r}$ 计算得到）、旋转、尺度、不透明度及颜色。
- **Motion Head**：预测高阶运动系数（速度、加速度、加加速度），用于通过泰勒展开计算任意时间偏移下的位移，实现无监督场景流学习。
- **Semantic Head**：生成 64 维语义特征图，经 MLP 升维至 512 维，与 LSeg 教师特征对齐，赋予高斯原语语言感知的语义属性。

**流式推理与状态传播。** 在在线推理模式下，SLARM 采用窗口因果注意力，仅依赖过去与当前帧进行重建。模型根据运动幅度将高斯原语划分为静态与动态子集：静态高斯直接保留，动态高斯则通过后向扭曲（backward warping）从后续帧传播并精炼，从而在恒定延迟和稳定内存消耗下实现长序列的增量式流式推理。

**训练信号。** 整个框架通过一个复合损失函数端到端训练，损失项包括 RGB 渲染损失（MSE + LPIPS）、深度损失、天空正则、运动正则以及语义蒸馏/分类损失，其中语义损失同时充当时序正则化器，约束语义一致物体的运动轨迹保持物理合理性。

### 补充图表

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/001_Figure_1.jpg]]
*Figure 1: SLARM is a large feedforward Transformer using a self-supervised approach for fast and accurate inference of 3D scene flow, metric depth and language-aligned semantics in dynamic scenes. For real-time inference deployment in autonomous driving and embodied AI applications, our model also supports incremental streaming inference*



### 1. 整体流水线：从图像到4D高斯原语

SLARM 的推理流水线由三个核心模块串联构成（Figure 2）：

1. **共享权重 ViT 骨干网络**：将输入的多帧图像分别切分为 patch 并提取视觉 token。所有帧共享同一个 ViT 编码器，保证特征空间的一致性。
2. **交替注意力 Transformer**：对提取的 token 依次执行帧注意力（Frame Attention）与全局注意力（Global Attention），实现时空信息的交替融合。
3. **多任务解码器**：融合后的 token 分别输入三个解码头——高斯解码器（Gaussian Decoder）、运动头（Motion Head）和语义头（Semantic Head），输出 4D 高斯原语的全部参数。

高斯解码器为每个像素回归一条射线上的 3D 高斯原语参数：3D 位置 $\pmb{\mu}$、旋转四元数、各向异性尺度、不透明度以及颜色。3D 位置由射线上预测的深度值计算得到：

$$\pmb{\mu} = \pmb{o} + \pmb{d} \cdot \pmb{r}$$

其中 $\pmb{o}$ 为相机光心，$\pmb{r}$ 为像素对应的射线方向，$\pmb{d}$ 为网络预测的深度标量。

---

### 2. 高阶运动建模：从恒定速度到加加速度

现有前馈式动态重建方法（如 **STORM**，Yang et al., arXiv 2024）普遍采用恒定速度假设，仅建模一阶运动，无法精确描述真实场景中行人的步态、车辆的加减速等非均匀运动（Figure 5(a)）。

SLARM 将运动建模提升为**多阶泰勒展开**，显式预测速度、加速度和加加速度（对应 $L=3$）。运动头为每个高斯原语输出各阶运动系数：

$$m_l = s_l \cdot \frac{\mathbf{v}_l}{\|\mathbf{v}_l\|_2}$$

其中 $s_l$ 为第 $l$ 阶的标量速率，$\mathbf{v}_l$ 为方向向量，$m_l$ 为二者组合后的运动系数（Eq. (1)）。

给定时间偏移量 $\Delta t$，高斯原语的总位移由各阶运动系数加权求和得到：

$$\Gamma(\Delta t) = \sum_{l=0}^{L-1} \frac{m_l \cdot (\Delta t)^{l+1}}{(l+1)!}$$

其中 $l=0,1,2$ 分别对应速度、加速度和加加速度的贡献（Eq. (2)）。该公式的物理含义是：位移是速度的积分、加速度的二重积分、加加速度的三重积分，分母的阶乘因子来源于泰勒展开的系数。

**关键设计**：整个运动学习过程完全自监督，仅依赖可微分渲染损失进行优化，无需任何真实场景流标注。

---

### 3. 语言对齐的语义蒸馏

SLARM 的语义头输出 64 维特征图，经 MLP 升维至 512 维后，与预训练的 **LSeg** 特征进行对齐。语义监督包含两个互补的损失项（Figure 3）：

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of semantic supervision in SLARM. Left: Self-supervised feature learning via distillation from LSeg, where rendered semantic Gaussians are decoded. Right: Supervised training on labeled data by aligning predictions with class text embeddings*

**语义蒸馏损失** $\mathcal{L}_{\mathrm{sem}}$（Eq. (5)）：将渲染得到的语义特征图 $\tilde{\mathbf{F}}_{t+\Delta t}$ 与 LSeg 从真实图像中提取的 2D 特征 $\hat{\mathbf{F}}_{t+\Delta t}'$ 之间计算 MSE 损失，实现自监督特征学习。

**分类损失** $\mathcal{L}_{\mathrm{cls}}$（Eq. (6)）：将渲染特征 $f_{ij}$ 与 CLIP 文本编码器提取的各类别文本嵌入 $t_k$ 做内积，经温度参数 $\tau=0.07$ 的 softmax 归一化后计算交叉熵损失：

$$\mathcal{L}_{\mathrm{cls}} = \frac{1}{hw} \sum_{i,j=1}^{h,w} -\log \left( \frac{\exp(f_{ij} \cdot t_{k_{ij}} / \tau)}{\sum_{k=1}^K \exp(f_{ij} \cdot t_k / \tau)} \right)$$

消融实验表明（Figure 5(b)）：仅使用 $\mathcal{L}_{\mathrm{sem}}$ 即可显著降低场景流 EPE；进一步引入 $\mathcal{L}_{\mathrm{cls}}$ 后，PSNR 和语义 mIoU 也同步提升。这验证了语义一致性可作为时序正则化器，约束具有相同语义身份的目标（如车辆、行人）遵循平滑且物理合理的运动轨迹。

---

### 4. 流式推理的状态传播机制

为实现在线部署，SLARM 采用**窗口因果注意力**替代全局注意力，严格遵循因果约束：推理时刻 $t$ 只能访问当前帧及历史帧（Eq. (7)）：

$$(\mathcal{G}_t, \mathbf{\Gamma}_t) = \phi(\mathbf{I}_t \mid \mathbf{I}_{t-\Delta t}, \mathbf{I}_{t-2\Delta t}, \ldots)$$

流式更新的核心是**静态/动态高斯划分**（Eq. (8)-(9)）：根据运动幅度阈值 $\tau_m$ 将高斯原语分为静态子集 $\mathcal{G}^{\mathrm{static}}$ 和动态子集 $\mathcal{G}^{\mathrm{dynamic}}$。静态高斯直接保留，动态高斯则通过预测的运动场从历史帧向后向 warping 至当前时刻（Figure 4 右），实现增量式状态传播。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of motion handling for dynamic Gaussians under two modes. In offline inference, the target frame is synthesized by 0 2 interpolating all input frames. In online inference, the target frame is reconstructed via backward warping from the subsequent frame*

该设计使 SLARM-W（窗口注意力流式模式）的推理时间和内存消耗随序列长度线性增长，而 SLARM-F（全注意力离线模式）呈二次增长（Figure 5(d)），验证了流式架构在长序列场景中的部署优势。

---

### 5. 复合训练损失

总损失函数整合了多模态监督信号（Eq. (10)）：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rgb}} + \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{sky}} \mathcal{L}_{\mathrm{sky}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}} + \lambda_{\mathrm{feat}} \mathcal{L}_{\mathrm{feat}}$$

其中 $\mathcal{L}_{\mathrm{rgb}}$ 为 MSE 与 LPIPS（$\lambda_{\mathrm{lpips}}=0.05$）的加权组合（Eq. (4)），$\mathcal{L}_{\mathrm{depth}}$ 为深度监督项，$\mathcal{L}_{\mathrm{sky}}$ 为天空区域正则项，$\mathcal{L}_{\mathrm{reg}}$ 为运动正则项，$\mathcal{L}_{\mathrm{feat}}$ 为语义特征对齐项。训练使用 AdamW 优化器，共 200k 次迭代。



## 实验与关键发现

SLARM 在动态重建、语义分割与场景流估计三项核心任务上均取得显著提升，其性能优势源于高阶运动建模与语义蒸馏的协同作用。

### 动态重建主结果

在 Waymo Open Dataset (WOD) 全图设定下，SLARM 的离线全注意力版本 SLARM-F 达到 **27.49 dB PSNR**，相较前馈基线 **STORM** (Yang et al., arXiv 2024) 的 25.86 dB 提升 **1.63 dB**，SSIM 从 0.804 提升至 0.828，深度 RMSE 从 5.47 降至 4.57（Table 1）。流式窗口注意力版本 SLARM-W 也取得 27.30 dB PSNR 与 0.825 SSIM，表明流式推理模式仅以微弱性能代价换取了常数延迟的在线部署能力。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/006_Table_1.jpg]]
*Table 1: Comparison to state-of-the-art methods on the WOD. We compare photorealism and geometry metrics against generalizable feed-forward methods. PSNR, SSIM, and Depth RMSE (D-RMSE) are reported. SLARM-F denotes the model using full attention in offline mode, whereas SLARM-W uses windowattention in online mode. ∗: reproduced by us. †: Non-sky region*

在跨数据集泛化实验中，SLARM-F 在 NuScenes 上 PSNR 达 26.71 dB（vs. STORM 26.25 dB），在 Argoverse2 上达 26.49 dB（vs. STORM 26.13 dB），验证了高阶运动模型对不同场景动态特性的鲁棒适应能力（Table 4）。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/010_Table_4.jpg]]
*Table 4: Comparison on NuScenes and Argoverse2 Datasets*

### 语义分割

SLARM 在 WOD 上取得 **0.6663 mIoU**，显著超越 **LSeg** 的 0.4876（提升 0.1787），以及其他 2D 分割方法（Table 2）。定性结果（Figure 6）显示，SLARM 的分割结果在帧间具有更好的时序连贯性，这得益于语义特征作为 4D 高斯原语的固有属性，而非逐帧独立推理。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison of semantic segmentation performance. Our method produces more accurate and coherent segmentations compared to previous 2D segmentation approaches*

### 场景流估计

在 WOD 场景流评估中，SLARM-F 的 **EPE3D 降至 0.240**，较 STORM 的 0.304 降低 21%（Table 3）。值得注意的是，SLARM 的场景流完全通过渲染损失自监督学习，无需任何真实流标注。这一改进直接归因于三阶运动模型对非均匀运动（如行人步态中的加加速度分量）的更精确建模。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/008_Table_3.jpg]]
*Table 3: Comparison of scene flow estimation on the WOD*

### 消融实验

**运动阶数的影响**（Figure 5c）：将运动模型从一阶（恒定速度）逐步提升至三阶（含 jerk 项），重建 PSNR 和流估计误差持续改善，三阶时达到最优。继续增加阶数未带来额外收益，表明三阶泰勒展开已能充分捕捉自动驾驶场景中的典型运动模式。

**语义损失的贡献**（Figure 5b）：单独引入语义蒸馏损失 $\mathcal{L}_{\mathrm{sem}}$ 即可降低 Flow EPE，验证了语义一致性作为时序正则化的有效性。进一步加入分类损失 $\mathcal{L}_{\mathrm{cls}}$ 后，PSNR 和语义 mIoU 同步提升，说明显式类别监督有助于特征空间的判别性。

**教师特征选择**（Figure 7）：对比 MaskCLIP、SAM-CLIP 与 LSeg 三种语言对齐特征，LSeg 在语义连贯性和帧间连续性上表现最优，且无需额外的分割模型推理开销，被确定为最适合 4D 语义蒸馏的教师特征。

**流式推理效率**（Figure 5d）：SLARM-W 的推理时间和 GPU 显存消耗随序列长度呈线性增长，而离线模式呈二次增长。这验证了窗口因果注意力机制在长序列场景下的可扩展性优势。

### 失败模式与局限

论文明确指出 SLARM 的两个主要局限：① 依赖准确的相机姿态，在无标定或标定噪声较大的场景下性能可能退化；② 对包含玻璃、镜面等复杂材质的场景处理能力不足，因为光度一致性假设在这些区域不再成立。这两点均需在后续工作中引入额外的鲁棒信号或几何先验加以解决。

### 补充图表

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/005_Figure_5.jpg]]
*Figure 5: (a) Qualitative comparison of dynamic scenes. (b) Influence of different semantic loss terms on model performance. (c) Impact of varying motion levels on model performance. (d) Comparison of inference speed and memory usage between online and offline modes*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/009_Figure_7.jpg]]
*Figure 7: Comparison of different language-aligned features. The first row is the input consists of a set of images from adjacent frames, the next three rows correspond to the three types of features for each frame, respectively*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/011_Figure_8.jpg]]
*Figure 8: Qualitative results on a simple outdoor scene: left shows rendered RGB, depth, 3D scene flow, and semantic map from predicted 4DGS; right displays a novel view of the 4DGS in a 3DGS visualizer*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2603_22893/figures/012_Figure_9.jpg]]
*Figure 9: Qualitative results on a complex outdoor scene: left shows rendered RGB, depth, 3D scene flow, and semantic map from predicted 4DGS; right displays a novel view of the 4DGS in a 3DGS visualizer*



## 定位与知识库关联

### 与前馈式高斯重建方法的关系

SLARM 在架构范式上延续了前馈式 3D 高斯重建（feed-forward 3DGS）的技术路线，与 **LGM**（Tang et al., ECCV 2024）和 **GS-LRM**（Zhang et al., ECCV 2024）共享核心设计理念：通过 Transformer 直接从多视图图像回归像素对齐的高斯基元参数，避免逐场景优化。然而，上述方法仅处理静态场景，SLARM 将这一范式首次系统性地扩展至动态 4D 重建，其关键突破在于引入可微高阶运动建模与自监督场景流学习，使模型能够在无真实光流标注的条件下学习复杂运动模式。

与最直接的可比工作 **STORM**（Yang et al., arXiv 2024）相比，SLARM 在三个关键维度上实现了根本性改进：

1. **运动表示能力**：STORM 采用恒定速度假设（一阶运动模型），在行人肢体摆动、车辆变速等非均匀运动场景中产生显著重建误差（见 Figure 5(a)）。SLARM 将运动建模提升至三阶泰勒展开，包含速度、加速度和加加速度项，仅通过渲染损失进行自监督学习，在 WOD 数据集上将 PSNR 从 25.86 dB 提升至 27.49 dB（+1.63 dB），场景流 EPE3D 从 0.304 降至 0.240（-21%）。

2. **语义理解能力**：STORM 完全不涉及语义建模。SLARM 通过蒸馏 LSeg 的语言对齐特征，赋予每个高斯基元 512 维语义表示，使模型在输出几何与运动信息的同时，能够进行零样本语义查询。在 WOD 语义分割评测中，SLARM 的 mIoU 达到 0.6663，显著超越 LSeg 自身的 0.4876（+17.87 个百分点），表明 4D 重建过程本身为语义理解提供了有效的时序正则化。

3. **推理模式**：STORM 为离线批量处理设计。SLARM 通过窗口因果注意力机制实现了流式推理（SLARM-W），在保持 PSNR 27.30 dB（仅比离线模式低 0.19 dB）的同时，实现了线性推理时间和稳定内存消耗，支持长序列实时处理，这对自动驾驶等部署场景至关重要。

### 与通用 3D 重建模型的关系

**MapAnything** 作为通用 3D 重建模型，旨在处理多样化的静态场景，但其设计未涉及动态建模和语义对齐。SLARM 可视为在特定领域（自动驾驶动态场景）中，将通用前馈重建思路与运动物理先验、语言语义先验深度融合的专用化扩展。这种“通用架构 + 领域先验”的设计策略，为其他领域的 4D 重建研究提供了可参照的技术路径。

### 与场景流估计方法的关系

传统场景流估计方法如 **NSFP** 和 **NSFP++** 通常依赖专用网络架构和显式光流监督。SLARM 的核心创新在于将场景流估计内化为 4D 重建的副产品——通过高阶运动系数预测和可微渲染损失进行自监督学习，无需任何真实光流标注。Table 3 的结果表明，这种隐式学习方式在 EPE3D 和角度误差上均优于显式监督的基线方法，验证了“渲染即监督”范式在运动估计任务中的有效性。

### 适用边界与局限

根据论文披露的局限性，SLARM 的适用边界受以下因素制约：

1. **相机姿态依赖**：SLARM 当前要求准确的相机外参作为输入，在无精确姿态估计的场景（如手持拍摄、非结构化环境）中性能可能显著下降。这限制了其在通用视频重建任务中的直接应用。

2. **光度一致性假设**：模型依赖渲染图像与真实图像之间的光度一致性进行自监督学习。对于包含玻璃、镜面等反射/透明材质，或极端光照变化的场景，光度损失可能提供误导性信号，导致几何和运动估计失败。

3. **动态/静态划分阈值**：流式推理中的高斯状态传播依赖于运动幅度阈值 $\tau_m$ 来划分静态与动态高斯基元。该阈值的设定对场景运动尺度敏感，论文未讨论其在不同数据集间的迁移鲁棒性。

### 开放问题

1. **自标定能力的集成**：SLARM 能否将相机姿态估计（如通过束调整或位姿回归网络）集成到流式框架中，从而摆脱对外部 SLAM/SfM 系统的依赖，是走向完全端到端 4D 重建的关键一步。

2. **鲁棒光度信号的引入**：对于反射/透明物体，仅依靠光度一致性的自监督学习可能失效。引入结构光、深度传感器等多模态信号，或采用对抗性数据增强策略，可能是提升鲁棒性的可行方向。

3. **语义蒸馏教师模型的选择**：Figure 7 的消融表明 LSeg 在语义连贯性和帧间连续性上优于 MaskCLIP 和 SAM-CLIP，但随着更强视觉-语言模型（如 CLIP 变体、开放词汇分割模型）的涌现，教师特征的最优选择仍是一个开放问题。该结论需要后续工作进一步验证。

4. **运动阶数的理论解释**：Figure 5(c) 显示三阶运动模型达到最优，更高阶不再带来明显收益。论文将此归因于“三阶对应加加速度，足以描述真实物理运动”，但缺乏对数据集运动分布（如加速度谱、加加速度谱）的定量分析。该经验结论的理论基础需要进一步验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/SLARM_Streaming_and_Language_Aligned_Reconstruction_Model_for_Dynamic_Scenes.pdf]]
