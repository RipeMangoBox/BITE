---
title: "Scan Clusters, Not Pixels: A Cluster-Centric Paradigm for Efficient Ultra-high-definition Image Restoration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Scan_Clusters_Not_Pixels_A_Cluster_Centric_Paradigm_for_Efficient_Ultra_high_definition_Image_Restoration.pdf
project_link: null
code_link: "https://github.com/5chen/C2SSM"
aliases:
- Scan_Clusters_No
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将全局依赖关系建模的基本单元从单个像素替换为少量可学习的语义聚类中心，并通过概率相似性分布将中心级上下文扩散回所有像素。
primary_logic: 自然图像具有结构冗余与语义汇聚特性，其高维特征可被简洁表示为稀疏的聚类中心，而全局推理仅需在这些中心上进行，大幅降低计算量，同时通过概率分布保持与原始像素的关联。
claims:
- 移除聚类中心扫描模块（CCSM）后，UHD-LOL4K上的PSNR从完整模型的39.61 dB骤降至35.87 dB，证明CCSM不可或缺。
- 在五个UHD恢复任务上均取得新的最优结果，例如UHD-LOL4K上PSNR 39.61 dB，超过先前最优MixNet 0.39 dB。
- 所提扫描策略的FLOPs仅为0.407G，远低于MambaIRv2等代表性方法，实现高效全分辨率处理。
- UHD-LOL4K 上 PSNR (dB) = 39.61
---

# Scan Clusters, Not Pixels: A Cluster-Centric Paradigm for Efficient Ultra-high-definition Image Restoration

