---
title: "RigMo: Unifying Rig and Motion Learning for Generative Animation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RigMo_Unifying_Rig_and_Motion_Learning_for_Generative_Animation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_RigMo_Unifying_Rig_and_Motion_Learning_for_Generative_Animation_CVPR_2026_paper.html
project_link: https://RigMo-Page.github.io
code_link: null
aliases:
- RigMo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过纯自监督学习，从原始网格序列中同时推断高斯骨骼与运动参数，使模型能够从顶点轨迹中发现可泛化的关节结构，无需任何人工标注，从而打通结构—运动联合建模的关键链路。
primary_logic: 利用前馈神经网络将动态网格分解为静态的骨骼绑定特征（高斯骨骼）和动态的运动潜变量，并通过可微线性混合蒙皮和测地线感知细化实现高质量变形重建；在此基础上，扩散模型在运动潜空间中进行生成，实现结构感知的动画生成与控制。
claims:
- "RigMo在DeformingThings4D测试集的跨运动泛化任务中，CD-L1误差仅为13.82±0.49（×10^{-3}），远优于逐例优化方法（68.8±6.7）和UniRig+Optimization。"
- RigMo在重建保真度和推理效率方面均取得最佳结果，CD-L1为1.73±0.11，推理20帧仅需0.74秒 (Table 2)。
- 移除测地线权重细化模块后，CD-L1从1.73±0.11上升至2.37±0.15，验证了拓扑一致性约束对于蒙皮质量的关键作用 (Table 3)。
- "DeformingThings4D (Cross-Motion Generalization) 上 CD-L1 (×10^{-3}) = 13.82 ± 0.49"
---

# RigMo: Unifying Rig and Motion Learning for Generative Animation

