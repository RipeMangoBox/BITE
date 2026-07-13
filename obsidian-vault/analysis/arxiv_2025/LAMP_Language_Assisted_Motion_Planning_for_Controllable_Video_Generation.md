---
title: "LAMP: Language-Assisted Motion Planning for Controllable Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/LAMP_Language_Assisted_Motion_Planning_for_Controllable_Video_Generation.pdf
project_link: https://cyberiada.github.io/LAMP/
code_link: null
aliases:
- LAMP
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过LLM将自然语言描述转化为电影摄影启发的符号化运动DSL程序，再确定性地映射为3D轨迹，从而实现对物体和摄像机运动的精确控制。
primary_logic: 将运动控制重构为语言到程序的合成问题，利用LLM的推理能力生成结构化的、可解释的运动程序，在统一的3D空间中规划物体和摄像机运动，以电影摄影语义驱动视频生成。
claims:
- LAMP在DataDoP数据集上的摄像机轨迹F1分数达到0.763，远超GenDoP专有训练的0.400，无需任何数据集特定训练。
- 在ET数据集的两个难度分割上，LAMP均取得最高F1分数（纯场景0.976，混合场景0.769），展现出强大的泛化能力。
- 使用DSL程序预测的物体运动精确度（细粒度平移F1 0.966）显著高于直接轨迹回归（0.781）。
- 在用户研究中，52%的参与者认为LAMP生成的整体视频质量更好，在摄像机跟随、物体跟随方面均被一致偏好。
---

# LAMP: Language-Assisted Motion Planning for Controllable Video Generation

