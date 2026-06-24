---
title: "MoDebug v3: Semantic Locking-Aware Decoupled Guidance for Text-to-Motion Generation"
created: 2026-06-13T21:00:00+08:00
updated: 2026-06-16T02:30:00+08:00
status: self_falsified
hypothesis: >
  SELF-FALSIFIED. After 6 rounds of experiments, the original SLAD design (GDC adaptive
  detection + direction decoupling + semantic projection) has been disproven by its own
  ablation and a control-pair experiment. The residual "method" (simple two-phase ω
  scheduling) differs from ANT only in split point (0.5 vs 0.6) and shows negligible
  effect (Δk50 ≈ 0). The only robust motion-specific finding is direction asymmetry
  (a→b ≠ b→a locking points), which remains descriptive rather than causal. Current
  contribution = PCI replication in motion + proof that GDC does not measure semantic locking.
tags:
  - MoDebug
  - semantic_locking
  - adaptive_guidance
  - counterfactual_swap
  - motion_generation
  - model_agnostic
prior_art:
  - "PCI (Görgün et al., arXiv Dec 2025): trajectory swap for image diffusion — DESCRIPTIVE only, no mechanism"
  - "ANT (Chen et al., ACM MM 2025): spectral partitioning + DCFG for motion — fixed schedule, no causal discovery"
  - "C2FG (Gao et al., CVPR 2026): exponential CFG schedule from score theory — fixed, not adaptive"
novelty_gap: >
  ORIGINAL CLAIM (now disproven): First to combine causal discovery + adaptive mechanism in motion.
  ACTUAL: PCI already established trajectory swap for causal discovery in images. Our motion
  replication adds domain but not insight. The adaptive mechanism (GDC) was falsified by
  control-pair experiment. The remaining contribution is proving that direction consistency
  (GDC) is a false signal for semantic locking — a negative result of limited impact.
supplements: "[[archived/v2/2026-06-13_modebug_research_framework_v2]]"
replaces: "[[archived/v2/2026-06-13_modebug_probes_and_mechanisms]] (layer-level probes deprecated in favor of trajectory-level)"
---

# MoDebug v3: Semantic Locking-Aware Decoupled Guidance

> [!abstract] 一句话
> 我们不关心 "L15 是否比 L10 更敏感"。我们关心的是：**在去噪过程中，条件信号何时从"决定做什么动作"转变为"精调动作质量"，以及如何利用这个转变来解耦引导信号，打破质量-对齐的 tradeoff。** 这个方法不需要访问模型内部结构，只需要 velocity predictions —— 对任何 flow/diffusion motion generator 通用。

---

> [!danger] 2026-06-16 六轮实验后的诚实评估
>
> **核心主张已被自己的实验否定。**
>
> v3 声称的独特组合是 "causal discovery + adaptive inference-time mechanism"：
> - **Causal discovery** ✅ 成立但价值有限——trajectory swap 确认了 motion 中的早期语义锁定，但这是 PCI (2025) 在图像上的发现在 motion 领域的复制。方向不对称（kicks↔punches a→b/b→a ratio=2.79）是唯一的 motion-specific 信号，但它是描述性的——没有因果解释，没有被利用。
> - **Adaptive mechanism** ❌ 已被自己的 ablation 和 control pair 实验否定——GDC detector（control pair k50 0→4）、direction decoupling（简单 scaling 更好）、semantic projection（attribute +0.12 不值得保留）全部证伪。
>
> **去掉三个组件后，剩下的"方法"就是 ANT 的两段式 ω 调度（split=0.5 vs ANT 的 0.6），且效应幅度接近于零（Δk50 = −0.06 到 −0.18）。**
>
> 站得住脚的发现：
>
> | # | 结论 | 强度 | 问题 |
> |---|------|------|------|
> | 1 | Motion diffusion 存在早期语义锁定 | 高 | PCI known，motion 版无增量 insight |
> | 2 | 方向不对称（a→b ≠ b→a）是跨 seed 稳健现象 | 高 | 描述性，无因果解释 |
> | 3 | GDC 不测量语义锁定（control pair 证伪） | 高 | 负面结果，否定了自己的设计 |
> | 4 | 简单两段式 ω 略优于均匀 CFG | 低 | Δk50≈0，效应在噪声范围内 |
>
> **当前实际贡献 = PCI 在 motion 上的复制 + 证明了 GDC 不可行。构不成一篇 paper。**
>
> 接下来的选择：
> - **A. 降级收尾** — short/workshop paper："Why GDC Fails"
> - **B. 回到现象** — 方向不对称是唯一稳健的 motion-specific 信号，先理解 "why"，再做方法
>
> 六轮实验最大的教训：从现象直接跳到方法设计（M0 → GDC → SLAD），跳过了最关键的一步——**理解 locking 的因果机制**。PCI 的 "when" 还没吃透就急于做 "so what"。

---

## 0. 为什么 Layer-Level 路线被放弃

旧版（v2 框架 + probes 文档）的核心缺陷：

| 问题 | 后果 |
|------|------|
| Layer 不是跨模型的公共接口（MoLingo 的 L15 ≠ MDM 的任何层） | 无法证明通用性 |
| 每层"功能"的语义标签（语义层/质量层）是事后解释，不是因果证明 | Reviewer 会说是讲故事 |
| 层探针越多，越像在为 MoLingo 手动定制 | 失去 model-agnostic 的核心价值 |

**Trajectory-level 方案的根本优势**：所有 flow/diffusion model 都有 $z_t$、$v(z_t, t, c)$、去噪循环。这是真正的公共接口。

---

## 1. 相关工作定位（诚实版）

### 1.1 PCI：最接近的前置工作

**PCI** (Görgün et al., arXiv Dec 2025) 做了 trajectory-level counterfactual swap，发现：
- 全局因素（天气、季节）在 early step 锁定
- 人类属性（年龄、性别）在 mid step 锁定
- 细粒度细节在 late step 仍可编辑
- Rectified flow 模型比 DDPM 更早锁定概念

