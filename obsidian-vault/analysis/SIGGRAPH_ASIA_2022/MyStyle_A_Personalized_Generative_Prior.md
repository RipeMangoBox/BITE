---
title: "MyStyle: A Personalized Generative Prior"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/MyStyle_A_Personalized_Generative_Prior.pdf
project_link: null
code_link: "https://github.com/google/mystyle"
aliases:
- MyStyle
tags:
- SIGGRAPH_ASIA_2022
- topic/generative_models_diffusion
core_operator: 通过在StyleGAN潜在空间中构建由锚点定义的膨胀凸包，形成个性化低维流形，并通过调节扩张参数β平衡身份保持与表现力。
primary_logic: 利用预训练StyleGAN的平滑与解耦特性，对特定个体进行少量样本的生成器微调，使其局部区域形成忠实于该个体的生成空间；通过限制投影到该空间的膨胀凸包内，可在各种图像增强和编辑任务中实现高身份保持。
claims:
- 在锚点插值和邻域随机游走中，微调后生成图像的身份保持得分显著提升。
- 扩张参数β控制身份保持与重建精度之间的权衡。
- 在修复和超分辨率任务上，MyStyle的身份保持指标与用户偏好均优于基线方法。
- 仅6.7%的插值结果身份得分低于两个端点，且最大下降仅为0.1，表明个性化空间具有很强的身份保真性。
---

# MyStyle: A Personalized Generative Prior

> [!tip] 核心洞察
> 利用预训练StyleGAN的平滑与解耦特性，对特定个体进行少量样本的生成器微调，使其局部区域形成忠实于该个体的生成空间；通过限制投影到该空间的膨胀凸包内，可在各种图像增强和编辑任务中实现高身份保持。

| 字段 | 内容 |
|------|------|
| 中文题名 | MyStyle：个性化生成先验 |
| 英文题名 | MyStyle: A Personalized Generative Prior |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://mystyle-personalized-prior.github.io/) · [Code](https://github.com/google/mystyle) |
| Topic | #topic/generative_models_diffusion |
| Method | MyStyle |
| Dataset |  |

> [!tip] 效果简介
> - 图像生成 (Synthesis) 上，ID (↑) 0.79 ± 0.04 vs 优于Ojha et al. 和 DiffAugment（数值未提供） (领先)；User % (↑) (真实度) 68.9 vs 远高于Ojha et al. 和 DiffAugment (显著提升)。
> - 图像修复 (Inpainting) 上，ID (↑) 0.72 ± 0.08 vs CoModGAN (Domain Prior) (优于所有基线)。
> - 超分辨率 (Super-Resolution) 上，ID (↑) 0.81 ± 0.04 vs GPEN (Domain Prior) (优于所有基线)。

## 概要

**问题**：通用人脸生成先验（如在FFHQ上预训练的StyleGAN）在图像修复、超分辨率或语义编辑时，会丢失个人的独特面部特征，无法保持身份一致性。

**方法**：MyStyle利用少量（约100张）个人肖像，对预训练StyleGAN生成器进行微调，形成局部、低维的个性化流形。具体而言，先将参考图像反演至W空间的固定锚点，再以锚点定义的膨胀凸包（由参数β控制扩张程度）作为个性化子空间；所有增强与编辑任务均通过在该子空间内投影优化完成。

**主要结果**：在图像生成、修复、超分辨率和姿态编辑等任务上，MyStyle的身份保持得分（ID）均显著优于通用先验及少样本域适应基线。例如，超分辨率任务上ID达到0.81±0.04，比GPEN的0.56±0.07提升约0.25。用户研究也表明MyStyle生成结果更真实。仅6.7%的锚点插值结果身份得分低于端点，证实个性化空间具有高身份保真性。

**方法定位**：MyStyle将通用域先验替换为个性化域先验，并通过膨胀凸包约束潜在空间，属于少样本个性化生成与图像增强的交叉改进。

## 核心方法与创新机理

### 问题瓶颈与核心思想

通用人脸生成先验（如在FFHQ上预训练的StyleGAN）在图像修复、超分辨率、语义编辑等任务中表现优异，但存在一个根本性缺陷：当处理特定个体的图像时，生成结果会丢失该人物的关键面部特征，导致身份一致性崩塌。这是因为通用先验学习的是跨人群的平均面部分布，无法表征个体独有的、细微的身份特征。

