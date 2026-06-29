---
title: "DiLightNet: Fine-grained Lighting Control for Diffusion-based Image Generation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/DiLightNet_Fine_grained_Lighting_Control_for_Diffusion_based_Image_Generation.pdf
project_link: null
code_link: "https://github.com/iamNCJ/DiLightNet"
aliases:
- DDLC
- DiLightNet
tags:
- SIGGRAPH_2024
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入基于粗糙几何估计的radiance hints（漫反射与多级镜面反射）作为条件信号，将其与学习到的暂定图像编码进行通道级乘法后注入扩散模型，从而在无需精确三维几何的情况下实现对光照强度与分布的精细引导。
primary_logic: 扩散模型的采样分布已蕴含不同光照条件下的外观变化，因此仅需近似的radiance hints即可将去噪过程引导至符合目标光照的方向，让模型自身补全缺失的几何和材质细节。
claims:
- 用户研究显示DiLightNet在光照相似性（19.61）上与正样本基线（19.85）无显著差异，且显著优于负样本基线（12.25）。
- 在合成测试集上，完整模型达到PSNR 22.97、SSIM 0.8249、LPIPS 0.1165，优于直接拼接radiance hints的ControlNet变体。
- 消融实验证实编码后乘法（encoded multiplication）是保留纹理的关键，而直接拼接或未编码乘法均导致质量下降。
- 训练时对着色法线进行扰动（模拟深度估计的平滑法线）是弥合合成域与估计域差距的最关键数据增强。
---

# DiLightNet: Fine-grained Lighting Control for Diffusion-based Image Generation

> [!tip] 核心洞察
> 扩散模型的采样分布已蕴含不同光照条件下的外观变化，因此仅需近似的radiance hints即可将去噪过程引导至符合目标光照的方向，让模型自身补全缺失的几何和材质细节。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiLightNet: 面向扩散图像生成的细粒度光照控制 |
| 英文题名 | DiLightNet: Fine-grained Lighting Control for Diffusion-based Image Generation |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://dilightnet.github.io/) · [Code](https://github.com/iamNCJ/DiLightNet) |
| Topic | #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | DiLightNet (Diffusion Lighting ControlNet) |
| Dataset | Synthetic test set, User study - lighting similarity, User study - appearance consistency under rotated lighting |

> [!tip] 效果简介
> - Synthetic test set (50 objects × 3 viewpoints × 6 lightings) 上，PSNR / SSIM / LPIPS 22.97 / 0.8249 / 0.1165 (DiLightNet) vs 22.82 / 0.8216 / 0.1212 (Direct ControlNet) (+0.15 / +0.0033 / -0.0047)。
> - User study - lighting similarity 上，average total rating 19.61 (DiLightNet) vs 19.85 (positive baseline) / 12.25 (negative baseline) (接近positive baseline (-0.24); 显著优于negative baseline (+7.36))。
> - User study - appearance consistency under rotated lighting 上，average total rating 25.75 (DiLightNet) vs 25.05 (positive baseline) / 11.35 (negative baseline) (略优于positive baseline (+0.70); 显著优于negative baseline (+14.40))。

## 概要

扩散模型在文本到图像生成中表现出色，但其内部存在固有的光照偏见，且光照与图像内容高度纠缠——文本提示难以精细描述复杂光照的空间分布，导致用户无法独立控制生成图像的光照效果。DiLightNet 提出了一种三阶段解决方案：首先生成无光照控制的暂定图像；随后在粗糙几何估计上渲染 radiance hints（漫反射与三级镜面反射图），将其与暂定图像的编码特征进行通道级乘法后注入 ControlNet，引导扩散模型重合成前景以匹配目标光照；最后补全与前景光照一致的背景。其核心洞察在于：扩散模型的采样分布已蕴含不同光照下的外观变化，仅需近似的 radiance hints 即可将去噪过程引导至正确方向，无需精确三维几何。

