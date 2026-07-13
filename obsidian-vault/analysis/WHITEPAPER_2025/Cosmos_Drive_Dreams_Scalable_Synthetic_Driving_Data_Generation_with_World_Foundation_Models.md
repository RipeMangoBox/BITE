---
title: "Cosmos-Drive-Dreams: Scalable Synthetic Driving Data Generation with World Foundation Models"
type: paper
paper_level: A
venue: Whitepaper
year: 2025
pdf_ref: paperPDFs/WHITEPAPER_2025/Cosmos_Drive_Dreams_Scalable_Synthetic_Driving_Data_Generation_with_World_Foundation_Models.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/cosmos_drive_dreams/
aliases:
- CDDCDMS
- Cosmos-Drive-Dreams
tags:
- WHITEPAPER_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "利用预训练世界基础模型（WFM）并对其进行驾驶领域后训练，通过HDMap结构化条件控制视频布局、LLM驱动的提示词改写扩展场景多样性，生成可控、多视角一致的合成视频数据，以可控方式扩充训练集中的长尾场景。"
primary_logic: "通过将通用WFM的物理世界先验迁移到驾驶场景，结合精确的几何条件（HDMap）与语言引导的多样性控制，Cosmos-Drive-Dreams能够生成高保真、布局准确、多视角一致的驾驶视频，从而作为合成数据有效缓解长尾问题，提升下游任务精度和数据效率。"
claims:
- "在Waymo和RDS-HQ数据集上，引入SDG后3D车道线检测F1分数显著提升，尤其在雨雾天气下提升超过9-10%（相对提升）。"
- "对于3D目标检测，仅使用1K真实片段配合SDG数据，性能可媲美9.3倍的真实数据，且在加入大量真实数据后SDG仍能带来增益。"
- "在LiDAR-based 3D目标检测中，加入SDG数据后mAP从0.240提升至0.250（1K设定），证实SDG对多模态检测有效。"
- "在驾驶策略学习中，添加SDG数据持续降低minADE，且仅需更少的真实数据即可达到相同轨迹预测精度，并改善弱势道路使用者等长尾场景。"
---

# Cosmos-Drive-Dreams: Scalable Synthetic Driving Data Generation with World Foundation Models

