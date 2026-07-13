---
title: "PrITTI: Primitive-based Generation of Controllable and Editable 3D Semantic Urban Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PrITTI_Primitive_based_Generation_of_Controllable_and_Editable_3D_Semantic_Urban_Scenes.pdf
project_link: "https://raniatze.github.io/pritti/"
code_link: "https://github.com/ZiYang-xie/WorldGen"
aliases:
- PrITTI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用紧凑的混合基元表示（栅格化地面 + 参数化物体基元）以及解耦的布局潜在空间，使得潜在扩散模型能够高效生成、编辑和条件控制。
primary_logic: 将城市场景分解为栅格化的地面高程图与参数化的物体基元，并通过解耦的变分自编码器嵌入统一2D潜在空间，利用 Transformer 扩散模型实现高质量、可控且可编辑的3D语义布局生成。
claims:
- PrITTI 在 KITTI-360 数据集上的生成指标（Precision 0.712, Recall 0.491, FID 73.952, IS 3.856）均显著优于基于体素的最佳基线 XCube Level 2（Precision 0.482 等），且推理速度提升约 6 倍（0.58 s vs 3.50 s）。
- 解耦的潜在空间设计对重建质量至关重要：移除 latent split 导致 AP3D 从 62.12 降至 53.78，MSE 从 0.0075 升至 0.0355。
- Cholesky 参数化相比四元数编码在合成实验中表现出更高的重建稳定性和平均 IoU3D，性能随数据量增加而提升，而四元数方法出现饱和。
- KITTI-360 上 Precision ↑ = 0.712
---

# PrITTI: Primitive-based Generation of Controllable and Editable 3D Semantic Urban Scenes

