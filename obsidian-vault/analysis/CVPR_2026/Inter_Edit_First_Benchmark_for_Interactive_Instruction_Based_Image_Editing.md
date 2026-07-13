---
title: "Inter-Edit: First Benchmark for Interactive Instruction-Based Image Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Inter_Edit_First_Benchmark_for_Interactive_Instruction_Based_Image_Editing.pdf
project_link: null
code_link: "https://github.com/Delong-liu-bupt/Inter-Edit"
aliases:
- IIIBIE
- Inter-Edit
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将编辑输入从精确mask或冗长文本描述转变为简洁指令与不精确空间引导（涂鸦）的组合，使模型学习从模糊的空间线索中推理目标区域并生成自然融合的编辑结果。
primary_logic: 通过大规模自动生成并模拟用户不精确标注的数据集，以及设计位置感知评估指标，可以训练模型理解模糊空间意图，在编辑区域内外实现一致性，从而统一语义灵活性与空间精确性。
claims:
- 提出了交互式指令图像编辑(I3E)任务，结合简洁文本指令和不精确空间引导，实现直观、高质量的定位编辑。
- 自动数据生成流水线创建了包含1,099,964个训练样本的Inter-Edit数据集，其mask模拟了用户的不精确标注。
- 提出的位置感知评估指标（包括BDS、区域保真度、VQA分数）与人类主观判断高度相关。
- 基于Inter-Edit训练的三种基线方法（RNI、CIA、CJT）在定位精度和编辑质量上显著超越现有SOTA模型，包括闭源系统。
---

# Inter-Edit: First Benchmark for Interactive Instruction-Based Image Editing

