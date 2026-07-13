---
title: "Vinedresser3D: Towards Agentic Text-guided 3D Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Vinedresser3D_Towards_Agentic_Text_guided_3D_Editing.pdf
project_link: null
code_link: null
aliases:
- Vinedresser3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用多模态大语言模型（MLLM）作为智能体核心，自动解析编辑意图、生成多模态引导并检测3D编辑掩码，结合原生3D潜在空间上的反演-修复方法。
primary_logic: 通过在原生3D流生成模型（Trellis）的潜在空间中引入反演-修复和交错去噪策略，并将2D视觉-语言推理作为编辑规划工具，可以在不依赖人工3D掩码的情况下实现高保真、语义对齐的3D编辑。
claims:
- Vinedresser3D 在文本对齐指标 CLIP-T 上达到 0.252，优于 Instant3dit (0.227)、VoxHammer (0.235) 和 Trellis (0.247)。
- 用户研究中 Vinedresser3D 在编辑对齐、未编辑区域保持和整体3D质量上分别以92.5%、82.0%和90.8%的胜率优于 Trellis。
- 自动检测的编辑区域掩码显著提升未编辑区域保持：带掩码 PSNR 29.45 vs 无掩码 25.65。
- 交错 Trellis-text 与 Trellis-image 去噪设计优于仅用 Trellis-image：FID 29.49 vs 30.59。
---

# Vinedresser3D: Towards Agentic Text-guided 3D Editing

> [!tip] 核心洞察
> 通过在原生3D流生成模型（Trellis）的潜在空间中引入反演-修复和交错去噪策略，并将2D视觉-语言推理作为编辑规划工具，可以在不依赖人工3D掩码的情况下实现高保真、语义对齐的3D编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | Vinedresser3D: 迈向智能体驱动的文本引导3D编辑 |
| 英文题名 | Vinedresser3D: Towards Agentic Text-guided 3D Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chi_Vinedresser3D_Towards_Agentic_Text-guided_3D_Editing_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Vinedresser3D |
| Dataset | 泛化3D编辑测试集 |

> [!tip] 效果简介
> - 泛化3D编辑测试集 上，CLIP-T↑ (文本对齐) 0.252 (Ours) vs 0.247 (Trellis) (+0.005)；FID↓ (整体3D质量) 29.49 (Ours) vs 31.10 (Trellis) (-1.61)；PSNR↑ (未编辑区域保持) 29.45 (Ours) vs 37.35 (Trellis) (-7.90)。
> - 用户偏好研究 上，编辑对齐胜率 vs Trellis 92.5% vs 7.5% (+85.0%)。

## 概要

**问题瓶颈**：现有文本引导的3D编辑方法面临三重挑战——难以自动理解复杂的自然语言编辑指令、无法在3D空间中精确定位编辑区域，以及难以可靠地保持未编辑区域的几何与外观一致性。基于“2D编辑+3D重建”的范式（如 Instant3dit）在语义对齐上存在局限，而基于原生3D生成模型的方法（如 **VoxHammer** (Li et al., arXiv 2025)）仍依赖用户手动提供3D掩码，自动化程度不足。

**核心思路**：Vinedresser3D 将多模态大语言模型（MLLM，具体为 Gemini-2.5-flash）作为智能体核心，使其能够自动解析编辑意图、生成分解的结构与外观文本引导，并结合 PartField 分割自动检测3D编辑掩码。在此基础上，通过在原生3D流生成模型 **Trellis**（Xiang et al., CVPR 2025）的潜在空间中引入基于 RF-Solver 的二阶反演与交错去噪修复机制，实现高保真、语义对齐的3D编辑，全程无需人工3D掩码。

**方法定位**：该方法属于“智能体驱动+原生3D反演修复”范式，区别于依赖2D中间表示或人工掩码的既有路线。其关键创新在于将2D视觉-语言推理能力转化为3D编辑的规划工具，并通过交错 Trellis-text 与 Trellis-image 去噪策略平衡文本语义对齐与视觉质量。

