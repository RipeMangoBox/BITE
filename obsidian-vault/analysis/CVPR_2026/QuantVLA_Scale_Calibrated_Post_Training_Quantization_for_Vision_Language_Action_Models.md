---
title: "QuantVLA: Scale-Calibrated Post-Training Quantization for Vision-Language-Action Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/QuantVLA_Scale_Calibrated_Post_Training_Quantization_for_Vision_Language_Action_Models.pdf
project_link: null
code_link: null
aliases:
- QuantVLA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "注意力有效温度 $T_{\\text{eff}} = \\sqrt{d} / (s_q s_k)$ 和残差流能量（由 $s_v s_o$ 控制）是决定量化后DiT行为的关键控制变量。"
primary_logic: 通过选择性量化（保持注意力投影为浮点）并结合轻量级的注意力温度匹配（ATM）和输出头平衡（OHB），将校正标量折叠入反量化尺度，无需训练即可消除量化引起的注意力温度与残差能量漂移，首次实现VLA模型整体的稳定低比特推理。
claims:
- QuantVLA在LIBERO基准上超过全精度基线，同时将量化模块内存减少约70%。
- 在OpenPI π0.5上，QuantVLA W4A8平均成功率达97.6%，内存从4.27 GB降至1.28 GB；在GR00T N1.5上平均成功率达88.0%，内存从2.02 GB降至0.91 GB。
- 选择性量化布局使量化LLM + DiT MLP的性能最接近全精度基线，而全量化导致任务成功率严重下降（π0.5上从97.1%降至76.3%）。
- ATM校正logits标准差，OHB校正注意力输出RMS，两者使量化后的统计量回归教师模型，显著减小漂移。
---

# QuantVLA: Scale-Calibrated Post-Training Quantization for Vision-Language-Action Models

> [!tip] 核心洞察
> 通过选择性量化（保持注意力投影为浮点）并结合轻量级的注意力温度匹配（ATM）和输出头平衡（OHB），将校正标量折叠入反量化尺度，无需训练即可消除量化引起的注意力温度与残差能量漂移，首次实现VLA模型整体的稳定低比特推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视觉-语言-动作模型的尺度校准后训练量化 |
| 英文题名 | QuantVLA: Scale-Calibrated Post-Training Quantization for Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20309) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | QuantVLA |
| Dataset | LIBERO, Memory, Pick-and-Can |

> [!tip] 效果简介
> - LIBERO (four suites average) 上，success rate 97.6% (QuantVLA W4A8, π0.5) vs 97.1% (FP16, π0.5) (+0.5%)；success rate 88.0% (QuantVLA W4A8, GR00T N1.5) vs 86.5% (FP16, GR00T N1.5) (+1.5%)。
> - Memory (LLM+DiT) 上，memory usage (GB) 1.28 GB (π0.5), 0.91 GB (GR00T N1.5) vs 4.27 GB (π0.5), 2.02 GB (GR00T N1.5) (~70% relative saving)。
> - LIBERO (π0.5) 上，success rate 97.6% (QuantVLA W4A8, π0.5) vs 76.3% (DuQuant W4A8, π0.5) (+21.3%)。

## 概要

视觉-语言-动作（VLA）模型在机器人操控中展现出强大的泛化能力，但其部署面临严峻的效率瓶颈：语言骨干网络与基于扩散变换器（DiT）的动作头同时带来巨大的计算与内存开销，而现有的高效VLA方法多聚焦于架构裁剪或推理加速，几乎不触及DiT动作头的数值精度优化。

直接对VLA模型进行训练后量化（PTQ）会引发两个系统性的数值漂移——注意力温度漂移与残差流能量偏移——严重破坏低比特推理的稳定性。QuantVLA针对这一核心矛盾，提出了首个面向VLA模型的训练免调后训练量化框架。其核心洞见在于：**注意力投影的量化是漂移的根源，通过选择性保持浮点计算并结合轻量级的尺度校准，即可消除量化引起的分布畸变**。

具体而言，QuantVLA包含三个协同组件：（1）选择性量化布局，将语言骨干网络的全部线性层与DiT的前馈网络进行整数量化，同时保持注意力投影（Q、K、V、O）为浮点；（2）注意力温度匹配（ATM），通过每头标量校正量化后的logits标准差，稳定注意力分布；（3）输出头平衡（OHB），通过每层标量恢复残差流能量。所有校准标量均可折叠入反量化尺度，不引入额外推理开销。

