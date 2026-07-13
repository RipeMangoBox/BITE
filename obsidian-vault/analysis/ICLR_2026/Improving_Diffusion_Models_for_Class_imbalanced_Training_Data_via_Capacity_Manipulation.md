---
title: "Improving Diffusion Models for Class-imbalanced Training Data via Capacity Manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Improving_Diffusion_Models_for_Class_imbalanced_Training_Data_via_Capacity_Manipulation.pdf
project_link: null
code_link: https://github.com/Feng-Hong/ImbDiff-CM
openreview_forum_id: wSGle6ag5I
aliases:
- CMC
- IDMCITDCM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "模型容量的显式预留与分配：通过低秩分解将参数拆分为通用部分 θ^g 和少数类专长部分 θ^e，并利用基于类别样本量加权的容量操纵损失，将少数类知识引导至预留的容量，从而保护少数类学习。"
primary_logic: "避免多数类侵占少数类容量的关键在于训练前便为少数类预留低秩容量，并在训练中通过对比通用模型输出与完整模型输出，自适应地分配知识，使通用能力保留在 θ^g，少数类专长固化在 θ^e，最终在不增加推理开销的前提下显著提升不平衡条件下的生成鲁棒性。"
claims:
- "少数类对参数剪枝异常敏感，其信息被挤占至非关键容量中，成为容量支配问题的直接实证。"
- "定理2.1给出多数类主导参数更新比例的解析表达，证明容量失衡与不平衡程度正相关。"
- "CM在Imb. CIFAR-100 (IR=100)上FID从最优基线 8.309 降至 7.519，且在所有数据集和指标上一致优于现有方法。"
- "消融实验表明，移除容量操纵损失中的一致性项或多样性项均导致性能显著退化，验证二者的必要性。"
---

# Improving Diffusion Models for Class-imbalanced Training Data via Capacity Manipulation

