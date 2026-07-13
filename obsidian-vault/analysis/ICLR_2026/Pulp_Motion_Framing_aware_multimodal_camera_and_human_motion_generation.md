---
title: "Pulp Motion: Framing-aware multimodal camera and human motion generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.pdf
project_link: null
code_link: https://github.com/robincourant/pulp-motion
aliases:
  - PMAS
  - PMFAMCHMG
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 辅助采样中的屏幕构图引导权重 w_z，该权重控制生成朝向高多模态一致性的倾向强度。
primary_logic: 将人体与相机的潜表示通过一个可学习的线性变换映射到屏幕构图潜空间，并在扩散采样时利用正交投影把无条件分数分解为构图相关分量，从而在不修改训练的情况下引导采样趋向多模态一致区域。
claims:
  - 辅助采样（Aux）在 DiT 和 MAR 两种架构上均一致降低构图 FID 和出画率，同时提升文本‑模态对齐分数。
  - 对于 DiT 模型，Aux 将混合子集上的 FD_framing 从 4.90 降至 3.37，Out‑rate 从 25.98% 降至 16.76%，TMR‑Score 从 23.50 升至 25.05。
  - 适中的 w_z 可在改善构图的同时保持人类与相机质量，过高则损害保真度。
  - PulpMotion 混合子集 上 FD_framing↓ / Out-rate↓ / TMR-Score↑ / CLaTr-Score↑ = 3.37 / 16.76% / 25.05 / 32.81 (DiT, (x,y)+Aux)
---

# Pulp Motion: Framing-aware multimodal camera and human motion generation

> [!tip] 核心洞察
> 将人体与相机的潜表示通过一个可学习的线性变换映射到屏幕构图潜空间，并在扩散采样时利用正交投影把无条件分数分解为构图相关分量，从而在不修改训练的情况下引导采样趋向多模态一致区域。

