---
title: "MotionDuet: Dual-Conditioned 3D Human Motion Generation with Video-Regularized Text Learning"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: "paperPDFs/arxiv_2025/MotionDuet:_Dual-Conditioned_3D_Human_Motion_Generation_with_Video-Regularized_Text_Learning.pdf"
project_link: null
code_link: null
aliases:
- MotionDuet
tags:
- arxiv_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 利用视频特征作为分布先验，通过DASH损失对齐运动潜空间与视频特征分布，结合DUET融合模块与自适应引导实现多模态平衡与互校正。
primary_logic: 在训练中引入视频条件作为正则化手段，通过分布感知对齐（DASH）和双流融合（DUET）将真实视频的时空先验注入运动生成器，使得即使在纯文本推理时也能生成物理一致、时序连贯的高质量运动。
claims:
- DASH损失通过令牌级与结构一致性正则化有效缩小视频特征与运动嵌入的分布差距
- DUET融合模块在所有消融实验中显著提升FID与R精度
- 自适应引导机制使用退化分支替代无条件分支，稳定多模态平衡且可固定权重ω
- 仅使用文本输入时MotionDuet仍能生成优于基线的高质量运动
---

# MotionDuet: Dual-Conditioned 3D Human Motion Generation with Video-Regularized Text Learning

> [!tip] 核心洞察
> 在训练中引入视频条件作为正则化手段，通过分布感知对齐（DASH）和双流融合（DUET）将真实视频的时空先验注入运动生成器，使得即使在纯文本推理时也能生成物理一致、时序连贯的高质量运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionDuet：基于视频正则化文本学习的双条件三维人体运动生成 |
| 英文题名 | MotionDuet: Dual-Conditioned 3D Human Motion Generation with Video-Regularized Text Learning |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2511.18209) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MotionDuet |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，R@3 ↑ 0.795±.003 vs 0.772±.002 (MLD) (+0.023)；FID ↓ 0.179±.024 vs 0.473±.013 (MLD) (-0.294)；MM Dist ↓ 3.154±.010 vs 3.196±.010 (MLD) (-0.042)。

## 概要

现有文本驱动的人体运动生成方法（如 **MLD**、**MDM**、**MotionDiffuse**、**MoMask** 等）仅依赖文本条件，或仅使用视频作为唯一输入，导致生成的运动分布偏离真实运动的统计特性——缺乏有效的多模态对齐机制与时空先验迁移能力。MotionDuet 的核心洞察在于：将视频条件作为训练阶段的正则化手段，通过分布感知对齐（DASH）和双流融合（DUET）将真实视频的时空先验注入运动生成器，使得即使在纯文本推理时，也能产生物理一致、时序连贯的高质量运动。

方法上，MotionDuet 在 **MLD** 扩散去噪骨干的基础上做出三项关键改动：用 VideoMAE 视频编码器与 CLIP 文本编码器构成双条件输入；用 DUET 融合模块（含 FFT 分支、卷积分支、动态掩码机制 DMM 与残差连接）替代简单的串联或注意力融合；引入 DASH 损失（令牌级余弦相似度损失 + 成对结构一致性损失）作为分布对齐正则项，配合特征空间 dropout 扰动实现自适应引导，以退化副本替代无条件分支进行自校正。

在 HumanML3D 基准上，MotionDuet（纯文本推理）相比 MLD 基线取得显著提升：R@3 从 0.772 升至 0.795，FID 从 0.473 降至 0.179，Diversity 更接近真实分布（9.532 vs 真实 9.503）。消融实验证实 DUET 模块使 FID 从 0.168 降至 0.101，DASH 损失进一步将 FID 改善至 0.084（过滤数据集），且 dropout 扰动策略比高斯噪声更稳定。需要指出的是，在部分定量指标上 MotionDuet 仍逊于 MoMask，但定性上运动方向与时序连贯性更优；此外，训练需大量计算资源（8×A800-80GB），视频数据集经清洗后仍有约 39% 异常样本，可能影响训练稳定性。



三维人体运动生成是计算机视觉与图形学中的核心问题，在游戏动画、电影制作、虚拟现实和机器人仿真等领域有广泛应用。近年来，基于扩散模型的文本到运动生成取得了显著进展，代表性工作包括**MLD**（Motion Latent Diffusion）、**MDM**、**MotionDiffuse**、**MotionGPT**和**MoMask**等。这些方法以文本描述作为条件，通过潜空间扩散去噪生成运动序列，在HumanML3D等标准基准上展现了令人瞩目的性能。

然而，现有方法存在一个关键瓶颈：**它们仅从文本生成运动或仅依赖视频条件，导致生成的运动分布偏离真实运动统计特性，缺乏有效的多模态对齐机制和时空先验迁移**。具体而言，纯文本条件虽然语义灵活，但难以捕捉真实运动中微妙的物理约束和时序连贯性——文本描述“一个人向前走并挥动右手”无法精确传达步态节奏、重心转移和肢体协调等细粒度时空模式。另一方面，现有视频条件方法往往将视频作为简单的输入信号，未能有效提取和迁移视频中蕴含的丰富时空先验。

