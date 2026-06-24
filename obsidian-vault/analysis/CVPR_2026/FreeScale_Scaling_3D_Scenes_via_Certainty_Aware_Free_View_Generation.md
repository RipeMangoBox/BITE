---
title: "FreeScale: Scaling 3D Scenes via Certainty-Aware Free-View Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FreeScale_Scaling_3D_Scenes_via_Certainty_Aware_Free_View_Generation.pdf
project_link: "https://mvp-ai-lab.github.io/FreeScale"
code_link: null
aliases:
- FreeScale
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 确定度感知的视角图采样策略：通过从重建的3D高斯中构建确定度网格，并基于加权交并比（WIoU）建立视角图，选择既能捕捉丰富语义信息又受重建伪影影响最小的新视角，从而实现高质量的数据增广。
primary_logic: 将不完美的重建场景视为几何代理，利用确定度引导的采样策略生成大量高质量、高多样性的自由视角图像，这些数据不仅能扩展训练集以提升前馈模型的泛化能力，还能通过主动不确定性探索增强每场景的3D高斯优化。
claims:
- LVSM 在大相机运动场景中使用 FreeScale 数据后 PSNR 大幅提升（18.75 dB -> 21.45 dB）。
- FreeScale 在 DL3DV、Nerfbusters 和 Tanks & Temples 等数据集上一致地改进每场景重建质量。
- 去除扩散增强后，PSNR 仍大幅提升（+2.14 dB），表明主要提升来自视角覆盖而非扩散先验。
- 消融实验证明视角图对于减少冗余和提升性能至关重要：与随机选择相比，基于视角图的采样在 PSNR、SSIM 上均有显著提升。
---

# FreeScale: Scaling 3D Scenes via Certainty-Aware Free-View Generation

