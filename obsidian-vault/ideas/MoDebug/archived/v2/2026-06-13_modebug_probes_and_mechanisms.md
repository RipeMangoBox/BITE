---
title: "MoDebug 探针方法与机制设计：从发现分工到利用分工"
created: 2026-06-13T19:00:00+08:00
updated: 2026-06-13T19:00:00+08:00
status: active_design
hypothesis: >
  Motion generator 的层分工不能靠加噪来理解（加噪只测脆弱性，不揭示功能）。
  需要一组因果探针来分别测量每层在语义对齐、运动质量、部件协调、时序结构上的功能角色。
  探针结果直接映射到具体干预策略：哪些层调 CFG、哪些层调 attention、哪些层做 steering、哪些层做 post-training。
tags:
  - MoDebug
  - probes
  - causal_intervention
  - CFG_design
  - attention_modulation
  - activation_steering
supplements: "[[2026-06-13_modebug_research_framework_v2]]"
---

# MoDebug 探针方法与机制设计

> [!abstract] 核心问题
> v2 框架（[[2026-06-13_modebug_research_framework_v2]]）定义了 Layer Specialization Hypothesis 和五阶段路线图，
> 但在探针方法和机制实现上不够具体。本文档回答三个问题：
> 1. **怎么探**：除了加噪，如何因果地测量每层的功能角色？
> 2. **探完怎么用（CFG）**：探针结果如何转化为具体的 layer/step-conditioned CFG？
> 3. **除了 CFG 还能做什么**：分工理解还能催生哪些非 CFG 的干预机制？

---

## 1. 探针方法论：从"加噪测脆度"到"因果测功能"

### 1.0 为什么加噪不够

加噪（noise injection / activation ablation）只回答一个问题：**"破坏这层会不会让模型变差？"**

这混淆了两个维度：
- **重要性**（importance）：这层对最终输出有多大因果影响
- **功能性**（function）：这层具体编码了什么信息

两层可以同等"重要"但功能完全不同：L3 可能编码关节角度分布的统计约束（破坏后 motion 不自然），L15 可能编码条件信号和运动先验的平衡（破坏后条件失效）。加噪无法区分这两种情况。

需要一组能**分别测量不同功能维度**的探针。

### 1.1 探针分类

```
探针类型                   测量的功能维度              方法性质
─────────────────────────────────────────────────────────
Counterfactual Swap        信息内容（这层编码了什么）    因果
Linear Decode              可解码信息（这层能被读出什么）  关联
Intervention Response      因果效应（改这层会影响什么）    因果
Score Geometry             方向结构（这层的梯度空间）      几何
Attention Pattern          信息路由（这层关注什么）        结构
```

### 1.2 探针一：Counterfactual Activation Swap（核心探针）

**原理**：用两个相关但不同的输入（prompt A 和 prompt B）分别做 forward pass，然后在 forward pass B 的某一层插入 forward pass A 的 activation，测量输出变化。

**为什么优于加噪**：加噪问的是"没有这层会怎样"，swap 问的是"把这层的 A 信息注入 B 会怎样"——后者直接测量该层编码的信息内容和因果效力。

**Motion 领域的三种 Swap 设计**：

| Swap 类型 | Prompt Pair 设计 | 测量目标 |
|-----------|-----------------|---------|
| **Semantic Swap** | A="a person walks", B="a person runs" | 该层是否编码动作类别信息？swap L 的 activation 后，B 的输出是否变得更像 "walk"？ |
| **Part Swap** | A="right hand waves", B="left hand waves" | 该层是否编码部件侧向信息？swap 后，输出是否从右手变左手？ |
| **Attribute Swap** | A="run fast", B="run slowly" | 该层是否编码运动属性（速度/幅度）？swap 后，B 的速度是否改变？ |
| **Quality Swap** | A=高 FID 样本的 activation, B=低 FID 样本的 activation | 该层是否编码运动质量信息？swap 后，B 的 FID 是否改善/恶化？ |

**具体实现**（以 Semantic Swap 为例）：

