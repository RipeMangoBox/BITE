---
title: "DreamMat: High-quality PBR Material Generation With Geometry- and Light-aware Diffusion Models"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/DreamMat_High_quality_PBR_Material_Generation_With_Geometry_and_Light_aware_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- DreamMat
tags:
- SIGGRAPH_2024
- topic/graphics_geometry_processing
- topic/graphics_rendering_materials
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过微调一个以几何（深度/法向）和光照（预定义材质渲染图）为条件的2D扩散模型，并在蒸馏时随机选取预定义HDR环境图，强制生成图像与给定光照一致，从而解耦材质与光照。
primary_logic: 大规模扩散模型在蒸馏不同步骤时隐含未知环境光，造成材质分解的不确定性。DreamMat通过固定环境光并训练光照感知扩散模型，确保蒸馏过程中的光照一致性，从而准确估计材质参数，消除反照率中的烘焙效果。
claims:
- 定性比较显示，TEXTure和Fantasia3D生成的反照率包含烘焙的光照阴影，而DreamMat的反照率无此伪影，新光照下渲染真实。
- 用户研究（42名被试）中，DreamMat在总体质量、反照率、粗糙度、金属度及渲染质量等所有指标上均获最高评分，总体质量4.39/7。
- 消融实验（图8）证明，完整的几何与光照感知扩散模型结合随机环境光选择才能生成最佳材质；缺少光照条件或使用固定环境光均导致反照率残留高光。
- 用户研究（42份反馈） 上 总体质量 (1-7分) = 4.39
---

# DreamMat: High-quality PBR Material Generation With Geometry- and Light-aware Diffusion Models

> [!tip] 核心洞察
> 大规模扩散模型在蒸馏不同步骤时隐含未知环境光，造成材质分解的不确定性。DreamMat通过固定环境光并训练光照感知扩散模型，确保蒸馏过程中的光照一致性，从而准确估计材质参数，消除反照率中的烘焙效果。