这一瓶颈的因果机制在于：真实人体运动遵循复杂的物理和生物力学约束，其统计分布具有高维、多模态和强时序依赖的特性。纯文本条件提供的语义信号过于稀疏，无法充分约束生成空间；而视频特征与运动潜空间之间存在显著的分布差距，直接融合会导致模态冲突和生成质量下降。因此，**如何将真实视频的时空先验有效注入运动生成器，同时保持文本语义的灵活性，成为突破现有方法上限的核心挑战**。

MotionDuet针对上述问题提出了一个明确的解决思路：**在训练中引入视频条件作为正则化手段，通过分布感知对齐和双流融合将真实视频的时空先验注入运动生成器，使得即使在纯文本推理时也能生成物理一致、时序连贯的高质量运动**。这一思路的核心洞察在于，视频条件不应仅被视为额外的输入模态，而应作为运动生成器的“教师信号”，在训练阶段提供分布级别的正则化约束。具体而言，MotionDuet利用预训练VideoMAE编码器提取视频时空特征，通过DUET融合模块实现多模态特征的自适应整合，并通过DASH损失在令牌级和结构级对齐运动潜空间与视频特征分布。最终，自适应引导机制使得模型在推理时即使仅使用文本输入，也能保持训练阶段学到的物理先验。

这一设计将视频从“推理时依赖”转变为“训练时正则化”，从根本上改变了多模态运动生成的范式。



## 核心方法与创新机理

MotionDuet 的核心创新在于将**视频特征作为分布先验**注入文本到运动的扩散生成流程，通过两个关键机制——**分布感知对齐（DASH）**和**双流统一融合（DUET）**——解决现有方法仅依赖单一模态导致的运动分布偏移与时空一致性不足问题。其设计哲学是“用视频训练，用文本推理”：训练阶段利用配对视频的时空先验正则化运动潜空间，推理阶段即使仅输入文本，生成器也能产出物理一致、时序连贯的高质量运动。

### 1. 条件输入：从单模态文本到双模态视频-文本协同

现有文本到运动方法（如 **MLD** 、**MDM** 、**MotionDiffuse** ）仅使用 CLIP 文本嵌入作为条件信号。MotionDuet 将条件空间扩展为**视频嵌入 + 文本嵌入**的双条件结构：

- **视频特征** $\mathbf{V} = \mathcal{E}_{\mathrm{Vim}}(I)$：由预训练 VideoMAE 编码器（ViT-G）从渲染运动视频中提取，捕获真实的时空动态与关节协调模式。
- **文本特征** $\mathbf{T} = \mathcal{E}_{\mathrm{CLIP}}(\mathbf{t})$：由冻结的 CLIP 文本编码器提取语义嵌入。

双条件的核心价值不在于推理时多模态输入，而在于**训练时视频特征作为正则化信号**，将真实运动的统计特性（如周期性、关节协同、动量守恒）隐式编码进运动潜空间。证据表明，即使推理时仅使用文本（Table 1 中 `Our (text-only)`），FID 仍从 MLD 的 0.473 降至 0.179，R@3 从 0.772 提升至 0.795。

### 2. 多模态融合：DUET 模块替代简单串联

基线方法对多模态特征通常采用简单串联或交叉注意力。MotionDuet 提出的 **DUET（Dual-stream Unified Encoding and Transformation）**模块集成了四条互补分支：

| 分支 | 功能 | 关键操作 |
|------|------|----------|
| **FFT 分支** | 捕获全局周期性与时序规律 | $\mathbf{F} = \mathcal{F}^{-1}(W \odot \mathcal{F}(\mathbf{R}))$，可学习幅度滤波器 $W$ |
| **卷积分支** | 提取局部空间关系与几何表示 | 标准卷积操作 |
| **动态掩码机制（DMM）** | 自适应选择与融合表示更接近的特征分支 | 基于 L2 距离的硬选择：$d_0 = \|\mathbf{R}_{\mathrm{fusion}} - \mathbf{R}_0\|_2$，$d_{\mathrm{b}} = \|\mathbf{R}_{\mathrm{fusion}} - \mathbf{R}_{\mathrm{b}}\|_2$ |
| **残差连接** | 保留原始信息流，稳定训练 | 标准残差结构 |

DMM 的巧妙之处在于**天然处理模态缺失**：当视频输入不存在时，$\mathbf{V}$ 置零，其与融合表示的距离最大化，DMM 自动将信息流路由至文本分支，无需额外条件判断逻辑。

消融实验（Table 9）证实 DUET 的卷积融合策略将 FID 从 0.168 降至 0.101，R@3 从 0.747 提升至 0.755，显著优于简单相加、串联和注意力等基线融合方式。

### 3. 训练损失：DASH 分布对齐正则化

