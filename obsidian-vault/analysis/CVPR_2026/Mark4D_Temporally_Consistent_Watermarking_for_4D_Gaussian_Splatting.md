---
title: "Mark4D: Temporally-Consistent Watermarking for 4D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Mark4D_Temporally_Consistent_Watermarking_for_4D_Gaussian_Splatting.pdf
project_link: null
code_link: null
aliases:
- Mark4D
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过沿高斯运动轨迹施加位置偏移来嵌入水印，并采用运动自适应损失权重根据帧间运动幅度调节水印监督强度，从而在保持几何和时间一致性的同时实现鲁棒的水印嵌入。
primary_logic: 利用X-CLIP视频-文本潜在空间进行水印解码，避免像素级失真；引入轨迹对齐损失确保高斯沿运动路径平滑变化以保持几何一致性；设计运动自适应损失加权，在静态帧维持视觉质量，在动态帧增强水印鲁棒性。
claims:
- X-CLIP引导的解码器在潜在空间而非像素空间恢复水印，实现鲁棒且不易察觉的嵌入。
- 轨迹对齐偏移通过最小化偏移与局部运动切向的余弦距离，确保水印沿高斯运动路径平滑演化，保持几何保真度。
- 运动自适应损失加权根据帧间平均运动幅度动态调整消息损失权重，在静止帧降低权重以避免过拟合，在动态帧提高权重以加强水印嵌入。
- D-NeRF + DyNeRF (平均) 上 Bit Acc (%) @32 bits (帧级) = 96.34
---

# Mark4D: Temporally-Consistent Watermarking for 4D Gaussian Splatting

> [!tip] 核心洞察
> 利用X-CLIP视频-文本潜在空间进行水印解码，避免像素级失真；引入轨迹对齐损失确保高斯沿运动路径平滑变化以保持几何一致性；设计运动自适应损失加权，在静态帧维持视觉质量，在动态帧增强水印鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Mark4D：面向4D高斯溅射的时间一致性水印方法 |
| 英文题名 | Mark4D: Temporally-Consistent Watermarking for 4D Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lee_Mark4D_Temporally-Consistent_Watermarking_for_4D_Gaussian_Splatting_CVPR_2026_paper.html) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Mark4D |
| Dataset | D-NeRF + DyNeRF |

> [!tip] 效果简介
> - D-NeRF + DyNeRF (平均) 上，Bit Acc (%) @32 bits (帧级) 96.34 vs 88.33 (GuardSplat) (+8.01)；PSNR (dB) @32 bits (帧级) 42.32 vs 38.69 (GuardSplat) (+3.63)；Bit Acc (%) @64 bits Ours vs 3D-GSW (+9.35%p)。

## 概要

**核心问题**：将现有3DGS水印方法直接应用于动态4DGS时，高斯体的连续时空变形与不同运动动态导致几何保真度损失、时间不一致，且缺乏针对运动变化的自适应监督机制。

**方法定位**：Mark4D 提出三项关键设计——(1) 在X-CLIP视频-文本潜在空间而非像素域进行水印解码，避免像素级失真；(2) 沿高斯运动轨迹施加位置偏移以嵌入水印，并通过轨迹对齐损失保持几何一致性；(3) 运动自适应损失加权，根据帧间运动幅度动态调节水印监督强度。

**主要结果**：在 D-NeRF 与 DyNeRF 数据集上，Mark4D 在32位水印容量下平均比特准确率达96.34%，PSNR达42.32 dB，分别超出最强基线 GuardSplat (Chen et al., CVPR 2025) 8.01个百分点和3.63 dB；在64位容量下，比特准确率与PSNR分别领先 3D-GSW (Jang et al., CVPR 2025) 9.35个百分点和10.40 dB。消融实验证实，轨迹对齐损失、空间偏移与运动自适应加权均为性能提升的关键因素。



### 4D高斯溅射与版权保护需求

4D高斯溅射（4D Gaussian Splatting, 4DGS）将3D高斯溅射（3DGS）扩展到动态场景，通过变形场驱动高斯体在时间维度上连续运动，实现了高质量的新视角动态渲染。其核心表示是一组随时刻 $t$ 变形的高斯基元：

$$\tilde{\mathcal{G}}(t) = \{ \mathbf{x}_i(t), h_i(t), \alpha_i(t), \Sigma_i(t) \}_{i=1}^{N_{\mathcal{G}}}$$

每个高斯的空间影响由密度函数 $g_i(\mathbf{z}) = \exp\left(-\frac{1}{2}(\mathbf{z} - \mathbf{x}_i)^\top \Sigma_i^{-1} (\mathbf{z} - \mathbf{x}_i)\right)$ 刻画，并通过投影矩阵 $\mathbf{P}$、视角变换 $\mathbf{W}$ 和雅可比 $\mathbf{J}$ 映射到2D图像平面：$\mathbf{x}_i^{2D} = \mathbf{P}\mathbf{W}\mathbf{x}_i$，$\Sigma_i^{2D} = \mathbf{J}\mathbf{W}\Sigma_i\mathbf{W}^\top\mathbf{J}^\top$。

