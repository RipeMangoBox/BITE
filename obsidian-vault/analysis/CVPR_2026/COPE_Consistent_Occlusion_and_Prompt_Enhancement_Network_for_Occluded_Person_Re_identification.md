---
title: "COPE: Consistent Occlusion and Prompt Enhancement Network for Occluded Person Re-identification"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/COPE_Consistent_Occlusion_and_Prompt_Enhancement_Network_for_Occluded_Person_Re_identification.pdf
project_link: null
code_link: "https://github.com/Cecoming/COPE"
aliases:
- COPE
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过跨身份一致的遮挡增强和特征对齐（CICO）减少遮挡特征干扰，利用视觉语言提示定位前景并随机背景填充（PBF）增强前景鲁棒性，基于完整性提示的评分修正策略（PSS）利用可靠样本缓解信息丢失。
primary_logic: 强制不同身份在相同遮挡区域的特征一致可以隐式抑制遮挡注意力，视觉语言对齐能准确提取前景区域，而利用提示评分筛选高完整性样本可有效修正遮挡查询的检索相似度。
claims:
- COPE通过跨身份一致性遮挡模块抑制遮挡特征干扰。
- PBF模块利用视觉语言对齐生成前景热力图并进行随机背景填充。
- PSS模块利用提示引导的可靠性分数修正检索相似度。
- CICO和PBF显著减少了注意力中的遮挡干扰，并增强前景关注。
---

# COPE: Consistent Occlusion and Prompt Enhancement Network for Occluded Person Re-identification

> [!tip] 核心洞察
> 强制不同身份在相同遮挡区域的特征一致可以隐式抑制遮挡注意力，视觉语言对齐能准确提取前景区域，而利用提示评分筛选高完整性样本可有效修正遮挡查询的检索相似度。