> [!tip] 核心洞察
> 将运动控制重构为语言到程序的合成问题，利用LLM的推理能力生成结构化的、可解释的运动程序，在统一的3D空间中规划物体和摄像机运动，以电影摄影语义驱动视频生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | LAMP：面向可控视频生成的语言辅助运动规划 |
| 英文题名 | LAMP: Language-Assisted Motion Planning for Controllable Video Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.03619) · [Project](https://cyberiada.github.io/LAMP/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LAMP |
| Dataset | DataDoP, ET, Procedural Dataset, User Study |

> [!tip] 效果简介
> - DataDoP 上，F1-Score (Revised) 0.763 (Ours pretrained) vs 0.400 (GenDoP DataDoP trained) (+0.363)。
> - ET (Pure) 上，F1-Score 0.976 vs best baseline (lower) (显著提升)。
> - ET (Mixed) 上，F1-Score 0.769 vs best baseline (lower) (显著提升)。

## 概要

现有视频生成框架在运动控制方面存在关键瓶颈：用户难以通过自然、高效的方式同时指定物体和摄像机的三维运动轨迹，导致生成结果与创作意图之间的对齐度不足。LAMP（Language-Assisted Motion Planning）将这一挑战重构为**语言到程序的合成问题**，利用大语言模型的推理能力，将自然语言描述转化为电影摄影启发的符号化运动DSL程序，再确定性地映射为3D轨迹，从而在统一的共享空间内实现对物体和摄像机运动的精确控制。

核心结论是：通过引入结构化的、可解释的运动程序作为中间表示，LAMP无需在目标真实数据集上进行特定训练，即可在多个基准上取得显著优于现有专有训练方法的运动控制精度。在DataDoP数据集上，LAMP的摄像机轨迹F1分数达到0.763，远超GenDoP专有训练的0.400（Table 1）；在ET数据集的两个难度分割上，LAMP均取得最高F1分数（纯场景0.976，混合场景0.769），展现出强大的泛化能力（Table 2）。用户研究进一步表明，52%的参与者认为LAMP生成的整体视频质量更好，在摄像机跟随和物体跟随方面均被一致偏好（Figure 6）。

方法定位上，LAMP区别于直接回归逐帧摄像机坐标的现有方案（如**CCD**（Jiang et al., EG 2024）、**GenDoP**（Zhang et al., ICCV 2025）），以及仅规划摄像机轨迹的方法（如**E.T.**（Courant et al., ECCV 2024）），通过电影摄影语义驱动的DSL程序和LLM运动规划器，实现了物体与摄像机的联合轨迹生成与迭代细化。

可控视频生成旨在根据用户提供的条件信号（如文本、图像、轨迹）合成动态视觉内容。近年来，扩散模型驱动的文本到视频（T2V）生成取得了显著进展，但在运动控制方面仍存在一个核心瓶颈：**用户难以通过自然、高效的方式同时指定物体和摄像机的3D运动轨迹**，导致生成结果与用户意图之间难以对齐。

现有方法在运动控制上存在三个关键缺口。其一，**控制接口不够自然**。以 **CCD**（Jiang et al., EG 2024）、**GenDoP**（Zhang et al., ICCV 2025）为代表的摄像机轨迹生成方法，通常要求用户直接指定摄像机参数或从视频/草图中提取运动信号，而非通过自由形式的自然语言进行描述。其二，**运动规划范围受限**。大多数方法仅规划摄像机轨迹，将物体视为静态或隐式建模，缺乏在共享3D空间中统一规划物体与摄像机运动的能力。**E.T.**（Courant et al., ECCV 2024）虽同时处理摄像机和角色轨迹，但仍依赖文本条件驱动，未能充分利用结构化的运动语义。其三，**运动表示缺乏可解释性**。主流方法多采用逐帧摄像机坐标的连续回归或离散分类，这种低层表示难以捕捉电影摄影层面的运动意图，也不利于迭代细化和用户交互。

上述缺口的根本原因在于：**运动控制被建模为低层轨迹回归问题，而非高层语义理解与规划问题**。这导致两个后果——模型需要大量特定数据集的标注训练，泛化能力受限；用户无法用自然语言表达复杂的电影摄影意图（如“摄像机绕物体旋转的同时缓慢拉远”），系统也缺乏将这种意图精确映射为3D轨迹的机制。

LAMP 的动机正是弥合这一鸿沟：**将运动控制重构为语言到程序的合成问题**，利用大语言模型（LLM）的推理能力，从自然语言描述中生成结构化的、电影摄影启发的符号化运动程序，再确定性地转换为3D轨迹，从而在统一的3D空间中实现对物体和摄像机运动的精确、可解释控制。

## 核心方法与创新机理

LAMP 的核心创新在于将视频生成中的运动控制重构为一个**语言到程序的合成问题**，通过引入电影摄影启发的领域特定语言（DSL）和基于大语言模型（LLM）的运动规划器，在统一的 3D 空间中实现对物体和摄像机运动的精确、可解释控制。与现有方法相比，LAMP 在三个关键维度上实现了根本性改变：

### 1. 运动表示：从连续回归到符号程序合成

现有方法（如 **CCD**（Jiang et al., EG 2024）、**GenDoP**（Zhang et al., ICCV 2025））通常将运动轨迹建模为逐帧摄像机坐标的连续回归或离散分类问题，这种数值化的表示方式缺乏语义可解释性，且对 LLM 的推理能力利用不足。

LAMP 将运动规划转化为**电影摄影启发的 DSL 符号程序生成**（Section 3.2, 3.3）。该 DSL 编码了典型的电影摄影运动原语（如 `orbit_track`、`tail_track`、`free_form`）及其组合修饰符，再通过确定性转换器将符号程序映射为 3D 轨迹。消融实验（Table 4）提供了决定性证据：DSL 符号程序生成的物体运动细粒度平移 F1 达到 0.966，而直接轨迹回归仅为 0.781（+0.185），表明 LLM 在结构化符号程序上的推理效率远高于直接数值回归。

### 2. 运动规划范围：从单一摄像机到物体-摄像机联合规划

现有方法通常仅规划摄像机轨迹，物体运动要么是静态的，要么通过隐式方式建模。**E.T.**（Courant et al., ECCV 2024）虽然同时涉及摄像机和角色轨迹，但其控制接口和表示方式与 LAMP 有本质区别。

LAMP 在**共享 3D 空间中统一规划物体和摄像机轨迹**（Section 3.1, 3.5），并将运动规划分解为反映电影摄影层次的条件概率分布：

$$p ( \mathbf { s } _ { \mathrm { c a m } } , \mathbf { s } _ { \mathrm { o b j } } | \mathbf { t } ) : = p ( \mathbf { s } _ { \mathrm { o b j } } | \mathbf { t } _ { \mathrm { o b j } } ) p ( \mathbf { s } _ { \mathrm { c a m } } | \mathbf { s } _ { \mathrm { o b j } } , \mathbf { t } _ { \mathrm { c a m } } )$$

这一分解体现了“物体优先”的电影摄影原则：先确定物体的运动轨迹，再基于物体运动规划摄像机的相对运动。在程序化数据集上，物体运动的粗粒度平移 F1 高达 0.9983，旋转 F1 达到 0.975（Table 3），验证了联合规划框架的有效性。

### 3. 控制接口：从参数指定到自然语言迭代细化

现有方法的控制接口通常要求用户直接指定摄像机参数（如坐标序列、视角角度）或从视频/草图提取运动信息，使用门槛高且缺乏灵活性。

LAMP 提供**自然语言控制接口**（Section 3.5, 3.6），用户通过自然语言描述场景中的物体和摄像机运动意图，LLM 作为运动规划器生成 DSL 程序，并支持通过简单的文本指令进行**迭代细化**（Figure 4）。用户研究（Figure 6）显示，52% 的参与者认为 LAMP 生成的整体视频质量更好，在摄像机跟随和物体跟随方面均被一致偏好，相比基线有 27% 的偏好优势（52% vs 25% both）。

### 创新点的因果机制

这三个创新点构成了一个完整的因果链条：**DSL 符号表示**为 LLM 提供了结构化的推理空间，使其能够有效捕捉电影摄影语义；**联合规划框架**确保了物体与摄像机运动的空间一致性；**自然语言接口**降低了使用门槛，使非专业用户也能精确控制复杂的 3D 运动。这一设计使得 LAMP 在未使用目标数据集训练的情况下，在 DataDoP 数据集上的摄像机轨迹 F1 分数达到 0.763，远超 GenDoP 专有训练的 0.400（Table 1），展现出强大的零样本泛化能力。

LAMP 将运动控制重构为一个**语言到程序的合成问题**，其核心思路是：利用大语言模型（LLM）的推理能力，将用户提供的自然语言运动描述转化为结构化的、电影摄影启发的符号化运动程序，再确定性地映射为 3D 轨迹，最终驱动视频生成。整个框架由四个顺序模块构成，形成一条从文本到视频的端到端可控管线（见图 2）。

### 管线模块与数据流

1.  **Motion Planner (LLM)**  
    接收用户对场景中物体和摄像机运动的自然语言描述 $\mathbf{t}$，生成符号化的 DSL 程序 $(\mathbf{s}_{\mathrm{obj}}, \mathbf{s}_{\mathrm{cam}})$。该模块将运动规划建模为条件生成问题，其联合分布分解为物体运动条件概率与摄像机运动条件概率的乘积：
    $$p ( \mathbf { s } _ { \mathrm { c a m } } , \mathbf { s } _ { \mathrm { o b j } } | \mathbf { t } ) : = p ( \mathbf { s } _ { \mathrm { o b j } } | \mathbf { t } _ { \mathrm { o b j } } ) p ( \mathbf { s } _ { \mathrm { c a m } } | \mathbf { s } _ { \mathrm { o b j } } , \mathbf { t } _ { \mathrm { c a m } } )$$
    这一分解反映了电影摄影中“物体运动优先于摄像机运动”的层次化语义。LLM 以自回归方式逐 token 生成运动标签，利用已生成的上下文保持长程时序一致性，并天然保证输出程序的语法合法性（Section 3.5）。该模块还支持通过简单的文本指令对已生成的轨迹进行**迭代细化**（Figure 4）。

2.  **DSL-to-Trajectory Converter**  
    将 LLM 生成的符号化 DSL 程序**确定性地转换**为 3D 空间中的物体轨迹和摄像机轨迹。DSL 本身包含运动原语（如 `orbit_track`、`free_form`）和修饰符（如速度、方向、目标点），转换器根据这些结构化指令精确计算每一帧的 6-DoF 摄像机位姿和物体位移（Section 3.4, 3.6）。这种确定性映射保证了运动规划的可解释性和可复现性。

3.  **Control Video Renderer**  
    将 3D 轨迹渲染为帧对齐的**控制视频**——通常是将物体边界框、运动箭头等 2D 投影叠加到空白或参考帧上，形成稠密的运动条件信号（Section 3.6）。

4.  **Video Generator**  
    以控制视频为条件，调用预训练的视频生成模型（如 VACE）生成最终视频。该模块是**即插即用**的：DSL 框架可与多种现成模型（CameraCtrl、EPiC、ReCamMaster）集成，展示了其通用性（Figure 11）。

### 关键设计决策

- **统一 3D 运动空间**：与以往仅规划摄像机轨迹或将物体视为静态的工作不同，LAMP 在共享的 3D 坐标系中同时规划物体和摄像机的运动，使二者能够产生物理一致的交互（如摄像机跟随运动物体）。
- **符号化中间表示**：选择 DSL 程序而非直接回归逐帧坐标，是 LAMP 性能优势的因果杠杆。消融实验表明，DSL 程序预测的物体运动细粒度平移 F1 达到 0.966，而直接轨迹回归仅为 0.781（Table 4），验证了 LLM 在结构化符号程序上的推理效率远高于连续数值回归。
- **无需真实数据训练**：Motion Planner 仅在程序化合成数据上预训练，即可在真实数据集（DataDoP、ET）上取得超越专有训练基线的泛化性能（Table 1, Table 2），体现了 DSL 作为强归纳偏置的迁移能力。

### 当前局限

框架目前仅支持**单个物体和单台摄像机**的运动规划；LLM 生成的 DSL 程序偶有语法或语义错误（整体失败率约 0.11%）；视频生成器对控制信号的依从性有时不足，导致最终视频中的运动与预期存在偏差。多物体交互轨迹生成和端到端一体化留作未来工作。

### 补充图表

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/002_Figure_2.jpg]]
*Figure 2: Overview of LAMP. A learned LLM acts as a motion planner, generating symbolic motion programs in a DSL format from textual descriptions of object and camera motion. These programs are deterministically converted into 3D trajectories, which are used to condition a pretrained video generator*

