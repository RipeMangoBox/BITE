---
title: "OmniCam: Unified Multimodal Camera Control for Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/OmniCam_Unified_Multimodal_Camera_Control_for_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- OmniCam
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 离散运动表示（<starttime, endtime, speed, direction, rotate>）作为中间桥梁，通过LLM将多模态输入统一为运动基元，结合轨迹规划算法与扩散模型修复，实现精确的6DoF控制。
primary_logic: 将相机轨迹解耦为离散运动描述，并组合单目重建与视频扩散先验，OmniCam首次支持文本、视频和轨迹任意输入组合下的帧级相机控制与时空一致视频生成。
claims:
- OmniCam在旋转误差(RotErr)、平移误差(TransErr)、LPIPS、PSNR、FID等指标上全面超越CameraCtrl、LucidDreamer、CamI2V、ZeroNVS、MotionCtrl等基线。
- 对于文本到轨迹的生成，Llama骨干网络在轨迹平均准确率(Avg)上达到80.171，并支持帧级时间、速度、方向、旋转的全面评估。
- 视频引导的轨迹提取中，Llama+SLAM方案显著优于SIFT和VLM方案，验证了平滑模块与坐标映射的必要性。
- Camera-controlled video generation (OmniTr/RealEstate test set) 上 Rotation Error (RotErr) ↓ = 1.066
---

# OmniCam: Unified Multimodal Camera Control for Video Generation

> [!tip] 核心洞察
> 将相机轨迹解耦为离散运动描述，并组合单目重建与视频扩散先验，OmniCam首次支持文本、视频和轨迹任意输入组合下的帧级相机控制与时空一致视频生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | OmniCam：面向视频生成的统一多模态相机控制 |
| 英文题名 | OmniCam: Unified Multimodal Camera Control for Video Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2504.02312) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | OmniCam |
| Dataset | Camera-controlled video generation |

> [!tip] 效果简介
> - Camera-controlled video generation (OmniTr/RealEstate test set) 上，Rotation Error (RotErr) ↓ 1.066 vs 6.423 (CameraCtrl) (-5.357)。
> - 同上 上，Translation Error (TransErr) ↓ 2.731 vs 5.792 (CameraCtrl) (-3.061)；LPIPS ↓ 0.167 vs 0.291 (CameraCtrl) (-0.124)；PSNR ↑ 22.14 vs 18.37 (CameraCtrl) (+3.77)。

## 概要

**问题瓶颈**：现有相机控制方法面临两大结构性困境。其一，输入模态单一——通常仅支持文本描述或预定义轨迹中的一种，无法同时处理文本、参考视频和直接轨迹输入。其二，控制粒度粗糙——多数方法只能实现关键帧级别的粗略控制，缺乏帧级的时间、速度、方向与旋转角度的精确设定。这导致生成视频的空间结构易扭曲，且难以覆盖复杂的长时间序列运动。

**核心思路**：OmniCam 提出以**离散运动表示**作为统一中间桥梁——将任意轨迹输入（文本描述或参考视频提取）转化为 `<starttime, endtime, speed, direction, rotate>` 序列。这一表示由微调的 LLM 生成，随后经轨迹规划算法解算为逐帧的 6DoF 相机外参。在此基础上，OmniCam 将单目重建（DUSt3R 提取点云与内参）与视频扩散模型的先验知识相结合：先渲染带空洞的粗视图，再由潜在扩散模型补全未知区域，最终生成时空一致的视频。这一设计首次实现了文本、视频和轨迹任意输入组合下的帧级相机控制。

**方法定位**：OmniCam 处于相机控制视频生成与单目新视角合成的交叉地带。相较于 CameraCtrl（依赖数据集预定义轨迹）、LucidDreamer（基于深度变形）、CamI2V（图像到视频的相机控制）和 MotionCtrl（相机嵌入控制）等基线，OmniCam 的差异化在于**多模态轨迹输入的统一解析**与**帧级精确控制**。同时，其配套构建的 OmniTr 数据集（1000 条轨迹、10k 文本描述、30k 视频）填补了多模态轨迹数据缺失的空白。

**主要结果**：在 OmniTr/RealEstate 测试集上，OmniCam 在旋转误差（RotErr: 1.066 vs. CameraCtrl 6.423）、平移误差（TransErr: 2.731 vs. 5.792）、LPIPS（0.167 vs. 0.291）、PSNR（22.14 vs. 18.37）和 FID（24.26 vs. 69.4）上全面超越基线方法。文本到轨迹的生成中，Llama 骨干网络达到 80.171 的轨迹平均准确率。视频引导轨迹提取方面，Llama+SLAM 组合显著优于 SIFT 和 VLM 方案，验证了平滑模块与坐标映射的必要性。强化学习端到端优化带来小幅但稳定的提升（准确率从 78.341 升至 80.171）。

