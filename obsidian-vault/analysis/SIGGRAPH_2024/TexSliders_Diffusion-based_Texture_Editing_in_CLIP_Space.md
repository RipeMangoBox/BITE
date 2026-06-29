---
title: "TexSliders: Diffusion-based Texture Editing in CLIP Space"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/TexSliders_Diffusion_based_Texture_Editing_in_CLIP_Space.pdf
project_link: null
code_link: null
aliases:
- TexSliders
tags:
- SIGGRAPH_2024
- topic/graphics_rendering_materials
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 在CLIP图像嵌入空间中定义编辑方向，并通过维度选择（仅保留编辑属性相关维度，抑制身份变化维度）来控制纹理属性的独立编辑，同时保持身份。
primary_logic: 利用纹理扩散先验从一对文本提示（如“metal”→“rusty metal”）采样多个CLIP图像嵌入，形成源与目标两个聚类；取聚类中心差作为初始编辑方向，再选择簇间距离大于簇内标准差的维度作为最终编辑方向，从而去除噪声维度，实现编辑效果与身份保持的平衡。
claims:
- 交叉注意力图不适用于纹理编辑，因为纹理缺乏清晰的物体分离，导致以往方法性能下降。
- 在文本和图像条件之间，图像条件（CLIP图像嵌入）能更好地保持纹理身份。
- 维度筛选后的编辑方向在CLIP-Direction和CLIP-Im2Im上均显著优于现有方法。
- 消融实验证明维度选择是身份保持的关键：全维度或单样本嵌入均导致身份偏移。
---

# TexSliders: Diffusion-based Texture Editing in CLIP Space

> [!tip] 核心洞察
> 利用纹理扩散先验从一对文本提示（如“metal”→“rusty metal”）采样多个CLIP图像嵌入，形成源与目标两个聚类；取聚类中心差作为初始编辑方向，再选择簇间距离大于簇内标准差的维度作为最终编辑方向，从而去除噪声维度，实现编辑效果与身份保持的平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | TexSliders: 基于扩散模型的CLIP空间纹理编辑 |
| 英文题名 | TexSliders: Diffusion-based Texture Editing in CLIP Space |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://graphics.unizar.es/projects/TexSliders/) |
| Topic | #topic/graphics_rendering_materials #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | TexSliders |
| Dataset | Test dataset |

> [!tip] 效果简介
> - Test dataset (80 images: 66 generated + 14 real photographs) 上，↑ CLIP-Direction (编辑方向一致性) 0.1063 vs 0.0880 (P2P) / 0.0811 (Pix2pix-zero) / 0.0706 (SDEdit 0.5) (最高提升~50%)；↑ CLIP-Im2Im (身份保持) 0.9303 vs 0.9033 (P2P) / 0.8667 (Pix2pix-zero) / 0.8753 (SDEdit 0.5) (最高提升~7%)。

## 概要

现有基于扩散模型的图像编辑方法（如 Prompt-to-Prompt、Pix2Pix-zero）依赖交叉注意力图保持结构，但纹理图像缺乏清晰的语义边界，导致编辑时无法维持纹理身份。本文提出 **TexSliders**，在 CLIP 图像嵌入空间中定义编辑方向，并通过维度筛选实现纹理属性的独立操控。方法利用在纹理数据集上训练的扩散先验，将文本提示映射为 CLIP 图像嵌入，采样多个嵌入形成源与目标聚类，以聚类中心差作为初始编辑方向，再保留簇间距离显著大于簇内标准差的维度，抑制身份噪声。最终以图像条件潜扩散模型生成可平铺的编辑纹理。实验表明，TexSliders 在 CLIP-Direction（0.1063 vs. P2P 0.0880）和 CLIP-Im2Im（0.9303 vs. P2P 0.9033）上均显著优于现有方法，消融实验证实维度筛选是身份保持的关键。方法定位为基于 CLIP 图像嵌入空间的纹理域扩散编辑，无需优化，仅需一对文本提示即可定义编辑滑块。

## 核心方法与创新机理

### 问题瓶颈：交叉注意力在纹理编辑中的结构性失效

