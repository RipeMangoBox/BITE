---
title: "The Geometry of Robustness: Optimizing Loss Landscape Curvature and Feature Manifold Alignment for Robust Finetuning of Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/The_Geometry_of_Robustness_Optimizing_Loss_Landscape_Curvature_and_Feature_Manifold_Alignment_for_Robust_Finetuning_of_Vision_Language_Models.pdf
project_link: null
code_link: "https://huggingface.co/openai/clip-vit-basepatch32"
aliases:
- GROLLCFMARF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过层自适应低秩对抗权重扰动（LAR-AWP）平坦化损失景观曲率，并利用Gram-体积对齐损失强制特征表示在干净、对抗及权重扰动下保持稳定，从几何层面同时控制参数空间尖锐度和特征空间域差异。
primary_logic: 鲁棒性权衡源于两个相互耦合的几何失败——参数空间尖锐各向异性极小值与特征流形不稳定——而联合正则化曲率与特征不变性可以打破这一三元悖论。
claims:
- "GRACE维持了最高的特征空间对齐（ID→OOD: 0.89, ID→Adv: 0.85）且局部流形维度增量最小（ΔLID≤2.5），证实特征流形在分布偏移下保持稳定。"
- GRACE收敛到最平坦的解（Hessian top eigenvalue 1.6e4, 归一化Frobenius范数 0.43e2），显著低于FT和WiSE-FT，证明了曲率正则化的有效性。
- GRACE在ImageNet上同时实现了74.21% ID精度和25.44% 对抗精度，OOD平均精度54.41%与零样本基线持平，超越了所有对抗训练方法并逼近泛化保留方法。
- 消融实验表明，LAR-AWP单独使对抗鲁棒性提升8.6%，GV损失使OOD泛化提升1.5%，二者联合及秩自适应达到最佳综合性能。
---

# The Geometry of Robustness: Optimizing Loss Landscape Curvature and Feature Manifold Alignment for Robust Finetuning of Vision-Language Models

> [!tip] 核心洞察
> 鲁棒性权衡源于两个相互耦合的几何失败——参数空间尖锐各向异性极小值与特征流形不稳定——而联合正则化曲率与特征不变性可以打破这一三元悖论。

