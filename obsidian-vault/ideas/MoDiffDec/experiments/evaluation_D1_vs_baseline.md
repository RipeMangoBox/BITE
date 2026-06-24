# MoDiffDec vs MoLingo CNN Decoder — 全量测试集评估

> 日期：2026-06-17  
> 评估数据：HumanML3D test split (4,041 样本)  
> 评估指标：MPJPE (mm), FID, Velocity Correlation, Per-Joint MPJPE  
> MoDiffDec 推理：16-step Euler 采样，clean latent (σ=0)

---

## 1. 总览

| Model | Epoch | MPJPE ↓ | FID ↓ | VelCorr ↑ |
|-------|-------|---------|-------|-----------|
| **SAE CNN** (baseline) | — | **10.00** ± 8.14 | **0.027** | **0.980** |
| MoDiffDec | 50 | 44.82 ± 34.52 | 1.091 | 0.368 |
| MoDiffDec | 100 | 39.93 ± 35.23 | 0.626 | 0.409 |
| MoDiffDec | 150 | 37.64 ± 32.66 | 0.592 | 0.411 |
| MoDiffDec | **200** | **33.95** ± 26.44 | 0.539 | **0.451** |
| MoDiffDec | 250 | 35.84 ± 32.25 | 0.549 | 0.441 |
| MoDiffDec | 300 | 34.61 ± 31.73 | **0.461** | 0.417 |

**趋势**：所有指标随训练改善（E50 → E200 MPJPE 减 24%，FID 减 51%），但与 CNN baseline 差距仍然显著（MPJPE 3.4×，FID 17×，VelCorr 2.2×）。

---

## 2. 训练 vs 测试差异化分析

### 2.1 表面矛盾

- **训练期间 val 指标**持续下降：eval/l1_recon 0.291→0.143（-51%），eval/flow_loss 0.391→0.121（-69%）
- **测试集 MPJPE**仅改善 24%（44.8→34.0），且绝对数值远超 baseline

### 2.2 根因分析

**a) 评估空间不一致（核心原因）**

```
训练 eval/l1_recon:    特征空间 272-dim normalized L1 误差
测试 MPJPE:            关节空间 22×3 的 root-aligned Euclidean 误差
```

二者之间存在非线性几何变换（`recover_from_local_position_batched`）。特征空间小误差在关节空间可能被放大：
- 特征包含 velocity/contact/rotation 等辅助维度（~272 dims）
- 其中仅 8+66=74 dims 直接决定关节点位置
- 模型可能在优化辅助维度时牺牲了关节点精度

**b) 扩散步数不足**

- 当前 16-step Euler 积分求解 rectified flow ODE
- PiD 论文采用 32-50 步（128×128×3=49K dims）
- MoDiffDec 处理 300×272=81.6K dims，应至少需要同等步数
- 步数不足导致积分误差累积，重建偏离真实分布

**c) 模型容量不足**

| | PiD (FLUX.1) | MoDiffDec D1 |
|---|---|---|
| Backbone | PixelDiT 2.6B | Transformer 29.7M |
| 输出维度 | 128×128×3=49K | 300×272=81.6K |
| 参数/输出维度比 | 53,000:1 | 364:1 |

虽然 motion 分布比自然图像简单（物理约束、低自由度），但 87× 的容量差距仍可能是瓶颈。

**d) 潜在训练-推理 mismatch**

- **训练时**：`z_sigma = (1-σ)·z + σ·ξ`（带噪声的 latent），σ ∈ [0, 0.8]
- **推理时**：传入 σ=0（clean latent）
- Sigma-aware gate：`gate = σ(Linear(h) - α·σ)`，当 σ=0 时 gate 始终对 latent 开放
- 训练阶段模型学习"根据噪声水平调节 latent 注入"，但推理时 σ=0 是一个**分布外（OOD）条件**——训练从未见过 σ=0 + 纯 noise x_T 的组合（训练时 x_t 由插值构建，始终包含真实信号）

**e) 训练初期 noise 问题已修复，但尚未验证**