> [!tip] 核心洞察
> 利用前馈神经网络将动态网格分解为静态的骨骼绑定特征（高斯骨骼）和动态的运动潜变量，并通过可微线性混合蒙皮和测地线感知细化实现高质量变形重建；在此基础上，扩散模型在运动潜空间中进行生成，实现结构感知的动画生成与控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | RigMo：联合骨骼与运动学习的生成式动画 |
| 英文题名 | RigMo: Unifying Rig and Motion Learning for Generative Animation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_RigMo_Unifying_Rig_and_Motion_Learning_for_Generative_Animation_CVPR_2026_paper.html) · [Project](https://RigMo-Page.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | RigMo |
| Dataset | DeformingThings4D |

> [!tip] 效果简介
> - DeformingThings4D (Cross-Motion Generalization) 上，CD-L1 (×10^{-3}) 13.82 ± 0.49 vs 68.8 ± 6.7 (-80.0%)。
> - DeformingThings4D (Reconstruction) 上，CD-L1 (×10^{-2}) 1.73 ± 0.11；CD-L2 (×10^{-2}) 1.26 ± 0.08。
> - DeformingThings4D (Inference) 上，Time (20f) 0.74s。

## 概要

三维可变形物体的动画生成长期面临一个根本性瓶颈：骨骼绑定（rigging）与运动生成被割裂为两个独立任务。传统管线依赖艺术家手工设计的骨架与蒙皮权重，或通过逐序列非线性优化（如 SSDR）进行逆向绑定，难以扩展至任意形状和大规模数据。这种分离式范式缺乏统一的刚性结构与运动动力学联合学习框架，导致自动化程度低、泛化能力弱。

RigMo 提出了一种前馈式生成动画框架，通过纯自监督学习从原始网格序列中同时推断高斯骨骼与运动参数。其核心洞察在于：利用双分支编码器将动态网格分解为静态的骨骼绑定特征（高斯骨骼）和动态的运动潜变量，并通过可微高斯蒙皮与测地线感知细化实现高质量变形重建；在此基础上，扩散模型在运动潜空间中进行生成，实现结构感知的动画生成与控制。该方法无需任何人工标注的骨架、蒙皮权重或姿势参数，仅依靠顶点重建损失与 KL 正则项完成端到端训练。

在 DeformingThings4D 测试集上，RigMo 展现出显著的性能优势：跨运动泛化任务中，CD-L1 误差仅为 13.82±0.49（×10⁻³），较逐例优化方法（68.8±6.7）降低约 80%；重建保真度方面，CD-L1 达到 1.73±0.11（×10⁻²），同时推理 20 帧仅需 0.74 秒，在几何精度与效率上均优于现有基线。消融实验进一步验证了测地线权重细化模块的关键作用——移除该模块后 CD-L1 升至 2.37±0.15，表明拓扑一致性约束对蒙皮质量至关重要。

在方法谱系上，RigMo 区别于依赖标注数据的自动绑定方法（如 **UniRig**）和逐序列优化方案（**SSDR**），通过前馈网络直接从顶点轨迹中发现可泛化的关节结构，打通了结构—运动联合建模的关键链路。其生成范式也从传统的顶点空间直接生成或预定义骨架姿势生成，转向在学习的运动潜空间中进行条件扩散生成，为 4D 动画的创建与控制提供了新的技术路径。

需要指出的是，RigMo 当前假设输入网格序列具有一致的拓扑与顶点数，训练数据主要来自动物和人体，对机械装置、植物等非典型可变形物体的泛化能力有待验证。此外，高斯骨骼数量 K 需提前设定，生成的运动仍受限于训练数据的多样性，在外推姿势时可能产生非物理形变。

### 问题背景

三维可变形物体的动画生成是计算机图形学与视觉计算中的核心问题，广泛应用于影视特效、游戏角色、虚拟现实和数字孪生等领域。传统的动画管线遵循一个成熟但高度手工化的流程：首先由艺术家为静态网格模型设计骨骼绑定（rigging）——定义关节层级结构并绘制蒙皮权重，再由动画师逐帧调整骨骼姿势参数以驱动网格变形。这一范式虽然能产出高质量结果，但严重依赖专业人员的大量劳动，且绑定结构一旦确定便难以迁移至不同拓扑或形态的模型，限制了动画内容的大规模生产。

### 现有方法的局限

近年来，学术界在自动化骨骼绑定和运动生成方面取得了显著进展，但现有方法普遍存在一个根本性的结构缺陷：**将骨骼绑定与运动生成视为两个分离的独立任务**。

在绑定发现方面，传统方法如 **SSDR**（Smooth Skinning Decomposition with Rigid bones）等采用逐序列非线性优化，在给定完整网格动画序列上拟合稀疏的刚性骨骼和蒙皮权重。这类方法需要针对每条新序列重新运行昂贵的迭代优化，无法实现跨实例的泛化，且对初始化高度敏感。近年来涌现的自动绑定方法（如 **UniRig**）尝试通过神经网络直接从单帧静态网格预测骨架和蒙皮权重，但它们仍依赖人工标注的骨架数据作为监督信号，难以扩展至大规模、多样化的任意形状数据集。更关键的是，这些方法在静态网格上学习绑定结构，完全忽略了运动动力学信息，导致其在真实动画驱动下出现严重的变形失真——即便蒙皮权重在视觉上看似合理，一旦施加新姿势便可能崩溃。

在运动生成方面，现有方法要么直接在顶点点空间上操作（缺乏结构先验，易产生非物理形变），要么依赖预定义的固定骨架进行姿势生成（限制了可泛化性）。这两种范式都无法实现“结构—运动”的联合理解：前者没有骨骼结构的概念，后者无法从运动中推断结构。

### 核心瓶颈

上述分离式管线的根本瓶颈在于：**缺乏一个统一的刚性结构与运动动力学的联合学习框架**。具体表现为三个层面：

1. **结构推断与运动学习的信息割裂**：绑定发现仅利用静态几何，运动生成仅利用姿势序列，二者无法相互促进。实际上，网格的运动轨迹蕴含了丰富的结构线索——哪些区域协同运动、哪些部位相对独立，这些信息对于推断合理的关节位置和蒙皮权重至关重要。

2. **对人工标注的过度依赖**：无论是骨架拓扑设计、蒙皮权重绘制还是姿势参数标注，都需要大量专家劳动，使得现有方法难以利用互联网规模的无标注动态网格数据进行扩展训练。

3. **泛化能力的缺失**：逐序列优化方法无法跨实例迁移，而基于监督学习的方法受限于标注数据的分布，在面对训练集未见过的物体类别或极端姿势时性能急剧下降。

### 本文动机

针对上述瓶颈，**RigMo** 提出了一种全新的范式：**通过纯自监督学习，从原始网格序列中同时推断刚性结构与运动参数，实现“结构—运动”的端到端联合建模**。

其核心动机源于一个关键洞察：动态网格的顶点轨迹天然编码了物体的刚性结构信息——如果能够设计一个可微分的绑定-蒙皮-变形前馈管线，使得网络在仅以顶点重建为监督信号的条件下，被迫从运动中发现有意义的高斯骨骼和蒙皮权重，那么就能打通结构推断与运动学习之间的信息壁垒。进一步，在学到的结构化运动潜空间中引入生成模型（如扩散模型），便可实现结构感知的运动生成与可控动画合成。

这一思路的技术可行性建立在三个关键设计之上：（1）双分支编码器将静态几何与动态运动解耦为刚性潜变量和运动潜变量；（2）基于马氏距离的可微高斯蒙皮模块，使骨骼参数的梯度能够通过线性混合蒙皮（LBS）反向传播至编码器；（3）测地线感知的权重细化机制，利用表面拓扑距离抑制跨部位的非物理影响，保证蒙皮权重的拓扑一致性。这些组件共同构成了一个无需任何骨骼或蒙皮标注、仅依赖顶点重建损失即可端到端训练的统一框架，为大规模生成式动画开辟了新路径。

## 核心方法与创新机理

RigMo 的核心创新在于将**骨骼绑定推断**与**运动生成**统一为一个纯自监督的前馈框架，从根本上改变了传统动画管线中“先绑定、后驱动”的分离范式。其关键突破体现在以下四个维度。

### 从逐例优化到前馈推断：骨骼结构的自主学习

传统骨骼绑定方法（如 **SSDR** 等逐序列非线性优化方案）需要为每个网格序列单独求解骨架与蒙皮权重，计算成本高且无法跨形状泛化。RigMo 通过**前馈神经网络**直接从原始顶点序列中推断显式的高斯骨骼描述（骨骼中心 $c_k$、各向异性尺度 $s_k$、方向 $R_k$），无需任何人工标注的骨架或蒙皮先验。这一转变使得模型能够从大规模运动数据中**自动发现可泛化的关节结构**，而非拟合单序列的特定形变——在 DeformingThings4D 跨运动泛化测试中，RigMo 的 CD-L1 误差仅为 $13.82 \pm 0.49$（$\times 10^{-3}$），相较逐例优化方法的 $68.8 \pm 6.7$ 降低了约 **80%**（Table 1），充分验证了前馈推断在结构泛化上的根本优势。

### 从刚性蒙皮到拓扑感知的高斯蒙皮

传统蒙皮权重计算通常依赖骨架距离或手工设计的刚性绑定，容易在拓扑不连续区域产生跨部位的影响泄漏。RigMo 提出了**基于马氏距离的可微高斯蒙皮**机制（Eq. 11），利用高斯骨骼的坐标系对顶点进行各向异性距离度量，生成软蒙皮权重 $w_{ik}$；在此基础上，引入**测地线感知权重细化**（Eq. 13–15）：通过表面测地距离生成二值掩膜 $M_{ik}$，强制抑制拓扑不相关区域之间的权重传播，保证蒙皮权重的拓扑一致性。消融实验显示，移除测地线细化模块后，CD-L1 从 $1.73 \pm 0.11$ 上升至 $2.37 \pm 0.15$（$\times 10^{-2}$，Table 3），直接证实了拓扑约束对蒙皮质量的关键作用。

### 从顶点空间生成到潜空间条件扩散

现有运动生成方法或直接在顶点空间操作，或依赖预定义骨架的姿势参数，缺乏对底层刚性结构的感知。RigMo 的生成范式发生根本转移：**运动扩散模型（Motion DiT）并非在原始顶点空间生成，而是在 RigMo-VAE 学到的运动潜空间中进行**。具体而言，RigMo-VAE 将运动分解为局部骨骼变换潜变量 $z_{\text{local}}$ 和根运动潜变量 $z_{\text{root}}$，Motion DiT 以刚性分支输出的静态骨骼特征作为条件信号，通过时空交叉注意力引导扩散过程，生成时序运动潜变量后再经高斯蒙皮解码为完整网格序列。这种“结构条件化 + 潜空间生成”的范式使模型天然具备结构感知能力，生成的动画始终保持与输入几何的骨骼一致性。

### 从强监督到纯自监督的训练范式

传统绑定与运动生成方法依赖人工标注的骨架拓扑、蒙皮权重或姿势参数进行监督，标注成本高昂且难以扩展至任意形状。RigMo 实现了**完全的标注解耦**：整个 RigMo-VAE 仅通过顶点重建损失 $\mathcal{L}_{\text{recon}}$ 和 KL 正则项 $\mathcal{L}_{\text{KL}}$ 进行端到端训练（Eq. 16–18），无需任何 rig 相关的监督信号。这一设计使得模型能够利用约 20,000 个来自 DeformingThings4D、TrueBones 和 Objaverse-XL 的网格序列进行大规模预训练，从根本上解决了标注瓶颈对可扩展性的制约。

RigMo 提出了一种前馈式动画生成框架，其核心思路是将骨骼绑定（rigging）与运动学习（motion）统一到一个端到端的可学习管线中，直接从原始网格顶点序列出发，无需任何人工标注的骨架、蒙皮权重或姿态参数。整个 pipeline 由两大阶段构成：（1）**RigMo-VAE**，负责从动态网格中解耦出静态的刚性结构与动态的运动潜变量，并实现高保真重建；（2）**Motion DiT**，在 RigMo-VAE 学到的运动潜空间中进行条件扩散生成，实现结构感知的动画合成与控制。

### 输入输出规范

给定一个包含 $B$ 个样本、每样本 $T$ 帧、每帧 $N$ 个顶点的网格序列 $\mathbf{V} \in \mathbb{R}^{B \times T \times N \times 3}$，RigMo-VAE 的输出是重建的变形运动 $\hat{\mathbf{V}} \in \mathbb{R}^{B \times (T-1) \times N \times 3}$。这里的核心假设是：输入序列的所有帧共享一致的拓扑和顶点数——这也是当前框架的主要约束之一。

### RigMo-VAE：双路径编码-解码架构

RigMo-VAE 的设计遵循“结构-运动解耦”原则，通过双路径编码器分别处理静态几何与动态形变，再经由统一的解码器重建出可动画化的表示（Figure 2）。

**编码阶段**由两个并行的分支构成：

- **刚性分支（Rigging Branch）**：以首帧网格的顶点几何作为输入，通过拓扑感知的注意力层提取顶点嵌入，再与一组可学习的骨骼令牌（bone tokens）进行交叉注意力交互，建立骨骼-顶点的对应关系。该分支的输出是刚性特征 $\mathbf{A}_{\mathrm{rig}}$，它编码了网格的静态结构信息。

- **运动分支（Motion Branch）**：以相邻帧间的顶点位移 $\mathbf{V}_{\Delta} = \mathbf{V}[:, 1:, :, :] - \mathbf{V}[:, :-1, :, :]$ 作为输入，同样经过拓扑感知注意力编码后，与骨骼令牌进行交叉注意力，得到骨骼-运动交互特征 $\mathbf{A}_{\mathrm{motion}}$。该特征随后被送入两个 MLP 头，分别预测局部运动的变分后验参数 $[\boldsymbol{\mu}_{\mathrm{local}}, \log \boldsymbol{\sigma}_{\mathrm{local}}]$ 和根节点运动的全局后验参数 $[\boldsymbol{\mu}_{\mathrm{root}}, \log \boldsymbol{\sigma}_{\mathrm{root}}]$。通过重参数化技巧，从这些分布中采样得到局部运动潜变量 $\mathbf{z}_{\mathrm{local}}$ 和根运动潜变量 $\mathbf{z}_{\mathrm{root}}$。

**解码阶段**将两类潜变量映射为物理可解释的动画组件：

- **刚性解码器**：将刚性分支的特征解码为一组显式的高斯骨骼 $\mathcal{G}$，每根骨骼由中心 $\mathbf{c}_k$、尺度 $\mathbf{s}_k$ 和方向 $\mathbf{R}_k$ 三个参数描述。这些高斯骨骼是后续蒙皮权重计算的基础。

- **运动解码器**：将 $\mathbf{z}_{\mathrm{local}}$ 解码为每骨骼每帧的局部 SE(3) 变换 $\{\mathbf{q}_{\mathrm{local}}, \mathbf{t}_{\mathrm{local}}\}$，将 $\mathbf{z}_{\mathrm{root}}$ 解码为全局根节点变换 $\{\mathbf{q}_{\mathrm{root}}, \mathbf{t}_{\mathrm{root}}\}$。层次化组合后得到每根骨骼的完整变换矩阵 $\mathbf{T}_k$。

**变形重建**通过可微的高斯蒙皮模块完成：首先基于马氏距离计算每个顶点对每根骨骼的原始蒙皮权重 $w_{ik}^{\mathrm{raw}}$，然后引入测地线感知的权重细化——利用表面测地距离生成二值掩膜，抑制拓扑不相关部位之间的错误影响——最后通过线性混合蒙皮（LBS）将骨骼变换作用于顶点，得到重建位置 $\hat{\mathbf{v}}_i = \sum_{k=1}^{K} w_{ik} \cdot \mathbf{T}_k \cdot \tilde{\mathbf{v}}_i$。

整个 RigMo-VAE 采用纯自监督训练，损失函数仅包含两项：顶点级 L2 重建损失 $\mathcal{L}_{\mathrm{recon}}$ 和隐变量 KL 正则项 $\mathcal{L}_{\mathrm{KL}}$，无需任何骨骼或蒙皮的真值标注。

### Motion DiT：条件扩散运动生成

在 RigMo-VAE 完成训练后，其运动潜空间 $\mathbf{z}_{\mathrm{local}}$ 和 $\mathbf{z}_{\mathrm{root}}$ 已经形成了一个紧凑且结构化的运动表示。Motion DiT 在这一潜空间中构建条件扩散模型（Figure 3）：以刚性分支提取的静态骨骼特征作为条件信号，通过一个条件编码器生成锚点令牌（anchor tokens）和全局令牌（global tokens），引导扩散 Transformer 在运动潜空间中进行去噪过程。模型使用空间注意力、时间注意力和帧条件交叉注意力来预测去噪后的运动潜变量，这些潜变量随后被 RigMo-VAE 的解码器还原为骨骼变换和顶点序列。

扩散阶段的训练采用多级加权损失：潜空间损失 $\mathcal{L}_{\mathrm{lat}}$（权重 0.5）、旋转损失 $\mathcal{L}_{\mathrm{rot}}$（权重 1.0）、平移损失 $\mathcal{L}_{\mathrm{trans}}$（权重 0.2）和顶点损失 $\mathcal{L}_{\mathrm{vert}}$（权重 0.1），以确保生成的运动在潜空间、骨骼变换和最终顶点三个层面都与真实运动保持一致。

### 端到端动画生成流程

完整 RigMo 管线的工作流程可概括为：给定一段网格序列（甚至可以是稀疏观测的部分帧），RigMo 首先通过双路径编码器推断出高斯骨骼和蒙皮权重（刚性结构），同时将运动信息压缩为潜变量；随后，Motion DiT 以刚性条件为引导，在潜空间中生成完整的运动轨迹；最后，高斯蒙皮模块将骨骼变换解码为高保真的动画网格序列（Figure 4）。这种“结构推断—运动生成—蒙皮解码”的级联设计，使得 RigMo 能够在没有任何人工标注的条件下，从原始顶点数据中发现可泛化的关节结构并合成自然运动。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RigMo_Unifying_R/figures/001_Figure_1.jpg]]
*Figure 1: RigMo jointly learns rigging and motion by understanding the underlying structure of mesh sequences. Unlike optimizationbased methods that fit a rig per sequence, RigMo is a feed-forward framework that infers Gaussian bones, skinning weights, and motion parameters directly from input meshes for unified 4D animation generation. Colors visualize the influence of Gaussian bones on vertices (skinning weights) across the mesh surface; similar colors may appear for different bones as they are randomly assigned for visualization*

