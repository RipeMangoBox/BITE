---
title: Unsupervised Representation Learning for 3D Mesh Parameterization with Semantic and Visibility Objectives
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Unsupervised_Representation_Learning_for_3D_Mesh_Parameterization_with_Semantic_fb445667e240.pdf
project_link: "https://ahhhz975.github.io/Automatic3DMeshParameterization/"
code_link: "https://github.com/AHHHZ975/Semantic-Visibility-UV-Param"
aliases:
- SVAUP
- URL3MPSVO
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 提出两个新颖的感知目标函数：语义感知目标，通过形状直径函数（ShDF）分割与逐部分参数化，迫使UV图表与语义3D部件对齐；可见性感知目标，利用环境光遮蔽（AO）作为可见性代理，设计可微的AO加权缝线损失，将切割缝线引导至遮挡/低可见性区域。
primary_logic: 通过“分割-参数化”策略，在保留几何低畸变的基础双向循环映射架构上叠加语义与可见性约束，可在不显著牺牲保角/保面积特性的前提下，生成语义一致、视觉无缝的UV图谱。
claims:
- 提出无监督可微分框架，同时优化几何保持、语义感知和可见性感知目标。
- 语义感知流水线通过ShDF分割、逐部分参数化和图谱聚合，产生语义对齐的UV图表。
- 可见性感知目标利用环境光遮蔽（AO）作为曝光代理，反向传播AO加权的可微缝线损失，将切割缝线导向遮挡区域。
- 在用户研究中，可见性感知方法获得91.42%的普通用户偏好，语义感知方法获得74.29%的偏好，证明感知优越性。
---

# Unsupervised Representation Learning for 3D Mesh Parameterization with Semantic and Visibility Objectives

