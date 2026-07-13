---
title: "Thermal is Always Wild: Characterizing and Addressing Challenges in Thermal-Only Novel View Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Thermal_is_Always_Wild_Characterizing_and_Addressing_Challenges_in_Thermal_Only_Novel_View_Synthesis.pdf
project_link: "https://nubivlab.github.io/wild_thermal"
code_link: null
aliases:
- WTPS3ECE
- TIAWCACTONVS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 通过基于指数滑窗参考 CDF 的直方图对齐与亮度保持双直方图均衡（BBHE）实现光度稳定化，再结合每-高斯与每-帧嵌入的标量发射 MLP，显式消弭帧间辐射不一致并吸收残余变化。
primary_logic: 将热成像的帧间辐射不一致视为“野外观”（in‑the‑wild）外观变化，采用物理约束的单通道标量发射模型替代 RGB 球谐，并通过嵌入条件外观建模在不扭曲几何的前提下稳定光度，从而仅靠纯热输入即可实现高保真重建。
claims:
- 光度稳定化与发射 MLP 两者独立有效且高度互补：预处理将平均 PSNR 从 22.25 dB 提升至 23.01 dB，发射 MLP 进一步提升至 24.93 dB，完整方法达到 26.14 dB，消融实验证实各组件缺一不可。
- 预处理有效抑制帧间均值漂移，增强后的热成像空间频谱更接近 RGB，同时 SIFT 特征点数量明显上升，为 COLMAP 初始化和 3DGS 训练提供更强监督。
- 在 MSX、ThermalMix、MVTV、Lin et al.、Ye et al.、TINSD 六个数据集上均取得 SOTA PSNR 与 SSIM，训练时间仅 11 分钟，且无需针对特定数据集调参。
- MSX 上 PSNR↑ / SSIM↑ = 23.59 / 0.71
---

# Thermal is Always Wild: Characterizing and Addressing Challenges in Thermal-Only Novel View Synthesis

