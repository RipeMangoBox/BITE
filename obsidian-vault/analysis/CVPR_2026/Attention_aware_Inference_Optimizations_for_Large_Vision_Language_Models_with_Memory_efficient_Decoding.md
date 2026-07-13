---
title: Attention-aware Inference Optimizations for Large Vision-Language Models with Memory-efficient Decoding
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Attention_aware_Inference_Optimizations_for_Large_Vision_Language_Models_with_Memory_efficient_Decoding.pdf
project_link: null
code_link: "https://github.com/gitdisl/AttentionPack"
aliases:
- AAIOLVLMMED
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用视觉令牌键值向量的内在低秩特性，沿隐藏维度进行多注意力头联合压缩，同时引入基于注意力累积分数的部分解压缩，直接缩小每令牌的存储体积。
primary_logic: 视觉令牌通常携带冗余信息，其键值向量的内在秩远低于其显式的特征维度；先沿头维度合并再作奇异值分解，可大幅压缩缓存而几乎不损失模型质量，且配合注意力感知的部分解压能抵消解压时延。
claims:
- 视觉令牌的键值向量可被压缩多达8倍而不损害模型输出质量。
- 在LLaVA1.5-7B上，压缩秩R_kv=R_vv=64时，缓存缩小5.09倍，A-OKVQA准确率从76.64%提升至76.88%。
- VideoLLaVA‑7B上，压缩秩R_kv=R_vv=128时，缓存缩小8.11倍，MSVD‑QA准确率仅比FastV低0.39%。
- 对值缓存的前25%令牌使用全秩解压即可达到与全解压几乎相同的性能，同时解压FLOPs降低约30%。
---

# Attention-aware Inference Optimizations for Large Vision-Language Models with Memory-efficient Decoding