RigMo 的核心架构由两大组件构成：**RigMo-VAE** 负责从原始网格序列中自监督地学习骨骼绑定与运动表示，**Motion DiT** 则在该学习的运动潜空间中进行条件扩散生成。以下按模块拆解其关键设计与公式。

### 拓扑感知编码器 (Topology-aware Encoder)

编码器采用双分支结构，将静态几何与动态运动解耦。输入为网格顶点序列 $\mathbf{V} \in \mathbb{R}^{B \times T \times N \times 3}$（批大小 $B$、帧数 $T$、顶点数 $N$）。

**拓扑感知注意力层** 首先对每帧顶点独立编码，利用网格邻域信息增强结构感知：

$$\mathbf{h}_{\ell} = \mathrm{Attn}(\mathrm{LN}(\mathbf{h}_{\ell-1}), \mathcal{N}) + \mathbf{h}_{\ell-1}$$

其中 $\mathcal{N}$ 为顶点邻域集合，$\mathrm{LN}$ 为层归一化。该层堆叠 6 次（隐藏维度 256，8 头注意力，邻域大小 $k=5$），输出顶点嵌入 $\mathbf{V}^{\mathrm{emb}}$。

**刚性分支 (Rigging Branch)** 仅处理首帧（规范姿态）顶点嵌入 $\mathbf{V}_0^{\mathrm{emb}}$，通过可学习的骨骼令牌 $\mathbf{B}^{\mathrm{emb}} \in \mathbb{R}^{K \times d_b}$ 与顶点特征进行交叉注意力，建立骨骼-顶点关联：

