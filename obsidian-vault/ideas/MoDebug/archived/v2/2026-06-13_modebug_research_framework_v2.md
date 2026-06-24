---
title: "MoDebug Research Framework v2: From CFG-CA Tuning to Mechanistic Interpretability of Motion Generators"
created: 2026-06-13T18:00:00+08:00
updated: 2026-06-13T18:00:00+08:00
status: active_framework
hypothesis: >
  Text-to-motion flow/diffusion models exhibit functional specialization across layers, denoising steps,
  and attention heads — some components govern semantic alignment (text→motion mapping), others govern
  motion quality (temporal coherence, physical plausibility), and others handle part-level coordination.
  Systematically mapping this specialization enables principled, multi-mechanism interventions that
  improve controllability and quality beyond single-point CFG tuning.
tags:
  - MoDebug
  - mechanistic_interpretability
  - motion_generation
  - layer_specialization
  - guidance_mechanisms
  - research_framework
source_papers:
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation]]"
  - "[[analysis/ICLR_2025/CFG_Manifold_constrained_Classifier_Free_Guidance_for_Diffusion_Models]]"
  - "[[analysis/ICLR_2025/Eliminating_Oversaturation_and_Artifacts_of_High_Guidance_Scales_in_Diffusion_Models]]"
  - "[[analysis/CVPR_2025/TCFG_Tangential_Damping_Classifier_free_Guidance]]"
  - "[[analysis/CVPR_2026/C2FG_Control_Classifier_Free_Guidance_via_Score_Discrepancy_Analysis]]"
  - "[[analysis/CVPR_2026/CFG_Ctrl_Control_Based_Classifier_Free_Diffusion_Guidance]]"
  - "[[analysis/CVPR_2026/ParTY_Part_Guidance_for_Expressive_Text_to_Motion_Synthesis]]"
  - "[[analysis/CVPR_2026/TempoControl_Temporal_Attention_Guidance_for_Text_to_Video_Models]]"
  - "[[analysis/CVPR_2024/NoiseCLR_A_Contrastive_Learning_Approach_for_Unsupervised_Discovery_of_Interpretable_Directions_in_Diffusion_Models]]"
  - "[[analysis/NEURIPS_2024/Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controller]]"
  - "[[analysis/ICLR_2026/DiffusionBlocks_Block_wise_Neural_Network_Training_via_Diffusion_Interpretation]]"
  - "[[analysis/ICLR_2026/Activation_Steering_with_a_Feedback_Controller]]"
  - "[[analysis/arxiv_2025/CFG_Zero_Improved_Classifier_Free_Guidance_for_Flow_Matching_Models]]"
  - "[[analysis/CVPR_2026/FlowMotion_Training_Free_Flow_Guidance_for_Video_Motion_Transfer]]"
  - "[[analysis/CVPR_2024/Rethinking_the_Spatial_Inconsistency_in_Classifier_Free_Diffusion_Guidance]]"
  - "[[analysis/arxiv_2024/Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training_free_Editing]]"
---

# MoDebug Research Framework v2: From CFG-CA Tuning to Mechanistic Interpretability of Motion Generators

> [!abstract] 一句话定位
> MoDebug 不是"给 MoLingo 调 CFG 参数"，而是**以 MoLingo 为首个显微镜，系统揭示 text-to-motion flow/diffusion 模型内部组件（层、去噪步、注意力头）的功能分工，并据此设计 principled interventions 来提高运动质量和文本跟随能力**。旧版 CFG-CA 实验不是失败，而是提供了第一组约束条件和探针靶点。

---

## 1. 旧版路线的根本问题

旧版文档（[[2026-06-13_molingo_evidence_and_related_work_reassessment]]）存在三个结构性缺陷：

### 1.1 问题一：机制空间坍缩为 CFG-CA 单点

旧版所有实验围绕 MoLingo 的 `CFG_CA` hidden state 做 intervention，路线被压缩为：
- 换 L15/L10 的 CFG_CA → 观察 FID 变化
- 用 cosine gate 加权 CFG_CA → gate 退化为常数
- APG/norm clamp 在 hidden space → 失败

这不是 MoDebug 应该有的机制空间。MoDebug 的核心目标是**理解 motion generator 的共性规律并设计共性策略**，而 CFG_CA 只是 MoLingo 的一个具体实现细节。正确的机制空间应该覆盖：

