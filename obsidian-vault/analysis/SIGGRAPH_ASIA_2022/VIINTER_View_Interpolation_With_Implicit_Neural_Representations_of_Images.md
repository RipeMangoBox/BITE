---
title: "VIINTER: View Interpolation With Implicit Neural Representations of Images"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/VIINTER_View_Interpolation_With_Implicit_Neural_Representations_of_Images.pdf
project_link: null
code_link: "https://github.com/AugmentariumLab/VIINTER"
aliases:
- VIINTER
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 对每个图像的隐编码施加单位L1范数正则化，使所有编码处于统一尺度，从而其线性组合能被解码器合理解析；同时引入基于CLIP的感知插值损失，进一步约束插值结果与源图像的语义一致性。
primary_logic: 通过强制隐编码的L1范数归一化，可以消除编码间的尺度差异，使得在编码空间中的线性插值对应于视觉上平滑的视角过渡；无需依赖任何3D信息或像素对应，仅凭2D图像INR的编码插值即可实现视角合成。
claims:
- 不加正则化时，编码插值完全失效。
- 采用L1范数归一化后，插值质量大幅提升。
- 基于CLIP的插值损失显著优于VGG损失，能有效减少插值伪影。
- Stanford 4D Light Fields (Novel Views) 上 SSIM = 0.975
---

# VIINTER: View Interpolation With Implicit Neural Representations of Images

