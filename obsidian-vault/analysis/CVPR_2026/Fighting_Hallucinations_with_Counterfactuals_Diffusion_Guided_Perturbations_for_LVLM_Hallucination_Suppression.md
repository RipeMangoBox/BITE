---
title: "Fighting Hallucinations with Counterfactuals: Diffusion-Guided Perturbations for LVLM Hallucination Suppression"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Fighting_Hallucinations_with_Counterfactuals_Diffusion_Guided_Perturbations_for_LVLM_Hallucination_Suppression.pdf
project_link: "https://hamidreza-dastmalchi.github.io/cipher-cvpr2026/"
code_link: null
aliases:
- CCIPHER
- FHCDGPLHS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过扩散模型生成反事实图像（语义错误的视觉扰动），提取LVLM特征空间中的视觉幻觉方向子空间。
primary_logic: 视觉幻觉在LVLM隐藏表示中呈现低秩结构；通过对比真实与反事实图像-描述对的表示差异，用SVD估计该子空间，并在推理时投影消除幻觉成分，即可无需重训练地有效抑制视觉幻觉。
claims:
- CIPHER在CHAIR基准上显著降低了幻觉率，在LLaVA-1.5上CHAIR_S降至13.05%，比最佳基线Nullu低2.15个百分点，比贪婪解码低7.35个百分点。
- 在OPOPE基准上，CIPHER在所有三个评估指标（Accuracy, Precision, F1）上均取得最高分，同时保持输出质量。
- 消融实验证实，仅使用图像扰动（视觉反事实）比文本扰动或两者结合产生更低的幻觉率。
- CIPHER的推理吞吐量与标准贪婪解码相当（0.70 items/s），且幻觉抑制效果更好。
---

# Fighting Hallucinations with Counterfactuals: Diffusion-Guided Perturbations for LVLM Hallucination Suppression

