---
title: "SKED: Sketch-guided Text-based 3D Editing"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/SKED_Sketch_guided_Text_based_3D_Editing.pdf
project_link: https://sked-paper.github.io/
code_link: null
aliases:
- SKED
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入多视图草图作为空间约束，并通过保真损失（preservation loss）和草图填充损失（silhouette loss）调节扩散模型对NeRF的编辑过程。"
primary_logic: "将复杂的草图引导3D编辑分解为两个子任务：基于多视图几何推理的粗编辑区域确定，以及基于预训练扩散模型语义知识的精细编辑，再通过距离感知的保真损失和草图对齐损失协同优化。"
claims:
- "SKED在PSNR上显著优于仅文本的基线（Mean 27.53 vs 16.65），证明了草图引导的保真性。"
- "SKED的草图填充率（IoS）达到0.8220，而移除草图损失后降至0.0211，验证了草图对齐损失的必要性。"
- "SKED在CLIP相似度上与仅文本方法接近（0.2739 vs 0.2806），在不牺牲语义对齐的同时保证了局部编辑。"
- "五个代表性样本 (Cat+chef hat, Cupcake+candle, Horse+horn, Sundae+cherry, Plant+flower) 上 PSNR (保真度) ↑ = 27.53 (平均)"
---

# SKED: Sketch-guided Text-based 3D Editing

