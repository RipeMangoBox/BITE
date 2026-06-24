---
title: "SkyEvents: A Large-Scale Event-enhanced UAV Dataset for Robust 3D Scene Reconstruction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SkyEvents_A_Large_Scale_Event_enhanced_UAV_Dataset_for_Robust_3D_Scene_Reconstru_5f0daf32f322.pdf
project_link: "https://openreview.net/forum?id=PQ2zoIZqvm"
code_link: "https://github.com/Anthony-ECPKN/SkyEvent"
aliases:
- GRGCTARWERL
- SkyEvents
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 引入事件相机作为补充模态，利用其高动态范围和高时间分辨率特性，结合几何约束的时间戳对齐（GTA）实现精细的 RGB‑事件同步。
primary_logic: 通过 GTA 模块最大化几何一致性来精确对齐 RGB 与事件流，并设计区域感知的事件渲染损失（RER）约束 3DGS 的亮度变化一致性，从而在低光和模糊条件下显著提升渲染质量和几何精度。
claims:
- 在模糊+低光场景(Scene2)中，加入事件监督的 Improved-GS 将 PSNR 从 25.8635 提升至 26.4789 (+0.6154 dB)，LPIPS 从 0.2653 降至 0.2482 (-0.0171)。
- 定性结果显示事件增强的 Improved-GS 在模糊区域的双重轮廓和鬼影明显减少，细节更清晰。
- 在低光条件下，事件数据为 Luminance-GS 提供了稳定的监督信号，在多个场景中获得 PSNR 提升和 LPIPS 下降。
- SkyEvents Scene2 (Low‑light Blur) 上 PSNR (RGB+Event vs RGB) = 26.4789
---

# SkyEvents: A Large-Scale Event-enhanced UAV Dataset for Robust 3D Scene Reconstruction

