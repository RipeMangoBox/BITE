---
title: Motion-example-controlled Co-speech Gesture Generation Leveraging Large Language Models
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_Large_Language_Models.pdf
project_link: https://robinwitch.github.io/MECo-Page
code_link: null
aliases:
- MECCSGGLLLM
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将运动样例的离散token序列经去重、打乱和dropout后作为显式提示前缀直接输入大语言模型，利用LLM的上下文理解与条件自回归能力使输出token序列隐式复现样例运动特征，并通过惩罚项和logit偏置调节模仿程度。
primary_logic: 利用预训练LLM的通用文本理解和分布建模能力，将语音与运动统一为离散token并通过三阶段微调（嵌入对齐、语音到手势映射、样例条件训练）实现高保真样例一致手势，同时几乎不损害LLM原生文本能力（MMLU下降<0.5%）。
claims:
- 在BEAT2语音到手势生成上取得最优FGD (3.401)，加入样例后进一步降至2.999；多样性也最高（15.30）。
- 与示例驱动方法SynTalker和ZeroEGGS相比，MECo在ZEGGS数据集上的示例相似度（FGD1_test=1.98）远优于ZeroEGGS（4.54）和SynTalker（在BEAT2上FGD1_test=8.21）。
- 微调后LLM的MMLU得分仅从46.50降至46.27，退化0.49%，大幅优于其他多模态LLM方法。
- 消融显示，去除冻结初始化（w/o freeze）使FGD飙升至8.512，验证了Token嵌入初始化对保护LLM能力至关重要。
---

# Motion-example-controlled Co-speech Gesture Generation Leveraging Large Language Models

