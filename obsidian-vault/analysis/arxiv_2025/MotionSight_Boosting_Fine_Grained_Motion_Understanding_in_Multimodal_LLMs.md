---
title: "MotionSight: Boosting Fine-Grained Motion Understanding in Multimodal LLMs"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/MotionSight_Boosting_Fine_Grained_Motion_Understanding_in_Multimodal_LLMs.pdf
project_link: https://nju-pcalab.github.io/projects/MotionSight
code_link: null
aliases:
- MotionSight
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过零样本视觉提示(视觉聚光灯与运动模糊)显式解耦对象运动与摄像机运动，从而强化MLLM对局部运动线索和帧间动态差异的感知。
primary_logic: MLLM在大规模预训练中已获得的潜在运动理解能力可以通过无需训练的视觉提示被有效释放：对象聚焦的视觉聚光灯引导注意力至核心运动区域，而合成运动模糊则增强对摄像机运动等微妙时序变化的感知。
claims:
- 视觉聚光灯在对象运动理解上取得最高平均分，而直接应用图像背景模糊反而损害性能。
- 全局运动模糊合成显著提升了摄像机运动的理解，比基线有大幅提高。
- MotionChat经SFT+DPO在MotionVid-QA上微调后，在FAVOR-Bench达到48.3%总体准确率，与Qwen2.5VL-72B的48.1%相当。
- MotionSight在MotionBench上将Qwen2.5VL-7B的摄像机运动(CM)指标提升14.3个百分点(从34.0到48.3)。
---

# MotionSight: Boosting Fine-Grained Motion Understanding in Multimodal LLMs