随着4DGS模型的商业价值日益凸显，模型创作者面临严重的版权侵权风险：恶意用户可下载已发布的4DGS模型，对其渲染视频施加各种扭曲后宣称虚假所有权。因此，亟需一种能够在4DGS模型中嵌入鲁棒且不可见水印的技术，使合法所有者能够从被篡改的模型或渲染视频中可靠恢复身份消息，以验证版权归属（如Figure 1所示）。

### 现有水印方法的局限性

当前3DGS水印方法（如 **GuardSplat**（Chen et al., CVPR 2025）、**3D-GSW**（Jang et al., CVPR 2025）、**GaussianMarker**（Huang et al., NeurIPS 2024））主要针对静态场景设计，其核心策略是直接微调全部或部分高斯参数以嵌入水印。当将这些方法简单迁移到动态4DGS时，面临三个根本性瓶颈：

1. **几何保真度损失**：4DGS中的高斯体随时间连续变形，直接修改高斯参数会破坏变形场的几何一致性，导致渲染结果出现明显的几何伪影和表面不一致。

2. **时间不一致性**：现有方法缺乏对高斯沿运动轨迹的约束，水印嵌入在不同时刻可能产生冲突的信号，造成渲染视频在时间维度上的抖动和不连续。

3. **运动动态适应缺失**：真实场景的运动幅度分布极不均匀。如Figure 2所示，合成数据集D-NeRF的运动幅度相对集中，而真实场景数据集DyNeRF则呈现更广泛的运动分布。对所有帧施加均匀的水印监督强度，会导致静态帧过拟合（视觉质量下降）而动态帧欠拟合（水印恢复率不足）。

此外，视频水印方法 **VideoSeal**（Fernandez et al., arXiv 2024）虽然支持视频级解码，但其在像素域嵌入水印的方式在4DGS渲染场景下不可见性较差，且同样未考虑场景的运动动态特性。

### 本文动机与核心思路

针对上述瓶颈，Mark4D提出了三个协同设计：

- **潜在空间解码**：摒弃像素级水印恢复，转而利用X-CLIP视频-文本潜在空间进行消息解码，从根本上提升对像素级扭曲的鲁棒性，同时避免在像素域引入可见失真。

- **轨迹对齐偏移**：将水印信号沿高斯运动轨迹的方向嵌入——仅对位置 $\mathbf{x}_i(t)$ 和球谐系数 $h_i(t)$ 添加可学习偏移 $\varepsilon_i(t)$ 和 $\delta_i(t)$，并通过轨迹对齐损失约束位置偏移与局部运动切向一致，从而保证水印在时间维度上平滑演化，维持几何保真度。

- **运动自适应监督**：根据帧间平均运动幅度动态调节水印损失权重 $\lambda_{S_t}$——在静止帧降低权重以保持视觉质量，在剧烈运动帧提高权重以增强水印嵌入强度，使模型自适应地平衡不可见性与鲁棒性。



## 核心方法与创新机理

Mark4D 针对动态 4D 高斯溅射（4DGS）场景中水印嵌入的核心瓶颈——时间不一致性与几何保真度损失——提出了三个环环相扣的创新机制，构成一条从“水印如何解码”到“水印如何嵌入”再到“嵌入强度如何调控”的完整因果链。

### 1. 从像素域到视频-文本潜在空间的解码范式迁移

现有 3DGS 水印方法（如 **GuardSplat**（Chen et al., CVPR 2025）、**3D-GSW**（Jang et al., CVPR 2025））均依赖像素级图像解码器直接从渲染帧中恢复水印消息。这种设计在动态场景中面临双重困境：像素级失真易被感知，且帧间独立解码忽略了视频的时序关联。

Mark4D 的解码器 **D_M** 是一个仅 3 层的 MLP，但它并不直接接收像素输入，而是工作在冻结的 **X-CLIP 视频-文本潜在空间**之上。具体而言，水印消息的恢复路径为：

$$\hat{M} = \mathcal{D}_M( \mathcal{E}_V( \hat{I}_{\mathcal{S}_t} ) )$$

其中 $\mathcal{E}_V$ 是冻结的 X-CLIP 视频编码器（ViT-B-32，潜在维度 512），它将渲染视频片段 $\hat{I}_{\mathcal{S}_t}$ 映射为富含时空语义的潜在表示；$\mathcal{D}_M$ 再从中解码出 $L$ 位水印比特。训练阶段，$\mathcal{D}_M$ 通过冻结的文本编码器 $\mathcal{E}_W$ 学习从任意随机映射的文本令牌中重建二进制消息，优化目标为二元交叉熵损失：

$$\mathcal{L}_{\mathrm{msg}} = - \sum_{i=1}^{L} [ m_i \log \hat{m}_i + (1 - m_i) \log (1 - \hat{m}_i) ]$$

这一设计的核心优势在于：潜在空间天然对像素级扰动不敏感，使得水印嵌入可以在不牺牲视觉不可见性的前提下获得更强的鲁棒性。实验证据表明，在 32 位消息的帧级解码设定下，Mark4D 的平均比特准确率达到 **96.34%**，较 GuardSplat 的 88.33% 提升了 **+8.01 个百分点**（Table 1），同时 PSNR 从 38.69 dB 提升至 **42.32 dB**，验证了“潜在空间解码 → 更优的容量-保真度权衡”这一因果路径。