> [!tip] 核心洞察
> 自然图像具有结构冗余与语义汇聚特性，其高维特征可被简洁表示为稀疏的聚类中心，而全局推理仅需在这些中心上进行，大幅降低计算量，同时通过概率分布保持与原始像素的关联。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扫描聚类而非像素：面向高效超高清图像恢复的聚类中心范式 |
| 英文题名 | Scan Clusters, Not Pixels: A Cluster-Centric Paradigm for Efficient Ultra-high-definition Image Restoration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21917) · [Code](https://github.com/5chen/C2SSM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | C2SSM |
| Dataset | UHD-LOL4K, UHD-LL, 4K-Rain13k, 4K-RealRain |

> [!tip] 效果简介
> - UHD-LOL4K 上，PSNR (dB) 39.61 vs 39.22 (MixNet) (+0.39)。
> - UHD-LL 上，PSNR (dB) 27.63 vs 27.54 (MixNet) (+0.09)。
> - 4K-Rain13k 上，PSNR (dB) 35.13 vs 34.48 (ERR) (+0.65)。

## 概要

超高清（UHD）图像恢复面临的核心瓶颈在于：现有基于状态空间模型（SSM）的方法仍依赖像素级序列扫描，当处理数百万像素时会产生无法承受的计算与存储开销，难以在消费级GPU上实现高效的全分辨率建模。

本文提出**C2SSM**，一种以聚类为中心的扫描范式。其核心洞察是：自然图像具有结构冗余与语义汇聚特性，高维特征可被简洁表示为稀疏的聚类中心，而全局推理仅需在这些中心上进行。具体而言，C2SSM将全局依赖建模的基本单元从单个像素替换为少量可学习的语义聚类中心，通过概率相似性分布将中心级上下文扩散回所有像素，从而在保持全局建模能力的同时大幅降低计算复杂度。

在五个UHD恢复任务（低光增强、去雨、去模糊、去雾、去雪）上，C2SSM均取得了新的最优结果。例如，在UHD-LOL4K低光增强数据集上达到39.61 dB PSNR，超过先前最优方法MixNet 0.39 dB。所提扫描策略的FLOPs仅为0.407G，远低于MambaIRv2等代表性方法，验证了聚类中心扫描范式在效率与性能上的双重优势。



### 超高清图像恢复的困境

随着4K/8K显示设备的普及，超高清（Ultra-High-Definition, UHD）图像恢复已成为计算机视觉领域的核心挑战之一。UHD图像通常包含数百万乃至数千万像素，其恢复任务——包括低光增强、去雨、去模糊、去雾和去雪——不仅要求模型具备强大的全局上下文建模能力，还必须能够在消费级GPU的显存限制下完成全分辨率处理。

传统的卷积神经网络（CNN）受限于局部感受野，难以捕获UHD图像中的长程依赖关系。近年来，基于状态空间模型（State Space Model, SSM）的方法，尤其是Mamba架构，凭借其线性计算复杂度和优异的全局建模能力，在图像恢复领域展现出巨大潜力。然而，现有SSM方法在应对UHD图像时暴露出一个根本性瓶颈。

### 像素级扫描的不可承受之重

现有基于Mamba的图像恢复方法，如**MambaIR**（Guo et al., ECCV 2024）和**MambaIRv2**（Guo et al., CVPR 2025），均采用像素级序列扫描策略：将图像特征展开为一维序列，逐像素地进行状态空间建模。这种“扫描所有像素”的范式在处理UHD图像时面临两个严重问题：

1. **计算与显存爆炸**：UHD图像的特征图尺寸极大，像素级扫描导致序列长度呈平方级增长，使得SSM的计算量和显存占用远超消费级GPU的承载能力。如Vmamba所采用的Z形扫描路径，在处理UHD图像时会产生严重的显存瓶颈。

2. **效率与精度的两难**：为缓解上述问题，**EfficientVMamba**等方法通过省略采样步骤来降低扫描成本，但这不可避免地损害了全局建模的精度，形成效率与性能之间的零和博弈。

### 核心洞察：从像素到聚类的范式转移

本文的核心洞察在于：自然图像具有显著的结构冗余与语义汇聚特性。一幅UHD图像的高维特征空间并非均匀分布，而是呈现出明显的聚类结构——大量像素共享相似的语义属性，可以被压缩为少数具有代表性的语义中心。这意味着，全局依赖关系建模的基本单元完全可以从“数百万像素”缩减为“少量聚类中心”，从而在保持全局感受野的同时，将计算复杂度降低数个数量级。

基于这一洞察，本文提出了**C2SSM**（Cluster-Centric State Space Model），从根本上改变了SSM在UHD图像恢复中的应用范式：不再逐像素扫描，而是将特征分布蒸馏为稀疏的语义聚类中心，仅在中心间进行全局推理，再通过概率相似性分布将中心级上下文扩散回所有像素。这一“扫描聚类而非像素”的策略，使得在消费级GPU上对UHD图像进行高效全分辨率建模成为可能。



## 核心方法与创新机理

### 瓶颈诊断：像素级扫描的不可承受之重

现有基于状态空间模型（SSM）的超高清图像恢复方法——如 **MambaIR**（Guo et al., ECCV 2024）及其改进版 **MambaIRv2**（Guo et al., CVPR 2025）——在建模全局依赖时，无一例外地沿袭了像素级序列扫描的范式。当图像分辨率跃升至4K乃至8K级别，像素数量动辄数百万，这种逐像素扫描的策略会导致计算复杂度与显存占用呈平方级膨胀，使得在消费级GPU上实现全分辨率端到端处理成为奢望。**Wave-Mamba**（Zou et al., ACM MM 2024）虽引入小波分解以降低空间维度，但仍未跳出“扫描像素”这一根本性约束。

### 因果杠杆：从“扫描像素”到“扫描聚类中心”

C2SSM的核心创新在于**将全局依赖建模的基本单元从单个像素替换为少量可学习的语义聚类中心**。这一转变基于一个关键的观察：自然图像具有高度的结构冗余与语义汇聚特性，其高维特征空间可以被简洁地表示为稀疏的聚类中心，而无需在每一个像素上独立执行全局推理。

具体而言，C2SSM通过以下三个相互耦合的机制实现这一转变：

**1. 特征聚合（Feature Aggregating, FA）——语义中心的神经参数化学习**

传统聚类方法依赖迭代优化（如K-Means），在深度网络中难以端到端训练。C2SSM采用一种基于概率相似性分布的神经参数化混合模型：首先计算每个像素特征 $f_p$ 与各聚类中心 $c_k$ 的余弦相似度，并归一化为概率分布 $p_k(f_p)$：

$$p_k(f_p) = \frac{\mathrm{sim}(f_p, c_k)}{\sum_{p \in \Omega} \mathrm{sim}(f_p, c_k)}, \quad \mathrm{sim}(f_p, c_k) = \frac{f_p^T \cdot c_k}{\|f_p\| \cdot \|c_k\|}$$

随后，通过可学习的门控机制 $\delta(\alpha \cdot p_k(f_p) + \beta)$ 筛选出对中心 $k$ 具有显著语义贡献的像素，并聚合更新聚类中心 $\hat{c}_k$：

$$\hat{c}_k = \frac{1}{N_k} \left( v_k + \sum_{p \in \Omega} \delta(\alpha \cdot p_k(f_p) + \beta) \cdot \hat{f}_p \right), \quad N_k = 1 + \sum_{p \in \Omega} \delta(\alpha \cdot p_k(f_p) + \beta)$$

该门控机制天然地剪枝了与中心语义无关的像素，在保留语义相关性的同时降低了有效计算量。

**2. 选择性扫描（Selective Scanning, S6）——中心级全局推理**

全局依赖建模仅在 $n$ 个聚类中心上执行（$n \ll HW$，典型值 $n=4$）。通过Mamba的S6块获得各中心的全局上下文权重 $W$：

$$W = \mathrm{S6}(\hat{C}; \theta_{mamba})$$

此步骤的计算复杂度为 $O(C \cdot n^2)$，与全像素扫描的 $O(C \cdot H^2W^2)$ 相比几乎可忽略不计。

**3. 得分扩散（Score Diffusing, SD）——全概率反演至像素级权重**

这是C2SSM区别于简单“降采样-上采样”策略的关键设计。通过softmax归一化得到像素 $p$ 属于中心 $k$ 的后验概率 $\alpha_{p,k}$：

$$\alpha_{p,k} = \frac{\exp(\alpha \cdot p_k(f_p) + \beta)}{\sum_{k'=1}^n \exp(\alpha \cdot p_{k'}(f_p) + \beta)}$$

