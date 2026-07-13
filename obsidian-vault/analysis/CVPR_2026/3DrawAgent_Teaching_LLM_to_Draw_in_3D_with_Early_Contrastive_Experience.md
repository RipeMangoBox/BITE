---
title: "3DrawAgent: Teaching LLM to Draw in 3D with Early Contrastive Experience"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/3DrawAgent_Teaching_LLM_to_Draw_in_3D_with_Early_Contrastive_Experience.pdf
project_link: null
code_link: null
aliases:
- 3TLD3ECE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 对比经验优化机制（contrastive experience optimization）：通过生成多个草图并基于CLIP感知评分和LLM定性评估构建成对优劣比较，将相对优势信号转化为黑盒强化提示调优，使LLM在不更新参数的情况下逐步获取3D空间推理能力。
primary_logic: 将训练自由的GRPO范式泛化为成对对比经验设置，摆脱对真实标注的依赖，通过混合CLIP感知对齐和LLM定性推理，实现从自产反馈中蒸馏3D几何先验，使冻结的大语言模型在自反思中持续提升3D草图的空间连贯性、对称性及拓扑质量。
claims:
- 对比知识提取（CKE）将CLIP-S评分从基线的0.5735提升至0.6643，增幅显著且无需任何微调。
- 在用户研究中，3DrawAgent获得了46.66%的偏好率，明显优于Dream3DVG（36.67%）和Diff3DS（16.67%）。
- 对比组大小K=5在信息丰富度与计算效率之间达到最佳平衡，CLIP-S峰值为0.6643。
- 即使不使用真实标注（GT=False），CKE也能达到与提供标注几乎相同的峰值性能（0.6643 vs 0.6648），证明了方法的无监督有效性。
---

# 3DrawAgent: Teaching LLM to Draw in 3D with Early Contrastive Experience

> [!tip] 核心洞察
> 将训练自由的GRPO范式泛化为成对对比经验设置，摆脱对真实标注的依赖，通过混合CLIP感知对齐和LLM定性推理，实现从自产反馈中蒸馏3D几何先验，使冻结的大语言模型在自反思中持续提升3D草图的空间连贯性、对称性及拓扑质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3DrawAgent: 通过早期对比经验教大语言模型绘制3D草图 |
| 英文题名 | 3DrawAgent: Teaching LLM to Draw in 3D with Early Contrastive Experience |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.08042) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3DrawAgent |
| Dataset | ModelNet40 + QuickDraw + Diff3DS混合基准 |

> [!tip] 效果简介
> - ModelNet40 + QuickDraw + Diff3DS混合基准 上，CLIP-S (语义对齐) 0.6643 (CKE后) vs 0.5735 (Base, w/o CKE) (+0.0908)。
> - 用户研究 (40个类别覆盖刚性与有机物体) 上，用户偏好率 46.66% vs Diff3DS: 16.67%, Dream3DVG: 36.67% (+10.0% over Dream3DVG)。
> - 单物体生成成本 上，时间与货币成本 ~2 min/样本, $0.09/样本 (DeepSeek API) vs Diff3DS: ~120 min, $1.50; Dream3DVG: ~60 min, $1.30 (速度提升60倍以上，成本降低12倍以上)。

## 概要

**问题瓶颈**：现有语言驱动的草图生成方法将绘制操作限制在二维平面坐标 $(x, y)$ 上，缺乏深度建模能力，导致生成的草图无法维持投影一致性和空间连贯性。同时，以训练自由的GRPO为代表的优化技术依赖组内相对评估、标量奖励或真实标注，难以适应开放式创造任务（如3D草图生成）中无绝对标注的情况，阻碍了大语言模型获取3D空间推理能力。

**核心方法**：**3DrawAgent** 提出了一种训练自由、语言驱动的3D草图生成框架。其核心创新在于**对比经验优化机制**（Contrastive Experience Optimization）：将GRPO范式泛化为成对对比经验设置，通过生成多个3D Bézier曲线草图并基于CLIP感知评分和LLM定性评估构建优劣比较对，将相对优势信号转化为黑盒强化提示调优，使冻结的大语言模型在不更新参数的情况下逐步蒸馏3D几何先验。

**方法定位**：3DrawAgent将草图表示从二维坐标平面扩展到三维Bézier曲线空间 $\mathcal{S} = \{ \mathbf{C}_1, \mathbf{C}_2, \dots, \mathbf{C}_N \}$，每个控制点显式支持深度信息 $(x, y, z)$。它不依赖预训练扩散模型作为3D先验，而是通过可迭代更新的经验库 $\mathcal{E}$ 积累可迁移的空间原则，在推理阶段将经验作为扩展提示注入LLM的上下文窗口，实现条件生成 $o = p_{\boldsymbol{\theta}}(o \mid \mathcal{T}, \mathcal{E})$。