在LIBERO基准上，QuantVLA以W4A8精度在OpenPI π0.5上达到97.6%的平均任务成功率，**超越全精度基线的97.1%**，同时将量化模块的内存占用从4.27 GB降至1.28 GB（约70%相对节省）；在GR00T N1.5上同样以88.0%的成功率超越全精度的86.5%。即使在极端的W4A4精度下，π0.5仍保持95.3%的成功率，展现出对极低位宽的鲁棒性。与现有量化基线相比，QuantVLA在W4A8下较DuQuant提升21.3个百分点，较SmoothQuant在Pick-and-Can任务上多完成11次成功抓取，验证了尺度校准机制在VLA场景下的决定性作用。



### 视觉-语言-动作模型的部署瓶颈

视觉-语言-动作模型（VLA）将大规模语言模型与扩散策略头结合，在机器人操控任务中展现出强大的泛化能力。然而，其部署面临严峻的计算与内存挑战：语言骨干网络（LLM）参数量庞大，而基于扩散变换器（DiT）的动作头在推理时需执行多步去噪，两者叠加导致显存占用和推理延迟成为实际部署的瓶颈。

现有高效VLA方案主要从三个方向切入：（1）**架构压缩**，如TinyVLA通过紧凑多模态变换器和轻量扩散策略头减少参数量；（2）**推理加速**，如EfficientVLA剪枝冗余语言层并复用中间表示，MoLe-VLA采用混合专家层路由动态跳过计算；（3）**缓存优化**，如VLA-Cache通过键值复用和视觉token静态缓存提升吞吐。然而，这些方法要么重新设计模型架构，要么在原有策略外围添加路由与缓存机制，几乎不直接操作DiT动作头的数值精度，未能从根本上降低模型在边缘设备上的存储与计算开销。

### 量化VLA模型的核心困难

后训练量化（PTQ）是一种不改变模型架构、无需重新训练即可压缩模型的成熟技术。然而，将PTQ直接应用于VLA模型面临两个关键障碍：

**注意力温度漂移。** 在DiT动作头中，注意力机制的计算涉及查询（Q）与键（K）的矩阵乘法。量化后，查询和键的反量化尺度 $s_q$ 和 $s_k$ 会改变注意力有效温度 $T_{\text{eff}} = \sqrt{d} / (s_q s_k)$。当 $s_q s_k$ 偏离浮点参考值时，softmax输入logits的尺度发生偏移，导致注意力分布过尖锐或过平坦，破坏动作去噪过程的稳定性。

**残差流能量偏移。** DiT中的残差连接和层归一化对特征能量高度敏感。量化引入的扰动经注意力值通路（由 $s_v$ 控制）和输出投影（由 $s_o$ 控制）传播后，会改变残差流的均方根（RMS）能量，进而干扰后续层的归一化操作和梯度流等效行为，使模型在低比特下迅速退化。

现有量化方法如 **DuQuant**（Lin et al., NeurIPS 2024）和 **SmoothQuant**（Xiao et al., ICML 2023）在纯语言模型上表现良好，但未针对VLA中语言-扩散耦合的特性进行设计。实验表明，将DuQuant的W4A8全量化直接应用于OpenPI π0.5模型，LIBERO平均任务成功率从全精度的97.1%骤降至76.3%（Table 2），充分说明现有PTQ方法无法应对VLA模型的量化挑战。

### 本文动机与核心思路

本文提出QuantVLA，一个无需训练的PTQ框架，首次实现对VLA模型语言骨干和DiT动作头的联合低比特量化。核心洞察在于：量化破坏VLA性能的根本原因不是参数精度损失本身，而是量化引起的**注意力温度**和**残差能量**两个关键尺度的漂移。基于此，QuantVLA采用三项协同设计：

1. **选择性量化布局**：对所有LLM线性层和DiT MLP层进行低比特整型化，但保持DiT的注意力投影（Q、K、V、O）为浮点计算，从源头避免量化对注意力核心计算路径的干扰。
2. **注意力温度匹配（ATM）**：为每个注意力头学习一个标量 $\alpha$，通过匹配教师与量化模型的logits标准差恢复注意力温度，并将该标量折叠入反量化尺度，不引入额外推理开销。
3. **输出头平衡（OHB）**：为每层学习一个标量 $\beta$，通过匹配注意力输出RMS恢复残差流能量，同样折叠入反量化尺度。

该方法保持原始模型架构和算子调度不变，仅需少量未标注校准数据即可完成标定，为VLA模型在资源受限边缘设备上的高效部署提供了可行路径。



## 核心方法与创新机理

QuantVLA 的核心创新在于首次揭示了 VLA 模型量化失败的根本机制，并据此设计了一套无需训练的尺度校准方案，使语言骨干网络与扩散动作头能够协同稳定地运行在低比特精度下。

### 瓶颈定位：注意力温度漂移与残差能量偏移