> [!tip] 核心洞察
> 通过将通用WFM的物理世界先验迁移到驾驶场景，结合精确的几何条件（HDMap）与语言引导的多样性控制，Cosmos-Drive-Dreams能够生成高保真、布局准确、多视角一致的驾驶视频，从而作为合成数据有效缓解长尾问题，提升下游任务精度和数据效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Cosmos-Drive-Dreams：基于世界基础模型的可扩展合成驾驶数据生成 |
| 英文题名 | Cosmos-Drive-Dreams: Scalable Synthetic Driving Data Generation with World Foundation Models |
| 会议/期刊 | Whitepaper 2025 |
| Links | [paper](https://arxiv.org/abs/2506.09042) · [Project](https://research.nvidia.com/labs/toronto-ai/cosmos_drive_dreams) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Cosmos-Drive-Dreams (with Cosmos-Drive model suite) |
| Dataset | RDS-HQ / Waymo (3D Lane Detection), RDS-HQ-HL (3D Object Detection, 1K real setting B), RDS-HQ (LiDAR-based 3D Detection, 1K), RDS-Bench[Policy] (Trajectory Prediction) |

> [!tip] 效果简介
> - RDS-HQ / Waymo (3D Lane Detection) 上，F1-score 为 0.871 (RDS-HQ All) / 0.855 (Waymo All) with R_s2r=1，对比 0.852 (RDS-HQ) / 0.847 (Waymo) original，变化 +0.019 / +0.008。
> - RDS-HQ-HL (3D Object Detection, 1K real setting B) 上，LET-AP relative improvement 为 +55.0% relative to real only, +14.5% absolute LET-AP boost，对比 Only 1K real clips，变化 +14.5% LET-AP。
> - RDS-HQ (LiDAR-based 3D Detection, 1K) 上，mAP 为 0.250 (with SDG LiDAR data)，对比 0.240 (real only)，变化 +0.010。

## 概要

### 问题瓶颈

自动驾驶感知与规划模型在长尾（corner-case）场景下的泛化能力，受限于真实多视角驾驶数据的稀缺和高昂的标注成本。极端天气、罕见道路布局、弱势道路使用者等场景在训练集中天然不足，导致下游模型在这些情况下性能急剧退化。

### 核心思路

Cosmos-Drive-Dreams 提出了一条基于**世界基础模型（World Foundation Model, WFM）**的可控合成数据生成管道。其核心逻辑是：将通用 WFM 在物理世界中习得的先验迁移到驾驶域，通过**高精地图（HDMap）结构化条件**实现像素级布局控制，同时利用**LLM 驱动的提示词重写**扩展场景多样性，从而以可控方式生成高保真、多视角一致、覆盖长尾分布的合成驾驶视频。这些合成数据直接混入下游任务训练集，以极低的真实数据成本显著提升模型在罕见场景下的鲁棒性。

### 方法定位

该方法属于**基于生成模型的合成数据增强**范式，区别于传统的基于 3D 引擎物理模拟或图像级增强（如 **Albumentations**, Buslaev et al., Information 2020）的方案。其关键差异化在于：

- **生成范式**：以预训练 WFM 为基座，经驾驶域后训练获得可控视频生成能力，而非依赖手工构建的 3D 场景。
- **布局控制**：通过 HDMap 投影视频与 LiDAR 深度作为 ControlNet 条件，实现像素级对齐的精确几何约束，替代传统的人工标注或 3D 重建。
- **多视图一致性**：引入 Single2Multiview 模型，从单视图扩展至多视图（最多 6 个），确保跨视角时空一致，区别于单视图分别生成。
- **质量保障**：采用 VLM（Qwen2.5-VL-7B-Instruct）进行自动视觉质量评估与拒绝采样，替代人工抽查。

管道由四个步骤构成（Figure 2）：➊ 像素对齐 HDMap 条件视频生成；➋ 提示词重写与单视图生成；➌ 多视图扩展；➍ VLM 拒绝采样。

### 主要结果

在下游任务上的实验表明，合成数据对长尾场景的增益尤为显著：

- **3D 车道线检测**：在 Waymo 和 RDS-HQ 数据集上，引入 SDG 后 F1 分数分别提升至 0.855 和 0.871；在雨雾等极端天气下，相对提升超过 9–10%（Table 1）。
- **3D 目标检测**：仅使用 1K 真实片段配合 SDG 数据，性能增益（+14.5% LET-AP）相当于将真实数据扩大 9.3 倍；多视角 SDG 相比单视图进一步推高检测精度（Figure 16）。
- **LiDAR-based 3D 检测**：在 1K 真实数据设定下，加入 SDG 后 mAP 从 0.240 提升至 0.250，验证了该方法对多模态检测的有效性（Table 3）。
- **驾驶策略学习**：添加 SDG 数据持续降低轨迹预测的 minADE，且仅需更少的真实数据即可达到相同精度；针对 VRU/left 等特定长尾场景的定向 SDG 注入，能提升预测准确度而不损害整体表现（Figure 20, Table 4）。

### 局限与待验证问题

当前管道依赖计算密集的扩散模型，大规模生成耗时且资源需求高。自动标注模型（Cosmos-7B-Annotate-Sample-AV）在不同环境下的鲁棒性尚未全面评估。此外，VLM 过滤器的失效模式、生成数据规模的饱和效应、向其他传感器模态的推广，以及推理成本的显著降低，均为待探索的开放问题。



自动驾驶系统在真实世界中部署的核心挑战之一，是长尾（极端）驾驶场景下真实多视角数据的极度稀缺与高昂的标注成本。尽管现有数据集在常规天气和交通条件下已积累了大量样本，但雨、雪、雾等恶劣天气，以及涉及弱势道路使用者、罕见障碍物等边缘案例的覆盖仍然严重不足。这种数据分布的长尾特性直接导致下游感知与规划模型在罕见情况下泛化能力不足，成为制约自动驾驶安全性的关键瓶颈。

当前缓解数据稀缺问题的主流方案可分为两类。一类是基于传统图像增强的方法，如 **Albumentations**（Buslaev et al., Information 2020），通过对已有图像施加颜色抖动、模糊、噪声等像素级变换来模拟环境变化。这类方法操作简单，但无法改变场景的几何结构或引入新的语义内容，对长尾场景多样性的扩展能力极为有限。另一类是基于物理引擎或三维重建的传感器仿真，能够生成具有精确几何标注的合成数据，但其场景构建高度依赖人工建模，难以创造完全新颖的极端场景，且生成数据的视觉真实感往往与真实域存在明显差距。

近年来，世界基础模型（World Foundation Model, WFM）的兴起为合成数据生成开辟了新的可能性。这类模型在海量视频数据上预训练，内化了丰富的物理世界先验，具备从条件信号生成高保真、时序一致视频的能力。然而，将通用WFM直接应用于驾驶场景面临两个核心缺口：其一，通用模型缺乏对驾驶场景几何约束（如道路布局、车道线走向）的精确控制能力，生成的视频可能违背物理合理性；其二，如何系统性地将WFM的生成能力转化为可量化的下游任务增益，在自动驾驶评测基准上形成闭环验证，此前尚无完整方案。

本文的核心动机在于：**利用预训练世界基础模型的物理世界先验，通过驾驶领域后训练与结构化条件控制，构建一个可扩展的合成驾驶数据生成管线，以可控方式系统性地扩充训练集中的长尾场景，从而提升下游感知与规划模型在罕见情况下的泛化能力与数据效率。**



## 核心方法与创新机理

Cosmos-Drive-Dreams 的核心创新并非单一算法突破，而是一套**将通用世界基础模型（WFM）的物理先验迁移至自动驾驶领域的可控合成数据生成体系**。其关键创新体现在以下四个“changed slots”上，它们共同构成了从“仿真模拟”到“生成式数据工厂”的范式跃迁。

### 1. 数据生成范式：从物理模拟到世界模型生成

传统自动驾驶合成数据管线依赖基于3D引擎的物理模拟或场景重建（如传感器仿真），其瓶颈在于**难以经济地创造全新的极端场景**——模拟器需要人工构建3D资产、定义物理规则，长尾场景的覆盖成本随多样性需求指数增长。

Cosmos-Drive-Dreams 将范式切换为**基于预训练世界基础模型的可控视频生成**。其起点是 NVIDIA Cosmos-1 世界基础模型，该模型在海量互联网视频上预训练，内化了关于物理世界动态、光照、几何的丰富先验。通过对该模型进行**驾驶领域后训练**（在 RDS 数据集上微调），得到驾驶专用的 WFM，再进一步后训练为三个专用模型（Cosmos-Transfer1-7B-Sample-AV、Cosmos-7B-Single2Multiview-Sample-AV、Cosmos-7B-Annotate-Sample-AV），构成 Cosmos-Drive 模型套件（Figure 3）。这一范式的核心优势在于：**生成模型可以从布局条件（HDMap）和文本提示词的组合空间中“想象”出训练集中从未出现过的场景**，例如同一路口在晴天、暴雨、火灾、樱花季等不同条件下的视觉呈现（Figure 5），从而以可控方式系统性扩充长尾场景。

### 2. 布局控制机制：从人工标注到像素对齐的 HDMap 条件

传统方法实现精确的场景布局控制通常依赖人工标注或完整的3D场景构建，成本高昂且难以规模化。Cosmos-Drive-Dreams 创新性地引入**从高精地图（HDMap）渲染的像素对齐条件视频**作为生成控制信号。

具体而言，管道第一步（Step ➊）将结构化标签中的 HDMap 元素（车道线、路沿、人行横道等）投影到相机平面，渲染为与目标视频帧逐像素对齐的 HDMap 视频；同时可选择性加入 LiDAR 深度信息作为额外条件。该条件视频随后作为 ControlNet 的输入，驱动 Cosmos-Transfer1-7B-Sample-AV 进行布局精确控制的视频生成（Section 2.3）。这种设计使得**生成视频的道路结构、车道几何与真实地图严格一致**，同时允许外观（天气、光照、纹理）在文本提示词引导下自由变化——实现了“几何可控、外观多样”的解耦生成。

### 3. 多视图一致性：从单视图到跨视角联合生成

多视图一致性是自动驾驶感知模型训练的核心需求，但传统方法要么逐视图独立生成（导致视角间不一致），要么依赖复杂的3D重建管线。Cosmos-Drive-Dreams 通过 **Single2Multiview 模型**（Cosmos-7B-Single2Multiview-Sample-AV）实现了从单视图到多视图的扩展生成。

该模型以单视图视频为输入，同时生成最多5个输出视图（前、后、左、右等），其 DiT 架构中引入了专门的 **MV transformer block**（Figure 7），通过联合注意力机制在去噪过程中隐式建模跨视图的几何与外观一致性。训练时从5个输出视图中随机选择3个与输入视图组成 batch，推理时则一次性生成全部5个输出视图（Section 2.4）。此外，多视图 ControlNet 同样支持 HDMap 或 LiDAR 条件输入，确保所有生成视图共享相同的场景布局。这一设计使得 **SDG 数据天然具备多视图时空一致性**，无需后处理对齐。

### 4. 数据质量筛选：从人工抽查到 VLM 自动拒绝采样

生成数据的质量控制是合成数据实用化的关键瓶颈。传统方法依赖人工抽查或简单规则过滤，难以规模化且标准不一致。Cosmos-Drive-Dreams 引入**基于视觉语言模型（VLM）的自动拒绝采样机制**（Step ➍）。

具体采用 Qwen2.5-VL-7B-Instruct 对每条生成视频进行视觉质量评估，自动识别并丢弃存在物体消失、形状畸变、严重伪影等问题的低质量样本。实验表明，拒绝采样丢弃约 **3%** 的生成样本（Section 3.3），在保证数据集整体质量的同时不显著减少有效数据量。Figure 13 和 Figure 14 展示了在 Waymo 和 RDS-HQ 合成数据上被丢弃的典型样本，验证了该过滤器的实际效果。这一机制使得大规模 SDG 管线具备了**闭环的自动化质量保障能力**。

---

**综上**，Cosmos-Drive-Dreams 的创新本质在于将世界基础模型的生成能力、HDMap 的几何约束、多视图联合建模和 VLM 自动质检整合为一个**可扩展的自动驾驶数据飞轮**（Figure 1 Left），实现了从“真实数据稀缺”到“可控合成数据充裕”的关键跨越。



Cosmos-Drive-Dreams 的生成管线围绕一个核心瓶颈展开：自动驾驶中长尾（极端）驾驶场景的真实多视角数据稀缺且标注成本高昂，导致下游感知与规划模型在罕见情况下泛化能力不足。为解决这一问题，管线利用预训练世界基础模型（WFM）的物理世界先验，结合高精地图（HDMap）结构化条件控制视频布局、LLM驱动的提示词改写扩展场景多样性，生成可控、多视角一致的合成驾驶视频，以可控方式扩充训练集中的长尾场景（Figure 2）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Cosmos-Drive-Dreams pipeline. Starting from either structured labels or in-the-wild video, we generated pixel-aligned HDMap condition video (Step ➊). Then we leverage a prompt rewriter to generate diverse prompts and synthesize single-view videos (Step ➋). Each single-view video is then expanded into multiple views (Step ➌). Finally, a Vision-Language Model (VLM) filter performs rejection sampling to automatically discard low-quality samples, yielding a high-quality, diverse SDG dataset (Step ➍)*

管线由四个串行模块构成，形成“条件构建→多样性提示→多视角扩展→质量过滤”的生成流水线：

1. **步骤➊：像素对齐HDMap条件视频生成。** 从结构化标签或in-the-wild视频出发，通过 Cosmos-7B-Annotate-Sample-AV 模型渲染 HDMap 投影和 LiDAR 深度视频，作为后续生成的精确布局条件。该步骤确保下游生成模型能够获得像素级对齐的几何约束，而非仅依赖文本描述。

2. **步骤➋：提示词重写与单视图生成。** 使用 Qwen2.5-7B-Instruct 根据原视频字幕自动生成天气、时间、光照等多样化的新提示词，然后由 Cosmos-Transfer1-7B-Sample-AV 基于 HDMap 条件生成单视图视频。该模型采用 ControlNet 架构，以 HDMap 视频（可选 LiDAR 深度）为条件输入，在保持精确布局控制的同时，通过文本提示引入场景多样性（Figure 5）。

3. **步骤➌：多视图扩展。** 利用 Cosmos-7B-Single2Multiview-Sample-AV 将前视图视频扩展为多视角（前、后、左、右等最多6个视角）一致性视频。该模型从 Cosmos-7B-Multiview-Sample-AV 微调而来，训练时选取输入视图和任意3个输出视图，推理时同时生成全部5个输出视图（Figure 7）。

4. **步骤➍：VLM拒绝采样。** 采用 Qwen2.5-VL-7B-Instruct 评估生成视频的视觉质量，自动过滤存在物体消失、形状畸变等伪影的视频。实验数据显示拒绝率约3%，在保证视觉质量的同时不显著减少有效数据量（Figure 13, Figure 14）。

管线支持两种启动模式：从结构化标签（如 RDS-HQ 数据集）出发，直接渲染 HDMap 条件；或从 in-the-wild 无标注视频（如 Nexar Dashcam 碰撞预测数据集）出发，先由 Cosmos-7B-Annotate-Sample-AV 自动预测 HDMap 和深度，再进入后续生成流程（Figure 8）。此外，管线还包含 LiDAR 数据生成分支（Cosmos-7B-LiDAR-GEN-Sample-AV），可将 LiDAR 点云转换为 range map 表示后，基于 HDMap 或 RGB 图像条件生成合成 LiDAR 数据（Figure 11），并支持不同天气提示下的物理特性变化（如雨天增加射线衰减，Figure 12）。

整个生成管线以 Cosmos-Drive 模型套件为引擎，该套件由通用 WFM（NVIDIA Cosmos-1）经驾驶领域后训练得到，包含精确布局控制、多视角扩展、野生视频标注和 LiDAR 生成四个专用模型（Figure 3）。这种“通用WFM→领域后训练→专用模型”的范式，使得管线能够将物理世界先验迁移到驾驶场景，同时保持对布局、视角和传感器模态的精确控制。



Cosmos-Drive-Dreams 的生成管线由四个核心模块串联构成，每个模块针对合成数据的一个关键质量维度进行专门设计。

### 模块一：像素对齐 HDMap 条件视频生成

该模块负责将结构化标签或 in-the-wild 视频转化为精确的几何条件信号。对于结构化标签，直接从高精地图渲染 HDMap 投影视频和 LiDAR 深度视频；对于无标注的野生视频，则通过 **Cosmos-7B-Annotate-Sample-AV** 自动预测 HDMap 与深度信息。该模型由 Cosmos-7B-Sample-AV 改造而来，将原有的文本嵌入替换为输出嵌入，使其能够从单目视频中推断场景的几何布局。渲染后的 HDMap 视频作为后续生成模块的 ControlNet 条件输入，确保生成视频的道路结构、车道线位置与真实场景像素级对齐。

### 模块二：提示词重写与单视图生成

为扩展场景多样性，采用 **Qwen2.5-7B-Instruct** 作为提示词重写器，根据原始视频字幕自动生成天气、时间、光照等维度的多样化文本描述。随后，**Cosmos-Transfer1-7B-Sample-AV** 基于 HDMap 条件视频和重写后的提示词生成单视图驾驶视频。该模型以预训练世界基础模型 Cosmos-7B-Sample-AV 为基座，通过 ControlNet 机制注入 HDMap 条件，实现精确的布局控制。训练在 RDS-HQ 数据集上进行，batch size 64，学习率 $5 \times 10^{-5}$，共 25K 步。

### 模块三：多视图扩展

**Cosmos-7B-Single2Multiview-Sample-AV** 将前视图视频扩展为多视角一致性视频（最多 6 个视角）。其核心设计在于输入结构：将干净输入视图 token、带噪多视图 token、全局逐视图嵌入 token 以及输入/输出二值指示符拼接后送入 DiT。训练时随机选择输入视图和 3 个输出视图组成 batch；推理时同时生成全部 5 个输出视图。该模型从 Cosmos-7B-Multiview-Sample-AV 微调而来，基座模型在 2,000 小时内部驾驶数据上预训练（batch size 32，学习率 $5 \times 10^{-5}$，30K 步），随后在 RDS-HQ 多视图视频上训练 HDMap 和 LiDAR ControlNet（20K 步），以实现多视图条件下的精确场景布局控制。

### 模块四：VLM 拒绝采样

采用 **Qwen2.5-VL-7B-Instruct** 作为视觉质量评估器，自动检测生成视频中的物体消失、形状畸变等伪影，丢弃约 3% 的低质量样本，在保障数据集质量的同时不显著减少有效数据量。

### LiDAR 生成与坐标转换

LiDAR 数据以 range map 形式表示，需将点云从笛卡尔坐标 $(x, y, z)$ 转换为球坐标 $(r, \theta, \phi)$：

$$r = \sqrt{x^2 + y^2 + z^2}, \quad \phi = \arctan 2(y, x), \quad \theta = \arcsin(z / r).$$

其中 $r$ 为径向距离，$\phi$ 为方位角，$\theta$ 为仰角。需注意，原始 LiDAR 数据通常经过运动补偿，为准确投影到 range map，必须反转该补偿并估计每个点的时间戳。**Cosmos-7B-LiDAR-GEN-Sample-AV** 以 HDMap 或 RGB 图像为条件生成 LiDAR range map，并通过专门微调的 Cosmos LiDAR tokenizer 重建高质量点云。该 tokenizer 在 RDS-HQ 数据集上微调 30K 步，能够高保真地恢复 LiDAR 输入的几何结构。



## 实验与关键发现

### 核心实验设计

Cosmos-Drive-Dreams 的评估围绕一个核心命题展开：**合成数据能否在真实数据稀缺的条件下，系统性地提升下游驾驶任务的性能与数据效率**。实验覆盖 3D 车道线检测、3D 目标检测（含纯视觉与 LiDAR 多模态）以及驾驶策略学习三类任务，在 RDS-HQ、RDS-HQ-HL、Waymo 和 RDS-Bench 等多个基准上验证。实验设计遵循严格的公平性原则：所有下游任务采用相同的检测器架构（LATR、BEVFormer、Transfusion）与训练配置，真实数据量受控，合成数据以固定比例 $R_{s2r}$ 混入训练集。

### 3D 车道线检测：长尾天气下的显著增益

在 RDS-HQ 和 Waymo 两个数据集上，引入 Cosmos-Drive-Dreams 生成的合成数据后，3D 车道线检测的 F1 分数均获得一致提升（Table 1）。当使用全部真实数据并混入 $R_{s2r}=1$ 的合成数据时，RDS-HQ 上 F1 从 0.852 提升至 0.871（+0.019），Waymo 上从 0.847 提升至 0.855（+0.008）。对比传统增强方法 **Albumentations**（Buslaev et al., Information 2020），Cosmos-Drive-Dreams 在所有设定下均表现出更优或相当的性能。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/018_Table_1.jpg]]
*Table 1: 3D lane detection performance with Cosmos-Drive-Dreams. Our pipeline significantly improves the 3D lane detection performance over baseline and Albumentations [5]. “Cate. Acc.” means category accuracy*