> [!tip] 核心洞察
> MLLM在大规模预训练中已获得的潜在运动理解能力可以通过无需训练的视觉提示被有效释放：对象聚焦的视觉聚光灯引导注意力至核心运动区域，而合成运动模糊则增强对摄像机运动等微妙时序变化的感知。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionSight: 增强多模态大语言模型的细粒度运动理解 |
| 英文题名 | MotionSight: Boosting Fine-Grained Motion Understanding in Multimodal LLMs |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2506.01674) · [Project](https://nju-pcalab.github.io/projects/MotionSight) · [paper](https://arxiv.org/abs/1212.0402) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionSight |
| Dataset | MotionBench, FAVOR-Bench, VideoMME |

> [!tip] 效果简介
> - MotionBench 上，AVG. accuracy 52.2 (Qwen2.5VL-7B + MotionSight) vs 48.8 (Qwen2.5VL-7B) (+3.4)；CM (camera motion) 48.3 (Qwen2.5VL-7B + MotionSight) vs 34.0 (Qwen2.5VL-7B) (+14.3)；Overall accuracy (InternVL3-78B backbone) 63.0 (InternVL3-78B + MotionSight) vs 61.5 (InternVL3-78B) (+1.5)。
> - FAVOR-Bench 上，AVG. accuracy 44.1 (Qwen2.5VL-7B + MotionSight) vs 41.6 (Qwen2.5VL-7B) (+2.5 (文本声称+3.0，以表格为准))。
> - VideoMME 上，Overall accuracy 76.0% (Qwen2.5VL-7B + MotionSight) vs 73.7% (Qwen2.5VL-7B) (+2.3%)。

## 概要

### 问题瓶颈

现有多模态大语言模型（MLLMs）在视频细粒度运动理解上面临根本性瓶颈：模型缺乏有效的帧间差分机制，倾向于对时序线索进行平均化处理或直接忽略微妙的视觉差异，导致对对象运动和摄像机运动的感知能力严重受限（Figure 1b）。这一缺陷使得现有模型在需要精确判断运动类型、方向和幅度的任务上表现不佳，即使是大规模视频预训练的模型也难以弥合这一差距。

### 核心洞察

MotionSight 的核心洞察在于：MLLM 在大规模预训练中已潜在习得运动理解能力，但这些能力被“埋没”于标准推理流程中，无法被有效激活。通过精心设计的零样本视觉提示——无需任何训练或微调——可以显式释放这些潜在能力。具体而言，**对象聚焦的视觉聚光灯**引导模型注意力至核心运动区域，抑制背景干扰；**合成运动模糊**则通过时序加权平均增强模型对帧间细微变化的感知，尤其有利于摄像机运动的理解。

### 方法定位

MotionSight 是一种**零样本、免训练的视觉提示方法**，定位在 MLLM 推理前端，作为即插即用的视觉预处理模块。其方法谱系如下：

- **多模态大语言模型基础**：以 **Qwen2.5VL-7B**（Bai et al., 2025）、**Qwen2.5VL-72B**、**InternVL3-78B**（Zhu et al., 2025a）等开源 MLLM 为骨干，无需修改模型参数。
- **专用运动理解方法对比**：与 **TE Fusion**（Hong et al., CVPR 2025）等需要训练的运动理解方法形成对照，MotionSight 以零样本方式达到甚至超越其性能。
- **视频理解基线**：与 **LLaVA-NeXT-Video-34B**（Zhang et al., 2024a）等视频专用模型对比，验证视觉提示策略的通用性。

MotionSight 的方法设计围绕**运动解耦门控**展开：根据用户查询意图判断运动类型（对象运动或摄像机运动），将输入路由至相应的视觉提示模块——对象运动走视觉聚光灯分支，摄像机运动走运动模糊分支，从而实现精细化的运动感知增强（Figure 4）。

### 主要结果摘要

在 **MotionBench** 基准上，MotionSight 将 Qwen2.5VL-7B 的平均准确率从 48.8 提升至 52.2（+3.4），其中**摄像机运动（CM）指标大幅提升 14.3 个百分点**（34.0 → 48.3），充分验证了运动模糊模块的有效性（Table 2）。在 **FAVOR-Bench** 上，MotionSight 将基线从 41.6 提升至 44.1（+2.5），且经 SFT+DPO 微调后的 MotionChat 模型达到 48.3%，与 Qwen2.5VL-72B 的 48.1% 相当（Table 3, Table 4）。在通用视频理解基准 **VideoMME** 上，MotionSight 同样带来 2.3% 的提升（73.7% → 76.0%），证明视觉提示策略不损害通用能力（Table 5）。

消融实验进一步揭示：视觉聚光灯在对象运动理解上取得最高平均分，而直接应用图像背景模糊反而损害性能；全局运动模糊合成则显著提升摄像机运动理解，远超其他视觉提示方案（Table 6）。



### 视频运动理解：从静态感知到时序动态

视频与静态图像的本质差异在于其承载的**时序动态信息**——对象的位移、形变，以及摄像机的推拉摇移等运动线索共同构成了人类理解视觉世界的关键维度。近年来，多模态大语言模型（MLLMs）在图像理解领域取得了长足进步，然而当面对视频中的细粒度运动时，这些模型暴露出显著的感知盲区。

现有 MLLMs 的核心瓶颈在于**缺乏有效的帧间差分机制**。模型倾向于对连续帧的视觉特征进行平均化处理，或直接忽略微妙的时序变化线索，导致在判断“对象是否在移动”“摄像机如何运动”等基础问题上频繁出错。这一问题并非源于模型参数规模的不足——即便是 Qwen2.5VL-72B（Bai et al., 2025）这类大型开源模型，在 MotionBench 基准上的摄像机运动（CM）指标也仅为 34.0%（Table 2），远未达到实用水平。这表明，**大规模视频预训练所获得的潜在运动理解能力被“封印”在模型内部，缺乏合适的机制将其释放**。

### 现有方法的局限

当前针对视频运动理解的改进路径主要分为两类：

- **端到端微调**：在特定运动理解数据集上对 MLLM 进行全参数或参数高效微调。这类方法虽然有效，但计算成本高昂，且容易损害模型的通用能力。
- **专用时序模块**：如 **TE Fusion**（Hong et al., CVPR 2025）等工作通过设计专门的时序融合架构来增强运动感知。然而，这些方法通常需要修改模型结构，难以即插即用地部署到不同 backbone 上。

更为关键的是，上述方法普遍**将对象运动与摄像机运动混为一谈**，采用统一的处理流程。这种“一刀切”的策略忽视了两种运动类型在视觉表征上的本质差异：对象运动需要聚焦于局部区域的位移，而摄像机运动则体现为全局画面的系统性变化。直接套用图像领域的视觉提示方法（如背景模糊）甚至会产生反效果——Table 6 的实验表明，对原始帧施加背景模糊反而**损害**了对象运动理解的性能。

### 核心洞察与本文动机

MotionSight 的核心洞察在于：**MLLM 在大规模预训练中已获得的潜在运动理解能力，可以通过无需训练的视觉提示被有效释放**。这一洞察建立在两个关键认知之上：

1. **对象聚焦的视觉聚光灯**能够引导模型注意力至核心运动区域，避免背景噪声的干扰。Grad-CAM 可视化（Figure 7）证实，施加视觉聚光灯后，模型的注意力分布显著向运动主体集中。
2. **合成运动模糊**通过时序加权平均显式编码帧间差异，能够增强模型对摄像机运动等微妙全局变化的感知能力。这种人工引入的运动痕迹为模型提供了原本被忽略的时序线索。

基于上述认知，MotionSight 提出了一种**零样本、无需训练**的视觉提示框架：通过运动类型门控将查询意图解耦为对象运动与摄像机运动，分别路由至视觉聚光灯模块和运动模糊模块，从而在不修改 MLLM 参数的前提下，显著提升细粒度运动理解能力。这一设计既保留了基础模型的通用能力，又以极低的部署成本（作者声称平均推理延迟增加少于 75%）实现了可观的性能增益。



## 核心方法与创新机理

MotionSight 的核心创新在于**无需训练的零样本视觉提示策略**，通过显式解耦对象运动与摄像机运动，释放现有多模态大语言模型（MLLM）在预训练中已获得的潜在运动理解能力。其关键洞察是：MLLM 缺乏帧间差分机制，倾向于平均化或忽略微妙的视觉线索，而通过精心设计的视觉提示可以有效引导模型关注这些被忽视的动态信息。

### 方法谱系与知识库定位

当前视频理解的主流方案可分为两类：一类是专用运动理解方法，如 **TE Fusion**（Hong et al., CVPR 2025），通过时序编码器显式建模运动特征；另一类是通用视频 MLLM，如 **Qwen2.5VL-7B/72B**（Bai et al., 2025）、**InternVL3-78B**（Zhu et al., 2025a）和 **LLaVA-NeXT-Video-34B**（Zhang et al., 2024a），依赖大规模视频预训练隐式捕获时序信息。然而，这些通用模型在细粒度运动理解上表现受限——Qwen2.5VL-7B 在 MotionBench 的摄像机运动（CM）指标上仅 34.0%，远低于对象运动相关指标，暴露出帧间差分感知的不足。

MotionSight 采取了一条与上述方案正交的路径：**不修改模型参数，而是在输入端注入结构化的视觉先验**。这一思路与图像域的视觉提示（visual prompting）工作一脉相承，但 MotionSight 首次将其系统性地扩展到视频运动解耦场景，填补了“零样本视频运动增强”这一方法空白。

### 三个关键 changed slots

MotionSight 相对于原始 MLLM 推理管线，改变了以下三个核心组件：

**1. 对象运动视觉提示（Visual Spotlight）**

- **基线做法**：直接将原始 RGB 帧输入 MLLM，模型需自行在复杂场景中定位运动主体。
- **MotionSight 做法**：在检测到的目标边界框外暗化背景，形成“视觉聚光灯”效果，强制模型将注意力集中于核心运动区域（Eq. 4: $\Phi_{obj}(\mathbf{V}_s) = \mathcal{F}_{VP}(\mathbf{V}_s, B)$）。
- **因果机制**：Grad-CAM 可视化（Figure 7）证实，视觉聚光灯使模型的注意力分布从分散的全图背景显著收缩至运动对象区域，从而提升对局部运动线索的感知精度。消融实验（Table 6）表明，视觉聚光灯在对象运动理解上取得最高平均分，而直接应用图像背景模糊反而损害性能，说明“聚焦”而非“模糊”是对象运动增强的关键。

**2. 摄像机运动视觉提示（Motion Blur Synthesis）**

- **基线做法**：逐帧独立输入，模型缺乏显式的帧间变化信息。
- **MotionSight 做法**：通过加权聚合前 $N$ 帧合成人工运动模糊（Eq. 5: $\mathcal{T}_{MB}(\cdot) = \sum_{k=0}^{N-1} w_k(\gamma) \cdot \mathcal{T}_{s_t - k}$），将时序变化编码为单帧内的视觉特征。
- **因果机制**：运动模糊将摄像机平移、旋转等全局运动转化为可感知的拖影轨迹，弥补了 MLLM 缺乏显式光流或差分计算的短板。Table 6 显示，全局运动模糊在摄像机运动理解上带来大幅提升，显著优于所有其他视觉提示方法。在 MotionBench 上，该模块将 Qwen2.5VL-7B 的 CM 指标从 34.0 提升至 48.3（+14.3 个百分点），是整体性能提升的主要贡献者。

**3. 运动类型门控（Motion Decoupling Gate）**

- **基线做法**：统一处理所有查询，不区分对象运动与摄像机运动。
- **MotionSight 做法**：基于查询意图判断运动类型，将对象运动查询路由至视觉聚光灯模块，将摄像机运动查询路由至运动模糊模块（Figure 4）。
- **因果机制**：解耦避免了两种视觉提示的相互干扰——Figure 3 展示，直接应用图像级视觉提示会导致对运动类型的误判，而解耦后的针对性增强使模型能准确区分“对象在动”与“摄像机在动”。Figure 8 的汇总分析进一步证实，解耦后两类运动指标均有显著提升。

### 从零样本提示到数据飞轮

MotionSight 的创新不仅限于推理阶段的零样本增强，还构建了一个数据飞轮：利用视觉提示增强后的 MLLM 自动标注大规模视频数据，经 VQAScore 过滤和人工偏好对齐后，形成高质量数据集 **MotionVid-QA**。在该数据集上对 Qwen2.5VL-7B 进行 SFT+DPO 微调（Eq. 6），得到的 **MotionChat** 在 FAVOR-Bench 上达到 48.3% 总体准确率，与 Qwen2.5VL-72B 的 48.1% 相当，实现了 7B 模型对标 72B 模型的运动理解能力。

### 关键消融发现

消融实验揭示了几个重要的设计原则：
- **视觉提示优于文本坐标**（Table 11）：直接输入边界框坐标的方法性能不及视觉聚光灯，表明视觉通道的注意力引导比文本通道的空间信息传递更有效。
- **暗化因子的最优值为 0.9**（Table 12）：过强的背景暗化可能破坏上下文信息，过弱则不足以引导注意力。
- **时序窗口大小 7、衰减因子 0.65 为最优配置**（Table 13, 14）：窗口过小无法充分捕获运动轨迹，过大则引入无关帧噪声。

### 局限与开放问题

尽管 MotionSight 在零样本设定下表现优异，其有效性仍受以下因素制约：
- 对象运动增强依赖检测模型，在无显著对象的场景（如纯风景）中视觉聚光灯的优势减弱甚至消失。
- 运动模糊的超参数（$N$ 和 $\gamma$）可能需要在不同视频内容上重新调整。
- 视觉聚光灯的成功是否部分源于训练数据中已有的“舞台聚光灯”效应，导致分布偏移，仍需进一步验证。
- 零样本推理引入额外延迟（作者声称平均增加少于 75%），在实时场景中可能成为瓶颈。



MotionSight 的整体设计围绕一个核心观察展开：现有多模态大语言模型（MLLMs）在视频理解中缺乏显式的帧间差分机制，倾向于平均化或忽略微妙的运动线索，导致细粒度运动理解严重受限。为解决这一问题，MotionSight 提出了一套**零样本视觉提示框架**，通过无需训练的视觉变换，显式增强 MLLM 对对象运动与摄像机运动的感知能力。

### 框架总览

MotionSight 的完整 pipeline 如 Figure 4 所示，由四个核心阶段构成：**查询驱动的运动解耦**、**对象运动视觉提示**、**摄像机运动视觉提示**，以及**MLLM 推理与决策**。整个流程以用户查询为输入，以结构化的运动理解结果为输出，无需对 MLLM 本身进行任何微调。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/004_Figure_4.jpg]]
*Figure 4: The detailed pipeline of MotionSight. Our method includes query-based motion decoupling, gating based on object motion and camera motion. Subsequently, it selectively passes through modules based on the decoupled type. Then, we carefully designed a template prompt for MLLMs to understand our enhanced input and make final decisions*

