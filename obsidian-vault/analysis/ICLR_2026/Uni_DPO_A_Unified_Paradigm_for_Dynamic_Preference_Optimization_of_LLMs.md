---
title: "Uni-DPO: A Unified Paradigm for Dynamic Preference Optimization of LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Uni_DPO_A_Unified_Paradigm_for_Dynamic_Preference_Optimization_of_LLMs.pdf
project_link: null
code_link: https://github.com/pspdada/Uni-DPO
openreview_forum_id: G7DBGlgjjp
aliases:
- UD
- Uni-DPO
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "基于数据质量（评分 margin）和模型学习动态（奖励 margin）的联合自适应权重机制，并结合针对困难高质量正样本的校准负对数似然损失。"
primary_logic: "通过动态重加权偏好对，同时考虑内在数据质量和模型当前性能，并选择性增强困难高质量正样本的概率，训练更加高效且鲁棒。"
claims:
- "消融实验表明，移除质量权重 w_qual、性能权重 w_perf、长度归一化或校准 NLL 损失中的任一组件，性能均会下降。"
- "高质量偏好对可能已被模型过度学习，过分强调它们会导致过拟合。"
- "Uni-DPO 在多个文本理解、数学推理和多模态基准上一致超越 DPO 和 SimPO。"
- "AlpacaEval 2.0 上 Length-Controlled Win Rate (LC%) = 23.8"
---

# Uni-DPO: A Unified Paradigm for Dynamic Preference Optimization of LLMs

