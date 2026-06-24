---
title: "DualFlow: Unified Multi-Modal Interactive & Reactive 3D Motion Generation via Rectified Flow"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/DualFlow_Unified_Multi_Modal_Interactive_Reactive_3D_Motion_Generation_via_Rectified_Flow.pdf
aliases:
- DualFlow
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用统一的双分支架构，通过可切换掩码同时支持交互与反应生成；引入检索增强生成（RAG）模块，利用LLM分解的文本描述和音乐特征检索运动范例，注入多模态语义信息；使用对比整流流损失与加权同步损失，增强运动-条件对齐和人际协调性，并在仅20步直线采样中实现高效推理。
primary_logic: 将交互与反应式两人运动生成统一到整流流框架，结合LLM驱动的多层次检索和对比学习锐化运动表示，可在极少采样步数下生成高度同步且语义一致的协调运动。
claims:
- DualFlow在MDD交互任务上R-Precision@3达到0.513，FID仅为0.415，显著优于InterGen (R-Precision@3 0.302, FID 0.426)。
- DualFlow在MDD反应任务上FID为0.686，MMDist为1.056，远超DuoLando的0.698和2.113。
- DualFlow仅需20步整流流推理，速度是50步DDIM的2.5倍。
- MDD (Duet Task, 交互生成, text+music) 上 R-Precision@3 = 0.513 (DualFlow Both)
---

# DualFlow: Unified Multi-Modal Interactive & Reactive 3D Motion Generation via Rectified Flow

