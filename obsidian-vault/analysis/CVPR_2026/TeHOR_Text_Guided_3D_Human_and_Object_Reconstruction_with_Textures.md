---
title: "TeHOR: Text-Guided 3D Human and Object Reconstruction with Textures"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TeHOR_Text_Guided_3D_Human_and_Object_Reconstruction_with_Textures.pdf
project_link: "https://hygenie1228.github.io/TeHOR/"
code_link: null
aliases:
- TeHOR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 利用文本描述作为语义引导，通过预训练扩散模型（StableDiffusion）监督渲染外观与文本的对齐，将全局语境和外观线索注入优化过程，从而驱动三维重建同时捕捉接触与非接触交互。
primary_logic: 将文本-图像对齐的先验知识作为三维人体与物体重建的语义约束，通过多视角渲染与分数蒸馏采样（SDS）损失，使重建结果在几何和纹理上服从于文本描述的整体交互语境，实现超越物理接触的语义级交互推理。
claims:
- 去除外观损失会导致重建结果无法捕捉整体交互语境，产生不合理的空间关系（Table 2 第一行）。
- 文本引导优化显著降低 Chamfer 距离并提高接触分数（Table 1：优化前 CD_human 5.252 → 4.941，CD_object 31.268 → 16.701）。
- 核心优势在于由文本引导的整体交互推理，而非精确的接触预测（Table S3 替换接触预测仍有良好表现）。
- 与非接触场景中，TeHOR 显著优于所有依赖接触的方法（Table 5：CD_human 4.958, CD_object 17.546）。
---

# TeHOR: Text-Guided 3D Human and Object Reconstruction with Textures