| 字段      | 内容                                                                                                                                                    |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | 鲁棒性的几何：优化损失景观曲率与特征流形对齐以实现视觉语言模型的鲁棒微调                                                                                                                  |
| 英文题名    | The Geometry of Robustness: Optimizing Loss Landscape Curvature and Feature Manifold Alignment for Robust Finetuning of Vision-Language Models        |
| 会议/期刊   | CVPR 2026                                                                                                                                             |
| Links   | [paper](https://arxiv.org/abs/2603.27139) · [HuggingFace](https://huggingface.co/openai/clip-vit-basepatch32)    |
| Topic   | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method  | GRACE                                                                                                                                                 |
| Dataset | ImageNet-1K, OOD Average, Zero-Shot Average, Harmonic Mean of ID/OOD/Adv                                                                              |

> [!tip] 效果简介
> - ImageNet-1K (ID Clean) 上，Top-1 Accuracy (%) 74.21 vs 63.35 (CLIP zero-shot) (+10.86)。
> - ImageNet-1K (Adversarial, AutoAttack APGD-CE ε=4/255) 上，Top-1 Accuracy (%) 25.44 vs 0.00 (CLIP zero-shot / Vanilla FT / WiSE-FT) (+25.44)。
> - OOD Average (ImageNet-V2/S/R) 上，Top-1 Accuracy (%) 54.41 vs 55.58 (CLIP zero-shot) (-1.17)。

## 概述

视觉-语言模型（VLM）在微调后面临一个根本性的三元困境：提升分布内（ID）精度往往以牺牲分布外（OOD）泛化或对抗鲁棒性为代价，现有方法最多只能同时优化其中两项。**GRACE**（Gram-aligned Robustness via Adaptive Curvature Estimation）从几何视角揭示了这一权衡的本质——它源于两个相互耦合的几何失败：参数空间中的尖锐、各向异性极小值，以及特征流形在分布偏移下的不稳定变形。

GRACE的核心思想是通过**联合正则化损失景观曲率与特征流形对齐**来打破这一三元悖论。具体而言，它引入两个关键机制：（1）**层自适应低秩对抗权重扰动（LAR-AWP）**，根据每层局部曲率动态分配低秩扰动，将优化引向更平坦的参数区域；（2）**Gram-体积对齐损失**，强制干净样本、对抗样本与权重扰动下的特征表示在Gram矩阵张成的体积上保持一致，从而稳定特征流形。理论分析（Robust PAC-Bayes上界）表明，鲁棒微调需要同时控制邻近性、参数空间尖锐度和特征域差异三项——这正是GRACE的设计依据。

在ImageNet-1K上，GRACE（基于CLIP ViT-B/32）同时实现了**74.21%的ID精度**和**25.44%的对抗精度（AutoAttack）**，OOD平均精度**54.41%**与零样本基线基本持平，调和均值达39.69，显著优于现有对抗训练和泛化保留方法。消融实验证实，LAR-AWP单独使对抗鲁棒性提升约8.6个百分点，Gram-体积损失使OOD泛化提升约1.5个百分点，二者联合及曲率驱动的秩自适应策略实现了最佳综合性能。

## 背景与动机

### VLM鲁棒性的三元悖论

视觉-语言基础模型（如CLIP）在零样本泛化上展现出强大能力，但将其微调至下游任务时面临一个根本性困境：**分布内（ID）精度、分布外（OOD）泛化与对抗鲁棒性三者难以兼得**。如Figure 1所示，现有鲁棒微调策略最多只能同时解决其中两个维度——泛化保留方法（如**WiSE-FT**、**FLYP**）维持了OOD性能却丧失了对抗鲁棒性（对抗精度降至0%），而对抗训练方法（如**TeCoA**、**FARE**）提升了对抗鲁棒性却以牺牲OOD泛化为代价。

这一三元权衡的核心在于两个相互耦合的几何失败：

1. **参数空间尖锐性**：微调后的模型收敛到尖锐、各向异性的极小值，Hessian矩阵的top特征值高达$1.6\times10^4$量级（Table 3），对权重扰动极度敏感；
2. **特征流形不稳定性**：在分布偏移下，类条件特征表示发生显著变形——ID到OOD的类中心余弦相似度下降，局部内在维度（LID）增量超过可接受范围（Table 2），表明特征流形在域间无法保持稳定。

### 现有方法的优化缺口

Table 1对现有鲁棒微调方法按优化目标进行了分解，揭示了系统性缺口：

- **邻近性约束**（Proximity）：LoRA、WiSE-FT等方法通过限制参数偏离预训练权重来保护零样本先验，但无法控制极小值的尖锐度；
- **尖锐度正则化**（Sharpness）：SAM及其变体通过扰动权重寻找平坦区域，但忽略了特征空间的域不变性；
- **特征稳定性**（Stability）：对抗训练或域对齐方法增强特征鲁棒性，但往往破坏了参数空间的平坦性。

**没有任何现有方法同时显式优化这三个目标**。这种割裂导致了鲁棒PAC-Bayes上界（Theorem 3.1）中各项的失衡：

$$R_{\mathrm{Rob}}(\theta) \le \hat{R}_{\mathrm{ID}}(\theta) + \underbrace{\frac{\|\theta-\theta_0\|^2}{2n\sigma^2}}_{\text{邻近性}} + \underbrace{\frac{\sigma^2}{2}\mathrm{Tr}(\mathbb{E}[\nabla^2_\theta R_{\mathrm{Rob}}])}_{\text{参数尖锐度}} + \underbrace{\max_{s\neq t} d_{\mathcal{H}\Delta\mathcal{H}}(\mathcal{D}_s,\mathcal{D}_t)}_{\text{域差异}} + \lambda^*$$

该上界显式表明：仅控制邻近性或尖锐度无法收紧整个界，域差异项$d_{\mathcal{H}\Delta\mathcal{H}}$必须在特征层面被约束。Lemma 3.2进一步将域差异上界分解为类条件均值与协方差的函数，为特征空间对齐提供了可操作的几何可观测量。

### 本文动机与设计思路

基于上述分析，本文的核心洞察是：**鲁棒性权衡源于参数空间尖锐各向异性极小值与特征流形不稳定这两个相互耦合的几何失败，而联合正则化曲率与特征不变性可以打破这一三元悖论**。

为此，GRACE框架从两个几何维度同时介入：

- **参数空间**：通过层自适应低秩对抗权重扰动（LAR-AWP），根据每层局部曲率动态分配扰动秩，将优化偏向平坦区域；
- **特征空间**：通过Gram-体积对齐损失，强制干净、对抗及AWP扰动下的特征三元组保持一致的几何结构，稳定特征流形。

这种双几何正则化策略直接对应PAC-Bayes上界中的尖锐度项和域差异项，从理论上为同时提升ID-OOD-Adversarial三维性能提供了统一框架。

## 核心创新

GRACE的核心创新在于**从几何视角同时操控参数空间的曲率与特征空间的流形稳定性**，从而突破视觉语言模型（VLM）微调中长期存在的ID-OOD-Adversarial三元权衡。现有方法之所以失败，根源在于两个相互耦合的几何失败：参数空间中的尖锐、各向异性极小值，以及特征流形在分布偏移下的不稳定变形。GRACE通过三个紧密协作的模块化创新，将这两个几何失败转化为可联合正则化的目标。

### 创新一：层自适应低秩对抗权重扰动（LAR-AWP）

传统对抗训练或权重扰动方法在参数空间中施加均匀扰动，忽略了不同层对损失景观曲率的异质性敏感度。GRACE的LAR-AWP机制改变了这一范式：

- **扰动参数化**：在LoRA低秩子空间内注入对抗权重扰动，将权重参数化为 $W_{\mathrm{pert}}(\theta,\Delta) = W(\theta_0) + B_W A_W + B_{\mathrm{AWP}}A_{\mathrm{AWP}}$（Eq. 6）。这意味着扰动被严格约束在与预训练先验一致的子空间内，避免了对预训练知识的灾难性破坏。
- **曲率驱动的秩自适应**：LAR-AWP的核心在于根据每层的局部曲率估计 $h_W \approx n_v g_W \odot g_W$（基于mini-batch梯度的Gauss-Newton矩阵对角无偏估计）动态分配扰动秩。高曲率层（损失景观陡峭处）被分配更高的扰动秩，以集中“平滑”力量；平坦层则分配零秩，避免不必要的扰动。这一机制通过Figure 4中的对角秩掩码实现，形成了训练过程中的曲率引导秩课程。
- **内部最大化逼近平坦区域**：通过 $\mathcal{L}_{\mathrm{LAR-AWP}} \approx \frac{1}{n}\sum_{i=1}^n \max_{\|\delta_i\|\le\epsilon} \mathcal{L}(F_{W_{\mathrm{pert}}}(x_i), y_i)$（Eq. 7）的内部最大化，LAR-AWP将优化过程偏向参数空间中曲率更低的平坦区域。

**证据强度**：Table 3显示，GRACE收敛到Hessian最大特征值仅 $1.6\times10^4$、归一化Frobenius范数 $0.43\times10^2$ 的解，显著低于FT和WiSE-FT，直接证实了曲率正则化的有效性。消融实验（Table 8）进一步表明，单独使用LAR-AWP（无秩自适应）可使对抗鲁棒性提升8.6%，而加入曲率驱动的秩自适应后性能进一步提升。

### 创新二：Gram-体积特征对齐损失（GV Loss）

参数空间的平坦化仅解决了问题的一半——特征空间在分布偏移下的变形仍然会导致OOD泛化退化。GRACE的GV损失通过一个简洁的几何约束来稳定特征流形：

- **三元Gram矩阵构建**：对每个输入样本，GRACE收集干净特征、对抗特征和AWP扰动特征的嵌入向量，构建一个 $3\times3$ 的Gram矩阵 $G_i$（Eq. 8），其元素为三向量之间的内积。
- **体积最小化**：损失函数 $\mathcal{L}_{\mathrm{GV}} = \sqrt{|\det(G_i)|}$（Eq. 9）直接度量三个特征向量张成的平行六面体体积。最小化该体积强制三种特征表示保持高度一致（低体积），同时保持类间分离。
- **与理论分析的呼应**：Lemma 3.2将域差异上界表达为类条件均值与协方差的函数，GV损失正是通过维持跨域特征的一致性来收紧这一上界。

**证据强度**：Table 2的定量分析显示，GRACE维持了最高的特征空间对齐（ID→OOD余弦相似度0.89，ID→Adv 0.85），且局部流形维度增量最小（$\Delta$LID $\le 2.5$）。消融实验（Table 8）证实，单独添加GV损失使OOD平均精度提升约1.5%，而对对抗鲁棒性无负面影响，验证了其在稳定特征流形方面的独立贡献。

### 创新三：曲率-特征的联合正则化框架

GRACE的第三个关键创新在于**将LAR-AWP与GV损失统一在一个理论驱动的框架内**，而非简单叠加。总损失函数 $\mathcal{L}_{\mathrm{GRACE}} = \mathcal{L}_{\mathrm{task}} + \lambda_{\mathrm{LAR}}\mathcal{L}_{\mathrm{LAR-AWP}} + \lambda_{\mathrm{GV}}\mathcal{L}_{\mathrm{GV}}$（Eq. 4）直接对应Robust PAC-Bayes上界（Theorem 3.1）中的三项：邻近性（通过LoRA保持）、参数空间尖锐度（LAR-AWP控制）和域差异（GV损失约束）。

这种联合正则化产生了协同效应：LAR-AWP平坦化参数空间使得特征提取对权重扰动不敏感，而GV损失稳定特征流形使得参数更新方向更稳健，两者相互增强。消融实验（Table 8）明确证实了这一点——完整的GRACE（联合LAR-AWP+GV+秩自适应）在所有指标上取得最佳平均性能，超越了各模块单独使用的效果。

### 与现有方法的本质区别

Table 1的方法分类清晰揭示了GRACE的独特定位：现有方法最多同时覆盖邻近性、尖锐度、特征稳定性中的两项。例如，WiSE-FT通过权重插值保持邻近性但完全忽略尖锐度和特征稳定性，导致对抗精度为0%；TeCoA等对抗训练方法关注尖锐度但缺乏显式的特征流形约束。GRACE是首个同时显式优化这三项的方法，从根本上改变了VLM鲁棒微调的设计范式。

## 整体框架

GRACE 的整体设计源于一个核心洞察：视觉语言模型（VLM）微调中的鲁棒性三元悖论——分布内（ID）精度、分布外（OOD）泛化与对抗鲁棒性难以同时获得——根源于两个相互耦合的几何失败。其一是参数空间中尖锐、各向异性的极小值，使模型对权重扰动高度敏感；其二是特征流形在分布偏移下的不稳定变形，导致干净、对抗和OOD输入的特征表示之间出现显著域差异。现有方法通常仅针对其中一维或两维进行优化（Table 1），无法同时控制参数空间曲率和特征空间对齐。

GRACE 通过一个统一的微调框架联合正则化这两个几何维度，其整体目标函数为：

$$\mathcal{L}_{\mathrm{GRACE}} = \mathcal{L}_{\mathrm{task}} + \lambda_{\mathrm{LAR}}\mathcal{L}_{\mathrm{LAR-AWP}} + \lambda_{\mathrm{GV}}\mathcal{L}_{\mathrm{GV}}$$

其中 $\mathcal{L}_{\mathrm{task}}$ 为标准分类交叉熵损失，$\mathcal{L}_{\mathrm{LAR-AWP}}$ 为层自适应低秩对抗权重扰动损失，$\mathcal{L}_{\mathrm{GV}}$ 为 Gram-体积对齐损失。三个模块协同运作，形成一条完整的训练管线（Figure 3）：

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/007_Figure_3.jpg]]
*Figure 3: Low-rank adaptation and perturbation in GRACE. Frozen pretrained weights*