> [!tip] 核心洞察
> 视觉幻觉在LVLM隐藏表示中呈现低秩结构；通过对比真实与反事实图像-描述对的表示差异，用SVD估计该子空间，并在推理时投影消除幻觉成分，即可无需重训练地有效抑制视觉幻觉。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用反事实对抗幻觉：用于LVLM幻觉抑制的扩散引导扰动 |
| 英文题名 | Fighting Hallucinations with Counterfactuals: Diffusion-Guided Perturbations for LVLM Hallucination Suppression |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.10470) · [Project](https://hamidreza-dastmalchi.github.io/cipher-cvpr2026/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CIPHER (Counterfactual Image Perturbations for Hallucination Extraction and Removal) |
| Dataset | CHAIR, OPOPE, LLaVA-Bench, Efficiency |

> [!tip] 效果简介
> - CHAIR (LLaVA-1.5) 上，CHAIR_S ↓ 13.05% vs 20.40% (Greedy) (-7.35%)。
> - OPOPE (LLaVA-1.5) 上，Accuracy ↑ 80.05 vs 79.14 (Greedy) (+0.91)。
> - LLaVA-Bench (LLaVA-1.5) 上，Accuracy (GPT-4V) ↑ 7.08 vs 6.79 (Original) (+0.29)。

## 概述

大型视觉语言模型（LVLM）在图像描述和视觉问答中展现出强大的能力，但普遍存在**幻觉**问题——生成与图像内容不符的描述。现有幻觉抑制方法主要针对语言模态引起的幻觉，而忽略了**视觉模态**本身触发的幻觉信号。这一瓶颈导致视觉幻觉未被针对性消除，限制了抑制效果的上限。

本文提出 **CIPHER**（Counterfactual Image Perturbations for Hallucination Extraction and Removal），核心洞察是：视觉幻觉在LVLM的隐藏表示中呈现**低秩结构**。通过对比真实图像-描述对与反事实（语义错误）图像-描述对的特征差异，可以用SVD估计出幻觉方向子空间，并在推理时通过投影消除这些成分——整个过程**无需重训练**。

方法分为两个阶段：离线阶段利用GPT-3.5和Stable Diffusion构建反事实数据集OHC-25K，提取幻觉子空间基底；推理阶段在每个解码步前将隐藏状态投影到该子空间的正交补上，抑制幻觉成分。

实验表明，CIPHER在CHAIR基准上将LLaVA-1.5的CHAIR_S降至13.05%，比最佳基线Nullu低2.15个百分点，比贪婪解码低7.35个百分点；在OPOPE基准上三项指标均取得最高分；同时推理吞吐量与标准贪婪解码持平（0.70 items/s），无额外时间开销。消融实验证实，仅使用视觉反事实扰动比文本扰动或两者混合产生更低的幻觉率，验证了视觉幻觉源的关键作用。

## 背景与动机

### 大视觉语言模型的幻觉困境

大视觉语言模型（LVLM）在图像描述、视觉问答等多模态任务中展现出强大的能力，但始终面临一个核心挑战：**幻觉（hallucination）**——模型生成的文本内容与输入图像的事实信息不一致，凭空捏造不存在的物体、属性或关系。这种幻觉严重削弱了LVLM在医疗、自动驾驶等安全关键场景中的可信度。

### 现有方法的视觉盲区

当前主流的幻觉缓解策略存在一个显著的**视觉模态缺口**。解码干预方法如**DoLa**（ICLR 2024）、**OPERA**（CVPR 2024）和**VCD**（CVPR 2024）主要通过调整语言解码路径来抑制幻觉，本质上是对语言生成过程的修正；后处理方法如**Woodpecker**（SCIS 2024）和**LURE**（ICLR 2024）则在生成完成后进行纠错。这些方法的共同特点是**关注语言引起的幻觉，而忽略了视觉模态本身触发的幻觉**——即图像中的某些视觉模式会系统性地诱导模型产生错误描述。

线性探测实验（Figure 6）为这一判断提供了直接证据：基于文本扰动（如替换描述中的物体词）产生的特征差异在不同Transformer层之间表现出中等且不稳定的可分离性，而基于扩散模型的视觉扰动则产生了一致的高准确率、高召回率和高F1分数。这表明**视觉幻觉在LVLM隐藏表示中具有稳定且可被线性分类的特征结构**，但现有方法未能针对性地利用这一特性。

### 核心动机：从反事实中学习幻觉方向

本文的核心动机源自一个关键洞察：要抑制视觉幻觉，需要先理解视觉幻觉在特征空间中的“形状”。如果能够构造**反事实图像**——即同一场景下语义被故意扭曲的视觉输入——并通过对比真实与反事实图像-描述对在LVLM中的隐藏表示差异，就可以估计出**视觉幻觉方向子空间**。在推理时，只需将隐藏状态投影到该子空间的正交补上，即可无训练、零额外推理开销地消除幻觉成分。

这一思路的技术瓶颈在于：如何生成高质量的视觉反事实数据？如何从高维特征差异中提取紧凑且有效的幻觉子空间？如何确保投影操作不损害模型的正常描述能力？论文提出的**CIPHER**方法正是围绕这三个问题展开。

## 核心创新

CIPHER的核心创新在于**首次将幻觉抑制的注意力从语言模态转向视觉模态**，并建立了一套完整的“反事实视觉扰动→子空间估计→推理时投影”的免训练干预范式。

### 创新动机：视觉幻觉的忽视

现有LVLM幻觉抑制方法——无论是测试时解码干预（如**DoLa**、**OPERA**、**VCD**）还是特征级干预（如**Nullu**）——主要关注语言引起的幻觉，即模型在生成文本时偏离视觉输入而产生的虚假描述。然而，这些方法忽略了视觉模态本身可能引发的幻觉：当图像中的视觉线索模糊、歧义或与模型训练分布不一致时，LVLM的视觉编码器可能产生误导性表示，进而诱发下游的语言幻觉。CIPHER正是针对这一被忽视的视觉幻觉源进行系统性干预。

### 关键发现：视觉幻觉的低秩结构

CIPHER的核心洞察在于：**视觉幻觉在LVLM的隐藏表示空间中呈现低秩结构**。通过构建反事实图像-描述对（正确图像+错误描述），提取LVLM各层的隐藏状态差异向量 $\delta = \tilde{h} - h$，并对这些差异向量进行奇异值分解（SVD），作者发现仅需保留前 $r$ 个右奇异向量即可有效捕获视觉幻觉的主要方向。在LLaVA-1.5上，$r=8$ 即达到最佳幻觉抑制效果，这证实了视觉幻觉方向的高度集中性。

### 方法创新：三个核心changed slots

相较于标准贪婪解码基线，CIPHER引入了两个关键的方法变更：

**1. 幻觉子空间估计（新增模块）**

基线方法在推理时不具备任何幻觉方向的知识。CIPHER在离线阶段构建了OHC-25K反事实数据集：利用GPT-3.5对真实图像描述进行语义扰动生成错误描述 $\tilde{C}$，再通过稳定扩散模型（Stable Diffusion）对原始图像进行部分正向扩散（$t_h$ 步）和以 $\tilde{C}$ 为条件的反向扩散，生成视觉上合理但语义错误的“反事实图像” $\tilde{I}$。LVLM编码 $(\tilde{I}, C)$ 和 $(I, C)$ 后，提取各层的隐藏状态差异向量，堆叠后进行SVD分解：

$$\Delta_{\ell} = U_{\ell} \Sigma_{\ell} V_{\ell}^{\top}$$

取前 $r$ 个右奇异向量构成幻觉基底 $\{v_{\ell,j}\}_{j=1}^{r}$。这一过程的创新在于：通过扩散模型对图像的**受控视觉扰动**生成反事实样本，而非仅依赖文本层面的修改，从而直接捕捉视觉模态触发的幻觉方向。

**2. 推理时投影抑制（推理时特征干预）**

基线方法在每个解码步骤直接使用原始隐藏状态。CIPHER在每个解码步骤前，将选定层的隐藏状态投影到幻觉子空间的正交补上：

$$h_{\ell,k}^{\mathrm{clean}} = h_{\ell,k}^{\mathrm{test}} - \sum_{j=1}^{r} \langle h_{\ell,k}^{\mathrm{test}}, v_{\ell,j} \rangle v_{\ell,j}$$

等价于通过投影矩阵 $P_{\ell} = I - V_{\ell,r} V_{\ell,r}^{\top}$ 消除幻觉成分。该操作无需任何模型参数更新，完全在推理时执行，且计算开销极低——实验表明CIPHER的推理吞吐量（0.70 items/s）与标准贪婪解码完全一致。

### 创新验证：视觉扰动优于文本扰动

消融实验（Table 5）直接验证了视觉反事实扰动的必要性：仅使用图像扰动（视觉反事实）产生的幻觉率显著低于仅使用文本扰动或两者混合的方案。层线性探测实验（Figure 6）进一步揭示，文本扰动在各层的可分性中等且不稳定，而基于扩散的视觉扰动在各层均产生一致的高准确率、高召回率和高F1值。这从机制层面证实了视觉模态在幻觉形成中的独立作用，以及CIPHER针对视觉源进行干预的合理性。

### 与现有方法的本质区别

| 维度 | 现有方法（DoLa/OPERA/VCD/Nullu） | CIPHER |
|------|------|--------|
| 幻觉源假设 | 语言解码偏差 | 视觉编码偏差 |
| 干预方式 | 对比解码/logit调整/特征归零 | 子空间投影 |
| 是否需要反事实数据 | 否（Nullu除外，但仅用文本扰动） | 是（视觉反事实图像） |
| 训练需求 | 无 | 无（离线构建仅需推理） |
| 推理开销 | 部分方法增加显著开销 | 与贪婪解码持平 |

CIPHER的独特之处在于：它不修改解码策略，不依赖辅助模型进行对比，也不简单地归零某些特征维度，而是通过**几何投影**的方式精确移除隐藏空间中的幻觉方向分量，在保持语义完整性的同时实现幻觉抑制。这种“估计-投影”的范式为LVLM幻觉抑制开辟了新的技术路径。

## 整体框架

CIPHER 的整体设计围绕一个核心洞察展开：视觉幻觉在 LVLM 的隐藏表示空间中呈现低秩结构，可以通过对比真实与反事实图像-描述对的表示差异来估计，并在推理时通过投影消除。该方法分为**离线阶段**和**推理阶段**两个互补的模块，如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/002_Figure_2.jpg]]
*Figure 2: (a) Hallucinated image generation: given an image*