> [!tip] 核心洞察
> 利用预训练LLM的通用文本理解和分布建模能力，将语音与运动统一为离散token并通过三阶段微调（嵌入对齐、语音到手势映射、样例条件训练）实现高保真样例一致手势，同时几乎不损害LLM原生文本能力（MMLU下降<0.5%）。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用大型语言模型的运动样例可控共语手势生成 |
| 英文题名 | Motion-example-controlled Co-speech Gesture Generation Leveraging Large Language Models |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [Project](https://robinwitch.github.io/MECo-Page) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MECo |
| Dataset | BEAT2, ZEGGS |

> [!tip] 效果简介
> - BEAT2 上，FGD (×10⁻¹) 3.401 vs 5.512 (EMAGE) (-2.111)；Diversity (L1) 15.30 vs 13.47 (TalkShow) (+1.83)。
> - ZEGGS 上，FGD1_test (示例相似度) 1.98 ± 0.59 vs 4.54 ± 0.28 (ZeroEGGS) (-2.56)。

## 概要

共语手势生成旨在根据语音音频合成与说话内容同步、风格自然的人体手势动作。现有方法面临一个核心瓶颈：**样例驱动的手势生成通常依赖压缩后的风格向量或伪标签作为条件，这不可避免地丢失了运动样例中的精细运动学细节**（如关节速度、加速度模式、身体部位协调关系）。同时，基于预设标签的控制方式受限于标注粒度，无法灵活表达自由风格，导致生成姿势与样例匹配度低，且难以保持与语音节奏的对齐。

针对上述问题，本文提出 **MECo**（Motion-Example-Controlled Co-speech Gesture Generation），一个利用大型语言模型（LLM）实现运动样例可控共语手势生成的框架。其核心洞察在于：**利用预训练LLM的通用上下文理解与分布建模能力，将语音与运动统一为离散token，通过三阶段微调实现高保真样例一致手势生成，同时几乎不损害LLM原生的文本能力**。

MECo的关键技术路线为：将运动样例的离散token序列经过去重、打乱和dropout处理后，作为显式提示前缀直接输入LLM；LLM在语音token的引导下自回归生成目标运动token，并通过惩罚项和logit偏置调节对样例风格的模仿程度。这一设计使模型能够隐式复现样例中的运动特征，而非仅依赖压缩后的全局风格编码。

实验结果表明，MECo在语音到手势生成任务上取得最优FGD（3.401），加入运动样例后FGD进一步降至2.999，同时多样性达到最高（15.30）。在与示例驱动方法的对比中，MECo在ZEGGS数据集上的示例相似度（FGD1_test=1.98）显著优于ZeroEGGS（4.54）和SynTalker（在BEAT2上FGD1_test=8.21）。微调后LLM的MMLU得分仅从46.50降至46.27，退化幅度不足0.5%，验证了所提三阶段微调策略对保护LLM原生能力的有效性。

方法的主要局限包括：无法提供精准的关节级别控制；运动tokenizer采用非因果架构，仅支持离线生成；以及在域外数据上的泛化能力有限。未来方向包括设计因果运动tokenizer以实现低延迟实时生成，以及通过更大规模数据或不同LLM结构突破模型扩展瓶颈。



共语手势（co-speech gesture）是人类交流中与语音节奏和语义自然同步的身体动作，对于提升虚拟人、数字角色和具身智能体的表现力至关重要。自动生成与语音匹配且风格可控的共语手势，一直是计算机图形学与多模态学习交叉领域的前沿问题。

现有方法在处理风格控制时面临两个核心瓶颈。其一，基于预设标签的风格控制方法（如直接将“高兴”“开放”等离散属性作为条件）受限于标注粒度和类别数量，无法灵活表达连续、复合或新颖的运动风格。其二，近年来兴起的样例驱动方法试图通过提供一段参考运动来引导生成，但主流方案在条件化方式上存在结构性缺陷：**SynTalker**（Chen et al., 2024a）尝试建立文本-运动对齐，但跨模态映射过程损失了运动样例中的精细运动学细节；**ZeroEGGS**（Ghorbani et al., 2023）将运动样例压缩为固定维度的风格向量作为条件，这种信息瓶颈不可避免地丢弃了样例中的时间动态和局部运动模式。这些方法在定量评估中表现出明显的样例-生成距离偏大：ZeroEGGS在ZEGGS数据集上的FGD1_test高达4.54，SynTalker在BEAT2上的FGD1_test达到8.21，表明生成手势与参考样例之间存在显著的分布偏移。

与此同时，语音到手势生成（speech-to-gesture）领域的方法演进为多模态集成提供了新的技术语境。早期方法如**S2G**（Ginosar et al., CVPR 2019）采用确定性映射，生成的多样性不足；**Trimodal**（Yoon et al., TOG 2020）引入文本-音频-身份三模态融合，但各模态编码器独立训练，缺乏统一的表示空间；**TalkShow**（Yi et al., CVPR 2023）基于VQ-VAE进行离散化建模，在生成质量上取得进步，但多样性（BEAT2上Diversity=13.47）仍有提升空间；**EMAGE**（Liu et al., 2024b）作为当前最优的全身体手势生成方法，在BEAT2上FGD达到5.512，但该方法并非为样例条件控制设计，无法直接利用参考运动进行风格引导。

上述技术格局揭示了一个关键缺口：**如何在保留运动样例完整信息的前提下，将其作为灵活、可调节的条件注入生成过程，同时不损害语音-手势的对齐质量？** 这一问题的解决需要突破传统“压缩编码再注入”的范式，寻找一种能够原生理解序列模态、保持信息保真度且具备上下文建模能力的生成架构。大型语言模型（LLM）在通用序列理解和条件自回归生成方面的突破性进展，为这一方向提供了新的可能性——如果将语音和运动统一表示为离散token序列，LLM的上下文学习能力理论上可以同时解析语音内容和运动样例风格，从而在统一的token空间中实现高保真、可控的共语手势生成。



## 核心方法与创新机理

MECo的核心创新在于**将运动样例作为显式离散Token提示直接输入大语言模型**，替代了传统方法中将样例压缩为固定维度风格向量或CLIP嵌入的间接条件方式。这一设计使LLM能够利用其上下文理解与自回归建模能力，在生成目标手势Token序列时隐式复现样例的运动特征，从而在保持语音对齐的同时实现高保真的样例一致性。

具体而言，MECo通过以下三个关键机制实现上述目标：

1. **运动样例的Token化与提示构造**：运动样例经Motion RQ-VAE编码为离散Token序列后，经过**去重、随机打乱和Dropout**处理，作为系统提示前缀直接输入LLM（见Section 3.2.3）。这种处理方式迫使模型学习样例Token的共现模式而非简单记忆序列顺序，增强了泛化能力。

2. **三阶段渐进式微调策略**：区别于传统多模态LLM方法分别训练模态编码器再对齐的做法，MECo直接扩展LLM词表，通过**嵌入层冻结初始化→语音到手势映射→样例条件生成**三个阶段逐步将语音与运动模态融入LLM（见Section 3.2）。第一阶段仅训练新增Token的嵌入和输出层，使新Token与LLM预训练分布对齐，这是保护LLM原生能力的关键——消融实验表明，去除该阶段（w/o freeze）会导致FGD从3.401飙升至8.512（Table 1）。

3. **惩罚项与Logit偏置的双重控制**：训练阶段引入惩罚项 $\lambda \sum_{i=1}^{T_c} \phi(\mathbf{c}_i \notin \{\mathbf{c}_1, \ldots, \mathbf{c}_{T_C}\})$ 抑制生成非样例Token（Eq. 5）；推理阶段通过 $logits_i' = (logits_i + \beta) \cdot \gamma^t$ 对样例Token施加概率增强，并以衰减因子 $\gamma$ 避免重复采样（Eq. 6），提供了从严格模仿到自由生成的连续可控性。

上述设计使MECo在BEAT2基准上取得FGD 3.401的最优结果（加入样例后进一步降至2.999），同时生成多样性达到15.30，显著优于TalkShow（13.47）和EMAGE（5.512）等方法（Table 1）。在ZEGGS数据集上的示例相似度（FGD1_test=1.98）也远优于ZeroEGGS（4.54），验证了显式Token条件在保留运动细节方面的优势（Table 2）。此外，微调后LLM的MMLU得分仅从46.50降至46.27（退化0.49%），表明该方法几乎不损害LLM的通用文本能力（Table 6）。



MECo 的整体 pipeline 围绕“离散化—提示前缀—自回归生成”三条主线展开，如 Figure 2 和 Figure 3 所示。系统接收两类输入：**语音音频**和**运动样例**（可为运动片段、单帧姿态、人体视频甚至文本描述，见 Figure 1）。两类输入分别经过独立的离散化 tokenizer 转换为 token 序列，再以特定提示模板（Figure 8）拼接后馈入大语言模型（LLM）进行自回归生成；生成的离散运动 token 经运动解码器恢复为连续的目标手势运动序列。

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/002_Figure_2.jpg]]
*Figure 2: Our model takes motion examples and speech audio as inputs. Both inputs are converted into token sequences by tokenizers and fed into an LLM for autoregressive generation. The generated motion tokens are then processed through a motion decoder to produce the target gesture motion*

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/003_Figure_3.jpg]]
*Figure 3: The structure of our example-guided co-speech generation model. Both motion and audio are tokenized and fed into a large language model (LLM) to generate co-speech motion tokens. Initially, we fine-tune the embedding layer and output linear layer (unembedding space) to adapt the new tokens to the token distribution of the LLM. Subsequently, we perform full parameter fine-tuning to enable the LLM to generate motion tokens*