> [!tip] 核心洞察
> 通过“分割-参数化”策略，在保留几何低畸变的基础双向循环映射架构上叠加语义与可见性约束，可在不显著牺牲保角/保面积特性的前提下，生成语义一致、视觉无缝的UV图谱。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向语义与可见性感知的三维网格无监督参数化表示学习 |
| 英文题名 | Unsupervised Representation Learning for 3D Mesh Parameterization with Semantic and Visibility Objectives |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9LYsvna4Sk) · [Project](https://ahhhz975.github.io/Automatic3DMeshParameterization/) · [Code](https://github.com/AHHHZ975/Semantic-Visibility-UV-Param) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | Semantic-Visibility-Aware UV Parameterization |
| Dataset | Visibility Metric, Semantic-Aware Metric, User Study |

> [!tip] 效果简介
> - Visibility Metric 上，Seam AO (Visibility↓) 0.6065 (Ours Vis) vs 0.8604 (FlexPara) (-0.2539)；Conformality↑ 0.9175 (Ours Vis) vs 0.9097 (FlexPara) (+0.0078)；Equiareality↑ 0.6093 (Ours Vis) vs 0.6759 (FlexPara) (-0.0666)。
> - Semantic-Aware Metric 上，Hamming Distance (AS)↓ 0.3188 (Ours Sem) vs N/A (best baseline value not provided) (N/A)；Rand Index (AR)↑ 0.8151 (Ours Sem) vs N/A (N/A)；Conformality (AU)↑ 0.9123 (Ours Sem) vs N/A (N/A)。
> - User Study (Visibility) 上，General User Preference Percentage 91.42% (Ours Vis) vs 1.43% (OptCuts) / 7.14% (FlexPara) (+84.28% vs FlexPara)。

## 概要

三维网格的UV参数化是计算机图形学中的基础问题，直接影响纹理映射、细节编辑和跨形状迁移等下游任务的质量。现有自动UV展开方法普遍以最小化几何畸变（保角性、等面积性）为核心目标，却忽视了内容创作流程中两个关键的感知标准：**语义感知性**与**可见性感知性**。前者要求UV图表与语义上有意义的3D部件对齐，否则纹理编辑和跨形状迁移将变得困难；后者要求切割缝线位于不易被观察到的遮挡区域，否则渲染后会产生明显的纹理接缝伪影。这一双重感知缺失构成了当前自动参数化方法从几何最优走向感知最优的核心瓶颈。

本文提出**Semantic-Visibility-Aware UV Parameterization**，一个无监督、可微分的统一框架，在保留几何低畸变特性的基础上，同时优化语义感知和可见性感知目标。其核心洞察在于：通过“分割-参数化”策略，在双向循环映射主干架构上叠加语义与可见性约束，可以在不显著牺牲保角/保面积特性的前提下，生成语义一致、视觉无缝的UV图谱。

具体而言，**语义感知流水线**通过形状直径函数（ShDF）结合高斯混合模型与图割，将网格分割为语义3D部件，随后对每个部件独立训练UV参数化，最后通过网格相似变换将部件UV岛屿聚合为统一图谱。**可见性感知流水线**则以环境光遮蔽（AO）作为可见性代理，设计可微的AO加权接缝损失，利用log-sum-exp近似和sigmoid软成员函数实现端到端的梯度反向传播，将切割缝线引导至低可见性区域。

实验表明，该方法在感知指标上取得显著优势：可见性感知方法在用户研究中获得**91.42%**的普通用户偏好，语义感知方法获得**74.29%**的偏好，均大幅领先基线方法（如FlexPara仅7.14%）。同时，语义感知流水线在保角性上甚至略有提升（0.9123），可见性感知流水线虽在等面积性上有所折损（0.6093 vs 基线0.6759），但通过组合流水线（0.6369）可取得良好权衡。该方法为感知驱动的自动UV参数化开辟了新方向，但语义流水线的推理耗时（约15秒）和可见性流水线的训练开销（接缝检测占90%训练时间）仍是实际部署中需要优化的问题。



三维网格参数化（UV映射）是计算机图形学与几何处理中的基础任务，其目标是将3D表面映射到2D纹理域，从而支持纹理绘制、重光照、细节迁移等下游应用。一个理想的UV映射需要同时满足多重目标：**几何保持**（低角度畸变与低面积畸变）、**语义一致性**（UV图表与3D语义部件对齐）以及**视觉无缝性**（切割缝线位于不可见或低可见性区域）。

然而，现有自动UV参数化方法普遍忽视了两个对内容创作至关重要的感知标准。

**语义感知缺口**：传统方法（如工业库**xatlas** (jpcy, 2025) 或商业工具**Blender/Autodesk Maya**）以及近期的学习型方法（如**FlexPara** (Zhao et al., 2025)）主要优化几何畸变目标，其生成的UV图表通常不与语义上有意义的3D部分对齐。这导致纹理编辑困难——艺术家难以在2D纹理图中定位特定语义部件（如角色的头部或手臂），跨形状的纹理迁移也变得不可行。**OptCuts** (Li et al., 2018) 虽然联合优化了切割与参数化，但同样缺乏语义感知机制。

**可见性感知缺口**：现有方法的切割缝线往往位于3D模型的高可见性区域（如正面或特征突出部位），在渲染后产生明显的纹理接缝伪影。这一问题在游戏资产和影视级内容中尤为突出，因为任何可见的接缝都会破坏视觉沉浸感。无论是经典的几何驱动方法还是现代的神经参数化方法，均未将可见性作为优化目标。

上述两个缺口源于一个共同的瓶颈：**现有框架缺乏将语义理解与可见性感知融入UV参数化优化的可微机制**。具体而言：（1）缺少将3D语义分割与逐部件参数化结合、并能端到端聚合为统一图谱的流水线；（2）缺少可微的接缝检测与可见性引导损失，使得切割缝线的位置无法通过梯度优化推向遮挡区域。

针对这些缺口，本文提出**Semantic-Visibility-Aware UV Parameterization**——一个无监督、可微分的框架，在保留几何低畸变特性的基础上，联合优化语义感知和可见性感知目标。核心思路是通过“分割-参数化”策略叠加感知约束：语义感知流水线利用形状直径函数（ShDF）进行3D语义分割，对每个语义部件独立训练UV映射后聚合为统一图谱；可见性感知流水线则采用环境光遮蔽（AO）作为可见性代理，设计可微的AO加权缝线损失，将切割缝线引导至遮挡/低可见性区域。两个模块可独立使用或组合部署，在不显著牺牲保角性与等面积性的前提下，生成语义一致、视觉无缝的UV图谱。



## 核心方法与创新机理

本文的核心创新在于将**语义感知**与**可见性感知**两个内容创作中的关键需求，首次形式化为可微目标函数，并嵌入到无监督几何保持UV参数化框架中。这一设计在不显著牺牲保角性与等面积性的前提下，解决了现有方法“接缝显眼”与“UV图表无语义”两大瓶颈。

### 创新点一：语义感知的“分割-参数化”流水线

现有自动UV方法仅最小化几何畸变，导致UV图表边界与3D语义部件错位，纹理编辑和跨形状迁移困难。本文提出**语义感知UV参数化**，其核心机制为：

1. **语义3D分割**：利用形状直径函数（ShDF）结合高斯混合模型（GMM）与图割，将输入网格 $ \mathcal{M} = (V, \boldsymbol{F}) $ 映射为逐顶点语义标签 $ S: V \to \{1, \dots, K\} $。
2. **逐部件参数化**：对每个语义部件 $ V_k $ 独立训练基础UV映射主干，最小化几何畸变损失：
   $$
   \mathcal{L}_{\mathrm{part}}^{(k)}(\theta_k) = \mathcal{L}_{\mathrm{wrap}}^{(k)} + \mathcal{L}_{\mathrm{cycle}}^{(k)} + \mathcal{L}_{\mathrm{repel}}^{(k)} + \mathcal{L}_{\mathrm{dist}}^{(k)} \tag{1}
   $$
3. **图谱聚合与打包**：通过网格相似变换将各部件UV岛屿放置到统一图谱中：
   $$
   T_k(u) = s \cdot u + t_{r_k,c_k}, \quad s = \frac{1 - 2 \cdot \mathrm{pad}}{G} \tag{2}
   $$
   $$
   u_{\mathrm{final}}(v) = T_k(u_{\theta_k}(v)), \quad v \in V_k \tag{3}
   $$

这一流水线使UV图表边界自然对齐到语义部件边界，显著提升纹理编辑的便利性。消融实验表明，相较于**FlexPara**（Zhao et al., 2025）的基础几何保持主干，语义感知流水线在保角性上略有提升（0.9123 vs 0.9097），等面积性几乎持平（0.6707 vs 0.6759），同时获得了语义对齐能力（Table 7）。

### 创新点二：可见性感知的可微接缝损失

传统方法的切割缝线常落在模型的高曝光区域，渲染后产生刺眼的纹理接缝。本文提出**可见性感知UV参数化**，将接缝引导至遮挡/低可见性区域，其关键设计包括：

1. **环境光遮蔽（AO）作为可见性代理**：逐顶点计算半球余弦加权可见性积分：
   $$
   AO(p) = \frac{1}{\pi} \int_{\Omega^{+}(p)} V(p, \omega) \, (n(p) \cdot \omega) \, \mathrm{d}\omega \tag{4}
   $$
   AO值越低，表示该顶点越隐蔽。

2. **可微软接缝检测**：通过log-sum-exp近似最大UV距离，结合sigmoid函数生成可微的软接缝成员分数：
   $$
   \eta_i \approx \frac{1}{\gamma} \log\Big(\sum_{j \in N_i^N} \exp\big(\gamma \| q_i - q_{i,j} \|_2 \big)\Big), \qquad s_i = \sigma\big(\beta(\eta_i - \tau)\big) \tag{6}
   $$

3. **AO加权接缝损失**：以软接缝分数为权重，最小化接缝顶点的平均AO值：
   $$
   \mathcal{L}_{\mathrm{AO}} = \frac{\sum_i s_i AO_i}{\sum_i s_i + \varepsilon} \tag{7}
   $$
   完整的可见性感知目标为：
   $$
   \mathcal{L}_{\mathrm{vis}}(\theta) = \mathcal{L}_{\mathrm{wrap}} + \mathcal{L}_{\mathrm{cycle}} + \mathcal{L}_{\mathrm{repel}} + \mathcal{L}_{\mathrm{dist}} + \lambda_{\mathrm{vis}} \mathcal{L}_{\mathrm{AO}} \tag{8}
   $$

这一机制使接缝从高曝光区域“迁移”到模型内侧、缝隙等天然隐蔽处。定量结果显示，可见性感知方法将接缝AO从FlexPara的0.8604降至0.6065（Table 1），降幅达29.5%；用户研究中，91.42%的普通用户偏好本方法的接缝隐蔽效果（Table 10）。

### 创新点三：端到端可微的统一框架

两个感知模块共享同一基础双向循环映射主干（DeformNet、WrapNet、CutNet、UnwrapNet），整个框架**无需标注数据**即可端到端训练。语义感知与可见性感知可独立或联合使用，联合流水线在保角性（0.9175）、等面积性（0.6369）与接缝AO（0.6065）之间取得实用权衡（Table 7），验证了多目标协同优化的可行性。

### 与基线方法的本质差异

| 维度 | **FlexPara** (Zhao et al., 2025) | **OptCuts** (Li et al., 2018) | **本文方法** |
|------|------|------|------|
| 语义对齐 | 无 | 无 | ShDF分割+逐部件参数化+图谱聚合 |
| 接缝引导 | 无可见性意识 | 仅优化切割代价 | 可微AO加权接缝损失 |
| 可微性 | 端到端可微 | 非完全可微 | 全流程端到端可微 |
| 训练监督 | 无监督（仅几何损失） | 联合优化 | 无监督（几何+感知损失） |

综上，本文的核心创新并非提出全新的参数化算法，而是在成熟的几何保持主干上**叠加语义与可见性两个感知约束**，通过可微形式化使其与几何目标协同优化，从而在不牺牲数学质量的前提下，大幅提升UV参数化在内容创作场景中的实用价值。



本文提出一个无监督、可微分的三维网格UV参数化框架，在保持几何低畸变的基础上，联合优化语义感知与可见性感知目标。整体架构由**基础几何保持双向循环映射主干**和两个任务导向的感知模块构成：**语义感知流水线**和**可见性感知流水线**。两套流水线共享同一个预训练的基础主干，但在训练和推理阶段叠加不同的约束与计算流程。

### 基础主干：双向循环映射

基础主干采用**FlexPara**（Zhao et al., 2025）的神经表面参数化架构，由四个几何可解释的子网络组成：
- **DeformNet**：将输入网格变形到二维域；
- **WrapNet**：将变形后的二维坐标包裹回三维表面；
- **CutNet**：预测切割边以展开网格；
- **UnwrapNet**：将切割后的网格展平到UV空间。

该主干通过包裹损失、循环一致性损失、防重叠损失和畸变损失联合训练，实现从三维网格到二维UV图谱的双向映射，并保持保角性与等面积性。

### 语义感知流水线

语义感知流水线采用“**分割-参数化-聚合**”三阶段策略（图2）：

1. **三维语义分割**：利用形状直径函数（ShDF）结合高斯混合模型（GMM）和图割，将输入网格 $ \mathcal{M} = (V, \boldsymbol{F}) $ 分割为 $K$ 个语义上有意义的部件，得到逐顶点语义标签映射 $ S: V \to \{1, \dots, K\} $。
2. **逐部件参数化**：对每个语义部件 $V_k$ 独立训练一个基础主干实例，最小化部件级损失：
   $$ \mathcal{L}_{\mathrm{part}}^{(k)}(\theta_k) = \mathcal{L}_{\mathrm{wrap}}^{(k)} + \mathcal{L}_{\mathrm{cycle}}^{(k)} + \mathcal{L}_{\mathrm{repel}}^{(k)} + \mathcal{L}_{\mathrm{dist}}^{(k)} $$
3. **图谱聚合与打包**：将各部件归一化后的UV岛屿通过网格相似变换放置到统一UV图谱中：
   $$ T_k(u) = s \cdot u + t_{r_k, c_k}, \quad s = \frac{1 - 2 \cdot \mathrm{pad}}{G} $$
   $$ u_{\mathrm{final}}(v) = T_k(u_{\theta_k}(v)), \quad v \in V_k $$
   该网格聚合器简单、确定且便于逐部件纹理编辑与跨形状迁移，同时可替换为更高级的商业打包算法。

### 可见性感知流水线

可见性感知流水线在基础主干的训练过程中引入可微的**环境光遮蔽（AO）加权接缝损失**，将切割缝线引导至遮挡或低可见性区域（算法1）：

1. **逐顶点AO计算**：为每个顶点计算环境光遮蔽值作为可见性代理：
   $$ AO(p) = \frac{1}{\pi} \int_{\Omega^{+}(p)} V(p, \omega) \, (n(p) \cdot \omega) \, \mathrm{d}\omega $$
   AO值范围 $[0,1]$，1表示完全暴露，0表示完全遮挡。

2. **可微接缝检测**：在UV空间中，通过3D邻居的最大UV距离识别接缝顶点，并利用log-sum-exp近似与sigmoid函数生成可微的软接缝成员分数：
   $$ \eta_i \approx \frac{1}{\gamma} \log \Big( \sum_{j \in N_i^N} \exp \big( \gamma \| q_i - q_{i,j} \|_2 \big) \Big), \quad s_i = \sigma \big( \beta (\eta_i - \tau) \big) $$
   其中 $\tau = \tau_{\mathrm{scale}} L(Q)$ 为相对阈值。

3. **可见性感知接缝损失**：以软接缝成员分数为权重，计算AO的加权平均，推动接缝向低AO区域移动：
   $$ \mathcal{L}_{\mathrm{AO}} = \frac{\sum_i s_i AO_i}{\sum_i s_i + \varepsilon} $$
   最终可见性感知总目标为：
   $$ \mathcal{L}_{\mathrm{vis}}(\theta) = \mathcal{L}_{\mathrm{wrap}} + \mathcal{L}_{\mathrm{cycle}} + \mathcal{L}_{\mathrm{repel}} + \mathcal{L}_{\mathrm{dist}} + \lambda_{\mathrm{vis}} \mathcal{L}_{\mathrm{AO}} $$

### 模块关系与输入输出流

两条流水线共享基础主干，但在训练和推理时独立运行：
- **语义感知流水线**：输入三维网格 → ShDF语义分割 → 逐部件独立参数化 → 网格聚合输出统一UV图谱。推理时间约15秒（含分割、多主干调用和打包），训练时间因分割为小部件而低于多图表基线。
- **可见性感知流水线**：输入三维网格 → 基础主干训练 + 逐迭代AO计算与可微接缝检测 → 输出接缝位于遮挡区域的UV图谱。推理时间与基础主干一致（约2秒），但训练时间因接缝检测开销显著增加（占总训练时间约90%）。

两套流水线可独立使用，也可组合训练以同时获得语义一致且视觉无缝的UV参数化结果。

### 补充图表

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative ablations of different UV-packing strategies. To further improve our semantic-aware UV parameterization pipeline’s output, we present alternative more advanced UV packing results (different from the one proposed in Sec. 3.3) obtained from three widely used commercial tools: (a) Autodesk Maya, (b) Blender, and (c) Houdini. The left-most column shows the 3D cow mesh segmented by PartField (Liu et al., 2025). In the Autodesk Maya result (a), each UV chart corresponding to a semantic 3D part is colored to match its counterpart on the 3D mesh. The same applies to the Blender and Houdini results. Specifically, the 3D cow is first partitioned by PartField (Liu et al., 2025) into seven...*



### 基础UV参数化主干网络

该方法构建在一个无监督、可微分的双向循环映射主干之上，由四个几何可解释的子网络构成（**DeformNet**、**WrapNet**、**CutNet**、**UnwrapNet**），负责在保持几何低畸变的前提下学习初始UV映射。该主干为后续叠加语义与可见性感知模块提供了统一的优化基础。

### 语义感知模块：分割-参数化流水线

语义感知UV参数化的核心思想是“先分割、再参数化、后聚合”，迫使UV图表与语义上有意义的3D部件对齐。流水线包含三个阶段：

1. **3D语义分割**：利用形状直径函数（ShDF）结合高斯混合模型（GMM）和图割，计算逐顶点的语义分割标签，将网格划分为 $K$ 个语义部件 $V_1, \dots, V_K$。
2. **逐部件参数化**：对每个语义部件 $k$ 独立训练基干网络，最小化几何畸变损失。第 $k$ 个部件的总损失为：

$$
\mathcal{L}_{\mathrm{part}}^{(k)}(\theta_k) = \mathcal{L}_{\mathrm{wrap}}^{(k)} + \mathcal{L}_{\mathrm{cycle}}^{(k)} + \mathcal{L}_{\mathrm{repel}}^{(k)} + \mathcal{L}_{\mathrm{dist}}^{(k)} \tag{1}
$$

其中 $\mathcal{L}_{\mathrm{wrap}}$ 为包裹损失，$\mathcal{L}_{\mathrm{cycle}}$ 为循环一致性损失，$\mathcal{L}_{\mathrm{repel}}$ 为防止UV三角形重叠的排斥损失，$\mathcal{L}_{\mathrm{dist}}$ 为保角/保面积畸变损失。

3. **图谱聚合与打包**：将各部件归一化后的UV岛通过相似变换放置到 $G \times G$ 的网格图谱中。变换定义为：

$$
T_k(u) = s \cdot u + t_{r_k,c_k}, \quad s = \frac{1 - 2 \cdot \mathrm{pad}}{G}, \quad t_{r,c} = \left[ \frac{c + \mathrm{pad}}{G}, \frac{r + \mathrm{pad}}{G} \right]^T \tag{2}
$$

最终整个网格的逐顶点UV坐标为：

$$
u_{\mathrm{final}}(v) = T_k(u_{\theta_k}(v)), \quad v \in V_k \tag{3}
$$

该网格聚合器简单、确定性高，便于逐部件纹理编辑与跨形状迁移，且可替换为更先进的商业打包算法。

### 可见性感知模块：AO加权的可微缝线损失

可见性感知模块的核心目标是将切割缝线引导至遮挡/低可见性区域，从而减少渲染后的纹理接缝伪影。该模块包含三个关键组件：

**环境光遮蔽（AO）代理**：使用逐顶点AO值作为可见性度量。AO定义为半球余弦加权可见性积分：

$$
AO(p) = \frac{1}{\pi} \int_{\Omega^{+}(p)} V(p, \omega) \, (n(p) \cdot \omega) \, \mathrm{d}\omega \tag{4}
$$

其中 $AO \in [0,1]$，1表示完全暴露，0表示完全遮挡。

**可微缝线检测**：为克服传统缝线检测不可微的问题，提出基于log-sum-exp的软最大值近似。首先对每个顶点 $i$ 计算其3D邻居在UV空间中的最大距离：

$$
\eta_i \approx \frac{1}{\gamma} \log \Big( \sum_{j \in N_i^N} \exp \big( \gamma \| q_i - q_{i,j} \|_2 \big) \Big) \tag{5}
$$

随后通过sigmoid函数生成可微的软缝线成员分数：

$$
s_i = \sigma \big( \beta (\eta_i - \tau) \big), \quad \tau = \tau_{\mathrm{scale}} \, L(Q) \tag{6}
$$

其中 $\tau$ 为相对阈值，$\beta$ 控制软硬程度，$L(Q)$ 为UV坐标的归一化尺度因子。

**AO加权缝线损失**：利用软缝线成员分数对AO值进行加权平均，构造可微损失：

$$
\mathcal{L}_{\mathrm{AO}} = \frac{\sum_i s_i \, AO_i}{\sum_i s_i + \varepsilon} \tag{7}
$$

该损失将缝线位置推向低AO区域。完整的可见性感知优化目标为：

$$
\mathcal{L}_{\mathrm{vis}}(\theta) = \mathcal{L}_{\mathrm{wrap}} + \mathcal{L}_{\mathrm{cycle}} + \mathcal{L}_{\mathrm{repel}} + \mathcal{L}_{\mathrm{dist}} + \lambda_{\mathrm{vis}} \mathcal{L}_{\mathrm{AO}} \tag{8}
$$

其中 $\lambda_{\mathrm{vis}}$ 控制可见性约束的权重。训练流程如Algorithm 1所示，在每次迭代中计算AO、检测缝线、计算 $\mathcal{L}_{\mathrm{AO}}$ 并反向传播，实现端到端的可见性感知优化。

### 模块间的协同与权衡

语义感知模块通过“分割-参数化”策略在保持几何低畸变的同时实现语义对齐；可见性感知模块通过可微缝线损失将切割线导向遮挡区域。两者可独立使用，也可联合训练。消融实验（Table 7）表明，语义感知流水线几乎不损失等面积性且略微提升保角性，而可见性感知模块在追求低接缝AO时会引入一定的等面积性下降（0.6093 vs 基础模型0.6759），组合流水线（0.6369）取得了良好权衡。

### 补充图表

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the training of the proposed semantic-aware UV parameterization method (Sec. 3.3), consisting of three stages: (i) semantic 3D partitioning, computes a per-vertex semantic partition of the input mesh using shape diameter function (Appendix A.1); (ii) geometry-preserving UV learning, applies the base UV-parameterization backbone (Sec. 3.2) independently to each semantic part to obtain per-part UV islands; and (iii) UV atlas aggregation and packing, aggregates and packs these islands into a unified UV atlas*



## 实验与关键发现

### 主结果分析

#### 可见性感知评估

表1给出了可见性感知UV参数化在多个指标上的定量对比。核心指标**Seam AO（Visibility↓）**直接衡量切割缝线所在顶点的平均环境光遮蔽值——该值越低，表示接缝越隐蔽于遮挡区域。本文可见性感知方法（Ours Vis）将Seam AO从FlexPara的0.8604大幅降至**0.6065**（降幅-0.2539），证明可微AO加权接缝损失成功将切割缝线推向了低可见性区域。

在几何保持方面，可见性感知方法的**保角性（Conformality↑）**为0.9175，略优于FlexPara的0.9097（+0.0078），表明可见性约束并未损害角度保持能力。但**等面积性（Equiareality↑）**从0.6759降至0.6093（-0.0666），这是一个可感知的退化，说明将接缝强制导向低AO区域会引入额外的面积畸变。这一权衡在消融实验中进一步得到量化分析（见下文）。

用户研究（Table 10）提供了最直接的感知证据：在可见性感知评价中，本文方法获得了**91.42%**的普通用户偏好，而OptCuts仅获1.43%，FlexPara获7.14%。这一压倒性优势（相对FlexPara提升+84.28个百分点）强有力地验证了“将接缝隐藏在不可见区域”对于视觉质量的关键作用。棋盘格纹理定性对比（Figure 5、Figure 8）直观展示了这一差异：本文方法的纹理接缝几乎不可见，而基线方法在模型显著位置产生明显的纹理不连续。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/006_Figure_5.jpg]]
*Figure 5: Checkerboard texturing using UV maps produced by our visibility-aware method, FlexPara, and OptCuts. Each row shows rendered views of different meshes textured with a checkerboard and a magnified inset of a visually important region near seams (red circles). Because our method steers seams toward occluded regions, the checkerboard pattern appears substantially more continuous from typical camera viewpoints. By contrast, baselines exhibit visible seam artifacts in the zoomed-in insets*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/016_Table_10.jpg]]
*Table 10: To evaluate semantic- and visibility-awareness of the proposed method, we conducted a user-study with 70 general participants (including graduate students with computer science and engineering backgrounds) performing 11 comparisons between textured 3D shapes and UV parameterizations produced by our method and baselines. We report the percentage of general participant preferences for each method. Our proposed method is strongly preferred by the general users over the baselines*