> [!tip] 核心洞察
> 将文本-图像对齐的先验知识作为三维人体与物体重建的语义约束，通过多视角渲染与分数蒸馏采样（SDS）损失，使重建结果在几何和纹理上服从于文本描述的整体交互语境，实现超越物理接触的语义级交互推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | TeHOR: 基于文本引导的带纹理三维人体与物体联合重建 |
| 英文题名 | TeHOR: Text-Guided 3D Human and Object Reconstruction with Textures |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.19679) · [Project](https://hygenie1228.github.io/TeHOR/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | TeHOR |
| Dataset | Open3DHOI, BEHAVE |

> [!tip] 效果简介
> - Open3DHOI 上，CD_human (cm) 4.941 vs 5.111 (HOI-Gaussian) (-0.170 (3.3%))；CD_object (cm) 16.701 vs 19.363 (HOI-Gaussian) (-2.662 (13.7%))；Contact F1 0.412 vs 0.392 (InteractVLM) (+0.020 (5.1%))。
> - BEHAVE 上，CD_human (cm) 5.615 vs 5.748 (HOI-Gaussian) (-0.133 (2.3%))；CD_object (cm) 17.339 vs 19.197 (InteractVLM) (-1.858 (9.7%))。
> - Open3DHOI (non-contact) 上，CD_human (cm) 4.958 vs 5.111 (HOI-Gaussian, general) (-0.153 (3.0%))。

## 概述

三维人体与物体联合重建旨在从单张图像中恢复交互场景的几何与纹理，但现有方法普遍**过度依赖物理接触信息**来推断空间关系，难以捕捉注视、指向等非接触交互，且仅基于局部几何接近度驱动优化，忽视人体与物体的全局外观上下文，导致重建结果在视觉上不合理。

针对这一瓶颈，本文提出 **TeHOR**（Text-guided 3D Human and Object Reconstruction），其核心思路是**利用文本描述作为语义引导**，通过预训练扩散模型（Stable Diffusion）监督渲染外观与文本的对齐，将全局语境和外观线索注入优化过程，从而驱动三维重建同时捕捉接触与非接触交互。方法的决定性洞察在于：将文本-图像对齐的先验知识作为三维人体与物体重建的语义约束，通过多视角渲染与分数蒸馏采样（SDS）损失，使重建结果在几何和纹理上服从于文本描述的整体交互语境，实现超越物理接触的语义级交互推理。

在 Open3DHOI 与 BEHAVE 两个基准数据集上，TeHOR 在 Chamfer 距离和接触 F1 分数上均取得最优或次优结果。消融实验表明，**移除外观损失**会导致物体 Chamfer 距离从 16.701 cm 恶化至 22.094 cm，且重建缺乏整体语境；**移除文本条件**同样使物体 Chamfer 距离升至 20.348 cm，验证了文本引导对隐式交互（如视线方向）的纠正作用。尤其在非接触场景中，TeHOR 显著优于所有依赖接触的方法，证实其核心优势在于由文本引导的整体交互推理，而非精确的接触预测。

## 背景与动机

从单张图像重建三维人体与物体的联合表示是理解人类行为、构建数字内容的核心技术。其关键挑战在于：**单张二维图像仅提供单一视角的投影，缺失了深度、遮挡区域以及交互语义等多重信息**。现有方法通过引入物理接触线索来弥补这一信息缺口——它们预测或标注人体与物体的接触区域，并基于局部几何接近度驱动优化，从而推断二者的空间关系。

然而，这种“接触驱动”范式存在根本性瓶颈。**接触信息本质上只能刻画物理触碰，无法捕捉大量非接触交互场景中的语义关系**，例如注视、指向、交谈等。在这些场景中，人体的空间定位并非由接触约束决定，而是由更高层次的交互意图驱动。更关键的是，现有方法仅依赖局部几何接近度来拟合接触，忽视了人体与物体的全局外观上下文——例如，一个“手持手机”的场景中，即使手部与手机存在接触，若头部朝向错误方向，重建结果在视觉上仍然不合理。

图 Figure 2 直观展示了这一困境：依赖接触预测的方法（如 InteractVLM）在非接触场景中会因错误的接触估计而导致空间关系崩溃；而在接触场景中，缺乏全局语境约束也会产生语义上不合理的重建。**问题的本质在于，物理接触只是交互的表征之一，而非交互本身**。

TeHOR 的核心动机由此产生：**能否用更丰富的语义信号替代或补充物理接触，来驱动三维人体与物体的联合重建？** 文本描述天然地编码了交互的整体语境——它不仅包含了“谁接触了谁”，还包含了“如何交互”、“交互的意图是什么”等语义信息。同时，预训练的文本-图像生成模型（如 StableDiffusion）已经内化了从文本到视觉外观的强先验知识。因此，一个自然的思路是：将文本描述作为语义引导，通过预训练扩散模型监督渲染外观与文本的对齐，从而将全局语境和外观线索注入优化过程，驱动三维重建同时捕捉接触与非接触交互。

这一思路将三维重建问题从“物理约束拟合”提升为“语义对齐优化”，为处理复杂交互场景开辟了新的可能。

## 核心创新

### 问题瓶颈：从物理接触到语义交互的鸿沟

现有三维人体与物体联合重建方法（如 **PHOSA** (Zhang et al., ECCV 2020)、**LEMON + PICO** (Yang et al., CVPR 2024; Cseke et al., CVPR 2025)、**InteractVLM** (Dwivedi et al., CVPR 2025)、**HOI-Gaussian** (Wen et al., CVPR 2025)）的核心瓶颈在于**过度依赖物理接触信息**来推断人体与物体的空间关系。这些方法通过预测接触图或手动标注接触区域，以局部几何接近度（接触损失）驱动优化，从而将人体拉向物体表面。然而，这种范式存在两个根本缺陷：

1. **无法捕捉非接触交互**：对于注视、指向、交谈等不存在物理接触的交互场景，接触驱动的优化缺乏有效的空间约束信号，导致重建结果在空间关系上完全失效。
2. **忽视全局外观上下文**：仅基于局部几何距离的优化忽略了人体与物体的整体外观线索（如视线方向、身体朝向、物体功能属性），导致重建结果虽然在局部几何上可能满足接触约束，但在视觉上却不合理——例如，人物面向错误方向使用物体。

Figure 2 直观展示了这一瓶颈：现有方法因接触预测错误或接触信息缺失而产生不合理的空间排列，而 TeHOR 通过文本描述的全局语义引导，能够推理出正确的交互姿态。

### 核心因果机制：文本作为语义引导信号

TeHOR 的核心创新在于**将文本描述引入三维人体与物体联合重建的优化循环**，以此替代或补充传统方法中单一的物理接触信号。这一设计通过以下因果链发挥作用：

1. **文本生成交互语境**：利用 GPT-4 从输入图像中提取两个层次的文本提示——整体交互描述 $P_{\text{holistic}}$（如"一个人正在用右手拿起杯子喝水"）和接触身体部位描述 $P_{\text{contact}}$（如"右手与杯子接触"）。这两个提示分别承担全局语境注入和局部接触引导的角色。

2. **外观损失注入全局语义**：通过预训练扩散模型（StableDiffusion）的分数蒸馏采样（SDS）损失 $\mathcal{L}_{\text{appr}}$，将多视角渲染图像的外观与整体文本提示 $P_{\text{holistic}}$ 对齐。该损失的梯度形式为：

   $$\nabla_{\Phi} \mathcal{L}_{\mathrm{appr}} = \mathbb{E}[ w_t ( \hat{\epsilon}_t( \mathbf{x}_t; P_{\mathrm{holistic}} ) - \epsilon_t ) \frac{\partial \mathbf{x}_t}{\partial \Phi} ]$$

   这一损失在像素级别提供密集梯度信号，将扩散模型中蕴含的丰富视觉先验蒸馏到三维高斯表示中，迫使重建结果在几何和纹理上服从于文本描述的整体交互语境。

3. **接触损失保留局部约束**：在注入全局语义的同时，TeHOR 保留了接触损失 $\mathcal{L}_{\text{contact}}$ 作为局部几何约束，对预测接触的身体部位点集与物体表面间的距离进行惩罚（阈值 $\tau = 10\text{cm}$）：

   $$\mathcal{L}_{\mathrm{contact}} = \frac{1}{|V_{h,c}|} \sum_{v_h \in V_{h,c}} d(v_h, V_o) \cdot \mathbb{1}[d(v_h, V_o) < \tau]$$

### 关键设计变更（Changed Slots）

相对于现有基线方法，TeHOR 在以下四个关键维度上进行了系统性重构：

| 设计维度 | 基线方法 | TeHOR 方案 | 创新性质 |
|---------|---------|-----------|---------|
| **交互推理信号** | 仅物理接触信息（预测接触图或手动标注） | 文本描述（整体语义 + 接触身体部位），由 GPT-4 生成 | 信号源的根本替换 |
| **全局上下文注入方式** | 局部几何接近度拟合（接触损失） | 外观损失 $\mathcal{L}_{\text{appr}}$：通过 StableDiffusion SDS 对齐多视角渲染与文本 | 从局部几何到全局语义的范式转移 |
| **三维表示** | 主要为三角网格（mesh） | 三维高斯溅射（3DGS），最终转换回网格以与基线比较 | 表示层面的现代化升级 |
| **损失函数组成** | 重建损失 + 接触损失（或类似项） | $\mathcal{L} = \mathcal{L}_{\text{recon}} + \mathcal{L}_{\text{appr}} + \mathcal{L}_{\text{contact}} + \mathcal{L}_{\text{collision}}$，新增 $\mathcal{L}_{\text{appr}}$ 为核心创新 | 损失函数的语义维度扩展 |

### 创新点的证据强度

消融实验为上述创新提供了强有力的因果证据：

- **外观损失的决定性作用**：Table 2 显示，移除 $\mathcal{L}_{\text{appr}}$ 后，物体 Chamfer 距离从 16.701 急剧恶化至 22.094，且重建结果无法捕捉整体交互语境，产生不合理的空间关系。相比之下，用 CLIP 损失替代外观损失时，CD_object 为 18.504，证明了像素级 SDS 损失的优越性。

- **文本条件的必要性**：Table 1 表明，移除文本条件后，优化无法纠正隐式交互（如视线方向），CD_object 从 16.701 升至 20.348。

- **对接触估计误差的鲁棒性**：Table S3 显示，替换接触预测源（LEMON 与 GPT-4 接触描述）对重建精度影响很小（CD_human 4.988 vs. 4.941），验证了方法的核心优势在于文本引导的整体交互推理，而非精确的接触预测。

- **非接触场景的显著优势**：Table 5 表明，在非接触交互场景中，TeHOR 显著优于所有依赖接触的方法（CD_human 4.958, CD_object 17.546），直接证明了文本引导机制在物理接触缺失时的独特价值。

### 方法谱系与知识库定位

TeHOR 位于**三维人体-物体交互重建**与**文本驱动的三维生成**两个领域的交叉点。其方法谱系可追溯至：

- **接触驱动重建线**：PHOSA → LEMON + PICO → InteractVLM → HOI-Gaussian，这些方法逐步从手工标注接触发展到学习预测接触，但始终受限于接触信号的局部性。
- **文本驱动三维生成线**：DreamFusion（SDS 损失）→ 各类文本到三维方法，这些方法证明了扩散模型先验可用于三维生成，但此前未被系统性地应用于人体-物体交互重建这一特定任务。

TeHOR 的关键贡献在于**将文本-图像对齐先验首次作为三维人体与物体联合重建的语义约束**，实现了从"物理接触驱动"到"语义语境驱动"的范式转换。这一转换使得重建方法能够捕捉超越物理接触的语义级交互推理，在非接触场景和复杂交互中展现出传统方法无法企及的性能。

## 整体框架

TeHOR 的整体流程从单张 RGB 图像出发，依次完成三个实体的初始重建——三维人体、三维物体与二维背景——随后在统一的 HOI 优化阶段联合精修人体与物体的几何、纹理及空间位姿，最终输出带纹理的网格模型。整个 pipeline 的核心设计在于将文本描述作为语义引导信号注入优化过程，使重建结果不仅满足几何一致性，更服从于整体交互语境的语义约束。

### 从图像到初始三维表示

给定输入图像 $I$，框架首先通过三个并行的预处理分支获取初始三维资产：

- **人体分支**：使用 SmartEraser 移除交互物体与背景，得到仅包含人体的干净图像。该图像送入 **LHM** 重建初始三维高斯属性 $\phi_h$，同时由 **Multi-HMR** 估计 SMPL-X 人体姿态 $\theta$ 与形状 $\beta$ 参数。人体最终表示为一组由 LBS 驱动的三维高斯 $\Phi_h$。
- **物体分支**：同样借助 SmartEraser 与 **SAM** 分割出物体区域，获取干净的物体图像。**InstantMesh** 据此重建带纹理的物体网格，并转换为高斯表示 $\Phi_o$。物体的 6D 位姿（旋转 $R$、平移 $t$、尺度 $s$）通过将重建表面与 **ZoeDepth** 预测的深度图对齐来估计。
- **背景分支**：利用 SmartEraser 移除人体与物体，得到二维背景图像，用于后续渲染合成真实感的多视角视图。

### 文本描述生成

为驱动后续的语义对齐，框架调用 GPT-4 从输入图像中提取两类文本提示：整体交互提示 $P_{holistic}$（描述完整的交互场景与人物动作）和接触身体部位提示 $P_{contact}$（指明参与接触的具体身体部位）。这两类提示分别服务于外观损失和接触损失，是连接视觉重建与语义理解的桥梁。

### HOI 联合优化

初始重建的人体与物体在空间关系上往往存在偏差，且纹理缺乏交互语境的一致性。HOI 优化阶段将人体高斯 $\Phi_h$ 与物体高斯 $\Phi_o$ 联合优化（共 200 步），通过以下总体损失函数驱动：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{recon}} + \mathcal{L}_{\mathrm{appr}} + \mathcal{L}_{\mathrm{contact}} + \mathcal{L}_{\mathrm{collision}}
$$

