---
title: "TileGen: Tileable, Controllable Material Generation and Capture"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/TileGen_Tileable_Controllable_Material_Generation_and_Capture.pdf
project_link: null
code_link: null
aliases:
- TileGen
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_rendering_materials
- topic/generative_models_diffusion
core_operator: 将StyleGAN2架构中的卷积、上采样、下采样操作替换为wrap-around（循环边界）版本，使网络天然输出周期性（可平铺）的材质贴图；同时引入条件编码器处理用户提供的结构图案，将结构布局与风格（随机潜码）解耦。
primary_logic: 通过强制网络使用循环卷积等操作，可以隐式地保证生成结果在任何位置都具有平铺一致性，而无需依赖数据集的可平铺性；此外，将材质的结构（通过条件图案）与外观风格（通过潜码）分离，结合基于全局风格损失（Gram矩阵）的逆向渲染优化，能够在匹配单张照片外观的同时避免像素级过拟合，并实现可平铺和可编辑的材质重建。
claims:
- 与MaterialGAN、Deschaintre等人及Zhou等人的方法相比，我们的方法在单张图像重建中产生干净、无高光烧入伪影的材质贴图，且渲染结果逼真。
- 即使在非平铺数据集上训练，我们的无条件模型也能生成无缝平铺的纹理，而原始MaterialGAN不能。
- 仅将MaterialGAN的损失函数替换为我们的全局损失仍无法避免高光烧入伪影且不可平铺，说明架构的平铺设计和条件控制是关键。
- 单张手机闪光照片的SVBRDF重建 上 定性视觉质量（材质贴图干净度、渲染真实性、可平铺性） = 生成的材质贴图干净、无高光烧入伪影，可平铺，且可通过条件图案控制结构
---

# TileGen: Tileable, Controllable Material Generation and Capture

> [!tip] 核心洞察
> 通过强制网络使用循环卷积等操作，可以隐式地保证生成结果在任何位置都具有平铺一致性，而无需依赖数据集的可平铺性；此外，将材质的结构（通过条件图案）与外观风格（通过潜码）分离，结合基于全局风格损失（Gram矩阵）的逆向渲染优化，能够在匹配单张照片外观的同时避免像素级过拟合，并实现可平铺和可编辑的材质重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | TileGen：可平铺、可控的材质生成与采集 |
| 英文题名 | TileGen: Tileable, Controllable Material Generation and Capture |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2206.05649) |
| Topic | #topic/graphics_rendering_materials #topic/generative_models_diffusion |
| Method | TILEGEN |
| Dataset | 单张手机闪光照片的SVBRDF重建 |

> [!tip] 效果简介
> - 单张手机闪光照片的SVBRDF重建 上，定性视觉质量（材质贴图干净度、渲染真实性、可平铺性） 生成的材质贴图干净、无高光烧入伪影，可平铺，且可通过条件图案控制结构 vs MaterialGAN、Deschaintre等、Zhou等方法产生高光烧入伪影、不可平铺、不可控 (显著提升视觉质量和实用性)。
> - 材质生成多样性 上，随机采样质量与条件遵循度 给定结构图案，随机潜码产生风格多变但结构一致的材质；无条件模型产生丰富多样的材质 vs MaterialGAN生成随机但不可控的材质 (增加结构控制和类别特定生成)。

## 概要

现有无条件生成对抗网络（如**MaterialGAN**，Guo et al. 2020b）虽能生成材质贴图，但无法保证平铺性，且缺乏对材质类别或结构布局的控制；而基于单张照片的逆向重建方法（**Deschaintre et al.** 2018；**Zhou and Kalantari** 2021）常产生高光烧入伪影且结果不可平铺，限制了其在内容创作流程中的实际应用。

本文提出**TileGen**，一种基于StyleGAN2架构的材质生成与采集方法。其核心创新在于：将网络中的卷积、上采样和下采样操作全部替换为循环边界（wrap-around）版本，使生成器天然输出可平铺的SVBRDF贴图；同时引入条件编码器，将用户提供的结构图案映射为特征图注入解码器，实现结构布局与外观风格（随机潜码）的解耦。训练时辅以平移等变损失$L_{\mathrm{shift}}$，强制生成器对输入平移保持等变，进一步巩固平铺一致性。在逆向渲染阶段，TileGen采用基于Gram矩阵的全局风格损失替代像素级损失，结合优化过程中对材质贴图的随机平移，在匹配目标照片外观的同时避免过拟合，从而重建出干净、可平铺且可编辑的材质。