**PCI 的局限**：
- 纯描述性——CIS curves 回答了 "when"，但没有回答 "so what"
- 唯一的应用是"选一个更好的编辑 timestep"——不涉及新机制
- 只在图像生成上验证
- 没有利用 locking 发现来改进生成过程本身

### 1.2 ANT：最接近的 motion 工作

**ANT** (Chen et al., ACM MM 2025) 提出：
- 用频谱分析将去噪过程分为低频结构规划期和高频细节精调期
- Dynamic CFG (DCFG) 在不同阶段使用不同的引导强度

**ANT 的局限**：
- 阶段划分基于频谱启发式（假设低频谱 = 结构，高频谱 = 细节），没有因果验证
- DCFG 仍然是固定 schedule（只是分了两段），不随具体 prompt 或生成过程自适应
- 修改了模型架构（STA module），不是纯 inference-time

### 1.3 C2FG

**C2FG** (Gao et al., CVPR 2026) 理论推导出 score discrepancy 指数衰减，提出 $\omega(t) = \omega_0 \exp(\lambda(1-t/T))$。

**局限**：固定指数衰减。如果实际 locking 不是指数衰减（PCI 显示存在 sharp transition），C2FG 的 schedule 就不是最优的。

### 1.4 MoDebug 的空白

```
                Causal Discovery    Adaptive Mechanism    Motion Domain    Inference-Only
PCI             ✓ (descriptive)     ✗                     ✗                ✓
ANT             ✗ (heuristic)       ✗ (fixed schedule)    ✓                ✗ (modifies arch)
C2FG            ✗ (theoretical)     ✗ (fixed exponential)  ✗                ✓
MoDebug SLAD    ✓ (causal swap)     ✓ (online detection)   ✓                ✓
```

**MoDebug 的独特组合**：在 motion 领域做 causal discovery + 基于 discovery 设计 adaptive inference-time mechanism。

---

## 2. 核心现象：Semantic Locking in Motion Diffusion

### 2.1 发现方法：Trajectory Counterfactual Swap

```python
def trajectory_swap(model, z_T, prompt_A, prompt_B, swap_step, num_steps=50):
    """
    不需要任何模型内部访问。只需 model.denoise_step()。
    
    核心逻辑：从 prompt A 开始去噪，在 step t_swap 处切换为 prompt B，
    测量最终输出偏向 A 还是 B。
    """
    z = z_T
    for step in range(num_steps, 0, -1):
        t = step / num_steps
        if step > swap_step:
            condition = prompt_A   # 切换前用 A
        else:
            condition = prompt_B   # 切换后用 B
        z = model.denoise_step(z, t, condition)
    return z  # 最终 motion

# 对所有 swap_step 重复
for swap_t in [1.0, 0.9, 0.8, ..., 0.1, 0.0]:
    motion = trajectory_swap(model, z_T, "walk", "run", swap_t)
    
    # 测量：输出更接近 "walk" 还是 "run"？
    action_score = action_similarity(motion, "walk")  # 0=完全是run, 1=完全是walk
    
    # 测量：运动质量如何？
    fid_score = evaluate_fid(motion)
    
    results[swap_t] = {"action": action_score, "fid": fid_score}
```

### 2.2 预期发现与 PCI 对比

PCI 在图像生成中发现的是**连续渐变**（CIS 从 0 平滑过渡到 1）。但 motion 有独特的结构——身体部件、时序依赖、物理约束——可能产生不同的模式：

**假设的 Motion-Specific 发现**：

| 发现 | 与 PCI 的关系 | Motion 特有的原因 |
|------|-------------|------------------|
| Action identity（walk/run）有相对 sharp 的 locking transition | PCI 也发现概念有 transition，但 motion 可能更 sharp | Motion 的动作类别是离散的（walk vs run 是二选一），不像图像中"老"可以渐变 |
| Body parts 有分层 locking：torso/root 先锁定，limbs 后锁定 | PCI 没有 part-level 分析 | 人体动力学约束：躯干稳定性先于四肢灵活性 |
| 运动质量（FID）的 locking window 晚于语义 locking | PCI 没有区分 quality vs semantics | Motion quality 涉及精细的物理合理性，自然在后期决定 |
| 时序结构（动作的开始/结束）在不同阶段锁定 | PCI 没有 temporal 维度 | Motion 是时序数据，不同帧的语义可能在不同步决定 |

**如果上述发现成立** → motion 的 semantic locking 有独特结构，不是 PCI 在图像上的简单复现。这是贡献。

**如果所有属性在同一个 window 锁定** → locking 存在但无细分结构。此时贡献降级为 "first characterization of semantic locking in motion generation"，仍有价值但体量减小。

### 2.3 关键：不依赖语义标签

我们不需要声称"这一段的 Δv 编码了 action，那一段编码了 quality"。我们只测量一个客观量：

> **Guidance Direction Consistency (GDC)**：连续两步之间 Δv 方向的余弦相似度
> $$\text{GDC}(t) = \cos\left(\Delta v(z_t, t, c), \Delta v(z_{t+1}, t+1, c)\right)$$

当 GDC 从波动转为稳定（持续 > 阈值），说明模型已 "commit" 到某个生成方向——这就是 **semantic locking point**。

这个定义：
- 不需要人工标注"什么是 action、什么是 speed"
- 不需要知道模型内部结构
- 对任何 prompt 自适应
- 对任何 model 自适应

---

## 3. 机制：Semantic Locking-Aware Decoupled Guidance (SLAD)

### 3.1 核心洞察

标准 CFG 的根本问题是：**同一个 $\omega$ 同时服务于两个矛盾的目标**。

- **目标 1（Semantic Establishment）**：在模型还未决定生成什么时，条件信号需要足够强来建立正确的语义
- **目标 2（Quality Refinement）**：在语义已锁定后，条件信号只需要维持方向，过度干预反而破坏质量（这就是 L15 cliff 的 trajectory-level 解释）

