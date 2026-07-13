---
title: "VideoControlNet: A Motion-Guided Video-to-Video Translation Framework by Using Diffusion Model with ControlNet"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/VideoControlNet_A_Motion_Guided_Video_to_Video_Translation_Framework_by_Using_Diffusion_Model_with_ControlNet.pdf
project_link: null
code_link: null
aliases:
- VideoControlNet
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/benchmarks_datasets_evaluation
core_operator: 引入输入视频的运动信息（光流）作为引导，结合遮挡感知的局部修复，使生成过程沿时间轴保持结构一致性。
primary_logic: 借鉴视频编码中利用运动补偿降低时间冗余的思想，将生成过程分解为I帧、P帧和B帧的GOP结构：I帧由ControlNet独立生成，P帧通过运动补偿与修复仅生成新出现区域，B帧由相邻关键帧插值得到，从而在保留预训练扩散模型生成能力的同时实现连续、一致的视频转换。
claims:
- 引入运动信息可有效防止冗余区域再生，保持内容一致性。
- 在用户偏好研究中，VideoControlNet获得74.7%的偏好率，远超Text2Video-Zero的9.4%和CCPL的15.8%。
- 在DAVIS数据集上，VideoControlNet在FVD、IS、FID、CLIPSIM、LPIPS、光流误差和速度等指标上均优于Text2Video-Zero。
- 同时使用残差图和遮挡图生成修复掩膜至关重要，仅用残差信息不可靠（如图7所示）。
---

# VideoControlNet: A Motion-Guided Video-to-Video Translation Framework by Using Diffusion Model with ControlNet

> [!tip] 核心洞察
> 借鉴视频编码中利用运动补偿降低时间冗余的思想，将生成过程分解为I帧、P帧和B帧的GOP结构：I帧由ControlNet独立生成，P帧通过运动补偿与修复仅生成新出现区域，B帧由相邻关键帧插值得到，从而在保留预训练扩散模型生成能力的同时实现连续、一致的视频转换。

| 字段 | 内容 |
|------|------|
| 中文题名 | VideoControlNet：一种基于扩散模型与ControlNet的运动引导视频到视频转换框架 |
| 英文题名 | VideoControlNet: A Motion-Guided Video-to-Video Translation Framework by Using Diffusion Model with ControlNet |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2307.14073) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/benchmarks_datasets_evaluation |
| Method | VideoControlNet |
| Dataset | User Study, DAVIS |

> [!tip] 效果简介
> - User Study 上，Preference (%) 74.7% vs CCPL 15.8%, Text2Video-Zero 9.4% (+58.9% vs CCPL, +65.3% vs Text2Video-Zero)。
> - DAVIS (运行效率) 上，平均每帧时间 3.4s vs N/A (未直接比较) (N/A)。

## 概要

### 问题瓶颈

扩散模型在视频生成任务中展现出强大的单帧生成能力，但将其直接应用于视频到视频的转换时面临一个核心瓶颈：**逐帧独立生成导致相邻帧内容不一致**。扩散过程的随机性使得即使输入帧高度相似，输出帧之间也会出现纹理闪烁、结构漂移等问题，尤其在运动区域和遮挡区域表现尤为突出。这一问题的本质在于，逐帧生成范式完全忽略了视频序列中固有的时间冗余信息。

### 核心思路

VideoControlNet 的核心洞察在于**借鉴视频编码中利用运动补偿降低时间冗余的思想**，将生成过程分解为类似 GOP（Group of Pictures）的 I/P/B 帧结构：

- **I帧**：首帧由 ControlNet 独立生成，作为整个序列的锚点。
- **P帧**：通过运动引导的 P 帧生成模块（MgPG），利用前帧的光流进行运动补偿，仅对遮挡和新出现区域进行扩散修复，避免冗余区域再生。
- **B帧**：通过运动引导的 B 帧插值模块（MgBI），利用最近两个 I/P 参考帧和光流直接插值生成。

这一设计使得生成过程沿时间轴保持结构一致性，同时保留了预训练扩散模型的生成能力。

### 方法定位

在方法谱系中，VideoControlNet 处于**基于扩散模型的视频编辑与转换**方向，与以下工作形成对比：

