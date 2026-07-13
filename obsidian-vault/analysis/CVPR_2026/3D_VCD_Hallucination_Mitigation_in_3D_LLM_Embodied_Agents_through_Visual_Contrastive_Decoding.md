---
title: "3D-VCD: Hallucination Mitigation in 3D-LLM Embodied Agents through Visual Contrastive Decoding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/3D_VCD_Hallucination_Mitigation_in_3D_LLM_Embodied_Agents_through_Visual_Contrastive_Decoding.pdf
project_link: "https://plan-lab.github.io/3d-vcd"
code_link: null
aliases:
- 3V
- 3VHM3LEATVCD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 原始结构化3D场景图与被语义/几何扰动后的扭曲场景图之间的token logit差异：在扰动下概率不变（甚至升高）的token表明其依赖语言先验而非3D证据，应当被抑制。
primary_logic: 通过对物体中心的3D场景图施加可控的语义（类别标签替换）和几何（质心/包围盒加高斯噪声）扰动，构建“负”上下文，并对比原始与扰动表示下的logit，可以在不重新训练的前提下识别并压制仅由语言先验驱动的预测，将对比解码从2D像素推广到3D结构化表示。
claims:
- 3D-VCD通过对比原始与扰动3D场景图的logit，识别出对3D证据不敏感的幻觉token并予以抑制。
- 在3D-POPE Random split上，3D-VCD将精度从50.03%提升至62.16%，Yes-rate从99.81%骤降至75.15%，同时大幅提高准确率。
- 在HEAL Distractor Injection设置下，3D-VCD将Qwen-14B的状态幻觉率从16.45%降至5.0%，同时在多个探针上大幅降低物体幻觉。
- 适中的几何扰动（ε≈0.05）和低程度语义替换+几何噪声的组合产生最强的对比信号；扰动过弱（ε=0.01）或过强（ε=0.45）均导致效果下降，表明3D-VCD依赖粗粒度结构而非精确坐标。
---

# 3D-VCD: Hallucination Mitigation in 3D-LLM Embodied Agents through Visual Contrastive Decoding