> [!tip] 核心洞察
> 将不完美的重建场景视为几何代理，利用确定度引导的采样策略生成大量高质量、高多样性的自由视角图像，这些数据不仅能扩展训练集以提升前馈模型的泛化能力，还能通过主动不确定性探索增强每场景的3D高斯优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | FreeScale：通过确定度感知自由视角生成扩展三维场景 |
| 英文题名 | FreeScale: Scaling 3D Scenes via Certainty-Aware Free-View Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.10512) · [Project](https://mvp-ai-lab.github.io/FreeScale) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | FreeScale |
| Dataset | DL3DV, MipNeRF360, Nerfbusters, Tanks & Temples |

> [!tip] 效果简介
> - DL3DV (Large Camera Motion) 上，PSNR 21.45 vs 18.75 (+2.70)。
> - MipNeRF360 (OOD) 上，PSNR 17.27 vs 13.88 (+3.39)。
> - DL3DV (Per-Scene) 上，PSNR 19.57 vs 19.18 (+0.39)。

## 概述

三维场景理解与重建的核心瓶颈在于高质量训练数据的匮乏：真实世界捕获虽真实但视角稀疏离散，合成数据存在域间隙，而扩散生成方法难以提供精确的相机位姿。若简单地从有瑕疵的重建几何中采样新视角，则会放大伪影，严重损害前馈模型的泛化能力。

FreeScale 提出了一条**确定度感知的自由视角生成**路径来解决这一困境。其核心洞察在于：将不完美的重建场景视为几何代理，利用确定度引导的采样策略，在捕捉丰富语义信息与规避重建伪影之间取得最优折衷。具体而言，该方法从重建的 3D 高斯中构建确定度网格，基于加权交并比（WIoU）建立视角图，并通过非极大抑制筛选出高质量、高多样性的自由视角图像。

这些生成数据同时服务于两条技术路线：**扩展前馈模型的训练集**以提升跨场景泛化能力，以及**通过主动不确定性探索增强每场景的 3D 高斯优化**。实验表明，仅增加 22% 的生成自由视角，LVSM 在大相机运动场景下的 PSNR 即从 18.75 dB 提升至 21.45 dB（+2.70 dB）；在 DL3DV、Nerfbusters 和 Tanks & Temples 等多个基准上，FreeScale 一致地改进了每场景重建质量。消融实验进一步揭示，主要性能增益来源于视角覆盖的扩展，而非扩散先验的引入——去除扩散增强后，PSNR 仍大幅提升 2.14 dB。

**方法定位**：FreeScale 属于数据增广驱动的新视角合成增强框架，与前馈方法（如 LVSM）、基于优化的方法（如 3DGS，Kerbl et al., SIGGRAPH 2023）、扩散增强方法（如 DIFIX3D+）以及几何先验增强方法（如 Nerfbusters）形成互补或增强关系。其独特之处在于将确定度感知的视角图采样作为统一的数据生成策略，同时服务于前馈训练和每场景优化两种范式。

## 背景与动机

三维场景理解与重建是计算机视觉的核心任务，其关键瓶颈之一在于可泛化的新视角合成模型受限于训练数据的规模与多样性。当前的前馈式新视角合成方法（如 **LVSM**）虽然在稀疏视角重建上展现出潜力，但其泛化能力严重受制于训练场景的数量与相机轨迹的丰富程度。真实世界捕获数据虽然具备高度真实性，但通常稀疏且离散，难以覆盖大范围相机运动下的视角变化；合成数据虽然可以无限生成，却存在显著的合成-真实域间隙；而基于扩散模型的生成方法尽管能产出逼真图像，却无法提供精确的相机位姿，难以直接用于三维任务训练。

现有数据增广策略面临一个根本性困境：从不完美的重建几何中简单采样新视角，会不可避免地放大重建伪影，反而损害模型的泛化能力。具体而言，基于3D高斯泼溅（**3DGS**, Kerbl et al., SIGGRAPH 2023）等优化方法重建的场景，在未充分观测区域往往存在漂浮体、几何噪声等伪影。若不加区分地从这些区域渲染新视角，生成的训练数据将携带大量错误信号，导致前馈模型学习到偏差化的几何先验。另一方面，现有的视角选择策略——无论是随机采样还是基于位姿距离的顺序采样——均无法有效区分“信息丰富且重建可靠”的视角与“受伪影污染”的视角，造成数据增广的效率低下甚至适得其反。

这一困境在真实应用场景中尤为突出：当训练相机运动幅度较小而测试时需处理大相机运动时，模型的性能会急剧下降。例如，**LVSM** 在大相机运动场景下的PSNR仅为18.75 dB，远不能满足实际部署需求。这表明，现有方法缺乏一种系统性的机制，能够从有限且不完美的重建中挖掘出对泛化能力真正有益的训练信号。

FreeScale正是针对上述缺口提出的解决方案。其核心动机在于：将不完美的重建场景视为几何代理，而非最终的真值；通过设计确定度感知的采样策略，主动识别那些既能捕捉丰富语义信息、又受重建伪影影响最小的新视角，从而在“信息增益”与“伪影风险”之间取得精细平衡。这一思路将数据增广从被动的几何采样升级为主动的质量引导探索，为突破前馈模型的数据瓶颈提供了新的范式。

## 核心创新

FreeScale 的核心创新在于将不完美的三维重建场景转化为几何代理，通过**确定度感知的视角图采样策略**生成高质量、高多样性的自由视角图像，从而同时解决前馈新视角合成模型的数据稀缺问题和每场景三维重建的欠观测问题。

### 从随机采样到确定度感知的视角图采样

传统数据增广方法在从重建几何中采样新视角时，通常采用随机采样或基于帧距离的顺序采样。这种策略存在两个根本缺陷：一是容易采样到重建质量差的区域，导致生成的图像放大伪影而非提供有效信息；二是缺乏对视角间信息冗余的度量，可能生成大量重复视角，浪费计算资源且对模型训练贡献有限。

FreeScale 通过三个关键机制改变了这一采样范式：

**1. 确定度网格构建（Certainty Grid）**  
从重建的三维高斯表征出发，将场景空间划分为体素网格，并为每个体素 $v_i$ 计算确定度分数：

$$\mathcal{C}(\boldsymbol{v}_i) = \sum_{g_j \in \mathcal{G}_i} \frac{\alpha_j}{\mathrm{Vol}_j + \epsilon}$$

其中 $\alpha_j$ 为高斯的不透明度，$\mathrm{Vol}_j \triangleq \prod_{k=1}^{3} \exp((\mathbf{s}_j)_k)$ 为高斯的体积。这一设计使得确定度分数同时反映了区域的**几何覆盖密度**（高斯数量多则确定度高）和**重建精度**（体积小的高斯通常对应精细结构，权重更高）。确定度网格本质上是一张场景的“可信度地图”，为后续采样提供了避开重建伪影区域的依据。

**2. 基于加权交并比的视角图（View Graph）**  
在确定度网格的基础上，FreeScale 构建视角图来度量候选视角之间的信息重叠程度。对于视角 $i$，其对体素 $v_k$ 的加权可见性定义为：

$$W_{i,k} = \mathcal{C}(v_k) \cdot M_{i,k}$$

其中 $M_{i,k}$ 为二值可见性掩膜。两个视角 $i$ 和 $j$ 之间的加权交并比（WIoU）为：

$$\operatorname{WIoU}(i,j) = \frac{\sum_{k=1}^{N} \min(W_{i,k}, W_{j,k})}{\sum_{k=1}^{N} \max(W_{i,k}, W_{j,k})}$$

WIoU 度量的是两个视角在**高确定度信息**上的重叠程度。与传统的基于位姿距离的视角关系度量相比，WIoU 直接反映了视角在场景几何层面的语义对应关系，能够有效识别信息冗余的视角对。

**3. 非极大抑制视角选择**  
基于视角图，FreeScale 采用类似非极大抑制的策略选择候选视角：优先选择确定度得分高且与其他已选视角 WIoU 低的视角。这确保了生成的自由视角集合既覆盖了场景中重建可靠的区域，又最大化了视角多样性。消融实验（Table 6）表明，移除视角图仅靠确定度得分选择候选视角会导致 PSNR 从 17.75 dB 下降到 17.63 dB，且图像冗余度高；而移除确定度网格、仅基于位姿距离计算视角对应则导致性能不稳定且计算开销增大。

### 视角图引导的参考图像选择

在自由视角图像的扩散增强阶段，现有方法（如 **DIFIX3D+**）通常基于位姿距离选择最近的参考图像。然而，位姿接近并不保证可见区域的对应关系——两个相机可能位置相近但朝向不同，观测到完全不同的场景区域。

FreeScale 利用视角图的二阶连接关系来选择参考图像：对于待增强的自由视角，在视角图中找到与其共享高确定度可见区域的训练视角作为参考。这一策略确保了参考图像与目标视角在几何内容上的高度一致性，从而避免了扩散模型因参考不匹配而引入的伪影。消融实验（Table 3）显示，使用距离参考（w/ dist ref）导致 PSNR 从 19.18 dB 下降到 17.88 dB，验证了视角图参考选择的关键作用。

### 课程学习驱动的训练策略

FreeScale 将视角图进一步应用于前馈模型的训练策略设计。传统方法以固定帧距离采样训练批次，而 FreeScale 采用课程学习策略：训练初期从高 WIoU 邻居开始（视角变化小，学习难度低），逐步过渡到低 WIoU 邻居（视角变化大，学习难度高）。这一策略使模型能够渐进地适应大视角变化，从而提升对稀疏输入和大相机运动的泛化能力。

### 关键证据总结

- **核心增益来源**：去除扩散增强后，PSNR 仍大幅提升（+2.14 dB，Table 7），表明主要提升来自视角覆盖的扩展而非扩散先验，验证了确定度感知采样策略的核心作用。
- **视角图的必要性**：与随机加入自由视图（+FV random）相比，基于视角图的选择在两项任务上性能均显著更优（Table 5），且移除视角图导致候选视角冗余度高、训练效果下降（Table 6）。
- **跨任务泛化**：FreeScale 生成的自由视角数据一致地提升了前馈模型 LVSM 的泛化能力（DL3DV 大运动场景 PSNR 从 18.75 dB 提升至 21.45 dB）和每场景 3DGS 的重建质量（DL3DV、Nerfbusters、Tanks & Temples 三个数据集上均有提升，Table 2）。

## 整体框架

FreeScale 的整体流程围绕一个核心洞察展开：**将不完美的重建场景视为几何代理，通过确定度引导的采样策略生成大量高质量、多样化的自由视角图像**。这些生成数据既能扩展训练集以提升前馈模型的泛化能力，又能通过主动不确定性探索增强每场景的 3D 高斯优化。

如图 2 所示，整个 pipeline 由三个紧密衔接的阶段构成：

**阶段一：场景重建。** 给定稀疏多视角图像序列，首先将场景重建为连续的 3D 高斯表征（3DGS，Kerbl et al., SIGGRAPH 2023）。这一步的目的是获得一个可微分、可渲染的几何代理，使得后续可以在任意虚拟相机位姿处生成候选视角，而不受原始采集轨迹的限制。

**阶段二：确定度感知的自由视角合成。** 这是 FreeScale 的核心创新所在。该阶段包含四个关键子模块：

1. **确定度网格构建**：从重建的 3D 高斯中，将场景空间离散化为体素网格，每个体素 $v_i$ 的确定度通过累加落入其中的高斯的不透明度与体积之比得到：
   $$\mathcal{C}(\boldsymbol{v}_i) = \sum_{g_j \in \mathcal{G}_i} \frac{\alpha_j}{\mathrm{Vol}_j + \epsilon}$$
   其中 $\mathrm{Vol}_j \triangleq \prod_{k=1}^{3} \exp((\mathbf{s}_j)_k)$ 为高斯 $g_j$ 的体积。确定度越高，表示该区域的重建越可靠。

2. **视角图构建**：基于确定度网格，为候选虚拟视角建立图结构。节点为视角，边权重由加权交并比（WIoU）度量：
   $$\operatorname{WIoU}(i,j) = \frac{\sum_{k=1}^{N} \min(W_{i,k}, W_{j,k})}{\sum_{k=1}^{N} \max(W_{i,k}, W_{j,k})}$$
   其中 $W_{i,k} = \mathcal{C}(v_k) \cdot M_{i,k}$ 为视角 $i$ 对体素 $v_k$ 的加权可见性。WIoU 衡量两个视角在高确定度信息上的重叠程度，高 WIoU 意味着视角冗余，低 WIoU 则意味着互补性强。

3. **虚拟视角生成与选择**：在预定义的多种相机轨迹模式（如轨道、推拉等，见图 3）上密集采样候选位姿，渲染后通过视角图进行非极大抑制，去除冗余候选。随后通过 BRISQUE 无参考图像质量评分和归一化深度范围检查过滤低质量渲染结果，并对位姿进行迭代插值校正。

4. **图像校正**：对筛选后的自由视角图像，使用单步扩散模型 **DIFIX3D+** 进行真实感增强。与传统基于位姿距离选择参考图像的方式不同，FreeScale 利用预构建的视角图选择二阶连接的共享可见区域作为参考，确保校正过程在几何一致的高确定度区域进行（见图 6、图 8、图 10）。

**阶段三：自由视角引导的训练与优化。** 生成的自由视角数据以两种方式赋能下游任务：

- **前馈模型训练**：选择与现有训练相机 WIoU 最低的 Top-K 自由视角作为辅助目标，并采用基于视角图的课程学习策略——训练初期优先选择高 WIoU 邻居（容易学习），后期逐步转向低 WIoU 或更大几何分离度的视角（困难样本），从而稳定提升模型的泛化边界。
- **每场景优化**：将低 WIoU 的自由视角作为伪标签加入 3DGS 优化，损失函数为：
  $$\mathcal{L}_{\mathrm{FV}} = \alpha^{\mathrm{fv}} \left( || I - I^{\mathrm{fv}} ||_1 + (1 - \mathcal{L}_{\mathrm{SSIM}}(I, I^{\mathrm{fv}})) \right)$$
  其中 $\alpha^{\mathrm{fv}}$ 为根据自由视角质量衰减的权重，确保低质量伪标签对优化的影响受控。

**输入输出流总结**：输入为稀疏多视角图像序列；中间产物为 3D 高斯表征、确定度网格、视角图及经过质量过滤与校正的自由视角图像；最终产出为增强后的训练数据集（用于前馈模型如 **LVSM** 的联合训练）和优化后的每场景 3D 高斯（用于新视角合成）。整个 pipeline 无需额外的人工标注或精确的相机轨迹先验，仅依赖初始重建几何作为引导。

**关键设计决策的因果链路**：确定度网格 → 视角图 → 非冗余采样 → 高质量自由视角 → 数据增广 + 不确定性探索 → 泛化能力与重建质量双提升。消融实验（Table 6）证实，移除视角图仅靠确定度得分选择候选视角会导致高冗余且性能下降；移除确定度网格则只能依赖位姿距离计算视角对应，既不准确又计算低效。Table 7 进一步表明，即使去除扩散增强，PSNR 仍大幅提升（+2.14 dB），说明主要增益来自视角覆盖的扩展，而非扩散先验的注入。

### 补充图表

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/002_Figure_2.jpg]]
*Figure 2: FreeScale generation pipeline. Our overall pipeline consists of three phases. First, given an image sequence, we reconstruct the scene as a continuous 3D representation, which allows us to place arbitrary viewpoint candidates. Second, we perform certainty-aware freeview synthesis: we establish a view graph based on a certainty grid and filter redundant candidates. Finally, we apply image rectification to produce the final free-views. The generated data can then be used to train feed-forward models like LVSM and refine the scene Gaussians*

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/001_Figure_1.jpg]]
*Figure 1: We introduce FreeScale, a framework that scales current scene data by generating free-view images from reconstructed scene geometry, which can be used for feed-forward model training. Training LVSM with an additional 22% of generated free-views significantly improves sparse-view reconstruction from PSNR 18.75 to 21.45, particularly enhancing its generalization to large camera motion*

