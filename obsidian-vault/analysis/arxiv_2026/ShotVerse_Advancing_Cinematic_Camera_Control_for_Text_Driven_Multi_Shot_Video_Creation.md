---
title: "ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arXiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.pdf
project_link: null
code_link: https://github.com/LAION-AI/aesthetic-predictor
aliases:
- ShotVerse
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将对齐的 (Caption, Trajectory, Video) 三元组作为联合分布，并从中建模条件概率 P(Trajectory|Caption) 和 P(Video|Caption, Trajectory)，从而将任务解耦为自动规划和精确执行。
primary_logic: 通过构建对齐的数据三元组，可以利用预训练VLM的空间先验自动从文本生成电影级轨迹，并独立训练生成器以忠实执行这些轨迹，形成“先规划后控制”的范式。
claims:
- ShotVerse 在 Track B 中实现了最低的平移误差 0.0163 和旋转误差 0.73，以及最高的坐标系对齐得分 CAS 0.500。
- 消融实验表明，移除 4D RoPE 会导致镜头切换准确率从 0.933 急剧下降到 0.429。
- 用户研究和 VLM 评估均显示 ShotVerse 在运动类型恰当性、运动时长、主体强调与电影节奏四个维度上均优于所有基线。
- ShotVerse-Bench (Track A) 上 F1-Score↑ = 0.422
---

# ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation

> [!tip] 核心洞察
> 通过构建对齐的数据三元组，可以利用预训练VLM的空间先验自动从文本生成电影级轨迹，并独立训练生成器以忠实执行这些轨迹，形成“先规划后控制”的范式。

