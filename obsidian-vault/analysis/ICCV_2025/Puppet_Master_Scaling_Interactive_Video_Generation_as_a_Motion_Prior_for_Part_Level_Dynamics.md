---
title: "Puppet-Master: Scaling Interactive Video Generation as a Motion Prior for Part-Level Dynamics"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Puppet_Master_Scaling_Interactive_Video_Generation_as_a_Motion_Prior_for_Part_Level_Dynamics.pdf
project_link: null
code_link: null
aliases:
- PM
- Puppet-Master
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "训练数据从混杂的真实视频转变为精心筛选的合成动画数据集（Objaverse-Animation-HQ），并在预训练视频扩散模型中新增拖拽调制、拖拽令牌交叉注意力以及all-to-first注意力。"
primary_logic: "利用高质量合成动画数据（消除无关运动因素）并结合拖拽编码注入和all-to-first注意力捷径，可使大规模预训练视频扩散模型仅通过微调就习得部件级运动先验，并零样本泛化至真实图像。"
claims:
- "在Drag-a-Move和Human3.6M两个基准上，Puppet-Master在所有指标（PSNR、SSIM、LPIPS、FVD、Motion Error）上均大幅超越基于真实视频训练的DragNUWA、DragAnything等模型，且第二部分Motion Error（全局前景误差）远低于其他方法，证明其具备真正的部件级运动控制能力。"
- "消融实验证实：自适应归一化（scale+shift）优于仅shift；提供拖拽终点信息v_k^N提升运动一致性；交叉注意力中加入drag tokens增强空间感知；all-to-first attention对视频质量至关重要，缺少时背景产生严重伪影。"
- "Drag-a-Move 上 PSNR↑ = 24.41"
- "Drag-a-Move 上 SSIM↑ = 0.927"
---

# Puppet-Master: Scaling Interactive Video Generation as a Motion Prior for Part-Level Dynamics

> [!tip] 核心洞察
> 利用高质量合成动画数据（消除无关运动因素）并结合拖拽编码注入和all-to-first注意力捷径，可使大规模预训练视频扩散模型仅通过微调就习得部件级运动先验，并零样本泛化至真实图像。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Puppet-Master：扩展交互式视频生成作为部件级动态的运动先验 |
| 英文题名 | Puppet-Master: Scaling Interactive Video Generation as a Motion Prior for Part-Level Dynamics |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2408.04631) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Puppet-Master |
| Dataset | Drag-a-Move |

> [!tip] 效果简介
> - Drag-a-Move 上，PSNR↑ 为 24.41，对比 20.09 (DragNUWA)，变化 +4.32。
> - Drag-a-Move 上，SSIM↑ 为 0.927，对比 0.874 (DragNUWA)，变化 +0.053。
> - Drag-a-Move 上，LPIPS↓ 为 0.085，对比 0.172 (DragNUWA)，变化 -0.087。

## 概要

**问题瓶颈**。现有的拖拽条件视频生成模型——如 DragNUWA、DragAnything (Wu et al., ECCV 2024)、Image Conductor——在给定输入图像和运动拖拽箭头后，往往只能产生物体的整体平移或缩放，无法可靠地生成部件级（part-level）的内部运动。其根本原因在于：这些模型训练所用的互联网视频数据中混杂了全局物体运动、相机运动与遮挡，而模型架构本身缺乏对稀疏拖拽空间信息的精细利用能力。

**核心思路**。Puppet-Master 提出了一条不同的技术路径：将训练数据域从混杂的真实视频切换为精心筛选的合成动画数据集 Objaverse-Animation-HQ，并在预训练视频扩散模型（Stable Video Diffusion, SVD）中引入三项架构改进——拖拽调制（drag modulation）、拖拽令牌交叉注意力（drag tokens cross-attention）以及 all-to-first 注意力——从而仅通过微调就使大规模预训练模型习得部件级运动先验，并零样本泛化至真实图像。

