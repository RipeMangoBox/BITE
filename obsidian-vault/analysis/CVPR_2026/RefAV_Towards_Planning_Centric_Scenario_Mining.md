---
title: "RefAV: Towards Planning-Centric Scenario Mining"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RefAV_Towards_Planning_Centric_Scenario_Mining.pdf
project_link: null
code_link: null
aliases:
- RTBPSR
- RefAV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过将自然语言查询分解为可组合的原子动作，并利用大语言模型（LLM）合成可执行程序来过滤现成的3D轨迹，从而桥接语言理解和精确的时空定位。
primary_logic: 程序合成方法能够将复杂的指称表达解构为基本运动原语的组合，结合离线3D感知模型，显著提升零样本场景挖掘的准确性，同时保持跨数据集的泛化能力。
claims:
- 直接复用现成的视觉语言模型（VLMs）进行场景挖掘效果很差
- RefProg 显著优于所有其他零样本基线方法
- RefProg + LE3DE2E tracks 在 HOTA-Temporal 指标上比 LLMs as a Black Box 提高了13.8%（绝对提升）
- RefProg 在 nuPrompt 数据集上取得了最先进的零样本准确率，表明原子动作具有良好的泛化性
---

# RefAV: Towards Planning-Centric Scenario Mining

> [!tip] 核心洞察
> 程序合成方法能够将复杂的指称表达解构为基本运动原语的组合，结合离线3D感知模型，显著提升零样本场景挖掘的准确性，同时保持跨数据集的泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | RefAV：面向规划中心的场景挖掘 |
| 英文题名 | RefAV: Towards Planning-Centric Scenario Mining |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.20981) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Referential Tracking by Program Synthesis (RefProg) |
| Dataset | RefAV, nuPrompt |

> [!tip] 效果简介
> - RefAV (Argoverse 2 Sensor dataset) 上，HOTA-Temporal 50.1 (RefProg + LE3DE2E tracks) vs 37.2 (LLM API Black Box + LE3DE2E tracks) (+12.9)；HOTA-Track 51.1 (RefProg + LE3DE2E tracks) vs 39.2 (LLM API Black Box + LE3DE2E tracks) (+11.9)。
> - nuPrompt 上，AMOTA 0.321 (RefProg) vs 0.259 (PromptTrack) (+0.062)。

## 概述

自动驾驶系统的安全验证面临一个核心瓶颈：如何从海量非结构化驾驶日志中，高效且精确地检索出那些涉及复杂多智能体交互的安全关键场景？这本质上是一个“大海捞针”问题——自然语言描述的罕见场景（如“雨天中一辆车在自车路径上左转”）散落在数千小时的传感器数据中，现有方法难以同时兼顾语义理解的灵活性与时空定位的精确性。

本文重新审视了基于视觉语言模型（VLM）的时空场景挖掘任务，并发现了一个关键事实：**直接复用现成的 VLM 进行场景挖掘效果很差**——这些模型缺乏细粒度的组合推理能力和运动理解能力，无法可靠地判断复杂指称表达是否在驾驶日志中发生。针对这一瓶颈，我们提出了 **RefProg（Referential Tracking by Program Synthesis）**，一种将自然语言查询分解为可组合原子动作，并利用大语言模型（LLM）合成可执行程序的方法。其核心洞察在于：程序合成能够将复杂的指称表达解构为基本运动原语的组合，结合离线 3D 感知模型，显著提升零样本场景挖掘的准确性，同时保持跨数据集的泛化能力。

为系统性地评估这一任务，我们构建了 **RefAV** 数据集——包含 10,000 条多样化自然语言查询，覆盖 1,000 个来自 Argoverse 2 Sensor 数据集的驾驶日志，每条查询均描述与运动规划相关的多智能体交互场景。实验结果表明，RefProg 在所有零样本基线方法上均取得显著优势：在 RefAV 基准上，RefProg 结合 LE3DE2E 轨迹的 HOTA-Temporal 指标达到 50.1，较黑盒 LLM 方法提升 12.9 个百分点；在 nuPrompt 数据集上，RefProg 以零样本设置取得最先进准确率（AMOTA 0.321），验证了原子动作设计的强泛化性。