| 字段 | 内容 |
|------|------|
| 中文题名 | ShotVerse：推进文本驱动的多镜头视频创作中的电影镜头控制 |
| 英文题名 | ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.11421) · [paper](https://arxiv.org/) · [Code](https://github.com/LAION-AI/aesthetic-predictor) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ShotVerse |
| Dataset | ShotVerse-Bench |

> [!tip] 效果简介
> - ShotVerse-Bench (Track A) 上，F1-Score↑ 0.422 vs 0.343 (GenDoP) (+0.079)；CLaTr-CLIP↑ 35.016 vs 33.875 (GenDoP) (+1.141)。
> - ShotVerse-Bench (Track B) 上，Trans. Error↓ 0.0163 vs 0.0589 (ReCamMaster) (-0.0426)；Rotation Error↓ 0.73 vs 1.12 (ReCamMaster) (-0.39)；CAS↑ 0.500 vs 0.408 (ReCamMaster) (+0.092)。
> - ShotVerse-Bench (Track C) 上，Aesthetic Quality↑ 5.465 vs 4.981 (HoloCine) (+0.484)。

## 概要

文本驱动的视频生成模型近年来取得了显著进展，但在电影级多镜头创作中仍面临一个根本性瓶颈：**缺乏精确的相机控制**。现有方法要么依赖隐式文本提示来描述镜头运动，难以传达复杂的电影语言（如“环绕拍摄后快速推近”）；要么要求用户手工绘制显式轨迹，成本高昂且往往超出模型的能力范围，导致生成失败。这一困境的根源在于，文本、轨迹与视频三者之间缺乏对齐的联合建模——文本无法可靠地转化为轨迹，轨迹也无法被忠实地执行。

ShotVerse 针对上述瓶颈提出了 **“先规划后控制”（Plan-then-Control）** 的范式。其核心洞察是：通过构建对齐的 (Caption, Trajectory, Video) 三元组数据，可以将任务解耦为两个可独立优化的阶段——从文本自动规划电影级相机轨迹，再基于轨迹精确合成视频。这一设计将条件概率 $P(\text{Video} \mid \text{Caption})$ 分解为 $P(\text{Trajectory} \mid \text{Caption})$ 与 $P(\text{Video} \mid \text{Caption}, \text{Trajectory})$ 的联合建模，使自动规划与精确执行各司其职。

在方法层面，ShotVerse 的关键创新体现在三个维度。**第一，自动分层轨迹规划**：利用预训练视觉语言模型（VLM）的空间先验，将用户文本分解为全局描述与逐镜头描述，并自动生成上下文感知的相机轨迹，替代了传统的手工绘制或隐式提示。**第二，4D 位置编码**：将标准 3D RoPE（帧、高、宽）扩展为 4D RoPE（镜头、帧、高、宽），在注意力机制中显式建模多镜头的层次时空结构。**第三，真实电影数据基础**：构建了首个大规模多镜头电影级相机轨迹数据集 ShotVerse-Bench，通过标定管道将分立的单镜头轨迹对齐到统一全局坐标系，为模型训练提供了高质量的对齐三元组。

实验结果表明，ShotVerse 在三个评测轨道上均显著优于现有方法。在轨迹规划（Track A）中，F1-Score 达到 0.422，比最优基线 GenDoP 提升 0.079；在相机控制精度（Track B）中，平移误差降至 0.0163，旋转误差降至 0.73，坐标系对齐得分 CAS 达到 0.500，均大幅领先 ReCamMaster 等基线；在多镜头生成质量（Track C）中，美学质量得分 5.465，FVD 降至 281.71，镜头切换准确率达到 0.933。消融实验进一步揭示，4D RoPE 是镜头切换准确率的关键——移除后该指标从 0.933 骤降至 0.429；相机编码器则对主体朝向与视点一致性至关重要。

值得注意的是，ShotVerse 在以下方面仍存在局限：高密度人群动态场景的建模、长序列中重复视角的像素级场景持久性，以及向多场景、无限长度生成的能力拓展。这些方向构成了未来工作的开放挑战。



文本驱动的视频生成近年来取得了显著进展，以 Sora、VEO 等为代表的闭源模型和一系列开源工作，已能根据自然语言描述生成高质量的视频内容。然而，当创作场景从单镜头短视频扩展到多镜头的电影级叙事时，一个关键瓶颈逐渐凸显：**现有模型缺乏对相机运动的精确控制能力**。

在电影语言中，相机运动——推拉摇移、轨道环绕、镜头切换——不仅是技术手段，更是叙事语法。导演通过精心设计的相机轨迹来引导观众注意力、营造情绪氛围、建立空间关系。但在当前的文本驱动范式中，用户只能通过隐式的自然语言提示（如“镜头缓慢推进”）来间接传达拍摄意图。这种模糊的交互方式存在两个根本性缺陷：其一，文本难以精确描述复杂的电影级镜头语言，例如“从远景以弧形轨道绕主体半周，同时缓慢上摇”这样的复合运动；其二，即使提供了详尽的文本描述，模型也缺乏将语言指令映射为精确几何轨迹的内在机制。

针对这一困境，部分工作尝试引入显式的相机轨迹作为条件信号，如 **CameraCtrl**（He et al., arXiv 2024）和 **MotionCtrl**（Wang et al., SIGGRAPH 2024）等方法。这些方法虽然提升了控制的精度，却将高昂的设计成本转移到了用户端——用户需要手工绘制每一条相机轨迹，这对于包含多个镜头的完整叙事序列而言几乎不可行。更关键的是，手工设计的轨迹往往超出当前模型的能力边界，导致生成结果出现主体漂移、视角跳变等严重失效（见 Figure 3）。与此同时，**HoloCine**（Meng et al., arXiv 2025）、**MultiShotMaster**（Wang et al., arXiv 2025）等多镜头视频模型虽然支持镜头切换，但在面对“轨道环绕”等复杂相机指令时，生成的画面几乎保持静止，暴露出仅靠扩展文本密度无法实现精确几何控制的深层局限。

上述困境的根本原因在于：**文本-轨迹-视频三者之间缺乏对齐的数据基础**。现有的相机轨迹数据集（如 RealEstate10K、DL3DV）仅提供单镜头轨迹，且缺少与电影级语义描述的结构化关联。这意味着无论是训练轨迹规划器还是相机控制器，都缺乏一个能够桥接语言理解与几何执行的联合分布空间。

ShotVerse 正是在这一背景下提出的。其核心洞察是：如果将任务解耦为“先规划后控制”（Plan-then-Control）的范式，并构建对齐的 (Caption, Trajectory, Video) 三元组数据集作为基础，就可以利用预训练视觉语言模型（VLM）的空间先验，自动从文本生成电影级轨迹，再由独立的生成器忠实执行这些轨迹。这一思路将相机控制从“手工设计或隐式猜测”转变为“自动规划与精确执行”的工程化流程，为文本驱动的多镜头电影创作开辟了新的技术路径。



## 核心方法与创新机理

ShotVerse 的核心创新在于将多镜头相机控制任务解耦为“先规划后控制”的范式，并通过三个关键的技术槽位变更，系统性地解决了现有文本驱动视频生成模型在电影级相机控制上的瓶颈。

### 从隐式提示到显式分层轨迹的规划-控制解耦

现有方法（如 **CameraCtrl** (He et al., arXiv 2024)、**MotionCtrl** (Wang et al., SIGGRAPH 2024)）依赖隐式文本描述或繁重的手工轨迹绘制来实现相机控制。隐式描述难以传达复杂的电影级镜头语言（如“环绕主体并推进”），而手工绘制轨迹成本高昂且往往超出当前模型的能力范围，导致生成失败。

ShotVerse 的核心洞察在于将对齐的 (Caption, Trajectory, Video) 三元组视为联合分布，并从中建模两个条件概率：
- **Planner** 建模 $P(\text{Trajectory} \mid \text{Caption})$，利用预训练 VLM 的空间先验，自动从分层文本描述生成电影级、全局统一的相机轨迹；
- **Controller** 建模 $P(\text{Video} \mid \text{Caption}, \text{Trajectory})$，通过相机编码器将显式轨迹精确注入生成过程。

这种“先规划后控制”的解耦设计，使得轨迹规划可以充分利用 VLM 的语义理解能力，而视频生成则可以专注于忠实执行轨迹，避免了单阶段模型中规划与控制相互干扰的问题。

### 4D RoPE：多镜头时空结构的层次化建模

多镜头视频的本质特征是镜头间的切换与连续，但现有方法普遍采用标准 3D RoPE（帧, 高, 宽），将不同镜头视为孤立的时空片段，无法建模镜头间的时序关系。

ShotVerse 提出了 **4D RoPE** 位置编码，将注意力维度显式划分为四个子空间：
$$d_h \gets \lfloor d/3 \rfloor, \quad d_w \gets \lfloor d/3 \rfloor, \quad d_{shot} \gets \lfloor (d - d_h - d_w)/2 \rfloor, \quad d_{frame} \gets \lfloor (d - d_h - d_w)/2 \rfloor$$

通过在注意力中加入镜头和帧两个独立的时间维度，4D RoPE 能够编码多镜头的层次化时空结构，使模型感知镜头边界并保持镜头间的时序一致性。消融实验（Table 7）表明，将 4D RoPE 替换为 3D RoPE 会导致镜头切换准确率从 0.933 急剧下降到 0.429，充分验证了该设计对多镜头结构的建模能力。

### 真实电影多镜头数据与全局标定

现有相机轨迹数据集多为单镜头或合成数据，缺乏真实电影的多镜头结构和丰富的文本标注。ShotVerse 构建了 **ShotVerse-Bench**，包含 20,500 个来自高制作价值电影的多镜头片段，并提出了多镜头相机标定管道，将分立的单镜头轨迹对齐到统一的全局坐标系统。

这一数据基础的变更带来了双重收益：
1. **Planner 训练**：真实电影数据中的分层描述（全局描述 + 逐镜头描述）与对应的相机轨迹，使 VLM 能够学习电影级镜头语言的语义-几何映射；
2. **Controller 训练**：全局标定后的轨迹确保了跨镜头运动的一致性，消融实验（Table 7, Fig. 4(d)）显示，移除标定会导致相机/轨迹在镜头间失去全局对齐，造成主体跟踪不准确；使用合成数据训练则使美学质量从 5.465 显著下降至 4.833，并削弱真实感。

### 创新点的协同效应

三个 changed slots 并非孤立存在，而是形成了递进的协同关系：真实电影数据提供了学习电影镜头语言的基础，4D RoPE 为多镜头结构提供了正确的时空归纳偏置，而规划-控制解耦则使得 VLM 的空间推理能力与扩散模型的生成能力可以各司其职。这种系统性的设计使得 ShotVerse 在 Track B 中实现了最低的平移误差 0.0163 和旋转误差 0.73，以及在 Track A 中 F1-Score 达到 0.422，均显著优于各赛道的最强基线。



ShotVerse 提出“先规划后控制”（Plan-then-Control）范式，将文本驱动的多镜头电影级相机控制解耦为两个协作阶段：**轨迹规划**与**轨迹执行**。这一解耦的核心洞察在于，现有文本驱动视频生成模型之所以难以实现精确的相机控制，根源在于隐式文本提示无法可靠地传达复杂的电影镜头语言，而显式轨迹条件又面临高昂的手工设计成本。ShotVerse 通过构建对齐的 (Caption, Trajectory, Video) 三元组，将问题形式化为两个条件概率的建模：Planner 学习 $P(\text{Trajectory} \mid \text{Caption})$，Controller 学习 $P(\text{Video} \mid \text{Caption}, \text{Trajectory})$。

### 整体数据流

框架的输入端是用户提供的分层文本描述，包含全局场景描述和逐镜头的电影指令。输出端是一段完整的多镜头视频，其相机运动严格遵循规划出的轨迹。整个 pipeline 按以下顺序流转（参见 Figure 2）：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2603_11421/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. (i) Dataset Curation. We construct the ShotVerse-Bench by aligning multi-shot trajectories into a unified global coordinate system via camera calibration, paired with hierarchical global and per-shot captions. (ii) Trajectory Plotting: The Planner utilizes a VLM to process the hierarchical prompt interleaved with learnable trajectory query tokens. These inputs are encoded into context-aware embeddings and transformed into explicit camera poses via a Trajectory Decoder and a Pose De-Tokenizer. (iii) Trajectory Injection: The Controller synthesizes high-fidelity videos using a holistic DiT backbone. It precisely follows the trajectories via a Camera Adapter and a 4D Rotary Po...*

1. **分层提示构建器** 将用户文本分解为全局提示 $\mathcal{X}_{global}$ 和 $K$ 个逐镜头提示 $\mathcal{X}_{shot}^{(k)}$，并与 $M$ 个可学习的轨迹查询令牌 `<TRAJ>` 交织，形成 VLM 的输入序列：
   $$\mathbf{I}_{in} = \mathrm{Tok}(\mathcal{X}_{global}) \oplus \bigoplus_{k=1}^{K} \left( \mathrm{Tok}(\mathcal{X}_{shot}^{(k)}) \oplus [<\mathrm{TRAJ}>_{1}^{(k)}, \dots, <\mathrm{TRAJ}>_{M}^{(k)}] \right)$$

2. **Planner VLM 编码器**（基于 Qwen3-VL-2B 预训练视觉语言模型）处理该序列，利用其空间先验将分层提示编码为上下文感知的相机码 $\mathbf{H}_{plan}^{(k)} \in \mathbb{R}^{M \times D_{vlm}}$。各镜头的相机码通过可学习的 `<SEP>` 令牌拼接，以支持跨镜头的联合时序建模。

3. **轨迹解码器**（基于 OPT 架构的自回归 Transformer，12 层）将固定长度的相机码扩展为变长的离散轨迹令牌序列 $\mathbf{S}_{traj}$，通过 Nucleus 采样（$\tau=0.9, p=0.95$）生成。

4. **姿态去令牌化器** 将离散令牌映射回连续的相机外参矩阵，形成显式的、全局对齐的电影级轨迹。

5. **相机编码器** 将外参矩阵展平后注入扩散 Transformer（DiT）的每个注意力块，在自注意力计算前与归一化后的特征相加：$\mathbf{F}_{attn}^{in} = \mathbf{F}_{norm} + \mathbf{c}_{cam}$。

6. **4D RoPE 位置编码** 将注意力维度划分为镜头、帧、高、宽四个子空间：
   $$d_h \gets \lfloor d/3 \rfloor,\ d_w \gets \lfloor d/3 \rfloor,\ d_{shot} \gets \lfloor (d - d_h - d_w)/2 \rfloor,\ d_{frame} \gets \lfloor (d - d_h - d_w)/2 \rfloor$$
   以此在注意力机制中显式编码多镜头的层次化时空结构。

7. **HoloCine 多镜头视频主干**（基于 DiT 的整体式生成模型）通过 Flow Matching 训练，在文本条件 $\mathbf{c}_{text}$ 和相机条件 $\mathbf{c}_{cam}$ 的共同引导下合成最终视频：
   $$\mathcal{L}_{control} = \mathbb{E}_{\sigma, \mathbf{v}_0, \mathbf{v}_1} [|| v_\theta(\mathbf{v}_\sigma, \sigma, \mathbf{c}_{text}, \mathbf{c}_{cam}) - (\mathbf{v}_1 - \mathbf{v}_0) ||_2^2]$$

### 关键模块关系

Planner 与 Controller 之间形成松耦合的协作关系：Planner 的输出是显式的相机轨迹，作为 Controller 的条件输入。这种解耦带来的关键优势是，Planner 可以独立利用预训练 VLM 的空间推理能力从文本自动生成电影级轨迹，而 Controller 则专注于忠实执行这些轨迹。消融实验证实了这一设计的必要性：移除 VLM 编码器（改用浅层文本编码器）导致 F1-Score 从 0.422 降至 0.343（Table 6）；移除相机编码器则使平移误差从 0.0163 上升至 0.0609，旋转误差从 0.73 升至 1.27（Table 7）。4D RoPE 的作用同样关键——将其替换为标准 3D RoPE 会导致镜头切换准确率从 0.933 急剧下降到 0.429（Table 7），说明显式的镜头维度建模对于多镜头时空一致性至关重要。

整个框架建立在 ShotVerse-Bench 数据集之上，该数据集通过多镜头相机标定管道将分立的单镜头轨迹对齐到统一全局坐标系，为 Planner 和 Controller 提供了对齐的三元组训练基础。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2603_11421/figures/001_Figure_1.jpg]]
*Figure 1: Cinematic, Camera-Controlled, Multi-Shot Video Creation via our ShotVerse Framework. (i) Multi-Shot Data Foundation: We curate ShotVerse-Bench dataset from high-production cinema and propose a novel calibration pipeline that aligns disjoint shot trajectories into a unified global coordinate system. (ii) “Plan-then-Control” Framework: A VLM-based Planner automates the plotting of explicit, unified, cinematic trajectories from prompts, which serve as precise guidance for the Controller to synthesize content. (iii) Superior Performance: Examples demonstrate high-fidelity and great camera-controlled generation across diverse genres. The inset 3D plots visualize the plotted explicit trajectories*



