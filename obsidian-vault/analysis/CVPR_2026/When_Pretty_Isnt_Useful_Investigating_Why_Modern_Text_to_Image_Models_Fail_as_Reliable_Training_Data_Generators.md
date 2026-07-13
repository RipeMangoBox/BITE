---
title: "When Pretty Isn't Useful: Investigating Why Modern Text-to-Image Models Fail as Reliable Training Data Generators"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/When_Pretty_Isn_t_Useful_Investigating_Why_Modern_Text_to_Image_Models_Fail_as_Reliable_Training_Data_Generators.pdf
project_link: null
code_link: "https://huggingface.co/blackforest-labs/FLUX.1-dev"
aliases:
- SSRDBF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 生成模型的保真度-多样性权衡：新模型倾向产生高密度、低覆盖率的合成数据集，即样本集中且缺乏类别内差异，同时引入纹理和高频失真。
primary_logic: 生成式视觉进步 ≠ 数据真实性进步；较新的 T2I 模型生成的图像虽然更美观，但作为训练数据反而使下游分类器在真实数据上的泛化能力持续下降，其根本原因是分布漂移和多样性崩溃。
claims:
- 训练于新 T2I 模型合成数据的分类器在真实测试集上的准确率随时间呈下降趋势。
- 合成图像的结构信息受影响较小，而纹理和高频成分受到严重损害，这是性能差距的主要来源。
- 合成数据的密度和覆盖率与泛化性能强相关：新模型的数据集呈现高密度、低覆盖率，即分布过于集中，缺乏多样性。
- Real→Synth 迁移准确率高而 Synth→Real 迁移准确率低的严重不对称性，表明合成域形成了易分类但偏离真实数据决策边界的簇。
---

# When Pretty Isn't Useful: Investigating Why Modern Text-to-Image Models Fail as Reliable Training Data Generators

> [!tip] 核心洞察
> 生成式视觉进步 ≠ 数据真实性进步；较新的 T2I 模型生成的图像虽然更美观，但作为训练数据反而使下游分类器在真实数据上的泛化能力持续下降，其根本原因是分布漂移和多样性崩溃。

| 字段 | 内容 |
|------|------|
| 中文题名 | 好看不中用：探究现代文本到图像模型为何无法可靠生成训练数据 |
| 英文题名 | When Pretty Isn't Useful: Investigating Why Modern Text-to-Image Models Fail as Reliable Training Data Generators |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Adamkiewicz_When_Pretty_Isnt_Useful_Investigating_Why_Modern_Text-to-Image_Models_Fail_CVPR_2026_paper.html) · [HuggingFace](https://huggingface.co/blackforest-labs/FLUX.1-dev) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Systematic Synth→Real Diagnosis and Benchmarking Framework |
| Dataset | ImageNet-1k, Density & Coverage, Cross-domain transfer |

> [!tip] 效果简介
> - ImageNet-1k (200-class subset, 100k training images) 上，Classification accuracy (Synth→Real, ResNet-50) Newer T2I models (e.g., Qwen-Image, Flux, Lumina) vs Older T2I models (e.g., SD v1.5, SD 2.1) (持续下降趋势（类名提示）)。
> - ImageNet-1k (200-class subset) 上，Synth→Real 分类准确率 vs. GenEval 和 CLIPScore 较新的 T2I 模型 vs 较早的 T2I 模型 (负相关：更高的文本对齐分数对应更低的训练数据效用（类名提示）)。
> - ImageNet-1k (structure vs. texture analysis) 上，Synth→Real 分类准确率差距 结构空间 (Depth) 分类器 vs 纹理空间 (BagNet) 分类器 (结构空间差距显著小于纹理空间差距)。

## 概要

**核心矛盾**：现代文本到图像（T2I）模型在视觉保真度和文本遵循度上持续进步，但作为训练数据生成器时，其合成数据训练的下游分类器在真实测试集上的准确率却呈**持续下降趋势**（Figure 1）。这一现象揭示了一个关键悖论：生成式视觉进步 ≠ 数据真实性进步。

**根本瓶颈**：新模型在追求美学质量和提示遵循度的过程中，坍塌到一个**狭窄的、以美学为中心的分布**，严重损害了数据多样性、纹理真实性和高频细节与真实数据的一致性。具体表现为合成数据集呈现**高密度、低覆盖率**的特征——样本在特征空间中过度集中，缺乏类别内差异（Figure 5）。

