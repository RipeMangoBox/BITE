---
title: "CLIP-Mesh: Generating textured meshes from text using pretrained image-text models"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/CLIP_Mesh_Generating_textured_meshes_from_text_using_pretrained_image_text_models.pdf
project_link: null
code_link: "https://github.com/NasirKhalid24/CLIP-Mesh"
aliases:
- CM
- CLIP-Mesh
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过Loop细分曲面隐式正则化、可微渲染下的CLIP余弦相似度损失以及扩散先验，共同优化网格控制顶点、纹理图与法线图；同时引入随机背景、位置偏移和高分辨率渲染等增强策略，迫使优化偏向形状变形而非单纯纹理绘制。
primary_logic: 将3D网格生成转化为可微渲染图像的文本-图像嵌入对齐问题：利用预训练CLIP的零样本评分能力与Loop细分的隐式平滑性，让网格形状和纹理在无3D监督下直接通过梯度优化收敛到与文本描述一致的结果。
claims:
- 在153个COCO标题的生成上，CLIP-Mesh在CLIP R-Precision指标上全面超过Dreamfields，如ViT-B/16生成+ViT-B/16评估下达到96.7 vs. 93.5。
- 消融实验表明，逐步加入Loop细分、背景增强、位置偏移、高分辨率渲染和扩散先验损失均能单调提升R-Precision，验证了各个组件的有效性。
- COCO caption object generation (153 captions) 上 CLIP R-Precision (↑) = 96.7
- COCO caption object generation (153 captions) 上 CLIP R-Precision (↑) = 91.4
---

# CLIP-Mesh: Generating textured meshes from text using pretrained image-text models

> [!tip] 核心洞察
> 将3D网格生成转化为可微渲染图像的文本-图像嵌入对齐问题：利用预训练CLIP的零样本评分能力与Loop细分的隐式平滑性，让网格形状和纹理在无3D监督下直接通过梯度优化收敛到与文本描述一致的结果。

