---
title: "3Doodle: Compact Abstraction of Objects With 3D Strokes"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/3Doodle_Compact_Abstraction_of_Objects_With_3D_Strokes.pdf
project_link: "https://blendswap.com/blend/25086"
code_link: "https://github.com/changwoonchoi/3Doodle"
aliases:
- 3CAO3S
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将草图表示为可微的3D笔划参数（贝塞尔曲线+超二次曲面），通过感知损失直接优化，绕过了训练数据和显式3D重建。
primary_logic: 将草图分解为视图无关的3D特征线（贝塞尔曲线）和视图相关的光滑轮廓（超二次曲面轮廓），并设计完全可微的渲染管线，使得仅用少量参数即可通过优化生成紧凑且视图一致的抽象草图。
claims:
- 3Doodle在所有感知指标上均优于稀疏表示方法NEF和CLIPasso（综合评估）。
- "3Doodle在CLIPtxt指标（与文本“A sketch of a(n) {object name}”的相似度）上超过所有基线，表明生成结果最被识别为“草图”。"
- 感知研究中，3Doodle在“草图感”和“有效性”评分上显著高于密集表示方法（ARF和Suggestive Contours），并在“表达力”上与其可比。
- 多视图合成数据集 (Blender, InvRender, 自建) 上 LPIPS(↓) = 0.217
---

# 3Doodle: Compact Abstraction of Objects With 3D Strokes

> [!tip] 核心洞察
> 将草图分解为视图无关的3D特征线（贝塞尔曲线）和视图相关的光滑轮廓（超二次曲面轮廓），并设计完全可微的渲染管线，使得仅用少量参数即可通过优化生成紧凑且视图一致的抽象草图。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3Doodle: 用3D笔画紧凑抽象物体 |
| 英文题名 | 3Doodle: Compact Abstraction of Objects With 3D Strokes |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2402.03690) · [Code](https://github.com/changwoonchoi/3Doodle) · [Project](https://blendswap.com/blend/25086) · [arXiv](https://arxiv.org/abs/2402.03690") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3Doodle |
| Dataset |  |

> [!tip] 效果简介
> - 多视图合成数据集 (Blender, InvRender, 自建) 上，LPIPS(↓) 0.217 vs 0.255 (CLIPasso) (-0.038)。
> - 多视图合成数据集 上，CLIPtxt(↑) 0.665 vs 0.651 (ARF), 0.659 (CLIPasso) (+0.014 / +0.006)；模型大小 (稀疏性) <1.5kB vs ~6MB (NEF), <70MB (CLIPasso), <3.8GB (ARF) (数量级更小)。
> - 感知用户调研 (72人) 上，Human realistic sketch rating (1-5) 显著高于ARF和Suggestive Contours vs ARF, Suggestive Contours (定性优势)。

## 概要

从多视图图像中直接生成紧凑、视图一致且语义丰富的三维草图，是计算机图形学中的一个开放难题。现有方法或局限于二维画布导致视图不一致，或依赖预训练的三维模型（网格/NeRF）而无法产生稀疏的笔划抽象。**3Doodle** 提出了一种新的三维草图表示与优化框架：将草图分解为**视图无关的三维贝塞尔曲线**（表达特征线）和**视图相关的超二次曲面轮廓**（表达光滑表面边界），并设计完全可微的渲染管线，使得仅通过最小化感知损失（LPIPS+CLIP）即可从多视图图像直接优化少量几何基元参数，无需任何训练数据或显式三维重建。

实验表明，3Doodle 生成的草图在所有感知指标上均优于稀疏表示基线（CLIPasso、NEF），在“草图感”文本相似度（CLIPtxt: 0.665）上超越所有方法，模型大小仅不足 1.5 kB——比 NEF（~6 MB）和 CLIPasso（<70 MB）小三个数量级以上。用户调研中，3Doodle 在“草图感”和“有效性”评分上显著高于密集表示方法（ARF、Suggestive Contours），同时保持可比的表达力。该方法将三维草图生成定位为**基于感知优化的紧凑几何抽象**，为可编辑、可风格化的三维矢量草图提供了新路径。

## 核心方法与创新机理

### 问题瓶颈与核心思路

现有草图生成方法面临一个根本性困境：基于2D画布的优化方法（如CLIPasso）只能在单视图上生成笔划，无法保证多视图一致性；而具备3D表示的方法要么依赖精确的预重建网格（如Suggestive Contours）或预训练NeRF（如ARF），要么需要成对训练数据（如Kampelmühler & Pinz），无法直接从多视图图像中产生紧凑、视图一致且语义丰富的3D草图笔划。

3Doodle的核心洞察在于：**将草图分解为视图无关的3D特征线和视图相关的光滑轮廓，并设计完全可微的渲染管线，使得仅用少量参数即可通过感知损失直接优化生成紧凑的抽象草图**。这一策略绕过了对训练数据和显式3D重建的依赖，将问题转化为一个可微渲染框架下的参数优化问题。

### 三个关键changed slots

相比现有方法，3Doodle在三个维度上做出了根本性改变：

**1. 输入数据要求**：从“单张图像（CLIPasso）或预训练NeRF/网格（NEF、ARF、Suggestive Contours）”转变为“多视图图像及其相机位姿，无需预重建3D模型”。这消除了对昂贵3D重建预处理步骤的依赖，使方法可直接应用于摄影测量或SfM输出。

**2. 草图表示空间**：从“2D画布上的笔划（CLIPasso）、3D边场（NEF）或无几何的密集像素（ARF、Suggestive Contours）”转变为“3D贝塞尔曲线（视图无关）+ 超二次曲面轮廓（视图相关）的混合表示”。这种分解使表示能够分别处理物体的结构性边线（如棱角、纹理边界）和光滑曲面的轮廓线，覆盖了更广泛的几何特征类型。

**3. 优化范式**：从“需要成对训练数据或风格参考图像”转变为“完全可微的渲染管线，直接最小化LPIPS+CLIP感知损失，无需训练”。这使方法成为一个test-time optimization框架，对任意输入物体具有泛化能力。

### 方法框架与模块顺序

3Doodle的完整流程包含三个顺序耦合的模块（Fig. 2）：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_03690/figures/002_Figure_2.jpg]]
*Figure 2: Overview of 3Doodle. We generate a compact 3D geometric representation from multi-view images of objects. We separately define view-independent stroke*