1. **LoRA 低秩适配**：冻结预训练权重 $W(\theta_0)$，仅训练低秩分解因子 $B_W$ 和 $A_W$，使参数更新 $W(\theta) = W(\theta_0) + B_W A_W$ 保持在预训练先验的邻近区域内。这一设计显式控制 PAC-Bayes 上界中的邻近项 $\|\theta - \theta_0\|^2$，抑制参数漂移对零样本泛化的破坏。

2. **LAR-AWP（层自适应低秩对抗权重扰动）**：在 LoRA 子空间内注入额外的低秩对抗扰动分支 $B_{\mathrm{AWP}}A_{\mathrm{AWP}}$，使扰动后的权重为 $W_{\mathrm{pert}}(\theta,\Delta) = W(\theta_0) + B_W A_W + B_{\mathrm{AWP}}A_{\mathrm{AWP}}$。通过对扰动进行内部最大化 $\max_{\|\delta\|\le\epsilon} \mathcal{L}(F_{W_{\mathrm{pert}}}(x), y)$，优化过程被偏置向更平坦的损失景观区域。关键在于，每层的扰动秩并非固定，而是根据该层的局部曲率估计 $h_W$ 动态分配——曲率越大的层获得越高的扰动秩，平坦层则可分配零秩（Figure 4）。这一曲率驱动的秩自适应策略将有限的计算资源集中于损失景观最陡峭的层，实现高效的平坦化。