### 离线阶段：反事实数据集构建与幻觉子空间估计

离线阶段完成两项关键任务：构建反事实图像-描述数据集，以及从该数据集中提取幻觉方向子空间。

**反事实图像生成（Figure 2a）**：给定 MSCOCO 中的真实图像-描述对 $(I_i, C_i)$，首先使用 GPT-3.5 对描述进行语义扰动，生成包含错误对象或属性的幻觉描述 $\tilde{C}_i$。随后，通过 Stable Diffusion 的 VAE 编码器 $\mathcal{E}$ 将图像 $I_i$ 编码为潜在变量 $z_0 = \mathcal{E}(I_i)$，并对其进行 $t_h$ 步正向扩散加噪：

$$\tilde{z}_{t_h} = \sqrt{\bar{\alpha}_{t_h}} z_0 + \sqrt{1 - \bar{\alpha}_{t_h}} \epsilon, \qquad \epsilon \sim \mathcal{N}(0, I)$$

以幻觉描述 $\tilde{C}_i$ 为条件，对加噪后的潜在变量执行反向扩散过程，生成多张反事实图像 $\tilde{I}_{i,j}$。这些图像在保持场景布局的同时，引入了与错误描述一致的视觉幻觉线索。最终构建的数据集 OHC-25K 包含 25,000 个反事实样本。