- **Text2Video-Zero**（Khachatryan et al., 2023）：零样本文本到视频生成，依赖跨帧注意力机制保持一致性，但缺乏显式运动引导。
- **CCPL**（Wu et al., ECCV 2022）：基于对比一致性保持损失的视频风格迁移，但未利用运动信息进行帧间补偿。
- **Text2LIVE**：文本驱动的分层视频编辑，在定性对比中作为参考。

VideoControlNet 的关键区别在于引入了**显式的运动信息（光流）作为引导**，并设计了**遮挡感知的局部修复机制**，从而在生成质量与时间一致性之间取得平衡。

### 主要结果

- **用户偏好**：在用户研究中，VideoControlNet 获得 **74.7%** 的偏好率，远超 Text2Video-Zero 的 9.4% 和 CCPL 的 15.8%（Table 1）。
- **定量指标**：在 DAVIS 数据集上，VideoControlNet 在 FVD、IS、FID、CLIPSIM、LPIPS、光流误差等指标上均优于 Text2Video-Zero（Table 2）。
- **修复掩膜有效性**：消融实验表明，同时使用残差图和遮挡图生成修复掩膜至关重要，仅依赖残差信息会遗漏部分遮挡区域（Figure 7）。
- **运行效率**：在 20 步采样的 Stable Diffusion 配置下，平均每帧生成时间约 **3.4 秒**（约 0.30 fps），其中 I 帧、P 帧、B 帧的生成时间各有差异（Table 3）。

### 局限性

- 生成速度较慢，难以满足实时应用需求。
- 方法严重依赖光流估计的准确性，在快速运动或严重遮挡场景下可能失效。
- 当前仅支持 canny edge 和 depth map 作为控制条件，未利用分割图、人体姿态等更丰富的条件。
- 内容一致性仍有提升空间，未来可引入更多可学习网络模块。

扩散模型在图像生成领域取得了显著成功，但在视频生成任务中面临一个核心瓶颈：**逐帧独立生成时，扩散过程的随机性导致相邻帧之间内容不一致**，尤其在运动剧烈和遮挡区域，生成的视频会出现闪烁、抖动或纹理漂移等现象。这一问题的本质在于，扩散模型在去噪过程中缺乏对时间维度结构信息的显式建模。

现有方法尝试从不同角度缓解这一问题。**Text2Video-Zero**（Khachatryan et al., 2023）采用零样本方式，利用文本到图像的扩散模型生成视频，但未充分挖掘输入视频中已有的运动信息，导致帧间连续性不足。**CCPL**（Wu et al., ECCV 2022）通过对比一致性保持损失实现视频风格迁移，但其范式仍倾向于全局约束，难以精细处理局部运动与遮挡场景。

本文的核心动机来源于视频编码领域的一个经典观察：**视频序列中存在大量时间冗余，利用运动补偿可以有效减少冗余信息的重复编码**。受此启发，VideoControlNet 提出将视频编码中的 GOP（Group of Pictures）结构引入扩散生成过程——将视频帧分为 I 帧、P 帧和 B 帧，分别采用不同的生成策略。I 帧由 ControlNet 独立生成，P 帧通过运动补偿与局部修复仅生成新出现区域，B 帧则由相邻关键帧插值得到。这一设计使得生成过程能够“借用”输入视频的运动信息来引导扩散，从而在保留预训练扩散模型生成能力的同时，实现时间轴上连续且一致的视频转换。

## 核心方法与创新机理

### 问题瓶颈与设计动机

扩散模型在逐帧生成视频时面临一个根本性瓶颈：**扩散过程的随机性不可控，导致相邻帧之间内容不一致**，尤其在运动剧烈和遮挡区域表现尤为突出。直接对每帧独立调用 ControlNet 会“重新发明”已在参考帧中出现的冗余区域，破坏时序连贯性。

VideoControlNet 的核心洞察来自视频编码领域的经典思想——**利用运动补偿降低时间冗余**。与其让扩散模型为每一帧从零生成全部内容，不如借助输入视频的运动信息（光流）将已生成帧的内容“搬运”到新帧位置，仅对运动暴露出的新区域（遮挡区域）进行扩散修复。

### 生成范式的根本转变：从逐帧独立到 GOP 分级生成

与逐帧独立生成的 baseline 方法（如 **Text2Video-Zero**，Khachatryan et al., 2023）相比，VideoControlNet 将生成过程重构为视频编码中经典的 **I/P/B 帧图像组（GOP）结构**：