**方法定位**。Puppet-Master 以 SVD 作为视频生成骨干，在其 UNet 中新增：(1) 自适应层归一化模块，从多分辨率拖拽编码中回归缩放与偏移参数，以元素级仿射变换调制内部特征图；(2) 拖拽令牌，通过 MLP 从拖拽轨迹和扩散特征中回归额外的键值对，注入交叉注意力层以增强空间感知；(3) all-to-first 注意力，替换所有空间自注意力层，强制每帧的查询仅与第一帧的键值交互，形成从干净参考帧到其余帧的捷径，从而抑制背景伪影和外观退化。训练数据方面，从 Objaverse 三维资产库中构建了两个层次的数据集——Objaverse-Animation（16k）和更高质量的 Objaverse-Animation-HQ（10k），并结合 Drag-a-Move 数据集进行微调。

**关键结果**。在 Drag-a-Move 基准上，Puppet-Master 在所有指标上均大幅超越基于真实视频训练的基线模型：PSNR 达到 24.41（DragNUWA 为 20.09），SSIM 为 0.927（DragNUWA 为 0.874），LPIPS 降至 0.085（DragNUWA 为 0.172），FVD 降至 246.99（DragNUWA 为 281.49）。尤为关键的是，Puppet-Master 的第二部分运动误差（全局前景误差）仅为 3.53，而 DragNUWA 高达 15.41，直接证明了其具备真正的部件级运动控制能力。在 Human3.6M 上的零样本测试同样展现了竞争力。消融实验进一步证实：自适应归一化（scale+shift）、拖拽终点编码、拖拽令牌交叉注意力以及 all-to-first 注意力各自对运动一致性和视频质量均有显著贡献，且数据筛选对训练稳定性和最终质量不可或缺。

### 问题背景：拖拽条件视频生成与部件级动态的缺失

拖拽条件视频生成（drag-conditioned video generation）旨在通过用户指定的稀疏运动轨迹（拖拽箭头）来驱动图像中的物体产生动画。这一交互范式在数字内容创作、视觉特效和交互式媒体中具有广泛的应用前景。然而，现有方法面临一个核心瓶颈：**它们无法可靠地生成物体自身的部件级（part-level）内部运动**。

所谓部件级运动，是指物体不同组成部分之间的相对运动——例如人抬手时大臂相对躯干的旋转、抽屉相对柜体的滑出，或风扇叶片相对机身的转动。与之相对的是全局物体运动（整体平移、缩放或旋转），后者不涉及物体内部结构的形变。现有拖拽条件视频生成模型在接收到拖拽信号时，往往只产生整体平移或缩放，而非真正的部件级动态。这种“整体移动”的行为暴露了模型对运动语义理解的缺失。

### 现有方法的缺口：数据混杂与架构局限

造成上述瓶颈的原因可归结为两个层面。

**数据层面**：现有方法（如 **DragNUWA**、**DragAnything** (Wu et al., ECCV 2024)、**Image Conductor**）普遍在大规模互联网视频数据上进行训练，包括 WebVid、RealEstate10K 和 VIPSeg 等。这些真实视频中混杂着多种无关运动因素：相机运动（推拉摇移）、全局物体位移、遮挡关系变化，以及物体自身的部件级运动。模型从这样的数据中难以解耦出部件级运动的纯粹信号，导致学到的运动先验偏向于“整体移动”这一统计上的简单解。

**架构层面**：现有的拖拽条件注入机制过于粗糙。以 DragNUWA 为例，其仅通过 CLIP 图像嵌入实现单一的交叉注意力，未对拖拽的空间信息进行精细编码和利用。稀疏的拖拽信号（通常仅包含起点和终点坐标）在经过简单的编码后，不足以向扩散模型传递足够的空间约束来驱动部件级变形。

### 核心洞察与本文动机

本文的核心洞察是：**通过消除训练数据中的无关运动因素，并结合精细的拖拽编码注入与架构设计，可以使大规模预训练视频扩散模型仅通过微调就习得鲁棒的部件级运动先验**。

具体而言，Puppet-Master 从三个关键维度切入：

1. **数据域迁移**：从混杂的真实视频转向精心筛选的合成动画数据集（Objaverse-Animation-HQ）。合成数据天然消除了相机运动和全局物体位移的干扰，使模型能够专注于学习稀疏拖拽与部件级运动之间的映射关系。

2. **拖拽条件精细化注入**：在预训练视频扩散模型（Stable Video Diffusion）中新增两个互补的拖拽编码通路——自适应层归一化（drag modulation，同时回归 scale 和 shift 参数）和拖拽令牌交叉注意力（drag tokens），共同将拖拽的起点、中间点及终点信息注入生成过程。