**幻觉子空间估计（Figure 2b）**：将真实图像-描述对 $(I_i, C_i)$ 和反事实图像-描述对 $(\tilde{I}_{i,j}, C_i)$ 分别输入目标 LVLM，在指定层 $\ell$ 提取隐藏状态 $h_\ell^{(i)}$ 和 $\tilde{h}_\ell^{(i)}$。计算差异向量 $\delta_\ell^{(i)} = \tilde{h}_\ell^{(i)} - h_\ell^{(i)}$，该向量捕获了由视觉扰动触发的表示偏移。将所有样本的差异向量堆叠为矩阵 $\Delta_\ell$，进行奇异值分解：

$$\Delta_{\ell} = U_{\ell} \Sigma_{\ell} V_{\ell}^{\top}$$

选取前 $r$ 个右奇异向量构成幻觉子空间的基底 $V_{\ell, r} = \{v_{\ell,1}, \dots, v_{\ell,r}\}$，存入幻觉基底库。这一过程逐层独立进行，最终得到覆盖多个 Transformer 层的幻觉方向集合。

### 推理阶段：投影抑制

在推理时（Figure 3），对于给定的测试输入（图像与指令），LVLM 逐 token 自回归生成文本。在每一个解码步骤 $k$，从选定层的隐藏状态 $h_{\ell,k}^{\mathrm{test}}$ 中减去其在幻觉基底上的投影：

$$h_{\ell,k}^{\mathrm{clean}} = h_{\ell,k}^{\mathrm{test}} - \sum_{j=1}^{r} \langle h_{\ell,k}^{\mathrm{test}}, v_{\ell,j} \rangle v_{\ell,j}$$

等价地，可通过投影矩阵 $P_{\ell} = I - V_{\ell,r} V_{\ell,r}^{\top}$ 一次性完成正交投影。经过净化的隐藏状态替代原始状态继续前向传播，从而在保持核心语义的前提下抑制幻觉成分。

### 模块关系与数据流

三个模块形成清晰的串行数据流：**反事实图像生成**为**幻觉子空间估计**提供训练数据，**幻觉子空间估计**为**推理时投影抑制**提供预计算的幻觉基底。离线阶段的计算开销集中在数据集构建和 SVD 分解上，推理阶段仅增加了隐藏状态的投影操作，因此吞吐量与标准贪婪解码持平（0.70 items/s，Table 4）。整个流程无需对 LVLM 进行任何微调或重训练，是一种即插即用的测试时干预方法。

### 补充图表

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/021_Figure_13.jpg]]
*Figure 13: An illustration of the prompt used to guide GPT-4V for visual question evaluation*

## 核心模块与公式推导

CIPHER 的核心由三个模块级联构成：反事实图像生成、幻觉子空间估计、推理时投影抑制。下面按流程展开各模块的关键机制与公式。

### 1. 反事实图像生成

该模块的目标是构造视觉幻觉图像——即语义上与真实描述不一致但视觉上保持合理性的图像变体。具体流程为：

1. **文本扰动**：对每张图像的真实描述 $C_i$，使用 GPT-3.5 生成语义错误的幻觉描述 $\tilde{C}_i$。
2. **图像潜在编码**：通过 Stable Diffusion 的 VAE 编码器 $\mathcal{E}$ 将原始图像 $I_i$ 编码为潜在变量：

   $$z_0 = \mathcal{E}(I_i)$$

3. **部分正向扩散**：对潜在变量施加 $t_h$ 步正向扩散，得到含噪潜在变量：

   $$\tilde{z}_{t_h} = \sqrt{\bar{\alpha}_{t_h}} z_0 + \sqrt{1 - \bar{\alpha}_{t_h}} \epsilon, \qquad \epsilon \sim \mathcal{N}(0, I)$$

   其中 $\bar{\alpha}_{t_h}$ 为扩散调度参数，$t_h$ 控制扰动强度。这一步在保留图像结构的同时引入足够的随机性，为后续条件生成提供起点。

4. **条件反向扩散**：以幻觉描述 $\tilde{C}_i$ 为条件，对 $\tilde{z}_{t_h}$ 执行反向扩散，生成反事实图像 $\tilde{I}_i$。

这一设计的核心直觉是：通过扩散模型的部分加噪与条件去噪，在图像空间中引入与描述语义矛盾的视觉线索，从而激发 LVLM 的视觉幻觉。