VLA 模型由语言骨干（LLM）与基于扩散变换器（DiT）的动作头构成，二者的计算与内存开销共同成为部署瓶颈。直接对 DiT 应用现有后训练量化方法会导致任务成功率严重下降——例如在 π0.5 上，全量化 W4A8 的平均成功率从全精度的 97.1% 骤降至 76.3%（Table 1）。QuantVLA 通过一阶扰动分析指出，量化在 DiT 中引入了两类系统性漂移：

- **注意力温度漂移**：查询 $Q$ 与键 $K$ 的量化扰动改变了预 softmax logits 的方差，等效于修改了注意力机制的有效温度 $T_{\text{eff}} = \sqrt{d} / (s_q s_k)$，其中 $s_q$、$s_k$ 为反量化尺度。温度变化直接扭曲 softmax 的锐度，破坏注意力分布。
- **残差能量偏移**：经过多头拼接与输出投影后，量化引起的值通路扰动与输出投影扰动改变了注意力输出的 RMS 能量，进而干扰残差连接和后续层归一化的数值流。

这两类漂移构成了量化后 DiT 行为失稳的因果控制变量，也是 QuantVLA 设计的核心靶点。

### 选择性量化布局

基于上述分析，QuantVLA 提出了差异化的量化策略：将 LLM 的所有线性层与 DiT 的 MLP 层进行低比特整型量化，同时**保持 DiT 的注意力投影 $W_q$、$W_k$、$W_v$、$W_o$ 为浮点计算**（Figure 2）。这一选择性布局直接切断了量化噪声向注意力温度与残差能量这两个敏感控制变量的传播路径。消融实验（Table 1）证实，仅量化 LLM + DiT MLP 的性能最接近全精度基线，而一旦将注意力投影也纳入量化，性能即出现断崖式下降。

### 轻量级尺度校准：ATM 与 OHB

即便采用了选择性量化，DiT MLP 的量化仍会通过残差连接间接影响注意力统计量。为此，QuantVLA 引入两项免训练的校准机制，通过匹配教师模型（全精度）的关键统计量来消除残余漂移：

- **注意力温度匹配（ATM）**：为每个注意力头计算一个标量 $\alpha_{\text{raw}} = \frac{\mathrm{Std}(L_T)}{\mathrm{Std}(L_Q) + 10^{-6}}$，即教师与量化模型预 softmax logits 标准差的比值。该标量经裁剪后折叠入反量化尺度，等效于对量化后的 logits 进行温度校准，使注意力分布回归教师模型的锐度。
- **输出头平衡（OHB）**：为每层计算一个标量 $\beta_{\text{raw}}(l) = \frac{\mathrm{RMS}(Z_{T,l})}{\mathrm{RMS}(Z_{Q,l}) + 10^{-6}}$，即教师与量化模型注意力输出 RMS 的比值。该标量同样经裁剪后折叠入反量化尺度，恢复残差流的能量水平，稳定层归一化的输入分布。

两项校准所需的标量均从小规模无标注校准数据中估计，并在推理时折叠入反量化尺度，不引入额外计算开销。可视化结果（Figure 3）表明，ATM 显著缩小了量化模型与教师模型在注意力 logits 标准差上的差距，OHB 则有效恢复了注意力输出的 RMS，使各层的统计量回归教师水平。

### 方法定位：免训练的尺度感知 PTQ

与现有 VLA 效率方案相比，QuantVLA 的独特之处在于：它既不修改模型架构（区别于 TinyVLA 的紧凑设计），也不引入动态路由或缓存机制（区别于 MoLe-VLA、VLA-Cache），而是**直接在数值精度层面操作，以无训练的后训练量化方式同时压缩语言与动作模块**。相较于通用 PTQ 基线 **DuQuant**（Lin et al., NeurIPS 2024）和 **SmoothQuant**（Xiao et al., ICML 2023），QuantVLA 的关键增量在于对 DiT 注意力机制的因果诊断与针对性尺度恢复，使得 VLA 模型首次在 W4A8 精度下超越全精度基线，并在 W4A4 极端位宽下仍保持可用性能（π0.5 平均成功率 95.3%，Table 3）。



QuantVLA 是一个无需训练的后训练量化框架，面向基于 DiT 动作头的 VLA 模型，保持原始架构与算子调度不变。其整体 pipeline 由三个协同组件构成：**选择性量化布局**、**注意力温度匹配** 和 **输出头平衡**，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/003_Figure_2.jpg]]
*Figure 2: Overview of QuantVLA for VLAs with a DiT-based action head. The framework is training-free and preserves the original architecture and operator schedule. It combines: (1) a selective quantization layout that integerizes all linear layers in the LLM and all MLP layers in the DiT while keeping the attention projections Q, K, V , O in floating point; (2) Attention Temperature Matching (ATM), a per-head scalar α that aligns teacher–student logits and is folded into dequantization scales; and (3) Output Head Balancing (OHB), a per-layer scalar β that matches post-projection energy at the residual interface*