**主要结果**：
- 对比知识提取（CKE）将CLIP-S评分从基线的 **0.5735** 提升至 **0.6643**，增幅显著且无需任何微调。
- 在用户研究中，3DrawAgent获得了 **46.66%** 的偏好率，明显优于Dream3DVG（36.67%）和Diff3DS（16.67%）。
- 单物体生成仅需约 **2分钟** 和 **$0.09**，比Diff3DS快60倍以上、成本降低12倍以上。
- 即使不使用真实标注（GT=False），CKE也能达到与提供标注几乎相同的峰值性能（0.6643 vs 0.6648），验证了方法的无监督有效性。

### 语言驱动草图的维度瓶颈

语言驱动的草图生成是视觉内容创作的重要方向，但现有方法长期受限于二维平面。以 **SketchAgent** 为代表的代理通过大语言模型在 $(x, y)$ 坐标平面上生成矢量草图，实现了灵活的语言到图形映射。然而，这种二维表示从根本上无法建模深度、投影和几何一致性——当用户描述“一把面向左前方的椅子”时，二维代理无法表达椅腿的前后遮挡关系和三维空间中的对称结构。由此产生的草图缺乏空间连贯性，难以满足三维内容创作的需求。

### 现有3D生成方法的代价与局限

为突破二维限制，近期工作尝试将语言或图像引导的生成扩展到三维空间。**Diff3DS** 利用预训练扩散模型作为三维先验，通过得分蒸馏采样（SDS）优化有理Bézier曲线；**3Doodle** 依赖多视图图像构建视图一致的3D草图；**Dream3DVG** 则采用双分支框架结合3D高斯喷溅进行引导优化。这些方法虽然能够生成具有空间结构的3D草图，但存在两个共同瓶颈：一是严重依赖预训练扩散模型或真实三维标注作为监督信号，训练和推理成本高昂（单物体生成需60-120分钟，成本在1.30-1.50美元）；二是在开放式的创造性任务中，缺乏绝对标注使得标量奖励难以定义，限制了优化范式的适用性。

### 训练自由优化的困境

近期兴起的群组奖励策略优化（GRPO）等训练自由技术，通过组内相对评估实现黑盒提示调优，为不更新模型参数的优化提供了新路径。然而，GRPO依赖组内标量奖励或真实标注来构建相对优势信号。在3D草图生成这类开放式创造任务中，不存在“标准答案”式的真实标注——对同一文本提示“一只飞翔的鸟”，不同风格的3D草图可能同样合理。这使得直接套用GRPO范式面临根本性困难：如何在没有绝对标注的条件下，为冻结的大语言模型提供有效的学习信号？

### 核心动机：从对比中蒸馏空间先验

上述瓶颈共同指向一个关键问题：**能否让大语言模型在不依赖真实标注、不更新参数的前提下，通过自我产生的反馈逐步习得3D空间推理能力？** 本文的核心动机正是构建这样一种对比经验优化机制——通过生成多个候选草图并利用CLIP感知评分和LLM定性评估构建成对优劣比较，将相对优势信号转化为可迭代积累的经验库，使冻结模型在自反思循环中持续提升3D草图的空间连贯性、对称性及拓扑质量。这一思路将训练自由的优化范式从“需要标注的标量奖励”泛化到“仅需相对比较的对比经验”设置，为语言驱动的3D创作开辟了低门槛、高效率的新路径。

## 核心方法与创新机理

3DrawAgent 的核心创新在于将大语言模型（LLM）从二维平面草图生成拓展至三维空间，并通过一种无需训练、无需真实标注的对比经验优化机制，使冻结的 LLM 在自反思中持续获取 3D 空间推理能力。以下从三个关键维度展开分析。

### 从 2D 到 3D 的草图表示空间跃迁

现有语言驱动的草图生成方法（如 SketchAgent）操作在二维坐标平面 (x, y) 上，完全不包含深度信息，因此无法建模投影、遮挡和几何连续性。3DrawAgent 引入了 **3D Bézier 曲线表示**，每条曲线由四个三维控制点 $\mathbf{P}_i^{(0)}, \mathbf{P}_i^{(1)}, \mathbf{P}_i^{(2)}, \mathbf{P}_i^{(3)}$ 参数化，显式支持深度和空间连续性。整个草图被定义为一组 3D Bézier 曲线的集合：

