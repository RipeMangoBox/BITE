---
title: Drivable Volumetric Avatars Using Texel-aligned Features
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Drivable_Volumetric_Avatars_Using_Texel_aligned_Features.pdf
project_link: null
code_link: null
aliases:
- DVAD
- DVAUTAF
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 纹素对齐特征（texel-aligned features）：将姿态、多视图图像和视角信号统一映射到局部UV纹理空间，为每个体积原语提供高保真、空间对齐的密集条件化，从而保留细节并增强泛化。
primary_logic: 通过将混合体积原语（MVP）附着于线性混合蒙皮（LBS）网格，并对每个原语使用其对应纹素的局部条件化（包括局部视角方向投影），DVA 同时获得了参数化模型的鲁棒先验和模型无关方法的细节捕捉能力，在稀疏驱动信号下实现真实感可驱动化身。
claims:
- "在ZJU-MoCap数据集上，DVA在PSNR上显著超越FBCA和NeuralBody（S386: 35.414 vs 32.123/33.196; S387: 30.512 vs 27.886/28.640）。"
- 局部视角条件化在未见姿态-视角组合下消除全局条件化带来的严重伪影。
- 纹素对齐特征相比瓶颈表示显著更好地保留衣物高频细节。
- DVA在稀疏多视图驾驶（2-3个视图）下在PSNR上优于LookingGood和FBCA，且对缺失信息更鲁棒。
---

# Drivable Volumetric Avatars Using Texel-aligned Features

> [!tip] 核心洞察
> 通过将混合体积原语（MVP）附着于线性混合蒙皮（LBS）网格，并对每个原语使用其对应纹素的局部条件化（包括局部视角方向投影），DVA 同时获得了参数化模型的鲁棒先验和模型无关方法的细节捕捉能力，在稀疏驱动信号下实现真实感可驱动化身。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于纹素对齐特征的可驱动体积化身 |
| 英文题名 | Drivable Volumetric Avatars Using Texel-aligned Features |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2207.09774) · [paper](http://arxiv.org/abs/2004.02460v1) |
| Topic | #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | Drivable Volumetric Avatars (DVA) |
| Dataset | ZJU-MoCap S386, ZJU-MoCap S387 |

> [!tip] 效果简介
> - ZJU-MoCap S386 (novel view synthesis) 上，PSNR 35.414 vs FBCA: 32.123 (+3.291)；PSNR 35.414 vs NeuralBody: 33.196 (+2.218)。
> - ZJU-MoCap S387 (novel view synthesis) 上，PSNR 30.512 vs FBCA: 27.886 (+2.626)；PSNR 30.512 vs NeuralBody: 28.640 (+1.872)。

## 概要

现有可驱动人体化身方法依赖全局低维参数化（如人体姿态）或低维嵌入，丢弃了大量观测细节，导致无法忠实再现衣物褶皱与动态细节；而模型无关方法缺乏结构先验，在稀疏输入下表现不佳。本文提出**可驱动体积化身（Drivable Volumetric Avatars, DVA）**，核心创新是**纹素对齐特征（texel-aligned features）**：将姿态、多视图图像和视角信号统一映射到局部UV纹理空间，为每个体积原语提供高保真、空间对齐的密集条件化。DVA将混合体积原语（MVP）附着于线性混合蒙皮（LBS）网格，同时获得参数化模型的鲁棒先验和模型无关方法的细节捕捉能力。在ZJU-MoCap数据集上，DVA的新视角合成PSNR显著超越FBCA和NeuralBody（S386: 35.414 vs 32.123/33.196）；在稀疏多视图驱动下亦优于LookingGood和FBCA。该方法定位于参数化化身与神经渲染的交汇点，以局部纹素对齐条件化替代全局瓶颈表示，解决了稀疏驱动信号下细节保留与泛化的核心矛盾。

## 核心方法与创新机理

### 问题瓶颈与设计动机

现有可驱动人体化身方法面临一个根本性矛盾：参数化方法（如基于SMPL模型的FBCA、基于姿态潜码的NeuralBody）依赖低维全局参数化或瓶颈嵌入来驱动，虽然具备结构先验带来的鲁棒性，但丢弃了大量观测细节，无法忠实再现衣物褶皱、动态光影等高频信息；而模型无关方法（如LookingGood）虽能保留细节，却缺乏人体结构先验，在稀疏多视图输入下表现脆弱。这种“鲁棒性-表达力”的权衡构成了领域核心瓶颈。

DVA的设计动机正是打破这一僵局：**能否在保留参数化模型鲁棒先验的同时，为每个局部区域注入高保真、空间对齐的密集条件信号？** 论文提出的纹素对齐特征（texel-aligned features）正是这一因果调节变量——它将姿态、多视图图像和视角信号统一映射到UV纹理空间，为附着于LBS网格的每个体积原语提供局部条件化，从而同时获得参数化方法的泛化能力和模型无关方法的细节捕捉能力。

### 核心架构与模块流程

DVA采用编码器-解码器架构（Fig. 2），输入为稀疏多视图图像、人体姿态参数θ、面部表情和视角方向，输出为附着于人体骨骼网格上的混合体积原语（Mixture of Volumetric Primitives, MVP），再通过可微分光线行进渲染为最终图像。整个流水线包含六个关键模块，按信息流动顺序为：

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2207_09774/figures/002_Figure_2.jpg]]
*Figure 2: General overview of the architecture. The core of our full-body model is a encoder-decoder architecture, which takes as input raw images, body pose, facial expression and view direction, and outputs a mixture of volumetric primitives. These are ray marched through to produce a full-body avatar*