**长尾场景的收益更为突出**。在仅使用 2k 真实片段（极低数据量）的设定下，全天气 F1 提升 6.0%，雾天场景 F1 提升 9.4%（Figure 15）。这直接验证了合成数据对缓解长尾分布问题的有效性——模型在罕见天气条件下获得了原本稀缺的训练信号。数据缩放曲线显示，合成数据在所有真实数据量级上均带来增益，且在真实数据极少时收益最大，随着真实数据增加，增益趋于平缓但仍保持正向。

### 3D 目标检测：合成数据媲美数倍真实数据

在 RDS-HQ-HL 的 3D 目标检测任务上，仅使用 1K 真实片段训练的基线模型性能有限；加入 SDG 数据后，LET-AP 绝对提升 14.5%，相对提升 55.0%（Figure 16 左）。这一增益幅度**相当于将真实数据量扩大约 9.3 倍**——换言之，合成数据在极端数据稀缺场景下展现出极高的数据效率。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/021_Figure_16.jpg]]
*Figure 16: Cosmos-Drive-Dreams generated data improves detection performance at various scales on RDS-HQ-HL (setting B ). Left: Adding Cosmos-Drive-Dreams generated data from RDS-HQ to RDS-HQ-HL train-set significantly improves performance on RDS-HQ-HL test-set. Performance improvement from the addition of SDG data to 1K real clips (55.0% relative to only real, +14.5% in LET-AP) is comparable to 9.3× increase in real data. Center: Cosmos-Drive-Dreams generated multiview data significantly improves performance on RDS-HQ-HL in the multi-view setting. Right: Performance increases correlate steadily with the amount of SDG data added for all tested amounts of real data*