> [!tip] 核心洞察
> 避免多数类侵占少数类容量的关键在于训练前便为少数类预留低秩容量，并在训练中通过对比通用模型输出与完整模型输出，自适应地分配知识，使通用能力保留在 θ^g，少数类专长固化在 θ^e，最终在不增加推理开销的前提下显著提升不平衡条件下的生成鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过容量操纵改善类别不平衡训练数据下的扩散模型 |
| 英文题名 | Improving Diffusion Models for Class-imbalanced Training Data via Capacity Manipulation |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=wSGle6ag5I) · [GitHub](https://github.com/Feng-Hong/ImbDiff-CM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Capacity Manipulation (CM) |
| Dataset | Imb. CIFAR-100 (IR=100), Imb. CIFAR-10 (IR=100), Imb. CelebA-HQ (IR=100), Imb. ArtBench-10 (IR=100) w/ LoRA fine-tuning |

> [!tip] 效果简介
> - Imb. CIFAR-100 (IR=100) 上，FID↓ 为 7.519，对比 8.309 (OC)，变化 ↓0.790。
> - Imb. CIFAR-10 (IR=100) 上，FID↓ 为 7.727，对比 8.390 (OC)，变化 ↓0.663。
> - Imb. CelebA-HQ (IR=100) 上，Overall FID↓ 为 7.538，对比 7.823 (CBDM)，变化 ↓0.285。

## 概要

**核心问题：类别不平衡训练导致扩散模型容量被多数类垄断。** 在长尾分布数据上训练扩散模型时，多数类样本主导了参数更新方向，迫使少数类知识被挤占至模型的非关键参数中。一旦对模型进行剪枝（移除 L1 范数最小的 10% 参数），少数类的生成损失急剧上升，而多数类几乎不受影响（Fig. 1(b)）——这直接证实了少数类信息被边缘化存储，成为生成质量严重退化的根源。定理 2.1 进一步从理论上证明，多数类主导参数更新的期望比例与类别不均衡度正相关，与类间相似度负相关。

**核心思路：容量操纵（Capacity Manipulation, CM）。** 该方法在训练前通过低秩分解将模型参数显式拆分为两部分：通用容量 $\theta^g$（保留多数类和通用知识）和少数类专属容量 $\theta^e = BA$（低秩矩阵乘积）。训练时引入容量操纵损失 $\mathcal{L}_{\mathrm{CM}}$，由一致性项 $\mathcal{L}_{\mathrm{Con}}$ 和多样性项 $\mathcal{L}_{\mathrm{Div}}$ 组成：对多数类，强制完整模型 $\theta^g \oplus \theta^e$ 的输出与纯通用模型 $\theta^g$ 对齐；对少数类，则鼓励二者产生差异，从而将少数类专长知识引导至预留的 $\theta^e$ 中。推理时只需将两部分参数相加恢复完整模型，无额外计算开销。

**主要结果。** 在 Imb. CIFAR-100（不平衡比 IR=100）上，CM 将 FID 从最优基线 OC 的 8.309 降至 7.519；在 Imb. CIFAR-10、Imb. CelebA-HQ、Imb. ArtBench-10 及大规模数据集 ImageNet-LT 和 iNaturalist 上，CM 在所有指标上一致优于现有方法（DDPM、CBDM、OC、ADA、RS、Focal 等）。消融实验表明，移除一致性项或多样性项均导致性能显著退化，验证了容量分配机制的必要性。CM 还可作为通用框架集成至不同基线方法中，持续提升不平衡条件下的生成鲁棒性。

**方法定位。** CM 属于训练时的容量分配策略，与重采样、重加权、数据增强等现有长尾处理方法正交，可与之协同使用。其核心创新在于将“容量预留”从隐式学习转变为显式的结构化设计，为类别不平衡生成任务提供了一种轻量、即插即用的解决方案。



扩散模型在图像生成领域取得了显著成功，但其训练通常依赖大规模、类别平衡的数据集。现实世界的数据分布往往呈现长尾特性，即多数类拥有充足样本，而少数类样本稀缺。当扩散模型直接在这种类别不平衡数据上训练时，会出现一个根本性问题：**多数类垄断模型容量，导致少数类生成质量严重退化**。

Fig. 1(a) 直观展示了这一现象：在样本比为 100:1 的 Imb. CelebA-HQ 数据集上训练的 DDPM，多数类（Female）生成质量良好，而少数类（Male）的生成结果严重失真。这揭示了不平衡训练的核心矛盾——模型并非缺乏表达能力，而是其容量被多数类信息过度占据。

### 容量支配问题的实证与理论根源

为探究这一退化的深层原因，本文对训练好的 DDPM 模型进行剪枝实验：移除 L1 范数最小的 10% 参数后，计算各类别的相对损失变化 $(L_{pruned} - L_{raw}) / L_{raw}$。如 Fig. 1(b) 所示，少数类的损失变化远大于多数类，表明**少数类信息被挤占至非关键参数中**，对剪枝异常敏感。这一发现直接证实了容量支配（capacity dominance）现象——多数类不仅数量占优，更在参数空间中占据了支配地位。

从理论层面，**定理 2.1** 对这一现象给出了解析刻画。在两类极端不平衡设定下，多数类主导参数更新方向的期望比例为：

$$\Pi_{\mathrm{maj}} = \Phi\left(\frac{(2a-1)\mu\sqrt{2N(1-\cos\angle(\mu_1,\mu_2))}}{2\sigma}\right)$$

其中 $a$ 为多数类样本占比，$N$ 为总样本量，$\mu_1$、$\mu_2$ 为两类梯度均值方向。该定理揭示了三个关键规律：
- **不平衡度正相关**：$a$ 越大，多数类支配的参数比例越高；
- **样本总量放大效应**：$N$ 增大时，支配比例进一步上升，说明大规模训练反而加剧容量失衡；
- **类间相似度负相关**：两类数据分布越相似（$\cos\angle(\mu_1,\mu_2)$ 越大），支配效应越弱。

### 现有方法的局限

针对不平衡生成问题，现有方法主要从三个角度切入：
- **数据层面**：重采样（RS, Mahajan et al., 2018）和自适应增强（ADA, Karras et al., 2020）通过调整样本分布来缓解不平衡，但无法从根本上解决容量分配问题；
- **损失层面**：焦点损失（Focal, Lin et al., 2017b）通过加权强调难样本，CBDM（Qin et al., 2023）和 OC（Zhang et al., 2024）设计了针对扩散模型的不平衡损失函数，但这些方法仅在训练信号上做调整，未触及模型内部容量的结构性分配；
- **架构层面**：缺乏对模型参数空间的显式划分与保护机制。

这些方法的共同盲点是：**它们试图在训练过程中“纠正”不平衡，却未在训练前为少数类预留专属容量**。当多数类样本在梯度更新中占据主导时，少数类信息被迫存储于参数的低敏感区域，最终在生成时无法被有效激活。

### 核心动机

基于上述分析，本文的核心动机在于：**将容量分配从训练中的被动竞争转变为训练前的主动预留**。具体而言，需要解决两个关键问题：
1. 如何在模型架构中为少数类预留专属容量，使其免受多数类梯度侵占；
2. 如何设计训练机制，将少数类知识精确引导至预留容量，同时保持多数类的生成质量不退化。

这一思路的出发点是：模型容量本身是充足的，问题在于分配的失衡。通过低秩分解将参数拆分为通用容量和少数类专属容量，并在训练中施加容量操纵损失，可以在不增加推理开销的前提下，显著提升不平衡条件下的生成鲁棒性。



## 核心方法与创新机理

本研究针对类别不平衡扩散模型训练中**多数类垄断模型容量、挤占少数类信息**这一瓶颈，提出 **Capacity Manipulation (CM)** 方法。其核心创新在于引入了一种**显式的容量预留与分配机制**，将模型参数划分为通用容量与少数类专属容量，并通过自适应损失函数引导知识分流，从而在不增加推理开销的前提下系统性保护少数类生成质量。

### 关键创新点

**1. 低秩容量预留：将模型容量显式拆分为通用与专属两部分**

与现有方法（如 CBDM、OC 等）使用单一参数矩阵 $W$ 进行训练不同，CM 通过低秩分解将任意参数矩阵拆分为两部分：

$$W = W^g + BA = W^g + W^e, \quad \forall W \in \theta$$

其中 $W^g$ 为**通用容量**，负责捕获多数类及跨类共享知识；$W^e = BA$ 为低秩的**少数类专属容量**，其秩 $r$ 由超参数控制，用于存储少数类特有的生成专长（Eq. (1), Sec. 3.1）。这一分解在训练前即完成，从根本上**预留**了少数类的模型容量，防止其在训练过程中被多数类信息侵占。

**2. 容量操纵损失：自适应引导知识分配**

CM 引入容量操纵损失 $\mathcal{L}_{\mathrm{CM}}$，由**一致性项** $\mathcal{L}_{\mathrm{Con}}$ 与**多样性项** $\mathcal{L}_{\mathrm{Div}}$ 组成：

$$\mathcal{L}_{\mathrm{CM}} = \mathcal{L}_{\mathrm{Con}} + \mathcal{L}_{\mathrm{Div}}$$

$$\mathcal{L}_{\mathrm{Con}} = \omega_{\mathrm{Con}}^y \mathbb{E}_t \| \epsilon_{\theta^g \oplus \theta^e} - \epsilon_{\theta^g} \|^2, \quad \mathcal{L}_{\mathrm{Div}} = -\omega_{\mathrm{Div}}^y \mathbb{E}_t \| \epsilon_{\theta^g \oplus \theta^e} - \epsilon_{\theta^g} \|^2$$

其中类别权重根据样本量自适应分配：$\omega_{\mathrm{Con}}^y \propto N_y$（多数类权重高，强制完整模型与通用模型输出一致），$\omega_{\mathrm{Div}}^y \propto 1/N_y$（少数类权重高，鼓励完整模型与通用模型输出产生差异）。这一设计使得**多数类知识自然保留在 $\theta^g$ 中，而少数类专长被“推入”预留的 $\theta^e$ 容量**（Eq. (2)–(3), Sec. 3.2）。

**3. 无额外推理开销的参数合并**

推理时，CM 将 $\theta^g$ 与 $\theta^e$ 显式相加合并为单一参数矩阵，以标准扩散模型流程进行采样，**不增加任何推理延迟或模型容量**（Sec. 3.2 Inference 段落）。这一设计使 CM 在保持部署高效性的同时，实现了对少数类生成质量的显著提升。

### 与现有方法的核心差异

| 维度 | 现有方法（DDPM, CBDM, OC 等） | CM 方法 |
|------|-------------------------------|---------|
| 参数结构 | 单一参数矩阵 $W$ | $W = W^g + BA$（通用 + 低秩专属） |
| 容量分配 | 隐式，多数类自然垄断 | 显式预留，训练前即划分 |
| 损失函数 | 仅基础扩散损失 $\mathcal{L}_{\mathrm{base}}$ | $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{base}} + \lambda \mathcal{L}_{\mathrm{CM}}$ |
| 少数类保护机制 | 依赖重采样、重加权等间接策略 | 通过容量操纵损失直接引导知识存储位置 |
| 推理开销 | 标准 | 标准（参数合并后无额外开销） |