本文的主要贡献可概括为三点：（1）揭示了现有 VLM 在组合时空推理上的根本性不足；（2）提出了基于程序合成的模块化场景挖掘范式，以可解释、可组合的方式桥接语言理解与精确时空定位；（3）构建了大规模、多样化的场景挖掘基准 RefAV，为规划中心的安全验证提供了系统化评估平台。

## 背景与动机

自动驾驶系统的安全验证需要大规模、多样化的场景测试。然而，从海量非结构化驾驶日志中高效且精确地检索复杂的多智能体安全关键场景，本质上是一个“大海捞针”问题。现有的场景挖掘方法主要依赖基于规则的分类器或手工设计的特征，难以应对自然语言描述的灵活性和组合性。

近期视觉语言模型（VLMs）的进展为基于自然语言的场景理解提供了新的可能。然而，论文发现**直接复用现成的 VLMs 进行场景挖掘效果很差**——这些模型缺乏细粒度的组合推理和运动理解能力，无法精确地将“车辆在雨中左转穿过自车路径”这类复杂指称表达定位到具体的 3D 轨迹和时空窗口。

这一瓶颈的根源在于：自然语言描述往往涉及多智能体交互、时空关系和运动属性的复杂组合，而现有方法要么将语言理解与视觉特征匹配割裂，要么将整个推理过程压缩为单一的黑盒问答，缺乏对场景结构的显式建模。

针对上述缺口，本文的核心动机是：**能否将复杂的指称表达解构为基本运动原语的组合，并通过程序合成桥接语言理解与精确的时空定位？** 这一思路不仅能够利用大语言模型（LLM）的语义理解能力，还能借助预定义的原子动作 API 保证检索的精确性和可解释性，同时保持跨数据集的零样本泛化能力。

## 核心创新

RefAV 的核心创新在于**将自然语言场景挖掘重构为程序合成问题**，提出 **Referential Tracking by Program Synthesis (RefProg)** 方法。该方法通过一个关键的 **changed slot**——语言理解与决策机制的根本转变——实现了对复杂多智能体安全关键场景的精确检索。

传统零样本基线方法（如 ReferGPT、Image-Embedding Similarity 或黑盒 LLM API）试图通过视觉-语言特征匹配或一步问答直接完成场景判断。然而，论文发现“直接复用现成的视觉语言模型（VLMs）进行场景挖掘效果很差”（`we find that naively repurposing off-the-shelf VLMs yields poor performance`），因为这些模型缺乏对细粒度组合推理和运动理解的能力。

RefProg 的突破在于将复杂的指称表达**分解为可组合的原子动作**，并利用大语言模型（LLM）合成可执行的 Python 程序来过滤现成的 3D 轨迹。具体而言，RefProg 将语言理解与决策机制从“端到端匹配”转变为“程序化推理”：LLM 接收自然语言查询后，调用预定义的 28 个原子动作 API（涵盖对象状态、对象间关系及布尔逻辑运算符），生成一个显式的过滤程序，再交由 Program Executor 对离线 3D 感知模型（如 LE3DE2E）输出的高质量轨迹进行精确筛选。

这一设计带来了三重核心优势：

1. **组合性**：程序合成能够将复杂的时空指称（如“在自车路径上左转的车辆”）解构为基本运动原语（如 `is_making_left_turn()`、`intersects_ego_path()`）的组合，使得模型无需在端到端黑盒中隐式学习这些关系。

2. **零样本泛化**：由于原子动作的定义独立于特定数据集，RefProg 在未修改任何原子动作定义的情况下，直接在 nuPrompt 数据集上取得了最先进的零样本准确率（AMOTA 0.321 vs. PromptTrack 0.259），验证了方法的强跨数据集泛化能力（`we do not modify RefProg's atomic action definitions`）。