## 核心模块与公式推导

FreeScale 将不完美的 3DGS 重建场景转化为几何代理，通过确定度感知的采样策略生成高质量自由视角图像。整个生成管线包含四个核心模块：场景重建、确定度感知自由视角合成、图像校正增强、以及自由视角引导训练。以下聚焦前三者的关键设计与公式。

### 4.1 确定度网格构建

从稀疏多视角输入重建 3D 高斯表征后，FreeScale 首先构建一个确定度网格，用于量化场景空间中各区域的重建可靠度。该网格通过对场景空间进行体素化得到，每个体素 $\boldsymbol{v}_i$ 的确定度定义为落入其边界内的所有高斯中心的个体确定度得分之和：

$$
\mathcal{C}(\boldsymbol{v}_i) = \sum_{g_j \in \mathcal{G}_i} \frac{\alpha_j}{\mathrm{Vol}_j + \epsilon}
$$

其中 $\mathcal{G}_i$ 表示中心落入体素 $\boldsymbol{v}_i$ 的高斯集合，$\alpha_j$ 为高斯 $g_j$ 的不透明度，$\mathrm{Vol}_j$ 为该高斯的体积，定义为三个尺度参数的指数乘积：

$$
\mathrm{Vol}_j \triangleq \prod_{k=1}^{3} \exp((\mathbf{s}_j)_k)
$$

