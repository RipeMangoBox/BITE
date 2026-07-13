---
title: "VDFE: Difference-Aware 3D Scene Editing with Non-Intrusive Video Diffusion Priors for Multi-View Consistency and Efficiency"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VDFE_Difference_Aware_3D_Scene_Editing_with_Non_Intrusive_Video_Diffusion_Priors_for_Multi_View_Consistency_and_Efficiency.pdf
project_link: null
code_link: null
aliases:
- VDFE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将多视角编辑重构为伪视频编辑，通过非侵入式预训练视频扩散先验提供时空一致性；利用解耦流差异（DFD）实现无需训练的精确定位；并采用差异感知高斯编辑（DAGE）进行选择性优化。
primary_logic: 将多视角编辑重新定义为伪视频编辑，以充分利用视频扩散模型固有的帧间一致性，同时结合最优控制引导的流编辑（FlowOCE）与解耦流差异定位，实现高保真、高效率的3D场景编辑。
claims:
- VDFE在3D编辑任务中取得最佳A-LPIPS (0.2316)、MEt3R (0.0668)及用户调研得分 (37.14%)，全面优于对比方法。
- FlowOCE+DFD在FiVE视频编辑基准上取得最佳Structure Dist. (5.32×10³) 和 PSNR (29.43)，验证了视频扩散先验的有效性。
- 消融实验表明，DAGE模块带来最显著的性能提升，缺少DAGE会导致细节丢失和非编辑区域的无意修改。
- 3D Editing (Table 1) 上 A-LPIPS↓ = 0.2316
---

# VDFE: Difference-Aware 3D Scene Editing with Non-Intrusive Video Diffusion Priors for Multi-View Consistency and Efficiency

> [!tip] 核心洞察
> 将多视角编辑重新定义为伪视频编辑，以充分利用视频扩散模型固有的帧间一致性，同时结合最优控制引导的流编辑（FlowOCE）与解耦流差异定位，实现高保真、高效率的3D场景编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | VDFE：利用非侵入式视频扩散先验实现多视角一致且高效的差异感知3D场景编辑 |
| 英文题名 | VDFE: Difference-Aware 3D Scene Editing with Non-Intrusive Video Diffusion Priors for Multi-View Consistency and Efficiency |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_VDFE_Difference-Aware_3D_Scene_Editing_with_Non-Intrusive_Video_Diffusion_Priors_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | VDFE |
| Dataset | 3D Editing, 3D Editing User Study, FiVE Video Editing |

> [!tip] 效果简介
> - 3D Editing (Table 1) 上，A-LPIPS↓ 0.2316 vs 所有对比方法中最优 (最优)；MEt3R↓ 0.0668 vs 所有对比方法中最优 (最优)。
> - 3D Editing User Study 上，User Study↑ 37.14% vs 所有对比方法中最优 (最高得票率)。
> - FiVE Video Editing (Table 2) 上，Structure Dist.×10³↓ 5.32 vs 所有对比方法中最优 (最优)。

## 概要

**瓶颈与动机** 现有3D场景编辑方法普遍依赖图像扩散模型，缺乏对时空一致性的显式建模，导致多视角编辑结果出现几何错位与语义漂移。同时，基于交叉注意力图或Lang-SAM等分割模型的编辑区域定位方式精度不足、边界模糊，进一步削弱了编辑的可控性。这些局限使得高保真、多视角一致的3D编辑难以实现。

**核心思路** VDFE将多视角编辑重新定义为**伪视频编辑**，通过非侵入式地利用预训练视频扩散先验，为3D场景编辑注入帧间一致性约束。其关键洞察在于：视频扩散模型天然具备的时空一致性可以有效弥合多视角编辑中的视角断裂问题，而无需对模型本身进行侵入式微调。

**方法定位** VDFE由三个协同模块构成：**FlowOCE**（最优控制引导的流编辑）将编辑建模为最优控制问题，通过控制项注入源数据时空特征，生成噪声无关、背景保持的编辑轨迹；**DFD**（解耦流差异）利用源与目标速度场的差异，经多步Softmax融合生成高精度流差异图，实现无需训练的细粒度语义定位；**DAGE**（差异感知高斯编辑）则基于流差异图识别核心高斯，通过参数扰动与梯度分配进行选择性优化，高效精炼3DGS模型。