随后基于全概率公式，将像素的全局权重 $w_p$ 表达为各中心权重的期望：

$$w_p = \mathbb{E}_{k \sim \mathcal{D}(p)}[w_k] = \sum_{k=1}^n \alpha_{p,k} \cdot w_k$$

这一机制确保了**每一个像素都能获得全局上下文信息**，而非仅中心像素受益，从而在保持全分辨率建模精度的同时，将计算开销压缩至极致。

### 补充创新：空域-通道特征调制器（SCFM）

聚类压缩过程不可避免地会丢失部分高频细节。为此，C2SSM引入并行的**空域-通道特征调制器（Spatial-Channel Feature Modulator, SCFM）**，通过空间注意力 $W_s$ 与通道注意力 $W_c$ 的双路径设计，最大化保留原始特征中的细节信息：

$$W_s = \delta(\mathrm{Conv}([\mathrm{Max}(\pmb{F}_{in}); \mathrm{Mean}(\pmb{F}_{in})]))$$

$$W_c = \delta(\mathrm{Max}(\pmb{F}_d) + \mathrm{Avg}(\pmb{F}_d))$$

$$\pmb{F}_{out} = \mathrm{Conv}(W_s \cdot \pmb{F}_{in}) + \mathrm{Conv}(W_c \cdot \pmb{F}_{in})$$

SCFM与CCSM并行部署于解码器中，共同实现空间-通道的全局特征耦合。

### 与基线方法的关键差异总结

| 设计维度 | 代表性基线 | C2SSM |
|---------|-----------|-------|
| 全局建模的扫描对象 | 所有像素（MambaIR, MambaIRv2） | $n$ 个可学习聚类中心（$n=4$） |
| 上下文传播方式 | 直接对像素特征应用SSM扫描 | 中心级SSM扫描 + 全概率公式反演至像素 |
| 高频细节保留 | 仅依赖主干网络潜在表示 | 并行SCFM分支进行空间-通道补偿 |
| 计算复杂度 | $O(C \cdot H^2W^2)$ | $O(C \cdot n^2)$，$n \ll HW$ |

