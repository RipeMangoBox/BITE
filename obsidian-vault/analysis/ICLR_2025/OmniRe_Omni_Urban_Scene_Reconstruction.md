---
title: "OmniRe: Omni Urban Scene Reconstruction"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/OmniRe_Omni_Urban_Scene_Reconstruction.pdf
project_link: https://ziyc.github.io/omnire/
code_link: null
aliases:
- OmniRe
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过构建动态高斯场景图，引入基于SMPL的人体参数模型对行人进行关节级建模，并利用变形网络处理其它无模板非刚体对象，实现了对所有动态实体的统一可控重建。"
primary_logic: "OmniRe 采用场景图结构，为不同类型的动态物体分配不同的高斯表示（包括背景、刚体节点、SMPL 节点和变形节点），使得系统能够捕捉精细的人体运动和外观，从而支持高保真仿真和场景编辑。"
claims:
- "OmniRe 在全图重建上达到 34.25 PSNR，比之前最优方法 StreetGS 的 29.08 高出 5.17 PSNR。"
- "移除 SMPL 节点导致人类区域 PSNR 从 28.15 骤降至 24.71，验证了关节级建模的关键性。"
- "在 32 个高动态 Waymo 场景上，OmniRe 达到 33.73 PSNR，显著优于 StreetGS (29.93) 和 EmerNeRF (31.29)。"
- "Waymo (8 dynamic scenes) 上 Full Image PSNR = 34.25"
---

# OmniRe: Omni Urban Scene Reconstruction