> [!tip] 核心洞察
> 将热成像的帧间辐射不一致视为“野外观”（in‑the‑wild）外观变化，采用物理约束的单通道标量发射模型替代 RGB 球谐，并通过嵌入条件外观建模在不扭曲几何的前提下稳定光度，从而仅靠纯热输入即可实现高保真重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 热成像始终充满“野性”：纯热成像新视角合成的挑战分析与应对 |
| 英文题名 | Thermal is Always Wild: Characterizing and Addressing Challenges in Thermal-Only Novel View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.20448) · [Project](https://nubivlab.github.io/wild_thermal) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | Wild Thermal (Photometric Stabilized 3DGS with Embedding-conditioned Emission) |
| Dataset | MSX, ThermalMix, MVTV, Lin et al. |

> [!tip] 效果简介
> - MSX 上，PSNR↑ / SSIM↑ 23.59 / 0.71 vs Prior SOTA (Thermal3D-GS) (SOTA（详见 Table 1）)。
> - ThermalMix 上，PSNR↑ / SSIM↑ 24.61 / 0.74 vs Prior SOTA (Thermal3D-GS) (SOTA)。
> - MVTV 上，PSNR↑ / SSIM↑ 25.13 / 0.84 vs Prior SOTA (Thermal3D-GS) (SOTA)。

## 概要

纯热成像新视角合成（Thermal‑only NVS）面临一个根本性瓶颈：热红外图像的低动态范围、强烈的帧间光度波动以及缓慢的辐射漂移，严重破坏多视图一致性，使得依赖稳定光度与纹理线索的 NeRF/3DGS 方法难以收敛，并产生漂浮几何伪影。本文提出 **Wild Thermal**，将热成像的帧间辐射不一致视为“野外观”（in‑the‑wild）外观变化，通过**光度稳定化预处理**与**嵌入条件发射建模**两大核心组件协同解决这一挑战。

方法的核心因果机制是：首先，基于指数滑窗参考 CDF 的直方图对齐与亮度保持双直方图均衡（BBHE）实现输入帧的光度稳定化与对比度增强，有效抑制帧间均值漂移并使热成像空间频谱更接近 RGB；随后，在 3DGS 框架中采用物理约束的单通道标量发射模型替代 RGB 球谐，通过每‑高斯与每‑帧嵌入经 MLP 映射为标量发射值，显式消弭帧间残余辐射不一致并吸收瞬变，从而在不扭曲几何的前提下稳定光度。

在 MSX、ThermalMix、MVTV、Lin et al.、Ye et al.、TINSD 六个公开数据集上，Wild Thermal 以仅 11 分钟的训练时间全面超越 NeRF、ThermalMix‑TS、Lin et al.、ThermoNeRF 及 Thermal3D‑GS 等基线方法，取得 SOTA PSNR 与 SSIM。消融实验证实，光度稳定化与发射 MLP 两者独立有效且高度互补：预处理将平均 PSNR 从 22.25 dB 提升至 23.01 dB，发射 MLP 进一步提升至 24.93 dB，完整系统达到 26.14 dB，各组件缺一不可。定性结果表明，本文方法在保持锐利边界与稳定背景温度的同时，有效消除了 Thermal3D‑GS 中常见的漂浮伪影。



热红外成像在安防监控、自动驾驶、工业检测和夜间感知等场景中具有不可替代的价值——它直接捕获物体自身的热辐射，无需外部光源即可全天候工作。然而，与成熟的 RGB 新视角合成（NVS）技术相比，纯热成像驱动的三维重建与渲染仍然是一个几乎未被探索的领域。这一差距并非偶然：热成像数据携带一系列独特的物理与信号退化特性，使得直接迁移 RGB 领域的 NeRF 或 3DGS 方法面临系统性失败。

### 热成像数据的“野性”本质

本文通过对六个公开热成像多视图数据集的系统分析，揭示了阻碍纯热成像 NVS 的三重核心挑战：

**1. 剧烈的帧间光度不一致。** 热像仪在连续采集过程中，帧与帧之间的平均强度会发生显著漂移。这种漂移既包含快速的帧间波动（通常由传感器内部的自动增益控制、非均匀性校正等 ISP 操作触发），也包含缓慢的辐射爬移（随传感器升温或环境温度变化而累积）。定量分析表明，热成像序列的相对均值变化 $\Delta I_t$ 的标准差远高于 RGB 视频，严重破坏了多视图立体匹配所依赖的光度一致性假设。对于 NeRF 和 3DGS 而言，这意味着同一三维点在不同视图中呈现截然不同的“颜色”，直接导致几何重建失败或产生大量漂浮伪影。

**2. 低动态范围与纹理匮乏。** 热成像的空间频谱分析揭示了一个结构性缺陷：与 RGB 图像相比，热图像的径向平均功率谱 $S_t(f)$ 在中高频段能量显著偏低。这既是传感器分辨率限制的结果，也源于热扩散效应的物理本质——热量在物体表面传导，模糊了原本锐利的纹理边界。低动态范围进一步压缩了像素强度的分布，使得传统依赖角点、边缘等纹理线索的特征匹配（如 SIFT）在热图像上提取到的特征点数量大幅减少，从而削弱了 COLMAP 等 SfM 初始化流程的可靠性。

**3. 传感器特异性退化。** 热像仪还引入了一系列 RGB 相机中罕见的退化模式，包括固定模式噪声、晕影效应以及非均匀性残留。这些退化在帧间可能呈现不同的空间分布，进一步加剧了多视图不一致性。

### 现有方法的缺口

现有的热成像 NVS 方法大致可分为两类，但均未能充分应对上述挑战：

- **RGB-热成像融合方法**（如 **ThermoNeRF** (Hassan et al., 2023)、**Lin et al.** (Lin et al., 2024)）依赖配对的 RGB 图像提供纹理和几何线索，通过跨模态一致性约束辅助热重建。这类方法在 RGB 与热像仪严格标定、同步采集的场景下有效，但极大地限制了应用场景——在纯热成像条件下（如完全黑暗环境、无 RGB 传感器部署）完全失效。

- **纯热成像方法**（如 **Thermal3D-GS** (Chen et al., 2025)）尝试将 3DGS 适配到热域，通过物理启发的温度建模和温度一致性约束进行重建。然而，这些方法仍然假设热成像帧间光度是基本稳定的，未对帧间辐射漂移进行显式建模。当面对真实场景中剧烈的光度波动时，其渲染结果往往出现漂浮的亮块、错误的几何结构以及不稳定的背景温度——这正是光度不一致性未被处理的典型症状。

### 核心洞察与动机

本文的核心洞察在于：**热成像的帧间辐射不一致性本质上是一种“野外观”（in-the-wild）外观变化**——类似于 RGB 领域中因光照变化、曝光差异和相机响应函数不同导致的外观变异。然而，热成像领域的独特之处在于，这种变化是**标量强度维度上的单通道漂移**，而非 RGB 三通道的颜色偏移。这意味着：

1. 无需复杂的球谐函数或高维外观嵌入来建模视角相关颜色——一个物理约束的**单通道标量发射模型**足以描述热辐射的本质；
2. 在将数据送入三维表示之前，可以通过**轻量级的光度预处理**在二维图像域显著抑制帧间漂移，为下游重建提供更一致的监督信号；
3. 将预处理与嵌入条件的外观建模相结合，可以在**不扭曲底层几何**的前提下稳定光度表现，避免现有方法中常见的“以几何畸变为代价换取光度拟合”的失败模式。

基于这一洞察，本文提出 **Wild Thermal**——一个由光度稳定化预处理与嵌入条件发射 3DGS 组成的纯热成像 NVS 流水线，旨在以极低的计算开销（训练仅需约 11 分钟）实现跨数据集的鲁棒高保真热重建。



## 核心方法与创新机理

### 问题本质的重新定义：热成像的“野外观”属性

本文的核心创新始于对问题本质的重新审视。与以往将热成像视为“低纹理 RGB”或需要物理建模的辐射测量数据的视角不同，本文首次将热成像帧间剧烈的光度不一致性——包括低动态范围、帧间均值漂移、缓慢的辐射瞬变——系统性地定义为一种 **“野外观”（in‑the‑wild）外观变化问题**。这一认知转变是关键性的：它意味着问题的根源不在于热物理过程的复杂性，而在于多视图光度一致性的缺失，这直接破坏了 NeRF/3DGS 等现代新视角合成方法的底层假设。

定量分析（Figure 2）揭示了这一问题的严重性：热成像序列的相对均值变化 $\Delta I_t$ 的标准差远高于 RGB 序列，且径向平均功率谱 $S_t(f)$ 表明热成像在中高频段的能量显著匮乏。这两个现象共同构成了**双重瓶颈**——帧间辐射漂移使多视图匹配失效，而纹理匮乏则使几何优化缺乏约束，最终导致漂浮几何伪影和重建失败。

### 方法谱系与知识库定位

在方法谱系中，Wild Thermal 处于两条技术路线的交汇点。在热成像 NVS 方向，它区别于 **Thermal3D‑GS**（physics‑inspired 3DGS with temperature‑consistency constraints）的物理建模路径，也不同于 **Thermal‑NeRF**（thermal mapping + structural patch constraint）或 **Lin et al.**（RGB‑热成像双分支 NeRF）的跨模态依赖策略。在野外观建模方向，它借鉴了 NeRF‑W 等工作中“嵌入条件外观建模”的思想，但做出了关键适配：将 RGB 空间中的高维球谐外观变化，压缩为热成像物理本质所允许的**单通道标量发射变化**。

### Changed Slots：五个维度的系统性重构

本文相对于 3DGS 基线的创新可精确分解为五个 changed slots，每个 slot 对应热成像的一个独特挑战：

**Slot 1：颜色/辐射表示——从 RGB 球谐到标量发射**

3DGS 使用 RGB 颜色 + 球谐系数建模视角依赖的外观变化，这在热成像中不仅冗余（热辐射无视角依赖性），而且有害——球谐的过度表达能力会将帧间辐射漂移错误地吸收为视角依赖效应，产生不可靠的几何。Wild Thermal 将每个 3D 高斯原语的颜色表示缩减为**单个标量发射值**，物理上对应热成像传感器的辐射亮度测量。这一约束性设计（物理先验）是后续嵌入条件外观建模的基础。

**Slot 2：外观建模——从固定颜色到嵌入条件发射**

这是性能提升最大的单一创新。传统 3DGS 中每个高斯的颜色在训练后固定，无法适应帧间辐射变化。Wild Thermal 引入**每‑高斯嵌入 $\mathbf{e}_i^{(g)}$** 与**每‑帧嵌入 $\mathbf{e}_t^{(f)}$**，通过轻量 MLP $f_{\boldsymbol{\theta}}$ 映射为帧相关的标量发射值 $c_i(t) = f_{\boldsymbol{\theta}}(\mathbf{e}_i^{(g)}, \mathbf{e}_t^{(f)})$。这一设计的精巧之处在于：每‑高斯嵌入编码了空间位置固有的热辐射特性（如材质发射率差异），而每‑帧嵌入则吸收全局性的辐射瞬变（如传感器增益漂移），两者解耦后，几何优化不再受外观波动干扰。消融实验证实，仅此一项即将平均 PSNR 从 22.25 dB 提升至 24.93 dB（Table 2）。

**Slot 3：输入预处理——从原始帧到光度稳定化**

热成像的帧间辐射漂移在进入 3DGS 优化前即已造成破坏。Wild Thermal 提出了一个两阶段预处理管线：

1. **光度稳定化**：维护指数滑窗参考 CDF $F_t^*(x) = (1-\alpha)F_{t-1}^*(x) + \alpha F_t(x)$，通过混合映射 $I_t'(x) = (1-\beta)x + \beta F_t^{*-1}(F_t(x))$ 将每帧的直方图对齐到时序平滑的参考分布，在抑制漂移与保留原始内容间取得平衡（$\beta$ 控制对齐强度）。
2. **对比度增强**：采用亮度保持双直方图均衡（BBHE），以均值亮度 $T_t^\mu$ 为界划分直方图，对上、下子区间独立均衡化，扩宽动态范围的同时避免传统直方图均衡的亮度偏移问题。

该预处理的效果是双重的：不仅直接抑制了帧间均值漂移（Figure 3e），还使增强后的热成像空间频谱更接近 RGB（Figure 3f），SIFT 特征点数量显著上升（Figure 3h），为 COLMAP 初始化和后续 3DGS 训练提供了更强的监督信号。消融实验表明，传统直方图均衡反而损害性能，而 BBHE 增强与光度稳定化高度互补（Table S1）。

**Slot 4：背景建模——从简单远距处理到背景 MLP**

针对热成像中远景区域（如天空、远距离建筑）辐射特性与前景差异显著的问题，Wild Thermal 引入背景 MLP $b_\phi(\mathbf{d}, \mathbf{e}_t^{(f)})$，以视线方向 $\mathbf{d}$ 和每‑帧嵌入为输入预测背景辐射。前景高斯渲染 $\hat{I}_t(\mathbf{r})$ 与背景预测通过残余透射率 $m(\mathbf{r})$ 融合：$\tilde{I}_t(\mathbf{r}) = (1 - m(\mathbf{r})) \hat{I}_t(\mathbf{r}) + m(\mathbf{r}) b_\phi(\mathbf{d}, \mathbf{e}_t^{(f)})$。这一设计使背景区域的辐射变化被显式建模，避免前景高斯为拟合背景而畸变。

**Slot 5：损失函数——从 L1+SSIM 到热感知损失**

标准 SSIM 在低动态范围的热成像中区分度不足。Wild Thermal 采用**热感知 SSIM（$\mathcal{L}_{\text{HSSIM}}$）** 强调热对比度与结构信息，辅以背景正则化项 $\mathcal{L}_\alpha$ 抑制背景区域的漂浮高斯。完整损失函数为 $\mathcal{L} = \lambda_1 \mathcal{L}_{\text{L1}} + \lambda_2 \mathcal{L}_{\text{HSSIM}} + \lambda_3 \mathcal{L}_\alpha$。

### 创新的因果机制

上述五个 slot 并非孤立改进，而是沿一条清晰的因果链协同作用：**预处理稳定输入光度 → 标量发射约束防止过拟合 → 嵌入条件建模吸收残余变化 → 背景 MLP 处理远景 → 热感知损失引导优化**。消融实验（Table 2）精确量化了这一协同效应：预处理单独使用将平均 PSNR 从 22.25 dB 提升至 23.01 dB，发射 MLP 单独使用提升至 24.93 dB，两者结合达到 26.14 dB，证实了“稳定输入”与“灵活建模”两个维度的互补性。

### 与 SOTA 的本质差异

与最强基线 **Thermal3D‑GS** 的对比最能体现创新价值。Thermal3D‑GS 试图通过物理启发的温度一致性约束来应对辐射不一致，但这一策略在遭遇帧间辐射瞬变时会产生**漂浮几何伪影**——优化过程将辐射波动错误地解释为空间结构变化，生成随视角漂移的亮斑（Figure 7）。Wild Thermal 从根本上避免了这一问题：预处理在输入端消弭大部分辐射漂移，嵌入条件发射 MLP 在优化中吸收残余瞬变，使几何优化免受外观波动干扰。Figure 6 的定性对比显示，Wild Thermal 在保持锐利边界和稳定背景温度的同时，忠实重建了 Thermal3D‑GS 丢失的纹理细节（如窗户、树木、墙壁纹理）。

### 局限与开放性问题的创新启示

当前方法的局限也为后续创新指明了方向。光度稳定化依赖于已知相机位姿和完整的序列帧，这限制了其在纯热成像 SLAM 场景中的应用——**热成像原生位姿估计**仍是一个开放挑战。此外，预处理在放大动态范围的同时也放大了传感器噪声，在极低纹理区域可能引入结构化伪影。这些局限暗示了下一阶段创新的可能方向：将光度稳定化与三维重建**联合优化**，使系统在缺乏完整序列先验时也能自适应调整；或引入**显式的噪声建模模块**，在增强对比度与抑制噪声之间取得动态平衡。



### 问题本质与设计动机

热红外图像天然存在三大“野性”挑战，直接破坏了多视图几何重建所需的帧间一致性：(1) **低动态范围与纹理匮乏**，导致特征匹配困难；(2) **强烈的帧间光度波动**，表现为缓慢的辐射漂移和瞬态偏移；(3) **传感器特异性退化**，包括晕影、固定模式噪声等。传统 NeRF 与 3DGS 方法依赖稳定的光度与丰富的纹理线索，在此类数据上极易产生漂浮几何伪影或完全无法收敛。

本文的核心洞察在于：将热成像的帧间辐射不一致视为“野外观”（in‑the‑wild）外观变化问题，通过**物理约束的单通道标量发射模型**替代 RGB 球谐，并结合**嵌入条件外观建模**，在不扭曲几何的前提下稳定光度，从而仅靠纯热输入即可实现高保真重建。

### Pipeline 总览

整体系统由两大阶段串联构成，如 Figure 4 所示：

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/004_Figure_4.jpg]]
*Figure 4: Our pipeline. Given thermal frames and camera poses, we first stabilize the inputs to ensure consistent training data across views (bottom). The frames are modeled with a novel combination of per-Gaussian embeddings, which encode spatial appearance, per-frame embeddings, which capture residual temporal artifacts, and a physics-restricted parameter set (grayscale with no spherical harmonics) that stabilizes learning. These components jointly enable consistent thermal reconstruction while preserving fine geometric and intensity details*

