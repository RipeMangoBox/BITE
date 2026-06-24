---
title: "3DGSR: Implicit Surface Reconstruction with 3D Gaussian Splatting"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/3DGSR_Implicit_Surface_Reconstruction_with_3D_Gaussian_Splatting.pdf
project_link: null
code_link: "https://github.com/NVlabs/tiny-cuda-nn"
aliases:
- 3ISR3GS
tags:
- SIGGRAPH_ASIA_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过将隐式 SDF 场与 3DGS 进行松散耦合（约束高斯位置靠近表面并使法线对齐）并利用体积渲染的几何一致性损失提供密集监督。
primary_logic: 松散耦合策略为 SDF 和 3DGS 保留灵活性，既保证表面重建细节又维持高渲染质量，同时体积渲染一致性损失弥补高斯稀疏信号的不足。
claims:
- 在 NeRF-synthetic 和 DTU 数据集上同时达到最佳表面重建和渲染性能。
- 松散耦合策略优于紧密耦合，Chamfer-L1 1.37 vs 1.52，PSNR 33.86 vs 33.52。
- 移除体积渲染深度/法线正则化导致 Chamfer-L1 退化至 3.63。
- NeRF-synthetic 上 PSNR / Chamfer-L1 = 33.86 / 1.37
---

# 3DGSR: Implicit Surface Reconstruction with 3D Gaussian Splatting

> [!tip] 核心洞察
> 松散耦合策略为 SDF 和 3DGS 保留灵活性，既保证表面重建细节又维持高渲染质量，同时体积渲染一致性损失弥补高斯稀疏信号的不足。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3DGSR: 基于三维高斯泼溅的隐式表面重建 |
| 英文题名 | 3DGSR: Implicit Surface Reconstruction with 3D Gaussian Splatting |
| 会议/期刊 | SIGGRAPH ASIA 2024 |
| Links | [paper](https://arxiv.org/abs/2404.00409) · [Code](https://github.com/NVlabs/tiny-cuda-nn) · [arXiv](https://arxiv.org/abs/2403.16964) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3DGSR |
| Dataset | NeRF-synthetic, DTU |

> [!tip] 效果简介
> - NeRF-synthetic 上，PSNR / Chamfer-L1 33.86 / 1.37 vs 3DGS PSNR 33.32 / 2DGS C-L1 1.40 (+0.54 PSNR, -0.03 C-L1)。
> - DTU 上，Chamfer-L1 (mean) 0.70 vs 2DGS 0.80 (-0.10)。

## 概要

原始三维高斯泼溅（3DGS）虽能高效高质量渲染，但其无组织点云表示缺乏连续表面几何，难以直接用于表面重建。本文提出 **3DGSR**，核心思路是在 3DGS 中引入隐式符号距离场（SDF），并通过“松散耦合”策略将高斯分布约束在表面附近、使高斯最短轴对齐表面法线，同时利用体积渲染的深度与法线一致性损失提供密集几何监督。这一设计既保留了 3DGS 的渲染灵活性与效率，又赋予其精确的表面重建能力。在 NeRF-synthetic 和 DTU 数据集上，3DGSR 同时达到最优表面重建精度（Chamfer-L1 1.37 / 0.70）和视角合成质量（PSNR 33.86），超越 2DGS、NeuS、SuGaR 等方法。方法定位于基于高斯泼溅的隐式表面重建，通过 SDF 场与高斯表示的松散对齐填补了 3DGS 在几何建模上的关键缺口。

## 核心方法与创新机理

### 问题背景与唯一瓶颈

3D Gaussian Splatting（3DGS）以显式点云表示场景，通过泼溅渲染实现高质量实时视角合成，但其无组织的离散高斯点云无法直接提供连续、规整的表面几何。要从 3DGS 中提取表面，面临的核心瓶颈是：**高斯点缺乏对底层表面的显式约束，既没有表面对齐信号，也缺乏全局几何一致性监督**。这导致从高斯点提取的网格往往噪声大、细节缺失或结构错误。

现有基于高斯的方法（如 2DGS、SuGaR、GOF）尝试通过将高斯扁平化为 2D 面片或直接定义高斯为表面元素来获得几何，但这些紧密耦合策略要么牺牲了 3DGS 原有的渲染灵活性，要么因高斯分布不均匀而产生过平滑或噪声伪影（Fig. 2, Fig. 3）。因此，核心挑战在于：**如何在保留 3DGS 高效渲染能力的同时，赋予其高质量表面重建能力**。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2404_00409/figures/002_Figure_2.jpg]]
*Figure 2: Oversmooth reconstruction results from 2DGS [Huang et al. 2024] lead to poorer performance, reflected by a higher chamfer-L1 error (1.40) compared to 3DGSR (0.72)*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2404_00409/figures/003_Figure_3.jpg]]
*Figure 3: Imperfect reconstruction from the non-uniform distributions of Gaussians. Directly defining the surface from the Gaussian points may lead the noisy reconstruction or artifacts*