### 2. 轨迹对齐偏移：沿运动路径嵌入水印以保持几何一致性

将 3DGS 水印方法直接迁移至 4DGS 时，高斯体在连续时间步上的变形使得独立微调各帧参数极易破坏几何一致性。Mark4D 的核心操作是仅对变形后的高斯位置 $\mathbf{x}_i(t)$ 和球谐系数 $h_i(t)$ 添加可学习的偏移量 $\varepsilon_i(t)$ 和 $\delta_i(t)$，形成水印高斯集：

$$\tilde{\mathcal{G}}(t) = \{ \mathbf{x}_i(t) + \varepsilon_i(t),\, h_i(t) + \delta_i(t),\, \alpha_i(t),\, \Sigma_i(t) \}_{i=1}^{N_{\mathcal{G}}}$$

关键创新在于对位置偏移 $\varepsilon_i(t)$ 施加的**轨迹对齐约束**。定义高斯 $i$ 在时间 $\tau$ 的运动切向为 $\mathbf{d}_i(\tau) = \mathbf{x}_i(\tau+\Delta t) - \mathbf{x}_i(\tau)$，轨迹对齐损失迫使偏移方向与局部运动方向一致：

$$\mathcal{L}_{\mathrm{align}} = \frac{1}{N_{\mathcal{G}} T} \sum_{\tau \in S_t} \sum_{i=1}^{N_{\mathcal{G}}} \left( 1 - \frac{\varepsilon_i(\tau) \cdot \mathbf{d}_i(\tau)}{\|\varepsilon_i(\tau)\|_2 \|\mathbf{d}_i(\tau)\|_2} \right)$$

这一设计保证了水印信号沿高斯自然运动路径平滑演化，而非在空间中任意扰动。消融实验（Table 3, Figure 5）提供了强因果证据：移除 $\mathcal{L}_{\mathrm{align}}$ 后，渲染表面出现明显的几何不一致性，PSNR 和 Bit Acc 均显著下降。同时，仅使用外观偏移 $\delta_i(t)$ 而移除空间偏移 $\varepsilon_i(t)$ 会导致明显的颜色偏移且水印容量不足，证实了两种偏移类型的互补必要性。

### 3. 运动自适应损失加权：动态平衡视觉质量与水印嵌入强度

真实动态场景中，不同时间窗口的运动幅度差异显著（Figure 2 揭示了 DyNeRF 相比 D-NeRF 具有更广的运动幅度分布）。对所有帧均匀施加相同的水印监督强度，会导致静止帧过拟合（视觉质量下降）而剧烈运动帧嵌入不足（水印鲁棒性差）。

Mark4D 引入**运动自适应损失权重** $\lambda_{S_t}$ 来解决这一矛盾。首先计算时间窗口 $S_t$ 内所有高斯的平均运动幅度：

$$v_{S_t} = \frac{1}{N_{\mathcal{G}} T} \sum_{\tau \in S_t} \sum_{i=1}^{N_{\mathcal{G}}} \| \mathbf{x}_i(\tau+\Delta t) - \mathbf{x}_i(\tau) \|_2$$

经全局归一化得到 $\beta_{S_t} \in [0, 1]$ 后，通过线性插值动态调节消息损失的权重：

$$\lambda_{S_t} = (1 - \beta_{S_t}) \lambda_{\min} + \beta_{S_t} \lambda_{\max}$$

其中 $\lambda_{\min}$ 和 $\lambda_{\max}$ 为预设的超参数边界。最终的总损失函数为：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{S_t} \mathcal{L}_{\mathrm{msg}} + \lambda_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{align}} \mathcal{L}_{\mathrm{align}}$$

这一机制的效果在运动分布更广的 DyNeRF 数据集上尤为显著：启用 $\lambda_{S_t}$ 后，Bit Acc 提升 **+3.14**，PSNR 提升 **+2.18**（Table 4）。Figure 6 进一步显示，$\lambda_{S_t}$ 使得各视频片段的比特准确率和 PSNR 随时间变化更加平稳，消除了均匀加权时的大幅波动，验证了“运动幅度感知 → 时间一致性监督”这一因果机制的有效性。

### 创新点之间的协同关系

上述三个创新并非孤立存在，而是形成了一条递进式的因果链路：**潜在空间解码**（创新 1）为水印嵌入提供了对像素级扰动鲁棒的优化目标；**轨迹对齐偏移**（创新 2）确保了在满足该目标的过程中不破坏 4DGS 的几何与时间一致性；**运动自适应加权**（创新 3）则进一步精细调控不同运动状态下的嵌入强度，使得静态帧保持视觉质量、动态帧获得足够的鲁棒性。三者共同实现了“不可见性-容量-鲁棒性-时间一致性”的四维平衡，这是现有 3DGS 水印方法直接应用于 4D 场景时无法达成的。



Mark4D 采用两阶段训练范式，将水印信息嵌入到预训练的 4D 高斯溅射模型中，同时保持渲染结果的几何保真度和时间一致性。其核心设计围绕三个关键机制展开：**潜在空间水印解码**、**轨迹对齐偏移**和**运动自适应损失加权**。

### 两阶段训练流程