标准扩散模型仅使用均方误差 $\mathcal{L}_{\mathrm{MLD}}$ 作为重建损失。MotionDuet 引入 **DASH（Distribution-Aware Structural Harmonization）损失**，显式缩小生成运动特征与真实视频特征之间的分布差距：

$$\mathcal{L}_{\mathrm{DASH}} = \mathcal{L}_{\mathrm{token}} + \mathcal{L}_{\mathrm{pair}}$$

- **令牌级边界损失** $\mathcal{L}_{\mathrm{token}}$：约束每个运动令牌与对应视频令牌的余弦相似度不低于阈值 $m_{\mathrm{cos}}$：
  $$\mathcal{L}_{\mathrm{token}} = \frac{1}{N} \sum_{i=1}^{N} \mathrm{ReLU}(1 - m_{\mathrm{cos}} - \cos(\hat{z}_{t,\mathrm{d},i}, v_i))$$

- **成对结构一致性损失** $\mathcal{L}_{\mathrm{pair}}$：保持特征空间内令牌间相似度结构与视频特征一致：
  $$\mathcal{L}_{\mathrm{pair}} = \frac{1}{N^2} \sum_{i,j=1}^{N} \mathrm{ReLU}\big( |\cos(\hat{z}_{t,\mathrm{d},i}, \hat{z}_{t,\mathrm{d},j}) - \cos(v_i, v_j)| - m_{\mathrm{pair}} \big)$$

总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{MLD}} + \lambda_{\mathrm{DASH}} \mathcal{L}_{\mathrm{DASH}}$。DASH 的核心作用是**将视频的时空先验蒸馏进运动潜空间**，使生成的运动在统计分布上逼近真实运动。Table 11 显示，加入 DASH 后 FID 进一步改善至 0.084，R@3 提升至 0.764。但需注意 $\lambda_{\mathrm{DASH}}$ 取值敏感：Table 6 表明过大的权重（如 300）会导致 FID 急剧上升至 14.676，需要在验证集上仔细调参。

### 4. 引导机制：特征空间扰动自适应引导

传统分类器自由引导（CFG）需要训练无条件分支或在输入空间施加掩码。MotionDuet 提出**特征空间扰动自适应引导**，直接在融合表示 $\mathbf{H}$ 上施加退化操作，用退化副本替代无条件分支：

$$\hat{\mathbf{x}}_t = (1 + \omega) \cdot \hat{\mathbf{x}}_t^{\mathrm{strong}} - \omega \cdot \hat{\mathbf{x}}_t^{\mathrm{weak}}$$

其中 $\hat{\mathbf{x}}_t^{\mathrm{weak}}$ 由扰动后的弱条件生成，$\hat{\mathbf{x}}_t^{\mathrm{strong}}$ 由完整双条件生成，$\omega$ 为固定外推因子。两种扰动策略：

- **Dropout 扰动**：$\tilde{\mathbf{H}}^{(T)} = \mathrm{Dropout}(\mathbf{H}; \mathcal{D})$，随机置零 $p$ 比例的特征维度
- **高斯噪声扰动**：$\tilde{\mathbf{H}}^{(\sigma)} = \mathbf{H} + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2)$

Table 7/8 的消融表明，Dropout 扰动比高斯噪声更稳定，能提供一致的性能增益。该设计的优势在于**无需修改模型架构或训练额外分支**，仅通过特征空间操作即可实现多模态平衡与自校正，且 $\omega$ 经一次轻量验证搜索后即可固定。

### 创新总结

MotionDuet 的四个 changed slots 形成了一条完整的创新链条：**双条件输入**提供视频先验来源 → **DUET 融合**实现多模态特征的有效整合与自适应路由 → **DASH 损失**将视频分布显式蒸馏进运动潜空间 → **自适应引导**在推理时平衡多模态信号。这条链条的核心洞察是“视频正则化文本学习”——视频仅在训练时作为正则化手段存在，推理时模型已内化了真实运动的统计先验，从而在纯文本条件下也能生成超越单模态基线的高质量运动。



MotionDuet 是一个以扩散模型为骨干的多模态运动生成框架，核心目标是将文本语义与视频时空先验统一为互补的双条件信号，从而在纯文本推理时也能生成物理一致、时序连贯的三维人体运动。其整体 pipeline 遵循“视频特征提取 → 双流融合与自适应引导 → 多模态分布对齐”的三阶段范式（Figure 2）。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2511_18209/figures/002_Figure_2.jpg]]
*Figure 2: MotionDuet framework overview. It primarily consists of three key steps: 1) fine-tuning video motion dataset based on a pre-trained model and freezing the weights to focus on inference (orange background); 2) proposing a dual-stream control mechanism combined with auto-guidance mechanism to integrate video and text inputs, effectively guiding motion generation (blue background); and 3) utilizing the DUET module (purple dashed box) combined with DASH Loss to align and fuse multimodal information, enhancing overall information processing capabilities*