> [!tip] 核心洞察
> 将交互与反应式两人运动生成统一到整流流框架，结合LLM驱动的多层次检索和对比学习锐化运动表示，可在极少采样步数下生成高度同步且语义一致的协调运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | DualFlow：基于整流流的统一多模态交互与反应式3D运动生成 |
| 英文题名 | DualFlow: Unified Multi-Modal Interactive & Reactive 3D Motion Generation via Rectified Flow |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2509.24099) · [Project](https://gprerit96.github.io/dualflow-page) · [arXiv](https://arxiv.org/abs/2210.02747) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DualFlow |
| Dataset | MDD, InterHuman-AS |

> [!tip] 效果简介
> - MDD (Duet Task, 交互生成, text+music) 上，R-Precision@3 0.513 (DualFlow Both) vs 0.302 (InterGen Both) (+69.9%)；FID 0.415 vs 0.426 (InterGen Both) (-2.6%)。
> - MDD (Reactive Task, 反应生成, text+music) 上，R-Precision@3 0.471 (DualFlow Both) vs 0.219 (DuoLando Both) (+115%)；FID 0.686 vs 0.698 (DuoLando Both) (-1.7%)。
> - InterHuman-AS (Text Interactive) 上，R-Precision@1 0.437 vs 0.113 (InterGen) (+287%)。

## 概述

双人运动生成面临一个核心瓶颈：现有方法将**交互式生成**（两人同步合成）与**反应式生成**（一人响应另一人动作）视为两个独立任务，采用互不兼容的架构，且仅支持文本或音乐等单一模态条件。此外，主流的扩散模型依赖多步随机去噪，采样效率低、误差累积严重。

DualFlow 提出了一种**统一框架**来解决上述问题。其核心思路是将交互与反应式两人运动生成统一到**整流流（Rectified Flow）**框架下，结合 LLM 驱动的多层次检索和对比学习来锐化运动表示，从而在极少采样步数（仅 20 步直线传输）下生成高度同步且语义一致的协调运动。

在方法定位上，DualFlow 区别于三类基线：**MDM**（Tevet et al., 2022）作为扩散式单人运动生成模型，扩展后用于多人条件生成；**InterGen**（Liang et al., 2024）是专门的扩散式两人交互文本条件生成模型；**DuoLando** 则面向反应式两人运动生成，支持文本或音乐条件。DualFlow 的关键改进在于：
- 将生成框架从扩散模型升级为整流流，实现确定性直线传输，推理速度是 50 步 DDIM 的 2.5 倍；
- 通过统一双分支架构和可切换掩码机制，无缝支持交互与反应两种模式；
- 引入检索增强生成（RAG）模块，利用 LLM 将文本分解为空间关系、身体运动和节奏三个子描述，结合音乐特征检索运动范例并注入多模态语义；
- 采用对比整流流损失与加权同步损失，增强运动-条件对齐和人际协调性。

实验结果验证了上述设计的有效性：在 MDD 数据集的交互任务上，DualFlow 的 R-Precision@3 达到 0.513（InterGen 为 0.302），FID 为 0.415；在反应任务上，FID 为 0.686，MMDist 为 1.056（DuoLando 分别为 0.698 和 2.113）。在 InterHuman-AS 文本交互任务上，R-Precision@1 达到 0.437，远超 InterGen 的 0.113。消融实验进一步证实，RAG 模块、对比损失和同步损失对性能均有显著贡献。

## 背景与动机

**核心瓶颈：交互与反应式两人运动生成的分离与低效**

现有的两人互动运动生成方法存在三个根本性缺陷。首先，交互式生成（同时合成两人的协调运动）与反应式生成（基于一人运动生成另一人的响应）被视作两个独立任务，各自使用互不兼容的模型架构——交互式模型如 **InterGen**（Liang et al., 2024）基于扩散模型同时输出两人动作，而反应式模型如 **DuoLando** 则采用条件生成范式。这种分离导致无法在一个统一框架内灵活切换任务模式。其次，现有方法仅支持单一模态条件（纯文本或纯音乐），缺乏对多模态语义信息的有效融合。第三，也是最为关键的效率瓶颈，主流方法均基于扩散模型（DDPM/DDIM），需要数十甚至上百步的随机去噪迭代才能生成合理结果，推理速度慢且存在误差累积问题，严重制约了实际应用场景中的实时交互需求。

**因果突破口：统一整流流框架与多模态检索增强**

DualFlow 针对上述瓶颈提出了系统性的解决方案。在生成范式层面，该方法摒弃了扩散模型的随机采样路径，转而采用**整流流（Rectified Flow）**框架，将生成过程建模为确定性直线传输，仅需20步即可完成高质量推理，速度达到50步DDIM的2.5倍（见 Figure 4）。在架构统一性层面，DualFlow设计了**双分支Transformer架构**，通过可切换掩码机制实现交互与反应模式的无缝切换：交互模式下两个分支对称激活，通过运动交叉注意力协调两人动作；反应模式下演员分支被掩码，反应者分支通过带前瞻窗口的因果交叉注意力（Causal Cross-Attention with Look-Ahead）条件化于演员运动。在多模态语义注入层面，DualFlow首次在两人运动生成中引入**检索增强生成（RAG）模块**，利用LLM（GPT-4o）将文本描述分解为空间关系、身体运动和节奏三个子描述，结合音乐特征检索运动范例，并通过检索交叉注意力将范例中的语义信息注入生成过程。此外，**对比整流流损失**通过三元组约束拉近语义相似运动的速度场表示，而**加权同步损失**则结合距离权重和解剖关节权重显式优化人际空间协调性。

**核心洞察：语义锐化与高效采样的一体化**

DualFlow 的核心洞察在于：将交互与反应式两人运动生成统一到整流流框架，并利用LLM驱动的多层次检索和对比学习锐化运动表示的语义边界，可以在极少采样步数下生成高度同步且语义一致的协调运动。实验证据充分支撑了这一洞察——在MDD数据集的交互任务上，DualFlow的R-Precision@3达到0.513，显著优于InterGen的0.302（+69.9%），FID降至0.415；在反应任务上，FID为0.686，MMDist为1.056，远超DuoLando的0.698和2.113（Table 1）。在InterHuman-AS数据集上，文本条件下的R-Precision@1达到0.437，相较InterGen的0.113提升287%（Table 2）。消融实验进一步验证了各组件的因果贡献：完全移除RAG模块导致交互任务FID从0.415升至0.622（Table 7），去除三元组对比损失使FID恶化至0.783（Table 4），去除同步损失则使交互和反应任务的FID分别升至0.472和0.774（Table 8）。

## 核心创新

DualFlow 的核心创新在于将**交互式**与**反应式**两人运动生成统一至单一整流流框架，并通过三个关键机制突破现有方法的瓶颈。

### 1. 统一的双分支架构与任务切换

现有方法将交互式与反应式生成视为分离任务，使用独立模型处理，架构不兼容。**InterGen**（Liang et al., 2024）仅支持交互式文本条件生成，**DuoLando** 则专注于反应式生成，两者无法在同一框架下协同工作。

DualFlow 采用双分支 Transformer 架构，通过**可切换掩码机制**实现任务无缝切换：
- **交互模式**：两个分支同时激活，通过 Motion Cross-Attention 协调两人的运动生成。
- **反应模式**：演员（Actor）分支被掩码，仅反应者（Reactor）分支激活，并以 Causal Cross-Attention with Look-Ahead 替代 Motion Cross-Attention，使反应者能关注演员过去及未来 L 帧的运动，实现因果条件生成。

这一设计使得单一模型能同时处理两类任务，无需额外训练或架构修改。

### 2. 检索增强生成（RAG）模块

传统方法仅使用文本或音乐作为单一条件，语义信息有限。DualFlow 首次将检索增强生成引入两人运动生成，构建了多层次语义注入管道：

- **LLM 文本分解**：利用 GPT-4o 将文本描述分解为**空间关系**、**身体运动**和**节奏**三个子描述，细化语义粒度。
- **多模态检索**：基于分解后的文本（CLIP 嵌入）和音乐特征（Jukebox 嵌入），结合运动长度惩罚的余弦相似度评分 $$s_{i}^{q} = \langle f_{i}^{q}, f_{p}^{q} \rangle \cdot e^{-\lambda \cdot \frac{|l_{i} - l_{p}|}{\max\{l_{i}, l_{p}\}}}$$ 从数据库中检索运动范例。
- **语义注入**：检索到的运动范例通过 Retrieval Cross-Attention 注入生成过程，提供细粒度的运动先验。

消融实验表明，完全移除 RAG 模块导致交互任务 FID 从 0.415 升至 0.622，R-Precision 大幅下降，验证了检索增强对语义对齐的关键作用。

### 3. 对比整流流损失

扩散模型（如 DDPM/DDIM）需要多步随机去噪，采样效率低且误差累积严重。DualFlow 采用**整流流（Rectified Flow）**框架，通过确定性直线传输实现高效生成：

- **整流流损失**：$$\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{\mathbf{x}_{0}, \epsilon, t} \left[ || \mathbf{v}_{\theta}(\mathbf{x}_{t}, t, c) - (\mathbf{x}_{0} - \epsilon) ||_{2}^{2} \right]$$ 训练网络预测直线速度场，仅需 20 步即可完成推理，速度是 50 步 DDIM 的 2.5 倍。
- **三重对比损失**：引入 $$\mathcal{L}_{\mathrm{triplet}} = \mathbb{E} \left[ \max \left( 0, d(\hat{\mathbf{v}}, \mathbf{v}^{+}) - d(\hat{\mathbf{v}}, \mathbf{v}^{-}) + m \right) \right]$$ 拉近语义相似运动的速度表示，推远不相似样本，增强运动-条件对齐。
- **联合优化**：$$\mathcal{L}_{\mathrm{CRF}} = \mathcal{L}_{\mathrm{flow}} + \lambda_{\mathrm{triplet}} \mathcal{L}_{\mathrm{triplet}}$$（$$\lambda_{\mathrm{triplet}}=0.1$$）实现重建精度与语义判别性的平衡。

去除三元组对比损失后，交互任务 FID 恶化至 0.783，证实对比学习对生成质量的显著贡献。

### 4. 加权同步损失

现有交互损失（如距离图、相对朝向）仅提供粗粒度的人际约束。DualFlow 设计了**加权同步损失** $$\mathcal{L}_{\mathrm{sync}}$$，显式优化两人关节间的空间关系：

- **距离权重**：$$w_{\mathrm{d}}(j_{1}, j_{2}) = e^{\left( -\alpha \| d_{\mathrm{gt}}(j_{1}, j_{2}) \| \right)}$$ 对自然近距离关节对赋予更高重要性。
- **解剖关节权重**：$$w_{\mathrm{j}}(j_{1}, j_{2})$$ 根据关节所属身体部位（手部、上体、下体）赋予不同固定权重，突出交互关键区域。

消融实验显示，去除 $$\mathcal{L}_{\mathrm{sync}}$$ 后交互任务 FID 升至 0.472，反应任务 FID 升至 0.774，验证了细粒度同步约束对协调性的重要作用。

### 创新总结

| 创新维度 | 基线方法 | DualFlow |
|---------|---------|----------|
| 生成框架 | 扩散模型（多步随机去噪） | 整流流（20步确定性直线传输） |
| 任务统一性 | 交互/反应分离模型 | 统一双分支架构，掩码切换 |
| 多模态语义 | 单一文本或音乐条件 | LLM分解+RAG多模态检索增强 |
| 对比学习 | 无 | 三重对比整流流损失 |
| 同步约束 | 基础交互损失 | 加权同步损失（距离+解剖权重） |

这些创新协同作用，使 DualFlow 在 MDD 交互任务上 R-Precision@3 达到 0.513（InterGen 为 0.302），反应任务 FID 降至 0.686（DuoLando 为 0.698），同时保持仅需 20 步的高效推理。

## 整体框架

DualFlow 是一个基于整流流（Rectified Flow）的统一多模态框架，首次将交互式（Interactive）与反应式（Reactive）两人运动生成整合到单一架构中。整体 pipeline 由三个核心阶段构成：**多模态条件编码与运动检索**、**双分支 Transformer 生成网络**、以及**对比整流流优化与几何正则化**。

### 输入与条件编码

框架接受四类输入：文本描述、音乐音频、演员（Actor，记为 A）的运动序列，以及反应者（Reactor，记为 B）的运动序列。文本通过预训练的 **CLIP ViT-L/14** 编码为语义嵌入，再经一个 Transformer 编码器进一步抽象；音乐则通过 **Jukebox** 编码器提取时序特征潜变量。两人运动序列以统一表征形式输入，每帧包含全局关节位置 $j_g^p \in \mathbb{R}^{3N_j}$、全局关节速度 $j_g^v \in \mathbb{R}^{3N_j}$、局部关节旋转 $j^r \in \mathbb{R}^{6N_j}$ 以及足部接触标签 $j^f \in \mathbb{R}^{N_f}$。

### 检索增强生成模块

为注入细粒度多模态语义，DualFlow 引入了一个检索增强生成（RAG）模块。该模块首先利用 **LLM（GPT-4o）** 将原始文本描述分解为三个子描述——空间关系、身体运动和节奏——分别捕捉两人相对位置、个体动作细节以及与音乐节拍的关联。随后，基于分解后的文本特征（CLIP 嵌入）和音乐特征（Jukebox 嵌入），在运动数据库中检索语义最匹配的运动范例。检索相似度评分结合了余弦相似度与运动长度惩罚，公式为：

$$s_i^q = \langle f_i^q, f_p^q \rangle \cdot e^{-\lambda \cdot \frac{|l_i - l_p|}{\max\{l_i, l_p\}}}$$

其中 $f_i^q$ 和 $f_p^q$ 分别为查询与候选运动的特征嵌入，$l_i$、$l_p$ 为对应运动长度，$\lambda$ 控制长度差异的惩罚强度。检索到的运动范例随后通过检索交叉注意力（Retrieval Cross-Attention）注入生成网络，为运动合成提供显式的语义先验。

### 双分支生成网络

生成网络的核心是级联的 **DualFlow Block**，每个 Block 内包含两个对称分支，分别处理演员和反应者的运动潜变量。每个分支内部由多尺度时间卷积、门控融合、自注意力、音乐交叉注意力和检索交叉注意力等模块堆叠而成。多尺度时间卷积提取不同感受野下的运动节奏特征，门控融合自适应地整合多分辨率信息；自注意力层建模每个人的内部时间依赖，并以文本条件 LayerNorm 注入语义；音乐交叉注意力将运动表示与音乐潜变量对齐。

**任务切换通过掩码机制实现**：在交互模式下，两个分支均激活，Motion Cross-Attention 协调两人的运动生成；在反应模式下，演员分支被掩码，反应者分支中的 Motion Cross-Attention 被替换为带 Look-Ahead 参数 $L$ 的 Causal Cross Attention，使反应者仅能关注演员过去及未来 $L$ 帧的运动，从而模拟实时响应场景。

### 训练目标

DualFlow 的训练目标由三部分组成。**对比整流流损失** $\mathcal{L}_{\mathrm{CRF}}$ 联合了整流流重建损失和三元组对比损失——前者训练网络预测直线传输速度场 $\mathbf{v}_\theta$，后者通过拉近语义相似运动的速度表示、推远不相似样本来锐化运动-条件对齐：

$$\mathcal{L}_{\mathrm{CRF}} = \mathcal{L}_{\mathrm{flow}} + \lambda_{\mathrm{triplet}} \mathcal{L}_{\mathrm{triplet}}$$

**几何正则化损失** $\mathcal{L}_{\mathrm{geo}}$ 约束足部接触、关节速度和骨骼长度，保证单人生理合理性。**交互损失** $\mathcal{L}_{\mathrm{inter}}$ 则引入加权同步损失 $\mathcal{L}_{\mathrm{sync}}$，通过距离权重 $w_d$ 和解剖关节权重 $w_j$ 显式优化两人关节间的空间距离，增强人际协调性。最终总损失为：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{CRF}} + \lambda_{\mathrm{geo}}\mathcal{L}_{\mathrm{geo}} + \lambda_{\mathrm{inter}}\mathcal{L}_{\mathrm{inter}}$$