### 输入离散化：运动与语音的统一 token 表示

运动侧采用 **Motion RQ-VAE**（Section 3.1）将运动序列压缩为离散 token。该模块包含编码器、残差量化层和解码器，训练时最小化 L1 重建损失与残差量化的承诺损失之和（Eq. (1)）。为支持精细控制，运动 token 化按解剖结构分区进行——上半身、下半身、双手分别独立量化，使得后续可通过拼接不同区域的 token 实现身体部位的独立风格注入（Figure 5）。

语音侧采用 **HuBERT Audio Tokenizer**（Section 3.2）将原始音频波形编码为离散单元序列，与运动 token 共享相同的离散符号空间，从而统一为 LLM 可处理的 token 流。

### LLM 骨干与三阶段微调

LLM 骨干选用 **Qwen2.5**（Section 3.2），其原生词表被扩展以容纳新增的运动和语音 token。微调分三个阶段递进，核心目标是让 LLM 在几乎不损失原生文本能力的前提下，学会从语音和运动样例到目标手势的映射：

1. **Token 嵌入初始化**（Section 3.2.1）：冻结 LLM 主体参数，仅训练新增 token 的嵌入层和输出投影层，使新 token 的表示与 LLM 预训练分布对齐。这是保护 LLM 原生能力的关键步骤——消融实验显示，去除该阶段（w/o freeze）会使 FGD 从 3.401 飙升至 8.512（Table 1），验证了嵌入初始化对训练稳定性的决定性作用。