多视角合成数据的价值在消融实验中得到证实：多视角 SDG 相比单视图 SDG 进一步提升了 3D 检测性能（Figure 16 中），证明多视一致性合成对空间感知任务至关重要。此外，性能随 SDG 数据量增加而单调上升，且在所有真实数据量级下均保持正向趋势（Figure 16 右），未观察到明显的饱和现象。

在设定 Q（全量真实数据增强）下，Cosmos-Drive-Dreams 在通用天气和极端天气条件下均改善了检测性能（Table 2），进一步验证了合成数据作为通用数据增强策略的普适性。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/020_Table_2.jpg]]
*Table 2: 3D object detection performance with Cosmos-Drive-Dreams. When applied to augment training set (setting $\pmb { \mathbb { Q } }$ ) , Cosmos-Drive-Dreams improves the detection performance in general and extreme weather conditions

### LiDAR 多模态检测：跨模态有效性

Cosmos-Drive-Dreams 不仅生成视觉数据，还通过 Cosmos-7B-LiDAR-GEN-Sample-AV 生成 LiDAR 点云数据。在 LiDAR-based 3D 目标检测任务中，使用 1K 真实片段设定，加入 SDG LiDAR 数据后 mAP 从 0.240 提升至 0.250（+0.010，Table 3）。这一结果表明合成数据对多模态感知同样有效，且生成管线能够产生与真实传感器数据分布兼容的 LiDAR 表示。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/023_Table_3.jpg]]
*Table 3: LiDAR-based 3D object detection performance with Cosmos-Drive-Dreams. Cosmos-Drive-Dreams improves the overall detection performance*

