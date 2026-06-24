---
title: "MoDebug SLAD M0 Prompt Swap Formal Suite Analysis"
created: 2026-06-14T00:00:00+08:00
updated: 2026-06-14T00:00:00+08:00
status: experiment_analysis
tags:
  - MoDebug
  - MoLingo
  - SLAD
  - semantic_locking
  - counterfactual_swap
  - experiment
related:
  - "[[ideas/MoDebug/2026-06-13_modebug_slad_v3]]"
  - "[[ideas/MoDebug/experiments/molingo/scripts/modebug_slad.py]]"
---

# MoDebug SLAD M0 Prompt Swap Formal Suite Analysis

## Verdict

This run supports the weak but important claim:

> MoLingo shows early trajectory-level source prompt retention under token-unmasking prompt swap across multiple motion dimensions, not only the original walk to run pilot.

The evidence is **endpoint-distance diagnostic evidence**, not yet a formal semantic evaluator or human-evaluation result. It is enough to justify the next GDC/SLAD experiment design, but not enough to claim final semantic control improvement.

## Provenance

Formal suites were run on both 4090 GPUs with MoLingo inference settings preserved:

| Run | GPU | Prompt scope | Remote root | Rows | Failures | Elapsed |
|---|---:|---|---|---:|---:|---:|
| action/control | 0 | control + action swaps | `/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/slad/slad_m0_suite_action_control_seed3407_official_20260613_gpu0` | 102 | 0 | 977.35s |
| attribute/direction | 1 | speed + height + direction swaps | `/data/public/ripemangobox/Motion/experiments/MoDebug/molingo/slad/slad_m0_suite_attribute_direction_seed3407_official_20260613_gpu1` | 102 | 0 | 977.00s |

Settings:

- `cfg=5.5`, `cfg_schedule=constant`
- `sample_steps=32`: inner rectified-flow ODE sampling steps, kept at the MoLingo setting
- `acc=3`: outer token-unmasking acceleration setting, giving `seq_len=150` and `outer_steps=50`
- `seed=3407`
- `directions=a_to_b,b_to_a`
- `swap_iterations=all`, i.e. k = 0..50
- `validate_cfg_equivalence=true`: both suites recorded `max_abs=0.0`, so the CFG path is numerically equivalent to the original MoLingo CFG call

Artifacts:

- `swap_metrics.jsonl`: per k and direction metric rows
- `summary.json`: aggregate mean curves
- `manifest.json`: settings, hashes, limitations, runtime metadata
- `stdout_stderr.log`: full sweep completion log

## Metric

For each pair A/B, the script records affinity to endpoint A in decoded and latent spaces. For analysis, both directions are converted to a common quantity:

- `a_to_b`: `source_retention = affinity_to_a`
- `b_to_a`: `source_retention = 1 - affinity_to_a`

Thus every non-control curve should move from 0 to 1 as more early outer steps are assigned to the source prompt.

Definitions:

- `k50`: interpolated outer swap iteration where source retention crosses 0.50
- `width`: `k75 - k25`, the transition width from 0.25 to 0.75 retention
- Smaller `k50` means earlier source-prompt locking
- Larger `width` means a more gradual or ambiguous transition

## Results

Decoded-space results:

| Prompt pair | Direction | k50 | Width | Endpoint check |
|---|---|---:|---:|---|
| walks vs walks | a_to_b | n/a | n/a | control constant 0.50 |
| walks vs walks | b_to_a | n/a | n/a | control constant 0.50 |
| walks vs runs | a_to_b | 5.75 | 15.64 | 0 to 1 |
| walks vs runs | b_to_a | 5.15 | 6.90 | 0 to 1 |
| sits down vs stands up | a_to_b | 7.32 | 4.52 | 0 to 1 |
| sits down vs stands up | b_to_a | 4.00 | 4.11 | 0 to 1 |
| kicks vs punches | a_to_b | 9.74 | 17.96 | 0 to 1 |
| kicks vs punches | b_to_a | 3.83 | 9.95 | 0 to 1 |
| walks slowly vs walks quickly | a_to_b | 3.97 | 7.00 | 0 to 1 |
| walks slowly vs walks quickly | b_to_a | 3.84 | 6.98 | 0 to 1 |
| jumps high vs jumps low | a_to_b | 11.24 | 16.22 | 0 to 1 |
| jumps high vs jumps low | b_to_a | 5.30 | 11.80 | 0 to 1 |
| walks forward vs walks backward | a_to_b | 3.67 | 1.79 | 0 to 1 |
| walks forward vs walks backward | b_to_a | 7.42 | 16.29 | 0 to 1 |
| turns left vs turns right | a_to_b | 5.56 | 3.26 | 0 to 1 |
| turns left vs turns right | b_to_a | 5.86 | 2.50 | 0 to 1 |