**SLAD 的解耦方案**：

```
Pre-Locking Phase:            Post-Locking Phase:
─────────────────────         ─────────────────────
Strong CFG (ω_high)           弱 Quality Guidance (ω_qual ≈ 1.0)
完整 Δv 方向                   仅语义方向上的强保持 (ω_sem > 1.0)
目标: 建立正确语义              目标: 维持语义 + 释放质量空间
```

### 3.2 算法

```python
def SLAD_guidance(model, z_T, text_condition,
                  omega_high=5.0, omega_sem=3.0, omega_qual=1.0,
                  lock_threshold=0.95, lock_patience=3):
    """
    Semantic Locking-Aware Decoupled Guidance
    
    Args:
        omega_high:   pre-locking 阶段的 CFG scale（强引导建立语义）
        omega_sem:    post-locking 阶段语义方向上的保持强度
        omega_qual:   post-locking 阶段质量方向上的引导强度（≈1.0）
        lock_threshold: GDC 超过此值视为方向稳定
        lock_patience:  连续稳定步数才判定为 locked
    """
    z = z_T
    locked = False
    stable_count = 0
    semantic_direction = None  # 累积的语义方向
    guidance_history = []
    
    for step in range(T, 0, -1):
        t = step / T
        
        # 1. 获取条件和无条件速度
        v_c = model.velocity(z, t, text_condition)
        v_unc = model.velocity(z, t, None)
        delta_v = v_c - v_unc  # guidance direction
        
        # 2. 检测 semantic locking
        if len(guidance_history) > 0:
            prev_delta = guidance_history[-1]
            gdc = cosine_similarity(delta_v, prev_delta)
            
            if gdc > lock_threshold:
                stable_count += 1
            else:
                stable_count = 0
            
            if stable_count >= lock_patience and not locked:
                locked = True
                # 锁定时的 Δv 方向即为语义方向
                semantic_direction = delta_v / torch.norm(delta_v)
        else:
            gdc = 1.0  # 第一步无历史
        
        guidance_history.append(delta_v)
        
        # 3. 根据锁定状态选择引导策略
        if not locked:
            # Pre-locking: 标准 CFG，强引导
            v_guided = v_unc + omega_high * delta_v
        else:
            # Post-locking: 解耦引导
            # 将 Δv 分解为语义方向分量和质量方向分量
            delta_sem = project_onto(delta_v, semantic_direction)
            delta_qual = delta_v - delta_sem
            
            # 语义方向强保持，质量方向弱扰动
            v_guided = v_unc + omega_sem * delta_sem + omega_qual * delta_qual
        
        # 4. 去噪步
        z = model.denoise_step(z, t, v_guided)
    
    return z


def project_onto(v, direction):
    """将 v 投影到 unit direction 上"""
    return torch.dot(v, direction) * direction
```

### 3.3 为什么这不是 "不同的 ω per step"

| 简单的 step-conditioned CFG | SLAD |
|---------------------------|------|
| ω(t) 是预先定义的函数 | Locking point 是在线检测的 |
| 对所有 prompt 使用相同 schedule | 每个 prompt 自适应（复杂 prompt 可能更晚锁定） |
| 只改变一个标量 ω | 改变的是引导的**方向结构**（语义分量 vs 质量分量） |
| 无法解释为什么后期要降低 ω | 有明确的因果逻辑：锁定后质量分量不需强引导 |

### 3.4 为什么这不是 ANT

| ANT | SLAD |
|-----|------|
| 用频谱分析划分阶段（假设低频=结构） | 用 GDC 在线检测 locking（因果性的） |
| DCFG 是固定的两段 schedule | Locking point 随 prompt 和 seed 自适应 |
| 修改模型架构（STA module） | 纯 inference-time，不改模型 |
| 未验证阶段划分是否正确 | 用 counterfactual swap 验证 locking 检测的准确性 |

### 3.5 Ablation 组件

| 组件 | 移除方式 | 验证什么 |
|------|---------|---------|
| **Adaptive detection** | 用固定步数阈值（如 step 25/50）替代 GDC 检测 | 自适应检测是否优于固定 schedule |
| **Direction decoupling** | Post-locking 仍用标准 CFG（仅降低 ω） | 方向分解是否有独立价值 |
| **Semantic projection** | Post-locking 用 $\omega_{sem} \cdot \Delta v$ 而非投影 | 投影操作是否必要（保护质量分量） |
| **Locking patience** | patience=1（一次高 GDC 即判定锁定） | 锁定检测的鲁棒性 |

---

## 4. 实验设计

### 4.1 实验一：GDC 作为 Locking 检测器的验证

**目的**：证明 GDC 确实能检测 semantic locking。

**方法**：
- 对 5 个 prompt pairs 做 trajectory swap（§2.1），测量 swap effect curve
- 同时记录每个 step 的 GDC
- 计算 GDC 稳定点与 swap effect 衰减点的相关性

**通过条件**：GDC 稳定点（连续 3 步 GDC > 0.95）与 "swap 不再改变输出 action" 的步数之间的 Spearman 相关系数 > 0.7。

**如果失败**：说明 GDC 不稳定不能作为 proxy。需要找其他检测信号（如 Δv 的范数变化率、z_t 的轨迹曲率等）。但这是实现细节，不影响方向。

### 4.2 实验二：SLAD vs Baselines

**Baselines**：
1. **Uniform CFG**：标准 CFG，ω ∈ {1.0, 2.0, 3.0, 5.0, 7.5}
2. **C2FG**：指数衰减 schedule，λ 从 grid search
3. **ANT-style DCFG**：两段固定 schedule（ω_high 前 60% steps, ω_low 后 40%）
4. **SLAD (ours)**：自适应检测 + 解耦引导

**指标**：FID vs R-Precision 的 Pareto frontier（不是单点对比）

