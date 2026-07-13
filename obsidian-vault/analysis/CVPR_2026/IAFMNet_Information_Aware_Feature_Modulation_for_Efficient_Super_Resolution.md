---
title: "IAFMNet: Information-Aware Feature Modulation for Efficient Super-Resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/IAFMNet_Information_Aware_Feature_Modulation_for_Efficient_Super_Resolution.pdf
project_link: null
code_link: null
aliases:
- IAFMNet
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 通过无监督信息熵损失学习到的像素级信息密度映射（IDM），可调控区域计算资源分配与特征调制强度。
primary_logic: 从信息论出发，利用编码代价刻画重建难度，生成信息密度图引导稀疏卷积硬分配和仿射变换软调制，将计算资源集中在高信息密度区域，从而在有限计算预算下提升重建质量。
claims:
- 所估计的IDM能成功捕获误差图中高亮的纹理工整区域，与真实重建困难区高度吻合。
- 引入子流形稀疏卷积（SSConv）在 Manga109 上仅额外 6 GFLOPs 即带来 0.26 dB 的提升，证实信息感知硬分配的高效性。
- Urban100 (×2) 上 PSNR/SSIM = 32.52/0.9312
- Manga109 (×2) 上 PSNR/SSIM = 39.32/0.9792
---

# IAFMNet: Information-Aware Feature Modulation for Efficient Super-Resolution

> [!tip] 核心洞察
> 从信息论出发，利用编码代价刻画重建难度，生成信息密度图引导稀疏卷积硬分配和仿射变换软调制，将计算资源集中在高信息密度区域，从而在有限计算预算下提升重建质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | IAFMNet：基于信息感知特征调制的轻量级超分辨率网络 |
| 英文题名 | IAFMNet: Information-Aware Feature Modulation for Efficient Super-Resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_IAFMNet_Information-Aware_Feature_Modulation_for_Efficient_Super-Resolution_CVPR_2026_paper.html) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | IAFMNet |
| Dataset | Urban100, Manga109 |

> [!tip] 效果简介
> - Urban100 (×2) 上，PSNR/SSIM 32.52/0.9312 vs 32.30/0.9275 (+0.22/+0.0037)。
> - Manga109 (×2) 上，PSNR/SSIM 39.32/0.9792 vs 39.19/0.9774 (+0.13/+0.0018)。

## 概要

现有轻量级图像超分辨率（SISR）方法普遍对所有空间位置分配均等的计算资源，忽略了自然图像中视觉复杂度的空间不均匀性——纹理丰富、边缘密集的区域重建难度远高于平坦区域，这种“一刀切”的计算策略导致高信息区域的误差集中，制约了有限计算预算下的重建质量提升。

针对这一瓶颈，IAFMNet 从信息论视角出发，提出以**像素级信息密度图（Information Density Map, IDM）** 作为区域重建难度的代理信号。IDM 通过最小化无监督信息熵损失 $\mathcal{L}_{IE}$ 学习得到，其核心直觉是：编码代价越高的特征位置，所含信息量越大，重建难度也越高。基于 IDM，网络以**硬分配**（稀疏卷积仅在高信息区域计算）与**软调制**（信息感知仿射变换重校准特征响应）双分支协同的方式，将有限的计算资源精准集中于纹理与边缘等关键区域。

实验表明，IDM 成功捕获了误差图中高亮的纹理区域（Figure 2），验证了其作为重建难度代理的有效性。在 Manga109 ×2 任务上，引入子流形稀疏卷积（SSConv）仅额外增加 6 GFLOPs 即带来 0.26 dB 的提升；完整模型在 Urban100 ×2 上取得 32.52 dB PSNR，较无 IDM 引导的基线提升 0.22 dB。IAFMNet 在多个公开基准上以更低的参数量和计算量，实现了优于 **CARN-M**（Ahn et al., ECCV 2018）、**IMDN**（Hui et al., ACM MM 2019）、**ShuffleMixer**（Sun et al., NeurIPS 2022）、**SAFMN**（Sun et al., ICCV 2023）等代表性轻量级 SR 方法的性能-复杂度权衡。



单图像超分辨率（SISR）旨在从低分辨率观测中恢复高分辨率图像，是底层视觉领域的经典病态逆问题。随着深度学习的普及，大量高性能SR模型相继涌现，但其庞大的参数量和计算开销严重限制了在资源受限设备上的部署。因此，轻量级高效超分方法成为近年来的研究热点。

