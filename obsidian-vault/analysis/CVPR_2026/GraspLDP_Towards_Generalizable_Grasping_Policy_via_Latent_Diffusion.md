---
title: "GraspLDP: Towards Generalizable Grasping Policy via Latent Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GraspLDP_Towards_Generalizable_Grasping_Policy_via_Latent_Diffusion.pdf
project_link: null
code_link: null
aliases:
- GraspLDP
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在潜在扩散模型框架中注入抓取检测器的两个先验——① 在行动潜在空间中用抓取位姿引导去噪；② 提供几何驱动的可抓性视觉提示（graspness map）并辅以自监督重建——从而操控动作生成的精度与泛化性。
primary_logic: 将抓取检测的先验知识融入潜在扩散策略：通过潜在空间中的位姿引导和可抓性视觉提示，使生成的轨迹紧密贴合可行抓取配置，在保持实时性的同时大幅提升抓取精度和泛化能力。
claims:
- 与 Diffusion Policy 相比，GraspLDP 在域内抓取成功率提升 17.5%，空间、对象、视觉泛化分别提升 22.2%、46.8%、48.3%。
- 消融实验：移除 Graspness Cue 使域内成功率下降 2.9 点，移除 Latent Guidance 改用 Condition Guidance 则下降 6.8 点，证实各组件的独立贡献。
- 推理延迟仅比相同配置的扩散策略增加约 15%，保留实用实时性。
- LIBERO 仿真域内 (In Domain) 上 成功率 (SR, %) = 80.3
---

# GraspLDP: Towards Generalizable Grasping Policy via Latent Diffusion

> [!tip] 核心洞察
> 将抓取检测的先验知识融入潜在扩散策略：通过潜在空间中的位姿引导和可抓性视觉提示，使生成的轨迹紧密贴合可行抓取配置，在保持实时性的同时大幅提升抓取精度和泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | GraspLDP：面向可泛化抓取策略的潜在扩散模型 |
| 英文题名 | GraspLDP: Towards Generalizable Grasping Policy via Latent Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.22862) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GraspLDP |
| Dataset | LIBERO 仿真域内 |

> [!tip] 效果简介
> - LIBERO 仿真域内 (In Domain) 上，成功率 (SR, %) 80.3 vs 62.8 (Diffusion Policy) (+17.5)。
> - LIBERO 仿真对象泛化 (Object Generalization) 上，成功率 (SR, %) 58.2 vs 11.4 (Diffusion Policy) (+46.8)。
> - 真实世界组合 (ID&SG + OG + VG) 上，平均成功率 (Avg SR, %) 78.7 vs 37.0 (Diffusion Policy) (+41.7)。

## 概要

机器人抓取面临一个根本性瓶颈：现有模仿学习策略难以将抓取先验有效融入动作生成。抓取位姿与动作序列之间仅存在弱关联，而低语义的位姿表示与视觉输入并不匹配，导致抓取精度不足，且在空间、对象和视觉维度上的泛化能力均受限。

GraspLDP 的核心思路是将预训练抓取检测器的先验知识注入潜在扩散策略框架。具体而言，它在两个层面操控动作生成的精度与泛化性——① 在动作潜在空间中，利用抓取位姿引导去噪解码过程；② 提供几何驱动的可抓性视觉提示（graspness map），并辅以自监督重建目标，强化模型对可抓取区域的关注。这一设计使生成的轨迹紧密贴合可行抓取配置，在保持实时性的同时大幅提升抓取成功率和泛化能力。

在仿真实验中，GraspLDP 相较 **Diffusion Policy**（Chi et al., RSS 2023）在域内抓取成功率上提升 17.5 个百分点，空间、对象和视觉泛化分别提升 22.2、46.8 和 48.3 个百分点。真实世界组合场景下，平均成功率从 37.0% 提升至 78.7%。消融实验证实，可抓性视觉提示和潜在空间引导各自贡献独立且显著；推理延迟仅比同配置的 Diffusion Policy 增加约 15%，保留了实用实时性。

在方法谱系上，GraspLDP 区别于直接预测抓取位姿的经典方法（如 AnyGrasp）和从原始观测生成动作块的 Diffusion Policy，也与通用视觉‑语言‑动作模型 **OpenVLA**（Kim et al., arXiv 2024）及 **GraspVLA**（Hu et al., arXiv 2025）不同——它通过两阶段训练（动作潜在学习 + 潜在扩散）将抓取先验结构化地融入策略，而非将其作为简单的条件输入。当前方法已在刚体物体上得到充分验证，但对可变形、易碎物体及高度堆叠场景的泛化仍是待探索的开放问题。

