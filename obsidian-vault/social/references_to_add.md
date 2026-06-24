---
title: "待补充文献 — 统一场景感知动作生成方案参考"
date: 2026-06-17
---

# 待补充文献列表

> 以下论文在报告中引用但尚未收录于 `paper_list.csv`，按类别列出论文名称和下载链接。

## 已确认在 paper_list.csv 中的论文（无需补充）

| 论文 | venue |
|------|-------|
| Dyn-HSI: Dynamic Worlds Dynamic Humans Generating Virtual Human Scene Interaction Motion in Dynamic Scenes | arXiv 2026 |
| MotionCraft: Crafting Whole Body Motion with Plug and Play Multimodal Controls | AAAI 2025 |
| UniMuMo: Unified Text Music and Motion Generation | AAAI 2025 |
| MoRL: Reinforced Reasoning for Unified Motion Understanding and Generation | arXiv 2026 |
| DualFlow: Unified Multi-Modal Interactive & Reactive 3D Motion Generation via Rectified Flow | ICLR 2026 |
| UniHSI: Unified Human Scene Interaction via Prompted Chain of Contacts | ICLR 2024 |
| MoConVQ: Unified Physics-Based Motion Control via Scalable Discrete Representations | TOG 2024 |
| HMVLM: Human Motion Vision Language Model via MoE LoRA | NeurIPS 2025 |
| CLAW: Composable Language-Annotated Whole-body Motion Generation | arXiv 2026 |
| TRUMANS: Scaling Up Dynamic Human Scene Interaction Modeling | CVPR 2024 |
| LINGO: Autonomous Character Scene Interaction Synthesis from Text Instruction | SIGGRAPH Asia 2024 |
| A Survey on Human Interaction Motion Generation | IJCV 2025 |
| InterGen: Diffusion based Multi human Motion Generation under Complex Interactions | 2024 |
| ReMoS: 3D Motion Conditioned Reaction Synthesis for Two Person Interactions | 2024 |
| Rank-1 EWC: Avoid Catastrophic Forgetting with Rank-1 Fisher from Diffusion Models | ICLR 2026 |
| FIRE: Frobenius-Isometry Reinitialization for Balancing the Stability–Plasticity Tradeoff | ICLR 2026 |
| CompSLOT: Plug-and-Play Compositionality for Boosting Continual Learning with Foundation Models | ICLR 2026 |
| Sketch2Colab: Sketch-Conditioned Multi-Human Animation via Controllable Flow Distillation | CVPR 2026 |
| MDM: Human Motion Diffusion Model | ICLR 2023 |
| AMD: Anatomical Motion Diffusion with Interpretable Motion Decomposition and Fusion | AAAI 2024 |
| MotionGPT3: Human Motion as a Second Modality | 2024 |
| Motion Agent: A Conversational Framework for Human Motion Generation with LLMs | 2024 |
| AvatarGPT: All-in-One Framework for Motion Understanding Planning Generation | 2024 |
| Kimodo: Scaling Controllable Human Motion Generation | 2026 |
| FLAME: Free-form Language-based Motion Synthesis & Editing | AAAI 2023 |

---

## 需要补充到 paper_list.csv 的论文

### A. 核心架构参考

**1. Lance: Unified Multimodal Modeling by Multi-Task Synergy**
- ByteDance Research, arXiv 2026.05
- 链接: https://arxiv.org/abs/2605.18678
- GitHub: https://github.com/bytedance/Lance
- HF: https://huggingface.co/bytedance-research/Lance

**2. EVA01: Unified Native 3D Understanding and Generation via Mixture-of-Transformers**
- SeeleAI, arXiv 2026.05
- 链接: https://arxiv.org/abs/2605.16745
- Project: https://www.seeles.ai/research/pages/EVA01

### B. 多模态运动生成

**3. OmniMotion-X: Versatile Multimodal Whole-Body Motion Generation**
- arXiv 2025.10
- 链接: https://arxiv.org/abs/2510.19789