**输入与编码阶段**：给定文本描述 $\mathbf{t}$ 和参考视频帧序列 $I$，分别通过冻结的 CLIP 文本编码器 $\mathcal{E}_{\mathrm{CLIP}}$ 和经过微调的 VideoMAE 视频编码器 $\mathcal{E}_{\mathrm{Vim}}$ 提取语义嵌入 $\mathbf{T}$ 与时空特征 $\mathbf{V}$。VideoMAE 采用预训练的 ViT-G 骨干并在自建运动视频数据集上微调，以捕获真实人体运动的时序动态与空间结构先验。

**双流融合与条件注入**：$\mathbf{V}$ 和 $\mathbf{T}$ 进入 DUET（Dual-stream Unified Encoding and Transformation）融合模块，通过四条互补分支——快速傅里叶变换（FFT）分支捕获周期性时序规律、卷积分支聚焦局部空间几何、动态掩码机制（DMM）自适应选择与融合表示更接近的特征分支、以及残差连接保留原始信息——生成统一的多模态融合表示 $\mathbf{H}$。该表示随后被注入扩散去噪网络（基于 MLD 的 MldDenoiser），作为条件信号引导运动潜变量的逐步去噪生成。

**自适应引导与推理灵活性**：框架引入特征空间扰动自适应引导机制，通过对 $\mathbf{H}$ 施加 dropout 或高斯噪声生成退化副本，以退化分支替代传统分类器自由引导中的无条件分支，实现强/弱条件预测的自校正外推。当视频输入缺失时，$\mathbf{V}$ 置为零向量，DMM 自动路由至文本分支，使模型在纯文本推理模式下仍能保持生成质量。

**训练目标与分布对齐**：训练损失由扩散重建损失 $\mathcal{L}_{\mathrm{MLD}}$ 与 DASH（Distribution-Aware Structural Harmonization）正则项联合构成。DASH 损失包含令牌级余弦相似度边界损失 $\mathcal{L}_{\mathrm{token}}$ 和成对结构一致性损失 $\mathcal{L}_{\mathrm{pair}}$，通过在训练过程中将运动潜空间与真实视频特征分布对齐，将视频的时空先验“蒸馏”进运动生成器，从而在推理时即使不提供视频也能受益于这一正则化效果。

**模块关系总结**：VideoMAE 编码器与 CLIP 编码器为条件提供方，DUET 模块负责多模态信息融合与路由，自适应引导机制实现多模态平衡与互校正，DASH 损失在训练阶段完成跨模态分布对齐，MldVae 与 MldDenoiser 构成运动潜空间的压缩-生成闭环。各模块的参数量与训练状态详见 Table 12。

### 补充图表




MotionDuet 的核心架构围绕三个关键模块展开：**双条件编码**、**DUET 多模态融合** 和 **自适应引导**，辅以 **DASH 分布对齐损失** 在训练阶段注入视频时空先验。以下逐一拆解其公式与变量含义。

### 双条件编码

框架接收成对的视频帧序列 $I$ 和文本描述 $\mathbf{t}$，分别通过冻结的预训练编码器提取特征：

$$
\mathbf{V} = \mathcal{E}_{\mathrm{Vim}}(I), \quad \mathbf{T} = \mathcal{E}_{\mathrm{CLIP}}(\mathbf{t}) \tag{1}
$$

其中 $\mathcal{E}_{\mathrm{Vim}}$ 为 VideoMAE 编码器（实际使用 VideoMAEv2 ViT-G，在运动视频数据集上微调后冻结），输出视频时空特征 $\mathbf{V}$；$\mathcal{E}_{\mathrm{CLIP}}$ 为 CLIP 文本编码器，输出文本语义嵌入 $\mathbf{T}$。两者构成双条件输入，后续通过 DUET 模块融合为统一表示 $\mathbf{H}$：

$$
\mathbf{H} = \Theta_{\mathrm{DUET}}(\mathbf{V}, \mathbf{T}) \tag{3}
$$

### DUET 多模态融合模块

DUET（Dual-stream Unified Encoding and Transformation）是框架的融合核心，由四个互补分支组成：

1. **FFT 分支**：捕捉全局周期性与时序规律。对输入特征 $\mathbf{R}$ 进行快速傅里叶变换，通过可学习的幅度滤波器 $W$ 调制频域分量后逆变换：

   $$
   \mathbf{F} = \mathcal{F}^{-1} \big( W \odot \mathcal{F}(\mathbf{R}) \big) \tag{6}
   $$

   其中 $\mathcal{F}$ 为时域 FFT，$W$ 为可学习幅度权重，$\odot$ 表示逐元素乘法。该分支增强周期性运动线索（如行走、摆臂）的表达。

2. **卷积分支**：聚焦几何表示与局部空间关系，通过标准卷积操作提取细粒度特征。