**输入与输出定义**（Section 3, Eq. 1）：给定一段视频 $\mathbf{V}$ 及其均匀采样的 $T$ 帧 $\mathbf{V}_s = \{\mathcal{T}_{s_t}\}_{t=1}^T$，MotionSight 分别通过对象运动视觉提示函数 $\Phi_{obj}$ 和摄像机运动视觉提示函数 $\Phi_{cam}$ 对输入进行变换，再由 MLLM 生成对应的运动理解结果：

$$\mathcal{R}_{obj} = \mathbf{MLLM}(\Phi_{obj}(\mathbf{V}_s)), \quad \mathcal{R}_{cam} = \mathbf{MLLM}(\Phi_{cam}(\mathbf{V}_s, \mathbf{V}))$$

### 阶段一：查询驱动的运动解耦

MotionSight 首先根据用户查询的意图，通过**运动解耦门控**（Motion Decoupling Gate）判断当前任务属于对象运动理解还是摄像机运动理解，并将请求路由至相应的视觉提示模块。这一设计使得框架能够有针对性地施加不同类型的视觉增强，避免了统一处理带来的信息混淆（Figure 3）。

### 阶段二：对象运动视觉提示

当查询涉及对象运动时，MotionSight 执行以下子流程：

1. **对象检测与跟踪**（Section 3.1, Eq. 2）：从关键帧 $\mathcal{T}_{s_t}$ 中检测与查询相关的对象类别 $\mathcal{C}$，并利用跟踪模块将检测结果传播至后续帧，获得全时序对象轨迹 $\mathcal{O}$：

   $$\mathcal{O} = \mathcal{M}_{track}(\mathcal{M}_{detect}(\mathcal{T}_{s_t}, \mathcal{C}; \theta_{det}), \{\mathcal{T}_{s_j}\}_{j=t+1}^{T}; \theta_{track})$$