### 输入输出流

VLA 模型的推理流程分为两条通路。视觉编码器接收 RGB 帧，提取视觉特征；语言骨干网络处理自然语言指令，并与视觉 token 融合，生成视觉-语言特征 $F_{\mathrm{VL}}$。该特征随后注入基于扩散变换器的动作头，结合机器人本体感知和扩散时间步 $t$，通过迭代去噪过程更新动作隐变量：

$$x_{t-1} = f_{\theta}(x_t, F_{\mathrm{VL}}, t)$$

最终输出可执行的动作序列。在整个流程中，视觉编码器保持冻结且不量化，而语言骨干和动作头是量化的主要目标。

### 选择性量化布局

QuantVLA 采用差异化的量化策略：对语言骨干网络中的所有线性层进行整型量化；对 DiT 动作头则采用选择性布局——**前馈网络层进行低比特量化，而注意力投影 $W_q$、$W_k$、$W_v$、$W_o$ 保持浮点计算**。这一设计的核心依据来自 Table 1 的消融实验：仅量化 LLM 和 DiT MLP 的组合在 π0.5 上达到 95.4% 平均成功率，最接近全精度基线的 97.1%，而全量化则导致性能急剧下降至 76.3%。保持注意力投影为浮点，有效避免了量化引入的两类系统性漂移。

### 两类关键漂移与校准机制

量化在 DiT 注意力通路中引入两个相互关联的扰动。其一，查询和键的量化误差改变了预 softmax logits 的方差，导致注意力分布的温度漂移，等价于改变了有效温度 $T_{\mathrm{eff}} = \sqrt{d} / (s_q s_k)$。其二，值通路和输出投影的量化误差改变了注意力输出在残差连接处的能量注入，影响后续层归一化的稳定性。

针对这两类漂移，QuantVLA 引入两个轻量级校准机制，均通过小批量未标注校准数据估计标量，并在推理时折叠入反量化尺度：

- **注意力温度匹配**：为每个注意力头计算标量 $\alpha$，通过匹配教师模型与量化模型的 logits 标准差来校准注意力分布。$\alpha_{\mathrm{raw}} = \mathrm{Std}(L_T) / (\mathrm{Std}(L_Q) + 10^{-6})$，经裁剪后折叠入反量化尺度，恢复正确的 softmax 温度。
- **输出头平衡**：为每层计算标量 $\beta$，通过匹配教师模型与量化模型的输出 RMS 来恢复残差流能量。$\beta_{\mathrm{raw}}(l) = \mathrm{RMS}(Z_{T,l}) / (\mathrm{RMS}(Z_{Q,l}) + 10^{-6})$，同样经裁剪后折叠，确保残差连接处的能量分布与全精度模型一致。

Figure 3 的可视化验证了这两个机制的效果：ATM 显著缩小了量化模型与教师模型在注意力 logits 标准差上的差距，OHB 则有效恢复了注意力输出的 RMS，使量化后的统计量回归教师模型。两个标量均被裁剪至 ±0.4 的安全范围，并使用 0.03 的中性带以避免过度校正。

### 与现有高效 VLA 方法的区别

如 Figure 1 所示，现有高效 VLA 方法主要从架构设计、层剪枝、KV 缓存或动态路由等角度切入，而 QuantVLA 直接操作数值精度，在不改变模型架构和执行顺序的前提下，首次实现了语言骨干和扩散动作头的联合低比特量化。

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of representative VLA efficiency frameworks. (1) TinyVLA focuses on compact multimodal transformers and lightweight diffusion-policy heads for architectural efficiency; (2) EfficientVLA accelerates inference by pruning redundant language layers and reusing intermediate representations; (3) VLA-Cache improves throughput through key–value reuse and static caching of vision tokens; (4) MoLe-VLA adopts mixture-of-layers routing to dynamically skip computation in the language module; and (5) QuantVLA introduces a training-free PTQ framework that low-bit quantizes both language and action modules without altering the model architecture*



### 3.1 VLA模型架构与量化瓶颈

QuantVLA面向的VLA模型由三个核心组件构成：视觉编码器（如SigLIP2/DINOv2）提取RGB帧特征，语言骨干网络（LLM）处理自然语言指令并与视觉token融合，以及基于扩散变换器（DiT）的动作头根据融合特征迭代生成机器人动作。视觉编码器保持冻结且不量化，量化仅作用于LLM和DiT模块。

动作头的扩散过程可表述为：

$$x_{t-1} = f_{\theta}(x_t, F_{\mathrm{VL}}, t)$$

