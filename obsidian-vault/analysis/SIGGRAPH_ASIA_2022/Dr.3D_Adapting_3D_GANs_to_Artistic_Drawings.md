---
title: "Dr.3D: Adapting 3D GANs to Artistic Drawings"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Dr_3D_Adapting_3D_GANs_to_Artistic_Drawings.pdf
project_link: null
code_link: null
aliases:
- D3
- D3A3GAD
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_geometry_processing
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过三个关键组件协同缓解几何模糊性：变形感知的3D合成网络（Deformation-aware 3D synthesis network）以建模绘画中多样化的形状变化；交替适应方案（Alternating adaptation）以逐步提升姿态估计和图像合成；以及几何先验（Geometric priors）在适配过程中保持合理的3D结构。
primary_logic: 绘画虽然具有几何模糊性，但与真实照片仍存在高层次形状相似性。通过引入变形网络扩展潜在空间、用基于伪数据的交替训练缩小姿态估计与合成的鸿沟、并利用深度相似性和法线平滑性作为几何先验，能够将从真实人脸照片预训练的3D GAN稳定地迁移到绘画域，实现多视角一致的生成与编辑。
claims:
- 绘画具有内在几何模糊性，导致直接适配3D GAN失败，如图1及图6所示。
- Dr.3D的三大组件（变形感知合成网络、交替适应、几何先验）有效处理几何模糊性，消融研究（图7）证实每个组件的贡献。
- 与三个3D GAN基线（π-GAN, StyleNeRF, EG3D）相比，Dr.3D在四个绘画数据集上取得了更优的图像质量和3D几何准确性（FID、KID、Depth/Pose MSE）。
- Historical Art 上 FID ↓ = 23.42
---

# Dr.3D: Adapting 3D GANs to Artistic Drawings

> [!tip] 核心洞察
> 绘画虽然具有几何模糊性，但与真实照片仍存在高层次形状相似性。通过引入变形网络扩展潜在空间、用基于伪数据的交替训练缩小姿态估计与合成的鸿沟、并利用深度相似性和法线平滑性作为几何先验，能够将从真实人脸照片预训练的3D GAN稳定地迁移到绘画域，实现多视角一致的生成与编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | Dr.3D：将三维生成对抗网络适配到艺术绘画 |
| 英文题名 | Dr.3D: Adapting 3D GANs to Artistic Drawings |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://jinwonjoon.github.io/dr3d/) |
| Topic | #topic/graphics_geometry_processing #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Dr.3D |
| Dataset | Historical Art, Ukiyo-e, Anime, Caricature |

> [!tip] 效果简介
> - Historical Art 上，FID ↓ 23.42 vs 26.95 (EG3D) (-3.53)。
> - Ukiyo-e 上，FID ↓ 37.38 vs 58.72 (EG3D) (-21.34)。
> - Anime 上，FID ↓ 8.699 vs 12.41 (EG3D) (-3.711)。

## 概要

**问题**：将3D GAN从真实人脸照片域适配到艺术绘画域时，绘画固有的几何模糊性（非确定性形状与相机姿态）导致直接适配产生扁平几何和低质量图像。

**方法**：Dr.3D 通过三个协同组件缓解几何模糊性——（1）变形感知的3D合成网络，引入额外潜在码和变形网络以建模绘画中多样化的形状与风格变化；（2）交替适应方案，交替更新合成网络与姿态估计网络，逐步缩小姿态估计与图像合成的鸿沟；（3）几何先验损失（深度相似性、法线平滑性、姿态损失），在适配过程中保持合理的3D结构。

**主要结果**：在历史艺术、浮世绘、动漫、漫画四个绘画数据集上，Dr.3D 在图像质量（FID/KID）和几何准确性（深度/姿态MSE）上均优于 π-GAN、StyleNeRF、EG3D 三个3D GAN基线。消融实验证实三个组件各自对避免扁平几何、提升形状保真度和图像质量有决定性贡献。