**模块一：3D笔划参数化** — 定义草图的几何基元，将3D草图表示为两类组件的并集：

$$S^{\mathrm{3D}} = S_{\mathrm{ind}}^{\mathrm{3D}} \cup S_{\mathrm{dep}}^{\mathrm{3D}}$$

其中视图无关组件 $S_{\mathrm{ind}}^{\mathrm{3D}}$ 由 $N_{\mathrm{ind}}$ 条3D三次贝塞尔曲线构成：

$$S_{\mathrm{ind}}^{\mathrm{3D}} = \left\{ B^{\mathrm{3D}}(\boldsymbol{p}_i) \right\}_{i=1}^{N_{\mathrm{ind}}}$$

每条贝塞尔曲线 $B^{\mathrm{3D}}(t; \boldsymbol{p}_i) = \sum_{j=0}^{3} b_j(t) p_i^j$ 由4个3D控制点参数化，在优化过程中可自由更新位置。这些曲线用于捕捉物体上视图不变的结构性边线，如棱角分明的几何特征。

视图相关组件 $S_{\mathrm{dep}}^{\mathrm{3D}}$ 由 $N_{\mathrm{dep}}$ 个超二次曲面的并集构成。每个超二次曲面通过隐式函数定义：

$$f(\mathbf{x}; \alpha_i, \epsilon_i) = \left( \left( \frac{x}{\alpha_{i,1}} \right)^{\frac{2}{\epsilon_{i,2}}} + \left( \frac{y}{\alpha_{i,2}} \right)^{\frac{2}{\epsilon_{i,2}}} \right)^{\frac{\epsilon_{i,2}}{\epsilon_{i,1}}} + \left( \frac{z}{\alpha_{i,3}} \right)^{\frac{2}{\epsilon_{i,1}}}$$