| 字段 | 内容 |
|------|------|
| 中文题名 | COPE：用于遮挡行人重识别的一致性遮挡与提示增强网络 |
| 英文题名 | COPE: Consistent Occlusion and Prompt Enhancement Network for Occluded Person Re-identification |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Sun_COPE_Consistent_Occlusion_and_Prompt_Enhancement_Network_for_Occluded_Person_CVPR_2026_paper.html) · [Code](https://github.com/Cecoming/COPE) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | COPE |
| Dataset | Occluded-Duke |

> [!tip] 效果简介
> - Occluded-Duke 上，Rank-1 / mAP 82.1 / 75.4 (COPE) vs 76.7 / 72.8 (FPC) (+5.4 / +2.6)。

## 概要

遮挡行人重识别（Occluded Person Re-ID）的核心瓶颈在于**遮挡区域的特征干扰**与**严重遮挡下的信息丢失**。相似遮挡模式易导致错误匹配，而现有数据增强方法未能充分抑制遮挡特征；当可见信息极少时，直接特征匹配变得极为困难。针对上述问题，本文提出**COPE（Consistent Occlusion and Prompt Enhancement Network）**，通过三个关键机制实现突破：

1. **跨身份一致性遮挡（CICO）**：对不同身份施加相同遮挡，并强制遮挡区域的特征一致，从而隐式抑制遮挡注意力，减少遮挡特征干扰。
2. **提示背景填充（PBF）**：利用视觉-语言对齐生成前景热力图，并执行随机背景填充，增强前景特征在不同背景下的鲁棒性。
3. **提示相似度评分（PSS）**：在推理阶段利用提示引导的可靠性分数筛选高完整性中间样本，修正遮挡查询的检索相似度，缓解信息丢失问题。

COPE以**PCL-CLIP**（Li and Gong, arXiv 2023）为基线，在原型对比学习框架基础上引入上述模块，总损失函数扩展为交叉熵损失、原型对比损失、遮挡一致性损失、分割损失、前景对齐损失与相似度评分监督损失的联合优化。

实验表明，COPE在遮挡与整体行人重识别基准上均取得最优性能。在**Occluded-Duke**数据集上，COPE达到**82.1% Rank-1**和**75.4% mAP**，较此前最优方法**FPC**分别提升**+5.4%**和**+2.6%**。消融研究进一步验证：CICO模块带来Rank-1提升4.6%、mAP提升7.6%；PSS模块在CICO+PBF基础上额外贡献Rank-1提升5.3%、mAP提升6.6%。注意力图可视化（Figure 1b, Figure 6）直观展示了CICO与PBF对遮挡干扰的显著抑制效果。

**方法定位**：COPE属于“数据增强+特征对齐+检索修正”的混合范式，区别于纯注意力解耦或姿态引导的方法。其CICO模块通过跨身份特征一致性实现隐式遮挡抑制，PBF模块借助CLIP的视觉-语言先验实现前景定位，PSS模块则以轻量级评分修正替代传统的重排序（re-ranking），在效率与精度之间取得平衡。

**局限性**：PBF模块依赖人类解析标签进行预训练，训练设置与部分不使用额外标注的遮挡Re-ID方法不完全对等；CICO的遮挡形状为预定义高斯形状，对不规则遮挡的泛化能力尚待验证；PSS虽较re-ranking快121秒，但仍引入额外相似度计算，对极低时延场景可能产生影响。



行人重识别（Person Re-Identification, Re-ID）旨在跨非重叠摄像头匹配同一行人的图像，是智能视频监控的核心技术。然而，现实场景中行人常被各种物体（如车辆、广告牌、其他行人）部分遮挡，形成**遮挡行人重识别（Occluded Person Re-ID）**这一更具挑战的子问题。与整体Re-ID不同，遮挡Re-ID面临两个根本性瓶颈：

**1. 遮挡区域的特征干扰**

当不同行人被相似物体遮挡时，遮挡区域的特征会主导匹配过程，导致模型将遮挡模式相似但身份不同的行人错误匹配。如Figure 1(a)所示，基线方法CLIP-REID在相似遮挡下产生了大量错误匹配。现有数据增强方法（如随机擦除）虽然模拟了遮挡，但未显式约束模型抑制遮挡特征，使得模型注意力仍分散在遮挡区域（见Figure 1(b)左侧和中侧注意力图）。

**2. 严重遮挡下的信息丢失**

当遮挡严重时，行人可见区域极小，直接进行特征匹配极为困难。Figure 1(c)展示了一个典型案例：查询图像中行人被严重遮挡，其可见信息不足以直接匹配到正确目标。现有方法缺乏有效机制来利用图库中其他高完整性样本作为“桥梁”进行间接匹配。

**现有方法的缺口**

当前遮挡Re-ID方法主要分为三类：基于人体姿态/解析的方法依赖额外标注且对遮挡敏感；基于特征对齐的方法试图匹配可见区域但计算开销大；基于数据增强的方法（如随机擦除、批次遮挡增强）虽简单但未从根本上解决遮挡特征干扰问题。特别是，**相似遮挡模式导致的错误匹配**和**严重遮挡下的信息缺失**这两个核心问题尚未被统一框架有效解决。

**本文动机**

针对上述瓶颈，本文提出**COPE（Consistent Occlusion and Prompt Enhancement）**网络，核心思路是：

- **通过跨身份一致的遮挡增强与特征对齐，隐式抑制遮挡特征干扰**：强制不同身份在相同遮挡区域的特征趋于一致，使模型学习到“遮挡区域不具身份判别性”的先验，从而将注意力转移到前景行人区域。
- **通过视觉语言提示引导前景定位与背景填充，增强前景鲁棒性**：利用CLIP的视觉语言对齐能力生成前景热力图，并通过随机背景填充迫使模型关注前景特征，减少背景干扰。
- **通过提示引导的完整性评分修正检索相似度，缓解信息丢失**：学习一个轻量级提示分数来度量样本完整性，在推理时利用高完整性中间样本修正遮挡查询的检索结果，实现间接匹配。



## 核心方法与创新机理

COPE 的核心创新围绕遮挡行人重识别中的两个关键瓶颈展开：**遮挡区域的特征干扰**和**严重遮挡下的信息丢失**。与基于原型对比学习的 CLIP ViT 微调基线 **PCL‑CLIP**（Li and Gong, arXiv 2023）相比，COPE 在训练与推理两个阶段引入了三个关键的 changed slots，形成“增强—对齐—修正”的闭环。

### 1. 跨身份一致性遮挡（CICO）：从随机擦除到隐式抑制

基线方法通常仅采用随机擦除或不做专门遮挡增强，无法有效应对相似遮挡模式导致的错误匹配。CICO 模块的核心思路是**强制不同身份在相同遮挡区域的特征一致**，从而隐式地抑制遮挡特征的干扰。

具体而言，CICO 使用一组预定义的高斯形状遮挡掩码，对同一批次中不同身份的图像施加**完全相同的遮挡**，并通过遮挡一致性损失 $\mathcal{L}_{\mathrm{oc}}$ 约束同一遮挡类型下各图像的遮挡区域特征彼此接近：

$$
\mathcal{L}_{\mathrm{oc}} = \sum_{n=1}^{N} \frac{1}{|I_n|^2} \sum_{i,j\in I_n} \left\| F_n^{\mathrm{cico}}(i) - F_n^{\mathrm{cico}}(j) \right\|^2
$$

这一设计的关键洞察在于：当不同身份的行人在相同遮挡位置被强制产生相似特征时，模型无法依赖遮挡区域来区分身份，注意力自然会从前景之外的干扰区域移开。消融实验证实了这一机制的有效性——移除 $\mathcal{L}_{\mathrm{oc}}$ 导致 Rank‑1 下降 2.9%（Table 3），而 CICO 模块整体带来 Rank‑1 +4.6%、mAP +7.6% 的增益（Table 2）。

### 2. 提示背景填充（PBF）：视觉‑语言对齐驱动的前景鲁棒增强

基线方法缺乏对背景干扰的专门处理，当同一行人在不同背景下出现时，特征提取容易受背景噪声影响。PBF 模块的创新在于利用 **CLIP 的视觉‑语言对齐能力**，以可学习的提示词生成前景热力图，并在此基础上执行随机背景填充，迫使模型聚焦于行人前景区域。

PBF 使用一组可学习的 token 与固定类别词 “person” 拼接，通过冻结的 CLIP 文本编码器生成文本特征，再与图像 patch 特征计算相似度，得到前景热力图 $\mathcal{H}$。该热力图由人类解析标签通过分割损失 $\mathcal{L}_{\mathrm{seg}}$ 监督：

$$
\mathcal{L}_{\mathrm{seg}} = \sum_{h}^{H} \sum_{w}^{W} \sum_{j=0}^{1} \mathbb{I}[\hat{\mathcal{H}}^{(x,y)}=j] \log \operatorname{Up}(\mathcal{H})_j^{(h,w)}
$$

在获得可靠的前景定位后，PBF 随机替换背景区域，并以前景对齐损失 $\mathcal{L}_{\mathrm{align}}$ 约束原始图像与背景填充图像的前景特征一致：

$$
\mathcal{L}_{\mathrm{align}} = \left\| \mathbf{GWAP}(\mathcal{H}, f_{\mathrm{pat}}^{\mathrm{src}}) - \mathbf{GWAP}(\mathcal{H}, f_{\mathrm{pat}}^{\mathrm{rbf}}) \right\|^2
$$

移除 $\mathcal{L}_{\mathrm{align}}$ 导致 Rank‑1 下降 1.2%（Table 3），验证了前景一致性约束的必要性。Table 6 的消融进一步表明，基于 CoCoOp 风格的自适应提示热力图优于固定文本提示的方案。

### 3. 提示相似度评分（PSS）：利用完整性提示修正检索相似度

基线方法在推理时直接使用欧氏距离排序，严重遮挡下可见信息极少，直接匹配容易失败。PSS 策略的创新在于**利用训练阶段学到的提示分数（prompt score）作为样本完整性的代理指标**，筛选高完整性样本作为中间参考，对查询‑候选相似度进行修正。

提示分数 $\mathcal{P}$ 通过相似度监督损失 $\mathcal{L}_{\mathrm{sim}}$ 学习逼近实例特征与类中心的余弦相似度：

$$
\mathcal{L}_{\mathrm{sim}} = \left\| \mathcal{P} - \mathcal{S} \right\|^2
$$

推理时，PSS 选取提示分数最高的 $K_1$ 个查询和 $K_2$ 个候选作为可靠参考，重新计算相似度矩阵。与传统的 re‑ranking 方法相比，PSS 在 Occluded‑Duke 上速度快 121 秒，同时 Rank‑1 提升超过 1.0%（Table 7）。在 CICO+PBF 的基础上，PSS 进一步贡献了 +5.3%/+6.6% 的 Rank‑1/mAP 增益（Table 2），表明其在信息严重丢失场景下的关键作用。

### 4. 创新闭环：从损失函数到系统协同

上述三个模块通过联合损失函数形成统一优化目标：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{ce}} + \mathcal{L}_{\mathrm{pcl}} + \mathcal{L}_{\mathrm{oc}} + \mathcal{L}_{\mathrm{seg}} + \mathcal{L}_{\mathrm{align}} + \mathcal{L}_{\mathrm{sim}}
$$