**因果机制**：通过系统诊断框架（Figure 2），本文定位了性能退化的三个主要维度：
1. **纹理损伤是主因**：在剥离纹理信息的深度结构空间中，合成数据与真实数据的性能差距大幅缩小；而仅依赖局部纹理特征（9×9 感受野）的分类器则暴露了巨大的纹理域差距（Figure 4 左）。
2. **高频成分失真严重**：低通滤波域的训练性能接近 RGB 域，而高通滤波域的性能差距显著更大，表明合成图像的高频细节遭到严重破坏（Figure 4 右）。
3. **分布漂移与多样性崩溃**：Real→Synth 迁移准确率高且随模型更新而上升，而 Synth→Real 准确率低且持续下降，呈现严重的不对称性——合成域形成了易被分类但偏离真实决策边界的孤立簇（Figure 6）。

**方法谱系与知识库定位**：本文构建了一套**系统化的 Synth→Real 诊断与基准测试框架**，而非提出新的生成模型。该框架以 13 个开源 T2I 模型为基线（从 **Stable Diffusion v1.5**（Rombach et al., CVPR 2022）到 **Flux-Dev**（Black Forest Labs, 2024）、**Qwen-Image**（Wu et al., arXiv 2025）等），在受控的 ImageNet-1k 200 类子集上生成合成训练数据，通过深度结构分类器、BagNet 纹理分类器、频率滤波分析和密度-覆盖率度量等模块化诊断工具，系统解耦纹理、结构、高频和分布多样性对泛化性能的影响。

**关键发现**：文本-图像对齐指标（GenEval、CLIPScore）与训练数据效用呈**负相关**——更高的对齐分数对应更低的迁移性能（Figure 3）。使用详细字幕提示可部分缓解性能退化，但会进一步降低数据多样性（覆盖率），无法从根本上解决分布漂移问题。

**局限与开放问题**：当前分析限于 ImageNet-1k 分类任务和 ResNet-50 架构，尚未验证在目标检测、分割等更复杂视觉任务中的适用性。专有闭源模型（如 DALL·E 3、Midjourney）的表现未知。如何在生成阶段引入对学习有用的多样性奖励，实现视觉保真度与数据真实性的协同提升，仍是待解决的关键问题。



文本到图像（T2I）生成模型在近三年经历了爆发式进步。从 **Stable Diffusion v1.5**（Rombach et al., CVPR 2022）到 **Flux-Dev**（Black Forest Labs, 2024）、**Qwen-Image**（Wu et al., arXiv 2025）等最新模型，生成图像的视觉保真度和提示遵循度持续攀升。一个自然而迫切的问题是：这些越来越“好看”的生成模型，是否也能作为更可靠的训练数据生成器，服务于下游视觉任务？

这一问题的现实意义不言而喻。真实数据的采集、清洗与标注成本高昂，且受隐私和版权约束日趋严格。若合成数据能有效替代真实数据，将极大降低模型训练的门槛。然而，现有工作对这一假设的验证存在明显缺口：多数研究仅评估单一或少数几代模型，缺乏对生成技术进步与训练数据效用之间关系的系统性、跨代际审视。

本文正是针对这一缺口展开。作者选取了 2022 至 2025 年间发布的 13 个开源 T2I 模型，在受控的 ImageNet-1K 子集上生成大规模合成数据集，训练标准 ResNet-50 分类器，并在真实测试集上评估其泛化能力。核心发现令人警醒：**随着 T2I 模型世代的更新，合成数据训练的分类器在真实数据上的准确率呈持续下降趋势**（Figure 1）。换言之，生成模型的“好看”并未转化为“有用”，甚至出现了系统性倒退。

这一现象揭示了生成式视觉研究中一个深层的**保真度-多样性权衡**：较新的 T2I 模型在追求视觉质量和文本对齐的过程中，其输出分布坍缩到了狭窄的、以美学为中心的区域，牺牲了类别内多样性和真实数据所具备的高频纹理细节。本文的动机正在于解剖这一退化现象的成因——是纹理失真、高频信息丢失，还是分布漂移与多样性崩溃？通过系统性的诊断框架，作者试图回答一个更根本的问题：**生成式视觉的进步，是否等价于数据真实性的进步？**



## 核心方法与创新机理

本工作的核心创新不在于提出新的生成模型或训练范式，而是构建了一套**系统性的合成数据诊断框架**，首次从数据真实性（data realism）而非视觉质量的角度，对 2022–2025 年间 13 个开源 T2I 模型作为训练数据生成器的效用进行了大规模基准测试。

### 1. 问题定义的逆转：从“生成更好看的图”到“生成更有用的训练数据”

