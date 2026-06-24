---
title: Toward Early Quality Assessment of Text-to-Image Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Toward_Early_Quality_Assessment_of_Text_to_Image_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/Guhuary/ProbeSelect"
aliases:
- PS
- TEQATIDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 去噪网络中间层的激活特征（如 U-Net 或 DiT 的某层输出）在生成早期（约 20% 进度）就已包含稳定的粗结构信息（物体布局、空间构成），这些信息与最终图像质量强相关，因此可以作为早期预测质量的直接信号。
primary_logic: 通过训练一个轻量级探针（probe）读取去噪网络中期激活并借助列表排序损失和文本对齐损失预测最终质量分数，可以在生成早期（如 20% 步数）准确排名候选种子，从而仅继续推进高质量候选项，大幅节省计算开销，而无需修改生成模型本身。
claims:
- 早期评估在 20% 轨迹时已能准确排列候选种子，采样成本降低超过 60%。
- 在 t=0.2 时，SD2 的 PickScore Spearman 相关性为 0.79，ImageReward 相关性高达 0.99，并随时间保持稳定。
- SD2 使用 Probe-Select 根据 ImageReward 选择后，ImageReward 得分从 0.49 升至 1.59，HPSv2.1 从 26.95 升至 29.03。
- 跨骨架迁移实验表明探针具有良好泛化性：SD2 训练探针应用于 SD3-M 相关性达 0.96。
---

# Toward Early Quality Assessment of Text-to-Image Diffusion Models