#### 语义感知评估

语义感知方法的定量评估（Table 3）采用了**Hamming Distance（AS↓）**和**Rand Index（AR↑）**来衡量UV图表与语义3D部件的对齐程度。本文方法（Ours Sem）取得了AS=0.3188、AR=0.8151的成绩。需要注意的是，验证分析中未提供基线方法在这些语义对齐指标上的具体数值，因此无法直接量化相对提升幅度——这一对比缺口需要读者手动查阅原文Table 3进行确认。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/008_Table_3.jpg]]
*Table 3: Quantitative comparison of the proposed semantic-aware UV parameterization method against baselines on multiple evaluation metrics*

在几何指标上，语义感知方法保持了高保角性（AU=0.9123），与基础架构FlexPara相比几乎没有退化，甚至在某些情况下略有改善。用户研究中，语义感知方法获得了**74.29%**的普通用户偏好，远超xatlas（4.28%）和FlexPara（7.14%），相对FlexPara提升+67.15个百分点。值得注意的是，专家用户对语义感知流水线的偏好略低于普通用户（80.22% vs 74.29%），这可能反映了专家对几何精度有更高要求，而语义对齐带来的编辑便利性对普通用户更具吸引力。

### 消融实验

#### 分割策略消融

Table 6对比了三种3D分割策略对最终UV质量的影响：默认的**ShDF**（Shape Diameter Function，Shapira et al., 2008）、**SAMesh**（Tang et al., 2024）和**PartField**（Liu et al., 2025）。在保角性上，ShDF达到0.9123，优于SAMesh（0.8694）和PartField（0.8999）；等面积性方面，PartField表现最佳（0.6921），ShDF居中（0.6707），SAMesh最低（0.6270）。