现有高效超分方法在设计上主要沿两条路径演进：一是通过精巧的卷积模块设计（如通道分裂、信息蒸馏、特征重参数化）来压缩模型体积；二是引入空间自适应调制或注意力机制，使网络对不同区域产生差异化的响应。代表性的轻量级基线包括基于信息蒸馏的 **IMDN**（Hui et al., ACM MM 2019）、采用高效卷积混合的 **ShuffleMixer**（Sun et al., NeurIPS 2022）、空间自适应调制的 **SAFMN**（Sun et al., ICCV 2023），以及自调制特征聚合的 **SMFANet**（Zheng et al., ECCV 2024）等。

然而，上述方法存在一个共性的结构性盲区：**它们对所有空间位置平等地分配计算资源，忽视了视觉信息在空间上的天然不均匀性**。真实图像中，平坦区域（如天空、墙面）包含的信息量极低，仅需少量计算即可准确重建；而纹理密集区域（如毛发、文字、栅格结构）则蕴含丰富的高频信息，是重建误差的集中来源。Figure 2 清晰展示了这一现象：基线模型的重建差异图（difference map）中，高误差区域恰好对应纹理结构密集的位置。当网络对所有像素一视同仁地执行相同深度的特征提取时，大量算力被浪费在低信息区域，而真正需要精细建模的高信息区域却得不到足够的计算资源。

该问题的本质在于缺乏一个有效的**区域重要性度量**来指导计算资源的差异化分配。传统方法通常依赖梯度算子（如 Sobel、Laplacian）生成边缘图作为先验，但这些手工设计的算子仅能捕获局部强度变化，无法从信息论角度刻画区域的编码难度与重建价值（见 Figure 7 对比）。因此，如何以无监督方式学习一个能准确反映像素级重建难度的信息密度信号，并据此实现计算资源的硬分配与特征响应的软调制，成为突破现有高效SR性能瓶颈的关键切入点。

IAFMNet 正是从这一动机出发，首次从信息密度视角审视退化特征增强问题，提出以无监督信息熵损失驱动的像素级信息密度图（IDM）作为核心调控信号，协同引导稀疏卷积的显式计算分配与仿射变换的隐式特征重校准，从而在有限计算预算下实现重建质量的显著提升。



## 核心方法与创新机理

IAFMNet 的核心创新在于将**信息密度感知**引入轻量级超分辨率网络的特征调制机制，从根本上改变了传统方法对图像空间均匀分配计算资源的范式。其关键创新可归纳为三个紧密耦合的 changed slots。

### 1. 无监督信息密度图（IDM）作为引导信号

传统高效超分方法通常缺乏显式的空间重要性引导，或仅依赖 Sobel、Laplacian 等基于梯度的边缘检测算子。这些算子对纹理丰富但梯度不显著的区域（如规律性纹理、平坦区域的细微变化）捕获能力有限（见 Figure 7）。IAFMNet 提出通过最小化**无监督信息熵损失**（$\mathcal{L}_{IE}$）来估计像素级**信息密度图（IDM）**。

其理论依据源自信息论：信号 $x$ 的信息量为 $I(x) = -\log_2 p(x)$，编码代价可表示为近似分布与真实分布的交叉熵：

$$R = \mathbb{E}_{\hat{x} \sim m}[-\log_2 p_{\hat{x}}(\hat{x})] = H(m) + D_{KL}(m \| p_{\hat{x}})$$

具体实现中，信息密度估计器（IDE）假设量化特征 $\hat{F}_i$ 服从独立高斯分布 $\mathcal{N}(\mu_i, \theta_i)$，其似然为：

$$p_{\hat{F}_i}(\hat{F}_i \mid \mu_i, \theta_i) = \Phi\left(\frac{\hat{F}_i + \frac{1}{2} - \mu_i}{\theta_i}\right) - \Phi\left(\frac{\hat{F}_i - \frac{1}{2} - \mu_i}{\theta_i}\right)$$

信息熵损失即为所有空间位置编码代价之和：

$$\mathcal{L}_{IE} = \sum_i -\log_2 p_{\hat{F}_i}(\hat{F}_i \mid \mu_i, \theta_i)$$

通过最小化 $\mathcal{L}_{IE}$，$\theta_i$ 自然收敛为反映该位置信息密度（即重建难度）的估计。Figure 2 提供了决定性证据：估计的 IDM 与基线模型重建误差图中高亮的纹理区域高度吻合，证实其能有效捕获真实重建困难区（置信度 0.95）。

### 2. 信息引导的硬性资源分配（IGRA）

传统方法对所有空间位置执行统一卷积计算，在平坦区域浪费大量计算资源。IAFMNet 的**信息引导资源分配（IGRA）**分支利用 IDM 生成二值掩膜 $\mathbf{M} = \mathcal{T}(\theta, k)$，仅保留信息密度最高的 top-$k$% 位置，其余位置直接跳过计算。