经过刚性变换 $\mathbf{R}_i, \mathbf{t}_i$ 后，单个超二次曲面的隐式表面为 $S(\mathbf{x}; \theta_i) = f(\mathbf{R}_i^{-1}(\mathbf{x} - \mathbf{t}_i); \alpha_i, \epsilon_i)$，多个超二次曲面的并集取各隐式函数的最小值：

$$S(\mathbf{x}; \theta) = \bigcup_{i=1}^{N_{\mathrm{dep}}} S(\mathbf{x}; \theta_i) = \min_i S(\mathbf{x}; \theta_i)$$

参数 $\alpha_i$ 控制三轴尺度，$\epsilon_i$ 控制形状从立方体到球体的连续变化，使超二次曲面能灵活拟合各类光滑体块。

**模块二：可微笔划渲染** — 将两类3D基元分别渲染为2D草图线，实现端到端的梯度回传。

对于视图无关的贝塞尔曲线，3Doodle利用**正交投影定理**：3D贝塞尔曲线的正交投影等价于其控制点投影后定义的2D贝塞尔曲线。这使3D曲线可直接投影为2D矢量笔划，通过可微光栅化器渲染为像素草图，梯度可流畅回传至3D控制点。

对于视图相关的超二次曲面轮廓，3Doodle提出**轮廓体积密度**机制（Fig. 3）。首先将隐式表面转化为表面体积密度 $\sigma_{\mathrm{surf}}$，然后通过法向与视线夹角衰减该密度：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_03690/figures/003_Figure_3.jpg]]
*Figure 3: (a) We visualize the volume density*

$$\sigma_{\mathrm{contour}}(\mathbf{x}, \mathbf{d}) = (1 - (\mathbf{n}(\mathbf{x}) \cdot \mathbf{d})^{\beta}) \sigma_{\mathrm{surf}}$$

当表面法向与视线方向接近平行时（即位于轮廓线附近），密度显著增强；当法向正对视线时密度衰减。通过体积渲染对该密度场积分，即可获得仅包含轮廓线的2D图像。参数 $\beta$ 控制轮廓的锐利程度。这一设计使超二次曲面的轮廓渲染完全可微，梯度可通过体积渲染积分和隐式表面求导回传至曲面参数。

两类渲染结果叠加形成最终草图图像 $\mathcal{R}(S^{\mathrm{3D}})$。

**模块三：感知损失优化** — 直接优化基元参数以匹配目标多视图图像。

给定目标图像集 $\mathcal{Z}$ 和对应相机位姿，损失函数结合结构感知和语义感知：

$$\mathcal{L} = \sum_{I \in \mathcal{Z}} \lambda \rho(\mathrm{LPIPS}(I, \mathcal{R}(S^{\mathrm{3D}})), \alpha, c) + \mathrm{dist}(\mathrm{CLIP}(I), \mathrm{CLIP}(\mathcal{R}(S^{\mathrm{3D}})))$$

其中LPIPS捕捉图像的结构布局相似性，CLIP余弦距离维护高层语义一致性（使草图保持可识别性），$\rho$ 为鲁棒损失函数（Charbonnier形式）以处理多视图间的异常值。优化直接对所有贝塞尔曲线控制点、超二次曲面参数（尺度、形状、位姿）进行梯度下降。

### 模块间的因果链路

三个模块形成紧密的因果依赖链：**参数化模块**定义了可优化的几何空间，其分解设计（曲线+曲面）决定了后续渲染模块需要处理的几何类型；**渲染模块**将几何参数映射为图像空间的草图，其可微性是优化模块能够工作的前提；**优化模块**通过感知损失将多视图图像信号反向传播至几何参数，驱动两类基元分别收敛到物体的结构线和轮廓线。

关键因果机制在于：贝塞尔曲线通过正交投影定理保证了视图间几何一致性（同一曲线在不同视角下投影为对应的2D曲线），而超二次曲面通过轮廓体积密度实现了视图相关的自适应轮廓提取（曲面在不同视角下自动产生对应的轮廓线）。两者通过共享的感知损失联合优化，使视图无关和视图相关组件在梯度驱动下自然分工——曲线趋向于拟合跨视图稳定的边线，曲面趋向于拟合光滑体块的轮廓。