其中，$\mathcal{L}_{\mathrm{recon}}$ 约束渲染图像与输入图像在像素级的一致性；$\mathcal{L}_{\mathrm{appr}}$ 通过 StableDiffusion 的分数蒸馏采样（SDS）梯度，使多视角渲染的外观与 $P_{holistic}$ 对齐，将全局语义与外观先验注入优化过程；$\mathcal{L}_{\mathrm{contact}}$ 基于 $P_{contact}$ 指定的身体部位，对接触顶点间的距离施加阈值惩罚（$\tau=10$ cm）；$\mathcal{L}_{\mathrm{collision}}$ 则防止人体与物体发生不合理穿透。

### 高斯到网格的转换

优化完成后，框架将人体与物体的高斯表示转换为带纹理的三角网格，以便与现有基线方法公平比较。对于接触区域，在转换过程中施加局部偏移，将物体网格向人体表面推移，确保接触一致性。实验验证表明，该转换对 Chamfer 距离等指标的影响轻微（CD_object 变化约 0.2 cm，Table S4），不会改变方法间的相对排序。

整个 pipeline 的模块化设计使得各组件可独立替换：接触预测源可从 GPT-4 描述切换为 LEMON 估计而性能几乎不变（Table S3），表明框架的核心优势在于文本驱动的整体交互推理，而非对精确接触边界的依赖。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/001_Figure_1.jpg]]
*Figure 1: TeHOR. Given a single image, our framework jointly reconstructs textured 3D human and object by capturing their holistic and semantic interactions using text descriptions*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/004_Figure_3.jpg]]
*Figure 3: Overall pipeline of TeHOR. Given an input image, our framework initially reconstructs a 3D human, a 3D object, and a 2D background. Then, the initially reconstructed 3D human and object are jointly optimized using three core loss functions: reconstruction loss, appearance loss, and contact loss, to ensure accurate and semantically plausible human-object interaction*