| 机制轴 | 可以做什么 | 跨域依据 |
|--------|-----------|---------|
| **什么被干预** | hidden states, attention maps, velocity predictions, denoised latents, score estimates | MOFT 证明不同表示空间编码不同信息；TCFG 证明 score 的方向分解有意义 |
| **在哪里干预** | 特定层、特定去噪步、特定 attention head、特定 token position | C2FG 证明 step-dependent guidance；ParTY 证明 part-dependent 建模 |
| **如何干预** | 缩放、旋转/投影、mask、添加 steering vector、重路由 | CFG++ 用插值替代外推；CFG-Ctrl 用滑模控制替代线性增益 |
| **干预目标** | 全局 FID、文本对齐、部件可控、时间可控、属性强调 | TempoControl 控制时序；ParTY 控制部件 |

### 1.2 问题二："能力先行"的倒置逻辑

旧版 §4.1 定义 T1-T4 能力 demo（时间区间控制、身体部件控制等），然后要求图谱为这些 demo 服务。这种"先定义产品功能再做科学"的思路适合工程交付，不适合 ICLR 级别的科研。

ICLR reviewer 期待的叙事是：
1. **发现现象** → 模型不同组件有功能分工（科学贡献）
2. **提出机制** → 基于分工设计针对性干预（方法贡献）
3. **展示能力** → 干预自然产生可控性（能力是机制的副产物）

而非：
1. ~~先定义想要什么能力~~
2. ~~为能力收集最小图谱~~
3. ~~图谱转干预~~

### 1.3 问题三：MoLingo 单点依赖

旧版承认需要多 baseline 但两周计划中 Phase 8 才做迁移，且只有"如果 D1/D2 成立"才进入。这意味着整个路线图建立在 MoLingo 单一模型上，一旦跨模型迁移失败，全部工作降级为 case study。

---

## 2. 已有实验的重新定位

旧实验不是失败，而是提供了**约束条件**和**第一组探针靶点**。

### 2.1 作为约束条件的负结果

| 观察 | 约束 | 科学含义 |
|------|------|---------|
| L15 direct replacement → FID 7.70（崩坏） | **L15 不可直接替换** | L15 承担关键功能，可能是 motion quality 的"守护层" |
| L10 replacement → FID 3.65（接近 baseline 3.59） | **L10 是安全干预点** | 浅层对 CFG_CA 操作鲁棒，可能主要处理低层特征 |
| L11-L13 mild degradation, L14 pre-collapse, L15 cliff | **层敏感性连续递增** | 不是单层异常，而是 late-layer 系统性更敏感 |
| Cosine gate 退化为常数（0.90-0.97） | **简单 gate 无动态信息** | CFG_CA 的 layer-wise 差异不足以支撑 adaptive gating |
| APG hidden hook 失败（FID 4.82） | **hidden space 不是正确的分解空间** | APG 的方向分解需要在 velocity/score 空间做，不是 hidden state |
| Norm clamp 失败（FID 5.12） | **简单压范数不是充分机制** | L15 的问题不是范数过大，而是语义信号结构被破坏 |

### 2.2 作为探针靶点的正向线索

| 观察 | 数据 | 可转化为 |
|------|------|---------|
| L15 fixed-scale a0.9 → FID 3.38（优于 baseline 3.59） | 3-seed mean | **L15 存在更好的 scaling 点**，说明 CFG 外推在这些层过度 |
| L15 replace cliff 幅度 ~4.1 FID | 3.59→7.70 | **effect size 足够大**，是理想的 causal probe target |
| Layer sensitivity 单调性 | L11<L12<L13<L14<<L15 | **连续谱**而非二值分类，说明逐层功能渐变 |

### 2.3 旧实验的核心科学价值

这些实验已经完成了 MoDebug 的第一阶段：**在 MoLingo 上建立了一个可靠的 causal observation** —— late-layer CFG_CA 干预存在从 mild degradation 到 cliff 的连续敏感性谱，且 fixed-scale substitution 在 a0.9 处越过 baseline 给出更优指标。这不是"调参成功"，也不是"实验失败"，而是**一个需要被解释的科学现象**。

下一步的科学问题是：**为什么 late layer 更敏感？L15 究竟在做什么导致替换即崩坏？fixed-scale a0.9 为什么优于 baseline？**

