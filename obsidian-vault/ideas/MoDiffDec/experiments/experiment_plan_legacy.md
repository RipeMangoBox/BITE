# MoDiffDec: 实验设计与评估方案

---

## 1. 实验阶段总览

```
Phase 1: SAE Baseline     → 验证环境 + 获得 baseline metrics
Phase 2: MoDiffDec Stage 1 → 冻结 encoder，训练 diff decoder（重建任务）
Phase 3: MoDiffDec Stage 2 → 接入 MoLingo T2M，端到端评估生成质量
Phase 4: Ablation & Analysis → 消融实验 + 深度分析
```

## 2. Phase 1: SAE Baseline

### 2.1 目标
- 在 HumanML3D 上训练 MoLingo SAE
- 获得 CNN decoder 重建质量 baseline
- 导出 encoder weights 供后续使用

### 2.2 训练配置

```bash
python mogen/train_sae.py \
    --dataset_name ms \
    --device cuda --gpu_id 0 \
    --batch_size 32 \
    --max_epoch 500 \
    --lr 5e-5 \
    --lr_scheduler cosine \
    --warm_up_iter 1000 \
    --down_t 2 --stride_t 2 \
    --width 1024 --depth 3 \
    --output_emb_width 32 \
    --loss_type l1_smooth \
    --sem_loss_mode token_sentence \
    --cosine_ratio 0.001 \
    --kl_ratio 1e-5 \
    --sentence_ratio 0.1 \
    --data_root /data/public/ripemangobox/Motion/datasets \
    --exp_name baseline_v1 \
    --save_every_e 50 --eval_every_e 50
```

### 2.3 评估指标（Baseline）

| 指标 | 目标值 | 说明 |
|------|--------|------|
| MPJPE (mm) | < 40 | Mean Per Joint Position Error |
| FID | < 0.05 | Fréchet Inception Distance (motion) |
| Diversity | ~9.5 | Motion diversity (should match GT) |
| Reconstruction loss | 收敛 | Training loss curve 稳定 |

### 2.4 记录内容

- Training loss curves (TensorBoard)
- Validation metrics every 50 epochs
- 可视化：GT vs Reconstruction 对比动画
- 最佳 checkpoint epoch

## 3. Phase 2: MoDiffDec Stage 1 — 重建任务

### 3.1 目标
- 验证 diff decoder 在重建任务上优于 CNN decoder
- 确定最优 sigma_max 和噪声分布

### 3.2 实验矩阵

| Exp ID | d_model | num_layers | sigma_max | freq_loss | vel_loss | 说明 |
|--------|---------|------------|-----------|-----------|----------|------|
| D1 | 512 | 6 | 0.8 | 0.0 | 0.0 | Baseline diff decoder |
| D2 | 512 | 6 | 0.5 | 0.0 | 0.0 | 降低 sigma_max |
| D3 | 512 | 6 | 1.0 | 0.0 | 0.0 | 提高 sigma_max |
| D4 | 512 | 6 | 0.8 | 0.1 | 0.0 | + Frequency-aware loss |
| D5 | 512 | 6 | 0.8 | 0.1 | 0.1 | + Velocity loss |
| D6 | 768 | 8 | 0.8 | 0.1 | 0.1 | Larger model |
| D7 | 512 | 6 | 0.8 (log_normal) | 0.1 | 0.1 | 不同 σ 分布 |

### 3.3 训练配置

```bash
python mogen/train_diff_decoder.py \
    --sae_ckpt mogen/checkpoints/ms/sae_baseline_v1/model_epoch500.pth \
    --dataset_name ms \
    --data_root /data/public/ripemangobox/Motion/datasets \
    --batch_size 16 \
    --max_epoch 300 \
    --lr 1e-4 \
    --d_model 512 --num_layers 6 --num_heads 8 \
    --sigma_max 0.8 \
    --freq_loss_weight 0.1 \
    --velocity_loss_weight 0.1 \
    --gpu_id 0 \
    --exp_name D5
```

### 3.4 评估指标（与 CNN decoder 对比）

| 指标 | CNN Decoder | MoDiffDec Target | 提升目标 |
|------|------------|-----------------|---------|
| MPJPE (mm) | baseline | < baseline × 0.9 | >10% 改进 |
| rFID | baseline | < baseline | 越低越好 |
| Per-joint MPJPE | baseline | ↓ 尤其在手/足部位 | 细节关节特别受益 |
| HFER (高频能量比) | baseline | 更接近 GT | 验证高频恢复 |
| 推理时间 (ms) | ~5ms | < 200ms (16 steps) | 可接受 |

### 3.5 推理步数对比

测试不同采样步数的质量-速度 trade-off：