> [!tip] 核心洞察
> 通过 GTA 模块最大化几何一致性来精确对齐 RGB 与事件流，并设计区域感知的事件渲染损失（RER）约束 3DGS 的亮度变化一致性，从而在低光和模糊条件下显著提升渲染质量和几何精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | SkyEvents：面向鲁棒三维场景重建的大规模事件增强无人机数据集 |
| 英文题名 | SkyEvents: A Large-Scale Event-enhanced UAV Dataset for Robust 3D Scene Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=dxHPqQindP) · [Code](https://github.com/Anthony-ECPKN/SkyEvent) · [arXiv](https://arxiv.org/abs/2412.01402) · [Project](https://openreview.net/forum?id=PQ2zoIZqvm) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | GTA + RER (Geometry-constrained Timestamp Alignment + Region-wise Event Rendering loss) |
| Dataset | SkyEvents Scene2, SkyEvents Scene1 |

> [!tip] 效果简介
> - SkyEvents Scene2 (Low‑light Blur) 上，PSNR (RGB+Event vs RGB) 26.4789 vs 25.8635 (+0.6154 dB)；LPIPS (RGB+Event vs RGB) 0.2482 vs 0.2653 (-0.0171)。
> - SkyEvents Scene1 (Low‑light Blur) 上，PSNR (RGB+Event vs RGB) 27.4368 vs 27.3554 (+0.0814 dB)。

## 概述

无人机在城市级三维重建中面临的核心瓶颈在于传统 RGB 相机在低光照和运动模糊条件下的动态范围严重不足，导致渲染质量与几何精度大幅下降。事件相机凭借其高动态范围（HDR）和微秒级时间分辨率，天然适合补充这一短板，但现有事件增强无人机数据集普遍缺乏同步的高分辨率 RGB、稠密深度真值和精确的 6-DoF 位姿，无法为城市规模重建提供完整的监督信号。

针对这一问题，SkyEvents 提出了一个大规模事件增强无人机数据集，包含 **45 条序列、超过 8 小时**的配对 RGB 与事件数据，覆盖 **0.72 km²** 的点云真值，并提供 120 Hz 的 RGB 图像、深度图、几何真值及 6-DoF 位姿（Table 1）。在数据层面，作者设计了**几何约束时间戳对齐（GTA）** 模块，通过最大化 RGB 帧与事件帧之间的几何一致性得分，实现精细的跨模态时间同步。在方法层面，引入**区域感知事件渲染损失（RER）**，在 RGB 与事件传感器的重叠区域内约束合成对数亮度变化与累积事件帧的一致性，从而将事件信号作为额外的监督源嵌入 3D Gaussian Splatting（3DGS）重建管线。

实验表明，事件增强策略在模糊与低光场景下带来了稳定的性能增益。以 Improved-GS 为基线，在低光模糊的 Scene2 中，加入事件监督后 **PSNR 从 25.86 dB 提升至 26.48 dB（+0.62 dB），LPIPS 从 0.265 降至 0.248**（Table 2）。定性结果进一步显示，事件增强有效抑制了模糊区域的双重轮廓和鬼影伪影（Figure 4）。在 Luminance-GS 基线上同样观察到一致的提升趋势，验证了事件模态对复杂光照条件下 3DGS 重建的通用辅助能力。

**方法定位**：SkyEvents 在方法谱系上处于事件驱动 3D 重建与 3D Gaussian Splatting 的交叉点。其核心贡献并非提出全新的重建架构，而是通过 **GTA + RER** 这一轻量、即插即用的同步与损失模块，将事件数据有效注入现有 3DGS 基线（如 Improved-GS 和 Luminance-GS），在不改变主干网络的前提下显著提升对退化条件的鲁棒性。这一设计思路与利用多模态信号增强神经渲染的主流趋势一致，但将焦点从传统的曝光或去模糊后处理前移至数据同步与损失函数层面。

**主要局限**：当前 RGB 与事件相机之间尚未实现完美的时空同步；低光评估采用合成数据（伽马校正与线性缩放），而非真实低光采集；实验仅在合成退化条件下进行，缺乏真实极端环境的验证。这些因素限制了结论向实际部署的直接外推能力。

## 背景与动机

无人机（UAV）搭载的视觉感知系统在城市建模、灾害评估、基础设施巡检等任务中扮演着日益关键的角色。基于多视角图像的3D重建与新型视图合成，尤其是以3D Gaussian Splatting（3DGS）为代表的显式辐射场方法，已展现出卓越的渲染质量与实时性能。然而，现有无人机视觉系统几乎完全依赖传统RGB相机，其固有的物理局限正构成大规模城市场景鲁棒重建的核心瓶颈。

**核心瓶颈：低动态范围与运动模糊。** RGB相机在低光照环境下信噪比急剧下降，而在高速飞行或快速机动中又不可避免地产生运动模糊。这两种退化在无人机航拍中往往同时出现——例如黄昏时分的城市巡检——导致图像丢失关键的纹理与几何信息。传统去模糊或低光增强方法属于后处理，无法恢复已丢失的场景细节，从根本上限制了3DGS等方法的渲染保真度与几何精度。

**事件相机的互补优势。** 神经形态事件相机以异步方式感知每像素的亮度变化，具备微秒级时间分辨率（> 10 kHz）和极高的动态范围（> 120 dB），天然对运动模糊和极端光照不敏感。将事件流作为补充模态引入3D重建管线，有望在RGB失效的场景中提供稳定的监督信号。然而，这一融合面临两个关键挑战：其一，RGB相机与事件相机之间的精确时空对齐；其二，如何将异步的事件信号转化为适合监督辐射场优化的损失函数。

**现有数据集的缺口。** 尽管已有若干面向事件驱动视觉的数据集（如MVSEC、DSEC），但它们缺乏面向无人机3D重建的关键要素：同步的高分辨率RGB图像（≥ 120 Hz）、稠密深度真值、准确的6自由度位姿，以及覆盖城市级尺度的大范围场景。如Table 1所示，SkyEvents是首个同时提供上述全部模态的大规模事件增强无人机数据集，包含45个序列、超过8小时的配对RGB-事件数据，以及覆盖0.72 km²的稠密点云真值。

**本文动机。** 为填补上述空白，本文构建了SkyEvents数据集，并提出几何约束的时间戳对齐模块（GTA）与区域感知事件渲染损失（RER），将事件相机的高动态范围与高时间分辨率特性系统性地融入3DGS重建管线。核心假设是：通过最大化RGB帧与事件帧之间的几何一致性来实现精确同步，并在渲染优化中约束合成亮度变化与累积事件图像的一致性，可以在低光和模糊条件下显著提升渲染质量与几何精度。

## 核心创新

SkyEvents 的核心创新并非提出一个全新的重建架构，而是为 **3D Gaussian Splatting (3DGS)** 管线引入了**事件相机模态**，并通过两个关键模块解决了多模态融合中的时空对齐与监督信号设计问题。其创新本质可归结为两个 **changed slots**：**输入模态的扩展** 与 **损失函数的重新设计**。

### 1. 输入模态扩展：从纯 RGB 到 RGB‑事件同步流

传统 3DGS 基线（如 **Improved‑GS** (Deng et al., 2025) 和 **Luminance‑GS** (Cui et al., 2025)）仅依赖 RGB 图像作为输入。在低光或运动模糊条件下，RGB 传感器有限的动态范围和曝光时间导致图像信息严重退化，使重建质量大幅下降。

SkyEvents 将**事件相机**作为互补模态引入。事件相机具有高动态范围（>120 dB）和微秒级时间分辨率，能够捕捉场景中快速的亮度变化，且不受运动模糊影响。然而，事件数据与 RGB 帧之间存在时空不对齐问题——两种传感器的触发时刻、视场角均存在差异，直接融合会导致监督信号错位。

为解决这一瓶颈，论文提出了 **GTA（Geometry‑constrained Timestamp Alignment）模块**。其核心机制如下：

1. **局部时间戳选择**：对于每帧 RGB 图像 $I_{t_k}$，在其时间戳 $t_k$ 附近的对称搜索窗口 $\mathcal{T}_k = \{t_k - \Delta, t_k - \Delta + \delta, \ldots, t_k + \Delta\}$ 内，选择使几何一致性得分 $S$ 最大的事件时间 $\tau_k^\star$（公式 1）：
   $$\tau_k^\star \in \arg\max_{\tau \in \mathcal{T}_k} S(I_{t_k}, E_\tau)$$

2. **几何一致性度量**：通过鲁棒的单应矩阵 $\mathbf{H}$ 将 RGB 像素映射到事件像素（公式 2），然后基于内点数量与归一化重投影误差的加权组合计算得分（公式 3）：
   $$S(I_{t_k}, E_\tau) = \sum_{i=1}^{N} m_i - \alpha \frac{\sum_{i=1}^{N} m_i \varepsilon_i}{\max(1, \sum_{i=1}^{N} m_i)}$$
   其中 $m_i$ 为内点指示，$\varepsilon_i$ 为重投影误差，$\alpha > 0$ 为平衡系数。

3. **全局时序精化**：在序列级别联合优化所有事件时间戳，在最大化几何一致性之和的同时，惩罚偏离 1 秒均匀间隔的时序漂移（公式 4）：
   $$\{\widetilde{\tau}_k\}_{k=1}^{K} = \arg\max_{\{\tau_k\}} \left[ \sum_{k=1}^{K} S(I_{t_k}, E_{\tau_k}) - \beta \sum_{k=2}^{K} |(\tau_k - \tau_{k-1}) - 1\text{s}| \right]$$

通过 GTA 模块，事件流与 RGB 帧之间建立了像素级的时空对应关系，为后续的监督信号设计奠定了基础。

### 2. 损失函数设计：区域感知事件渲染损失 (RER)

标准 3DGS 的损失函数通常由 L1 和 SSIM 组成，仅约束渲染图像与真实 RGB 图像之间的一致性。当 RGB 图像因模糊或低光而质量下降时，这种像素级监督本身已不可靠。

SkyEvents 提出的 **RER（Region‑wise Event Rendering）损失** 直接利用事件数据监督渲染过程。其设计逻辑如下：

- **事件帧累积**：在时间区间 $(t_1, t_2)$ 内累加事件极性 $p_i$，形成近似对数亮度变化的二维事件帧（公式 5）：
  $$\bar{E}(t_1, t_2)(\mathbf{x}) = \sum_{t_1 < t_i < t_2} p_i \ \mathbf{1}[\mathbf{x}_i = \mathbf{x}]$$

- **亮度变化一致性约束**：在 RGB 和事件传感器的**重叠区域**内，约束 3DGS 渲染的两帧对数亮度差与累积事件帧一致（公式 6）：
  $$\mathcal{L}_{\text{event}} = \Big\| \big( \log \mathcal{C}_{\pmb\theta}(\hat{I}_{t_2}) - \log \mathcal{C}_{\pmb\theta}(\hat{I}_{t_1}) \big) - \bar{E}(t_1, t_2) \Big\|_2^2$$
  其中 $\mathcal{C}_{\pmb\theta}$ 为辐射映射函数，$\hat{I}_{t}$ 为渲染图像。

这一设计的**关键洞察**在于：事件相机记录的是**亮度变化的相对量**，而非绝对强度。因此 RER 损失不要求渲染图像与退化 RGB 完全一致，而是要求渲染的**亮度变化模式**与事件流一致。这使得事件信号在 RGB 图像质量极差（如严重模糊）时，仍能提供稳定、可靠的监督。

### 3. 创新的因果机制

两项 changed slots 形成了一条清晰的因果链：

> **GTA 对齐** → 建立 RGB 与事件的精确时空对应 → **RER 损失** 在重叠区域约束亮度变化一致性 → 3DGS 在低光/模糊条件下获得额外几何与光度监督 → **渲染质量与几何精度提升**

实验证据表明，在模糊+低光场景 (Scene2) 中，加入事件监督的 Improved‑GS 将 PSNR 从 25.8635 提升至 26.4789（+0.6154 dB），LPIPS 从 0.2653 降至 0.2482（-0.0171）（Table 2）。定性结果进一步显示，事件增强后模糊区域的双重轮廓和鬼影明显减少（Figure 4）。

### 4. 方法的局限性与开放问题

尽管创新点明确，但以下方面需要关注：

- **合成低光数据的局限性**：评估中的低光图像是通过伽马校正和线性缩放从正常光照图像合成的（$L_t(p) = \beta \times (\alpha \times I_t(p))^\gamma$），而非真实低光采集。RER 损失在真实极端低光下的有效性尚需验证。
- **时空同步的硬件瓶颈**：GTA 模块通过后处理优化时间戳对齐，但 RGB 与事件相机之间尚未实现完美的硬件级同步，这可能在高动态场景中引入残余误差。
- **开放问题**：事件增强 3DGS 能否扩展到动态场景？GTA 能否适应更灵活的传感器配置（如不同 FOV 或异步曝光）？这些方向需要进一步探索。

## 整体框架

SkyEvents 的整体框架围绕“多模态数据采集 → 时空同步 → 事件增强三维重建”三条主线展开，核心目标是利用事件相机的高动态范围和高时间分辨率特性，弥补传统 RGB 相机在低光和运动模糊条件下的不足，从而提升无人机航拍场景的三维重建质量。

### 数据采集与传感器套件

系统硬件平台以 DJI Matrice 350 RTK 无人机为载体（图 8），搭载一套同步传感器套件，包括一台 120 Hz 高帧率 RGB 相机、一台事件相机、一台激光雷达（LiDAR）以及一台机载 Mini PC 用于实时数据记录。传感器通过定制碳纤维板刚性固定，并由电源转换模块统一供电。飞行任务通过预加载 KML 航线实现全自主飞行，覆盖校园内五个不同场景区域（图 10），包括主楼群、宿舍区、数据中心、运动场等，涵盖多种光照条件和飞行高度。

### GTA 模块：几何约束的时间戳对齐

由于 RGB 相机与事件相机之间缺乏硬件级同步，原始数据存在时间戳偏差。为此，论文提出 **GTA（Geometry-constrained Timestamp Alignment）模块**，以几何一致性最大化为目标实现精细的 RGB‑事件时间对齐。

具体流程如下：

1. **逐帧时间戳选择**：对于每一帧 RGB 图像 $I_{t_k}$，在以 $t_k$ 为中心的对称时间窗口 $\mathcal{T}_k = \{t_k - \Delta, t_k - \Delta + \delta, \ldots, t_k + \Delta\}$ 内搜索事件帧 $E_\tau$，选择使几何一致性得分 $S(I_{t_k}, E_\tau)$ 最大的事件时间戳 $\tau_k^\star$：

   $$\tau_k^\star \in \arg\max_{\tau \in \mathcal{T}_k} S(I_{t_k}, E_\tau)$$

2. **单应映射**：利用 MAGSAC 估计鲁棒的单应矩阵 $\mathbf{H}$，将 RGB 像素映射到事件像素坐标系：

   $$\lambda [\boldsymbol{v}] = \mathbf{H} [\boldsymbol{v}'], \quad \lambda \neq 0$$

3. **几何一致性得分**：根据内点数量与归一化重投影误差的加权组合定义得分函数，$\alpha > 0$ 为平衡系数：

   $$S(I_{t_k}, E_\tau) = \sum_{i=1}^{N} m_i - \alpha \frac{\sum_{i=1}^{N} m_i \varepsilon_i}{\max(1, \sum_{i=1}^{N} m_i)}$$

4. **全局时间戳精化**：在序列级别联合优化所有事件时间戳，最大化几何一致性得分之和，同时惩罚偏离 1 秒均匀间隔的时序漂移（$\beta > 0$ 控制惩罚强度）：

   $$\{\widetilde{\tau}_k\}_{k=1}^{K} = \arg\max_{\{\tau_k\}} \left[ \sum_{k=1}^{K} S(I_{t_k}, E_{\tau_k}) - \beta \sum_{k=2}^{K} \big| (\tau_k - \tau_{k-1}) - 1\mathrm{s} \big| \right]$$

该模块的输出是经过精细对齐的 RGB‑事件时间戳对应关系，为后续事件监督渲染提供了可靠的数据基础。

### 三维重建管线与 RER 损失

重建管线以 **3D Gaussian Splatting（3DGS）** 为骨干网络，采用显式高斯表示与可微渲染。在标准 3DGS 的渲染损失（L1 + SSIM）之外，引入 **RER（Region-wise Event Rendering）损失**，利用对齐后的事件数据提供额外监督信号。

RER 损失的核心机制如下：

1. **事件帧累积**：在时间区间 $(t_1, t_2)$ 内累加事件极性 $p_i$，形成近似对数亮度变化的二维事件帧：

   $$\bar{E}(t_1, t_2)(\mathbf{x}) = \sum_{t_1 < t_i < t_2} p_i \ \mathbf{1}[\mathbf{x}_i = \mathbf{x}]$$

2. **区域感知损失计算**：在 RGB 与事件传感器的重叠区域内，计算合成对数亮度差与累积事件帧之间的 L2 损失：

   $$\mathcal{L}_{\mathrm{event}} = \Big\| \Big( \log \mathcal{C}_{\boldsymbol{\theta}}(\hat{I}_{t_2}) - \log \mathcal{C}_{\boldsymbol{\theta}}(\hat{I}_{t_1}) \Big) - \bar{E}(t_1, t_2) \Big\|_2^2$$

   其中 $\mathcal{C}_{\boldsymbol{\theta}}$ 表示将渲染图像裁剪至重叠区域的算子，$\hat{I}_{t_1}$ 和 $\hat{I}_{t_2}$ 为 3DGS 在相邻时间戳的渲染结果。

### 输入输出流总结

- **输入**：120 Hz RGB 图像序列、事件流、LiDAR 点云与位姿。
- **GTA 模块**：输出对齐后的事件时间戳，实现 RGB‑事件像素级对应。
- **3DGS 重建**：以 RGB 图像和 LiDAR 位姿为输入，通过可微渲染生成新视角图像。
- **RER 损失**：将对齐后的事件帧作为监督信号，约束渲染亮度变化与真实事件记录一致，从而在低光和模糊条件下提升渲染质量与几何精度。

整个框架的模块关系和数据流如图 2 所示：数据采集平台输出配对的 RGB 与事件数据，经 GTA 模块同步时间戳并完成空间对齐后，送入 3DGS 重建管线，最终由 RGB 渲染损失与 RER 事件损失联合优化。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/011_Figure_8.jpg]]
*Figure 8: Multi-modal UAV data collection platform overview. The DJI Matrice 350 RTK is equipped with a synchronized sensor suite and An onboard mini-PC*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/014_Figure_9.jpg]]
*Figure 9: Key components of the UAV data collection system. (a) Custom carbon fiber plate provides rigid mounting for sensors and computing unit while damping vibrations. (b) Power conversion module regulates DJI battery output to stable 12V/5V for onboard electronics. (c) Remote controller with pre-loaded KML routes enables fully autonomous flight operations*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/015_Figure_10.jpg]]
*Figure 10: Campus region overview. The map shows five distinct areas: (1) Main Building complex, (2) North Dormitory, (3) Data Center, (4) Playground, and (5) South Dormitory, covering diverse urban scenarios for multi-modal data collection*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/003_Figure_2.jpg]]
*Figure 2: Data collection and rendering pipelines. The data acquisition platform consists of an UAV payload, an event camera, a 120HZ RGB camera, and a Mini PC. After collecting paired RGB and event data, we utilized the proposed GTA module to synchronize timestamps and warp between the event and RGB cameras*

