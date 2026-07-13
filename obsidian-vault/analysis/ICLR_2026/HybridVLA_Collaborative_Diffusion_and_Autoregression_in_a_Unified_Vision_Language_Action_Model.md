---
title: "HybridVLA: Collaborative Diffusion and Autoregression in a Unified Vision-Language-Action Model"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/HybridVLA_Collaborative_Diffusion_and_Autoregression_in_a_Unified_Vision_Language_Action_Model.pdf
project_link: https://hybrid-vla.github.io/
code_link: null
openreview_forum_id: H1KDMNOKQn
aliases:
- HybridVLA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将扩散去噪过程嵌入LLM的next-token预测机制，使LLM统一执行扩散和自回归动作生成，并通过协作训练配方实现相互增强。"
primary_logic: "自回归与扩散生成在VLA建模中具有互补优势：扩散擅长精细控制和动态场景，自回归更鲁棒于未见对象和指令。通过在统一的LLM骨干中联合训练这两种范式，并利用自适应集成机制，可以同时继承VLM的推理能力与扩散的连续精度，实现协同增强。"
claims:
- "混合训练目标使得自回归和扩散生成相互增强，单独使用各自损失训练时性能较低。"
- "将扩散去噪过程嵌入LLM内部优于附加外部扩散头，证明LLM作为动作专家的有效性。"
- "协同训练产生了更紧密的类内聚类和更大的类间分离，有利于动作生成。"
- "自适应集成自回归和扩散动作进一步提高了机器人控制鲁棒性。"
---

# HybridVLA: Collaborative Diffusion and Autoregression in a Unified Vision-Language-Action Model