$\epsilon$ 为防止除零的小常数。核心直觉：**体积小且不透明度高的高斯贡献更高的确定度**，这类高斯通常对应重建良好的精细几何结构（如边缘、纹理区域）；反之，体积大且不透明度低的高斯往往对应重建不确定的模糊区域。确定度网格由此为后续视角选择提供了场景级的质量地图。

### 4.2 确定度感知视角图构建

在确定度网格基础上，FreeScale 构建视角图来管理候选虚拟视角之间的关系。视角图的节点为候选视角，边权重由加权交并比（Weighted IoU, WIoU）定义。

首先定义视角 $i$ 对体素 $v_k$ 的加权可见性：

$$
W_{i,k} = \mathcal{C}(v_k) \cdot M_{i,k}
$$

其中 $M_{i,k} \in \{0, 1\}$ 为二值可见性掩膜，指示体素 $v_k$ 在视角 $i$ 下是否可见。该公式将确定度与可见性耦合：**只有同时满足“重建可靠”且“当前视角可见”的体素才对视角间关系产生贡献**。

基于加权可见性，视角 $i$ 与 $j$ 之间的 WIoU 定义为：

$$
\operatorname{WIoU}(i,j) = \frac{\sum_{k=1}^{N} \min(W_{i,k}, W_{j,k})}{\sum_{k=1}^{N} \max(W_{i,k}, W_{j,k})}
$$

