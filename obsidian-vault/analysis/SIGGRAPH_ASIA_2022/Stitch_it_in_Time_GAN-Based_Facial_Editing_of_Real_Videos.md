---
title: "Stitch it in Time: GAN-Based Facial Editing of Real Videos"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Stitch_it_in_Time_GAN_Based_Facial_Editing_of_Real_Videos.pdf
project_link: null
code_link: "https://github.com/rotemtzaban/STIT"
aliases:
- SIT
- SITGBFERV
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_animation_interaction
- topic/vision_multimodal_applications
core_operator: pivot的平滑性以及生成器对低频率函数的偏好。采用编码器（e4e）代替优化寻找pivot，利用其低频归纳偏置保证相邻帧隐编码平滑变化；通过微调生成器（PTI）维持全局一致性；并引入‘缝合微调’（stitching tuning）在边界产生平滑过渡。
primary_logic: 原始视频本身时序一致，因此无需显式施加强制时序约束。只需在编辑流水线中选用具有平滑归纳偏置的工具（如编码器、生成器微调），即可保持一致性，而神经网络天然倾向于学习低频函数，这一特性足以提供强大的时序一致性先验。
claims:
- 使用编码器替代优化进行pivot发现，可以显著提升局部一致性，TL-ID达到0.996（接近1）
- 我们的方法在TL-ID和TG-ID上均优于PTI和Latent Transformer
- 消融实验显示，去掉编码器、PTI或缝合微调都会导致编辑质量下降
- In-the-wild videos 上 TL-ID↑ = 0.996
---

# Stitch it in Time: GAN-Based Facial Editing of Real Videos

> [!tip] 核心洞察
> 原始视频本身时序一致，因此无需显式施加强制时序约束。只需在编辑流水线中选用具有平滑归纳偏置的工具（如编码器、生成器微调），即可保持一致性，而神经网络天然倾向于学习低频函数，这一特性足以提供强大的时序一致性先验。

| 字段 | 内容 |
|------|------|
| 中文题名 | 及时缝合：基于GAN的真实视频面部编辑 |
| 英文题名 | Stitch it in Time: GAN-Based Facial Editing of Real Videos |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2201.08361) · [Code](https://github.com/rotemtzaban/STIT) |
| Topic | #topic/graphics_animation_interaction #topic/vision_multimodal_applications |
| Method | Stitch it in Time |
| Dataset | In-the-wild videos |

> [!tip] 效果简介
> - In-the-wild videos 上，TL-ID↑ 0.996 vs 0.976 (Latent Transformer) (+0.020)；TG-ID↑ 0.933 vs 0.901 (PTI) (+0.032)。

## 概要

现有基于GAN的真实视频面部编辑方法面临两个核心瓶颈：**局部时间抖动**（相似帧被映射到差异较大的隐空间区域，导致编辑不一致）与**全局身份漂移**（随视频推进身份特征逐渐偏离原始人物），同时简单的泊松融合在编辑区域边界产生伪影。

本文提出 **Stitch it in Time** 流水线，核心洞察在于：原始视频本身是时序一致的，因此无需显式施加时序约束，只需在编辑流水线中选用具有平滑归纳偏置的工具即可保持一致性。方法包含六个步骤：（1）对关键点施加高斯低通滤波以实现平滑的面部对齐；（2）使用 **e4e 编码器**（替代优化方式）将每帧映射到 StyleGAN2 隐空间，利用编码器的低频归纳偏置保证相邻帧隐编码平滑变化；（3）在所有帧上并行执行 **PTI 生成器微调**以纠正逆映射误差并恢复全局身份一致性；（4）使用线性方向编辑 pivot 隐编码；（5）提出**缝合微调**，以边界损失和掩码损失联合微调生成器，将编辑后人脸无缝融入原始背景；（6）反向对齐并合成最终视频。

实验表明，该方法在时序局部身份保持（TL-ID 达 0.996，接近原始视频的 1.0）和时序全局身份保持（TG-ID 达 0.933）上均优于 Latent Transformer 和 PTI 基线，同时消融实验验证了编码器、PTI 微调和缝合微调三个组件各自的关键作用。

## 核心方法与创新机理

### 问题瓶颈：视频编辑中的双重时间不一致性

真实视频（talking-head）的人脸编辑面临两个核心挑战：**局部时间抖动（local jitter）**和**全局身份漂移（global identity drift）**。这两者根源于现有逆映射-编辑流水线中pivot隐编码的发现方式与融合机制的缺陷。

**PTI**（Roich et al.）采用基于优化的方式在StyleGAN的W+空间中搜索pivot隐编码。由于优化过程的非凸性和随机性，相邻的视频帧（视觉上高度相似）可能被映射到W+空间中相距较远的点。当对这些pivot施加相同的编辑方向时，帧间的编辑效果出现不一致——即局部抖动。同时，PTI通过微调生成器来修正逆映射误差，这在一定程度上维持了全局身份一致性，但无法根治pivot层面的局部不稳定性。

**Latent Transformer**（Yao et al.）使用pSp编码器直接预测pivot，编码器的平滑归纳偏置使得相邻帧的隐编码天然接近，局部一致性较好。然而，编码器的逆映射精度有限，逐帧独立编码缺乏全局约束，导致编辑后的人物身份随时间缓慢漂移。此外，该方法的融合步骤依赖基于分割掩码的泊松融合（Poisson blending），在头发、颈部等区域产生明显的边界伪影。

本工作的核心洞察在于：**原始视频本身是时序一致的——无需在编辑流水线中显式引入时序约束模块或损失函数。只需在流水线的关键环节选用具有平滑归纳偏置的工具，即可将原始视频的一致性传递到编辑结果中。** 神经网络天然倾向于学习低频函数（spectral bias），这一特性本身就是一个强大的时序一致性先验。

### 六阶段流水线架构

完整的编辑流水线包含六个顺序模块（Figure 2），每个模块对应一个明确的处理阶段：

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2201_08361/figures/002_Figure_2.jpg]]
*Figure 2: Our full video editing pipeline contains 6 steps. (1) Videos are split into individual frames. The face in each frame is cropped and aligned. (2) Each cropped face is inverted into the latent space of a pre-trained StyleGAN2 model, using a pre-trained e4e encoder. (3) The generator is fine-tuned using PTI across all video frames in parallel, correcting for inaccuracies in the initial inversion and restoring global coherence. (4) All frames are edited by manipulating their pivot latent codes linearly, using a fixed direction and step-size. (5) We fine-tune the generator a second time, stitching the backgrounds and the edited faces together in a spatially-smooth manner. (6) We reverse the ali...*