```python
# 1. 生成 paired motions（用不同 prompt，同样 noise）
z_T = torch.randn(...)  # 固定的初始噪声
motion_A, cache_A = model.forward_with_cache(z_T, prompt="a person walks")
motion_B, cache_B = model.forward_with_cache(z_T, prompt="a person runs")

# 2. 逐层 swap 并测量效应
for layer_idx in range(num_layers):
    # 在 prompt B 的 forward 中，把 layer_idx 的 activation 换成 A 的
    motion_swapped = model.forward_with_patched_activation(
        z_T, prompt="a person runs",
        patch_layer=layer_idx,
        patch_source=cache_A.activations[layer_idx]
    )
    
    # 3. 测量 swap 效应
    semantic_shift = distance(motion_swapped, motion_A)  # 向 A 靠近多少
    quality_retention = fid(motion_swapped)               # 质量是否保持
    
    # 记录该层的 causal effect
    results[layer_idx] = {
        "semantic_influence": semantic_shift,  # 越大 → 该层编码语义
        "quality_impact": quality_retention     # 变化越大 → 该层影响质量
    }
```

**产出**：每层的 **Semantic Influence Score** 和 **Quality Influence Score**。理想情况下，middle layers（~L8-L12）在 semantic swap 中影响力最大，deep layers（~L14-L15）在 quality swap 中影响力最大。

### 1.3 探针二：Linear Decoding（辅助探针）

**原理**：在每层 activation 上训练线性回归器/分类器，预测不同的 motion 属性。可解码性（R² 或 accuracy）越高，说明该层编码了该信息。

**为什么有用**：不同于 swap（因果），linear decode 是关联性的，但它更高效（一次 forward 可收集所有层的 training data），且可以同时测量多个属性维度。

**Decode 目标设计**：

| Decode 目标 | 标签来源 | 含义 |
|------------|---------|------|
| Per-joint velocity (regression) | 生成 motion 的关节点速度 | 该层编码了多少细粒度关节运动信息 |
| Body part activation (classification) | 哪组关节（arm/leg/torso）位移最大 | 该层是否对特定身体部件有偏好 |
| Frame index (regression) | 帧序号 / 标准化时间戳 | 该层编码了多少时序位置信息 |
| Action class (classification) | 动作类别标签 | 该层编码了多少高层语义信息 |
| Motion attribute (regression) | 速度/幅度/加速度 | 该层编码了多少运动属性信息 |
| Text token identity (classification) | 当前帧对应的文本 token | 该层在多模态对齐中的角色 |

**具体实现**：

```python
# 1. 收集数据：对 1000 个 prompts 各生成 1 条 motion
dataset = []
for prompt in prompt_set:
    motion, cache = model.forward_with_cache(z_T, prompt)
    for layer_idx, activation in enumerate(cache.activations):
        # activation: (seq_len, hidden_dim) for each layer
        for frame_idx, frame_act in enumerate(activation):
            dataset.append({
                "layer": layer_idx,
                "activation": frame_act,
                "frame_idx": frame_idx,
                "joint_velocities": motion.velocity[frame_idx],
                "action_class": action_label,
                "body_part_active": which_part_moves_most(motion[frame_idx]),
            })

# 2. 逐层训练 linear probes
for layer_idx in range(num_layers):
    layer_data = [d for d in dataset if d["layer"] == layer_idx]
    
    # Probe A: 能读出多少关节运动信息？
    r2_joint[layer_idx] = train_linear_regression(
        X=layer_data.activations, y=layer_data.joint_velocities
    ).r2_score
    
    # Probe B: 能读出多少动作类别信息？
    acc_action[layer_idx] = train_linear_classifier(
        X=layer_data.activations, y=layer_data.action_class
    ).accuracy
    
    # Probe C: 能读出多少时序信息？
    r2_time[layer_idx] = train_linear_regression(
        X=layer_data.activations, y=layer_data.frame_idx
    ).r2_score
```

**产出**：每层的 **Joint Info Curve**、**Semantic Info Curve**、**Temporal Info Curve**。理想情况下：
- 浅层：高 joint info + 高 temporal info（编码运动结构）
- 中层：高 semantic info（编码动作类别）
- 深层：中等 joint info + 低 semantic info（精细调整，不再编码粗粒度语义）

### 1.4 探针三：Intervention Response Curve（因果探针）

**原理**：对目标层施加不同强度的 scaling intervention，测量每条 motion property 的 dose-response 曲线。

**为什么优于简单加噪**：加噪是 binary 的（正常/破坏），response curve 是 continuous 的，可以揭示非单调关系。

**具体设计**：