### 驾驶策略学习：数据效率与长尾定向优化

在 RDS-Bench[Policy] 的轨迹预测任务上，添加 SDG 数据持续降低 minADE（Figure 20 左）。数据效率分析表明，达到相同 minADE 1.35 的目标，使用合成数据只需约 50k 真实片段（配合 $R_{s2r}=0.5$），而纯真实数据需要约 60k——**减少了约 17% 的真实数据需求**（Figure 20 中）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/027_Figure_20.jpg]]
*Figure 20: Policy learning. Left: Given an amount of real-world clips, adding SDG data improves trajectory prediction accuracy (minADE on RDS-Bench[Policy], lower is better). Center: Less real-world data is needed to reach a target minADE. Right: Adding a small amount of targeted SDG data can improve performance for certain corner cases (RDS-Bench[VRU/left], without hurting overall driving performance*

更具实践价值的是**定向长尾优化**：针对弱势道路使用者（VRU）和左转等特定长尾场景添加少量定向 SDG 数据，可提升这些场景的预测准确度，同时不影响整体驾驶性能（Figure 20 右，Table 4 右）。这展示了合成数据在“按需生成”方面的独特优势——开发者可以针对模型暴露的薄弱场景定向扩充训练集，而非盲目增加数据量。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/025_Table_4.jpg]]
*Table 4: Policy learning performance. Left: Cosmos-Drive-Dreams improves the trajectory prediction accuracy on RDS-Bench[Policy]. Right: Small amount of targeted SDG data can improve predictions in corner cases (RDS-Bench[VRU/left])*