2. **动态时序聚合**（Section 3.2, Eq. 3）：基于轨迹内边界框位置方差 $\mathcal{V}(\mathcal{X})$，动态合并多帧检测结果，输出稳定的空间区域 $B = \{b_t\}_{t=1}^T$：

   $$B = \mathcal{A}\left(\mathcal{X}, \mathcal{V}(\mathcal{X})\right) = \{b_t\}_{t=1}^T$$

3. **视觉聚光灯**（Section 3.2, Eq. 4）：在聚合区域 $B$ 外暗化背景，保留原始对象区域，生成视觉增强帧：

   $$\Phi_{obj}(\mathbf{V}_s) = \mathcal{F}_{VP}(\mathbf{V}_s, B)$$

这一设计的关键洞察是：通过在目标边界框外暗化背景，视觉聚光灯引导 MLLM 的注意力集中于核心运动区域，从而强化对局部运动线索的感知。消融实验（Table 6）证实，视觉聚光灯在对象运动理解上取得最高平均分，而直接应用图像背景模糊反而损害性能。

### 阶段三：摄像机运动视觉提示

当查询涉及摄像机运动时，MotionSight 采用**时序运动模糊合成**策略（Section 3.3, Eq. 5），通过加权聚合前 $N$ 帧来引入人工运动模糊，增强对摄像机运动轨迹等微妙时序变化的感知：