1. **帧拆分与平滑对齐**：将视频拆分为独立帧，检测面部关键点，对关键点序列施加高斯低通滤波以消除检测噪声引起的帧间抖动，然后基于平滑后的关键点裁剪并对齐人脸区域。
2. **编码器逆映射**：使用预训练的e4e编码器将每一帧的裁剪人脸映射到StyleGAN2的W空间（而非W+空间），获得pivot隐编码。
3. **PTI生成器微调**：在所有帧上并行微调StyleGAN2生成器的权重，以修正编码器逆映射的误差，恢复全局身份一致性。
4. **隐空间编辑**：对pivot隐编码施加线性编辑方向（如“微笑”、“年龄”等），获得编辑后的隐编码。
5. **缝合微调**：第二次微调生成器，使编辑后的人脸与原始背景在空间上平滑过渡，消除边界伪影。
6. **反向对齐与合成**：将对齐变换逆向应用于编辑后的人脸，将其粘贴回原始视频帧。

### 关键创新槽位一：编码器替代优化进行pivot发现

这是本方法最核心的**changed slot**。PTI使用优化器在W+空间中逐帧搜索pivot：
$$w_{\text{pivot}} = \arg\min_w \mathcal{L}(G(w), x)$$
其中$G$为StyleGAN2生成器，$x$为裁剪帧。该过程对每一帧独立运行，缺乏帧间约束，且优化轨迹对初始化敏感。

本方法将其替换为**e4e编码器**的直接前馈推理：
$$w_{\text{pivot}} = E_{\text{e4e}}(x)$$
e4e编码器在训练过程中已经学会了将图像映射到StyleGAN的W空间（而非W+空间）。W空间的维度远低于W+空间，且编码器网络本身具有**低频归纳偏置（spectral bias）**——即神经网络在学习映射时天然倾向于产生平滑的输出。这意味着视觉上相似的相邻帧会被映射到W空间中相近的点，从根本上保证了pivot的局部平滑性。

