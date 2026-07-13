---
title: "Dual-Space Smoothness for Robust and Balanced LLM Unlearning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Dual_Space_Smoothness_for_Robust_and_Balanced_LLM_Unlearning.pdf
project_link: null
code_link: https://github.com/Tsuzukii/PRISM
openreview_forum_id: VIMW3eys6x
aliases:
- PPGISM
- DSSRBLU
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/fairness_equity_justice_and_safety
core_operator: "通过对表示空间和参数空间同时施加平滑性约束（即扩大对抗攻击所需的“裕度”）来增强鲁棒性并平衡遗忘指标。"
primary_logic: "利用最小-最大优化框架，在表示空间通过对抗训练探针扩大越狱裕度，在参数空间通过惩罚梯度范数平坦化遗忘损失曲面并解耦保留梯度冲突，从而同时提升遗忘效果、保持模型通用能力并抵抗多种攻击。"
claims:
- "PRISM通过双空间平滑性统一框架提升鲁棒性并平衡遗忘指标"
- "表示空间平滑性通过对抗训练探针扩大越狱攻击裕度"
- "参数空间平滑性通过惩罚梯度范数增大重新学习裕度"
- "MUSE-Books 上 Unlearn Score (↑) = 0.860"
---

# Dual-Space Smoothness for Robust and Balanced LLM Unlearning

