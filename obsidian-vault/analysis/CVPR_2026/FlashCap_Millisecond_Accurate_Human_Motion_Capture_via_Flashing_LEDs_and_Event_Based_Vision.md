---
title: "FlashCap: Millisecond-Accurate Human Motion Capture via Flashing LEDs and Event-Based Vision"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlashCap_Millisecond_Accurate_Human_Motion_Capture_via_Flashing_LEDs_and_Event_Based_Vision.pdf
project_link: null
code_link: null
aliases:
- FlashCap
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用搭载闪烁LED的运动捕捉服与事件相机的组合，通过为每个LED分配独特的通断时间模式，直接从事件流中提取1000 Hz的关节位置，绕过传统光学系统的帧率瓶颈。
primary_logic: 将每个LED的身份编码进高频率的闪烁模式中，事件相机异步捕捉的光强变化不仅能定位LED，还能通过极性变化周期识别LED的唯一标识，从而自动标注毫秒级真值。
claims:
- 自动标注管线达到99.99%的精确率和98.82%的召回率，性能接近人工标注。
- 在FlashMotion数据集上，ResPose相比标准RGB插值将MPJPE降低约40%，并取得5.66的MPJPE和0.99的PCK0.5。
- ResPose在精准动作计时任务中实现击拳4.8 ms、踢腿7.2 ms、跳跃6.5 ms的平均时间误差。
- FlashMotion (PMT) 上 Mean Error of Estimated Time (ms) – Punching = 4.8
---

# FlashCap: Millisecond-Accurate Human Motion Capture via Flashing LEDs and Event-Based Vision

> [!tip] 核心洞察
> 将每个LED的身份编码进高频率的闪烁模式中，事件相机异步捕捉的光强变化不仅能定位LED，还能通过极性变化周期识别LED的唯一标识，从而自动标注毫秒级真值。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlashCap：基于闪烁LED和事件视觉的毫秒级人体运动捕捉 |
| 英文题名 | FlashCap: Millisecond-Accurate Human Motion Capture via Flashing LEDs and Event-Based Vision |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.19770) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ResPose |
| Dataset | FlashMotion |

> [!tip] 效果简介
> - FlashMotion (PMT) 上，Mean Error of Estimated Time (ms) – Punching 4.8 vs N/A (N/A)；Mean Error of Estimated Time (ms) – Kicking 7.2 vs N/A (N/A)；Mean Error of Estimated Time (ms) – Jumping 6.5 vs N/A (N/A)。
> - FlashMotion (High Temporal Resolution HPE) 上，MPJPE 5.66 vs ~9.4 (standard RGB interpolation, inferred from ~40% reduction) (~40% reduction)；PCK0.5 0.99 vs N/A (N/A)。

## 概要

现有运动捕捉数据集受限于传统RGB相机的帧率（30–60 Hz），无法为毫秒级精确动作计时（Precise Motion Timing, PMT）提供高于120 Hz的真值标注；高速相机虽可解决帧率问题，但其高昂成本与巨大带宽需求使其难以在常规环境中部署。这一瓶颈直接制约了体育分析、康复评估等需要亚毫秒动作时序的应用。

FlashCap 通过**闪烁LED与事件相机**的组合打破上述限制。其核心思路是：在运动捕捉服上搭载多个LED，为每个LED分配独特的通断时间模式，将身份信息直接编码进高频闪烁信号中；事件相机异步捕捉光强变化，不仅能定位LED，还能通过极性变化周期识别LED的唯一标识，从而自动生成1000 Hz的关节位置真值。这一范式将标注过程从“事后插值”转变为“原生事件流驱动”。

基于该标注管线，作者构建了**FlashMotion**数据集——首个同时提供1000 Hz 2D标签与同步多模态数据（RGB、LiDAR、IMU、事件）的运动捕捉基准，包含715万标注帧，远超现有数据集（Table 1）。在FlashMotion上，所提出的高时间分辨率人体姿态估计方法**ResPose**以RGB锚点姿势与事件残差姿势相加（$P_i = P_{\mathrm{rgb}} + P_i^{\Delta}$）的方式，将MPJPE相比标准RGB插值降低约40%，取得5.66的MPJPE和0.99的PCK0.5（Table 4）。在精准动作计时任务中，ResPose对击拳、踢腿、跳跃的平均时间误差分别仅为4.8 ms、7.2 ms和6.5 ms（Table 3）。