消融实验证实了上述创新设计的必要性：移除一致性损失 $\mathcal{L}_{\mathrm{Con}}$ 导致 Imb. CIFAR-100 (IR=100) 上 FID 从 7.519 升至 8.412；移除多样性损失 $\mathcal{L}_{\mathrm{Div}}$ 使 FID 升至 8.073（Table 7 Right）。低秩分量 $\theta^e$ 的秩比例约为 0.1 时 FID 最低，表明**少量预留容量即可有效保护少数类学习**（Fig. 4(c)）。此外，CM 可作为通用框架集成至 CBDM、OC、ADA 等多种基线方法，持续提升其在不平衡条件下的生成性能（Fig. 4(a)）。



![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/003_Figure_2.jpg]]
*Figure 2: (a,b) An overview of our method, CM. (a) An illustration of the capacity reservation part of CM. (b) An illustration of how CM allocates the corresponding knowledge to the reserved model capacity during training. (c) Many/Medium/Few split performance on Imb. CIFAR100 with imbalance ratio $\mathrm { I R }$ = 1 0 0 , where Many/Medium/Few represents the top, middle, and bottom thirds of classes sorted by sample number in descending order. CM significantly improves minority performance without sacrificing the performance of majorities*

**核心瓶颈与设计动机**  
在类别不平衡的扩散模型训练中，多数类垄断了模型容量，迫使少数类信息被挤占至非关键参数中，导致少数类生成质量严重下降。直接证据来自 Fig. 1(b)：对在 Imb. CIFAR-100 (IR=100) 上训练的 DDPM 剪枝 10% L1 范数最小的参数后，少数类的相对损失变化远大于多数类，表明少数类知识被压缩至非关键容量中。Theorem 2.1 进一步从理论上证明，多数类主导的参数更新比例与不平衡程度正相关，形成“容量支配”问题。