1. **光度稳定化预处理阶段**：对输入热成像序列进行帧间辐射对齐与动态范围扩展，输出光度一致的增强帧。
2. **嵌入条件 3DGS 重建阶段**：以稳定化后的帧作为训练数据，采用每‑高斯嵌入与每‑帧嵌入联合驱动的标量发射 MLP 进行场景表示与渲染。

```
输入热成像序列 + 相机位姿
        │
        ▼
┌─────────────────────────────┐
│  光度稳定化预处理            │
│  · 指数滑窗参考 CDF 对齐     │
│  · BBHE 对比度增强          │
└──────────────┬──────────────┘
               │ 稳定化帧
               ▼
┌─────────────────────────────┐
│  嵌入条件 3DGS 重建          │
│  · 标量发射高斯原语          │
│  · 发射 MLP (e_i^(g), e_t^(f))│
│  · 背景 MLP + 前景‑背景融合   │
│  · 热感知损失 (L1+HSSIM+Lα)  │
└──────────────┬──────────────┘
               │
               ▼
         新视角热成像渲染
```

### 模块间数据流与接口

**阶段一 → 阶段二的衔接**：预处理模块输出光度稳定化且对比度增强的帧序列 $\hat{I}_t$，这些帧直接作为 3DGS 重建阶段的训练输入。预处理参数在所有数据集上保持一致，无需场景特化调优。