消融实验（Table 8）提供了决定性证据：移除CCSM后，UHD-LOL4K上的PSNR从完整模型的39.61 dB骤降至35.87 dB，降幅高达3.74 dB，充分证明聚类中心扫描策略是不可或缺的核心创新。同时，SCFM的移除也导致性能衰减，验证了双路径设计的必要性。效率对比（Table 10）进一步表明，C2SSM的扫描策略FLOPs仅为0.407G，远低于MambaIRv2等代表性方法，真正实现了高效的全分辨率全局建模。



C2SSM 采用**非对称编码器-解码器架构**，其核心设计理念是将全局依赖建模的基本单元从像素置换为少量可学习的语义聚类中心，从而在保持全分辨率处理能力的同时，将计算和内存开销压缩至消费级GPU可承受的范围。

### 架构总览

整体架构包含三个主要阶段：**编码器（Encoder）**、**瓶颈层（Bottleneck）** 和 **解码器（Decoder）**，后接一个**精炼阶段（Refinement）**。具体结构参数为：编码器与解码器各含 $N_1=3$ 个层级，每层共享相同的块结构 $N_2=[2,4,4]$；瓶颈层和精炼阶段各含 $N_3=N_5=4$ 个块，基础嵌入维度为 32。

**编码器**的设计刻意保持轻量——**仅由前馈网络（FFN）构成**，不含任何注意力或SSM模块。这一非对称设计的目的在于：编码器仅负责特征下采样以降低后续处理的空间分辨率，而将所有全局建模能力集中于解码器。输入UHD图像经编码器逐级下采样后，得到紧凑的特征表示。

**解码器**是C2SSM的核心，集成了两个互补模块：
- **聚类中心扫描模块（Cluster-Centric Scanning Module, CCSM）**：负责全局上下文建模，将特征聚合为少量语义聚类中心，在中心间执行选择性扫描（S6），再通过概率分布将全局信息扩散回所有像素。
- **空域-通道特征调制器（Spatial-Channel Feature Modulator, SCFM）**：作为并行分支运行，利用空间注意力和通道注意力保留聚类过程中可能丢失的高频细节，最大化特征间的互信息。

解码器中的每个块将CCSM和SCFM与FFN级联，实现**空间-通道全局特征耦合**。具体而言，输入特征 $\pmb{F}_{in}$ 首先经MLP和深度可分离卷积变换后由SiLU激活，得到中间表示 $\pmb{F}_d$；随后依次经过特征聚合（FA）、选择性扫描（S6）和得分扩散（SD），经归一化后与门控信号相乘，形成CCSM的最终输出。SCFM则在并行路径上计算空间注意力图 $W_s$ 和通道注意力权重 $W_c$，将两者分别作用于输入特征后相加，补偿聚类过程中的信息损失。

### 数据流与输入输出

完整的数据流如下：
1. **输入**：全分辨率UHD图像（训练时采用 768×768 的随机裁剪块）。
2. **编码器下采样**：经3级FFN-only的下采样路径，逐步压缩空间维度，得到低分辨率特征图。
3. **瓶颈层**：4个块对压缩后的特征进行深度变换。
4. **解码器上采样**：3级解码器逐级恢复空间分辨率，每级通过CCSM注入全局上下文、通过SCFM保留局部细节。
5. **精炼阶段**：4个块对恢复后的特征进行最终精炼。
6. **输出**：与输入同分辨率的恢复图像。

这种非对称设计的关键优势在于：编码器不执行任何全局扫描，将计算资源集中于解码器；而解码器中的CCSM仅对 $n$ 个聚类中心（默认 $n=4$）而非 $H \times W$ 个像素执行SSM扫描，使得全局建模的复杂度从 $O(C \cdot H^2 W^2)$ 降至 $O(C \cdot n^2)$，在4K分辨率下实现了数量级的效率提升（FLOPs仅为0.407G，远低于MambaIRv2等代表性方法）。

### 补充图表

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our proposed C2SSM. C2SSM employs an asymmetric U-Net architecture whose decoder integrates the Cluster-Centric Scanning Module and Spatial-Channel Feature Modulator to achieve spatial-channel global feature coupling*