现有基于扩散模型的图像编辑方法（如 **Prompt-to-Prompt**，Hertz et al., ICLR 2023；**Pix2Pix-zero**，Parmar et al., SIGGRAPH 2023）的核心机制是操纵交叉注意力图来保持图像结构。然而，这一机制在纹理编辑场景中系统性失效。其根本原因在于：交叉注意力图依赖语义对象边界来捕获结构信息，而纹理图像（如石块、木纹、锈蚀金属）缺乏清晰的物体分离与语义边界——交叉注意力图无法形成有意义的空间结构表征（Figure 2）。这导致直接迁移此类方法时，编辑后的纹理无法保持原始纹理的“身份”（identity），即纹理的视觉特征、排列方式和整体风格在编辑过程中发生不可控的偏移。

### 核心洞察：从文本条件转向图像条件，在 CLIP 嵌入空间中定义编辑

TexSliders 的核心洞察有两点。第一，纹理身份在图像嵌入空间中比在文本嵌入空间中更容易保持。如图 3 所示，文本条件（Stable Diffusion 的文本编码）映射到外观空间的一个较大区域，同一文本提示可生成多种视觉身份差异显著的纹理；而图像条件（CLIP 图像嵌入）将生成结果约束到更具体的外观邻域，从而天然地抑制身份漂移。第二，编辑操作可以在 CLIP 图像嵌入空间中定义为一个方向向量——沿该方向移动嵌入，即可控制纹理属性的变化程度。

基于这两点洞察，TexSliders 将编辑问题转化为：给定一对描述编辑属性的文本提示（如“metal”→“rusty metal”），在 CLIP 图像嵌入空间中寻找一个编辑方向 **d**，使得沿该方向移动输入纹理的嵌入时，能够独立地改变目标属性（锈蚀程度）而不改变纹理身份（金属的排列结构）。

### Changed Slots：三个关键机制替换

与现有方法相比，TexSliders 在三个关键机制上进行了替换：

| 机制槽位 | 基线方法 | TexSliders 方案 |
|---------|---------|----------------|
| **编辑机制** | 操纵交叉注意力图（P2P, Pix2Pix-zero） | 在 CLIP 图像嵌入空间中定义编辑方向并进行维度筛选 |
| **扩散条件类型** | 文本条件（Stable Diffusion 文本编码） | 图像条件（通过纹理扩散先验生成的 CLIP 图像嵌入） |
| **领域适配** | 无特定领域先验（通用扩散模型） | 使用在纹理数据集上训练的扩散先验，约束生成到纹理域 |

### 方法框架与模块顺序

TexSliders 由三个核心模块级联构成，其推理流程如下：

**模块一：纹理扩散先验 P（Text → CLIP Image Embedding）**

该模块是一个在纹理数据集上训练的扩散先验模型，负责将文本提示转换为 CLIP 图像嵌入。其作用是将文本语义映射到纹理域的 CLIP 图像嵌入子空间，从而约束后续生成始终位于纹理流形上。给定一对文本提示（原始描述 $p_o$ 和目标描述 $p_t$），先验 P 分别生成对应的 CLIP 图像嵌入。

**模块二：编辑方向计算与维度筛选（Embedding → Direction d）**

这是 TexSliders 的核心创新模块，分为三个子步骤：

1. **聚类采样**：对原始提示 $p_o$ 和目标提示 $p_t$，分别通过先验 P 采样 $n_e$ 个 CLIP 图像嵌入（论文中 $n_e=150$），形成原始嵌入聚类 $\{\mathbf{o}^{(i)}\}_{i=1}^{n_e}$ 和目标嵌入聚类 $\{\mathbf{t}^{(k)}\}_{k=1}^{n_e}$。

2. **初始方向计算**：取两个聚类中心的差作为初始编辑方向 $\mathbf{d}' \in \mathbb{R}^{768}$，其第 $j$ 个分量为：

   $$d_{j}^{\prime} = \frac{1}{n_{e}} \left(\sum_{k} t_{j}^{(k)} - \sum_{i} o_{j}^{(i)}\right) \tag{1}$$

   该方向表示从原始纹理属性到目标纹理属性的平均语义位移。