这一结果揭示了一个关键发现：**不同分割策略在保角性与等面积性之间不存在一致的优劣关系**。PartField在某些定性案例中提供了更准确和更紧凑的分割（Figure 13、Figure 14），但并未在所有几何指标上取得最优。验证分析明确指出，目前缺乏对不同分割方法影响UV质量的因果机制的深入理解，这构成了一个开放问题。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/023_Figure_13.jpg]]
*Figure 13: Ablation studies on the proposed partitioning strategy (ShDF vs. SAMesh vs. PartField) of simple meshes. We replace our default Shape Diameter Function (ShDF) partitioner (Shapira et al., 2008) with SAMesh (Tang et al., 2024) and PartField (Liu et al., 2025) while keeping the remainder of the partition-andparameterize pipeline identical. Qualitatively all three partitioners can produce part decompositions that align with geometric structure across simple meshes, resulting compact, low-distortion per-part UV charts. However, it seems that PartField produces more accurate and more detailed semantic segmentations than ShDF and SAMesh in some cases (e.g., the feet and the tail are correctly det...*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/024_Figure_14.jpg]]
*Figure 14: Ablation studies on the proposed partitioning strategy (ShDF vs. SAMesh vs. PartField) of complex meshes with high number of triangle faces. We replace our default Shape Diameter Function (ShDF) partitioner (Shapira et al., 2008) with SAMesh (Tang et al., 2024) and PartField (Liu et al., 2025) while keeping the remainder of the partition-and-parameterize pipeline identical. Qualitatively all partitioners produce part decompositions that align with geometric structure across complex models. However, PartField appears to produce more accurate and more compact semantic segmentations than ShDF and SAMesh in some cases. For example, PartField correctly groups the entire set of fan blades into a...*