| 字段      | 内容                                                                                                                                                   |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | Pulp Motion：面向屏幕构图感知的多模态相机与人体运动联合生成                                                                                                                  |
| 英文题名    | Pulp Motion: Framing-aware multimodal camera and human motion generation                                                                             |
| 会议/期刊   | ICLR 2026                                                                                                                                            |
| Links   | [paper](https://arxiv.org/abs/2510.05097) · [code](https://github.com/robincourant/pulp-motion)                                                        |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method  | 辅助采样（Pulp Motion / Auxiliary Sampling）                                                                                                               |
| Dataset | PulpMotion 混合子集                                                                                                                                      |

> [!tip] 效果简介
> - PulpMotion 混合子集 上，FD_framing↓ / Out-rate↓ / TMR-Score↑ / CLaTr-Score↑ 3.37 / 16.76% / 25.05 / 32.81 (DiT, (x,y)+Aux) vs 4.90 / 25.98% / 23.50 / 30.75 (DiT, (x,y)) (-1.53 / -9.22% / +1.55 / +2.06)。
> - PulpMotion 纯子集 上，FD_framing↓ / Out-rate↓ / TMR-Score↑ / CLaTr-Score↑ 4.90 / 24.28% / 21.90 / 55.43 (MAR, (x,y)+Aux) vs 6.55 / 30.19% / 20.16 / 52.17 (MAR, (x,y)) (-1.65 / -5.91% / +1.74 / +3.26)；FD_framing↓ / Out-rate↓ / TMR-Score↑ / CLaTr-Score↑ 5.03 / 24.92% / 21.80 / 38.42 (DiT, (x,y)+Aux) vs 6.78 / 36.25% / 20.74 / 35.99 (DiT, (x,y)) (-1.75 / -11.33% / +1.06 / +2.43)。

## 概要

现有的人体运动生成与相机轨迹生成通常被作为两个独立任务处理，导致在屏幕空间中二者缺乏构图一致性——角色可能出画或出现糟糕的取景效果。Pulp Motion 针对这一瓶颈，将人体运动与相机轨迹的联合生成问题重新表述为**多模态一致性问题**，并提出一种模型无关的辅助采样框架（Auxiliary Sampling）。

核心思想是引入**屏幕构图（on‑screen framing）**作为辅助模态：通过一个可学习的线性变换 $W$，将人体与相机的潜表示映射到屏幕构图潜空间，并在扩散采样时利用正交投影 $P_{//}$ 将无条件分数分解为构图相关分量，从而在不修改训练流程的前提下引导采样趋向多模态一致区域。该框架对 DiT 和 MAR 两种扩散主干架构均适用。

在 PulpMotion 混合子集上，辅助采样将构图 FID（$\text{FD}_{\text{framing}}$）从 4.90 降至 3.37，出画率（Out‑rate）从 25.98% 降至 16.76%，同时文本‑模态对齐分数（TMR‑Score）从 23.50 提升至 25.05。适中的辅助引导权重 $w_z$ 可在改善构图的同时保持人体与相机生成质量，过高则损害保真度。

### 问题背景：电影式人‑相机关节运动生成

在电影、动画和虚拟制作中，人体运动与相机轨迹的协调配合是决定画面表现力的关键因素。相机不仅是记录工具，更是叙事语言的一部分——推拉摇移、跟拍、环绕等运镜手法与演员的动作相互呼应，共同构成屏幕空间中的视觉构图。因此，从文本描述出发，联合生成时空一致的人体运动序列与相机运动轨迹，成为多模态生成领域的重要课题。

现有工作通常将人体运动生成与相机轨迹生成视为两个独立或单向依赖的任务。例如，**DIRECTOR**（Courant et al., 2024）采用“先人体、后相机”的策略，先生成人体运动，再以此为条件生成相机轨迹。这种串行范式虽然简化了建模，却从根本上割裂了人‑相机之间的双向耦合关系——相机不仅响应人体，人体在拍摄语境下的表现同样受到相机取景的约束。

### 核心瓶颈：屏幕构图一致性的缺失

上述分离式处理的直接后果是**屏幕空间中的构图不一致**。人体运动与相机轨迹各自生成时，缺乏对最终屏幕呈现的联合约束，导致两个典型失败模式：

- **角色出画**：相机运动未能有效跟随人体，导致角色部分或全部移出画面边界；
- **糟糕的取景效果**：即使角色保持在画面内，其位置、比例和构图关系也可能不符合电影语言的基本规范，如角色被裁切在画面边缘、留白空间失衡等。

这些问题在长时序生成中尤为突出——随着时间推移，人体与相机之间的累积误差会不断放大，使生成结果在后期帧中完全偏离合理构图。

### 现有方法的局限

当前应对多模态一致性的方法主要分为两类，均存在明显不足：

1. **三模态联合生成**：直接将屏幕构图作为第三模态纳入扩散模型，学习联合分布 p(x, y, z|c)。这种方式虽然理论上能约束构图，但实际上增加了训练复杂度，且要求训练数据中必须包含构图标注，限制了方法的通用性。

2. **判别器引导采样**：如 **ReDi**（Kouzelis et al., 2025）在采样阶段引入预训练的判别器来引导生成朝向一致区域。该方法依赖额外训练的判别模型，且引导信号的质量受限于判别器自身的泛化能力。

上述方法的一个共同缺陷是**与特定模型架构或训练范式强绑定**，难以灵活迁移到不同的生成主干网络上。

### 本文动机：以辅助模态桥接多模态生成

针对上述瓶颈，Pulp Motion 提出了一种**模型无关的辅助采样框架**。其核心思想是：不直接生成屏幕构图，也不修改扩散模型的训练过程，而是将屏幕构图作为一种“辅助模态”，在推理阶段通过分数空间的投影操作，将无条件采样引导至人‑相机多模态一致的区域。

这一设计基于一个关键洞察：人体运动潜变量与相机轨迹潜变量通过一个可学习的线性变换，可以映射到屏幕构图潜空间。这意味着，即使扩散模型从未显式见过构图模态，其潜空间中天然存在一个与构图对齐的子空间。通过正交投影，可以在不改变模型参数的前提下，增强采样过程中对该子空间的偏向，从而提升生成结果的构图质量与模态间一致性。

该方法的核心优势在于：

- **训练无侵入**：辅助模态仅用于推理阶段的分数修正，无需修改训练目标或数据管线；
- **架构无关**：适用于 DiT、MAR 等不同扩散主干，无需针对特定架构调整；
- **即插即用**：通过单一的辅助引导权重 w_z 即可在构图质量与生成保真度之间实现灵活权衡。

## 核心方法与创新机理

### 问题瓶颈：屏幕构图一致性的缺失

现有工作通常将人体运动生成与相机轨迹生成视为两个独立或条件依赖的任务。例如，**(x)+DIRECTOR**（Courant et al., 2024）先独立生成人体运动，再以之为条件生成相机轨迹。这种分离式处理忽略了一个关键事实：相机轨迹与人体运动在屏幕空间中的耦合关系——即**屏幕构图（on‑screen framing）**——是评价生成质量的核心维度。若缺乏对构图的显式建模，生成的相机极易导致角色出画或产生糟糕的取景效果。

本工作的核心瓶颈洞察在于：**人‑相机联合生成的根本困难不是单模态质量不足，而是跨模态的屏幕空间一致性无法保证**。

### 核心机制：辅助模态引导的潜空间分解与采样

Pulp Motion 的核心创新并非重新设计生成架构，而是提出了一种**模型无关的辅助采样（Auxiliary Sampling）框架**，在不修改训练流程的前提下，将屏幕构图一致性注入扩散模型的推理过程。该框架由两个紧密耦合的设计组成：

#### 1. 屏幕构图潜空间的线性桥接

在训练阶段，作者设计了一个多模态自编码器（Figure 2），将人体运动 $\mathbf{x}_{\mathrm{raw}}$ 与相机轨迹 $\mathbf{y}_{\mathrm{raw}}$ 通过共享编码器 $E_\phi$ 映射到统一潜空间。关键在于，**屏幕构图 $\mathbf{z}$ 并不由独立编码器提取，而是通过一个可学习的线性变换 $W$ 从人体和相机潜变量直接映射得到**：

$$\mathbf{z} = W \left[ \mathbf{x}, \mathbf{y} \right]^{\top}$$

这一设计的意义在于：线性变换 $W$ 在训练中仅受构图重建损失的监督，被迫学习人体‑相机潜变量到屏幕构图的线性映射关系。这为后续采样中的正交投影提供了数学基础——**$W$ 的行空间张成的子空间，恰好对应于潜空间中影响屏幕构图的方向**。

#### 2. 辅助采样中的正交投影引导

推理时，标准分类器自由引导（CFG）的噪声预测公式为：

$$\tilde{\varepsilon}_{\theta}(\mathbf{x}_t, \mathbf{y}_t, \mathbf{c}, t) = \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t) + w_c (\varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \mathbf{c}, t) - \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t))$$