**设计哲学：容量预留与知识分配**  
CM 的核心思路是：在训练前显式为少数类预留低秩容量，并在训练中通过容量操纵损失引导知识分配，使通用能力保留在通用容量中、少数类专长固化在预留容量中，最终在不增加推理开销的前提下提升不平衡条件下的生成鲁棒性。

**Pipeline 总览**  
整体流程由四个模块串联构成（见 Fig. 2(a,b)）：

1. **低秩容量预留** — 将模型参数矩阵 $W$ 分解为通用部分 $W^g$ 和低秩的少数类专长部分 $W^e = BA$：
   $$W = W^g + BA = W^g + W^e, \quad \forall W \in \theta$$
   其中 $B \in \mathbb{R}^{d \times r}$、$A \in \mathbb{R}^{r \times k}$，秩 $r$ 控制为少数类预留的容量比例。这一分解类似于 LoRA 的低秩适配思想，但目的不同：LoRA 旨在微调，CM 旨在容量划分。

2. **容量操纵损失** — 训练时计算两个互补项，引导知识分配：
   - **一致性项** $\mathcal{L}_{\mathrm{Con}}$：对多数类施加，鼓励完整模型 $\epsilon_{\theta^g \oplus \theta^e}$ 与通用模型 $\epsilon_{\theta^g}$ 输出一致，使多数类知识保留在 $\theta^g$ 中。
   - **多样性项** $\mathcal{L}_{\mathrm{Div}}$：对少数类施加，鼓励完整模型与通用模型输出差异，使少数类专长固化在 $\theta^e$ 中。
   
   两项通过类别自适应权重控制：
   $$\omega_{\mathrm{Con}}^y = \frac{C N_y}{\sum_{c=1}^C N_c}, \quad \omega_{\mathrm{Div}}^y = \frac{C}{N_y \sum_{c=1}^C \frac{1}{N_c}}$$
   一致性权重正比于类别样本量，多样性权重反比于类别样本量，平衡数据下二者相等。

3. **联合优化** — 总损失为基础扩散损失与容量操纵损失的加权和：
   $$\min_{\theta} \mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{base}}(\mathcal{D}, \theta) + \lambda \sum_{(x,y)\in\mathcal{D}} \frac{1}{N} \mathcal{L}_{\mathrm{CM}}(x,y,\theta^g,\theta^e)$$
   同时更新 $\theta^g$ 和 $\theta^e$，$\lambda$ 控制容量操纵损失的强度。

4. **参数合并推理** — 推理时将 $\theta^g$ 与 $\theta^e$ 显式相加恢复完整参数 $\theta = \theta^g \oplus \theta^e$，以标准扩散模型流程采样，不增加模型容量或推理延迟。

**输入输出流**  
- **输入**：不平衡训练集 $\mathcal{D}$，包含图像 $x$ 及其类别标签 $y$，各类别样本量 $N_y$ 差异显著。
- **输出**：训练后的完整模型参数 $\theta = \theta^g \oplus \theta^e$，其中 $\theta^g$ 承载通用/多数类知识，$\theta^e$ 承载少数类专长。
- **推理**：以合并后的 $\theta$ 进行标准扩散采样，生成各类别图像，少数类生成质量显著提升而不牺牲多数类性能。

**关键设计决策**  
- 秩比例 $r / \min(d,k)$ 在约 0.1 时 FID 最低（Fig. 4(c)），表明少量预留容量即可有效保护少数类。
- $\lambda$ 在 1.0 附近性能最优，且在 [0.5, 1.5] 范围内均优于最优基线 OC（Fig. 4(b)）。
- CM 可作为通用框架集成至不同基线（CBDM、OC、ADA 等），使用对应目标函数作为 $\mathcal{L}_{\mathrm{base}}$ 即可持续提升不平衡生成性能（Fig. 4(a)）。



### 容量预留：低秩参数分解

CM 的核心操作是在训练前将扩散模型的参数矩阵显式拆分为通用容量与少数类专属容量。对于网络中任意参数矩阵 $W \in \mathbb{R}^{d \times k}$，分解形式为：

$$W = W^g + B A = W^g + W^e, \quad \forall W \in \theta$$

其中：
- **$W^g$**：通用容量（generalized part），负责捕获多数类知识及跨类共享的通用表示；
- **$W^e = BA$**：少数类专长容量（expertise part），$B \in \mathbb{R}^{d \times r}$、$A \in \mathbb{R}^{r \times k}$ 为低秩矩阵，秩 $r \ll \min(d, k)$ 控制为少数类预留的容量大小。