推理时，DualFlow 仅需 20 步确定性直线采样即可生成高质量运动，速度是 50 步 DDIM 的 2.5 倍。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/002_Figure_2.jpg]]
*Figure 2: (a) Our framework takes text (CLIP-L/14), music, and motion sequences from an actor (A) and reactor (B) as inputs. Motion samples are retrieved using music features and LLM-decomposed text cues (spatial relationship, body movement, rhythm). These modality-specific latents are processed by cascaded Multi-Modal DualFlow Blocks that model interactive dynamics. Outputs are either both actors’ motions (interactive) or only the reactor’s motion (reactive) via a masking mechanism. (b) A DualFlow Block: in the interactive setting, both branches operate symmetrically with Motion Cross Attention coordinating joint motion; in the reactive setting, the actor branch is masked and the reactor branch empl...*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/001_Figure_1.jpg]]
*Figure 1: Our DualFlow model unifies two tasks: (a) Interactive Motion Generation, which synthesizes synchronized two-person interactions, (b) Reactive Motion Generation, which generates responsive motions for Person B (red) conditioned on Person A’s (blue) movements. The generation process is conditioned jointly on text, music, and the retrieved motion samples*

## 核心模块与公式推导

### 3.1 问题形式化

DualFlow将两人运动交互表示为一对同步的运动序列。设演员A的运动为 $\mathbf{x}_a = \{x_a^i\}_{i=1}^{T}$，演员B的运动为 $\mathbf{x}_b = \{x_b^i\}_{i=1}^{T}$，其中 $T$ 为序列长度。每帧运动表示包含以下分量：