1. **姿态编码与LBS蒙皮**：给定姿态参数θ和模板网格M，通过线性混合蒙皮（LBS）生成粗几何代理M_θ：
   $$M_{\theta} = \mathrm{LBS}(\theta, M)$$
   该网格为后续体积原语提供初始附着位置和蒙皮权重，构成参数化结构先验。

2. **纹素对齐特征提取**：这是DVA的核心创新模块。将多视图图像反投影到UV纹理空间，与局部姿态编码（基于蒙皮权重和骨骼变换）在纹素级别融合，生成空间对齐的密集特征图。该特征图保留了输入信号的空间结构，避免了瓶颈表示的信息压缩损失。

3. **运动解码分支**：以纹素对齐特征为条件，预测每个体积原语相对于LBS网格附着点的位置偏移δt_k、旋转和缩放变换。最终原语位置为：
   $$t_{k} = \delta t_{k} + \hat{t}_{k}(\pmb{\theta})$$
   其中$\hat{t}_{k}(\theta)$为LBS网格上的初始附着点。该分支使原语能在参数化先验基础上灵活调整，捕捉衣物变形等非刚性运动。

4. **不透明度/外观解码分支**：预测每个原语的透明度体积$V^\alpha$和颜色体积$V^{\mathrm{rgb}}$，包含视角相关的外观效果。

5. **阴影分支**：在纹理空间独立操作，捕捉非局部的姿态相关光照效果（如自阴影、环境光遮蔽），与外观分支输出相乘得到最终颜色场。

6. **可微分光线行进渲染**：沿每条像素光线累积颜色和透明度场，计算像素颜色：
   $$I_{p}^{\mathrm{rgb}} = \int_{t_{\mathrm{min}}}^{t_{\mathrm{max}}} V^{\mathrm{rgb}}(\mathbf{r}_{\hat{p}}(t)) \frac{d T(t)}{d t} d t$$
   其中透射率$T(t) = \int_{t_{\min}}^{t_{\max}} V^{\alpha}(\mathbf{r}_{\hat{P}}(t)) d t$沿光线从近端到远端累积不透明度。

三个解码分支均采用2D转置卷积序列，使用非共享偏置（untied biases）以保持空间对齐性。训练损失为多分量加权组合：
$$\mathcal{L} = \lambda_{\mathrm{rgb}} \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{vgg}} \mathcal{L}_{\mathrm{vgg}} + \lambda_{\mathrm{m}} \mathcal{L}_{\mathrm{m}} + \lambda_{\mathrm{vol}} \mathcal{L}_{\mathrm{vol}}$$
包含均方误差图像损失、VGG感知损失、掩码L1损失和体积先验损失（约束原语紧凑性）。

### 三个关键Changed Slots及其因果机制

**Changed Slot 1：底层表示——从纹理网格到混合体积原语（MVP）**

FBCA等方法将化身表示为带纹理的三角网格，虽然渲染高效，但几何表达能力受限于网格拓扑，且在无精确表面跟踪时难以学习准确几何。DVA将底层表示替换为附着于LBS骨骼网格的混合体积原语，每个原语是带透明度的体积基元。这一改变的因果机制在于：体积表示天然支持拓扑变化和模糊边界（如头发、宽松衣物边缘），且能通过可微分渲染从纯图像监督中学习更准确的底层几何，无需显式表面跟踪。实验表明，在同等图像监督条件下，体积原语比网格表示学习到更准确的几何形态（Section 4.3）。