ShotVerse 将多镜头相机控制任务解耦为规划与控制两个阶段，核心模块可归纳为四个部分：分层提示构建、Planner 轨迹规划、Controller 轨迹注入、以及 4D RoPE 时空建模。

### 分层提示构建器

该模块将用户文本分解为全局描述与逐镜头描述，并与可学习的轨迹查询令牌交织，形成 VLM 的输入序列。其构建方式如公式所示：

$$
\mathbf{I}_{in} = \mathrm{Tok}(\mathcal{X}_{global}) \oplus \bigoplus_{k=1}^{K} \left( \mathrm{Tok}(\mathcal{X}_{shot}^{(k)}) \oplus [<\mathrm{TRAJ}>_{1}^{(k)}, \dots, <\mathrm{TRAJ}>_{M}^{(k)}] \right)
$$

其中 $\mathcal{X}_{global}$ 为全局场景描述，$\mathcal{X}_{shot}^{(k)}$ 为第 $k$ 个镜头的描述，$<\mathrm{TRAJ}>_{m}^{(k)}$ 为可学习的轨迹查询令牌，$K$ 为镜头总数，$M$ 为每镜头的查询令牌数。该结构使 VLM 能够在全局语境下理解每个镜头的语义需求。

### Planner：从文本到显式轨迹