WIoU 度量两个视角在高确定度信息上的重叠程度。高 WIoU 表示两视角观察到的可靠几何高度重合（信息冗余），低 WIoU 表示两视角互补性强。视角图构建后，FreeScale 通过非极大抑制从候选视角中筛选出高多样性、低冗余的自由视角集合，确保生成的增广数据既捕获丰富语义信息，又最小化重建伪影的放大效应。

### 4.3 自由视角质量评估与校正

生成的自由视角渲染图像需经过质量过滤与校正。FreeScale 采用组合度量进行评估：

- **BRISQUE 分数**：无参考图像质量评估指标，衡量渲染图像的视觉保真度；
- **归一化深度范围指标**：确认渲染视角包含足够的几何内容，排除退化视角（如纯天空区域）。

通过质量筛选的视角进一步经过**迭代位姿插值校正**，以缓解 3DGS 渲染中可能的位姿偏差。随后，FreeScale 引入一步扩散模型 **DIFIX3D** 进行图像校正增强，关键创新在于：不同于传统基于位姿距离的最近参考图像选择，FreeScale 利用视角图引导参考选择——选择与待校正视角共享最大可见区域（即视角图中二阶连接的高 WIoU 节点）的训练图像作为参考。这确保了扩散模型在正确的图像分布条件下进行细化，避免因参考图像与目标视角内容不匹配而引入的伪影。

### 4.4 自由视角引导训练

生成的自由视角数据通过两条路径反哺模型训练：

**前馈模型训练**：选择与现有训练相机 WIoU 最低的 top-K 自由视角作为辅助目标，这些低 WIoU 视角代表对原始数据集的最大信息补充。训练批次基于视角图的邻接关系选择，并采用课程学习策略——逐步从高 WIoU 邻居转向低 WIoU 邻居，使模型渐进式适应更大视角变化。自由视角的训练损失为：

$$
\mathcal{L}_{\mathrm{FV}} = \alpha^{\mathrm{fv}} \left( || I - I^{\mathrm{fv}} ||_1 + (1 - \mathcal{L}_{\mathrm{SSIM}}(I, I^{\mathrm{fv}})) \right)
$$

其中 $\alpha^{\mathrm{fv}}$ 为基于自由视角质量的衰减权重，联合优化 L1 像素损失与 SSIM 结构相似性损失。

**每场景优化**：同样选择低 WIoU 自由视角作为伪标签，对 3DGS 进行额外优化，主动探索重建不确定区域，提升单场景重建质量。

### 补充图表

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/010_Figure_6.jpg]]
*Figure 6: Comparison of reference image selection. Our view graph identifies the shared visible region with the noisy view (red circle), ensuring accurate image rectification*

## 实验与分析

### 核心实验设置

FreeScale 在两个互补的任务维度上验证其有效性：**前馈新视角合成模型的泛化能力提升**，以及**每场景 3D 高斯优化的重建质量增强**。前馈实验以 **LVSM** 为基线，在 DL3DV 数据集上分别评估小相机运动和大相机运动两种设置，并进一步在 MipNeRF360 上测试跨域泛化能力。每场景优化实验以 **3DGS**（Kerbl et al., SIGGRAPH 2023）为基线，在 DL3DV、Nerfbusters 和 Tanks & Temples 三个数据集上采用 Out-Of-Domain 协议进行评估。所有实验中，FreeScale 仅使用原始训练数据额外生成约 22% 的自由视角图像作为增广数据。

### 前馈模型泛化能力

