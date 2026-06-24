---
created: 2026-03-25
topic: Motion Generation × Video/Image Generation × MLLM Cross-Domain Analogy
status: draft
updated: 2026-04-08T13:29
---
# 跨域对称：从 Video/Image Generation 与 MLLM 最新进展看 Motion Generation 的研究机会 — 2026-03-25

## 0. TL;DR

Video/Image Generation 领域已经完成了 "DiT + Rectified Flow + Scaling Law + Native Multimodal LLM" 的范式升级，而 Motion Generation 领域虽然开始跟进（HY-Motion、ScaMo、LLaMo），但在 **原生多模态统一架构、大规模数据-模型协同设计、以及 RL/推理增强生成** 三个方向上仍存在显著 gap。本文系统梳理跨域对称机会，评估各方向的能力上限与 CCF-A 审稿人认可度。

<!-- SECTION_BREAK_1 -->

## 1. 核心 Idea 与动机

### 问题定义

Motion Generation 领域正处于从 "小模型 + 小数据 + 单任务" 向 "大模型 + 大数据 + 多任务统一" 的范式转换期。Video/Image Generation 已经走完了这条路（Sora → HunyuanVideo → Wan2.1 → GPT-4o native image），而 Motion 领域的对称进展明显滞后 1-2 年。

### 为什么现在是做这个的好时机

1. **Video Generation 的技术栈已经成熟并开源**：DiT + Rectified Flow + Causal 3D VAE 的完整 pipeline 已有 HunyuanVideo (13B)、Wan2.1 (14B) 等开源实现，可以直接借鉴架构设计
2. **Motion 领域的 Scaling Law 刚刚被验证**：ScaMo (CVPR 2025) 首次证明 motion 的 autoregressive 模型遵循 power law scaling；HY-Motion 1.0 首次将 flow matching 扩展到 billion-scale
3. **MLLM 原生多模态生成范式刚刚出现**：GPT-4o native image generation (2025.03) 证明了 "理解 + 生成" 统一在一个 autoregressive transformer 中的可行性；LLaMo、MG-MotionLLM 开始在 motion 领域尝试
4. **RL/推理增强生成是全新方向**：Motion-R1 (2025) 首次将 decomposed CoT + RL binding 引入 motion generation，但仍处于非常早期阶段

<!-- SECTION_BREAK_2 -->

## 2. 跨域技术对称分析 (Cross-Domain Analogy)

### 2.1 源领域最新进展概览

#### Video Generation
- **HunyuanVideo** (Tencent, 13B params): Causal 3D VAE + Dual-stream→Single-stream DiT + 3D RoPE + Llama text encoder
- **HunyuanVideo 1.5** (8.3B): Selective & Sliding Tile Attention (SSTA) + 1080p super-resolution
- **Wan2.1** (Alibaba, 14B): DiT + Flow Matching + cross-attention text conditioning
- **FramePack** (NeurIPS 2025): Next-frame prediction + context packing for drift prevention

#### Image Generation
- **FLUX / SD3**: DiT + Rectified Flow 成为标准架构
- **UltraFlux**: Native 4K generation + Resonance 2D RoPE + Aesthetic Curriculum Learning
- **Self-Flow** (arXiv 2026.03): Self-supervised flow matching + Dual-Timestep Scheduling → multi-modal (image/video/audio) 统一

#### MLLM Native Generation
- **GPT-4o native image** (2025.03): Autoregressive transformer 原生生成图像，理解与生成统一
- **Janus-4o**: 开源复现，91K synthetic samples + 6h training
- **Interleaving Reasoning for Image Generation** (ICLR 2026): 推理与生成交织

### 2.2 对称映射表

