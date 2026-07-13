---
title: "EagleVision: A Dual-Stage Framework with BEV-grounding-based Chain-of-Thought for Spatial Intelligence"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EagleVision_A_Dual_Stage_Framework_with_BEV_grounding_based_Chain_of_Thought_for_Spatial_Intelligence.pdf
project_link: "https://wallelwan.github.io/EagleVision"
code_link: null
aliases:
- EagleVision
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过BEV地图上的主动姿态查询，模型可在推理过程中动态获取验证空间假设所需的特定视点，形成假设-观察-验证的闭环。
primary_logic: 将空间推理形式化为BEV-grounded姿态查询，并利用纯强化学习（无需人工CoT标注）训练查询策略，使模型能够根据当前信念请求最具信息量的视点。
claims:
- EagleVision在VSI-Bench上以63.5分超越所有开源VLM，比基线Qwen3-VL-8B提升+4.1分。
- 在SQA3D上取得60.3% EM@1，比Struct2D、Spatial-MLLM和Spatial-Mind分别高出1.8%、4.4%和14.0%。
- 消融实验表明，每个组件（Spatial MCoT、BEV grounding、SPF-DPP）均带来显著增益，三个组件相互补充，最终从59.4提升到63.5。
- 框架对位姿噪声具有鲁棒性：中等噪声（5%,5°）下VSI-Bench分数仅下降0.4%，更换SLAM后端为VGGT后性能为63.2（-0.3）。
---

# EagleVision: A Dual-Stage Framework with BEV-grounding-based Chain-of-Thought for Spatial Intelligence

> [!tip] 核心洞察
> 将空间推理形式化为BEV-grounded姿态查询，并利用纯强化学习（无需人工CoT标注）训练查询策略，使模型能够根据当前信念请求最具信息量的视点。