> [!tip] 核心洞察
> 通过动态重加权偏好对，同时考虑内在数据质量和模型当前性能，并选择性增强困难高质量正样本的概率，训练更加高效且鲁棒。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Uni-DPO：大语言模型动态偏好优化的统一范式 |
| 英文题名 | Uni-DPO: A Unified Paradigm for Dynamic Preference Optimization of LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=G7DBGlgjjp) · [GitHub](https://github.com/pspdada/Uni-DPO) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Uni-DPO |
| Dataset | AlpacaEval 2.0, Arena-Hard, Math Reasoning (Average 8 tasks), MME (Multimodal) |

> [!tip] 效果简介
> - AlpacaEval 2.0 上，Length-Controlled Win Rate (LC%) 为 23.8，对比 19.4 (SimPO)，变化 +4.4。
> - Arena-Hard 上，Win Rate (WR%) 为 67.1，对比 59.1 (SimPO)，变化 +8.0。
> - Math Reasoning (Average 8 tasks) 上，Accuracy (%) 为 56.80，对比 53.73 (SimPO)，变化 +3.07。

## 概要

### 问题与瓶颈

基于人类偏好的直接偏好优化（DPO）已成为对齐大语言模型（LLM）的主流范式，但现有 DPO 方法存在一个核心瓶颈：**平等对待所有偏好对，忽略了数据质量和学习难度的差异**。训练数据中，高质量偏好对的正负样本差异清晰、能有效反映人类偏好，而低质量偏好对的差异模糊、无法准确表征偏好信号（Figure 2）。同时，模型对不同样本的学习进度并不一致——部分高质量样本可能已被充分拟合，过度强调它们会导致过拟合（Figure 5c）。这种“一刀切”的训练策略导致数据利用效率低下和次优性能。

### 核心方法

Uni-DPO 提出了一种**统一的动态偏好优化范式**，通过双视角自适应加权机制和校准负对数似然损失来协同解决上述问题：

- **质量权重 $w_{\mathrm{qual}}$**：基于外部评分边际 $S_w - S_l$ 自适应地提升高质量偏好对的权重，抑制低质量样本的影响（Eq. 5）。
- **性能权重 $w_{\mathrm{perf}}$**：根据模型当前表现动态调整学习焦点——对已充分拟合的样本降低权重，将训练资源集中于尚未学好的困难样本，从而缓解过拟合（Eq. 10）。该权重引入长度归一化和统一阈值 $\tau_{\mathrm{ref}}$ 以保证训练稳定性（Figure 5b）。
- **校准负对数似然损失 $\mathcal{L}_{\mathrm{c-NLL}}$**：仅对“参考模型优于策略模型”且“外部评分达到高质量阈值”的正样本施加额外概率增强，精准提升困难高质量样本的生成概率（Eq. 11）。

三个组件通过乘法融合（$w_{\mathrm{qual}} \cdot w_{\mathrm{perf}}$），使训练梯度聚焦于**高质量且尚未拟合**的偏好对（Figure 4 四象限分析），同时通过 $\mathcal{L}_{\mathrm{c-NLL}}$ 选择性强化这些样本的正响应。

### 方法定位

Uni-DPO 在偏好优化方法谱系中处于 DPO 的扩展位置：它保留了 DPO 的无显式奖励模型特性，但引入了**数据质量感知**和**模型性能感知**两个新维度。与标准 DPO（Rafailov et al., 2023）和 SimPO（Meng et al., 2024）等无参考模型变体相比，Uni-DPO 不改变基础优化目标的形式，而是通过动态重加权和校准损失来提升训练效率和鲁棒性。

### 主要结果

Uni-DPO 在文本理解、数学推理和多模态三个领域均一致超越 DPO 和 SimPO：

- **文本理解**：在 AlpacaEval 2.0 上，Llama3-8B Base 的 Length-Controlled Win Rate 达到 **23.8%**（SimPO 为 19.4%，提升 +4.4）；在 Arena-Hard 上，Gemma-2-9B-IT 的 Win Rate 达到 **67.1%**（SimPO 为 59.1%，提升 +8.0）（Table 1）。
- **数学推理**：在 8 个数学基准的平均准确率上，Qwen2.5-Math 7B 达到 **56.80%**（SimPO 为 53.73%，提升 +3.07），且 1.5B 和 7B 两个规模均取得显著提升（Table 2）。
- **多模态**：在 MME 基准上，Qwen2-VL-2B 得分达到 **1905.1**（SimPO 为 1813.2，提升 +91.9）（Table D.4）。

### 消融验证

消融实验（Table 3）表明，移除 $w_{\mathrm{qual}}$、$w_{\mathrm{perf}}$、长度归一化或 $\mathcal{L}_{\mathrm{c-NLL}}$ 中任一组件均导致性能一致下降，证实了每个组件的独立贡献。其中，移除性能权重会在 AlpacaEval 2.0 上造成尤为显著的性能退化，而移除长度归一化则几乎使模型无提升，凸显了训练稳定性的关键作用。$\mathcal{L}_{\mathrm{c-NLL}}$ 的两个指示器函数各自均有正向贡献（Table D.7）。即使使用较弱的评分模型（如 Qwen2.5-72B、ArmoRM-7.5B），Uni-DPO 仍保持竞争力（Table D.9），表明方法对评分质量具有较好的鲁棒性。

### 局限与展望

该方法依赖外部专家评分信号，超参数 $\gamma$ 和 $\tau_{\mathrm{ref}}$ 可能需要针对不同任务进行调整，且未在 70B+ 超大规模模型上进一步验证可扩展性。未来工作可探索更精细的数据质量估计方法，以及 $\mathcal{L}_{\mathrm{c-NLL}}$ 在不同领域的最优强度配置。



### 偏好优化中的数据利用瓶颈

大语言模型的对齐训练已广泛采用直接偏好优化方法，其中 **DPO**（Rafailov et al., 2023）通过直接在偏好数据上学习策略，绕过显式奖励建模，成为主流范式。DPO 的训练目标为：

$$\mathcal{L}_{\mathrm{DPO}} = -\mathbb{E}_{(x,y_w,y_l)\sim D}\left[ \log \sigma\Bigl( \beta \log \frac{\pi_{\theta}(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \beta \log \frac{\pi_{\theta}(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)} \Bigr) \right]$$

其核心机制是通过隐式奖励边际 $\Delta_r = r(x,y_w) - r(x,y_l)$ 来区分正负样本，其中隐式奖励定义为 $r(x,y) = \beta \log \frac{\pi_{\theta}(y|x)}{\pi_{\mathrm{ref}}(y|x)} + \beta \log Z(x)$。然而，DPO 及其变体（如无参考模型的 **SimPO**，Meng et al., 2024）存在一个关键局限：**平等对待所有偏好对，忽略了数据质量和学习难度的差异**。

### 数据质量与学习难度的双重忽视

现有方法面临两个相互交织的问题：

1. **数据质量不均**：偏好数据中，高质量样本对的正负差异清晰，能有效反映人类偏好；低质量样本对的正负边界模糊，无法准确代表人类偏好（Figure 2）。然而 DPO 对所有样本对赋予相同权重，导致低质量数据中的噪声干扰训练过程。

2. **学习难度差异被忽略**：模型在学习过程中对不同样本的拟合速度不同。已被模型充分学习的偏好对继续参与训练不仅效率低下，还可能导致过拟合——实验证据表明，仅使用质量权重而不引入性能权重时，训练损失持续下降而验证损失反而上升（Figure 5c）。

更关键的是，**数据质量与学习难度并非天然对齐**。在 UltraFeedback 数据集上，专家评分边际与模型奖励边际之间的 Spearman 相关系数仅为 $\rho = 0.08$（Figure 4b），几乎无相关性。这意味着高质量样本未必难以学习，低质量样本未必容易拟合。因此，仅从单一视角优化偏好数据必然导致数据利用效率低下和次优性能。

### 核心动机与解决思路

针对上述瓶颈，Uni-DPO 提出**统一动态偏好优化**范式，核心洞察是：通过动态重加权偏好对，同时考虑内在数据质量和模型当前性能，并选择性增强困难高质量正样本的概率，实现更高效且鲁棒的训练。具体而言，Uni-DPO 引入三个协同组件：

- **质量权重** $w_{\mathrm{qual}}$：基于外部评分边际自适应优先处理高质量样本，抑制低质量样本的影响；
- **性能权重** $w_{\mathrm{perf}}$：将学习焦点动态转移到尚未拟合的样本对，缓解过拟合；
- **校准负对数似然损失** $\mathcal{L}_{\mathrm{c-NLL}}$：仅针对困难且高质量的正样本增强其生成概率，进一步提升模型表现。

这种双视角加权机制引导优化轨迹朝向更能反映人类偏好的区域（Figure 3），从根本上解决了 DPO 类方法的数据利用效率问题。



## 核心方法与创新机理

Uni-DPO 的核心创新在于将偏好优化从“平等对待所有样本”的静态范式，转变为**基于数据质量与模型学习动态的联合自适应重加权**范式。其关键设计围绕三个相互协同的 changed slots 展开。

### 1. 质量权重：让模型学会区分“好”与“坏”的偏好对

现有 DPO 方法隐式假设所有偏好对同等重要，忽略了数据本身的质量差异——低质量偏好对中正负样本差异模糊，无法准确反映人类偏好（Figure 2）。Uni-DPO 引入**质量权重** $w_{\mathrm{qual}}$，利用外部评分边际直接量化数据质量：

$$w_{\mathrm{qual}}(y_w, y_l) = \sigma\big( \eta \cdot (S_w - S_l) \big)$$

其中 $S_w$、$S_l$ 分别为正负样本的外部评分，$\eta$ 控制权重对评分差异的敏感度。该设计使模型自动提升高质量偏好对的优化优先级，同时抑制低质量对的干扰。消融实验证实，移除 $w_{\mathrm{qual}}$ 会导致 AlpacaEval 2.0 和 Arena-Hard 上的性能显著下降（Table 3）。

### 2. 性能权重：动态抑制已拟合样本，缓解过拟合

即使数据质量高，若模型已充分学习某偏好对，继续强调该样本不仅低效，还可能导致过拟合。Uni-DPO 引入**性能权重** $w_{\mathrm{perf}}$，基于模型当前表现动态调整学习焦点：

$$w_{\mathrm{perf}} = \left[ 1 - \sigma\left( \frac{\beta}{|y_w|} \log \pi_\theta(y_w|x) - \frac{\beta}{|y_l|} \log \pi_\theta(y_l|x) - \tau_{\mathrm{ref}} \right) \right]^\gamma$$

该设计的三个关键改进：
- **长度归一化**：对 log 概率按响应长度归一化，消除序列长度对偏好信号的干扰，使优化目标真正反映偏好差异而非生成长度。
- **统一阈值 $\tau_{\mathrm{ref}}$**：替代直接 focal 权重中依赖参考模型表现的逐样本约束，解决了直接 focal 集成导致的训练不稳定问题（Figure 5b）。
- **$\gamma$ 调节衰减速度**：$\gamma$ 越大，对易分样本的权重衰减越剧烈，强制模型聚焦困难样本。

实验表明，移除 $w_{\mathrm{perf}}$ 后模型出现明显过拟合（训练损失下降而验证损失上升，Figure 5c），而加入 $w_{\mathrm{perf}}$ 有效缓解了该问题（Figure 5d），并在 AlpacaEval 2.0 上带来显著增益（Table 3）。

### 3. 校准负对数似然损失：选择性增强困难高质量正样本

单纯依赖偏好对比损失可能无法充分提升模型在正样本上的生成概率，尤其是那些参考模型表现更好且质量高的困难样本。Uni-DPO 提出**校准负对数似然损失** $\mathcal{L}_{\mathrm{c-NLL}}$：

$$\mathcal{L}_{\mathrm{c \cdot NLL}} = - \Big[ \mathbf{1}\big( \log \pi_{\mathrm{ref}}(y_w | x) > \log \pi_\theta(y_w | x) \big) \cdot \mathbf{1}\big( S_w \geq \tau_{\mathrm{good}} \big) \Big] \cdot \frac{\log \pi_\theta(y_w | x)}{|y_w|}$$

该损失通过两个指示器函数实现精确的样本筛选：
- **指示器 I**：仅当参考模型的 log 似然高于当前策略时激活，确保损失只作用于模型尚未学好的样本。
- **指示器 II**：仅当正样本评分 $S_w \geq \tau_{\mathrm{good}}$ 时激活，避免对低质量样本施加不必要的概率提升。

消融实验表明，两个指示器各自均有独立贡献，完整 $\mathcal{L}_{\mathrm{c-NLL}}$ 带来显著的性能提升（Table D.7）。

### 创新协同机制

三个 changed slots 通过**乘法组合**形成统一目标（Eq. (4)），在四象限样本空间中实现差异化处理（Figure 4）：高质量且困难样本获得最大权重，低质量或已拟合样本被有效抑制。这种“数据质量 × 模型动态”的双视角机制，使优化轨迹持续聚焦于最能反映人类偏好且尚未被学习的区域（Figure 3），从而在文本理解、数学推理和多模态任务上一致超越 DPO 和 SimPO（Table 1, Table 2, Table D.4）。



![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/004_Figure_3.jpg]]
*Figure 3: Comparison of DPO and Uni-DPO objectives. The Uni-DPO objective introduces a dual-perspective weighting mechanism, including a quality-aware weight $w _ { \mathrm { q u a l } }$ , a performance-based weight $w _ { \mathrm { p e r f } }$ . and a calibrated negative log-likelihood term $\bar { \mathcal { L } } _ { \mathrm { c - N L I } }$ that emphasizes challenging and high-quality positive samples. Left: schematic illustration of the two objectives. Right: compared with DPO, Uni-DPO dynamically reweights data pairs during training, guiding the optimization trajectory toward regions that better reflect human preference

Uni-DPO 的核心设计围绕一个统一动态偏好优化目标展开，其整体损失函数为：

$$
\mathcal{L}_{\mathrm{Uni-DPO}} = -\mathbb{E}_{(x,y_w,y_l)\sim D}\left[ w_{\mathrm{qual}}(y_w,y_l) \cdot w_{\mathrm{perf}}(\pi_\theta) \cdot \log \sigma(\Delta_r) \right] + \lambda \mathcal{L}_{\mathrm{c-NLL}}
$$

该目标在标准 DPO 损失的基础上引入了三个协同工作的模块，形成一个从数据质量感知到模型动态适应的完整优化管线。

**管线流程与模块关系：**

1. **质量权重模块（Quality Weighting Factor）**  
   输入为偏好对 $(x, y_w, y_l)$ 的外部评分 $S_w$ 和 $S_l$，通过评分边际计算质量权重：
   $$w_{\mathrm{qual}}(y_w, y_l) = \sigma\big( \eta \cdot (S_w - S_l) \big)$$
   该权重自适应地提升高质量偏好对（正负样本区分清晰）的贡献，抑制低质量偏好对（正负样本差异模糊）的影响。

2. **性能权重模块（Performance Weighting Factor）**  
   输入为策略模型 $\pi_\theta$ 对正负样本的长度归一化对数概率，结合统一阈值 $\tau_{\mathrm{ref}}$ 和聚焦参数 $\gamma$，计算动态性能权重：
   $$w_{\mathrm{perf}} = \left[ 1 - \sigma\left( \frac{\beta}{|y_w|} \log \pi_\theta(y_w|x) - \frac{\beta}{|y_l|} \log \pi_\theta(y_l|x) - \tau_{\mathrm{ref}} \right) \right]^\gamma$$
   该权重随模型对当前样本拟合程度的提升而衰减，将学习焦点从已充分学习的样本转移至尚未拟合的困难样本，从而缓解过拟合（消融实验中移除 $w_{\mathrm{perf}}$ 后训练损失下降而评估损失上升，见 Figure 5c-d）。

3. **校准负对数似然损失（Calibrated NLL Loss）**  
   在 DPO 主损失之外，选择性对困难且高质量的正样本施加额外监督：
   $$\mathcal{L}_{\mathrm{c-NLL}} = - \left[ \mathbf{1}\big( \log \pi_{\mathrm{ref}}(y_w | x) > \log \pi_\theta(y_w | x) \big) \cdot \mathbf{1}\big( S_w \geq \tau_{\mathrm{good}} \big) \right] \cdot \frac{\log \pi_\theta(y_w | x)}{|y_w|}$$
   两个指示器函数共同约束：仅当参考模型对正样本的对数概率高于当前策略模型（即该正样本对模型而言仍困难），且该正样本的评分达到高质量阈值 $\tau_{\mathrm{good}}$ 时，才施加长度归一化的 NLL 损失，以增强模型对高质量正样本的生成概率。

**模块间的协同机制：** 质量权重 $w_{\mathrm{qual}}$ 和性能权重 $w_{\mathrm{perf}}$ 以乘法形式组合（$w_{\mathrm{qual}} \cdot w_{\mathrm{perf}}$），共同作用于 DPO 损失中每个偏好对的梯度贡献。这种双视角加权机制使得优化轨迹被引导至**既高质量又尚未被模型充分拟合**的样本区域。校准 NLL 损失 $\mathcal{L}_{\mathrm{c-NLL}}$ 则以较小的系数 $\lambda$（实验中固定为 0.001）作为补充，进一步强化困难高质量正样本的概率提升。

**输入输出流：** 整个管线接收偏好数据集 $D$（包含提示 $x$、正样本 $y_w$、负样本 $y_l$ 及其外部评分 $S_w, S_l$）、参考模型 $\pi_{\mathrm{ref}}$ 和当前策略模型 $\pi_\theta$，输出标量损失值。训练过程中，$w_{\mathrm{perf}}$ 随策略模型更新而动态变化，$w_{\mathrm{qual}}$ 在数据预处理阶段固定，二者联合实现了训练全程的自适应数据利用。



Uni-DPO 的训练目标由三个核心模块构成：质量权重（Quality Weighting Factor）、性能权重（Performance Weighting Factor）和校准负对数似然损失（Calibrated NLL Loss）。整体损失函数为：

$$
\mathcal{L}_{\mathrm{Uni-DPO}} = -\mathbb{E}_{(x,y_w,y_l)\sim D}\left[ w_{\mathrm{qual}}(y_w,y_l) \cdot w_{\mathrm{perf}}(\pi_\theta) \cdot \log \sigma(\Delta_r) \right] + \lambda \mathcal{L}_{\mathrm{c-NLL}} \tag{4}
$$

其中 $\Delta_r = r(x, y_w) - r(x, y_l)$ 为隐式奖励边际，衡量正负样本在模型当前策略下的奖励差异。以下逐一解析各模块的公式与变量含义。

---

### 1. 质量权重 $w_{\mathrm{qual}}$

该模块根据偏好对的内在质量差异进行加权，使模型优先学习高质量样本对：

$$
w_{\mathrm{qual}}(y_w, y_l) = \sigma\big( \eta \cdot (S_w - S_l) \big) \tag{5}
$$

- $S_w$、$S_l$：分别表示正样本 $y_w$ 和负样本 $y_l$ 的外部评分（由专家打分模型给出）。
- $\eta$：控制评分边际对权重敏感度的超参数。
- $\sigma(\cdot)$：Sigmoid 函数，将评分边际映射到 $(0, 1)$ 区间。

**机制**：当正负样本的评分差距 $S_w - S_l$ 较大时，说明该偏好对质量高、区分度清晰，$w_{\mathrm{qual}}$ 趋近于 1，赋予更高学习权重；反之，评分差距小的低质量样本对权重被压低，减少其对训练的干扰。

---

### 2. 性能权重 $w_{\mathrm{perf}}$

该模块根据模型当前表现动态调整学习焦点，降低已充分拟合样本的权重以缓解过拟合。其设计经历了从直接 Focal Loss 集成到稳定化变体的演进。

**Focal Loss 基础形式**（用于目标检测，降低易分样本权重）：

$$
\mathcal{L}_{\mathrm{FL}}(p_t) = - (1-p_t)^\gamma \log(p_t) \tag{6}
$$

其中 $p_t$ 为模型对正确类别的预测概率，$\gamma$ 控制降权强度。

**直接 Focal 加权 DPO**（存在训练不稳定问题）：

$$
w_{\mathrm{focal}} = \left[1 - \sigma\left(\beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)}\right)\right]^{\gamma} \tag{7}
$$