**主要结果**：
- **自动指标**：在泛化3D编辑测试集上，Vinedresser3D 的文本对齐指标 CLIP-T 达到 0.252，优于 Instant3dit (0.227)、VoxHammer (0.235) 和 Trellis (0.247)；整体3D质量 FID 为 29.49，优于 Trellis 的 31.10（Table 1）。
- **用户偏好**：用户研究中，Vinedresser3D 在编辑对齐、未编辑区域保持和整体3D质量上分别以 92.5%、82.0% 和 90.8% 的胜率显著优于 Trellis（Table 2）。
- **消融验证**：自动检测的编辑掩码对未编辑区域保持至关重要（带掩码 PSNR 29.45 vs 无掩码 25.65）；交错去噪设计优于仅用 Trellis-image（FID 29.49 vs 30.59）（Table 3）。

**局限与展望**：当前 MLLM 主要在2D数据上训练，对3D空间关系的理解有限；编辑区域检测受 PartField 分割粒度影响；基础生成模型的分辨率（64³体素）限制了细节保真度。未来方向包括让 MLLM 直接消费3D输入进行原生3D推理、引入更强的3D分割模型，以及探索更优的交错去噪调度方案。



### 文本引导3D编辑的现状与瓶颈

3D内容创作在游戏、影视和虚拟现实等领域的需求持续增长，但高质量3D资产的制作仍然高度依赖专业建模技能和大量人工时间。文本引导的3D编辑旨在让用户通过自然语言指令直接修改3D资产，从而降低创作门槛。然而，现有方法面临一个核心瓶颈：**难以自动理解复杂自然语言指令、在3D空间中精确定位编辑区域，同时可靠地保持未编辑区域的几何与外观**。

当前主流方法大致分为两类。一类基于“2D编辑+3D重建”范式，如**Instant3dit**，先对渲染视图进行2D编辑，再通过逆渲染或重建恢复3D表示。这类方法受限于2D编辑与3D重建之间的信息损失，难以保证多视图一致性和未编辑区域的完整保持。另一类基于原生3D生成模型，如**VoxHammer**（Li et al., arXiv 2025），直接在3D表示上进行编辑，但通常需要用户手动提供精确的3D掩码来指定编辑区域，这在复杂场景中极为繁琐且不切实际。

更根本的困难在于，现有方法缺乏对编辑意图的深层语义理解能力。当用户说“给这只猫戴上一顶巫师帽”时，系统不仅需要知道“巫师帽”是什么，还需要推断猫的头顶位置、帽子的合理比例，以及编辑不应改变猫的面部和身体。这种跨模态的语义推理和3D空间定位能力，是传统编辑管线所不具备的。

### 本文动机：从被动工具到主动智能体

本文的动机在于，将文本引导3D编辑从**被动工具**升级为**主动智能体**。具体而言，我们希望系统能够：

1. **自动解析编辑意图**：理解用户的自然语言指令，识别编辑类型（增加、修改、删除）和目标部件。
2. **自主生成多模态引导**：不仅依赖文本描述，还能主动选择最优视图并生成编辑后的图像作为视觉参考。
3. **自动检测编辑区域**：在3D空间中定位需要编辑的体素区域，无需人工提供掩码。
4. **在原生3D空间中执行高保真编辑**：利用3D生成模型的先验知识，确保编辑结果的几何一致性和渲染质量。

这一思路的核心洞察是：**通过在原生3D流生成模型（Trellis, Xiang et al., CVPR 2025）的潜在空间中引入反演-修复和交错去噪策略，并将2D视觉-语言推理作为编辑规划工具，可以在不依赖人工3D掩码的情况下实现高保真、语义对齐的3D编辑**。多模态大语言模型（MLLM）作为智能体核心，负责从多视角渲染图像和编辑提示中提取结构化和外观层面的文本引导，并结合PartField分割结果推断编辑掩码，从而打通从语言指令到3D修改的完整闭环。



## 核心方法与创新机理

Vinedresser3D 的核心突破在于将**多模态大语言模型（MLLM）作为智能体核心**引入文本引导的 3D 编辑管线，解决了现有方法在理解复杂自然语言指令、自动定位编辑区域和保持未编辑区域保真度之间的根本矛盾。其创新可归纳为三个关键的 **changed slots**：

