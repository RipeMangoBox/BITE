---
title: "P$^2$-DPO: Grounding Hallucination in Perceptual Processing via Calibration Direct Preference Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/P2_DPO_Grounding_Hallucination_in_Perceptual_Processing_via_Calibration_Direct_Preference_Optimization.pdf
project_link: null
code_link: null
aliases:
- PPDPOPD
- P2DGHPPCDPO
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "The causal knob is the visual input signal: by directly manipulating the image (crop/enhance for winning, erase/degrade/noise for losing), the method creates a Visual Information..."
primary_logic: "Hallucination in LVLMs can be categorized into Perception failures (model cannot see) and Perceptual Processing failures (model sees but still hallucinates). The latter is an underexplored, self-correctable bottleneck. By framing preference optimization as a self-supervised visual grounding task—where the model learns from its own on-policy, vision-aware preference pairs generated through visual interventions—we can..."
claims:
- "P2-DPO significantly improves Attention Focus Ratio (AFR) from 14.73 to 18.71 and Processing Accuracy from 66.29% to 70.10% on TextVQA, directly validating perceptual bottleneck m..."
- "Under Gaussian noise (σ=0.20) on the POPE benchmark, P2-DPO achieves >4 F1 points higher than the base model, demonstrating enhanced visual robustness."
- "P2-DPO achieves a substantial +8.5 F1R gain over the base LLaVA-1.5-7B on AMBER's relational reasoning, and reduces MMHal hallucination rate by -3.13% on Qwen2.5-VL-3B, outperform..."
- "TextVQA (Attention Focus Ratio) 上 AFR (Avg. ↑) = 18.71"
---

# P$^2$-DPO: Grounding Hallucination in Perceptual Processing via Calibration Direct Preference Optimization

> [!tip] 核心洞察
> Hallucination in LVLMs can be categorized into Perception failures (model cannot see) and Perceptual Processing failures (model sees but still hallucinates). The latter is an underexplored, self-correctable bottleneck. By framing preference optimization as a self-supervised visual grounding task—where the model learns from its own on-policy, vision-aware preference pairs generated through visual interventions—we can effectively reduce hallucinations without any external human feedback.

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | P$^2$-DPO：通过校准直接偏好优化在感知处理中消除幻觉 |
| 英文题名 | P$^2$-DPO: Grounding Hallucination in Perceptual Processing via Calibration Direct Preference Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ekOwxTn65Y) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Perceptual Processing Direct Preference Optimization (P2-DPO) |
| Dataset | TextVQA (Attention Focus Ratio), TextVQA (Processing Accuracy), POPE under Gaussian noise (σ=0.20), AMBER (relational reasoning) on Qwen2.5-VL-3B |

> [!tip] 效果简介
> - TextVQA (Attention Focus Ratio) 上，AFR (Avg. ↑) 为 18.71，对比 14.73，变化 +3.98。
> - TextVQA (Processing Accuracy) 上，P-Acc. (% ↑) 为 70.10%，对比 66.29%，变化 +3.81%。
> - POPE under Gaussian noise (σ=0.20) 上，F1 Score 为 exceeds baseline by >4 points，对比 LLaVA-1.5-7B，变化 >+4。

## 概要

大视觉语言模型（LVLM）的幻觉现象不仅源于纯粹感知失败，更深层的问题在于**感知处理阶段的缺陷**：模型即使正确聚焦于关键区域仍会输出错误答案（感知瓶颈），同时对轻微视觉扰动缺乏鲁棒性。现有基于直接偏好优化（DPO）的缓解方法大多依赖视觉无关、离线的偏好对，难以向视觉主导参数提供充分的优化信号，导致这些感知处理层面的错误难以被矫正。

本文提出 **P²‑DPO (Perceptual Processing Direct Preference Optimization)**，一种完全自监督、在策略的训练范式。其核心思想是直接操纵视觉输入构造**视觉感知偏好对**（增强/聚焦图像作为胜出响应，擦除/加噪图像作为落后响应），迫使模型依赖视觉证据；并引入**校准损失**显式最大化优选响应的视觉信息依赖，同时通过**动态缺失权重**自适应平衡聚焦增强与视觉鲁棒性两种目标。整个流程无需任何人类反馈或外部标注。

实验结果表明该方法显著缓解了感知瓶颈：在 TextVQA 上注意力聚焦比（AFR）从 14.73 提升至 18.71，处理准确率从 66.29% 提升至 70.10%；在 POPE 基准上面对逐渐增强的高斯噪声时，F1 分数较基线高出超过 4 分，展现出更强的视觉鲁棒性。在 AMBER、MMHal‑Bench 等多项幻觉基准上，P²‑DPO 一致超越基于昂贵人类反馈或 AI 反馈的对齐方法——例如 LLaVA‑1.5‑7B 的 AMBER 关系推理 F1R 提升 +8.5，Qwen2.5‑VL‑3B 的 MMHal‑Bench 幻觉率下降 3.13%。消融实验证实了视觉偏好对、校准损失及动态权重各自的重要贡献。