| 生成范式 | Baseline（逐帧独立） | VideoControlNet（GOP 分级） |
|---------|---------------------|---------------------------|
| **首帧（I 帧）** | 与普通帧无区别 | ControlNet 独立生成，作为后续帧的参考锚点 |
| **关键帧（P 帧）** | 全帧扩散生成 | 运动补偿 + 仅修复遮挡区域 |
| **中间帧（B 帧）** | 不存在此概念 | 由相邻两个 I/P 帧通过光流插值直接合成 |

这一范式转变的关键因果机制在于：**将扩散模型的生成能力聚焦于“新出现内容”而非“全部内容”**，从而在保留预训练扩散模型生成质量的同时，天然保证已存在区域的时序一致性。

### 三个关键模块的创新设计

**1. 运动引导的 P 帧生成（MgPG）**

P 帧生成不再从噪声开始全帧扩散，而是采用“运动补偿 + 局部修复”策略：
- 利用前一参考帧和光流进行后向变形（backward warping），得到初步的变形帧；
- 仅对变形帧中无法从参考帧获取的遮挡区域进行扩散修复，其余区域直接复用变形结果。

这使得 P 帧中大部分像素直接继承自参考帧，只有新暴露的区域才触发扩散模型，从根本上消除了冗余区域的再生风险。

**2. 修复掩膜的双信息融合机制**

修复掩膜的生成是 MgPG 的关键——它决定了哪些区域需要扩散修复。与仅依赖残差图的简单方案不同，VideoControlNet 同时利用两种互补信息：

- **遮挡图** $O_i$：通过前向光流将全 1 图变形得到，零值区域表示当前帧中参考帧未出现的新区域；
- **残差图** $R_i$：变形帧与真实帧之间的差异。

最终掩膜通过阈值化公式生成：

$$I_{i,k} = \begin{cases} 1 & \text{if } O_{i,k} - \alpha R_{i,k} > threshold \\ 0 & \text{otherwise} \end{cases}$$

消融实验（Figure 7）明确表明，**仅使用残差信息不可靠**，会遗漏部分遮挡区域；同时引入遮挡图才能生成完整的修复掩膜，确保新区域被充分覆盖。

**3. 运动引导的 B 帧插值（MgBI）**

B 帧生成完全绕开扩散模型，利用最近两个 I/P 参考帧和双向光流直接插值合成。具体而言：
- 分别从前向和后向参考帧进行变形，得到两个候选帧；
- 基于遮挡图和残差图计算每个像素位置的前/后向匹配得分，通过带温度系数 $\tau$ 的 softmax 归一化：

$$S_{j,k}^{front} = \frac{\exp(\hat{S}_{j,k}^{front}/\tau)}{\exp(\hat{S}_{j,k}^{front}/\tau) + \exp(\hat{S}_{j,k}^{back}/\tau)}$$

- 最终 B 帧由两个变形参考帧按匹配得分加权求和得到：

$$\hat{X}_j = S_j^{front} \times \bar{X}_j^{front} + S_j^{back} \times \bar{X}_j^{back}$$

MgBI 的设计使得大部分中间帧无需调用扩散模型，显著降低计算开销，同时保持了与参考帧的运动连续性。

### 光流估计器的选择升级

在光流估计环节，VideoControlNet 采用了更通用的 **FlowFormer** 网络，而非视频编码中常用的 SpyNet。这一选择使得光流估计能更好地适应自然视频中多样化的运动模式，为后续的运动补偿和遮挡检测提供更可靠的基础。

### 创新点的协同效果

上述三个模块的协同作用体现在：**I 帧提供内容锚点，P 帧在保持内容一致性的前提下推进叙事，B 帧以极低成本填充中间过渡**。这种分层策略使得 VideoControlNet 在用户偏好研究中获得了 **74.7%** 的偏好率，远超 Text2Video-Zero 的 9.4% 和 **CCPL**（Wu et al., ECCV 2022）的 15.8%（Table 1），验证了运动引导的 GOP 生成范式在视频到视频转换任务中的有效性。

VideoControlNet 的整体生成范式借鉴了视频编码中 **I/P/B 帧结构** 的设计思想，将视频到视频的转换过程分解为三个层次化的生成阶段，从而在保留预训练扩散模型生成能力的同时，实现对时间轴上内容一致性的有效控制。

### 核心设计动机