$$
\mathcal{S} = \{ \mathbf{C}_1, \mathbf{C}_2, \dots, \mathbf{C}_N \}
$$

其中每条曲线 $\mathbf{C}_i = \mathrm{Bezier}(\mathbf{P}_i^{(0)}, \mathbf{P}_i^{(1)}, \mathbf{P}_i^{(2)}, \mathbf{P}_i^{(3)})$。LLM 以结构化文本形式输出绘制动作序列 $a_t = \mathrm{draw.bezier}[(\mathbf{P}^{(0)}, \mathbf{P}^{(1)}, \mathbf{P}^{(2)}, \mathbf{P}^{(3)})]$，经轻量解析器转换为参数化曲线后，由深度感知的可微渲染器（基于 pydiffvg）生成多视图 2D 投影。这种表示空间的变化是后续所有 3D 空间推理能力的基础——没有深度坐标，LLM 就无法学习投影一致性和空间对称性。

### 成对对比经验优化：摆脱真实标注的强化范式

**瓶颈分析**：训练自由的 GRPO（Group Reward Policy Optimization）等优化技术依赖组内相对评估、标量奖励或真实标注，难以适应开放式创造任务（如 3D 草图生成）中无绝对标注的情况。3DrawAgent 的核心洞察是将 GRPO 范式**泛化为成对对比经验设置**，仅靠相对比较信号驱动优化，无需任何真实 3D 标注或梯度更新。

具体而言，方法构建成对对比经验 $(S_i^+, S_j^-)$，其中优劣判断由两个互补信号融合决定：

1. **CLIP 感知评分**：将多视图渲染图像与文本描述的 CLIP 平均余弦相似度作为感知对齐信号：
   
$$
r_{\mathrm{CLIP}} = \frac{1}{V} \sum_{v=1}^{V} \cos\left( \mathrm{E}_{\mathrm{I}}(I_V), \mathrm{E}_{\mathrm{T}}(T) \right)
$$

2. **LLM 语义优势判断**：LLM 作为定性比较器，对成对草图进行对比推理，输出语义优势描述：
   
$$
A^{\mathrm{text}} = \mathrm{LLM}(p_{\mathrm{judge}}, T, S_i, S_j, \mathcal{E})
$$

**决定性证据**：消融实验表明，即使不使用真实标注（GT=False），CKE 也能达到与提供标注几乎相同的峰值性能（CLIP-S: 0.6643 vs 0.6648），且学习过程更稳定。这直接证明了方法在无监督条件下的有效性。

### 可迭代更新的经验库：从自产反馈中蒸馏 3D 几何先验

3DrawAgent 的第三个关键创新是**外部经验库 $\mathcal{E}$** 的设计。与 SketchAgent 等不迭代提升的方法不同，CKE 将每次对比提取的语义优势转化为经验库的离散编辑操作：

$$
\mathcal{E} \ \mathrm{Update}(\mathcal{E}, A^{\mathrm{text}}), \quad \mathrm{Update} \in \{ \mathrm{Add, Delete, Modify, Keep} \}
$$

这些操作（添加、删除、修改、保留）将噪声奖励信号转化为简洁、可操作的 3D 空间原则。在推理阶段，累积的经验库作为扩展提示注入 LLM 的上下文窗口，实现经验引导的条件生成：

$$
o = p_{\boldsymbol{\theta}}(o \mid \mathcal{T}, \mathcal{E})
$$

**因果机制**：经验库充当了“黑盒强化提示调优”的载体——LLM 参数完全冻结，但通过不断注入提炼后的几何经验，模型在自反思中逐步获取 3D 空间推理能力。消融实验证实了这一机制的决定性作用：移除 CKE 后 CLIP-S 停留在 0.5735，而使用 CKE 在两个周期内提升至 0.6643，增幅达 +0.0908。

**对比组大小的关键作用**：消融显示 $K=5$ 在信息丰富度与计算效率之间达到最佳平衡（CLIP-S 峰值 0.6643）。$K=2$ 因多样性不足学习缓慢，$K=10$ 则无额外增益。此外，随机选择对比对（而非 CLIP 引导）会导致性能显著下降（Epoch 2 降至 0.5595，甚至低于基线的 0.5735），验证了感知引导的必要性。

### 创新带来的实际效益