**Changed Slot 2：条件化信号——从全局低维嵌入到局部纹素对齐特征**

这是DVA最核心的创新机制。FBCA使用全局姿态参数和低维嵌入作为条件信号，NeuralBody仅使用姿态驱动SMPL扩散潜码，两者都将丰富的高维观测压缩为信息瓶颈，丢弃了大量局部细节。DVA通过纹素对齐特征将条件化信号提升为**空间密集、局部对齐**的形式：多视图图像被反投影到UV空间，与局部姿态编码在纹素级别融合，每个原语获得其对应纹素位置的专属特征。

因果链路如下：纹素对齐特征保留了输入信号的空间结构（Fig. 4），使得模型能够直接“看到”衣物褶皱、纹理细节的局部对应关系，而非从压缩的全局编码中猜测。这带来了两个关键优势：(1) **表达力提升**：高频细节（如衣物褶皱、布料纹理）被忠实保留；(2) **泛化增强**：在未见姿态下，局部特征仍能提供有意义的条件信号，而非依赖全局编码对未见姿态-外观组合的外推。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2207_09774/figures/005_Figure_4.jpg]]
*Figure 4: Effects of texel-aligned features. Expressive texel-aligned features allow our model to generalize better to challenging unseen clothing states*

**Changed Slot 3：视角表示——从全局相机位置到局部视角方向投影**

传统方法将相机相对于根关节的全局位置作为视角条件，这迫使模型从有限数据中学习姿态相关变形与视角的复杂交互，容易在未见姿态-视角组合下产生严重伪影（Fig. 3）。DVA将视角信号表达为每个原语局部坐标系下的投影：
$$v_t = \mathbf{v} \cdot \mathbf{n}_t$$
其中v为全局视角方向，n_t为蒙皮网格上第t个三角形的法线。这一改变的因果机制在于**解耦视角变化与姿态变形**：局部视角坐标仅编码相机相对于该原语局部表面的朝向，与全局身体姿态解耦，从而在未见姿态-视角组合下仍能产生合理的视角相关外观（如高光、边缘光），避免了全局条件化带来的过拟合伪影。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2207_09774/figures/004_Figure_3.jpg]]
*Figure 3: Effects of view conditioning. Localized view conditioning leads to better generalization on unseen combinations of poses and viewpoints*

### 训练与推理路径

**训练阶段**：输入为多视角同步捕获的图像序列、对应的人体姿态参数θ和相机参数。编码器提取纹素对齐特征后，三个解码分支分别预测原语变换、体积属性和阴影效果。通过可微分光线行进渲染得到预测图像，与真实图像计算复合损失并反向传播。体积先验损失约束原语紧凑附着于网格表面，避免漂浮伪影。

**推理/驱动阶段**：给定新的姿态序列和视角参数，模型无需重新训练即可生成对应视角的渲染图像。纹素对齐特征从驱动信号（可为稀疏2-3个视图）中实时提取，为每个原语提供局部条件化，支持自由视角渲染和动画驱动。值得注意的是，DVA在仅2-3个稀疏视角驱动下仍保持较高PSNR（Table 2），且对缺失信息比LookingGood更鲁棒，这得益于LBS网格提供的结构先验。

### 关键公式与变量含义

- **$M_\theta$**：经LBS蒙皮后的粗几何网格，为原语提供初始附着位置
- **$t_k$**：第k个原语的最终位置，由网络预测偏移δt_k与LBS附着点$\hat{t}_k(\theta)$相加得到
- **$V^{\mathrm{rgb}}$, $V^\alpha$**：分别为颜色场和不透明度场，由外观/不透明度解码分支预测
- **$T(t)$**：沿光线的累积透射率，决定光线穿透到深度t的概率
- **$v_t$**：全局视角方向v在三角形法线n_t上的投影，构成局部视角条件
- **$\mathcal{L}_{\mathrm{vol}}$**：体积先验损失，约束原语紧凑性，防止原语过度扩散

### 创新机理总结

