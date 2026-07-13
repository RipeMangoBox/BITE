---
title: "Astra: General Interactive World Model with Autoregressive Denoising"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Astra_General_Interactive_World_Model_with_Autoregressive_Denoising.pdf
project_link: https://eternalevan.github.io/Astra-project/
code_link: https://github.com/EternalEvan/Astra
aliases:
- Astra
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "Astra adapts a pretrained video diffusion transformer with action-aware adapters, noise-as-mask history, MoAE routing, and action-free guidance."
primary_logic: "It autoregressively denoises future video chunks conditioned on noisy history and heterogeneous action streams, then amplifies action-conditioned velocity at inference."
claims:
- "Noise-as-mask reduces visual inertia and forces the model to attend to action signals."
- "MoAE maps camera, robot, and navigation actions into a unified action embedding through modality-specialized experts."
- "The note reports higher Astra-Bench instruction following and visual consistency than Wan-2.1, Matrix-Game, and YUME."
---

# Astra: General Interactive World Model with Autoregressive Denoising

> [!tip] 核心洞察
> 通过噪声增强历史记忆（noise-as-mask）削弱视觉惯性，迫使模型在生成未来帧时同时依赖历史上下文和动作信号；混合动作专家（MoAE）统一处理异构动作模态。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Astra：基于自回归去噪的通用交互式世界模型 |
| 英文题名 | Astra: General Interactive World Model with Autoregressive Denoising |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8UZpmrxoLG) · [GitHub](https://github.com/EternalEvan/Astra) · [Project](https://eternalevan.github.io/Astra-project/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Astra |
| Dataset | Astra-Bench |

> [!tip] 效果简介
> - Astra-Bench 上，Instruction Following ↑ 为 0.669，对比 Wan-2.1: 0.084, Matrix-Game: 0.247, YUME: 0.619，变化 +0.05 vs YUME。
> - Astra-Bench 上，Subject Consistency ↑ 为 0.939，对比 Wan-2.1: 0.827, Matrix-Game: 0.923, YUME: 0.933，变化 +0.006 vs YUME。
> - Astra-Bench 上，Background Consistency ↑ 为 0.945，对比 Wan-2.1: 0.843, Matrix-Game: 0.939, YUME: 0.927，变化 +0.006 vs Matrix-Game。

## 概要

Astra 是一种通用的交互式世界模型，旨在根据外部动作输入（如相机位姿、机器人控制指令、键盘鼠标操作）动态生成连贯的视频序列。该模型采用自回归去噪框架，将预训练的视频扩散模型（Wan-2.1）与动作感知适配器（ACT-Adapter）相结合，通过逐块自回归预测实现即时动作响应。核心创新包括：噪声增强历史记忆（noise-as-mask）策略以削弱视觉惯性、混合动作专家（MoAE）以统一处理异构动作模态，以及动作自由引导（AFG）以放大动作信号效果。在Astra-Bench和CityWalker等基准测试中，Astra在指令跟随、主体一致性、背景一致性、运动平滑度、美学质量和成像质量六个指标上均优于现有方法。



现有视频生成模型（如Sora、Wan-2.1）在生成高质量视频方面取得了显著进展，但存在一个根本性瓶颈：**缺乏交互性**。这些模型无法根据外部动作输入动态调整生成内容，且难以在长时间预测中平衡历史一致性与动作响应性。具体而言：

- **视觉惯性问题**：当模型使用干净历史帧作为条件时，会过度依赖视觉上下文而忽略动作信号，导致生成内容无法准确反映用户指定的动作。
- **异构动作模态挑战**：不同应用场景（自动驾驶、机器人操作、相机控制）使用不同结构和尺度的动作表示（如7维相机位姿、7维机器人动作、离散键盘鼠标输入），单一模型难以统一处理。
- **长时预测一致性**：自回归生成过程中误差会逐步累积，极长序列的质量和一致性难以保证。



## 核心方法与创新机理

Astra 的核心洞察在于：**通过噪声增强历史记忆削弱视觉惯性，迫使模型在生成未来帧时同时依赖历史上下文和动作信号；混合动作专家统一处理异构动作模态**。具体创新点包括：

1. **噪声增强历史记忆（Noise-as-Mask）**：在训练时向历史帧注入随机噪声，削弱视觉主导地位，迫使模型整合动作信号。
2. **ACT-Adapter（Action-Aware Flow Transformer Adapter）**：在每个Transformer块后插入线性层（初始化为恒等映射），通过逐元素加法将动作特征直接注入潜空间。
3. **混合动作专家（MoAE）**：通过可学习路由将不同模态映射到专用专家，输出聚合为统一动作嵌入。
4. **动作自由引导（AFG）**：训练时随机丢弃动作条件，推理时通过外推计算引导速度场，放大动作效果。



![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_8UZpmrxoLG_Astra_General/figures/001_Figure_1.jpg]]

