---
title: Uncertainty-Aware Exploratory Direct Preference Optimization for Multimodal Large Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Uncertainty_Aware_Exploratory_Direct_Preference_Optimization_for_Multimodal_Large_Language_Models.pdf
project_link: null
code_link: null
aliases:
- UDUAEDPO
- UAEDPOMLLM
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过引入token级别的认知不确定性度量，即比较清晰图像与模糊图像下的预测逻辑值差异，来识别模型的视觉认知缺陷，并据此动态调整偏好学习中的探索强度（λ_w和λ_l）。
primary_logic: 应将幻觉缓解的重点从强化已建立的视觉敏感度转向主动发现并纠正视觉认知缺陷，通过基于认知不确定性的探索强度控制，在偏好样本中增加对视觉认知不足标记的学习压力，同时在非偏好样本中减轻对有益视觉知识的过度惩罚。
claims:
- UE-DPO通过token级别的认知不确定性引导模型识别认知缺陷并进行自我纠错探索。
- 在多模态幻觉基准测试上，UE-DPO在大多数指标和模型规模上均表现出优越的性能。
- 消融实验证明，偏好分支的探索控制是减少幻觉的主要驱动力，且完整的双分支策略进一步提升了性能。
- Object-Hal 上 CHAIRs↓ = 13.72
---

# Uncertainty-Aware Exploratory Direct Preference Optimization for Multimodal Large Language Models

> [!tip] 核心洞察
> 应将幻觉缓解的重点从强化已建立的视觉敏感度转向主动发现并纠正视觉认知缺陷，通过基于认知不确定性的探索强度控制，在偏好样本中增加对视觉认知不足标记的学习压力，同时在非偏好样本中减轻对有益视觉知识的过度惩罚。

| 字段 | 内容 |
|------|------|
| 中文题名 | 不确定感知的探索性直接偏好优化用于多模态大语言模型 |
| 英文题名 | Uncertainty-Aware Exploratory Direct Preference Optimization for Multimodal Large Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.04874) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | UE-DPO (Uncertainty-aware Exploratory Direct Preference Optimization) |
| Dataset | Object-Hal, MMHal-Bench, AMBER-g, AMBER-d |

> [!tip] 效果简介
> - Object-Hal 上，CHAIRs↓ 13.72 vs 55.67 (LLaVA-v1.5-7B) (-41.95)。
> - MMHal-Bench 上，Score↑ 2.82 vs 2.01 (LLaVA-v1.5-7B) (+0.81)；HalRate↓ 0.48 vs 0.61 (LLaVA-v1.5-7B) (-0.13)。
> - AMBER-g 上，CHAIR↓ 2.9 vs 7.7 (LLaVA-v1.5-7B) (-4.8)。

## 概要

多模态大语言模型（MLLM）的幻觉问题——即模型生成与视觉输入不一致的内容——是阻碍其可靠应用的关键瓶颈。现有的偏好学习方法（如POVID、mDPO、V-DPO等）主要依赖模型自我评估的**视觉敏感度**来分配优化压力：对模型“认为”视觉关联强的token施加更大学习强度，而对模型“认为”视觉关联弱的token则几乎不加干预。这种策略存在根本性的**自我参照偏差**——模型过度关注已掌握的视觉线索，却系统性地忽略了那些难以感知但对正确理解至关重要的视觉细节，从而限制了更深层次的对齐效果。

本文提出**不确定感知的探索性直接偏好优化（UE-DPO）**，将幻觉缓解的焦点从强化已有的视觉敏感度，转向**主动发现并纠正模型的视觉认知缺陷**。其核心机制是：通过比较清晰图像与扩散噪声模糊图像下的token预测逻辑值差异，量化token级别的**认知不确定性**，并据此动态调控偏好学习中的探索强度——对偏好样本中高不确定性但低视觉敏感度的token增加学习压力，鼓励模型主动探索视觉认知不足的区域；同时对非偏好样本中高不确定性且高视觉敏感度的token减轻惩罚，避免对已习得的有益视觉知识造成过度压制。

