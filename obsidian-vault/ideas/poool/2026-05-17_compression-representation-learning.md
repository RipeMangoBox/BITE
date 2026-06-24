---
title: "Compression, Decompression, and Representation Learning"
created: 2026-05-17T20:59:53+08:00
updated: 2026-05-17T20:59:53+08:00
status: seed
hypothesis: "把压缩的 rate-distortion / predictive coding / MDL 视角显式引入 motion-video 表示学习，可以更清楚地区分可预测结构、必须保留的任务变量和模型记忆。"
source_papers:
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation|MARDM]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]"
tags:
  - compression
  - representation_learning
  - motion_generation
  - visual_tokenization
  - context_compression
---
# 2026-05-17 Compression, Decompression, and Representation Learning

> [!abstract] Core note
> 无损压缩不是“丢失信息后再恢复”，而是构造一个更短但可逆的描述。对神经网络的启发不在于把所有学习都等同为压缩，而在于用码率、失真、条件熵、预测残差和 MDL 来约束表示是否真的抓住了可复用结构。

---
## 1. Idea decomposition and association

- Problem restatement:
  - 经典压缩把数据分成“可由模型/上下文解释的冗余”和“必须显式编码的剩余信息”。神经网络表示学习也面对同一个问题：latent/token 应该保留什么、压掉什么、什么时候需要可变容量。
  - 无损压缩要求 `Dec(Enc(x)) = x`，本质是可逆编码；多数神经生成和 tokenizer 是有损表示，只能在任务定义的失真度量下保真。
- Key elements:
  - 信息论：熵、条件熵、交叉熵、KL、rate-distortion、MDL。
  - 表示学习：autoencoder/VAE/VQ-VAE/BSQ/RVQ、latent bottleneck、entropy model、tokenizer。
  - 序列建模：predictive coding、next-token loss、context/KV compression、held-out compression。
  - 运动/视频：motion token、接触/相位/轨迹、长视频 token budget、复杂片段的可变码率。
- Multi-dimensional decomposition:
  - Task: image/video/audio compression, visual/audio tokenizer, long-context compression, text-to-motion generation.
  - Data: image/video/audio/text/motion；motion 的关键变量包括 contact、phase、body scale、trajectory、fine-grained part control。
  - Model: entropy-coded latent model, BSQ/tokenizer, adaptive token allocation, autoregressive prior, diffusion/flow decoder。
  - Evaluation: compression rate, reconstruction distortion, semantic alignment, held-out likelihood, downstream generation/control quality。

## 2. Real scenarios and pain points

- Typical scenarios:
  - 长视频/长动作生成中 token 数随长度线性增长，固定码率会浪费简单片段预算，也会压坏复杂交互片段。
  - 动作生成中 VQ/tokenizer 常用 reconstruction MSE 训练，但实际失败出现在接触、相位、局部细节、文本可控性。
  - 大模型长上下文推理中，KV/context compression 需要在显存、延迟和推理正确性之间做动态权衡。
- Existing solutions and pain points:
  - 固定长度 tokenizer 简单稳定，但没有按输入复杂度分配码率。
  - 纯 diffusion 生成强，但难解释哪些信息来自条件、哪些来自模型补全，难做“压缩域”诊断。
  - 只看训练集重构或 likelihood 容易混淆泛化和记忆；更可靠的是 held-out compression / composition split。

## 3. Related-work support and research opportunities

### 3.1 Related-work overview

- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation|MARDM]]: 本地 KB 已有分析。它直接指出离散 motion tokens 可能造成信息损失和多样性下降，支持“motion tokenizer 不能只看压缩率”的判断。
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]: 本地 KB 已有分析。它用多粒度 motion script 支持理解与生成，说明运动表示需要跨 coarse/fine 粒度组织信息。
- Fitted Neural Lossless Image Compression: 已加入 `analysis_log.csv` 并下载 PDF。它把每张图像的概率分布进行 overfitting，再做熵编码，适合作为“无损压缩 = 概率建模 + 可逆编码”的神经例子。
- Approaching Rate-Distortion Limits in Neural Compression with Lattice Transform Coding: 已加入并下载。它指出 latent scalar rounding 可能偏离最优向量量化，适合支撑“压缩瓶颈的形状也重要”。
- Image and Video Tokenization with Binary Spherical Quantization / ElasticTok / WavTokenizer: 已加入并下载。它们分别代表低熵离散视觉表示、可变 token 预算、音频离散 codec tokenizer。
- COMI / Contextual Semantic Anchors / Reasoning Meets Compression: 已加入并下载。它们把上下文压缩和模型压缩推到 reasoning 场景，适合作为“压缩不能只看平均保真，必须看关键能力损伤”的证据。