**第一阶段：消息解码器预训练。** 该阶段独立于 4DGS 模型，目标是训练一个能够在潜在空间中恢复水印消息的解码器 $D_M$。具体而言，使用冻结的 X-CLIP 文本编码器 $E_W$ 将随机映射的文本令牌 $W$ 编码为文本嵌入，随后由 $D_M$（一个 3 层 MLP）从该嵌入中预测 $L$ 位水印消息 $\hat{M}$，并通过二元交叉熵损失进行优化。这一设计使解码器学会在语义潜在空间中关联文本嵌入与二进制消息，而非依赖像素级特征，从而从根本上增强了对像素域失真的鲁棒性。

**第二阶段：水印嵌入到 4DGS。** 在预训练 4DGS 模型 $\mathcal{G}$ 及其变形网络 $F_\theta$ 的基础上，对每个时间戳 $t$ 下的高斯体施加可学习的偏移量，得到水印模型：

$$\tilde{\mathcal{G}}(t) = \{ \mathbf{x}_i(t) + \varepsilon_i(t), h_i(t) + \delta_i(t), \alpha_i(t), \Sigma_i(t) \}_{i=1}^{N_{\mathcal{G}}}$$

其中 $\varepsilon_i(t)$ 为位置偏移，$\delta_i(t)$ 为球谐（SH）系数偏移，而透明度 $\alpha_i(t)$ 和协方差 $\Sigma_i(t)$ 保持不变。渲染后的帧序列 $\hat{I}_{\mathcal{S}_t}$ 经过可微失真模块 $\mathcal{A}$ 施加帧级和视频级失真后，由冻结的 X-CLIP 视频编码器 $E_V$ 提取潜在表示，再由第一阶段预训练好的 $D_M$ 恢复水印消息：

$$\hat{M} = \mathcal{D}_M( \mathcal{E}_V( \mathcal{A}( \hat{I}_{\mathcal{S}_t} ) ) )$$

### 核心模块关系

整个框架的模块间数据流和约束关系如 **Figure 3** 所示，各模块的职责分工如下：

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Mark4D_Temporally/figures/003_Figure_3.jpg]]
*Figure 3: Overall framework of Mark4D. In the first stage, the watermark decoder*

| 模块 | 角色 | 阶段 |
|------|------|------|
| $E_W$（X-CLIP 文本编码器） | 将文本令牌编码为嵌入，用于训练 $D_M$ | 第一阶段 |
| $D_M$（消息解码器） | 3 层 MLP，从潜在表示恢复 $L$ 位水印 | 第一阶段训练，第二阶段冻结 |
| $E_V$（X-CLIP 视频编码器） | 提取渲染视频的潜在表示 | 第二阶段，冻结 |
| $\mathcal{A}$（可微失真模块） | 施加帧级和视频级失真以增强鲁棒性 | 第二阶段 |
| $\varepsilon_i(t), \delta_i(t)$（可学习偏移） | 在高斯位置和 SH 系数上嵌入水印信号 | 第二阶段 |
| $\mathcal{L}_{\mathrm{align}}$（轨迹对齐损失） | 约束 $\varepsilon_i(t)$ 沿高斯运动路径方向 | 第二阶段 |
| $\lambda_{S_t}$（运动自适应权重） | 根据帧间运动幅度动态调节消息损失贡献 | 第二阶段 |

### 优化目标

最终的总损失函数综合了三个优化目标：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{S_t} \mathcal{L}_{\mathrm{msg}} + \lambda_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{align}} \mathcal{L}_{\mathrm{align}}$$

- **消息损失 $\mathcal{L}_{\mathrm{msg}}$**：二元交叉熵，衡量恢复消息 $\hat{M}$ 与真实消息 $M$ 的比特级一致性。
- **重建损失 $\mathcal{L}_{\mathrm{recon}}$**：结合 L1 和 LPIPS 损失，维持渲染图像与原始帧的视觉保真度。
- **轨迹对齐损失 $\mathcal{L}_{\mathrm{align}}$**：最小化 $\varepsilon_i(t)$ 与高斯运动切向 $\mathbf{d}_i(t)$ 的余弦距离，确保水印沿运动路径平滑演化，保持几何一致性。

其中 $\lambda_{S_t}$ 是运动自适应的动态权重，根据时间窗口 $\mathcal{S}_t$ 内所有高斯的平均位移 $v_{S_t}$ 归一化后插值得到，运动幅度越大则消息损失权重越高，从而在静态帧保持视觉质量、在动态帧增强水印嵌入强度。

### 与基线方法的本质差异

与现有 3DGS 水印方法（如 **GuardSplat** (Chen et al., CVPR 2025)、**3D-GSW** (Jang et al., CVPR 2025)、**GaussianMarker** (Huang et al., NeurIPS 2024)）相比，Mark4D 的根本区别在于三点：其一，解码器工作在 X-CLIP 的视频-文本潜在空间而非像素空间，天然抗像素级失真；其二，水印嵌入仅通过位置和 SH 系数的轨迹对齐偏移实现，而非直接微调所有高斯参数；其三，引入运动自适应损失加权替代均匀加权，解决了动态场景中不同运动幅度对水印嵌入的矛盾需求。这些设计共同解决了将 3DGS 水印直接迁移到 4DGS 时面临的几何保真度损失和时间不一致问题。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Mark4D_Temporally/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the 4DGS watermarking scenario. An owner (Alice) embeds a message key into a trained 4DGS model and releases it online. Even if a malicious user (Bob) distorts the BobRender Mmodel or its rendered videos to assert false ownership, our method Bob (Owner) Trained 4DGS Message Key Watermarked 4DGS ssguarantees embedded message recovery for verification*