被选中的稀疏特征通过**子流形稀疏卷积（SSConv）**处理，其输出仅在掩膜激活位置计算：

$$\mathbf{F}_{\mathrm{ssc}}(p) = \begin{cases} \sum_{q \in \mathcal{N}(p)} \mathbf{W}(q-p) \cdot \mathbf{F}_{\mathrm{sparse}}(q) + \mathbf{F}_1(p), & \text{if } \mathbf{M}(p)=1 \\ \quad & \text{otherwise} \end{cases}$$

这一硬分配策略的核心优势在于**计算资源与信息密度直接挂钩**。消融实验证实，引入 SSConv 在 Manga109 上仅额外增加 6 GFLOPs 即带来 **0.26 dB** 的提升（Table 4，置信度 0.95），5% 的稀疏阈值在性能与计算量之间取得最佳平衡。

### 3. 信息感知的软性特征调制（ARM）

与硬分配的“计算或不计算”互补，**仿射重校准模块（ARM）**对特征进行软性调制。ARM 将输入特征拆分后，利用 IDM 与特征拼接生成通道级仿射尺度：

$$s = \mathrm{Conv}_{1\times1}([S(\mathrm{Conv}_{1\times1}(\mathbf{F}_2))[0], \theta])$$

同时通过深度可分离卷积提取局部结构特征：

$$\mathbf{F}_{\mathrm{local}} = \mathrm{DWConv}(S(\mathrm{Conv}_{1\times1}(\mathbf{F}_2))[1])$$

最终通过逐通道乘法 $\mathbf{F}_{\mathrm{ARM}} = \mathbf{F}_{\mathrm{local}} \odot s$ 实现信息感知的特征重校准。消融实验表明，在 ARM 中加入 IDM 引导可额外带来 **0.06 dB** 提升（Manga109），且几乎无计算开销（Table 5，置信度 0.95）。

### 创新协同机制

三个 changed slots 形成闭环协同：**IDE 提供空间重要性先验 → IGRA 根据该先验进行硬性计算分配 → ARM 利用同一先验进行软性特征调制**。这种“硬分配+软调制”的双分支设计，使 IAFMNet 在 Urban100（×2）上相比无 IDM 引导的基线提升 **+0.22 dB** PSNR（32.52 vs. 32.30），同时保持计算效率。



IAFMNet 的整体架构遵循轻量级超分辨率网络的主流设计范式，但其核心创新在于引入了**信息密度图（Information Density Map, IDM）** 作为全局引导信号，驱动双分支特征增强模块进行区域自适应的计算分配与特征调制。整个 pipeline 由四个关键阶段构成：浅层特征提取、信息密度估计、信息引导特征增强、以及图像重建。

### 网络结构总览

给定低分辨率输入 $I_{LR} \in \mathbb{R}^{H \times W \times 3}$，首先通过一个 $3 \times 3$ 卷积层提取浅层特征 $F_0 \in \mathbb{R}^{H \times W \times C}$。该特征随后被送入**信息密度估计器（Information Density Estimator, IDE）**，并行输出两个关键信号：均值特征图 $\mu$ 和信息密度图 $\theta$。

$\theta$ 作为全局引导信号贯穿整个特征增强阶段。网络堆叠 $N$ 个**信息引导特征增强块（Information-guided Feature Enhancement Block, IFEB）**，每个 IFEB 包含两个子模块：**信息引导特征增强模块（IFEM）** 和**通道门控前馈网络（CGFN）**。IFEM 是核心计算单元，内部采用双分支设计——信息引导资源分配（IGRA）分支和仿射重校准模块（ARM）分支——分别实现硬性的稀疏计算分配与软性的特征调制。

经过 $N$ 个 IFEB 的逐步细化后，输出的增强特征与 IDE 生成的均值特征图 $\mu$ 进行融合，最终通过一个轻量卷积层和 PixelShuffle 上采样操作重建高分辨率图像 $I_{SR}$。

### 信息密度估计器（IDE）：引导信号的生成

IDE 是 IAFMNet 区别于现有方法的关键组件。其设计动机源于信息论：图像中纹理丰富、边缘锐利的区域包含更多信息量，编码代价更高，因而需要更多的计算资源。IDE 通过对浅层特征 $F_0$ 建模其概率分布，以编码代价作为信息密度的代理指标。

具体而言，IDE 假设量化后的特征图 $\hat{F}$ 的每个元素服从独立高斯分布，参数化为均值 $\mu_i$ 和尺度 $\theta_i$（即信息密度）。通过引入均匀噪声模拟量化过程，每个特征元素的似然为：