自动标注管线在24段人工标注序列上达到**99.99%精确率**与**98.82%召回率**，性能接近人工标注水平（Table 2）；消融实验表明，移除匹配项中的开-关时间距离（$d_{ji}^{t}$）或周期距离（$d_{ji}^{p}$）会导致关节误分类，移除离群过滤或跟踪则造成关节漏检（Figure 7）。系统在部分光照变化与遮挡场景下已验证鲁棒性，但在强光干扰或全部LED被遮挡时的性能尚未充分探索。



### 高速运动计时的“帧率鸿沟”

精准运动计时（Precise Motion Timing, PMT）在体育科学、康复医学和生物力学分析中至关重要。例如，击剑运动员的出剑瞬间、拳击手的出拳时机、舞者的起跳时刻，都需要毫秒级的计时精度才能进行有效的技术诊断。然而，现有运动捕捉系统长期受困于一个根本性瓶颈：**标注帧率远低于实际运动的时间分辨率需求**。

传统 RGB 相机的帧率通常局限在 30–60 Hz，这意味着相邻帧之间的时间间隔长达 16–33 毫秒。对于击拳、踢腿等爆发性动作，关键的运动相位变化可能发生在短短几毫秒之内，低帧率系统只能通过插值来“猜测”中间时刻的关节位置，导致显著的运动失真和时间偏差。高速相机虽然能够达到数千帧每秒，但其成本高昂、数据带宽巨大，且通常需要专业照明和受控环境，难以在常规训练场景中大规模部署。

### 事件相机带来的机遇与挑战

事件相机（Event Camera）的出现为打破帧率限制提供了新的可能。与逐帧曝光的传统相机不同，事件相机异步感知每个像素的亮度变化，仅当光强变化超过阈值时才输出一个事件 $\boldsymbol{e} = (h, w, t, p)$，包含像素坐标、微秒级时间戳和极性。这种工作机制天然具备高时间分辨率（微秒级）和低数据冗余的优势。

然而，将事件相机直接用于人体运动捕捉面临一个核心难题：**如何从稀疏、异步的事件流中自动获取关节级真值标注？** 事件相机记录的是亮度变化的“边缘信号”，而非完整的图像内容。要从这些事件中定位人体关节并赋予身份标签，传统方法需要大量人工标注，这在 1000 Hz 的时间尺度上几乎不可行。

### 从“拍完再标”到“拍即标”的范式转变

现有运动捕捉数据集的标注流程本质上是“事后加工”：先采集视频，再通过人工或半自动方式逐帧标注关节位置。这一范式在帧率超过 120 Hz 时便难以为继——标注工作量随帧率线性增长，而人眼在毫秒尺度上已难以准确判断关节位置。

**FlashCap** 提出了一种根本性的范式转变：**将关节身份直接编码进物理信号中**。具体而言，系统在运动捕捉服上的每个关节位置安装一个 LED，并为每个 LED 分配唯一的闪烁模式（通断时间序列）。当事件相机捕捉到这些 LED 的亮灭变化时，产生的脉冲事件不仅携带了空间位置信息，还通过闪烁频率和时序模式隐含了关节身份。这样一来，**关节定位与身份识别在信号层面就被同步解决**，系统可以自动从事件流中提取 1000 Hz 的 2D 关节标注，无需人工逐帧标记。

### 本文的核心贡献

基于上述动机，本文的主要贡献包括：

1. **FlashCap 系统**：首个基于闪烁 LED 和事件视觉的毫秒级运动捕捉系统，集成了多 LED 运动捕捉服与 RGB-事件多模态采集设备。
2. **自动标注管线**：通过事件聚类、频率分析、时距-周距匹配与跟踪算法，实现 99.99% 精确率和 98.82% 召回率的全自动 1000 Hz 关节标注。
3. **FlashMotion 数据集**：首个提供 1000 Hz 2D 关节标签的多模态人体运动数据集，包含 7.15M 标注帧，远超现有数据集的标注帧率与规模。
4. **ResPose 方法**：一种融合低帧率 RGB 锚点姿势与事件流残差的高时间分辨率人体姿态估计方法，在 FlashMotion 上将 MPJPE 相比标准 RGB 插值降低约 40%。