其中 $x_t$ 为当前扩散步的动作隐变量，$F_{\mathrm{VL}}$ 为视觉-语言融合特征，$t$ 为扩散时间步，$f_{\theta}$ 为DiT参数化的去噪函数。该迭代去噪过程是推理延迟的主要来源之一。

### 3.2 量化引起的注意力漂移分析

QuantVLA将量化对DiT注意力的影响分解为两个系统性漂移，这是方法设计的理论根基。

**注意力温度漂移。** 设教师模型的查询和键分别为 $Q_T$、$K_T$，量化后的对应量为 $Q_Q$、$K_Q$，量化引入的扰动为 $\varepsilon_{\mathrm{up}}$，则有：

$$Q_Q = Q_T + \varepsilon_{\mathrm{up}} W_q, \quad K_Q = K_T + \varepsilon_{\mathrm{up}} W_k$$

预softmax注意力logits分别为：

$$L_T = \frac{Q_T K_T^\top}{\sqrt{d}}, \quad L_Q = \frac{Q_Q K_Q^\top}{\sqrt{d}}$$

量化引起的一阶logits扰动为：

$$\Delta L \approx \frac{1}{\sqrt{d}} \Big( (\varepsilon_{\mathrm{up}} W_q) K_T^\top + Q_T (\varepsilon_{\mathrm{up}} W_k)^\top \Big) + \Delta L_{\mathrm{local}}$$

通过softmax的雅可比矩阵 $J_{\mathrm{softmax}}(L_T)$，注意力权重的变化可近似为：

$$A_Q \approx A_T + J_{\mathrm{softmax}}(L_T) \Delta L$$

这一扰动直接改变了注意力分布的温度特性。附录C进一步揭示了注意力有效温度 $T_{\mathrm{eff}} = \sqrt{d} / (s_q s_k)$ 由查询和键的反量化尺度 $s_q$、$s_k$ 决定，量化后该温度发生偏移，导致softmax输出的锐度改变。

**残差能量漂移。** 注意力输出经过多头拼接和输出投影后，量化还会引起残差流能量的变化。一阶展开的输出扰动为：

$$\Delta O \approx J_{\mathrm{softmax}}(L_T) \Delta L V_T W_{o,T} + A_T \varepsilon_{\mathrm{up}} W_v W_{o,T} + A_T V_T \delta W_o + \Delta O_{\mathrm{local}}$$

该扰动包含三项：logits扰动经注意力权重传播、值通路量化噪声、以及输出投影权重的量化误差。这些扰动经残差连接和层归一化逐层累积，严重破坏低比特下的模型稳定性。

### 3.3 选择性量化布局

基于上述分析，QuantVLA采用选择性量化策略：对LLM的所有线性层进行整数量化，对DiT的MLP层进行整数量化，但**保持注意力投影 $W_q$、$W_k$、$W_v$、$W_o$ 为浮点计算**。这一布局直接规避了量化对注意力温度和残差能量的破坏性影响，同时保留了LLM和DiT MLP的量化带来的内存节省。消融实验（Table 1）证实，仅量化LLM和DiT MLP的性能最接近全精度基线，而全量化（包括注意力投影）导致任务成功率从97.1%骤降至76.3%。

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/004_Table_1.jpg]]
*Table 1: Selective layer-quantization results under the QuantVLA architecture without ATM/OHB calibration for π0.5 and GR00T N1.5 on LIBERO*

### 3.4 注意力温度匹配（ATM）

为进一步消除量化LLM引入的logits分布偏移，ATM对每个注意力头学习一个温度标量 $\alpha$。该标量通过匹配教师模型与量化模型的logits标准差计算：

$$\alpha_{\mathrm{raw}} = \frac{\mathrm{Std}(L_T)}{\mathrm{Std}(L_Q) + 10^{-6}}$$

为保证稳定性，对原始标量进行裁剪：

$$\alpha = \mathrm{clip}(\alpha_{\mathrm{raw}}, \alpha_{\mathrm{min}}, \alpha_{\mathrm{max}})$$

裁剪后的 $\alpha$ 被折叠入反量化尺度，在推理时无额外计算开销。Figure 3（左）显示，ATM显著缩小了量化模型与教师模型在各注意力块的logits标准差差距。

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/005_Figure_3.jpg]]
*Figure 3: ATM and OHB effects across attention blocks. (Left) shows logits standard deviation. (Right) shows attention output RMS after the output projection. The figure reports three configurations: the teacher model in floating point without quantization, the quantized baseline with LLM and DiT MLP integerized, and QuantVLA with ATM in the left panel or QuantVLA with OHB in the right panel, which are evaluated on the GR00T N1.5 model*

### 3.5 输出头平衡（OHB）

为恢复残差流的能量分布，OHB对每层学习一个能量标量 $\beta$。该标量通过匹配教师与量化模型在注意力输出投影后的RMS值计算：