$$\mathbf{A}_{\mathrm{rig}} = \mathrm{CrossAttn}(\mathbf{B}^{\mathrm{emb}}, \mathbf{V}_0^{\mathrm{emb}}, \mathbf{V}_0^{\mathrm{emb}})$$

**运动分支 (Motion Branch)** 以帧间顶点位移作为输入：

$$\mathbf{V}_{\Delta} = \mathbf{V}[:, 1:, :, :] - \mathbf{V}[:, :-1, :, :] \in \mathbb{R}^{B \times (T-1) \times N \times 3}$$

将位移嵌入与骨骼令牌进行交叉注意力，捕获骨骼运动交互：

$$\mathbf{A}_{\mathrm{motion}} = \mathrm{CrossAttn}(\mathbf{B}^{\mathrm{emb}}, \mathbf{V}_{\Delta}^{\mathrm{emb}}, \mathbf{V}_{\Delta}^{\mathrm{emb}}) \in \mathbb{R}^{B \times (T-1) \times K \times d_b}$$

随后通过时序-空间注意力提取运动动力学特征。

### 刚性-运动解码器 (Rig-Motion Decoder)

解码器将双分支特征映射为物理可解释的绑定与运动参数。

**刚性解码** 从 $\mathbf{A}_{\mathrm{rig}}$ 解码出 $K$ 个高斯骨骼描述子 $\mathcal{G} = \{(\mathbf{c}_k, \mathbf{s}_k, \mathbf{R}_k)\}_{k=1}^{K}$，分别表示骨骼中心、轴对齐尺度和旋转矩阵。