Mark4D 的核心设计围绕三个关键模块展开：**潜在空间消息解码器**、**轨迹对齐偏移嵌入**和**运动自适应损失加权**。以下逐一阐述其公式化定义与作用机理。

### 水印嵌入的参数化形式

给定预训练的 4DGS 模型 $\mathcal{G}(t) = \{ \mathbf{x}_i(t), h_i(t), \alpha_i(t), \Sigma_i(t) \}_{i=1}^{N_{\mathcal{G}}}$，其中 $\mathbf{x}_i(t)$ 为第 $i$ 个高斯在时刻 $t$ 的位置，$h_i(t)$ 为球谐系数。Mark4D 通过引入可学习的**位置偏移** $\varepsilon_i(t)$ 和**外观偏移** $\delta_i(t)$ 来嵌入水印，得到带水印的高斯集：

$$
\tilde{\mathcal{G}}(t) = \{ \mathbf{x}_i(t) + \varepsilon_i(t),\; h_i(t) + \delta_i(t),\; \alpha_i(t),\; \Sigma_i(t) \}_{i=1}^{N_{\mathcal{G}}} \tag{6}
$$

选择仅对位置和 SH 系数施加偏移，而非微调全部高斯参数，是为了在嵌入容量与几何保真度之间取得平衡——位置偏移直接控制高斯在空间中的位移，SH 系数偏移调节颜色外观，而透明度 $\alpha_i(t)$ 和协方差 $\Sigma_i(t)$ 保持冻结以维持原始场景结构。

### X-CLIP 潜在空间消息解码器

区别于现有 3DGS 水印方法在像素域进行消息恢复，Mark4D 将解码过程迁移到 X-CLIP 的视频-文本联合潜在空间。具体而言，第一阶段先训练一个消息解码器 $\mathcal{D}_M$（3 层 MLP），使其从冻结的 X-CLIP 文本编码器 $\mathcal{E}_W$ 编码的文本嵌入中重建任意 $L$ 位二进制消息 $M$，优化目标为二元交叉熵损失：

$$
\mathcal{L}_{\mathrm{msg}} = -\sum_{i=1}^{L} \left[ m_i \log \hat{m}_i + (1 - m_i) \log (1 - \hat{m}_i) \right] \tag{10}
$$

在嵌入阶段，冻结的 X-CLIP 视频编码器 $\mathcal{E}_V$ 从渲染序列 $\hat{I}_{\mathcal{S}_t}$ 中提取潜在表示，再由冻结的 $\mathcal{D}_M$ 解码出水印消息：

$$
\hat{M} = \mathcal{D}_M \left( \mathcal{E}_V ( \hat{I}_{\mathcal{S}_t} ) \right) \tag{11}
$$

这一设计的核心优势在于：潜在空间对像素级失真（如 JPEG 压缩、H.264 编码）具有天然鲁棒性，避免了直接在像素域优化导致的可见伪影。

### 轨迹对齐损失

直接对位置施加无约束偏移会破坏高斯的运动连续性，导致渲染结果出现几何不一致。Mark4D 引入**轨迹对齐损失** $\mathcal{L}_{\mathrm{align}}$，约束位置偏移 $\varepsilon_i(\tau)$ 的方向与高斯自身运动切向 $\mathbf{d}_i(\tau)$ 保持一致：

$$
\mathcal{L}_{\mathrm{align}} = \frac{1}{N_{\mathcal{G}} T} \sum_{\tau \in S_t} \sum_{i=1}^{N_{\mathcal{G}}} \left( 1 - \frac{\varepsilon_i(\tau) \cdot \mathbf{d}_i(\tau)}{\|\varepsilon_i(\tau)\|_2 \|\mathbf{d}_i(\tau)\|_2} \right) \tag{14}
$$

其中 $\mathbf{d}_i(\tau)$ 由相邻时刻的位置差分 $\mathbf{x}_i(\tau+\Delta t) - \mathbf{x}_i(\tau)$ 定义。该损失最小化偏移向量与运动切向的余弦距离，使水印嵌入沿高斯运动路径平滑演化，从而保持几何保真度和时间一致性。

### 运动自适应损失加权

不同时间窗口的运动幅度差异显著——合成数据集（如 D-NeRF）运动相对受控，而真实场景（如 DyNeRF）运动分布更广（见 Figure 2）。若对所有帧均匀施加消息损失，静态帧易过拟合导致视觉质量下降，动态帧则水印嵌入不足。Mark4D 提出**运动自适应权重** $\lambda_{S_t}$：

首先计算时间窗口 $S_t$ 内所有高斯的平均运动幅度：

$$
v_{S_t} = \frac{1}{N_{\mathcal{G}} T} \sum_{\tau \in S_t} \sum_{i=1}^{N_{\mathcal{G}}} \| \mathbf{x}_i(\tau+\Delta t) - \mathbf{x}_i(\tau) \|_2 \tag{15}
$$