在多模态幻觉基准测试上，UE-DPO在大多数评估指标和模型规模上均展现出显著优势。以LLaVA-v1.5-7B为基础模型，UE-DPO在Object-Hal上使CHAIRs指标从55.67降至13.72（降幅达41.95），在MMHal-Bench上使Score从2.01提升至2.82，同时HalRate从0.61降至0.48。消融实验进一步揭示，偏好分支的探索控制是幻觉减少的**主要驱动力**，而完整的双分支策略通过协调偏好增强与非偏好保护，进一步提升了整体性能。

从方法谱系看，UE-DPO属于基于偏好学习的幻觉缓解方法，但其创新在于将优化信号分配策略从“模型自评的视觉敏感度”切换为“认知不确定性引导的探索强度控制”，为多模态对齐提供了一个从被动强化到主动纠错的范式转换。



### 多模态大语言模型的幻觉困境

多模态大语言模型（MLLMs）在视觉理解与语言生成任务中展现出强大的能力，但普遍存在**幻觉（hallucination）**问题——模型生成的内容与给定图像的事实信息不一致，例如描述不存在的物体或错误的视觉属性。这种幻觉严重损害了模型在医疗、自动驾驶等高风险场景中的可靠性，因此幻觉缓解成为MLLM对齐研究的核心挑战之一。

### 现有偏好学习方法的自我参照偏差

近年来，基于偏好学习的幻觉缓解方法取得了显著进展。这些方法通常构建偏好数据对（包含人类或AI偏好的正确回答与包含幻觉的错误回答），并通过直接偏好优化（DPO）或其变体进行微调。代表性工作包括**POVID**（Zhou et al., arXiv 2024）利用GPT-4V构建偏好数据，**mDPO**通过辅助目标缓解语言过优先，**V-DPO**使用视觉引导因子进行细粒度幻觉缓解，以及**TPO**基于视觉锚定奖励的优化。

然而，这些方法存在一个共性的结构性缺陷：它们依赖**模型自我评估的视觉敏感度**来分配优化压力。具体而言，模型倾向于对自身已经能够感知的视觉线索（如显著物体）施加更强的学习信号，而对那些难以感知但同样关键的视觉细节（如背景中的小物体、模糊区域）施加较弱的学习压力。这种策略形成了一个**自我参照偏差（self-reference bias）**的闭环：模型不断强化已掌握的视觉知识，却系统性忽略了自身的视觉认知盲区。

如Figure 1所示，现有方法在偏好样本中对“men”这类视觉敏感token施加强优化压力，而对“ships”这类视觉不敏感但信息有价值的token给予弱压力。这种偏向性的训练信号分配使得模型难以突破自身的感知上限，限制了更深层次的对齐和幻觉缓解效果。

### 核心动机：从视觉敏感度到认知缺陷的焦点转移

本文的核心洞察是：**幻觉缓解的重点应从强化已建立的视觉敏感度，转向主动发现并纠正模型的视觉认知缺陷**。模型产生幻觉的根本原因并非缺乏对显著视觉线索的关注，而是对某些视觉信息存在“认知不足”（under-cognition）——即模型在生成特定token时，未能充分将预测锚定在图像证据之上。

基于这一洞察，本文提出将**认知不确定性（epistemic uncertainty）**作为识别视觉认知缺陷的关键信号。认知不确定性衡量的是模型对自身预测的不确定性来源于知识不足的程度，而非数据噪声。在多模态场景中，当一个token的预测高度依赖语言先验而非视觉输入时，模型对该token的认知不确定性就会升高——这正是幻觉产生的温床。

通过将优化焦点从“模型认为自己擅长什么”转向“模型实际欠缺什么”，UE-DPO旨在打破自我参照偏差的闭环，引导模型主动探索并纠正其视觉认知盲区，从而实现更深层次的幻觉缓解。



## 核心方法与创新机理

UE-DPO 的核心创新在于将多模态大模型幻觉缓解的优化焦点，从**依赖模型自我评估的视觉敏感度**转向**主动发现并纠正视觉认知缺陷**。这一转变通过三个紧密耦合的 changed slots 实现。

### 从视觉敏感度到认知缺陷的焦点转移

现有偏好学习方法（如 V-DPO、TPO 等）通过视觉锚定奖励或视觉引导因子来识别模型“已经看到”的视觉线索，并据此分配优化压力。这种策略存在一个根本性缺陷：**模型过度关注已掌握的视觉信息，而忽略那些难以感知但对正确理解至关重要的视觉细节**，形成自我参照偏差（Figure 1）。