DVA的本质创新在于通过**纹素对齐特征**这一因果调节变量，在参数化人体模型的骨骼结构上构建了一个**空间密集条件化的体积表示**。这并非简单的“体积+纹理”组合，而是通过三个changed slots的协同作用——体积原语提供几何灵活性，纹素对齐特征提供局部高保真条件，局部视角投影解耦姿态-视角交互——实现了对“鲁棒性-表达力”权衡的根本性突破。模型既继承了LBS骨骼网格对人体拓扑和运动范围的强先验约束（保证稀疏输入下的鲁棒性），又通过纹素级别的密集条件化保留了观测信号的几乎全部细节信息（保证高保真度），从而在未见姿态、未见视角和稀疏驱动等多个维度展现出显著优于基线方法的泛化能力。

## 实验与关键发现

### 评估设置

DVA 在两个任务上接受验证：**新视角合成**（NVS）和**未见姿态驱动**。NVS 实验在 ZJU-MoCap 数据集的两个代表性序列（S386 和 S387）上进行，评估模型在训练视角之外的泛化能力。驱动实验则使用作者自采集的多视图数据集，测试模型在未见运动序列上的表现。评估指标采用 PSNR，对比基线包括基于网格的可驱动化身 **FBCA**（Bagautdinov et al., TOG 2021）、基于 SMPL 潜码扩散的体渲染方法 **NeuralBody**（Peng et al., CVPR 2021），以及实时 2D 神经重渲染系统 **LookingGood**（Martin-Brualla et al., 2018）。

### 新视角合成结果

Table 1 给出了 ZJU-MoCap 上的定量对比。DVA 在两个序列上均显著超越所有基线：

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2207_09774/figures/007_Table_1.jpg]]
*Table 1: Quantitative results (PSNR) for NVS on ZJU-MoCap*

- **S386 序列**：DVA 达到 35.414 PSNR，相比 FBCA（32.123）提升 **+3.291 dB**，相比 NeuralBody（33.196）提升 **+2.218 dB**。
- **S387 序列**：DVA 达到 30.512 PSNR，相比 FBCA（27.886）提升 **+2.626 dB**，相比 NeuralBody（28.640）提升 **+1.872 dB**。

这一优势的核心机制在于纹素对齐特征提供的密集空间条件化。FBCA 依赖全局姿态参数和低维嵌入，丢弃了大量局部观测细节；NeuralBody 仅以姿态为驱动信号，缺乏对多视图图像信息的直接利用。DVA 通过将多视图图像反投影到 UV 纹理空间，为每个体积原语提供空间对齐的局部特征，从而更忠实地再现衣物褶皱等高频细节。Fig. 5 的定性对比进一步佐证了这一点：DVA 在衣领、袖口等细节区域的重建质量明显优于两个基线。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2207_09774/figures/003_Figure_5.jpg]]
*Figure 5: Novel View Synthesis. We compare our method to state-of-the-art for NVS on ZJU-MoCap. Despite not being explicitly tailored to be trained with sparse supervision, our method outperforms competitors. Real faces and their reconstructions are blurred for anonymity*

值得注意的是，DVA 并未针对稀疏视角训练做特殊设计，但在 ZJU-MoCap 的稀疏多视图设置下仍取得了最优性能，这表明纹素对齐特征本身具备较强的信息融合能力。

### 驱动性能

Table 2 报告了在未见运动序列上的驱动结果。DVA 在 3 视图和 2 视图驾驶条件下均优于 FBCA 和 LookingGood：

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2207_09774/figures/006_Table_2.jpg]]
*Table 2: Quantitative results (PSNR) on unseen motion. Please refer to supplementary video for more results*

- **3 视图驾驶**：DVA 平均 PSNR 为 33.728。
- **2 视图驾驶**：DVA 平均 PSNR 为 33.409。

更重要的是，DVA 对缺失信息表现出更强的鲁棒性。LookingGood 作为非参数方法，虽然在输入完备时表现良好，但在稀疏视图下缺乏结构先验，性能下降明显。DVA 通过将体积原语附着于 LBS 骨骼网格，引入了参数化模型的鲁棒先验，同时利用纹素对齐特征保留模型无关方法的细节捕捉能力，在稀疏驱动信号下实现了二者的优势互补。

### 消融实验

#### 局部视角条件化 vs 全局视角条件化

Fig. 3 展示了视角条件化策略的关键消融。当使用全局视角条件化（相机相对于根关节的位置）时，模型在未见姿态-视角组合下会产生严重的视觉伪影，表现为面部和衣物区域的不自然阴影和纹理扭曲。这是因为全局条件化迫使模型从有限数据中学习姿态相关变形与视角之间的复杂交互，导致过拟合。