实验表明，TileGen在单张闪光照片的SVBRDF重建任务上显著优于已有方法，生成的材质贴图无高光伪影、可无缝平铺，且支持通过条件图案控制结构。即使在非平铺数据集上训练，其无条件模型仍能产生无缝纹理，而MaterialGAN不能。消融实验证实，仅替换损失函数而不修改架构无法消除伪影与不可平铺问题，验证了循环架构设计与条件控制机制的关键作用。

## 核心方法与创新机理

### 问题瓶颈与核心思路

现有基于GAN的材质生成方法（如MaterialGAN）存在一个根本性缺陷：生成器架构本身不保证输出的空间周期性（平铺性），导致生成的材质贴图在重复拼接时出现明显接缝。同时，从单张照片逆向重建材质时，基于像素级损失（如L1）的优化方案容易将闪光灯高光“烧入”材质贴图，产生不可编辑的伪影，且重建结果同样不可平铺。这些限制使得现有方法难以直接嵌入游戏、影视等需要无缝纹理和可控编辑的内容创作流程。

TileGen的核心洞察是：**通过将网络架构中的基础操作替换为循环边界版本，可以隐式地强制生成器输出天然可平铺的材质贴图，无需依赖训练数据集本身的可平铺性**。在此基础上，引入条件编码器将材质的结构布局与外观风格解耦，并结合基于全局风格损失的逆向渲染优化，在匹配单张照片外观的同时避免像素级过拟合，实现可平铺、可编辑的材质重建。

### 网络架构与模块设计

TileGen以StyleGAN2为骨架，在三个关键维度上进行了架构改造，形成条件版本和无条件版本两条生成路径。图2展示了条件版本的完整架构。

**模块1：循环边界操作替换（平铺性保证机制）**

这是TileGen最根本的架构变革。将StyleGAN2中所有的卷积（Convolution）、上采样（Upsampling）和下采样（Downsampling）操作替换为对应的wrap-around版本。所谓wrap-around，即卷积核在特征图边界处进行循环索引，使得左边界与右边界、上边界与下边界在计算上等价。这一替换的因果效应是：生成器在任意位置输出的特征天然满足周期性边界条件，无论输入的随机潜码如何变化，生成的材质贴图在空间上始终无缝可平铺。

关键证据来自Fig.9：即使在一个本身不可平铺的数据集上训练，TileGen的无条件模型仍能生成无缝的2×2平铺纹理，而原始MaterialGAN在相同数据集上训练后，平铺结果出现明显的接缝断裂。这证明平铺性源于架构本身的归纳偏置，而非数据集的统计特性。

**模块2：条件编码器（结构与风格解耦机制）**

条件版本的TileGen引入了一个受CollageGAN启发的编码器网络，但做了关键修改。编码器将用户提供的结构图案$p$（如砖缝布局、皮革纹理的颗粒分布）映射为特征图$\phi$，该特征图直接注入生成器解码器的初始层（分辨率32×32），取代StyleGAN2原本的可学习常量张量。

与CollageGAN的根本区别在于：TileGen的随机潜码$z$独立于输入图案$p$，从标准正态分布中随机采样，经映射网络转换为风格向量$w$后，通过AdaIN调制各层特征。这一设计实现了**结构（由$p$控制）与外观风格（由$z$控制）的完全解耦**：给定同一结构图案，不同潜码产生风格各异但布局一致的材质实例（Fig.3）；反之，给定同一潜码，不同结构图案则改变材质的空间组织。

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2206_05649/figures/003_Figure_3.jpg]]
*Figure 3: Randomly sampled conditional materials from the tile and leather classes.We feed the conditional pattern on the left to TiLEGeN,along with four different random latent vectors*

**模块3：平移等变损失$L_{\text{shift}}$（条件控制强化机制）**

