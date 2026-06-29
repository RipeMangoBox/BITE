---
title: Water Simulation and Rendering from a Still Photograph
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Water_Simulation_and_Rendering_from_a_Still_Photograph.pdf
project_link: null
code_link: null
aliases:
- WSRFSP
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_rendering_materials
- topic/graphics_physical_simulation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 用基于优化的杜鹃搜索（cuckoo search）算法取代端到端回归网络，在参数空间中搜索使得渲染结果与输入图像在纹理相似度（DISTS）和颜色分布（HSV颜色直方图）上一致的最优参数，从而解耦了模糊的映射关系。
primary_logic: 将传统参数化水面图形学模型与基于学习的外观估计（如U-Net生成反射纹理）相结合，利用优化算法从单张照片自动恢复全部动态、光照与相机参数，在保持物理合理性的同时实现全自动的可编辑动画生成。
claims:
- 神经网络直接预测参数失败，导致渲染结果缺乏高频波细节且颜色偏移
- 加入HSV颜色直方图相似性后，渲染结果的颜色与输入图像一致性显著提升
- 用户研究中渲染图像的‘真实率’达65.46%，接近真实图像的81.67%，表明方法生成结果具有高度的真实感
- User study on 30 test images 上 Real rate (user-perceived realism) = 65.46%
---

# Water Simulation and Rendering from a Still Photograph

> [!tip] 核心洞察
> 将传统参数化水面图形学模型与基于学习的外观估计（如U-Net生成反射纹理）相结合，利用优化算法从单张照片自动恢复全部动态、光照与相机参数，在保持物理合理性的同时实现全自动的可编辑动画生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从单张静态照片进行水面模拟与渲染 |
| 英文题名 | Water Simulation and Rendering from a Still Photograph |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://rsugimoto.net/WaterAnimationProject/) |
| Topic | #topic/graphics_rendering_materials #topic/graphics_physical_simulation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Water Simulation and Rendering from a Still Photograph |
| Dataset | User study on 30 test images, Runtime on 4K image |

> [!tip] 效果简介
> - User study on 30 test images 上，Real rate (user-perceived realism) 65.46% vs 81.67% (real images) (-16.21%)。
> - Runtime on 4K image (1/3 water) 上，Processing time Seg: 7s + Refl tex: 9s + Param est: 4.5min。

## 概要

从单张静态照片自动生成逼真的动态水面动画，核心难点在于水面参数估计是一个高度欠定问题——不同的参数组合可能产生相似的视觉外观，使得直接的神经网络回归方法失效。本文提出将传统参数化水面图形学模型与基于学习的外观估计相结合：先通过渐进式分块分割框架提取水区域掩码，再利用U-Net生成镜面反射纹理，最后采用杜鹃搜索（cuckoo search）优化算法，在21维参数空间中搜索使渲染结果与输入图像在纹理相似度（DISTS）和颜色分布（HSV颜色直方图）上一致的最优动力学、光照与相机参数。该方法解耦了模糊的映射关系，保持了物理合理性。用户研究表明，渲染图像的真实率达65.46%，接近真实图像的81.67%；处理一张4K图像约需4.5分钟。方法支持合成物体插入和反射感知的颜色迁移等交互式编辑应用，但对碎波、强烈阳光反射等场景仍存在局限。

## 核心方法与创新机理

### 1. 问题背景与唯一瓶颈

从单张静态照片生成可编辑、可动画化的水面，其根本困难在于：水面外观（波浪几何、反射、折射、颜色）由一组高维物理参数共同决定，包括波浪谱参数、风力条件、相机位姿、光照方向等。然而，单张图像仅提供了这些参数在特定瞬间的二维投影，参数到图像的映射是高度**欠定**的——不同的参数组合可能产生视觉上极为相似的渲染结果。这一多对一的映射关系使得**直接的端到端神经网络回归方法失效**，网络预测的参数往往导致渲染结果丢失高频波浪细节，并出现明显的颜色偏移（如整体偏绿，见 Fig. 5）。这是本工作的核心瓶颈。

### 2. 核心洞察与创新机制

本方法的核心洞察在于：**将传统参数化水面图形学模型与基于学习的外观估计解耦，并引入基于优化的搜索算法来桥接“参数空间”与“图像空间”之间的模糊映射**。具体而言，系统并未试图直接从图像回归所有参数，而是构建了一个包含三个关键“changed slots”的管线：