#### 语义/可见性目标对几何指标的影响

Table 7的消融直接量化了语义感知和可见性感知模块对几何保持指标的独立与联合影响。核心发现如下：

- **语义感知流水线**：相比基础架构几乎不损失等面积性，甚至略微提升保角性。这得益于“分割-参数化”策略将复杂全局映射分解为多个局部映射，降低了每个部件的畸变难度。
- **可见性感知流水线**：等面积性下降较大（0.6093 vs 基础架构0.6759），验证了可见性约束与面积保持之间存在内在张力——强制接缝避开暴露区域会限制UV展开的自由度。
- **组合流水线（语义+可见性）**：取得良好权衡（等面积性0.6369），表明语义分割先验可以在一定程度上缓解可见性约束带来的面积畸变。

### 计算开销分析

推理时间方面，可见性感知方法与FlexPara共享相同的推理架构，推理时间几乎一致（约2秒）。语义感知流水线因需执行3D分割、多主干调用和图谱打包，推理时间增加至约15秒，但可通过多线程并行改善。

训练时间方面（Table 8、Table 9），语义感知流水线因将网格分割为多个小部件，实际训练时间反而低于FlexPara的多图表版本。可见性感知流水线则因逐迭代的AO计算和接缝检测（占总训练时间的90%），训练时间显著高于单图表基线（平均31160s vs 1285s）。验证分析指出，通过多线程或GPU加速接缝检测是可行的优化方向。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/014_Table_8.jpg]]
*Table 8: Comparison of training time between our proposed semantic-aware parameterization pipeline and FlexPara’s multi-chart parameterization (Zhao et al., 2025). Total times are shown outside the parentheses, and per-iteration times are shown inside*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/015_Table_9.jpg]]
*Table 9: Comparison of training time between our proposed visibility-aware parameterization pipeline and FlexPara’s global (single-chart) parameterization (Zhao et al., 2025). Total times are shown outside the parentheses, and per-iteration times are shown inside*