- v5 已实现 (1-t) 加权辅助 loss + freq_weight 0.1→0.3
- 但 v5 尚未训练到收敛，D1 结果基于旧版 loss（freq 持续升高）

---

## 3. Per-Joint 分析

选取代表性关节（pelvis 为根关节点，误差固定为 0）：

| Joint | CNN | MoDiffDec E200 | MoDiffDec E300 | 比值 (E200/CNN) |
|-------|-----|---------------|---------------|-----------------|
| pelvis (0) | 0.0 | 0.0 | 0.0 | — |
| l_hand (4) | 9.6 | 34.4 | 36.4 | 3.6× |
| r_hand (7) | 13.1 | 45.1 | 45.0 | 3.4× |
| l_foot (10) | 14.4 | 49.5 | 49.3 | 3.4× |
| head (15) | 14.4 | 39.2 | 42.0 | 2.7× |
| r_foot (18) | 12.6 | 44.1 | 42.7 | 3.5× |
| l_toe (21) | 14.2 | 54.9 | 55.8 | 3.9× |

**结论**：
- 所有关节按相似比例退化（2.7-3.9×），无明显"受益关节"
- 足部/脚趾（l_foot, r_foot, l_toe）误差最大——这些关节运动幅度小、细节多，对高频信息敏感
- 头部（head）缩小比例最小（2.7×），因头部运动较平稳

---

## 4. 改进路线

| 优先级 | 方向 | 预期影响 | 实现代价 |
|--------|------|---------|---------|
| **P0** | 增加推理步数（32/50 steps） | 验证步数不足假设 | 低（仅改参数） |
| **P0** | 修复训练/推理 mismatch（训练时引入 σ=0） | 消除 OOD 条件 | 中（改 noise schedule） |
| **P1** | 训练 v5（新 loss + freq=0.3）并重评 | 验证 loss 修复效果 | 高（~5h GPU） |
| **P1** | D6 大模型（d_model=768, layers=8） | 验证容量假设 | 中（~7h GPU） |
| **P2** | 在训练 eval 中增加 per-joint MPJPE 监控 | 更直接的训练指标 | 低 |
| **P2** | 多步数 vs 质量曲线（4/8/16/32/50） | Pareto 最优步数 | 低（仅推理） |

---

## 5. 速查：最佳 Checkpoint

| 指标 | 最优 Epoch | 最优值 |
|------|-----------|--------|
| MPJPE | E200 | 33.95 mm |
| FID | E300 | 0.461 |
| VelCorr | E200 | 0.451 |

---

## 7. 步数消融（E200，全量 test set）

| 步数 | MPJPE |
|------|-------|
| 16 | **34.14 mm** |
| 32 | 34.15 mm |
| 50 | 34.55 mm |

**结论：增加扩散步数无效。** 32 步与 16 步几乎一致，50 步反而略差。说明离散化/积分误差**不是 MPJPE 差距的主因**——模型本身学到的 velocity field 指向的 reconstruction 在关节空间中就是不准的。

修正后诊断优先级：
1. **特征空间 vs 关节空间 misalignment** —— 训练 L1 在 normalized 272-dim 特征空间，评估 MPJPE 在 22×3 关节空间
2. **模型容量/训练策略** —— D1_v6（修复 loss）+ D6（86.7M）正在训练中测试
3. ~~扩散步数~~ —— 已排除
4. ~~σ=0 OOD~~ —— 不太可能是主因（p_clean=0.1 已在 v6 中修复）

最佳整体：**E200** (`decoder_epoch_0200.pth`)，MPJPE 和 VelCorr 均为最优，FID 次优。

---

## 6. 原始数据

完整 JSON：`/tmp/modiffdec_eval_results.json`（4090 服务器）

评估脚本：`/tmp/eval_modiffdec.py`

```bash
# 复现命令
cd /data/public/ripemangobox/Motion/MoLingo
/home/ripemangobox/miniconda3/envs/director/bin/python /tmp/eval_modiffdec.py
```