## 核心方法与创新机理

FlashCap 的核心创新在于**将运动捕捉服的 LED 身份直接编码进高频率的闪烁模式中**，从而绕过了传统光学运动捕捉系统的帧率瓶颈。这一范式转变通过两个紧密耦合的机制实现：一是硬件层面的“闪烁编码身份”设计，二是算法层面的“事件流直接解码”管线。

### 闪烁编码身份：绕过帧率的瓶颈

传统 RGB 相机受限于 30–60 Hz 的采样率，高速相机虽能提升帧率，但成本极高且带宽需求大，难以在常规环境中实现毫秒级精确动作计时。FlashCap 的解决方案是：为运动捕捉服上的每个 LED 分配独特的通断时间模式（on‑time 与 off‑time 分别配置在 100–300 μs 范围内），使每个 LED 以 4000 Hz 的高频闪烁。事件相机异步捕捉光强变化，不仅能定位 LED 的空间位置，还能通过极性变化周期识别 LED 的唯一标识。这种“身份即闪烁模式”的设计，使得系统无需依赖高帧率图像序列，即可直接从事件流中提取 1000 Hz 的关节位置真值。

### 从事件流到毫秒级标注：自动解码管线

与闪烁编码身份相配合，FlashCap 构建了一套完整的自动标注管线（Figure 3），其核心是将事件聚类与预定义的 LED 闪烁模式进行匹配。匹配过程通过两个关键距离度量实现：
- **开‑关时间距离** $d_{ji}^{t} = |\overline{t_j^p} - t_i^p| + |\overline{t_j^n} - t_i^n|$：衡量事件集群 $j$ 与 LED $i$ 在平均开启时长和关闭时长上的差异；
- **周期距离** $d_{ji}^{p} = |T_j^n - T_i| + |T_j^p - T_i|$：衡量集群 $j$ 与 LED $i$ 在正/负极性事件序列周期上的差异。

综合距离 $d_{ji} = \alpha \cdot d_{ji}^{t} + \beta \cdot d_{ji}^{p}$ 用于最终匹配，配合离群过滤与跟踪算法，确保标注的稳定性。该管线达到 **99.99% 的精确率和 98.82% 的召回率**（Table 2），性能接近人工标注。消融实验（Figure 7）表明，移除任一距离项会导致关节误分类，移除离群过滤或跟踪则导致关节漏检。

### ResPose：事件驱动的高时间分辨率姿态估计

基于 FlashMotion 数据集提供的 1000 Hz 真值，作者提出了 **ResPose**，其核心 changed slot 在于将高时间分辨率姿态估计从“RGB 插值”转变为“RGB 锚点 + 事件残差”的范式：

- **Baseline**：RGB 姿态估计后进行样条插值（如 ViTPose + spline），无法捕捉帧间的真实运动细节。
- **Proposed**：ResPose 先通过 ViTPose 从低帧率 RGB 帧估计一个 2D 锚点姿势 $P_{\mathrm{rgb}}$，再通过事件分支提取时空事件补丁（32×32），经 LIF 神经元和 1×1 卷积突出运动区域，最后通过骨骼感知的 Transformer 建模 17 个关节间的全局依赖，输出一系列残差姿势 $P_i^{\Delta}$。最终的高时间分辨率姿势为 $P_i = P_{\mathrm{rgb}} + P_i^{\Delta}$。

这一设计使 ResPose 在 FlashMotion 数据集上将 MPJPE 相比标准 RGB 插值降低约 40%（Table 4），并取得 5.66 的 MPJPE 和 0.99 的 PCK0.5。在精准动作计时任务中，ResPose 实现击拳 4.8 ms、踢腿 7.2 ms、跳跃 6.5 ms 的平均时间误差（Table 3），验证了事件残差对捕捉毫秒级运动细节的关键作用。