仅使用对抗损失训练条件模型时，实验发现模型会将部分结构变化“烘焙”进潜码$z$，削弱条件图案对结构的控制力。为此，引入平移等变损失：

$$L_{\text{shift}} = || T(\mathcal{G}(p, z, \xi)) - \mathcal{G}(T(p), z, T(\xi)) ||_1$$

其中$\mathcal{G}$为生成器，$T$为随机平移操作，$\xi$为噪声向量。该损失强制生成器满足平移等变性：将生成结果平移，应与将输入图案和噪声平移后再生成的结果一致。这一约束的因果效应是：生成器无法将空间位置信息编码进潜码$z$，因为任何位置变化都必须通过输入图案$p$的平移来驱动，从而确保$p$是结构控制的唯一来源。

**模块4：判别器**

判别器接收生成的SVBRDF贴图（及对应的条件图案），判断其真伪。训练时，生成的材质贴图和条件图案一起被随机平移后送入判别器，与平移等变损失形成协同：生成器必须学会在任何平移位置都产生判别器认可的材质，进一步强化平铺性。

**模块5：可微渲染器与逆向渲染优化**

在逆向渲染阶段，目标是从单张闪光照片$I$中恢复材质贴图。TileGen不直接优化潜码$z$，而是在W+N空间中优化风格向量$w^+$和噪声向量$\xi$的拼接向量$\pmb{u}$：

$$\pmb{u}^{*} = \arg \min_{\pmb{u}} \mathcal{L}(\mathcal{R}(\mathcal{G}(\pmb{u}, \pmb{p})), I)$$

其中$\mathcal{R}$为可微渲染器，根据生成的漫反射、法线、粗糙度、高光等贴图合成闪光照明下的图像。

损失函数$\mathcal{L}$的设计是避免高光烧入伪影的关键。主要损失项为基于VGG网络的Gram矩阵风格损失，它匹配生成渲染图与目标照片的全局纹理统计特征，而非逐像素值。配合下采样后的L1损失以保持低频结构一致性。优化过程中，每隔一次迭代对生成的材质贴图施加随机平移——这一操作只有在生成器本身输出可平铺材质时才有意义，因为平移后的贴图在循环边界下仍代表同一材质，优化器可以自由选择最佳对齐位置，避免将照片中的高光位置“刻死”在材质贴图的固定坐标上。

### 训练与推理路径

**训练阶段**：条件模型需要成对的SVBRDF参数贴图与条件图案作为监督数据。每个材质语义类（砖瓦、皮革、石头、金属）单独训练一个网络，使用4块NVIDIA V100 GPU训练数天，输出分辨率512×512。无条件模型仅需材质贴图数据，训练流程与StyleGAN2类似但使用循环操作。

**推理阶段**：无条件生成时，随机采样潜码$z$即可获得多样化的可平铺材质。条件生成时，用户提供结构图案$p$，配合随机潜码$z$控制风格变化。逆向渲染时，固定生成器权重，在W+N空间中优化$\pmb{u}$，每张目标图像约需两分钟。

### 关键因果链路总结

循环操作替换 → 隐式平铺性保证 → 无需数据集可平铺性依赖 → Fig.9验证

条件编码器 + 独立潜码 → 结构与风格解耦 → 可控生成与编辑 → Fig.3验证

平移等变损失$L_{\text{shift}}$ → 强制结构控制唯一性 → 避免潜码“烘焙”结构信息

全局风格损失 + 随机平移优化 → 避免像素级过拟合 → 消除高光烧入伪影 + 逆向结果可平铺 → Fig.8、Fig.10验证

Fig.10的消融实验提供了决定性证据：仅将MaterialGAN的损失函数替换为全局风格损失，但保持其原始架构不变，结果仍然存在高光烧入伪影且不可平铺。这说明**架构的循环操作替换和逆向渲染中的随机平移策略是TileGen有效性的必要条件**，单纯改变损失函数无法弥补架构层面的缺陷。

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2206_05649/figures/007_Figure_7.jpg]]
*Figure 7: Demonstration of tileability for both inverse rendering (two top rows) and randomly sampled results (two bottom rows). The leftmost image is either the target for inverse rendering or the original generated material for randomly sampling,followed by a rerendered image using tiled texture maps and the corresponding tiled texture maps.The results show seamless tileability (periodicity) of our resulting textures,even though the target image is not tileable in the inverse rendering examples*