以往工作默认 T2I 模型的进步（更高的分辨率、更强的文本遵循度、更美观的视觉输出）会自然转化为更好的合成训练数据。本文通过受控实验证明这一假设**在类名提示（class name prompt）条件下完全失效**：随着 T2I 模型代际更迭，合成数据训练的分类器在真实测试集上的准确率呈单调下降趋势（Figure 1）。这一发现将领域关注点从“如何生成更逼真的图像”扭转为“为什么更好的生成模型反而产生更差的训练数据”，并以此作为全文诊断的出发点。

### 2. 多维度解耦诊断管线

为定位性能衰退的根源，作者设计了一套**可控变换的诊断管线**（Figure 2），将合成数据的失真分解为三个正交维度，逐一量化其对下游泛化的影响：

- **纹理 vs. 结构解耦**：利用 Depth Anything V2 将 RGB 图像转换为深度图，在纯结构空间训练 ResNet-50，彻底剥离纹理信息；同时使用感受野仅 $9 \times 9$ 的 BagNet 分类器，仅捕捉局部纹理而无法利用全局形状。对比二者与 RGB 空间的性能差距，可定量归因纹理与结构各自的损伤程度。
- **高频 vs. 低频解耦**：对图像施加高通滤波（保留 $f \le 0.2 \times f_N$）和低通滤波（保留 $f \ge 0.8 \times f_N$），在频域上分离高频细节与低频轮廓。通过在滤波后的数据上独立训练分类器，揭示合成图像在不同频段的失真模式。
- **分布漂移与多样性量化**：基于 CLIP-ViT-L 视觉头提取特征，采用 Naeem et al. 的密度（density）与覆盖率（coverage）度量，在特征空间中直接量化合成数据相对于真实训练数据的分布对齐程度和类别内多样性。

### 3. 关键因果机制的发现

通过上述诊断管线，本文揭示了导致合成数据效用下降的**核心因果链**：

1. **纹理与高频成分是主要受损维度**：结构空间分类器的性能差距远小于纹理空间分类器（Figure 4 左）；低通滤波训练的性能紧贴 RGB 域，而高通滤波训练的性能差距显著更大（Figure 4 右）。这表明新 T2I 模型在追求视觉美学时，对纹理真实性和高频细节的损害最为严重。
2. **保真度-多样性权衡是深层瓶颈**：新模型生成的合成数据集呈现**高密度、低覆盖率**的特征——样本在特征空间中高度集中，缺乏类别内差异（Figure 5）。这种分布坍塌直接导致下游分类器在真实数据上的泛化能力下降。较低的密度和较高的覆盖率与更好的 Synth→Real 迁移准确率强相关。
3. **合成域与真实域的决策边界偏移**：Real→Synth 迁移准确率随模型更新而上升，而 Synth→Real 准确率持续下降（Figure 6），呈现严重的不对称性。这说明合成图像在特征空间中形成了**易于分类但与真实数据决策边界偏离的簇**——真实模型可以轻松识别合成图像，但合成数据训练的模型却无法泛化到真实域。

### 4. 与 baseline 的本质区别

本文并非提出一个新的 T2I 模型或数据增强方法，而是对现有 T2I 模型作为训练数据生成器的**元评估**。相较于直接使用 T2I 模型生成训练数据的 baseline 工作（如 Stable Diffusion 系列、Flux、Qwen-Image 等），本文的贡献在于：

- **建立了评估合成数据效用的基准框架**，而非参与生成质量的竞赛；
- **揭示了生成式视觉进步与数据真实性进步之间的脱节**，为领域提供了方向性警示；
- **提出了可复用的诊断工具链**（深度结构分类器、BagNet 纹理分类器、频域滤波、密度-覆盖率分析），可用于评估未来任何 T2I 模型作为训练数据源的适用性。

### 5. 局限与待验证边界

本文的分析范围明确限定在图像分类任务（ImageNet-1k 200 类子集）和开源 T2I 模型，且下游模型以 ResNet-50 为主。所发现的趋势是否在目标检测、分割等任务中成立，以及专有模型（如 DALL·E 3、Midjourney）是否呈现相同模式，仍需进一步验证。此外，详细字幕提示虽能缓解部分问题，但在缺乏原始图像标注的纯合成场景下不可行，其实用性受限。



本文提出了一套**系统化的合成→真实诊断与基准测试框架**，旨在解耦现代文生图模型作为训练数据生成器时的失效根源。框架的核心逻辑并非改进生成模型本身，而是通过受控的数据变换和跨域评估，逐层剥离并量化合成图像在**结构、纹理、频谱和分布**四个维度上的失真程度，最终建立这些失真与下游分类器泛化性能之间的因果关联。

### 流水线总览

整个框架由五个功能模块串联而成，形成从数据生成到诊断归因的闭环：