Table 1 展示了前馈模型在视角泛化任务上的定量对比。在大相机运动设置下，LVSM 联合 FreeScale 生成的自由视角数据训练后，PSNR 从 18.75 dB 提升至 21.45 dB（+2.70 dB），SSIM 从 0.572 提升至 0.647，LPIPS 从 0.345 降至 0.291。在小相机运动设置下，PSNR 同样从 22.20 dB 提升至 24.20 dB（+2.00 dB）。值得注意的是，在 MipNeRF360 这一跨域测试集上，FreeScale 带来的增益更为显著：PSNR 从 13.88 dB 跃升至 17.27 dB（+3.39 dB），表明自由视角增广有效缓解了前馈模型对训练位姿分布的过拟合，显著增强了模型在未见相机轨迹下的泛化能力。

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of feed-forward models on viewpoint generalization. Joint training with our FVGen data yields consistent improvements across both small and large camera motion settings*

Figure 4 的定性对比进一步印证了这一结论。在目标视角与训练位姿差异较大的挑战性区域（图中红色框标注），LVSM 基线产生明显的模糊和结构失真，而 FreeScale 增强后的模型能够恢复更清晰的纹理细节和几何结构。

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison for feed-forward model. We use red boxes to highlight challenging regions where the target viewpoint differs significantly from the corresponding areas in the training poses*

### 每场景重建质量

Table 2 报告了 Out-Of-Domain 协议下每场景重建的定量结果。3DGS 联合 FreeScale 在 DL3DV 上取得 19.57 dB PSNR，较基线 19.18 dB 提升 0.39 dB；在 Nerfbusters 上从 18.14 dB 提升至 18.40 dB；在 Tanks & Temples 上从 20.37 dB 提升至 20.66 dB。三个数据集的 SSIM 和 LPIPS 指标同样呈现一致改善。Figure 5 的定性结果揭示了性能提升的关键机制：3DGS 基线在未观测区域产生大量浮动体和几何噪声，而 FreeScale 通过从重建几何中采样补充视角，有效约束了这些欠观测区域的优化过程，从而获得更高保真度的重建结果。

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of per-scene reconstruction on the Out-Of-Domain protocol. Our FreeScale achieves consistent advantages in PSNR and SSIM without incurring a significant increase in computational burden*

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results on the Nerfbusters dataset. The 3DGS baseline exhibits significant artifacts in unobserved areas, such as floaters and geometric noise, particularly in unobserved areas. In contrast, our method ensures high-fidelity results by sampling supplementary views from the reconstructed scene geometry*

### 消融实验

#### 扩散增强的贡献解耦

Table 7 的消融实验明确区分了视角覆盖与扩散先验的各自贡献。去除扩散增强后（wo/ Diffusion），PSNR 仍从基线 18.75 dB 大幅提升至 20.89 dB（+2.14 dB），占总提升（+2.70 dB）的约 79%。这一结果表明，**性能提升的主要驱动力来自自由视角带来的视角多样性和几何覆盖扩展**，而非扩散模型的生成先验。在此基础上集成扩散增强（完整 FreeScale）可进一步消除残余伪影，达到最优保真度 21.45 dB。

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/013_Table_7.jpg]]
*Table 7: Ablation isolating the impact of diffusion-based image rectification. Comparing the LVSM baseline to our method without diffusion (wo/ Diffusion) demonstrates that the primary performance boost stems directly from the expanded viewpoint diversity and geometric coverage. Integrating the diffusion prior (FreeScale) resolves remaining artifacts for optimal fidelity*

#### 视角图的核心作用

Table 6 直接验证了视角图在自由视角生成中的关键性。移除视角图、仅依赖确定度得分选择候选视角时，PSNR 从 17.75 dB 降至 17.63 dB，且生成的图像冗余度显著升高，无法为前馈模型训练提供有效指导。移除确定度网格、仅基于位姿距离计算视角对应关系时，不仅性能不稳定，计算开销也大幅增加。这证明 **WIoU 视角图在平衡信息多样性与去冗余方面具有不可替代的作用**。

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/011_Table_6.jpg]]
*Table 6: Ablation study on Free-View generation. Our certainty-aware generation relies fundamentally on the certainty grid and the established view graph. Without the view graph, selecting the top-500 candidates solely by certainty score results in high redundancy and fails to provide valuable guidance for feed-forward model training. Without the certainty grid, we must resort to calculating inter-view correspondence only via position and rotation distance, which is both inaccurate and computationally inefficient*

#### 视角图引导的参考选择