扩散模型在逐帧独立生成时，扩散过程不可控，导致相邻帧内容不一致，这一问题在运动与遮挡区域尤为突出。VideoControlNet 的核心洞察在于：**利用输入视频的运动信息（光流）作为引导，避免对冗余区域的重复生成，仅对因运动遮挡而新出现的区域进行修复**。通过这种方式，生成过程沿时间轴保持了结构一致性，同时最大限度地复用了 ControlNet 的生成质量。

### 三层生成架构

框架将视频帧划分为三种角色，对应不同的生成策略：

1. **I 帧生成**：以输入视频的首帧作为 I 帧，直接使用 ControlNet 独立生成。条件信息（如 canny 边缘图或深度图）从输入 I 帧中提取，作为扩散模型的控制输入。I 帧是整个生成过程的锚点，后续所有帧均以此为参考。

2. **运动引导的 P 帧生成（MgPG）**：将后续帧划分为若干图像组（Group of Pictures, GoP），每个 GoP 的最后一帧被指定为 P 帧。MgPG 模块首先利用前一个参考帧（I 帧或前一 P 帧）的光流进行后向扭曲（backward warping），得到运动补偿后的扭曲帧；随后，通过结合前向光流生成的**遮挡图**和扭曲帧与真实帧之间的**残差图**，计算出需要修复的区域掩膜；最后，仅对这些新出现的遮挡区域进行扩散修复，而非全帧重新生成。这一机制有效防止了冗余区域的再生。

3. **运动引导的 B 帧插值（MgBI）**：GoP 中位于两个参考帧（I/P 帧）之间的其余帧被设置为 B 帧。MgBI 模块利用最近的两个参考帧及其光流信息，分别进行前向和后向扭曲，并通过基于遮挡图和残差图的匹配得分（经 softmax 归一化）对两个扭曲帧进行加权融合，直接插值生成 B 帧。B 帧无需调用扩散模型，大幅降低了计算开销。

### 关键子模块：修复掩膜生成

修复掩膜的质量直接影响 P 帧生成的效果。VideoControlNet 的掩膜生成策略结合了两种互补信息：

- **遮挡图** $O_i$：通过对全 1 图施加前向光流 $M_{i \to i-g}$ 的前向扭曲操作得到，零值区域表示当前帧中在参考帧内不可见的遮挡区域。
- **残差图** $R_i$：表示扭曲帧与真实帧之间的差异。

最终的修复掩膜 $I_i$ 由以下阈值公式生成：

$$I_{i,k} = \begin{cases} 1 & \text{if } O_{i,k} - \alpha R_{i,k} > threshold \\ 0 & \text{otherwise} \end{cases}$$

其中 $\alpha$ 和 $threshold$ 为控制修复范围的超参数。消融实验表明，仅使用残差信息生成的掩膜不可靠，会遗漏部分遮挡区域；同时利用遮挡图可明显改善掩膜质量，实现更完整的新区域修复。

### 输入输出流

整个框架的输入为一段视频及其对应的文本提示词，输出为风格化或编辑后的视频。流程如下：

1. 从输入视频提取条件信息（canny 边缘图或深度图）和帧间光流（使用 FlowFormer 估计）。
2. 首帧作为 I 帧，通过 ControlNet 独立生成。
3. 按 GoP 结构依次处理：对每个 GoP 的 P 帧执行 MgPG，对中间的 B 帧执行 MgBI。
4. 所有生成帧按时间顺序拼接，得到最终输出视频。

框架的整体流程可参考 **图 2**，MgPG 模块的细节见 **图 3**，MgBI 模块的细节见 **图 4**。

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2307_14073/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed motion-guided video-to-video translation framework. (a) The generation process of I-frame: Taking the first input frame*

VideoControlNet 的核心创新在于将视频编码中的运动补偿思想引入扩散模型的生成过程，构建了一个基于 GOP（Group of Pictures）结构的分级生成框架。整个流程围绕三个关键模块展开：I 帧生成、运动引导的 P 帧生成（MgPG）和运动引导的 B 帧插值（MgBI）。

### I 帧生成

I 帧作为整个 GOP 的锚点，由扩散模型独立生成。具体而言，从输入视频的首帧提取条件（如 Canny 边缘图或深度图），将其输入 ControlNet 引导 Stable Diffusion 生成对应的输出帧。该过程不涉及运动信息，仅依赖预训练扩散模型的生成能力来建立首帧的内容与风格。

### 运动引导的 P 帧生成（MgPG）