> [!tip] 核心洞察
> 自回归与扩散生成在VLA建模中具有互补优势：扩散擅长精细控制和动态场景，自回归更鲁棒于未见对象和指令。通过在统一的LLM骨干中联合训练这两种范式，并利用自适应集成机制，可以同时继承VLM的推理能力与扩散的连续精度，实现协同增强。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | HybridVLA：统一视觉-语言-动作模型中的协作式扩散与自回归生成 |
| 英文题名 | HybridVLA: Collaborative Diffusion and Autoregression in a Unified Vision-Language-Action Model |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=H1KDMNOKQn) · [Project](https://hybrid-vla.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | HybridVLA |
| Dataset | RLBench (10 tasks), SimplerEnv (4 tasks), Real-world Single-arm (5 tasks) |

> [!tip] 效果简介
> - RLBench (10 tasks) 上，Mean Success Rate 为 0.78 ±0.04，对比 0.61 ±0.03 (π0 2.6B)，变化 +0.17。
> - RLBench (10 tasks) 上，Mean Success Rate 为 0.78 ±0.04，对比 0.41 ±0.02 (OpenVLA 7B)，变化 +0.37。
> - SimplerEnv (4 tasks) 上，Mean Success Rate 为 0.59，对比 0.49 (π0 2.6B)，变化 +0.10。

## 概要

### 问题瓶颈

视觉-语言-动作模型（VLA）的核心挑战在于如何将大规模预训练视觉-语言模型（VLM）的知识有效迁移至连续机器人控制。现有方法陷入两难困境：**自回归VLA方法**（如OpenVLA）通过离散化动作来复用VLM的next-token预测范式，但动作离散化破坏了连续控制所需的精度；**扩散式VLA方法**（如π0、CogACT）在VLM后附加独立的扩散头，仅将VLM降格为特征提取器，未能充分释放LLM作为动作生成专家的潜力。两种范式各自为政，缺乏将VLM推理能力与扩散连续精度有机融合的机制。

### 核心方法

**HybridVLA**提出了一种统一框架，在单一LLM骨干中同时执行扩散与自回归动作生成。其核心创新在于：将扩散去噪过程嵌入LLM的next-token预测机制，使每个去噪步成为LLM内部的一次推理迭代；通过协作训练配方（混合损失 $\mathcal{L}_{hybrid} = \mathcal{L}_{ar} + \mathcal{L}_{dif}$）实现两种生成范式的相互增强；并设计自适应动作集成机制，根据自回归token置信度动态融合两类动作。

### 方法定位

在VLA方法谱系中，HybridVLA占据**统一生成范式**的新位置——不同于纯自回归方法（ARP、ManipLLM、OpenVLA）的动作离散化路线，也不同于纯扩散方法（π0、CogACT）的外挂扩散头路线，而是将扩散与自回归统一于LLM内部，使LLM同时承担多模态理解与双范式动作生成的双重角色。

### 主要结果

- **仿真基准（RLBench 10任务）**：HybridVLA（7B）平均成功率达0.78，较π0（2.6B）提升17%，较OpenVLA（7B）提升37%。
- **真实世界单臂操作（5任务）**：平均成功率0.83，较π0提升22%。
- **真实世界双臂操作（5任务）**：平均成功率0.71，较π0提升16%。
- **SimplerEnv（4任务）**：平均成功率0.59，较π0提升10%。
- **关键消融**：混合训练使自回归动作成功率从0.57提升至0.65（+8%），扩散动作成功率从0.65提升至0.72（+7%）；协作动作集成进一步将成功率推至0.78。将扩散模块移出LLM改为外部头后，性能从0.72降至0.67或0.59，验证了LLM作为动作专家的必要性。

### 局限与展望

模型在精确旋转控制、双臂协调和推理速度（集成模式6.1 Hz）方面仍有不足，且大规模预训练需760K轨迹、超10K A800 GPU小时。未来方向包括加速推理、动态损失权重调整、跨具身泛化以及协同训练的理论分析。



视觉-语言-动作（VLA）模型的核心目标是将视觉感知、语言理解与机器人动作生成统一于单一模型中，使机器人能够根据图像观测 $o_t$、语言指令 $l_t$ 和自身状态 $r_t$，直接预测未来的动作序列 $a_{t+1:t+H}$。动作通常表示为 SE(3) 空间中的 7 维向量：$a = [\Delta x, \Delta y, \Delta z, Roll, Pitch, Yaw, 0/1]$，涵盖末端执行器的相对平移、欧拉角旋转和夹爪开合状态。这一任务对生成范式的选择极为敏感：既需要连续控制的精细精度，又需要语义层面的鲁棒推理。

当前 VLA 方法主要沿两条技术路线展开，但各自存在结构性缺陷。

**自回归 VLA 方法的瓶颈。** 这类方法（如 **OpenVLA**、**ManipLLM**、**ARP**）将连续动作离散化为 token，利用大语言模型（LLM）的 next-token prediction 范式进行预测。其优势在于能够直接继承 VLM 预训练中积累的语义理解和指令跟随能力。然而，离散化操作从根本上破坏了连续控制所需的精度——动作空间中的微小偏差在离散化后可能映射到截然不同的 token，导致精细操作（如倒水、精确放置）中出现累积误差。从因果机制上看，离散化引入的量化噪声是自回归 VLA 在需要高精度连续控制的任务上性能受限的直接原因。

**扩散 VLA 方法的瓶颈。** 另一类方法（如 **π0**、**CogACT**）在 VLM 之后附加独立的扩散头，利用扩散模型的连续去噪过程生成动作。扩散范式天然适合连续动作空间，在精细控制和动态场景中表现优异。但这类方法的架构设计存在根本性局限：VLM 仅被降格为视觉特征提取器，扩散头独立于 LLM 运作，无法利用 LLM 内部的预训练知识进行动作推理。LLM 中蕴含的物体语义、空间关系和指令理解能力未能有效传递到动作生成环节，导致模型在未见物体和未见指令场景下的泛化能力受限。

**核心洞察：互补而非替代。** 实验证据表明，自回归与扩散生成在 VLA 建模中具有清晰的互补优势：扩散擅长精细控制和动态场景（动作精度显著更高），而自回归对未见对象和指令更为鲁棒（性能退化更小，见 Figure 3）。这意味着，两种范式并非竞争关系，而是可以通过协同设计实现相互增强。关键问题在于：如何在保持 VLM 预训练知识完整性的前提下，将扩散的连续精度能力注入动作生成过程？

**现有方案的架构断层。** 无论是自回归还是扩散 VLA，现有方法都将两种生成范式割裂开来——要么完全依赖离散化，要么将扩散作为外部模块附加。缺少一种统一的架构设计，使得 LLM 自身能够同时作为自回归推理引擎和扩散去噪专家，从而在单一骨干网络中融合两种范式的优势。这一架构断层正是 HybridVLA 试图填补的核心缺口。



## 核心方法与创新机理

HybridVLA 的核心创新在于将扩散去噪过程嵌入单一LLM骨干的next-token预测机制中，使LLM统一执行扩散与自回归两种动作生成范式，并通过协作训练实现相互增强。与现有方法相比，这一设计在四个关键维度上实现了范式转变：

### 从“附加扩散头”到“LLM作为动作专家”

现有扩散式VLA方法（如 **π0**、**CogACT**）在VLM后附加独立的扩散头，仅将LLM作为视觉-语言特征提取器，未能充分利用LLM的预训练推理能力。HybridVLA将扩散去噪过程直接嵌入LLM内部：扩散时间步和噪声动作通过可学习的投影层映射为连续向量，由专用标记`<BOD>`/`<EOD>`封装后输入LLM，使LLM自身执行去噪预测（Figure 1）。

消融实验验证了这一设计的必要性：将扩散模块从LLM内部移出、改为外部附加Transformer扩散头后，性能从0.72显著降至0.67（保留AR生成）或0.59（禁用AR生成）（Table 13, Variation 1和2）。这表明LLM作为动作生成专家，其预训练知识对于扩散去噪具有不可替代的价值。

### 从“单一损失”到“混合训练目标”

现有方法分别使用独立的交叉熵损失（自回归VLA）或扩散损失（扩散VLA）进行训练。HybridVLA引入混合损失 $\mathcal{L}_{hybrid} = \mathcal{L}_{ar} + \mathcal{L}_{dif}$，在统一骨干中联合优化两种生成范式。

这一设计的关键效果是**相互增强**而非简单叠加：
- 混合训练使自回归动作生成成功率从0.57提升至0.65（+8%）（Table 3, Ex1 vs Ex2）
- 混合训练使扩散动作生成成功率从0.65提升至0.72（+7%）（Table 3, Ex3 vs Ex4）

PCA特征分析揭示了协同训练的表征层面机制：联合训练使扩散令牌特征的类内聚类更紧密（类内距离0.49 vs 独立训练0.73），同时使自回归令牌特征的类间分离更大（类间距离10.8 vs 独立训练4.4）（Table 7）。这表明两种损失在共享表征空间中产生了正向的梯度交互。

### 从“固定顺序”到“防泄漏令牌序列设计”

在统一LLM中同时生成扩散和自回归动作，面临令牌序列组织的关键挑战。HybridVLA通过消融实验确定了最优序列方案：将扩散令牌（`<BOD>`包裹）置于自回归令牌之前（Table 1, Type 4）。这一设计防止了自回归令牌的信息泄漏到扩散去噪过程中，同时避免了两种范式间的语义混淆。

### 从“单一动作”到“自适应动作集成”

推理阶段，HybridVLA同时生成扩散动作 $a_{t+1}^{d}$ 和自回归动作 $a_{t+1}^{ar}$。基于自回归令牌的平均置信度 $c_{t+1}^{ar}$ 与阈值 $\theta = 0.96$ 的比较，自适应地选择融合策略：当置信度高于阈值时集成两种动作，否则仅使用扩散动作。这一机制将集成模式下的成功率从单独使用扩散动作的0.72进一步提升至0.78（Table 3, Ex4 vs Ex5），在保持扩散动作精细控制优势的同时，利用自回归动作的语义鲁棒性增强整体控制稳定性。



![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/001_Figure_1.jpg]]
*Figure 1: (a) Unlike recent diffusion-based VLA methods that attach a separate diffusion head after VLMs, (b) HybridVLA innovatively integrates diffusion and autoregressive action prediction within a single LLM, embedding the denoising process of diffusion into the next-token prediction. Under our proposed methods, HybridVLA achieves remarkable performance across a wide range of tasks*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/002_Figure_2.jpg]]
*Figure 2: HybridVLA Framework. All multimodal inputs are encoded into tokens and subsequently organized into our designed token sequence formulation within the LLM’s embedding space. For diffusion tokens, HybridVLA simultaneously projects the denoising timestep and noise into continuous vector representations. The corresponding noisy samples are iteratively fed into the LLM to predict the noise at each step. The marker tokens, ${ \bf \mathrm { < B O D > } }$ (Beginning of Diffusion) and <EOD> (End of Diffusion), are introduced to bridge the two generation paradigms. Subsequently, autoregressive actions are generated via next action-token prediction, explicitly conditioned on the preceding tokens. The t...