### 1. 从手动掩码到 MLLM 驱动的自动编辑区域检测

现有原生 3D 编辑方法（如 **VoxHammer**，Li et al., arXiv 2025）依赖用户手动提供精确的 3D 掩码来界定编辑范围，这在实际应用中极不友好且容易出错。Vinedresser3D 通过 **PartField 分割 + MLLM 推理**的级联机制实现自动化：PartField 先将 3D 资产分解为语义部件，MLLM 再根据编辑指令识别目标部件并判断操作类型（增加/修改/删除），最终生成体素级的编辑掩码（见 Eq. 3）。

该设计的因果效应在消融实验中得到直接验证：**带自动检测掩码时未编辑区域 PSNR 达 29.45，而无掩码时骤降至 25.65**（Table 3）。这一差距揭示了掩码在约束去噪扩散过程、防止编辑操作“外溢”到保留区域中的关键作用——本质上，掩码为高维流空间中的修复过程提供了空间正则化边界。

### 2. 从单一文本指令到分解的多模态引导

传统方法仅将用户的简短编辑指令作为条件输入，信息量有限。Vinedresser3D 的 MLLM 智能体通过分析多视角渲染图像，自动生成**结构化的引导信息**（Figure 3）：
- **原始资产完整描述**与**编辑后完整描述**之间的差异词（标记为下划线斜体），分解为阶段 1 相关（青色）和阶段 2 相关（红色）的结构/外观信息；
- **最优视图选择**后，调用图像编辑模型生成视觉引导，为目标 3D 外观提供像素级参考。

这种分解策略的深层逻辑在于：3D 编辑需要同时保持几何结构的合理性和外观纹理的语义对齐，而单一文本条件难以同时约束这两个维度。通过将结构引导注入阶段 1 的 Trellis-text 去噪、外观引导注入阶段 2 的 Trellis-image 去噪，实现了**条件信号的解耦与协同**。

### 3. 从直接生成到基于反演的原生 3D 修复

不同于“2D 编辑 + 3D 重建”范式（如 **Instant3dit**）引入的跨维度不一致风险，Vinedresser3D 直接操作原生 3D 流生成模型 **Trellis**（Xiang et al., CVPR 2025）的潜在空间。其编辑机制包含两个关键设计：

- **RF-Solver 二阶反演**（Eq. 2）：在标准一阶反演（Eq. 1）基础上引入二阶泰勒展开项 $\frac{1}{2}(t_{i-1} - t_i)^2 v_{\theta}^{(1)}(X_i, t_i)$，利用速度场的时间导数 $v_{\theta}^{(1)}$ 提升反演精度，确保原始资产的几何结构被准确编码为结构化噪声。

- **交错 Trellis-text / Trellis-image 去噪**：在所有时间步上交替使用文本条件和编辑图像条件进行去噪修复，而非仅依赖图像条件。消融实验表明，交错策略的 FID 为 29.49，显著优于仅用 Trellis-image 的 30.59（Table 3），验证了文本条件对维持 3D 结构合理性的贡献——纯图像条件容易产生扭曲或不合理的几何输出（Figure 6）。

---

**创新边界与代价**：上述三个 changed slots 共同构成了 Agent 驱动的自动化编辑闭环，但其代价也是明确的——在未编辑区域保持指标（PSNR/SSIM）上弱于直接用 Trellis 生成的原始资产（Table 1），这是以局部保真度换取全局编辑语义对齐的权衡。当提供人工掩码（Ours w/ HM）时，该方法在全部指标上达到最优，说明自动掩码检测仍是当前性能瓶颈所在。



Vinedresser3D 的完整管线围绕一个多模态大语言模型（MLLM）智能体核心构建，将复杂的文本编辑指令自动转化为高保真的3D资产编辑结果。如图2所示，系统接收一个原始3D资产和一条自然语言编辑指令，通过三个串联阶段完成编辑：**多模态引导生成**、**编辑区域检测**和**基于反演的3D编辑**。

### 输入与输出流