**问题**：该形式下每个样本的权重阈值依赖于参考模型在该样本上的表现，导致不同样本间的约束不统一，训练梯度不稳定（见 Figure 5b）。

**Uni-DPO 的稳定化性能权重**（引入长度归一化和统一阈值）：

$$
w_{\mathrm{perf}} = \left[ 1 - \sigma\left( \frac{\beta}{|y_w|} \log \pi_\theta(y_w|x) - \frac{\beta}{|y_l|} \log \pi_\theta(y_l|x) - \tau_{\mathrm{ref}} \right) \right]^\gamma \tag{10}
$$

- $|y_w|$、$|y_l|$：正负样本的 token 长度，用于长度归一化，确保优化目标反映偏好差异而非序列长度。
- $\tau_{\mathrm{ref}}$：统一性能阈值，替代原 Focal 权重中依赖参考模型表现的动态阈值，解耦参考模型影响。
- $\gamma$：控制对易分样本的降权强度，$\gamma$ 越大，梯度在易分样本上衰减越快。

**机制**：当模型对正负样本的归一化对数概率差（即当前策略的偏好区分度）超过 $\tau_{\mathrm{ref}}$ 时，$w_{\mathrm{perf}}$ 降低，减少对该样本对的更新；反之，对尚未充分学习的困难样本保持较高权重。消融实验证实，移除 $w_{\mathrm{perf}}$ 会导致训练损失下降而验证损失上升的过拟合现象（Figure 5c），加入后有效缓解（Figure 5d）。