> [!tip] 核心洞察
> 通过训练一个轻量级探针（probe）读取去噪网络中期激活并借助列表排序损失和文本对齐损失预测最终质量分数，可以在生成早期（如 20% 步数）准确排名候选种子，从而仅继续推进高质量候选项，大幅节省计算开销，而无需修改生成模型本身。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向文本到图像扩散模型的早期质量评估 |
| 英文题名 | Toward Early Quality Assessment of Text-to-Image Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.02829) · [Code](https://github.com/Guhuary/ProbeSelect) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Probe-Select |
| Dataset | MS-COCO, DrawBench |

> [!tip] 效果简介
> - MS-COCO (SD2) 上，ImageReward 1.59 (Probe-Select IR) vs 0.49 (average over 5 seeds) (+1.10)；HPSv2.1 29.03 (Probe-Select IR) vs 26.95 (+2.08)。
> - MS-COCO (SD3-L) 上，ImageReward 1.83 (Probe-Select IR) vs 1.14 (+0.69)；HPSv2.1 31.81 (Probe-Select IR) vs 30.29 (+1.52)。
> - MS-COCO (FLUX.1-dev) 上，ImageReward 1.79 (Probe-Select IR) vs 0.92 (+0.87)。

## 概述

文本到图像扩散模型在创意设计、内容生成等领域得到广泛应用，但标准的“生成-选择”流程存在显著的计算瓶颈：图像质量评估（如 CLIPScore、ImageReward）只能在完整生成图像后进行，导致大量计算资源消耗在最终质量不高的候选样本上。针对这一问题，本文提出 **Probe-Select**，一种即插即用的早期质量评估模块，通过在生成早期（约 20% 总步数）读取去噪网络中间层激活特征来预测最终图像质量，从而提前终止低分候选项，仅继续推进高分种子。

核心发现是：去噪网络（U-Net 或 DiT）的中间层激活在生成早期就已包含稳定的粗结构信息（物体布局、空间构成），这些信息与最终图像质量强相关，且随时间保持稳定（Table 1 显示 SD2 在 t=0.2 时 ImageReward Spearman 相关性高达 0.99）。基于此，Probe-Select 训练一个轻量级探针，结合列表排序损失和对比文本对齐损失，直接从早期激活中预测评估器分数，无需修改生成模型本身。

在 MS-COCO 基准上，Probe-Select 在多个生成骨架（SD2、SD3-L、FLUX.1-dev）上均显著提升图像质量：SD2 的 ImageReward 得分从 0.49 升至 1.59，HPSv2.1 从 26.95 升至 29.03；FLUX.1-dev 的 ImageReward 从 0.92 升至 1.79。同时，采样成本降低超过 60%。跨骨架迁移实验表明探针具有良好的泛化性（SD2 训练探针应用于 SD3-M 相关性达 0.96），大幅降低了部署成本。

## 背景与动机

文本到图像扩散模型在图像生成领域取得了显著进展，但实际部署中普遍采用的“生成-选择”策略面临严重的计算效率瓶颈。该策略的核心流程是：对同一提示生成多个候选图像，然后使用图像质量评估器（如 CLIPScore、ImageReward）对完整生成的图像进行评分，最终选择最高分图像输出。这一流程中，所有候选种子都必须完成完整的去噪过程，导致大量计算资源被消耗在最终质量不高的候选样本上。随着生成模型规模的增长和候选数量 $N$ 的扩大，这种计算浪费变得愈发突出。

解决这一瓶颈的关键洞察在于：扩散模型的去噪过程并非在整个轨迹上均匀地构建图像信息。如图 1 所示，去噪网络中间层的隐藏状态可视化表明，粗粒度的物体布局和空间构成在生成早期（约 20% 进度）就已出现，且后续变化缓慢。这些早期激活特征与最终图像质量之间存在稳定的相关性，构成了早期质量预测的因果信号。

然而，现有方法未能有效利用这一信号。简单地在早期时间步解码出近似图像并直接应用现成评估器的策略，其 Spearman 相关性仅为 0.52（见 Section 8.5），远不足以支撑可靠的候选筛选。这是因为早期解码的图像仍包含大量噪声，而现有评估器是针对完整清晰图像设计的，无法从噪声信号中提取有效的质量判断。因此，需要一种专门设计的机制，能够直接从去噪网络的中间激活中预测最终质量，而非依赖早期解码的模糊图像。

基于上述动机，本文提出了 Probe-Select 方法。其核心思想是：训练一个轻量级探针网络，读取去噪网络在早期时间步（如 20% 总步数）的中间激活特征，直接预测目标评估器对最终图像的质量评分。通过这一早期预测，可以在生成过程中提前终止低分候选种子，仅继续推进高分候选项，从而大幅节省计算开销。该方法无需修改生成模型本身，以即插即用的方式嵌入现有“生成-选择”流程，实现了计算效率与图像质量的双重提升。

## 核心创新

Probe-Select 的核心创新在于将图像质量评估从“生成后”前移至“生成中”，通过读取去噪网络中间激活特征，在仅完成约 20% 去噪轨迹时即可准确预测最终图像质量，从而实现对候选种子的早期筛选与选择性继续生成。这一设计直接改变了标准“生成-选择”流程中的三个关键环节。

### 评估时机的根本性前移

在传统流程中，评估必须在完整生成图像后进行——所有候选种子均需经历完整的去噪过程，然后使用预训练评估器（如 ImageReward、CLIPScore）对最终图像进行评分。这意味着大量计算资源被消耗在最终质量不高的候选样本上，成为计算效率的核心瓶颈。

Probe-Select 将评估时机前移至生成早期（默认 $t=0.2$，即总步数的 20%）。此时去噪网络尚未完成全部迭代，但中间层激活特征已包含稳定的粗结构信息（物体布局、空间构成），这些信息与最终图像质量存在强关联。实验表明，在 $t=0.2$ 时，SD2 的预测分数与 PickScore 的 Spearman 相关性为 0.79，与 ImageReward 的相关性高达 0.99（Table 1），且相关性随时间保持稳定，验证了早期信号的可靠性。

### 评估输入从最终图像转向中间激活

传统评估器直接以最终解码图像 $x_1$ 为输入，而 Probe-Select 的评估输入是去噪网络选定块在早期时间步的中间激活特征 $h_t$。这一转变的关键洞察在于：去噪网络的中间层激活在生成早期就已编码了决定最终图像质量的粗粒度结构信息，无需等待图像完全解码即可进行质量判别。

通过从去噪网络内部“窃听”（feature tap）中间激活，Probe-Select 避免了对生成图像的依赖，也无需修改生成模型本身的参数或架构，实现了完全即插即用的设计。

### 评分模型与训练目标的专用化设计

传统评估器（如 ImageReward）是预训练的通用图像评分模型，直接使用它们需要在生成完成后进行。Probe-Select 则训练一个轻量级探针 $E_{\phi}$ 来预测评估器分数，其训练目标由两部分组成：

- **列表排序损失** $\mathcal{L}_{list}$：基于 softmax 的列表排序损失，传递评估器间的相对偏好排序，促使探针关注区分性结构线索，而非拟合绝对分数值。
- **对比文本对齐损失** $\mathcal{L}_{Align}$：将探针嵌入 $u_t$ 与 CLIP 文本嵌入对齐的 InfoNCE 损失，保持预测的质量分数对文本语义敏感。

消融实验揭示了文本对齐损失的关键作用：移除该损失后，ImageReward 预测相关性从 0.99 骤降至 0.66（Table 7），证明文本感知对早期质量预测至关重要。

### 生成策略从“全量生成”转向“选择性继续”

传统流程对所有候选种子均完成完整去噪，然后取平均分数或选择最佳结果。Probe-Select 则采用选择性采样策略：在 $t=0.2$ 时使用探针对 $N$ 个候选种子进行评分，仅保留预测得分最高的 $K$ 个种子继续完成生成（$K \ll N$），其余低分种子提前终止。

这一策略的计算开销比率近似为：

$$\text{Cost Ratio} \approx \eta + (1 - \eta) \frac{K}{N}$$

其中 $\eta$ 为早期检查点占总步数的比例。当 $t=0.2$（$\eta=0.2$）、$N=5$、$K=1$ 时，计算开销约为完整生成的 36%，即节省超过 60% 的采样成本（Abstract）。

### 跨骨架迁移的泛化能力

Probe-Select 的另一项重要创新在于其跨模型骨架的迁移能力。实验表明，在 SD2 上训练的探针直接应用于 SD3-M 时，Spearman 相关性仍达 0.96；应用于 FLUX.1-dev 时同样为 0.96（Table 5）。这意味着无需为每个新模型重新训练探针，大幅降低了部署成本，进一步强化了其作为通用即插即用模块的定位。

与之形成对比的是，简单的早期解码基线——在 $t=0.2$ 时解码出近似图像并直接用现成评估器评分——Spearman 相关性仅有 0.52，远低于 Probe-Select 的 0.9+（Section 8.5），充分说明早期评估需要专用的探针设计，而非简单地提前解码图像。

## 整体框架

Probe-Select 是一种即插即用的早期质量评估模块，其核心思想是在扩散模型去噪过程的早期阶段（约 20% 总步数）截取中间激活特征，通过一个轻量级探针网络预测最终图像的评估器分数，从而在生成完成前筛选出高质量候选种子，仅对高分候选项继续完成生成，大幅节省计算开销。

### 动机与关键洞察

在标准的“生成-选择”流程中，图像质量评估（如 CLIPScore、ImageReward）必须在完整生成图像后进行，导致大量计算资源消耗在最终质量不高的候选样本上。Probe-Select 的提出基于一个关键观察：去噪网络中间层的激活特征在生成早期就已包含稳定的粗结构信息（物体布局、空间构成），这些信息与最终图像质量强相关。如 Figure 1 所示，在稳定扩散采样器的反过程中，粗布局和物体轮廓在早期即出现且变化缓慢，为早期质量预测提供了可靠信号。

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/001_Figure_1.jpg]]
*Figure 1: Top: Snapshots of the reverse process in stable diffusion sampler from noisy latent to clean image. Middle: Denoiser architecture. Bottom: Visualization of hidden states. It shows that coarse layout and object contours emerge early and change slowly, which correlates with the final image*