辅助采样的核心修改在于**对无条件项进行正交分解**（Figure 3）。将联合潜变量 $\mathbf{u} = [\mathbf{x}, \mathbf{y}]^{\top}$ 分解为两个正交分量：
- $\mathbf{u}_{//}$：平行于 $W$ 行空间的构图相关分量
- $\mathbf{u}_{\perp}$：正交于 $W$ 行空间的构图无关分量

修改后的采样公式为：

$$\tilde{\varepsilon}_{\theta}(\mathbf{x}_t, \mathbf{y}_t, \mathbf{c}, t) = \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t) + w_z P_{//} \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t) + w_c (\varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \mathbf{c}, t) - \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t))$$

其中 $P_{//}$ 是向构图相关子空间的正交投影矩阵，$w_z$ 是新增的**辅助引导权重**。这一公式的直觉是：通过 $w_z P_{//} \varepsilon_\theta(\emptyset)$ 项，在无条件分数中额外增强构图相关方向的分量，从而将采样过程“推向”多模态一致性更高的区域。

### 相对于基线的关键差异（Changed Slots）

| 维度        | 基线方法                                 | Pulp Motion (Aux)                          |
| --------- | ------------------------------------ | ------------------------------------------ |
| **采样公式**  | 标准 CFG，仅含无条件项和文本条件项                  | 在无条件项中引入 $w_z P_{//}$ 加权分量，通过辅助权重调控构图一致性强度 |
| **构图建模**  | 无显式构图监督（(x,y)联合生成）或直接作为第三模态（(x,y,z)） | 构图仅作为辅助模态，通过线性变换 $W$ 桥接，不参与扩散训练            |
| **训练依赖**  | (x,y,z) 需要三模态联合训练                    | 辅助模态仅在自编码器阶段用于学习 $W$，扩散模型训练与 (x,y) 完全相同    |
| **架构兼容性** | 依赖特定架构设计                             | **模型无关**，已验证兼容 DiT 和 MAR 两种架构              |

### 创新本质总结

Pulp Motion 的本质创新在于**将多模态一致性问题转化为潜空间中的几何引导问题**。它不试图让扩散模型直接学习构图约束，而是利用自编码器阶段学到的线性映射 $W$，在推理时通过正交投影将构图信息作为“免费”的引导信号注入采样过程。这种“训练时隐式学习映射，推理时显式几何引导”的策略，使得方法兼具**架构无关性**（不修改扩散主干）、**训练高效性**（无需额外训练扩散模型）和**即插即用性**（仅需调整单一超参数 $w_z$）。

Pulp Motion 提出一种**模型无关的辅助采样框架**，在不修改扩散模型训练的前提下，增强人体运动与相机轨迹生成之间的多模态一致性。其核心思路是引入一个辅助模态——屏幕构图（on‑screen human framing）——作为“桥梁”，在推理时引导采样过程趋向人‑相机高度协调的区域。

### 核心瓶颈与解决思路

现有工作通常将人体运动生成与相机轨迹生成视为独立任务，或采用先人体后相机的级联方式（如 **(x)+DIRECTOR**, Courant et al., 2024）。这种做法忽略了二者在屏幕空间中固有的耦合关系：相机的移动直接影响人体在画面中的位置、大小和完整性，反之亦然。独立处理极易导致角色出画、取景不佳等构图失败。

Pulp Motion 的核心洞察在于：**屏幕构图天然是人‑相机关系的显式表达**。将人体关节通过相机参数投影到二维屏幕，得到的屏幕构图 $z$ 同时蕴含了人体姿态和相机位姿的信息。因此，$z$ 可以作为连接人体潜变量 $x$ 与相机潜变量 $y$ 的辅助模态，在采样时提供多模态一致性信号。

现有工作通常将人体运动生成与相机轨迹生成视为独立任务，或采用先人体后相机的级联方式。这种做法忽略了二者在屏幕空间中固有的耦合关系：相机的移动直接影响人体在画面中的位置、大小和完整性，反之亦然。独立处理极易导致角色出画、取景不佳等构图失败。

Pulp Motion 的核心洞察在于：**屏幕构图天然是人‑相机关系的显式表达**。将人体关节通过相机参数投影到二维屏幕，得到的屏幕构图 $z$ 同时蕴含了人体姿态和相机位姿的信息。因此，$z$ 可以作为连接人体潜变量 $x$ 与相机潜变量 $y$ 的辅助模态，在采样时提供多模态一致性信号。

### 整体 Pipeline

框架由两个阶段构成：**多模态潜空间学习**（训练阶段）和**辅助采样**（推理阶段）。

#### 阶段一：多模态潜空间学习

1. **共享编码**：将原始人体运动 $\mathbf{x}_{\mathrm{raw}}$ 和相机轨迹 $\mathbf{y}_{\mathrm{raw}}$ 拼接后送入共享编码器 $E_{\phi}$，得到统一潜空间中的联合表示 $[\mathbf{x}, \mathbf{y}]^{\top}$。共享编码确保了两种模态在潜空间中的对齐。

2. **辅助模态映射**：通过一个可学习的线性变换 $W$，将联合潜表示映射为屏幕构图潜变量：
   $$\mathbf{z} = W \left[ \mathbf{x}, \mathbf{y} \right]^{\top}$$
   值得注意的是，屏幕构图**从不直接编码**，而是完全通过线性变换从人体和相机潜变量中派生，仅通过重构损失进行监督。

3. **三路解码**：三个独立解码器 $D_{\psi_x}$、$D_{\psi_y}$、$D_{\psi_z}$ 分别重构原始人体运动、相机轨迹和屏幕构图。训练损失为三者的均方误差之和：
   $$\mathcal{L}_{\mathrm{AE}} = \| D_{\psi_x}(\cdots) - \mathbf{x}_{\mathrm{raw}} \|^2 + \| D_{\psi_y}(\cdots) - \mathbf{y}_{\mathrm{raw}} \|^2 + \| D_{\psi_z}(W \cdots) - \mathbf{z}_{\mathrm{raw}} \|^2$$

4. **扩散模型训练**：在学到的潜空间上，以标准 DDPM 方式训练文本条件化的扩散模型（支持 DiT 和 MAR 两种架构）：
   $$\mathcal{L}_{\mathrm{noise}}(\theta) = \mathbb{E}_{t, \varepsilon_{xy}} \left[ \| \varepsilon_{xy} - \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \mathbf{c}) \|^2 \right]$$
   该阶段不涉及辅助模态 $z$ 的扩散训练。

#### 阶段二：辅助采样（推理阶段）

推理时，框架在标准分类器自由引导（CFG）的基础上引入**辅助引导项**，核心操作如下：

1. **正交分解**：将联合潜变量 $\mathbf{u} = [\mathbf{x}, \mathbf{y}]^{\top}$ 分解为两个正交分量——与辅助模态 $z$ 平行的分量 $\mathbf{u}_{//}$ 和垂直分量 $\mathbf{u}_{\perp}$（详见 Figure 3）。

2. **分数修正**：在每一步去噪中，将无条件分数投影到平行方向，并通过辅助权重 $w_z$ 进行缩放，最终噪声预测公式为：
   $$\tilde{\varepsilon}_{\theta}(\mathbf{x}_t, \mathbf{y}_t, \mathbf{c}, t) = \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t) + w_z P_{//} \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t) + w_c (\varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \mathbf{c}, t) - \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t))$$
   其中 $P_{//}$ 为投影矩阵，$w_c$ 为文本引导权重。该公式在保留文本条件控制的同时，通过 $w_z P_{//}$ 项将采样推向人‑相机构图一致的区域。

### 关键调控参数

辅助引导权重 $w_z$ 是框架的核心调控旋钮。适中的 $w_z$ 能够显著改善屏幕构图质量（降低 FD_framing 和出画率）并提升文本‑模态对齐分数；但过高的 $w_z$ 会过度约束生成空间，损害人体运动和相机轨迹的保真度（详见 Table 5、Table 9 的消融实验）。这一权衡关系是该框架在实际应用中的主要调参焦点。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2510_05097/figures/008_Table_5.jpg]]
*Table 5: Auxiliary guidance ablation on the mixed subset. We vary the auxiliary guidance weight wz to evaluate its effect on the framing, camera and human metrics. Results are reported for DiT (Peebles & Xie, 2023) and MAR (Li et al., 2024). Superscript ± denotes the 95% confidence interval over 10 samplings. To assess controllability and effectiveness of auxiliary sampling, we ablate in Table 5 the auxiliary guidance weight $w _ { z }$ (Eq (8)) on both DiT and MAR. We see that a (1) moderate guidance weight improves framing and text–modality alignment. On DiT, increasing $w _ { z }$ from 0.00 to 0.25 reduces $\mathrm { F D } _ { \mathrm { f r a m i n g } }$ 4 . 9 0 3 . 3 7 and Out-rate 25.98→16.76; on MA...

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2510_05097/figures/020_Table_9.jpg]]
*Table 9: Auxiliary guidance ablation on the pure subset. We vary the auxiliary guidance weight wz to evaluate its effect on the framing, camera and human metrics. Results are reported for DiT (Peebles & Xie, 2023) and MAR (Li et al., 2024). Superscript ± denotes the 95% confidence interval over 10 samplings*