3. **精确的时空定位**：相比黑盒 LLM API 基线，RefProg 在 HOTA-Temporal 指标上实现了 13.8% 的绝对提升（50.1 vs. 37.2），在 HOTA-Track 上提升 11.9%（51.1 vs. 39.2），证明程序化推理对精确时空定位的关键作用。

值得注意的是，RefProg 还引入了视觉工具（如 SigLIPv2）来识别被跟踪对象的视觉属性（如颜色），部分弥补了纯轨迹推理在视觉语义理解上的不足，但这一扩展仍属于程序合成框架内的模块化增强，而非对核心机制的改变。

## 整体框架

RefAV 提出了一种面向规划中心的场景挖掘范式，其核心挑战在于从海量非结构化驾驶日志中高效且精确地检索复杂的多智能体安全关键场景——即“大海捞针”问题。直接复用现成的视觉语言模型（VLMs）效果很差，因为它们缺乏细粒度的组合推理和运动理解能力。

为解决这一瓶颈，论文提出了 **Referential Tracking by Program Synthesis (RefProg)**，一种双路架构的模块化方法，将自然语言理解与精确的时空定位解耦为两条并行的处理通路。

### 双路架构设计

RefProg 的整体流程（见 Figure 4）由三个核心模块串联构成：

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/005_Figure_4.jpg]]
*Figure 4: Method Overview. RefProg is a dual-path method that independently generates 3D perception outputs and Python-based programs for referential grounding. Given raw LiDAR and RGB inputs, RefProg runs a offline 3D perception model to generate high quality 3D tracks. In parallel, it prompts an LLM to generate code to identify the referred track. Finally, the generated code is executed to filter the output of the offline 3D perception model to produce a final set of referred objects, related objects, and other objects*

1.  **离线 3D 感知通路**：给定原始 LiDAR 和环视 RGB 输入，RefProg 首先运行一个现成的离线 3D 感知模型（如 LE3DE2E），生成高质量的 3D 轨迹。这些轨迹构成了后续程序化过滤的候选对象池。

2.  **LLM 程序合成通路**：与感知通路并行，RefProg 将自然语言查询送入大语言模型（LLM）。LLM 被赋予一个预定义的原子动作 API 清单，其任务是将复杂的指称表达分解为可组合的基本动作，并合成一段可执行的 Python 程序。该程序调用原子 API 来精确描述被指称对象的运动状态、与其他智能体的交互关系以及视觉属性。

3.  **程序执行与过滤**：生成的程序在 3D 轨迹上执行，通过对候选轨迹进行逐层过滤和逻辑组合，最终输出三类对象集合：**指称对象**（referred objects）、**相关对象**（related objects）和**其他对象**（other objects）。这一过程将语言层面的指称表达转化为确定性的时空定位结果。

### 因果机制与核心洞察

RefProg 的核心洞察在于**程序合成作为语言与时空定位之间的桥梁**。传统的 VLM 方法试图通过特征匹配或黑盒问答一步完成场景判断，这在需要精确组合推理的多智能体交互场景中表现不佳。RefProg 改变了这一决策机制：它将 LLM 的角色从“端到端答案生成器”转变为“程序合成器”，利用代码的结构化表达能力来组合基本运动原语。

具体而言，方法定义了 28 个原子函数（基于 nuPlan 的规划场景列表），涵盖对象轨迹的状态查询、与其他对象的空间关系判定以及布尔逻辑运算。LLM 通过组合这些原子动作来构建复杂的时空查询逻辑，从而实现了从“语义模糊匹配”到“精确程序化检索”的范式转变。

### 输入输出流

- **输入**：一段 20 秒的驾驶日志（含 LiDAR 点云、360° 环视图像和 HD 地图）以及一条自然语言场景描述（如“雨天，一辆车在自车路径上左转”）。
- **输出**：场景是否发生的二值判定，以及在 3D 空间和时间维度上对被指称对象的精确定位轨迹。