> [!tip] 核心洞察
> 将城市场景分解为栅格化的地面高程图与参数化的物体基元，并通过解耦的变分自编码器嵌入统一2D潜在空间，利用 Transformer 扩散模型实现高质量、可控且可编辑的3D语义布局生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | PrITTI：基于基元的可控可编辑3D语义城市场景生成 |
| 英文题名 | PrITTI: Primitive-based Generation of Controllable and Editable 3D Semantic Urban Scenes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.19117) · [Project](https://raniatze.github.io/pritti/) · [Code](https://github.com/ZiYang-xie/WorldGen) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PrITTI |
| Dataset | KITTI-360 |

> [!tip] 效果简介
> - KITTI-360 上，Precision ↑ 0.712 vs 0.482 (XCube L2) (+0.230)；Recall ↑ 0.491 vs 0.230 (XCube L2) (+0.261)；FID ↓ 73.952 vs 94.822 (XCube L2) (-20.870)。

## 概要

现有基于体素（voxel）的3D城市场景表示受限于固定分辨率、内存消耗大、难以编辑且缺乏对象级结构，这直接制约了生成质量和下游交互能力。PrITTI 针对这一瓶颈，提出一种紧凑的混合基元表示——将地面元素栅格化为鸟瞰高度图，同时将物体建模为参数化基元（立方体与椭球体），从而在语义层面实现高质量、可控且可编辑的3D城市场景生成。

核心思路是将城市场景分解为栅格化地面高程图与参数化物体基元，通过解耦的变分自编码器（Layout VAE）嵌入统一的2D潜在空间，再利用 Diffusion Transformer（DiT）学习该空间中的生成分布。这一设计使得模型既能高效生成，又天然支持条件控制（如植被密度）和局部编辑。

在 KITTI-360 数据集上，PrITTI 的生成指标全面超越基于体素的最佳基线 XCube Level 2：Precision 从 0.482 提升至 0.712，Recall 从 0.230 提升至 0.491，FID 从 94.822 降至 73.952，同时推理速度提升约 6 倍（0.58 s vs 3.50 s），内存占用仅为 2.52 MB。消融实验证实，解耦的潜在空间设计对重建质量至关重要——移除 latent split 会导致 AP3D 下降 8.34 点，MSE 上升 0.028——而 Cholesky 参数化在合成实验中展现出优于四元数编码的数值稳定性和可扩展性。

尽管 PrITTI 在生成质量、内存效率和可控性方面取得了显著进展，其当前框架仍限于静态场景和固定语义类别集，细粒度附件（如杆上灯具）的重建精度不足，且外推任务中大片空白区域易产生语义不连贯的补全。这些局限为后续研究指明了开放方向，包括开放词汇场景生成、几何感知约束集成以及动态场景扩展。



### 3D 城市场景生成的需求与挑战

大规模 3D 城市场景生成是自动驾驶仿真、城市规划、虚拟世界构建等领域的核心技术需求。一个理想的生成框架不仅需要产生高质量、多样化的场景布局，还应支持灵活的下游交互——包括可控生成、局部编辑、场景修复与外推，以及向真实感渲染的衔接（见 Figure 1）。然而，现有方法在表示能力、生成质量与交互灵活性之间存在显著张力，难以同时满足上述需求。

### 体素表示的固有瓶颈

当前主流的 3D 城市场景生成方法几乎全部建立在**体素（voxel）表示**之上。代表性工作包括基于三平面自编码器的 **SemCity**、多层级离散扩散模型 **PDD**，以及多层级 VAE-扩散模型 **XCube** 等。这些方法将场景离散化为固定分辨率的占用网格，虽能统一处理几何与语义，却面临三个根本性瓶颈：

1. **内存效率低下**：体素表示的内存占用随分辨率呈立方增长。例如，SemCity 在 256³ 分辨率下单场景平均消耗 8.00 MB，而紧凑的基元表示仅需 2.52 MB（Table 1）。
2. **编辑困难**：体素网格缺乏对象级结构，无法直接对单个物体进行移动、删除或属性修改——任何编辑都需在像素/体素层面重新生成，严重限制了交互式应用。
3. **几何失真**：固定分辨率导致细长结构（如杆状物）和曲面边界出现锯齿状失真，且垂直方向可能发生截断（Figure 3），影响下游视觉质量。

### 对象级表示的研究空白

尽管体素方法在生成指标上不断进步，但其**始终缺乏对象级语义结构**——场景中的车辆、行人、植被等实体被隐式地编码在占用概率中，而非显式地表示为可操作的物体。这一缺失直接导致两个后果：生成质量受限于网格分辨率，且无法实现对象粒度的编辑与控制。

在 3D 物体表示领域，基元（primitive）——如立方体、椭球体——已被证明是高效且可解释的形状抽象方式。然而，**将基元表示引入大规模城市场景生成仍属空白**：尚无工作探索如何在统一框架内同时处理栅格化地面与参数化物体，并在该表示之上构建生成模型。

### 本文的核心动机

针对上述缺口，PrITTI 提出以下核心主张：

- **表示层面**：将城市场景分解为栅格化的 BEV 地面高度图与参数化的物体基元，形成紧凑的混合表示，从根本上解决体素的内存与编辑瓶颈。
- **生成层面**：通过解耦的变分自编码器（Layout VAE）将混合表示嵌入统一的 2D 潜在空间，再利用 Diffusion Transformer（DiT）学习布局分布，实现高质量、可控且可编辑的生成。
- **交互层面**：基于潜在空间的修复与外推操作，使框架天然支持场景编辑、局部修复和滑动窗口式扩展等下游任务。

这一设计将对象级结构显式地注入生成流程，使得“生成一个场景”等价于“生成一组有意义的物体及其空间布局”，从而在生成质量、推理速度和交互灵活性上实现对体素方法的全面超越。



## 核心方法与创新机理

PrITTI 的核心创新在于用一套**混合基元表示**替代了现有方法中占主导地位的体素网格，并围绕该表示构建了**解耦的潜在空间**与**Transformer扩散生成框架**。这一设计直接回应了体素表示的根本性瓶颈：固定分辨率导致的内存爆炸、缺乏对象级结构带来的编辑困难，以及网格离散化造成的几何失真。以下从四个关键维度剖析其相对于基线方法的创新之处。

### 从密集体素到紧凑混合基元的表示跃迁

现有方法（**SemCity**、**PDD**、**XCube**）均采用固定分辨率的体素网格作为场景表示，每个体素存储占用概率或语义标签。这种表示的内存消耗随分辨率立方增长，且缺乏对物体边界的显式建模。PrITTI 将场景解构为两类截然不同的基元：

- **地面元素**：将道路、人行道、植被地面等 5 类语义地面栅格化为 BEV 高度图 $\mathbf{H} \in \mathbb{R}^{H \times W \times 5}$ 和占用掩膜 $\mathbf{B} \in \{0,1\}^{H \times W \times 5}$，保留了地面的连续高度信息。
- **物体元素**：将车辆、建筑、杆状物等 8 类物体建模为参数化基元（立方体或椭球体），每个基元由一个 9 维特征向量 $\mathbf{f}_i \in [0,1]^9$ 描述——前 3 维为中心位置，后 6 维为 **Cholesky 参数化**的联合方向-尺寸表示。

这一转变的直接收益体现在内存效率上：PrITTI 的单场景内存占用仅为 **2.52 MB**，而 SemCity 256³ 体素表示需要 **8.00 MB**（Table 1），压缩比超过 3 倍。更关键的是，基元表示天然支持对象级选择、平移、旋转和删除等编辑操作，这是体素方法难以实现的。

### Cholesky 参数化：数值稳定的物体姿态编码

物体方向与尺寸的编码是基元表示的核心技术挑战。传统方法通常采用四元数表示旋转，但四元数存在符号歧义和归一化约束，在神经网络优化中容易导致梯度不稳定。PrITTI 引入了一种**基于 Cholesky 分解的参数化策略**：

$$\mathbf{S} = \mathbf{L} \mathbf{L}^{\top}$$

将物体的正定散射矩阵 $\mathbf{S}$ 进行 Cholesky 分解，取 6 个下三角非零元素作为连续表示。这一参数化天然保证正定性，无需额外的归一化约束。消融实验（Figure 4）表明，Cholesky 参数化在合成数据上始终优于四元数编码，且随着训练数据量增加，平均 IoU3D 持续提升，而四元数方法出现性能饱和甚至下降——这验证了 Cholesky 参数化具有更好的数据扩展性和数值稳定性。

### 通道解耦的 2D 联合潜在空间

现有体素方法通常将整个场景压缩为单一潜在表示（如 SemCity 的三平面潜在空间），这导致地面和物体的模态特征相互纠缠，不利于扩散模型的学习。PrITTI 的 Layout VAE（LVAE）设计了**分离的编码器-解码器对**：地面分支处理栅格图，物体分支通过 DETR 风格的 Transformer 解码器从潜在网格中预测固定数量的基元参数。

两者的潜在编码在通道维度拼接为联合变量：

$$\mathbf{z}_{\mathcal{L}} = [\mathbf{z}_{\mathcal{G}}; \mathbf{z}_{\mathcal{O}}] \in \mathbb{R}^{h \times w \times 2c}$$

这一**解耦设计**的消融证据极为充分（Table 2）：移除潜在空间分离（w/o latent split）导致 AP3D 从 62.12 骤降至 53.78，MSE 从 0.0075 升至 0.0355，证明分离潜在空间对保留模态特异性特征至关重要。此外，联合训练地面与物体分支相比独立训练提升 AP3D 1.84 点（62.12 vs 60.28），表明跨分支语义对齐有助于上下文感知的物体放置。

### DiT 扩散主干与可控生成

在第二阶段，PrITTI 采用 **Diffusion Transformer（DiT）** 而非传统的 UNet 作为扩散主干网络，并结合 adaLN-Zero 条件机制实现对场景标签 $y$（如植被密度、车辆密度）的可控生成。这一选择使得模型能够通过缩放策略（DiT-B → DiT-L → DiT-XL）系统性地提升生成质量：Precision 从 0.712 提升至 0.807（Table 3），且 DiT-XL 的收益边际表明模型容量已得到充分挖掘。

此外，基于 RePaint 的潜在空间操作策略使 PrITTI 无需微调即可支持场景修复、局部编辑和滑动窗口式外推等下游应用，这在体素方法中需要额外的适配工作。

### 创新总结

PrITTI 的创新并非孤立的算法改进，而是一套**从表示到架构的系统性重构**：混合基元表示降低了内存并赋予编辑能力，Cholesky 参数化提供了数值稳定的物体编码，解耦潜在空间保留了模态特异性，DiT 扩散框架实现了可控高质量生成。这四个 changed slots 相互协同，共同构成了 PrITTI 相对于体素基线的根本性优势。



PrITTI 采用两阶段生成范式，将 3D 语义城市场景的生成问题从高维体素空间迁移到紧凑的混合基元潜在空间。整体 pipeline 由三个核心模块串联构成：**场景表示层**（Sec. 3.1）、**布局变分自编码器 LVAE**（Sec. 3.2）和**潜在扩散模型 DiT**（Sec. 3.3），辅以基于 RePaint 的潜在空间编辑模块支撑下游应用。

### 输入：混合基元场景表示

给定一个 3D 语义布局，PrITTI 将其拆分为两类异构元素并分别参数化：

- **地面元素**：将属于 5 个地面语义类（如道路、人行道、植被等）的多边形沿垂直方向挤出，然后栅格化为 BEV 高度图 $\mathbf{H} \in \mathbb{R}^{H \times W \times 5}$ 和二值占用掩膜 $\mathbf{B} \in \{0,1\}^{H \times W \times 5}$。
- **物体元素**：将车辆、行人、建筑等实例建模为立方体或椭球体基元，每个基元编码为 9 维特征向量 $\mathbf{f}_i \in [0,1]^9$——前 3 维为中心位置，后 6 维为由 Cholesky 分解 $\mathbf{S} = \mathbf{L}\mathbf{L}^{\top}$ 导出的下三角参数，联合表示姿态与尺寸。所有物体特征堆叠为矩阵 $\mathbf{F}$。

完整场景布局的数学表示为 $\mathcal{L} = \{\mathbf{H}, \mathbf{B}, \mathbf{F}\}$。

### 第一阶段：布局 VAE（LVAE）压缩与解耦

LVAE 负责将异构的 3D 布局压缩为统一的 2D 潜在空间，同时保留模态特异性。其设计核心是**双分支解耦架构**：

- **地面编码器 $E_G$** 与**物体编码器 $E_O$** 分别处理栅格化地面图与参数化物体基元。物体编码器通过 scatter-mean 操作将基元特征映射到 2D 潜在网格上，再经 Transformer 编码器建模基元间关系。
- 两分支各自输出潜在变量 $\mathbf{z}_{\mathcal{G}}$ 和 $\mathbf{z}_{\mathcal{O}}$，然后在通道维度拼接为联合潜在变量：
  $$\mathbf{z}_{\mathcal{L}} = [\mathbf{z}_{\mathcal{G}}; \mathbf{z}_{\mathcal{O}}] \in \mathbb{R}^{h \times w \times 2c}$$
- **地面解码器 $D_G$** 与基于 DETR Transformer 的**物体解码器 $D_O$** 从 $\mathbf{z}_{\mathcal{L}}$ 中分别重建高度图、占用掩膜和每类固定数量的基元参数及存在概率。

LVAE 的总训练目标为三个损失项的加权和：
$$\mathcal{L}_{\mathrm{LVAE}} = \mathcal{L}_{\mathrm{ground}} + \mathcal{L}_{\mathrm{object}} + \mathcal{L}_{\mathrm{KL}}$$

消融实验（Table 2）表明，**潜在空间分离**是 LVAE 性能的关键瓶颈：移除 latent split 导致 AP3D 从 62.12 骤降至 53.78，MSE 从 0.0075 升至 0.0355。此外，**联合训练**地面与物体分支相比独立训练提升 AP3D 1.84 点（62.12 vs 60.28），验证了跨分支语义对齐对上下文感知物体放置的重要性。

### 第二阶段：扩散 Transformer（DiT）生成

在冻结的 LVAE 潜在空间之上，PrITTI 训练一个 DiT（Diffusion Transformer）模型学习场景布局的生成分布。DiT 以 adaLN-Zero 机制注入条件信息，支持基于离散类别标签（如植被密度 low/medium/high）的可控生成。训练目标为标准去噪分数匹配损失：
$$\mathcal{L}_{\mathrm{LDM}} = \mathbb{E}_{\mathbf{z}_{\mathcal{L}}^0, \epsilon, t, y} \left[ \| \epsilon - \epsilon_{\theta} ( \sqrt{\bar{\alpha}_t} \mathbf{z}_{\mathcal{L}}^0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, t, y ) \|^2 \right]$$

缩放实验（Table 3）显示，模型容量是生成质量的因果旋钮：从 DiT-B 到 DiT-L，Precision 从 0.712 提升至 0.807；进一步扩大至 DiT-XL 收益边际，表明当前容量已接近瓶颈。

### 下游编辑：潜在空间操作

基于 RePaint 策略，PrITTI 在推理时对联合潜在变量 $\mathbf{z}_{\mathcal{L}}$ 进行掩膜扩散修复，无需微调即可实现场景局部编辑（inpainting）和滑动窗口式扩展（outpainting）。该模块将编辑操作统一在潜在空间完成，再经 LVAE 解码器还原为 3D 基元布局。

### 数据流总览

```
3D 语义布局 (H, B, F)
    │
    ▼
┌──────────────┐     ┌──────────────┐
│  E_G (地面)   │     │  E_O (物体)   │
└──────┬───────┘     └──────┬───────┘
       │ z_G                │ z_O
       └────────┬───────────┘
                ▼
        z_L = [z_G; z_O]   ←── 条件 y
                │
                ▼
        ┌──────────────┐
        │   DiT 扩散    │
        └──────┬───────┘
                │
                ▼
        ┌──────────────┐     ┌──────────────┐
        │  D_G (地面)   │     │  D_O (物体)   │
        └──────┬───────┘     └──────┬───────┘
                │                    │
                ▼                    ▼
          重建 H, B            重建 F (基元参数)
                └────────┬───────────┘
                         ▼
                   3D 基元场景
```

该框架的紧凑性带来显著的资源效率：PrITTI 的单场景内存占用仅 2.52 MB，相比 SemCity（256³ 体素）的 8.00 MB 降低约 3 倍；推理时间 0.58 秒，约为最佳体素基线 XCube L2（3.50 秒）的 1/6（Table 1, Table 3）。

### 补充图表

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/002_Figure_2.jpg]]
*Figure 2: Training Overview. An input 3D semantic layout*