**主要结果** 在3D编辑任务中，VDFE在A-LPIPS（0.2316）、MEt3R（0.0668）及用户调研得票率（37.14%）上均达到最优（Table 1），全面超越**GaussianEditor**（Chen et al., CVPR 2024）、**EditSplat**（Lee et al., CVPR 2025）、**VcEdit**（Wang et al., ECCV 2025）等基线方法。在FiVE视频编辑基准上，FlowOCE+DFD同样取得最佳Structure Dist.（5.32×10³）与PSNR（29.43），验证了视频扩散先验在编辑任务中的有效性（Table 2）。消融实验表明，DAGE模块对性能提升贡献最大，缺少DAGE会导致细节丢失及非编辑区域的无意修改（Fig. 5, Table 3）。

3D场景编辑旨在根据文本指令对预重建的3D场景进行语义修改，同时保持非编辑区域的完整性与多视角几何一致性。随着3D高斯泼溅（3D Gaussian Splatting, 3DGS）作为显式场景表示方法的成熟，围绕3DGS的编辑技术迅速发展。然而，现有方法面临两个核心瓶颈：

**时空一致性缺失。** 当前主流3D编辑方法（如**GaussianEditor** (Chen et al., CVPR 2024)、**Instruct-NeRF2NeRF** (Haque et al., ICCV 2023)、**GaussCtrl** (Wu et al., ECCV 2024)）普遍依赖2D图像扩散模型对渲染视图进行逐帧编辑，再通过迭代优化将编辑信息提升至3D。这种逐帧独立编辑的策略缺乏对多视角间时空一致性的显式建模，容易导致不同视角下的编辑结果出现纹理闪烁、几何错位等不一致现象。尽管**DGE** (Chen et al., arXiv 2024) 尝试引入几何约束，**VcEdit** (Wang et al., ECCV 2025) 探索了视图一致性机制，但这些方法本质上仍受限于图像扩散模型缺乏时序感知能力的根本缺陷。

**编辑定位粗糙。** 现有方法对编辑区域的定位主要依赖交叉注意力图或基于Lang-SAM等分割模型生成的掩码。交叉注意力图通常边界模糊、语义粒度粗糙，难以精确界定编辑范围；而分割模型受限于预定义类别，面对开放词汇的编辑指令时灵活性不足。这种粗糙的定位导致编辑操作容易溢出到非目标区域，产生背景伪影或不希望的修改。

**优化效率与精度矛盾。** 在将编辑信息回传至3DGS模型时，全局优化所有高斯或基于注意力权重修剪高斯的策略要么计算开销大，要么容易误删对场景结构重要的高斯，难以在编辑精度与优化效率之间取得平衡。

针对上述问题，VDFE提出了一种全新的解决思路：**将多视角3D编辑重构为伪视频编辑问题**，通过非侵入式地利用预训练视频扩散模型固有的帧间一致性先验，从根源上解决多视角一致性问题。同时，引入基于解耦流差异（Decoupled Flow Difference, DFD）的无需训练精确定位机制，以及差异感知高斯编辑（Difference-Aware Gaussians Editing, DAGE）的选择性优化策略，实现高保真、高效率的3D场景编辑。

## 核心方法与创新机理

VDFE的核心创新在于将3D场景多视角编辑**重新定义为伪视频编辑问题**，并以**非侵入式**方式利用预训练视频扩散先验，系统性地解决了现有方法在时空一致性与编辑可控性上的瓶颈。其创新架构由三个紧密协同的模块构成，对应三个关键的**changed slots**：

### 1. 编辑轨迹控制：从噪声注入到最优控制（FlowOCE）

**瓶颈**：现有方法（如FlowEdit）在每一步速度场计算中引入高斯噪声以增强多样性，但噪声在多步编辑中累积，导致编辑轨迹偏离原始图像，产生背景偏移和多视图不一致（Section 3.2）。