> [!tip] 核心洞察
> 视觉令牌通常携带冗余信息，其键值向量的内在秩远低于其显式的特征维度；先沿头维度合并再作奇异值分解，可大幅压缩缓存而几乎不损失模型质量，且配合注意力感知的部分解压能抵消解压时延。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向大规模视觉语言模型的注意力感知推理优化与内存高效解码 |
| 英文题名 | Attention-aware Inference Optimizations for Large Vision-Language Models with Memory-efficient Decoding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.23914) · [Code](https://github.com/gitdisl/AttentionPack) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AttentionPack |
| Dataset | A-OKVQA, OCR-VQA, MMMU, MSVD-QA |

> [!tip] 效果简介
> - A-OKVQA 上，准确率 (Accuracy) 76.88% vs 76.64% (Full KV Caching) (+0.24%)。
> - OCR-VQA 上，ROUGE-L 52.44 vs 51.05 (Full KV Caching) (+1.39)。
> - MMMU 上，准确率 (Accuracy) 34.59% vs 34.68% (Full KV Caching) (-0.09%)。

## 概要

大规模视觉语言模型在解码过程中需存储巨量键值对缓存，视觉令牌的高占比使显存瓶颈尤为突出，严重制约批处理规模与上下文长度。针对该问题，本文提出 **AttentionPack**，一种注意力感知的KV缓存压缩与部分解压方法。

核心思路源于一个关键观察：视觉令牌的键值向量具有内在低秩特性，其有效秩远低于显式特征维度。AttentionPack 先将多注意力头的键值向量沿头轴合并，再通过随机化奇异值分解压缩为低秩表示，从而大幅缩减每令牌的存储体积。在解码时，利用历史累计注意力分数对令牌进行重要性分组——高重要性令牌以全秩解压，低重要性令牌以降秩解压——以抵消解压带来的计算延迟。

主要实验结果如下：

- **缓存压缩比**：在 LLaVA1.5-7B 上，压缩秩 $R_{kv}=R_{vv}=64$ 时，缓存缩小 **5.09 倍**，A-OKVQA 准确率从 76.64% 提升至 76.88%；在 VideoLLaVA-7B 上，压缩秩 $R_{kv}=R_{vv}=128$ 时，缓存缩小 **8.11 倍**，MSVD-QA 准确率仅比 FastV 低 0.39%。
- **部分解压效率**：仅对前 25% 重要视觉令牌以全秩解压值缓存，精度几乎不变，解压 FLOPs 降低约 30%。
- **批推理加速**：缓存压缩使批次大小扩大约 4 倍，总解码延迟最高降低 54%；融合解压-注意力核在批量推理中最高实现 **2.4 倍** 加速。
- **兼容性**：可与 4-bit 量化、令牌淘汰等方法叠加，缓存再缩小 5 倍，推理提速 2 倍。

方法在 LLaVA1.5、QwenVL、VideoLLaVA 等多个模型及图像/视频问答基准上验证有效，代码已开源。需注意，单条推理时解压引入的延迟可达约 30%，在低并发场景下可能反而增加时延；此外，压缩秩和重压缩周期仍需手动设定。



大规模视觉语言模型（Large Vision-Language Models, LVLMs）在图像理解、视频问答等多模态任务中展现了卓越能力，但其推理部署面临严峻的显存瓶颈。核心矛盾在于：模型在自回归解码过程中需存储所有历史令牌的键值对（KV cache），以支持缩放点积注意力计算。对于视觉语言模型而言，视觉编码器通常将每张图像转换为数百甚至上千个视觉令牌（如LLaVA系列每张图像产生576个视觉令牌），导致KV缓存的体积急剧膨胀。以LLaVA1.5-7B为例，其KV缓存中视觉令牌占比可超过90%，严重制约了批处理大小和可支持的上下文长度。

现有缓解方案主要沿三条技术路线展开，但均存在结构性缺陷：

**令牌淘汰策略**（如**FastV**、**ScissorHands**、**H2O**）通过注意力分数识别并丢弃“不重要”的令牌以缩减序列长度。此类方法在丢弃令牌的同时永久失去对应信息，且不释放已分配的内存空间——被淘汰令牌的KV缓存仍占据显存，实际内存占用并未降低。

**KV缓存量化**（如**KVQuant**）将键值向量压缩至低比特表示（如4-bit），以乘积方式缩小每令牌存储体积。然而，量化引入的精度损失在视觉令牌上尤为敏感，且压缩比受限于比特宽度，难以实现数量级的内存缩减。

**沿深度维度的压缩**（如**Minicache**）在Transformer层间进行缓存压缩，但未触及每令牌存储体积这一根本瓶颈。

上述方法的共同盲点是忽略了视觉令牌键值向量的内在低秩特性。观察表明，视觉令牌通常携带高度冗余的空间信息，其键值矩阵的有效秩远低于显式的特征维度（注意力头数 × 每头维度）。若能系统性地利用这一低秩结构进行有损压缩，有望在几乎不损害模型输出质量的前提下，将缓存体积缩小数倍——这正是AttentionPack方法的核心动机。

具体而言，本文致力于回答以下关键问题：

1. **压缩粒度**：沿注意力头维度合并后进行奇异值分解（SVD），是否比独立压缩每个注意力头更有效？
2. **压缩-解压权衡**：如何设计解压策略，使得压缩带来的内存收益不被解压延迟所抵消？
3. **跨模态泛化**：低秩压缩假设在视觉令牌上成立，在文本令牌和超长上下文场景下是否仍然有效？

论文提出的**AttentionPack**方法通过三项关键设计回应上述问题：（1）多注意力头联合SVD压缩，将视觉令牌的键值缓存压缩至低秩表示；（2）基于累计注意力分数的部分解压缩机制，仅对高重要性令牌使用全秩解压；（3）融合解压-注意力计算核，将解压操作与注意力分数计算合并为单一算子以降低延迟。实验表明，该方法可在LLaVA1.5-7B上将缓存缩小5.09倍，同时A-OKVQA准确率从76.64%提升至76.88%；在VideoLLaVA-7B上缓存缩小8.11倍，MSVD-QA准确率仅比最佳非压缩基线低0.39%。



## 核心方法与创新机理

AttentionPack 的核心创新在于**将视觉令牌 KV 缓存的低秩压缩与注意力感知的差异化解压相结合**，形成一条从“压缩什么”到“如何解压”的完整优化链路。其关键设计可从三个 changed slots 展开。

### 多注意力头联合低秩压缩：从独立头到跨头共享

传统 KV 缓存压缩通常按单个注意力头独立处理（如逐头量化或逐头淘汰），或完全不分头直接压缩。AttentionPack 的基线值 `Full KV Caching` 即为每令牌存储完整的 $K, V \in \mathbb{R}^{T \times HD}$ 矩阵。

AttentionPack 提出的替代方案是**先沿注意力头轴合并，再执行低秩 SVD**。具体而言，将视觉令牌的键矩阵沿头维度合并为 $T_v \times HD$ 的矩阵后，通过随机化 SVD 分解为：

$$ \mathbf{K}_v \approx \overline{\mathbf{K}}_v \mathbf{D}_{kv}, \quad \overline{\mathbf{K}}_v \in \mathbb{R}^{T_v \times R_{kv}}, \; \mathbf{D}_{kv} \in \mathbb{R}^{R_{kv} \times HD} $$

值矩阵同理。推理时仅保存压缩后的低秩缓存 $\overline{\mathbf{K}}_v$、$\overline{\mathbf{V}}_v$ 和解压缩矩阵 $\mathbf{D}_{kv}$、$\mathbf{D}_{vv}$，而非完整的 $HD$ 维向量。

这一设计的理论依据在于：视觉令牌通常携带大量冗余信息，其键值向量的内在秩远低于显式的特征维度。论文通过方差解释比分析（Figure 2）验证了合并头后再压缩相比不合并头能更有效地捕获方差，同等秩下解释力更强。消融实验进一步表明，多注意力头联合压缩在同等缓存缩小比下，性能比独立头压缩高出 **1.8%**。

压缩粒度上，AttentionPack 对视觉令牌与文本令牌**分别执行 SVD**，避免跨模态信息混合导致次优压缩。这一分离策略是保证压缩质量的关键工程决策。

### 注意力感知的部分解压：从均匀解压到差异化分配

压缩后的缓存需要在使用前解压，直接全秩解压会引入显著的计算开销。AttentionPack 的创新在于**利用历史注意力分数指导解压秩的分配**：高重要性令牌以全秩解压，低重要性令牌以降秩解压。

具体机制为：维护每个令牌的累计注意力分数 $\mathcal{T}_{t_p}$，通过移动平均更新：

$$ \mathcal{T}_{t_p} \gets \alpha^{T_q} \mathcal{T}_{t_p} + (1 - \alpha^{T_q}) \frac{\sum_{t'=t-T_q}^{t} A_{t' t_p}}{T_q} $$

解码时，按分数将视觉令牌分组（默认 $F=2$ 组），前 $r_1$ 比例的高分令牌以原始压缩秩 $R_{vv}$ 解压，其余以 $R_{vv}/4$ 解压。实验表明，**仅对前 25% 重要视觉令牌以全秩解压值缓存，精度几乎不变，解压 FLOPs 降低约 30%**（Figure 4）。

这一设计的直觉在于：与问题相关的视觉区域（如 OCR 任务中的文字区域）天然获得更高的注意力分数，值得完整解压；而背景或无关区域以低秩近似即可。Figure 7 和 Figure 8 的可视化验证了分数分布与语义相关性的对应关系。

### 周期性重压缩与融合算子：工程实现的完整性

除上述核心算法设计外，AttentionPack 还引入了两个支撑性创新：

- **周期性重压缩**：解码过程中新生成的令牌暂存于未压缩缓存，当累积数量超过阈值 $T_p$ 时触发新一轮 SVD 压缩。这避免了每次解码步都执行 SVD 的开销，同时保持缓存的持续压缩状态。

- **融合解压-注意力核**：将解压缩矩阵乘法与注意力分数计算合并为单一 CUDA 算子，消除中间结果的显存读写。在批量推理中，该融合核可将解码延迟降低近一半，最高实现 **2.4 倍加速**（Figure 6）。

### 与同类方法的本质差异

AttentionPack 与现有 KV 缓存优化方法存在根本性区别：

- **FastV** 和 **ScissorHands** 通过淘汰令牌来减少计算量，但**不释放缓存内存**，内存瓶颈未解决。
- **H2O** 基于累计注意力的滑动窗口淘汰，同样不改变每令牌的存储体积。
- **KVQuant** 通过量化降低每元素的位宽，与 AttentionPack 的低秩压缩正交——论文 Table 4 表明二者可叠加使用，缓存再缩小 5 倍。
- **Minicache** 沿深度维度压缩，而 AttentionPack 沿隐藏维度压缩，二者压缩轴不同。

AttentionPack 的独特之处在于：通过**缩小每令牌的存储体积**而非淘汰令牌来降低内存占用，同时以注意力感知解压抵消精度损失。这一策略使缓存缩小 **5–8 倍**的同时，在 A-OKVQA 上准确率甚至略高于全缓存基线（76.88% vs 76.64%），体现了压缩的正则化效应。



AttentionPack 的推理工作流围绕“压缩—选择性解压—注意力计算—周期性重压缩”这一闭环构建，其核心目标是在不损害模型输出质量的前提下，将视觉令牌的键值缓存体积缩小数倍。整个 pipeline 由以下模块串联而成，各模块的输入输出关系在 Figure 1 中以示意图形式呈现。

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/001_Figure_1.jpg]]
*Figure 1: The schematic of the workflow during inference. After the prefill phase, at each decoding step, we first compress the cache along combined heads. We perform attention-aware partial decompression before attention score computation*