**局限与开放问题**：强化学习优化的提升幅度较小且可能随随机种子波动；复杂场景中单目重建点云不完整时，遮挡区域恢复仍可能出现瑕疵；OmniTr 数据集规模有限（1000 条轨迹），极开放场景的泛化能力有待验证。此外，相机控制领域尚无统一评估标准，当前定量比较存在固有局限性。

### 相机控制视频生成的现状与瓶颈

相机运动控制是视频生成中的核心挑战之一，其目标是根据用户指定的相机轨迹，从单张或少量参考图像生成时空一致的视频序列。这一能力在电影制作、虚拟现实、3D 场景漫游等应用中具有广泛需求。然而，现有方法在灵活性和精确性之间存在显著矛盾。

从输入模态角度看，当前相机控制方法通常只能支持单一类型的轨迹输入：要么接受文本描述，要么依赖预定义的数值轨迹，要么从参考视频中提取运动。这种模态锁定严重限制了用户的使用场景——例如，创作者可能希望先用自然语言描述“从左侧缓慢平移至右侧，同时轻微旋转”，再通过一段实拍视频精确复刻其运镜节奏，而现有系统无法同时满足这两种需求。

从控制粒度看，多数方法仅提供粗糙的关键帧级控制或基础平移操作。以 **CameraCtrl** 为代表的基于数据集的相机控制方法，虽然能生成相对平滑的运动，但缺乏对每帧操作的精确时间边界、速度曲线和复合旋转的支持。**MotionCtrl** 等嵌入控制方法同样受限于预定义的相机嵌入空间，难以表达任意方向的复合运动。**LucidDreamer** 和 **ZeroNVS** 等基于深度变形或零样本新视角合成的方法，则侧重于空间一致性而忽视了时序控制的精确性。

更深层的瓶颈在于**数据层面**：现有数据集（如 RealEstate）仅包含视频与对应轨迹，缺乏文本描述与离散运动表示的标注，导致模型无法学习从自然语言到精确运动参数的映射。这使得文本驱动的相机控制长期停留在简单方向描述阶段，难以处理“在前3秒以0.5倍速向右上方45度平移，同时以每秒2度顺时针旋转”这类复合指令。

### 核心动机：统一多模态与帧级精确控制

OmniCam 的提出正是为了填补上述双重缺口。其核心洞察在于：**相机轨迹本质上可以被解耦为一组离散运动基元**——每个基元包含起止时间、速度、方向和旋转角度。这种离散运动表示天然适合作为多模态输入与精确轨迹规划之间的中间桥梁。

具体而言，OmniCam 的设计动机围绕三个递进目标展开：

1. **多模态统一输入**：通过大语言模型（LLM）将文本描述、参考视频提取的轨迹、或直接输入的6DoF参数统一转换为离散运动表示序列`<starttime, endtime, speed, direction, rotate>`，首次实现三种模态的任意组合输入。

2. **帧级精确控制**：在离散运动表示的基础上，通过轨迹规划算法将每个基元展开为逐帧的相机外参，支持任意方向的复合运动、推拉变焦、速度调节和旋转操作，控制精度达到帧级别。

3. **时空一致生成**：结合单目重建（DUSt3R）获取场景点云，利用轨迹外参渲染初始粗视图，再通过预训练视频扩散模型的先验知识修复遮挡和未知区域，最终生成时空一致的高质量视频。

这种“离散表示桥接 + 重建渲染 + 扩散修复”的流水线设计，使得 OmniCam 在灵活性（支持多模态输入）与精确性（帧级6DoF控制）之间取得了此前方法未能实现的平衡。此外，为支撑这一框架的训练与评估，作者构建了 **OmniTr 数据集**，包含1000条轨迹、10,000条文本描述和30,000个视频，全面覆盖方向、速度、旋转、时间边界等运动属性，填补了多模态相机控制数据的空白。

## 核心方法与创新机理

OmniCam的核心创新在于通过**离散运动表示**这一中间桥梁，首次将多模态相机轨迹输入（文本描述、参考视频提取、直接轨迹参数）统一为帧级精确的6自由度（6DoF）控制信号，并借助单目重建与视频扩散先验的组合，实现时空一致的相机控制视频生成。以下从三个维度剖析其相对于现有方法的突破。

### 1. 多模态轨迹输入的统一抽象：离散运动表示