**创新**：FlowOCE将编辑过程建模为**最优控制问题**，通过设计控制项 $u_t$ 注入源数据的时空特征，生成一条**无噪声、背景保持**的编辑轨迹。其动力学方程基于FlowEdit的直接编辑轨迹：
$$
\frac{d X_t^{edit}}{dt} = V_t^{tar}(X_t^{tar}, c_{tar}) - V_t^{src}(X_t^{src}, c_{src})
$$
在此基础上，FlowOCE最小化如下损失函数以平衡编辑效果与内容保留：
$$
J[u] = \int_0^1 \frac{1}{2} ||u_t - V_t^{edit}||_2^2 dt + \frac{\gamma}{2} ||X_0^{edit} - X_1^{edit}||_2^2
$$
控制项 $u_t$ 基于源与目标条件期望的差异设计，显式抑制非目标区域的意外修改并增强多视图间的一致性（Eq. 8）。

### 2. 编辑区域定位：从交叉注意力到解耦流差异（DFD）

**瓶颈**：现有方法依赖交叉注意力图或Lang-SAM等分割模型进行编辑区域定位，精度低且边界模糊，难以实现细粒度的语义级控制（Section 3.3, Fig. 3）。

**创新**：DFD模块通过计算目标速度场 $V_t^{tar}$ 与源速度场 $V_t^{src}$ 在特征层面的**L2距离**，生成高精度的流差异图 $D_{maps}$，实现**无需训练**的细粒度语义定位：
$$
D_{maps}(i,j) = \sum_{t=1}^{M} w_t \cdot \frac{\exp(D_t(i,j))}{\sum_{k=1}^{H} \sum_{l=1}^{W} \exp(D_t(k,l))}
$$
该多步加权融合并经Softmax增强的差异图能够精确识别语义变化区域，随后通过Otsu阈值提取二值掩码 $M$，用于将源特征注入非编辑区域，减少背景伪影：
$$
\hat{X}_t^{inject} = M \cdot \hat{X}_t^{edit} + (1-M) \cdot X_1^{edit}
$$

### 3. 3DGS优化策略：从全局优化到差异感知高斯编辑（DAGE）

**瓶颈**：现有3DGS编辑方法通常全局优化所有高斯或基于注意力权重进行修剪，导致非编辑区域的无意修改、细节丢失及计算效率低下（Section 3.4）。

**创新**：DAGE通过**差异感知**的选择性优化策略，仅对编辑关键区域贡献最高的核心高斯进行精细更新。其核心机制包括：
- **参数扰动（Parameter Perturbation）**：利用流差异图 $D_{maps}$ 计算每个高斯 $\mathbf{g}_i$ 的贡献得分 $C(\mathbf{g}_i)$，筛选出核心高斯集 $\mathcal{G}^*$ 并进行扰动初始化。
- **梯度分配（Gradient Assignment）**：引入差异化梯度缩放因子 $\lambda(\mathbf{g}_i)$，对核心高斯赋予高缩放因子 $\lambda_{high}$，对非编辑区域高斯赋予低缩放因子 $\lambda_{low}$，从而在梯度更新 $\Delta \mathbf{g}_i^{grad} = \lambda(\mathbf{g}_i) \cdot \nabla \mathcal{L}(\mathbf{g}_i)$ 中保持未编辑区域的稳定状态。

消融实验证实，DAGE模块对整体性能提升贡献最大——缺少DAGE会导致非编辑区域出现扭曲和细节丢失，而完整VDFE方法实现了精确且符合文本指令的编辑（Fig. 5, Table 3）。

VDFE 的整体流水线围绕一个核心洞察构建：将多视角 3D 场景编辑重新定义为**伪视频编辑**，从而充分利用预训练视频扩散模型（Video Diffusion Models, VDMs）固有的帧间一致性先验。如图 2(a) 所示，该方法包含四个串联的功能模块，形成从场景渲染到 3D 高斯精炼的闭环：

1. **伪视频渲染（Pseudo-Video Rendering）**：从预训练的 3D Gaussian Splatting (3DGS) 模型中，沿预设相机轨迹渲染多视角图像序列，构成一段“伪视频”。该视频作为后续 FlowOCE 和 DFD 模块的输入载体，将 3D 编辑问题转化为视频编辑问题。