其中 $\mathcal{L}_{\mathrm{ce}}$ 和 $\mathcal{L}_{\mathrm{pcl}}$ 来自基线，$\mathcal{L}_{\mathrm{oc}}$、$\mathcal{L}_{\mathrm{seg}}$、$\mathcal{L}_{\mathrm{align}}$、$\mathcal{L}_{\mathrm{sim}}$ 分别为 CICO 的遮挡一致性约束、PBF 的分割监督与前景对齐、PSS 的提示评分监督。这种“增强—对齐—修正”的三阶段设计使 COPE 在 Occluded‑Duke 上达到 82.1% Rank‑1 和 75.4% mAP（Table 1），显著优于包括 **FPC**（76.7%/72.8%）在内的现有方法。

**值得注意的公平性问题**：PBF 模块的训练依赖人类解析标签，而部分对比方法不使用此类额外标注，训练设置不完全对等；CICO 的遮挡形状为预定义高斯形状，可能无法覆盖所有真实遮挡类型。这些限制在评估创新优势时需纳入考量。



COPE 的整体训练流程围绕三个核心模块构建：**跨身份一致性遮挡（CICO）**、**提示背景填充（PBF）** 和 **提示相似度评分（PSS）**，如 Figure 2 所示。其设计逻辑直接针对遮挡行人重识别中的两大瓶颈——遮挡区域的特征干扰与严重遮挡下的信息丢失。

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/002_Figure_2.jpg]]
*Figure 2: The training of the proposed Consistent Occlusion and Prompt Enhancement (COPE) Network. First, the source image is passed through the Visual Encoder to extract the original image features. Then, data augmentation is applied through the Cross-Identity Consistent Occlusion (CICO) and Prompt Background Filling (PBF) modules, which introduce occlusion and background filling, respectively, to extract corresponding enhanced features. Finally, in the Prompt Similarity Scoring module, the prompt scores are learned based on the similarity between features instances and their corresponding prototypes center*

### 数据流与模块协同

1. **视觉编码与基础特征提取**  
   输入图像首先通过基于 CLIP ViT 的视觉编码器，提取全局特征 $\mathbf{F}_g$ 和 patch 特征 $f_{\mathrm{pat}}$。同时，记忆库维护各类别的原型中心 $\mathcal{K}$，用于后续的原型对比学习。