---

### 3. 校准负对数似然损失 $\mathcal{L}_{\mathrm{c-NLL}}$

该模块选择性增强困难且高质量正样本的生成概率：

$$
\mathcal{L}_{\mathrm{c \cdot NLL}} = - \left[ \mathbf{1}\Bigl( \log \pi_{\mathrm{ref}}(y_w | x) > \log \pi_\theta(y_w | x) \Bigr) \mathbf{1}\Bigl( S_w \geq \tau_{\mathrm{good}} \Bigr) \right] \cdot \frac{\log \pi_\theta(y_w | x)}{|y_w|} \tag{11}
$$

- **指示器 I**：$\mathbf{1}(\log \pi_{\mathrm{ref}}(y_w|x) > \log \pi_\theta(y_w|x))$，仅当参考模型对正样本的对数概率高于当前策略时激活，确保损失只作用于模型尚未学好的正样本。
- **指示器 II**：$\mathbf{1}(S_w \geq \tau_{\mathrm{good}})$，仅当正样本的外部评分达到高质量阈值 $\tau_{\mathrm{good}}$ 时激活，避免对低质量样本施加 NLL 损失。
- $\frac{\log \pi_\theta(y_w|x)}{|y_w|}$：长度归一化的对数概率，直接提升正样本的生成概率。