大型视觉语言模型（LVLMs）在多模态理解任务中取得了显著进展，但其普遍存在的“幻觉”现象——生成与图像事实不符的内容——严重制约了可靠性。已有工作大多将幻觉归因为模型“没有看到”相关信息，即纯粹的感知失败，并因此采用训练无关的解码策略（如VCD）或引入外部视觉专家进行后处理修正。然而，本文通过深入分析发现，LVLM幻觉的一个更隐蔽且更具自我修复潜力的根源在于**感知处理阶段的失败**，具体表现为两种典型形式（Figure 1）：  
1. **注意力区域内的感知瓶颈（Perceptual Bottleneck）**：模型的注意力尽管正确聚焦于关键实体，却依然输出错误答案，说明模型“看见”了却未能有效利用视觉证据；  
2. **视觉鲁棒性缺失（Lack of Visual Robustness）**：当图像受到人眼难以察觉的轻微噪声或模糊时，模型立即产生大量幻觉，暴露出其对视觉扰动极度敏感的本质。

这两类失效的本质不在前端感知，而在于模型在后处理阶段未能将已捕获的视觉信号转化为可靠输出，是一个迄今为止**未被充分探索、且具备自我纠正可能性的瓶颈**。

现有的对齐训练方法，例如基于人类偏好数据的DPO（DPO_RLHF‑V、V‑DPO_RLHF‑V）和AI反馈驱动的HA‑DPO，虽然在一定程度上改善了整体响应质量，但其偏好对构建存在两个根本缺陷，难以触达上述感知处理瓶颈：  
- **视觉不可知（vision‑agnostic）**：偏好数据多通过文本层面的事后语义修正（PSC）生成，不感知原始视觉输入，无法为视觉主导参数提供直接的优化信号；  
- **离策略（off‑policy）**：偏好对依赖外部人类标注或编辑，与模型自身的生成策略分布严重脱节。  
如式(1)与式(2)的分析所示，要使DPO对视觉参数产生有意义的更新，偏好对必须在视觉表示空间引起足够大的分离，从而增大视觉参数的Fisher信息量；而传统离策略且视觉不敏感的偏好数据恰恰缺失这一性质，导致训练信号难以渗透到感知处理环节。

基于上述洞察，本文的动机在于：**将幻觉问题重新定义为“感知处理失败”，并利用视觉干预构建自监督、在策略的偏好对，直接驱动视觉主导参数的校准**。通过故意在图像上制造“聚焦增强”与“擦除退化”、“清晰”与“噪声”的**视觉信息差异**，让模型从自身生成的响应中学会依赖视觉证据，从而在没有外部人工反馈的情况下，系统性地缓解感知瓶颈并提升视觉鲁棒性。这一思路促成了**P²‑DPO（Perceptual Processing Direct Preference Optimization）**方法，其核心即是通过在策略的视觉感知偏好对生成与校准损失的结合，将自监督视觉基础任务嵌入偏好优化框架之中。



## 核心方法与创新机理

现有对齐方法（如 HA-DPO、DPO_RLHF‑V）将幻觉仅归因于感知缺失，依赖离策略（off-policy）、视觉无关的偏好数据，并通过标准 DPO 损失优化文本响应。这类范式存在两大根本缺陷：（1）**视觉主导参数的梯度信号极弱**——离线编辑产生的偏好对在视觉主导参数上的梯度差 $\Delta(\theta_1)$ 趋于消失（见附录 Eq.18），导致模型无法有效学习视觉证据的利用；（2）**忽略感知处理瓶颈**——即使注意力正确聚焦，模型仍会输出错误答案（Figure 1 左），且轻微图像退化即可诱发幻觉（Figure 1 右）。P²-DPO 针对上述缺陷，在**偏好数据构造**与**优化目标设计**两个维度实现关键转变，构成其核心创新。

### 1. 从“视觉无关离策略修订”到“视觉交互在策略对比”：VCPG 数据生成范式

传统方法通过外部语义编辑将错误回答修订为正确回答，构建偏好对（PSC 策略）。该过程不引入额外视觉信号，导致赢/输响应之间的视觉信息依赖度（VID）差异微小，DPO 无法向视觉参数集中优化压力。P²-DPO 提出**视觉感知对比偏好生成（VCPG）**，完全基于参考模型自身在**受控视觉干预**下的生成行为构造偏好对，无需任何人类标注或外部模型反馈。

- **Focus-and-Enhance 偏好对**（针对感知瓶颈）：对原始图像进行注意力引导的裁剪，形成增强输入 $I_{\mathrm{aug}}$（原始图 + 显著区域裁剪）；同时擦除该裁剪区域形成退化输入 $I_{\mathrm{deg}}$。让模型分别从 $I_{\mathrm{aug}}$ 和 $I_{\mathrm{deg}}$ 自回归生成赢/输响应，直接制造**视觉信息悬殊**，最大化 $\lVert\Delta(\theta_1)\rVert$（Eq.1）。
- **Visual Robustness 偏好对**（针对视觉鲁棒性）：对图像施加高斯噪声构造退化输入 $I_{\mathrm{noise}}$，诱发幻视应答作为负例；再利用 Contrastive Amplification 解码（Eq.3）从原图生成高视觉忠诚的正例。这一设计使优化压力指向视觉鲁棒性，而非单纯文本偏好。

该范式从根源上解决了离策略数据导致的梯度减弱问题（推理见附录 A.2，VCPG 的梯度更新幅度显著大于 PSC），并使学习信号完全由模型自身的“视觉－回答”因果通路产生（Table 3：在策略 IPS 均值 >16，负样本比率 <10% vs. 离策略 IPS = -58.52），无需外部反馈即可稳定训练。

### 2. 从“文本偏好对齐”到“视觉因果对齐”：校准损失与动态缺陷加权机制