### 初始化策略

3Doodle采用SfM点云初始化（远端点采样），而非随机初始化或基于线条的SfM初始化。具体做法是对SfM稀疏点云计算凸包并采样远端点作为贝塞尔曲线控制点初值，超二次曲面则初始化为覆盖点云的椭球。这一策略对含光滑表面的物体尤为关键，能引导优化更稳健地收敛到合理草图（Fig. 10, Fig. 15），避免了随机初始化导致的退化问题。

## 实验与关键发现

### 主要量化结果

3Doodle 在自建多视图合成数据集（含 Blender、InvRender 及自采集物体）上与四类基线方法进行了全面对比，涵盖稀疏表示方法（**CLIPasso**，Vinker et al., ACM TOG 2022；**NEF**，Ye et al., CVPR 2023）和密集表示方法（**ARF**，Zhang et al., ECCV 2022；**Suggestive Contours**，DeCarlo et al., 2003）。所有方法使用相同的多视图输入和相机位姿。

**Table 1** 报告了五项核心指标。在结构感知指标 LPIPS 上，3Doodle 取得 0.217，显著优于稀疏基线 CLIPasso（0.255，Δ = -0.038）和 NEF（0.324，Δ = -0.107），表明其草图与目标视图的结构一致性更强。在语义层面，3Doodle 的 CLIPtxt 指标（测量渲染草图与文本 “A sketch of a(n) {object name}” 的 CLIP 余弦相似度）达到 0.665，超过所有基线（ARF 0.651，CLIPasso 0.659），证明其生成结果最容易被识别为“草图”。CLIPimg 指标（0.895）与 CLIPasso（0.897）和 Suggestive Contours（0.887）可比，DINO 指标（0.784）略低于 CLIPasso（0.828），但整体处于有竞争力的水平。

**紧凑性优势**是 3Doodle 的突出特点。其模型大小仅 <1.5 kB，相比 NEF（~6 MB）、CLIPasso（<70 MB）和 ARF（<3.8 GB）呈数量级压缩。这源于其直接优化稀疏几何基元参数（贝塞尔曲线控制点 + 超二次曲面参数）的范式，无需存储密集特征场或网格。

### 感知用户调研

为弥补深度特征指标与人类感知之间的差距，作者开展了 72 人参与的用户调研（**Fig. 4**），从四个维度评估：草图感（sketch-likeness）、有效性（effectiveness）、表达力（expressiveness）和视图一致性（view consistency）。结果显示，3Doodle 在“草图感”和“有效性”评分上显著高于密集表示方法 ARF 和 Suggestive Contours，在“表达力”上与其可比。这表明 3Doodle 的稀疏笔划表示虽然信息量远小于密集方法，但能有效捕获物体的核心语义结构，产生更接近人类手绘草图的感知效果。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_03690/figures/005_Figure_4.jpg]]
*Figure 4: Bar plots of the perceptual study results*

### 关键消融实验

**（1）草图组件的必要性（Fig. 8）**

仅使用视图无关的 3D 贝塞尔曲线（$S_{\mathrm{ind}}^{\mathrm{3D}}$）优化时，对于具有锐利边缘的物体（如椅子、汽车）可生成合理结果，但对于光滑表面的物体（如泰迪熊、雪人）则完全失效——贝塞尔曲线无法自然地表达光滑曲面的轮廓变化。加入视图相关的超二次曲面轮廓（$S_{\mathrm{dep}}^{\mathrm{3D}}$）后，系统能够自动在需要的位置生成闭合轮廓线，补全光滑物体的边界信息。这验证了混合表示设计的因果必要性：两类基元分别对应物体表面的特征线与轮廓线，缺一不可。

**（2）损失函数的作用（Fig. 9, Table 2）**

移除 CLIP 语义损失后，草图虽保留了大致的空间布局（LPIPS 仍有监督），但丢失了关键的语义部件。以椅子为例，仅用 LPIPS 优化的结果中，椅背的笔划退化消失，导致物体识别度显著下降。Table 2 的量化消融显示，在椅子场景上，完整损失（LPIPS + CLIP）的 LPIPS 为 0.217，移除 CLIP 后升至 0.234，DINO 从 0.784 降至 0.751。这证实 CLIP 损失在高层语义引导中起决定性作用，而 LPIPS 负责维护底层结构对齐。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_03690/figures/010_Table_2.jpg]]
*Table 2: Quantitative results on ablated loss terms*