现有相机控制方法通常仅支持单一模态的轨迹输入——要么接受文本指令，要么依赖预定义的数值轨迹，缺乏跨模态的灵活性。OmniCam提出将任意轨迹源统一映射为**离散运动表示**，即一组结构化的五元组序列：

$$\langle \text{starttime}, \text{endtime}, \text{speed}, \text{direction}, \text{rotate} \rangle$$

这一表示充当了多模态输入与相机位姿之间的“语义中间层”。具体而言，系统使用经过LoRA微调的大语言模型（LLM）将自然语言描述转换为上述离散序列，训练目标为负对数似然损失：

$$\mathcal{L}_{\mathrm{trajectory}} = - \sum_{t=1}^{T} \log p(\boldsymbol{y}_t | \hat{\boldsymbol{y}}_{<t})$$

对于视频轨迹输入，则通过SLAM提取原始轨迹后，经平滑模块与坐标映射再交由LLM转换为离散表示。这种设计使得OmniCam同时支持三种轨迹输入方式：文本描述、参考视频提取、以及直接输入6DoF轨迹参数，而现有基线（如**CameraCtrl**、**MotionCtrl**）仅能处理其中一种。

### 2. 从粗粒度关键帧到帧级精确控制

传统方法多停留在粗略的关键帧控制或基础平移操作，无法精细调节每段运动的起止时间、速度变化和任意方向上的复合运动。OmniCam的离散运动表示天然支持**帧级控制**——通过`starttime`和`endtime`字段精确设定每段操作的起止帧，`speed`字段控制运动速率，`direction`和`rotate`字段支持任意方向的平移与旋转组合。

在实现层面，**轨迹规划算法**将离散运动表示转换为每帧的相机外参，采用球坐标参数化 $(\phi, \theta, r)$，使得任意方向的复合运动（如“先向右上45度平移，同时缓慢左旋”）可被精确分解为逐帧位姿。这一能力在消融实验中得到了验证：Llama骨干网络在文本到轨迹的转换中，细粒度方向准确率（M_d-fine）达到76.488，旋转准确率（M_rotate）达到79.818（Table 2），表明模型确实捕获了精细的运动语义。

### 3. 单目重建与扩散先验的协同修复机制

OmniCam的另一关键创新在于将相机控制问题分解为“粗视图初始化+扩散模型修补”的两阶段流水线。首先通过**DUSt3R**从内容参考中提取点云和内参，结合轨迹规划得到的每帧外参进行点云渲染，生成带空洞的初始视图序列；随后以预训练视频扩散模型为核心，注入参考图像的CLIP特征作为条件，对渲染结果中的未知/遮挡区域进行修补，最终拼接为时空一致的视频。

这一设计的深层洞察在于：单目重建提供了几何约束，确保相机运动在三维空间中的一致性；而扩散模型的生成先验则弥补了单目重建在遮挡区域的信息缺失。相比**LucidDreamer**等纯深度变形方法或**ZeroNVS**等零样本新视角合成方法，OmniCam在旋转误差（RotErr: 1.066 vs. 6.423）和平移误差（TransErr: 2.731 vs. 5.792）上均有数量级的提升（Table 3），验证了“几何引导+生成修补”协同策略的有效性。

### 4. 配套数据集OmniTr的构建

上述创新的实现离不开专门构建的**OmniTr数据集**。现有数据集（如RealEstate）仅包含视频与轨迹，缺乏文本描述和离散运动表示。OmniTr包含1000条轨迹、10,000条文本描述和30,000个视频，全面覆盖方向、速度、旋转、起止时间等运动属性（Figure 2饼图展示了各属性的均衡分布）。这一数据集不仅支撑了LLM的微调，也为多模态轨迹理解提供了首个标准化基准。

### 5. 端到端强化学习优化的初步探索

OmniCam还引入了一个可选的强化学习优化环节：冻结下游扩散模型作为奖励信号，使用PPO算法微调上游轨迹大模型，以提高上下游模块的耦合度。消融实验显示，移除RL微调后轨迹平均准确率从80.171降至78.341（Table 2），提升幅度虽小但稳定。作者也坦承，RL优化的提升在不同随机种子下可能波动，这一方向仍需进一步探索。

### 创新边界与遗留问题

尽管OmniCam在多模态输入统一和帧级控制上取得了显著突破，仍存在若干局限：单目重建在严重遮挡场景下点云不完整，导致扩散修补可能出现瑕疵；OmniTr数据集规模（1000条轨迹）仍有限，可能制约模型在极端开放场景的泛化能力；此外，相机控制领域缺乏统一的自动化评估标准，部分定性比较仍依赖人工评测。

