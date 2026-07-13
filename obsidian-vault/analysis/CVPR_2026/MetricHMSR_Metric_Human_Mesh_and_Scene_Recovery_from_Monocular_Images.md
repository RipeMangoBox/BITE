---
title: "MetricHMSR: Metric Human Mesh and Scene Recovery from Monocular Images"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MetricHMSR_Metric_Human_Mesh_and_Scene_Recovery_from_Monocular_Images.pdf
project_link: null
code_link: "https://Metaverse-AI-Lab-THU.github.com/MetricHMSR"
aliases:
- MetricHMSR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 提出边界相机光线图（bounding camera ray map）将相机内参、边界框信息统一编码为像素对齐的显式度量线索；设计HumanMoE动态路由图像特征，实现局部姿态与全局度量位置的特征级解耦；以重建的度量人体作为几何锚点，引导单目深度精修，实现人-景度量一致重建。
primary_logic: (1) 相机内参与边界框隐含人体三维全局位置线索，显式提供可缓解尺度歧义；(2) 特征解耦有利于同一架构同时学习局部姿态、度量形状和全局位置；(3) 度量人体可作为强几何先验，显著提升单目深度估计的精度与物理一致性。
claims:
- MetricHMSR在人体网格恢复和单目深度估计两个子任务上均达到最优（online methods中最佳）。
- 边界光线图将全局位置误差W-MPJPE从191.8降至154.1（↓37.7），证明像素级光线表示对度量位置估计的关键作用。
- HumanMoE在+Ray基础上进一步降低PA-MPJPE（33.6 vs 34.4）和MPJPE（53.0 vs 55.0），验证特征解耦的有效性。
- 人引导深度精修在PROX上取得0.13 AbsRel、0.46 MAE、0.91 δ1，优于无精修基线。
---

# MetricHMSR: Metric Human Mesh and Scene Recovery from Monocular Images