**Prefill 阶段**：输入图像和文本首先经过视觉编码器与投影层，生成视觉令牌的隐藏表示 $\mathbf{H_v} = \mathbf{W}_p \mathbf{X_v}$，随后与文本令牌一同送入大语言模型，完成前向传播后产生完整的、未压缩的 KV 缓存 $\mathcal{C} = \{ \mathbf{K}, \mathbf{V} \in \mathbb{R}^{T \times HD} \}$。此阶段不涉及任何压缩操作，为后续步骤提供原始缓存基准。

**多头联合压缩（SVD）**：在首个解码步或当未压缩令牌累积超过阈值 $T_p$ 时，系统对视觉令牌的键和值矩阵分别执行压缩。与常规做法不同，AttentionPack 先将所有注意力头的向量沿头维度合并为 $HD$ 维的单一表示，再应用随机化 SVD 进行低秩分解：
$$
\mathbf{K}_v \approx \overline{\mathbf{K}}_v \mathbf{D}_{kv}, \quad \overline{\mathbf{K}}_v \in \mathbb{R}^{T_v \times R_{kv}}, \; \mathbf{D}_{kv} \in \mathbb{R}^{R_{kv} \times HD}
$$
$$
\mathbf{V}_v \approx \overline{\mathbf{V}}_v \mathbf{D}_{vv}, \quad \overline{\mathbf{V}}_v \in \mathbb{R}^{T_v \times R_{vv}}, \; \mathbf{D}_{vv} \in \mathbb{R}^{R_{vv} \times HD}
$$
压缩后仅保留低秩缓存 $\overline{\mathbf{K}}_v$、$\overline{\mathbf{V}}_v$ 和解压缩矩阵 $\mathbf{D}_{kv}$、$\mathbf{D}_{vv}$，原始完整缓存被释放。压缩秩 $R_{kv}$、$R_{vv}$ 远小于 $\min(T_v, HD)$，通常取 64 或 128。视觉令牌与文本令牌的 SVD 分别独立执行，避免跨模态信息混合导致压缩效率下降。这一设计的关键瓶颈在于：SVD 本身的计算开销在极长序列时不可忽略，论文通过随机化 SVD 有所缓解，但仍缺乏增量压缩策略。