FlashCap 提出了一套完整的毫秒级人体运动捕捉与自动标注系统，其核心思想是将 LED 身份直接编码进高频率的闪烁模式中，利用事件相机异步捕捉的光强变化同时完成定位与识别，从而绕过传统光学系统的帧率瓶颈。整个框架由硬件采集层、自动标注管线和高时间分辨率人体姿态估计（HPE）三大部分构成，三者形成从数据获取到下游应用的高效闭环。

### 硬件采集层

系统包含两套协同硬件（Figure 2）。运动捕捉服上搭载多个可独立配置闪烁频率的 LED 标记点与惯性测量单元（IMU），每个 LED 以预设的通断时间模式（例如 4000 Hz 频率，开启/关闭时长在 100–300 μs 之间差异化配置）发射光脉冲。多模态采集设备则由一台 RGB 相机和一台事件相机组成，同步记录场景的常规图像与异步事件流。事件相机输出的每个事件 $\boldsymbol{e} = (h, w, t, p)$ 包含像素坐标、微秒级时间戳和极性 $p$（亮度上升为正，下降为负），为毫秒级标注提供了物理基础。

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/003_Figure_2.jpg]]
*Figure 2: The FlashCap Mocap outfit(left) and multi-modal capture device(right)*

### 自动标注管线

标注管线（Figure 3）从原始事件流出发，依次完成事件聚类、频率分析、噪声过滤和 LED-集群匹配四个步骤，最终生成 1000 Hz 的 2D 关节标注。其关键机制在于：每个 LED 的闪烁模式在事件流中形成具有独特周期特征的“事件集群”，通过计算集群的平均闪烁周期 $\overline{T^j} = \overline{t_j^p} + \overline{t_j^n}$ 并与已知的 LED 配置进行匹配，即可在识别关节位置的同时确定其身份标识。

匹配过程采用双距离度量：
- **开-关时间距离** $d_{ji}^{t} = |\overline{t_j^p} - t_i^p| + |\overline{t_j^n} - t_i^n|$ 衡量集群与 LED 在平均开启时长和关闭时长上的差异；
- **周期距离** $d_{ji}^{p} = |T_j^n - T_i| + |T_j^p - T_i|$ 衡量正/负极性事件序列的周期差异。

综合距离 $d_{ji} = \alpha \cdot d_{ji}^{t} + \beta \cdot d_{ji}^{p}$ 用于最终匹配决策。为确保时序稳定性，管线还引入了基于历史帧的跟踪算法。消融实验（Figure 7）表明，移除 $d_{ji}^{t}$ 或 $d_{ji}^{p}$ 会导致关节误分类，移除离群过滤或跟踪则会造成关节漏检；完整管线在人工标注的 24 个序列上达到 99.99% 的精确率和 98.82% 的召回率（Table 2），性能接近人工标注水平。

### 高时间分辨率 HPE（ResPose）

在获得 1000 Hz 标注后，FlashCap 进一步提出 ResPose 以解决高时间分辨率姿态估计问题（Figure 8）。ResPose 采用双分支架构：

1. **RGB 分支**：以低帧率 RGB 帧为输入，通过 ViTPose（Xu et al., NeurIPS 2022）等现成方法估计 2D 锚点姿势 $P_{\mathrm{rgb}}$。
2. **事件分支**：以 $P_{\mathrm{rgb}}$ 锚点为中心进行动态裁剪，提取 32×32 的局部时空事件补丁，通过 LIF（Leaky Integrate-and-Fire）神经元和轻量 1×1 卷积分支突出运动区域，编码为事件特征 $F_{\mathrm{event}}$。
3. **Transformer 编码器**：将 $P_{\mathrm{rgb}}$ 通过可学习线性层升维后与 $F_{\mathrm{event}}$ 拼接，利用骨骼感知的自注意力机制建模 17 个关节间的全局依赖，输出残差姿势序列 $[P_i^{\Delta}]_{i=0}^N$。
4. **残差相加**：最终高时间分辨率姿势通过 $P_i = P_{\mathrm{rgb}} + P_i^{\Delta}$ 获得，在 RGB 锚点的基础上叠加事件流捕捉的精细运动细节。