- **全局关节位置** $j_g^p \in \mathbb{R}^{3N_j}$：$N_j$ 个关节在世界坐标系下的三维坐标；
- **全局关节速度** $j_g^v \in \mathbb{R}^{3N_j}$：关节位置的逐帧差分；
- **局部关节旋转** $j^r \in \mathbb{R}^{6N_j}$：以6D旋转表示编码的关节局部朝向；
- **足部接触标签** $j^f \in \{0,1\}^{4}$：双脚脚跟与脚尖的地面接触二值标记。

交互式生成任务中，模型需同时生成 $\mathbf{x}_a$ 和 $\mathbf{x}_b$；反应式生成任务中，给定演员A的完整运动 $\mathbf{x}_a$ 作为条件，仅生成反应者B的运动 $\mathbf{x}_b$。

---

### 3.2 多模态运动检索模块（RAG）

**动机**：纯文本条件难以精确刻画两人交互中的空间关系、身体运动细节和节奏特征。DualFlow引入检索增强生成（RAG）模块，从训练集中检索与输入条件最相似的运动片段作为语义范例，为生成过程提供细粒度指导。

**LLM文本分解**：给定原始文本描述，利用GPT-4o将其分解为三个语义聚焦的子描述：

- **空间关系描述**：两人之间的相对位置、朝向和接触模式；
- **身体运动描述**：每人各自的身体动作和运动轨迹；
- **节奏描述**：动作的时间节拍和速度变化。

