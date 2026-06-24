# MotionStreamer MoDebug Commands

These scripts formalize the temporary encode-cache runs from `2026-06-07`.

Current remote evidence on `4090`:

- `sa/layer_0` completed at `/data/public/ripemangobox/Motion/experiments/MoDebug/motionstreamer/formal_candidates/trace1_full_eval_sa_cfg_sa_ds_review_20260605_gpu1/sa/layer_0`.
- `cfg_sa/layer_0` completed at the matching `cfg_sa/layer_0` path.
- Both temporary tmux runs disappeared during `layer_1` without Python traceback or failed manifest, leaving empty `official_eval_log/run.log` files for `layer_1`. Full per-layer sweep is no longer the active policy.

Use the resume wrappers for the current representative-layer set by default:

```bash
MODEBUG_DS_APPROVED_EXECUTE=1 bash resume_encodecache_sa_gpu0.sh --execute
MODEBUG_DS_APPROVED_EXECUTE=1 bash resume_encodecache_cfgsa_gpu1.sh --execute
```

Or launch/repair both cards without duplicating existing tmux sessions:

```bash
MODEBUG_DS_APPROVED_EXECUTE=1 bash run_remaining_dual_gpu.sh
```

The dual-GPU launcher waits for both GPUs to have no active compute apps across
several consecutive checks by default. Override only when you intentionally want
to co-run with another job:

```bash
WAIT_FOR_GPUS=0 MODEBUG_DS_APPROVED_EXECUTE=1 bash run_remaining_dual_gpu.sh
```

It also waits while tmux sessions matching `BLOCKING_TMUX_PATTERN` exist. The
default is `storymotion`; set `BLOCKING_TMUX_PATTERN=` to disable that guard.

Current default representative-layer schedule:

- Rule: split 12 layers into `0-3`, `4-7`, `8-11`; take the last layer in each segment.
- GPU0: `sa/layer_3`, `sa/layer_7`, `sa/layer_11`, then baseline, CA guard, CFG_CA guard.
- GPU1: `cfg_sa/layer_3`, `cfg_sa/layer_7`, `cfg_sa/layer_11`.

Estimated completion from a fresh representative-layer launch, using layer 0 timing: roughly 35 hours.

Useful overrides:

```bash
LAYERS=3,7,11 MODEBUG_DS_APPROVED_EXECUTE=1 bash resume_encodecache_sa_gpu0.sh --execute
LAYERS=3,7,11 MODEBUG_DS_APPROVED_EXECUTE=1 bash resume_encodecache_cfgsa_gpu1.sh --execute
LAYERS=3,7,11 MODEBUG_DS_APPROVED_EXECUTE=1 bash run_remaining_dual_gpu.sh
```

The wrappers skip already completed layers, write per-layer `wrapper_exit_status.json`, and keep a timestamped `/tmp/modebug_motionstreamer_resume_*.log`.