### 整体 Pipeline

Probe-Select 的完整流程包含训练和推理两个阶段，其训练流程概览如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Probe-Select training. The model receive the intermediate denoiser activations and the timestep t to produce the final quality. An additional text-aligned InfoNCE loss is employed for meaningful representation learning*

**训练阶段**由以下模块串联构成：

1. **Feature Tap（特征截取）**：从去噪网络选定的中间块中提取激活特征 $h_t$，截取时间点通常为总步数的 20%（即 $t = 0.2$）。

2. **PCA Compression（PCA 压缩）**：沿通道维度对提取的高维特征图应用 PCA 压缩，保留前 48 个主成分，在保持预测性能的同时显著降低 GPU 内存占用。消融实验（Table 10）表明，48 维即可使性能饱和，降至 16 维则 Spearman 相关性下降至 0.84。

3. **Time-Conditioned Encoder（时间条件编码器）**：使用注意力残差下采样块配合时间调制，将压缩后的特征 $h_t$ 编码为紧凑的表示向量 $u_t$。

4. **Text Alignment Module（文本对齐模块）**：通过对比文本对齐损失 $\mathcal{L}_{Align}$ 将探针嵌入 $u_t$ 与 CLIP 文本嵌入对齐，确保预测的质量分数对文本语义敏感。消融实验（Table 7）显示，移除该损失后 ImageReward 预测相关性从 0.99 骤降至 0.66，证明文本感知对质量预测至关重要。