2. **语音到手势映射**（Section 3.2.2）：全参数微调 LLM，建立从语音 token 序列到目标运动 token 序列的条件自回归映射。此阶段不引入运动样例，使模型先掌握基本的语音-手势对应关系。消融表明，跳过此阶段（w/o s2g）会导致 FGD 升至 4.845（Table 1），说明分阶段训练有助于稳固跨模态关联。

3. **样例条件微调**（Section 3.2.3）：引入运动样例作为条件。具体做法是将样例的运动 token 序列经**去重—打乱—dropout**处理后，作为显式提示前缀拼接在语音 token 之前输入 LLM；训练损失中加入惩罚项（Eq. (5)），抑制生成非样例 token 的概率，从而强化输出对样例运动特征的复现。

### 推理时的可控采样

推理阶段（Section 3.3），语音 token 作为“用户查询”，运动样例 token 作为“系统提示”，角色的初始姿态 token 则作为 LLM 应答序列的起始点。通过调整 logit 偏置参数 β 和衰减因子 γ（Eq. (6)），可在推理时连续控制样例 token 被采样的频率：β 提升样例 token 的采样概率，γ 随 token 出现次数衰减以避免机械重复，从而在“忠实复现样例”与“保持语音对齐”之间提供可调节的平衡。

### 输入输出流总结

整个 pipeline 的端到端数据流可概括为：**运动样例 → Motion RQ-VAE → 离散 token（去重/打乱/dropout）→ 提示前缀**；**语音音频 → HuBERT → 离散 token → 提示正文**；二者拼接后输入 LLM 自回归生成目标运动 token，最终经运动解码器输出连续手势序列。该设计使得 MECo 既能以样例驱动方式生成与参考运动高度一致的共语手势，又在语音到手势基准上取得了最优的 FGD（3.401，Table 1），且引入样例后 FGD 进一步降至 2.999。



### 运动表示：解剖分区残差量化

MECo 将连续运动序列压缩为离散 token 的核心模块是基于残差向量量化（Residual Vector Quantization, RVQ）的运动 VAE。与常规 VQ-VAE 不同，该模块实施**解剖分区 token 化**：将人体姿态按功能区域划分为上半身、下半身和双手三个独立通道，每个通道拥有各自的编码器、码本和解码器。这一设计使得后续可通过组合不同样例的区域 token 实现身体部位的精细控制（见 Figure 5）。

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/007_Figure_5.jpg]]
*Figure 5: We can control specific body parts by tokenizing examples and combining their corresponding tokens. For instance, we tokenize two examples, use the upper body token from the first and the lower body token from the second as a prompt. The generated motion effectively reflects these references*

运动编码器 $\mathcal{E}$ 将输入运动序列 $\mathbf{m}_{1:N}$ 映射为潜在表示，经 $Q$ 层残差量化后得到离散 token 序列。解码器 $\mathcal{D}$ 从量化后的潜在表示重建运动。训练损失为：

$$
\mathcal{L}_{rec} = \| \hat{\mathbf{m}}_{1:N} - \mathbf{m}_{1:N} \|_1 + \eta \sum_{q=0}^{Q} \| \mathbf{z}_{1:n}^q - \mathrm{sg}[\hat{\mathbf{z}}_{1:n}^q] \|_2^2
$$

其中 $\hat{\mathbf{m}}_{1:N}$ 为重建运动，$\mathbf{z}^q$ 为第 $q$ 层量化前的编码器输出，$\hat{\mathbf{z}}^q$ 为量化后的码本向量，$\mathrm{sg}[\cdot]$ 为停止梯度算子，$\eta$ 为承诺损失权重。第一项 L1 损失保证重建精度，第二项承诺损失约束编码器输出靠近码本向量，同时通过停止梯度使码本独立更新。