Planner 建模条件概率 $P(\text{Trajectory} \mid \text{Caption})$，将分层提示转化为显式相机轨迹。其流水线包含三个子模块：

**VLM 编码器** 采用 Qwen3-VL-2B 作为骨干网络，处理上述分层输入序列后，提取每个镜头对应查询令牌的末层隐藏状态作为相机码：

$$
\mathbf{H}_{plan}^{(k)} \in \mathbb{R}^{M \times D_{vlm}}
$$

不同镜头的相机码通过可学习分隔符令牌拼接，形成联合序列以建模镜头间的时间依赖：

$$
\mathbf{H}_{plan} = \left[ \mathbf{H}_{plan}^{(1)} ; \mathrm{<SEP>} ; \mathbf{H}_{plan}^{(2)} ; \mathrm{<SEP>} ; \ldots ; \mathrm{<SEP>} ; \mathbf{H}_{plan}^{(K)} \right]
$$

**轨迹解码器** 基于 OPT 架构的自回归 Transformer（12 层），将固定长度的相机码扩展为变长的离散轨迹令牌序列 $\mathbf{S}_{traj}$。推理时采用 Nucleus 采样（$\tau=0.9, p=0.95$）。

**姿态去令牌化器** 将离散令牌映射回连续的相机外参参数（平移向量与旋转四元数），输出可直接用于 Controller 的显式轨迹。