Astra 的整体框架如Figure 2和Figure 3所示。模型采用自回归去噪架构，从初始图像、动作序列和可选文本提示开始，逐块生成未来视频帧。

**Figure 2**: Overview of the proposed Astra. Our autoregressive denoising world model generates future video chunk by chunk from an initial image, actions, and optional prompts. Chunk-wise causal conditioning enforces temporal coherence and faithful action response.

**Figure 3**: The overall framework of Astra. The Action-Aware Flow Transformer (AFT) injects action signals into the latent space via an ACT-Adapter (right), which aligns action features through an encoder and adds them to each transformer block. During training (left top), the model learns next-chunk prediction with flow matching. During inference (left bottom), it autoregressively generates video chunks conditioned on history and action streams, producing interactive videos.

**Figure 4**: Mixture of Action Experts (MoAE). Action signals from diverse modalities are projected into a shared space, augmented with a history mask, and routed to modality-specialized experts. A dynamic router selects top-k experts, whose outputs are aggregated into unified embeddings and fed into the Flow Transformer, enabling versatile and precise action-conditioned generation.



### 5.1 自回归生成目标

给定视频序列离散化为块 $z^{1:N}$，生成目标为：

$$p(z^{1:N}) = \prod_{i=1}^{N} p(z^{i} \mid z^{<i})$$

该公式将视频块序列的联合概率分解为每个块在给定先前块条件下的概率乘积。

### 5.2 流匹配噪声插值

对于每个块 $z^i$，训练时使用流匹配（flow matching）方法。目标块与高斯噪声在时间 $t$ 处线性插值：

$$z_t^i = (1 - t) z_0^i + t \epsilon, \quad \epsilon \sim \mathcal{N}(0, I), t \in [0, 1]$$

### 5.3 流匹配损失

训练流模型预测从噪声插值到干净数据的真实速度方向：

$$\mathcal{L}(\theta) = \mathbb{E}_{i,t,\epsilon} \left[ \| \mathbf{v}_\theta(z_t^i, t \mid z^{<i}) - \mathbf{v}^*(z_t^i, t \mid z^{<i}) \|_2^2 \right]$$

### 5.4 动作自由引导（AFG）

推理时，通过从无条件预测外推至有条件预测来放大动作信号的效果：

$$v_{\mathrm{guided}} = v_\theta(z_t, t, \emptyset) + s \cdot \left( v_\theta(z_t, t, a) - v_\theta(z_t, t, \emptyset) \right)$$

其中 $s$ 为引导尺度，推理时设为3.0。

### 5.5 核心模块设计

- **3D VAE编码器**：将视频帧编码到潜空间，训练在潜空间中进行。
- **动作编码器**：将原始动作信号投影到与视频潜变量对齐的特征空间。
- **ACT-Adapter**：在每个Transformer块后插入单线性层，初始化为恒等映射，与注意力参数联合微调。
- **MoAE路由与专家**：由线性路由器和MLP专家组成，支持相机控制（7或12维向量）、机器人动作（7维向量）和导航命令（离散键盘鼠标输入）。
- **Flow Transformer (DiT)**：基于Wan-2.1的30层流Transformer骨干，冻结除自注意力层外的所有参数。