2. **最优控制引导的流编辑（FlowOCE）**：将编辑过程建模为最优控制问题，在 FlowEdit 定义的编辑轨迹动力学基础上，通过引入控制项 $u_t$ 注入源数据的时空特征，生成噪声无关、背景保持的编辑轨迹，输出初步编辑视频。该模块的核心作用是**抑制背景偏移并增强多视图一致性**。

3. **解耦流差异（DFD）**：从 FlowOCE 编辑过程中提取源与目标的速度场，计算其 L2 距离并经多步 Softmax 加权融合，生成高精度的流差异图 $D_{maps}$。这些差异图在特征层面定位编辑区域，无需额外训练即可实现细粒度语义定位。随后通过 Otsu 阈值化提取二值掩码 $M$，用于将源特征注入非编辑区域以减少背景伪影。

4. **差异感知高斯编辑（DAGE）**：利用 $D_{maps}$ 识别对编辑关键区域贡献最高的“核心高斯”，通过参数扰动（Parameter Perturbation）和梯度分配（Gradient Assignment）仅对这些高斯进行选择性优化，避免全局更新带来的细节丢失和非编辑区域的无意修改。

**模块间的数据流关系**：伪视频渲染为 FlowOCE 提供输入；FlowOCE 的输出编辑视频与速度场信息同时传递给 DFD；DFD 生成的流差异图 $D_{maps}$ 一方面通过掩码 $M$ 反馈至 FlowOCE 的特征注入步骤，另一方面作为 DAGE 模块识别核心高斯的依据；DAGE 最终驱动 3DGS 模型的参数更新，完成场景编辑。

**关键设计选择**：
- **非侵入式先验利用**：VDFE 不修改预训练视频扩散模型的权重，仅通过最优控制框架和特征注入机制引导其输出，保持先验的完整性与泛化能力。
- **无需训练的定位**：DFD 模块直接从速度场差异中产生定位信息，避免了基于交叉注意力图或分割模型（如 Lang-SAM）的粗糙定位缺陷，显著提升编辑区域边界的精度（见 Figure 3 的可视化对比）。
- **选择性优化策略**：DAGE 通过高斯贡献得分 $C(\mathbf{g}_i)$ 筛选核心高斯，并采用差异化的梯度缩放因子 $\lambda(\mathbf{g}_i)$，确保非编辑区域保持稳定状态，同时高效精炼目标区域。

![[assets/figures/papers/paper_list_l2272_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VDFE_Difference/figures/002_Figure_2.jpg]]
*Figure 2: VDFE Overview. (a) The overall pipeline of VDFE. Our method first renders a pseudo-video of the scene. This video is then edited using our Optimal Control Guided Flow Editing (FlowOCE) and Decoupled Flow Difference (DFD) generating flow-difference maps*

VDFE 将多视角 3D 编辑重构为伪视频编辑，通过三个核心模块协同工作：**FlowOCE**（最优控制引导的流编辑）生成噪声无关的编辑轨迹，**DFD**（解耦流差异）实现无需训练的细粒度定位，**DAGE**（差异感知高斯编辑）对 3DGS 模型进行选择性优化。以下逐一展开各模块的动机、公式与变量含义。

---

### FlowOCE：最优控制引导的流编辑

**动机**：现有 FlowEdit 方法在每步计算速度场 $V_t^{src}$ 和 $V_t^{tar}$ 时注入高斯噪声，虽提升生成多样性，但多步编辑中噪声累积导致原始图像严重偏离，破坏多视角一致性。FlowOCE 将编辑重新定义为最优控制问题，通过设计控制项 $u_t$ 注入源数据时空特征，在保持编辑能力的同时抑制背景偏移。

**基础动力学**：FlowEdit 定义从源分布到目标分布的直接编辑轨迹：

$$
\frac{d X_t^{edit}}{dt} = V_t^{tar}(X_t^{tar}, c_{tar}) - V_t^{src}(X_t^{src}, c_{src}) \tag{Eq. 5}
$$

其中 $X_t^{tar}$、$X_t^{src}$ 分别为目标和源在 Rectified Flow 时间 $t$ 的状态，$c_{tar}$、$c_{src}$ 为对应文本条件。

**最优控制建模**：FlowOCE 引入控制项 $u_t$ 修正轨迹，损失函数为：