| 步数 | 预期质量 | 预期延迟 |
|------|---------|---------|
| 4 | 略低于 CNN | ~50ms |
| 8 | 接近 CNN | ~100ms |
| 16 | 优于 CNN | ~200ms |
| 32 | 显著优于 CNN | ~400ms |
| 50 | best | ~600ms |

## 4. Phase 3: MoDiffDec Stage 2 — 生成任务

### 4.1 目标
- 将 MoDiffDec 接入 MoLingo T2M pipeline
- 评估对生成质量的端到端影响

### 4.2 集成方式

```
Text → T5 → MoLingo T2M (Rectified Flow + Transformer Decoder)
    → partially denoised latent ẑ → MoDiffDec → motion
```

两个子模式：
- **模式 A (重建)**：MoLingo 运行完整去噪 → clean ẑ → MoDiffDec（σ=0）
- **模式 B (生成增强)**：MoLingo 早期退出（50-70%步数）→ partially denoised ẑ → MoDiffDec（σ>0）

### 4.3 实验矩阵

| Exp ID | T2M Model | Decoder | Early Exit | 说明 |
|--------|-----------|---------|------------|------|
| G1 | MoLingo (full) | CNN decoder | No | 原始 baseline |
| G2 | MoLingo (full) | MoDiffDec (σ=0) | No | 仅 decoder 切换 |
| G3 | MoLingo (50% steps) | MoDiffDec (σ=0.3) | Yes | 早期退出 50% |
| G4 | MoLingo (70% steps) | MoDiffDec (σ=0.15) | Yes | 早期退出 70% |
| G5 | MoLingo (full) | MoDiffDec-F (freq loss) | No | 最佳 decoder |

### 4.4 评估指标（T2M 生成）

| 指标 | 说明 |
|------|------|
| R-Precision Top-1/2/3 | Text-motion retrieval accuracy |
| FID | Fréchet Inception Distance |
| gFID | Generated FID (vs GT distribution) |
| Diversity | Generated motion diversity |
| MM-Dist | Multi-Modal Distance |
| MModality | Multi-Modality |

### 4.5 User Study（可选）

如果指标差异显著，进行：
- 10-20 个 text prompts
- A/B test: CNN decoder vs MoDiffDec
- 3-5 个 evaluators
- 评估维度: 细节丰富度、物理真实性、整体质量

## 5. Phase 4: 消融与分析

### 5.1 核心消融（类比 PiD Table 4）

| 消融条件 | 预期效果 |
|---------|---------|
| Full MoDiffDec | Best |
| - Sigma-aware gate | ↓ 质量（高 σ 时重建差） |
| - Noise latent conditioning | ↓ 早期退出能力 |
| - T5 text condition | ↓ 生成质量（类比 PiD 移除 T2I 先验） |
| - Frequency loss | ↓ 高频细节 |
| - Velocity loss | ↓ 时序平滑性 |

### 5.2 σ_max 敏感性分析

测试 σ_max ∈ {0.2, 0.4, 0.6, 0.8, 1.0} 对重建和生成质量的影响。

### 5.3 频率分析

- 对比 CNN decoder vs MoDiffDec 的 per-joint 频谱
- 量化"低频偏好"改善程度
- 分析哪些关节受益最多（预期：手指、脚踝等细节关节）

### 5.4 可视化分析

- GT vs CNN Decoder vs MoDiffDec 的逐帧对比动画
- Per-joint error heatmap over time
- Velocity profile 对比

## 6. 评估脚本

### 6.1 重建评估

```python
# eval_reconstruction.py
# 评估 SAE + decoder 的重建质量
metrics = {
    'mpjpe': compute_mpjpe(motion_gt, motion_recon),  # mm
    'per_joint_mpjpe': compute_per_joint_mpjpe(...),
    'fid': compute_fid(motion_recon, motion_gt),
    'hfer': compute_hfer(motion_recon, motion_gt),  # 高频能量比
    'velocity_correlation': compute_vel_corr(...),
}
```

### 6.2 T2M 评估

复用 MoLingo 的评估脚本 `mogen/eval_mogen.py`：

```bash
python mogen/eval_mogen.py \
    --model_path checkpoints/molingo_t2m.pth \
    --decoder_type modiffdec \
    --decoder_path checkpoints/modiffdec_D5_e300.pth \
    --num_steps 16 \
    --cfg 2.0
```

## 7. 实验记录模板

每个实验记录以下内容：

```markdown
## Experiment: D1
- Date: 2026-06-XX
- Config: d_model=512, num_layers=6, sigma_max=0.8
- Epochs: 300
- Best epoch: XXX
- Best val loss: XXX

### Reconstruction
- MPJPE: XX.X mm
- FID: X.XXX

### Notes
- Training stability: ...
- Convergence speed: ...
- Issues: ...
```

---

*Next: 开始 Phase 1 实施*