**通过条件**：SLAD 在 Pareto frontier 上，且至少有一个操作点同时优于 uniform CFG 的 best FID 和 best R-Precision。

### 4.3 实验三：Ablation

| 条件 | FID | R-Precision |
|------|-----|-------------|
| Uniform CFG (best ω) | baseline | baseline |
| SLAD full | ? | ? |
| SLAD − adaptive detection (fixed step=25) | 应退化 | 应退化 |
| SLAD − direction decoupling (post-lock ω_low only) | 应退化 | 应持平或退化 |
| SLAD − semantic projection (rescale Δv) | 应退化 | 应持平或退化 |

### 4.4 实验四：Cross-Model Transfer

**模型**：MoLingo (rectified flow + transformer) + MDM (DDPM + UNet)

**方法**：相同的 SLAD 代码（只换 `model.velocity()` 和 `model.denoise_step()` 的实现），相同的超参数，跑相同的 prompts。

**测量**：
- 两模型各自的 FID-R-Precision tradeoff 改善
- 两模型各自的平均 locking step（预期：rectified flow 的 locking 早于 DDPM，与 PCI 发现一致）
- 超参数敏感度（是否需要 per-model tuning）

**通过条件**：两模型在 SLAD 下都有同向改善（不要求等幅度）。

### 4.5 实验五：Locking 的 Motion-Specific 分析

**目的**：证明 motion 的 semantic locking 有独特结构（区别于 PCI 在图像上的发现）。

**方法**：
- 对不同类型的 prompt pairs 分别做 trajectory swap：
  - Action pairs（walk↔run）
  - Speed pairs（fast↔slow）
  - Direction pairs（left↔right）
  - Body part pairs（arm wave↔leg kick）
  - Quality pairs（paired by FID score 高低）
- 比较各类型的 locking window

**预期发现**：
- Action identity 在中等噪声水平（t≈0.6-0.7）锁定
- Speed/Amplitude 在较低噪声水平（t≈0.4-0.5）锁定
- Body part 细节在最晚期（t≈0.2-0.3）锁定
- Motion quality 也晚期锁定
- **关键**：属性的 locking 顺序在不同 prompt 间保持一致（即使绝对值有 shift）

**如果所有属性在同一个 window**：说明 motion 没有分层的 locking 结构。降级 claim。

---

## 5. ICLR 叙事

### 5.1 核心故事

```
Title: Semantic Locking-Aware Decoupled Guidance for Text-to-Motion Generation

1. Introduction
   - Text-to-motion diffusion 模型越来越好，但 guidance 机制还是 2021 年的 uniform CFG
   - CFG 的根本问题：同一个 ω 服务于语义建立和质量精调两个矛盾目标
   - 我们问：能否检测语义何时"锁定"，然后解耦引导？

2. Preliminaries: Semantic Locking in Motion Diffusion
   - Trajectory counterfactual swap 实验
   - 发现：motion 的语义属性在去噪过程中存在分层的 locking 结构
     · Action identity 先锁定，quality 后锁定
     · Body parts 有独立的 locking 顺序
   - 与 PCI（图像）的对比：motion 的 locking 因时序结构和物理约束而有独特模式

3. Method: SLAD
   - Guidance Direction Consistency (GDC)：在线检测 locking 的信号
   - 检测到 locking 后，将 Δv 分解为语义分量和质量分量
   - 语义分量：强保持（high ω_sem）
   - 质量分量：弱引导（ω_qual ≈ 1.0，释放质量空间）
   - 纯 inference-time，模型无关

4. Experiments
   - SLAD 在 MoLingo 上 Pareto-dominates uniform CFG 和 C2FG
   - Ablation：检测、解耦、投影各有独立贡献
   - Cross-model：相同代码在 MDM 上同向改善
   - 可控性：Post-locking 阶段可以独立调节 quality 而不改变 action

5. Analysis
   - 为什么 semantic locking 存在？（扩散过程的 coarse-to-fine 本质）
   - 为什么解耦有效？（语义和质量对 guidance 的需求不同）
   - Motion vs Image locking 差异
   - 局限：GDC 检测在极短步数（<10 steps）时可能不可靠
```

### 5.2 与 Reviewer 的预判对话

**Q: "PCI 已经做了 trajectory swap，你的 swap 有什么新意？"**
A: PCI 在图像上做，我们在 motion 上做，发现了 motion 特有的分层 locking（body parts、temporal structure）。更重要的是，PCI 只描述不设计机制，我们设计了基于 locking 的自适应 guidance。

**Q: "ANT 已经有 dynamic CFG 了，你的 SLAD 有什么不同？"**
A: ANT 的 DCFG 是固定两段 schedule（基于频谱启发式），SLAD 是在线检测 locking + 方向分解。Ablation 中 fixed-step 替代 adaptive detection 会导致退化，证明自适应是必要的。

**Q: "GDC 信号稳定吗？怎么知道检测到的 locking 就是真的 locking？"**
A: 实验一专门验证 GDC 与 counterfactual swap effect 的相关性。如果 GDC 不准，可以替换检测信号，机制框架不变。

**Q: "这个机制是不是只对 MoLingo 有效？"**
A: 实验四在 MDM 上同向验证。SLAD 只需要 velocity() 和 denoise_step() 两个接口，不对模型内部做任何假设。

---

## 6. 即刻行动项（聚焦版）

### Day 1: Trajectory Swap 基础设施

```python
# 最小实现：不需要 hook，不需要理解模型内部
class TrajectorySwapProbe:
    def __init__(self, model):  # model 只需两个方法
        self.model = model
    
    def probe_pair(self, z_T, cond_A, cond_B, swap_steps):
        """对一对 prompt 在所有 swap step 上做 swap"""
        results = {}
        for swap_t in swap_steps:
            motion = self._swap_run(z_T, cond_A, cond_B, swap_t)
            results[swap_t] = {
                "action_similarity_to_A": self._measure_action(motion, cond_A),
                "action_similarity_to_B": self._measure_action(motion, cond_B),
                "fid": self._evaluate_fid(motion),
                "gdc_curve": self._recorded_gdc,  # 顺便记录 GDC
            }
        return results
```