Planner 的训练目标为：

$$
\mathcal{L}_{plan} = \mathrm{CrossEntropy}(\mathbf{S}_{traj}, \hat{\mathbf{S}}_{traj}) + \lambda \| \mathbf{H}_{plan} \|_{2}^{2}
$$

第一项最大化轨迹令牌的似然，第二项通过 L2 正则化约束相机码的幅度，防止过拟合。

### Controller：轨迹条件视频生成

Controller 建模条件概率 $P(\text{Video} \mid \text{Caption}, \text{Trajectory})$，基于 Flow Matching 范式训练。其核心组件为：

**相机编码器** 将相机外参矩阵展平后，通过线性投影注入扩散 Transformer 的每个块中，与归一化后的特征相加：

$$
\mathbf{F}_{attn}^{in} = \mathbf{F}_{norm} + \mathbf{c}_{cam}
$$

该设计使每个 Transformer 层都能直接感知当前帧的相机位姿，实现精确的视点控制。

**训练目标** 为 Flow Matching 损失，模型预测从干净视频 $\mathbf{v}_1$ 到噪声 $\mathbf{v}_0$ 的速度场：

$$
\mathcal{L}_{control} = \mathbb{E}_{\sigma, \mathbf{v}_0, \mathbf{v}_1} \left[ \| v_\theta(\mathbf{v}_\sigma, \sigma, \mathbf{c}_{text}, \mathbf{c}_{cam}) - (\mathbf{v}_1 - \mathbf{v}_0) \|_2^2 \right]
$$

其中 $\sigma$ 为时间步，$\mathbf{v}_\sigma$ 为加噪后的视频潜变量，$\mathbf{c}_{text}$ 和 $\mathbf{c}_{cam}$ 分别为文本条件与相机条件嵌入。

### 4D RoPE：多镜头时空位置编码

为建模多镜头的层次化时空结构，ShotVerse 将标准 3D RoPE（帧、高、宽）扩展为 4D RoPE（镜头、帧、高、宽）。注意力维度按如下规则分配：

$$
d_h \gets \lfloor d/3 \rfloor, \quad d_w \gets \lfloor d/3 \rfloor, \quad d_{shot} \gets \lfloor (d - d_h - d_w)/2 \rfloor, \quad d_{frame} \gets \lfloor (d - d_h - d_w)/2 \rfloor
$$

其中 $d$ 为注意力头总维度，$d_{shot}$、$d_{frame}$、$d_h$、$d_w$ 分别分配给镜头索引、帧索引、高度位置和宽度位置的旋转编码子空间。该设计使模型能够区分不同镜头内的时空位置，是实现镜头切换一致性的关键——消融实验表明，移除 4D RoPE 会导致镜头切换准确率从 0.933 骤降至 0.429（Table 7）。

### 模块间协作机制

上述模块形成“先规划后控制”的完整闭环：分层提示构建器将用户意图结构化，Planner 利用 VLM 的空间先验自动生成全局对齐的电影级轨迹，Controller 通过相机编码器和 4D RoPE 精确执行该轨迹。训练时 Planner 与 Controller 独立优化，推理时 Planner 的输出直接作为 Controller 的条件输入，无需人工干预即可完成从文本到多镜头可控视频的端到端生成。



## 实验与关键发现

### 实验设置与评估协议

ShotVerse 的实验评估围绕三个核心赛道（Track A/B/C）展开，分别检验文本-轨迹对齐、相机控制精度与多镜头视频质量。所有实验均基于 **ShotVerse-Bench** 数据集——首个大规模多镜头电影级相机轨迹数据集，包含 20.5K 个来自高制作价值电影的片段，配有 19,819 词汇量的分层标注（Table 1）。评估的公平性通过以下措施保证：所有轨迹规划器接收相同的分层提示输入；对于单镜头基线方法，分别对每个镜头应用后使用本研究的标定管道对齐以模拟多镜头场景；闭源模型仅接收分层提示以测试其零样本电影级理解能力；用户研究遵循统一提示和预定义标准。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2603_11421/figures/003_Table_1.jpg]]
*Table 1: Comparisons of Camera Trajectory Datasets. ShotVerse-Bench is the first large-scale dataset that provides multi-shot cinematic camera trajectories together with rich, multi-level caption annotations*