3. **维度筛选**：初始方向 $\mathbf{d}'$ 的 768 个维度并非全部与目标编辑属性相关——许多维度编码的是身份信息或随机噪声。TexSliders 通过簇间距离与簇内标准差的比较来筛选相关维度。具体而言，对每个维度 $j$，先对嵌入进行标准化得到 $\tilde{\mathbf{o}}^{(i)}$ 和 $\tilde{\mathbf{t}}^{(k)}$，然后保留满足以下条件的维度分量：

   $$d_{j} = \begin{cases} d_{j}^{\prime}, & \text{if } |\tilde{d}_{j}^{\prime}| > \tau \cdot \text{std}(\tilde{t}_{j}^{(k)}) \text{ and } |\tilde{d}_{j}^{\prime}| > \tau \cdot \text{std}(\tilde{o}_{j}^{(i)}) \\ 0, & \text{otherwise.} \end{cases} \tag{2}$$

   其中 $\tau$ 为阈值（通常取 0.8）。该筛选的逻辑是：如果某维度上两个聚类中心的标准化距离同时大于各自聚类内部的标准化标准差，则该维度携带的是类别间差异信号（编辑属性），而非类别内波动（身份变化或噪声）；否则将该维度置零，从编辑方向中剔除。

**模块三：图像条件潜扩散模型 D（Edited Embedding → Texture Image）**

给定输入纹理的 CLIP 图像嵌入 $\mathbf{e}_0$，沿筛选后的编辑方向 $\mathbf{d}$ 移动 $\alpha$ 步长，得到编辑后的嵌入：

$$\mathbf{e}_{\alpha} = \mathbf{e}_{0} + \alpha \cdot \mathbf{d} \tag{3}$$

其中 $\alpha$ 为可调参数：$\alpha > 0$ 向目标属性方向编辑，$\alpha < 0$ 向反方向编辑，$|\alpha| > 1$ 实现外推。该嵌入作为条件输入到预训练的图像条件潜扩散模型 D 中，生成最终的、可平铺的纹理图像。

### 模块间因果关系

三个模块形成严格的因果链：**先验 P 提供领域约束**（确保生成停留在纹理流形上）→ **维度筛选提供属性解耦**（从高维嵌入中分离编辑信号与身份信号）→ **扩散模型 D 提供生成能力**（将编辑后的嵌入解码为像素级纹理）。其中，维度筛选是整个方法有效性的关键因果节点：消融实验（Figure 6）表明，若跳过维度筛选直接使用全 768 维的 $\mathbf{d}'$，编辑结果会出现明显的身份偏移；若仅使用单个嵌入对（$n_e=1$）计算方向，由于无法区分属性变化与采样噪声，同样导致身份保持失败。

![[assets/figures/papers/paper_list_l38_https_graphics_unizar_es_projects_TexSliders/figures/006_Figure_6.jpg]]
*Figure 6: Ablation study. We show qualitative ablations for the direction “metal” to “rusty metal” (positive and negative). We compare to using a single image embedding for original and target prompts*

### 推理与训练路径

- **推理阶段**：用户提供一对文本提示和一张输入纹理图像 → 先验 P 采样 $n_e$ 个嵌入并计算编辑方向 $\mathbf{d}$（约 2 分钟，单张 A10G GPU）→ 将输入纹理的 CLIP 嵌入沿 $\mathbf{d}$ 移动 → 扩散模型 D 生成编辑结果。整个过程无需优化或微调。
- **训练阶段**：扩散先验 P 和图像条件扩散模型 D 均为预训练模型，TexSliders 不引入额外训练。先验 P 在纹理数据集上训练以适配纹理域。