1. **水区域分割**：从手动标注→渐进式分块分割框架（Sec. 2）
2. **反射纹理获取**：从手工拼接环境贴图→基于U-Net的反射纹理生成网络（Sec. 3）
3. **参数估计**：从手工调试/端到端回归→杜鹃搜索（Cuckoo Search）优化算法（Sec. 4）

其中，第三个changed slot是解决瓶颈的**因果旋钮**（causal knob）：杜鹃搜索在21维参数空间中随机采样候选解，调用图形学渲染器生成对应的水面图像，再通过精心设计的能量函数与输入图像进行比对，迭代搜索使渲染结果与输入图像在纹理和颜色分布上一致的最优参数。这一优化范式避开了直接学习模糊映射的困难，转而利用图形学渲染器作为“物理验证器”，在参数空间中寻找视觉上合理的解。

### 3. 系统管线与模块顺序

系统整体流程如 Fig. 2 所示，包含四个串行模块：

![[assets/figures/papers/paper_list_l101_https_rsugimoto_net_WaterAnimationProject/figures/002_Figure_2.jpg]]
*Figure 2: System overview. Given an input image, we "rst segment water, then predict re!ection texture from the water segment, and estimate other parameters. With the re!ection texture and parameters, we generate the water animation using an image-based renderer*

**模块1：渐进式分块水区域分割（Sec. 2）**
- 输入：单张高分辨率RGB图像
- 处理：构建图像金字塔（多级细节层次），从最低分辨率开始，使用预训练的水体分割模型对重叠分块进行预测，将分割概率双线性上采样至下一层级，并迭代更新分块位置以聚焦于水边界区域
- 输出：精细的水区域二值掩码
- 关键设计：分块策略使网络能专注于局部细节，逐步恢复高分辨率下的精确水岸边界（Fig. 3）

![[assets/figures/papers/paper_list_l101_https_rsugimoto_net_WaterAnimationProject/figures/003_Figure_3.jpg]]
*Figure 3: Intermediate results of the progressive patch-based segmentation framework, As the image level and resolution increase, "ne-detailed segmentation edges are progressively detected. Input image: Andrea S/Flickr*

**模块2：反射纹理生成网络（Sec. 3）**
- 输入：原始图像 + 水区域掩码
- 架构：基于U-Net的图像合成网络
- 目标：预测一张“反射纹理”——即假设水面为完全平坦镜面时，水面上每个像素应反射的环境颜色
- 训练数据：使用Places数据集中的水面图像，通过镜像翻转和图像修复技术构造伪真值（ground truth）
- 损失函数（公式1）：

$$L(x,y) = \frac{1}{N} \sum_{i}^{N} (m_i + \lambda (1 - m_i)) |x_i - y_i|$$

其中 $m_i$ 为水区域掩码（水像素为1，非水为0），$\lambda=0.1$ 控制非水体区域对损失的贡献权重。该加权L1损失使网络重点关注水体区域的反射颜色预测精度，同时保持非水体区域的结构一致性。

- 输出：与输入图像同尺寸的反射纹理图（Fig. 4展示了湍流和静水两种场景下的预测结果）

**模块3：参数估计——杜鹃搜索优化（Sec. 4）**
- 搜索空间：21维参数向量，涵盖：
  - 波浪参数（振幅、波长、方向等，基于Tessendorf 2001谱域模型）
  - 风参数（风速、风向）
  - 相机参数（视点位置、焦距等）
  - 光照参数（光源方向、环境光强度等）
- 优化算法：杜鹃搜索元启发式算法（cuckoo search metaheuristic）
  - 初始化：随机生成一组“蛋”（候选参数向量）
  - 迭代：通过Lévy飞行生成新解，替换能量较高的劣解
  - 终止条件：使用平滑能量 $E'(k)$ 判断收敛

- 能量函数（公式2-4）：

$$E_{total} = E_T + \lambda E_C$$

其中：
- **纹理相似度能量** $E_T = d(x, y)$：使用DISTS（Deep Image Structure and Texture Similarity）指数衡量输入图像 $x$ 与当前参数渲染图像 $y$ 之间的感知纹理差异。DISTS对纹理结构变化敏感，能有效捕捉高频波浪细节的匹配程度。
- **颜色分布能量** $E_C = H(x, y)$：基于HSV颜色空间的Hellinger距离：