**轨迹规划器（Planner）** 集成 Qwen3-VL-2B 作为骨干网络，搭配基于 OPT 的解码器（12 层），使用 LoRA（r=32）进行微调，轨迹采用离散令牌化（码本大小 B=256），推理时采用 Nucleus 采样（τ=0.9, p=0.95）。

### 主实验结果

#### Track A：文本-轨迹对齐

Table 2 展示了文本提示与生成轨迹之间的对齐质量。ShotVerse 在 ShotVerse-Bench 上取得了最高的 **F1-Score 0.422**，优于最强基线 **GenDoP**（Zhang et al., arXiv 2025）的 0.343（+0.079）。在 CLaTr-CLIP 指标上，ShotVerse 达到 **35.016**，同样领先 GenDoP 的 33.875（+1.141）。这一优势源于 Planner 中 VLM 编码器对分层提示的深层语义理解——消融实验（Table 6）证实，将 VLM 编码器替换为浅层文本编码器会导致 F1-Score 降至 0.343、CLaTr-CLIP 降至 33.875，直接退化为 GenDoP 级别性能。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2603_11421/figures/005_Table_2.jpg]]
*Table 2: Track A: Quantitative Evaluation of Text-Trajectory Alignment*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2603_11421/figures/009_Table_6.jpg]]
*Table 6: Quantitative Evaluation of Ablation Study (Planner)*

#### Track B：相机控制精度

Table 3 报告了在给定真实轨迹条件下各方法的相机控制精度。ShotVerse 在所有指标上均取得最优：**平移误差 0.0163**（对比 ReCamMaster 的 0.0589，降低 72.3%），**旋转误差 0.73**（对比 ReCamMaster 的 1.12，降低 34.8%），**坐标系对齐得分 CAS 0.500**（对比 ReCamMaster 的 0.408，提升 22.5%）。这一决定性优势来自 Camera Encoder 将外参矩阵精确注入扩散 Transformer 块的设计——消融实验（Table 7）表明，移除 Camera Encoder 后平移误差飙升至 0.0609、旋转误差升至 1.27，系统退化为 HoloCine 的基线水平。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2603_11421/figures/006_Table_3.jpg]]
*Table 3: Track B: Quantitative Evaluation of Camera Control. All methods receive ground-truth trajectories*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2603_11421/figures/010_Table_7.jpg]]
*Table 7: Quantitative Evaluation of Ablation Study (Controller)*

Figure 3 的定性对比进一步揭示了纯文本驱动方法的根本局限：**CameraCtrl**（He et al., arXiv 2024）和 **MotionCtrl**（Wang et al., SIGGRAPH 2024）等早期相机控制模型无法处理复杂的电影级轨迹；**ReCamMaster** 虽能执行轨迹，但在镜头 1 中偏离了主体；**HoloCine**（Meng et al., arXiv 2025）、**MultiShotMaster**（Wang et al., arXiv 2025）以及闭源模型 **Sora2**（OpenAI, 2025）、**VEO3**（Google DeepMind, 2025）、**Kling3.0**（Kuaishou, 2025）、**Seedance2.0**（Gao et al., arXiv 2025）均无法执行复杂的“环绕”指令，几乎保持静止。这些失败表明，仅靠扩展文本密度无法实现精确控制，显式几何引导不可或缺。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2603_11421/figures/004_Figure_3.jpg]]
*Figure 3: Comparisons with the State-of-the-Art Baseline Methods. Early camera-controlled text-driven generation models (e.g. , CameraCtrl, MotionCtrl) struggle to handle complex cinematic camera trajectories. ReCamMaster executes the trajectory but drifts away from the subject in Shot 1. HoloCine, MultiShotMaster, Sora2, VEO3, and Kling3.0, and Seedance2.0 fail to execute the complex “orbit” command, remaining nearly static. These failures demonstrate that for text-driven models, scaling up caption density is insufficient to achieve precise control without explicit geometric guidance*

#### Track C：多镜头视频质量

Table 4 展示了端到端多镜头视频生成质量。ShotVerse 在美学质量上达到 **5.465**，显著超越 HoloCine 的 4.981（+0.484）；FVD 降至 **281.71**，相比 HoloCine 的 407.54 大幅降低 125.83。在镜头切换准确率上，ShotVerse 达到 **0.933**，略高于 MultiShotMaster 的 0.927（+0.006）。值得注意的是，Table 5 的 VLM 评估和用户研究在运动类型恰当性、运动时长、主体强调与电影节奏四个维度上均显示 ShotVerse 全面优于所有基线，验证了“先规划后控制”范式在电影级质量上的综合优势。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2603_11421/figures/007_Table_4.jpg]]
*Table 4: Track C: Quantitative Evaluation of Multi-Shot Quality. Without shot-splitting, shot metrics cannot be calculated for some baselines*

### 消融实验

#### Planner 消融（Table 6）

移除 VLM 编码器导致 F1-Score 从 0.422 降至 0.343，CLaTr-CLIP 从 35.016 降至 33.875，证实 VLM 的空间先验对轨迹规划至关重要。其他设计选择（如分层提示结构、轨迹令牌化策略）的消融结果进一步支持了 Planner 架构的合理性。