### 3.2 Support points

- 压缩质量等价于概率建模质量：`E[-log q(x)] = H(p) + KL(p || q)`，这把 next-token loss、entropy coding、held-out likelihood 放在同一框架下。
- 可变码率是自然需求：真实视频/动作复杂度不均匀，固定 token budget 会把 worst-case 预算浪费在简单片段上。
- 表示形状影响失真：不仅 latent 维度、码本大小重要，量化几何和残差路径也决定哪些变量被保留。
- 泛化可以用压缩诊断：能压训练集可能是记忆；能压 held-out 组合、未见动作组合或跨数据集片段，才更接近学到生成规律。

### 3.3 Research opportunities

- 可变码率 motion tokenizer:
  - 简单动作分配少 token，复杂接触、交互、手部细节分配更多 token。
  - 训练目标从 reconstruction MSE 扩展为 `R + λD + contact/phase/text-alignment`。
- Predict + residual motion generation:
  - 先预测低频意图、相位、轨迹，再只生成/编码不可预测残差。
  - 可把失败分析拆成“条件预测失败”还是“残差补全失败”。
- Held-out compression as memorization diagnostic:
  - 比较 train / nearest-neighbor / held-out composition 的码长、重构、生成相似度。
  - 用于 text-to-motion、dance generation、human-scene interaction 的泛化审计。
- Compression-aware context for motion-video MLLM:
  - 将 motion vector、residual、contact events、key poses 作为压缩域上下文，而不是全帧/全关节序列。

## 4. Frontier cross-domain techniques and validation ideas

- Neural lossless compression: [Fitted Neural Lossless Image Compression](https://openaccess.thecvf.com/content/CVPR2025/html/Zhang_Fitted_Neural_Lossless_Image_Compression_CVPR_2025_paper.html) 可作为“概率分布拟合 + entropy coding”的严格例子。
- Rate-distortion geometry: [Lattice Transform Coding](https://openreview.net/forum?id=Tv36j85SqR) 可迁移到 motion latent，检查 scalar quantization 是否损伤多关节相关结构。
- Adaptive tokenization: [ElasticTok](https://arxiv.org/abs/2410.08368) 提供可变 token 分配范式，可迁移到长动作/长视频。
- Visual/audio tokenizer: [BSQ](https://openreview.net/forum?id=eQJd5QkHgb) 和 [WavTokenizer](https://openreview.net/forum?id=yBlVlS2Fd9) 支持“离散 token 是跨模态 LLM 的接口”，但需要任务失真约束。
- Context compression: [COMI](https://openreview.net/forum?id=OGDIXDfaN4) 与 [Contextual Semantic Anchors](https://openreview.net/forum?id=8Pi6Du0n7F) 适合借鉴到 motion/video context selection。

## 5. Summary and next steps

- Core idea summary:
  - 压缩视角的核心价值是把“表示好不好”转化为可检验问题：在给定码率下，哪些任务变量被保留，哪些只是由 decoder 幻觉补全。
  - 对 motion/video，最有价值的不是追求无损，而是建立 task-aware rate-distortion：简单内容少码率，复杂接触/交互多码率，并用 held-out compression 区分记忆和泛化。
- Near-term executable steps:
  - 对现有 motion tokenizer 统计 token entropy、per-frame residual、contact/phase error，画 rate-distortion 曲线。
  - 设计 variable-rate motion tokenizer baseline：固定 token vs adaptive token，在 HumanML3D / MotionFix / interaction split 上比较。
  - 增加 held-out compression 诊断：训练集、近邻集、组合 held-out 的 NLL/码长和生成相似度分开报告。
- Potential target venue:
  - CVPR/ICCV: motion/video 表示与生成评估。
  - ICLR/NeurIPS: rate-distortion representation learning、context compression 和 MDL 泛化分析。
