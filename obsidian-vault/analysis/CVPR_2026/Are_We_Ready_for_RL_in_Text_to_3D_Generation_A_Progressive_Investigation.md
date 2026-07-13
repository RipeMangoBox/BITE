---
title: Are We Ready for RL in Text-to-3D Generation? A Progressive Investigation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Are_We_Ready_for_RL_in_Text_to_3D_Generation_A_Progressive_Investigation.pdf
project_link: null
code_link: "https://github.com/Ivan-Tang-3D/3DGen-R1"
aliases:
- AWRRT3GPI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: Hi-GRPO通过分解粗到细的分层生成过程，并利用分步奖励集成，使得RL训练能够针对3D生成的全局结构和局部纹理分别进行优化。
primary_logic: 3D自回归生成具有内在的从全局几何到局部纹理的层次化进展，利用这一特性进行分层RL训练，并结合专门设计的奖励模型（尤其是人类偏好奖励和通用多模态模型的3D一致性评估），可以显著提升生成质量。
claims:
- AR3D-R1在MME-3DR和Toys4K基准上均达到最优结果，显著超过ShapeLLM-Omni和Trellis。
- Hi-GRPO的分步奖励系统（特别是Step-1特定奖励的引入）带来CLIP分数2.1点的提升。
- 与直接生成相比，文本推理引导的GRPO提升了0.9点CLIP分数，并改善了全局规划。
- HPS V2.1作为核心奖励信号，结合3D一致性评估（使用通用LMM）能进一步提升性能。
---

# Are We Ready for RL in Text-to-3D Generation? A Progressive Investigation

