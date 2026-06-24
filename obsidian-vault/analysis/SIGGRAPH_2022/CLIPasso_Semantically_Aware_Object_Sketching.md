---
title: "CLIPasso: Semantically Aware Object Sketching"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/CLIPasso_Semantically_Aware_Object_Sketching.pdf
project_link: "https://clipasso.github.io/clipasso/"
code_link: null
aliases:
- CLIPasso
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
core_operator: 笔画数量 n（贝塞尔曲线笔画的多少），通过调整 n 直接控制草图的抽象程度，n 越小抽象程度越高。
primary_logic: 利用预训练 CLIP 模型的语义理解能力，通过对其最终嵌入层使用余弦距离作为语义损失、对中间层激活使用 L2 距离作为几何损失，联合优化贝塞尔曲线的控制点，使得生成的草图在保持输入图像几何结构的同时具有语义敏感性和可识别性，且无需任何草图数据集训练。
claims:
- CLIP 能同时编码图像和草图的语义信息，无需进一步训练，使得无数据集优化成为可能。
- 用户研究表明，使用 16 笔画的草图类别级识别率达到 97.9%，接近甚至有超过基于数据集方法的水平。
- 显著引导的初始化显著提升最终草图质量，尤其是在高抽象（低笔画数）场景下。
- 与纯文本驱动的 CLIPDraw 相比，所提出的几何损失项为草图提供了图像几何基础，避免了结构崩塌。
---

# CLIPasso: Semantically Aware Object Sketching

> [!tip] 核心洞察
> 利用预训练 CLIP 模型的语义理解能力，通过对其最终嵌入层使用余弦距离作为语义损失、对中间层激活使用 L2 距离作为几何损失，联合优化贝塞尔曲线的控制点，使得生成的草图在保持输入图像几何结构的同时具有语义敏感性和可识别性，且无需任何草图数据集训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | CLIPasso：语义感知的物体草图生成 |
| 英文题名 | CLIPasso: Semantically Aware Object Sketching |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://clipasso.github.io/clipasso/) · [Project](https://clipasso.github.io/clipasso/") |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation |
| Method | CLIPasso |
| Dataset | User Study, SketchyCOCO |

> [!tip] 效果简介
> - User Study (Category-Level) 上，Recognition accuracy Ours 16s 97.9% ±0.8% vs Kampelmuhler and Pinz 65% ±2% (+32.9%)。
> - User Study (Instance-Level) 上，Recognition accuracy Ours 8s 95% ±1% vs Kampelmuhler and Pinz 65% ±2% (+30%)。
> - SketchyCOCO (CLIP ViT-B/32 Top-3) 上，Accuracy Ours 32s 97% vs Li et al. 77% (+20%)。

## 概要

将照片转换为具有不同抽象层次的语义感知草图是一个挑战：传统方法依赖像素损失或边缘图，无法捕捉语义；基于配对数据集的方法则受限于数据集中固有的抽象风格。**CLIPasso** 提出一种无需草图数据集训练的新范式——将草图定义为一组贝塞尔曲线，通过可微分光栅化器直接优化曲线控制点，并利用预训练 CLIP 模型同时提供语义监督和几何监督。具体而言，语义损失使用 CLIP 最终嵌入的余弦距离，几何损失使用 CLIP 中间层激活的 L2 距离；抽象程度通过笔画数量 n 自由控制。用户研究表明，该方法在 16 笔画下类别级识别率达 **97.9%**，显著优于基于数据集的方法；在 SketchyCOCO 上 CLIP 分类准确率领先基线 **20%** 以上。该方法定位于将大规模预训练视觉-语言模型的语义理解能力引入矢量图形优化，突破了传统草图生成对配对数据和固定抽象层次的依赖。

## 核心方法与创新机理

### 问题瓶颈与核心思路

高质量抽象草图生成面临一个根本性矛盾：既要保持对输入图像的几何保真度（实例级可识别性），又要实现语义层面的抽象简化（类别级可识别性）。传统方法无法同时满足这两个要求——基于像素或边缘的方法（如 L2 损失、LPIPS）过度依赖低级图像信号，生成的草图仅相当于边缘图，缺乏语义理解；而基于配对照片-草图数据集训练的方法（如 Kampelmuhler and Pinz、Li et al.、SketchLattice 等）受限于数据集中存在的特定抽象层次和风格，无法灵活控制抽象程度，且泛化能力受数据集规模制约。