### 2. 幻觉子空间估计

该模块从反事实图像-描述对中提取 LVLM 隐藏状态中的幻觉方向，并用 SVD 估计其低秩子空间。

1. **特征提取**：对每对真实图像-描述 $(I_i, C_i)$ 和反事实图像-描述 $(\tilde{I}_i, C_i)$（注意两者使用相同描述），分别通过目标 LVLM 前向传播，在第 $\ell$ 层提取隐藏状态 $h_\ell^{(i)}$ 和 $\tilde{h}_\ell^{(i)}$。

2. **差异向量计算**：定义幻觉方向为：

   $$\delta_\ell^{(i)} = \tilde{h}_\ell^{(i)} - h_\ell^{(i)}$$

   该差异向量捕捉了视觉扰动引起的隐藏表示偏移。

3. **SVD 分解**：将所有 $M$ 个样本的差异向量堆叠为矩阵 $\Delta_\ell$，进行奇异值分解：

   $$\Delta_{\ell} = U_{\ell} \Sigma_{\ell} V_{\ell}^{\top}$$

   选取前 $r$ 个右奇异向量 $v_{\ell,1}, \dots, v_{\ell,r}$ 作为幻觉子空间基底 $V_{\ell,r}$，存入幻觉基底库供推理时使用。

子空间秩 $r$ 是方法的关键超参数——消融实验表明 LLaVA-1.5 上 $r=8$ 最优（Figure 8），MiniGPT-4 上 $r=64$ 最优（Figure 11），mPLUG-Owl2 上 $r=32$ 最优（Figure 12）。这一差异反映了不同 LVLM 架构中幻觉成分的维度特性不同。

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/019_Figure_11.jpg]]
*Figure 11: Effect of subspace rank r on*

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/020_Figure_12.jpg]]
*Figure 12: Effect of subspace rank r on*

### 3. 推理时投影抑制

在推理阶段，CIPHER 对每个解码步骤的隐藏状态进行在线投影，消除幻觉成分。

给定测试输入的隐藏状态 $h_{\ell,k}^{\mathrm{test}}$（第 $\ell$ 层、第 $k$ 个解码步），清洁表示为：

$$h_{\ell,k}^{\mathrm{clean}} = h_{\ell,k}^{\mathrm{test}} - \sum_{j=1}^{r} \langle h_{\ell,k}^{\mathrm{test}}, v_{\ell,j} \rangle v_{\ell,j}$$

等价地，可表示为投影矩阵形式：

$$P_{\ell} = I - V_{\ell,r} V_{\ell,r}^{\top}$$

$$h_{\ell,k}^{\mathrm{clean}} = P_{\ell} \, h_{\ell,k}^{\mathrm{test}}$$

该操作将隐藏状态投影到幻觉子空间的正交补上，逐层、逐解码步执行，在移除幻觉方向的同时保留核心语义信息。投影层范围需针对不同模型手动设定——消融实验（Table 8）表明对 LLaVA-1.5 而言，在 16-32 层范围内投影效果最佳。

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/018_Table_8.jpg]]
*Table 8: Ablation study on the transformer layer range used for projection in VISTA*

**关键设计要点**：投影仅作用于选定层的隐藏状态，不修改模型参数，因此 CIPHER 无需任何微调，推理吞吐量与标准贪婪解码持平（0.70 items/s，Table 4），且幻觉抑制效果显著优于其他测试时干预方法。

### 补充图表

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/003_Figure_3.jpg]]
*Figure 3: Inference-time projection mechanism. Given an input image and instruction, the model generates text autoregressively. At each decoding step during generation, hidden states from selected layers are projected onto the subspace orthogonal to the corresponding hallucination space, using the hallucination basis bank obtained in the offline phase*

## 实验与分析

CIPHER在三个主流LVLM架构（LLaVA-1.5、MiniGPT-4、mPLUG-Owl2）上进行了全面评估，覆盖CHAIR、OPOPE、LLaVA-Bench和MMHal四个基准，并与贪婪解码、束搜索、DoLa、OPERA、VCD、HALC、Nullu、Woodpecker、LURE等方法进行了系统对比。

### 主实验结果