因果链路：**编码器的低频归纳偏置 → 相邻帧pivot隐编码平滑变化 → 编辑后帧间效果一致 → 局部时间一致性（TL-ID = 0.996）**。

### 关键创新槽位二：PTI并行微调维持全局一致性

编码器虽然保证了局部平滑性，但其逆映射精度有限——编码器-生成器串联的重建图像与原始帧之间存在误差。如果仅使用编码器pivot进行编辑，这些误差会在时间维度上累积，导致编辑后的人物身份逐渐偏离原始身份（全局漂移）。

本方法保留了PTI的生成器微调机制，但将其置于编码器逆映射之后，形成一个**“编码器发现pivot + 微调修正误差”**的混合方案。PTI微调的目标函数为：

$$\min_{\theta} \frac{1}{N} \sum_{i=1}^{N} \left( \mathcal{L}_{\mathrm{LPIPS}}(c_i, r_i) + \lambda_{L2}^{P} \mathcal{L}_{L2}(c_i, r_i) \right) + \lambda_{R}^{P} \mathcal{L}_{R}$$

其中$c_i$为第$i$帧的裁剪人脸，$r_i = G_\theta(w_i)$为生成器重建图像，$w_i$为编码器预测的pivot。微调在所有$N$帧上**并行进行**，损失函数包含LPIPS感知损失、L2像素损失和局部正则化项$\mathcal{L}_R$（约束生成器权重的局部变化）。

因果链路：**编码器pivot（局部平滑）→ PTI并行微调（全局身份约束）→ 编辑后身份不漂移 → 全局时间一致性（TG-ID = 0.933）**。

### 关键创新槽位三：缝合微调替代泊松融合

传统的融合方法（如Latent Transformer采用的泊松融合）基于分割掩码将编辑后人脸直接粘贴到原始帧中。这在以下区域产生明显伪影：
- **边界过渡生硬**：人脸区域与背景之间存在不自然的接缝
- **头发区域**：分割掩码难以精确覆盖发丝，导致原始头发与编辑后头发的不连续
- **颈部/衣物区域**：编辑可能改变颈部纹理，与原始衣物产生冲突

本方法提出**缝合微调（stitching tuning）**，将融合问题转化为生成器的第二次微调。具体步骤（Figure 4）：
1. 使用编辑后的pivot生成编辑人脸$e_i = G_\theta(w_i^{\text{edit}})$
2. 使用现成的分割网络获得人脸掩码$m_i$，通过膨胀操作创建边界掩码$b_i$
3. 微调生成器权重$\theta_{st}$，最小化双重目标：

**边界损失**（恢复原始背景）：
$$\mathcal{L}_{b,i} = \mathcal{L}_{L1}(s_i \odot b_i, x_i \odot b_i)$$
其中$s_i = G_{\theta_{st}}(w_i^{\text{edit}})$为缝合生成器的输出，$x_i$为原始帧，$b_i$为边界掩码。该损失强制边界区域恢复到编辑前的原始像素值。

**掩码损失**（保持编辑效果）：
$$\mathcal{L}_{m,i} = \mathcal{L}_{L1}(s_i \odot m_i, e_i \odot m_i)$$
该损失确保人脸区域（掩码$m_i$内）保持编辑后的效果。

缝合微调的总体目标为：
$$\min_{\theta_{st}} \mathcal{L}_{b,i} + \lambda_m \mathcal{L}_{m,i}$$

因果链路：**生成器在边界区域学习恢复原始背景 + 在人脸区域保持编辑效果 → 编辑人脸与原始背景在隐空间层面平滑过渡 → 消除泊松融合的边界伪影**。

### 训练与推理路径

**推理路径**（处理一个新视频）：
1. 对每一帧进行关键点检测 → 高斯滤波平滑 → 裁剪对齐
2. 将裁剪帧送入e4e编码器，获得W空间pivot（前馈推理，无需优化）
3. 使用所有帧的pivot-裁剪对并行微调StyleGAN2生成器（约数百次迭代）
4. 对pivot施加线性编辑方向，获得编辑后pivot
5. 使用编辑后pivot和原始帧对生成器进行缝合微调（第二次微调）
6. 使用最终生成器合成编辑帧，反向对齐后粘贴回视频