**输入**由两部分组成：一个由Trellis（Xiang et al., CVPR 2025）原生3D流生成模型表示的3D资产，以及一条自由形式的文本编辑指令。**输出**为编辑后的3D资产，其编辑区域与指令语义对齐，同时未编辑区域的几何与外观得到保持。

### 三阶段管线

**阶段一：多模态引导生成（Sec. 3.2）**。MLLM（Gemini-2.5-flash）首先分析3D资产的多视角渲染图像，输出原始资产的完整描述、目标编辑部件的名称、编辑操作类型（增加/修改/删除）以及编辑后的完整描述。通过对比原始描述与编辑后描述，MLLM将文本引导分解为**结构级引导**（用于第一阶段反演-修复）和**外观级引导**（用于第二阶段细化）。同时，MLLM从多视角中选择信息量最大的视图，调用2D图像编辑模型生成视觉引导，为后续3D修复提供像素级条件。

**阶段二：编辑区域检测（Sec. 3.3）**。利用PartField对原始资产进行3D语义分割，MLLM在分割结果上进行推理，确定编辑部件$P_{\mathrm{edit}}$和保留部件$P_{\mathrm{pres}}$。根据操作类型，系统按式（3）定义可编辑体素区域$R_{\mathrm{edit}}$：增加操作取资产外部的扩展区域，删除操作直接取$P_{\mathrm{edit}}$，修改操作则取$P_{\mathrm{edit}}$与边界扩展区域的并集。该区域随后转化为3D编辑掩码，用于指导修复过程。

**阶段三：基于反演的3D编辑（Sec. 3.4）**。如图4所示，该阶段首先使用RF-Solver的二阶反演（式2）将原始3D资产沿整流流轨迹映射回结构化噪声空间，以原始完整描述作为条件。随后，在编辑掩码的约束下，通过**交错Trellis-text与Trellis-image去噪**进行修复：在每个时间步，交替使用编辑后的文本描述和编辑图像作为条件，逐步去噪生成编辑后的3D资产。对于删除操作，系统跳过反演和修复，直接移除$R_{\mathrm{edit}}$中的体素并通过第二阶段平滑边界。

### 模块间的因果依赖

三个模块形成严格的因果链：MLLM生成的多模态引导决定了编辑的语义方向和视觉目标；编辑区域检测将引导聚焦到精确的3D空间位置；反演-修复模块则在掩码约束下执行实际的3D内容修改。任一模块的失效都会导致编辑失败——若引导不准确，编辑语义将偏离指令；若掩码不精确，未编辑区域将受到污染；若反演精度不足，则编辑结果的几何一致性会退化。消融实验证实了这一依赖关系：移除编辑掩码后，PSNR从29.45降至25.65（Table 3），未编辑区域出现明显畸变（Figure 7）；将交错去噪替换为仅Trellis-image去噪后，FID从29.49升至30.59（Table 3），整体3D质量下降（Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l2652_https_openaccess_thecvf_com_content_CVPR2026_html_Chi_Vinedresser3D_Towa/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline overview. Given a 3D asset and an editing prompt, Vinedresser3D uses an MLLM to obtain new text and image guidance, automatically detects the intended editing region and then performs precise editing through an inversion-editing module*



Vinedresser3D 的编辑管线由三个核心模块串联构成：多模态引导生成、编辑区域检测、以及基于反演的 3D 编辑。本节聚焦各模块的关键机制与支撑公式。

### 多模态引导生成

该模块以 MLLM（Gemini-2.5-flash）为推理核心，输入为原始 3D 资产的多视角渲染图像与用户的编辑指令。MLLM 完成三项分析任务：输出原始资产的完整描述、识别被编辑目标的部件名称与编辑操作类型（增加/修改/删除）、生成编辑后的完整描述。这一“原始描述—编辑后描述”的文本对，经关键词匹配提取出结构级（Stage 1）与外观级（Stage 2）的分解引导信息（Figure 3）。同时，MLLM 从多视角中选取最有利于编辑表达的一个视图，调用 2D 图像编辑模型生成视觉引导图像，为后续 3D 修复提供像素级条件。

