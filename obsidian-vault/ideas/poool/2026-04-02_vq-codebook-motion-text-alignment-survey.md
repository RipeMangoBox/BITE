---
created: 2026-04-02
updated: 2026-04-08T13:29
tags:
  - survey
  - VQ_VAE
  - codebook
  - motion_text_alignment
  - text_to_motion
---
# VQ-VAE / 码本视角下的动作-文本语义对齐综述

> 目标：专门整理“动作与文本语义对齐”里与 `VQ / VQ-VAE / codebook / 离散 token` 强相关的方法。
>
> 重点不是泛泛罗列 text-to-motion，而是显式追踪这些工作到底如何做对齐：
>
> 1. 将动作空间与文本空间直接对齐。
> 2. 扩充或共享词表 / 码本。
> 3. 用映射器把 motion token 接到 LLM。
> 4. 用多码本、分部位码本、组合式码流承载更细粒度语义。
> 5. 用显式辅助任务、检索或对比损失，把“语义对齐”从隐式条件建模变成可训练目标。

---
## 一页结论

### 结论 1

这条线的主问题其实不是“能不能生成动作”，而是“文本语义如何落到可操作的离散动作词汇上”。

如果只看最早的 `T2M-GPT` 路线，答案还是比较朴素的：

- 文本编码成条件向量；
- 动作用 VQ-VAE 量化为离散 token；
- GPT 预测 motion token。

这时的“对齐”主要还是隐式的条件生成。

后续工作的主要分化方向，可以概括为五类：

- 共享词表 / 词表扩充：把 motion token 真正当成“语言词汇”的一部分；
- 码本映射 / 词汇适配：不直接污染 LLM 原始词表，而是学习 motion token 到 LLM 隐空间的接口；
- 共享码本 / 统一 token 空间：让不同动作域或不同模态共用一套离散语义单元；
- 分部位码本 / 组合式码流：让语义能落在 body-part 或局部结构上，而不是只落在全身整体 token 上；
- 显式语义对齐目标：对比学习、检索、细粒度脚本、时间定位、辅助翻译任务等，把 alignment 变成明确训练信号。

### 结论 2

如果从“你想设计新方法”角度看，最值得借的不是某一篇论文，而是三种模式。

#### 模式 A：把 motion token 直接语言化

代表工作：

- [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Generation_and_Editing|UniPose]]

核心思想：

- 先有 VQ-VAE 把 motion 变成离散 token；
- 再把这些 token 视为“外语词汇”；
- 用统一词表让 LLM 学文本和动作之间的翻译关系。

适合做统一生成/理解框架，但容易遇到两个问题：

- motion 词表太小，细节不够；
- 直接扩词表会污染原始语言空间，训练效率也未必高。

#### 模式 B：不强行并词表，而是学一个 motion-to-LLM 映射接口

代表工作：

- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]

核心思想：

- motion 侧保留自己的 VQ token 语义；
- 通过 vocabulary adaptor 把 motion embedding 映射到 LLM 隐空间；
- 再通过独立 motion head 输出合法 motion token。

这类方法对工程更友好，本质上是“码本映射”路线。

#### 模式 C：不要只对齐“整段文本 ↔ 整段动作”，而要对齐到局部结构

代表工作：

- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]
- [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]
- [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]

核心思想：

- 语义不该只落在句子级 embedding；
- 它还应落在 body-part、时间段、局部 exemplars、局部脚本、局部 token stream 上。

这类方法对“细粒度可控生成”和“局部语义编辑”最重要。

---
## 分类总览：这些方法到底在对齐什么

### 1. 共享词表 / 词表扩充

核心机制：直接把 motion token 并入语言词表。

代表工作：

- [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Generation_and_Editing|UniPose]]

更像在解决的问题：让 LLM 把动作视为可读写的“另一种语言”。

### 2. 码本映射 / 词汇适配

核心机制：motion token 不直接进原词表，而是映射到 LLM 隐空间。

代表工作：

- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]

更像在解决的问题：如何低成本把 motion code 接入现成 LLM。

### 3. 共享码本 / 统一 token 空间

核心机制：不同动作域或不同模态共用同一离散语义空间。

代表工作：

- [[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation|M3GPT]]
- [[paperAnalysis/Motion_Generation/CVPR_2023/2023_UDE_A_Unified_Driving_Engine_for_Human_Motion_Generation|UDE]]

更像在解决的问题：如何让跨任务、跨模态迁移成立。