HybridVLA 的核心设计是将扩散去噪过程嵌入 LLM 的 next-token 预测机制中，使单一 LLM 骨干同时承担自回归与扩散两种动作生成范式，而非像现有方法那样在 VLM 后附加独立的扩散头（Figure 1）。

### 输入编码与 Token 序列组织

模型接收三类多模态输入：**图像观测** $o_t$、**语言指令** $l_t$ 和**机器人状态** $r_t$，输出未来动作序列 $a_{t+1:t+H}$，其中动作采用 SE(3) 表示 $a = [\Delta x, \Delta y, \Delta z, Roll, Pitch, Yaw, 0/1]$（Figure 2）。

**视觉编码器**采用 DINOv2 + SigLIP 组合（2.7B 版本使用 CLIP），将单视图或多视图 RGB 图像编码后沿通道维度拼接，经投影层映射至 LLM 嵌入空间。**机器人状态**则通过可学习 MLP 直接映射为嵌入向量 $f_r \in \mathbb{R}^{B \times 1 \times 4096}$。

**Token 序列组织**是 HybridVLA 的关键设计决策。通过消融实验（Table 1），最终采用 Type 4 方案：扩散 token（由 `<BOD>`/`<EOD>` 包裹）置于自回归 token 之前，防止信息泄漏与两种生成范式的混淆。