### 3.1 整体框架与运动规划器

LAMP 将运动控制重构为**语言到程序的合成问题**，核心是一个经过微调的自回归大语言模型 $\mathcal{F}_{\theta}$，作为运动规划器接收自然语言描述 $\mathbf{t}$，输出结构化的符号运动程序：

$$p ( \mathbf { s } _ { \mathrm { c a m } } , \mathbf { s } _ { \mathrm { o b j } } | \mathbf { t } ) : = p ( \mathbf { s } _ { \mathrm { o b j } } | \mathbf { t } _ { \mathrm { o b j } } ) p ( \mathbf { s } _ { \mathrm { c a m } } | \mathbf { s } _ { \mathrm { o b j } } , \mathbf { t } _ { \mathrm { c a m } } )$$

该公式将运动规划分解为两个条件概率：
- **物体运动** $\mathbf{s}_{\mathrm{obj}}$ 仅以物体描述文本 $\mathbf{t}_{\mathrm{obj}}$ 为条件；
- **摄像机运动** $\mathbf{s}_{\mathrm{cam}}$ 同时以物体运动程序和摄像机描述文本 $\mathbf{t}_{\mathrm{cam}}$ 为条件。

这一分解反映了电影摄影中“物体优先”的运动层次——摄像机的运动通常围绕物体的运动展开。