3. **Gram-体积对齐损失（GV Loss）**：对每个输入样本，收集其干净特征 $f_{\mathrm{ID}}$、对抗特征 $f_{\mathrm{Adv}}$ 和 LAR-AWP 扰动下的特征 $f_{\mathrm{AWP}}$，构建一个 $3\times 3$ 的 Gram 矩阵 $G_i$，并以其行列式的平方根作为损失：$\mathcal{L}_{\mathrm{GV}} = \sqrt{|\det(G_i)|}$。该损失度量三个特征向量所张成平行六面体的体积——体积越小，表示三种条件下的特征表示越趋于共线，即特征流形在分布偏移下越稳定（Figure 5）。这一设计直接针对 PAC-Bayes 上界中的域差异项 $d_{\mathcal{H}\Delta\mathcal{H}}$，从特征几何层面缩小 ID、OOD 和对抗域之间的鸿沟。

训练过程中，GRACE 在每个 mini-batch 上交替执行以下步骤（Algorithm 1）：(i) 计算干净特征与任务损失；(ii) 生成 PGD 对抗样本；(iii) 基于当前曲率估计执行若干步 LAR-AWP 内部最大化；(iv) 收集干净、对抗和 AWP 扰动下的特征，计算 Gram-体积对齐损失；(v) 将三项损失加权求和，更新 LoRA 参数。这一交替优化机制使得曲率正则化与特征对齐相互促进：更平坦的参数空间降低了对抗样本对特征表示的扰动幅度，而更稳定的特征流形又为曲率估计提供了更可靠的梯度信号。

## 核心模块与公式推导

GRACE 的整体训练目标由三项损失加权组合构成：

$$\mathcal{L}_{\mathrm{GRACE}} = \mathcal{L}_{\mathrm{task}} + \lambda_{\mathrm{LAR}}\mathcal{L}_{\mathrm{LAR-AWP}} + \lambda_{\mathrm{GV}}\mathcal{L}_{\mathrm{GV}}$$

其中 $\mathcal{L}_{\mathrm{task}}$ 为标准分类交叉熵损失，$\mathcal{L}_{\mathrm{LAR-AWP}}$ 为层自适应低秩对抗权重扰动损失，$\mathcal{L}_{\mathrm{GV}}$ 为 Gram-体积对齐损失。该设计直接源于鲁棒 PAC-Bayes 界的分解——定理 3.1 揭示了鲁棒微调需同时控制邻近性项 $\|\theta-\theta_0\|^2$、参数空间尖锐度项 $\mathrm{Tr}(\mathbb{E}[\nabla_\theta^2 R_{\mathrm{Rob}}])$ 和域差异项 $d_{\mathcal{H}\Delta\mathcal{H}}$。GRACE 的三个模块分别对应这三项约束。

### LoRA 低秩适配（邻近性控制）

GRACE 采用 LoRA 参数化以保持与预训练先验的邻近性。对于任一权重矩阵，其更新形式为：

$$W(\theta) = W(\theta_0) + B_W A_W$$

其中 $W(\theta_0)$ 为冻结的预训练权重，$B_W \in \mathbb{R}^{d_{\mathrm{out}} \times r}$ 和 $A_W \in \mathbb{R}^{r \times d_{\mathrm{in}}}$ 为可训练的低秩因子，秩 $r \ll \min(d_{\mathrm{in}}, d_{\mathrm{out}})$。这一约束将参数搜索限制在预训练点附近的低维流形上，直接控制 PAC-Bayes 界中的邻近性项。

### LAR-AWP：层自适应低秩对抗权重扰动（尖锐度正则化）

LAR-AWP 在 LoRA 子空间内注入可学习的对抗权重扰动分支，将参数化扩展为：

$$W_{\mathrm{pert}}(\theta, \Delta) = W(\theta_0) + B_W A_W + B_{\mathrm{AWP}}A_{\mathrm{AWP}}$$

其中 $B_{\mathrm{AWP}}A_{\mathrm{AWP}}$ 为额外添加的低秩扰动项。内部最大化目标为：

$$\mathcal{L}_{\mathrm{LAR-AWP}} \approx \frac{1}{n}\sum_{i=1}^n \max_{\|\delta_i\|\le\epsilon} \mathcal{L}(F_{W_{\mathrm{pert}}}(x_i), y_i)$$

该步骤通过在最差权重扰动方向上最大化损失，将优化引向更平坦的极小值区域。

**曲率驱动的秩自适应**：LAR-AWP 的核心创新在于根据每层的局部曲率动态分配扰动秩。曲率估计使用 mini-batch 梯度的逐元素平方作为 Gauss-Newton 矩阵对角元的无偏估计：

$$h_W \approx n_v \, g_W \odot g_W$$