3. **动态掩码机制（DMM）**：自适应选择更贴近融合表示的特征分支。设 $\mathbf{R}_{\mathrm{fusion}}$ 为当前融合特征，$\mathbf{R}_0$ 为运动分支特征，$\mathbf{R}_{\mathrm{b}}$ 为视频分支特征，计算 L2 距离：

   $$
   d_0 = \| \mathbf{R}_{\mathrm{fusion}} - \mathbf{R}_0 \|_2, \quad d_{\mathrm{b}} = \| \mathbf{R}_{\mathrm{fusion}} - \mathbf{R}_{\mathrm{b}} \|_2 \tag{7}
   $$

   根据距离比较生成二值掩码：

   $$
   \mathrm{Mask} = \begin{cases} 1, & \mathrm{if~} d_{\mathrm{o}} > d_{\mathrm{b}}, \\ 0, & \mathrm{otherwise.} \end{cases} \tag{8}
   $$

   最终 DMM 输出为自适应加权融合：

   $$
   \mathbf{R}_{\mathrm{DMM}} = \mathbf{Mask} \cdot \mathbf{R}_0 + (1 - \mathbf{Mask}) \cdot \mathbf{R}_{\mathrm{b}} \tag{9}
   $$

   当视频输入缺失时，$\mathbf{V}$ 置为零向量，DMM 自然路由至运动分支，实现缺失模态的优雅处理。

4. **残差连接**：将上述分支输出与原始输入相加，保证梯度流动与训练稳定性。

消融实验（Table 9）证实：采用卷积分支的 DUET 配置取得最优 FID 0.101 和 R@3 0.755，显著优于简单串联或注意力融合。

### 自适应引导机制

传统分类器自由引导（CFG）需要训练无条件分支，MotionDuet 改用**特征空间扰动**替代：对融合表示 $\mathbf{H}$ 施加退化操作，生成“弱条件”副本，利用强/弱条件预测差异进行自校正。

两种退化策略：

- **Dropout 扰动**：随机置零 $p$ 比例的特征维度：

  $$
  \tilde{\mathbf{H}}^{(T)} = \mathrm{Dropout}(\mathbf{H}; \mathcal{D}) \tag{11}
  $$

- **高斯噪声扰动**：添加各向同性高斯噪声：

  $$
  \tilde{\mathbf{H}}^{(\sigma)} = \mathbf{H} + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2) \tag{12}
  $$

引导输出公式为：

$$
\hat{\mathbf{x}}_t = (1 + \omega) \cdot \hat{\mathbf{x}}_t^{\mathrm{strong}} - \omega \cdot \hat{\mathbf{x}}_t^{\mathrm{weak}} \tag{13}
$$

其中 $\hat{\mathbf{x}}_t^{\mathrm{strong}}$ 为原始融合条件预测，$\hat{\mathbf{x}}_t^{\mathrm{weak}}$ 为退化条件预测，$\omega$ 为固定外推因子（通过轻量验证搜索一次后固定）。消融表明 Dropout 扰动比高斯噪声更稳定（Table 7/8），是推荐的退化策略。

### DASH 分布对齐损失

训练阶段的核心创新：通过 DASH（Distribution-Aware Structural Harmonization）损失将视频特征的时空先验注入运动潜空间，缩小分布差距。DASH 由两部分组成：

**令牌级边界损失**：约束运动特征令牌 $\hat{z}_{t,\mathrm{d},i}$ 与对应视频令牌 $v_i$ 的余弦相似度不低于边界 $m_{\mathrm{cos}}$：

$$
\mathcal{L}_{\mathrm{token}} = \frac{1}{N} \sum_{i=1}^{N} \mathrm{ReLU}(1 - m_{\mathrm{cos}} - \cos(\hat{z}_{t,\mathrm{d},i}, v_i)) \tag{15}
$$

**成对结构一致性损失**：保持特征空间内令牌间相似度结构与视频特征一致，边界为 $m_{\mathrm{pair}}$：

$$
\mathcal{L}_{\mathrm{pair}} = \frac{1}{N^2} \sum_{i,j=1}^{N} \mathrm{ReLU}\big( |\cos(\hat{z}_{t,\mathrm{d},i}, \hat{z}_{t,\mathrm{d},j}) - \cos(v_i, v_j)| - m_{\mathrm{pair}} \big) \tag{16}
$$

DASH 总损失为两者之和：

$$
\mathcal{L}_{\mathrm{DASH}} = \mathcal{L}_{\mathrm{token}} + \mathcal{L}_{\mathrm{pair}} \tag{17}
$$

最终训练目标联合扩散重建与分布对齐：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{MLD}} + \lambda_{\mathrm{DASH}} \mathcal{L}_{\mathrm{DASH}} \tag{18}
$$

其中 $\mathcal{L}_{\mathrm{MLD}}$ 为标准扩散去噪均方误差（Eq. 14），$\lambda_{\mathrm{DASH}}$ 为平衡系数。消融实验（Table 6）显示 $\lambda_{\mathrm{DASH}}$ 取值敏感：适中权重显著改善 FID 和 R@3，但过大（如 300）会导致 FID 急剧上升至 14.676，表明过度对齐会破坏运动生成质量。