### 3.2 运动 DSL 与符号程序

运动程序采用受电影摄影惯例启发的领域特定语言（DSL）表达。DSL 扩展了 CameraBench 的分类体系，编码了规范化的摄像机运动原语和组合修饰符。

**物体运动序列**定义为最多 $N \leq 4$ 个运动标签：

$$\mathbf { s } _ { \mathrm { o b j } } : = \{ s _ { \mathrm { o b j } } ^ { 0 } , \dots , s _ { \mathrm { o b j } } ^ { N - 1 } \}$$

**摄像机运动序列**支持完整的 6 自由度控制，自由形式时同样最多 4 个标签：

$$\mathbf { s } _ { \mathrm { c a m } } : = \{ s _ { \mathrm { c a m } } ^ { 0 } , \dots , s _ { \mathrm { c a m } } ^ { N - 1 } \}$$

每个运动标签由原语类型和一组 `key=value` 格式的修饰符组成。LLM 在生成时以先前生成的 token 和上下文为条件，强制施加长程时序一致性，并保证输出语法有效的 DSL 程序。

### 3.3 流水线模块

LAMP 包含四个关键模块，按数据流顺序为：

1. **Motion Planner (LLM)**：接收自然语言描述，将输入分解为物体中心和摄像机中心两个部分，生成对应的符号 DSL 程序（Section 3.5）。
2. **DSL-to-Trajectory Converter**：将 DSL 程序确定性转换为 3D 轨迹——包括物体轨迹和摄像机轨迹（Section 3.4, 3.6）。
3. **Control Video Renderer**：将 3D 轨迹渲染为帧对齐的控制视频（2D 投影叠加），作为视频生成器的条件输入（Section 3.6）。
4. **Video Generator**：以控制视频为条件生成最终视频，LAMP 框架可与多种现成模型（如 VACE、CameraCtrl、EPiC、ReCamMaster）集成（Section 3.6, Figure 11）。