其中 $g_W$ 为该层权重的 mini-batch 梯度向量，$n_v$ 为梯度估计的方差校正因子。曲率较大的层（损失景观更陡峭）被分配更高的扰动秩，以集中平滑最尖锐的方向；曲率平坦的层则可分配零秩（即不施加扰动）。Figure 4 展示了这一对角秩掩码机制：曲率估计 $h_W$ 经滑动平均和分位数归一化后，映射为各层的有效扰动秩，形成随训练进程演化的秩课程。

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/006_Figure_4.jpg]]
*Figure 4: LAR-AWP rank curriculum. A diagonal rank mask controls the effective perturbation rank per layer. Curvature estimates*

### Gram-体积对齐损失（特征稳定性正则化）

为约束特征流形在分布偏移下的变形，GRACE 对每个样本构建一个 $3 \times 3$ 的 Gram 矩阵，收集干净特征 $f_{\mathrm{ID}}$、对抗特征 $f_{\mathrm{Adv}}$ 和 AWP 扰动特征 $f_{\mathrm{AWP}}$ 的两两内积：

$$G_i = \begin{bmatrix} \langle f_{\mathrm{ID}}, f_{\mathrm{ID}}\rangle & \langle f_{\mathrm{ID}}, f_{\mathrm{Adv}}\rangle & \langle f_{\mathrm{ID}}, f_{\mathrm{AWP}}\rangle \\ \langle f_{\mathrm{Adv}}, f_{\mathrm{ID}}\rangle & \langle f_{\mathrm{Adv}}, f_{\mathrm{Adv}}\rangle & \langle f_{\mathrm{Adv}}, f_{\mathrm{AWP}}\rangle \\ \langle f_{\mathrm{AWP}}, f_{\mathrm{ID}}\rangle & \langle f_{\mathrm{AWP}}, f_{\mathrm{Adv}}\rangle & \langle f_{\mathrm{AWP}}, f_{\mathrm{AWP}}\rangle \end{bmatrix} + \varepsilon I$$

其中 $\varepsilon I$ 为数值稳定性项。Gram-体积损失定义为该矩阵行列式的平方根：

$$\mathcal{L}_{\mathrm{GV}} = \sqrt{|\det(G_i)|}$$

几何上，$\sqrt{|\det(G_i)|}$ 度量了三个特征向量张成的平行六面体体积。当三个向量高度共线时体积趋近于零，表示干净、对抗和 AWP 扰动下的特征表示高度一致。该损失直接针对引理 3.2 的结论——域差异 $d_{\mathcal{H}\Delta\mathcal{H}}$ 可由类条件特征均值与协方差的差异上界控制，因此最小化特征体积等价于收紧域差异上界。

### 训练流程

GRACE 在每个 mini-batch 上交替执行以下步骤（Algorithm 1）：
1. 计算干净特征与任务损失 $\mathcal{L}_{\mathrm{task}}$；
2. 通过 PGD 生成对抗样本；
3. 执行少量内部步的 LAR-AWP 低秩权重扰动，基于曲率秩课程；
4. 计算 Gram-体积对齐损失 $\mathcal{L}_{\mathrm{GV}}$；
5. 聚合总损失并更新 LoRA 参数。

消融实验（Table 8）验证了各模块的独立贡献与协同效应：单独添加 GV 损失使 OOD 平均精度提升约 1.5% 而对抗鲁棒性基本不变；单独使用无秩自适应的 LAR-AWP 使对抗精度提升 8.6% 但 OOD 略降；完整的 GRACE（联合 LAR-AWP + GV + 秩自适应）在所有指标上取得最佳平均性能。

### 补充图表

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/008_Figure_5.jpg]]
*Figure 5: Gram-volume feature alignment. For each input, GRACE compares clean, adversarial, and LAR-AWP-perturbed image embeddings via a small Gram matrix. The Gram-volume loss encourages these three vectors to remain close to each other (low volume) while preserving separation across different classes*

## 实验与分析

### 5.1 实验设置与对比基线

所有实验基于CLIP ViT-B/32在ImageNet-1K上进行微调，并以零样本CLIP作为预训练先验参照。对比方法覆盖两大范式：**泛化保留微调（S1）** 包括WiSE-FT、FLYP、TPGM、SPD，以及**对抗训练（S2）** 包括TeCoA、FARE、PMG-AFT、LAAT，同时报告标准全参数微调（Vanilla FT）作为下界。公平性保障措施如下：
- 所有PEFT方法统一采用LoRA配置（秩 $r=64$），确保参数效率可比；
- 对抗训练统一使用10步PGD（$\epsilon=4/255$，步长 $1/255$），测试采用AutoAttack（APGD-CE）；
- 零样本评估遵循标准CLIP协议，使用相同的8个数据集和提示模板。

### 5.2 主要结果：ID-OOD-Adversarial 三元权衡的突破

Table 4 和 Table 6 汇总了ViT-B/32在ImageNet-1K上的核心结果。GRACE在三个维度上实现了现有方法无法同时达成的性能：

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/010_Table_4.jpg]]
*Table 4: OOD Results on ImageNet. CLIP ViT-B/32 finetuned on ImageNet [3] dataset and evaluated on ImageNet variants. The numbers are top-1 accuracy (%). OOD Avg averages ImageNet-V2, -S, -R; Nat Adv Avg averages ImageNet-A and A-Plus*

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/011_Table_6.jpg]]
*Table 6: Unified summary across settings (ViT-B/32). CLIP ViT-B/32 fine-tuned on ImageNet-1K and evaluated across ID, OOD, PGD adversarial (AutoAttack/APGD-CE), and natural adversarial (ImageNet-A/A-Plus average)*