$$\Phi_{cam}(\mathbf{V}, \mathbf{V}_s) = \left\{\mathcal{T}_{MB}(\mathbf{V}_s, N, t)\right\}_{t=1}^T, \quad \mathcal{T}_{MB}(\cdot) = \sum_{k=0}^{N-1} w_k(\gamma) \cdot \mathcal{T}_{s_t - k}$$

其中权重核函数 $w_k(\gamma)$ 由衰减因子 $\gamma$ 控制（详见 Appendix A.1）。消融实验确定的最优超参数为：时序窗口大小 $N=7$，衰减因子 $\gamma=0.65$（Table 13, 14）。全局运动模糊合成在摄像机运动理解上带来了大幅提升（Table 6），验证了这一设计的有效性。

### 阶段四：MLLM 推理与决策

经视觉提示增强后的帧与精心设计的模板提示（template prompt）一同输入 MLLM，由模型生成最终的运动理解结果。整个流程中，MLLM 的参数保持不变，MotionSight 仅作为输入端的零样本增强方案运行。

### 关键设计选择

- **解耦优于统一**：Figure 8 的对比表明，将对象运动与摄像机运动解耦处理后，MotionSight 在两类指标上均展现出显著优势。统一处理会模糊两种运动类型的特异性视觉线索。
- **视觉提示优于文本坐标**：消融实验（Table 11）显示，直接输入边界框坐标的方法性能不及视觉聚光灯，表明视觉层面的注意力引导比文本坐标信息更有效。
- **零样本特性**：MotionSight 不依赖任何训练或微调，其能力来源于对 MLLM 在大规模预训练中已获得的潜在运动理解能力的有效释放。



MotionSight 的核心架构（图4）由三个功能模块构成：**查询感知的运动解耦门控**、**对象运动视觉提示**、**摄像机运动视觉提示**。各模块以零样本方式对 MLLM 的输入帧进行预处理，无需任何训练。

### 3.1 运动解耦门控

系统首先根据用户查询的语义意图判断运动类型，将请求路由至对象运动分支或摄像机运动分支。这一解耦设计的根本动机在于：对象运动与摄像机运动对视觉线索的需求截然不同——前者需要将注意力聚焦于运动主体，后者则需要增强对全局帧间位移的感知。统一处理会迫使 MLLM 在两种需求之间折衷，导致细粒度运动理解的瓶颈。

### 3.2 对象运动视觉提示

对象运动分支由三个子模块串联构成：

**对象检测与跟踪（$\mathcal{M}_{detect}$, $\mathcal{M}_{track}$）**：从关键帧 $\mathcal{T}_{s_t}$ 中检测与查询相关的对象类别 $\mathcal{C}$，并将检测结果传播到后续帧 $\{\mathcal{T}_{s_j}\}_{j=t+1}^{T}$，得到全时序对象轨迹 $\mathcal{O}$：

$$\mathcal{O} = \mathcal{M}_{track}(\mathcal{M}_{detect}(\mathcal{T}_{s_t}, \mathcal{C}; \theta_{det}), \{\mathcal{T}_{s_j}\}_{j=t+1}^{T}; \theta_{track})$$

**动态时序聚合器（$\mathcal{A}$）**：由于检测和跟踪产生的边界框在时序上可能存在抖动，直接使用会导致视觉提示区域不稳定。聚合器根据轨迹内位置方差 $\mathcal{V}(\mathcal{X})$ 动态合并边界框，输出稳定的空间区域 $B = \{b_t\}_{t=1}^T$：

$$B = \mathcal{A}\left(\mathcal{X}, \mathcal{V}(\mathcal{X})\right) = \{b_t\}_{t=1}^T$$

**视觉聚光灯（$\mathcal{F}_{VP}$）**：在聚合区域 $B$ 之外暗化背景，保留原始对象区域不变，从而引导 MLLM 的注意力集中于运动主体：

$$\Phi_{obj}(\mathbf{V}_s) = \mathcal{F}_{VP}(\mathbf{V}_s, B)$$

消融实验（Table 6）表明，视觉聚光灯在对象运动理解上取得最高平均分，而直接对背景应用图像模糊反而损害性能——这验证了“保留原始对象纹理、仅抑制背景干扰”的设计原则。Grad-CAM 可视化（图7）进一步证实，加入视觉聚光灯后，模型的注意力显著向核心运动区域集中。

### 3.3 摄像机运动视觉提示

摄像机运动（如平移、缩放、旋转）表现为全局帧间位移，其细微程度往往超出 MLLM 逐帧独立编码的感知能力。MotionSight 通过时序加权平均合成人工运动模糊，将 $N$ 帧的运动轨迹压缩到单帧中：

$$\Phi_{cam}(\mathbf{V}, \mathbf{V}_s) = \left\{\mathcal{T}_{MB}(\mathbf{V}_s, N, t)\right\}_{t=1}^T, \quad \mathcal{T}_{MB}(\cdot) = \sum_{k=0}^{N-1} w_k(\gamma) \cdot \mathcal{T}_{s_t - k}$$

