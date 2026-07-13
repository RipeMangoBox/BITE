---
title: "Sketch2CT: Multimodal Diffusion for Structure-Aware 3D Medical Volume Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Sketch2CT_Multimodal_Diffusion_for_Structure_Aware_3D_Medical_Volume_Generation.pdf
project_link: null
code_link: "https://github.com/adlsn/Sketch2CT"
aliases:
- Sketch2CT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 多模态特征融合质量：TSFE与CGFM模块通过局部文本引导的草图特征调制和全局层次注意力对齐，决定了解剖结构的生成精度，是生成质量的关键因果杠杆。
primary_logic: 将用户草图和文本描述作为互补的结构与语义条件，引入两阶段潜在扩散框架：首先生成3D分割掩模作为几何代理，再基于其合成CT体积，并以胶囊注意力骨干实现鲁棒多模态融合，从而以低成本实现结构感知且解剖连贯的3D医学体积生成。
claims:
- 移除跨模态全局融合模块（CGFM）导致下游分割Dice从0.893显著降至0.825，证明全局语义对齐对解剖精度至关重要。
- 仅使用草图或仅使用文本进行条件生成均失败：草图无法恢复完整3D几何（单视图歧义），文本无法提供准确的空间布局，证实了两种模态的互补性不可或缺。
- 在所有四个数据集的下游分割任务中，Sketch2CT生成的数据训练出的分割模型性能最接近真实数据训练的基线，显示了生成体积的解剖真实感和泛化能力。
- CHAOS liver (CT) 上 FID = 33.7
---

# Sketch2CT: Multimodal Diffusion for Structure-Aware 3D Medical Volume Generation