### 模块关系总结

| 模块               | 功能                   | 作用阶段    |
| ---------------- | -------------------- | ------- |
| 共享编码器 $E_{\phi}$ | 将人体与相机原始数据编码到统一潜空间   | 训练      |
| 线性变换 $W$         | 从联合潜变量映射到屏幕构图潜变量     | 训练      |
| 三路解码器 $D_{\psi}$ | 分别重构三种模态的原始表示        | 训练      |
| 扩散生成主干           | 在潜空间进行文本条件化的去噪扩散     | 训练 + 推理 |
| 辅助采样模块           | 通过 $P_{//}$ 投影修正采样分数 | 仅推理     |

整个框架的模型无关性体现在：辅助采样仅修改推理时的分数计算，不依赖特定的扩散架构，也不需要在训练阶段引入辅助模态的扩散建模。这一设计使其可以即插即用地应用于 DiT 和 MAR 等不同生成主干。

### 多模态潜空间构建

Pulp Motion 的核心架构围绕一个共享的多模态自编码器展开，其目标是将人体运动 $\mathbf{x}_{\mathrm{raw}}$ 与相机轨迹 $\mathbf{y}_{\mathrm{raw}}$ 编码到统一的潜空间中，并显式地引入屏幕构图作为辅助模态 $\mathbf{z}$。

**共享编码器 $E_\phi$** 对人体运动和相机轨迹进行联合编码，而非独立处理两个模态。这种设计使两个模态在潜空间中自然对齐，为后续的跨模态一致性引导奠定基础。

**线性变换 $W$** 是连接主模态与辅助模态的关键桥梁。给定编码后的联合潜变量 $[\mathbf{x}, \mathbf{y}]^\top$，屏幕构图潜变量通过一个可学习的线性映射得到：

$$\mathbf{z} = W \left[ \mathbf{x}, \mathbf{y} \right]^{\top}$$

值得注意的是，屏幕构图 $\mathbf{z}_{\mathrm{raw}}$ 从不被直接编码；它完全通过线性变换 $W$ 从人体和相机潜变量推导而来，仅通过重构损失进行监督。这种设计确保辅助模态的信息来源于主模态本身，而非外部注入。

**三路解码器 $D_\psi$** 分别负责重构三个模态：人体运动解码器 $D_{\psi_x}$、相机轨迹解码器 $D_{\psi_y}$ 和屏幕构图解码器 $D_{\psi_z}$。整个自编码器的训练目标是最小化三个模态的重构均方误差：

$$\mathcal{L}_{\mathrm{AE}} = \| D_{\psi_x}(\cdots) - \mathbf{x}_{\mathrm{raw}} \|^2 + \| D_{\psi_y}(\cdots) - \mathbf{y}_{\mathrm{raw}} \|^2 + \| D_{\psi_z}(W \cdots) - \mathbf{z}_{\mathrm{raw}} \|^2$$

### 扩散生成主干

在潜空间中，人体运动和相机轨迹的联合生成通过去噪扩散模型实现。给定文本条件 $\mathbf{c}$，模型学习预测添加到联合潜变量上的噪声：

$$\mathcal{L}_{\mathrm{noise}}(\theta) = \mathbb{E}_{t, \varepsilon_{xy}} \left[ \| \varepsilon_{xy} - \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \mathbf{c}) \|^2 \right]$$