（LLM分解示例见Table 5）

**检索评分函数**：对每个子描述 $q \in \{\text{spatial}, \text{body}, \text{rhythm}\}$，计算查询嵌入 $f_p^q$ 与数据库中候选运动嵌入 $f_i^q$ 的相似度，并引入运动长度惩罚项：

$$s_i^q = \langle f_i^q, f_p^q \rangle \cdot e^{-\lambda \cdot \frac{|l_i - l_p|}{\max\{l_i, l_p\}}}$$

其中 $\langle\cdot,\cdot\rangle$ 表示余弦相似度，$l_i$ 和 $l_p$ 分别为候选运动与查询运动的帧长度，$\lambda$ 为长度敏感系数。该惩罚项抑制了长度不匹配的运动片段被错误检索，确保检索到的范例在时间尺度上与目标序列一致。

**多模态特征提取**：文本子描述通过CLIP ViT-L/14编码为语义嵌入；音乐条件通过Jukebox编码器提取音乐特征嵌入。两者分别用于检索文本相似和音乐节奏匹配的运动范例。

---

### 3.3 双分支架构与掩码切换机制

DualFlow的核心架构由级联的DualFlow Block构成，每个Block内部包含两个对称分支，分别处理演员A和反应者B的运动表示。**通过掩码机制实现交互与反应模式的统一切换**：

- **交互模式**：两个分支均激活，Motion Cross-Attention在两人运动表示之间建立双向信息流，协调双方的同步运动；
- **反应模式**：演员A分支被掩码，仅反应者B分支激活。此时Motion Cross-Attention被替换为**Causal Cross-Attention with Look-Ahead**，反应者只能关注演员A过去帧及未来 $L$ 帧的运动信息，保证因果性同时允许短时前瞻以提升反应的自然度。

每个DualFlow Block内部包含以下核心计算模块（参见Figure 2）：

| 模块 | 功能 |
|------|------|
| 多尺度时间卷积 + 门控融合 | 提取多分辨率时间特征并自适应融合 |
| Self-Attention | 建模每个人的内部时间依赖，以文本条件LayerNorm注入 |
| Music Cross-Attention | 将运动表示与音乐潜变量对齐 |
| Motion Cross-Attention / Causal Cross-Attention | 交互模式协调两人运动；反应模式以因果掩码关注演员运动 |
| Retrieval Cross-Attention | 利用检索到的运动范例提供语义指导 |
| FFN + 残差连接 | 稳定训练并增加非线性 |

---

### 3.4 对比整流流损失（Contrastive Rectified Flow Loss）

**整流流损失**：DualFlow采用整流流（Rectified Flow）框架，训练网络直接预测从噪声到干净运动的直线传输速度场：

$$\mathcal{L}_{\text{flow}} = \mathbb{E}_{\mathbf{x}_0, \epsilon, t} \left[ \| \mathbf{v}_{\theta}(\mathbf{x}_t, t, c) - (\mathbf{x}_0 - \epsilon) \|_2^2 \right]$$

其中 $\mathbf{x}_t = t\mathbf{x}_0 + (1-t)\epsilon$，$\epsilon \sim \mathcal{N}(0, I)$，$c$ 为条件信息（文本、音乐、检索范例）。网络 $\mathbf{v}_\theta$ 学习预测从噪声样本 $\mathbf{x}_t$ 指向干净数据 $\mathbf{x}_0$ 的确定性速度方向，使得推理时仅需沿直线ODE路径以极少步数（20步）完成采样。

**三重对比损失**：为增强运动表示与语义条件之间的对齐，引入三元组损失，拉近语义相似运动的速度场表示，推远不相似样本：

$$\mathcal{L}_{\text{triplet}} = \mathbb{E} \left[ \max \left( 0, d(\hat{\mathbf{v}}, \mathbf{v}^{+}) - d(\hat{\mathbf{v}}, \mathbf{v}^{-}) + m \right) \right]$$

其中 $\hat{\mathbf{v}}$ 为当前样本的预测速度场，$\mathbf{v}^{+}$ 和 $\mathbf{v}^{-}$ 分别为正、负样本的速度场，$d(\cdot,\cdot)$ 为余弦距离，边界值 $m=0.2$。

**联合损失**：