## 实验与关键发现

### 主结果：单张照片SVBRDF重建的视觉质量与可平铺性

TILEGEN在单张手机闪光照片的材质逆向重建任务上，与三类代表性方法进行了定性比较：基于深度学习的**Deschaintre等人**（2018）、基于GAN数据增强的**Zhou和Kalantari**（2021），以及无条件GAN基准**MaterialGAN**（Guo et al., 2020b）。结果显示，TILEGEN生成的材质贴图（漫反射、法线、高光、粗糙度等）干净且无高光烧入伪影，而所有基线方法均不同程度地将闪光高光“烧入”了材质贴图中，导致渲染结果不可复用（Fig.8）。更重要的是，TILEGEN重建的材质具有天然的可平铺性，即使在目标照片本身不可平铺的情况下，也能输出无缝拼接的纹理（Fig.7），而MaterialGAN等方法无法做到这一点。

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2206_05649/figures/008_Figure_8.jpg]]
*Figure 8: Comparison with three SVBRDF estimation approaches [Deschaintre et al.2018; Guo et al.2020b; Zhou and Kalantari 2021] on SVBRDF capture from a single target image (left).All of these approaches generate unclean feature maps,baking in the flash highlight.In contrast,our material maps and re-renderings are clean and plausible*

在材质生成任务上，TILEGEN的条件模型能够根据输入的结构图案保持布局一致性，同时通过随机潜码产生风格多变的材质实例（Fig.3）；无条件模型则在特定材质类内表现出丰富的多样性（Fig.4）。这赋予了TILEGEN在内容创作流程中的直接可用性——既可控制结构，又可探索外观。

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2206_05649/figures/004_Figure_4.jpg]]
*Figure 4: Randomly sampled unconditional materials from the stone and metal classes,showing the diversity of the results within each class.The corresponding texture maps are shown in supplementary materials*

### 关键消融：架构平铺设计与损失函数的作用

**消融一：仅替换损失函数不足以解决问题。**
为验证架构平铺设计的关键性，作者将MaterialGAN的像素级损失替换为TILEGEN所用的全局风格损失（基于VGG的Gram矩阵），但保持MaterialGAN原有的非平铺架构不变。结果表明，即使使用非像素级的全局损失，MaterialGAN仍会产生高光烧入伪影，且输出材质不可平铺（Fig.10）。这证明，仅靠损失函数的改变无法消除伪影和实现平铺性——将卷积、上采样、下采样操作全部替换为wrap-around（循环边界）版本，从架构层面强制网络输出周期性信号，才是实现无缝平铺的根本原因。

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2206_05649/figures/010_Figure_10.jpg]]
*Figure 10: Comparison to the original MaterialGAN optimized with our global loss.Even when using a non pixel-wise loss,the results of MaterialGAN present highlight baking artifacts and are not tileable,unlike our results*

**消融二：平移一致性损失（shift loss）对条件控制至关重要。**
在训练条件模型时，若仅使用对抗损失而不加入平移一致性损失$L_{\mathrm{shift}}$，模型会将部分材质结构的变化“烘焙”进潜码$z$中（Sec.3.4），从而削弱条件图案$p$对结构的控制力。$L_{\mathrm{shift}}$通过强制生成器对输入平移具有等变性——即$|| T(\mathcal{G}(p, z, \xi)) - \mathcal{G}(T(p), z, T(\xi)) ||_1$——确保结构信息仅由条件图案决定，而风格变化完全由潜码和噪声控制，实现了结构与外观的有效解耦。

**消融三：非平铺数据集上的平铺性验证。**
将TILEGEN的无条件模型与MaterialGAN在相同的非平铺数据集上训练后，TILEGEN仍能生成无缝平铺的纹理，而MaterialGAN不能（Fig.9）。这表明TILEGEN的平铺性不依赖于训练数据本身是否平铺，而是由架构中的循环操作隐式保证的。