该主干支持 DiT 和 MAR 两种架构，体现了方法的模型无关性。

### 辅助采样机制

辅助采样是 Pulp Motion 的核心创新，它在推理时修改扩散模型的分数估计，引导生成朝向多模态一致性更高的区域，而无需重新训练模型。

**正交分解原理**：联合潜变量 $\mathbf{u} = [\mathbf{x}, \mathbf{y}]^\top$ 被分解为两个正交分量——平行于辅助模态 $\mathbf{z}$ 的分量 $\mathbf{u}_{//}$ 和垂直于 $\mathbf{z}$ 的分量 $\mathbf{u}_\perp$。辅助采样的目标是增强 $\mathbf{u}_{//}$ 方向的生成倾向，从而提升人与相机在屏幕空间中的构图一致性。

**修正的噪声预测公式**：推理时使用的噪声估计结合了无条件项、辅助引导项和文本条件项：

$$\tilde{\varepsilon}_{\theta}(\mathbf{x}_t, \mathbf{y}_t, \mathbf{c}, t) = \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t) + w_z P_{//} \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t) + w_c (\varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \mathbf{c}, t) - \varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t))$$

其中：
- $\varepsilon_\theta(\mathbf{x}_t, \mathbf{y}_t, \emptyset, t)$ 为无条件噪声预测；
- $P_{//}$ 为投影矩阵，将无条件分数投影到与辅助模态 $\mathbf{z}$ 平行的子空间；
- $w_z$ 为辅助引导权重，控制朝向构图一致性区域的倾向强度；
- $w_c$ 为标准分类器自由引导（CFG）的文本条件权重。

**关键设计选择**：辅助模态 $\mathbf{z}$ 在训练阶段完全不被扩散模型所见，仅在推理时通过投影矩阵 $P_{//}$ 隐式地影响采样方向。这使得方法可以即插即用地应用于任何已训练好的联合扩散模型，无需修改训练流程或引入额外预训练模型。

### 因果调控变量

辅助引导权重 $w_z$ 是方法中唯一的推理时调控变量。适中的 $w_z$ 可在显著改善屏幕构图质量（降低 FD_framing 和出画率）的同时保持人体运动与相机轨迹的生成保真度；过高的 $w_z$ 会过度约束生成空间，导致保真度下降。该权衡关系在 DiT 和 MAR 两种架构上均得到验证（Table 5, Table 9），构成了方法实际部署中需要手动调节的核心超参数。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2510_05097/figures/009_Figure_8.jpg]]
*Figure 8: $\colon$ ~ $w _ { z }$ ablation in DiT on the mixed set. Framing quality and modality-text alignment for c guidance ranges from 4 to 12. The optimal region is at the bottom-right (low framing FD, high alignment). Figure 9: wz ablation in MAR on the mixed set. Framing quality and modality-text alignment for c guidance ranges from 1 to 5. The optimal region is at the bottom-right (low framing FD, high alignment)*


## 实验与关键发现

### 主实验结果

Pulp Motion 在两个核心指标维度上验证了辅助采样（Aux）的有效性：屏幕构图质量（FD_framing↓、Out-rate↓）和多模态文本对齐（TMR-Score↑、CLaTr-Score↑）。实验在 PulpMotion 数据集的混合子集（mixed subset）和纯子集（pure subset）上分别进行，覆盖 DiT 和 MAR 两种扩散主干架构。

**混合子集上的表现。** 在 DiT 架构下，双模态联合生成 `(x, y)` 本身已优于独立模态生成 `(x)(y)` 和三模态联合生成 `(x, y, z)`，而辅助采样 `(x, y)+Aux` 在此基础上进一步将 FD_framing 从 4.90 降至 3.37，出画率（Out-rate）从 25.98% 降至 16.76%，同时将 TMR-Score 从 23.50 提升至 25.05，CLaTr-Score 从 30.75 提升至 32.81（Table 4）。这表明辅助采样在不修改训练的前提下，显著提升了人与相机在屏幕空间中的构图一致性。

与先独立生成人体运动再以之为条件生成相机轨迹的 `(x)+DIRECTOR`（Courant et al., 2024）相比，`(x, y)+Aux` 在所有四项指标上均取得更优结果。基于判别器引导的多模态采样方法 ReDi（Kouzelis et al., 2025）在构图指标上表现尚可，但其文本对齐分数显著低于本方法。

**纯子集上的表现。** 纯子集仅包含人体完全在画面内的样本，构图挑战相对较小，但辅助采样仍带来一致增益。在 DiT 架构下，`(x, y)+Aux` 将 FD_framing 从 6.78 降至 5.03，出画率从 36.25% 降至 24.92%（Table 8）。在 MAR 架构下，FD_framing 从 6.55 降至 4.90，出画率从 30.19% 降至 24.28%。文本对齐指标同样获得提升：MAR 上的 TMR-Score 从 20.16 升至 21.90，CLaTr-Score 从 52.17 升至 55.43。

**跨架构一致性。** 辅助采样在 DiT 和 MAR 两种架构上均表现出稳定的正向增益，验证了该方法的模型无关性（model-agnostic）。值得注意的是，三模态联合生成 `(x, y, z)` 在多数指标上反而不如双模态 `(x, y)`，说明直接将屏幕构图作为生成模态引入训练并非最优方案，而辅助采样的“仅在推理时引导”策略更为有效。

### 消融实验

**辅助引导权重 w_z 的影响。** 控制辅助采样强度的关键参数是 w_z。在混合子集上，随着 w_z 从 0 逐渐增大，FD_framing 和出画率持续下降，TMR-Score 和 CLaTr-Score 持续上升，在 DiT 上约 w_z=2.0、MAR 上约 w_z=1.0 时达到综合最优（Table 5）。然而，过高的 w_z 会导致人体运动和相机轨迹的生成保真度下降——具体表现为 FD_TMR 和相机相关指标的劣化（Table 5, Table 9）。这一现象在纯子集上的消融中同样得到验证（Table 9, Figure 8, Figure 9, Figure 19, Figure 20）。核心规律是：适度的辅助引导在改善构图一致性的同时保持了生成质量，过强引导则迫使采样偏离真实数据分布，损害保真度。

**模态联合方式的影响。** 对比独立模态生成 `(x)(y)` 与双模态联合生成 `(x, y)` 发现，联合生成本身就能带来更好的模态间对齐，而 Aux 在两种设置下均能带来进一步提升（Figure 21-24, Appendix E.2.5）。这表明辅助采样的增益并非仅来自联合训练，而是源于其独特的“构图空间投影引导”机制。

### 失败模式与局限性

1. **w_z 的手动调参瓶颈。** 辅助采样性能对 w_z 敏感，当前需要人工为不同架构和数据集子集分别调参，缺乏自适应机制。
2. **精细构图控制的缺失。** 方法目前仅关注人体整体在画面中的位置，不支持对特定身体部位（如手部、面部）的精细构图控制。
3. **场景假设限制。** 方法针对单人单相机场景设计，无法直接处理多人交互或多相机切换的复杂摄影场景。
4. **物理约束的缺失。** 未显式建模碰撞、遮挡等物理关系，在复杂交互场景下可能产生不真实的生成结果。

### 阅读疑问与待核查点

1. **对比实验实现细节仍然偏笼统。** Table 4 与 Table 8 同时比较 `(x)+DIRECTOR`、`(x)(y)`、`(x, y)`、`(x, y, z)`、ReDi 和 `(x, y)+Aux`，但正文与 Appendix E.2.1 主要给出方法类别、模型规模和统一训练步数，缺少足够细的 baseline 适配细节。因此目前较难判断各 baseline 是否完全公平，尤其包括：`(x)+DIRECTOR` 如何适配到 PulpMotion 的文本、人和相机条件；`(x)(y)`、`(x, y)`、`(x, y, z)` 是否共享同一自编码器、潜空间和调参预算；ReDi 的判别器/表示引导如何训练、选择权重并与 Aux 的调参预算对齐；以及不同方法在文本引导权重 `w_c` 和辅助权重 `w_z` 上是否采用相同的模型选择规则。
2. **`full`、`pure subset`、`mixed subset` 的划分口径未被清晰定义。** Appendix D 的 Table 6 写明比较 PulpMotion 的 `full (all)`、`pure` 和 `mixed` 子集，但正文没有显式说明三者的过滤规则。当前可确认的是：`full/all` 指 PulpMotion 全量统计；`pure` 和 `mixed` 是用于重建与生成实验的两个公开 split，HF 数据集 `robin-courant/pulpmotion-data` 中包含 `mixed_train_split.txt`、`mixed_test_split.txt`、`pure_train_split.txt`、`pure_test_split.txt` 等文件；4090 上通过镜像探测到 mixed train/test 分别约 94k/10.5k 条，pure train/test 分别约 36.6k/4.1k 条。结合正文对出画、近景和 out-of-screen body parts 的描述，可暂时推断 `pure` 更偏向人体完整在画面内的样本，`mixed` 包含完整入画与部分出画/近景等更复杂构图样本；但精确过滤规则仍需要从代码或数据 metadata 进一步核查，不能仅凭论文表述下定论。

### 关键图表结论

- **Table 4 & Table 8：** 辅助采样在混合和纯子集上一致超越所有基线，证明其通用性和有效性。
- **Table 5 & Table 9：** w_z 消融揭示了构图质量与生成保真度之间的权衡关系，为实际部署提供了调参参考。
- **Figure 4 & Figure 5：** 在 DiT 和 MAR 上分别展示了不同 w_z 下构图 FD 与文本对齐分数的 Pareto 前沿，直观呈现了最优 w_z 区间。
- **Figure 10：** 数据集精炼管线展示了从原始视频提取到人体姿态修复的完整流程，是 PulpMotion 数据集质量的基础保障。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2510_05097/figures/006_Table_4.jpg]]
*Table 4: State-of-the-art comparison on the mixed subset. We compare five baselines: human-conditioned camera generation (x)+DIRECTOR Courant et al. (2024), independent modality generation (x)(y), dualmodality generation (x, y), triplet-modality generation (x, y, z), and ReDi (Kouzelis et al., 2025), along with our auxiliary sampling (Aux). Results are reported for DiT (Peebles & Xie, 2023) and MAR (Li et al., 2024). Superscript ± denotes the 95% confidence interval over 10 samplings*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2510_05097/figures/010_Figure_10.jpg]]
*Figure 10: Dataset refinement pipeline. Given RGB frames from a video, we first estimate the camera and human pose. We then identify the out-of-screen body parts by reprojection. Finally, we refine the out-of-screen parts using a generative prior*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2510_05097/figures/018_Table_8.jpg]]
*Table 8: State-of-the-art comparison on the pure subset. We compare five baselines: human-conditioned camera generation (x)+DIRECTOR Courant et al. (2024), independent modality generation (x)(y), dualmodality generation (x, y), triplet-modality generation (x, y, z), and ReDi Kouzelis et al. (2025), along with our auxiliary sampling (Aux) method. Results are reported for DiT (Peebles & Xie, 2023) and MAR (Li et al., 2024). Superscript ± denotes the 95% confidence interval over 10 samplings*