5. **Prediction Head（预测头）**：三层 MLP 加 Sigmoid 激活，将表示向量映射到 $[0, 1]$ 范围内的标量预测分数 $\hat{y}_{t,m}$。

**训练目标**为联合优化列表排序损失 $\mathcal{L}_{list}$ 和对比文本对齐损失 $\mathcal{L}_{Align}$：

$$\mathcal{L} = \mathcal{L}_{list} + \lambda_{Align} \mathcal{L}_{Align}$$

其中 $\mathcal{L}_{list}$ 采用基于 softmax 的列表排序损失，强调评估器间的相对偏好排序而非绝对数值，促使探针关注区分性结构线索；$\mathcal{L}_{Align}$ 为 InfoNCE 形式的对比损失，将探针嵌入与提示文本嵌入对齐。超参数方面，$\lambda_{Align}$ 设为 10，列表排序损失的温度 $\tau$ 在 $[0.1, 10.0]$ 范围内表现鲁棒，列表排序边距 $\alpha_{max}$ 的最佳值为评估器分数标准差的 0.4 倍。

**推理阶段**的输入输出流如下：

- **输入**：一个提示 $p$ 对应的 $N$ 个候选种子，目标评估器类型，早期截取时间点 $t$（默认 0.2）。
- **处理**：对每个种子运行去噪过程至时间步 $t$，提取中间激活 $h_t$，经 PCA 压缩和编码器处理后由预测头输出预测分数。
- **选择性继续（Selective Sampling）**：根据早期预测得分对 $N$ 个候选排序，仅选择前 $K$ 个（$K \ll N$）继续完成剩余去噪步骤并解码为最终图像。
- **输出**：$K$ 张高质量图像。

选择性采样的计算开销比近似为：

$$Cost \, Ratio \approx \eta + (1 - \eta) \frac{K}{N}$$

其中 $\eta$ 为早期截取点占总步数的比例（默认 0.2）。当 $N=5, K=1$ 时，采样成本可降低超过 60%。

### 模块关系总结

各模块之间形成“截取→压缩→编码→对齐→预测→筛选”的串行数据流。Feature Tap 和 PCA Compression 负责高效提取和压缩早期结构信号；Time-Conditioned Encoder 将压缩特征转化为统一表示；Text Alignment Module 通过损失函数约束确保表示向量包含文本语义信息，与 Prediction Head 共同构成质量预测的核心；Selective Sampling 则利用预测结果做出生成资源的分配决策。整个流程无需修改生成模型本身，探针作为即插即用模块附加在去噪网络上，且训练好的探针可在任意时间步使用，具有良好的跨骨架迁移能力（SD2 训练探针应用于 SD3-M 相关性达 0.96，应用于 FLUX.1-dev 亦达 0.96）。

## 核心模块与公式推导

### 3.1 问题形式化与早期预测器

扩散模型生成一张图像需经过完整的反过程。给定文本提示 $p$，采样器从初始噪声 $z_{t_0} \sim \mathcal{N}(0, \mathbf{I})$ 出发，经 $S$ 步迭代更新：

$$z_{t_{k+1}} = \Psi( z_{t_k}, t_k, t_{k+1}, f_\theta, c(p) )$$

其中 $\Psi$ 是与调度器无关的更新函数，$f_\theta$ 为去噪网络，$c(p)$ 为文本条件嵌入。最终图像由解码器重建：$x_1 = D(z_{t_S})$。

传统“生成-选择”流程需对所有候选种子完成完整去噪后再用评估器 $E$ 评分，计算开销巨大。Probe-Select 的核心思路是：在生成早期（如 $t = 0.2$，即总步数的 20%）提取去噪网络中间激活 $h_t$，通过一个轻量级探针直接预测最终评估器分数：

$$E_\phi(h_t, t) = p_\phi( g_\phi(h_t, t) ) = \hat{y}_{t,m}$$

其中 $g_\phi$ 将中间激活编码为表示向量，$p_\phi$ 将其映射为标量预测值 $\hat{y}_{t,m}$。该预测值用于在早期筛选候选种子，仅对高分候选项继续完成生成。