| #   | 源领域技术                                         | Motion 领域对称                                   | 已有 Motion 工作                                   | Gap / 机会                                            |
| --- | --------------------------------------------- | --------------------------------------------- | ---------------------------------------------- | --------------------------------------------------- |
| 1   | **DiT + Rectified Flow (billion-scale)**      | DiT + Flow Matching for motion at scale       | HY-Motion 1.0, MotionFlux, DisCoRD             | HY-Motion 是工业界闭源；学术界缺乏开源 billion-scale motion DiT   |
| 2   | **Causal 3D VAE** (HunyuanVideo)              | Causal temporal motion VAE                    | COME (ICLR 2026), MotionStreamer               | Motion VAE 的 temporal causality 设计远不如 video VAE 成熟  |
| 3   | **Scaling Law 验证 + 数据-模型协同**                  | Motion scaling law + data curation pipeline   | ScaMo (CVPR 2025), Being-M0 (ICML 2025)        | 数据规模仍在 million-level，缺乏 video 级别的 data curation 方法论 |
| 4   | **Native multimodal LLM generation** (GPT-4o) | Motion-Language 原生统一模型                        | LLaMo, MG-MotionLLM, VersatileMotion           | 现有工作仍是 "LLM + motion tokenizer" 拼接，非原生统一            |
| 5   | **Interleaving Reasoning + Generation**       | CoT reasoning → motion generation             | Motion-R1, MoRL, IRG-MotionLLM                 | 极早期，reasoning 质量和 motion 质量的 binding 机制不成熟          |
| 6   | **RL from Human Feedback** (HY-Motion RLHF)   | Motion RLHF / preference optimization         | MotionCritic (ICLR 2025), SoPo (NeurIPS 2025)  | MotionCritic 提供了 reward model，但 RLHF pipeline 未完整验证 |
| 7   | **Multi-resolution / Progressive Training**   | Coarse-to-fine motion generation              | COME, TriC-Motion (ICLR 2026)                  | 缺乏 video 领域的 progressive resolution training 对应物    |
| 8   | **Consistency Model / Few-step Generation**   | Fast motion generation                        | MotionLCM (ECCV 2024), DART (ICLR 2025)        | 已有一定进展，但与 video 领域的 consistency distillation 差距大    |
| 9   | **Controllable generation (ControlNet-like)** | Fine-grained motion control                   | OmniControl, Kimodo (arXiv 2026), MotionLab    | 相对成熟，但缺乏 video ControlNet 级别的即插即用通用性                |
| 10  | **Data-Model Co-Design** (UltraFlux)          | Motion data quality + model architecture 联合优化 | The Quest for Generalizable Motion (ICLR 2026) | 刚开始被关注，是高价值方向                                       |

### 2.3 已有 Motion 工作覆盖度分析