在合成测试集上，DiLightNet 达到 PSNR 22.97、SSIM 0.8249、LPIPS 0.1165，优于直接拼接 radiance hints 的 ControlNet 变体。用户研究表明，该方法在光照相似性评分（19.61）上与正样本基线（19.85）无显著差异，且显著优于负样本基线（12.25）。该方法定位于扩散模型的细粒度条件控制领域，以近似几何估计替代精确三维重建，为光照可控生成提供了实用且高效的新范式。

## 核心方法与创新机理

### 问题瓶颈：扩散模型中的光照-内容纠缠

扩散模型在文本到图像生成中存在两个根本性问题。其一，模型内部存在**固有的光照偏见**——在缺乏明确光照描述时，绝大多数生成图像会被单一光源模式（如正面闪光灯）主导（Figure 2）。其二，**光照与图像内容在生成过程中高度纠缠**：文本提示虽可粗略描述光照（如“warm light”），但缺乏对光照空间分布、强度、颜色等属性的细粒度表达能力，用户无法独立控制“物体是什么”和“物体如何被照亮”。

![[assets/figures/papers/paper_list_l16_https_dilightnet_github_io/figures/002_Figure_2.jpg]]
*Figure 2: Examples of lighting bias in diffusion-based image generation. Left: a batch of 12 images (text prompt: “a photo of a soccer ball” ). The majority of the images are lit by a flash light; only two exhibit off-center lighting (3rd row, 1st column and 3rd column). Right: a batch of generated images of a robot dominated by light coming from either the front-left or front-right (text prompt: “a photo of a toy robot standing on a wooden table” ; images are generated with a depth conditioned model to ensure a consistent shape)*

### 核心洞察：近似几何引导即可重定向去噪轨迹

DiLightNet的核心洞察在于：扩散模型的采样分布已经蕴含了同一物体在不同光照条件下的外观变化。因此，**不需要精确的三维几何和完整材质信息**即可实现光照控制——仅需提供近似的radiance hints，将去噪过程“指向”目标光照方向，扩散模型自身的生成能力会补全缺失的几何细节和材质-光照交互。这一洞察将问题从“精确重光照”降维为“条件引导生成”，使方法得以在仅依赖现成深度估计器的条件下工作。

### 三阶段管线架构

DiLightNet采用三阶段管线（Figure 3），各阶段之间存在明确的因果依赖关系：