3. **空间注意力捷径**：引入 all-to-first attention 机制，强制所有生成帧的空间自注意力查询仅与干净的第一帧（参考帧）的键值进行交互。这一设计既保留了参考帧的高质量外观，又建立了拖拽终点像素与起点像素之间的直接注意力连接，从而降低模型学习部件级运动的难度。

值得注意的是，Puppet-Master 仅在合成数据上进行微调，未在任何真实视频数据集上训练，却能零样本泛化至真实图像（包括 Human3.6M 人体动作、Amazon-Berkeley Objects 物体及网络图像），这验证了合成数据驱动的部件级运动先验具有跨域迁移能力。

## 核心方法与创新机理

Puppet-Master 的核心创新在于通过**三个架构层面的改动**（changed slots）与**训练数据域的迁移**，使预训练视频扩散模型从只能生成整体平移/缩放，跃迁到能够精准控制物体内部的部件级运动。

### 1. 拖拽条件的精细注入：Drag Modulation 与 Drag Tokens

现有拖拽条件视频模型（如 DragNUWA、DragAnything）通常仅依赖 CLIP 图像嵌入进行单一的交叉注意力，缺乏对稀疏拖拽空间信息的有效利用。Puppet-Master 设计了两条互补的注入路径：

- **Drag Modulation（自适应层归一化）**：将每条拖拽的起点、中间点与终点编码为多分辨率空间特征图 $\mathcal{D}_{\mathrm{enc}}^s$，通过小型网络回归尺度 $\gamma_s$ 与偏移 $\beta_s$，以元素级仿射变换调制 UNet 各层特征图：
  $$f_s \gets f_s \otimes ( \mathbf{1} + \gamma_s( \mathcal{D}_{\mathrm{enc}}^s ) ) + \beta_s( \mathcal{D}_{\mathrm{enc}}^s )$$
  消融实验证实，同时使用 scale 与 shift（自适应归一化）远优于仅使用 shift 的方案，PSNR 从 13.23 跃升至 22.98，且运动方向错误率大幅降低（Table 2, A vs B）。

- **Drag Tokens 交叉注意力**：通过 MLP 从拖拽的起点、终点及内部扩散特征中回归额外的 $K$ 组键值对，与原始 CLIP 图像 token 共同组成 $1+K$ 组键值注入交叉注意力层。这为模型提供了显式的空间感知能力，使 PSNR 进一步提升至 24.00，LPIPS 降至 0.069（Table 2, C vs D）。

### 2. 外观质量的捷径：All-to-First Attention

在分布外合成数据上微调视频扩散模型时，生成视频的背景与外观往往严重退化。Puppet-Master 提出 **all-to-first attention**，直接替换 UNet 中所有空间自注意力层：每一帧的查询 $Q[i]$ 仅与第一帧的键 $K[0]$ 和值 $V[0]$ 计算注意力：
$$A_i = \mathrm{softmax}\left( \frac{ \mathrm{flat}(Q[i]) \mathrm{flat}(K[0])^{\top} }{ \sqrt{D} } \right) \mathrm{flat}(V[0])$$

这一设计形成从干净参考帧到后续所有帧的“捷径”，同时使拖拽终点对应的潜在像素更容易关注到第一帧中拖拽起点的潜在像素，从而促进运动学习。消融实验表明，缺少 all-to-first attention 时，生成视频背景杂乱、外观退化，FVD 从 205.40 飙升至 624.64（Table 2, C vs E）。

### 3. 训练数据域的根本性迁移

此前方法训练于混杂全局物体运动、相机运动与遮挡的互联网真实视频（如 WebVid、VIPSeg），模型难以从中分离出纯粹的部件级运动信号。Puppet-Master 将训练数据完全切换为精心筛选的**合成动画数据集 Objaverse-Animation-HQ**（10k 个高质量部件级运动动画），从根本上消除了无关运动因素的干扰。数据筛选对训练稳定性与生成质量至关重要：使用未精筛的 Objaverse-Animation 训练时，PSNR 仅为 6.04，FVD 高达 1475.35，且训练在约 7k 次迭代后崩溃；而使用 Objaverse-Animation-HQ 后，PSNR 提升至 19.87，FVD 降至 624.47，训练保持稳定（Table 3; Figure 7）。

### 创新协同效应