---

## 3. 核心科学假设：Layer Specialization Hypothesis

### 3.1 假设陈述

> **Layer Specialization Hypothesis (LSH)**：在 text-to-motion flow/diffusion 模型中，不同层在去噪过程中承担不同功能角色。具体而言：
> - **Shallow layers（≈L1-L10）**：主要处理 motion 的低层结构（姿态几何、帧间平滑），对语义条件信号的变化相对鲁棒。
> - **Middle layers（≈L11-L14）**：逐步将文本语义条件映射到 motion 表示空间，是 text→motion alignment 的"翻译层"。
> - **Deep layers（≈L15+）**：执行最后的 motion quality 精调（物理合理性、细节协调），对条件信号的扰动极度敏感——因为这些层需要在强条件信号和 motion prior 之间做精确平衡。
>
> 如果此假设成立，那么：
> - L15 cliff 的原因是该层在条件信号和 motion prior 的平衡被 replace 操作破坏
> - fixed-scale a0.9 改善的原因是将过度外推的 CFG 拉回到更合理的插值点
> - 浅层的鲁棒性是因为它们处理的 motion 结构与条件信号的耦合较弱

### 3.2 假设的科学意义

这个假设将 MoDebug 从"MoLingo 调参"升级为"理解 motion generator 的内部工作机制"。如果 LSH 在多个 backbone 上成立，那么它就成为一个**跨模型的科学发现**，而不仅是 MoLingo 的单点观察。

类比：
- **CV 领域**：StyleGAN 的 style space 有层级分工（粗层控制姿态，中层控制形状，细层控制纹理）
- **NLP 领域**：Transformer 的不同层处理不同粒度的语言特征（浅层语法，深层语义）
- **MoDebug 的 LSH**：Motion generator 的不同层在 text→motion 生成管道中有功能分工

### 3.3 如何验证 LSH

验证 LSH 需要的不是"跑更多 CFG_CA 替换实验"，而是**设计因果探针**来测量每层在具体功能维度上的贡献：

| 探针类型 | 测量目标 | 方法 |
|---------|---------|------|
| **Semantic alignment probe** | 该层对 text-motion 对齐的贡献 | 对该层 activation 加噪声/ablated，测量 R-Precision 退化 |
| **Motion quality probe** | 该层对运动质量（FID）的贡献 | 对该层做 intervention，测量 FID 变化（已有 L11-L15 数据） |
| **Part specialization probe** | 该层对不同身体部件的选择性 | 分别 mask arms/legs/torso 相关维度，测量各部分 motion 退化 |
| **Temporal probe** | 该层对帧间时序的贡献 | 对该层做 temporal shuffle，测量 motion jerkiness 变化 |
| **Score direction probe** | 该层 cond/uncond score 的方向关系 | 类似 TCFG，测量该层 SVD 谱和法向/切向对齐度 |

---

## 4. 机制设计空间：超越 CFG-CA 的四轴框架

MoDebug 的机制设计不应绑定在 CFG_CA hidden state 上，而应在四个轴上展开。每个轴的每个机制选项都有跨域依据。

### 4.1 轴一：干预空间（What to intervene on）

| 空间 | 为什么有意义 | 跨域依据 | MoLingo 中对应 |
|------|------------|---------|---------------|
| **Score/Velocity space** | CFG 的数学定义在此空间；方向分解（法向/切向）在此有几何意义 | TCFG（SVD 分解）、CFG++（外推→插值）、APG（parallel/orthogonal 分解） | Flow velocity $v_\theta(x_t, t, c)$ |
| **Hidden/Residual space** | 层间信息流的主要载体；旧实验对此空间已有测量 | DiffusionBlocks（残差=去噪步骤）、PID Steering（层间误差控制） | MoLingo 的 hidden states / CFG_CA |
| **Attention space** | 交叉注意力直接编码 text→motion token 对齐；自注意力编码帧间依赖 | TempoControl（时间注意力控制）、MotionCLR（cross-attention 编辑） | MoLingo 的 cross-attention / self-attention maps |
| **Latent/Output space** | 最接近最终 motion 的表示，直接控制运动属性 | FlowMotion（$z_0$ hat probe）、MOFT（输出端运动特征提取） | MoLingo 的 denoised latent / decoder output |