### 失败模式与局限性

1. **等面积性退化**：可见性感知模块在追求低接缝AO时，会引入不可忽略的面积畸变。组合流水线虽能缓解，但仍需在可见性与等面积性之间进行显式权衡。
2. **分割策略的不确定性**：ShDF/SAMesh/PartField在几何指标上缺乏统一的因果结论，且PartField在定性上更紧凑的分割并未稳定转化为更优的量化指标。这意味着当前“分割-参数化”流水线对分割器的选择较为敏感。
3. **图谱打包效率**：当前的网格划分聚合方案在纹理密度和空间利用率上可能不及商业打包算法（如Table 5所示），但聚合模块设计为可独立替换。
4. **训练开销瓶颈**：可见性感知流水线的接缝检测计算成本高昂，对复杂网格尤其明显，限制了其在工业级大规模资产上的直接应用。

### 补充图表

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of the proposed visibility-aware UV parameterization method against baselines on multiple evaluation metrics*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/013_Table_7.jpg]]
*Table 7: Ablation: the effect of semantic and visibility objectives on geometry-preserving metrics. Reported are mean Conformality and Equiareality (higher is better). The Semantic-Aware and the combined Visibility+Semantic-Aware pipelines lose little equiareality relative to the baseline and even show slight improvement in conformality in some cases. Intuitively, this is because the semantic-aware stage first partitions the mesh into multiple semantically meaningful subparts and so the network can better satisfy geometrypreservation while also enforcing semantic consistency. However, the visibility-aware pipeline does not partition the mesh. Instead, it steers seams to less-visible (more occluded)...*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_9LYsvna4Sk/figures/010_Table_5.jpg]]
*Table 5: Quantitative ablations of different UV-packing strategies from three widely used commercial tools: Autodesk Maya, Blender, and Houdini. We use a 3D cow mesh shown in Fig. 6 to evaluate texel density and UV-space utilization of UV parameterizations packed using different UV packing strategies from the three commercial tools. Specifically, after applying our semantic-aware UV parameterization framework, we obtain UV parameterizations for each segmented 3D part, resulting in seven UV charts. Then, instead of using our default UV packing (presented in Sec. 3.3), we apply different UV packing strategies from the three commercial tools. Lastly, for each packing strategy, we compute two UV metrics...*