经全局归一化得到 $\beta_{S_t} \in [0, 1]$，再通过线性插值产生自适应权重：

$$
\lambda_{S_t} = (1 - \beta_{S_t}) \lambda_{\min} + \beta_{S_t} \lambda_{\max} \tag{18}
$$

其中 $\lambda_{\min}$ 和 $\lambda_{\max}$ 为预设的超参数。运动越剧烈的窗口，$\beta_{S_t}$ 越接近 1，$\lambda_{S_t}$ 越接近 $\lambda_{\max}$，从而增强水印监督强度；反之在静止帧降低权重以优先保证重建质量。

### 可微失真模块与总损失

为增强水印对实际传输中各种扭曲的鲁棒性，嵌入阶段引入可微失真模块 $\mathcal{A}$，同时施加帧级失真（如 JPEG 压缩、高斯噪声）和视频级失真（如 H.264 编码）。带失真的解码流程为：

$$
\hat{M} = \mathcal{D}_M \left( \mathcal{E}_V \left( \mathcal{A}( \hat{I}_{\mathcal{S}_t} ) \right) \right) \tag{19}
$$

最终总损失函数综合三项优化目标：

$$
\mathcal{L}_{\mathrm{total}} = \lambda_{S_t} \mathcal{L}_{\mathrm{msg}} + \lambda_{\mathrm{recon}} \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{align}} \mathcal{L}_{\mathrm{align}} \tag{21}
$$

其中 $\mathcal{L}_{\mathrm{recon}}$ 为结合 L1 和 LPIPS 的重建损失，$\lambda_{\mathrm{recon}}$ 和 $\lambda_{\mathrm{align}}$ 为固定权重。$\lambda_{S_t}$ 的动态调节机制使得模型能自适应地在视觉保真度与水印鲁棒性之间分配优化资源。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Mark4D_Temporally/figures/007_Figure_5.jpg]]
*Figure 5: Visualizations of the effects of*



## 实验与关键发现

### 核心瓶颈与验证逻辑

Mark4D的评估围绕一个核心矛盾展开：**在动态4DGS中嵌入水印时，如何同时维持高比特准确率（Bit Acc）与视觉保真度（PSNR/SSIM/LPIPS）**。现有3DGS水印方法（如**GuardSplat** (Chen et al., CVPR 2025)、**3D-GSW** (Jang et al., CVPR 2025)、**GaussianMarker** (Huang et al., NeurIPS 2024)）直接应用于动态场景时，面临高斯体连续时空变形导致的几何保真度损失和时间不一致问题。Mark4D通过三个因果调节变量——X-CLIP潜在空间解码、轨迹对齐偏移、运动自适应损失加权——来解耦这一矛盾。实验设计围绕这三个变量展开：主结果验证整体有效性，消融实验逐一拆解各模块的贡献，鲁棒性测试检验解码器在失真条件下的稳定性。

### 主结果：容量-保真度权衡的突破

Table 1展示了D-NeRF和DyNeRF两个数据集上的平均定量结果。在32位帧级解码配置下，Mark4D取得了**96.34%的比特准确率**和**42.32 dB的PSNR**，相比最强基线GuardSplat分别提升+8.01个百分点和+3.63 dB。这一提升在更高容量设置下更为显著：在64位配置下，Mark4D相比3D-GSW的比特准确率提升+9.35个百分点，PSNR提升+10.40 dB——这验证了核心洞察：**在潜在空间而非像素空间恢复水印，能从根本上解耦容量与视觉质量的冲突**。

值得注意的是，Mark4D在视频级解码（96.96% Bit Acc）与帧级解码（96.34% Bit Acc）之间保持了高度一致性，而GuardSplat和3D-GSW的视频级解码准确率显著低于帧级（分别约为88.33%和更低），说明X-CLIP视频编码器对时序信息的聚合能力有效提升了时间一致性。

Table 1的SSIM和LPIPS指标进一步佐证了不可见性：Mark4D在32位配置下达到0.9960 SSIM和0.0018 LPIPS，与原始4DGS渲染结果几乎无感知差异。定性可视化（Figure 4）中，Mark4D的差异图（×10放大）几乎不可见纹理或结构痕迹，而GuardSplat和3D-GSW在火焰边缘和高频区域出现明显的嵌入伪影。

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Mark4D_Temporally/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparisons. Visualization of rendered results at 48 bits on the DyNeRF dataset (Top: flame salmon, Bottom: flame steak). For each baseline, the top left shows the full rendered view, the top right shows the difference map (magnified by ×10) against the ground truth, and the bottom panels display zoomed regions marked with yellow and red boxes for detailed comparison*

### 消融实验：三个因果变量的独立贡献

**轨迹对齐损失 L_align 的因果效应**（Table 3）：移除L_align后，PSNR从42.32 dB降至约39.50 dB，Bit Acc从96.34%降至约93.10%。Figure 5的可视化揭示了退化机制：无L_align时，高斯位置偏移方向与运动轨迹切向不一致，导致渲染表面出现几何抖动和不连续，尤其在物体边界和快速运动区域。L_align通过最小化偏移与局部运动切向的余弦距离（Eq. (14)），强制水印嵌入沿运动路径平滑演化，从而将几何保真度损失控制在可忽略范围。

