---
title: "EMNLP Review Notes - Real-Time Streaming Reasoning with Temporal Self-Distillation Policy Optimization"
type: review-notes
venue: EMNLP
created: 2026-06-30T14:42:00+08:00
updated: 2026-06-30T15:45:11+08:00
tags:
  - review/emnlp
  - status/draft
  - streaming-reasoning
  - rlvr
aliases:
  - TSDPO Review
pdf_ref: "_attachments/17411_Real_Time_Streaming_Reas.pdf"
---

# Real-Time Streaming Reasoning with Temporal Self-Distillation Policy Optimization

## Submission Draft

### Paper Summary

The paper studies policy optimization for real-time streaming reasoning, where a model reasons over progressively revealed text instead of waiting for the full context. The proposed method, TSDPO, addresses a credit-assignment issue in applying GRPO to streaming rollouts: final-answer rewards give only a trajectory-level signal, while different reasoning segments are generated under different partial observations. TSDPO keeps the GRPO final-answer advantage but redistributes it across streaming segments using answer-conditioned likelihood differences as a training-time support signal. Experiments on Qwen3-1.7B and Qwen3-4B report improvements over GRPO on several in-domain benchmarks, with additional ablations on credit granularity, normalization, OOD performance, and serving latency.

### Summary Of Strengths

1. The paper targets a relevant problem: reasoning under partial, streaming input rather than only in the standard full-context setting.

2. The method is simple and well matched to the problem structure. Segment-level credit assignment is a natural fit for streaming rollouts, and the method does not require process labels or an external teacher.

3. The paper includes useful ablations on allocation granularity and position-wise normalization, plus an initial latency analysis under vLLM serving.

4. The paper is easy to follow.

### Summary Of Weaknesses

**Major weaknesses**

1. The efficiency claim is not fully consistent across tables. Table 1 suggests that TSDPO reduces total length relative to GRPO across all main settings, but Table 2 shows full TSDPO with higher total length than GRPO on both GSM-symbolic P1 and P2. The TSDPO numbers in Table 2 also do not match the corresponding Table 1 entries. This needs explanation before the efficiency conclusion is convincing.

2. The “real-time” claim is only weakly supported. The paper includes one latency table under a simulated 150 wpm input rate, but does not report per-task latency, final-answer latency, variance, or sensitivity to input speed. Given the title, the real-time evaluation should be more central.

3. The answer-conditioned likelihood gap is a plausible proxy for segment usefulness, but the paper does not validate that it tracks causal contribution. A segment can be answer-compatible while still redundant or non-causal.

**Minor weaknesses**

4. The novelty over StreamingThinker combined with recent self-distilled RLVR / SDPO-style methods could be positioned more sharply. The segment-level budget-preserving adaptation is useful, but the paper should better distinguish it from nearby privileged-information self-distillation work.

5. The OOD result on GSM-Infinite is mixed: TSDPO is shorter than GRPO but less accurate. The conclusion about generalization should be stated more cautiously.

### Comments Suggestions And Typos

**Major suggestions**

1. Reconcile the Table 1 and Table 2 results. If the tables use different checkpoints, variants, hyperparameters, or evaluation protocols, state this explicitly.

2. Expand the latency evaluation. At minimum, report per-dataset latency, final-answer latency, variance, and sensitivity to input arrival speed.

3. Add an analysis of learned segment weights, preferably with qualitative examples, to show whether high-weight segments correspond to genuinely useful reasoning.

**Minor suggestions**

4. Report standard deviations or confidence intervals, since several GRPO-to-TSDPO accuracy gains are small.

5. Clarify the difference between TSDPO-streaming and full TSDPO in Table 2.

6. Check Table 7 for consistency. It lists `KL coefficient: False`, while the appendix text states \(\beta = 0.01\).

### Confidence

2

### Soundness

2.5

### Excitement

3

### Overall Assessment

2.5

### Best Paper Justification

Not applicable.

## New Reviewer Checklist Draft

### Appropriateness

Yes

### Appropriateness Justification

The paper is relevant to computational processing of natural language because it studies reasoning over text streams and evaluates on language/math/QA tasks.

### Formatting

Yes

### Formatting Justification

I did not observe an obvious formatting violation in the provided PDF.

### Length

Yes

### Length Justification

I did not observe an obvious length violation in the provided PDF.

### Anonymity

Yes

### Anonymity Justification

The PDF is anonymized and the metadata does not expose author identity.

### Limitations

Yes

### Limitations Justification

The paper includes a section entitled “Limitations.”

### Overall Level

Yes

### Overall Level Justification

The submission appears to be a good-faith research paper with a concrete method, experiments, ablations, limitations, and references.

### Responsible Checklist

Needs manual confirmation in OpenReview.

### Need Ethics Review

No

### Ethics Review Justification

I do not see an obvious need for separate ethics review. The main concerns are methodological and reproducibility-related.

### Other Issues

No prompt injection or AI-review manipulation instructions were found in the supplied Markdown note or PDF text/object streams.

## Private Reading Notes

### Prompt Injection Check

**Conclusion:** No evidence of prompt injection or hidden instructions intended to manipulate review.

Checks performed:

- Read the Markdown note and extracted PDF text.
- Searched PDF text and raw extraction for terms such as `prompt`, `ignore`, `instruction`, `reviewer`, `AI`, `assistant`, `system`, `accept`, `reject`, `rating`, `OpenReview`, and `ARR`.
- Inspected PDF metadata and embedded files.
- Expanded the PDF with `qpdf --qdf --object-streams=disable` and searched the object stream.

Observed:

- PDF metadata is anonymized; no author field is exposed.
- `pdfinfo` reports no JavaScript and no embedded files.
- Matched terms are normal paper content or references, e.g. `OpenAI`, `DeepSeek-AI`, `LLM`, and citation titles.
- `qpdf` matches such as `ignore_newline` are QDF formatting markers, not author instructions.

### Quick Concept Map

- **Read-then-think:** Sees full context before reasoning. Useful reference, but not a fair streaming baseline.
- **StreamingThinker (SFT):** Streaming supervised baseline trained on constructed streaming CoT traces.
- **GRPO:** Uses final-answer reward and assigns the same group-normalized advantage to the whole rollout.
- **TSDPO:** Keeps GRPO's final-answer advantage but redistributes it across streaming segments.
- **Acc:** Final answer accuracy.
- **S.Len:** Tokens generated during the streaming phase.
- **D.Len:** Tokens generated during the final deep reasoning phase.
- **T.Len:** Total generated tokens.

### My Key Takeaway

TSDPO does not make GRPO “support streaming.” The streaming rollout format already exists. TSDPO changes how credit is assigned inside such rollouts: from uniform trajectory-level credit to answer-conditioned segment-level redistribution.

### GRPO vs TSDPO

| Dimension | GRPO | TSDPO |
|---|---|---|
| Reward source | Final-answer correctness | Final-answer correctness |
| Credit granularity | Uniform over rollout | Weighted over segments |
| Training-only privilege | None | Verified answer for rescoring |
| External teacher | No | No |
| Inference visibility | No answer privilege | No answer privilege |
| Main change | Outcome-only RL | Segment-aware credit redistribution |

## PDF

![[17411_Real_Time_Streaming_Reas.pdf]]
