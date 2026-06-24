---
title: "HumanRAM: Feed-forward Human Reconstruction and Animation Model using Transformers"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/HumanRAM_Feed_forward_Human_Reconstruction_and_Animation_Model_using_Transformers.pdf
project_link: "https://zju3dv.github.io/humanram/"
code_link: null
aliases:
- HumanRAM
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在LVSM框架中额外注入基于共享SMPL-X神经纹理的姿态图像作为输入/目标Token，同时将线性解码器替换为DPT解码器。
primary_logic: 将SMPL-X神经纹理光栅化到输入/目标视图，为Transformer自注意力提供显式的跨视图/跨姿态对应关系，从而在单次前馈中同时实现高质量重建和姿态可控的动画。
claims:
- 引入显式SMPL-X神经纹理姿态条件到LRM中，统一人体重建与动画任务
- 在THuman2.1上PSNR达到30.34 dB，比LVSM基线（28.24 dB）提升2.10 dB，验证了姿态条件带来的显著增益
- 在ActorsHQ真实数据上零样本泛化，PSNR达25.47 dB，远超LVSM的20.25 dB，证明姿态对应带来的泛化优势
- 消融实验显示，姿态图像与DPT解码器组合带来最佳性能（PSNR 30.34），移除任一组件均导致质量下降
---

# HumanRAM: Feed-forward Human Reconstruction and Animation Model using Transformers

> [!tip] 核心洞察
> 将SMPL-X神经纹理光栅化到输入/目标视图，为Transformer自注意力提供显式的跨视图/跨姿态对应关系，从而在单次前馈中同时实现高质量重建和姿态可控的动画。