$$\mathcal{L}_{\text{CRF}} = \mathcal{L}_{\text{flow}} + \lambda_{\text{triplet}} \mathcal{L}_{\text{triplet}}, \quad \lambda_{\text{triplet}}=0.1$$

---

### 3.5 几何正则化与同步损失

**几何正则化损失**：约束单人生成的物理合理性，包含三项：

$$\mathcal{L}_{\text{geo}} = \mathcal{L}_{\text{foot}} + \lambda_{\text{vel}}\mathcal{L}_{\text{vel}} + \lambda_{\text{BL}}\mathcal{L}_{\text{BL}}$$

- $\mathcal{L}_{\text{foot}}$：足部接触损失，约束足部在接触地面时速度为零；
- $\mathcal{L}_{\text{vel}}$：关节速度平滑损失，抑制高频抖动；
- $\mathcal{L}_{\text{BL}}$：骨骼长度约束，保证肢体段长度恒定。

**加权同步损失**：显式优化两人关节间的空间协调性，是DualFlow区别于基线方法的关键设计：

$$\mathcal{L}_{\text{sync}} = \sum_{j_1, j_2} w_{\text{d}}(j_1, j_2) \cdot w_{\text{j}}(j_1, j_2) \cdot \| d_{\text{p}}(j_1, j_2) - d_{\text{gt}}(j_1, j_2) \|^2$$

其中 $d_{\text{p}}$ 和 $d_{\text{gt}}$ 分别为预测和真实的两关节间欧氏距离。两项自适应权重分别从空间距离和解剖重要性两个维度加权：

- **距离权重**：对自然近距离关节对赋予更高重要性，指数衰减形式：

$$w_{\text{d}}(j_1, j_2) = e^{-\alpha \| d_{\text{gt}}(j_1, j_2) \|}$$

- **解剖关节权重**：根据关节所属身体部位赋予固定权重：

$$w_{\text{j}}(j_1, j_2) = \begin{cases} w_{\text{h}}, & j_1, j_2 \in \mathcal{I}_{\text{hands}} \\ w_{\text{u}}, & j_1, j_2 \in \mathcal{I}_{\text{upper}} \\ w_{\text{l}}, & j_1, j_2 \in \mathcal{I}_{\text{lower}} \\ w_{\text{small}}, & \text{otherwise} \end{cases}$$

其中 $\mathcal{I}_{\text{hands}}$、$\mathcal{I}_{\text{upper}}$、$\mathcal{I}_{\text{lower}}$ 分别表示手部、上半身、下半身关节集合，$w_{\text{h}} > w_{\text{u}} > w_{\text{l}} \gg w_{\text{small}}$ 反映了手部交互在舞蹈等场景中的核心地位。

**交互损失**：组合距离图损失、相对朝向损失和同步损失：

$$\mathcal{L}_{\text{inter}} = \mathcal{L}_{\text{DM}} + \lambda_{\text{RO}}\mathcal{L}_{\text{RO}} + \lambda_{\text{sync}}\mathcal{L}_{\text{sync}}$$

**总训练目标**：

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{CRF}} + \lambda_{\text{geo}}\mathcal{L}_{\text{geo}} + \lambda_{\text{inter}}\mathcal{L}_{\text{inter}}$$

该损失函数联合优化重建精度、语义对齐、物理合理性和人际协调性，使DualFlow在仅20步直线采样中即可生成高度同步且语义一致的两人协调运动。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/010_Table_5.jpg]]
*Table 5: Examples of input text decomposed into three fine-grained, semantically focused descriptions using LLM for MDD Dataset*

## 实验与分析

### 主实验：双人交互与反应式生成

DualFlow 在三个公开基准（MDD、InterHuman-AS、DD100）上均显著超越现有方法，覆盖文本和音乐双模态条件。

**MDD 双人舞数据集（Table 1）：** 在交互式生成任务（text+music）上，DualFlow 的 R-Precision@3 达到 0.513，比 **InterGen**（Liang et al., 2024）的 0.302 提升 **69.9%**；FID 降至 0.415，优于 InterGen 的 0.426。在反应式生成任务上，DualFlow 的 R-Precision@3 为 0.471，远超 **DuoLando** 的 0.219（提升 115%），FID 为 0.686，优于 DuoLando 的 0.698。多模态距离（MMDist）在反应任务上为 1.056，相比 DuoLando 的 2.113 缩减约 50%，表明运动-条件语义对齐显著增强。

**InterHuman-AS 文本交互生成（Table 2）：** 在纯文本条件下，DualFlow 的 R-Precision@1 达到 0.437，而 InterGen 仅为 0.113，提升幅度达 **287%**，证明检索增强和对比整流流在多模态条件削弱时仍能维持强语义对齐。

**DD100 文本反应式生成（Table 3）：** DualFlow 同样展现出跨数据集的泛化能力，在反应式单人响应生成任务上保持领先。

### 推理效率

DualFlow 基于整流流框架，推理过程为确定性直线传输，仅需 **20 步**即可完成生成。相比 50 步 DDIM，推理速度提升 **2.5 倍**（Fig. 4），同时 FID 随步数减少的退化幅度远小于扩散基线，在低步数区间仍保持高质量。