**阶段二内部的数据流**：
- 每个 3D 高斯原语存储一个**标量发射值**（不含球谐系数），同时携带一个可学习的**每‑高斯嵌入向量** $\mathbf{e}_i^{(g)}$。
- 每帧关联一个可学习的**每‑帧嵌入向量** $\mathbf{e}_t^{(f)}$。
- 发射 MLP $f_{\boldsymbol{\theta}}$ 接收上述两类嵌入的拼接，输出该高斯在当前帧的标量发射值 $c_i(t) = f_{\boldsymbol{\theta}}(\mathbf{e}_i^{(g)}, \mathbf{e}_t^{(f)})$。
- 沿光线累积透射渲染：$\hat{I}_t(\mathbf{r}) = \sum_i T_i \alpha_i c_i(t)$。
- 背景 MLP 处理远景区域，通过残余透射率 $m(\mathbf{r})$ 与前景高斯渲染融合：$\tilde{I}_t(\mathbf{r}) = (1 - m(\mathbf{r})) \hat{I}_t(\mathbf{r}) + m(\mathbf{r}) b_{\phi}(\mathbf{d}, \mathbf{e}_t^{(f)})$。

### 关键设计决策的因果逻辑

| 设计选择 | 解决的瓶颈 | 因果机制 |
|---------|-----------|---------|
| CDF 对齐 + BBHE 预处理 | 帧间辐射漂移 + 低动态范围 | 指数滑窗参考 CDF 抑制时序均值漂移，BBHE 以均值亮度为界独立均衡化上下子直方图，扩宽动态范围的同时保持亮度结构 |
| 标量发射替代 RGB 球谐 | 热成像无颜色信息，球谐引入冗余自由度 | 单通道辐射亮度符合热物理本质，减少过参数化风险 |
| 每‑高斯 + 每‑帧嵌入 | 帧间残余辐射瞬变无法被几何吸收 | 嵌入条件外观建模将辐射变化显式归因于外观空间，避免几何扭曲 |
| 背景 MLP + 残余透射率融合 | 远景区域高斯覆盖不足 | 将背景建模为与方向、帧嵌入相关的函数，通过透射率实现无缝前景‑背景过渡 |
| 热感知 SSIM + 背景正则化 | 标准 SSIM 对热对比度不敏感，漂浮物难以抑制 | $\mathcal{L}_{\text{HSSIM}}$ 强调热对比与结构，$\mathcal{L}_{\alpha}$ 惩罚背景区域的漂浮高斯 |