**注意力感知部分解压**：在每个解码步，系统根据历史累计注意力分数对已压缩的视觉令牌进行分组解压。具体而言，式 (1) 以移动平均方式追踪每个令牌的重要性：
$$
\mathcal{T}_{t_p} \gets \alpha^{T_q} \mathcal{T}_{t_p} + (1 - \alpha^{T_q}) \frac{\sum_{t'=t-T_q}^{t} A_{t' t_p}}{T_q}
$$
累计分数高的令牌（通常与当前问题语义紧密相关的图像区域）以原始压缩秩全秩解压，分数低的令牌则以降秩（如 $R/4$）解压，从而在保证关键信息精度的同时大幅降低解压 FLOPs。解压后的键值矩阵与未压缩的新生成令牌拼接，形成完整的 $\tilde{\mathbf{K}}$、$\tilde{\mathbf{V}}$ 供注意力计算使用。

**注意力计算与重要性更新**：在解压后的键值对上执行标准缩放点积注意力：
$$
\mathbf{A} \gets \mathsf{softmax}\left(\frac{\mathbf{Q} \tilde{\mathbf{K}}^T}{\sqrt{D}}\right), \quad \mathbf{O} \gets (\mathbf{A} \tilde{\mathbf{V}}) \mathbf{W}_o
$$
每次注意力计算后，系统按式 (1) 更新各令牌的累计分数，为下一步的解压决策提供依据。这一闭环使得解压策略能够动态适应生成过程中注意力分布的变化。

**周期性重压缩**：随着解码进行，未压缩的新令牌不断累积。当数量超过预设阈值 $T_p$ 时，系统重新执行 SVD 压缩，将新令牌纳入低秩缓存并清空未压缩缓冲区。该机制避免了缓存体积的持续膨胀，但也引入了周期性的 SVD 计算开销。

**融合解压‑注意力核（可选）**：为进一步降低延迟，AttentionPack 提供了将解压矩阵乘法与注意力分数计算合并的融合 CUDA 核实现。在批量推理场景下，该融合核可将解码延迟降低近一半，最高实现 2.4 倍加速（Figure 6），但依赖自定义算子，可能与某些注意力实现存在兼容性问题。

整体而言，AttentionPack 通过“多头联合低秩压缩 + 注意力感知选择性解压”的双重机制，在缓存体积缩小约 5–8 倍的同时，将模型性能保持在 Full KV Caching 基线水平附近。其因果链条可概括为：视觉令牌 KV 向量的内在低秩特性 → 多头合并后 SVD 高效压缩 → 注意力分数指导差异化解压 → 关键信息无损、冗余信息降秩 → 缓存体积锐减、批量推理吞吐提升。该框架的主要局限在于单条推理时解压延迟可达 30%，且压缩周期和秩的选择依赖经验设定，缺乏自适应策略。



### 视觉特征提取与投影

LVLM 推理的第一步是将视觉输入转换为与文本嵌入对齐的表示。给定输入图像 $\mathbf{X_v}$，预训练视觉编码器 $g(\cdot)$ 提取特征：

$$\mathbf{Z_v} = g(\mathbf{X_v}) \in \mathbb{R}^{T_v \times D_v}$$

随后通过线性投影矩阵 $\mathbf{W}_p$ 将视觉特征映射到语言模型的嵌入空间：

$$\mathbf{H_v} = \mathbf{W}_p \mathbf{X_v}$$

经过投影后，视觉令牌与文本令牌拼接，共同进入 Transformer 层。在自回归解码过程中，每层生成的键值对被存储为 KV 缓存：

$$\mathcal{C} = \{ \mathbf{K}, \mathbf{V} \in \mathbb{R}^{T \times HD} \}$$

其中 $T = T_v + T_t$ 为视觉令牌数与文本令牌数之和，$H$ 为注意力头数，$D$ 为每头维度。对于视觉令牌密集的场景（如多帧视频），$T_v$ 可高达数千，使得 $\mathcal{C}$ 成为显存瓶颈的核心来源。

### 多头联合低秩压缩（核心模块一）

AttentionPack 的核心洞察是：视觉令牌的键值向量在跨注意力头合并后呈现显著的低秩特性（Figure 2 验证了合并头轴后解释方差比大幅提升）。基于此，方法对视觉令牌的键矩阵和值矩阵分别执行随机化 SVD 分解。

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/002_Figure_2.jpg]]
*Figure 2: Rank vs explained variance ratio without/with combining along head axis before compression for key and value vectors*

**压缩过程**：先将所有注意力头的键向量沿头轴合并为 $T_v \times HD$ 矩阵，再分解为低秩形式：

$$\mathbf{K}_v \approx \overline{\mathbf{K}}_v \mathbf{D}_{kv}, \quad \overline{\mathbf{K}}_v \in \mathbb{R}^{T_v \times R_{kv}}, \; \mathbf{D}_{kv} \in \mathbb{R}^{R_{kv} \times HD}$$