> [!tip] 核心洞察
> 3D自回归生成具有内在的从全局几何到局部纹理的层次化进展，利用这一特性进行分层RL训练，并结合专门设计的奖励模型（尤其是人类偏好奖励和通用多模态模型的3D一致性评估），可以显著提升生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 我们准备好将RL应用于文本到3D生成了吗？一项渐进式研究 |
| 英文题名 | Are We Ready for RL in Text-to-3D Generation? A Progressive Investigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.10949) · [Code](https://github.com/Ivan-Tang-3D/3DGen-R1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | AR3D-R1 |
| Dataset | MME-3DR, Toys4K |

> [!tip] 效果简介
> - MME-3DR 上，CLIP Score↑ 28.5 vs 22.7 (ShapeLLM-Omni) / 27.2 (Trellis) (+5.8 / +1.3)；KD_incep↓ 0.194 vs 0.249 (ShapeLLM-Omni) / 0.208 (Trellis) (-0.055 / -0.014)。
> - Toys4K 上，CLIP Score↑ 29.3 vs 22.7 (ShapeLLM-Omni) / 28.1 (Trellis) (+6.6 / +1.2)；KD_incep↓ 0.156 vs 0.249 (ShapeLLM-Omni) / 0.168 (Trellis) (-0.093 / -0.012)。

## 概要

**研究问题**：强化学习（RL）已在文本和图像生成中展现出显著潜力，但其在文本到3D生成领域的适用性尚不明朗。核心瓶颈在于，3D生成任务具有更高的空间复杂度和全局一致性要求，现有的RL策略无法直接迁移，且缺乏能够评估模型内隐推理能力的基准。

**核心发现**：本文通过一项渐进式研究，系统揭示了RL在文本到3D生成中的可行路径。研究发现，3D自回归生成具有内在的从全局几何到局部纹理的层次化进展——利用这一特性进行分层RL训练，并结合专门设计的奖励模型，可以显著提升生成质量。在此基础上，本文提出了**AR3D-R1**，首个RL增强的3D自回归模型，并配套设计了**Hi-GRPO**分层优化算法。

**方法定位**：AR3D-R1以**ShapeLLM-Omni**（Ye et al., arXiv 2025）为基础3D自回归模型，将单步生成范式改造为两阶段分层生成——先生成语义推理与粗网格，再生成视觉推理与精网格。Hi-GRPO针对这一分层过程，将基础GRPO算法（Shao et al., 2024）升级为解耦裁剪、token级损失和动态采样的版本，并设计了分步专家奖励集成系统，包括HPS v2.1人类偏好奖励、UnifiedReward美学评估，以及基于通用多模态模型的3D一致性检查。

**主要结果**：在MME-3DR和Toys4K基准上，AR3D-R1均达到最优结果——CLIP分数分别达到28.5和29.3，显著超过基础模型ShapeLLM-Omni（22.7）和当前先进的扩散模型**Trellis**（Xiang et al., CVPR 2025）（27.2/28.1）。消融实验表明，Hi-GRPO的分步奖励系统带来CLIP分数2.1点的提升，文本推理引导的GRPO相比直接生成提升0.9点CLIP分数，验证了分层优化与推理引导的协同效应。

**局限与展望**：当前验证仅基于ShapeLLM-Omni单一架构，方法的通用性有待在其他3D表示（如网格、点云）上检验。奖励模型组合依赖特定模型，可能引入偏好偏差。未来方向包括将Hi-GRPO扩展至更大规模3D数据集，以及探索对抗性奖励以增强生成多样性与物理合理性。

### 文本到3D生成中的强化学习困境

强化学习（RL）在文本生成和图像生成领域已展现出显著的价值——在文本生成中，RL能够诱导模型产生显式的文本推理（textual reasoning）；在2D自回归生成中，RL主要改善token级别的生成质量。然而，在文本到3D生成任务中，RL的应用仍处于几乎空白的状态。这一现状背后的核心瓶颈在于：**3D生成任务具有更高的空间复杂度和全局一致性要求**，现有的RL策略无法直接迁移，且缺乏能够评估模型内隐推理能力的基准。

Figure 1 清晰展示了这一跨模态的差异：左侧对比了RL在文本、图像和3D生成中的不同作用机制，右侧则呈现了不同策略对RL性能的影响。该图以ShapeLLM-Omni为基线模型，初步揭示了RL在3D生成中的潜力与挑战。

### 现有方法的缺口

当前文本到3D生成领域存在两个关键缺口：

**其一，RL算法与3D生成特性的不匹配。** 基础RL算法如GRPO（Shao et al., 2024）在3D自回归生成中面临训练不稳定、熵坍缩等问题。后续变体如DAPO（Yu et al., 2025）通过解耦裁剪边界和动态采样缓解了部分问题，GSPO（Yang et al., 2025）则将优化提升至序列级别以应对token级优化的波动。然而，这些算法均未考虑3D生成的内在层次结构——从全局几何到局部纹理的粗到细（coarse-to-fine）进展，导致优化目标与生成过程之间存在结构性错位。

**其二，奖励模型设计缺乏3D特异性。** 现有奖励模型多为2D导向，如HPS v2.1评估人类偏好、UnifiedReward评估美学质量与提示对齐，但缺乏对3D一致性（如几何连贯性、纹理与光照协调性）的专门评估。Figure 2 的可视化对比表明，不同奖励模型对生成结果的影响差异显著，3D一致性奖励能有效增强物体在颜色、纹理和几何上的连贯性。

### 本文动机：渐进式RL探索

针对上述缺口，本文提出一项渐进式研究，系统探索RL在文本到3D生成中的可行性。核心动机源于一个关键观察：**3D自回归生成具有内在的从全局几何到局部纹理的层次化进展**，利用这一特性进行分层RL训练，并结合专门设计的奖励模型，可以显著提升生成质量。

具体而言，本文的探索路径包含三个递进层次：

1. **文本推理引导**：让模型首先生成文本推理，再基于推理生成3D标记，验证推理引导对3D生成的有效性（Table 3）。
2. **分层RL范式**：提出Hi-GRPO，将3D生成解耦为粗到细的两个步骤——Step 1生成高级语义推理和粗网格，Step 2生成低级视觉推理和精网格（Figure 6），并设计分步奖励集成（Figure 7）。
3. **奖励模型集成**：构建包含HPS v2.1、UnifiedReward、Qwen2.5-VL（2D LMM）和ShapeLLM（3D LMM）的专家奖励集成，分别评估全局对齐和局部细化。

最终，基于这些策略构建的AR3D-R1成为首个RL增强的3D自回归模型，旨在回答一个根本性问题：**我们是否已经准备好将RL应用于文本到3D生成？**

## 核心方法与创新机理

AR3D-R1 的核心创新在于将强化学习（RL）首次系统性地引入文本到3D自回归生成，并围绕3D生成的层次化本质设计了分层RL范式 **Hi-GRPO**。与现有方法相比，其关键变化体现在以下五个维度：

### 1. 生成范式：从单步生成到两阶段分层生成

基础模型 **ShapeLLM-Omni**（Ye et al., arXiv 2025）采用单步生成3D体素网格的方式，缺乏对生成过程的显式分解。AR3D-R1 将其重构为 **两阶段分层生成**（Figure 6）：
- **Step 1（高层语义规划）**：模型首先生成描述全局结构和组件布局的语义推理文本，再基于提示和该推理生成粗粒度3D形状。
- **Step 2（低层视觉细化）**：在高层语义推理的引导下，生成聚焦于局部纹理和细节的视觉推理，进而产生精细化3D对象。

这一设计利用了3D自回归生成“从全局几何到局部纹理”的内在层次化进展，使得RL训练能够分别针对全局结构和局部细节进行优化。

### 2. RL算法：从GRPO到Hi-GRPO

基础RL算法 **GRPO**（Shao et al., 2024）采用组内标准化优势估计和序列级损失优化，但在3D生成场景下存在训练不稳定和熵坍缩问题。AR3D-R1 提出的 **Hi-GRPO** 引入了四项关键改进（Table 2, Appendix B.3）：
- **解耦裁剪（Decoupled Clip）**：将策略更新的上下界分离，增强探索能力，避免GRPO中对称裁剪导致的策略坍缩。
- **Token级平均损失（Token Avg.）**：将序列级损失替换为token级平均损失，使梯度信号更均匀地分配到每个生成步骤，CLIP分数提升 **+0.6**。
- **KL正则化保留**：采用token级KL散度（$\beta=0.01$）约束策略偏离参考模型的幅度，完全移除KL惩罚会导致性能下降。
- **动态采样（Dynamic Sampling）**：根据训练进程自适应调整采样策略，稳定训练过程。

Hi-GRPO 的总损失为两步损失之和：$\mathcal{L}_{\mathrm{total}} = \mathcal{L}^{(1)} + \mathcal{L}^{(2)}$，其中高层奖励通过 $R_{\mathrm{high}} = R_{\mathrm{high}} + \lambda \cdot R_{\mathrm{low}}$ 接收来自低层步骤的反馈信号。

### 3. 奖励模型：从单一奖励到分步专家奖励集成

基础方案仅使用 **HPS v2.1** 单一人类偏好奖励。AR3D-R1 设计了 **分步专家奖励集成系统**（Figure 7, Table 5）：
- **Step 1 奖励**：聚焦全局对齐，引入专门的高层几何对齐奖励（组件级奖励 $R_i^{\mathrm{part},2} = \frac{1}{N_c}\sum_{p=1}^{N_c}(e_p + q_p)$，基于ShapeLLM评估组件存在性和完整性）。引入该奖励带来 CLIP 分数 **+2.1** 的提升。
- **Step 2 奖励**：聚焦局部细化，联合使用 HPS v2.1、UnifiedReward-2.0-Qwen7B（美学质量与提示对齐）和 Qwen2.5-VL（3D一致性评估）。通用多模态模型对3D一致性的评估额外贡献 **+0.6** CLIP 提升。

仅使用Step-1奖励会导致纹理质量下降，仅用Step-2奖励无法有效控制几何形状，两者结合取得最佳效果。

### 4. 推理引导：从直接生成到文本推理引导

基础模型直接根据文本提示生成3D标记，缺乏中间推理环节。AR3D-R1 引入 **文本推理引导机制**（Table 3）：模型首先生成描述对象想象和规划的文本推理，再基于该推理生成3D内容。仅此一项改进，在GRPO框架下即带来 CLIP 分数 **+0.9** 的提升，并改善了全局规划能力。这表明文本推理为3D生成提供了有效的语义锚点，使RL优化更具方向性。

### 5. 算法对比与融合

AR3D-R1 系统对比了 GRPO、**DAPO**（Yu et al., 2025）和 **GSPO**（Yang et al., 2025）三种RL算法在3D生成中的适用性（Table 2）。DAPO 的解耦裁剪和token级损失聚合被证明对3D生成有效，但其序列级重要性采样在3D场景下效果有限；GSPO 的序列级优化在3D生成中表现不如token级优化。Hi-GRPO 融合了各算法的优势组件，形成针对3D层次化生成的最优配置。

**证据强度**：上述创新点的核心证据（Table 4-6, Table 2-3）置信度在 0.9-0.95 之间，均来自论文内部消融实验和基准对比。需注意所有RL训练均基于 ShapeLLM-Omni 单一架构，扩展至其他3D生成模型（如扩散模型 Trellis）的通用性有待验证。

AR3D-R1 的整体框架围绕一个核心洞察构建：**3D 自回归生成天然具有从全局几何到局部纹理的层次化进展**。基于此，方法将强化学习训练解耦为粗到细的分层过程，使策略优化与3D生成的固有结构对齐。

### Pipeline 总览

整个 pipeline 由 **Hi-GRPO** 算法驱动，在单次迭代中完成两个阶段的联合优化。图6给出了框架的完整示意：输入为文本提示，输出为经过语义推理引导的精细化3D对象。

**Step 1：高层语义规划与粗粒度生成**
1. **语义推理模块**：模型基于3D提示首先生成高层语义推理（semantic reasoning），描述对象的全局结构、组件布局和空间关系。
2. **粗粒度3D生成模块**：将提示与语义推理共同作为条件，生成粗粒度3D标记（tokens），经解码和重建得到粗略的3D形状。

**Step 2：低层视觉推理与精细化生成**
3. **视觉推理模块**：以3D提示和高层语义思维链为条件，模型生成低层视觉推理（visual reasoning），聚焦于局部外观细节、纹理和几何细化。
4. **精细化3D生成模块**：基于提示、语义推理和视觉推理的联合条件，生成精细化3D标记，最终输出高质量3D对象。

### 奖励集成与策略更新

两个步骤分别配备**专用奖励集成**（图7），形成分层奖励体系：
- **Step 1 奖励**：聚焦全局对齐，包括 CLIP 分数、HPS v2.1 人类偏好奖励、UnifiedReward 联合美学与提示对齐评估，以及组件完整性检查。
- **Step 2 奖励**：强调局部细化，在全局奖励基础上引入基于通用多模态模型（Qwen2.5-VL）的3D一致性评估，以及基于 ShapeLLM 的组件存在性与完整性得分（$R_i^{\mathrm{part},2}$）。

奖励信号通过公式 $R_{\mathrm{high}} = R_{\mathrm{high}} + \lambda \cdot R_{\mathrm{low}}$ 将步骤2的低级奖励反传至步骤1，权重 $\lambda$ 控制层级间的梯度流动。

**Hi-GRPO 策略更新模块**接收两个步骤的损失 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}^{(1)} + \mathcal{L}^{(2)}$，采用解耦裁剪（decoupled clipping）、token级平均损失（替代序列级操作）、KL正则化（$\beta=0.01$）和动态采样进行策略更新。Token级KL散度定义为：