> [!tip] 核心洞察
> 将复杂的草图引导3D编辑分解为两个子任务：基于多视图几何推理的粗编辑区域确定，以及基于预训练扩散模型语义知识的精细编辑，再通过距离感知的保真损失和草图对齐损失协同优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SKED：基于草图的文本引导3D编辑 |
| 英文题名 | SKED: Sketch-guided Text-based 3D Editing |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2303.10735v3) · [Project](https://sked-paper.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SKED |
| Dataset | 五个代表性样本 (Cat+chef hat, Cupcake+candle, Horse+horn, Sundae+cherry, Plant+flower), 同上五个样本 |

> [!tip] 效果简介
> - 五个代表性样本 (Cat+chef hat, Cupcake+candle, Horse+horn, Sundae+cherry, Plant+flower) 上，PSNR (保真度) ↑ 为 27.53 (平均)，对比 16.65 (平均, Text-Only)，变化 +10.88。
> - 同上五个样本 上，Intersection-over-Sketch (IoS) ↑ 为 0.8220 (平均)，对比 0.0211 (SKED no-silh 变体)，变化 +0.8009。
> - 同上五个样本 上，CLIP-similarity ↑ 为 0.2739 (平均)，对比 0.2806 (平均, Text-Only)，变化 -0.0067。

## 概要

**核心瓶颈**：现有的文本到3D编辑方法仅依赖文本提示，难以实现精确的局部控制——用户无法通过简单的语言界面指定编辑的空间范围、形状和边界。文本语义虽然能指导“编辑什么”，却无法约束“在哪里编辑”这一关键几何维度。

**核心思路**：SKED 将复杂的草图引导3D编辑分解为两个协同子任务——其一，基于多视图几何推理，从至少两个视角的用户草图中确定粗粒度的3D编辑区域；其二，利用预训练文本到图像扩散模型的语义知识，通过 Score Distillation Sampling (SDS) 生成符合文本提示的精细细节。两个子任务通过**距离感知的保真损失**（preservation loss）和**草图填充损失**（silhouette loss）协同优化，前者根据3D点到草图区域的距离动态调节对原始NeRF密度和颜色的约束强度，后者最大化渲染对象掩码在草图区域内的覆盖。

**主要结果**：在五个代表性样本（猫+厨师帽、杯蛋糕+蜡烛、马+角、圣代+樱桃、植物+花）上的定量实验表明：
- **保真度**：SKED 的 PSNR 均值达 27.53，而纯文本基线（DreamFusion Text-Only）仅为 16.65（Table 1），提升 10.88 dB，证明草图引导在保持基模型结构方面的决定性作用。
- **草图对齐**：SKED 的草图填充率（Intersection-over-Sketch, IoS）达 0.8220，移除草图损失后骤降至 0.0211（Table 2），验证了草图对齐损失的必要性。
- **语义保持**：SKED 的 CLIP 相似度为 0.2739，与纯文本基线（0.2806）接近（Table 3），表明在不牺牲语义对齐的前提下实现了局部化编辑。

**方法定位**：SKED 作用于已重建或生成的 NeRF 模型，以文本提示和至少两个视角的草图掩码为输入，在 DreamFusion 框架基础上引入两个新损失函数（保真损失与草图填充损失），并辅以稀疏性损失和占用网格预热策略，属于**基于草图的文本引导3D编辑**这一新兴范式。相较于仅文本的编辑基线，SKED 首次将多视图草图作为空间约束引入扩散模型驱动的NeRF编辑流程，填补了文本提示在局部控制上的空白。

3D内容的创建与编辑一直是计算机图形学与视觉领域的核心挑战。传统的3D建模管线依赖专业软件与大量人工操作，成本高昂且难以普及。近年来，基于神经辐射场（NeRF）的3D重建与生成技术取得了突破性进展，尤其是以DreamFusion为代表的文本到3D方法，使得用户仅通过自然语言提示即可生成完整的3D场景。这一范式极大地降低了3D内容创作的门槛。

然而，当任务从“从零生成”转向“对已有3D模型进行局部编辑”时，现有方法暴露出一个关键瓶颈：**仅靠文本提示难以实现精确的局部控制**。文本描述天然是全局性和语义性的，用户无法通过简单的语言界面指定编辑的空间范围、边界形状和精确位置。例如，用户希望“给这只猫戴上一顶厨师帽”，仅靠文本提示的方法（如DreamFusion的Score Distillation Sampling优化）往往会不可控地改变整个NeRF模型的结构，导致原始场景中不需要修改的部分也发生扭曲或退化。定量实验印证了这一缺陷：在五个代表性样本上，仅文本方法的PSNR均值仅为16.65，远低于SKED的27.53（Table 1），说明其保真度严重不足。

这一问题的本质在于：文本信号缺乏空间约束能力。用户心中构想的编辑往往具有明确的几何意图——“在这里加一个东西，形状大致是这样”——而纯语言界面无法传递这种空间信息。已有的3D草图形状编辑尝试（如Latent-NeRF的sketch shape pipeline）通过包围盒交叉构造3D掩码来约束编辑区域，但这种方式交互粒度粗糙，难以精确匹配用户手绘草图的轮廓意图。

SKED的动机正是弥合这一鸿沟。其核心洞察在于：**将复杂的草图引导3D编辑分解为两个更易处理的子任务**——其一是基于多视图几何推理的粗编辑区域确定，其二是利用预训练扩散模型丰富语义知识的精细细节生成。用户只需在至少两个视角下绘制简单的填充草图，系统便能从这些二维掩码中推理出编辑应发生的三维空间区域，进而在该区域内通过扩散模型生成符合文本语义的内容，同时严格保持区域外原始场景不变。

这一设计使得SKED在三个维度上同时获益：（1）**保真性**——通过距离感知的保真损失（preservation loss）约束未编辑区域，PSNR相较仅文本方法提升10.88；（2）**草图对齐性**——通过草图填充损失（silhouette loss）确保生成内容精确覆盖用户绘制的区域，IoS达到0.8220；（3）**语义一致性**——CLIP相似度与仅文本方法接近（0.2739 vs 0.2806），在不牺牲语义对齐的前提下实现了局部可控编辑。

简言之，SKED回应了一个朴素而迫切的需求：让用户像在纸上画草图一样，直观地告诉3D模型“在这里改，改成这样”。这一需求在3D资产生成、游戏设计、虚拟现实内容创作等场景中具有广泛的应用前景。

## 核心方法与创新机理

SKED 的核心创新在于将**多视图草图**作为空间约束引入文本到 3D 编辑流程，解决了现有方法仅靠文本提示难以实现精确局部控制的关键瓶颈。其创新体现在三个相互协同的 changed slots 上。

### 编辑控制信号的扩展：文本 + 多视图草图

现有文本到 3D 编辑方法（如 **DreamFusion** 的 Text-Only 变体）仅依赖文本提示驱动编辑，用户无法指定编辑的空间范围和形状——模型可能为了满足文本语义而改变整个基模型的结构。SKED 将控制信号扩展为 **文本提示 + 至少两个视图的草图掩码**（Figure 1, Figure 2）。用户在不同视角绘制草图，系统将其预处理为二值掩码 $\{M_i\}$，从而在 3D 空间中定义出需要编辑的粗略区域。这一设计将复杂的草图引导 3D 编辑分解为两个子任务：基于多视图几何推理的粗编辑区域确定，以及基于预训练扩散模型语义知识的精细细节生成。

### 保真损失 $\mathcal{L}_{pres}$：距离感知的基模型保护

Text-Only 基线没有专门的保真度损失，编辑过程会无差别地修改整个 NeRF 场，导致基模型结构被严重破坏（PSNR 平均仅 16.65）。SKED 引入了**基于距离的保真损失** $\mathcal{L}_{pres}$（Eq. 2），其核心机制是：

1. **距离计算**：对每个采样的 3D 点 $\mathbf{p}_i$，计算其到多视图草图区域的投影距离 $D(\mathbf{p}_i)$（Eq. 1, Figure 3）。距离越远，表示该点越不需要编辑。
2. **权重调制**：通过权重函数 $w_i = 1 - \exp(-D(\mathbf{p}_i)^2 / 2\beta^2)$（Eq. 3）将距离转化为保真损失的调制因子。在远离草图区域，$w_i \to 1$，强约束编辑后 NeRF $F_e$ 的密度和颜色与基模型 $F_o$ 一致；在草图区域内，$w_i \to 0$，允许自由编辑。
3. **损失形式**：$\mathcal{L}_{pres}$ 对占位值使用交叉熵约束、对颜色使用 L2 约束，仅在基模型有不透明占位（$\overline{\alpha_o}$）的区域施加颜色约束，避免在空白区域引入伪影。

参数 $\beta$ 控制编辑的敏感度（Figure 8）：较小的 $\beta$ 使编辑严格限制在草图区域内，较大的 $\beta$ 允许编辑向外柔和扩散。

### 草图填充损失 $\mathcal{L}_{sil}$：确保编辑内容符合用户意图

即使有了保真损失的约束，扩散模型的 Score Distillation Sampling（SDS）梯度本身并不保证生成的内容会填充到用户指定的草图区域。SKED 引入了**草图填充损失** $\mathcal{L}_{sil}$（Eq. 4），在草图视图下最大化渲染对象掩码 $C_j^{\alpha}$ 在草图掩码 $M_j$ 区域内的值：

$$\mathcal{L}_{sil} = \frac{1}{H \cdot W \cdot N} \sum_{j=1}^{N} \sum_{i=1}^{H \cdot W} -\mathbb{I}_{M_j}(\mathbf{x}_i) \log C_j^{\alpha}(\mathbf{x}_i)$$

这一损失与 $\mathcal{L}_{pres}$ 形成互补：保真损失告诉模型“哪里不要改”，草图填充损失告诉模型“哪里必须生成内容”。

### 创新点的协同效果

三个 changed slots 的协同效果在定量消融实验中得到了充分验证（Table 1, Table 2, Figure 9）：

- **移除 $\mathcal{L}_{pres}$**（SKED no-preserve）：PSNR 从 27.53 骤降至 16.14，与 Text-Only 基线（16.65）相当，证明保真损失是保护基模型结构的关键。
- **移除 $\mathcal{L}_{sil}$**（SKED no-silh）：草图填充率 IoS 从 0.8220 降至 0.0211，模型几乎不在草图区域内生成任何内容，证明草图填充损失是引导编辑位置的必要条件。
- **完整 SKED**：在保持基模型高保真度（PSNR 27.53）的同时，实现了高草图对齐度（IoS 0.8220），且 CLIP 语义相似度（0.2739）与 Text-Only（0.2806）接近，表明在不牺牲语义对齐的前提下实现了精确的局部控制。

此外，SKED 还引入了**稀疏性损失** $\mathcal{L}_{sp}$ 和**占用网格预热机制**等辅助设计，前者通过最小化对象掩码的熵保证生成物体的紧凑性，后者通过在编辑初期手动开启草图交叉区域内的占用网格比特，避免因空间为空而跳过采样。

### 与 Latent-NeRF 草图管线的对比

**Latent-NeRF** 的草图形状编辑管线通过包围盒交叉构造 3D 掩码进行约束，而 SKED 直接利用多视图 2D 草图通过投影距离进行逐点调制，无需显式构造 3D 形状。这一设计使得 SKED 在保真度上显著优于 Latent-NeRF 基线（Table 7），且运行时间更短。

SKED 的编辑 pipeline 将“草图引导的文本到 3D 编辑”分解为两个协同执行的子任务：**基于多视图几何推理的粗编辑区域确定**，与**基于预训练扩散模型语义知识的精细编辑**。这一分解使得仅靠文本提示难以实现的局部空间控制，能够通过用户绘制的多视图草图自然地注入编辑优化过程。

### 输入与输出

pipeline 接受三类输入：
- **基 NeRF 模型** $F_o$：一个已训练好的神经辐射场，可以来自重建（如 InstantNGP）或生成（如 DreamFusion）。
- **多视图草图**：用户在至少两个视角下绘制的草图，经预处理转换为二值掩码 $\{M_i\}$。
- **文本提示**：描述期望编辑语义的自然语言指令，例如“一只戴着厨师帽的猫”。

输出为一个编辑后的 NeRF 模型 $F_e$，其在草图指定的空间区域内生成符合文本语义的新内容，同时在草图区域之外保持与基模型 $F_o$ 的一致性。

### 核心模块与数据流

整个优化过程以迭代方式进行，每次迭代包含以下关键模块（参见 Figure 2 的流程示意）：

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2303_10735v3/figures/002_Figure_2.jpg]]
*Figure 2: An overview of SKED. We render the base NeRF model $F _ { o }$ from at least two views and sketch over them (Ci). The input to the editing algorithm is these sketches preprocessed to masks ( $M _ { i }$ ) and a text prompt. In each iteration similar to DreamFusion [52], we render a random view and apply the Score Distillation Loss to semantically align with the text prompt. Additionally, we compute $\mathcal { L } _ { p r e s }$ to preserve the base NeRF by constraining $F _ { e }$ ’s density and color output to be similar to $F _ { o }$ away from the sketch regions. Finally, we use the object mask renderings of the sketch views to define $\mathcal { L } _ { s i l }$ . This loss ensures that the object...