#### Controller 消融（Table 7, Figure 4）

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2603_11421/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative Ablation Study. (a) Camera encoder is vital for viewpoint grounding; without it, the model fails to maintain subject orientation (e.g., frontal faces). (b) High-noise pose injection already establishes the global motion scaffold, while adding low-noise injection yields marginal gains. (c) 4D RoPE ensures better shot-cutting stability over 3D RoPE. (d) Without calibration, the camera/trajectory is not globally aligned across shots, causing inaccurate subject tracking. (e) Training on synthetic triplets further makes both the character and the environment look synthetic, and the domain gap to real videos degrades visual quality and temporal stability*

- **Camera Encoder**（Figure 4a）：移除后模型无法维持主体朝向（如面部始终面向镜头），平移误差升至 0.0609，旋转误差升至 1.27，美学质量降至 4.981，证明相机编码器对视角锚定不可或缺。
- **4D RoPE**（Figure 4c）：将 4D RoPE 替换为标准 3D RoPE 导致镜头切换准确率从 0.933 急剧下降至 0.429，降幅超过 54%。这是最关键的消融发现——4D RoPE 在注意力中显式编码镜头维度是多镜头时空结构建模的核心机制。
- **标定管道**（Figure 4d）：移除多镜头相机标定后，各镜头轨迹无法对齐到统一全局坐标系，导致主体跟踪失准。
- **数据域**（Figure 4e）：使用合成数据训练导致美学质量降至 4.833，角色和环境均呈现合成感，真实感显著削弱，验证了真实电影数据对视觉质量的不可替代性。

### 失败模式与局限性

尽管 ShotVerse 在定量和定性评估中均表现优异，论文明确指出了三类失败模式：

1. **高密度人群动态场景**：模型尚无法精确建模复杂群体运动，在人群密集场景中可能出现运动失真。
2. **长序列场景持久性**：对于长序列中重复视角的像素级场景一致性仍是一项开放挑战，重新访问同一视点时画面可能出现不一致。
3. **单场景限制**：当前方法仅限单个场景内的多镜头生成，尚未拓展至多场景、无限长度的整体可控生成。

这些局限性指向了未来研究的关键方向：长时间跨度的精确场景持久性、多场景叙事演进与连续相机运动的统一控制，以及显式相机控制与复杂叙事结构（如对话、动作序列）的深度融合。



## 定位与知识库关联

### 1. 核心范式定位：“先规划后控制”的解耦框架

ShotVerse 将多镜头电影级视频生成任务形式化为对联合分布 $P(\text{Caption}, \text{Trajectory}, \text{Video})$ 的建模，并通过条件分解将其解耦为两个阶段：轨迹规划 $P(\text{Trajectory} \mid \text{Caption})$ 和轨迹条件生成 $P(\text{Video} \mid \text{Caption}, \text{Trajectory})$。这一“先规划后控制”（Plan-then-Control）范式从根本上区别于现有的文本驱动相机控制方法。

传统方法面临一个核心瓶颈：隐式文本提示难以精确传达复杂的电影级镜头语言（如“先推轨后环绕”），而显式轨迹条件则需要高昂的手工设计成本，且往往超出当前模型的能力范围。ShotVerse 的因果调控机制在于，通过构建对齐的（Caption, Trajectory, Video）三元组作为数据基础，利用预训练视觉语言模型（VLM）的空间先验自动从文本生成电影级轨迹，并独立训练生成器以忠实执行这些轨迹，从而将“理解镜头意图”与“执行相机运动”这两个子任务分别优化。

### 2. 与基线方法的关系图谱

ShotVerse 在三个评价轨道（Track）上与现有方法进行了系统性对比，其方法定位可以从以下维度加以理解。

#### 2.1 轨迹规划器（Track A）：从隐式提示到显式几何推理

在文本到轨迹的生成任务中，ShotVerse 的 Planner 模块与四类基线形成对比：

- **CCD**（Jiang et al., CGF 2024）：早期基于规则的轨迹生成方法，缺乏对复杂文本语义的泛化能力。
- **Director3D**（Li et al., NeurIPS 2024）：将 3D 场景表示引入轨迹规划，但依赖显式 3D 重建，限制了其在大规模真实视频数据上的应用。
- **GenDoP**（Zhang et al., arXiv 2025）：当前最强的文本-轨迹对齐基线，采用自回归轨迹生成，但缺乏对多镜头层次结构的显式建模。
- **E.T.**：具体方法细节需手动核实，论文中未提供完整引用信息。

ShotVerse Planner 的核心改进在于**分层提示构建**与**VLM 编码器的引入**。通过将用户文本分解为全局描述和逐镜头描述，并插入可学习的轨迹查询令牌（Eq. 1），Planner 能够利用 Qwen3-VL-2B 的预训练空间先验，将文本语义映射为上下文感知的相机码。消融实验（Table 6）证实了 VLM 编码器的关键作用：将其替换为浅层文本编码器后，F1-Score 从 0.422 降至 0.343，CLaTr-CLIP 从 35.016 降至 33.875，性能退化为与 GenDoP 相当的水平。

#### 2.2 相机控制生成（Track B）：从单镜头轨迹到全局统一坐标

在给定真实轨迹的条件下，ShotVerse Controller 与以下方法对比：