$$\mathbf{KL}_{i,t}^{(k)} = \frac{\pi_{\mathrm{ref}}(y_{i,t}^{(k)}|\mathbf{y}_{i,<t}^{(k)})}{\pi_{\theta}(y_{i,t}^{(k)}|\mathbf{y}_{i,<t}^{(k)})} - \log\frac{\pi_{\mathrm{ref}}(y_{i,t}^{(k)}|\mathbf{y}_{i,<t}^{(k)})}{\pi_{\theta}(y_{i,t}^{(k)}|\mathbf{y}_{i,<t}^{(k)})} - 1$$

### 与基线的关键差异

相比基础模型 **ShapeLLM-Omni**（Ye et al., arXiv 2025）的单步生成范式，AR3D-R1 的核心改变体现在：
- **生成范式**：从单步体素网格生成转为两阶段分层生成，引入文本推理作为中间引导。
- **RL算法**：从标准 GRPO（Shao et al., 2024）升级为 Hi-GRPO，融合了 DAPO（Yu et al., 2025）的解耦裁剪、动态采样和 token 级损失聚合，同时保留 KL 正则化以避免性能下降。
- **奖励模型**：从 HPS v2.1 单一奖励扩展为分步专家奖励集成，引入 3D 一致性评估和组件级奖励。