| 字段 | 内容 |
|------|------|
| 中文题名 | EagleVision：面向空间智能的BEV锚定思维链双阶段框架 |
| 英文题名 | EagleVision: A Dual-Stage Framework with BEV-grounding-based Chain-of-Thought for Spatial Intelligence |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.15160) · [Project](https://wallelwan.github.io/EagleVision) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EagleVision |
| Dataset | VSI-Bench, SQA3D |

> [!tip] 效果简介
> - VSI-Bench 上，Overall score 63.5 vs 59.4 (Qwen3-VL-8B) (+4.1)；Overall score 63.5 vs 60.9 (VLM-3R-7B) (+2.6)。
> - SQA3D 上，EM@1 60.3 vs 58.5 (Struct2D) (+1.8)；EM@1 60.3 vs 55.9 (Spatial-MLLM) (+4.4)。

## 概要

### 问题与瓶颈

视频空间推理要求模型理解三维场景中物体的位置、朝向和空间关系。当前多模态大语言模型（MLLMs）在固定token预算下采用统一采样帧进行推理，存在两个根本性缺陷：一是无法主动获取几何信息丰富的额外视点，二是缺乏将抽象空间假设与具体视频帧关联的机制。这导致模型在面对需要多视角验证的空间问题时，只能在有限的初始帧上进行单次文本推理，难以形成可靠的几何判断。

### 核心思路

EagleVision提出了一种**双阶段框架**，将空间推理解耦为宏感知（Macro Perception）与微验证（Micro Verification）两个阶段。其核心洞见在于将空间推理形式化为**BEV锚定的姿态查询过程**：模型在鸟瞰视图（BEV）平面上预测查询姿态，检索最匹配的真实帧，从而形成“假设—观察—验证”的闭环推理。整个查询策略通过**纯强化学习**（GRPO）训练，无需人工标注的思维链数据，仅需答案级别的监督信号。

### 方法定位

EagleVision在方法谱系中处于**主动视觉推理**与**几何感知多模态学习**的交叉点。与现有工作相比，其关键差异体现在四个维度：

- **帧选择策略**：从固定均匀采样升级为SPF-DPP（语义-视角融合行列式点过程），在token预算下联合最大化语义相关性与SE(3)视点多样性。
- **视图获取机制**：从仅使用初始帧升级为BEV锚定的主动姿态查询，使模型能在推理过程中动态请求缺失的观察角度。
- **推理过程**：从单次文本推理升级为迭代空间多模态思维链（Spatial MCoT），包含文本生成、姿态查询、终止回答三种动作。
- **训练机制**：从监督微调升级为基于GRPO的强化学习，以空间接地奖励约束查询的有效性。

在知识库定位上，EagleVision区别于**VLM-3R**（Zheng et al., arXiv 2024）的3D重建编码器融合、**Struct2D**（Zhu et al., arXiv 2025）的结构化2D投影、**Spatial-MLLM**（Wu et al., arXiv 2025）的VGGT空间编码器，以及**Spatial-Mind**（Zhang et al., arXiv 2025）的结构化提示与仿真数据——这些方法均未赋予模型主动选择观察视点的能力。

### 主要结果

EagleVision以**Qwen3-VL-8B**为基础模型，在两项核心基准上取得开源VLM中的最优性能：

- **VSI-Bench**：总体得分**63.5**，较基线Qwen3-VL-8B（59.4）提升+4.1分，较VLM-3R-7B（60.9）提升+2.6分。
- **SQA3D**：EM@1达到**60.3%**，分别超出Struct2D（58.5%）+1.8%、Spatial-MLLM（55.9%）+4.4%、Spatial-Mind（46.3%）+14.0%。

消融实验揭示了各组件的因果贡献：Spatial MCoT单独将基线从59.4提升至61.9（+2.5）；引入BEV grounding进一步提升至62.7（+3.3 over baseline）；叠加SPF-DPP达到最优63.5（+0.8）。三个组件相互补充，验证了“主动查询+几何感知帧选择”的双阶段设计有效性。框架对位姿噪声表现出强鲁棒性：中等噪声（5%平移，5°旋转）下VSI-Bench分数仅下降0.4%，更换SLAM后端为VGGT后性能为63.2（-0.3），表明对底层重建系统的依赖较弱。

### 空间推理：视觉语言模型的核心挑战

空间推理——理解三维场景中物体的位置、朝向、距离和相对关系——是具身智能、自动驾驶和增强现实等应用的基础能力。近年来，多模态大语言模型（MLLMs）在图像和视频理解上取得了显著进展，但在空间推理任务上仍面临根本性瓶颈。以 **Qwen3-VL-8B**（An Yang et al., arXiv 2025）、**LLaVA-OneVision-7B**（Bo Li et al., arXiv 2024）和 **InternVL2-8B**（Zhe Chen et al., arXiv 2024）为代表的开源 VLM，以及 **GPT-4o**（Hurst et al., arXiv 2024）和 **Gemini-1.5 Flash**（Gemini Team et al., arXiv 2024）等闭源模型，在处理需要精确三维几何理解的问题时，性能仍远未令人满意。

### 现有方法的三个结构性缺口

当前视频空间推理方法存在三个相互关联的缺口，共同制约了模型的空间智能水平。

**缺口一：被动帧采样与固定token预算的矛盾。** 现有 MLLMs 通常采用统一采样策略，以固定时间间隔从视频中抽取帧，在预设的 token 预算下一次性输入模型。这种做法隐含假设所有帧对空间推理的贡献是均等的——这一假设在三维场景中显然不成立。某些视点包含丰富的几何信息（如墙角、物体交界处），而另一些视点则提供冗余或模糊的证据。统一采样无法主动获取信息量最大的视点，导致模型在有限的 token 预算内浪费了宝贵的上下文窗口。

**缺口二：缺乏主动视图获取的闭环机制。** 即使模型获得了初始帧，传统方法也仅进行单次前向推理，无法在推理过程中根据当前的空间不确定性主动请求新的观察。人类在进行空间判断时，会自然地移动视点、从不同角度验证假设——例如，走到房间另一侧确认两个物体的前后关系。现有 MLLMs 完全缺乏这种“假设-观察-验证”的闭环能力：**VLM-3R-7B**（Duo Zheng et al., arXiv 2024）通过 3D 重建编码器注入几何先验，**Struct2D**（Fangrui Zhu et al., arXiv 2025）利用结构化 2D 投影，**Spatial-MLLM**（Diankun Wu et al., arXiv 2025）融合 VGGT 空间编码器，**Spatial-Mind**（Haoyu Zhang et al., arXiv 2025）则借助结构化提示和仿真数据——这些方法虽然从不同角度增强了空间感知，但本质上仍是“一次性”推理，无法动态获取缺失的视点信息。

**缺口三：抽象空间假设与具体视频帧的脱节。** 模型在文本空间中进行的空间推理（如“物体A在物体B的左前方”）缺乏与具体视觉证据的锚定机制。当推理链条中出现不确定性时，模型无法将抽象的空间假设转化为可验证的视点查询——它不知道应该“看向哪里”来确认或修正当前的信念。这种脱节使得推理过程悬浮于文本层面，无法从丰富的视频数据中按需提取几何证据。

### EagleVision 的核心洞察

EagleVision 的核心洞察是：**将空间推理形式化为 BEV-grounded 姿态查询，使模型能够在推理过程中动态获取验证空间假设所需的特定视点，形成假设-观察-验证的闭环。** 具体而言，通过预先构建的鸟瞰图（BEV）地图和相机姿态数据库，模型可以将文本推理中的空间不确定性转化为 BEV 平面上的姿态预测，检索最匹配的真实帧作为新的视觉证据。这一机制将抽象的文本推理与具体的几何观察耦合起来，使模型从被动的帧消费者转变为主动的视点采集者。

### 技术路线选择的关键考量

实现上述洞察需要解决两个关键技术挑战。其一，**如何在不依赖人工标注思维链的情况下训练查询策略？** EagleVision 采用基于 GRPO（Group Relative Policy Optimization）的纯强化学习训练，仅需答案级别的监督信号，配合空间接地惩罚（spatial grounding penalty）来约束查询的有效性——这避免了昂贵的人工 CoT 标注，同时使模型能够自主探索有效的查询模式。其二，**如何在固定 token 预算下选择最具信息量的初始帧？** EagleVision 提出 SPF-DPP（Semantics-Perspective-Fusion Determinantal Point Process），联合优化语义相关性和 SE(3) 视点多样性，在几何感知的帧选择层面为后续的主动推理奠定基础。

这一双阶段设计——宏感知（macro perception）的几何感知帧选择与微验证（micro verification）的 BEV 锚定主动推理——构成了 EagleVision 应对空间推理挑战的完整方案。

## 核心方法与创新机理

EagleVision 的核心创新在于将视频空间推理重新形式化为一个**闭环的假设-观察-验证过程**，通过三个相互耦合的机制突破现有 MLLM 的局限：

**1. 主动视图获取：BEV 锚定的姿态查询**

现有方法使用统一采样帧在固定 token 预算下被动推理，无法主动获取几何信息丰富的额外视点。EagleVision 将空间推理形式化为 BEV-grounded 姿态查询——模型在推理过程中可以预测一个 BEV 平面上的姿态，系统检索与该姿态最匹配的真实帧返回给模型，形成"提出假设→观察新视图→验证/修正"的闭环。这一机制使模型能够根据当前信念动态请求最具信息量的视点，而非依赖初始采样的有限信息。

**2. 迭代空间多模态思维链 (Spatial MCoT)**

传统方法采用单次文本推理，缺乏将抽象空间假设与具体视频帧关联的能力。EagleVision 引入三种交替执行的推理动作：生成文本推理、查询 BEV 姿态获取新帧、或终止推理输出答案。状态空间包含文本 token、视觉观察和 BEV 姿态缓冲区，使模型能够在证据不足时主动请求缺失视角，迭代精炼空间判断。

**3. 纯强化学习训练策略，无需人工 CoT 标注**

现有空间推理方法依赖人工标注的推理轨迹进行监督微调。EagleVision 使用 GRPO（Group Relative Policy Optimization）纯强化学习训练查询策略，仅需答案级别的监督信号。奖励函数由任务奖励（准确性、格式、工具调用）和空间接地惩罚组成——当模型查询的位姿与任何真实相机轨迹帧的相似度低于阈值时，施加 -1 惩罚，防止模型查询无覆盖的无效区域。

**4. 几何-语义融合的帧选择 (SPF-DPP)**

在宏感知阶段，EagleVision 用 SPF-DPP（Semantics-Perspective-Fusion Determinantal Point Process）替代统一采样。该过程在 SE(3) 位姿图上通过热核扩散构建视点多样性核 $K_{\mathrm{view}}$，与 FG-CLIP 的语义质量矩阵 $Q$ 融合为 DPP L-ensemble 核 $\mathcal{L}_{\mathrm{dpp}} = Q K_{\mathrm{view}} Q$，在固定 token 预算下贪婪选择 $k$ 个关键帧，联合最大化语义相关性和视点多样性。消融实验表明，几何扩散和语义调制两个组件互补：单独几何达 63.2，单独语义达 63.0，组合后达 63.5。

**关键 changed slots 总结**

| 维度 | 基线方法 | EagleVision |
|------|---------|-------------|
| 帧选择策略 | 统一采样 | SPF-DPP 联合优化语义相关性与 SE(3) 视点多样性 |
| 视图获取机制 | 仅使用初始帧，无主动请求 | BEV 锚定姿态查询，推理中动态检索最匹配帧 |
| 推理过程 | 单次文本推理 | 迭代 Spatial MCoT，三类动作交替执行 |
| 训练信号 | 人工标注推理轨迹的 SFT | GRPO 强化学习，仅需答案级监督 + 空间接地惩罚 |

这些创新使 EagleVision 在 VSI-Bench 上以 63.5 分超越所有开源 VLM，比基座模型 Qwen3-VL-8B 提升 +4.1 分；在 SQA3D 上取得 60.3% EM@1，超越 Struct2D、Spatial-MLLM 和 Spatial-Mind 等专用空间推理方法。

EagleVision 将视频空间推理解耦为**宏观感知（Macro Perception）**与**微观验证（Micro Verification）**两个阶段，形成“假设—观察—验证”的闭环流水线。其核心设计动机在于：现有 MLLMs 在固定 token 预算下使用统一采样帧，既无法主动获取几何信息丰富的额外视点，也缺乏将抽象空间假设与具体视频帧关联的机制。EagleVision 通过离线重建的 BEV 地图实现主动姿态查询，使模型在推理过程中动态获取验证空间假设所需的特定视点。

### 流水线总览

**输入**：一段室内场景视频及一个空间推理问题（如“哪个物体离电视最近？”）。

**阶段一：宏观感知**。首先运行一个冻结的、现成的 SLAM 系统（默认使用 DROID-SLAM）进行一次性离线预处理，恢复每帧相机位姿与深度图，构建可复用的空间索引——BEV 地图与位姿数据库。随后，SPF-DPP（Semantics–Perspective-Fusion Determinantal Point Process）在固定 token 预算下联合优化语义相关性与 SE(3) 视点多样性，从视频中选取 *k* 个信息量最大的关键帧。语义相关性由 FG-CLIP 计算帧-关键词相似度并经温度校准得到；视点多样性则通过在 SE(3) 姿态图上构建稀疏亲和矩阵、经热核扩散生成正半定视点核 $K_{\mathrm{view}}$ 来度量。最终，DPP L-ensemble 核 $\mathcal{L}_{\mathrm{dpp}} = Q K_{\mathrm{view}} Q$ 通过贪婪 MAP 推理（带秩一 Cholesky 更新）选出 *k* 帧，保证 $(1-1/e)$ 近似最优。

**阶段二：微观验证**。选定的关键帧与渲染的 BEV 图像一同送入 VLM 进行迭代式空间思维链（Spatial MCoT）。每一步推理中，模型可执行三种动作之一：生成文本推理、在 BEV 平面上预测查询姿态以检索最近的真实帧、或终止并输出答案。BEV 查询机制将模型预测的 $(x, y, \text{yaw})$ 姿态与位姿数据库中存储的帧姿态进行高斯核相似度匹配，返回最接近的帧作为新的视觉观察。这一闭环使模型能够根据当前信念主动请求最具信息量的视点，逐步精炼空间判断。

**输出**：问题的最终答案。

### 训练机制

EagleVision 的查询策略完全通过强化学习训练，无需人工标注的思维链轨迹。采用 GRPO（Group Relative Policy Optimization），奖励函数由任务奖励与空间接地惩罚组成：

$$R(\tau) = \underbrace{R_{\mathrm{acc}}(\tau) + R_{\mathrm{format}}(\tau) + \lambda_{\mathrm{tool}} R_{\mathrm{tool}}(\tau)}_{\text{任务奖励}} + \underbrace{\lambda_{\mathrm{spatial}} R_{\mathrm{spatial}}(\tau)}_{\text{空间接地}}$$

其中，空间接地惩罚 $R_{\mathrm{spatial}}$ 对任何查询到相机覆盖范围外区域的步骤给予 -1 惩罚，防止模型请求无效视点。训练仅需答案级别的监督信号，无需 SFT 冷启动。

### 模块关系

三个核心模块呈递进互补关系：SPF-DPP 提供高质量的初始视觉证据；BEV 接地使模型能够在推理中主动获取缺失视点；Spatial MCoT 则将这些能力组织为迭代的假设-验证循环。消融实验证实了这一互补性：仅添加 Spatial MCoT 将基线从 59.4 提升至 61.9；引入 BEV 接地进一步提至 62.7（+3.3 over baseline）；叠加 SPF-DPP 达到最优 63.5（+0.8）。框架对位姿噪声具有鲁棒性：中等噪声（5% 平移，5° 旋转）下 VSI-Bench 分数仅下降 0.4%，更换 SLAM 后端为 VGGT 后性能为 63.2（-0.3），表明对特定 SLAM 系统的依赖较弱。

![[assets/figures/papers/paper_list_l2387_https_arxiv_org_abs_2512_15160/figures/002_Figure_2.jpg]]
*Figure 2: Framework of EagleVision. The framework operates in two stages: (i) Macro perception selects spatially informative keyframes under a token budget by jointly optimizing semantic relevance and viewpoint diversity. (ii) Micro verification performs iterative spatial CoT with active BEV-grounded pose querying to refine spatial understanding*

EagleVision 将视频空间推理分解为两个串行阶段：**宏感知（Macro Perception）** 与 **微验证（Micro Verification）**。前者在固定 token 预算下从视频中选取一组几何感知的关键帧；后者以迭代空间思维链（Spatial MCoT）的方式，在 BEV 地图上主动查询缺失视点，形成“假设—观察—验证”的闭环。

---

### 宏感知：SPF-DPP 关键帧选择

宏感知阶段的核心是 **语义-视角融合行列式点过程（SPF-DPP）**，它联合优化帧的语义相关性与 SE(3) 视点多样性，在固定数量 $k$ 下选出最具信息量的关键帧子集。其构建流程如下：

**步骤一：构建视点核 $K_{\text{view}}$。** 从 SLAM 重建中获取每帧的相机位姿 $(R_i, \mathbf{t}_i)$，定义帧间 SE(3) 距离：

$$d_{ij}^2 = \frac{\|\mathbf{t}_i - \mathbf{t}_j\|^2}{\sigma_t^2} + \beta^2 \theta(R_i, R_j)^2$$

其中旋转角距离为测地线距离：

$$\theta(R_i, R_j) = \arccos\left(\frac{\mathrm{tr}(R_i^{\top} R_j) - 1}{2}\right)$$

将距离通过 RBF 核 $w_{ij} = \exp(-d_{ij}^2)$ 转化为相似度，并限制时间带宽 $b$ 构建稀疏邻接矩阵：

$$W_{ij} = \begin{cases} w_{ij}, & \text{if } |i - j| \leq b \\ 0, & \text{otherwise} \end{cases}$$

在图拉普拉斯 $\mathcal{L} = I - D^{-1/2} W D^{-1/2}$ 上施加热核扩散，得到全局视点相似度核：

$$K_{\text{view}} = \exp(-\tau \mathcal{L})$$

该核为半正定（PSD），将局部姿态亲和传播为全局视点冗余度度量。

**步骤二：构建语义质量矩阵 $Q$。** 利用 FG-CLIP 计算每帧与问题关键词的相似度，经温度校准后编码为对角质量矩阵 $Q = \operatorname{diag}(q_1, \ldots, q_N)$，$q_i$ 越高表示该帧语义越相关。

**步骤三：DPP 子集选择。** DPP 的 L-ensemble 核定义为 $\mathcal{L}_{\text{dpp}} = Q K_{\text{view}} Q$，因其为两个 PSD 矩阵的合同变换，仍保持 PSD。在固定预算 $k$ 下，通过贪婪 MAP 推理最大化子矩阵行列式对数：

$$\max_{X \subseteq [N], |X| = k} \log \det(L_{\text{dpp}, X})$$

该目标天然平衡质量与多样性：$Q$ 鼓励选择语义相关的帧，$K_{\text{view}}$ 惩罚视点冗余的帧。贪婪算法配合秩一 Cholesky 更新，可保证 $(1-1/e)$ 近似比。

---

### 微验证：BEV-Grounded 空间思维链

微验证阶段将空间推理形式化为 **迭代多模态思维链**，模型在每个推理步可执行三种动作之一：**生成文本**、**查询 BEV 姿态**或**终止并输出答案**。状态由文本 token、视觉观测和 BEV 姿态缓冲区共同构成。

**BEV 姿态查询机制：** 当模型判断当前证据不足以支撑空间判断时，会在 BEV 平面上预测一个查询姿态 $(\hat{x}_t, \hat{y}_t, \hat{r}_t)$（2D 位置 + 偏航角）。系统计算该查询与所有候选帧存储姿态的高斯核相似度：

$$s_{tj} = \exp\left[-\frac{1}{2}\left(\frac{\|(\hat{x}_t,\hat{y}_t) - (x_j,y_j)\|^2}{\sigma_p^2} + \beta^2 (\hat{r}_t - r_j)^2\right)\right]$$

检索相似度最高的帧作为新观测返回给模型，形成“假设—观察—验证”闭环。

**BEV 地图构建：** 离线 SLAM 阶段通过像素反投影将深度图转换为全局点云：

$$\mathbf{X}_t(\mathbf{u}) = R_t^{-1} ( D_t(\mathbf{u}) K^{-1} \tilde{\mathbf{u}} - \mathbf{t}_t )$$

其中 $\mathbf{u}$ 为像素坐标，$D_t(\mathbf{u})$ 为深度，$K$ 为相机内参。地面平面估计通过统计点云在候选垂直轴上的低/高 5% 分位数跨度确定接地侧：

$$d_{\text{bottom}} = z^{(5)} - z^{(0)}, \quad d_{\text{top}} = z^{(100)} - z^{(95)}$$

选择跨度较小的一侧作为地面，将点云投影至该平面生成 BEV 图像。

---

### 训练：GRPO 与空间接地奖励

查询策略通过 **Group Relative Policy Optimization（GRPO）** 纯强化学习训练，无需人工 CoT 标注。轨迹总奖励由四部分组成：

$$R(\tau) = R_{\text{acc}}(\tau) + R_{\text{format}}(\tau) + \lambda_{\text{tool}} R_{\text{tool}}(\tau) + \lambda_{\text{spatial}} R_{\text{spatial}}(\tau)$$

其中任务奖励包括答案正确性 $R_{\text{acc}}$、格式合规 $R_{\text{format}}$ 和工具调用激励 $R_{\text{tool}}$。特有的**空间接地惩罚** $R_{\text{spatial}}$ 防止模型查询相机轨迹外的无效区域：

$$R_{\text{spatial}}(\tau) = \begin{cases} -1, & \text{if } \exists t \in \mathcal{C}(\tau) \text{ s.t. } s_{\max}^{(t)} < \tau_s \\ 0, & \text{otherwise} \end{cases}$$

若任一次查询的最大帧相似度 $s_{\max}^{(t)}$ 低于覆盖阈值 $\tau_s$，则给予 $-1$ 惩罚。惩罚幅度由 $\lambda_{\text{spatial}}$ 统一控制，单次惩罚固定为 $-1$ 以简化设计。消融实验表明，工具奖励是性能提升的主要驱动力（+1.9），空间惩罚进一步贡献 +0.5。

---

### 关键公式汇总

| 公式 | 变量含义 |
|------|----------|
| $d_{ij}^2 = \frac{\|\mathbf{t}_i - \mathbf{t}_j\|^2}{\sigma_t^2} + \beta^2 \theta(R_i, R_j)^2$ | $\sigma_t$：平移尺度因子；$\beta$：旋转权重；$\theta$：旋转测地线角 |
| $K_{\text{view}} = \exp(-\tau \mathcal{L})$ | $\tau$：扩散时间参数；$\mathcal{L}$：归一化图拉普拉斯 |
| $\mathcal{L}_{\text{dpp}} = Q K_{\text{view}} Q$ | $Q$：语义质量对角阵；$K_{\text{view}}$：视点相似度核 |
| $s_{tj} = \exp[-\frac{1}{2}(\frac{\|(\hat{x}_t,\hat{y}_t)-(x_j,y_j)\|^2}{\sigma_p^2} + \beta^2(\hat{r}_t - r_j)^2)]$ | $\sigma_p$：位置尺度；$(\hat{x}_t,\hat{y}_t,\hat{r}_t)$：查询姿态；$(x_j,y_j,r_j)$：候选帧姿态 |
| $R_{\text{spatial}}(\tau) = -1 \text{ if } s_{\max}^{(t)} < \tau_s \text{ else } 0$ | $\tau_s$：覆盖阈值；$s_{\max}^{(t)}$：第 $t$ 步最大帧相似度 |

## 实验与关键发现

### 主实验结果

EagleVision 在两个空间推理基准 VSI-Bench 和 SQA3D 上均取得开源模型最优。在 VSI-Bench 上，EagleVision 以 63.5 的平均分位列所有开源 VLM 之首，较基座模型 **Qwen3-VL-8B**（An Yang et al., arXiv 2025）的 59.4 提升 +4.1 分，较此前最强的专用空间推理方法 **VLM-3R-7B**（Duo Zheng et al., arXiv 2024）的 60.9 提升 +2.6 分。在 SQA3D 上，EagleVision 取得 60.3% EM@1，分别超出 **Struct2D**（Fangrui Zhu et al., arXiv 2025）1.8%、**Spatial-MLLM**（Diankun Wu et al., arXiv 2025）4.4% 和 **Spatial-Mind**（Haoyu Zhang et al., arXiv 2025）14.0%。与 **LLaVA-OneVision-7B**（Bo Li et al., arXiv 2024）、**InternVL2-8B**（Zhe Chen et al., arXiv 2024）等通用 VLM 以及闭源模型 **Gemini-1.5 Flash**、**GPT-4o** 相比，EagleVision 同样保持显著优势。所有模型使用相同的视频输入与问题模板，训练数据来自 VLM-3R 和 SQA3D 训练集，与测试集无重叠，比较公平。

### 整体架构消融

为验证双阶段框架各组件的独立贡献，作者以 Qwen3-VL-8B 为基线（VSI-Bench 59.4）进行逐步消融：仅添加 Spatial MCoT 将性能提升至 61.9（+2.5），表明迭代式多模态推理本身已带来显著增益；在此基础上引入 BEV grounding 进一步将分数推至 62.7（较基线 +3.3），证明主动视点查询能有效补充初始帧缺失的空间证据；叠加 SPF-DPP 后达到最优 63.5（+0.8），说明几何感知的关键帧选择改善了推理起点的证据质量。三个组件相互补充，最终从 59.4 累积提升至 63.5。

### SPF-DPP 组件消融

在 MCoT+BEV 基线（62.7）上对 SPF-DPP 的几何扩散和语义调制进行拆解：仅使用几何视点扩散核选帧达到 63.2（+0.5），仅使用语义质量矩阵选帧达到 63.0（+0.3），两者联合达到 63.5（+0.8）。几何与语义两个维度的信息互补，联合优化比任一单独维度带来更大增益。

SPF-DPP 对超参数不敏感：旋转权重 β、时间带宽 b 等参数在合理范围内变动时，性能波动在 0.5 分以内，且所有配置下均优于朴素的时间均匀采样。所有实验使用统一的固定超参数（见附录 Table A1），未针对单个基准调优。

![[assets/figures/papers/paper_list_l2387_https_arxiv_org_abs_2512_15160/figures/017_Table.jpg]]
*Table: A1. Hyper-parameters used in SPF-DPP. All values are fixed across experiments*

### GRPO 奖励项消融

RL 训练中使用的组合奖励包含四项：准确性奖励（R_acc）、格式奖励（R_format）、工具调用奖励（R_tool）和空间接地惩罚（R_spatial）。消融显示，仅使用 Accuracy + Format 奖励时得分为 61.1；添加 Tool 奖励后跃升至 63.0（+1.9），是性能提升的主要驱动力；进一步添加 Spatial 惩罚项达到 63.5（+0.5），通过抑制对相机轨迹外无效区域的查询，进一步规范了推理行为。空间接地惩罚的设计为：若任一次 BEV 查询的最大帧-查询相似度低于覆盖阈值 τ_s，则给予 -1 惩罚，惩罚强度由 λ_spatial 单独控制。

### 鲁棒性分析

EagleVision 对位姿噪声表现出强鲁棒性：在中等噪声水平（平移 5%、旋转 5°）下，VSI-Bench 分数仅下降 0.4%。将 SLAM 后端替换为 VGGT 后性能为 63.2（-0.3），表明框架对具体 SLAM 系统的依赖较弱，离线重建模块的精度波动不会显著影响下游推理质量。

### 关键图表结论

- **Table 1**：EagleVision 在 VSI-Bench（63.5）和 SQA3D（60.3）上均位列开源模型第一，全面超越通用 VLM 和专用空间推理方法。
- **Table 2**：MCoT、BEV grounding、SPF-DPP 三者逐步叠加，性能从 59.4 → 61.9 → 62.7 → 63.5，每个组件均带来不可替代的增益。
- **Table 3**：SPF-DPP 的几何扩散与语义调制互补，联合使用达到最优 63.5。
- **Table 4**：Tool 奖励是 GRPO 训练的主要驱动力（+1.9），空间惩罚提供额外 +0.5 的精细化提升。
- **Table 5**：SPF-DPP 超参数在宽范围内鲁棒，所有配置均优于朴素时间采样。
- **Table 6**：位姿噪声和 SLAM 后端替换对性能影响极小（≤0.4%），框架鲁棒性强。

![[assets/figures/papers/paper_list_l2387_https_arxiv_org_abs_2512_15160/figures/005_Table_1.jpg]]
*Table 1: Evaluations on SQA-3D (Val) and VSI-Bench. EagleVision ranks first among open-source VLMs, showcasing the effectiveness of our dual-stage framework. †Results on the VSI-Bench tiny set are presented following the setup in [39]*

![[assets/figures/papers/paper_list_l2387_https_arxiv_org_abs_2512_15160/figures/008_Table_2.jpg]]
*Table 2: Ablation study of overall architecture. MCoT means Spatial MCoT; BEV means BEV image input; SPF-DPP means geometry-aware frame selection*

![[assets/figures/papers/paper_list_l2387_https_arxiv_org_abs_2512_15160/figures/006_Table_3.jpg]]
*Table 3: Ablation study of SPF-DPP components on the MCoT+BEV baseline*

![[assets/figures/papers/paper_list_l2387_https_arxiv_org_abs_2512_15160/figures/009_Table_4.jpg]]
*Table 4: Ablation study of GRPO reward terms. Acc. means accuracy reward*

## 定位与知识库关联

### 核心方法定位

EagleVision 处于视频空间推理（Video Spatial Reasoning）与多模态大语言模型（MLLM）主动感知的交汇点。其核心创新在于将传统 MLLM 的**被动单次推理**范式改造为**双阶段主动闭环**：宏感知（Macro Perception）通过几何-语义联合优化的关键帧选择压缩视频冗余，微验证（Micro Verification）通过 BEV 锚定的姿态查询实现假设-观察-验证的迭代推理。这一设计直接回应了现有 MLLM 在固定 token 预算下无法主动获取几何信息丰富的额外视点、且缺乏将抽象空间假设与具体视频帧关联机制的根本瓶颈。

### 基线方法谱系

论文将基线工作划分为三个层次，分别对应不同的技术路线：

**1. 通用开源 VLM 基线**

这些模型未针对空间推理进行专项设计，仅依赖统一采样帧和单次文本推理。EagleVision 的基础模型 **Qwen3-VL-8B**（An Yang et al., arXiv 2025）在 VSI-Bench 上取得 59.4 分，是 EagleVision 的直接微调起点。其他通用 VLM 包括 **LLaVA-OneVision-7B**（Bo Li et al., arXiv 2024）和 **InternVL2-8B**（Zhe Chen et al., arXiv 2024），以及闭源模型 **GPT-4o**（Hurst et al., arXiv 2024）和 **Gemini-1.5 Flash**（Gemini Team et al., arXiv 2024）。这些模型的共同局限在于：缺乏对视频几何结构的显式建模，且无法在推理过程中动态请求缺失视点的信息。

**2. 任务专用空间推理方法**

- **VLM-3R-7B**（Duo Zheng et al., arXiv 2024）：通过 3D 重建编码器将视频帧转化为显式三维表示，在 VSI-Bench 上取得 60.9 分，是此前开源方法中的最优。EagleVision 以 63.5 分超越其 +2.6 分，且不依赖专用的 3D 编码器模块。

- **Struct2D**（Fangrui Zhu et al., arXiv 2025）：利用结构化 2D 投影进行空间推理，在 SQA3D 上取得 58.5% EM@1。EagleVision 以 60.3% 领先 +1.8 个百分点。

- **Spatial-MLLM**（Diankun Wu et al., arXiv 2025）：融合 VGGT 空间编码器，在 SQA3D 上取得 55.9% EM@1。EagleVision 领先 +4.4 个百分点。

- **Spatial-Mind**（Haoyu Zhang et al., arXiv 2025）：使用结构化提示和仿真数据进行空间推理，在 SQA3D 上取得 46.3% EM@1。EagleVision 领先 +14.0 个百分点。

这些方法的共同特征是将空间信息编码为模型输入的附加模态（3D 特征、2D 投影、仿真数据），但推理过程仍为单次前向传播，无法形成闭环验证。

**3. EagleVision 的差异化路径**

EagleVision 与上述方法的关键差异体现在四个维度：

| 维度 | 基线方法 | EagleVision |
|------|----------|-------------|
| 帧选择策略 | 统一采样（Uniform sampling） | SPF-DPP：联合最大化语义相关性与 SE(3) 视点多样性 |
| 视图获取机制 | 无主动请求；仅使用初始帧 | BEV-grounded 姿态查询：在推理中动态检索最匹配的真实帧 |
| 推理过程 | 单次文本推理 | 迭代 Spatial MCoT：三步动作（文本输出/姿态查询/终止），状态包含文本 token、视觉观察和 BEV 姿态缓冲 |
| 训练信号 | 监督微调 + 人工标注推理轨迹 | GRPO 强化学习 + 空间接地奖励；仅需答案级监督，无需人工 CoT 标注 |

### 技术继承与创新溯源

**SPF-DPP 的谱系**：DPP（Determinantal Point Process）在视频摘要和关键帧选择中已有应用，但 EagleVision 的 SPF-DPP 将语义质量矩阵 $Q$（通过 FG-CLIP 计算帧-关键词相似度并经温度校准）与视点扩散核 $K_{\mathrm{view}}$（通过 SE(3) 姿态图的 heat-kernel diffusion 生成）在 DPP L-ensemble $\mathcal{L}_{\mathrm{dpp}} = Q K_{\mathrm{view}} Q$ 中融合，实现了几何感知与语义感知的联合优化。消融实验（Table 3）表明，单独几何扩散达到 63.2 分，单独语义调制达到 63.0 分，两者组合达到 63.5 分，验证了互补性。

**BEV-grounded 查询的谱系**：BEV（Bird's-Eye-View）表示在自动驾驶和具身智能中广泛使用，但 EagleVision 首次将其引入 MLLM 的空间推理闭环：模型在 BEV 平面上预测查询姿态 $(\hat{x}_t, \hat{y}_t, \hat{r}_t)$，通过高斯核相似度 $s_{tj}$ 检索最近的真实帧，形成假设-观察-验证循环。这一机制将抽象的空间推理锚定在可操作的几何查询上。

**GRPO 训练的谱系**：Group Relative Policy Optimization（GRPO）是近期在 LLM 推理训练中兴起的方法。EagleVision 的贡献在于设计了适配空间推理的奖励组合：

$$R(\tau) = \underbrace{R_{\mathrm{acc}}(\tau) + R_{\mathrm{format}}(\tau) + \lambda_{\mathrm{tool}} R_{\mathrm{tool}}(\tau)}_{\mathrm{task\ rewards}} + \underbrace{\lambda_{\mathrm{spatial}} R_{\mathrm{spatial}}(\tau)}_{\mathrm{spatial\ grounding}}$$

其中空间接地惩罚 $R_{\mathrm{spatial}}$ 在查询的最大帧相似度低于覆盖阈值 $\tau_s$ 时给予 -1 惩罚，防止模型查询相机轨迹外的无效区域。消融实验（Table 4）显示，工具奖励是主要驱动力（Accuracy+Format 为 61.1，加入 Tool 后升至 63.0，+1.9），空间惩罚进一步提至 63.5（+0.5）。

### 适用边界与局限

**场景依赖性**：框架依赖离线 SLAM 重建步骤构建 BEV 地图和姿态数据库。实验表明框架对 SLAM 质量具有鲁棒性——中等位姿噪声（5% 平移误差, 5° 旋转误差）下 VSI-Bench 分数仅下降 0.4%，更换 SLAM 后端为 VGGT 后性能为 63.2（-0.3）。然而，这一结论基于室内场景（ScanNet、SQA3D 训练数据），在室外或高度动态场景下的鲁棒性尚未验证。

**动态场景适用性**：当前训练数据偏向静态室内环境。对于包含大量运动物体或快速相机运动的视频，SLAM 重建质量和 BEV 查询的有效性可能下降。这一问题在论文中未被系统评估，需要进一步验证。

**Token 预算固定**：SPF-DPP 的关键帧数量 $k$ 固定为 32。消融实验中未探索自适应调整 $k$ 的策略，这可能在高信息密度场景下限制性能，或在低信息密度场景下浪费计算资源。

**RL 训练的超参数敏感性**：空间接地惩罚的权重 $\lambda_{\mathrm{spatial}}$ 需要手动设置。虽然 SPF-DPP 的超参数（旋转权重 $\beta$、时间带宽 $b$ 等）在 Table 5 中表现出较好鲁棒性（性能波动在 0.5 点以内），但 RL 奖励权重的自适应调节机制尚未探索。

### 开放问题

1. **动态场景扩展**：EagleVision 的 BEV-grounded 查询策略是否适用于包含大量运动物体的视频？可能需要引入运动分割或动态物体追踪机制。

2. **域外泛化**：当前训练数据偏向室内场景（ScanNet、SQA3D），在室外自动驾驶或开放环境下的扩展性如何？需要新的基准和训练数据进行验证。

3. **自适应 Token 预算**：SPF-DPP 的 $k$ 固定为 32，自适应调整 $k$ 是否能进一步平衡效率与性能？可探索基于问题复杂度或场景信息密度的动态预算分配。

4. **RL 奖励权重的自动调节**：$\lambda_{\mathrm{spatial}}$ 需要手动设置，是否可以通过元学习或自适应方式自动调节？这可以降低对人工调参的依赖。

5. **在线 SLAM 与推理的紧耦合**：离线 SLAM 预处理步骤是否可能成为实时应用的瓶颈？能否将重建与推理过程进行在线联合优化，减少预处理延迟？

6. **SLAM 失败的鲁棒恢复**：如果初始 SLAM 重建严重不准确（而非仅含噪声），BEV 查询是否仍能有效工作？可能需要更鲁棒的错误恢复机制或不确定性感知的查询策略。

7. **多模态空间推理的扩展**：当前框架主要处理视觉空间推理，是否可以扩展至音频空间定位（如声源方向判断）或触觉空间感知等多模态场景？

## 原文 PDF

![[paperPDFs/CVPR_2026/EagleVision_A_Dual_Stage_Framework_with_BEV_grounding_based_Chain_of_Thought_for_Spatial_Intelligence.pdf]]
