---
title: "DCT-Net: Domain-calibrated Translation for Portrait Stylization"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/DCT_Net_Domain_calibrated_Translation_for_Portrait_Stylization.pdf
project_link: null
code_link: "https://github.com/menyifang/DCT-Net"
aliases:
- DN
- DCT-Net
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 域校准策略：先通过内容校准（CCN）将目标域分布拉近源域分布，再利用几何扩展（GEM）打破空间约束，最后在已校准的域对上学习局部纹理翻译。
primary_logic: “先校准，后翻译”：利用源域丰富先验校准目标域的内容分布，并通过几何变换扩大空间多样性，将跨域全局映射转化为像素级局部纹理转换，实现高保真、强泛化的少样本肖像风格化。
claims:
- 消融实验表明，移除内容校准网络（CCN）会导致FID从35.92急剧上升至58.52，身份一致性（ID）从0.71降至0.58，验证了内容校准的关键作用。
- 用户研究中超过80%的参与者认为DCT-Net的结果在风格化效果和内容保留方面均优于其他方法，表明其主观质量优势。
- 方法仅使用头部训练样本即可推广到全身体图像翻译，且效果和谐、变形自适应，证明校准策略有效缓解了分布偏差。
- CelebA (5000 images) 上 FID = 35.92
---

# DCT-Net: Domain-calibrated Translation for Portrait Stylization

> [!tip] 核心洞察
> “先校准，后翻译”：利用源域丰富先验校准目标域的内容分布，并通过几何变换扩大空间多样性，将跨域全局映射转化为像素级局部纹理转换，实现高保真、强泛化的少样本肖像风格化。

| 字段 | 内容 |
|------|------|
| 中文题名 | DCT-Net: 域校准图像翻译用于肖像风格化 |
| 英文题名 | DCT-Net: Domain-calibrated Translation for Portrait Stylization |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://menyifang.github.io/projects/DCTNet/DCTNet.html) · [Code](https://github.com/menyifang/DCT-Net) |
| Topic | #topic/other_unclear |
| Method | DCT-Net |
| Dataset | CelebA |

> [!tip] 效果简介
> - CelebA (5000 images) 上，FID 35.92 vs CycleGAN, U-GAT-IT, Toonify, PSP (exact values in Table 1) (N/A (DCT-Net achieves lowest FID))；ID 0.71 vs CycleGAN, U-GAT-IT, Toonify, PSP (exact values in Table 1) (N/A (DCT-Net achieves highest ID))。
> - 用户研究 (20 participants) 上，Pref. A (Stylization preference) 82.6% vs other competing methods (< 20% each) (> ~70% above chance level)；Pref. B (Content preservation) 90.5% vs other competing methods (< 10% each) (> ~80% above chance level)。

## 概要

**问题**：在少样本条件下，目标风格域样本分布严重偏差且多样性不足，现有图像翻译方法易出现过拟合、内容（身份、配饰）丢失，且难以泛化至复杂真实场景。

**方法**：提出 DCT-Net，核心思想为“先校准，后翻译”。首先通过内容校准网络（CCN）利用预训练 StyleGAN2 生成器微调至目标域，生成与源域内容对称的目标样本，校准内容分布；再通过几何扩展模块（GEM）施加随机缩放与旋转，释放空间约束；最后在已校准的域对上，以 U-Net 架构的纹理翻译网络（TTN）学习像素级局部纹理转换，结合风格、内容、面部感知及全变分损失进行无监督训练。

**主要结果**：在 CelebA 数据集上，DCT-Net 取得最低 FID（35.92）和最高身份一致性 ID（0.71）；用户研究中，风格化偏好达 82.6%，内容保留偏好达 90.5%，显著优于 CycleGAN、U-GAT-IT、Toonify、PSP 等基线方法。仅使用头部训练样本即可泛化至全身体图像翻译。

**方法定位**：该方法将少样本肖像风格化从“全局域映射”转化为“局部纹理转换”，通过域校准策略缓解目标分布偏差，属于无需反演的端到端翻译范式，与基于 GAN 反演或常规图像翻译的基线形成明确区分。

## 核心方法与创新机理

### 问题背景与核心瓶颈