**分布内（ID）精度**：GRACE达到74.21% Top-1准确率，较零样本CLIP基线（63.35%）提升10.86个百分点，超越了WiSE-FT等泛化保留方法，证明LoRA低秩适配有效保持了预训练先验的邻近性。

**对抗鲁棒性**：在AutoAttack（APGD-CE, $\epsilon=4/255$）下，GRACE取得25.44%的对抗精度。相比之下，CLIP零样本、Vanilla FT和WiSE-FT的对抗精度均为0.00%，而专门设计的对抗训练方法TeCoA和FARE也仅达到约20%左右。这一25.44%的绝对增益直接源于LAR-AWP对损失景观曲率的平坦化作用。

**分布外（OOD）泛化**：GRACE在ImageNet-V2/S/R上的OOD平均精度为54.41%，与零样本基线（55.58%）仅差1.17个百分点，显著优于Vanilla FT（约45%）和对抗训练方法（通常低于50%）。这表明Gram-体积对齐损失有效抑制了微调过程中的特征流形变形。

**综合度量**：GRACE的ID/OOD/Adv调和均值达到39.69，而零样本CLIP因对抗精度为0导致该度量为0，其他方法均未超过30。在零样本迁移评估（Table 5）中，GRACE在8个数据集上的平均精度为59.61%，与零样本基线（59.31%）持平（+0.30%），进一步验证了其预训练知识保留能力。

### 5.3 几何证据：参数空间平坦化与特征流形稳定

GRACE的性能优势可从两个几何层面获得直接验证。

**参数空间尖锐度**（Table 3）：GRACE收敛到Hessian最大特征值 $\lambda_{\max}=1.6\times10^4$、归一化Frobenius范数 $\|\mathbf{H}\|_F/\sqrt{d}=0.43\times10^2$ 的解，显著低于FT（$\lambda_{\max}=4.2\times10^4$）和WiSE-FT（$\lambda_{\max}=3.1\times10^4$）。这证实了LAR-AWP通过曲率自适应的低秩权重扰动，成功将优化轨迹导向更平坦的极小值区域——这正是Theorem 3.1中参数空间尖锐度项（B项）所要求的。

**特征空间稳定性**（Table 2）：GRACE在ID→OOD类质心余弦相似度上达到0.89，ID→Adv达到0.85，均为所有方法中最高；同时其局部内在维度增量 $\Delta\text{LID}\leq2.5$，远低于FT（$\Delta\text{LID}>8$）和WiSE-FT（$\Delta\text{LID}>5$）。这说明Gram-体积对齐损失通过约束干净、对抗和AWP扰动下特征的三元Gram矩阵体积（Eq. 8-9），有效稳定了特征流形的局部几何结构，直接压制了Lemma 3.2中的域差异上界。

Figure 2 的可视化进一步佐证了这一双几何机制：Figure 2(a)显示FT和WiSE-FT的特征分布在OOD和对抗偏移下发生严重坍缩，而GRACE保持了三者的紧凑对齐；Figure 2(b)的损失景观切片表明GRACE收敛到明显更宽、更平坦的盆地。

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/005_Figure_2.jpg]]
*Figure 2: (a) Feature Distribution Analysis: 3D projection of image features for in-distribution*

### 5.4 消融实验：模块贡献与协同效应

Table 8 的消融实验逐模块分解了GRACE各组件的贡献：

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/014_Table_8.jpg]]
*Table 8: Ablation Study. CLIP ViT-B/32 fine-tuned on ImageNet-1K. Avg is the simple mean of the four columns*

| 配置 | ID精度 | OOD平均 | 对抗精度 | 自然对抗平均 |
|------|---------|---------|-----------|---------------|
| LoRA基线 | 73.85 | 52.90 | 0.00 | 30.15 |
| +GV损失 | 73.92 | 54.40 | 0.00 | 31.20 |
| +LAR-AWP（无秩自适应） | 74.10 | 52.10 | 8.60 | 32.50 |
| +LAR-AWP+秩自适应 | 74.15 | 53.20 | 12.80 | 34.10 |
| **GRACE完整** | **74.21** | **54.41** | **25.44** | **36.85** |

关键发现：
- **Gram-体积对齐损失单独作用**：使OOD平均精度提升约1.5个百分点（52.90→54.40），自然对抗精度提升约1个百分点，但对PGD对抗精度无贡献——这符合预期，因为GV损失仅约束特征空间，不直接参与对抗优化。
- **LAR-AWP单独作用**：使对抗精度从0跃升至8.60%，但OOD精度略有下降（52.90→52.10），表明纯粹的参数空间平坦化可能以牺牲少量分布外泛化为代价。
- **曲率自适应秩分配**：在固定秩LAR-AWP基础上，对抗精度进一步提升至12.80%，OOD精度回升至53.20%，验证了Figure 4中曲率引导的差异化扰动秩策略的有效性——高曲率层获得更高扰动秩以实现针对性平滑，平坦层保持零秩以避免不必要的先验破坏。
- **完整GRACE的协同效应**：联合LAR-AWP+秩自适应+GV损失后，对抗精度跃升至25.44%（远超单独模块的线性叠加），OOD精度恢复至54.41%，证实了参数空间曲率正则化与特征空间对齐之间存在正向协同——平坦的损失景观使特征对齐损失更容易优化，而稳定的特征流形又为对抗扰动提供了更鲁棒的表示基础。

### 5.5 失败模式与局限性分析

尽管GRACE在ViT-B/32上表现优异，论文揭示了若干值得关注的边界条件：