MgPG 模块的目标是基于已生成的参考帧（I 帧或前一个 P 帧）生成当前 P 帧，同时避免对冗余区域进行重复生成。其核心流程分为两步：

**步骤一：运动补偿。** 给定已生成的参考帧 $\hat{X}_{i-g}$ 和从输入视频中提取的光流 $M_{i-g \to i}$，通过后向变形（backward warping）操作将参考帧对齐到当前帧位置，得到变形帧 $\bar{X}_i$。变形帧中大部分区域与目标帧结构一致，但遮挡区域（即参考帧中不可见、当前帧中新出现的区域）会存在空洞或错位。

**步骤二：遮挡感知的局部修复。** 为了仅对遮挡区域进行扩散修复，需要生成精确的修复掩膜。掩膜生成综合考虑两个信息源：

1. **遮挡图 $O_i$**：通过对全 1 图施加前向变形操作得到，公式为：

$$O_i = \text{ForwardWarp}(\text{Ones}, M_{i \to i-g})$$

其中 $M_{i \to i-g}$ 为前向光流。变形后，遮挡图中值为 0 的区域即表示当前帧中参考帧未覆盖的新出现区域。

2. **残差图 $R_i$**：变形帧与真实当前帧之间的差异，反映运动补偿后的剩余误差。

最终的修复掩膜 $I_i$ 通过阈值化操作融合两者信息：

$$I_{i,k} = \begin{cases} 1 & \text{if } O_{i,k} - \alpha R_{i,k} > threshold \\ 0 & \text{otherwise} \end{cases}$$

其中 $\alpha$ 和 $threshold$ 为超参数，控制修复范围的敏感度。该设计的必要性在消融实验中得到验证：仅使用残差图生成的掩膜不可靠，会遗漏部分遮挡区域；同时引入遮挡图能显著改善掩膜质量（见 Figure 7 的可视化对比）。

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2307_14073/figures/009_Figure_7.jpg]]
*Figure 7: Visualization of our inpainting mask generation during our motion-guided P-frame generation (MgPG). (a) is the residual map that represents the difference between the warped frame and the ground truth frame. (b) is the ground truth of the current frame. (c) is the occlusion map calculated by using the forward warping operation. (d) is the wrapped frame by using the backward warping operation based on the reference frame. (e) is the inpainting mask calculated based on the residual map and the occlusion map. (f) is our warped frame with the inpainting mask*

获得修复掩膜后，将其应用于变形帧，仅对掩膜标记的区域调用 Stable Diffusion with ControlNet 进行扩散修复，其余区域直接复用变形帧的像素值。这一策略从机制上防止了冗余区域的再生，是保持帧间内容一致性的关键。

### 运动引导的 B 帧插值（MgBI）

B 帧位于两个参考帧（I 帧或 P 帧）之间，MgBI 模块通过插值方式生成，无需再次调用扩散模型，从而大幅提升效率。给定前向参考帧 $\hat{X}_{i-g}$ 和后向参考帧 $\hat{X}_i$，以及对应的光流信息，流程如下：

首先，分别将两个参考帧变形到目标 B 帧位置，得到前向变形帧 $\bar{X}_j^{front}$ 和后向变形帧 $\bar{X}_j^{back}$。然后，为每个像素位置计算两个变形帧的匹配得分。以前向得分为例，原始匹配得分定义为：

$$\hat{S}_{j,k}^{front} = O_{j,k}^{front} - \beta R_{j}^{front}$$

其中 $O_{j,k}^{front}$ 为前向变形产生的遮挡图，$R_{j}^{front}$ 为对应的残差图，$\beta$ 为加权超参数。后向得分 $\bar{S}_{j,k}^{back}$ 同理计算。随后通过带温度系数 $\tau$ 的 softmax 进行归一化：

$$S_{j,k}^{front} = \frac{\exp(\hat{S}_{j,k}^{front}/\tau)}{\exp(\hat{S}_{j,k}^{front}/\tau) + \exp(\bar{S}_{j,k}^{back}/\tau)}$$

最终 B 帧由两个变形帧按匹配得分加权求和得到：

$$\hat{X}_j = S_j^{front} \times \bar{X}_j^{front} + S_j^{back} \times \bar{X}_j^{back}$$

该插值策略使得 B 帧能够自适应地融合前后参考帧的信息：在非遮挡区域，匹配得分高的参考帧贡献更大；在仅单侧可见的遮挡区域，则主要依赖可见侧的参考帧。