OmniCam 的整体流水线遵循“统一表示—轨迹规划—粗视图渲染—扩散修复—端到端优化”五阶段范式，其核心设计在于将多模态轨迹输入（文本描述、参考视频提取的轨迹、或直接给定的6DoF轨迹）统一转换为离散运动表示，从而在单一框架下实现帧级相机控制与时空一致视频生成。

**输入层**接受两类参考：内容参考（单张图像或视频）与轨迹参考（文本指令、视频中的相机运动、或显式轨迹）。这两类参考支持任意组合，使 OmniCam 具备高度的模态灵活性（Table 4）。

**离散运动表示生成器**是整个流水线的“统一中间层”。轨迹参考首先被转换为形如 `<starttime, endtime, speed, direction, rotate>` 的离散运动表示序列。对于文本输入，采用经 LoRA 微调的大语言模型（以 Llama 为骨干）将自然语言指令映射为上述结构化元组，微调目标为负对数似然损失：

$$\mathcal{L}_{\mathrm{trajectory}} = - \sum_{t=1}^{T} \log p(\boldsymbol{y}_t | \hat{\boldsymbol{y}}_{<t})$$

对于视频轨迹输入，则通过 SLAM 提取粗轨迹后经平滑模块与 LLM 映射得到离散表示。这一设计将多模态输入统一为相同的运动基元，为下游模块提供与模态无关的控制接口。

**轨迹规划算法**将离散运动表示转换为每帧的相机外参。相机位姿采用球坐标 $(\phi, \theta, r)$ 参数化，支持任意方向平移、推拉变焦、旋转以及速度控制。该算法是连接语义级运动描述与精确几何位姿的关键桥梁。

**单目重建与点云渲染**模块负责生成初始粗视图。首先通过 DUSt3R 从内容参考中提取点云和相机内参，并利用 Weiszfeld 算法优化焦距；随后结合轨迹规划得到的外参，将点云渲染到每个目标视点。此步骤产生带有空洞和未知区域的初始帧（如 Figure 3 所示），为后续扩散修复提供几何引导。

**潜在扩散模型修补**模块以渲染粗视图为条件，利用预训练视频扩散模型的先验知识补全遮挡/未知区域。具体而言，将参考图像的 CLIP 特征注入 UNet 作为条件，优化目标为最小化噪声预测误差：

$$\min_{\theta} = \mathbb{E}_{t \sim \mathcal{U}(0,1), \epsilon \sim \mathcal{N}(0,I)} \left[ \| \epsilon_{\theta}(z_t, t, \hat{z}, I_{\mathrm{ref}}) - \epsilon \|^2 \right]$$

其中 $z_t = \alpha_t z_0 + \sigma_t \epsilon$ 为加噪后的潜在变量。该模块训练于 RealEstate、DL3DV 及 OmniTr 子集上，学习率 $5\times10^{-5}$，批量大小 16，共 50,000 次迭代，每段视频 25 帧。修补后的帧被拼接为时空一致的输出视频。

**端到端强化学习优化**作为可选的后处理阶段，冻结下游扩散模型作为奖励信号，采用 PPO 对上游轨迹大模型进行微调，以提升上下游模块之间的耦合性。消融实验表明，该步骤带来小幅但稳定的提升（轨迹平均准确率从 78.341 提升至 80.171），但其增益幅度可能受随机种子影响（Table 2）。

整个流水线的输入输出流可概括为：多模态轨迹参考 → 离散运动表示 → 每帧相机外参 → 点云渲染粗视图 → 扩散修补完整帧 → 时空一致视频。这一设计使得 OmniCam 首次在统一框架下同时支持文本、视频和显式轨迹任意组合下的帧级相机控制。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_02312/figures/001_Figure_1.jpg]]
*Figure 1: An overview of OmniCam. Given diverse modalities of content references and trajectory guidance, OmniCam generates high-quality video sequences by camera motion control. Specifically, OmniCam integrates various combinations of content (e.g., image or video) and trajectory (e.g., text instructions or camera motion from video) references. This approach allows OmniCam to accurately synthesize videos consistent with user-specified inputs*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_02312/figures/003_Figure_3.jpg]]
*Figure 3: An overview of OmniCam model pipeline. After receiving the trajectory reference, OmniCam first converts it into discrete motion representations through LLM. Subsequently, OmniCam uses a trajectory planning algorithm to calculate the camera pose for each frame based on these motions. Combined with the content reference, OmniCam renders the initial view for each frame. Finally, it utilizes a diffusion model to complete unknown regions in the new viewpoints, and stitch all frames together to generate a coherent video*