1. **T2I 生成**：以类名或详细描述为提示，调用不同时期发布的文生图扩散模型生成合成训练图像，控制统一的采样参数（CFG=2.0，50 步去噪，Turbo 版 4 步），确保比较的公平性。
2. **结构-纹理解耦**：利用深度估计模型将 RGB 图像转换为深度图，在仅保留全局形状的空间中训练分类器；同时采用感受野仅 $9 \times 9$ 的 BagNet 分类器，使其只能捕捉局部纹理而无法利用全局结构信息。
3. **频谱分离**：对图像施加高通滤波（保留 $f \leq 0.2 \times f_N$）或低通滤波（保留 $f \geq 0.8 \times f_N$），在频域上分离高频细节与低频轮廓，探测合成图像的谱失真模式。
4. **分布密度与覆盖率分析**：基于 CLIP-ViT-L 视觉头提取特征，计算合成数据集相对于真实训练集的密度和覆盖率指标，量化分布对齐程度与多样性崩溃程度。
5. **跨域迁移评估**：同时测量 Real→Synth 和 Synth→Real 两个方向的分类准确率，通过两者之间的不对称性揭示合成域决策边界与真实域的偏离程度。

### 模块间的信息流与逻辑关系

框架的输入是不同 T2I 模型生成的合成图像集，输出是一组可解释的诊断信号。各模块之间的信息流如下：

- **T2I 生成模块**作为数据源，为后续所有诊断模块提供统一的合成图像素材。
- **结构-纹理解耦**与**频谱分离**两个模块并行工作，分别从空间域和频域对合成图像进行变换，生成结构空间、纹理空间、低频域和高频域四种受控训练数据。通过比较这些变换域上的分类准确率与原始 RGB 域的差距，可以定位性能损失主要发生在哪个信息维度。
- **分布密度与覆盖率分析**模块独立于下游分类器训练，直接在特征空间中度量合成数据的多样性和覆盖范围，为解释泛化能力变化提供分布层面的证据。
- **跨域迁移评估**模块则从决策边界的角度，综合验证合成数据是否形成了偏离真实数据分布、且易于被分类器识别的“捷径簇”。

### 核心诊断逻辑

框架的诊断策略遵循“假设-隔离-验证”的原则：

- **假设**：纹理失真、高频损伤和分布多样性崩溃是导致合成数据训练效用下降的三个主要因素。
- **隔离**：通过深度空间训练移除纹理信息，通过 BagNet 限制结构信息的利用，通过频域滤波分离高/低频成分，通过密度-覆盖率指标量化分布特性。
- **验证**：若在移除某一信息维度后，合成数据与真实数据之间的性能差距显著缩小，则说明该维度是性能损失的关键来源。

这一设计使得框架能够在不修改任何 T2I 模型内部结构的前提下，仅通过对生成数据和下游训练流程的受控干预，完成对合成数据质量的细粒度归因分析。

### 补充图表

![[assets/figures/papers/paper_list_l2363_https_openaccess_thecvf_com_content_CVPR2026_html_Adamkiewicz_When_Prett/figures/002_Figure_2.jpg]]
*Figure 2: To probe which aspects of synthetic images are most affected, we transform images to suppress or amplify the effects of distortions in a given domain. To separate the effect of low and high level details, we measure the performance gap when training in depth space, which removes textures, and training a low-receptive-field (visualized in the figure) classifier which operates on 9 × 9 image patches and hence does not rely on structure. To separate the effects of high and low frequency distortions, we train on low and high-pass filtered images. Removing offending features should close the gap with relation to RGB, while removing non-offending features should widen it*



### 诊断框架总览

本工作构建了一个系统性的合成→真实诊断框架，用于定位 T2I 生成图像中损害下游训练效用的关键维度。框架围绕三个核心假设展开：(i) 纹理与结构失真，(ii) 高频成分失真，(iii) 分布漂移与多样性崩溃。通过对合成数据施加受控变换（Figure 2），逐一分离并量化这些因素的影响。

### 关键诊断模块

#### 1. 结构-纹理分离模块

该模块通过两个互补的分类器将图像的全局结构与局部纹理信息解耦：

- **深度结构分类器**：利用 Depth Anything V2 将 RGB 图像转换为深度图，随后在深度空间上训练 ResNet-50。深度图剥离了所有颜色和纹理信息，仅保留全局结构与形状。若性能差距在此空间显著缩小，则表明纹理损伤是主要瓶颈。
- **局部纹理分类器**：采用 BagNet（感受野仅 $9 \times 9$ 像素）进行训练与评估。该分类器仅能捕捉局部纹理特征，无法利用全局结构信息，用于量化纹理质量对分类性能的独立贡献。