> [!tip] 核心洞察
> OmniRe 采用场景图结构，为不同类型的动态物体分配不同的高斯表示（包括背景、刚体节点、SMPL 节点和变形节点），使得系统能够捕捉精细的人体运动和外观，从而支持高保真仿真和场景编辑。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | OmniRe：全能城市场景重建 |
| 英文题名 | OmniRe: Omni Urban Scene Reconstruction |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2408.16760) · [Project](https://ziyc.github.io/omnire/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | OmniRe |
| Dataset | Waymo (8 dynamic scenes), Waymo (32 dynamic scenes) |

> [!tip] 效果简介
> - Waymo (8 dynamic scenes) 上，Full Image PSNR 为 34.25，对比 29.08 (StreetGS)，变化 +5.17。
> - Waymo (8 dynamic scenes) 上，Human PSNR (Recon.) 为 28.15，对比 16.83 (StreetGS)，变化 +11.32。
> - Waymo (8 dynamic scenes) 上，Vehicle PSNR (Recon.) 为 28.91，对比 27.73 (StreetGS)，变化 +1.18。

## 概要

### 1. 问题瓶颈

现有动态城市场景重建方法 —— 无论是基于 NeRF 的 **EmerNeRF**（Yang et al., 2023a）还是基于 3D Gaussian Splatting 的 **StreetGS**（Yan et al., 2024）、**HUGS**（Zhou et al., 2024）—— 主要聚焦于车辆等刚体对象的建模，对行人、骑行者等非刚体交通参与者缺乏精细的关节级表示。这使得重建结果在人体区域模糊失真，无法支持以人为中心的交互仿真和场景编辑，成为制约数字孪生与自动驾驶模拟应用的关键瓶颈。

### 2. 核心方法定位

**OmniRe** 的核心思路是构建一个**动态高斯场景图（Gaussian Scene Graph）**，为不同类型的场景元素分配异构的高斯基元表示：

- **静态背景**与**天空**：分别由独立的高斯节点建模，天空采用环境贴图合成。
- **刚体对象**（车辆等）：通过实例级刚体节点，利用车辆姿态将高斯从局部空间变换到世界空间。
- **非刚体行人**：引入 **SMPL 人体参数模型**，将高斯绑定在 SMPL 网格表面，通过线性混合蒙皮（LBS）实现关节级控制，捕捉精细的人体运动和外观。
- **其他无模板非刚体**（骑行者、远距离行人等）：使用**共享变形网络**，结合实例嵌入，在自监督下学习变形场。

以上所有节点在每帧被统一变换到世界空间，经栅格化渲染后与 LiDAR 深度监督联合端到端优化。这种设计使 OmniRe 成为首个同时覆盖刚体车辆、关节级行人及无模板非刚体对象的统一重建框架。

### 3. 主要结果

在 Waymo 开放数据集的 8 个动态场景上，OmniRe 的全图重建 PSNR 达到 **34.25 dB**，较此前最优方法 StreetGS 的 29.08 dB 提升 **+5.17 dB**（Table 1）。在人体区域，重建 PSNR 达到 **28.15 dB**，比 StreetGS 的 16.83 dB 高出 **+11.32 dB**，验证了 SMPL 节点对非刚体建模的决定性贡献。在扩展的 32 个高动态场景上，OmniRe 同样以 33.73 dB 显著优于 StreetGS（29.93 dB）和 EmerNeRF（31.29 dB）（Table 5）。

### 4. 方法谱系与知识库定位

| 维度 | 基线方法 | OmniRe 的变更 |
|------|----------|---------------|
| **非刚体人体建模** | StreetGS / HUGS 无关节级建模，仅使用变形场或不专门处理 | 使用 SMPL 动态高斯，实现关节级控制与表面绑定（Eq.2） |
| **其他非刚体建模** | 无处理或不区分 | 共享变形网络 + 实例嵌入，自监督建模无模板物体（Eq.3） |
| **场景图节点类型** | StreetGS / HUGS 仅刚体节点 | 背景、Sky、Rigid、SMPL、Deformable 五种异构节点（Fig.2） |
| **人体姿态估计** | 无专门多视角时序优化 | 多视角匹配与缺失姿态插值，联合优化姿态与高斯（Fig.3） |

OmniRe 继承了 **3DGS**（Kerbl et al., 2023）的高效栅格化渲染管线，以及场景图分解的思想（HUGS、StreetGS），但在非刚体建模上做出了实质性突破：首次将 SMPL 模板先验与 3DGS 深度融合，并通过共享变形网络覆盖模板外类别，填补了“以人为中心”的动态场景重建空白。

### 5. 证据强度与局限

- **高置信度证据**：全图与人体区域的 PSNR 大幅领先（Table 1），消融实验确认 SMPL 节点移除导致人体 PSNR 骤降 3.44 dB（Table 2），边界框优化贡献约 +1.2 dB（Table 4）。
- **需注意的局限**：方法依赖数据集提供的精确边界框和语义标签，在标注质量较低的场景下泛化能力可能受限；缺乏显式光照建模，动态仿真中插入的虚拟物体与背景的视觉和谐性有待验证。

### 城市场景重建的范式转移

自动驾驶与数字孪生对高保真城市场景重建提出了迫切需求。近年来，3D 重建范式经历了从 NeRF 到 3D Gaussian Splatting（3DGS）的关键转变。3DGS 以显式三维高斯球表示场景几何与外观，通过可微栅格化实现实时渲染，为大规模动态场景重建开辟了新路径。

### 现有方法的根本瓶颈

当前动态城市场景重建方法——包括基于 NeRF 的 **EmerNeRF**（Yang et al., 2023a）和基于 3DGS 的 **StreetGS**（Yan et al., 2024）、**HUGS**（Zhou et al., 2024）——主要聚焦于车辆等刚体对象的建模。这些方法通过场景图结构将车辆表示为独立的刚体节点，利用目标姿态实现时空变换。然而，它们对行人、骑行者等非刚体交通参与者缺乏精细建模能力。

这一缺陷的根源在于表示机制的缺失：现有方法要么完全忽略非刚体对象，要么将其与背景一同交由通用变形场处理，无法捕捉人体的关节级运动细节。由此导致两个层面的问题：

- **重建质量断层**：人类相关区域的重建质量显著低于车辆区域，StreetGS 在 Waymo 数据集上的人类区域 PSNR 仅为 16.83，远低于车辆区域的 27.73（Tab.1）。
- **应用能力受限**：缺乏对人体的关节级控制，使得重建结果无法直接对接行为模型与动画系统，难以支撑高保真仿真、场景编辑、人车交互等下游应用。

### OmniRe 的核心动机

OmniRe 的出发点在于：**城市场景的数字孪生必须以人为中心**。真实的交通场景中，行人与骑行者的行为是驾驶决策的关键输入，任何忽略非刚体参与者的重建都只是残缺的世界模型。

为实现这一目标，OmniRe 提出构建**动态高斯场景图**，为不同类型的动态实体分配差异化的高斯表示：刚体节点处理车辆，SMPL 节点引入人体参数模型实现关节级建模，变形节点覆盖无模板的非刚体对象。这一统一框架使得系统能够同时捕捉精细的人体运动与外观，从而将重建质量从“能看清车”提升到“能看清人”的层次，并天然支持行为仿真与场景编辑。

## 核心方法与创新机理

OmniRe 的核心创新在于构建了一个**支持非刚体精细建模的动态高斯场景图**，从根本上突破了现有方法仅能处理刚体动态对象的局限。其关键创新点体现在以下几个 changed slots 上：

### 1. 非刚体人体建模：从无关节建模到 SMPL 关节级控制

**Baseline 现状：** 现有动态场景重建方法（如 **StreetGS** (Yan et al., 2024)、**HUGS** (Zhou et al., 2024)）仅通过刚体节点处理车辆等刚性运动物体，对行人等非刚体缺乏专门建模，导致人体区域重建质量严重不足——StreetGS 在人体区域的 PSNR 仅 16.83（Tab.1）。

**OmniRe 方案：** 引入基于 SMPL 参数人体模型的**动态高斯节点**，实现关节级精细控制。具体而言，每个行人在规范空间中被初始化为绑定在 SMPL 模板表面的一组高斯，在任意时刻 $t$ 通过线性混合蒙皮（LBS）和全局姿态变换将高斯变形到世界空间：

$$\mathcal{G}_h^{\mathrm{SMPL}}(t) = \mathbf{T}_h(t) \otimes \mathrm{LBS}(\pmb{\theta}(t), \bar{\mathcal{G}}_h^{\mathrm{SMPL}})$$

这一设计使得系统能够捕捉行人的关节运动、肢体姿态和外观细节。消融实验（Tab.2）表明，移除 SMPL 节点导致人体区域 PSNR 从 28.15 骤降至 24.71（-3.44），验证了关节级建模对非刚体人体重建的关键性。

### 2. 其他非刚体建模：从无处理到共享变形网络

**Baseline 现状：** 现有方法对骑行者、携带物品的行人等无模板的非刚体对象缺乏有效处理，这些“分布外”类别往往被忽略或重建失败。

**OmniRe 方案：** 提出**共享变形网络**（shared deformation field）对无模板非刚体对象进行建模。该网络权重在多个实例间共享，通过实例嵌入 $e_h$ 区分不同对象的身份，以自监督方式学习每个对象的变形：

$$\mathcal{G}_h^{\mathrm{deform}}(t) = \mathbf{T}_h(t) \otimes \left( \bar{\mathcal{G}}_h^{\mathrm{deform}} \oplus \mathcal{F}_\varphi(\bar{\mathcal{G}}_h^{\mathrm{deform}}, e_h, t) \right)$$

消融实验（Tab.2）显示，移除变形节点导致人体区域 PSNR 从 28.15 降至 25.26（-2.89），证明该模块对处理多样化非刚体对象不可或缺。

### 3. 场景图节点类型：从仅刚体到五类异构节点

**Baseline 现状：** 现有高斯场景图方法（如 StreetGS、HUGS）仅包含背景节点和刚体节点两类，缺乏对不同语义类别动态实体的差异化表示能力。

**OmniRe 方案：** 将场景图扩展为五类异构节点（Fig.2）：
- **Sky Node**：单独优化的环境贴图，通过 alpha 合成与高斯渲染结果融合
- **Background Node**：静态背景高斯
- **Rigid Nodes**：车辆等刚体，通过物体姿态变换建模
- **SMPL Nodes**：行人非刚体，通过 SMPL+LBS 实现关节级控制
- **Deformable Nodes**：其他非刚体，通过共享变形网络建模

这种异构节点设计使得系统能够为不同类型的动态实体分配最适合的高斯表示，从而实现统一而精细的全场景重建。

### 4. 人体姿态估计：从无专门优化到多视角联合优化

**Baseline 现状：** 现有方法不涉及人体姿态的专门处理，或仅依赖单帧单视角的离线姿态估计，难以应对自动驾驶场景中的严重遮挡和多视角一致性问题。

**OmniRe 方案：** 设计了完整的人体姿态处理管线（Fig.3），包括：
- **多视角 ID 匹配**：确保同一行人在不同摄像头视角下被一致识别
- **缺失姿态插值**：对遮挡个体进行姿态补全
- **联合优化**：将人体姿态参数与高斯参数端到端联合优化，使姿态估计服务于最终重建质量

消融实验（Tab.2, Fig.6）表明，移除人体姿态优化导致人体区域 PSNR 从 28.15 降至 26.97（-1.18），验证了该模块对提升人体重建精度的重要贡献。

### 创新总结

OmniRe 的核心创新逻辑链条清晰：**识别瓶颈（缺乏非刚体建模）→ 引入因果调节变量（SMPL 关节级控制 + 变形网络）→ 构建统一框架（五类异构场景图节点）→ 辅助优化（多视角人体姿态联合优化）**。这一系列创新使得 OmniRe 在全图重建上达到 34.25 PSNR，比之前最优方法 StreetGS 的 29.08 高出 5.17 PSNR（Tab.1），尤其在人体区域实现了 +11.32 PSNR 的跨越式提升。

OmniRe 的核心是一个**动态高斯场景图**（Dynamic Gaussian Scene Graph），它将整个城市场景分解为五种功能互补的节点类型，并在统一框架下进行端到端联合优化。该框架的输入为多相机 RGB 图像与 LiDAR 点云，输出为可支持新视角合成、场景编辑与行为仿真的完整 3D 表征。

### 场景图结构与节点角色

OmniRe 的场景图由以下五类节点构成（Fig. 2）：

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2408_16760/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. Gaussians of all foreground models are defined in their local or canonical spaces. At a given time t, the Gaussians are deformed and transformed into the world space, forming a Gaussian scene graph together with background Gaussians to model the entire scene. The Gaussians in the scene graph are rasterized to render images and depth, and are jointly optimized using reconstruction losses. We utilize SMPL Gaussians to model non-rigid human bodies and deformable Gaussians to handle out-of-distribution non-rigid categories*

1. **天空节点（Sky Node）**：使用一个可优化的环境贴图对天空颜色进行建模，通过视角方向查询天空颜色，并与高斯渲染结果进行合成（Eq. 4）。
2. **背景节点（Background Node）**：以一组世界空间中的静态 3D 高斯表示场景的静态背景几何与外观。
3. **刚体节点（Rigid Nodes）**：为每个车辆等刚体目标分配一组局部空间中的高斯，通过目标的 6-DoF 位姿变换到世界空间（Eq. 1）。
4. **SMPL 节点（SMPL Nodes）**：针对行人等人体目标，将高斯绑定到 SMPL 参数化人体模型上，通过全局位姿与线性混合蒙皮（LBS）驱动关节级变形（Eq. 2）。
5. **变形节点（Deformable Nodes）**：针对骑行者等无模板的非刚体目标，使用共享权重的变形网络结合实例嵌入，对规范空间中的高斯进行逐点变形（Eq. 3）。

### 前向推理流程

在任意时刻 $t$，系统按照以下流程生成渲染结果（Fig. 2）：

1. **前景变换**：所有前景节点（刚体、SMPL、变形）的高斯从其局部或规范空间出发，经过各自的变换或变形操作，被映射到统一的世界空间。
2. **场景图组装**：变换后的前景高斯与背景高斯在世界空间中合并，形成完整的场景高斯集合。
3. **栅格化渲染**：对场景高斯进行排序和栅格化，生成 RGB 图像 $C_{\mathcal{G}}$ 与不透明度掩膜 $O_{\mathcal{G}}$，同时渲染 LiDAR 深度图用于监督。
4. **天空合成**：将栅格化结果与天空环境贴图 $C_{\mathrm{sky}}$ 按透明度混合，得到最终像素颜色：
   $$C = C_{\mathcal{G}} + (1 - O_{\mathcal{G}}) C_{\mathrm{sky}}$$

### 人体姿态处理管线

为获得 SMPL 节点所需的人体姿态参数，OmniRe 设计了一套专门的人体姿态处理管线（Fig. 3）：

- **多相机 ID 匹配**：利用多视角几何一致性，将不同相机视角中检测到的行人进行跨视角身份匹配，确保同一行人在各视角中获得一致的 ID。
- **缺失姿态补全**：针对被遮挡或检测失败的行人，通过时序插值补全缺失的 SMPL 姿态参数，保证动态建模的连续性。

### 联合优化策略

OmniRe 将所有可学习参数——包括高斯属性、节点位姿、SMPL 姿态、变形网络权重、天空贴图——置于统一的优化框架中，采用如下联合损失函数进行端到端训练：

$$\mathcal{L} = (1 - \lambda_r) \mathcal{L}_1 + \lambda_r \mathcal{L}_{\mathrm{SSIM}} + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{opacity}} \mathcal{L}_{\mathrm{opacity}} + \mathcal{L}_{\mathrm{reg}}$$