**关键决策**：旧版只在 Hidden space 做 intervention。新版至少需要在 Score space 和 Attention space 同时展开。

### 4.2 轴二：干预位置（Where to intervene）

| 维度 | 粒度选项 | 依据 |
|------|---------|------|
| **Layer** | 单层 / 层组（shallow/mid/deep）/ 全层统一 | 旧实验已证明 layer-dependent sensitivity |
| **Denoising step** | 单步 / 阶段（early/mid/late）/ 全步统一 | C2FG 证明 score discrepancy 随 step 指数衰减 |
| **Attention head** | 单头 / 头组 / 全头统一 | MotionCLR 证明不同 head 编码不同 motion 属性 |
| **Text token** | 单 token / token 组（verb/noun/adverb）/ 全 token | TempoControl 证明不同 token 的 attention 可独立控制 |
| **Body part / Joint** | 单关节 / part 组（arms/legs/torso）/ 全身 | ParTY 证明 part-level modeling 可行且有效 |

**关键决策**：旧版只在 layer 维度做 intervention（L10/L15 replace）。新版至少需要 step × layer 的二维探针。

### 4.3 轴三：干预算子（How to intervene）

| 算子类型 | 具体操作 | 跨域依据 | 适用场景 |
|---------|---------|---------|---------|
| **Scaling** | 对目标表示乘以系数 α | 旧版 fixed-scale substitution | 调整某层/某步的条件信号强度 |
| **Direction decomposition** | SVD/PCA 分解后保留/丢弃特定方向 | TCFG（法向保留/切向阻尼） | 去除不对齐的噪声方向 |
| **Interpolation** | 在 cond 和 uncond 之间做插值而非外推 | CFG++（λ∈[0,1] 替代 ω>1） | 防止 off-manifold |
| **Mask/Sparsify** | 对特定维度/token/帧施加 mask | TempoControl（帧级 attention mask） | 时间/部件选择性控制 |
| **Steering vector** | 添加预计算的引导向量 | PID Steering（I 项消除稳态误差） | 持续偏向目标属性 |
| **Feedback control** | 使用 P/PID/SMC 控制器动态调整 | CFG-Ctrl（滑模控制）、PID Steering | 需要闭环稳定的场景 |
| **Gradient-based optimization** | 对 latent 做梯度步以优化目标函数 | TempoControl（对 $z_t$ 做梯度优化）、MOFT | 精细控制（计算开销大） |

### 4.4 轴四：干预时机（When to intervene）

| 时机 | 操作 | 优点 | 缺点 |
|------|------|------|------|
| **Inference-time only** | 不改模型权重，只改前向过程 | 即插即用、可跨模型 | 控制精度有限、计算开销 |
| **Post-training** | 对特定层做轻量微调/LoRA/权重插值 | 持久效果、无推理开销 | 需要训练数据、可能过拟合 |
| **Pre-training** | 在训练阶段加入辅助损失/架构改进 | 根本性改进 | 训练成本高、不适用于已训练模型 |

**关键决策**：旧版只做 inference-time。对于 ICLR 级别的贡献，至少需要展示 inference-time + post-training 两条路径，或者说明为什么 inference-time 方法有独特优势（无需训练、可跨模型）。

---

## 5. 新实验路线图

路线图的设计原则：
1. **科学问题驱动**，不是能力 demo 驱动
2. **每个阶段产出可独立的 partial claim**，降低全路线风险
3. **多 baseline 尽早介入**（Phase 3 即引入第二模型）
4. **机制空间逐步展开**，不一次铺开所有轴

### Phase 1: Layer Specialization Hypothesis 验证（Week 1-2）

**核心问题**：不同层在 text→motion 生成中是否有功能分工？

**实验**：