### 4. 分部位码本 / 组合式码流

核心机制：不再只用全身单码本，而是按部位拆分或组合。

代表工作：

- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]
- [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]
- [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]

更像在解决的问题：如何把语义对齐到局部身体结构。

### 5. 码本扩充 / 多层残差量化

核心机制：用 RVQ 或多层量化扩大动作词汇表达能力。

代表工作：

- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]
- [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]

更像在解决的问题：先提升 motion token 的表达上限。

### 6. 显式语义对齐损失

核心机制：对比学习、InfoNCE、匹配分类、检索增强。

代表工作：

- [[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]]
- [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]
- [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]

更像在解决的问题：如何把“对齐”从隐式条件变成训练目标。

### 7. 显式粒度桥接任务

核心机制：motion script、时间定位、粗细粒度互译。

代表工作：

- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]

更像在解决的问题：如何让句子级文本真正落到局部时间段。

---
## 第一类：共享词表 / 词表扩充

这类方法最直接。

它们的核心判断是：既然 motion 已经被 VQ-VAE 离散化为 token，那它和 text token 在“形式上”就是统一的，剩下要做的只是让 LLM 接受这些新 token。

### MotionGPT：最典型的“运动即外语”

对应论文：[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]。

#### MotionGPT 的对齐策略

- 先用 VQ-VAE 把动作量化成 `Vm = 512` 个 motion token；
- 再把 motion token 直接并入 T5 原始文本词表；
- 构造统一词表 `V = {Vt, Vm}`；
- 用 motion-to-text、text-to-motion、prediction、in-between 等多任务训练，让模型把动作 token 当成一种“外语”。

#### MotionGPT 的码本意义

MotionGPT 本质上不是在学“文本 embedding 到动作 latent 的投影”，而是在学：

- 文本词和动作词如何共存在一个离散语法系统里；
- motion codebook 如何被 LLM 视为可翻译、可续写、可补全的词汇集合。

这就是最标准的词表扩充式对齐。

#### MotionGPT 的优点

- 最统一；
- 多任务最自然；
- 语言模型 prior 可以直接迁移到动作 token 序列建模。

#### MotionGPT 的局限

- 单码本 VQ-VAE 细节有限；
- 直接扩词表，motion 与 text 共享生成接口，容易出现模态混用或语义污染；
- 本质仍偏粗粒度，对 body-part 细节对齐能力有限。

### UniPose：把“姿态 token”也视为统一词汇

对应论文：[[paperAnalysis/Motion_Generation/CVPR_2025/2025_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Generation_and_Editing|UniPose]]。

#### UniPose 的对齐策略

- 3D pose 先用 VQ-VAE 离散化为码本大小 2048、每姿态 80 个 token；
- 与文本 token 共享统一词汇空间；
- LLM 在同一词汇系统中处理理解、生成和编辑。

#### UniPose 的价值

虽然 UniPose 是单帧 pose 而非长时 motion，但它很清楚地说明：

- 只要离散 token 足够稳定；
- “共享词表”这套范式可以从 motion 扩展到 pose、image-conditioned pose、editing。

对做 motion-text work 的启发是：

- 词表扩充路线并不局限于文本到动作生成；
- 它本质是让 LLM 变成一个统一的多模态离散推理器。

---
## 第二类：码本映射 / 词汇适配

这类方法承认一个现实：

- motion token 是离散的没错；
- 但不一定非要把它们粗暴塞进 LLM 原始词表。

更优雅的做法是保留 motion codebook 自身的结构，再学一个映射器，把 motion 侧的语义接到 LLM 的隐空间。

### AvatarGPT：vocabulary adaptor 是这一类最清楚的代表

对应论文：[[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]。

#### AvatarGPT 的对齐策略

- motion 先经 VQ-VAE 量化；
- adaptor 把 VQ embedding 从 motion 空间映射到 LLM hidden space；
- 不直接污染 LLM 原始词表；
- 同时增加独立的 motion prediction head，保证输出仍然落在合法 motion token 范围内。

#### AvatarGPT 真正在对齐什么

它并不是“对齐文本空间和 motion 空间到一个完全相同的 embedding 空间”。

它更像是在做两步：

1. 保留 motion codebook 作为 motion 侧语义字典；
2. 学一个 `motion-token → LLM hidden state` 的接口。

所以它是非常典型的码本映射思路。

#### AvatarGPT 为什么重要

相较于 MotionGPT 式直接扩词表，AvatarGPT 提供了更工程化的折中：

- motion codebook 不需要完全语言化；
- LLM 也不需要重学整个扩展词表；
- 可以更方便地把现有大模型接进 motion 任务。

---
## 第三类：共享码本 / 统一 token 空间

这里的重点不再是“motion token 怎么接 LLM”，而是：

- 不同任务、不同运动域、不同模态之间，是否能共用同一套 motion 离散语义单元。

### M3GPT：共享 Motion + Dance tokenizer

对应论文：[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation|M3GPT]]。