$$p_{\hat{F}_i}(\hat{F}_i \mid \mu_i, \theta_i) = \Phi\left(\frac{\hat{F}_i + \frac{1}{2} - \mu_i}{\theta_i}\right) - \Phi\left(\frac{\hat{F}_i - \frac{1}{2} - \mu_i}{\theta_i}\right)$$

其中 $\Phi$ 为标准正态分布的累积分布函数。基于此，定义**信息熵损失（Information Entropy Loss）** 为所有空间位置编码代价之和：

$$\mathcal{L}_{IE} = \sum_i -\log_2 p_{\hat{F}_i}(\hat{F}_i \mid \mu_i, \theta_i)$$

该损失等价于近似分布与真实分布之间的交叉熵：$R = H(m) + D_{KL}(m \| p_{\hat{x}})$。通过最小化 $\mathcal{L}_{IE}$，IDE 以无监督方式学习输出 $\theta$，其值越大表示该位置的信息密度越高、重建难度越大。可视化验证表明，所估计的 IDM 能成功捕获误差图中高亮的纹理与边缘区域，与真实重建困难区高度吻合。

### 信息引导特征增强块（IFEB）：双分支协同设计

每个 IFEB 接收前一阶段的特征 $F_{in}$ 和全局 IDM $\theta$，通过 IFEM 进行信息感知增强，再由 CGFN 进行通道维度的门控精炼。

**IFEM 的双分支分流机制**：输入特征首先经过卷积扩展通道，随后被拆分为两部分 $F_1$ 和 $F_2$，分别送入 IGRA 和 ARM 分支：

$$\mathbf{F}_1, \mathbf{F}_2 = \mathcal{S}(\mathrm{Conv}(\mathbf{F}_{\mathrm{in}})), \quad \mathbf{F}_2' = \mathrm{ARM}(\mathbf{F}_2), \quad \mathbf{F}_1' = \mathrm{IGRA}(\mathbf{F}_1)$$

两支输出通过加法融合，形成 IFEM 的最终输出。这一设计实现了硬分配与软调制的协同互补：IGRA 通过稀疏卷积将计算资源集中到高信息密度区域，ARM 则通过信息感知的仿射变换对所有位置进行细粒度特征重校准。

### 图像重建与训练策略

经过所有 IFEB 处理后，增强特征与 IDE 输出的均值特征图 $\mu$ 进行融合，随后通过一个轻量卷积层和 PixelShuffle 操作完成上采样重建。训练采用联合损失函数：

$$\mathcal{L} = \mathcal{L}_1 + \lambda \mathcal{L}_{IE}$$

其中 $\mathcal{L}_1$ 为像素级 L1 重建损失，$\mathcal{L}_{IE}$ 为信息熵损失，$\lambda$ 为平衡权重。所有模型在 DF2K 数据集上以标准协议训练（$64 \times 64$ LR 图像块，随机翻转和旋转），测试集采用 Set5、Set14、BSD100、Urban100 和 Manga109，评估指标为 Y 通道 PSNR/SSIM。

### 补充图表

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the proposed IAFMNet: (a) the overall network architecture, (b) the information density estimator, and (c) the information-guided feature enhancement module*



IAFMNet 的核心设计围绕一个中心假设展开：图像不同区域的重建难度由其信息密度决定，计算资源应当向高信息密度区域倾斜。本章从信息论视角出发，依次阐述信息密度估计器（IDE）、信息引导特征增强模块（IFEM）及其内部的两个互补分支——信息引导资源分配（IGRA）与仿射重校准模块（ARM）。

### 3.1 信息密度估计器（IDE）

IDE 是整个框架的感知核心，其任务是为输入特征图的每个空间位置赋予一个信息密度值。设计思路源于信息论中“信息量”的定义：信号 $x$ 的信息量由其负对数概率给出，即 $I(x) = -\log_2 p(x)$。在图像编码中，编码代价越高，意味着该区域包含的信息越丰富，重建难度也越大。

具体而言，IDE 将浅层特征 $F_0$ 经过卷积与广义分裂归一化（GDN）层处理后，并行输出两个量：均值特征图 $\mu$ 和信息密度图 $\theta$。在独立高斯假设下，量化特征 $\hat{F}_i$ 的概率似然建模为：

$$p_{\hat{F}_i}(\hat{F}_i \mid \mu_i, \theta_i) = \Phi\left(\frac{\hat{F}_i + \frac{1}{2} - \mu_i}{\theta_i}\right) - \Phi\left(\frac{\hat{F}_i - \frac{1}{2} - \mu_i}{\theta_i}\right)$$