上述三个 changed slots 并非孤立改进，而是形成协同效应：高质量合成数据提供了纯净的部件级运动监督信号；drag modulation 与 drag tokens 将稀疏拖拽信息精细嵌入扩散去噪过程；all-to-first attention 则保障了外观质量不因域迁移而退化。三者共同使 Puppet-Master 仅通过微调就在 Drag-a-Move 和 Human3.6M 两个基准上全面超越基于真实视频训练的 DragNUWA、DragAnything 等方法，尤其在衡量全局前景误差的第二部分 Motion Error 上取得压倒性优势（3.53 vs 15.41），验证了其真正的部件级运动控制能力。

![[assets/figures/papers/paper_list_l18_Puppet_Master_Scaling_Interactive_Video_Generation_as_a_Motion_Prior_for/figures/002_Figure_2.jpg]]
*Figure 2: Architectural Overview of Puppet-Master. To enable precise drag conditioning, we first modify the original latent video diffusion architecture (Sec. 3.1) by (A) adding adaptive layer normalization modules to modulate the internal diffusion features and (B) adding cross attention with drag tokens (Sec. 3.2). Furthermore, to ensure high-quality appearance and background, we introduce (C) all-to-first attention, a drop-in replacement for the spatial self-attention modules, where every video frame attends the first one (Sec. 3.3)*

Puppet-Master 的整体流程围绕一个核心设计展开：将稀疏的拖拽（drag）信号转化为精确的部件级视频运动先验。系统接收一张参考图像和一组用户指定的拖拽箭头作为输入，输出一段符合拖拽意图的部件级动态视频。其 pipeline 由三个紧密耦合的模块构成：**预训练视频扩散骨干网络**、**拖拽条件注入机制**，以及**全帧到首帧注意力**。

### 输入输出流

输入端的拖拽定义为一组 $K$ 条运动轨迹 $\mathcal{D} = \{d_1, \dots, d_K\}$，每条轨迹 $d_k$ 包含起点 $\mathbf{u}_k$、中间点 $\mathbf{v}_k^n$ 和终点 $\mathbf{v}_k^N$。参考图像 $x^1$ 经编码器映射到潜在空间，与拖拽信息一同送入去噪网络。输出为 $N$ 帧的潜在编码序列，解码后得到最终视频。

### 模块关系

**Stable Video Diffusion (SVD) 骨干**（Sec. 3.1）提供基础的视频动态先验。SVD 是一个预训练的图像到视频潜在扩散模型，其前向过程按噪声调度向视频潜在编码逐步添加高斯噪声：

$$z_{t}^{1:N} = \sqrt{\bar{\alpha}_{t}} z_{0}^{1:N} + \sqrt{1 - \bar{\alpha}_{t}} \epsilon^{1:N}$$

去噪网络 $\epsilon_\theta$ 通过最小化噪声预测误差进行训练：

$$\min_{\theta} \mathbb{E}_{(x^{1:N}, y), t, \epsilon^{1:N} \sim \mathcal{N}(0, I)} \left[ \| \epsilon^{1:N} - \epsilon_{\theta}(z_{t}^{1:N}, t, y) \|_{2}^{2} \right]$$

在该骨干基础上，Puppet-Master 新增两类模块以实现精细的拖拽控制（图 2）：

1. **拖拽条件注入**（Sec. 3.2）：首先通过多分辨率编码函数 $\text{enc}(\cdot, s)$ 将每条拖拽编码为空间特征图 $\mathcal{D}_{\text{enc}}^s$，编码内容覆盖拖拽起点、中间点及终点。这些编码随后以两种方式注入 UNet：
   - **自适应层归一化（Drag Modulation）**：通过 MLP 从 $\mathcal{D}_{\text{enc}}^s$ 回归缩放参数 $\gamma_s$ 和偏移参数 $\beta_s$，对 UNet 各层特征图 $f_s$ 执行元素级仿射变换：

     $$f_s \gets f_s \otimes ( \mathbf{1} + \gamma_s( \mathcal{D}_{\text{enc}}^s ) ) + \beta_s( \mathcal{D}_{\text{enc}}^s )$$

   - **拖拽令牌交叉注意力（Drag Tokens）**：从每条拖拽的起点、终点及内部扩散特征中通过 MLP 回归额外的键值对，与原始 CLIP 图像嵌入组成 $1+K$ 组键值注入交叉注意力层，增强空间感知。