![[assets/figures/papers/paper_list_l94_https_arxiv_org_abs_2206_05649/figures/009_Figure_9.jpg]]
*Figure 9: Comparison of randomly sampled results of original MaterialGAN and our unconditional model trained on the same non-tileable dataset MaterialGAN was trained on,showing 2x2 tiled results and the corresponding tiled material maps.Even when trained with a non-tileable dataset,our unconditional model can produce seamless texture maps*

### 逆向渲染优化的设计有效性

TILEGEN的逆向渲染不直接优化潜码$z$，而是在$\mathcal{W}^+\mathcal{N}$空间优化风格向量$\mathbf{w}^+$和噪声向量$\xi$的组合$\mathbf{u}^* = \arg \min_{\mathbf{u}} \mathcal{L}(\mathcal{R}(\mathcal{G}(\mathbf{u}, \mathbf{p})), I)$。损失函数以基于VGG的Gram矩阵风格损失为主，辅以下采样的L1损失，并在优化过程中每隔一次迭代对材质贴图施加随机平移。这种设计使得优化过程匹配的是目标图像的全局风格纹理，而非逐像素精确对齐，从而避免了将目标照片中的高光、阴影等非材质固有属性过拟合到材质贴图中。同时，随机平移操作进一步强化了生成结果在空间上的平铺一致性。

### 适用边界与限制

1. **类别依赖性**：每个材质语义类（砖瓦、皮革、石头、金属）需要单独训练一个网络，且需要足量的各类别真值SVBRDF数据。这限制了方法向新材质类别的快速扩展。
2. **计算开销**：当前条件生成器输出分辨率为512×512，训练需要4块NVIDIA V100 GPU运行数天；逆向渲染优化每张目标图像约需两分钟，虽已可用但在交互式应用中仍有提速空间。
3. **材质类别覆盖有限**：当前仅支持四类材质，尚未验证在更多样化材质类别（如木材、织物、地形等）上的有效性。
4. **条件图案的平铺性要求**：对于条件模型，输入的结构图案必须是平铺的（周期性的），否则会破坏输出材质的平铺性（Sec.5）。这要求用户提供或生成周期性的结构图案作为条件输入。

### 证据强度评估

- Fig.8的视觉比较（与三种基线方法在单张图像重建上的对比）提供了强定性证据，置信度0.95，清晰展示了TILEGEN在避免高光伪影方面的优势。
- Fig.9的平铺性对比（非平铺数据集训练后与MaterialGAN比较）直接验证了架构设计的因果作用，置信度0.95。
- Fig.10的损失函数消融（MaterialGAN+全局损失 vs. TILEGEN）排除了“仅靠损失函数即可解决问题”的替代假说，置信度0.95。
- 平移一致性损失的消融分析基于作者的经验观察（Sec.3.4），虽未提供独立的可视化对比图，但其作用机制在理论上是清晰的，置信度0.9。

需要注意的是，所有主结果均为定性视觉比较，未提供定量指标（如PSNR、SSIM、LPIPS等）。这在材质生成和逆向渲染领域是常见做法——因为真值材质贴图难以获取，且像素级指标往往与感知质量不一致——但仍需读者在评估时考虑这一方法学特点。

## 定位与知识库关联

TILEGEN 的核心定位是**将材质生成从“随机纹理合成”推向“可平铺、可控、可逆向重建”的内容创作工具**。与现有工作的本质差异体现在三个关键 slot 的改变上，每个 slot 都对应着知识库中的一个明确挂载点。

### 改变的 Slot 一：卷积边界处理——从标准 padding 到 wrap-around

**基线状态**：MaterialGAN（Guo et al., 2020b）基于 StyleGAN2 的标准卷积操作，使用零填充或镜像填充，生成的材质贴图在边界处不连续，无法平铺。

**TILEGEN 的改变**：将生成器和判别器中所有卷积、上采样、下采样操作替换为 wrap-around（循环边界）版本（Sec. 3.1）。这一修改使得网络在架构层面天然保证输出的周期性——无论输入如何，生成的材质贴图在任意位置拼接时都无缝连续。

**知识库挂载点**：这一设计属于 **“架构诱导的等变性”** 范式，与传统的后处理平铺（如基于拼接的纹理合成）或数据驱动的平铺（要求训练集本身可平铺）有本质区别。TILEGEN 即使训练在非平铺数据集上，无条件模型仍能输出无缝纹理（Fig. 9），证明了架构层面的平铺约束比数据层面的约束更强。