### 3.4 关键设计选择

**DSL 符号程序 vs 直接轨迹回归**是 LAMP 的核心设计决策。消融实验（Table 4）表明，DSL 方法在细粒度平移 F1 上达到 0.966，而直接轨迹回归仅为 0.781（提升 +0.185）。这一差距说明 LLM 在结构化符号程序上的推理比在连续数值轨迹上的回归更有效——符号空间更稀疏、更可解释，且天然排除了无效轨迹的生成。

**物体-摄像机联合规划**是另一个关键创新。传统方法通常仅规划摄像机轨迹，物体为静态或隐式建模。LAMP 在共享 3D 空间中统一规划两者，使得摄像机可以围绕运动物体进行“轨道跟踪”（orbit_track）、“尾部跟踪”（tail_track）等电影摄影行为，从而生成物理一致且语义连贯的摄像机-物体交互（Section 3.1, 3.5）。

### 补充图表

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/004_Figure_4.jpg]]
*Figure 4: LAMP allows iterative control over synthesized motion trajectories via simple textual instructions. We visualize the 3D trajectories converted from the LLM predicted motion programs*

## 实验与关键发现

### 评估设置与基准

LAMP在三个互补的基准上接受评估：**DataDoP**（真实视频的摄像机轨迹）、**ET**（Emerging Trajectories，包含纯场景和混合场景两个难度分割）以及一个自建的**程序化合成数据集**（用于物体运动评估）。所有对比基线均在相同评估协议下测试，LAMP未在任何目标真实数据集上进行特定训练——仅使用程序化合成数据预训练LLM运动规划器。修订后的F1指标消除了重构偏差，确保公平比较。

基线方法涵盖文本条件轨迹生成的主要范式：**CCD**（Jiang et al., EG 2024）用于摄像机轨迹生成，**E.T.**（Courant et al., ECCV 2024）同时生成摄像机和角色轨迹，**Director3D**（Li et al., NeurIPS 2024）生成摄像机轨迹和3D场景，**GenDoP**（Zhang et al., ICCV 2025）采用自回归方式生成摄像机轨迹。

### 摄像机轨迹控制：跨数据集泛化优势