### 核心创新思路

3DGSR 的核心洞察是采用**松散耦合策略**：不将 SDF 直接绑定到高斯的不透明度上，而是将隐式 SDF 场作为一个独立的几何先验，仅通过位置和方向约束引导高斯分布，使高斯附着于表面附近。同时，引入**体积渲染一致性损失**，从 SDF 场渲染深度和法线，与 3DGS 自身的深度/法线进行对齐，为 SDF 提供密集的几何监督信号。这种设计为 SDF 和高斯各自保留了优化自由度，既保证了表面重建的精度和细节，又维持了 3DGS 的渲染质量。

### 关键 Changed Slots

相比 3DGS 和现有高斯表面重建方法，3DGSR 在以下三个关键维度进行了改变：

| 维度 | 基线方法 | 3DGSR 方案 | 因果作用 |
|------|---------|-----------|---------|
| **几何表示** | 仅 3D 高斯点云 | 增加隐式 SDF 场（多分辨率哈希网格 + 单层 MLP） | 提供连续、可微的表面表示 |
| **高斯-表面耦合** | 无耦合或紧密耦合 | 松散耦合：距离约束 + 法线对齐 | 引导高斯分布而不限制其表达力 |
| **SDF 正则化** | 仅图像光度损失 | 体积渲染深度/法线一致性损失 | 为 SDF 提供密集几何监督 |

### 方法框架与模块顺序

3DGSR 的整体流程如 Fig. 4 所示，由四个核心模块级联构成：

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2404_00409/figures/004_Figure_4.jpg]]
*Figure 4: Pipeline of our proposed approach for implicit surface reconstruction. We model the surface with an implicit SDF field, with which the SDF value of each 3D Gaussian can be predicted. We propose two different coupling strategies to make the distribution of Gaussians align with the implicit SDF field. The geometry attributes of 3D Gaussians serve as a regularization for the SDF field, while the rendered image is supervised by the captured image*

**模块 1：隐式 SDF 场**  
使用多分辨率哈希编码对空间位置 $x$ 进行编码，送入单层 MLP 预测 SDF 值 $f(x)$。表面 $\operatorname{S}$ 定义为 SDF 的零等值面：
$$\operatorname{S} = \{ x \in \mathbb{R}^3 \mid f(x) = 0 \}$$
该模块为场景提供连续的隐式几何表示，是后续所有几何约束的基础。

**模块 2：3DGS 渲染模块**  
维护一组 3D 高斯点，每个高斯由中心位置 $\mu$、协方差矩阵 $\Sigma = RSS^TR^T$（分解为缩放 $S$ 和旋转 $R$）、不透明度 $\alpha$ 和球谐系数组成。通过泼溅渲染生成图像、深度图 $\mathcal{D}(r)$ 和法线图 $\mathcal{N}(r)$。