机器人抓取是具身智能的核心任务，要求系统在多样化的物体、空间配置和视觉条件下可靠地完成操作。当前主流方法大致分为两脉：一是以 AnyGrasp 为代表的**抓取检测**方法，直接预测可行的抓取位姿；二是以 **Diffusion Policy**（Chi et al., RSS 2023）为代表的**模仿学习**方法，从未压缩的视觉观测中直接生成动作序列。然而，这两类方法之间存在显著的语义鸿沟——抓取检测器输出的低语义位姿难以与模仿学习所需的高维动作序列建立有效关联，导致策略在面对未见物体、新位姿或视觉干扰时泛化能力严重不足。

这一瓶颈的根源在于：现有模仿学习策略缺乏将抓取先验知识有效融入动作生成的机制。抓取位姿与动作序列之间是弱关联的，且低语义的位姿表示与视觉输入不匹配，使得模型难以学习到从“看到物体”到“精准抓取”的稳健映射。尽管一些工作尝试将抓取位姿作为条件输入拼接到观测中（Condition Guidance），但这种粗暴的注入方式并未从根本上解决表示空间不匹配的问题，泛化性能提升有限。

针对上述缺口，GraspLDP 提出了一个核心洞察：**将抓取检测的先验知识融入潜在扩散策略框架**。具体而言，该方法通过两个关键机制实现先验注入——在动作潜在空间中用抓取位姿引导去噪过程，同时提供几何驱动的可抓性视觉提示（graspness map）并辅以自监督重建目标。这一设计使生成的轨迹紧密贴合可行抓取配置，在保持实时性的同时大幅提升抓取精度和泛化能力。实验表明，与 Diffusion Policy 相比，GraspLDP 在域内抓取成功率提升 17.5%，空间、对象、视觉泛化分别提升 22.2%、46.8%、48.3%，推理延迟仅增加约 15%。

## 核心方法与创新机理

现有抓取策略通常沿两条独立路径演进：**抓取位姿预测**（如 Anygrasp）仅输出目标位姿而不生成完整动作序列，或**动作序列生成**（如 **Diffusion Policy**，Chi et al., RSS 2023）直接从视觉观测生成动作块却缺乏抓取先验的引导。这两种范式的割裂导致抓取位姿与动作序列之间仅存在弱关联，低语义的位姿表示难以与高维视觉输入有效匹配，从而限制了抓取精度和泛化能力。

GraspLDP 的核心创新在于**将预训练抓取检测器的先验知识系统地注入潜在扩散策略框架**，通过三个关键设计改变（changed slots）实现动作生成与抓取先验的深度融合：

### 1. 动作表征：从原始动作空间到抓取位姿引导的潜在空间

**Diffusion Policy** 等基线方法直接在高维观测空间中完成动作块的去噪生成，抓取位姿与动作序列之间缺乏显式关联。GraspLDP 引入**动作潜在学习（Action Latent Learning）** 模块，利用轻量 VAE 将动作块 $A$ 压缩为紧凑的潜在表示 $Z = \mathcal{E}(A)$，并在解码阶段注入抓取位姿 $\mathcal{G}$ 进行引导重构：

$$\hat{A} = \mathcal{D}(Z \oplus \mathcal{G})$$

这一设计使抓取位姿能够在低维潜在空间中直接调控动作生成方向，而非仅作为外部条件输入。VAE 通过重构损失与 KL 正则化联合训练：

$$\mathcal{L}_{VAE} = \mathrm{MSE}(A, \hat{A}) + \lambda \mathcal{L}_{KL}$$

### 2. 视觉条件：从纯 RGB 观测到几何驱动的可抓性视觉提示

基线方法仅使用腕部 RGB 图像作为视觉条件，缺乏对场景抓取可行性的显式感知。GraspLDP 提出**可抓性视觉提示（Graspness Cue）** 机制，利用抓取检测器生成的可抓性得分图 $M$ 构建增强观测 $O_{cue}$：

$$O_{cue}(j,k) = \begin{cases} O_{wrist}(j,k), & M(j,k) \le \tau \\ masked\\_color, & M(j,k) > \tau \end{cases}$$