### 数据流与闭环

整体数据流可概括为：闪烁 LED 标记点 → 事件相机异步事件流 → 自动标注管线（聚类、匹配、跟踪）→ 1000 Hz 2D 标注 → 多模态数据集（FlashMotion）→ ResPose 高时间分辨率 HPE。其中 FlashMotion 数据集（Table 1）以 1000 Hz 的 2D 标注帧率和 715 万标注帧数显著超越现有数据集，为毫秒级运动分析提供了前所未有的真值基础。

### 补充图表

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/001_Figure_1.jpg]]
*Figure 1: FlashCap Overview. Left/Middle: A fencing lunge recorded via our multi-modal, event-based system using flashing LEDs. Right: Generated annotations featuring 1000Hz 2D labels (bottom) alongside 60Hz 3D SMPL (top), capturing fine-grained motion dynamics*



### 事件表示与LED闪烁编码

事件相机输出的单个事件表示为四元组：

$$\boldsymbol{e} = (h, w, t, p)$$

其中 $(h,w)$ 为像素坐标，$t$ 为微秒级时间戳，$p$ 为极性（正/负分别对应亮度增加或减少）。FlashCap 为每颗 LED $i$ 配置独特的通断时间模式——开启时长与关闭时长在 $100\,\mu\text{s}$ 到 $300\,\mu\text{s}$ 范围内差异化设置，并以约 4000 Hz 的频率闪烁。事件相机异步捕捉这些光强变化，从而在事件流中形成可区分的时空模式。

### 事件聚类与周期提取

事件流首先按空间邻近性和时间连续性被聚合为事件集群 $j$。对每个集群，系统分别计算正极性事件序列的平均时间间隔 $\overline{t_j^p}$ 和负极性事件序列的平均时间间隔 $\overline{t_j^n}$，进而得到集群的平均闪烁周期：

$$\overline{T^j} = \overline{t_j^p} + \overline{t_j^n}$$

该周期是后续 LED 身份识别的核心特征之一。

### LED-集群匹配距离

将事件集群 $j$ 与已知 LED $i$ 进行匹配时，系统计算两个互补的距离度量：

**开-关时间距离**衡量集群与 LED 在平均开启时长和关闭时长上的差异：

$$d_{ji}^{t} = |\overline{t_j^p} - t_i^p| + |\overline{t_j^n} - t_i^n|$$

**周期距离**衡量正/负极性事件序列周期的一致性：

$$d_{ji}^{p} = |T_j^n - T_i| + |T_j^p - T_i|$$

综合距离为二者的加权和：

$$d_{ji} = \alpha \cdot d_{ji}^{t} + \beta \cdot d_{ji}^{p}$$

其中 $\alpha$ 和 $\beta$ 为权重系数。通过最小化 $d_{ji}$，系统将每个事件集群分配给最匹配的 LED 标识，并辅以跟踪算法维持跨帧匹配的稳定性。消融实验表明，移除 $d_{ji}^{t}$ 或 $d_{ji}^{p}$ 中任一项均会导致关节误分类（Figure 7）。

### ResPose 残差融合公式

ResPose 的核心思路是将低帧率 RGB 锚点姿势与事件流导出的高时间分辨率残差姿势相加。设 RGB 分支（如 ViTPose）从单帧 RGB 图像 $I$ 中估计出 2D 锚点姿势 $P_{\text{rgb}}$，事件分支从事件流中估计出 $N$ 个残差姿势序列 $[P_i^{\Delta}]_{i=0}^{N}$，则最终的高时间分辨率姿势序列为：

$$P_i = P_{\text{rgb}} + P_i^{\Delta}$$

这一残差设计使得模型无需从事件流中独立回归完整姿势，而是以 RGB 锚点为先验，仅需学习运动偏移量，显著降低了事件分支的学习难度。

### 补充图表

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/004_Figure_3.jpg]]
*Figure 3: An example of the FlashCap data annotation pipeline: (0) Event Streams. (1) Identified Event Clusters. (2) Cluster Frequency Analysis. (3) Filtered Clusters After Noise Removal. (4) Matched LED-Cluster Pairs (Labels)*

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/010_Figure_8.jpg]]
*Figure 8: Architecture of ResPose. It obtain high-temporal resolution pose Pi through*