1. **基 NeRF 模型与多视图草图预处理**：用户在基 NeRF 的至少两个渲染视图上绘制草图，系统将其转换为二值掩码。这些掩码定义了编辑的空间范围——草图交叉区域即为编辑发生的三维空间。

2. **随机视图渲染与 Score Distillation Sampling (SDS)**：在每次迭代中，类似 DreamFusion 的范式，随机采样一个相机视角并渲染编辑后 NeRF $F_e$ 的图像。利用预训练的文本到图像潜在扩散模型（Stable Diffusion v1.4），通过 SDS 损失 $\mathcal{L}_{SDS}$ 提供梯度，驱动渲染图像在语义上与文本提示对齐。

3. **距离计算与权重调制**：对于每条光线采样到的 3D 点 $\mathbf{p}_i$，将其投影到各个草图视图 $C_j$ 上，计算投影点到最近草图像素 $m_k$ 的最小距离 $d_j(\mathbf{p}_i)$（公式 1）。对所有草图视图的距离取平均，得到该 3D 点到草图区域的综合距离 $D(\mathbf{p}_i)$。该距离随后通过高斯核函数转换为保真损失的权重 $w_i$（公式 3）：
   $$w_i = 1 - \exp\left(-\frac{D(\mathbf{p}_i)^2}{2\beta^2}\right)$$
   其中 $\beta$ 控制编辑敏感度——$\beta$ 越小，编辑越局限于草图区域；$\beta$ 越大，编辑向外扩散的软化过渡越明显（见 Figure 8）。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2303_10735v3/figures/012_Figure_8.jpg]]