#### M3GPT 的对齐策略

- motion 和 dance 共享一套 VQ-VAE tokenizer；
- 音乐则用另一套 tokenizer；
- 在统一词表中做多模态建模；
- 再通过 `music→text` 和 `text→dance` 这些辅助任务，把音乐、文本、舞蹈语义串起来。

#### M3GPT 的关键启发

更关键的是它说明了：

- 共享码本等于共享语义原语；
- 一旦 motion 和 dance token 落在同一空间里，text-motion 学到的语义迁移就有机会作用到 music-dance。

这是一种非常有价值的统一 token 空间对齐。

#### M3GPT 的额外亮点

M3GPT 不是只优化离散 token 预测。

它还让 de-tokenizer 的连续动作重建误差反传回 LLM，使训练同时发生在：

- 离散语义空间；
- 连续动作空间。

所以它既是共享码本路线，也是“离散-连续双空间联合对齐”的代表。

### UDE：统一 codebook 支持跨模态切换

对应论文：[[paperAnalysis/Motion_Generation/CVPR_2023/2023_UDE_A_Unified_Driving_Engine_for_Human_Motion_Generation|UDE]]。

#### UDE 的对齐策略

- 文本和音频先经模态无关编码器 `MATE` 映射到联合空间；
- 后续统一由同一个 motion codebook 和 UTT 自回归预测 motion token；
- 因为 codebook 被文本驱动和音频驱动两边共享，所以可以做跨模态自然切换。

#### UDE 的意义

UDE 的关键词是：统一 codebook 不是为了省参数，而是为了让“同一段运动 token”在不同模态条件下都成立。

对做 text-motion alignment 的启发：

- 如果系统未来想支持更多模态，早期就把 motion codebook 设计成“模态无关动作语义单元”会很有价值。

---
## 第四类：分部位码本 / 组合式码流 / 码本拼接

这类方法最接近你提到的“码本拼接、局部对齐、body-part 对齐”。

核心思想是：

- 单一全身 codebook 往往太粗；
- 文本语义里很多信息本来就是局部的，例如“右手挥动”“左腿后撤”“脸部高兴、上身前倾”；
- 所以 token 化也应该是分解式、组合式的。

### The Language of Motion：四路分部位 VQ-VAE