消融实验表明，token级平均损失优于序列级操作，动态采样带来 +0.6 CLIP 的稳定提升，而完全移除 KL 惩罚会导致性能下降（Table 2）。

![[assets/figures/papers/paper_list_l2201_https_arxiv_org_abs_2512_10949/figures/009_Figure_6.jpg]]
*Figure 6: Framework of Hi-GRPO. In Step 1, we instruct the model to generate high-level semantic reasoning based on the 3D prompt, and use it together with the prompt to produce a coarse 3D shape. In Step 2, conditioned on the 3D prompt and the high-level semantic CoT, the model generates low-level visual reasoning focused on local appearance details, which is used to produce the refined 3D object*

### 分层生成范式与Hi-GRPO框架

AR3D-R1的核心创新在于将3D自回归生成从单步预测重构为**从全局几何到局部纹理的层次化推理生成过程**，并通过专门设计的Hi-GRPO算法进行联合优化。该框架包含两个顺序步骤，每一步均整合文本推理与3D标记生成（Figure 6）：

- **Step 1 — 语义推理与粗粒度生成**：模型首先基于3D提示生成高级语义推理（描述全局结构、组件布局与空间关系），随后结合提示与语义推理生成粗粒度3D标记，解码为初始网格。
- **Step 2 — 视觉推理与精细化生成**：以3D提示和Step 1的语义推理为条件，模型生成低级视觉推理（聚焦局部纹理、细节和外观属性），并据此产出精细化3D标记，完成高质量重建。

Hi-GRPO的关键设计在于**分层奖励集成**（Figure 7）：Step 1的奖励侧重全局对齐（使用HPS v2.1、UnifiedReward-2.0-Qwen7B及基于ShapeLLM的组件存在性评估），Step 2的奖励侧重局部精细化（引入Qwen2.5-VL进行3D一致性评估，检查颜色、纹理与几何的跨视角连贯性）。为建立两步间的因果联系，Step 2的低级奖励通过加权系数 $\lambda$ 反向传播至Step 1：

![[assets/figures/papers/paper_list_l2201_https_arxiv_org_abs_2512_10949/figures/010_Figure_7.jpg]]
*Figure 7: Illustration of the Reward Ensemble Design. We design reward ensembles for steps in Hi-GRPO: step 1 focuses on global alignment, while step 2 emphasizes local refinement*