| # | 实验 | 方法 | 产出 |
|---|------|------|------|
| 1.1 | Layer-wise semantic ablation | 对 MoLingo 每层 hidden state 加噪声/置零，测量 R-Precision 和 CLIP-Score 退化曲线 | **Semantic sensitivity profile**：哪些层对 text-motion alignment 关键 |
| 1.2 | Layer-wise quality ablation | 对每层做不同程度的 scaling（0.5/0.7/0.9/1.0/1.1），测量 FID 变化 | **Quality sensitivity profile**：哪些层对 motion quality 关键 |
| 1.3 | Layer-wise part ablation | 对每层各 body part 维度分别做 mask，测量各 part 的 motion error | **Part specialization matrix**：每层是否对不同 part 有偏好 |
| 1.4 | Step × Layer joint probe | 选择 5 个关键层 × 5 个去噪步，做 scaling intervention，测量 FID + R-Precision | **Step-Layer sensitivity heatmap**：确认 step 和 layer 是否有交互效应 |
| 1.5 | Score direction analysis | 在每层提取 cond/uncond score，做 SVD 分解，计算法向/切向对齐度 | **Layer-wise score geometry**：确认哪些层存在 TCFG 式的切向不对齐 |

**通过条件**：
- 至少 MoLingo 上不同层的 sensitivity profile 有显著差异（statistical test）
- Step × Layer heatmap 显示非均匀模式（不是所有 step 所有层一样）
- 如果所有层 profile 趋同，则 LSH 不成立，需要重新考虑方向

**风险**：如果 MoLingo 上层间差异不够显著（全层 sensitivity profile 相似），则 LSH 可能不成立。此时转向"step specialization"或"model-agnostic CFG improvement"。

### Phase 2: 基于 LSH 的机制设计（Week 3-4）

**核心问题**：利用 LSH 发现，能否设计比 uniform CFG 更好的 intervention？

**实验**：

| # | 实验 | 方法 | 产出 |
|---|------|------|------|
| 2.1 | Layer-conditioned CFG schedule | 根据 Phase 1.1/1.2 的 profile，为每层设置不同的 CFG scale：高 sensitivity 层用小 scale，低 sensitivity 层用大 scale | **Layer-wise CFG** baseline |
| 2.2 | Step-conditioned CFG schedule | 受 C2FG 启发，early step 强引导、late step 弱引导（或反之），基于 Phase 1.4 heatmap 设计 | **Step-wise CFG** baseline |
| 2.3 | Score direction damping | 对 Phase 1.5 发现切向不对齐的层，应用 TCFG 式切向阻尼 | **Layer-wise TCFG for motion** |
| 2.4 | Interpolation vs extrapolation | 对 late layer（L14-L15），用 CFG++ 式插值（λ∈[0,1]）替代外推（ω>1） | **CFG++ adaptation for motion** |
| 2.5 | Combined schedule | 组合 2.1+2.2：layer-wise + step-wise 联合 schedule | **Combined guidance** |
| 2.6 | Ablation: component contribution | 逐一移除 layer schedule、step schedule、direction damping，测量退化 | 各组件的独立贡献 |

**通过条件**：
- 至少一种 layer/step-conditioned 方法在 FID 上优于 uniform CFG（≥3 seeds）
- 不引入明显的 R-Precision 退化（不能 trade alignment for quality）
- 组件消融显示非平凡贡献（不只是找到了更好的 uniform scale）

### Phase 3: 跨模型迁移与共性验证（Week 5-6）

**核心问题**：MoLingo 上的发现是模型特异的还是 motion generator 的共性？

**实验**：

| # | 实验 | 方法 | 产出 |
|---|------|------|------|
| 3.1 | Second backbone LSH verification | 选择第二个 text-to-motion 模型（MDM/MoMask/MLD），重复 Phase 1.1-1.4 的核心探针 | 第二模型的 sensitivity profile |
| 3.2 | Profile comparison | 比较两个模型的 layer sensitivity profile、step-layer heatmap | **共性模式**（如 late-layer sensitivity）vs 模型特异模式 |
| 3.3 | Cross-model mechanism transfer | 将 Phase 2 最优方法迁移到第二模型，直接应用或微调参数 | 跨模型效果 |
| 3.4 | Failure analysis | 如果迁移失败，分析哪些 profile 特征不同导致方法不兼容 | 理解方法的适用边界 |

**通过条件**：
- 至少一个核心发现（如 late-layer sensitivity）在两个模型上一致
- 迁移方法在第二模型上有同向效果（不要求同等幅度）
- 如果不能迁移，必须能解释"为什么 MoLingo 特殊"，并降级为 case study

### Phase 4: 可控性作为机制的副产物（Week 7-8）

**核心问题**：基于分工的干预是否自然产生细粒度可控性？