## 实验与关键发现

### 标注管线定量评估

FlashCap 自动标注管线的核心目标是替代昂贵的人工标注，生成可靠的 1000 Hz 2D 关节真值。Table 2 报告了在 24 段人工标注序列上的定量评估结果：完整管线达到 **99.99% 的精确率**和 **98.82% 的召回率**，性能接近人工标注水平。

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/011_Table_2.jpg]]
*Table 2: Quantitative evaluation against human annotated labels*

消融实验（Figure 7）揭示了各组件的关键作用：
- **移除开-关时间距离 $d_{ji}^{t}$** 或 **周期距离 $d_{ji}^{p}$**：导致事件集群与 LED 身份的错误匹配，引发关节误分类。
- **移除离群过滤** 或 **跟踪模块**：导致部分关节漏检，召回率显著下降。

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative evaluation when ablating the annotation pipeline*

上述结果表明，基于闪烁模式的身份编码机制（将每个 LED 的唯一通断时间模式嵌入事件流）是实现高精度自动标注的因果瓶颈——仅依赖空间聚类或单一时间特征无法可靠区分 17 个关节。

### 精准动作计时任务

精准动作计时（Precise Motion Timing, PMT）是 FlashMotion 数据集独有的评测任务，要求方法准确估计动作跨越预设线的时间戳。Table 3 报告了 ResPose 与各基线方法的平均时间误差：

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/012_Table_3.jpg]]
*Table 3: The Mean Error of Estimated Time (PMT).Unit: ms*

- **击拳**：4.8 ms
- **踢腿**：7.2 ms
- **跳跃**：6.5 ms

ResPose 在所有动作类别上均取得最低误差。这一优势源于其架构设计：RGB 分支提供低频锚点姿势 $P_{\text{rgb}}$，事件分支通过 LIF 神经元和 1×1 卷积提取毫秒级运动残差 $P_i^{\Delta}$，最终通过 $P_i = P_{\text{rgb}} + P_i^{\Delta}$ 合成 1000 Hz 姿势序列。相比之下，传统 RGB 插值方法（如 ViT + spline）无法捕捉高频运动细节，而纯事件方法（如 Hybrid ANN-SNN、EventPointPose、GraphEnet、EvSharp2Blur、LEIR）缺乏 RGB 锚点提供的全局结构约束，在长时间序列上易产生漂移。

### 高时间分辨率 HPE 任务

Table 4 报告了 FlashMotion 上高时间分辨率人体姿态估计（HPE）任务的结果。ResPose 取得 **5.66 的 MPJPE** 和 **0.99 的 PCK0.5**。摘要中明确指出，相比标准 RGB 插值方法，ResPose 将 MPJPE **降低约 40%**（基线 MPJPE 约 9.4）。

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/014_Table_4.jpg]]
*Table 4: High Temporal Resolution HPE Task in FlashMotion*

Figure 10 提供了 50 ms 间隔内的轨迹定性对比。ViTPose 和 ViT（spline）的轨迹呈平滑线性，无法反映真实运动的非线性动态；事件方法（Hybrid ANN-SNN、EventPointPose、GraphEnet、EvSharp2Blur、LEIR）虽能捕捉部分高频变化，但在关节间空间一致性上表现不佳。ResPose 通过骨骼感知的自注意力机制建模 17 个关节间的全局依赖，同时利用事件补丁的动态裁剪（以 $P_{\text{rgb}}$ 锚点为中心的 32×32 时空窗口）聚焦局部运动区域，实现了高频精度与空间一致性的平衡。

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/015_Figure_10.jpg]]
*Figure 10: Qualitative comparison of trajectories for the High Temporal Resolution HPE task over a 50 ms interval. (a) ViTPose. (b) ViT (spline). (c) Hybrid ANN-SNN. (d) EventPointPose. (e) GraphEnet. (f) EvSharp2Blur. (g) LEIR. (h) ResPose (Ours)*