$$R_{\text{high}} = R_{\text{high}} + \lambda \cdot R_{\text{low}}$$

该机制使全局结构优化能感知局部精细化结果，实现端到端的层次化策略更新。

### 核心公式体系

**GRPO优势函数**（基础算法，Sec. 3, Eq. 1）：

$$A_i = \frac{R_i - \mathrm{mean}(\{R_i\}_{i=1}^G)}{\mathrm{std}(\{R_i\}_{i=1}^G)}$$

其中 $G$ 为每组采样数量（$G=8$），$R_i$ 为第 $i$ 个样本的奖励值。该标准化优势值替代了PPO中的价值函数，通过组内相对比较驱动策略更新。

**Hi-GRPO总损失**（Appendix B.3, Eq. 14）：

$$\mathcal{L}_{\text{total}} = \mathcal{L}^{(1)} + \mathcal{L}^{(2)}$$

$\mathcal{L}^{(1)}$ 和 $\mathcal{L}^{(2)}$ 分别为Step 1和Step 2的独立策略损失，两者共享模型参数但基于不同的奖励信号与优势值计算。

**Token级KL散度正则化**（Appendix B.3, Eq. 13）：

$$\mathbf{KL}_{i,t}^{(k)} = \frac{\pi_{\text{ref}}(y_{i,t}^{(k)}|\mathbf{y}_{i,<t}^{(k)})}{\pi_{\theta}(y_{i,t}^{(k)}|\mathbf{y}_{i,<t}^{(k)})} - \log\frac{\pi_{\text{ref}}(y_{i,t}^{(k)}|\mathbf{y}_{i,<t}^{(k)})}{\pi_{\theta}(y_{i,t}^{(k)}|\mathbf{y}_{i,<t}^{(k)})} - 1$$

其中 $\pi_{\theta}$ 为当前策略，$\pi_{\text{ref}}$ 为参考策略（初始模型），$y_{i,t}^{(k)}$ 表示第 $i$ 个样本在第 $k$ 步生成的第 $t$ 个标记。该token级KL惩罚（系数 $\beta=0.01$）替代传统序列级约束，能更精细地控制策略偏移，防止训练崩溃。

**组件完整性奖励**（Appendix B.2.4）：

$$R_i^{\text{part},2} = \frac{1}{N_c}\sum_{p=1}^{N_c}(e_p + q_p)$$

$N_c$ 为检测到的组件数量，$e_p$ 和 $q_p$ 分别表示ShapeLLM评估的组件存在概率和完整性得分。该奖励仅在Step 2中应用，确保精细化阶段关注局部结构的完整呈现。

### 算法改进要点

Hi-GRPO相较于基础GRPO（Shao et al., 2024）引入了四项关键技术改进（Table 2消融验证）：

1. **解耦裁剪**：为上下界设置独立裁剪范围，增强探索能力，避免熵坍缩。
2. **动态采样**：根据训练进度自适应调整采样策略，稳定训练过程（+0.6 CLIP分数提升）。
3. **Token级平均损失**：将序列级损失替换为token级平均，更精确地分配优化信号。
4. **KL正则化保留**：完全移除KL惩罚会导致性能下降，验证了token级约束的必要性。

这些改进源自对DAPO（Yu et al., 2025）和GSPO（Yang et al., 2025）等GRPO变体的系统分析，最终组合形成了适合3D层次化生成的最佳RL配置。

## 实验与关键发现

### 4.1 实验设置与基准

所有实验基于自回归3D生成模型 **ShapeLLM-Omni**（Ye et al., arXiv 2025）进行RL微调。评估采用两个基准：**Toys4K**（通用文本到3D生成评估）和 **MME-3DR**（包含249个复杂3D对象，覆盖空间与结构几何、生物与有机形状、风格化表示、机械功能、世界知识稀有物体五类，用于评估模型内隐推理能力）。主要指标为 **CLIP Score**（↑，越高越好）和 **KD_incep**（↓，越低越好，表中报告为×100）。对比基线包括基础模型 ShapeLLM-Omni 和当前先进的文本到3D扩散模型 **Trellis**（Xiang et al., CVPR 2025）。所有RL训练中，组大小 $G=8$，KL惩罚系数 $\beta=0.01$。

### 4.2 主实验结果

**AR3D-R1 在两个基准上均达到最优。** 如 Table 4 所示，在 MME-3DR 上，AR3D-R1 的 CLIP Score 达到 28.5，较 ShapeLLM-Omni（22.7）提升 +5.8，较 Trellis（27.2）提升 +1.3；KD_incep 降至 0.194，较 ShapeLLM-Omni（0.249）降低 -0.055，较 Trellis（0.208）降低 -0.014。在 Toys4K 上，CLIP Score 达到 29.3（+6.6 / +1.2），KD_incep 降至 0.156（-0.093 / -0.012）。