在DataDoP数据集上，LAMP以**0.763的Revised F1分数**显著超越所有基线（Table 1/5）。尤其值得注意的是，GenDoP在DataDoP上专有训练后仅取得0.400，而LAMP无需任何数据集特定训练即实现**+0.363的绝对提升**。这一结果直接验证了将运动控制重构为符号程序合成问题的核心洞察——LLM对结构化DSL程序的推理能力天然具备更强的泛化性，无需依赖特定数据分布的回归拟合。

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/007_Table_1.jpg]]
*Table 1: Camera trajectory evaluation on the DataDoP dataset. LAMP achieves superior performance than DataDoP-trained baselines despite no dataset-specific training*

在ET数据集上，LAMP在纯场景分割取得**0.976 F1**，混合场景分割取得**0.769 F1**，均为最高分（Table 2/6）。ET的混合分割包含更复杂的运动模式组合，是未见过的难度级别，LAMP在此场景下的领先优势表明DSL框架对运动复杂度的鲁棒性——符号化运动原语的组合泛化能力远超连续轨迹回归方法。

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/005_Table_2.jpg]]
*Table 2: Camera trajectory results on the ET dataset. The ET benchmark includes a simpler pure and a harder mixed split. LAMP attains the highest F1-scores on both, demonstrating strong generalization across (unseen) motion complexity levels*

### 物体运动控制：DSL符号推理的决定性作用

在程序化数据集的物体运动评估中（Table 3），LAMP在粗粒度平移上达到**0.9983 F1**，细粒度平移**0.9293 F1**，旋转**0.975 F1**，展现了近乎完美的运动类型识别能力。这得益于DSL将物体运动编码为最多4个运动标签的序列 $\\mathbf{s}_{\\mathrm{obj}} := \\{ s_{\\mathrm{obj}}^{0}, \\dots, s_{\\mathrm{obj}}^{N-1} \\}$，每个标签明确指定运动原语和修饰符，消除了连续回归中的模糊性。

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/006_Table_3.jpg]]
*Table 3: Object motion evaluation on the test split of our procedural dataset*

消融实验（Table 4）揭示了DSL框架的关键因果机制：**DSL符号程序生成相比直接轨迹回归，将细粒度平移F1从0.781提升至0.966（+0.185）**。直接回归要求LLM输出连续数值坐标，模型容易产生方向混淆和累积误差；而DSL将运动规划转化为离散符号的分类与组合问题，LLM只需推理运动语义（如"从左向右平移"），确定性转换器再将其映射为精确的3D轨迹。这证明了"结构化符号程序作为中间表示"是运动控制精度提升的瓶颈因素。

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/010_Table_4.jpg]]
*Table 4: DSL vs trajectory ablation on the procedural dataset*

### 真实数据微调的边际收益

在DataDoP上使用DSL转换后的真实数据进行微调，仅带来轻微提升（Revised F1从0.763到0.776，Table 5）。这表明预训练模型已具备很强的泛化能力，真实数据的噪声和标注不精确性反而可能引入干扰。DSL转换本身对真实轨迹的平滑作用（Figure 9）在一定程度上弥合了合成-真实域差距，使得额外训练收益有限。

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/016_Table_5.jpg]]
*Table 5: Camera trajectory evaluation on the DataDoP dataset. LAMP achieves performance comparable to DataDoP-trained baselines despite no dataset-specific training*

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/013_Figure_9.jpg]]
*Figure 9: Using real data for training. Samples from real datasets (e.g., DataDoP) are converted to our DSL format via motion tagging and optionally re-captioned. The DSL conversion smooths the noisy trajectories extracted from real videos and improves alignment between textual descriptions and motion*

### 用户研究：端到端感知质量验证