2. **CICO 模块：抑制遮挡特征干扰**  
   源图像的 patch 特征 $f_{\mathrm{pat}}$ 进入 CICO 模块。该模块从预定义的 $N$ 种高斯形状遮挡掩码中采样，对同一批次内不同身份的图像施加**相同的遮挡**，生成增强后的 patch 特征 $f_{\mathrm{pat}}^{\mathrm{cico}}$。随后，通过遮挡一致性损失 $\mathcal{L}_{\mathrm{oc}}$ 强制不同身份在相同遮挡区域的特征趋于一致。其核心机制在于：当模型被迫使不同身份在相同遮挡位置输出相似特征时，该遮挡区域对身份判别的贡献被隐式削弱，从而将注意力从遮挡物转移到前景人体区域（见 Figure 1(b) 的可视化证据）。

3. **PBF 模块：增强前景鲁棒性**  
   与 CICO 并行，PBF 模块利用可学习提示词 $\{v_1, v_2, v_3, v_4\}$ 与固定词 "person" 拼接，通过冻结的 CLIP 文本编码器生成前景热力图 $\mathcal{H}$。该热力图在人类解析标签的监督下（$\mathcal{L}_{\mathrm{seg}}$）学习定位人体前景区域。基于热力图，PBF 执行随机背景填充——将原始背景替换为随机图像，生成增强后的 patch 特征 $f_{\mathrm{pat}}^{\mathrm{rbf}}$。前景对齐损失 $\mathcal{L}_{\mathrm{align}}$ 进一步约束原始图像与背景填充图像的前景特征一致，迫使模型在多样背景下稳定提取前景表征。

4. **PSS 模块：学习完整性度量**  
   在特征层面，PSS 模块为每个实例学习一个标量提示分数 $\mathcal{P}$，通过 $\mathcal{L}_{\mathrm{sim}}$ 使其逼近实例特征与所属类中心的余弦相似度。这一设计使得提示分数天然反映样本的“完整性”——高遮挡样本因特征偏离类中心而获得低分，完整样本则获得高分。训练阶段，该分数作为辅助监督信号嵌入总损失。

5. **联合优化**  
   最终，所有模块的损失函数统一联合优化：
   $$
   \mathcal{L} = \mathcal{L}_{\mathrm{ce}} + \mathcal{L}_{\mathrm{pcl}} + \mathcal{L}_{\mathrm{oc}} + \mathcal{L}_{\mathrm{seg}} + \mathcal{L}_{\mathrm{align}} + \mathcal{L}_{\mathrm{sim}}
   $$
   其中 $\mathcal{L}_{\mathrm{ce}}$ 为交叉熵损失，$\mathcal{L}_{\mathrm{pcl}}$ 为基于记忆库原型的对比损失。

### 推理阶段的修正策略

推理时，PSS 模块发挥独立的相似度修正作用（Figure 3）。对于遮挡查询图像，其提示分数 $\mathcal{P}$ 较低。PSS 策略利用 $\mathcal{P}$ 从图库中筛选出 $K_1$ 个高完整性样本作为“中间参考”，计算查询与这些参考的相似度，再以参考样本自身的提示分数为权重，对原始检索相似度进行加权修正。最终将修正后的相似度 $S$ 通过 $D' = \frac{1}{S} - 1$ 转换回距离进行排序。这一机制有效缓解了严重遮挡下直接特征匹配不可靠的问题。

### 方法谱系与知识库定位

COPE 建立在 **PCL-CLIP**（Li and Gong, arXiv 2023）的基线框架之上，后者使用原型对比学习微调 CLIP ViT。COPE 的增量贡献在于：

| 改进槽位 | 基线方案 | COPE 方案 |
|---------|---------|----------|
| 遮挡增强与特征约束 | 随机擦除或无 | CICO 模块 + 遮挡一致性损失 $\mathcal{L}_{\mathrm{oc}}$ |
| 背景泛化增强 | 无特定处理 | PBF 模块 + 前景对齐损失 $\mathcal{L}_{\mathrm{align}}$ |
| 推理相似度修正 | 直接欧氏距离排序 | PSS 策略：提示分数筛选中间参考样本修正相似度 |
| 总损失函数 | $\mathcal{L}_{\mathrm{ce}} + \mathcal{L}_{\mathrm{pcl}}$ | 额外引入 $\mathcal{L}_{\mathrm{oc}} + \mathcal{L}_{\mathrm{seg}} + \mathcal{L}_{\mathrm{align}} + \mathcal{L}_{\mathrm{sim}}$ |

该方法在遮挡 Re-ID 领域的位置：相比仅依赖数据增强（如随机擦除、**SPT** 等）或仅做特征对齐（如 **FPC**）的方法，COPE 同时从数据增强策略、特征空间约束和检索后处理三个层面协同解决遮挡问题。其视觉-语言对齐的 PBF 设计也与 **CoCoOp** 等自适应提示方法形成对比（Table 6 的消融表明自适应提示热力图优于固定文本提示）。



### 基线框架与视觉编码器