其中 $\mathcal{L}_1$ 和 $\mathcal{L}_{\mathrm{SSIM}}$ 为 RGB 重建损失，$\mathcal{L}_{\mathrm{depth}}$ 为 LiDAR 深度监督损失，$\mathcal{L}_{\mathrm{opacity}}$ 约束前景高斯的不透明度以抑制漂浮物，$\mathcal{L}_{\mathrm{reg}}$ 包含对变形幅度和姿态参数的正则化项。

### 与现有方法的关键差异

相较于现有基于场景图的方法（如 **StreetGS**（Yan et al., 2024）和 **HUGS**（Zhou et al., 2024）仅包含刚体节点），OmniRe 的核心创新在于引入了 **SMPL 节点** 和 **变形节点** 两类非刚体建模机制。这一设计使得框架能够：

- 对行人实现关节级精细控制，捕捉肢体运动与外观细节；
- 对骑行者等无模板动态目标进行自监督变形建模，覆盖此前方法无法处理的“分布外”类别；
- 在统一的场景图中实现对静态背景、刚体车辆、非刚体行人及其他动态实体的**全类别统一重建**。

消融实验证实，移除 SMPL 节点会导致人类区域 PSNR 从 28.15 骤降至 24.71（Tab. 2），而移除变形节点则降至 25.26，验证了这两类非刚体节点在框架中的关键作用。