![[assets/figures/papers/paper_list_l16_https_dilightnet_github_io/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our pipeline for lighting-controlled prompt-driven image synthesis: (1) We start by generating a provisional image using a pretrained diffusion model under uncontrolled lighting given a text prompt and a content-seed. (2) Next, we pass an appearance-seed, the provisional image, and a set of radiance hints (computed from the target lighting and a coarse estimate of the depth) to DiLightNet that will resynthesize the image such that becomes consistent with the target lighting while retaining the content of the provisional image. (3) Finally, we inpaint the background to be consistent with foreground object and the target lighting*

**阶段一：暂定图像生成。** 给定文本提示和内容种子（content-seed），使用预训练的Stable Diffusion（Rombach et al., CVPR 2022）在无光照控制的条件下生成一幅暂定图像。该图像确定了物体的语义内容和大致形状，但其光照由扩散模型隐式决定，不服从用户控制。此阶段输出的暂定图像将作为阶段二的内容锚点。

**阶段二：DiLightNet重合成。** 这是方法的核心创新所在，包含三个关键子模块：

1. **粗糙几何估计**：利用现成的前景分割网络（U2Net或SAM）和单目深度估计器（ZoeDepth）从暂定图像中提取前景蒙版和深度图。深度图经过三角化生成网格，再通过拉普拉斯平滑处理以模拟深度估计器输出的平滑法线特性——这一平滑操作是弥合合成训练域与真实估计域差距的关键步骤。

2. **Radiance Hints渲染**：在平滑后的粗糙网格上，使用Disney BRDF模型（Burley, 2012）渲染4个光照提示图——1个纯漫反射（roughness=1.0）和3个不同粗糙度（0.34, 0.13, 0.05）的镜面反射。这些radiance hints编码了目标光照在“假设物体为标准材质”条件下的空间分布，为扩散模型提供了光照方向和强度的像素级引导信号。选择4个hints而非更多或更少，是基于消融实验的最优配置（Table 1 rows 4-6）。

3. **编码乘法注入**：这是DiLightNet区别于朴素ControlNet变体的核心changed slot。暂定图像首先通过一个可训练的编码器提取为12通道特征图，然后与4通道的radiance hints进行**通道级乘法**（channel-wise multiplication），乘积结果作为条件输入ControlNet（Zhang et al., ICCV 2023）。乘法操作的意义在于：它使得radiance hints能够**调制**暂定图像特征的每个通道，而非简单地将两者作为并列信息源。这一设计确保了光照条件与图像内容在特征空间中深度融合，同时保留了暂定图像的纹理细节。消融实验（Figure 6）证实，直接拼接（Direct ControlNet）或未编码乘法均会导致纹理丢失或光照不一致。

![[assets/figures/papers/paper_list_l16_https_dilightnet_github_io/figures/009_Figure_6.jpg]]
*Figure 6: Ablation comparison of different architecture variants that: (1) directly pass the radiance hints and provisional image (without multiplication) to ControlNet, and (2) multiply the radiance hints with the non-encoded provisional image. DiLightNet’s encoded multiplication generates visually more plausible results*

阶段二还引入两个辅助控制信号：**前景蒙版**作为额外输入通道，减少边缘伪影；**外观种子**（appearance-seed）允许用户在不改变文本提示的情况下，对材质-光照交互的解释（如光泽度）进行采样。

**阶段三：背景补全。** 使用预训练的stable-diffusion-2-inpainting模型，以阶段二输出的前景合成图像和逆蒙版为条件，生成与目标光照环境一致的背景。前景与背景通过3×3均值滤波平滑后的蒙版进行合成。

### 关键Changed Slots及其因果机制

**Changed Slot 1：光照条件传递方式。** 基线方法仅通过文本提示传递光照信息，空间分辨率为零。DiLightNet将其替换为radiance hints——在粗糙几何上渲染的像素级光照分布图。这一改变使得光照控制从“语义描述”升级为“空间引导”，因果链为：目标光照→粗糙几何渲染→radiance hints→空间调制→去噪方向引导。

**Changed Slot 2：条件信号融合方式。** 基线ControlNet将条件信号直接拼接为额外通道。DiLightNet引入“编码后乘法”机制：暂定图像编码→12通道特征×4通道hints→ControlNet输入。乘法操作建立了光照与内容的**调制关系**而非并列关系，使得网络学习到“在特定光照下该纹理应如何变化”的映射，而非“同时看到内容和光照”的简单组合。

**Changed Slot 3：所需几何精度。** 传统重光照方法依赖精确三维几何。DiLightNet将需求降级为“现成深度估计器+拉普拉斯平滑”即可，其因果机制为：扩散模型已内化几何-光照交互的先验，radiance hints仅需提供大致正确的光照方向，模型自身会补全缺失的法线细节。

### 训练策略与数据增强

训练数据来自Objaverse三维物体数据集，在Blender中渲染多种光照条件下的ground truth。训练时的关键数据增强包括：对着色法线进行扰动以模拟深度估计的平滑法线（**正常增强**，移除后PSNR从22.97降至21.88，Table 1 row 10）、颜色增强和材质增强。这些增强共同弥合了合成训练域与真实估计域之间的分布差距。训练使用8×NVidia V100 GPU，耗时约30小时。

### 推理路径

推理时，用户提供文本提示、目标光照环境图和可选的外观种子。系统依次执行：暂定图像生成→前景分割+深度估计→radiance hints渲染→DiLightNet重合成→背景补全。整个流程无需精确三维扫描或人工标注几何，仅依赖现成视觉模型即可完成。

## 实验与关键发现

### 定量评估

DiLightNet在合成测试集（50个物体 × 3个视点 × 6种光照条件，共900个测试样本）上进行了系统评估。完整模型取得了**PSNR 22.97、SSIM 0.8249、LPIPS 0.1165**的最佳结果（Table 1）。相较于直接将radiance hints与暂定图像拼接后输入ControlNet的Direct ControlNet变体（PSNR 22.82、SSIM 0.8216、LPIPS 0.1212），DiLightNet在全部三项指标上均有提升，其中LPIPS的改善（-0.0047）表明感知质量上的优势。测试时每种组合选取LPIPS最低的外观种子，模拟用户在实际使用中的优选行为。

### 用户研究

为验证光照控制的主观质量，研究招募了20名非专家参与者进行两项用户研究。所有图像背景统一替换为目标环境光以避免干扰，图像顺序随机化。

**光照相似性评估**：参与者对DiLightNet生成图像与ground truth参考图像的光照相似性进行打分。DiLightNet的平均总评分为**19.61**，与正样本基线（ground truth图像，19.85）无显著差异（差值仅-0.24），且显著优于负样本基线（12.25，差值+7.36）。这表明用户难以区分DiLightNet生成的光照效果与真实渲染结果。

**旋转光照下的外观一致性**：在固定内容但旋转光照的条件下，DiLightNet的平均总评分为**25.75**，甚至略优于正样本基线（25.05，+0.70），远超负样本基线（11.35，+14.40）。这一结果证实了DiLightNet在保持物体外观一致性的同时，能准确响应光照方向的变化。

### 决定性消融实验

**架构设计的因果验证**（Table 1 rows 1-3, Figure 6）：编码乘法（encoded multiplication）是DiLightNet的核心设计。消融实验对比了三种架构变体：(1) 直接将radiance hints与暂定图像拼接输入ControlNet（Direct ControlNet），PSNR降至22.82；(2) 将radiance hints与未编码的暂定图像进行乘法，PSNR进一步降至22.37。DiLightNet的编码乘法（先将暂定图像通过编码器提取12通道特征，再与radiance hints做通道级乘法）在所有指标上均最优，证实了编码步骤对保留纹理信息和正确融合光照提示至关重要。

**Radiance Hints数量的最优选择**（Table 1 rows 4-6）：采用4个radiance hints（1个纯漫反射 + 3个粗糙度分别为0.34、0.13、0.05的镜面反射）取得了最佳性能。仅使用1个漫反射hint时PSNR降至22.49；增加至7个hints时PSNR为22.62，均不及4个hints的配置。这表明适度的镜面反射层次能有效引导模型理解不同粗糙度下的光照-材质交互，但过多的hints会引入冗余信息。

**前景蒙版的必要性**（Table 1 rows 7-8）：将前景分割蒙版作为额外输入通道可有效抑制边缘伪影。移除蒙版后PSNR降至22.23（-0.74），尤其在复杂轮廓区域出现明显的边界不一致。

**数据增强的关键作用**（Table 1 rows 9-12）：训练时对着色法线进行扰动以模拟深度估计产生的平滑法线，是最关键的数据增强策略。移除该增强后PSNR骤降至**21.88**（-1.09），证实了弥合合成域（精确几何）与估计域（粗糙深度）差距的必要性。颜色增强和材质增强的移除也分别导致PSNR降至22.67和22.79，进一步验证了数据多样性对模型泛化的重要性。

### 间接材质控制

DiLightNet提供了两种无需更改光照条件的材质控制途径：

**外观种子采样**（Figure 4）：改变外观种子可引导模型对暂定图像中的材质产生不同解释。例如，在文本提示未充分约束材质时（如“leather gloves”），不同外观种子可产生从哑光到高光泽度的皮革质感变化，本质上是在扩散模型的采样分布中对材质-光照交互进行重采样。

**提示词特化**（Figure 5）：在第二阶段向文本提示添加材质描述（如“paper made”、“mirror polished metallic”），可在固定光照条件下独立控制材质外观。这为无需精确三维几何即可实现材质编辑提供了实用接口。

### 失败模式与适用边界

尽管DiLightNet在光照控制上表现优异，但存在以下明确边界：

1. **材质控制的间接性**：用户只能通过文本提示间接影响材质，无法精确指定BRDF参数。当文本描述与实际光照交互产生歧义时（如“shiny”在不同光照下可产生截然不同的高光模式），生成结果可能与用户意图存在偏差。

2. **深度估计依赖**：方法依赖现成的深度估计器（ZoeDepth）和前景分割网络（U2Net/SAM）。当这些网络产生严重错误（例如透明物体、细薄结构的深度歧义，或复杂轮廓的分割失败）时，radiance hints的几何基础将偏离真实形状，导致光照引导失效或产生伪影。

3. **跨帧一致性缺失**：在固定内容种子下改变光照时，生成的各帧之间可能存在轻微的形状变化。这是因为扩散模型的采样过程本身具有随机性，且DiLightNet未引入显式的跨帧一致性约束，因此不适合直接用于视频或动态光照序列。

4. **风格限制**：当前设计假设图像风格为物理光照交互（照片级写实），radiance hints基于Disney BRDF模型渲染。该方法不支持卡通渲染、超现实或其他非物理的艺术风格，因为radiance hints的光学假设在这些风格下不再成立。

5. **前景-背景分离假设**：管线假设前景对象可被清晰分割，且背景可通过inpainting独立生成。对于前景与背景高度融合的场景（如透过玻璃的折射、环境雾效），该分离策略可能导致视觉不连贯。

### 扩展验证

**真实照片重光照**（Figure 7）：通过跳过第一阶段、直接将真实照片作为暂定图像输入DiLightNet，该方法可近似实现单张图像重光照。这展示了radiance hints引导机制对真实世界图像的泛化能力，但论文未提供该场景的定量评估，其鲁棒性仍需进一步验证。

**深度条件模型的改进**（Figure 8）：当提供参考深度图作为额外输入（使用深度条件扩散模型）时，生成质量进一步提升，表明更精确的几何信息可直接转化为更好的光照控制效果，为未来绕过深度估计步骤提供了方向。

![[assets/figures/papers/paper_list_l16_https_dilightnet_github_io/figures/006_Figure_5.jpg]]
*Figure 5: Impact of prompt specialization in DiLightNet. Instead of altering the appearance-seed, the user can also specialize the prompt with additional material information in the 2nd stage. In this example the initial prompt (“toy robot” ) is augmented with additional material descriptions while keeping the (point lighting) fixed*

![[assets/figures/papers/paper_list_l16_https_dilightnet_github_io/figures/004_Figure_4.jpg]]
*Figure 4: Impact of changing the appearance-seed. If not sufficiently constrained by the text prompt, the generated provisional image (left) might not provide sufficient information for DiLightNet to determine the exact materials of the object. Altering the appearance-seed directs DiLightNet to sample a different interpretation of light-matter interaction in the provisional image. In this example, altering the appearance-seed induces changes in the interpretation of the glossiness and smoothness of the leather gloves*

![[assets/figures/papers/paper_list_l16_https_dilightnet_github_io/figures/007_Figure_8.jpg]]
*Figure 8: Lighting control results for a depth-controlled textto-image diffusion model improves the quality of the results by providing a depth map as additional input*

## 定位与知识库关联

**相对于已有方法的本质差异**

DiLightNet 在文本到图像扩散模型的条件下控制范式中，改变了“光照信息传递方式”这一关键 slot。此前的方法（如 **Stable Diffusion**，Rombach et al., CVPR 2022）仅通过文本提示描述光照（例如“warm light from left”），这种方式无法精确指定光照的空间分布、强度衰减和镜面高光位置，且扩散模型内部存在固有的光照偏见——多数生成结果倾向于正面闪光灯照明（Figure 2）。DiLightNet 的核心改变在于：将光照条件从模糊的文本描述替换为空间显式的 radiance hints——在粗糙几何代理上渲染的漫反射与多级镜面反射图——从而使模型能够接收像素级的光照分布信号。

第二个被改变的 slot 是“条件信号与图像特征的融合机制”。直接的做法是将 radiance hints 与暂定图像作为额外通道拼接到 **ControlNet**（Zhang et al., ICCV 2023）中（即 Direct ControlNet），但实验表明这种方式会导致纹理退化。DiLightNet 引入了一个编码器将暂定图像映射为 12 通道特征，再与 radiance hints 进行通道级乘法后注入 ControlNet。这种“编码后乘法”的融合策略是保留原图纹理与施加光照引导之间的关键平衡机制。

第三个被改变的 slot 是“所需几何精度”。传统上，基于物理的重光照需要精确的三维几何和材质估计。DiLightNet 的核心洞察在于：扩散模型的采样分布已经蕴含了不同光照下的外观变化，因此仅需近似的 radiance hints 即可将去噪过程引导至正确方向，让模型自身补全缺失的几何和材质细节。这使得系统可以仅依赖现成的深度估计器（ZoeDepth）和前景分割网络（U2Net/SAM）产出的粗糙几何，而不需要任何精确的三维重建。

**知识库挂载点**

DiLightNet 在知识库中的挂载点位于“扩散模型条件控制”与“图像重光照”两个领域的交叉处。

在扩散模型条件控制维度，它直接继承并扩展了 ControlNet 的架构范式。ControlNet 通过复制 UNet 编码器并注入额外条件信号来实现可控生成，DiLightNet 在此框架上增加了“编码后乘法”的融合模块，为条件信号与内容特征的交互提供了新的设计空间。这一设计模式可泛化至其他需要精细空间控制的条件生成任务（如法线引导、材质引导）。

在图像重光照维度，DiLightNet 与传统方法（需要精确几何和逆渲染）形成互补。传统重光照方法追求物理精确性，但在几何不可靠时容易产生严重伪影；DiLightNet 则通过扩散模型的生成能力容忍几何近似误差，牺牲了一定的物理精确性换取了鲁棒性。它与 **Alchemist** 等材质感知扩散模型形成自然的知识互补——后者可提供更精细的材质控制，而 DiLightNet 提供光照控制，两者结合有望实现光照与材质的双向独立控制。

**适用边界**

DiLightNet 的适用边界受以下因素约束：

1. **对象类型**：主要针对孤立前景对象设计，依赖前景分割网络将对象与背景分离。对于复杂场景中多个交互对象的光照控制，当前方法未提供解决方案。

2. **风格约束**：假设生成图像的风格为物理光照交互（如照片级写实），不支持卡通、超现实等艺术风格，因为 radiance hints 基于物理渲染模型（Disney BRDF）生成。

3. **跨帧一致性**：在固定内容种子下改变光照时，生成的各帧之间可能存在轻微的形状变化，缺乏跨帧一致性，因此不适合直接用于视频或动态光照变换序列。

4. **深度估计依赖**：方法依赖现成深度估计器的输出质量。当深度估计产生严重错误（如低频歧义导致形状扭曲）时，radiance hints 的引导方向会出现偏差，生成结果可能不够理想。

5. **材质控制间接性**：用户只能通过文本提示间接控制材质，或通过外观种子采样不同的材质解释，无法直接指定材质的物理参数（如粗糙度、金属度）。

**后续启发**

DiLightNet 的核心思想——用近似物理信号引导扩散模型去噪方向——具有超出光照控制的推广价值。这一范式暗示：对于任何可以从粗糙几何或简单物理模型近似计算出的视觉属性（如环境光遮蔽、间接光照、次表面散射），都可以采用类似的“近似信号 + 扩散模型补全”策略实现可控生成，从而绕过精确物理模拟的计算瓶颈。

在单图像重光照方向，Figure 7 展示了跳过第一阶段、直接注入真实照片作为暂定图像的可行性，这为将 DiLightNet 发展为通用的单图像重光照工具提供了概念验证。后续工作可以探索如何提高对捕获照片中未知光照和材质的鲁棒性。

在三维内容生成方向，该方法的核心思想可以推广至文本到 3D 物体生成：在优化过程中用近似 radiance hints 引导扩散模型的评分蒸馏，有望在无需精确几何的情况下实现兼具丰富材质和一致光照的 3D 资产创建。

在系统简化方向，一个开放问题是能否进一步减少对外部深度/分割网络的依赖，直接从扩散模型内部特征推断几何信息，形成一个端到端的可控生成系统。这需要探索扩散模型中间层特征与场景几何之间的对应关系。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/DiLightNet_Fine_grained_Lighting_Control_for_Diffusion_based_Image_Generation.pdf]]