PrITTI 的核心架构由两个阶段构成：第一阶段 Layout VAE (LVAE) 将 3D 语义场景布局压缩为解耦的 2D 潜在编码，第二阶段 Diffusion Transformer (DiT) 在该潜在空间上学习生成分布。以下详述各模块的数学形式与设计机理。

### 3.1 混合基元场景表示

PrITTI 将城市场景分解为地面元素与物体基元两类，形成统一布局表示：

$$
\mathcal{L} = \{\mathbf{H}, \mathbf{B}, \mathbf{F}\}
$$

其中 $\mathbf{H} \in \mathbb{R}^{H \times W \times 5}$ 为 5 类地面语义类的栅格化 BEV 高度图，$\mathbf{B} \in \{0,1\}^{H \times W \times 5}$ 为对应的二值占用掩膜，$\mathbf{F}$ 为物体基元的参数化特征矩阵。每个基元 $i$ 编码为 9 维归一化向量：

$$
\mathbf{f}_i \in [0,1]^9
$$

前 3 维为物体中心位置，后 6 维为 Cholesky 参数。Cholesky 参数化的核心在于将表示物体方向与尺寸的正定散射矩阵 $\mathbf{S}$ 进行 Cholesky 分解：

$$
\mathbf{S} = \mathbf{L} \mathbf{L}^{\top}
$$