**方法定位**：Dr.3D 以 EG3D 为基础架构，在其生成器中插入变形网络、采用交替训练策略并施加几何先验，属于面向绘画域的3D GAN域适配方法。

## 核心方法与创新机理

### 1. 问题瓶颈与核心思路

将预训练于真实人脸照片的3D GAN直接微调到绘画域面临根本性困难：绘画具有**内在的几何模糊性（geometric ambiguity）**。与照片不同，绘画中的形状和相机姿态并非唯一确定——同一幅肖像画可能对应多种合理的三维解释。这种不确定性使得标准的逐像素域适配策略极易产生**扁平的几何体**和**低质量的图像**（Figure 1, Figure 6）。

Dr.3D的核心洞察在于：尽管绘画存在几何模糊性，但其与真实照片之间仍保持着高层次的形状相似性。基于这一观察，Dr.3D通过三个协同组件将不适定的适配问题转化为可解问题：

1. **变形感知的3D合成网络（Deformation-aware 3D synthesis network）**：扩展潜在空间以显式建模绘画中多样化的形状变化；
2. **交替适应方案（Alternating adaptation）**：逐步缩小姿态估计与图像合成之间的鸿沟；
3. **几何先验（Geometric priors）**：在适配过程中约束合成网络保持合理的3D结构。

### 2. 基础架构：EG3D的继承

Dr.3D构建于**EG3D**（Chan et al. 2022）之上，继承了其核心的3D感知生成框架。EG3D的生成器包含三个关键模块：

- **映射网络（Mapping network）**：将标准GAN潜在码 $z$ 映射为中间潜在码 $w$，遵循StyleGAN的设计范式；
- **特征生成器（Feature Generator）**：基于StyleGAN2架构，从 $w$ 生成2D特征图，并将其重组为3D正交特征平面（tri-plane）；
- **体积渲染模块（Volume Rendering Module）**：利用轻量MLP从tri-plane特征中预测采样点的颜色和密度，通过可微分体积渲染生成最终图像和深度图。

这一基础管线提供了多视角一致的3D表示能力，但直接将其微调到绘画域时，几何模糊性导致生成器倾向于“平均化”所有可能的形状解释，从而产生扁平的几何和失真的图像。

### 3. 创新组件一：变形感知的3D合成网络

#### 3.1 设计动机

绘画域与照片域之间存在系统性的形状分布差异。例如，漫画肖像中人物的面部比例被刻意夸张，浮世绘中的人物轮廓具有独特的风格化变形。标准的EG3D生成器仅通过映射网络控制风格和内容，缺乏显式建模这类**局部形状变化**的能力。

#### 3.2 网络结构

Dr.3D在EG3D生成器中引入了一个**变形网络（Deformation network）**和额外的**变形潜在码 $z_d$**。具体结构如下（Figure 2, Figure 3）：

![[assets/figures/papers/paper_list_l48_https_jinwonjoon_github_io_dr3d/figures/002_Figure_2.jpg]]
*Figure 2: Network architecture of a deformation-aware 3D synthesis network. The network consists of a deformation network, a mapping network, a feature generator, and a volume rendering module. The network takes latent codes*

![[assets/figures/papers/paper_list_l48_https_jinwonjoon_github_io_dr3d/figures/003_Figure_3.jpg]]
*Figure 3: Network architectures of a generator and a deformation network. The generator network is based on the Style-GAN2 generator [Karras et al. 2020b]. FC: a fully-connected (FC) layer. A: an affine layer consisting of a single FC layer. Mod: a modulation layer. Demod: a demodulation layer*

1. **变形潜在码 $z_d$**：从标准正态分布采样，独立于控制内容的潜在码 $z$，专门编码形状变形信息；
2. **变形网络**：一个基于MLP的网络，将 $z_d$ 转换为空间变化的**残差特征（residual features）**；
3. **特征注入**：残差特征被注入到StyleGAN2生成器的浅层卷积特征中，通过调制-解调（modulation-demodulation）机制影响局部形状和外观。