#### 2. 频率分解模块

基于自然图像振幅谱近似遵循幂律分布 $S(f) \propto f^{-\alpha}$ 的先验知识，该模块通过频域滤波分离高频与低频成分：

- **高通滤波**：保留 $f \geq 0.8 \times f_N$ 的频率成分（$f_N$ 为奈奎斯特频率），移除低频结构信息，仅保留纹理细节与边缘。
- **低通滤波**：保留 $f \leq 0.2 \times f_N$ 的频率成分，移除高频纹理与噪声，仅保留全局形状与平滑结构。

通过在滤波后的数据上训练分类器并与 RGB 域性能对比，可精确定位谱失真所在频段。

#### 3. 分布密度与覆盖率评估模块

为量化合成数据相对于真实数据的分布对齐程度，该模块基于 CLIP-ViT-L 视觉编码器提取图像特征，并采用 Naeem et al. 的密度（density）与覆盖率（coverage）度量：

- **密度**：衡量合成样本在真实数据流形上的聚集程度。高密度意味着合成样本集中在真实分布的少数区域。
- **覆盖率**：衡量合成样本对真实数据分布的支持范围。低覆盖率意味着合成数据仅覆盖真实分布的狭窄子集。

密度与覆盖率共同揭示了合成数据集的分布宽度与集中度，是解释泛化性能差异的核心指标。

#### 4. 跨域迁移评估模块

该模块通过对比两个方向的分类准确率来探测合成域与真实域决策边界的偏离程度：

- **Real → Synth**：在真实数据上训练，在合成数据上测试。
- **Synth → Real**：在合成数据上训练，在真实数据上测试。

若 Real → Synth 准确率高而 Synth → Real 准确率低，表明合成数据形成了易于被真实模型分类的簇，但其决策边界与真实数据存在系统性偏移。

### 关键公式

本工作仅涉及一项显式公式，用于描述自然图像的频域先验：

$$S(f) \propto f^{-\alpha}$$

**变量含义**：
- $S(f)$：空间频率 $f$ 处的振幅谱（amplitude spectrum）。
- $\alpha$：幂律衰减指数，自然图像通常满足 $\alpha \approx 1$，即能量随频率升高而衰减。

该公式是频率分解模块的理论基础：合成图像若偏离此幂律分布（尤其是高频成分异常增强或衰减），将导致纹理失真，进而损害下游分类器的泛化能力。实验证实，合成图像的高频域性能差距远大于低频域，与幂律先验的偏离程度随 T2I 模型的更新而加剧。

### 补充图表

![[assets/figures/papers/paper_list_l2363_https_openaccess_thecvf_com_content_CVPR2026_html_Adamkiewicz_When_Prett/figures/004_Figure_4.jpg]]
*Figure 4: Performance comparison for (left) structure (depth-based classifier) and texture (local feature classifier), and (right) frequencyfiltered data for class name- and caption-guided synthetic datasets. Image structure is consistently less affected than texture, while high-frequency components degrade more strongly than low frequencies (especially in better-performing models)*



## 实验与关键发现

### 核心发现：生成式进步与训练数据效用的背离

本研究对 2022 至 2025 年间发布的 13 个开源 T2I 模型进行了系统性评估，核心实验设置如下：使用每个模型为 ImageNet-1k 的 200 类子集生成合成训练图像（以类名为提示，CFG=2.0，采样步数 50），在合成数据上训练 ResNet-50 分类器，并在真实测试集上评估（Synth→Real）。结果揭示了一个反直觉的趋势：**较新的 T2I 模型作为训练数据生成器时，下游分类器在真实数据上的准确率持续下降**（Figure 1）。这一趋势在多个模型代际间一致成立——从早期的 Stable Diffusion v1.5（Rombach et al., CVPR 2022）到最新的 Qwen-Image（Wu et al., arXiv 2025）和 Lumina Image 2.0（Qin et al., arXiv 2025），生成模型的视觉保真度和提示遵循度不断提升，但其合成数据的训练效用却同步恶化。

![[assets/figures/papers/paper_list_l2363_https_openaccess_thecvf_com_content_CVPR2026_html_Adamkiewicz_When_Prett/figures/001_Figure_1.jpg]]
*Figure 1: We train ResNet-50 classifiers on images generated by various T2I models for a subset of ImageNet-1k classes and evaluate their accuracy on real test data (Synth → Real). Our results reveal a downward trend over time. Newer models get progressively worse as reliable training data generators*