### 扩散生成管线

扩散 token 由**扩散时间步**和**噪声动作**经投影器编码为连续向量，封装在 `<BOD>` 与 `<EOD>` 标记之间送入 LLM。在每个去噪步，LLM 预测噪声 $\epsilon_\pi(a_t^i, i, c)$，损失函数为：

$$\mathcal{L}_{dif} = \mathbb{E}_{a,i,c} \|\epsilon - \epsilon_\pi(a_t^i, i, c)\|^2$$

推理时采用 DDIM 采样，去噪步数可压缩至 4 步而不显著牺牲性能（Figure 5）。

### 自回归生成管线

自回归生成在 `<EOD>` 标记之后开始。末端执行器位姿经**自回归分词器**离散化为离散 token，LLM 以标准 next-token 预测方式逐 token 生成，损失为交叉熵 $\mathcal{L}_{ar}$。

### 混合训练目标与协作动作集成

两种生成范式通过**混合损失**联合优化：

$$\mathcal{L}_{hybrid} = \mathcal{L}_{ar} + \mathcal{L}_{dif}$$

训练分为两阶段：先在大规模机器人数据集（35 个数据集、760K 轨迹、33M 帧）上预训练 10 个 epoch，再在下游数据上微调 300 个 epoch。

推理时，**协作动作集成模块**（CAE）根据自回归 token 的平均置信度 $c_{t+1}^{ar}$ 自适应融合两种动作：当置信度超过阈值 $\theta = 0.96$ 时采用自回归动作 $a_{t+1}^{ar}$，否则回退至扩散动作 $a_{t+1}^{d}$。该阈值在消融实验中验证为最优（Table 10），过高或过低均会降低性能。

### 关键设计验证

消融实验（Table 3）揭示了各模块的因果效应：
- **混合训练目标**使自回归和扩散生成相互增强：单独使用 $\mathcal{L}_{ar}$ 时自回归动作成功率为 0.57，加入混合训练后提升至 0.65（+8%）；单独使用 $\mathcal{L}_{dif}$ 时扩散动作成功率为 0.65，混合训练后达 0.72（+7%）。
- **将扩散模块嵌入 LLM 内部**优于附加外部扩散头：移除 LLM 内扩散模块改为外部 Transformer 扩散头后，性能从 0.72 降至 0.67（Variation 1），若同时禁用自回归则进一步降至 0.59（Variation 2，Table 13），验证了 LLM 作为动作专家的必要性。
- **协作动作集成**进一步将成功率从 0.72（纯扩散）提升至 0.78（+6%），证明两种范式具有互补优势。
- **协同训练**产生更紧密的类内聚类（扩散 token 类内距离 0.49 vs 独立训练 0.73）和更大的类间分离（自回归 token 类间距离 10.8 vs 4.4，Table 7），表明特征表示质量显著提升。



### 问题形式化

给定图像观测 $o_t$、语言指令 $l_t$ 和机器人状态 $r_t$，策略模型预测未来 $H$ 步动作序列：

$$\pi : \left( o _ { t } , l _ { t } , r _ { t } \right) \to a _ { t + 1 : t + H }$$

其中单步动作 $a$ 采用 SE(3) 表示：

$$a = [ \Delta x , \Delta y , \Delta z , Roll , Pitch , Yaw , 0 / 1 ]$$

包含末端执行器的相对平移量、欧拉角以及夹爪开合状态（0/1）。

### 核心模块

**1. 视觉编码器**：HybridVLA 7B 版本采用 DINOv2 + SigLIP 双编码器组合，2.7B 版本使用 CLIP。多视图图像经编码后沿通道维度拼接，通过投影层映射至 LLM 嵌入空间。

**2. LLM 骨干**：7B 版本使用 LLaMA-2，2.7B 版本使用 Phi-2。LLM 不仅承担多模态理解，更作为动作生成专家，在其内部同时执行扩散去噪和自回归预测。

**3. 扩散 Token 投影器**：将扩散时间步 $i$ 和当前噪声动作 $a_t^i$ 投影为连续向量，由专用标记 `<BOD>` 和 `<EOD>` 封装后嵌入 LLM。扩散去噪过程被嵌入 next-token 预测机制中——每个去噪步对应一次 LLM 前向传播，预测噪声 $\epsilon_\pi(a_t^i, i, c)$。