这些创新直接转化为显著的性能与效率优势。在用户研究中，3DrawAgent 获得了 **46.66%** 的偏好率，明显优于 Dream3DVG（36.67%）和 Diff3DS（16.67%）。在生成成本方面，单物体生成仅需约 2 分钟和 $0.09（基于 DeepSeek API），相比 Diff3DS（~120 min, $1.50）和 Dream3DVG（~60 min, $1.30），**速度提升 60 倍以上，成本降低 12 倍以上**，且完全无需 GPU 训练。

### 尚存的局限与开放问题

尽管创新显著，方法仍存在若干结构性问题：经验库提供高层结构指导，但缺乏稠密的矢量点监督，导致语义连接处可能出现断开或漂浮元素；CLIP 评分作为整体语义相似度奖励，无法惩罚局部拓扑错误（如曲线端点匹配和几何闭环）；此外，过度推理风险在后期迭代中出现（Epoch 3 CLIP-S 从 0.6643 回退至 0.6428），提示需要机制来维持经验库的抽象性和迁移性。这些局限指向未来的改进方向：集成显式的交点促进损失、引入预训练线框重建模型作为几何先验，以及设计稠密的多视图奖励函数来惩罚漂浮基元。

**3DrawAgent** 将冻结的大语言模型（LLM）作为空间规划器，通过“生成—评估—对比—经验注入”的闭环，实现免训练的文本驱动3D草图生成。其核心管线由四个模块串联构成，数据流覆盖从文本提示到可渲染3D曲线的完整链路。

### 管线总览

整体流程如 **Figure 2** 所示，可分为两条协同路径：**单次前向生成路径** 和 **对比经验优化路径**。

![[assets/figures/papers/paper_list_l2366_https_arxiv_org_abs_2604_08042/figures/002_Figure_2.jpg]]
*Figure 2: Framework Overview. Given a text prompt, our framework uses an LLM to autoregressively generate 3D Bezier curves. Each generated sketch is evaluated with a CLIP-based model to produce quality scores, forming contrastive pairs that teach the LLM which sketches are better or worse. These insights are accumulated into an experience library, which is then leveraged to guide subsequent language-driven 3D sketch generation, enabling coherent, semantically aligned, and spatially consistent 3D drawings*

1. **语言驱动的3D草图规划器**  
   给定文本描述 $\mathcal{T}$，冻结的LLM以自回归方式一次性输出结构化的3D绘制动作序列。每个动作 `draw.bezier` 包含四个三维控制点坐标，对应于一条3D Bézier曲线。所有曲线被封装在 `<curves>` 标签内，形成完整的草图表示 $\mathcal{S} = \{ \mathbf{C}_1, \dots, \mathbf{C}_N \}$。该模块无需任何梯度更新，仅依赖少量示例提示引导LLM的空间推理。

2. **3D解析与渲染管道**  
   LLM输出的结构化文本经轻量级解析器转换为参数化Bézier曲线，随后由基于 `pydiffvg` 的可微渲染器进行深度感知投影，生成多视角2D图像 $I_V$。这些渲染视图是后续感知评分的唯一视觉信号来源。

3. **对比知识提取器（CKE）**  
   这是方法的核心创新模块。对于同一文本提示，LLM生成 $K$ 个候选草图 $\{S_1, \dots, S_K\}$。CKE通过两步构建成对对比经验：
   - **CLIP感知评分**：计算每个草图多视图渲染与文本的CLIP余弦相似度 $r_{\text{CLIP}}$，作为无监督感知信号。
   - **LLM语义优势判断**：将CLIP得分最高和最低的草图配对 $(S_i^+, S_j^-)$，交由LLM进行定性对比推理，输出语义优势描述 $A^{\text{text}}$。
   
   该优势描述随后用于更新外部经验库 $\mathcal{E}$，通过离散编辑操作（添加/删除/修改/保留）提炼可迁移的3D空间知识。整个过程仅依赖相对比较，无需真实标注或参数更新。

4. **经验引导的3D绘图**  
   推理阶段，累积的经验库 $\mathcal{E}$ 作为扩展提示注入LLM的上下文窗口，使模型在给定任意新文本提示时能够生成符合几何规范和语义一致性的最终3D草图：$o = p_{\theta}(o \mid \mathcal{T}, \mathcal{E})$。

### 关键设计决策

- **3D Bézier曲线表示**：与先前2D草图代理在 $(x, y)$ 平面操作不同，3DrawAgent显式引入深度维度 $(x, y, z)$，使每条曲线由四个三维控制点参数化，支持空间连续性和多视角一致性。
- **成对对比优化范式**：将训练自由的GRPO从组内相对评估泛化为成对对比设置，摆脱了对标量奖励和真实标注的依赖，仅靠CLIP感知对齐与LLM定性推理即可驱动经验积累。
- **可迭代经验库**：经验库 $\mathcal{E}$ 在多个CKE周期中持续更新，使冻结的LLM在自反思中逐步获取3D几何先验，无需任何微调。