### 补充图表

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/001_Figure_1.jpg]]
*Figure 1: Scenario Mining Problem Setup. Given a natural language prompt such as vehicle making left turn through ego-vehicle’s path while it is raining, our problem setup requires models to determine whether the described scenario occurs within a 20-second driving log, and if so, precisely localize the referred object in 3D space and time from raw sensor data (LiDAR, 360◦ ring cameras, and HD maps). Based on the example above, a VLM should localize the start and end timestamps and 3D location of the red Mini Cooper executing a “Pittsburgh left” through the ego-vehicle’s path with a 3D track. Notably, the “Pittsburgh left” is a regional driving practice where a driver quickly makes a left turn before...*

## 核心模块与公式推导

RefProg 采用双路解耦架构（Figure 4），将感知与推理分离：一条路径运行离线3D感知模型生成高质量轨迹，另一条路径通过LLM将自然语言查询合成为可执行程序，最后通过程序执行器对轨迹进行精确过滤与分类。

### 3D轨迹感知模块

该模块从原始LiDAR和RGB输入中提取时空轨迹。每条轨迹在每个时间步的状态由运动统计向量表征：

$$\mathbf{C}_{t}^{i} = [x, y, \theta, v_{x}, v_{y}, \alpha, d]$$

其中 $x, y$ 为位置坐标，$\theta$ 为偏航角，$v_x, v_y$ 为速度分量，$\alpha$ 为偏航速率，$d$ 为距自车的欧氏距离。该向量构成了后续原子动作API的输入基础。

### 原子动作API库

RefProg的核心创新在于将复杂的指称表达解构为可组合的原子动作。论文基于nuPlan的规划场景列表定义了28个原子函数（Figure 2左），涵盖三类操作：

1. **单对象状态判断**：检测轨迹是否满足特定运动条件（如左转、加速、静止等）。
2. **对象间关系判断**：基于底层场景图，判断对象间的空间关系（如“切入自车路径”、“与另一车辆距离小于阈值”）。
3. **布尔逻辑组合**：支持 `and`、`or`、`not` 等逻辑运算符实现函数组合。

这些原子函数以Python API的形式暴露给LLM，使其能够像程序员一样调用底层感知结果。

### LLM程序合成模块

给定自然语言查询，LLM（默认使用Claude 3.7 Sonnet）接收完整的API清单和上下文示例，生成一个Python程序。该程序调用原子动作API对轨迹进行逐步筛选。对于涉及视觉属性的查询（如“红色轿车”），RefProg额外提供SigLIPv2等视觉工具，通过CLIP风格的图像-文本匹配来识别颜色、车型等属性。这种“语言分解+程序执行”的机制是RefProg区别于黑盒LLM问答或纯特征匹配方法的关键——它将模糊的语义理解转化为确定的、可验证的时空过滤逻辑。

### 程序执行与输出

生成的Python代码在预定义的沙箱环境中执行，对离线3D感知模块输出的轨迹集合进行过滤，最终将对象分为三类：**被指称对象**（referred objects）、**相关对象**（related objects）和**其他对象**（other objects）。这种三级分类粒度使得场景挖掘不仅定位核心交互主体，还能保留上下文中的关联智能体，为下游分析提供更完整的场景快照。

### 基线方法中的公式参考

在对比基线ReferGPT中，指称相似度得分定义为：

$$s = s_{\mathrm{cosine}} + 0.1 s_{\mathrm{fuzzy}}$$

其中 $s_{\mathrm{cosine}}$ 为CLIP文本嵌入的余弦相似度，$s_{\mathrm{fuzzy}}$ 为模糊匹配得分。为抑制短轨迹（尤其是长度为1的误检）的影响，进一步引入长度惩罚项：

$$s_{\mathrm{modified}} = s_{\mathrm{cosine}} - \frac{0.05}{\mathrm{len}(\mathrm{track})}$$

这些启发式公式在RefProg中被更精确的程序化逻辑所取代，但其设计思路揭示了纯相似度匹配方法的固有局限——缺乏对时序结构和组合语义的显式建模。

## 实验与分析

