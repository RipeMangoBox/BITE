---
title: "WonderZoom: Multi-Scale 3D World Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/WonderZoom_Multi_Scale_3D_World_Generation.pdf
project_link: "https://wonderzoom.github.io/"
code_link: null
aliases:
- WonderZoom
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 提出尺度自适应高斯面元（Scale-Adaptive Gaussian Surfels），通过增量添加新面元（无需重新优化）和尺度感知透明度调制，实现多尺度3D内容的动态扩展与平滑过渡；并设计渐进式细节合成器（Progressive Detail Synthesizer），以粗尺度3D几何为条件，通过超分重建、语义编辑、深度配准和辅助视图合成，迭代生成精细...
primary_logic: 多尺度3D生成应遵循由粗到细的迭代范式：先构建粗尺度场景，再将其渲染结果和几何信息作为空间条件，逐步合成细尺度内容。可增量更新且保持实时渲染能力的分层3D表示是实现该范式的核心，它打破了重建范式对先验数据的依赖，使3D世界能够按需生长。
claims:
- 在8张测试图像（涵盖自然、城市、水下等多种场景）上，WonderZoom在CLIP分数（CS）、CLIP-IQA+（CIQA）、Q-align IQA（QIQA）、NIQE和Q-align IAA（QIAA）五项指标上均显著优于所有基线方法（包括WonderWorld、HunyuanWorld、Gen3C、Voyager）。
- 在人工2AFC偏好测试中，WonderZoom在‘相机变焦感’、‘视觉质量’和‘文本对齐’三个维度均被显著偏好（favor rate远高于50%），表明其生成的多尺度内容在感知质量和可控性上远超现有方法。
- 消融实验证明，移除透明度调制会导致约110倍的渲染时间增长且视觉质量下降；去除深度配准会造成显著的几何不一致；去除辅助视图合成则降低3D场景的完整性。
- Multi-Scale World Generation (8 images, 32 scenes) 上 CLIP Score (CS) = 0.3432
---

# WonderZoom: Multi-Scale 3D World Generation

> [!tip] 核心洞察
> 多尺度3D生成应遵循由粗到细的迭代范式：先构建粗尺度场景，再将其渲染结果和几何信息作为空间条件，逐步合成细尺度内容。可增量更新且保持实时渲染能力的分层3D表示是实现该范式的核心，它打破了重建范式对先验数据的依赖，使3D世界能够按需生长。