该提示通过掩膜方式高亮可抓取区域，为扩散模型提供几何驱动的注意力引导。同时，引入**辅助自监督重建目标** $\mathcal{L}_{Recon.} = \mathrm{MSE}(O_{cue}, \hat{O}_{cue})$，强制模型从扩散中间表示中重建可抓性提示，进一步强化对抓取区域的关注。

### 3. 推理时抓取位姿选择：从简单筛选到启发式综合选择

基线方法通常直接使用检测器最高分抓取位姿或随机选择，忽略了当前末端执行器位姿与候选抓取位姿之间的空间关系。GraspLDP 提出**启发式位姿选择器（HPS）**，综合抓取得分与加权 SE(3) 测地距离进行最优选择：

$$d_{\mathcal{G}_j, W} = \sqrt{\xi^{\top} W \xi}$$

该策略在仿真消融实验（Table 3）中全面优于随机选择、最高分选择及最近距离选择，验证了空间邻近性在抓取位姿选择中的关键作用。

### 创新效果验证

消融实验（Table 2）量化了各组件的独立贡献：移除可抓性视觉提示（GC）使域内成功率下降 2.9 点，视觉泛化下降最为明显；移除潜在空间引导（LG）改用条件引导（CG）则使域内成功率下降 6.8 点，证实了在潜在空间中进行抓取位姿引导的设计优势。整体而言，GraspLDP 在域内抓取成功率上较 Diffusion Policy 提升 17.5%，空间、对象、视觉泛化分别提升 22.2%、46.8%、48.3%，且推理延迟仅增加约 15%，保持了实用实时性。

GraspLDP 的整体设计遵循“先压缩动作、再在潜在空间中注入抓取先验”的两阶段训练范式，其架构如 Figure 2 所示。核心思路是：**将预训练抓取检测器的几何先验融入潜在扩散策略，使生成的轨迹紧密贴合可行抓取配置**，从而在保持实时性的同时大幅提升抓取精度与泛化能力。

![[assets/figures/papers/paper_list_l2514_https_arxiv_org_abs_2602_22862/figures/002_Figure_2.jpg]]
*Figure 2: Framework of proposed GraspLDP. In Action Latent Learning stage action chunks are refined under the guidance of a grasp pose in latent space encoded by a VAE. In Diffusion on Latent Action Space stage the graspness cue is used to condition the diffusion model’s denoising process and to reconstruct for enhancement*

### 两阶段训练流程

**阶段一：动作潜在学习 (Action Latent Learning)**

此阶段的目标是为高维动作块构建一个紧凑、可解码的潜在空间，并在解码时引入抓取位姿引导。具体而言：

- 使用轻量级 VAE 编码器 $\mathcal{E}$ 将动作块 $A$ 压缩为潜在表示 $Z$：
  $$Z = \mathcal{E}(A)$$
- 解码器 $\mathcal{D}$ 从潜在表示与抓取位姿 $\mathcal{G}$ 的拼接中重构动作块：
  $$\hat{A} = \mathcal{D}(Z \oplus \mathcal{G})$$
- 训练损失由重构损失与 KL 正则化组成：
  $$\mathcal{L}_{VAE} = \mathrm{MSE}(A, \hat{A}) + \lambda \mathcal{L}_{KL}$$

这一设计使得抓取位姿能够在潜在空间中直接引导动作重构，为后续扩散阶段奠定基础。

**阶段二：潜在动作空间上的扩散 (Diffusion on Latent Action Space)**

在冻结的 VAE 潜在空间中，以视觉条件为输入进行扩散去噪。此阶段引入两个关键的抓取先验：

1. **可抓性视觉提示 (Graspness Cue)**：将预训练抓取检测器输出的可抓性得分图 $M$ 通过阈值 $\tau$ 掩膜处理，生成几何驱动的视觉提示 $O_{cue}$：
   $$O_{cue}(j,k) = \begin{cases} O_{wrist}(j,k), & M(j,k) \le \tau \\ masked\_color, & M(j,k) > \tau \end{cases}$$
   该提示叠加在腕部 RGB 图像上，作为扩散模型的条件输入。

2. **自监督重建目标**：从扩散中间表示重建 $O_{cue}$，以强化模型对可抓性区域的关注：
   $$\mathcal{L}_{Recon.} = \mathrm{MSE}(O_{cue}, \hat{O}_{cue})$$

扩散训练的总损失为去噪得分匹配损失与重建损失的加权和：
$$\mathcal{L}_{LDP} = \mathcal{L}_{Diff.} + \lambda_{Recon.} \mathcal{L}_{Recon.}$$