### 关键因果机制总结

DASH 损失通过令牌级与结构级双重正则化，将视频特征的分布先验注入运动潜空间，使得即使在纯文本推理（无视频输入）时，生成的运动仍能保持物理一致性与时序连贯性。DUET 模块则通过频域增强、动态掩码选择与残差融合，实现多模态信息的有效整合。自适应引导以退化分支替代无条件分支，稳定平衡多模态条件强度，且 $\omega$ 可固定无需动态调整。三个模块协同作用，构成了“训练时视频正则化、推理时文本驱动”的核心因果链路。



## 实验与关键发现

### 主实验结果

MotionDuet 在 HumanML3D 基准上与多种文本到运动生成方法进行了系统对比（Table 1）。在纯文本推理模式下（无视频引导），MotionDuet 取得 **R@3 0.795±.003**、**FID 0.179±.024**，相较于骨干网络 **MLD**（Motion Latent Diffusion）的 R@3 0.772 和 FID 0.473，FID 大幅降低 0.294，表明生成运动分布与真实分布的统计距离显著缩小。同时，Diversity 指标为 9.532，更接近真实数据的 9.503，而 MLD 为 9.724，说明生成运动未牺牲多样性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2511_18209/figures/004_Table_1.jpg]]
*Table 1: Performance comparison of various methods on the HumanML3D dataset. ↑ indicates higher is better, ↓ indicates lower is better, and → indicates closer is better. ’Filtering’ denotes that data cleaning has been applied to the HumanML3D dataset to remove noisy or low-quality samples. † indicates that during testing, no video was used as guidance, the motion was generated solely based on text. We highlight the top three results in each column with Red bold (best), Blue underline (second), and Green (third)*

与同期强基线对比：**MoMask** 在 R@3 和 FID 上仍保持一定优势（R@3 0.803，FID 0.095），但 MotionDuet 在 Multimodal Distance（MM Dist 3.154 vs MoMask 3.130）和 Multimodality（MM 2.496 vs MoMask 2.450）上达到可比甚至更优水平。关键差异在于：MoMask 等纯文本方法的定量优势源于其训练目标与评估指标的直接对齐，而 MotionDuet 通过视频正则化注入真实时空先验，在定性层面展现出更优的运动方向准确性与时序连贯性（见 Figure 3 定性对比）。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2511_18209/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative results. MotionDuet captures motion direction and temporal coherence more accurately than prior methods, more results can be seen in Appendix D. MoMask uses parallel masked modeling, while MLD adopts progressive diffusion denoising. In both rows, MotionDuet achieves smoother coordination and more precise dynamics. † denotes text-only inference without video guidance*

在经数据清洗的 HumanML3D 子集上，MotionDuet 的 FID 进一步降至 0.084，R@3 提升至 0.764（Table 11），验证了视频正则化策略在高质量数据下的增益。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2511_18209/figures/018_Table_11.jpg]]
*Table 11: Evaluation on each component. The top results are highlighted in each column with bold*

### 消融实验

#### DUET 融合模块的有效性

Table 9 展示了不同融合策略的逐步叠加效果。以元素加法（Element-wise Addition）为基础融合方式，逐步引入 DUET 各子模块：

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2511_18209/figures/016_Table_9.jpg]]
*Table 9: Performance comparison of different multimodal fusion strategies. Table indentation denotes the sequential integration of modules, with each indented block representing a component appended downstream within the overall architecture. The top results in each column are highlighted with bold (best)*

- 基础加法融合：FID 0.168，R@3 0.747
- 加入 FFT 分支：FID 降至 0.131，R@3 升至 0.752
- 加入卷积分支（Conv）：FID 进一步降至 **0.101**，R@3 达到 **0.755**
- 加入 DMM 动态掩码机制：FID 0.102，R@3 0.751（与 Conv 相当）
- 加入残差连接：FID 0.108，R@3 0.752

卷积分支的增益最为显著，表明局部空间关系的显式建模对运动特征融合至关重要。FFT 分支通过频域可学习幅度滤波器 $W$ 增强周期运动线索，对周期性动作（如行走、跑步）的时序一致性有直接贡献。DMM 机制在视频模态缺失时可自动路由至文本分支，实现无缝降级。

#### DASH 损失的作用

Table 11 显示，在基础 MLD 损失上叠加 DASH 损失后，FID 从 0.168 降至 **0.084**，R@3 从 0.747 升至 **0.764**。DASH 损失由令牌级余弦相似度边界损失 $\mathcal{L}_{\mathrm{token}}$ 和成对结构一致性损失 $\mathcal{L}_{\mathrm{pair}}$ 组成，分别约束运动潜变量与视频特征的逐令牌对齐和特征空间内成对相似度结构的保持。