$$\beta_{\mathrm{raw}}(l) = \frac{\mathrm{RMS}(Z_{T,l})}{\mathrm{RMS}(Z_{Q,l}) + 10^{-6}}$$

其中 $Z_{T,l}$ 和 $Z_{Q,l}$ 分别为第 $l$ 层教师和量化模型的输出头激活值。与ATM类似，$\beta$ 经过裁剪后折叠入反量化尺度。Figure 3（右）显示，OHB使量化模型的注意力输出RMS回归教师水平，有效稳定了残差连接和后续层归一化的输入分布。

### 3.6 标定与部署

ATM的 $\alpha$ 和OHB的 $\beta$ 均通过少量未标注标定数据估计，裁剪至 $\pm 0.4$ 的安全范围，并使用 $\varepsilon = 0.03$ 的中性带避免过度校正。所有标量在标定后折叠入反量化尺度，推理时无额外计算或内存开销。



## 实验与关键发现

### 实验设置

QuantVLA 在两个代表性 VLA 模型上进行评估：**OpenPI π0.5**（基于 PaliGemma 语言骨干网络）和 **GR00T N1.5**（基于 SmolLM2 语言骨干网络），两者均采用基于 DiT 的动作头。评估基准为 **LIBERO** 套件，包含 LIBERO-Spatial、LIBERO-Object、LIBERO-Goal 和 LIBERO-Long 四个子任务，指标为任务成功率。主实验采用 **W4A8** 量化精度，即权重 4 比特、激活 8 比特。标定数据来自少量无标注校准样本，ATM 的 α 和 OHB 的 β 在折叠入反量化尺度前被裁剪至 ±0.4 的安全范围，并使用 ε=0.03 的中立带。

### 主要结果

**Table 2** 展示了 QuantVLA 在 LIBERO 上的核心结果。在 OpenPI π0.5 上，QuantVLA W4A8 在四个子任务上的平均成功率达到 **97.6%**，不仅未损失性能，反而**超过全精度基线 0.5 个百分点**（FP16 基线为 97.1%）。在 GR00T N1.5 上，QuantVLA W4A8 平均成功率为 **88.0%**，同样**超出全精度基线 1.5 个百分点**（FP16 基线为 86.5%）。这一反直觉的提升表明，校准机制在消除量化噪声的同时，可能对注意力分布起到了良性正则化作用。

与现有量化方法的对比更加突出 QuantVLA 的优势。在 π0.5 上，**DuQuant**（Lin et al., NeurIPS 2024）在相同 W4A8 设置下仅获得 76.3% 的平均成功率，QuantVLA 相对提升 **+21.3 个百分点**。在 GR00T N1.5 上，**SmoothQuant**（Xiao et al., ICML 2023）W4A8 在 Pick-and-Can 操控任务上仅完成 16/50 次成功，而 QuantVLA 达到 27/50 次（**Table 6**）。这些差距说明，通用的后训练量化方法无法处理 VLA 模型中 DiT 动作头的独特漂移问题。

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/010_Table_6.jpg]]
*Table 6: Quantization results on Pick-and-Can*

内存节省方面，QuantVLA 将 π0.5 的 LLM+DiT 模块内存从 4.27 GB 降至 **1.28 GB**，将 GR00T N1.5 从 2.02 GB 降至 **0.91 GB**，相对节省约 **70%**（**Figure 4**）。这一节省得益于选择性量化布局：LLM 全部线性层和 DiT MLP 层被整型化，而视觉编码器保持冻结不量化。

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/007_Figure_4.jpg]]
*Figure 4: Memory saving of QuantVLA over the baseline on OpenPI π0.5 and GR00T N1.5*

### 选择性量化布局消融

**Table 1** 报告了不同层选择方案的消融结果（不含 ATM/OHB 校准）。关键发现：

- **仅量化 LLM** 时，π0.5 平均成功率为 96.8%，GR00T N1.5 为 85.0%，与全精度基线接近。
- **量化 LLM + DiT MLP**（即 QuantVLA 的选择性布局），π0.5 为 95.4%，GR00T N1.5 为 82.5%，性能保持良好。
- **全量化**（包括 DiT 注意力投影 Q、K、V、O）导致性能急剧下降：π0.5 从 97.1% 跌至 76.3%，GR00T N1.5 从 86.5% 跌至 69.5%。

这验证了核心假设：DiT 的注意力投影对量化极为敏感，保持其浮点计算是维持模型稳定性的关键。量化注意力投影会同时引入温度漂移和残差能量偏移，两者叠加导致动作生成质量严重退化。

### ATM 与 OHB 校准效果