COPE 以 **PCL-CLIP**（Li and Gong, arXiv 2023）为基线，采用冻结的 CLIP ViT 作为视觉编码器，提取图像的全局特征 $\mathbf{F}_g$ 与 patch 特征 $f_{\text{pat}}$。基线损失由交叉熵损失 $\mathcal{L}_{\text{ce}}$ 与原型对比损失 $\mathcal{L}_{\text{pcl}}$ 组成。原型对比损失利用记忆库 $\mathcal{K}$ 中维护的类别原型进行计算：

$$
\mathcal{L}_{\mathrm{pcl}} = -\log \frac{\exp\bigl( s(\mathcal{K}[i],\mathbf{F}_g[i]) / \tau \bigr)}{\sum_{j=1}^{C}\exp\bigl( s(\mathcal{K}[j],\mathbf{F}_g[i]) / \tau \bigr)}
$$

其中 $s(\cdot,\cdot)$ 为余弦相似度，$\tau$ 为温度系数，$C$ 为类别数，$\mathcal{K}[i]$ 为第 $i$ 类的原型向量。记忆库在训练过程中以动量方式更新，为后续提示评分模块提供类中心参考。

### 跨身份一致性遮挡模块（CICO）

CICO 模块解决的核心瓶颈是：相似遮挡模式导致不同身份的行人图像被错误匹配，根源在于遮挡区域的特征在特征空间中形成干扰信号。其设计机理是：若强制不同身份在**相同遮挡区域**产生一致的特征表达，网络将隐式学习忽略遮挡区域，转而关注有判别力的前景区域。

具体而言，CICO 预定义 $N$ 种遮挡类型，每种类型对应一个高斯形状的二值遮挡掩码 $\mathcal{O}_n$。在训练时，同一批次内的图像被随机分配遮挡类型，同一遮挡类型下的图像共享完全相同的掩码。对每张图像，将遮挡掩码作用于 patch 特征，通过全局加权平均池化（GWAP）提取遮挡区域特征：

$$
F_n^{\mathrm{cico}}(i) = \mathrm{GWAP}(\mathcal{O}_n, F_{\mathrm{pat}}^{\mathrm{cico}}) = \frac{\sum_{h}^{fH}\sum_{w}^{fW} \mathcal{O}_n^{(h,w)} \cdot F_{\mathrm{pat}}^{\mathrm{cico}}(h,w)}{\sum_{h}^{fH}\sum_{w}^{fW} \mathcal{O}_n^{(h,w)}}
$$

其中 $F_{\text{pat}}^{\text{cico}}$ 为增强后图像的 patch 特征，$fH$、$fW$ 为特征图尺寸。随后施加遮挡一致性损失，强制同一遮挡类型下所有图像的遮挡区域特征彼此接近：

$$
\mathcal{L}_{\mathrm{oc}} = \sum_{n=1}^{N} \frac{1}{|I_n|^2} \sum_{i,j\in I_n} \left\| F_n^{\mathrm{cico}}(i) - F_n^{\mathrm{cico}}(j) \right\|^2
$$

其中 $I_n$ 表示被分配第 $n$ 种遮挡类型的所有图像索引集合。该损失通过最小化成对均方误差，隐式抑制了网络对遮挡区域的注意力分配——消融实验表明，移除 $\mathcal{L}_{\text{oc}}$ 会导致 Rank-1 下降 2.9%（Table 3），验证了其对遮挡干扰抑制的关键作用。

### 提示背景填充模块（PBF）

PBF 模块的目标是增强前景特征在不同背景下的鲁棒性。其核心思路是利用视觉-语言对齐能力精确定位前景区域，并通过随机背景填充迫使网络关注行人主体而非背景上下文。

**提示热力图生成**：PBF 使用一组可学习 token $\mathbf{v} = \{v_1, v_2, v_3, v_4\}$ 与固定文本 "person" 拼接为 `{v, person}`，输入冻结的 CLIP 文本编码器得到文本特征。该文本特征与视觉 patch 特征计算相似度，经上采样后得到与输入图像等尺寸的前景热力图 $\mathcal{H}$。热力图通过人类解析标签监督的分割损失进行训练：

$$
\mathcal{L}_{\mathrm{seg}} = \sum_{h}^{H} \sum_{w}^{W} \sum_{j=0}^{1} \mathbb{I}[\hat{\mathcal{H}}^{(x,y)}=j] \log \operatorname{Up}(\mathcal{H})_j^{(h,w)}
$$

其中 $\hat{\mathcal{H}}$ 为人类解析标签（前景/背景二值图），$\operatorname{Up}(\cdot)$ 为上采样操作，$H$、$W$ 为图像尺寸。

**随机背景填充与前景对齐**：获得热力图后，PBF 将原始图像的前景区域与随机选取的无关背景图像进行混合，生成背景填充后的增强图像。为抑制背景干扰，对原始图像和填充图像的前景特征施加对齐约束：

$$
\mathcal{L}_{\mathrm{align}} = \left\| \mathbf{GWAP}(\mathcal{H}, f_{\mathrm{pat}}^{\mathrm{src}}) - \mathbf{GWAP}(\mathcal{H}, f_{\mathrm{pat}}^{\mathrm{rbf}}) \right\|^2
$$