$$
J[u] = \int_0^1 \frac{1}{2} ||u_t - V_t^{edit}||_2^2 dt + \frac{\gamma}{2} ||X_0^{edit} - X_1^{edit}||_2^2 \tag{Eq. 6}
$$

- 第一项约束控制项 $u_t$ 不偏离原始编辑方向 $V_t^{edit}$；
- 第二项约束编辑结果的起点 $X_0^{edit}$ 与终点 $X_1^{edit}$ 保持一致，抑制内容偏移；
- $\gamma$ 为平衡系数。

**控制项设计**：基于源与目标条件期望差异构造 $u_t$：

$$
u_t = \lambda \Big[ \Big( \mathbb{E}[X_0^{tar} \mid X_t^{tar}] - \mathbb{E}[X_0^{src} \mid X_t^{src}] \Big) + \Big( \mathbb{E}[X_1^{tar} \mid X_t^{tar}] - \mathbb{E}[X_1^{src} \mid X_t^{src}] \Big) \Big] \tag{Eq. 8}
$$

- $\mathbb{E}[X_0 \mid X_t]$ 表示从当前状态 $X_t$ 预测的初始状态条件期望，由预训练视频扩散模型提供；
- 通过源与目标在 $t=0$ 和 $t=1$ 两端的期望差异，$u_t$ 引导编辑轨迹在语义修改的同时保持非编辑区域的结构稳定；
- $\lambda$ 为控制强度系数。

---

### DFD：解耦流差异定位

**动机**：传统方法依赖交叉注意力图或 Lang-SAM 等分割模型定位编辑区域，精度低、边界模糊。DFD 利用 FlowOCE 计算过程中源与目标速度场的差异，在特征层面生成高精度流差异图 $D_{maps}$，无需额外训练即可实现细粒度定位。

**流差异图生成**：对 $M$ 个时间步的速度场差异进行 Softmax 增强并加权融合：

$$
D_{maps}(i,j) = \sum_{t=1}^{M} w_t \cdot \frac{\exp(D_t(i,j))}{\sum_{k=1}^{H} \sum_{l=1}^{W} \exp(D_t(k,l))} \tag{Eq. 11}
$$

- $D_t(i,j) = ||V_t^{tar}(i,j) - V_t^{src}(i,j)||_2$ 为第 $t$ 步在空间位置 $(i,j)$ 的速度场 L2 差异；
- Softmax 归一化增强高响应区域对比度；
- $w_t$ 为时间步权重，$H$、$W$ 为特征图高宽。

**特征注入**：利用 Otsu 阈值法从 $D_{maps}$ 提取二值掩码 $M$，将源特征注入非编辑区域：

$$
\hat{X}_t^{inject} = M \cdot \hat{X}_t^{edit} + (1-M) \cdot X_1^{edit} \tag{Eq. 12}
$$

- $\hat{X}_t^{edit}$ 为编辑后的中间特征；
- $X_1^{edit}$ 为源视频终态特征（$t=1$）；
- 掩码 $M$ 中编辑区域保留编辑特征，非编辑区域回注源特征，减少背景伪影。

---

### DAGE：差异感知高斯编辑

**动机**：传统 3DGS 编辑方法全局优化所有高斯或基于注意力权重修剪，效率低且易引入非编辑区域的无意修改。DAGE 利用 $D_{maps}$ 识别对编辑贡献最大的“核心高斯”，通过参数扰动和梯度分配进行选择性优化。

**高斯贡献评分**：根据高斯对 $D_{maps}$ 高响应区域的可见性与不透明度贡献计算得分：

$$
C(\mathbf{g}_i) = \sum_{p \in D_{maps}} w(\mathbf{g}_i, p) \cdot p \tag{Eq. 13}
$$

- $\mathbf{g}_i$ 为第 $i$ 个高斯；
- $p$ 为 $D_{maps}$ 中像素值；
- $w(\mathbf{g}_i, p)$ 为高斯 $\mathbf{g}_i$ 对像素 $p$ 的贡献权重，由投影不透明度和空间覆盖决定；
- 得分最高的高斯集合 $\mathcal{G}^*$ 被选为核心高斯。