| 字段 | 内容 |
|------|------|
| 中文题名 | CLIP-Mesh：利用预训练图文模型从文本生成带纹理网格 |
| 英文题名 | CLIP-Mesh: Generating textured meshes from text using pretrained image-text models |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2203.13333) · [Code](https://github.com/NasirKhalid24/CLIP-Mesh) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CLIP-Mesh |
| Dataset | COCO caption object generation |

> [!tip] 效果简介
> - COCO caption object generation (153 captions) 上，CLIP R-Precision (↑) 96.7 vs 93.5 (+3.2)；CLIP R-Precision (↑) 91.4 vs 86.6 (+4.8)。

## 概要

**问题**：零样本条件下直接从文本生成带纹理、可直接部署为标准网格资产的3D模型极具挑战——既无3D监督数据可用，又需避免形状混乱与纹理伪影。

**方法**：CLIP-Mesh将3D网格生成转化为可微渲染图像的文本-图像嵌入对齐问题。其核心思路是：以Loop细分曲面的控制顶点、纹理图与法线图为优化变量，通过可微渲染器生成多视角图像，利用预训练CLIP模型的余弦相似度损失、扩散先验损失以及拉普拉斯形状正则化进行梯度优化，同时引入随机背景、位置偏移和高分辨率渲染等增强策略，迫使优化偏向形状变形而非单纯纹理绘制。

**主要结果**：在153个COCO标题的对象生成上，CLIP-Mesh的CLIP R-Precision全面超越Dreamfields（如ViT-B/16评估下96.7 vs. 93.5），且单张P100 GPU仅需50分钟，速度提升约100倍。消融实验证实，Loop细分、背景增强、位置偏移、高分辨率渲染和扩散先验损失均能单调提升性能。

**定位**：该方法属于基于预训练视觉-语言模型的零样本3D生成范式，以网格表示为载体，区别于NeRF隐式表示路线，适用于需要直接输出标准网格资产的下游应用。

## 核心方法与创新机理

CLIP-Mesh 的核心技术路线是将零样本文本驱动3D网格生成转化为一个**可微渲染下的文本-图像嵌入对齐优化问题**。整个系统无需任何3D监督数据，仅依赖预训练的CLIP模型的零样本跨模态评分能力，通过梯度反向传播同时优化网格形状、纹理和法线表示，使渲染图像与文本描述在CLIP嵌入空间中趋于一致。

### 瓶颈与核心机制

该任务的根本瓶颈在于：在没有任何3D真值监督的条件下，直接从文本生成可部署为标准网格资产（含纹理）的3D模型，且必须避免形状混乱和纹理伪影。CLIP-Mesh 的应对策略是将问题分解为三个相互耦合但可独立优化的子问题——形状表示、外观表示和优化约束——并通过**Loop细分曲面的隐式正则化**和**多层级随机增强**迫使优化过程偏向真实的形状变形而非单纯的纹理绘制捷径。

### 管线模块与因果关系

CLIP-Mesh 的优化管线由七个关键模块串联构成，形成从参数化表示到损失反馈的完整梯度回路：

**1. Loop细分控制网格（形状表示）**  
系统不直接优化普通三角网格顶点，而是优化一个粗糙控制网格的顶点 $V_0 \in \mathbb{R}^{n \times 3}$，并通过解析可微的Loop细分方案 $V = S(V_0)$ 生成极限曲面。这一设计构成第一个关键changed slot：相比Dreamfields直接优化普通网格顶点，Loop细分曲面天然防止三角形翻转并平滑形状，充当隐式正则化器。消融实验证实，仅添加Loop细分即可将R-Precision从75.8提升至77.7（ViT-B/16评估）。

**2. 纹理图与法线图（外观表示）**  
外观与几何解耦为独立的纹理图 $T$ 和法线图 $\tilde{T}$。这一设计允许在优化过程中选择性冻结形状或纹理，为多物体场景中的部分固定形状优化提供灵活性。与Dreamfields的简单着色相比，分离表示使纹理细节不干扰几何优化梯度。

**3. 可微渲染器**  
采用基于Laine et al. (2020)的可微渲染器，从采样相机位姿 $p$ 渲染图像，要求提供抗锯齿梯度以确保反向传播的数值稳定性。渲染器将当前形状、纹理和法线合成为2D视图，作为CLIP编码器的输入。

**4. CLIP编码器与损失函数**  
渲染图像经CLIP图像编码器编码为嵌入向量 $e_i$，文本提示经文本编码器编码为 $e_t$。核心优化目标为负平均余弦相似度：

$$L_{CLIP}(V, T, \tilde{T}, p) = -\frac{1}{K} \sum_{e_i \in E} e_i^T e_t$$

该损失驱动渲染视图在CLIP语义空间中逼近文本描述，是整个优化的首要驱动力。

**5. 拉普拉斯正则化**  
为防止网格在优化中退化（如顶点飞散或自交），引入均匀拉普拉斯算子约束：

$$\delta_i = v_i - \frac{1}{|N_i|} \sum_{j \in N_i} v_j$$

$$L_\delta = \frac{1}{N} \sum_{i=1}^{N} \| \delta_i \|^2$$

该损失使每个顶点趋近其一邻域平均位置，保持网格局部平滑。关键设计在于拉普拉斯权重 $\lambda_t$ 采用指数衰减策略：

$$\lambda_t = (\lambda_{t-1} - \lambda_{min}) \cdot 10^{-kt} + \lambda_{min}$$

早期强正则化防止初始大梯度破坏网格拓扑，后期弱正则化释放形状细节表达能力。

**6. 扩散先验损失**  
为缓解CLIP损失可能导致的对抗性纹理模式，引入基于扩散模型的图像嵌入先验。给定文本嵌入，扩散先验采样生成合理的CLIP图像嵌入 $\hat{e}_k$，并施加额外约束：

$$L_{PRIOR}(V, T, \tilde{T}, p) = -\frac{1}{K} \sum_{e_i \in E} e_i^T \hat{e}_k$$

该损失引导渲染图像的嵌入不偏离文本描述对应的“合理图像”分布，消融实验中添加扩散先验后R-Precision从62.7跃升至77.7（B/32评估），贡献显著。

**7. 随机增强策略**  
为防止CLIP利用背景或位置等捷径线索而非形状信息进行评分，系统在每次渲染时随机化三个要素：
- **随机背景**：在高斯噪声、纯色和棋盘格之间随机切换，阻止CLIP将背景纹理与物体语义关联。
- **随机位置偏移**：将物体从图像中心随机平移，迫使优化关注物体轮廓而非固定位置特征。消融显示该策略贡献最大，将R-Precision从81.0提升至90.1。
- **高分辨率渲染后缩放**：以512×512渲染后缩放至224×224送入CLIP，提供更丰富的梯度信息。该策略对多数CLIP模型有效，但对ViT-L/14有负面影响。

### 总优化目标

上述模块整合为统一的可微优化框架：

$$\min_{V_0, T, \tilde{T}} L_{CLIP}(S(V_0), T, \tilde{T}, p) + \lambda_t L_\delta(V) + \alpha L_{PRIOR}(S(V_0), T, \tilde{T}, p)$$

其中 $V_0$ 为控制顶点、$T$ 为纹理图、$\tilde{T}$ 为法线图、$S(V_0)$ 为Loop细分极限曲面、$\alpha$ 为先验损失权重。三个损失项的梯度通过可微渲染器反向传播至控制顶点和纹理/法线图，形成端到端的优化闭环。

### 训练/推理路径

CLIP-Mesh 本质上是**测试时优化**方法，无传统意义上的训练阶段。推理路径为：初始化控制网格（通常为球体或模板形状）→ 迭代优化约50分钟（单张NVIDIA P100 16GB GPU）→ 输出带纹理的Loop细分网格。每步迭代中，采样多个相机视角渲染图像，计算复合损失并反向传播更新参数。优化完成后，网格可直接导出为标准资产用于下游渲染引擎。

### 关键创新机理总结

CLIP-Mesh 的核心创新不在于提出新的网络架构，而在于**将Loop细分的隐式几何正则化、扩散先验的语义引导和随机增强的捷径抑制有机组合**，形成一个无需3D监督即可生成高质量带纹理网格的优化系统。三个changed slots——Loop细分控制网格（vs. 普通网格）、分离纹理/法线表示（vs. 简单着色）、复合损失约束（vs. 纯CLIP损失）——协同作用，使优化过程从“在2D投影上绘制纹理”转变为“变形3D形状以匹配语义”，这是其能够在CLIP R-Precision上全面超越Dreamfields的根本原因。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2203_13333/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our optimization pipeline. The differentiable renderer creates views which are encoded and compared to the text encoding as well as the generated image embedding. We optimize for the texture, normal, vertices position*

## 实验与关键发现

### 定量评估：与Dreamfields的全面对比

CLIP-Mesh在153个COCO标题驱动的对象生成任务上与Dreamfields（Jain et al., arXiv 2021）进行了系统定量对比。评估采用CLIP R-Precision指标：对于每个生成形状，在held-out视角（45°仰角）渲染图像，计算其CLIP嵌入与文本嵌入的余弦相似度，并在一批干扰文本中检索正确文本的准确率。生成视角限制在30°仰角以内，与Dreamfields协议保持一致。

**Table 1** 展示了跨不同CLIP骨干网络的一致性优势。当生成与评估均使用ViT-B/16时，CLIP-Mesh达到**96.7**，Dreamfields为**93.5**（+3.2）；使用ViT-B/32时差距进一步拉大至**91.4 vs. 86.6**（+4.8）。在其他跨模型组合（如生成用ViT-B/32、评估用ViT-B/16）中，CLIP-Mesh同样保持领先。这一结果表明CLIP-Mesh的形状-纹理解耦优化策略在多种CLIP视觉编码器下均能产生与文本描述更一致的3D资产。

值得注意的是，CLIP-Mesh的资源消耗显著低于Dreamfields：单个形状仅需**单张NVIDIA P100 16GB GPU约50分钟**，而Dreamfields需**4张A100运行超过24小时**——速度优势约100倍。这一效率差异源于CLIP-Mesh直接优化网格表示而非通过NeRF等隐式场间接生成，但资源不对等可能对定量公平性产生一定影响，文中已注明双方均采用各自推荐配置。

### 消融实验：各组件的因果贡献

**Table 2** 通过逐步叠加组件的方式揭示了每个设计选择的因果效应。基线配置为直接优化普通网格顶点、仅使用CLIP损失、无渲染增强。

**形状正则化的关键作用**：将普通网格替换为Loop细分控制网格后，ViT-B/16评估下的R-Precision从**75.8提升至77.7**，ViT-B/32评估下从**56.1提升至62.7**。Loop细分极限曲面的解析可微性充当了隐式正则化器，防止三角形翻转并维持平滑形状，这一改进在所有评估模型上均一致出现。

**渲染增强的贡献分解**：在Loop细分基础上逐步加入增强策略。添加随机背景（高斯噪声/纯色/棋盘格）将B/16 R-Precision从77.7推至**81.0**；加入物体中心随机偏移带来最大单次提升，B/16指标跃升至**90.1**。这一现象揭示了CLIP模型的一个关键行为特征：当物体始终位于图像中心时，模型倾向于利用背景捷径而非形状信息进行文本匹配。位置偏移迫使优化过程真正变形几何体以匹配语义，而非在固定轮廓内绘制纹理。

**高分辨率渲染的双刃剑效应**：将渲染分辨率提升至512²后缩放至224×224输入CLIP，在多数模型上带来正向增益（B/16评估下从90.1升至**91.5**），但对ViT-L/14评估模型产生负面影响。这表明高分辨率细节对不同CLIP视觉编码器的信息利用模式存在差异，较大模型可能对高频纹理细节更敏感，反而分散了对形状的判别。

**扩散先验的补充监督**：在已包含所有增强的配置上加入扩散先验损失，B/32评估下R-Precision从62.7大幅跃升至**77.7**，B/16评估下从91.5升至**96.7**（即最终完整模型）。扩散先验从文本嵌入采样合理的CLIP图像嵌入作为额外优化目标，有效引导渲染图像嵌入向更合理的区域收敛，尤其对较弱CLIP骨干（B/32）的改善更为显著。

消融路径的整体单调性——从基线75.8到完整模型96.7——强有力地验证了各组件间的协同关系：Loop细分提供几何稳定性，渲染增强阻断背景捷径，扩散先验补充语义引导，三者缺一不可。

### 定性结果与视觉证据

**Fig. 3** 展示了从日常物品（“a coffee”、“a apple”）到复杂形状（“an armchair in the shape of an avocado”）的广泛生成结果，渲染图与底面网格均呈现出与文本描述一致的几何结构和纹理细节。**Fig. 4** 进一步验证了方法在世界著名地标重建上的能力，包括吉萨金字塔、悉尼歌剧院、埃菲尔铁塔、泰姬陵等，生成网格捕捉了各建筑的标志性轮廓。

**Fig. 5** 和**Fig. 6** 展示了多物体同时优化的能力。在“boat and red lighthouse”、“office chair and a desk and a computer monitor”等复合提示下，方法成功生成多个空间关系合理的独立网格。当固定部分物体的初始形状时（如将初始球体约束为“cactus and sand”中的仙人掌），优化过程能在保持固定几何的同时调整纹理和其他物体的形状。

与Dreamfields的视觉对比（**Fig. 7, Fig. 8**）进一步凸显了CLIP-Mesh的优势：在“a sculpture of a rooster”、“Eiffel tower”、“a red chair”等提示下，CLIP-Mesh生成的网格具有更清晰的几何结构和更合理的纹理分布，而Dreamfields的结果常出现形状模糊或纹理混乱。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2203_13333/figures/008_Figure_7.jpg]]
*Figure 7: Comparison with [Jain et al. 2021] results from their paper/project website. Top: results from [Jain et al. 2021]. Bottom: our results. Prompts: a) "matte painting of a bonsai tree; trending on art station" b) "matte painting of a castle made of cheesecake surrounded by a moat made of ice cream; trending on artstation; unreal engine" c) "a cluster of pine trees are in a barren area" d) "a cluster of pine trees are in a barren area" e) "a sculpture of a rooster"*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2203_13333/figures/010_Figure_8.jpg]]
*Figure 8: Comparison with [Jain et al. 2021]. Shapes generated using CLIP ViT/B-16 Top: results from [Jain et al. 2021]. Bottom: our results. Prompts: a) "mount everest" b) "a vase with pink flowers" c) "a hamburger" d) "Eiffel tower" e) "a red chair"*

