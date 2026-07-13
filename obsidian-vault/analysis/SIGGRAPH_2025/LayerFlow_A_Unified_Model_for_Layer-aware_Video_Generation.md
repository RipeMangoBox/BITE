---
title: "LayerFlow: A Unified Model for Layer-aware Video Generation"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/LayerFlow_A_Unified_Model_for_Layer_aware_Video_Generation.pdf
project_link: "https://s2025.conference-schedule.org/presentation/?id=papers_572&sess=sess146"
code_link: null
aliases:
- LayerFlow
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过 Motion LoRA 和 Content LoRA 对预训练 DiT‑T2V 模型进行多阶段适应，从而将高质量静态图层图像的知识迁移到视频生成中，同时保留动态运动先验。
primary_logic: 将不同图层的视频片段拼接为长序列并注入可学习的图层嵌入，使得单一扩散变换器能够同时生成多个对齐的图层视频；进一步结合图像-视频联合训练与 LoRA 解耦动静态表征，突破了多层视频数据稀缺的瓶颈。
claims:
- 联合图像-视频训练在所有 VBench 指标上均优于纯视频训练，尤其美学质量显著提升。
- 用户研究中，LayerFlow 的整体质量和文本对齐得分明显高于 LayerDiffuse+运动模块的流水线。
- 消融实验表明，去除 Motion LoRA 并在推理时仅保留 Content LoRA 能恢复视频动态，同时提高图层分离质量。
- VBench (prompt sets) 上 Aesthetic Quality BL = 0.5742 (LayerFlow joint)
---

# LayerFlow: A Unified Model for Layer-aware Video Generation