2. **全帧到首帧注意力（All-to-First Attention）**（Sec. 3.3）：替换 UNet 中所有空间自注意力层。第 $i$ 帧的查询 $Q[i]$ 仅与第一帧的键 $K[0]$ 和值 $V[0]$ 进行注意力计算：

   $$A_i = \text{softmax}\left( \frac{ \text{flat}(Q[i]) \text{flat}(K[0])^{\top} }{ \sqrt{D} } \right) \text{flat}(V[0])$$

   这一捷径使后续帧可直接访问参考帧未退化外观细节，同时让拖拽终点对应的潜在像素更容易关注到首帧中的拖拽起点，从而促进运动学习。

### 数据与训练

Puppet-Master 仅使用合成数据集进行微调，不依赖任何真实视频。训练数据来自精心筛选的 **Objaverse-Animation-HQ**（约 10k 个高质量部件级运动动画资产），结合 Drag-a-Move 数据集。拖拽轨迹通过采样 3D 模型可见部分的运动点并投影到 2D 像素空间生成，采样概率正比于该点的总位移。为保证拖拽的稀疏性，当两条轨迹的 $L_2$ 距离低于阈值 $\delta$ 时随机移除其一：

$$\lVert \boldsymbol{v}_i^{1:N} - \boldsymbol{v}_j^{1:N} \rVert_2^2 \leq \delta$$

这种合成数据驱动策略消除了真实视频中混杂的全局物体运动、相机运动与遮挡等干扰因素，使模型仅通过微调即可习得纯净的部件级运动先验，并零样本泛化至真实图像。

Puppet-Master 以 Stable Video Diffusion（SVD）作为预训练视频生成骨干，在其基础上新增三个核心模块，将稀疏拖拽控制信号注入去噪过程，并保障生成视频的外观质量。

### 拖拽编码与自适应层归一化

拖拽控制的核心是将用户输入的 $K$ 条拖拽轨迹 $\mathcal{D} = \{d_k\}_{k=1}^K$ 编码为空间特征，并注入 UNet 的各个层级。每条拖拽 $d_k$ 由起点 $\mathbf{u}_k$、$N$ 帧中每一帧的中间位置 $\mathbf{v}_k^n$ 以及终点 $\mathbf{v}_k^N$ 组成。编码函数 $\text{enc}(\cdot, s)$ 针对 UNet 的第 $s$ 层分辨率，将拖拽信息转化为多分辨率特征图 $\mathcal{D}_{\text{enc}}^s$，其中每个空间切片编码了拖拽起点、当前帧位置及终点位置。

编码后的拖拽特征通过**自适应层归一化**（drag modulation）注入 UNet 特征图 $f_s$：

$$f_s \gets f_s \otimes (\mathbf{1} + \gamma_s(\mathcal{D}_{\text{enc}}^s)) + \beta_s(\mathcal{D}_{\text{enc}}^s)$$

其中 $\gamma_s$ 和 $\beta_s$ 是由拖拽编码回归得到的缩放与偏移参数，$\otimes$ 表示逐元素乘法。该仿射变换同时调节特征的尺度与偏移，相比仅使用偏移项的方案提供了更强的条件控制能力（消融实验中 PSNR 从 13.23 提升至 22.98，见 Table 2 A vs B）。

### 拖拽令牌交叉注意力

为进一步增强空间感知，Puppet-Master 在交叉注意力层中引入**拖拽令牌**（drag tokens）。对于每条拖拽 $d_k$，一个 MLP 以拖拽起点 $\mathbf{u}_k$、终点 $\mathbf{v}_k^N$ 和当前帧位置 $\mathbf{v}_k^n$ 以及内部扩散特征为输入，回归出一对额外的键值对。最终，交叉注意力层拥有 $1 + K$ 组键值对：1 组来自原始 CLIP 图像嵌入，$K$ 组来自拖拽令牌。这使得模型能够显式地关注拖拽所指向的空间区域，从而改善生成细节（PSNR 从 23.67 提升至 24.00，LPIPS 降至 0.069，见 Table 2 C vs D）。

### All-to-First 注意力

在 SVD 上进行域外数据微调时，生成视频的外观质量会严重退化——除第一帧外，其余帧常出现背景杂乱和纹理失真。为解决这一问题，Puppet-Master 将所有空间自注意力层替换为 **all-to-first attention**：