![[assets/figures/papers/paper_list_l2366_https_arxiv_org_abs_2604_08042/figures/001_Figure_1.jpg]]
*Figure 1: Top: Prior works typically rely on pre-trained diffusion models as 3D priors. Bottom: Our work performs training-free 3D sketch generation by refining an LLM’s spatial reasoning*

### 3D草图表示空间

3DrawAgent 将草图形式化为 3D Bézier 曲线的集合。一条 3D 草图 $\mathcal{S}$ 由 $N$ 条曲线组成：

$$\mathcal{S} = \{ \mathbf{C}_1, \mathbf{C}_2, \dots, \mathbf{C}_N \}$$

每条曲线 $\mathbf{C}_i$ 由四个三维控制点参数化：

$$\mathbf{C}_i = \mathrm{Bezier}(\mathbf{P}_i^{(0)}, \mathbf{P}_i^{(1)}, \mathbf{P}_i^{(2)}, \mathbf{P}_i^{(3)})$$

其中 $\mathbf{P}_i^{(k)} \in \mathbb{R}^3$。这一表示空间的核心变化在于：**从二维平面坐标 $(x, y)$ 显式扩展到三维 $(x, y, z)$**，使深度和几何连续性成为可建模的原生属性。在渲染阶段，曲线通过参数化 Bézier 形式表达为连续轨迹：

$$B_i(t) = \sum_{j=0}^{3} \binom{3}{j} (1-t)^{3-j} t^{j} P_j, \quad t \in [0,1]$$

该公式用于深度感知的可微渲染管道，将 3D 曲线投影为多视图 2D 图像，供后续评分模块使用。

### 语言驱动的3D草图规划器

冻结的大语言模型（LLM）作为空间规划器，在单次前向过程中自回归生成 3D 绘制动作序列。单次绘制动作定义为：

$$a_t = \mathrm{draw.bezier}[(\mathbf{P}^{(0)}, \mathbf{P}^{(1)}, \mathbf{P}^{(2)}, \mathbf{P}^{(3)})]$$

LLM 输出是包裹在 `<curves>` 与 `</curves>` 标记内的 Python 列表，编码所有 Bézier 控制点。给定文本提示 $\mathcal{T}$ 和上下文示例 $c$，生成过程的条件概率为：

$$p_{\theta}(\mathcal{A} \mid \mathcal{T}, c)$$

### 对比知识提取器

这是方法的核心创新模块，将训练自由的 GRPO 范式泛化为**成对对比经验设置**，摆脱对真实标注的依赖。

**感知评分**：使用预训练 CLIP 模型对渲染的多视图草图进行评分：

$$r_{\mathrm{CLIP}} = \frac{1}{V} \sum_{v=1}^{V} \cos\left( \mathrm{E}_{\mathrm{I}}(I_V), \mathrm{E}_{\mathrm{T}}(T) \right)$$

其中 $V$ 为视图数量，$\mathrm{E}_{\mathrm{I}}$ 和 $\mathrm{E}_{\mathrm{T}}$ 分别为 CLIP 的图像和文本编码器，$I_V$ 为第 $v$ 个视角的渲染图像，$T$ 为文本描述。该评分衡量草图与语义描述的感知对齐程度。

**语义优势判断**：LLM 作为语义优势估计器，对成对草图 $(S_i, S_j)$ 进行对比推理，输出定性优势描述：

$$A^{\mathrm{text}} = \mathrm{LLM}(p_{\mathrm{judge}}, T, S_i, S_j, \mathcal{E})$$

其中 $p_{\mathrm{judge}}$ 为判断提示模板，$\mathcal{E}$ 为当前经验库。该模块不依赖标量奖励的绝对大小，而是通过相对比较提取结构性和语义性的改进方向。

**经验库更新**：提取的语义优势通过离散编辑操作更新经验库 $\mathcal{E}$：

$$\mathcal{E} \leftarrow \mathrm{Update}(\mathcal{E}, A^{\mathrm{text}}), \quad \mathrm{Update} \in \{ \mathrm{Add, Delete, Modify, Keep} \}$$

这四种操作分别对应添加新的空间原则、删除冗余经验、修改已有条目和保留不变，使经验库持续精炼。

### 经验引导的条件生成

在推理阶段，累积的经验库 $\mathcal{E}$ 作为扩展提示注入冻结 LLM 的上下文窗口，实现经验引导的 3D 绘图：