### 质量控制的消融：拒绝采样的作用

VLM 拒绝采样（基于 Qwen2.5-VL-7B-Instruct）丢弃约 3% 的生成样本（Section 3.3），这些样本存在物体消失、形状畸变等明显伪影（Figure 13、Figure 14 展示典型丢弃案例）。3% 的低拒绝率表明生成管线本身具有较高的基础质量，而拒绝采样在几乎不损失有效数据量的前提下，为数据集质量提供了自动化的安全网。

### 失败模式与局限性

尽管整体性能提升显著，实验中也暴露出一些值得关注的问题：

1. **生成质量的下限**：VLM 过滤器丢弃的样本揭示了扩散模型的典型失败模式——物体形态畸变、小物体消失、跨帧不一致等。这些伪影在极端天气或复杂光照条件下更为突出（Figure 13、Figure 14）。

2. **计算成本瓶颈**：整个生成管线依赖大规模扩散模型（Cosmos-Transfer1-7B、Single2Multiview 等），单次推理计算开销大，大规模数据生成耗时显著。这限制了实时或近实时数据增强的应用前景。

3. **自动标注模型的鲁棒性未充分验证**：Cosmos-7B-Annotate-Sample-AV 的 HDMap 和深度预测精度在不同环境条件下的表现尚未全面量化评估，其误差可能向下游生成传播。