Table 6 的 $\lambda_{\mathrm{DASH}}$ 参数研究表明该超参数取值敏感：当 $\lambda_{\mathrm{DASH}} = 100$ 时性能最优；过大的权重（如 300）会导致 FID 急剧恶化至 14.676，说明过强的分布对齐约束会干扰扩散去噪主任务的学习。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2511_18209/figures/013_Table_6.jpg]]
*Table 6: Parameter Study on λDASH. ↑ indicates higher is better, and ↓ indicates lower is better*

#### 视频编码器的选择与微调

Table 10 对比了不同视频编码器的效果。VideoMAEv2 ViT-G 经微调后 FID 为 0.179，显著优于零样本使用的 0.238，验证了在运动视频数据上进行领域适配的必要性。轻量化编码器（如 ViT-B）的性能下降明显，FID 升至 0.298，表明视频特征提取能力是整体性能的关键瓶颈。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2511_18209/figures/017_Table_10.jpg]]
*Table 10: Performance Assessment of the Video Encoders. ↑ indicates higher is better, ↓ indicates lower is better, and → indicates closer is better*

#### 自适应引导机制

Table 7 和 Table 8 分别验证了退化策略和引导权重的选择。Dropout 扰动（随机置零 $p$ 比例特征维度）比高斯噪声扰动更稳定，在不同 $\omega$ 取值下性能波动更小。固定外推因子 $\omega$ 经一次性轻量验证搜索后即可固定，无需逐样本调整，降低了推理复杂度。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2511_18209/figures/014_Table_7.jpg]]
*Table 7: Parameter Study on ω and Dropout. ↑ indicates higher is better, and*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2511_18209/figures/015_Table_8.jpg]]
*Table 8: Evaluation of Loss Function. ↑ indicates higher is better, ↓ indicates lower is better, and → indicates closer is better*

### 失败模式与局限性

1. **定量指标的固有偏差**：由于引入视频特征导致分布差异，MotionDuet 的 FID 与 R@3 在纯文本设定下可能逊于 MoMask 等纯文本优化方法，但定性上生成的运动更符合物理约束和时序逻辑。

2. **数据质量问题**：视频数据清洗后仍有约 39% 的异常样本（蒙皮错误、局部关节失调等，见 Figure 9-11），这些噪声样本在训练中可能引入不稳定梯度，影响收敛。

3. **计算资源需求**：VideoMAE ViT-G 微调需 8×A800-80GB GPU 约一周，VAE 训练需单卡 30 小时，完整视频数据集渲染需 45 天×4 GPU，复现门槛较高。

4. **泛化边界**：对未见过真实视频的泛化仍局限于训练动作类型，复杂动作组合（如芭蕾旋转+棒球投掷的混合）可能存在拓扑误判。

5. **超参数敏感性**：$\lambda_{\mathrm{DASH}}$ 和 dropout 比例 $p$ 需网格搜索，取值窗口较窄，部署调参成本较高。

### 重要图表结论

- **Table 1**：MotionDuet 在纯文本推理下 FID 0.179，较 MLD 降低 62%，Diversity 更接近真实分布。
- **Table 9**：DUET 卷积分支是融合性能的核心贡献者，FID 从 0.168 降至 0.101。
- **Table 11**：DASH 损失使 FID 进一步降至 0.084，验证了分布对齐正则化的必要性。
- **Table 10**：ViT-G 微调 vs 零样本的 FID 差距（0.179 vs 0.238）表明领域适配不可忽略。
- **Table 6**：$\lambda_{\mathrm{DASH}}$ 在 100 附近最优，300 时 FID 崩溃至 14.676，需谨慎调参。

### 补充图表


![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2511_18209/figures/009_Table_5.jpg]]
*Table 5: Parameter study for ω and dropout. Only core metrics reported. More grid searching results are shown in Appendix K*



## 定位与知识库关联

### 1. 与基线方法的关系

MotionDuet 构建于**运动潜空间扩散模型**（Motion Latent Diffusion, MLD）的去噪骨干之上，继承了潜变量压缩与扩散生成的基本范式，但在条件注入、多模态融合和分布正则化三个关键维度上进行了系统性改造。