取 3×3 下三角矩阵 $\mathbf{L}$ 的 6 个非零元素作为连续参数化。相较于四元数编码，该参数化在合成实验中展现出更高的数值稳定性：随训练数据量增加，平均 IoU3D 持续提升，而四元数方法出现性能饱和甚至下降（见 Figure 4）。

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/006_Figure_4.jpg]]
*Figure 4: Cholesky vs. quaternion encodings across training sizes*

### 3.2 Layout VAE：解耦潜在空间

LVAE 包含地面与物体两条独立编码-解码通路。地面分支采用标准 VAE 架构，将 $\mathbf{H}$ 和 $\mathbf{B}$ 编码为潜在变量 $\mathbf{z}_{\mathcal{G}} \in \mathbb{R}^{h \times w \times c}$（下采样因子 $d=8$，潜在通道维度 $c=32$）。物体分支通过 scatter-mean 操作将基元特征映射到 2D 潜在网格，经 Transformer 编码器建模基元间关系后，得到物体潜在变量 $\mathbf{z}_{\mathcal{O}} \in \mathbb{R}^{h \times w \times c}$。

两路潜在变量在通道维度拼接，形成联合布局潜在变量：

$$
\mathbf{z}_{\mathcal{L}} = [\mathbf{z}_{\mathcal{G}}; \mathbf{z}_{\mathcal{O}}] \in \mathbb{R}^{h \times w \times 2c}
$$