```python
# 对每层，做 7 个 scaling level × N 个属性
scale_levels = [0.5, 0.7, 0.9, 1.0, 1.1, 1.3, 1.5]

for layer_idx in range(num_layers):
    for scale in scale_levels:
        motion = model.forward_with_scaled_activation(
            z_T, prompt, layer=layer_idx, scale=scale
        )
        results[layer_idx][scale] = {
            "FID": evaluate_fid(motion),
            "R-Precision": evaluate_r_precision(motion),
            "arm_error": evaluate_part_error(motion, part="arms"),
            "leg_error": evaluate_part_error(motion, part="legs"),
            "jerk": evaluate_motion_smoothness(motion),
        }
```

**Response curve 的形状揭示了该层的功能角色**：

| 曲线形状 | FID response | R-Precision response | 功能解释 |
|---------|-------------|---------------------|---------|
| **Flat** | 不随 scale 变化 | 不随 scale 变化 | 该层对该属性无因果影响 |
| **Monotonic increasing** | scale↑ → FID↓（质量提升） | scale↑ → R-Prec↑ | 该层直接增强该属性 |
| **Monotonic decreasing** | scale↑ → FID↑（质量退化） | scale↑ → R-Prec↓ | 过度激活该层破坏该属性 |
| **U-shaped** | scale=1.0 处最优 | scale=1.0 处最优 | 该层有精确的最优点（常态已最优） |
| **Asymmetric U** | scale<1 时退化严重 | scale>1 时退化严重 | 该层对该方向敏感（如 L15 的 scale>1 侧） |

**旧版实验的对照**：
- L15 的 FID response curve 在 scale=1.0 替换（等价于 scale=0 for original signal）时崩坏 → L15 的 curve 是强烈的 monotonic decreasing 或 asymmetric U
- L10 的 curve 接近 flat → L10 对 FID 无强因果影响
- fixed-scale a0.9 优于 baseline → L15 的 FID curve 在 scale=1.0 并非最优点

### 1.5 探针四：Score/Velocity Direction Geometry（几何探针）

**原理**：在每层测量条件速度 $v_c$ 和无条件速度 $v_\emptyset$ 的方向关系。类似 TCFG，但逐层进行。

**具体设计**：

```python
for layer_idx in range(num_layers):
    # 提取该层的 cond/uncond velocity（在 flow matching 中即去噪网络的输出）
    v_c = model.get_velocity_at_layer(z_t, t, condition="text", layer=layer_idx)
    v_unc = model.get_velocity_at_layer(z_t, t, condition=None, layer=layer_idx)
    
    # 1. 方向对齐度
    cos_sim = cosine_similarity(v_c, v_unc)
    
    # 2. 范数比
    norm_ratio = ||v_c|| / ||v_unc||
    
    # 3. SVD 分解（类似 TCFG，在 batch 维度上收集该层的 velocity 矩阵）
    V_c = collect_velocities(v_c, num_samples=100)  # (100, d)
    V_unc = collect_velocities(v_unc, num_samples=100)
    
    U_c, S_c, Vt_c = svd(V_c)
    U_unc, S_unc, Vt_unc = svd(V_unc)
    
    # 法向对齐度（高奇异值对应方向的对齐程度）
    normal_alignment = cosine_similarity(U_c[:, :k], U_unc[:, :k])  # top-k 奇异向量
    
    # 切向发散度（低奇异值方向的对齐程度）
    tangential_divergence = 1 - cosine_similarity(U_c[:, k:], U_unc[:, k:])
    
    results[layer_idx] = {
        "cosine_sim": cos_sim,
        "norm_ratio": norm_ratio,
        "normal_alignment": normal_alignment,
        "tangential_divergence": tangential_divergence,
    }
```

**产出**：每层的 **Normal Alignment Score** 和 **Tangential Divergence Score**。

**解读**：
- 如果 L15 的法向对齐度显著低于浅层（且切向发散度高）→ L15 的 cond/uncond velocity 方向更混乱 → L15 cliff 的一个几何解释
- 如果某层的 norm_ratio 远偏离 1.0 → 该层的条件信号过强或过弱
- **干预方向**：对法向对齐度低的层做 TCFG 式切向阻尼；对 norm_ratio 异常的层做 rescaling

### 1.6 探针五：Cross-Attention Functional Mapping（结构探针）

**原理**：提取每层、每个 attention head 对 text tokens 的 attention 分布，分析其功能偏好。