## 实验与关键发现

### 6.1 主要定量结果

**Table 2**: Quantitative comparison of different models. Astra demonstrates superior visual quality and instruction-following performance across a variety of real-world scenarios.

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_8UZpmrxoLG_Astra_General/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison of different models. Astra demonstrates superior visual quality and instruction-following performance across a variety of real-world scenarios.*

| 指标 | Astra | Wan-2.1 | Matrix-Game | YUME |
|------|-------|---------|-------------|------|
| Instruction Following ↑ | **0.669** | 0.084 | 0.247 | 0.619 |
| Subject Consistency ↑ | **0.939** | 0.827 | 0.923 | 0.933 |
| Background Consistency ↑ | **0.945** | 0.843 | 0.939 | 0.927 |
| Motion Smoothness ↑ | **0.989** | 0.913 | 0.946 | 0.972 |
| Aesthetic Quality ↑ | **0.531** | 0.417 | 0.426 | 0.511 |
| Imaging Quality ↑ | **0.747** | 0.632 | 0.653 | 0.628 |

### 6.2 消融实验

**Table 3**: Ablation studies. We assess the contribution of each component in Astra, ensuring all experiments are conducted using the same random seed for fair comparison.

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_8UZpmrxoLG_Astra_General/figures/014_Table_3.jpg]]
*Table 3: Ablation studies. We assess the contribution of each component in Astra, ensuring all experiments are conducted using the same random seed for fair comparison.*

| 配置 | Instruction Following ↑ | Subject Consistency ↑ | Background Consistency ↑ | Motion Smoothness ↑ | Aesthetic Quality ↑ | Imaging Quality ↑ |
|------|------------------------|----------------------|------------------------|--------------------|--------------------|------------------|
| Astra (完整) | **0.669** | **0.939** | 0.945 | **0.989** | **0.531** | **0.747** |
| w/o AFG | 0.545 | 0.931 | 0.944 | 0.987 | 0.492 | 0.742 |
| w/o noise | 0.359 | 0.922 | **0.927** | 0.985 | 0.501 | 0.740 |
| Cross-attention | 0.642 | 0.935 | 0.943 | 0.988 | 0.523 | 0.744 |
| w/o MoAE | 0.651 | 0.937 | 0.944 | 0.988 | 0.527 | 0.745 |

关键发现：
- 去除噪声记忆（w/o noise）后指令跟随分数从0.669降至0.359，验证了噪声记忆对动作响应性的关键作用。
- 去除动作自由引导（w/o AFG）后指令跟随降至0.545，美学质量降至0.492。
- 使用交叉注意力适配器替代ACT-Adapter后指令跟随为0.642，低于Astra的0.669。
- 去除MoAE后指令跟随为0.651，低于Astra的0.669。

### 6.3 CityWalker数据集结果

**Table D**: Quantitative comparison on CityWalker dataset. Astra consistently achieves higher visual quality and more reliable action following when evaluated on fully unseen scenes.

| 指标 | Astra | Wan-2.1 | Matrix-Game | YUME |
|------|-------|---------|-------------|------|
| Instruction Following ↑ | **0.641** | 0.084 | 0.247 | 0.619 |
| Subject Consistency ↑ | **0.948** | 0.827 | 0.923 | 0.933 |
| Background Consistency ↑ | **0.944** | 0.843 | 0.939 | 0.927 |
| Motion Smoothness ↑ | **0.983** | 0.913 | 0.946 | 0.972 |
| Aesthetic Quality ↑ | **0.554** | 0.417 | 0.426 | 0.511 |
| Imaging Quality ↑ | **0.695** | 0.632 | 0.653 | 0.628 |

### 6.4 动作对齐定量比较

**Table A**: Quantitative action-alignment comparison. We complement the human-rated instruction-following metric by reporting rotation and translation errors that directly measure how well generated camera motions align with the commanded actions.

Astra在旋转误差（1.23）和平移误差（4.86）上均优于所有基线方法。

### 6.5 参数效率