MyStyle的核心洞察在于：预训练StyleGAN的潜在空间具有平滑性和解耦性，通过对特定个体的少量参考图像（约100张）进行**局部生成器微调**，可以在潜在空间中形成一个低维的、忠实于该个体的个性化流形。关键创新在于，该流形并非通过重新训练获得，而是通过**在锚点定义的扩张凸包内约束潜在编码**来实现身份保持与表现力之间的精细平衡。

### 方法模块与因果链路

MyStyle由四个核心模块串联构成，形成从个性化先验构建到下游任务应用的完整链路：

#### 模块一：图像反演与锚点生成

给定某个体的一组参考肖像图像 $\{x_i\}_{i=1}^N$，首先使用预训练的图像反演编码器将每张图像投影到通用域生成器 $G_d$ 的 $\mathcal{W}$ 空间，得到一组固定潜在编码 $\{w_i\}_{i=1}^N$，称为**锚点（anchors）**。这些锚点是参考图像在通用流形上的最近邻投影，构成了个性化空间的基础骨架。

#### 模块二：生成器局部微调

以锚点-图像对 $\{(w_i, x_i)\}$ 为监督信号，对预训练生成器 $G_d$ 的权重进行微调，得到个性化生成器 $G_p$。微调的损失函数结合了感知损失和像素级重建损失：

$$\mathcal{L}_{rec}(G, x_i, w_i) = \mathbb{E}_i \left[ \mathcal{L}_{lpips}(G(w_i), x_i) + \lambda_{L_2} \|G(w_i) - x_i\|_2 \right]$$

该损失确保每个锚点 $w_i$ 经过 $G_p$ 后能精确重建对应的参考图像 $x_i$。微调的关键特性在于其**局部性**：仅改变生成器在锚点邻域的行为，而不影响远离锚点的区域。这保证了 $G_p$ 在锚点附近形成高度个性化的生成空间，同时保留通用域先验的其他属性（如姿态、表情的连续性）。Fig. 4 的实验证实，微调后锚点插值和邻域随机游走生成图像的身份保持得分显著提升，且仅有6.7%的插值结果身份得分低于两端点，最大下降仅为0.1，表明个性化空间具有强身份保真性。

#### 模块三：扩张凸包个性化子空间建模

微调后的 $\mathcal{W}_p$ 空间中，锚点张成了一个低维子空间。MyStyle通过**扩张凸包（Dilated Convex Hull）** 对该子空间进行参数化建模。在广义重心坐标下，定义系数空间：

$$\mathcal{R}_{\beta} = \{ \pmb{\alpha} \in \mathbb{R}^N \mid \sum_i \alpha_i = 1, \forall i: \alpha_i \geq -\beta \}$$

对应潜在空间中的个性化先验为：

$$\mathcal{P}_{\beta} = \{ \sum_i \alpha_i w_i \mid \sum_i \alpha_i = 1, \forall i: \alpha_i \geq -\beta \}$$

其中 $\beta \geq 0$ 为扩张参数。当 $\beta=0$ 时，$\mathcal{P}_0$ 为标准凸包，仅能表达锚点的凸组合；增大 $\beta$ 允许系数取负值，使子空间向外扩张，增强表现力但削弱身份约束。该设计的因果机制在于：**$\beta$ 直接控制先验强度与表现力之间的权衡**——小的 $\beta$ 强制生成结果靠近锚点张成的身份核心区域，保证高身份保持但限制编辑自由度；大的 $\beta$ 允许偏离锚点，提升重建精度和编辑灵活性，但有身份漂移风险。

#### 模块四：基于投影的图像增强与编辑

下游任务通过将退化图像投影到个性化子空间来实现。以图像修复为例，给定退化图像 $I_d$ 和掩码 $M$，在 $\alpha$ 空间中优化潜在编码以最小化重建损失：

$$\pmb{\alpha}^* = \arg\min_{\pmb{\alpha}} \mathcal{L}_{rec}(\phi \circ G, I_d, M \pmb{\alpha}_{\beta})$$

其中 $\pmb{\alpha}_{\beta}$ 通过Shifted Softplus函数保证下界约束：

$$\pmb{\alpha}_{\beta} = \frac{1}{s} \log(1 + e^{s(\pmb{\alpha} + \beta)}) - \beta$$

为进一步提升表现力，引入**层偏移 $\Delta$** 将优化空间从 $\alpha$ 空间扩展到 $\alpha^+$ 空间，最终优化目标为：