CLIPasso 的核心洞察在于：预训练的 CLIP 模型已经编码了图像和草图的共享语义空间，无需任何草图数据集进行额外训练。通过同时利用 CLIP 的最终嵌入层（语义理解）和中间层激活（几何结构），可以在优化贝塞尔曲线控制点的过程中，使生成的草图既保持输入图像的语义可识别性，又保留其几何形态。抽象程度则通过笔画数量 $n$ 这一单一参数自由控制——$n$ 越小，优化任务越困难，迫使笔画捕捉对象的本质特征，从而实现更高层次的抽象。

### 方法框架与模块顺序

CLIPasso 将草图生成形式化为一个基于 CLIP 感知损失的贝塞尔曲线参数优化问题，整体流程包含以下顺序模块：

1. **显著性引导的笔画初始化**：从输入图像中提取 CLIP ViT 的注意力图作为显著性分布，结合 XDoG 边缘图调整后，在该分布上采样 $n$ 条贝塞尔曲线的初始位置。这一初始化策略使笔画初始位置集中在语义显著区域，为后续优化提供了良好的起点。

2. **贝塞尔曲线参数化**：每条笔画定义为具有 4 个控制点的二维三次贝塞尔曲线 $s_i = \{p_i^j\}_{j=1}^4$，所有笔画放置在白色背景上。为简化优化，仅优化控制点位置，笔画的阶数、宽度和不透明度保持固定。

3. **可微分光栅化**：使用可微分光栅化器 $\mathcal{R}$ 将矢量贝塞尔曲线渲染为光栅图像，使得损失函数相对于控制点坐标的梯度可以通过反向传播计算。

4. **数据增强**：在将光栅化草图和目标图像输入 CLIP 之前，对两者施加相同的随机仿射变换（裁剪、缩放、旋转），防止优化过程产生对抗性草图。

5. **CLIP 多层特征提取**：使用预训练的 CLIP 模型（基于 ResNet101 的图像编码器）提取目标图像 $I$ 和光栅化草图的特征，包括最终嵌入向量和中间层（layer3、layer4）的激活图。

6. **双重损失计算与反向传播优化**：计算语义损失和几何损失的加权和，通过 Adam 优化器迭代更新所有控制点坐标，直至收敛。

### 核心创新机制：双重 CLIP 损失函数

CLIPasso 的核心创新在于损失函数的设计，这是区别于所有基线方法的关键 changed slot。总损失函数为：

$$\min_{\{s_i\}_{i=1}^n} L_{geometric} + w_s \cdot L_{semantic}$$

其中 $w_s = 0.1$ 用于平衡两个损失项的贡献。

**语义损失** $L_{semantic}$ 定义为目标图像与光栅化草图的 CLIP 最终嵌入向量之间的余弦距离：

$$L_{semantic} = dist\big( CLIP(I), CLIP(\mathcal{R}(\{s_i\}_{i=1}^n)) \big)$$

该损失项确保草图在 CLIP 的语义空间中与目标图像保持相似，使生成的草图具有类别级别的可识别性。消融实验（Figure 32, column $L_s$）表明，移除语义损失会导致草图过于几何化，仅保留轮廓而丢失语义特征（如动物面孔退化为空洞的边缘）。

**几何损失** $L_{geometric}$ 定义为目标图像与草图在 CLIP 中间层激活上的 L2 距离之和：

$$L_{geometric} = \sum_l \| CLIP_l(I) - CLIP_l(\mathcal{R}(\{s_i\}_{i=1}^n)) \|_2^2$$

其中 $l$ 取 ResNet101 的 layer3 和 layer4。该损失项为草图提供几何基础，保持实例级的结构保真度。消融实验（Figure 32, column $L_g$）表明，移除几何损失会导致草图结构混乱，甚至无法识别。附录中的架构消融（Figure 29）进一步证实，使用 ResNet101 的 layer3 和 layer4 作为几何损失来源，比 ResNet50 或纯 ViT 产生更稳定、兼具语义与几何的结果。

**损失函数设计的因果机制**：语义损失作用于 CLIP 的高层语义空间，引导笔画捕捉对象的本质特征（如眼睛、鼻子等语义部件）；几何损失作用于 CLIP 的中层特征空间，约束笔画的空间布局与输入图像保持一致。两者形成互补——语义损失提供“画什么”的指导，几何损失提供“在哪里画”的约束。权重 $w_s = 0.1$ 的设置（Figure 33 消融验证）确保几何损失主导优化过程，语义损失作为辅助引导，避免过高的语义权重导致几何结构过度变形。

### 抽象控制与初始化策略