**关键发现：** MME-3DR 上 AR3D-R1 对 ShapeLLM-Omni 的提升幅度（+5.8 CLIP）显著大于 Toys4K 上的提升（+6.6），但考虑到 MME-3DR 包含更多需要隐式推理的复杂对象（Figure 4 左），这表明 RL 训练有效增强了模型的推理能力。Figure 4 右的可视化对比进一步证实，AR3D-R1 在需要空间理解和结构推理的类别上优势尤为突出。

**定性结果**（Figure 8、Figure 12-16）显示，AR3D-R1 生成的3D资产在全局几何一致性和局部纹理细节上均优于基线。Figure 9 展示了推理过程中不同步骤的生成结果：步骤1产生粗粒度全局结构，步骤2在此基础上细化局部细节，验证了分层生成的有效性。

### 4.3 奖励模型分析

**HPS v2.1 是核心奖励信号。** Table 1 系统比较了不同奖励模型组合在 Toys4K 上的效果。以 GRPO 为基础算法，单一使用 HPS v2.1 时 CLIP Score 达到 24.0（基线 22.7），是所有单一奖励中最强的。将 HPS v2.1 与 **UnifiedReward-2.0-Qwen7B**（联合评估美学质量和提示对齐）组合后，CLIP Score 进一步提升至 24.6，KD_incep 降至 0.235。

**3D一致性评估带来额外增益。** 引入通用多模态大模型 **Qwen2.5-VL** 评估3D一致性（颜色、纹理、几何的连贯性）后，CLIP Score 额外提升 0.6 点。Figure 2 的可视化结果证实，3D一致性奖励有效增强了生成对象在颜色、纹理和几何上的连贯性（如吉他和海豚案例）。Table 1 数据表明，HPS + UnifiedReward 组合优于 HPS + Qwen2.5-VL 组合（CLIP 差距 0.4），说明人类偏好奖励和美学评估的组合对3D生成更为关键，但一致性检查作为辅助信号仍有价值。

### 4.4 RL算法对比与消融

**Token级平均损失和动态采样是关键改进。** Table 2 系统比较了 GRPO、**DAPO**（Yu et al., 2025）和 **GSPO**（Yang et al., 2025）三种RL算法及其组件在 Toys4K 上的表现。基线 GRPO 的 CLIP Score 为 24.0。引入 DAPO 的解耦裁剪（Decoupled Clip）和动态采样（Dynamic Sampling）后提升至 24.4；进一步引入 Token级平均损失（Token Avg.）达到 24.6（+0.6 vs. 序列级损失）。GSPO 的序列级优化（Seq. Opt.）表现不如 Token 级方案，说明3D自回归生成中 Token 级优化更适合捕捉局部细节。

**KL正则化不可或缺。** 完全移除 KL 惩罚（KL Remov.）导致性能下降，验证了 KL 正则化对稳定训练的必要性。

### 4.5 文本推理引导的有效性

**文本推理先于3D生成能提升全局规划能力。** Table 3 的消融显示，使用 HPS v2.1 作为奖励、GRPO 作为算法，引入文本推理引导（WI）后 CLIP Score 从无推理的 23.4 提升至 24.0（+0.6），较基础模型（22.7）提升 +1.3。这表明让模型先“想象”并描述对象，再基于描述生成3D，能有效改善全局结构规划。

### 4.6 Hi-GRPO 分层奖励消融

**分步奖励集成是 Hi-GRPO 的核心贡献。** Table 5 的奖励分析显示，引入步骤1特定奖励（高等级几何对齐，基于 ShapeLLM 评估的组件存在性和完整性）带来 CLIP Score 2.1 点的显著提升，表明组件级奖励对正确零件定位和结构至关重要。

**两步奖励必须联合使用。** Table 6 比较了不同RL范式：仅使用步骤1奖励（侧重全局几何）会导致纹理质量下降；仅使用步骤2奖励（侧重局部细节）无法有效控制几何形状。Hi-GRPO 结合两步奖励取得最佳效果（CLIP 29.3），验证了分层奖励设计的必要性。此外，文本推理引导的 GRPO（无分层）相比直接3D标记优化提升 0.9 点 CLIP，进一步确认了推理引导的价值。

### 4.7 缩放策略分析

**数据缩放和迭代缩放均需谨慎校准。** Figure 3 展示了数据规模和训练迭代次数的缩放效果。适度扩大训练数据（3×）能稳定提升 CLIP Score，但过度增加训练迭代次数会导致性能下降——论文分析这可能是过拟合于奖励模型的偏好特征所致。这一发现表明，3D生成的RL训练需要更精细的早停策略和奖励校准机制。

### 4.8 局限性与待验证问题