$$\mathcal{L}_{final} = \mathcal{L}_{rec}(\phi \circ G, I_d, M\alpha_{\beta}^+) + \lambda_{reg}\mathcal{L}_{reg}(\Delta) + \mathcal{L}_{sum}(\alpha_{\beta}^+)$$

其中 $\mathcal{L}_{sum}(\pmb{\alpha}_{\beta}) = (\sum_i \alpha_i - 1)^2$ 鼓励系数之和接近1，$\mathcal{L}_{reg}(\Delta)$ 约束层偏移的幅度。该投影机制的核心在于：优化过程被限制在 $\mathcal{P}_{\beta}$ 内，确保生成结果始终处于个性化流形上，从而实现身份保持。

对于语义编辑，MyStyle采用两阶段方法：首先将通用编辑方向 $\mathbf{n}$ 投影到锚点张成的子空间 $V$ 上，得到个性化编辑方向 $\hat{\mathbf{n}}$；然后通过计算编辑后编码所需的最小扩张参数 $\beta_{edit} = |\min(\{\alpha_i^{edit}\} \cup \{0\})|$ 来验证编辑结果是否仍在 $\mathcal{P}_{\beta}$ 内，必要时可投影回子空间以维持身份一致性。

### 关键创新槽位对比

| 槽位 | 基线方法 | MyStyle | 因果作用 |
|------|---------|---------|---------|
| 生成器先验类型 | 通用域先验（FFHQ预训练StyleGAN） | 个性化域先验（少量个人照片微调） | 根本性解决身份丢失问题 |
| 潜在空间约束 | $\mathcal{W}$ 或 $\mathcal{W}^+$ 空间，无显式约束 | 扩张凸包 $\mathcal{P}_{\beta}$，通过 $\beta$ 控制先验强度 | 提供可调节的身份-表现力权衡机制 |
| 增强优化目标 | $\mathcal{W}^+$ 空间最小化重建损失 | $\alpha^+$ 空间中含正则项的重建损失，包括层偏移正则和和约束 | 在保持身份的同时提升重建精度和编辑灵活性 |

### 训练与推理路径

**训练阶段**：仅需一次生成器微调。给定约100张个人参考图像，通过反演编码器获得锚点，然后以锚点为输入、原图为目标优化 $G_p$ 的权重。消融实验证实，联合优化锚点与生成器（如GLO方法）会导致生成结果模糊失真，因此MyStyle采用固定预计算锚点的策略。

**推理阶段**：对于图像增强任务，在 $\alpha^+$ 空间中迭代优化潜在编码和层偏移，使其重建退化图像的同时受 $\mathcal{P}_{\beta}$ 约束。对于语义编辑，先投影编辑方向再验证子空间归属。整个过程无需重新训练，仅需调整 $\beta$ 即可适配不同任务的身份保持需求。

![[assets/figures/papers/paper_list_l68_https_mystyle_personalized_prior_github_io/figures/002_Figure_2.jpg]]
*Figure 2: An illustration of our tuning method. We project a set of ?? portrait images of an individual into StyleGAN’s W space, resulting in a set of anchors that are the nearest possible neighbors. We then tune the generator reconstruct the input images from their corresponding anchors*