## 核心模块与公式推导

### 三维高斯表示

TeHOR 将三维人体与物体分别表示为两组三维高斯 $\Phi_{\mathrm{h}}$ 和 $\Phi_{\mathrm{o}}$。人体高斯由高斯属性 $\phi_{\mathrm{h}}$ 与 SMPL-X 姿态 $\theta$ 和形状 $\beta$ 参数联合参数化，并通过线性混合蒙皮（LBS）驱动动画。物体高斯则从 InstantMesh 重建的纹理网格转换而来，携带 6D 位姿参数 $(R, t, s)$，该位姿通过将重建物体表面与 ZoeDepth 预测的深度图对齐获得。

### 文本描述生成模块

从输入图像出发，利用 GPT-4 生成两类文本提示：整体交互提示 $P_{\mathrm{holistic}}$（描述全局交互语境，如"一个人正在用右手握住网球拍"）和接触身体部位提示 $P_{\mathrm{contact}}$（指定参与交互的具体身体部位，如"右手"）。这两类提示分别驱动外观损失和接触损失，形成语义与几何的双重约束。

### HOI 联合优化阶段

在获得初始人体、物体重建和文本提示后，框架进入联合优化阶段，通过以下总体损失函数驱动优化：

$$\mathcal{L} = \mathcal{L}_{\mathrm{recon}} + \mathcal{L}_{\mathrm{appr}} + \mathcal{L}_{\mathrm{contact}} + \mathcal{L}_{\mathrm{collision}}$$