**偏移类型的选择**（Table 3）：仅使用外观偏移δ_i(t)（即仅修改球谐系数）而移除空间偏移ε_i(t)时，Bit Acc大幅下降（约-8个百分点），且Figure 5显示渲染结果出现明显颜色偏移。这揭示了容量瓶颈：SH系数的可学习自由度不足以承载高容量水印消息，而位置偏移提供了额外的嵌入空间。同时使用ε_i(t)和δ_i(t)的组合实现了容量与不可见性的最优平衡。

**运动自适应损失加权的场景依赖性**（Table 4）：在运动分布更广的DyNeRF数据集上，启用λ_{S_t}带来的提升（Bit Acc +3.14，PSNR +2.18）显著大于运动相对受控的D-NeRF数据集（Bit Acc +1.02，PSNR +0.89）。这与Figure 2的运动幅度分布分析一致：DyNeRF场景中高斯平均运动幅度覆盖更宽的范围，静态帧与动态帧之间的监督需求差异更大，自适应加权策略的价值因此更突出。Figure 6进一步验证了时间稳定性：启用λ_{S_t}后，各视频片段的Bit Acc和PSNR随时间的变化曲线趋于平坦，消除了无自适应加权时出现的周期性大幅波动。

### 鲁棒性：潜在空间解码的抗失真优势

Table 2展示了32位配置下对各种失真的鲁棒性。Mark4D在JPEG压缩（质量因子50）、H.264视频编码、高斯模糊、随机裁剪等失真下均保持90%以上的比特准确率，显著优于所有基线。关键机制在于：X-CLIP视频编码器在预训练阶段已学习了对常见图像退化的不变性，消息解码器D_M在潜在空间而非像素空间操作，因此对渲染输出的像素级扰动天然不敏感。可微失真模块A在嵌入阶段施加帧级和视频级失真（Eq. (19)），进一步增强了模型对特定失真类型的对抗鲁棒性。

**基线对比揭示的架构差异**：VideoSeal（Fernandez et al., arXiv 2024）作为视频水印方法，在帧级解码上表现尚可，但缺乏对4DGS几何结构的建模；GuardSplat和3D-GSW虽针对3DGS设计，但其像素域解码器在动态场景中鲁棒性显著下降，尤其在H.264压缩下比特准确率降至70%以下。

### 失败模式与局限性

尽管Mark4D在整体指标上表现优异，但分析揭示了若干边界条件：

1. **极端非刚性运动的几何退化**：当场景中存在拓扑变化（如物体分裂、融合）时，轨迹对齐的线性近似（Eq. (14)）可能不足以约束高斯偏移，导致局部几何失真。当前实验数据集（D-NeRF、DyNeRF）的运动模式相对规整，这一失败模式在更复杂的4D场景中可能更显著。

2. **容量上限约束**：仅对位置和SH系数施加偏移限制了可嵌入的最大比特数。当消息长度超过64位时，Bit Acc可能出现饱和或下降，因为可学习参数的自由度已接近信息容量的理论上限。

3. **X-CLIP编码器的依赖性**：解码器性能依赖于ViT-B-32架构的X-CLIP模型。若替换为其他视觉编码器（如ViT-L-14），需要重新训练D_M，且鲁棒性特性可能改变。这一耦合限制了方法的即插即用性。

4. **运动自适应超参数的手工性**：λ_min和λ_max需要根据数据集的运动分布手工设定。在未见过的场景或运动模式下，不恰当的参数选择可能导致静态帧过拟合或动态帧嵌入不足。

### 实验公平性说明

所有方法在相同的预训练4DGS模型上微调，使用相同的水印消息容量（32/48/64位），并在相同的数据集划分上评估。Mark4D未使用额外的训练数据或更大的模型容量，其性能提升完全归因于方法设计的三个创新模块，而非计算资源的倾斜。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Mark4D_Temporally/figures/004_Table_1.jpg]]
*Table 1: Quantitative results. Results are averaged over D-NeRF and DyNeRF datasets. Results marked with “–” indicate configurations that are not supported by the corresponding baseline. (Bold: best result, Underlined: second-best)*

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Mark4D_Temporally/figures/010_Table_3.jpg]]
*Table 3: Ablation study on offset types and loss terms. Results are averaged over D-NeRF and DyNeRF datasets*

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Mark4D_Temporally/figures/008_Table_4.jpg]]
*Table 4: Ablation study on motion-adaptive loss weighting across datasets featuring different motion magnitude distributions*

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Mark4D_Temporally/figures/005_Table_2.jpg]]
*Table 2: Quantitative results under various types of distortions at L = 32 bits. Results are averaged over D-NeRF and DyNeRF datasets. Results marked with “–” indicate methods that do not support video-level decoding*

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Mark4D_Temporally/figures/009_Figure_6.jpg]]
*Figure 6: Effect of*

