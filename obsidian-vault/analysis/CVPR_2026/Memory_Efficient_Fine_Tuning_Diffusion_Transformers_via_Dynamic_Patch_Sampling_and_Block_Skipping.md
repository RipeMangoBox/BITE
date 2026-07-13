---
title: Memory-Efficient Fine-Tuning Diffusion Transformers via Dynamic Patch Sampling and Block Skipping
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Memory_Efficient_Fine_Tuning_Diffusion_Transformers_via_Dynamic_Patch_Sampling_and_Block_Skipping.pdf
project_link: null
code_link: "https://github.com/blackforestlabs/flux"
aliases:
- DB
- MEFTDTDPSBS
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 跳过非关键块并重用预计算残差特征，同时使用动态块采样降低训练分辨率，从而直接减少前向/反向内存、参数内存和优化器状态内存。
primary_logic: 中间层块对主体身份保存至关重要；通过交叉注意力掩码识别并保留这些关键块，同时预计算残差特征补偿跳过块的信息损失，实现了与全模型微调相当的性能与显著内存降低。
claims:
- 在中层块上掩码交叉注意力导致主体消失，语义距离最大，表明中层块对主体信息编码至关重要。
- 使用残差特征预计算后，即使跳过50%的块，DINO仍从0.4301恢复至0.7150，训练内存降低71%。
- 动态块采样在FLUX上比简单缩放提升DINO和CLIP-I，并显著降低前向/反向内存。
- 在CustomConcept101上，我们的方法以30%跳过比在SANA上取得最高CLIP-I 0.7826，且训练内存仅3.10 GiB。
---

# Memory-Efficient Fine-Tuning Diffusion Transformers via Dynamic Patch Sampling and Block Skipping