### 失败模式与局限性

尽管整体性能优异，系统仍存在以下局限：

1. **标注管线依赖少量人工校验**：在极端噪声或遮挡场景下，个别 LED 集群可能被错误匹配，需人工修正。
2. **3D 标签帧率受限**：当前仅提供 1000 Hz 的 2D 标签，3D SMPL 标签仍受限于 60 Hz 的传统传感器融合，无法实现毫秒级 3D 运动捕捉。
3. **环境鲁棒性未充分验证**：系统在部分光照变化和遮挡场景下表现良好，但强光干扰（如户外日光）或全部 LED 被遮挡时的性能尚未系统评估。

### 数据集统计优势

Table 1 将 FlashMotion 与现有运动捕捉数据集进行了全面对比。FlashMotion 的 **2D 标签帧率达 1000 Hz**，标注帧数达 **715 万帧**，在帧率和规模上均显著超越现有数据集（包括事件相机数据集）。这一优势源于 FlashCap 的范式转变：通过将 LED 身份编码进高频闪烁模式，直接从事件流中生成原生 1000 Hz 标签，绕过了传统光学系统的帧率瓶颈。

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/002_Table_1.jpg]]
*Table 1: Comparisons with related human motion datasets. Datasets with Event camera data are grouped in the second block. Our FlashMotion provides the highest 2D label frame rate (1000Hz) and the largest number of labeled frames (7.15M) by a significant margin. Abbreviations: (Dur.) Duration, (# Seqs.) Number of Sequences, (# Subjs.) Number of Subjects*

### 补充图表

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/006_Figure_5.jpg]]
*Figure 5: Interpolated vs. Ground-Truth 1000 Hz Poses. (Left) Event frames at selected timestamps. (Middle) Accumulated event stream. (Right) trajectory comparison. The red line indicates 20 Hz interpolation, and the green line indicates 1000 Hz ground truth*