*Figure 8: Sensitivity control. Depending on the sensitivity value determined by β in Eq. 3, our method can either edit only the sketched region and minimally modify the rest of the neural field, or produce larger edits outside the sketch regions (softer blending). We display the overlay of sketches v.s. edited output*

4. **保真损失 $\mathcal{L}_{pres}$**：在远离草图区域的 3D 点上，约束编辑后 NeRF 的密度（以占位值 $\alpha$ 表示）和颜色与基模型一致（公式 2）：
   $$\mathcal{L}_{pres} = \frac{1}{K} \sum_{i=1}^{K} w_i \left[ CE(\alpha_e, \overline{\alpha_o}) + \lambda_c \overline{\alpha_o} \| \mathbf{c}_e - \mathbf{c}_o \|^2 \right]$$
   其中交叉熵项约束占位值的一致性，L2 项约束颜色的一致性，$\lambda_c$ 平衡两项的权重。权重 $w_i$ 确保约束力在草图区域附近弱、远离区域强，从而实现“局部编辑、全局保持”的效果。

5. **草图填充损失 $\mathcal{L}_{sil}$**：在草图视图上，鼓励渲染出的对象掩码 $C_j^{\alpha}$ 尽可能覆盖输入草图区域 $M_j$（公式 4）：
   $$\mathcal{L}_{sil} = \frac{1}{H \cdot W \cdot N} \sum_{j=1}^{N} \sum_{i=1}^{H \cdot W} -\mathbb{I}_{M_j}(\mathbf{x}_i) \log C_j^{\alpha}(\mathbf{x}_i)$$
   该损失确保编辑生成的内容在几何上尊重用户草图的形状约束。

6. **稀疏性损失 $\mathcal{L}_{sp}$**：通过最小化对象掩码的熵，促使生成的内容保持紧凑，避免在编辑区域产生浮空碎片。

7. **占用网格预热与手动开启**：为加速优化初期的收敛，系统手动开启草图交叉区域内的占用网格比特，并定义预热期（默认 1000 次迭代），在此期间逐步建立编辑区域的初始密度。

### 联合优化目标

上述损失函数通过加权求和构成总优化目标：
$$\mathcal{L}_{total} = \mathcal{L}_{SDS} + \lambda_{pres}\mathcal{L}_{pres} + \lambda_{sil}\mathcal{L}_{sil} + \lambda_{sp}\mathcal{L}_{sp}$$

默认超参数设置为 $\lambda_{pres}=5\times10^{-6}$，$\lambda_{sil}=1$，$\lambda_{sp}=5\times10^{-4}$，$\lambda_c=5$。优化器采用 ADAM，学习率 0.005，使用指数衰减调度器，衰减因子 0.1。扩散模型的引导尺度为 100，噪声时间步从 $(20, 980)$ 均匀采样。

### 设计逻辑

该框架的核心设计逻辑在于**通过多视图几何约束将文本驱动的生成能力锚定在用户指定的空间范围内**。SDS 损失提供语义驱动力，草图填充损失提供几何对齐约束，保真损失确保非编辑区域不受影响——三者协同工作，使得 SKED 既能生成符合文本语义的细节（如“厨师帽”的褶皱和质感），又能严格遵循草图的形状边界，同时保持基模型其余部分的完整性。

### 3.1 问题分解与整体流程

SKED 将「草图引导的文本驱动 3D 编辑」这一复杂任务拆解为两个子任务：**基于多视图几何推理的粗编辑区域确定**，以及**基于预训练扩散模型语义知识的精细细节生成**。整体流程如 Figure 2 所示，核心管线模块包括：

1. **基 NeRF 模型**：待编辑的 3D 场景，可以是 InstantNGP 重建或 DreamFusion 生成的结果，定义为 $F_o: (\mathbf{p}, \hat{\mathbf{r}}; \theta) \to (\mathbf{c}_o, \sigma_o)$。
2. **多视图草图预处理**：用户从至少两个视角在基 NeRF 的渲染图上绘制草图，经填充后转换为二值掩码 $\{M_i\}$。
3. **Score Distillation Sampling (SDS)**：沿用 DreamFusion 的 SDS 方法，以预训练文本到图像潜在扩散模型提供梯度，驱动编辑后的 NeRF 生成符合文本语义的图像。
4. **保真损失 $\mathcal{L}_{pres}$**：在远离草图区域约束编辑后的密度和颜色与基模型一致。
5. **草图填充损失 $\mathcal{L}_{sil}$**：确保编辑后对象在草图视图下的渲染掩码覆盖输入草图区域。
6. **稀疏性损失 $\mathcal{L}_{sp}$**：通过最小化对象掩码的熵保证生成物体的紧凑性。
7. **占用网格预热与手动开启**：编辑初期手动开启草图交叉区域内的占用网格比特，并设置预热期（默认 1000 次迭代），避免因空间为空而跳过采样。