- **CameraCtrl**（He et al., arXiv 2024）与 **MotionCtrl**（Wang et al., SIGGRAPH 2024）：早期的相机控制方法，通过将相机参数注入扩散模型实现轨迹条件生成，但难以处理复杂的电影级运动（如多圈环绕），在定性对比中（Figure 3）表现为几乎静止。
- **ReCamMaster**：当前最强的相机控制基线，能够执行轨迹但在多镜头场景中容易出现主体漂移（Shot 1 中偏离主体）。

ShotVerse 在 Track B 中实现了最低的平移误差 0.0163（ReCamMaster 为 0.0589）、旋转误差 0.73（ReCamMaster 为 1.12），以及最高的坐标系对齐得分 CAS 0.500（ReCamMaster 为 0.408）（Table 3）。这一优势源于两个关键设计：

1. **相机编码器**：将相机外参矩阵展平后注入每个 DiT Transformer 块的自注意力层之前，实现精确的逐帧轨迹条件控制。消融实验（Table 7）表明，移除相机编码器后平移误差飙升至 0.0609，旋转误差升至 1.27。
2. **4D RoPE 位置编码**：在标准 3D RoPE（帧、高、宽）的基础上增加镜头维度，将注意力维度分配为 $d_{shot}$、$d_{frame}$、$d_h$、$d_w$ 四个子空间（Algorithm 1），以编码多镜头层次结构。这一设计对镜头切换准确率至关重要：替换为 3D RoPE 后，镜头切换准确率从 0.933 急剧下降至 0.429（Table 7）。

#### 2.3 多镜头视频生成（Track C）：从单镜头拼接到整体式生成

在多镜头视频质量评估中，ShotVerse 与以下方法对比：

- **HoloCine**（Meng et al., arXiv 2025）：整体式多镜头视频生成模型，作为 ShotVerse 的生成主干。ShotVerse 在其基础上增加了相机编码器和 4D RoPE，使美学质量从 4.981 提升至 5.465，FVD 从 407.54 降至 281.71（Table 4）。
- **MultiShotMaster**（Wang et al., arXiv 2025）：多镜头视频模型，镜头切换准确率为 0.927，ShotVerse 以 0.933 略胜一筹。
- **Sora2**（OpenAI, 2025）、**VEO3**（Google DeepMind, 2025）、**Kling3.0**（Kuaishou, 2025）、**Seedance2.0**（Gao et al., arXiv 2025）：闭源商业模型，仅通过分层提示进行零样本评估。定性结果（Figure 3）显示，这些模型在复杂相机指令（如“环绕”）下几乎保持静态，表明仅靠扩大文本描述密度无法替代显式几何引导。

### 3. 数据基础的范式性贡献

ShotVerse 的方法有效性建立在 **ShotVerse-Bench** 数据集之上。如表 1 所示，该数据集是首个大规模多镜头电影级相机轨迹数据集，包含 20,500 个来自高制作水准电影的片段，并配有多层次文本标注（词汇量 19,819）。其关键创新在于**多镜头相机标定管道**（Algorithm 2），能够将分立的单镜头轨迹对齐到统一的全局坐标系，从而为 Planner 的全局轨迹规划和 Controller 的跨镜头一致性提供监督信号。

消融实验（Table 7）揭示了真实数据的关键作用：使用合成数据训练导致美学质量显著下降至 4.833，并使人物和环境呈现“合成感”（Figure 4e），验证了真实电影数据域对于生成质量的不可替代性。

### 4. 适用边界与失效模式

尽管 ShotVerse 在多个维度上取得了显著提升，其方法仍存在明确的适用边界：

1. **高密度人群动态场景**：模型尚无法精确建模复杂群体运动，这限制了其在战争场面、大型集会等电影场景中的应用。这一失效模式可能源于训练数据中此类场景的稀疏性，以及当前 DiT 架构对细粒度多主体运动的建模能力不足。

2. **长序列中的场景持久性**：对于重复视角的像素级场景一致性仍是一项开放挑战。当镜头在长序列中重新访问同一视点时，画面可能无法保持完全一致，这限制了其在需要精确空间记忆的叙事场景中的应用。

3. **单场景约束**：当前方法仅限单个场景内的多镜头生成，尚未拓展至多场景、无限长度的整体可控生成。这意味着尚无法处理包含场景转换的完整故事线。

### 5. 开放问题与未来方向

基于上述局限，ShotVerse 框架指出了以下开放研究方向：

1. **长时间场景持久性**：如何实现长时间跨度内的精确场景持久性，使得在重新访问同一视点时画面保持一致？这可能需要引入显式的场景记忆模块或 3D 表示。

2. **多场景无限长度生成**：如何将整体可控性扩展到多场景、无限长度的多镜头生成，同时处理故事线演进与连续相机运动？这需要将当前的单场景框架拓展为场景感知的层次化生成架构。

3. **叙事级导演控制**：如何将显式相机控制与更复杂的叙事结构（如对话、动作序列）深度融合，实现更高层次的导演级创作？这要求将相机控制从纯几何层面提升到语义叙事层面，与角色行为、剧情节奏形成协同。



## 原文 PDF

![[paperPDFs/arXiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.pdf]]
