---
title: "GeoPredict: Leveraging Predictive Kinematics and 3D Gaussian Geometry for Precise VLA Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GeoPredict_Leveraging_Predictive_Kinematics_and_3D_Gaussian_Geometry_for_Precise_VLA_Manipulation.pdf
project_link: "https://jingjingqian75.github.io/GeoPredict-Page/"
code_link: null
aliases:
- GeoPredict
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过训练时引入预测性机器人关键点轨迹和3D高斯几何模块，为策略提供未来运动学先验和空间几何先验，增强3D推理能力。
primary_logic: 仅在训练阶段利用未来深度渲染监督来学习预测性3D表示，推理时不增加额外3D解码开销，即可显著提升VLA策略的3D感知和长时域规划能力。
claims:
- 加入历史轨迹编码器使成功率从42.3%提升至44.8%，验证运动学先验的有效性。
- 未来轨迹预测查询进一步将成功率提升至47.2%，表明显式预测未来运动的重要性。
- 联合训练深度损失（无轨迹引导细化）达到50.5%，而启用完整轨迹引导细化机制达到最高52.4%，证明自适应几何容量分配的关键作用。
- RoboCasa Human-50 上 Average Success Rate = 52.4%
---

# GeoPredict: Leveraging Predictive Kinematics and 3D Gaussian Geometry for Precise VLA Manipulation