### 与基线方法的架构差异

相比于 **Thermal3D-GS**（物理启发的热成像高斯泼溅）和 **ThermalMix-TS**（基于 Instant-NGP 的快速 NeRF 变体）等方法，本文 pipeline 的核心区分点在于：(1) 在进入重建之前主动稳定输入光度，而非依赖网络自身消化辐射波动；(2) 将外观变化建模从“每高斯固定颜色”升级为“嵌入条件标量发射”，赋予了模型吸收帧间残余瞬变的表达能力。消融实验证实，这两个设计独立有效且高度互补——预处理将平均 PSNR 从 22.25 dB 提升至 23.01 dB，发射 MLP 进一步提升至 24.93 dB，完整系统达到 26.14 dB（Table 2）。



### 4.1 光度稳定化与对比度增强

热红外视频序列存在严重的帧间辐射漂移，直接导致多视图几何一致性被破坏。本文提出一种轻量级预处理流水线，包含两个串联步骤：**光度稳定化**与**对比度增强**。

#### 帧间辐射漂移的量化

首先定义相对均值强度变化，用于诊断序列的光度稳定性：

$$\Delta I_{t} = \frac{\mu_{t} - \bar{\mu}}{\bar{\mu}}$$

其中 $\mu_t$ 为第 $t$ 帧的像素均值，$\bar{\mu}$ 为全序列均值。该指标的标准差越大，表明帧间辐射波动越剧烈（见 Figure 2(a)）。

#### 指数滑窗参考 CDF 对齐

为抑制逐帧漂移，维护一个时序平滑的累积分布函数作为对齐目标：

$$F_{t}^{*}(x) = (1-\alpha) F_{t-1}^{*}(x) + \alpha F_{t}(x)$$

其中 $F_t(x)$ 为当前帧的 CDF，$\alpha$ 控制更新速率。随后通过混合映射将当前帧对齐到参考 CDF：

$$I_{t}^{\prime}(x) = (1-\beta) x + \beta F_{t}^{*-1}(F_{t}(x))$$

混合系数 $\beta$ 在保持原始内容与抑制漂移之间取得平衡——$\beta=1$ 为完全对齐，$\beta=0$ 为恒等映射。

#### BBHE 对比度增强

热成像动态范围狭窄，直接训练 3DGS 易导致梯度稀疏。本文采用亮度保持双直方图均衡（BBHE），以均值亮度 $T_t^{\mu}$ 为界分割直方图，对上下子区间独立均衡化：

$$\hat{I}_{t}(x) = \begin{cases} T_{t}^{L}(x), & x \leq T_{t}^{\mu} \\ T_{t}^{U}(x), & x > T_{t}^{\mu} \end{cases}$$

该操作在扩宽动态范围的同时保留整体亮度水平，避免传统全局直方图均衡带来的过增强伪影。实验证实传统直方图均衡反而损害性能（见 Table S1），而 BBHE 能有效提升 SIFT 特征点数量并使空间频谱更接近 RGB 分布（Figure 3）。

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/003_Figure_3.jpg]]
*Figure 3: Photometric stabilization and contrast enhancement (a) An input thermal frame, with less contrast and texture than the corresponding RGB image (b). Notice the photometric drift when compared to reference frame (c), which shows the same scene at a different time point. (d) Our invertible enhancement improves photometric inconsistency and image contrast. (e) Temporal mean intensity across frames showing reduced radiometric drift after stabilization. (f) Normalized spatial frequency spectrum with enhanced thermal data resembling RGB statistics. (g) Our preprocessing expands the effective dynamic range of thermal images, shown with pixel instensity distributions on a sample frame. (h) Improved...*

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/010_Figure_S.2.jpg]]
*Figure S.2: Spatial frequency characteristics of thermal versus RGB images. Thermal images generally exhibit weaker mid- and high-frequency components than RGB images. This is partly due to sensor-resolution limits, but also because heat diffuses across surfaces and through the surrounding air, producing the naturally smoother appearance typical of thermal scenes. As a result, fine texture and sharp edges are often diminished, reducing the highfrequency cues that NeRF and 3D Gaussian Splatting rely on for accurate geometry and appearance estimation. Our pipeline increases contrast and strengthens spatial gradients, making features more distinguishable while unavoidably amplifying noise and discretizati...*

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/012_Figure_S.4.jpg]]
*Figure S.4: Revisit of*

---

### 4.2 嵌入条件发射建模

#### 物理约束的标量辐射表示

与 RGB 3DGS 使用球谐系数建模视角相关颜色不同，热成像本质上是场景自发热辐射的标量测量。本文强制每个 3D 高斯原语仅存储**单一标量发射系数**，摒弃球谐分量。这一物理约束避免了模型将帧间辐射波动错误解释为视角相关效应。

#### 嵌入条件外观 MLP

为吸收预处理后残留的帧间辐射瞬变，引入“野外观”建模策略。每个高斯原语 $i$ 关联一个可学习嵌入 $\mathbf{e}_i^{(g)}$，每帧 $t$ 关联一个可学习嵌入 $\mathbf{e}_t^{(f)}$，二者拼接后经 MLP 映射为标量发射值：