## 定位与知识库关联

### 1. 问题定位：从独立生成到多模态一致性

人体运动生成与相机轨迹生成在电影、游戏和虚拟现实中有广泛需求，但现有工作普遍将二者视为独立任务。这种解耦策略虽降低了建模复杂度，却引入了严重的屏幕空间不一致问题——生成的人体运动可能与相机运动不匹配，导致角色频繁出画或出现糟糕的取景效果。Pulp Motion 正是针对这一瓶颈而提出。

### 2. 基线方法谱系

论文系统比较了五类基线，构成一条从“完全解耦”到“显式联合”的方法谱系：

**（1）条件生成基线：(x)+DIRECTOR**
先独立生成人体运动 x，再以 x 为条件生成相机轨迹 y。该方法来自 **DIRECTOR**（Courant et al., 2024），本质上仍将生成过程分解为两个阶段，缺乏反向约束，相机无法反过来影响人体运动。

**（2）独立模态生成：(x)(y)**
人体运动和相机轨迹完全分开生成，没有任何模态间交互。这是最极端的解耦方案，出画率最高。

**（3）双模态联合生成：(x, y)**
直接学习联合分布 p(x, y | c)，在训练时建立模态间的统计依赖。相较于 (x)(y)，这一方案能更好地捕捉模态间对齐关系，是 Pulp Motion 辅助采样的基础模型。