用户研究（Figure 6）从感知层面验证了定量指标的生态效度。参与者在摄像机依从性、物体依从性和整体视频质量三个维度上一致偏好LAMP：**52%的参与者认为LAMP生成的整体视频质量更好**，而认为两者相当的仅25%。这一27%的偏好差距表明，DSL驱动的运动规划不仅在轨迹精度上占优，其生成的视频在视觉连贯性和意图对齐度上也更符合人类预期。

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/009_Figure_6.jpg]]
*Figure 6: User study results. We compare LAMP against baseline methods in a qualitative user study. Participants consistently preferred our results in terms of camera adherence, object adherence, and overall video quality, demonstrating stronger alignment between textual descriptions and generated motion*

### 失败模式与框架通用性

LLM生成的DSL程序偶尔出现错误，整体失败率约**0.11%**（每10k样本约3次运动类型混淆和8次无效标签），可能导致不合逻辑的轨迹。此外，视频生成器对控制视频的依从性有时不足——即使轨迹正确，最终视频中的运动仍可能与预期存在偏差，这暴露了条件注入机制的瓶颈。

DSL框架的通用性在Figure 11中得到验证：LAMP的运动规划输出可无缝集成到**CameraCtrl**、**EPiC**、**ReCamMaster**等多种现成视频生成模型中，覆盖T2V、I2V、V2V不同范式，表明DSL轨迹作为中间表示具有模型无关的即插即用特性。

### 局限与待验证边界

当前框架仅支持单个物体和摄像机的运动规划，多物体交互轨迹生成留作未来工作。DSL虽然具有表现力，但可能无法覆盖所有复杂的电影摄影技巧（如非线性、超长镜头中的复杂互动）。在模糊或未充分指定的自然语言输入下，LLM的鲁棒性仍需进一步增强——这需要更大规模、更多样化的程序化训练数据覆盖边缘情况。

### 补充图表

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results of LAMP. For each example, we show user-provided text prompts describing object + camera motion, corresponding DSL-based motion programs synthesized by our LLM, the resulting 3D object and camera trajectories, and generated video frames. For the first example, we also show the control video given to VACE as an inset. These showcase that LAMP produces coherent and physically consistent camera–object interactions across diverse scenarios. See supplemental webpage for videos and comparisons*

![[assets/figures/papers/paper_list_l97_https_arxiv_org_abs_2512_03619/figures/017_Figure_11.jpg]]
*Figure 11: DSL w/ CameraCtrl, EPiC, and ReCamMaster. DSL applied to multiple off-the-shelf models (T2V, I2V, V2V, respectively)*

## 定位与知识库关联

### 与现有工作的关系

LAMP 的核心贡献在于将可控视频生成中的运动控制问题重构为**语言到程序的合成**任务，这与现有工作的设计哲学形成根本性差异。当前主流方法可归为两类轨迹生成范式：

**直接轨迹回归/分类范式**：**CCD**（Jiang et al., EG 2024）、**GenDoP**（Zhang et al., ICCV 2025）等方法直接从文本条件回归逐帧摄像机坐标或对离散化动作进行分类。这类方法将运动规划视为连续空间的拟合问题，其瓶颈在于：LLM 在数值空间中的推理精度不足，且缺乏对运动语义的结构化约束。LAMP 的消融实验直接验证了这一瓶颈——在程序化数据集上，直接轨迹回归的细粒度平移 F1 仅为 0.781，而 DSL 符号程序生成达到 0.966（Table 4），表明**结构化符号表示是 LLM 发挥推理能力的关键因果旋钮**。

**文本条件轨迹生成范式**：**E.T.**（Courant et al., ECCV 2024）和 **Director3D**（Li et al., NeurIPS 2024）探索了从文本同时生成摄像机和角色/场景轨迹的可能性。然而，这些方法通常在独立的表示空间中处理摄像机和物体运动，缺乏统一的 3D 空间规划。LAMP 在共享 3D 坐标系中联合规划物体和摄像机轨迹，并通过电影摄影启发的分解式概率建模 $p(\mathbf{s}_{\mathrm{cam}}, \mathbf{s}_{\mathrm{obj}} | \mathbf{t}) := p(\mathbf{s}_{\mathrm{obj}} | \mathbf{t}_{\mathrm{obj}}) p(\mathbf{s}_{\mathrm{cam}} | \mathbf{s}_{\mathrm{obj}}, \mathbf{t}_{\mathrm{cam}})$ 体现“物体优先”的运动层次，这在方法论上更贴近真实的电影摄影工作流。