$$c_{i}(t) = f_{\boldsymbol{\theta}}\big(\mathbf{e}_{i}^{(g)}, \mathbf{e}_{t}^{(f)}\big)$$

MLP 采用三层隐藏层（宽度 128），ReLU 激活，线性输出层。该设计的关键洞察在于：**将帧间辐射不一致显式建模为外观变化，而非几何扰动**，从而在不引入漂浮几何伪影的前提下稳定光度。

#### 体积渲染与前景-背景融合

沿光线的渲染遵循标准体积透射公式，使用标量发射值替代 RGB 颜色：

$$\hat{I}_{t}(\mathbf{r}) = \sum_{i} T_{i} \alpha_{i} c_{i}(t)$$

其中 $T_i$ 为累积透射率，$\alpha_i$ 为高斯不透明度。对于远景区域，引入背景 MLP $b_{\phi}$，通过残余透射率 $m(\mathbf{r})$ 与前景高斯渲染融合：

$$\tilde{I}_{t}(\mathbf{r}) = \big(1 - m(\mathbf{r})\big) \hat{I}_{t}(\mathbf{r}) + m(\mathbf{r}) b_{\phi}(\mathbf{d}, \mathbf{e}_{t}^{(f)})$$

背景 MLP 以视线方向 $\mathbf{d}$ 和帧嵌入 $\mathbf{e}_t^{(f)}$ 为输入，确保背景辐射也随帧间变化自适应调整。

#### 热感知损失函数

训练损失由三项加权组成：

$$\mathcal{L} = \lambda_{1} \mathcal{L}_{\mathrm{L1}} + \lambda_{2} \mathcal{L}_{\mathrm{HSSIM}} + \lambda_{3} \mathcal{L}_{\alpha}$$

- $\mathcal{L}_{\mathrm{L1}}$：像素级 L1 重建误差。
- $\mathcal{L}_{\mathrm{HSSIM}}$：热感知结构相似性损失，强调热对比度与结构保持。
- $\mathcal{L}_{\alpha}$：背景正则化项，抑制远景区域的漂浮高斯伪影。

---

### 模块协同机制总结

整个系统的因果链路清晰可追溯：**光度稳定化**抑制帧间均值漂移，为 COLMAP 初始化与 3DGS 训练提供一致的多视图监督；**BBHE 增强**提升动态范围，缓解梯度稀疏问题；**标量发射约束**防止模型将辐射波动误建模为视角效应；**嵌入条件 MLP** 吸收残余瞬变，使几何优化不受外观变化干扰。消融实验（Table 2）证实：预处理单独将平均 PSNR 从 22.25 dB 提升至 23.01 dB，发射 MLP 单独提升至 24.93 dB，二者组合达到 26.14 dB，各组件缺一不可。

### 补充图表

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/001_Figure_1.jpg]]
*Figure 1: Our method overcomes significant challenges in thermal images. Thermal data contain limited texture and lack multispectral cues, making correspondence estimation harder than in RGB. They also exhibit sensor-specific degradations, including (a) frame-to-frame photometric inconsistency from sensor heating, (b) softened transitions between hot and cold regions characteristic of microbolometer sensors, (c) vignetting that produces viewpoint-dependent attenuation, and (d) fixed-pattern noise visible as structured artifacts. Our method explicitly stabilizes the photometry in (a), while the effects in (b–d) are mitigated in our SOTA reconstructions (e) through multiview consistency enabled by a no...*



## 实验与关键发现

### 数据集与评估协议

本文在六个公开热成像多视图数据集上进行评测：**MSX**、**ThermalMix**、**MVTV**、**Lin et al.**、**Ye et al.** 和 **TINSD**。这些数据集涵盖了从建筑立面到室内物体等多种场景，且在辐射稳定性与空间频率特性上存在显著差异（见 Figure 2）。所有方法均在已知相机位姿下训练与测试，评测指标采用 PSNR 和 SSIM。对比基线包括 **NeRF**、**ThermalMix-TS**（基于 Instant-NGP 的快速变体）、**Lin et al.**（RGB-热双分支 NeRF）、**ThermoNeRF** 和 **Thermal3D-GS**。所有对比方法均基于官方开源代码复现，缺失结果已向原作者索取；预处理对所有数据集采用统一参数，未进行场景特化调优。

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/002_Figure_2.jpg]]
*Figure 2: Dataset-level radiometric and spatial-frequency characteristics. (a) Standard deviation of the relative mean-intensity change*

### 主实验结果

Table 1 给出了纯热成像新视角合成的全面定量对比。**Wild Thermal 在所有六个数据集上均取得最优 PSNR 与 SSIM**，且训练时间仅约 11 分钟。具体而言，在 TINSD 数据集上达到 32.94 dB / 0.94，在 Ye et al. 数据集上达到 28.10 dB / 0.92，在最具挑战性的 MSX 数据集上亦达到 23.59 dB / 0.71。值得注意的是，各方法在不同数据集上的性能排序呈现系统性趋势——这与本文在 Section 3 中对数据集难度（辐射稳定性与空间频率特性）的分析高度一致，验证了所提诊断指标的有效性。

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/005_Table_1.jpg]]
*Table 1: Thermal-only NVS comparison across six multiview datasets. We report mean PSNR and SSIM across all scenes for six publicly available datasets. Our analysis of dataset difficulty predicts systematic trends in performance across methods. By designing a pipeline that addresses thermal data challenges directly, we deliver SOTA performance on thermal-only NVS*