OmniCam 的核心流程由四个关键模块串联而成，将多模态轨迹输入最终转化为时空一致的受控视频。整体流水线如 Figure 3 所示：轨迹参考经 LLM 转换为离散运动表示，再通过轨迹规划算法计算每帧相机位姿，结合内容参考渲染初始视图，最后用扩散模型补全未知区域并拼接成连贯视频。

### 4.1 离散运动表示生成器

该模块负责将异构的轨迹输入统一为结构化的中间表示，是 OmniCam 实现多模态统一控制的关键桥梁。

离散运动表示定义为由五元组 `<starttime, endtime, speed, direction, rotate>` 构成的序列。其中 `starttime` 与 `endtime` 指定操作的起止帧，`speed` 控制运动速率，`direction` 表示任意方向的平移，`rotate` 编码旋转角度。这种设计将连续轨迹解耦为语义明确、可组合的运动基元，使后续的轨迹规划算法能够独立处理每段操作。

对于文本输入，OmniCam 使用 LoRA（Low-Rank Adaptation）微调大语言模型，将其输出的自然语言描述映射为离散运动表示序列。微调的优化目标为负对数似然损失：

$$\mathcal{L}_{\mathrm{trajectory}} = - \sum_{t=1}^{T} \log p(\boldsymbol{y}_t | \hat{\boldsymbol{y}}_{<t}) \tag{1}$$

其中 $\boldsymbol{y}_t$ 为第 $t$ 个离散运动表示的真实值，$\hat{\boldsymbol{y}}_{<t}$ 为模型已预测的前缀序列。对于视频输入，则结合 SLAM 提取粗略轨迹，经平滑模块处理后由 LLM 映射为离散表示。消融实验（Table 2）表明，LLM（Llama）在文本到轨迹任务上的平均准确率达 80.171，显著优于 VLM（Qwen2-VL）的 72.976，验证了纯文本理解任务中 LLM 的优越性。

### 4.2 轨迹规划算法

获得离散运动表示后，轨迹规划算法将其转换为每帧的相机外参，实现帧级精确控制。

相机位姿采用球坐标 $(\phi, \theta, r)$ 参数化，分别对应方位角、极角和径向距离。算法根据每段操作的 `direction` 和 `speed` 计算相邻帧间的角度与距离增量，根据 `rotate` 叠加旋转分量，并根据 `starttime` 和 `endtime` 将运动均匀分配至目标帧区间。这种参数化方式天然支持任意方向的复合运动、推拉镜头以及速度控制，突破了现有方法仅支持基础平移或粗略关键帧控制的局限。

### 4.3 单目重建与点云渲染

该模块利用内容参考图像生成初始的新视角视图，为后续扩散模型提供结构先验。

OmniCam 通过 DUSt3R 从参考图像中提取点云与相机内参，并使用 Weiszfeld 算法优化焦距 $f_0$。结合轨迹规划算法输出的每帧外参，将点云投影渲染为对应视角的粗视图。如 Figure 3 所示，这些渲染结果通常包含因遮挡或视野外区域产生的空洞（unknown regions），需要后续模块进行补全。

### 4.4 潜在扩散模型修补

该模块以预训练视频扩散模型为基础，将点云渲染的粗视图修复为时空一致的高质量视频帧。

扩散模型的优化目标为最小化噪声预测误差：

$$\min_{\theta} = \mathbb{E}_{t \sim \mathcal{U}(0,1), \epsilon \sim \mathcal{N}(0,I)} \left[ \| \epsilon_{\theta}(z_t, t, \hat{z}, I_{\mathrm{ref}}) - \epsilon \|^2 \right] \tag{2}$$

其中 $z_t = \alpha_t z_0 + \sigma_t \epsilon$ 为加噪后的潜变量，$\hat{z}$ 为渲染视图编码后的潜变量条件，$I_{\mathrm{ref}}$ 为参考图像的 CLIP 特征，通过交叉注意力注入 UNet 以保持内容一致性。该设计使扩散模型能够利用其预训练先验，在填补空洞的同时维持全局时空连贯性。

### 4.5 端到端强化学习优化

为进一步提升上下游模块的耦合度，OmniCam 引入强化学习微调阶段。具体而言，冻结下游扩散模型作为奖励信号，使用 PPO 算法优化上游轨迹大模型，使生成的离散运动表示更适配后续的渲染与修补流程。消融实验（Table 2）显示，移除 RL 微调后轨迹平均准确率从 80.171 降至 78.341，表明 RL 带来了稳定但有限的提升。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_02312/figures/010_Figure_7.jpg]]
*Figure 7: Visualization of Rotation Algorithm*

## 实验与关键发现

### 主实验结果