**CHAIR基准。** 表1展示了各方法在CHAIR基准上的幻觉率与流畅度。CIPHER在所有三个模型上均取得最低的CHAIR_S分数：LLaVA-1.5上降至13.05%，比贪婪解码低7.35个百分点，比最佳对比方法Nullu（CVPR 2025）低2.15个百分点；MiniGPT-4上降至18.48%，比贪婪解码低13.92个百分点；mPLUG-Owl2上降至13.60%，比贪婪解码低6.03个百分点。在CHAIR_I指标上，CIPHER在MiniGPT-4和mPLUG-Owl2上同样取得最低值（分别为8.33%和4.92%），在LLaVA-1.5上与最优方法持平。值得注意的是，CIPHER在降低幻觉的同时保持了较高的BLEU分数，表明其抑制机制未损害生成文本的流畅性。

**OPOPE基准。** 表2展示了各方法在OPOPE基准上的Accuracy、Precision和F1三项指标。CIPHER在所有三个模型的所有三项指标上均取得最高分：LLaVA-1.5上Accuracy达到80.05，Precision 93.72，F1 92.11；MiniGPT-4上Accuracy 72.25，Precision 96.50，F1 92.58；mPLUG-Owl2上Accuracy 77.87，Precision 92.93，F1 90.95。这一结果验证了CIPHER在区分存在和不存在对象的细粒度判别任务上的优越性。

**LLaVA-Bench。** 表3展示了GPT-4V评估结果。CIPHER在LLaVA-1.5上获得7.08的Accuracy分数，高于原始模型的6.79，同时答案详尽度也有所提升。这表明CIPHER不仅抑制了幻觉，还增强了模型的视觉基础能力。

**MMHal基准。** 图4的雷达图显示，CIPHER在八类幻觉（如对象存在、属性、关系、计数等）上均优于原始模型，尤其在对象存在和属性幻觉类别上提升显著。

**效率分析。** 表4对比了各方法的推理吞吐量。CIPHER在LLaVA-7B上的吞吐量为0.70 items/s，与标准贪婪解码完全一致，且CHAIR_S远低于其他方法。这是因为CIPHER的投影操作仅涉及向量内积和减法，计算开销极小，无需额外的前向传播或模型调用。

### 消融实验

**幻觉来源消融。** 表5对比了不同扰动来源对幻觉抑制效果的影响。仅使用图像反事实扰动（视觉幻觉源）时CHAIR_S最低，仅使用文本扰动时效果次之，两者混合反而导致效果下降。这一结果直接支持了论文的核心主张：视觉模态引起的幻觉是当前LVLM幻觉的重要来源，且需要针对性的视觉反事实干预。

**子空间秩消融。** 图8展示了LLaVA-1.5上子空间秩r对CHAIR和BLEU的影响。r=8时CHAIR_S和CHAIR_I均达到最低，同时BLEU最高。过小的r无法充分捕获幻觉方向，过大的r则会引入噪声并损害语义保真度。MiniGPT-4和mPLUG-Owl2的最佳秩分别为64和32（图11、图12），表明不同模型架构需要不同的子空间维度。

**投影层范围消融。** 表8显示，对LLaVA-1.5的16-32层进行投影可获得最佳效果。仅投影浅层或深层均不如中间层范围有效，这与视觉幻觉信息在LVLM中间层最为集中的假设一致。

**扩散步数消融。** 图7显示，使用t_h=0.5T扩散步数生成的子空间获得最佳CHAIR_S抑制效果。过小的步数无法产生足够的视觉扰动，过大的步数则可能破坏图像结构信息，导致子空间估计不准确。

**线性探测验证。** 图6通过逐层线性探测对比了文本扰动和视觉扰动产生的隐藏状态差异的可分性。扩散引导的视觉扰动在各层均产生一致且高准确率的可分性，而文本扰动的可分性则中等且不稳定。这为视觉反事实方法的有效性提供了机制层面的证据。

### 鲁棒性分析

图9展示了原始模型与CIPHER在不同高斯噪声水平下的CHAIR_S对比。随着噪声增强，原始模型的幻觉率急剧上升，而CIPHER的幻觉率保持相对稳定，表明投影抑制机制对输入扰动具有较好的鲁棒性。

### 局限性讨论

尽管CIPHER在多个基准上表现优异，仍存在以下局限：

1. **离线构建成本**：反事实数据集的构建依赖GPT-3.5和Stable Diffusion等外部模型，需要额外的计算资源和时间。对于资源受限的场景，这一离线阶段可能成为部署瓶颈。

2. **超参数手动调优**：子空间秩r和投影层范围需要针对不同LVLM架构手动选择，缺乏自动化的超参数选择机制。这限制了方法在新模型上的即插即用能力。

3. **模型与语言覆盖**：目前仅在三个英文LVLM上验证，尚未扩展到更多模型架构（如BLIP-2、InstructBLIP）和其他语言。方法的跨语言泛化性有待进一步研究。