物体解码器基于 DETR Transformer，为每个类别预设固定数量的可学习物体查询，从 $\mathbf{z}_{\mathcal{O}}$ 中预测基元参数及存在概率。

LVAE 的总训练目标由三项损失构成：

$$
\mathcal{L}_{\mathrm{LVAE}} = \mathcal{L}_{\mathrm{ground}} + \mathcal{L}_{\mathrm{object}} + \mathcal{L}_{\mathrm{KL}}
$$

其中 $\mathcal{L}_{\mathrm{ground}}$ 为高度图 MSE 与占用掩膜 BCE 的组合，$\mathcal{L}_{\mathrm{object}}$ 为物体参数的 L1 损失与存在性二元交叉熵，$\mathcal{L}_{\mathrm{KL}}$ 为潜在空间的 KL 正则化项。

**解耦设计的因果作用**：消融实验（Table 2）表明，移除潜在空间分离（w/o latent split）导致 AP3D 从 62.12 骤降至 53.78，MSE 从 0.0075 升至 0.0355。这证明解耦设计对保留地面与物体的模态特异性特征至关重要——地面需要密集的空间精度，物体则需要稀疏的实例级语义，混合编码会引入跨模态干扰。此外，联合训练地面与物体分支相较于独立训练提升 AP3D 1.84 点（62.12 vs 60.28），表明跨分支语义对齐有助于上下文感知的物体放置。

### 3.3 Diffusion Transformer 与条件生成

第二阶段在联合潜在空间上训练潜扩散模型，采用 DiT (Diffusion Transformer) 结合 adaLN-Zero 条件机制。扩散模型以场景标签 $y$（如植被密度、车辆密度）为条件，训练目标为标准去噪分数匹配损失：

$$
\mathcal{L}_{\mathrm{LDM}} = \mathbb{E}_{\mathbf{z}_{\mathcal{L}}^0, \epsilon, t, y} \left[ \| \epsilon - \epsilon_{\theta} ( \sqrt{\bar{\alpha}_t} \mathbf{z}_{\mathcal{L}}^0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, t, y ) \|^2 \right]
$$

其中 $\epsilon_{\theta}$ 为 DiT 预测的噪声，$\bar{\alpha}_t$ 为噪声调度参数。推理时，DiT 可从纯噪声出发，条件于场景标签 $y$ 生成新的潜在编码，再经 LVAE 解码器还原为基元布局。

**模型缩放的收益**：缩放 DiT 模型容量（DiT-B → DiT-L）带来显著的生成质量提升（Precision 从 0.712 升至 0.807），但进一步扩大至 DiT-XL 收益边际，表明当前数据规模下 DiT-L 已接近容量饱和点（Table 3）。

### 3.4 场景编辑与外推

基于 RePaint 启发的潜在空间操作策略，PrITTI 无需微调即可实现场景修复（inpainting）与滑动窗口式外推（outpainting）。修复时，已知区域在扩散反向过程中被强制替换为编码后的已知潜在值，未知区域由扩散模型补全。外推通过逐块生成并利用重叠区域保持语义连贯性，但大范围空白条件区域可能导致补全不连贯或块间明显接缝（见 Figure 12 失败案例）。