## 定位与知识库关联

### 1. 核心基线对比与谱系定位

本工作建立在无监督神经UV参数化的双向循环映射主干之上，其直接基线为 **FlexPara**（Zhao et al., 2025）。FlexPara通过四个几何可解释的子网络（DeformNet、WrapNet、CutNet、UnwrapNet）实现单图表/多图表的保角保面积UV展开，但完全忽略语义一致性与可见性感知。本文的核心贡献在于该主干上叠加两个感知目标模块，形成差异化能力：

- **语义感知分支**：在FlexPara的几何保持主干前插入“分割-参数化”流水线，利用形状直径函数（ShDF）结合GMM与图割进行3D语义分割，随后对每个语义部件独立训练UV映射，最后通过网格相似变换聚合为统一UV图谱。这一策略与FlexPara的多图表参数化形成鲜明对比——后者按几何畸变最小化原则自动生成图表边界，而非语义边界。
- **可见性感知分支**：在FlexPara的单图表主干上附加可微的AO加权接缝损失，通过log-sum-exp近似与sigmoid软成员函数实现端到端的接缝位置优化，将切割缝线引导至遮挡/低可见性区域。这是FlexPara完全不具备的能力。

在更广泛的方法谱系中，本文与以下工作构成对比或互补关系：

- **OptCuts**（Li et al., 2018）：经典联合优化切割与参数化的方法，在用户研究中作为可见性感知的基线。OptCuts仅优化几何目标，未考虑可见性，因此在接缝AO指标上显著劣于本文方法（用户偏好仅1.43% vs 本文91.42%）。
- **xatlas**（jpcy, 2025）：工业级参数化库，作为语义感知评估的基线。xatlas追求几何效率与打包密度，但缺乏语义对齐机制，用户偏好仅为4.28%（vs 本文74.29%）。
- **Blender / Autodesk Maya**（Blender Foundation, 2025; Autodesk, Inc., 2025）：商业工具内置UV展开策略，在打包密度对比（Table 5）中作为参考。本文的网格聚合方案在纹理密度和空间利用率上不及这些商业打包算法，但聚合模块可独立替换。
- **SAMesh**（Tang et al., 2024）与 **PartField**（Liu et al., 2025）：作为分割策略消融实验中的替代分割器。SAMesh是现代零样本分割方法，PartField是另一种3D语义分割方法。消融表明，默认的ShDF分割器在保角性（0.9123 vs SAMesh 0.8694 vs PartField 0.8999）和等面积性（0.6707 vs 0.6270 vs 0.6921）上取得最佳平衡，但PartField在部分定性案例中提供更紧凑的分割。