**模型规模的敏感性**：在ViT-B/16上的部分指标略有下降，表明曲率估计的层分辨率与模型结构存在交互——更小的patch size可能改变各层的曲率分布模式，影响LAR-AWP的秩分配策略。Figure 7的层曲率各向异性分析证实，不同CLIP变体（ViT-B/32、ViT-B/16、ViT-L/14）的曲率分布存在显著差异，这要求秩课程机制具备足够的结构适应性。

**计算开销的权衡**：GRACE的训练包含内部LAR-AWP步骤和Gram体积计算，虽然相比现有对抗训练方法实现了1.4×加速（Figure 6），但在资源受限场景下仍显著高于标准LoRA微调。这一开销主要来自：每步需生成PGD对抗样本、执行曲率估计的梯度计算、以及Gram矩阵的行列式求解。

**对抗威胁模型的覆盖范围**：当前评估限于 $\ell_\infty$ PGD和AutoAttack（APGD-CE），对更强的自适应攻击（如联合输入-权重扰动）或 $\ell_2/\ell_1$ 攻击的鲁棒性尚未验证。Table 9揭示了AWP引起的特征空间位移与OOD偏移具有相似量级，这暗示攻击者可能利用AWP机制本身构造更具针对性的对抗策略。

**架构迁移性的未验证**：所有实验基于CLIP视觉编码器，GRACE的几何正则化框架对其他视觉-语言架构（如ALIGN、SigLIP）或纯视觉模型的可迁移性仍是开放问题。

### 5.6 与LoRA基方法的对比

Table 7 将GRACE与其他LoRA基微调方法进行了直接比较。在统一的LoRA秩配置（$r=64$）下，GRACE在ID精度（74.21%）、OOD平均（54.41%）和对抗精度（25.44%）三个维度上均显著优于其他LoRA变体。这验证了GRACE的核心主张：**仅靠参数效率不足以解决鲁棒性权衡，必须显式地在低秩子空间内同时注入曲率感知的对抗扰动和特征对齐约束**。Figure 3示意性地展示了这一设计——冻结的预训练权重（蓝色）仅通过LoRA适配器（橙色）更新，而LAR-AWP在相同子空间内注入额外的低秩扰动分支（红色），实现了参数邻近性与曲率平坦化的解耦控制。

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/012_Table_7.jpg]]
*Table 7: Comparison of GRACE with other LoRA-based finetuning approaches. CLIP ViT-B/32 fine-tuned on ImageNet-1K*

### 补充图表

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/002_Table_1.jpg]]
*Table 1: Decomposition of robust fine-tuning methods by optimization objectives. Methods addressing each term explicitly through their loss function or training procedure are marked*

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/003_Table_2.jpg]]
*Table 2: Class-conditional feature-space stability. Cosine similarity between ID and shifted class centroids (left) and change in LID relative to ID (right). Lower ∆LID implies more stable local manifolds*

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/015_Figure_7.jpg]]
*Figure 7: Layerwise curvature anisotropy in CLIP. Normalized Hutchinson curvature*

![[assets/figures/papers/paper_list_l2243_https_arxiv_org_abs_2603_27139/figures/009_Table_5.jpg]]
*Table 5: Clean and adversarial evaluation on zero-shot image classification datasets (ViT-B/32). Models are trained on ImageNet; all other datasets are zero-shot. ZS Avg is the mean across the 8 datasets*

## 方法谱系与知识库定位

### 1. 与现有鲁棒微调方法的系统关系

GRACE 的核心贡献在于首次将鲁棒微调问题显式地分解为三个可独立优化的几何项——参数邻近性、参数空间尖锐度与特征空间稳定性——并针对后两项设计了专用的正则化机制。这一分解源于 **Theorem 3.1** 中的 Robust PAC-Bayes 上界，该上界将鲁棒风险界定为 ID 经验风险、参数偏移量、Hessian 迹（尖锐度）以及域间 $\mathcal{H}\Delta\mathcal{H}$-散度之和。现有方法至多覆盖其中两项（**Table 1** 给出了系统分类），而 GRACE 是首个同时显式优化全部三项的框架。

**泛化保留微调方法（S1）**——包括 **WiSE-FT**、**FLYP**、**TPGM** 和 **SPD**——通过权重插值、投影或约束来保持与预训练先验的邻近性（项 A），从而有效保留 OOD 泛化能力。然而，这些方法完全忽略了参数空间尖锐度（项 B）和特征空间域差异（项 C），导致对抗鲁棒性为零（见 **Section 4** 中的 Failure Mode 2：WiSE-FT 对抗精度 = 0%）。从几何角度看，它们收敛到损失景观中邻近预训练点但极度尖锐的区域，对权重扰动毫无抵抗力。

**对抗训练方法（S2）**——包括 **TeCoA**、**FARE**、**PMG-AFT** 和 **LAAT**——通过对抗样本训练隐式地降低了参数空间尖锐度（项 B），但缺乏对预训练先验邻近性（项 A）和特征空间域差异（项 C）的显式控制。这解释了它们虽然获得一定对抗鲁棒性，却严重牺牲 OOD 泛化能力的现象（**Table 4** 中 TeCoA 的 OOD 平均精度仅约 50%，远低于零样本基线的 55.58%）。从几何角度看，对抗训练将解推向更平坦区域，但这些区域可能远离预训练先验，且特征流形在分布偏移下仍不稳定。

GRACE 通过三项机制填补了这一空白：
- **LoRA 低秩适配**：保持项 A（邻近性），通过 Equation (5) 将参数更新约束在低秩子空间内，锚定于预训练权重。
- **LAR-AWP（层自适应低秩对抗权重扰动）**：显式优化项 B（尖锐度），通过 Equation (7) 的内部最大化逼近平坦区域，并根据层曲率估计（Equation 中的 $h_W$）自适应分配扰动秩。
- **Gram-体积对齐损失（GV Loss）**：显式优化项 C（特征稳定性），通过 Equation (9) 最小化干净、对抗及 AWP 扰动下特征三元组的 Gram 体积，强制特征流形在分布偏移下保持稳定。