总优化目标为：

$$\mathcal{L}_{total} = \mathcal{L}_{SDS} + \lambda_{pres}\mathcal{L}_{pres} + \lambda_{sil}\mathcal{L}_{sil} + \lambda_{sp}\mathcal{L}_{sp} \tag{5}$$

默认超参数为 $\lambda_{pres}=5\times10^{-6}$，$\lambda_{sil}=1$，$\lambda_{sp}=5\times10^{-4}$，$\lambda_c=5$。

### 3.2 距离感知的保真损失

保真损失的核心思想是：**根据 3D 点到多视图草图区域的距离，动态调节对基 NeRF 输出的约束强度**。距离越远，约束越强；距离越近（即位于或靠近编辑区域），约束越弱，允许编辑发生。

#### 3.2.1 每视图距离计算

对于在随机视角采样的一条射线上的 3D 点 $\mathbf{p}_i$，将其投影到每个草图视图 $C_j$，计算投影点到最近草图像素 $m_k$ 的距离（Figure 3 展示了该过程）：

$$d_j(\mathbf{p}_i) = \min_k \| \nabla[\Pi(\mathbf{p}_i, C_j) + \frac{1}{2}] - m_k \|^2 \tag{1}$$

其中 $\Pi(\mathbf{p}_i, C_j)$ 为投影函数，$\nabla$ 为梯度算子用于边缘检测。所有草图视图的距离取平均得到该点的综合距离 $D(\mathbf{p}_i)$。

#### 3.2.2 权重函数

将距离 $D(\mathbf{p}_i)$ 通过高斯核转换为保真损失的逐点权重 $w_i$：

$$w_i = 1 - \exp\left(-\frac{D(\mathbf{p}_i)^2}{2\beta^2}\right) \tag{3}$$

- **变量含义**：$D(\mathbf{p}_i)$ 为点 $\mathbf{p}_i$ 到所有草图视图的平均距离；$\beta$ 为敏感度参数，控制编辑区域向外的软过渡范围（Figure 8 展示了 $\beta$ 的效果）。
- **行为**：当 $D(\mathbf{p}_i) \to 0$（点在草图区域内），$w_i \to 0$，保真约束几乎完全释放；当 $D(\mathbf{p}_i) \gg \beta$（点远离草图区域），$w_i \to 1$，保真约束最强。

#### 3.2.3 保真损失函数

$$\mathcal{L}_{pres} = \frac{1}{K} \sum_{i=1}^{K} w_i \left[ CE(\alpha_e, \overline{\alpha_o}) + \lambda_c \overline{\alpha_o} \| \mathbf{c}_e - \mathbf{c}_o \|^2 \right] \tag{2}$$

- **第一项** $CE(\alpha_e, \overline{\alpha_o})$：对编辑后 NeRF 的占位值 $\alpha_e$ 与基模型占位值 $\overline{\alpha_o}$ 的二元交叉熵，约束几何结构一致性。$\overline{\alpha_o}$ 为基模型占位值的停止梯度版本。
- **第二项** $\lambda_c \overline{\alpha_o} \| \mathbf{c}_e - \mathbf{c}_o \|^2$：对颜色的 L2 约束，仅在基模型有占位（$\overline{\alpha_o} > 0$）的区域生效，避免对空白区域施加无意义的颜色约束。
- **变量含义**：$\mathbf{c}_e, \mathbf{c}_o$ 分别为编辑后和原始 NeRF 的颜色输出；$\lambda_c$ 为颜色约束权重；$K$ 为采样点数量。

### 3.3 草图填充损失

草图填充损失直接优化编辑结果与用户草图的空间对齐，确保生成内容覆盖草图指定的区域：

$$\mathcal{L}_{sil} = \frac{1}{H \cdot W \cdot N} \sum_{j=1}^{N} \sum_{i=1}^{H \cdot W} -\mathbb{I}_{M_j}(\mathbf{x}_i) \log C_j^{\alpha}(\mathbf{x}_i) \tag{4}$$

- **变量含义**：$N$ 为草图视图数量；$H, W$ 为渲染图像分辨率；$\mathbb{I}_{M_j}(\mathbf{x}_i)$ 为指示函数，当像素 $\mathbf{x}_i$ 位于草图掩码 $M_j$ 内时为 1，否则为 0；$C_j^{\alpha}(\mathbf{x}_i)$ 为编辑后 NeRF 在草图视图 $j$ 上渲染的对象掩码值（alpha 通道）。
- **行为**：该损失鼓励渲染的对象掩码在草图区域内的像素值尽可能大（即 $\log C_j^{\alpha} \to 0$），从而最大化生成内容对草图区域的覆盖。

### 3.4 评估指标：草图-填充比

为量化草图对齐程度，定义 Intersection-over-Sketch (IoS)：