### 2. 技术谱系中的“因果旋钮”定位

本文的核心洞察在于识别并操作了两个被现有方法普遍忽视的感知关键标准：

1. **语义感知性**：现有自动UV参数化方法（包括FlexPara、OptCuts、xatlas）的图表边界由几何畸变最小化驱动，与语义部件无对应关系。这导致纹理编辑时难以按语义区域操作，跨形状纹理迁移时缺乏对应。本文通过ShDF分割与逐部分参数化，将“语义部件边界”显式地塑造为UV图表边界，从而在保留几何低畸变的前提下实现语义对齐。

2. **可见性感知性**：传统方法的切割缝线位置完全由几何展开需求决定，常落于模型的高曝光区域（如角色面部、武器刃部），渲染后产生明显的纹理接缝伪影。本文利用环境光遮蔽（AO）作为可见性代理，设计可微的AO加权缝线损失，首次将“接缝可见性”作为可优化目标引入UV参数化框架。这一因果干预直接体现在接缝AO指标上：本文方法将接缝AO从FlexPara的0.8604降至0.6065，降幅达29.5%。

### 3. 适用边界与局限

**语义感知流水线**：
- 推理时间较长（约15秒），因需执行3D分割、多主干调用和打包。可通过多线程并行改善，但当前不适合实时应用。
- 训练时间反而低于FlexPara的多图表版本（因将网格分割为许多小部件后每个子问题规模缩小），但分割质量直接影响最终UV质量——不同分割器（ShDF/SAMesh/PartField）在保角性与等面积性之间缺乏统一的因果结论。
- 图谱聚合采用简单的网格划分方案，纹理密度和空间利用率不及商业打包算法（如Maya、Blender），但该模块可独立替换为更先进的打包求解器。

**可见性感知流水线**：
- 训练时间显著增加（平均31160s vs FlexPara单图表的1285s），主要瓶颈在于逐迭代的AO计算和可微接缝检测（占总训练时间的90%），对复杂网格尤其明显。
- 在追求低接缝AO时，会引入一定的等面积性下降（0.6093 vs FlexPara 0.6759）。组合流水线（语义+可见性）可缓解至0.6369，但仍需权衡。
- 推理时间与FlexPara几乎一致（约2秒），因为可见性感知模块仅在训练时通过损失函数引导接缝位置，推理架构与FlexPara共享。

**通用局限**：
- 当前方法针对静态三角网格设计，尚未验证在非刚性形状或更大规模工业资产上的泛化能力。
- 语义感知与可见性感知联合训练时是否存在对抗性效应，以及如何动态调整权重以获得最优平衡，尚待探索。

### 4. 开放问题与未来方向

1. **分割策略的因果机制**：不同3D分割方法（ShDF/SAMesh/PartField）对最终UV质量的影响并非单调一致——保角性与等面积性的变化方向在不同分割器间存在差异。需要设计更鲁棒的评估协议或可控分割研究来揭示因果链条。

2. **端到端可微分割**：当前ShDF/GMM/图割步骤不可微，与神经主干分离。是否可以利用学习型分割或端到端可微分割来替代，可能进一步提升语义对齐和几何保真度。

3. **可微接缝检测的效率**：现有的log-sum-exp近似与逐顶点邻居搜索计算成本高昂。空间哈希、缓存查找或GPU加速可能显著降低训练开销，是将可见性感知方法推向实用的关键。

4. **感知目标的联合优化**：语义感知与可见性感知在联合训练时可能存在目标冲突（如语义边界恰好位于高可见性区域）。如何设计动态权重调度或帕累托优化策略，在不同任务间取得最优平衡，是一个值得深入的方向。

5. **跨域泛化**：该方法能否扩展到非刚性形状（如动态角色网格）或大规模工业资产（如包含数万部件的CAD模型），其泛化能力和计算可扩展性尚待验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/Unsupervised_Representation_Learning_for_3D_Mesh_Parameterization_with_Semantic_fb445667e240.pdf]]