进一步分析表明，这一现象并非偶然：合成数据的训练效用与 T2I 模型在 GenEval 和 CLIPScore 等文本-图像对齐基准上的得分呈**负相关**（Figure 3）。在仅使用类名提示的条件下，对齐分数越高的模型，其合成数据训练的迁移准确率反而越低。这说明当前 T2I 模型的优化目标（视觉保真度、文本对齐）与下游任务对数据真实性和多样性的需求之间存在根本性张力。

![[assets/figures/papers/paper_list_l2363_https_openaccess_thecvf_com_content_CVPR2026_html_Adamkiewicz_When_Prett/figures/003_Figure_3.jpg]]
*Figure 3: Accuracy on the real ImageNet-1k test set versus GenEval score (top) and CLIPScore (bottom). Each point represents the performance of a classifier trained on data synthesized by a specific T2I model; the horizontal line indicates the baseline trained on real data. Across architectures, we observe a downward trend; higher benchmark scores correspond to lower transfer performance for class label prompts*

### 性能瓶颈定位：纹理与高频失真

为定位合成数据性能损失的具体来源，论文设计了三个诊断维度：**结构 vs. 纹理**、**高频 vs. 低频**、以及**分布密度与覆盖率**。

**结构与纹理分离实验**（Figure 4 左）使用两种互补的分类器：基于 Depth Anything V2 的深度图分类器（仅保留全局结构信息，去除纹理）和 BagNet 分类器（感受野仅 9×9，仅捕捉局部纹理特征）。结果显示，结构空间中的合成-真实性能差距显著小于纹理空间。这意味着合成图像的结构信息受损较轻，而**纹理质量是导致性能退化的主要瓶颈**。

**频率分解实验**（Figure 4 右）对图像施加高通滤波（保留 f ≤ 0.2×f_N）或低通滤波（保留 f ≥ 0.8×f_N）。结果表明，低频域的分类性能紧贴 RGB 域，而高频域的性能差距显著更大。结合自然图像振幅谱遵循幂律分布 $S(f) \propto f^{-\alpha}$ 的先验知识，这一发现表明**合成图像的高频成分失真最为严重**——新模型在追求视觉光滑和美学效果时，系统性地损害了真实数据中固有的高频纹理细节。

### 分布崩溃：高密度、低覆盖率的合成数据集

使用基于 CLIP-ViT-L 特征空间的密度与覆盖度量（Naeem et al. 方法）分析合成数据分布，Figure 5 揭示了新模型合成数据的一个结构性缺陷：**高密度、低覆盖率**。具体而言，较新的 T2I 模型生成的样本在特征空间中高度集中（高密度），但覆盖真实数据分布的范围更窄（低覆盖率）。这种分布模式意味着合成数据集缺乏类别内多样性，样本集中在少数“典型”模式上，无法覆盖真实世界中丰富的视觉变体。

![[assets/figures/papers/paper_list_l2363_https_openaccess_thecvf_com_content_CVPR2026_html_Adamkiewicz_When_Prett/figures/005_Figure_5.jpg]]
*Figure 5: Dataset diversity using density and coverage metrics from Naeem et al. [35], plotted against classifier accuracy on real data (color). Models with high density but low coverage produce visually consistent yet distributionally narrow samples, while those with higher coverage span a broader portion of real data space and correlate with better generalization. Thus, recent T2I models achieve higher sample quality through compact, high-density clusters but sacrifice diversity essential for training quality*

密度和覆盖率与泛化性能之间存在强相关：更低的密度和更高的覆盖率对应更高的 Synth→Real 迁移准确率。值得注意的是，使用详细字幕替代简单类名提示可以提升覆盖率并降低密度，从而改善迁移性能，但效果有限——详细提示主要改善低频和结构信息，对纹理和高频失真的修复作用有限，且会引入额外的分布偏移。

### 跨域迁移的不对称性

Figure 6 展示了一个极具诊断价值的不对称现象：**Real→Synth 迁移准确率高且随模型更新而上升，而 Synth→Real 迁移准确率低且持续下降**。这意味着真实数据训练的模型可以轻松分类合成图像（合成域对真实模型而言是“易分类”的），但合成数据训练的模型却越来越难以泛化到真实数据。这种严重的不对称性表明，合成数据在特征空间中形成了与真实数据分离的、决策边界偏离的簇——合成样本虽然视觉上逼真，但其底层特征分布已偏离真实数据的流形。