**训练路径**（方法本身无需训练，但依赖预训练模型）：
- e4e编码器：在FFHQ数据集上预训练，用于StyleGAN2的W空间逆映射
- StyleGAN2生成器：在FFHQ上预训练
- 分割网络：现成的BiSeNet，用于获得人脸掩码
- 身份检测网络：ArcFace，用于计算TL-ID和TG-ID指标

整个流水线**不包含任何时序模块**（如光流、时序卷积、RNN），也不使用任何时序损失函数。时序一致性完全来源于工具选择（编码器的低频偏置、微调的全局约束）和原始视频的天然连续性。

### 局限性

1. **裁剪区域外的头发问题**：StyleGAN的对齐过程可能将部分头发（如辫子、长发末端）留在裁剪框之外。当编辑改变头发长度或颜色时，裁剪区域内的头发被修改，而外部区域保持不变，导致不自然的过渡。缝合微调无法解决裁剪区域外的问题。
2. **纹理粘附（texture sticking）**：尽管通过逐帧微调（而非隐空间插值）已大幅减少该现象，但在某些情况下编辑后的纹理仍会“粘附”在移动的面部区域上。这与StyleGAN2的隐空间特性有关，可能需要StyleGAN3的等变性来彻底解决。

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2201_08361/figures/001_Figure_1.jpg]]
*Figure 1: Video editing using our proposed pipeline. Our framework can successfully apply consistent semantic manipulations to challenging talking-head videos, without requiring any temporal components or losses*

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2201_08361/figures/006_Figure_6.jpg]]
*Figure 6: Additional Video editing results using our proposed pipeline. For most modifications, our stitching framework can handle more challenging cases such as long hair*

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2201_08361/figures/010_Figure_9.jpg]]
*Figure 9: Qualitative demonstration of the importance of our pipeline components. Replacing the encoder with an optimization step results in poor editing consistency. Without PTI, identity drifts over time, and stitching performance deteriorates. Replacing stitching with a mask-based blending scheme results in visual artifacts, such as sharp transitions in hair regions. Our full pipeline successfully avoids these pitfalls and generates a consistent video*

## 实验与关键发现

### 时序一致性指标设计

为量化视频编辑的时序质量，本文提出两个互补指标：**TL-ID**（Temporally-Local Identity Preservation）和 **TG-ID**（Temporally-Global Identity Preservation）。TL-ID 利用现成的人脸识别网络，计算相邻帧对的身份相似度，并以原始视频的相邻帧相似度作归一化——原始视频的 TL-ID 因此恒为 1，编辑后视频越接近 1 表示局部一致性越好。TG-ID 则计算所有帧与首帧的身份相似度，衡量编辑过程中是否发生全局身份漂移。两个指标分别对应“局部抖动”和“全局漂移”这两类核心失效模式。

### 主结果：与 Latent Transformer 和 PTI 的定量对比

Table 1 报告了在 in-the-wild 视频上的对比结果：

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2201_08361/figures/009_Table_1.jpg]]
*Table 1: Temporal consistency metrics. Encoder based methods display improved identity preservation at the local (adjacent frame) level, but show considerable identity drift over time. PTI, preserves a greater degree of global identity, at the cost of local jitter from inconsistent pivots. Our pipeline outperforms the alternatives and achieves a local-identity preservation score which is nearly equal to the original video (1), demonstrating our ability to maintain a high degree of consistency*

| 方法 | TL-ID ↑ | TG-ID ↑ |
|------|---------|---------|
| 原始视频 | 1.000 | — |
| Latent Transformer（Yao et al.） | 0.976 | 0.811 |
| PTI（Roich et al.） | — | 0.901 |
| **Stitch it in Time（本文）** | **0.996** | **0.933** |

**关键数值解读：**

- **TL-ID = 0.996**：本文方法的局部一致性几乎与原始视频持平（仅差 0.004），较 Latent Transformer 的 0.976 提升 2.0%。这一优势直接归因于用 e4e 编码器替代优化式 pivot 搜索——编码器的低频归纳偏置使相邻帧的隐编码天然平滑，无需任何显式时序约束。

- **TG-ID = 0.933**：全局身份保持上，本文方法较 PTI（0.901）提升 3.2%，较 Latent Transformer（0.811）提升 12.2%。PTI 通过生成器微调维持了较好的全局一致性，但因其优化式 pivot 发现导致局部抖动；Latent Transformer 虽局部尚可，但缺乏全局矫正机制，身份随时间显著漂移。本文合并二者优势：编码器保证局部平滑，PTI 微调锁定全局身份。