$$IoS = \sum_{i=1}^{N} |M_i \cap C_i^{\alpha}| / |M_i|$$

其中 $C_i^{\alpha}$ 为阈值化后的渲染 alpha 掩码。该指标衡量生成内容占据草图区域的比例，值越接近 1 表示对齐越好。Table 2 显示 SKED 的 Mean IoS 达到 0.8220，而移除 $\mathcal{L}_{sil}$ 后骤降至 0.0211，直接验证了草图填充损失的必要性。

## 实验与关键发现

### 核心瓶颈的验证

SKED的出发点在于纯文本驱动的3D编辑存在根本性控制缺陷：用户无法通过语言界面精确指定编辑的空间范围和形状。实验设计围绕三个核心假设展开验证——草图引导能否在不牺牲语义对齐的前提下，显著提升编辑的局部保真度和空间控制精度。

**保真度实验（Table 1）** 直接回应了这一瓶颈。在五个代表性样本（Cat+chef hat、Cupcake+candle、Horse+horn、Sundae+cherry、Plant+flower）上，SKED的平均PSNR达到27.53，而纯文本基线（DreamFusion的公开复现）仅为16.65，差距达+10.88。更关键的是，移除保真损失L_pres的SKED变体（no-preserve）PSNR骤降至16.14，与纯文本基线相当。这一对比揭示了因果链条：保真损失是维持基NeRF结构完整性的必要条件，仅靠SDS的语义梯度无法阻止扩散模型对非编辑区域的侵蚀。附录中的SSIM（Table 4）和LPIPS（Table 5）指标进一步佐证了这一结论，SKED在结构相似性和感知距离上均显著优于纯文本基线和移除保真损失的变体。

**草图对齐实验（Table 2）** 验证了第二个核心假设：草图填充损失L_sil是确保编辑内容出现在用户指定区域的充分条件。SKED的Intersection-over-Sketch（IoS）达到0.8220，表明渲染的对象掩码平均覆盖了82.2%的草图区域。而移除L_sil后（no-silh变体），IoS暴跌至0.0211——编辑内容几乎完全避开草图区域，仅在文本提示的语义引导下随机生成。这一极端对比（Δ=+0.8009）强有力地证明，仅靠文本语义和保真损失的组合无法实现空间定位，草图对齐损失是空间控制的关键因果旋钮。

**语义对齐实验（Table 3）** 排除了“保真度提升以牺牲语义为代价”的可能性。SKED的CLIP相似度为0.2739，与纯文本基线的0.2806仅差-0.0067，差异在统计上不显著。这意味着SKED在严格约束编辑区域的同时，仍能利用预训练扩散模型的语义知识生成符合文本描述的内容。Figure 6的定性结果进一步印证了这一点：同一组草图配合不同文本提示（如“a red tie” vs “a chef hat”），编辑结果既遵循草图几何约束，又体现出不同的语义细节。

### 消融研究的因果分析

消融实验（Figure 9, Table 1-2）揭示了各损失函数的独立贡献和失效模式：

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2303_10735v3/figures/004_Table_1.jpg]]
*Table 1: Fidelity of base field. To assess a method’s ability to preserve the original content, we measure the PSNR ↑ of the method’s output against renderings from the base model. SKED (no-preserve) refers to a variant of our method which doesn’t apply $\mathcal { L } _ { p r e s }$ . Text-Only refers to a public re-implementation of [52]*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2303_10735v3/figures/010_Table_2.jpg]]
*Table 2: Sketch alignment score. We measure the similarity between the user input and generated result by Intersection-over-Sketch (IoS ↑). The IoS is calculated using the intersection between two views of filled sketches, $M _ { i }$ , and the alpha mask of generated edit $C _ { i } ^ { \alpha }$ . See Section 4.3 for elaborate details of this metric. The SKED (no-silh) variant, which runs with $\mathcal { L } _ { p r e s }$ and without $\mathcal { L } _ { s i l }$ avoids generating content in the sketch region (see also Fig. 9)

- **移除L_pres**：基NeRF结构被严重破坏，PSNR降至16.14。视觉上表现为非编辑区域出现纹理漂移和几何变形，说明SDS梯度会不加区分地修改整个辐射场，保真损失是抵抗这种扩散性修改的唯一屏障。
- **移除L_sil**：草图区域几乎不生成任何内容（IoS=0.0211）。编辑后的对象掩码与草图几乎无交集，说明SDS和保真损失的组合无法自发地将编辑内容引导至用户指定位置——空间定位必须通过显式的草图对齐损失来实现。
- **仅使用文本（Text-Only）**：基模型结构被大幅改变以满足文本语义，PSNR仅16.65，但CLIP相似度略高（0.2806）。这暴露了纯文本方法的本质缺陷：它在“理解要编辑什么”和“知道不该编辑什么”之间存在根本性失衡，倾向于以破坏保真度为代价换取语义对齐。

### 敏感度参数β的调控作用

Figure 8展示了保真损失权重函数中的敏感度参数β对编辑范围的连续调控能力。β控制高斯衰减的宽度（见Eq. 3），决定了保真约束从草图边界向外衰减的速率：
- **小β值**：保真约束快速衰减，允许编辑效果向草图外柔和扩散，实现与基模型的自然融合。
- **大β值**：保真约束在草图外仍保持较高强度，编辑严格限定在草图区域内，非编辑区域几乎不受影响。