**运动解码** 从运动分支特征预测变分后验参数。局部运动后验（每骨骼每帧）：

$$[\boldsymbol{\mu}_{\mathrm{local}}, \log \boldsymbol{\sigma}_{\mathrm{local}}] = \mathrm{MLP}(\mathbf{A}_{\mathrm{motion}})$$

$$\mathbf{z}_{\mathrm{local}} = \boldsymbol{\mu}_{\mathrm{local}} + \boldsymbol{\sigma}_{\mathrm{local}} \odot \boldsymbol{\epsilon}, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I})$$

全局根运动后验（时序聚合后）：

$$[\boldsymbol{\mu}_{\mathrm{root}}, \log \boldsymbol{\sigma}_{\mathrm{root}}] = \mathbf{MLP}(\mathrm{Agg}(\mathbf{A}_{\mathrm{motion}}))$$

$$\mathbf{z}_{\mathrm{root}} = \boldsymbol{\mu}_{\mathrm{root}} + \boldsymbol{\sigma}_{\mathrm{root}} \odot \epsilon$$

潜变量经解码器映射为 SE(3) 变换：

$$\{ \mathbf{q}_{\mathrm{local}}, \mathbf{t}_{\mathrm{local}} \} = \mathrm{Dec}_{\mathrm{local}}(\mathbf{z}_{\mathrm{local}})$$

$$\{ \mathbf{q}_{\mathrm{root}}, \mathbf{t}_{\mathrm{root}} \} = \mathrm{Dec}_{\mathrm{root}}(\mathbf{z}_{\mathrm{root}})$$

其中 $\mathbf{q}_{\mathrm{local}}$ 为每骨骼旋转四元数，$\mathbf{t}_{\mathrm{local}}$ 为局部平移；$\mathbf{q}_{\mathrm{root}}$、$\mathbf{t}_{\mathrm{root}}$ 为全局根节点旋转与平移。

### 高斯蒙皮与测地线感知细化 (Gaussian Skinning LBS)

该模块是 RigMo 实现高质量变形重建的核心机制，将骨骼变换与蒙皮权重结合生成变形顶点。

**马氏距离蒙皮权重** 基于高斯骨骼坐标系计算软蒙皮权重，使骨骼影响范围自然地随尺度和方向变化：

$$w_{ik}^{\mathrm{raw}} = \frac{\exp\left( -\frac{1}{2} \| \mathbf{R}_k^{\top}(\mathbf{v}_i - \mathbf{c}_k) \oslash \mathbf{s}_k \|^2 \right)}{\sum_{j=1}^{K} \exp\left( -\frac{1}{2} \| \mathbf{R}_j^{\top}(\mathbf{v}_i - \mathbf{c}_j) \oslash \mathbf{s}_j \|^2 \right)}$$

其中 $\oslash$ 表示逐元素除法，$\mathbf{v}_i$ 为规范姿态下的顶点坐标。

**线性混合蒙皮** 将层次化骨骼变换（根变换 $\times$ 局部变换）通过蒙皮权重作用于顶点：

$$\hat{\mathbf{v}}_i = \sum_{k=1}^{K} w_{ik} \cdot \mathbf{T}_k \cdot \tilde{\mathbf{v}}_i$$