Aggregate over 7 non-control pairs and 14 directions:

| Metric | Mean | Median | Min | Max | Count <= 8 outer steps |
|---|---:|---:|---:|---:|---:|
| decoded k50 | 5.90 | 5.43 | 3.67 | 11.24 | 12/14 |
| latent k50 | 6.17 | 6.37 | 3.69 | 11.14 | 12/14 |
| decoded width | 8.92 | 6.99 | 1.79 | 17.96 | 8/14 |
| latent width | 8.29 | 6.80 | 2.46 | 16.64 | 8/14 |

## Interpretation

The first usable conclusion is that source retention usually becomes dominant very early: 12 of 14 non-control decoded curves cross 0.50 by outer step 8/50. This is compatible with the semantic-locking hypothesis at the trajectory level.

The second conclusion is that locking is not a single universal timestep. Some prompt dimensions are sharp and symmetric:

- `walks slowly` vs `walks quickly`: k50 is 3.97/3.84.
- `turns left` vs `turns right`: k50 is 5.56/5.86 with narrow widths.

Other dimensions are asymmetric or gradual:

- `jumps high` vs `jumps low`: a_to_b is later and wider than b_to_a.
- `kicks` vs `punches`: a_to_b is much later and wider than b_to_a.
- `walks forward` vs `walks backward`: a_to_b is sharp, b_to_a is gradual.

This asymmetry matters for SLAD. A fixed schedule can cover an average transition, but prompt-specific and direction-specific transitions argue for an online detector rather than a hard-coded global split.

## Validity Boundary

What this run supports:

- Multiple prompt dimensions produce early source-retention curves under token-unmasking counterfactual swap.
- The behavior appears in both decoded and latent metrics.
- The run is not explained by a changed CFG implementation, because CFG equivalence is exact in the recorded validation.
- `sample_steps=32` was not a new experimental variable; it is the inner ODE sampling setting used by MoLingo inference.

What this run does not yet support:

- It does not prove human-perceived semantic correctness.
- It does not prove official evaluation improvement.
- It does not estimate variance across random seeds.
- It does not separate prompt wording effects, tokenization effects, and semantic-distance effects.

## DeepSeek Review Notes

DeepSeek review agreed with the limited conclusion: the experiment is a reasonable endpoint-distance proxy for early locking, but the claim should not be upgraded to formal semantic locking without additional validation.

Main risks flagged:

- Endpoint affinity is not equivalent to human semantic judgment.
- Direction asymmetry means a_to_b and b_to_a cannot be treated as interchangeable.
- One seed and one prompt per dimension are not enough for variance or generality claims.
- Prompt wording and tokenization may confound the measured crossing times.

## Next Experiments

Immediate next step:

1. Run the same 8-pair suite with at least 3 seeds, keeping `cfg=5.5`, `sample_steps=32`, and `acc=3`.
2. Add the first inner-ODE GDC trace readout on the same prompt pairs, then check whether GDC transition timing predicts the M0 source-retention transition.
3. Start GDC/SLAD only after the detector is calibrated against these M0 curves; report SLAD as a mechanism evaluation, not as another descriptive swap curve.

Optional validation:

- Add same-action paraphrase pairs such as `runs` vs `sprints`.
- Add token-length controlled prompt variants.
- Add lightweight human or classifier inspection for selected k values near k25/k50/k75.