$$A_i = \text{softmax}\left( \frac{\text{flat}(Q[i]) \, \text{flat}(K[0])^{\top}}{\sqrt{D}} \right) \text{flat}(V[0])$$

其中 $Q[i]$ 为第 $i$ 帧的查询，$K[0]$ 和 $V[0]$ 为第一帧的键和值。该机制强制每一帧的查询仅与第一帧的干净键值进行注意力计算，形成一条从参考帧到后续帧的外观捷径。这一设计同时促进了拖拽终点对应的隐空间像素更容易关注到第一帧中拖拽起点的对应像素，从而加速运动模式的学习。消融实验表明，移除 all-to-first attention 会导致 FVD 从 205.40 飙升至 624.64，且背景产生严重伪影（Table 2 C vs E；Figure 6）。

### 前向扩散与训练目标

Puppet-Master 沿用 SVD 的潜在扩散框架。给定视频的潜在编码 $z_0^{1:N}$，前向扩散过程按噪声调度逐步添加高斯噪声：

$$z_t^{1:N} = \sqrt{\bar{\alpha}_t} \, z_0^{1:N} + \sqrt{1 - \bar{\alpha}_t} \, \epsilon^{1:N}, \quad t = 1, \ldots, T$$

去噪网络 $\epsilon_\theta$ 以噪声潜在编码 $z_t^{1:N}$、时间步 $t$ 和条件 $y$（包含 CLIP 图像嵌入与拖拽信息）为输入，通过最小化噪声预测的均方误差进行训练：

$$\min_\theta \mathbb{E}_{(x^{1:N}, y), t, \epsilon^{1:N} \sim \mathcal{N}(0, I)} \left[ \| \epsilon^{1:N} - \epsilon_\theta(z_t^{1:N}, t, y) \|_2^2 \right]$$

训练中采用连续时间扩散框架，并将噪声水平 $\log \sigma$ 的分布偏移至 $\mathcal{N}(0.7, 1.6^2)$，以增强模型对抽象运动的建模能力。

## 实验与关键发现

### 实验设置

Puppet-Master 以 Stable Video Diffusion（SVD）为骨干，仅使用合成数据集进行微调：包含 Drag-a-Move 训练集以及精心筛选的 Objaverse-Animation-HQ（约 10k 个高质量部件级动画资产）。训练时从 3D 动画的可见表面点中，按其跨帧位移概率采样运动轨迹并投影至 2D 像素空间作为拖拽条件，同时通过后处理步骤确保各拖拽轨迹间 L2 距离足够大（$\lVert \boldsymbol{v}_i^{1:N} - \boldsymbol{v}_j^{1:N} \rVert_2^2 \leq \delta$ 时随机移除其一），以保持运动提示的稀疏性。为增强对抽象运动的建模，训练中将连续时间噪声水平分布向高噪声偏移（$\log \sigma \sim \mathcal{N}(0.7, 1.6^2)$）。

所有对比方法均使用公开预训练权重并按官方推荐方式推理，视频统一调整为 256×256 分辨率、14 帧进行评估。Puppet-Master 未在任何真实视频数据集上训练，所有真实数据（Human3.6M、Amazon-Berkeley Objects 及网络图像）均为零样本测试。

### 主实验结果

Table 1 展示了在 Drag-a-Move 和 Human3.6M 两个基准上的定量对比。在 Drag-a-Move 上，Puppet-Master 在所有指标上均大幅领先：

![[assets/figures/papers/paper_list_l18_Puppet_Master_Scaling_Interactive_Video_Generation_as_a_Motion_Prior_for/figures/004_Table_1.jpg]]
*Table 1: Comparisons with DragNUWA [70], DragAnything [67], Image Conductor [32] and DragAPart [31] on the Drag-a-Move and Human3.6M datasets. Our model has not been trained on Human3.6M or any other real video dataset. Colors denote best and second best*

- **PSNR** 达到 24.41，较 DragNUWA（20.09）提升 4.32dB；
- **SSIM** 为 0.927（DragNUWA 0.874），**LPIPS** 降至 0.085（DragNUWA 0.172），**FVD** 降至 246.99（DragNUWA 281.49）；
- **Motion Error** 尤为关键：Puppet-Master 的全局前景误差（第二部分 ME）仅为 3.53，而 DragNUWA 高达 15.41，差距达 11.88。这表明先前方法主要产生整体平移/缩放，而 Puppet-Master 真正习得了部件级内部运动控制能力。