对应论文：[[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]。

#### The Language of Motion 的对齐策略

- 面部、手部、上身、下身分别训练 VQ-VAE；
- 各自得到部位专属 token；
- 再统一到多模态词表里，与文本 token、音频 token 一起建模；
- 预训练时显式做“body-part ↔ audio/text”对齐。

#### 为什么它最像“码本拼接”

因为它不是单纯有多个码本，而是明确地：

- 为不同身体区域维护不同的离散语义子空间；
- 再把这些子空间组合成统一 motion 表达；
- 让不同语义源分别对齐不同 body part。

例如：

- hand token 更偏语义内容；
- face token 更偏表情和韵律；
- lower-body token 更偏整体节律。

#### 研究启发

如果要做“文本中不同片段控制不同身体部位”，这篇的组合式 tokenization 是非常直接的参考。

### Being-M0.5：Part-aware Residual Quantization

对应论文：[[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]。

#### Being-M0.5 的对齐策略

- 人体分解为 5 个解剖区域；
- 每个区域独立残差量化；
- 得到“部位 × 层级”的 token 组织形式；
- LLM 在统一词表上处理这些 token，实现部位级控制。

#### Being-M0.5 为什么重要

这篇不仅是“分部位码本”，还是“分部位 + 残差量化”的结合：

- 局部结构清晰；
- token 表达能力又比单层 codebook 强。

它说明分部位对齐和码本扩充并不冲突，完全可以同时做。

### ReMoGPT：部位级检索增强

对应论文：[[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]。

#### ReMoGPT 的对齐策略

- motion 仍先 token 化；
- 但检索不再只在句子级做 text-motion matching；
- 而是通过 `PL-TMR` 做 part-level 的 text-motion retrieval；
- 再把检索到的局部 exemplars 注入 prompt。

#### ReMoGPT 和上面两篇的差别

- The Language of Motion 更偏 tokenizer 层面分部位建模；
- ReMoGPT 更偏检索和示例层面分部位对齐。

但两者都在解决同一个问题：

- 文本语义不能只在全局句子向量里对齐；
- 它应该落到具体 body-part motion pattern 上。

---
## 第五类：码本扩充 / 多层残差量化

这一类方法本身不一定直接做 text-motion alignment，但它们会显著改变“动作语义能否被精细表达”的上限。

换句话说：

- 如果 motion token 本身过粗；
- 语言再强，也只能对齐到粗糙动作原语。

所以码本扩充其实是 alignment 的基础设施。

### T2M-GPT：单码本的基线起点

对应论文：[[paperAnalysis/Motion_Generation/CVPR_2023/2023_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete_Representations|T2M-GPT]]。

#### T2M-GPT 的对齐策略

- 文本用 CLIP 编码；
- 动作用单码本 VQ-VAE 量化；
- GPT 自回归预测 motion token。

#### T2M-GPT 的定位

T2M-GPT 是离散动作-文本路线的标准起点，但从今天回看，它更像是：

- 证明“text → motion token”可行；
- 还没有很好解决 token 粒度不够的问题。

### MoMask：RVQ 把动作词汇容量显著拉高

对应论文：[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]。

#### MoMask 的对齐策略

严格说，MoMask 的主要创新不在文本空间，而在 motion token 空间：

- 用 RVQ 替代单层 VQ；
- 让 token 表示从“单码一次量化”升级成“粗到细多层残差量化”；
- 再用 masked transformer 生成基础层 token，residual transformer 逐层细化。

#### 为什么 MoMask 对 alignment 重要

MoMask 说明：

- 当动作 token 的重建精度从单码本提升到多层残差码本后；
- 文本条件的语义可以落到更细的动作差异上；
- 因而 `R-Precision` 和 `FID` 都会显著改善。

它相当于在说：更好的 motion codebook 本身就是更好的语义承载体。

### Being-M0.5：把“码本扩充”与“分部位对齐”合并

对应论文：[[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]。

#### Being-M0.5 在这一类中的意义

它的 `PRQ` 可以理解为更进一步的版本：

- 不是只在全身 latent 上堆 RVQ 层；
- 而是对每个 body part 分别做多层残差量化。

这使得“码本扩充”不只是增加容量，还直接带来了结构性可控性。

---
## 第六类：显式语义对齐损失

这类方法的关键区别是：

- 不满足于“给文本条件然后训练生成”；
- 而是明确写出某种 alignment objective，让文本和动作在表示空间中被拉近或比较。

### LaMP：四路代理任务，把对齐做成预训练目标

对应论文：[[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]]。

#### LaMP 的对齐策略

LaMP 做了四类代理任务：

- 对比学习；
- matching 分类；
- motion-conditioned text generation；
- text-conditioned motion generation。

它相当于同时训练：

- motion-aware text feature；
- language-aware motion feature。

#### LaMP 和 MotionGPT / AvatarGPT 的区别

- MotionGPT 更偏统一词表；
- AvatarGPT 更偏接入接口；
- LaMP 则直接把“language-motion 对齐”本身当成预训练对象。

#### LaMP 对码本路线的意义

LaMP 并没有推翻 VQ-VAE，而是：

- 保留离散 motion token；
- 但把 `CLIP text feature` 换成 `motion-aware text feature`；
- 让 text condition 不再停留在 image-language 空间，而是真正适配 motion。

这是非常重要的一步。

### MoLingo：语义对齐 latent space + InfoNCE

对应论文：[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]。

#### MoLingo 的对齐策略

MoLingo 严格说不是 VQ-VAE codebook 路线，而是 VAE 连续潜空间路线。

但它对“动作-文本语义对齐”非常关键，因为它把对齐写成了明确的损失：

- 在重建损失之外加入 `InfoNCE`；
- 拉近匹配文本-动作对的潜码；
- 推远不匹配对；
- 让扩散发生在语义结构化的 motion latent 里。

#### 为什么这里仍然值得纳入

因为它非常清晰地给出了一个判断：

- 光有好的生成器不够；
- motion latent 或 code space 本身也必须具备语义结构；
- 否则文本条件很难有效控制生成。

如果以后做离散 codebook 工作，也完全可以借鉴这种 `recon + align loss` 的思路。

### ReMoGPT：检索增强也是一种显式对齐

对应论文：[[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]。

#### ReMoGPT 的显式对齐机制

这里的显式对齐不体现为一个简单 loss，而体现为：

- 用 part-level 检索显式找出与 query 对应的局部动作模式；
- 再把这些 exemplars 作为额外对齐锚点注入模型。

这其实是一种“外部记忆增强”的 alignment：

- 不是逼模型参数自己记住所有局部语义；
- 而是允许模型在生成时检索到最相近的局部动作原语。

---
## 第七类：显式粒度桥接任务

有些论文没有直接改 codebook，却显著提升了“文本如何落到动作局部结构”这件事。

这类论文非常值得纳入，因为它们解决的是 alignment 的另一半：不是 tokenizer 本身，而是 supervision granularity。

### MG-MotionLLM：用 motion script 和 localization 强制细粒度对齐

对应论文：[[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]。

#### MG-MotionLLM 的对齐策略

- 仍使用 VQ-VAE motion token；
- 但引入粗粒度描述和细粒度 motion script 两套文本；
- 再加入两个辅助任务：
  - temporal localization；
  - 细粒度描述生成。

#### MG-MotionLLM 解决了什么

它不是在扩 codebook，而是在扩 supervision：

- 让文本不再只描述整段动作摘要；
- 而是能绑定到具体时间段和身体部位行为。

所以它实际上完成了句子级语义到局部时序语义的桥接。

#### MG-MotionLLM 的研究启发

如果想做“更可控的码本对齐”，不一定先改 tokenizer。

先构造 `time-span × body-part × text-span` 的 supervision，有时更关键。

---
## 第八类：与“码本扩充 / 组合控制”强相关的邻近工作

这一组论文不一定是最纯粹的 text-motion 语义对齐方法，但在“如何让离散动作表示承载更多可控语义”上非常有参考价值。

### Shape My Moves：离散动作 token + 连续体型参数联合生成

对应论文：[[paperAnalysis/Motion_Generation/CVPR_2025/2025_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions|Shape My Moves]]。

#### Shape My Moves 的相关点

- 动作用 SA-VAE 或 FSQ 量化为离散 token；
- 体型参数 `β` 作为连续条件注入解码器；
- 文本侧同时预测动作 token 和 `[BETA]` 特殊 token。

#### 为什么它值得看

这篇说明：

- “codebook 承载动作语义，连续向量承载额外属性语义”是可行的；
- 动作语义与体型语义不必都挤进一个离散码本里；
- 可以做离散-连续混合对齐。

### M3GPT：双空间联合优化值得单独记住

虽然前面已提到，但这里再强调一次：

- 离散 token loss 负责 token 级语义；
- 连续重建 loss 负责动作细节；
- 文本桥梁辅助任务负责跨模态迁移。

这可能是做下一代 codebook alignment 方法时最容易被忽视、但其实最重要的点之一。

---
## 逐篇映射：这些论文分别属于哪种对齐范式

### T2M-GPT

- 路径：[[paperAnalysis/Motion_Generation/CVPR_2023/2023_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete_Representations|T2M-GPT]]
- 主要范式：文本条件到单码本动作 token
- 是否是显式 codebook 路线：是
- 更适合作为：离散 text-to-motion 最简基线

### MotionGPT

- 路径：[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]
- 主要范式：词表扩充、统一语言化
- 是否是显式 codebook 路线：是
- 更适合作为：“motion as language”范式起点

### AvatarGPT

- 路径：[[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]
- 主要范式：码本映射、vocabulary adaptor
- 是否是显式 codebook 路线：是
- 更适合作为：motion token 接 LLM 的工程范式

### MoMask

- 路径：[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]
- 主要范式：码本扩充、RVQ
- 是否是显式 codebook 路线：是
- 更适合作为：高质量 motion tokenizer 与生成 backbone

### M3GPT

- 路径：[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation|M3GPT]]
- 主要范式：共享码本、文本桥梁、双空间联合优化
- 是否是显式 codebook 路线：是
- 更适合作为：跨模态共享 token 空间范式

### LaMP

- 路径：[[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]]
- 主要范式：显式预训练对齐、对比加匹配加双向生成
- 是否是显式 codebook 路线：是
- 更适合作为：“先学 alignment 再做生成”的代表

### The Language of Motion

- 路径：[[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]
- 主要范式：分部位码本、组合式码流
- 是否是显式 codebook 路线：是
- 更适合作为：部位级对齐和组合码本代表

### ReMoGPT

- 路径：[[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]
- 主要范式：part-level 检索增强对齐
- 是否是显式 codebook 路线：是
- 更适合作为：局部语义 exemplar 检索范式

### MG-MotionLLM

- 路径：[[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]
- 主要范式：粗细粒度桥接、localization、script
- 是否是显式 codebook 路线：是
- 更适合作为：supervision granularity 设计范式

### Being-M0.5

- 路径：[[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]
- 主要范式：分部位残差量化、实时可控
- 是否是显式 codebook 路线：是
- 更适合作为：part-aware RVQ 代表

### UDE

- 路径：[[paperAnalysis/Motion_Generation/CVPR_2023/2023_UDE_A_Unified_Driving_Engine_for_Human_Motion_Generation|UDE]]
- 主要范式：统一 codebook、模态无关映射
- 是否是显式 codebook 路线：是
- 更适合作为：多模态共享动作语义空间代表

### Shape My Moves

- 路径：[[paperAnalysis/Motion_Generation/CVPR_2025/2025_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions|Shape My Moves]]
- 主要范式：离散动作加连续属性联合对齐
- 是否是显式 codebook 路线：强相关
- 更适合作为：离散-连续混合条件设计参考

### MoLingo

- 路径：[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]
- 主要范式：InfoNCE 语义对齐 latent
- 是否是显式 codebook 路线：非纯 VQ
- 更适合作为：显式 semantic latent alignment 参考

---
## 如果专门围绕“码本拼接 / 映射 / 扩充”来重排

### 码本拼接 / 组合

严格来说，直接写“codebook concatenation”的论文并不算多，更多是以下几种等价或近似形式：

- 多部位码流组合：[[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]
- 部位乘以残差层级组合：[[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]
- 检索 exemplars 与 query token 拼接：[[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]
- 文本 token 与 pose 或 motion token 统一串接进词表序列：[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]、[[paperAnalysis/Motion_Generation/CVPR_2025/2025_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Generation_and_Editing|UniPose]]

如果要在自己论文中写“码本拼接”，建议更精确地表述为：

- `multi-codebook composition`
- `part-wise token stream composition`
- `retrieved code exemplar concatenation`
- `joint vocabulary serialization`

### 码本映射

最典型代表就是 [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]。

其次也可把以下工作看成广义映射：

- [[paperAnalysis/Motion_Generation/CVPR_2023/2023_UDE_A_Unified_Driving_Engine_for_Human_Motion_Generation|UDE]]：模态无关编码器把文本和音频映到统一 token 预测空间；
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions|Shape My Moves]]：`[BETA]` token 嵌入再映射到连续体型参数；
- [[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]]：把 text encoder 学成 motion-aware 的条件映射器。

### 码本扩充

代表最明确的是：

- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]：从单码本升级到 RVQ；
- [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]：part-aware residual quantization；
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions|Shape My Moves]]：用 FSQ 稳定离散化，并把属性语义外接到解码侧。

### 显式文本-动作空间对齐

最值得一起看的三篇是：

- [[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]]：预训练式显式对齐；
- [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]：InfoNCE 显式对齐 latent；
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]：通过脚本和定位任务做细粒度对齐。

---
## 更抽象的判断

### 判断 1：单一 codebook 的时代已经过去了

从 `T2M-GPT` 到 `MoMask`、`The Language of Motion`、`Being-M0.5`，趋势非常清楚：

- 要么多层残差量化；
- 要么分部位量化；
- 要么组合多个 token stream；
- 要么干脆离散-连续混合。

原因很简单：

- 粗粒度全身单码本很难承载细语义；
- 文本一旦更细，token 也必须更细。

### 判断 2：仅靠“text encoder + generator”已经不够了

后续真正强的方法，都在把 alignment 前置成独立模块或独立目标：

- LaMP：先学 motion-aware text encoder；
- MoLingo：先把 latent space 语义结构化；
- ReMoGPT：先检索局部 exemplar；
- MG-MotionLLM：先构造细粒度脚本与定位 supervision。

这说明领域共识已经从：

- “把文本喂给生成器”

转向：

- “先把文本语义变成 motion space 里真正可消费的结构”。

### 判断 3：未来最有价值的是“结构化码本 + 结构化监督 + 显式对齐损失”三者合流

如果要设计下一篇更强的工作，我会优先考虑这样的组合：

- 结构化码本：part-wise RVQ 或 shared-hierarchical codebook；
- 结构化监督：`time-span × body-part × text-span` 的 script 或 localization 数据；
- 显式对齐损失：contrastive、matching、retrieval-aware、preference-aware objective；
- LLM 接口：adaptor 或独立 motion head，而不是简单粗暴扩词表；
- 外部记忆：局部 exemplar 检索，缓解长尾动作问题。

这几乎就是把：

- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]] 的 adaptor；
- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]] 与 [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]] 的结构化码本；
- [[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]] 与 [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]] 的显式对齐；
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]] 与 [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]] 的细粒度监督和检索结合起来。

