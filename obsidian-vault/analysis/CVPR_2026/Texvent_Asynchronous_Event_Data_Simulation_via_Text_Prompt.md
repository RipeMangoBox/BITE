---
title: "Texvent: Asynchronous Event Data Simulation via Text Prompt"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Texvent_Asynchronous_Event_Data_Simulation_via_Text_Prompt.pdf
project_link: null
code_link: "https://github.com/rfww/texvent"
aliases:
- Texvent
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用多模态大语言模型实现训练无关的文本到视频生成，并通过自适应亮度感知帧插值、平衡对数强度比较及缓存电压刷新机制，生成高保真事件流。
primary_logic: 将文本到视频生成与物理仿真相集成，通过平衡对数亮度和缓存机制缓解仿真与真实的差距，实现开放世界事件数据的快速生成。
claims:
- Texvent在NT-ImageNet数据集上获得最高的EQS 0.8851，同时运行时间仅0.0653秒，显著优于现有视频到事件模拟器。
- 在事件相机数据集的图像重建任务中，仅添加5%的Texvent生成数据，即可使HyperE2VID的PSNR提升至23.3000。
- 消融研究显示，移除亮度缓存会使EQS下降4.01%，验证了缓存机制的必要性。
- NT-ImageNet (Event Frames) 上 MSE = 0.045
---

# Texvent: Asynchronous Event Data Simulation via Text Prompt