## 核心模块与公式推导

SkyEvents 并未提出全新的三维重建架构，而是在现有 3D Gaussian Splatting（3DGS）框架之上，通过两个关键模块引入事件模态的监督信号：**几何约束时间戳对齐（GTA）** 和 **区域感知事件渲染损失（RER）**。两者分别解决了事件数据与 RGB 数据的时间同步问题，以及如何将异步、稀疏的事件流转化为对 3DGS 渲染过程的有效约束。

### GTA：几何约束的时间戳对齐

事件相机与 RGB 相机之间存在时间戳异步，这是多模态融合的首要障碍。GTA 模块的核心思想是：将时间同步问题转化为一个几何一致性最大化问题。对于每一帧 RGB 图像 $I_{t_k}$，在其时间戳 $t_k$ 附近的对称搜索窗口 $\mathcal{T}_k$ 内，寻找一个事件时间 $\tau_k^\star$，使得该时刻的事件帧与 RGB 图像之间的几何一致性得分 $S$ 最高：

$$\tau _ { k } ^ { \star } \in \arg \operatorname* { m a x } _ { \tau \in \mathcal { T } _ { k } } S \big ( I _ { t _ { k } } , E _ { \tau } \big ) , \qquad \mathcal { T } _ { k } = \{ t _ { k } - \Delta , t _ { k } - \Delta + \delta , \ldots , t _ { k } + \Delta \} \tag{1}$$