- 在 MoLingo 上实现 `model.denoise_step(z, t, condition)`
- 选 5 action pairs × 10 swap steps × 1 seed = 50 次生成
- **产出**：第一张 swap effect curve + GDC vs swap effect 相关性

### Day 2: GDC 检测器 + SLAD 实现

- 从 Day 1 的 GDC 曲线确定 lock_threshold 和 lock_patience
- 实现 SLAD 的 denoise loop
- 对比 uniform CFG baseline（3 seeds × 5 ω values）

### Day 3-4: Ablation + 更多 prompts

- 跑 §4.3 的 ablation 条件
- 扩展到多种 prompt 类型（§4.5）

### Day 5-6: 第二模型

- 在 MDM 上实现相同的 model wrapper（denoise_step + velocity）
- 重跑 trajectory swap + SLAD
- **产出**：跨模型对比

### Day 7: 整理 + 写 paper outline

---

## 7. 风险与降级路径

| 风险 | 概率 | 降级方案 |
|------|------|---------|
| GDC 不能可靠检测 locking（相关性 < 0.5） | 中 | 尝试替代信号：Δv 范数的变化率、z_t 的 trajectory curvature、多 seed 的 Δv 方差 |
| Locking pattern 与 PCI 的图像发现雷同（无 motion 特异性） | 中 | 降级 claim 为 "first characterization in motion" 而非 "motion-specific structure" |
| SLAD 不优于 C2FG 的指数衰减 | 低 | 检查 GDC 检测是否过于保守（locking 太晚 → ω_high 阶段太短） |
| MDM 的 SLAD 改善不显著 | 中 | 分析原因（DDPM 的 locking 是否更 gradual？）；降级为 MoLingo case study |
| 所有属性的 locking window 重叠 | 中 | 说明 motion locking 没有分层结构；聚焦 GDC 检测 + 解耦本身的价值 |

---

## Appendix A: 关键论文定位

| 论文 | 域 | 做了什么 | 没做什么 |
|------|------|---------|---------|
| **PCI** (Görgün et al., arXiv 12/2025) | Image | Trajectory swap → CIS curves → 选编辑 timestep | 没设计 guidance 机制 |
| **ANT** (Chen et al., ACM MM 2025) | Motion | 频谱分区 + DCFG | 没因果验证，固定 schedule，改架构 |
| **C2FG** (Gao et al., CVPR 2026) | Image | 指数衰减 CFG schedule | 固定函数，理论推导而非发现驱动 |
| **MoDebug SLAD** (ours) | Motion | Causal swap → GDC detection → Decoupled guidance | — |

## 11. 2026-06-15 实验更新：Multi-Seed Calibration 完成

> [!note] 结果摘要
> 2026-06-14 22:42 在 4090 双卡上启动 5-seed (3407, 2026, 1337, 1991, 614) M0 + GDC probe + 相关性分析，2026-06-15 00:14 双卡全部完成。总计约 90 分钟/卡，无报错。核心结论：**stability_score（GDC × norm_ratio）可以校准为 semantic locking 检测器，但分维度通过率不同。**

### M0 Multi-Seed 结果

**GPU0 action/control（5 seeds × 3 non-control pairs × 2 directions = 30 curves）：**

| Prompt pair | Dir | k50 mean | k50 std | width mean | width std |
|---|---|---|---:|---:|---:|---:|
| walks vs runs | a_to_b | 5.71 | 1.87 | 16.26 | 3.17 |
| walks vs runs | b_to_a | 6.10 | 1.69 | 11.52 | 3.32 |
| sits down vs stands up | a_to_b | 5.11 | 1.30 | 4.63 | 1.18 |
| sits down vs stands up | b_to_a | 4.16 | 0.46 | 6.66 | 3.08 |
| kicks vs punches | a_to_b | **11.00** | 0.80 | **16.75** | 1.05 |
| kicks vs punches | b_to_a | 3.83 | 0.03 | 9.77 | 1.24 |

- Aggregate: mean k50 = 5.98 ± 2.67, 23/30 (77%) ≤ step 8
- kicks vs punches a_to_b 在 multi-seed 下仍然是最晚锁定的（~11.0），且极低 std

**GPU1 attribute/direction（5 seeds × 4 non-control pairs × 2 directions = 40 curves）：**

| Prompt pair | Dir | k50 mean | k50 std | width mean | width std |
|---|---|---|---:|---:|---:|---:|
| walks slowly vs walks quickly | a_to_b | 3.91 | 0.03 | 6.35 | 1.81 |
| walks slowly vs walks quickly | b_to_a | 3.89 | 0.04 | 8.05 | 2.72 |
| jumps high vs jumps low | a_to_b | **9.22** | 5.60 | 14.97 | 2.55 |
| jumps high vs jumps low | b_to_a | 5.34 | 1.40 | 10.64 | 3.41 |
| walks forward vs walks backward | a_to_b | 3.74 | 0.07 | 3.55 | 1.44 |
| walks forward vs walks backward | b_to_a | 6.88 | 1.21 | 17.83 | 0.92 |
| turns left vs turns right | a_to_b | 4.62 | 0.88 | 1.42 | 1.08 |
| turns left vs turns right | b_to_a | 4.70 | 0.97 | 1.29 | 0.88 |

- Aggregate: mean k50 = 5.29 ± 2.77, 37/40 (92%) ≤ step 8
- jumps high/low 在 multi-seed 下暴露出最高方差（std=5.6），含一个 outlier seed 拉出 ~19 k50

### 方向不对称（跨 seed 一致）