**模块 3：耦合对齐模块**  
这是 3DGSR 的核心创新。松散耦合策略通过两个损失函数将高斯分布约束到 SDF 表面：

- **方向对齐损失**：强制高斯的最短轴（最小缩放方向）与 SDF 梯度（表面法线）对齐：
  $$\mathcal{L}_a = \|1 - n_g \cdot \nabla f(x_g)\|$$
  其中 $n_g$ 是高斯最短轴方向，$\nabla f(x_g)$ 是高斯位置处的 SDF 梯度。

- **最近表面点距离损失**：将高斯位置投影到 SDF 最近表面点：
  $$x_{\text{nearest}} = x_g + f(x_g) \cdot \nabla f(x_g)$$
  然后用 L1 损失最小化 $x_g$ 与 $x_{\text{nearest}}$ 的距离。

这种松散耦合的因果优势在于：SDF 仅作为几何引导，不直接控制高斯的不透明度或颜色，因此高斯仍能自由优化以保持渲染质量；同时，距离和方向约束使高斯自然聚集在表面附近，形成规整分布，减少了约 20% 的高斯数量而不损失渲染质量（Fig. 3）。

**模块 4：体积渲染正则化模块**  
为弥补高斯稀疏信号对 SDF 监督的不足，该模块从 SDF 场进行体积渲染，生成深度和法线，并与 3DGS 的对应输出计算一致性损失：

- **SDF 到不透明度的转换**：使用 S 形函数 $\phi_s$ 将 SDF 值转换为密度，再计算沿射线的透射率 $T_i^r$ 和 alpha 值：
  $$T_i^r = \prod_{j=1}^{i-1}(1-\alpha_i),\quad \alpha_i = \max\left(\frac{\phi_s(f(x_i)) - \phi_s(f(x_{i+1}))}{\phi_s(f(x_i))}, 0\right)$$

- **体积渲染深度和法线**：
  $$\tilde{\mathbf{D}}(r) = \sum_{i=1}^{M} T_i^r \alpha_i t_i^r,\quad \tilde{\mathbf{N}}(r) = \sum_{i=1}^{M} T_i^r \alpha_i \tilde{n}_i^r$$

- **一致性损失**：
  $$\mathcal{L}_{\text{vd}} = \sum_{r \in \mathcal{R}} \|\mathcal{D}(r) - \tilde{\mathbf{D}}(r)\|_2$$
  $$\mathcal{L}_{\text{vn}} = \sum_{r \in \mathcal{R}} \|\mathcal{N}(r) - \tilde{\mathbf{N}}(r)\|_1 + \|1 - \mathcal{N}(r) \cdot \tilde{\mathbf{N}}(r)\|_1$$

该模块的因果链路是：3DGS 渲染的深度和法线虽然来自离散高斯，但已被光度损失优化至合理精度；将这些作为伪真值监督 SDF 的体积渲染输出，为 SDF 场提供了密集、全局的几何一致性信号，这是仅靠稀疏高斯位置约束无法获得的。

### 训练与推理路径

**训练阶段**，总损失函数为：
$$\mathcal{L} = \mathcal{L}_{\text{rgb}} + \lambda_a \mathcal{L}_a + \lambda_d \mathcal{L}_d + \lambda_{\text{vd}} \mathcal{L}_{\text{vd}} + \lambda_{\text{vn}} \mathcal{L}_{\text{vn}} + \lambda_{\text{eik}} \mathcal{L}_{\text{eik}}$$
其中 $\mathcal{L}_{\text{rgb}}$ 是 3DGS 的图像光度损失，$\mathcal{L}_d$ 是最近表面点距离损失，$\mathcal{L}_{\text{eik}} = \mathbb{E}_x[(\|\nabla f\| - 1)^2]$ 是 Eikonal 正则项。所有模块联合优化，SDF 场和高斯参数通过反向传播同步更新。在 DTU 数据集上还可选加入稀疏深度监督 $D_{\text{sfm}}$。