> [!tip] 核心洞察
> 中间层块对主体身份保存至关重要；通过交叉注意力掩码识别并保留这些关键块，同时预计算残差特征补偿跳过块的信息损失，实现了与全模型微调相当的性能与显著内存降低。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于动态块采样和块跳过的扩散变换器高效微调方法 |
| 英文题名 | Memory-Efficient Fine-Tuning Diffusion Transformers via Dynamic Patch Sampling and Block Skipping |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.20755) · [Code](https://github.com/blackforestlabs/flux) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DiT-BlockSkip |
| Dataset | DreamBooth, CustomConcept101, FLUX Training Memory, SANA Training Memory |

> [!tip] 效果简介
> - DreamBooth (30 subjects, FLUX) 上，DINO / CLIP-I / CLIP-T 0.7194 / 0.8036 / 0.3199 (30% skip, 256×256) vs LoRA 0.7324 / 0.8146 / 0.3173 (512×512) (DINO -0.013, CLIP-I -0.011, CLIP-T +0.0026)。
> - DreamBooth (30 subjects, SANA) 上，DINO / CLIP-I / CLIP-T 0.7388 / 0.8043 / 0.3240 (30% skip, 512×512) vs LoRA 0.7374 / 0.8108 / 0.3254 (1024×1024) (DINO +0.0014, CLIP-I -0.0065, CLIP-T -0.0014)。
> - CustomConcept101 (FLUX) 上，DINO / CLIP-I / CLIP-T (50% skip, 256×256) 0.6137 / 0.7513 / 0.3056 vs LoRA 0.6726 / 0.7961 / 0.2937 (512×512) (DINO -0.0589, CLIP-I -0.0448, CLIP-T +0.0119)。

## 概要

扩散变换器（DiT）微调的核心瓶颈在于其巨大的内存消耗——完整的前向/反向传播需要同时保留所有基础模型参数、激活值和优化器状态，而传统参数高效微调方法（PEFT）虽减少了可训练参数量，却仍需通过整个网络反向传播，内存开销依然居高不下。**DiT-BlockSkip** 针对这一瓶颈提出了两条相互协同的优化路径：**动态块采样**在训练阶段根据扩散时间步自适应调整裁剪块大小并缩放至固定低分辨率，从而显著降低前向/反向传播中的激活内存；**块跳过机制**则通过交叉注意力掩码分析识别出对主体身份保存至关重要的中间层块，仅对未跳过块注入LoRA可调参数，同时利用预计算的残差特征补偿跳过块的信息损失，并将跳过块参数从GPU卸载，直接削减参数内存和优化器状态内存。

在方法谱系中，DiT-BlockSkip 区别于 **DreamBooth** 式的全模型微调、**LoRA** 式的全层参数高效微调，以及 **LISA**、**LoRA-FA** 等仅关注优化器内存的PEFT方法。它借鉴了 **HollowedNet** 在U-Net上的层跳过思想，但通过残差特征预计算和基于交叉注意力掩码的关键块识别策略，将其有效适配到DiT架构上，避免了HollowedNet在DiT上因无法识别关键块而导致的性能显著下降。

实验结果表明，在FLUX模型上，DiT-BlockSkip以30%的跳过比和256×256训练分辨率取得了与全分辨率LoRA（512×512）高度接近的主体与文本保真度（DINO 0.7194 vs 0.7324，CLIP-I 0.8036 vs 0.8146），同时训练内存从35.99 GiB降至20.78 GiB；当跳过比提升至50%时，内存进一步降至10.42 GiB，降幅达71%。在SANA模型上，该方法以30%跳过比在CustomConcept101数据集上取得了最高的CLIP-I（0.7826），且训练内存仅3.10 GiB，相比LoRA的8.35 GiB降低62.9%。消融实验证实，动态块采样优于固定缩放，残差特征预计算是块跳过机制有效性的关键使能因素，而跳过中间层块会导致主体身份严重丢失，验证了中层块对个性化信息编码的核心作用。

扩散变换器（Diffusion Transformer, DiT）已成为文生图领域的主流架构，其规模化扩展带来了显著的生成质量提升。然而，当用户希望将预训练DiT个性化微调至特定主体时——例如通过DreamBooth范式注入新概念——内存消耗问题变得极为突出。核心瓶颈在于：微调过程必须保留完整的前向/反向传播计算图和整个基础模型参数。即使采用参数高效微调（PEFT）方法（如LoRA）大幅削减可训练参数量，反向传播仍需流经全部Transformer块，导致激活内存和参数内存开销居高不下。当训练分辨率提升至512×512甚至1024×1024时，这一矛盾进一步激化——在FLUX上，标准LoRA微调需占用约36 GiB GPU内存，严重限制了普通用户的可用性。

现有内存优化策略各自存在明显缺口。**梯度检查点**（Gradient Checkpointing）以计算换内存，但额外的前向重计算显著拖慢训练速度。**LoRA-FA**仅减少优化器状态内存，无法缓解激活内存压力。**LISA**（源于LLM领域）通过逐层随机激活释放内存，但直接迁移至DiT会导致性能退化。**HollowedNet**在U-Net架构上通过层跳过实现内存节约，但其层选择策略无法有效识别DiT中对主体身份至关重要的中间层块，适配后性能下降严重。这些方法的共同局限在于：它们或仅作用于单一内存组分，或缺乏对DiT架构特性的针对性设计，难以在内存效率与个性化保真度之间取得令人满意的平衡。

本文的核心洞察源于一项关键观察：在DiT的交叉注意力层中，**中间层块对主体身份编码起着决定性作用**。当对连续14个中间层块的交叉注意力进行掩码时，生成图像中的主体完全消失，语义距离达到最大（Figure 3）。相比之下，掩码浅层或深层块的影响相对轻微。这一发现揭示了一个因果机制——主体特定信息主要驻留在DiT的中间表示层，而浅层和深层块承载的更多是通用视觉特征或高频细节。基于此，本文提出**DiT-BlockSkip**，通过两个协同机制直击内存瓶颈：**动态块采样**根据扩散时间步自适应调整训练分辨率，同时捕获全局结构与局部细节；**块跳过与残差特征预计算**仅微调关键块，并利用预存储的残差特征补偿跳过块的信息损失，从而在将训练内存降低71%的同时，保持与全模型微调相当的主体保真度。

## 核心方法与创新机理

DiT-BlockSkip 的核心创新在于**从传统“减少可训练参数”转向“直接削减前向/反向传播路径”**，通过两个协同的 *changed slots* 实现 DiT 个性化微调的内存大幅降低，同时保持与全模型微调相当的保真度。

### 1. 动态块采样：低分辨率下的多尺度学习

传统方法（如 LoRA）在固定高分辨率（FLUX 512×512，SANA 1024×1024）上训练，激活内存随分辨率平方增长。DiT-BlockSkip 将训练分辨率固定为低分辨率（256×256 / 512×512），但引入**动态块采样**来弥补细节损失：

- **机制**：根据扩散时间步 $t$ 动态调整裁剪块大小，再缩放至固定低分辨率。块大小函数为：
  $$f(s_{\min}, s_{\max}, t) = s_{\min} + \frac{t}{T} \cdot (s_{\max} - s_{\min}), \quad 0 \leq t \leq T$$
  其中 $s_{\min}$、$s_{\max}$ 为最小/最大块大小，$T$ 为最大时间步（Eq. 1, Sec 3.1）。

- **因果逻辑**：高噪声阶段（$t$ 大）采样大块，学习主体的全局结构；低噪声阶段（$t$ 小）采样小块，学习局部细节。这使低分辨率训练仍能捕获多尺度信息。

- **证据**：在 FLUX 上，动态块采样将 DINO 从固定缩放的 0.7164 提升至 0.7253，CLIP-I 从 0.8044 提升至 0.8099（Table 2）。消融实验进一步表明，“Low-to-High”策略（$t$ 增大时块增大）优于“High-to-Low”和随机采样（Table 11）。

### 2. 块跳过与残差特征预计算：选择性反向传播

传统 PEFT 方法（LoRA、LoRA-FA 等）虽减少可训练参数，但仍需通过完整网络反向传播，导致激活和参数内存居高不下。DiT-BlockSkip 的**块跳过**机制从根本上缩短了反向传播路径：

- **关键块识别**：通过交叉注意力掩码实验发现，**中层块对主体身份编码至关重要**——掩码中层交叉注意力导致主体消失，语义距离最大（Fig. 3(a), Sec 3.2）。基于此，块选择策略以最小化与全注意力参考图像的语义距离之和为目标，优化跳过前 $n^*$ 个和后 $m^*$ 个块：
  $$(n^*, m^*) = \underset{n+m=k}{\arg\min} \sum_{j=1}^{N} \left( D(x_g^{(j)}, \hat{x}_n^{(j)}) + D(x_g^{(j)}, \tilde{x}_m^{(j)}) \right)$$
  其中 $D(x,y)=1-\text{sim}(x,y)$ 为语义距离（Eq. 2, Sec 3.2）。

- **残差特征预计算**：跳过块的信息损失通过预计算残差特征 $\Delta f_{i,i+l} = f_{i+l} - f_i$ 来补偿。微调时，将更新后的输入与预存储残差相加：
  $$f_{i+l}' = f_i' + \Delta f_{i,i+l}$$
  这使跳过的块无需参与反向传播，同时保持信息流动（Eq. 3, Sec 3.2）。

- **内存降低的因果链**：跳过块参数从 GPU 卸载 → 减少参数内存和优化器状态；缩短反向传播路径 → 减少激活内存。在 FLUX 上，50% 跳过比将训练内存从 LoRA 的 35.99 GiB 降至 10.42 GiB（降低约 71%），TFLOPS 从 1.89 降至 0.90（Table 12, Fig. 4）。

- **残差特征的决定性作用**：无残差特征时，50% 跳过导致 DINO 骤降至 0.4301；加入残差特征后恢复至 0.7150（Table 2），定性结果也显示生成质量显著恢复（Fig. 7）。

### 3. 协同效应：1+1>2

动态块采样和块跳过各自独立降低内存（仅动态采样 30.48 GiB，仅块跳过 50% 12.85 GiB），二者结合进一步降至 10.42 GiB（Table 12）。更重要的是，二者在性能上互补：动态采样弥补低分辨率训练的细节损失，块跳过通过保留中层块和残差补偿维持主体身份。在 DreamBooth 上，30% 跳过的 DiT-BlockSkip 取得 DINO 0.7194 / CLIP-I 0.8036，与全分辨率 LoRA（0.7324 / 0.8146）差距极小（Table 1）；在 SANA 上甚至以 30% 跳过比取得 CLIP-I 0.7826，略超 LoRA 的 0.7792（Table 9）。

**与基线的本质差异**：HollowedNet 虽也使用层跳过和残差预计算，但其源于 U-Net，无法有效识别 DiT 中的关键块，导致性能显著下降（Table 2）；LISA、LoRA-FA 等仅减少优化器内存或部分参数，未触及激活内存瓶颈。DiT-BlockSkip 通过**识别并保留关键中层块 + 残差补偿跳过块**，实现了内存与保真度的帕累托改进。

DiT-BlockSkip 的整体 pipeline 由三个核心模块串联构成：**动态块采样（Dynamic Patch Sampling）**、**基于交叉注意力掩码的块选择与残差预计算（Block Selection & Residual Feature Precomputation）**，以及**未跳过块的 LoRA 微调（Fine-Tuning Unskipped Blocks with LoRA）**。图 2 给出了完整的流程示意。

**输入与预处理**。给定一张高分辨率参考图像（如 FLUX 的 512×512 或 SANA 的 1024×1024），动态块采样模块首先根据当前扩散时间步 $t$ 决定裁剪块的大小，然后将裁剪后的块缩放至固定的低分辨率（FLUX 为 256×256，SANA 为 512×512）。这一设计使得模型在高噪声阶段（$t$ 大）学习主体的全局结构，在低噪声阶段（$t$ 小）关注局部细节，而无需改变实际训练分辨率。

**块选择与残差预计算**。在正式微调之前，系统通过交叉注意力掩码实验识别出对主体身份保存至关重要的中间层块。具体地，对于给定的总跳过块数 $k$，通过最小化与全注意力参考图像之间的语义距离之和，自动确定最优的跳过前 $n^*$ 个块和后 $m^*$ 个块（满足 $n^*+m^*=k$）。随后，在预计算阶段，使用冻结的基础模型前向传播一次，提取并存储跳过块段的残差特征 $\Delta f_{i,i+l}=f_{i+l}-f_i$，其中 $f_i$ 和 $f_{i+l}$ 分别为跳过段首尾块的输出特征。这一残差特征编码了被跳过块所处理的信息，将用于后续微调中的特征补偿。

**微调执行**。在训练迭代中，仅对未跳过的中间块注入 LoRA 可调参数，跳过的块参数则从 GPU 卸载以释放内存。对于每个跳过段，将当前更新后的输入 $f_i'$ 与预存储的残差 $\Delta f_{i,i+l}$ 相加，得到 $f_{i+l}'=f_i'+\Delta f_{i,i+l}$ 作为下一块的输入，从而在不进行实际前向/反向传播的情况下补偿跳过块的信息损失。整个网络使用条件流匹配损失进行端到端微调。

**内存降低的因果链路**。该 pipeline 从三个层面压缩训练内存：（1）动态块采样降低前向/反向传播中的激活内存；（2）块跳过通过卸载参数减少参数内存和优化器状态内存；（3）残差预计算使得跳过块无需反向传播，进一步削减激活内存。消融实验表明，仅动态采样将 FLUX 训练内存从 35.99 GiB 降至 30.48 GiB，仅 50% 块跳过降至 12.85 GiB，二者结合进一步降至 10.42 GiB（Table 12），验证了各模块独立且协同的内存削减效果。

![[assets/figures/papers/paper_list_l899_https_arxiv_org_abs_2603_20755/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed method. (a) The dynamic patch sampling applies different patch sizes for each diffusion timestep, enabling the model to learn both global structure and fine-grained details depending on the noise level. Cropped patches of various sizes are resized to the same fixed resolution*

DiT-BlockSkip 围绕两条因果链路降低 DiT 微调的内存瓶颈：**动态块采样**从输入端压缩训练分辨率，**块跳过与残差特征预计算**从模型端削减前向/反向传播中的参数与激活内存。两条链路协同作用，使训练内存在 FLUX 上从 LoRA 的 35.99 GiB 降至 10.42 GiB（50% 跳过比），降幅约 71%。

### 动态块采样

扩散模型在不同时间步对全局结构与局部细节的学习需求不同：高噪声阶段（大 $t$）需要大感受野学习主体轮廓，低噪声阶段（小 $t$）则需要精细纹理。动态块采样据此调整裁剪区域大小，随后统一缩放至固定低分辨率，使模型在低分辨率下同时捕获两类信息。

块大小函数定义为：

$$f(s_{\min}, s_{\max}, t) = s_{\min} + \frac{t}{T} \cdot (s_{\max} - s_{\min}), \quad 0 \leq t \leq T$$

其中 $s_{\min}$、$s_{\max}$ 分别为最小和最大裁剪块边长，$T$ 为最大扩散时间步，$t$ 为当前时间步。随着 $t$ 增大，裁剪块线性增大，再缩放至固定分辨率（如 256×256）送入 DiT。这一“Low-to-High”策略在消融实验中显著优于“High-to-Low”和随机采样，在 FLUX 上将 DINO 从固定缩放的 0.7164 提升至 0.7253，CLIP-I 从 0.8044 提升至 0.8099（Table 2）。

### 关键块识别与跳过选择

并非所有 Transformer 块对主体身份保存同等重要。交叉注意力掩码实验表明：掩码中层块（中间 14 个连续块）导致主体消失、语义距离最大，而掩码浅层或深层块的影响几乎可忽略（Figure 3）。这揭示了中层块是编码主体特异性信息的关键瓶颈。

![[assets/figures/papers/paper_list_l899_https_arxiv_org_abs_2603_20755/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative results and mean semantic distances are reported for LoRA fine-tuned FLUX on the CustomConcept101 dataset [19], evaluated across 30 randomly selected classes. We mask the attention scores from image (query) to text (key) within the joint attention across 14 consecutive blocks. Masking mid-level blocks causes a significant drop in similarity compared to full attention*

基于此，方法将跳过块限定在前 $n$ 个和后 $m$ 个块，保留中间层参与微调。最优跳过对 $(n^*, m^*)$ 通过最小化语义距离之和确定：

$$(n^*, m^*) = \underset{n+m=k}{\arg\min} \sum_{j=1}^{N} \left( D(x_g^{(j)}, \hat{x}_n^{(j)}) + D(x_g^{(j)}, \tilde{x}_m^{(j)}) \right)$$

其中 $k$ 为总跳过块数，$N$ 为用于评估的微调模型数量，$x_g^{(j)}$ 为全注意力参考图像，$\hat{x}_n^{(j)}$ 和 $\tilde{x}_m^{(j)}$ 分别为掩码前 $n$ 个和后 $m$ 个块交叉注意力后的生成图像。语义距离 $D(x, y) = 1 - \text{sim}(x, y)$，$\text{sim}$ 为 DINO 或 CLIP 嵌入的余弦相似度。该优化通过遍历所有满足 $n+m=k$ 的组合完成（Algorithm 1），无需梯度计算。

消融实验验证了该策略的有效性：仅跳过前 50% 的块 DINO 为 0.6651，仅跳过后 50% 则骤降至 0.4808，而本文选择策略达到 0.7150（Table 2），证实中层块不可跳过。

### 残差特征预计算

跳过块虽然减少了可训练参数和激活内存，但直接丢弃其输出会导致严重的信息损失——50% 块跳过且无补偿时 DINO 仅 0.4301（Table 2）。残差特征预计算通过在微调前一次性前向传播，存储跳过块的输入-输出残差 $\Delta f_{i, i+l} = f_{i+l} - f_i$，在微调时将其作为固定偏移量补偿跳过块的信息：

$$f_{i+l}' = f_i' + \Delta f_{i, i+l} = f_i' + (f_{i+l} - f_i)$$

其中 $f_i'$ 为第 $i$ 个未跳过块经 LoRA 更新后的输出，$f_{i+l}'$ 为补偿后的第 $(i+l)$ 个块输入。该操作使反向传播仅需流经未跳过块，跳过块的参数可从 GPU 卸载，残差特征本身不参与梯度计算。加入残差特征后，50% 跳过下的 DINO 从 0.4301 恢复至 0.7150，接近 LoRA 全模型微调水平（Table 2）。

### 微调未跳过块

仅对保留的中间块注入 LoRA 可调参数，使用条件流匹配损失进行微调。预计算残差特征从存储加载并与更新后的特征相加，作为后续块的输入。整个流程中，动态块采样降低前向/反向激活内存，块跳过削减参数内存与优化器状态，残差预计算弥补信息损失——三者协同实现了内存与保真度的 Pareto 改进。

![[assets/figures/papers/paper_list_l899_https_arxiv_org_abs_2603_20755/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative ablation results of (a) dynamic patch sampling and (b) skipped block positions*

## 实验与关键发现

### 主要定量结果

**Table 1** 报告了在 DreamBooth 数据集（30 个主体）上，DiT-BlockSkip 与多种基线的对比。在 FLUX 模型上，30% 跳过比 + 256×256 训练分辨率下，本方法取得 DINO 0.7194、CLIP-I 0.8036、CLIP-T 0.3199，与全分辨率 LoRA（512×512，DINO 0.7324、CLIP-I 0.8146）的差距仅为 DINO -0.013、CLIP-I -0.011，且 CLIP-T 略微领先（+0.0026）。在 SANA 模型上，30% 跳过比 + 512×512 训练分辨率下，DINO 达 0.7388，甚至略超 LoRA（1024×1024，0.7374），CLIP-I 差距仅 -0.0065。这表明 DiT-BlockSkip 在显著降低训练分辨率的前提下，几乎无损地保持了主体保真度和文本对齐能力。

在更大规模的 CustomConcept101 数据集上，**Table 8**（FLUX）和 **Table 9**（SANA）进一步验证了方法的泛化性。FLUX 上 50% 跳过比取得 DINO 0.6137、CLIP-I 0.7513，与 LoRA 的差距有所扩大（DINO -0.0589），但 CLIP-T 反而提升 0.0119。SANA 上 30% 跳过比取得 CLIP-I 0.7826，超越 LoRA 的 0.7792，同时训练内存仅需 3.10 GiB（**Table 7**），相比 LoRA 的 8.35 GiB 降低约 62.9%。

![[assets/figures/papers/paper_list_l899_https_arxiv_org_abs_2603_20755/figures/014_Table_7.jpg]]
*Table 7: Detailed training memory comparison and TFLOPs with baselines based on SANA. Inference resolution is 1024 × 1024*

**Table 3** 的用户偏好调查显示，在主体保真度上，本方法获得 48.3% 的偏好率，接近 LoRA 的 51.7%；在文本保真度上，两者几乎持平（本方法 49.2% vs LoRA 50.8%），说明人眼感知质量与自动指标结论一致。

### 内存与计算效率

**Figure 4** 和 **Table 6** 展示了训练内存与 TFLOPS 的系统对比。在 FLUX 上，LoRA 全分辨率训练需 35.99 GiB，本方法 30% 跳过比降至 20.78 GiB，50% 跳过比进一步降至 10.42 GiB，降幅达 71%。同时，每迭代 TFLOPS 从 LoRA 的 1.90 降至 0.90（50% 跳过比），计算量减半以上。**Table 12** 的消融揭示了两项技术各自的内存贡献：仅动态块采样内存为 30.48 GiB，仅块跳过 50% 内存为 12.85 GiB，二者结合达到最优的 10.42 GiB，证明两项技术独立且协同地降低内存。

### 消融实验

**Table 2** 系统消融了三个核心设计选择：

1. **动态块采样 vs 固定缩放**：在 FLUX 256×256 训练下，采用动态块采样将 DINO 从 0.7164 提升至 0.7253，CLIP-I 从 0.8044 提升至 0.8099。**Figure 6(a)** 的定性结果也显示，动态采样能更好地保留主体细节。**Table 11** 进一步比较了三种采样策略："Low-to-High"（本方法）在 DINO 上以 0.7253 优于 "High-to-Low"（0.7184）和随机采样（0.7201），验证了从高噪声阶段学习全局结构、低噪声阶段学习局部细节的策略有效性。

2. **残差特征预计算**：无残差特征时，50% 块跳过导致 DINO 骤降至 0.4301；加入残差特征后恢复至 0.7150，接近全模型水平。**Figure 7** 的定性对比直观展示了残差特征对保持主体身份的决定性作用——无残差时生成结果几乎丢失主体特征。

3. **跳过块位置选择**：仅跳过前 50% 的块（DINO 0.6651）或后 50% 的块（DINO 0.4808）均远不如本方法基于交叉注意力掩码的最优选择（DINO 0.7150）。**Figure 6(b)** 和 **Figure 9** 的热力图一致表明，中间层块对主体身份编码至关重要，跳过中间块会导致语义距离急剧增大。**Table 4** 列出了在 FLUX 和 SANA 上，分别使用 DINO 和 CLIP-I 编码器时选择的最优跳过索引 (n*, m*)，进一步验证了中层块保留的必要性。

![[assets/figures/papers/paper_list_l899_https_arxiv_org_abs_2603_20755/figures/011_Table_4.jpg]]
*Table 4: Skip indices selected in FLUX and SANA for the CustomConcept101 datasets. Encoder denotes the pre-trained encoder to extract image embedding for semantic distance*

### 与补充基线的对比

**Table 10** 在 SANA 上将本方法与 Partial LoRA（仅微调 50% 层，层选择采用本方法的块选择策略）和 Gradient Checkpointing 进行了对比。Partial LoRA 的 DINO 为 0.7270，低于本方法的 0.7388（30% 跳过比），说明仅减少可调参数而不进行残差补偿无法达到同等性能。Gradient Checkpointing 以时间换空间，内存降低但计算开销增加，而本方法同时降低了内存和 TFLOPS。

### 收敛性与训练时间

**Figure 8** 展示了 LoRA 与本方法在训练迭代过程中的性能变化曲线。本方法在早期迭代中收敛速度略慢于 LoRA，但在 500 次迭代后性能差距显著缩小，最终达到接近 LoRA 的水平。**Figure 10** 分解了训练时间：预计算阶段耗时较短，主要开销来自 I/O 加载残差特征，但总体训练时间仍可控。需要注意的是，预计算残差特征需要额外的 ROM 存储空间，论文建议采用周期性存储策略缓解，但该部分内存未计入训练内存报告。

### 失败模式与局限性

1. **高跳过比下的性能衰减**：当跳过比升至 50% 时，FLUX 上的 DINO 从 0.7194（30%）降至 0.6963，CLIP-I 从 0.8036 降至 0.7877（**Table 1**）。CustomConcept101 上 50% 跳过比的 DINO 衰减更明显（0.6137 vs LoRA 0.6726，**Table 8**），表明极端跳过比下残差补偿无法完全弥补信息损失。

![[assets/figures/papers/paper_list_l899_https_arxiv_org_abs_2603_20755/figures/004_Table_1.jpg]]
*Table 1: Comparison with baselines based on FLUX and SANA. Ratio refers to skip ratio. Resolution denotes the training resolution. Inference resolution is fixed at 1024×1024*

2. **预计算存储开销**：残差特征预计算需要额外 ROM 空间，若每迭代完整存储将造成较大存储负担。论文提出了周期性存储策略，但增加了实现复杂度，且该部分开销在当前报告中未充分量化。

3. **模型架构泛化性**：当前验证仅限于 FLUX 和 SANA 两个 DiT 架构，对其他 DiT 变体（如 PixArt-σ）的适用性有待验证。HollowedNet 从 U-Net 适配至 DiT 后性能显著下降（**Table 1**），暗示块跳过策略对架构特性敏感。

4. **设备端部署未验证**：尽管训练内存大幅降低，实际移动/IoT 设备上的部署可行性尚未演示，ROM 与 VRAM 的协同优化仍是开放问题。

## 定位与知识库关联

### 1. 与参数高效微调（PEFT）方法的关系

DiT-BlockSkip 的核心定位是在扩散变换器（DiT）的个性化微调场景中，以极低的内存代价逼近全参数微调或 LoRA 的性能上界。与传统 PEFT 方法相比，其关键差异在于**不依赖缩减可训练参数数量来降低内存，而是通过结构性跳过和特征补偿直接削减前向/反向传播的计算图规模**。

- **LoRA**：作为本文的性能上界参照，LoRA 仅注入低秩适配器，可训练参数量极小，但反向传播仍需流经全部基础模型层，导致激活内存和参数内存几乎无缩减。在 FLUX 上，LoRA 训练内存达 35.99 GiB（512×512），而 DiT-BlockSkip 在 50% 跳过比下仅需 10.42 GiB（256×256），内存降低约 71%，同时 DINO 仅从 0.7324 降至 0.6963（Table 1 / Table 12）。这表明**内存瓶颈不在可训练参数数量，而在完整计算图的保留**。

- **LoRA-FA**：该方法通过冻结部分投影矩阵降低优化器状态内存，但在 DiT 上仍保留完整前向/反向图，内存收益有限。在 SANA 上，LoRA-FA 的 DINO 仅 0.6268，远低于 DiT-BlockSkip 的 0.7388（Table 1），说明单纯的优化器内存缩减无法补偿层间信息损失。

- **Partial LoRA (50%)**：仅对 50% 的层注入 LoRA（使用本文的块选择策略），在 SANA 上训练内存为 4.14 GiB，DINO 为 0.7107（Table 10）。DiT-BlockSkip 在 50% 跳过比下内存仅 3.10 GiB，DINO 达 0.7308，差距显著。这验证了**跳过块并卸载参数比单纯冻结层更有效地释放内存**。

### 2. 与内存高效微调方法的关系

- **LISA**（层级重要性采样适配，原用于 LLM）：直接迁移到 DiT 时，在 SANA 上 DINO 仅 0.7121，CLIP-I 仅 0.7703（Table 1），性能显著低于 DiT-BlockSkip。原因在于 LISA 的层级采样策略未考虑 DiT 中交叉注意力层的主体信息编码特性，导致关键块可能被错误跳过。

- **HollowedNet**（原用于 U-Net 的层跳过方法）：本文将其适配到 DiT，结合残差特征预计算，但在 FLUX 上 DINO 仅 0.6830，CLIP-I 仅 0.7718（Table 2），远低于 DiT-BlockSkip 的 0.7150 / 0.7952。根本原因在于 HollowedNet 的层选择策略源于 U-Net 的编码器-解码器对称结构，**无法识别 DiT 中关键的中层交叉注意力块**，导致主体身份信息丢失。

- **Gradient Checkpointing**：作为补充基线，在 SANA 上与 Partial LoRA 结合时，训练内存可降至 3.82 GiB，但 DINO 仅 0.7024（Table 10）。DiT-BlockSkip 以更低内存（3.10 GiB）获得更高 DINO（0.7308），说明**特征补偿比激活重计算更高效**。

### 3. 与个性化微调基线的关系

- **Textual Inversion (TI)**：梯度无关的文本嵌入反演方法，在 FLUX 上 DINO 仅 0.5451，CLIP-I 仅 0.6884（Table 1），远低于 DiT-BlockSkip。TI 仅优化文本嵌入空间，无法修改模型对主体视觉特征的编码，本质上是能力受限的方法。

- **DreamBooth**：全参数微调方法，在 FLUX 上 DINO 达 0.7401，CLIP-I 达 0.8133（Table 1），略高于 LoRA 和 DiT-BlockSkip，但训练内存远超所有方法。DiT-BlockSkip 以约 1/3 的内存代价逼近其性能。

### 4. 适用边界与局限

**适用边界**：
- 当前方法在 FLUX 和 SANA 两个 DiT 架构上验证有效，且在不同模型规模（SANA-0.6B 到 1.6B）上保持鲁棒（Table 1 / Table 9）。
- 跳过比在 30%–50% 范围内性能-内存权衡最优；超过 50% 时，即使有残差特征补偿，DINO 和 CLIP-I 仍出现明显下降（Table 2），表明中层关键块的数量存在下限。
- 动态块采样的“Low-to-High”策略（随 t 增大增大块尺寸）优于“High-to-Low”和随机采样（Table 11），说明**高噪声阶段学习全局结构、低噪声阶段学习局部细节的策略与扩散过程的物理特性一致**。

**已声明局限**：
- 残差特征预计算需要额外 ROM 存储空间；若每个迭代存储完整特征，存储开销较大。可采用周期性存储策略缓解，但增加了实现复杂度（原文 limitations）。
- 训练内存报告不包括预计算阶段的部分内存消耗，尽管可通过部分前向传播降低（原文 limitations）。
- 实际移动/IoT 设备部署尚未演示，当前工作聚焦于算法效率验证（原文 limitations）。
- 模型范围限于 FLUX 和 SANA，对其他 DiT 变体（如 PixArt-σ）的泛化性有待验证（原文 limitations）。

### 5. 开放问题

基于本文的分析和方法设计，以下问题尚未解决：

1. **ROM-VRAM 协同优化**：如何协同优化 ROM 存储和 VRAM 使用，以实现在设备端（如手机、边缘设备）的无缝个性化微调？残差特征的存储与加载策略是关键瓶颈。

2. **与其他内存优化技术的组合**：动态块采样和块跳过能否与量化（如 NF4、INT8）、梯度检查点、FlashAttention 等技术进一步结合，实现更低的内存开销？当前方法在 SANA 上已降至 3.10 GiB，但仍高于部分消费级设备的可用内存。

3. **跨架构泛化**：在更多样的 DiT 模型（如 PixArt-σ、SD3）和更多个性化场景（如多主体、风格迁移）下的适用性与鲁棒性如何？中层块的关键性是否在所有 DiT 架构中普遍成立？

4. **关键块识别的自动化**：当前块选择依赖预先的交叉注意力掩码分析和语义距离优化（Eq. 2, Algorithm 1），能否将该过程自动化并适应不同的个性化任务，而无需针对每个新主体或新模型重复分析？这直接关系到方法的实际部署便捷性。

5. **预计算开销的进一步压缩**：残差特征预计算需要完整前向传播一次，能否通过部分前向传播或特征压缩技术进一步降低预计算阶段的内存和时间开销？

## 原文 PDF

![[paperPDFs/CVPR_2026/Memory_Efficient_Fine_Tuning_Diffusion_Transformers_via_Dynamic_Patch_Sampling_and_Block_Skipping.pdf]]