![[assets/figures/papers/paper_list_l68_https_mystyle_personalized_prior_github_io/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of our enhancement method for Inpainting. We optimize a latent code in ??-space to find the latent code in*

![[assets/figures/papers/paper_list_l68_https_mystyle_personalized_prior_github_io/figures/006_Figure_6.jpg]]
*Figure 6: The effect of reference set size and diversity on the prior’s expressiveness. We sample subsets of different sizes from the reference set of Joe Biden. For each subset we additionally tune a model*

## 实验与关键发现

### 核心实验设置

实验围绕约100张个人肖像的参考集展开，为每位人物训练个性化先验。身份保持（ID）通过预训练人脸识别网络的深度特征余弦相似度衡量，用户研究则邀请熟悉目标人物的参与者进行真实度与身份保持的二元选择判断。数据集按人物划分训练/测试集（Table 1），测试图像不出现在参考集中，确保评估的泛化性。

### 主结果：身份保持的系统性优势

**图像生成（Synthesis）** 任务上，MyStyle 与少样本域适应方法 **Ojha et al. (2021)** 和数据增强方法 **DiffAugment (Zhao et al., 2020)** 进行对比。MyStyle 的 ID 得分达到 **0.79 ± 0.04**，显著领先于两种基线；用户研究中，MyStyle 生成图像被判定为真实的占比达 **68.9%**，远超基线方法（Fig. 8）。这表明个性化子空间不仅能生成高保真身份的结果，其输出在感知真实度上也具有压倒性优势。

**图像修复（Inpainting）** 对比 **CoModGAN (Zhao et al., 2021)** 作为通用域先验基线，MyStyle 的 ID 得分为 **0.72 ± 0.08**，在身份保持维度上全面超越所有基线（Fig. 9）。值得注意的是，在通用域先验基础上进行个性化微调（Domain Prior + FT）虽能部分提升身份保持，但仍不及 MyStyle，说明仅微调生成器而不约束潜在空间不足以形成稳定的个性化流形。

**超分辨率（Super-Resolution）** 对比 **GPEN (Yang et al., 2021a)**，MyStyle 取得 **0.81 ± 0.04** 的 ID 得分，同样优于所有基线（Fig. 9）。在更具挑战性的 **Held-out 测试集**上，MyStyle 的 ID 得分为 **0.75 ± 0.03**，而 GPEN 仅 **0.56 ± 0.07**，GPEN+FT 为 **0.67 ± 0.07**，DiffAugment 为 **0.67 ± 0.05**（Fig. 21b）。MyStyle 相较最强基线的提升幅度达 **+0.08 至 +0.19**，证明个性化先验在分布外图像上仍能稳健保持身份特征。

**姿态编辑（Pose Editing）** 中，MyStyle 的 ID 得分为 **0.66 ± 0.05**，优于使用 FFHQ-StyleGAN 和 DiffAugment 的基线方法；用户偏好判断中，MyStyle 编辑结果在身份保持维度上以显著比例胜出（Fig. 10）。

### 关键消融实验

**扩张参数 β 的调控作用** 是最核心的机制验证。实验通过在 $P_\beta^+$ 空间中反演测试图像并变化 β 值，同时测量 ID 误差和 LPIPS 重建误差（Fig. 5, Fig. 18）。结果表明 β 增大时 ID 误差单调上升，而重建误差单调下降，形成清晰的权衡曲线。这直接证实了 β 作为“先验强度-表现力”控制旋钮的有效性：较小的 β 将潜在编码严格约束在锚点凸包内，牺牲重建精度以换取高身份保持；较大的 β 则放松约束，允许更精确的重建但身份特征可能漂移。

**参考集规模与多样性的影响**（Fig. 6）显示，初期增加参考图像数量能快速提升先验的表达能力，但达到一定规模后，多样性成为主导因素——即使数量相同，覆盖更多姿态、光照和表情的参考集会带来更好的生成质量。这为实际应用中参考集的采集策略提供了指导。

**投影空间的选择** 消融（Fig. 19）对比了三种投影策略：在 $W_p$ 空间、α 空间和 $\alpha^+$ 空间中优化。结果显示 $\alpha^+$ 空间（即允许每层独立偏移的扩展 α 空间）在身份保持和表现力上均优于前两者，验证了层偏移正则项 $\mathcal{L}_{reg}(\Delta)$ 的设计有效性。

**锚点优化策略** 的消融（Fig. 22）对比了联合优化锚点与生成器（GLO 方式，Bojanowski et al., 2017）与使用预计算固定锚点的方案。GLO 方式导致生成结果模糊、失真，说明将锚点固定为反演编码器的输出是维持个性化空间稳定性的关键——联合优化会破坏锚点在潜在空间中的结构关系，使得凸包定义的子空间失去语义一致性。

**生成结果的原创性验证**（Fig. 20）通过最近邻检索表明，MyStyle 生成的图像并非参考集的简单复制：生成图像与其最近参考图像之间存在显著差异，证实个性化流形确实产生了参考集之外的合理变化，而非记忆训练样本。

### 个性化空间的保真度分析

对锚点插值和邻域随机游走的定量分析（Fig. 4, Fig. 15）提供了个性化空间身份保真性的直接证据。在生成器微调后，锚点间的插值路径和锚点邻域内的随机采样点，其 ID 得分均显著高于微调前的通用生成器。特别地，仅 **6.7%** 的插值结果 ID 得分低于两个端点，且最大下降幅度仅为 **0.1**（Fig. 15），表明个性化流形具有全局性的身份保持特性——不仅锚点本身，其张成的整个子空间都忠实于目标人物。

### 适用边界

MyStyle 的效果依赖于预训练 StyleGAN 在 FFHQ 上习得的通用人脸先验，因此对于与 FFHQ 分布差异过大的人群（如极端年龄、特殊面部特征）可能需要更多的参考图像或额外的域适应步骤。方法假设参考集能覆盖目标人物的主要外观变化；若参考集过于单一（如全部为正面中性表情），则个性化子空间的表达能力受限（Fig. 6 的多样性消融已暗示此边界）。此外，评估依赖预先知晓人物特征的用户研究，存在主观偏差；使用广泛识别公众人物进行定性展示虽增强了结果的可感知性，但基于合理使用（fair-use）图像的隐私与伦理审查尚不充分。

![[assets/figures/papers/paper_list_l68_https_mystyle_personalized_prior_github_io/figures/015_Figure_10.jpg]]
*Figure 10: Comparing editing performance with priors of different generators – FFHQ-StyleGAN, tuned with DiffAugment, tuned with MyStyle (ours). ID score is reported for head pose. User study values reflect the percentages of responses in which the compared method was preferred over MyStyle*

![[assets/figures/papers/paper_list_l68_https_mystyle_personalized_prior_github_io/figures/009_Figure_8.jpg]]
*Figure 8: Comparing the synthesis of our generator to few-shots training approaches – Ojha et al. [2021], and DiffAugment [Zhao et al. 2020]. The user study values reflect the percentages of images that appeared real to the users. Generated images of Adele are provided for visual inspection. Our results exhibit diverse appearances of Adele, which are faithful to her actual different appearances over several years*

![[assets/figures/papers/paper_list_l68_https_mystyle_personalized_prior_github_io/figures/011_Figure_9.jpg]]
*Figure 9: Comparison of our personalized enhancement with alternative approaches. "Domain Prior“ refers to ComodGAN [Zhao et al. 2021] for inpainting and GPEN [Yang et al. 2021a] for super-resolution. "+FT“ refers to fine-tuning these methods on the personalized set. Zoom-in to better view fine details. User study values reflect the percentages of responses in which the compared method was preferred over MyStyle*

## 定位与知识库关联

### 一、改变的“槽位”：从通用域先验到个性化域先验

MyStyle 相对于已有工作的本质差异，在于将图像生成与增强任务中使用的**生成器先验类型**这一关键槽位，从“通用域先验”替换为“个性化域先验”。具体而言：

- **基线槽位值**：在 FFHQ 等大规模人脸数据集上预训练的 StyleGAN 生成器 $G_d$，构成一个覆盖广泛人脸的通用域先验。基于该先验的方法（如用于修复的 **CoModGAN** (Zhao et al., 2021)、用于超分辨率的 **GPEN** (Yang et al., 2021a)）在投影或反演时，只能在通用人脸流形上搜索最优潜在编码，无法保证输出结果保留特定个体的身份特征。

- **MyStyle 的槽位值**：在少量（约100张）个人肖像照片上对预训练生成器进行微调，得到个性化生成器 $G_p$。该生成器在锚点附近形成了一个局部、低维的个性化流形，使得后续的图像增强投影和语义编辑均被约束在此流形内，从而在根本上保证了身份保持。

这一槽位变更的因果链条是：微调改变了生成器在锚点邻域的局部几何结构 → 锚点间的插值和邻域随机游走均保持高身份得分（Fig. 4）→ 基于投影的图像增强（修复、超分辨率）自然继承此身份保持特性。这与仅改变训练策略（如 **Ojha et al.** (2021) 的少样本域适应、**DiffAugment** (Zhao et al., 2020) 的数据增强）或仅在通用先验上微调（Domain Prior + FT）有本质区别：后者虽然也使用了个人数据，但并未显式建模个性化子空间，也未在推理时施加投影约束。

### 二、知识库挂载点

MyStyle 可挂载到知识库的以下节点：

1. **个性化生成先验 (Personalized Generative Prior)**：这是核心贡献节点。与通用域先验形成对比，MyStyle 通过“锚点定义 + 生成器微调 + 膨胀凸包约束”三阶段流程，构建了针对特定个体的生成空间。该节点下可关联的关键属性包括：锚点数量与多样性对先验表达能力的影响（Fig. 6）、扩张参数 $\beta$ 对身份保持与重建精度权衡的控制（Fig. 5）。

2. **膨胀凸包约束 (Dilated Convex Hull Constraint)**：在 StyleGAN 潜在空间中，MyStyle 不直接使用锚点的标准凸包，而是引入扩张参数 $\beta \ge 0$，允许系数 $\alpha_i \ge -\beta$（同时保持 $\sum_i \alpha_i = 1$），形成一个膨胀凸包 $\mathcal{P}_\beta$。这一约束是连接“个性化生成器微调”与“图像增强投影优化”的关键桥梁。知识库中可记录：$\beta=0$ 时退化为标准凸包（最强先验、最低表现力）；增大 $\beta$ 则先验逐渐弱化，最终趋近无约束的 $W_p$ 空间。

3. **投影式图像增强 (Projection-based Enhancement)**：MyStyle 将图像修复、超分辨率等任务统一为在 $\alpha^+$ 空间中优化潜在编码，目标是最小化退化图像在未损坏区域的重建损失。与通用域先验下的投影方法相比，关键差异在于优化变量的搜索空间从 $W^+$ 变为受膨胀凸包约束的 $\alpha^+$ 空间，并额外引入了层偏移正则 $\mathcal{L}_{reg}(\Delta)$ 和总和约束 $\mathcal{L}_{sum}$。

4. **个性化语义编辑 (Personalized Semantic Editing)**：MyStyle 将通用编辑方向投影到锚点张成的子空间 $V$ 上，并通过计算编辑后编码对应的最小扩张参数 $\beta_{edit}$ 来验证编辑是否仍在个性化子空间内。这为语义编辑提供了身份保持的理论保证。

### 三、适用边界

MyStyle 的有效性依赖于以下前提条件，超出这些边界时性能可能下降：

1. **参考集质量与多样性**：消融实验（Fig. 6）表明，初期增加参考图像数量可显著提升先验表达能力，但达到一定数量后，多样性成为主导因素。若参考集仅包含单一表情、单一光照条件下的正面照片，个性化空间将缺乏足够的表达能力来处理大姿态变化或极端光照的测试图像。

2. **预训练 StyleGAN 的域匹配**：MyStyle 依赖 StyleGAN 在 FFHQ 上预训练获得的解耦与平滑特性。若目标个体的外貌特征与 FFHQ 分布差异过大（如极端年龄、特殊装饰），微调后的生成器可能无法有效泛化。论文未提供此类边缘案例的系统评估。

3. **扩张参数 $\beta$ 的选择**：$\beta$ 需要在身份保持与重建精度之间权衡（Fig. 5）。论文未给出自动选择 $\beta$ 的方法，实际应用中可能需要针对不同任务手动调整。在 held-out 测试中（Fig. 21b），MyStyle 的身份得分（0.75 ± 0.03）虽优于所有基线，但相比在训练集上的表现（0.81 ± 0.04）仍有下降，说明泛化到未见过的姿态和表情时仍存在身份保持的退化。

4. **锚点的固定性**：消融实验（Fig. 22）表明，联合优化锚点与生成器（类似 **GLO** (Bojanowski et al., 2017)）会导致生成结果模糊、失真。因此 MyStyle 要求锚点必须通过预训练编码器预先计算并固定，这限制了参考图像编码精度的上限。

### 四、后续研究启发

1. **更丰富的个性化先验建模**：当前膨胀凸包是锚点的线性组合，本质上是一个低维线性子空间。未来工作可探索非线性个性化流形建模（如通过神经网络参数化的流形），以在保持身份约束的同时提升对复杂变化的表达能力。

2. **自动确定最优 $\beta$**：$\beta$ 的取值目前依赖经验或手动调节。可研究基于验证集身份保持与重建精度曲线自动选择 $\beta$ 的方法，或设计任务自适应的 $\beta$ 调节机制。

3. **跨域个性化先验**：MyStyle 局限于 StyleGAN 的人脸域。将其扩展到其他生成模型架构（如 Diffusion Models）或其他图像域（如人体、场景），需要重新设计个性化子空间的定义方式和投影优化策略。

4. **隐私与伦理考量**：论文使用广泛识别的人物进行定性评估，基于合理使用图像，但未提供严格的隐私审查机制。在实际部署中，个性化生成先验可能被滥用于生成虚假肖像，需要配套的防伪检测和授权机制。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/MyStyle_A_Personalized_Generative_Prior.pdf]]