变形网络的设计借鉴了StyleGAN的层次化控制思想：浅层特征控制粗粒度的形状和姿态，深层特征控制细粒度的纹理。通过将变形残差注入浅层，$z_d$ 能够有效控制绘画中多样化的几何变形，而不会破坏内容潜在码 $z$ 对身份和整体结构的主控能力。

#### 3.3 因果机制

变形感知合成网络通过以下因果链缓解几何模糊性：

- **扩展潜在空间**：$z_d$ 为每种内容潜在码 $z$ 提供了额外的变形自由度，使得生成器可以覆盖绘画域中更广泛的形状分布；
- **解耦内容与变形**：$z$ 控制“画的是谁”，$z_d$ 控制“以何种风格变形”，二者的解耦避免了内容信息与风格变形之间的冲突；
- **局部控制**：残差特征的空间变化特性允许生成器在不同区域施加不同程度的变形（例如仅夸张眼睛大小而不改变鼻子形状），这比全局变换更符合绘画中常见的局部夸张手法。

Figure 8展示了固定 $z$ 而改变 $z_d$ 的效果：同一身份在不同变形码下呈现出多样化的形状变化，验证了变形网络的解耦控制能力。

### 4. 创新组件二：交替适应方案

#### 4.1 设计动机

绘画域适配面临的另一个核心困难是**相机姿态的未知性**。在标准3D GAN训练中，真实照片的姿态可通过现成的姿态估计器获得。但绘画的几何模糊性使得姿态估计变得极不可靠——同一幅画可能被估计出多种不同的姿态。若直接使用不可靠的姿态估计来训练合成网络，会导致生成器学习到错误的几何-姿态对应关系；反之，若合成网络本身质量差，其生成的图像也无法用于训练姿态估计器。这形成了一个“先有鸡还是先有蛋”的困境。

#### 4.2 交替训练流程

Dr.3D通过**交替适应**打破这一循环依赖（Figure 4）：

![[assets/figures/papers/paper_list_l48_https_jinwonjoon_github_io_dr3d/figures/004_Figure_4.jpg]]
*Figure 4: Alternating adaptation. Our approach alternatingly adapts the deformation-aware 3D synthesis network and the pose-estimation network*

**阶段一：合成网络适配**
- 使用当前的姿态估计网络 $P$ 为真实绘画 $x_{\text{real}}$ 预测姿态 $\theta_{\text{est}} = P(x_{\text{real}})$；
- 以 $\theta_{\text{est}}$ 作为条件，训练变形感知合成网络 $G$，使其生成的图像 $x_{\text{fake}}$ 与真实绘画在判别器 $D$ 下不可区分；
- 合成网络的总损失为：
  $$\mathcal{L} = \mathcal{L}_{a}(x_{\text{fake}}, x_{\text{real}}, \theta) + \mathcal{L}_{g}(x_{\text{fake}}, d_{\text{fake}}, \theta)$$
  其中 $\mathcal{L}_{a}$ 为条件对抗损失，$\mathcal{L}_{g}$ 为几何先验损失（见组件三）。

**阶段二：姿态估计网络微调**
- 使用当前合成网络 $G$ 生成伪数据集 $\Omega = \{(\theta, x_{\text{fake}}^{\theta})\}$，其中 $\theta$ 为随机采样的真实姿态，$x_{\text{fake}}^{\theta}$ 为对应姿态下的合成图像；
- 在伪数据集上微调姿态估计网络 $P$，损失为均方误差：
  $$\mathcal{L}_{\boldsymbol{P}} = \frac{1}{|\Omega|} \sum_{\{\theta, x_{\text{fake}}^{\theta}\}\in\Omega} \left\| \theta - P(x_{\text{fake}}^{\theta}) \right\|_2^2$$

两个阶段交替进行，形成正向反馈循环：更好的合成网络产生更真实的伪数据 → 更准确的姿态估计 → 更好的合成网络。

#### 4.3 因果机制

交替适应的有效性源于以下机制：