> [!tip] 核心洞察
> 通过大规模自动生成并模拟用户不精确标注的数据集，以及设计位置感知评估指标，可以训练模型理解模糊空间意图，在编辑区域内外实现一致性，从而统一语义灵活性与空间精确性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Inter-Edit：交互式指令图像编辑的首个基准 |
| 英文题名 | Inter-Edit: First Benchmark for Interactive Instruction-Based Image Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_Inter-Edit_First_Benchmark_for_Interactive_Instruction-Based_Image_Editing_CVPR_2026_paper.html) · [Code](https://github.com/Delong-liu-bupt/Inter-Edit) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | I3E (Interactive Instruction-based Image Editing) |
| Dataset | Inter-Edit test set |

> [!tip] 效果简介
> - Inter-Edit test set (6,250 样本) 上，Human Eval. score (higher better) 6.672 (RNI, 论文提出的主要基线) vs 其他方法未在上下文中提供数值 (N/A)。
> - Inter-Edit test set 上，S_in (In-Region Fidelity) 0.976 (RNI, CJT) vs N/A (显著超越SOTA) (N/A)；BDS (Boundary Discontinuity, lower better) 未提供精确值 vs 5.329 (Q-Edit, 非基线方法中最优) (N/A)。

## 概要

图像编辑领域长期面临一对核心矛盾：**语义灵活性**与**精确空间控制**难以兼得。基于文本指令的编辑方法（如 Qwen-Image-Edit-2509 等）虽能理解丰富语义，却无法可靠地将编辑定位到目标区域；基于 mask 的方法虽能提供空间约束，但要求用户绘制高质量、与物体边界严格对齐的 mask，且编辑结果常出现边界伪影、环境变化难以自然传播等问题。

针对这一瓶颈，本文提出 **交互式指令图像编辑（Interactive Instruction-based Image Editing, I3E）** 任务，将编辑输入从精确 mask 或冗长文本描述转变为**简洁文本指令 + 不精确空间引导（涂鸦/粗略 mask）** 的组合。核心洞见在于：通过大规模自动生成模拟用户不精确标注的数据集，并设计位置感知的评估指标，可以训练模型从模糊的空间线索中推理目标区域，生成边界自然融合的编辑结果。

方法层面，论文构建了包含三阶段的自动数据生成流水线（来源图像生成 → 迭代指令精炼 → 自然化 mask 生成与过滤），产出了 **1,099,964 个训练样本**的 Inter-Edit 数据集，其 mask 刻意模拟用户手绘的不精确性。在此基础上，提出三种基线方法（RNI、CIA、CJT），分别通过辅助 ControlNet 分支、红色框叠加图像输入、原图与 mask 联合输入等策略，将空间引导条件注入扩散模型。评估方面，设计了包括区域保真度（$S_{in}$）、背景保持度（$S_{out}$）、边界不连续分数（BDS）和 VQA 自动评分在内的位置感知指标套件，与人类主观判断高度相关。

实验表明，基于 Inter-Edit 训练的三种基线方法在定位精度和编辑质量上显著超越现有 SOTA 模型（包括闭源系统），验证了 I3E 范式在统一语义灵活性与空间精确性方面的有效性。



图像编辑是视觉内容创作的核心需求，而“精确的空间控制”是实际应用中最常见却又最难满足的要求之一。当前主流方案在语义灵活性与空间精确性之间始终存在难以调和的矛盾，形成了该领域的关键瓶颈。

**指令式编辑的定位困境。** 以文本指令驱动的编辑模型（如 **Q-Edit** 等）允许用户通过自然语言描述编辑意图，语义表达极为灵活，但在空间定位上表现脆弱——即便是最先进的闭源商业系统，也常常无法准确地将编辑操作限定在用户期望的目标区域内（见 Figure 1）。文本天然缺乏像素级空间约束能力，导致编辑结果出现位置偏差或意外溢出。

**Mask式编辑的交互负担。** 基于mask的方法虽然能够提供精确的空间控制，却将沉重的交互成本转嫁给了用户：用户必须绘制与目标区域边界高度对齐的高质量mask，这一过程耗时且需要相当的操作技巧。更关键的是，mask方法通常难以自然地传播编辑引起的环境变化（如阴影、反射、光照一致性），容易在编辑边界产生明显的伪影和融合痕迹，破坏图像的整体和谐感。

**根本矛盾。** 上述两种范式的对立揭示了一个深层瓶颈：现有方法无法同时提供语义灵活性与精确空间控制。文本指令可靠地传达“做什么”却说不清“在哪里做”；mask精确地指定“在哪里做”却无法自然地处理“编辑如何与环境融合”。用户真正需要的是既能用简洁语言表达意图、又能以轻量空间标记划定目标区域的编辑方式，而非在两个极端之间做取舍。

**本文动机。** 针对这一矛盾，本文引入**交互式指令图像编辑（Interactive Instruction-based Image Editing, I3E）**任务，其核心思想是将编辑输入从“精确mask或冗长文本描述”转变为“简洁文本指令 + 不精确空间引导（涂鸦）”的组合。这一范式转变的关键假设是：模型可以从模糊的空间线索中推理出目标区域，并生成与周围环境自然融合的编辑结果，从而在语义灵活性与空间精确性之间建立统一。为系统性地支撑这一任务，本文进一步构建了首个大规模基准数据集**Inter-Edit**，设计了位置感知的评估指标体系，并提出了三种基线方法，为该方向提供了完整的实验与评测框架。



## 核心方法与创新机理

### 问题瓶颈：语义灵活性与空间精确性的两难困境

现有图像编辑方法长期面临一个根本性矛盾：**文本指令驱动的方法**（如 Q-Edit 等）虽能灵活表达编辑意图，但缺乏可靠的空间定位能力，即使是最先进的闭源模型也难以精确控制编辑位置；**基于 mask 的方法**虽能提供精确的空间控制，却高度依赖用户设计高质量的像素级精确 mask，且难以自然传播编辑区域外的环境变化，容易产生边界伪影。这一瓶颈使得直观、高质量的空间定位编辑在实际应用中难以实现。

### 关键创新：将模糊空间引导转化为可控条件

本文的核心创新在于提出**交互式指令图像编辑（Interactive Instruction-based Image Editing, I3E）**任务，其本质是将编辑输入范式从“精确 mask 或冗长文本”转变为**“简洁文本指令 + 不精确空间涂鸦”的组合**。这一转变的深层逻辑在于：让模型学会从模糊的空间线索中推理目标区域，而非依赖精确的像素级标注。具体而言，I3E 在以下三个维度实现了突破性创新：

#### 创新一：输入范式的根本性重构

I3E 将空间引导从精确的像素级 mask（baseline 值）替换为**不精确的涂鸦式 mask**，允许模糊边界和不完美标注。这一改变直接降低了用户的操作门槛——用户只需用粗略的涂鸦标记编辑区域，无需精细勾勒物体轮廓。模型通过学习从这些模糊线索中推理编辑范围，实现了**语义灵活性与空间精确性的统一**。

#### 创新二：百万级模拟用户标注的数据集

为支撑上述范式转变，论文提出了一套**全自动数据生成流水线**，构建了包含 **1,099,964 个训练样本**的 Inter-Edit 数据集。该流水线的关键设计在于：

- **迭代指令精炼机制**：采用“编辑-再生成”循环工作流，由 MLLM 生成初始编辑指令 → 编辑模型执行 → 结果回传 MLLM 重新生成更精确的指令与边界框，确保指令与空间标注的高度一致性。
- **自然化 mask 模拟**：通过 SAM-2 分割后经形态学操作（膨胀/腐蚀）平滑处理，模拟真实用户手绘 mask 的模糊特性，而非使用严格对齐分割边界的精确 mask。消融实验证实，去除该后处理步骤会显著降低模型在真实世界数据上的泛化能力。
- **MLLM 质量过滤**：利用 MLLM 自动过滤低质量样本，消融实验表明去除该步骤会引入噪声样本，显著降低编辑性能。

#### 创新三：位置感知评估指标体系

针对 I3E 任务的双重目标——（1）在指定区域内忠实执行编辑意图；（2）保持区域外内容不变——论文提出了**一套与人类感知高度相关的位置感知评估指标**：

- **区域保真度** $S_{in}$：利用 Alpha-CLIP 计算编辑区域内编辑结果与真值的语义相似度：
  $$\boldsymbol{S_{in}} = S_{cos}(E_{\alpha}(I_e, M), E_{\alpha}(I_{gt}, M))$$

- **背景保持度** $S_{out}$：计算非编辑区域编辑结果与源图像的相似度：
  $$\boldsymbol{S_{out}} = S_{cos}(E_{\alpha}(I_e, 1-M), E_{\alpha}(I_s, 1-M))$$

- **边界不连续分数 BDS**：衡量 mask 边界内外梯度幅值差异，值越低表示过渡越自然：
  $$\mathrm{BDS} = \left| \frac{||\mathcal{G}(I_{out}) \odot T_{in}||_1}{||T_{in}||_1} - \frac{||\mathcal{G}(I_{out}) \odot T_{out}||_1}{||T_{out}||_1} \right|$$

- **VQA 自动评分**：通过 MLLM 自动评估编辑成功度、自然度、美学和对齐度四个维度：
  $$\{S_{edit}, S_{nat}, S_{aes}, S_{align}\} = \Phi_{VQA}(I_s, I_e, M, P_{vqa})$$

这些指标的设计突破了传统全局相似度指标无法区分编辑区域与背景区域的局限，为空间定位编辑提供了细粒度的自动化评估手段。

#### 创新四：三种条件注入策略的系统探索

为将模糊空间引导有效注入编辑模型，论文设计了三种互补的基线方法（见 Figure 4），系统探索了条件注入的不同策略：

1. **Reference Net Injection (RNI)**：通过辅助 ControlNet 分支将控制条件注入编辑模型，在保持背景完整性方面表现最强（$S_{out}=0.974$）。
2. **Conditional Image Augmentation (CIA)**：将 mask 边缘以“红框”形式叠加到原图上，仅需少量数据训练 LoRA，实现轻量级条件注入。
3. **Concat Joint Training (CJT)**：将原图与 mask 联合输入，在编辑成功度上达到最高（$S_{edit}=6.338$）。

三种方法均在 Inter-Edit 训练集上使用 flow-matching loss 训练，实验表明它们**在定位精度和编辑质量上显著超越现有 SOTA 模型**（包括闭源系统），其中 RNI 在人类评估中得分最高（6.672）。

### 方法谱系与知识库定位

I3E 在图像编辑方法谱系中占据了一个独特的位置：它既不同于纯文本指令方法（如 Q-Edit）缺乏空间控制，也不同于传统 mask 方法（如基于 SAM 的编辑流程）依赖精确标注。其核心贡献在于**通过大规模自动生成模拟用户不精确标注的数据集，以及设计位置感知评估指标，训练模型理解模糊空间意图**，从而在编辑区域内外实现一致性。这一范式为交互式图像编辑设立了首个系统性基准，并为未来扩展到视频编辑、三维场景编辑等方向奠定了基础。



Inter-Edit 基准的构建围绕一个核心瓶颈展开：现有图像编辑方法无法同时提供语义灵活性与精确空间控制——文本指令难以可靠地空间定位，基于 mask 的方法则依赖高质量 mask 且难以自然传播环境变化，易产生边界伪影。为解决这一问题，本文提出 **交互式指令图像编辑（I3E）** 任务，将编辑输入从精确 mask 或冗长文本描述转变为**简洁文本指令 + 不精确空间引导（涂鸦/scribble）** 的组合，使模型学习从模糊的空间线索中推理目标区域并生成自然融合的编辑结果。

整体框架由两大模块构成：**自动数据生成流水线（训练集构建）** 和 **用户中心标注流程（测试集构建）**，如图 2 所示。

### 自动数据生成流水线（训练集）

训练集的构建采用全自动三阶段流水线，最终生成包含 **1,099,964 个图像编辑对** 的大规模数据集，其 mask 模拟了用户的不精确标注而非严格分割对齐：

1.  **阶段一：来源图像生成（Source Image Generation）**
    利用大语言模型（LLM）生成多样化的图像描述提示，通过文生图（T2I）模型合成高度多样的源图像，为后续编辑提供丰富的视觉基础。

2.  **阶段二：迭代指令精炼（Iterative Instruction Grounding Refinement）**
    采用循环“编辑-再生成”工作流：多模态大语言模型（MLLM）首先生成编辑指令，编辑模型据此执行编辑；编辑结果回传至 MLLM，由其重新生成更精确的指令与边界框标注。这一迭代过程确保指令与编辑区域之间的语义对齐。

3.  **阶段三：自然化 mask 生成与过滤（Naturalistic Mask Generation and Filtering）**
    利用 SAM-2 对第二阶段得到的边界框进行分割，随后通过形态学操作（膨胀、腐蚀等）平滑 mask 边缘，模拟用户手绘涂鸦的自然模糊特性。最后，MLLM 对生成样本进行质量过滤，剔除低质量编辑对。

训练集的编辑类型分布为：**局部编辑 37.1%，添加 28.4%，移除 28.0%，纹理编辑 6.5%**，覆盖了多样化的用户编辑需求。

### 用户中心标注流程（测试集）

测试集的构建遵循与训练集相同的采集顺序（源图像 → 编辑图像 → 编辑指令 → 编辑区域），但采用人工标注以确保真实用户交互模式的捕捉。标注者提供简洁的文本指令和直观的手绘 mask，测试集由 10 名不同性别和年龄的标注者手动标注以减少偏差，最终包含 6,250 个样本。

### 条件注入机制（三种基线策略）

为将空间引导条件（不精确 mask）注入编辑模型，本文提出三种互补的基线策略，架构对比如图 4 所示：

-   **RNI（Reference Net Injection）**：添加辅助 ControlNet 分支，将控制条件（mask）通过旁路网络注入编辑模型。
-   **CIA（Conditional Image Augmentation）**：将提取的 mask 边缘以红色框叠加到原始图像上，形成修改后的输入图像，通过 LoRA 进行高效微调。
-   **CJT（Conditional Joint Training）**：将原始图像与 mask 作为联合输入直接馈送至编辑模型。

三种方法均使用 flow-matching loss 作为监督信号，在 Inter-Edit 训练集上训练。其中 RNI 在人类评估中得分最高（6.672），CJT 在编辑成功度（S_edit）上表现最优（6.338），而两者在区域保真度（S_in）上均达到 0.976，显著超越现有 SOTA 方法。

### 补充图表

![[assets/figures/papers/paper_list_l2208_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Inter_Edit_First_B/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the Inter-Edit benchmark construction. (a) A three-stage automated pipeline for synthesizing large-scale training data that simulates user annotations for I3E model training. (b) A user-centered annotation process for the Inter-Edit test set, where human annotators provide concise instructions and intuitive hand-drawn masks to capture realistic user interaction patterns*

![[assets/figures/papers/paper_list_l2208_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Inter_Edit_First_B/figures/002_Figure_1.jpg]]
*Figure 1: In practice, precise spatial editing is a common requirement. However, current instruction-based editing models, even the most advanced proprietary ones, struggle to achieve accurate localization. Mask-based approaches can provide spatial control but heavily rely on users to design high-quality masks that precisely align with their intent. In contrast, our proposed task enables natural and seamless editing with only simple scribble guidance, and we also establish a comprehensive benchmark and baseline methods for systematic evaluation*



### 交互式指令图像编辑任务定义

Inter-Edit 将图像编辑形式化为一个条件生成问题。给定源图像 $I_s$、简洁文本指令 $T$ 以及不精确的空间引导 $M$（手绘涂鸦或粗糙 mask），模型需生成编辑后图像 $I_e$，使其在 $M$ 指示的区域内忠实地执行 $T$ 描述的编辑操作，同时保持 $M$ 外部区域与 $I_s$ 一致。

该任务的核心挑战在于：$M$ 并非精确的像素级分割 mask，而是模拟用户自然标注的模糊边界——这正是 Inter-Edit 与现有 mask-based 方法的本质区别。

### 数据生成流水线的三阶段模块

Inter-Edit 训练集通过全自动三阶段流水线构建（Figure 2），各模块设计如下：

**阶段一：高多样性源图像生成。** 利用大语言模型（LLM）生成覆盖广泛场景、物体和风格的多样化提示词，再通过文生图（T2I）模型合成源图像。该模块确保数据集的视觉多样性，避免模型过拟合于特定域。

**阶段二：迭代指令精炼。** 这是数据质量的关键保障模块，采用“编辑-再生成”循环工作流：MLLM 首先生成初始编辑指令 → 编辑模型执行编辑 → 将编辑结果回传 MLLM → MLLM 基于实际编辑效果重新生成更精确的指令和边界框标注。此迭代机制有效消除了指令与编辑结果之间的歧义，确保训练对中的指令高度可靠。

**阶段三：自然化 mask 生成与过滤。** 利用 SAM-2 对阶段二产生的边界框进行分割，随后通过形态学膨胀/腐蚀操作平滑 mask 边界，模拟用户手绘的不精确性。最后，MLLM 对样本进行质量过滤，剔除编辑效果不佳或 mask 不合理的低质量对。消融实验证实，去除 MLLM 过滤步骤会引入噪声样本，显著降低编辑性能。

最终 Inter-Edit 数据集包含 1,099,964 个图像编辑对，编辑类型分布为：局部修改 37.1%、添加 28.4%、移除 28.0%、纹理编辑 6.5%。

### 三种基线方法的条件注入模块

论文提出三种将空间引导条件注入编辑模型的不同策略（Figure 4），均以 FLUX 为骨干网络，使用 flow-matching loss 在 Inter-Edit 训练集上训练：

![[assets/figures/papers/paper_list_l2208_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Inter_Edit_First_B/figures/005_Figure_4.jpg]]
*Figure 4: Three baseline methods for the I3E task. The three approaches integrate the additional control condition of I3E into the network through different strategies: adding a bypass branch (RNI), modifying the original image (CIA), or jointly feeding multiple inputs (CJT)*

- **Reference Net Injection（RNI）：** 采用 ControlNet 作为辅助旁路分支，将 mask 条件注入编辑模型。ControlNet 编码器接收 $I_s$ 和 $M$ 的拼接输入，其输出特征与主去噪网络的多层特征相加融合。该方法在不修改原始模型结构的前提下实现空间条件控制。

- **Conditional Image Augmentation（CIA）：** 将 mask 边界提取为“红色框”叠加到原始图像 $I_s$ 上，形成增强输入。该方案将空间信息直接编码在像素空间中，仅需少量数据训练 LoRA（低秩适配）即可使模型学会解读红色框标记的编辑区域。

- **Conditional Joint Training（CJT）：** 将 $I_s$ 和 $M$ 作为两个独立输入联合送入网络，通过交叉注意力机制在去噪过程中融合空间条件。该方法在多输入联合建模上最为直接。

### 位置感知评估指标体系

为评估 I3E 任务的双重目标——编辑区域内忠实执行指令、编辑区域外保持背景不变——论文提出一套位置感知评估指标。

**区域语义保真度。** 利用 Alpha-CLIP 编码器 $E_{\alpha}$ 计算 mask 引导下的语义相似度：

$$S_{in} = S_{cos}(E_{\alpha}(I_e, M), E_{\alpha}(I_{gt}, M))$$

其中 $S_{cos}$ 为余弦相似度，$I_{gt}$ 为 ground-truth 编辑图像。$S_{in}$ 衡量编辑区域 $M$ 内生成内容与目标的语义一致性。

**背景保持度。** 对称地计算非编辑区域的相似度：

$$S_{out} = S_{cos}(E_{\alpha}(I_e, 1-M), E_{\alpha}(I_s, 1-M))$$

$S_{out}$ 量化编辑后图像在 $M$ 外部区域与源图像 $I_s$ 的保持程度。

**边界不连续度（BDS）。** 为评估编辑区域与背景之间的过渡自然度，BDS 计算 mask 边界内外梯度幅值的差异：

$$\mathrm{BDS} = \left| \frac{||\mathcal{G}(I_{out}) \odot T_{in}||_1}{||T_{in}||_1} - \frac{||\mathcal{G}(I_{out}) \odot T_{out}||_1}{||T_{out}||_1} \right|$$

其中 $\mathcal{G}(\cdot)$ 为梯度幅值算子，$T_{in}$ 和 $T_{out}$ 分别为 mask 边界的内侧和外侧窄带区域。BDS 值越低，表示边界过渡越自然，伪影越少。

**VQA 自动评分。** 通过 MLLM $\Phi_{VQA}$ 从四个维度自动评估编辑质量：

$$\{S_{edit}, S_{nat}, S_{aes}, S_{align}\} = \Phi_{VQA}(I_s, I_e, M, P_{vqa})$$

分别输出编辑成功度（$S_{edit}$）、自然度（$S_{nat}$）、美学质量（$S_{aes}$）和指令对齐度（$S_{align}$）分数。论文验证该自动评分与人类主观判断高度相关。



## 实验与关键发现

### 核心定量结果

论文在Inter-Edit测试集（6,250样本，由10名不同性别与年龄的标注者手动标注）上对三类编辑范式进行了系统对比：基于mask的方法、基于文本指令的方法（含闭源系统）以及本文提出的I3E基线方法。Table 1汇总了主要定量结果。

**整体编辑质量与人类偏好**：在人类评估（Human Eval.）中，RNI方法以6.672分取得最优，显著超越所有对比方法。在VQA自动评估的编辑成功度（S_edit）上，CJT方法以6.338分居首。这表明I3E方法在综合编辑质量上具有明确优势。

**区域定位精度**：在区域保真度（S_in）指标上，RNI与CJT均达到0.976，显著高于SOTA方法。该指标通过Alpha-CLIP计算编辑区域内的语义相似度，高值表明模型能准确理解模糊的空间引导并生成符合指令的内容。

**背景保持能力**：RNI在背景保持度（S_out）上取得0.974的最佳成绩，说明该方法在编辑目标区域的同时，对非编辑区域的扰动最小。这一特性对于实际交互场景中的用户体验至关重要。

**边界自然度**：在边界不连续度（BDS，越低越好）上，I3E方法整体优于对比方法。其中Q-Edit（Qwen-Image-Edit-2509）作为SOTA指令编辑模型，BDS为5.329，而I3E方法实现了更低的边界伪影，验证了不精确mask引导下模型学习自然过渡的能力。

### 定性分析

Figure 5展示了各方法的定性对比。基于mask的方法（黄色框）在mask边界处常出现明显伪影，且难以自然传播光照、阴影等环境变化。基于文本指令的方法（绿色框）缺乏空间定位能力，编辑效果常偏离用户意图区域。闭源系统（橙色框）虽整体质量较高，但在精确定位任务上仍存在失败案例（红色叉标记）。相比之下，I3E方法（蓝色框）在仅提供涂鸦级空间引导的条件下，实现了编辑区域内的语义一致性与区域外的无缝融合。

### 消融实验

Table 2报告了消融实验结果，揭示了数据生成流水线中关键组件的贡献：

- **Mask后处理步骤**：去除mask的形态学平滑操作后，模型在真实世界手绘mask上的泛化能力显著下降。这表明训练数据中模拟用户不精确标注的mask分布，是模型理解模糊空间意图的关键。

- **MLLM质量过滤**：移除MLLM过滤步骤会引入噪声样本，导致编辑性能显著降低。该步骤通过多模态大模型自动筛除低质量图像-编辑对，保证了训练数据的整体质量。

- **LoRA秩的选择**：实验表明LoRA秩设为32是最佳平衡点。继续增大秩值不再带来性能提升，反而可能导致过拟合。这一结论为实际部署提供了参数效率的参考。

### 方法对比与架构选择

Figure 4展示了三种基线方法在条件注入策略上的差异，Table 1的结果揭示了各策略的特性：

- **RNI（Reference Net Injection）**：通过辅助ControlNet分支注入空间条件，在背景保持（S_out=0.974）和人类偏好（6.672）上表现最优。其旁路设计使得编辑模型主干保持完整，有利于维持原始图像的生成先验。

- **CJT（Conditional Joint Training）**：将原图与mask联合输入，在编辑成功度（S_edit=6.338）上略优于RNI。联合输入策略使模型更直接地感知空间约束，但可能对背景信息造成轻微干扰。

- **CIA（Conditional Image Augmentation）**：通过红色框叠加图像输入，在保持轻量训练（仅需LoRA微调）的同时取得了有竞争力的结果，验证了简单可视化空间线索的有效性。

### 失败模式与局限性

尽管I3E方法在整体指标上表现优异，定性分析揭示了以下失败模式：

1. **复杂语义理解不足**：当编辑指令涉及抽象概念或多对象关系时，模型偶尔无法准确推理目标区域，导致编辑内容与指令不完全匹配。

2. **极端涂鸦质量敏感**：当用户提供的涂鸦过于稀疏或严重偏离目标边界时，编辑效果会退化。这反映了模型对空间引导质量的依赖边界。

3. **编辑类型差异**：数据集编辑类型分布（Local 37.1%, Add 28.4%, Remove 28.0%, Texture 6.5%）表明纹理编辑样本相对较少，可能影响该类编辑的性能。

需要指出的是，Table 1中各对比方法的完整数值未在提供的上下文中完全呈现，具体指标需参考原文或附录进行精确对比。

### 补充图表

![[assets/figures/papers/paper_list_l2208_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Inter_Edit_First_B/figures/006_Table_1.jpg]]
*Table 1: Main quantitative comparison on the Inter-Edit test set. ↑ indicates higher is better, and ↓ indicates lower is better. The best results are shown in bold, while the second and third-best results are underlined*

![[assets/figures/papers/paper_list_l2208_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Inter_Edit_First_B/figures/008_Table_2.jpg]]
*Table 2: Ablation study results of different variants*

![[assets/figures/papers/paper_list_l2208_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Inter_Edit_First_B/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison on the Inter-Edit test set. Our I3E methods (blue) are compared with mask-based (yellow), instructionbased (green), and proprietary models (orange). Red crosses mark editing failures, and red boxes highlight imperfect regions*



## 定位与知识库关联

### 1. 任务定义与问题定位

Inter-Edit 将图像编辑重新定义为 **交互式指令图像编辑 (I3E)**：输入为源图像、简洁文本指令和不精确的空间引导（涂鸦/粗糙mask），输出为在指定区域内自然融合编辑结果的图像。这一范式位于传统**纯文本指令编辑**与**精确mask编辑**之间，试图同时获得前者的语义灵活性和后者的空间可控性。

现有方法在这两个维度上存在结构性断裂：
- **指令编辑模型**（如 Qwen-Image-Edit-2509 等）依赖文本描述进行编辑，但文本天然缺乏精确的空间定位能力，导致“编辑了错误区域”或“遗漏目标对象”；
- **mask编辑方法**要求用户提供高质量像素级分割，边界伪影明显，且难以自然传播光照、纹理等环境变化到编辑区域内部；
- 两者都无法处理用户实际交互中的**模糊空间意图**——用户通常只能提供粗略涂鸦，而非精确分割。

Inter-Edit 的核心假设是：模型可以从模糊的空间线索中推理出目标区域，并生成与周围环境一致的结果，从而在单一框架内统一语义灵活性与空间精确性。

### 2. 与现有工作的关系

**2.1 相对于指令编辑方法的推进**

Inter-Edit 在输入空间上增加了一个关键的自由度：不精确的空间引导。这使得模型不再需要从纯文本中推断“在哪里编辑”，而是将文本用于描述“做什么”，将空间引导用于约束“在哪里做”。这一分工显著降低了对文本描述精确性的依赖，同时避免了纯指令方法中常见的定位失败。

**2.2 相对于mask编辑方法的改进**

传统mask编辑（如基于 SAM 分割 + inpainting 的 pipeline）存在两个瓶颈：
- **mask质量依赖**：用户必须提供精确的边界，否则编辑结果会出现明显伪影；
- **环境传播缺失**：mask内部编辑与外部背景之间的光照、纹理、景深一致性难以保证，边界处常出现不连续。

Inter-Edit 通过训练模型接受**自然化mask**（经形态学平滑、模拟手绘的不精确标注），使模型学会在模糊边界处推断合理的过渡，而非机械地沿mask边界剪切粘贴。这一能力通过边界不连续性指标（BDS, Eq. 4）进行量化评估，直接衡量mask边界内外梯度幅值差异。

**2.3 在数据驱动编辑方法中的位置**

Inter-Edit 属于**大规模自动生成训练数据 + 专用评估指标**驱动的方法谱系。其数据生成流水线（Figure 2）包含三个关键创新：
- **迭代指令精炼**：通过“编辑-回传-重新生成”循环，使 MLLM 能够生成与编辑结果精确对齐的指令和边界框，解决了自动标注中指令与视觉内容不一致的问题；
- **自然化mask生成**：使用 SAM-2 分割后经形态学操作平滑，模拟用户手绘的不精确性，而非直接使用精确分割mask；
- **MLLM质量过滤**：过滤低质量样本，消融实验表明去除该步骤会引入噪声样本，显著降低编辑性能。

### 3. 三种基线方法的设计逻辑

论文提出了三种将空间条件注入编辑模型的方法（Figure 4），代表了不同的条件融合策略：

| 方法 | 条件注入方式 | 设计权衡 |
|------|-------------|----------|
| **RNI** (Reference Net Injection) | 辅助 ControlNet 分支 | 保持原始模型结构完整，空间条件通过旁路注入；在背景保持（S_out=0.974）上表现最强 |
| **CIA** (Conditional Image Augmentation) | 红色框叠加到输入图像 | 最轻量的改造方案，仅需 LoRA 训练；空间信息直接编码在像素空间 |
| **CJT** (Concat Joint Training) | 原图与mask联合输入 | 多输入联合训练，在编辑成功度（S_edit=6.338）上最优 |

三种方法均在 Inter-Edit 训练集（1,099,964 样本）上使用 flow-matching loss 训练。RNI 在人类评估（Human Eval. 6.672）和背景保持上取得最佳综合表现，CJT 在编辑成功度上领先，CIA 提供了最轻量的适配方案。

### 4. 适用边界与局限

**适用场景**：
- 用户需要通过简单涂鸦指定编辑区域，而非提供精确mask；
- 编辑任务涉及局部修改、对象添加/移除、纹理替换等（数据集分布：Local 37.1%, Add 28.4%, Remove 28.0%, Texture 6.5%）；
- 需要编辑结果在边界处自然过渡，而非生硬拼接。

**已知局限**：
- **模型偏差传递**：训练数据通过 T2I 模型合成源图像、MLLM 生成指令、编辑模型执行编辑，整个流水线中的模型偏差可能层层累积，对下游编辑质量产生长远影响——这是一个开放的验证问题；
- **LoRA 秩的敏感性**：消融实验表明 LoRA 秩设为 32 是最佳平衡点，继续增大不再提升且可能导致过拟合，说明模型容量与泛化之间存在精细的权衡；
- **视频/3D扩展未验证**：当前方法仅针对单张静态图像，能否扩展到视频编辑或三维场景编辑仍是开放问题。

### 5. 评估体系的知识贡献

Inter-Edit 提出的位置感知评估指标是该工作的独立贡献，解决了传统全图相似度指标无法区分“编辑区域变化”与“背景破坏”的问题：

- **区域保真度 (S_in)**：利用 Alpha-CLIP 计算编辑区域内的语义相似度，公式为 $\boldsymbol{S_{in}} = S_{cos}(E_{\alpha}(I_e, M), E_{\alpha}(I_{gt}, M))$；
- **背景保持度 (S_out)**：计算非编辑区域的语义保持程度，$\boldsymbol{S_{out}} = S_{cos}(E_{\alpha}(I_e, 1-M), E_{\alpha}(I_s, 1-M))$；
- **边界不连续性 (BDS)**：$\mathrm{BDS} = \left| \frac{||\mathcal{G}(I_{out}) \odot T_{in}||_1}{||T_{in}||_1} - \frac{||\mathcal{G}(I_{out}) \odot T_{out}||_1}{||T_{out}||_1} \right|$，值越低表示过渡越自然；
- **VQA自动评分**：通过 MLLM 输出编辑成功度、自然度、美学和对齐度四个维度的分数。

这些指标与人类主观判断高度相关，为交互式编辑提供了比传统 FID/CLIP Score 更有诊断力的评估工具。

### 6. 开放问题

1. **自动生成数据的偏差传播**：整个数据流水线依赖多个预训练模型（T2I、MLLM、SAM-2、编辑模型），各环节的系统性偏差如何影响最终编辑质量，目前缺乏定量分析。
2. **时空扩展**：I3E 范式能否推广到视频编辑（需要时序一致性）或三维场景编辑（需要多视角一致性），是重要的后续方向。
3. **交互范式进化**：当前假设用户提供单次涂鸦和指令，但实际编辑可能是多轮交互过程——模型如何利用编辑历史进行迭代精炼，尚未探索。
4. **具体定量对比的完整性**：Table 1 中各方法的完整指标数值（包括 Q-Edit 等 SOTA 方法的 BDS=5.329）在提供的分析上下文中未完全呈现，精确的数值对比需参考原文或附录进行手动验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Inter_Edit_First_Benchmark_for_Interactive_Instruction_Based_Image_Editing.pdf]]
