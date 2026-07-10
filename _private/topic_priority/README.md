# ICLR 2026 Topic Priority Outputs

- generated_at: `2026-05-12T09:29:59.427938+00:00`
- input_manifest: `_private/iclr26_batch/status/iclr26_all_papers_status.jsonl`
- pdf_root: `_private/resmax_downloads/pdfs/ICLR_2026`
- total_manifest_rows: `5348`
- processed_rows: `5348`
- sample_stride: `1`
- limit: `all`

## Outputs

- assignments: `iclr26_topic_assignments.jsonl`
- summary: `iclr26_topic_summary.csv`
- top papers: `iclr26_topic_top_papers.csv`
- taxonomy: `iclr26_topic_taxonomy.json`

## Notes

- Classification is document-only and uses local PDF front matter plus the manifest title.
- Each paper gets one primary topic and up to two secondary topics.
- Summary ranking is by primary-topic count, which prioritizes the largest hot directions first.

## Top Primary Topics

- LLM Reasoning & Agents (llm_reasoning_agents): `1854` papers | examples: $\nabla$-Reasoner: LLM Reasoning via Test-Time Gradient Descent in Latent Space | $\textbf{Re}^{2}$: Unlocking LLM Reasoning via Reinforcement Learning with Re-solving | $p\textrm{-less}$ Sampling: A Robust Hyperparameter-Free Approach for LLM Decoding
- Diffusion & Generative Modeling (diffusion_generation): `732` papers | examples: $\textit{MADFormer}$: Mixed Autoregressive and Diffusion Transformers for Continuous Image Generation | $PhyWorldBench$: A Comprehensive Evaluation of Physical Realism in Text-to-Video Models | A Bayesian Nonparametric Framework For Learning Disentangled Representations
- Optimization & Theory (optimization_theory): `452` papers | examples: $\mu$LO: Compute-Efficient Meta-Generalization of Learned Optimizers | ``Noisier'’ Noise Contrastive Estimation is (Almost) Maximum Likelihood | A Block Coordinate Descent Method for Nonsmooth Composite Optimization under Orthogonality Constraints
- Efficient Models, Scaling & Systems (efficient_llm_systems): `431` papers | examples: $\mathbf{Li_2}$: A Framework on Dynamics of Feature Emergence and Delayed Generalization | 3DGEER: 3D Gaussian Rendering Made Exact and Efficient for Generic Cameras | 3DSMT: A Hybrid Spiking Mamba-Transformer for Point Cloud Analysis
- Reinforcement Learning (reinforcement_learning): `350` papers | examples: $AutoDrive\text{-}P^3$: Unified Chain of Perception–Prediction–Planning Thought via Reinforcement Fine-Tuning | 3D-aware Disentangled Representation for Compositional Reinforcement Learning | A New Approach to Controlling Linear Dynamical Systems
- Robustness, OOD & Adaptation (robustness_ood): `347` papers | examples: $\pi^3$: Permutation-Equivariant Visual Geometry Learning | A Brain-Inspired Gating Mechanism Unlocks Robust Computation in Spiking Neural Networks | A Relative Error-Based Evaluation Framework of Heterogeneous Treatment Effect Estimators
- Multimodal & Vision-Language (multimodal_vlm): `289` papers | examples: A Comprehensive Information-Decomposition Analysis of Large Vision-Language Models | A High Quality Dataset and Reliable Evaluation for Interleaved Image-Text Generation | A Rich Knowledge Space for Scalable Deepfake Detection
- Alignment, Safety & Preference Learning (alignment_safety): `263` papers | examples: $\alpha$-DPO: Robust Preference Alignment for Diffusion Models via $\alpha$ Divergence | A Guardrail for Safety Preservation: When Safety-Sensitive Subspace Meets Harmful-Resistant Null-Space | ActiveDPO: Active Direct Preference Optimization for Sample-Efficient Alignment
- Time Series & Sequential Modeling (time_series_sequential): `243` papers | examples: 3D Scene Prompting for Scene-Consistent Camera-Controllable Video Generation | A foundation model with multi-variate parallel attention to generate neuronal activity | A General Spatio-Temporal Backbone with Scalable Contextual Pattern Bank for Urban Continual Forecasting
- Privacy, Security & Trustworthiness (privacy_security): `122` papers | examples: A Bayesian Nonparametric Framework for Private, Fair, and Balanced Tabular Data Synthesis | A General Framework for Black-Box Attacks Under Cost Asymmetry | Adaptive Attacks on Trusted Monitors Subvert AI Control Protocols