C2SSM的核心创新在于将全局依赖建模的基本单元从像素替换为少量可学习的语义聚类中心，并围绕这一思想构建了**聚类中心扫描模块（Cluster-Centric Scanning Module, CCSM）**和**空间-通道特征调制器（Spatial-Channel Feature Modulator, SCFM）**两个关键组件。

### 聚类中心扫描模块（CCSM）

CCSM是整个方法的核心，包含三个阶段：特征聚合（Feature Aggregating, FA）、选择性扫描（S6）和得分扩散（Score Diffusing, SD）。其整体计算流程如下：

首先，输入特征 $\pmb{F}_{in}$ 经过MLP、深度可分离卷积和SiLU激活后得到中间表示：

$$\pmb{F}_d = \mathrm{SiLU}(\mathrm{DWConv}(\mathrm{MLP}(\pmb{F}_{in}))) \tag{1}$$

随后，对 $\pmb{F}_d$ 依次执行特征聚合、选择性扫描和得分扩散，并进行归一化，得到融合全局上下文的特征：

$$\pmb{F}_f = \mathrm{Norm}(\mathrm{SD}(\mathrm{S6}(\mathrm{FA}(\pmb{F}_d)))) \tag{2}$$

最终，CCSM的输出由融合特征与原始输入的门控机制产生：

$$\pmb{F}_{out} = \pmb{F}_f \cdot \mathrm{SiLU}(\mathrm{MLP}(\pmb{F}_{in})) \tag{3}$$

#### 特征聚合（FA）

特征聚合的目标是从UHD图像的高维特征中学习一组语义代表性的聚类中心，避免传统迭代聚类带来的低效。对于每个聚类中心 $c_k$，定义像素 $p$ 对其的归一化相似度分布：

$$p_k(f_p) = \frac{\mathrm{sim}(f_p, c_k)}{\sum_{p \in \Omega} \mathrm{sim}(f_p, c_k)} \tag{4}$$

其中余弦相似度定义为：

$$\mathrm{sim}(f_p, c_k) = \frac{f_p^T \cdot c_k}{\|f_p\| \cdot \|c_k\|} \tag{5}$$

通过可学习的门控机制聚合像素特征，得到精炼后的聚类中心：

$$\hat{c}_k = \frac{1}{N_k} \left( v_k + \sum_{p \in \Omega} \delta(\alpha \cdot p_k(f_p) + \beta) \cdot \hat{f}_p \right) \tag{6}$$

其中门控因子 $N_k$ 用于归一化，同时天然地剪枝掉与中心相似度不显著的像素，减少有效计算量：

$$N_k = 1 + \sum_{p \in \Omega} \delta(\alpha \cdot p_k(f_p) + \beta) \tag{7}$$

#### 选择性扫描（S6）

在获得精炼的聚类中心 $\hat{C}$ 后，通过Mamba的S6块对中心间的全局依赖进行建模。由于中心数量 $n$ 远小于像素总数（$n \ll HW$），该步骤的复杂度仅为 $O(C \cdot n^2)$，相比全像素扫描的 $O(C \cdot H^2W^2)$ 可忽略不计：

$$W = \mathrm{S6}(\hat{C}; \theta_{mamba}) \tag{8}$$

#### 得分扩散（SD）

得分扩散通过概率分布将中心级的全局上下文权重反演回每个像素。首先计算像素 $p$ 属于聚类 $k$ 的后验概率：

$$\alpha_{p,k} = \frac{\exp(\alpha \cdot p_k(f_p) + \beta)}{\sum_{k'=1}^n \exp(\alpha \cdot p_{k'}(f_p) + \beta)} \tag{9}$$

随后，基于全概率公式，像素 $p$ 的全局权重等于各中心权重的期望：

$$w_p = \mathbb{E}_{k \sim \mathcal{D}(p)}[w_k] = \sum_{k=1}^n \alpha_{p,k} \cdot w_k \tag{10}$$

该设计确保所有像素——包括那些未被聚类中心直接覆盖的“非必要像素”——都能获得来自全局上下文的丰富信息。

### 空间-通道特征调制器（SCFM）