这一机制使SKED区别于硬性3D掩码方法（如Latent-NeRF的包围盒交叉构造），提供了从“精确手术刀式编辑”到“柔和融合式编辑”的连续控制谱。

### 与Latent-NeRF基线的对比

与Latent-NeRF的3D草图形状管线相比（Table 7），SKED在保真度（PSNR）上表现更优，且平均运行时间更短。Latent-NeRF通过包围盒交叉构造3D掩码进行约束，其交互方式要求用户定义3D空间范围而非2D草图，这在实际操作中更不直观。SKED的2D多视图草图交互更贴近用户的自然绘画习惯，且通过距离感知的权重机制实现了比硬掩码更灵活的保真度调控。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2303_10735v3/figures/020_Table_7.jpg]]
*Table 7: To compare our method’s ability to preserve the base with the baseline derived from Latent-NeRF [41], we measure the PSNR of both method’s outputs against renderings from the base model. Additionally, we report the average runtime of our method compared to the baseline*

### 扩散模型骨架的影响

Figure 10揭示了SKED对底层扩散模型的依赖性。该方法兼容任何适用于DreamFusion框架的扩散模型，但编辑质量受限于扩散模型对方向性提示的敏感度。论文使用的Stable Diffusion v1.4对方向性提示的响应较弱，且实现基于较早的Stable-DreamFusion版本，未包含Magic3D的优化。这解释了为什么SKED的视觉质量无法直接与使用商业扩散模型（如Imagen）的DreamFusion或Magic3D相比——这是实现框架的固有限制，而非方法本身的缺陷。公平性说明中强调，所有比较实验均使用相同的扩散模型和超参数，确保了内部对比的有效性。

### 失败模式与边界条件

基于实验证据和论文自述的局限性，SKED的主要失败模式包括：

1. **分布外物体编辑**：方法假设基NeRF的渲染属于底层扩散模型的分布。对于扩散模型训练数据中罕见的物体类别，编辑质量可能下降。
2. **非不透明材质**：当前框架未支持半透明或非朗伯材质的高级编辑，保真损失和草图填充损失均基于不透明假设。
3. **多视图草图不一致**：草图编辑的精度依赖于用户在多视图间绘制的一致性。不一致的草图（如同一结构在不同视图中位置矛盾）会导致次优结果，因为距离计算和保真权重基于多视图投影的平均值。
4. **扩散模型方向性敏感度不足**：Stable Diffusion对方向性提示的响应较弱，可能导致编辑结果未能完全体现文本语义的细微差异。

### 关键图表结论汇总

- **Table 1 (PSNR)**：SKED的保真度（27.53）显著优于纯文本基线（16.65）和移除保真损失的变体（16.14），证明保真损失是维持基模型结构的关键。
- **Table 2 (IoS)**：SKED的草图填充率（0.8220）远超移除草图损失的变体（0.0211），证明草图对齐损失是实现空间定位的必要条件。
- **Table 3 (CLIP)**：SKED的语义对齐（0.2739）与纯文本基线（0.2806）无显著差异，证明空间控制不以牺牲语义为代价。
- **Figure 8 (β敏感度)**：保真损失的权重衰减参数β提供了从精确编辑到柔和融合的连续控制。
- **Figure 9 (消融可视化)**：各损失函数的独立移除导致保真度崩溃或空间定位失败，验证了联合优化的必要性。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2303_10735v3/figures/011_Table_3.jpg]]
*Table 3: Semantic alignment score. We measure the CLIP-similarity [53] ↑ of the rendered method output with the clip embedding of the input text prompt. Text-Only refers to a public re-implementation of [52]. The qualitative equivalents of Cat and Plant examples are depicted in Fig. 7 from the main paper: Compared with [52] which changes the structure of the base model to satisfy the text semantics, our method preserves the base model, while also maintaining semantic correlation with the text*

## 定位与知识库关联

### 任务定位与核心瓶颈

SKED 面向的是**文本驱动的 3D 编辑**任务，其核心瓶颈在于：仅依赖文本提示的现有方法（如 **DreamFusion** (Poole et al., 2022) 的 SDS 优化范式）难以实现精确的局部控制——用户无法通过自然语言界面指定编辑的空间范围和几何形状。这导致编辑往往产生全局性的结构改变，破坏了基模型的保真性。

SKED 的核心洞察是将这一困难问题**分解为两个子任务**：第一，利用多视图草图的纯几何推理确定编辑的粗略 3D 区域和边界；第二，利用预训练扩散模型的丰富语义知识生成符合文本提示的精细细节。通过引入**多视图草图**作为空间约束信号，SKED 在保持基 NeRF 模型未编辑区域完整性的同时，实现了局部化的、语义一致的编辑。

### 与已有工作的关系

#### 1. 文本到 3D 生成与编辑范式

SKED 直接建立在 **DreamFusion** (Poole et al., 2022) 提出的 **Score Distillation Sampling (SDS)** 框架之上。DreamFusion 首次展示了利用预训练文本到图像扩散模型的梯度来优化 NeRF 的可能性，但其编辑变体仅接受文本提示，缺乏对编辑位置和形状的精确控制。SKED 沿用了 SDS 作为语义对齐的核心机制，但通过引入草图约束和保真损失，从根本上改变了优化的目标空间。