> [!tip] 核心洞察
> 通过对物体中心的3D场景图施加可控的语义（类别标签替换）和几何（质心/包围盒加高斯噪声）扰动，构建“负”上下文，并对比原始与扰动表示下的logit，可以在不重新训练的前提下识别并压制仅由语言先验驱动的预测，将对比解码从2D像素推广到3D结构化表示。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3D-VCD: 通过视觉对比解码缓解3D-LLM具身智能体幻觉 |
| 英文题名 | 3D-VCD: Hallucination Mitigation in 3D-LLM Embodied Agents through Visual Contrastive Decoding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.08645) · [Project](https://plan-lab.github.io/3d-vcd) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3D-VCD |
| Dataset | 3D-POPE Random, 3D-POPE Popular, 3D-POPE Adversarial, HEAL Distractor Injection |

> [!tip] 效果简介
> - 3D-POPE Random 上，Precision 62.16 vs 50.03 (3D-LLM) (+12.13)；Accuracy 67.99 vs 50.07 (3D-LLM) (+17.92)；Yes-rate 75.15 vs 99.81 (3D-LLM) (-24.66)。
> - 3D-POPE Popular 上，Precision 52.35 vs 49.97 (3D-LLM) (+2.38)。
> - 3D-POPE Adversarial 上，F1 67.33 vs 66.61 (3D-LLM) (+0.72)。

## 概要

### 问题瓶颈

3D具身多模态大语言模型（MLLM）在视觉或几何证据模糊、遮挡或缺失时，会过度依赖语言先验，频繁产生三类幻觉：物体存在性误判、物体状态错误以及空间布局偏差。现有的2D对比解码方法仅操作像素空间，无法迁移到需要结构化3D推理的具身场景，因此3D幻觉缓解成为一个尚未被充分探索的关键瓶颈。

### 核心方法

**3D-VCD**（3D Visual Contrastive Decoding）是一种无需训练、仅在推理时生效的对比解码框架。其核心洞察是：**幻觉token是那些在底层3D感知状态被扰动后，预测概率不被抑制（甚至升高）的token**——这表明它们的生成依赖语言先验而非3D证据。基于此，3D-VCD构建了一个3D反事实接地机制：

1. 从3D观测中提取结构化的物体中心场景图 $\mathcal G_t = \{ o_i = (c_i, a_i) \}_{i=1}^{N_t}$，编码每个物体的语义类别、质心和包围盒；
2. 对场景图施加**语义扰动**（类别标签随机替换）和/或**几何扰动**（质心与包围盒加零均值高斯噪声），生成扭曲图 $\hat{\mathcal G}_t$；
3. 分别将原始图与扭曲图输入MLLM，得到两组next-token logits $\mathbf z_t^o$ 和 $\mathbf z_t^d$；
4. 通过对比融合公式 $\mathbf z_t^{\mathrm{vcd}} = (1+\alpha)\mathbf z_t^{(o)} - \alpha\mathbf z_t^{(d)}$ 抑制对3D证据不敏感的token，其中 $\alpha \ge 0$ 控制对比惩罚强度。

这一设计将对比解码从2D像素空间推广到了3D结构化表示，无需重新训练即可压制仅由语言先验驱动的预测。

### 主要结果

在**3D-POPE**基准的Random分割上，3D-VCD将精度从50.03%提升至62.16%（+12.13），准确率从50.07%提升至67.99%（+17.92），同时将过度肯定率（Yes-rate）从99.81%骤降至75.15%（-24.66），在Popular和Adversarial分割上也保持一致的增益。在**HEAL**基准的Distractor Injection设置下，3D-VCD将Qwen-14B的状态幻觉率从16.45%降至5.0%（约70%降幅），并在多个探针上大幅降低物体幻觉率。推理开销仅增加约0.25×端到端延迟，适合实时具身交互。

### 方法谱系与知识库定位

3D-VCD属于**推理时幻觉缓解**方法，与训练时对齐、RLHF反馈或模型编辑等范式正交。在3D具身MLLM领域，现有基线如**3D-LLM**、**3D-VisTA**和**LEO**均未包含推理时的幻觉缓解机制，而3D-VCD可即插即用地应用于这些模型。与2D视觉对比解码方法（如VCD）相比，3D-VCD的独特贡献在于将扰动空间从像素级扩展到结构化3D场景图，使得对比信号能够捕捉物体存在、状态和空间布局层面的接地证据缺失。

### 3D具身智能体的幻觉困境

具身智能体在开放世界中执行任务时，必须将自然语言指令与3D环境中的视觉与几何证据对齐。然而，当前以3D-LLM为核心的具身系统在面临视觉模糊、遮挡或感知缺失时，频繁产生**物体存在幻觉**（报告不存在的物体）与**状态幻觉**（错误描述物体状态）。这类幻觉的根源在于模型过度依赖语言先验——例如，当场景包含“床”和“衣柜”时，模型可能根据“卧室”的统计共现模式幻觉出“桌子”，即使3D观测中并无此物。

现有的3D多模态大语言模型（如3D-LLM、3D-VisTA、LEO）在标准自回归解码下缺乏对预测是否真正由3D证据支撑的检验机制。它们将结构化场景表示编码后直接生成文本，无法区分哪些token的预测概率来自真实的3D感知，哪些仅由语言模型的内部先验驱动。

### 2D对比解码的局限与3D结构化对比的缺失

在2D视觉-语言领域，**视觉对比解码（VCD）** 已被证明是一种有效的推理时幻觉缓解策略：通过对比原始图像与被噪声扰动的图像下的输出logit，识别并抑制对视觉证据不敏感的token。然而，这一范式无法直接迁移到3D具身场景，原因在于：

1. **表示空间不兼容**：2D VCD操作于像素空间，通过添加高斯噪声破坏低级视觉特征；而3D具身推理依赖的是结构化的物体中心表示（类别标签、质心坐标、包围盒等），像素级扰动无法产生有意义的“负”上下文。
2. **扰动语义不可控**：随机像素噪声可能破坏与任务无关的背景区域，而非有针对性地扰乱模型依赖语言先验的预测路径，导致对比信号噪声过大或失效。
3. **缺乏结构化反事实**：具身场景中的幻觉往往表现为对物体存在与否、空间关系的错误断言，需要一种能够在语义和几何层面施加可控扰动的机制，以构建与原始场景形成有意义对比的“扭曲世界”。

### 核心动机与研究问题

上述缺口引出了本文的核心动机：**能否将对比解码从2D像素空间推广到3D结构化表示，在不重新训练模型的前提下，通过推理时干预识别并压制仅由语言先验驱动的幻觉token？**

这一动机具体化为以下研究问题：

- 如何对3D场景图施加**可控的语义与几何扰动**，构造能够暴露语言先验依赖的“负”上下文？
- 如何设计**logit级对比融合机制**，使得在扰动下概率不变甚至升高的token（即对3D证据不敏感的token）被有效抑制？
- 该框架能否在**多个基准和模型架构**上一致地降低物体与状态幻觉，同时保持推理效率？

### 方法定位

3D-VCD作为首个面向3D具身智能体的训练无关、推理时对比解码框架，填补了从2D VCD到3D结构化对比解码的方法空白。它不修改模型参数，不引入辅助模型，仅通过双上下文logit对比融合实现幻觉抑制，可即插即用于现有3D-LLM管线。

## 核心方法与创新机理

3D-VCD 的核心创新在于将 **对比解码（Contrastive Decoding）从 2D 像素空间推广到 3D 结构化表示**，构建了一个无需训练、即插即用的推理时幻觉缓解框架。其关键 changed slot 体现在：

### 从标准自回归解码到双上下文 logit 对比融合

基线 3D-LLM 采用标准自回归解码，在视觉/几何证据模糊时过度依赖语言先验，频繁产生物体存在、状态、空间布局等幻觉。3D-VCD 将推理阶段的解码策略替换为 **基于语义和几何扰动的双上下文 logit 对比融合**（Section 3.1）：

1. **结构化场景图构建**：从 3D 观测中提取物体中心的结构化表示，定义为场景图 $\mathcal G_t = \{ o_i = (c_i, a_i) \}_{i=1}^{N_t}$，编码每个物体的语义类别 $c_i$ 和几何属性 $a_i$（质心、包围盒）。

2. **可控扰动算子**：对场景图施加两类扰动生成“负”上下文 $\hat{\mathcal G}_t$：
   - **语义扰动**：随机替换物体类别标签，破坏语义-几何对应关系；
   - **几何扰动**：对质心和包围盒施加零均值高斯噪声，扭曲空间结构。

3. **双上下文 logit 生成与对比融合**：分别将原始图与扭曲图输入 MLLM，得到两组 next-token logits $\mathbf z_t^o$ 和 $\mathbf z_t^d$，再通过加权相减进行融合：
   $$\mathbf z_t^{\mathrm{vcd}} = (1+\alpha) \mathbf z_t^{(o)} - \alpha \mathbf z_t^{(d)}$$
   其中 $\alpha \geq 0$ 控制对比惩罚强度。核心直觉是：**在 3D 证据被破坏后概率不变（甚至升高）的 token，表明其预测由语言先验而非 3D 证据驱动，应当被抑制**。

4. **自回归解码**：对融合后的 logit 施加 softmax，逐 token 生成最终回答。

### 关键设计选择与因果机制

消融实验揭示了 3D-VCD 有效性的因果机制：

- **扰动强度存在最优区间**：适中的几何扰动（$\varepsilon \approx 0.05$）在 3D-POPE Random 上取得最高 F1=75.00 和准确率 67.65%，Yes-rate 降至 78.41%；扰动过弱（$\varepsilon = 0.01$）或过强（$\varepsilon = 0.45$）均导致性能下降（Table 3）。这表明 3D-VCD 依赖**粗粒度结构破坏**而非精确坐标扰动来产生对比信号。

- **语义与几何联合扰动最优**：低程度语义替换 + 几何噪声（Low-SemSub-Geom）配合 $\alpha = 1.0$ 在 3D-POPE Random 上获得最佳 F1=74.48%、准确率 67.99%，Yes-rate 低至 75.15%（Table 4）。单一扰动类型无法同时破坏语义和几何证据，联合扰动提供最均衡的正则化。

- **推理效率可控**：利用批量双前向传递和 KV 缓存优化，3D-VCD 仅增加约 0.25× 端到端延迟（平均 2 秒增至 2.5 秒），适合实时具身交互（Section 3.1, Section 4.1）。

### 与 2D 对比解码的本质差异

现有 2D 对比解码方法（如 VCD）仅操作像素空间，通过图像噪声扰动构建负上下文，无法迁移到需要结构化 3D 推理的具身场景。3D-VCD 的关键突破在于**将扰动空间从像素级提升到物体中心的结构化场景图**，通过语义和几何的双重扰动，在保留场景整体结构的前提下精准破坏 3D 证据，从而识别并压制仅由语言先验驱动的幻觉 token。这一设计使得方法无需重新训练或修改模型架构，可公平地适用于现有各类 3D MLLM。

3D-VCD 是一个**免训练、纯推理时**的对比解码框架，旨在缓解 3D 具身智能体中的物体与状态幻觉。其核心流水线由五个紧密耦合的模块构成，形成“原始上下文—扭曲上下文—对比融合—自回归生成”的闭环。

### 输入与输出

- **输入**：用户的文本查询 $\mathbf{x}_t$ 与时刻 $t$ 的 3D 环境观测（点云或 RGB-D 数据）。
- **输出**：经过幻觉抑制的文本回复 $\mathbf{y}_t$，其中对 3D 证据不敏感的 token 被系统性压制。

### 流水线模块

**模块 1：3D 场景图构建**
从 3D 观测中提取结构化的、以物体为中心的表示，定义为场景图 $\mathcal{G}_t$：

$$\mathcal{G}_t = \{ o_i = (c_i, a_i) \}_{i=1}^{N_t}$$

其中 $N_t$ 为物体节点数量，$c_i$ 为语义类别标签，$a_i$ 为几何属性（质心坐标、包围盒尺寸）。该图显式编码了每个物体的语义身份与空间位置，为后续扰动提供结构化锚点。

**模块 2：扰动算子**
对原始场景图 $\mathcal{G}_t$ 施加可控的**语义扰动**（随机替换物体类别标签）和/或**几何扰动**（对质心与包围盒注入零均值高斯噪声），生成扭曲图 $\hat{\mathcal{G}}_t$。扰动强度由 $\varepsilon$ 控制，其设计原则是破坏语言先验可依赖的统计规律，但不完全摧毁 3D 结构——适中的扰动（$\varepsilon \approx 0.05$）能产生最强的对比信号，而过弱或过强的扰动均导致效果下降。

**模块 3：双上下文 Logit 生成**
将原始图 $\mathcal{G}_t$ 与扭曲图 $\hat{\mathcal{G}}_t$ 分别输入同一 MLLM $f_\theta$，并行生成两组 next-token logits：

$$\mathbf{z}_t^o = f_\theta(\mathbf{x}_t, \mathcal{G}_t), \quad \mathbf{z}_t^d = f_\theta(\mathbf{x}_t, \hat{\mathcal{G}}_t)$$

利用批量双前向传递与 KV 缓存优化，该步骤仅增加约 0.25× 的端到端延迟，平均推理时间从 2 秒增至 2.5 秒，可满足实时具身交互需求。

**模块 4：对比融合**
通过加权相减融合两组 logit，压制在扭曲上下文中概率不变（甚至升高）的 token——这些 token 被识别为依赖语言先验而非 3D 证据的幻觉源：

$$\mathbf{z}_t^{\mathrm{vcd}} = (1 + \alpha) \mathbf{z}_t^{(o)} - \alpha \mathbf{z}_t^{(d)}$$

其中 $\alpha \geq 0$ 控制对比惩罚强度，默认 $\alpha = 1.0$。融合后的 logit 中，真正依赖 3D 证据的 token 被保留，而仅由语言先验驱动的 token 被抑制。

**模块 5：自回归解码**
对融合后的 logit 施加 softmax，逐 token 生成最终回答：

$$\mathbf{y}_{t,k} = \mathrm{softmax}(\mathbf{z}_{t,k}^{\mathrm{vcd}})$$

默认采用贪心解码（温度 $T = 1.0$），确保输出确定性且可复现。

### 核心机制：因果调节变量

3D-VCD 的**因果调节变量**是原始与扭曲场景图之间的 token logit 差异。在扰动下概率不变甚至升高的 token，表明其预测不依赖真实的 3D 结构，而仅由语言统计规律驱动。通过对比融合，这些 token 被系统性识别并压制，从而在不重新训练模型的前提下，将对比解码范式从 2D 像素空间推广到 3D 结构化表示。

![[assets/figures/papers/paper_list_l2156_https_arxiv_org_abs_2604_08645/figures/002_Figure_2.jpg]]
*Figure 2: 3D-VCD Overview. Given 3D environment observations, 3D-VCD builds a structured 3D scene graph (G) encoding object categories, centroids, and extents, and injects controlled semantic and geometric perturbations to obtain a distorted version of the environment (Gˆ). The MLLM agent processes both contexts in parallel, given the textual query (x). 3D-VCD contrastively fuses their logits to reveal and suppress hallucination-prone tokens. This training-free procedure enforces 3D-grounded reasoning at inference time*

### 问题形式化

给定时刻 $t$ 的文本查询 $\mathbf{x}_t$ 和 3D 环境观测，MLLM 智能体 $f_\theta$ 产生逐 token 的自回归响应。幻觉的核心成因在于：当视觉/几何证据模糊、遮挡或缺失时，模型过度依赖语言先验做出预测，产生物体存在、状态、空间布局等虚假陈述。

### 结构化 3D 场景图构建

3D-VCD 首先将 3D 观测转化为以物体为中心的结构化场景图，作为推理的 grounded 上下文。场景图显式编码每个物体的语义与几何属性：

$$\mathcal{G}_t = \{ o_i = (c_i, a_i) \}_{i=1}^{N_t}$$

其中 $N_t$ 为时刻 $t$ 场景中的物体数量，$c_i$ 为物体 $i$ 的语义类别标签，$a_i$ 为几何属性集合（包含质心坐标与包围盒尺寸）。该表示将连续 3D 感知信号抽象为离散的、可操作的符号化图结构，为后续扰动提供明确的干预靶点。

### 扰动算子：构建负上下文

这是 3D-VCD 的核心创新。对原始场景图 $\mathcal{G}_t$ 施加可控扰动，生成扭曲版本 $\hat{\mathcal{G}}_t$，使其在语义和/或几何层面偏离真实 3D 证据。扰动分为两类：

- **语义扰动**：以概率随机替换物体类别标签 $c_i$ 为场景中其他物体的类别，破坏语义-视觉对应关系。
- **几何扰动**：对质心坐标和包围盒参数施加零均值高斯噪声 $\mathcal{N}(0, \varepsilon^2)$，其中 $\varepsilon$ 控制扰动强度。

核心假设：如果一个 token 的预测概率在 3D 证据被破坏后**不降反升**或保持不变，说明该 token 的激活主要来自语言先验而非 grounded 感知，应被识别为幻觉候选并予以抑制。

### 双上下文 Logit 生成

将原始场景图 $\mathcal{G}_t$ 和扭曲场景图 $\hat{\mathcal{G}}_t$ 分别与文本查询 $\mathbf{x}_t$ 拼接，输入同一 MLLM $f_\theta$ 进行前向传播，得到两组 next-token logits：

$$\mathbf{z}_t^{o} = f_\theta(\mathbf{x}_t, \mathcal{G}_t), \quad \mathbf{z}_t^{d} = f_\theta(\mathbf{x}_t, \hat{\mathcal{G}}_t)$$

其中 $\mathbf{z}_t^{o}$ 为原始上下文下的 logits，$\mathbf{z}_t^{d}$ 为扰动上下文下的 logits。两组 logits 的差异直接反映每个候选 token 对 3D 证据的敏感程度。

### 对比融合与自回归解码

对两组 logits 进行加权相减，得到对比增强后的 logits：

$$\mathbf{z}_t^{\mathrm{vcd}} = (1 + \alpha) \mathbf{z}_t^{(o)} - \alpha \mathbf{z}_t^{(d)}$$

其中 $\alpha \geq 0$ 为对比惩罚强度。当 $\alpha = 0$ 时退化为标准解码；$\alpha$ 越大，对在扰动下概率不降的 token 惩罚越重。默认设置 $\alpha = 1.0$。

最后对融合 logits 施加 softmax，逐 token 生成最终回答：

$$\mathbf{y}_{t,k} = \mathrm{softmax}(\mathbf{z}_{t,k}^{\mathrm{vcd}})$$

### 幻觉量化指标

在 HEAL 基准上，采用 CHAIR 指标量化幻觉程度：

$$C_t = \frac{|\{\text{hallucinated } t\}|}{|\{\text{all } t \text{ mentioned}\}|}, \quad t \in \{\text{states}, \text{objects}\}$$

其中 $C_S$ 衡量生成文本中幻觉状态占所有提及状态的比例，$C_O$ 衡量幻觉物体占所有提及物体的比例。该指标直接反映模型将不存在于场景中的物体/状态错误纳入输出的频率。

### 效率优化

3D-VCD 仅需一次额外的 MLLM 前向传播。通过批量双前向传递和 KV 缓存复用优化，端到端延迟仅增加约 $0.25\times$，平均推理时间从 2 秒增至 2.5 秒，适合实时具身交互场景。方法无需训练或微调，可即插即用于任意现有 3D MLLM。

## 实验与关键发现

### 评估基准与设置

3D-VCD在两个互补的幻觉评估基准上进行验证：**3D-POPE**（物体存在性探测）和**HEAL**（具身任务中的物体与状态幻觉）。3D-POPE包含Random、Popular、Adversarial三个子集，分别测试随机负样本、基于物体共现频率的流行负样本和对抗性负样本下的过肯定倾向，指标包括Accuracy、Precision、Recall、F1-score和Yes-rate。HEAL通过CHAIR指标衡量生成文本中幻觉物体（C_O）和幻觉状态（C_S）的占比，并在Distractor Injection等探针设置下评估模型对干扰项的鲁棒性。

实验设置方面，对比强度默认$\alpha=1.0$，采用贪婪自回归解码（温度$T=1.0$）。通过批量双前向传递和KV缓存优化，3D-VCD仅增加约0.25×的端到端延迟，平均推理时间从2秒增至2.5秒，适合实时具身交互场景。

### 主实验结果

#### 3D-POPE物体存在性探测

3D-VCD在所有三个子集上一致提升精度和准确率，同时大幅抑制过肯定倾向（Table 1）。在最具挑战性的**Random**子集上，3D-VCD将Precision从3D-LLM基线的50.03%提升至62.16%（+12.13%），Accuracy从50.07%提升至67.99%（+17.92%），F1从66.61提升至74.48；同时Yes-rate从99.81%骤降至75.15%（-24.66%），表明模型从几乎无条件肯定转变为更审慎的判断模式。在**Popular**子集上，Precision从49.97%提升至52.35%，Yes-rate从99.88%降至82.08%。在**Adversarial**子集上，F1从66.61提升至67.33，Yes-rate从99.78%降至88.88%。值得注意的是，3D-VCD在显著降低过肯定的同时，Recall仅轻微下降（Random子集从99.81降至92.59），说明方法主要压制了由语言先验驱动的虚假肯定，而非削弱对真实物体的识别能力。

![[assets/figures/papers/paper_list_l2156_https_arxiv_org_abs_2604_08645/figures/003_Table_1.jpg]]
*Table 1: Results on the 3D-POPE benchmark. Across all three evaluation categories (Random, Popular, and Adversarial) 3D-VCD achieves the highest precision, accuracy, and F1-score, surpassing prior 3D language models (3D-LLM, 3D-VisTA, and LEO). The substantial reduction in Yes-rate (e.g., 99.81% → 75.15% in the Random set) alongside consistent gains in precision and accuracy demonstrates that VCD effectively mitigates over-affirmation bias and hallucination, yielding more balanced and reliable predictions in 3D reasoning*

定性对比（Figure 4、Figure 7、Figure 8）进一步揭示了机制：基线3D-LLM在场景中不存在餐桌、床或书桌时错误地肯定其存在，而3D-VCD通过对比原始与扰动场景图的logit，成功识别并压制了缺乏3D证据支撑的token激活，从而正确输出否定回答。

![[assets/figures/papers/paper_list_l2156_https_arxiv_org_abs_2604_08645/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison on 3D-POPE. The baseline incorrectly predicts the absence of a dining table, missing the true table object. In contrast, 3D-VCD correctly grounds and identifies the dining table by aligning contrastive decoding with the scene graph*

![[assets/figures/papers/paper_list_l2156_https_arxiv_org_abs_2604_08645/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative comparison on 3D-POPE. The baseline 3D-LLM hallucinates the presence of a bed. In contrast, 3D-VCD correctly answers No by contrasting logits under perturbed 3D scene graphs, effectively suppressing hallucinated object activations. The right panel shows the object-level scene segmentation for reference*

![[assets/figures/papers/paper_list_l2156_https_arxiv_org_abs_2604_08645/figures/014_Figure_8.jpg]]
*Figure 8: Qualitative comparison on 3D-POPE. The baseline 3D-LLM hallucinates a desk object and incorrectly predicts its presence. In contrast, 3D-VCD correctly determines that no desk exists by suppressing spurious category matches through contrastive decoding aligned with the object-centric scene graph*

#### HEAL具身幻觉评估

在HEAL的Distractor Injection探针下，3D-VCD将Qwen-14B-Instruct的状态幻觉率（C_S）从16.45%降至5.0%（降幅约70%），物体幻觉率（C_O）从4.13%降至3.55%（Table 2）。在更细粒度的探针分析中（Table 5），Scene-Task Contradiction设置下物体幻觉率从53.9%降至1.5%，Distractor Object探针下状态幻觉率从16.5%降至5.0%。定性示例（Figure 5）显示，基线Qwen-14B在“刷去衣物上的棉絮”任务中幻觉出不存在的微波炉，而3D-VCD生成的符号化目标完全基于场景图中的真实物体（床上的毛衣），未引入任何幻觉实体。

### 消融实验

#### 几何扰动强度的影响

Table 3展示了仅使用几何扰动（质心与包围盒加零均值高斯噪声）时不同扰动强度$\varepsilon$的效果。在3D-POPE Random子集上，适中的扰动强度$\varepsilon=0.05$取得最优结果：F1=75.00、Accuracy=67.65、Yes-rate降至78.41%。扰动过弱（$\varepsilon=0.01$）时，扭曲图与原始图差异过小，对比信号不足，Yes-rate仍高达96.54%；扰动过强（$\varepsilon=0.45$）时，3D结构被过度破坏，对比信号失效，F1降至73.58。这表明3D-VCD依赖粗粒度结构信息而非精确坐标——适度的几何噪声足以暴露语言先验驱动的token，而不会完全破坏场景的语义完整性。

#### 语义与几何扰动组合

Table 4系统比较了不同扰动类型组合及对比强度$\alpha$的效果。在3D-POPE Random子集上，**低程度语义替换+几何噪声**（Low-SemSub-Geom）配合$\alpha=1.0$取得最佳综合表现：F1=74.48%、Accuracy=67.99%、Yes-rate=75.15%。相比之下，纯语义替换（SemSub）虽能降低Yes-rate，但对F1的提升有限；纯几何扰动（Geom）在$\alpha=1.0$时F1=75.00但Yes-rate略高（78.41%）。联合扰动提供了最均衡的正则化——语义扰动破坏了类别标签的先验关联，几何扰动破坏了空间定位的证据，两者协同迫使模型更严格地依赖3D证据。此外，对比强度$\alpha$的选择存在最优区间：$\alpha=1.0$在多数设置下优于$\alpha=0.5$或$\alpha=1.5$，过高的惩罚可能导致对真实物体的误抑制。

#### 扰动类型的整体排序

Figure 3以F1为指标对各类扰动组合进行整体排序，确认了语义+几何联合扰动优于单一扰动类型，且适中的扰动程度优于极端扰动。这一排序与上述定量消融结论一致。

### 推理效率

3D-VCD无需额外训练或辅助模型，仅需一次额外的MLLM前向传播。通过批量处理原始与扭曲场景图的输入并复用KV缓存，额外开销控制在约0.25×。Figure 6显示推理时间随场景物体数量呈近似线性增长，在典型具身场景（10-30个物体）下延迟增量在可接受范围内。

### 失败模式与局限性

尽管3D-VCD在物体和状态幻觉抑制上表现显著，但存在以下已知局限：

1. **非幻觉错误的残留**：3D-VCD仅针对由语言先验驱动的幻觉token进行压制，无法纠正规划错误、动作执行失败或逻辑推理缺陷等其他具身推理中的错误来源。
2. **极端扰动的失效**：当扰动强度过大（如$\varepsilon=0.45$）或语义替换比例过高时，扭曲图可能破坏必要的3D结构信息，导致对比信号失效甚至性能退化。
3. **动态场景未验证**：当前评估仅限于静态3D场景的快照式问答，尚未在动态3D场景、长时间交互任务或需要物理仿真反馈的环境中得到验证。
4. **开放式生成的评估挑战**：在具身对话或指令执行等开放式生成任务中，如何将对比解码从二元问答推广到更复杂的输出评估仍是一个开放问题。

### 实验公平性说明

3D-VCD作为一种推理时方法，无需训练或微调，不引入额外的训练数据偏差，可直接应用于现有3D MLLM（如3D-LLM、Qwen-14B-Instruct）而无需修改模型架构。所有对比实验均在相同基线和评估协议下进行，确保了比较的公平性。

![[assets/figures/papers/paper_list_l2156_https_arxiv_org_abs_2604_08645/figures/010_Table_4.jpg]]
*Table 4: Ablation on Semantic and Geometric Distortions under varying contrastive strengths α on 3D-POPE*

## 定位与知识库关联

### 对比解码从2D到3D的迁移

3D-VCD的核心贡献在于将对比解码（Contrastive Decoding）范式从2D像素空间推广到3D结构化表示。现有的2D对比解码方法（如VCD、ICD等）通过在原始图像与被噪声/遮挡/扭曲后的图像之间对比logit来抑制视觉幻觉，但其操作对象是像素或图像特征，无法直接应用于需要结构化3D推理的具身场景。3D-VCD识别出关键瓶颈：**3D具身MLLM在视觉/几何证据模糊、遮挡或缺失时过度依赖语言先验**，频繁产生物体存在、状态、空间布局等幻觉。通过将扰动空间从像素域迁移到物体中心的3D场景图空间——对类别标签（语义）和质心/包围盒（几何）施加可控扰动——3D-VCD构建了“负”上下文，并对比原始与扰动表示下的token logit，从而在不重新训练的前提下识别并压制仅由语言先验驱动的预测。

### 与基线方法的关系

论文将3D-VCD与三类方法对比：

- **3D-LLM**（基线3D多模态大语言模型）：未包含任何推理时幻觉缓解机制，在3D-POPE Random split上精度仅50.03%，Yes-rate高达99.81%，表现出严重的过度肯定偏置。3D-VCD在其基础上以零训练的方式将精度提升至62.16%，Yes-rate骤降至75.15%。
- **3D-VisTA**（基线3D视觉-语言对齐模型）：在3D-POPE Popular和Adversarial split上表现优于3D-LLM，但在Random split上精度仅50.02%，仍存在明显幻觉。3D-VCD在所有split上均超越3D-VisTA。
- **LEO**（基线3D具身模型，具备显式物体定位）：在Adversarial split上F1达到66.61%，3D-VCD以67.33%略胜，表明即使具备定位能力的模型仍可从对比解码中获益。

值得注意的是，3D-VCD并非替代这些基线模型，而是作为推理时即插即用的幻觉缓解层叠加于其上。其训练无关（training-free）的特性意味着不引入额外的训练数据偏差，不需要修改模型架构，公平地提升各类3D MLLM的可靠性。

### 适用边界

3D-VCD的适用前提是：能够从3D观测中构建结构化的物体中心场景图 $\mathcal{G}_t = \{ o_i = (c_i, a_i) \}_{i=1}^{N_t}$。当前实现依赖显式的物体类别标签 $c_i$ 和几何属性 $a_i$（质心、包围盒），因此适用于已部署物体检测/分割管线的3D具身感知系统。在以下条件下方法有效：

- 场景图中的物体节点 $N_t$ 数量适中（消融实验显示推理时间随物体数量线性增长，见Figure 6）。
- 扰动强度在合理范围内：几何扰动 $\varepsilon \approx 0.05$ 和低程度语义替换+几何噪声的组合提供最强对比信号；$\varepsilon$ 过小（0.01）则对比信号不足，过大（0.45）则破坏必要的3D结构导致效果下降（Table 3, Table 4）。这表明3D-VCD依赖粗粒度结构而非精确坐标。
- 对比强度 $\alpha = 1.0$ 在多数设置下为最优，配合贪婪自回归解码（temperature $T = 1.0$）。

### 局限与失败模式

1. **幻觉类型覆盖有限**：3D-VCD仅缓解物体存在/状态幻觉，不能完全消除具身推理中的其他错误来源，如规划错误、动作执行失败等。在HEAL Distractor Injection设置下，Qwen-14B的状态幻觉率从16.45%降至5.0%，但仍有5%的残余幻觉（Table 2）。
2. **极端扰动下的失效**：在严重分布偏移或极端噪声场景下，过强的扰动可能破坏必要的3D结构，导致对比信号失效。Table 3显示 $\varepsilon = 0.45$ 时F1从75.00降至约73.00，准确率同步下降。
3. **动态场景未验证**：当前实验仅在静态3D场景（3D-POPE、HEAL基准）上进行，尚未在动态3D场景、长时间交互任务或需要物理仿真反馈的环境中得到验证。
4. **推理开销**：3D-VCD需要额外的一次前向传播（批量双前向传递+KV缓存优化后约增加0.25×延迟），平均推理时间从2秒增至2.5秒。虽适合实时具身交互，但对极低延迟场景仍需进一步优化。

### 开放问题

1. **时序扩展**：能否将3D对比解码范式扩展到动态3D场景的时序推理和长期规划？当前场景图 $\mathcal{G}_t$ 仅编码单时刻的静态结构，未建模物体运动、状态变化或交互历史。
2. **表示泛化**：3D-VCD当前依赖显式场景图。是否适用于其他3D表示，如点云、3D特征tokens、多视图隐式表示？若将扰动操作直接施加于隐式表示空间，对比信号的语义可解释性将下降，需要新的校准策略。
3. **自适应扰动选择**：如何自适应地选择最优的扰动类型与强度，以在不同基准和场景分布下达到最佳幻觉抑制？当前 $\varepsilon$ 和 $\alpha$ 需手动调参，Table 4显示不同扰动组合对 $\alpha$ 的敏感度各异。
4. **开放式生成评估**：在开放式生成任务（如具身对话或指令执行）中，如何将VCD从二元问答推广到更复杂的输出评估？当前CHAIR指标（$C_t = \frac{|\{\text{hallucinated } t\}|}{|\{\text{all } t \text{ mentioned}\}|}$）依赖标注，难以在线部署。

## 原文 PDF

![[paperPDFs/CVPR_2026/3D_VCD_Hallucination_Mitigation_in_3D_LLM_Embodied_Agents_through_Visual_Contrastive_Decoding.pdf]]