![[assets/figures/papers/paper_list_l1062_https_arxiv_org_abs_2603_19770/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative evaluation against a high-speed camera: Columns (a), (c), and (e) show that our labels (green spots) overlap with the images captured by high-speed cameras closely. This demonstrate the correctness of FlashMotion labels qualitatively. Columns (b), (d), and (f) show that the corresponding events overlaid on the RGB frames. The red/blue dots indicate events with positive/negative polarity*



## 定位与知识库关联

FlashCap 的核心贡献在于**数据获取范式**而非模型架构本身——它通过“闪烁 LED + 事件相机”的组合，首次实现了 1000 Hz 的 2D 人体姿态真值自动标注。这一范式区别于现有所有基于光学标记或 RGB 插值的运动捕捉方案，其方法定位可从以下几个维度理解。

### 1. 与传统光学 MoCap 的关系：绕过帧率瓶颈

传统光学运动捕捉系统依赖高速相机以高帧率追踪被动反光标记，但成本极高、带宽需求大，且难以在常规环境中部署。FlashCap 的**因果旋钮**在于：将每个 LED 的身份编码进高频通断模式（on-time 与 off-time 各配置为 100–300 μs 的不同组合），事件相机异步捕捉光强变化后，可直接从事件流中提取 1000 Hz 的关节位置。这绕过了“相机帧率决定标注帧率”的根本瓶颈，使毫秒级真值生成成为可能。

与高速相机的定性对比（Figure 6）表明，FlashCap 生成的标签与高速相机图像中的 LED 位置高度重合，验证了标注的空间准确性。

### 2. 与现有事件相机数据集的定位差异

Table 1 将 FlashMotion 与现有含事件相机数据的人体运动数据集进行了对比。FlashMotion 的 2D 标签帧率达 **1000 Hz**，标注帧数达 **715 万帧**，在两项指标上均显著超越已有数据集（第二组 block 中的其他事件数据集）。这使 FlashMotion 成为当前唯一支持精确动作计时（Precise Motion Timing, PMT）和高时间分辨率 HPE 的基准。

### 3. ResPose 在 HPE 方法谱系中的位置

ResPose 并非独立的全新姿态估计架构，而是一种**融合 RGB 锚点与事件残差的混合范式**：

$$P_i = P_{\mathrm{rgb}} + P_i^{\Delta}$$

其中 $P_{\mathrm{rgb}}$ 由 **ViTPose**（Xu et al., NeurIPS 2022）从低帧率 RGB 帧生成，$P_i^{\Delta}$ 由事件分支从时空事件补丁中学习。事件分支通过 LIF 神经元和 1×1 卷积突出运动区域，再经骨骼感知自注意力的 Transformer 建模 17 个关节的全局依赖。

在 FlashMotion 的高时间分辨率 HPE 任务中，ResPose 相比以下基线取得了显著优势：

- **ViTPose**（纯 RGB 基线）：直接使用低帧率 RGB 估计，缺乏帧间运动信息。
- **ViT (spline)**：对 ViTPose 输出进行样条插值——这正是 FlashCap 试图取代的“插值伪高帧率”范式。Figure 5 直观展示了插值轨迹与真实 1000 Hz 轨迹的偏差。
- **Hybrid ANN-SNN**、**EventPointPose**、**GraphEnet**（Goyal et al., ICCVW 2025）、**EvSharp2Blur**（Kim et al., ICCV 2025）、**LEIR**：均为事件驱动的 HPE 方法，但未利用 RGB 锚点提供的全局结构先验，在高时间分辨率场景下精度不及 ResPose。

ResPose 将 MPJPE 从标准 RGB 插值的约 9.4 降至 **5.66**（降幅约 40%），PCK0.5 达 **0.99**（Table 4），在 PMT 任务中击拳、踢腿、跳跃的平均时间误差分别为 **4.8 ms、7.2 ms、6.5 ms**（Table 3）。这些结果表明，RGB 锚点提供空间稳定性、事件流提供时间精度的分工是有效的。

### 4. 自动标注管线的可验证性

标注管线本身经过了严格的消融验证（Table 2, Figure 7）：

- 完整管线达到 **99.99% 精确率**和 **98.82% 召回率**，与人工标注高度一致。
- 移除开-关时间距离 $d_{ji}^{t}$ 或周期距离 $d_{ji}^{p}$ 会导致关节误分类。
- 移除离群过滤或跟踪模块会导致关节漏检。

这一定量证据的置信度极高（0.99），表明基于闪烁模式的身份编码机制是可靠的。

### 5. 适用边界与局限

尽管 FlashCap 在受控场景下表现优异，其适用边界需谨慎界定：

1. **3D 标签仍受限于 60 Hz**：当前系统仅提供 1000 Hz 的 2D 标签，3D SMPL 标注仍依赖传统传感器融合，帧率停留在 60 Hz。如何将毫秒级精度扩展到全身 3D 运动捕捉，是首要开放问题。
2. **人工校验尚未完全消除**：自动标注管线仍依赖少量人工校验修正个别错误标签，距离完全自动化尚有距离。
3. **极端光照与遮挡鲁棒性未充分探索**：系统虽在部分光照变化和遮挡场景下得到验证，但强光干扰（如户外直射日光）或全部 LED 被遮挡时的性能退化程度尚未量化。事件相机在强光下的噪声特性可能显著影响标注精度。
4. **RGB 锚点的依赖性**：ResPose 仍需低帧率 RGB 帧提供锚点姿势。能否完全用事件相机替代 RGB 分支，实现纯事件驱动的 1000 Hz HPE，是另一个开放方向。

### 6. 知识库定位总结

FlashCap 在知识库中的定位可概括为：**首个将闪烁 LED 身份编码与事件视觉结合、实现毫秒级运动真值自动生成的数据获取范式**。它不直接竞争 HPE 模型架构，而是为高时间分辨率 HPE 提供了一个此前不存在的基准（FlashMotion）和一种锚点-残差融合的基线方法（ResPose）。后续工作若能在 3D 扩展、纯事件驱动、极端环境鲁棒性三个方向上取得突破，将进一步释放这一范式的潜力。



## 原文 PDF

![[paperPDFs/CVPR_2026/FlashCap_Millisecond_Accurate_Human_Motion_Capture_via_Flashing_LEDs_and_Event_Based_Vision.pdf]]