**推理阶段**，表面重建直接从优化后的 SDF 场提取零等值面（如使用 Marching Cubes），无需依赖高斯点的分布。视角合成则使用标准 3DGS 渲染管线，保持了实时渲染效率。

### 与紧密耦合的本质区别

紧密耦合策略（如 GOF）通过可微变换将 SDF 值直接映射为高斯不透明度：
$$\Phi_\beta(f(x)) = \frac{e^{-\beta \cdot f(x)}}{(1 + e^{-\beta \cdot f(x)})^2}$$
这强制 SDF 值接近零以产生高不透明度，导致高斯被迫聚集在零等值面附近，限制了优化自由度，容易产生噪声表面和不必要细节（Fig. 3, Fig. 10）。松散耦合解除了这种硬性绑定，使 SDF 和高斯各司其职：SDF 负责几何表示，高斯负责外观渲染，二者通过软约束协调，实现了渲染质量与重建精度的双赢。

## 实验与关键发现

3DGSR 在 NeRF-synthetic 和 DTU 两个标准基准上同时评估了视角合成质量与表面重建精度，与神经隐式表面重建方法（NeuS）、基于高斯的表面重建方法（2DGS、SuGaR、GOF）以及纯视角合成方法（3DGS）进行了系统对比。

### 主实验结果

在 NeRF-synthetic 数据集上，3DGSR 实现了 **PSNR 33.86** 的渲染质量，超越了原始 3DGS 的 33.32，同时获得了 **Chamfer-L1 1.37** 的表面重建精度，优于 2DGS 的 1.40（Table 1, Table 3）。这验证了核心论断：松散耦合策略在引入表面约束的同时并未损害 3DGS 的渲染能力，反而通过几何正则化略微提升了视角合成质量。2DGS 的过平滑问题导致其 Chamfer-L1 误差更高（Fig. 2 中 2DGS 为 1.40，3DGSR 为 0.72），说明将高斯扁平化为二维圆盘虽有利于表面定义，但牺牲了几何细节的保真度。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2404_00409/figures/007_Table_1.jpg]]
*Table 1: We assess the quality of synthesized images and the accuracy of surface reconstruction, with each cell colored to indicate the best and second best . Our method is compared against various state-of-the-art (SOTA) approaches in tasks of novel view synthesis and surface reconstruction. It outperforms all competitors in both tasks, achieving the highest PSNR and the lowest Chamfer-L1 (C-L1) distance*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2404_00409/figures/009_Table_3.jpg]]
*Table 3: More quantitative assessment on the NeRF synthetic dataset*

在 DTU 真实扫描数据集上，3DGSR 取得了 **平均 Chamfer-L1 0.70**，显著优于 2DGS 的 0.80（Table 2）。值得注意的是，当加入稀疏深度监督 $D_{sfm}$ 后，3DGSR 的 Chamfer-L1 从 0.81 进一步降至 0.70（Table 6），而同样的监督信号对 2DGS 产生了负面影响。这一对比揭示了方法设计的深层差异：3DGSR 的隐式 SDF 场能够有效利用稀疏深度信号进行全局几何正则化，而 2DGS 的显式高斯圆盘表示缺乏类似的连续场来吸收和传播稀疏约束。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2404_00409/figures/008_Table_2.jpg]]
*Table 2: Quantitative assessment on the DTU dataset with each cell colored to indicate the best second best and third best . Our method achieves the highest average quality of surface reconstruction and the lowest Chamfer*

### 关键消融实验

Table 5 的消融研究揭示了各组件的因果贡献：

**体积渲染正则化是最关键的组件。** 移除体积渲染的深度和法线一致性损失后，Chamfer-L1 从 1.37 急剧退化至 **3.63**，表明仅靠高斯位置约束和图像光度损失无法提供足够的几何监督。3DGS 渲染的深度和法线本质上是高斯原语的加权混合，缺乏全局几何一致性；体积渲染从 SDF 场累积深度和法线（Eq. 11-12），通过一致性损失（Eq. 13-14）将这种全局几何信号反向传播至 SDF 场，形成了密集监督闭环。