**（3）初始化策略的影响（Fig. 10, Fig. 15）**

对比三种初始化方式：随机初始化、基于线条的 SfM 点云初始化、以及基于远端点采样的 SfM 点云初始化。结果显示，远端点采样策略能更稳健地引导优化收敛到合理草图，尤其对光滑表面物体效果显著。随机初始化容易陷入局部最优，产生杂乱无章的笔划；基于线条的 SfM 初始化对边缘丰富的物体有效，但对光滑物体提供的引导不足。这一消融揭示了稀疏基元优化的初始化敏感性，以及利用多视图几何线索提供先验的重要性。

### 失败模式与适用边界

**（1）深度排序与遮挡缺失**

当前可微渲染管线将完整的 3D 线框无遮挡地投影到 2D，忽略了几何基元之间的前后遮挡关系。这意味着草图无法表现自遮挡轮廓，对于具有复杂嵌套结构的物体，渲染结果会出现“透视”效应，降低真实感。这是方法的一个结构性限制，源于其选择了简洁性而非物理正确的渲染。

**（2）优化效率瓶颈**

参数优化过程相当耗时，最长可达 6 小时。这限制了其在实时或交互式场景中的应用。瓶颈主要来自每轮迭代需对多视图进行完整渲染和感知损失计算。

**（3）笔划数量需手动指定**

贝塞尔曲线数量 $N_{\mathrm{ind}}$ 和超二次曲面数量 $N_{\mathrm{dep}}$ 需用户预设，系统无法自动在紧凑性与表现力之间取得平衡。设置过少会丢失细节，过多则引入冗余笔划并增加优化难度。

**（4）复杂纹理物体的局限性**

对于含有大量细节或纹理噪声的物体，稀疏 3D 笔划可能无法完整表达所有视觉特征。方法的优势在于抽象和简化，而非忠实复现，因此对需要精确纹理再现的任务不适用。

### 补充能力验证

**Fig. 6** 展示了 3Doodle 对稀疏输入的鲁棒性：仅需 15 张输入视图即可生成合理的草图，这对实际采集条件受限的场景具有实用价值。**Fig. 7** 证明了 3D 笔划作为矢量表示的可编辑性——通过将优化后的贝塞尔曲线和超二次曲面轮廓导出为矢量格式，可在 Adobe Illustrator 中应用不同笔刷风格，实现草图风格化，这为下游艺术创作提供了灵活接口。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_03690/figures/004_Table_1.jpg]]
*Table 1: Sketch recognition accuracy. We mark the best and second-best results in bold and underlined numbers*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_03690/figures/007_Figure_6.jpg]]
*Figure 6: 3Doodle robustly generates sketch for a few multi-view inputs*

## 定位与知识库关联

3Doodle 在“从多视图图像生成紧凑且视图一致的3D草图”这一问题上，相对于已有工作改变了三个核心 slot，从而在知识库中占据了一个独特位置。

**改变的 slot 一：输入数据要求——绕过显式3D重建。** 传统3D草图或特征线提取方法几乎都依赖预重建的3D模型：**Suggestive Contours**（DeCarlo et al., 2003）需要精确的3D网格来计算几何特征线；**ARF**（Zhang et al., ECCV 2022）需要预训练的NeRF作为风格化载体；**NEF**（Ye et al., CVPR 2023）虽能提取3D参数曲线，但同样需要多视图重建的边场作为输入。2D草图方法如 **CLIPasso**（Vinker et al., ACM TOG 2022）只需单张图像，却无法保证视图一致性。3Doodle 的输入 slot 改为“多视图图像+相机位姿”，直接从图像优化3D笔划参数，绕过了网格重建或NeRF训练这一中间环节。这一改变使得方法可以应用于那些难以获得完整3D模型但仍有多视图拍摄的场景，降低了数据获取门槛。