与 **Latent-NeRF** (Metzer et al., 2023) 的草图形状管线相比，两者都试图利用草图进行 3D 形状控制，但交互方式和约束机制存在本质差异：
- Latent-NeRF 通过**包围盒交叉**构造 3D 掩码来约束编辑区域，用户需要从多个视图绘制包围盒而非自由形状的草图。
- SKED 允许用户**直接在渲染视图上绘制任意形状的草图**，然后通过投影距离计算将 2D 草图约束软性地映射到 3D 空间，提供了更直观和灵活的交互方式。

实验表明（Table 7），SKED 在保真度（PSNR）上显著优于 Latent-NeRF 的草图形状管线，同时运行时间更短。

#### 2. 保真损失与草图对齐损失的创新

SKED 提出了两个关键的损失函数，这是其区别于所有现有工作的核心创新：

- **距离感知的保真损失** `$L_{pres}$`（Eq. 2）：根据每个 3D 采样点到多视图草图区域的投影距离 `$D(\mathbf{p}_i)$` 动态计算权重 `$w_i$`（Eq. 3），在远离草图的区域强约束编辑后 NeRF 的密度和颜色与基模型一致，而在草图附近放松约束。这实现了**平滑的编辑过渡**，避免了硬性 3D 掩码带来的边界伪影。参数 `$\beta$` 控制敏感度（Figure 8），允许用户在精确局部编辑和柔和融合之间进行调节。

- **草图填充损失** `$L_{sil}$`（Eq. 4）：通过最大化草图视图下渲染对象掩码在草图区域内的像素值，确保编辑生成的内容**真正占据用户指定的草图区域**。消融实验（Table 2）表明，移除该损失后，草图填充率（IoS）从 0.8220 急剧下降至 0.0211，几乎不生成任何内容。

这种"保真+填充"的双损失设计，使得 SKED 在**不牺牲语义对齐**的前提下（CLIP 相似度 0.2739 vs 仅文本方法 0.2806，Table 3），实现了对基模型结构的高保真保持（PSNR 27.53 vs 16.65，Table 1）。

### 适用边界

SKED 的适用性受以下因素约束：

1. **扩散模型分布假设**：方法假设基 NeRF 模型的渲染属于底层扩散模型的分布。对于该分布之外的物体（如高度专业化的工业零件或医学影像），编辑效果可能下降。Figure 10 展示了不同扩散模型骨架的影响，表明 SKED 兼容任何适用于 SDS 框架的扩散模型。

2. **材质限制**：当前框架暂未支持**半透明或非朗伯材质**（如玻璃、烟雾、水）的编辑，这受限于底层 NeRF 表示和扩散模型的训练数据分布。

3. **草图质量依赖**：编辑精度依赖于用户绘制的准确性和多视图间的一致性。不一致的草图可能导致次优结果——这是多视图几何推理的固有局限。

4. **实现版本约束**：论文实现基于早期版本的 Stable-DreamFusion，未包含 **Magic3D** (Lin et al., 2023) 等后续工作提出的最新优化（如粗到细的优化策略、DMTet 几何表示），因此视觉质量无法直接与使用商业扩散模型（如 Imagen）的 DreamFusion 或 Magic3D 相比。

### 局限与开放问题

#### 已知局限

1. **扩散模型敏感性**：使用的 Stable Diffusion 对方向性提示（directional prompts）的敏感度较低，影响了编辑的精确语义控制。

2. **多视图一致性要求**：方法至少需要两个视图的草图，且草图间需要保持几何一致性。单视图草图或严重不一致的多视图输入可能导致 3D 空间的歧义性。

3. **材质泛化性不足**：不支持透明、镜面等高级材质的编辑。

#### 开放问题

1. **非不透明材质扩展**：如何将草图引导的编辑框架扩展到半透明材质（如玻璃器皿、烟雾效果）？这可能需要修改 NeRF 的渲染方程和扩散模型的引导方式。

2. **多模态协同编辑**：能否将草图引导扩展到与其他模态（如语音指令、深度图、法向图）的协同编辑？例如，用语音指定"这里加一个金属质感的把手"，同时用草图勾画位置。

3. **动态序列编辑**：能否利用草图线条（而非填充区域）进行动画序列的 3D 编辑，类似于传统 2D 动画工具中的关键帧绘制？这需要解决时序一致性和运动插值问题。

4. **降低交互门槛**：如何减少对多视图草图一致性的依赖？能否仅凭单视图草图或更模糊的线稿实现可靠编辑？这可能需要引入更强的 3D 先验（如单目深度估计、对称性假设）来补偿缺失的视图信息。

5. **与最新 3D 表示的融合**：当前方法基于 InstantNGP 的 NeRF 表示，如何将草图引导的编辑策略迁移到更先进的 3D 表示（如 3D Gaussian Splatting、DMTet）上，以获得更好的几何质量和编辑灵活性？

## 原文 PDF

![[paperPDFs/ICCV_2023/SKED_Sketch_guided_Text_based_3D_Editing.pdf]]