**机制**：两个指示器的联合作用将 NLL 损失精确限定在“参考模型表现优于当前策略且样本本身高质量”的正样本上，既避免了对已充分学习样本的冗余强化，也防止了对低质量样本的错误引导。消融实验表明，两个指示器各自均有独立贡献（Table D.7）。

---

### 4. 双视角权重协同

$w_{\mathrm{qual}}$ 和 $w_{\mathrm{perf}}$ 以乘法方式结合，形成对训练样本的四象限划分（Figure 4）：

|  | 高质量 | 低质量 |
|---|---|---|
| **困难（模型未学好）** | 高 $w_{\mathrm{qual}}$ × 高 $w_{\mathrm{perf}}$ → 最大权重 | 低 $w_{\mathrm{qual}}$ × 高 $w_{\mathrm{perf}}$ → 中等权重 |
| **简单（模型已学好）** | 高 $w_{\mathrm{qual}}$ × 低 $w_{\mathrm{perf}}$ → 中等权重 | 低 $w_{\mathrm{qual}}$ × 低 $w_{\mathrm{perf}}$ → 最小权重 |

数据质量（评分边际）与学习难度（奖励边际）并非天然对齐（Spearman 相关系数 $\rho$ 较低，Figure 4b），因此双视角加权机制是必要的——它确保训练资源集中于“高质量且尚未学好”的样本，同时抑制低质量或已过拟合样本的影响。



## 实验与关键发现

### 主要结果

Uni-DPO 在文本理解、数学推理和多模态三大类基准上一致超越 DPO 和 SimPO，且在不同模型规模和架构上均表现出稳定的增益。

