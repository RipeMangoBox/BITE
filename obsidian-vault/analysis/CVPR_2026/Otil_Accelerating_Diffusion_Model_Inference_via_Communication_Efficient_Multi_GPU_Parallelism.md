---
title: "Otil: Accelerating Diffusion Model Inference via Communication-Efficient Multi-GPU Parallelism"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Otil_Accelerating_Diffusion_Model_Inference_via_Communication_Efficient_Multi_GPU_Parallelism.pdf
project_link: null
code_link: "https://github.com/uplaoli/OTIL-PROJECT"
aliases:
- Otil
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过信息引导的潜在子块选择性传输——计算相邻步的余弦相似度，仅发送变化最大的top-k子块（k/K=1/4），并引入动态轮询机制保证所有子块在若干步内轮流更新，在不牺牲生成保真度的前提下大幅降低通信量。
primary_logic: 扩散去噪过程中相邻步间潜在激活变化微小且空间局部化，因此只需同步最活跃的少数区域即可实现近无损的并行推理。
claims:
- 相邻步激活的平均相对MAE仅为0.01
- 当复用陈旧激活时，只有少量空间区域产生显著更新
- 根据余弦相似度选择top-k变化最大的子块进行通信（k/K=1/4）可在保持质量的同时降低延迟
- 动态轮询机制确保每个子块在若干步内至少被更新一次，避免遗漏区域
---

# Otil: Accelerating Diffusion Model Inference via Communication-Efficient Multi-GPU Parallelism