**差异化梯度缩放**：仅对核心高斯施加高梯度权重，其余高斯保持低权重：

$$
\lambda(\mathbf{g}_i) = \begin{cases} \lambda_{\mathrm{high}} & \mathbf{g}_i \in \mathcal{G}^* \\ \lambda_{\mathrm{low}} & \mathbf{g}_i \notin \mathcal{G}^* \end{cases}
$$

$$
\Delta \mathbf{g}_i^{\mathrm{grad}} = \lambda(\mathbf{g}_i) \cdot \nabla \mathcal{L}(\mathbf{g}_i)
$$

- $\mathcal{L}$ 为渲染损失；
- $\lambda_{\mathrm{high}} \gg \lambda_{\mathrm{low}}$，确保编辑区域的精确修改同时保持非编辑区域稳定。

---

### 模块间数据流关系

三个模块形成闭环流水线（见 Figure 2(a)）：

1. **伪视频渲染**：从预训练 3DGS 模型渲染多视角伪视频；
2. **FlowOCE + DFD**：对伪视频执行最优控制流编辑，同步生成 $D_{maps}$ 和特征注入掩码 $M$；
3. **DAGE**：将 $D_{maps}$ 映射回 3DGS 空间，筛选核心高斯并执行差异感知优化，完成 3D 场景编辑。

## 实验与关键发现

### 3D场景编辑主实验

VDFE在3D编辑任务上全面超越现有基线方法，在语义相似度、多视图一致性和编辑效率三个维度均取得最优结果（Table 1）。具体而言，VDFE的A-LPIPS达到0.2316，MEt3R达到0.0668，均为所有对比方法中的最佳值，表明编辑后的多视图渲染结果在像素级一致性上显著优于**GaussianEditor**（Chen et al., CVPR 2024）、**DGE**（Chen et al., arXiv 2024）、**EditSplat**（Lee et al., CVPR 2025）等方法。在用户调研中，VDFE以37.14%的最高得票率获得用户偏好，进一步验证了编辑效果的主观质量优势。

![[assets/figures/papers/paper_list_l2272_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VDFE_Difference/figures/005_Table_1.jpg]]
*Table 1: 3D Editing Performance Comparisons. We compare againsst baselines across six metrics, where CLIP-sim and CLIP-dir for semantic similarity, A-LPIPS and MEt3R for evaluating multi-view consistency, and Avg. Time (iterations) for evaluating efficiency*

这些指标背后的因果链条值得关注：A-LPIPS衡量编辑前后相邻视图间的感知一致性，VDFE的低A-LPIPS直接受益于FlowOCE将多视图编辑建模为伪视频的最优控制问题，通过控制项$u_t$显式注入源数据的时空特征，抑制了跨视图的背景偏移。MEt3R则评估3D几何一致性，DAGE模块的选择性优化策略——仅对贡献最高的核心高斯进行参数扰动和梯度分配——有效防止了非编辑区域的几何形变，从而保持了场景的3D结构稳定性。

### 视频编辑基准验证

为验证FlowOCE与DFD作为视频扩散先验的有效性，作者在FiVE视频编辑基准上进行了独立评估（Table 2）。VDFE的Structure Dist.为$5.32 \times 10^3$，PSNR为29.43，均取得最优结果。Structure Dist.的低值表明编辑后的视频帧间结构保持良好，这源于DFD模块通过解耦流差异（Eq. 11）精确定位编辑区域，并利用二值掩码$M$将源特征注入非编辑区域（Eq. 12），从而减少背景伪影和结构漂移。PSNR的高值则直接反映了FlowOCE编辑轨迹的噪声无关特性——通过将编辑建模为最优控制问题（Eq. 6），避免了FlowEdit中高斯噪声累积导致的图像质量退化。

![[assets/figures/papers/paper_list_l2272_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VDFE_Difference/figures/006_Table_2.jpg]]
*Table 2: Video Editing Performance Comparisons. We compare against baselines on the FiVE benchmark. Bold indicates the best, and underline denotes the second-best. ∗ and † denote methods that require optimization and depth/segmentation maps, respectively*

### 消融实验