![[assets/figures/papers/paper_list_l31_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Mark4D_Temporally/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of the distributions of average motion magnitude of Gaussians over time in pretrained 4DGS models on D-NeRF (lego) and DyNeRF (flame salmon) scenes. The x-axis indicates the average motion magnitude normalized to range [0, 1] using the global maximum across both datasets, and the y-axis represents its occurrence frequency*



## 定位与知识库关联

### 与现有3DGS水印方法的区别

Mark4D 直接回应了将静态3DGS水印方法迁移到动态4DGS时所暴露的核心瓶颈：高斯体的连续时空变形破坏了静态方法所依赖的几何稳定性假设，导致不可见性下降和时间不一致。与现有3DGS水印方法的本质区别体现在三个关键设计维度：

**解码空间的迁移**。现有方法如 **GuardSplat**（Chen et al., CVPR 2025）、**3D-GSW**（Jang et al., CVPR 2025）和 **GaussianMarker**（Huang et al., NeurIPS 2024）均在像素域进行水印恢复，这使它们对渲染视角变化和像素级失真敏感。Mark4D 将解码器移至 X-CLIP 的视频-文本联合潜在空间，利用语义级表示天然抵抗像素扰动。这一选择并非简单的编码器替换——它使得水印嵌入与视觉感知解耦，从而在动态场景中维持不可见性的同时获得更强的鲁棒性。

**嵌入参数的选择与约束**。3D-GSW 和 GaussianMarker 通过微调高斯参数子集嵌入水印，但未对动态场景中的参数变化施加时空一致性约束。Mark4D 仅对位置和球谐系数施加可学习偏移，并引入轨迹对齐损失约束位置偏移方向与高斯运动切向一致。这一设计将水印嵌入从“静态参数扰动”转变为“沿运动轨迹的平滑调制”，直接解决了动态场景中几何保真度损失的问题。

**监督信号的时空自适应**。现有方法对所有帧施加均匀的消息损失权重，忽略了动态场景中运动幅度的时空异质性。Mark4D 的运动自适应损失加权策略根据帧间平均运动幅度动态调节监督强度——静止帧降低权重以避免过拟合，动态帧提高权重以强化嵌入——这是现有3DGS水印方法未曾考虑的维度。

与视频水印方法 **VideoSeal**（Fernandez et al., arXiv 2024）相比，Mark4D 的水印嵌入发生在4DGS模型参数空间而非渲染后的像素序列，这意味着水印与场景表示共生存，即使攻击者改变渲染配置或视角，水印仍可通过重新渲染恢复。

### 适用边界与局限

Mark4D 的适用性受以下边界条件约束：

1. **依赖预训练4DGS模型**。方法建立在已训练的4D高斯溅射模型及其变形场之上，无法从零开始进行水印嵌入。这意味着水印嵌入是后处理步骤，不参与原始场景重建训练，对变形场的质量有直接依赖。

2. **编码器架构耦合**。X-CLIP解码器的性能依赖于特定的ViT-B-32模型架构（潜在空间维度固定为512）。更换视频编码器可能需要重新训练消息解码器，限制了方法的即插即用性。

3. **参数空间容量上限**。仅对位置和球谐系数施加偏移限制了可嵌入的水印容量。对于需要超大容量（如数百比特）的应用场景，可能需要探索更多参数空间（如协方差矩阵或不透明度），但这可能以牺牲不可见性为代价。

4. **极端变形的线性近似失效**。轨迹对齐损失基于位置偏移与运动切向的余弦距离，本质上假设高斯运动在局部时间窗口内是近似线性的。在极端非刚性运动或拓扑变化剧烈的场景中，这一线性近似可能不足以保持几何一致性。

5. **运动自适应权重的超参数敏感性**。自适应权重 $\lambda_{S_t}$ 的设计依赖于手工设定的 $\lambda_{\min}$ 和 $\lambda_{\max}$ 边界值。对于未见过的数据集或运动模式，这些超参数可能需要重新调整以获得最优的视觉质量-水印鲁棒性权衡。

### 开放问题

以下问题在论文中未被充分探索，代表潜在的后续研究方向：

- **跨表示泛化**。Mark4D 的设计深度绑定4D高斯溅射的参数化方式。该方法能否扩展到其他动态场景表示（如基于NeRF的4D模型、三平面表示或隐式变形场），而无需从根本上重新设计嵌入机制？

- **4DGS变体的兼容性**。当前实验基于特定的4DGS实现。在不同的4DGS变体（如使用多分辨率哈希网格、三平面编码或隐式变形场的方法）上，Mark4D 的泛化能力尚未验证。

- **联合攻击的鲁棒性**。论文评估了单一失真类型下的鲁棒性，但实际攻击者可能同时施加多种失真（如JPEG压缩叠加帧裁剪）。对组合攻击的鲁棒性边界尚未被刻画。

- **自适应权重的自动化**。能否通过学习或启发式方法自适应调整 $\lambda_{\min}$ 和 $\lambda_{\max}$，使运动自适应策略对不同场景无需手工超参数调优？这涉及对运动分布与最优权重之间关系的进一步建模。

- **更精细的几何约束**。轨迹对齐损失仅约束位置偏移的方向，未考虑高斯形状或协方差的保持。是否可以用更精细的几何约束（如限制协方差矩阵的形变程度或保持高斯体积）替代或补充现有损失，以进一步提升不可见性？



## 原文 PDF

![[paperPDFs/CVPR_2026/Mark4D_Temporally_Consistent_Watermarking_for_4D_Gaussian_Splatting.pdf]]