其中 $\mathbf{T}_k$ 为骨骼 $k$ 的累积变换矩阵，$\tilde{\mathbf{v}}_i$ 为齐次坐标扩展。

**测地线感知权重细化** 是消融实验验证的关键设计。原始马氏距离权重可能将骨骼影响错误地扩散到拓扑不相关的表面区域（如左臂骨骼影响右臂顶点）。该模块计算顶点到骨骼锚点 $a_k$ 的测地距离 $d_g$，生成二值掩膜抑制远距离影响：

$$M_{ik} = \begin{cases} 1, & d_g(v_i, a_k) < \tau \\ 0, & \text{otherwise} \end{cases}$$

最终权重经掩膜过滤并重归一化：

$$w_{ik} = \frac{\tilde{W}_{ik}}{\sum_{j=1}^{K} \tilde{W}_{ij} + \varepsilon}, \quad \tilde{W}_{ik} = w_{ik}^{\mathrm{raw}} \odot M_{ik}$$

消融实验（Table 3）表明，移除该模块后 CD-L1 从 $1.73 \times 10^{-2}$ 升至 $2.37 \times 10^{-2}$，验证了拓扑一致性约束对蒙皮质量的关键作用。

### 自监督训练目标 (RigMo-VAE)

RigMo-VAE 完全自监督训练，无需任何骨骼或蒙皮标注。总损失为重建损失与 KL 正则的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}}$$

**顶点重建损失** 强制变形后顶点与原始网格一致：

$$\mathcal{L}_{\mathrm{recon}} = \frac{1}{B T N} \sum_{b, t, i} \| \hat{\mathbf{v}}_{b, t, i} - \mathbf{v}_{b, t, i} \|^2$$

**KL 正则损失** 将局部与根运动潜变量的后验分布拉向标准高斯先验，保证潜空间的连续性与可采样性：

$$\mathcal{L}_{\mathrm{KL}} = \frac{1}{2} \sum_{i} (\mu_i^2 + \sigma_i^2 - \log \sigma_i^2 - 1)$$

### Motion DiT（条件扩散 Transformer）

在 RigMo-VAE 训练收敛后，Motion DiT 在其冻结的运动潜空间中执行条件扩散生成。给定刚性分支输出的静态绑定特征作为条件，扩散 Transformer 从高斯噪声逐步去噪生成运动潜变量序列，再通过高斯蒙皮解码为完整动画。扩散阶段采用多级加权损失：

$$\mathcal{L} = \lambda_{\mathrm{lat}} \mathcal{L}_{\mathrm{lat}} + \lambda_{\mathrm{rot}} \mathcal{L}_{\mathrm{rot}} + \lambda_{\mathrm{trans}} \mathcal{L}_{\mathrm{trans}} + \lambda_{\mathrm{vert}} \mathcal{L}_{\mathrm{vert}}$$

四项分别对应潜空间、旋转、平移和顶点层级的监督，权重依次为 0.5、1.0、0.2、0.1。该设计使生成过程既能保持运动潜空间的语义一致性，又能精确还原骨骼变换与网格形变。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RigMo_Unifying_R/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the RigMo-VAE framework. Given temporal vertex trajectories from deforming mesh sequences, RigMo employs a dual-path encoder to disentangle static geometry (rigging branch) and dynamic motion (motion branch), learning a compact latent representation that captures both spatial structure and temporal dynamics. The decoder maps these latent features to physically interpretable rig components: Gaussian bone descriptors defining geodesic-aware skinning weights and variational motion parameters for local and root transformations. Different colors indicate the influence regions of learned Gaussian bones, demonstrating semantically meaningful decomposition of mesh deformation without ma...*