**为什么关键**：Cross-attention 是 text→motion 信息流的**直接物理通道**。如果理解了哪些 head、哪些层在关注哪些 token 类型，就可以直接操控信息流。

**具体设计**：

```python
# 对每个 prompt 的每个 token 标注类型
token_labels = {
    "a": "article", "person": "subject", "walks": "verb",
    "quickly": "adverb", "right": "part_side", "hand": "body_part",
    "waves": "verb", "fast": "attribute"
}

for layer_idx in range(num_layers):
    for head_idx in range(num_heads):
        # 提取该 head 的 cross-attention 分布
        attn_weights = cache.cross_attn[layer_idx][head_idx]  # (frames, tokens)
        
        # 计算该 head 对各 token 类型的平均关注度
        for token_type in ["verb", "body_part", "adverb", "attribute"]:
            type_tokens = [t for t, label in token_labels.items() if label == token_type]
            type_attention = attn_weights[:, type_tokens].mean()
            results[layer_idx][head_idx][token_type] = type_attention
        
        # 计算 attention 的时间集中度
        temporal_entropy = entropy(attn_weights.mean(dim=1))  # 低熵=集中在特定帧
        results[layer_idx][head_idx]["temporal_concentration"] = temporal_entropy
```

**产出**：每层每头的 **Token-Type Attention Profile** 和 **Temporal Concentration Score**。

**解读**：
- 有些 head 主要关注 verb → "动作选择器"
- 有些 head 主要关注 body_part → "部件定位器"
- 有些 head 主要关注 attribute → "属性调制器"
- 有些 head 低 temporal entropy → "时序控制器"（只在特定帧激活）

### 1.7 探针优先级

| 优先级 | 探针 | 理由 |
|-------|------|------|
| **P0（必须做）** | Counterfactual Swap (§1.2) | 最直接的因果证据，直接回答"每层编码什么" |
| **P0（必须做）** | Intervention Response (§1.4) | 直接测量因果效应，且与后续干预设计直接挂钩 |
| **P1（强烈建议）** | Score Geometry (§1.5) | 为 CFG 变体（TCFG 式阻尼、CFG++ 式插值）提供依据 |
| **P1（强烈建议）** | Cross-Attention (§1.6) | 为 attention-based 干预提供依据，是区别于纯 CFG 路线的关键 |
| **P2（有时间做）** | Linear Decode (§1.3) | 关联性证据，辅助解释，但不是因果性的核心证据 |

---

## 2. 从探针到 CFG：具体实现路径

### 2.1 探针结果如何转化为 CFG 设计

CFG 的标准形式：$v_{guided} = v_\emptyset + \omega (v_c - v_\emptyset)$，其中 $\omega$ 是全局标量。

MoDebug 的核心改进：**$\omega$ 不再是全局标量，而是探针结果的函数**。

#### 2.1.1 Layer-Conditioned CFG：$\omega \rightarrow \omega(l)$

**依据**：Intervention Response Curve (§1.4) 的 FID response 和 R-Precision response。

**推导**：

对每层 $l$，Intervention Response 给出了 FID$(l, \omega)$ 和 R-Prec$(l, \omega)$ 的曲线。layer-conditioned CFG 的目标是找 $\omega(l)$ 使得：

$$\omega^*(l) = \arg\min_\omega \text{FID}(l, \omega) \quad \text{s.t.} \quad \text{R-Prec}(l, \omega) \geq \text{R-Prec}_{baseline}$$

具体实现分两步：

```python
# Step 1: 从探针结果中提取每层的 safe scale range
for layer_idx in range(num_layers):
    # FID response curve 中 FID 不显著恶化的 scale 范围
    safe_range = find_safe_range(
        scale_levels, fid_curve[layer_idx],
        tolerance=0.05  # FID 退化不超过 5%
    )
    # 在该范围内选最优 scale（如最大化 R-Precision）
    optimal_scale[layer_idx] = argmax_within_range(
        r_prec_curve[layer_idx], safe_range
    )

# Step 2: 在 CFG 采样中应用
def layer_conditioned_cfg(z_t, t, text_embed, omega_l):
    v_c = model.velocity(z_t, t, text_embed)
    v_unc = model.velocity(z_t, t, None)
    
    # 逐层 blend，每层用不同的 omega
    v_guided = v_unc  # start from unconditional
    for l in range(num_layers):
        delta_l = model.get_layer_contribution(v_c, l) - model.get_layer_contribution(v_unc, l)
        v_guided_l = model.get_layer_contribution(v_unc, l) + omega_l[l] * delta_l
        # 将 guided 结果注入该层的 forward
        ...
    
    return v_guided
```