### 核心问题与评估设置

本文的核心实验围绕一个关键瓶颈展开：**从海量非结构化驾驶日志中高效且精确地检索复杂的多智能体安全关键场景**，即“大海捞针”问题。直接复用现成的视觉语言模型（VLMs）进行场景挖掘效果不佳（*we find that naively repurposing off-the-shelf VLMs yields poor performance*），因为现有VLMs缺乏细粒度的组合推理和运动理解能力。

评估在RefAV数据集（基于Argoverse 2 Sensor dataset的1000个驾驶日志、10,000条自然语言查询）上进行。实验采用三项核心指标：
- **HOTA-Temporal** 和 **HOTA-Track**：衡量指称跟踪的时空定位精度；
- **平衡准确率（Balanced Accuracy）**：衡量场景挖掘的信息检索性能。采用平衡准确率而非F1分数的原因在于数据集中正负提示样本极不平衡，平衡准确率能更严格地评估方法的误报率。

所有比较方法均在**零样本设置**下评估，未利用RefAV的任何训练标注进行微调，确保公平对比。

---

### 主要实验结果

**Table 2** 展示了各零样本基线方法的对比结果。核心发现是 **RefProg 显著优于所有其他零样本基线方法**（*RefProg significantly outperforms all other zero-shot baselines*）。

| 方法 | 轨迹来源 | HOTA-Temporal | HOTA-Track |
|------|----------|---------------|------------|
| Filtering by Referred Class | LE3DE2E | 36.6 | 37.9 |
| ReferGPT | LE3DE2E | 35.8 | 37.5 |
| Image-Embedding Similarity | LE3DE2E | 32.0 | 32.9 |
| LLM API as a Black Box | LE3DE2E | 37.2 | 39.2 |
| **RefProg** | **LE3DE2E** | **50.1** | **51.1** |
| RefProg | Ground Truth | 64.8 | 68.7 |

以LE3DE2E轨迹为输入时，RefProg相比黑盒LLM API方法在HOTA-Temporal上取得了**+12.9的绝对提升**（50.1 vs. 37.2），在HOTA-Track上取得了**+11.9的绝对提升**（51.1 vs. 39.2）。值得注意的是，简单的“按指称类别过滤”（Filtering by Referred Class）基线意外地强，甚至优于基于图像嵌入相似度的方法，这表明仅靠视觉-语言特征匹配难以捕捉复杂的多智能体交互语义。

当使用真值轨迹（Ground Truth）时，RefProg的HOTA-Temporal达到64.8、HOTA-Track达到68.7，揭示了**离线3D感知模型的精度是当前性能上界的主要瓶颈**。

---

### LLM选择与代码合成质量消融

**Table 3** 评估了不同LLM对程序合成质量的影响。关键发现：
- **Claude 3.7 Sonnet** 取得了最高的HOTA-Temporal（50.1），综合性能最优；
- **Claude 3.5 Sonnet** 的程序失败率最低（仅0.5%），表明其代码生成可靠性最高；
- 不同LLM之间的性能差异主要源于**程序失败率**和**语义解释准确性**的权衡，而非单一维度的优劣。

这一消融揭示了RefProg框架的核心因果机制：**LLM的程序合成能力直接决定了场景挖掘的精度**，而不仅仅是LLM的通用推理能力。

---

### 跨数据集泛化验证

**Table 4** 展示了RefProg在nuPrompt数据集上的零样本评估结果。RefProg取得了最先进的零样本准确率（AMOTA 0.321），优于PromptTrack（0.259），**且未对原子动作定义做任何修改**。这一结果强有力地验证了方法的泛化性——原子动作的抽象层次足够通用，能够跨数据集、跨场景定义进行迁移。

---

### Token效率与成本分析

**Table 5** 对比了不同LLM基线的token效率与成本。RefProg在场景挖掘性能（HOTA-Temporal 42.3）与成本（$13.89 USD）上均达到最优权衡：
- 相比ReferGPT，RefProg以更低的成本实现了更高的精度；
- 相比黑盒LLM API方法，RefProg在显著降低成本的同时大幅提升了性能。