**4. 自回归分词器**：将末端执行器位姿离散化为离散 token，在 `<EOD>` 之后由 LLM 逐 token 自回归生成。

**5. 机器人状态 MLP**：将机器人本体状态（关节角度等）通过可学习 MLP 直接映射至嵌入空间。

**6. 协作动作集成模块**：根据自回归动作 token 的平均置信度 $c_{t+1}^{ar}$ 自适应融合扩散动作 $a_{t+1}^{d}$ 与自回归动作 $a_{t+1}^{ar}$。当 $c_{t+1}^{ar} > \theta$ 时采用自回归动作，否则使用扩散动作。阈值经验设定为 $\theta = 0.96$。

### 关键公式

**扩散损失**：预测噪声与真实高斯噪声的均方误差：

$$\mathcal{L}_{dif} = \mathbb{E}_{a,i,c} \|\epsilon - \epsilon_\pi(a_t^i, i, c)\|^2$$

**混合训练目标**：自回归交叉熵损失与扩散损失之和：

$$\mathcal{L}_{hybrid} = \mathcal{L}_{ar} + \mathcal{L}_{dif}$$

该混合损失是协同训练的核心——消融实验表明（Table 3），单独使用 $\mathcal{L}_{ar}$ 时自回归动作成功率为 0.57，加入混合训练后提升至 0.65；单独使用 $\mathcal{L}_{dif}$ 时扩散动作成功率为 0.65，混合训练后提升至 0.72。两种损失联合优化实现了相互增强，而非相互干扰。

### 训练与推理流程

训练分两阶段：先在大规模机器人数据集（35 个数据集、760K 轨迹、33M 帧）上预训练 10 个 epoch，再在下游数据上微调 300 个 epoch，全程使用混合目标 $\mathcal{L}_{hybrid}$。

推理时，扩散生成采用 DDIM 采样，去噪步数可压缩至 4 步而不显著牺牲性能（Figure 5），在速度与精度间取得平衡。扩散动作与自回归动作经置信度阈值机制自适应融合后输出。集成模式下推理速度约 6.1 Hz，纯扩散模式可达 9.4 Hz。



## 实验与关键发现

### 核心瓶颈与因果机制

HybridVLA的设计出发点是解决VLA领域的一个关键瓶颈：**自回归VLA方法**（如OpenVLA）通过将连续动作离散化为token来适配LLM的next-token预测范式，虽然继承了VLM的预训练知识，但破坏了连续控制所需的精度；**扩散VLA方法**（如π₀、CogACT）在VLM后附加独立的扩散头，仅将VLM作为特征提取器，未能充分利用LLM的预训练知识作为动作生成专家。

HybridVLA的核心因果调节变量是**将扩散去噪过程嵌入LLM的next-token预测机制内部**，使单一LLM骨干统一执行扩散和自回归两种动作生成。通过协作训练配方（混合损失 $\mathcal{L}_{hybrid} = \mathcal{L}_{ar} + \mathcal{L}_{dif}$），两种范式实现相互增强，而非相互干扰。在此基础上，自适应动作集成机制根据自回归token的置信度 $c_{t+1}^{ar}$（阈值 $\theta = 0.96$）动态融合两类动作，进一步提升控制鲁棒性。

### 仿真实验主结果

在RLBench的10个多任务操作场景中，HybridVLA（7B）取得了**0.78的平均成功率**，显著超越所有基线方法（Table 2）。具体而言：

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/004_Table_2.jpg]]
*Table 2: Comparison of HybridVLA and baselines on RLBench. We train all methods in the multi-task setting (Shridhar et al., 2022) and report the success rates (S.R.) and variances (Var.)*

- 相比自回归VLA方法 **OpenVLA**（7B，0.41），提升**+0.37**；
- 相比扩散VLA方法 **π₀**（2.6B，0.61），提升**+0.17**；
- 相比扩散VLA方法 **CogACT**（7B，0.60），提升**+0.18**。

值得注意的是，HybridVLA-dif（仅使用扩散动作生成）的平均成功率为0.72，已超越π₀（0.61）和CogACT（0.60），表明将扩散过程嵌入LLM内部优于附加外部扩散头的设计。HybridVLA（2.7B）以更小的模型规模达到0.67的平均成功率，仍优于所有7B级别的自回归基线。

在SimplerEnv的4个任务上（Table 9），HybridVLA（7B）平均成功率为0.59，比π₀（2.6B，0.49）高出**+0.10**，验证了方法在不同仿真环境下的泛化能力。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/019_Table_9.jpg]]
*Table 9: Evaluation results on SimperEnv. We evaluate our models in the variant aggregation setting of the Google Robot benchmark, where the number of test trials per scene follows the official protocol. All models are finetuned on the Fractal dataset. Bold indicates the highest score*

