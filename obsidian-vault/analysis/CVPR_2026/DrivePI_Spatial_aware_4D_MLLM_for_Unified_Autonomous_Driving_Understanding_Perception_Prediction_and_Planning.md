---
title: "DrivePI: Spatial-aware 4D MLLM for Unified Autonomous Driving Understanding, Perception, Prediction and Planning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DrivePI_Spatial_aware_4D_MLLM_for_Unified_Autonomous_Driving_Understanding_Perception_Prediction_and_Planning.pdf
project_link: null
code_link: "https://github.com/happinesslz/DrivePI"
aliases:
- DrivePI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入LiDAR作为互补模态增强3D几何信息，设计多阶段数据引擎生成文本-占位、文本-流等QA对，并将粗粒度语言理解与细粒度空间学习（3D占位、占位流、轨迹规划）通过统一MLLM架构与多任务头联合优化，从而同时提升交互性与感知精度。
primary_logic: 通过统一框架融合粗粒度语言理解和细粒度空间学习，利用LiDAR提供精准3D几何先验，构建多阶段数据引擎生成丰富空间推理QA数据，使小参数MLLM也能在语言理解和精细感知上同时超越现有VA和VLA模型，实现真正空间感知的4D MLLM。
claims:
- DrivePI在OpenOcc上以49.3 RayIoU超越FB-OCC 10.3，同时将占位流mAVE从0.591降至0.509，并在未使用自车状态时比VAD的L2误差降低32%（0.72m→0.49m）
- DrivePI以0.5B模型在nuScenes-QA上达到60.7%准确率，优于OpenDriveVLA-7B（2.5%提升），且碰撞率相对于ORION降低70%（0.37%→0.11%）
- 消融实验显示联合文本头与视觉头使3D占位RayIoU提高1.8%、占位流mAVE降低0.18、规划L2降低0.52，证明统一框架的互补增益
- 数据缩放实验表明，将占位QA对从28K扩充至560K，使占位状态准确率提升14%、类别准确率提升44.9%，验证数据引擎的有效性
---

# DrivePI: Spatial-aware 4D MLLM for Unified Autonomous Driving Understanding, Perception, Prediction and Planning

> [!tip] 核心洞察
> 通过统一框架融合粗粒度语言理解和细粒度空间学习，利用LiDAR提供精准3D几何先验，构建多阶段数据引擎生成丰富空间推理QA数据，使小参数MLLM也能在语言理解和精细感知上同时超越现有VA和VLA模型，实现真正空间感知的4D MLLM。