**松散耦合策略优于紧密耦合。** 紧密耦合将 SDF 值通过可微变换 $\Phi_\beta$ 直接映射为高斯不透明度（Eq. 7），强制高斯分布与 SDF 零等值面严格绑定。然而，这种强约束导致 Chamfer-L1 升至 1.52，PSNR 降至 33.52。原因在于 3DGS 的高斯分布天然具有非均匀性，紧密耦合会将这种非均匀性传导至表面定义，产生噪声和伪影（Fig. 3, Fig. 10）。松散耦合仅通过方向对齐损失（Eq. 9）和最近表面点距离损失（Eq. 10）约束高斯的位置和朝向，保留了 3DGS 对复杂外观的建模灵活性，同时确保高斯分布在几何上靠近隐式表面。

**方向对齐损失和最近点投影损失的独立贡献**在 Table 5 中得到量化：单独移除方向对齐损失或最近点投影损失均导致 Chamfer-L1 上升，验证了“位置靠近表面”和“最短轴对齐法线”两个约束的互补性。

### 速度与资源分析

Table 4 显示，3DGSR 在 DTU 上的训练时间约为 15 分钟（单卡 RTX 3090，30000 次迭代），推理速度达到实时水平。与 NeuS 等神经隐式方法相比，训练速度提升了一个数量级以上，同时保持了可比的表面重建精度。这一效率优势源于 3DGS 的光栅化渲染管线与隐式 SDF 场的轻量设计（多分辨率哈希网格 + 单层 MLP）的结合。

### 失败模式与适用边界

尽管 3DGSR 在受控场景下表现优异，论文明确指出了三个适用边界：

1. **无界场景能力有限**：多分辨率哈希网格和隐式 SDF 的表示能力受限于预定义的边界范围，难以直接扩展到大规模室外场景。这是哈希编码方法的固有局限，需要手动验证是否有后续工作通过收缩空间或分层哈希网格解决。

2. **噪声姿态估计敏感**：在真实数据集上，因 SfM 姿态估计存在噪声，导致重建结果不理想。体积渲染正则化依赖准确的光线投射，姿态误差会破坏深度和法线一致性约束的有效性。

3. **透明物体重建困难**：SDF 场假设表面为不透明介质的分界面，透明物体违反了这一假设，导致 SDF 零等值面定义模糊。这是所有基于 SDF 的表面重建方法的共同局限。

此外，稀疏深度监督 $D_{sfm}$ 的可用性依赖于 SfM 关键点的可见性和密度，在纹理稀疏或无纹理区域可能无法提供有效监督，此时方法的几何精度将退回到仅依赖体积渲染正则化的水平。

## 定位与知识库关联

3DGSR 的核心定位是在 **3D Gaussian Splatting（3DGS）** 这一高效新视角合成框架之上，通过引入隐式 SDF 场与松散耦合策略，补足了原始 3DGS 在表面几何重建上的根本性缺陷。与现有工作的本质差异体现在三个关键 slot 的改变上。

**Slot 1：几何表示从无组织点云到隐式 SDF 场。** 原始 **3DGS**（Kerbl et al., ACM TOG 2023）仅维护一组各向异性 3D 高斯核，其优化目标纯粹由光度损失驱动，因此高斯点的空间分布并不遵循任何显式的表面约束，无法直接提取连续、高质量的网格表面。**2DGS**（Huang et al., SIGGRAPH 2024）通过将 3D 高斯坍缩为 2D 平面高斯（surfels）来强制表面性，但这一硬约束导致重建结果过度平滑（图 2，Chamfer-L1 1.40 vs 3DGSR 0.72），丧失了细节保真度。3DGSR 则独立维护一个基于多分辨率哈希网格编码的单层 MLP 隐式 SDF 场 $f(x)$，其零等值面 $\operatorname{S} = \{x \in \mathbb{R}^3 \mid f(x) = 0\}$ 直接定义了重建表面。这一设计将表面表示与高斯渲染解耦，使得 SDF 场可以专注于几何优化，而 3DGS 继续负责高质量渲染。