SCFM作为CCSM的并行分支，旨在保留聚类过程中可能丢失的高频细节。它通过空间注意力和通道注意力的协同作用来最大化互信息。

空间注意力由最大池化和平均池化级联后经卷积和激活得到：

$$W_s = \delta(\mathrm{Conv}([\mathrm{Max}(\pmb{F}_{in}); \mathrm{Mean}(\pmb{F}_{in})])) \tag{11}$$

通道注意力路径先将输入特征经两层卷积和ReLU处理：

$$\pmb{F}_d = \mathrm{Conv}(\mathrm{ReLU}(\mathrm{Conv}(\pmb{F}_{in}))) \tag{12}$$

随后通过特征的最大值与平均值相加后激活得到通道注意力权重：

$$W_c = \delta(\mathrm{Max}(\pmb{F}_d) + \mathrm{Avg}(\pmb{F}_d)) \tag{13}$$

SCFM的最终输出融合空间与通道注意力：

$$\pmb{F}_{out} = \mathrm{Conv}(W_s \cdot \pmb{F}_{in}) + \mathrm{Conv}(W_c \cdot \pmb{F}_{in}) \tag{14}$$

### 架构集成

C2SSM采用非对称U-Net架构：编码器仅包含前馈网络（FFN）以降低计算量，解码器则集成CCSM和SCFM，实现空间-通道的全局特征耦合。消融实验表明，移除CCSM会导致UHD-LOL4K上的PSNR从39.61 dB骤降至35.87 dB，而移除SCFM同样造成明显的性能衰减，验证了双路径设计的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/001_Figure_1.jpg]]
*Figure 1: The scanning strategies in existing Mamba-based methods and our proposed method. (a) Vmamba [19] employs a Z-shaped scan path that incurs VRAM bottlenecks when processing UHD images due to its full-pixel scanning. (b) EfficientVMamba [23] reduces scanning costs by omitting sampling steps, this compromises global modeling accuracy. (c) The proposed cluster-centric scanning strategy*



## 实验与关键发现

### 核心实验设置

C2SSM 采用非对称 U‑Net 架构，编码器仅包含前馈网络（FFN），解码器集成聚类中心扫描模块（CCSM）与空域‑通道特征调制器（SCFM）。网络配置为 $N_1=3$ 个下采样层级，编码器与解码器各层块数 $N_2=[2,4,4]$，瓶颈与精炼阶段各含 $N_3=N_5=4$ 个块，基础嵌入维度为 32。训练使用 AdamW 优化器，初始学习率 $5\times10^{-4}$ 配合余弦退火调度，输入为从 4K 全分辨率图像中裁剪的 $768\times768$ 块。

### 多任务主结果

C2SSM 在五个超高清恢复任务上均取得最优结果，关键指标如下：

- **UHD‑LOL4K 低光增强**：PSNR 达到 39.61 dB，超越此前最优方法 **MixNet** (Wu et al., arXiv 2024) 0.39 dB，参数量保持竞争力。
- **UHD‑LL 低光增强**：PSNR 27.63 dB，较 MixNet 提升 0.09 dB。需注意文中摘要声称提升 0.19 dB，但表内差值仅为 0.09 dB，存在不一致，建议核对原始数据。
- **4K‑Rain13k 去雨**：PSNR 35.13 dB，超越此前最优 **ERR** 0.65 dB，误差图显示细节恢复更优。
- **4K‑RealRain 真实去雨**：在无参考指标上取得最佳 NIQE (8.198) 与 PIQE (54.90)，表明感知质量领先。
- **UHD‑Blur 去模糊**：PSNR 31.53 dB，较 ERR 提升 1.81 dB，提升幅度显著。
- **UHD‑Haze 去雾**：PSNR 24.08 dB，达到最优。
- **UHD‑Snow 去雪**：PSNR 42.45 dB，超越 **UHDDIP** 0.89 dB。文中摘要声称提升 1.5 dB，与表内数据不符，需核实原表。

### 消融实验

消融实验基于 UHD‑LOL4K 数据集，揭示了各模块的因果贡献：

