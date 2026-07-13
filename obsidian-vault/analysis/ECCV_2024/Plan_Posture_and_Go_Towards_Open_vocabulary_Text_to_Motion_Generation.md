---
title: Plan Posture and Go Towards Open vocabulary Text to Motion Generation
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Plan_Posture_and_Go_Towards_Open_vocabulary_Text_to_Motion_Generation.pdf
project_link: https://moonsliu.github.io/Pro-Motion/
code_link: null
aliases:
- PM
- PPGTOVTMG
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用大型语言模型（LLM）将开放世界自然语言描述分解为结构化的姿势脚本，从而将复杂任务分解为可控的子模块：姿势生成和运动重建。
primary_logic: 通过“计划（Plan）-姿态（Posture）-行进（Go）”三阶段框架，将开放世界文本到动作生成转化为：首先用LLM规划关键姿势描述，然后用扩散模型从描述生成姿态，最后利用另一个扩散模型推断全局运动并插值，实现从任意文本生成流畅、多样且具有全局运动的人体动作。
claims:
- PRO-Motion采用分而治之的框架，包括motion planner、posture-diffuser和go-diffuser三个模块。
- Motion planner使用LLM生成描述关键姿势的脚本，从而弥合自然语言和姿势描述之间的差距。
- Posture-diffuser能够从结构化的脚本生成精确的姿势，并支持通过编辑描述实现细粒度控制。
- Go-diffuser能够从关键姿势序列估计全身平移和旋转，并实现平滑的姿势插值。
---

# Plan Posture and Go Towards Open vocabulary Text to Motion Generation

> [!tip] 核心洞察
> 通过“计划（Plan）-姿态（Posture）-行进（Go）”三阶段框架，将开放世界文本到动作生成转化为：首先用LLM规划关键姿势描述，然后用扩散模型从描述生成姿态，最后利用另一个扩散模型推断全局运动并插值，实现从任意文本生成流畅、多样且具有全局运动的人体动作。