*   **相对于 MLD 的改进**：MLD 仅依赖 CLIP 文本嵌入作为唯一条件信号，缺乏对真实运动时空统计特性的显式建模。MotionDuet 引入视频条件作为**分布先验**，通过冻结的 VideoMAE 编码器提取视频时空特征，与文本嵌入构成双条件输入。这一改动使得模型在训练阶段能够接触到真实运动的时序结构与物理约束，即使在纯文本推理时也能受益于视频正则化带来的分布校准。
*   **相对于 MoMask 等掩码建模方法**：MoMask 采用并行掩码建模策略，在定量指标（R@3, FID）上表现强劲，但其生成的运动在定性层面存在方向捕捉不准确、时序连贯性不足的问题（见 Figure 3）。MotionDuet 通过 DUET 模块中的 FFT 分支显式建模周期运动线索，以及 DASH 损失强制运动潜空间与视频特征分布对齐，在保持竞争力的定量指标同时，显著提升了运动的物理一致性和时序平滑度。
*   **相对于 CrossDiff 等交叉注意力扩散方法**：CrossDiff 通过交叉注意力融合文本与运动模态，但缺乏对视频模态的支持和分布级对齐。MotionDuet 的 DUET 模块采用**四分支融合架构**（FFT + 卷积 + DMM + 残差），通过动态掩码机制自适应选择更接近融合表示的特征分支，相较于简单的注意力融合具有更强的多模态交互能力。
*   **相对于 T2M、MDM、MotionDiffuse、MotionGPT、Fg-T2M**：这些方法均仅从文本生成运动，无法利用视频中蕴含的丰富时空先验。MotionDuet 首次将视频正则化引入文本到运动生成框架，通过**训练时视频条件注入 + 推理时纯文本生成**的策略，实现了对基线方法的全面超越（Table 1：纯文本推理下 R@3 0.795, FID 0.179，显著优于 MLD 的 0.772 和 0.473）。

### 2. 适用边界

*   **输入模态**：训练阶段需要配对的文本-视频-运动三元组数据；推理阶段支持纯文本、纯视频或文本-视频组合三种模式。当视频输入缺失时，DUET 模块中的 DMM 机制自动将视频特征置零并路由至文本分支，无需额外处理。
*   **运动类型覆盖**：模型在 HumanML3D 数据集涵盖的日常动作（行走、跑步、跳跃、舞蹈等）上表现良好，对真实视频中的复杂动作（如芭蕾旋转、棒球投掷、高尔夫挥杆）也展现出一定的泛化能力（Figure 4）。但泛化范围受限于训练动作类型，未见过的极端动作组合可能导致拓扑误判。
*   **计算资源需求**：训练需要大规模 GPU 集群（VideoMAE 微调需 8×A800-80GB 约一周，VAE 训练需单卡 A800 约 30 小时，扩散模型训练需 2×H100-80GB）。视频数据集的渲染构建耗时约 45 天×4 GPU，整体复现门槛较高。
*   **数据质量依赖**：视频数据清洗后仍存在约 39% 的异常样本（蒙皮错误、局部失调、轻度运动偏差等，见 Figure 9-11），可能影响训练稳定性和生成质量的上限。

### 3. 局限与开放问题

**已识别的局限**：

1. **定量指标的权衡**：引入视频特征导致分布差异，在过滤后的 HumanML3D 数据集上，纯文本推理的 FID（0.179）和 R@3（0.795）略逊于 MoMask（FID 0.045, R@3 0.801）。这表明视频正则化在提升定性质量的同时，可能对纯文本条件下的分布匹配精度产生轻微负面影响。
2. **超参数敏感性**：DASH 损失的权重 λ_DASH 对性能影响显著——过大的权重（如 300）会导致 FID 急剧上升至 14.676（Table 6）。自适应引导的外推因子 ω 和 dropout 比例需要通过网格搜索确定（Table 5/7），增加了部署调参成本。
3. **视频编码器规模依赖**：微调后的 ViT-G 编码器显著优于零样本 ViT-G（FID 0.179 vs 0.238，Table 10），但轻量级编码器（如 ViT-B）下的生成质量尚不明确，限制了低资源场景的部署。
4. **数据清洗自动化不足**：当前视频数据清洗依赖人工规则与运动先验知识，39% 的异常率表明自动化清洗方法仍有较大改进空间。

**开放问题**：

1. **分布对齐的理论深化**：DASH 损失采用令牌级余弦相似度与成对结构一致性作为对齐目标，本质上是一种启发式分布匹配。更先进的分布对齐方法（如最优传输、最大均值差异）能否进一步缩小多模态差距，提升定量指标？
2. **轻量化与部署**：如何在轻量级视频编码器（如 ViT-B）下保持运动生成质量？是否可以通过知识蒸馏将 ViT-G 的时空先验迁移至更小的编码器？
3. **数据质量闭环**：能否结合运动先验（如物理约束、骨骼长度一致性）构建自动化数据清洗流水线，将异常率从 39% 降至可接受水平，减少人工干预？
4. **跨模态扩展性**：视频正则化策略是否可以迁移至其他时序生成任务（如手势生成、舞蹈合成）？DUET 融合框架能否扩展到音频、场景图等其他模态，实现更通用的可控运动生成？
5. **真实视频泛化边界**：模型对未见过真实视频的泛化仍局限于训练动作类型的组合。如何通过少样本学习或测试时自适应，扩展对开放域视频的运动理解与生成能力？



## 原文 PDF

![[paperPDFs/arxiv_2025/MotionDuet:_Dual-Conditioned_3D_Human_Motion_Generation_with_Video-Regularized_Text_Learning.pdf]]