消融实验揭示了各模块对整体性能的贡献权重（Fig. 5, Table 3）。DAGE模块对性能提升贡献最大：缺少DAGE时，仅用视频扩散模型编辑会导致非编辑区域出现扭曲和无意修改，且在有限更新步数下会引发细节丢失。完整的VDFE框架则实现了精确且符合文本指令的编辑效果。

![[assets/figures/papers/paper_list_l2272_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VDFE_Difference/figures/007_Figure_5.jpg]]
*Figure 5: Visualization Ablation. We perform visualized ablation studies to dissect the individual contributions of the proposed VDFE framework and DAGE module*

![[assets/figures/papers/paper_list_l2272_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VDFE_Difference/figures/008_Table_3.jpg]]
*Table 3: VDFE Ablation. We evalute the contribution of modules*

DAGE的有效性源于其两阶段设计：参数扰动（Parameter Perturbation）通过扰动和剪枝操作识别对编辑区域贡献最大的核心高斯；梯度分配（Gradient Assignment）则通过差异化的梯度缩放因子$\lambda(\mathbf{g}_i)$，对核心高斯施加高缩放因子$\lambda_{\text{high}}$，对非编辑区域高斯施加低缩放因子$\lambda_{\text{low}}$，从而在优化过程中保护背景区域的稳定状态。这种选择性优化策略是VDFE在有限迭代次数下仍能保持高保真编辑的关键。

### 失败模式与局限性

尽管VDFE在定量和定性评估中表现优异，其编辑性能的上限受限于所采用的视频扩散模型能力。当目标编辑涉及视频扩散模型不擅长的语义转换时，FlowOCE生成的编辑轨迹可能无法充分表达编辑意图。此外，整体流水线涉及伪视频渲染、FlowOCE、DFD和DAGE四个模块的协同运作，系统复杂度较高，可能在实际部署中引入额外的调参负担。