DVA 改用局部视角条件化：将全局视角方向 $\mathbf{v}$ 投影到蒙皮网格每个三角形的法线 $\mathbf{n}_t$ 上，得到局部坐标 $v_t = \mathbf{v} \cdot \mathbf{n}_t$。这一设计将视角信息分解到每个原语的局部坐标系中，使得模型只需学习局部几何与视角的简单关系，显著提升了对未见姿态-视角组合的泛化能力。消融结果显示，局部条件化下的渲染结果视角相关外观自然，无明显伪影。

#### 纹素对齐特征 vs 瓶颈表示

Fig. 4 对比了纹素对齐特征与瓶颈表示（将多视图信息压缩为低维全局潜码）在保留高频细节方面的能力。瓶颈表示因其信息压缩的特性，丢失了空间局部性，导致衣物褶皱、纹理细节等高频信息被平滑化。纹素对齐特征通过直接在 UV 空间保留空间结构，使解码器能够访问每个纹素位置的完整局部信息，从而在未见衣物状态下仍能生成清晰的高频细节。这一消融直接验证了本文的核心因果机制：**空间对齐的密集条件化是保留观测细节、增强泛化能力的关键**。

#### 体积原语 vs 网格表示

Section 4.3 分析了底层表示的影响。FBCA 使用纹理网格作为输出表示，其训练依赖精确的表面跟踪来建立跨帧对应。当表面跟踪不准确时，网格表示难以学习正确的几何。DVA 的体积原语表示则更为灵活：即使在缺乏精确表面监督的情况下，仅通过图像重建损失即可学习到更准确的底层几何。这一优势源于体积表示的连续性——原语的位置、旋转和缩放偏移由运动解码分支以纹素对齐特征为条件进行预测（Eq. 4），无需显式的跨帧对应约束。

### 失败模式与适用边界

论文明确指出了 DVA 的几项局限性：

1. **宽松衣物的建模质量下降**：当衣物与 LBS 引导网格存在显著偏差时（如裙摆、宽松外套），体积原语难以通过有限的偏移量准确跟踪衣物的独立运动。这是因为原语的初始附着位置由 LBS 网格决定，偏移预测的容量有限。对于极端宽松的服装，需要更灵活的基元附着机制或额外的非刚性变形模块。

2. **单一身份与单一服装的限制**：当前模型为个性化化身设计，每个模型仅支持一个身份的一套服装。扩展到多身份训练或服装更换需要重新设计条件化架构，可能涉及身份/服装解耦的潜空间或元学习策略。

3. **头戴式捕获设备的未验证性**：论文未在 VR 眼镜等极稀疏视角设备上进行测试。双向远程呈现场景对视角外推能力和实时性提出了更高要求，当前模型的泛化边界在此类条件下尚不明确。

4. **稀疏视角驱动的信息缺失**：虽然 DVA 在 2-3 视图下优于基线，但 Table 2 中 PSNR 随视图数减少而下降的趋势表明，极端稀疏（如单目）条件下仍存在信息瓶颈。纹素对齐特征的多视图聚合策略在视图过少时可能退化为不完整的纹理填充。

### 关键发现总结

DVA 的实验结果揭示了三个层次的核心发现：

- **表示层面**：体积原语比网格表示更适合图像监督下的可驱动化身学习，因为它降低了对精确表面跟踪的依赖。
- **条件化层面**：纹素对齐的密集条件化是连接参数化先验和模型无关表达力的关键桥梁——它既保留了 UV 空间的空间结构，又为每个原语提供了局部化的姿态和图像信息。
- **视角建模层面**：局部视角条件化通过将全局视角分解为每个原语的局部坐标，有效避免了过拟合，是实现未见姿态-视角组合泛化的必要设计。

这些发现共同指向一个统一的因果逻辑：**通过将混合体积原语附着于 LBS 网格，并对每个原语使用其对应纹素的局部条件化，DVA 同时获得了参数化模型的鲁棒先验和模型无关方法的细节捕捉能力**。Table 1 和 Table 2 的定量优势、Fig. 3 和 Fig. 4 的消融证据，以及 Fig. 5 的定性对比，共同构成了支撑这一主张的完整证据链。

## 定位与知识库关联

DVA 在可驱动人体化身领域同时改写了三个关键设计槽位，其核心贡献在于证明了**密集的、空间对齐的局部条件化**能够弥合参数化模型的鲁棒性与模型无关方法的表达力之间的鸿沟。