其中 $\mathcal{L}_{\mathrm{recon}}$ 为重建损失，约束优化后的人体与物体不偏离各自初始重建过远；$\mathcal{L}_{\mathrm{collision}}$ 为碰撞惩罚项，防止人体与物体网格发生穿透。

### 外观损失（核心创新）

外观损失 $\mathcal{L}_{\mathrm{appr}}$ 是 TeHOR 的核心创新，通过预训练扩散模型（StableDiffusion）的分数蒸馏采样（SDS）机制，将多视角渲染图像的外观与整体交互文本 $P_{\mathrm{holistic}}$ 对齐。其梯度形式为：

$$\nabla_{\Phi} \mathcal{L}_{\mathrm{appr}} = \mathbb{E}\left[ w_t \left( \hat{\epsilon}_t( \mathbf{x}_t; P_{\mathrm{holistic}} ) - \epsilon_t \right) \frac{\partial \mathbf{x}_t}{\partial \Phi} \right]$$

**变量含义**：$\Phi$ 为待优化的人体与物体高斯参数；$\mathbf{x}_t$ 为在时间步 $t$ 加噪后的渲染图像；$\hat{\epsilon}_t$ 为扩散模型以 $P_{\mathrm{holistic}}$ 为条件预测的噪声；$\epsilon_t$ 为实际采样的噪声；$w_t$ 为时间步相关的权重。该梯度驱使渲染图像在像素级别服从文本描述的语义约束，从而将全局交互语境注入三维几何与纹理的优化过程。