**预期**：基于旧版实验数据，L10 的 safe_range 较宽（可用高 ω），L15 的 safe_range 较窄（ω 需接近 1.0，或 < 1.0 如 a0.9）。

#### 2.1.2 Step-Conditioned CFG：$\omega \rightarrow \omega(t)$

**依据**：Score Geometry (§1.5) 在不同 denoising step 的重测。C2FG 已经证明 cond/uncond score discrepancy 随 step 指数衰减。

**具体设计**：

在 5 个代表性 denoising step（t=0, 0.25T, 0.5T, 0.75T, T）上重做 Intervention Response 和 Score Geometry。如果发现：

- Early step（高噪声）：cond/uncond divergence 小 → 需要更高 ω 来放大弱条件信号
- Late step（低噪声）：cond/uncond divergence 大 → 需要更低 ω 防止过度条件化

则设计：

$$\omega(t) = \omega_0 \cdot \exp\left(\lambda \cdot \frac{t}{T}\right)$$

其中 $\lambda$ 从探针数据拟合。

**与 C2FG 的区别**：C2FG 的衰减函数是通用的指数衰减。MoDebug 的衰减函数是 **motion-specific** 的——从 motion generator 的 actual layer-step response 数据拟合而来。

#### 2.1.3 Joint Layer-Step CFG：$\omega \rightarrow \omega(l, t)$

**依据**：§1.4 和 §1.5 在多个 step 上的联合测量。

**矩阵结构**：

```
            t=0   t=0.25T  t=0.5T  t=0.75T  t=T
Layer 1-5   高     高       中       低       低
Layer 6-10  很高   很高     高       中       低
Layer 11-13 中     中       中       中       中
Layer 14    低     低       低       很低     很低
Layer 15    很低   很低     很低     很低     很低
```

**解读**：
- 浅中层（1-10）在 early/mid step 可用高 ω：这些层在这些步承担语义翻译
- 深层（14-15）在所有步都应使用保守 ω：这些层是质量关隘
- 中层（11-13）在所有步保持中等 ω：持续参与对齐但不过度

**实现**：$\omega(l, t)$ 是一个 2D lookup table，从探针数据插值得到。

#### 2.1.4 Direction-Conditioned CFG（TCFG 适配）

**依据**：Score Geometry (§1.5) 的 normal_alignment 和 tangential_divergence。

**设计**：对 normal_alignment 低的层，不直接使用 $v_c - v_\emptyset$，而是先投影到法向子空间：

$$v_{guided}^{(l)} = v_\emptyset^{(l)} + \omega_l \cdot \text{Proj}_{\text{normal}}(v_c^{(l)} - v_\emptyset^{(l)})$$

其中 $\text{Proj}_{\text{normal}}$ 由该层 SVD 的 top-k 奇异向量定义。

**何时使用**：仅对 tangential_divergence > 0.3 且 normal_alignment < 0.7 的层启用。如果所有层的法向对齐度都高，则不使用此机制——这本身也是一个发现。

### 2.2 CFG 设计的检验：Ablation

所有 CFG 变体都必须经过 ablation：

| 条件 | 验证 |
|------|------|
| 用随机 schedule（随机排列 ω(l)）替代从探针推导的 schedule | 效果退化 → 证明探针信息有价值 |
| 用 uniform optimal ω（全局最优标量）替代 layer-conditioned ω(l) | 退化 → 证明 layer conditioning 有价值 |
| 用 uniform schedule ω(t) 替代探针拟合的 ω(t) | 退化 → 证明 step conditioning 有价值 |
| 移除 direction projection | 退化 → 证明 direction damping 有价值 |

**关键**：如果 random schedule 和探针推导的 schedule 效果相同，说明探针没有提供有效信息——这是整个框架的 falsification test。

---

## 3. 超越 CFG：分工理解的其他干预机制

CFG 只做一件事：条件信号和无条件信号的线性混合。分工理解可以催生更丰富的机制。

### 3.1 机制一：Attention Modulation（非 CFG）

**依据**：Cross-Attention Functional Mapping (§1.6) 发现的 head 功能偏好。