![[assets/figures/papers/paper_list_l2363_https_openaccess_thecvf_com_content_CVPR2026_html_Adamkiewicz_When_Prett/figures/006_Figure_6.jpg]]
*Figure 6: Comparison of cross-domain transfer for ResNet-50: classification accuracy of models trained on real data and evaluated on synthetic images (Real → Synth) versus the reverse setting (Synth → Real). Synthetic data are increasingly easy for realtrained models to classify, yet models trained on synthetic data transfer progressively worse to real test images, revealing growing asymmetry between visual and learning alignment*

### 消融与补充验证

除 ResNet-50 外，论文还在 ViT-Ti 和 ConvNeXt-Ti 上进行了补充验证，确认了趋势的架构无关性。详细字幕消融实验（Figure 5, Section 4.2）表明，虽然丰富提示可提升迁移准确率，但会降低合成数据的多样性（覆盖率），且在实际缺乏原始图像的纯合成场景下不可行。深度结构分类器消融（Figure 4 左）证实移除纹理信息后性能差距大幅缩小，而移除结构信息（BagNet）则扩大了差距，进一步确认纹理损伤是核心因素。频率域消融（Figure 4 右）显示详细提示对高频失真的修复有限，说明高频退化是当前 T2I 模型的内在特性，难以仅通过提示工程解决。

### 失败模式总结

综合上述证据，现代 T2I 模型作为训练数据生成器的主要失败模式可归纳为三点：
1. **纹理失真**：合成图像的纹理特征与真实数据存在系统性偏差，这是性能差距的最大来源。
2. **高频退化**：模型在优化视觉质量时抑制或扭曲了高频细节，导致合成数据缺乏真实图像的高频统计特性。
3. **分布多样性崩溃**：合成数据集呈现高密度、低覆盖率的特征，缺乏类别内多样性，导致下游模型在真实数据上的泛化能力受限。

这些失败模式相互关联：对视觉保真度和美学质量的优化倾向使模型坍塌到狭窄的、以美学为中心的分布，同时损害了纹理真实性和高频细节，最终导致合成数据的训练效用不升反降。



## 定位与知识库关联

### 1. 问题定位：生成式视觉进步 ≠ 数据真实性进步

本工作揭示了一个反直觉的核心矛盾：现代文生图（T2I）模型在视觉保真度和文本对齐度上的持续进步，并未转化为更好的合成训练数据效用。相反，**训练于新 T2I 模型合成数据的分类器在真实测试集上的准确率呈现持续下降趋势**（Figure 1）。这一发现挑战了“更好的生成模型自然产生更好的训练数据”这一普遍假设，将问题从“如何生成更逼真的图像”重新锚定为“如何生成对下游学习有用的图像”。

### 2. 方法谱系：诊断框架的设计逻辑

本工作并非提出一个新的 T2I 模型，而是构建了一套系统性的 **Synth→Real 诊断与基准测试框架**，用于解耦合成数据效用下降的因果维度。该框架沿三条轴线展开：

**（1）纹理-结构解耦。** 受启发于图像表示学习中纹理与形状偏好的经典讨论（Geirhos et al., ICLR 2019），该框架利用 Depth Anything V2 将 RGB 图像转换为深度图，在深度空间训练 ResNet-50，从而剥离纹理信息、仅保留全局结构（Figure 2）。同时，采用感受野仅 $9 \times 9$ 的 BagNet（Brendel & Bethge, ICLR 2019）作为纹理分类器，只捕捉局部纹理特征而无法利用全局结构。这一对偶设计使得纹理损伤与结构损伤可被独立量化。

**（2）频率分解。** 基于自然图像振幅谱近似遵循幂律分布 $S(f) \propto f^{-\alpha}$ 的先验知识（Section 3.2），框架对合成图像施加高通滤波（保留 $f \leq 0.2 \times f_N$）和低通滤波（保留 $f \geq 0.8 \times f_N$），在频域上分离高频与低频成分，以探测谱失真对下游性能的影响。

**（3）分布漂移与多样性度量。** 采用 Naeem et al. 的密度与覆盖率度量，在 CLIP-ViT-L 特征空间中量化合成数据相对于真实训练数据的分布对齐度。密度衡量合成样本是否集中在真实分布的特定区域，覆盖率衡量合成样本覆盖真实分布的程度。这一分析直接揭示了新模型“高密度、低覆盖率”的分布坍塌现象。

### 3. 与基线工作的关系

本工作评估了 13 个开源 T2I 模型作为训练数据生成器的表现，时间跨度从 2022 年至 2025 年，构成了一条天然的“生成技术进步时间线”：