其中权重核函数 $w_{N-1-k}(\gamma) = \gamma^{k} \cdot \prod_{j=k+1}^{N-1} (1 - \gamma^{j})$，衰减因子 $\gamma$ 控制历史帧的贡献衰减速度。消融实验（Table 6）显示，全局运动模糊合成在摄像机运动理解上相较基线有大幅提升，且显著优于其他视觉提示方法。最优超参数经消融确定为：暗化因子 0.9（Table 12）、时序窗口大小 $N=7$（Table 13）、衰减因子 $\gamma=0.65$（Table 14）。

### 3.4 推理流程

最终，MLLM 接收视觉提示后的采样帧并输出运动理解结果：

$$\mathcal{R}_{obj} = \mathbf{MLLM}(\Phi_{obj}(\mathbf{V}_s)), \quad \mathcal{R}_{cam} = \mathbf{MLLM}(\Phi_{cam}(\mathbf{V}_s, \mathbf{V}))$$

整个流程为零样本推理增强，不修改 MLLM 参数。作者声称平均推理延迟增加少于 75%，相较其他工作流较轻量。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of our method with other existing methods. Directly applying image visual prompts can lead to misinterpretation. By employing decoupled objectguided motion focusing and inter-frame information enhancement, our method addresses the challenge faced by previous methods*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/010_Figure_7.jpg]]
*Figure 7: The difference between using visual spotlight and the original MLLM. We used Grad-CAM and selected the same layer for gradient computation. After incorporating the visual spotlight, the model pays more attention to the core region. Prompt: “What are the people doing?”*



## 实验与关键发现

### 核心实验设置

MotionSight 是一种零样本、无需训练的视觉提示增强方案，其评估分为两条线索：**MotionSight** 直接作为视觉提示插入 MLLM 推理流程；**MotionChat** 则是在 MotionSight 生成的 MotionVid‑QA 数据集上进行 SFT + DPO 微调后的模型。主要基准包括 **MotionBench**（细粒度运动理解）、**FAVOR‑Bench**（对象/摄像机运动细粒度评测）、**VideoMME**（通用视频理解）和 **TempCompass**（时序理解）。

### 主结果：MotionBench 与 FAVOR‑Bench

在 MotionBench 上，将 MotionSight 应用于 **Qwen2.5VL‑7B**（Bai et al., 2025）后，总体平均准确率从 48.8 提升至 52.2（+3.4 个百分点），其中摄像机运动（CM）指标从 34.0 跃升至 48.3（+14.3 个百分点）——这是所有指标中幅度最大的提升，直接验证了运动模糊模块对摄像机运动感知的强化效应。在更大规模的 **InternVL3‑78B**（Zhu et al., 2025a）骨干上，MotionSight 同样带来 +1.5 的总体增益（61.5 → 63.0），表明该方法对模型容量具有良好的可扩展性（见 Table 2）。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/008_Table_2.jpg]]
*Table 2: Quantitative results on MotionBench. We compared our MotionSight with both proprietary MLLMs and open-source MLLMs on MotionBench, all of which have been trained on large-scale video data. The best results of open-source methods are marked in bold*

在 FAVOR‑Bench 上，MotionSight 使 Qwen2.5VL‑7B 的总体准确率从 41.6 提升至 44.1（+2.5 个百分点；正文声称 +3.0，以表格实测为准）。值得注意的是，经过 MotionVid‑QA 数据集 SFT+DPO 微调的 **MotionChat**（基于 Qwen2.5VL‑7B）在 FAVOR‑Bench 达到 48.3% 总体准确率，与 72B 规模的 **Qwen2.5VL‑72B** 的 48.1% 相当（Table 4），说明高质量运动理解数据可以大幅弥补模型规模差距。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/011_Table_4.jpg]]
*Table 4: Quantitative results for MotionChat based on Qwen2.5VL-7B across different training stages. We analyzed the impact of different training strategies by selectively including or excluding SFT and preference datasets on FAVOR-Bench. Green areas indicate best performance. “✔” indicates the presence of a training stage, while “✘” indicates its absence*

### 通用视频理解与跨基准泛化

在 VideoMME 上，MotionSight 将 Qwen2.5VL‑7B 的总体准确率从 73.7% 提升至 76.0%（+2.3 个百分点，Table 5），表明运动感知增强并未损害通用视频理解能力，反而带来正向迁移。在 TempCompass 主基准和细粒度描述子维度上（Table 8–10），MotionChat 在绝对速度（AS）、摄像机运动（CM）、细粒度动作（FGA）等子项上均表现出显著优势，进一步验证了运动解耦策略的跨任务泛化性。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/012_Table_5.jpg]]
*Table 5: Evaluation on VideoMME. We present the core general-purpose tasks*

### 消融实验：视觉提示策略的核心作用

Table 6 的消融实验直接揭示了不同视觉提示策略对运动理解的影响机制：

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/014_Table_6.jpg]]
*Table 6: Experiments of several visual prompt methods specialized for motion decoupling on MotionBench. Green areas indicate best performance and red areas show lowest scores*