---
## 如果只保留最值得精读的 8 篇

### A. 词表扩充 / 统一语言化

- [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]

### B. 码本映射 / adaptor

- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]

### C. 码本扩充 / 高质量 tokenizer

- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]

### D. 共享 token 空间 / 跨模态迁移

- [[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation|M3GPT]]

### E. 显式预训练对齐

- [[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]]

### F. 分部位码本 / 组合式对齐

- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]

### G. 粒度桥接 / 时间段语义对齐

- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]

### H. 局部 exemplar / part-level 检索对齐

- [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]

---
## 可直接复用到你自己研究里的命题表述

### 命题 1

共享词表不是最优接口，adaptor 可能更优。

可引用脉络：`MotionGPT → AvatarGPT`。

### 命题 2

更细的 motion codebook 是更强 semantic alignment 的前提。

可引用脉络：`T2M-GPT → MoMask → Being-M0.5`。

### 命题 3

细粒度文本-动作对齐不能只靠句子级 caption，需要 body-part 和 time-span supervision。

可引用脉络：`MG-MotionLLM + ReMoGPT + The Language of Motion`。

### 命题 4

理想的 motion-language alignment 不应只在生成阶段发生，而应在 tokenizer、latent、retrieval、pretraining 各层共同发生。

可引用脉络：`LaMP + MoLingo + M3GPT`。