消融实验（Table 5）表明，移除残差量化层的训练（w/o res. in train & infer）会使 FGD 从 3.401 升至 3.762 且视觉质量下降，验证了多层残差量化对运动细节保留的必要性。

### 语音 Token 化

语音模态通过预训练的 HuBERT 模型编码为离散单元序列。HuBERT 将原始音频波形转换为每 20ms 一个离散 token，4 秒音频对应约 200 个 token。这些 token 与运动 token 共享同一 LLM 词表空间，无需额外的跨模态对齐网络。

### LLM 骨干与三阶段微调

MECo 采用 Qwen2.5 作为 LLM 骨干，将语音和运动统一为离散 token 序列进行自回归建模。核心创新在于**三阶段微调策略**，逐步将多模态能力注入预训练 LLM 而不损害其原生文本能力。

**阶段一：Token 嵌入冻结初始化。** 直接向 LLM 添加新 token 并全参数微调会破坏预训练分布，导致训练崩溃。MECo 提出冻结 LLM 主体参数，仅训练新增 token 的嵌入层和输出投影层，使用 LLM 原始的下一 token 预测任务进行对齐。损失函数为：

$$
\mathcal{L}(\theta_0) = -\sum_{t=1}^{T_a} \log \hat{p}(\mathbf{a}_t \mid \mathbf{a}_1, \ldots, \mathbf{a}_{t-1}) - \sum_{t=1}^{T_c} \log \hat{p}(\mathbf{c}_t \mid \mathbf{c}_1, \ldots, \mathbf{c}_{t-1})
$$

其中 $\mathbf{a}_t$ 为音频 token，$\mathbf{c}_t$ 为运动 token，$\hat{p}$ 为 LLM 输出概率。此阶段使新 token 的嵌入与 LLM 预训练分布对齐，为后续微调提供稳定初始化。消融实验（Table 1）中去除冻结初始化（w/o freeze）使 FGD 从 3.401 飙升至 8.512，证明该阶段对保护 LLM 能力至关重要。

**阶段二：语音到手势映射。** 全参数微调 LLM，建立语音到运动的跨模态映射。损失为标准的下 token 预测交叉熵：

$$
\mathcal{L}(\boldsymbol{\theta}) = -\sum_{t=1}^{T_c} \log \mathcal{P}(m_t \mid \mathbf{a}_1, \ldots, \mathbf{a}_{T_a}, \mathbf{c}_1, \ldots, \mathbf{c}_{t-1})
$$

其中 $m_t$ 为目标运动 token。此阶段使模型学会从语音特征自回归生成连贯手势。消融中跳过此阶段（w/o s2g）使 FGD 升至 4.845，验证分阶段训练对建立语音-运动关联的必要性。

**阶段三：样例条件微调。** 引入运动样例作为显式控制信号。将样例运动 token 序列经**去重—随机打乱—dropout**处理后作为提示前缀 $\mathbf{E}_c$ 输入 LLM，训练损失加入惩罚项：

$$
\mathcal{L}(\boldsymbol{\theta}) = -\sum_{t=1}^{T_c} \log \boldsymbol{\phi}(\mathbf{c}_t \mid \mathbf{E}_c, \mathbf{a}_1, \ldots, \mathbf{a}_{T_a}, \mathbf{c}_1, \ldots, \mathbf{c}_{t-1}) + \lambda \sum_{i=1}^{T_c} \boldsymbol{\phi}(\mathbf{c}_i \notin \{\mathbf{c}_1, \ldots, \mathbf{c}_{T_C}\})
$$

其中 $\boldsymbol{\phi}$ 为 LLM 输出概率分布，$\lambda$ 为惩罚系数。惩罚项对生成不在运动样例 token 集合中的 token 施加额外损失，引导模型输出与样例风格一致的运动。去重和打乱操作防止 LLM 简单记忆样例序列，迫使模型学习样例的**运动学特征分布**而非时序模式。

### 推理阶段：Logit 偏置采样控制器

推理时，MECo 将音频作为用户查询、运动样例作为系统提示，并以角色初始姿态作为回答序列起点。为提供连续可控性，引入基于 logit 调整的采样控制器：

$$
logits_i' = (logits_i + \beta) \cdot \gamma^t
$$

