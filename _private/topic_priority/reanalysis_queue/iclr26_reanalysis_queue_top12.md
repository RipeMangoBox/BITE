# ICLR26 Reanalysis Queue

## 1. ACCORD: Alleviating Concept Coupling through Dependence Regularization for Text-to-Image Diffusion Personalization
- path: `obsidian-vault/paper/ICLR_2026/P__ACCORD_Alleviating_Concept_Coupling_through_Dependence_Regularization_for_Text-to-Image_Diffusion_Personalization.md`
- severity: `critical`
- reasons:
  - manual_review_placeholder 残留，说明文档未完成
  - DreamBench table caption 混入 theorem 文本，图表 grounding 已串线
  - 5.2 公式表达可疑，属于核心方法层风险

## 2. Bridging Degradation Discrimination and Generation for Universal Image Restoration
- path: `obsidian-vault/paper/ICLR_2026/P__Bridging_Degradation_Discrimination_and_Generation_for_Universal_Image_Restoration.md`
- severity: `critical`
- reasons:
  - 5.2 扩散采样公式高度可疑，疑似转写/幻觉
  - Figure 1 / Figure 2 错位，Table 2 caption 串入别的表
  - 旧 Topic placeholder 残留过，说明导出链也不稳

## 3. Why We Need New Benchmarks for Local Intrinsic Dimension Estimation
- path: `obsidian-vault/paper/ICLR_2026/P__Why_We_Need_New_Benchmarks_for_Local_Intrinsic_Dimension_Estimation.md`
- severity: `critical`
- reasons:
  - known_formula_suspect_lidl 命中
  - 5.2 把 LIDL 原理压成裸 d-D，关键理论解释失真
  - 你已人工指出 Figure 1 / 5.2 质量明显错误

## 4. Agentic Reinforced Policy Optimization
- path: `obsidian-vault/paper/ICLR_2026/P__Agentic_Reinforced_Policy_Optimization.md`
- severity: `critical`
- reasons:
  - 5.2 公式语法断裂，核心机制不可置信
  - 结果解释依赖该公式，无法靠局部修补恢复

## 5. A Study of Posterior Stability in Time-Series Latent Diffusion
- path: `obsidian-vault/paper/ICLR_2026/P__A_Study_of_Posterior_Stability_in_Time-Series_Latent_Diffusion.md`
- severity: `critical`
- reasons:
  - 后验坍缩核心公式疑似自指/错误
  - 该问题会污染整篇方法论解释

## 6. 3D-aware Disentangled Representation for Compositional Reinforcement Learning
- path: `obsidian-vault/paper/ICLR_2026/P__3D-aware_Disentangled_Representation_for_Compositional_Reinforcement_Learning.md`
- severity: `high`
- reasons:
  - Figure 4 caption 吞入 Table 2，图表 grounding 错位
  - 关键公式表达可疑，方法解释不稳

## 7. A Reward-Free Viewpoint on Multi-Objective Reinforcement Learning
- path: `obsidian-vault/paper/ICLR_2026/P__A_Reward-Free_Viewpoint_on_Multi-Objective_Reinforcement_Learning.md`
- severity: `high`
- reasons:
  - 结果锚点漂移到无关超参表
  - 正文结构错位在方法/实验层都可见

## 8. Bridging the Distribution Gap to Harness Pretrained Diffusion Priors for Super-Resolution
- path: `obsidian-vault/paper/ICLR_2026/P__Bridging_the_Distribution_Gap_to_Harness_Pretrained_Diffusion_Priors_for_Super-Resolution.md`
- severity: `high`
- reasons:
  - Figure 1/2 错位，Table 2 caption 吞并 Table 3/4
  - 图表系统性串线，影响整体可信度

## 9. A Balanced Neuro-Symbolic Approach for Commonsense Abductive Logic
- path: `obsidian-vault/paper/ICLR_2026/P__A_Balanced_Neuro-Symbolic_Approach_for_Commonsense_Abductive_Logic.md`
- severity: `high`
- reasons:
  - Table 1 caption 混入 RQ1/Table 2 文本
  - 实验与问题设定 grounding 已污染

## 10. A Biologically Plausible Dense Associative Memory with Exponential Capacity
- path: `obsidian-vault/paper/ICLR_2026/P__A_Biologically_Plausible_Dense_Associative_Memory_with_Exponential_Capacity.md`
- severity: `high`
- reasons:
  - Figure 1 被碎裂成 a/b 残片
  - 图表说明和正文混线，指数容量主张支撑不稳

## 11. A Probabilistic Hard Concept Bottleneck for Steerable Generative Models
- path: `obsidian-vault/paper/ICLR_2026/P__A_Probabilistic_Hard_Concept_Bottleneck_for_Steerable_Generative_Models.md`
- severity: `high`
- reasons:
  - Table 1 与 Figure 3 描述混杂，编号漂移
  - 核心 steerability 结论的图表 anchoring 不可信

## 12. A Fano-Style Accuracy Upper Bound for LLM Single-Pass Reasoning in Multi-Hop QA
- path: `obsidian-vault/paper/ICLR_2026/P__A_Fano-Style_Accuracy_Upper_Bound_for_LLM_Single-Pass_Reasoning_in_Multi-Hop_QA.md`
- severity: `high`
- reasons:
  - 有重复 framework/experiment 结构的外部审查证据
  - formula 与章节拼接异常，建议整篇重跑更稳