与 CLIP 损失的对比消融（Table 2）表明，$\mathcal{L}_{\mathrm{appr}}$ 提供的是密集的像素级梯度，能够从扩散网络中蒸馏出更丰富的先验信息，而 CLIP 损失仅提供图像级别的对齐信号，导致 CD_object 从 16.701 恶化至 18.504。

### 接触损失

接触损失 $\mathcal{L}_{\mathrm{contact}}$ 利用 $P_{\mathrm{contact}}$ 指定的身体部位，对预测接触的人体顶点集 $V_{h,c}$ 与最近物体顶点集间的距离进行惩罚：

$$\mathcal{L}_{\mathrm{contact}} = \frac{1}{|V_{h,c}|} \sum_{v_h \in V_{h,c}} d(v_h, V_o) \cdot \mathbb{1}[d(v_h, V_o) < \tau]$$

其中 $d(v_h, V_o)$ 为人体顶点 $v_h$ 到物体顶点集 $V_o$ 的最近距离，$\tau = 10\text{cm}$ 为距离阈值，仅对小于该阈值的顶点施加惩罚。该损失确保文本指定的身体部位与物体在空间上保持合理接近，但并非 TeHOR 的核心优势来源——Table S3 显示替换接触预测源对重建精度影响很小，验证了整体交互推理比精确接触边界划分更为关键。

### 高斯转网格

优化完成后，将三维高斯转换为带纹理网格以便与基于网格的基线方法公平比较。转换过程中，对接触区域施加局部偏移，将物体网格向人体表面移动以保证接触一致性。Table S4 验证该转换对指标影响轻微（CD_object 变化约 0.2）。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/005_Figure_4.jpg]]
*Figure 4: Gaussians-to-mesh conversion process*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/007_Figure_7.jpg]]
*Figure 7: Effectiveness of each loss function in our framework*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/008_Figure_6.jpg]]
*Figure 6: Effectiveness of text descriptions in optimization*

## 实验与分析

### 核心实验设置

TeHOR 在两个公开基准上进行了评估：**Open3DHOI**（超过 2.5K 张图像，133 个物体类别）和 **BEHAVE**。评估指标包括 Chamfer 距离（CD，单位 cm）、接触 F1 分数和碰撞分数。所有对比方法使用相同的初始人体姿态（Multi-HMR）和初始物体形状（InstantMesh），保证公平比较。高斯转网格转换对指标影响轻微（CD_object 变化约 0.2，Table S4）。

### 主定量结果

TeHOR 在两个基准上均达到最优或次优性能（Table 4）。

**Open3DHOI 基准：**
- CD_human：4.941 cm，优于 **HOI-Gaussian**（Wen et al., CVPR 2025）的 5.111 cm（-3.3%）。
- CD_object：16.701 cm，显著优于 **HOI-Gaussian** 的 19.363 cm（-13.7%），也优于 **InteractVLM**（Dwivedi et al., CVPR 2025）的 17.782 cm。
- 接触 F1：0.412，优于 **InteractVLM** 的 0.392（+5.1%）。

**BEHAVE 基准：**
- CD_human：5.615 cm，优于 **HOI-Gaussian** 的 5.748 cm（-2.3%）。
- CD_object：17.339 cm，优于 **InteractVLM** 的 19.197 cm（-9.7%）。

**非接触场景**（Table 5）：TeHOR 在 Open3DHOI 的非接触子集上 CD_human 为 4.958 cm，CD_object 为 17.546 cm，显著优于所有依赖接触的方法。这验证了文本引导在捕捉非接触交互（如注视、指向）方面的核心优势。

### 定性对比

Figure 8 展示了与 **PHOSA**（Zhang et al., ECCV 2020）、**InteractVLM** 和 **HOI-Gaussian** 的定性对比。现有方法因过度依赖接触信息，在非接触或弱接触场景中产生不合理的空间关系（红框标注）。TeHOR 通过文本描述注入全局语义上下文，使重建结果在视觉上更合理。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/013_Figure_8.jpg]]
*Figure 8: Qualitative comparison with state-of-the-art methods. We highlight their representative failure cases with red circles*

### 关键消融实验