- **打破循环依赖**：通过使用合成数据训练姿态估计器，避免了在真实绘画上直接估计姿态的不确定性；
- **逐步精化**：初始阶段合成网络质量较低，但即使粗糙的合成数据也能为姿态估计器提供有效的训练信号（因为合成数据的姿态是已知的精确值）；随着合成网络改善，伪数据质量提升，姿态估计器进一步精化；
- **域对齐**：姿态估计器在合成绘画上训练，使其学习到绘画域特有的姿态-外观映射关系，而非简单迁移照片域的估计能力。

消融实验（Figure 7b）证实：仅在EG3D基线上添加交替适应，就能有效避免扁平几何体的产生，验证了这一组件对缓解姿态模糊性的关键作用。

### 5. 创新组件三：几何先验

#### 5.1 设计动机

即使有了变形感知网络和交替适应，合成网络仍可能在适配过程中“走捷径”——生成视觉上逼真但几何上不合理的形状（例如将人脸压扁为一个平面但仍能渲染出正确的2D外观）。几何先验的作用是**显式约束合成网络的3D输出**，确保其保持合理的立体结构。

#### 5.2 先验损失设计

几何先验损失 $\mathcal{L}_g$ 由三个子损失加权组合：
$$\mathcal{L}_g = \alpha \mathcal{L}_d + \beta \mathcal{L}_n + \gamma \mathcal{L}_p$$

**（1）深度相似性损失 $\mathcal{L}_d$**

$$\mathcal{L}_d = \| k * d_{\text{fake}} - k * d_{\text{fake,photo}} \|_2^2$$

- $d_{\text{fake}}$：合成绘画的深度图；
- $d_{\text{fake,photo}}$：使用**相同潜在码 $z$ 和姿态 $\theta$** 但通过**预训练的照片域EG3D生成器**合成的对应照片深度图；
- $k$：低通高斯核，用于提取深度图的低频分量。

该损失的核心思想是：尽管绘画和照片在纹理和局部细节上差异巨大，但二者的**整体3D几何结构应当相似**。通过惩罚合成绘画与对应合成照片之间深度低频分量的差异，$\mathcal{L}_d$ 引导生成器保持与照片域一致的宏观几何形状。

**（2）法线平滑性损失 $\mathcal{L}_n$**

$$\mathcal{L}_n = \| \nabla n_{\text{fake}} \|_2^2$$

- $n_{\text{fake}}$：合成绘画的表面法线图；
- $\nabla$：空间梯度算子。

该损失惩罚法线图的突变，鼓励生成器产生平滑的几何表面。这在绘画域适配中尤为重要，因为对抗训练可能诱导生成器产生高频的几何伪影来欺骗判别器。

**（3）姿态损失 $\mathcal{L}_p$**

姿态损失直接惩罚合成网络对输入姿态条件的偏离，确保生成的图像确实对应指定的相机视角，从而维护3D一致性。

#### 5.3 因果机制

三个几何先验从不同层面约束合成网络的3D行为：

- $\mathcal{L}_d$ 提供**全局几何锚定**：防止生成器在适配过程中“遗忘”预训练阶段学到的3D结构；
- $\mathcal{L}_n$ 提供**局部几何正则化**：抑制对抗训练可能引入的几何噪声；
- $\mathcal{L}_p$ 提供**姿态一致性约束**：确保多视角生成的可靠性。

消融实验（Figure 7d）表明，在交替适应和变形网络基础上添加几何先验后，完整Dr.3D达到了最佳的图像质量和形状重建效果，验证了几何先验对最终性能的贡献。

### 6. 训练与推理路径

#### 6.1 训练路径

1. **预训练阶段**：在FFHQ真实人脸照片数据集上预训练标准EG3D模型（包括生成器、判别器和姿态估计器）；
2. **适配阶段**：在目标绘画数据集上执行Dr.3D适配：
   - 初始化：加载预训练的EG3D权重，随机初始化变形网络参数；
   - 交替迭代：
     a. 固定姿态估计网络，使用当前姿态预测训练变形感知合成网络（包含对抗损失和几何先验损失）；
     b. 固定合成网络，生成伪数据集并微调姿态估计网络；
   - 重复直至收敛。