OmniCam在相机控制视频生成任务上进行了全面的定量评估，与多个代表性基线方法进行了对比，包括基于数据集的相机控制方法**CameraCtrl**、基于深度变形的新视角生成方法**LucidDreamer**、图像到视频的相机控制方法**CamI2V**、零样本新视角合成方法**ZeroNVS**以及基于相机嵌入控制的视频生成方法**MotionCtrl**。

在OmniTr和RealEstate测试集上的评估结果如Table 3所示。OmniCam在所有核心指标上均取得了最优性能：

- **相机轨迹精度**：旋转误差（RotErr）仅为1.066，而最强基线CameraCtrl为6.423，降幅达83.4%；平移误差（TransErr）为2.731，相比CameraCtrl的5.792降低了52.8%。这表明OmniCam生成的视频在相机运动轨迹上与真实轨迹高度吻合。

- **视觉质量**：LPIPS达到0.167（CameraCtrl为0.291），PSNR为22.14（CameraCtrl为18.37），FID大幅降至24.26（CameraCtrl为69.4）。FID的显著降低表明OmniCam生成视频的整体分布与真实视频更为接近，视觉真实感更强。

旋转误差和平移误差的计算公式分别为：

$$\mathrm{RotErr} = \sum_{i=1}^{n} \operatorname{arccos} { \frac { t r ( { \boldsymbol { r } } _ { \mathrm { g e n } } ^ { i } \cdot { \boldsymbol { r } } _ { \mathrm { g t } } ^ { i T } ) - 1 } { 2 } }$$

$$\mathrm{TransErr} = \sum_{i=1}^{n} \| \pmb { t } _ { \mathrm { g t } } ^ { i } - \pmb { t } _ { \mathrm { g e n } } ^ { i } \| _ { 2 }$$

为确保评估的公平性，实验采取了多项措施：部分对比方法仅支持方形图像，因此在计算定量指标时将生成结果统一裁剪至方形；相机位姿估计采用DUSt3R而非COLMAP，因为COLMAP对不一致特征敏感，使用DUSt3R可确保评估位姿的鲁棒性；所有方法在同数据集子集上训练或直接使用开源权重，推理时使用相同的DDIM采样与引导策略。

在模态支持能力方面，Table 4对比了各方法的输入灵活性。OmniCam是唯一同时支持图像和视频作为内容参考、文本描述和视频轨迹作为轨迹参考的方法，展现了显著的多模态集成优势。

### 消融实验

为验证各设计选择的有效性，论文进行了系统的消融实验，主要围绕轨迹提取的模态组合与骨干网络选择展开（Table 2）。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_02312/figures/005_Table_2.jpg]]
*Table 2: The performance of different modalities (including content reference and trajectory reference) under different backbones across multiple indicators. These metrics are used to determine the effectiveness of extracting tracks from text or video. The best result is bolded*

**文本到轨迹的生成**：在Image(C)+Text(T)模态下，Llama骨干网络取得了80.171的轨迹平均准确率（Avg），在方向粗粒度（M_d-course）上达到85.267，方向细粒度（M_d-fine）为76.488，速度、旋转、起止时间等指标均为79.818。当移除强化学习微调（w/o RL）时，平均准确率从80.171下降至78.341，表明RL带来了稳定但幅度有限的提升。使用VLM（Qwen2-VL）替代LLM（Llama）处理文本输入时，轨迹准确率从80.171降至72.976，说明在纯文本理解任务中LLM优于VLM。

**视频引导的轨迹提取**：在Image(C)+Video(T)模态下，Llama+SLAM组合方案显著优于纯SLAM和SIFT方法，验证了平滑模块与LLM映射在视频轨迹提取中的必要性。SIFT方法在处理复杂相机运动时精度明显不足，而VLM方案（Qwen2-VL）同样表现不佳，进一步确认了专用SLAM管道与LLM组合的设计优势。

**扩散模型修补的作用**：消融实验还验证了基于视频扩散先验的修补模块对最终视频质量的关键贡献。移除扩散修补后，渲染结果中的遮挡/未知区域无法得到合理补全，导致LPIPS和FID显著恶化。

### 定性分析

Figure 4展示了文本控制相机运动的定性结果，OmniCam能够准确执行指定角度的方向移动、旋转以及复合运动，生成视频在时空一致性上表现良好。Figure 5展示了视频引导的轨迹迁移效果，OmniCam成功将输入视频的相机轨迹提取并迁移到输出视频中，保持了运动模式的保真度。

Figure 6的雷达图从八个维度（集成灵活性、开源、生成速度、视频操控、泛化性、易用性、复杂指令支持、视频轨迹支持）对比了OmniCam与领域专用模型，OmniCam在集成灵活性和复杂指令支持方面具有明显优势。