### 失败模式与适用边界

**拓扑不可变性**：CLIP-Mesh的生成物体的亏格（genus）完全由初始模板网格决定，优化过程无法改变拓扑结构。例如，从球体模板出发无法生成带手柄的杯子（亏格1）。文中仅通过纹理透明通道部分缓解此限制，但本质上无法处理需要拓扑变化的任务。

**CLIP图像先验导致的纹理伪影**：由于CLIP模型基于自然图像训练，其嵌入空间中隐含的图像统计先验会反向投影到3D纹理上。具体表现为：金字塔侧面出现不期望的小人影像（Fig. 4a），珠穆朗玛峰表面浮现“Everest”文字（Fig. 8a）。使用更大的CLIP ViT-B/32模型可部分缓解文字伪影，但无法根除。这一现象揭示了CLIP图像嵌入与3D纹理空间之间的语义错配：模型倾向于在纹理中嵌入2D图像片段以满足CLIP的判别需求，而非生成纯粹的表面材质。

**计算资源与初始化依赖**：尽管相比Dreamfields已大幅提速，单形状50分钟的优化时间仍限制了实时交互应用。此外，最终结果对初始模板网格和相机采样策略存在一定敏感性，文中未系统探讨初始化的影响范围。

**评估指标的局限性**：CLIP R-Precision仅衡量渲染图像与文本的语义对齐程度，无法直接评估3D几何质量（如表面平滑度、拓扑合理性）或多视角一致性。目前缺乏零样本3D生成的标准化几何评估基准，定量结论的泛化性需谨慎解读。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2203_13333/figures/011_Table_2.jpg]]
*Table 2: Ablation study on the R-Precision quantitative metric where higher score is better. We observe that starting from a baseline approach, adding limit subdivision, augmentation, large rendering, and the generative prior systematically improves performance*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2203_13333/figures/004_Figure_4.jpg]]
*Figure 4: Reconstruction of famous landmark around the world: a) "pyramid of giza " b) "Sydney opera house" c) "Eiffel Tower" d) "lighthouse of alexandria" e) "Burj Al Arab" f ) "Taj Mahal"*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2203_13333/figures/005_Figure_5.jpg]]
*Figure 5: Multiple object optimization. Prompts: a) "boat and red lighthouse" b) "office chair and a desk and a computer monitor"*