这一优势源于RefProg的程序合成范式：**LLM仅需生成一次可执行程序，而非对每个候选轨迹进行重复推理**，从而大幅降低了token消耗。

---

### 采样率与跟踪精度消融

**Table 7** 评估了输入轨迹采样率对性能的影响。将跟踪输入降采样至2Hz导致标准HOTA下降约5%，主要原因是稀疏检测增加了时序关联的难度。这表明RefProg对轨迹的时序密度有一定依赖，但即使在低采样率下仍保持合理的性能。

---

### 失败模式与局限性分析

基于实验结果和定性分析，RefProg的主要失败模式可归纳为以下几类：

1. **原子动作覆盖不足**：预定义的28个原子函数无法完全覆盖任意复杂场景的语义。当查询涉及隐含的多步因果关系或罕见交互（如“车辆因避让突然横穿的行人而急刹”）时，LLM合成的程序可能无法精确表达语义，导致检索失败。

2. **远距离感知退化**：当前的3D感知模型在远距离（>50m）的检测和跟踪精度不足，限制了长距离场景挖掘的可靠性。Table 2中使用真值轨迹时性能大幅提升（HOTA-Temporal从50.1升至64.8）也佐证了这一点。

3. **环境条件建模缺失**：尽管RefProg利用SigLIP2处理了颜色等视觉属性，但对天气、光照等环境条件的理解仍缺乏显式的程序化建模，导致涉及“雨天”、“夜间”等环境描述的查询准确率下降。

4. **LLM语义偏差**：LLM合成的程序并非永远正确，存在语义解释偏差或逻辑错误的风险。Table 3中不同LLM的程序失败率差异（0.5%~3.2%）表明，代码合成的可靠性仍是实际部署中的关键挑战。

### 补充图表

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/006_Table_2.jpg]]
*Table 2: Experimental Results. We evaluate several zero-shot referential tracking baselines. We find that RefProg significantly outperforms all other zero-shot baselines. Notably, filtering by referred class is a particularly strong baseline, outperforming image-embedding similarity. Interestingly, directly using LLM APIs as a black box outperforms ReferGPT’s hand-crafted approach. All winning submissions to our challenge build upon RefProg*

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/008_Table_3.jpg]]
*Table 3: Impact of Different LLMs on Code Synthesis Quality. We evaluate the impact of using different LLMs for program synthesis in the RefProg pipeline. Interestingly, we find that Claude 3.5 Sonnet has the lowest program failure rate (e.g. 99.5% of Claude 3.5 Sonnet’s generated programs were valid, compared to 81.9% for Qwen 2.5B Instruct), while Claude 3.7 Sonnet achieves the highest HOTA-Temporal*

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/007_Table_4.jpg]]
*Table 4: Zero-Shot Evaluation on nuPrompt. We evaluate Ref-Prog on nuPrompt and achieve state-of-the-art accuracy, highlighting the strong generalization of our approach. Importantly, we do not modify RefProg’s atomic action definitions*

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/009_Table_5.jpg]]
*Table 5: Token Efficiency by LLM Baseline RefProg achieves the highest scenario mining performance for the lowest cost. Cost is in USD for the OpenAI Platform in November 2025. We report the total number of tokens used millions. CIS refers to code interpreter sessions*

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/004_Table_1.jpg]]
*Table 1: Comparison to Other Benchmarks. Language-based 3D scene understanding has been extensively studied in the context of referential multi-object tracking (RMOT) and multi-modal visual question answering (VQA). Different from prior work, we address the problem of spatio-temporal scenario mining. Specifically, RefAV is based on Argoverse 2, which provides 3D track-level annotations for 30 categories at 10 Hz. Although RefAV does not include as many referential expressions as prior work (e.g. OmniDrive [68] and nuGrounding [29]), our referential annotations focus on capturing diverse multi-agent interactions. Lastly, RefAV includes negative prompts, which allows us to more accurately measure scen...*

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/014_Table_7.jpg]]
*Table 7: Impact of Sampling Rate. We evaluate RefProg’s performance with subsampled inputs to measure the relative impact on referential tracking accuracy. We find that standard tracking performance drops by 5% when subsampling due to the difficulty of associating sparse detections*

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/011_Table_6.jpg]]
*Table 6: Referential Tracking Accuracy for Related and Other Objects. We present RefProg’s referential tracking accuracy for related objects and other objects. We find that HOTA (for the base tracker) is similar to HOTA-Temporal (Other) because most objects are not relevant to the referential prompt*

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/016_Figure_8.jpg]]
*Figure 8: RefAV Object Distribution. RefAV includes referred objects in all directions up to 150m away from the ego vehicle. RefAV places a special focus on the ego vehicle and objects that interact with the ego vehicle. Therefore, referred objects are disproportionately located on the road in front of the ego vehicle. Both referred object heatmaps are in the ego vehicle coordinate frame*

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/013_Figure_6.jpg]]
*Figure 6: RefAV Expression Statistics. We compute the number of referring expressions categorized by expression type, count the number of the expressions that are positive or negative, and whether they are procedurally generated or manually constructed. We also highlight the number of positive expressions that include related object annotations and explicit references to the ego vehicle. The bar chart on the right shows the number of objects refered to by each expression. Most expressions in RefAV refer to zero (e.g. a negative match) or one object. On average, each expression refers to 3.92 objects*