**Figure 3** 可视化了 ATM 和 OHB 对注意力统计量的恢复效果。左图显示，量化基线（无校准）的注意力 logits 标准差与教师模型存在显著偏差，而 ATM 通过每头标量 α 将量化模型的 logits 标准差拉回教师水平。右图显示，OHB 通过每层标量 β 有效缩小了注意力输出 RMS 的差距。两个校准机制共同作用，使量化模型的内部表示统计量回归教师模型，这是 QuantVLA 能够在低比特下超越全精度基线的直接原因。

### 极低位宽鲁棒性

**Table 3** 展示了 QuantVLA 在 W4A4 精度下的表现。在 π0.5 上，W4A4 仍达到 **95.3%** 的平均成功率，仅比 W4A8 的 97.6% 下降 2.3 个百分点，且仍高于 DuQuant W4A8 的 76.3%。这表明 ATM 和 OHB 的校准机制在极低位宽下依然有效，为未来更激进的压缩提供了可能性。

### 去噪步数鲁棒性

**Table 4** 测试了 GR00T N1.5 在不同去噪步数下的表现。将去噪步数从 16 步减至 8 步，QuantVLA W4A8 的性能几乎不受影响（成功率波动在 1 个百分点以内），说明量化后的 DiT 动作头对去噪步数不敏感，这有利于进一步降低推理延迟。

### 非 DiT 架构的适用性

**Table 7** 报告了 QuantVLA 在 **OpenVLA**（非 DiT 动作头）上的结果。由于 ATM/OHB 主要针对 DiT 的注意力漂移设计，在 OpenVLA 上 QuantVLA 采用 W8A16 精度，成功率达到 80.7%，接近全精度基线的 82.3%。这验证了选择性量化布局的通用性，但也表明校准机制需要针对不同动作头架构进行适配。

### 失败模式与局限性

尽管 QuantVLA 在多数场景下表现优异，仍存在以下局限：

1. **长程任务退化**：在 W4A4 精度下，LIBERO-Long 的成功率下降相对明显，表明极低位宽下长序列推理的累积误差仍是挑战。
2. **架构依赖性**：ATM/OHB 校准机制针对 DiT 注意力头设计，对于 OpenVLA 等非 DiT 架构需采用不同策略（如 W8A16），通用性受限。
3. **标定数据敏感性**：量化标定依赖少量无标注数据，若标定数据分布与实际部署环境差异较大，校准效果可能下降。当前论文未提供跨场景泛化的标定鲁棒性实验。
4. **无训练恢复路径**：方法未涉及训练感知量化，无法通过微调进一步恢复极低位宽下的性能损失。

### 补充图表

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/006_Table_2.jpg]]
*Table 2: Results on LIBERO for different QuantVLA variants on OpenPI π0.5 and GR00T N1.5. The table reports success rates (%) across four LIBERO tasks, memory (GB), and the relative memory savings versus each model’s baseline*

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/008_Table_3.jpg]]
*Table 3: LIBERO results on OpenPI π0.5 comparing FP16, W4A8, and W4A4 precision*

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/009_Table_4.jpg]]
*Table 4: LIBERO results under different denoising steps on GR00T N1.5*

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/011_Table_7.jpg]]
*Table 7: Quantization results on LIBERO-Spatial for OpenVLA*

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/012_Table_5.jpg]]
*Table 5: Additional quantization comparison on the LIBERO benchmark for OpenPI π0.5*

![[assets/figures/papers/paper_list_l2242_https_arxiv_org_abs_2602_20309/figures/002_Table.jpg]]



## 定位与知识库关联

### 问题定位：VLA模型的后训练量化空白

视觉-语言-动作（VLA）模型将多模态理解与机器人操控统一为端到端策略，但其推理部署面临严重的计算与内存瓶颈。现有VLA效率优化方法主要沿三条路径展开：**架构压缩**（如TinyVLA设计紧凑的多模态Transformer和轻量扩散策略头）、**推理加速**（如EfficientVLA剪枝冗余语言层并重用中间表示）、以及**缓存与路由策略**（如VLA-Cache通过键值缓存和静态视觉token缓存提升吞吐，MoLe-VLA采用混合层路由动态跳过语言模块计算）。然而，这些方法均未触及**数值精度**层面的优化——它们要么重新设计模型架构，要么在未改变的模型外围添加缓存/路由机制，几乎没有方法直接对扩散动作头（DiT）进行部署效率优化。

QuantVLA填补了这一空白：它首次提出面向VLA模型的**训练无关后训练量化（PTQ）框架**，同时量化语言骨干网络和扩散动作头，且不改变原有架构与算子调度。这一设计使其与现有VLA效率方法形成互补而非竞争关系——QuantVLA的量化压缩可以叠加在架构优化或缓存策略之上。

### 量化方法谱系中的继承与突破