4. **反事实质量依赖**：幻觉抑制效果受限于反事实图像的质量和多样性。如果生成的视觉扰动不能充分覆盖真实场景中的幻觉模式，子空间估计可能存在偏差。

### 开放问题

1. **动态投影机制**：当前方法对所有样本使用统一的全局子空间。如何实现样本自适应的动态投影，以更灵活地抑制上下文相关的幻觉？

2. **任务泛化性**：该方法能否推广到其他视觉-语言任务（如VQA、视觉推理、指代表达理解）并保持一致的幻觉抑制效果？

3. **自动化超参数选择**：如何设计子空间秩和投影层的自动选择策略，使方法在不同模型上实现即插即用？

4. **轻量化构建**：能否利用更轻量的图像编辑方式（如基于注意力机制的编辑）替代完整的扩散模型生成，以降低离线阶段的构建成本？

### 补充图表

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/004_Table_1.jpg]]
*Table 1: CHAIR and BLEU scores across LVLMs; lower CHAIR = less hallucination, higher BLEU = better fluency*

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/010_Table_4.jpg]]
*Table 4: Comparison of CHAIRS and throughput (items/s) for different mitigation methods, tested on LLaVA-7B with an NVIDIA A6000 GPU*

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/014_Table_5.jpg]]
*Table 5: Ablation study on the source of hallucination. ✓denotes hallucinated input and ✗ denotes ground-truth input*

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/013_Figure_8.jpg]]
*Figure 8: Ablation study on subspace rank (r)*

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/009_Figure_6.jpg]]
*Figure 6: Layer-wise linear probing performance comparing textual and diffusion-based visual hallucination perturbations. Textual perturbations exhibit moderate and unstable separability across layers, whereas diffusion-based visual perturbations produce consistently high accuracy, recall, and F1*

![[assets/figures/papers/paper_list_l870_https_arxiv_org_abs_2603_10470/figures/011_Figure_7.jpg]]
*Figure 7: CHAIRS of CIPHER using hallucination subspaces derived from images perturbed at different diffusion steps*

## 方法谱系与知识库定位

### 方法继承与对比定位

CIPHER 的核心技术路径属于**推理时特征干预**（inference-time feature intervention）这一研究分支，与现有的幻觉抑制方法形成清晰的方法论对照。

**与解码策略方法的对比。** 早期工作如 **DoLa** (Chuang et al., ICLR 2024)、**OPERA** (Huang et al., CVPR 2024)、**HALC** (Wang et al., ICML 2024) 等通过在解码过程中修改 logits 或注意力权重来抑制幻觉。这类方法操作在输出概率层面，本质上是对语言生成路径的修正，但并未直接触及视觉-语言对齐中的根本性问题——即视觉模态引入的虚假信号如何在隐藏表示中传播。CIPHER 的投影操作发生在中间隐藏状态层面，干预粒度更细，且直接针对视觉幻觉的特征方向，从因果链条的上游进行阻断。

**与对比解码方法的对比。** **VCD** (Leng et al., CVPR 2024) 通过对比原始图像和失真图像的条件输出来放大真实视觉信号，其思路与 CIPHER 有表面相似性——都利用了图像扰动。但关键区别在于：VCD 的扰动是随机的（如高斯噪声），旨在削弱视觉条件以暴露语言先验偏差；而 CIPHER 的扰动是**语义引导的反事实生成**，通过 GPT-3.5 修改描述后经扩散模型合成语义错误的图像，直接模拟视觉幻觉的触发模式。这一设计差异使得 CIPHER 提取的特征方向具有更强的因果针对性。

**与特征级方法的对比。** 最直接的可比工作是 **Nullu** (CVPR 2025)，它同样在隐藏状态层面进行干预。Nullu 通过计算真实和噪声图像在特征空间的差异来估计“噪声方向”并投影消除。CIPHER 在此基础上实现了两个关键跃迁：其一，将无结构的噪声扰动替换为语义驱动的反事实图像生成，使得提取的子空间更准确地对应幻觉而非一般噪声；其二，通过 SVD 估计低秩子空间而非单一方向向量，捕获了幻觉的多维结构。实验证据（Table 1）表明，CIPHER 在 LLaVA-1.5 上将 CHAIR_S 降至 13.05%，比 Nullu 的 15.20% 进一步降低了 2.15 个百分点，验证了这一方法论改进的有效性。