其中 $\Phi(\cdot)$ 为标准正态分布的累积分布函数，$\theta_i$ 在此处作为尺度参数，直接反映了该位置特征分布的不确定性——$\theta_i$ 越大，特征值越分散，编码所需比特数越高，信息密度也就越大。所有空间位置的编码代价之和构成信息熵损失：

$$\mathcal{L}_{IE} = \sum_i -\log_2 p_{\hat{F}_i}(\hat{F}_i \mid \mu_i, \theta_i)$$

该损失以完全无监督的方式驱动 IDE 学习：无需任何显式标注，网络通过最小化自身特征的编码代价，自动发现哪些区域包含难以压缩的纹理与边缘信息。Figure 2 的可视化证实了这一点：由 $\mathcal{L}_{IE}$ 训练得到的 $\theta$ 图与基线模型的重建误差图高度吻合，说明 IDE 确实捕获了真正的重建困难区。Figure 7 进一步表明，与传统 Sobel、Laplacian 等梯度算子相比，IDM 能有效凸显被简单边缘检测器忽略的信息丰富纹理。

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the difference map (d) between the HR image and the SR image (b) reconstructed by baseline f(·) on Urban100. The estimated IDM θ in (e), obtained via*

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/009_Figure_7.jpg]]
*Figure 7: Visual comparison of the proposed Information Density Map (IDM) with traditional gradient-based operators (Sobel and Laplacian). The IDM effectively highlights information-rich textures that are often overlooked by simple edge detectors*

### 3.2 信息引导特征增强模块（IFEM）

每个 IFEB（信息引导特征增强块）包含一个 IFEM 和一个通道门控前馈网络（CGFN）。IFEM 是信息感知调制的执行单元，其处理流程为：输入特征 $F_{in}$ 经卷积扩展后，沿通道维度拆分为 $F_1$ 和 $F_2$，分别送入 IGRA 和 ARM 两个分支：

$$\mathbf{F}_1, \mathbf{F}_2 = \mathcal{S}(\mathrm{Conv}(\mathbf{F}_{\mathrm{in}})), \quad \mathbf{F}_2' = \mathrm{ARM}(\mathbf{F}_2), \quad \mathbf{F}_1' = \mathrm{IGRA}(\mathbf{F}_1)$$

两分支输出相加后与残差连接融合，形成 IFEM 的最终输出。这种“硬分配 + 软调制”的双分支协同设计是 IAFMNet 区别于现有方法的关键：IGRA 通过稀疏卷积实现计算资源的显式重分配，ARM 则通过仿射变换对特征进行隐式的精细校准，二者均受同一 IDM 的引导。

### 3.3 信息引导资源分配（IGRA）

IGRA 分支实现“硬分配”：根据 IDM 的值，仅对信息最丰富的前 $k\%$ 空间位置执行卷积计算。具体步骤为：首先从 $\theta$ 生成二值掩膜 $\mathbf{M} = \mathcal{T}(\theta, k)$，激活值最高的 $k\%$ 位置；然后将 $F_1$ 中对应位置的特征提取为稀疏表示 $F_{sparse}$，送入子流形稀疏卷积（Submanifold Sparse Convolution, SSC）层。SSC 仅在 $\mathbf{M}(p)=1$ 的位置进行卷积运算：

$$\mathbf{F}_{\mathrm{ssc}}(p) = \begin{cases} \sum_{q \in \mathcal{N}(p)} \mathbf{W}(q-p) \cdot \mathbf{F}_{\mathrm{sparse}}(q) + \mathbf{F}_1(p), & \text{if } \mathbf{M}(p)=1 \\ \quad & \text{otherwise} \end{cases}$$

对于 $\mathbf{M}(p)=0$ 的低信息区域，特征直接跳过卷积计算，仅保留残差连接。消融实验（Table 4）表明，$k=5\%$ 的稀疏阈值在性能和计算量之间取得最佳平衡：在 Manga109 数据集上，引入 SSC 仅增加 6 GFLOPs 即带来 0.26 dB 的 PSNR 提升，证实了信息感知硬分配的高效性。稀疏输出随后与降采样 IDM 生成的注意力图融合，进一步细化激活区域的特征表达：

$$\mathbf{A} = \mathrm{Upsample}(\mathrm{Conv}_{1\times1}(\mathbf{F}_{\mathcal{D}} + \boldsymbol{\theta}_{\mathcal{D}}))$$

### 3.4 仿射重校准模块（ARM）

