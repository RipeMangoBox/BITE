

---

## GPT 接力摘要（2026-06-17）

### 服务器
- 4090: `ssh 4090` → `user-SYS-7049GP-TRT`, root: `/data/public/ripemangobox/Motion`
- Conda env: `director` (torch 2.3.1+cu121, Python 3.10), TensorBoard: `event-t2m` env
- GPU 0: idle | GPU 1: D6 训练中 (E214/300, ~2.8h remaining as of 2026-06-17 ~13:00)
- 代码位置: `MoLingo/mogen/models/motion_diff_decoder/` + `MoLingo/mogen/train_diff_decoder.py`
- 设计文档: `MoDiffDec/docs/` (4090 上) + `obsidian-vault/ideas/MoDiffDec/` (本地)

### 核心结论

**MoDiffDec** = PiD 风格 Transformer 扩散解码器，替换 MoLingo SAE 的 CNN 解码器。训练基于 rectified flow + frozen SAE encoder。

**测试集上最佳 MPJPE：29.4 mm vs CNN 基线 10.0 mm（差距 3×）。**

三轮实验：

| 轮次 | 关键改动 | 最佳 MPJPE | 核心发现 |
|------|---------|-----------|---------|
| D1_v5 | Baseline diff decoder (29.7M, freq=0.1) | 33.95 | 扩散步数(16→50)无效——积分误差非瓶颈 |
| D1_v6 | (1-t)加权 aux loss + freq=0.3 + p_clean=0.1 | **29.42** | **最大改善来源（-13%）** |
| D6 | 86.7M (d=768, 8层) + 同上 fixes | 30.18 | 更大模型未改善 MPJPE |

**根本瓶颈**：训练目标在 normalized 272-dim 特征空间（L1/flow loss），评估在 22×3 关节空间（MPJPE）。两者经非线性几何变换关联——特征空间优化不完全传导至关节空间。

### Checkpoints（MoLingo 相对路径下）

| Checkpoint | MPJPE | 备注 |
|-----------|-------|------|
| `mogen/checkpoints/ms/modiffdec_D1_v6/best_l1.pt` | **29.42** | 当前最佳 |
| `mogen/checkpoints/ms/modiffdec_D1_baseline/decoder_epoch_0200.pth` | 33.95 | |
| `mogen/checkpoints/ms/modiffdec_D6_large/decoder_epoch_0200.pth` | 30.18 | |
| CNN baseline | 10.02 | SAE 自带 |

### 关键文件
- 方案文档: `obsidian-vault/ideas/MoDiffDec/` (README/architecture/implementation/experiments/progress/evaluation_D1_vs_baseline.md)
- 评估脚本: 4090 上 `/tmp/eval_v6_d6.py`、`/tmp/eval_modiffdec.py`
- 评估结果 JSON: 4090 上 `/tmp/modiffdec_eval_results.json`
- TensorBoard 统一启动: `MoLingo/scripts/run_tb_unified.sh`

### 未完成 / 待尝试
- D6 训练至 E300（traind6_gpu1 session, GPU 1）
- D6 E300 评估
- Phase 3: T2M 集成（MoDiffDec 接入 MoLingo text-to-motion pipeline）
- Phase 4: 消融实验（无 gate/无 noise conditioning/无 text）
- 未尝试 D2-D5/D7 实验矩阵
- 未尝试在关节空间添加直接监督 loss（如 joint position loss）
- 未尝试 MMDiT / DiT 架构替代 Transformer
- 未尝试蒸馏（DMD2）