| Pair | a_to_b / b_to_a ratio | 说明 |
|---|---|---|
| kicks vs punches | **2.54** | a→b 始终远晚于 b→a |
| jumps high vs jumps low | **2.12** | 同向不对称 |
| walks forward vs walks backward | **0.49** | 反向不对称（b→a 更晚） |
| sits down vs stands up | 1.83 | 中等不对称 |
| walks slowly vs walks quickly | **1.03** | 几乎对称 |
| turns left vs turns right | **0.95** | 几乎对称 |

### GDC Detector 校准

| GPU | Best field | Best threshold | Pearson vs k50 | 通过 (≥0.7) |
|---|---|---|---|---|
| GPU0 action/control | stability_score | 0.90 | **0.613** | 否 |
| GPU1 attribute/direction | stability_score | 0.95 | **0.813** | **是** |

**关键发现：**
- `stability_score`（GDC × norm_ratio 衰减惩罚）在所有条件下均优于 raw GDC — 单纯的方向一致性不够，需结合 Δv 范数变化率做联合检测
- **attribute 维度通过** detector 门槛（Spearman ρ ≈ Pearson），意味着对 speed/height/direction 这类连续属性，可以开始 SLAD vs baseline 对比
- **action 维度未通过**（0.61），离散动作 swap 的 source retention transition 与 GDC stability 的映射更复杂，需要专项诊断

### SLAD vs Baselines 首次对比（2026-06-15）

> [!note] 关键结果
> 在 attribute prompt set 上对比 4 种 guidance 模式的 M0 source retention 曲线（1 seed pilot）。**SLAD 是唯一一致提前 semantic locking 的方法，且 action 维度效果反而强于 attribute 维度。**

**Attribute 维度（GPU1, seed=3407, 4 pairs × 2 dirs = 8 curves）：**

| Method | Mean Δk50 vs CFG | Earlier / Total | Range | 稳定性 |
|---|---|---|---|---|
| **SLAD** | **-0.25** | 5/8 | [-2.15, +1.56] | 一致 |
| C2FG (exponential λ=2.0) | -0.16 | 3/8 | [-7.56, +4.18] | 极不稳定 |
| ANT (two-phase 7.5→1.5) | +0.20 | 3/8 | [-0.10, +1.03] | ≈CFG |

**Action 维度（GPU0, 2 seeds, 3 non-control pairs × 2 dirs × 2 seeds = 12 curves）：**

| Method | Mean Δk50 vs CFG | Earlier / Total | Range |
|---|---|---|---|
| **SLAD** | **-0.37** | 7/12 | [-1.57, +1.90] |

- SLAD 在 hardest case（kicks/punches a→b, k50 ~10-12）上改进最大：-1.49 到 -1.57

### Ablation 拆解（2026-06-15）

> [!important] 关键发现：SLAD 的真正机制比设计简单得多
> 三个组件的 ablation 显示：**adaptive detection（GDC）、direction decoupling、semantic projection 对 SLAD 效果的贡献均为零或负面。** SLAD 的全部收益来自两段式 guidance 结构本身（early strong CFG → late weak guidance）。

**Action 维度（GPU0, 2 seeds × 3 pairs）：**

| 条件 | Mean Δk50 vs CFG | vs SLAD full |
|---|---|---|
| **SLAD full** | **-0.37** | — |
| − adaptive detection (fixed step=25) | **-0.37** | 0.00 |
| − direction decoupling (post-lock ω=1.5) | -0.54 | −0.17 (反而更好) |
| − semantic projection (post-lock ω_sem·Δv) | -0.46 | −0.09 |

**Attribute 维度（GPU1, 2 seeds × 4 pairs）：**

| 条件 | Mean Δk50 vs CFG | vs SLAD full |
|---|---|---|
| **SLAD full** | **-0.75** (11/16) | — |
| − adaptive detection (fixed step=25) | **-0.76** (11/16) | 0.00 |
| − direction decoupling (post-lock ω=1.5) | -0.99 (11/16) | −0.24 (反而更好) |
| − semantic projection (post-lock ω_sem·Δv) | -0.64 (11/16) | +0.12 (仅此组件有微弱正向) |

**跨维度一致结论：**
1. **Adaptive detection 贡献为零** — 固定 step=25 与 GDC 检测的 SLAD 完全等价（action 和 attribute 均 0.00 degrad）
2. **Direction decoupling 有害** — 简单 ω scaling 在 action 上更好（−0.17），attribute 上也更好（−0.24）
3. **Semantic projection 微弱正向但仅在 attribute** — action 上负面（−0.09），attribute 上正向（+0.12），不值得保留
4. **真正机制：两段式 guidance** — 早期强 CFG 建立语义 + 后期弱 guidance 释放质量空间

这解释了三件事：
- 为什么 GDC 校准质量 ≠ SLAD 效果（GDC 根本不重要）
- 为什么 C2FG 失败（ω 40→5.5 早期过强，不稳定）
- 为什么 ANT 失败（split=60% 切换点与有效切换点不同）

**Paper 叙事应简化为：** 两段式 guidance（early strong → late weak）优于所有复杂设计。这是更强的故事——更简单、更普适、更容易跨模型验证。

| 维度 | GDC Pearson | SLAD Mean Δk50 |
|---|---|---|
| Attribute | **0.81** (pass) | -0.25 |
| Action | 0.61 (fail) | **-0.37** |

这说明 decoupled guidance 的方向分解（semantic projection + quality release）可能有独立于精确 locking 检测的贡献。即使 locking point 检测不完美，将 Δv 分解为语义分量和质量分量本身就能改善 guidance。

**C2FG/ANT 教训：**
- C2FG 的指数衰减在 motion 上极不稳定 — 同一个 schedule 让某些 pair 的 k50 从 11→4，另一些从 7→12
- ANT 的固定两段 schedule 几乎等于 CFG baseline
- 这直接支撑了 v3 的核心论点：**固定 schedule（理论推导或启发式）不如自适应检测**

### 现在的设置与下一步