4. **性能增益的饱和趋势**：数据缩放曲线（Figure 15、Figure 16 右）显示，当真实数据量足够大时，合成数据的边际增益递减。如何在高数据量区间保持显著的增量价值，是后续优化的方向。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/019_Figure_15.jpg]]
*Figure 15: Cosmos-Drive-Dreams improves F-score across varying amounts of real-world training data on 3D Lane Detection task. SDG clips are mixed with real clips using a ratio of R _ { s 2 r } = 0 . 5 . Left: Results on testing dataset. Under all weather conditions, SDG consistently improves detection performance across varying amounts of real-world training data, with the most significant gain (+6.0%) observed in the low-data regime (2k clips). Right: Results on the extreme weather subset of the testing dataset. In more challenging settings (Rainy and Foggy), the benefits of SDG are even more pronounced—showing gains of up to +9.4% under foggy conditions with only 2k real clips. This highlights SDG’s...*

### 开源资产

Cosmos-Drive 开源了包括 RDS-HQ 子集、预训练模型权重、推理脚本和定制化工具在内的完整资产（Table 5），为社区复现和扩展提供了基础。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/001_Figure_1.jpg]]
*Figure 1: Left: Autonomous Vehicle Data Flywheel enabled by Cosmos-Drive-Dreams. The cycle illustrates a continuous feedback loop for improving autonomous driving models with synthetic data generation. Right: Cosmos-Drive generates high-quality and diverse synthetic videos with multi-view and LiDAR modality support*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/011_Figure.jpg]]
*Figure: Elevation angle profile Beam zig-zag pattern Range map representation*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/029_Figure_21.jpg]]
*Figure 21: Distribution for weather, time of day, and scenario of our RDS-HQ subset*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2506_09042_fixed_weights/figures/024_Figure_18.jpg]]
*Figure 18: Visualization of LiDAR-based 3D object detection on RDS-HQ (2k) dataset after adding Cosmos-Drive-Dreams*



## 定位与知识库关联

### 核心范式定位

Cosmos-Drive-Dreams 处于**世界基础模型（WFM）驱动的合成数据生成**这一新兴范式，其技术路径可概括为：以预训练通用WFM的物理世界先验为基座，通过驾驶领域后训练将其迁移至自动驾驶场景，再结合精确几何条件控制与语言引导的多样性扩展，生成可控、多视角一致、高保真的合成驾驶视频。这与传统数据增强和基于物理仿真的数据生成形成根本性差异。

### 与基线方法的关键差异

**传统图像增强（Albumentations）**（Buslaev et al., Information 2020）仅对已有图像进行像素级变换（如色彩抖动、几何扰动），无法创造新的场景布局或天气条件，对长尾问题的缓解能力极为有限。实验表明，在3D车道线检测任务中，Albumentations的增益远低于Cosmos-Drive-Dreams（Table 1），后者在雨雾天气下F1分数相对提升超过9-10%。