注意：这里的可控性不是预先定义的目标，而是机制的自然结果。例如：
- 如果发现某些层对 arm motion 有选择性（Phase 1.3），那么对这些层做 part-specific scaling 就自然产生部件控制
- 如果发现 cross-attention 在特定 step 对特定 token 敏感，那么对这些 step 做 token-specific attention modulation 就自然产生词汇级控制

| # | 实验 | 方法 | 产出 |
|---|------|------|------|
| 4.1 | Emergent part control | 基于 Phase 1.3 part specialization matrix，对高选择性层做 part-specific scaling | 能否只增强右臂运动而不影响左腿 |
| 4.2 | Emergent temporal control | 基于 Phase 1.4 heatmap，对特定 step 做 frame-masked guidance | 能否控制动作的时间位置 |
| 4.3 | Emergent attribute control | 如果发现某些层对不同运动属性（速度/幅度）敏感，做属性-specific 干预 | 能否让 "run" 变快而不变成其他动作 |
| 4.4 | Control precision metrics | 设计定量指标：target part activation、非目标 part drift、root stability | 控制精度量化 |

**通过条件**：
- 至少一种可控性来自机制发现而非手工设计
- 可控性不显著破坏全局 FID（可以有轻微 tradeoff，但不能 collapse）

### Phase 5: Post-Training 路线（Week 9-10，P1）

**核心问题**：inference-time 的发现能否转化为 post-training 的持久改进？

| # | 实验 | 方法 |
|---|------|------|
| 5.1 | Layer-specific LoRA | 对 Phase 1 发现的关键层做轻量 LoRA fine-tune，目标是最小化 cond/uncond score discrepancy |
| 5.2 | Activation steering vector | 从 Phase 2 最优 intervention 中提取 steering pattern，训练一个 lightweight steering network |
| 5.3 | Post-trained model evaluation | 评估 post-training 后的模型在 zero-shot 上的表现对比 inference-time 方法 |

### 暂缓/不做

- ❌ 继续旧版 cosine gate 网格搜索
- ❌ 在 hidden space 重做 APG
- ❌ 全量 layer-step-token-part atlas（做图谱必须回答明确科学问题）
- ❌ 在没有 LSH 验证前定义"能力 demo"

---

## 6. ICLR 叙事架构

### 6.1 推荐的核心叙事

```
Title: Understanding and Improving Text-to-Motion Generators via Layer-wise Functional Probing

1. Introduction
   - Text-to-motion 模型越来越强（MoLingo 等），但我们不理解它们内部如何工作
   - 现有工作要么是"更强的架构"（MoLingo/ParTY），要么是"更复杂的 CFG"（CFG++/TCFG）
   - 缺失的是：理解不同组件（层/步/头）在 text→motion 管道中的功能角色
   
2. Layer Specialization Hypothesis
   - 提出假设：不同层承担不同功能
   - 设计因果探针来验证
   
3. Probing Methodology
   - Layer-wise semantic/quality/part/temporal ablation
   - Step × Layer joint intervention
   - Score direction analysis (SVD-based)
   
4. Discoveries
   - Late-layer sensitivity cliff（MoLingo: L15 FID +4.1 on replacement）
   - Layer sensitivity continuum（not binary）
   - [跨模型一致性发现]
   - [Part specialization pattern]
   
5. Mechanism Design
   - 基于发现的 layer-conditioned CFG
   - 基于发现的 step-conditioned schedule
   - 基于 score geometry 的方向阻尼
   - [可控性的自然涌现]
   
6. Results
   - MoLingo: FID improvement + R-Precision preservation
   - Second model: transfer results
   - Ablation: component contributions
   - Fine-grained evaluation (part-level, temporal)

7. Analysis & Limitations
   - 为什么 late layer 更敏感（可能的解释）
   - MoLingo 特异性 vs 共性
   - 计算开销
   - 未覆盖的模型类型（VQ-based, GPT-based）
```

### 6.2 叙事的关键 claim 层级

| Claim 层级 | 内容 | 需要的证据 |
|-----------|------|-----------|
| **C1 (核心)** | Motion generator 的不同层有功能分工 | ≥2 个模型的 layer sensitivity profile 有显著差异 |
| **C2 (核心)** | 基于分工的干预优于 uniform 干预 | ≥1 个指标上 layer/step-conditioned > uniform CFG |
| **C3 (增强)** | 这个分工在多个 backbone 上一致 | ≥2 个模型有一致的 late-layer sensitivity |
| **C4 (增强)** | 分工理解自然导致可控性 | ≥1 个可控性 demo 来自 probe 发现而非手工设计 |
| **C5 (可选)** | 发现可转化为 post-training 改进 | post-training 方法在 zero-shot 上优于 baseline |