$$\mathbf{V}_v \approx \overline{\mathbf{V}}_v \mathbf{D}_{vv}, \quad \overline{\mathbf{V}}_v \in \mathbb{R}^{T_v \times R_{vv}}, \; \mathbf{D}_{vv} \in \mathbb{R}^{R_{vv} \times HD}$$

其中 $R_{kv}, R_{vv} \ll \min(T_v, HD)$ 为压缩秩。推理时仅保存压缩后的低秩缓存 $\overline{\mathbf{K}}_v, \overline{\mathbf{V}}_v$ 和解压缩矩阵 $\mathbf{D}_{kv}, \mathbf{D}_{vv}$。键缓存的理论压缩比为：

$$c_{kv} = \frac{T_v HD}{T_v R_{kv} + R_{kv} HD}$$

该设计的三个关键决策：(1) **多头联合压缩**——合并头轴后再做 SVD，相比独立头压缩在同等缓存缩小比下性能高 1.8%；(2) **视觉与文本令牌分离处理**——跨模态混合压缩会导致次优结果，因此对两类令牌分别执行 SVD；(3) **随机化 SVD**——缓解长序列下完整 SVD 的计算开销。

### 注意力感知部分解压缩（核心模块二）

全秩解压缩会引入不可忽略的延迟（单条推理可达 30%）。AttentionPack 的解决方案是利用历史注意力分数区分令牌重要性，对高重要性令牌以全秩解压，低重要性令牌以降秩解压。

**令牌重要性追踪**：每个视觉令牌 $t_p$ 维护累计注意力分数 $\mathcal{T}_{t_p}$，通过指数移动平均更新：

$$\mathcal{T}_{t_p} \gets \alpha^{T_q} \mathcal{T}_{t_p} + (1 - \alpha^{T_q}) \frac{\sum_{t'=t-T_q}^{t} A_{t' t_p}}{T_q}$$

其中 $A_{t' t_p}$ 为第 $t'$ 步时令牌 $t_p$ 的注意力分数，$T_q$ 为滑动窗口大小，$\alpha \in [0,1]$ 控制衰减速率（论文设定 $\alpha = 0.25$）。

**分组解压**：将视觉令牌按 $\mathcal{T}_{t_p}$ 排序后分为 $F$ 组（默认 $F=2$），前 $r_1$ 比例的令牌以全秩 $R_{kv}$ 解压，剩余 $r_2 = 1 - r_1$ 的令牌以降秩 $R_{kv}/4$ 解压。解压后的键矩阵拼接新生成的未压缩令牌：

$$\tilde{\mathbf{K}} \gets \bigoplus_{f=1}^{F} \overline{\mathbf{K}}[m_f, :R_k^{(f)}] \mathbf{D}_k[:R_k^{(f)}] \oplus \mathbf{K}$$

其中 $m_f$ 为第 $f$ 组的令牌索引，$R_k^{(f)}$ 为对应解压秩。实验表明，仅对前 25% 重要视觉令牌以全秩解压值缓存，即可达到与全解压几乎相同的精度，同时解压 FLOPs 降低约 30%。

### 注意力计算与周期性重压缩

解压完成后，执行标准缩放点积注意力：

$$\mathbf{A} \gets \mathsf{softmax}\left(\frac{\mathbf{Q} \tilde{\mathbf{K}}^T}{\sqrt{D}}\right)$$

$$\mathbf{O} \gets (\mathbf{A} \tilde{\mathbf{V}}) \mathbf{W}_o$$

当未压缩的新令牌数量超过阈值 $T_p$ 时，触发周期性重压缩：对当前全部缓存重新执行 SVD，清空未压缩缓存。这一机制平衡了压缩频率与内存占用。

### 融合解压-注意力核（可选优化）

为进一步降低延迟，AttentionPack 实现了融合 CUDA 核，将解压缩矩阵乘法 $\overline{\mathbf{K}} \mathbf{D}_k$ 与注意力分数计算 $\mathbf{Q} \tilde{\mathbf{K}}^T$ 合并为单一算子。在批量推理中，该融合核可将解码延迟降低近一半，最高实现 2.4 倍加速。

### 补充图表

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of compression and partial decompression*



## 实验与关键发现

### 核心实验设置

AttentionPack 在图像问答和视频问答两类任务上进行了系统评估。图像任务采用 **LLaVA1.5-7B**、**LLaVA1.5-13B** 和 **QwenVL-Chat-7B** 三个模型，在 A-OKVQA、OCR-VQA 和 MMMU 三个基准上测试；视频任务采用 **VideoLLaVA-7B**，在 MSVD-QA 和 MSRVTT-QA 上评估。压缩秩默认设为 $R_{kv}=R_{vv}=64$（LLaVA 系列）或 $R_{kv}=R_{vv}=128$（VideoLLaVA），注意力感知解压采用 $F=2$ 组，其中前 $r_1=0.25$ 比例的重要令牌以全秩解压，其余以 $R/4$ 降秩解压，衰减因子 $\alpha=0.25$。

对比基线涵盖四类主流 KV 缓存优化策略：令牌淘汰方法 **ScissorHands** 和 **H2O** 、视觉令牌跳跃方法 **FastV** 、深度维度压缩 **Minicache** 、以及量化方法 **KVQuant - 4bit**。所有方法均在相同硬件环境下测量缓存内存占用量和吞吐量变化。

### 主实验结果

**图像问答任务。** 在 LLaVA1.5-7B 上，AttentionPack 以 $R=64$ 的压缩秩将平均每实例缓存缩小 **5.09 倍**，同时 A-OKVQA 准确率从 76.64% 提升至 **76.88%**（+0.24%），OCR-VQA 的 ROUGE-L 从 51.05 提升至 **52.44**（+1.39），MMMU 准确率仅下降 0.09%（34.68% → 34.59%）。在更大的 LLaVA1.5-13B 上，缓存缩小 **5.17 倍**，性能保持同等水平。QwenVL-Chat-7B 上 MMMU 准确率仅下降 0.10%（35.82% → 35.72%），验证了方法跨模型架构的泛化性。

与令牌淘汰基线相比，ScissorHands 和 H2O 虽然也减小了缓存，但在 A-OKVQA 上分别有 0.5%–1.2% 的性能损失，且缓存缩小幅度远不及 AttentionPack。FastV 通过跳跃视觉令牌减少计算量，但不释放缓存内存，因此缓存大小与全量缓存相同。Minicache 沿深度维度压缩，在同等缓存缩小比下性能损失更显著。KVQuant 的 4‑bit 量化可与 AttentionPack 正交叠加，但单独使用时缓存缩小比有限。

**视频问答任务。** VideoLLaVA-7B 处理多帧视频输入时视觉令牌数量激增，缓存压力更大。AttentionPack 以 $R=128$ 将缓存缩小 **8.11 倍**，MSVD-QA 准确率为 69.21%，仅比最佳非压缩方法 FastV（69.60%）低 0.39%；MSRVTT-QA 准确率为 55.47%，比全量缓存的 55.60% 仅低 0.13%。相比之下，H2O 的令牌淘汰在视频场景下性能下降更为明显（MSVD-QA 上约 2% 的损失），说明低秩压缩比直接丢弃令牌更有利于保留视觉信息。

### 压缩秩消融分析

Table 3 报告了 LLaVA1.5-7B 上不同压缩秩的系统消融。当 $R_{kv}=R_{vv}$ 从 16 线性增加到 128 时，A-OKVQA 和 OCR-VQA 的性能分别提升 0.38% 和 0.36%。秩低于 64 时性能开始明显下降，秩高于 128 时收益趋于饱和。秩 64 在约 **5 倍缓存缩小**下实现了性能与效率的最佳平衡——此时缓存大小仅约为全量缓存的 19.6%，而准确率几乎无损甚至略有提升（A-OKVQA +0.24%）。

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/006_Table_3.jpg]]
*Table 3: Performance and cache size for various compression rank values using LLaVA1.5-7B for batch size of 32*