少样本肖像风格化的根本困难在于**目标域分布的系统性偏差**。当仅有约100张风格样本时，目标域在内容维度（身份、配饰、姿态）上形成极度稀疏且有偏的分布，而源域（真实人脸）则覆盖了丰富多样的内容变化。这种分布不对称导致三个连锁问题：

1. **过拟合**：翻译网络记忆有限的风格样本，无法泛化到未见姿态或遮挡；
2. **内容丢失**：身份特征、眼镜、帽子等细节在跨域映射中被扭曲或抹除；
3. **空间约束僵化**：模型学习到固定的空间对应关系，难以处理全身体图像或大幅姿态变化。

现有方法（如CycleGAN、U-GAT-IT、Toonify、PSP、AgileGAN）或依赖GAN反演嵌入，或直接在偏差分布上训练翻译网络，均未能从根本上解决分布不对称问题。

### 核心创新：“先校准，后翻译”

DCT-Net提出**域校准翻译**（Domain-calibrated Translation）范式，将跨域风格化分解为两个阶段：首先利用源域丰富先验**校准**目标域的内容分布与几何分布，然后在已对齐的域对上学习**局部纹理翻译**。这一策略将困难的全局跨域映射转化为可控的像素级纹理转换，从根本上缓解了少样本条件下的分布偏差问题。

核心因果链为：
- **内容校准网络（CCN）** 将目标域分布拉近源域 → 提供内容对称的合成目标样本；
- **几何扩展模块（GEM）** 打破空间位置约束 → 增强几何对称性与泛化能力；
- **纹理翻译网络（TTN）** 在已校准域对上学习局部纹理映射 → 实现高保真风格化。

### Changed Slots：与基线方法的关键差异

**Slot 1：目标域分布处理方式**

基线方法直接使用少量真实风格样本训练翻译网络（如CycleGAN、U-GAT-IT），或依赖StyleGAN反演将源图像嵌入目标域潜在空间（如Toonify、PSP）。这些方法要么过拟合有限样本，要么因反演不精确导致身份丢失。

DCT-Net的CCN模块通过**迁移学习**微调预训练的StyleGAN2源域生成器$G_s$，使其适应目标风格域。具体而言，CCN冻结$G_s$的卷积权重（保留内容先验），仅微调仿射变换层中的风格调制参数，使生成器能够产生与源域共享内容分布（身份、姿态、配饰）但具有目标风格纹理的合成样本$\hat{x}_t$。这一过程无需成对数据，仅需少量目标域真实样本作为风格参考。

**Slot 2：翻译网络架构与监督方式**

基线方法多采用编码器-解码器结构结合反演损失（如PSP、AgileGAN），训练复杂且不稳定。DCT-Net的TTN采用简洁的**U-Net架构**，直接在CCN生成的合成源-目标对$(\tilde{x}_s, \hat{x}_t)$上进行无监督训练，无需反演步骤。训练数据由10,000张FFHQ源域图像和混合目标域（约100张真实风格样本 + 10,000张CCN生成的合成样本）组成。

**Slot 3：几何约束处理**

现有方法通常隐式学习空间对应关系，对姿态变化和全身体图像敏感。DCT-Net通过GEM显式施加随机缩放（0.8-1.2倍）和旋转（-15°至15°）变换，主动扩展两个域的几何分布，迫使TTN学习姿态无关的局部纹理映射，从而天然支持全身体翻译。

### 模块顺序与训练/推理路径

**训练阶段**分为两个独立步骤：

**Step 1：内容校准网络（CCN）训练**

CCN以预训练的StyleGAN2源域生成器$G_s$为起点，通过以下损失函数微调至目标域：
- **风格损失**：约束生成图像的风格特征与目标域真实样本一致；
- **内容保留损失**：冻结卷积权重的隐式约束确保内容结构不变。

训练完成后，CCN可生成任意源域图像对应的“内容对称”目标域样本$\hat{x}_t$——即保持源图像的身份、姿态、配饰，但渲染为目标风格纹理。

**Step 2：纹理翻译网络（TTN）训练**