这一分解的动机源于定理2.1的启示：在类别不平衡训练中，多数类主导参数更新的期望占比 $\Pi_{\mathrm{maj}}$ 与不平衡程度正相关。通过低秩分解引入秩比率 $\alpha_r$，可将该占比的上界收紧为：

$$\Pi_{\mathrm{maj}} < \Phi\left(\frac{(1-\alpha_r)\mu\sqrt{2N(1-\cos\angle(\mu_1,\mu_2))}}{2\sigma}\right)$$

这意味着预留的容量 $\theta^e$ 在训练初期即被物理隔离，多数类的梯度更新难以侵占这部分参数空间。

### 容量操纵损失：知识分配机制

仅有容量预留并不足以保证少数类知识被正确引导至 $\theta^e$。CM 通过容量操纵损失 $\mathcal{L}_{\mathrm{CM}}$ 实现训练过程中的知识自适应分配，该损失由一致性项与多样性项构成：

$$\mathcal{L}_{\mathrm{CM}} = \mathcal{L}_{\mathrm{Con}} + \mathcal{L}_{\mathrm{Div}}$$

**一致性项** $\mathcal{L}_{\mathrm{Con}}$ 约束多数类样本，迫使完整模型输出 $\epsilon_{\theta^g \oplus \theta^e}$ 与通用模型输出 $\epsilon_{\theta^g}$ 保持一致：

$$\mathcal{L}_{\mathrm{Con}} = \omega_{\mathrm{Con}}^y \, \mathbb{E}_t \left\| \epsilon_{\theta^g \oplus \theta^e}(x_t, t, y) - \epsilon_{\theta^g}(x_t, t, y) \right\|^2$$

**多样性项** $\mathcal{L}_{\mathrm{Div}}$ 则鼓励少数类样本在 $\theta^e$ 中存储差异化信息，使完整模型输出偏离通用模型：

$$\mathcal{L}_{\mathrm{Div}} = -\omega_{\mathrm{Div}}^y \, \mathbb{E}_t \left\| \epsilon_{\theta^g \oplus \theta^e}(x_t, t, y) - \epsilon_{\theta^g}(x_t, t, y) \right\|^2$$

两项的类别权重根据样本量自适应分配，实现“多数类对齐、少数类发散”的差异化引导：

$$\omega_{\mathrm{Con}}^y = \frac{C N_y}{\sum_{c=1}^C N_c}, \quad \omega_{\mathrm{Div}}^y = \frac{C}{N_y \sum_{c=1}^C \frac{1}{N_c}}$$

当数据完全平衡（$N_1 = N_2 = \cdots = N_C$）时，$\omega_{\mathrm{Con}}^y = \omega_{\mathrm{Div}}^y = 1$，两项互为抵消；在不平衡条件下，多数类（$N_y$ 大）获得高一致性权重，少数类（$N_y$ 小）获得高多样性权重。

### 联合优化与推理

训练时，CM 联合优化基础扩散损失与容量操纵损失：

$$\min_{\theta} \mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{base}}(\mathcal{D}, \theta) + \lambda \sum_{(x,y)\in\mathcal{D}} \frac{1}{N} \mathcal{L}_{\mathrm{CM}}(x, y, \theta^g, \theta^e)$$

其中 $\lambda$ 为容量操纵损失的权重，消融实验表明 $\lambda \approx 1.0$ 时性能最优（Fig. 4(b)）。

推理时，将 $\theta^g$ 与 $\theta^e$ 显式相加合并为完整参数 $\theta = \theta^g \oplus \theta^e$，以标准扩散模型采样流程生成，不引入任何额外推理延迟或参数量增长。

### 模块间因果链路

上述三个模块形成一条完整的因果链：
1. **低秩容量预留**在参数空间中物理隔离出少数类专属子空间，阻断多数类梯度对这部分容量的侵占；
2. **容量操纵损失**通过对比 $\theta^g \oplus \theta^e$ 与 $\theta^g$ 的输出差异，将少数类专长知识“推入”预留的 $\theta^e$，同时将通用知识“保留”在 $\theta^g$ 中；
3. **参数合并推理**使预留容量在部署时无缝融入完整模型，实现零开销的少数类生成质量提升。

消融实验验证了这一因果链的必要性：移除 $\mathcal{L}_{\mathrm{Con}}$ 使 Imb. CIFAR-100 (IR=100) 的 FID 从 7.519 升至 8.412；移除 $\mathcal{L}_{\mathrm{Div}}$ 使 FID 升至 8.073（Table 7 Right），表明一致性约束与多样性鼓励缺一不可。



## 实验与关键发现

### 核心瓶颈与容量支配的实证动机