这一反直觉的“压缩后性能提升”现象可能源于低秩分解的隐式正则化效应：SVD 截断过滤了视觉令牌中的高频噪声成分，使注意力计算更聚焦于语义相关信息。Figure 2 的秩-解释方差分析为此提供了佐证：沿头轴合并后，前 64 个奇异值即可解释键向量 90% 以上的方差，说明视觉令牌的键值向量确实具有显著的低秩结构。

### 注意力感知解压的有效性

注意力感知部分解压是 AttentionPack 控制解压延迟的关键设计。Figure 4 展示了不同解压策略对性能和 FLOPs 的影响。核心发现是：**仅对前 25% 重要视觉令牌以全秩解压值缓存**，即可达到与全解压几乎相同的精度，同时解压 FLOPs 降低约 30%。具体而言，当 $r_1=0.25$（即 25% 令牌全秩解压，75% 令牌以 $R/4$ 降秩解压）时，A-OKVQA 准确率与 $r_1=1.0$（全解压）相差不到 0.1%，但解压计算量显著减少。

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/007_Figure_4.jpg]]
*Figure 4: Impact of attention-aware decompression. Each line represents the results when AttentionPack is applied for key (k), value (v) caches or both (kv). Every line has four dots with the size of each representing the ratio of visual tokens*

Figure 7 和 Figure 8 可视化了式 (1) 追踪的令牌重要性分数。在 MSVD-QA 视频问答中，与问题语义相关的视觉令牌（如包含人物、动作对象的区域）获得更高的重要性分数，在解压时被分配更高秩；背景或无关区域则以降秩解压。在 OCR-VQA 图像问答中，包含文字区域的令牌重要性分数明显高于纯背景区域，验证了注意力感知机制的语义合理性。

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/013_Figure_7.jpg]]
*Figure 7: Visualization of scores (Eq. 1) at the first decoding step after processing the question on various examples from MSVD-QA, showing that the visual tokens closely related to the prompt have higher importance scores and will be decompressed with higher ranks*

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/014_Figure_8.jpg]]
*Figure 8: Visualization of tracked attention-score statistics (Eq. 1) on various image QA pairs from OCR-VQA and A-OKVQA*