$$H(x, y) = \sqrt{1 - \frac{1}{\sqrt{\sum_{i=1}^n x_i \sum_{i=1}^n y_i}} \sum_{i=1}^n \sqrt{x_i y_i}}$$

该度量比较两幅图像在HSV各通道的颜色直方图分布，对整体色调偏移（如偏绿）具有强约束力。

- 平滑终止能量（公式5）：

$$E'(k) = \sum_{i=k-s+1}^{k} \{i - (k-s)\} E(i)$$

其中 $s$ 为平滑窗口大小，对最近 $s$ 次迭代的能量进行加权平均，当 $E'(k)$ 趋于稳定时终止搜索。

- 输出：最优的21维参数向量

**模块4：基于图像的实时渲染器（Sec. 5）**
- 水面几何生成：使用Tessendorf 2001谱域方法，根据波浪和风参数生成水面位移图
- LOD策略：采用Johanson和Lejdfors 2004的投影网格LOD方法，在屏幕空间生成自适应分辨率的网格
- 反射计算（Fig. 7）：采用屏幕空间光线步进（ray-marching）结合3D空间校验
  - 将场景物体映射到水面平面，确定反射源点的3D位置
  - 在图像空间沿反射方向进行光线步进
  - 通过垂直曲面墙代理几何体处理遮挡
  - 从反射纹理中采样颜色嵌入水面
- 折射简化：假设深水区域使用单一颜色，未详细建模水下折射
- 输出：可实时渲染的水面动画，支持交互式编辑（如放置合成物体、颜色迁移，见Fig. 9）

![[assets/figures/papers/paper_list_l101_https_rsugimoto_net_WaterAnimationProject/figures/007_Figure_7.jpg]]
*Figure 7: The image-based re!ection method. The objects are mapped onto the water plane to determine the re!ection source point in 3D. We perform ray-marching in image space with additional checks in 3D space to consider the height of wall proxy objects. Then, we fetch the re!ection color embedded in the water surface from the re!ection texture*

### 4. 模块间因果关系

模块之间存在严格的**前馈依赖与反馈验证**关系：

1. **分割→反射纹理生成**：水区域掩码为U-Net提供了精确的感兴趣区域，使网络能专注于水体反射的预测，同时掩码也直接参与损失函数的加权计算，确保预测质量。

2. **反射纹理→参数优化**：反射纹理作为渲染器的输入资源之一，直接影响渲染结果的视觉质量。参数优化过程中，杜鹃搜索的每次迭代都会调用渲染器，使用当前参数和预测的反射纹理生成水面图像，再计算能量函数。

3. **参数优化→渲染器**：优化得到的21维参数直接驱动水面几何（波浪形状）和光照计算，与反射纹理共同决定最终动画的视觉外观。

4. **能量函数作为闭环反馈**：能量函数 $E_{total}$ 是连接“渲染结果”与“输入图像”的唯一桥梁。其设计直接决定了优化的收敛方向：$E_T$（DISTS）确保纹理结构（波浪细节）的匹配，$E_C$（HSV直方图）确保全局颜色的保真度。消融实验（Fig. 6）证实，移除 $E_C$ 会导致渲染颜色与输入图像出现显著偏差，验证了颜色度量在能量函数中的不可替代性。

### 5. 训练与推理路径

- **U-Net训练**：离线完成，使用Places数据集中的水面图像及自动构造的伪真值进行监督学习，损失函数为加权L1。
- **推理阶段**：
  1. 分割模块：约7秒（4K图像，水面占1/3）
  2. 反射纹理生成：约9秒
  3. 杜鹃搜索参数估计：约4.5分钟（主要计算瓶颈，每次迭代需调用渲染器）
  4. 实时渲染：参数确定后，渲染器可实时运行动画

整个推理过程**无需任何手动标注或参数调试**，实现了从单张照片到可编辑水面动画的全自动流程。

![[assets/figures/papers/paper_list_l101_https_rsugimoto_net_WaterAnimationProject/figures/010_Figure_9.jpg]]
*Figure 9: Applications. In (a), our method allows to place synthetic objects on the water surface and generates realistic re-!ections. In (b), given an input image, we transfer its color to simulate di$erent environments and predict corresponding re!ection textures. By interpolating between the predicted parameters, the edited results vary smoothly. Input Images: (a) Krzysztof Golik/Wikimedia (b) Confaulk/Wikimedia (top) and Rixie/Adobe Stock (bottom)*