> [!tip] 核心洞察
> 将文本到视频生成与物理仿真相集成，通过平衡对数亮度和缓存机制缓解仿真与真实的差距，实现开放世界事件数据的快速生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Texvent: 通过文本提示进行异步事件数据仿真 |
| 英文题名 | Texvent: Asynchronous Event Data Simulation via Text Prompt |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Texvent_Asynchronous_Event_Data_Simulation_via_Text_Prompt_CVPR_2026_paper.html) · [Code](https://github.com/rfww/texvent) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Texvent |
| Dataset | NT-ImageNet, Event Camera Dataset |

> [!tip] 效果简介
> - NT-ImageNet (Event Frames) 上，MSE 0.045 (best)。
> - NT-ImageNet (Reconstructed Images) 上，SSIM 0.472 (highest)。
> - NT-ImageNet 上，LPIPS (Event Frames) 0.339 (lowest)。

## 概要

事件相机以其异步、高时间分辨率、低延迟的特性，在高速运动和高动态范围场景中展现出独特优势，但其数据采集成本高昂、标注困难，严重制约了下游算法的发展。现有事件仿真方法主要分为两类：**视频到事件模拟器**（如 **ESIM** (Rebecq et al., CoRL 2018)、**VID2E** (Gehrig et al., CVPR 2020)、**V2E** (Hu et al., CVPR 2021)、**V2CE** (Zhang et al., ICRA 2024)、**DVS-Voltmeter** (Lin et al., ECCV 2022)）依赖视频输入，采集成本依然较高且难以适应开放世界的多样化场景；**文本到事件方法**（如 **Text-to-Events** (Ott et al., NICE 2024)）则依赖昂贵的文本-事件对进行训练，缺乏通用性和效率。这一瓶颈的核心在于：**缺乏一种训练无关、仅凭文本即可生成高保真异步事件流的通用框架**。

Texvent 的核心思路是将**多模态大语言模型驱动的文本到视频生成**与**物理仿真**相集成，实现开放世界事件数据的快速生成。其关键因果机制包括：(1) 利用训练无关的文本到视频模型生成高帧率视频序列，免去对文本-事件对的依赖；(2) 提出**自适应亮度感知帧插值**策略，根据亮度变化动态确定中间帧数量；(3) 引入**平衡对数强度比较**与**缓存电压刷新机制**，缓解低光与高光区域事件激活的不平衡问题，并防止长时仿真中的事件丢失；(4) 通过自适应泊松噪声注入和基于亮度变化率的密集时间戳重建，进一步缩小仿真与真实数据的差距。

在 NT-ImageNet 数据集上，Texvent 取得了最高的 **EQS 0.8851**，同时运行时间仅 **0.0653 秒**，显著优于现有视频到事件模拟器（Table 2）。在事件相机数据集的图像重建任务中，仅添加 **5%** 的 Texvent 生成数据，即可使 HyperE2VID 的 PSNR 提升至 **23.3000**（Table 3）。消融研究进一步验证了亮度缓存机制的关键作用：移除缓存导致 EQS 下降 **4.01%**（Figure 7）。

**方法定位**：Texvent 属于训练无关的文本到事件仿真方法，区别于需要视频输入或文本-事件对训练的现有方案。其知识贡献在于将物理仿真中的对数亮度平衡与缓存机制引入文本驱动的生成管线，为开放世界事件数据增强提供了高效、低成本的解决方案。当前局限性包括：生成质量受底层文本到视频模型性能约束，未完全模拟事件相机的所有非理想特性（如像素阈值失配），且尚不支持实时生成。

事件相机是一种受生物启发的视觉传感器，通过异步记录像素级对数亮度变化来输出稀疏事件流。与传统帧相机不同，事件相机具有微秒级时间分辨率、高动态范围和低数据冗余等优势，在高速运动估计、低光照视觉和动态场景理解等任务中展现出巨大潜力。然而，事件相机依赖物理采集获取数据，硬件成本高昂，且难以覆盖开放世界中多样化的场景与运动模式，这严重制约了事件驱动视觉算法的开发与评估。

为缓解数据稀缺问题，事件仿真技术应运而生。其核心目标是从现有数字内容（如图像、视频）出发，通过物理模型模拟事件生成过程，从而绕过物理采集。现有视频到事件模拟器，如 **ESIM**（Rebecq et al., CoRL 2018）、**VID2E**（Gehrig et al., CVPR 2020）、**V2E**（Hu et al., CVPR 2021）、**V2CE**（Zhang et al., ICRA 2024）和 **DVS-Voltmeter**（Lin et al., ECCV 2022），已能生成较逼真的事件流，但它们严重依赖高质量视频输入。视频数据的采集本身同样耗时耗力，且难以灵活适配文本描述所定义的新场景，使得仿真管线在开放世界场景下的可扩展性受到根本性限制。

另一条技术路线试图直接从文本生成事件，如 **Text-to-Events**（Ott et al., NICE 2024），但这类方法依赖昂贵的文本-事件配对数据进行监督训练，缺乏通用性，且生成的事件流在保真度和多样性上仍与真实数据存在显著差距。

上述困境揭示了一个关键瓶颈：**现有事件仿真方法要么受限于视频数据的采集成本与场景覆盖度，要么受限于文本-事件对的稀缺性与训练依赖，均无法实现低成本、高保真且场景可自由定义的开放世界事件数据生成。**

Texvent 正是在这一背景下提出，旨在打破传统仿真管线对视频采集或配对训练的依赖。其核心动机是：**将多模态大语言模型驱动的文本到视频生成与物理级事件仿真相集成，通过训练无关的方式，仅凭文本提示即可生成高保真异步事件流，从而以极低成本实现开放世界事件数据的按需生成。**

## 核心方法与创新机理

Texvent 的核心创新在于将**训练无关的文本到视频生成**与**物理感知的事件仿真**深度耦合，构建了一条从文本提示直接生成高保真异步事件流的流水线。相较于传统视频到事件仿真器（如 **ESIM**（Rebecq et al., CoRL 2018）、**VID2E**（Gehrig et al., CVPR 2020）、**V2E**（Hu et al., CVPR 2021）、**V2CE**（Zhang et al., ICRA 2024）、**DVS-Voltmeter**（Lin et al., ECCV 2022））依赖真实视频数据，以及 **Text-to-Events**（Ott et al., NICE 2024）依赖昂贵文本-事件对训练，Texvent 通过多模态大语言模型（MLLM）实现了开放世界的文本驱动仿真，从根本上解耦了数据采集成本与场景多样性。

方法层面的关键创新体现在以下五个 changed slots 上：

**1. 自适应亮度感知帧插值（Brightness-aware Frame Interpolation）**
传统仿真器通常采用固定帧率或基于光流的插值策略。Texvent 提出基于亮度变化的自适应插值机制（Eq. 4），根据两连续帧间的最大对数亮度差动态确定中间帧数量 $K_i = \max(|L(\mathbf{I}_{t_i}) - L(\mathbf{I}_{t_{i+1}})|) \mod \delta$。这一设计使插值密度与场景运动强度解耦，在高动态区域生成更密集的中间帧，避免了固定插值带来的事件缺失或冗余。

**2. 平衡对数强度比较（Balanced Logarithmic Intensity Comparison）**
标准对数强度差在低光照区域具有极高灵敏度，导致事件激活分布向暗区严重偏移。Texvent 引入平衡参数 $\alpha$，将比较公式修正为 $L(\alpha + \mathbf{I})$ 形式（Fig. 3, Sec. 3.2.2），有效缓解了低光照与高光照下事件激活的不平衡问题。消融实验（Figure 7）验证了该机制的定性有效性。

**3. 缓存电压刷新机制（Cache-based Voltage Refreshment）**
传统逐帧亮度比较方式存在事件丢失风险：当某像素长期未触发事件时，其参考亮度值会随时间漂移。Texvent 提出亮度缓存 $\kappa$ 机制（Eq. 5, Fig. 2），在像素未激活事件时持续存储其参考亮度值，周期性重置以避免长期仿真中的虚假事件。消融实验表明，移除亮度缓存会导致事件质量分数（EQS）下降 4.01%（Figure 7），验证了该机制在防止事件丢失方面的关键作用。

**4. 自适应泊松噪声注入（Poisson Noise Injection with Adaptive Low-Light Targeting）**
区别于传统方法使用动态对比阈值模拟背景活动（BA）噪声，Texvent 采用泊松噪声注入策略（Eq. 6），通过掩码 $\mathbf{M}$ 定位低光背景区域，优先向这些区域添加符合传感器填充因子特性的噪声。这一设计更贴近真实事件传感器的噪声分布模式。

**5. 基于亮度变化率的密集时间戳重构（Dense Time Stamp Reconstruction）**
传统仿真器通常采用均匀或压缩时间戳，Texvent 提出基于亮度变化率 $\Delta_L$ 的微秒级时间戳重构（Eq. 7）：$$t^{\mathbf{x}_i} = \gamma \times (t_{i+1} - t_i) \left(1 - \frac{\Delta_L^{\mathbf{x}_i} - \min(\Delta_L)}{\max(\Delta_L) - \min(\Delta_L)}\right) + t_i$$ 较大亮度变化对应较早的触发时刻，使生成的事件流在时间维度上更接近真实传感器的异步特性。

上述五个创新点共同构成了 Texvent 的因果调节旋钮（causal knob）：通过平衡对数亮度和缓存机制缓解仿真与真实的差距，实现开放世界事件数据的快速生成。其决定性证据包括：在 NT-ImageNet 数据集上取得最高 EQS 0.8851，同时运行时间仅 0.0653 秒（Table 2）；仅添加 5% 生成数据即可使 HyperE2VID 的 PSNR 提升至 23.3000（Table 3）。

Texvent 的整体设计遵循“文本→视频→事件流”的两阶段生成范式，将多模态大语言模型的开放世界内容生成能力与物理事件仿真器相结合，实现训练无关（training-free）的异步事件数据合成。

**输入与输出**  
系统接受自然语言文本提示 $\mathbf{T}$ 作为唯一输入，输出为异步稀疏事件流 $\pmb{\mathcal{E}}$，包含像素坐标、极性、微秒级时间戳。整个映射过程可形式化为 $\mathcal{E} = \mathcal{F}(\mathbf{T})$（Eq. 2），其中 $\mathcal{F}$ 为 Texvent 的复合生成函数。

**阶段一：文本驱动的视频生成**  
利用多模态大语言模型（MLLM）的文本编码器 $E(\cdot; \theta_e)$ 和图像解码器 $D(\cdot; \theta_d)$，从文本提示 $\mathbf{T}$ 生成高帧率视频序列 $\mathbf{I}_{t_{\{1:N\}}}$（Eq. 3）。该阶段的关键创新在于亮度感知自适应帧插值（Eq. 4）：根据两连续帧间的最大对数亮度差模除对比阈值 $\delta$，动态确定需插入的中间帧数量 $K_i$，从而在亮度变化剧烈区域生成更多中间帧，提升时序分辨率。

**阶段二：物理事件仿真**  
在生成的高帧率视频序列基础上，依次执行四个核心模块：
1. **事件帧生成**（Eq. 5）：采用平衡对数强度比较，引入平衡参数 $\alpha$ 缓解低光照与高光照区域的事件激活不平衡问题；同时引入亮度缓存 $\kappa$ 存储未触发事件坐标的参考亮度值，防止逐帧计算导致的事件丢失。缓存周期性清零以避免长期仿真中的虚假事件。
2. **背景活动噪声注入**（Eq. 6）：通过掩码 $\mathbf{M}$ 定位低光背景区域，向事件流中添加泊松噪声，噪声强度由填充因子参数 $\lambda_1$ 和传感器适配参数 $\lambda_2$ 联合控制。
3. **密集时间戳重建**（Eq. 7）：基于各坐标的亮度变化率 $\Delta_L^{\mathbf{x}_i}$ 重构每事件的微秒级时间戳——亮度变化越大，触发时刻越早。

**模块间数据流**  
Figure 2 清晰展示了端到端流程：文本提示经 MLLM 编码-解码生成视频帧 → 亮度感知插值提升帧率 → 平衡对数比较与缓存机制生成事件帧 → 泊松噪声注入增强真实性 → 亮度变化率引导的时间戳重建输出最终事件流。各模块之间的耦合关系为串行级联，前一模块的输出直接作为后一模块的输入，无需额外的对齐或优化步骤。

![[assets/figures/papers/paper_list_l2064_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Texvent_Asynchron/figures/002_Figure_2.jpg]]
*Figure 2: Framework of Texvent, including the high frame-rate video generation (Eq. 3, Eq. 4) and event simulation. During computing the event frame (E. F.), we present the brightness cache to store the brightness values at coordinates where no event data has been activated. These values still serve as the reference brightness values in the subsequent event frame generation (Eq. 5). Such a cache is periodically reset as null to avoid acting fake events in long-term event simulation. After injecting the background noise (Eq. 6), we calculate the brightness variation rate (V. R.) at each coordinate to reconstruct the dense time stamps (Eq. 7)*

Texvent 的核心流水线由五个关键模块串联构成：文本驱动视频生成、亮度感知帧插值、带缓存的事件帧生成、背景活动噪声注入、以及密集时间戳重建。以下按处理顺序展开各模块的数学形式与物理含义。

### 文本驱动视频生成

给定文本提示 $\mathbf{T}$，利用多模态大语言模型的编码器 $E(\cdot;\theta_e)$ 与图像解码器 $D(\cdot;\theta_d)$ 生成高帧率视频序列：

$$
\mathbf{I}_{t_{\{1:N\}}} = D(E(\mathbf{T}; \theta_e); \theta_d)
$$

其中 $\mathbf{I}_{t_{\{1:N\}}}$ 表示 $N$ 帧连续图像。该模块将文本语义映射为时空连续的亮度信号，是后续事件仿真的物理基础。

### 亮度感知帧插值

事件相机的时间分辨率远高于常规视频帧率，因此需要在相邻帧间插入中间帧。Texvent 提出亮度感知的自适应插值策略，根据两连续帧间的最大对数亮度差动态确定插值数量 $K_i$：

$$
K_i = \max\left(\left|L(\mathbf{I}_{t_i}) - L(\mathbf{I}_{t_{i+1}})\right|\right) \bmod \delta
$$

其中 $L(\cdot)$ 为对数亮度函数，$\delta$ 为事件相机的对比阈值。该设计的直觉是：亮度变化剧烈的区域需要更密集的时间采样以捕获快速运动，而亮度平稳区域则可减少冗余插值。

### 带缓存的事件帧生成

事件激活的核心条件基于对数亮度差与阈值 $\delta$ 的比较。Texvent 引入两个关键改进——平衡参数 $\alpha$ 与亮度缓存 $\kappa$：

$$
\prod_{i \in \{0:N-1\}} \prod_{j \in \{1:K_i\}} \big| L(\alpha + \mathbf{I}_{(t_i, t_{i+1})}^j) - L(\alpha + \kappa \odot \mathbf{I}_{(t_i, t_{i+1})}^{j-1}) \big| > \delta
$$

**平衡参数 $\alpha$** 的作用：标准对数函数在低光照区域灵敏度极高，高光照区域灵敏度不足（见 Figure 3）。引入 $\alpha$ 可平移对数曲线，缓解这种不公平的事件激活分布，使不同亮度水平下的响应趋于均衡。

**亮度缓存 $\kappa$** 的作用：传统逐帧比较方式中，若某像素因亮度变化不足而未触发事件，其参考亮度值会丢失，导致后续可能遗漏真实事件。缓存机制将未激活坐标的亮度值暂存于 $\kappa$ 中，作为下一事件帧生成的参考基准，并周期性清零以防止长期仿真中产生虚假事件。消融实验表明，移除亮度缓存会使事件质量评分（EQS）下降 4.01%（Figure 7），验证了该机制在防止事件丢失方面的关键作用。

### 背景活动噪声注入

真实事件传感器存在固有的背景活动噪声，Texvent 通过自适应泊松噪声注入进行模拟：

$$
\pmb{\mathcal{E}} = \pmb{\mathcal{E}} \cdot (1 - \mathbf{M}) + \mathbf{M} \cdot \mathbf{Poisson}(\lambda_1 \lambda_2)
$$

其中 $\mathbf{M}$ 为低光背景区域掩码，$\lambda_1$ 控制噪声强度（与传感器填充因子适配），$\lambda_2$ 为场景相关缩放参数。该设计优先在低光照背景区域注入噪声，符合真实传感器在暗光条件下噪声更显著的特性。

### 密集时间戳重建

事件流中每个事件的精确时间戳对下游任务至关重要。Texvent 基于亮度变化率重建微秒级时间戳：

$$
t^{\mathbf{x}_i} = \gamma \times (t_{i+1} - t_i) \left(1 - \frac{\Delta_L^{\mathbf{x}_i} - \min(\Delta_L)}{\max(\Delta_L) - \min(\Delta_L)}\right) + t_i
$$

其中 $\Delta_L^{\mathbf{x}_i}$ 为像素 $\mathbf{x}_i$ 在两帧间的对数亮度变化量，$\gamma$ 为时间缩放参数。直觉上，亮度变化越大的像素，其事件触发时刻越接近帧间隔的起始端，从而在时间维度上更精细地刻画异步事件的物理时序。

## 实验与关键发现

### 实验设置概览

Texvent 的实验验证围绕三个核心维度展开：事件帧与重建图像的保真度、模拟事件流的感知质量与效率，以及生成数据在下游任务中的增强效果。所有模拟器均在统一硬件（NVIDIA H100）和参数设置下评估，运行时间对比具有公平性。基线方法覆盖视频到事件模拟器 **ESIM**（Rebecq et al., CoRL 2018）、**VID2E**（Gehrig et al., CVPR 2020）、**V2E**（Hu et al., CVPR 2021）、**V2CE**（Zhang et al., ICRA 2024）、**DVS-Voltmeter**（Lin et al., ECCV 2022），以及文本到事件模拟器 **Text-to-Events**（Ott et al., NICE 2024）。

### 事件帧与图像重建质量

Table 1 报告了在 NT-ImageNet 数据集上事件帧与重建图像的定量评估结果。在事件帧质量方面，Texvent 取得最低 MSE 0.045 和最低 LPIPS 0.339，SSIM 达到 0.488，表明生成的事件帧在像素级误差和感知相似度上均优于现有方法。在重建图像质量方面，Texvent 以 SSIM 0.472 和 LPIPS 0.296 取得最优，说明从生成事件流重建的图像在结构保持和感知质量上具有显著优势。值得注意的是，Texvent 在两项 LPIPS 指标上均为最低，这直接反映了平衡对数强度比较和亮度缓存机制对事件流结构保真度的贡献。

![[assets/figures/papers/paper_list_l2064_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Texvent_Asynchron/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation of event frames (E. F.) / reconstructed images (R. I.) in terms of mean squared error (MSE), structural similarity (SSIM), and the calibrated perceptual loss (LPIPS). The best and second-best scores are highlighted in bold and underlined*

### 事件质量评分与运行效率

Table 2 给出了各模拟器在 NT-ImageNet 上的事件质量评分（EQS）与运行时间对比。Texvent 以 **EQS 0.8851** 取得最高分，较第二名 DVS-Voltmeter 的 0.8721 提升了 0.0130，验证了所提仿真机制在事件流整体质量上的优势。在效率维度，Texvent 的单次仿真时间仅 **0.0653 秒**，相比 ESIM 约 0.5 秒的参考时间加速近一个数量级。这一效率优势源于训练无关的文本到视频生成流程，无需昂贵的文本-事件对训练或逐帧光流计算。

![[assets/figures/papers/paper_list_l2064_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Texvent_Asynchron/figures/008_Table_2.jpg]]
*Table 2: Event Quality Score (EQS) [5] and runtime of different simulators. The best and second-best scores are highlighted in bold and underlined. DVS. denotes the DVS-Voltmeter*

### 下游任务增强效果

Table 3 展示了在事件相机数据集[33]上，仅添加 **5% 的 Texvent 生成数据**进行增强训练时，各图像重建方法的性能变化。以 HyperE2VID 为例，引入 Texvent 增强后 PSNR 提升至 **23.3000**，达到表中最高值。这一结果表明，即使极小比例的合成数据也能显著提升下游模型的泛化能力，验证了 Texvent 生成数据与真实事件分布的兼容性。该实验同时排除了数据量增加带来的混淆效应——5% 的增量远不足以单独解释性能跃升，核心收益应归因于生成数据的多样性补充。

![[assets/figures/papers/paper_list_l2064_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Texvent_Asynchron/figures/009_Table_3.jpg]]
*Table 3: Comparison to various image reconstruction methods without (✗) and with (✓) our augmented event data on Event Camera dataset [33]. Only 5% event data are generated by Texvent in this experiment. Best results are bolded*

### 消融研究

Figure 7 展示了平衡参数 α 和亮度缓存 κ 的消融结果。移除亮度缓存导致 EQS 下降 **4.01%**，这一显著退化验证了缓存机制在防止事件丢失方面的关键作用——逐帧强度比较会因参考亮度未持续更新而遗漏大量应激活的事件。平衡参数 α 的引入则有效缓解了低光照与高光照区域事件激活的不平衡问题（见 Figure 3）：标准对数函数在低光区对微小亮度变化过于敏感，而 α 通过平移对数曲线使激活阈值在不同亮度区间趋于均匀。

### 定性分析与失败模式

Figure 4 展示了真实事件数据与 Texvent 模拟数据的定性对比，生成的事件流在空间稀疏性、正负事件分布和边缘结构上与真实数据高度一致。Figure 6 揭示了 DSEC 数据集上的一个系统性问题：真实事件与对应视频序列之间存在时间对齐误差，导致模拟事件与真值之间的差异部分源于数据本身的对齐缺陷，而非仿真方法的能力瓶颈。

![[assets/figures/papers/paper_list_l2064_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Texvent_Asynchron/figures/004_Figure_4.jpg]]
*Figure 4: Comparison between the real data (1st row) and our simulated data (2nd row). The event-video collection system consists of a DAVIS346 sensor and an RGB camera (480p, 30fps) followed by [7]. Blue and red denote the positive and negative events, respectively*

![[assets/figures/papers/paper_list_l2064_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Texvent_Asynchron/figures/007_Figure_6.jpg]]
*Figure 6: Warped event and depth map of simulated event data. Discrepancies between groundtruth and simulated event data arise from the misalignment between raw event data and corresponding video sequences in the DSEC dataset [12]*

Texvent 的已知局限包括：（1）生成视频质量受限于底层文本到视频模型（如 Cosmos）的性能，当文本提示处于分布外时可能产生视觉伪影；（2）仿真流程未完全模拟事件相机的所有非理想特性（如像素阈值失配、温度噪声），可能残留 sim-to-real 差距；（3）当前实现无法实时生成，因视频生成和事件模拟需要一定推理时间，但单次仿真效率已显著优于传统方法。这些局限在评估中需要手动验证，因论文未提供针对分布外提示或极端光照条件的系统退化测试。

## 定位与知识库关联

### 与现有事件仿真器的关系

Texvent 处于“文本驱动事件仿真”这一新兴范式与成熟“视频到事件仿真”路线的交汇点。理解其位置需要先梳理两类基线。

**视频到事件仿真器** 是该领域长期的主流方案，它们以高帧率视频为输入，通过物理模型生成事件流。代表性工作包括 **ESIM**（Rebecq et al., CoRL 2018）、**VID2E**（Gehrig et al., CVPR 2020）、**V2E**（Hu et al., CVPR 2021）、**V2CE**（Zhang et al., ICRA 2024）和 **DVS-Voltmeter**（Lin et al., ECCV 2022）。这些方法的共同瓶颈在于：它们严重依赖视频数据采集，而高质量高帧率视频的获取成本高，且难以覆盖开放世界中多样化的场景变化。Texvent 通过引入文本到视频生成，绕过了对真实视频的依赖，从根本上改变了数据来源的约束。

**文本到事件仿真器** 是更直接的竞争者。**Text-to-Events**（Ott et al., NICE 2024）首次尝试从文本提示直接生成事件，但其依赖昂贵的文本-事件对进行训练，缺乏通用性和效率。Texvent 的核心差异在于“训练无关”（training-free）策略：它利用多模态大语言模型的文本到视频生成能力，再通过物理模拟器将视频转换为事件，无需任何文本-事件对的端到端训练。这一设计使其在开放世界场景的适应性和部署效率上具有本质优势。

### 技术演进中的关键改动

Texvent 在继承视频到事件仿真管线框架的同时，对五个关键模块进行了实质性改造：

1. **帧插值策略**：从基于双向光流的自适应插值，改为亮度感知自适应插值（Eq. 4），根据连续帧间的最大对数亮度差动态确定中间帧数量 $K_i = \max(|L(\mathbf{I}_{t_i}) - L(\mathbf{I}_{t_{i+1}})|) \mod \delta$。这使得插值密度与场景运动复杂度自适应匹配，而非依赖光流估计的精度。

2. **对数强度比较**：引入平衡参数 $\alpha$，将标准对数强度差替换为 $L(\alpha + \mathbf{I})$ 形式（Eq. 5, Fig. 3）。这一改动的物理动机是：原始对数函数对低光照变化过于敏感，导致事件激活在暗区和亮区之间严重不平衡。平衡参数通过平移对数函数的输入域，缓解了这种不公平激活。

3. **参考亮度更新机制**：从直接帧间亮度比较，改为基于缓存 $\kappa$ 的电压刷新机制（Eq. 5）。亮度缓存存储那些尚未触发事件的位置的参考亮度值，只有当累积变化超过对比阈值 $\delta$ 时才触发事件并刷新缓存。这模拟了事件相机像素电路的“采样-保持”行为，防止帧间直接比较导致的事件丢失。

4. **噪声注入**：从动态对比度阈值建模背景活动（BA）噪声，改为自适应泊松噪声注入（Eq. 6）。通过掩码 $\mathbf{M}$ 定位低光背景区域，优先在这些区域添加泊松噪声，噪声强度由填充因子 $\lambda_1$ 和传感器参数 $\lambda_2$ 联合控制。这更贴近真实事件相机在低光照下的噪声分布特性。

5. **时间戳重建**：从均匀或压缩时间戳，改为基于亮度变化率的密集时间戳重建（Eq. 7）。每个事件的时间戳 $t^{\mathbf{x}_i}$ 根据其亮度变化率 $\Delta_L^{\mathbf{x}_i}$ 在帧间进行非线性映射，较大亮度变化对应较早的触发时刻。这恢复了事件流中微秒级的时间精度，对下游时序敏感任务至关重要。

### 适用边界与局限性

**适用场景**：Texvent 最适合需要大规模多样化事件数据的开放世界场景，尤其是数据采集成本高昂或物理不可行的情形（如极端光照、危险环境）。其训练无关特性使其可以快速适配新的文本提示分布，无需重新训练。

**已知局限**：

- **视频生成质量瓶颈**：生成的视频质量受限于底层文本到视频模型（如 Cosmos）的性能。当文本提示处于模型分布外时，可能产生视觉伪影，这些伪影会通过物理模拟器传播到事件流中。该局限的严重程度与所选用视频生成模型直接相关，但论文未对不同视频生成模型进行系统性对比。

- **非理想特性建模不完整**：仿真流程未完全模拟事件相机的所有非理想特性，如像素间阈值失配（threshold mismatch）、温度噪声等。这导致仿真事件与真实事件之间仍存在 sim-to-real 差距，尽管消融实验表明缓存机制和平衡参数已显著缩小该差距。

- **实时性限制**：当前实现无法实时生成事件流，因为文本到视频生成和事件模拟需要一定推理时间。尽管单次仿真效率（0.0653 秒，Table 2）已显著优于传统方法，但仍不适用于需要在线事件生成的实时闭环系统。

### 开放问题

论文提出或暗示了以下待解决问题：

1. **可控运动生成**：能否通过条件控制（如运动轨迹、深度图）生成具有可控运动模式的事件流？这将使 Texvent 从“场景级仿真”升级为“运动级仿真”，支持光流估计、目标跟踪等需要精确运动真值的下游任务。

2. **仿真加速**：如何在保持高保真度的同时进一步加速仿真，使其适用于实时闭环系统（如机器人控制）？可能的路径包括轻量化视频生成模型或事件模拟的并行化。

3. **模块可迁移性**：所提的平衡对数参数 $\alpha$ 和亮度缓存机制是否在其他视频生成模型（如 Sora、Stable Video Diffusion）上同样有效？这决定了 Texvent 方法能否从底层视频模型的进步中持续获益。

4. **多模态输入扩展**：是否可以将 Texvent 扩展到多模态输入（如图像+文本），以增强事件仿真的可控性和细粒度？这将使方法从“文本到事件”扩展为“条件到事件”，覆盖更广泛的应用需求。

**需要手动验证的点**：论文未提供 Texvent 与 Text-to-Events（Ott et al., NICE 2024）的直接定量对比，两者在文本到事件任务上的相对优劣需通过额外实验确认。此外，平衡参数 $\alpha$ 的敏感性分析仅在消融研究中定性展示，缺乏不同 $\alpha$ 取值下的定量性能曲线。

## 原文 PDF

![[paperPDFs/CVPR_2026/Texvent_Asynchronous_Event_Data_Simulation_via_Text_Prompt.pdf]]