**笔画数量作为抽象控制旋钮**：CLIPasso 通过改变笔画数量 $n$ 自由控制抽象层次，这是区别于数据集驱动方法的第二个关键 changed slot。$n$ 越小，优化问题的约束越强，迫使笔画以更简洁的方式捕捉对象的本质。实验显示，该方法可在 4 笔画（极高抽象）下仍产生可识别的草图，而 16 笔画下的类别级识别率达到 97.9%。

**显著性引导初始化**：随机初始化在低笔画数（高抽象）场景下极易陷入局部最优，导致草图质量显著下降。CLIPasso 提出的显著性引导初始化（第三个 changed slot）利用 CLIP ViT 的注意力图提取语义显著区域，结合 XDoG 边缘图调整后作为笔画初始位置的采样分布。Figure 8a 的对比显示，该初始化策略显著提升了最终草图质量，尤其在高抽象场景下效果更为明显。为进一步缓解初始化敏感性，方法采用 3 次不同随机种子初始化，自动选择损失最低的结果作为最终输出（Figure 8b）。

### 训练/推理路径

CLIPasso 无需任何训练阶段，直接对每张输入图像执行从零开始的优化。推理路径为：给定目标图像 $I$ 和笔画数 $n$ → 显著性引导初始化贝塞尔曲线控制点 → 可微分光栅化渲染草图 → CLIP 提取多层特征 → 计算双重损失 → Adam 优化器反向传播更新控制点 → 迭代至收敛（通常 2000 次迭代）。整个过程无需配对数据、无需网络训练，仅依赖预训练 CLIP 模型，实现了完全无数据集的草图生成范式。

![[assets/figures/papers/paper_list_l16_https_clipasso_github_io_clipasso_repair/figures/008_Figure_8.jpg]]
*Figure 8: Strokes Initialization. (a) Left to right: input, the saliency map produced from CLIP ViT activations, final distribution map (adjusted to adhere to image edges) with sampled initial stroke locations (in red), the sketch produced using the proposed initialization procedure, and the sketch produced when using random initialization. (b) Results of three different initializations with the same number of strokes. The sketches marked in blue produced the lowest loss value, and would thus be used as the final output*

![[assets/figures/papers/paper_list_l16_https_clipasso_github_io_clipasso_repair/figures/010_Figure_9.jpg]]
*Figure 9: Sketches produced by our method for infrequent categories*

## 实验与关键发现

CLIPasso 的核心实验围绕三个维度展开：**抽象层次可控性**、**语义可识别性**（用户研究与自动识别）以及**各模块的因果贡献**（消融实验）。以下按主结果、关键消融、失败模式与适用边界组织。

### 主结果：语义可识别性与抽象控制

**用户研究（Table 2）** 是衡量草图语义质量的关键证据。在类别级识别任务中，CLIPasso 使用 16 笔画（16s）达到 **97.9% ± 0.8%** 的识别率，而基于 Sketchy 数据集训练的 Kampelmuhler and Pinz 方法仅为 **65% ± 2%**，绝对提升 **+32.9%**。在实例级识别中，8 笔画（8s）即达到 **95% ± 1%**，同样远超对比方法的 65% ± 2%（+30%）。值得注意的是，笔画数降至 4 时，类别级识别率骤降至 **36% ± 3%**，这构成了当前方法的**语义可识别性断裂点**——在极端抽象下，几何与语义信息同时严重退化。

在 **SketchyCOCO 自动识别基准（Table 3）** 上，使用 CLIP ViT-B/32 的 Top-3 准确率，CLIPasso 32 笔画达到 **97%**，较 Li et al. 的 77% 提升 **+20%**；Top-1 准确率为 **77%**，较 Kampelmuhler and Pinz 的 49% 提升 **+28%**。但需注意，自动识别与用户研究存在方法学差异——自动识别依赖预训练模型，其评估偏好可能与人类感知不完全一致，因此用户研究的 97.9% 是更直接的语义质量证据。

![[assets/figures/papers/paper_list_l16_https_clipasso_github_io_clipasso_repair/figures/016_Table_3.jpg]]
*Table 3: Top-1 and Top-3 sketch recognition accuracy computed with ResNet34 and CLIP ViT-B/32 on 200 sketches from 10 categories. (A) Kampelmuhler and Pinz [ ¨ 21], (B) Li et al. [23]*

**与 CLIPDraw 的对比（Figure 13）** 揭示了几何损失的决定性作用：纯文本驱动的 CLIPDraw 仅使用语义损失，生成的 16 笔画草图虽然语义类别可辨，但**整体结构崩塌**，无法保持输入图像的实例级几何特征。CLIPasso 通过引入中间层 L2 几何损失，在保持语义的同时锚定了图像的空间结构，这是两者性能差异的因果机制。

### 关键消融：损失函数各组分的作用