在通用PTQ方法谱系中，QuantVLA继承了**旋转量化**（rotation-based quantization）的异常值抑制思想。具体而言，它借鉴了**DuQuant**（Lin et al., NeurIPS 2024）和**SmoothQuant**（Xiao et al., ICML 2023）中的重参数化技术，通过正交矩阵变换平滑激活异常值，提升VLA模型中线性层的量化稳定性。但与这些通用PTQ方法不同，QuantVLA面临的核心挑战是**多模态-扩散耦合场景下的量化漂移**——这是传统LLM或ViT量化中不曾出现的系统性失效模式。

QuantVLA的关键突破在于识别并校正了DiT量化引入的两类系统性漂移：

1. **注意力温度漂移**：量化引入的查询/键扰动改变了预softmax logits的方差，等效于改变了softmax的有效温度 $T_{\text{eff}} = \sqrt{d} / (s_q s_k)$，导致注意力分布过度集中或平坦化，破坏动作生成的精度。

2. **残差流能量偏移**：值通路和输出投影的量化扰动改变了注意力输出的RMS，经残差连接传播后破坏层归一化的统计假设，引发误差的逐层累积。

针对这两类漂移，QuantVLA提出了**注意力温度匹配（ATM）**和**输出头平衡（OHB）**两个轻量级校准机制，通过无标注校准数据估计校正标量并折叠入反量化尺度，无需任何训练或梯度回传。这一"标量折叠"设计在PTQ方法中具有通用性——其本质是在不增加推理计算的前提下恢复关键统计量，可推广至其他需要保持注意力分布或残差能量稳定性的量化场景。

### 选择性量化布局的设计逻辑

QuantVLA的另一个关键设计决策是**选择性量化布局**：对语言骨干网络（LLM）的所有线性层和DiT的前馈网络（MLP）进行低比特量化，但保持DiT的注意力投影（Q、K、V、O）为浮点计算。这一选择并非出于工程便利，而是基于对量化误差传播的因果分析：

- 注意力投影的量化误差通过softmax的非线性放大效应和残差连接的累积效应，对最终动作质量产生远超其他线性层的影响。
- 保持注意力投影为浮点的额外内存开销极小（仅占DiT总参数的一小部分），但能从根本上避免温度漂移和能量偏移的源头。

消融实验（Table 1）验证了这一设计的必要性：全量化方案（包括注意力投影）在π0.5上导致任务成功率从97.1%骤降至76.3%，而仅量化LLM和DiT MLP的方案已接近全精度基线（95.4% vs. 97.1%），再叠加ATM/OHB后可进一步超越基线（97.6%）。

### 适用边界与局限

QuantVLA的当前设计存在明确的适用边界：

**架构依赖**：ATM和OHB校准机制主要针对DiT动作头设计。对于非DiT架构的VLA模型（如OpenVLA），需采用不同策略（如W8A16精度），通用性受限。这一局限的根源在于：DiT中注意力温度和残差能量的漂移机制与标准Transformer存在差异，ATM/OHB的标量估计依赖于DiT特有的统计特性。

**数据分布敏感**：量化标定依赖少量未标注数据，若标定数据分布与实际部署环境差异较大，校准效果可能下降。这是PTQ方法的共性问题，但VLA场景中机器人操作环境的多样性加剧了这一风险。

**极低位宽退化**：在W4A4精度下，长程任务（如LIBERO Long）的成功率略有下降，表明极端量化下长期时序依赖的稳定性仍需提升。当前方法无法通过微调恢复性能，因为其设计哲学是训练无关的。

### 开放问题

1. **通用动作头量化方案**：如何设计适用于更广泛多模态-扩散耦合场景的通用量化方案，使得非DiT动作头（如基于MLP的策略头、自回归动作头）也能获得同等低比特效率？

2. **训练感知扩展**：是否可以将ATM/OHB的"温度-能量校准"思想推广到训练感知量化（QAT）中，通过端到端学习动态调整温度与能量标量，进一步压缩位宽并恢复性能？

3. **大规模VLA扩展性**：在大规模基础VLA模型（如更大参数量的GR00T版本）上，QuantVLA的扩展性如何？量化误差是否会随模型规模增大而出现新的失效模式？

4. **实时部署验证**：量化后模型在实际机器人部署中的实时性和控制精度能否进一步验证？当前评估主要基于离线基准测试，在线操控场景中的延迟、抖动和安全性尚未充分评估。

5. **与系统优化的协同**：QuantVLA的量化压缩与VLA-Cache、MoLe-VLA等系统级优化是否可叠加？若能，组合后的内存和延迟收益边界在哪里？



## 原文 PDF

![[paperPDFs/CVPR_2026/QuantVLA_Scale_Calibrated_Post_Training_Quantization_for_Vision_Language_Action_Models.pdf]]