### 3.2 关键模块

Probe-Select 由以下五个模块构成流水线：

**1. 特征提取（Feature Tap）**：在去噪网络 $f_\theta$ 的选定中间层（如 U-Net 或 DiT 的某块输出）提取激活特征 $h_t$。该特征在生成早期（约 20% 进度）已包含粗布局、物体轮廓等稳定结构信息，与最终图像质量强相关。

**2. PCA 压缩（PCA Compression）**：沿通道维度对 $h_t$ 应用主成分分析（PCA），保留前 48 个主成分。消融实验表明（Table 10），48 维即可使预测性能饱和，而降至 16 维则 Spearman 相关性降至 0.84。该压缩大幅降低后续模块的 GPU 内存占用。

**3. 时间条件编码器（Time-conditioned Encoder）**：使用注意力残差下采样块（attention–residual down blocks）配合时间调制（time modulation），将压缩后的特征编码为固定维度的表示向量 $u_t$。时间步 $t$ 通过调制注入编码器，使探针感知生成进度。

**4. 文本对齐模块（Text Alignment Module）**：通过对比对齐损失（见下节）将探针表示 $u_t$ 与提示文本的 CLIP 嵌入 $e_p$ 对齐。该模块确保预测的质量分数对文本语义敏感，而非仅依赖视觉结构。消融实验（Table 7）表明，移除该模块后 ImageReward 预测相关性从 0.99 骤降至 0.66。

**5. 预测头（Prediction Head）**：三层 MLP 后接 Sigmoid 激活，将表示向量映射为 $[0, 1]$ 区间的标量分数 $\hat{y}_{t,m}$。

### 3.3 核心损失函数

Probe-Select 的训练目标由两部分组成：

$$\mathcal{L} = \mathcal{L}_{list} + \lambda_{Align} \mathcal{L}_{Align}$$

**列表排序损失 $\mathcal{L}_{list}$**：基于 softmax 的列表级排序损失，旨在传递评估器间的相对偏好排序，使探针关注区分性结构线索：

$$\mathcal{L}_{list} = -\frac{1}{B} \sum_{i=1}^B \log \frac{\exp( \hat{y}_t^i / \tau_{list} )}{\sum_{j: y_j + \alpha < y_i} \exp( \hat{y}_t^j / \tau_{list} )}$$

其中 $B$ 为批次大小，$\hat{y}_t^i$ 为样本 $i$ 的预测分数，$y_i$ 为真实评估器分数，$\tau_{list}$ 为温度参数，$\alpha$ 为排序边距。该损失仅惩罚排序错误超过边距 $\alpha$ 的样本对，使训练对分数尺度不敏感。消融实验（Table 8）表明，$\tau_{list}$ 在 $[0.1, 10.0]$ 内相关性保持在 0.96–0.99，表现鲁棒；而边距 $\alpha_{max}$（Table 9）是关键超参，最佳值为评估器分数标准差的 0.4 倍（$\alpha_{max} = 0.4\sigma$），此时相关性达 0.99。

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/019_Table_8.jpg]]

**对比文本对齐损失 $\mathcal{L}_{Align}$**：将探针表示 $u_i$ 与对应提示文本的 CLIP 嵌入 $e_p^i$ 对齐的 InfoNCE 损失：

$$\mathcal{L}_{Align} = -\frac{1}{B} \sum_{i=1}^B \log \frac{\exp( \cos(u_i, e_p^i) / \tau_{Align} )}{\sum_{j=1}^B \exp( \cos(u_i, e_p^j) / \tau_{Align} )}$$

其中 $\cos(\cdot, \cdot)$ 为余弦相似度，$\tau_{Align}$ 为对齐温度。该损失使探针表示保持文本感知，确保预测的质量分数反映文本-图像一致性。

### 3.4 选择性采样策略

训练完成后，Probe-Select 作为通用评估器可在任意时间步使用。选择性采样流程如下：

1. 对 $N$ 个候选种子，运行采样器至早期检查点 $t = 0.2$；
2. 提取中间激活，用探针预测每个候选项的评估器分数 $\hat{y}_{t,m}$；
3. 根据预测分数排序，选择前 $K$ 个（$K \ll N$）候选项继续完成生成；
4. 其余候选项提前终止。

该策略的计算开销比可近似为：

$$\text{Cost Ratio} \approx \eta + (1 - \eta) \frac{K}{N}$$