### 模块间的协同与效率

三个模块的分工体现了“好钢用在刀刃上”的设计哲学：I 帧承担最重的全帧扩散生成（约 13.7 秒/帧），P 帧仅对遮挡区域进行局部修复（同样约 13.7 秒，但修复面积远小于全帧），B 帧则完全通过光流插值完成（仅需约 0.2 秒/帧）。当 GOP 大小设为 10 时，平均每帧生成时间约 3.4 秒（约 0.30 fps），其中扩散模型的采样步数为 20 步。此外，在将掩膜应用于潜在空间时，还引入了高斯模糊和最小池化操作以扩展修复区域，确保潜在空间中的修复边界平滑过渡。

## 实验与关键发现

VideoControlNet 的实验评估围绕三个维度展开：用户偏好研究、DAVIS 数据集上的定量指标对比，以及各模块的运行效率分析。此外，消融实验揭示了修复掩膜生成策略的关键作用，定性结果展示了不同控制条件的生成效果。

### 用户偏好研究

为评估生成视频的主观质量，作者进行了用户偏好调查，将 VideoControlNet 与 **Text2Video-Zero**（Khachatryan et al., 2023）和 **CCPL**（Wu et al., ECCV 2022）进行对比。如表 1 所示，VideoControlNet 获得了 **74.7%** 的偏好率，远超 CCPL 的 15.8% 和 Text2Video-Zero 的 9.4%（置信度 0.98）。这一结果直接验证了运动引导的 GOP 生成范式在保持时间一致性和内容连贯性方面的优势——用户明显更倾向于 VideoControlNet 生成的连续、稳定的视频输出。

### DAVIS 数据集定量评估

在 DAVIS 数据集上，VideoControlNet 与 Text2Video-Zero 进行了全面的定量对比，涵盖视频质量、内容一致性和运动保真度等多个指标。如表 2 所示，VideoControlNet 在 **FVD**（981.99）、**IS**、**FID**、**CLIPSIM**、**LPIPS**、光流误差和生成速度等指标上均优于 Text2Video-Zero（置信度 0.9）。这一结果说明，通过运动补偿和局部修复避免冗余区域再生，不仅提升了帧间一致性，还改善了整体视频质量。需要指出的是，原文未提供与 CCPL 在 DAVIS 上的定量对比数据，该比较仅存在于用户偏好研究中。

### 运行效率分析

表 3 给出了各模块的运行时间分解。在 GoP 大小设为 10、Stable Diffusion 采样步数为 20 的设置下，**I 帧生成**和 P 帧的遮挡区域修复各需约 **13.7 秒**（即 Stable Diffusion with ControlNet 的推理时间），而 B 帧插值仅需约 0.07 秒。得益于 B 帧的高效插值，**平均每帧生成时间约为 3.4 秒**（约 0.30 fps）。这一速度虽然远不能满足实时应用需求（作者在局限性中明确指出），但相比于逐帧全图扩散的方案已大幅降低计算开销——B 帧插值几乎不消耗扩散模型的推理时间。

### 修复掩膜消融实验

修复掩膜的质量直接影响 P 帧中新出现区域的生成完整性。消融实验（Section 4.4 及 Figure 7）表明，**仅使用残差图生成的修复掩膜会遗漏部分遮挡区域**，导致新区域修复不完整；同时利用遮挡图（通过前向光流变形生成）与残差图的阈值掩膜（公式 $I_{i,k} = \begin{cases} 1 & \text{if } O_{i,k} - \alpha R_{i,k} > threshold \\ 0 & \text{otherwise} \end{cases}$）可明显改善掩膜质量，使新出现区域得到更完整的修复（置信度 0.9）。Figure 7 直观展示了残差图、遮挡图、最终掩膜及带掩膜的变形帧之间的差异，验证了双信息源融合的必要性。

### 控制条件的定性对比

Figure 6 展示了使用不同 ControlNet 条件（深度图与 canny 边缘图）的生成结果对比。深度图条件倾向于保留更多的几何结构信息，而 canny 图条件则更注重边缘轮廓的保持，生成风格存在明显差异（置信度 0.85）。这为用户提供了可控性——可根据应用场景选择最合适的控制条件。但当前方法仅支持这两种条件，尚未利用分割图、人体姿态等更丰富的控制信息，这是作者列出的主要局限性之一。

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2307_14073/figures/007_Figure_6.jpg]]
*Figure 6: Generated results when using different conditions. The input videos are provided in the first row. The sentence below the input video is the input prompt of the StableDiffusion. The last two rows are the generated results, in which the middle row is the results when using the ControlNet with the depth map condition, and the last row contains the results when using the ControlNet with the canny map condition*