**（4）三模态联合生成：(x, y, z)**
在双模态基础上，将屏幕构图 z 作为第三模态直接纳入扩散生成。这一方案试图通过增加显式的构图监督来改善一致性，但需要修改训练流程。

**（5）判别器引导采样：ReDi**
**ReDi**（Kouzelis et al., 2025）是一种基于判别器的多模态采样方法，通过在推理时引入判别器信号来引导生成朝向更一致的方向。与 Pulp Motion 的辅助采样类似，ReDi 也试图在不重新训练主干网络的情况下改善多模态一致性，但其依赖额外的判别器训练。

### 3. 方法定位与核心差异

Pulp Motion 的核心贡献——**辅助采样（Auxiliary Sampling）**——在方法谱系中占据了一个独特位置：

- **相较于 (x)(y) 和 (x)+DIRECTOR**：辅助采样不再将模态间关系视为单向条件，而是通过共享潜空间和正交投影实现双向一致性引导。
- **相较于 (x, y, z)**：辅助采样不需要在训练时引入第三模态，屏幕构图 z 仅通过一个可学习的线性变换 W 从人体/相机潜变量中派生，训练成本与双模态生成相同。
- **相较于 ReDi**：辅助采样不需要训练额外的判别器，其引导信号完全来自自编码器中已学到的线性变换 W，实现更轻量。