![[assets/figures/papers/paper_list_l2089_https_arxiv_org_abs_2505_20981/figures/010_Figure_5.jpg]]
*Figure 5: Manual Annotation Tool. We create an annotation tool to assist with labeling manually defined scenarios. Our tool allows us to quickly annotate multi-object referential tracks in AV2*

## 方法谱系与知识库定位

### 问题定位：从“大海捞针”到程序化组合推理

RefAV 所瞄准的核心瓶颈在于：如何从海量非结构化驾驶日志中，仅凭一句自然语言描述，就高效且精确地检索出符合描述的复杂多智能体安全关键场景。这本质上是一个“大海捞针”式的时空检索问题。现有视觉语言模型（VLMs）虽然具备强大的开放世界理解能力，但论文明确指出，直接复用现成的 VLMs 进行场景挖掘效果很差（*we find that naively repurposing off-the-shelf VLMs yields poor performance*），原因在于它们缺乏对细粒度组合推理和运动理解的原生支持。

这一诊断将 RefAV 的工作与两类现有路线清晰地区分开来：一类是传统的基于规则或模板的场景挖掘方法，它们依赖预定义的场景分类，泛化能力有限；另一类是直接将 VLM 作为黑盒问答系统的方法，它们无法可靠地处理涉及多智能体交互时序逻辑的指称表达。

### 方法谱系：从 VLM 黑盒到程序合成

为了建立方法谱系，论文系统性地对比了四种零样本基线，它们构成了从“简单启发式”到“黑盒 LLM”的技术光谱：

1.  **Filtering by Referred Class**：最朴素的启发式基线。它仅利用 LLM 从描述中解析出被指称的对象类别（如“车辆”），然后不加区分地保留该类别下的所有轨迹。这一方法完全不涉及交互推理，其性能构成了场景挖掘任务的“难度下限”。

2.  **Image-Embedding Similarity**：直接计算 CLIP 图像特征与提示文本嵌入的余弦相似度来过滤轨迹。这种方法的局限在于，它只能捕捉静态的外观或场景级语义相似性，无法建模时序行为和交互关系。

3.  **ReferGPT**：在 Image-Embedding Similarity 基础上增加了 VLM 字幕生成步骤，通过文本相似度筛选轨迹。它尝试引入更丰富的语义上下文，但本质上仍是一种基于全局特征匹配的方法，缺乏对时空逻辑的显式建模。