标准 DPO 损失仅鼓励模型在文本层面偏向赢者，未显式约束视觉信号是否真正被使用。P²-DPO 引入两项新损失，将优化信号直接对准**视觉信息依赖度（VID）**，迫使模型在感知处理阶段利用视觉证据。

- **校准损失（Calibration Loss, $\mathcal{L}_{\mathrm{Calib}}$）**：基于 Focus‑and‑Enhance 偏好对，计算“原始+裁剪”增强输入下的赢响应相对退化输入的隐性奖励增益（Eq.5）。该损失本质上等价于最大化赢响应的 VID（$I(Y;F_v|P,\theta)$），迫使模型从增强视觉输入中显著获益，从而确切校准视觉主导参数（Table 4：移除 $\mathcal{L}_{\mathrm{Calib}}$ 在所有基准上导致性能下降）。
- **动态缺陷加权（Dynamic Deficit-Weighting, DDW）**：不同样本的主导缺陷（感知瓶颈 vs. 鲁棒性缺失）程度不一。P²-DPO 提出感知增益比 $r = \mathrm{CLIPScore}(P, I_{\mathrm{crop}})/\mathrm{CLIPScore}(P, I)$，通过 $r$ 值自动判断样本更需要 Focus 还是 Robustness 优化，并动态分配权重 $\alpha$（Eq.8）。这避免了对两种损失的无差别平均，实现了样本级的自适应平衡（Table 4：移除 DDW 同样导致性能衰减）。

### 3. 框架完备性：自我驱动的闭环

上述两方面的创新形成一个**自监督、无外部反馈的闭环**：模型从自身对视觉干预的生成行为中采集偏好数据 → 校准损失强制提高 VID → DDW 自动平衡多缺陷 → 更新后模型再次产出更准确的偏好对。所有对比方法（Ablation study, Table 4）证明任一组件切除都会损害最终结果，尤其 Focus‑and‑Enhance 对和校准损失的去除造成 POPE F1 从 87.42 降至 85.84，AMBER F1R 也明显下滑。在未使用任何人类标注的前提下，P²-DPO 在 AMBER 关系推理上相对 LLaVA‑1.5‑7B 取得 +8.5 F1R 增益，并大幅提升噪声鲁棒性（$\sigma=0.20$ 时 F1 领先 >4 点），直接验证了上述设计对感知处理瓶颈的针对性缓解（Table 1：AFR↑+3.98，Processing Accuracy↑+3.81%；Figure 4：噪声区间优势显著）。