### 失败模式与局限性

尽管OmniCam在整体性能上表现优异，但仍存在若干失败模式和局限性：

1. **强化学习优化的不稳定性**：RL带来的提升幅度较小且可能随随机种子波动，其在不同任务和随机种子上的表现一致性有待进一步验证。

2. **复杂场景中的遮挡恢复**：当单目重建点云不完整时，扩散模型对遮挡区域的恢复可能出现瑕疵，尤其在场景结构复杂或相机运动幅度较大时更为明显。

3. **数据集规模的限制**：OmniTr数据集目前包含1000条轨迹，虽然已覆盖全部运动属性，但在极开放场景下的泛化能力可能受限于数据规模。

4. **评估标准的局限性**：相机控制领域尚无统一评估标准，现有定量比较存在局限性，部分定性比较仍依赖人工评测。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_02312/figures/004_Table_1.jpg]]
*Table 1: Comparison of other datasets with OmniTr. None of the other datasets include textual descriptions of the trajectories. T in the table stands for Text*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2504_02312/figures/014_Table_4.jpg]]
*Table 4: Comparison of Content and Trajectory Reference Capabilities*

## 定位与知识库关联

### 问题定位与核心瓶颈

相机可控视频生成旨在根据用户指定的相机运动轨迹，从单张或多张参考图像合成时空一致的视频序列。现有方法面临两个根本性瓶颈：

1.  **输入模态的割裂**：当前方法通常仅支持单一轨迹输入模态——要么是预定义的数值轨迹，要么是文本描述，缺乏对文本、视频、直接轨迹等多种输入的联合支持。这种割裂严重限制了用户的交互灵活性与应用场景的覆盖范围。
2.  **控制粒度与空间一致性的矛盾**：基于深度变形的方法（如 **LucidDreamer**）在较大视角变化下易产生空间结构扭曲；基于扩散模型的方法（如 **CameraCtrl**、**MotionCtrl**）虽能生成高质量画面，但通常只提供粗略的关键帧控制，难以实现帧级的精确速度、方向与旋转调节。此外，现有数据集（如 RealEstate）仅包含视频与对应轨迹，缺乏文本描述与离散运动表示，无法支撑多模态轨迹理解模型的训练。

OmniCam 的核心洞察在于：将相机轨迹解耦为**离散运动表示**——即 `<starttime, endtime, speed, direction, rotate>` 序列——作为多模态输入与精确相机控制之间的中间桥梁。通过组合单目重建提供的几何先验与视频扩散模型的生成先验，OmniCam 首次实现了文本、视频和轨迹任意输入组合下的帧级相机控制与时空一致视频生成。

### 方法谱系与基线对比

OmniCam 处于相机可控视频生成、新视角合成与多模态轨迹理解的交叉地带。以下从控制机制、模态支持与生成质量三个维度，将其与代表性基线进行系统对比。

**与基于扩散模型的相机控制方法对比**：

- **CameraCtrl** 通过将相机嵌入注入预训练视频扩散模型实现相机控制，但其控制粒度受限于预定义的关键帧轨迹，无法处理文本或视频形式的轨迹输入。在 OmniTr 测试集上，CameraCtrl 的旋转误差（RotErr）高达 6.423，平移误差（TransErr）为 5.792，而 OmniCam 分别降至 1.066 和 2.731（Table 3），表明离散运动表示与轨迹规划算法的组合显著提升了控制的精确性。
- **MotionCtrl** 同样采用相机嵌入控制，但仅支持基础的平移运动，缺乏对旋转、速度变化及复合运动的支持。OmniCam 通过 `<direction, rotate, speed>` 三元组的显式建模，覆盖了任意方向的复合运动与帧级速度调节。
- **CamI2V** 作为图像到视频的相机控制基线，在生成质量上表现一般，其 FID 为 69.4，而 OmniCam 降至 24.26（Table 3），反映出单目重建初始化与扩散修补相结合的策略在保持时空一致性方面的优势。

**与基于深度变形的新视角合成方法对比**：

- **LucidDreamer** 通过深度估计与点云变形生成新视角，但在大角度旋转或复杂轨迹下，点云的空洞与变形伪影会导致严重的空间扭曲。OmniCam 同样依赖单目重建（DUSt3R）获取初始视图，但关键区别在于：OmniCam 将渲染结果视为带空洞的“粗视图”，随后利用视频扩散模型的先验知识进行补全，而非直接插值或变形。这一设计使得 OmniCam 在 LPIPS（0.167 vs. 0.291）和 PSNR（22.14 vs. 18.37）上显著优于 CameraCtrl（Table 3），间接验证了扩散先验对几何重建误差的容忍与修复能力。
- **ZeroNVS** 作为零样本新视角合成方法，在未见场景上具有泛化优势，但其缺乏对相机轨迹的显式控制能力，无法按用户指定的运动序列生成视频。