### 补充图表

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/014_Figure_8.jpg]]
*Figure 8: Latent-space Scene Outpainting. Given a known layout block P (green) with latent*



## 实验与关键发现

### 核心实验设置

PrITTI 的实验分为两个阶段评估：第一阶段评估布局变分自编码器（LVAE）的重建能力，第二阶段评估潜在扩散模型（DiT）的生成质量。主要实验在 KITTI-360 数据集上进行，该数据集包含大规模城市场景的语义标注。所有生成指标（Precision、Recall、FID、IS）基于统一的评估协议：1000 个最大空间距离参考样本，邻近大小 k=3。推理时间在相同计算环境下测量（单 GPU，batch size 1），确保对比公平。

### 第一阶段：重建质量评估

#### 体素化重建对比

为与基于体素的基线方法公平对比，PrITTI 的重建结果被体素化后计算 IoU 和 mIoU 指标。Table 1 展示了定量对比结果：尽管 PrITTI 原生为基元表示（在体素指标上处于先天劣势），其体素化重建仍保持竞争力——IoU 达 90.58，mIoU 达 70.27，同时单样本平均内存仅 2.52 MB，远低于 SemCity 256³ 的 8.00 MB。

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/003_Table_1.jpg]]
*Table 1: Stage 1: Voxel reconstruction results comparing IoU, mIoU, and mean per-sample memory for voxel-based baselines and voxelized PrITTI. Despite being natively primitive-based (and hence at a disadvantage), PrITTI remains competitive on these metrics. Best , second-best , and third-best results refer to the same (finest) resolution, where native size comparisons are meaningful*

定性对比（Figure 3）揭示了体素方法的固有缺陷：基于体素的重建有时会产生不完整几何和网格诱导的畸变，如高基元处的垂直截断。PrITTI 的基元原生表示天然避免了此类问题。

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/004_Figure_3.jpg]]
*Figure 3: Stage 1: Qualitative reconstruction results on the same test scenes shown in each method’s native representation: primitives for PrITTI and voxel grids for SemCity and XCube. Voxel-based methods sometimes yield incomplete geometry and grid-induced distortions, such as vertical clipping at tall primitives*

#### LVAE 消融实验

Table 2 展示了 LVAE 设计的消融结果，验证了两个关键设计选择：

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/005_Table_2.jpg]]
*Table 2: LVAE ablations for latent split and joint training*

**潜在空间分离（latent split）至关重要。** 移除解耦设计（w/o latent split）导致 AP3D 从 62.12 骤降至 53.78（下降 8.34 点），MSE 从 0.0075 升至 0.0355。这表明地面与物体的模态特异性特征需要独立的潜在通道来保留，混合编码会显著损害重建精度。

**联合训练优于独立训练。** 联合训练地面与物体分支相较独立训练提升 AP3D 1.84 点（62.12 vs 60.28），证明跨分支语义对齐有助于上下文感知的物体放置。联合训练使物体解码器能够利用地面信息推断合理的物体位置。

#### Cholesky 参数化验证

Figure 4 对比了 Cholesky 参数化与四元数编码在不同训练数据量下的表现。Cholesky 方法在合成实验中始终优于四元数编码，且随数据量增加，平均 IoU3D 持续提升，而四元数方法出现性能饱和甚至下降。这验证了 Cholesky 分解作为物体姿态与尺寸连续表示的数值稳定性和数据效率优势。

### 第二阶段：生成质量评估

#### 主结果对比

Table 3 展示了生成结果的主对比。PrITTI（DiT-B）在所有生成指标上均显著优于基于体素的最佳基线 XCube Level 2：

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/008_Table_3.jpg]]
*Table 3: Generation Results. Comparison of PrITTI and baselines across generative metrics and mean generation time per scene*

- **Precision**：0.712 vs 0.482（+0.230）
- **Recall**：0.491 vs 0.230（+0.261）
- **FID**：73.952 vs 94.822（-20.870）
- **IS**：3.856 vs 3.480（+0.376）

同时，PrITTI 的推理速度提升约 6 倍（0.58 s vs 3.50 s）。进一步缩放模型容量至 DiT-L 带来显著提升（Precision 0.807），但 DiT-XL 收益边际，表明模型容量已得到充分挖掘。

定性对比（Figure 5）显示，PrITTI 生成的场景具有更清晰的物体边界和更真实的布局结构，而基线方法（SemCity、PDD、XCube）常出现几何碎片化和语义不一致（Figure 9 展示了基线方法的低质量示例）。PrITTI 还支持植被密度等条件控制，基线方法仅能无条件生成。

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/016_Figure_9.jpg]]
*Figure 9: Low-quality scene generation examples from baseline methods exhibiting fragmented geometry and semantic inconsistencies*

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/007_Figure_5.jpg]]
*Figure 5: 3D Semantic Scene Generation. Comparison of 3D semantic layouts generated by PrITTI (Ours, left) and voxel-based baselines (SemCity, PDD, XCube, right). PrITTI enables controllable generation, here conditioned on vegetation density (low, medium, or high), and produces more realistic, well-shaped scenes with clearer object boundaries. All baseline samples are generated unconditionally*