消融实验（Figure 32）系统验证了损失函数各组分的因果贡献：

- **移除语义损失（L_semantic）**：草图退化为纯几何轮廓，动物面孔仅剩外轮廓线，丢失了眼睛、鼻子等语义关键特征。这表明**语义损失是草图具备类别可识别性的必要条件**。
- **移除几何损失（L_geometric）**：草图失去实例级保真度，结构混乱，甚至无法辨认原始对象。这说明**几何损失是维持图像-草图空间对应关系的必要条件**。
- **移除 layer3 或 layer2**：仅使用 layer4 作为几何损失来源时，草图过于高层语义化；加入 layer3 后获得了更稳定的几何-语义平衡。Appendix E.1（Figure 29）进一步表明，使用 **ResNet101 的 layer3 + layer4** 作为几何损失来源，优于 ResNet50 或纯 ViT，后者会产生不稳定的几何变形。

**语义损失权重消融（Figure 33）** 确定了 $w_s = 0.1$ 为最优平衡点。当 $w_s = 0$ 时草图过度几何化；$w_s = 0.5$ 或 $1.0$ 时，语义项主导导致几何结构发生过大形变，草图偏离原始图像的空间布局。

**初始化策略消融（Figure 8）** 表明，基于 CLIP ViT 显著图引导的初始化显著优于随机初始化，尤其在**低笔画数（高抽象）场景**下差异更为明显。为缓解初始化敏感性，方法采用 3 次不同种子初始化并自动选择损失最低者（Figure 8b），这一策略有效提升了输出稳定性（Appendix D, Figure 25）。

### 失败模式与适用边界

1. **背景处理缺陷**：当输入图像包含复杂背景时，高抽象层次下性能显著下降。目前依赖外部的 U2-Net 预分割模型进行预处理，但背景抑制并未集成到损失函数内部，导致分割错误会直接传播到草图生成。这是方法从“物体草图”扩展到“场景草图”的核心障碍。

2. **笔画数需人工预设**：抽象层次通过笔画数 $n$ 控制，但不同复杂度的对象需要不同数量的笔画才能达到相似的抽象效果。例如，简单几何体用 8 笔画可能已足够，而复杂动物可能需要 16 笔画才能保持可识别性。目前尚未实现**自适应笔画数学习**。

3. **非顺序生成过程**：所有笔画同时被优化，而非逐笔顺序生成。这与人类手绘草图的自然过程不符，限制了方法在交互式草图生成场景中的应用。

4. **极端抽象下的性能断裂**：4 笔画时类别级识别率仅 36%，表明当前方法在极低笔画数下无法维持语义可识别性。这是 CLIP 嵌入空间在高维语义压缩下的固有限制，还是优化过程的局部极小值问题，尚需进一步验证。

5. **与基于数据集方法的对比公平性**：Table 1 的系统对比表明，CLIPasso 在“不受训练类别限制”“可产生不同抽象层次”“不受数据集抽象风格限制”“可生成矢量草图”四个维度上具有优势，但“可顺序生成”维度不满足。这些优势的代价是每张图像需独立优化（约数分钟），而基于学习的方法可实时推理。

![[assets/figures/papers/paper_list_l16_https_clipasso_github_io_clipasso_repair/figures/005_Table_1.jpg]]
*Table 1: Comparison of sketch synthesis algorithms. (A) Is not restricted to categories from training dataset, (B) Can produce different levels of abstractions, (C) Is not limited to abstractions in the dataset, (D) Can produce vector sketches, (E) Can produce a sequential sketch (F) Is not directly relying on the edge map*

**适用边界总结**：CLIPasso 最适合**前景分割良好的单物体照片**，在 8-32 笔画范围内可生成兼具几何保真度和语义可识别性的抽象草图；对于包含背景的场景图像或需要极端抽象（≤4 笔画）的任务，性能明显下降。

![[assets/figures/papers/paper_list_l16_https_clipasso_github_io_clipasso_repair/figures/014_Figure_13.jpg]]
*Figure 13: Comparison to CLIPDraw [11]. All sketches were produced using 16 strokes*

![[assets/figures/papers/paper_list_l16_https_clipasso_github_io_clipasso_repair/figures/015_Table_2.jpg]]
*Table 2: User study results – average recognition rates. (A) Kampelmuhler and Pinz [ ¨ 21], (B) Li et al. [23]*

## 定位与知识库关联

CLIPasso 的核心定位是**无数据集训练的语义感知物体草图生成**，其相对于现有工作的本质差异在于改变了四个关键 slot：