### 适用边界

LAMP 的适用性由以下几个维度界定：

1. **运动复杂度边界**：DSL 支持最多 4 个运动标签的序列组合（$\mathbf{s}_{\mathrm{obj}} := \{s_{\mathrm{obj}}^{0}, \dots, s_{\mathrm{obj}}^{N-1}\}$，$N \leq 4$），覆盖了常见的电影摄影运动原语（自由形式、轨道跟踪、尾随跟踪、旋转跟踪）及其修饰符组合。但对于超出此标签数的超长镜头、非线性复杂互动或多物体协调运动，当前 DSL 的表达力存在上限。

2. **物体数量边界**：当前框架仅支持**单个物体**与摄像机的运动规划。多物体关系轨迹生成被明确列为未来工作，这意味着涉及多角色交互的场景（如对话场景中两个角色的相对运动）不在当前能力范围内。

3. **生成器依赖边界**：LAMP 作为运动规划前端，其最终视频质量受限于下游视频生成器对控制信号的依从性。论文指出视频生成器有时无法完全忠实地执行控制视频中的运动指令，这构成了端到端质量的瓶颈。尽管 DSL 框架已展示与多种现成模型（CameraCtrl, EPiC, ReCamMaster）的集成能力（Figure 11），但生成器的依从性问题仍是系统性能的上限约束。

4. **数据分布边界**：LAMP 在程序化合成数据上预训练，在真实数据集（DataDoP, ET）上展现出无需目标域训练的强泛化能力（DataDoP Revised F1: 0.763 vs GenDoP 专有训练的 0.400）。然而，在 DataDoP 上微调 DSL 转换后的数据仅带来轻微提升（0.763 → 0.776），暗示程序化数据的分布覆盖已接近当前 DSL 的表达极限，进一步突破需要扩展 DSL 的语义粒度或引入更丰富的真实运动模式。

### 局限与开放问题

**已识别的技术局限**：

- **LLM 生成错误**：DSL 程序存在约 0.11% 的整体失败率，表现为运动类型混淆（每 10k 样本 3 次）和无效标签（每 10k 样本 8 次），可能导致不合逻辑的轨迹。这类错误在模糊或未充分指定的自然语言输入下可能进一步放大。

- **电影摄影覆盖不全**：DSL 虽然受电影摄影惯例启发，但可能无法覆盖所有复杂技巧，特别是涉及非线性节奏变化、多主体交互或长镜头内多次运动模式切换的场景。

- **非端到端流水线**：DSL 轨迹需手动输入视频生成器，缺乏从语言到视频的一体化优化，限制了运动规划与视觉生成之间的联合微调可能性。

**开放研究问题**：

1. **鲁棒性增强**：如何提升 LLM 在模糊、歧义或信息不足的自然语言输入下的运动规划鲁棒性？这涉及对未充分指定运动参数的合理推断机制。

2. **DSL 表达能力扩展**：如何扩展 DSL 以支持更复杂、新颖或高动态的运动模式，同时保持符号程序的可解释性和确定性转换特性？

3. **生成器依从性改善**：如何通过微调视频生成模型或设计更紧密的条件注入机制来提升对运动控制信号的依从性？这需要运动规划与视觉生成之间的更深层耦合。

4. **多物体交互自动化**：如何从单物体运动规划扩展到多物体交互轨迹的自动生成，同时保持物理一致性和电影摄影合理性？

5. **统一创作流水线**：如何将迭代运动细化过程与外观控制、场景布局等其他创作维度相结合，实现更全面的文本驱动视频创作系统？

## 原文 PDF

![[paperPDFs/arxiv_2025/LAMP_Language_Assisted_Motion_Planning_for_Controllable_Video_Generation.pdf]]