| 字段 | 内容 |
|------|------|
| 中文题名 | DreamMat：基于几何与光照感知扩散模型的高质量PBR材质生成 |
| 英文题名 | DreamMat: High-quality PBR Material Generation With Geometry- and Light-aware Diffusion Models |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](http://www.cad.zju.edu.cn/home/jin/Sig20242/DreamMat.htm) |
| Topic | #topic/graphics_geometry_processing #topic/graphics_rendering_materials #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DreamMat |
| Dataset | 用户研究（42份反馈）, 50个文本提示，10个网格 |

> [!tip] 效果简介
> - 用户研究（42份反馈） 上，总体质量 (1-7分) 4.39 vs TANGO / TEXTure / Text2Tex / Fantasia3D (最高分，显著优于所有基线)。
> - 50个文本提示，10个网格 上，CLIP Score 80.28 vs 所有基线方法（TANGO, TEXTure, Text2Tex, Fantasia3D） (最高，优于所有基线)；FID 114.97 vs 所有基线方法 (最低，优于所有基线)。

## 概要

为三维物体生成高质量PBR材质是计算机图形学中的核心挑战。现有方法借助2D扩散模型进行材质蒸馏，但由于扩散模型仅被训练生成最终着色图像，缺乏对材质属性的显式约束，导致反照率图中残留高光和阴影，材质分解呈病态。

DreamMat提出了一种几何与光照感知的材质生成框架。其核心思路是：微调一个以几何（深度/法向）和光照（预定义材质渲染图）为条件的2D扩散模型，使其生成的图像与给定光照环境一致；在蒸馏过程中，每次迭代从预定义HDR环境光集合中随机选取光照，强制生成图像与该光照匹配，从而解耦材质与光照，消除反照率中的烘焙效果。

实验表明，DreamMat在用户研究（42名被试）中总体质量得分4.39/7，显著优于TANGO、TEXTure、Text2Tex和Fantasia3D；在50个文本提示、10个网格上的CLIP Score（80.28）和FID（114.97）均达最优。消融实验证实，完整的几何与光照感知扩散模型配合随机环境光选择是生成高质量材质的关键。该方法不支持透明或次表面散射等复杂材质，蒸馏耗时约18分钟，对极端光照条件的泛化能力有限。

## 核心方法与创新机理

### 问题瓶颈与核心思路

现有文本到3D材质生成方法（如TEXTure、Fantasia3D）的核心瓶颈在于：它们蒸馏的2D扩散模型仅被训练用于生成最终的着色图像，缺乏对材质属性与光照的显式解耦约束。这导致蒸馏出的反照率（albedo）图中残留高光和阴影等“烘焙”光照效果，材质分解呈现病态。如图2所示，TEXTure生成的RGB纹理包含大量着色信息，在新环境光下渲染时出现错误；Fantasia3D直接蒸馏材质与光照，反照率同样残留光照伪影。

DreamMat的核心洞察是：大规模扩散模型在蒸馏不同步骤时隐含了未知的环境光假设，造成了材质分解的不确定性。因此，DreamMat通过两个关键设计来打破这一瓶颈：（1）训练一个**光照感知的2D扩散模型**，显式地将环境光作为条件输入；（2）在蒸馏过程中**固定并随机选取预定义的HDR环境光**，强制生成图像与给定光照一致，从而将材质与光照解耦。

### 方法框架与模块因果链

DreamMat的整体流水线（图4）由五个核心模块串联构成，形成“表示→渲染→扩散先验→蒸馏优化→平滑正则”的闭环。

#### 模块一：材质表示（哈希网格编码）

DreamMat采用Instant-NGP的哈希网格表示 $\Gamma_\theta$ 存储空间变化的BRDF参数。对于表面上任意点 $\mathbf{p}$，材质参数通过下式计算：

$$(\mathbf{c}, \alpha, m) = \Gamma_{\theta}(\mathbf{p})$$

其中 $\mathbf{c}$ 为反照率（albedo），$\alpha$ 为粗糙度（roughness），$m$ 为金属度（metalness）。选择哈希网格编码而非传统的位置编码（positional encoding）是一个关键的**changed slot**：消融实验（图19）表明，位置编码会产生轴对齐的伪影，且收敛速度较慢；哈希网格编码则能生成更平滑、无伪影的反照率图，并加速优化过程。

#### 模块二：可微渲染（蒙特卡洛重要性采样）

从材质表示到图像的渲染过程采用重要性驱动的蒙特卡洛采样策略，将渲染方程分离为漫反射和镜面反射两个分量：

$$L(\mathbf{p}, \omega_{\mathbf{o}}) = \int_{\Omega} L_i(\omega_{\mathbf{i}}) f(\omega_{\mathbf{i}}, \omega_{\mathbf{o}}) (\omega_{\mathbf{i}} \cdot \mathbf{n}) d\omega_i$$

其中 $L_i$ 为入射环境光辐射度，$f$ 为简化的Disney BRDF。这一分离策略使得渲染过程可微，梯度能够从渲染图像反向传播至材质参数 $\theta$，为后续的蒸馏优化提供基础。渲染时使用的环境光从预定义的HDR环境光集合中随机选取——这是DreamMat**第二个关键的changed slot**（相比Fantasia3D等使用固定或联合优化环境光的方法）。

#### 模块三：几何与光照感知扩散模型（核心创新）

这是DreamMat**最核心的changed slot**。标准Stable Diffusion仅以深度或法向作为几何条件，缺乏对光照的显式建模。DreamMat在ControlNet框架下微调扩散模型，构建了一个22通道的条件图（图5）：

- **几何条件**：渲染的深度图和法向图（提供物体的几何信息）
- **光照条件**：6种预定义材质（如纯漫反射、纯镜面反射等）在给定环境光下的渲染结果（提供该光照下的着色先验）

这一设计的因果逻辑是：通过将6种“标准材质”在特定光照下的渲染图作为条件，扩散模型学会了在给定光照下生成与几何一致的图像，而不再隐含地推断未知的环境光。图3直观展示了这一差异：标准深度条件扩散模型生成的图像与给定环境光不一致，而DreamMat的光照感知模型生成的图像与给定光照高度一致。这为后续蒸馏提供了可靠的光照一致性先验。

#### 模块四：CSD蒸馏损失（分类器分数蒸馏）

DreamMat采用改进的CSD（Classifier Score Distillation）损失替代传统的SDS损失，这是**第三个关键的changed slot**。CSD损失的核心公式为：

$$\delta(I_t) = \eta_1 \epsilon_{\phi}(I_t; y_{\mathrm{pos}}, t) + (\eta_2 - \eta_1) \epsilon_{\phi}(I_t; t) - \eta_2 \epsilon_{\phi}(I_t; y_{\mathrm{neg}}, t)$$

其中 $I_t$ 为加噪后的渲染图像，$\epsilon_{\phi}$ 为扩散模型的去噪预测，$y_{\mathrm{pos}}$ 为正文本提示（描述期望材质），$y_{\mathrm{neg}}$ 为负提示（如“过饱和、不真实”），$\eta_1$ 和 $\eta_2$ 为权重系数。相比SDS仅使用正提示和空提示，CSD通过引入负提示来“推开”不期望的属性，有效抑制了过饱和问题（图9）。

蒸馏梯度通过链式法则传递至材质参数：

$$\nabla_{\boldsymbol{\theta}} \mathcal{L}_{\mathrm{Distill}} = \mathbb{E}_t \left[ \delta(I_t) \frac{\partial I}{\partial \boldsymbol{\theta}} \right]$$

这一模块的关键因果链路是：扩散模型提供的损失信号 $\delta(I_t)$ 通过渲染图像的梯度 $\partial I / \partial \boldsymbol{\theta}$ 反向传播至哈希网格表示，驱动材质参数向符合文本描述且与给定光照一致的方向优化。消融实验（图14）进一步揭示，条件图必须同时应用于CSD损失的三个组件（正提示、空提示、负提示）；若仅应用于部分组件，会导致色调失真。

#### 模块五：材质平滑损失

为消除材质参数中的噪声伪影，DreamMat引入了平滑正则项：

$$\mathcal{L}_{\mathrm{smooth}} = ||\Gamma_{\theta}(\mathbf{p}) - \Gamma_{\theta}(\mathbf{p} + \epsilon)||^2$$

该损失鼓励相邻表面点的材质参数（反照率、粗糙度、金属度）相似，使材质更平滑。用户可通过调整平滑系数控制纹理细节的保留程度（图16消融实验）。

### 训练与推理路径

**训练阶段**：DreamMat首先在Objaverse数据集上微调光照感知扩散模型。训练数据通过渲染大量3D模型在随机环境光下的图像构建，条件图包含深度、法向及6种预定义材质的渲染结果。扩散模型学会在给定几何和光照条件下生成一致的图像。

**推理/蒸馏阶段**：对于给定的无纹理网格和文本描述，DreamMat执行以下迭代过程（约4000步，Adam优化器，学习率0.01）：
1. 从哈希网格表示中查询表面点的BRDF参数
2. 从预定义HDR环境光集合中随机选取一个环境光
3. 使用蒙特卡洛渲染生成图像
4. 向渲染图像添加噪声，通过光照感知扩散模型去噪
5. 计算CSD损失和材质平滑损失，反向传播更新哈希网格参数

ControlNet的控制尺度初始设为1.0，在700步后逐渐衰减至0.8，以在优化后期放松几何约束，允许更灵活的材质生成。

### 关键设计决策的因果验证

消融实验（图8）系统验证了各模块的因果贡献：
- **完整模型**（几何+光照条件 + 随机环境光）：反照率无烘焙阴影，新光照下渲染真实
- **仅几何条件**（移除光照条件）：反照率残留大量高光和阴影
- **固定环境光**（非随机选取）：反照率仍残留光照伪影，泛化性下降
- **联合蒸馏材质与光照**（图15）：材质与光照高度纠缠，反照率保留大量光照信息

这些消融结果共同证明了DreamMat的核心因果机制：光照感知扩散模型与随机环境光策略的协同作用是实现材质-光照解耦的必要条件，二者缺一不可。

![[assets/figures/papers/paper_list_l17_http_www_cad_zju_edu_cn_home_jin_Sig20242_DreamMat_htm/figures/005_Figure_4.jpg]]
*Figure 4: Overview of our pipeline. DreamMat distills a diffusion model to generate PBR materials. We first use Monte Carlo sampling to render images of the object from its material representation and a randomly-selected predefined environment light. Then, we train the material representation by CSD loss on rendered images using a geometry- and light-aware diffusion model*

## 实验与关键发现

### 主结果：用户研究与定量评估

DreamMat 在材质生成质量上全面超越现有基线方法。论文通过用户研究和自动化指标两种方式进行了验证。

**用户研究（Table 1）** 共收集42份反馈（来自37位用户），评估维度涵盖总体质量、反照率质量、粗糙度质量、金属度质量、光照/材质解耦质量以及新光照下的渲染质量。DreamMat 在所有维度上均获得最高评分，其中总体质量得分 **4.39/7**，显著优于 TANGO、TEXTure、Text2Tex 和 Fantasia3D。特别在反照率质量上，DreamMat 获得 **4.65/7**，而基线方法得分均明显偏低——这直接印证了核心瓶颈：现有方法生成的反照率图中残留了烘焙的光照阴影和高光，而 DreamMat 通过光照感知蒸馏有效消除了这一伪影。

**定量评估（Table 2）** 在50个文本提示、10个不同网格上计算 CLIP Score 和 FID。DreamMat 的 CLIP Score 达到 **80.28**，FID 为 **114.97**，两项指标均优于所有基线方法。CLIP Score 衡量渲染图像与文本提示的语义一致性，FID 衡量生成外观与真实材质分布的距离，双指标领先说明 DreamMat 不仅在语义匹配上更准确，其生成的材质在分布层面也更接近真实材质。

**定性比较（Fig. 2, Fig. 6）** 直观展示了差异：TEXTure 生成的是包含光照信息的 RGB 纹理，在新环境光下渲染时出现错误着色；Fantasia3D 直接蒸馏材质和光照，反照率中明显嵌入了环境光的高光和阴影。DreamMat 的反照率图干净无伪影，在新光照下渲染结果真实可信。

### 关键消融实验

消融实验系统验证了 DreamMat 各设计组件的因果贡献。

**几何与光照感知扩散模型 + 随机环境光选择（Fig. 8）** 是最关键的消融。完整模型生成的反照率无残留光照信息，渲染质量最佳。当移除光照条件（仅使用几何条件）时，扩散模型无法感知给定环境光，蒸馏出的反照率出现明显阴影和高光残留。当使用固定单一环境光替代随机选取策略时，模型对特定光照过拟合，泛化到新光照时材质质量下降。这验证了核心洞察：蒸馏过程中光照一致性是材质解耦的必要条件，随机环境光策略迫使模型学习光照无关的材质表示。

**CSD 损失 vs. SDS 损失（Fig. 9）** 表明，标准 SDS 损失会导致生成结果过饱和、细节模糊。CSD 损失通过引入负提示（negative prompt）和退火策略，在保持语义一致性的同时抑制了过饱和，产生更真实的外观细节。这是 DreamMat 相比早期基于 SDS 蒸馏方法的重要改进。

**条件图应用策略（Fig. 14）** 进一步揭示了蒸馏损失设计的精细之处：条件图（几何+光照）必须同时应用于 CSD 损失的三个组件——正提示去噪、空提示去噪和负提示去噪。若仅应用于部分组件，会导致色调失真或材质与光照解耦不彻底。这说明扩散模型的去噪过程在不同提示条件下对条件信息的依赖程度不同，统一施加条件约束是保证一致性的关键。

**材质平滑损失（Fig. 16）** 有效消除了反照率图中的噪声伪影，使材质过渡更自然。用户可通过调整平滑系数控制纹理细节程度，在平滑度和细节保留之间取得平衡。

**哈希网格编码 vs. 位置编码（Fig. 19）** 显示，位置编码在低频设置下会产生轴对齐伪影，而哈希网格编码不仅避免了该问题，且收敛速度更快，验证了材质表示选择的合理性。

**直接联合蒸馏材质和光照（Fig. 15）** 的失败案例进一步强化了核心论点：若不使用预定义环境光而直接联合优化材质参数和环境光，材质与光照高度纠缠，反照率中保留大量光照信息，材质分解失败。这从反面证明了预定义环境光策略的必要性。

### 失败模式与适用边界

尽管 DreamMat 在 PBR 材质生成上取得了显著进展，但仍存在明确的适用边界：

1. **材质类型受限**：当前方法仅支持简化 Disney BRDF 模型（反照率、粗糙度、金属度），不支持透明、高反射（如镜面）、次表面散射等复杂材质属性。对于需要这些属性的场景（如玻璃、皮肤），方法不适用。

2. **光照泛化有限**：蒸馏过程依赖有限的预定义 HDR 环境光集合（6种预定义材质在给定光照下的渲染图作为条件）。对于极端或与训练分布差异较大的未见光照条件，生成材质在新光照下的渲染质量可能下降。这本质上是光照感知扩散模型的条件分布外推问题。

3. **计算成本高**：单次材质生成约需 **18分钟**，无法满足实时或交互式创作需求。时间瓶颈主要来自每步迭代的蒙特卡洛渲染和扩散模型去噪。

4. **域间隙**：使用简化 Disney BRDF 与部分训练数据（Objaverse）中的着色模型存在域间隙。论文指出这一影响有限，但未提供定量分析，该点需要手动验证。

5. **全局光照缺失**：未建模间接光照和全局光照效应，生成的材质在复杂光照场景（如室内多反射）中可能表现不物理准确。

这些边界条件为后续研究指明了方向：扩展材质类型、引入间接光照、加速蒸馏过程、以及用数据驱动先验替代预定义环境光以减少对特定光图的依赖。

![[assets/figures/papers/paper_list_l17_http_www_cad_zju_edu_cn_home_jin_Sig20242_DreamMat_htm/figures/012_Figure_9.jpg]]
*Figure 9: Comparison between the vanilla SDS loss, the vanilla CSD loss, and our method. (a) Materials generated with vanilla SDS loss [Poole et al. 2022] and geometry condition. (b) Material generated using vanilla CSD loss [Yu et al. 2023b] with geometry condition. (c) Materials generated by our method which combines the CSD loss with our geometry- and light-aware diffusion model*

![[assets/figures/papers/paper_list_l17_http_www_cad_zju_edu_cn_home_jin_Sig20242_DreamMat_htm/figures/018_Figure_14.jpg]]
*Figure 14: (a) Our result, incorporating condition maps concurrently to*

![[assets/figures/papers/paper_list_l17_http_www_cad_zju_edu_cn_home_jin_Sig20242_DreamMat_htm/figures/003_Figure_2.jpg]]
*Figure 2: Generated albedo and rendering results in the same environment light. (a) TEXTure [Yu et al. 2023a] generates an RGB texture map containing shading effects, leading to incorrect renderings in a new environment. (b) Fantasia3D [Chen et al. 2023a] directly distills a diffusion model to generate materials, which still contain unwanted shading effects in albedo. (c) Our method can generate correct materials, allowing for more photorealistic renderings in a new environment*

![[assets/figures/papers/paper_list_l17_http_www_cad_zju_edu_cn_home_jin_Sig20242_DreamMat_htm/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison. We compared our method to TANGO [Chen et al. 2022a], TEXTure [Yu et al. 2023a], Text2Tex [Chen et al. 2023c], and Fantasia3D [Chen et al. 2023a]. We use NvDiffRec [Munkberg et al. 2022] to decompose the texture map produced by TEXTure and Text2Tex. Each object has three images: the albedo map on the left, the rendered image on the top right, and the roughness map on the bottom right*

![[assets/figures/papers/paper_list_l17_http_www_cad_zju_edu_cn_home_jin_Sig20242_DreamMat_htm/figures/010_Table_2.jpg]]
*Table 2: Quantitative results. We use 50 different text prompts on 10 meshes to generate appearances and calculate the CLIP score (similarity between rendered views and text prompts) and FID (distribution’s distance between rendered images from the generated appearances and the generated images by Stable Diffusion) to assess the text fidelity and visual quality of the generated appearances*

## 定位与知识库关联

DreamMat 的核心定位是**为无纹理的3D网格生成高质量、物理可分离的PBR材质**，其相对于已有工作的本质差异在于将材质蒸馏过程中的光照条件从“隐式且不确定”转变为“显式且可控”。这一转变通过修改两个关键 slot 实现：

1. **扩散模型 slot**：从标准 Stable Diffusion（深度/法向条件）或无条件模型，变为**几何与光照感知的微调扩散模型**（ControlNet，22通道条件图，包含深度、法向及6种预定义材质在给定光照下的渲染图）。这使得扩散模型在蒸馏时能够“看到”当前环境光下的着色结果，从而将光照一致性内化为模型的生成先验。

2. **环境光策略 slot**：从固定单一环境光（如 **Fantasia3D**（Chen et al., 2023a））或无光照约束，变为**每次蒸馏迭代从预定义HDR环境光集合中随机选取**。这一随机化策略迫使材质表示学习与光照无关的固有属性，而非记忆特定光照下的着色模式。

这两个 slot 的协同改变构成了 DreamMat 的因果引擎：**光照感知扩散模型提供光照一致的生成先验，随机环境光选择消除材质对特定光照的过拟合**，二者共同解耦了材质与光照这一长期病态问题。

### 相对于已有方法的本质差异

与 **TEXTure**（Yu et al., 2023a）和 **Text2Tex**（Chen et al., 2023c）等文本引导的RGB纹理生成方法相比，DreamMat 不生成包含烘焙光照的RGB纹理，而是直接输出反照率、粗糙度和金属度贴图。TEXTure/Text2Tex 的输出需要通过 **NvDiffRec**（Munkberg et al., 2022）进行后处理材质分解，该过程本身就是病态的，分解结果往往残留光照伪影（Fig. 2a）。DreamMat 在蒸馏阶段即通过光照感知扩散模型强制光照一致性，从源头消除了反照率中的烘焙阴影和高光。

与 **Fantasia3D**（Chen et al., 2023a）相比，关键差异在于光照策略。Fantasia3D 在蒸馏过程中使用固定环境光，导致生成的材质与该环境光高度纠缠——反照率图中保留了大量光照信息，换用新光照时渲染结果失真（Fig. 2b）。DreamMat 的随机环境光策略打破了这种纠缠，使得材质参数真正成为表面固有属性。

与 **TANGO**（Chen et al., 2022a）相比，DreamMat 在材质表示和蒸馏损失上均有改进。TANGO 使用 MLP + 位置编码表示材质，而 DreamMat 采用哈希网格编码（Instant-NGP），避免了位置编码中常见的轴对齐伪影，且收敛更快（Fig. 19）。蒸馏损失方面，DreamMat 使用 CSD 损失（Classifier Score Distillation）配合退火负提示，相比 TANGO 等使用的 SDS 损失（Score Distillation Sampling），显著减少了过饱和问题，生成更真实的外观（Fig. 9）。

### 知识库挂载点

DreamMat 在知识库中的主要挂载点包括：

- **材质与光照解耦**：这是计算机图形学和视觉中的经典问题。DreamMat 通过扩散模型先验实现解耦，其核心思想——在蒸馏过程中显式控制光照条件——可追溯到本征图像分解的传统方法，但利用了大规模扩散模型的生成能力作为正则化手段。

- **扩散模型蒸馏**：DreamMat 继承并改进了 Score Distillation Sampling（SDS）范式（Poole et al., 2022），通过引入分类器分数蒸馏（CSD）和负提示机制，提升了蒸馏质量。这一改进对后续基于扩散模型的3D生成工作具有参考价值。

- **ControlNet 条件生成**：DreamMat 将 ControlNet 的条件通道从标准的深度/法向/边缘扩展至**材质渲染图**，展示了如何通过设计条件图将扩散模型适配到特定物理过程（渲染方程）。这种“物理条件注入”的思路可推广至其他需要物理一致性的生成任务。

- **神经渲染与可微渲染**：DreamMat 使用可微的蒙特卡洛渲染器连接材质表示与扩散模型，这一架构使整个管线端到端可训练。哈希网格编码（Instant-NGP）的采用则体现了神经场表示在材质建模中的优势。

### 适用边界与局限性

DreamMat 的适用边界由以下因素界定：

1. **材质类型限制**：使用简化的 Disney BRDF，不支持透明、高反射（如镜面）、次表面散射等复杂材质属性。对于玻璃、水、皮肤等材质类型，方法需要扩展 BRDF 模型。

2. **光照泛化能力**：蒸馏过程依赖预定义的HDR环境光集合，对极端或未见光照条件（如强方向光、点光源）的泛化能力有限。环境光集合的覆盖范围直接决定了方法的鲁棒性。

3. **计算成本**：生成时间约18分钟（4,000步优化），无法满足实时或交互式应用需求。这一限制源于蒸馏过程需要反复渲染和扩散模型推理。

4. **全局光照缺失**：未建模间接光照和全局光照效应，渲染结果在复杂场景中可能缺乏物理真实性。

5. **训练数据域间隙**：微调扩散模型使用的 Objaverse 数据集中部分模型采用不同的着色模型，与 Disney BRDF 存在域间隙，尽管论文指出影响有限。

### 后续工作启发

DreamMat 为后续研究提供了以下方向：

- **更丰富的材质模型**：将方法扩展到更复杂的 BRDF 模型（如全 Disney Principled BRDF）或支持次表面散射、透明等材质类型，需要解决蒸馏过程中参数空间增大带来的优化困难。

- **数据驱动先验替代预定义光图**：当前方法依赖人工预定义的环境光集合，后续可探索从大规模光照数据集中学习光照先验，减少对特定光图的依赖，提升泛化能力。

- **加速蒸馏过程**：18分钟的生成时间限制了交互式应用，可通过模型蒸馏、渐进式优化、或利用更高效的扩散模型推理技术来加速。

- **引入间接光照**：在可接受的计算成本下引入间接光照和全局光照效应，将显著提升渲染结果的物理真实性，但需要解决可微渲染的效率和梯度传播问题。

- **多物体场景扩展**：当前方法针对单个物体，扩展到多物体场景需要考虑物体间的光照交互和材质一致性。

总体而言，DreamMat 通过**在扩散模型蒸馏过程中显式建模光照条件**这一核心创新，为文本引导的PBR材质生成建立了新的范式。其成功的关键在于认识到：材质蒸馏的病态性源于扩散模型对光照的隐式编码，而解决之道是将光照从隐式变量提升为显式可控条件。这一洞察对任何涉及物理属性解耦的生成任务都具有方法论层面的启示意义。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/DreamMat_High_quality_PBR_Material_Generation_With_Geometry_and_Light_aware_Diffusion_Models.pdf]]