- **互补性验证**：Table 1 还揭示了一个关键洞察——编码器方法（Latent Transformer）在 TL-ID 上表现较好但在 TG-ID 上急剧下降，而 PTI 在 TG-ID 上较好但牺牲了 TL-ID。本文方法在两个维度同时达到最优，证明“编码器 + PTI 微调”的组合并非简单叠加，而是分别解决了时序一致性的两个正交维度。

### 消融实验：各组件的因果贡献

Figure 9 通过定性消融揭示了流水线中三个关键组件的独立作用：

**（1）移除 e4e 编码器（w/o e4e），回退到优化式 pivot 搜索：**
编辑一致性显著下降。优化过程对每帧独立进行，缺乏跨帧平滑机制，导致相似帧被映射到差异较大的隐空间区域，编辑后出现明显的帧间跳变。这直接验证了核心假设：编码器的低频归纳偏置是局部一致性的因果来源。

**（2）移除 PTI 微调（w/o PTI）：**
出现两个连锁退化。其一，身份随时间逐渐漂移——编码器逆映射的累积误差无法得到全局矫正；其二，缝合质量恶化——生成器未针对视频整体微调，后续缝合微调缺乏良好的初始化，边界过渡不自然。

**（3）移除缝合微调（w/o Stitching），改用掩码泊松融合：**
头发区域和面部边界出现明显伪影。泊松融合仅做像素级混合，无法处理编辑后生成人脸与原始背景之间的语义不匹配（如头发纹理断裂、颈部色差）。缝合微调通过生成器层面的双目标优化，在边界区域恢复原始背景的同时保持编辑效果，从根本上避免了这类伪影。

三个消融的退化模式恰好对应了本文解决的三个瓶颈：局部抖动（无 e4e）、全局漂移（无 PTI）、融合伪影（无缝合微调）。

### 效率与适用边界

**计算开销：** 对于 300 帧视频，完整流水线在单张 NVIDIA RTX 2080 上耗时约 1.5 小时。主要开销来自两轮生成器微调（PTI 和缝合微调），但二者均在所有帧上并行进行，相比逐帧优化方案仍具效率优势。

**适用边界与已知限制：**

1. **裁剪区域外的头发处理：** StyleGAN 的对齐流程会将部分头发（如辫子、长发末端）留在裁剪框外。当编辑涉及头发长度或颜色时，裁剪框内外出现不一致，导致不自然的过渡。这是 StyleGAN 预训练对齐范式的固有局限，非本文流水线可解决。

2. **纹理粘附（texture sticking）：** 尽管通过逐帧独立编辑（而非隐空间插值）已大幅减少该现象，但在某些情况下仍可见——编辑后人脸的纹理细节随头部运动呈现不自然的“粘附”效果。论文指出，迁移到 StyleGAN3 的傅里叶特征表示可能是彻底消除此问题的路径，但尚未实现。

3. **域外泛化：** Figure 8 展示了在动画人脸等域外数据上的编辑效果，表明流水线对非真实人脸有一定泛化能力，但论文未提供域外数据的定量评估，该结论需谨慎看待。

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2201_08361/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of our full editing pipeline. In the left column, we show three frames extracted from the source video. In the following columns, we show intermediate results of our pipeline over the same three frames. Left to right: the encoder-inversion step, the PTI fine-tuning step, the pivot editing step, and finally our stitching procedure. When not applying our stitching procedure, we use a segmentation-mask based blending procedure [48]. Note in particular the neck region, which displays considerable artifacts after the editing step which are then eliminated through our stitching-tuning approach*

## 定位与知识库关联

本文的核心贡献在于识别并替换了现有视频编辑流水线中的三个关键 slot，从而在不引入任何显式时序约束的前提下，实现了高度一致的视频人脸编辑。

### 相对于已有方法的 slot 变更

**Slot 1：pivot 发现机制（优化 → 编码器）**