### 消融实验

**检索增强生成（RAG）模块（Table 7）：** 完全移除 RAG 后，交互任务 FID 从 0.415 升至 0.622，R-Precision 大幅下降，验证了检索运动范例对语义保真度的关键作用。在反应式任务中，检索深度 k=3 提供最佳语义对齐；k≥5 时引入时序漂移，性能反而下降。

**对比整流流损失（Table 4）：** 去除三元组对比损失 $\mathcal{L}_{\mathrm{triplet}}$ 后，交互任务 FID 恶化至 0.783，表明对比学习对锐化运动速度场表示、增强条件-运动对齐至关重要。

**同步损失（Table 8）：** 移除加权同步损失 $\mathcal{L}_{\mathrm{sync}}$ 后，交互任务 FID 升至 0.472，R-Precision 降低；反应任务 FID 升至 0.774。该损失通过距离权重 $w_{\mathrm{d}}$ 和解剖关节权重 $w_{\mathrm{j}}$ 显式约束两人关节间距离，对维持人际空间协调性不可或缺。

**多尺度时间卷积（Table 6）：** 用单一卷积替代多尺度卷积后，R-Precision@1 从 0.185 降至 0.172，FID 升至 0.595，验证了多分辨率时间特征提取对捕捉不同节奏层次运动的必要性。

### 定性分析

Fig. 5 的可视化对比显示，InterGen 在交互生成中产生手部间距不自然、身体穿透、遗漏 Alemana 转身等问题；DuoLando 在反应生成中出现腿部启动错误和头部朝向偏差。DualFlow 生成的编舞动作平滑、文本对齐度高，且同伴响应与真值高度一致。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/008_Figure_5.jpg]]
*Figure 5: Comparing DualFlow with InterGen (interactive) and DuoLando (reactive) against ground truth on MDD Dataset. Black circles mark regions where baselines lose contact or produce distortions. InterGen shows artifacts like unnatural hand spacing, body interpenetration, and skipping the Alemana (follower’s inside turn), while DuoLando shows incorrect leg initiation and head orientation. In contrast, DualFlow generates smooth, text-aligned choreography and coherent partner responses closely matching the ground truth. Supplementary video provides detailed visualizations*

### 失败模式与局限

尽管整体表现优异，DualFlow 在以下场景存在退化：
- **检索质量依赖：** 当输入文本、领导者运动或音乐模糊时，RAG 可能检索到语义不匹配的邻居，导致风格漂移或动作偏离。
- **近距离接触穿透：** 反应式设置下，手握手或躯干靠近等序列偶尔出现穿透和物理协调偏差，欠缺显式物理接触约束。
- **长序列时序漂移：** 检索基于局部运动片段，长序列生成会累积时序漂移，削弱长程结构一致性和拍点对齐。

### 公平性说明

所有模型在相同数据集（MDD、InterHuman-AS、DD100）上训练和评估，使用统一的评价指标（FID、MMDist、R-Precision 等）。DualFlow 与基线共享相同的文本编码器（CLIP ViT-L/14）和音乐编码器（Jukebox），消融实验保持训练协议和超参数搜索空间一致。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/003_Table_1.jpg]]
*Table 1: Duet Generation results on MDD dataset with both text and music modalities. Bold for best, underline for second best*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/005_Table_2.jpg]]
*Table 2: Interactive Two-person Generation results conditioned on text modality for the InterHuman-AS dataset*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/007_Table_3.jpg]]
*Table 3: Reactive Motion Generation results conditioned on text modality for the DD100 dataset*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/009_Table_4.jpg]]
*Table 4: Ablation Study on MDD dataset (both text & music)*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/011_Table_6.jpg]]
*Table 6: Ablation study results for Reactive Setting on the MDD dataset*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/012_Table_7.jpg]]
*Table 7: Ablation Study on RAG in DualFlow on the MDD dataset*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/013_Table_8.jpg]]
*Table 8: Ablation Study on Synchronization Loss on the MDD dataset*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2509_24099/figures/004_Figure_3.jpg]]
*Figure 3: User study results*

## 方法谱系与知识库定位

### 1. 与基线工作的关系

DualFlow 的提出建立在单人运动生成与双人交互运动生成两条技术路线的交汇点上。其核心突破在于将先前分离的“交互式”与“反应式”生成任务统一到单一框架内，同时引入检索增强与整流流，形成差异化的方法定位。

**相对于扩散式单人运动生成模型**

以 **MDM**（Tevet et al., 2022）为代表的扩散模型将运动生成建模为多步随机去噪过程，通过 Transformer 骨架处理文本条件。DualFlow 继承了 Transformer 骨架与条件注入的思路，但将生成框架从扩散模型迁移至**整流流**。这一迁移带来了两个结构性优势：一是推理从 50 步 DDIM 压缩至 20 步直线采样，速度提升 2.5 倍；二是确定性传输路径避免了扩散模型中随机采样带来的误差累积。此外，MDM 原生仅支持单人运动，扩展至双人场景需外部协调机制，而 DualFlow 通过双分支架构原生建模人际交互。