## 实验与关键发现

### 用户感知真实感研究

为评估系统整体输出质量，作者对30张测试图像进行了用户研究。参与者被要求判断图像是否为真实照片。结果显示，真实图像的平均“真实率”为**81.67%**，而本方法生成的渲染图像真实率达到**65.46%**，仅相差约16个百分点。这一结果表明，尽管渲染图像与真实照片之间仍存在可辨识的差距，但系统已能生成具有高度真实感的水面动画效果，在单张图像输入这一高度欠定的约束条件下表现出较强的视觉欺骗能力。

需要指出的是，该用户研究未与同期基于单张图像的水面动画方法（如Holynski et al. 2021）进行定量比较，且测试集仅包含67张图像，规模较小。因此上述“65.46%”的绝对值应理解为方法可行性的初步验证，而非严格基准测试下的性能指标。

### 运行效率分析

系统各模块的运行时间在4K分辨率、水面约占图像三分之一面积的典型场景下进行了测量：
- **水区域分割**：约7秒
- **反射纹理生成**：约9秒
- **参数估计（杜鹃搜索优化）**：约4.5分钟

整体处理时间约为5分钟，主要瓶颈在于参数估计阶段的迭代渲染与能量评估。由于杜鹃搜索需要在21维参数空间中反复生成候选解并调用渲染器计算能量函数，该阶段的耗时与图像分辨率及水面面积呈正相关。论文未提供针对不同分辨率或水面占比的消融时间数据，此处的运行时间仅反映典型使用场景。

### 关键消融实验

**消融一：神经网络直接预测参数 vs. 杜鹃搜索优化**

论文通过一项决定性消融实验验证了优化策略的必要性。作者训练了一个神经网络直接回归水面参数（包括波高、风速、相机姿态等21维向量），并与基于杜鹃搜索的优化方法进行定性比较（Figure 5）。结果表明，神经网络直接预测的参数导致渲染结果**缺乏输入图像中的高频波浪细节**，且**整体颜色向绿色偏移**。这一现象的根本原因在于：单张图像到水面参数的映射高度欠定——多组不同的参数组合可能产生视觉上相似的静止水面外观，端到端回归网络难以从模糊的监督信号中学习到正确的参数解。

![[assets/figures/papers/paper_list_l101_https_rsugimoto_net_WaterAnimationProject/figures/005_Figure_5.jpg]]
*Figure 5: Comparison between our method and a neural network approach. The result of the neural network method in this example lacks the high frequency waves present in the input image. Furthermore, the overall color is shifted towards green*

相比之下，杜鹃搜索通过在参数空间中显式搜索使渲染结果与输入图像在纹理和颜色分布上一致的最优参数，有效绕开了这一欠定映射问题。该消融实验直接支撑了论文的核心设计选择：以优化替代回归。

**消融二：HSV颜色直方图相似性度量的作用**

能量函数由两部分组成：DISTS纹理相似度 $E_T$ 和HSV颜色直方图差异 $E_C$，总能量为 $E_T + \lambda E_C$。为验证颜色度量的必要性，论文比较了仅使用DISTS度量和加入HSV颜色度量后的渲染结果（Figure 6）。实验表明，**加入颜色相似性度量后，渲染图像的颜色与输入图像的一致性显著提升**；仅使用DISTS时，尽管纹理结构相似，但颜色分布可能出现明显偏差。

![[assets/figures/papers/paper_list_l101_https_rsugimoto_net_WaterAnimationProject/figures/006_Figure_6.jpg]]
*Figure 6: Comparison between our method with and without the color similarity metric*

这一结果揭示了纹理相似度度量在颜色感知上的局限性——DISTS主要捕获结构差异，对全局颜色偏移不够敏感。引入基于Hellinger距离的HSV直方图比较作为补充，使优化过程同时关注局部纹理保真度和全局色彩一致性。

### 失败模式与适用边界

论文明确列出了方法的若干局限性（Figure 10）：