ARM 分支实现“软调制”：不改变计算的空间分布，而是利用 IDM 生成通道级的仿射变换参数，对局部特征进行精细重校准。具体流程为：将 $F_2$ 经 $1\times1$ 卷积后沿通道拆分为两部分。第一部分与 IDM $\theta$ 拼接后，通过 $1\times1$ 卷积生成信息感知的尺度因子 $s$：

$$s = \mathrm{Conv}_{1\times1}([S(\mathrm{Conv}_{1\times1}(\mathbf{F}_2))[0], \theta])$$

第二部分通过深度可分离卷积提取局部结构特征：

$$\mathbf{F}_{\mathrm{local}} = \mathrm{DWConv}(S(\mathrm{Conv}_{1\times1}(\mathbf{F}_2))[1])$$

最终，ARM 的输出由局部特征与信息感知尺度的逐元素乘积得到：$\mathbf{F}_{ARM} = \mathbf{F}_{local} \odot s$。消融实验（Table 5）显示，在已有 ARM 的基础上引入 IDM 引导，在 Manga109 上额外带来 0.06 dB 提升，且几乎不增加计算开销，验证了信息感知软调制的有效性。

### 3.5 训练损失

整体网络以 $L_1$ 像素损失与信息熵损失的加权和进行端到端训练：

$$\mathcal{L} = \mathcal{L}_1 + \lambda \mathcal{L}_{IE}$$

其中 $\lambda$ 为平衡两项损失的权重系数。$L_1$ 损失保证重建图像与真值的像素级一致性，$\mathcal{L}_{IE}$ 则驱动 IDE 无监督地学习信息密度分布，无需任何额外的密度标注。

### 补充图表

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of the proposed information-aware sparse convolution module*

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of progressive feature enhancement via IDM-guided sparse allocation and soft modulation*



## 实验与关键发现

### 核心结果与效率权衡

IAFMNet 在五个标准基准（Set5、Set14、BSD100、Urban100、Manga109）上以轻量级参数量取得了具有竞争力的重建性能。在 ×2 放大任务中，IAFMNet 在 Urban100 上达到 **32.52 dB PSNR**，较其消融基线（仅含 ARM 而无 IDM 引导）提升 **+0.22 dB**；在纹理密集的 Manga109 上达到 **39.32 dB PSNR**，提升 **+0.13 dB**。这些增益源自信息密度图对富纹理区域的精准定位与资源倾斜。

在效率维度，IAFMNet 的核心优势体现为“将有限 FLOPs 集中投放到高信息密度区域”。消融实验（Table 4）表明，引入子流形稀疏卷积（SSConv）仅额外增加 **6 GFLOPs**，即在 Manga109 上带来 **0.26 dB** 的显著提升，验证了信息感知硬分配策略的高效性。5% 的稀疏阈值被证实为性能与计算量的最佳平衡点——更高的稀疏度虽可进一步降低计算，但会因丢失过多低频结构信息而导致性能退化。

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/010_Table_4.jpg]]
*Table 4: Ablation studies on different settings in IGRA*

### 关键模块消融

**信息密度估计器（IDE）结构选择**（Table 3）：对比纯卷积与卷积-GDN 混合设计，采用“卷积 + GDN”的 IDE 配置在 Set5 和 Urban100 上均获得最优 PSNR，表明广义除法归一化（GDN）层对高斯化特征分布、提升似然估计精度具有实质贡献。

**信息引导资源分配（IGRA）**（Table 4）：除稀疏阈值外，消融还考察了稀疏卷积类型与掩膜生成策略。替换为标准稀疏卷积或随机掩膜均导致性能显著下降，证实子流形稀疏卷积的保结构特性与 IDM 引导的必要性。

**仿射重校准模块（ARM）**（Table 5）：在 ARM 中引入 IDM 引导的尺度生成，较无引导版本在 Manga109 上额外带来 **0.06 dB** 提升，且几乎不增加计算开销。该增益源于 IDM 提供的像素级信息密度信号使仿射调制能差异化地增强纹理区域、抑制平坦区域的噪声放大。可视化消融（Figure 8）进一步显示，移除 IDM 引导后，重建图像在边缘和纹理区域出现明显模糊或伪影。

### 信息密度图的有效性验证

Figure 2 提供了 IDM 有效性的直接证据：基线模型重建的 SR 图像与 HR 图像之间的差异图（difference map）高亮区域恰好对应纹理和边缘等重建困难区，而无监督信息熵损失 $\mathcal{L}_{IE}$ 估计的 IDM $\theta$ 成功捕获了这些区域，且 IAFMNet 在 IDM 引导下的重建结果（Figure 2(c)）显著优于基线。Figure 7 将 IDM 与传统梯度算子（Sobel、Laplacian）进行对比，表明 IDM 能有效突出传统边缘检测器遗漏的富信息纹理，验证了基于编码代价的信息度量相比启发式梯度的优越性。