其中 $\mathcal{L}_{Diff.}$ 为标准潜在扩散损失：
$$\mathcal{L}_{Diff.} = \mathrm{MSE}\left(\epsilon^{k}, \epsilon_{\theta}(\bar{\alpha}_{k} \mathbf{Z}^{0} + \bar{\beta}_{k} \epsilon^{k}, O, k)\right)$$

### 推理预处理：启发式位姿选择器

推理阶段，GraspLDP 在调用扩散策略之前，通过 **启发式位姿选择器 (Heuristic Pose Selector, HPS)** 从抓取检测器输出的候选位姿中选取最优目标，如 Figure 3 所示。HPS 综合考虑抓取得分与当前末端执行器位姿的加权 SE(3) 测地距离：
$$d_{\mathcal{G}_j, W} = \sqrt{\xi^{\top} W \xi}$$

这一选择策略确保引导位姿既具有高抓取置信度，又在空间上与当前机械臂状态接近，从而提升动作生成的可行性与成功率。

### 输入输出流总结

| 阶段 | 输入 | 输出 | 关键模块 |
|------|------|------|----------|
| 训练阶段一 | 动作块 $A$、抓取位姿 $\mathcal{G}$ | 重构动作块 $\hat{A}$ | VAE 编码器 $\mathcal{E}$、解码器 $\mathcal{D}$ |
| 训练阶段二 | 腕部 RGB + 可抓性提示 $O_{cue}$、噪声潜在表示 | 去噪潜在表示、重建 $O_{cue}$ | 潜在扩散模型 $\epsilon_{\theta}$ |
| 推理 | 腕部 RGB、抓取检测器输出 | 动作块序列 | HPS + 潜在扩散 + VAE 解码器 |

### 与基线方法的本质差异

与 **Diffusion Policy**（Chi et al., RSS 2023）直接在高维观测-动作空间去噪不同，GraspLDP 将去噪过程迁移至潜在空间，并在解码阶段注入抓取位姿引导。与简单地将抓取位姿作为条件输入拼接至观测的 **Condition Guidance** 消融基线相比，GraspLDP 的潜在引导设计使抓取位姿在动作潜在空间中直接参与重构，证据表明这一设计使域内成功率提升 6.8 个百分点（Table 2）。

GraspLDP 采用**两阶段训练**的潜在扩散模型框架（Figure 2）。第一阶段学习动作潜在空间，第二阶段在该空间中进行条件扩散去噪，并在推理时引入启发式位姿选择器。以下逐一解析各模块的设计逻辑与核心公式。

### 动作潜在学习 (Action Latent Learning)

**设计动机**：原始动作块（action chunk）维度较高，直接在观测空间进行扩散去噪效率低且难以融入抓取先验。本模块通过轻量 VAE 将动作块压缩为紧凑的潜在表示，并在解码阶段注入抓取位姿引导，使重构的动作块天然偏向可行抓取配置。

**编码**：给定动作块 $A$，VAE 编码器将其映射到潜在空间：

$$Z = \mathcal{E}(A)$$

**解码**：将潜在表示 $Z$ 与抓取位姿特征 $\mathcal{G}$ 拼接后解码，重构动作块：

$$\hat{A} = \mathcal{D}(Z \oplus \mathcal{G})$$

**训练损失**：VAE 的优化目标由重构损失与 KL 正则化组成：

$$\mathcal{L}_{VAE} = \mathrm{MSE}(A, \hat{A}) + \lambda \mathcal{L}_{KL}$$

该阶段的核心因果机制在于：抓取位姿 $\mathcal{G}$ 仅在解码时注入，迫使编码器学习与抓取无关的紧凑动作表征，而解码器则学会在给定抓取目标时生成朝向该目标的动作序列。这一设计使得后续扩散模型可以在低维潜在空间中高效运行，同时保留抓取引导的能力。

### 潜在扩散与可抓性视觉提示 (Latent Diffusion with Graspness Cue)

**设计动机**：第二阶段在潜在空间中进行条件扩散去噪。为使扩散模型感知“何处可抓”，引入几何驱动的可抓性视觉提示（Graspness Cue），并辅以自监督重建目标强化模型对该提示的关注。

**可抓性视觉提示构造**：利用预训练抓取检测器输出的可抓性得分图 $M$，将高分区域（$M(j,k) \le \tau$）保留原始腕部 RGB 图像像素，低分区域覆盖为掩膜颜色：