**基于物理模拟或3D重建的仿真方法**依赖精确的3D场景建模和渲染引擎，虽然能生成几何准确的传感器数据，但创造全新极端场景（如火灾、暴雪中的异常物体）的成本极高，且生成内容的视觉真实感和多样性受限于手工构建的资产库。Cosmos-Drive-Dreams通过扩散模型的生成能力绕过了这一瓶颈——从同一HDMap条件出发，仅需改变文本提示词即可生成从晴朗白天到火灾混乱场景的多样化视频（Figure 5）。

**单视图或独立多视图生成方法**通常难以保证跨视角的时空一致性。Cosmos-Drive-Dreams通过专门的Cosmos-7B-Single2Multiview-Sample-AV模型，从前视图一次性扩展生成最多6个视角的一致视频（Section 2.4），并在训练中采用“输入视图+随机3个输出视图”的策略学习多视一致性。消融实验证实，多视图SDG相比单视图能进一步提升3D目标检测性能（Figure 16 center panel）。

### 方法谱系中的继承与创新

Cosmos-Drive-Dreams继承自NVIDIA Cosmos-1世界基础模型（WFM），其关键创新在于**驾驶领域的深度特化**：

1. **WFM → 驾驶WFM**：在RDS数据集上对通用WFM进行后训练，使其理解驾驶场景的特定动态和几何结构（Section 2.2）。
2. **驾驶WFM → 三个专用模型**：进一步后训练为布局控制模型（Cosmos-Transfer1-7B-Sample-AV）、多视图扩展模型（Cosmos-7B-Single2Multiview-Sample-AV）和野生视频标注模型（Cosmos-7B-Annotate-Sample-AV），形成完整的模型套件（Figure 3）。
3. **ControlNet机制**：采用ControlNet架构（Zhang et al., ICCV 2023）将HDMap渲染视频和LiDAR深度作为条件注入扩散模型，实现像素级对齐的精确布局控制——这是将通用文生视频能力转化为可工程化驾驶数据生成的核心技术手段。
4. **VLM驱动的自动质量筛选**：引入Qwen2.5-VL-7B-Instruct进行拒绝采样，自动丢弃约3%的存在物体消失、形状畸变等伪影的低质量样本（Section 3.2-3.3），这是将生成式AI纳入工业级数据管线的重要闭环机制。

### 适用边界与局限

**计算资源需求**：整个生成管线依赖大规模扩散模型（7B参数级别），单次推理成本高，大规模生成数据集时耗时且资源密集。这限制了其在资源受限场景下的实时或近实时数据增强应用。

**自动标注模型的鲁棒性未充分验证**：Cosmos-7B-Annotate-Sample-AV虽能从未标注的野生视频中预测HDMap和深度（Figure 8），但其在不同地理区域、天气条件、传感器配置下的精度和鲁棒性尚未全面评估。若标注质量下降，将直接影响后续生成视频的布局准确性。

**VLM过滤器的失效模式未知**：虽然3%的拒绝率在保证视觉质量的同时未显著减少有效数据量，但VLM评分器本身可能存在系统性偏见（如对某些天气条件或物体类别的过度敏感/不敏感），其失效模式有待系统研究。

**生成多样性的上限**：提示词重写器（基于Qwen2.5-7B-Instruct）的多样性受限于LLM的创造力和训练数据分布，能否覆盖真正的开放世界长尾场景（如罕见交通事故类型、极端天气组合）仍存疑。

**传感器模态覆盖有限**：当前管线主要支持RGB视频和LiDAR点云生成，尚未扩展到雷达、热成像等其他传感器形态。LiDAR生成虽展示了天气条件响应（雨天射线丢失增加，Figure 12），但其物理真实性与真实传感器数据之间的域差距未量化。

### 开放问题

1. **VLM质量控制的可优化性**：能否通过多模态评分（结合几何一致性、时序连贯性等多维度指标）或迭代优化（生成-评估-再生成循环）进一步提升自动质量控制的精度和召回？
2. **数据规模的收益饱和点**：在极低真实数据量（1K-2K clips）下SDG收益最大，但进一步扩大生成数据规模时，下游性能增益是否会趋于饱和？Figure 16右图显示性能随SDG数据量持续增长，但未探索上限。
3. **多智能体交互场景的生成能力**：当前生成主要围绕自车视角的场景外观变化，能否扩展到涉及多智能体复杂交互的动态场景（如博弈性换道、无保护左转）仍有待验证。
4. **推理效率的突破路径**：如何在保持生成视觉质量的同时显著降低扩散模型推理成本？模型蒸馏、步数压缩、专用推理硬件等方向值得探索。
5. **生成数据与真实数据的域适应**：当前采用简单的固定比例混合（R_s2r），更智能的域适应或课程学习策略能否进一步提升数据效率？



## 原文 PDF

![[paperPDFs/WHITEPAPER_2025/Cosmos_Drive_Dreams_Scalable_Synthetic_Driving_Data_Generation_with_World_Foundation_Models.pdf]]