在零样本泛化的 Human3.6M 上，Puppet-Master 的 FVD（454.76）优于 DragNUWA（466.91），PSNR 和 SSIM 基本持平，证明了合成数据训练的运动先验可有效迁移至真实人体场景。

定性对比（Figure 4）进一步印证：Puppet-Master 生成的视频包含更真实的局部动态，而基线方法常出现整体位移或运动方向错误。Figure 5 展示了模型对多种类别（人体、动物、铰接及软体物体）的泛化能力，以及多部件运动相关性——例如未明确拖拽后腿时，四条腿仍能同步运动。

### 消融实验

Table 2 和 Figure 6 系统验证了各设计选择的贡献：

![[assets/figures/papers/paper_list_l18_Puppet_Master_Scaling_Interactive_Video_Generation_as_a_Motion_Prior_for/figures/008_Table_2.jpg]]
*Table 2: Ablations. In addition to the standard metrics and motion error (ME) which we introduced in Sec. 5.1, we also manually count the frequency of generated videos whose motion directions are opposite to the intention of their drag inputs (% wrong direction, or %WD in short). Here, ≥ indicates there are video samples whose motion directions are hard to distinguish. When ablating various designs of attention with the reference image, we use C as the base drag conditioning architecture*

**拖拽调制机制**（A vs B）：采用自适应归一化（scale + shift）替代仅 shift 的版本，PSNR 从 13.23 跃升至 22.98，且运动方向错误率显著降低，证实 scale 参数对精确调节特征响应至关重要。

**拖拽终点编码**（B vs C）：在拖拽编码中额外加入最终终止位置 $v_k^N$ 作为上下文，PSNR 进一步提升至 23.67，说明终点信息有助于模型规划完整运动轨迹。

**Drag Tokens 交叉注意力**（C vs D）：在交叉注意力中引入 drag tokens 后，PSNR 达到 24.00，LPIPS 降至 0.069，且 Figure 6 显示细节质量明显改善。这表明 drag tokens 有效增强了空间感知能力。

**All-to-First 注意力**（C vs E）：缺少 all-to-first attention 时，FVD 从 205.40 急剧恶化至 624.64，背景出现严重伪影（Figure 6）。该机制通过强制所有帧仅与第一帧交互，为后续帧提供干净的外观捷径，同时使拖拽终点对应的隐空间像素更易关注到第一帧中的拖拽起点，从而促进运动学习。

### 数据筛选的关键作用

Table 3 和 Figure 7 揭示了数据质量的决定性影响：使用未精筛的 Objaverse-Animation（16k）训练时，PSNR 仅为 6.04，FVD 高达 1475.35；而采用 Objaverse-Animation-HQ（10k）后，PSNR 提升至 19.87，FVD 降至 624.47。更重要的是，Figure 7 显示未筛选数据在约 7k 次迭代后训练崩溃，而高质量数据使训练保持稳定。这证实了消除混杂的全局运动、相机运动与遮挡是习得部件级运动先验的瓶颈所在。

![[assets/figures/papers/paper_list_l18_Puppet_Master_Scaling_Interactive_Video_Generation_as_a_Motion_Prior_for/figures/010_Table_3.jpg]]
*Table 3: Training on more abundant but lower-quality data leads to lower generation quality. Here, ‘w/o Data Curation’ model is trained on Objaverse-Animation while ‘w/ Data Curation’ model is trained on Objaverse-Animation-HQ. Both models are trained for 7k iterations. Evaluation is performed on the test split of Draga-Move*

### 局限性

尽管 Puppet-Master 在部件级运动控制上表现优异，仍存在若干不足：在需要多个部件精确协调的场景（如五片风扇叶片同时旋转）中，模型可能无法保持部件的完整形状；对真实图像推理时，合成资产的风格化纹理与真实图像的颜色分布差异会导致轻微颜色偏差；低分辨率（256×256）推理时，SVD 骨干卷积层的固定感受野可能引发轻微闪烁；当前模型专为内部运动设计，无法处理全局物体位移；所有训练视频使用白色背景，在复杂纹理背景下的生成质量仍有提升空间。