其中 $\beta$ 为样例 token 的增强偏置，$\gamma$ 为衰减因子（$0 < \gamma \leq 1$），$t$ 为该 token 已出现的次数。$\beta$ 提高样例 token 的采样概率以增强风格一致性，$\gamma^t$ 随出现次数衰减以避免过度重复。通过调整 $\beta$ 和 $\gamma$，用户可在样例忠实度与生成多样性之间连续调节。

### 提示格式设计

Figure 8 展示了 MECo 的提示模板。与常规 LLM 的文本提示不同，MECo 使用运动 token 和音频 token 构建多模态提示：系统提示为去重打乱后的样例运动 token，用户查询为音频 token 序列，模型回答为目标运动 token。这种设计使 LLM 的上下文理解能力直接作用于运动域，无需文本中介。

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/011_Figure_8.jpg]]
*Figure 8: The prompt format of regular LLM and of our method. We prompt the LLM using tokens from motion and audio modals with different template designs*



## 实验与关键发现

### 主实验结果

**语音到手势生成基准** 在BEAT2数据集（Liu et al., 2024b）上，MECo在不使用运动样例的条件下即取得FGD 3.401（×10⁻¹），显著优于此前最优方法EMAGE的5.512（Table 1）。加入运动样例后，FGD进一步降至2.999，同时多样性达到15.30，超越TalkShow的13.47。BC指标为7.346，表明生成手势在保持语音节奏同步性方面同样具有竞争力。

**示例相似度** 在ZEGGS数据集上，MECo的FGD1_test为1.98±0.59，远优于ZeroEGGS的4.54±0.28（Table 2）。在BEAT2上，MECo的FGD1_test为1.91±0.66，而SynTalker为8.21±1.53。这一差距揭示了MECo的核心优势：通过将运动样例离散token直接作为LLM提示前缀，模型能够隐式复现样例中的精细运动学特征，而非仅依赖压缩风格向量。

**用户主观评价** 双盲配对比较研究（30名参试者，24组对比视频，0-2强度量纲）显示，MECo在人类相似性、恰当性和样例一致性三个维度上均显著优于对比方法（Table 4）。在BEAT2和ZEGGS两个数据集上，MECo的样例一致性评分均达到最高，验证了样例控制机制的主观有效性。

### 消融实验

| 消融变体 | FGD (×10⁻¹) | 关键发现 |
|---------|------------|---------|
| MECo（完整） | 3.401 | 基线 |
| w/o freeze | 8.512 | 移除冻结初始化阶段，新token嵌入无法与LLM预训练分布对齐，训练崩溃 |
| w/o s2g | 4.845 | 跳过语音到手势预训练，模型缺乏语音-运动关联先验 |
| w/o res. in train&infer | 3.762 | 残差量化层未参与训练和推理，重建质量下降 |

去除冻结初始化（w/o freeze）是影响最大的消融项，FGD从3.401飙升至8.512（Table 1），证实了Token嵌入初始化阶段对保护LLM原生能力并稳定后续微调至关重要。跳过语音到手势预训练（w/o s2g）使FGD升至4.845，表明分阶段训练策略有助于逐步建立跨模态映射。去除残差量化层训练（Table 5）导致FGD增至3.762且视觉质量下降，说明残差量化对运动重建精度有实质贡献。

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/004_Table_1.jpg]]
*Table 1: Comparison with the state-of-the art methods on BEAT2 [Liu et al. 2024b] test set. Quantitative evaluation on BEAT2. We report FGD ×10−1, BC ×10−1, and diversity. Bold face indicates the best result*

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/012_Table_5.jpg]]
*Table 5: Abalation study on BEAT2 [Liu et al. 2024b]. We report FGD ×10−1, BC ×10−1, and diversity*

### LLM文本能力保持

微调后，Qwen2.5的MMLU得分仅从46.50降至46.27，退化幅度仅0.49%（Table 6）。相比之下，其他多模态LLM方法在类似微调后通常面临更严重的文本能力退化。这一结果归因于三阶段微调策略中第一阶段仅训练新增token的嵌入和输出层，冻结LLM主体参数，使新token平滑融入预训练分布空间。

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/013_Table_6.jpg]]
*Table 6: Impact of finetuning on LLMs’ original text capabilities, M&S refers to motion and speech*