#### 6.2 推理路径

1. **随机生成**：采样 $z \sim \mathcal{N}(0, I)$、$z_d \sim \mathcal{N}(0, I)$ 和目标姿态 $\theta$，通过变形感知合成网络一次性生成多视角一致的绘画图像；
2. **GAN反演与编辑**：使用现成的GAN反演方法将真实绘画嵌入到潜在空间，获得对应的 $z$ 和 $z_d$，随后可通过修改 $z$（语义编辑）或 $\theta$（新视角合成）实现可控操作（Figure 9, Figure 10）。

### 7. 三个组件的协同关系

三个组件并非独立工作，而是形成紧密的因果耦合：

- **变形网络**扩展了生成器的表达能力，使其能够覆盖绘画域的形状分布，为**交替适应**提供了更丰富的合成数据空间；
- **交替适应**逐步提升姿态估计的准确性，为**几何先验**中的深度相似性损失提供了更可靠的照片域深度参考（因为照片域深度依赖于正确的姿态条件）；
- **几何先验**约束合成网络在变形网络提供的灵活性范围内保持合理的3D结构，防止表达能力被滥用于生成几何上不合理的形状。

移除任一组件都会导致性能退化：仅用交替适应（无变形网络）可避免扁平几何但形状保真度不足（Figure 7b）；添加变形网络后形状质量提升但仍缺乏几何约束（Figure 7c）；三者结合达到最优（Figure 7d）。

## 实验与关键发现

### 实验设置概览

Dr.3D在四个风格差异显著的绘画数据集上进行验证：**Historical Art**（古典肖像油画）、**Ukiyo-e**（浮世绘版画）、**Anime**（动漫风格）和**Caricature**（夸张漫画）。所有方法均在FFHQ真实人脸照片上预训练，然后使用相同训练数据在目标绘画域上进行微调，确保对比公平。定量评估采用标准图像质量指标（FID、KID），形状与姿态评估则利用伪地面真值或艺术家标注的真值数据进行Depth MSE和Pose MSE计算。

### 核心定量结果

**Table 1** 给出了图像质量的全面对比。Dr.3D在绝大多数数据集上取得了最优的FID分数：

| 数据集 | Dr.3D FID↓ | EG3D FID↓ | 提升幅度 |
|--------|-----------|----------|---------|
| Historical Art | 23.42 | 26.95 | -3.53 |
| Ukiyo-e | 37.38 | 58.72 | **-21.34** |
| Anime | 8.699 | 12.41 | -3.711 |
| Caricature | 7.123 | 11.72 | -4.597 |

其中**Ukiyo-e数据集上的改进最为显著**，FID降低了21.34，说明Dr.3D对极端风格化绘画（如浮世绘的平面色块与轮廓线）具有更强的适应能力。KID指标同样验证了这一趋势：Historical Art上Dr.3D的KID×10³为5.916，而EG3D为9.295，降低了3.379。

**Table 2** 报告了3D几何与姿态估计的精度的对比。在Historical Art上，Dr.3D的Depth MSE为0.217（与EG3D的0.215基本持平），但Pose MSE从0.054降至**0.030**，姿态估计精度提升显著。在Caricature数据集上，Depth MSE从0.033降至**0.020**，表明变形感知网络有效捕捉了漫画夸张的几何变形；但Pose MSE略有上升（0.070 vs. EG3D的0.047），这反映了漫画中极度非真实的五官比例对姿态估计的额外挑战。

### 与基线的定性对比

**Figure 6** 展示了StyleNeRF、π-GAN、EG3D和Dr.3D的视觉对比。在Ukiyo-e和Anime等挑战性风格上，三种基线方法均产生了**严重退化的3D几何**（如扁平化的人脸结构）和**不自然的图像伪影**。Dr.3D则生成了更合理的形状和更高质量的图像，尤其是在多视角一致性方面表现突出。Figure 5的策展结果进一步证明Dr.3D能够为四种截然不同的绘画风格生成3D感知的合成结果。