**相对于扩散式双人交互生成模型**

**InterGen**（Liang et al., 2024）是基于扩散的两人交互运动生成模型，通过共享潜空间协调双人运动。DualFlow 在交互任务上与 InterGen 直接对标，并在 MDD 数据集上实现了显著超越：R-Precision@3 从 0.302 提升至 0.513（+69.9%），FID 从 0.426 降至 0.415（-2.6%）。InterGen 的局限性在于仅支持文本条件且无法处理反应式生成，而 DualFlow 通过 RAG 模块同时注入文本与音乐多模态语义，并通过掩码机制无缝切换交互/反应模式。定性分析显示，InterGen 在紧密接触场景中存在身体穿透、手部间距异常等问题，而 DualFlow 的加权同步损失显式约束了关节间距离，缓解了此类伪影。

**相对于反应式运动生成模型**

**DuoLando** 是现有反应式两人运动生成的代表性工作，支持文本或音乐条件。在 MDD 反应式任务上，DualFlow 的 FID（0.686）优于 DuoLando（0.698），MMDist 从 2.113 降至 1.056，语义对齐指标提升超过一倍。DuoLando 采用独立架构处理反应式任务，无法复用于交互式生成，而 DualFlow 通过因果交叉注意力与 Look-Ahead 机制在统一架构内实现了反应式条件建模。这一设计的关键在于：反应者分支仅关注自身历史帧与领导者未来 L 帧的运动信息，通过上三角掩码实现因果约束，从而在保持架构统一性的同时避免信息泄露。

### 2. 适用边界

DualFlow 的设计假设和实验设置界定了其有效范围：

- **双人场景限定**：框架显式建模两个角色的运动及其交互，未验证扩展至三人及以上群组交互的能力。双分支架构的对称设计在多人场景中可能面临组合爆炸问题。
- **舞蹈/互动动作域**：训练与评估均在舞蹈类数据集（MDD、InterHuman-AS）和日常交互数据集（DD100）上进行，生成的动作风格受限于这些域内的动作分布。对于体育对抗、格斗等高频接触或高动态场景，现有同步损失缺乏物理接触约束，生成质量未经检验。
- **检索依赖**：RAG 模块的性能依赖于检索库的覆盖度和质量。当输入文本、领导者运动或音乐特征模糊时，检索到的运动范例可能与目标语义不匹配，导致风格漂移或动作偏离。这一依赖在开放域或低资源场景下构成瓶颈。
- **中短时序生成**：检索基于局部运动片段，长序列生成会累积时序漂移，削弱长程结构一致性和音乐拍点对齐。当前框架缺乏显式的层次化时间建模来缓解这一问题。

### 3. 局限与开放问题

**已识别的局限**

1. **检索鲁棒性不足**：RAG 模块的语义对齐质量受限于检索样本的相关性。当多模态条件模糊或检索库稀疏时，可能引入语义不匹配的运动范例，导致生成动作偏离文本或音乐描述。消融实验表明，完全移除 RAG 模块使交互任务 FID 从 0.415 升至 0.622，验证了检索质量对整体性能的关键影响。

2. **物理接触建模缺失**：在反应式设置下，近距离接触序列（如手握手或躯干靠近）偶尔出现穿透和物理协调偏差。当前同步损失通过距离权重和解剖权重约束关节间距离，但缺乏力反馈、穿透惩罚等显式物理约束，难以保证高接触场景的物理真实性。

3. **长序列时序漂移**：检索基于局部运动片段，长序列生成会累积时序漂移。反应式任务中，检索深度 k=3 提供最佳语义对齐，k=5 或更高将引入时序漂移，表明当前检索机制难以维持长程时间一致性。

**开放问题**

1. **检索增强的鲁棒性提升**：如何通过语义重排序、跨模态评分或不确定性感知检索来提高 RAG 的鲁棒性？在模糊条件下，能否引入自适应检索深度或检索结果质量评估机制来避免语义漂移？

2. **物理接触约束的集成**：如何加入基于物理的接触约束（如力反馈、穿透惩罚、接触面建模）以提升近距离互动的真实感？这需要在不破坏整流流端到端训练特性的前提下设计可微分物理损失。

3. **层次化时间建模**：如何引入层次化时间建模（如粗粒度音乐节拍对齐与细粒度动作生成的分层结构）来缓解长序列生成中的结构漂移，同时保持 20 步采样的高效推理？

4. **少样本风格泛化**：当前框架依赖大规模标注数据训练。能否通过检索库的动态更新或元学习策略，实现少样本甚至零样本的风格泛化到新的舞蹈流派或交互模式？

5. **多人扩展**：对比整流流的训练策略是否能迁移到更多人数（如群组舞蹈）或更复杂的物理交互场景？双分支架构的对称设计在多人场景中需要重新设计注意力机制和同步损失。

## 原文 PDF

![[paperPDFs/arxiv_2025/DualFlow_Unified_Multi_Modal_Interactive_Reactive_3D_Motion_Generation_via_Rectified_Flow.pdf]]