OmniRe 的核心在于构建一个**动态高斯场景图**（Gaussian Scene Graph），为不同类型的场景实体分配差异化高斯表示，并在统一框架下进行端到端联合优化。整个管线由五个节点模块、人体姿态处理模块和联合优化模块构成。

### 4.1 高斯场景图节点

场景图包含五种节点类型，所有前景高斯均在局部或规范空间中定义，在时刻 $t$ 通过变换进入世界空间（Fig. 2）。

**Sky Node（天空节点）**：使用独立的可优化环境贴图 $C_{\mathrm{sky}}$ 建模天空颜色，通过视角方向查询。

**Background Node（背景节点）**：直接在世界空间中放置一组静态高斯，建模不随时间变化的场景结构。

**Rigid Nodes（刚体节点）**：针对车辆等刚体对象，通过车辆姿态 $\mathbf{T}_v(t)$ 将局部高斯变换到世界空间：

$$\mathcal{G}_v^{\mathrm{rigid}}(t) = \mathbf{T}_v(t) \otimes \bar{\mathcal{G}}_v^{\mathrm{rigid}} \tag{1}$$

其中 $\bar{\mathcal{G}}_v^{\mathrm{rigid}}$ 为局部空间中的高斯集，$\otimes$ 表示对高斯均值和协方差的刚性变换。