$$o = p_{\boldsymbol{\theta}}(o \mid \mathcal{T}, \mathcal{E})$$

其中 $\boldsymbol{\theta}$ 为冻结的 LLM 参数，$\mathcal{T}$ 为新颖文本提示。该过程无需任何梯度更新，完全通过上下文学习实现从经验中蒸馏 3D 几何先验。

## 实验与关键发现

### 核心瓶颈与方法定位

现有语言驱动的草图生成方法（如 **SketchAgent**）局限于二维平面坐标，无法建模深度与投影一致性；而扩散模型引导的3D生成管线（如 **Diff3DS**、**Dream3DVG**）依赖预训练3D先验，推理成本高昂。**3DrawAgent** 的核心创新在于将训练自由的GRPO范式泛化为成对对比经验设置：仅通过CLIP感知评分与LLM定性评估构建相对优劣对，无需真实标注或参数更新，即可从自产反馈中蒸馏3D几何先验。

### 主实验结果

**语义对齐与生成质量。** 在ModelNet40测试集上，对比知识提取（CKE）将CLIP-S评分从基线的0.5735提升至0.6643（+0.0908），增幅显著且无需任何微调（Table 2）。定性对比（Figure 3）显示，3DrawAgent在类别级和细粒度文本到3D生成中均能产生空间连贯、对称性良好的草图，而Diff3DS在复杂语义下易出现拓扑断裂。

**用户偏好研究。** 在覆盖40个类别的用户研究中，3DrawAgent获得了46.66%的偏好率，显著优于 **Dream3DVG**（36.67%）和 **Diff3DS**（16.67%）（Figure 7）。这表明对比经验优化机制提取的3D空间原则更符合人类对草图抽象性和结构完整性的期望。

**生成效率与成本。** 单物体生成仅需约2分钟和$0.09（DeepSeek API），相比之下Diff3DS需约120分钟和$1.50，Dream3DVG需约60分钟和$1.30（Table 3）。速度提升60倍以上，成本降低12倍以上，且无需GPU训练资源，使该方法在低门槛部署场景中具有显著优势。

### 消融实验分析

**经验库（CKE）的核心作用。** 移除CKE后，基础模型CLIP-S停留在0.5735，而使用CKE在2个周期内提升至0.6643（Table 2）。这验证了从成对对比中提取的语义优势经验是性能提升的唯一驱动力，而非LLM本身的先验知识。

**对比组大小的关键影响。** K=5在信息丰富度与计算效率之间达到最佳平衡（CLIP-S峰值0.6643）；K=2因多样性不足导致学习缓慢；K=10未带来额外增益（Table 2）。这表明适度的对比规模足以捕获有效的相对优势信号。

**无监督有效性验证。** 即使不使用真实标注（GT=False），CKE也能达到与提供标注几乎相同的峰值性能（0.6643 vs 0.6648），且学习过程更稳定（Table 2）。这证明了成对对比经验设置完全摆脱了对绝对标注的依赖，仅通过相对优势信号即可实现有效的黑盒提示调优。

**对比选择策略的必要性。** 随机选择对比对导致性能高度不稳定，Epoch 2降至0.5595，甚至低于基线（Table 5）。这验证了CLIP引导的成对选择对于构建有意义对比经验的关键作用。

**过度推理风险。** CKE在Epoch 3出现轻微性能回退（从0.6643降至0.6428），表明随着迭代进行，提取的经验可能变得过于局部和特定化，导致模型灵活性下降。这提示需要维护简洁抽象的经验库，避免过拟合到特定实例。

### 失败模式分析

**几何连接性不足。** 尽管经验库提供高层结构指导，但缺乏稠密的矢量点监督，导致语义连接处可能出现断开或漂浮元素（Figure 8a,b）。例如，复杂组件的曲线端点未能精确对接，形成视觉上的断裂感。

**复杂语义歧义与组件错位。** 对于非规范物体结构（如婴儿车），文本驱动代理可能产生重叠线簇而非清晰轮廓，造成视觉混乱（Figure 8c）。这源于CLIP评分仅关注整体语义相似度，无法惩罚局部拓扑错误。

**CLIP奖励函数的局限性。** 基于整体语义相似度的评分机制无法捕捉曲线端点匹配、几何闭环等细节，导致某些看似语义对齐但拓扑错误的草图获得较高分数，限制了进一步优化空间。

### 方法谱系与知识库定位