4.  **LLM API as a Black Box**：将 GPT-5 作为黑盒，直接输入地图、自车位姿和轨迹预测等结构化数据，要求其输出匹配的对象列表。这是最接近“端到端推理”的基线，但其性能受限于 LLM 对原始数值轨迹数据的理解精度和幻觉问题。

**RefProg（Referential Tracking by Program Synthesis）** 在方法谱系中占据了一个独特的位置。它并不试图让 LLM 直接“看懂”轨迹数据，而是改变了 LLM 的角色：从“决策者”变为“程序合成器”。具体而言，RefProg 利用 LLM 将复杂的自然语言查询分解为可组合的原子动作，并合成一个调用预定义 API 的 Python 程序。该程序随后被离线执行，对现成的 3D 轨迹进行精确过滤和分类（输出指称对象、相关对象和其他对象）。这一范式转变的关键在于，它将语言理解的模糊性“编译”为了确定性的、可执行的空间-时序逻辑，从而桥接了语义理解与精确的数值计算。

### 知识库定位与适用边界

RefProg 的方法论贡献在于提出了一种**零样本、程序化、模块化**的场景挖掘框架。其核心洞察——程序合成能够将复杂的指称表达解构为基本运动原语的组合——使其天然具备以下优势与边界：

**适用边界与优势：**
-   **强零样本泛化能力**：RefProg 在未修改任何原子动作定义的情况下，直接在 nuPrompt 数据集上取得了最先进的零样本准确率（AMOTA 0.321 vs. PromptTrack 0.259），证明了其原子动作库具有良好的跨数据集迁移性。
-   **高精度与低成本兼得**：相比黑盒 LLM API，RefProg 不仅将 HOTA-Temporal 指标从 37.2 提升至 50.1（绝对提升 12.9%），同时将推理成本降至 $13.89 USD，实现了性能与效率的帕累托最优。
-   **可解释与可调试**：由于决策逻辑被显式地编写在生成的 Python 程序中，RefProg 的推理过程完全透明，便于人工验证和错误溯源，这与黑盒 VLM 方法形成鲜明对比。

**局限与开放问题：**
-   **原子动作库的完备性瓶颈**：当前 28 个原子函数基于 nuPlan 的场景列表定义，依赖专家知识。对于隐含多步因果关系或罕见交互的复杂场景，预定义 API 可能无法覆盖，导致程序合成失败。这引出了一个关键开放问题：**如何自动扩展原子函数库以适应持续演变的新型场景？**
-   **环境感知的显式建模缺失**：尽管 RefProg 利用 SigLIP2 处理了颜色等视觉属性，但对“下雨”、“夜间”等天气和光照条件的理解仍缺乏显式的程序化建模。能否在保持零样本泛化能力的同时，有效引入对动态环境因素的推理，是未来工作的一个方向。
-   **感知前端的长尾效应**：当前的 3D 感知模型在远距离（>50m）的检测和跟踪精度不足，直接限制了长距离场景挖掘的可靠性。RefProg 的性能上限受制于其离线 3D Tracker 模块的输出质量。
-   **LLM 合成的非确定性风险**：LLM 合成的程序并非永远正确，存在语义解释偏差或逻辑错误的风险。实验表明，不同 LLM 的程序失败率存在差异（Claude 3.5 Sonnet 最低，为 0.5%），这提示该方法对底层 LLM 的代码生成能力有一定依赖。

### 与下游任务的连接前景

RefAV 的工作开启了场景挖掘与规划验证之间的闭环可能性。一个值得探索的开放问题是：**场景挖掘方法是否能与下游规划或接管预测任务进行端到端联合优化**？例如，可以将 RefProg 检索出的高价值安全关键场景，直接用于训练或测试规划器的鲁棒性，从而形成一个以“规划为中心”的数据飞轮。此外，如何在大规模部署中进一步降低 LLM 程序合成的 token 消耗和延迟，使实时或在线上应用成为可能，也是该方法走向工业级应用必须跨越的工程门槛。

## 原文 PDF

![[paperPDFs/CVPR_2026/RefAV_Towards_Planning_Centric_Scenario_Mining.pdf]]