### 失败模式与局限性

综合原文讨论，VideoControlNet 的主要失败模式和局限包括：

1. **内容一致性仍有提升空间**：尽管运动引导机制显著改善了帧间一致性，但在快速运动或复杂遮挡场景下仍可能出现不一致，作者建议未来引入更多可学习网络模块来增强一致性。
2. **严重依赖光流估计精度**：MgPG 和 MgBI 模块均以光流为运动信息基础，当光流估计不准确时（如快速运动、严重遮挡），运动补偿和 B 帧插值的质量会显著下降。
3. **生成速度较慢**：约 0.30 fps 的生成速度难以满足实时应用需求，主要瓶颈在于扩散模型的多次推理。
4. **控制条件有限**：当前仅支持 canny edge 和 depth map 两种条件，限制了在更复杂编辑任务中的应用。

> **注意**：以上局限性分析基于原文明确列出的内容。关于在更极端场景（如剧烈相机运动、长序列生成）下的具体失效表现，原文未提供系统性的失败案例研究，需要进一步实验验证。

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2307_14073/figures/006_Table_1.jpg]]
*Table 1: User preference of Text2Video-Zero [16], CCPL [43] and our proposed method*

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2307_14073/figures/008_Table_2.jpg]]
*Table 2: Quantitative results on the DAVIS dataset [27]*

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2307_14073/figures/010_Table_3.jpg]]
*Table 3: Running Time of different modules in which we use 20 sampling steps for the StableDiffusion with ControlNet. “Pixel to Latent" denotes encoding the image to latent space for the diffusion networks. “Latent to Pixel" denotes decoding the image from latent space. We also provide the inference time of I-frame generation, P-frame generation and B-frame generation. The average time is calculated when the GoP size is set as 10*

## 定位与知识库关联

### 核心范式：从逐帧独立生成到运动补偿的GOP结构生成

VideoControlNet的核心创新在于将扩散模型的视频生成从“逐帧独立生成”范式升级为“运动补偿的GOP结构生成”范式。传统基于扩散模型的视频生成方法（如**Text2Video-Zero** (Khachatryan et al., arXiv 2023)）对每一帧独立执行扩散去噪，这导致扩散过程的随机性在相邻帧之间产生不可控的内容偏移，尤其在运动区域和遮挡区域表现明显。VideoControlNet借鉴视频编码中利用运动补偿降低时间冗余的思想，将生成过程分解为I帧、P帧和B帧的分级结构：I帧由ControlNet独立生成，P帧通过运动补偿与修复仅生成新出现区域，B帧由相邻关键帧插值得到。

这一范式转换的关键因果机制在于：**运动信息（光流）的引入使生成过程从“全帧重绘”变为“局部修复”**。具体而言，对于P帧，方法首先利用前帧生成的光流对参考帧进行后向扭曲（backward warping），获得与当前帧结构对齐的扭曲帧；然后通过前向扭曲生成遮挡图，结合残差图生成修复掩膜，仅对遮挡区域进行扩散修复。这从根本上避免了冗余区域的再生，从而在保留预训练扩散模型生成能力的同时实现时间一致性。

### 与基线方法的差异化定位

**Text2Video-Zero** (Khachatryan et al., arXiv 2023) 是零样本文本到视频生成方法的代表，其核心思路是通过跨帧注意力机制将文本到图像扩散模型适配到视频生成。然而，该方法缺乏对输入视频运动信息的显式利用，生成结果在时间一致性上存在明显不足。VideoControlNet在用户偏好研究中获得74.7%的偏好率，远超Text2Video-Zero的9.4%（Table 1），且在DAVIS数据集上的FVD、IS、FID、CLIPSIM、LPIPS、光流误差和速度等指标上均优于Text2Video-Zero（Table 2）。这一性能差距验证了运动补偿机制在视频到视频转换任务中的关键作用。

