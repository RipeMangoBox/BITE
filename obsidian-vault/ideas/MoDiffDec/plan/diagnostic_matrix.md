---
title: "MoDiffDec Diagnostic Matrix"
status: active
hypothesis: "Each experiment changes one variable and separates strict PiD-style latent-conditioned target-space RF from LDM-style latent-space RF."
created: 2026-06-17T23:20:00+08:00
updated: 2026-06-18T15:35:00+08:00
tags:
  - MoDiffDec
  - experiments
  - diagnostic
source_papers:
  - "[[analysis/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.md|PiD]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]"
---

# MoDiffDec Diagnostic Matrix

## Baseline

| Item | Value |
|---|---|
| CNN decoder baseline | about 10.0 mm MPJPE |
| Current best MoDiffDec | D1_v6 about 29.4 mm MPJPE |
| D6 E200 | about 30.2 mm MPJPE |
| Sampling steps | 16/32/50 steps nearly unchanged |
| Current blocker | target-space from-scratch RF quality, loss/eval mismatch, unsafe checkpoint selection |

## Priority Matrix

| ID | One variable changed | Question | Yes criterion | No criterion | Next action |
|---|---|---|---|---|---|
| T0 | Fix clean estimate: `x0_hat = x_t + (1-t)*v_pred`; rerun D1_v6 setting. | Was the auxiliary-target bug a major cause? | MPJPE ≤ 20 mm. | MPJPE > 20 mm. | Completed; bug is not the main cause. |
| T1 | Add global joint MPJPE and joint velocity loss on correct `x0_hat`. | Does joint-space supervision close most of the gap? | MPJPE ≤ 14 mm. | MPJPE > 14 mm. | Completed; joint loss helps but still fails. |
| T2-SAE | Keep RF target in 272D raw motion; condition on frozen SAE latent; select by validation MPJPE. | Does SAE latent condition make target-space RF competitive? | MPJPE ≤ 16 mm or >5 mm better than T3. | MPJPE > 16 mm and gain ≤5 mm. | If yes, continue PiD-style route. If no, test VAE or seek prior. |
| T3-uncond | Same raw-motion RF architecture and loss, but remove SAE/VAE latent condition. | How much of T2-SAE is due to latent conditioning? | T2-SAE beats T3 by >5 mm. | Gap ≤5 mm. | If no gap, current latent condition is not effective. |
| T4-LDM | SAE latent-space RF + frozen CNN decoder; latent MSE only. | Is latent-space diffusion easier as a non-PiD baseline? | MPJPE ≤ 16 mm. | MPJPE > 16 mm. | Use only as LDM comparison, not PiD evidence. |
| T5-VAE | Replace SAE condition with matched VAE condition under T2 protocol. | Is VAE latent a better condition than SAE? | Improves by >5 mm over matched SAE-conditioned RF. | Improvement ≤5 mm. | Requires matched VAE direct decoder baseline. |
| T6-prior | Initialize or adapt a pretrained raw-space motion diffusion/RF prior. | Is target-space pretrained prior decisive? | MPJPE ≤ 12 mm after fine-tune. | MPJPE > 12 mm. | If yes, claim PiD-style adaptation. If no, abandon PiD framing. |
| T7-text | Add text condition only after reconstruction improves. | Does text prior help reconstruction or T2M? | Improves reconstruction by >3 mm or T2M metrics. | No clear gain. | Keep only for generation phase. |

## Implementation Notes

- T0 must happen before interpreting old D1/D6 results.
- T1 joint loss must be computed from `x0_hat`, not from `v_pred` or `eps_hat`.
- T2-SAE and T3-uncond must share architecture, schedule, losses, sampling steps, and checkpoint selector.
- T4-LDM must be labeled as an LDM-style baseline because diffusion happens in latent space and the frozen CNN remains the decoder.
- T5-VAE requires matched SAE/VAE direct decoder baselines. Do not compare VAE-conditioned RF to SAE direct CNN baseline without reporting VAE direct reconstruction.
- T6-prior is not “MoLingo generator initialization”: MoLingo generator is a latent-space generator, not a raw-motion target-space prior.

## Stop Rule

Stop the current from-scratch MoDiffDec route if T2-SAE does not beat T3-uncond by more than 5 mm and both stay above 16 mm MPJPE. The remaining gap is then unlikely to be fixed by bigger transformers, more sampling steps, or text conditioning.