### 补充图表

![[assets/figures/papers/paper_list_l18_Puppet_Master_Scaling_Interactive_Video_Generation_as_a_Motion_Prior_for/figures/001_Figure_1.jpg]]
*Figure 1: Puppet-Master generates videos depicting internal, part-level motion, prompted by one or more drags (arrows). Fine-tuned solely on our curated synthetic Objaverse-Animation-HQ dataset, it generalizes well to real-world scenarios and diverse object categories*

## 定位与知识库关联

Puppet-Master 处于拖拽条件视频生成与部件级运动控制的交叉点，其方法谱系可追溯到三个并行发展的技术线索：基于拖拽的图像/视频生成、基于扩散模型的视频生成基础架构，以及合成数据驱动的运动先验学习。

**与拖拽条件生成基线的关系。** 现有拖拽条件视频生成模型（DragNUWA、DragAnything、Image Conductor）均依赖大规模互联网真实视频进行训练，这些数据中混杂了全局物体位移、相机运动和遮挡，导致模型难以解耦出纯粹的部件级内部运动——它们倾向于将拖拽解释为整体平移或缩放指令。Puppet-Master 的核心突破在于**将训练数据域从混杂的真实视频切换为精心筛选的合成动画数据**（Objaverse-Animation-HQ），从根本上消除了无关运动因素的干扰。这一数据策略与 DragAPart（仅做图像生成，逐帧独立生成导致时间不一致）形成对比：Puppet-Master 在合成数据上微调预训练视频扩散模型，保留了视频生成的时间连续性优势。定量结果显示，在 Drag-a-Move 基准上，Puppet-Master 的 Motion Error 第二部分（全局前景误差）仅为 3.53，而 DragNUWA 为 15.41，差距达 11.88，直接证明了其对部件级运动（而非整体位移）的控制能力。

**架构创新的定位。** Puppet-Master 在 Stable Video Diffusion（SVD）预训练骨干上引入了三个关键模块，各自解决不同的瓶颈问题：（1）**自适应层归一化（drag modulation）** 采用 scale+shift 双参数仿射变换，相比 DragAPart 仅使用 shift 的版本，将 PSNR 从 13.23 提升至 22.98（Tab. 2, A vs B），说明 scale 参数为特征调制提供了关键的灵活性；（2）**drag tokens 交叉注意力** 在原有 CLIP 图像嵌入之外附加 K 个拖拽键值对，增强了空间感知能力，使 PSNR 进一步提升至 24.00（Tab. 2, C vs D）；（3）**all-to-first attention** 将所有帧的查询强制指向第一帧的键值，构建了从干净参考帧到后续帧的信息捷径。消融实验表明，缺少该模块时 FVD 从 205.40 飙升至 624.64（Tab. 2, C vs E），且背景出现严重伪影（Fig. 6），证实了其在微调过程中防止外观退化方面的关键作用。

**适用边界与局限。** 该方法专为**部件级内部运动**设计，当前不具备处理全局物体位移的能力。当输入的拖拽不对应合理的部件级运动时，可能产生视觉伪影。在需要多个部件精确协调运动的场景中（如五片风扇叶片同时旋转），模型可能无法保持部件的完整形状。此外，模型在 256×256 低分辨率下推理时，由于 SVD 骨干卷积层的固定感受野与预训练分辨率（1024×576）不匹配，噪声可能在较大范围内传播，导致轻微闪烁（Fig. 8）。所有训练视频均采用白色背景，虽然模型保留了一定的背景泛化能力，但在复杂纹理背景下的生成质量仍有提升空间。

**开放问题。** 该工作为后续研究留下了若干明确方向：（1）如何设计动态路由机制，将部件级运动与物体整体运动统一到同一生成框架中；（2）在保持部件级运动质量的前提下，如何通过蒸馏、采样加速或模型压缩实现面向实时交互应用的高效推理；（3）该运动先验是否可以扩展到多对象动态场景或交互式视频编辑任务中；（4）如何通过加入随机背景训练或域自适应技术，进一步改善生成视频的颜色一致性与高分辨率细节。

## 原文 PDF

![[paperPDFs/ICCV_2025/Puppet_Master_Scaling_Interactive_Video_Generation_as_a_Motion_Prior_for_Part_Level_Dynamics.pdf]]