## 定位与知识库关联

CLIP-Mesh 的核心定位是将**零样本文本驱动的 3D 网格生成**问题转化为一个**可微渲染下的 CLIP 嵌入空间对齐优化问题**。相对于已有方法，它改变的 slot 是**形状表示的先验形式与优化约束的组合方式**：Dreamfields（Jain et al., arXiv 2021）直接优化普通网格顶点，缺乏几何正则化，导致形状混乱；CLIP-Mesh 则引入 Loop 细分曲面作为隐式平滑先验，将优化变量从密集的极限曲面顶点退耦为稀疏的控制顶点 $V_0$，再通过解析可微的细分算子 $V = S(V_0)$ 生成光滑曲面。这一 slot 替换的因果效应是：优化过程中三角形翻转和局部退化被自动抑制，形状收敛到更合理的流形结构。

在优化约束层面，CLIP-Mesh 在 Dreamfields 仅使用 CLIP 相似度损失的基础上，新增了两个关键 slot：**拉普拉斯形状正则化**（指数衰减权重 $\lambda_t$）和**扩散先验损失** $L_{PRIOR}$。拉普拉斯项约束每个顶点与其一邻域平均位置的一致性，防止网格在梯度驱动下塌缩；扩散先验则由文本嵌入采样 CLIP 图像嵌入，为渲染结果提供额外的语义引导，缓解 CLIP 损失自身的局部最优问题。这一组合使优化从“仅匹配文本嵌入”升级为“匹配文本嵌入 + 保持几何平滑 + 对齐生成式图像先验”的多目标体系。