#### 1. 文本引导优化的有效性（Table 1）

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/010_Table_1.jpg]]
*Table 1: Effectiveness of text-guided optimization*

优化前 CD_human 为 5.252 cm，CD_object 为 31.268 cm；优化后分别降至 4.941 cm 和 16.701 cm，接触 F1 从 0.305 升至 0.412。移除文本条件时，CD_object 从 16.701 升至 20.348，证明文本语义对纠正隐式交互（如视线方向）至关重要（Figure 6）。

#### 2. 损失函数配置消融（Table 2）

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/009_Table_2.jpg]]
*Table 2: Ablation studies for loss configurations*

- **移除外观损失 L_appr**：CD_object 从 16.701 急剧恶化至 22.094，且重建缺乏整体交互语境（Figure 7 第一行）。
- **用 CLIP 损失替代 L_appr**：CD_object 为 18.504，证明像素级 SDS 损失的稠密梯度信号优于 CLIP 的全局特征对齐。
- **同时使用 L_appr 和 L_contact** 取得最佳性能，但单独使用 L_appr 已显著优于单独使用 L_contact（CD_object 17.824 vs 19.254），说明文本引导的整体交互推理比精确接触预测更重要。

#### 3. 外观渲染组件消融（Table 3）

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/011_Table_3.jpg]]
*Table 3: Ablation studies for appearance rendering*

移除二维背景导致 CD_object 从 16.701 升至 18.196，表明完整的场景上下文对外观损失充分利用扩散网络先验知识至关重要。

#### 4. 接触估计鲁棒性（Table S3）

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/018_Table_S.3.jpg]]
*Table S.3: Impact of contact estimation accuracy on TeHOR’s reconstruction, evaluated on Open3DHOI *

替换接触预测源（LEMON 接触图 vs GPT-4 接触描述）对重建精度影响很小（CD_human 4.988 vs 4.941），证明 TeHOR 的核心优势在于文本引导的整体推理，而非精确的接触边界刻画。

### 失败模式与局限性

1. **局部细节重建困难**（Figure S6）：文本描述侧重整体交互语境，缺少对精细几何与纹理的像素级指导信号，导致手指等局部区域重建不准确。
2. **语义漂移风险**：优化过程依赖预训练扩散模型（StableDiffusion）的显式内容先验，对训练数据中未见的物体类别或极端姿态可能产生语义漂移。
3. **推理效率**：单样本优化耗时约 134 秒（NVIDIA RTX 8000），不适用于实时应用。
4. **单帧输入限制**：无法利用时序信息，难以处理动态交互或严重遮挡场景。

### 外观-文本对齐评估（Table S1）

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/016_Table_S.1.jpg]]
*Table S.1: Quantitative evaluation of appearance-text alignment*

通过 CLIP 分数量化渲染图像与文本描述的对齐程度，TeHOR 在所有对比方法中取得最高分，进一步验证了文本引导在语义一致性方面的优势。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2602_19679/figures/014_Table_5.jpg]]
*Table 5: Quantitative comparison with state-of-the-art methods for non-contact scenarios on Open3DHOI [74]*

## 方法谱系与知识库定位

### 1. 方法谱系：从接触驱动到语义引导的范式迁移

三维人体与物体联合重建长期依赖物理接触作为核心推断信号。早期方法 **PHOSA** (Zhang et al., ECCV 2020) 通过预定义的接触标签优化空间排列，奠定了接触驱动的范式基础。后续工作沿两条路径深化：其一是提升接触预测精度，如 **LEMON + PICO** (Yang et al., CVPR 2024; Cseke et al., CVPR 2025) 引入接触估计模块与接触 Transformer，**InteractVLM** (Dwivedi et al., CVPR 2025) 则微调视觉语言模型预测多视角接触图；其二是改进表示与优化策略，如 **HOI-Gaussian** (Wen et al., CVPR 2025) 采用三维高斯表示并联合接触损失与序贯深度损失，**HDM** (Xie et al., CVPR 2024) 探索模板无关的重建方案。

这些方法的共同瓶颈在于：**优化过程仅由局部几何接近度驱动**，无法捕捉非接触交互（如注视、指向）中隐含的语义关系，且忽视了人体与物体的全局外观上下文，导致重建结果在视觉上不合理（Figure 2 中 InteractVLM 因错误接触预测产生失败案例）。