![[assets/figures/papers/paper_list_l38_https_graphics_unizar_es_projects_TexSliders/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our diffusion-based texture editing approach. Top row: Our approach leverages a diffusion prior model*

## 实验与关键发现

### 定量评估：编辑方向一致性与身份保持

TexSliders 在包含 80 张纹理图像（66 张生成纹理 + 14 张真实照片）的测试集上，与三类基于扩散模型的图像编辑方法进行了系统对比：**Prompt-to-Prompt**（P2P, Hertz et al., ICLR 2023）、**Pix2Pix-zero**（Parmar et al., SIGGRAPH 2023）和 **SDEdit**（Meng et al., ICLR 2022，噪声水平 0.5 和 0.75）。所有方法统一使用 50 步扩散采样和无分类器引导系数 7.5；对基于 Stable Diffusion 的方法，提示均添加前缀“a texture of…”以约束生成子空间。

定量评估采用两个互补指标：**CLIP-Direction** 衡量编辑结果与目标编辑方向的一致性（即编辑是否按预期执行），**CLIP-Im2Im** 衡量编辑结果与输入纹理的身份相似度（即纹理身份是否得以保持）。Table 1 报告了测试集上的均值结果。

![[assets/figures/papers/paper_list_l38_https_graphics_unizar_es_projects_TexSliders/figures/007_Table_1.jpg]]
*Table 1: Quantitative metrics (mean values on our full test dataset, including generated images and photographs). Our approach’s results better match the required edit direction (CLIP-Direction) than previous work, while also better preserving the identity of the input texture (CLIP-Im2Im)*

| 方法 | ↑ CLIP-Direction | ↑ CLIP-Im2Im |
|------|:------:|:------:|
| SDEdit (0.5) | 0.0706 | 0.8753 |
| SDEdit (0.75) | 0.0601 | 0.8659 |
| Pix2Pix-zero | 0.0811 | 0.8667 |
| Prompt-to-Prompt | 0.0880 | 0.9033 |
| **TexSliders (Ours)** | **0.1063** | **0.9303** |

在 CLIP-Direction 上，TexSliders 达到 0.1063，较最优基线 P2P（0.0880）提升约 20.7%，较 Pix2Pix-zero（0.0811）提升约 31.1%。在 CLIP-Im2Im 上，TexSliders 达到 0.9303，较 P2P（0.9033）提升约 3.0%，较 Pix2Pix-zero（0.8667）提升约 7.3%。两个指标的同时领先表明，TexSliders 并非通过牺牲编辑强度来换取身份保持，而是实现了二者的更好平衡。

### 消融实验：维度筛选是身份保持的因果关键

为验证编辑方向计算中两个核心设计选择——**多采样嵌入聚类**和**维度筛选**——的因果作用，论文围绕编辑方向“metal”→“rusty metal”进行了定性消融（Figure 6）。

- **单样本嵌入（n_e=1）**：仅使用原始提示和目标提示各一个 CLIP 图像嵌入计算编辑方向。此时编辑方向完全由两个单点决定，无法解耦属性变化与身份变化，导致沿方向移动时纹理身份发生明显偏移（Figure 6 上行）。
- **全维度方向 d'（768维）**：使用多个嵌入（n_e=150）计算初始方向 d'，但不进行维度筛选，保留所有 768 个分量。尽管多采样降低了部分噪声，但 d' 仍包含大量与目标编辑无关的身份相关维度，编辑结果的身份保持不理想（Figure 6 中行）。
- **维度筛选后的方向 d**：在 d' 基础上，仅保留那些簇间标准化距离同时超过目标簇和原始簇标准化标准差 τ 倍（τ=0.8）的维度。筛选后的方向在实现“rusty metal”正向编辑和“clean metal”反向编辑的同时，良好地保持了输入纹理的原始结构（Figure 6 下行）。

这一消融链条建立了清晰的因果路径：多采样嵌入聚类提供了统计稳健的初始方向估计，而维度筛选通过抑制身份相关噪声维度，是实现身份保持编辑的**决定性机制**。缺失任一环节均会导致身份偏移。

### 定性对比：身份保持与编辑真实感

Figure 8 展示了 TexSliders 与 P2P、Pix2Pix-zero、SDEdit 在多种材质和编辑方向上的定性对比。在“small stones”→“big stones”、“metal”→“rusty metal”、“bricks”→“mossy bricks”等编辑任务中，基线方法普遍存在两类失败模式：

1. **编辑不充分**：P2P 和 Pix2Pix-zero 依赖交叉注意力图保持结构，但纹理缺乏清晰的语义边界，导致编辑效果微弱或未按预期方向变化。
2. **身份丢失**：SDEdit 通过加噪-去噪实现编辑，但噪声注入破坏了纹理的细粒度结构，生成结果与输入纹理的身份一致性差。

相比之下，TexSliders 在 CLIP 图像嵌入空间中操作，通过维度筛选后的编辑方向直接条件扩散生成，既实现了语义上可信的编辑效果，又保持了输入纹理的铺贴结构和材质特征。

### 泛化性与多维度编辑

实验进一步验证了编辑方向的跨材质泛化能力（Figure 9 左）：在砖块纹理上计算的“aged”→“new”编辑方向，可直接应用于木材纹理，产生合理的老化到翻新过渡，表明编辑方向捕获的是材质无关的语义属性。

多维度编辑方面（Figure 9 右），将“small stones”→“big stones”和“→mossy stones”两个独立编辑方向组合，可同时控制石子大小和苔藓程度两个属性维度，生成“big, mossy stones”的组合编辑结果。这验证了 CLIP 图像嵌入空间中编辑方向的线性可加性。

### 真实照片纹理编辑

TexSliders 不仅适用于生成纹理，也可用于真实拍摄的纹理照片（Figure 7）。处理流程为：先使用扩散模型基于输入照片的 CLIP 嵌入重建纹理，再对重建纹理应用编辑方向。实验在多种真实材质（如鹅卵石、木纹）上验证了该流程的有效性，表明方法对非合成纹理同样适用。

![[assets/figures/papers/paper_list_l38_https_graphics_unizar_es_projects_TexSliders/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative results. We show our method on different kinds of materials for various editing directions. We can see that our method applies convincing editing, including when extrapolating the directions (two leftmost columns and rightmost column), and preserves well the texture identity. Here we use generated input textures; Figure 7 and the Supplemental Material provide results also on photographed inputs*

![[assets/figures/papers/paper_list_l38_https_graphics_unizar_es_projects_TexSliders/figures/008_Figure_7.jpg]]
*Figure 7: Photographed texture edits. We use the CLIP embedding of the input texture to reconstruct the photograph using the diffusion model, and apply our editing approach to the reconstructed texture (highlighted in grey), showing that our approach can be used for non-synthetic textures as well*

### 失败模式与适用边界

论文通过 Figure 10 系统展示了三类典型失败模式，定义了方法的当前边界：

1. **CLIP 与扩散模型的语义偏置**：CLIP 嵌入空间和扩散模型本身带有概念偏置，例如对垂直方向图案的偏好。当编辑方向涉及与偏置冲突的语义变换（如“垂直”转“水平”图案）时，编辑可能失败（Figure 10 上行）。
2. **编辑方向的残留身份噪声**：即使经过维度筛选，编辑方向仍可能包含少量与身份相关的噪声分量。在某些纹理上，这会导致编辑后纹理的细粒度结构（如鹅卵石的排列方式）发生非预期的改变（Figure 10 中行）。
3. **外推超出分布边界**：沿编辑方向外推过大（α 远大于 1.0 或远小于 0.0）时，编辑后的 CLIP 嵌入可能超出训练时采样的嵌入分布范围，导致扩散模型生成的纹理身份不可保持（Figure 10 下行）。这表明编辑方向仅在采样分布支撑集内有效。
4. **领域限制**：当前方法仅适用于颜色纹理（albedo textures），扩展到材质贴图（如法线、粗糙度）受限于材质扩散模型的训练数据量。
5. **身份定义的模糊性**：纹理“身份”缺乏形式化定义，评估依赖定性判断和 CLIP-Im2Im 指标，但该指标本身也有局限性，无法完全捕获人类对纹理身份保持的感知。

![[assets/figures/papers/paper_list_l38_https_graphics_unizar_es_projects_TexSliders/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of cross-attention maps. We show maps at the last diffusion step of SD 1.4 [Rombach et al. 2022], given two different input prompts. Top: “a cute panda eating pizza” (non-texture). Bottom: “a texture of small stones” (texture). The attention maps contain interesting semantic information for the panda image, but fail to capture the texture structure*

## 定位与知识库关联

TexSliders 的核心定位在于：**将扩散模型的纹理编辑从“文本-交叉注意力”范式迁移到“CLIP图像嵌入空间的方向操控”范式**。这一迁移的本质是改变了编辑机制这一关键 slot——现有方法（如 **Prompt-to-Prompt** (Hertz et al., ICLR 2023)、**Pix2Pix-zero** (Parmar et al., SIGGRAPH 2023)）依赖操纵交叉注意力图来保持图像结构并实现编辑，但交叉注意力图的有效性建立在图像中存在清晰的语义物体边界这一前提之上。纹理图像恰恰缺乏这种语义分离（Figure 2 提供了直接证据：对“a texture of small stones”，交叉注意力图无法捕获纹理结构），导致这些方法在纹理编辑任务上性能退化。

TexSliders 将这一 slot 替换为：**在CLIP图像嵌入空间中定义编辑方向，并通过维度筛选来解耦属性编辑与身份保持**。这使得编辑不再依赖于扩散模型内部的注意力机制，而是通过对齐文本提示与图像嵌入的统计结构来实现可控编辑。这一改变同时触发了另外两个 slot 的联动变化：扩散条件类型从文本条件变为图像条件（利用在纹理数据集上训练的扩散先验将文本映射为CLIP图像嵌入），以及领域适配从通用扩散模型变为纹理域约束的先验模型。这三个 slot 的协同改变构成了方法的核心差异。

### 知识库挂载点

TexSliders 可挂载到以下知识节点：

1. **CLIP空间的语义方向发现**：该方法延续了在CLIP嵌入空间中寻找可解释语义方向的研究传统（如StyleCLIP等），但将其从人脸/物体编辑扩展到纹理域，并引入了基于聚类统计量的维度筛选策略。关键创新在于：不是简单地取两个文本嵌入的差值作为方向，而是通过纹理扩散先验采样多个图像嵌入形成簇，利用簇间距离与簇内标准差的比值来筛选真正与编辑属性相关的维度（公式2），从而抑制身份噪声。

2. **扩散先验用于域约束**：该方法使用在纹理数据集上训练的扩散先验模型（而非微调整个扩散模型），将文本嵌入映射到纹理域的CLIP图像嵌入空间。这一设计既约束了生成结果保持在纹理域内，又避免了微调带来的过拟合和计算开销。这与利用扩散先验进行图像生成（如DALL·E 2）的思路一致，但将其应用于编辑方向的定义。

3. **图像条件扩散生成**：方法的下游使用图像条件潜扩散模型（基于Aggarwal et al., 2023）进行纹理生成。与文本条件相比，图像条件能将生成结果约束到更特定的外观子空间（Figure 3提供了定性证据：文本条件即使使用特定提示，仍映射到较大的外观区域，产生多样的视觉身份；而图像条件映射到更特定的外观），这是身份保持的关键机制之一。

### 适用边界与局限性

- **纹理类型限制**：当前方法仅适用于颜色纹理（albedo textures），尚未扩展到材质贴图（如法线、粗糙度等），主要受限于材质扩散模型的训练数据量。
- **CLIP与扩散模型的偏置**：方法继承了CLIP和扩散模型中存在的概念偏置（如对垂直方向图案的偏好），可能导致某些编辑失败（Figure 10 top）。
- **身份保持的非完美性**：即使在维度筛选后，编辑方向仍可能残留噪声，导致输入纹理的身份发生改变（如鹅卵石的排列方式改变，Figure 10 middle）。
- **外推边界**：沿编辑方向外推过大时，嵌入可能超出已采样的CLIP分布范围，导致身份不可保持（Figure 10 bottom）。
- **身份定义的模糊性**：纹理“身份”缺乏正式定义，仅依靠定性评估和CLIP-Im2Im指标，难以量化和保证。

### 后续启发

1. **编辑方向的优化学习**：当前的维度筛选基于简单的统计阈值（τ倍标准差），可探索更精细的子空间学习方法（如通过优化或学习来选择编辑相关维度），进一步抑制身份噪声。
2. **扩展到材质贴图**：若能解决材质扩散模型的训练数据稀缺问题，该方法框架可扩展到法线、粗糙度等材质贴图的编辑，这对材质创作管线具有直接价值。
3. **纹理身份的正式化**：如何形式化地定义纹理的“身份”是一个开放问题，这可能需要结合纹理的统计特征（如Gram矩阵、自相似性等）或感知度量，从而为扩散模型中的身份保持提供更可靠的理论基础。
4. **CLIP图像嵌入空间的几何理解**：深入理解纹理图像嵌入在CLIP空间中的流形结构（如局部线性性、曲率等），可能进一步提升编辑方向的精度和泛化能力。
5. **艺术家界面集成**：将该方法集成到完整的艺术家界面后，艺术家在可用性和功能上的反馈将驱动方法向更实用的方向演进，例如多方向组合编辑的交互范式、滑块灵敏度的自适应调整等。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/TexSliders_Diffusion_based_Texture_Editing_in_CLIP_Space.pdf]]