#### 可控生成

PrITTI 支持基于离散语义标签的条件生成。Figure 5 展示了植被密度（低、中、高）条件下的可控生成效果。Figure 16 和 Figure 17 进一步展示了车辆密度条件及植被-车辆联合密度条件下的可控生成，证明框架对多类基元的条件控制能力。

#### 最近邻分析

Figure 11 的最近邻分析表明，生成样本与训练样本在布局和物体放置上存在显著差异，排除了模型记忆训练数据的可能，验证了生成多样性。

### 跨数据集泛化

Table 9 展示了 PrITTI 在 Argoverse 2 数据集上的评估结果，包括重建和生成指标。模型在非 KITTI-360 环境下仍保持有效性能，表明框架具有一定的泛化能力，但具体指标值需查阅原文表格确认。

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/021_Table_9.jpg]]
*Table 9: PrITTI evaluation results on AV2 [86], showing (a) reconstruction and (b) generation metrics*

### 下游应用评估

PrITTI 支持多种无需微调的下游应用：

- **场景修复**：Figure 24 展示了顶部、底部、右侧、左侧区域的修复结果，编辑区域与周围几何和语义无缝融合。
- **场景外推**：基于滑动窗口式的潜在操作实现场景扩展（Figure 8），但当条件区域存在大片空白时，模型易生成语义不连贯的补全，并可能在块间出现明显接缝。
- **街景合成**：Figure 31 展示了基于 ControlNet 的真实感街景图像合成，基元渲染的粗几何作为控制信号，生成的图像展现出超越立方体/椭球体的多样化物体外观。

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/028_Figure_24.jpg]]
*Figure 24: PrITTI Inpainting Results. Inpainting applied to (a) top, (b) bottom, (c) right, and (d) left regions of an input scene. PrITTI produces localized edits that blend seamlessly with the surrounding geometry and semantics, yielding consistent and plausible completions*

### 失败模式与局限

Figure 12 展示了 PrITTI 的典型失败案例：

1. **细粒度附件重建失败**：杆上灯具等细小附属结构常被错误重建，产生漂浮物体。这源于训练数据中的几何不准确被模型学习并传播。
2. **外推不连贯**：当条件区域存在大片空白时，模型生成语义不连贯的补全，块间出现明显接缝。
3. **物理违规**：框架未显式强制施加硬几何约束，可能产生物体穿透或地面错位等违反物理规律的场景。

此外，框架仅限于静态场景和固定的语义类别集，无法处理训练时未见过的物体类别。地面表示受栅格图分辨率限制，挤出过程可能导致地面表面细节不足。

### 补充图表

![[assets/figures/papers/paper_list_l2575_https_arxiv_org_abs_2506_19117/figures/001_Figure_1.jpg]]
*Figure 1: PrITTI generates (1) high-quality, controllable 3D semantic urban scenes in a compact primitive-based representation using a latent diffusion model. Starting from a generated scene (e.g. middle sample), we demonstrate downstream applications including (2) scene editing, (3) inpainting, (4) outpainting, and (5) photo-realistic street view synthesis*



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

现有基于体素（voxel）的3D城市场景生成方法——如 **SemCity**、**PDD** 和 **XCube**——面临一个根本性瓶颈：固定分辨率的体素网格表示导致内存消耗随分辨率立方增长，难以扩展至大规模场景，且缺乏对象级结构，使得场景编辑、局部修复和语义控制等下游任务难以实现。PrITTI 的因果调控旋钮在于**场景表示的范式转换**：将3D场景分解为栅格化的地面高程图（$\mathbf{H} \in \mathbb{R}^{H \times W \times 5}$）与参数化物体基元（立方体/椭球体），并通过**通道解耦的2D联合潜在空间**将两类模态统一编码，使得潜在扩散模型能够高效生成、编辑和条件控制。

这一设计带来了三重因果收益：① 内存占用从 SemCity 256³ 的 8.00 MB 降至 2.52 MB（Table 1）；② 推理速度从 XCube L2 的 3.50 s 提升至 0.58 s（约6倍加速，Table 3）；③ 生成质量全面超越体素基线，Precision 从 0.482 跃升至 0.712（Table 3）。

### 2. 方法谱系中的关键设计选择

PrITTI 在以下四个关键方法槽位上做出了区别于现有工作的选择：

| 方法槽位 | 基线方法取值 | PrITTI 取值 | 证据锚点 |
|---------|------------|------------|---------|
| 场景表示 | 固定分辨率体素网格（SemCity 三平面、XCube 多层级体素） | 混合基元：栅格化 BEV 高度图 + 参数化物体基元 | Sec. 3.1 |
| 物体编码 | 体素占用概率 | 9D 特征向量（3D 中心 + 6D Cholesky 参数），联合表示方向与尺寸 | Sec. 3.1 |
| 潜在空间结构 | 三平面潜在空间（SemCity）或多层级体素 | 通道解耦的 2D 联合潜在空间，地面与物体特征分离 | Sec. 3.2 |
| 扩散主干网络 | UNet 或特定体素网络 | DiT (Diffusion Transformer) 结合 adaLN-Zero 条件机制 | Sec. 3.3 |

