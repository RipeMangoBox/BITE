# TAMR Stage4.1 D2b Evaluation

## Scope

- Goal: test whether the D2a gains survive when the full motion encoder is unfrozen under the same minimal event-time head.
- D2b setting: keep D2a's minimal head, attention pooling, masked InfoNCE, and warm-start recipe, but expand motion unfreezing from `last-2 blocks` to the full `motion_encoder`.
- Run dir: `RUN_DIR/stage4_1_d2b`
- Date: `2026-04-11`

## Training Config

- Model: `tmr_d2b`
- Dataset: `humanml3d_e`
- Warm-start: `RUN_DIR/stage4_1_d1/last_weights`
- Motion unfreeze scope: full `motion_encoder`
- Still frozen: `text_encoder`, `motion_decoder`
- Compatibility fix: keep `motion_encoder.seqTransEncoder.enable_nested_tensor = False` and `use_nested_tensor = False`
- Event loss: same D1/D2a masked InfoNCE with attention pooling
- Optimizer: `AdamW`
- Learning rate: `1e-4`
- Batch size: `32`
- Max epochs: `100`
- Device: `1 GPU`

### Commands

```bash
bash scripts/run_stage4_1_d2b.sh |& tee RUN_DIR/stage4_1_d2b/train.out
```

```bash
conda run -n TMR python retrieval.py \
  run_dir=RUN_DIR/stage4_1_d2b \
  protocol=all \
  device=cuda \
  ckpt=last \
  batch_size=256 |& tee RUN_DIR/stage4_1_d2b/retrieval.out
```

## D2b Metrics

### Validation Event Alignment

| Metric | First | Last | Best |
| --- | ---: | ---: | ---: |
| `val_evt_align_acc` | 0.3199 | 0.3486 | 0.4332 |

| Metric | First | Last | Best Min |
| --- | ---: | ---: | ---: |
| `val_evt_align` | 2.2932 | 2.2482 | 2.0095 |

### Retrieval

| Protocol | t2m R@1 | t2m R@5 | t2m R@10 | m2t R@1 | m2t R@5 | m2t R@10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| normal | 15.54 | 43.92 | 60.14 | 22.30 | 47.97 | 54.05 |
| threshold@0.95 | 30.41 | 53.38 | 68.24 | 31.08 | 51.35 | 58.78 |
| nsim | 22.00 | 53.00 | 67.00 | 33.00 | 54.00 | 63.00 |
| guo | 39.84 | 75.00 | 88.28 | 38.28 | 75.00 | 89.84 |

## D1 vs D2a vs D2b

### Validation Event Alignment

| Metric | D1 | D2a | D2b |
| --- | ---: | ---: | ---: |
| `val_evt_align_acc` first | 0.1118 | 0.3471 | 0.3199 |
| `val_evt_align_acc` last | 0.3587 | 0.3315 | 0.3486 |
| `val_evt_align_acc` best | 0.3960 | 0.4061 | 0.4332 |
| `val_evt_align` first | 3.2866 | 2.1684 | 2.2932 |
| `val_evt_align` last | 2.0884 | 2.0694 | 2.2482 |

### Retrieval Gate: normal

| Metric | D1 | D2a | D2b | Delta (D2b - D2a) |
| --- | ---: | ---: | ---: | ---: |
| normal t2m R@1 | 9.46 | 13.51 | 15.54 | +2.03 |
| normal t2m R@5 | 22.97 | 37.16 | 43.92 | +6.76 |
| normal t2m R@10 | 27.70 | 52.03 | 60.14 | +8.11 |
| normal m2t R@1 | 2.70 | 16.22 | 22.30 | +6.08 |
| normal m2t R@5 | 13.51 | 37.84 | 47.97 | +10.13 |
| normal m2t R@10 | 14.19 | 48.65 | 54.05 | +5.40 |

### Retrieval Gate: nsim

| Metric | D1 | D2a | D2b | Delta (D2b - D2a) |
| --- | ---: | ---: | ---: | ---: |
| nsim t2m R@1 | 13.00 | 17.00 | 22.00 | +5.00 |
| nsim t2m R@5 | 29.00 | 46.00 | 53.00 | +7.00 |
| nsim t2m R@10 | 37.00 | 61.00 | 67.00 | +6.00 |
| nsim m2t R@1 | 3.00 | 26.00 | 33.00 | +7.00 |
| nsim m2t R@5 | 12.00 | 49.00 | 54.00 | +5.00 |
| nsim m2t R@10 | 18.00 | 56.00 | 63.00 | +7.00 |

## Gate Conclusion

- D2a had already shown that `partial unfreeze + minimal head` does not damage the main representation and can even improve retrieval.
- D2b does **not** reintroduce the original Stage4 first-round degradation.
- Instead, full motion unfreeze under the D2a minimal-head recipe improves both `normal` and `nsim` again.
- There is no core retrieval metric in `normal` or `nsim` that drops relative to D2a.

Conclusion:

- **D2b 通过 gate，Go D3。**

Interpretation:

- The earlier Stage4 failure mode was not caused by unfreezing the motion backbone alone.
- The failure mode was the combination of `too much unfreeze scope + overly heavy auxiliary branch`.
- Once the auxiliary branch is reduced to the D1/D2a minimal event head, even full motion unfreezing remains beneficial instead of destructive.

## Recommendation

- **Go D3 with D2b as the Stage4.1 winner.**
- Keep D2a as the key control result proving that partial unfreeze is already safe.
- Use D2b as the default Stage4.1 backbone setting for the next step, because it strictly improves the retrieval-first gate over D2a.