其中 $\Delta$ 为搜索窗口半径，$\delta$ 为搜索步长。这里的“事件帧”$E_\tau$ 是通过在极短时间窗口内累积事件极性得到的二维表示，用于提取与 RGB 图像可匹配的几何特征。

由于事件相机与 RGB 相机的视场（FOV）不同，直接进行特征匹配并不可行。GTA 采用鲁棒的单应矩阵 $\mathbf{H}$ 将 RGB 像素 $\boldsymbol{v}'$ 映射到事件像素 $\boldsymbol{v}$：

$$\lambda \left[ { \boldsymbol { v } } \right] = \mathbf { H } \left[ { \boldsymbol { v } } ^ { \prime } \right] , \qquad \lambda \neq 0 \tag{2}$$

单应矩阵通过 MAGSAC 鲁棒估计算法获得，能够有效处理外点干扰。

几何一致性得分 $S$ 的定义综合考虑了内点数量与重投影误差：

$$S \big ( I _ { t _ { k } } , E _ { \tau } \big ) = \sum _ { i = 1 } ^ { N } m _ { i } \ - \ \alpha \frac { \sum _ { i = 1 } ^ { N } m _ { i } \varepsilon _ { i } } { \operatorname* { m a x } \big ( 1 , \sum _ { i = 1 } ^ { N } m _ { i } \big ) } , \qquad \alpha > 0 \tag{3}$$