- `cfg=5.5`, `sample_steps=32`, `acc=3`, `directions=a_to_b,b_to_a`, `swap_iterations=all`
- `trace_detail=aggregate`, `stability_score` 作为 detector 信号, `lock_threshold=0.95`, `lock_patience=3`
- SLAD: `omega_high=5.5` (pre-lock), `omega_sem=3.0`, `omega_qual=1.0` (post-lock)
- **下一步（按优先级）**：
  1. **Multi-seed SLAD vs CFG 确认**：在 attribute + action 两个维度上用 3+ seeds 确认 SLAD 的优势幅度，估计方差
  2. **Ablation 拆解贡献来源**：分别移除 adaptive detection、direction decoupling、semantic projection（§3.5），判断哪个组件贡献最大
  3. **MDM 跨模型验证**：在 MDM 上实现相同的 model wrapper（denoise_step + velocity），验证 SLAD 非 MoLingo 专属
  4. **连接 evaluator**：用 MoLingo 的 FID/R-Precision pipeline 验证 SLAD 在 quality 维度上的改善

详细原始数据见 4090: `experiments/MoDebug/molingo/slad/slad_vs_baselines_attribute_*` 和 `slad_action_diagnostic_*`。

详细表格和原始数据见 4090: `experiments/MoDebug/molingo/slad/slad_core_calibration_*_20260614_core_seed5_official_gpu*`。接力记录看 [[experiments/molingo/2026-06-14_slad_history]]。

### 11.1 简化版 SLAD 实现（2026-06-15）

> [!important] 路线简化
> Ablation 证明三个设计组件（GDC adaptive detection、direction decoupling、semantic projection）贡献为零或负面后，立即将 SLAD 简化为纯 two-phase ω 调度。

**新算法（`cfg_schedule=slad_simple`）：**

```python
# 去掉 GDC/locking detection/direction decoupling/semantic projection
# 只保留最核心的两段式 ω 调度
omega_high = cfg       # pre-split: standard CFG to establish semantics
omega_post = 1.5       # post-split: weak guidance to free quality space
t_split = 0.5          # timestep fraction → outer step ~25/50

def slad_simple_guidance(timestep, cfg):
    if timestep < t_split:
        return cfg          # ω = 5.5, standard CFG
    else:
        return omega_post   # ω = 1.5, simple scaling
```

**代码修改**（`modebug_slad.py`）：
- 新增 `--cfg_schedule slad_simple` option
- 新增 `--slad_split`（默认 0.5 = step 25/50）和 `--slad_omega_post`（默认 1.5）参数
- 与现有 `two_phase` schedule 的关键区别：split=0.5 vs ANT 的 0.6，且 `guidance_mode=cfg`（无 SLAD 内部逻辑）
- 部署路径：`experiments/MoDebug/molingo/scripts/modebug_slad.py`

**Multi-Seed 验证结果**（2026-06-16 02:20 完成，双卡 ~170 min）：

> [!note] 实验完成，0 failures，CFG equivalence 全通过，max_abs=0.0

### 11.2.1 Action Control — 完整 Per-Pair 分解

**Prompt pairs:**
- [0] control: walks ↔ walks
- [1] walks ↔ runs
- [2] sits down ↔ stands up
- [3] kicks ↔ punches

| Pair | CFG k50 | Simplified SLAD k50 | Δ vs CFG | SLAD Full k50 | Δ vs CFG |
|------|---------|-------------------|----------|---------------|----------|
| [0] walks↔walks (ctrl) | 0.00±0.00 | 0.00±0.00 | 0.00 | **3.94±2.89** | **+3.94** |
| [1] walks↔runs | 5.51±1.56 | 5.39±1.54 | −0.13±0.23 | 4.83±1.54 | −0.68±0.65 |
| [2] sits↔stands | 4.92±1.25 | 4.91±1.24 | 0.00 | 5.03±1.30 | +0.12±0.89 |
| [3] kicks↔punches | 7.23±3.46 | 7.10±3.35 | −0.12±0.11 | 6.26±2.58 | −0.97±1.01 |

**🚨 关键发现：SLAD Full 污染 control pair**

Control pair（walks↔walks）在 CFG 和 Simplified SLAD 下 k50=0.00（无 swap 效应，正确）。但在 SLAD Full 下 k50=3.94±2.89——GDC-based 检测错误地将噪声方向识别为 "semantic locking"，修改了 guidance，导致原本相同的 prompt 产生了不同的 motion。**这是 GDC 检测器的根本缺陷：它测量方向一致性而非语义变化，因此在语义相同的 prompt 上会引入虚假的 "locking" 信号。**

排除 control pair 后 action 维度修正结果：
- Simplified SLAD: Δk50 = −0.08（3 real pairs）
- SLAD Full: Δk50 = −0.51（3 real pairs，但受 control pair 污染影响整体统计）

**Per-seed breakdown（action, all 4 pairs）：**

| Seed | CFG | Simplified SLAD | SLAD Full |
|------|-----|----------------|-----------|
| 42 | 3.95±3.10 | 3.83±2.99 | 3.35±2.33 |
| 2026 | 4.82±3.71 | 4.78±3.65 | **5.80±2.10** |
| 3407 | 4.47±3.13 | 4.44±3.08 | **5.90±1.53** |

SLAD Full 在 seed=2026 和 3407 上**增加**了 k50（变得更差），与 pilot 方向相反。

### 11.2.2 Attribute Direction — 完整 Per-Pair 分解

**Prompt pairs:**
- [0] walks slowly ↔ walks quickly
- [1] jumps high ↔ jumps low
- [2] walks forward ↔ walks backward
- [3] turns left ↔ turns right