$$O_{cue}(j,k) = \begin{cases} O_{wrist}(j,k), & M(j,k) \le \tau \\ masked\_color, & M(j,k) > \tau \end{cases}$$

**扩散损失**：在潜在空间中执行标准去噪得分匹配，以视觉条件 $O$（包含可抓性提示）为条件：

$$\mathcal{L}_{Diff.} = \mathrm{MSE}\left(\epsilon^{k}, \epsilon_{\theta}(\bar{\alpha}_{k} \mathbf{Z}^{0} + \bar{\beta}_{k} \epsilon^{k}, O, k)\right)$$

其中 $\mathbf{Z}^{0}$ 为干净的动作潜在表示，$\epsilon^{k}$ 为第 $k$ 步的噪声，$\bar{\alpha}_{k}$ 与 $\bar{\beta}_{k}$ 为噪声调度参数。

**自监督重建辅助损失**：从扩散模型的中间表示重建可抓性视觉提示，强制模型在去噪过程中持续关注可抓性信息：

$$\mathcal{L}_{Recon.} = \mathrm{MSE}(O_{cue}, \hat{O}_{cue})$$

**总损失**：扩散损失与重建损失的加权组合：

$$\mathcal{L}_{LDP} = \mathcal{L}_{Diff.} + \lambda_{Recon.} \mathcal{L}_{Recon.}$$

该模块的因果机制在于：可抓性视觉提示将几何驱动的抓取先验转化为视觉条件，自监督重建目标则确保扩散模型在去噪过程中不丢失这一关键信息，从而生成更精准的抓取动作。

### 启发式位姿选择器 (Heuristic Pose Selector, HPS)

**设计动机**：推理时，预训练抓取检测器为当前观测生成大量候选抓取位姿。简单的最高分选择或随机选择难以兼顾抓取质量与空间可达性。HPS 综合抓取得分与空间邻近性，选择最优目标位姿。

**核心公式**：定义当前末端执行器位姿与候选抓取位姿之间的加权 SE(3) 测地距离：

$$d_{\mathcal{G}_j, W} = \sqrt{\xi^{\top} W \xi}$$

其中 $\xi$ 为 SE(3) 空间中的对数映射，$W$ 为权重矩阵，用于平衡平移与旋转分量。HPS 综合该距离与检测器输出的抓取得分，选择综合最优的候选位姿（详见推理预处理流程 Figure 3）。

![[assets/figures/papers/paper_list_l2514_https_arxiv_org_abs_2602_22862/figures/003_Figure_3.jpg]]
*Figure 3: Inference Pre-process presents our inference pipeline with Heuristic Pose Selector*

### 推理流程整合

推理时（Figure 3），HPS 首先从当前观测中筛选最优抓取位姿 $\mathcal{G}$；随后，扩散模型在潜在空间中从随机噪声出发，以可抓性视觉提示为条件逐步去噪，生成动作潜在表示 $Z$；最后，VAE 解码器将 $Z \oplus \mathcal{G}$ 解码为最终的动作块 $\hat{A}$。整个流程仅比同配置的 Diffusion Policy 增加约 15% 的推理延迟（Figure 4），保留了实用的实时性。

## 实验与关键发现

### 仿真基准评估

GraspLDP 在 LIBERO 仿真环境的四项评估维度上均显著超越主流模仿学习基线。Table 1 汇总了域内（In Domain）、空间泛化（Spatial Generalization）、对象泛化（Object Generalization）和视觉泛化（Visual Generalization）的成功率对比。

![[assets/figures/papers/paper_list_l2514_https_arxiv_org_abs_2602_22862/figures/004_Table_1.jpg]]
*Table 1: Results of evaluation in simulator. In Domain denotes cases where both the objects and their poses were present in the training data; Spatial Generalization measures how well the model handles those training objects placed in unseen poses; Object Generalization assesses performance on entirely novel objects; and Visual Generalization tests robustness under visual disturbances like lighting changes. The † refers to the model that has been fine-tuned on our dataset for fair comparison*

**域内性能**：GraspLDP 成功率达 80.3%，较 **Diffusion Policy**（Chi et al., RSS 2023）的 62.8% 提升 17.5 个百分点，较经微调的 **OpenVLA**（Kim et al., arXiv 2024）的 57.5% 提升 22.8 个百分点。这表明注入抓取先验对已知场景的动作生成质量有实质性改善。