**SMPL Nodes（SMPL 节点）**：针对行人等人体对象，结合全局姿态与线性混合蒙皮（LBS）实现关节级变形控制：

$$\mathcal{G}_h^{\mathrm{SMPL}}(t) = \mathbf{T}_h(t) \otimes \mathrm{LBS}(\pmb{\theta}(t), \bar{\mathcal{G}}_h^{\mathrm{SMPL}}) \tag{2}$$

$\mathbf{T}_h(t)$ 为人体全局姿态，$\pmb{\theta}(t)$ 为 SMPL 姿态参数，LBS 函数将规范空间高斯根据骨骼变换进行蒙皮变形。SMPL 提供了人体先验模板几何，使高斯初始化更精确，并支持关节级显式控制。

**Deformable Nodes（变形节点）**：针对骑行者、携带物体者等无模板非刚体对象，使用共享变形网络 $\mathcal{F}_\varphi$ 结合实例嵌入 $e_h$ 进行变形建模：

$$\mathcal{G}_h^{\mathrm{deform}}(t) = \mathbf{T}_h(t) \otimes \left( \bar{\mathcal{G}}_h^{\mathrm{deform}} \oplus \mathcal{F}_\varphi(\bar{\mathcal{G}}_h^{\mathrm{deform}}, e_h, t) \right) \tag{3}$$

网络权重 $\varphi$ 在所有变形节点间共享，实例嵌入 $e_h$ 用于区分不同个体，$\oplus$ 表示将网络预测的偏移量叠加到原始高斯属性上。

### 4.2 渲染合成

所有节点高斯在世界空间中组合后，通过 3DGS 标准栅格化管线渲染颜色 $C_{\mathcal{G}}$ 和不透明度掩膜 $O_{\mathcal{G}}$，最终与天空环境贴图合成：

$$C = C_{\mathcal{G}} + (1 - O_{\mathcal{G}}) C_{\mathrm{sky}} \tag{4}$$

其中 $C_{\mathcal{G}}$ 由排序高斯 alpha 混合计算：

$$C = \sum_{i \in \mathcal{N}} \pmb{c}_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)$$

### 4.3 人体姿态处理

人体姿态处理管线（Fig. 3）包含两个关键步骤：(a) 跨摄像头人体 ID 匹配，确保同一人在多视角下身份一致；(b) 缺失姿态补全，通过插值恢复被遮挡个体的 SMPL 姿态参数。姿态参数与高斯属性联合优化，使人体重建精度进一步提升（消融实验中移除姿态优化导致人类区域 PSNR 从 28.15 降至 26.97，Tab. 2）。

### 4.4 联合优化目标

整体损失函数联合监督 RGB 颜色、深度和几何正则：

$$\mathcal{L} = (1 - \lambda_r) \mathcal{L}_1 + \lambda_r \mathcal{L}_{\mathrm{SSIM}} + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{opacity}} \mathcal{L}_{\mathrm{opacity}} + \mathcal{L}_{\mathrm{reg}} \tag{7}$$

各分量含义：
- $\mathcal{L}_1$、$\mathcal{L}_{\mathrm{SSIM}}$：RGB 重建损失，$\lambda_r$ 平衡两者权重
- $\mathcal{L}_{\mathrm{depth}}$：LiDAR 深度监督损失
- $\mathcal{L}_{\mathrm{opacity}}$：不透明度正则，抑制漂浮高斯
- $\mathcal{L}_{\mathrm{reg}}$：其他正则项集合

所有模块参数（高斯属性、节点姿态、变形网络权重、SMPL 参数、环境贴图）在式 (7) 下端到端联合优化。