**文本理解**（Table 1）：在 AlpacaEval 2.0 上，Llama3-8B Base 经 Uni-DPO 微调后长度控制胜率（LC%）达到 23.8，较 SimPO 的 19.4 提升 +4.4，较 DPO 的 15.5 提升 +8.3。在 Arena-Hard 上，Gemma-2-9B-IT 经 Uni-DPO 微调后胜率（WR%）达到 67.1，较 SimPO 的 59.1 提升 +8.0，并超越 Claude 3 Opus（60.4）和 Llama-3.1-70B-Instruct（55.7）。在 IFEval 和 SedarEval 上，Uni-DPO 同样保持领先。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/010_Table_1.jpg]]
*Table 1: Main evaluation result of textual understanding. WR denotes the Win Rate, LC denotes the Length-Controlled win rate, and Acc. denotes the Accuracy. The best results are highlighted in bold. The results show that Uni-DPO consistently outperforms the SimPO and DPO methods across models and benchmarks*

**数学推理**（Table 2）：在 Qwen2.5-Math 7B 上，Uni-DPO 在 8 个数学基准上的平均准确率达到 56.80%，较 SimPO 的 53.73% 提升 +3.07%，较 DPO 的 51.55% 提升 +5.25%。在 1.5B 模型上，Uni-DPO 的平均增益为 8.3 个百分点，在 7B 模型上进一步扩大至 17.7 个百分点，表明方法具有良好的模型规模可扩展性。所有数学推理评估统一采用 zero-shot 链式思维提示和贪心解码。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/011_Table_2.jpg]]
*Table 2: Main evaluation result of mathematical reasoning. All benchmarks are evaluated with zero-shot chain-of-thought prompting and greedy decoding. The best results are highlighted in bold. The Uni-DPO method delivers significant improvements across all eight benchmarks for both 1.5B and 7B model scales*

**多模态任务**（Table D.4）：在 Qwen2-VL-2B 基座模型上，Uni-DPO 在 10 个多模态基准中的 9 个上取得最优结果。MME 得分达到 1905.1，较 SimPO 的 1813.2 提升 +91.9，较 DPO 的 1786.3 提升 +118.8。

**可扩展性**（Figure 6d–e）：在 Qwen2.5 系列 0.5B 至 14B 共 5 个模型规模上，Uni-DPO 一致优于 SimPO，验证了方法的跨规模可扩展性。

### 消融分析

Table 3 的系统消融实验证实了 Uni-DPO 四个核心组件的独立贡献。在 Llama3-8B Base 和 Instruct 上分别移除质量权重 $w_{\text{qual}}$、性能权重 $w_{\text{perf}}$、长度归一化（LN）或校准 NLL 损失 $\mathcal{L}_{\text{c-NLL}}$，均导致性能一致下降：

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/012_Table_3.jpg]]
*Table 3: Main ablation results. Removing either the quality weight $w _ { \mathrm { q u a l } }$ , the performance weight $w _ { \mathrm { p e r f } }$ , length normalization (LN), or the calibrated NLL loss $\mathcal { L } _ { \mathrm { c - N L L } }$ consistently degrades performance compared to Uni-DPO, confirming that each component of Uni-DPO contributes meaningfully to its overall effectiveness

- **移除 $w_{\text{qual}}$**：质量权重消融后，模型无法区分高低质量偏好对，在 AlpacaEval 2.0 和 Arena-Hard 上均出现显著性能退化。
- **移除 $w_{\text{perf}}$**：性能权重消融后，模型对已拟合样本过度学习，导致过拟合。Figure 5c 显示训练损失持续下降而验证损失上升，而加入 $w_{\text{perf}}$ 后（Figure 5d）该过拟合现象得到有效抑制。
- **移除长度归一化**：长度归一化对训练稳定性至关重要，移除后模型几乎无提升，表明直接使用未归一化的对数概率会导致优化目标偏向长序列而非偏好差异本身。
- **移除 $\mathcal{L}_{\text{c-NLL}}$**：校准 NLL 损失的消融（Table D.7）进一步表明，其两个指示器函数各自均有贡献——第一个指示器确保仅在参考模型优于策略时施加惩罚，第二个指示器限制仅对高质量正样本施加惩罚，同时移除两者性能下降最为严重。

### 组件机制与训练动态