**原理**：不修改 CFG，而是直接修改交叉注意力 weights，让特定 token 在特定层/头的信号更强或更弱。

**场景 1：部件选择性控制**

如果 §1.6 发现 Layer 8 Head 3 主要关注 body_part tokens：
```python
# 对 "right hand waves, left hand still"，增强右手相关 token 的 attention
boost_mask = torch.zeros(num_tokens)
boost_mask[token_of("right")] = 2.0
boost_mask[token_of("hand")] = 2.0
suppress_mask = torch.zeros(num_tokens)
suppress_mask[token_of("left")] = -1.0
suppress_mask[token_of("waves")] = 0.0  # 共享动作 token 不抑制

# 修改 cross-attention logits
attn_logits[layer=8, head=3] += boost_mask + suppress_mask
```

**场景 2：时序控制**

如果 §1.6 发现某些 head 有低 temporal entropy（在特定帧集中激活）：
```python
# 对 "前半段 walk 后半段 run"，创建 frame-dependent attention mask
# walk token 的 attention 在前半帧增强、后半帧抑制
temporal_mask["walk"] = [1.5]*前T/2 + [-1.0]*后T/2
temporal_mask["run"] = [-1.0]*前T/2 + [1.5]*后T/2
```

**优势 vs CFG**：
- Attention modulation 是**稀疏的**（只影响特定 head × token），CFG 是全局的
- Attention modulation 控制**信息路由**，CFG 控制**信号强度**
- 两者可以叠加：CFG 做全局质量-对齐平衡，attention modulation 做细粒度控制

### 3.2 机制二：Activation Steering（非 CFG）

**依据**：Counterfactual Swap (§1.2) 发现的 layer-wise semantic encoding。

**原理**：不混合 cond/uncond signal，而是直接在关键层添加预计算的 steering vector。

**具体设计**：

```python
# Step 1: 从探针数据提取 steering vector
# 如果 Counterfactual Swap 发现 Layer 10 编码 "walk" vs "run" 的语义差异
v_steer_walk_to_run = mean(h["run"] - h["walk"], over_samples, at_layer=10)

# Step 2: 推理时施加 steering
def forward_with_steering(z_t, t, text_embed, steer_layer, steer_vector, steer_scale):
    # 正常 forward，但在 steer_layer 处添加 steering vector
    h = model.encode_to_layer(z_t, t, text_embed, up_to_layer=steer_layer)
    h += steer_scale * steer_vector  # <-- 唯一的干预
    motion = model.decode_from_layer(h, from_layer=steer_layer)
    return motion

# 使用：如果 prompt 是 "run"，但想要更快的 run
motion = forward_with_steering(z_t, t, "run", 
    steer_layer=10, 
    steer_vector=v_steer_slow_to_fast, 
    steer_scale=0.5
)
```

**优势 vs CFG**：
- CFG 只能做"更多条件信号 vs 更少条件信号"的一维控制
- Steering 可以做**任意属性方向**的控制（速度、幅度、风格、情感...），不限于 text condition
- Steering 只需要一个 vector（几十 KB），CFG 需要两次 forward（2× 计算）

**局限**：
- 需要从数据中提取可靠的 steering vector（需要足够的 paired samples）
- Steering direction 可能不是全局线性的（大 scale 时可能偏离 manifold）
- 目前 LLM 领域证明有效（PID Steering），motion 领域需要验证

### 3.3 机制三：Layer-Specific Post-Training（轻量微调）

**依据**：Intervention Response Curve (§1.4) 发现的层敏感性差异。

**原理**：不对全模型做 fine-tune，只对探针发现的"质量瓶颈层"做轻量 post-training，使其对 guidance 更鲁棒。

**具体设计**：

```python
# 如果发现 L14-L15 是质量瓶颈（response curve 太陡），
# 对这些层做 LoRA fine-tune，目标：扩大 safe scale range

# LoRA 配置：只在 L14-L15 的线性层插入 LoRA adapter
lora_config = {
    "target_layers": [14, 15],  # 仅瓶颈层
    "rank": 8,                   # 极小 rank
    "alpha": 16,
}

# 训练目标：在多个 CFG scale 下都保持好的 FID
def post_training_loss(motion, text, omega_range):
    total_loss = 0
    for omega in omega_range:  # [0.5, 0.7, 0.9, 1.0, 1.1, 1.3]
        motion_omega = model.forward_with_cfg(z_T, text, omega=omega)
        total_loss += fid_loss(motion_omega) + r_prec_loss(motion_omega, text)
    return total_loss  # 最小化各 scale 下的平均退化
```