> [!tip] 核心洞察
> 扩散去噪过程中相邻步间潜在激活变化微小且空间局部化，因此只需同步最活跃的少数区域即可实现近无损的并行推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | Otil：通过通信高效的多GPU并行加速扩散模型推理 |
| 英文题名 | Otil: Accelerating Diffusion Model Inference via Communication-Efficient Multi-GPU Parallelism |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Otil_Accelerating_Diffusion_Model_Inference_via_Communication-Efficient_Multi-GPU_Parallelism_CVPR_2026_paper.html) · [Code](https://github.com/uplaoli/OTIL-PROJECT) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Otil |
| Dataset | SD 1.5 (U-Net) 512×512, COCO Captions 2014, SDXL 1.0 (U-Net) 1024×1024, COCO Captions 2014 (2 GPUs), SD3 (DiT) 1024×1024, COCO Captions 2014 (4 GPUs), SDXL 1.0, Communication Volume |

> [!tip] 效果简介
> - SD 1.5 (U-Net) 512×512, COCO Captions 2014 上，Speedup↑ 1.74× vs 1.0× (Original) (+0.74×)。
> - SDXL 1.0 (U-Net) 1024×1024, COCO Captions 2014 (2 GPUs) 上，Speedup↑ 1.88× vs 1.0× (Original) (+0.88×)。
> - SDXL 1.0 (U-Net) 1024×1024, COCO Captions 2014 (4 GPUs) 上，Speedup↑ 2.23× vs 1.0× (Original) (+1.23×)。

## 概要

扩散模型在高质量图像生成领域取得了显著成功，但其迭代去噪过程计算量庞大，单GPU推理延迟居高不下。现有多GPU并行方案——如**DistriFusion**（Li et al., CVPR 2024）通过陈旧激活实现并行、**AsyncDiff**（Chen et al., NeurIPS 2024）采用异步去噪流水线——虽能加速推理，却均需在每个去噪步后交换完整的中间特征激活，导致严重的GPU间通信开销，成为制约加速比的关键瓶颈。

本文的核心洞察在于：扩散去噪过程中，相邻步间的潜在激活变化极其微小（平均相对MAE仅约0.01），且这些变化高度集中于少数空间区域，因此全量通信存在极大的冗余。基于此，论文提出**Otil**——一种通信高效的多GPU并行推理框架。Otil将特征图划分为均匀方形子块，通过计算相邻步子块的余弦相似度，仅选择变化最大的top-k子块进行GPU间传输，并引入动态轮询机制确保所有空间区域在若干步内均被更新，从而在不牺牲生成保真度的前提下大幅压缩通信量。

实验表明，在SDXL 1.0上，Otil在2 GPU和4 GPU配置下分别实现1.88×和2.23×的加速，同时相比AsyncDiff减少87.5%至93.75%的通信量；与快速采样器和LoRA结合后，加速比可进一步提升至2.84×。该方法为扩散模型的高效多GPU部署提供了新的通信优化范式。

扩散模型已成为文本到图像生成领域的主流架构，但其迭代去噪过程计算密集，单GPU推理延迟居高不下。为加速推理，多GPU并行方案应运而生，然而现有方法面临一个核心瓶颈：**每步去噪后需在GPU间交换完整的中间特征激活，导致严重的通信开销**。

现有并行方法大致分为两类。**Patch方法**（如**DistriFusion**，Li et al., CVPR 2024）将特征图切分到多GPU，每步通过陈旧激活实现并行，但需广播完整激活图；**流水线方法**（如**AsyncDiff**，Chen et al., NeurIPS 2024）以异步方式组织去噪流水线，但每一步仍需交换完整中间结果。两类方法均未触及通信冗余的本质——它们默认每步激活的所有空间区域都同等重要，因而传输全量数据。**ParaDiGMS**（Shih et al., NeurIPS 2023）虽尝试并行采样，但使用Picard迭代可能偏离扩散轨迹，影响生成保真度。

本文通过经验观察揭示了打破这一瓶颈的关键洞见。如Figure 3(a)所示，**相邻去噪步之间潜在激活的平均相对MAE仅为0.01**，变化幅度极小。更关键的是，如Figure 3(b)所示，当复用陈旧激活时，**只有少量空间区域产生显著更新**，绝大多数区域的变化几乎可以忽略。这意味着每步全量通信存在极大的冗余——大量传输的激活信息在相邻步间近乎不变。

基于这一观察，Otil提出了一条根本性的优化路径：**既然相邻步激活变化微小且空间局部化，只需同步最活跃的少数区域即可实现近无损的并行推理**。具体而言，Otil将特征图分解为均匀方形子块，通过计算相邻步子块的余弦相似度识别变化最大的top-k子块，仅传输这些“高信息量”子块，从而将通信量降至全量传输的k/K（默认1/4）。同时引入动态轮询机制，确保所有空间区域在若干步内至少被更新一次，避免信息遗漏。

这一设计使得Otil在保持生成质量的前提下，相比DistriFusion减少75%通信量，相比AsyncDiff减少最高93.75%的通信量（4 GPU场景），为扩散模型的多GPU高效推理开辟了新方向。

## 核心方法与创新机理

Otil 的核心创新在于将多 GPU 扩散推理的通信模式从“全量同步”转变为“信息引导的选择性同步”，从而在不牺牲生成保真度的前提下大幅降低通信开销。这一转变建立在两个关键的经验观察之上：**（1）相邻去噪步间潜在激活的变化极小**——平均相对 MAE 仅为 0.01（Figure 3(a)）；**（2）变化高度空间局部化**——当复用陈旧激活时，仅有少数空间区域产生显著更新（Figure 3(b)）。基于这些观察，Otil 引入了三个紧密耦合的 changed slots，构成其相对于现有并行方法（如 **DistriFusion** (Li et al., CVPR 2024) 和 **AsyncDiff** (Chen et al., NeurIPS 2024)）的本质差异。

### 从全量通信到信息引导子块传输

**DistriFusion** 和 **AsyncDiff** 在每个去噪步后均需交换完整的中间特征激活，通信量与激活张量大小成正比。Otil 将这一通信策略从“全量激活广播/交换”改为“仅传输 $k/K = 1/4$ 的最具信息量子块”（changed slot: 通信策略）。具体而言，Otil 首先将各 GPU 上的特征图分解为 $K$ 个 $8 \times 8$ 的均匀方形子块（changed slot: 子块粒度），然后计算相邻步同一空间位置子块的余弦相似度：

$$s _ { t } ^ { ( n ) } ( i ) = \frac { \left. \Pi _ { i } x _ { t } ^ { ( n ) } , \Pi _ { i } x _ { t + 1 } ^ { ( n ) } \right. _ { F } } { \left\| \Pi _ { i } x _ { t } ^ { ( n ) } \right\| _ { F } \left\| \Pi _ { i } x _ { t + 1 } ^ { ( n ) } \right\| _ { F } }$$

相似度越小表示该子块变化越大。基于此，Otil 选取 top-k 个变化最大的子块进行跨 GPU 传输（changed slot: 子块选择机制）：

$$\mathcal { A } _ { t } ^ { ( n ) } = \mathrm { T o p k } _ { i \in \{ 1 , . . . , K \} } \big ( d _ { t } ^ { ( n ) } ( i ) , k \big )$$

消融实验证实，当 $k/K = 1/4$ 时，延迟与图像质量取得最佳平衡——在 SD 1.5 双 GPU 配置下，每步延迟降至 13.6975ms，LPIPS 仅为 0.0425（Table 3）。子块大小 $8 \times 8$ 同样被验证为最优设置，在 SDXL 双 GPU 配置下延迟为 27.5324ms，LPIPS 为 0.0142（Table 4）。余弦相似度作为选择指标优于 SSIM、MSE 等传统指标，更能吻合图像可见变化区域（Figure 7）。

### 动态轮询机制保证空间覆盖完整性

纯粹基于相似度的 top-k 选择存在一个隐患：某些空间区域可能在多步中始终未被选中，导致信息遗漏和生成质量下降。Otil 引入**动态轮询机制**（changed slot: 空间覆盖保证）来解决这一问题。该机制维护一个未访问子块集合 $\mathcal{U}_t$，强制每步选择的子块必须来自该集合，一旦所有子块均被访问后则重置：

$$\mathcal { A } _ { t } ^ { ( n ) } \subseteq \mathcal { U } _ { t } , \qquad \mathcal { U } _ { t + 1 } = \left\{ \begin{array} { l l } { \mathcal { U } _ { t } \setminus \mathcal { A } _ { t } ^ { ( n ) } , } & { \mathrm { i f } \mathcal { U } _ { t } \not = \emptyset , } \\ { \{ 1 , 2 , \dots , K \} , } & { \mathrm { o t h e r w i s e } . } \end{array} \right.$$

这一机制确保每个子块在若干步内至少被更新一次，避免遗漏区域，同时不显著增加通信量。其设计前提是去噪步数足够让所有子块完成一次覆盖；在极少步数或极高并行度下，空间覆盖完整性可能受影响，这是需要手动验证的边界条件。

### 通信量的理论缩减

从通信量角度，Otil 每步的 GPU 间通信量为：

$$C _ { \mathrm { O t i l } } = \frac { k } { K } ( p - 1 ) M$$

其中 $p$ 为 GPU 数量，$M$ 为单 GPU 的激活数据量。与 DistriFusion 的全量通信 $C_{\mathrm{DistriFusion}} = (p-1)M$ 相比，Otil 将通信量降低至原来的 $k/K$。实验结果表明，Otil 相比 DistriFusion 减少 75% 通信量，相比 AsyncDiff 在双 GPU 下减少 87.5%、四 GPU 下减少 93.75%（Section 4.3, Section 5）。这一通信缩减直接转化为推理加速：在 SDXL 1024×1024 分辨率下，Otil 在双 GPU 上实现 1.88× 加速，四 GPU 上实现 2.23× 加速（Table 1）。

**需注意的公平性限制**：所有评估均在 PCIe 互连的 A100 GPU 上进行，该环境可能放大通信瓶颈的影响。在更高带宽连接（如 NVLink）下，通信减少带来的加速比可能下降，此时计算瓶颈可能成为主要矛盾，这一点需要手动验证。

Otil 的整体设计围绕一个核心观察展开：扩散模型相邻去噪步之间的潜在激活变化极小（平均相对 MAE 仅约 0.01），且变化集中在少数空间区域（Figure 3）。基于此，Otil 将传统的“全量激活交换”范式替换为“信息引导的部分子块传输”，在保持生成保真度的前提下大幅削减 GPU 间通信量。其 pipeline 由四个关键模块串联构成：

1. **空间划分（Spatial Partitioning）**  
   将特征图沿行或列方向划分为 N 个连续段，每段分配给一个 GPU（N = 设备数）。每段内部再进一步分解为 K 个均匀的方形子块（默认 8×8 大小）。该两级划分策略既均衡了各 GPU 的计算负载，又为后续细粒度的选择性通信提供了基础单元。

2. **信息引导传输（Information-guided Sub-block Transmission）**  
   在每个去噪步 t，各 GPU 计算其本地段内每个子块在相邻两步（t 与 t+1）之间的余弦相似度（Equation 1）。相似度越小，表示该子块的变化越大。随后，按变化程度排序，选取 top-k 个变化最大的子块进行跨 GPU 传输（Equation 2）。默认 k/K = 1/4，即仅传输 25% 的子块，通信量同比降至全量传输的 1/4。

3. **动态轮询机制（Dynamic Polling）**  
   单纯依赖 top-k 选择可能导致某些空间区域长期不被更新。为此，Otil 维护一个未访问子块集合 $\mathcal{U}_t$，强制在当前轮询周期内优先从 $\mathcal{U}_t$ 中选择传输子块；一旦所有子块均被访问一次，集合重置（Equation 4）。该机制保证了在有限步数内所有空间区域至少被同步一次，避免信息遗漏。

4. **分布式注意力融合（Distributed Attention Fusion）**  
   各 GPU 仅计算本地 Query，而 Key/Value 通过跨设备共享。接收到的远端子块按空间位置拼回完整的特征图后，各 GPU 再进行本地的去噪计算。这一设计使得注意力计算可以分布式执行，同时保持全局上下文的一致性。

**输入输出流**：  
- **输入**：随机噪声或上一轮去噪后的完整潜在表示 $x_t$（经过若干预热步后，每个 GPU 已持有完整图像激活的副本）。  
- **每步处理**：各 GPU 仅对其分配的空间段执行去噪，生成对应段的输出；同时，通过信息引导传输模块将变化最大的子块发送给其他 GPU，并接收来自其他 GPU 的子块以补全本地特征图。  
- **输出**：最终去噪步前，所有 GPU 的结果聚合为完整的生成图像。

整个 pipeline 的通信量由 $C_{\text{Otil}} = \frac{k}{K}(p-1)M$ 给出（Equation 7），其中 $p$ 为 GPU 数量，$M$ 为单 GPU 的激活数据量。与 DistriFusion 的全量通信 $C_{\text{DistriFusion}} = (p-1)M$ 相比，Otil 的通信量降低至其 $k/K$ 倍；与 AsyncDiff 相比，在 4 GPU 配置下通信量可减少 93.75%。这一架构层面的通信压缩是 Otil 实现 1.74×–2.23× 加速比（Table 1）且保持图像质量（LPIPS、PSNR、CLIP Score 等指标接近原始模型）的根本原因。

![[assets/figures/papers/paper_list_l907_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Otil_Accelerating_D/figures/001_Figure_1.jpg]]
*Figure 1: (a) Patch method broadcasts full activations, causing heavy communication. (b) Pipeline method exchanges full intermediate activations, limiting efficiency. (c) Otil sends only variant sub-blocks, minimizing communication*

### 两级空间划分

Otil 采用两级空间划分策略以充分利用多 GPU 资源。首先将特征图沿行或列方向划分为 N 段，每段分配给一个 GPU；每个 GPU 完成其分段的去噪后，将该段进一步分解为 K 个均匀方形子块（默认 8×8）。这一划分使得后续的选择性通信可以在更细粒度上操作，同时保持计算负载均衡（Section 3.2）。

### 信息引导的子块传输

该模块是 Otil 的核心创新，其设计动机来自两个关键经验观察（Figure 3）：
- 相邻去噪步之间激活的平均相对 MAE 仅为约 0.01，说明逐步变化整体微小；
- 当复用陈旧激活时，只有少量空间区域产生显著更新，其余区域几乎不变。

![[assets/figures/papers/paper_list_l907_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Otil_Accelerating_D/figures/003_Figure_3.jpg]]
*Figure 3: (a) Relative MAE between adjacent denoising steps t and t+1 for the activations*

基于上述观察，Otil 通过计算相邻步同一空间位置子块的余弦相似度来量化变化程度：

$$s _ { t } ^ { ( n ) } ( i ) = \frac { \left\langle \Pi _ { i } x _ { t } ^ { ( n ) } , \Pi _ { i } x _ { t + 1 } ^ { ( n ) } \right\rangle _ { F } } { \left\| \Pi _ { i } x _ { t } ^ { ( n ) } \right\| _ { F } \left\| \Pi _ { i } x _ { t + 1 } ^ { ( n ) } \right\| _ { F } } \quad \text{(Eq. 1)}$$

其中 $\Pi_i$ 表示取出第 $i$ 个子块，$x_t^{(n)}$ 为 GPU $n$ 在时间步 $t$ 的激活，$\langle\cdot,\cdot\rangle_F$ 为 Frobenius 内积。相似度越小，表示该子块变化越大。

定义差异度 $d_t^{(n)}(i) = 1 - s_t^{(n)}(i)$，然后选取差异度最大的 top-k 子块进行跨 GPU 传输：

$$\mathcal { A } _ { t } ^ { ( n ) } = \mathrm { Topk } _ { i \in \{ 1 , ... , K \} } \big ( d _ { t } ^ { ( n ) } ( i ) , k \big ) \quad \text{(Eq. 2)}$$

消融实验（Table 3）表明，$k/K=1/4$ 时延迟与生成质量达到最佳平衡：在 SD1.5 2 GPU 设置下，每步延迟仅 13.70 ms，LPIPS 为 0.0425。子块尺寸消融（Table 4）则验证了 8×8 为最优粒度。

### 动态轮询机制

仅依赖相似度选择可能导致某些空间区域在多个步中持续被忽略，造成信息遗漏。为此 Otil 引入动态轮询机制，维护未访问子块集合 $\mathcal{U}_t$，强制在有限步数内让所有子块至少被传输一次：

$$\mathcal { A } _ { t } ^ { ( n ) } \subseteq \mathcal { U } _ { t } , \qquad \mathcal { U } _ { t + 1 } = \left\{ \begin{array} { l l } { \mathcal { U } _ { t } \setminus \mathcal { A } _ { t } ^ { ( n ) } , } & { \mathrm { i f } \ \mathcal { U } _ { t } \neq \emptyset , } \\ { \{ 1 , 2 , \dots , K \} , } & { \mathrm { o t h e r w i s e } . } \end{array} \right. \quad \text{(Eq. 4)}$$

当一个轮询周期内所有子块均被访问后，$\mathcal{U}_t$ 重置为全集，开始新周期。该机制以极小开销保证了空间覆盖的完整性，避免生成质量因局部区域长期未更新而退化。

### 分布式注意力融合与通信量分析

各 GPU 仅计算本地 Query，而 Key/Value 跨设备共享；接收到的子块按空间位置拼回完整特征图后继续去噪。这一融合方式使得 Otil 可与标准扩散 U-Net 或 DiT 架构无缝集成（Section 3.4）。

从通信量角度看，设每步全量通信量为 $M$，GPU 数量为 $p$。DistriFusion 每步通信量为 $(p-1)M$，而 Otil 仅传输 $k/K$ 比例的子块：

$$C _ { \mathrm { O t i l } } = \frac { k } { K } ( p - 1 ) M \quad \text{(Eq. 7)}$$

当 $k/K=1/4$ 时，Otil 相比 DistriFusion 减少 75% 通信量；在 4 GPU 设置下相比 AsyncDiff 可减少最高 93.75% 通信量，直接转化为端到端推理加速。

### 与扩散更新过程的关联

Otil 的选择性传输策略之所以可行，根植于扩散模型去噪过程的更新公式：

$$\boldsymbol { x } _ { t - 1 } = \alpha _ { t } \boldsymbol { x } _ { t } + \beta _ { t } \boldsymbol { \hat { \varepsilon } } _ { \boldsymbol { \theta } } ( \boldsymbol { x } _ { t } , t ) \quad \text{(Eq. 3)}$$

该式表明，相邻步的潜在变化由预测噪声 $\hat{\varepsilon}_\theta$ 驱动，而噪声预测在空间上天然具有局部性——这正是 Otil 仅需同步少量变化子块即可维持全局生成一致性的理论基础。

## 实验与关键发现

### 实验设置

实验在NVIDIA A100 GPU（PCIe互连）上进行，评估涵盖U-Net架构的Stable Diffusion 1.5（512×512）和SDXL 1.0（1024×1024），以及DiT架构的Stable Diffusion 3（1024×1024）。测试数据集为COCO Captions 2014的一个子集。评估指标包括加速比（Speedup↑）、PSNR、LPIPS、FID和CLIP Score，以综合衡量推理效率与生成保真度。基线方法包括原始单GPU推理、**DistriFusion**（Li et al., CVPR 2024）和**AsyncDiff**（Chen et al., NeurIPS 2024）。

### 主要结果

**Table 1**展示了Otil在文本到图像生成任务上的定量对比结果。在SD 1.5上，Otil在2 GPU下实现1.74×加速，相比原始单GPU推理提升显著。在SDXL 1.0上，Otil的加速效果更为突出：2 GPU下达到1.88×，4 GPU下达到2.23×。对于SD3（DiT架构），4 GPU下实现2.00×加速，证明了该方法对不同扩散模型架构的泛化能力。

值得注意的是，Otil在取得显著加速的同时，生成质量指标（PSNR、LPIPS、FID、CLIP Score）与原始模型相比仅有轻微下降。例如，SDXL 1.0在2 GPU下的PSNR为25.171，LPIPS为0.0142，表明选择性子块传输策略有效保持了空间一致性。与DistriFusion和AsyncDiff相比，Otil在相近或更好的质量指标下实现了更高的加速比，这归因于其大幅降低的通信开销。

**Table 2**展示了Otil与快速采样器和LoRA加速技术的兼容性。在SD 1.5上结合LoRA后，Otil在2 GPU下实现2.46×加速，显示出该方法可与现有加速技术正交叠加，进一步缩短推理延迟。

### 通信量分析

Otil的核心优势在于通信量的显著降低。根据Section 4.3的分析，Otil相比DistriFusion减少75%的通信量，相比AsyncDiff在2 GPU下减少87.5%，在4 GPU下减少高达93.75%。这一结果直接验证了信息引导子块传输策略的有效性——仅传输k/K=1/4的最具信息量子块即可维持近无损的生成质量。

通信量的降低直接转化为延迟的减少。由于通信延迟与传输数据量成正比，Otil通过将全量激活交换替换为部分子块传输，打破了通信瓶颈对多GPU并行效率的限制。

### 消融实验

#### 传输子块数量（k/K）的影响

**Table 3**展示了传输子块比例k/K对每步延迟和图像质量的影响。当k/K=1/4时，系统取得延迟与质量的最佳平衡：在SD 1.5 2 GPU设置下，每步延迟为13.6975ms，LPIPS为0.0425。进一步减少k/K会导致质量明显下降，而增加k/K则带来通信开销的线性增长，削弱加速效果。该结果验证了“仅少数空间区域产生显著更新”的核心观察——传输1/4的子块已足以覆盖最具信息量的变化区域。

#### 子块尺寸的影响

**Table 4**考察了子块尺寸对性能的影响。实验表明8×8的均匀方形子块为最优设置：在SDXL 2 GPU下，每步延迟为27.5324ms，LPIPS为0.0142。过大的子块会导致传输粒度过粗，包含冗余信息；过小的子块则增加选择开销和通信碎片化。8×8的子块在空间精度和传输效率之间取得了良好平衡。

#### 子块选择指标的比较

**Figure 7**比较了不同图像相似度指标（余弦相似度、SSIM、MSE等）作为子块选择依据的效果。余弦相似度最能吻合图像中实际可见变化的区域，因此被选为Otil的子块变化度量。这一选择基于以下观察：余弦相似度对特征方向变化敏感，而扩散去噪过程中潜在激活的变化主要体现在方向而非幅度上。

#### 动态轮询机制的必要性

消融实验（Section 3.3，Equation 4）表明，移除动态轮询机制会导致部分空间区域在多个去噪步内未被更新，产生可见的伪影和质量下降。动态轮询通过维护未访问子块集合并在周期内强制覆盖所有区域，确保了空间一致性和生成保真度。

### 定性结果

**Figure 5**展示了SDXL 1.0上的定性生成结果。Otil在使用2 GPU和4 GPU时均能生成与原始模型视觉质量相当的图像，细节保留完整，无明显拼接痕迹或空间不一致性。**Figure 6**进一步展示了Otil与快速采样器和LoRA结合的可视化结果，验证了方法在实际部署场景中的兼容性和鲁棒性。

### 实验局限性

需要指出的是，所有实验均在PCIe互连的A100 GPU上进行。PCIe的带宽限制可能放大了通信瓶颈的严重程度，使得Otil的通信减少策略获得了更显著的加速收益。在更高带宽连接（如NVLink）下，通信开销本身较小，Otil的相对加速比可能有所降低——此时计算瓶颈可能成为主要矛盾。此外，实验仅覆盖COCO Captions 2014子集和有限模型规模，对不同分辨率、更大规模GPU集群及视频扩散模型的泛化性尚需进一步验证。

![[assets/figures/papers/paper_list_l907_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Otil_Accelerating_D/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison for text-to-image generation. Underlined values denote the best performance*

![[assets/figures/papers/paper_list_l907_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Otil_Accelerating_D/figures/009_Table_3.jpg]]
*Table 3: The Impact of the Number of High-Quality Latents on Per-Step Latency and Overall Image Quality*

![[assets/figures/papers/paper_list_l907_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Otil_Accelerating_D/figures/010_Table_4.jpg]]
*Table 4: The Impact of Sub-block Size on Per-Step Latency and Overall Image Quality*

![[assets/figures/papers/paper_list_l907_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Otil_Accelerating_D/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results on SDXL 1.0. Otil can reduce the latency according to the number of used devices with minimal impact on generative quality*

## 定位与知识库关联

### 与基线方法的关系

Otil 的核心贡献在于将扩散模型多 GPU 并行推理的优化焦点从**计算调度**转向**通信选择性**，这与现有方法形成了清晰的演进关系。

**DistriFusion**（Li et al., CVPR 2024）首次提出利用扩散去噪的时序平滑性，允许各 GPU 使用陈旧激活进行并行计算，从而打破同步屏障。然而，其每步仍需广播完整特征图，通信量随分辨率和设备数线性增长。Otil 继承了“容忍陈旧激活”的思想，但将通信对象从全量激活收缩为**信息量最大的局部子块**——这一改变的根本依据来自 Figure 3(a) 的观察：相邻步激活的平均相对 MAE 仅为 0.01，全量通信存在严重冗余。

**AsyncDiff**（Chen et al., NeurIPS 2024）通过流水线异步去噪进一步隐藏通信延迟，但传输内容仍为完整中间结果。Otil 与之正交：AsyncDiff 优化的是**通信时机**（何时传），Otil 优化的是**通信内容**（传什么）。两者可叠加，但 Otil 单独即在通信量上实现 87.5%（2 GPUs）至 93.75%（4 GPUs）的削减（Section 4.3），从根本上压缩了通信瓶颈。

**ParaDiGMS**（Shih et al., NeurIPS 2023）采用 Picard 迭代近似并行采样，绕开了逐步依赖，但可能偏离原始扩散轨迹，影响生成保真度。Otil 与之不同：它严格遵循原始去噪路径，仅在通信环节做近似，保真度损失由信息引导选择机制和动态轮询机制双重约束。

### 核心创新与因果机制

Otil 的方法设计可拆解为三个因果环节，形成一条完整的“观察→选择→保障”链条：

1. **空间稀疏性观察**（Figure 3）：相邻步激活变化不仅幅度微小（MAE≈0.01），且高度局部化——当复用陈旧激活时，仅少数空间区域产生显著更新（Figure 3(b)）。这构成了选择性通信的实证基础。

2. **信息引导的 Top-k 选择**（Equation 1-2）：将特征图划分为 K 个均匀方形子块（默认 8×8），计算相邻步同一子块的余弦相似度 $s_t^{(n)}(i)$，值越小表示变化越大。选取 top-k 个最活跃子块进行跨 GPU 传输，k/K=1/4 在延迟与质量间取得最佳平衡（Table 3：SD1.5 2 GPUs 延迟 13.70ms，LPIPS 0.0425）。

3. **动态轮询保障**（Equation 4）：维护未访问子块集合 $\mathcal{U}_t$，强制在若干步内让每个子块至少被更新一次，防止信息遗漏区域累积误差。这一机制是 Otil 在通信量大幅削减后仍能维持生成质量的关键——它保证了空间覆盖的完整性，而非仅依赖局部变化检测。

### 适用边界与局限

Otil 的适用边界由以下条件刻画：

- **通信瓶颈主导的场景**：Otil 的加速效果依赖于通信开销在总延迟中占比显著。在 PCIe 互连（如实验所用的 A100 环境）下效果明显，但在 NVLink 等高带宽连接下，计算瓶颈可能上升为主要矛盾，通信削减的边际收益将递减。这一边界尚未在论文中验证。

- **去噪步数充足的假设**：动态轮询机制要求去噪步数足够让所有子块至少被覆盖一次。在极少数步采样（如 4 步 DPM-Solver）或极高并行度（GPU 数接近子块数）下，空间覆盖的完整性可能受影响。Table 2 显示 Otil 与快速采样器兼容，但未见对轮询周期长度的敏感性分析。

- **模型与分辨率泛化**：实验覆盖 SD 1.5（U-Net，512²）、SDXL 1.0（U-Net，1024²）和 SD3（DiT，1024²），但均基于 A100 GPU 和 COCO Captions 2014 子集。对不同模型架构（如视频扩散模型）、更大规模 GPU 集群、更低带宽环境的泛化性尚不明确。

- **子块粒度与 k/K 比例的固定性**：当前 8×8 子块和 k/K=1/4 为固定设置，未根据去噪进度或内容复杂度动态调整。去噪早期可能需更多通信，后期可进一步压缩，固定比例可能非全局最优。

### 开放问题

1. **高带宽互联下的瓶颈转移**：在 NVLink 等环境下，通信削减是否仍能带来显著加速？此时计算瓶颈是否会成为主要矛盾，需要结合计算优化（如算子融合、量化）才能进一步提升？

2. **自适应轮询与 k/K 比例**：能否根据去噪进度（如噪声水平 $\sigma_t$）或内容变化幅度动态调整轮询频率和传输子块数量？例如，在去噪早期使用更大的 k/K，后期逐步缩减。

3. **视频扩散模型的时序并行**：Otil 的空间子块选择机制是否可扩展到视频扩散模型的时空并行？时序维度的相邻帧变化是否同样具有稀疏性？

4. **与其他压缩技术的联合**：Otil 的通信削减与特征量化、低精度通信等技术是否可叠加？联合优化空间有多大？

## 原文 PDF

![[paperPDFs/CVPR_2026/Otil_Accelerating_Diffusion_Model_Inference_via_Communication_Efficient_Multi_GPU_Parallelism.pdf]]