**质量权重与性能权重的协同**（Figure 4）：奖励边际 $\Delta_r$ 与评分边际 $S_w - S_l$ 的 Spearman 相关系数较低，表明数据质量与学习难度并不天然对齐——高质量偏好对可能已被模型轻易拟合，而低质量偏好对可能仍处于困难状态。Uni-DPO 通过 $w_{\text{qual}} \cdot w_{\text{perf}}$ 的乘法组合，将优化重点引导至“高质量且尚未拟合”的样本象限，同时抑制低质量样本和已过拟合样本的梯度贡献。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/005_Figure_4.jpg]]
*Figure 4: Analysis of reward margin versus score margin. (a) Illustrative reward margin versus score margin examples across training data. The four quadrants reflect the combinations of high/low data quality and easy/hard learning difficulty. (b) Distribution of reward margin (y-axis) versus score margin (x-axis), along with their Spearman correlation coefficient $\rho$ , indicating data quality is not necessarily aligned with learning difficulty, suggesting the need to account for both factors during training. (c) Demonstration of dual-perspective weighting mechanism: the quality weight $w _ { \mathrm { q u a l } }$ where: (top) rises with data quality, while the performance weight $w _ { \mathrm { p e r...$

**性能权重的稳定性设计**（Figure 5a–b）：直接将 focal loss 的加权因子 $w_{\text{focal}}$ 引入偏好学习会导致训练不稳定（梯度范数剧烈波动）。Uni-DPO 通过引入固定的统一性能阈值 $\tau_{\text{ref}}$ 并施加长度归一化，解耦了边际约束与参考模型性能的关系，实现了稳定的训练动态。

### 参数敏感性与鲁棒性

性能权重超参数 $\gamma$ 和 $\tau_{\text{ref}}$ 的敏感性分析（Figure 6a–c）表明：$\gamma$ 在 [1.0, 5.0] 范围内、$\tau_{\text{ref}}$ 在 [0.5, 2.0] 范围内均能取得有竞争力的结果。较高的 $\gamma$ 意味着对简单样本的梯度衰减更剧烈，需要更强的边际约束 $\tau_{\text{ref}}$ 来维持训练稳定性。其余超参数（$w_{\text{qual}}=0.7$，$\lambda=0.001$，$\tau_{\text{good}}=3.2$）在所有模型和基准上保持固定，体现了方法的鲁棒性。

此外，即使使用较弱的开源评分模型（如 Qwen2.5-72B、ArmoRM-7.5B）替代强评分模型来估计数据质量，Uni-DPO 仍保持竞争性或更优性能（Table D.9），降低了对高质量外部评分的依赖。

### 局限与待验证点

- 方法依赖于外部专家评分来构建质量权重，尽管弱评分模型下的鲁棒性已得到初步验证，但在无评分信号的场景中适用性尚不明确。
- 性能权重的超参数 $\gamma$ 和 $\tau_{\text{ref}}$ 在不同任务间可能需要针对性调整，文中给出的实用范围基于当前实验配置，跨领域泛化时需额外验证。
- 最大验证模型规模为 14B，在 70B+ 规模上的可扩展性仍需进一步确认。
- $\mathcal{L}_{\text{c-NLL}}$ 中第一个指示器可能需要额外的边际参数 $\tau_{\text{in}}$ 以获得最优结果，该方向有待探索。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/024_Table_7.jpg]]
*Table 7: Table D.4: Main result of multimodal tasks. We evaluate the performance of Qwen2-VL-2B (Wang et al., 2024d) base model on various multimodal benchmarks. The best results are highlighted in bold and the second best in underline. The results demonstrate that Uni-DPO consistently outperforms the baseline, DPO, and SimPO across all benchmarks, achieving significant improvements in overall performance*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/020_Table_4.jpg]]
*Table 4: Table C.1: Training setup for textual understanding evaluation. We maintain largely consistent hyperparameter configurations across all model variants and datasets to demonstrate the robustness and scalability of Uni-DPO. In this table, the placeholder x in Qwen2.5-xB denotes the model size in billions of parameters, with x $\in \{$ 0 . 5 , 1 . 5 , 3 , 7 , 1 4 $\}$ . We set the threshold $\tau _ { \mathrm { g o o d } }$ = 3 . 2 since this value corresponds to the median score of the chosen response $y _ { w }$ in the training dataset, thereby reflecting the central tendency of the score distribution

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/021_Table_5.jpg]]
*Table 5: Table C.3: Training setup for math reasoning and multimodal tasks. We maintained largely consistent hyperparameter configurations across all models to demonstrate the robustness and scalability of Uni-DPO*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/023_Table_6.jpg]]
*Table 6: Table D.1: Evaluation benchmarks for textual understanding. The baseline model refers to the model being compared against. A unified judge model GPT-4o 2024-05-13 is employed across benchmarks to ensure fairness*


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/026_Table_9.jpg]]
*Table 9: Table D.6: Result of textual understanding in Qwen2.5 model. WR denotes the Win Rate, LC denotes the Length-Controlled win rate, and Acc. denotes the Accuracy. The best results are highlighted in bold. The results show that our Uni-DPO method consistently outperforms SimPO across various model sizes and benchmarks*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_G7DBGlgjjp/figures/028_Table_10.jpg]]
*Table 10: Table D.7: Calibrated negative log-likelihood loss $\mathcal { L } _ { \mathbf { c } \mathbf { . } \mathbf { N L L } }$ ablation results. The full c-NLL loss delivers substantial performance gains, and each of the two indicator functions makes a meaningful contribution to the overall improvement, which demonstrates the effectiveness of our proposed loss function



## 定位与知识库关联

### 1 方法沿革与基线关系

Uni-DPO 建立在直接偏好优化（Direct Preference Optimization, DPO）的范式之上。DPO（Rafailov et al., 2023）通过将偏好学习重新参数化为策略与参考模型的对数概率比，绕过了显式奖励模型的训练，成为 RLHF 的高效替代方案。其核心目标为：