**泛化能力**：在更具挑战性的泛化场景中，GraspLDP 的优势进一步扩大：
- 空间泛化：71.1% vs. Diffusion Policy 的 48.9%（+22.2 点）
- 对象泛化：58.2% vs. 11.4%（+46.8 点）
- 视觉泛化：64.6% vs. 16.3%（+48.3 点）

对象泛化中，不可见物体同时对策略和预训练抓取检测器不可见，GraspLDP 仍能保持近六成成功率，说明几何驱动的可抓性视觉提示（graspness cue）提供了跨物体类别的鲁棒先验。视觉泛化场景包含光照变化等干扰，GraspLDP 的优势验证了自监督重建目标对视觉条件稳定性的增强作用。

**推理延迟**：Figure 4 对比了三类方法的推理延迟。GraspLDP 在 RTX 4090 上每次推理仅比相同配置的 Diffusion Policy 慢约 15%，额外耗时主要来自可抓性推断（36 ms）和潜在解码（<1 ms）。经 torch.compile() 加速的 **GraspVLA**（Hu et al., arXiv 2025）延迟显著更高。GraspLDP 在保持实用实时性的前提下实现了大幅性能提升。

### 组件消融分析

Table 2 系统拆解了 GraspLDP 两大核心组件的独立贡献。

![[assets/figures/papers/paper_list_l2514_https_arxiv_org_abs_2602_22862/figures/005_Table_2.jpg]]
*Table 2: Results of ablation study. ID, SG, OG, and VG denote In Domain, Spatial, Object and Visual Generalization, respectively. GC and LG denotes Graspness Cue and Latent Guidance. CG denotes Condition Guidance used in Ours Baseline*

**可抓性视觉提示（Graspness Cue, GC）**：移除 GC 后，域内成功率下降 2.9 点（80.3% → 77.4%），视觉泛化下降最为明显（64.6% → 59.1%，-5.5 点）。这证实几何驱动的 graspness map 叠加自监督重建目标，有效强化了策略对抓取可行区域的关注，尤其在视觉干扰下作用突出。

**潜在空间引导（Latent Guidance, LG）**：将 LG 替换为条件引导（Condition Guidance, CG，即将抓取位姿直接拼接至观测作为条件输入），域内成功率骤降 6.8 点（80.3% → 73.5%），对象泛化下降 5.5 点（58.2% → 52.7%）。这一对比揭示：在动作潜在空间中施加抓取位姿引导，比在原始观测空间拼接条件，能更有效地将抓取先验融入动作生成过程。潜在空间引导使去噪过程直接受抓取配置约束，而非依赖模型自行从条件中解耦抓取信息。

**启发式位姿选择器（HPS）**：Table 3 对比了四种推理时的抓取位姿选择策略。HPS 综合抓取得分与 SE(3) 测地距离，在所有评估维度上均优于随机选择（Random）、最高分选择（Highest Score）和最近距离选择（Nearest）。以域内为例，HPS 的 80.3% 比随机选择的 66.8% 高出 13.5 点，比最高分选择的 72.0% 高出 8.3 点。这说明仅依赖抓取检测器得分或空间距离均不足以保证最优位姿选择，两者的联合考量对动作生成的准确性至关重要。

### 真实世界验证

真实世界实验使用日常物体，由于无法完全复现物体位姿，将域内与空间泛化合并为 ID&SG 评测集（Table 4）。

![[assets/figures/papers/paper_list_l2514_https_arxiv_org_abs_2602_22862/figures/010_Table_4.jpg]]
*Table 4: Results of real world evaluation. Because it’s difficult to ensure identical object poses in the real world, we merge the ID and SG splits into a single evaluation set*

GraspLDP 在三项真实世界评测中均大幅领先基线：
- ID&SG：84.0% vs. Diffusion Policy 的 44.0%（+40.0 点）
- 对象泛化（OG）：75.0% vs. 25.0%（+50.0 点）
- 视觉泛化（VG）：77.0% vs. 42.0%（+35.0 点）
- 平均成功率：78.7% vs. 37.0%（+41.7 点）

Figure 5 的定性分析展示了仿真与真实世界的抓取轨迹对比。在“mug”、“mustard bottle”、“thera med”等物体上，GraspLDP 生成的末端执行器轨迹紧密贴合目标抓取位姿，而 Diffusion Policy 的轨迹常偏离可行抓取区域。真实世界视觉泛化实验中，使用彩色 LED 灯带在低光照条件下模拟视觉干扰，GraspLDP 仍能保持 77.0% 的成功率。