1. **损失函数 slot**：从传统的 L2 像素损失或 LPIPS 感知损失，替换为 **CLIP 语义损失 + CLIP 几何损失的组合**。这是最根本的改变——传统方法（如 Kampelmuhler and Pinz 的 Sketchy 分类器引导方法、Li et al. 2019/2020 的变形笔画模型）依赖像素级或边缘级监督，无法捕捉语义级别的抽象；CLIPDraw 虽使用 CLIP，但仅有文本驱动的语义损失，缺乏几何锚定。CLIPasso 通过同时使用 CLIP 最终嵌入的余弦距离（语义）和中间层激活的 L2 距离（几何），实现了语义可识别性与几何保真度的统一。

2. **抽象控制 slot**：从“受限于训练数据集的抽象层次”改为**通过笔画数量 n 自由控制抽象程度**。现有基于数据集的方法（如 SketchLattice 的 LSTM-图模型、Song et al. 的混合监督学习、Berger et al. 的面部肖像抽象）只能产生数据集中存在的抽象风格和层次，而 CLIPasso 通过调节贝塞尔曲线笔画数 n，可在同一框架下连续地从写实到高度抽象（如 4 笔画）进行生成，无需重新训练。

3. **笔画初始化 slot**：从随机初始化改为**基于 CLIP ViT 显著图和 XDoG 边缘图的采样初始化**。这一改变在高抽象（低笔画数）场景下尤为关键——随机初始化容易陷入局部最优，导致结构崩塌，而显著引导初始化使笔画初始位置集中在语义重要区域，显著提升最终草图质量。

4. **训练数据需求 slot**：从“依赖配对照片-草图数据集”改为**完全无需草图数据集训练**，仅使用预训练 CLIP 模型。这使方法不受数据集类别、风格、抽象层次的限制，可泛化到任意物体类别（如 Figure 9 中的稀有类别）。

### 知识库挂载点

CLIPasso 在知识库中的挂载点位于**视觉-语言预训练模型的下游应用**分支，具体连接路径为：

- **上游依赖**：CLIP（Radford et al., ICML 2021）——作为冻结的特征提取器，提供语义嵌入空间和中间层几何表征。CLIPasso 不修改 CLIP 参数，仅将其作为损失函数的计算基础。
- **并行关联**：CLIPDraw（Frans et al., 2021）——同属 CLIP-based 优化生成范式，但 CLIPDraw 是纯文本驱动的矢量图生成，无图像几何约束。CLIPasso 可视为 CLIPDraw 在图像-草图转换场景下的几何增强版本。
- **下游延伸**：可微分渲染 + 矢量图形优化——使用可微分光栅化器（如 DiffVG）将贝塞尔曲线渲染为光栅图像，使梯度可回传至控制点坐标。这一技术栈与后续的矢量图形生成工作（如 LIVE、DiffSketcher）共享基础。

### 适用边界

- **输入要求**：需要前景分割后的物体图像。论文通过外部分割模型（U2-Net）进行预处理，但分割质量直接影响草图质量——包含背景的图像在高抽象层次下性能显著下降。
- **笔画数量限制**：实验显示 4 笔画是当前方法的“断裂点”——类别级识别率骤降至 36%±3%，表明极端抽象下语义保持能力有限。
- **生成范式限制**：所有笔画同时优化，非顺序生成，与传统手绘过程不同。这限制了方法在模拟人类绘画过程、交互式草图生成等场景的适用性。
- **风格多样性**：虽可通过改变笔画阶数和笔刷风格实现有限风格变化，但核心风格受限于“黑色贝塞尔曲线 + 白色背景”的表示形式，无法生成灰度或彩色草图。

### 后续启发

CLIPasso 揭示了一个关键洞察：**预训练视觉-语言模型的中间层激活天然编码了几何结构信息**，这为无监督几何约束提供了新范式。直接启发的工作方向包括：

1. **自适应笔画数学习**：当前笔画数需人工指定，不同复杂度物体需要不同 n 以达到相似抽象效果。将 n 作为可学习参数或基于图像复杂度自动预测，是直接改进方向。
2. **背景感知损失函数**：将背景处理集成到损失函数内部（而非依赖外部分割），可消除预处理依赖，提升含背景图像的鲁棒性。
3. **顺序生成过程**：引入自回归或强化学习机制使笔画顺序生成，可更接近人类绘画过程，并可能提升极端抽象下的结构保持能力。
4. **多模态扩展**：CLIPasso 的损失函数框架可扩展到文本引导的草图生成、草图编辑、风格迁移等多模态任务，仅需调整 CLIP 嵌入的对比目标。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/CLIPasso_Semantically_Aware_Object_Sketching.pdf]]