### 消融实验：三大组件的因果贡献

**Figure 7** 的消融研究清晰揭示了每个组件的独立作用：

1. **基线（EG3D直接微调）**：产生扭曲的图像和完全扁平的几何体（Figure 7a），验证了绘画几何模糊性导致直接适配失败的核心瓶颈。

2. **+交替适应（Alternating adaptation）**：避免了扁平几何的产生（Figure 7b），证明通过伪数据驱动的姿态估计微调能够逐步缩小姿态估计与图像合成的鸿沟，为后续组件提供更准确的相机先验。

3. **+变形感知合成网络（Deformation-aware synthesis network）**：进一步提升了形状重建保真度和图像质量（Figure 7c）。Figure 8通过固定同一潜在码、仅改变变形码 $z_d$ 的实验，直观展示了变形网络对局部形状和外观变化的解耦控制能力。

4. **+几何先验（Geometric priors）**：完整的Dr.3D达到了最佳的图像和形状合成质量（Figure 7d），验证了深度相似性损失 $\mathcal{L}_d$ 和法线平滑损失 $\mathcal{L}_n$ 在保持合理3D结构中的关键作用。

### 应用验证：GAN反演与语义编辑

Dr.3D在真实世界绘画上的应用能力通过两个案例得到验证：
- **Figure 9** 展示了维米尔名作《戴珍珠耳环的少女》的新视角合成，证明方法能够为历史名画赋予3D一致的几何重建。
- **Figure 10** 展示了语义编辑能力，包括性别转换（上排）和发型更改（下排），表明适配后的3D GAN继承了原始EG3D的编辑能力，同时保持了绘画风格的一致性。

### 失败模式与适用边界

论文明确指出了以下局限性：

1. **极端风格的几何退化**：对于极具挑战性的绘画风格（如某些动漫样本），部分潜在码仍可能产生扁平的几何体。这暗示变形网络的表达能力在极端域偏移下仍有上限。

2. **背景区域处理缺陷**：由于训练图像中背景缺乏3D一致的共享几何特征，Dr.3D在处理背景区域时存在局限性。这一问题与EG3D等现有3D GAN方法相同，属于领域共性问题而非Dr.3D特有。

3. **域泛化边界**：当前验证仅限于人脸肖像绘画，尚未扩展到非人脸或更广泛的绘画类别，方法的跨类别泛化能力仍属未知。

4. **姿态估计的域敏感性**：Caricature数据集上Pose MSE的轻微升高表明，极度夸张的几何变形可能超出姿态估计网络的鲁棒范围，需要在交替适应过程中引入更强的约束或更丰富的伪数据增强。

![[assets/figures/papers/paper_list_l48_https_jinwonjoon_github_io_dr3d/figures/001_Figure_1.jpg]]
*Figure 1: GAN inversion and semantic editing examples on a portrait drawing. For comparison, we perform naïve domain adaptation to ??-GAN [Chan et al. 2021] and StyleNeRF [Gu et al. 2022] by finetuning them on portrait drawings. Then, we invert the input image in (a) using an off-the-shelf GAN inversion method to a latent code and reconstruct the image and its shape at a different camera pose using each 3D GAN model. The results in (b) and (c) show that naïve adaptations of existing 3D GANs fail to handle the input drawing. On the other hand, our method can successfully reconstruct the input image, and also allow semantic editing as shown in (d) and (e). Image in (a): Portrait of a Member of the Wedi...*