**效果预期**：
- Post-training 后，L14-L15 的 response curve 变平（safe range 变宽）
- 这意味着推理时可以使用更大的 ω 范围而不崩坏质量
- 注意：这不是"提升 FID"，而是"扩大可用 guidance 范围"——不同的贡献维度

### 3.4 机制四：Scheduled Score Projection（几何干预）

**依据**：Score Geometry (§1.5) 发现的 layer-wise tangential divergence。

**原理**：对 tangential_divergence 高的层/步，在采样时将 velocity prediction 投影到法向空间（类似 TCFG，但是逐层逐步的）。

**与 TCFG 的区别**：
- TCFG 对整个模型的 score 做一次 SVD
- MoDebug 对**每层每步**做 SVD，只对需要阻尼的层/步施加投影
- 这是 "surgical TCFG" 而非 "global TCFG"

```python
def layer_step_tcfg(z_t, t, text_embed):
    v_c = model.velocity(z_t, t, text_embed)
    v_unc = model.velocity(z_t, t, None)
    
    delta = v_c - v_unc
    
    for l in range(num_layers):
        delta_l = project_to_layer(delta, l)
        
        # 仅在 tangential_divergence[l][t] > threshold 时施加阻尼
        if tangential_scores[l][t] > 0.3:
            # 保留法向分量，阻尼切向分量
            normal_component = project_normal(delta_l, basis=normal_basis[l][t])
            tangential_component = delta_l - normal_component
            delta_l = normal_component + 0.1 * tangential_component  # 阻尼系数 0.1
        
        v_guided_l = get_uncond_component(l) + omega * delta_l
```

### 3.5 机制选择决策树

```
探针发现                                   →  推荐机制
─────────────────────────────────────────────────────────────
某层 FID response 曲线陡峭（质量敏感）       →  Layer-Conditioned CFG（降低该层 ω）
                                              + Layer-Specific Post-Training（使该层更鲁棒）

某层 R-Prec response 曲线呈单调递增（语义层） →  Layer-Conditioned CFG（提高该层 ω）

某层 cond/uncond 切向发散度高               →  Direction-Conditioned CFG / Scheduled Score Projection

某 head 对 body_part token 选择性高         →  Attention Modulation（部件控制）

某步的 cond/uncond divergence 异常大/小      →  Step-Conditioned CFG / Joint Layer-Step CFG

某层在 Counterfactual Swap 中语义影响大      →  Activation Steering（该层加 steering vector）

多层组合发现                                  →  多机制叠加（如 Layer-CFQ + Attention Modulation）
```

---

## 4. 核心验证实验：最小可行证据链

不要两周做八个 phase。只聚焦一个核心验证循环：

### 实验 A：Semantic Swap 验证 LSH（Day 1-2）

**目的**：用 Counterfactual Swap 确认不同层确实编码不同信息。

**最小执行**：
- 5 个 action pairs（walk↔run, jump↔squat, wave↔clap, kick↔punch, sit↔stand）
- 5 个 target layers（L1, L5, L10, L14, L15）
- 固定 noise seed，swap 每层，测量 semantic shift 和 FID

**通过条件**：至少有一个 layer pair 的 semantic shift 差异 > 2×，且 FID impact 差异 > 2×。如果所有层表现一样，LSH 不成立。

### 实验 B：从 Swap 结果设计 CFG（Day 3-4）

**目的**：验证 Swap 结果能直接指导 CFG 设计。

**最小执行**：
- 用实验 A 的 5 层 swap 结果，按 §3.5 决策树为每层选择 ω
- 实现 Layer-Conditioned CFG（§2.1.1）
- 对比：uniform CFG baseline、random ω schedule（falsification）、A-derived ω schedule

**通过条件**：A-derived schedule > uniform baseline = random schedule。如果 random schedule 效果相当，说明 Swap 探针没有提供有效信息。

### 实验 C：Cross-Attention 探针 + Attention Modulation（Day 5-6）

**目的**：走通非 CFG 路线的第一个完整循环。