ICLR 的最低门槛：C1 + C2 必须坚固。C3 显著增强说服力。C4/C5 是锦上添花。

### 6.3 与已有工作的差异化

| 维度 | CFG++ / TCFG / C2FG / CFG-Ctrl | ParTY / TempoControl / MotionCLR | MoDebug (ours) |
|------|-------------------------------|----------------------------------|----------------|
| **目标** | 改进 CFG 机制本身 | 实现特定可控性（部件/时间） | **理解模型内部功能分工** |
| **方法** | 修改 CFG 公式 | 修改生成架构或添加引导模块 | **因果探针 + 机制适配** |
| **范围** | 通用图像/视频生成 | Motion-specific 可控性 | **Text-to-motion 的内部机理** |
| **贡献** | 更好的采样质量 | 更好的可控性 | **理解 + 干预的统一框架** |

MoDebug 的独特贡献不是"更好的 CFG"或"更强的可控性"，而是**first systematic map of functional specialization in text-to-motion generators**。CFG 改进和可控性是这张地图的自然应用，不是独立贡献。

---

## 7. 机制适配库：从跨域工作到 MoDebug 的具体路径

### 7.1 CFG-Ctrl → Layer-wise PID Guidance

CFG-Ctrl 将 CFG 建模为 P-controller，并用 SMC 替代。MoDebug 可以更进一步：

**适配**：不是对整个模型用一个 controller，而是**每层一个 PID controller**，每层的 error signal 来自该层的 cond/uncond score discrepancy。浅层（鲁棒）用大增益，深层（敏感）用小增益 + 强 damping。

**实验**：Phase 2 的 layer-conditioned CFG 即此路线的第一步。

### 7.2 TCFG → Layer-wise Score Geometry Analysis

TCFG 在整体 score 上做 SVD。MoDebug 可以：

**适配**：**逐层做 SVD**，测量每层 cond/uncond score 的法向对齐度。如果 L15 的法向对齐度显著低于浅层，就找到了 L15 cliff 的几何解释——late layer 的 score 方向更混乱，直接 replace 破坏了脆弱的法向结构。

**实验**：Phase 1.5 即此路线。

### 7.3 TempoControl → Cross-Attention as Probe and Control Interface

TempoControl 用交叉注意力的时间曲线控制概念时序。MoDebug 可以：

**适配**：**逐层提取 cross-attention maps**，分析不同层对不同 text token 在哪些帧上的 attention 分布。这可以作为 layer specialization 的另一个证据维度——如果某些层的 attention 更集中（负责精确对齐），某些层更分散（负责全局一致性）。

**实验**：作为 Phase 1 的补充探针。不急于做控制，先用 attention 模式作为 LSH 的证据。

### 7.4 NoiseCLR → Unsupervised Discovery of Motion Semantics Directions

NoiseCLR 在噪声预测差异上做对比学习发现语义方向。MoDebug 可以：

**适配**：在 motion generator 的不同层提取 cond/uncond score difference，做对比学习，发现每层编码了哪些运动语义方向（如"快/慢"、"大/小幅度"、"手臂/腿部"）。这可以直接验证 LSH：如果不同层发现的语义方向不同，就证明了功能分工。

**实验**：可作为 Phase 1 的高级探针（P1，需要一定计算量）。

### 7.5 PID Steering → Layer-wise Error Accumulation Control

PID Steering 用 PID controller 逐层积累误差信号。MoDebug 可以：

**适配**：在 multi-step denoising 中，对每层维护一个积分项，积累该层在前几步的 cond/uncond discrepancy。如果某层的积分项持续增长，说明该层存在系统性的条件信号偏差，需要特别处理。

**实验**：Phase 2 的高级版本（P1）。

### 7.6 ParTY → Part Specialization as Natural Property

ParTY 显示 part-level modeling 可行。MoDebug 的 LSH 预测：

