---
title: "The Hot Mess of AI: How Does Misalignment Scale With Model Intelligence and Task Complexity?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/The_Hot_Mess_of_AI_How_Does_Misalignment_Scale_With_Model_Intelligence_and_Task_Complexity.pdf
project_link: https://huggingface.co/datasets/hot-mess/hot-mess-data
code_link: https://github.com/haeggee/hot-mess-of-ai
aliases:
- EIAFBVD
- HMAHDMSMITC
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "推理长度（思考步骤数）和任务复杂度是导致错误不一致性增加的关键可调节因素；模型规模对不一致性的影响取决于任务难度。"
primary_logic: "通过偏差-方差分解定义错误不一致性，揭示更大更智能的模型虽然总体误差更低，但在复杂任务上变得更不一致，其失败由方差主导，这挑战了仅靠规模实现对齐的假设。"
claims:
- "Across all multitask settings (GPQA, SWE-BENCH, MWE, synthetic), longer reasoning and action sequences increase error-incoherence."
- "Natural variation in reasoning length leads to significantly higher error-incoherence for longer sequences, with minimal accuracy difference."
- "On MMLU, QWEN3 models become less incoherent on easy tasks but more incoherent on the hardest tasks as model size increases."
- "In synthetic optimizer experiments, larger models reduce bias faster than variance, making them variance-dominated and more incoherent."
---

# The Hot Mess of AI: How Does Misalignment Scale With Model Intelligence and Task Complexity?