**最小执行**：
- 对 MoLingo 做 Cross-Attention Functional Mapping（§1.6），识别 verb-specialized 和 body_part-specialized heads
- 设计一个最小 attention modulation demo：对 "right hand waves" prompt，增强右手相关 token 在 body_part-specialized head 的 attention
- 测量：target part 的运动幅度变化、非 target part 的 drift

**通过条件**：target part 的运动幅度可被 attention modulation 显著改变（而 uniform CFG scale change 做不到这一点）。

### 实验 D：跨模型 Swap（Day 7）

**目的**：验证发现不是 MoLingo 特异的。

**最小执行**：
- 第二模型（MDM/MLD）上重做实验 A
- 比较两模型的 semantic/quality sensitivity profile

**通过条件**：至少一个定性模式在两个模型上一致（如 late-layer sensitivity > early-layer sensitivity）。

---

## 5. ICLR 叙事中的核心 Figure

| Figure | 内容 | 探针来源 |
|--------|------|---------|
| **Fig 2: Layer Specialization Map** | 横轴=layer，纵轴=semantic influence & quality influence（来自 Swap），两条曲线呈 X 形交叉 | §1.2 |
| **Fig 3: Intervention Response Landscape** | 横轴=layer，纵轴=scale，热力图=FID（或 R-Prec），显示不同层的 dose-response 差异 | §1.4 |
| **Fig 4: Layer-Conditioned CFG vs. Baselines** | FID-R-Precision tradeoff curve，layer-conditioned CFG 在 Pareto 前沿 | §2.1 |
| **Fig 5: Attention Modulation for Part Control** | 左右对比：uniform CFG（全臂激活）vs attention-modulated（仅右手激活） | §3.1 |
| **Fig 6: Cross-Model Consistency** | 两模型的 layer sensitivity profile 对比，核心模式一致 | §4 实验 D |

---

## 6. 即刻行动项（具体）

### Day 1
1. **MoLingo 代码 fork + activation cache 实现**
   - 在 forward 中插入 hook，保存每层 hidden states、cross-attention weights、velocity predictions
   - 确认 layer naming convention（MoLingo 有几层？命名规则？CFG_CA 在哪些层？）
   - 产出：可用的 `model.forward_with_cache()` API

2. **Counterfactual Swap 最小实现**
   - 实现 §1.2 的 Semantic Swap：5 action pairs × 5 layers × 1 seed
   - 度量：swap 后 motion 的 semantic shift（用 motion encoder 的 embedding 距离）和 FID 变化
   - 产出：第一张 Layer Specialization 曲线图

### Day 2
3. **Intervention Response Curve**
   - 实现 §1.4：5 layers × 7 scale levels × 1 seed
   - 度量：FID、R-Precision、per-part error
   - 产出：Intervention Response Landscape heatmap

### Day 3
4. **Layer-Conditioned CFG 实现**
   - 用 Day 1-2 结果推导 $\omega(l)$
   - 实现 §2.1.1 的逐层 CFG
   - 跑 3 seeds vs uniform baseline vs random schedule
   - 产出：第一张方法效果图（FID-R-Prec tradeoff）

### Day 4-5
5. **Cross-Attention Mapping**
   - 实现 §1.6：提取所有层的 cross-attention weights
   - 标注 token types，计算 head 功能偏好
   - 产出：Cross-attention functional map

6. **Attention Modulation 实现**
   - 基于 cross-attention map，选择 body_part-specialized head
   - 实现 attention bias injection
   - 验证部件选择性控制效果

### Day 6-7
7. **第二 baseline 环境搭建 + Swap 验证**
   - 选型并部署 MDM 或 MLD
   - 重做实验 A 的 Semantic Swap
   - 比较两模型 profile

---

## 7. 关键风险与 falsification 条件

| 风险 | Falsification 条件 | 降级方案 |
|------|-------------------|---------|
| Semantic Swap 在所有层产生相同效应 | LSH 不成立 | 转向 step specialization（step 维度可能有更清晰的分离） |
| Layer-Conditioned CFG ≤ random schedule | 探针信息无效 | 检查探针方法是否有 bug；尝试更直接的 dose-response 设计 |
| Cross-Attention heads 无功能偏好 | attention modulation 不可行 | 聚焦 CFG 路线；attention 作为辅助分析而非干预接口 |
| 第二模型 profile 完全不同 | 非共性发现 | 降级为 "Understanding MoLingo" case study |