![[assets/figures/papers/paper_list_l2652_https_openaccess_thecvf_com_content_CVPR2026_html_Chi_Vinedresser3D_Towa/figures/003_Figure_3.jpg]]
*Figure 3: Text guidance output by the MLLM. The modified words between the original complete description and the new complete description are marked with underlined italics. We highlight the extracted stage 1-related (in cyan) and stage 2-related (in red) information*

### 编辑区域检测

编辑区域检测模块将 MLLM 的语义理解与 PartField 的 3D 分割结果相结合，自动生成体素级编辑掩码，替代了 VoxHammer 等基线方法所需的人工 3D 掩码。其核心是依据编辑操作类型分段定义可编辑区域 $R_{\mathrm{edit}}$：

$$R_{\mathrm{edit}} = \begin{cases}
C \setminus A, & \text{addition} \\[4pt]
P_{\mathrm{edit}}, & \text{deletion} \\[4pt]
P_{\mathrm{edit}} \cup (C \setminus \mathrm{bbox}_{\mathrm{pres}}) \cup V, & \text{modification}
\end{cases}$$

其中 $C$ 为整个 3D 资产的体素集合，$A$ 为资产主体区域，$P_{\mathrm{edit}}$ 为 PartField 分割出的目标编辑部件，$\mathrm{bbox}_{\mathrm{pres}}$ 为 MLLM 指定的保留包围盒，$V$ 为基于 $k$ 近邻比例阈值确定的边界过渡体素。增加操作将编辑区域定义为资产主体之外的空间，删除操作直接以目标部件为编辑区域，修改操作则合并目标部件、保留包围盒之外的空间与边界过渡区域。

### 基于反演的 3D 编辑

该模块在原生 3D 流生成模型 Trellis 的潜在空间中执行反演-修复，是方法区别于“2D 编辑+3D 重建”范式的关键。

**反演阶段**采用 RF-Solver 的二阶反演公式，将原始 3D 资产映射回流噪声空间。标准一阶整流流反演为：

$$X_{i-1} = X_i + (t_{i-1} - t_i) v_{\theta}(X_i, t_i)$$

RF-Solver 在此基础上引入速度场 $v_{\theta}$ 的时间导数项 $v_{\theta}^{(1)}$，以二阶泰勒展开提升反演精度：

$$X_{i-1} = X_i + (t_{i-1} - t_i) v_{\theta}(X_i, t_i) + \frac{1}{2} (t_{i-1} - t_i)^2 v_{\theta}^{(1)}(X_i, t_i)$$

反演以原始完整描述为条件，确保结构化噪声中保留原始资产的几何与外观信息。

**修复阶段**采用交错去噪策略：在所有时间步上交替使用 Trellis-text（以编辑后文本描述为条件）和 Trellis-image（以编辑后视觉引导图像为条件）进行去噪修复。编辑区域掩码 $R_{\mathrm{edit}}$ 在此阶段引导修复范围——未编辑区域的潜在特征被注入以正则化去噪过程，从而约束几何一致性。对于删除操作，管线跳过 Stage 1 反演与修复，直接移除 $R_{\mathrm{edit}}$ 内体素后仅执行 Stage 2 边界平滑；对于修改与增加操作，则完整执行两阶段反演-修复流程。消融实验（Table 3）证实，交错 Trellis-text/Trellis-image 设计相较于仅使用 Trellis-image 将 FID 从 30.59 降至 29.49，而引入编辑掩码将未编辑区域 PSNR 从 25.65 提升至 29.45，验证了各公式机制的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2652_https_openaccess_thecvf_com_content_CVPR2026_html_Chi_Vinedresser3D_Towa/figures/004_Figure_4.jpg]]
*Figure 4: Our native 3D inversion-based editing pipeline. It first invert the original 3D asset back to structured noises using RF-Solver [53] and the original complete description as the condition. Then it performs editing through inpainting by denoising with Trellis-text and Trellis-image alternatively for all timesteps, using both the new text and edited image as conditions*



## 实验与关键发现

### 主结果：定量对比