**CCPL** (Wu et al., ECCV 2022) 通过对比一致性保持损失实现视频风格迁移，属于基于优化的视频风格迁移方法。与VideoControlNet基于扩散模型的生成范式不同，CCPL依赖预训练的风格迁移网络和专门设计的一致性约束。VideoControlNet在用户偏好率上以74.7%对15.8%大幅领先CCPL，表明基于扩散模型的生成范式在视频转换质量上具有显著优势。

**Text2LIVE** 被用于定性对比（Figure 5），该方法支持文本驱动的分层视频编辑。VideoControlNet在保持内容一致性和编辑质量上展现出更好的视觉效果。

### 方法谱系定位

VideoControlNet处于**扩散模型视频生成**与**视频编码运动补偿**两个技术脉络的交汇点：

1. **扩散模型脉络**：继承ControlNet的条件控制能力，利用预训练的Stable Diffusion作为基础生成器，通过canny edge或depth map等条件图引导生成过程。这使得方法能够利用大规模预训练模型的生成能力，同时保持对输入视频结构的忠实度。

2. **视频编码脉络**：借鉴传统视频编码中的GOP结构和运动补偿思想，将I/P/B帧的生成策略引入扩散模型。这一跨领域迁移的关键在于将视频编码中的“帧间预测+残差编码”转化为“运动扭曲+遮挡修复”。

在技术实现层面，方法选择了**FlowFormer**作为光流估计网络，而非视频编码中常用的SpyNet。FlowFormer作为更通用的光流估计网络，能够提供更准确的前向和后向光流估计，这对于遮挡图的生成和修复掩膜的精度至关重要。

### 适用边界与限制

**条件类型的限制**：当前方法仅支持canny edge和depth map作为ControlNet的控制条件。论文明确指出未利用分割图、人体姿态等更丰富的条件类型，这限制了方法在需要精细语义控制的场景（如人物编辑、场景分割引导生成）中的应用。

**光流依赖的脆弱性**：方法严重依赖光流估计的准确性。在快速运动或严重遮挡场景下，光流估计误差会通过运动补偿和遮挡图生成两个环节级联放大，导致扭曲帧质量下降和修复掩膜不准确。虽然方法通过结合遮挡图和残差图的双重掩膜生成策略（Eq. 2）缓解了这一问题，但本质上仍受限于光流估计的上限性能。

**生成效率瓶颈**：在GoP大小为10的配置下，平均每帧生成时间约为3.4秒（约0.30 fps），难以满足实时应用需求。其中Stable Diffusion with ControlNet的推理耗时13.7秒是主要瓶颈（Table 3）。这一效率限制源于扩散模型本身的多步采样特性，I帧生成和P帧的遮挡区域修复均需执行完整的扩散去噪过程。

**内容一致性的上限**：虽然运动补偿机制有效减少了冗余区域的再生，但论文承认生成视频的内容一致性仍有提升空间。B帧插值虽然避免了扩散去噪，但其基于前后向扭曲帧加权求和的方式（Eq. 6）本质上是一种线性插值，无法处理复杂的非线性运动和非刚体形变。

### 开放问题与未来方向

**可学习模块的引入**：论文提出未来可引入更多可学习网络模块以增强视频内容一致性。这指向了将当前基于规则的修复掩膜生成和B帧插值替换为可学习模块的方向，例如使用轻量级神经网络预测修复区域或执行非线性帧插值。

**条件类型的扩展**：能否将分割图或人体姿态作为额外的控制条件并保持生成质量，是一个值得探索的方向。这涉及到多条件ControlNet的融合策略，以及不同条件类型对时间一致性的影响机制。

**光流估计的替代方案**：是否可以替换为更有效的光流估计网络以提升整体性能？这包括探索最新的光流估计架构，或考虑使用基于特征匹配的运动估计方法以增强对快速运动的鲁棒性。

**分辨率和序列长度的扩展**：方法能否扩展到更高分辨率或更长的视频序列？这涉及到扩散模型在高分辨率下的计算效率问题，以及长序列中误差累积的控制策略。

**局部编辑的精确控制**：如何在保持生成多样性的同时，更好地控制局部编辑的精确度？当前方法通过提示词和条件图控制全局生成，但在需要精确指定编辑区域的场景下（如仅修改视频中特定物体的外观），缺乏细粒度的空间控制机制。

## 原文 PDF

![[paperPDFs/arxiv_2023/VideoControlNet_A_Motion_Guided_Video_to_Video_Translation_Framework_by_Using_Diffusion_Model_with_ControlNet.pdf]]