在CCN生成的合成目标样本基础上，GEM对源域样本$x_s$和目标域样本$\hat{x}_t$同时施加随机仿射变换，得到几何扩展后的训练对$(\tilde{x}_s, \tilde{x}_t)$。TTN以U-Net架构学习映射$\mathcal{M}_{st}: \tilde{x}_s \rightarrow x_g$，通过以下多表示约束训练：

**风格损失**（Style Loss）：
$$\mathcal{L}_{sty} = \mathbb{E}_{\tilde{x}_s}[\log(1-D_s(\mathcal{F}_{sty}(\mathcal{M}_{st}(\tilde{x}_s))))] + \mathbb{E}_{\tilde{x}_t}[\log(D_s(\mathcal{F}_{sty}(\tilde{x}_t)))]$$

其中$\mathcal{F}_{sty}$为预训练VGG16的风格表示提取器，$D_s$为风格判别器。该损失惩罚生成图像与目标风格图像在风格特征分布上的差异，促使$M_{st}$产生具有目标域纹理特征的输出。

**内容损失**（Content Loss）：
$$\mathcal{L}_{con} = \|VGG(\tilde{x}_s) - VGG(M_{st}(\tilde{x}_s))\|_1$$

在VGG16特征空间中最小化生成图像与源图像的L1距离，保持内容结构（面部形状、身份特征、配饰位置）不变。与风格损失形成对抗平衡：风格损失推动纹理迁移，内容损失防止结构扭曲。

**面部感知损失**（Facial Perception Loss）：
$$\mathcal{L}_{per} = \|\mathcal{R}_{exp}(x_g) - \boldsymbol{\alpha}\|_2$$

$\mathcal{R}_{exp}$为预训练的3D人脸表情参数回归器，$\boldsymbol{\alpha}$为源图像的表情参数。该损失约束生成图像的面部表情与源图像一致，特别针对极度夸张的风格（如动漫大眼、艺术变形），可自适应调节五官局部变形程度。论文明确指出，对于非极度夸张风格，该损失项可被省略（$\lambda_{per}=0$）。

**全变分损失**（Total Variation Loss）：
$$\mathcal{L}_{tv} = \frac{1}{h \cdot w \cdot c} \| \nabla_u (x_g) + \nabla_v (x_g) \|$$

对生成图像在水平和垂直方向的梯度施加平滑正则，抑制高频伪影。

**总训练损失**：
$$\mathcal{L}_{total} = \mathcal{L}_{sty} + \lambda_{con}\mathcal{L}_{con} + \lambda_{per}\mathcal{L}_{per} + \lambda_{tv}\mathcal{L}_{tv}$$

四个损失项形成多层级约束：风格损失负责全局纹理迁移，内容损失和面部感知损失分别从结构和局部表情层面保持内容，全变分损失确保图像质量。

**推理阶段**：

仅使用训练好的TTN。输入源图像经GEM施加随机几何变换后，由TTN单次前向传播生成风格化结果。对于全身体图像翻译，TTN直接处理整张图像，无需额外的身体检测、分割或多网络级联——这是GEM打破空间约束的直接收益。

### 模块间因果关系

三个模块形成递进依赖的因果链：

1. **CCN → TTN**：CCN提供内容对称的合成目标样本，使TTN的训练数据在内容维度上实现源-目标对齐。若无CCN（消融实验证实），TTN将直接面对内容偏差的少量真实样本，导致FID从35.92急剧恶化至58.52，身份一致性ID从0.71降至0.58。

2. **GEM → TTN**：GEM通过随机仿射变换扩展几何分布，使TTN学习到姿态无关的局部纹理映射。移除GEM后，模型对未对齐人脸和全身体图像表现敏感，无法泛化到训练分布外的姿态。

3. **CCN + GEM → TTN**：两者的协同效应是方法成功的关键。CCN解决内容分布偏差，GEM解决几何分布偏差，共同为TTN提供“校准后”的训练环境，使简单的U-Net即可实现高保真少样本风格化。

### 全身体翻译的优雅实现

传统方法（如AgileGAN）需要复杂的多阶段流水线（人脸检测→分割→局部翻译→融合）处理全身体图像。DCT-Net凭借GEM的几何扩展，使TTN天然具备处理任意空间位置的能力，仅需单次网络评估即可完成全身体翻译（Fig. 6）。这一简洁性源于域校准策略的本质优势：当模型学会局部纹理映射而非全局空间对应时，图像尺寸和构图不再构成限制。