$$\mathcal{L}_{\mathrm{DPO}} = -\mathbb{E}_{(x,y_w,y_l)\sim D}\left[ \log \sigma\Bigl( \beta \log \frac{\pi_{\theta}(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \beta \log \frac{\pi_{\theta}(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)} \Bigr) \right]$$

然而，DPO 平等对待所有偏好对，未区分数据质量与学习难度的差异。SimPO（Meng et al., 2024）在此基础上引入了长度归一化和无参考模型的简化形式，但同样未对偏好对进行动态加权。Uni-DPO 的核心突破在于识别了一个关键瓶颈：**数据质量（偏好对中正负样本的区分度）与模型学习动态（当前策略对该对的拟合程度）并非天然对齐**——高质量样本可能已被模型充分学习，而低质量样本可能仍未被正确拟合。Figure 4 通过奖励边际与评分边际的 Spearman 相关性分析验证了这一判断，表明仅凭单一维度无法有效指导训练。

针对上述瓶颈，Uni-DPO 引入了三个协同工作的新组件：

- **质量权重** $w_{\mathrm{qual}} = \sigma(\eta \cdot (S_w - S_l))$：基于外部评分边际，优先关注高质量偏好对。
- **性能权重** $w_{\mathrm{perf}} = \left[ 1 - \sigma\left( \frac{\beta}{|y_w|} \log \pi_\theta(y_w|x) - \frac{\beta}{|y_l|} \log \pi_\theta(y_l|x) - \tau_{\mathrm{ref}} \right) \right]^\gamma$：受 Focal Loss 启发，动态降低已拟合样本的权重，并通过统一阈值 $\tau_{\mathrm{ref}}$ 和长度归一化稳定训练。
- **校准负对数似然损失** $\mathcal{L}_{\mathrm{c-NLL}}$：仅对参考模型优于策略且质量高的正样本施加，选择性增强困难样本的概率。

完整目标函数为：

$$\mathcal{L}_{\mathrm{Uni-DPO}} = -\mathbb{E}_{(x,y_w,y_l)\sim D}\left[ w_{\mathrm{qual}} \cdot w_{\mathrm{perf}} \cdot \log \sigma(\Delta_r) \right] + \lambda \mathcal{L}_{\mathrm{c-NLL}}$$

从方法谱系看，Uni-DPO 与 $\beta$-DPO 和 D²PO 等后续工作形成直接对比。论文 Table F.1 报告了 Uni-DPO 与二者的对比结果，Uni-DPO 在各基准上一致取得更优性能，验证了其双视角动态加权机制的有效性。

### 2 适用边界与关键约束

Uni-DPO 的适用边界由以下因素界定：

1. **对外部评分的依赖**：质量权重 $w_{\mathrm{qual}}$ 需要偏好对的正负样本评分。论文在 Table D.9 中验证了即使使用较弱打分模型（如 Qwen2.5-72B、ArmoRM-7.5B），Uni-DPO 仍保持竞争力，但性能会随评分质量下降而衰减。在无评分标注的场景下，该组件无法直接使用。

2. **超参数敏感性**：性能权重 $w_{\mathrm{perf}}$ 的两个关键超参数 $\gamma$ 和 $\tau_{\mathrm{ref}}$ 存在耦合关系。Figure 6(a)-(c) 显示，$\gamma$ 的实用范围为 [1.0, 5.0]，$\tau_{\mathrm{ref}}$ 为 [0.5, 2.0]，且较高的 $\gamma$ 需要更强的边际约束 $\tau_{\mathrm{ref}}$。论文在所有实验中固定 $\gamma=3.0$，但不同任务可能需要独立调参。

3. **模型规模验证范围**：论文主要验证了 1.5B 至 9B 参数规模的模型。Figure 6(d)-(e) 展示了在该范围内的可扩展性，但未在 70B+ 级别模型上进一步验证。

4. **校准 NLL 损失的阈值依赖**：$\mathcal{L}_{\mathrm{c-NLL}}$ 中的质量阈值 $\tau_{\mathrm{good}}$ 固定为 3.2，其最优值在不同领域和评分体系下可能需要调整。Table D.7 的消融表明两个指示器函数各自均有贡献，但第一个指示器（参考模型优于策略）可能需要额外的边际参数 $\tau_{\mathrm{in}}$ 以获得最佳结果。

### 3 局限与开放问题

**已识别的局限**：

- 方法依赖外部专家评分，尽管对弱评分模型具有鲁棒性，但在完全无评分信号的场景下，质量权重组件将失效。
- 超参数 $\gamma$ 和 $\tau_{\mathrm{ref}}$ 的耦合关系增加了调参复杂度，论文未提供自动化的参数选择策略。
- 未在超大模型（70B+）上验证可扩展性，大规模下的训练稳定性和收益有待确认。

**开放问题**：

1. **更精细的数据质量估计**：当前 $w_{\mathrm{qual}}$ 仅基于评分边际的 sigmoid 变换，未来可探索利用偏好对语义一致性、推理链质量等多维信号构建更鲁棒的质量度量。

2. **校准 NLL 损失的优化**：$\mathcal{L}_{\mathrm{c-NLL}}$ 的第一个指示器可能需要引入额外的边际参数 $\tau_{\mathrm{in}}$，且不同领域中的最优强度 $\lambda$ 需要系统研究。

3. **不同偏好优化策略的系统性影响**：Uni-DPO 的双视角加权机制是否可推广到其他偏好优化框架（如 KTO、ORPO），以及各组件在不同数据分布下的相对贡献，值得进一步分析。

4. **训练效率与权重计算开销**：$w_{\mathrm{perf}}$ 需要在每个训练步计算策略的对数概率，其计算开销在大规模数据下的影响未在论文中量化讨论。



## 原文 PDF

![[paperPDFs/ICLR_2026/Uni_DPO_A_Unified_Paradigm_for_Dynamic_Preference_Optimization_of_LLMs.pdf]]
