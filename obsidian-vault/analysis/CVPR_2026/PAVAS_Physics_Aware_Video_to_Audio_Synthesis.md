---
title: "PAVAS: Physics-Aware Video-to-Audio Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PAVAS_Physics_Aware_Video_to_Audio_Synthesis.pdf
project_link: "https://physics-aware-video-to-audio-synthesis.github.io"
code_link: null
aliases:
- PPAVAS
- PAVAS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 将物体级别的质量与速度参数显式注入扩散生成过程，作为物理调节信号，使模型能学习生成与物体动力学（动能变化）一致的声音。
primary_logic: 通过VLM估计物体质量、通过分割与动态3D重建估计速度，并利用Phy-Adapter将物理参数融合进扩散模型，使生成过程反映真实世界物体相互作用的动力学，从而实现物理一致的音频合成。
claims:
- PAVAS在VGG-Impact上获得最低的APCC-∆（0.378），表明生成音频与物理动力学（动能变化）的耦合程度最接近真实数据。
- 用户研究中，PAVAS在物理可信度上达到4.37±0.84（Likert 5分制），显著优于其他基线。
- 消融实验表明同时注入质量和速度（+Cmass and Cvel）获得最佳性能，且残差Δ-调制优于直接求和。
- "VGGSound (测试集) 上 用户研究 Likert 评分 (1-5): 音频质量 / 语义对齐 / 时序对齐 / 物理可信度 = PAVAS-L: 4.23±0.77 / 4.47±0.71 / 4.45±0.80 / 4.37±0.84"
---

# PAVAS: Physics-Aware Video-to-Audio Synthesis