## 实验与关键发现

OmniRe 在 Waymo Open Dataset 上进行了全面的定量与定性评估，涵盖场景重建、新视角合成、LiDAR 深度精度以及多维度消融实验。所有方法均在相同的三前视摄像头数据上训练，并使用 LiDAR 深度监督。为确保对比公平，作者重新实现了 **StreetGS**（Yan et al., 2024）并加入 LiDAR 监督；**3DGS**（Kerbl et al., 2023）和 **DeformableGS**（Yang et al., 2023c）同样添加了相同的深度损失。AbsGrad 在所有重现方法中默认启用，但消融实验（Tab.11）表明其贡献微小（约 +0.1 PSNR），并非 OmniRe 性能领先的关键因素。

### 场景重建与新视角合成主结果

Table 1 展示了在 8 个动态 Waymo 场景上的核心对比。OmniRe 在全图重建上达到 **34.25 PSNR / 0.954 SSIM**，相比此前最优方法 StreetGS 的 29.08 PSNR 提升了 **+5.17 PSNR**，相对 EmerNeRF（Yang et al., 2023a）的 28.62 PSNR 优势更为显著。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2408_16760/figures/004_Table_1.jpg]]
*Table 1: Comparison on Waymo Open Dataset. We compute PSNR and SSIM for both the full image and dynamic regions. Vehicle indicates regions corresponding to vehicle-related classes, while Human indicates regions corresponding to human-related classes. Box indicates methods that utilize bounding boxes for dynamic modeling. LiDAR means method using LiDAR information*

动态区域的指标差异更为突出：
- **人类区域重建**：OmniRe 达到 28.15 PSNR，StreetGS 仅 16.83 PSNR（差距 **+11.32 PSNR**），EmerNeRF 为 15.80 PSNR。这表明现有方法对行人等非刚体对象几乎完全失效。
- **车辆区域重建**：OmniRe 为 28.91 PSNR，StreetGS 为 27.73 PSNR（+1.18 PSNR），EmerNeRF 为 26.32 PSNR。刚体建模的增益相对温和，但 OmniRe 仍保持领先。
- **新视角合成（NVS）**：人类区域 NVS 上 OmniRe 达到 25.62 PSNR，StreetGS 为 22.56 PSNR（+3.06 PSNR），进一步验证了关节级建模对视角变化的鲁棒性。

定性对比（Fig.4, Fig.8）显示，OmniRe 能够恢复行人面部细节、骑行者姿态以及车辆精细纹理，而 PVG（Chen et al., 2023）等方法在动态区域产生明显模糊和伪影。LiDAR 深度可视化（Fig.5）表明 OmniRe 对人体和车辆的深度重建也更为精确。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2408_16760/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative Comparison of Novel View Synthesis. The insets highlight the details of the reconstructed dynamic objects. OmniRe manages to recover very fine details, achieving high-quality reconstruction of various common dynamic objects, including vehicles, pedestrians, and cyclists. 2024), and PVG (Chen et al., 2023). Additionally, we compare our method with NeRF-based approach EmerNeRF (Yang et al., 2023a). Among methods compared, for StreetGS (Yan et al., 2024), we use our own reimplementation. For 3DGS (Kerbl et al., 2023) and DeformableGS (Yang et al., 2023c), we use the implementation with LiDAR supervision to ensure the comparison fairness. For other methods, we use their official cod...*

### 扩展场景评估

在 32 个高动态 Waymo 场景的扩展评估（Tab.5）中，OmniRe 达到 **33.73 PSNR**，显著优于 StreetGS（29.93 PSNR，+3.80）和 EmerNeRF（31.29 PSNR，+2.44），证明了方法在更大规模数据上的泛化能力。

针对极端场景的专项对比进一步验证了 OmniRe 的鲁棒性：
- **超拥挤场景**（Tab.7）：OmniRe 保持领先，表明场景图结构能有效处理多实例密集交互。
- **夜间场景**（Tab.8）：低光照条件下 OmniRe 仍优于对比方法。
- **恶劣天气**（Tab.9）和**高速场景**（Tab.10）：OmniRe 在这些挑战性条件下均表现出稳定的性能优势。

### LiDAR 深度精度

Table 3 评估了 LiDAR 深度精度。OmniRe 在深度重建上同样优于 StreetGS 和 EmerNeRF，这得益于其显式的实例级几何建模与联合深度监督。精确的深度重建对于自动驾驶仿真中的碰撞检测和空间推理至关重要。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2408_16760/figures/008_Table_3.jpg]]
*Table 3: Evaluation of LiDAR Depth Accuracy*

### 消融实验