其中 $m_i \in \{0, 1\}$ 表示第 $i$ 个匹配点是否为内点，$\varepsilon_i$ 为重投影误差，$\alpha$ 为惩罚系数。该得分的直观含义是：内点越多、重投影误差越小，几何一致性越高。

逐帧独立匹配后，GTA 进一步执行全局时间戳优化。考虑到无人机航拍数据通常以固定帧率采集，相邻帧的时间间隔应接近 1 秒，全局优化在最大化几何一致性得分的同时，对偏离标准间隔的时序漂移施加惩罚：

$$\{ \widetilde { \tau } _ { k } \} _ { k = 1 } ^ { K } = \arg \operatorname* { m a x } _ { \{ \tau _ { k } \} } \left[ \sum _ { k = 1 } ^ { K } S \big ( I _ { t _ { k } } , E _ { \tau _ { k } } \big ) - \beta \sum _ { k = 2 } ^ { K } \big | ( \tau _ { k } - \tau _ { k - 1 } ) - 1 \mathrm { s } \big | \right] , \qquad \beta > 0 \tag{4}$$

其中 $\beta$ 控制时序一致性惩罚的权重。通过这一全局优化步骤，GTA 能够纠正逐帧匹配可能产生的局部错位，输出全局一致的时间对齐结果。