- **CCSM 的不可替代性**：移除 CCSM 后，PSNR 从完整模型的 39.61 dB 骤降至 35.87 dB，降幅达 3.74 dB，证明聚类中心扫描是性能核心瓶颈。同时移除 SCFM 也会导致额外衰减，表明双路径设计不可或缺。
- **聚类中心数量的敏感性**：在低光增强、去模糊、去雾三个任务上扫描中心数 $n=4$ 时取得最佳 PSNR/SSIM 平衡。过少的中心（$n=1$）限制全局建模能力，过多的中心（$n>4$）引入冗余计算且性能不再提升。
- **扫描策略效率**：以 $64\times64$ 输入测量 FLOPs，C2SSM 的聚类中心扫描策略仅需 0.407 G FLOPs，远低于 **MambaIR** (Guo et al., ECCV 2024)、**Wave‑Mamba** (Zou et al., ACM MM 2024)、**EVSSM** 及 **MambaIRv2** (Guo et al., CVPR 2025) 等像素级扫描方案，验证了 $O(C\cdot n^2)$ 复杂度（$n\ll HW$）带来的实际效率增益。

### 关键图表结论

- **Table 1–7** 汇总了各任务定量对比，C2SSM 在所有有参考和无参考指标上均处于领先位置。
- **Table 8** 的消融结果构成最有力因果证据：CCSM 的移除导致性能崩溃，确认聚类中心扫描是方法有效性的决定性组件。
- **Table 10** 的效率对比直接支撑“扫描聚类而非像素”的核心主张，FLOPs 降低一个数量级以上。
- **Figure 3–5** 的可视化对比显示 C2SSM 在颜色保真度、高频细节保留和伪影抑制方面均优于基线方法，颜色直方图与误差图进一步量化了恢复质量。

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/005_Table_1.jpg]]
*Table 1: Comparison of quantitative results on UHD-LOL4K dataset [32]*

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/013_Table_8.jpg]]
*Table 8: Ablation study of proposed blocks on UHD-LOL4K dataset [32]*

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/014_Table_10.jpg]]
*Table 10: Comparison of different scanning strategies. FLOPs are measured with an image of the size 64 × 64 pixels*

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/003_Figure_3.jpg]]
*Figure 3: Visual quality comparisons on UHD-LOL4K dataset [32]. The last row shows the color histogram of the image*

### 数据一致性提醒

UHD‑LL 与 UHD‑Snow 数据集上，摘要中声称的提升幅度与表内实际差值存在明显出入，建议读者以原始表格数据为准，并关注后续版本是否修正相关表述。

### 补充图表

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/006_Table_2.jpg]]
*Table 2: Comparison of quantitative results on UHD-LL dataset [17]*

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/004_Table_3.jpg]]
*Table 3: Comparison of quantitative results on 4K-Rain13k dataset [1]*

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/008_Table_4.jpg]]
*Table 4: Comparison of quantitative results on 4K-RealRain dataset [1]*

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/009_Table_5.jpg]]
*Table 5: Comparison of quantitative results on UHD-Blur dataset [29]*

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/010_Table_7.jpg]]
*Table 7: Comparison of quantitative results on UHD-Snow dataset [31]*

![[assets/figures/papers/paper_list_l929_https_arxiv_org_abs_2602_21917/figures/012_Table_9.jpg]]
*Table 9: Ablation study of the number of centers*



## 定位与知识库关联

### 1. 与现有工作的关系

#### 1.1 与基于状态空间模型（SSM）的图像恢复方法

C2SSM 属于视觉状态空间模型在图像恢复中的应用谱系。现有基于 Mamba 的方法，如 **MambaIR**（Guo et al., ECCV 2024）和 **MambaIRv2**（Guo et al., CVPR 2025），以及针对 UHD 低光增强的 **Wave-Mamba**（Zou et al., ACM MM 2024），均沿袭了 Vmamba 的像素级序列扫描范式。这一范式的核心瓶颈在于：当处理超高清（UHD）图像时，数百万像素的逐点序列化导致计算复杂度为 $O(C \cdot H^2W^2)$，在消费级 GPU 上引发显存瓶颈。

