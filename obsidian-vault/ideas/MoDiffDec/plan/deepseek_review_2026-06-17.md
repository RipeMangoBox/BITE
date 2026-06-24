---
title: "DeepSeek Review 2026-06-17"
status: reviewed
hypothesis: "Strict review identifies missing target-space prior, loss/eval mismatch, and a rectified-flow clean-estimate bug as the main issues."
created: 2026-06-17T23:20:00+08:00
updated: 2026-06-17T23:20:00+08:00
tags:
  - MoDiffDec
  - DeepSeek
  - review
source_papers:
  - "[[analysis/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.md|PiD]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]"
---

# DeepSeek Review 2026-06-17

> [!warning] Superseded scope
> This review predates the 2026-06-18 PiD/LDM terminology correction in [[ideas/MoDiffDec/plan/deepseek_pid_correction_2026-06-18|deepseek_pid_correction_2026-06-18]]. Its recommendation to run “T2 latent-space RF” is now downgraded to an LDM-style baseline, not the PiD mainline.

## Session

- Tool: DeepSeek MCP `deepseek-reasoner`
- Session id: `440918dcaa53`
- Role: strict research engineering reviewer

## Main Review Conclusions

1. **SAE motion-text alignment is not an explanation for the reconstruction gap.** Current Stage 1 uses no text condition, and the CNN decoder reaches about 10 mm using the same SAE latent.
2. **SAE vs VAE is not P0.** VAE may be easier for diffusion because of a more Gaussian latent distribution, but this cannot explain a 29 mm vs 10 mm reconstruction gap by itself.
3. **Current implementation is not faithful PiD adaptation.** PiD depends on a pretrained target-space diffusion prior. Current MoDiffDec is a from-scratch raw-motion RF decoder.
4. **MoLingo generator cannot simply warm-start raw-space MoDiffDec.** MoLingo generator works in latent token space and then calls the CNN decoder; it is not a raw-motion target-space diffusion prior.
5. **A P0 code bug must be fixed before further diagnosis.** Given `x_t = t*x0 + (1-t)*eps` and `v = x0 - eps`, clean motion is `x_t + (1-t)*v_pred`. Current auxiliary losses used `x_t - t*v_pred`, which estimates noise if `v_pred` is correct.

## Root-Cause Ranking

| Rank | Cause | Review judgment |
|---:|---|---|
| 1 | Wrong clean estimate for auxiliary losses | Strong immediate blocker; must rerun baseline after fix. |
| 2 | Feature-space loss vs joint-space MPJPE mismatch | Strong likely cause; needs joint loss. |
| 3 | Missing target-space pretrained prior | Strong reason current route should not claim PiD adaptation. |
| 4 | raw 272D space may be harder than latent space | Plausible; needs T2 diagnostic. |
| 5 | SAE text alignment weakness | Not relevant to current reconstruction failure. |
| 6 | SAE vs VAE | Secondary variable after clean baseline. |

## DeepSeek Recommendations Integrated

- Run T0 first: fix `x0_pred` and rerun D1_v6 settings.
- Only after T0, run T1 joint-space loss and T2 latent-space RF.
- Do not continue expanding model size as primary strategy.
- Do not proceed to T2M integration until reconstruction approaches CNN baseline.
- If no raw-space pretrained motion diffusion prior is used, describe the work as conditional RF decoding, not PiD adaptation.

## Open Checks

- Verify whether `recover_from_local_position_batched` is differentiable enough for training. If it uses NumPy or detached operations anywhere, use a differentiable PyTorch equivalent.
- For 272D HumanML3D features, confirm exact feature ordering before adding joint loss.
- Report matched CNN baselines for SAE and VAE if comparing SAE vs VAE.