> [!tip] 核心洞察
> 仅在训练阶段利用未来深度渲染监督来学习预测性3D表示，推理时不增加额外3D解码开销，即可显著提升VLA策略的3D感知和长时域规划能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeoPredict: 利用预测运动学与3D高斯几何实现精确VLA操控 |
| 英文题名 | GeoPredict: Leveraging Predictive Kinematics and 3D Gaussian Geometry for Precise VLA Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.16811) · [Project](https://jingjingqian75.github.io/GeoPredict-Page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GeoPredict |
| Dataset | RoboCasa Human-50, LIBERO, LIBERO-Long, Real-World |

> [!tip] 效果简介
> - RoboCasa Human-50 上，Average Success Rate 52.4% vs 42.3% (π0) (+10.1%)。
> - LIBERO (4 suites average) 上，Average Success Rate 96.5% vs 76.5% (OpenVLA, 20.0% gap) / SOTA UniVLA (+20.0% over OpenVLA)。
> - LIBERO-Long 上，LIBERO-Long Success Rate 94.0%。

## 概要

当前视觉-语言-动作（VLA）模型在机器人操控任务中主要依赖2D图像和瞬时观测，缺乏对3D空间关系与未来动态的预测能力，导致在需要精确3D推理的操控场景中表现不佳。GeoPredict 针对这一瓶颈，提出了一种几何感知的VLA框架，通过在训练阶段引入**预测性运动学先验**和**3D高斯几何先验**来增强策略的3D推理能力，而推理时不增加任何额外的3D解码开销。

GeoPredict 的核心思路是“以预测促感知”：模型联合学习未来机器人关键点的3D轨迹和未来场景的3D高斯几何表示，并将这些预测作为先验条件融入动作生成。具体而言，**轨迹预测模块**编码历史关键点运动并显式预测多步未来轨迹，为策略提供运动学先验；**3D几何预测模块**通过空间查询和体素解码器预测未来工作空间的深度渲染，并利用轨迹引导的细化机制在任务相关区域自适应分配几何容量。两个预测模块仅在训练时作为监督信号使用，推理阶段动作生成流程与标准VLA策略一致，保持了部署效率。

在实验验证上，GeoPredict 在多个基准上展现出显著优势。在 **RoboCasa Human-50** 仿真基准上，GeoPredict 平均成功率达到 **52.4%**，较基础VLA模型 π0 的 42.3% 提升 **+10.1%**；在 **LIBERO** 四个评估套件上平均成功率达 **96.5%**，比 OpenVLA 高出 **20.0%**；在真实世界实验中，Geometry 和 Robustness 场景下分别以 **95.0%** 和 **90.0%** 的成功率大幅领先 π0 的 50.0% 和 35.0%，充分验证了预测性几何先验在精确操控任务中的关键作用。

消融实验进一步揭示了各组件的因果贡献：仅添加历史轨迹编码器使成功率从 42.3% 提升至 44.8%，加入未来轨迹预测损失后提升至 47.2%，联合深度监督达到 50.5%，而启用完整的轨迹引导细化机制后达到最高的 **52.4%**，证明自适应几何容量分配是性能提升的核心机制。



视觉-语言-动作（VLA）模型近年来在机器人操控领域取得了显著进展，但其核心能力仍受限于对2D图像和瞬时观测的依赖。当前主流VLA模型，如**π0**（连续动作流匹配）和**OpenVLA**（Kim et al., CoRL 2025，基于离散动作token），主要从当前时刻的多视角RGB图像中提取特征来生成动作指令。这种设计在需要精确3D空间推理的操控任务中暴露出根本性缺陷：模型缺乏对三维空间关系的深层理解，也无法预判机器人运动与环境交互的未来动态。

具体而言，现有VLA方法面临两个关键缺口。第一，**运动学先验缺失**：模型仅从单帧视觉输入推断动作，无法利用机器人关键点的运动历史来捕捉运动趋势，导致在需要精确轨迹规划的接触式操作中表现不稳定。第二，**几何先验缺失**：2D视觉编码器无法显式建模工作空间的三维几何结构，使得模型难以推理空间占据、遮挡关系和精细的物体位姿——这些恰是抓取、插入、对准等操控原语的核心需求。尽管**SpatialVLA**（Qu et al., arXiv 2025）等近期工作尝试显式集成3D信息，但现有方法普遍未将运动预测与几何推理统一在端到端框架中，且在推理时引入额外3D解码会带来显著的计算开销。

上述瓶颈在仿真和真实世界基准中均有明确体现。在RoboCasa Human-50基准上，基础π0模型的平均成功率仅为42.3%；在LIBERO四套评估集上，OpenVLA的平均成功率为76.5%，与当前最优通用模型**UniVLA**（Li et al., arXiv 2025）仍存在差距。真实世界实验中，π0在空间推理、几何理解和鲁棒性三类任务上的成功率分别仅为60.0%、50.0%和35.0%，凸显了精确3D推理能力的严重不足。

GeoPredict的核心动机在于：**能否在不增加推理开销的前提下，为VLA策略注入预测性运动学和几何先验？** 其关键洞察是——仅在训练阶段利用未来深度渲染监督来学习预测性3D表示，推理时保持与标准VLA一致的计算流程，即可显著提升策略的3D感知和长时域规划能力。这一设计通过两个互补的预测模块实现：轨迹级预测模块编码机器人关键点运动历史并预测未来多步3D轨迹，3D高斯几何模块则预测未来工作空间的几何结构。两个模块作为训练时的辅助监督信号，驱动底层LLM Transformer学习更丰富的时空表征，而推理阶段无需调用任何3D解码器。



## 核心方法与创新机理

GeoPredict 的核心创新在于**将预测性运动学先验与预测性3D几何先验注入连续动作VLA策略的训练过程**，而推理时完全不引入额外计算开销。这一设计直接回应了当前VLA模型的核心瓶颈：依赖2D瞬时观测，缺乏对3D空间关系和未来动态的预测能力，导致在需要精确3D推理的操控任务中表现不佳。

### 创新一：轨迹级运动学预测模块

传统VLA策略（如π0）仅基于当前观测生成动作，缺乏对机器人运动历史和未来趋势的显式建模。GeoPredict引入了一个**轨迹级预测模块**，包含两个关键组件：

- **历史轨迹编码器（Track Encoder）**：将机器人所有关键点（关节和末端执行器点）的运动历史压缩为紧凑的token表示，为Transformer提供运动学上下文先验。
- **未来轨迹查询（Future Track Query）**：通过$K$个可学习的查询token，联合正弦时间位置编码，显式解码出未来$H$步的3D关键点轨迹：$\hat{\mathbf{p}}_{k,t+\tau} = \mathbf{MLP}(\mathbf{e}_k^{\mathrm{fut}} + \mathbf{PE}^{\mathrm{time}}[\tau])$，并通过MSE损失$\mathcal{L}_{\mathrm{track}}$进行监督。

这一模块的核心价值在于：**为策略提供了关于“机器人将如何移动”的显式预测信号**，使动作生成能够利用未来运动学先验，而非仅依赖当前状态的隐式推理。

### 创新二：预测性3D高斯几何模块

仅靠运动学预测仍不足以解决空间推理问题。GeoPredict进一步引入了一个**预测性3D高斯几何模块**，使模型能够“想象”未来场景的3D几何结构：

- **3D空间查询（Spatial Query）**：将机器人工作空间离散化为体素网格，通过可学习初始嵌入与3D正弦位置编码相加构建空间查询token。
- **体素解码器（Voxel Decoder）**：将空间嵌入解码为3D高斯原始体素特征，形成对场景几何的隐式表示。
- **轨迹引导细化（Track-guided Refinement）**：这是连接两个预测模块的关键机制——利用预测的未来关键点轨迹，在任务相关的交互区域自适应地增加高斯密度，实现几何容量的定向分配。
- **深度渲染监督**：通过可微Alpha合成渲染深度图$\hat{\mathbf{D}}(\mathbf{r}) = \sum_{i\in\mathcal{N}} T_i \alpha_i d_i$，并与真实深度进行对比，为几何预测提供训练信号。

### 创新三：训练-推理解耦的设计哲学

GeoPredict最具实用价值的创新在于其**训练-推理解耦策略**：两个预测模块（轨迹预测和3D高斯几何模块）仅在训练阶段作为辅助监督信号使用，推理时完全不执行。这意味着：

- **推理效率不变**：动作生成流程与标准VLA策略一致，不增加任何3D解码或渲染开销。
- **性能显著提升**：消融实验表明，完整的轨迹引导细化机制使RoboCasa成功率从π0基线的42.3%提升至52.4%（+10.1%）；在LIBERO上超越OpenVLA达20.0个百分点；真实世界几何任务上提升达45个百分点（95.0% vs 50.0%）。

### 与现有方法的差异化

| 对比维度 | π0 / OpenVLA | SpatialVLA | GeoPredict |
|---------|-------------|------------|------------|
| 运动学先验 | 无 | 无 | 历史编码+未来预测 |
| 3D几何建模 | 无 | 显式3D集成 | 预测性3D高斯+深度监督 |
| 推理开销 | 标准 | 增加3D处理 | 无额外开销 |
| 几何容量分配 | 均匀 | 均匀 | 轨迹引导自适应细化 |

GeoPredict的独特之处在于：它不改变VLA的基础架构，而是通过训练时的辅助预测任务，迫使模型学习更丰富的3D时空表示。这种“免费午餐”式的设计使其在保持推理效率的同时，获得了显著的3D推理能力提升。



GeoPredict 在连续动作 VLA 策略的基础上引入两个仅在训练阶段使用的预测模块：**轨迹级运动学预测**和**预测性 3D 高斯几何建模**。其核心设计思想是，通过训练时学习未来机器人关键点轨迹和场景深度结构，为策略提供运动学先验与空间几何先验，而在推理时不增加任何 3D 解码开销。

### 输入与编码

系统接收三类输入：

1. **语言指令**：描述操控任务的自然语言文本。
2. **多视图图像**：来自多个相机的 RGB 观测，经视觉编码器提取特征后送入中央 LLM Transformer。
3. **运动历史**：机器人所有关键点（关节及末端执行器点）的历史 3D 轨迹，由 **Track Encoder** 压缩为紧凑 token。

Track Encoder 对每个关键点 $k$ 的历史轨迹 $\mathcal{T}_k$ 进行交叉注意力编码，生成单一的历史轨迹 token $\mathbf{Z}_k^{\mathrm{hist}}$。这一过程将时序运动信息抽象为 Transformer 可直接处理的表示。

### 中央 LLM Transformer

所有 token——包括视觉 token、语言 token、历史轨迹 token 以及可学习的查询 token——被送入一个统一的 LLM Transformer 骨干网络。该 Transformer 采用分块因果注意力机制（Figure 2），在保持自回归生成能力的同时，允许不同模态 token 之间的信息交互。

Transformer 内部同时学习两个并行的预测任务：

- **轨迹预测**：通过 $K$ 个可学习的 **Future Track Query** 与历史轨迹 token 交互，生成未来轨迹嵌入 $\mathbf{e}_k^{\mathrm{fut}}$。这些嵌入经 MLP 与正弦时间位置编码 $\mathbf{PE}^{\mathrm{time}}[\tau]$ 相加后，解码为未来 $H$ 步的 3D 关键点坐标 $\hat{\mathbf{p}}_{k,t+\tau}$。
- **3D 几何预测**：定义机器人工作空间的 3D 体素网格，将可学习初始查询与 3D 正弦空间位置编码相加，构建 **3D Spatial Query** $\mathbf{Q}^{\mathrm{spatial}}[i,j,k]$。这些空间查询经 Transformer 处理后得到空间嵌入 $\mathbf{E}^{\mathrm{spatial}}$。

### 预测性 3D 高斯几何模块

空间嵌入 $\mathbf{E}^{\mathrm{spatial}}$ 通过时间位置编码偏移到未来时间步，得到 $\mathbf{E}_{t+\tau}^{\mathrm{spatial}}$。随后，**Voxel Decoder**（由转置卷积组成）将空间嵌入解码为 3D 高斯原始体素特征，每个体素映射为一组高斯基元。

关键的创新在于 **Track-guided Refinement**（轨迹引导细化）机制：利用预测的未来关键点轨迹 $\mathbf{P}_{t+\tau}$ 生成二值掩码 $\mathbf{M}^{\mathrm{refine}}$，标记包含预测关键点的体素。在这些感兴趣区域内，系统增加高斯基元密度，实现**自适应几何容量分配**——将有限的表示能力集中于任务相关的交互区域。

细化后的高斯场 $\mathbf{G}_{t+\tau}^{\mathrm{total}}$ 通过可微 Alpha 合成渲染为深度图 $\hat{\mathbf{D}}(\mathbf{r})$，并与真实深度进行监督。深度监督通过空间掩码限制在机器人操作空间内，避免背景区域干扰。

### 动作生成与推理

**Action Expert** 基于 Transformer 的注意力输出，通过集成的学习向量场生成连续动作块 $\mathbf{A}_t = [\mathbf{a}_t, \mathbf{a}_{t+1}, \dots, \mathbf{a}_{t+H-1}]$，其中每个动作 $\mathbf{a}_t$ 为 7 自由度末端执行器指令（平移 $\Delta\mathbf{x}$、旋转 $\Delta\boldsymbol{\theta}$、夹爪状态 $g$）。

**推理阶段的关键特性**：Voxel Decoder、Track-guided Refinement 和深度渲染模块均不执行。推理时的计算流程与标准 VLA 策略无异，仅保留 Transformer 前向传播和 Action Expert 的动作生成。这意味着 GeoPredict 在部署时**不引入额外推理延迟**，所有 3D 预测能力均通过训练阶段的监督信号“蒸馏”进策略表示中。

### 训练损失

总损失函数由三项组成，权重均设为 1.0：

- **动作损失**：标准的行为克隆或流匹配损失。
- **轨迹预测损失** $\mathcal{L}_{\mathrm{track}}$：所有关键点和未来时间步上的均方误差。
- **深度渲染损失**：渲染深度与真实深度之间的误差。

消融实验（Table 3）严格验证了各模块的因果贡献：基线 $\pi_0$ 成功率 42.3%，添加 Track Encoder 升至 44.8%，加入未来轨迹预测升至 47.2%，联合深度监督升至 50.5%，最终启用轨迹引导细化达到最高 52.4%。值得注意的是，加入颜色渲染无增益（49.2% vs 仅深度的 49.4%），表明**深度几何信息是核心驱动因素**，纹理信息对 3D 推理帮助有限。

### 补充图表

![[assets/figures/papers/paper_list_l972_https_arxiv_org_abs_2512_16811/figures/001_Figure_1.jpg]]
*Figure 1: Overview of GeoPredict. Given an instruction, multi-view images and motion history encoded by the Track Encoder, a central LLM Transformer learns two main tasks. First, it predicts multi-timestep 3D keypoint trajectories using learnable Future Track Query. Second, it forecasts future workspace geometry as a predictive 3D Gaussian by processing a 3D Spatial Query through a Voxel Decoder. A track-guided refinement mechanism leverages the predicted future tracks to allocate geometric capacity to task-relevant interaction regions. Our policy then generates the final action via an Action Expert. Crucially, these predictive modules serve exclusively as trainingtime supervision and are not invoked...*



GeoPredict 的核心设计思想是在训练阶段引入两个预测性模块——轨迹级运动学预测与 3D 高斯几何预测——为底层 VLA 策略提供未来运动学先验和空间几何先验，而在推理时这两个模块均不执行，从而在不增加推理开销的前提下显著提升 3D 感知与长时域规划能力。

### 轨迹级运动学预测模块

该模块由**历史轨迹编码器（Track Encoder）** 和**未来轨迹查询（Future Track Query）** 两部分构成，共同为动作生成提供紧凑的运动学先验。

**Track Encoder** 将机器人所有关键点（关节及末端执行器点）的运动历史压缩为紧凑 token。对于第 $k$ 个关键点，其历史轨迹 $\mathcal{T}_k$ 经过 MLP 编码后，通过交叉注意力与可学习查询 $\mathbf{Q}^{\mathrm{hist}}$ 交互，生成单一历史轨迹 token $\mathbf{Z}_k^{\mathrm{hist}}$：

$$
\mathbf{Z}_k^{\mathrm{hist}} = \mathrm{CrossAttn}(\mathrm{query}=\mathbf{Q}^{\mathrm{hist}},\; \mathrm{key}=\mathrm{MLP}(\mathcal{T}_k),\; \mathrm{value}=\mathrm{MLP}(\mathcal{T}_k))
$$

**Future Track Query** 引入 $K$ 个可学习的未来轨迹查询 token，经 Transformer 处理后输出未来轨迹嵌入 $\mathbf{e}_k^{\mathrm{fut}}$。随后，利用正弦时间位置编码 $\mathbf{PE}^{\mathrm{time}}[\tau]$ 将嵌入解码为显式的多步 3D 关键点坐标：

$$
\hat{\mathbf{p}}_{k,t+\tau} = \mathbf{MLP}(\mathbf{e}_k^{\mathrm{fut}} + \mathbf{PE}^{\mathrm{time}}[\tau]), \quad \tau = 0, \ldots, H
$$

其中 $H=50$ 为预测时域长度。轨迹预测通过真值关键点坐标 $\mathbf{p}_{k,t+\tau}^{\mathrm{gt}}$ 进行监督，损失函数为所有关键点和时间步上的均方误差：

$$
\mathcal{L}_{\mathrm{track}} = \frac{1}{K(H+1)} \sum_{k=1}^{K} \sum_{\tau=0}^{H} \| \hat{\mathbf{p}}_{k,t+\tau} - \mathbf{p}_{k,t+\tau}^{\mathrm{gt}} \|_2^2
$$

### 3D 高斯几何预测模块

该模块通过**3D 空间查询**、**体素解码器**和**轨迹引导细化**三个子模块，在训练时预测未来工作空间的 3D 几何结构。

**3D 空间查询** 将机器人工作空间离散化为体素网格，每个体素 $[i,j,k]$ 对应一个可学习的初始嵌入 $\mathbf{Q}^{\mathrm{init}}[i,j,k]$，并与 3D 正弦空间位置编码相加，构建空间查询 token：

$$
\mathbf{Q}^{\mathrm{spatial}}[i,j,k] = \mathbf{Q}^{\mathrm{init}}[i,j,k] + \mathbf{PE}^{\mathrm{spatial}}[i,j,k]
$$

空间查询经 Transformer 处理后得到空间嵌入 $\mathbf{E}^{\mathrm{spatial}}$。为预测未来几何，利用时间位置编码将当前空间嵌入偏移到未来时间步：

$$
\mathbf{E}_{t+\tau}^{\mathrm{spatial}} = \mathbf{E}^{\mathrm{spatial}} + \mathbf{PE}^{\mathrm{time}}[\tau], \quad \tau = 0, \ldots, H
$$

**体素解码器（Voxel Decoder）** 由转置卷积构成，将空间嵌入解码为 3D 高斯原始体素特征，每个体素映射为一组高斯原语（位置、协方差、不透明度等参数）。

**轨迹引导细化（Track-guided Refinement）** 是连接两个预测模块的关键机制。根据预测的未来关键点轨迹 $\mathbf{P}_{t+\tau}$，生成体素级二值掩码，标记包含预测关键点的体素：

$$
\mathbf{M}^{\mathrm{refine}}[i,j,k] = \begin{cases} 1, & \text{if } \exists \mathbf{p} \in \mathbf{P}_{t+\tau} \text{ s.t. } \mathbf{p} \in \mathcal{V}[i,j,k], \\ 0, & \text{otherwise.} \end{cases}
$$

被标记的体素区域将增加高斯原语密度，从而在任务相关的交互区域自适应分配几何容量。

### 深度渲染与监督

从预测的 3D 高斯模型 $\mathbf{G}_{t+\tau}^{\mathrm{total}}$ 出发，通过可微 Alpha 合成渲染深度图。对于像素光线 $\mathbf{r}$，渲染深度为：

$$
\hat{\mathbf{D}}(\mathbf{r}) = \sum_{i\in\mathcal{N}} T_i \alpha_i d_i
$$

其中 $T_i = \prod_{j=1}^{i-1} (1-\alpha_j)$ 为累计透射率，$\alpha_i$ 为第 $i$ 个高斯的不透明度，$d_i$ 为其中心的深度值。深度监督仅施加于机器人操作空间内的像素，通过空间掩码过滤无关区域。

### 动作生成

动作专家（Action Expert）基于 Transformer 的注意力输出，通过整合学习到的向量场生成连续动作块 $\mathbf{A}_t = [\mathbf{a}_t, \mathbf{a}_{t+1}, \dots, \mathbf{a}_{t+H-1}]$，其中每个动作 $\mathbf{a}_t = \{\Delta \mathbf{x}, \Delta \pmb{\theta}, g\}$ 为 7 自由度末端执行器指令（平移、旋转及夹爪状态）。

> **推理效率**：预测性 3D 高斯几何模块（体素解码器、深度渲染）在推理时不执行，动作生成流程与标准 VLA 策略一致，保证了推理效率。

### 补充图表

![[assets/figures/papers/paper_list_l972_https_arxiv_org_abs_2512_16811/figures/002_Figure_2.jpg]]
*Figure 2: Block-wise Causal Attention Mechanism. For simplicity, the detailed attention pathways from the 3D Token and State Token blocks to other blocks are not fully drawn*



## 实验与关键发现

### 仿真基准评估

GeoPredict在两个主流的机器人操控仿真基准上进行了系统评估：RoboCasa Human-50（24个子任务，每任务50条演示）和LIBERO（4个评估套件，每任务50条演示）。所有方法均在相同数据量和硬件条件（8 NVIDIA H20 GPU）下训练，损失权重统一设为1.0。

**Table 1**展示了RoboCasa基准上的完整结果。GeoPredict以**52.4%**的平均成功率显著超越所有对比方法，相比基础VLA模型π0（42.3%）提升**10.1个百分点**。这一增益在24个子任务上具有一致性，表明预测性运动学与几何先验对多样化操控场景的普适贡献。值得注意的是，GeoPredict超越了显式集成3D信息的**SpatialVLA**（Qu et al., arXiv 2025）和基于3D高斯世界模型的**GWM**（Lu et al., ICCV 2025），验证了“训练时预测未来几何”策略优于“推理时显式建模”的设计选择。

**Table 2**汇报了LIBERO基准的结果。GeoPredict在四个套件上平均达到**96.5%**的成功率，较开源VLA模型**OpenVLA**（Kim et al., CoRL 2025）的76.5%提升**20.0个百分点**，并超越当前最优通用VLA模型**UniVLA**（Li et al., arXiv 2025）。在长时域任务套件LIBERO-Long上，GeoPredict单独取得**94.0%**的成功率，表明预测性轨迹先验对需要长程规划的任务尤为关键。

### 消融实验：因果链验证

**Table 3**通过逐步激活GeoPredict各模块，在RoboCasa基准上验证了核心因果机制。消融链从π0基线（42.3%）出发：

1. **添加历史轨迹编码器**（Track Encoder）：成功率提升至44.8%。这验证了运动历史先验的有效性——仅让策略感知机器人关键点过去的运动轨迹，即可改善动作生成。
2. **添加未来轨迹预测**（+L_track）：成功率进一步提升至47.2%。显式预测未来多步关键点轨迹，为策略提供了前向运动学引导，证明“预测未来”比“仅记忆历史”更有价值。
3. **联合训练深度损失**（+L_depth，无轨迹引导细化）：达到50.5%。引入3D几何预测模块后，即使不做自适应容量分配，深度渲染监督已能显著增强策略的空间理解。
4. **启用完整轨迹引导细化**：达到最高**52.4%**。该机制根据预测的未来轨迹在任务相关区域增加高斯密度，证明自适应几何容量分配是性能饱和的关键一环。

**Table 4**进一步消融了深度渲染的设计选择。仅使用深度渲染（49.4%）与额外加入颜色渲染（49.2%）性能相当，表明几何信息（深度）是主要驱动力，颜色纹理对策略的3D推理贡献有限。这一发现支持了“纯几何先验即可”的设计决策，同时避免了颜色渲染的额外计算开销。

### 真实世界实验

**Table 5**汇报了真实世界实验在三种设置下的结果：

- **空间泛化**（Spatial）：GeoPredict达到**85.0%**，较π0的60.0%提升25个百分点。任务要求模型在未见过的空间配置中定位和操作物体，预测性几何先验显著增强了空间理解。
- **几何泛化**（Geometry）：GeoPredict达到**95.0%**，较π0的50.0%提升45个百分点。任务涉及复杂几何形状的物体交互，3D高斯预测模块对此类场景的几何理解提供了关键支撑。
- **鲁棒性**（Robustness）：GeoPredict达到**90.0%**，较π0的35.0%提升55个百分点。在存在视觉干扰物的环境中，预测性运动学先验帮助策略聚焦于任务相关区域，抑制无关信息。

真实世界结果与仿真趋势高度一致，且增益幅度更大，表明GeoPredict的预测性先验在真实感知噪声和动态变化中具有更强的补偿作用。

### 关键发现总结

1. **预测性先验的因果效力**：消融实验清晰展示了从“历史运动编码→未来轨迹预测→3D几何预测→轨迹引导细化”的递进增益链，每一步均带来统计显著的性能提升。
2. **几何容量自适应分配是关键**：轨迹引导细化机制贡献了1.9个百分点的额外增益（50.5%→52.4%），证明在预测交互区域集中建模资源比均匀分配高斯容量更有效。
3. **深度几何足够，颜色纹理冗余**：深度渲染与颜色渲染性能无显著差异，说明策略所需的3D先验本质上是几何结构信息，而非外观纹理。
4. **仿真到真实的迁移增益**：真实世界实验中GeoPredict相对π0的提升幅度（25-55个百分点）远大于仿真基准（10.1个百分点），暗示预测性先验在应对真实世界不确定性时具有更强的鲁棒性补偿效应。

### 补充图表

![[assets/figures/papers/paper_list_l972_https_arxiv_org_abs_2512_16811/figures/004_Table_1.jpg]]
*Table 1: RoboCasa Simulation Benchmark Results. Task success rates (%) across 24 sub-tasks and the Average Success Rate (%). ∗Denotes our fine-tuned experimental results. Bold indicates the best performing model. See Appendix for detailed sub-task definitions*

![[assets/figures/papers/paper_list_l972_https_arxiv_org_abs_2512_16811/figures/005_Table_2.jpg]]
*Table 2: LIBERO Simulation Benchmark Results. Task success rates (%) across 4 evaluation suites and the Average Success Rate (%). ∗Denotes our reproduced experimental results. †Denotes no available standard deviation data. Bold indicates the best performing model, and underline indicates the runner-up model*

![[assets/figures/papers/paper_list_l972_https_arxiv_org_abs_2512_16811/figures/007_Table_3.jpg]]
*Table 3: Ablation Study on RoboCasa Simulation Benchmark. Future Depth is rendered from initial global Gaussians*

![[assets/figures/papers/paper_list_l972_https_arxiv_org_abs_2512_16811/figures/008_Table_4.jpg]]
*Table 4: Ablation Study on Depth Rendering*

![[assets/figures/papers/paper_list_l972_https_arxiv_org_abs_2512_16811/figures/009_Table_5.jpg]]
*Table 5: Real-World Experiment Results. Task success rates (%) across three distinct settings: Spatial, Geometry, and Robustness*

![[assets/figures/papers/paper_list_l972_https_arxiv_org_abs_2512_16811/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Comparisons of Future Depth Rendering. Visualizations are shown for timesteps*



## 定位与知识库关联

### 与基线方法的差异化关系

GeoPredict 的核心定位是在连续动作 VLA 框架中注入**预测性运动学先验**和**预测性几何先验**，这与现有工作的设计哲学形成清晰对比。

**与 π0 的关系**：GeoPredict 以 π0 作为基础 VLA 骨架，继承了其连续动作流匹配的生成范式。π0 主要依赖 2D 图像和瞬时观测进行动作生成，缺乏对 3D 空间关系和未来动态的显式建模。GeoPredict 在此基础上增加了三个关键模块——轨迹预测模块、3D 几何预测模块和对应的训练监督信号，将 π0 在 RoboCasa Human-50 上的平均成功率从 42.3% 提升至 52.4%（+10.1%），在真实世界 Geometry 场景中更是从 50.0% 提升至 95.0%（+45.0%）。这一巨大差距揭示了**缺乏 3D 先验是 π0 在精确操控任务中的核心瓶颈**。

**与 OpenVLA 的关系**：OpenVLA（Kim et al., CoRL 2025）是代表性的开源 VLA 模型，基于离散动作 token 进行策略学习。在 LIBERO 四个评估套件上，GeoPredict 以 96.5% 的平均成功率领先 OpenVLA 达 20.0 个百分点。这一结果不仅体现了连续动作表示的优势，更关键地说明了预测性 3D 先验对提升跨任务泛化能力的作用。值得注意的是，GeoPredict 在训练数据量（每任务 50 条演示）和硬件条件（8 NVIDIA H20 GPU）上与复现的 OpenVLA 保持一致，确保了对比的公平性。

**与 UniVLA 的关系**：UniVLA（Li et al., arXiv 2025）是当前最优的通用 VLA 模型。GeoPredict 在 LIBERO 上的表现与其形成竞争关系，但 GeoPredict 的方法论路径截然不同——UniVLA 追求更大规模的预训练和模型容量，而 GeoPredict 通过**训练时注入预测性 3D 表示**这一更轻量的方式，在不增加推理开销的前提下实现了可比甚至更优的性能。

**与 SpatialVLA 的关系**：SpatialVLA（Qu et al., arXiv 2025）显式集成了 3D 信息，与 GeoPredict 同属“几何感知 VLA”这一技术路线。两者的关键区别在于：SpatialVLA 在推理时依赖 3D 信息处理，而 GeoPredict 的预测性 3D 高斯几何模块仅在训练时使用，推理时不执行体素解码和深度渲染。这种“训练时注入、推理时免费”的设计是 GeoPredict 的核心创新，使其在保持推理效率的同时获得 3D 推理能力。

**与 GWM 的关系**：GWM（Lu et al., ICCV 2025）使用 3D 高斯作为世界模型进行未来状态预测，与 GeoPredict 共享 3DGS 这一技术要素。但二者目标不同：GWM 侧重于学习通用的世界动力学模型，而 GeoPredict 将 3DGS 预测**聚焦于机器人工作空间内的任务相关几何**，并通过轨迹引导细化机制将高斯容量自适应地分配到预测关键点轨迹附近的交互区域。这种任务驱动的几何建模策略是 GeoPredict 在操控任务上取得显著提升的关键。

### 适用边界与局限

GeoPredict 的设计存在若干明确的适用边界：

1. **固定工作空间假设**：3D 空间查询定义在预定义的机器人工作空间体素网格内，深度渲染的监督也通过空间掩码限制在此范围内。这意味着模型对工作空间外的物体和场景变化缺乏建模能力，在需要大范围移动操作的任务中可能失效。

2. **预测窗口固定**：当前所有实验均使用 H=50 的预测窗口。对于需要更长时域规划的任务（如长时间序列的装配操作），该窗口是否足够尚待验证。

3. **深度监督的依赖性**：训练时使用的深度渲染损失需要真实的深度图作为监督信号。在仿真环境中可直接获取，但在真实世界部署时，深度传感器的精度和可用性可能成为限制因素。论文未明确说明真实世界实验中深度监督的具体获取方式，这一点需要读者自行验证。

4. **机器人形态的泛化**：当前方法在单臂固定基座机器人上验证，轨迹编码器针对 K 个预定义关键点设计。对于移动操作、多臂协同或灵巧手等不同形态，关键点定义和轨迹编码方式需要重新设计。

### 开放问题

1. **深度监督的真实世界可扩展性**：预测模块在真实世界中的深度监督如何获取？是否依赖仿真深度传感器或外部深度估计算法？这直接影响方法在实际部署中的可行性。

2. **跨场景和跨物体的泛化**：模型在未见过的环境布局和物体实例上的泛化能力如何？当前实验虽然覆盖了仿真和真实世界场景，但未见系统性的分布外泛化评估。

3. **预测窗口的时域扩展**：H=50 的预测窗口是否适用于更长时间的任务？增加预测窗口是否会引入累积误差，以及如何通过训练策略缓解这一问题？

4. **多模态感知融合的潜力**：当前方法使用多视角 RGB 图像作为视觉输入。触觉、力觉等模态的融入是否能进一步增强几何预测的精度和操控的鲁棒性？



## 原文 PDF

![[paperPDFs/CVPR_2026/GeoPredict_Leveraging_Predictive_Kinematics_and_3D_Gaussian_Geometry_for_Precise_VLA_Manipulation.pdf]]