![[assets/figures/papers/paper_list_l48_https_jinwonjoon_github_io_dr3d/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative comparison among StyleNeRF [Gu et al. 2022], ??-GAN [Chan et al. 2021], EG3D [Chan et al. 2022] and ours. The contents of the images are different as they are generated by differently trained generator models. StyleNeRF, ??-GAN and EG3D produce corrupted 3D geometries and unnatural-looking images especially for challenging styles such as ukiyo-e and anime, while our method produces more plausible shapes and images*

![[assets/figures/papers/paper_list_l48_https_jinwonjoon_github_io_dr3d/figures/010_Figure_7.jpg]]
*Figure 7: Ablation study. The baseline model (EG3D [Chan et al. 2022]) synthesizes a distorted image and a flattened geometry as shown in (a). While our alternating adaptation helps avoid flattened shapes as shown in (b), our deformationaware 3D synthesis network, and geometric priors further improve the synthesis quality*

## 定位与知识库关联

Dr.3D 的核心定位是**将预训练的 3D GAN 从真实照片域适配到艺术绘画域**，其本质挑战在于绘画具有固有的几何模糊性（geometric ambiguity）——形状和相机姿态均不确定，导致直接进行逐像素域适配时，现有 3D GAN 会崩溃为扁平几何和低质量图像。与现有方法的本质差异在于，Dr.3D 并非提出一个全新的 3D GAN 架构，而是**在 EG3D**（Chan et al., 2022）的基础上，针对绘画域适配这一特定任务，改变了三个关键 slot，形成一套完整的适配方案。

### 相对于已有方法改变的 slot

**Slot 1：合成网络架构 —— 从固定生成器到变形感知生成器**

基线 EG3D 的生成器仅包含映射网络和基于 StyleGAN2 的特征生成器，其潜在空间编码的是真实人脸照片的形状分布，缺乏对绘画中多样化形状变化（如夸张变形、风格化扭曲）的表达能力。Dr.3D 在此 slot 上新增了一个**变形网络（Deformation network）**，这是一个基于 MLP 的模块，接收额外的变形潜在码 $z_d$，将其转换为空间变化的残差特征，注入到 StyleGAN2 生成器的浅层卷积特征中。这一改变使得生成器能够在不破坏预训练 3D 先验的前提下，扩展潜在空间以覆盖绘画中丰富的局部形状和风格变化。证据来自图 7 的消融实验：仅添加交替适应（slot 2）可避免扁平几何，但加入变形网络后形状重建保真度和图像质量进一步提升。

**Slot 2：训练策略 —— 从固定姿态训练到交替适应**

基线 EG3D 在预训练阶段使用已知的真实相机姿态进行对抗训练，但在绘画域适配时，真实绘画的姿态是未知的，且直接使用在真实照片上训练的姿态估计器会产生严重偏差。Dr.3D 在此 slot 上引入了**交替适应（Alternating adaptation）方案**：交替更新 3D 合成网络和姿态估计网络。合成网络利用当前姿态估计进行训练，姿态网络则利用合成数据生成的伪标签（由合成网络以已知姿态渲染的图像构成伪数据集）进行微调。这种交替迭代逐步缩小了姿态估计与图像合成之间的鸿沟，使得两个网络在绘画域上协同进化。图 7(b) 显示，仅此组件就能避免基线 EG3D 产生的扁平几何体。

**Slot 3：损失函数 —— 从纯对抗损失到几何先验约束**

基线 EG3D 仅使用对抗损失进行训练，这在绘画域适配中缺乏对 3D 几何的显式引导，容易导致几何退化。Dr.3D 在此 slot 上引入了**几何先验损失** $\mathcal{L}_g = \alpha \mathcal{L}_d + \beta \mathcal{L}_n + \gamma \mathcal{L}_p$，包含三个子项：深度相似性损失 $\mathcal{L}_d$ 惩罚合成绘画深度图与对应合成照片深度图之间的低频差异（通过高斯核 $k$ 滤波后计算 MSE），利用预训练模型在照片域上仍能生成合理深度的事实作为软约束；法线平滑损失 $\mathcal{L}_n$ 惩罚合成几何表面法线的突变，鼓励平滑的 3D 结构；姿态损失 $\mathcal{L}_p$ 确保合成图像的姿态与输入姿态一致。这些先验在适配过程中持续引导生成器保持合理的 3D 结构，而非退化为 2D 图像生成器。

### 知识库挂载点

Dr.3D 挂载在以下知识库节点上：

1. **3D GAN 域适配（Domain Adaptation of 3D GANs）**：在 **EG3D**（Chan et al., CVPR 2022）的 tri-plane 混合表示和体积渲染框架上构建，继承了其高效的多视角一致生成能力。同时与 **π-GAN**（Chan et al., 2021）和 **StyleNeRF**（Gu et al., 2022）形成直接对比——后两者在直接微调到绘画域时均产生严重退化的几何和图像质量（见图 1、图 6）。

2. **GAN 域适配中的几何保持**：现有 2D GAN 域适配方法（如 StyleGAN-NADA、Mind-the-Gap）主要关注图像风格的迁移，不涉及 3D 几何一致性。Dr.3D 首次将域适配问题扩展到 3D GAN，并识别出几何模糊性是核心瓶颈，通过几何先验损失显式保持 3D 结构。

3. **变形建模与潜在空间扩展**：变形网络的设计借鉴了 StyleGAN 的层注入思想，但将其定向用于建模绘画中的形状变化而非风格变化，与 3D 可变形模型（3DMM）的显式参数化变形形成互补——前者是隐式的、从数据中学习的变形空间。

4. **姿态估计的自适应微调**：交替适应方案与自训练（self-training）和协同训练（co-training）范式相关，通过伪标签生成实现姿态估计器在无标注绘画数据上的域适配。

### 适用边界与局限

1. **目标域限制**：Dr.3D 目前仅在人脸肖像绘画上验证（历史艺术、浮世绘、动漫、漫画四个数据集），尚未扩展到非人脸或更广泛的绘画类别。对于缺乏共享 3D 几何特征的物体类别（如风景画、抽象画），几何先验的有效性可能显著下降。

2. **背景区域处理**：与 EG3D 等现有 3D GAN 一样，Dr.3D 在处理背景区域时存在局限，因为训练图像中背景缺乏 3D 一致的共享几何特征。这是 tri-plane 表示本身的结构性限制，而非 Dr.3D 特有的问题。

3. **极端风格的几何退化**：对于极具挑战性的绘画风格（如动漫），某些潜在码仍可能产生扁平的几何体（见补充文档），说明变形网络和几何先验的组合尚不能完全覆盖所有极端变形情况。

4. **姿态估计精度波动**：在 Caricature 数据集上，Dr.3D 的姿态 MSE（0.070）略高于 EG3D（0.047），尽管图像和深度质量更优。这表明交替适应在姿态精度和图像质量之间存在一定的权衡，可能与漫画中更极端的形状变形干扰了姿态估计有关。

### 后续启发与延伸方向

1. **扩展到非人脸域**：如何将变形感知合成网络和几何先验推广到包含非人脸物体的绘画域（如全身肖像、动物、场景），需要重新设计几何先验的形式，可能引入类别特定的 3D 模板或可变形模型。

2. **前景-背景分离生成**：通过分离前景与背景的特征生成路径，可以部分解决背景区域的 3D 一致性问题，使背景采用 2D 生成而前景保持 3D 结构。

3. **减少对几何先验的依赖**：当前方法依赖显式的深度和法线先验，这需要预训练模型在照片域上具有可靠的几何预测能力。未来方向包括让模型隐式学习绘画几何，例如通过对抗学习中的 3D 一致性判别，或利用多视角绘画数据（如连环画、动画帧）进行弱监督。

4. **与其他 3D 表示的结合**：Dr.3D 的适配方案（变形网络 + 交替适应 + 几何先验）是模块化的，可挂载到其他 3D GAN 架构（如基于 NeRF 的 π-GAN 或基于特征体的 StyleNeRF），为不同 3D 表示在绘画域上的适配提供通用框架。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Dr_3D_Adapting_3D_GANs_to_Artistic_Drawings.pdf]]