3DrawAgent在方法谱系中处于**训练自由LLM驱动3D生成**与**对比强化提示优化**的交汇点。与依赖扩散模型先验的 **Diff3DS**（基于得分蒸馏采样优化有理Bézier曲线）和 **Dream3DVG**（双分支框架结合3D高斯喷溅引导）不同，3DrawAgent将3D几何先验的获取完全外包给LLM的自反思过程。与2D草图代理 **SketchAgent** 相比，其核心突破在于将绘制空间从平面坐标扩展至3D Bézier曲线，并引入可迭代更新的经验库机制。该方法为开放域3D内容创建提供了一种无需真实标注、低计算门槛的新范式，其对比经验优化思路可迁移至其他缺乏绝对标注的开放式生成任务。

![[assets/figures/papers/paper_list_l2366_https_arxiv_org_abs_2604_08042/figures/004_Table_2.jpg]]
*Table 2: Ablation study on the core components of our CKE pipeline. We report CLIP-S on the ModelNet40 test set. The Base model (Epoch 0) has no experience. Our method achieves strong results even without ground truth and benefits from a group size of K = 5*

![[assets/figures/papers/paper_list_l2366_https_arxiv_org_abs_2604_08042/figures/003_Table_1.jpg]]
*Table 1: Comparison results on Text-to-3D (category- and fine-grained) and Image-to-3D generation. “-”: not reported*

![[assets/figures/papers/paper_list_l2366_https_arxiv_org_abs_2604_08042/figures/008_Table_3.jpg]]
*Table 3: Cost comparison with single objects*

![[assets/figures/papers/paper_list_l2366_https_arxiv_org_abs_2604_08042/figures/010_Table_5.jpg]]
*Table 5: Comparison of CKE against Random Selection. We report the*

## 定位与知识库关联

### 从2D平面到3D空间的草图表示跃迁

3DrawAgent 的核心推进在于将语言驱动草图的表示空间从二维平面坐标提升至三维 Bézier 曲线空间，从而首次赋予大语言模型显式的深度建模能力。在2D基准 **SketchAgent** 中，LLM 仅操作 $(x, y)$ 平面坐标，生成的矢量草图缺乏深度、投影和几何一致性。3DrawAgent 通过引入 3D Bézier 曲线 $\mathbf{C}_i = \mathrm{Bezier}(\mathbf{P}_i^{(0)}, \mathbf{P}_i^{(1)}, \mathbf{P}_i^{(2)}, \mathbf{P}_i^{(3)})$，使每个控制点携带 $(x, y, z)$ 三维坐标，从根本上改变了 LLM 对空间关系的表征方式。这一表示空间的跃迁并非简单的维度扩展——它要求 LLM 在无任何视觉编码器或3D先验模型辅助的情况下，仅通过文本提示学习三维几何的拓扑连贯性、对称性和深度排序。

### 与现有3D草图方法的范式差异

当前3D草图生成方法可大致分为两类：基于扩散模型优化的方法和基于多视图重建的方法，3DrawAgent 开创了第三条路径——训练自由的语言驱动生成。

**Diff3DS** 采用得分蒸馏采样（SDS）优化有理 Bézier 曲线，依赖预训练扩散模型作为3D先验，单物体生成需约120分钟和1.50美元。**Dream3DVG** 使用双分支框架配合3D高斯喷溅（3DGS）引导优化，耗时约60分钟、成本1.30美元。**3Doodle** 则利用多视图图像生成视图一致的3D草图，使用立方 Bézier 曲线。这些方法的核心瓶颈在于：需要预训练模型提供几何先验，且优化过程计算密集。

3DrawAgent 在范式层面实现了三重突破：（1）**无需任何预训练3D先验模型**，仅依靠冻结 LLM 的空间推理能力；（2）**生成效率提升60倍以上**，单物体约2分钟、成本仅0.09美元（DeepSeek API）；（3）**训练完全自由**，不涉及任何梯度更新或微调。

### 对比经验优化：GRPO范式的关键泛化

3DrawAgent 的方法论创新根植于对 Group Reward Policy Optimization（GRPO）范式的根本性改造。传统 GRPO 依赖组内相对评估、标量奖励或真实标注来驱动策略优化，这在开放式创造任务（如3D草图生成）中面临致命缺陷：不存在绝对的真实标注，且标量奖励难以捕捉几何质量的细粒度语义。

3DrawAgent 将这一范式泛化为**成对对比经验设置**（pairwise contrastive experience setting），核心机制如下：