- **视觉聚光灯（Visual Spotlight）**：在对象运动（OM AVG.）上取得最高平均分，显著优于直接输入原始帧的基线。关键证据是，若将聚光灯替换为简单的**背景模糊**（Background Blur），性能反而下降——这说明精确保留对象区域、暗化背景的“舞台聚光灯”效应是引导 MLLM 注意力至运动主体的关键，而非单纯的背景抑制。
- **全局运动模糊（Motion Blur）**：在摄像机运动理解上取得大幅领先，优于所有其他视觉提示变体。该结果直接支持核心设计直觉：通过时序加权平均引入合成运动模糊，能够强化模型对帧间微妙差异的感知，从而弥补 MLLM 缺乏显式帧间差分机制的瓶颈。
- **坐标输入对比**：Table 11 显示，直接向 MLLM 输入边界框坐标文本的方法，性能不及视觉聚光灯，验证了“视觉提示优于文本坐标”的设计选择。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/019_Table_11.jpg]]
*Table 11: Ablation study of different input methods*

### 运动解耦的归因分析

Figure 8 汇总了对象运动、摄像机运动及其他运动类别的平均指标。解耦后，对象运动分支和摄像机运动分支在各自相关的任务上均取得显著增益；即使在“其他运动”（与对象运动相关性较低的任务）上，视觉聚光灯对核心区域的聚焦也带来正向效果。这证实了运动类型门控（Motion Decoupling Gate）的有效性——统一处理会平均化线索，而解耦后各分支可针对性地强化对应信号。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/013_Figure_8.jpg]]
*Figure 8: We compiled the metrics related to object motion, camera motion, and other motion from the benchmark and averaged the experimental model and task metrics. Other motion refers to tasks with low correlation to object motion, for which we also used the visual spotlight to focus on core regions. Our method shows significant advantages after decoupling motion*

### 超参数敏感性

消融实验确定了关键超参数的最优配置（Table 12–14）：
- **暗化因子**：0.9（背景暗化程度）
- **时序窗口大小 N**：7 帧
- **衰减因子 γ**：0.65

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/021_Table_12.jpg]]
*Table 12: Ablation study on the degree of background darkening*

这些参数在 MotionBench 上通过网格搜索得出，但论文同时指出，不同视频内容（如快速运动 vs 缓慢运镜）可能需要重新调整，这是零样本方法的固有限制。

### 失败模式与边界条件

1. **无显著对象场景**：在缺乏清晰前景对象的视频中，视觉聚光灯的优势减弱甚至消失（论文自述限制）。此时系统完全依赖摄像机运动分支，而该分支的独立支撑能力尚未被充分验证。
2. **检测模型依赖**：MotionSight 的对象轨迹提取依赖外部检测器，在特定领域（如医学影像、水下场景）可能需要微调检测模型，否则边界框质量下降会级联影响视觉聚光灯效果。
3. **推理延迟**：零样本方法引入额外的检测、跟踪和帧合成步骤，作者声称平均延迟增加少于 75%，但具体场景下的实时性仍需评估。
4. **数据集预过滤阈值未公开**：MotionVid‑QA 构建中使用的光流阈值 τ_f 和清晰度阈值 τ_c 未给出具体数值，这影响数据集复现和对过滤策略严格程度的判断。

### 证据强度总结

| 核心主张 | 证据锚点 | 置信度 |
|---------|---------|--------|
| 视觉聚光灯提升对象运动理解，背景模糊反而损害 | Table 6 | 高 |
| 运动模糊大幅提升摄像机运动理解 | Table 6, Table 2 (CM +14.3) | 高 |
| MotionChat 经 SFT+DPO 可媲美 72B 模型 | Table 4 | 高 |
| 方法对更大骨干模型有效 | Table 2 (InternVL3‑78B) | 中高 |
| 通用视频理解不降反升 | Table 5 (VideoMME) | 高 |
| FAVOR‑Bench 文本声称与表格存在差异 | 正文 vs Table 3 | 需注意 |

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/009_Table_3.jpg]]
*Table 3: Quantitative results on FAVOR-Bench. We selected representative MLLMs as baselines for comparison. We computed the OM (object motion) metric by averaging all metrics excluding the CM (camera motion) metric in FAVOR-Bench*

### 补充图表

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2506_01674/figures/022_Table_13.jpg]]
*Table 13: Ablation study on temporal window size (N in Equation 5), with fixed decay factor: 0.65*



## 定位与知识库关联

### 核心瓶颈与设计动机

现有多模态大语言模型（MLLMs）在视频理解中面临一个根本性瓶颈：**缺乏帧间差分机制**，倾向于对时序信息进行平均化处理，导致对微妙的细粒度运动线索感知能力严重受限（Figure 1(b)）。MotionSight 的核心洞察在于，MLLM 在大规模预训练中已潜在习得运动理解能力，只是缺乏合适的“触发器”将其释放。因此，该方法选择了一条**无需训练的零样本视觉提示**路径，通过显式解耦对象运动与摄像机运动，分别施加针对性视觉增强，从而激活模型的潜在运动感知能力。

### 方法谱系定位

**MotionSight** 处于“零样本视觉提示增强”与“运动解耦理解”的交叉地带。与现有方法相比，其关键差异体现在两个维度：