核心机制可概括为：在标准分类器自由引导（CFG）的无条件项中，引入一个沿屏幕构图方向的正交投影分量 P_{//}，通过辅助权重 w_z 控制引导强度。这一设计的精巧之处在于，它利用了自编码器训练阶段已经学到的潜空间几何结构——W 将人体/相机潜变量映射到构图潜空间，而 P_{//} 则提取与构图相关的子空间分量——无需任何额外的训练或模型修改。

### 4. 适用边界与局限

**（1）辅助引导权重的调参依赖**
w_z 是平衡构图质量与生成保真度的关键旋钮。消融实验表明，适中的 w_z 能在显著改善构图 FID 和出画率的同时保持人体与相机质量，但过高的 w_z 会损害保真度。目前该权重需要手动调节，缺乏自适应机制。

**（2）场景与主体限制**
方法针对单人-单相机的电影式生成场景设计，不直接适用于多人交互或复杂多相机设置。此外，屏幕构图仅通过关键关节的 2D 投影定义，不支持对特定身体部位（如面部、手部）的精细构图控制。

**（3）物理约束的缺失**
方法未显式建模物理约束（如碰撞检测、遮挡关系、地面接触），在复杂交互场景下可能产生不真实的结果。

**（4）数据偏见风险**
PulpMotion 数据集基于 CondensedMovies 视频自动提取，依赖 TRAM 进行 3D 人体-相机姿态估计，并使用 Qwen2.5-VL 自动生成文本描述。这一管线可能引入：
- 姿态估计误差在出画场景下的累积；
- VLM 标注中的语言与视觉偏见；
- 数据集在人种、体型和摄影风格上的覆盖偏差。

### 5. 开放问题

1. **自适应引导**：能否学习一个依赖于时间步 t、文本条件 c 和当前噪声状态的自适应 w_z，替代人工调参？这类似于 CFG 中动态引导权重的思想。

2. **辅助模态框架的泛化**：辅助采样的核心思想——利用一个可线性映射的辅助模态来引导采样——是否适用于其他多模态生成任务？例如，在视频-音频联合生成中，可将音频能量包络作为辅助模态引导视频的节奏一致性。

3. **更丰富的构图空间**：当前构图仅定义为关键关节的 2D NDC 坐标。是否可以引入更结构化的构图表示（如三分法、引导线、头部空间等电影摄影规则）作为辅助模态，实现艺术层面的构图控制？

4. **多主体与多相机扩展**：在多人场景中，屏幕构图需同时考虑多个主体的空间关系；在多相机设置中，不同机位之间存在约束。如何将辅助采样的正交投影机制推广到这些高维约束空间，是一个具有挑战性的开放方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.pdf]]