1. **混合评分体系**：通过 CLIP 感知评分 $r_{\mathrm{CLIP}} = \frac{1}{V} \sum_{v=1}^{V} \cos\left( \mathrm{E}_{\mathrm{I}}(I_V), \mathrm{E}_{\mathrm{T}}(T) \right)$ 提供多视图语义对齐信号，同时由 LLM 自身作为语义优势判断器 $A^{\mathrm{text}} = \mathrm{LLM}(p_{\mathrm{judge}}, T, S_i, S_j, \mathcal{E})$ 进行定性比较推理。

2. **经验库蒸馏**：将相对优势信号转化为可迭代更新的经验库 $\mathcal{E}$，通过离散编辑操作 $\mathrm{Update} \in \{ \mathrm{Add, Delete, Modify, Keep} \}$ 提取可迁移的3D空间原则。

3. **无监督有效性**：即使不使用任何真实标注（GT=False），CKE 也能达到与提供标注几乎相同的峰值性能（CLIP-S 0.6643 vs 0.6648），证明了该方法对绝对标注的完全解耦。

### 知识库定位：自产反馈中的几何先验蒸馏

3DrawAgent 的经验库 $\mathcal{E}$ 本质上是一个从 LLM 自产反馈中蒸馏出的**可迁移3D几何先验知识库**。与传统的知识蒸馏不同，这里的"教师"并非更强的模型，而是 CLIP 感知对齐和 LLM 定性推理的混合信号。经验库的构建过程呈现以下特征：

- **从噪声中提取原则**：200次滚动的统计分析（Figure 4）显示，LLM 的原始输出在曲线相似度、数量分布和奖励分布上呈现高度离散，CKE 通过成对对比从中提取出稳定的空间原则。
- **从基础形状到空间意识**：知识演变分析（Figure 5）表明，经验库的学习轨迹从基础几何形状逐步过渡到3D空间意识，包括深度排序、对称性维护和组件间空间关系。
- **抽象性与迁移性**：提取的经验以自然语言形式存储，可注入任意新提示的条件生成过程 $o = p_{\boldsymbol{\theta}}(o \mid \mathcal{T}, \mathcal{E})$，实现跨类别的知识迁移。

### 适用边界与核心局限

尽管3DrawAgent在效率和语义对齐上表现优异，其方法存在明确的适用边界：

**严格几何连接性不足**：经验库提供的是高层结构指导，缺乏稠密的矢量点监督。这导致语义连接处可能出现断开或漂浮元素（Figure 8a,b），例如复杂物体的组件间缺乏精确的端点匹配。CLIP 基于整体语义相似度的奖励函数无法惩罚局部拓扑错误，可能忽略曲线端点对齐和几何闭环等细节。

**复杂语义歧义下的退化**：对于非规范物体结构（如婴儿车、复杂机械），文本驱动代理可能产生重叠线簇而非清晰轮廓，造成视觉混乱（Figure 8c）。这暴露了纯语言驱动方法在缺乏视觉反馈闭环时的固有局限。

**过度推理风险**：随着 CKE 迭代进行，提取的经验可能变得过于局部和特定化，导致模型灵活性下降。实验显示 Epoch 3 性能从 0.6643 回退至 0.6428，表明需要维护经验库的简洁性和抽象性。

**对比组敏感性与随机选择失效**：消融实验（Table 5）表明，随机选择对比对会导致性能急剧下降（Epoch 2 降至 0.5595，低于基线的 0.5735），验证了 CLIP 引导的对比对构建是不可或缺的。这同时意味着方法对奖励信号的质量高度敏感。

### 开放问题与未来方向

1. **显式几何约束的集成**：如何将交点促进损失或端点匹配损失集成到优化中，以强制实现精确的几何连接？预训练的线框重建模型能否作为几何先验插入生成管道？

2. **稠密多视图奖励设计**：什么样的奖励函数可以有效惩罚漂浮基元或不完整的几何闭环？是否需要引入基于图拓扑的结构化评估？

3. **经验库维护策略**：如何在持续更新经验库的同时避免过度推理？是否需要引入经验遗忘或抽象化压缩机制？

4. **交互式扩展**：该方法能否扩展到交互式3D草图编辑或渐进式细化场景？LLM 是否能在用户反馈的引导下进行局部修改而非重新生成？

5. **与其他模态的融合**：纯语言驱动的方法在视觉细节上存在天然局限，能否将单视图或多视图图像信息作为辅助条件注入生成过程，同时保持训练自由的特性？

## 原文 PDF

![[paperPDFs/CVPR_2026/3DrawAgent_Teaching_LLM_to_Draw_in_3D_with_Early_Contrastive_Experience.pdf]]