| 字段 | 内容 |
|------|------|
| 中文题名 | 计划、姿态与行进：面向开放词汇的文本到动作生成 |
| 英文题名 | Plan Posture and Go Towards Open vocabulary Text to Motion Generation |
| 会议/期刊 | ECCV 2024 |
| Links | [Project](https://moonsliu.github.io/Pro-Motion/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PRO-Motion |
| Dataset | ood368, kungfu, AMASS |

> [!tip] 效果简介
> - ood368 (IDEA-400 subset) 上，R@10 20.25 vs 17.81 (MDM) (+2.44)。
> - ood368 上，FID 1.488678 vs 3.500541 (MDM) (-2.011863)；MultiModal Dist 1.534521 vs 2.613644 (MDM) (-1.079123)。
> - kungfu (Motion-X subset) 上，R@10 20.31 vs 12.50 (MDM) (+7.81)。

## 概要

现有文本到动作生成方法面临一个根本瓶颈：配对训练数据的规模与覆盖范围极其有限，难以泛化到开放世界中的任意自然语言描述。基于CLIP空间对齐的方法虽然绕开了对文本-动作对的要求，却缺乏时序先验，无法生成具有合理时间顺序和全局运动的动作序列。针对这一瓶颈，PRO-Motion提出了一种“分而治之”的生成范式，将开放世界文本到动作生成这一复杂任务分解为三个可控的子模块：**Motion Planner**利用大型语言模型将自然语言描述分解为结构化的关键姿势脚本；**Posture-Diffuser**基于扩散模型将脚本转换为精确的人体姿态；**Go-Diffuser**则从关键姿态序列推断全身平移与旋转，并插值生成流畅完整的动作。这一“计划（Plan）—姿态（Posture）—行进（Go）”框架的核心洞察在于：通过引入LLM作为语义规划器，将开放文本到动作的映射问题转化为“文本→结构化姿势描述→姿势序列→完整运动”的级联生成过程，从而在无需大规模配对数据的条件下实现多样、可控且具有全局运动的人体动作生成。

在方法定位上，PRO-Motion区别于以**MDM**（Tevet et al., arXiv 2022）为代表的监督学习扩散模型和以**MotionCLIP**（Tevet et al., ECCV 2022）为代表的CLIP对齐方法。前者受限于训练数据分布，后者缺乏时序建模能力。PRO-Motion则通过LLM规划与双扩散模型的组合，将文本条件从原始自然语言提升为结构化的身体部位描述，并在姿态生成与运动重建两个阶段分别建模，从而在开放词汇场景下取得显著优势。

实验结果表明，在开放世界数据集ood368和kungfu上，PRO-Motion在R精度（R@10: 20.25 vs. MDM的17.81）和FID（1.49 vs. MDM的3.50）等核心指标上显著优于监督学习和现有开放词汇方法。在AMASS数据集上，Go-Diffuser对全局平移和旋转的预测精度（平均位置误差0.418，平均方差误差0.118）也达到了最优水平。消融实验进一步验证了LLM生成的局部身体部位描述对姿态精确性的关键作用，以及Transformer架构在全局运动推断中的必要性。

### 文本到动作生成的核心瓶颈

3D人体动作生成旨在根据自然语言描述合成逼真的人体运动序列。现有主流方法大多采用监督学习范式，直接在配对的文本-动作数据上训练生成模型（如 **MDM**，Tevet et al., arXiv 2022），试图建立从文本到动作空间的直接映射。这一范式面临根本性瓶颈：配对训练数据的规模和语义覆盖范围严重受限。现实世界中的人类动作语义极其丰富，从具体的物理动作（如“单脚跳跃”）到抽象的情感表达（如“体验深沉的喜悦”），而现有文本-动作数据集（如HumanML3D、KIT-ML）的动作类别和语言描述多样性远不足以覆盖开放世界场景。

此外，部分工作尝试利用CLIP的跨模态对齐能力实现开放词汇动作生成，例如 **MotionCLIP**（Tevet et al., ECCV 2022）和 **AvatarCLIP**（Hong et al., CVPR 2022）。这类方法将3D姿态渲染为图像，通过CLIP的图像空间间接对齐文本与姿态，从而绕开对配对文本-动作数据的依赖。然而，CLIP空间本身缺乏时序先验——它擅长捕获单帧的语义相似性，却无法建模动作序列中关键的时间顺序和因果关联。这导致生成的动作往往缺乏合理的时间结构和连贯的全局运动（如身体的整体平移与旋转），在复杂描述下容易出现时序错乱或运动不自然的问题。

### 现有方法的缺口

总结而言，当前文本到动作生成领域存在两个相互关联的缺口：

1. **监督学习方法的泛化瓶颈**：受限于训练数据的规模和分布，难以泛化到训练集之外的新颖动作描述。
2. **CLIP方法的时序缺失**：虽然具备开放词汇能力，但缺乏对动作时序结构和全局运动的有效建模，生成质量难以保证。

这两个缺口共同指向一个核心矛盾：如何在不依赖大规模配对数据的条件下，生成既语义准确又时序合理、且具备全局运动的人体动作序列。

### 本文动机与核心思路

针对上述瓶颈，PRO-Motion提出了一种“分而治之”（divide-and-conquer）的解决策略。其核心洞察在于：开放世界文本到动作生成可以被分解为三个更可控的子问题——

- **计划（Plan）**：利用大型语言模型（LLM）将开放世界自然语言描述分解为结构化的姿势脚本，弥合自然语言与精确姿态描述之间的语义鸿沟。
- **姿态（Posture）**：从结构化的姿势描述生成精确的3D人体姿态，并支持通过编辑描述实现细粒度控制。
- **行进（Go）**：从关键姿势序列推断全身平移和旋转，并通过插值生成流畅完整的动作序列。

这一“Plan-Posture-Go”三阶段框架将复杂的开放世界动作生成任务转化为LLM规划、姿态扩散生成和运动扩散重建的级联，从根本上规避了对大规模配对文本-动作数据的依赖，同时通过显式的时序建模（关键姿势序列规划与全局运动推断）弥补了CLIP方法的时序缺失。

## 核心方法与创新机理

PRO-Motion的核心创新在于将开放世界文本到动作生成这一复杂问题，通过“计划-姿态-行进”三阶段框架进行结构化分解，从而绕开了传统方法对大规模配对文本-动作数据的依赖。其关键洞察是：**开放世界自然语言描述的复杂性可以通过大型语言模型的先验知识进行结构化降维，将动作生成转化为可控的姿态生成与运动重建两个子问题**。

### 1. 文本到动作生成策略的根本转变

传统方法（如 **MDM** (Tevet et al., arXiv 2022)）直接在文本-动作对上训练生成模型，其泛化能力受限于配对数据的规模和覆盖范围。基于CLIP的开放词汇方法（如 **MotionCLIP** (Tevet et al., ECCV 2022)、**AvatarCLIP** (Hong et al., CVPR 2022)）虽然摆脱了文本-动作配对限制，但CLIP空间缺乏时序先验，无法生成具有合理时间顺序和全局运动的动作序列。

PRO-Motion的策略转变体现在三个层面：
- **从“文本→动作”到“文本→姿势脚本→姿态→动作”**：利用LLM将开放世界自然语言分解为结构化的关键姿势描述脚本，将非结构化的语义理解与结构化的姿态生成解耦。
- **从“局部姿态生成”到“全局运动重建”**：大多数现有方法仅生成局部关节旋转，缺乏全身平移和旋转。PRO-Motion通过Go-Diffuser从关键姿态序列中推断完整的全局运动。
- **从“隐式文本条件”到“显式结构化条件”**：使用Distill-BERT编码的结构化姿势脚本作为扩散模型的条件，替代CLIP嵌入匹配或直接文本条件，实现了更精确的可控生成。

### 2. 三阶段分而治之框架

PRO-Motion由三个功能明确的模块构成，每个模块解决一个子问题：

**Motion Planner（运动规划器）**：利用GPT-3.5根据用户提示生成一系列描述关键姿势的脚本。通过五条基本规则（如描述身体部位的弯曲程度、判断是否接触地面等）引导LLM输出结构化的姿势描述，弥合自然语言和精确姿势描述之间的语义鸿沟。

**Posture-Diffuser（姿态扩散器）**：一个条件扩散模型，将离散的姿势脚本转换为具体的人体姿态。其架构由N个相同层堆叠而成，每层包含一个残差块（融入时间步信息）和一个交叉模态Transformer块（融合Distill-BERT编码的文本条件）。随后通过Viterbi算法进行**姿态规划**，在候选姿态库中选择时序连贯且与文本语义对齐的关键姿态序列。

**Go-Diffuser（行进扩散器）**：一个Transformer扩散模型，将关键姿态视为独立token，通过注意力机制建模关键姿态与噪声化运动序列之间的关系。该模块从离散关键姿态插值生成完整动作序列，同时推断全身平移和旋转，实现具有全局运动的流畅动作。

### 3. 精确姿态控制能力

PRO-Motion的另一个关键创新在于其对生成姿态的细粒度可解释控制。由于Posture-Diffuser直接以结构化的身体部位描述为条件，用户可以通过编辑姿势描述来精确控制特定身体部位的动作。实验表明，修改手部位置描述或删除特定身体部位的描述，会导致生成姿态中对应部位发生预期的变化，验证了模型对文本输入的可解释性和可控性。这一特性在传统端到端文本-动作生成模型中难以实现。

PRO-Motion 采用“计划—姿态—行进”三阶段分而治之框架，将开放世界文本到动作生成拆解为三个可控子模块：**Motion Planner**、**Posture-Diffuser** 和 **Go-Diffuser**（Figure 3）。这一设计的核心洞察在于：现有方法受限于配对训练数据的规模和覆盖范围，而基于 CLIP 的方法又缺乏时序先验，难以生成具有合理时间顺序和全局运动的人体动作序列。PRO-Motion 通过引入大型语言模型作为运动规划器，在自然语言与结构化姿态描述之间架起桥梁，使下游的扩散模型能够专注于各自擅长的子任务。

![[assets/figures/papers/paper_list_l1878_Plan_Posture_and_Go_Towards_Open_vocabulary_Text_to_Motion_Generation/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of our framework for open-world text-to-motion generation from language. Specifically, we employ the large language models as the motion planner to plan pose scripts. Then, our Posture-Diffuser module receives discrete pose descriptions and generates corresponding poses to construct a candidate posture base. Posture Planning is utilized to select the reasonable pose sequence from the candidate posture base. Finally, the Go-Diffuser module increases the motion frames and infers the translation and rotation*

### 模块职责与数据流

**Motion Planner** 是整个流水线的入口。它接收开放世界的自然语言提示，利用 GPT-3.5 将动作描述分解为一系列结构化的关键姿态脚本。为引导 LLM 生成精确且可执行的姿态描述，系统设定了五条基本规则：(1) 描述身体部位的弯曲程度；(2) 描述身体部位的空间位置关系；(3) 描述身体部位的方向；(4) 描述左右对称性；(5) 识别身体部位是否与地面接触。这些规则将模糊的自然语言转化为 Posture-Diffuser 可理解的结构化输入，弥合了文本语义与姿态空间之间的鸿沟。

**Posture-Diffuser** 接收 Motion Planner 生成的离散姿态描述脚本，为每一帧关键姿态生成对应的候选人体姿态。该模块是一个去噪扩散模型，由 N 个相同层堆叠而成，每层包含一个残差块（用于融入时间步信息）和一个跨模态 Transformer 块（用于融合文本条件）。文本条件使用冻结的 Distill-BERT 编码器提取嵌入，作为交叉注意力中的 Key 和 Value。生成候选姿态后，系统通过 **Posture Planning** 子模块，利用 Viterbi 算法在候选姿态之间选择一条时序连贯且与文本语义对齐的最优姿态序列——转移概率基于相邻帧姿态的相似度，发射概率基于姿态与对应文本描述的匹配度。

**Go-Diffuser** 是流水线的最后一环，也是一个基于 Transformer 的扩散模型。它接收 Posture Planning 选出的关键姿态序列（这些姿态仅包含局部关节旋转，不含全局平移和旋转信息），将其视为独立的 Token，并通过注意力机制在关键姿态 Token 与加噪运动序列之间进行独立交互。该模块同时完成两个任务：在关键帧之间插值生成完整的运动帧序列，以及从姿态序列中推断全身的平移和旋转，从而生成具有全局运动的人体动作。

### 与已有范式的对比

Figure 2 清晰展示了 PRO-Motion 与两类主流范式的本质区别：(a) 大多数现有方法直接在文本-动作对上训练生成模型，受限于数据规模；(b) 部分方法将 3D 姿态渲染为图像，利用 CLIP 的图像空间对齐文本与姿态，但缺乏时序建模能力。PRO-Motion 则先将动作描述分解为结构化姿态描述，再分别生成姿态并重建局部与全局维度的运动，实现了从“端到端黑箱”到“可解释分步生成”的范式转变。

![[assets/figures/papers/paper_list_l1878_Plan_Posture_and_Go_Towards_Open_vocabulary_Text_to_Motion_Generation/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of different paradigms for text-to-motion generation. (a) Most existing models leverage the generative models [22, 33, 41] to construct the relationship between text and motion based on text-motion pairs. (b) Some methods render 3D poses to images and employ the image space of CLIP to align text with poses. Then they reconstruct the motion in the local dimension based on the poses. (c) Conversely, we decompose motion descriptions into structured pose descriptions. Then we generate poses based on corresponding pose descriptions. Finally, we reconstruct the motion in local and global dimensions. “Gen.”, “Decomp.”, “Desc.”, “Rec.” stand for “Generative model”, “Decompose”, “Pose Des...*

### 关键公式

框架底层依赖去噪扩散概率模型（DDPM），其前向过程为：

$$q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t I)$$

训练目标为直接预测原始样本 $x_0$：

$$\min_{\theta} \mathcal{L} = \mathbb{E}_{x_0, t, c} \left[ \| x_0 - f_{\theta}(x_t, t, c) \|_2^2 \right]$$

推理时采用无分类器引导，通过引导系数 $w$ 平衡多样性与保真度：

$$f_{\theta}^w(x_t, t, c) = f_{\theta}(x_t, t, \emptyset) + w \cdot (f_{\theta}(x_t, t, c) - f_{\theta}(x_t, t, \emptyset))$$

Posture Planning 中的转移概率矩阵和发射概率矩阵分别定义为：

$$A_{jk}^{i} = \frac{\exp\left(\Theta(p_j^{i-1})^T \Theta(p_k^i)\right)}{\sum_{l=1}^L \exp\left(\Theta(p_j^{i-1})^T \Theta(p_l^i)\right)}$$

$$E_j^i = \frac{\exp\left(\Phi(t_i)^T \Theta(p_j^i)\right)}{\sum_{l=1}^L \exp\left(\Phi(t_i)^T \Theta(p_l^i)\right)}$$

Viterbi 算法的目标是最大化联合概率：

$$\underset{G}{\arg\max} P(G) = \prod_{i=1}^F P(g_i | g_{i-1}) = E_{g_1}^1 \prod_{i=2}^F E_{g_i}^i A_{g_{i-1}g_i}^i$$

### 框架的局限与待验证问题

多阶段流水线存在误差累积的风险——Motion Planner 的描述偏差会传播至 Posture-Diffuser，进而影响 Go-Diffuser 的生成质量。此外，系统依赖 GPT-3.5 进行运动规划，推理成本较高，且受限于 LLM 的知识范围。Motion Planner 如何处理模糊或矛盾的自然语言提示，以及在更大规模、更多样化的开放世界基准上的泛化性能，仍需进一步验证。

PRO-Motion 采用“计划—姿态—行进”三阶段分而治之框架，将开放世界文本到动作生成分解为三个可独立优化的子模块：**Motion Planner**、**Posture-Diffuser** 和 **Go-Diffuser**。框架整体流程如 Figure 3 所示。

### Motion Planner：结构化姿势脚本生成

Motion Planner 利用大型语言模型（GPT-3.5）将自然语言动作描述转化为一系列结构化的关键姿势脚本。其核心设计在于五条引导规则，约束 LLM 对每个关键姿势的描述粒度：(1) 刻画身体部位的弯曲程度；(2) 描述身体部位的空间位置；(3) 指明身体部位相对于身体中心的方向；(4) 说明身体部位之间的相对位置关系；(5) 识别身体部位是否接触地面（Sec. 3.2）。通过这套规则，LLM 输出的姿势脚本弥合了自然语言与精确姿势描述之间的语义鸿沟，为下游姿势生成提供了可操作的结构化条件。

### Posture-Diffuser：从脚本到姿态的扩散生成

Posture-Diffuser 是一个去噪扩散模型，负责将 Motion Planner 输出的姿势脚本转化为具体的人体姿态。其架构由 $N$ 个相同层堆叠而成，每层包含两个子模块（Figure 4a）：

- **残差块**：融入时间步信息，处理扩散过程中的噪声水平；
- **跨模态 Transformer 块**：以冻结的 Distill-BERT 编码的文本嵌入作为 Key 和 Value，通过交叉注意力机制将姿势描述条件注入姿态生成过程。

训练采用直接预测原始样本 $x_0$ 的简化目标：
$$
\min_{\theta} \mathcal{L} = \mathbb{E}_{x_0, t, c} \left[ \| x_0 - f_{\theta}(x_t, t, c) \|_2^2 \right] \tag{2}
$$
其中 $x_t$ 为加噪后的姿态，$t$ 为扩散时间步，$c$ 为文本条件。前向扩散过程遵循标准 DDPM 公式：
$$
q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t I) \tag{1}
$$
采样时采用无分类器引导，通过引导系数 $w$ 平衡生成多样性与条件保真度：
$$
f_{\theta}^w(x_t, t, c) = f_{\theta}(x_t, t, \emptyset) + w \cdot (f_{\theta}(x_t, t, c) - f_{\theta}(x_t, t, \emptyset)) \tag{3}
$$
姿势扩散模型使用线性噪声调度，参数设置为 $\beta_{start}=0.00085$，$\beta_{end}=0.012$（Appendix D）。

#### 姿态规划：Viterbi 序列选择

Posture-Diffuser 为每个关键帧生成多个候选姿态后，需要通过姿态规划选出时序连贯且语义对齐的最优序列。该问题被形式化为隐马尔可夫模型，通过 Viterbi 算法求解。

**转移概率矩阵** $A_{jk}^i$ 衡量从第 $i-1$ 帧候选姿态 $j$ 转移到第 $i$ 帧候选姿态 $k$ 的概率，基于姿态嵌入的余弦相似度：
$$
A_{jk}^{i} = \frac{\exp\left(\Theta(p_j^{i-1})^T \Theta(p_k^i)\right)}{\sum_{l=1}^L \exp\left(\Theta(p_j^{i-1})^T \Theta(p_l^i)\right)} \tag{4}
$$
其中 $\Theta(\cdot)$ 为姿态编码器。

**发射概率矩阵** $E_j^i$ 衡量第 $i$ 帧候选姿态 $j$ 与对应文本描述 $t_i$ 的匹配程度：
$$
E_j^i = \frac{\exp\left(\Phi(t_i)^T \Theta(p_j^i)\right)}{\sum_{l=1}^L \exp\left(\Phi(t_i)^T \Theta(p_l^i)\right)} \tag{5}
$$
其中 $\Phi(\cdot)$ 为文本编码器。

Viterbi 算法通过最大化联合概率来寻找最优姿态路径 $G$：
$$
\underset{G}{\arg\max}\ P(G) = \prod_{i=1}^F P(g_i | g_{i-1}) = E_{g_1}^1 \prod_{i=2}^F E_{g_i}^i A_{g_{i-1}g_i}^i \tag{6}
$$

### Go-Diffuser：全局运动推断与姿态插值

Go-Diffuser 是另一个基于 Transformer 的扩散模型，负责从关键姿态序列生成完整动作序列，同时推断全身平移和旋转（Figure 4b）。其核心设计在于将关键姿态视为独立 Token，与加噪动作序列之间执行独立的交叉注意力操作，从而增强模型对每个条件姿态与完整运动序列之间关联的感知能力。这一设计使 Go-Diffuser 能够捕捉关键姿态之间的内在联系，生成平滑的中间帧插值，并预测根关节的全局轨迹。

### 评估公式

为评估全局运动预测精度，论文定义了以下指标（Appendix E）：

**平均位置误差 (APE)** 衡量生成关节位置与真实值之间的平均 L2 距离：
$$
APE[j] = \frac{1}{NF} \sum_{n \in N} \sum_{f \in F} \left\| \boldsymbol{H}_f[j] - \hat{\boldsymbol{H}}_f[j] \right\|_2 \tag{7}
$$

**平均方差误差 (AVE)** 衡量生成运动方差与真实方差之间的平均 L2 距离，用于评估运动自然度：
$$
AVE[j] = \frac{1}{N} \sum_{n \in N} \left\| \delta[j] - \hat{\delta}[j] \right\|_2 \tag{8}
$$
其中关节方差定义为：
$$
\delta[j] = \frac{1}{F-1} \sum_{f \in F} \left( H_f[j] - \tilde{H}_f[j] \right)^2 \in \mathbb{R}^3 \tag{9}
$$

## 实验与关键发现

### 主要结果：开放世界文本到动作生成

PRO-Motion 在两个开放世界基准上展现出显著优于监督学习和现有开放词汇方法的性能，核心优势体现在文本-动作语义一致性与运动质量两个维度。

**ood368 基准（IDEA-400 子集）**：如 Table 1 所示，PRO-Motion 在 R@10 精度上达到 20.25，相较监督学习扩散模型 **MDM**（Tevet et al., arXiv 2022）的 17.81 提升 2.44 个点；在 FID 指标上，PRO-Motion 取得 1.488678，较 MDM 的 3.500541 降低 2.01，表明生成运动的分布更接近真实数据；MultiModal Dist 从 2.613644 降至 1.534521，降幅达 1.08，验证了生成动作与文本描述之间更强的跨模态对齐。与开放词汇方法 **MotionCLIP**（Tevet et al., ECCV 2022）、**AvatarCLIP**（Hong et al., CVPR 2022）和 **OOHMG**（Huang et al., CVPR 2023）相比，PRO-Motion 在所有三项指标上均保持领先。

**kungfu 基准（Motion-X 子集）**：该数据集包含更具挑战性的武术动作描述，PRO-Motion 的优势进一步放大。R@10 从 MDM 的 12.50 跃升至 20.31（+7.81），FID 从 12.060187 大幅降至 4.124218（-7.94），MultiModal Dist 从 3.740486 降至 2.689832。这一结果表明，PRO-Motion 的“计划-姿态-行进”框架在处理复杂、非日常动作描述时，其分而治之的策略具有更强的泛化能力，而端到端监督模型受限于训练数据分布，难以覆盖此类开放词汇。

**全局运动预测精度**：Table 2 报告了在 AMASS 数据集上的全局运动评估。PRO-Motion 在 Mean Global 指标上取得 Average Positional Error 0.418265 和 Average Variance Error 0.118334，均优于 **TEMOS**（Baseline[62]，Petrovich et al., ECCV 2022）的 0.469322 和 0.126049。值得注意的是，在仅考虑根关节平移和旋转的 Root Joint 指标上，PRO-Motion 的 APE 为 0.344176（基线 0.394379），AVE 为 0.103329（基线 0.112569），证明 Go-Diffuser 能够从无全局信息的关键姿态序列中有效推断出合理的全身平移和旋转。

### 消融实验与关键设计验证

**文本到姿态生成的精确性**：Figure 6 对比了不同文本到姿态生成方法的效果。使用 CLIP 直接匹配的方法往往产生语义模糊的姿态，而 PRO-Motion 的 Posture-Diffuser 通过 LLM 生成的局部身体部位描述作为条件，能够生成更精确的姿态。例如，对于“弯腰”动作，CLIP 方法可能仅捕捉到躯干前倾的模糊概念，而 PRO-Motion 能够准确控制脊柱弯曲程度、手臂位置等细粒度属性。这一优势源于 Posture-Diffuser 训练时使用的 PoseScript 数据集提供了结构化的身体部位描述，使模型学习到文本与具体关节角度之间的可解释映射。

**全局运动预测的架构选择**：Figure 7 和 Table 2 揭示了 Go-Diffuser 中 Transformer 架构的关键作用。相比于 MLP 和特征串联基线，Transformer 能够更好地捕捉关键姿态之间的长程依赖关系，从而准确预测平移和旋转。Figure 7 中红色标注的区域显示，基线方法在膝盖弯曲等细节处存在明显偏差，而 PRO-Motion 能够保持这些运动学细节的准确性。这一现象可归因于 Transformer 的自注意力机制允许每个关键姿态作为独立 token 与所有噪声运动帧进行交叉注意力交互，显著增强了对条件姿态的感知能力。

**细粒度姿态控制的可解释性**：Figure 8 展示了通过编辑姿态描述实现的精确控制能力。在示例 #1 中，修改手部描述（如从“双手下垂”改为“双手举起”）能精确改变生成姿态中手臂的位置；在示例 #2 中，删除特定身体部位的描述会导致该部位姿态发生随机变化，验证了 Posture-Diffuser 对文本条件的因果依赖，而非统计相关性。这一特性为交互式动作编辑提供了可解释的接口。

### 失败模式与局限性

尽管 PRO-Motion 在开放世界场景中表现优异，其多阶段流水线引入了几类潜在失败模式：

1. **运动规划器的语义偏差**：Motion Planner 依赖 GPT-3.5 将自然语言分解为姿势脚本，当输入描述模糊或矛盾时（如“既快又慢地行走”），LLM 可能生成不连贯的姿势序列，导致后续模块无法纠正。当前实验未系统评估此类边缘情况。

2. **误差累积效应**：Posture-Diffuser 生成的姿态存在微小偏差，这些偏差在 Posture Planning 的 Viterbi 选择过程中可能被放大，进而影响 Go-Diffuser 的插值和平移预测。Figure 5 的定性比较中，部分复杂描述（如“bury one's head and cry, and finally crouched down”）的生成结果在时序过渡处仍存在不自然的抖动，提示误差累积问题。

3. **极端动作的泛化边界**：Go-Diffuser 的训练数据规模较小，对于训练分布外的极端动作（如空翻、地面翻滚），预测的平移和旋转可能出现物理不合理的情况。Table 2 中 Mean Global 的 AVE 改善幅度（-0.0077）远小于 APE 改善幅度（-0.051），暗示模型在运动方差（即自然度）方面的提升相对有限。

![[assets/figures/papers/paper_list_l1878_Plan_Posture_and_Go_Towards_Open_vocabulary_Text_to_Motion_Generation/figures/007_Table_2.jpg]]
*Table 2: Comparison of our method with baseline methods on AMASS[52] dataset. We achieve state-of-the-art performance on Average Positional Error and Average Variance Error. Root joint, global traj. and mean local metrics represent the performance of translation and rotation. Mean global represents the performance of body joints and global translation*

4. **评估指标的适用性**：R 精度和 FID 等指标最初设计用于封闭世界评估，其在开放世界场景下对语义细微差别的敏感性尚未充分验证。例如，两个语义相似但运动风格不同的生成结果可能在指标上表现相近，但用户体验差异显著。

### 图表核心结论

| 图表 | 核心结论 |
|------|----------|
| **Table 1** | PRO-Motion 在 ood368 和 kungfu 两个开放世界基准上全面超越监督学习基线 MDM 和开放词汇方法，尤其在复杂动作数据集 kungfu 上优势显著（R@10 +7.81，FID -7.94） |
| **Table 2** | Go-Diffuser 的 Transformer 架构有效预测全局平移和旋转，在 Mean Global APE 上达到 0.418，优于基线 0.469 |
| **Figure 5** | 定性比较显示 PRO-Motion 在时序合理性上优于 MotionCLIP 等方法，但复杂长描述仍存在过渡不自然问题 |
| **Figure 6** | LLM 生成的局部身体部位描述使 Posture-Diffuser 的文本-姿态映射精度优于 CLIP 匹配方法 |
| **Figure 7** | Transformer 架构对捕捉关键姿态间的长程依赖至关重要，MLP 基线在膝盖弯曲等细节处存在明显偏差 |
| **Figure 8** | 通过编辑姿态描述可实现对手臂等身体部位的精确控制，验证了模型对文本条件的因果可解释性 |

![[assets/figures/papers/paper_list_l1878_Plan_Posture_and_Go_Towards_Open_vocabulary_Text_to_Motion_Generation/figures/005_Table_1.jpg]]
*Table 1: Comparison of our method with previous methods on the subsets of the IDEA-400 [45] dataset, i.e., ood368 and kungfu. We achieve superior performance on R precision, and the MultiModal Dist. MDM [85] is for supervised learning. MotionCLIP [84], Codebook+Interpolation [34], Avatarclip [34] and OOHMG [44] are designed for open vocabulary text-to-motion generation*

![[assets/figures/papers/paper_list_l1878_Plan_Posture_and_Go_Towards_Open_vocabulary_Text_to_Motion_Generation/figures/008_Figure_6.jpg]]
*Figure 6: Comparison of our method with previous text-to-pose generation methods*

![[assets/figures/papers/paper_list_l1878_Plan_Posture_and_Go_Towards_Open_vocabulary_Text_to_Motion_Generation/figures/009_Figure_7.jpg]]
*Figure 7: Comparison of different methods. Yellow color represents details that need attention, and red color represents inaccuracies*

## 定位与知识库关联

### 1. 方法谱系与范式对比

PRO-Motion 的提出根植于文本到动作生成领域的两条主要技术路线及其固有瓶颈：

**监督学习路线**以 **MDM**（Tevet et al., arXiv 2022）为代表，直接在文本-动作对上训练扩散模型。这类方法受限于配对训练数据的规模和覆盖范围，难以泛化到训练分布之外的开放词汇描述。

**CLIP对齐路线**包括 **MotionCLIP**（Tevet et al., ECCV 2022）、**AvatarCLIP**（Hong et al., CVPR 2022）和 **OOHMG**（Huang et al., CVPR 2023）。这些方法将3D姿态渲染为图像，利用CLIP的图像-文本空间进行跨模态对齐，从而绕过对配对文本-动作数据的需求。然而，CLIP空间缺乏时序先验，导致生成的全局运动（平移和旋转）不合理，且难以保证动作序列的时间连贯性。

PRO-Motion 的核心创新在于**引入大型语言模型作为“运动规划器”**，将开放世界的自然语言描述分解为结构化的姿势脚本，从而将复杂任务转化为三个可控的子模块。这一“计划-姿态-行进”框架与前述两条路线的本质区别如 Figure 2 所示：传统方法试图直接从文本映射到动作，而 PRO-Motion 通过中间的结构化姿势描述层，将语义理解与时序推理解耦。

### 2. 关键设计槽位对比

| 设计槽位 | 基线方法取值 | PRO-Motion 取值 | 证据锚点 |
|---------|------------|----------------|---------|
| 文本到动作的生成策略 | 直接在文本-动作对上训练生成模型，或使用CLIP对齐文本和姿势空间 | 通过LLM将文本分解为结构化的姿势脚本，然后使用扩散模型分别生成姿势和动作 | Figure 2, Sec. 3.2 |
| 全局运动预测 | 大多数方法仅生成局部姿态，缺乏全局运动 | 通过Go-Diffuser从关键姿势序列中推断全身平移和旋转 | Abstract, Sec. 3.4 |
| 姿势生成与文本条件 | 使用CLIP嵌入匹配或直接文本条件 | 使用Distill-BERT编码的结构化姿势脚本作为条件，并通过交叉注意力融合 | Sec. 3.3 |

### 3. 适用边界与局限

**适用边界**：
- 适用于开放词汇的自然语言描述，无需针对特定动作类别训练
- 支持通过编辑姿势描述实现对特定身体部位的细粒度控制（Figure 8）
- 可生成包含全局平移和旋转的完整人体运动

**已知局限**（基于论文分析和实验设计）：

1. **LLM依赖瓶颈**：运动规划器依赖GPT-3.5进行姿势脚本生成，推理成本较高，且受限于LLM的知识范围。对于LLM无法准确理解的罕见动作或专业运动术语，上游规划错误会向下游传播。

2. **姿势生成多样性受限**：Posture-Diffuser的训练依赖PoseScript数据集，其姿势覆盖范围可能不足以涵盖所有可能的身体姿态。在极端或罕见动作上的泛化性未充分验证。

3. **多阶段误差累积**：整个流水线包含LLM规划、姿势扩散、Viterbi序列选择、运动扩散四个阶段，每个阶段的误差可能累积放大。论文未系统分析各阶段误差的传播机制。

4. **评估基准的局限性**：实验主要在筛选的ood368（IDEA-400子集）和kungfu（Motion-X子集）上进行，规模较小。在更大规模、更多样化的开放世界基准上的性能尚不清楚。此外，R精度、FID等指标在开放世界场景下的适用性尚未充分探讨——当测试文本来自任意开放域时，基于预训练特征空间的度量可能无法准确反映生成质量。

5. **数据分布偏向**：训练数据主要基于AMASS运动捕捉数据集，可能偏向于运动捕捉场景中的常见动作，对日常生活中的细微动作或抽象情感表达（如“体验深刻的喜悦”）的生成质量需要更多验证。

### 4. 开放问题

1. **模糊提示处理**：运动规划器如何处理模糊或矛盾的自然语言提示？例如，“既快又慢地走”这类语义冲突的描述如何被分解为姿势脚本？

2. **标准基准对比缺失**：论文未在标准基准（如HumanML3D）上与全监督方法进行量化对比。在封闭词汇设定下，PRO-Motion 的多阶段框架是否会因为信息损失而弱于端到端监督方法？

3. **扩展性**：框架能否扩展到多人交互或场景交互的动作生成？姿势脚本的表示方式是否足以描述多智能体协调或物体操控等复杂场景？

4. **实时性**：如何进一步缩减LLM推理和多阶段扩散采样的开销，实现实时交互？当前流水线的端到端延迟在论文中未报告。

5. **评估体系**：在开放词汇设定下，如何设计更合理的评估指标？现有的R精度依赖测试集内负样本，可能无法反映真实开放场景中的语义对齐质量。

## 原文 PDF

![[paperPDFs/ECCV_2024/Plan_Posture_and_Go_Towards_Open_vocabulary_Text_to_Motion_Generation.pdf]]
