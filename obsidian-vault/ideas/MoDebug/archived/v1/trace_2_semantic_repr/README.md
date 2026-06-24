---
title: Trace 2 — Semantic Motion Representation
created: 2026-06-02
updated: 2026-06-02T23:45:00+08:00
status: demoted
---

# Trace 2: Semantic Motion Representation

对应 Line 2，旧称 Track C。

> [!warning] 降级为参考资料
> 该方向赛道拥挤，且 Motion 域缺少 DINOv2 级别 frozen semantic encoder。当前不投入双卡测试。

## 技术参考

REPA 类比：

```text
L_repa_motion = MSE(Proj(h_t), f_motion_enc(motion_gt))
```

VAVAE 类比：

```text
L_vavae = L_recon + lambda_KL L_KL + lambda_align (1 - cos(Proj(z), f_enc(x)))
```

候选 encoder：TMR、MoCHA、MoLingo SAE、COME/MoCMAE。它们都不足以作为 DINOv2 等价替代。

## 重新激活条件

- Trace 1 和 Trace 3 已有可复核结果。
- 有证据表明某 motion encoder 语义质量足够强。
- 有明确差异化角度，而不是简单迁移图像域 REPA/VAVAE。
