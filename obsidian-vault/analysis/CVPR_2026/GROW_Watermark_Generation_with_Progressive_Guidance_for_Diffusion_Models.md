---
title: "GROW: Watermark Generation with Progressive Guidance for Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GROW_Watermark_Generation_with_Progressive_Guidance_for_Diffusion_Models.pdf
project_link: null
code_link: null
huggingface_link: "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0"
aliases:
- GGPW
- GROW
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在扩散模型的迭代去噪过程中，通过频率域梯度引导逐步调整预测的干净潜变量，使生成图像自然融合水印信号，从而消除对反演的依赖。
primary_logic: 将水印嵌入从一次性静态“印制”转变为渐进式动态“生长”，利用扩散模型自身的去噪能力协同地将水印编织进图像纹理，同时保留内生性和视觉质量。
claims:
- 初始噪声水印方法提取速度极慢，因为必须进行DDIM反演。
- GROW无需反演，提取速度提升近100倍。
- 渐进式引导至关重要；一次性注入会导致图像质量灾难性下降。
- Extraction Efficiency 上 Time (s/image) = 0.24
---

# GROW: Watermark Generation with Progressive Guidance for Diffusion Models

> [!tip] 核心洞察
> 将水印嵌入从一次性静态“印制”转变为渐进式动态“生长”，利用扩散模型自身的去噪能力协同地将水印编织进图像纹理，同时保留内生性和视觉质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于渐进式引导的扩散模型水印生成 |
| 英文题名 | GROW: Watermark Generation with Progressive Guidance for Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Luo_GROW_Watermark_Generation_with_Progressive_Guidance_for_Diffusion_Models_CVPR_2026_paper.html) · [HuggingFace](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GROW (Generation with progressive Watermarking) |
| Dataset | Extraction Efficiency, MS-COCO |

> [!tip] 效果简介
> - Extraction Efficiency 上，Time (s/image) 0.24 vs >20 (Tree-Ring inversion) (~100x faster)。
> - MS-COCO (Ablation) 上，FID 12.32 vs 157.8 (One-step) (-145.48)；PSNR 27.54 vs 11.36 (One-step) (+16.18)；SSIM 0.85 vs 0.19 (One-step) (+0.66)。

## 概要

扩散模型生成内容的版权保护与溯源面临一个关键瓶颈：现有训练免（training‑free）水印方案，如**Tree‑Ring**（Wen et al., arXiv 2023）、**RingID**（Ci et al., ECCV 2024）和**Gaussian Shading**（Yang et al., CVPR 2024），均将水印嵌入初始噪声，依赖昂贵的DDIM反演进行提取。这一范式导致提取延迟严重（单张图像>20秒），阻碍大规模实时应用。本文提出**GROW**（Generation with progressive Watermarking），一种无需训练的新范式，将水印嵌入从一次性静态“嵌入”转变为渐进式动态“生长”：在扩散模型的迭代去噪过程中，通过频率域梯度引导逐步调整预测的干净潜变量，使水印信号自然融入图像纹理，从而彻底消除对反演的依赖。

核心因果机制在于：利用扩散模型自身的去噪能力，将水印目标定义在潜变量的中频DCT域，并在去噪后期（$t > T \cdot r_{\text{start}}$）施加主动梯度引导，使生成过程协同地将水印“编织”进图像。这一设计不仅保留了内生性与视觉质量，还实现了近乎无开销的提取——直接对VAE编码后的潜变量DCT系数符号进行解码，结合多数投票即可恢复水印比特。

实验表明，GROW在提取速度上较反演方法提升近100倍（0.24 s vs. >20 s，Table 3），同时在MS‑COCO数据集上保持与无 watermark 图像相当的视觉质量（FID=12.32，PSNR=27.54，SSIM=0.85）。消融实验进一步验证了渐进式引导的必要性：若将水印一次性注入最终潜变量，图像质量将灾难性下降（FID=157.8，PSNR=11.36，SSIM=0.19），充分说明“生长”策略是平衡不可感知性与鲁棒性的关键。

扩散模型正以前所未有的速度渗透到创意产业中，但随之而来的深度伪造滥用与版权归属问题使得**内容溯源**成为不可回避的技术需求。数字水印作为溯源的核心手段，其理想形态是在不损害生成质量的前提下，将可验证的身份信息不可见地“缝入”图像纹理之中。

当前主流的扩散模型水印范式可归为两类：**后处理水印**与**初始噪声水印**。后处理方法（如 **DwtDctSvd** (Shih, CRC Press 2017)、**Hidden** (Zhu et al., ECCV 2018)）在生成完成后对图像施加变换，虽实现简单，但水印与生成过程解耦，容易在后续压缩或编辑中丢失。初始噪声水印（如 **Tree-Ring** (Wen et al., arXiv 2023)、**RingID** (Ci et al., ECCV 2024)、**Gaussian Shading** (Yang et al., CVPR 2024)、**WIND** (Arabi et al., arXiv 2024)）则将水印信号注入扩散模型的初始噪声，利用去噪过程的“被动散射”将信号隐式保留在最终图像中。这一范式虽在不可感知性上表现优异，却存在一个**致命瓶颈**：水印提取必须依赖昂贵的DDIM反演过程，将图像逆向映射回初始噪声空间才能解码信号。这一反演步骤的计算开销极大，单张图像提取耗时超过20秒，使其在大规模、实时部署场景中几乎不可用。

更深层地审视，初始噪声水印的根本困境在于**嵌入与提取的时空错配**——水印在生成起点一次性注入，却要在生成终点通过逆向工程恢复。这种“一次性静态印制”的策略使得水印信号在数百步去噪迭代中经历不可控的衰减与畸变，最终只能依靠反演来重建。一个自然的追问是：能否将水印嵌入从生成前的“预设”转变为生成中的“生长”，让扩散模型自身的去噪能力协同地将水印编织进图像纹理？

这正是 **GROW** 的出发点。GROW 将水印嵌入重新定义为**渐进式引导任务**：在扩散模型的迭代去噪过程中，通过频率域梯度引导逐步调整预测的干净潜变量，使水印信号在图像逐步清晰化的同时自然“生长”出来。这一范式转换带来了双重收益——一方面，水印与图像内容在生成过程中深度融合，视觉质量得以保留；另一方面，提取时只需对最终潜变量进行DCT变换并检测系数符号，**彻底消除了对DDIM反演的依赖**，将提取速度提升了近100倍（0.24秒 vs >20秒，Table 3）。

Figure 1 直观对比了两种范式的本质差异：初始噪声水印依赖“被动散射+昂贵反演”，而GROW的渐进式引导实现了“主动生长+无反转提取”。这一从“印制”到“生长”的视角转换，为训练免水印的实用化部署打开了新的可能。

## 核心方法与创新机理

GROW的核心创新在于将扩散模型水印从“被动散射”转变为“主动渐进引导”，从根本上消除了对昂贵DDIM反演的依赖。这一转变通过四个关键槽位的重新设计实现。

**水印嵌入阶段：从初始噪声到去噪过程后期。** 现有训练免水印方法（如**Tree-Ring** (Wen et al., arXiv 2023)、**RingID** (Ci et al., ECCV 2024)、**Gaussian Shading** (Yang et al., CVPR 2024)）在初始噪声中嵌入水印，依赖去噪模型的隐式过滤能力将信号保留到最终图像。这种“被动散射”机制迫使提取时必须通过DDIM反演恢复初始噪声，成为速度瓶颈——Tree-Ring的单张提取时间超过20秒（Table 3）。GROW将嵌入阶段移至去噪过程的后期（$t > T \cdot r_{\text{start}}$），在生成过程中主动干预，使水印自然“生长”进图像纹理。

**提取机制：从DDIM反演到直接潜变量解码。** 这是GROW最关键的效率突破。由于水印在生成过程中已被主动引导嵌入预测的干净潜变量 $\hat{\mathbf{z}}_0$，提取时无需反演：直接将生成图像通过VAE编码回潜变量 $\mathbf{z}_0$，对其DCT系数符号进行解码即可。这一设计使提取时间降至0.24秒，相比Tree-Ring的>20秒实现了近100倍加速（Table 3），消除了大规模实时部署的延迟瓶颈。

**水印信号域：从空间域/初始噪声模式到中频DCT域。** GROW在潜变量的离散余弦变换（DCT）域中选择中频带进行嵌入（Section 4.2.1）。中频带平衡了不可感知性和鲁棒性：低频嵌入易被感知，高频嵌入易被破坏。目标水印信号 $\mathbf{S}$ 定义为：
$$\mathbf{S}(u,v) = \begin{cases} \alpha \cdot (2w_i - 1) & \text{if } \mathbf{M}(u,v) = 1 \\ 0 & \text{otherwise} \end{cases}$$
其中 $\alpha$ 为水印强度，$w_i$ 为比特值，$\mathbf{M}$ 为由密钥生成的随机掩码。这一设计使水印信号在频率域中具有结构化的可解码性。

**集成方式：从被动散射到主动梯度引导。** 这是GROW方法论层面的核心转变。在每个去噪步，GROW计算预测干净潜变量的DCT与目标信号在掩码位置的均方误差：
$$\mathcal{L}_{wm} = || (\mathrm{DCT}(\hat{\mathbf{z}}_0) - \mathbf{S}) \odot \mathbf{M} ||_2^2$$
随后通过梯度下降更新 $\hat{\mathbf{z}}_0$：
$$\hat{\mathbf{z}}_0^{\mathrm{guided}} = \hat{\mathbf{z}}_0 - \eta \nabla_{\hat{\mathbf{z}}_0} \mathcal{L}_{wm}$$
并反推修正后的噪声预测供调度器使用：
$$\mathcal{E}^{\mathrm{guided}} = \frac{1}{\sqrt{1 - \bar{\alpha}_t}} (\mathbf{z}_t - \sqrt{\bar{\alpha}_t} \hat{\mathbf{z}}_0^{\mathrm{guided}})$$

消融实验（Table 4, Figure 6）提供了决定性证据：若将水印一次性注入最终潜变量（而非渐进引导），图像质量灾难性崩溃——FID从GROW的12.32飙升至157.8，PSNR从27.54降至11.36，SSIM从0.85降至0.19。这证明**渐进式引导是GROW有效的必要条件**：扩散模型自身的去噪能力在多个步骤中协同地将水印编织进图像纹理，而一次性注入则粗暴地破坏了潜变量结构。

**方法谱系与知识库定位。** GROW属于训练免水印方法，但与现有工作形成明确分界：初始噪声方法（Tree-Ring、RingID、Gaussian Shading、**WIND** (Arabi et al., arXiv 2024)）依赖反演提取；后处理方法（**DwtDctSvd** (Shih, CRC Press 2017)、**Hidden** (Zhu et al., ECCV 2018)）在生成后添加水印，可能被重生成攻击绕过。GROW通过“渐进式引导”在生成过程中嵌入，兼具训练免的灵活性和无反转的高效性，在方法谱系中开辟了新的技术路径。

**已知局限。** 当前GROW对随机比例拉伸的鲁棒性较弱，水印容量受限于静态DCT频域结构（当前16位）。如何用可学习的、抗攻击的表示空间替代静态DCT域，以提升水印容量和安全性，是值得探索的开放问题。

GROW 将水印嵌入从传统的一次性“静态印制”转变为在扩散模型去噪过程中的“渐进式动态生长”。其整体流程由三条相互协作的管线构成：目标信号生成、渐进式引导嵌入、以及无反转提取。

**目标信号生成。** 首先将秘密消息 $W$ 转换为比特序列 $w$。基于密钥 $K$ 生成一个二值掩码 $\mathbf{M}$，用于指定在潜变量离散余弦变换（DCT）域中嵌入水印的具体位置——这些位置被策略性地选在中频带，以平衡不可感知性与鲁棒性。目标水印信号 $\mathbf{S}$ 在 DCT 域中定义为：

$$\mathbf{S}(u,v) = \begin{cases} \alpha \cdot (2w_i - 1) & \text{if } \mathbf{M}(u,v) = 1 \\ 0 & \text{otherwise} \end{cases}$$

其中 $\alpha$ 为水印强度，$w_i$ 为对应的信息比特。这一信号矩阵是整个引导过程的优化目标。

**渐进式引导嵌入。** 在扩散模型的迭代去噪过程中，对于时间步 $t > T \cdot r_{\text{start}}$（$r_{\text{start}}$ 控制引导开始的阶段，默认 0.5），GROW 在每一步执行以下操作：

1. 从当前噪声潜变量 $\mathbf{z}_t$ 和噪声预测 $\boldsymbol{\mathcal{E}}_{\theta}(\mathbf{z}_t, t, c)$ 估计预测的干净潜变量 $\hat{\mathbf{z}}_0$：
   $$\hat{\mathbf{z}}_0 = \frac{1}{\sqrt{\bar{\alpha}_t}} (\mathbf{z}_t - \sqrt{1 - \bar{\alpha}_t} \boldsymbol{\mathcal{E}}_{\theta}(\mathbf{z}_t, t, c))$$

2. 对 $\hat{\mathbf{z}}_0$ 进行 DCT 变换，计算其与目标信号 $\mathbf{S}$ 在掩码 $\mathbf{M}$ 指定位置上的均方误差作为水印损失：
   $$\mathcal{L}_{wm} = || (\mathrm{DCT}(\hat{\mathbf{z}}_0) - \mathbf{S}) \odot \mathbf{M} ||_2^2$$

3. 通过梯度下降单步更新预测干净潜变量，使其 DCT 系数向目标水印信号靠拢：
   $$\hat{\mathbf{z}}_0^{\mathrm{guided}} = \hat{\mathbf{z}}_0 - \eta \nabla_{\hat{\mathbf{z}}_0} \mathcal{L}_{wm}$$
   其中 $\eta$ 为引导尺度。

4. 从引导后的干净潜变量反推修正后的噪声预测，交还给调度器以继续去噪：
   $$\mathcal{E}^{\mathrm{guided}} = \frac{1}{\sqrt{1 - \bar{\alpha}_t}} (\mathbf{z}_t - \sqrt{\bar{\alpha}_t} \hat{\mathbf{z}}_0^{\mathrm{guided}})$$

这一渐进式引导机制是 GROW 的核心创新。消融实验（Table 4, Figure 6）给出了决定性证据：若将所有引导压缩为一次性注入最终潜变量，图像质量会灾难性崩溃（FID=157.8, PSNR=11.36, SSIM=0.19），而 GROW 的渐进式引导将 FID 维持在 12.32，PSNR 达 27.54，SSIM 达 0.85，证明去噪过程本身的协同演化对水印的自然“编织”至关重要。

**无反转提取。** 提取过程完全绕开了 DDIM 反演。将最终图像通过 VAE 编码回潜变量 $\mathbf{z}_0$，进行 DCT 变换后，利用相同的密钥 $K$ 恢复掩码 $\mathbf{M}$，在掩码指定位置检查 DCT 系数的符号：正号解码为“1”，负号解码为“0”。由于每个消息比特被冗余嵌入多次，最终通过多数投票确定每个比特的值，显著增强了提取的鲁棒性。

整个框架的输入输出关系清晰：输入为文本提示 $c$、秘密消息 $W$ 和密钥 $K$；输出为带有水印的图像及其可提取的消息。生成端额外引入的水印开销仅为 0.17 秒，而提取端仅需 0.24 秒——相比依赖 DDIM 反演的初始噪声方法（如 Tree-Ring 需超过 20 秒）实现了近 100 倍的加速（Table 3）。

![[assets/figures/papers/paper_list_l883_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_GROW_Watermark_Gen/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of our proposed method, GROW. (a) Watermark generation: A secret message W is first converted into a bit sequence w. The watermark w is embedded into the target frequency domain at the positions defined by a mask M, which is generated from a secret key K. During the iterative denoising process, we compute a loss between the DCT of the predicted clean latent*

GROW将水印嵌入重新定义为一种**渐进式引导**过程，而非传统的一次性注入。其核心由三个模块串联构成：目标信号生成、渐进式引导嵌入、无反转提取。

### 目标信号生成

水印嵌入在潜空间的中频DCT域进行，以平衡不可感知性与鲁棒性。给定秘密消息 $W$，先转换为比特序列 $\mathbf{w} = \{w_i\}_{i=1}^{L}$，再由密钥 $K$ 生成一个二值掩码 $\mathbf{M}$，指定DCT系数中哪些位置承载水印。每个比特 $w_i$ 在掩码区域内重复嵌入多次，以增强后续提取的容错能力。

目标水印信号 $\mathbf{S}$ 定义为：

$$
\mathbf{S}(u,v) = \begin{cases} \alpha \cdot (2w_i - 1) & \text{if } \mathbf{M}(u,v) = 1 \\ 0 & \text{otherwise} \end{cases}
$$

其中 $\alpha$ 为水印强度，控制嵌入信号的幅度；$(2w_i - 1)$ 将比特 $w_i \in \{0,1\}$ 映射为 $\{-1, +1\}$，使信号在DCT域具有正负极性。

### 渐进式引导嵌入

这是GROW区别于所有现有方法的核心机制。在扩散模型的迭代去噪过程中，对于时间步 $t > T \cdot r_{\text{start}}$（$r_{\text{start}}$ 为引导起始比例，默认0.5），每一步执行以下操作：

**步骤1：估计干净潜变量。** 从当前噪声潜变量 $\mathbf{z}_t$ 和噪声预测网络 $\boldsymbol{\mathcal{E}}_{\theta}$ 出发，计算预测的干净潜变量：

$$
\hat{\mathbf{z}}_0 = \frac{1}{\sqrt{\bar{\alpha}_t}} (\mathbf{z}_t - \sqrt{1 - \bar{\alpha}_t} \boldsymbol{\mathcal{E}}_{\theta}(\mathbf{z}_t, t, c))
$$

**步骤2：计算水印损失。** 对 $\hat{\mathbf{z}}_0$ 进行离散余弦变换（DCT），在掩码 $\mathbf{M}$ 指定的位置上与目标信号 $\mathbf{S}$ 计算均方误差：

$$
\mathcal{L}_{wm} = \| (\mathrm{DCT}(\hat{\mathbf{z}}_0) - \mathbf{S}) \odot \mathbf{M} \|_2^2
$$

**步骤3：梯度引导更新。** 以引导尺度 $\eta$ 沿损失梯度方向调整 $\hat{\mathbf{z}}_0$，使预测的干净潜变量向水印目标靠拢：

$$
\hat{\mathbf{z}}_0^{\mathrm{guided}} = \hat{\mathbf{z}}_0 - \eta \nabla_{\hat{\mathbf{z}}_0} \mathcal{L}_{wm}
$$

**步骤4：修正噪声预测。** 将引导后的干净潜变量反推回噪声预测，供DDIM调度器在下一步使用：

$$
\mathcal{E}^{\mathrm{guided}} = \frac{1}{\sqrt{1 - \bar{\alpha}_t}} (\mathbf{z}_t - \sqrt{\bar{\alpha}_t} \hat{\mathbf{z}}_0^{\mathrm{guided}})
$$

这一机制的关键在于：水印信号并非一次性“印制”到最终潜变量上，而是在多个去噪步骤中**渐进式地“生长”**进图像纹理。扩散模型自身的去噪能力协同地将水印编织进图像结构，从而避免了对视觉质量的灾难性破坏——消融实验证实，一次性潜空间注入会导致FID飙升至157.8、PSNR跌至11.36，而GROW将FID控制在12.32、PSNR维持在27.54。

### 无反转提取

提取过程完全绕开了昂贵的DDIM反演。将待检测图像通过VAE编码器映射回潜空间得到 $\mathbf{z}_0$，对其应用DCT变换获得系数矩阵 $\mathbf{F}$。利用与嵌入阶段相同的密钥 $K$ 生成掩码 $\mathbf{M}$，对每个掩码位置 $(u,v)$ 根据系数符号提取比特：正号解码为“1”，负号解码为“0”。由于每个消息比特在嵌入时被重复多次，提取阶段采用**多数投票**确定每个比特的最终值，显著提升了抗攻击鲁棒性。

整个提取流程仅需单次VAE编码和一次DCT变换，在Tesla T4 GPU上耗时仅0.24秒/图，相比Tree-Ring等依赖DDIM反演的方法（>20秒/图）实现了近100倍的加速。

## 实验与关键发现

### 核心瓶颈与评估逻辑

现有训练免水印方法（如Tree-Ring、RingID、Gaussian Shading、WIND）依赖DDIM反演从生成图像中恢复初始噪声以提取水印，这一过程计算开销极大，形成严重的延迟瓶颈，阻碍大规模实时应用。GROW通过渐进式引导将水印信号“生长”进图像纹理，从而彻底消除对反演的依赖。实验评估围绕三个核心问题展开：（1）不可感知性——水印是否损害图像质量；（2）鲁棒性——水印在各类攻击下能否被正确提取；（3）效率——生成和提取的时间开销是否可接受。

### 实验设置

实验使用Stable Diffusion v2.1-base模型，在MS-COCO和Stable-Diffusion-Prompts两个公开数据集上各生成1,000张图像进行评估。默认超参数设置为：水印强度α=0.5，引导尺度η=100，采样步数50步，引导起始比例r_start=0.5。不可感知性指标包括PSNR、SSIM（越高越好）和FID、LPIPS（越低越好）；鲁棒性以消息准确率M-ACC衡量，攻击类型涵盖旋转、JPEG压缩、随机裁剪、高斯模糊、高斯噪声、亮度调整和对抗攻击Diff-Pure。时间效率在单块Tesla T4 GPU上测量。

### 主要结果

**不可感知性与鲁棒性的平衡。** 在MS-COCO数据集上，GROW在保持图像质量的同时实现了优异的鲁棒性。如Table 1所示，GROW的FID为12.32，PSNR为27.54，SSIM为0.85，平均M-ACC达到97.8%。在Stable-Diffusion-Prompts数据集上，平均M-ACC为97.6%。与后处理方法（DwtDctSvd、Hidden）相比，GROW在视觉质量上具有显著优势；与初始噪声方法（Tree-Ring、RingID）相比，GROW在鲁棒性上保持竞争力，同时避免了反演开销。

**跨模型泛化。** Table 2展示了GROW在不同扩散模型（Stable Diffusion v1-5、v2-1-base、SDXL）上的表现。GROW在所有模型上均保持稳定的不可感知性和鲁棒性，平均M-ACC在96%以上，表明渐进式引导机制对底层去噪模型具有较好的适应性。

**时间效率的质变。** Table 3揭示了GROW最显著的优势：提取时间仅为0.24秒/图，而Tree-Ring等基于反演的方法提取时间超过20秒，速度提升近100倍。GROW的渐进式引导仅增加0.17秒的生成开销，总生成时间仍处于可接受范围。这一效率飞跃使得GROW在实际大规模部署中具有可行性。

### 消融实验

**渐进式引导的必要性。** 这是论文最具决定性的消融证据。若将水印一次性注入最终潜变量再解码，图像质量发生灾难性崩溃：FID飙升至157.8（GROW为12.32），PSNR降至11.36（GROW为27.54），SSIM仅为0.19（GROW为0.85）（Table 4）。Figure 6直观展示了这一对比——一次性注入导致图像出现严重伪影和纹理扭曲，而渐进式引导生成的图像与无水印版本几乎无法区分。这验证了核心洞察：水印必须与去噪过程协同“生长”，而非事后“印制”。

**超参数敏感性。** Figure 5展示了三个关键超参数的权衡曲线：
- **水印强度α**（Figure 5a）：α从0.3增至0.7时，M-ACC从92%提升至99%，但FID从9.5恶化至28.2。α=0.5提供了较好的平衡点。
- **引导尺度η**（Figure 5b）：η从50增至100时，M-ACC从90%提升至99%，图像质量保持稳定，表明梯度引导在合理范围内对视觉质量影响有限。
- **起始比例r_start**（Figure 5c）：控制引导开始的去噪阶段，影响水印嵌入的充分性与图像质量的平衡。r_start=0.5（即后50%的去噪步进行引导）取得了最佳折衷。

### 失败模式与局限性

尽管GROW在多数攻击下表现鲁棒，但论文明确指出其对**随机比例拉伸**（random ratio stretching）的鲁棒性较弱。这一失败模式可能源于DCT域水印的空间频率特性——非均匀缩放会破坏中频系数的符号一致性，而多数投票机制难以补偿这种结构性失真。

此外，当前水印容量受限于静态DCT频域结构（16位），在需要嵌入更多信息的应用场景中可能不足。

### 图表结论摘要

| 图表 | 核心结论 |
|------|----------|
| Table 1 | GROW在不可感知性和鲁棒性上达到或超越现有方法，无需反演 |
| Table 2 | 跨扩散模型泛化良好，平均M-ACC >96% |
| Table 3 | 提取速度提升约100倍（0.24s vs >20s），消除延迟瓶颈 |
| Table 4 | 一次性注入导致FID=157.8，证明渐进式引导不可或缺 |
| Figure 5 | α和η控制鲁棒性-质量权衡，r_start=0.5为最优起始点 |
| Figure 6 | 视觉对比确认渐进式引导避免了一次性注入的灾难性伪影 |

![[assets/figures/papers/paper_list_l883_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_GROW_Watermark_Gen/figures/005_Table_1.jpg]]
*Table 1: Comparison of different watermarking methods across datasets. For imperceptibility metrics (PSNR, SSIM, FID, LPIPS), we report the performance on clean images. For robustness, we report the M-ACC (%) under various attacks. Best results are in bold, second best are underlined*

![[assets/figures/papers/paper_list_l883_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_GROW_Watermark_Gen/figures/010_Table_4.jpg]]
*Table 4: Quantitative comparison of image quality for the progressive guidance ablation study*

![[assets/figures/papers/paper_list_l883_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_GROW_Watermark_Gen/figures/008_Figure_5.jpg]]
*Figure 5: Ablation studies on key hyperparameters. We plot the trade-off between image quality (FID, blue line) and robustness (M-ACC, orange line). (a) Watermark strength α. (b) The guidance scale η. (c) Start Ratio*

![[assets/figures/papers/paper_list_l883_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_GROW_Watermark_Gen/figures/006_Table_2.jpg]]
*Table 2: Comparison of different watermarking methods across diffusion models. For imperceptibility (PSNR, SSIM, FID, LPIPS), we report performance on clean images. For robustness, we report the average Message Accuracy (M-ACC) across all attacks. Best results are in bold, second best are underlined*

![[assets/figures/papers/paper_list_l883_https_openaccess_thecvf_com_content_CVPR2026_html_Luo_GROW_Watermark_Gen/figures/009_Figure_6.jpg]]
*Figure 6: A visual comparison using prompts from the MS-COCO dataset. (a)Non-watermarked image. (b) Watermarked image by GROW. (c) One-step method*

## 定位与知识库关联

### 核心范式转换：从被动散射到主动生长

扩散模型水印技术可沿嵌入阶段和提取机制两个轴进行划分。当前主流范式——**初始噪声水印**——在采样起点的初始噪声中嵌入信号，依赖扩散模型自身的去噪过程将信号“被动散射”至输出图像。代表方法包括 **Tree-Ring**（Wen et al., arXiv 2023）、**RingID**（Ci et al., ECCV 2024）、**Gaussian Shading**（Yang et al., CVPR 2024）和 **WIND**（Arabi et al., arXiv 2024）。这类方法的根本瓶颈在于提取端：必须通过DDIM反演将生成图像逆向映射回初始噪声，单张提取耗时超过20秒（Table 3），构成大规模实时部署的严重延迟障碍。

另一条技术路线是**后处理水印**，即在生成完成后对图像施加传统频域或深度学习水印，如 **DwtDctSvd**（Shih, CRC Press 2017）和 **Hidden**（Zhu et al., ECCV 2018）。这类方法虽无需反演，但水印嵌入与图像生成过程解耦，难以在不可感知性、鲁棒性和生成质量之间取得平衡。

GROW的方法论定位在于**将水印嵌入从一次性静态“印制”转变为渐进式动态“生长”**。这一转变体现在四个关键设计槽位的重构：

| 设计维度 | 初始噪声范式 | GROW |
|---------|------------|------|
| 嵌入阶段 | 初始噪声（t=T） | 去噪后期步骤（t > T·r_start） |
| 提取机制 | DDIM反演恢复初始噪声 | 直接对潜变量DCT系数符号解码 |
| 信号域 | 空间域或初始噪声模式 | 预测干净潜变量的中频DCT域 |
| 集成方式 | 被动散射（去噪隐式过滤） | 主动梯度引导（最小化DCT域MSE） |

### 与基线方法的关系

**对初始噪声方法的超越**：GROW直接回应了Tree-Ring等方法的提取效率瓶颈。通过将水印嵌入从初始噪声移至去噪过程中的预测干净潜变量，GROW使得提取端仅需VAE编码+DCT变换+符号检测，完全消除反演依赖。Table 3显示GROW提取时间仅0.24秒，与Tree-Ring的>20秒形成约100倍加速。

**对后处理方法的改进**：后处理方法在已生成图像上施加水印，容易引入可见伪影或与图像内容冲突。GROW利用扩散模型自身的去噪能力，在生成过程中协同地将水印编织进图像纹理。Figure 4的视觉对比显示，GROW在保持图像自然度的同时实现了水印嵌入。

**渐进式引导的关键性**：最直接的对比来自消融实验中的“一次性潜空间注入”——将水印直接写入最终潜变量后再解码。该基线导致图像质量灾难性崩溃：FID=157.8，PSNR=11.36，SSIM=0.19（Table 4）。这证明了在扩散模型的迭代去噪框架内渐进施加引导是保证视觉质量的前提。

### 适用边界

1. **扩散模型依赖**：GROW设计上绑定于扩散模型的迭代去噪机制，其引导操作依赖于预测干净潜变量这一中间表示。对于非扩散类生成模型（如GAN、自回归模型），该方法无法直接迁移。

2. **频域结构限制**：水印嵌入在固定的中频DCT域，当前容量为16位。这一静态结构限制了水印容量，且对随机比例拉伸（random ratio stretching）的鲁棒性较弱——这是论文明确指出的局限性。

3. **训练免特性**：GROW是训练免方法，不修改扩散模型权重。这意味着其水印强度完全由引导过程中的超参数（α、η、r_start）控制，在极端攻击下可能不如训练嵌入方法鲁棒。

4. **VAE编码器依赖**：提取过程依赖VAE编码器将图像映射回潜变量。若图像经过严重失真导致VAE重建偏差，提取精度会受到影响。

### 局限与开放问题

**已知局限**：
- 对随机比例拉伸的鲁棒性较弱，这与固定DCT频域结构直接相关。
- 水印容量受限于静态DCT掩码设计（当前16位），难以扩展到长消息场景。

**开放问题**：
1. **可学习表示空间**：能否用可学习的、抗攻击的频域或隐空间表示替代静态DCT域？这有望同时提升水印容量、鲁棒性和安全性。
2. **大规模泛化**：当前实验在MS-COCO和Stable-Diffusion-Prompts两个数据集上使用1,000张图像进行，在更大规模、更多样化攻击下的泛化表现尚待验证。
3. **安全性分析**：论文未深入讨论针对GROW的针对性攻击（如对DCT域符号的对抗扰动），这是实际部署前需要填补的空白。
4. **跨模型迁移**：Table 2展示了跨扩散模型的鲁棒性结果，但GROW的引导机制对不同架构（如DiT、U-ViT）的适配性值得进一步探索。

### 知识库定位

GROW在扩散模型水印领域引入了“渐进式引导”这一新范式，填补了训练免方法与免反演提取之间的空白。其核心贡献不在于提出全新的水印编码方案，而在于**重新设计了水印与扩散生成过程的交互时序和机制**——将水印从生成前的静态输入转变为生成中的动态约束。这一思路与扩散模型中的classifier guidance和classifier-free guidance形成方法论呼应，但将其应用目标从语义控制转向了隐式信号嵌入。

## 原文 PDF

![[paperPDFs/CVPR_2026/GROW_Watermark_Generation_with_Progressive_Guidance_for_Diffusion_Models.pdf]]