### 失败模式与局限性

尽管 IDM 能有效定位信息密集区域，其基于编码成本的度量标准并不完全等价于人眼感知重要性——某些高编码代价区域可能对应噪声或非结构化纹理，导致资源分配并非总是感知最优。此外，硬阈值掩膜 $T(\theta, k)$ 引入的二元决策在低稀疏阈值下可能截断部分低频结构信息，表现为平坦区域的过度平滑或块状伪影。该问题在 ×4 大放大因子下更为突出，因为此时输入 LR 图像中的可用信息本就极度匮乏，稀疏卷积可能进一步加剧信息丢失。

### 补充图表

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/006_Table_1.jpg]]
*Table 1: Comparison with SOTA lightweight SR methods on public benchmark datasets. Best results are colored with red*

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/007_Table_2.jpg]]
*Table 2: Performance comparison against lightweight CNN- and ViT-based SR methods on public benchmark datasets. Best and second-best results are colored with red and blue*

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/012_Table_5.jpg]]
*Table 5: Ablation studies on different settings in ARM*

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/013_Figure_8.jpg]]
*Figure 8: Visual comparison of the ablation study results. Zoom in for better visualization*

![[assets/figures/papers/paper_list_l886_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_IAFMNet_Information/figures/001_Figure_1.jpg]]
*Figure 1: Performance and model complexity comparison on the Manga109 [22] dataset for ×4 super-resolution*



## 定位与知识库关联

### 1. 与现有工作的关系

IAFMNet 的核心贡献在于将**信息密度**作为显式引导信号引入高效超分辨率重建，这与以往轻量级 SR 方法形成了清晰的继承与分叉关系。

**与轻量级 CNN 基线的关系。** 在架构骨架层面，IAFMNet 继承了轻量级 SR 的经典设计范式——浅层特征提取、深层特征增强、PixelShuffle 上采样重建。其直接对比的 CNN 基线包括 **CARN-M**（Ahn et al., ECCV 2018）、**IMDN**（Hui et al., ACM MM 2019）和 **ShuffleMixer**（Sun et al., NeurIPS 2022）。这些方法的核心瓶颈在于：它们对特征图上所有空间位置执行**均等的卷积计算**，忽略了纹理丰富区域与平滑区域之间重建难度的巨大差异。IAFMNet 的突破在于打破了这一均等假设——通过信息密度图（IDM）识别高信息区域，将有限的计算预算进行**非均匀分配**。

**与空间自适应调制方法的关系。** 在特征调制层面，IAFMNet 与 **SAFMN**（Sun et al., ICCV 2023）和 **SMFANet**（Zheng et al., ECCV 2024）共享“自适应特征重校准”的设计意图。但关键差异在于**引导信号的来源与性质**：SAFMN 和 SMFANet 的调制参数由特征本身通过注意力机制生成，属于自监督的信号；而 IAFMNet 的仿射重校准模块（ARM）直接受 IDM 引导——IDM 是通过最小化信息熵损失 $\mathcal{L}_{IE}$ 无监督学习得到的，其物理含义是**编码代价的空间分布**，而非简单的特征统计量。这一差异使得 IAFMNet 的调制具有了信息论意义上的可解释性。

**与专家挖掘方法的关系。** **SeemoRe**（Zamfir et al., ICML 2024）通过多专家机制对不同难度的区域进行差异化处理，其“专家挖掘”思想与 IAFMNet 的“信息感知资源分配”在目标上一致——都是将计算资源集中于困难区域。但实现路径截然不同：SeemoRe 依赖多个专家网络的路由选择，而 IAFMNet 使用单一网络内的**稀疏卷积硬分配 + 仿射变换软调制**双分支协同机制，避免了多专家的参数冗余。

**与轻量级 Transformer 的关系。** **SRFormer-light**（Zhou et al., ICCV 2023）代表了轻量级 SR 的 Transformer 路线。IAFMNet 与这类方法的关系是**互补而非对抗**：IDM 作为通用引导信号，理论上可以与 Transformer 的自注意力机制结合——例如，仅在 IDM 高响应区域计算注意力，或使用 IDM 调制注意力权重。这已被列为开放问题。

**方法谱系总结。** IAFMNet 处于“自适应特征增强”与“信息论引导”的交汇点。其上游是均等计算的轻量级 CNN 和自注意力的空间调制方法，下游则指向信息感知的稀疏计算范式。从引导信号的角度看，IDM 替代了传统的梯度算子（Sobel、Laplacian）——Figure 7 的对比表明，传统边缘检测器会遗漏大量信息丰富的纹理区域，而 IDM 能有效捕获这些区域。