### 改变的 Slot 二：条件注入方式——从纯随机潜码到结构-风格解耦

**基线状态**：MaterialGAN 仅使用随机潜码 z 控制生成，无法指定材质的结构布局；CollageGAN（Li et al., 2021）虽然引入了条件编码器，但其潜码 z 依赖于条件图案 p，导致结构与风格耦合。

**TILEGEN 的改变**：引入 CollageGAN 风格的条件编码器，将输入的结构图案 p 映射为特征图 ϕ，直接注入生成器的初始层（替换 StyleGAN2 的可学习常量张量），而潜码 z 仍从正态分布随机采样，独立于 p（Sec. 3.2）。这使得**结构（来自 p）与外观风格（来自 z）完全解耦**——给定同一结构图案，不同 z 产生风格多变但布局一致的材质（Fig. 3）。

**知识库挂载点**：这一设计属于 **“条件GAN的解耦控制”** 研究方向，挂载在条件注入的早期层（32×32 分辨率）与风格调制的分离机制上。与 SPADE（Park et al., CVPR 2019）等语义图像合成方法不同，TILEGEN 的条件编码器不使用空间自适应归一化，而是直接替换初始常量，使得结构信息在生成过程的最早期就被锚定。

### 改变的 Slot 三：逆向渲染损失——从像素级匹配到全局风格匹配

**基线状态**：Deschaintre et al.（2018）和 Zhou & Kalantari（2021）等单图像 SVBRDF 重建方法使用像素级损失（如 L1），导致网络试图逐像素拟合目标照片，将闪光高光“烧入”材质贴图（产生不可重光照的伪影），且重建结果不可平铺。

**TILEGEN 的改变**：逆向渲染优化使用基于 VGG 的 Gram 矩阵风格损失作为主损失项，结合下采样后的 L1 损失，并在优化过程中对材质贴图施加随机平移（Sec. 4）。风格损失匹配的是纹理的全局统计特征而非精确像素值，避免了高光伪影的过拟合；随机平移则进一步强化了平铺一致性。

**知识库挂载点**：这一设计属于 **“基于感知损失的逆向图形学”** 范式，与传统的像素级逆向渲染优化有本质区别。关键洞察在于：风格损失天然容忍空间偏移，恰好与平铺材质所需的平移等变性兼容。Fig. 10 的消融实验直接证明了这一点——即使将 MaterialGAN 的损失替换为 TILEGEN 的全局风格损失，由于 MaterialGAN 的架构不支持平铺，仍会产生高光烧入伪影且不可平铺。这说明**架构平铺设计是风格损失发挥作用的必要条件**。

### 适用边界与限制

1. **类别依赖**：每个材质语义类（砖瓦、皮革、石头、金属）需要单独训练一个网络，且需要足够的各类别真值 SVBRDF 数据。这限制了向新材质类别的快速扩展。
2. **分辨率与计算成本**：当前生成器分辨率为 512×512，条件模型训练需要 4 块 NVIDIA V100 GPU 数天；逆向渲染优化每张图像约需两分钟。
3. **条件图案的平铺性要求**：条件模型要求输入的结构图案本身是周期性的（tileable），否则 shift loss 无法有效约束。

### 后续启发与知识库价值

TILEGEN 为知识库提供了以下可复用的设计原则：

- **架构层面的等变性约束比损失函数约束更可靠**：Fig. 9 和 Fig. 10 共同证明了，仅靠损失函数（即使是非像素级的风格损失）无法实现平铺，必须在架构中嵌入 wrap-around 操作。
- **结构与风格的解耦注入点选择**：将条件信息注入生成器的初始常量层（而非通过空间自适应归一化），是实现结构-风格分离的有效策略，尤其适用于需要精确结构控制的纹理生成任务。
- **风格损失在逆向渲染中的独特优势**：Gram 矩阵损失对局部空间偏移的不敏感性，使其天然适配可平铺材质的逆向重建，这一发现可推广到其他需要全局外观匹配但允许局部形变的逆向图形学问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/TileGen_Tileable_Controllable_Material_Generation_and_Capture.pdf]]