![[assets/figures/papers/paper_list_l13_https_menyifang_github_io_projects_DCTNet_DCTNet_html/figures/006_Figure_6.jpg]]
*Figure 6: Pipelines of full image translation. Instead of exploiting complicated architectures as other existing approaches, we achieve the goal in an elegant single network with one evaluation*

![[assets/figures/papers/paper_list_l13_https_menyifang_github_io_projects_DCTNet_DCTNet_html/figures/003_Figure_3.jpg]]
*Figure 3: An overview of the proposed framework, which consists of the content calibration network (CCN), the geometry expansion module (GEM), and the texture translation network (TTN). CCN borrows the content prior from the real face generator*

![[assets/figures/papers/paper_list_l13_https_menyifang_github_io_projects_DCTNet_DCTNet_html/figures/005_Figure_5.jpg]]
*Figure 5: The architecture of the texture translation network*

![[assets/figures/papers/paper_list_l13_https_menyifang_github_io_projects_DCTNet_DCTNet_html/figures/002_Figure_2.jpg]]
*Figure 2: An illustration of domain-calibrated translation. It is difficult to learn correspondences from the diverse source distribution to the biased target distribution formed by few-shot examples. We firstly calibrate the distribution of the target domain D?? in content features by adapting source samples, and then expand D?? in the geometry dimension. With examples sampled from the calibrated distribution, it is easier to learn a fine-grained texture translation with advanced ability, generality, and scalability*

## 实验与关键发现

DCT-Net 的实验评估围绕三个核心维度展开：少样本风格化质量、内容保真度，以及各模块的因果贡献。评估采用定量指标（FID、身份一致性 ID）、用户主观偏好研究，以及多组定性可视化对比。所有对比方法均使用官方实现或预训练模型进行公平测试。

### 主实验结果

**定量指标对比。** 在包含 5000 张图像的 CelebA 测试集上，DCT-Net 取得了最低的 FID（35.92）和最高的身份一致性 ID（0.71），显著优于四个先进基线方法（Table 1）。FID 衡量生成图像与真实目标风格分布的距离，越低表示风格越接近目标域；ID 通过人脸识别网络度量身份信息保留程度，越高表示内容保真度越好。DCT-Net 在这两个相互制约的维度上同时取得最优，验证了“先校准、后翻译”策略的有效性——内容校准网络（CCN）将目标域分布拉近源域，使得后续纹理翻译网络（TTN）无需在分布偏差和内容保持之间进行艰难权衡。

**用户主观偏好。** 在 20 名参与者进行的用户研究中，DCT-Net 的结果在风格化效果偏好（Pref. A）上获得 82.6% 的选择率，在内容保留偏好（Pref. B）上获得 90.5% 的选择率，远超其他竞争方法（各方法均低于 20% 和 10%）。这一压倒性优势表明，用户不仅认可 DCT-Net 的风格化质量，更对其在身份、配饰、复杂遮挡等场景下的内容保持能力给予高度评价。

**定性对比。** 与 CycleGAN、U-GAT-IT、Toonify、PSP 的视觉对比（Fig. 8）显示，基线方法在少样本条件下普遍出现身份丢失、纹理模糊或风格迁移不彻底的问题，而 DCT-Net 在保持面部结构完整性的同时，实现了细腻的局部纹理转换。与同期少样本方法 AgileGAN 和 Few-shot Ada 的对比（Fig. 9）进一步表明，DCT-Net 无需依赖 GAN 反演即可获得更稳定的生成质量和更强的泛化能力。

### 关键消融实验

消融实验（Table 1, Fig. 10）逐一验证了三个核心模块的因果贡献：

![[assets/figures/papers/paper_list_l13_https_menyifang_github_io_projects_DCTNet_DCTNet_html/figures/011_Table_1.jpg]]
*Table 1: Quantitative comparison of our method and four state-of-the-art approaches evaluated by two metrics (i.e., FID and ID) and user studies*

![[assets/figures/papers/paper_list_l13_https_menyifang_github_io_projects_DCTNet_DCTNet_html/figures/012_Figure_10.jpg]]
*Figure 10: Effects of our proposed CCN, GEM, and TTN*