类别不平衡扩散模型训练的根本瓶颈在于**多数类垄断了模型容量**。在 Imb. CelebA-HQ (IR=100) 上，DDPM 对多数类（Female）生成质量良好，但少数类（Male）严重退化（Fig. 1(a)）。更直接的证据来自剪枝实验：对 Imb. CIFAR-100 (IR=100) 上训练的 DDPM 剪去 10% 的 L1 范数最小参数后，少数类的相对损失变化远大于多数类（Fig. 1(b)），表明**少数类信息被挤占至非关键容量中**，一旦剪枝便立即崩溃。定理 2.1 进一步从理论上证明，在两类极端不平衡下，多数类主导参数更新的期望占比 $\Pi_{\mathrm{maj}}$ 与不均衡度 $a$ 和样本总量 $N$ 正相关，与类间相似度负相关，为容量失衡提供了解析表达。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/002_Figure_1.jpg]]
*Figure 1: (a) Real images from Imb. CelebA (Imbalance Ratio IR = 100) and generated images from DDPM and our method. Images are randomly sampled. (b) Relative per-class loss change, defined as ( $\mathcal { L } _ { p r u n e d } ^ { c } - \mathcal { L } _ { r a w } ^ { c }$ ) / $\mathcal { L } _ { r a w } ^ { c }$ , for a DDPM model trained on Imb. CIFAR-100 (IR = 100) when 10% of its parameters with the smallest L1-Norm are pruned. Raw losses and absolute loss changes are provided in Figs. G.1 and G.2

### 主实验结果

CM 在多个数据集、不平衡比率和评估指标上一致优于现有方法。

**Imb. CIFAR-10/100**（Table 2）：在 IR=100 的 Imb. CIFAR-100 上，CM 的 FID 降至 **7.519**，相较最优基线 OC 的 8.309 降低了 0.790；在 Imb. CIFAR-10 上 FID 从 8.390 降至 **7.727**。KID、Recall、IS 等指标同样全面领先。IR=50 设置下优势保持。按 Many/Medium/Few 分割的 FID（Table 3）显示，CM 在三个子集上均取得最优，其中 Few 类 FID 在 CIFAR-100 上为 18.729，显著优于 OC（24.707）和 CBDM（24.463），验证了容量预留对少数类的保护效果。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/005_Table_2.jpg]]
*Table 2: FIDs ( ), KIDs ( ), Recalls ( ), and ISs ( ) of CM and various baseline methods on Imb. CIFAR-10 and Imb. CIFAR-100. Results for imbalance ratios IR = {100, 50} are shown side-byside. Best and second-best results are highlighted. Results with Mean Std can be found in Tab. G.1*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/006_Table_3.jpg]]
*Table 3: Per-split FIDs (↓) of CM and baselines on Imb. CIFAR-10 (IR = 100) and Imb. CIFAR-100 (IR = 100) shown. Many, Medium, and Few are the three splits based on training imbalancedness. Best and second-best results are highlighted. Results with Mean±Std can be found in Tab. G.4*

**Imb. CelebA-HQ**（Table 4）：在 IR=100 的二分类（Female/Male）设置下，CM 的 Overall FID 为 **7.538**，优于 CBDM（7.823）和 OC（8.051），且两个类别的 per-class FID 均取得最优。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/007_Table_4.jpg]]
*Table 4: FIDs (↓), KIDs (↓), and per-class FIDs (↓) of CM and baselines on Imb. CelebA-HQ with imbalance ratios $\mathrm { I R } = \{$ 1 0 0 , 5 0 $\}$ shown side-by-side. Female and Male are the two classes. Best and second-best results are highlighted. Results with Mean±Std can be found in Tab. G.2*

**大规模长尾数据集**（Table 5）：在 ImageNet-LT 和 iNaturalist 的 32×32 和 64×64 分辨率上，CM 在 FID 和 KID 上均取得最佳，证明了方法在大规模真实长尾分布下的鲁棒性。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/008_Table_5.jpg]]
*Table 5: FIDs (↓) and KIDs (↓) on ImageNet-LT and iNaturalist at 3 2 $\times$ 3 2 and 64 64 resolutions*

**LoRA 微调场景**（Table 6）：在 Imb. ArtBench-10 (IR=100) 上使用 LoRA 微调 Stable Diffusion，CM 的 FID 为 **22.776**，相较 OC（24.559）降低 1.783。定性可视化（Fig. 3）显示，对尾类“Realism”，CM 生成结果在多样性和风格贴近度上显著优于 DDPM。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/009_Table_6.jpg]]
*Table 6: FIDs (↓), KIDs (↓), Recalls (↑), and ISs (↑) of CM and various baselines on Imb. ArtBench-10 with $\mathrm { I R } = \{$ 1 0 0 , 5 0 $\}$ shown, using LoRA to fine-tune Stable Diffusion. Best and second-best results are highlighted. Full results with Mean±Std can be found in Tab. G.3*

### 消融实验