| 字段 | 内容 |
|------|------|
| 中文题名 | HumanRAM：基于Transformer的前馈式人体重建与动画模型 |
| 英文题名 | HumanRAM: Feed-forward Human Reconstruction and Animation Model using Transformers |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](http://arxiv.org/abs/2506.03118v1) · [Project](https://zju3dv.github.io/humanram/) · [arXiv](https://arxiv.org/abs/2407.08414) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HumanRAM |
| Dataset | THuman2.1, Human4DiT, ActorsHQ |

> [!tip] 效果简介
> - THuman2.1 上，PSNR↑ 30.34 vs 28.24 (LVSM) (+2.10)；SSIM↑ 0.9535 vs 0.9396 (LVSM) (+0.0139)；LPIPS↓ 0.0184 vs 0.0226 (LVSM) (-0.0042)。
> - Human4DiT 上，PSNR↑ 26.35 vs 25.56 (LVSM) (+0.79)。
> - ActorsHQ (reconstruction) 上，PSNR↑ 25.47 vs 20.25 (LVSM) (+5.22)。

## 概要

现有基于Transformer的大规模人体重建模型（如LVSM）缺乏显式的人体姿态先验，导致在稀疏视图和复杂姿态下难以捕获精细几何与纹理，且线性解码器易产生块状伪影，同时不支持动画任务。本文提出**HumanRAM**——一种统一人体重建与动画的前馈式模型。其核心思路是在LVSM框架中注入由共享SMPL-X神经纹理光栅化得到的姿态图像，作为输入与目标Token的显式姿态条件；同时将线性解码器替换为DPT-based解码器，利用Transformer中间层特征合成目标视图。该设计使自注意力机制能够建立跨视图、跨姿态的显式对应关系，从而在单次前馈中同时实现高质量新视角合成和姿态可控的动画。

在THuman2.1上，HumanRAM的PSNR达到30.34 dB，较LVSM基线（28.24 dB）提升2.10 dB；在ActorsHQ真实数据上零样本泛化时，PSNR达25.47 dB，远超LVSM的20.25 dB，验证了姿态条件带来的显著泛化优势。消融实验表明，姿态图像与DPT解码器的组合是实现最佳性能的关键。方法定位于类LRM重建范式的延续，兼具泛化性人体重建与动画能力。

## 核心方法与创新机理

### 瓶颈与动机

现有基于Transformer的大规模重建模型（如LVSM）在人体重建任务中面临两个关键缺陷。其一，输入表示仅依赖RGB图像块与Plücker射线嵌入的拼接，缺乏显式的人体姿态先验，导致Transformer自注意力在稀疏视图和复杂姿态下难以建立跨视图的几何对应关系，重建质量受限。其二，LVSM使用线性全连接层直接回归目标视图的RGB值，这种全局操作缺乏局部信息融合能力，容易在渲染结果中产生明显的块状伪影（checkerboard artifacts）。更根本的是，LVSM架构本身不支持姿态驱动的动画合成，无法在单次前馈中同时完成重建与动画任务。

### 核心创新：显式姿态条件注入与DPT解码

HumanRAM的核心创新在于将人体重建与动画统一到同一个前馈框架中，其关键机制可归结为两个互补的设计。

**第一，基于SMPL-X神经纹理的显式姿态条件。** HumanRAM在LVSM的输入/目标Token构造中额外注入姿态图像（Pose Image），该姿态图像通过将共享的三平面神经纹理（triplane neural texture）绑定到SMPL-X几何代理并光栅化到对应视图得到。具体而言，对于标准SMPL-X空间的每个顶点$\mathbf{v}$，通过三平面双线性插值采样获得神经纹理特征：

$$\mathbf{F}(\mathbf{v}; \mathbf{T}) = [\mathrm{BLerp}(\mathbf{v}^{xy}; \mathbf{T}^{xy}), \mathrm{BLerp}(\mathbf{v}^{xz}; \mathbf{T}^{xz}), \mathrm{BLerp}(\mathbf{v}^{yz}; \mathbf{T}^{yz})] \in \mathbb{R}^{3C}$$

随后将该特征作为顶点颜色光栅化到给定视图，生成姿态图像$\mathbf{F}_{ij}$。输入Token构造由原始的RGB+Plücker拼接扩展为三元组拼接：

$$\mathbf{x}_{ij} = \mathrm{Linear}_{\mathrm{inp}}([\mathbf{I}_{ij}, \mathbf{P}_{ij}, \mathbf{F}_{ij}])$$

目标Token同样纳入姿态信息（重建时使用目标视图的对应姿态图像，动画时使用新目标姿态驱动的SMPL-X光栅化结果）：

$$\mathbf{q}_j^{\mathrm{recon}} = \mathrm{Linear}_{\mathrm{tar}}([\mathbf{P}_j^t, \mathbf{F}_j^t])$$

这一设计的核心洞察在于：姿态图像为Transformer自注意力提供了显式的跨视图/跨姿态对应关系——不同视图下SMPL-X表面同一语义区域在姿态图像中具有相似的特征表达，使得注意力机制能够更有效地聚合相关区域的图像信息，从而在稀疏输入和复杂姿态下仍能捕获精细几何与纹理。

**第二，DPT-based解码器替代线性层。** HumanRAM将LVSM的线性输出层替换为类似DPT（Dense Prediction Transformer）的残差CNN解码器，汇集Transformer第3、6、9、12层的中间目标Token：

$$\hat{\mathbf{I}}^t = \mathrm{Sigmoid}(\mathrm{DPT}(\{\mathbf{y}^i | i = 3,6,9,12\}))$$

该解码器通过跳跃连接和多层卷积进行局部信息融合，有效消除了线性解码器固有的块状伪影，同时保留了Transformer的全局建模能力。

### 统一框架的关键特性

上述两个设计共同实现了重建与动画的统一：重建时，目标Token使用与输入相同姿态下的新视角参数；动画时，目标Token使用新目标姿态驱动的SMPL-X模型光栅化结果。整个过程在单次前馈中完成，无需逐场景优化或后处理。训练采用MSE损失与VGG感知损失的联合优化：

$$\mathcal{L} = \frac{1}{M} \sum_{i=1}^{M} \left( \mathcal{L}_{\mathrm{MSE}}(\hat{\mathbf{I}}_i, \mathbf{I}_i) + \lambda \cdot \mathcal{L}_{\mathrm{Perc}}(\hat{\mathbf{I}}_i, \mathbf{I}_i) \right)$$

其中$\lambda=1.0$。消融实验（Table 5）证实，姿态图像与DPT解码器的组合带来最佳性能（PSNR 30.34），移除任一组件均导致质量显著下降，验证了二者对最终效果的独立且互补的贡献。

![[assets/figures/papers/paper_list_l7_http_arxiv_org_abs_2506_03118v1/figures/012_Table_5.jpg]]
*Table 5: Ablation study on THuman2.1 [Yu et al. 2021]. We report PSNR, SSIM, and LPIPS to evaluate the contribution of proposed components and the impact of different input views*

![[assets/figures/papers/paper_list_l7_http_arxiv_org_abs_2506_03118v1/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of HumanRAM. HumanRAM adopts transformers for human reconstruction and animation from sparse view images in a feed-forward manner. We first patchify and project spare-view RGB images and their corresponding Plücker rays and pose images into input tokens through a linear layer. The pose images are acquired by rasterizing the SMPL-X neural texture onto the input views. Similarly, given the target novel view under the same or another novel pose, the target tokens are created from the target Plücker rays and pose images through another linear layer. Then both input tokens and target tokens are fed into transformer blocks. Finally, a DPT-based decoder regresses the intermediate target t...*

## 实验与关键发现

### 核心定量结果

HumanRAM 在受控合成数据与真实跨域数据上均取得一致且显著的性能提升，验证了显式姿态条件与 DPT 解码器的双重增益。

**THuman2.1 基准（Table 1）**：以 4 个均匀分布输入视图评估，HumanRAM 达到 PSNR 30.34 dB，相较基础架构 LVSM（28.24 dB）提升 **+2.10 dB**；SSIM 从 0.9396 提升至 0.9535，LPIPS 从 0.0226 降至 0.0184。在 Human4DiT 数据集上，PSNR 从 25.56 dB 提升至 26.35 dB（+0.79 dB），表明方法对不同数据源具有一定鲁棒性。

**ActorsHQ 跨域泛化（Table 2）**：所有方法直接使用预训练模型、不做微调，HumanRAM 取得 PSNR 25.47 dB，远超 LVSM 的 20.25 dB（**+5.22 dB**）。这一差距揭示出核心机理：SMPL-X 神经纹理为 Transformer 自注意力提供了跨视图的显式几何对应，使模型在未见域仍能有效匹配特征，而纯 RGB+Plücker 射线嵌入的 LVSM 在域偏移下匹配失效。

**动画任务（Table 3, Table 4）**：在 ZJU-MoCap 多视角动画设定下，HumanRAM 在 PSNR/SSIM/LPIPS 三项指标上均优于 NNA、SHERF 等专用动画基线；单视角动画设定下同样保持优势。这证明统一的姿态条件框架可同时支撑重建与动画，无需任务特定分支。

### 消融实验揭示的因果链路

Table 5 的消融实验清晰分离了各组件的贡献，形成一条完整的因果链：

| 配置 | PSNR↑ |
|------|-------|
| 仅 Position（无姿态图像，线性解码器） | 28.24 |
| + Pose Image（姿态图像，线性解码器） | 29.48 |
| + DPT（姿态图像，DPT 解码器，**即 HumanRAM**） | **30.34** |

1. **姿态图像（Pose Image）的独立增益**：在 LVSM 基线（28.24 dB）上单独引入姿态图像，PSNR 提升至 29.48 dB（+1.24 dB）。这直接验证了“显式姿态对应”这一因果旋钮的有效性——神经纹理光栅化将 SMPL-X 几何代理转化为像素空间的特征图，使自注意力能够利用跨视图的顶点级对应关系，而非仅依赖图像外观相似性。

2. **DPT 解码器的叠加增益**：在姿态图像基础上将线性解码器替换为 DPT-based 解码器，PSNR 进一步从 29.48 dB 提升至 30.34 dB（+0.86 dB）。定性结果（Fig. 8）显示，线性解码器在目标视图产生明显的块状（checkerboard）伪影，而 DPT 解码器通过汇聚 Transformer 第 3、6、9、12 层中间 token 并进行残差 CNN 融合上采样，有效消除了此类伪影，恢复更连贯的纹理细节。

3. **输入视图数量的边际效应**：当输入视图从 1 增至 4，PSNR 从 21.69 dB 跃升至 30.34 dB；但从 4 增至 8 时，PSNR 仅从 30.34 dB 提升至 32.34 dB。这表明 4 视图已能提供足够的跨视角对应信息，更多视图的增益递减，为实际部署的视图数量选择提供了依据。

### 失败模式与适用边界

**分辨率瓶颈**：当前方法针对 512×512 分辨率优化。由于 Transformer token 数量随图像分辨率二次增长，扩展到 1024×1024 或更高分辨率时面临显存和计算效率挑战。这是 LRM 类架构的共性局限，非 HumanRAM 特有，但限制了其在需要高保真面部/手部细节场景中的应用。

**时序一致性未验证**：论文仅评估了静态重建与动画的单帧质量，未涉及视频序列的时序一致性。在动画应用中，逐帧独立推理可能导致帧间闪烁，这是前馈方法相较于时序模型（如基于 3DGS 的个性化头像）的潜在劣势。

**跨域泛化仍有差距**：尽管在 ActorsHQ 上 HumanRAM 大幅领先 LVSM，但其 PSNR（25.47 dB）仍显著低于域内测试（30.34 dB），说明神经纹理学习到的姿态-外观映射对训练分布外的衣物拓扑、光照条件仍存在适应性不足。这一差距指向开放问题：如何在不牺牲前馈特性的前提下增强跨场景鲁棒性。

**依赖 SMPL-X 姿态估计**：HumanRAM 以 SMPL-X 姿态参数作为输入条件，其性能受上游姿态估计精度影响。对于严重遮挡或极端姿态，姿态估计误差会通过神经纹理光栅化传播至下游渲染，可能产生几何错位伪影。论文未对此进行敏感性分析，需在实际部署中注意。

![[assets/figures/papers/paper_list_l7_http_arxiv_org_abs_2506_03118v1/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results on ActorsHQ [Işık et al. 2023] and THuman2.1 [Yu et al. 2021]. The top two rows show the reconstruction and animation results from multi-view inputs, while the bottom two rows show the results from single-view input. The driving poses for animation are from ActorsHQ [Işık et al. 2023] and AMASS [Mahmood et al. 2019]*

![[assets/figures/papers/paper_list_l7_http_arxiv_org_abs_2506_03118v1/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison of reconstruction on ActorsHQ [Işık et al. 2023]. All methods are evaluated directly on ActorsHQ without training or finetuning*

![[assets/figures/papers/paper_list_l7_http_arxiv_org_abs_2506_03118v1/figures/010_Table_3.jpg]]
*Table 3: Quantitative comparison of multi-view animation on ZJU-MoCap [Peng et al. 2021b]. Metrics are computed on unseen subjects using the same crop manner as NNA [Gao et al. 2023]*

![[assets/figures/papers/paper_list_l7_http_arxiv_org_abs_2506_03118v1/figures/011_Table_4.jpg]]
*Table 4: Quantitative comparison of single-view animation on ZJU-MoCap [Peng et al. 2021b]. Metrics are computed on unseen poses and unseen subjects following SHERF [Hu et al. 2023b]*

## 定位与知识库关联

### 问题定位：从“通用视图合成”到“人体感知的生成式重建”

HumanRAM 的核心定位是在 **Large View Synthesis Model (LVSM)**（Jin et al., 2024）这类基于 Transformer 的大规模前馈式新视角合成模型框架内，补足其缺失的**显式人体姿态先验**。LVSM 将多视图 RGB 图像与 Plücker 射线嵌入拼接后直接送入 Transformer，依赖自注意力隐式学习跨视图对应关系。这一设计在通用物体上有效，但在人体这种高度铰接、姿态变化剧烈的对象上暴露了两个关键瓶颈：

1. **稀疏视图下的几何歧义**：当输入视图数量少（如 4 个）且姿态差异大时，纯 RGB+射线嵌入缺乏足够的跨视图匹配线索，Transformer 难以推断精细的几何结构，容易产生模糊或错误的渲染。
2. **姿态泛化与动画能力的缺失**：LVSM 仅支持“重建”（同一姿态下的新视角合成），无法处理“动画”（新姿态下的渲染），因为其输入/输出表示中完全没有姿态信息的显式编码。

HumanRAM 的因果性创新在于：**在 LVSM 的输入和目标 Token 中额外注入经由 SMPL-X 神经纹理光栅化得到的“姿态图像”（pose image）**，为 Transformer 的自注意力机制提供显式的、逐像素的跨视图/跨姿态几何对应关系。这一设计将人体重建与动画统一到同一个前馈框架中——只需改变目标 Token 中的姿态图像，即可在推理时自由切换重建与动画任务。

### 与基线方法的本质差异

| 维度 | LVSM | HumanRAM |
|------|------|----------|
| 输入表示 | RGB + Plücker 射线 | RGB + Plücker 射线 + **SMPL-X 神经纹理姿态图像** |
| 目标表示 | Plücker 射线 | Plücker 射线 + **目标姿态的姿态图像** |
| 姿态条件 | 无显式姿态编码 | 通过共享 SMPL-X 三平面神经纹理提供显式几何对应 |
| 解码器 | 线性全连接层 + Sigmoid | **DPT-based 残差 CNN 解码器**（融合第 3, 6, 9, 12 层中间 Token） |
| 动画能力 | 不支持 | 支持（替换目标姿态图像即可） |
| 跨域泛化 | 弱（ActorsHQ 上 PSNR 仅 20.25 dB） | 强（ActorsHQ 上 PSNR 达 25.47 dB，提升 5.22 dB） |

与其他人体重建方法的差异：
- **GPS-Gaussian** 和 **GHG** 等泛化性重建方法依赖显式 3D 表示（如点云或高斯椭球体），需要逐场景优化或复杂的几何推理流水线，而 HumanRAM 保持纯前馈式推理，无需任何测试时优化。
- **NNA** 和 **SHERF** 等泛化性动画方法通常需要多阶段处理（如先重建后驱动）或依赖 2D 先验，HumanRAM 则在单次前馈中同时完成重建与动画。
- **3DGS-Avatar** 等个性化动画方法需要针对每个主体进行训练，不具备泛化性，HumanRAM 在未见主体上直接推理。

### 知识库挂载点

1. **Large Reconstruction Model (LRM) 系列**：HumanRAM 直接继承 LVSM 的 Transformer 架构和分块 Token 化策略，属于 LRM 家族在人体特定领域的扩展。其“注入显式几何先验到 Token 表示”的思路可推广到其他铰接物体（如人手、动物）的 LRM 变体。

2. **SMPL-X 与神经纹理**：姿态条件的参数化方式借鉴了 **Neural Texture**（Thies et al., 2019）将纹理特征绑定到 SMPL-X 标准空间顶点的思想，但将其从“纹理映射”重新定义为“跨视图对应线索的生成器”。三平面采样（Eq. 5）提供了连续、可微的查询机制，避免了显式 3D 重建的中间步骤。

3. **DPT (Dense Prediction Transformer) 解码器**：将 Transformer 中间层特征通过跳跃连接和残差 CNN 上采样融合的设计，源自密集预测任务中的 DPT 架构。在 HumanRAM 中，这一替换直接解决了线性解码器产生的块状伪影问题（Fig. 8），说明 Transformer 中间层保留了丰富的局部空间信息，但需要合适的解码器来释放。

4. **前馈式人体动画**：与基于 NeRF 或 3DGS 的动画方法（需逐场景优化）不同，HumanRAM 展示了“姿态条件 + 前馈 Transformer”在动画任务上的可行性，为实时、泛化性人体动画提供了新的技术路线。

### 适用边界

- **输入模态**：需要稀疏/单视图 RGB 图像、对应的相机参数和 SMPL-X 姿态参数。姿态参数需由外部估计器（如现成的姿态估计网络）提供，HumanRAM 本身不解决姿态估计问题。
- **分辨率限制**：当前设计针对 512×512 分辨率优化。当分辨率提升时，Token 数量呈二次增长，对显存和计算效率构成挑战——这是 Transformer 架构在图像生成任务中的共性瓶颈，不是 HumanRAM 特有的。
- **泛化范围**：在 THuman2.1 和 Human4DiT 等室内受控数据集上表现优异，在 ActorsHQ 真实数据上展示了显著的零样本泛化能力（PSNR 25.47 dB）。但对极端姿态、严重遮挡或与训练数据服装风格差异过大的场景，效果可能下降——这一点在论文中未给出定量上限，需要实际部署时验证。
- **时序一致性**：当前模型逐帧独立推理，未考虑时序约束。对于视频输入或需要时序平滑的动画序列，可能需要额外的时序后处理或模型扩展。
- **SMPL-X 依赖**：姿态条件的有效性依赖于 SMPL-X 拟合的准确性。若输入姿态估计有显著误差，姿态图像提供的对应关系将不可靠，可能反而引入噪声——论文未对此进行鲁棒性分析。

### 后续启发

1. **高效高分辨率扩展**：当前 Token 数量的二次增长是主要瓶颈。后续工作可探索分层 Token 化、稀疏注意力或混合表示（如结合 3DGS 的显式几何缓存）来支持 1024×1024 或更高分辨率，同时保持实时推理能力。

2. **时序扩展**：将单帧推理扩展到时序序列，引入时序自注意力或光流引导的跨帧一致性约束，有望实现视频级别的人体重建与动画，并消除逐帧推理可能产生的闪烁。

3. **更丰富的条件模态**：当前仅依赖 RGB 图像和 SMPL-X 姿态。融合深度、法向或语义分割等额外模态，或引入文本描述作为外观/服装的条件信号，可进一步提升重建质量和可控性。

4. **跨域鲁棒性**：ActorsHQ 上的 5.22 dB PSNR 提升证明了姿态对应带来的泛化优势，但 25.47 dB 的绝对值仍低于室内数据集的 30.34 dB。如何进一步缩小域间差距（如通过域随机化训练、更强的数据增强或适配层）是一个开放问题。

5. **姿态估计误差的容错机制**：当前框架对姿态估计精度的依赖程度未经验证。设计对姿态噪声鲁棒的 Token 表示（如引入不确定性建模或姿态校正模块）可提升实际部署的可靠性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/HumanRAM_Feed_forward_Human_Reconstruction_and_Animation_Model_using_Transformers.pdf]]