定性对比（Figure 5 和 Figure 6）进一步揭示了本文方法的优势。与所有基线方法相比，Wild Thermal 在挑战性场景下产生更锐利的边界和更稳定的背景温度。与当前 SOTA 方法 **Thermal3D-GS** 的对比尤为关键：尽管 Thermal3D-GS 在指标上具有竞争力，但其在几何与纹理重建上存在显著失败——例如 Human0 场景中的窗户、树木和光滑墙面纹理缺失，Lion 场景中的爪部几何失真。本文方法则忠实重建了这些细节。

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/007_Figure_6.jpg]]
*Figure 6: Comparison to Thermal3D-GS. Despite competitive metrics (PSNR in dB left, SSIM right), Thermal3D-GS exhibits significant failures in geometry and texture, while our method shows texture like the Human0 window, tree, and smooth wall, and faithfully reconstructs the Lion paw shape*

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/006_Figure_5.jpg]]
*Figure 5: Comparison to all methods. Representative novel views, PSNR (bottom left, dB), and SSIM (bottom right) across datasets. Our method yields sharper boundaries and more stable background temperature on challenging scenes (top rows), while maintaining competitive quality on easier scenes (bottom rows)*

### 光度一致性的关键作用

Figure 7 通过平滑相机路径渲染实验，直观展示了光度一致性对高质量重建的促进机制。Thermal3D-GS 产生明亮的漂浮结构，这些结构在视角间漂移并严重损害几何稳定性。相比之下，Wild Thermal 的预处理与嵌入条件发射模型有效吸收了帧间辐射异常，未引入漂浮物，几何结构保持稳定。这一实验直接验证了本文核心洞察：**将热成像的帧间辐射不一致视为“野外观”（in‑the‑wild）外观变化，并通过物理约束的标量发射模型进行建模，是在不扭曲几何的前提下实现光度稳定的关键**。

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/008_Figure_7.jpg]]
*Figure 7: Photometric consistency promotes high-quality reconstruction. We render a smooth camera path for our method (top) and Thermal3D-GS (bottom). Thermal3D-GS produces bright floating structures that drift across frames and then assemble into a copy of the photometrically inconsistent training frame (right) when the viewpoint aligns. Our preprocessing and embedding-conditioned emission model handle this outlier without introducing floaters, yielding stable geometry throughout the trajectory*

### 消融实验

Table 2 和 Table S1 提供了详尽的消融分析，量化了各组件对性能的独立贡献与协同效应。

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/009_Table_2.jpg]]
*Table 2: Ablation study. We demonstrate that our preprocessing algorithm and “in-the-wild” architecture (3DGS + Emission MLP) independently improve 3DGS performance, and combining them yields superior results. Additional analysis comparing our method to traditional histogram equalization and evaluating each preprocessing step is provided in Tab. S1*

![[assets/figures/papers/paper_list_l2610_https_arxiv_org_abs_2603_20448/figures/014_Table_S.1.jpg]]
*Table S.1: Ablation study. We demonstrate that our preprocessing steps (constrast enhancement as an improvement over traditional histogram equalization, in combination with photometric stabilization) improve 3DGS performance, but not to the level of our method. We then demonstrate the effect of per-frame embedding ablation, with and without pre-processing*

**光度稳定化与对比度增强**：以原始 3DGS 为基线（平均 PSNR 22.25 dB），单独使用光度稳定化将 PSNR 提升至 23.01 dB，验证了抑制帧间辐射漂移对多视图一致性的直接益处。单独使用对比度增强（BBHE）亦带来小幅提升，而传统直方图均衡（Hist. Eq.）反而损害性能（Table S1），说明亮度保持的双直方图均衡策略对保留热信息至关重要。两者结合使用时，性能进一步提升，证明稳定化与增强具有互补性。

**发射 MLP**：独立使用时，发射 MLP 将平均 PSNR 从 22.25 dB 大幅提升至 24.93 dB，是性能提升最大的单一组件。这表明，即便输入未经光度稳定化，嵌入条件的外观建模仍能吸收相当程度的帧间辐射变化。然而，仅靠发射 MLP 无法完全解决输入端的辐射漂移问题。

**完整系统**：将预处理与发射 MLP 结合后，平均 PSNR 达到 26.14 dB，SSIM 达到 0.88，在所有场景上均优于各消融变体。背景 MLP 的加入进一步提升了远景区域的重建质量。这些结果确证了本文设计的因果逻辑：**预处理在输入端抑制大幅辐射漂移，发射 MLP 在渲染端吸收残余瞬变，两者缺一不可**。

### 失败模式与局限性

尽管 Wild Thermal 在多个数据集上取得了 SOTA 性能，论文仍诚实报告了若干局限性。首先，方法假设相机位姿已知——在实际纯热成像场景中，位姿估计本身极具挑战性，通常需要 IMU 等外部传感器辅助。其次，光度稳定化与对比度增强在扩宽动态范围的同时，不可避免地放大了传感器噪声和离散化伪影；在极低纹理区域，这可能引入结构化瑕疵。此外，发射 MLP 虽能吸收大部分帧间辐射瞬变，但对极端的固定模式噪声或严重晕影可能仍无法完全消除。最后，模型尚未在实时推理约束下验证，且对超出所测数据集分布的传感器类型（如冷却型红外探测器）的泛化性尚未评估。这些局限性为后续研究指明了方向，包括热成像原生位姿估计、动态场景扩展以及更显式的辐射补偿机制等。



## 定位与知识库关联

### 问题定位：热成像 NVS 的“野外观”本质