C2SSM 的根本性突破在于**改变了全局建模的基本单元**。它不再将单个像素作为扫描对象，而是将高维特征分布蒸馏为少量（默认 $n=4$）可学习的语义聚类中心，将 SSM 扫描的复杂度降至 $O(C \cdot n^2)$（$n \ll HW$）。这一转变使得全分辨率 UHD 图像的全局推理在消费级 GPU 上成为可能。

#### 1.2 与 UHD 图像恢复专用架构

在 UHD 恢复领域，**UHDformer**（Wang et al., AAAI 2024）采用双分支 Transformer 架构，通过空间和通道维度的分离处理来降低计算量。**MixNet**（Wu et al., arXiv 2024）作为多个 UHD 恢复任务的前 SOTA，同样致力于在有限资源下实现有效建模。C2SSM 在五个 UHD 恢复基准上全面超越这些方法，其中在 UHD-LOL4K 上以 39.61 dB PSNR 超过 MixNet 0.39 dB，在 UHD-Blur 上以 31.53 dB PSNR 超过 ERR 1.81 dB，验证了聚类中心范式在性能上限上的优势。

#### 1.3 与高效 SSM 扫描策略

EfficientVMamba 尝试通过省略采样步骤来降低扫描成本，但这以牺牲全局建模精度为代价。C2SSM 则通过**概率分布保持与原始像素的关联**：在聚类中心上完成 SSM 扫描后，利用得分扩散（Score Diffusing）机制，通过全概率公式将中心级全局权重反演回每一个像素，从而在不损失全局覆盖的前提下实现高效推理。消融实验（Table 10）表明，C2SSM 的扫描策略 FLOPs 仅为 0.407G，远低于 MambaIR、Wave-Mamba、EVSSM 和 MambaIRv2 等代表性方法。

### 2. 适用边界

**适用场景**：
- 超高清（4K 及以上）图像的多类退化恢复，包括低光增强、去雨、去模糊、去雾、去雪。
- 需要在消费级 GPU 上完成全分辨率端到端推理的部署场景。

**技术前提**：
- 输入图像需具有足够的结构冗余与语义汇聚特性，使得高维特征可被稀疏聚类中心有效表征。对于纹理极度随机或信息高度分散的图像（如纯噪声图），聚类中心的表征能力可能下降，但论文未对此类边界情况进行验证。

**已知局限**：
- 论文未报告任何明确的失效模式或负面结果，这可能是实验筛选的结果。建议在实际部署中对极低信噪比场景进行额外验证。
- 聚类中心数量 $n$ 的敏感性：消融实验（Table 9）表明 $n=4$ 在低光增强、去模糊和去雾三个任务上取得最佳平衡，但该参数在不同任务间的最优值可能存在差异，需要针对新任务进行调优。

### 3. 开放问题

1. **聚类中心的可解释性**：论文未对学习到的聚类中心进行语义可视化或分析。这些中心是否对应可解释的语义概念（如“天空”、“纹理”、“平坦区域”），还是仅为统计意义上的特征聚合点，尚不明确。这一问题的回答将影响该方法在可控恢复和交互式编辑中的扩展潜力。

2. **动态中心数量的自适应机制**：当前聚类中心数量 $n$ 是固定的超参数。对于内容复杂度差异极大的 UHD 图像，是否可以通过自适应机制动态调整中心数量以进一步优化计算资源分配，是一个值得探索的方向。

3. **与其他高效架构的融合**：C2SSM 的聚类中心扫描模块（CCSM）作为一个即插即用的全局建模组件，是否可以与基于 Transformer 或卷积的高效 UHD 架构（如 UHDformer）融合以产生协同增益，有待验证。

4. **数据不一致性问题**：论文在 UHD-LL 数据集上声称超越 MixNet 0.19 dB，但实际表中值差为 0.09 dB；在 UHD-Snow 数据集上声称优于 UHDDIP 1.5 dB，但实际表中值差为 0.89 dB。这些数据描述与表格数值之间的不一致需要作者澄清，可能影响对方法在对应任务上增益幅度的判断。



## 原文 PDF

![[paperPDFs/CVPR_2026/Scan_Clusters_Not_Pixels_A_Cluster_Centric_Paradigm_for_Efficient_Ultra_high_definition_Image_Restoration.pdf]]