| 模型 | 发布年份 | 角色 |
|------|---------|------|
| Stable Diffusion v1.5 (Rombach et al., CVPR 2022) | 2022 | 早期基线 |
| Stable Diffusion 2.1 (Rombach et al., CVPR 2022) | 2022 | 早期基线 |
| Stable Diffusion XL (Podell et al., arXiv 2023) | 2023 | 中期基线 |
| SDXL-Turbo (Podell et al., arXiv 2023) | 2023 | 蒸馏加速版 |
| Stable Diffusion 3.5 Large / Medium (Stability AI, 2024) | 2024 | 后期基线 |
| Stable Diffusion 3.5-Large-Turbo (Stability AI, 2024) | 2024 | 蒸馏加速版 |
| Sana (Esser et al., 2024) | 2024 | 后期基线 |
| Flux-Dev / Flux-Schnell (Black Forest Labs, 2024) | 2024 | 后期基线 |
| Qwen-Image (Wu et al., arXiv 2025) | 2025 | 最新基线 |
| Lumina Image 2.0 (Qin et al., arXiv 2025) | 2025 | 最新基线 |

这些模型在 GenEval 和 CLIPScore 等文本对齐基准上的得分持续提升，但本工作发现**这些基准得分与合成数据的训练效用呈负相关**（Figure 3）——在仅使用类名提示的条件下，更高的文本对齐分数对应更低的 Synth→Real 迁移准确率。这表明现有的 T2I 评估指标无法捕捉数据对下游学习的有用性。

### 4. 关键因果发现

**纹理与高频是性能差距的主要来源。** 在结构空间（深度图）中训练的分类器，其与真实数据训练的分类器之间的性能差距显著小于纹理空间（BagNet）中的差距（Figure 4, left）。同时，低频域的性能紧密跟随 RGB 域，而高频域的性能差距显著更大（Figure 4, right）。这表明合成图像的结构信息受影响较小，而**纹理和高频成分遭受了严重损害**，且详细字幕提示对纹理和高频的改善有限。

**分布坍塌是泛化下降的根本原因。** 新 T2I 模型生成的合成数据集呈现高密度、低覆盖率的特征——样本集中在真实分布的狭窄区域，缺乏类别内多样性（Figure 5）。较低的密度和较高的覆盖率与更高的 Synth→Real 迁移准确率相关。详细字幕提示虽能提升覆盖率并降低密度，但会引入额外的分布偏移。

**跨域迁移不对称性揭示了决策边界的偏离。** Real→Synth 迁移准确率高且随模型更新而上升，而 Synth→Real 迁移准确率低且持续下降（Figure 6）。这一严重不对称性说明合成数据形成了易于被真实模型分类的簇，但这些簇的决策边界与真实数据存在系统性偏差，导致合成模型在真实数据上泛化失败。

### 5. 适用边界与局限

本工作的发现和诊断框架目前受限于以下边界：

- **任务范围：** 仅验证了图像分类任务（ImageNet-1k 200 类子集），在目标检测、实例分割、人体姿态估计等更复杂的视觉任务中是否成立尚待验证。
- **模型覆盖：** 仅评估了开源 T2I 模型，专有或闭源模型（如 DALL·E 3、Midjourney）的表现未知。
- **提示策略：** 详细字幕提示虽能提升性能，但在实际缺乏原始图像的纯合成场景下不可行，且重新字幕化需要额外计算成本。
- **下游架构：** 分析聚焦于 ResNet-50，虽有 ViT-Ti、ConvNeXt-Ti 作为补充验证，但未深入探究更多架构的敏感性。
- **特征空间：** 密度与覆盖率估计受限于 CLIP-ViT-L 特征空间，其他表示空间可能揭示不同的分布特性。

### 6. 开放问题

本工作打开了若干值得进一步探索的方向：

1. **任务泛化性：** 所观察到的趋势在目标检测、实例分割等需要更丰富空间信息的视觉任务中是否依然成立？
2. **闭源模型评估：** 专有 T2I 模型（如 DALL·E 3、Midjourney）作为训练数据生成器的表现如何？其训练数据效用是否同样遵循下降趋势？
3. **多样性奖励机制：** 如何在生成阶段引入对学习有用的多样性奖励，将生成过程与下游任务学习耦合，以提升合成数据的训练效用？这可能需要重新设计 T2I 模型的训练目标或采样策略。
4. **保真度-真实性协同：** 是否存在一种能够同时提高视觉保真度和数据真实性的 T2I 模型设计或后训练策略？当前模型在追求美学质量时牺牲了数据多样性，这暗示需要新的权衡机制。



## 原文 PDF

![[paperPDFs/CVPR_2026/When_Pretty_Isn_t_Useful_Investigating_Why_Modern_Text_to_Image_Models_Fail_as_Reliable_Training_Data_Generators.pdf]]