UE-DPO 的核心洞察是：幻觉缓解的关键不在于强化已有的视觉敏感度，而在于**识别模型的“视觉认知盲区”——即模型未能将 token 预测有效锚定于图像信息的区域**，并针对性地施加探索压力。

### Token 级别的认知不确定性度量

为实现上述焦点转移，UE-DPO 引入了一个全新的信号来源：**认知不确定性（epistemic uncertainty）**。与依赖模型损失或敏感度代理的基线不同，该方法通过比较清晰图像 $v$ 与扩散噪声模糊图像 $v'$ 下的预测逻辑值差异，量化每个 token 的视觉认知不确定性：

$$\mathrm{u}(s_t,a_t)=\mathrm{logit}_\theta(\hat{a}_t(v')|v,x,y_{<t}) - \mathrm{logit}_\theta(a_t|v,x,y_{<t}) \quad \text{(Eq. 6)}$$

其中模糊图像通过前向扩散过程生成：$v'(k) = \sqrt{\bar{\xi}_k} \cdot v + \sqrt{1 - \bar{\xi}_k} \cdot \epsilon$。这一度量的直觉在于：如果模型对某个 token 的预测高度依赖视觉信息，当图像被模糊后，其预测逻辑值会发生显著变化，从而暴露出模型的视觉认知缺陷。

### 基于不确定性的探索强度控制

在获得 token 级别的认知不确定性后，UE-DPO 将其与视觉敏感度 $\Delta$ 结合，对偏好样本和非偏好样本中的 token 进行分类，并实施**差异化的探索强度控制**：

- **偏好样本中的探索增强**：对于高不确定性但低视觉敏感度的 token（Type-I），增大学习强度，迫使模型主动探索被忽略的视觉线索：
  $$\lambda_w(s_t,a_t)=1+\alpha \mathbf{1}\{\mathrm{I}_w=1\} \sigma(\frac{\mathrm{u}(s_t,a_t)-\mu_I}{\varsigma_I}) \quad \text{(Eq. 9)}$$

- **非偏好样本中的惩罚缓解**：对于高不确定性且高视觉敏感度的 token（Type-I），减轻偏好惩罚，避免对模型已建立的视觉知识造成破坏：
  $$\lambda_l(s_t,a_t)=1-\alpha \mathbf{1}\{\mathrm{I}_l=1\} \sigma(\frac{\mathrm{u}(s_t,a_t)-\mu_I}{\varsigma_I}) \quad \text{(Eq. 11)}$$

这两个权重通过停止梯度操作集成到 DPO 损失函数中（Eq. 12），实现了对隐式优势的自适应调节。从理论视角看，该机制等价于在 RL 目标中引入由认知不确定性调制的动态 KL 正则化，扩展的优势函数为：

$$\beta\log\frac{\pi^*(a|s)^\lambda}{\pi_{\mathrm{ref}}(a|s)} = Q^*(s,a) - V^*(s) - \beta(\lambda - \mathbb{E}_{a'\sim\pi^*}[\lambda']) \triangleq A_e^*(s,a) \quad \text{(Eq. 15)}$$

当 $\lambda$ 降低时，探索成本减小，优势增加，从而引导策略向视觉认知不足的区域进行探索。

### 与基线方法的关键差异总结

| 维度 | 现有方法（V-DPO、TPO 等） | UE-DPO |
|------|--------------------------|--------|
| 信号来源 | 模型自我评估的视觉敏感度 | 认知不确定性（清晰 vs 模糊图像逻辑值差异） |
| 优化焦点 | 强化已掌握的视觉线索 | 发现并纠正视觉认知缺陷 |
| Token 权重策略 | 均匀加权或基于敏感度加权 | 基于不确定性与敏感度的联合分类，差异化控制 |
| 非偏好样本处理 | 统一施加惩罚 | 对高不确定性且高敏感度 token 减轻惩罚，保护已有知识 |

消融实验证实，偏好分支的探索控制是幻觉减少的**主要驱动力**：单独使用偏好分支控制（w/o dispref.）即可在标准 DPO 基础上带来显著性能跃升，而完整的双分支策略进一步提升了性能（Table 2）。



UE-DPO的整体pipeline由三个核心模块串联构成，形成“量化认知缺陷→控制探索强度→偏好优化”的闭环，如图2所示。

**输入与数据流**：pipeline接收一个三元组 $(x, y_w, y_l)$，其中 $x$ 为图像-文本查询，$y_w$ 为偏好响应，$y_l$ 为非偏好响应。对于每个待优化的token，系统同时持有原始清晰图像 $v$ 和经扩散噪声模糊处理的图像 $v'$。

**模块一：不确定性感知模块**。该模块负责计算token级别的两个关键信号——视觉敏感度 $\Delta$ 和认知不确定性 $u$。视觉敏感度通过比较清晰图像与模糊图像下模型对同一token的预测逻辑值差异来量化，反映模型对该token的视觉依赖程度。认知不确定性则定义为清晰图像下的预测逻辑值与模糊图像下最高概率替代token的逻辑值之差（Eq. 6），捕捉模型因视觉信息不足而产生的认知缺陷。两个信号共同构成后续探索控制的决策依据。

**模块二：探索强度控制模块**。基于视觉敏感度阈值 $\tau$ 和认知不确定性 $u$，该模块将token划分为不同类型，并分别计算偏好分支的探索强度 $\lambda_w$ 和非偏好分支的惩罚缓解因子 $\lambda_l$。具体而言：在偏好样本中，对高不确定性且低视觉敏感度的token（Type-I）施加增强的探索权重；在非偏好样本中，对高不确定性且高视觉敏感度的token减轻惩罚权重，避免对已掌握的视觉知识过度压制。

**模块三：UE-DPO训练目标**。将 $\lambda_w$ 和 $\lambda_l$ 通过停止梯度操作集成到标准DPO损失函数的对数概率项中（Eq. 12），实现token级别的隐式优势动态调整。训练时，模型在保持偏好排序能力的同时，梯度被重新分配——偏好分支中视觉认知不足的token获得更强的优化信号，非偏好分支中有价值的视觉知识得到保护。

**推理时无额外开销**：认知不确定性的计算仅发生在训练阶段，推理阶段不引入模糊图像或额外前向传播，模型直接以标准自回归方式生成响应。

### 补充图表

![[assets/figures/papers/paper_list_l2285_https_arxiv_org_abs_2605_04874/figures/002_Figure_2.jpg]]
*Figure 2: Schematic illustration of our method. (a) For preferred responses, the method intensifies exploration on Type-I tokens characterized by high uncertainty and low sensitivity. Type-II tokens correspond to legitimate language dependencies. Type-III tokens already exhibit high visual sensitivity. (b) For dispreferred responses, the method mitigates preference penalties on Type-I tokens exhibiting both high epistemic uncertainty and visual sensitivity. The visual grounding of Type-II tokens is sufficiently stable, and Type-III tokens are visually insensitive in our view*

![[assets/figures/papers/paper_list_l2285_https_arxiv_org_abs_2605_04874/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the focus shift from established visual sensitivity to cognitive deficits. (a) Existing methods rely on selfassessed visual sensitivity in learning. Stronger optimization pressure is placed on the visually sensitive men, while giving weak pressure to the “ships” in response sample, even though such nonsensitive information remains valuable for improving visual understanding. (b) Our UE-DPO method is to rebalance the training by redirecting the focus toward visual cognitive deficiencies. More optimization pressure is applied to insensitive yet crucial “ships”, to facilitate a deeper alignment*



UE-DPO 的核心由三个紧密耦合的模块构成：不确定性感知模块、探索强度控制模块和 UE-DPO 训练目标。三个模块协同工作，将 token 级别的认知不确定性转化为差异化的优化压力。

### 认知不确定性的量化

模型在生成 token $a_t$ 时，其对视觉信息的依赖程度可通过比较清晰图像 $v$ 与模糊图像 $v'$ 下的预测逻辑值差异来度量。模糊图像通过扩散噪声过程生成：

$$
v'(k) = \sqrt{\bar{\xi}_k} \cdot v + \sqrt{1 - \bar{\xi}_k} \cdot \epsilon
$$

其中 $\bar{\xi}_k$ 为扩散噪声水平，$\epsilon$ 为标准高斯噪声。基于此，token 级别的认知不确定性定义为：

$$
\mathrm{u}(s_t, a_t) = \mathrm{logit}_\theta(\hat{a}_t(v') \mid v, x, y_{<t}) - \mathrm{logit}_\theta(a_t \mid v, x, y_{<t})
$$

该公式的核心直觉是：当模型对某个 token 的预测高度依赖视觉信息时，模糊图像会导致预测逻辑值显著下降，从而产生较大的不确定性值；反之，若模型主要依赖语言先验而非视觉内容，则模糊化对逻辑值影响较小，不确定性较低。这一度量直接识别了模型的视觉认知缺陷——即那些模型未能充分将 token 预测锚定在图像信息上的位置。

### 视觉敏感度与 token 分类

与认知不确定性互补，视觉敏感度 $\Delta(s_t, a_t)$ 衡量模型在清晰图像下对视觉信息的依赖程度。通过结合认知不确定性 $u$ 和视觉敏感度 $\Delta$，UE-DPO 将 token 分为三类，并据此设计差异化的探索策略：

- **Type-I token（偏好样本）**：高认知不确定性且低视觉敏感度。这类 token 代表模型的视觉认知盲区——模型未能有效利用视觉信息，但自身并未意识到这一缺陷。在偏好样本中，对此类 token 施加增强的探索强度。
- **Type-I token（非偏好样本）**：高认知不确定性且高视觉敏感度。这类 token 虽存在认知缺陷，但模型已表现出一定的视觉锚定能力。在非偏好样本中，对此类 token 减轻惩罚，以保护已获得的视觉知识。
- **Type-II/III token**：分别对应合法的语言依赖和已充分视觉敏感的 token，维持标准 DPO 处理。

### 探索强度的动态控制

基于上述 token 分类，UE-DPO 为偏好样本和非偏好样本分别设计探索强度权重 $\lambda_w$ 和 $\lambda_l$。

对于偏好样本，探索强度定义为：

$$
\lambda_w(s_t, a_t) = 1 + \alpha \mathbf{1}\{\mathrm{I}_w = 1\} \sigma\left(\frac{\mathrm{u}(s_t, a_t) - \mu_I}{\varsigma_I}\right)
$$

其中 $\mathbf{1}\{\mathrm{I}_w = 1\}$ 指示该 token 属于 Type-I（高不确定性、低敏感度），$\sigma(\cdot)$ 为 sigmoid 函数，$\mu_I$ 和 $\varsigma_I$ 为不确定性值的均值和标准差，$\alpha$ 为探索强度因子。该公式的效果是：对视觉认知盲区中的 token，$\lambda_w > 1$，从而放大其在损失函数中的梯度贡献。

对于非偏好样本，惩罚缓解权重定义为：

$$
\lambda_l(s_t, a_t) = 1 - \alpha \mathbf{1}\{\mathrm{I}_l = 1\} \sigma\left(\frac{\mathrm{u}(s_t, a_t) - \mu_I}{\varsigma_I}\right)
$$

其中 $\mathbf{1}\{\mathrm{I}_l = 1\}$ 指示 Type-I token（高不确定性、高敏感度）。此时 $\lambda_l < 1$，降低对非偏好样本中已具备视觉锚定能力的 token 的惩罚力度，避免对有益视觉知识的过度压制。

### UE-DPO 训练目标

将上述 token 级别权重集成到 DPO 损失函数中，通过停止梯度操作（$\mathrm{sg}[\cdot]$）实现隐式优势的动态调整：

$$
L_{\mathrm{UE-DPO}}(\pi_\theta, \pi_{\mathrm{ref}}) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \log \sigma \left( \beta \sum_{t=0}^{T_w} \log \frac{\pi_\theta(a_t^w \mid s_t)^{\mathrm{sg}[\lambda_w]}}{\pi_{\mathrm{ref}}(a_t^w \mid s_t)} - \beta \sum_{t=0}^{T_l} \log \frac{\pi_\theta(a_t^l \mid s_t)^{\mathrm{sg}[\lambda_l]}}{\pi_{\mathrm{ref}}(a_t^l \mid s_t)} \right)
$$

停止梯度操作确保 $\lambda_w$ 和 $\lambda_l$ 仅作为缩放因子影响梯度传播，而不参与自身的梯度计算。该目标在保持偏好排序拟合能力的同时，通过 $\lambda$ 加权梯度引导模型：在偏好样本中加强对视觉认知不足 token 的学习，在非偏好样本中保护已获得的视觉知识。

### 理论支撑：探索性优势函数

从理论角度，UE-DPO 的目标可被解释为在 token 级别引入动态 KL 正则化的逆 RL 问题。扩展后的隐式优势函数为：

$$
\beta \log \frac{\pi^*(a \mid s)^\lambda}{\pi_{\mathrm{ref}}(a \mid s)} = Q^*(s, a) - V^*(s) - \beta(\lambda - \mathbb{E}_{a' \sim \pi^*}[\lambda']) \triangleq A_e^*(s, a)
$$

其中 $A_e^*(s, a)$ 为探索性优势函数，由标准价值优势与探索成本项组成。当 $\lambda$ 降低时（如非偏好样本中 $\lambda_l < 1$），探索成本减小，优势函数值增大，从而隐式地提升该 token 在优化中的相对重要性。这一理论框架为 UE-DPO 的差异化探索策略提供了形式化基础。



## 实验与关键发现

### 核心发现与基准性能

UE-DPO 在多模态幻觉基准上展现出显著且一致的性能优势。在 Object-Hal 基准上，基于 LLaVA-v1.5-7B 的 UE-DPO 将 CHAIRs 指标从基线的 55.67 降至 **13.72**，降幅达 41.95 点；在 MMHal-Bench 上，Score 从 2.01 提升至 **2.82**，HalRate 从 0.61 降至 **0.48**。在 AMBER 基准的生成式任务（AMBER-g）中，CHAIR 指标从 7.7 降至 **2.9**；在判别式任务（AMBER-d）中，F1 从 74.3 提升至 **85.7**。这一性能优势在不同模型规模上保持稳定——在 LLaVA-v1.5-13B 和 Qwen2.5-VL-3B 上，UE-DPO 同样取得了最优或接近最优的 CHAIRs 和 Score 指标（Table 1）。

![[assets/figures/papers/paper_list_l2285_https_arxiv_org_abs_2605_04874/figures/003_Table_1.jpg]]
*Table 1: Performance comparison with preference learning based hallucination mitigation methods for MLLMs across various hallucination benchmarks. For baselines without official checkpoints, the results are taken from the respective papers. For baselines with available official checkpoints, we primarily refer to the re-evaluation results reported in [37]. The † indicates that the method was trained on the same dataset as ours. The best for each metric is in bold*

与现有偏好学习类幻觉缓解方法的对比中，UE-DPO 在大多数指标上超越了 **POVID**（Zhou et al., arXiv 2024）、**mDPO**、**V-DPO**、**TPO** 和 **RLAIF-V** 等方法。值得注意的是，UE-DPO 仅使用与 RLHF-V 相同规模的偏好数据（5.7k 样本），未借助 GPT-4V 等外部模型构建复杂偏好数据，却取得了显著的性能跃升。

### 消融实验：探索控制双分支的必要性

消融实验揭示了探索控制双分支的差异化贡献（Table 2）。**偏好分支的探索控制是幻觉减少的主要驱动力**：单独使用偏好分支（w/o dispref.）即可带来相比标准 DPO 的显著性能跃升。而非偏好分支的惩罚缓解机制（w/o pref.）则进一步提升了整体性能。完整的 UE-DPO 方法同时控制两个分支，在 CHAIRs、Score 和 HalRate 等指标上均优于单一分支变体，验证了双分支协同设计的必要性。

![[assets/figures/papers/paper_list_l2285_https_arxiv_org_abs_2605_04874/figures/005_Table_2.jpg]]
*Table 2: Ablation study of exploration control on the preferred and dispreferred branches with LLaVA-v1.5-7B. The w/o pref. indicates that exploration control is retained only on the dispref. branch, while the pref. branch reverts to the standard DPO logprobability summation. Conversely, the w/o dispref. applies control only to the pref. branch. The complete UE-DPO method applies exploration control to both branches*

### 关键超参数敏感性分析

探索强度因子 α 控制着认知不确定性对优化压力的调节幅度。实验表明，α 在 **0.3** 时性能达到峰值（Table 3）。过小的 α 削弱了探索驱动的纠正效果，而过大的 α 可能导致优化压力过度集中于不确定性区域，干扰已建立的正确视觉理解。

![[assets/figures/papers/paper_list_l2285_https_arxiv_org_abs_2605_04874/figures/004_Table_3.jpg]]
*Table 3: Ablation study on the exploration intensity factor α*

视觉敏感度阈值 τ 决定了 token 被归类为“视觉敏感”或“视觉不敏感”的界限。实验表明，τ 在 **0.4** 时性能最强（Table 4）。该阈值直接影响 Type-I token（高不确定性、低敏感度）和 Type-III token（高不确定性、高敏感度）的识别精度，进而决定探索强度的分配质量。

![[assets/figures/papers/paper_list_l2285_https_arxiv_org_abs_2605_04874/figures/006_Table_4.jpg]]
*Table 4: Ablation study on the visual sensitivity threshold τ*

### 失败模式与局限性

尽管 UE-DPO 在生成式幻觉缓解上表现优异，但在 AMBER-d 的 **准确率（Acc.）指标**上表现略低于某些基线。这表明模型在判别式幻觉检测任务中仍有提升空间——即判断给定描述是否存在幻觉，而非自主生成无幻觉描述。这一差距可能源于训练数据的覆盖范围：当前偏好数据主要针对生成式场景构建，对细粒度判别能力的训练信号相对不足。

此外，方法在训练阶段需要额外的前向推理步骤来计算认知不确定性（通过扩散噪声模糊图像获取对比逻辑值），增加了训练计算成本。但推理阶段无需此额外开销，因为 λ 权重仅用于梯度计算，不参与推理时的自回归生成。



## 定位与知识库关联

### 与现有偏好学习方法的谱系关系

UE-DPO 处于多模态大语言模型（MLLM）幻觉缓解的偏好学习技术谱系中，但其核心贡献在于**从“强化已知视觉敏感度”转向“发现并纠正视觉认知缺陷”**的范式转换。

**标准 DPO 的局限与继承。** 标准 DPO（Direct Preference Optimization）通过最大化偏好样本与非偏好样本之间的隐式奖励差距来对齐模型，其损失函数中所有 token 的 log 概率被均匀求和。这一设计隐含假设每个 token 对偏好学习的贡献均等，但在多模态场景下，它无法区分模型是“真正理解了视觉内容”还是“仅凭语言先验做出了正确预测”。UE-DPO 继承了 DPO 的成对偏好优化框架，但通过引入 token 级别的探索强度权重 $\lambda_w$ 和 $\lambda_l$（见 Eq. 12），打破了均匀加权的限制。

**与视觉敏感度驱动方法的差异。** 现有工作普遍依赖模型自我评估的视觉敏感度来分配优化压力：
- **V-DPO** 使用视觉引导因子来强调某些 token；
- **TPO** 基于视觉锚定奖励进行优化；
- **POVID**（Zhou et al., arXiv 2024）利用 GPT-4V 构建偏好数据。

这些方法的共同瓶颈在于：它们强化的是模型已经能够感知的视觉线索，而对模型尚未掌握的视觉细节（即认知缺陷）分配了较弱的优化信号，形成**自我参照偏差**（self-referential bias）。UE-DPO 的关键不同在于，它通过显式量化认知不确定性来识别这些缺陷区域，并**反向分配优化压力**——对偏好样本中高不确定性但低视觉敏感度的 token 增加学习强度（$\lambda_w > 1$），对非偏好样本中高不确定性且高视觉敏感度的 token 减轻惩罚（$\lambda_l < 1$）。

**与 mDPO 和 RLAIF-V 的关系。** mDPO 通过辅助目标缓解语言过优先问题，RLAIF-V 基于 AI 反馈进行偏好学习。这些方法侧重于偏好数据质量或辅助训练目标，而 UE-DPO 侧重于**训练信号在 token 层面的重新分配**，两者在技术路径上互补。UE-DPO 可以与这些方法的数据构建策略结合使用。

### 适用边界与条件

**模型适用性。** UE-DPO 在 LLaVA-v1.5-7B、LLaVA-v1.5-13B 和 Qwen2.5-VL-3B 上均展现出一致的性能提升（Table 1），表明该方法对不同规模的 MLLM 架构具有较好的泛化性。其核心组件——认知不确定性估计——仅依赖模型自身的预测逻辑值差异，无需外部标注器或额外模型，降低了部署门槛。

**数据依赖性。** 实验主要基于 RLHF-V 5.7k 和 RLAIF-V 数据集进行训练。对于使用相同数据集的基线方法（Table 1 中标记为 † 的方法），UE-DPO 表现出显著优势，说明性能提升确实源于方法本身而非数据质量差异。但需注意，论文排除了依赖复杂偏好数据构建过程的方法（如 SENTINEL 和 OPA-DPO），以保持比较的公平性。

**计算开销。** 认知不确定性计算需要在训练时对每张清晰图像生成对应的扩散噪声模糊图像 $v'$（$v'(k) = \sqrt{\bar{\xi}_k} \cdot v + \sqrt{1 - \bar{\xi}_k} \cdot \epsilon$），并进行一次额外的前向传播来获取模糊图像下的 token 预测逻辑值。这增加了训练阶段的计算成本。但推理时无需任何额外开销——$\lambda$ 权重通过停止梯度操作（sg[·]）仅在训练中生效，推理时模型结构与标准 MLLM 完全一致。

### 局限性与待解决问题

**判别式幻觉检测的不足。** 在 AMBER-d 的 Acc. 指标上，UE-DPO 表现略低于某些基线方法（Table 1）。AMBER-d 是一个判别式任务，要求模型判断给定描述是否存在幻觉，而非生成自由文本。这表明 UE-DPO 在需要精细细节判别的场景中仍有提升空间，可能的原因是该任务对视觉细节的依赖程度更高，而当前的认知不确定性估计可能未能充分捕捉这些细粒度需求。

**数据集覆盖的局限。** 论文明确指出，进一步增强数据集覆盖可能有助于提升模型在细节敏感的幻觉检测任务上的表现。当前的 RLHF-V 和 RLAIF-V 数据集主要覆盖通用视觉问答场景，对于特定领域的视觉细节（如医学图像中的微小病变、遥感图像中的小目标）可能覆盖不足。

**不确定性估计方法的推广性。** 认知不确定性估计依赖于“清晰图像 vs. 模糊图像”的对比范式。这一设计在多模态幻觉缓解中有效，但其是否适用于其他多模态任务（如视觉推理、视觉问答中的可信度评估）尚未得到验证。此外，扩散噪声水平 $\xi$ 的设置在训练中是固定的（$\xi = \sigma(l_t) \cdot (0.5 \times 10^{-2} - 10^{-5}) + 10^{-5}$），是否需要根据图像内容自适应调整仍是一个开放问题。

**与其他技术的融合潜力。** UE-DPO 目前作为独立的偏好微调方法被验证，其与解码策略（如 contrastive decoding、beam search 约束）或其他幻觉缓解技术（如检索增强生成）的结合效果尚未探索。理论上，基于认知不确定性的 token 级权重可以与解码时的置信度校准机制协同工作，这为后续研究留下了空间。

### 知识库定位

UE-DPO 在 MLLM 幻觉缓解的知识谱系中占据**“不确定性驱动的探索性对齐”**这一独特位置。它连接了三个研究脉络：

1. **偏好优化**：继承 DPO 的成对优化框架，但通过 token 级权重实现了细粒度控制；
2. **认知不确定性**：将贝叶斯深度学习中的认知不确定性概念引入多模态对齐，通过逻辑值差异而非模型集成来估计；
3. **探索性学习**：通过 $\lambda_w$ 和 $\lambda_l$ 的非对称设计，在偏好学习中实现了“对已知知识保守、对未知区域探索”的策略，其理论支撑来自扩展的优势函数 $A_e^*(s,a) = Q^*(s,a) - V^*(s) - \beta(\lambda - \mathbb{E}_{a'\sim\pi^*}[\lambda'])$（Eq. 15）。

这一框架的核心洞察——**应将对齐的重点从“强化已知”转向“发现未知”**——对后续研究具有方法论层面的启示意义，可能推动更多基于模型自我诊断的偏好学习方法的发展。



## 原文 PDF

![[paperPDFs/CVPR_2026/Uncertainty_Aware_Exploratory_Direct_Preference_Optimization_for_Multimodal_Large_Language_Models.pdf]]