其中 $f_{\text{pat}}^{\text{src}}$ 和 $f_{\text{pat}}^{\text{rbf}}$ 分别为原始图像和背景填充图像的 patch 特征，GWAP 以前景热力图 $\mathcal{H}$ 为权重提取前景特征。消融实验显示，移除 $\mathcal{L}_{\text{align}}$ 导致 Rank-1 下降 1.2%（Table 3），证实了前景一致性约束的必要性。

### 提示相似度评分模块（PSS）

PSS 模块在推理阶段运行，用于修正遮挡查询样本的检索相似度，缓解严重遮挡下的信息丢失问题。其核心机制是学习一个**提示分数** $\mathcal{P}$，用于量化样本的完整性/可靠性。

**提示分数学习**：在训练阶段，PSS 模块通过一个小型网络预测每张图像的提示分数，并以实例特征与对应类原型的余弦相似度作为监督信号：

$$
\mathcal{L}_{\mathrm{sim}} = \left\| \mathcal{P} - \mathcal{S} \right\|^2
$$

其中 $\mathcal{S} = s(\mathbf{F}_g, \mathcal{K}[y])$ 为图像全局特征与其类别原型的余弦相似度。该设计使提示分数能够反映样本的完整程度——遮挡越严重，特征与类中心偏离越大，提示分数越低。

**推理时相似度修正**：给定查询图像 $q$，首先计算其与所有图库图像的初始余弦相似度，选取前 $K_1$ 个候选作为中间参考样本。利用这些参考样本的提示分数对查询的相似度进行加权修正，得到最终相似度 $S$，再通过 $D' = \frac{1}{S} - 1$ 转换回距离用于排序。消融实验表明，PSS 在 CICO+PBF 基础上带来 +5.3%/+6.6% 的 Rank-1/mAP 增益（Table 2），且比传统 re-ranking 方法快 121 秒同时 Rank-1 提升超过 1.0%（Table 7）。

### 总训练损失

COPE 的完整训练目标为上述各损失的联合优化：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{ce}} + \mathcal{L}_{\mathrm{pcl}} + \mathcal{L}_{\mathrm{oc}} + \mathcal{L}_{\mathrm{seg}} + \mathcal{L}_{\mathrm{align}} + \mathcal{L}_{\mathrm{sim}}
$$

各损失项分别对应：分类判别（$\mathcal{L}_{\text{ce}}$）、原型对比学习（$\mathcal{L}_{\text{pcl}}$）、遮挡一致性约束（$\mathcal{L}_{\text{oc}}$）、前景分割监督（$\mathcal{L}_{\text{seg}}$）、前景特征对齐（$\mathcal{L}_{\text{align}}$）、提示评分学习（$\mathcal{L}_{\text{sim}}$）。六项损失协同作用，使网络在训练过程中同时获得遮挡鲁棒性、背景不变性和完整性感知能力。

### 补充图表

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/003_Figure_3.jpg]]
*Figure 3: During inference, the Prompt Similarity Scoring module uses prompt scores to further refine final similarity*



## 实验与关键发现

### 主要结果

COPE在遮挡与整体行人重识别基准上均取得最优性能。在核心遮挡数据集**Occluded-Duke**上，COPE达到**Rank-1 82.1%、mAP 75.4%**（Table 1），相比基线方法**FPC**（Rank-1 76.7%、mAP 72.8%）分别提升**+5.4%/+2.6%**。采用重叠滑动窗口设置（步长≤12）的COPE*进一步将性能推至**Rank-1 82.4%、mAP 76.4%**，验证了该方法在严重遮挡场景下的鲁棒性优势。在整体数据集上的表现同样具有竞争力，表明COPE未以牺牲非遮挡场景性能为代价。

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/004_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on occluded and holistic person re-identification benchmarks. Bold and underline indicate optimal and sub-optimal results, respectively. ∗ indicates that the backbone network uses an overlapping sliding window setting with a stride size of 12 or less. † indicates results reproduced by us*

### 消融研究

**模块级消融**（Table 2）揭示了各组件的独立贡献。以基线（仅含交叉熵损失和原型对比损失）为起点，逐一添加模块：

- **CICO模块**带来最显著的增益：Rank-1提升**+4.6%**，mAP提升**+7.6%**。这直接验证了核心洞察——强制不同身份在相同遮挡区域的特征一致性能够有效抑制遮挡特征的干扰。
- **PBF模块**在CICO基础上进一步贡献**+1.2%/+1.5%**的Rank-1/mAP增益，表明视觉-语言对齐生成的前景热力图成功增强了前景特征提取的鲁棒性。
- **PSS模块**在CICO+PBF基础上额外带来**+5.3%/+6.6%**的Rank-1/mAP提升，证明了利用提示评分筛选高完整性参考样本进行相似度修正是缓解严重遮挡信息丢失的有效策略。

**损失函数消融**（Table 3）进一步验证了关键约束的必要性：

- 移除遮挡一致性损失$\mathcal{L}_{\mathrm{oc}}$导致Rank-1下降**2.9%**，证实了该损失对抑制遮挡区域特征干扰的核心作用。
- 移除前景对齐损失$\mathcal{L}_{\mathrm{align}}$使Rank-1下降**1.2%**，验证了原始图像与背景填充图像间前景特征一致性约束的必要性。