### RER：区域感知事件渲染损失

时间对齐完成后，事件数据被转化为可监督 3DGS 渲染的损失函数。首先，在时间区间 $(t_1, t_2)$ 内，将事件极性 $p_i$ 按像素位置 $\mathbf{x}$ 累加，形成近似对数亮度变化的二维事件帧：

$$\bar { E } ( t _ { 1 } , t _ { 2 } ) ( \mathbf { x } ) = \sum _ { \substack { t _ { 1 } < t _ { i } < t _ { 2 } } } p _ { i } \ \mathbf { 1 } [ \mathbf { x } _ { i } = \mathbf { x } ] \tag{5}$$

其中 $p_i \in \{-1, +1\}$ 表示亮度下降或上升事件，$\mathbf{1}[\cdot]$ 为指示函数。该累积帧反映了区间内的亮度变化趋势。

RER 损失的核心设计在于：它仅在 RGB 与事件传感器的**重叠区域**内计算约束。令 $\mathcal{C}_{\theta}(\hat{I}_t)$ 为 3DGS 在时间 $t$ 渲染的图像经裁剪到重叠区域后的结果，则事件损失定义为合成对数亮度差与累积事件帧之间的 L2 范数：

$$\mathcal { L } _ { \mathrm { e v e n t } } = \Big \| \Big ( \log \mathcal { C } _ { \pmb \theta } ( \hat { I } _ { t _ { 2 } } ) - \log \mathcal { C } _ { \pmb \theta } ( \hat { I } _ { t _ { 1 } } ) \Big ) - \bar { E } ( t _ { 1 } , t _ { 2 } ) \Big \| _ { 2 } ^ { 2 } \tag{6}$$

该损失直接约束 3DGS 渲染的亮度变化与事件相机记录的变化一致。由于事件相机天然具有高动态范围和对数响应特性，这一约束在低光和运动模糊区域尤为有效——这些区域正是传统 RGB 光度损失失效的场景。

### 模块间的因果链路

GTA 和 RER 构成了一个因果闭环：GTA 提供精确的时间对齐，使得事件帧 $\bar{E}(t_1, t_2)$ 与 RGB 渲染对 $(\hat{I}_{t_1}, \hat{I}_{t_2})$ 能够按像素对应；RER 则将这种对应转化为对 3DGS 优化过程的梯度信号。值得注意的是，RER 被设计为一种**即插即用**的损失项，可以与标准 3DGS 的 L1 和 SSIM 损失联合使用，且论文在 **Improved-GS**（Deng et al., 2025）和 **Luminance-GS**（Cui et al., 2025）两个不同基线上均验证了其有效性。

### 关键局限

需要指出的是，公式 (6) 中的事件监督依赖于合成对数亮度差，而事件相机的实际响应并非严格对数线性。论文未对这一近似引入的系统偏差进行定量分析。此外，当前 GTA 模块假设 RGB 与事件相机之间的单应变换是静态的，在无人机剧烈姿态变化时可能存在对齐误差——这一点在论文的局限性讨论中未被充分展开，需读者自行评估。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/016_Figure_11.jpg]]
*Figure 11: Matching results with the proposed GTA module on SkyEvents and MVSEC datasets*

## 实验与分析

### 实验设置与评估协议

论文在自建的大规模事件增强无人机数据集 **SkyEvents** 上验证所提方法的有效性。该数据集包含 45 条序列、超过 8 小时的同步 RGB 与事件数据，以及覆盖 0.72 km² 的稠密点云真值（Table 1）。评估涵盖多种光照条件（正常、低光）与成像质量（清晰、模糊），以全面考察事件模态对 3D 重建的增益。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/002_Table_1.jpg]]
*Table 1: Comparison of SkyEvents with previous event-based UAV datasets*

