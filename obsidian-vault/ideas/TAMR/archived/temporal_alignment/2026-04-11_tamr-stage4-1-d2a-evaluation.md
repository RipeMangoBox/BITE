# TAMR Stage4.1 D2a Evaluation

## Scope

- Goal: test whether partial motion-backbone unfreezing still harms the main retrieval representation under the D1 minimal event-time head.
- D2a setting: continue from D1 and unfreeze only the last 2 motion encoder transformer blocks.
- Run dir: `RUN_DIR/stage4_1_d2a`
- Date: `2026-04-11`

## Training Config

- Model: `tmr_d2a`
- Dataset: `humanml3d_e`
- Warm-start: `RUN_DIR/stage4_1_d1/last_weights`
- Motion unfreeze scope: `motion_encoder.seqTransEncoder.layers[-2:]`
- Still frozen: motion encoder projection/tokens/positional dropout path, text encoder, motion decoder
- Event loss: same D1 masked InfoNCE with attention pooling
- Optimizer: `AdamW`
- Learning rate: `1e-4`
- Batch size: `32`
- Max epochs: `100`
- Device: `1 GPU`

### Commands

```bash
conda run -n TMR python train.py \
  model=tmr_d2a \
  data=humanml3d_e \
  run_dir=RUN_DIR/stage4_1_d2a \
  dataloader.batch_size=32 \
  dataloader.num_workers=0 \
  trainer.accelerator=gpu \
  trainer.devices=1 \
  trainer.max_epochs=100 \
  trainer.log_every_n_steps=20
```

```bash
conda run -n TMR python retrieval.py \
  run_dir=RUN_DIR/stage4_1_d2a \
  protocol=all \
  device=cuda \
  ckpt=last \
  batch_size=256
```

## D2a Metrics

### Validation Event Alignment

| Metric | First | Last | Best |
| --- | ---: | ---: | ---: |
| `val_evt_align_acc` | 0.3471 | 0.3315 | 0.4061 |

| Metric | First | Last | Best Min |
| --- | ---: | ---: | ---: |
| `val_evt_align` | 2.1684 | 2.0694 | 2.0211 |

### Retrieval

| Protocol | t2m R@1 | t2m R@5 | t2m R@10 | m2t R@1 | m2t R@5 | m2t R@10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| normal | 13.51 | 37.16 | 52.03 | 16.22 | 37.84 | 48.65 |
| threshold@0.95 | 27.70 | 43.24 | 59.46 | 20.27 | 42.57 | 53.38 |
| nsim | 17.00 | 46.00 | 61.00 | 26.00 | 49.00 | 56.00 |
| guo | 28.12 | 64.84 | 86.72 | 30.47 | 64.06 | 86.72 |

## D1 vs D2a

### Retrieval Gate

| Metric | D1 | D2a | Delta (D2a - D1) |
| --- | ---: | ---: | ---: |
| normal t2m R@1 | 9.46 | 13.51 | +4.05 |
| normal t2m R@5 | 22.97 | 37.16 | +14.19 |
| normal t2m R@10 | 27.70 | 52.03 | +24.33 |
| normal m2t R@1 | 2.70 | 16.22 | +13.52 |
| normal m2t R@5 | 13.51 | 37.84 | +24.33 |
| normal m2t R@10 | 14.19 | 48.65 | +34.46 |
| nsim t2m R@1 | 13.00 | 17.00 | +4.00 |
| nsim t2m R@5 | 29.00 | 46.00 | +17.00 |
| nsim t2m R@10 | 37.00 | 61.00 | +24.00 |
| nsim m2t R@1 | 3.00 | 26.00 | +23.00 |
| nsim m2t R@5 | 12.00 | 49.00 | +37.00 |
| nsim m2t R@10 | 18.00 | 56.00 | +38.00 |

### Event Alignment

| Metric | D1 | D2a | Delta (D2a - D1) |
| --- | ---: | ---: | ---: |
| `val_evt_align_acc` first | 0.1118 | 0.3471 | +0.2353 |
| `val_evt_align_acc` last | 0.3587 | 0.3315 | -0.0272 |
| `val_evt_align_acc` best | 0.3960 | 0.4061 | +0.0101 |
| `val_evt_align` first | 3.2866 | 2.1684 | -1.1182 |
| `val_evt_align` last | 2.0884 | 2.0694 | -0.0190 |

## Conclusion

- D2a **passes** the retrieval gate.
- There is no sign of the original Stage4 failure mode under this partial-unfreeze setup.
- Instead of degrading retrieval, D2a improves both `normal` and `nsim` substantially.

Interpretation:

- The D1 minimal event-time head appears to stabilize fine-tuning enough that unfreezing only the last 2 motion blocks does not collapse the global representation.
- D2a is therefore a valid `Go` point for proceeding to D2b, but D2b should still be treated as a fresh high-risk experiment because it changes the unfreeze scope qualitatively.

## Recommendation

- **Go D2b, but keep the same retrieval-first gate.**
- Reuse the D2a setup as the baseline for D2b.
- If D2b shows any drop on `normal` or `nsim`, stop there and keep D2a as the Stage4.1 winner.