**移除内容校准网络（CCN）。** 这是最具破坏性的消融：FID 从 35.92 急剧恶化至 58.52，ID 从 0.71 降至 0.58。该结果直接证明了内容校准是系统性能的瓶颈所在——若缺少 CCN 对目标域分布的内容校准，TTN 将被迫在严重偏差的少样本分布上学习跨域映射，导致过拟合和内容丢失。这一发现与论文的核心洞察高度一致：源域丰富的内容先验是少样本风格化的关键杠杆。

**移除几何扩展模块（GEM）。** 缺少 GEM 后，模型对姿态变化和未对齐人脸的敏感度显著上升，全身体图像翻译能力受限（Fig. 10）。GEM 通过随机缩放和旋转释放空间约束，使模型学习到的纹理映射对几何变化具有不变性，这是 DCT-Net 能够仅用头部训练样本推广到全身体翻译的关键机制。

**替换纹理翻译网络（TTN）。** 将 U-Net 架构的 TTN 替换为简单映射网络后，生成结果出现细节模糊和内容丢失，无法有效保留身份信息（Fig. 10）。这表明在已校准的域对上，仍需要具备足够容量的局部纹理映射网络来捕捉细粒度的风格-内容对应关系。

**面部感知损失（L_per）的辅助作用。** 该损失函数针对极度夸张的风格设计，通过约束生成图像的面部表情参数与源图像一致，自适应地调节五官变形程度。消融显示（Fig. 11），在非夸张风格中去除 L_per 影响有限，但在需要大幅局部结构变化的风格中，L_per 能有效引导五官区域的合理变形，避免结构崩溃。

### 失败模式与适用边界

**夸张风格的局限。** 论文明确指出，面部感知损失 L_per 仅在极度夸张的风格中被激活使用，对于不需要夸张局部形变的风格，该方法不施加此约束（Section 4.5.2）。这意味着 DCT-Net 在默认配置下可能无法主动产生大幅度的五官变形效果，其风格化更侧重于纹理层面的转换而非几何层面的重构。

**失败案例的存在。** 论文提及存在失败案例，但未在正文中详细讨论，相关分析见于补充材料。根据方法机理推断，可能的失败模式包括：当目标风格样本数量极度稀少（如少于几十张）时，CCN 的微调可能不充分；当源域内容与目标域风格存在根本性的语义不匹配时，内容对称假设可能失效。

**数据依赖边界。** 训练配置显示（Section 4.1），CCN 使用约 100 张真实风格样本配合 10,000 张合成校准样本进行微调，TTN 在此基础上训练约 10k 迭代。该方法对风格样本数量的最低要求未在论文中明确给出，但从实验设置推断，约 100 张真实样本是当前验证的有效工作范围。

**全身体翻译的推广条件。** DCT-Net 的全身体翻译能力（Fig. 12）源于 GEM 释放空间约束和 CCN 校准内容分布，但其成功依赖于头部训练样本与全身体图像在纹理特征上的一致性。当身体区域的纹理风格与头部存在显著差异时，推广效果可能下降，论文未对此边界条件进行系统评估。

## 定位与知识库关联

DCT-Net 的核心定位是**少样本肖像风格化的域校准翻译框架**，其与已有工作的本质差异在于改变了“目标域分布处理”这一关键 slot：已有方法（如 **CycleGAN** (Zhu et al., ICCV 2017)、**U-GAT-IT** (Kim et al., ICLR 2020)、**Toonify** (Pinkney and Adler, arXiv 2020)、**PSP** (Richardson et al., CVPR 2021)、**AgileGAN** (Song et al., ACM TOG 2021) 以及 **Few-shot Ada** (Ojha et al., CVPR 2021)）或直接利用少量目标域样本训练翻译网络，或依赖 StyleGAN 反演嵌入进行风格迁移，均面临目标域分布严重偏差导致的过拟合、内容丢失和泛化困难。DCT-Net 将这一 slot 替换为“先校准，后翻译”的两阶段策略：通过内容校准网络（CCN）将目标域的内容分布拉近源域，再利用几何扩展模块（GEM）扩大空间多样性，最终在已校准的域对上学习像素级局部纹理翻译。