**TeHOR 的核心范式迁移**在于将交互推理信号从“物理接触”替换为“文本语义描述”。具体而言，TeHOR 利用 GPT-4 从输入图像生成两类文本提示——整体交互提示 $P_{\text{holistic}}$ 和接触身体部位提示 $P_{\text{contact}}$——并通过预训练扩散模型（StableDiffusion）的分数蒸馏采样（SDS）损失 $\mathcal{L}_{\text{appr}}$，将多视角渲染图像与文本描述对齐。这一设计使得全局语境和外观线索得以注入优化过程，驱动重建同时捕捉接触与非接触交互。

### 2. 知识库定位：文本-图像先验作为三维语义约束

TeHOR 的方法论创新可定位于“**将二维基础模型先验注入三维重建**”这一研究脉络。与 CLIP 等全局图像-文本对齐方法不同，TeHOR 采用像素级 SDS 梯度：

$$
\nabla_{\Phi} \mathcal{L}_{\mathrm{appr}} = \mathbb{E}[ w_t ( \hat{\epsilon}_t( \mathbf{x}_t; P_{\mathrm{holistic}} ) - \epsilon_t ) \frac{\partial \mathbf{x}_t}{\partial \Phi} ]
$$

消融实验直接验证了这一选择的必要性：用 CLIP 损失替代 $\mathcal{L}_{\text{appr}}$ 时，物体 Chamfer 距离从 16.701 升至 18.504（Table 2 第三行），证明密集的像素级监督对于精细空间对齐至关重要。

在损失函数层面，TeHOR 的总体目标整合了四类约束：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{recon}} + \mathcal{L}_{\mathrm{appr}} + \mathcal{L}_{\mathrm{contact}} + \mathcal{L}_{\mathrm{collision}}
$$

其中 $\mathcal{L}_{\text{contact}}$ 保留了接触驱动的物理约束（对预测接触的身体部位点集与最近物体点集间的距离进行阈值惩罚），但消融实验（Table S3）揭示了一个关键事实：**替换接触预测源（LEMON 与 GPT-4 接触描述）对重建精度影响很小**，CD_human 仅从 4.941 变为 4.988。这表明 TeHOR 的核心优势在于文本引导的整体交互推理，而非精确的接触边界刻画。

### 3. 适用边界与局限

**适用场景**：TeHOR 在接触与非接触交互场景中均表现优异。在 Open3DHOI 的非接触子集上，CD_human 为 4.958，CD_object 为 17.546，显著优于所有依赖接触的方法（Table 5）。这一优势源于文本描述能够编码注视、指向等非物理接触的语义关系。

**已知局限**：

1. **局部细节重建不足**（Figure S6）：文本描述侧重于整体交互语境，缺少对精细几何与纹理的像素级指导信号，导致局部细节丢失。

2. **预训练先验依赖**：优化过程依赖 StableDiffusion 对显式内容的先验，对训练数据中未见的物体类别或极端姿态可能引入语义漂移。

3. **计算开销**：单样本优化耗时约 134 秒（NVIDIA RTX 8000），不适用于实时应用。

4. **时序信息缺失**：当前框架仅从单张图像输入，无法利用时序信息处理动态交互或严重遮挡场景。

### 4. 开放问题

1. **局部化文本监督**：如何设计局部化的文本驱动监督信号，在保持整体语义对齐的同时实现精细细节重建？

2. **视频扩展**：如何将方法扩展到视频输入，利用时序一致性与文本到视频生成模型增强重建的时空连贯性？

3. **端到端文本-重建联合优化**：可否联合优化文本描述生成与重建过程，以进一步减轻对 VLM 黑盒的依赖，并实现描述与重建的相互促进？

4. **表示层面的改进**：当前高斯转网格的转换（Figure 4）虽经验证对指标影响轻微（Table S4，CD_object 变化约 0.2），但该步骤引入了额外的后处理流程，未来可探索直接在网格表示上进行文本引导优化的方案。

## 原文 PDF

![[paperPDFs/CVPR_2026/TeHOR_Text_Guided_3D_Human_and_Object_Reconstruction_with_Textures.pdf]]