> [!tip] 核心洞察
> (1) 相机内参与边界框隐含人体三维全局位置线索，显式提供可缓解尺度歧义；(2) 特征解耦有利于同一架构同时学习局部姿态、度量形状和全局位置；(3) 度量人体可作为强几何先验，显著提升单目深度估计的精度与物理一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MetricHMSR：从单目图像进行度量级人体网格与场景恢复 |
| 英文题名 | MetricHMSR: Metric Human Mesh and Scene Recovery from Monocular Images |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Song_MetricHMSR_Metric_Human_Mesh_and_Scene_Recovery_from_Monocular_Images_CVPR_2026_paper.html) · [Code](https://Metaverse-AI-Lab-THU.github.com/MetricHMSR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | MetricHMSR |
| Dataset | 3DPW / EMDB（混合） |

> [!tip] 效果简介
> - 3DPW / EMDB（混合） 上，PA-MPJPE / MPJPE / PVE / WA-MPJPE / W-MPJPE (mm) 34.4 / 55.0 / 64.9 / 56.4 / 154.1 (+Ray) vs 35.6 / 57.2 / 66.8 / 64.5 / 191.8 (仅图像) (↓1.2 / ↓2.2 / ↓1.9 / ↓8.1 / ↓37.7)；PA-MPJPE / MPJPE / PVE / WA-MPJPE / W-MPJPE (mm) 33.6 / 53.0 / 62.7 / 55.6 / 152.5 (+Ray&MoE) vs 34.4 / 55.0 / 64.9 / 56.4 / 154.1 (+Ray) (↓0.8 / ↓2.0 / ↓2.2 / ↓0.8 / ↓1.6)。

## 概要

从单目图像恢复度量尺度的人体网格与场景几何，是三维视觉中长期悬置的瓶颈问题。现有方法——从早期端到端基线 **HMR** (Kanazawa et al., CVPR 2018) 的弱透视假设，到 **CLIFF** (Li et al., ECCV 2022) 引入全帧位置信息的全透视模型，再到 **TRAM** (Wang et al., ECCV 2024)、**WHAM** (Shin et al., CVPR 2024)、**GVHMR** (Shen et al., SIGGRAPH Asia 2024) 等世界坐标系运动重建方法——始终面临三个根本性困难：**尺度模糊性**（单目线索无法唯一确定深度）、**特征耦合**（局部姿态与全局位置信息在特征空间中高度混叠）、以及**多阶段累积误差**（依赖外部深度估计器限制性能上限）。

本文提出 **MetricHMSR**，一个统一的度量级人体网格与场景恢复框架。其核心洞察在于三点：(1) 相机内参与边界框信息隐含了人体三维全局位置的强线索，将其显式编码为像素对齐的度量表示，可有效缓解尺度歧义；(2) 通过动态专家路由实现局部姿态与全局度量位置的特征级解耦，使同一架构能同时学习两类性质迥异的输出；(3) 重建得到的度量人体可作为强几何先验，引导单目深度估计进行物理一致的精修。

方法层面，MetricHMSR 做出三项关键设计（详见 Figure 2 整体流程）：

- **边界相机光线图**（bounding camera ray map）：将相机内参、图像裁剪和缩放信息统一编码为像素对齐的光线方向图，为每个图像块提供显式的度量线索。该表示将全局位置误差 W-MPJPE 从 191.8 mm 降至 154.1 mm（↓37.7），是度量位置估计的关键因果杠杆。
- **HumanMoE 混合专家架构**：包含 Patch MoE 和 Global MoE 两层动态路由，将图像特征解耦为局部姿态相关与全局度量相关的表征。在光线图基础上进一步降低 PA-MPJPE（33.6 vs 34.4）和 MPJPE（53.0 vs 55.0），验证了特征解耦的有效性。
- **人引导度量深度精修**：以重建的度量人体网格为几何锚点，预测逐像素仿射场（尺度+偏移）修正单目深度，在 PROX 数据集上取得 0.13 AbsRel 和 0.91 δ1 的深度估计精度。

实验表明，MetricHMSR 在人体网格恢复和单目深度估计两个子任务上均达到同期最优水平（online methods 中最佳，Table 3–5）。消融实验系统验证了光线图表示、HumanMoE 解耦设计以及过完备损失各组件对度量精度的贡献（Table 6）。

在方法谱系中，MetricHMSR 位于**单目前馈式度量人体-场景联合重建**这一新兴方向，与 **MapAnything** (Keetha et al., arXiv 2025) 等前馈场景重建方法形成互补——后者提供初始单目深度，前者以度量人体为锚点进行精修。其 HumanMoE 的特征解耦范式也为通用视觉任务中的多属性学习提供了可迁移的设计思路。

**当前局限**包括：主要验证于单人、有限遮挡场景；相机内参未知时依赖 AnyCalib 估计，误差会传播至度量重建；深度精修模块在无真值监督的野外图像上的泛化性尚待验证。

从单目图像中恢复三维人体网格与场景几何是计算机视觉的核心问题，在虚拟现实、增强现实、人机交互等领域具有广泛应用。近年来，基于参数化人体模型（如SMPL）的端到端方法取得了显著进展，**HMR**（Kanazawa et al., CVPR 2018）率先实现了从单张图像直接回归人体姿态与形状。然而，这一领域仍面临三个关键瓶颈。

**尺度模糊性与相机模型局限。** 单目三维重建本质上是一个病态问题——从二维投影推断三维结构存在固有的尺度歧义。早期方法多采用弱透视投影假设，将相机模型简化为缩放与平移，无法恢复真实的度量尺度。**CLIFF**（Li et al., ECCV 2022）引入全帧位置信息与全透视投影，但仍需已知相机内参，且边界框信息未被充分利用。**TRAM**（Wang et al., ECCV 2024）尝试结合度量深度估计，但依赖外部深度估计器限制了性能上限。**WHAM**（Shin et al., CVPR 2024）与**GVHMR**（Shen et al., SIGGRAPH Asia 2024）虽在全局运动估计上取得进展，但度量尺度恢复仍不理想。

**特征耦合与累积误差。** 现有方法将局部人体姿态（关节角度）与全局度量位置（根节点平移）的特征高度耦合在同一表示中，导致网络难以同时优化这两个性质迥异的子任务。多阶段策略虽尝试解耦，但引入了累积误差，使得整体精度受限于最薄弱环节。

**人-景度量不一致。** 单目深度估计方法（如DepthAnythingV2）虽能提供相对深度，但缺乏度量尺度，与恢复的人体网格之间存在物理一致性鸿沟。直接使用全局缩放因子对齐无法处理局部几何差异，导致人-景重建结果在空间上不协调。

针对上述问题，MetricHMSR提出了三个核心洞察：（1）相机内参与边界框隐含人体三维全局位置线索，将其显式编码为像素对齐的度量信号可有效缓解尺度歧义；（2）通过动态路由机制实现局部姿态与全局位置的特征级解耦，使同一架构能同时学习这两类信息；（3）恢复的度量人体网格可作为强几何先验，引导单目深度估计实现物理一致的人-景重建。

## 核心方法与创新机理

MetricHMSR 的核心创新围绕三个相互协同的 **changed slots** 展开，分别解决单目度量人体恢复中的尺度模糊性、特征耦合和深度不一致三大瓶颈。

### 创新一：边界相机光线图——显式度量线索的像素对齐编码

传统方法（如 **HMR** (Kanazawa et al., CVPR 2018) 的弱透视投影、**CLIFF** (Li et al., ECCV 2022) 的全透视模型）将相机内参与边界框信息作为全局标量或隐式条件处理，未能充分利用裁剪操作中蕴含的三维几何约束。MetricHMSR 提出 **边界相机光线图**（bounding camera ray map），将相机内参、图像裁剪和缩放统一编码为与输入图像像素对齐的三通道光线方向图。

具体而言，对于像素 $(u, v)$，其相机光线方向为 $d = K^{-1} [u, v, 1]$；经过裁剪与缩放后，等效内参矩阵变为：

$$K' = \begin{bmatrix} f_x/s & 0 & (c_x - u_{bbox})/s \\ 0 & f_y/s & (c_y - v_{bbox})/s \\ 0 & 0 & 1 \end{bmatrix}$$

该表示将“人体边界框在图像中的位置和尺度”与“相机投影几何”耦合为逐像素的显式三维方向线索，使网络能够直接从局部图像块推断其在相机坐标系中的绝对方向，从而缓解尺度模糊性。消融实验（Table 6）证实，仅添加光线图即可将全局位置误差 **W-MPJPE 从 191.8 mm 降至 154.1 mm（↓37.7）**，WA-MPJPE 从 64.5 降至 56.4（↓8.1），证明像素级光线表示对度量位置估计的关键作用。

### 创新二：HumanMoE——局部姿态与全局位置的特征级解耦

现有方法中，图像特征经通用 Transformer 或 MLP 处理后高度耦合，局部人体姿态信息与全局度量位置信息相互干扰，限制了同一架构同时优化两类目标的能力。MetricHMSR 设计 **HumanMoE**，基于混合专家（Mixture-of-Experts）结构实现特征级解耦。

HumanMoE 由 **Patch MoE** 和 **Global MoE** 两级组成。Patch MoE 对每个图像块 token 动态路由至 4 个可路由图像专家和 1 个共享图像专家，其中专设 **光线专家**（ray expert）学习来自相机光线图的特征；Global MoE 则聚合全局图像表示，捕获度量属性上下文。MoE 层输出为：

$$\mathrm{MoE}(\boldsymbol{x}) = \sum_{i=0}^{K} g_i(\boldsymbol{x}) e_i(\boldsymbol{x})$$

并辅以软负载均衡损失 $\mathcal{L}_{\mathrm{aux}} = \lambda K \sum_{i=1}^{K} p_i^2$ 鼓励专家使用均匀化。路由热力图（Figure 5）可视化显示，不同专家确实关注人体不同部位——部分专家聚焦躯干和近端肢体（与全局位置相关），另一部分专家关注远端关节细节（与局部姿态相关），验证了解耦的有效性。

在 +Ray 基础上引入 HumanMoE 后，**PA-MPJPE 进一步从 34.4 降至 33.6 mm，MPJPE 从 55.0 降至 53.0 mm**（Table 6），且完整 HumanMoE（Patch + Global）优于仅使用单一模块的变体，表明局部与全局信息的互补性。

### 创新三：人引导度量深度精修——以人体为几何锚点的物理一致重建

单目深度估计方法（如 DepthAnythingV2）缺乏度量尺度，直接全局缩放无法保证人-景几何一致性。MetricHMSR 以重建的度量人体网格作为强几何先验，设计 **人引导度量深度精修模块**。

该模块以度量人体渲染深度为参考，预测逐像素的仿射校正场：

$$\hat{z}(x) = s(x) z_{\mathrm{in}}(x) + b(x)$$

其中 $s(x)$ 和 $b(x)$ 分别为尺度因子和偏移量。训练时联合深度回归损失、锚点一致性损失（强制人体区域深度与网格渲染深度一致）、全变分正则化和方差正则化：

$$\mathcal{L} = \lambda_{d} \mathcal{L}_{\mathrm{depth}} + \lambda_{a} \mathcal{L}_{\mathrm{anchor}} + \lambda_{\mathrm{tv}} \mathcal{L}_{\mathrm{tv}} + \lambda_{\mathrm{var}} \mathcal{L}_{\mathrm{var}}$$

在 PROX 数据集上，该模块取得 **AbsRel 0.13、MAE 0.46、δ1 0.91**（Table 5），显著优于无精修基线。这证明度量人体可作为有效的几何锚点，将单目深度从“相对排序”提升至“度量一致”，实现人-景物理一致重建。

### 创新协同机制

三个创新形成因果闭环：**光线图**提供像素级度量线索，使网络具备恢复绝对三维位置的能力；**HumanMoE** 通过特征解耦，使同一骨干能同时学习局部姿态和全局位置，避免信息混叠；**深度精修**则以重建的度量人体为锚点，将场景深度拉至与人一致的度量空间。三者共同突破了“单目图像→度量人-景重建”的核心瓶颈。

MetricHMSR 构建了一个端到端的统一框架，从单张 RGB 图像联合恢复**度量级人体网格**与**场景几何**。其核心设计遵循一条清晰的信息流：**显式度量线索注入 → 特征解耦人体重建 → 人体引导深度精修**，三者级联形成从图像到度量一致人-景重建的完整链路。

### 输入与编码

框架接收两个并行输入（Figure 2）：

![[assets/figures/papers/paper_list_l1029_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MetricHMSR_Metric/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MetricHMSR. Given a single image, the framework jointly recovers the metric human mesh and the scene. The cropped image and the corresponding bounding ray map are encoded into tokens and processed by HumanMoE, which consists of a Patch MoE and a Global MoE to capture patch-level and image-level representations. The output heads predict the SMPL pose, shape, and global position. The recovered metric human mesh is then used to refine the depth predicted by MapAnything, producing geometrically consistent metric depth and enabling accurate human–scene reconstruction. ⊕ denotes concatenation*

1. **裁剪人体图像**：由检测框裁剪并缩放后的 RGB 图像，经 **ViTPose** 编码为图像 token 序列。
2. **边界相机光线图**（bounding camera ray map）：将相机内参、裁剪与缩放变换统一编码为像素对齐的三通道光线方向图。该光线图由 **ViT-Large-Patch16-224** 独立编码为光线 token 序列。

两路 token 经拼接（⊕）融合后，送入核心解码网络 HumanMoE。

### HumanMoE：特征解耦重建

HumanMoE 是框架的**核心推理模块**，基于混合专家（Mixture-of-Experts）架构设计，旨在解决传统方法中局部人体姿态与全局度量位置特征高度耦合的问题。它由两级 MoE 组成：

- **Patch MoE**：对每个图像块 token 进行动态专家路由，捕获**局部**人体姿态与形状的细粒度特征。
- **Global MoE**：聚合全局图像表示，捕获**全局**度量位置与场景上下文的宏观特征。

其中，MoE 层（Figure 4）设计了 1 个**光线专家**（专门学习来自相机光线的度量线索）、4 个**可路由图像专家**（处理分化的图像知识）和 1 个**共享图像专家**（捕获通用图像特征）。路由门控网络动态决定每个 token 流向哪些专家，实现局部-全局特征的**显式解耦**。

MoE 层的输出经 MLP 头部分别回归 SMPL 模型参数——姿态 $\theta \in \mathbb{R}^{72}$、形状 $\beta \in \mathbb{R}^{10}$，以及**度量全局平移** $t_{\text{global}}$，从而直接输出度量尺度的人体网格。

### 人体引导度量深度精修

获得度量人体网格后，框架将其作为**强几何先验**，引导单目深度估计的精修（Figure 6）。具体而言，以预训练单目深度估计器（如 MapAnything）的初始深度作为输入，利用重建人体网格提供可靠的度量锚点，预测一个**逐像素仿射场**——尺度 $s(x)$ 和偏移 $b(x)$——对初始深度进行校正：

$$\hat{z}(x) = s(x) z_{\text{in}}(x) + b(x)$$

该模块通过锚点一致性损失等约束，确保精修后的人体深度与场景深度在物理上一致，最终输出度量级场景深度图，实现人-景几何的度量一致重建。

### 信息流总结

```
裁剪图像 ──→ ViTPose ──→ 图像 tokens ──┐
                                        ├──→ HumanMoE (Patch + Global) ──→ SMPL θ, β, t_global ──→ 度量人体网格
光线图   ──→ ViT-L ──→ 光线 tokens ──┘                                         │
                                                                              ▼
                                                              人体引导仿射场精修 ──→ 度量场景深度
```

这一流水线的核心优势在于：光线图在输入端显式提供度量线索，HumanMoE 在特征层解耦局部与全局信息，人体网格在输出端充当场景深度精修的几何锚点——三个环节协同，使得单目图像到度量人-景重建的整个通路既保持端到端可训练，又具备物理一致性。

### 3.1 边界相机光线图（Bounding Camera Ray Map）

**设计动机**：现有方法（如 **HMR**（Kanazawa et al., CVPR 2018）的弱透视投影、**CLIFF**（Li et al., ECCV 2022）的全透视假设）均未将相机内参与边界框信息统一编码为像素对齐的显式度量线索，导致全局位置估计存在严重尺度模糊性。

**核心公式**：对于图像中像素 $(u, v)$，其对应的相机光线方向为：

$$d = K^{-1} [u, v, 1]^\top \tag{1}$$

其中 $K$ 为相机内参矩阵。当图像经过裁剪和缩放变换后，等效内参矩阵更新为：

$$K' = \begin{bmatrix} f_x/s & 0 & (c_x - u_{bbox})/s \\ 0 & f_y/s & (c_y - v_{bbox})/s \\ 0 & 0 & 1 \end{bmatrix} \tag{2}$$

其中 $(u_{bbox}, v_{bbox})$ 为边界框左上角坐标，$s$ 为缩放因子，$(f_x, f_y)$ 为焦距，$(c_x, c_y)$ 为主点。

**表示形式**：将每个像素的光线方向向量映射为三通道图像，形成与输入图像空间对齐的“光线图”。该表示将相机投影模型与人体边界框信息统一为像素级度量线索，显式注入网络。

**编码器**：采用 **ViT-Large-Patch16-224** 提取光线图特征，与 **ViTPose** 编码的图像特征拼接后送入后续的 HumanMoE 解码器（Figure 2）。

---

### 3.2 HumanMoE：基于混合专家的特征解耦

**设计动机**：传统 Transformer 解码器对所有图像 token 平等处理，导致局部姿态特征与全局度量位置特征高度耦合。HumanMoE 通过动态路由机制实现特征级解耦。

**MoE 层输出**：

$$\mathrm{MoE}(\boldsymbol{x}) = \sum_{i=0}^{K} g_i(\boldsymbol{x}) e_i(\boldsymbol{x}) \tag{3}$$

其中 $\boldsymbol{x}$ 为输入 token，$g_i(\boldsymbol{x})$ 为门控网络输出的第 $i$ 个专家的路由权重，$e_i(\boldsymbol{x})$ 为第 $i$ 个专家的输出，$K$ 为专家总数。

**专家设计**（Figure 4）：
- **1 个光线专家**（Ray Expert）：专门学习来自相机光线图的特征。
- **4 个路由图像专家**（Routed Image Experts）：处理特定的图像知识，由门控网络动态分配。
- **1 个共享图像专家**（Shared Image Expert）：捕获所有 token 的共性图像知识，始终激活。

**双阶段 MoE 架构**：
- **Patch MoE**：对每个图像块 token 独立路由，实现局部姿态特征的精细解耦。
- **Global MoE**：聚合全局图像表示，捕获度量属性上下文。

**负载均衡损失**：为防止门控网络坍塌到少数专家，引入软负载均衡损失：

$$\mathcal{L}_{\mathrm{aux}} = \lambda K \sum_{i=1}^{K} p_i^2 \tag{4}$$

其中 $p_i$ 为第 $i$ 个专家在批次中被选中的概率，$\lambda$ 为权重系数。

**路由可视化**（Figure 5）：最深 MoE 层的路由热力图显示，不同专家关注人体不同区域（如躯干、四肢），验证了特征解耦的实际效果。

---

### 3.3 过完备损失设计

MetricHMR 的总损失函数包含六项监督，形成“过完备”设计以提升度量形状精度：

$$\mathcal{L} = \lambda_{J_{2D}} \mathcal{L}_{J_{2D}} + \lambda_{J_{3D}} \mathcal{L}_{J_{3D}} + \lambda_{V_{3D}} \mathcal{L}_{V_{3D}} + \lambda_{\theta} \mathcal{L}_{\theta} + \lambda_{\beta} \mathcal{L}_{\beta} + \lambda_{h} \mathcal{L}_{h} \tag{5}$$

其中：
- $\mathcal{L}_{J_{2D}}$：2D 关键点重投影损失
- $\mathcal{L}_{J_{3D}}$：3D 关键点位置损失
- $\mathcal{L}_{V_{3D}}$：3D 顶点损失
- $\mathcal{L}_{\theta}$：SMPL 姿态参数 $\theta \in \mathbb{R}^{72}$ 正则化
- $\mathcal{L}_{\beta}$：SMPL 形状参数 $\beta \in \mathbb{R}^{10}$ 正则化
- $\mathcal{L}_{h}$：人体高度监督（额外辅助项）

消融实验（Table 6）表明，该过完备损失通过增加高度监督等辅助项，有效提升了度量形状精度。

---

### 3.4 人引导度量深度精修

**设计动机**：现有单目度量深度估计（MMDE）方法（如 **DepthAnythingV2**）缺乏场景级物理约束。MetricHMSR 以重建的度量人体网格作为几何锚点，对初始单目深度进行逐像素校正。

**深度仿射校正**（Figure 6）：

$$\hat{z}(x) = s(x) z_{\mathrm{in}}(x) + b(x) \tag{6}$$

其中 $z_{\mathrm{in}}(x)$ 为输入的单目深度（由 **MapAnything**（Keetha et al., arXiv 2025）提供），$s(x)$ 和 $b(x)$ 为网络预测的逐像素尺度和偏移参数，$\hat{z}(x)$ 为精修后的度量深度。

**深度精修总损失**：

$$\mathcal{L} = \lambda_{d} \mathcal{L}_{\mathrm{depth}} + \lambda_{a} \mathcal{L}_{\mathrm{anchor}} + \lambda_{\mathrm{tv}} \mathcal{L}_{\mathrm{tv}} + \lambda_{\mathrm{var}} \mathcal{L}_{\mathrm{var}} \tag{7}$$

其中：
- $\mathcal{L}_{\mathrm{depth}}$：与真值深度的回归损失
- $\mathcal{L}_{\mathrm{anchor}}$：锚点一致性损失——约束人体网格投影深度与精修深度在人体区域一致
- $\mathcal{L}_{\mathrm{tv}}$：全变分正则化，鼓励平滑的仿射场
- $\mathcal{L}_{\mathrm{var}}$：方差正则化，防止仿射参数剧烈波动

该模块在 PROX 数据集上取得 0.13 AbsRel、0.46 MAE、0.91 $\delta_1$，显著优于无精修基线（Table 5）。

## 实验与关键发现

### 核心定量结果

MetricHMSR在人体网格恢复和单目深度估计两个子任务上均取得最优性能（online方法中最佳）。在全局运动估计上，Table 3显示MetricHMSR在RICH静态相机数据集上的根平移误差（RTE）达到1.9，优于所有online和offline方法。在动态相机场景EMDB-2上，无论使用预测外参（Table 1）还是真实外参（Table 2），MetricHMSR均取得最佳或次佳的全局轨迹估计精度。

![[assets/figures/papers/paper_list_l1029_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MetricHMSR_Metric/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparisons of global motion and trajectory estimation with predicted extrinsic parameters on EMDB-2, a dynamic camera dataset*

![[assets/figures/papers/paper_list_l1029_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MetricHMSR_Metric/figures/010_Table_2.jpg]]
*Table 2: Quantitative comparisons of global motion and trajectory estimation with GT extrinsic parameters on EMDB-2, a dynamic camera dataset*

在局部姿态估计方面，Table 4显示MetricHMSR在3DPW数据集上取得PA-MPJPE 33.6、MPJPE 53.0、PVE 62.7，三个指标均为最优。在EMDB-2上同样取得PA-MPJPE 43.2、MPJPE 70.7、PVE 81.6的最佳结果。

在深度估计任务上，Table 5显示人引导深度精修模块在PROX数据集上取得AbsRel 0.13、MAE 0.46、δ1 0.91，显著优于无精修基线和其他单目深度估计方法。

### 关键消融分析

Table 6系统验证了各核心组件的贡献：

**边界相机光线图的核心作用**：在仅使用图像输入的基线（Image only）上，全局位置误差W-MPJPE为191.8。引入边界光线图（+Ray）后，W-MPJPE骤降至154.1（↓37.7），同时WA-MPJPE从64.5降至56.4（↓8.1）。这证明像素对齐的光线表示能有效编码相机内参和边界框信息，为度量位置估计提供显式几何线索。局部姿态指标PA-MPJPE也从35.6改善至34.4，表明全局位置信息的改善对局部姿态估计也有正向溢出效应。

**HumanMoE的特征解耦效果**：在+Ray基础上引入HumanMoE（+Ray & MoE），PA-MPJPE进一步从34.4降至33.6，MPJPE从55.0降至53.0，PVE从64.9降至62.7。全局指标WA-MPJPE从56.4降至55.6，W-MPJPE从154.1降至152.5。这表明通过Patch MoE和Global MoE的动态路由机制，局部姿态特征与全局度量位置特征实现了有效解耦，同一架构可同时学习两类信息而不相互干扰。

**HumanMoE设计的互补性**：仅使用Patch MoE或仅使用Global MoE均不如完整设计。仅Patch MoE时MPJPE为54.5，仅Global MoE时为54.3，而完整HumanMoE（Patch + Global）达到53.0。这验证了局部块级特征和全局图像级特征的信息互补性——前者擅长捕获人体关节细节，后者更适合编码相机视角和场景上下文。

**过完备损失设计**：通过引入高度监督等辅助项（Eq.(5)），度量形状精度得到进一步提升，但具体贡献量级在消融中未单独拆解，需手动核实。

### 失败模式与局限

1. **相机内参依赖**：当相机内参未知时，MetricHMSR需借助AnyCalib进行估计。内参估计误差会直接传播至光线图编码和后续的度量重建，导致全局位置精度下降。这一依赖在无标定相机或低质量图像的野外场景中构成瓶颈。

2. **多人及遮挡场景**：当前工作主要在单人、有限复杂度场景下验证，未对多人交互及严重遮挡情况进行系统评估。HumanMoE的路由热力图（Figure 5）显示专家分工在单人场景下清晰，但在多人交叠时可能出现路由歧义。

3. **深度精修泛化**：人引导深度精修模块在PROX数据集上使用真值深度监督训练，直接在无深度标注的野外图像上泛化的能力尚待验证。该模块将重建人体作为几何锚点，当人体重建本身存在较大误差时，锚点一致性损失可能引导深度精修向错误方向收敛。

### 图表结论要点

- **Figure 1**：MetricHMSR从单目图像联合恢复度量人体网格和场景几何，左图展示人-景度量一致重建，右图展示逐帧独立应用方法得到的全局一致3D轨迹。
- **Figure 7**：SMPL根节点在相机坐标系中的分布对比显示，MetricHMSR（绿点）的根节点分布更集中、更接近真实分布，而Human3R（蓝点）的分布更分散，验证了度量位置估计的准确性。
- **Figure 8**：PROX上的度量测量对比直观展示了MetricHMSR恢复的人体与场景物体（如椅子、桌子）之间的距离关系更接近真实尺度。
- **Table 5**：深度估计对比中，人引导精修在所有指标上均优于直接使用DepthAnythingV2或简单全局缩放，验证了度量人体作为几何先验的有效性。
- **Table 6**：消融实验完整揭示了“光线图→全局位置”、“HumanMoE→特征解耦”、“Patch+Global→信息互补”的因果链条。

![[assets/figures/papers/paper_list_l1029_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MetricHMSR_Metric/figures/013_Table_6.jpg]]
*Table 6: Ablation study of the key components of our method and additional ablation study on HumanMoE. (PA-M.: PA-MPJPE, WA-M.: WA-MPJPE, W-M.: W-MPJPE.)*

![[assets/figures/papers/paper_list_l1029_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MetricHMSR_Metric/figures/014_Table_5.jpg]]
*Table 5: Depth estimation comparison on PROX dataset*

![[assets/figures/papers/paper_list_l1029_https_openaccess_thecvf_com_content_CVPR2026_html_Song_MetricHMSR_Metric/figures/012_Figure_8.jpg]]
*Figure 8: Comparison of the metric measurement on PROX*

## 定位与知识库关联

### 1. 方法谱系：从弱透视到度量级人-景联合重建

MetricHMSR 处于单目人体网格恢复（HMR）与单目度量深度估计（MMDE）的交汇点，其演进脉络可从相机模型、特征解耦和深度先验三个维度追溯。

**相机模型的演进。** 早期端到端方法如 **HMR**（Kanazawa et al., CVPR 2018）采用弱透视投影，仅能恢复归一化的相对姿态，无法获取度量尺度的全局位置。**CLIFF**（Li et al., ECCV 2022）将全帧位置信息引入全透视模型，但需已知相机内参，且边界框信息未被充分利用。MetricHMSR 提出的**边界相机光线图**（bounding camera ray map）将相机内参、图像裁剪和缩放统一编码为像素对齐的显式度量线索，本质上是对 CLIFF 相机表示的泛化与像素化重构——从标量焦距/边界框参数升级为稠密的逐像素光线方向场。

**特征解耦的演进。** 现有方法（包括 CLIFF、**TRAM**（Wang et al., ECCV 2024）、**WHAM**（Shin et al., CVPR 2024）等）通常使用通用 Transformer 或 MLP 解码器，所有图像 token 被平等处理，导致局部人体姿态特征与全局度量位置特征高度耦合。MetricHMSR 的 **HumanMoE** 通过 Patch MoE 和 Global MoE 两级混合专家路由，首次在架构层面实现局部-全局特征解耦——Patch MoE 对图像块进行动态专家分配，Global MoE 聚合全图上下文以捕获度量属性。这一设计受 MoE 在语言模型中的负载均衡思想启发，但将其适配到人体重建的特征解耦需求。

**深度先验的演进。** 在场景重建侧，**MapAnything**（Keetha et al., arXiv 2025）作为前馈度量场景重建基线，直接输出单目深度估计。MetricHMSR 的人引导度量深度精修模块以重建的度量人体网格为几何锚点，预测逐像素仿射场（尺度+偏移）修正 MapAnything 的初始深度，将“人”从重建目标升级为深度估计的强几何先验。这种“以人体为锚”的策略在 **Human3R** 等 4D 人-景重建方法中也有类似动机，但 MetricHMSR 将其实现为端到端可训练的逐像素精修模块。

**与全局运动估计方法的关系。** **GVHMR**（Shen et al., SIGGRAPH Asia 2024）在重力视角坐标系下进行全局运动估计，侧重时序一致性；MetricHMSR 则聚焦单帧度量重建，通过逐帧独立推理即可获得全局一致的 3D 轨迹（见 Figure 1 右），在单帧在线方法中达到最优（Table 3-5）。

### 2. 适用边界与关键假设

MetricHMSR 的适用性受以下假设和边界约束：

- **单人场景假设。** 当前验证主要在单人、有限复杂度场景下完成（3DPW、EMDB、RICH、PROX），未系统评估多人交互及严重遮挡场景。HumanMoE 的路由机制在多人情况下能否正确解耦不同个体的特征，仍需验证。
- **相机内参依赖。** 当相机内参未知时，方法依赖 AnyCalib 进行估计。内参估计误差会通过光线图编码直接传播至度量重建——消融实验（Table 6）显示光线图对 W-MPJPE 贡献达 37.7mm，反向说明光线质量对性能敏感。在无标定相机或内参估计困难场景（如极端畸变、低分辨率）中，性能可能退化。
- **深度精修的监督依赖。** 人引导深度精修模块在 PROX 数据集（有真值深度监督）上训练，其向无深度标注的野外图像泛化的能力尚未充分验证。模块设计中的全变分和方差正则化（Eq.7）旨在提升平滑性，但域外场景的物理一致性保真度仍需实测。
- **预训练编码器依赖。** 方法使用 ViTPose 和 ViT-Large-Patch16-224 作为特征提取骨干，这些强预训练模型可能赋予方法一定的性能优势。当某些基线未使用同等规模预训练模型时（公平性备注），直接数值对比需谨慎解读。

### 3. 局限与开放问题

**已识别的局限：**

1. **多人与遮挡场景未验证。** 当前框架未包含多人交互建模或显式遮挡处理机制。HumanMoE 的 patch 级路由在人体重叠区域可能出现专家分配歧义。
2. **内参估计误差传播。** 对 AnyCalib 的依赖构成部署瓶颈——在移动端或实时应用中，内参估计的精度和延迟可能限制整体性能。
3. **深度精修泛化边界不明。** 精修模块在 PROX 室内场景上训练，对室外、水下、弱光照等域外场景的适应性未经验证。锚点一致性损失（Eq.7 中的 $\mathcal{L}_{\mathrm{anchor}}$）在人体网格本身存在误差时可能引入偏差。

**开放问题：**

1. **多人交互及严重遮挡场景如何处理？** HumanMoE 的解耦机制能否自然扩展到多人实例，还是需要实例级路由或注意力掩码？严重遮挡下光线图提供的度量线索是否仍然可靠？
2. **如何构建大规模互联网数据的伪真值标注管线？** 当前训练依赖 BEDLAM、3DPW 等有监督数据集。利用 MetricHMSR 自身的度量重建能力进行自训练或伪标签生成，是扩展训练数据规模的关键方向。
3. **HumanMoE 的解耦特性能否推广？** Patch MoE + Global MoE 的局部-全局解耦范式是否适用于其他视觉任务（如通用 3D 姿态估计、目标检测、场景理解）？路由热力图（Figure 5）显示专家在人体关键点区域呈现结构化激活，暗示该机制可能捕获了通用的结构感知能力。
4. **度量人体作为通用几何先验的潜力。** 人引导深度精修的成功表明，度量人体可作为强几何锚点。这一思路能否扩展到其他几何任务（如法线估计、三维重建、新视图合成）？人体先验与场景先验的联合优化框架值得探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/MetricHMSR_Metric_Human_Mesh_and_Scene_Recovery_from_Monocular_Images.pdf]]