### 失败模式与局限性

1. **关节级控制缺失**：MECo无法提供精确的末端轨迹控制，运动tokenizer采用非因果架构，仅支持离线生成，无法实时在线推理。
2. **域外泛化受限**：运动VQ-VAE在in-the-wild视频重建的SMPL-X数据上可能产生物理不自然的伪影（如脚滑动），泛化能力有限。
3. **模型扩展瓶颈**：7B参数版本的性能并无提升，可能受限于共语手势训练数据的有限规模（约54k运动token），而非模型容量本身。
4. **样例与语义的权衡**：在极端样例条件下，生成手势可能过度偏向样例风格而削弱与语音语义内容的一致性，需要手动调节logit偏置参数β和衰减因子γ来平衡。

### 重要图表结论

- **Table 1**：MECo在BEAT2上以FGD 3.401取得语音到手势生成最优，加入样例后降至2.999，同时多样性最高（15.30）。
- **Table 2**：在示例相似度上，MECo（FGD1_test=1.98）大幅领先ZeroEGGS（4.54）和SynTalker（BEAT2上8.21），验证了离散token提示机制对样例特征复现的有效性。
- **Table 6**：微调后LLM的MMLU退化仅0.49%，证明三阶段微调策略在引入多模态能力的同时几乎不损害原生文本理解能力。
- **Figure 5**：通过分别token化上下半身样例并组合对应token作为提示，MECo可实现身体部位的精细控制，生成动作有效反映各自的参考样例。

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/005_Table_2.jpg]]
*Table 2: Comparison of the similarity between the generated results and the motion example. The values in this table represent the mean and standard deviation, where the standard deviation is shown after ’±’*

### 补充图表

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/010_Table_4.jpg]]
*Table 4: User study of different systems on BEAT2 and ZeroEGGS datasets. The results are reported as average scores with 95% confidence intervals*

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/008_Figure_6.jpg]]
*Figure 6: A qualitative comparison between our method and ZeroEGGS. Both methods use the same input, with the motion example displayed on the left side of the arrows in the figure, and the input audio presented at the bottom of the figure*

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/009_Figure_7.jpg]]
*Figure 7: A qualitative comparison between our method and SynTalker. Both methods use the same input, with the motion example displayed on the left side of the arrows in the figure, and the input audio presented at the bottom of the figure*

![[assets/figures/papers/paper_list_l1927_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_L/figures/014_Figure_9.jpg]]
*Figure 9: Screenshot of the user interface used for user study*



## 定位与知识库关联

### 技术路线定位

MECo 处于**样例驱动共语手势生成**与**多模态大语言模型**的交叉点。传统共语手势生成的主流范式可分为三类：

1. **语音到手势的直接映射**：早期方法如 **S2G**（Ginosar et al., CVPR 2019）直接从音频特征回归手势序列，但缺乏风格控制能力。后续工作 **Trimodal**（Yoon et al., TOG 2020）引入文本-音频-身份三模态条件，**TalkShow**（Yi et al., CVPR 2023）和 **EMAGE**（Liu et al., 2024b）进一步采用 VQ-VAE 与扩散模型，在语音对齐和运动质量上取得显著提升。然而，这些方法本质上是“一对多映射”的确定性或随机采样模型，无法接受用户指定的运动样例作为显式风格条件。

2. **样例驱动的风格控制**：**ZeroEGGS**（Ghorbani et al., 2023）通过将运动样例压缩为固定维度的风格向量作为条件输入，实现了初步的样例可控生成。**SynTalker**（Chen et al., 2024a）则尝试建立文本-运动对齐空间，以文本为中介桥接语音与运动风格。这两类方法的共同瓶颈在于：压缩后的风格向量或伪标签丢失了运动样例中的精细运动学细节——例如关节速度分布、运动节奏模式和肢体协调关系——导致生成手势与样例的匹配度有限。定量证据显示，ZeroEGGS 在 ZEGGS 测试集上的示例相似度 FGD1_test 为 4.54，SynTalker 在 BEAT2 上为 8.21，均显著劣于 MECo 的 1.98（Table 2）。