1. **动态水体失效**：方法假设水面为开阔海域的统计波模型，无法模拟**碎波（breaking waves）**和流动水体（如瀑布）。Figure 10a展示了碎波场景下的失败案例，渲染结果无法再现波浪破碎时的泡沫和飞溅效果。

2. **强烈太阳光反射**：反射纹理预测网络使用标准24-bit RGB图像作为输入和输出，无法存储高动态范围的辐射强度。当输入图像包含强烈的太阳光镜面反射时（Figure 10b），预测的反射纹理将丢失高光细节，导致渲染结果中该区域过曝或失真。

3. **折射建模简化**：系统未对水下折射进行详细建模，而是假设深水区域使用单一颜色填充。对于清澈浅水场景，这一简化可能导致视觉真实感下降。

4. **参数均匀性假设**：整个水体区域共享同一组波、风参数，不适用于近岸区域（波浪行为受海底地形影响而显著变化）或包含多个不同水体的场景。论文指出多水体支持可通过简单扩展实现，但当前版本未提供此功能。

5. **优化收敛性的理论空白**：杜鹃搜索算法的理论收敛性分析仍是开放问题，论文仅引用了简化版本算法的部分收敛结果（He et al. 2018），并未对当前应用场景下的收敛性提供严格保证。

## 定位与知识库关联

本工作的核心定位是**将单张静态照片中水面动画的参数估计问题从“端到端回归”转变为“基于物理模型的优化搜索”**，从而绕过了单图到多参数的欠定映射困境。相对已有方法，它改变的 slot 是**水面动力学/光照参数估计模块**：传统图形学流程依赖手工调试或物理测量，而直接的神经网络回归方法（如论文中作为消融基线的 direct regression baseline）则因单张图像中不同参数组合可产生相似视觉外观而失效（Fig. 5）。本工作用杜鹃搜索（cuckoo search）在 21 维参数空间中优化一个结合 DISTS 纹理相似度与 HSV 颜色直方图差异的能量函数，将模糊的映射关系解耦为“渲染-比较-搜索”的闭环。

在知识库中，本工作可挂载于以下节点：

1. **单图到物理场景参数估计（image-to-physics inverse rendering）**  
   与从单张图像恢复 BRDF、光照、几何等物理参数的逆渲染方法同属一类问题。本工作的独特贡献在于处理的是**动态时变参数**（波浪、风场）而非静态材质，且引入元启发式优化算法替代梯度下降或回归网络，为欠定逆问题提供了一种不依赖大规模标注数据的求解路径。

2. **基于图形学先验的神经渲染（graphics-prior-guided neural rendering）**  
   本工作将传统水面图形学模型（Tessendorf 2001 的频谱域波浪模型）作为正向渲染器，将学习型方法（U-Net）用于反射纹理生成，将优化算法用于参数搜索，形成“学习+图形学+优化”的混合架构。这与 **Holynski et al. (2021)** 等同期单图水面动画方法形成对比：后者可能采用不同的参数化或估计策略，但本工作未与之进行定量比较，该对比关系需手动验证。

3. **基于感知度量的图像合成优化（perceptual-metric-driven synthesis）**  
   能量函数中 DISTS（Ding et al. 2020）与 HSV 颜色直方图的组合使用，证明了下游视觉任务中“纹理结构相似性+颜色分布一致性”双重度量的有效性。这一设计可迁移至其他需要同时保持局部纹理和全局色调的图像合成任务。

**适用边界**方面，本方法存在若干硬约束：假设整个水体具有同一组参数，不适用于近岸浅水区域；无法处理流动水体（瀑布）和碎波（Fig. 10a）；光照模型不支持强太阳光反射（Fig. 10b），因为反射纹理预测网络使用标准 24-bit RGB 图像，无法存储高辐射强度值；当前实现仅支持单一水体（虽声称可简单扩展）。这些边界条件为后续工作提供了明确的改进方向。

**后续启发**包括：(1) 将杜鹃搜索替换为更具理论收敛性保证的贝叶斯优化或可微渲染方法，提升参数估计的效率和可靠性；(2) 引入空间变化的参数场以处理近岸和非均匀水面；(3) 扩展反射纹理的 HDR 表示以支持强光场景；(4) 建立标准 benchmark 以定量比较不同单图水面动画方法，目前该领域缺乏统一评测基准。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Water_Simulation_and_Rendering_from_a_Still_Photograph.pdf]]