Table 3 针对每场景优化的消融显示，将视角图引导的参考选择替换为基于位姿距离的最近参考选择（w/ dist ref）后，PSNR 从 19.18 dB 骤降至 17.88 dB，降幅达 1.30 dB。Figure 6 和 Figure 8 直观对比了两种策略的差异：基于位姿距离的参考选择可能选取与目标视角可见区域重叠不足的图像，导致扩散校正阶段引入严重伪影（蓝色框标注）；而视角图能够准确识别共享可见区域（红色圆圈标注），确保图像校正的一致性。

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/008_Table_3.jpg]]
*Table 3: Ablation of per-scene optimization on DL3DV. “w/ dist ref”: distance-based reference for rectification. “w/ sparse init.”: incomplete initialization*

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/014_Figure_8.jpg]]
*Figure 8: Consistent showcases of view graph impact. Compared to DIFIX3D+’s distance-based reference selection strategy, our view graph provides better overlap and higher free-view consistency for reference. The red bounding boxes delineate artifacts introduced by inaccurate reference images during the image rectification stage*

#### 视角图引导的数据选择

Table 5 对比了基于视角图的自由视角选择与随机选择对两项任务的影响。在前馈模型训练中，随机加入自由视图（+FV random）的性能显著低于视角图引导的联合训练（View-graph）；在每场景优化中，基于 WIoU 选择低重叠度的自由视角同样优于随机选择。这一结果验证了 **“选择与现有训练视角信息互补最大的自由视角”这一策略的有效性**。

![[assets/figures/papers/paper_list_l2491_https_arxiv_org_abs_2604_10512/figures/009_Table_5.jpg]]
*Table 5: Ablation study on free-view images. “FV” indicate generated free-view images, “View-graph” means graph-guided joint training and certainty-guided per-scene reconstruction*

#### 数据稀疏度鲁棒性

Table 4 在 Tanks & Temples 数据集上测试了不同数据稀疏度（10%~50%）下的性能。FreeScale 在所有稀疏度级别上均一致优于 3DGS 基线，表明该方法对输入数据的稀疏程度具有良好的鲁棒性。

### 失败模式分析

Figure 16 展示了 FreeScale 自由视角生成的两类典型失败案例。第一类涉及复杂视角相关反射：扩散模型难以正确处理镜面反射的一致性，导致反射内容失真（上图红色圆圈）。第二类源于 3DGS 浮动体：扩散增强可能将重建中的浮动体误判为有效结构并过度锐化，反而强化了伪影（下图红色圆圈）。这些失败模式根源于**外部扩散模型与自由视角校正任务之间的适配不足**——扩散模型缺乏对场景几何确定度的感知能力，无法区分可靠结构与重建伪影。

### 方法谱系与知识库定位

FreeScale 处于**数据增广驱动的新视角合成**这一研究脉络中。与传统的基于位姿插值或随机采样的数据增广策略不同，FreeScale 首次将重建几何的确定度显式建模为采样指导信号。其核心创新——确定度感知的 WIoU 视角图——在概念上区别于 **DIFIX3D+** 的纯扩散增强路径和 **Nerfbusters** 的几何先验注入路径：前者依赖生成先验修复图像质量，后者通过深度正则化约束几何优化，而 FreeScale 通过主动探索欠观测区域来扩展数据覆盖，从数据层面提升模型的泛化边界。在技术定位上，FreeScale 是一种**模型无关的数据增广框架**，可与各类前馈模型（如 LVSM）和基于优化的方法（如 3DGS）协同工作，其增广数据可作为即插即用的训练资源直接融入现有流程。

## 方法谱系与知识库定位

### 1. 核心问题域定位

FreeScale 解决的核心瓶颈是**可泛化新视角合成模型的训练数据稀缺性**。现有前馈模型（如 LVSM）受限于训练场景数量有限、相机轨迹稀疏且缺乏多样性，导致在大相机运动或域外场景下泛化能力不足。与此同时，每场景优化方法（如 3DGS）在稀疏输入下容易在未观测区域产生漂浮物和几何噪声。FreeScale 的独特定位在于：**将不完美的重建场景作为几何代理，通过确定度感知的采样策略从代理中挖掘高质量、高多样性的自由视角数据，同时服务于前馈模型训练和每场景优化增强**。

### 2. 与基线方法的关系谱系

#### 2.1 前馈新视角合成基线：LVSM

LVSM 是 FreeScale 在前馈模型训练任务中的直接基线。LVSM 采用固定帧距离采样训练批次，在稀疏视角重建中表现出色，但在大相机运动场景下 PSNR 仅为 18.75 dB。FreeScale 通过视角图引导的课程学习策略，逐步从高 WIoU 邻居转向低 WIoU 邻居，使 LVSM 在大相机运动场景下 PSNR 提升至 21.45 dB（+2.70 dB），在域外 MipNeRF360 数据上从 13.88 dB 提升至 17.27 dB（+3.39 dB）。消融实验（Table 7）表明，去除扩散增强后 PSNR 仍大幅提升（+2.14 dB），说明主要增益来自视角覆盖扩展而非扩散先验，证实了数据增广策略本身的有效性。

#### 2.2 基于优化的新视角合成基线：3DGS