**相对基线的槽位变更**

| 设计维度 | 基线方法 | DVA 的变更 | 因果效应 |
|----------|----------|------------|----------|
| 底层几何表示 | 纹理网格（**FBCA**, Bagautdinov et al., TOG 2021） | 附着于 LBS 骨骼网格的混合体积原语（MVP），并允许原语位置/旋转/缩放偏移 | 体积表示免除了对精确表面跟踪的依赖，可在仅图像监督下学习更准确的几何（Section 4.3）；原语偏移提供了局部变形自由度 |
| 条件化信号 | 全局姿态参数 + 低维嵌入（FBCA）；仅姿态驱动（**NeuralBody**, Peng et al., CVPR 2021） | 局部纹素对齐的多视图图像特征 + 局部姿态编码，映射到 UV 纹理空间 | 保留了驱动信号的空间结构，避免瓶颈表示的信息损失，显著提升高频细节保真度（Fig. 4） |
| 视角表示 | 相机相对根关节的全局位置 | 每个原语局部坐标系下的视角方向投影 $v_t = \mathbf{v} \cdot \mathbf{n}_t$ | 消除全局视角条件化在未见姿态-视角组合下的严重过拟合伪影（Fig. 3） |

**与已有工作的本质差异**

FBCA 代表了参数化网格路线的上限：它利用精确的网格跟踪将纹理映射到 UV 空间，但依赖全局条件化，且网格拓扑限制了拓扑变化的表达。NeuralBody 则代表了神经体积路线的典型范式：在 SMPL 顶点上扩散潜码，但条件化信号仅限于姿态，缺乏对观测图像的直接利用。**LookingGood**（Martin-Brualla et al., 2018）作为模型无关的 2D 神经重渲染方法，在稀疏输入下缺乏结构先验，表现脆弱。

DVA 的独特定位在于：它用 LBS 网格提供了**强关节体积先验**（继承参数化模型的鲁棒性），同时通过纹素对齐特征将多视图观测**密集注入**到每个体积原语（继承模型无关方法的表达力）。这种设计使得 DVA 在稀疏驱动信号下（2-3 个视图）仍能保持优于 LookingGood 和 FBCA 的 PSNR（Table 2），且对缺失信息更鲁棒。

**知识库挂载点**

1. **可驱动神经渲染**：DVA 可被归入“参数化先验 + 神经体积表示”这一分支，与 NeuralBody、Animatable NeRF（Peng et al., ICCV 2021）并列。其纹素对齐特征机制为后续工作提供了一个通用条件化范式——将全局驱动信号分解到局部坐标框架。

2. **体积原语表示**：DVA 继承并扩展了 MVP（Lombardi et al., TOG 2021）的体积原语框架，关键创新在于将原语**附着于可变形骨骼网格**并赋予运动解码分支。这为体积原语在可驱动人体上的应用提供了蓝图。

3. **UV 空间条件化**：DVA 将条件化信号映射到 UV 纹理空间的做法，与 FBCA 的纹理生成管线形成对比：FBCA 在 UV 空间生成 RGB 纹理，而 DVA 在 UV 空间生成**特征图**来条件化解码器。这种“特征纹理”思路可迁移到其他需要密集空间条件的生成任务。

**适用边界与局限**

- **宽松衣物**：当衣物严重偏离 LBS 引导网格时（如长裙、斗篷），原语附着点的初始位置不再有效，建模质量下降。这是 LBS 先验的固有边界。
- **身份与服装泛化**：当前模型为单身份、单服装的个性化化身，未扩展到多身份或多服装设置。这是与通用人体先验模型（如 SMPL 参数化身体）的本质差异。
- **捕获条件**：模型依赖多视图捕捉系统，尚未在头戴式设备（如 VR 眼镜）的极稀疏视角下验证。双向远程呈现场景需要进一步研究。

**后续启发**

DVA 的局部条件化策略提出了一个可泛化的问题：**能否将“全局信号→局部坐标框架分解”的模式应用于其他原语类型（如高斯泼溅）或更复杂的交互场景？** 纹素对齐特征的本质是将非结构化的驱动信号（姿态、图像）重新组织为与几何表面绑定的结构化表示，这一思想可能适用于手部-物体交互、面部微表情等需要精细空间控制的领域。此外，将体积原语的运动解码分支与物理仿真结合，可能是处理宽松衣物的潜在方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Drivable_Volumetric_Avatars_Using_Texel_aligned_Features.pdf]]