基于优化的逆映射方法（如 **PTI**，Roich et al.）在逐帧寻找隐编码时，由于优化过程的随机性和高自由度，会将视觉上相似的相邻帧映射到 W+ 空间中距离较远的点，导致编辑后出现局部时间抖动（local jitter）。本文将此 slot 替换为基于 e4e 编码器的逆映射，利用神经网络天然偏好学习低频函数的归纳偏置，使相似帧在隐空间中自然聚集，从而在无需显式时序损失的情况下获得平滑的 pivot 序列。这一替换直接解释了 TL-ID 指标从 0.976（Latent Transformer）提升至 0.996 的因果机制。

**Slot 2：融合方法（泊松融合 → 缝合微调）**

主流视频编辑方法（如 **Latent Transformer**，Yao et al.）采用基于分割掩码的泊松融合将编辑后人脸粘贴回原始帧，在头发、颈部等边界区域容易产生明显的过渡伪影。本文将此 slot 替换为“缝合微调”（stitching tuning）——对生成器进行第二次微调，通过边界损失 $\mathcal{L}_{b,i}$ 和掩码损失 $\mathcal{L}_{m,i}$ 的联合优化，使生成器在编辑区域保持修改效果的同时，在边界区域恢复原始背景。这一替换本质上是将“后处理融合”提升为“生成器内在能力”，使边界过渡成为生成过程的一部分而非后期修补。

**Slot 3：面部对齐（离散关键点 → 平滑关键点）**

标准的关键点检测对齐在相邻帧间可能产生微小抖动，本文对检测到的关键点应用高斯低通滤波，以极低成本消除了对齐步骤引入的时序不一致性。

### 知识库挂载点

本文在知识图谱中的挂载位置是 **StyleGAN 逆映射与编辑** 向 **视频时序一致性** 的交叉节点。上游依赖包括：

- **StyleGAN2** 生成器架构与隐空间特性（低频归纳偏置）
- **e4e 编码器**（Tov et al., 2021）提供的快速、平滑逆映射能力
- **PTI**（Roich et al.）的生成器微调策略，用于恢复逆映射误差和身份细节
- **线性隐空间编辑**技术（如 InterfaceGAN、StyleCLIP 等），提供语义编辑方向

本文的关键洞察在于：原始视频本身是时序一致的，因此一致性问题的根源不在“如何约束”，而在“如何不破坏”。这一认知将问题从“设计时序约束”转化为“选择具有平滑归纳偏置的工具”，属于方法论层面的视角转换。

### 适用边界

1. **生成器依赖**：方法建立在 StyleGAN2 的隐空间特性之上，编辑效果受限于 StyleGAN2 的生成能力和域内范围。对于 StyleGAN2 无法高质量重建的人脸（如极端姿态、严重遮挡），编辑质量会下降。
2. **纹理粘附残留**：虽然通过逐帧优化而非隐空间插值大幅减少了纹理粘附（texture sticking）现象，但在某些情况下仍可见。作者指出结合 StyleGAN3 的等变性可能彻底消除此问题，但尚未实现。
3. **头发编辑局限**：StyleGAN 的对齐裁剪过程可能将部分头发（如辫子、长发末端）留在裁剪区域之外，当编辑涉及头发长度或颜色时，这些外部区域未经处理，可能导致不自然的过渡。
4. **计算开销**：300 帧视频的完整编辑约需 1.5 小时（单张 NVIDIA RTX 2080），主要瓶颈在于两次生成器微调，限制了实时应用场景。

### 后续启发与开放问题

1. **与 StyleGAN3 的结合**：StyleGAN3 的平移等变性理论上可彻底消除纹理粘附，将其逆映射和编辑工具与本文的缝合微调框架结合，是自然的后续方向。
2. **编码器的视频级微调**：当前 e4e 编码器在通用数据上预训练，若在输入视频上微调编码器以进一步促进隐编码的一致性，可能进一步提升时序稳定性。
3. **缝合微调的泛化**：缝合微调本质上是一种“生成器局部适配”技术，其边界损失 + 掩码损失的联合优化范式可推广到其他需要无缝融合生成内容与真实背景的任务（如虚拟试穿、场景编辑）。
4. **无时序约束范式的推广**：本文证明“选择平滑工具”足以替代显式时序约束，这一思路可启发其他视频生成任务（如视频超分、视频修复）重新审视是否必须引入光流、时序注意力等复杂组件。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Stitch_it_in_Time_GAN_Based_Facial_Editing_of_Real_Videos.pdf]]