基线方法选用两类 3D Gaussian Splatting 变体：通用基线 **Improved-GS**（Deng et al., 2025）和面向复杂光照的 **Luminance-GS**（Cui et al., 2025）。所有实验均在 NVIDIA RTX 4090 上运行，统一使用 Adam 优化器训练 30000 次迭代，事件细化损失从第 8000 次迭代开始介入，确保对比公平。低光图像通过伽马校正与线性缩放从正常光照帧合成，以保持像素级对应关系。

评估指标采用 PSNR、SSIM 和 LPIPS，分别衡量渲染图像的保真度、结构相似性和感知质量。

### 主要结果

Table 2 汇总了在不同场景与条件下，加入事件监督前后的渲染性能对比，核心发现如下：

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/005_Table_2.jpg]]
*Table 2: Rendering performance comparison across different conditions and scenarios, with and without event data*

**模糊场景的去模糊增益最为显著。** 在低光模糊的 Scene2 中，Improved-GS 引入事件监督后 PSNR 从 25.8635 提升至 26.4789（+0.6154 dB），LPIPS 从 0.2653 降至 0.2482（-0.0171）。这表明事件相机的高时间分辨率特性有效补偿了 RGB 帧的运动模糊信息损失，使渲染结果的双重轮廓和鬼影明显减少（Figure 4）。

**低光场景下事件数据提供稳定的亮度变化监督。** 在低光模糊的 Scene1 中，Improved-GS 的 PSNR 从 27.3554 提升至 27.4368（+0.0814 dB）。对于 Luminance-GS，事件监督在多个场景中均带来一致的 PSNR 提升和 LPIPS 下降，说明事件模态为低光条件下的亮度变化建模提供了可靠的约束信号。

**事件监督的增益具有跨方法泛化性。** 无论基于 Improved-GS 还是 Luminance-GS，加入 RER 事件损失后所有场景的 PSNR 均提升、LPIPS 均下降，证明所提区域感知事件渲染损失是一种即插即用的通用增强策略。

### 消融分析

消融实验的核心结论是：**RER 事件损失在所有场景和基线方法上均带来正向收益，且对模糊场景的去模糊效果尤为突出**（Table 2）。移除事件损失后，模糊区域的渲染质量显著退化，表现为边缘模糊、细节丢失和伪影增多。这验证了事件数据在补偿 RGB 运动模糊方面的不可替代性。

### 事件到视频重建方法的域迁移局限性

Table 3 和 Figure 7 展示了多种事件到视频重建方法（E2VID+、FireNet、SSL-E2VID 等）在 SkyEvents 上的表现。结果表明，**这些方法在从地面数据迁移到无人机航拍事件流时性能显著下降**。原因在于无人机视角的大范围深度变化、快速运动和独特场景纹理与地面数据集存在显著分布差异，现有方法缺乏对航拍场景的适配能力。这一发现进一步凸显了 SkyEvents 作为事件增强无人机视觉基准的价值。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/009_Table_3.jpg]]
*Table 3: Quantitative comparison of event-to-video methods*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/010_Figure_7.jpg]]
*Figure 7: Video reconstruction performance comparison: E2VID+ (Stoffregen et al., 2020), FireNet (Scheerlinck et al., 2020), and SSL-E2VID (Paredes-Valles & De Croon, 2021). ´*

### 深度估计

Figure 6 展示了深度估计的可视化结果。事件增强的 3DGS 在模糊和低光区域能够恢复出更清晰的深度边界，与 RGB 渲染质量的提升趋势一致。然而，当前深度估计仍依赖 3DGS 的隐式几何，缺乏专门针对无人机航拍大范围深度变化的显式优化机制。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/008_Figure_6.jpg]]
*Figure 6: Depth Estimation*

### 局限性与失败模式

尽管事件增强带来了全面的性能提升，但以下局限性值得关注：

1. **时空同步精度受限。** 由于当前硬件限制，RGB 与事件相机之间尚未实现完美的时空同步，残余的时空偏差可能在快速运动场景中引入额外的对齐误差。
2. **低光评估为合成数据。** 实验中的低光图像通过伽马校正和线性缩放合成，而非真实低光采集数据，因此事件监督在真实极端低光环境下的增益幅度有待进一步验证。
3. **未在真实极端环境中验证。** 目前的实验仅在合成模糊和低光条件下进行，缺乏真实暴雨、浓雾或夜间等极端环境下的鲁棒性评估。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/006_Figure_4.jpg]]
*Figure 4: Comparison of 3D scene reconstruction with Improved-GS and Improved-GS+RER in blurred environments*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_dxHPqQindP/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of 3D scene reconstruction using existing 3D GS methods (Improved-GS and Luminance-GS), with and without event enhancement. The integration of event modality through RER markedly enhances rendering quality*

## 方法谱系与知识库定位

### 1. 基线方法定位

本工作以两类 3D Gaussian Splatting (3DGS) 方法为基线，验证事件增强的泛化有效性：