热红外图像与 RGB 图像存在根本性差异：纹理匮乏、缺乏多光谱线索、动态范围窄，且帧间存在强烈的光度波动和缓慢的辐射漂移（图 2）。这些特性使得依赖稳定光度与纹理线索的 NeRF/3DGS 类方法在纯热输入下难以收敛，常产生漂浮几何伪影。本文将这一问题本质地建模为**“野外观”（in‑the‑wild）外观变化**——即多帧采集条件下同一场景的辐射外观不可控地变化，而非简单的低纹理或低对比度问题。这一视角将热成像 NVS 与 RGB 场景下的“野外观”NeRF 研究（如 NeRF‑W）建立了概念上的联系，但热成像的“野”源于传感器物理而非光照/遮挡变化，因此需要专门的光度稳定化与表示设计。

### 基线方法谱系

本文在六个公开数据集上与以下方法进行了系统对比：

- **NeRF**（Mildenhall et al., ECCV 2020）：经典新视角合成基线，依赖多视图光度一致性，在热成像数据上因帧间辐射漂移而严重退化。
- **ThermalMix‑TS**（基于 Instant‑NGP 的快速 NeRF 变体）：通过哈希编码加速训练，但仍未显式处理热成像的光度不一致问题。
- **Lin et al.**：RGB‑热成像双分支 NeRF 方法，利用 RGB 分支提供几何先验，**依赖额外的 RGB 传感器**，非纯热方案。
- **ThermoNeRF**：针对建筑场景的 RGB‑热成像 NeRF，同样需要 RGB 辅助。
- **Thermal3D‑GS**：物理启发的热成像高斯泼溅方法，是目前纯热 NVS 的 SOTA。其通过物理约束建模热辐射，但**仍使用固定的高斯颜色参数**，无法适应帧间辐射变化，在光度不一致场景下产生漂浮伪影（图 7）。

上述基线中，NeRF 和 ThermalMix‑TS 代表了通用 NVS 方法的直接迁移；Lin et al. 和 ThermoNeRF 代表了多模态融合路线；Thermal3D‑GS 则是与本文最直接可比的纯热方法。

### 方法差异与创新槽位

本文方法“Wild Thermal”在以下关键槽位上与基线形成系统性差异：

1. **输入预处理**：基线方法均使用原始热成像帧。本文引入基于指数滑窗参考 CDF 的直方图对齐（Eq. 3‑4）与亮度保持双直方图均衡 BBHE（Eq. 5），实现光度稳定化与对比度增强。传统直方图均衡（Hist. Eq.）反而损害性能（Table S1），而 BBHE 显著优于前者。

2. **颜色/辐射表示**：3DGS 基线使用 RGB 颜色 + 球谐系数建模视角相关外观。本文用**单通道标量发射值**替代球谐（Section 4.2），符合热成像的物理本质——热辐射是标量而非三通道颜色，且不依赖视角方向。

3. **外观建模**：基线方法每高斯存储固定颜色，无帧间适应性。本文引入**每‑高斯嵌入 e_i^{(g)} 与每‑帧嵌入 e_t^{(f)}**，经 MLP 映射为标量发射值 c_i(t)（Eq. 6），显式吸收帧间残余辐射变化。这一设计与 NeRF‑W 的外观嵌入思路一致，但适配了热成像的单通道标量特性。

4. **背景建模**：引入背景 MLP 与前景‑背景融合（residual transmittance，Eq. 8），处理远景区域的辐射建模。

5. **损失函数**：在 L1 + SSIM 基础上，引入热感知 SSIM（L_HSSIM）与背景正则化（L_α），抑制漂浮伪影。

### 适用边界与局限

**已知位姿假设**：方法假设相机位姿已知（由 COLMAP 或外部传感器提供）。实际场景中，纯热成像的位姿估计仍极具挑战性——低纹理和高噪声导致特征匹配失败率高。本文的预处理通过提升 SIFT 特征点数量（图 3h）部分缓解了这一问题，但完整的无外部辅助 NVS 流程仍需要更鲁棒的热成像原生位姿估计方法。

**传感器噪声放大**：光度稳定化与 BBHE 对比度增强不可避免地放大了传感器噪声和离散化伪影。在极低纹理区域（如均匀温度墙面），增强后的图像可能引入结构化瑕疵，被 3DGS 误认为真实几何。

**残余辐射伪影**：发射 MLP 虽能吸收大部分帧间辐射瞬变，但对极端的固定模式噪声（如非均匀性校正残留）或严重晕影（vignetting）可能仍无法完全消除。这些效应在空间上非均匀且与场景内容耦合，超出了当前嵌入条件外观建模的表达能力。

**泛化性未验证**：模型在六个公开数据集上验证，但所有数据集均使用非制冷型微测辐射热计传感器。对冷却型红外探测器（更高灵敏度、不同噪声特性）或长波/中波红外不同波段的泛化性尚未评估。此外，训练时间约 11 分钟，尚未在实时推理约束下验证。

### 开放问题

1. **端到端联合优化**：当前预处理与重建分离，光度稳定化参数（α, β）为固定值。能否将光度稳定化与三维重建联合优化，使预处理参数根据下游重建损失自适应调整？

2. **热成像原生位姿估计**：如何发展更鲁棒的热成像专用特征提取与匹配方法，使完整 NVS 流程真正独立于 RGB 或 IMU 辅助？预处理带来的 SIFT 特征增益是一个有希望的起点，但需要更根本的特征设计。

3. **动态场景扩展**：当前方法假设静态场景。热成像中运动物体（如行人、车辆）的温度变化与帧间辐射漂移耦合，如何解耦并同时保持帧间光度一致性？

4. **外观嵌入的表达上限**：针对低纹理、大基线、严重辐射偏移等极端情形，当前嵌入条件外观建模的表达能力上限在哪里？是否需要更显式的物理辐射补偿模块（如传感器响应函数反演）作为补充？



## 原文 PDF

![[paperPDFs/CVPR_2026/Thermal_is_Always_Wild_Characterizing_and_Addressing_Challenges_in_Thermal_Only_Novel_View_Synthesis.pdf]]