---
## 一个我认为最有潜力的组合方向

如果后面要单独写 idea，我会把它概括成：

**Part-aware shared RVQ codebook + motion-aware text encoder + span-part script supervision + retrieval-augmented adaptor LLM**。

拆开就是：

- `part-aware shared RVQ codebook`：借 [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]] 和 [[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]；
- `motion-aware text encoder`：借 [[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]]；
- `span-part script supervision`：借 [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]；
- `retrieval-augmented adaptor LLM`：借 [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]] 和 [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]。

这条路线的潜台词是：

- 不再把 alignment 看成单个 loss；
- 而把它理解为 tokenizer、memory、interface、supervision 四层同时设计的问题。

---
## 备注

### 哪些论文是“严格意义上的 VQ / codebook 路线”

最严格可归入的有：

- [[paperAnalysis/Motion_Generation/CVPR_2023/2023_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete_Representations|T2M-GPT]]
- [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]
- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_All_in_One_Framework_for_Motion_Understanding_Planning_Generation_and_Beyond|AvatarGPT]]
- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]
- [[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation|M3GPT]]
- [[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning|LaMP]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion|The Language of Motion]]
- [[paperAnalysis/Motion_Generation/AAAI_2025/2025_RemoGPT_Part_Level_Retrieval_Augmented_Motion_Language_Models|ReMoGPT]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]
- [[paperAnalysis/Human_Interaction/ICCV_2025/2025_Being_M0_5_A_Real_Time_Controllable_Vision_Language_Motion_Model|Being-M0.5]]
- [[paperAnalysis/Motion_Generation/CVPR_2023/2023_UDE_A_Unified_Driving_Engine_for_Human_Motion_Generation|UDE]]

### 哪些是“强相关但不完全是 codebook 主线”

- [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_Shape_My_Moves_Text_Driven_Shape_Aware_Synthesis_of_Human_Motions|Shape My Moves]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_UniPose_A_Unified_Multimodal_Framework_for_Human_Pose_Comprehension_Generation_and_Editing|UniPose]]

它们不一定是最标准的 VQ 文本到动作主线，但在“语义空间如何被结构化”上非常值得参考。