### 遮挡增强与提示热力图设计分析

**CICO模块中遮挡增强方法的对比**（Table 5）显示，所提跨身份一致性遮挡策略优于随机擦除等传统增强方法。ViT+CICO在Occluded-Duke上达到Rank-1 67.4%、mAP 57.8%，与**SPT**和**ADM**等专门设计的遮挡增强方法性能相当，但CICO无需复杂的遮挡建模。

**PBF模块中提示热力图来源的消融**（Table 6）表明，基于可学习提示（CoCoOp风格的自适应提示）生成的热力图优于固定文本提示，在Occluded-Duke上达到最优的Rank-1 82.1%、mAP 75.4%。这验证了让模型自适应学习前景描述词对提升前景定位精度的重要性。

### 推理效率与相似度修正策略对比

**PSS与re-ranking的对比**（Table 7）展示了所提策略的效率优势。PSS方法比re-ranking快**121秒**，同时在Rank-1上提升超过**1.0%**。这表明PSS通过提示分数筛选少量高置信度中间样本进行相似度修正，比全局re-ranking更高效且更准确，适合大规模检索场景。

### 超参数敏感性

**CICO模块超参数分析**（Figure 4）考察了遮挡组数量$M$和每组内图像数量$N$的影响。实验表明，适当增加遮挡组数和组内样本数可提升遮挡一致性学习效果，但过大取值会引入计算冗余。**综合超参数敏感性分析**（Table 4）进一步验证了模型对关键超参数在一定范围内具有较好的鲁棒性。

### 可视化分析

**注意力图可视化**（Figure 6）对比了基线方法与COPE在Occluded-Duke测试集上的注意力分布。基线模型在遮挡区域存在明显的注意力分散，而COPE通过CICO和PBF的联合作用，显著减少了对遮挡区域的关注，同时增强了对目标人物前景区域的聚焦。这从可解释性角度印证了CICO模块“隐式抑制遮挡注意力”的核心机制。

**检索排名可视化**（Figure 5）展示了两种典型查询（高完整性和低完整性）在不同模块配置下的检索结果。绿色/红色边框分别表示正确/错误匹配，$P$为提示分数。结果显示，PSS模块能够有效利用提示分数筛选可靠样本，显著提升低完整性查询的检索准确率。

### 公平性说明与失败模式

尽管COPE在多个基准上表现优异，需注意以下限制：

1. **标注依赖**：PBF模块的训练依赖人类解析标签（human parsing labels），而部分对比方法不使用此类额外像素级标注，训练设置不完全对等。
2. **遮挡形状泛化**：CICO模块采用预定义的高斯形状遮挡，可能无法覆盖真实场景中的细长条状或多人物交错遮挡等不规则类型。
3. **推理延迟**：PSS推理虽轻量，但额外引入的相似度计算步骤在严格实时系统中可能产生不可忽略的延迟。
4. **预训练先验优势**：COPE使用CLIP预训练模型，相比传统CNN基线具有海量数据预训练的先验知识优势，在公平性对比上需谨慎解读。

### 补充图表

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/005_Table_2.jpg]]
*Table 2: Ablation study of the proposed components in COPE on Occluded-Duke dataset*

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/008_Table_3.jpg]]
*Table 3: Ablation study of the proposed loss functions in COPE on Occluded-Duke dataset*

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/012_Table_7.jpg]]
*Table 7: Comparison with re-ranking and FPC on Occluded-Duke dataset. † indicates results reproduced by us*

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/006_Table_5.jpg]]
*Table 5: Comparison with other occlusion augmentation methods in CICO module on Occluded-Duke dataset*

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/007_Table_6.jpg]]
*Table 6: Ablation study on the origin of the prompt heatmap in PBF module on Occluded-Duke dataset*

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/010_Table_4.jpg]]
*Table 4: Sensitivity analysis of hyperparameters*

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/011_Figure_5.jpg]]
*Figure 5: Visualization of retrieval rankings for two types of queries under different modules. Green/red borders indicate correct/incorrect matches. P is the prompt score*

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/001_Figure_1.jpg]]
*Figure 1: Existing challenges on Occluded-Duke dataset and our solutions. (a) shows incorrect matches with similar occlusions for CLIP-REID and clean correct matches for our COPE under occlusion interference. (b) shows the attention map of the query with different CICO settings. Without CICO, attention is scattered; with data augmentation, attention on the occlusion decreases; with feature loss, attention on the target person increases. (c) shows the difficult matching problem caused by information loss, which we address by using similar intermediate samples*

![[assets/figures/papers/paper_list_l2299_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_COPE_Consistent_Oc/figures/009_Figure_4.jpg]]
*Figure 4: Sensitivity analysis of hyperparameters M and N in CICO module on Occluded-Duke dataset*



## 定位与知识库关联

### 基线定位：从 PCL-CLIP 到 COPE