- **Improved‑GS** (Deng et al., 2025)：通用 3DGS 变体，面向标准场景重建，仅依赖 RGB 图像与标准渲染损失（L1 + SSIM）。在 SkyEvents 的低光模糊场景中，其纯 RGB 版本出现明显的双重轮廓与鬼影（Figure 4），PSNR 在 Scene2 仅为 25.86 dB。
- **Luminance‑GS** (Cui et al., 2025)：针对复杂光照条件设计的 3DGS 变体，具备一定的光照鲁棒性，但在极端低光下仍缺乏稳定的监督信号。引入事件后，其在多个场景中获得一致的 PSNR 提升与 LPIPS 下降（Table 2）。

两类基线均未使用事件模态，因此本工作的核心贡献在于提出一种**与具体 3DGS 骨干解耦的事件增强策略**——通过 GTA 对齐模块与 RER 损失函数，将事件流转化为可插拔的监督信号。

### 2. 方法谱系中的位置

本工作处于**事件相机辅助的三维重建**与**3D Gaussian Splatting**的交叉地带，其技术路径可沿以下维度定位：

**（1）事件到视频重建 → 事件增强 3DGS**

传统事件重建方法（如 E2VID+、FireNet、SSL‑E2VID）致力于从纯事件流恢复灰度视频帧，再输入下游重建管线。SkyEvents 的实验表明，这些方法在无人机航拍场景中泛化能力严重退化（Table 3, Figure 7）——地面训练的模型难以适应高空视角、大范围深度变化和快速运动。本工作绕过“事件→视频”的中间重建步骤，直接在 3DGS 的可微渲染管线中注入事件约束（RER 损失），避免了级联误差。

**（2）多模态对齐 → GTA 模块**

事件与 RGB 的时空对齐是多模态 3D 重建的前提。现有数据集（如 MVSEC）依赖硬件同步，限制了传感器选型灵活性。GTA 模块通过**最大化几何一致性得分**实现软件级时间戳对齐（Eq 1–4），将搜索窗口内的单应映射质量作为同步度量，并在全局优化中惩罚时序漂移。这一设计使得 GTA 可适配不同 FOV 和异步曝光的传感器配置，降低了硬件门槛。

**（3）3DGS 损失函数设计 → RER 损失**

标准 3DGS 的渲染损失仅约束 RGB 空间的像素级一致性。RER 损失（Eq 6）将事件相机的**对数亮度变化**建模为监督目标：在 RGB 与事件传感器的重叠区域内，约束合成视图的对数亮度差与累积事件帧之间的 L2 一致性。这一设计利用了事件相机的高动态范围特性，在模糊和低光区域提供了传统 RGB 损失无法给出的梯度信号。

### 3. 适用边界与局限

基于论文公开信息，本方法的适用边界与已知局限如下：

| 维度 | 边界描述 | 证据强度 |
|------|----------|----------|
| **时空间同步** | 当前硬件条件下，RGB 与事件相机尚未实现完美的时空间同步（GTA 仅缓解而非根除）。 | 论文自述局限 |
| **低光评估真实性** | 实验中的低光图像通过伽马校正和线性缩放合成（$L_t(p) = \beta \times (\alpha \times I_t(p))^\gamma$），而非真实低光采集。 | 论文自述局限 |
| **模糊评估真实性** | 模糊场景通过合成方式生成，未在真实极端环境（如暴风雨、沙尘）中验证。 | 论文自述局限 |
| **动态场景** | 当前实验限于静态场景重建，未涉及动态物体或长时序序列。 | 开放问题 |
| **传感器配置泛化** | GTA 在不同 FOV 或异步曝光配置下的精度保持能力尚未充分验证。 | 开放问题 |

**需要人工验证的点**：论文未报告 GTA 模块在不同场景下的同步精度量化指标（如时间误差的均值/方差），仅展示了定性匹配结果（Figure 11）。该模块的实际鲁棒性需要在更多样化的采集条件下独立评估。

### 4. 开放问题

1. **真实极端环境验证**：事件增强 3DGS 在真实户外低光（非合成）和真实运动模糊场景下的提升幅度尚不明确。合成评估可能高估事件监督的收益。
2. **深度估计的扩展**：当前事件辅助的深度估计（Figure 6）在无人机航拍的大范围深度变化场景中仍有明显误差，如何改进事件引导的单目深度估计以适应高空视角是重要方向。
3. **GTA 的通用性边界**：GTA 模块依赖特征匹配与单应估计，在纹理稀疏或重复纹理场景（如大面积草坪、水面）中可能失效，其退化条件需要系统研究。
4. **动态场景与长时序**：将事件增强 3DGS 扩展到包含运动物体的动态场景，以及更长的时序序列（如数十分钟的连续飞行），是迈向实际部署的关键一步。

## 原文 PDF

![[paperPDFs/ICLR_2026/SkyEvents_A_Large_Scale_Event_enhanced_UAV_Dataset_for_Robust_3D_Scene_Reconstru_5f0daf32f322.pdf]]