**非刚体建模消融**（Tab.2, Tab.14）揭示了各组件的因果贡献：
- **移除 SMPL 节点**：人类区域 PSNR 从 28.15 骤降至 24.71（-3.44），验证了基于 SMPL 的关节级建模是处理行人的核心要素。
- **移除变形节点**：人类区域 PSNR 降至 25.26（-2.89），表明共享变形网络对无模板非刚体对象（如骑行者、携带物品的行人）的建模不可或缺。
- **同时移除两者**：PSNR 进一步降至 24.71，说明两类非刚体节点存在互补关系。

**人体姿态优化消融**（Tab.2, Fig.6）：
- 移除多视角人体姿态优化导致人类区域 PSNR 从 28.15 降至 26.97（-1.18）。Fig.6 的可视化表明，未经优化的姿态在遮挡和跨视角匹配中产生明显错位，直接影响高斯绑定的准确性。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2408_16760/figures/009_Figure_6.jpg]]
*Figure 6: Ablation of Human Body Pose Refinement*

**边界框优化消融**（Tab.4, Tab.13）：
- 移除边界框优化后全图 PSNR 从 34.25 降至 33.04（-1.21）。精确的边界框为刚体节点提供了更准确的初始姿态，对整体重建质量有显著影响。

**AbsGrad 消融**（Tab.11）：
- 在所有方法上启用/禁用 AbsGrad 的对比表明，AbsGrad 带来约 +0.1 PSNR 的微小提升，属于良好实践而非 OmniRe 性能领先的决定性因素。值得注意的是，DeformableGS 在无 AbsGrad 时因显存溢出而失败。

### 失败模式与局限性

尽管 OmniRe 在多数场景下表现优异，仍存在以下局限：
1. **标注依赖**：方法依赖数据集提供的精确边界框和语义标签。在标注质量较低的场景下，实例分解和姿态初始化的准确性可能下降，泛化能力受限。
2. **光照建模缺失**：OmniRe 缺乏显式光照模型。在动态仿真中，插入的虚拟物体（如车辆、行人）与背景的光照一致性难以保证，可能影响视觉和谐度（Fig.11 的编辑示例虽展示了资产编辑能力，但光照融合问题未完全解决）。
3. **极端视角泛化**：新视角合成在训练轨迹附近表现优异，但在大幅度偏离训练视角时（如俯视或侧视极端角度），重建质量可能下降。这一问题在现有方法中普遍存在，OmniRe 未提供针对性的解决方案。

### 关键图表结论总结

| 图表 | 核心结论 |
|------|----------|
| **Tab.1** | OmniRe 全图 PSNR 34.25，人类区域 PSNR 28.15，均大幅领先 StreetGS 和 EmerNeRF |
| **Tab.2** | SMPL 节点和变形节点分别贡献 +3.44 和 +2.89 人类区域 PSNR，验证非刚体建模的关键性 |
| **Tab.5** | 32 场景扩展评估中 OmniRe 达 33.73 PSNR，证明大规模泛化能力 |
| **Fig.4** | 定性展示 OmniRe 在行人、骑行者细节恢复上的显著优势 |
| **Fig.5** | LiDAR 深度重建精度优于对比方法，对人体和车辆几何建模更准确 |
| **Fig.6** | 人体姿态优化对高斯绑定精度有直接影响，移除后出现明显错位 |
| **Tab.11** | AbsGrad 贡献微小（+0.1 PSNR），非性能领先的决定性因素 |

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2408_16760/figures/007_Table_2.jpg]]
*Table 2: Ablation on Non-Rigid Modeling*

## 定位与知识库关联

### 动态城市场景重建的演进与 OmniRe 的定位

OmniRe 处于**基于高斯泼溅的动态城市场景重建**这一快速发展的技术线上。该领域的演进可归纳为三个阶段：

1. **隐式动态场阶段**：以 **EmerNeRF**（Yang et al., 2023a）为代表，基于 NeRF 对动态驾驶场景进行整体建模，但缺乏显式的实例分解，对非刚体运动（尤其是行人）的重建精度有限。

2. **高斯场景图阶段**：**3DGS**（Kerbl et al., 2023）的提出使得显式场景表示成为可能。**HUGS**（Zhou et al., 2024）和 **StreetGS**（Yan et al., 2024）进一步构建了基于高斯的场景图，将背景、车辆等分解为独立节点。然而，这些方法的**场景图节点类型仅限于刚体**，对行人、骑行者等非刚体交通参与者缺乏专门的建模机制，仅依赖通用变形场（如 **DeformableGS**，Yang et al., 2023c）或隐式处理（如 **PVG**，Chen et al., 2023），无法捕捉关节级的人体运动细节。

3. **全类别动态场景图阶段**：OmniRe 的核心贡献在于**将场景图节点类型从刚体扩展至非刚体**，构建了包含五种节点（Sky、Background、Rigid、SMPL、Deformable）的统一框架。这一扩展并非简单的增量改进——它从根本上改变了系统对以人为中心的动态场景的建模能力。