**Table 1** 的分类证实了这一分析：GRACE 是唯一在邻近性、尖锐度和特征稳定性三项上均获得显式优化标记（✓）的方法。

### 2. 与对抗权重扰动（AWP）方法的继承与突破

GRACE 的 LAR-AWP 模块在思想上继承了对抗权重扰动（AWP）的范式，但做出了三项关键改进，使其适配于 VLM 微调场景：

1. **低秩子空间约束**：传统 AWP 在全参数空间施加扰动，对大规模 VLM 而言计算代价极高且易破坏预训练先验。GRACE 将扰动注入 LoRA 的同一低秩子空间（**Figure 3**，Equation (6)：$W_{\mathrm{pert}} = W(\theta_0) + B_W A_W + B_{\mathrm{AWP}}A_{\mathrm{AWP}}$），既保持了邻近性，又大幅降低了计算开销。

2. **层自适应秩分配**：传统 AWP 对所有层施加均匀扰动，忽略了不同层的曲率异质性。**Figure 7** 揭示了 CLIP 各 Transformer 层间存在显著的曲率各向异性（归一化 Hutchinson 曲率 $\kappa_\ell$ 跨层变化可达数倍）。GRACE 利用这一发现，通过 mini-batch 梯度的 Hadamard 积估计 Hessian 对角（$h_W \approx n_v g_W \odot g_W$），为高曲率层分配更高扰动秩，为平坦层分配零秩（**Figure 4** 的对角秩掩码机制），实现了精准的曲率驱动平滑。

3. **与特征对齐的协同**：传统 AWP 仅关注参数空间平坦化，GRACE 将其与 Gram-体积对齐损失联合优化，使权重扰动下的特征表示与干净/对抗特征保持一致（**Figure 5**），从而同时控制参数空间和特征空间的几何性质。

### 3. 与 LoRA 基微调方法的关系

**Table 7** 将 GRACE 与其他 LoRA 基微调方法进行了对比。标准 LoRA 微调仅通过低秩适配保持邻近性，缺乏对尖锐度和特征稳定性的控制，导致对抗鲁棒性为零。GRACE 在 LoRA 基础上叠加了 LAR-AWP 和 GV 损失，在不显著增加可训练参数的前提下（仅添加低秩 AWP 分支）实现了鲁棒性的质变。消融实验（**Table 8**）证实：单独添加 LAR-AWP 使对抗精度提升 8.6%，单独添加 GV 损失使 OOD 平均精度提升约 1.5%，二者联合及秩自适应达到最佳综合性能。

### 4. 适用边界与局限

尽管 GRACE 在 ViT-B/32 上实现了 ID-OOD-Adversarial 三维指标的同步提升（**Table 6**：调和均值 39.69，对比零样本基线的 0.00），其适用边界存在以下约束：

- **架构依赖性**：实验主要基于 CLIP 视觉编码器（ViT-B/32、ViT-B/16、ViT-L/14）。对其他视觉-语言架构（如 ALIGN、SigLIP）或纯语言模型的可迁移性未经严格验证，需要手动确认。
- **模型规模敏感性**：在 ViT-B/16 上部分指标略有下降，表明层曲率估计和秩分配策略对模型结构和规模存在一定敏感性。**Figure 7** 显示不同规模 CLIP 模型的曲率分布模式存在差异，可能需要针对性地调整秩分配的分位数阈值。
- **对抗攻击范围**：对抗评估限于 $\ell_\infty$ 约束下的 PGD 和 AutoAttack（APGD-CE），对更强的自适应攻击（如联合输入-权重扰动攻击）或 $\ell_2/\ell_1$ 攻击的鲁棒性未知。
- **计算开销**：GRACE 虽比现有对抗训练方法快 1.4 倍（**Figure 6** 的 Pareto 曲线），但内部 LAR-AWP 步骤和 Gram 体积计算仍使其开销高于标准 LoRA 微调，在资源受限场景可能构成瓶颈。

### 5. 开放问题

GRACE 的几何正则化框架开辟了若干值得探索的方向：

1. **跨模态与跨架构推广**：Robust PAC-Bayes 上界（Theorem 3.1）和特征空间域差异界（Lemma 3.2）的推导未依赖视觉模态的特殊假设，理论上可推广至 LLM 微调或其他跨模态模型，但需要实验验证。

2. **曲率估计的鲁棒性**：LAR-AWP 的曲率估计依赖于 mini-batch 梯度的滑动平均和分位数阈值（**Figure 4**），这些超参数对不同训练动态（如学习率调度、batch size 变化）的鲁棒性需要系统研究。

3. **特征对齐策略的扩展**：Gram-体积对齐损失约束的是干净/对抗/AWP 三元组的一致性，能否与其他特征对齐策略（如对比损失、互信息最大化）结合以进一步提升 OOD 泛化，是一个开放的设计空间。

4. **真实世界部署的对抗韧性**：在部署场景中，攻击者可能针对 GRACE 的几何特性设计自适应攻击（如同时扰动输入和 LoRA 权重），GRACE 对此类联合攻击的防御能力需要进一步评估。

## 原文 PDF

![[paperPDFs/CVPR_2026/The_Geometry_of_Robustness_Optimizing_Loss_Landscape_Curvature_and_Feature_Manifold_Alignment_for_Robust_Finetuning_of_Vision_Language_Models.pdf]]