- **覆盖较好的方向** (#8, #9): Controllable generation 和 fast generation 已有多篇 CCF-A 工作
- **刚起步的方向** (#1, #3, #6): Scaling + RLHF 有 1-2 篇先驱工作但远未饱和
- **几乎空白的方向** (#4, #5): Native multimodal unified model 和 reasoning-enhanced generation 在 motion 领域几乎是全新的

<!-- SECTION_BREAK_3 -->

## 3. 能力上限分析 (Capability Ceiling)

### 方向 A: Motion DiT + Rectified Flow at Scale

| 维度            | 评估                                                                                                                                                  |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **理论上限**      | 类比 HunyuanVideo，billion-scale motion DiT 应能覆盖 200+ motion categories，支持 open-vocabulary text-to-motion，FID/R-Precision 大幅超越现有 SOTA                  |
| **实际瓶颈**      | ① 高质量 motion 数据远少于 video（motion capture 成本高，目前最大 Being-M0 约 1M clips）；② 单卡训练 billion-scale 不现实，需要多机并行；③ 评估指标 (FID on HumanML3K) 已接近饱和，需要新 benchmark |
| **6 个月可达**    | 在 HumanML3K + MotionX 上训练 100M-500M 级 DiT，验证 scaling trend；不太可能达到 billion-scale                                                                     |
| **与 SOTA 差距** | HY-Motion 1.0 已经做了但未开源；学术界复现并超越的难度中等                                                                                                                |

### 方向 B: Native Multimodal Motion-Language Model

| 维度            | 评估                                                                                                                                                   |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **理论上限**      | 类比 GPT-4o，一个模型同时理解 text/motion/music/speech 并原生生成 motion，支持 multi-turn conversation + in-context learning                                            |
| **实际瓶颈**      | ① Motion tokenization 质量是核心瓶颈（discrete VQ 有量化损失，continuous 需要 flow matching head）；② 训练数据的 text-motion alignment 质量不够；③ 评估 "理解+生成" 统一能力缺乏标准 benchmark |
| **6 个月可达**    | 基于 LLaMo/MG-MotionLLM 的框架，在 7B LLM 上做 motion instruction tuning，验证 multi-task 能力                                                                     |
| **与 SOTA 差距** | LLaMo (CVPR 2025) 和 VersatileMotion 刚出，仍有大量改进空间                                                                                                      |

### 方向 C: Reasoning-Enhanced Motion Generation (Motion-R1 路线)

| 维度            | 评估                                                                                                                    |
| ------------- | --------------------------------------------------------------------------------------------------------------------- |
| **理论上限**      | 模型能像人类动画师一样 "先规划再执行"：分解复杂指令 → 规划关键帧 → 逐步生成 → 自我评估修正                                                                   |
| **实际瓶颈**      | ① CoT reasoning 的 ground truth 难以获取（需要动画师标注思维过程）；② RL reward 设计困难（MotionCritic 只评估整体质量，不评估 reasoning 质量）；③ 推理开销大，实时性差 |
| **6 个月可达**    | 在 Motion-R1 基础上改进 reward model + CoT 模板，在 complex motion (长序列、多动作组合) 上验证                                              |
| **与 SOTA 差距** | Motion-R1 和 MoRL 是仅有的两篇，方向极新，竞争少                                                                                      |

### 方向 D: Motion RLHF / Preference Optimization

| 维度            | 评估                                                                         |
| ------------- | -------------------------------------------------------------------------- |
| **理论上限**      | 类比 InstructGPT/DPO 对 LLM 的提升，RLHF 应能显著提升 motion 的 "人类感知质量"（自然度、流畅度、语义一致性）  |
| **实际瓶颈**      | ① MotionCritic 的 reward model 泛化性有限；② 人类偏好标注成本高；③ RL 训练不稳定                 |
| **6 个月可达**    | 基于 MotionCritic + DPO/SoPo 框架，在 1-2 个 base model 上验证 RLHF 提升               |
| **与 SOTA 差距** | MotionCritic (ICLR 2025) + SoPo (NeurIPS 2025) 已有基础，但完整 RLHF pipeline 未被验证 |

<!-- SECTION_BREAK_4 -->

## 4. CCF-A 审稿人认可度评估

### 方向 A: Motion DiT + Rectified Flow at Scale

| 维度                     | 评分        | 理由                                                                                                     |
| ---------------------- | --------- | ------------------------------------------------------------------------------------------------------ |
| **Novelty**            | 2.5/5     | DiT + Flow Matching 在 video 领域已成熟，motion 领域的 HY-Motion 已做过；纯 "搬运架构" 的 novelty 不足                       |
| **Technical Depth**    | 3/5       | 如果只是 scale up 没有 motion-specific 创新，技术深度有限；需要在 motion tokenization / temporal modeling 上有独特设计          |
| **Experimental Rigor** | 4/5       | Scaling law 实验本身就需要大量 ablation，容易做得扎实                                                                  |
| **潜在 Weakness**        | —         | "What is the novelty beyond applying existing video generation techniques to motion?"                  |
| **Rebuttal 策略**        | —         | 需要强调 motion-specific challenges（skeleton topology, physical plausibility, contact constraints）和对应的架构创新 |
| **推荐 Venue**           | CVPR/ICCV | 偏工程 + 实验驱动，适合 vision 会议                                                                                |

### 方向 B: Native Multimodal Motion-Language Model

| 维度                     | 评分           | 理由                                                                                                                              |
| ---------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **Novelty**            | 4/5          | "原生统一" 而非 "拼接" 是一个有说服力的 narrative；如果能证明 native 比 pipeline 好，novelty 很强                                                          |
| **Technical Depth**    | 4/5          | 需要解决 continuous motion representation + autoregressive generation 的技术难题，有深度                                                     |
| **Experimental Rigor** | 3.5/5        | 需要在 generation + understanding + editing 多个 task 上全面评估，实验量大                                                                     |
| **潜在 Weakness**        | —            | "How does this compare to simply using a better motion tokenizer with an existing LLM?"                                         |
| **Rebuttal 策略**        | —            | 需要 ablation 证明 native 统一 > tokenizer + LLM pipeline；展示 emergent capabilities (in-context motion editing, multi-turn refinement) |
| **推荐 Venue**           | NeurIPS/ICLR | 偏方法论创新，适合 ML 会议                                                                                                                 |

### 方向 C: Reasoning-Enhanced Motion Generation

| 维度                     | 评分           | 理由                                                                                                   |
| ---------------------- | ------------ | ---------------------------------------------------------------------------------------------------- |
| **Novelty**            | 4.5/5        | 极新方向，Motion-R1 是唯一先驱；"让模型先思考再生成 motion" 的 narrative 非常吸引人                                            |
| **Technical Depth**    | 3.5/5        | CoT + RL binding 的技术设计有深度，但 reward model 设计可能被质疑                                                     |
| **Experimental Rigor** | 3/5          | 缺乏标准 benchmark 评估 reasoning 质量；需要自建评估体系                                                              |
| **潜在 Weakness**        | —            | "How do you evaluate the quality of reasoning? Is the CoT actually helping or just adding overhead?" |
| **Rebuttal 策略**        | —            | 需要设计 reasoning quality metric；在 complex/compositional motion 上展示 CoT 的必要性                            |
| **推荐 Venue**           | ICLR/NeurIPS | 方法论创新 + 新 paradigm，适合 ML 顶会                                                                          |

### 方向 D: Motion RLHF / Preference Optimization

| 维度                     | 评分        | 理由                                                                                                            |
| ---------------------- | --------- | ------------------------------------------------------------------------------------------------------------- |
| **Novelty**            | 3.5/5     | RLHF 在 LLM/image 领域已成熟，但在 motion 领域的完整 pipeline 仍是新的                                                          |
| **Technical Depth**    | 3.5/5     | Reward model 设计 + RL 训练稳定性 + motion-specific preference 定义都有技术挑战                                              |
| **Experimental Rigor** | 4/5       | 可以做 human evaluation + automatic metrics 双重验证，实验设计清晰                                                          |
| **潜在 Weakness**        | —         | "MotionCritic already exists. What is new about your reward model?"                                           |
| **Rebuttal 策略**        | —         | 需要在 MotionCritic 基础上做 fine-grained reward (per-joint, per-segment)；或引入 pairwise preference 而非 pointwise score |
| **推荐 Venue**           | CVPR/ECCV | 偏应用驱动，human evaluation 是 vision 会议的强项                                                                         |

### 综合推荐排序（CCF-A 认可度 × 可行性）

1. **方向 C (Reasoning-Enhanced)** — 最高 novelty，竞争最少，但实验设计难度大
2. **方向 B (Native Multimodal)** — 高 novelty + 高 technical depth，但工程量大
3. **方向 D (Motion RLHF)** — 中等 novelty 但可行性最高，可以快速出结果
4. **方向 A (DiT at Scale)** — novelty 最低，需要大量计算资源，不适合学术组

<!-- SECTION_BREAK_5 -->

## 5. 知识库支撑分析 (Knowledge Base Support)

### 5.1 直接相关工作 (Importance S/A)

#### Scaling & Flow Matching
- **HY-Motion 1.0** [S] — Flow matching + DiT scaling to billion-scale, RLHF for motion
- **ScaMo** [S, CVPR 2025] — 首次验证 motion autoregressive model 的 scaling law
- **Being-M0** [S, ICML 2025] — Million-level motion data scaling
- **DART** [S, ICLR 2025] — Diffusion-based autoregressive real-time motion

#### MLLM + Motion
- **Motion-Agent** [S, ICLR 2025] — LLM conversational framework for motion generation
- **MG-MotionLLM** [A, CVPR 2025] — Multi-granularity motion comprehension + generation
- **LLaMo** [A, CVPR 2025] — Motion instruction tuning with LLM
- **SOLAMI** [S, CVPR 2025] — Social vision-language-action modeling

#### Reasoning & RL for Motion
- **Motion-R1** [A, arXiv 2025] — Decomposed CoT + RL binding for motion generation
- **MoRL** [B, arXiv 2026] — Reinforced reasoning for unified motion understanding/generation
- **IRG-MotionLLM** [B, arXiv 2025] — Interleaving generation, assessment, refinement
- **MotionCritic** [A, ICLR 2025] — Human perception-aligned motion reward model
- **SoPo** [B, NeurIPS 2025] — Semi-online preference optimization for motion

#### Unified / Generalist Models
- **MotionLab** [S, ICCV 2025] — Unified motion generation + editing via MCM paradigm
- **GENMO** [A, ICCV 2025] — Generalist model for human motion (NVIDIA)
- **COME** [A, ICLR 2026] — Advancing representation learning for text-to-motion
- **TriC-Motion** [A, ICLR 2026] — Causal diffusion framework
- **The Quest for Generalizable Motion** [S, ICLR 2026] — Data, model, evaluation 三位一体

#### Motion Representation
- **DisCoRD** [B, ICCV 2025] — Discrete tokens → continuous motion via rectified flow decoding
- **COME** [A, ICLR 2026] — Advanced representation learning
- **Language-Motion Pretraining** [S, ICLR 2025] — Motion-language alignment

### 5.2 间接相关工作 (Importance B/C)

#### Video/Image Generation (in KB)
- **FramePack** [B, NeurIPS 2025] — Next-frame prediction paradigm
- **Interleaving Reasoning for Image Generation** [B, ICLR 2026] — Reasoning + generation 交织
- **MotionStream** [A, ICLR 2026] — Real-time video generation with motion controls
- **MTVCraft** [A, ICLR 2026] — 4D motion tokenization for character animation
- **OmniHuman-1.5** [B, ICLR 2026] — Cognitive simulation for avatars

#### Motion Editing & Control (可作为下游验证)
- **Kimodo** [A, arXiv 2026] — Scaling controllable motion generation (NVIDIA)
- **FrankenMotion** [A, CVPR 2026] — Part-level motion generation and composition
- **MoLingo** [A, CVPR 2026] — Motion-language alignment

### 5.3 文献覆盖度评估

| 方向                      | KB 中相关论文数 | 覆盖度   | 评价                                                    |
| ----------------------- | --------- | ----- | ----------------------------------------------------- |
| Scaling + Flow Matching | 5-6 篇     | ★★★☆☆ | 核心工作已收录，但缺少 MotionFlux、DualFlow                       |
| MLLM + Motion           | 6-8 篇     | ★★★★☆ | 覆盖较好，VersatileMotion 未收录                              |
| Reasoning + RL          | 4-5 篇     | ★★★☆☆ | Motion-R1、MoRL 已收录，但 LLM reasoning 领域的通用工作未收录         |
| Video/Image Generation  | 3-4 篇     | ★★☆☆☆ | 仅收录了与 motion 直接相关的，缺少 HunyuanVideo、Wan2.1 等纯 video 工作 |

### 5.4 需要补充阅读的方向

1. **MotionFlux** (arXiv 2508.19527) — Rectified flow matching + preference alignment for motion
2. **DualFlow** (arXiv 2509.24099) — Unified multi-modal interactive motion via rectified flow
3. **VersatileMotion** (arXiv 2411.17335) — Unified motion synthesis + comprehension
4. **Self-Flow** (arXiv 2603.06507) — Self-supervised flow matching for multi-modal synthesis
5. **HunyuanVideo** (arXiv 2412.03603) — 了解 video DiT 的完整架构设计
6. **Janus-4o / ShareGPT-4o-Image** (arXiv 2506.18095) — 了解 native multimodal generation 的开源复现

<!-- SECTION_BREAK_6 -->

## 6. 技术路线与实验设计

### 6.1 推荐组合路线：Reasoning-Enhanced Native Motion-Language Model (方向 B+C 融合)

**核心 narrative**: 构建一个原生 Motion-Language Model，不仅能生成 motion，还能 "先推理再生成"——对复杂指令进行 decomposed reasoning，规划关键帧和动作序列，然后逐步生成并自我评估。

**为什么选 B+C 融合**:
- 单独做 B (native multimodal) 容易被质疑 "和 LLaMo/MG-MotionLLM 有什么区别"
- 单独做 C (reasoning) 容易被质疑 "reasoning 真的有用吗"
- 融合后的 narrative 更强："native 统一架构使得 reasoning 和 generation 可以在同一个 latent space 中交互，而非 pipeline 拼接"

### 6.2 Baseline 选择

| Baseline                 | 类型                 | 理由                            |
| ------------------------ | ------------------ | ----------------------------- |
| MoMask (CVPR 2024)       | Masked modeling    | 经典 discrete token baseline    |
| MLD (CVPR 2023)          | Latent diffusion   | 经典 continuous latent baseline |
| MotionGPT (NeurIPS 2023) | LLM + motion       | 早期 motion-language model      |
| MG-MotionLLM (CVPR 2025) | MLLM + motion      | 最新 multi-granularity baseline |
| Motion-R1 (arXiv 2025)   | Reasoning + motion | 最新 reasoning baseline         |

### 6.3 最小可行实验 (MVP)

**Phase 1 (2 周)**: Motion Tokenizer 验证
- 在 HumanML3K 上训练 continuous motion VAE (参考 COME 的设计)
- 对比 discrete VQ-VAE (MoMask) vs continuous VAE 的重建质量
- 指标: reconstruction FID, per-joint MPJPE

**Phase 2 (3 周)**: Native Motion-Language Model
- 基于 7B pretrained LLM (e.g., Qwen2.5-7B)
- 用 MoT (Mixture-of-Transformers) 架构接入 motion modality (参考 LLaMo)
- 训练 text-to-motion + motion captioning 双任务
- 指标: FID, R-Precision, BLEU (captioning)

**Phase 3 (3 周)**: Reasoning Enhancement
- 构造 reasoning 训练数据：用 GPT-4 对 complex motion descriptions 生成 CoT decomposition
- 训练模型在生成 motion 前先输出 reasoning tokens
- 对比 w/ reasoning vs w/o reasoning 在 compositional motion 上的表现
- 指标: compositional accuracy, FID on complex prompts

### 6.4 完整实验矩阵

| 实验                            | 数据集                        | 指标                                   | 目的            |
| ----------------------------- | -------------------------- | ------------------------------------ | ------------- |
| Text-to-Motion                | HumanML3K, KIT-ML          | FID, R-Precision, MM-Dist, Diversity | 基础生成质量        |
| Motion Captioning             | HumanML3K                  | BLEU, ROUGE, CIDEr                   | 理解能力          |
| Compositional Motion          | HumanML3K (complex subset) | Compositional accuracy, FID          | Reasoning 效果  |
| Long-form Motion              | MotionX                    | FID, transition smoothness           | 长序列能力         |
| Multi-turn Editing            | 自建                         | Edit accuracy, preservation rate     | 交互能力          |
| Ablation: w/ vs w/o reasoning | HumanML3K                  | FID, R-Precision                     | Reasoning 必要性 |
| Ablation: native vs pipeline  | HumanML3K                  | FID, latency                         | 架构优势          |
| Human Evaluation              | 100 samples                | Naturalness, text-alignment (1-5)    | 人类感知质量        |

<!-- SECTION_BREAK_7 -->

## 7. 风险与缓解策略

| #   | 风险                                                  | 严重度 | 缓解方案                                                                                                                  |
| --- | --------------------------------------------------- | --- | --------------------------------------------------------------------------------------------------------------------- |
| 1   | **Reasoning 数据质量差** — GPT-4 生成的 CoT 可能不符合动画师的真实思维过程 | 高   | ① 邀请 2-3 位动画专业学生标注 50 条 gold CoT 作为 seed；② 用 seed 做 few-shot prompting 提升 GPT-4 生成质量；③ 设计 reasoning quality filter    |
| 2   | **Continuous motion representation 训练不稳定**          | 中   | ① 先用 COME 的 pretrained VAE 做 warm start；② 如果 continuous 不行，fallback 到 discrete + rectified flow decoding (DisCoRD 路线) |
| 3   | **7B LLM 的 motion generation 质量不够**                 | 中   | ① 先在 3B 上做 proof-of-concept；② 如果 7B 不够，考虑 MoE 架构 (参考 HMVLM 的 MoE LoRA)                                                |
| 4   | **计算资源不足**                                          | 中   | ① MVP 阶段只用 HumanML3K (14K clips)，不需要大规模数据；② 用 LoRA/QLoRA 微调而非全量训练                                                     |
| 5   | **同期竞争** — LLaMo、VersatileMotion 等工作可能在投稿前发表        | 高   | ① 核心差异化在 reasoning enhancement，这是它们没有的；② 保持对 arXiv 的持续监控                                                              |
| 6   | **评估 reasoning 质量缺乏标准**                             | 中   | ① 自建 compositional motion benchmark (参考 SINC 的 simultaneous action 设定)；② 设计 reasoning faithfulness metric             |

## 8. Next Steps (按优先级排序)

### 立即执行 (本周)
1. **补充阅读** MotionFlux、DualFlow、VersatileMotion、Self-Flow 四篇论文，更新 knowledge base
2. **确认技术路线** — 决定走 B+C 融合路线还是单独做 D (RLHF)，后者风险更低但 novelty 也更低

### 短期 (1-2 周)
3. **Motion VAE 实验** — 在 HumanML3K 上训练 continuous motion VAE，对比 COME 和 MoMask 的 tokenizer
4. **Reasoning 数据构造** — 用 GPT-4 对 HumanML3K 的 complex descriptions 生成 CoT decomposition，评估质量

### 中期 (3-4 周)
5. **Native Motion-Language Model MVP** — 基于 Qwen2.5-7B + MoT 架构，训练 text-to-motion + captioning
6. **Reasoning Enhancement** — 在 MVP 基础上加入 reasoning tokens，对比 compositional motion 效果

### 长期 (5-8 周)
7. **完整实验** — 跑完实验矩阵，准备 paper
8. **Human Evaluation** — 100 samples 的人类评估

---
## 附录：关键参考文献速查

| 简称              | 全称                                                  | Venue            | 与本 idea 的关系       |
| --------------- | --------------------------------------------------- | ---------------- | ----------------- |
| HY-Motion       | HY-Motion 1.0: Scaling Flow Matching for T2M        | Tech Report 2025 | 方向 A 的工业界先驱       |
| ScaMo           | Exploring the Scaling Law in AR Motion Generation   | CVPR 2025        | Scaling law 验证    |
| Being-M0        | Scaling Motion Generation with Million-Level Data   | ICML 2025        | 数据 scaling        |
| LLaMo           | Human Motion Instruction Tuning                     | CVPR 2025        | 方向 B baseline     |
| MG-MotionLLM    | Multi-Granularity Motion Comprehension & Generation | CVPR 2025        | 方向 B baseline     |
| Motion-R1       | Decomposed CoT + RL Binding for Motion              | arXiv 2025       | 方向 C 先驱           |
| MoRL            | Reinforced Reasoning for Motion                     | arXiv 2026       | 方向 C 相关           |
| MotionCritic    | Aligning Motion with Human Perceptions              | ICLR 2025        | 方向 D reward model |
| SoPo            | Semi-Online Preference Optimization for Motion      | NeurIPS 2025     | 方向 D preference   |
| COME            | Advancing Representation Learning for T2M           | ICLR 2026        | Motion VAE 参考     |
| DisCoRD         | Discrete Tokens → Continuous via Rectified Flow     | ICCV 2025        | Tokenization 参考   |
| VersatileMotion | Unified Motion Synthesis & Comprehension            | arXiv 2025       | 方向 B 竞争者          |
| MotionFlux      | Rectified Flow + Preference for Motion              | arXiv 2025       | 方向 A+D 交叉         |
| IRG (Image)     | Interleaving Reasoning for Image Generation         | ICLR 2026        | 方向 C 的 image 领域对应 |
| GPT-4o native   | Native Image Generation in GPT-4o                   | OpenAI 2025      | 方向 B 的 image 领域对应 |