### 消融实验：各组件贡献

Table 3的系统消融揭示了各组件的因果贡献：

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/005_Table_3.jpg]]
*Table 3: Impact of each component. AR and Dif denote that use solely autoregressive and diffusionbased action, respectively. CAE indicates the collaborative action ensemble method, whereas LSP refers to large-scale pretraining on robotic datasets*

**混合训练目标的相互增强效应**：单独使用自回归损失训练时（Ex1），平均成功率仅为0.57；引入混合训练目标后（Ex2），自回归动作成功率提升至0.65（**+8%**）。类似地，单独使用扩散损失（Ex3）时成功率为0.65，混合训练后（Ex4）提升至0.72（**+7%**）。这表明两种生成范式在联合训练中产生了正向协同效应，而非负向干扰。

**协作动作集成的增益**：在混合训练的基础上引入协作动作集成模块（Ex5），成功率从0.72进一步提升至0.78（**+6%**），验证了自适应融合两种动作模式对控制鲁棒性的增强作用。

**大规模预训练的必要性**：移除大规模机器人数据预训练后（Ex6），成功率从0.78降至0.69（**-9%**），说明预训练阶段对模型性能有实质性贡献。该预训练使用了35个数据集、760K条机器人轨迹、33M帧图像，消耗超过10K A800 GPU小时。

**LLM作为动作专家的验证**：Table 13的关键消融表明，将扩散模块从LLM内部移除、改为外部附加Transformer扩散头的设计会导致性能显著下降——Variation 1（外部头，保留AR）成功率为0.67（vs HybridVLA-dif 0.72），Variation 2（外部头，禁用AR）进一步降至0.59。这有力地证明了LLM内部执行扩散去噪的独特价值。

### 扩散与自回归的互补优势

Figure 3和Table 6揭示了两种生成范式的相对优势：

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/014_Figure_3.jpg]]
*Figure 3: Respective strengths of diffusion-based and autoregressive action generation paradigms. We evaluate the performance of Our-ar and Our-dif across a variety of scenarios*

- **扩散生成**在已见场景中表现更强（成功率0.72 vs 0.65），擅长精细控制和动态场景；
- **自回归生成**对未见指令和对象更鲁棒，在未见语言场景中成功率下降幅度更小（相对下降-0.09 vs -0.20），表明其更好地保留了VLM的语义理解能力。

这种互补性正是协作集成能够进一步提升性能的基础。

### 特征空间分析

Table 7的PCA分析为协同训练的有效性提供了表征层面的证据：与独立训练相比，协同训练下扩散token特征的**类内距离从0.73降至0.49**（聚类更紧密），自回归token特征的**类间距离从4.4增至10.8**（分离更大）。这表明混合训练目标改善了LLM内部的动作相关特征表示质量，为两种生成范式的相互增强提供了几何解释。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/015_Table_7.jpg]]
*Table 7: PCA feature analysis of HybridVLA. Comparison of intra-class and inter-class distances under collaborative training versus independent training. Collaborative optimization yields tighter intra-class clustering and larger inter-class separation*

### 关键超参数分析

**置信度阈值**（Table 10）：阈值0.96给出最优集成效果（平均成功率0.78）。阈值过低（0.90，0.74）会导致不可靠的自回归动作污染集成结果；阈值过高（0.98，0.71）则过度依赖扩散动作，丧失了集成带来的互补优势。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/020_Table_10.jpg]]
*Table 10: Confidence threshold. We explore the impact of different confidence thresholds on the performance of ensemble actions. The model used for testing is HybridVLA (7B)*

**扩散去噪步数**（Figure 5）：去噪步数可减少至4步而不显著牺牲性能，在速度与精度之间取得平衡。仅使用扩散生成时推理速度为9.4 Hz，集成模式下为6.1 Hz，低于π₀（13.8 Hz）和CogACT（9.8 Hz），这是当前方法的一个实际限制。

### 真实世界实验结果

在真实世界单臂操作任务中（Table 5），HybridVLA取得了**0.83的平均成功率**，比π₀（0.61）高出**+0.22**。在Pour water任务上优势尤为显著（0.80 vs 0.45，**+35%**），该任务对旋转精度要求高，体现了扩散生成在精细控制方面的优势。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/007_Table_5.jpg]]
*Table 5: Real-world experiments. The manipulation success is determined by human evaluation. Since CogACT lacks support for multi-view images, which are crucial for dual-arm tasks (Black et al., 2024; Fu et al., 2024), we conduct our dual-arm comparison solely with $\pi _ { 0 }$*