### 相对已有方法的本质差异

相较于基于 StyleGAN 反演的方法（如 Toonify、PSP），DCT-Net 无需反演步骤即可实现端到端翻译，避免了反演误差累积和训练不稳定的问题。相较于 Few-shot Ada 等少样本自适应方法，DCT-Net 不直接利用少量风格样本训练翻译网络，而是通过 CCN 生成内容对称的合成目标样本（约 10,000 张）来校准分布，从根本上缓解了过拟合。相较于 AgileGAN 等需要复杂架构的方法，DCT-Net 的全身体图像翻译仅需单一网络一次前向传播即可完成，架构更为简洁。

### 知识库挂载点

DCT-Net 可挂载至以下知识库节点：

1. **图像翻译（Image-to-Image Translation）**：作为少样本条件下域校准翻译的代表方法，与 CycleGAN、U-GAT-IT 等无监督图像翻译方法并列，核心贡献在于提出“先校准分布再学习映射”的范式，解决了目标域样本稀疏时的分布对齐难题。

2. **StyleGAN 微调与迁移学习**：CCN 模块本质是对预训练 StyleGAN2 生成器进行目标域微调，属于 StyleGAN 迁移学习的分支，可与 Toonify、PSP 等方法归入同一技术脉络，但 DCT-Net 的独特之处在于将微调仅用于分布校准而非直接生成最终结果。

3. **少样本风格化（Few-shot Stylization）**：作为少样本肖像风格化的专用方法，与 Few-shot Ada 等方法并列，关键区别在于利用源域丰富先验生成合成目标样本以扩充训练数据。

4. **人脸属性编辑与肖像生成**：TTN 模块结合面部感知损失 $\mathcal{L}_{per}$ 实现了对五官局部结构的可控变形，可与 AgileGAN 等肖像生成方法关联。

### 适用边界

1. **风格样本数量要求**：方法需要约 100 张真实风格样本用于 CCN 微调，若样本数量过少（如仅几张），CCN 可能无法有效校准目标域分布，导致后续翻译质量下降。论文未给出最低样本数量的系统实验，此边界需进一步验证。

2. **风格类型限制**：面部感知损失 $\mathcal{L}_{per}$ 仅用于极度夸张的风格（如漫画化），对于非夸张风格则不使用该损失，因此方法在非夸张风格下可能无法产生强烈的局部形变效果。此外，若目标风格与源域内容分布差异极大（如抽象艺术），CCN 的内容对称生成可能失效。

3. **全身体翻译的泛化条件**：方法仅使用头部训练样本即可推广到全身体图像翻译，但这一泛化能力依赖于 GEM 的几何扩展和源域先验的丰富性。若目标风格包含全身特有的纹理模式（如衣物褶皱风格化），仅使用头部样本训练的模型可能无法充分捕捉这些模式。

4. **遮挡与复杂姿态**：论文展示了方法对遮挡、配饰和罕见姿态的处理能力，但未系统评估极端遮挡（如大面积遮挡超过面部 50%）或极端姿态（如大角度侧脸）下的性能边界。

### 后续工作启发

1. **可学习的几何扩展**：当前 GEM 采用固定的随机缩放和旋转，若能引入可学习的几何变换参数，可能进一步提升对复杂姿态的适应能力。

2. **视频连续帧处理**：域校准翻译思想可拓展至视频风格化，关键在于如何保持帧间一致性，同时利用 CCN 校准目标域时间维度的分布。

3. **跨域泛化**：CCN 依赖预训练的 StyleGAN2 源域生成器，若能替换为其他域的预训练生成器（如动物、风景），方法有望拓展至更广泛的少样本图像翻译任务。

4. **自适应风格强度控制**：当前方法对风格强度的控制有限，后续可引入风格插值机制，在已校准的域对上实现连续的风格强度调节。

5. **失败案例分析**：论文提到存在失败案例但未详细讨论（详见补充材料），后续工作可系统分析失败模式，如 CCN 生成伪影的传播机制、TTN 在极端纹理下的失效条件等，以明确方法的鲁棒性边界。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/DCT_Net_Domain_calibrated_Translation_for_Portrait_Stylization.pdf]]