其中 $\eta$ 为早期检查点占总步数的比例。当 $N = 5, K = 1, \eta = 0.2$ 时，计算开销约为完整生成的 $0.2 + 0.8 \times 0.2 = 0.36$，即节省超过 60% 的采样成本。

## 实验与分析

### 核心实验设置

Probe-Select 的训练基于 MS-COCO 数据集，每个提示生成 16 个候选图像，使用 8 种不同的评估器（包括 ImageReward、HPSv2.1、PickScore、CLIPScore 等）计算真实质量分数。训练在 4 块 NVIDIA A100-SXM4-40GB GPU 上进行，批次大小为 480，最多 200 个 epoch，采用 AdamW 优化器（学习率 $1\times10^{-5}$，权重衰减 $1\times10^{-2}$）配合余弦退火调度（$\eta_{\min}=1\times10^{-6}$）。对比文本对齐损失的权重设为 $\lambda_{\mathrm{Align}}=10$，列表排序损失和对比对齐损失的最大温度参数均设为 $\tau_{\mathrm{list,max}}=\tau_{\mathrm{Align,max}}=1.0$。

### 早期信号稳定性验证

**Table 1** 展示了从去噪网络中间激活特征预测的分数与各评估器真实分数之间的 Spearman 相关性在不同时间步上的变化。核心发现是：**预测相关性在时间维度上表现出显著的稳定性**，在 SD2 上，t=0.2 时 PickScore 相关性为 0.79，ImageReward 相关性高达 0.99，且这些数值在后续时间步几乎保持不变。在 SD3-M 上，HPSv2.1 的相关性从 t=0.2 的 0.79 到 t=0.6 的 0.80，变化幅度极小。这验证了论文的核心假设——去噪网络在生成早期（约 20% 进度）就已包含稳定的粗结构信息，这些信息与最终图像质量强相关，因此可以作为早期质量预测的可靠信号。

**Table 4** 进一步验证了 SD3-L 在极早期时间步（0.05–0.20）的表现，确认 t=0.2 是预测质量与计算节省之间的良好平衡点。

### 选择性生成主结果

**Table 2** 展示了 Probe-Select 在不同生成模型骨架上的选择性生成结果。实验设置中，基线方法对每个提示生成 5 个候选并取平均分数（no-selection baseline），Probe-Select 则从 N=16 个候选中选择 K=5 个继续完成生成。

在 SD2 上，以 ImageReward 为目标评估器时，Probe-Select 将 ImageReward 得分从基线的 0.49 提升至 1.59（+1.10），HPSv2.1 从 26.95 提升至 29.03（+2.08）。在 SD3-L 上，ImageReward 从 1.14 提升至 1.83（+0.69），HPSv2.1 从 30.29 提升至 31.81（+1.52）。在 FLUX.1-dev 上，ImageReward 从 0.92 提升至 1.79（+0.87），HPSv2.1 从 29.14 提升至 31.47（+2.33）。值得注意的是，Probe-Select 在提升感知质量指标的同时，并未损害分布层面的指标——SD3-L 的 FID 从 23.72 改善至 23.64。

**Figure 5** 展示了候选数量 N 和被选择种子数 K 对平均 Top-K ImageReward 的影响。结果表明，在固定 K 下，随着 N 增加，质量提升趋于饱和，这为实际部署中平衡计算开销与质量收益提供了参考。

### 跨骨架迁移能力

**Table 5** 展示了探针网络的跨骨架迁移性能。在 SD2 上训练的探针直接应用于 SD3-M，Spearman 相关性达到 0.96；应用于 FLUX.1-dev 同样达到 0.96。这一结果表明，不同去噪网络在早期阶段学到的结构信号具有高度通用性，大幅降低了在新模型上部署 Probe-Select 的训练成本。

### 泛化性能

**Table 6** 展示了 Probe-Select 在 DrawBench、GenEval、HPD、T2I-CompBench 等额外基准上的泛化性能。在 DrawBench 上，Probe-Select 将 ImageReward 从 1.08 提升至 1.55（+0.47），表明该方法在分布外提示上同样有效，持续优于未选择的基线。

### 消融实验

消融实验系统性地验证了 Probe-Select 各组件的重要性：