### 批推理延迟与吞吐量

缓存压缩的核心收益在于提升批处理能力。Figure 5 展示了 LLaVA1.5-7B 处理 100 个查询的总解码延迟。由于每实例缓存缩小约 80%，批次大小可扩大约 **4 倍**，总解码延迟最多降低 **54%**（OCR-VQA 场景）。在 A-OKVQA 上延迟降低约 45%，MMMU 上降低约 35%。延迟降低幅度的差异与任务的平均生成长度相关：生成长度越长，解码步数越多，缓存压缩带来的累积收益越大。

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/012_Figure_5.jpg]]
*Figure 5: Total decode latency for 100 queries with LLaVA1.5-7B*

Table 4 进一步展示了 AttentionPack 与 4‑bit 量化和令牌淘汰的联合效果。叠加 KVQuant 的 4‑bit 量化后，缓存可再缩小约 5 倍，批推理吞吐量提升约 **2 倍**。然而，引入令牌淘汰在 OCR-VQA 上会带来约 0.5% 的额外性能下降，说明低秩压缩与令牌淘汰的信息损失机制存在部分重叠，联合使用时需谨慎调参。

### 融合核加速

Figure 6 对比了标准注意力实现与融合解压‑注意力核在不同批大小和序列长度下的解码延迟。融合核将解压矩阵乘法与注意力分数计算合并为单一 CUDA 算子，避免了解压结果的显式物化和内存往返。对于 32 令牌的解码，融合核可将延迟降低近一半，最高实现 **2.4 倍**推理加速。加速比随批大小增大而提升，因为大 batch 下解压操作的计算密度更高，融合带来的内存带宽节省更显著。

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/011_Figure_6.jpg]]
*Figure 6: Decoding latency for 32 tokens with various batch sizes and sequence lengths using standard attention and with fused kernel implementation of AttentionPack. We observe up to 2.4x faster inference in single and batch query settings*

### 文本域扩展与局限性

Table 6 报告了在纯文本任务（LongBench 数据集，LLaMA3.1-8B）上的初步结果。AttentionPack 在文本摘要和问答任务上也能实现一定的缓存压缩，但需要手动设置较低的压缩秩以避免性能损失。这表明当前方法的压缩策略主要针对视觉令牌优化，文本令牌的低秩假设不如视觉令牌强——文本令牌的语义信息更密集，过度压缩容易丢失关键上下文。此外，单条推理时解压引入的延迟可达 30%，在小批次或无并行场景下反而增加时延，这是该方法在实时交互场景中面临的主要限制。

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/015_Table_6.jpg]]
*Table 6: Text QA and summarization results on LongBench datasets with LLaMA3.1-8B*

### 失败模式与待验证问题

以下几点需特别注意或需进一步验证：

1. **单条推理延迟增加**：解压操作在 batch size=1 时无法被计算密集型操作掩盖，导致端到端延迟上升约 30%。对于低延迟要求的实时应用，需评估融合核的实际收益是否足以抵消这一开销。

2. **压缩秩的自动化选择**：当前 $R$ 和重压缩周期 $T_p$ 依赖离线网格搜索，缺乏自适应机制。不同层、不同任务的最优秩可能存在显著差异，静态设置可能导致某些场景下过度压缩或压缩不足。

3. **超长上下文下的低秩假设**：评测集中在常规长度的视觉问答（视觉令牌数通常 < 3000），在 >100K tokens 的超长上下文场景中，低秩假设是否仍然成立需要独立验证。

4. **生成式对话与多轮交互**：当前评测集中于单轮问答，尚未在开放式生成、多轮对话等场景中验证压缩对生成质量和一致性的影响。

5. **SVD 的计算开销**：虽然采用随机化 SVD 缓解了分解成本，但在极长序列（如小时级视频）下，每次重压缩的 SVD 开销可能不可忽略。增量 SVD 更新策略是潜在的改进方向。

### 补充图表

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/004_Table_1.jpg]]
*Table 1: Image QA results on AOKV-QA, OCRKV-QA and MMMU with LLaVA1.5-7B, LLaVA1.5-13B and QwenVL-Chat-7B. We report evaluation metrics along with cache memory and throughput statistics for full KV caching, ScissorHands [21], H2O [32], FastV [5], Minicache [19] to compare with AttentionPack*

![[assets/figures/papers/paper_list_l738_https_arxiv_org_abs_2603_23914/figures/005_Table_2.jpg]]
*Table 2: Video QA results on MSVD-QA and MSRVTT-QA with VideoLLaVA-7B. We report evaluation metrics along with cache memory and throughput statistics for full KV caching, H2O eviction, FastV to compare with our approach AttentionPack*



## 定位与知识库关联

### 核心思路：从令牌淘汰到低秩压缩

现有视觉语言大模型（VLM）推理加速方法主要沿两条路径展开：**令牌淘汰**与**缓存量化**。令牌淘汰类方法通过注意力分数识别并丢弃“不重要”的视觉令牌，典型代表包括 **FastV**（视觉令牌跳跃）、**ScissorHands**（基于注意力的令牌淘汰）和 **H2O**（基于累计注意力的滑动窗口淘汰）。这类方法不改变缓存结构，仅减少参与计算的令牌数量，因此**不释放KV缓存内存**，在批推理场景下显存瓶颈依然存在。缓存量化方法如 **KVQuant**（4‑bit量化），通过降低每元素的位宽来压缩存储，但量化误差可能累积，且与低秩压缩存在正交的互补空间。