**Table B**: Parameter comparison. Astra introduces the smallest parameter overhead among all methods, adding only lightweight adapters while preserving the efficiency of the frozen backbone.

Astra仅需366.8M可训练参数，是所有比较方法中最少的。

### 6.6 定性结果

**Figure 5**: Qualitative results on action-driven real-world exploration. Starting from a single initial frame, our model generates long-term exploration videos with high visual fidelity, smooth and coherent dynamics, and precise responsiveness to action inputs.

**Figure 6**: Qualitative comparisons on action-driven real-world exploration. Given the initial image and action sequence, Astra generates exploration sequences that maintain strong visual fidelity, coherent dynamics, and accurate responsiveness to user-specified actions.

**Figure 7**: Extended applications of Astra. Our framework handles diverse scenarios: (a) autonomous driving, predicting long-horizon traffic dynamics from control inputs; (b) manipulation, conditioning robot actions on object interactions; and (c) camera control, reflecting viewpoint changes in coherent videos. These demonstrate Astra’s versatility for interactive world modeling.

**Figure 8**: Multi-agent interaction of Astra. Given a specified action sequence, Astra generates smooth, realistic multi-agent interactions, such as an ego-vehicle overtaking other cars.

### 6.7 域外泛化

**Figure A**: Out-of-domain generation results of Astra. Astra generalizes to scenes not seen during training, including indoor environments, Minecraft worlds, and animation-style scenes, producing coherent futures that follow camera or navigation commands. The last two rows show two distinct complex action sequences executed within the same scene.

### 6.8 视觉惯性现象

**Figure C**: Effect of visual inertia. As the history length increases, video quality improves, but the action-following score drops sharply, illustrating the visual inertia phenomenon.

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_8UZpmrxoLG_Astra_General/figures/006_Table_1.jpg]]
*Table 1: Datasets used in experiments, along with their actions and sample sizes. For each dataset, we list the action type, followed by the dimensionality of its representation.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_8UZpmrxoLG_Astra_General/figures/021_Table_4.jpg]]
*Table 4: Table A: Quantitative action-alignment comparison. We complement the human-rated instruction-following metric by reporting rotation and translation errors that directly measure how well generated camera motions align with the commanded actions.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_8UZpmrxoLG_Astra_General/figures/022_Table_5.jpg]]
*Table 5: Table B: Parameter comparison. Astra introduces the smallest parameter overhead among all methods, adding only lightweight adapters while preserving the efficiency of the frozen backbone.*



## 定位与知识库关联

Astra 属于交互式世界模型（Interactive World Model）这一新兴研究方向，其方法谱系可定位如下：

- **基础架构**：基于预训练视频扩散模型（Wan-2.1），采用自回归去噪框架，结合了自回归的长时建模能力和扩散的高保真合成能力。
- **动作注入方式**：区别于Matrix-Game的交叉注意力适配器和YUME的掩码视频扩散Transformer，Astra采用ACT-Adapter通过逐元素加法将动作特征直接注入潜空间，实现更细粒度的动作偏移建模。
- **历史条件处理**：创新性地提出噪声增强历史记忆（noise-as-mask）策略，解决了现有方法中视觉惯性导致动作响应不足的问题。
- **异构动作处理**：MoAE模块使Astra能够统一处理相机位姿、机器人动作、键盘鼠标等多种动作模态，而现有方法通常局限于单一模态。
- **参数效率**：Astra仅需366.8M可训练参数，远少于Matrix-Game（1.2B）和YUME（1.5B），实现了高效的动作条件生成。

**Table C**: Comparative overview of various world model methods, detailing their respective domains of application, supported control modalities, and interaction horizons.

Astra在探索、机器人操作、自动驾驶和相机控制等多个领域均展现出优越性能，支持8-10秒的交互时长，并通过噪声记忆和输入打包技术（Zhang & Agrawala, 2025）实现了长时预测的一致性。



## 原文 PDF

![[paperPDFs/ICLR_2026/Astra_General_Interactive_World_Model_with_Autoregressive_Denoising.pdf]]