- **文本对齐损失的关键作用**（**Table 7**）：当 $\lambda_{\mathrm{Align}}=0$（完全移除对比文本对齐损失）时，ImageReward 预测相关性从 0.99 骤降至 0.66，证明文本感知对准确预测图像质量至关重要。这表明探针需要理解提示语义才能正确评估生成图像与文本的匹配程度。

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/017_Table_7.jpg]]
*Table 7: Ablation on the contrastive alignment loss weight*

- **温度参数的鲁棒性**（**Table 8**）：列表排序损失的温度 $\tau$ 在 [0.1, 10.0] 范围内表现鲁棒，相关性保持在 0.96–0.99，说明该方法对温度超参不敏感。

- **列表排序边距的影响**（**Table 9**）：最大列表排序边距 $\alpha_{\max}$ 是关键超参，最佳值为 0.4σ（评估器分数的标准差），此时相关性达到 0.99；过小（0.01σ）降至 0.90，过大（0.5σ）降至 0.97。

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/020_Table_9.jpg]]
*Table 9: Ablation on the maximum listwise ranking margin*

- **PCA 压缩维度的平衡**（**Table 10**）：PCA 压缩后的通道维度在 48 时即可饱和，使用 16 维则相关性下降至 0.84，表明适中的特征维度可平衡预测性能与 GPU 内存开销。

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/021_Table_10.jpg]]
*Table 10: Ablation on on the reduced channel dimension CPCA for the denoiser feature map*

### 早期解码基线的对比

论文还对比了一种朴素的早期评估基线：在 t=0.2 时直接解码出近似图像，再用现成的评估器（如 BLIP-ITM）进行评分。该基线的 Spearman 相关性仅有 0.52，远低于 Probe-Select 的 0.9+。这一对比揭示了关键洞察：早期阶段的中间激活包含的结构信息远丰富于早期解码的模糊图像，因此**早期质量评估需要专门设计的探针网络，而非简单复用现有评估器**。

### 补充图表

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/004_Table_1.jpg]]
*Table 1: Spearman correlation between predicted score and each evaluator from latent feature in different time stamps. The results demonstrate remarkable stability, with correlation scores remaining constant to two significant figures across time*

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/005_Table_2.jpg]]
*Table 2: Evaluation of models across various benchmarks. The best result is highlighted in bold, and the second best result is underlined*

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/011_Table_5.jpg]]
*Table 5: Cross-backbone transfer of probe networks. Each entry reports the Spearman correlation when a probe trained on the source backbone is applied to the target backbone*

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/007_Figure_5.jpg]]
*Figure 5: The relationship of number of candidates (N) and selected seeds (K)*

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/016_Table_6.jpg]]
*Table 6: Generalization to additional text-to-image benchmarks. Probe-Select consistently improves final quality metrics over the no-selection baseline*

![[assets/figures/papers/paper_list_l2348_https_arxiv_org_abs_2603_02829/figures/012_Table_4.jpg]]
*Table 4: Spearman correlation at very early checkpoints on SD3- L. Correlations become consistently strong at*

## 方法谱系与知识库定位

### 1. 问题定位：从后验评估到早期预测

在扩散模型的标准“生成-选择”流程中，图像质量评估（如 CLIPScore、ImageReward）必须在完整生成图像后进行，导致大量计算资源消耗在最终质量不高的候选样本上。Probe-Select 的核心突破在于将评估时机从“后验”前移至“早期”（约 20% 总步数），其因果机制建立在一条关键发现之上：去噪网络中间层的激活特征在生成早期就已包含稳定的粗结构信息（物体布局、空间构成），这些信息与最终图像质量强相关。

与直接使用现成评估器的简单早期解码基线（在 t=0.2 解码图像并用 BLIP-ITM 评分，Spearman 相关性仅 0.52）相比，Probe-Select 通过专用探针设计将预测相关性提升至 0.9 以上，证明早期评估需要专用的特征读取和训练策略，而非简单的时间前移。

### 2. 方法谱系中的位置

Probe-Select 处于扩散模型效率优化与质量评估的交叉地带，其方法谱系可沿以下维度展开：

**（1）扩散模型加速采样**：与 DDIM、DPM-Solver 等通过减少采样步数来加速的方法不同，Probe-Select 不修改生成模型本身，而是通过提前终止低分候选来节省计算。其选择性采样策略的期望开销比为 $\text{Cost Ratio} \approx \eta + (1 - \eta) \frac{K}{N}$，其中 $\eta$ 为早期评估所占开销比例，$K$ 为保留候选数，$N$ 为总候选数。