1.  **与直接视觉提示方法的对比**：直接应用图像级别的视觉提示（如背景模糊、边界框标注）会导致 MLLM 产生误解（Figure 3）。MotionSight 通过**运动类型门控**将对象运动与摄像机运动解耦，分别路由至不同的增强模块，避免了统一处理造成的语义混淆。

2.  **与专用运动理解方法的对比**：**TE Fusion**（Hong et al., CVPR 2025）等专用方法通常需要模型架构修改或额外训练。MotionSight 作为零样本方案，无需任何训练即可在 MotionBench 上将 **Qwen2.5VL-7B**（Bai et al., 2025）的平均准确率从 48.8 提升至 52.2（+3.4 个百分点），摄像机运动（CM）指标更是大幅提升 14.3 个百分点（从 34.0 到 48.3）（Table 2）。这种“即插即用”的特性使其具有极强的模型无关性——在 **InternVL3-78B**（Zhu et al., 2025a）上同样观察到 1.5 个百分点的整体提升（61.5 → 63.0）。

3.  **与大型模型的竞争力**：值得注意的是，MotionSight 增强的 Qwen2.5VL-7B 在 FAVOR-Bench 上达到 44.1% 平均准确率，显著缩小了与大型开源模型 **LLaVA-NeXT-Video-34B**（Zhang et al., 2024a）和 **Qwen2.5VL-72B**（48.1%）的差距（Table 3）。当进一步利用 MotionSight 生成的高质量数据集 MotionVid-QA 进行 SFT+DPO 微调后，**MotionChat**（基于 Qwen2.5VL-7B）在 FAVOR-Bench 上达到 48.3% 总体准确率，与 Qwen2.5VL-72B 的 48.1% 持平（Table 4）。

### 关键设计选择与消融证据

MotionSight 的方法设计由一系列消融实验支撑，揭示了若干关键因果机制：

-   **视觉聚光灯优于坐标输入**：直接向 MLLM 输入边界框坐标的方法性能不及视觉聚光灯（Table 11），表明**视觉层面的注意力引导**比文本坐标描述更有效地激活了模型的运动感知能力。

-   **背景暗化优于背景模糊**：在对象运动理解中，视觉聚光灯（暗化背景）取得最高平均分，而直接应用背景模糊反而损害性能（Table 6）。这暗示 MLLM 对“舞台聚光灯”式的视觉提示存在天然的响应偏好。

-   **运动模糊对摄像机运动的关键作用**：全局运动模糊合成显著提升了摄像机运动理解，效果优于所有其他视觉提示方法（Table 6）。这表明通过时序加权平均（Eq. 5）引入的人工运动模糊有效补偿了 MLLM 对帧间细微差异的感知不足。

-   **超参数敏感性**：消融实验确定了最优超参数组合——暗化因子 0.9（Table 12）、时序窗口大小 N=7（Table 13）、衰减因子 γ=0.65（Table 14），表明视觉提示的强度需要精确校准。

### 适用边界与局限

尽管 MotionSight 展示了显著的零样本增强能力，其适用边界受以下因素制约：

1.  **对象检测依赖**：方法准确性部分依赖于对象检测模块（$M_{detect}$），在特定领域（如医学影像、工业检测）可能需要微调检测模型才能有效工作。

2.  **无显著对象场景退化**：在缺乏显著运动主体的场景（如纯风景、抽象动画）中，视觉聚光灯的优势会减弱甚至消失。此时 Camera-only 分支能否独立支撑细粒度运动理解仍有待验证。

3.  **超参数泛化性**：运动模糊模块的窗口大小 N 和衰减因子 γ 在不同视频内容（如快速运动 vs. 缓慢运动）上可能需要重新调整，当前的最优值来自特定基准的消融实验。

4.  **推理延迟**：零样本方法引入额外推理开销，作者声称平均延迟增加少于 75%，相较其他工作流较轻量，但在实时应用中仍需权衡。

### 开放问题

1.  **预过滤阈值的透明性**：数据集预过滤使用的光流阈值 $\tau_f$ 和清晰度阈值 $\tau_c$（Eq. 8）未具体说明，不同阈值如何影响最终数据集质量与模型性能需要进一步公开。

2.  **分布偏移风险**：视觉聚光灯的成功是否部分来源于 MLLM 训练数据中已有的“舞台聚光灯”效应，导致模型对特定视觉模式产生偏好而非真正理解运动？这需要在更多分布外数据上验证。

3.  **数据集覆盖扩展**：MotionVid-QA 的偏好对齐依赖有限的人工标注，如何进一步扩展规模和标注类型以覆盖更多样的运动与交互模式（如多对象交互、非刚体变形）仍是开放挑战。

4.  **与轻量时序适配器的结合**：可否将视觉提示策略与轻量级时序适配器（如 temporal adapter）结合，在保持零样本灵活性的同时进一步降低推理延迟？这可能是通向实用化部署的关键路径。



## 原文 PDF

![[paperPDFs/arxiv_2025/MotionSight_Boosting_Fine_Grained_Motion_Understanding_in_Multimodal_LLMs.pdf]]