**假设**：不需要显式设计 part-level 架构（像 ParTY 那样），**模型内部自然存在 part specialization**——某些层/head 天然更关注 arm，某些更关注 leg。如果这个假设被 Phase 1.3 验证，那么 part-controllable generation 就是机制的自然副产物，而不是需要专门架构的功能。

这将是 MoDebug 相比 ParTY 的独特贡献：ParTY 说"我们可以做 part control"，MoDebug 说"我们可以解释为什么模型内部已经有了 part specialization，并利用它做 control"。

---

## 8. 风险评估与应对

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| **LSH 不成立**：所有层 sensitivity profile 相似 | 低 | 致命 | 转向 step specialization 或 model-agnostic CFG improvement |
| **MoLingo 特异性**：第二模型 profile 完全不同 | 中 | 严重 | 降级为 "Understanding MoLingo" case study，仍可投稿但需缩小 claim |
| **Layer-conditioned CFG 不优于 uniform** | 中 | 严重 | 转向 attention-based 或 score-decomposition 机制 |
| **LSH 成立但无法转化为改进** | 中低 | 严重 | 至少 "understanding" 本身就是 ICLR-worthy 的科学贡献 |
| **计算开销过大** | 中 | 中等 | 限制探针粒度，选择代表性层/步而非全量 |
| **Reviewer 认为 incremental** | 高 | 中等 | 重点强调"first systematic map"定位和跨域连接 |

---

## 9. 与旧版文档的关系

本文档**替代**（不是补充）[[2026-06-13_molingo_evidence_and_related_work_reassessment]] 中的 §3-§7。

保留旧文档的：
- §1（旧实验数据，重新解释为约束和探针靶点）
- §2（相关工作，重新组织为机制库）
- §8（一句话版本）

废弃旧文档的：
- §3（旧方案定位）→ 替换为本文档 §3（LSH）和 §6（叙事架构）
- §4（目标驱动机制适配）→ 替换为本文档 §4（四轴框架）和 §5（新路线图）
- §5（两周路线）→ 替换为本文档 §5（八周路线图）
- §6（ICLR 门槛）→ 替换为本文档 §6.2（claim 层级）和 §8（风险评估）
- §7（推荐阅读）→ 已整合到本文档 §7（机制适配库）

---

## 10. 即刻行动项（本周）

1. **Phase 1.1 探针实现**：写 MoLingo layer-wise semantic ablation 代码。最小版本：选 5 个层（L1/L5/L10/L14/L15），每层加 3 个 noise level，跑 1 seed，看 R-Precision 退化曲线是否存在 layer-dependent pattern。
2. **Phase 1.5 探针实现**：在 MoLingo 的 5 个层提取 cond/uncond velocity predictions，做 SVD 分解，计算法向对齐度。
3. **第二 baseline 选型**：确定第二个 text-to-motion 模型（建议 MDM 或 MLD，因为开源且架构不同于 MoLingo 的 autoregressive flow）。
4. **MoLingo 代码深读**：确认 cross-attention maps、hidden states、velocity predictions 的提取接口，确认 layer naming convention。

---

## Appendix A: 关键论文速查

| 论文 | 核心机制 | MoDebug 适配 |
|------|---------|-------------|
| CFG++ (ICLR 2025) | 外推→插值，重噪声用无条件估计 | Late-layer interpolation |
| TCFG (CVPR 2025) | SVD 分解 score，阻尼切向分量 | Layer-wise score geometry |
| C2FG (CVPR 2026) | Score discrepancy 指数衰减，time-dependent schedule | Step-conditioned schedule |
| CFG-Ctrl (CVPR 2026) | 滑模控制替代线性 CFG | Layer-wise PID/SMC guidance |
| NoiseCLR (CVPR 2024) | 对比学习发现 noise space 语义方向 | Layer-wise semantic direction discovery |
| MOFT (NeurIPS 2024) | 视频扩散特征中提取纯净运动通道 | Output-side motion probe |
| TempoControl (CVPR 2026) | 交叉注意力时间信号控制 | Cross-attention as probe |
| ParTY (CVPR 2026) | 部件先行+整体融合 | 验证 part specialization 是否天然存在 |
| DiffusionBlocks (ICLR 2026) | 残差块=扩散去噪步骤 | 层角色解释的理论框架 |
| PID Steering (ICLR 2026) | PID 控制替代 P 控制消除稳态误差 | Layer-wise error accumulation |