COPE 的技术基线是 **PCL-CLIP**（Li and Gong, arXiv 2023），一种基于原型对比学习（Prototype-based Contrastive Learning）的 CLIP ViT 微调方法。PCL-CLIP 的核心训练目标由交叉熵损失 $\mathcal{L}_{\mathrm{ce}}$ 和原型对比损失 $\mathcal{L}_{\mathrm{pcl}}$ 构成，后者利用记忆库（Memory Bank）维护的类别原型进行对比学习：

$$\mathcal{L}_{\mathrm{pcl}} = -\log \frac{\exp\bigl( s(\mathcal{K}[i],\mathbf{F}_g[i]) / \tau \bigr)}{\sum_{j=1}^{C}\exp\bigl( s(\mathcal{K}[j],\mathbf{F}_g[i]) / \tau \bigr)}$$

COPE 在此基线之上进行了四个关键槽位的替换与扩展：

| 方法槽位 | 基线值（PCL-CLIP） | COPE 方案 | 证据来源 |
|---------|-------------------|----------|---------|
| 遮挡增强与特征约束 | 仅随机擦除或无 | 跨身份一致性遮挡（CICO）模块 + $\mathcal{L}_{\mathrm{oc}}$ | Section 3.2 |
| 背景泛化增强 | 无特定背景处理 | 提示背景填充（PBF）模块 + $\mathcal{L}_{\mathrm{align}}$ | Section 3.3 |
| 推理相似度修正 | 直接欧氏距离排序 | 提示相似度评分（PSS）策略 | Section 3.4 & 3.5 |
| 总损失函数 | $\mathcal{L}_{\mathrm{ce}} + \mathcal{L}_{\mathrm{pcl}}$ | $\mathcal{L} = \mathcal{L}_{\mathrm{ce}} + \mathcal{L}_{\mathrm{pcl}} + \mathcal{L}_{\mathrm{oc}} + \mathcal{L}_{\mathrm{seg}} + \mathcal{L}_{\mathrm{align}} + \mathcal{L}_{\mathrm{sim}}$ | Section 3.6 |

### 与现有遮挡重识别方法的关系

COPE 的 CICO 模块与现有遮挡增强方法（如 SPT、ADM）在 Occluded-Duke 上进行了直接对比（Table 5）。在相同 ViT 骨干下，ViT+CICO 达到 Rank-1 67.4% / mAP 57.8%，与 SPT 和 ADM 性能可比，验证了跨身份一致性遮挡策略的有效性。

PBF 模块的核心创新在于利用视觉-语言对齐生成前景热力图。消融实验（Table 6）表明，基于 CoCoOp 的自适应提示热力图（Index-3: 82.1% / 75.4%）优于固定文本提示方案，证实了可学习提示在行人前景定位中的优势。需注意，PBF 的训练依赖人类解析标签（human parsing labels）进行分割损失 $\mathcal{L}_{\mathrm{seg}}$ 的监督，而部分对比方法不使用此类额外像素级标注，训练设置不完全对等。

PSS 模块提供了一种轻量级的检索相似度修正方案。与传统的 re-ranking 方法相比，PSS 在 Occluded-Duke 上快 121 秒，同时 Rank-1 提升超过 1.0%（Table 7），展示了在推理效率与精度之间的有利权衡。

### 适用边界与局限

1. **遮挡形状的泛化边界**：CICO 模块使用预定义的高斯形状遮挡（M 种遮挡尺度 × N 种遮挡位置），可能无法覆盖真实场景中的长尾遮挡类型，如细长条状遮挡、多人交错遮挡等非高斯形态。该泛化能力的边界需要进一步验证。

2. **标注依赖**：PBF 模块的分割损失 $\mathcal{L}_{\mathrm{seg}}$ 依赖人类解析标签进行前景/背景监督，限制了在无分割标注数据集上的直接应用。当无法获取像素级标注时，提示热力图的质量和后续前景对齐效果可能下降。

3. **预训练知识优势**：模型使用 CLIP 预训练权重，该模型在海量图文数据上训练，相比传统 CNN 基线（如 ResNet-50）具有显著的先验知识优势。在与纯视觉基线的公平性比较上存在一定偏差。

4. **推理延迟**：PSS 推理过程虽轻量，但仍需计算额外的中间参考样本相似度，在严格实时系统中可能引入不可忽略的延迟。超参数 $K_1$ 和 $K_2$ 的选择对不同数据集规模的敏感性也需进一步研究。

### 开放问题

- CICO 模块对非高斯形状遮挡（如线状、多物体组合遮挡）的泛化能力如何？是否需要自适应的遮挡形状生成机制？
- PBF 在前景热力图生成失败时如何影响最终性能？是否需要额外的鲁棒机制来应对视觉-语言对齐失效的场景？
- PSS 的超参数 $K_1$、$K_2$ 对不同数据集规模的敏感性如何？是否存在基于提示分数的自适应选择方案？
- 所提方法在真实监控场景的端到端部署中，能否保持高效的推理速度和稳定性？CLIP 编码器的计算开销在边缘设备上是否构成瓶颈？



## 原文 PDF

![[paperPDFs/CVPR_2026/COPE_Consistent_Occlusion_and_Prompt_Enhancement_Network_for_Occluded_Person_Re_identification.pdf]]