**（2）图像质量评估**：传统评估器（ImageReward、HPSv2.1、PickScore 等）均以后验方式作用于完整图像。Probe-Select 将这些评估器作为“教师信号”训练探针，使探针能够在生成中期预测最终评估分数，本质上是将后验评估器蒸馏为早期预测器。

**（3）中间特征利用**：与从扩散模型中间层提取语义特征用于分割、编辑等工作不同，Probe-Select 首次系统性地证明这些中间激活（经 PCA 压缩至 48 维后）可直接用于预测最终图像质量，且在 t=0.2 时即达到稳定相关性。

### 3. 与基线方法的差异分析

Probe-Select 与两类基线形成鲜明对比：

| 对比维度 | 完整生成基线 | 早期解码基线 | Probe-Select |
|---------|------------|------------|-------------|
| 评估时机 | 生成完成后 | 早期解码 | 早期激活直读 |
| 评估输入 | 最终图像 $x_1$ | 早期解码近似图像 | 中间激活 $h_t$ |
| 评分模型 | 现成评估器 | 现成评估器 | 训练专用探针 $E_\phi$ |
| 训练需求 | 无 | 无 | 列表排序 + 文本对齐损失 |
| 预测相关性 | — | ~0.52 | 0.79–0.99 |

完整生成基线代表真实应用场景的默认策略，对所有候选种子完成完整去噪后取平均分数。Probe-Select 在 SD2 上将 ImageReward 从 0.49 提升至 1.59，HPSv2.1 从 26.95 提升至 29.03，同时采样成本降低超过 60%。

### 4. 适用边界与跨骨架迁移

Probe-Select 的适用边界由以下实验证据界定：

**跨骨架泛化**：在 SD2 上训练的探针直接应用于 SD3-M 时，Spearman 相关性达 0.96；应用于 FLUX.1-dev 时同样为 0.96。这一结果表明，不同去噪网络在早期阶段编码的结构信息具有某种通用性，大幅降低了多模型部署的训练成本。

**多评估器兼容**：探针可针对不同评估器（ImageReward、HPSv2.1、PickScore、BLIP-ITM 等）分别训练，在 SD2 上中位 Spearman 相关性 ≥ 0.7，其中 ImageReward 和 BLIP-ITM 接近 0.99。

**多基准泛化**：在 DrawBench、GenEval、HPD、T2I-CompBench 等额外基准上，Probe-Select 持续优于未选择基线，如 DrawBench 上 ImageReward 从 1.08 提升至 1.55。

**时间步鲁棒性**：预测相关性在 t=0.2 至 t=0.6 间保持稳定（变化幅度在 0.01–0.02 以内），t=0.2 被确定为预测质量与计算节省的最佳平衡点。

### 5. 局限性与开放问题

**（1）评估器依赖性**：当前方法需要为每个目标评估器训练独立的探针，多个评估器需多个探针，增加了训练和存储成本。未来可探索多任务探针或评估器无关的通用质量表示。

**（2）层选择固定**：探针仅在生成去噪网络固定的中间层进行特征提取，未探索更深或更浅层的信息互补性。自适应层选择或层融合可能是提升预测精度的方向。

**（3）训练数据分布**：训练数据基于 MS-COCO，虽然在跨骨架迁移上表现良好，但在更复杂的用户生成场景或真实世界分布上的泛化性仍需进一步验证。

**（4）选择策略刚性**：选择策略依赖预设的 $K$ 和 $N$，尚未集成自适应停止或实时质量引导。引入动态阈值或置信度感知的提前终止可能进一步减少计算冗余。

**（5）范式覆盖有限**：研究仅覆盖扩散和流匹配模型（SD2、SD3、FLUX），对于自回归等其他生成范式的适用性尚未被探索。不同范式中“中间激活”的定义和可获取性可能存在根本差异。

**（6）文本对齐的关键性**：消融实验表明，移除对比文本对齐损失后 ImageReward 预测相关性从 0.99 骤降至 0.66，证明文本感知对质量预测至关重要。然而，当前对齐仅使用 CLIP 文本嵌入，更丰富的文本理解（如空间关系、属性绑定）可能进一步提升预测精度。

## 原文 PDF

![[paperPDFs/CVPR_2026/Toward_Early_Quality_Assessment_of_Text_to_Image_Diffusion_Models.pdf]]