Vinedresser3D 在泛化 3D 编辑测试集上与两类基线进行了系统对比：基于“2D 编辑 + 3D 重建”范式的 **Instant3dit**，以及基于原生 3D 生成模型但需用户手动提供 3D 掩码的 **VoxHammer**（Li et al., arXiv 2025）和基础生成模型 **Trellis**（Xiang et al., CVPR 2025）。如 Table 1 所示，Vinedresser3D 在文本对齐指标 CLIP-T 上达到 **0.252**，优于 Instant3dit (0.227)、VoxHammer (0.235) 和 Trellis (0.247)，验证了 MLLM 生成的分解式结构/外观文本引导对语义对齐的有效性。在整体 3D 质量（FID↓）上，本方法取得 **29.49**，显著优于 Trellis (31.10) 和 VoxHammer (32.18)，表明交错 Trellis-text / Trellis-image 去噪策略比单纯依赖图像条件能产生更高质量的 3D 输出。

![[assets/figures/papers/paper_list_l2652_https_openaccess_thecvf_com_content_CVPR2026_html_Chi_Vinedresser3D_Towa/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison. We include the results of our method with human-provided 3D masks (Ours w/ HM). Best results are in bold. Our method with human-provided 3D masks achieves the best results in all metrics. Even though our method without humanprovided 3D masks does not preserve the unedited parts as well as Trellis, it still closely aligns with the editing prompt and produces high-quality outcomes*

需要指出的是，在未编辑区域保持（PSNR↑）上，本方法（29.45）弱于 Trellis（37.35）——后者直接使用原始文本生成，天然保持全局一致性，而编辑过程不可避免地引入重建误差。这一 trade-off 在用户研究中得到了进一步阐释：用户更偏好编辑语义的对齐，而非未编辑区域的像素级保真度。

当使用人工提供的 3D 掩码（Ours w/ HM）时，本方法在所有指标上均达到最优（CLIP-T 0.252, PSNR 37.35, FID 26.78），这揭示了自动掩码检测是当前性能瓶颈之一，也为未来改进指明了方向。

### 用户偏好研究

如 Table 2 所示，在编辑对齐、未编辑区域保持和整体 3D 质量三个维度上，Vinedresser3D 相较于 Trellis 分别取得了 **92.5%**、**82.0%** 和 **90.8%** 的胜率。相较于 VoxHammer，胜率同样显著（编辑对齐 84.2%，未编辑保持 72.5%，整体质量 79.2%）。值得注意的是，VoxHammer 需要用户手动标注 3D 掩码，而 Vinedresser3D 完全自动化了该过程——即便如此，用户仍更偏好本方法的编辑结果，这充分证明了 MLLM 驱动的编辑区域检测在实用性和结果质量上的双重优势。

![[assets/figures/papers/paper_list_l2652_https_openaccess_thecvf_com_content_CVPR2026_html_Chi_Vinedresser3D_Towa/figures/006_Table_2.jpg]]
*Table 2: User study. We ask the user to select the better one between ours and another method in terms of editing prompt alignment, unedited parts preservation and overall 3D quality. We report the win rates of our methods. Our method achieves high win rates in all perspectives*

### 消融实验

Table 3 和 Figure 6、Figure 7 从定量和定性两个维度验证了两个核心设计选择。

![[assets/figures/papers/paper_list_l2652_https_openaccess_thecvf_com_content_CVPR2026_html_Chi_Vinedresser3D_Towa/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative ablation of interleaved Trellis vs Trellisimage only. The outputs of Trellis-image only editing may be distorted or unreasonable*

![[assets/figures/papers/paper_list_l2652_https_openaccess_thecvf_com_content_CVPR2026_html_Chi_Vinedresser3D_Towa/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative ablation of our method with and without the detected editing region as the 3D mask. Our method without the detected editing region may alter the intended preserved parts or produce distorted outputs*

**交错去噪 vs 仅 Trellis-image 去噪。** 移除 Trellis-text 去噪步骤、仅使用 Trellis-image 进行修复，整体 3D 质量显著下降（FID 从 29.49 升至 30.59），且未编辑区域保持也受损（PSNR 从 29.45 降至 28.12）。如 Figure 6 所示，仅用图像条件时输出容易出现几何畸变或语义不合理的结果——文本条件在去噪过程中提供了结构层面的正则化，防止图像引导过度主导生成过程。

**自动编辑掩码的影响。** 完全移除编辑区域掩码后，未编辑区域保持指标急剧恶化：PSNR 从 29.45 降至 **25.65**，SSIM 从 0.892 降至 0.854。Figure 7 的定性结果显示，无掩码条件下编辑会“溢出”到本应保留的区域，或产生全局性失真。这证实了 PartField 分割与 MLLM 推理联合生成的体素级掩码对于约束编辑范围、保护未编辑区域至关重要。消融结果还揭示了一个深层机制：掩码不仅定义了编辑边界，还通过注入保留区域特征来正则化去噪过程——这解释了为何带掩码时 FID 也更好（29.49 vs 30.32）。

### 失败模式与局限性

尽管整体性能优异，Vinedresser3D 在以下场景中存在可辨识的失败模式：

1. **复杂空间关系下的定位偏差。** 当前 MLLM（Gemini-2.5-flash）主要在 2D 数据上训练，对 3D 空间关系的理解有限。当编辑指令涉及“椅子左侧的扶手”或“桌子后方的装饰”等精细空间描述时，基于多视角 2D 渲染的推理可能错误定位编辑区域，导致编辑作用于错误部件。

2. **PartField 分割粒度不匹配。** 编辑区域检测依赖 PartField 的分割结果，当目标编辑部件（如“茶杯把手”）未被 PartField 独立分割，或分割粒度过细（将单一部件拆分为多个碎片）时，后续掩码生成会失效。这在处理非标准物体或复杂场景时尤为明显。

3. **生成分辨率与细节保真度受限。** 继承自 Trellis 的基础生成模型，输出分辨率限制在 64³ 体素，训练数据规模也约束了细节生成能力。对于需要精细几何细节的编辑（如添加复杂纹饰、修改面部特征），结果可能缺乏足够的保真度。

4. **计算开销。** 反演-修复过程需要完整的正向和反向整流流计算（RF-Solver 的二阶反演进一步增加了计算量），当前管线尚不适合实时交互场景。

### 补充图表

![[assets/figures/papers/paper_list_l2652_https_openaccess_thecvf_com_content_CVPR2026_html_Chi_Vinedresser3D_Towa/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of different methods. We can see that our method surpasses all the others by smartly interpreting the editing intention of the user, closely following the editing prompt, precisely locating the intended editing region and generating high-fidelity results*

![[assets/figures/papers/paper_list_l2652_https_openaccess_thecvf_com_content_CVPR2026_html_Chi_Vinedresser3D_Towa/figures/001_Figure_1.jpg]]
*Figure 1: We propose Vinedresser3D , an agent that can intelligently perform high-quality text-guided 3D editing. It can handle various kinds of edits (addition, modification and deletion), support multi-turn editing and tackle different types of 3D assets (objects and scenes)*



## 定位与知识库关联

### 1. 基线对比与谱系定位

Vinedresser3D 处于“文本引导 3D 编辑”这一快速发展的交叉领域，其核心贡献在于将**多模态大语言模型（MLLM）驱动的智能体范式**引入原生 3D 生成模型的编辑流程。与现有工作相比，本文在三个关键维度上实现了方法跃迁：

**编辑区域获取方式**。早期方法如 **VoxHammer**（Li et al., arXiv 2025）要求用户手动提供 3D 掩码来指定编辑区域，这在实际使用中构成显著的交互负担。Vinedresser3D 通过 MLLM 结合 PartField 分割自动检测编辑区域掩码（Sec. 3.3），将人工标注这一瓶颈环节自动化。消融实验表明，自动检测的编辑掩码对未编辑区域保持至关重要：带掩码时 PSNR 为 29.45，无掩码时降至 25.65（Table 3）。值得注意的是，本文同时报告了使用人工掩码的上限性能（Ours w/ HM），该设置在 Table 1 的所有指标上均取得最优，揭示了掩码精度仍是决定编辑质量上限的关键因素。

**引导信息源**。**Instant3dit** 等基于“2D 编辑 + 3D 重建”范式的方法仅依赖文本编辑指令，缺乏对 3D 结构的显式理解。Vinedresser3D 利用 MLLM（Gemini-2.5-flash）分析多视角图像，生成分解的结构/外观文本描述，并自动选择最优视图通过图像编辑模型获取视觉引导（Sec. 3.2, Fig. 3）。这种多模态引导策略使编辑意图的解析更为精确，在 CLIP-T 文本对齐指标上达到 0.252，优于 Instant3dit 的 0.227（Table 1）。

**3D 编辑机制**。与直接生成或 2D 引导下 3D 重建的范式不同，Vinedresser3D 采用基于 RF-Solver 二阶反演的交错 Trellis-text/Trellis-image 修复策略（Sec. 3.4, Fig. 4）。RF-Solver 通过在标准一阶反演基础上引入二阶泰勒展开项 $v_{\theta}^{(1)}(X_i, t_i)$，提高了整流流反演的精度（Eq. 2）。交错去噪设计优于仅使用 Trellis-image：FID 从 30.59 降至 29.49（Table 3），定性结果显示仅用 Trellis-image 的输出可能出现扭曲或不合理的结果（Fig. 6）。

### 2. 适用边界

Vinedresser3D 的适用边界由以下技术依赖共同划定：

- **资产类型**：支持物体和场景级 3D 资产（Fig. 1），但受限于 Trellis（Xiang et al., CVPR 2025）作为基础生成模型的表达范围——包括 64³ 体素分辨率和训练数据分布。
- **编辑操作**：覆盖增加（addition）、修改（modification）和删除（deletion）三种操作类型，支持多轮编辑（Fig. 1）。删除操作直接移除目标体素后仅执行 Stage 2 平滑，跳过了完整的反演-修复流程。
- **交互模式**：当前为单轮指令驱动的自动编辑流程，反演-修复过程需要完整的正向和反向整流流计算，在实时交互场景中存在计算开销。

### 3. 局限与开放问题

本文明确指出的局限及由此衍生的开放问题包括：

**MLLM 的 3D 空间理解**。当前 MLLM 主要在 2D 数据上训练，对 3D 空间关系的理解有限，可能影响复杂场景下的定位准确性。一个自然的问题是：如何让 MLLM 直接消费 3D 输入（如点云或神经场）并进行原生 3D 推理，而非仅依赖 2D 渲染图像？

**分割粒度依赖**。编辑区域的检测依赖 PartField 的分割粒度，分割过粗或过细都会影响后续掩码质量。未来更强的 3D 分割模型或通用的 3D 特征场能否进一步提升编辑区域的检测精度，是值得追踪的方向。

**基础模型瓶颈**。继承自 Trellis 的生成分辨率（64³ 体素）和训练数据规模限制了细节保真度。随着原生 3D 生成模型的持续进步，编辑质量的提升是可预期的。

**交错去噪的理论分析**。交错 Trellis-text 和 Trellis-image 去噪策略在实验中表现出优势，但如何在理论上平衡文本与图像条件的贡献、是否存在更优的调度方案，仍是开放问题。

**范式扩展性**。能否将相同的 Agent 范式扩展到包含动态场景、光照编辑或物理属性的通用 3D 编辑，是该方法论能否产生更广泛影响的关键。

### 4. 公平性说明

在解读 Table 1 的定量结果时需注意：Vinedresser3D 在未编辑区域保持指标（PSNR/SSIM）上弱于直接用 Trellis 生成的结果（PSNR 29.45 vs 37.35），但换来了更好的编辑语义对齐（CLIP-T 0.252 vs 0.247）。这一 trade-off 反映了编辑任务中“保真度-对齐度”的内在张力：主动修改区域必然偏离原始资产，而自动掩码的不完美进一步放大了这种偏离。Ours w/ HM（人工掩码）的设置展示了理想掩码下的性能上限，应将其理解为编辑区域检测模块的 oracle 参考，而非完全自动方法的直接对比。



## 原文 PDF

![[paperPDFs/CVPR_2026/Vinedresser3D_Towards_Agentic_Text_guided_3D_Editing.pdf]]