| 字段 | 内容 |
|------|------|
| 中文题名 | WonderZoom：多尺度三维世界生成 |
| 英文题名 | WonderZoom: Multi-Scale 3D World Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.09164) · [Project](https://wonderzoom.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | WonderZoom |
| Dataset | Multi-Scale World Generation |

> [!tip] 效果简介
> - Multi-Scale World Generation (8 images, 32 scenes) 上，CLIP Score (CS) 0.3432 vs 0.2687 (WonderWorld) (↑ 0.0745)；CLIP-IQA+ (CIQA) 0.7035 vs 0.5064 (WonderWorld) (↑ 0.1971)；Q-align IQA (QIQA) 3.926 vs 1.081 (WonderWorld) (↑ 2.845)。

## 概要

现有3D生成方法——无论是经典细节层次（LoD）、Mip-NeRF、分层3D高斯泼溅（Hierarchical 3DGS），还是近期单尺度场景生成工作如**WonderWorld**（Yu et al., CVPR 2025）——均建立在“所有尺度内容已知”的假设之上。这一假设天然适用于渲染或一次性重建，却无法支撑**渐进式多尺度生成**：当场景需要从宏观景观动态生长至微观细节时，现有3D表示既不能增量添加新尺度内容，也无法在更新过程中保持实时渲染。结果，已有方法只能在单一尺度上生成场景，无法构建从远景到近景无缝过渡的连贯三维世界。

WonderZoom 首次打破这一瓶颈。其核心洞察是：多尺度3D生成必须遵循“由粗到细”的迭代范式——先构建粗尺度场景，再将其渲染结果与几何信息作为空间条件，逐步合成细尺度内容。支撑这一范式的关键技术是**尺度自适应高斯面元（Scale-Adaptive Gaussian Surfels）**，一种可增量更新且保持实时渲染的分层3D表示。它允许新面元直接添加而无需重新优化已有场景，并通过尺度感知透明度调制实现相邻尺度间的无缝视觉过渡。在此基础上，**渐进式细节合成器（Progressive Detail Synthesizer）** 以粗尺度3D几何为条件，依次执行超分重建、语义编辑、深度配准和辅助视图合成，迭代生成精细尺度的3D结构。

实验从定量、定性与人工偏好三个层面验证了方法的有效性。在涵盖自然、城市、水下等8种场景的测试集上，WonderZoom在CLIP分数（CS）、CLIP-IQA+（CIQA）、Q-align IQA（QIQA）、NIQE和Q-align IAA（QIAA）五项指标上均显著优于所有基线方法（Table 1）。在约200人参与的2AFC人工偏好测试中，WonderZoom在“相机变焦感”“视觉质量”和“文本对齐”三个维度均被显著偏好（Table 2）。消融实验进一步证实，透明度调制、深度配准和辅助视图合成各自对渲染效率、几何一致性与场景完整性具有决定性贡献（Figure 5–7）。

**方法定位**：WonderZoom处于3D生成、可缩放表示与交互式内容创建的交汇点。它拓展了高斯泼溅类表示在动态场景生长中的能力边界，并首次将多尺度3D生成从“重建已知数据”推进到“按需生长未知世界”的新范式。

### 问题背景：从单尺度到多尺度的三维世界生成

三维内容生成近年来取得了显著进展，尤其是以单张图像为条件重建或生成三维场景的方法，已能产出视觉质量较高的静态三维表示。然而，这些方法几乎无一例外地局限于**单一空间尺度**：它们生成的是一个固定分辨率的场景快照，用户无法像在数字地图或虚拟地球应用中那样，自由地缩放到某个区域并观察到更精细的结构。现实世界的感知是多尺度的——从宏观的地形轮廓到微观的叶片纹理，人类视觉系统天然地在不同尺度间无缝切换。将这种多尺度体验带入三维生成，意味着场景不应是“一次性”产出的静态资产，而应具备**按需生长细节**的能力。

### 现有方法的瓶颈：重建范式无法支撑渐进式生成

现有三维表示方法在多尺度问题上并非毫无建树。经典层次细节（LoD）技术、Mip-NeRF以及层次化3D Gaussian Splatting（3DGS）等方法，都提供了在不同渲染尺度下保持视觉质量的手段。然而，这些方法的共同前提是：**所有尺度的内容在优化前已经存在**。它们解决的是“如何高效渲染已知的多尺度内容”，而非“如何在生成过程中动态添加未知的新尺度内容”。换言之，它们属于**重建范式**——依赖于预先采集的多尺度观测数据，无法在渐进式生成任务中，当用户指定一个此前不存在的精细尺度时，实时地扩展场景表示并保持渲染效率。

这一瓶颈直接导致了当前三维生成方法的两个关键缺陷：其一，生成场景的细节上限受限于初始重建时的输入分辨率，无法通过后续交互来“放大”观察；其二，即使尝试对已有场景做简单的超分辨率后处理，也无法生成真正新增的语义结构（例如，从“一片树林”缩放到“某片树叶上的瓢虫”），因为缺乏将粗尺度几何信息作为空间条件来引导精细尺度合成的机制。

### 本文动机：由粗到细的迭代生成范式

WonderZoom的出发点正是打破上述重建范式的限制，将多尺度三维生成重新定义为一种**由粗到细的迭代生长过程**。其核心直觉是：多尺度三维世界不应一次性生成，而应先构建粗尺度的场景框架，再将该框架的渲染结果和几何信息作为空间锚点，逐步合成更精细尺度的内容。为实现这一范式，需要两个关键能力：（1）一个**可增量更新且保持实时渲染**的三维表示，使得新生成的精细内容可以无缝融入现有场景，而无需触发全局重优化；（2）一个**以粗尺度几何为条件的渐进式合成器**，能够根据用户指定的文本提示和相机位姿，生成几何一致、语义合理的精细尺度三维结构。WonderZoom通过尺度自适应高斯面元（Scale-Adaptive Gaussian Surfels）和渐进式细节合成器（Progressive Detail Synthesizer）分别回应了这两项需求，从而首次实现了从单张图像出发、支持交互式多尺度探索的三维世界生成。

## 核心方法与创新机理

WonderZoom 的核心创新在于将多尺度3D世界生成从“一次性重建”范式转变为“由粗到细的渐进式生成”范式。现有3D表示——无论是经典的层次化细节层次（LoD）、Mip-NeRF，还是层次化3D高斯泼溅（Hierarchical 3DGS）——均假设所有尺度的内容已知，仅适用于渲染或一次性重建，无法在渐进式生成任务中动态添加新尺度内容并保持实时渲染。这导致现有方法只能在单一尺度上生成场景，无法生成从景观到微观细节的连贯多尺度世界。WonderZoom 通过两个紧密耦合的技术槽位突破这一瓶颈：**尺度自适应高斯面元表示**和**渐进式细节合成器**。

### 尺度自适应高斯面元（Scale-Adaptive Gaussian Surfels）

这是 WonderZoom 对3D表示槽位的核心改造。传统 Gaussian surfels（如 **WonderWorld**，Yu et al., CVPR 2025）是静态的、单尺度优化的表示，不支持增量添加新内容。WonderZoom 为每个面元引入**原生尺度**（native scale）参数 $s^{\mathrm{native}}$，定义为面元创建时的深度与相机焦距之比：

$$s^{\mathrm{native}} = \frac{d^{\mathrm{native}}}{\sqrt{f_x^{\mathrm{native}} f_y^{\mathrm{native}}}}$$

这一参数化使得面元天然携带“我属于哪个尺度层级”的信息，从而支持动态增量添加——新生成的精细尺度面元可以直接追加到场景中，无需重新优化已有面元。

更关键的是跨尺度一致性槽位的改造。传统方法在渲染不同尺度时缺乏显式过渡机制，导致混叠严重。WonderZoom 提出**尺度感知透明度调制**：在渲染时，根据面元原生尺度 $s^{\mathrm{native}}$ 与当前渲染尺度 $s^{\mathrm{render}}$ 的关系，在对数空间线性插值调制不透明度 $\tilde{o} = o \cdot \alpha$：

$$\alpha = \begin{cases} 1 & \text{if no parent and } s^{\mathrm{render}} \geq s^{\mathrm{native}} \\ \frac{\log(s^{\mathrm{parent}}) - \log(s^{\mathrm{render}})}{\log(s^{\mathrm{parent}}) - \log(s^{\mathrm{native}})} & \text{if } s^{\mathrm{parent}} \geq s^{\mathrm{render}} \geq s^{\mathrm{native}} \\ \frac{\log(s^{\mathrm{render}}) - \log(s^{\mathrm{child}})}{\log(s^{\mathrm{native}}) - \log(s^{\mathrm{child}})} & \text{if } s^{\mathrm{native}} \geq s^{\mathrm{render}} \geq s^{\mathrm{child}} \\ 1 & \text{if no child and } s^{\mathrm{render}} \leq s^{\mathrm{native}} \\ 0 & \text{otherwise} \end{cases}$$

该调制满足**无缝尺度过渡性质**（Proposition 1）：位于同一3D位置但属于相邻尺度的两个面元，其调制后不透明度之和恒为1，即 $\alpha_k(s^{\mathrm{render}}) + \alpha_j(s^{\mathrm{render}}) = 1$。这确保了缩放过程中视觉上无跳变，相邻尺度间实现连续淡入淡出。消融实验证实，移除该调制会导致渲染时间从约10ms激增至约1.1s（约110倍），且因混叠导致视觉质量下降（Figure 5; Table 3）。

### 渐进式细节合成器（Progressive Detail Synthesizer）

这是 WonderZoom 对精细尺度合成槽位的改造。传统方法（如 **HunyuanWorld** 的mesh表示或 **Gen3C** 的相机控制视频生成）只能做单尺度生成或简单的超分辨率，无法在变焦时生成全新的3D结构。WonderZoom 的渐进式细节合成器以粗尺度3D几何为空间条件，通过四步迭代生成精细尺度内容：

1. **新尺度图像合成**：将粗尺度场景渲染到目标相机位姿，经超分重建后，再通过语义编辑（根据用户提示）生成包含新细节的图像。
2. **尺度一致的深度配准**：以粗尺度渲染深度为目标，通过仅在已知几何区域施加监督的损失函数微调单目深度估计器，使其预测深度与已有几何对齐，同时保持对新区域的泛化能力。
3. **辅助视图合成**：利用相机控制视频扩散模型，以部分场景渲染结果为条件帧，生成目标尺度下的相邻视图，为构建完整3D场景提供多视角信息。
4. **面元优化**：基于合成图像和配准深度，优化新面元的透明度、朝向和尺度，使用光度损失 $\mathcal{L} = 0.8 L_1 + 0.2 L_{\mathrm{D-SSIM}}$。

消融实验表明，去除深度配准会导致新生成内容的估计深度与粗尺度几何不一致，产生明显的几何错位和漂浮伪影（Figure 6）；去除辅助视图合成则导致新尺度3D场景不完整，仅包含单个视点的内容，无法支持自由视角渲染（Figure 7）。

### 创新总结

WonderZoom 的本质洞察是：**多尺度3D生成应遵循由粗到细的迭代范式**——先构建粗尺度场景，再将其渲染结果和几何信息作为空间条件，逐步合成细尺度内容。可增量更新且保持实时渲染能力的分层3D表示是实现该范式的核心，它打破了重建范式对先验数据的依赖，使3D世界能够按需生长。两个 changed slots 的协同作用体现在：尺度自适应高斯面元解决了“如何表示和渲染动态增长的多尺度内容”，渐进式细节合成器解决了“如何生成这些新内容并保持几何一致性”。

WonderZoom 的整体流程遵循“由粗到细”的迭代生成范式，其核心是一条以 **尺度自适应高斯面元 (Scale-Adaptive Gaussian Surfels)** 为表示主干、以 **渐进式细节合成器 (Progressive Detail Synthesizer)** 为内容生长引擎的双模块管线（Figure 2）。

![[assets/figures/papers/paper_list_l2631_https_arxiv_org_abs_2512_09164/figures/002_Figure_2.jpg]]
*Figure 2: WonderZoom overview. From an input image, we first reconstruct an initialized 3D scene. Users specify prompts and camera viewpoints to generate finer-scale content. Our progressive detail synthesizer creates new-scale images, registers depth to maintain geometric consistency, and synthesizes auxiliary views for complete 3D scene creation. Our scale-adaptive Gaussian surfels enable dynamic updates without re-optimization, seamlessly integrating new content while preserving real-time rendering*

**输入与初始化。** 系统接收单张 RGB 图像作为输入，首先重建一个粗尺度的 3D 场景 $\mathcal{E}_0$，该场景由尺度自适应高斯面元表示，并关联一个初始的原生尺度层级。用户随后可通过指定文本提示和相机位姿 $\mathbf{C}_i \in \mathbb{R}^{4 \times 4}$ 来指示系统在特定空间区域生成更精细尺度的内容。

**渐进式细节合成器。** 当用户触发变焦生成时，渐进式细节合成器接管新尺度内容的创建，其内部包含四个有序子步骤：

1. **新尺度图像合成**：从当前粗尺度场景渲染观测视图，经由超分重建与语义编辑两阶段处理，生成包含新细节的目标图像。
2. **尺度一致的深度配准**：以粗尺度几何提供的目标深度 $\mathbf{D}_i^{\text{target}}$ 作为监督信号，在已知区域微调单目深度估计器 $\mathcal{D}_\theta$，使其预测深度与已有几何对齐，同时保持对新区域的泛化能力；损失函数仅在有效深度区域上计算（mask $m(u,v)$ 指示深度是否已定义）。
3. **辅助视图合成**：利用相机控制视频扩散模型，以当前部分场景 $\bar{\mathcal{E}}_i^{\text{partial}}$ 的渲染帧 $\{\text{render}(\bar{\mathcal{E}}_i^{\text{partial}}, \mathbf{C}_i^k)\}_{k=1}^K$ 作为条件，合成相邻视角的观测，为构建完整 3D 场景提供多视图约束。
4. **面元优化**：基于合成图像与配准深度，通过光度损失 $\mathcal{L} = 0.8 L_1 + 0.2 L_{\text{D-SSIM}}$ 优化新面元的透明度、朝向和尺度参数。

**尺度自适应高斯面元。** 这是整个框架的表示核心，其关键设计在于每个面元携带一个 **原生尺度** $s^{\text{native}} = d^{\text{native}} / \sqrt{f_x^{\text{native}} f_y^{\text{native}}}$，记录面元创建时的深度与相机焦距信息。渲染时，面元的不透明度 $\tilde{o} = o \cdot \alpha$ 由尺度感知调制因子 $\alpha$ 控制：$\alpha$ 根据当前渲染尺度 $s^{\text{render}}$ 与面元原生尺度及其相邻层级尺度（父尺度 $s^{\text{parent}}$、子尺度 $s^{\text{child}}$）的对数空间插值计算。这一设计保证了两个核心性质：(i) 新面元可增量添加到场景中而无需重新优化已有面元；(ii) 相邻尺度的面元在过渡区间满足 $\alpha_k(s^{\text{render}}) + \alpha_j(s^{\text{render}}) = 1$（Proposition 1），确保缩放过程中视觉上无跳变。

**输出与迭代。** 新生成的精细尺度面元被直接追加到现有场景表示中，场景 $\mathcal{E}$ 随之动态生长。整个过程可被重复执行，用户可继续向更微观的尺度深入，形成从宏观景观到微观细节的连续多尺度 3D 世界。渲染全程保持实时性能——单帧渲染时间约 10 ms 量级。

WonderZoom 的多尺度三维世界生成能力建立在两个紧密协作的核心模块之上：**尺度自适应高斯面元（Scale-Adaptive Gaussian Surfels）** 作为底层表示，提供可增量扩展且保持实时渲染的3D载体；**渐进式细节合成器（Progressive Detail Synthesizer）** 作为上层生成引擎，以粗尺度几何为条件，按需合成更精细尺度的图像与几何结构。以下逐一展开其关键设计与公式。

---

### 尺度自适应高斯面元

传统高斯面元（Gaussian surfels）在单一尺度上优化，无法表达跨尺度的内容变化。WonderZoom 对其核心改造在于为每个面元引入**原生尺度（native scale）** 参数 $s^{\mathrm{native}}$，定义为面元创建时刻的深度与相机焦距之比：

$$s^{\mathrm{native}} = \frac{d^{\mathrm{native}}}{\sqrt{f_x^{\mathrm{native}} f_y^{\mathrm{native}}}}$$

其中 $d^{\mathrm{native}}$ 为面元创建时的深度，$f_x^{\mathrm{native}}$、$f_y^{\mathrm{native}}$ 为对应相机的焦距。这一参数将面元与其“所属”的尺度层级绑定，为后续的尺度感知渲染提供了锚点。

**增量更新机制**：当用户缩放到新尺度时，渐进式细节合成器生成新的面元，直接追加到现有场景表示中，无需对已有面元进行重新优化。这打破了传统3D重建范式“所有尺度内容已知”的假设，使3D世界能够按需生长。

**尺度感知透明度调制**：渲染时，面元的原始不透明度 $o$ 被调制成 $\tilde{o} = o \cdot \alpha$，其中调制因子 $\alpha$ 根据当前渲染尺度 $s^{\mathrm{render}}$ 与面元原生尺度 $s^{\mathrm{native}}$ 的关系动态计算：

$$\alpha = \begin{cases} 
1 & \text{若无父尺度且 } s^{\mathrm{render}} \geq s^{\mathrm{native}} \\[4pt]
\dfrac{\log(s^{\mathrm{parent}}) - \log(s^{\mathrm{render}})}{\log(s^{\mathrm{parent}}) - \log(s^{\mathrm{native}})} & \text{若 } s^{\mathrm{parent}} \geq s^{\mathrm{render}} \geq s^{\mathrm{native}} \\[8pt]
\dfrac{\log(s^{\mathrm{render}}) - \log(s^{\mathrm{child}})}{\log(s^{\mathrm{native}}) - \log(s^{\mathrm{child}})} & \text{若 } s^{\mathrm{native}} \geq s^{\mathrm{render}} \geq s^{\mathrm{child}} \\[8pt]
1 & \text{若无子尺度且 } s^{\mathrm{render}} \leq s^{\mathrm{native}} \\[4pt]
0 & \text{其他情况}
\end{cases}$$

该设计的核心洞察在于：在相邻尺度的过渡区间内，通过对数空间的线性插值，使粗尺度面元逐渐淡出、细尺度面元逐渐淡入。这一机制具有**无缝尺度过渡性质（Proposition 1）**——对于位于同一3D位置但属于相邻尺度的两个面元 $k$ 和 $j$，其调制后不透明度之和恒为1：

$$\alpha_k(s^{\mathrm{render}}) + \alpha_j(s^{\mathrm{render}}) = 1$$

这确保了缩放过程中视觉上无跳变，从数学上保证了跨尺度渲染的连续性。

---

### 渐进式细节合成器

该模块负责在给定用户文本提示和新相机位姿 $\mathbf{C}_i \in \mathbb{R}^{4 \times 4}$ 的条件下，生成更精细尺度的3D内容。其流程分为四个子步骤：

**（1）新尺度图像合成**：首先将粗尺度场景渲染到目标视角，然后通过超分辨率重建提升分辨率，再结合文本提示进行语义编辑，生成包含新细节的图像 $\mathbf{I}_i$。

**（2）尺度一致的深度配准**：新图像的深度估计必须与粗尺度几何保持一致。方法是将粗尺度几何渲染得到的目标深度 $\mathbf{D}_i^{\mathrm{target}}$ 作为监督信号，仅对已知区域微调单目深度估计器 $\mathcal{D}_\theta$：

$$\mathcal{L}_{\mathrm{depth}} = \frac{\sum_{u,v} \| \mathbf{D}_i^{\mathrm{target}}(u,v) - \mathcal{D}_\theta(\mathbf{I}_i)(u,v) \| \cdot m(u,v) }{\sum_{u,v} m(u,v)}$$

其中 $m(u,v)$ 为掩码，仅标记粗尺度几何覆盖的有效像素。这种“部分监督”策略使深度估计器在已知区域对齐几何，同时在新区域保持泛化能力。此外，还使用 SAM 生成的分割掩码进行分块深度对齐，以纠正局部深度不一致。

**（3）辅助视图合成**：单张新尺度图像不足以构建完整的3D场景。方法利用相机控制的视频扩散模型，以部分场景的渲染帧 $\{\mathbf{O}_i^k\}$ 为条件，生成相邻视角的辅助视图，从而获得多视角覆盖。

**（4）面元优化**：基于合成图像和配准深度，优化新面元的透明度、朝向和尺度，使用结合 L1 损失和结构相似性损失的光度损失函数：

$$\mathcal{L} = 0.8 L_1 + 0.2 L_{\mathrm{D-SSIM}}$$

优化完成后，新面元被追加到尺度自适应高斯面元表示中，完成一次精细尺度的生长。

## 实验与关键发现

### 1. 实验设置

**测试基准与数据**。由于多尺度三维世界生成是一个新任务，尚无标准基准，作者构建了包含8张输入图像（涵盖自然、城市、水下等多种场景）的测试集，每张图像生成4个变焦层级，共32个多尺度场景。所有对比方法使用相同的固定相机路径和文本提示，确保条件对等。

**评估指标**。定量评估采用五项指标：CLIP Score（CS）衡量文本-图像对齐度；CLIP-IQA+（CIQA）和Q-align IQA（QIQA）评估无参考图像质量；NIQE衡量自然图像统计距离（越低越好）；Q-align IAA（QIAA）评估美学质量。此外，通过Prolific平台全球招募参与者（每对比约200人），进行三项维度的2AFC偏好测试：相机变焦感（Zoom feeling）、视觉质量（Visual quality）和文本对齐（Text alignment），问卷中方法的左右顺序随机化以消除偏差。

**基线方法**。对比了四类代表性方法：**WonderWorld**（Yu et al., CVPR 2025）为单尺度3D场景生成基线（Gaussian surfels表示）；**HunyuanWorld**（HunyuanWorld Team, arXiv 2025）为单尺度3D场景生成基线（mesh表示）；**Gen3C**（Ren et al., CVPR 2025）为相机控制视频生成基线；**Voyager**（Huang et al., arXiv 2025）为可探索3D场景视频生成基线。需注意，这些基线方法原本并非为多尺度生成设计，其在大变焦倍率下输出模糊是表示能力的内在局限，但这一设置恰好突出了所提方法在解决多尺度生成问题上的必要性。

---

### 2. 主要定量结果

**Table 1** 报告了所有方法在32个多尺度场景上的定量对比。WonderZoom在全部五项指标上均显著优于所有基线方法：

| 指标 | WonderZoom | WonderWorld（最佳基线） | 提升幅度 |
|------|-----------|----------------------|---------|
| CLIP Score ↑ | 0.3432 | 0.2687 | +0.0745 |
| CLIP-IQA+ ↑ | 0.7035 | 0.5064 | +0.1971 |
| Q-align IQA ↑ | 3.926 | 1.081 | +2.845 |
| NIQE ↓ | 3.695 | 21.74 | -18.045 |
| Q-align IAA ↑ | 2.986 | 1.339 | +1.647 |

值得注意的是，NIQE指标上WonderZoom（3.695）相比WonderWorld（21.74）降低了18.045，表明生成图像的自然度远超基线。在生成效率方面，WonderZoom单次新尺度场景生成耗时约9.3秒，与单尺度方法WonderWorld相当，验证了尺度自适应高斯面元在保持实时渲染能力（约10ms/帧）的同时，并未引入显著的额外计算开销。

---

### 3. 用户偏好研究

**Table 2** 展示了2AFC人工偏好测试结果。WonderZoom在三个评价维度上均被显著偏好（favor rate远高于50%的随机水平）：

- **相机变焦感**：用户明显更偏好WonderZoom生成的连续缩放体验，这直接验证了尺度感知透明度调制机制（Proposition 1）在消除跨尺度视觉跳变方面的有效性。
- **视觉质量**：WonderZoom生成的多尺度内容在清晰度和细节丰富度上远超基线，这与定量指标中CLIP-IQA+和NIQE的大幅领先一致。
- **文本对齐**：用户认为WonderZoom生成的内容更准确地反映了输入的文本提示，表明渐进式细节合成器中的语义编辑步骤有效实现了可控的精细尺度内容生成。

---

### 4. 消融实验

通过系统的组件消融，验证了三个核心设计的关键作用：

**尺度感知透明度调制（Figure 5; Table 3）**。移除透明度调制（Ours w/o mod）后，渲染时需要计算所有尺度的面元，导致渲染时间从约10ms急剧增加到约1.1s（约110倍增长），且由于不同尺度面元混叠，视觉质量显著下降。这证明了基于原生尺度的对数空间插值调制是实现实时多尺度渲染的关键使能技术。

**深度配准（Figure 6）**。去除深度配准步骤（Ours w/o depth registration）后，新生成图像的估计深度与粗尺度几何产生明显偏差，导致渲染结果中出现几何错位和漂浮伪影。这表明仅靠单目深度估计无法保证跨尺度几何一致性，必须通过对已知区域施加显式对齐约束来微调深度估计器。

**辅助视图合成（Figure 7）**。去除辅助视图合成（Ours w/o auxiliary views）后，新尺度3D场景仅包含单个视点的内容，无法支持自由视角渲染，场景完整性严重受损。这验证了利用相机控制视频扩散模型生成相邻视图对于构建完整3D表示的必要性。

---

### 5. 失败模式分析

**Figure 13** 展示了WonderZoom的典型失败案例。当用户连续缩放至纯纹理区域（如密集树枝内部）时，当前尺度图像不再包含可辨识的语义线索（如独立的枝干或叶片），导致渐进式细节合成器无法推断下一尺度应生成的内容。此时场景塌缩为无意义的纹理图案，无法继续多尺度生成。这是依赖语义驱动渐进合成所固有的局限——当语义信号消失时，系统缺乏纹理级先验或程序化生成能力来维持多尺度扩展。

---

### 6. 局限性

1. **语义依赖瓶颈**：如失败案例所示，当缩放至纯纹理区域时，方法无法继续生成有意义的精细结构，这是语义驱动范式的系统性局限。
2. **累积计算开销**：虽然单次新尺度生成耗时约9.3秒（与单尺度方法相当），但多次逐步变焦的总耗时可能较大，且非实时，限制了交互式探索的流畅性。
3. **多模型依赖**：方法需要调用多个现成模型（超分、视频扩散、深度估计）和优化过程，系统复杂度较高，可能影响鲁棒性和部署便捷性。

### 补充图表

![[assets/figures/papers/paper_list_l2631_https_arxiv_org_abs_2512_09164/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison. “CS” denotes CLIP score, “CIQA” denotes CLIP-IQA+, “QIQA” denotes Q-align IQA, “QIAA” denotes Q-align IAA, and “Time” measures the time used in generating a new-scale scene*

![[assets/figures/papers/paper_list_l2631_https_arxiv_org_abs_2512_09164/figures/007_Figure_5.jpg]]
*Figure 5: Ablation on the opacity modulation*

![[assets/figures/papers/paper_list_l2631_https_arxiv_org_abs_2512_09164/figures/008_Figure_6.jpg]]
*Figure 6: Ablation study on our depth registration*

![[assets/figures/papers/paper_list_l2631_https_arxiv_org_abs_2512_09164/figures/009_Figure_7.jpg]]
*Figure 7: Ablation study on auxiliary view synthesis*

![[assets/figures/papers/paper_list_l2631_https_arxiv_org_abs_2512_09164/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of WonderZoom with baselines on multi-scale 3D world generation*

## 定位与知识库关联

### 核心问题定位：从“重建多尺度”到“生成多尺度”

WonderZoom 的根本贡献在于将多尺度 3D 表示从**重建范式**推向**生成范式**。现有方法——无论是经典的离散层次细节（LoD）、连续尺度表示（如 **Mip-NeRF** (Barron et al., ICCV 2021)）、还是层次化 3D Gaussian Splatting——均假设所有尺度的 3D 内容在优化前已经存在。它们解决的是“如何高效存储和渲染已知的多尺度内容”，而非“如何在生成过程中动态创造尚不存在的精细尺度结构”。这一假设在渐进式生成场景下完全失效：当用户从未见过的区域放大时，系统需要凭空合成新的几何与纹理，而现有表示无法在不破坏已有场景的前提下增量添加新内容。

WonderZoom 识别出这一瓶颈的因果本质：**缺乏可增量更新且保持实时渲染的分层 3D 表示**，是多尺度 3D 生成无法实现的核心障碍。其解决方案遵循“由粗到细迭代生成”的范式——先构建粗尺度场景，再将其渲染结果和几何信息作为空间条件，逐步合成细尺度内容。这一范式将多尺度生成问题分解为两个可解的子问题：表示层的动态扩展（尺度自适应 Gaussian Surfels）和内容层的条件合成（渐进式细节合成器）。

### 与单尺度 3D 生成基线的关系

WonderZoom 的直接对比基线是单尺度 3D 场景生成方法。**WonderWorld** (Yu et al., CVPR 2025) 使用 Gaussian surfels 从单张图像生成可探索的 3D 场景，但其表示是静态的，不支持多尺度扩展——当相机大幅推进时，场景仅呈现模糊的放大纹理，无法生成新的细节。**HunyuanWorld** (HunyuanWorld Team, arXiv 2025) 采用 mesh 表示，同样局限于单一尺度。WonderZoom 在这两类表示上的显著优势（Table 1 中 CLIP-IQA+ 从 0.5064 提升至 0.7035，NIQE 从 21.74 降至 3.695）并非简单的“质量更好”，而是反映了**表示能力的代际差异**：静态单尺度表示在极端变焦下必然失效，而尺度自适应表示通过动态内容注入从根本上解决了这一问题。

与相机控制视频生成方法（如 **Gen3C** (Ren et al., CVPR 2025) 和 **Voyager** (Huang et al., arXiv 2025)）的对比则揭示了 3D 一致性在多尺度生成中的关键作用。视频生成模型可以产生视觉上连贯的变焦序列，但缺乏显式的 3D 几何约束，导致跨视角渲染时出现结构不一致。WonderZoom 在 Q-align IQA 上达到 3.926，而视频基线最高仅 1.081，这一巨大差距（↑ 2.845）表明：**多尺度生成的评估不能仅依赖单视图质量，3D 几何一致性是感知质量的决定性因素**。

### 方法谱系中的技术锚点

WonderZoom 的技术架构可定位于三个交叉领域：

**1. 3D Gaussian Splatting 的扩展谱系。** 3DGS 自提出以来经历了从静态场景到动态场景、从重建到生成的演化。WonderZoom 的尺度自适应 Gaussian surfels 在 3DGS 谱系中引入了一个新维度：**尺度感知的表示与渲染**。其核心创新——为每个面元定义原生尺度 $s^{\mathrm{native}}$ 并通过对数空间线性插值调制不透明度——可视为将 Mip-NeRF 的尺度感知思想从神经辐射场迁移到显式点云表示，但关键区别在于：Mip-NeRF 的尺度感知服务于反走样渲染，而 WonderZoom 的尺度感知服务于**跨尺度内容的无缝过渡**。Proposition 1 证明相邻尺度面元的不透明度之和恒为 1（$\alpha_k(s^{\mathrm{render}}) + \alpha_j(s^{\mathrm{render}}) = 1$），这一性质保证了缩放过程中不会出现内容的突然出现或消失——这是多尺度 3D 生成独有的需求，在纯重建任务中并不存在。

**2. 渐进式 3D 生成。** 与一次性生成完整场景的方法不同，WonderZoom 采用迭代式生成策略，每次变焦仅生成当前所需的精细尺度内容。这一设计借鉴了渐进式图像生成（如渐进式 GAN）的思想，但在 3D 领域面临独特挑战：如何保证新生成内容与已有粗尺度几何的一致性。WonderZoom 的深度配准损失 $\mathcal{L}_{\mathrm{depth}}$ 通过仅在粗尺度几何已知区域施加监督，微调单目深度估计器，使其在保持对新区域泛化能力的同时，与已有几何对齐。消融实验（Figure 6）证明，去除深度配准会导致显著的几何错位和漂浮伪影，验证了这一机制的必要性。

**3. 多模型编排与 3D 场景合成。** WonderZoom 的渐进式细节合成器编排了多个现成模型：超分辨率重建、语义编辑、深度估计、相机控制视频扩散。这种“模型编排”策略在 3D 生成领域日益常见（如 DreamFusion 使用 2D 扩散模型优化 3D 表示），但 WonderZoom 的独特之处在于其编排服务于**空间条件化**——粗尺度渲染结果和深度信息作为空间锚点，引导精细尺度内容的生成位置和几何结构。辅助视图合成模块利用相机控制视频扩散模型生成相邻视角，将单视图生成扩展为完整的 3D 场景，消融实验（Figure 7）表明去除该模块会导致场景不完整，无法支持自由视角渲染。

### 适用边界与失效模式

WonderZoom 的适用边界由其核心假设决定：**精细尺度内容可以通过语义条件从粗尺度观测中推断**。这一假设在场景具有明确语义结构时成立——例如从建筑全景放大到窗户细节，或从森林远景放大到树干纹理。然而，当语义线索消失时，方法会系统性失效。论文明确报告的失败案例（Figure 13）是：当连续放大至密集树枝内部时，图像不再包含可识别的语义结构（如独立的枝干或叶片），导致方法无法推断下一尺度应生成的内容，场景塌缩为无意义的纹理图案。

这一失效模式揭示了方法的深层局限：**语义驱动的渐进合成无法处理纯纹理或随机结构区域**。这是当前生成范式固有的边界——扩散模型和深度估计器都依赖语义先验，当输入退化为无结构纹理时，所有下游模块都会失效。突破这一边界需要引入纹理级先验或程序化生成机制，这超出了当前框架的能力范围。

此外，方法对深度估计精度的依赖构成了另一适用边界。原生尺度定义 $s^{\mathrm{native}} = d^{\mathrm{native}} / \sqrt{f_x^{\mathrm{native}} f_y^{\mathrm{native}}}$ 直接依赖于创建面元时的深度估计 $d^{\mathrm{native}}$。在复杂几何（如细长结构、透明表面）或极端变焦下，深度估计误差会被放大，导致面元尺度标注错误，进而破坏尺度感知渲染的平滑过渡性质。论文未报告在这些极端条件下的鲁棒性评估，这一边界需要进一步验证。

### 局限与开放问题

**已知局限：**

1. **语义枯竭导致的生成塌缩。** 如前所述，当连续缩放至纯纹理区域时，方法无法继续多尺度生成。这是语义驱动范式的根本局限，不是简单的工程改进可以解决。

2. **计算效率的累积成本。** 虽然单次新尺度生成耗时约 9.3 秒（与单尺度方法相当），但多次逐步变焦的总耗时线性增长。方法依赖多个现成模型的串行调用（超分、深度估计、视频扩散、面元优化），每次变焦都需要完整的推理管线，不支持实时交互式探索。

3. **单区域串行探索。** 当前方法假设用户每次仅放大一个区域，不支持同时探索多个分支区域或在不同尺度间自由跳转。这限制了交互式探索的灵活性。

**开放问题：**

1. **超越语义驱动的多尺度生成。** 当语义线索消失时，如何引入纹理级先验（如纹理合成、程序化生成）或自监督的几何先验来维持多尺度生成？这是将方法从“语义结构缩放”扩展到“任意材质缩放”的关键挑战。

2. **端到端可训练的统一框架。** 当前的多模型编排策略虽然灵活，但引入了模块间的误差累积和调优复杂度。能否设计端到端可训练的框架，将超分、深度估计、视图合成统一为单一模型，减少对外部模型的依赖并提高生成的一致性与效率？

3. **动态场景与多区域探索。** 如何将多尺度生成能力扩展到包含运动物体的动态场景？如何支持用户同时探索多个区域，或在尺度间自由跳转而无需重新生成？这需要表示层支持时间维度和空间分支结构。

4. **深度估计鲁棒性。** 在复杂几何和极端变焦下，当前依赖单目深度估计的尺度定义可能失效。能否通过多视图几何约束或尺度自校准机制提高鲁棒性？这是保证方法在任意场景下可靠运行的前提。

### 知识库定位总结

WonderZoom 在 3D 生成领域的知识库中占据了一个此前空白的生态位：**多尺度 3D 世界生成**。它桥接了三个此前相对独立的研究方向——3D Gaussian Splatting 的表示设计、渐进式 3D 生成、以及多模型编排的 3D 场景合成——并通过“由粗到细迭代生成”的统一范式将它们整合。其核心知识贡献不是单一技术的突破，而是**识别出多尺度生成需要可增量更新的尺度感知表示**这一因果瓶颈，并提供了完整的解决方案。后续工作的自然延伸方向包括：突破语义依赖的生成边界、提高计算效率以支持实时交互、以及扩展到时序和空间分支维度。

## 原文 PDF

![[paperPDFs/CVPR_2026/WonderZoom_Multi_Scale_3D_World_Generation.pdf]]