> [!tip] 核心洞察
> 通过VLM估计物体质量、通过分割与动态3D重建估计速度，并利用Phy-Adapter将物理参数融合进扩散模型，使生成过程反映真实世界物体相互作用的动力学，从而实现物理一致的音频合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | PAVAS：物理感知的视频到音频合成 |
| 英文题名 | PAVAS: Physics-Aware Video-to-Audio Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hyun-Bin_PAVAS_Physics-Aware_Video-to-Audio_Synthesis_CVPR_2026_paper.html) · [Project](https://physics-aware-video-to-audio-synthesis.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | PAVAS (Physics-Aware Video-to-Audio Synthesis) |
| Dataset | VGGSound, VGG-Impact |

> [!tip] 效果简介
> - VGGSound (测试集) 上，用户研究 Likert 评分 (1-5): 音频质量 / 语义对齐 / 时序对齐 / 物理可信度 PAVAS-L: 4.23±0.77 / 4.47±0.71 / 4.45±0.80 / 4.37±0.84 vs 其他V2A模型平均分数较低（参见 Table 2） (在物理可信度上显著超越所有基线，其他维度也保持最高或领先水平)。
> - VGG-Impact (物理交互子集) 上，APCC-∆ (物理一致性，越低越好) 0.378 vs 其他模型APCC-∆更高（物理相关性弱） (最接近真值的物理一致性，显著降低APCC-∆)。

## 概要

现有视频到音频合成（V2A）模型本质上是**外观驱动**的：它们从视觉帧中提取语义和时序线索，却未显式建模物体相互作用背后的物理因素——如质量与速度。因此，当视觉动力学变化（例如碰撞力度不同）时，生成的音频往往缺乏相应的物理真实性，无法随物体动能变化而调制声音属性。

PAVAS 提出将**物体级别的物理参数**——质量（时间不变）与帧级速度（时间变化）——作为显式条件注入扩散生成过程，使模型学习生成与物体动力学一致的音频。其核心思路是：通过视觉-语言模型估计物体质量，通过分割与动态 3D 重建估计速度，再利用 **Phy-Adapter** 以残差 Δ‑调制的方式将这些物理信号逐步融合进扩散 Transformer 的 AdaLN 参数中，从而在不破坏预训练 backbone 能力的前提下实现物理感知的声音合成。

**方法定位**：PAVAS 基于流匹配的潜在扩散架构，整体管线由三个模块构成——物理参数估计器（PPE）、物理驱动音频适配器（Phy-Adapter）与多模态潜在扩散主干。与 MMAudio（Cheng et al., CVPR 2025）、Frieren（Wang et al., NeurIPS 2025）、TARO（Ton et al., ICCV 2025）、V2A-Mapper（Wang et al., AAAI 2024）等现有 V2A 基线相比，PAVAS 的核心差异在于**物理条件信号**的引入及其**残差注入策略**，而非单纯扩展模型容量或数据规模。

**主要结果**：
- 在物理交互子集 **VGG-Impact** 上，PAVAS 取得最低的 APCC‑Δ（0.378），表明生成音频与物理动力学（动能变化）的耦合程度最接近真实数据。
- 在 **VGGSound** 测试集的用户研究中，PAVAS-L（44.1 kHz）在物理可信度上获得 4.37±0.84（Likert 5 分制），显著优于所有对比基线；在音频质量、语义对齐和时序对齐上也保持领先或最高水平。
- 消融实验证实：同时注入质量与速度特征优于单独注入任一特征，且残差 Δ‑调制策略优于直接求和，验证了逐步引入物理信号的有效性。

**局限与开放问题**：当前物理参数估计器依赖多个预训练模型且未与音频生成器联合优化，可能引入级联误差；仅建模质量与速度而未涵盖材料、弹性等属性，限制了声音合成的丰富性。未来方向包括设计更紧凑的物理注入适配器、端到端联合优化物理估计与音频生成，以及引入更丰富的物理因素（如显式材质建模）来进一步增强物理真实性。

### 问题背景：从视觉到听觉的跨模态生成

视频到音频（Video-to-Audio, V2A）合成旨在为给定的无声视频自动生成语义匹配、时序同步的音频内容。这一任务在电影后期制作、虚拟现实、游戏音效设计等领域具有广泛的应用前景。近年来，基于扩散模型和流匹配框架的生成式方法在音频质量、语义对齐和时序同步性方面取得了显著进展，代表性工作包括**MMAudio**（Cheng et al., CVPR 2025）、**Frieren**（Wang et al., NeurIPS 2025）、**TARO**（Ton et al., ICCV 2025）等。

然而，现有V2A方法共享一个根本性的设计范式：它们主要依赖视觉外观特征（如物体类别、场景语义、运动纹理）来驱动音频生成。这种“外观驱动”的范式虽然在语义层面能够生成“正确”的声音（例如看到吉他即生成吉他声），却无法捕捉视觉场景中更深层的物理动力学信息——物体的**质量**、**速度**、**碰撞力度**等物理属性如何调制声音的响度、频率分布和衰减特性。

### 核心瓶颈：外观驱动范式无法保证物理真实性

真实世界中的声音并非仅由“什么物体在运动”决定，更关键的是“物体如何相互作用”。考虑两个直观场景：

- **轻推一把椅子**与**猛力撞击桌子**：尽管两者都涉及“物体接触”，但产生的声音在响度、频谱分布和持续时间上截然不同。这种差异源于碰撞物体的质量、速度以及由此决定的动能变化。
- **同一物体以不同速度运动**：快速挥动网球拍与缓慢移动它，其破空声的强度和频率成分存在显著差异。

现有V2A模型缺乏对这类物理因素的显式建模。它们从视频帧中提取的视觉特征（如CLIP嵌入或光流）虽然能反映运动的存在，却无法解耦出物体的质量（时间不变属性）和瞬时速度（时间变化属性），更无法建立这些物理量与生成声学特征之间的因果映射。这导致生成音频在物理可信度上存在系统性缺陷：响度变化与视觉动力学不一致、频谱模式与真实碰撞事件的时间对齐度不足。

### 本文动机：将物理推理显式注入生成过程

针对上述瓶颈，本文提出一个核心洞见：**将物体级别的质量与速度参数显式注入扩散生成过程，作为物理调节信号，使模型能够学习生成与物体动力学（动能变化）一致的音频**。这一思路的直觉基础是：声音本质上是物体机械能转化为声能的产物，因此生成过程应当受到机械能相关物理量的直接约束。

实现这一洞见需要解决两个关键技术挑战：

1. **物理参数估计**：如何从单目视频中可靠地估计物体级别的质量（时间不变）和逐帧速度（时间变化）？这需要融合视觉语言模型（VLM）的常识推理、视频分割的物体定位以及动态3D重建的几何信息。
2. **物理条件注入**：如何将估计的物理参数有效地融入扩散模型的生成过程，使其能够调制音频的物理属性，同时不破坏预训练模型已有的语义和时序对齐能力？这需要设计一种非侵入式的条件注入机制。

基于上述动机，本文提出**PAVAS（Physics-Aware Video-to-Audio Synthesis）**，一个物理感知的视频到音频合成框架。PAVAS由两个核心模块构成：**Physics Parameter Estimator（PPE）**负责从输入视频中提取物体级别的质量与速度参数；**Physics-Driven Audio Adapter（Phy-Adapter）**则通过一种残差式的∆-调制机制，将这些物理参数注入基于流匹配的扩散Transformer，从而引导生成过程产生物理一致的音频。

## 核心方法与创新机理

### 问题瓶颈：从外观驱动到物理感知的范式跃迁

现有视频到音频合成（V2A）模型的核心局限在于其**外观驱动**的本质——它们仅基于视觉外观和语义标签生成声音，缺乏对物体物理属性的显式建模。这导致生成音频无法随视觉动力学（如碰撞力度、物体质量差异）调制声音属性：一个轻推乒乓球和一个重击保龄球可能产生相似的声音模式，违背物理直觉。

PAVAS的关键洞察在于：**声音的物理真实性取决于物体相互作用的动力学参数，而非仅视觉外观**。具体而言，物体的质量（决定惯性）和速度（决定动能）是影响碰撞声音强度、频率和衰减的核心物理变量。将这些物理参数显式注入生成过程，才能使模型学习到与物体动能变化一致的声音表征。

### 核心创新：两个关键 Changed Slots

相较于现有V2A基线（如**MMAudio** (Cheng et al., CVPR 2025)、**Frieren** (Wang et al., NeurIPS 2025)、**TARO** (Ton et al., ICCV 2025)等），PAVAS在两个关键维度上实现了范式改变：

#### Changed Slot 1：物理条件信号——从“无”到“显式物理参数”

**基线状态**：现有V2A模型仅使用视频帧特征和可选文本描述作为条件信号，缺乏对物体物理属性的显式表征。

**PAVAS方案**：引入显式的物体级物理参数集 $\mathcal{P} = \{ (m_i, \{v_i^\ell\}_{\ell=1}^{L-1}) \mid o_i \in \mathcal{O} \}$，包含：
- **质量 $m_i$**：时间不变的物体级质量估计，通过VLM从视觉外观和常识推理获得
- **速度 $v_i^\ell$**：帧级瞬时速度，通过分割掩码与动态3D质心重建计算位移 $d_i^\ell = \|\mathbf{c}_i^{\ell+1} - \mathbf{c}_i^\ell\|_2$ 及帧间隔 $\Delta\tau$ 得到 $v_i^\ell = d_i^\ell / \Delta\tau$

这一改变使模型首次获得了**定量链接视觉动力学与声音生成的物理桥梁**。

#### Changed Slot 2：条件注入方式——从“AdaLN直接调制”到“∆-残差调制”

**基线状态**：现有扩散模型使用AdaLN（自适应层归一化）基于多模态条件 $\mathbf{c}_{\text{multi}}$ 直接生成调制参数 $\omega(\mathbf{c}_{\text{multi}})$。

**PAVAS方案**：提出**∆-调制机制**，以残差方式逐步引入物理信息：

$$\tilde{\omega} = \omega(\mathbf{c}_{\text{multi}}) + \alpha_m g_m(\mathbf{c}_{\text{mass}}) + \alpha_v g_v(\mathbf{c}_{\text{vel}})$$

其中 $g_m$ 和 $g_v$ 是**零初始化**的残差混合器，$\alpha_m$、$\alpha_v$ 为可学习缩放因子。这一设计的精妙之处在于：
- **零初始化**确保物理分支在训练初期不干扰已预训练的多模态主干
- **残差形式**允许物理信号作为对基础调制的“修正量”，而非完全替代
- **逐步注入**使模型先学习基础声学模式，再学习物理调制规律

消融实验证实了这一设计的有效性：**残差∆-调制显著优于直接求和**（Table 3-C），验证了逐步注入物理信号的策略优势。

### 方法谱系与知识库定位

PAVAS处于**物理感知生成**与**多模态扩散模型**的交叉地带：

- **扩散V2A基线**：继承自MMAudio的流匹配框架和DiT骨干，但将纯外观条件扩展为“外观+物理”联合条件
- **物理推理**：不同于物理模拟器（需已知精确物理参数），PAVAS从单目视频中**估计**物理量，更贴近真实应用场景
- **适配器设计**：借鉴参数高效微调（PEFT）思想，Phy-Adapter以轻量方式（∆-调制）注入物理知识，避免全量微调的巨大开销

与最相关工作的本质差异：
- **MMAudio**：仅使用CLIP视觉+Synchformer同步特征，无物理建模
- **Frieren**：基于流匹配的高效V2A，但条件信号仍为外观驱动
- **TARO**：专注时序对齐，未涉及物理一致性
- **V2A-Mapper** (Wang et al., AAAI 2024)：轻量级映射器，缺乏物理推理能力
- **Tell What You Hear** (Liu et al., NeurIPS 2024)：自回归生成，无显式物理条件

PAVAS的贡献不在于提出全新的生成架构，而在于**识别并填补了V2A领域的关键缺失维度——物理一致性**，并通过可插拔的Phy-Adapter设计使物理感知能力可集成到现有扩散骨干中。

PAVAS 的整体管线由三个核心模块串联构成：**物理参数估计器（Physics Parameter Estimator, PPE）**、**物理驱动音频适配器（Physics-Driven Audio Adapter, Phy-Adapter）** 以及 **多模态潜在扩散骨干网络（Multimodal Latent Diffusion Backbone）**。给定一段输入视频，系统首先通过 PPE 从中提取物体级别的质量与速度，随后 Phy-Adapter 将这些物理参数编码并注入到扩散 Transformer 中，最终在流匹配框架下生成与视觉动力学物理一致的音频。

### 输入输出流

- **输入**：一段包含动态物体交互的视频，可附带可选的文本描述（测试时可不使用文本）。
- **PPE 阶段**：检测视频中所有可感知运动的物体，为每个物体 $o_i$ 估计**时间不变的质量** $m_i$ 和**帧级速度序列** $\{v_i^\ell\}_{\ell=1}^{L-1}$，形成物理参数集 $\mathcal{P} = \{ (m_i, \{v_i^\ell\}) \mid o_i \in \mathcal{O} \}$。
- **Phy-Adapter 阶段**：将物理参数与物体中心视觉特征融合，生成时间对齐的物理感知表征，并通过 **∆-调制** 机制注入扩散 Transformer 的 AdaLN 层。
- **扩散骨干阶段**：接收多模态条件 $\mathbf{c}_{\mathrm{multi}}$（融合 CLIP 视觉特征、Synchformer 同步特征、CLIP 文本嵌入和时间步嵌入）与物理条件，在流匹配目标下从高斯噪声逐步生成音频潜在表征。
- **输出**：解码后的音频波形，其频谱模式与视频中的物理事件（如碰撞力度）在时序上对齐。

### 模块关系与设计逻辑

三个模块形成“**物理提取 → 物理融合 → 条件生成**”的级联链路。PPE 负责将视觉动力学量化为显式物理参数，解决现有 V2A 模型仅依赖外观特征而无法感知质量与速度的瓶颈；Phy-Adapter 则通过 ∆-调制以**残差方式**将物理信号注入预训练骨干，避免破坏原有多模态条件的语义对齐能力；扩散骨干在流匹配框架下整合所有条件，最终输出物理一致的音频。

**关键设计选择**：物理参数的注入采用零初始化残差混合器，即 $\tilde{\omega} = \omega(\mathbf{c}_{\mathrm{multi}}) + \alpha_m g_m(\mathbf{c}_{\mathrm{mass}}) + \alpha_v g_v(\mathbf{c}_{\mathrm{vel}})$，使得训练初期物理分支贡献为零，逐步学习物理调制效应。消融实验证实该残差策略优于直接求和，验证了“逐步引入物理信号”的有效性。

> **注意**：PPE 内部依赖多个预训练模型（VLM、分割、动态 3D 重建）且未与音频生成器联合优化，可能引入级联误差；Phy-Adapter 虽轻量但仍带来额外计算开销。这些限制在后续版本中有待改进。

![[assets/figures/papers/paper_list_l2072_https_openaccess_thecvf_com_content_CVPR2026_html_Hyun_Bin_PAVAS_Physics/figures/001_Figure_1.jpg]]
*Figure 1: Physics-Aware Video-to-Audio Synthesis (PAVAS). [Top] Current V2A models often generate physically inconsistent audio. [Bottom] We estimate physics values (object-level mass and velocity) from an input video using Physics Parameter Estimator, which are explicitly integrated into a latent diffusion-based model using Phy-Adapter to generate a physically plausible audio*

![[assets/figures/papers/paper_list_l2072_https_openaccess_thecvf_com_content_CVPR2026_html_Hyun_Bin_PAVAS_Physics/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of the proposed Physics-Aware Video-to-Audio Synthesis (PAVAS). Given an input video, the Physics Parameter Estimator (PPE) extracts object-level mass and velocity. These physics cues are encoded by the Physics-Driven Audio Adapter (Phy-Adapter) and injected into the latent diffusion model alongside multimodal conditions*

PAVAS 基于条件流匹配的潜在扩散架构，由三个核心模块构成：**Physics Parameter Estimator (PPE)**、**Physics-Driven Audio Adapter (Phy-Adapter)** 和 **Multimodal Latent Diffusion Backbone**。其中 PPE 负责从视频中提取物体级物理参数，Phy-Adapter 负责将这些物理信号注入扩散模型，Backbone 则完成最终的条件音频生成。

### 3.1 条件流匹配 Backbone

扩散模型训练采用条件流匹配框架，目标是最小化模型预测流速与真实条件流速之间的加权误差：

$$
\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{t, q(\mathbf{x}_0), q(\mathbf{x}_1, \mathbf{c})} \left\| f_{\theta}(t, \mathbf{Y}, \mathbf{x}_t) - u(\mathbf{x}_t | \mathbf{x}_0, \mathbf{x}_1) \right\|_{\mathbf{\Omega}, \mathbf{\eta}}^{2}
$$

其中 $\mathbf{x}_0 \sim \mathcal{N}(0, \mathbf{I})$ 为高斯源分布，$\mathbf{x}_1$ 为目标音频潜在表征，$\mathbf{c}$ 为条件信号（包含视频、文本及物理参数），$\mathbf{Y}$ 为视频特征，$f_{\theta}$ 为可学习的流速场。该目标驱动模型学习从噪声到数据流形的最优传输路径。

### 3.2 物理参数估计器 (PPE)

PPE 从无约束视频中量化物体级别的质量和速度，建立视觉动力学与声音生成之间的定量桥梁。对检测到的每个运动物体 $o_i$，输出物理参数集合：

$$
\mathcal{P} = \{ ( m_i, \{ v_i^{\ell} \}_{\ell=1}^{L-1} ) \mid o_i \in \mathcal{O} \}
$$

其中 $m_i$ 为时间不变的质量估计，$v_i^{\ell}$ 为第 $\ell$ 帧的瞬时速度。**质量估计**通过 VLM 对物体进行语义识别后，依据常识知识赋予归一化质量值；**速度估计**则基于分割掩码与动态 3D 重建，计算物体质心的帧间位移：

$$
d_i^{\ell} = \| \mathbf{c}_i^{\ell+1} - \mathbf{c}_i^{\ell} \|_2, \quad v_i^{\ell} = d_i^{\ell} / \Delta \tau
$$

其中 $\mathbf{c}_i^{\ell}$ 为物体 $i$ 在第 $\ell$ 帧的 3D 质心坐标，$\Delta \tau$ 为帧间隔。

### 3.3 物理驱动音频适配器 (Phy-Adapter)

Phy-Adapter 将物理参数融合进物体中心的视觉特征，并通过 $\Delta$-调制注入扩散 Transformer 的 AdaLN 层。

**物体特征提取**：利用分割掩码对视觉 patch 嵌入加权求和，得到帧级物体中心特征：

$$
\mathbf{f}_i^{\ell} = \sum_{h,w} \mathbf{M}_i^{\ell}[h,w] \cdot \mathbf{V}^{\ell}[h,w,:]
$$

其中 $\mathbf{M}_i^{\ell}$ 为物体 $i$ 在第 $\ell$ 帧的分割掩码，$\mathbf{V}^{\ell}$ 为视觉编码器输出的 patch 特征图。

**质量调制 (FiLM)**：质量通过傅里叶特征映射编码后，经 FiLM 层对物体视觉特征进行仿射变换：

$$
\mathbf{h}_{\mathrm{mass},i} = (1 + \frac{1}{2} \tanh(\gamma_{\mathrm{mass},i})) \odot \mathbf{h}_i + \frac{1}{2} \tanh(\beta_{\mathrm{mass},i})
$$

其中 $\gamma_{\mathrm{mass},i}$ 和 $\beta_{\mathrm{mass},i}$ 由质量条件经 MLP 生成，分别控制缩放和平移。速度特征采用类似的时序调制方式，沿帧维度注入。

**$\Delta$-调制注入**：物理条件以残差方式逐步引入 AdaLN 参数，而非直接替换原有调制：

$$
\tilde{\omega} = \omega(\mathbf{c}_{\mathrm{multi}}) + \alpha_{m} g_{m}(\mathbf{c}_{\mathrm{mass}}) + \alpha_{v} g_{v}(\mathbf{c}_{\mathrm{vel}})
$$

其中 $\omega(\mathbf{c}_{\mathrm{multi}})$ 为基于多模态条件（视频 CLIP 特征、Synchformer 同步特征、文本嵌入、时间步嵌入）的标准 AdaLN 输出，$g_m$ 和 $g_v$ 为零初始化的残差混合器，$\alpha_m$ 和 $\alpha_v$ 为可学习的缩放因子。零初始化确保训练初期物理信号不干扰已收敛的多模态条件，随后逐步学习物理相关的调制残差。消融实验证实该残差策略显著优于直接求和（Table 3-C）。

## 实验与关键发现

### 定量评估：物理一致性指标 APCC-∆

为衡量生成音频与视觉物理动力学的一致性，作者引入 **APCC-∆** 指标——计算音频响度包络与视频帧间动能变化（∆KE）的平均皮尔逊相关系数。该指标直接量化“声音随物理量变化”的程度，越低表示生成音频与真实物理耦合的偏差越大（即越不物理一致）。

在 **VGG-Impact**（VGGSound 中筛选的物理交互子集）上，**PAVAS 取得最低的 APCC-∆（0.378）**，显著优于 MMAudio（Cheng et al., CVPR 2025）、Frieren（Wang et al., NeurIPS 2025）、TARO（Ton et al., ICCV 2025）等基线（Table 1）。这表明 PAVAS 生成的音频在能量动态上与真实物体相互作用最为接近。

![[assets/figures/papers/paper_list_l2072_https_openaccess_thecvf_com_content_CVPR2026_html_Hyun_Bin_PAVAS_Physics/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on the VGGSound test set. Following the standard evaluation protocol [9, 72], parameter counts exclude pretrained encoders (e.g., CLIP), latent audio encoders/decoders, and the modules that are not used in test time (e.g., vocoders). We report only the Large variants of MMAudio and PAVAS; both operate at 44.1kHz, while all other models run at 16kHz. ∗: results reproduced using publicly released code. †: results evaluated from author-provided samples. ♢: models that do not use text input at test time*

### VGGSound 测试集客观指标

Table 1 报告了 VGGSound 测试集上的 FAD、KID、CLAP 分数等标准指标。PAVAS-L（44.1kHz）在多项指标上达到或接近最优，且参数量仅 437M（排除预训练编码器与 vocoder），在性能与效率间取得平衡。

### 用户主观研究

27 名参与者对 8 个模型的生成样本进行 Likert 5 分制评分，涵盖四个维度（Table 2）：

![[assets/figures/papers/paper_list_l2072_https_openaccess_thecvf_com_content_CVPR2026_html_Hyun_Bin_PAVAS_Physics/figures/004_Table_2.jpg]]
*Table 2: User study on the VGGSound test set. 27 participants rate eight generated audios on four aspects: audio quality, semantic alignment, temporal alignment, and physical plausibility. We report the mean and standard deviation of the Likert [37] scale scores (1–5; strongly disagree, disagree, neutral, agree, strongly agree)*

- **音频质量**：PAVAS-L 获得 4.23±0.77，与 MMAudio-L 持平，显著高于其他基线。
- **语义对齐**：PAVAS-L 以 4.47±0.71 领先，说明生成声音与视频语义内容高度匹配。
- **时序对齐**：PAVAS-L 取得 4.45±0.80，表明声音事件与视觉事件在时间上精准同步。
- **物理可信度**：PAVAS-L 以 **4.37±0.84** 显著超越所有基线（次优模型约 3.5 分），这是本文核心贡献的直接验证——用户明确感知到生成音频的物理合理性。

### 消融实验

Table 3 系统拆解了物理特征与注入策略的贡献：

1. **额外训练 backbone 而不引入物理条件**（A 组）：性能变化微小，排除“更多训练步数”作为混淆因素。
2. **物理特征贡献**（B 组，∆-调制下）：
   - 单独注入质量（+Cmass）或速度（+Cvel）均带来一致提升。
   - **联合注入质量与速度**获得最佳性能，证明两种物理量互补。
3. **注入策略对比**（C 组）：
   - 残差 **∆-调制**优于直接求和（Summation），说明以零初始化残差方式逐步引入物理信号更有效，避免干扰已学到的多模态条件。

### 定性分析

Figure 3 展示了生成频谱图的定性对比。绿色虚线标记与视觉事件时序对齐的频谱模式。PAVAS 生成的频谱在碰撞、摩擦等物理交互时刻呈现出更清晰的瞬态结构，而其他方法（如 MMAudio、Frieren）常产生与视觉动态脱节的频谱成分。这从频谱层面印证了物理注入的有效性。

![[assets/figures/papers/paper_list_l2072_https_openaccess_thecvf_com_content_CVPR2026_html_Hyun_Bin_PAVAS_Physics/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative comparison of generated spectrograms. We visualize spectrograms from existing V2A models [9, 39, 68, 69, 75], our method, and the ground truth. Green dashed lines indicate spectral patterns temporally aligned with visual events in the video, and graphic icons denote audible objects or interactions present in the audio track. PAVAS produces spectral patterns that more closely align with these events, whereas other methods often generate components that are not well aligned with the visual dynamics*

### 失败模式与局限

1. **级联误差**：物理参数估计器（PPE）依赖 VLM、分割、3D 重建等多个预训练模型，未与音频生成器联合优化。若 VLM 误判物体质量或分割掩码不准确，误差会传播至生成阶段。
2. **物理属性覆盖有限**：当前仅显式建模质量与速度，未涵盖材料硬度、弹性模量等属性。例如，橡胶球与铁球撞击地面的声音差异无法通过现有物理参数区分。
3. **多物体复杂交互**：在多个物体同时发生物理交互的场景中，物体级特征的独立调制可能导致声音混合不自然，需进一步验证。

## 定位与知识库关联

### 与现有V2A方法的关系

PAVAS处于视频到音频合成（V2A）这一快速发展的研究脉络中。当前主流的V2A模型可大致分为三类：基于扩散的模型、基于流匹配的模型和自回归模型。PAVAS在架构上承袭了基于流匹配的潜在扩散范式，但其核心创新在于首次将**物体级别的物理参数显式注入生成过程**，这是对现有方法的关键突破。

具体而言，PAVAS与以下基线方法构成直接对比关系：

- **MMAudio**（Cheng et al., CVPR 2025）：作为多模态扩散V2A的代表，MMAudio使用AdaLN将视频、文本条件融合进扩散Transformer。PAVAS在保持类似多模态条件框架的同时，通过∆-调制机制将物理条件作为残差增量引入，而非简单扩展条件维度。Table 1显示PAVAS-L在FAD、KL等指标上全面超越MMAudio-L，且在物理一致性指标APCC-∆上优势显著（0.378 vs. 更高值）。

- **Frieren**（Wang et al., NeurIPS 2025）：采用流匹配框架进行V2A生成，与PAVAS共享流匹配训练范式。但Frieren未建模物理参数，其生成完全依赖外观特征。PAVAS在用户研究的物理可信度评分上以4.37±0.84显著超越Frieren等基线，验证了物理注入的有效性。

- **TARO**（Ton et al., ICCV 2025）、**V2A-Mapper**（Wang et al., AAAI 2024）、**Tell What You Hear**（Liu et al., NeurIPS 2024）：这些方法分别聚焦时序对齐、轻量化部署和自回归生成，但均未涉及物理建模。PAVAS在Table 2的用户研究中，在音频质量、语义对齐、时序对齐和物理可信度四个维度上均保持领先或最高水平，表明物理感知并未牺牲其他维度的性能。

从方法谱系看，PAVAS的独特贡献在于**将V2A从“外观-声音”映射推进到“物理-声音”映射**。这一转变的关键在于引入了一个可解耦的物理条件注入路径：Physics Parameter Estimator（PPE）负责从视频中提取质量与速度，Phy-Adapter负责将这些物理信号转化为扩散模型可理解的调制参数。这种模块化设计使得物理推理与音频生成可以独立优化，也为未来引入更多物理因素（如材质、弹性）预留了接口。

### 适用边界

PAVAS的物理感知能力建立在对质量与速度的显式估计之上，这决定了其适用边界：

1. **依赖视觉可观测的物理交互**：PPE需要从视频中检测运动物体并估计其3D轨迹。对于无明显运动的场景（如静态风景、缓慢变化的光影），物理参数估计的可靠性下降，物理注入的增益可能有限。

2. **单物体或简单交互场景更优**：当前设计以物体为中心提取特征，并通过求和池化聚合多物体信息。在复杂多物体交互场景（如拥挤的街道、多人运动）中，物体间的遮挡和轨迹交叉可能导致分割与跟踪误差累积，影响物理参数质量。

3. **质量估计依赖VLM的先验知识**：质量估计器基于视觉-语言模型对物体类别的常识推理（如“金属锤比木锤重”），而非精确物理测量。对于罕见物体或非标准材质，质量估计可能存在系统性偏差。

4. **未覆盖材料与弹性属性**：当前仅建模质量和速度，未显式考虑材料硬度、弹性模量等影响声音频谱特性的因素。对于材质差异显著但运动模式相似的场景（如金属碰撞 vs. 塑料碰撞），生成音频的物理丰富性可能受限。

### 局限与开放问题

**已知局限**（论文明确提及）：

- **级联误差风险**：PPE依赖多个预训练模型（VLM用于物体检测与质量估计、分割模型用于掩码提取、动态3D重建用于速度估计），这些模块未与音频生成器联合优化。任一环节的估计误差都可能传播至最终生成结果，且当前缺乏端到端的误差校正机制。

- **物理属性覆盖不足**：仅显式建模质量和速度两个物理量，未涵盖材料密度、弹性系数、表面粗糙度等影响声音特性的其他物理属性。这使得生成音频的物理表达力存在上限。

- **额外计算开销**：Phy-Adapter虽设计为轻量级模块，但仍引入额外的FiLM调制和∆-调制计算。在实时或资源受限场景下，这一开销需要进一步压缩。

**开放问题**（值得后续探索）：

- **端到端联合优化**：能否将PPE中的质量/速度估计与扩散模型的生成目标进行联合训练，使物理参数估计器能够根据生成质量反馈自我校正？这需要设计可微分的物理估计管线或基于强化学习的优化策略。

- **更紧凑的物理注入适配器**：当前Phy-Adapter包含Fourier特征映射、FiLM调制和∆-调制等多个子模块。能否通过知识蒸馏或架构搜索找到更精简的物理注入方案，在保持物理一致性的同时降低计算成本？

- **显式材质建模**：如何将材料属性（如杨氏模量、密度）作为额外的物理条件引入？这可能需要结合材质识别模型或物理仿真引擎，进一步丰富声音的频谱特性。

- **多物体复杂交互扩展**：在密集场景中，如何设计更鲁棒的物体关联与物理参数聚合策略？例如，引入图神经网络建模物体间的物理交互关系，而非简单的求和池化。

- **物理一致性的形式化度量**：APCC-∆虽能反映生成音频与物理动力学的耦合程度，但其计算依赖真实音频的动能曲线作为参考。能否设计无参考的物理一致性评估指标，使其更适用于开放域视频？

需要指出的是，上述局限和开放问题主要基于论文自身讨论和方法设计的自然延伸推断。关于PPE各模块的具体误差传播量级、Phy-Adapter在不同硬件上的实际推理延迟等细节，论文未提供定量数据，需通过代码复现或联系作者进行手动验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/PAVAS_Physics_Aware_Video_to_Audio_Synthesis.pdf]]