在知识库中，CLIP-Mesh 的挂载点位于**可微渲染 + 视觉-语言模型 + 3D 生成**的交叉节点。其上游依赖包括：Loop 细分曲面理论（Stam, 1998，提供解析可微的极限曲面计算）、可微渲染器（Laine et al., 2020，提供抗锯齿梯度）、CLIP 预训练模型（Radford et al., 2021，提供零样本图文对齐能力）以及扩散先验模型（Ramesh et al., 2022 或类似工作，提供文本到图像嵌入的生成映射）。其下游价值在于：首次证明仅凭 2D 图文模型即可生成可直接导出为标准网格资产（含纹理图与法线图）的 3D 内容，无需任何 3D 监督数据。

适用边界清晰且有限。首先，**拓扑结构不可变**：生成物体的亏格由初始模板网格决定，无法在优化中自动改变拓扑（如从球面变为环面）。文中仅通过纹理透明通道对此进行部分缓解，但并非真正的拓扑变形。其次，**纹理伪影是系统性缺陷**：由于 CLIP 本身在图像数据上训练，其嵌入空间携带了不期望的图像先验，导致纹理中可能投射出与文本无关的图案（如金字塔侧面出现小人影像）或文字（如“珠穆朗玛峰”表面浮现“Everest”字样）。使用更大的 CLIP ViT-B/32 模型可部分缓解文字问题，但无法根治。第三，**计算资源需求虽大幅降低但仍较高**：单形状需约 50 分钟（单张 NVIDIA P100 16GB），虽比 Dreamfields 的 4×A100 24 小时快约 100 倍，但仍难以实现实时或交互式生成。

后续启发方向明确。其一，如何在不改变初始拓扑的前提下实现亏格自适应变化，是提升生成多样性的关键瓶颈。其二，如何引入形状-纹理去偏机制以消除 CLIP 图像先验带来的伪影，可能的方向包括对抗性数据增强、多模态一致性约束或显式的语义分割引导。其三，CLIP-Mesh 的优化框架本身是模型无关的，用更强的图文对齐模型（如 SigLIP、ImageBind）或生成式先验替换 CLIP 和扩散先验，有望直接提升生成质量，这是一个低风险、高收益的跟进路径。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/CLIP_Mesh_Generating_textured_meshes_from_text_using_pretrained_image_text_models.pdf]]