| Pair | CFG k50 | Simplified SLAD k50 | Δ vs CFG | SLAD Full k50 | Δ vs CFG |
|------|---------|-------------------|----------|---------------|----------|
| [0] slowly↔quickly | 4.11±0.45 | 4.11±0.45 | 0.00 | 3.88±0.11 | −0.23±0.42 |
| [1] jumps high↔low | 8.96±**5.07** | 8.52±3.98 | −0.44±1.29 | 7.45±2.68 | **−1.51**±3.74 |
| [2] forward↔backward | 5.56±1.86 | 5.29±1.64 | −0.27±0.41 | 4.44±0.79 | **−1.12**±1.07 |
| [3] turns left↔right | 4.88±0.96 | 4.88±0.96 | 0.00 | 5.13±1.28 | +0.26±0.59 |

**关键 pattern：** SLAD Full 在 jumps（−1.51）和 forward/backward（−1.12）上效应最大，这两对也是跨 seed 方差最大的。SLAD Full 似乎通过压制 outlier（seed=2026 jumps k50=19.0→9.5）来降低平均 k50，而非系统性地提前所有 locking。

**Per-seed breakdown（attribute, all 4 pairs）：**

| Seed | CFG | Simplified SLAD | SLAD Full |
|------|-----|----------------|-----------|
| 42 | 4.90±1.71 | 4.71±1.43 | 4.46±1.44 |
| 2026 | **6.87±4.76** | 6.57±3.76 | 5.61±2.00 |
| 3407 | 5.86±2.35 | 5.82±2.29 | 5.61±2.38 |

Seed=2026 是最大方差来源（CFG std=4.76），SLAD Full 将其从 6.87 降到 5.61（−1.26），Simplified SLAD 仅降 0.30。这解释了 SLAD Full 在 attribute 上的 "优势"——它主要作用于 outlier seeds，而非均匀改善。

### 11.2.3 方向不对称（跨条件一致）

方向不对称模式在三种 guidance 条件下高度一致，证明这是模型/数据固有的，不是 guidance 引入的：

**Action:**
| Pair | a→b | b→a | Ratio | 与 pilot 一致？ |
|------|-----|-----|-------|---------------|
| walks↔runs | 4.5 | 6.5 | 0.70 | ✓ |
| sits↔stands | 5.5 | 4.3 | 1.27 | ✓ |
| kicks↔punches | **10.6** | 3.8 | **2.79** | ✓ (pilot 2.54) |

**Attribute:**
| Pair | a→b | b→a | Ratio | 与 pilot 一致？ |
|------|-----|-----|-------|---------------|
| slowly↔quickly | 3.9 | 4.3 | 0.91 | ✓ (pilot 1.03) |
| jumps high↔low | **11.4** | 6.5 | 1.75 | ✓ (pilot 2.12) |
| forward↔backward | 3.7 | 7.4 | 0.50 | ✓ (pilot 0.49) |
| turns left↔right | 4.8 | 4.9 | 0.98 | ✓ (pilot 0.95) |

**结论：** 方向不对称模式在 3 seeds multi-seed 下完全复现 pilot 的 5 seeds 结果。这是跨 seed 稳健的现象。

### 11.2.4 综合评估

| 指标 | Simplified SLAD | SLAD Full | Winner |
|------|----------------|-----------|--------|
| Action Δk50 | −0.06 | +0.60 | Simplified |
| Attribute Δk50 | −0.18 | −0.65 | SLAD Full |
| Action Δk50 std | **0.14** | 2.56 | **Simplified (18× lower)** |
| Attribute Δk50 std | **0.70** | 2.10 | **Simplified (3× lower)** |
| Control pair 污染 | 无 | **严重** (k50 0→4) | Simplified |
| 跨 seed 一致性 | 高 | 低 (action 反转) | Simplified |
| 跨 pair 一致性 | 中 | 低 (高度 pair-dependent) | Simplified |

**最终结论：**

1. **简化版 SLAD 在综合指标上优于 SLAD Full**——尽管平均效应不如 SLAD Full 的极端 case，但在稳定性、一致性、和无副作用方面全面领先。

2. **GDC-based 检测的致命缺陷被 control pair 暴露**——方向一致性（GDC）≠ 语义变化检测。当两个 prompt 语义相同时，GDC 仍可能触发 locking，导致不期望的 guidance 修改。

3. **SLAD Full 的 "优势" 主要来自 outlier suppression 而非系统性改进**——它在 jumps high/low 和 forward/backward 上的 Δk50 很大，但这是因为 seed=2026 的 outlier 被拉回，而非所有 seed 均匀改善。

4. **下一步优先级重排**：
   - ~~恢复 GDC 检测~~（已被 control pair 证伪）
   - ~~恢复 direction decoupling~~（ablation 证明有害）
   - **调优 split point 和 ω_post**（当前 split=0.5, ω_post=1.5 可能不是最优）
   - **MDM 跨模型验证**（简化版只需改 denoise loop 的 ω 调度）

## 12. 证据边界

> [!warning] 当前证据等级
> 结论基于 **5 seeds M0 calibration + 1-2 seeds SLAD vs baselines pilot + 2 seeds ablation + 3 seeds simplified SLAD multi-seed**。总计 6 轮实验。Control pair（walks↔walks）暴露了 GDC 检测器的致命缺陷。

- **GDC-based detection 已被证伪**：control pair（相同 prompt）下 SLAD Full 错误地将 k50 从 0 推到 4，证明 GDC 测量的是方向一致性而非语义变化。
- **Direction decoupling 已被证伪**（ablation）：简单 ω scaling 更好。
- **Semantic projection 已被证伪**（ablation）：仅 attribute 微弱正向（+0.12），不值得保留。
- **简化版 SLAD 是当前最佳 baseline**：稳定性 18× 优于 SLAD Full，无 control pair 污染，跨 seed/跨 pair 一致。
- 效应幅度仍需提升——调优 split point（当前 0.5）和 ω_post（当前 1.5）是下一步。
- **Paper 叙事定稿**：GDC 是错误信号——方向一致性在语义相同的 prompt 上也会触发。简单的两段式 ω 调度在稳定性、安全性和可复现性上全面优于复杂的自适应检测。