在双臂协作任务中，HybridVLA平均成功率为0.71，比π₀（0.55）高出**+0.16**。由于CogACT不支持多视图输入（对双臂任务至关重要），双臂对比仅与π₀进行。

### 泛化能力

Table 6展示了在未见物体、背景、空间位置和光照条件下的泛化性能。HybridVLA在Pick and place任务上对未见配置的平均成功率为0.71，而CogACT为0.51，π₀为0.52。整体上，HybridVLA在泛化场景中的精度下降比基线方法低5–16%，表明统一框架更好地保留了VLM的语义泛化能力。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/010_Table_6.jpg]]
*Table 6: Generalization. “Object”, “Background”, “Height”, and “Lighting” denote unseen manipulated objects, backgrounds, spatial positions, and lighting conditions, respectively. The image on the left depicts the unseen test scenarios, with red boxes marking the key differences*

### 失败模式与局限性

尽管整体性能优异，HybridVLA存在以下典型失败模式：

1. **旋转预测偏差**：在需要精确旋转控制的任务中（如倒水、放置瓶子到架子），模型可能出现累积误差或旋转角度错误，这源于欧拉角表示的固有限制。
2. **动作超出物理限制**：模型有时会预测超出机械臂工作空间或关节极限的位姿，表明对机器人运动学约束的隐式学习仍不充分。
3. **双臂协调故障**：在双臂协作任务中，一臂的动作会改变物体状态，可能导致另一臂的先前预测失效，模型缺乏对动作间动态耦合的显式建模。
4. **推理速度瓶颈**：集成模式下的6.1 Hz推理速度低于部分基线，可能不满足高频控制场景的需求。仅使用扩散生成可提升至9.4 Hz，但仍需进一步优化。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/006_Table_4.jpg]]
*Table 4: The impact of different confidence threshold. We report success rates for HybridVLA (7B) and HybridVLA (2.7B) on various tasks with confidence threshold from 0.90 to 0.98*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_H1KDMNOKQn/figures/016_Table_8.jpg]]
*Table 8: The dataset name and sampling weight used in our mixed large-scale pretraining dataset*



## 定位与知识库关联

### 核心瓶颈与设计动机

当前VLA（Vision-Language-Action）建模存在两条主流技术路线，各自面临结构性困境：

**自回归VLA路线**（如 **OpenVLA** 7B、**ManipLLM** 7B）通过将连续动作离散化为token，直接复用VLM的next-token prediction预训练范式。这一策略虽然继承了LLM的推理能力和对象级语义理解，但离散化过程不可避免地破坏了连续控制所需的精度——每个动作维度被量化到有限个离散区间，导致精细操作（如精确旋转、微小位移）中的累积误差难以消除。

**扩散VLA路线**（如 **π0** 2.6B、**CogACT** 7B）在VLM输出端附加独立的扩散去噪头，利用扩散模型的连续生成能力保持动作精度。然而，这种架构将VLM降格为特征提取器，扩散头与LLM骨干之间仅通过隐层特征单向连接，LLM内部的预训练知识（因果推理、指令理解、物理常识）无法有效参与去噪过程，导致模型在未见对象和复杂指令下的泛化能力受限。

HybridVLA的核心洞察在于：**自回归与扩散并非互斥的替代方案，而是在VLA建模中具有互补优势的两种生成范式**。扩散擅长精细控制和动态场景下的连续动作生成，自回归更鲁棒于未见对象和语义指令的理解。问题不在于选择哪一种，而在于如何在统一的LLM骨干中让两者协同工作。

### 方法差异点：与现有工作的关键区别

与前述两类方法的根本差异体现在四个维度：

**1. 动作生成范式的统一性。** 现有扩散VLA方法（π0、CogACT）将扩散头作为LLM的外部附加模块，自回归VLA方法（OpenVLA、ManipLLM）则完全放弃扩散。HybridVLA将扩散去噪过程嵌入LLM的next-token预测机制内部——扩散时间步和噪声动作通过投影层进入LLM的嵌入空间，由`<BOD>`/`<EOD>`特殊标记封装，LLM直接预测噪声残差。这一设计使LLM从被动的特征提取器转变为主动的动作生成专家。

**2. Token序列的组织策略。** 在同时包含扩散和自回归token的序列中，HybridVLA将扩散token置于自回归token之前（Table 1, Type 4），而非之后或交错排列。这一顺序设计的因果逻辑在于：扩散去噪是一个从噪声到清晰动作的渐进过程，其输出为后续的自回归离散预测提供了高质量的连续动作先验；反之，若自回归token在前，其离散化误差会污染扩散token的初始化。