**容量操纵损失的必要性**（Table 7 Right）：在 Imb. CIFAR-100 (IR=100) 上，移除一致性损失 $\mathcal{L}_{\mathrm{Con}}$ 导致 FID 从 7.519 升至 8.412，移除多样性损失 $\mathcal{L}_{\mathrm{Div}}$ 使 FID 升至 8.073，验证了二者的必要性——一致性项确保多数类知识留在 $\theta^g$，多样性项引导少数类专长进入 $\theta^e$。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/015_Table_7.jpg]]
*Table 7: (Left) Per-split FIDs and overall FIDs (↓) of DDPM, CM (θg), and CM on Imb. CIFAR-100 with imbalance ratio IR = 100. (Right) FIDs (↓), KIDs (↓), Recalls (↑), and ISs (↑) on Imb. CIFAR-100 with imbalance ratio IR = 100. The last two rows show the results of CM after removing $\mathcal { L } _ { \mathrm { C o n } }$ and ${ \mathcal { L } } _ { \mathrm { D i v } }$ , respectively. Full results with Mean±Std can be found in Tables G.5 and G.6

**知识分配验证**（Table 7 Left）：单独使用通用容量 $\theta^g$（即 CM($\theta^g$)）在 Many 和 Medium 类上表现良好，但在 Few 类上 FID 升至 27.195（完整 CM 为 18.729），直接证明**少数类专长确实被分配至预留容量 $\theta^e$ 中**。

**超参数敏感性**：容量操纵损失权重 $\lambda$ 在 1.0 附近 FID 最优，且在 [0.5, 1.5] 范围内均优于基线 OC（Fig. 4(b)）。低秩分量 $\theta^e$ 的秩比例约为 0.1 时 FID 最低（Fig. 4(c)），表明**少量预留容量即可有效保护少数类**。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/014_Figure_4.jpg]]
*Figure 4: (a) The performance of CM when integrated with baselines. (b) Ablation study on the hyperparameter λ in Eq. (4). (c) Ablation study on the rank r. (d) Ablation study on various UNet configurations. All experiments are conducted on Imb. CIFAR-100 with IR = 100. In (b) and (c), we use OC as a reference because it shows the best overall performance among the baselines*

**通用框架集成**（Fig. 4(a)）：将 CM 集成至 CBDM、OC、ADA、RS、Focal 等不同基线后，所有方法的 FID 均获得一致改善，验证了 CM 作为通用框架的正交性与可插拔性。

**不同 UNet 配置**（Fig. 4(d)）：在三种 UNet 深度配置下，CM 均一致优于 DDPM、CBDM 和 OC，表明方法对网络结构具有鲁棒性。

### 与低秩变体的对比

Table 1 显示，简单对 CBDM 施加低秩分解（$\theta = \theta^g \oplus \theta^e$）或标准 LoRA 并不能有效解决不平衡问题（CIFAR-100 上 FID 分别为 9.855 和 10.564），而 CM 通过容量操纵损失引导知识分配，将 FID 降至 7.519，说明**仅靠低秩结构不足以保护少数类，容量分配策略是关键**。与 MoE 风格的 Group-Expert LoRA 对比同样验证了这一结论（FID: CM 7.519 vs. MoE-style 10.06）。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/004_Table_1.jpg]]
*Table 1: FID comparison with baselines and low-rank variants*

### 局限性与失败模式

在绝对少数样本数量极低时（例如个位数样本），预留的容量 $\theta^e$ 仍可能因缺乏足够数据而难以学到有意义的表示，限制了生成质量的提升。当前验证集中于图像生成扩散模型，尚未在其他数据模态（如视频、3D 数据）上进行广泛评估。

### 补充图表

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/016_Table_8.jpg]]

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_wSGle6ag5I/figures/017_Table_9.jpg]]
*Table 9: Table E.1: Conceptual comparison of CM with related paradigms*



## 定位与知识库关联

### 1. 问题定位：类别不平衡下的扩散模型容量支配

在扩散生成模型中，类别不平衡训练导致的根本瓶颈并非简单的数据稀缺，而是**多数类对模型容量的系统性侵占**。标准训练下，多数类凭借样本量优势主导参数更新方向，将少数类信息挤占至非关键容量中。这一现象在两类极端不平衡设定下得到理论刻画：定理 2.1 给出了多数类主导参数矩阵的期望占比

$$\Pi_{\mathrm{maj}} = \Phi\left(\frac{(2a-1)\mu\sqrt{2N(1-\cos\angle(\mu_1,\mu_2))}}{2\sigma}\right)$$

其中 $a$ 为不均衡度，$N$ 为样本总量，$\mu$ 和 $\sigma$ 分别为类条件分布的均值和标准差。该式表明容量失衡与不均衡程度正相关，与类间相似度负相关。实证上，Fig. 1(b) 的剪枝实验直接验证了这一论断：对在 Imb. CIFAR-100（IR=100）上训练的 DDPM 剪除 10% L1 范数最小的参数后，少数类的相对损失变化远大于多数类，说明其信息被挤占至非关键容量中。

### 2. 方法谱系：从重采样到容量预留的范式演进

现有应对不平衡生成的方法可归为三类范式：