**Slot 2：耦合策略从紧密耦合到松散约束。** 与 3DGSR 同期的 **GOF**（Yu et al., 2024）采用紧密耦合策略，通过可微的 SDF-to-opacity 变换 $\Phi_\beta(f(x)) = e^{-\beta f(x)} / (1 + e^{-\beta f(x)})^2$ 将 SDF 值直接映射为高斯的不透明度。这一绑定迫使高斯严格分布在零等值面附近，但如图 3 和图 5 所示，当高斯分布不均匀时，紧密耦合会产生噪声表面和伪影。3DGSR 的松散耦合策略仅施加两项软约束：方向对齐损失 $\mathcal{L}_a = ||1 - n_g \nabla f(x_g)||$ 使高斯的最短轴与 SDF 法线对齐，以及将高斯位置投影到最近表面点 $x_{\text{nearest}} = x_g + f(x_g) \cdot \nabla f(x_g)$ 后施加 L1 距离损失。消融实验（表 5）证实，松散耦合在 Chamfer-L1（1.37 vs 1.52）和 PSNR（33.86 vs 33.52）上均优于紧密耦合，且能减少约 20% 的高斯点数量而不损害渲染质量。

**Slot 3：SDF 监督从稀疏信号到体积渲染密集正则化。** **NeuS**（Wang et al., NeurIPS 2021）等神经隐式方法依赖体积渲染直接从 SDF 推导图像，其几何监督来源于多视图光度一致性，但训练和渲染效率远低于 3DGS。3DGSR 创造性地将体积渲染用作正则化工具而非主渲染管线：从 SDF 场通过体积渲染累积深度 $\tilde{\mathbf{D}}(r)$ 和法线 $\tilde{\mathbf{N}}(r)$（式 11-12），并与 3DGS 光栅化得到的深度 $\mathcal{D}(r)$ 和法线 $\mathcal{N}(r)$ 计算一致性损失 $\mathcal{L}_{vd}$ 和 $\mathcal{L}_{vn}$（式 13-14）。这一设计使 SDF 场获得了密集的几何监督信号，弥补了 3DGS 高斯点稀疏分布的不足。消融实验（表 5）表明，移除体积渲染深度/法线正则化后 Chamfer-L1 从 1.37 退化至 3.63，证明了该模块的决定性作用。

**知识库挂载点与适用边界。** 3DGSR 在知识图谱中的挂载位置是 **3D Gaussian Splatting 框架的几何重建扩展分支**，与 2DGS、SuGaR（Guédon and Lepetit, 2023）、GOF 等构成高斯表面重建方法簇。其松散耦合范式为后续工作提供了一个重要启示：在高斯渲染框架中，表面表示与外观表示的适度解耦可以同时保留两者的优势。然而，该方法存在明确的适用边界：（1）多分辨率哈希网格和隐式 SDF 的表示能力受限于有界场景，在无界场景中表现受限；（2）对噪声姿态估计敏感，在真实数据集上结果不理想；（3）透明物体的 SDF 定义模糊，重建存在困难。这些限制为后续研究指明了方向：如何将隐式 SDF 扩展到无界场景、如何提升对姿态噪声的鲁棒性、以及如何处理非朗伯表面的几何重建。此外，稀疏深度监督 $D_{sfm}$ 对 3DGSR 有益（表 6，Chamfer-L1 从 0.81 降至 0.70）但对 2DGS 产生负面影响，这一现象提示松散耦合框架对外部几何先验具有更好的兼容性，值得进一步探索。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/3DGSR_Implicit_Surface_Reconstruction_with_3D_Gaussian_Splatting.pdf]]