**3. 训练目标的联合优化。** 现有方法各自使用单一损失（自回归交叉熵或扩散MSE），HybridVLA采用混合损失$\mathcal{L}_{hybrid} = \mathcal{L}_{ar} + \mathcal{L}_{dif}$进行端到端联合训练。消融实验（Table 3）提供了强因果证据：单独使用自回归损失时成功率为0.57（Ex1），加入扩散损失联合训练后提升至0.65（Ex2）；单独使用扩散损失时为0.65（Ex3），联合训练后提升至0.72（Ex4）。两种范式在联合优化中实现了相互增强，而非相互干扰。

**4. 动作融合机制。** 现有方法仅输出单一种类的动作。HybridVLA提出协作动作集成（Collaborative Action Ensemble, CAE），以自回归token的平均置信度$c_{t+1}^{ar}$为信号，当置信度超过阈值$\theta = 0.96$时采用自回归动作，否则回退至扩散动作。这一机制使集成后的成功率从纯扩散的0.72进一步提升至0.78（Table 3, Ex5 vs Ex4）。

### 适用边界与局限

**计算资源需求。** HybridVLA需要大规模预训练（35个数据集、760K轨迹、33M帧），预训练消耗超过10K A800 GPU小时。对于资源受限的研究团队，直接复现完整训练流程存在较高门槛。2.7B版本（Phi-2骨干）在一定程度上缓解了这一问题，但其RLBench平均成功率（0.67）与7B版本（0.78）仍有显著差距。

**推理速度约束。** 在集成模式下，推理速度为6.1 Hz，低于π0的13.8 Hz和CogACT的9.8 Hz。速度瓶颈主要来自自回归token的逐token生成过程。仅使用扩散模式时速度可提升至9.4 Hz，但会丧失自回归分支的鲁棒性优势。扩散去噪步数可压缩至4步而不显著牺牲性能（Figure 5），但仍无法完全弥合与纯自回归或纯扩散方法的延迟差距。

**旋转控制精度。** 在需要精确旋转操作的任务中（如倒水、将瓶子放置到架子），模型可能出现旋转角度的累积误差。这一问题在真实世界实验中表现为Pour water任务的成功率（0.80）虽已大幅领先基线（π0为0.45），但仍有20%的失败率，部分失败案例源于旋转预测偏差。

**双臂协调故障。** 在双机械臂协作任务中，HybridVLA为双臂分别预测动作，但缺乏显式的臂间协调建模。当一臂的动作改变了共享物体的状态时，另一臂的先前预测可能失效。真实世界双臂任务平均成功率为0.71，低于单臂的0.83，部分差距可归因于此。

**动作空间约束。** 模型有时会预测超出机械臂物理极限的位姿或超出工作空间的位置，表明当前方法缺乏对机器人运动学约束的显式建模。

### 开放问题

1. **推理加速的极限。** 扩散去噪步数已压缩至4步，是否可以通过一致性模型或蒸馏技术压缩至1步而不损失性能？自回归分支的逐token生成能否通过投机解码或并行预测加速？

2. **动态损失权重。** 当前混合损失中$\mathcal{L}_{ar}$和$\mathcal{L}_{dif}$的权重为静态的1:1。是否可以设计任务感知或训练阶段感知的动态权重调整机制，使模型在训练的早期阶段侧重扩散精度、后期阶段强化自回归鲁棒性？

3. **跨具身泛化。** 当前方法针对特定机器人平台（Franka FR3、AgileX双臂）进行微调。该统一框架能否泛化到具有不同动作空间（如关节空间vs末端执行器空间）、不同自由度和动力学的机器人平台？跨具身的协同训练是否会带来额外的表征收益？

4. **协同训练的理论机制。** PCA分析（Table 7）已初步验证协同训练导致扩散token特征的类内聚类更紧密（类内距离0.49 vs 0.73独立训练）和自回归token特征的类间分离更大（10.8 vs 4.4）。但两种损失函数在优化动力学中如何相互作用、是否存在隐式的互信息最大化机制，仍需更深入的理论分析。

5. **扩展到全身控制。** 当前方法仅预测末端执行器位姿，是否能将该统一框架扩展到包含基座移动、躯干姿态、手指关节的全身控制任务？扩散与自回归的分工模式在更高维动作空间中是否依然有效？



## 原文 PDF

![[paperPDFs/ICLR_2026/HybridVLA_Collaborative_Diffusion_and_Autoregression_in_a_Unified_Vision_Language_Action_Model.pdf]]