![[assets/figures/papers/paper_list_l2272_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VDFE_Difference/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Comparisons. Our method provides more intense and precise editing compared to other baselines. The leftmost column shows source images, while the right columns show rendering images from edited 3DGS. In each corner of the images, we include different views of the corresponding image to compare multi-view consistency*

## 定位与知识库关联

### 与现有3D编辑方法的关系

VDFE的提出建立在3D场景编辑领域两条主要技术路线的交汇点上：**基于2D扩散先验的迭代编辑方法**与**基于3D高斯泼溅（3DGS）的可微渲染框架**。理解VDFE的创新点，需要首先厘清它与这些基线工作的本质差异。

#### 对基于2D扩散模型方法的超越

早期的3D编辑方法，如**Instruct-NeRF2NeRF**（Haque et al., ICCV 2023），采用逐帧迭代编辑策略：对场景的每个视角独立应用2D扩散模型，再通过NeRF重建融合结果。这种“编辑-重建”循环的根本缺陷在于，**2D扩散模型缺乏对多视角时空一致性的显式建模**，导致不同视角的编辑结果在几何和外观上产生冲突，重建后出现模糊、伪影或语义漂移。

后续工作尝试在3DGS框架下缓解这一问题。**GaussianEditor**（Chen et al., CVPR 2024）和**GaussCtrl**（Wu et al., ECCV 2024）分别通过2D分割掩码和深度图来约束编辑区域，但定位精度受限于分割模型的边界模糊性。**DGE**（Chen et al., arXiv 2024）引入了几何约束来增强多视图一致性，**VcEdit**（Wang et al., ECCV 2025）和**EditSplat**（Lee et al., CVPR 2025）则通过多视图融合与注意力引导优化来改进编辑质量。然而，这些方法的共同瓶颈在于：**它们仍然依赖图像扩散模型作为编辑先验，而图像扩散模型在生成过程中天然缺乏帧间一致性约束**——这是由模型架构决定的根本限制，而非工程层面的可修补缺陷。

VDFE的核心突破在于**将先验来源从图像扩散模型切换为视频扩散模型**，从而在生成过程中内置了时空一致性。这不是简单的模型替换，而是对问题本质的重新定义：将多视角编辑重构为伪视频编辑，使视频扩散模型固有的帧间一致性机制自然作用于多视角序列。

#### 对FlowEdit基线的改进

在视频编辑层面，VDFE直接建立在FlowEdit的编辑轨迹框架之上。FlowEdit定义了从源分布到目标分布的直接编辑动力学：

$$\frac{d X_t^{edit}}{dt} = V_t^{tar}(X_t^{tar}, c_{tar}) - V_t^{src}(X_t^{src}, c_{src})$$

然而，FlowEdit在每个时间步引入高斯噪声以增强生成多样性，这导致**噪声在多步编辑中累积，使编辑结果逐渐偏离原始图像**，在背景保持和多视角一致性方面表现不佳。

VDFE的FlowOCE模块将编辑重新定义为最优控制问题，通过设计控制项 $u_t$ 来抑制这一偏差：

$$u_t = \lambda \Big[ \Big( \mathbb{E}[X_0^{tar} \mid X_t^{tar}] - \mathbb{E}[X_0^{src} \mid X_t^{src}] \Big) + \Big( \mathbb{E}[X_1^{tar} \mid X_t^{tar}] - \mathbb{E}[X_1^{src} \mid X_t^{src}] \Big) \Big]$$

该控制项利用源与目标条件期望的差异来引导编辑轨迹，**在保持编辑效果的同时抑制背景偏移**，这是对FlowEdit噪声机制的因果性修正。

#### 在定位策略上的差异化

现有方法的编辑区域定位主要依赖两类策略：基于交叉注意力图的方法（如**DreamCatalyst**，Kim et al., arXiv 2024）和基于分割模型的方法（如Lang-SAM）。前者受限于注意力图的空间分辨率与语义对齐精度，后者则依赖额外模型且边界粗糙。

VDFE的DFD模块通过**解耦流差异**实现无需训练的细粒度定位。其核心洞察是：在视频扩散模型的特征空间中，需要编辑的区域在两个提示条件下的速度场会产生显著偏移。通过计算源与目标速度场的L2距离并进行多步Softmax融合：

$$D_{maps}(i,j) = \sum_{t=1}^{M} w_t \cdot \frac{\exp(D_t(i,j))}{\sum_{k=1}^{H} \sum_{l=1}^{W} \exp(D_t(k,l))}$$

生成的流差异图在语义边界精度上显著优于交叉注意力图（如Figure 3所示），为后续的差异感知高斯编辑提供了精确的空间引导。

### 适用边界与局限

VDFE的性能上限受限于所采用的视频扩散模型能力。当编辑指令涉及视频扩散模型训练分布之外的概念组合、极端视角变换或细粒度结构修改时，FlowOCE生成的编辑轨迹可能出现语义偏离。此外，整体流水线涉及伪视频渲染、最优控制编辑、流差异计算和差异感知高斯优化四个模块的协同运作，计算开销高于简单的2D扩散迭代方法。

DAGE模块通过参数扰动和梯度分配实现了对核心高斯的精准优化，但其依赖于流差异图的质量。当编辑区域与非编辑区域在速度场空间中差异不显著时（如材质替换而非几何修改），DFD的定位精度可能下降，进而影响DAGE的选择性优化效果。

### 开放问题

1.  **视频扩散先验的轻量化使用**：当前方法需要完整的视频扩散模型前向传播来计算编辑轨迹和流差异图。能否通过知识蒸馏或特征缓存技术，将视频扩散先验的使用解耦为轻量级的条件注入模块，以降低计算开销？

2.  **非侵入式定位策略的泛化**：DFD模块的无需训练定位机制本质上利用了扩散模型特征空间中的语义偏移特性。这一策略是否可推广到其他生成式编辑任务，如3D生成过程中的局部控制、运动迁移中的区域指定，甚至超越视觉领域的序列编辑任务？

3.  **编辑一致性的理论边界**：VDFE通过视频扩散先验隐式地建模多视角一致性，但缺乏对一致性程度的显式量化与保证。在极端视角变化或长序列编辑场景下，一致性的理论下界是什么？能否通过引入显式的几何约束（如对极几何）来补充视频先验的隐式约束？

## 原文 PDF

![[paperPDFs/CVPR_2026/VDFE_Difference_Aware_3D_Scene_Editing_with_Non_Intrusive_Video_Diffusion_Priors_for_Multi_View_Consistency_and_Efficiency.pdf]]