### 2. 适用边界与局限

**计算效率边界。** IAFMNet 的优势在**视觉复杂度高度不均匀**的场景中最为显著。例如，Urban100 数据集包含大量建筑纹理和重复结构，信息密度分布极不均匀，IAFMNet 在此类数据上取得了 +0.22 dB 的提升（×2，PSNR 32.52 vs. 32.30）。相反，在纹理较为均匀的自然图像（如 BSD100）上，信息密度的空间变异性较低，稀疏分配的收益可能被稀释。

**稀疏阈值的敏感性。** 消融实验表明，5% 的稀疏阈值在性能和计算量之间取得最佳平衡（Table 4）。这一阈值是**经验性的**，其最优值可能随数据集和放大倍数变化。过低的阈值会丢失关键的低频结构信息，导致过度平滑；过高的阈值则退化为密集卷积，失去效率优势。该超参数需要针对具体场景进行调优。

**信息密度估计的局限性。** IDM 基于编码代价学习，其优化目标是 $\mathcal{L}_{IE} = \sum_i -\log_2 p_{\hat{F}_i}(\hat{F}_i \mid \mu_i, \theta_i)$——即最小化量化特征的负对数似然。这一目标与**像素级重建精度**高度相关，但与人眼感知质量并不完全一致。在某些情况下，人眼关注的结构性纹理可能编码代价较低，而高频噪声的编码代价反而较高。这意味着 IDM 可能对感知不重要的高频噪声过度敏感。

**硬性阈值的信息丢失风险。** IGRA 分支通过二值掩膜 $\mathbf{M} = T(\theta, k)$ 进行硬性稀疏选择，被排除的位置完全不参与稀疏卷积计算。这种“全有或全无”的分配策略可能导致**低频结构信息的永久丢失**——某些对整体结构重要但局部信息密度略低的区域可能被错误排除，且后续层无法恢复这些信息。ARM 分支的软调制部分缓解了这一问题，但两个分支的信息流是并行的，ARM 无法直接补偿 IGRA 的硬性丢失。

**泛化到其他任务的障碍。** 当前 IDM 的训练依赖于超分辨率任务中的 L1 像素损失与信息熵损失的联合优化 $\mathcal{L} = \mathcal{L}_1 + \lambda \mathcal{L}_{IE}$。将其推广到去噪、去模糊等任务时，需要重新设计信息密度与任务损失之间的耦合机制，且编码代价的分布特性可能因退化类型不同而发生显著变化。

### 3. 开放问题

**IDM 与长程依赖机制的结合。** IAFMNet 目前基于纯卷积架构，IDM 引导的稀疏卷积仅在局部邻域内操作。一个自然的问题是：IDM 能否与 Transformer 的自注意力机制结合？例如，使用 IDM 筛选参与注意力计算的 key-value 对，或使用 IDM 调制注意力权重的温度参数。这可能进一步提升对长程纹理结构的建模能力，同时保持计算效率。

**信息感知调制在其他复原任务中的推广。** 信息密度作为重建难度的代理指标，其核心假设——编码代价高的区域重建难度大——在去噪、去模糊、压缩伪影去除等任务中是否仍然成立？这些任务的退化模式与下采样有本质不同，编码代价的空间分布可能反映的是噪声强度或模糊核的局部特性，而非纹理复杂度。验证这一假设需要系统的跨任务实验。

**软硬协同机制的进一步探索。** 当前的 IGRA（硬分配）和 ARM（软调制）以并行分支的方式协同工作，两者之间的信息交互仅通过共享的 IDM 实现。是否存在更紧密的耦合方式？例如，使用 ARM 的输出动态调整 IGRA 的稀疏阈值，或使用 IGRA 的稀疏选择结果反向指导 ARM 的调制强度——这可能在保持效率的同时进一步减少硬性阈值的信息丢失。

**感知对齐的信息密度估计。** 当前 IDM 的优化目标完全基于信息论编码代价，与人眼感知存在偏差。一个值得探索的方向是将感知损失（如 LPIPS）或对抗损失引入 IDM 的学习过程，使信息密度图更准确地反映人眼关注的区域。这需要在编码代价的数学优雅性与感知对齐的经验有效性之间找到平衡。



## 原文 PDF

![[paperPDFs/CVPR_2026/IAFMNet_Information_Aware_Feature_Modulation_for_Efficient_Super_Resolution.pdf]]