![[assets/figures/papers/paper_list_l26_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RigMo_Unifying_R/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the Motion DiT. Given static rigging features, a condition encoder produces anchor and global tokens that guide a diffusion transformer operating in RigMo’s motion-latent space. The model uses spatial, temporal, and frame-conditioned cross-attention to predict denoised motion latents, which are decoded into bone transformations and vertex sequences via Gaussian skinning*

## 实验与关键发现

### 数据集与评估协议

RigMo 在三个互补的大规模数据集上进行训练与评估，总计约 20,000 个可变形网格序列。**DeformingThings4D (DT4D)** 提供 1,972 个真实世界扫描序列，涵盖多种动物类别，是跨运动泛化评估的核心基准。**TrueBones** 包含带有艺术家标注骨架的动画网格，用于验证骨骼发现的可解释性。**Objaverse-XL** 则提供大规模合成数据以支撑自监督预训练。所有方法在相同的训练/验证/测试划分上进行评估，RigMo 完全在无骨骼或蒙皮标注的无监督设置下训练。

评估指标采用倒角距离的 L1 和 L2 变体（CD-L1/L2），度量预测网格与真值网格之间的几何偏差，数值越低表示重建精度越高。推理效率以处理 20 帧序列的耗时衡量。

### 骨骼绑定发现与跨运动泛化

Table 1 报告了在 DT4D 测试集上的骨骼发现与跨运动泛化能力。RigMo 以纯前馈方式推断骨骼绑定结构，并在未见过的新运动序列上进行泛化测试，取得了 CD-L1 为 **13.82 ± 0.49**（×10⁻³）的结果。相比之下，逐序列优化的 SSDR 方法（Per-Case Optimization）误差高达 68.8 ± 6.7，RigMo 实现了约 80% 的相对提升。UniRig 作为自动绑定基线，在结合逐例优化后仍显著劣于 RigMo 的前馈推断结果。

Figure 5 的定性对比揭示了这一差距的深层原因：UniRig 虽然在某些情况下可以产生视觉上合理的蒙皮权重（如狐狸示例），但其绑定的骨架结构缺乏泛化性——在应用于实际动画时，蒙皮权重无法适应新的运动范围，导致网格出现严重的塌陷和撕裂伪影。相反，RigMo 直接从运动中学习刚性结构，无需任何真值骨骼监督，即可在多样的姿态和动物种类间保持稳定、高保真的形变。

![[assets/figures/papers/paper_list_l26_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RigMo_Unifying_R/figures/006_Figure_5.jpg]]
*Figure 5: Comparison between UniRig+Optimization and our RigMo Rigging Module. Although UniRig may produce visually plausible skinning weights in some cases (e.g., the fox), its rigging does not generalize and collapses under actual animation, leading to severe deformation artifacts. In contrast, RigMo learns robust and transferable rig structures directly from motion, without any ground-truth rig supervision, and achieves stable, high-fidelity deformations across diverse poses and animal species*

这一结果验证了 RigMo 的核心主张：**通过联合学习骨骼结构与运动动力学，模型能够从顶点轨迹中发现可泛化的关节结构**，而非仅仅拟合单个序列的表面变形模式。

### 重建保真度与推理效率

Table 2 对比了各方法在 DT4D 上的重建精度和推理效率。RigMo 在所有指标上均取得最优结果：CD-L1 为 **1.73 ± 0.11**（×10⁻²），CD-L2 为 **1.26 ± 0.08**（×10⁻²）。在推理速度方面，RigMo 处理 20 帧序列仅需 **0.74 秒**，显著快于所有对比基线，体现了前馈框架相较于逐例优化方法的效率优势。

![[assets/figures/papers/paper_list_l26_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RigMo_Unifying_R/figures/007_Table_2.jpg]]
*Table 2: Reconstruction fidelity and inference efficiency*

这一双重优势源于 RigMo 的架构设计：双路径编码器将静态几何与动态运动解耦为紧凑的潜表示，解码器通过可微高斯蒙皮和测地线感知细化直接生成变形顶点，避免了迭代优化的计算开销。

### 消融实验

Table 3 在 DT4D 验证集上对关键设计选择进行了消融分析。

![[assets/figures/papers/paper_list_l26_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_RigMo_Unifying_R/figures/008_Table_3.jpg]]
*Table 3: Ablation study on the DeformingThings4D validation set using CD-L1/L2 metrics*

**测地线感知权重细化**：移除该模块后，CD-L1 从 1.73 上升至 2.37（×10⁻²），性能退化显著。该结果验证了表面测地距离约束对于蒙皮质量的关键作用——通过抑制拓扑不相关部位之间的跨区域影响，测地线掩膜有效防止了变形过程中相邻但语义无关的身体部位（如动物的前后腿）产生不合理的联动伪影。

**骨骼令牌数量**：实验对比了 48 个和 128 个骨骼令牌的配置。128 个骨骼令牌取得了最佳的定量重建结果，表明更丰富的骨骼表示能力有助于捕获细粒度的形变模式。然而，这一超参数需要提前设定，可能并非对所有物体类别都是最优选择，构成方法的一个已知局限。

### 已知局限与失败模式

尽管 RigMo 在多个基准上取得了领先结果，论文明确指出了以下局限：

1. **拓扑一致性假设**：RigMo 要求输入的网格序列具有一致的顶点数和连接关系，无法直接处理拓扑变化的网格。这限制了其在涉及网格重剖分或拓扑修改的场景中的应用。
2. **类别泛化边界**：训练数据主要来自动物和人体，对机械装置、植物等非典型可变形物体的泛化能力未经验证。在这些域外类别上，高斯骨骼假设可能无法有效捕获形变模式。
3. **骨骼数量的先验依赖**：高斯骨骼数量 K 需人为设定，超参数选择依赖领域经验。对于结构复杂度差异显著的物体，固定骨骼数可能导致欠拟合或过参数化。
4. **运动外推的物理合理性**：生成的运动仍受限于训练数据的多样性，在远离训练分布的姿态下可能产生非物理形变。扩散模型在潜空间中的外推缺乏显式的物理约束。
5. **模态单一性**：当前框架仅接收纯顶点序列作为输入，未利用图像、纹理等多模态信息，限制了其在需要视觉条件生成的场景中的适用性。

这些局限为后续研究指明了方向：引入自适应骨骼数量推断、融合多模态条件信号、以及施加物理约束的生成机制，将是提升框架泛化性和鲁棒性的关键路径。

## 定位与知识库关联

### 核心问题与现有范式

传统可变形物体动画生成管线存在一个根本性瓶颈：骨骼绑定（rigging）与运动生成（animation）被割裂为两个独立阶段。骨骼绑定依赖艺术家手工设计骨架与蒙皮权重，或借助逐序列非线性优化方法（如 SSDR）进行逆蒙皮拟合，这些方法不仅耗时，且难以跨形状泛化。运动生成则通常直接操作顶点空间，或依赖预定义骨架的姿势参数，缺乏对底层刚性结构的统一建模。这种分离范式导致动画管线难以扩展至任意形状和大规模数据，无法实现结构感知的运动合成。

RigMo 的核心贡献在于打通了“结构—运动”联合建模的关键链路：通过纯自监督学习，从原始网格序列中同时推断显式的高斯骨骼（Gaussian bones）与运动参数，使模型能够从顶点轨迹中发现可泛化的关节结构，无需任何人工标注。这一思路在以下维度上区别于现有工作：

1. **相对于逐序列优化方法（SSDR 类）**：SSDR 对每个序列独立求解逆蒙皮问题，计算成本高且无法共享跨实例的结构先验。RigMo 采用前馈神经网络一次性推断骨骼与蒙皮权重，推理 20 帧仅需 0.74 秒（Table 2），且跨运动泛化误差（CD-L1 = 13.82 × 10⁻³）远优于 SSDR 的逐例优化结果（68.8 × 10⁻³）（Table 1）。

2. **相对于自动绑定方法（UniRig）**：UniRig 等基线依赖人工标注的骨架或蒙皮数据进行监督训练，其学到的绑定结构在未见运动上容易崩溃，产生严重变形伪影（Figure 5 定性对比）。RigMo 完全无需 rig 标注，通过顶点重建损失和 KL 正则项进行端到端自监督训练，学到的骨骼-蒙皮结构具有更强的泛化鲁棒性。

3. **相对于直接顶点生成方法**：在顶点点空间直接生成运动缺乏对刚性结构的显式约束，容易产生非物理形变。RigMo 在 VAEs 学到的局部/全局运动潜空间中通过 Motion DiT（条件扩散 Transformer）生成运动，再经高斯蒙皮解码为网格序列，实现了结构感知的动画生成与控制。

### 关键技术断点与因果链路

RigMo 的技术链路可拆解为以下因果环节，每个环节对应一个明确的断点突破：

| 环节 | 基线做法 | RigMo 方案 | 因果作用 |
|------|----------|------------|----------|
| 骨骼结构推断 | 手工设计或逐序列非线性优化 | 前馈网络从首帧网格直接推断高斯骨骼（中心、尺度、方向） | 消除人工标注依赖，实现跨实例结构共享 |
| 蒙皮权重计算 | 基于骨架距离或手工刚性蒙皮 | 马氏距离可微高斯蒙皮 + 测地线感知权重细化 | 保证拓扑一致性，抑制跨部位伪影 |
| 运动编码 | 直接操作顶点坐标 | 双分支 VAE 将静态几何与动态运动解耦为 rig latent 和 motion latent | 实现结构-运动的显式分离与联合建模 |
| 运动生成 | 顶点点空间生成或骨架姿势生成 | Motion DiT 在运动潜空间中以刚性条件为引导进行扩散生成 | 结构感知的动画合成，支持稀疏观测补全 |
| 训练监督 | 需要骨骼/蒙皮/姿势标注 | 纯自监督（顶点重建 + KL 正则） | 可利用大规模无标注网格序列进行训练 |

其中，**测地线感知权重细化**（geodesic-aware weight refinement）是最关键的消融发现：移除该模块后，CD-L1 从 1.73 升至 2.37（×10⁻²），验证了拓扑一致性约束对于蒙皮质量的决定性作用（Table 3）。其机制在于利用表面测地距离生成二值掩膜，抑制拓扑不相关区域之间的跨部位权重泄漏（Eq. 13-15），这对于保持变形后网格的局部刚性至关重要。

### 适用边界与局限

RigMo 的适用边界由以下假设和约束定义，这些也是未来工作的潜在突破方向：

1. **拓扑一致性假设**：RigMo 假设输入的网格序列具有一致的顶点数和连接关系，无法直接处理拓扑变化或不同网格之间的迁移。这一约束源于高斯蒙皮 LBS 模块需要固定的顶点-骨骼对应关系。

2. **训练数据分布限制**：当前训练数据主要来自 DeformingThings4D（1,972 个真实序列）、TrueBones 和 Objaverse-XL，合计约 20,000 个序列，主体为动物和人体。对机械装置、植物、流体等非典型可变形物体的泛化能力未经验证，需要人工确认。

3. **骨骼数量预设**：高斯骨骼的数量 K 需要提前设定（实验表明 128 个骨骼 token 优于 48 个，Table 3），但最优 K 值可能因物体复杂度而异，缺乏自适应机制。

4. **运动外推风险**：Motion DiT 生成的运动仍受限于训练数据的多样性，在外推极端姿势时可能产生非物理形变。扩散模型的多样性-保真度权衡在此场景下尚未充分探索。

5. **模态单一性**：当前框架仅接收纯顶点序列作为输入，未利用图像、纹理或物理仿真等多模态信息，限制了在视觉质量或物理合理性上的进一步提升空间。

### 开放问题

- 如何将 RigMo 的骨骼-运动联合学习框架扩展至非一致拓扑的网格集合，实现跨形状的绑定迁移？
- 高斯骨骼的数量 K 能否设计为自适应机制，根据物体复杂度动态调整？
- Motion DiT 的扩散过程是否可以引入物理约束（如动量守恒、穿透惩罚）以提升生成运动的物理合理性？
- 该框架能否与图像/视频生成模型（如 video diffusion models）结合，实现从单张图片或视频直接生成可驱动的 4D 资产？

## 原文 PDF

![[paperPDFs/CVPR_2026/RigMo_Unifying_Rig_and_Motion_Learning_for_Generative_Animation.pdf]]