> [!tip] 核心洞察
> 将用户草图和文本描述作为互补的结构与语义条件，引入两阶段潜在扩散框架：首先生成3D分割掩模作为几何代理，再基于其合成CT体积，并以胶囊注意力骨干实现鲁棒多模态融合，从而以低成本实现结构感知且解剖连贯的3D医学体积生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Sketch2CT：结构感知三维医学体积的多模态扩散生成 |
| 英文题名 | Sketch2CT: Multimodal Diffusion for Structure-Aware 3D Medical Volume Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22509) · [Code](https://github.com/adlsn/Sketch2CT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Sketch2CT |
| Dataset | CHAOS liver, AVT aorta, Decathlon liver, Decathlon heart |

> [!tip] 效果简介
> - CHAOS liver (CT) 上，FID 33.7 vs Seg-Diff: 37.8 (-4.1)。
> - AVT aorta (CT) 上，FID 36.9 vs Seg-Diff: 38.9 (-2.0)。
> - Decathlon liver (CT) 上，FID 36.5 vs Seg-Diff: 34.8 (+1.7)。

## 概要

**问题瓶颈**：现有医学图像生成方法在低数据条件下难以产生解剖学一致且可控的3D体积——2D方法缺乏层间连续性，纯3D方法计算代价高且多模态控制困难，数据稀缺与可控性不足构成核心矛盾。

**核心洞察**：Sketch2CT将用户草图和文本描述作为互补的结构与语义条件，引入两阶段潜在扩散框架：首先生成3D分割掩模作为几何代理，再基于其合成CT体积，从而以低成本实现结构感知且解剖连贯的3D医学体积生成。

**方法定位**：Sketch2CT区别于仅依赖分割掩模的传统扩散基线（如**Med-DDPM**、**MedGen3D**、**Seg-Diff**），关键创新在于多模态条件融合——通过文本增强草图特征提取器（TSFE）以FiLM机制实现文本引导的通道调制，以及跨模态全局融合模块（CGFM）以分层注意力实现局部与全局语义对齐。这两者构成生成质量的因果杠杆：消融实验显示，移除CGFM使下游分割Dice从0.893骤降至0.825（CHAOS肝脏），移除TSFE使Dice平均下降约0.03；而单独使用草图或文本均无法生成正确的3D解剖结构（Figure A3）。

**主要结果**：在CHAOS肝脏、AVT主动脉、Decathlon肝脏和Decathlon心脏四个数据集上，Sketch2CT生成数据训练的分割模型性能最接近真实数据训练的基线（Table 3），验证了生成体积的解剖真实感与泛化能力。合成图像质量方面，FID在多数数据集上优于基线（Table 1），但对输入掩模的忠实度（Dice）在所有数据集上一致最优（Table 2）。

**局限与开放问题**：当前实现仅限于单器官合成，尚未扩展到多器官联合生成场景；文本描述依赖自动流程从参考分割中提取几何特征，可能无法覆盖复杂解剖变异。未来方向包括多器官联合建模、疾病感知的草图编辑，以及放射科医生盲审验证临床诊断价值。

### 三维医学体积生成的核心瓶颈

三维医学体积（CT、MRI）的合成在数据增强、手术规划和医学教育中具有重要价值，但其生成面临两个根本性挑战：**数据稀缺**与**可控性不足**。医学影像数据的获取受限于隐私法规、标注成本高昂以及罕见病例的天然稀疏性，导致可用于训练生成模型的数据量远小于自然图像领域。与此同时，现有生成方法在低数据条件下难以产出解剖学一致且可控的三维体积——二维方法缺乏层间连续性，纯三维方法计算代价高且多模态控制困难，使得临床用户难以按需生成符合特定解剖结构的体积。

### 现有方法的缺口

当前医学图像生成方法在可控性与结构保真度之间存在明显的权衡：

- **纯三维扩散模型**（如 **Med-DDPM**、**MedGen3D**）虽然能够建模体积的空间连续性，但通常以分割掩模为唯一条件输入。这类条件缺乏语义上下文，且掩模本身需要专业标注才能获取，限制了用户驱动的交互式生成。
- **二维切片式方法**（如 **Seg-Diff**）将三维体积分解为独立切片进行生成，虽然降低了计算代价，但破坏了层间解剖连贯性，导致生成体积在冠状面和矢状面上出现结构断裂。
- **条件模态单一**：无论是基于掩模还是随机噪声的生成，现有方法均未充分利用用户可直观提供的**草图**和**文本描述**作为互补条件。草图能够编码二维轮廓和局部几何线索，但存在单视图歧义，无法恢复完整三维形状；文本能够传达全局形状、表面特征和空间位置等语义信息，但缺乏精确的空间布局约束。二者的互补性在现有工作中未被系统性地挖掘。

### 本文动机

Sketch2CT的提出旨在填补上述缺口，核心动机可归纳为三个层面：

1. **以用户友好的多模态条件替代专业标注**：草图和文本是临床用户能够快速提供的自然交互形式。将二者作为互补的结构与语义条件，可以绕过对精确分割掩模的依赖，降低生成门槛。
2. **以两阶段潜在扩散实现低成本的结构感知生成**：首先生成三维分割掩模作为几何代理，再基于其合成CT体积。这种解耦设计使得掩模生成阶段可以专注于解剖结构的正确性，而体积合成阶段可以专注于纹理和外观的真实感，从而在低计算代价下实现解剖连贯的三维体积生成。
3. **以鲁棒的多模态融合机制弥合模态鸿沟**：草图的稀疏几何特征与文本的密集语义特征在表示空间上存在本质差异。需要设计专门的编码与融合模块——文本增强草图特征提取器（TSFE）和跨模态全局融合模块（CGFM）——来建立局部轮廓与全局语义之间的对应关系，这是生成质量的关键因果杠杆。

## 核心方法与创新机理

Sketch2CT 的核心创新在于将**多模态条件生成**引入三维医学体积合成，通过**两阶段潜在扩散框架**和**因果性多模态融合机制**，解决了现有方法在低数据条件下解剖一致性与可控性不足的瓶颈。其相对于基线方法的关键创新可归纳为以下五个 changed slots。

### 1. 多模态条件范式：草图 + 文本的互补结构-语义控制

现有医学图像生成方法（如 **Med-DDPM**、**MedGen3D**、**Seg-Diff**）仅依赖分割掩模或随机掩模作为单一结构条件，缺乏对用户意图的灵活表达能力。Sketch2CT 首次将**用户提供的二维轮廓草图**与**LLM 生成的纯几何文本描述**作为互补条件引入：草图提供直观的局部结构约束，文本编码全局形状、表面特征和空间位置等语义先验。消融实验（Figure A3）直接证实了两种模态的**互补不可或缺性**——仅使用草图时，单视图歧义导致无法恢复完整三维几何；仅使用文本时，全局形状错误且空间位置偏差。这一发现构成了整个框架的设计基础。

### 2. 文本增强草图特征提取器（TSFE）：语义引导的稀疏特征调制

传统草图编码器（如标准 CNN）难以从稀疏的二维轮廓中提取具有解剖判别力的特征。Sketch2CT 提出的 **TSFE** 模块通过 **FiLM（Feature-wise Linear Modulation）** 机制实现文本语义对草图特征的**自适应通道级调制**：

$$\gamma, \beta = g(\mathbf{f}_t)$$

$$\tilde{\mathbf{f}}_s = \gamma \odot \mathbf{f}_s + \beta$$

文本嵌入经可学习函数 $g(\cdot)$ 生成缩放参数 $\gamma$ 和移位参数 $\beta$，逐元素作用于草图嵌入 $\mathbf{f}_s$，从而**放大与文本语义相关的解剖通道，抑制无关响应**。消融实验（Table A1）表明，移除 TSFE 导致下游分割 Dice 平均下降约 0.03（如 CHAOS liver 从 0.893 降至 0.864），验证了文本引导调制对稀疏草图特征的关键增强作用。

### 3. 跨模态全局融合模块（CGFM）：层次化注意力对齐

简单拼接或浅层融合无法建立草图与文本之间的深层语义对应。Sketch2CT 的 **CGFM** 模块设计了**两级注意力机制**实现局部到全局的多模态对齐：

$$\mathbf{F}_{\mathrm{local}} = \mathrm{Attention}(\tilde{\mathbf{f}}_s, \mathbf{f}_t, \mathbf{f}_t)$$

$$\mathbf{F}_{\mathrm{global}} = \mathrm{SelfAttn}(\mathbf{F}_{\mathrm{local}})$$

$$\mathbf{z}_{\mathrm{fusion}} = \mathrm{Proj}([\mathbf{F}_{\mathrm{local}} \parallel \mathbf{F}_{\mathrm{global}}])$$

第一级**文本引导交叉注意力**以增强后的草图特征为 Query、文本嵌入为 Key/Value，捕捉轮廓与语义描述的局部对应关系；第二级**草图引导自注意力**对局部响应进行全局聚合，形成器官的整体几何与语义表征。最终拼接局部与全局特征并投影为扩散条件输入。这是整个框架中**因果杠杆最强的组件**——消融实验（Table A1）显示，移除 CGFM 导致 Dice 下降约 0.06–0.07（如 CHAOS liver 从 0.893 骤降至 0.825），降幅显著大于移除 TSFE，证明层次化注意力对齐对解剖结构重建具有决定性影响。

### 4. 两阶段潜在扩散管线：分割代理 → 体积合成

区别于直接生成三维体积或逐切片合成的基线方案，Sketch2CT 采用**分割掩模作为几何代理**的两阶段策略：（1）多模态条件潜在扩散模型生成三维器官分割掩模；（2）以分割潜在表示为结构先验，通过通道级联条件潜在扩散模型合成解剖一致的 CT/MRI 体积：

$$\mathbf{z}_{t-1} = \epsilon_\theta(\mathbf{z}_t \mid\mid \mathbf{z}_{\mathrm{seg}}, t)$$

该设计的核心优势在于**解耦几何生成与纹理合成**，以低成本实现结构感知。消融实验（Table A1）提供了最强证据：移除分割潜在扩散模型（w/o Seg-LDM）导致 Dice 崩溃式下降（CHAOS liver 从 0.893 降至 0.642，降幅 > 0.25），证明在潜在空间显式建模分割是框架不可或缺的组件。

### 5. 胶囊注意力骨干：结构保持的特征编码

Sketch2CT 采用**胶囊网络结合注意力机制**作为草图编码器骨干（Figure 2a），替代基线方法中的标准 CNN。胶囊网络通过向量输出保留了草图中轮廓部件的空间层级关系与姿态信息，相比标量 CNN 特征更能保持细粒度结构，为后续的 TSFE 调制和 CGFM 对齐提供了更丰富的几何基元。该设计选择虽未单独消融，但其与 TSFE/CGFM 的协同构成了多模态特征提取的完整因果链。

**总结**：Sketch2CT 的创新本质在于通过 TSFE（文本→草图的语义注入）与 CGFM（局部→全局的注意力对齐）构建了高质量的多模态融合表征，并将其作为两阶段潜在扩散的条件驱动，从而在数据稀缺条件下实现解剖一致且用户可控的三维医学体积生成。

Sketch2CT 采用**两阶段级联潜在扩散**架构，将用户提供的草图和文本描述转化为解剖一致的三维医学体积。其核心设计理念在于：首先生成三维分割掩模作为几何代理，再以此为结构先验合成CT体积，从而在低数据条件下实现结构感知的生成。

### 两阶段生成管线

**阶段一：分割掩模生成。** 该阶段以用户的二维轮廓草图和文本描述为多模态条件，通过潜在扩散模型生成目标器官的三维分割掩模。草图提供局部结构约束，文本注入语义先验，二者互补——单独使用草图无法恢复完整的三维几何（单视图歧义），单独使用文本则缺乏准确的空间布局（Figure A3）。生成的分割掩模作为中间几何代理，为后续体积合成提供精确的结构蓝图。

**阶段二：医学体积合成。** 以第一阶段生成的分割潜在表示为条件，通过第二个潜在扩散模型合成解剖一致的三维CT体积。具体而言，分割潜在表示与含噪图像潜在表示在通道维度上进行拼接，以指导去噪轨迹（Eq. 10）。这种“先建几何、后填纹理”的策略将结构一致性与纹理真实感解耦，降低了直接生成三维体积的难度。

### 多模态条件提取

在进入扩散模型之前，系统需要从参考数据中提取训练所需的多模态条件对：

- **草图提取：** 利用 PyVista 库对三维分割标签进行高对比度表面投影渲染，再通过 Canny 边缘检测提取显著轮廓，形成二维草图。这模拟了用户手绘的结构输入。
- **文本获取：** 将多视角快照和几何指标（如体积、表面积等）作为提示输入大语言模型（GPT-4o-mini），生成纯几何描述文本。该文本随后通过预训练句子转换器编码为高维语义嵌入，为后续融合提供语义条件。

### 多模态融合核心模块

为有效对齐和融合草图的局部结构信息与文本的全局语义信息，框架引入了两个关键模块：

- **文本增强草图特征提取器（TSFE）：** 通过 FiLM 机制，由文本嵌入生成缩放参数 $\gamma$ 和移位参数 $\beta$（Eq. 1），对胶囊网络提取的草图嵌入进行逐元素调制（Eq. 2）：$\tilde{\mathbf{f}}_s = \gamma \odot \mathbf{f}_s + \beta$。这一设计使稀疏的草图特征能够在语义引导下自适应地增强解剖相关通道，抑制无关噪声。

- **跨模态全局融合模块（CGFM）：** 采用双层注意力机制实现全局语义对齐。首先通过文本引导交叉注意力捕捉草图轮廓与文本语义的局部对应关系，生成局部融合特征 $\mathbf{F}_{\mathrm{local}}$（Eq. 3）；随后通过草图引导自注意力聚合这些局部响应，形成器官的整体几何与语义表征 $\mathbf{F}_{\mathrm{global}}$（Eq. 4）。二者拼接后投影为最终的融合条件 $\mathbf{z}_{\mathrm{fusion}}$（Eq. 5），输入分割潜在扩散模型。

### 数据流总览

完整的输入输出流可概括为：**用户草图 + 文本描述 → TSFE 特征增强 → CGFM 跨模态融合 → 分割潜在扩散生成三维掩模 → 掩模潜在条件引导图像潜在扩散合成三维CT体积**。整个框架的概览如 Figure 2 所示，其中 (a) 展示多模态编码与融合，(b) 展示分割掩模生成，(c) 展示医学体积合成。

![[assets/figures/papers/paper_list_l2595_https_arxiv_org_abs_2603_22509/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Sketch2CT framework. (a) A capsule-based sketch encoder and a sentence transformer extract structural and semantic features, which are fused via a FiLM module. (b) The fused representation conditions a segmentation latent diffusion model to generate 3D organ masks. (c) The predicted segmentation latent guides an image latent diffusion model to synthesize 3D medical volumes*

### 与基线方法的差异

相较于仅使用分割掩模作为条件的基线方法（如 **Med-DDPM**、**MedGen3D**、**Seg-Diff**），Sketch2CT 的关键差异在于引入了**多模态用户控制**（草图+文本），并通过 TSFE 和 CGFM 实现了跨模态的深层交互。基线方法无法直接利用草图和文本生成条件分割掩模，因此在实验中为其提供了 Sketch2CT 生成的合成掩模作为输入，以确保比较的公平性。

Sketch2CT 的核心架构围绕**多模态条件融合**与**两阶段潜在扩散生成**两条主线展开。其关键模块包括文本增强草图特征提取器（TSFE）和跨模态全局融合模块（CGFM），二者共同将用户提供的草图和文本描述转化为解剖学一致的三维分割掩模，进而驱动后续的CT体积合成。

### 文本增强草图特征提取器（TSFE）

TSFE 旨在利用文本语义先验丰富稀疏的草图表示。其核心机制是**特征线性调制（FiLM）**：从预训练句子转换器编码的文本嵌入 $\mathbf{f}_t$ 出发，通过一个可学习函数 $g(\cdot)$ 生成缩放参数 $\gamma$ 和移位参数 $\beta$：

$$\gamma, \beta = g(\mathbf{f}_t) \tag{Eq. 1}$$

随后，这些参数被用于逐元素调制胶囊网络提取的草图嵌入 $\mathbf{f}_s$：

$$\tilde{\mathbf{f}}_s = \gamma \odot \mathbf{f}_s + \beta \tag{Eq. 2}$$

这一调制过程**自适应地放大了与文本语义相关的解剖通道**，使模型能够将用户随手绘制的粗略轮廓与器官的全局几何属性（如“肝脏呈楔形，表面光滑”）建立关联。

### 跨模态全局融合模块（CGFM）

CGFM 通过**两级注意力机制**实现局部与全局尺度的多模态对齐。首先，以文本嵌入为查询、文本增强后的草图特征为键和值，执行**文本引导的交叉注意力**，捕捉草图轮廓与文本语义之间的局部对应关系：

$$\mathbf{F}_{\mathrm{local}} = \mathrm{Attention}(\tilde{\mathbf{f}}_s, \mathbf{f}_t, \mathbf{f}_t) \tag{Eq. 3}$$

随后，在局部特征之上施加**草图引导的自注意力**，聚合分散的局部响应，形成器官的整体几何与语义表征：

$$\mathbf{F}_{\mathrm{global}} = \mathrm{SelfAttn}(\mathbf{F}_{\mathrm{local}}) \tag{Eq. 4}$$

最终，局部与全局特征被拼接并投影为统一的扩散条件输入：

$$\mathbf{z}_{\mathrm{fusion}} = \mathrm{Proj}([\mathbf{F}_{\mathrm{local}} \parallel \mathbf{F}_{\mathrm{global}}]) \tag{Eq. 5}$$

消融实验证实了 CGFM 的关键作用：**移除 CGFM 导致下游分割 Dice 从 0.893 骤降至 0.825**（CHAOS liver，Table A1），验证了分层注意力对齐对解剖结构重建的决定性影响。

### 分割潜在扩散模型

融合后的多模态特征 $\mathbf{z}_{\mathrm{fusion}}$ 作为条件，驱动一个在潜在空间中运行的扩散模型生成三维器官分割掩模。前向过程逐步向潜在变量 $\mathbf{z}_0$ 添加高斯噪声：

$$q(\mathbf{z}_t | \mathbf{z}_{t-1}) = \mathcal{N}(\sqrt{\alpha_t}\mathbf{z}_{t-1}, (1-\alpha_t)\mathbf{I}) \tag{Eq. 6}$$

逆向过程则基于多模态融合条件进行去噪：

$$p_\theta(\mathbf{z}_{t-1} | \mathbf{z}_t, \mathbf{z}_{\mathrm{fusion}}) = \mathcal{N}(\mu_\theta(\mathbf{z}_t, t, \mathbf{z}_{\mathrm{fusion}}), \sigma^2_t\mathbf{I}) \tag{Eq. 7}$$

训练采用 **v-预测参数化**，目标速度项定义为：

$$\mathbf{v}_t = \sqrt{\alpha_t}\epsilon - \sqrt{1-\alpha_t}\mathbf{z}_0 \tag{Eq. 8}$$

损失函数最小化预测速度与真实速度的均方误差：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{t,\mathbf{z}_0,\epsilon}[\|\epsilon_\theta(\mathbf{z}_t, t, \mathbf{z}_{\mathrm{fusion}}) - \mathbf{v}_t\|^2_2] \tag{Eq. 9}$$

消融实验中，**移除分割潜在扩散模型（w/o Seg-LDM）导致 Dice 崩溃式下降**（CHAOS liver 从 0.893 降至 0.642，Table A1），证明在潜在空间中进行分割建模是整个框架不可或缺的组件。

### 医学体积生成（图像潜在扩散模型）

第二阶段以生成的分割潜在表示 $\mathbf{z}_{\mathrm{seg}}$ 为结构先验，通过**通道级联**的方式将其与噪声图像潜在变量拼接，引导去噪轨迹：

$$\mathbf{z}_{t-1} = \epsilon_\theta(\mathbf{z}_t \mid\mid \mathbf{z}_{\mathrm{seg}}, t) \tag{Eq. 10}$$

该阶段同样采用 v-预测参数化（遵循 Eq. 9），确保生成的 CT 体积与第一阶段的分割掩模在解剖结构上严格对齐。

![[assets/figures/papers/paper_list_l2595_https_arxiv_org_abs_2603_22509/figures/009_Figure.jpg]]
*Figure: A3. Comparison of segmentation masks generated using sketch-only and text-only conditions. Sketch-only guidance fails to recover full 3D geometry due to single-view ambiguity. In contrast, text-only guidance yields incorrect global shape and spatial placement, underscoring the need to combine sketches and text*

## 实验与关键发现

### 主实验结果

Sketch2CT在四个数据集上与Med-DDPM、MedGen3D、Seg-Diff三个基线进行了对比。由于基线方法无法直接使用草图和文本条件生成分割掩模，实验统一为基线提供Sketch2CT生成的合成掩模作为输入，确保条件公平。

**图像质量评估**（Table 1）：以FID和LPIPS为指标，Sketch2CT在多数数据集上取得最优。在CHAOS肝脏CT上，FID降至33.7（Seg-Diff为37.8，降低4.1）；在AVT主动脉CT上FID为36.9（Seg-Diff为38.9）；在Decathlon心脏MRI上FID为65.1（Seg-Diff为68.4）。仅在Decathlon肝脏CT上，Seg-Diff的FID略优（34.8 vs. 36.5），但Sketch2CT的LPIPS（0.328）仍具竞争力。

**生成图像与输入掩模的忠实度**（Table 2）：通过两种Dice指标衡量——生成图像预测分割与输入掩模的Dice，以及生成图像预测分割与真实图像预测分割的Dice。Sketch2CT在所有数据集上均取得最高分：CHAOS肝脏上分别为0.868/0.852，AVT主动脉上为0.894/0.887，Decathlon肝脏上为0.912/0.904，Decathlon心脏上为0.642/0.614。这表明两阶段潜在扩散框架有效将掩模结构信息传递至最终体积。

**下游分割验证**（Table 3）：用各方法生成的合成数据训练分割模型，在真实测试集上评估Dice。Sketch2CT生成数据训练的模型在所有数据集上性能最接近真实数据训练的基线，证明其生成的体积具有最强的解剖真实感和泛化能力。这是验证生成数据临床可用性的关键证据。

### 消融实验

消融实验（Table A1）系统移除了三个核心组件，以下游分割Dice为指标评估各模块贡献：

![[assets/figures/papers/paper_list_l2595_https_arxiv_org_abs_2603_22509/figures/010_Table.jpg]]
*Table: A1. Ablation study of Sketch2CT. Removing TSFE, CGFM, or the segmentation latent diffusion model (Seg-LDM) reduces downstream segmentation performance, confirming that all components are essential for generating anatomically coherent and text-aligned 3D masks*

- **移除文本增强草图特征提取器（w/o TSFE）**：Dice在CHAOS肝脏上从0.893降至0.864，AVT主动脉从0.907降至0.859，Decathlon肝脏从0.917降至0.872，Decathlon心脏从0.733降至0.683。平均下降约0.03，证明文本引导的FiLM通道调制对稀疏草图特征的语义增强至关重要——没有文本先验，模型难以从单视角轮廓推断完整三维结构。

- **移除跨模态全局融合模块（w/o CGFM）**：性能下降更为剧烈，CHAOS肝脏Dice降至0.825（下降0.068），AVT主动脉降至0.818（下降0.089），Decathlon肝脏降至0.831（下降0.086），Decathlon心脏降至0.671（下降0.062）。这验证了分层注意力对齐（文本引导交叉注意力+草图引导自注意力）对解剖结构重建的关键作用——局部-全局联合推理是弥合稀疏草图和完整三维几何之间鸿沟的核心机制。

- **移除分割潜在扩散模型（w/o Seg-LDM）**：Dice崩溃式下降，CHAOS肝脏仅0.642（下降0.251），AVT主动脉0.629（下降0.278），Decathlon肝脏0.633（下降0.284），Decathlon心脏0.545（下降0.188）。这证明在潜在空间显式建模分割掩模是不可或缺的——直接跳过掩模生成会导致结构条件严重丢失。

### 模态互补性验证

单独使用草图或单独使用文本进行条件生成均失败（Figure A3）：仅草图引导无法从单视角轮廓恢复完整三维几何（多视图歧义问题），仅文本引导无法提供准确的空间布局（全局形状错误和位置偏差）。这直接证实了两种模态的互补性——草图提供局部结构约束，文本提供全局语义锚定，二者缺一不可。

### 失败模式与局限

当前框架仅支持单一器官合成（肝脏、主动脉、心脏），尚未扩展到多器官联合生成场景，无法建模器官间的空间关系。文本描述依赖自动流程从参考分割中提取几何特征，可能无法覆盖复杂的解剖变异。此外，Decathlon心脏MRI上的绝对Dice（0.642）仍显著低于其他器官，提示心脏的复杂运动和形态变化对生成构成更大挑战，需要进一步验证。

![[assets/figures/papers/paper_list_l2595_https_arxiv_org_abs_2603_22509/figures/003_Table_1.jpg]]
*Table 1: Quantitative evaluation of synthetic images. We report FID (lower is better) and LPIPS (higher is better) across four datasets. Since baseline models cannot generate conditional segmentations, we provide synthesized masks as their inputs*

![[assets/figures/papers/paper_list_l2595_https_arxiv_org_abs_2603_22509/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison of baseline methods. For each case, we extract a sketch and text description from the ground-truth mask to encode organ geometry. These features guide the generation of 3D masks and the synthesis of 3D volumes*

![[assets/figures/papers/paper_list_l2595_https_arxiv_org_abs_2603_22509/figures/011_Figure.jpg]]
*Figure: A4. Qualitative diversity demonstration using a single Decathlon liver case. Under identical sketch and text conditions, three independent runs (r1-r3) generate anatomically consistent yet appearance-varying CT volumes, illustrating the stochastic diversity of Sketch2CT*

## 定位与知识库关联

### 与现有基线的关系

Sketch2CT 处于可控医学图像生成与多模态条件扩散模型的交叉地带。其最直接的对比基线包括三类方法：

- **3D扩散生成方法**：**Med-DDPM** 和 **MedGen3D** 代表纯3D扩散范式，以分割掩模为条件直接生成医学体积。然而，这些方法依赖完整的分割掩模作为输入条件，无法接受草图和文本等多模态用户输入。Sketch2CT 在实验中为这些基线提供了合成掩模以保持公平比较（Table 1），但其核心差异在于条件模态的灵活性和可及性——草图比完整分割掩模更易获取，文本描述进一步补充了语义先验。

- **2D切片级扩散方法**：**Seg-Diff** 以分割引导的2D扩散逐切片合成，缺乏层间连续性建模。Sketch2CT 通过两阶段潜在扩散框架（先3D掩模生成，再3D体积合成）在潜在空间中显式建模三维结构，避免了2D方法固有的切片间不一致问题。

- **多模态融合范式**：与简单的拼接融合不同，Sketch2CT 引入了两个关键模块——**文本增强草图特征提取器（TSFE）** 和**跨模态全局融合模块（CGFM）**。TSFE 通过 FiLM 机制实现文本引导的通道级自适应调制（$\tilde{\mathbf{f}}_s = \gamma \odot \mathbf{f}_s + \beta$），CGFM 则通过文本引导交叉注意力（$\mathbf{F}_{\mathrm{local}} = \mathrm{Attention}(\tilde{\mathbf{f}}_s, \mathbf{f}_t, \mathbf{f}_t)$）和草图引导自注意力（$\mathbf{F}_{\mathrm{global}} = \mathrm{SelfAttn}(\mathbf{F}_{\mathrm{local}})$）实现分层全局语义对齐。消融实验表明，移除 CGFM 导致下游分割 Dice 从 0.893 降至 0.825（CHAOS liver），验证了分层注意力对齐对解剖精度的关键因果作用（Table A1）。

### 适用边界

Sketch2CT 的适用性受以下边界约束：

1. **器官范围限制**：当前实现仅在肝脏（CHAOS、Decathlon）、主动脉（AVT）和心脏（Decathlon）四个数据集上验证，均为单一器官场景。框架尚未扩展到多器官联合生成，无法建模器官间的空间关系和上下文约束。

2. **模态依赖**：方法依赖成对的草图-文本-分割掩模三元组进行训练。草图和文本均从参考分割中自动提取（Canny边缘检测 + LLM几何描述生成），这意味着训练数据的多样性和质量受限于自动提取流程的覆盖能力，可能无法充分捕获复杂解剖变异。

3. **病理建模缺失**：当前框架仅生成正常解剖结构，未涉及病变区域的条件生成。虽然草图编辑范式天然支持用户添加病变轮廓，但论文未验证疾病感知生成的有效性。

### 局限与开放问题

**已知局限**（论文明确指出的部分）：

- 仅支持单一器官合成，未扩展到多器官联合生成场景。
- 文本描述依赖自动流程从参考分割中提取几何特征，可能无法覆盖所有复杂解剖变异。

**开放问题**（需要进一步研究的方向）：

1. **多器官联合生成**：如何将两阶段框架扩展到多器官场景，建模器官间的空间关系（如肝-肾-脾的相对位置），以生成更真实的解剖上下文？这需要重新设计条件编码和注意力机制以处理多实例分割掩模。

2. **病理感知生成**：能否通过疾病感知的草图编辑（如添加肿瘤轮廓、血管狭窄标记）来模拟病理变化？这要求在分割掩模生成阶段引入病理形状先验，并在体积合成阶段生成相应的纹理异常（如低密度病灶）。

3. **临床验证**：论文使用下游分割任务的 Dice 作为解剖真实感的代理指标，但缺乏放射科医生的盲审评估。生成数据在实际临床诊断任务（如病变检测、良恶性分类）中的价值需要更广泛的专家验证。

4. **文本描述的自动化质量**：当前使用 GPT-4o-mini 从多视角快照和几何指标生成文本描述（Figure A1），但该流程的鲁棒性未经验证。不同LLM或不同提示策略对生成质量的影响尚不明确，且文本描述是否真正捕获了临床相关的解剖特征（而非仅几何属性）值得进一步探讨。

## 原文 PDF

![[paperPDFs/CVPR_2026/Sketch2CT_Multimodal_Diffusion_for_Structure_Aware_3D_Medical_Volume_Generation.pdf]]