![[assets/figures/papers/iclr26_0016_ekOwxTn65Y_P2-DPO_Grounding_Hallucination_in_Perceptual_Pro/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our proposed P2-DPO framework. The process flows from left to right: (1) Derive Visual Inputs: Based on an initial forward pass to obtain an attention map (A), we create an enhanced input via cropping ( $I _ { \mathrm { a u g } } ) _ { \mathrm { : } }$ , a degraded input via erasure ( $I _ { \mathrm { d e g } } ) _ { \cdot }$ , and a noisy input $\left( I _ { \mathrm { n o i s e } } \right$) , alongside the original image (I). (2) Generate Preference Pairs: The reference model generates two orthogonal preference pairs. (3) P2-DPO Training: Difference losses are dynamically combined

P$^2$-DPO 是一个完全自驱动的直接偏好优化范式，其核心流程由**视觉干预驱动的在线偏好数据生成**与**动态均衡的校准训练**两个阶段构成（框架总览见图 2）。方法不依赖任何外部人工标注，仅利用基础模型自身对同一指令在不同视觉输入下的响应差异来构造训练信号，最终通过强化视觉证据的利用来缓解感知处理层面的幻觉。

### 视觉干预驱动的在线偏好对生成

数据生成流水线以图像-文本指令对 $(I, P)$ 为输入，依次完成以下模块：

1. **注意力引导的提示工程与裁剪（Attention-based Prompt Engineering and Cropping）**  
   使用精心设计的提示 $P_{\text{opt}}$ 让模型前向传播，获取注意力图并定位与指令最相关的视觉区域。随后自适应地裁剪出关键内容图块 $I_{\text{crop}}$，用于后续视觉增强与退化操作。这一步骤利用了模型即使在幻觉时注意力也常落在正确区域的现象（第 4.1.1 节）。

2. **聚焦增强型偏好对生成器（Focus-and-Enhance Preference Pair Generator）**  
   - **获胜响应**：构造增强图像 $I_{\text{aug}}$（原始图像与裁剪块拼接），从中采样得到响应 $y^w$，即“聚焦增强”条件下的输出。  
   - **败选响应**：构造退化图像 $I_{\text{deg}}$（将裁剪区域擦除），从中采样得到响应 $y^l$，即“视觉信息缺失”条件下的输出。  
   该生成器直接针对感知瓶颈——模型看到正确区域却依然幻觉的问题——通过扩大视觉信息差距来提供强优化信号。

3. **视觉鲁棒型偏好对生成器（Visual Robustness Preference Pair Generator）**  
   - **败选响应**：对原始图像施加高斯噪声得到 $I_{\text{noise}}$，采样噪声条件下的输出作为 $y^l$。  
   - **获胜响应**：从原始清晰图像的输出中，经由**对比增强解码（Contrastive Amplification，公式 3）** 精炼生成 $y^w$。该策略增强模型在图像轻微扰动下保持正确回答的能力。

4. **数据质量过滤器（Data Quality Filter）**  
   以困惑度和对数概率边际为标准剔除低质量的偏好对，确保训练样本的可靠性与信号强度。

### 动态均衡的校准训练

训练阶段接收上述两族偏好对（聚焦增强型 $D_{\text{focus}}$ 与视觉鲁棒型 $D_{\text{rob}}$），并联合优化以下目标：

- **聚焦增强 DPO 损失 $\mathcal{L}_{\text{dpo.focus}}$**（公式 4）：标准 DPO 损失，驱使模型偏好增强图像下的正确回答。  
- **视觉鲁棒 DPO 损失 $\mathcal{L}_{\text{dpo,rob}}$**（公式 7）：迫使模型在噪声图像条件下依然输出正确回答。  
- **校准损失 $\mathcal{L}_{\text{Calib}}$**（公式 5）：一个额外的辅助目标，通过最大化获胜响应的**视觉信息依赖（Visual Information Dependency, VID）**，直接由像素级视觉差异驱动因果对齐，扩大对视觉主导参数的优化压力。

三种损失通过**动态赤字加权机制（Dynamic Deficit-Weighting, DDW）** 按样本自适应组合。该机制利用 CLIP 分数计算感知增益比 $r = \frac{\text{CLIPScore}(P, I_{\text{crop}})}{\text{CLIPScore}(P, I)}$，判断当前样本的主要短板是感知瓶颈还是视觉鲁棒性，并据此分配聚焦损失与鲁棒损失的动态权重 $\alpha$（公式 8 之前）。最终统一训练目标为：

$$\mathcal{L}_{\text{total}} = \mathbb{E}\Big[ w_{\text{focus}} \cdot \mathcal{L}_{\text{focus}} + w_{\text{robust}} \cdot \mathcal{L}_{\text{dpo,rob}} \Big],$$

其中 $\mathcal{L}_{\text{focus}} = \mathcal{L}_{\text{dpo.focus}} + \lambda_{\text{calib}} \cdot \mathcal{L}_{\text{Calib}}$（公式 6），$w_{\text{focus}}$ 与 $w_{\text{robust}}$ 由 DDW 动态确定。这种设计使模型能根据具体样本的视觉缺陷类型，自主侧重最相关的优化信号，从而在无须任何人工偏好数据的情况下，显著提升感知处理的准确性和抗干扰能力。



### 模块概述
P$^2$-DPO 围绕“自驱动的视觉感知处理偏好优化”构建，包含五个关键模块：

1. **注意引导的裁剪与增强**  
   使用优化后的提示获取模型的注意力图，自适应裁剪出显著性最强的图像区域；基于此构建增强输入（原图 + 裁剪区域）与退化输入（擦除该区域）。

2. **聚焦增强偏好对生成器**  
   将增强输入作为获胜样本的图像条件，退化输入作为失败样本的条件，直接生成一对聚焦感知质量的偏好数据（$y^w, y^l$）。

3. **视觉鲁棒性偏好对生成器**  
   对原图施加高斯噪声得到噪声图像 $I_{\text{noise}}$ 作为失败信号；利用**对比增强解码**（见式(3)）从纯净图像中生成视觉忠实的获胜回答，从而构建鲁棒性偏好对。

4. **数据质量过滤器**  
   基于困惑度与对数概率差额的阈值筛选，剔除低质量偏好对，保留约95%的样本用于训练。

5. **校准 DPO 训练与动态缺陷加权**  
   联合聚焦增强 DPO 损失、鲁棒性 DPO 损失以及**校准损失**进行优化，并通过**感知增益比**动态分配每样本的损失权重，使模型按需强化视觉依赖。

### 关键公式与变量含义

**理论基础：视觉主导参数的梯度差异**

$$
\Delta(\theta_1) \triangleq \nabla_{\theta_1} \log \pi_{\theta}(y^w \mid I_{\mathrm{orig}}, P) - \nabla_{\theta_1} \log \pi_{\theta}(y^l \mid I_{\mathrm{orig}}, P) \tag{1}
$$

其中 $\theta_1\) 为视觉主导参数，$I_{\mathrm{orig}}$ 为原始图像，$P$ 为文本提示，$y^w, y^l$ 分别为胜、负响应。该梯度差的大小决定了 DPO 对视觉模块的优化强度；P$^2$-DPO 通过构建视觉信息差异极大的偏好对提升 $\|\Delta(\theta_1)\|$。

**视觉信息依赖的 Fisher 度量**

$$
\mathrm{Tr}(F_{\theta_1}) \ \text{tends to increase with} \ \mathbb{E}_{\mathcal{D}}\!\left[ D_{\mathrm{KL}}\!\big(p_{\theta}(F_v \mid y^w, P) \,\|\, p_{\theta}(F_v \mid y^l, P)\big) \right] \tag{2}
$$

参数的有监督 Fisher 信息量随胜/负响应在视觉表征后验上的 KL 散度增长，说明更大的视觉条件差异能提供更强的训练信号。

**对比增强解码（用于生成鲁棒性获胜回答）**

$$
y_t \sim \mathrm{softmax}\!\Big((1+\lambda_{\mathrm{ca}})\cdot \mathrm{logits}_{\mathrm{EP}}(y_t) - \lambda_{\mathrm{ca}}\cdot \mathrm{logits}_{\mathrm{AT}}(y_t)\Big), \quad y_t \in \mathcal{V}_{\mathrm{head}}(y_{<t}) \tag{3}
$$

其中 $\lambda_{\mathrm{ca}}$ 为增强系数，$\mathrm{logits}_{\mathrm{EP}}$、$\mathrm{logits}_{\mathrm{AT}}$ 分别表示“专家”与“业余” logits；$\mathcal{V}_{\mathrm{head}}(y_{<t})$ 为候选 token 集合。该策略抑制业余模式，促使模型生成更忠于视觉的文本。

**聚焦增强 DPO 损失**

$$
\mathcal{L}_{\mathrm{dpo.focus}} = -\mathbb{E}_{(y^w, y^l)\sim D_{\mathrm{focus}}}\!\left[ \log \sigma\!\left( \beta \log \frac{\pi_{\theta}(y^w|I,P)}{\pi_{\mathrm{ref}}(y^w|I,P)} - \beta \log \frac{\pi_{\theta}(y^l|I,P)}{\pi_{\mathrm{ref}}(y^l|I,P)} \right) \right] \tag{4}
$$

$D_{\mathrm{focus}}$ 为聚焦增强偏好数据集；$\beta$ 控制偏好强度；$\pi_{\theta}$ 为当前策略，$\pi_{\mathrm{ref}}$ 为参考策略。该损失教导模型在标准图像条件下更倾向增强视觉上下文下的回答。

**校准损失（最大化视觉信息依赖）**

$$
\mathcal{L}_{\mathrm{Calib}} = -\mathbb{E}_{(y^w, y^l)\sim D_{\mathrm{focus}}}\!\left[ \log \sigma\!\left( \beta \log \frac{\pi_{\theta}(y^w|I, I_{\mathrm{crop}}, P)}{\pi_{\theta}(y^w|I_{\mathrm{deg}}, P)} - \beta \log \frac{\pi_{\mathrm{ref}}(y^l|I, I_{\mathrm{crop}}, P)}{\pi_{\mathrm{ref}}(y^l|I_{\mathrm{deg}}, P)} \right) \right] \tag{5}
$$

其中 $I_{\mathrm{crop}}$ 为裁剪出的关键区域，$I_{\mathrm{deg}}$ 为擦除该区域后的退化图像。该损失显式地提升获胜回答在增强输入相对于退化输入下的对数概率比，从而增大其**视觉信息依赖度**（VID）。

**感知瓶颈联合损失**

$$
\mathcal{L}_{\mathrm{focus}} = \mathcal{L}_{\mathrm{dpo.focus}} + \lambda_{\mathrm{calib}} \cdot \mathcal{L}_{\mathrm{Calib}} \tag{6}
$$

$\lambda_{\mathrm{calib}}$ 平衡普通 DPO 与校准损失，共同缓解感知瓶颈。

**视觉鲁棒性 DPO 损失**

$$
\mathcal{L}_{\mathrm{dpo,rob}} = -\mathbb{E}_{(y^w, y^l)\sim D_{\mathrm{rob}}}\!\left[ \log \sigma\!\left( \beta \log \frac{\pi_{\theta}(y^w|I_{\mathrm{noise}}, P)}{\pi_{\mathrm{ref}}(y^w|I_{\mathrm{noise}}, P)} - \beta \log \frac{\pi_{\theta}(y^l|I_{\mathrm{noise}}, P)}{\pi_{\mathrm{ref}}(y^l|I_{\mathrm{noise}}, P)} \right) \right] \tag{7}
$$

$D_{\mathrm{rob}}$ 为鲁棒性偏好数据集；$I_{\mathrm{noise}}$ 为添加高斯噪声的图像。该损失使模型在噪声条件下依然倾向输出正确回答。

**动态缺陷加权机制**

$$
r = \frac{\mathrm{CLIPScore}(P, I_{\mathrm{crop}})}{\mathrm{CLIPScore}(P, I)}, \quad
\alpha = \alpha_{\max} \cdot \tanh\!\left(\frac{r - 1.0}{\tau}\right) \tag{8}
$$

$r$ 为裁剪区域与完整图像的 CLIP 匹配分数之比，反映聚焦增强带来的感知增益；$\alpha_{\max}$、$\tau$ 为超参数。$r>1$ 时说明裁剪区域更贴合语义，此时应加强聚焦损失的权重；反之则侧重鲁棒性训练。

**总优化目标**

$$
\mathcal{L}_{\mathrm{total}} = \mathbb{E}\Big[ w_{\mathrm{focus}} \cdot \mathcal{L}_{\mathrm{focus}} + w_{\mathrm{robust}} \cdot \mathcal{L}_{\mathrm{dpo,rob}} \Big] \tag{9}
$$

其中 $w_{\mathrm{focus}} = \alpha$，$w_{\mathrm{robust}} = 1 - \alpha$，通过式(8)的动态因子为每个样本自适应分配聚焦与鲁棒性的训练强度，使模型按当前视觉缺陷程度进行针对性学习。



## 实验与关键发现

### 实验设置与公平性说明
所有实验均以 LLaVA-1.5‑7B 与 Qwen2.5‑VL 系列作为基础模型，使用统一的 RLHF‑V 场景提示，不引入任何人工反馈或额外标注。对比方法（VCD、HA‑DPO、DPO_RLHF‑V、V‑DPO_RLHF‑V）与 P²‑DPO 共享相同的 LoRA 微调配置（秩、学习率）和 DPO 超参（β 值），评测严格遵循各基准官方协议。P²‑DPO 完全由模型自身生成的偏好对驱动，而基线 DPO_RLHF‑V 与 V‑DPO_RLHF‑V 依赖于 RLHF‑V 中的人类偏好数据，这种设定突出了 P²‑DPO 在自主性与标注效率上的优势。

### 在策略数据的梯度优势验证
Table 3 的内隐偏好得分（IPS）分析揭示了离策略与在策略数据之间的根本差异：RLHF‑V 的离策略偏好对平均 IPS 高达 −58.52，且 68.3% 样本为负值，根据式 (12) 的梯度形式，这将导致视觉‑支配参数的更新量趋于零，训练信号近乎消失。相反，P²‑DPO 的 Focus‑and‑Enhance 与 Visual‑Robustness 数据均维持正的 IPS 均值（5.60 与 4.82）且标准差较小，为 DPO 提供了稳定、有效的梯度流。这一结果为 P²‑DPO 放弃离策略人类反馈、转向在策略视觉干预的决策提供了量化支撑。

![[assets/figures/papers/iclr26_0016_ekOwxTn65Y_P2-DPO_Grounding_Hallucination_in_Perceptual_Pro/figures/007_Table_3.jpg]]
*Table 3: IPS analysis reveals a severe policy gap in off-policy data, contrasted with the strong alignment of our on-policy methods*

### 主结果

#### 感知瓶颈的定量缓解
Table 1 直接度量了感知处理瓶颈的改善。P²‑DPO 将注意力聚焦比（AFR）从基线的 14.73 提升至 18.71（+3.98），处理精度（P‑Acc.）由 66.29% 提升至 70.10%（+3.81%）。这表明模型不再只是“看着”正确区域，而是能够有效利用捕获的视觉证据回答问题，体现了 VCPG 与校准损失在纠正感知‑‑‑推理断层上的协同效应。相比之下，基于人类反馈的 DPO_RLHF 不仅 AFR 提升微弱（+0.84），处理精度反而下降 0.45%，进一步印证离策略、无视感偏好的对齐无法修复此类缺陷。

![[assets/figures/papers/iclr26_0016_ekOwxTn65Y_P2-DPO_Grounding_Hallucination_in_Perceptual_Pro/figures/003_Table_1.jpg]]

#### 视觉鲁棒性的显著增强
Figure 4 的 POPE 评测显示，随高斯噪声强度（σ）增大，P²‑DPO 的 F1 分数始终高于基线，在 σ=0.20 时领先超过 4 个点。这源于 Visual‑Robustness 偏好对：通过噪音‑‑‑增强的对比学习，模型学会了在图像质量退化时依旧依赖视觉证据。Figure 3 的定性示例也佐证了该方法在人类难以察觉的模糊条件下仍能输出正确回答。

![[assets/figures/papers/iclr26_0016_ekOwxTn65Y_P2-DPO_Grounding_Hallucination_in_Perceptual_Pro/figures/005_Figure_4.jpg]]
*Figure 4: Model accuracy on the POPE benchmark under increasing levels of Gaussian noise (σ)*

#### 幻觉基准全面领先
Table 2 汇总了多模型、多基准对比。在 LLaVA‑1.5‑7B 上，P²‑DPO 将 AMBER 的关系推理 F1R 从 77.9 提升至 80.9（+3.0），在 Qwen2.5‑VL‑3B 上则取得 +8.5 的巨大增益；MMHal‑Bench 的幻觉率降低 3.13%，在 Qwen2.5‑VL‑3B 上同样表现优异。重要的是，P²‑DPO 在所有指标上均优于训练式基线 HA‑DPO 和训练‑‑‑解码式 VCD，并且超越了使用人类标注训练的 V‑DPO_RLHF‑V。这些收益完全来自自生成的在策略数据，证明了视觉‑‑‑感知偏好的学习机制具有本质优势。

![[assets/figures/papers/iclr26_0016_ekOwxTn65Y_P2-DPO_Grounding_Hallucination_in_Perceptual_Pro/figures/006_Table_2.jpg]]
*Table 2: Evaluation of P2-DPO against prominent alignment methods on core hallucination benchmarks. Baselines include the training-free VCD (Leng et al., 2024), the AI-feedback-driven HA-DPO (Zhao et al., 2023c), and methods trained on human preferences (DPORLHF-V, V-DPORLHF-V) from the RLHF-V dataset (Yu et al., 2024b). Our method, using only self-generated data, achieves highly competitive or superior results. Arrows show deltas vs. the corresponding Base in each block: green = improvement, red = degradation; for ↓ metrics (MMHal Hal, AMBER CHAIRi/Hal), smaller is better so green arrows point downward*

### 消融研究
Table 4 系统拆解了四个核心组件的作用，移除任一组件均导致一致性的性能退化：
- **去除 Focus‑and‑Enhance 对（W/o FEPs）**：POPE F1 从 87.42 降至 85.84，同时 AMBER 与 HallusionBench 下降，说明“增强‑‑‑擦除”的视觉对比是引导模型聚焦关键区域的关键信号。
- **去除 Visual‑Robustness 对（W/o VRPs）**：所有基准性能普遍回退，验证了噪音‑‑‑增强的偏好学习对强化视觉不变性不可或缺。
- **去除校准损失（W/o L_calib）**：多个维度全面下降，证实式 (5) 通过最大化偏好响应的视觉信息依赖（VID）引入的因果对齐信号有效促进了视觉‑‑‑推理耦合。
- **去除动态赤字加权（W/o DDW）**：性能同样受损，表明依据感知增益比（r）动态平衡 Focus‑and‑Enhance 与 Visual‑Robustness 损失可以防止某一类视觉缺陷被过度偏重，对整个框架的稳定性至关重要。

![[assets/figures/papers/iclr26_0016_ekOwxTn65Y_P2-DPO_Grounding_Hallucination_in_Perceptual_Pro/figures/008_Table_4.jpg]]
*Table 4: Ablation study of our method’s components. We report performance on key hallucination and reasoning benchmarks. Each component contributes positively to the final performance*

### 失败模式与局限分析
本工作未系统记录失败案例，但消融实验可间接反映模型的脆弱性边界。当移除 Visual‑Robustness 对时，模型在噪声下的优势消失，暗示其鲁棒性主要适配于训练中使用的噪声分布，对更强或新型扰动可能泛化不足。从 Table 2 可以看出，尽管 AMBER 关系推理增幅突出，POPE 等基准的绝对分数仍有提升空间，尤其在涉及细粒度视觉‑‑‑语言推理的 HallusionBench 上，增益幅度相对温和。以上观察提示 P²‑DPO 在面向更复杂、开域的视觉缺陷时仍需进一步拓展，相关失败边界的正式标定有待后续工作验证。



## 定位与知识库关联

### 1. 与主流幻觉缓解路线的差异定位

P²‑DPO 在现有幻觉缓解方法的谱系中占据一个独特位置：**它是首个将偏好优化（DPO）重新构造成“视觉自监督对比学习”的工作，不依赖任何外部人类或 AI 反馈，即 on‑policy、vision‑aware 且完全自驱动**。这一性质使其与三类代表性 baseline 形成根本性区别。

- **相对于训练无关的解码方法（VCD）**，
  VCD 通过对比专家‑业余 logits 在推理时减少幻觉，不改变模型参数；而 P²‑DPO 直接对视觉主导参数施加结构化梯度信号，将抗幻觉能力注入模型权重（参见附录 A 对 θ₁ 参数更新的梯度差异分析）。因此 P²‑DPO 的增益是全身性的：它不仅在噪声条件下持续优于推理时纠正方法（Figure 4 在 σ=0.20 时 F1 领先＞4 点），还在正常基准上系统性提升（Table 2，AMBER F1R 提升 +8.5）。

- **相对于基于人类偏好的 DPO 方法（DPO_RLHF‑V、V‑DPO_RLHF‑V）**，
  P²‑DPO 的根本断裂在于**偏好数据的政策空间（policy space）**。
  这些 baseline 使用 RLHF‑V 的 off‑policy 人类偏好对，其训练样本与当前模型分布严重错位：Table 3 显示 off‑policy 数据的平均 Implicit Policy Score（IPS）为 −58.52，且 68.3% 的样本具有负 IPS，导致 DPO 梯度信号极度稀疏且容易消失（Section 3.2 证明 off‑policy 奖励发散使梯度趋于零）。相反，P²‑DPO 的 on‑policy 生成对（Focus‑and‑Enhance 与 Visual Robustness）均保持正且低方差的 IPS，提供稳定的学习信号。
  这种数据政策差异直接转化为对视觉主导参数 θ₁ 的有效优化：VCPG（视觉干预对比生成）制造的视觉信息差异 **I⁺ 与 I⁻** 通过 KL 散度增大 Fisher 信息迹（式(2)），使得 ‖Δ(θ₁)‖ 远超基于纯文本编辑的 PSC 策略所能达到的水平（附录 A.2，式(18) vs. (20)）。

- **相对于 AI 反馈驱动的 DPO（HA‑DPO）**，
  HA‑DPO 利用合成反馈构造偏好对，但偏好信号依然源自语言模型的外部修正，非视觉驱动。P²‑DPO 则完全抛弃这一外在性：它直接通过对同一图像的物理性操作（裁剪增强 vs. 擦除退化、干净 vs. 噪声注入）让模型从自身对视觉条件变化的回应当中学习，因此无需承受外部标注的成本、偏见或政策错位。

从知识库角度，P²‑DPO 将一个之前未被充分利用的因果把手——“视觉输入信号的直接控制”——引入偏好优化框架，从而定义了一个新的范式：**通过设计“视觉证据依赖性”的差异来间接控制模型的输出质量，而非直接标注结果好坏**。

### 2. 适用边界与前提条件

P²‑DPO 的设计强烈依赖于一个经验事实：**LVLM 的注意力机制即使在产生幻觉时也能正确定位关键区域**（Section 4.1.1 的动机，Figure 1 左）。因此，该方法的有效域可界定如下。

- **注意力定位的准确性是 Focus‑and‑Enhance 分支的必需前提**。
  如果 base model 在某些样本上的注意力完全偏移到无关区域，注意力引导的裁剪将引入错误的视觉增强，从而可能使 Focus‑and‑Enhance 对成为“噪声标签”——增强的视觉信号反而奖励错误焦点。论文通过 attention‑based prompt engineering 提升注意力聚焦率（AFR，Table 1），并在附件中验证了注意力裁剪优于逆向裁剪（Table 6），这表明该方法通过在数据生成阶段主动筛选高 AFR 样本来部分规避该风险，但并未证明它可以纠正 attention 完全失效的场景。因此，在 base model 视觉定位极差的案例中，提升幅度预计有限。

- **视觉鲁棒性分支的泛化范围受限于训练噪声模式**。
  Visual Robustness 使用高斯噪声构造偏好对，训练使模型在有噪声时仍输出正确文本。从 Figure 4 来看，该策略对高斯噪声有极强抵抗能力，对运动模糊也显示出定性改善（Figure 7）。然而，这种噪声特异性的训练本质上是一种 Data Augmentation 的偏好化扩展：它使模型学习依赖视觉特征中经得起高斯噪声的部分，但不保证对 JPEG 压缩、遮挡、光照变化等未知退化类型的同等鲁棒性。由于未对不同噪声类型进行消融，其泛化边界尚待实证。

- **动态赤字加权（DDW）的有效性依赖于 CLIP 评分作为“知觉增益”代理的合理性**。
  DDW 用 CLIPScore 比值 r =  CLIPScore( I_crop, P ) / CLIPScore( P, I ) 来分配两个分支的权重：r > 1 表示裁剪区域信息更丰富，模型应采用 Focus‑and‑Enhance；反之优先 Robustness。CLIP 主要捕捉全局语义一致性，可能无法准确反映细粒度推理、计数或空间关系方面的视觉证据增益。因此，在需要精确空间定位或长推理链的任务中，DDW 的调节策略可能不如感知指标所暗示的那样有效。Table 4 虽显示去掉 DDW 会降低性能，但这个下降未必均匀分布；可能存在特定子任务上 DDW 反而引入偏差。

- **计算开销与数据依赖性**。
  偏好对生成需要一次前向传播获取注意力图、执行裁剪/噪声处理、以及对比放大解码（式(3)），这带来了额外的训练前准备成本。训练时，三组损失（式(6)、式(7)、式(8)）需要多次前向传播以计算校准损失中的条件概率。这些开销在计算受限的场景下可能成为实用瓶颈，尽管在论文的训练设置下 5 733 对原始数据即已足够（被过滤至约 5 400 对）。

### 3. 已知局限与待验证开放性

论文自身未显式列出方法局限，以下局限从实验证据与设计选择的缝隙中导出，需未来工作确认。

**已知或可推定的局限**：

1. **仅处理“知觉处理”类幻觉，不解决“感知”类失败**。该方法的目标瓶颈是“模型看见却仍输出错误答案”（Perceptual Bottleneck），即视觉证据已进入表征但未有效利用。若视觉编码器根本未能捕获正确信息（感知失败），通过注意力裁剪增加视觉刺激本身无法提供正确证据，反而可能加剧幻觉。论文通过 TextVQA 的 AFR 与 Processing Accuracy 指标验证了知觉处理瓶颈的缓解，但未报告在感知失败样本上的表现，也未给出感知失败样本的比例。

2. **依赖手工设计的视觉操作空间**。偏好对的质量受限于所选视觉干预（裁剪放大 vs. 擦除、高斯噪声）。这些操作无法覆盖所有现实世界的视觉退化类型，且不会为“物体计数错误”或“空间关系混淆”提供有针对性的校正信号。因此，对于这些特定错误类型，该方法可能存在改进天花板。

3. **奖励函数缺乏物理可解释性**。校准损失（Eq. 5）通过最大化 winning response 在有/无裁剪下的概率比来提升 VID，但这与真实世界视觉推理的因果关系仅存在统计关联，并非明确的结构因果模型。当模型学习利用捷径特征（如裁剪区域的简单纹理）满足这一目标时，可能产生新的隐式偏差，但这些偏差尚未被系统地探测。

**关键开放问题**：

- **跨模型、跨模态以及多轮对话的泛化**：当前实验限于 LLaVA‑1.5-7B、Qwen2.5‑VL 系列，且均为单轮视觉问答。在视频、多轮交互或结合其它传感器时，如何定义“视觉信息差异”以及如何构造多模态 DPO 对，仍是完全开放的问题。

- **与推理时方法的正交性与组合收益**：VCD 等训练无关方法与 P²‑DPO 是否正交？论文未测试联合使用。从机制上看，P²‑DPO 改变了模型权重，VCD 在推理时修正输出分布，两者可能存在边际增益递减（因目标部分重叠），也可能互补（处理不同的失败模式），但需实验验证。

- **光学上不可察觉的对抗扰动**：训练中使用的是人类可感知的视觉干预。若存在对抗性幻觉触发（如微小注入噪声），训练带来的鲁棒性是否能够泛化仍不清楚。由于未进行对抗评估，不宜断言其具有普遍鲁棒性。

- **训练效率优化**：偏好对的生成与多损失联合训练均有优化空间（如共享前向传播、异步数据生成）。若不能达到合理的训练吞吐量，该方法在超大规模模型上的部署将受限。

综上，P²‑DPO 在 on‑policy 视觉自对齐这一新轴线上建立了明显的先手优势，但它仍处于该方法谱系的早期阶段：它对注意力质量的依赖、对视觉干预类型的选择、以及对校准信号的启发式定义，意味着该路线依然存在大量未被探索的优化空间与潜在失效模式。后续工作若能将此范式扩展至更广泛的视觉推理任务与更丰富的视觉干预空间，并建立可解释的因果关系保证，将有望实质性地将 LVLM 幻觉问题推入可控区间。



## 原文 PDF

![[paperPDFs/ICLR_2026/P2_DPO_Grounding_Hallucination_in_Perceptual_Processing_via_Calibration_Direct_Preference_Optimization.pdf]]
