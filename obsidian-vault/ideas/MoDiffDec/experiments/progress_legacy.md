# MoDiffDec: 进度追踪

> 开始日期：2026-06-16
> 服务器：4090 (user-SYS-7049GP-TRT)

---

## Phase 1: 环境搭建与基线验证

### Step 1.1: Conda 环境
- [x] 服务器无外网，使用现有 `director` conda 环境
- [x] 验证 PyTorch 2.3.1+cu121 + CUDA 可用
- [x] 验证 T5-large 模型路径 (`/data/public/ripemangobox/Motion/Text-encoder/t5-large`)
- [x] 从 event-t2m 复制缺失包: tensorboard, absl, markdown, werkzeug, grpc
- [x] Patch wandb 导入为可选（所有 `*.py` 文件）
- [x] 验证所有 import: `SAETrainer, VAE, Text2MotionDatasetMSBabel, eval_vae_ms` OK

### Step 1.2: 数据验证
- [x] HumanML3D 数据集路径: `/data/public/ripemangobox/Motion/datasets/HumanML3D/`
- [x] 272-dim 预处理数据: `/data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D/`
- [x] 创建 symlink: `datasets/HumanML3D_272 → 272-dim-HumanML3D`
- [x] sentence_t5 缓存存在

### Step 1.3: SAE Baseline 训练
- [ ] 启动 SAE 训练（已有最佳 checkpoint MPJPE ~10mm 可复用）
- [ ] 或直接使用已有最佳 SAE 模型进行 MoDiffDec 开发

**Phase 1 完成标准**: SAE 训练完毕，MPJPE < 40mm，encoder weights 可用

---

## Phase 2: MoDiffDec 实现

### Step 2.1: 核心模块
- [ ] 创建 `mogen/models/motion_diff_decoder/` 目录
- [ ] 实现 `config.py`
- [ ] 实现 `sigma_aware_gate.py`
- [ ] 实现 `motion_diff_decoder.py`
- [ ] 实现 `decoder_trainer.py`
- [ ] 创建训练脚本 `train_diff_decoder.py`

### Step 2.2: 单元测试
- [ ] SigmaAwareGate forward test
- [ ] MotionDiffDecoder forward test
- [ ] 端到端 training step test
- [ ] 验证梯度流动

### Step 2.3: Stage 1 训练
- [ ] 加载 frozen SAE encoder
- [ ] 启动 D1-D7 实验矩阵中的至少 3 个
- [ ] 监控 loss curves
- [ ] 与 CNN decoder 对比重建质量

**Phase 2 完成标准**: MoDiffDec 重建 MPJPE 优于 CNN decoder baseline

---

## Phase 3: T2M 集成

### Step 3.1: Pipeline 集成
- [ ] 修改 MoLingo T2M 推理代码支持 diff decoder
- [ ] 实现 early exit 推理模式
- [ ] 端到端 test run

### Step 3.2: 生成实验
- [ ] 运行 G1-G5 实验矩阵
- [ ] 评估 T2M 生成指标
- [ ] 对比 CNN decoder vs MoDiffDec

**Phase 3 完成标准**: MoDiffDec 接入 T2M pipeline，生成指标不劣于 baseline

---

## Phase 4: 消融与分析

### Step 4.1: 核心消融
- [ ] 无 sigma-aware gate
- [ ] 无 noise latent conditioning
- [ ] 无 text condition
- [ ] 无 frequency loss
- [ ] 无 velocity loss

### Step 4.2: 深度分析
- [ ] σ_max 敏感性
- [ ] Per-joint 频谱分析
- [ ] 推理步数 vs 质量 trade-off
- [ ] 可视化对比动画

**Phase 4 完成标准**: 完整消融表格 + 深度分析报告

---

## 实验日志

### 2026-06-16
- [x] 完成研究调研 (`motion_detail_enhancement_research_ideas.md`)
- [x] 完成 MoDiffDec 方案设计（README + architecture + implementation + experiments）
- [x] 环境搭建：使用 `director` conda env + 补丁（无外网）
- [x] 所有核心 import 验证通过
- [x] 启动 MoDiffDec D1 训练 v4（遇到 batch indexing bug，修复后重训至 Epoch 8）

### 2026-06-17
- [x] **TensorBoard 监控完善**: 对照 MoLingo SAE trainer，补充以下监控能力：
  - Per-iteration logging（每 10 batch 写入 TensorBoard，非之前仅 per-epoch）
  - 分项 loss: `train/loss`, `train/flow_loss`, `train/freq_loss`, `train/vel_loss`
  - `train/grad_norm`, `train/lr` per-iteration
  - `epoch/train_loss` 等 epoch 级别汇总
  - 5% validation split（held-out eval）
  - `eval/l1_recon`, `eval/mse_recon`, `eval/flow_loss` 每 10 epoch
  - `eval/recon_l1` 每 50 epoch（16-step 采样重建）
- [x] 创建 `scripts/run_tensorboard.sh`（端口 6008，event-t2m env）
- [x] TensorBoard 启动：`http://user-SYS-7049GP-TRT:6008/`
- [x] 重启训练 v5：`traind1_v5` tmux session，日志 `logs/remote4090/traind1_v5.log`

### 2026-06-17 D1 训练完成
- [x] D1 训练完成（300/300 epochs，~4.8h）
- [x] 最佳验证指标在 E240：l1=0.143, mse=0.115, flow=0.124
- [x] 最佳重建 L1 在 E200：0.271（16 步 Euler 采样）
- [x] Checkpoints 保存于 E50/100/150/200/250/300
- [x] TensorBoard 日志完整（6 条 scalar 曲线 × 17,550 步）
- [x] **全量测试集评估完成** → `evaluation_D1_vs_baseline.md`
  - CNN baseline: MPJPE 10.00mm, FID 0.027, VelCorr 0.980
  - MoDiffDec 最佳 (E200): MPJPE 33.95mm, FID 0.539, VelCorr 0.451
  - 差距 3.4× (MPJPE)、20× (FID)、2.2× (VelCorr)
  - 根因：评估空间不一致 + 扩散步数不足 + 容量差距 + σ=0 OOD

---

## 关键决策记录

| 日期 | 决策 | 理由 |
|------|------|------|
| 2026-06-16 | 使用 MoLingo SAE 作为 backbone（非 Kimodo/HY-Motion） | 轻量、代码已有、SAE 训练可控 |
| 2026-06-16 | Decoder 使用 Transformer 架构（非 CNN） | PiD 使用 DiT，时序数据适合 Transformer |
| 2026-06-16 | 初期不做蒸馏 | 先验证核心机制有效，蒸馏是锦上添花 |
| 2026-06-16 | 保留 T5 text condition | PiD 消融证明 T2I 先验不可替代 |

---

## 问题追踪

| ID | 日期 | 问题 | 状态 |
|----|------|------|------|
| - | - | - | - |