![[assets/figures/papers/paper_list_l2514_https_arxiv_org_abs_2602_22862/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative experimental analysis. (a) Grasping trials using objects ”mug”, ”mustard bottle”, and ”thera med” in simulator. (b) Real world grasping trials corresponding to in domain, object generation, and visual generation performance. In particular, we use colored LED strips in low-light conditions to simulate visual interference*

**杂乱场景清空任务**：Table 5 汇报了真实世界杂乱场景的 Scene Completion Rate（SCR）。GraspLDP 在四个递增难度的场景中平均 SCR 达 72.5%，较 Diffusion Policy 的 35.0% 翻倍。Figure 10 展示了各场景的初始物体摆放。需注意，高度堆叠情形下抓取候选选择仍难完全避免碰撞和误选，这是当前方法的已知局限。

**动态抓取**：Table 6 评估了移动物体的抓取能力。GraspLDP 在慢速和快速运动条件下分别达到 72.0% 和 56.0% 的成功率，而 Diffusion Policy 仅为 36.0% 和 20.0%。当前实验的运动模式相对简单，未涉及高速、不规则运动，该场景下的性能边界仍需进一步探索。

### 鲁棒性与数据效率

**少样本学习**：Table 7 展示了不同演示数量下的域内性能。GraspLDP 在仅 25 条演示时即达到 66.2% 成功率，而 Diffusion Policy 为 50.8%。随演示数量增加，GraspLDP 的优势持续保持，表明抓取先验有效补偿了数据稀缺。

**抓取检测器替换**：Table 8 验证了方法对不同预训练抓取检测器的兼容性。替换检测器后，GraspLDP 的性能虽有小幅波动，但仍显著优于 Diffusion Policy，说明框架对检测器选择具有一定鲁棒性。但需注意，若检测器在未见物体类别上表现不佳，引导质量会下降，这是方法的依赖瓶颈。

### 失败模式与局限

综合实验结果和论文自述的局限性，GraspLDP 的主要失败模式包括：
1. **可变形/脆弱物体未验证**：当前仅在刚体物体上测试，对鸡蛋、烧杯等易碎或超薄物体的抓取性能未知。
2. **动态场景边界**：动态抓取实验中物体运动模式简单，高速不规则运动下的可靠性待验证。
3. **检测器依赖**：引导质量受限于预训练抓取检测器的泛化能力，在检测器失败的物体类别上性能退化。
4. **杂乱场景碰撞**：高度堆叠场景中，HPS 选择的抓取候选仍可能发生碰撞或误选。
5. **极端低时延场景**：推理延迟虽低，但在高频动态抓取等极端时延要求下未进一步优化。

## 定位与知识库关联

### 与主流模仿学习基线的继承与差异

**Diffusion Policy**（Chi et al., RSS 2023）是 GraspLDP 最直接的技术起点。Diffusion Policy 通过在高维观测空间直接对动作块执行去噪，展现了扩散模型在机器人操作中的潜力，但其动作生成过程完全依赖行为克隆，缺乏对抓取先验的显式编码。GraspLDP 在三个关键层面进行了改造：（1）将动作块从原始空间压缩至紧凑的 VAE 潜在空间，使扩散过程在更低维度、更具语义的动作潜在表示中进行；（2）在潜在空间解码阶段注入抓取位姿引导信号，使生成的动作轨迹天然偏向可行抓取配置；（3）在视觉条件中叠加几何驱动的可抓性视觉提示（Graspness Cue），替代单纯的腕部 RGB 图像。这三个改造槽位（动作表征、视觉条件、推理位姿选择）构成了 GraspLDP 相对于 Diffusion Policy 的核心增量。

**OpenVLA**（Kim et al., arXiv 2024）和 **GraspVLA**（Hu et al., arXiv 2025）代表了另一条技术路径——基于大规模预训练的视觉-语言-动作（VLA）模型。这类方法通过海量数据预训练获得强大的泛化能力，但其抓取行为主要依赖数据驱动，缺乏对抓取几何与可抓性先验的结构化利用。GraspLDP 与 VLA 路线的本质区别在于：GraspLDP 不依赖语言指令或大规模预训练，而是通过一个轻量的预训练抓取检测器提取几何先验，并将其融入扩散策略的潜在空间。这种设计使得 GraspLDP 在数据效率上具有优势——少样本域内评测（Table 7）表明，在仅使用少量演示的情况下，GraspLDP 仍能保持较高的成功率，而 VLA 类方法通常需要大量微调数据才能达到可比性能。

**Ours Baseline (Condition Guidance)** 是 GraspLDP 内部设计的消融基线，将抓取位姿直接作为条件输入拼接至观测。该基线在域内成功率上比完整的 GraspLDP 低 6.8 个百分点（Table 2），揭示了“在何处注入抓取先验”这一设计选择的关键性：将抓取位姿作为扩散条件直接输入，不如在潜在空间解码阶段进行引导来得有效。这一发现为后续工作提供了明确的架构设计指导——抓取先验的注入位置（潜在空间引导 vs. 条件输入）对性能有显著影响。

### 适用边界与约束条件

GraspLDP 的适用边界由以下约束条件共同定义：

**物体类型约束**：当前仅在刚体物体上验证，尚未评估对可变形物体（如布料、软包装）、易碎物体（如鸡蛋、烧杯）或超薄物体（如卡片、刀片）的抓取性能。预训练抓取检测器（如 AnyGrasp）在这些类别上的检测质量直接影响 GraspLDP 的引导效果。

**运动模式约束**：动态抓取实验中对象运动模式相对简单（Table 6），未涉及高速、不规则运动。在极端高频动态场景下，推理延迟虽仅比 Diffusion Policy 增加约 15%（Figure 4），但未经进一步优化，可能成为瓶颈。

**场景复杂度约束**：在杂乱场景清空任务中（Table 5），GraspLDP 虽优于基线，但抓取候选选择仍难以完全避免碰撞和误选，尤其在高度堆叠情形下。启发式位姿选择器（HPS）在 Table 3 中全面优于随机选择、最高分选择和最近距离选择，但其本质仍是启发式策略，缺乏对场景全局约束的显式推理。

**检测器依赖性**：方法的核心先验来源于预训练抓取检测器。若检测器在未见物体类别上表现不佳（例如 Object Generalization 场景中，检测器同样未见过这些物体），引导质量会下降。Table 8 展示了不同抓取检测器下的性能差异，证实了这一依赖性。

### 局限与开放问题

**结构化局限**：

1. **物体泛化边界不明确**：Object Generalization 场景中，抓取检测器和策略同时面对不可见物体。Table 1 显示 GraspLDP 在该场景下成功率为 58.2%，虽远超 Diffusion Policy 的 11.4%，但绝对数值仍表明存在显著提升空间。当检测器对不可见物体的抓取位姿预测失准时，潜在引导可能引入偏差而非增益。

2. **视觉提示机制的语义局限性**：Graspness Cue 本质是几何驱动的可抓性热力图，缺乏对物体语义属性（如“可挤压”、“易碎”）的建模。在需要区分抓取策略的精细操作场景中，纯几何提示可能不足。

3. **两阶段训练的解耦代价**：Action Latent Learning 和 Diffusion on Latent Action Space 分阶段训练，虽然简化了优化，但也可能导致潜在空间与扩散过程之间的次优耦合。Table 2 中移除 Latent Guidance 后性能下降 6.8 点，暗示当前设计对引导机制的依赖程度较高。

**开放研究问题**：

- **可变形与脆弱物体的抓取泛化**：能否将触觉、力/力矩信号融入潜在引导框架，使策略能够根据物体材质调整抓取力度和接近策略？这需要扩展 VAE 的动作表征空间以包含力控维度。

- **与 VLA 模型的融合路径**：GraspLDP 的潜在引导机制是否可以作为 VLA 模型的动作精炼模块？若能实现指令驱动的抓取（如“抓住杯子把手”），将大幅扩展方法的语义抓取能力。

- **杂乱场景的全局推理**：当前 HPS 基于单帧抓取候选进行选择，缺乏对场景中多物体关系的全局推理。引入图神经网络或关系推理模块，对抓取候选进行联合优化，可能进一步降低碰撞风险。

- **检测器鲁棒性的解耦**：能否通过多检测器集成或检测器置信度校准，降低对单一预训练检测器的依赖？Table 8 已初步探索了不同检测器的影响，但更系统的检测器鲁棒性研究仍是空白。

- **极端动态场景的实时性保障**：在需要毫秒级响应的动态抓取任务中，能否通过模型蒸馏或专用推理优化将延迟压缩至 50ms 以内？当前约 15% 的额外延迟在多数场景下可接受，但尚未触及实时控制的极限要求。

## 原文 PDF

![[paperPDFs/CVPR_2026/GraspLDP_Towards_Generalizable_Grasping_Policy_via_Latent_Diffusion.pdf]]