> [!tip] 核心洞察
> 通过强制隐编码的L1范数归一化，可以消除编码间的尺度差异，使得在编码空间中的线性插值对应于视觉上平滑的视角过渡；无需依赖任何3D信息或像素对应，仅凭2D图像INR的编码插值即可实现视角合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | VIINTER：基于图像隐式神经表示的视角插值 |
| 英文题名 | VIINTER: View Interpolation With Implicit Neural Representations of Images |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2211.00722) · [Code](https://github.com/AugmentariumLab/VIINTER) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | VIINTER |
| Dataset | Stanford 4D Light Fields |

> [!tip] 效果简介
> - Stanford 4D Light Fields (Novel Views) 上，SSIM 0.975 vs 0.944 (LFN) (+0.031)。

## 概要

**问题**：多视角图像插值通常依赖三维重建或相机位姿。若仅对每个视角独立训练图像的隐式神经表示（INR），各视角的隐编码在优化过程中会获得不同尺度，导致编码间的线性插值完全失效，无法生成有意义的过渡视图。

**方法**：提出 VIINTER，在无任何三维信息、相机位姿或像素对应的条件下实现视角插值。核心做法是：为每张图像分配一个可学习的隐编码，与坐标拼接后送入 SIREN 网络重建 RGB；训练时强制每个编码满足单位 L1 范数约束，消除尺度差异；同时引入基于 CLIP 的感知插值损失，约束插值结果与源图像在语义特征空间中的线性一致性。

**主要结果**：在 Stanford 4D Light Fields 上，VIINTER 的插值视图 SSIM 达 0.975，显著优于光场网络 LFN（0.944）。消融实验表明，L1 范数归一化是插值能力的关键（无控制时 SSIM 仅 0.595），CLIP 插值损失有效消除伪影，编码长度 M=128 达到性能峰值。

**方法定位**：区别于 NeRF 等依赖三维重建与相机位姿的视角合成方法，VIINTER 完全在二维 INR 的隐编码空间中完成插值，属于无三维先验的图像驱动视角过渡方案。

## 核心方法与创新机理

### 问题背景与核心瓶颈

视角插值（View Interpolation）的传统路径依赖于显式的三维重建、相机位姿估计或像素级对应关系（如NeRF、LFN等）。VIINTER探索了一条截然不同的路线：仅利用二维图像的隐式神经表示（INR），在不使用任何三维结构、相机位姿或像素对应信息的条件下实现视角间的平滑过渡。

然而，直接将多图像INR框架应用于视角插值面临一个**关键瓶颈**：在标准的联合训练过程中，每张图像对应的隐编码向量 $z_n$ 在优化时各自获得不同的尺度（magnitude），导致编码空间中的线性插值 $z_{Inter} = (1-t) \cdot z_i + t \cdot z_j$ 无法被解码器 $\mathcal{F}$ 合理解析。如Figure 2中“No Control”条件所示，虽然各图像在已知编码下的重建质量正常，但插值编码产生的图像完全失效——这一现象的根源在于解码器在训练期间从未见过处于“中间尺度”的编码，因此无法将其映射为有意义的RGB值。

### 核心洞察

VIINTER的核心洞察简洁而深刻：**通过强制所有隐编码具有统一的L1范数，可以消除编码间的尺度差异，使得编码空间中的线性插值对应于视觉上平滑的视角过渡。** 这一发现意味着，无需任何三维先验，仅凭二维INR的编码插值即可实现视角合成——编码空间本身被赋予了“视角流形”的结构。

### 方法框架与模块顺序

VIINTER的完整管线由以下模块按因果顺序构成：

1. **SIREN主干网络 $\mathcal{F}$**：以像素坐标 $(p_x, p_y)$ 和图像条件编码 $z_n$ 为输入，输出该图像中对应像素的RGB值 $p_{c|n}$。SIREN采用周期激活函数，天然适合表示高频图像细节。
2. **逐图像隐编码 $Z_N$**：为训练集中的每张图像随机初始化一个可学习的身份编码向量 $z_n \in \mathbb{R}^M$，该编码作为条件输入与坐标拼接后馈入 $\mathcal{F}$。
3. **L1范数归一化（Direct Regularization）**：在每次训练迭代中，将所有编码强制缩放为单位L1范数：$z = \frac{z}{\|z\|_1}, \forall z \in Z_N$。这是方法的核心控制旋钮。
4. **CLIP特征提取器 $\mathcal{E}$**：预训练的CLIP网络作为固定的感知特征提取器，用于计算插值损失。
5. **线性编码插值**：在推理阶段，对任意两个训练图像的编码进行线性加权组合 $z_{Inter} = (1-t) \cdot z_i + t \cdot z_j$，生成新视角的隐编码。

### 关键公式与变量含义

**单图像INR映射**（训练基础单元）：
$$\mathcal{F}(p_x, p_y) = p_c$$
INR将像素坐标直接映射为RGB值，通过最小化重建误差 $L_{SingleRecon} = \sum_{\mathcal{P}} \|p_c - p_c^{GT}\|^2$ 来拟合单张图像。

**多图像条件INR映射**（核心框架）：
$$\mathcal{F}(p_x, p_y \mid z_n) = p_{c|n}$$
其中 $z_n$ 是第 $n$ 张图像的身份编码。所有图像共享同一个网络 $\mathcal{F}$，通过不同的 $z_n$ 区分各图像的像素分布。

**多图像重建损失**：
$$L_{Recon} = \sum_{n} \sum_{p} \| p_{c|n} - p_{c|n}^{GT} \|^2$$
该损失仅约束已知图像在各自编码下的重建精度，不涉及任何插值监督。

**单位L1范数约束**（核心创新）：
$$z = \frac{z}{\|z\|_1}, \quad \forall z \in Z_N$$
这一操作在每次前向传播前执行，将所有编码投影到L1范数为1的超球面上。选择 $p=1$ 而非 $p=2$（Euclidean范数）的关键原因在于：L1范数在保持编码稀疏性的同时，能更好地维持插值路径上的编码分布一致性。实验证据（Table 1 Top）表明，$p=1$ 时插值视图的SSIM达到0.958/PSNR 32.39，显著优于 $p=2$ 的0.937/29.15和无控制的0.595/11.02。

**CLIP引导的插值损失**（间接正则化）：
$$L_{Inter} = \| \mathcal{E}(I_{Inter}) - [(1-t) \cdot \mathcal{E}(I_i) + t \cdot \mathcal{E}(I_j)] \|^2$$
其中 $I_{Inter} = \mathcal{F}(\cdot \mid z_{Inter})$ 是插值编码生成的图像，$\mathcal{E}$ 是CLIP图像编码器。该损失鼓励插值输出图像在CLIP语义特征空间中接近源图像特征的线性插值，从而约束插值路径上的语义一致性。

**总训练损失**：
$$L_{Total} = L_{Recon} + \lambda \cdot L_{Inter}$$
其中 $\lambda$ 为平衡系数。训练过程中，网络权重 $\theta_{\mathcal{F}}$ 和所有隐编码 $Z_N$ 联合优化。

### 训练与推理路径

**训练阶段**：
1. 从训练集中采样两张图像 $I_i$ 和 $I_j$，获取其对应的隐编码 $z_i$ 和 $z_j$。
2. 对 $z_i$ 和 $z_j$ 施加L1范数归一化。
3. 随机采样插值系数 $t \sim U(0,1)$，计算插值编码 $z_{Inter} = (1-t) \cdot z_i + t \cdot z_j$。
4. 分别用 $z_i$、$z_j$ 和 $z_{Inter}$ 查询网络 $\mathcal{F}$，获得三张图像的重建/生成结果。
5. 计算 $L_{Recon}$（仅对 $z_i$ 和 $z_j$ 对应的已知视图）和 $L_{Inter}$（对 $z_{Inter}$ 对应的插值视图），反向传播更新 $\theta_{\mathcal{F}}$ 和 $Z_N$。

**推理阶段**：
1. 选定两个已知视角的编码 $z_i$ 和 $z_j$（已在训练中归一化）。
2. 按所需步长采样 $t \in [0,1]$，计算插值编码序列。
3. 将每个插值编码馈入冻结的网络 $\mathcal{F}$，渲染对应视角的图像。

值得注意的是，VIINTER支持**多步插值**（Figure 8）：在生成两个插值编码后，可对它们再次进行线性插值，从而获得更密集的视角序列，表明编码空间确实形成了连续的视角流形。

![[assets/figures/papers/paper_list_l98_https_arxiv_org_abs_2211_00722/figures/010_Figure_8.jpg]]
*Figure 8: Interpolated Between Interpolated Latent Codes. After interpolating the latent codes for two training views (Column 1 and 4), we can further interpolate between those interpolated latent codes (Column 2 and 3). This additional step effectively leads to more viewpoints that can be expressed by our INR*

### 模块间的因果关系

整个方法的核心因果链可概括为：

**L1归一化 → 编码尺度统一 → 线性插值可解码 → 视角平滑过渡**

具体而言：
- **L1归一化**消除了训练过程中编码自由缩放的可能性，所有编码被约束在同一超球面上，使得任意两个编码的线性组合仍在解码器“熟悉”的分布范围内。
- **编码尺度统一**是插值有效性的必要条件：若无此约束，$z_i$ 和 $z_j$ 可能具有截然不同的范数，其线性组合会落入训练分布之外的“空洞”区域，导致解码器输出噪声。
- **CLIP插值损失**作为补充约束，在语义层面进一步引导插值路径，减少伪影。Figure 4表明，CLIP特征提取器相比VGG-based感知损失能更有效地消除插值伪影，而不会引入过度平滑。
- **编码长度 $M$** 是一个关键的超参数：Table 1（Bottom）显示 $M=128$ 时插值性能达到峰值（SSIM 0.958），$M=16$ 时性能急剧下降至0.891，而 $M=512$ 时提升微弱。这表明编码需要足够的容量来编码视角变化，但过大的编码并不会带来额外收益。

### 与基线的关键差异

相较于NeRF（Mildenhall et al., ECCV 2020）和LFN等基于三维重建的视角合成方法，VIINTER在以下两个slot上做出了根本性改变：

| 关键模块 | 基线方法 | VIINTER |
|---------|---------|---------|
| **隐编码正则化** | 无约束，编码尺度不一致 | 训练过程中强制每个编码的L1范数为1 |
| **插值监督** | 无插值损失（仅重建损失） | 基于CLIP特征提取器的插值感知损失 $L_{Inter}$ |

这些改变使得VIINTER完全摆脱了对三维信息的依赖，但同时也带来了固有的局限性：由于无法通过隐编码精确定位任意相机位姿，在非结构化光场数据上像素级指标显著偏低（Table 2中Unstructured场景Novel视图SSIM仅0.664），但视觉过渡仍然平滑。Table 3中的“Ours-Finetuned”实验进一步揭示了一个重要事实：当冻结网络权重、仅针对测试图像真值优化隐编码时，新视角指标大幅提升，这表明INR本身具备表达新视角的能力，只是缺乏从相机位姿到隐编码的精确映射机制——这也是该方法当前的核心局限所在。

## 实验与关键发现

### 核心假设与验证路径

VIINTER 的核心实验逻辑围绕一个关键因果链条展开：**隐编码尺度不一致是导致编码插值失效的根本瓶颈，而通过 L1 范数归一化消除尺度差异后，编码空间的线性插值可被解码为视觉平滑的视角过渡**。实验设计依次验证了：（1）无正则化时插值完全崩溃；（2）不同范数约束对插值质量的影响差异；（3）编码长度的关键作用；（4）CLIP 引导的插值损失对伪影的抑制效果；（5）在结构化与非结构化光场数据上的泛化能力与边界条件。

---

### 决定性消融实验

#### 1. 隐编码范数约束：从完全失败到平滑过渡的转折点

**Table 1 (Top)** 和 **Figure 2** 给出了最关键的消融证据。在“No Control”条件下（编码尺度不受任何约束），INR 在已知视图（t=0, t=1）上能够正常重建，但线性插值编码 $z_{Inter} = 0.5z_i + 0.5z_j$ 解码出的图像完全无法辨认——SSIM 仅 0.595，PSNR 仅 11.02 dB。这直接验证了论文的核心诊断：**编码尺度差异导致插值编码偏离了 INR 能够合理解析的隐空间区域**。

引入范数约束后，插值质量出现质的飞跃：
- **L1 范数（p=1）**：新视图 SSIM 达 0.958，PSNR 达 32.39 dB，已知视图 SSIM 0.968/PSNR 33.97 dB，为所有条件最优；
- **Euclidean 范数（p=2）**：新视图 SSIM 0.937/PSNR 29.15 dB，虽显著优于无控制，但仍明显弱于 L1 范数；
- **无穷范数（p=∞）**：插值结果仍存在严重问题（Figure 2 显示过渡不自然）。

![[assets/figures/papers/paper_list_l98_https_arxiv_org_abs_2211_00722/figures/002_Figure_2.jpg]]
*Figure 2: Effect of Controlling*

**因果机制**：L1 范数鼓励编码向量的稀疏性，使得每个编码的“活跃”维度更集中，不同图像的编码在隐空间中占据更正交、更结构化的位置，从而线性插值路径更可能穿过 INR 能够合理解码的区域。Euclidean 范数虽统一了尺度，但未提供这种稀疏性先验，插值质量因此次优。

#### 2. 编码长度 M：存在最优值 128

**Table 1 (Bottom)** 和 **Figure 3** 揭示了编码维度的非线性影响：
- M=16 时新视图 SSIM 骤降至 0.891/PSNR 25.27 dB，表明编码容量不足时，INR 无法为每个图像学习足够的身份信息，插值编码携带的混合信息过于模糊；
- M 从 64 增至 128 时，新视图 SSIM 从 0.949 提升至 0.958，PSNR 从 31.06 升至 32.39 dB；
- M 进一步增至 256/512 时，性能提升微弱甚至饱和（M=512 时新视图 SSIM 0.959/PSNR 32.42 dB），表明过大的编码并未带来额外表达能力，反而增加过拟合风险。

**Figure 3** 的定性结果进一步显示：短编码（M=16）在已知视图仍可重建清晰图像，但插值结果（t=0.5）出现严重模糊和伪影。这说明编码长度不足主要损害的是**插值泛化能力**而非重建能力。

#### 3. CLIP 引导的插值损失：消除伪影的关键

**Figure 4** 对比了三种条件：
- **无 L_Inter**：插值图像出现可见的结构伪影和撕裂；
- **VGG-based 感知损失**：伪影被过度平滑取代，图像细节丢失严重；
- **CLIP-based L_Inter**：伪影显著减少，同时保留了合理的纹理细节。

**Figure 12** 揭示了 L_Inter 的代价：训练集 PSNR 从 32.36 dB 降至 30.39 dB（下降约 2 dB），说明插值损失的平滑约束与重建精度的锐度需求之间存在固有张力。这是一个典型的**保真度-平滑度权衡**：L_Inter 强制插值结果在 CLIP 语义空间中接近源图像的线性组合，这有助于消除高频伪影，但也会抑制 INR 对训练图像细节的精确拟合。

---

### 主要定量结果与基线对比

#### Stanford 4D Light Fields（结构化光场）

**Table 3** 给出了与 NeRF（Mildenhall et al., ECCV 2020）和 LFN 的对比。在已知视图上，VIINTER 的 SSIM 达 0.968，PSNR 达 33.97 dB；在新视图上，SSIM 达 0.975，PSNR 达 32.39 dB。相比 LFN（新视图 SSIM 0.944/PSNR 29.71 dB），VIINTER 在 SSIM 上领先 +0.031，PSNR 领先 +2.68 dB。

**但需注意公平性前提**：VIINTER 完全不使用 3D 信息或相机位姿，而 NeRF 和 LFN 均依赖精确的相机参数。VIINTER 在“已知视图”上的优势部分源于其对训练图像的强记忆能力（INR 对训练像素的过拟合），而新视图的指标反映的更多是插值平滑度而非精确视角重建——因为 VIINTER 无法精确定位测试视角对应的编码，只能通过等距插值近似。

#### 真实场景光场：结构化 vs 非结构化

**Table 2** 揭示了方法的关键适用边界：
- **4D Planar（结构化光场）**：已知视图 SSIM 0.978/PSNR 37.28 dB，新视图 SSIM 0.975/PSNR 35.77 dB——指标与 Stanford 数据集接近，表明在规则采样的平面光场上，线性编码插值能很好地对应实际视角变化；
- **Unstructured（非结构化光场）**：已知视图 SSIM 仍达 0.885/PSNR 28.32 dB，但新视图指标骤降至 SSIM 0.664/PSNR 16.80 dB。

**失败原因分析**：非结构化光场中相机运动包含旋转和平移的复杂组合，且视点分布不均匀。由于 VIINTER 无法将相机位姿映射到编码空间，测试视角的“真实”编码与训练编码之间的线性插值位置存在严重偏差，导致渲染图像与真值在像素级对齐上差距巨大。**Figure 6** 的定性结果则显示，尽管像素级指标偏低，插值过渡在视觉上仍保持平滑——这说明 INRs 学到的是图像内容的连续流形，而非精确的视角对应。

---

### 表达能力上限验证：Ours-Finetuned

**Table 3** 中的“Ours-Finetuned”条件提供了关键的诊断性证据：冻结 INR 网络权重，仅针对测试图像的真值优化其隐编码（使用与训练相同的重建损失）。结果显示新视图 SSIM 从 0.975 跃升至 0.991，PSNR 从 32.39 升至 38.78 dB。

**这一结果排除了“INR 表达能力不足”的替代解释**，证明瓶颈不在于网络容量，而在于**缺乏从相机位姿到隐编码的映射机制**。INR 完全有能力表达训练集之外的新视角，只是 VIINTER 的纯插值策略无法精确找到对应的编码。

---

### 失败模式与适用边界

1. **大视差场景的崩溃**：**Figure 7** 显示当训练视点间视差过大（视点密度不足）时，插值图像出现明显的重影和撕裂伪影。这是因为 INR 仅从 2D 图像学习，缺乏 3D 几何先验来处理遮挡关系和深度不连续。当视点间距超出 INR 的隐式 2D 插值能力时，线性编码插值无法产生合理的中间视图。

2. **非结构化光场的像素级失准**：如 Table 2 所示，在相机运动复杂的场景中，像素级指标（PSNR/SSIM）显著偏低。这是方法“无 3D 位姿”设计理念的固有代价——VIINTER 牺牲了精确的视角控制能力，换取了无需标定的便利性。

![[assets/figures/papers/paper_list_l98_https_arxiv_org_abs_2211_00722/figures/008_Table_2.jpg]]
*Table 2: Quantitative results on real-world scenes with different viewpoint layouts. Our method can only render at the approximate viewpoints of ground truth, as discussed in Section 4, leading to lower PSNR and SSIM values for novel views of “Unstructured” where the viewpoint mismatch is severe. See visual results for more comprehensive quality assessments*

3. **插值损失对细节的损伤**：L_Inter 在消除伪影的同时降低了训练集 PSNR 约 2 dB（Figure 12），表明该方法在平滑过渡与细节保真之间存在可调节但不可消除的权衡。

4. **仅支持成对线性插值**：方法仅探索了两个训练编码之间的线性插值路径（Algorithm 1），未涉及多路径、非线性或外推场景。**Figure 8** 展示了可通过链式插值（在插值编码之间再次插值）获得更多中间视角，但这仍局限于初始编码对的凸组合范围内。

![[assets/figures/papers/paper_list_l98_https_arxiv_org_abs_2211_00722/figures/006_Table_1.jpg]]
*Table 1: Top: Effect of varying ?? for code rescaling. Quantitative results reaffirm that rescaling based on 1-norm achieves the best quality. Bottom: Effect of varying the length of code ??. Results indicate that the code length cannot be arbitrary, as a small ?? can be detrimental to the interpolation quality. Setting ?? too large is also not helpful, as the quality appears to peak at ?? = 128. More details about the experimental setting are in Sec. 4*

![[assets/figures/papers/paper_list_l98_https_arxiv_org_abs_2211_00722/figures/012_Table_3.jpg]]
*Table 3: Quantitative results on novel views with an additional condidtion Ours-Finetuned, where we render our INR with the latent code obtained after optimizing it against the ground truth test image (while freezing the network weights). Results suggest that the trained INR is capable of achieving better quantitative novel view results, but is handicapped by our inability input exact camera poses due to non-3D nature of our method*

![[assets/figures/papers/paper_list_l98_https_arxiv_org_abs_2211_00722/figures/003_Figure_3.jpg]]
*Figure 3: Effect of Code Length ??. When trained with shorter code vectors, the INR can still produce good results at known views*

## 定位与知识库关联

VIINTER 的核心定位在于改变了视角合成任务中“如何获得新视角的隐编码”这一关键 **slot**：传统基于 3D 重建的方法（如 **NeRF**, Mildenhall et al., ECCV 2020；**LFN** 等光场网络）通过相机位姿或光线参数来索引场景表示，隐式地将视角信息编码在网络输入或条件变量中；而 VIINTER 完全抛弃了相机位姿和 3D 结构，转而通过对 **每个训练图像分配一个可学习的隐编码向量**，并在训练时强制所有编码具有统一的 **单位 L1 范数**，使得编码空间中的线性插值能够被解码器合理解析为平滑的视角过渡。

这一改变的因果链条是：标准的多图像 INR 训练中，各图像的隐编码在优化过程中会获得不同的尺度（范数），导致编码之间的线性插值落入解码器从未见过的区域，产生完全无意义的输出（Figure 2 “No Control”）。VIINTER 通过在每次训练迭代中将每个编码除以其 L1 范数（$z = z / \|z\|_1$），将所有编码约束到同一超球面上，消除了尺度差异——这是插值能够成功的前提条件。在此基础上，引入基于 **CLIP** 预训练网络的插值感知损失 $L_{Inter}$，鼓励插值输出图像的特征与源图像特征的线性插值保持一致，进一步抑制了插值伪影。

### 与基线方法的本质差异

| 对比维度 | NeRF / LFN 等 3D 方法 | VIINTER |
|---------|----------------------|---------|
| **新视角编码来源** | 相机位姿或光线参数 → 网络隐式推理 | 训练编码的线性插值 $z_{Inter} = (1-t)z_i + t z_j$ |
| **是否依赖 3D 信息** | 需要相机位姿、3D 重建或光线几何 | 完全不需要 |
| **编码空间结构** | 由 3D 几何隐式决定 | 由 L1 范数归一化显式约束 |
| **插值机制** | 在 3D 空间中采样光线 | 在归一化编码空间中线性插值 |

VIINTER 与 NeRF 的根本区别不在于网络架构（都使用了基于坐标的 MLP），而在于 **“如何为任意目标视角获取有效的条件编码”** 这一槽位。NeRF 通过相机位姿将视角信息注入到光线采样过程中，本质上依赖 3D 一致性；VIINTER 则通过编码空间的代数结构（L1 归一化 + 线性插值）来隐式组织视角关系，将问题从 3D 重建转化为 2D 图像集合的隐空间组织问题。

### 知识库挂载点

VIINTER 可挂载到以下知识库节点：

1. **隐式神经表示（INR）的条件编码机制**：该方法属于“以可学习编码为条件的多图像 INR”这一技术路线。其核心贡献在于揭示了 **编码范数归一化** 对于编码空间可插值性的关键作用，这为后续研究提供了一个明确的操作原则：当需要在一个共享解码器的隐空间中实现样本间平滑过渡时，对隐编码施加单位范数约束是必要而非可选的。

2. **无位姿视角合成**：VIINTER 是一个极端的“无位姿”视角合成方法，与需要位姿的光场网络（LFN）和 NeRF 形成互补。它在知识库中的定位是：当相机位姿不可获得或不可靠时，提供一种仅依赖图像集合本身的视角插值方案。其适用边界由视点密度决定——当视差过大时（Figure 7），由于缺乏 3D 信息来指导大位移下的遮挡推理，插值会出现明显伪影。

3. **CLIP 作为感知先验**：VIINTER 将 CLIP 用作插值损失的感知特征提取器，而非生成式先验或文本条件。这一用法在知识库中属于“预训练视觉模型作为训练正则化器”的范畴，与 VGG-based 感知损失（如 LPIPS）形成对比。实验表明（Figure 4），VGG 损失会导致过度平滑，而 CLIP 损失能更好地保留细节并消除伪影——这提示 CLIP 的特征空间可能比 VGG 更适合作为图像插值的感知约束。

### 适用边界与限制

1. **视点密度依赖**：方法假设训练视角足够密集，使得相邻视角之间的视差在 INR 能够通过 2D 隐式插值处理的范围内。当视点稀疏导致视差过大时，插值质量显著下降（Figure 7）。这是不依赖 3D 信息的固有限制。

2. **无法精确控制视角**：由于不使用相机位姿，VIINTER 无法为任意给定的相机外参生成对应图像。在“非结构化”光场数据上，测试视角的编码只能通过线性插值近似，导致像素级指标（PSNR/SSIM）显著偏低（Table 2: Unstructured Novel SSIM 仅 0.664）。**Ours-Finetuned** 实验（Table 3）通过用测试图像真值优化编码，使指标大幅提升，证明 INR 本身具备表达新视角的能力，瓶颈在于缺乏从位姿到编码的映射机制。

3. **插值损失的双刃剑效应**：$L_{Inter}$ 在提升过渡平滑度的同时，会降低训练集重建 PSNR 约 2 dB（从 32.36 降至 30.39，Figure 12），损伤部分细节。这表明感知插值约束与像素级重建精度之间存在 trade-off。

4. **仅支持成对线性插值**：方法当前仅探索了两个训练编码之间的线性插值，未涉及多路径或非线性的插值方式（论文 Discussion 部分明确指出）。

### 后续研究启发

VIINTER 为以下方向提供了明确的出发点：

- **从插值到外推**：当前方法仅支持训练视角之间的插值，能否学习一个从相机位姿到隐编码的映射网络，使 INR 能够生成训练视角之外的任意新视角？这是将方法从“插值”推广到“任意视角合成”的关键一步。
- **非线性插值路径**：编码空间中的线性插值是否为最优路径？对于复杂场景（如包含遮挡、非朗伯反射），可能需要在归一化球面上学习非线性的插值函数。
- **对抗或生成先验的引入**：论文明确指出 VIINTER 未使用对抗训练。对于大视差场景，结合生成先验（如 GAN 或扩散模型）可能提升插值的鲁棒性和真实感。
- **编码空间的几何理解**：L1 归一化将编码约束到单纯形表面，这一几何结构是否与视角变化的物理结构存在对应关系？进一步的理论分析可能揭示编码空间的组织规律。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/VIINTER_View_Interpolation_With_Implicit_Neural_Representations_of_Images.pdf]]