AttentionPack 的方法学定位在于**改变KV缓存的表示形式本身**：它利用视觉令牌键值向量的内在低秩特性，沿注意力头维度合并后执行奇异值分解（SVD），将缓存压缩为低秩矩阵与解压缩矩阵的乘积。这一思路与 **Minicache**（沿深度维度的KV缓存压缩）同属“缓存表示压缩”家族，但 AttentionPack 的独特贡献在于：(1) 多注意力头联合压缩，而非逐头独立处理；(2) 视觉与文本令牌分别执行SVD，避免跨模态信息混合导致的次优压缩；(3) 引入注意力感知的部分解压缩机制，以抵消解压带来的延迟开销。

### 与其他方法的正交性与组合潜力

AttentionPack 与令牌淘汰、缓存量化存在天然的**正交互补性**。论文实验表明，将 AttentionPack 与4‑bit量化（KVQuant）及令牌淘汰结合后，缓存可在原有基础上再缩小约5倍，推理吞吐量提升约2倍。这种组合策略的代价是OCR‑VQA上约0.5%的性能下降，说明不同压缩机制的误差存在累积效应，需要在具体应用场景中权衡。

从方法谱系上看，AttentionPack 填补了“结构化低秩压缩”在VLM推理优化中的空白。此前低秩分解多用于模型权重压缩（如LoRA系列）或训练加速，而将其系统性地应用于KV缓存、并配合注意力感知的解压策略，是该工作的核心知识增量。

### 适用边界与局限

**适用场景**：AttentionPack 在视觉令牌占比较高的任务中收益最大，如图像问答（LLaVA1.5‑7B上缓存缩小5.09倍）、视频问答（VideoLLaVA‑7B上缓存缩小8.11倍）。批推理场景下，缓存压缩使单实例显存占用降低约80%，批次大小可扩大约4倍，总解码延迟最高降低54%。

**已知局限**：
1. **单条推理延迟增加**：解压操作在无并行或小批次场景下引入约30%的额外延迟，此时压缩反而降低吞吐量。
2. **文本令牌压缩未充分优化**：当前方法对视觉令牌压缩占主导，文本令牌压缩需手动设定较低秩，且纯文本任务（如LongBench）上的效果有限（见Table 6）。
3. **超参数依赖经验选择**：压缩秩R、压缩周期T_p、注意力感知分组比例r_1等关键参数缺乏自动化策略，依赖离线网格搜索。
4. **SVD计算开销**：尽管采用随机化SVD缓解，在极长序列（>10K tokens）下周期性重压缩的计算成本仍不可忽略。
5. **融合核算子兼容性**：融合解压‑注意力核依赖自定义CUDA实现，可能与某些注意力变体（如FlashAttention特定版本）存在兼容性问题。
6. **评估任务覆盖有限**：评测集中于问答基准（A-OKVQA、OCR‑VQA、MMMU、MSVD‑QA等），尚未在开放式生成对话或复杂多轮交互中验证压缩对生成质量的影响。

### 开放问题与后续方向

1. **自适应秩分配**：能否根据层的重要性动态分配压缩秩？浅层和深层的注意力模式差异显著，统一秩可能不是最优解。
2. **增量压缩**：当前每次达到阈值T_p时需对全缓存重新执行SVD。能否设计增量更新机制，仅处理新增令牌，避免重复分解？
3. **学习型重要性预测**：注意力感知解压目前依赖启发式累计注意力分数（式1）。能否训练轻量预测器替代该分数，实现更精准的令牌重要性估计？
4. **超长上下文泛化**：在>100K tokens的场景下，低秩假设是否仍然成立？压缩比能否继续提升，还是会出现秩瓶颈？
5. **安全性与公平性影响**：论文未涉及压缩对模型偏见或安全性的分析。低秩近似是否会放大某些模态或群体的表征误差，需要进一步研究。
6. **训练‑压缩联合优化**：能否通过微调使模型适应低秩表示？类似LoRA的思路，将压缩矩阵作为可训练参数，可能进一步提升压缩比下的性能保持。

### 知识库定位总结

AttentionPack 属于 **VLM推理效率优化** 方向中的 **KV缓存结构化压缩** 子领域。与令牌淘汰（FastV、H2O、ScissorHands）和缓存量化（KVQuant）形成互补三角，共同构成当前VLM推理优化的方法矩阵。其核心知识贡献在于验证了“多注意力头联合低秩分解 + 注意力感知部分解压”这一技术路线的有效性，为后续的自适应压缩、增量压缩和训练‑压缩联合优化提供了基准。代码已开源（[AttentionPack](https://github.com/gitdisl/AttentionPack)），为社区复现与改进提供了基础。



## 原文 PDF

![[paperPDFs/CVPR_2026/Attention_aware_Inference_Optimizations_for_Large_Vision_Language_Models_with_Memory_efficient_Decoding.pdf]]