1. **通用性待验证：** 所有RL训练仅基于 ShapeLLM-Omni，Hi-GRPO 在其他3D生成架构（如扩散模型、点云生成）上的迁移效果未知。
2. **奖励偏差：** 奖励模型组合依赖 HPS v2.1 和 UnifiedReward，可能引入特定领域的偏好偏差；在更广泛的3D类别上的泛化性需要进一步检验。
3. **基准覆盖有限：** MME-3DR 虽涵盖多种推理类型，但仅包含249个对象，评估覆盖面有限。
4. **物理合理性未评估：** 未对生成3D资产的物理合理性（如结构稳定性）或多模态一致性（如纹理与光照匹配）进行评估。
5. **λ 敏感性：** Hi-GRPO 中步骤2奖励回传权重 $\lambda$ 的敏感性和自适应调整策略尚未系统研究。

![[assets/figures/papers/paper_list_l2201_https_arxiv_org_abs_2512_10949/figures/012_Table_4.jpg]]
*Table 4: Quantitative Comparison on Text-to-3D Generation Benchmarks. (KD is reported ×100. †: evaluated using shaded images of PBR meshes.)*

![[assets/figures/papers/paper_list_l2201_https_arxiv_org_abs_2512_10949/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparisons using Toys4k for Different RL algorithms. In DAPO, Clip, Sampling, Token Avg., and KL Remov. correspond to Decoupled Clip, Dynamic Sampling, Token-level Loss Aggregation, and KL Penalty Removal, respectively. For GSPO, Seq. Opt. indicates that both importance sampling and clipping are performed at the sequence level. (KD is reported ×100)*

![[assets/figures/papers/paper_list_l2201_https_arxiv_org_abs_2512_10949/figures/014_Table_5.jpg]]
*Table 5: Quantitative comparisons using Toys4k for Reward Analysis*

![[assets/figures/papers/paper_list_l2201_https_arxiv_org_abs_2512_10949/figures/015_Table_6.jpg]]
*Table 6: Quantitative comparisons using Toys4k for Different RL Paradigms*

## 定位与知识库关联

### 1. 与基线方法的关系

AR3D-R1的构建并非孤立创新，而是沿着“3D自回归生成→推理引导→强化学习增强”三条技术脉络的交叉点展开，其核心贡献在于首次将RL训练系统地引入文本到3D生成，并针对3D生成特有的空间复杂性和全局一致性瓶颈设计了分层优化方案。

**基础生成模型：ShapeLLM-Omni** (Ye et al., arXiv 2025)。AR3D-R1以此为RL微调的起点。ShapeLLM-Omni本身是一个3D自回归模型，采用单步生成体素网格的范式。AR3D-R1在此基础上进行了两项根本性改造：(1) 将单步生成范式替换为两阶段分层生成——先产生语义推理和粗网格，再产生视觉推理和精网格；(2) 引入文本推理引导，使模型在生成3D标记之前先进行语言层面的语义规划。这一改造的动机在于：3D自回归生成天然具有从全局几何到局部纹理的层次化进展特性，而ShapeLLM-Omni的单步范式无法利用这一内在结构。

**强化学习算法：GRPO** (Shao et al., 2024)。GRPO作为基础RL算法，通过移除价值函数、采用组内奖励比较的方式简化了PPO。AR3D-R1在GRPO的基础上提出了**Hi-GRPO**，核心改进包括：(1) 解耦裁剪（Decoupled Clip），分离上下界以增强探索并避免熵坍塌；(2) Token级平均损失，替代序列级操作以稳定梯度信号；(3) KL正则化（β=0.01），防止策略偏离参考模型过远；(4) 动态采样策略。与GRPO的两个变体——**DAPO** (Yu et al., 2025) 和**GSPO** (Yang et al., 2025)——相比，Hi-GRPO吸收了DAPO的解耦裁剪和Token级损失思想，但拒绝了GSPO的序列级优化路径，因为3D生成中token级别的细粒度反馈对局部纹理控制至关重要（Table 2显示Token级平均损失优于序列级操作，动态采样带来+0.6 CLIP提升）。

**奖励模型：HPS v2.1**。作为核心奖励信号，HPS v2.1输出人类偏好奖励。AR3D-R1在此基础上构建了分步专家奖励集成，引入UnifiedReward-2.0-Qwen7B（联合评估美学质量和提示对齐）和Qwen2.5-VL（通用多模态模型，用于3D一致性评估）。Table 1显示，HPS与UnifiedReward的组合优于HPS与Qwen2.5-VL的组合（CLIP分数提升0.4），但当Qwen2.5-VL专门用于评估3D一致性时，额外带来0.6的CLIP提升。这一发现揭示了3D生成奖励设计的关键原则：人类偏好奖励是基础，但需要3D一致性评估来约束空间连贯性。

**与扩散模型的对比：Trellis** (Xiang et al., CVPR 2025)。作为当前先进的文本到3D扩散模型，Trellis在MME-3DR上达到27.2 CLIP分数。AR3D-R1以28.5超越Trellis（+1.3），在Toys4K上以29.3对比28.1（+1.2）。这一超越的意义在于：它证明了经过RL增强的自回归模型可以在不依赖扩散去噪过程的情况下，达到甚至超越扩散模型的生成质量，同时保留了自回归模型在推理可控性方面的优势。

### 2. 适用边界与条件依赖

AR3D-R1的有效性建立在以下条件之上，超出这些边界时性能可能显著下降：

**模型架构依赖**：所有RL训练均基于ShapeLLM-Omni进行。该方法能否迁移到其他3D生成架构（如基于Transformer的扩散模型、NeRF-based生成器、点云自回归模型）尚待验证。特别是，Hi-GRPO的分层设计依赖于自回归模型能够显式分解为粗-细两个生成阶段，对于端到端的隐式生成模型，这种分解可能不自然。

**奖励模型偏差**：奖励集成严重依赖HPS v2.1和UnifiedReward，这些模型本身在训练数据和偏好标注上存在领域偏差。Table 5的消融显示，Step-1特定奖励（高等级几何对齐）带来2.1 CLIP提升，表明组件级奖励对正确零件定位至关重要——但这也意味着奖励模型的质量直接决定了生成质量的上限。如果奖励模型对某些几何结构或纹理风格存在盲区，RL训练会放大这些偏差。

**数据规模与训练迭代的敏感性**：Figure 3揭示了缩放策略的非单调性——数据扩展3倍带来提升，但训练迭代增加3倍反而导致性能下降。论文将此归因于“过拟合于偏好特征”，这意味着RL训练存在一个狭窄的最优窗口，需要小心校准迭代次数。在更大规模数据集上，这个窗口的位置和宽度可能发生变化。

**基准覆盖的局限性**：实验仅在Toys4K和MME-3DR上进行。MME-3DR虽然包含5个类别249个对象，覆盖空间结构、生物形态、风格化表示、机械功能和世界知识稀有物体，但样本量有限，且主要面向复杂推理场景。对于大规模开放域文本到3D生成，AR3D-R1的泛化能力尚未被验证。

### 3. 已知局限

论文明确承认或实验揭示的局限包括：

1. **架构通用性未验证**：仅基于ShapeLLM-Omni进行RL训练，方法的通用性有待在其他3D生成架构上验证。

2. **奖励模型组合的偏好偏差**：依赖HPS v2.1等特定模型，可能引入领域偏好偏差，且奖励模型的选择空间本身受限于可用的开源模型。

3. **训练迭代的脆弱性**：需要小心校准，过多会导致过拟合于偏好特征。目前缺乏自动化的早停或自适应调度机制。

4. **基准覆盖面有限**：MME-3DR仅包含249个对象，Toys4K规模也有限，未在大规模多样化数据上验证。

5. **物理合理性未评估**：未评估生成3D资产的物理合理性（如结构稳定性、部件连接合理性）或多模态一致性（如纹理与光照的物理匹配）。

6. **推理质量缺乏独立评估**：文本推理的质量如何定量评估尚不明确。Table 3显示文本推理引导带来0.9 CLIP提升，但推理本身是否正确、是否包含幻觉，缺乏独立的评估指标。

### 4. 开放问题

从AR3D-R1的工作出发，以下问题值得进一步探索：

**表示扩展**：如何将Hi-GRPO扩展到其他3D表示（如网格、点云、隐式场）或大规模生成？分层优化的思想是否适用于非体素表示？

**对抗性奖励**：RL训练能否进一步结合对抗性奖励来增强生成对象的真实性和多样性？当前的奖励模型都是判别式的，对抗性信号可能推动模型探索更广泛的生成空间。

**大规模验证**：在更大规模和更多样化的3D数据集上，RL的效果如何？Figure 3的数据缩放实验仅扩展到3倍，更大规模的缩放是否会出现新的瓶颈？

**推理模型的升级**：文本推理的质量是否可以通过更强大的推理模型（如OpenAI o3）进一步提升？当前使用的是模型自身的推理能力，引入外部推理模型可能带来质的飞跃。

**λ权重的自适应**：Hi-GRPO中分层奖励权重λ的敏感性和自适应调整策略。当前λ是固定的，但不同提示对全局结构和局部纹理的侧重不同，自适应的λ可能进一步提升性能。

**多模态一致性的评估**：如何将纹理-光照一致性、物理合理性等更全面的3D质量维度纳入RL奖励体系？这需要开发新的奖励模型或评估协议。

## 原文 PDF

![[paperPDFs/CVPR_2026/Are_We_Ready_for_RL_in_Text_to_3D_Generation_A_Progressive_Investigation.pdf]]