**改变的 slot 二：草图表示空间——混合视图无关与视图相关组件。** 这是方法最本质的创新。已有工作要么仅表示视图无关的几何特征线（如NEF的3D边场），要么在2D画布上操作（如CLIPasso），要么不做几何抽象而直接风格化密集像素（如ARF）。3Doodle 将3D草图显式分解为 $S^{\mathrm{3D}} = S_{\mathrm{ind}}^{\mathrm{3D}} \cup S_{\mathrm{dep}}^{\mathrm{3D}}$：用3D三次贝塞尔曲线表示视图无关的结构线，用超二次曲面的轮廓表示视图相关的光滑表面边界。这一混合表示使得仅用极少量参数（<1.5kB）即可同时捕捉物体的棱边结构和曲面轮廓——纯贝塞尔曲线无法表达光滑表面（如泰迪熊、雪人，见Fig. 8消融），纯超二次曲面则丢失了棱角分明的结构线。知识库中此前缺乏这样一种“将2D草图的笔划概念直接提升到3D并区分视图依赖性的紧凑参数化”。

**改变的 slot 三：优化范式——完全可微的感知损失驱动，无需训练数据。** 传统草图生成要么需要成对训练数据（如Kampelmühler & Pinz的监督方法），要么依赖风格参考图像（如ARF），要么是重建后处理（如Suggestive Contours）。3Doodle 构建了完全可微的渲染管线：利用正交投影定理将3D贝塞尔曲线精确映射为2D贝塞尔曲线，通过轮廓体积密度 $\sigma_{\mathrm{contour}}(\mathbf{x}, \mathbf{d}) = (1 - (\mathbf{n}(\mathbf{x}) \cdot \mathbf{d})^{\beta}) \sigma_{\mathrm{surf}}$ 实现超二次曲面轮廓的可微体积渲染。在此之上，直接最小化LPIPS（结构布局）+ CLIP（高层语义）的感知损失，无需任何成对草图数据。这一范式使方法对未见过的物体类别具有较好的泛化能力。

**知识库挂载点。** 3Doodle 的核心贡献可挂载到三个知识库节点：(1) **可微渲染与逆图形学**——证明了将稀疏几何基元（贝塞尔曲线+超二次曲面）与感知损失结合，可以在无监督条件下恢复有语义意义的3D抽象表示；(2) **非真实感渲染（NPR）与草图生成**——提供了一个从多视图直接生成3D笔划的端到端方案，区别于传统的“先重建再描线”或“2D画布优化”路线；(3) **紧凑3D表示**——以<1.5kB的存储量实现了可编辑、可风格化的矢量3D草图，在紧凑性上远超NEF（~6MB）、CLIPasso（<70MB）和ARF（<3.8GB），为3D资产的轻量化表达提供了新思路。

**适用边界与限制。** (1) 参数优化相当耗时（最长可达6小时），难以满足实时或交互式应用需求；(2) 当前渲染管线忽略了几何基元之间的深度排序与遮挡，将完整线框无遮挡地渲染，无法表示自遮挡轮廓——这限制了草图在复杂几何下的真实感；(3) 笔划数量需要用户手动指定，不能自动在表现力与稀疏性之间取得平衡；(4) 对含有大量细节或纹理噪声的复杂物体，稀疏3D笔划可能无法完整表达所有视觉特征；(5) 方法目前仅处理孤立物体，尚未扩展到包含多物体和背景的场景。

**后续启发。** 3Doodle 打开了几个有价值的研究方向：(1) 自动确定最优基元数量（贝塞尔曲线和超二次曲面的个数）的自适应机制，以在紧凑性和表现力之间自动平衡；(2) 将深度排序和遮挡融入可微渲染管线，使生成的线框草图更符合物理真实；(3) 将紧凑的3D笔划用于下游任务，如3D编辑、动画驱动、跨视图对应或作为3D生成模型的中间表示；(4) 探索将方法扩展到更复杂的场景，通过分层或分区域策略处理多物体和背景。此外，这一“用可微基元+感知损失做逆抽象”的范式也可启发其他领域的紧凑表示学习。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/3Doodle_Compact_Abstraction_of_Objects_With_3D_Strokes.pdf]]