**4. OmniMotion: Multimodal Motion Generation with Continuous Masked Autoregression**
- arXiv 2025.10
- 链接: https://arxiv.org/abs/2510.14954

### C. 实时 / 游戏相关

**5. Matrix-Game 3.0: Real-Time and Streaming Interactive World Model with Long-Horizon Memory**
- Skywork AI, arXiv 2026.04
- 链接: https://arxiv.org/abs/2604.08995

**6. Matrix-Game 2.0: An Open-Source, Real-Time, and Streaming Interactive World Model**
- Skywork AI, arXiv 2025.08
- 链接: https://arxiv.org/abs/2508.13009

**7. FlowAct-R1: Towards Interactive Humanoid Video Generation**
- ByteDance, arXiv 2026.02
- 链接: https://arxiv.org/abs/2601.10103

### D. 持续学习 / 防遗忘

**8. FLAME: Adaptive Mixture-of-Experts for Continual Multimodal Multi-Task Learning**
- arXiv 2026.05
- 链接: https://arxiv.org/abs/2605.09355

### E. 场景交互 (HSI)

**9. SAMP: Stochastic Scene-Aware Motion Prediction**
- Hassan et al., ICCV 2021
- 链接: https://arxiv.org/abs/2108.08284
- Dataset: https://samp.is.tue.mpg.de

**10. SceneDiffuser: Diffusion-based Generation, Optimization, and Planning in 3D Scenes**
- Huang et al., CVPR 2023
- 链接: https://arxiv.org/abs/2301.06015
- GitHub: https://github.com/scenediffuser/Scene-Diffuser

**11. HUMANISE: Language-conditioned Human Motion Generation in 3D Scenes**
- Wang et al., NeurIPS 2022
- 链接: https://arxiv.org/abs/2210.09729
- Project: https://silverster98.github.io/HUMANISE/

### F. 人类交互运动

**12. PriorMDM: Human Motion Diffusion as a Generative Prior**
- Shafir et al., ICLR 2024
- 链接: https://arxiv.org/abs/2303.01418
- Project: https://priormdm.github.io/priorMDM-page/
- GitHub: https://github.com/priorMDM/priorMDM

**13. InterDiff: Generating 3D Human-Object Interactions with Physics-Informed Diffusion**
- Xu et al., ICCV 2023
- 链接: https://arxiv.org/abs/2308.16905
- Project: https://sirui-xu.github.io/InterDiff/

### G. 数据集论文

**14. GTA-Human: Playing for 3D Human Recovery**
- Cai et al., TPAMI 2024
- 链接: https://arxiv.org/abs/2110.07588
- Project: http://caizhongang.com/projects/GTA-Human/

---

## 汇总（共 14 篇待补充）

| # | 论文简称 | 下载链接 |
|---|---------|---------|
| 1 | Lance | https://arxiv.org/abs/2605.18678 |
| 2 | EVA01 | https://arxiv.org/abs/2605.16745 |
| 3 | OmniMotion-X | https://arxiv.org/abs/2510.19789 |
| 4 | OmniMotion | https://arxiv.org/abs/2510.14954 |
| 5 | Matrix-Game 3.0 | https://arxiv.org/abs/2604.08995 |
| 6 | Matrix-Game 2.0 | https://arxiv.org/abs/2508.13009 |
| 7 | FlowAct-R1 | https://arxiv.org/abs/2601.10103 |
| 8 | FLAME (MoE Continual) | https://arxiv.org/abs/2605.09355 |
| 9 | SAMP | https://arxiv.org/abs/2108.08284 |
| 10 | SceneDiffuser | https://arxiv.org/abs/2301.06015 |
| 11 | HUMANISE | https://arxiv.org/abs/2210.09729 |
| 12 | PriorMDM | https://arxiv.org/abs/2303.01418 |
| 13 | InterDiff | https://arxiv.org/abs/2308.16905 |
| 14 | GTA-Human | https://arxiv.org/abs/2110.07588 |