**数据层面方法**：重采样（RS, Mahajan et al., 2018）和自适应数据增强（ADA, Karras et al., 2020）通过调整训练分布缓解不平衡，但无法从根本上阻止多数类在参数更新中的支配地位。当不平衡比极高时，少数类样本的有限多样性限制了此类方法的有效性。

**损失层面方法**：焦点损失（Focal, Lin et al., 2017b）通过对难样本加权来重新分配学习信号，但仅作用于损失权重，未改变容量分配的结构性失衡。

**扩散模型专用方法**：CBDM（Qin et al., 2023）和 OC（Zhang et al., 2024）分别从条件增强和观测中心化的角度改进扩散模型在不平衡数据上的训练。这些方法在 Imb. CIFAR-100（IR=100）上分别达到 FID 10.051 和 8.309（Table 2），较 DDPM 有显著提升，但本质上仍是在共享容量框架内优化，未能显式保护少数类的参数空间。

CM 的核心范式转变在于**从“事后补偿”转向“事前预留”**：通过低秩分解将参数拆分为通用部分 $W^g$ 和少数类专长部分 $W^e = BA$（Eq. (1)），在训练前便为少数类分配专属容量，并通过容量操纵损失引导知识分配。这一设计使得 CM 可作为一个**通用框架**集成至各类基线方法：Fig. 4(a) 显示，将 CM 与 DDPM、CBDM、OC、ADA 等结合后，FID 一致下降，验证了容量预留策略的正交性和普适性。

### 3. 与低秩微调方法的关系

CM 的参数分解形式与 LoRA 相似，但二者在动机和机制上存在本质差异。LoRA 旨在高效微调预训练模型，其低秩分量学习的是任务相关的增量知识；CM 的低秩分量 $W^e$ 则专门用于承载少数类专长，且通过容量操纵损失中的一致性项 $L_{\mathrm{Con}}$ 和多样性项 $L_{\mathrm{Div}}$ 进行显式引导。Table 1 的对比实验直接验证了这一差异：CBDM 的朴素低秩变体（$\theta = \theta^g \oplus \theta^e$）和 LoRA 变体在 Imb. CIFAR-100 上的 FID 分别为 10.051 和 9.858，远逊于 CM 的 7.519，说明单纯的参数分解无法解决容量支配问题，关键在于配套的容量操纵损失。

此外，CM 的 LoRA 微调扩展（Sec. 3.3）将预训练权重 $W^f$ 冻结，同时引入通用低秩分量 $B^g A^g$ 和少数类专长低秩分量 $B^e A^e$，在保留 LoRA 高效性的同时实现了容量操纵。在 Imb. ArtBench-10 上微调 Stable Diffusion 时，CM 的 FID 降至 22.776，优于 OC 的 24.559（Table 6）。

### 4. 适用边界与局限

**适用边界**：
- CM 的核心假设是模型容量存在冗余，且少数类知识可被压缩至低秩子空间中。消融实验（Fig. 4(c)）表明，$W^e$ 的秩比例约为 0.1 时 FID 最低，验证了少量预留容量即可有效保护少数类。
- 容量操纵损失权重 $\lambda$ 在 $[0.5, 1.5]$ 范围内均优于基线 OC（Fig. 4(b)），表明方法对超参数具有较好的鲁棒性。
- 当前验证覆盖了 CIFAR-10/100、CelebA-HQ、ImageNet-LT、iNaturalist 和 ArtBench-10 等图像数据集，以及从 32×32 到 256×256 的分辨率范围。

**已知局限**：
- 在绝对少数样本数极低时（如个位数样本），预留容量 $W^e$ 仍可能因缺乏足够数据而难以学到有意义的表示。这是容量预留策略的固有边界——预留空间无法替代数据本身的信息量。
- 当前验证集中于图像生成扩散模型，尚未在视频、3D 数据等其他模态上进行广泛评估。

### 5. 开放问题

1. **跨模态迁移**：容量操纵策略在视频、3D 等不同数据模态中的适配性与有效性值得探索。这些模态的参数冗余特性可能与图像模型不同，低秩预留的秩比例需要重新校准。

2. **极端少样本场景**：对于近乎零样本的尾部类别，如何结合元学习或数据增强机制，使预留容量仍能发挥作用，是一个有待研究的路径。

3. **判别式任务的推广**：容量操纵思想在长尾识别任务上的初步实验已显现积极信号，但是否需要进一步的网络结构适配和理论分析，仍需系统验证。判别式任务中“容量”的定义可能与生成式任务不同，需要重新形式化。

4. **理论深化**：定理 2.1 给出了两类设定下的容量支配比例，但多类场景下的理论分析尚不完整，尤其是类别间语义层次结构对容量分配的影响值得进一步建模。



## 原文 PDF

![[paperPDFs/ICLR_2026/Improving_Diffusion_Models_for_Class_imbalanced_Training_Data_via_Capacity_Manipulation.pdf]]