> [!tip] 核心洞察
> 将不同图层的视频片段拼接为长序列并注入可学习的图层嵌入，使得单一扩散变换器能够同时生成多个对齐的图层视频；进一步结合图像-视频联合训练与 LoRA 解耦动静态表征，突破了多层视频数据稀缺的瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | LayerFlow：面向图层感知视频生成的统一模型 |
| 英文题名 | LayerFlow: A Unified Model for Layer-aware Video Generation |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](http://arxiv.org/abs/2506.04228v1) · [paper](https://arxiv.org/abs/2506.04228) · [Project](https://s2025.conference-schedule.org/presentation/?id=papers_572&sess=sess146) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | LayerFlow |
| Dataset | VBench, User Study, DAVIS |

> [!tip] 效果简介
> - VBench (prompt sets) 上，Aesthetic Quality BL 0.5742 (LayerFlow joint) vs 0.4959 (LayerFlow purely video) (+0.0783)。
> - User Study 上，Overall Quality Score 91.17 (LayerFlow joint) vs 74.68 (LayerFlow purely video) (+16.49)。
> - DAVIS (decomposition) 上，Aesthetic Quality FG 0.4240 (LayerFlow joint) vs 0.3973 (LayerFlow purely video) (+0.0267)。

## 概要

高质量多层视频训练数据严重稀缺，现有视频生成方法无法在统一框架下同时生成前景透明、背景干净及混合场景的图层感知视频。**LayerFlow** 提出一种基于预训练 DiT 文本到视频扩散变换器的统一模型，将不同图层的视频片段在时间维拼接为长序列，并通过可学习的图层嵌入区分各图层及其对应提示，使单一模型能同时输出多个对齐的图层视频。针对多层视频数据稀缺的瓶颈，设计了三阶段训练策略：先以粗粒度视频数据训练基座模型获得初始图层生成能力，再通过 **Motion LoRA** 适应静态图像数据，最后叠加 **Content LoRA** 从高质量图像-视频联合数据中学习内容细化，推理时移除 Motion LoRA 以恢复视频动态。

实验表明，联合图像-视频训练在所有 VBench 指标上均优于纯视频训练，美学质量从 0.4959 提升至 0.5742；用户研究中 LayerFlow 的整体质量得分达 91.17，显著高于 LayerDiffuse+运动模块流水线的 74.68。该方法为图层感知视频生成提供了统一、可扩展的基线方案。

## 核心方法与创新机理

**瓶颈**：高质量多层视频训练数据严重稀缺——现有数据仅能通过粗糙的“复制-粘贴”合成，导致前景边缘模糊、背景严重虚化；而直接微调预训练文本到视频（T2V）扩散模型会破坏其运动动态先验，产生静态化输出。

**核心机制**：LayerFlow 将不同图层的视频组织为子片段并在时间维拼接成一个长序列，通过可学习的层嵌入（layer embedder）注入图层感知，使单一 DiT 扩散变换器能够同时生成前景透明、背景干净和混合场景的对齐视频。在此基础上，通过 Motion LoRA 和 Content LoRA 的多阶段解耦适应，将高质量静态图层图像的知识迁移到视频生成中，同时保留动态运动先验。

**关键设计变更**：

1. **视频表示**：将前景（RGB）、前景（Alpha）、背景和混合四个子片段在时间维拼接为统一长序列，替代传统的单一视频片段输入。这使得模型能在统一的 3D 注意力计算中共享图层间信息，同时保持各图层的时空一致性。

2. **文本条件与图层感知**：为每个图层提示附加索引数字（如“1, a running dog”），经 T5 编码后，通过可学习的 layer embedder 将索引投影为与文本嵌入同尺寸的层嵌入，二者相加后注入 DiT 的交叉注意力层：
   $$\mathcal{L}(\theta) := \mathbb{E}_{t, x_0, y, i_l, \epsilon} \left\| \epsilon - \epsilon_\theta\left(\sqrt{\bar{\alpha}_t} x_0 + \sqrt{1-\bar{\alpha}_t} \epsilon, t, \tau_\theta(y) + \tau_l(i_l)\right) \right\|^2$$
   其中 $\tau_\theta(y)$ 为文本嵌入，$\tau_l(i_l)$ 为层嵌入，$i_l$ 为图层索引。

3. **三阶段训练与 LoRA 解耦**：
   - **阶段一**：在粗糙合成多层视频数据上微调基座模型，建立初始分层生成能力。
   - **阶段二（Motion LoRA）**：在注意力查询投影中引入低秩适应矩阵 $AB^T$，通过标量 $\alpha$ 控制静态/动态模式：
     $$Q = W^Q z + \alpha \cdot AB^T z$$
     训练时设 $\alpha=1$ 使模型适应静态图层图像数据，推理时设 $\alpha=0$ 移除 Motion LoRA 以恢复视频动态。
   - **阶段三（Content LoRA）**：在 Motion LoRA 基础上叠加第二个低秩矩阵 $CD^T$：
     $$Q = W^Q z + \alpha \cdot AB^T z + CD^T z$$
     结合高质量静态图层图像和视频数据进行联合训练，使 Content LoRA 学习内容细化（如清晰边缘、丰富纹理），推理时保留 Content LoRA 同时移除 Motion LoRA，实现动态视频与高质量图层的兼顾。

**架构基础**：LayerFlow 继承 CogVideoX 的 VAE 编解码器和 DiT Transformer 骨干，在 3D 全注意力机制上进行扩展，无需修改基础架构即可实现图层感知生成。

![[assets/figures/papers/paper_list_l8_http_arxiv_org_abs_2506_04228v1/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of LayerFlow, which allows for the production of multi-layer videos including transparent foreground, undisturbed background and blended sequences. We organize videos of different layers as sub-clips and concatenate them to form a whole sequence to be encoded by VAE encoder. At the same time, index modification is conducted before prompts are processed by the ?? 5 encoder, then layer embedding is added to text embeddings to impart layer awareness. All the visual patches and text embeddings are fed into transformer blocks as a long tensor. In the process of training, a base model is firstly trained on crudely made multi-layer video data for initial layered generation ability...*

![[assets/figures/papers/paper_list_l8_http_arxiv_org_abs_2506_04228v1/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison for multi-layer video generation with generation then animation pipeline, i.e., composition of LayerDiffuse [Zhang and Agrawala 2024] and motion module [Guo et al. 2023], where LayerFlow achieves better layer-level coherence and clearer separation of layers*

## 实验与关键发现

### 核心定量结果

LayerFlow 在生成与分解两类任务上均展现出相对于纯视频训练基线和现有替代方案的显著优势。所有评估均基于 VBench 指标集，涵盖前景（FG）、背景（BG）和混合图层（BL）三个维度。

**多图层生成任务**（Table 1）：联合图像-视频训练的 LayerFlow 在所有指标上全面超越纯视频训练版本。最具代表性的混合图层美学质量（Aesthetic Quality BL）从 0.4959 提升至 0.5742（+0.0783），前景美学质量从 0.6377 提升至 0.6506，背景质量从 0.5733 提升至 0.5820。这一提升的因果机制在于：纯视频训练数据质量粗糙，导致前景边缘模糊、背景严重虚化（见 Fig. 3 消融可视化）；而引入高质量静态图层图像后，Content LoRA 将精细的图层分离知识迁移至视频生成过程，同时 Motion LoRA 在推理时被移除以恢复运动动态。

与替代架构的对比进一步验证了设计选择的有效性。LayerDiffuse + motion module 流水线（先逐帧生成图层图像再动画化）在混合图层美学质量上仅达到 0.5270，显著低于 LayerFlow 的 0.5742。“Channel-concatenate”架构（将图层维度合并到通道维度的变体）表现更差，混合图层质量仅为 0.4835。这表明**时间维拼接 + 层嵌入**的设计在图层间信息共享和时序一致性上具有本质优势。

**多图层分解任务**（Table 3）：在 DAVIS 数据集（50 个视频序列）上，联合训练模型同样优于纯视频训练基线。前景美学质量从 0.3973 提升至 0.4240（+0.0267），背景质量从 0.4360 提升至 0.4467。值得注意的是，分解任务的提升幅度小于生成任务，这与分解本身对图层边缘重建精度要求更高有关——纯视频模型在边缘处的模糊问题在分解场景下更为突出。

### 用户研究验证

30 名标注者对视频的五个维度（整体质量、文本对齐、前景、背景、混合图层）进行 1-4 分偏好评分，满分 100 分（Table 2）。联合训练 LayerFlow 的整体质量得分高达 91.17，而纯视频训练版本仅为 74.68（差距 +16.49）；文本对齐得分分别为 89.33 和 74.17（差距 +15.16）。与 LayerDiffuse + motion module 流水线（整体质量 74.68）相比，LayerFlow 的优势同样显著。用户偏好的一致性表明，**联合图像-视频训练不仅提升了客观指标，更在人类感知层面带来了可辨识的质量增益**。

![[assets/figures/papers/paper_list_l8_http_arxiv_org_abs_2506_04228v1/figures/007_Table_2.jpg]]
*Table 2: User study for multi-layer video generation on LayerFlow and existing alternatives. “Quality” and “T-A” measure overall synthesis quality and text alignment respectively, “FG”, “BG”, and “BL” refer to the detailed evaluation of the foreground, background, and blended video*

### 关键消融发现

**训练数据质量的影响**（Fig. 3）：仅使用粗粒度视频数据训练的第一阶段基座模型，其输出与当前 SOTA 视频生成模型之间存在不可忽视的质量差距。具体表现为前景边缘不清晰、背景严重模糊且保真度低。引入高质量静态图像数据后，背景合成变得清晰无干扰，文本对齐程度（如“colorful flowers”等语义细节）显著提升。

**Motion LoRA 与 Content LoRA 的解耦作用**（Section 4.3）：消融实验揭示了两个 LoRA 模块的独立贡献。推理时移除 Motion LoRA（将 α 设为 0）能够恢复视频的动态程度，而保留 Content LoRA 则维持了图层生成的精细化质量。若同时移除两者，模型退化为仅经过第一阶段训练的基座模型，图层分离质量急剧下降。这一发现验证了**动静态表征解耦**策略的有效性：Motion LoRA 负责适应静态图像模式，Content LoRA 负责从高质量数据中学习内容增强，推理时可根据需求灵活组合。

### 失败模式与适用边界

尽管 LayerFlow 在图层感知视频生成上取得了突破性进展，但存在以下明确限制：

1. **固定图层数量**：当前框架仅支持前景、背景、混合三个固定图层，无法处理可变数量的图层场景。这是由子片段拼接和层嵌入的固定维度设计所决定的架构约束。

2. **动态程度折损**：Table 1 中，联合训练模型的 Dynamic Degree 指标（BL）为 0.4000，略低于纯视频训练版本的 0.4250。这表明尽管推理时移除 Motion LoRA 能够恢复大部分运动动态，但高质量静态图像数据的引入仍对视频动态程度造成轻微抑制。在需要极高动态程度的场景下，这一折损需要被纳入考量。

![[assets/figures/papers/paper_list_l8_http_arxiv_org_abs_2506_04228v1/figures/006_Table_1.jpg]]
*Table 1: Quantitative analysis for model framework and training data of multi-layer generation. Two groups of comparison are included, one is between our model trained without (top row) or with (bottom row) image data, and the other is among different architectures including our framework, LayerDiffuse [Zhang and Agrawala 2024]+motion module [Guo et al. 2023], and “Channel-concatenate” architecture (first three rows). Here, “FG”, "BG", and "BL" refer to foreground, background, and blended layer*

3. **分解任务边缘精度**：分解任务中前景美学质量的提升幅度（+0.0267）小于生成任务（+0.0129），且绝对数值（0.4240）仍处于中等水平。这暗示模型在重建被遮挡区域的图层边缘时仍存在锐度不足的问题，尤其在复杂遮挡场景下语义一致性可能下降。

### 证据强度评估

- **高置信度**（≥0.95）：联合训练在所有 VBench 指标上优于纯视频训练（Table 1, Table 3）；用户研究偏好得分显著领先（Table 2）；图层拼接架构优于通道拼接变体。
- **中等置信度**（0.90）：Motion LoRA 移除恢复动态的消融结论（Section 4.3 底部段落，需结合 Table 3 底部行数据交叉验证）；分解任务评估基于 DAVIS 数据集 50 个序列，样本量适中但非大规模。
- **需人工核实**：论文未提供统计显著性检验（如 p 值或置信区间），部分指标提升幅度较小（如分解任务前景质量 +0.0267）的统计意义尚不明确。用户研究的标注者间一致性指标未报告。

![[assets/figures/papers/paper_list_l8_http_arxiv_org_abs_2506_04228v1/figures/008_Table_3.jpg]]
*Table 3: Quantitative analysis for model framework and training data of multi-layer video decomposition. Two groups of comparison are included, one is between our model trained without (top row) and with (bottom row) images, and the other is between different architectures of our base model (top row), and “Channel-concatenate” (middle row)*

![[assets/figures/papers/paper_list_l8_http_arxiv_org_abs_2506_04228v1/figures/003_Figure_3.jpg]]
*Figure 3: Ablation for training data. We visualize the results for models trained on purely video data and joint image and video data. Without high-quality image data, the model tends to generate a fuzzy background with obvious blur and low fidelity, while joint image-video data training contributes to undisturbed background synthesis and a higher level of text alignment (e.g., "colorful flowers") and generation quality*

## 定位与知识库关联

**问题域定位**：LayerFlow 首次将图层感知生成从静态图像拓展到视频域，填补了“统一模型同时生成前景透明、背景干净及混合场景的多层视频”这一空白。此前的工作要么仅处理静态图层图像生成（如 **LayerDiffuse**，Zhang and Agrawala, 2024），要么将图层分解与视频动画分离为流水线（LayerDiffuse + 运动模块，Guo et al., 2023），缺乏端到端的图层级视频一致性。

**与基线流水线的本质差异**：LayerFlow 与“LayerDiffuse + 运动模块”流水线的核心区别不在于是否使用扩散模型，而在于**时空注意力的统一性**。流水线方法先逐帧生成图层图像再注入时序运动，导致图层间的时间对齐依赖后处理；LayerFlow 则在 DiT 骨干的 3D 全注意力中同时处理所有图层的时空 patch，使前景透明边缘、背景遮挡区域和混合帧在扩散去噪过程中自然协同。这一差异在用户研究中得到验证：LayerFlow 的整体质量得分（91.17）远高于流水线（74.68），且图层分离清晰度获得一致偏好（Table 2）。

**知识库挂载点**：
- **视频扩散变换器**：LayerFlow 直接继承 CogVideoX 的 VAE 编解码器和 DiT 骨干，未修改基础架构，表明其方法可迁移至任何 DiT-based T2V 模型。
- **LoRA 参数高效微调**：Motion LoRA 和 Content LoRA 的设计遵循标准低秩适应范式，但创新在于将“动/静态模式切换”编码为标量系数 α（α=1 为静态图像模式，α=0 恢复视频动态），推理时通过移除 Motion LoRA 实现零开销的模式切换（Eq. 2, Eq. 3）。
- **图层条件注入**：可学习的 Layer Embedder 将图层索引投影为与 T5 文本嵌入同维度的条件向量，以加法方式注入（Eq. 1），这与 ControlNet 等外部条件注入机制形成对比——LayerFlow 的条件来自序列内部的结构化索引，而非额外控制信号。

**适用边界**：
- **固定图层数量**：当前模型仅支持前景、背景、混合三个图层，无法扩展到可变数量的图层。这是子片段拼接策略的固有约束——时间维度的拼接长度与图层数绑定。
- **动态程度折损**：联合图像-视频训练虽然显著提升美学质量（Aesthetic Quality BL 从 0.4959 到 0.5742，Table 1），但 Dynamic Degree 指标略低于纯视频训练基线，表明静态图像数据的引入对运动幅度有轻微抑制作用。推理时移除 Motion LoRA 可部分恢复动态，但未能完全消除这一折损。
- **数据依赖瓶颈**：高质量多层视频训练数据仍然稀缺，当前方案依赖“复制粘贴”合成数据与静态图层图像的联合训练，对于复杂遮挡和快速运动的场景，分解质量可能下降（Table 3 中 FG Aesthetic Quality 仅从 0.3973 提升至 0.4240，提升幅度有限）。

**后续启发**：
- 可变图层数量的扩展可能需要在序列拼接之外引入图层维度的条件编码机制，例如将图层索引作为可扩展的位置编码而非固定长度的子片段。
- 分解任务中图层边缘锐度的提升方向可参考抠图（matting）领域的边缘感知损失，将其引入扩散训练目标。
- 该框架的“子片段拼接 + 层嵌入”策略为其他结构化视频生成任务（如多视角视频、多对象独立控制）提供了可复用的技术模板，只需将图层索引替换为视角索引或对象标识即可。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/LayerFlow_A_Unified_Model_for_Layer_aware_Video_Generation.pdf]]