> [!tip] 核心洞察
> 通过偏差-方差分解定义错误不一致性，揭示更大更智能的模型虽然总体误差更低，但在复杂任务上变得更不一致，其失败由方差主导，这挑战了仅靠规模实现对齐的假设。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AI的混乱：模型智能与任务复杂度如何影响错误不一致性？ |
| 英文题名 | The Hot Mess of AI: How Does Misalignment Scale With Model Intelligence and Task Complexity? |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=sIBwirjYlY) · [GitHub](https://github.com/haeggee/hot-mess-of-ai) · [Project](https://huggingface.co/datasets/hot-mess/hot-mess-data) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Error-Incoherence Analysis Framework (Bias-Variance Decomposition) |
| Dataset | GPQA (multiple-choice), SWE-BENCH (agentic coding), MMLU (QWEN3 scaling), Synthetic optimizer (quadratic) |

> [!tip] 效果简介
> - GPQA (multiple-choice) 上，KL error-incoherence 为 错误不一致性随推理长度增加而上升，不同模型家族斜率不同，对比 短推理长度组，变化 显著增加 (例如 QWEN3 各尺寸斜率几乎相同)。
> - SWE-BENCH (agentic coding) 上，coverage error-incoherence 为 错误不一致性随行动步数（动作/消息数）增加而上升，对比 少行动步数组，变化 O4-MINI 0.47→0.60, O3-MINI 0.12→0.25。
> - MMLU (QWEN3 scaling) 上，Brier error-incoherence 为 对于最难的问题组，错误不一致性随模型规模增大而上升；对于简单问题则下降，对比 最小模型 (0.6B)，变化 趋势在困难组呈正向，简单组呈负向。

## 概要

该工作将AI的失败归因于两种本质不同的成分：由模型与期望目标系统偏差造成的**偏差**（bias，非对齐失败），以及由测试时随机性导致的**方差**（variance，输出不一致性失败）。传统评估聚焦于整体错误率，却忽视了随着模型规模与任务复杂度提升，错误的性质可能从“一致地错误”转为“随机地失败”。论文的核心问题是：在模型智能和任务复杂度增长的过程中，错误是由偏差主导还是方差主导？这种“错误不一致性”（error‑incoherence）能否通过简单扩大模型规模消除？

为回答上述问题，作者提出了一套**基于偏差‑方差分解的错误不一致性分析框架**。该框架通过对同一问题采集至少30个随机采样（变化随机种子、few‑shot上下文），将期望误差 $\mathrm{ERROR}$ 分解为系统性偏差 $\mathrm{BIAS}^2$ 与不一致性方差 $\mathrm{VARIANCE}$ 之和：
$$
\mathrm{ERROR} = \mathrm{BIAS}^2 + \mathrm{VARIANCE}.
$$
随后定义**错误不一致性**为总方差占总误差的比例（Equation 2），取值0（纯系统偏差）到1（纯随机失败）。该度量可适配多种损失函数（KL散度、Brier评分等），并在多项选择、代码生成、合成优化等不同类型任务上进行计算。

通过分析多个前沿模型（如Claude Sonnet 4、O3‑MINI、O4‑MINI、QWEN3系列）以及合成优化器，研究得到以下关键结论：

* **推理长度与行动步骤是错误不一致性的强驱动因素**。在 GPQA、SWE‑BENCH、MWE 及合成任务中，模型思考或行动序列越长，错误不一致性越高（Figure 2）。即使控制任务和推理预算，自然产生的长度变化也足以显著提升不一致性，而准确率变化甚微（Figure 3）。
* **模型规模对错误不一致性的影响并非单调，而取决于任务难度**。在 QWEN3 家族上，对于简单问题（MMLU 最短推理长度分组），错误不一致性随参数量增加而下降；对于最难问题，不一致性反而上升（Figure 5）。合成优化器实验进一步揭示：增大模型规模主要降低偏差，方差下降缓慢，导致最终误差由方差主导（Figure 6）。
* **集成可有效抑制方差，且不增加偏差**。将同一问题的多个预测取平均，方差按 $1/E$ 的幂律下降，错误不一致性随之降低（Figure 7）。相比之下，单纯增大模型的推理预算虽能略微改善不一致性，但效果远小于自然推理长度变化所带来的影响。

这些发现表明，仅在准确率上追求 scaling law 不足以保证模型行为的一致性，尤其在长程推理和高难度任务场景下，方差可能成为主导失败模式。论文的“错误不一致性”概念为诊断和缓解此类“hot mess”提供了量化工具，并揭示了偏差‑方差权衡在 AI 对齐研究中的新维度。



随着大语言模型和智能体系统在数学推理、科学问答、代码生成等复杂任务中展现出越来越强的能力，AI 安全研究的焦点逐渐从“模型是否会犯错”转向“模型如何犯错”。传统上，评估模型性能主要依赖总体准确率或单次通过率（pass@1），但这些指标掩盖了错误的内部结构：模型究竟是因为系统性地偏离了真实目标（**对齐失败**，即偏差），还是因为对同一输入产生了随机、不一致的输出（**不一致性失败**，即方差）而出错，对于预测模型在超人类尺度上的风险至关重要。如果失败主要由偏差主导，那么模型可能以可预测的方式偏离人类意图，表现为典型的“对齐问题”；如果失败主要由方差主导，那么模型的错误则类似于工业事故，难以预判和归因，这在自主智能体执行长程任务时尤为危险。

然而，当前缺乏有效的分析框架来区分这两类失败模式，并考察它们如何随模型智能和任务复杂度的提升而演化。已有研究主要关注通过缩放模型规模来降低平均错误率，但逐渐有证据表明，更大、推理能力更强的模型在困难任务上可能表现出更显著的输出不一致性——即模型的错误中随机扰动的成分占比升高（参见 Figure 2, Figure 5）。这种“热混乱”现象（a hot mess）意味着，仅靠规模化可能不足以使模型在对齐层面变得更加可靠，反而可能在复杂场景下放大不安全行为的不可预测性。

本文直接回应上述缺口，提出一个基于偏差–方差分解的**错误不一致性（error-incoherence）分析框架**。具体而言，作者利用交叉熵误差（以及 Brier 评分等其他损失函数）的 Kl-divergence 分解，将模型在给定问题上的期望误差分解为系统性偏差（KL-偏差）和随机方差（KL-方差）两部分：

$$\underbrace{\mathbb{E}_{\varepsilon}[\mathbf{CE}(y,f_\varepsilon)]}_{\mathrm{ERROR}} = \underbrace{D_{\mathrm{KL}}(y\|\bar{f})}_{\mathrm{BIAS}^2} + \underbrace{\mathbb{E}_{\varepsilon}[D_{\mathrm{KL}}(\bar{f}\|f_\varepsilon)]}_{\mathrm{VARIANCE}}$$

进而定义**错误不一致性**为所有问题上方差占总误差的比例：

$$\mathrm{ERROR-INCOHERENCE}(Q,f_\varepsilon) := \frac{\sum_i \mathrm{VARIANCE}(q_i,f_\varepsilon)}{\sum_i \mathrm{ERROR}(q_i,f_\varepsilon)}$$

该指标取值在 $[0, 1]$ 之间，$0$ 表示错误全部来自统一的、系统性的偏差（纯对齐失败），$1$ 表示错误完全由测试时的随机波动引起（纯不一致性失败）。基于该定义，本文系统研究了多个前沿模型（如 Claude Sonnet 4, O3-MINI, O4-MINI）和模型族（QWEN3 0.6B–32B）在 GPQA、SWE-BENCH、MMLU 以及合成优化器任务上的错误结构，重点分析推理长度、模型规模和任务难度等可调节因素对错误不一致性的影响。

初步结果揭示出三组关键规律，它们共同构成了本研究的核心动机：第一，无论在多选题还是智能体编码任务中，**推理/行动长度的增加普遍导致错误不一致性上升**（Figure 2），且这种效应无法仅通过增大推理预算得到显著抑制（Figure 7(a)）；第二，模型规模对错误不一致性的影响**依赖于任务难度**——在简单任务上，扩大模型尺寸可以降低不一致性，但在最困难的任务组中，更大的模型反而变得更加不一致（Figure 5(e)）；第三，在合成优化器实验中，模型规模的增长更偏向于减少偏差，而方差的下落速度较慢，致使**大型模型在总体误差中方差成分占主导**（Figure 6）。这些发现表明，仅靠缩放模型并期望其自动对齐可能是一种高风险策略，需要在控制方差增长方面引入新的干预手段（例如重复采样集成，如 Figure 7(b) 所示）。

综上，本文的动机不在于提出新的推理技术或对齐算法，而是**建立一种可操作的错误结构分析方法**，以揭示模型智能增长过程中被忽视的“不一致性陷阱”，从而为未来 AI 系统的安全评估和风险外推奠定基础。



## 核心方法与创新机理

本研究的关键创新在于将 AI 安全评估从**单一误差量级**推进到**误差成分分解**，并提出可操作的度量与分析框架，从而揭示模型智能与任务复杂度如何影响失败的**不一致性**。与传统的以总体准确率或 pass@1 为核心指标的评估范式相比，本文的核心改变可归结为以下两个相互耦合的创新滑块：

1. **从“错误率”到“错误不一致性”的度量转换**  
   现有基线方法仅关心模型是否正确（例如分类准确率或单元测试通过率），却无法区分失败是源自系统性的对齐偏差，还是源自测试时随机的、不一致的输出。本文基于偏差–方差分解，定义了**错误不一致性（Error-Incoherence）**度量：
   $$ \text{ERROR-INCOHERENCE}(Q, f_\varepsilon) := \frac{\sum_i \text{VARIANCE}(q_i, f_\varepsilon)}{\sum_i \text{ERROR}(q_i, f_\varepsilon)} $$
   该度量取值 0（纯偏差驱动失败，模型始终以同一方式犯错）到 1（纯方差驱动失败，模型行为高度随机），将 AI 的不可靠性量化为**方差在总误差中的占比**。技术上，文章通过 KL 散度分解（$ \text{ERROR} = \text{BIAS}^2 + \text{VARIANCE} $）将交叉熵误差拆分为系统偏差与随机波动（见 Section 2.1, Equation 1），并在 Brier 评分和 0/1 损失上进行了鲁棒性验证（Appx. A）。这一度量从根本上改变了“模型变得更聪明”的解读方式：虽然更大模型的总误差可能更低，但其失败可能由方差主导，呈现出更难以预测的不一致行为。

2. **面向稳定估计的采样策略革新**  
   传统评估往往对每个问题仅采样 1–3 次，难以捕捉测试时随机性对输出分布的影响。本文强制每道题收集**至少 30 个样本**，并通过控制随机种子与 few-shot 上下文变化，构建稳定的偏差和方差估计（Section 3）。实证表明，大约 30 个样本后偏差–方差估计趋于稳定（Figure 21），这一采样密度是得出“更长推理序列、更大模型规模会增加不一致性”等核心结论的统计基础。

以上两个创新滑块共同构成了一个**可扩展的分析框架**，其管道模块包括：
- **多样本响应收集**：对每个题目生成 30+ 条回答，系统记录推理长度、动作步数等过程信息；
- **偏差–方差分解**：分别在分类（KL/Brier/0-1 损失）、代码编写（覆盖率误差，Appx. B.3）和合成优化（MSE 损失）等任务上量化系统误差与随机波动；
- **错误不一致性聚合**：将全类问题的方差与总误差求比，形成跨任务的统一度量；
- **基于长度的分组及缩放分析**：以推理长度（或动作步数）为任务复杂度的代理，将题目按中位数分组，研究错误不一致性如何随长度和模型尺寸变化（Section 3.1, 3.2）。

该框架在 GPQA、SWE-BENCH、MMLU 和合成优化器等多种设置上被验证有效：
- **推理长度效应**：所有被评估模型（包括前沿的 O4-MINI、SONNET 4 和 QWEN 系列）均表现出错误不一致性随推理长度/动作步数增加而上升的趋势（Figure 2）；
- **规模异质效应**：在 MMLU 上，QWEN3 模型在简单任务上随规模增大变得更一致，但在最难任务组上反而更不一致（Figure 5）；
- **偏差下降快于方差**：合成优化器实验显示，增大模型规模更多压缩的是偏差，而非方差，导致最终误差由方差主导（Figure 6）。

总体而言，该研究的核心创新不在于提出新的模型架构或训练目标，而在于**重新定义我们如何衡量模型的失败**：通过将“错误”拆解为“偏见”与“混乱”两部分，并为可靠估计这两部分设计严格的采样协议，论文为理解 AI 对齐的规模效应提供了新的概念工具和实证基础。



![[assets/figures/papers/iclr26_0016_sIBwirjYlY_The_Hot_Mess_of_AI_How_Does_Misalignment_Scale_W/figures/001_Figure_1.jpg]]
*Figure 1: AI can fail because it is misaligned, and produces consistent but undesired outcomes, or because it is incoherent, and does not produce consistent outcomes at all. These failures correspond to bias and variance respectively. As we extrapolate risks from AI, it is important to understand whether failures from more capable models performing more complex tasks will be bias or variance dominated. Bias dominated failures will look like model misalignment, while variance dominated failures will resemble industrial accidents. (top left) Qualitatively, we observe that AI models fail in unpredictable and inconsistent ways. Often, these failures can be fixed by resampling. (top right) To quantify thi...*

本错误不一致性分析框架通过大量重复采样与偏差‑方差分解，量化AI模型在测试时的不一致性（incoherence），并将传统“总误差”拆解为系统性偏差（Bias²）和随机方差（Variance）两个可诊断的成分。整体流程围绕四个核心模块组织，输入为问题集和模型，输出为错误不一致性指标以及该指标随推理长度和模型规模的缩放关系。

1. **多采样回答收集**  
   对每个问题执行 $M\ge 30$ 次独立采样，通过变动随机种子、少样本顺序等方式引入测试时随机性。对于多项选择题，记录每个选项的预测概率；对于代理编码任务（SWE‑BENCH），记录单元测试通过/失败二进制向量；对于开放式生成（MWE），将回答通过嵌入模型映射为向量。该模块的输出是能够反映模型预测分布多样性的样本集，是后续分解的数据基础。

2. **KL偏差‑方差分解**  
   对每个问题计算期望交叉熵误差 $\mathrm{ERROR}$，并按等式（1）将其分解为KL偏差（$\mathrm{BIAS}^2$，平均预测与真实分布的KL散度）和KL方差（$\mathrm{VARIANCE}$，各次预测与平均预测的期望散度）。对于Brier评分、覆盖率误差等非KL损耗，框架适配相应的分解形式，始终维持“$\mathrm{ERROR} = \mathrm{BIAS}^2 + \mathrm{VARIANCE}$”的结构。该模块输出每个问题的偏差和方差分量。

3. **错误不一致性聚合**  
   定义错误不一致性（Error‑Incoherence）为所有问题的总方差与总误差之比（等式2）：
   $$\mathrm{ERROR\!-\!INCOHERENCE}(Q,f_\varepsilon) \;:=\; \frac{\sum_i \mathrm{VARIANCE}(q_i,f_\varepsilon)}{\sum_i \mathrm{ERROR}(q_i,f_\varepsilon)}$$
   指标取值 $[0,1]$：0 代表失败完全由系统性偏差驱动（每次输出相同但错误），1 代表失败完全由随机波动驱动。该聚合提供了单一标量来刻画模型在任务上的“混乱”程度。

4. **基于长度的分组缩放分析**  
   以平均推理长度（输出token数或行动步数）作为任务复杂度的代理，将问题按此维度排序并等距分组。随后绘制各组内的错误不一致性、偏差和方差随推理长度和模型规模的变化曲线（例如Figure 2、Figure 5）。该模块揭示了推理链增长和模型扩大对错误不一致性的相反影响，并为集成和推理预算等缓解策略提供了分析基础。

**输入输出流**：给定问题集 $Q$、模型 $f_\varepsilon$ 及采样配置，模块一生成多样化的回答序列；模块二输出每个问题的偏差与方差；模块三汇聚得到任务整体的错误不一致性；模块四基于推理长度进行分段，输出缩放趋势和方差占优的判断。与仅依赖少量采样的传统评估相比，本框架不仅给出总体误差，更重要的是区分了“对齐失败”（偏差）与“不可靠波动”（方差），从而可以诊断模型失败的深层原因。



该研究提出 **错误不一致性（Error‑Incoherence）分析框架**，通过偏差‑方差分解将 AI 模型的失败模式量化为系统偏差与测试时随机方差的相对贡献。框架由四个核心模块构成。

### 核心模块

1. **多样本响应收集（Multi‑sample Response Collection）**  
   对每个问题生成至少 30 个回答，通过变动随机种子、少样本上下文等方式覆盖测试时随机性，保证偏差与方差估计的稳定性（见 §3，Appx. C.5）。该模块是所有后续分解与聚合的数据基础。

2. **KL 偏差‑方差分解（KL Bias‑Variance Decomposition）**  
   对单个问题，计算期望交叉熵误差，并利用 KL 散度将总误差严格分解为**系统偏差**（目标分布与平均预测分布的差异）和**方差**（平均预测与单次预测分布的期望差异）。该模块是量化不一致性的核心数学工具。

3. **错误不一致性聚合（Error‑Incoherence Aggregation）**  
   对问题集内所有问题的方差与总误差求和，计算总方差与总误差的比值，得到错误不一致性。取值 0 表示失败完全由系统偏差引起，取值 1 表示失败完全由随机方差引起。

4. **基于推理长度的分组与缩放分析（Length‑based Grouping & Scaling Analysis）**  
   按问题的平均推理长度（或行动步数）对样本分组，分析不同复杂度组别下错误不一致性随推理长度与模型规模的变化规律，揭示任务复杂度与模型规模对不一致性的因果影响。

### 关键公式与变量含义

**KL 偏差‑方差分解（式 1）**
$$
\underbrace{\mathbb{E}_{\varepsilon}[\mathbf{CE}(y,f_\varepsilon)]}_{\mathrm{ERROR}}
= \mathbb{E}_{\varepsilon}\!\left[\sum_{c=1}^C y[c]\log(f_\varepsilon[c])\right]
= \underbrace{D_{\mathrm{KL}}(y\|\bar{f})}_{\mathrm{BIAS}^2}
+ \underbrace{\mathbb{E}_{\varepsilon}[D_{\mathrm{KL}}(\bar{f}\|f_\varepsilon)]}_{\mathrm{VARIANCE}}
$$
其中：
- $y$ 为目标类别分布（one‑hot 编码）；
- $f_\varepsilon$ 为受随机性 $\varepsilon$ 影响的模型输出概率向量；
- $\bar{f}$ 为对 $\varepsilon$ 取平均的预测分布；
- $D_{\mathrm{KL}}$ 为 KL 散度；
- $C$ 为类别总数。

该式将期望交叉熵误差严格拆分为**偏差平方项**（模型平均预测与真值的偏离）与**方差项**（单次预测围绕平均预测的波动），为后续不一致性定义提供基础。

**错误不一致性定义（式 2）**
$$
\mathrm{ERROR-INCOHERENCE}(Q,f_\varepsilon)
:= \frac{\sum_i \mathrm{VARIANCE}(q_i,f_\varepsilon)}{\sum_i \mathrm{ERROR}(q_i,f_\varepsilon)}
$$
其中 $Q = \{q_i\}$ 为问题集。该比值直接衡量模型失败中由随机不一致性贡献的比例，是论文的核心评价指标。

**Brier 评分偏差‑方差分解（用于稳健性验证，附录 A）**
$$
\mathbb{E}_\varepsilon[\mathrm{BRIER}(y, f_\varepsilon)]
= \underbrace{\|y - \hat{f}\|_2^2}_{\mathrm{BRIER\ Bias}^2}
+ \underbrace{\mathbb{E}_\varepsilon[\|\hat{f} - f_\varepsilon\|_2^2]}_{\mathrm{BRIER\ Variance}}
$$
其中 $\hat{f}$ 为平均预测向量。该分解在多选题场景下提供与 KL 分解定性一致的趋势，支撑结论的稳健性。

**合成优化器中的二次损失（第 3.2.2 节）**
$$
f(x) = \frac{1}{2} (x - b)^T A (x - b)
$$
其中 $A$ 为条件数 50 的正定矩阵。该二次函数作为合成优化目标，用于研究语言模型作为优化器时规模增长对偏差与方差的不同抑制效果。

**概念性偏差‑方差方程（§1）**
$$
\mathrm{ERROR} = \mathrm{BIAS}^2 + \mathrm{VARIANCE}
$$
直观表达 AI 错误的可分解性：系统性失误对应偏差，随机不一致对应方差。框架即在此方程的基础上，通过具体的损失函数实现可操作的度量。



## 实验与关键发现

实验围绕错误不一致性分析框架展开：对每问题采集≥30个样本以捕捉测试时随机性，使用KL偏差-方差分解（式1）计算期望交叉熵误差，并将总方差占总误差的比例定义为错误不一致性（式2）。该框架应用于多项选择（GPQA, MMLU）、Agentic编码（SWE-BENCH）、开放式生成（MWE）和合成优化器任务，涵盖QWEN3系列（0.6B–32B）、O3-MINI、O4-MINI及Claude Sonnet 4等模型。

### 主发现：更长推理链导致更高不一致性

错误不一致性随模型推理长度成行动步数增加而单调上升，这是贯穿所有任务和模型的核心现象。推理链长度的自然波动（固定任务和预算，按中位数分组）显著预测不一致性：长推理/长行动组的错误不一致性远高于短组（如O4-MINI在SWE-BENCH上由0.47→0.60，O3-MINI由0.12→0.25），但准确率差异极小（图3）。这意味着推理步骤的增加直接引入方差放大，而非仅反映任务绝对难度。不同模型家族在错误不一致性-推理长度斜率上存在差异（图2），暗示架构或后训练策略可能调节方差的增长速率，但目前证据尚不足以归因。

![[assets/figures/papers/iclr26_0016_sIBwirjYlY_The_Hot_Mess_of_AI_How_Does_Misalignment_Scale_W/figures/002_Figure_2.jpg]]

![[assets/figures/papers/iclr26_0016_sIBwirjYlY_The_Hot_Mess_of_AI_How_Does_Misalignment_Scale_W/figures/025_Figure_7.jpg]]
*Figure 7: Ensembling and larger reasoning budgets reduce error-incoherence. Other forms of error correction may also reduce error-incoherence. (a) Instructing models to reason longer improves performance (inference scaling laws, Fig. 17) and sometimes error-incoherence. This effect is smaller than natural variation, where error-incoherence rises sharply (Fig. 3; direct comparison in Fig. 17). (b) With O4-MINI on GPQA, we analyze the effect of the ensembling, i.e., using multiple samples to average output probabilities over targets for the same question. The bias and variance are now computed by comparing different ensembles of the same size. We find that, as expected from theory, it reduces variance...*

### 模型规模的异质性效应：难度反转

模型规模对不一致性的影响取决于任务复杂度。在MMLU上按参照模型推理长度分组后，容易问题的错误不一致性随QWEN3规模增大而下降，但最难问题的错误不一致性却随规模显著上升（图5e）。合成优化器实验揭示了一种可能机制：训练Transformer执行二次函数优化时，更大模型降低偏差的速度远快于降低方差（偏差下降斜率更大），导致总误差中方差占比趋近1.0——即模型失败由随机波动主导（图6）。这表明增大模型更擅长消除系统性偏差，但对测试时随机性的控制相对滞后，在搜索空间大的困难任务中尤其明显。一项小型人类调查（15人）独立显示，被评判为更智能的实体也被认为更不一致（图4b），为上述趋势提供了跨领域互证。

![[assets/figures/papers/iclr26_0016_sIBwirjYlY_The_Hot_Mess_of_AI_How_Does_Misalignment_Scale_W/figures/020_Figure_5.jpg]]
*Figure 5: Details for QWEN3 scaling laws: easy tasks become less incoherent, harder tasks more incoherent. We group MMLU questions by reasoning length using a reference model (Qwen3 32B, (a)), which correlates across model sizes (b) and serves as a task complexity proxy, as accuracy drops with longer reasoning (c). These groups reveal distinct bias–variance scaling (d): bias slopes are similar across groups, but variance slopes decrease sharply for harder ones. In the hardest group, variance slopes fall below bias slopes, leaving variance as the limiting factor. Thus, larger models remain constrained by variance and more incoherent with scale (e). We provide more analyses including other models and t...*

![[assets/figures/papers/iclr26_0016_sIBwirjYlY_The_Hot_Mess_of_AI_How_Does_Misalignment_Scale_W/figures/022_Figure_6.jpg]]
*Figure 6: Details for synthetic optimization: In controlled settings with teacher forcing and a single objective, language models become variance dominated with increasing size. (left) We train autoregressive transformers to predict update steps to minimize a quadratic function using decoding based regression, i.e., next-token prediction. This setting involves sequentially performing steps towards a goal via next token prediction, emulating a key feature of goal seeking AI. (middle) The loss (next-token prediction objective) follows a clear power law improvement with model size. (right) When evaluating the trained models using their own rollouts, we find that increasing model size reduces bias much f...*

### 缓解与消融：集成降低方差符合幂律

集成多个预测样本可有效抑制方差：在O4-MINI上，Brier/KL错误不一致性随集成规模E按$1/E$速率下降（幂指数α≈−0.90），而偏差几乎不变（图7b）。这确认了方差可单独控制的统计特性。人为增大推理预算（如要求模型“思考更久”）虽能略微降低O3-MINI和O4-MINI的不一致性，但效果远弱于自然推理长度变化，且Sonnet 4无响应（图7a, 图17）。消融显示：（1）KL、Brier和0/1三种分解给出的错误不一致性趋势定性一致；（2）偏差-方差估计在约30个样本后稳定收敛；（3）集成降低方差遵循$1/E$幂律，不受Laplace平滑干扰。因此，推理长度和任务复杂度是错误不一致性的主要因果杠杆，简单的规模扩展或推理预算增加难以根本解决不一致性问题。

![[assets/figures/papers/iclr26_0016_sIBwirjYlY_The_Hot_Mess_of_AI_How_Does_Misalignment_Scale_W/figures/083_Figure_17.jpg]]
*Figure 17: Grouped comparison of reasoning budgets and natural variation in reasoning: natural variation dominates. We analyze GPQA (left, (a)) and SWE-BENCH (b) by splitting samples into above- or below-median reasoning length (GPQA) or actions (SWE-BENCH) per question. We then compute performance and error-incoherence for both groups. (a) Increasing the reasoning budget improves performance (inference scaling laws, top left), and slightly reduces error-incoherence (bottom left). On the other hand, naturally longer reasoning only has a small effect on accuracy (top right), but shows much higher error-incoherence (right). (b) Similar observations apply to SWE-BENCH, where more actions show minor devia...*

### 失败模式与适用边界

该框架依赖明确的目标函数（如选择题答案、单元测试通过向量），难以直接推广至无精确定义目标的开放式任务。推理长度与任务难度高度共线，即便采用固定预算和分组，仍无法完全解耦二者的独立贡献。合成优化器实验仅使用特定二次函数，其结论向真实多峰优化目标的泛化性需额外验证。人类调查样本量小且排序主观，无法支撑强结论。此外，当前分析未涉及推理链内部结构（如回溯、自我修正）如何影响方差，这可能是理解核心机制的关键缺口。



## 定位与知识库关联

本文提出的错误不一致性（error‑incoherence）分析框架并非凭空出现，而是将统计学习理论中经典的偏差‑方差分解（bias‑variance decomposition）重新锚定在大语言模型评测的语境中。传统上，模型能力被压缩为整体错误率、准确率或 pass@1 等标量指标，这些指标模糊了“一致性的系统错误”与“随机性的不可靠失败”之间的界限。该工作通过**将期望交叉熵（或其他损失）显式分解为系统偏差平方与试验‑时间方差之和**（Equation 1，Equation 2；Figure 1），直接改变了评测方法的核心度量槽（changed slot 1），从而将讨论从“模型有多容易出错”推向“错误中有多大比例源自不可预测的随机行为”。这一度量切换构成了与既有评测范式最根本的差异：传统评测使用 1～3 次采样下的总体错误率，而该框架要求每问题至少 30 次采样以稳定估计偏差与方差分量（Section 3，Appx. C.5，Figure 21），由此实现了对“失败性质”的解剖。

与该框架直接比较的 baseline 并非某一特定模型，而是**以整体错误率作为主要判据的评测文化**，例如各种榜单上仅给出单次或少数几次运行的准确率。被评测的模型（Claude Sonnet 4、O3‑MINI、O4‑MINI 以及 QWEN3 全族）在此处扮演的是“受试系统”而非 baseline 方法；真正被替代的是“只关心均值”的错误分析范式。这一范式变更带来两个关键后果：其一，能够区分偏差主导的失败（可视为一致性偏误，类似对齐失效）与方差主导的失败（类似工业事故式的不可靠性）；其二，揭示了仅扩大模型规模难以系统降低后一类失败，甚至在某些困难任务上方差占比会随规模上升（Figure 5(e)，Figure 6）。

**适用边界**首先由误差分解的数学形式决定：错误不一致性定义要求存在明确的目标概率分布（如多选题的标准答案向量、单元测试的 0/1 通过向量），因此该方法自然适用于 GPQA、MMLU、SWE‑BENCH 这类封闭或半封闭任务，对于完全开放的生成式任务（如非标准化长篇问答），目标分布的定义本身就构成挑战（已记录为 limitations 之一）。同样，偏差‑方差分量的稳定估计依赖多次输出采样，模型推理策略与采样的交互（温度、随机种子、少样本上下文）均会影响方差分量，因此在极端计算受限的场景下难以执行。此外，实验中将推理长度（或行动步数）作为任务复杂度的便于测量的代理，但长度与难度之间存在混淆（Figure 2，Figure 3）；虽然对固定任务按长度分组能缓解这一混淆，但因果关系上到底是更长推理本身增加了不一致性，还是更复杂的任务自然需要更长推理并同时贡献了额外方差，尚无法完全解耦。

**局限性与尚待验证的环节**。若干证据强度需要审慎看待。人类调查的样本量仅 15 人（Figure 4(b)，confidence = 0.9），其对“更智能则更不一致”的主观排序可能受样本偏差影响，短期内难以作为强证据推广。合成优化实验使用定常的二次函数（条件数 50），而实际优化问题可能具有非凸、高维、多模态特性，结论的外推需要更多架构与目标函数上的验证。关于推理链的内部结构（如回溯、自我纠错）如何调节方差分量，论文并未深入分析，这为未来工作留下了明确的切入点。另外，评测流程依赖 API 返回的 token 计数来衡量推理长度，不同模型家族的内部 token 化差异可能引入测量噪声，尤其对于推理预算受 API 控制的模型，其“自然推理长度”的定义存在口径不一致的风险。

**开放问题与其在知识库中的位置**。围绕错误不一致性这一新指标，涌现出几条贯穿当前对齐研究的深层疑问。第一，更大模型在困难任务上变得更不一致的内在机制是什么——是由于模型在困难区域遭遇了多维决策冲突，还是因为其先验足够强以至于最终答案收敛到不同局部模式？这直接关系到 scaling law 的重新解释：传统的损失幂律仅描述均值行为，而未能区分偏差与方差的各自缩放斜率（Figure 6 显示偏差下降斜率大于方差，造成方差主导）。第二，**能否在训练或推理阶段显式干预方差？** 现有证据表明，集成（ensembling）可将方差按 $1/E$ 速率压降，同时不影响偏差（Figure 7(b)），而仅增加推理预算仅能轻微降低不一致性（Figure 7(a)），这暗示着训练阶段的方差正则化或特定的推理解码策略（如温度退火）可能比事后平均更根本。第三，当目标本身模糊或多元时（开放式任务、偏好对齐），偏差‑方差分解的度量基础会动摇——如何定义广义的“正确”，并区分“多方一致”与“真正可接受”之间的偏差分量，是一个悬而未决的理论问题。第四，在极度超人类的尺度下，模型的不一致性是会趋于饱和还是持续发散？这既关系到安全性的外推，也挑战了“更大即更可靠”的直觉假设。最后，将错误不一致性直接作为奖励信号或正则项嵌入训练过程是否可行——这是否会生成“过于保守”的模型，抑或能提升实际鲁棒性——目前仍是空白地带。这些方向将错误不一致性框架与现有对齐方法论（RLHF、推理时缩放、评估驱动开发）连接起来，使其具备了催生后续工作的潜在纵深。



## 原文 PDF

![[paperPDFs/ICLR_2026/The_Hot_Mess_of_AI_How_Does_Misalignment_Scale_With_Model_Intelligence_and_Task_Complexity.pdf]]