3. **基于 LLM 的多模态生成**：MECo 的核心创新在于将运动样例的离散 token 序列——经过去重、打乱和 dropout 处理后——作为显式提示前缀直接输入大语言模型，利用 LLM 的上下文理解与条件自回归能力，使输出 token 序列隐式复现样例的运动特征。这与前述方法形成根本性差异：**条件信号从“压缩表示”变为“稀疏 token 示例”**，信息的保真度由 LLM 的注意力机制而非瓶颈层的容量决定。

### 与相关工作的关键差异

| 维度 | 传统方法 (ZeroEGGS/SynTalker) | MECo |
|------|------------------------------|------|
| 样例编码方式 | 固定维度风格向量或 CLIP 嵌入 | 离散 token 序列（去重+打乱+dropout） |
| 条件注入位置 | 解码器侧的条件输入 | LLM 的提示前缀（系统提示角色） |
| 多模态集成 | 分别训练编码器并映射到文本空间 | 直接扩展 LLM 词表，三阶段微调 |
| 风格保真度 | 受瓶颈层容量限制 | 由 LLM 注意力机制动态决定 |
| 文本能力保留 | 不适用（非 LLM 方法） | MMLU 仅下降 0.49%（46.50→46.27） |

### 适用边界与局限

**适用场景**：MECo 在以下条件下表现最优——
- 运动样例与目标语音在节奏和情感基调上存在可迁移的共性；
- 样例来自与训练数据分布相近的运动域（如 BEAT2 或 ZEGGS 数据集内的 SMPL-X 姿态序列）；
- 对生成手势的全局风格一致性要求高于关节级精确控制。

**已知局限**：

1. **关节级控制的缺失**：MECo 无法提供精准的末端轨迹控制（如手指指向特定位置或手掌精确朝向）。运动 tokenizer 的分区编码（上身/下身/手部）虽支持部位级别的样例混合（Figure 5），但 token 的离散化本质决定了其控制粒度止于码本索引级别，而非连续运动学参数。

2. **域外泛化能力有限**：运动 VQ-VAE 在 in-the-wild 视频重建的 SMPL-X 数据上可能产生物理不自然的伪影（如脚滑动）。这是因为 RQ-VAE 的码本是在受控数据集上训练的，对域外运动模式的量化误差会级联放大至下游 LLM 的生成结果。

3. **在线推理的架构障碍**：当前运动 tokenizer 采用非因果架构（编码器需访问完整序列），导致系统只能离线批处理生成，无法支持实时在线推理。这是制约 MECo 走向交互式应用（如虚拟人实时对话）的核心瓶颈。

4. **模型扩展的边际收益递减**：论文报告 7B 参数版本的性能并无提升，推测原因在于共语手势训练数据量有限（约 54k 运动 token），不足以支撑更大模型的充分训练。这提示当前瓶颈可能在数据规模而非模型容量。

### 开放问题

1. **因果运动 tokenizer 的设计**：如何构建因果架构的运动量化器，实现低延迟的逐帧 token 化，是打通实时生成链路的关键。可能的路径包括因果卷积编码器或基于状态空间模型的序列建模。

2. **语音语义与运动风格的一致性**：当前 MECo 在样例相似度（FGD1_test=1.98）上表现优异，但生成手势与语音语义内容（如特定词汇的重音手势、否定性摇头等）的对齐程度尚未被独立量化。如何在保留样例运动细节的同时，增强语义级的手势-语音耦合，是一个值得深入的方向。

3. **数据扩展与模型结构的协同优化**：7B 模型的性能停滞暗示需要更大规模或更高质量的训练数据。同时，不同的 LLM 架构（如非自回归解码器、MoE 结构）是否能在有限数据下实现更好的扩展性，仍有待探索。

4. **文本描述条件的精细对齐**：MECo 已展示文本提示作为运动样例的潜力（Figure 1），但从文本到运动 token 的映射目前依赖 LLM 的隐式理解。通过显式的动作-语言对比学习或指令微调，能否实现“快速挥手”与“缓慢挥手”等细粒度文本控制，是一个有意义的延伸方向。



## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_Large_Language_Models.pdf]]