| 字段 | 内容 |
|------|------|
| 中文题名 | DrivePI：面向统一自动驾驶理解、感知、预测和规划的空间感知4D多模态大语言模型 |
| 英文题名 | DrivePI: Spatial-aware 4D MLLM for Unified Autonomous Driving Understanding, Perception, Prediction and Planning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.12799) · [Code](https://github.com/happinesslz/DrivePI) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DrivePI |
| Dataset | OpenOcc validation set, nuScenes validation set, nuScenes-QA validation set, Occ3D-nuScenes validation set |

> [!tip] 效果简介
> - OpenOcc validation set 上，RayIoU (3D Occupancy) 49.3 vs FB-OCC 39.0 (+10.3)；mAVE (Occupancy Flow) 0.509 vs FB-OCC 0.591 (-0.082 (improvement))。
> - nuScenes validation set 上，L2 error (avg, without ego status) 0.49 vs VAD 0.72 (-0.23 (-32%))；Collision rate (avg, with ego status) 0.11% vs ORION 0.37% (-70%)。
> - nuScenes-QA validation set 上，Overall Accuracy 60.7% vs OpenDriveVLA-7B 58.2% (+2.5%)。

## 概要

自动驾驶系统正朝着端到端统一建模的方向演进，但现有范式存在结构性矛盾：**视觉-行动（VA）模型**（如VAD、FB-OCC）具备细粒度3D感知与规划能力，却缺乏自然语言交互接口，难以提供可解释的场景理解；**视觉-语言-行动（VLA）模型**（如OpenDriveVLA-7B、ORION）虽支持语言交互，却因缺少中间3D感知与预测输出，导致空间推理精度不足、安全隐患突出。二者如同鱼与熊掌，始终未能兼得。

DrivePI的核心洞见在于：**粗粒度语言理解与细粒度空间学习并非互斥，而是可以通过统一框架相互增强**。具体而言，该方法引入LiDAR点云作为互补模态，为3D几何推理提供精准先验；设计多阶段数据引擎，从场景描述、4D空间推理到规划推理，生成超百万条高质量QA对；将文本头（自回归场景理解）、3D占位头、占位流头与行动扩散头并行接入同一MLLM骨干，通过端到端联合优化，使小参数模型（Qwen2.5-0.5B）同时获得语言交互与精细感知的双重能力。

实验结果表明，DrivePI在多个基准上实现了跨范式的性能超越：
- **3D占位**：OpenOcc验证集上RayIoU达49.3，较FB-OCC提升10.3；
- **占位流预测**：mAVE从0.591降至0.509；
- **轨迹规划**：在未使用自车状态条件下，L2误差较VAD降低32%（0.72m→0.49m），碰撞率相较ORION降低70%（0.37%→0.11%）；
- **语言理解**：nuScenes-QA上以60.7%准确率超越OpenDriveVLA-7B（+2.5%）。

消融实验进一步揭示了统一框架的协同增益：联合训练文本头与视觉头使3D占位RayIoU提高1.8、占位流mAVE降低0.18、规划L2降低0.52；数据缩放实验表明，将占位QA对从28K扩充至560K，占位状态准确率提升14%、类别准确率提升44.9%。

**方法定位**：DrivePI处于VA与VLA的交汇地带，以“空间感知4D MLLM”的姿态，首次在统一架构内实现了从场景理解、3D感知、运动预测到轨迹规划的完整闭环。其关键设计——LiDAR增强的空间投影器、多阶段数据引擎、多任务头并行优化——为端到端自动驾驶的可解释性与安全性提供了新的技术路径。当前局限包括多任务损失权重未精细平衡、仅完成开环评估、泛化性待验证等问题，后续工作将探索自适应损失策略与闭环强化学习扩展。

端到端自动驾驶正经历从“感知-决策-控制”分离架构向统一模型范式的转变。当前主流路线可归为两类：**视觉-行动（VA）模型**与**视觉-语言-行动（VLA）模型**，二者在能力边界上形成鲜明互补，却也暴露出难以调和的矛盾。

VA模型（如**VAD**、**FB-OCC**）以多视图图像为输入，直接输出规划轨迹或中间3D占位表示，在感知精度和驾驶安全性上表现突出。然而，这类模型完全缺乏自然语言交互能力——它们无法解释“为什么此时选择变道”或“前方施工区域的风险等级如何”，使得系统决策过程对乘客和监管者而言如同黑箱。在安全攸关的自动驾驶场景中，这种可解释性缺失构成了根本性的信任障碍。

VLA模型（如**OpenDriveVLA-7B**、**ORION**、**OmniDrive**）则试图弥合这一鸿沟：通过将视觉编码器与大语言模型衔接，赋予自动驾驶系统场景描述、问答对话等粗粒度语言理解能力。但代价同样显著——现有VLA模型普遍缺少对3D占位、占位流等细粒度中间感知输出的显式建模，其空间理解停留在语言符号层面而非精确几何层面。当模型声称“前方有车辆”却无法给出该车辆的3D边界框或运动矢量时，语言交互的可信度便大打折扣，安全隐患也随之而来。

这一困境的根源在于：**粗粒度语言理解与细粒度空间感知被割裂为两个独立的技术栈**。VA模型精于后者却失语，VLA模型擅长前者却“近视”。二者之间的空白地带——一个既能进行自然语言交互、又能输出精确3D感知与运动预测的统一框架——构成了当前端到端自动驾驶的核心瓶颈。

DrivePI的动机正是打破这一僵局。其核心洞察在于：**通过引入LiDAR点云作为互补3D几何先验，并设计多阶段数据引擎生成大规模空间推理问答对，可以将语言理解与精细感知纳入同一MLLM架构进行端到端联合优化**。这不仅使小参数模型（0.5B）在语言交互上超越7B级VLA模型，更在3D占位、占位流和轨迹规划等细粒度任务上达到甚至超越专用VA模型的水平，首次实现了真正意义上的“空间感知4D多模态大语言模型”。

## 核心方法与创新机理

DrivePI 的核心创新在于**首次将粗粒度语言交互与细粒度 3D 空间感知/预测统一到单个轻量 MLLM 框架中**，从而同时继承了 VA 模型的感知精度与 VLA 模型的交互能力——这是现有方法长期未能兼得的瓶颈。围绕这一目标，方法在输入模态、空间投影、多任务头设计和训练数据四个维度进行了系统性改造。

### 1. 引入 LiDAR 作为互补几何先验

现有端到端 VA/VLA 模型普遍仅依赖多视图图像作为输入，缺乏显式的 3D 几何信息。DrivePI **在图像之外引入 LiDAR 点云**（含时序信息），为模型提供精确的 3D 空间先验。这一改动直接提升了细粒度空间感知的上限——在 OpenOcc 验证集上，3D 占位 RayIoU 达到 49.3，超越仅使用图像的 FB-OCC 达 10.3 个百分点（Table 1）；同时占位流 mAVE 从 0.591 降至 0.509，表明运动预测精度也同步受益。

### 2. 交叉注意力空间投影器：保留细粒度空间信息

传统方法通常将 BEV 特征池化为单一全局向量再映射到语言空间，这一过程严重压缩了空间细节。DrivePI 设计了**基于交叉注意力的空间投影器**：以池化后的 BEV 特征为 Query，以未池化的补丁特征为 Key/Value，通过交叉注意力生成视觉令牌 $F_v \in \mathbb{R}^{N \times C_l}$。这种设计保留了补丁级别的细粒度空间信息，使 MLLM 能够同时支持粗粒度场景描述和细粒度占位/流预测。消融实验（Table 5）表明，联合训练文本头与视觉头后，3D 占位 RayIoU 额外提升 1.8%，占位流 mAVE 降低 0.18，规划 L2 误差降低 0.52，直接验证了该投影器对多任务协同的关键支撑作用。

### 3. 四头并行输出：从“单一输出”到“粗细粒度联合推理”

现有 VA 模型仅输出规划轨迹，VLA 模型仅输出文本，二者均无法同时提供可解释的中间感知结果。DrivePI 在 MLLM 输出端并行挂载四个专用头：
- **文本头**：自回归式场景理解（粗粒度）
- **3D 占位头**：预测语义占位（细粒度）
- **占位流头**：预测像素级运动速度（细粒度）
- **行动扩散头**：轨迹规划（细粒度）

四个头共享 MLLM 的多模态表征，通过统一的端到端损失 $L_{total} = \lambda_1 L_{llm} + \lambda_2 L_{occ} + \lambda_3 L_{flow} + \lambda_4 L_{action}$ 联合优化。这一设计使得模型在输出规划指令的同时，能够显式地给出“看到了什么、物体如何运动”的中间表征，大幅增强了可解释性与安全性——规划碰撞率相对 ORION 降低 70%（0.37%→0.11%，Table 2），且在不使用自车状态时 L2 误差比 VAD 低 32%（0.72m→0.49m）。

### 4. 多阶段数据引擎：构建 4D 空间推理 QA 数据

现有 VLA 模型的训练数据多为简单的场景描述或基础 QA，缺乏对 3D 空间与时间动态的细粒度标注。DrivePI 构建了**三阶段数据引擎**（Figure 3）：
1. **场景描述生成**：利用 InternVL3-78B 融合前后视图字幕，生成 84k 高质量场景描述；
2. **4D 空间推理标注**：基于占位与流真值，通过多轮对话生成 text-occupancy 和 text-flow QA 对，共 560k 条；
3. **规划推理标注**：生成 24k text-planning QA 对。

数据缩放实验（Table 6）提供了强因果证据：将占位 QA 对从 28K 扩充至 560K，占位状态准确率提升 14%、类别准确率提升 44.9%，直接验证了数据引擎对空间推理能力的决定性作用。最终，DrivePI 仅以 0.5B 参数量在 nuScenes-QA 上达到 60.7% 准确率，超越 7B 的 OpenDriveVLA-7B 达 2.5%（Table 3），证明精心构造的空间推理数据可以弥补模型规模差距。

### 创新点之间的因果链路

上述四个创新并非孤立存在，而是形成了一条清晰的因果链：**LiDAR 提供几何先验 → 交叉注意力投影器保留空间细节 → 多任务头实现粗细粒度联合推理 → 数据引擎提供训练信号**。消融实验（Table 5）证实，仅启用文本头或仅启用视觉头时，各自性能均显著低于联合训练——说明粗细粒度任务之间存在互补增益，而非简单叠加。这一发现是 DrivePI 能够以小参数模型同时超越 VA 和 VLA 基线的根本原因。

DrivePI 的整体框架旨在统一粗粒度的语言理解与细粒度的空间感知、预测与规划。其核心设计思路是：将多视图图像与 LiDAR 点云作为互补输入，通过视觉编码与空间投影转换为视觉令牌，再与文本指令令牌共同送入一个轻量级多模态大语言模型（MLLM），最后由四个并行的专用头分别输出场景描述、3D 占位、占位流和轨迹规划。

### 输入模态与视觉编码

与现有仅依赖多视图图像的 VA 和 VLA 模型不同，DrivePI 显式引入 **LiDAR 点云**作为额外输入（nuScenes 数据集中的 LiDAR 点云天然包含时间信息），以提供精确的 3D 空间几何先验。视觉编码器从图像和 LiDAR 数据中提取潜在 BEV 特征 $F_{bev} \in \mathbb{R}^{H \times W \times C}$，随后将其切分为 $N = \frac{H}{K} \times \frac{W}{K}$ 个补丁（$K$ 为补丁尺寸），得到补丁特征 $F_{patch}$ 和池化特征 $F_{pool}$。

### 空间投影器

空间投影器（Spatial Projector）负责将潜在 BEV 特征映射到语言空间，生成视觉令牌 $F_v \in \mathbb{R}^{N \times C_l}$（$C_l$ 为 MLLM 隐藏状态维度）。与常见的池化聚合方式不同，DrivePI 采用**交叉注意力机制**：以池化特征 $F_{pool}$ 为查询，补丁特征 $F_{patch}$ 为键和值。这一设计保留了更细粒度的空间信息，为后续的 3D 占位和占位流预测提供了关键的空间表征基础。

### MLLM 处理与多任务头

视觉令牌与文本令牌共同输入 MLLM（默认采用 **Qwen2.5-0.5B**），生成多模态输出表征。MLLM 的输出通过四个专用头并行处理：

- **文本头（Text Head）**：以自回归方式生成场景描述，实现粗粒度语言理解。
- **3D 占位头（3D Occupancy Head）**：从视觉令牌中提取并重塑为空间特征图，预测 3D 占位的语义类别，实现细粒度空间感知。
- **占位流头（Occupancy Flow Head）**：预测像素级运动速度，实现细粒度运动预测。
- **行动扩散头（Action Diffusion Head）**：预测自车未来轨迹，实现细粒度规划。

### 多阶段数据引擎

为支撑上述统一框架的训练，DrivePI 设计了多阶段数据引擎（Figure 3），生成超过 1.0M 的 QA 对：

1. **场景描述生成**：分别生成前、后视图的字幕，再由 InternVL3-78B 合并润色，得到 84k 训练场景描述。
2. **4D 空间推理 QA 生成**：基于占位和占位流真值，通过多轮对话生成 text-occupancy 和 text-flow QA 对，共 560k，增强 4D 空间理解能力。
3. **规划推理 QA 生成**：生成 text-planning QA 对（24k），使 MLLM 能够预测自车的未来行动。

### 训练策略与损失函数

训练分两阶段进行：第一阶段冻结视觉编码器和 MLLM，仅训练空间投影器；第二阶段冻结视觉编码器，联合优化空间投影器、MLLM 和所有任务头。总损失函数为四项损失的加权和：

$$L_{total} = \lambda_{1} L_{llm} + \lambda_{2} L_{occ} + \lambda_{3} L_{flow} + \lambda_{4} L_{action}$$

默认所有权重 $\lambda_i = 1$，实现端到端的统一优化。值得注意的是，为避免捷径学习，训练默认**不使用自车状态**（ego status），所有实验结果（除非特别注明）均在此公平设置下获得。

![[assets/figures/papers/paper_list_l2149_https_arxiv_org_abs_2512_12799/figures/001_Figure_1.jpg]]
*Figure 1: (a) presents the pipeline of mainstream visionaction (VA) models for end-to-end autonomous driving. (b) illustrates mainstream Vision-Language-Action (VLA) models. (c) shows our DrivePI, which combines coarse-grained linguistic understanding with fine-grained 3D perception and prediction, inheriting advantages both existing VA models and VLA models*

### 视觉编码与空间投影器

DrivePI 的感知前端由视觉编码器与空间投影器构成，负责将多模态传感器数据转换为 MLLM 可消费的视觉令牌序列。视觉编码器以多视图图像和 LiDAR 点云为输入，提取潜在 BEV 特征 $F_{bev} \in \mathbb{R}^{H \times W \times C}$，其中 $H$、$W$ 为 BEV 特征图的空间尺寸，$C$ 为通道数。随后，BEV 特征图以补丁尺寸 $K$ 进行切分，得到 $N = \frac{H}{K} \times \frac{W}{K}$ 个补丁特征 $F_{patch}$，并经过池化得到全局池化特征 $F_{pool}$。

空间投影器采用交叉注意力机制完成 BEV 特征到语言空间的映射：以 $F_{pool}$ 作为查询（Query），$F_{patch}$ 同时作为键（Key）和值（Value）。这一设计相较于简单池化聚合保留了更细粒度的空间信息，最终输出视觉令牌 $F_v \in \mathbb{R}^{N \times C_l}$，其中 $C_l$ 为 MLLM 隐藏状态的维度。

### 多任务头设计

MLLM 输出的多模态表征被四个并行任务头共享，实现粗粒度语言理解与细粒度空间学习的统一：

- **文本头**：以自回归方式生成场景描述文本，承担粗粒度场景理解任务。
- **3D 占位头**：从视觉令牌中提取并重塑为空间特征图，预测 3D 占位语义类别，实现细粒度空间感知。
- **占位流头**：预测逐像素的占位流速度，提供细粒度运动预测。
- **行动扩散头**：基于扩散模型输出自车轨迹规划，属于细粒度决策输出。

### 总损失函数

DrivePI 将四项任务的损失以加权和形式联合优化，总损失定义为：

$$L_{total} = \lambda_{1} L_{llm} + \lambda_{2} L_{occ} + \lambda_{3} L_{flow} + \lambda_{4} L_{action}$$

其中 $L_{llm}$ 为文本生成的交叉熵损失，$L_{occ}$ 为 3D 占位分类损失，$L_{flow}$ 为占位流回归损失，$L_{action}$ 为轨迹规划损失。默认设置下 $\lambda_1 = \lambda_2 = \lambda_3 = \lambda_4 = 1$，即各任务损失等权重。

消融实验（Table 7）表明，降低占位与流损失权重（如从 1.0 降至 0.2）会损害 3D 占位与流性能，但略微提升规划与 QA 精度，提示当前均匀权重策略并非最优，多任务损失平衡仍需进一步优化。

### 隐藏状态加权组合

为进一步利用 MLLM 多层表征中的空间信息，DrivePI 将 MLLM 最后一个隐藏状态替换为所有 Transformer 层隐藏状态的加权组合：

$$h = \sum_{i=0}^{l} F_{i}^{h} \cdot w_{i}$$

其中 $F_i^h$ 为第 $i$ 层隐藏状态（$i=0$ 对应输入嵌入），$w_i$ 为可学习的重要性权重。实验（Table 8、Table 9）显示深层获得更高重要性权重，验证了高层表征对空间理解的关键作用。

![[assets/figures/papers/paper_list_l2149_https_arxiv_org_abs_2512_12799/figures/012_Table_8.jpg]]
*Table 8: The learned importance weights of all hidden states in the MLLM with Qwen-2.5 0.5B model, including the input embedding (indexed as 0). The Index and Weight column indicates the index and the learned importance weight of each hidden state*

## 实验与关键发现

### 核心瓶颈与实验逻辑

现有端到端自动驾驶方法面临结构性矛盾：视觉-行动（VA）模型缺乏自然语言交互能力，而视觉-语言-行动（VLA）模型因缺少细粒度中间3D感知与预测输出，导致可解释性不足、安全隐患突出。DrivePI的核心实验逻辑在于验证一个统一框架能否同时突破这两类模型的局限——既保持VLA的语言交互能力，又达到甚至超越VA模型的精细感知与规划精度。实验设计围绕四个维度展开：3D占位与占位流预测（空间感知）、轨迹规划（行动决策）、场景文本理解（语言交互），以及三者间的协同增益。

### 主实验结果

#### 3D占位与占位流：OpenOcc验证集

Table 1展示了DrivePI在OpenOcc验证集上的3D占位与占位流性能。DrivePI以49.3 RayIoU超越VA基线FB-OCC达10.3个百分点，同时占位流mAVE从0.591降至0.509（降幅13.9%），表明引入LiDAR互补模态和统一多任务训练有效提升了时空感知精度。值得注意的是，DrivePI仅使用0.5B参数的MLLM骨干网络（Qwen2.5-0.5B），而FB-OCC等VA基线通常采用专用的感知架构，这一对比凸显了统一框架的效率优势。

#### 轨迹规划：nuScenes验证集

Table 2报告了nuScenes验证集上的规划性能。默认设置下（不使用自车状态，以避免捷径学习），DrivePI的平均L2误差为0.49m，相比VAD的0.72m降低32%。当引入自车状态时，L2误差进一步降至0.40m，碰撞率仅0.11%，较ORION的0.37%降低70%。这一结果表明，细粒度3D占位与占位流预测为规划模块提供了更准确的环境动态表征，从而显著提升了规划安全性。

#### 文本理解：nuScenes-QA验证集

Table 3呈现了nuScenes-QA上的文本理解性能。DrivePI以60.7%的总体准确率超越OpenDriveVLA-7B（58.2%）达2.5个百分点，且模型参数量仅为后者的1/14。在存在性判断（Ext.）、计数（Cnt.）、物体识别（Obj.）、状态描述（Sts.）和比较推理（Cmp.）五个子任务上，DrivePI均展现出竞争力。这一结果验证了多阶段数据引擎生成的56万4D空间推理QA对的有效性——通过将占位与流真值转化为自然语言问答，小参数MLLM也能习得细粒度空间推理能力。

#### 3D占位：Occ3D-nuScenes验证集

Table 4展示了Occ3D-nuScenes上的3D占位性能。DrivePI以46.0 RayIoU超越此前最优方法OPUS（41.2）达4.8个百分点。当DrivePI仅在Occ3D-nuScenes上训练3D占位任务时（标记*），性能仍具竞争力，进一步验证了统一框架中多任务协同训练的正向迁移效应。

### 消融实验

#### 文本头与视觉头的协同增益

Table 5的消融实验揭示了粗粒度语言理解与细粒度空间学习之间的互补机制。仅启用文本头时，QA准确率为61.2%；仅启用视觉头（3D占位+占位流+规划）时，3D占位RayIoU为47.5，占位流mAVE为0.69，规划L2误差为1.02、碰撞率0.39%。联合训练后，3D占位RayIoU提升至49.3（+1.8），占位流mAVE降至0.51（-0.18），规划L2降至0.50（-0.52）。这一结果表明，语言理解任务提供的语义上下文能够正则化空间表征学习，而精细感知任务反过来强化了MLLM对场景几何的理解，形成双向增益。

#### 数据引擎的缩放效应

Table 6展示了数据引擎的缩放实验。将占位QA对从28K扩充至560K（20倍），占位状态准确率提升14%，类别准确率提升44.9%，占位流与行动指令准确率也稳步增长。这一趋势验证了多阶段数据引擎的设计合理性——基于真值自动生成的text-occupancy和text-flow QA对能够为MLLM提供密集的空间推理监督信号，且性能随数据规模持续改善，未出现饱和迹象。

#### 损失权重的敏感性

Table 7分析了多任务损失平衡权重的影响。将3D占位与占位流损失权重从1.0降至0.2时，占位RayIoU和流mAVE性能明显下降，但规划L2误差和QA准确率略有提升。这一权衡表明，当前均匀权重策略（$\lambda_1=\lambda_2=\lambda_3=\lambda_4=1$）并非最优，不同任务间存在一定程度的梯度冲突。如何设计自适应的多任务损失平衡策略，是该方向的一个开放问题。

#### MLLM隐藏层的重要性分布

Table 8和Table 9分别展示了Qwen2.5-0.5B和Qwen2.5-3B中各隐藏层的学习重要性权重。在0.5B模型中，深层（索引20-23）获得了显著更高的权重，表明高层语义表征对空间理解任务至关重要。3B模型也呈现类似趋势，但权重分布更为平滑。这一发现为后续优化视觉令牌注入位置提供了依据——将空间投影器的输出与MLLM高层表征对齐，可能进一步提升细粒度感知性能。

### 失败模式与局限性

尽管DrivePI在多个基准上取得了领先性能，但分析揭示了以下局限：

1. **多任务损失冲突**：如Table 7所示，感知任务与规划/语言任务之间存在权衡，均匀权重策略无法同时最大化所有任务的性能。当前框架缺乏任务优先级感知的损失平衡机制。

2. **开环评估局限**：规划模块仅在nuScenes开环设置下评估，闭环驾驶能力（如CARLA仿真器中的避障与交互）未经验证。开环指标（L2误差、碰撞率）与实际驾驶安全性之间的相关性需要进一步论证。

3. **数据集泛化性**：所有实验基于nuScenes数据集，其传感器配置（6相机+1 LiDAR）和场景分布（波士顿、新加坡城市道路）具有特定性。DrivePI在其他数据集或纯视觉配置下的迁移能力尚待验证。

4. **数据引擎成本**：多阶段数据引擎依赖InternVL3-78B等大模型生成标注，其推理成本与标注质量未量化分析。当扩展到更大规模数据集时，数据生成效率可能成为瓶颈。

### 关键图表结论总结

- **Table 1 & Table 2**：DrivePI在3D占位（RayIoU 49.3）、占位流（mAVE 0.509）和规划（L2 0.49m，碰撞率0.11%）上全面超越VA和VLA基线，验证了统一框架的有效性。
- **Table 3**：以0.5B参数超越7B VLA模型，证明数据引擎生成的4D空间推理QA对能够高效注入空间理解能力。
- **Table 5**：文本头与视觉头联合训练带来1.8 RayIoU和0.52 L2的增益，揭示了语言-空间双向协同机制。
- **Table 6**：数据缩放至560K QA对带来44.9%的类别准确率提升，验证了数据引擎的可扩展性。
- **Table 7**：损失权重调整揭示了感知与规划任务间的梯度冲突，指向自适应平衡策略的研发需求。

![[assets/figures/papers/paper_list_l2149_https_arxiv_org_abs_2512_12799/figures/006_Table_3.jpg]]
*Table 3: Text Understanding performance on the nuScenes-QA validation set. Ext., Cnt., Obj., Sts., Cmp. and Acc. are short for exist, count, object, status, comparison, and the overall accuracy*

![[assets/figures/papers/paper_list_l2149_https_arxiv_org_abs_2512_12799/figures/008_Table_5.jpg]]
*Table 5: Ablation study for text head and vision head in DrivePI*

![[assets/figures/papers/paper_list_l2149_https_arxiv_org_abs_2512_12799/figures/009_Table_6.jpg]]
*Table 6: The ablation study of DrivePI exploring data scaling. The columns of Occ. Status, Occ. Class, Occ. Flow, Action Status denote the occupancy status (i.e., “yes” or “no”), occupancy category, the occupancy flow, the action commands (i.e., “straight”, “right”, “left”, and “stop”), respectively*

![[assets/figures/papers/paper_list_l2149_https_arxiv_org_abs_2512_12799/figures/013_Table_7.jpg]]
*Table 7: Ablation study for the balancing weights in DrivePI*

## 定位与知识库关联

### 1. 与现有VA/VLA模型的关系

DrivePI处于端到端自动驾驶中**视觉-行动（VA）模型**与**视觉-语言-行动（VLA）模型**的交叉地带，其设计动机直接源于对两类方法结构性缺陷的回应。

**VA模型的瓶颈：** 以**VAD**、**FB-OCC**、**ALOcc-Flow-3D**等为代表的VA模型，擅长细粒度的3D感知（占位预测）和轨迹规划，但完全缺乏自然语言交互能力，无法解释其决策过程，构成安全隐患。这些模型通常仅依赖多视图图像作为输入，BEV特征经池化聚合后损失了大量空间细节。

**VLA模型的瓶颈：** 以**OpenDriveVLA-7B**、**ORION**、**OmniDrive**等为代表的VLA模型，虽然具备语言理解与交互能力，但其感知输出通常停留在粗粒度的场景描述层面，缺少可验证的中间3D感知与预测输出（如3D占位、占位流），导致可解释性不足。

**DrivePI的定位：** 如Figure 1所示，DrivePI通过统一框架同时继承VA模型的精细感知能力和VLA模型的语言交互能力。其核心策略是引入LiDAR点云作为互补模态以增强3D几何先验，并设计多阶段数据引擎生成text-occupancy、text-flow等空间推理QA对，使小参数MLLM（Qwen2.5-0.5B）也能在语言理解和精细感知上同时超越上述两类模型。

### 2. 关键设计差异

与现有工作相比，DrivePI在以下维度做出实质性改变：

| 维度 | 基线方法 | DrivePI |
|------|---------|---------|
| **输入模态** | 仅多视图图像 | 多视图图像 + LiDAR点云（含时间信息） |
| **空间投影** | 池化聚合BEV特征为单一表示 | 交叉注意力机制，以池化特征为查询、补丁特征为键/值，保留细粒度空间信息 |
| **输出任务** | 仅文本头或仅规划头 | 文本头 + 3D占位头 + 占位流头 + 行动扩散头，并行输出 |
| **训练数据** | 标准场景描述或简单QA | 多阶段数据引擎生成：84k场景描述、560k 4D空间推理QA、24k规划推理QA |
| **MLLM骨干** | 较大参数（如OpenDriveVLA-7B） | Qwen2.5-0.5B |

其中，空间投影器的交叉注意力设计是保留细粒度空间信息的关键——它避免了传统池化操作导致的信息压缩损失。3D占位头和占位流头的设计参考了**FlashOcc**等VA模型的占位头结构，但将其整合进统一的MLLM框架中。

### 3. 适用边界

**已验证的有效范围：**
- 数据集：nuScenes（含OpenOcc、Occ3D-nuScenes、nuScenes-QA子集）
- 传感器配置：多视图相机 + LiDAR
- 评估模式：开环（open-loop）规划评估
- 模型规模：0.5B参数级别

**未验证的边界：**
- 纯视觉配置下的细粒度感知能力
- 闭环（closed-loop）驾驶场景中的规划鲁棒性
- 其他数据集/场景/传感器配置的泛化性
- 更大规模MLLM骨干（如3B、7B）下的性能上限

### 4. 局限与开放问题

**已知局限：**

1. **多任务损失平衡粗糙：** 当前采用均匀损失权重（$\lambda_1 = \lambda_2 = \lambda_3 = \lambda_4 = 1$）。消融实验（Table 7）显示，降低占位与流损失权重会损害3D感知性能，但略微提升规划与QA精度，表明任务间存在竞争关系，统一权重并非最优。

2. **闭环能力未验证：** 所有规划评估均在开环设置下进行，无法评估模型在闭环仿真器中的实际驾驶鲁棒性。

3. **数据引擎依赖外部大模型：** 空间推理QA对的生成依赖InternVL3-78B（基于Qwen2.5-72B），其标注质量与生成成本未量化分析，可能引入系统性偏差。

4. **传感器配置单一：** 实验仅基于nuScenes的多视图相机+LiDAR配置，纯视觉或不同传感器组合下的表现未知。

**开放问题：**

1. **自适应多任务损失平衡：** 如何设计动态损失权重策略（如基于不确定性加权或梯度协调），以进一步释放各任务潜力？

2. **闭环规划鲁棒性：** 在闭环仿真器中，DrivePI的规划性能（尤其是碰撞率和轨迹平滑性）如何？是否会出现开环-闭环的性能鸿沟？

3. **强化学习增强规划推理：** 引入RL能否提升复杂交互场景（如无保护左转、密集车流汇入）下的规划推理质量？

4. **跨传感器泛化：** 如何将DrivePI扩展到纯视觉配置，同时保持细粒度3D感知能力？LiDAR先验能否通过知识蒸馏等方式迁移？

5. **模型规模扩展：** 当MLLM骨干从0.5B扩展到3B或7B时，细粒度感知与语言理解能力如何变化？Table 8-9的隐藏层权重分析暗示深层表征对空间理解更关键，这一规律是否跨规模成立？

## 原文 PDF

![[paperPDFs/CVPR_2026/DrivePI_Spatial_aware_4D_MLLM_for_Unified_Autonomous_Driving_Understanding_Perception_Prediction_and_Planning.pdf]]