### 关键设计决策与基线差异

| 设计维度 | StreetGS / HUGS | OmniRe | 差异的本质 |
|---------|----------------|--------|-----------|
| 非刚体人体建模 | 无关节级建模（仅通用变形场） | SMPL 动态高斯 + LBS 蒙皮 | 从“拟合表象”升级为“理解结构” |
| 无模板非刚体 | 无专门处理 | 共享变形网络 + 实例嵌入 | 覆盖行人之外的骑行、滑板等类别 |
| 人体姿态估计 | 无多视角时序优化 | 多视角 ID 匹配 + 缺失姿态插值 + 联合优化 | 从单帧估计升级为时序一致的多视角推理 |
| 场景图节点类型 | 刚体节点（+ 隐式动态区域） | 五种显式节点 | 从“车为中心”扩展为“人-车-场景”全要素 |

**证据强度**：消融实验（Tab.2）直接验证了每个设计决策的因果效应——移除 SMPL 节点导致人类区域 PSNR 骤降 3.44 dB（28.15→24.71），移除变形节点导致下降 2.89 dB（28.15→25.26），移除人体姿态优化导致下降 1.18 dB（28.15→26.97）。这些消融结果构成了强因果证据链。

### 适用边界

OmniRe 在以下条件下表现优越：
- **数据条件**：需要 Waymo 等自动驾驶数据集提供的精确 3D 边界框、语义标签和 LiDAR 深度监督。边界框优化消融（Tab.4）显示，移除该模块导致全图 PSNR 从 34.25 降至 33.04，说明标注质量直接影响性能。
- **场景类型**：针对城市驾驶场景中的常见动态实体（车辆、行人、骑行者）进行专门优化。在 32 个高动态场景上（Tab.5），OmniRe 达到 33.73 PSNR，显著优于 StreetGS（29.93）和 EmerNeRF（31.29）。
- **应用场景**：新视角合成在训练轨迹附近表现优异，且场景图结构天然支持车辆编辑、人车交互仿真等下游任务（Fig.1-c, Fig.9, Fig.11）。

### 局限与开放问题

**已知局限**（论文明确提及或可从实验推断）：

1. **标注依赖性**：依赖数据集提供的精确边界框和语义标签，在标注质量较低或完全无标注的场景下泛化能力受限。这是一个结构性约束——场景图的构建以实例检测为前提。

2. **缺乏显式光照建模**：天空节点使用环境贴图拟合，但整体框架未对场景光照进行物理建模。这意味着在动态仿真中插入虚拟物体时，难以保证其与背景在视觉上的光影和谐，限制了仿真应用的真实感上限。

3. **视角外推能力未充分验证**：所有评估均在训练轨迹附近进行，对于大幅度偏离训练视角的新视角合成鲁棒性，论文未提供实验证据。

**开放问题**（论文讨论或可从方法设计中自然引申）：

1. **自监督场景分解**：如何在无精确边界框和语义标注的情况下，实现完全自监督的动态场景分解与重建？这是将方法推广至非自动驾驶数据集的关键障碍。

2. **通用非刚体建模的泛化边界**：共享变形网络 + 实例嵌入的策略在 Waymo 数据集中有限的非刚体类别上表现良好，但其对更广泛、更极端的非刚体形变（如动物、飘动的衣物）的建模能力尚未经过验证。

3. **视觉-语言模型的集成**：论文提及可利用 GPT-4o 等模型自动分类行人类型（行人 vs. 使用代步工具的人），以减少对人工标注的依赖。这一方向的可行性及其对整体 pipeline 的影响值得探索。

4. **实时性约束**：论文未讨论推理速度。场景图结构中多种节点类型的联合优化和渲染，是否能在自动驾驶所需的实时性约束下运行，是一个工程上重要但未回答的问题。

### 在知识库中的定位

OmniRe 在动态城市场景重建知识库中占据**从“刚体为主”到“全类别动态实体”的桥梁位置**。其核心知识贡献不是单一技术的发明，而是：

- **系统集成创新**：将 SMPL 人体模型、共享变形网络、多视角姿态优化有机整合到高斯场景图框架中，证明了“为不同动态类型分配不同高斯表示”这一设计原则的有效性。
- **因果关系验证**：通过充分的消融实验，明确建立了“关节级建模→人类区域重建质量”的因果链条，为后续研究提供了清晰的设计指引。
- **应用导向**：场景图结构使重建结果天然可编辑、可仿真，为自动驾驶仿真中的以人为中心交互场景生成提供了技术基础。

## 原文 PDF

![[paperPDFs/ICLR_2025/OmniRe_Omni_Urban_Scene_Reconstruction.pdf]]