3DGS（Kerbl et al., SIGGRAPH 2023）是每场景优化任务的基线。FreeScale 通过选择与现有训练相机 WIoU 最低的 K 个自由视角作为伪标签，主动探索重建不确定区域。在 DL3DV 数据集上，3DGS w/ FreeScale 实现 PSNR 19.57 dB（基线 19.18 dB），在 Nerfbusters 上达到 18.40 dB（基线 18.14 dB），在 Tanks & Temples 上达到 20.66 dB（基线 20.37 dB）。这些一致但克制的提升表明，FreeScale 在不过度增加计算负担的前提下，有效补充了稀疏输入下的几何约束。

#### 2.3 扩散增强基线：DIFIX3D+

DIFIX3D+ 是图像校正阶段的基线方法。其原始实现基于位姿距离选择最近参考图像，在视角差异大时容易引入不准确的参考，导致校正图像产生幻觉内容（Figure 13 展示了灯具虚假反射和桌面细节损坏）。FreeScale 将参考选择策略替换为视角图引导的二阶连接选择，确保参考视图与待校正视图共享高确定度可见区域（Figure 6, Figure 8, Figure 10）。消融实验（Table 3）表明，使用距离参考的变体（w/ dist ref）导致 PSNR 从 19.18 dB 骤降至 17.88 dB，验证了视角图参考选择的关键作用。

#### 2.4 几何先验增强基线：Nerfbusters

Nerfbusters 代表利用几何先验增强重建的基线方向。FreeScale 在 Nerfbusters 数据集上取得 18.40 dB PSNR，优于基线 18.14 dB。定性结果（Figure 5）显示，3DGS 基线在未观测区域存在显著的漂浮物和几何噪声，而 FreeScale 通过从重建几何中采样补充视角，确保了高保真度结果。

### 3. 关键设计决策的消融证据

**视角图 vs. 随机选择**：随机加入自由视图（+FV random）在两项任务上性能均劣于视角图引导选择（Table 5），证明视角图对于减少冗余和提升性能至关重要。

**视角图 vs. 纯确定度得分**：移除视角图仅靠确定度得分选择候选视角，导致 PSNR 从 17.75 dB 降至 17.63 dB，且图像冗余度高（Table 6），表明非极大抑制式的视角图过滤不可或缺。

**确定度网格 vs. 位姿距离**：移除确定度网格后，基于位姿距离计算视角对应关系，导致性能不稳定且计算开销增大（Table 6），验证了确定度感知的 WIoU 度量在捕捉几何对应关系上的优势。

**多模态轨迹 vs. 单轨迹**：仅依赖 Orbit 轨迹限制了视角多样性，在欠观测区域产生明显模糊伪影；多模态采样确保了最大场景覆盖（Figure 9）。

**数据稀疏度鲁棒性**：在 Tanks & Temples 数据集上，不同稀疏度（10%~50%）下 FreeScale 均优于基线（Table 4），展示了方法的鲁棒性。

### 4. 适用边界与局限

**外部扩散模型的依赖与伪影风险**：自由视角校正阶段依赖 DIFIX3D 扩散模型，可能引入残余伪影。失败案例（Figure 16）揭示了两个典型问题：(1) 对复杂视角相关反射的错误处理；(2) 将 3DGS 漂浮体误判为有效结构并过度锐化。这表明扩散模型的合成-真实域间隙在特定场景下仍构成瓶颈。

**恶劣条件下的有效视角稀缺**：在极端低光照等恶劣条件下，严格的质量过滤机制（BRISQUE 分数 + 归一化深度范围检查）会拒绝大量渲染结果，导致有效自由视角数量不足，限制了方法的增益空间。

**计算管线复杂度**：虽然 FreeScale 声称不显著增加计算负担，但完整的生成管线涉及 3D 高斯重建、确定度网格计算、视角图构建、虚拟视角渲染、质量评估、位姿校正和扩散增强，实际部署时需权衡各阶段的算力分配。

### 5. 开放问题

1. **扩散模型域适应**：如何微调外部扩散模型以降低合成-真实域间隙，使其更好地适应 FreeScale 的采样策略？当前失败案例表明，扩散先验在特定材质和光照条件下的泛化能力仍是薄弱环节。

2. **确定度条件控制**：如何将视角特定的确定度可见性掩膜集成到扩散模型的条件控制中，使其仅在不确定区域进行细化，而非全局影响原图像分布？这有望在保持已知区域真实性的同时，仅修复不可靠区域。

3. **动态场景扩展**：当前方法假设静态场景，对于包含动态物体的场景，确定度网格和视角图的构建逻辑需要重新设计，以区分静态几何和动态区域的可靠性。

4. **与其他数据增广范式的融合**：FreeScale 的确定度感知采样策略是否可与基于生成式模型（如视频扩散模型）的自由视角生成方法互补，在更稀疏的输入条件下联合提升数据多样性？

## 原文 PDF

![[paperPDFs/CVPR_2026/FreeScale_Scaling_3D_Scenes_via_Certainty_Aware_Free_View_Generation.pdf]]