**多模态轨迹理解的能力边界**：

在文本到轨迹的生成任务中，OmniCam 采用 Llama 骨干网络微调，在轨迹平均准确率上达到 80.171（Table 2），并支持帧级时间、速度、方向、旋转的全面评估。消融实验揭示了两个关键发现：

1.  **LLM vs. VLM**：使用视觉语言模型 Qwen2-VL 替代纯文本 LLM 处理文本输入，轨迹准确率从 80.171 降至 72.976（Table 2），表明在纯文本轨迹理解任务中，LLM 的语义解析能力优于 VLM 的多模态融合能力。
2.  **视频轨迹提取的路径依赖**：Llama+SLAM 组合在视频引导的轨迹提取中显著优于纯 SLAM 和 SIFT 方法（Table 2），验证了平滑模块与坐标映射的必要性——原始 SLAM 轨迹包含高频噪声，直接映射为离散运动表示会导致运动属性预测失准。

### 适用边界与局限

尽管 OmniCam 在多模态相机控制上取得了显著进展，其适用边界仍受以下因素制约：

1.  **遮挡区域的恢复质量**：单目重建（DUSt3R）在复杂场景中可能产生不完整的点云，导致渲染视图中出现大面积未知区域。虽然扩散模型能补全部分空洞，但在严重遮挡条件下（如物体自遮挡或视角剧烈变化），补全结果可能出现纹理模糊或语义不一致的伪影（Section 7.8）。这一局限根植于单目深度估计的固有不确定性，而非扩散模型的能力上限。
2.  **强化学习优化的增益有限**：端到端 RL 微调（PPO）仅将轨迹平均准确率从 78.341 提升至 80.171（Table 2, w/o RL vs. Llama），增益幅度较小且可能随随机种子波动（Section 5.3）。这表明上游轨迹大模型与下游扩散修补模型之间的梯度耦合较弱，RL 信号难以有效穿透冻结的扩散模型反向传播至 LLM 参数。
3.  **数据集的规模与多样性瓶颈**：OmniTr 数据集包含 1000 条轨迹、10k 条文本描述和 30k 个视频（Table 1），虽已覆盖全部运动属性，但相比大规模视频生成数据集仍显有限。在极开放场景（如非刚性物体、动态背景）中，模型的泛化能力可能受限于训练数据的分布覆盖。
4.  **评估标准的缺失**：相机控制领域尚无统一的定量评估标准。现有指标（RotErr、TransErr）仅衡量轨迹精度，而生成质量指标（LPIPS、FID）无法解耦相机控制精度与画面真实性的贡献。人工评测仍是定性比较的主要手段，这为方法的公平对比带来了挑战（Section 7.7）。

### 开放问题

OmniCam 的设计选择与实验发现引出了若干值得进一步探索的方向：

1.  **RL 优化的稳定性与可扩展性**：当前 RL 提升幅度较小且不稳定，能否通过改进奖励设计（如引入判别器或 CLIP 空间的一致性约束）或采用更高效的对齐策略（如 DPO）来增强上下游耦合？在不同随机种子和任务类型上，RL 增益的一致性如何？
2.  **统一评估基准的建立**：能否设计一个综合指标，同时衡量相机轨迹精度、画面真实性与时空一致性？例如，结合位姿估计误差与感知质量指标的多维评分体系，或构建包含多样化轨迹与场景的标准测试集。
3.  **动态场景的扩展**：OmniCam 当前假设场景为静态，仅控制相机运动。能否将其框架扩展到动态场景中，同时控制相机运动与物体运动？这需要在离散运动表示中引入物体运动基元，并设计相应的轨迹规划与修补策略。
4.  **严重遮挡的鲁棒处理**：当单目重建点云不完整时，能否引入多帧信息聚合或显式的不确定性建模来改善遮挡区域的恢复？例如，结合视频帧间的光流信息或采用基于不确定性的条件扩散模型。
5.  **更大规模数据集的构建**：如何高效扩展 OmniTr 数据集，覆盖更多样化的场景类型、运动模式与文本描述风格？自动化标注管线（如利用 VLM 生成轨迹描述）可能是一个可行的方向，但需谨慎处理标注噪声与质量控制的权衡。

## 原文 PDF

![[paperPDFs/arxiv_2025/OmniCam_Unified_Multimodal_Camera_Control_for_Video_Generation.pdf]]