> [!tip] 核心洞察
> 利用最小-最大优化框架，在表示空间通过对抗训练探针扩大越狱裕度，在参数空间通过惩罚梯度范数平坦化遗忘损失曲面并解耦保留梯度冲突，从而同时提升遗忘效果、保持模型通用能力并抵抗多种攻击。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 双空间平滑性实现鲁棒且平衡的LLM遗忘 |
| 英文题名 | Dual-Space Smoothness for Robust and Balanced LLM Unlearning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VIMW3eys6x) · [GitHub](https://github.com/Tsuzukii/PRISM) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/fairness_equity_justice_and_safety |
| Method | PRISM (Probe-guided Iterative Smoothness Minimization) |
| Dataset | MUSE-Books, MUSE-News, WMDP_bio (Llama2-7B), WMDP_bio (Ministral-8B-Instruct) |

> [!tip] 效果简介
> - MUSE-Books 上，Unlearn Score (↑) 为 0.860，对比 0.000 (SAM+NPO)，变化 +0.860。
> - MUSE-News 上，Unlearn Score (↑) 为 0.522，对比 0.000 (SAM+NPO)，变化 +0.522。
> - WMDP_bio (Llama2-7B) 上，Unlearn Score (↑) 为 0.521，对比 0.322 (SAM+NPO)，变化 +0.199。

## 概要

现有大语言模型（LLM）遗忘方法面临三大瓶颈：**灾难性遗忘**导致模型效用崩溃，**遗忘效果与下游效用严重失衡**，以及在表示空间和参数空间**缺乏鲁棒性**，容易遭受越狱攻击和重新学习攻击。例如，梯度上升（GA）和 SAM+NPO 在遗忘训练过程中效用会断崖式下跌至接近零（Figure 1a）；而 NPO 遗忘后的模型仍能被重新学习攻击恢复已删除的知识，且在多种越狱攻击下保持较高的攻击成功率（Figure 2）。

针对上述问题，本文提出 **PRISM（Probe-guided Iterative Smoothness Minimization）**，一个基于最小-最大优化的统一遗忘框架。其核心思想是：在**表示空间**和**参数空间**同时施加平滑性约束，扩大对抗攻击所需的“裕度”，从而提升鲁棒性并平衡遗忘指标。具体而言，PRISM 包含两个阶段：

- **表示空间平滑性**：在冻结基模型的隐藏层状态上训练一个对抗鲁棒的探针，通过扩大有害表示与无害表示之间的决策边界来抵御越狱攻击。
- **参数空间平滑性**：在遗忘损失中惩罚梯度范数以平坦化损失曲面，同时将遗忘梯度投影到保留梯度的正交补上以解耦梯度冲突，从而抵抗重新学习攻击并防止效用崩塌。

实验表明，PRISM 在 MUSE-Books、MUSE-News 和 WMDP 等多个基准上均优于现有方法。例如，在 MUSE-Books 上，PRISM 的遗忘得分达到 0.860，而最强基线 SAM+NPO 仅为 0.000（Table 1）。在重新学习攻击和多种越狱攻击下，PRISM 也展现出显著更强的鲁棒性（Table 2, Table 3）。消融实验进一步证实，移除表示空间平滑性、参数空间平滑性或梯度冲突解耦中的任一组件，均会导致遗忘效果或模型效用的严重退化（Table 5）。

PRISM 的局限性包括：有时出现过高的过度拒绝率，可能与底层 NPO 组件的保守倾向有关；缺乏形式化理论保证来证明双空间平滑性的协同效果；以及参数平滑性带来的额外计算开销（单步时间增加约 35%）。



### 问题背景

大型语言模型（LLM）在训练过程中不可避免地会学习到有害、敏感或受版权保护的内容。LLM遗忘（unlearning）旨在从已训练模型中擦除特定知识，同时尽可能保持模型的通用能力。形式化地，遗忘问题可表述为在遗忘集 $D_f$ 和保留集 $D_r$ 上的加权优化目标：

$$\theta_u = \arg\min_\theta \Big[ \mathcal{L}_f(\theta; D_f) + \gamma \mathcal{L}_r(\theta; D_r) \Big]$$

其中 $\mathcal{L}_f$ 为遗忘损失，$\mathcal{L}_r$ 为保留损失，$\gamma \geq 0$ 为平衡系数。

### 现有方法的三大瓶颈

通过对现有遗忘方法的系统分析，本文识别出三个核心瓶颈：

**瓶颈一：灾难性效用崩塌。** 经典方法如梯度上升（Gradient Ascent, GA）和结合锐度感知最小化的 NPO（SAM+NPO）在遗忘训练过程中会出现模型效用的灾难性崩溃。如 Figure 1a 所示，随着训练步数增加，这两种方法在 MUSE-Books 保留集上的知识记忆指标（Knowledge Memorization）急剧下降至接近零，表明模型完全丧失了下游任务能力。这一现象的根本原因在于遗忘梯度与保留梯度之间存在严重冲突，遗忘更新未经约束地破坏了保留知识。

**瓶颈二：遗忘效果与下游效用的严重失衡。** 不同方法在遗忘有效性（Unlearning Effectiveness, UE）和后遗忘性能（Post-unlearning Performance, PP）之间存在显著的权衡困境（Figure 1b）。DOOR 和 Task Vector 等方法虽然较好地保持了模型效用，但遗忘效果不足；而 GA 和 NPO 则过度优化遗忘目标，以牺牲模型通用能力为代价。这种失衡使得现有方法难以在实际部署中同时满足安全性和可用性需求。

**瓶颈三：表示空间与参数空间的双重鲁棒性缺失。** 遗忘后的模型面临两类典型攻击。在表示空间层面，越狱攻击（jailbreak attack）通过构造对抗性提示，最大化有害表示向“接受方向”的投影来突破安全防线：

$$\max_{\mathbf{x}} \mathcal{L}(\mathbf{x}) := \langle g(f(\mathbf{x})) - g(f(\mathbf{x}_0)), \mathbf{e}_a \rangle$$

如 Figure 2b 所示，NPO 遗忘后的 Llama2-7B 模型在多种越狱攻击下仍存在显著的成功率（Multi-turn ASR 约 0.32，Prefilling ASR 约 0.40）。在参数空间层面，重新学习攻击（relearning attack）通过少量遗忘样本对遗忘后模型进行微调即可恢复已删除的知识。Figure 2a 表明，NPO 遗忘模型在经历约 100 步重新学习后，遗忘效果几乎被完全逆转。这两类攻击暴露了现有方法在表示空间和参数空间均缺乏足够的防御裕度（margin）。

### 核心动机与洞察

上述瓶颈的共性根源在于：现有遗忘方法仅在单一空间（表示空间或参数空间）进行优化，忽略了两个空间之间的协同关系。本文的核心洞察是：**通过对表示空间和参数空间同时施加平滑性约束，可以扩大对抗攻击所需的“裕度”，从而在提升鲁棒性的同时平衡遗忘与保留指标。**

具体而言，在表示空间通过对抗训练探针扩大越狱裕度，使有害表示与安全表示之间的决策边界更加稳健；在参数空间通过惩罚梯度范数平坦化遗忘损失曲面并解耦保留梯度冲突，增大重新学习攻击的难度。基于这一洞察，本文提出 PRISM（Probe-guided Iterative Smoothness Minimization）框架，通过最小-最大优化统一实现双空间平滑性，系统性地解决上述三大瓶颈。



## 核心方法与创新机理

PRISM 的核心创新在于通过**双空间平滑性（Dual-Space Smoothness）**统一框架，系统性地解决了现有 LLM 遗忘方法面临的三大瓶颈：灾难性遗忘导致的效用崩溃、遗忘效果与下游效用的严重失衡，以及表示空间和参数空间缺乏鲁棒性带来的越狱攻击和重新学习攻击脆弱性。

### 表示空间平滑性：扩大越狱裕度

现有遗忘方法（如 NPO）在隐藏层表示空间中缺乏对有害内容的鲁棒区分能力，导致模型容易被越狱攻击突破。PRISM 通过在冻结基模型的隐藏层状态上训练一个**对抗鲁棒的探针（Adversarially Robust Probe）**来解决这一问题。

具体而言，给定输入 $x$ 在第 $L$ 层的表示 $z(x) := h_{\theta_0, L}(x) \in \mathbb{R}^d$，PRISM 首先训练一个探针 $g(\cdot;\phi)$ 区分有害与无害表示。为扩大决策边界，在表示空间上施加 $\ell_\infty$ 球内的最坏情况对抗扰动：

$$z_i^{\mathrm{adv}} = z(x_i) + \varepsilon \, \mathrm{sign}(g(x_i; \phi))$$

该对抗训练过程可视为**表示空间中的对抗训练**，其目标是扩大任意有害表示与其安全对应物之间的裕度（margin）。随后，遗忘过程通过最小化探针引导的损失函数 $\mathcal{L}_{\mathrm{probe}}(\theta; x) = -\log p_{\phi^\star}(y = 0 \mid h_{\theta, L}(x))$，将遗忘集样本的表示推向无害区域。这一机制从表示层面切断了有害内容与安全响应之间的关联通路，从根本上提升了对抗越狱攻击的能力。

### 参数空间平滑性：增大重新学习裕度

重新学习攻击的核心在于攻击者通过少量微调步骤即可恢复已删除的知识，这源于遗忘后的损失曲面存在陡峭的下降方向。PRISM 通过对参数空间施加平滑性约束来平坦化损失曲面，使得攻击者需要更大的更新步长才能恢复知识——即**增大重新学习裕度（relearn margin）**。

PRISM 将遗忘目标的优化形式化为一个最小-最大问题：

$$\min_{\theta} \left[ \max_{\|\delta\|_2 \le \rho} \ell_{\mathrm{f}}(\theta + \delta) \right]$$

通过一阶近似，该目标等价于在遗忘损失上增加梯度范数惩罚项：

$$\mathcal{L}_{\mathrm{f}}^{\mathrm{SM}}(\theta) \approx \ell_{\mathrm{f}}(\theta) + \rho \|g(\theta)\|_2$$

这一惩罚项直接抑制参数空间中的大梯度，使损失曲面在遗忘解附近趋于平坦。消融实验证实，移除参数空间平滑性（PS）后，重新学习 100 步的 Verbatim Memorization 从 6.804 显著上升至 16.664，验证了该组件对抵抗重新学习攻击的关键作用。

### 梯度冲突解耦：防止灾难性遗忘

遗忘更新与保留更新之间的梯度冲突是导致模型效用崩溃的直接原因。PRISM 引入**梯度冲突解耦（Gradient Conflict Decoupling, GCD）**机制，将遗忘梯度 $g_{\mathrm{f}}$ 投影到保留梯度 $g_{\mathrm{r}}$ 的正交补上：

$$g_{\mathrm{f}}^{\perp} = g_{\mathrm{f}} - \frac{\langle g_{\mathrm{f}}, g_{\mathrm{r}} \rangle}{\|g_{\mathrm{r}}\|_2^2} g_{\mathrm{r}}$$

这一投影操作确保遗忘更新不会破坏保留集上的已有知识。消融实验显示，移除 GCD 后，重新学习 50 步时的模型效用从 46.588 暴跌至 1.333，出现灾难性崩塌，充分说明了梯度解耦在维持遗忘-保留平衡中的必要性。

### 与基线方法的关键差异

与最接近的基线 SAM+NPO 相比，PRISM 的三项改进构成了实质性差异：

| 改进维度 | SAM+NPO | PRISM |
|---------|---------|-------|
| 表示空间 | 无针对性防御 | 对抗训练探针扩大越狱裕度 |
| 参数空间 | SAM 仅作用于 NPO 损失 | 遗忘损失 + $\rho\|g(\theta)\|_2$ 惩罚，直接平坦化遗忘曲面 |
| 梯度处理 | 遗忘与保留梯度直接混合 | 遗忘梯度正交投影至保留梯度补空间 |

SAM+NPO 虽然在参数空间引入了 Sharpness-Aware Minimization，但其平滑性约束缺乏对遗忘目标的针对性设计，且未解决表示空间的鲁棒性问题。PRISM 通过双空间协同平滑与梯度解耦，在 MUSE-Books 上将遗忘得分从 0.000 提升至 0.860，在 WMDP_bio 上从 0.322 提升至 0.521，同时保持了模型效用的稳定。



![[assets/figures/papers/iclr26_0012_VIMW3eys6x_Dual-Space_Smoothness_for_Robust_and_Balanced_LL/figures/005_Figure_3.jpg]]
*Figure 3: Workflow of PRISM. After constructing the Forget and Retain datasets, Step 1 adversarially trains a probe on the hidden states of a given base model. In Step 2, guided by the robust probe and loss gradient, we perturb gradients toward flatter regions while decoupling conflicts between retain and forget gradients. Step 3 updates the model parameters accordingly*

PRISM（Probe-guided Iterative Smoothness Minimization）是一个基于最小-最大优化的统一遗忘框架，其核心设计思路是通过在表示空间和参数空间同时施加平滑性约束，扩大模型对越狱攻击和重新学习攻击的防御裕度，从而在遗忘效果与模型效用之间取得更优的平衡。

### 三阶段流水线

PRISM 的工作流程由三个顺序执行的模块组成，如图3所示：

**阶段一：对抗探针训练（Adversarial Probe Training）**

在冻结的基模型上，提取指定层 $L$ 的隐藏状态作为输入表示：
$$z(x) := h_{\theta_0, L}(x) \in \mathbb{R}^d$$

在此表示空间上训练一个分类探针 $g(\cdot;\phi)$，用于区分有害与无害表示。为增强探针的局部鲁棒性，采用对抗训练策略——对每个输入表示施加 $\ell_\infty$ 球内的最坏扰动，构造对抗样本：
$$z_i^{\mathrm{adv}} = z(x_i) + \varepsilon \,\mathrm{sign}(g(x_i; \phi))$$

该探针随后作为"引导器"，为遗忘过程提供表示空间的方向信号。

**阶段二：平滑性最小化（Smoothness Minimization）**

此阶段同时作用于两个空间：

- **表示空间平滑性**：通过最小化探针引导的遗忘损失 $\mathcal{L}_{\mathrm{probe}}(\theta; x)$，将遗忘集样本的隐藏表示推向无害区域，从而扩大越狱攻击所需的表示空间裕度。

- **参数空间平滑性**：在遗忘损失中引入梯度范数惩罚项，通过一阶近似实现损失曲面的平坦化：
$$\mathcal{L}_{\mathrm{f}}^{\mathrm{SM}}(\theta) \approx \ell_{\mathrm{f}}(\theta) + \rho \|g(\theta)\|_2$$
平坦的损失曲面意味着模型参数对微调扰动不敏感，从而增大重新学习攻击的裕度。

**阶段三：参数更新与梯度冲突解耦（Parameter Update with Decoupling）**

在计算遗忘梯度 $g_{\mathrm{f}}$ 和保留梯度 $g_{\mathrm{r}}$ 后，将遗忘梯度投影到保留梯度的正交补上：
$$g_{\mathrm{f}}^{\perp} = g_{\mathrm{f}} - \frac{\langle g_{\mathrm{f}}, g_{\mathrm{r}} \rangle}{\|g_{\mathrm{r}}\|_2^2} g_{\mathrm{r}}$$

这一解耦操作确保遗忘更新不会破坏保留知识，防止灾难性遗忘。最终使用正交化后的梯度更新模型参数。

### 输入输出与模块关系

- **输入**：基模型 $\theta_0$，遗忘集 $D_f$，保留集 $D_r$
- **中间产物**：经对抗训练的鲁棒探针 $\phi^*$，以及探针引导的遗忘损失信号
- **输出**：遗忘后模型 $\theta_u$，该模型在遗忘目标知识的同时保持通用能力，并对越狱和重新学习攻击具有鲁棒性

三个模块之间存在明确的依赖关系：阶段一的探针为阶段二提供表示空间的优化目标，阶段二的平滑性损失为阶段三提供梯度信号，阶段三的解耦机制确保整个流程中保留知识不被破坏。这种串联设计使得表示空间和参数空间的平滑性约束能够协同作用，共同提升遗忘的鲁棒性与平衡性。



PRISM (Probe-guided Iterative Smoothness Minimization) 是一个基于最小-最大优化的遗忘框架，其核心由三个模块级联构成：对抗探针训练、平滑性最小化、以及带冲突解耦的参数更新。

### 对抗探针训练（表示空间平滑性）

该模块在冻结的基模型隐藏层状态上训练一个具有局部鲁棒性的线性探针，用于区分有害与无害表示。其目标是扩大越狱攻击所需的表示空间“裕度”。

给定输入 $x$，从基模型第 $L$ 层的隐藏状态提取表示：

$$z(x) := h_{\theta_0, L}(x) \in \mathbb{R}^d$$

为增强探针的局部鲁棒性，在表示空间上构造对抗扰动。具体而言，对每个样本 $x_i$，通过 $\ell_\infty$ 球内的线性化最坏扰动构造对抗表示：

$$\delta_i^{\star} = \varepsilon \,\mathrm{sign}\big(g(x_i; \phi)\big), \quad z_i^{\mathrm{adv}} = z(x_i) + \delta_i^{\star}$$

其中 $g(x_i; \phi)$ 为探针在 $z(x_i)$ 处的梯度，$\varepsilon > 0$ 为扰动半径。探针随后在对抗表示上训练，扩大决策边界。

### 探针引导的遗忘损失

训练完成的稳健探针 $\phi^{\star}$ 用于引导遗忘过程。遗忘损失定义为使遗忘集表示被探针分类为无害类别 $y = 0$：

$$\mathcal{L}_{\mathrm{probe}}(\theta; x) = -\log p_{\phi^{\star}}\big(y = 0 \,\big|\, h_{\theta, L}(x)\big)$$

最小化该损失将遗忘集表示推离有害区域，实现表示空间的平滑性约束。

### 参数空间平滑性

参数空间平滑性通过平坦化遗忘损失曲面来增大重新学习攻击的裕度。核心是最小化遗忘损失在最坏参数扰动下的值：

$$\min_{\theta}\;\Big[\max_{\|\delta\|_2 \le \rho} \ell_{\mathrm{f}}(\theta + \delta)\Big]$$

对内部最大化进行一阶线性近似，得到平滑性遗忘损失：

$$\mathcal{L}_{\mathrm{f}}^{\mathrm{SM}}(\theta) \approx \ell_{\mathrm{f}}(\theta) + \rho \|g(\theta)\|_2$$

其中 $g(\theta) = \nabla_\theta \ell_{\mathrm{f}}(\theta)$ 为遗忘损失梯度，$\rho > 0$ 控制平滑性强度。额外项 $\rho\|g(\theta)\|_2$ 惩罚大梯度范数，迫使损失曲面在参数空间中趋于平坦，从而增大重新学习所需的最小扰动幅度。

### 梯度冲突解耦

为防止遗忘更新破坏保留知识，PRISM 将遗忘梯度投影到保留梯度的正交补上：

$$g_{\mathrm{f}}^{\perp} = g_{\mathrm{f}} - \frac{\langle g_{\mathrm{f}}, g_{\mathrm{r}} \rangle}{\|g_{\mathrm{r}}\|_2^2}\, g_{\mathrm{r}}$$

其中 $g_{\mathrm{f}}$ 和 $g_{\mathrm{r}}$ 分别为遗忘集和保留集上的损失梯度。该投影操作去除了遗忘方向中与保留方向冲突的分量，从而在参数更新时避免灾难性遗忘。

### 整体遗忘目标

将上述组件整合，PRISM 的优化目标可概括为遗忘损失与保留损失的加权组合：

$$\theta_u = \arg\min_\theta \Big[\mathcal{L}_{\mathrm{f}}(\theta; D_f) + \gamma \mathcal{L}_{\mathrm{r}}(\theta; D_r)\Big]$$

其中 $\mathcal{L}_{\mathrm{f}}$ 融合了探针引导的遗忘损失和参数平滑性惩罚，$\mathcal{L}_{\mathrm{r}}$ 为标准保留损失，$\gamma \ge 0$ 平衡两者。参数更新时使用正交化后的遗忘梯度 $g_{\mathrm{f}}^{\perp}$，完成双空间平滑性约束下的遗忘过程。



## 实验与关键发现

### 主要结果：遗忘效果与效用平衡

PRISM 在三个不同性质的数据集上均取得最优综合遗忘得分（Unlearn Score），并展现出显著优于基线方法的遗忘-效用平衡能力。表 1 汇总了核心数值对比。

![[assets/figures/papers/iclr26_0012_VIMW3eys6x_Dual-Space_Smoothness_for_Robust_and_Balanced_LL/figures/006_Table_1.jpg]]
*Table 1: Unlearn Scores on MUSE-Books, MUSE-News, WMDP and Wall-clock time required for each step, measured in seconds per step on MUSE-Books dataset. ↓ indicates lower is better, ↑ indicates higher is better. Note that the Unlearn Score on the WMDP benchmark includes results from two base models: Llama-2 7B and Mistral-8B-Instruct-2410, respectively. Red text indicates the best and blue text indicates the runner-up, respectively*

在 MUSE-Books 对话数据集上，PRISM 的 Unlearn Score 达到 **0.860**，而最强基线 SAM+NPO 仅为 0.000，提升幅度达 +0.860。在 MUSE-News 连续文本数据集上，PRISM 取得 **0.522**，同样远超 SAM+NPO 的 0.000（+0.522）。在 WMDP_bio 生物安全知识遗忘任务中，PRISM 在 Llama2-7B 上达到 **0.521**（SAM+NPO 为 0.322，+0.199），在 Ministral-8B-Instruct 上达到 **0.761**（SAM+NPO 为 0.721，+0.040）。

值得注意的是，Unlearn Score 是一个复合指标，综合了遗忘有效性（KnowMem 和 VerbMem 越低越好）和模型效用保留（Utility 越高越好）。PRISM 在所有基准上均排名第一，表明其双空间平滑性策略能够有效解耦遗忘与保留两个目标，避免了 GA 和 NPO 类方法常见的“遗忘越强、效用越差”的失衡问题。

PRISM 的计算代价主要体现在参数平滑性部分：单步耗时约 **11.223 秒**，相比 SAM+NPO 的 8.325 秒增加了约 35%，但仍处于可接受范围。最快的 DOOR 方法仅需 3.780 秒，但其遗忘效果远逊于 PRISM。

### 鲁棒性评估：抵抗重新学习攻击

重新学习攻击（Relearning Attack）是评估遗忘方法鲁棒性的关键维度——攻击者试图通过少量遗忘样本微调来恢复已删除的知识。表 2 展示了在 MUSE-Books 上不同攻击步数下的表现。

![[assets/figures/papers/iclr26_0012_VIMW3eys6x_Dual-Space_Smoothness_for_Robust_and_Balanced_LL/figures/007_Table_2.jpg]]
*Table 2: Unlearning robustness of different methods on MUSE-Books under relearning attacks with varying attack steps. Red text indicates the best and blue text indicates the runner-up, respectively. ↓ indicates lower is better, ↑ indicates higher is better*

PRISM 在 50、75、100 步重新学习攻击下始终保持最高的 Unlearn Score（0.860），且 VerbMem 指标控制优异：50 步时为 **0.746**，75 步时为 **5.405**，100 步时为 **6.804**。相比之下，SAM+NPO 在 100 步攻击后 VerbMem 飙升至 16.664，表明其遗忘效果严重退化。

更关键的是模型效用的保持。PRISM 在 50 步攻击后 Utility 为 **46.588**，100 步后仍维持在 **63.181**，未出现灾难性崩塌。而 SAM+NPO 在攻击下出现明显的效用崩溃（见图 5），验证了仅依赖 SAM 的单一参数平滑性不足以抵抗重新学习攻击。

在更极端的 Relearn 25% 设置下（攻击者掌握 25% 的遗忘数据），PRISM 在 50 步攻击后仍将 VerbMem 和 KnowMem 分别压制在 **0.082** 和 **0.000**（表 4），几乎完全阻止了知识恢复。RMU-LAT 和 RMU 在此设置下表现明显劣化，KnowMem 分别升至 24.164 和 29.203。

### 鲁棒性评估：抵抗越狱攻击

越狱攻击（Jailbreak Attack）评估遗忘模型是否仍能被诱导生成有害内容。表 3 报告了在 WMDP_bio 上三种攻击方式的成功率（ASR）。

![[assets/figures/papers/iclr26_0012_VIMW3eys6x_Dual-Space_Smoothness_for_Robust_and_Balanced_LL/figures/008_Table_3.jpg]]
*Table 3: Overall Jailbreak Attack Success Rate (ASR) on different jailbreak attack methods and the Unlearn Score indicating unlearning performance on $\mathrm { W M D P _ { b i o } }$ datasets. Red text indicates the best and blue text indicates the runner-up, respectively. ↓ indicates lower is better, ↑ indicates higher is better. Prefill Attacks include prefilling that is 15/20 tokens long*

PRISM 在所有攻击类型下均取得最低 ASR：Multi-turn ASR 为 **0.196**（SAM+NPO 为 0.244），Prefilling ASR 为 **0.293/0.279**（SAM+NPO 为 0.393/0.390），AutoDAN ASR 为 **0.000**（SAM+NPO 为 0.039）。这表明表示空间的对抗训练探针成功扩大了有害表示与安全表示之间的决策裕度，使越狱攻击难以找到突破方向。

然而，PRISM 的过度拒绝率（XStest Refusal Rate）为 **0.843**，高于 SAM+NPO 的 0.763 和原始模型的 0.780。这一副作用可能与底层 NPO 组件的保守倾向有关——NPO 本身倾向于扩大拒绝范围，PRISM 的表示空间平滑性进一步强化了这种倾向。这是方法的一个已知局限，需要在安全性与可用性之间进一步权衡。

### 消融实验：各组件的独立贡献

表 5 的消融实验揭示了 PRISM 三个核心组件的因果作用：

![[assets/figures/papers/iclr26_0012_VIMW3eys6x_Dual-Space_Smoothness_for_Robust_and_Balanced_LL/figures/010_Table_5.jpg]]
*Table 5: Ablation Study on PRISM’s components on MUSE-Books: removal of representation space (RS) smoothing, parameter space (PS) smoothing, and gradient-conflict decoupling (GCD)*

**移除表示空间平滑性（RS）**：当去掉对抗训练探针引导的表示空间平滑性后，模型在重新学习攻击下的 VerbMem 从 6.804 显著上升至 **16.664**，说明 RS 组件对抵抗逐字记忆恢复至关重要。这是因为 RS 将遗忘集的隐藏表示推离有害区域，增大了攻击者通过微调恢复原始表示的难度。

**移除参数空间平滑性（PS）**：去掉梯度范数惩罚后，模型在重新学习攻击下的整体遗忘效果明显退化。PS 组件通过平坦化遗忘损失曲面增大重新学习裕度，其缺失使得攻击者能以更少的步数恢复被遗忘的知识。

**移除梯度冲突解耦（GCD）**：这是影响最剧烈的消融项。去掉 GCD 后，模型在 50 步重新学习攻击下的 Utility 从 46.588 暴跌至 **1.333**，出现灾难性效用崩塌。这一现象揭示了核心机制：当遗忘梯度与保留梯度方向冲突时，直接相加会导致遗忘更新破坏保留知识。GCD 通过将遗忘梯度投影到保留梯度的正交补上，确保遗忘过程不干扰模型通用能力。

三个组件协同作用：RS 防御越狱攻击，PS 抵抗重新学习攻击，GCD 防止效用崩塌，共同构成了 PRISM 的鲁棒遗忘框架。

### 损失景观可视化

图 6 展示了 PRISM 在 MUSE-Books 遗忘集上的 3D 损失景观。与基线方法相比，PRISM 的损失曲面更加平坦，梯度范数更小，直观验证了参数空间平滑性约束的效果。平坦的损失曲面意味着局部微调难以快速降低遗忘损失，从而增大了重新学习攻击所需的计算代价——这与表 2 中 PRISM 在多次攻击步数下仍保持低 VerbMem 的结果一致。

![[assets/figures/papers/iclr26_0012_VIMW3eys6x_Dual-Space_Smoothness_for_Robust_and_Balanced_LL/figures/028_Figure_6.jpg]]
*Figure 6: 3D loss landscape of PRISM on MUSE-Books forget set; higher values near $\mathbf { X } = \mathtt { y }$ = 0 indicate more effective unlearning

### 遗忘-效用权衡分析

图 4 综合展示了所有方法在 MUSE-Books 上遗忘有效性与模型效用之间的权衡关系。PRISM 位于 Pareto 前沿的左上角（高遗忘有效性、高效用保留），而 GA 和 NPO 类方法则偏向高遗忘有效性但低效用保留的极端区域。SAM+NPO 虽然通过 SAM 改善了效用保留，但在重新学习攻击下出现效用崩塌（图 5），说明单一的参数平滑性不足以稳定维持权衡。PRISM 的双空间平滑性加上 GCD 冲突解耦，使得模型即使在多次攻击后仍能保持接近原始水平的效用。

### 已知局限与需人工验证的问题

1. **过度拒绝问题**：PRISM 的 XStest Refusal Rate 偏高（0.843），可能影响模型在合法安全查询上的可用性。这一数值在消融实验中未单独分析，需要进一步确认是 RS 组件还是底层 NPO 的主导因素。

2. **计算开销**：单步耗时增加约 35%，主要来自参数平滑性的梯度范数计算。对于大规模部署场景，需要评估总体训练时间的可接受性。

3. **消融实验的 KnowMem 数据**：表 5 中移除 PS 后的 KnowMem 数值在提供的证据中未明确给出，仅描述了“整体效果下降明显”。该结论置信度为 0.9，建议查阅完整表格确认具体数值。

4. **形式化保证缺失**：PRISM 的鲁棒性提升目前仅通过实验验证，缺乏理论证明表示空间和参数空间平滑性的协同机制。这是一个开放问题，不影响实验结论的可靠性，但限制了方法的理论深度。



## 定位与知识库关联

### 与基线方法的关系

PRISM 并非从零构建，而是在现有遗忘方法的基础上进行结构性改进。其核心遗忘损失建立在 **NPO (Negative Preference Optimization)** 之上，同时集成了 **GDR (Gradient Descent on Retain Set)** 正则器以维持保留集性能。与直接使用 NPO 或 GA 的基线相比，PRISM 的关键差异在于引入了三个协同组件：

**表示空间平滑性 (RS)** 是对 RMU 类方法（通过扰动隐藏表示进行遗忘）的深化。RMU 仅将表示推向随机方向，而 PRISM 通过对抗训练探针，在表示空间构建了一个具有明确决策边界的分类器，将遗忘集表示系统地推向“无害”区域，从而扩大越狱攻击所需的裕度。这一设计使得 PRISM 在面对 Multi-turn、Prefilling 和 AutoDAN 等越狱攻击时，攻击成功率显著低于所有基线（Table 3）。

**参数空间平滑性 (PS)** 可视为 SAM+NPO 的泛化与增强。SAM+NPO 仅在 NPO 损失上施加 Sharpness-Aware Minimization，而 PRISM 将平滑性惩罚 $\rho\|g(\theta)\|_2$ 显式地作用于遗忘损失曲面，通过平坦化损失景观来增大重新学习裕度。这一差异在重新学习攻击下尤为关键：SAM+NPO 在攻击步数增加时出现灾难性效用崩塌（Figure 5），而 PRISM 保持了稳定的遗忘效果与效用平衡（Table 2）。

**梯度冲突解耦 (GCD)** 解决了 GA 和 NPO 类方法中遗忘梯度与保留梯度直接相加导致的隐性破坏。通过将遗忘梯度投影到保留梯度的正交补上（$g_{\mathrm{f}}^{\perp} = g_{\mathrm{f}} - \frac{\langle g_{\mathrm{f}}, g_{\mathrm{r}} \rangle}{\|g_{\mathrm{r}}\|_2^2} g_{\mathrm{r}}$），PRISM 确保遗忘更新不会抵消保留知识，从而避免了 Figure 1(a) 所示的效用崩塌现象。

### 适用边界

PRISM 的有效性已在以下条件下得到验证：

- **模型规模**：Llama2-7B 和 Ministral-8B-Instruct，尚未在更大规模模型（如 70B+）上验证。
- **数据类型**：覆盖对话式数据（MUSE-Books、MUSE-News）和连续文本（WMDP_bio），包括知识记忆和逐字记忆两种遗忘模式。
- **攻击类型**：重新学习攻击（100/200/400 样本，25% 子集攻击）和越狱攻击（Multi-turn、Prefilling、AutoDAN）。
- **遗忘目标**：有害知识遗忘（WMDP_bio）和版权内容遗忘（MUSE 基准）。

超出此范围的有效性需要手动验证。特别是，PRISM 在更复杂的多轮对话遗忘场景、多语言遗忘任务以及更大规模模型上的表现尚无实验支撑。

### 局限与开放问题

**已知局限**：

1. **过度拒绝倾向**：PRISM 有时出现较高的过度拒绝率（over-refusal rate），这在一定程度上源于其依赖的 NPO 组件本身可能扩大模型的保守行为。Table 3 中 XStest Refusal Rate 的数据反映了这一问题。

2. **计算开销增加**：参数平滑性部分导致单步训练时间增加约 35%（Table 1 中 PRISM 为 11.223s/step，而最快的 DOOR 仅为 3.776s/step），这在资源受限场景下可能成为瓶颈。

3. **缺乏形式化保证**：论文未提供理论证明来严格论证表示空间平滑性与参数空间平滑性的组合能够产生协同鲁棒性。两个平滑性目标之间的关系及其对鲁棒性裕度的联合影响仍停留在经验层面。

**开放问题**：

- 能否设计更高效的平滑性正则化策略（如随机化近似或低秩投影）以降低额外计算开销，使 PRISM 在保持鲁棒性的同时接近基线方法的训练速度？
- 双空间平滑性策略能否与差分隐私遗忘、知识蒸馏等其他遗忘范式结合，以进一步提升隐私保护或跨模型迁移能力？
- 能否建立一个严格的理论框架，形式化证明遗忘任务中平滑性约束与越狱/重新学习攻击裕度之间的定量关系？
- PRISM 的平滑性组件在其他遗忘方法（如 Task Vector、DOOR）上的兼容性与增益效果如何，是否具有通用性？



## 原文 PDF

![[paperPDFs/ICLR_2026/Dual_Space_Smoothness_for_Robust_and_Balanced_LLM_Unlearning.pdf]]