**与后处理方法的对比。** **Woodpecker** (Yin et al., SCIS 2024) 和 **LURE** (Zhou et al., ICLR 2024) 在生成完成后对输出进行修正，属于事后补救。这类方法无法防止幻觉在生成过程中逐步累积和传播，且引入了额外的推理开销。CIPHER 的在线投影机制在生成过程中实时净化表示，在效率上具有天然优势——其吞吐量（0.70 items/s）与标准贪婪解码完全持平（Table 4）。

### 知识库定位与适用边界

CIPHER 的方法论贡献在于揭示了 LVLM 中视觉幻觉的**低秩结构假说**：幻觉并非随机噪声，而是在隐藏空间中沿着特定方向集中分布。这一发现将幻觉抑制问题转化为子空间估计与投影的线性代数操作，使得无需重训练即可实现有效的幻觉消除。

**适用边界**由以下因素界定：

1. **模型架构依赖性。** 该方法假设 LVLM 的隐藏表示中存在可被 SVD 捕获的线性幻觉子空间。论文在三种不同架构（LLaVA-1.5、MiniGPT-4、mPLUG-Owl2）上验证了有效性，表明这一假设具有一定的跨架构泛化性。但对于采用完全不同融合机制（如 cross-attention 而非 concatenation）的模型，子空间结构可能存在差异，需要进一步验证。

2. **反事实数据质量约束。** 离线阶段的子空间估计质量高度依赖反事实图像的语义准确性。若 GPT-3.5 生成的错误描述与图像内容差异过大，或扩散模型未能忠实地将语义错误转化为视觉扰动，估计的子空间可能偏离真实的幻觉方向。论文使用 0.5T 扩散步数达到最佳效果（Figure 7），暗示存在一个扰动强度的“甜区”：过弱则不足以触发幻觉特征，过强则破坏图像整体结构。

3. **超参数敏感性。** 子空间秩 r 和投影层范围需要针对不同模型手动调优。LLaVA-1.5 的最优秩为 r=8（Figure 8），MiniGPT-4 为 r=64（Figure 11），mPLUG-Owl2 为 r=32（Figure 12），差异显著。投影层范围在 16-32 层时效果最佳（Table 8）。这种模型特异性意味着部署到新架构时需要额外的验证成本。

4. **语言与任务边界。** 当前验证仅限于英语图像描述任务（CHAIR、OPOPE、MMHal、LLaVA-Bench）。该方法能否泛化到视觉问答（VQA）、视觉推理等多轮交互场景，以及非英语语言，仍是开放问题。

### 局限与开放问题

**已知局限。**

- **离线构建成本。** 反事实数据集的构建依赖 GPT-3.5 和 Stable Diffusion，对每张图像执行部分扩散和反向去噪，计算开销不容忽视。虽然这是一次性的离线过程，但对于大规模部署场景，数据构建的扩展性可能成为瓶颈。
- **静态子空间假设。** 当前方法为所有样本使用统一的幻觉子空间，无法适应样本级别的上下文变化。某些幻觉可能仅在特定视觉-语义组合下触发，全局投影可能过度抑制或抑制不足。
- **子空间秩的手动选择。** 缺乏自动确定最优秩的机制，增加了方法的使用门槛。

**开放问题。**

1. **样本自适应投影。** 如何实现动态的、依赖输入内容的投影策略？例如，根据当前图像的视觉特征或解码过程中的不确定性估计，自适应地调整投影强度或选择激活的子空间维度，可能进一步提升抑制精度。

2. **跨任务泛化。** 该方法在图像描述任务上的成功是否可迁移至 VQA、视觉蕴含、指代表达理解等任务？这些任务中幻觉的表现形式可能不同（如错误的对象指代、虚假的关系推理），需要验证子空间方法是否仍能捕获相应的特征方向。

3. **自动化超参数选择。** 能否设计一种基于验证集性能或表示空间本征维度的自动选择策略，为任意 LVLM 确定最优的秩 r 和投影层范围？这将显著降低部署门槛。

4. **轻量化反事实生成。** 是否可以利用更高效的图像编辑方法（如基于指令的图像编辑模型、或直接在特征空间进行扰动）替代完整的扩散过程，从而降低离线阶段的构建成本？

5. **与训练时方法的互补性。** CIPHER 作为测试时方法，与 RLHF、偏好对齐等训练时幻觉抑制方法的关系如何？两者是否可叠加使用以获得进一步的幻觉降低？初步的互补性假设值得系统验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Fighting_Hallucinations_with_Counterfactuals_Diffusion_Guided_Perturbations_for_LVLM_Hallucination_Suppression.pdf]]