**Cholesky 参数化**（$\mathbf{S} = \mathbf{L} \mathbf{L}^{\top}$，取 $\mathbf{L}$ 的6个非零元素）是物体编码的关键创新。合成实验（Figure 4）表明，Cholesky 参数化在平均 IoU3D 上始终优于四元数编码，且随训练数据量增加性能持续提升，而四元数方法出现饱和甚至下降——这归因于 Cholesky 分解为散射矩阵提供了连续、无歧义的表示，避免了四元数在方向空间中的不连续性问题。

**解耦潜在空间**的设计在消融实验中得到强力验证（Table 2）：移除潜在空间分离（w/o latent split）导致 AP3D 从 62.12 降至 53.78（下降 8.34 点），MSE 从 0.0075 升至 0.0355，证明分离设计对保留地面与物体的模态特异性特征至关重要。此外，联合训练地面与物体分支相较于独立训练提升 AP3D 1.84 点（62.12 vs 60.28），表明跨分支语义对齐有助于上下文感知的物体放置。

### 3. 与基线方法的系统性对比

PrITTI 在 KITTI-360 数据集上与三类体素基线方法进行了全面对比：

- **SemCity**：基于三平面自编码器与扩散模型，在体素重建上表现较强（IoU 90.58），但生成质量受限于三平面表示的几何保真度。
- **PDD**：多层级离散扩散模型，在生成多样性上具有一定优势，但体素离散化导致几何碎片化（Figure 9 展示的失败案例）。
- **XCube**：多层级 VAE-扩散模型，是体素方法中生成质量最强的基线，但其层级结构导致推理速度较慢（3.50 s）。

在生成指标上，PrITTI DiT-B 以 Precision 0.712、Recall 0.491、FID 73.952、IS 3.856 全面超越 XCube L2（Precision 0.482、Recall 0.230、FID 94.822、IS 3.480），且推理时间仅 0.58 s（Table 3）。缩放 DiT 模型至 DiT-L 进一步将 Precision 提升至 0.807，但扩大至 DiT-XL 收益边际，表明模型容量已得到充分挖掘。

值得注意的是，PrITTI 在体素化后的重建评估中仍保持竞争力（Table 1，IoU 90.58、mIoU 70.27），尽管其原生基元表示在体素指标上存在先天劣势——这进一步验证了混合基元表示的表达能力。

### 4. 适用边界与局限

PrITTI 的适用边界由以下设计约束划定：

1. **静态场景限定**：框架仅处理静态场景，使用粗粒度的3D基元表示物体，缺乏精细几何细节。细粒度附件（如杆上灯具）难以精确重建，可能产生漂浮物体（Figure 12a）。
2. **封闭类别集**：模型仅能处理固定的语义类别集（Table 4 定义的物体类别与语义类映射），无法生成训练时未见过的物体类别。
3. **地面分辨率限制**：地面表示受栅格图分辨率（256×256）限制，挤出过程可能导致地面表面细节不足。
4. **外推不稳定性**：外推任务中，当条件区域存在大片空白时，模型易生成语义不连贯的补全，并可能在块间出现明显接缝（Figure 12b）。
5. **缺乏物理约束**：未显式强制施加硬几何约束，可能产生物体穿透或地面错位等违反物理规律的场景。

### 5. 开放问题与未来方向

1. **开放词汇场景生成**：如何将框架扩展至开放词汇场景生成，以处理任意语义类别，是向通用场景生成器演进的关键挑战。
2. **几何约束集成**：能否在扩散过程中集成软约束或几何感知引导，以减少物理违规和提高布局合理性？物理仿真与扩散模型的结合是值得探索的方向。
3. **细粒度重建**：如何提升对细小附属结构和密集排列小物体（如栅栏）的重建精度？可能需要引入多尺度基元或自适应基元密度。
4. **动态场景扩展**：基元表示能否适应动态场景（如移动车辆、行人）的时间维度？引入时序基元参数化是潜在路径。
5. **跨域泛化**：该框架能否在室内场景、Argoverse 2 等非 KITTI-360 环境下有效推广？初步实验（Table 9）显示 PrITTI 在 Argoverse 2 上具有可行性，但需更系统的跨域评估。
6. **基元穿透预防**：如何进一步优化以防止基元间穿透和地面错位等常见失败模式？显式碰撞检测或基于物理的损失函数可能是解决方案。



## 原文 PDF

![[paperPDFs/CVPR_2026/PrITTI_Primitive_based_Generation_of_Controllable_and_Editable_3D_Semantic_Urban_Scenes.pdf]]
