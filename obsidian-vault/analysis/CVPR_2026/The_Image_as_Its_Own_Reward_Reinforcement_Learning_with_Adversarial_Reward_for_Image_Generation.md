---
title: "The Image as Its Own Reward: Reinforcement Learning with Adversarial Reward for Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/The_Image_as_Its_Own_Reward_Reinforcement_Learning_with_Adversarial_Reward_for_Image_Generation.pdf
project_link: "https://showlab.github.io/Adv-GRPO/"
code_link: "https://github.com/discus0434/aesthetic-predictor-v2-5"
aliases:
- IAIORRLARIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将参考图像引入对抗训练以校准奖励模型，并使用视觉基础模型（如DINO）提供密集的视觉信号替代单一标量奖励。
primary_logic: 通过让奖励模型作为鉴别器与生成器对抗训练，并利用视觉基础模型提取全局-局部特征作为奖励，可以有效缓解奖励黑客，并全方位提升图像质量、美学和图文对齐。
claims:
- Our method outperforms Flow-GRPO and SD3, achieving 70.0% and 72.4% win rates in image quality and aesthetics.
- Achieve comparable benchmark scores to Flow-GRPO, PickScore 22.78 vs 22.82, OCR Accuracy 0.91 vs 0.91, indicating adversarial training does not compromise quantitative performance.
- Using visual foundation model (DINO) as reward improves OCR Accuracy from 0.59 to 0.69 and GenEval from 0.61 to 0.69 over SD3.
- Under DINO reward, human evaluation shows 72.4% win rate in aesthetics over SD3.
---

# The Image as Its Own Reward: Reinforcement Learning with Adversarial Reward for Image Generation

> [!tip] 核心洞察
> 通过让奖励模型作为鉴别器与生成器对抗训练，并利用视觉基础模型提取全局-局部特征作为奖励，可以有效缓解奖励黑客，并全方位提升图像质量、美学和图文对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | 图像自身的奖励：基于对抗奖励的图像生成强化学习 |
| 英文题名 | The Image as Its Own Reward: Reinforcement Learning with Adversarial Reward for Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20256) · [Project](https://showlab.github.io/Adv-GRPO/) · [Code](https://github.com/discus0434/aesthetic-predictor-v2-5) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Adv-GRPO |
| Dataset | PickScore prompt dataset, OCR benchmark, General evaluation, Human evaluation |

> [!tip] 效果简介
> - PickScore prompt dataset 上，PickScore 22.78 (Adv-GRPO) vs 22.82 (Flow-GRPO) (-0.04 (等水平))。
> - OCR benchmark 上，OCR Accuracy 0.91 (Adv-GRPO) vs 0.91 (Flow-GRPO) (0.00 (等水平))。
> - General evaluation (PickScore, OCR, GenEval) 上，PickScore / OCR Accuracy / GenEval 21.90 / 0.69 / 0.69 (Adv-GRPO w/ DINO) vs 21.70 / 0.59 / 0.61 (SD3) (+0.20 / +0.10 / +0.08)。

## 概要

### 问题与瓶颈

文本到图像（T2I）生成模型在强化学习（RL）微调中普遍面临**奖励黑客**（Reward Hacking）问题：生成器学会钻奖励模型的空子，产生高奖励分数但视觉质量低劣的图像。例如，使用PickScore作为奖励优化时，图像画质反而下降；使用OCR精度作为奖励时，美学质量严重受损。其根本原因在于，固定的预训练奖励模型无法真正反映人类的感知偏好，且缺乏对生成过程的动态校准能力。

### 核心方法

本文提出**Adv-GRPO**，一个将对抗训练引入RL微调的新框架。其核心思想是：**让奖励模型同时充当鉴别器，与生成器进行对抗协同训练**。具体而言，奖励模型以高质量参考图像为正样本、生成图像为负样本进行动态更新，从而持续校准奖励信号，有效缓解奖励黑客。此外，方法进一步探索了**以视觉基础模型（如DINO）作为奖励源**：冻结DINO提取全局[CLS]和局部patch特征，通过轻量分类头合成密集奖励，为生成器提供丰富的视觉先验，而非单一标量分数。

### 方法定位

在方法谱系中，Adv-GRPO位于**RL微调与对抗训练的交叉点**。相较于Flow-GRPO等依赖固定奖励模型和KL散度正则化的RL方法，Adv-GRPO通过对抗机制实现了奖励模型的在线自适应，且实验表明不再需要KL惩罚即可获得更好的训练稳定性。相较于SFT（监督微调），Adv-GRPO在人工评估中展现出显著优势。

### 主要结果

- **奖励黑客缓解**：在PickScore和OCR两种奖励模型下，Adv-GRPO在保持基准分数持平的同时（PickScore 22.78 vs 22.82，OCR精度 0.91 vs 0.91），人工评估中画质胜率达70.0%，美学胜率达85.3%。
- **视觉基础模型奖励**：使用DINO作为奖励时，相较于SD3基线，OCR精度从0.59提升至0.69，GenEval从0.61提升至0.69；人工评估中美优胜率达72.4%。
- **数据高效性**：仅使用200张参考图像即可维持稳定的DINO相似度（0.621），验证了方法的鲁棒性。
- **风格定制**：通过选择特定领域的参考图像，Adv-GRPO可有效实现分布迁移，如将SD3迁移至动漫或科幻风格。

文本到图像（T2I）生成模型近年来取得了显著进展，但如何使生成结果更好地符合人类偏好仍是一个核心挑战。基于人类反馈的强化学习（RLHF）已成为对齐生成模型与人类偏好的主流范式，其中奖励模型扮演着关键角色——它负责评估生成图像的质量，并为生成器提供优化信号。

然而，现有奖励模型面临一个根本性困境：**奖励黑客（Reward Hacking）**。当生成器被训练去最大化奖励模型的输出时，它往往会找到奖励函数的漏洞，产生在指标上得分很高但实际质量不佳的图像。具体表现为：

- **PickScore奖励**：优化后虽然美学分数上升，但图像质量反而下降（画质退化）；
- **OCR奖励**：文本渲染精度提高，但以牺牲整体美学为代价；
- 奖励模型无法真正反映人类的感知偏好，其输出的单一标量信号缺乏足够的视觉信息密度。

这一瓶颈的根源在于：固定的预训练奖励模型一旦被生成器“攻破”，就无法提供有效的反馈信号。传统GRPO方法通过KL散度惩罚试图约束参数更新，但这只能延缓而非解决奖励黑客问题。

本文的核心动机由此产生：**能否让奖励模型与生成器协同进化，从而从根本上缓解奖励黑客？** 作者提出，将参考图像引入对抗训练框架，让奖励模型作为鉴别器动态区分高质量参考图像与生成图像，可以迫使奖励模型持续学习有意义的视觉判别特征。更进一步，利用视觉基础模型（如DINO）提取的全局-局部密集特征替代单一标量奖励，能够为生成器提供更丰富、更可靠的视觉先验，实现图像质量、美学和图文对齐的全面提升。

## 核心方法与创新机理

Adv-GRPO 的核心创新在于将对抗训练范式引入基于强化学习的文本到图像（T2I）微调框架，从两个层面重构了奖励信号的生成与校准机制，从而系统性地缓解了现有方法普遍面临的奖励黑客（reward hacking）问题。

### 1. 对抗协同训练：将奖励模型转化为动态鉴别器

传统 RL 微调方法（如 Flow-GRPO）依赖固定的预训练奖励模型（如 PickScore、OCR 准确率）提供标量反馈。然而，这些静态奖励函数容易被生成器“钻空子”——优化后的图像在自动指标上得分很高，但视觉质量反而下降（例如 PickScore 优化后画质劣化，OCR 优化后美学受损）。

Adv-GRPO 的关键改变是将奖励模型重新定位为**鉴别器**，与生成器进行对抗协同训练。具体而言：

- **生成器**仍基于 GRPO 损失进行优化，使用裁剪后的重要性加权优势函数：$$J_\text{gen}(\theta) = \mathbb{E}_{c\sim\mathcal{C},\{x_g^i\}_{i=1}^G\sim G_{\theta_\text{old}}}[f(r,\hat{A},\theta,\epsilon,\beta)]$$
- **奖励模型**则接收高质量参考图像作为正样本、生成图像作为负样本，通过鉴别损失动态更新：$$J_\text{reward}(\phi) = -\mathbb{E}_{x_r\sim\mathcal{D}_\text{ref}}[\log R_\phi(x_r)] - \mathbb{E}_{x_g\sim G_\theta(c)}[\log(1-R_\phi(x_g))]$$

这一对抗博弈机制的核心直觉是：当生成图像的质量逼近甚至超越参考图像时，固定的奖励模型将失去区分能力，从而被“黑客”。而对抗训练使奖励模型能够持续从生成图像中学习新的判别边界，从而提供更可靠的反馈信号。实验表明（Table 1），Adv-GRPO 在 PickScore（22.78 vs. 22.82）和 OCR 精度（0.91 vs. 0.91）上与 Flow-GRPO 保持同等水平，证明对抗训练并未牺牲定量性能；同时人工评估显示，在 PickScore 奖励下，Adv-GRPO 的图像质量胜率达到 70.0%（Figure 4a）。

值得注意的是，该框架对不同类型的奖励模型具有通用性。对于基于规则的奖励（如 OCR），Adv-GRPO 引入 CLIP 相似度作为辅助信号，将任务特定奖励与视觉真实性进行平衡：$$R_\text{combined}(x_g,c) = \lambda R_\text{rule}(x_g,c) + (1-\lambda) \text{sim}_\text{CLIP}(x_g,x_r)$$ 这使得 OCR 优化不再以牺牲美学为代价（Figure 4d vs. 4b）。

### 2. 视觉基础模型作为密集奖励源

第二个关键创新是用**冻结的视觉基础模型**替代传统偏好模型输出的单一标量奖励，从全局和局部两个粒度提供密集的视觉监督信号。

具体实现为：以冻结的 DINO 作为特征提取器 $F_\psi(\cdot)$，提取全局 `[CLS]` 嵌入 $\mathbf{f}_\text{cls}$ 和 patch 级特征 $\mathbf{F}_\text{patch}$，然后通过轻量分类头 $h_\phi(\cdot)$ 分别计算全局奖励和局部奖励：

$$R_\text{global}(x) = h_\phi(\mathbf{f}_\text{cls}), \quad R_\text{local}(x) = \frac{1}{n}\sum_{j\in\mathcal{S}} h_\phi(\mathbf{f}_j)$$

最终奖励为两者的加权组合：$$R_\phi(x) = \lambda_\text{g} R_\text{global}(x) + \lambda_\text{l} R_\text{local}(x)$$

这种全局-局部分离设计的优势在于：全局 `[CLS]` 特征强调高层语义和结构一致性，而局部 patch 特征捕获纹理、细节等细粒度视觉质量。两者互补，使奖励信号比单一标量更全面地反映人类感知偏好。

实验验证了这一设计的有效性。使用 DINO 奖励时，Adv-GRPO 在 GenEval 上从 SD3 的 0.61 提升至 0.69，OCR 精度从 0.59 提升至 0.69（Table 2）。人工评估更显示，在美学维度上 Adv-GRPO 相对 SD3 的胜率达到 72.4%（Figure 6a），且显著优于 Flow-GRPO 在 DINO 相似度奖励下的表现（Figure 6b）。此外，该方法还展现出对参考图像数量的高度数据效率——仅使用 200 张参考图像即可维持稳定的 DINO 相似度 0.621（Table 3）。

### 3. 无需 KL 正则化的稳定训练

传统 GRPO 依赖 KL 散度惩罚来约束策略更新幅度，防止生成器偏离初始分布过远。Adv-GRPO 的一个值得关注的特性是：在对抗训练框架下，**学习到的高质量奖励本身即可提供足够的引导信号，无需额外的 KL 正则化**。消融实验（Table 4）表明，Adv-GRPO 在 PickScore 和 OCR 精度上均显著优于 SFT 和带 KL 正则化的变体，验证了对抗奖励作为隐式正则化的有效性。

### 4. 与现有工作的本质差异

| 维度 | Flow-GRPO / 传统 RL 微调 | Adv-GRPO |
|------|--------------------------|----------|
| 奖励模型状态 | 固定预训练，静态 | 对抗协同训练，动态更新 |
| 奖励信号粒度 | 单一标量（偏好分数） | 全局 + 局部密集特征（DINO） |
| 奖励黑客应对 | 依赖 KL 正则化被动约束 | 对抗博弈主动校准 |
| 参考图像角色 | 无 | 作为正样本监督奖励模型 |
| 风格定制能力 | 无明确机制 | 通过选择特定域参考图像实现分布迁移（Figure 11） |

这些创新共同构成了一个闭环：对抗训练使奖励模型持续进化以抵抗黑客，视觉基础模型提供丰富的感知先验，二者结合使生成器在图像质量、美学和图文对齐三个维度均获得全面提升。

Adv-GRPO 的整体设计围绕一个核心洞察展开：**将对抗训练引入强化学习奖励回路，让奖励模型本身成为可学习的鉴别器**，从而动态校准奖励信号，缓解奖励黑客问题。整个框架由三条协同工作的支线构成，如 Figure 1 和 Figure 3 所示。

![[assets/figures/papers/paper_list_l2292_https_arxiv_org_abs_2511_20256/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our approach. Our method Adv-GRPO improves text-to-image (T2I) generation in three ways: 1) Alleviate Reward Hacking, achieving higher perceptual quality while maintaining comparable benchmark performance (e.g., PickScore, OCR), as shown in the top-left human evaluation panel; 2) Visual Foundation Model as Reward, leveraging visual foundation models (e.g., DINO) for rich visual priors, leading to overall improvements as shown in middle-top human evaluation results; 3) RL-based Distribution Transfer, enabling style customization by aligning generations with reference domains*

### 核心瓶颈与因果机制

现有 T2I 模型的 RL 微调（如 Flow-GRPO）面临一个根本性困境：固定的预训练奖励模型（PickScore、OCR 等）容易被生成器“钻空子”——生成器学会产出在奖励函数下得分极高、但人类感知质量反而下降的图像。例如，PickScore 优化会导致画质退化，OCR 奖励优化会损害美学（Figure 2, Figure 4c-d）。这一现象的根源在于**奖励模型缺乏对“高质量自然图像流形”的动态感知能力**，无法区分“真正更好”与“仅仅在评分维度上更高”。

Adv-GRPO 的因果调节手柄是：**在 GRPO 优化生成器的同时，将奖励模型作为鉴别器进行对抗训练**，以参考图像（高质量真实图像）为正样本、生成图像为负样本。这一设计迫使奖励模型持续学习“什么是好的图像”，而非固守一个静态的偏好函数。当生成图像的奖励均值超过参考图像时，触发对抗微调（Eq. 7），形成生成器与奖励模型的动态博弈。

### Pipeline 模块与数据流

整个 pipeline 由四个核心模块构成，数据流遵循“生成→评估→对抗更新→再生成”的闭环：

**1. Generator（SD3 with LoRA）**
基于 SD3 的去噪扩散骨干，通过 GRPO 损失进行优化。对于每条文本条件 $c$，生成一组 $G$ 张图像 $\{x_g^i\}_{i=1}^G$。生成器使用裁剪后的重要性加权优势进行更新（Eq. 5），其中优势值 $\hat{A}^i$ 由组内奖励归一化得到（Eq. 1）。

**2. Adversarial Reward Model（Discriminator）**
奖励模型同时充当鉴别器，接收参考图像 $x_r \sim \mathcal{D}_\text{ref}$（正样本）和生成图像 $x_g$（负样本），通过二元交叉熵损失进行训练（Eq. 6）。其输出作为动态奖励信号反馈给生成器。这一模块是缓解奖励黑客的关键：当生成器试图“刷分”时，鉴别器也会同步更新，提升对“伪高质量”图像的辨别能力。

**3. Visual Foundation Model（frozen DINO）**
作为替代奖励信号源，冻结的视觉基础模型（如 DINO）提取全局 `[CLS]` 嵌入 $\mathbf{f}_\text{cls}$ 和 patch 级特征 $\mathbf{F}_\text{patch}$（Eq. 9）。这提供了比单一标量奖励更丰富的视觉先验，涵盖语义结构（全局特征）和纹理细节（局部特征）两个互补维度。

**4. Reward Head（global + local）**
轻量分类头 $h_\phi$ 将 DINO 特征映射为奖励值：全局奖励 $R_\text{global}$ 来自 `[CLS]` 嵌入，局部奖励 $R_\text{local}$ 来自采样的 patch 特征均值（Eq. 10）。最终奖励为两者的加权组合（Eq. 11）。分类头通过 hinge loss 进行对抗训练，分别对全局特征（Eq. 12）和局部特征（Eq. 13）区分正负样本，总损失为加权和（Eq. 14）。

### 三种奖励模式

框架支持三类奖励模型的对抗训练，覆盖不同的应用场景：

- **人类偏好模型**（如 PickScore）：直接使用参考图像作为正样本进行对抗训练，当生成奖励超过参考时触发更新（Eq. 7）。
- **规则型奖励模型**（如 OCR）：由于规则奖励无法直接进行对抗训练，采用组合奖励 $R_\text{combined} = \lambda R_\text{rule} + (1-\lambda)\text{sim}_\text{CLIP}(x_g, x_r)$（Eq. 8），通过 CLIP 相似度引入视觉真实性约束。
- **视觉基础模型奖励**（如 DINO）：冻结骨干网络，仅训练分类头，提供全局-局部密集奖励信号。

### 与基线方法的关键差异

与 Flow-GRPO 相比，Adv-GRPO 在三个关键槽位上做了替换：

| 槽位 | Flow-GRPO | Adv-GRPO |
|------|-----------|----------|
| 奖励模型状态 | 固定预训练 | 对抗动态更新 |
| 奖励信号 | 单一标量 | 标量（偏好/规则）或密集特征（DINO） |
| 正则化策略 | KL 散度惩罚 | 无 KL 正则化，由对抗奖励引导 |

消融实验（Table 4）证实，Adv-GRPO 在去除 KL 惩罚后仍能保持训练稳定性，且性能显著优于 SFT 和带 KL 正则化的变体——这表明**对抗训练本身提供了比 KL 约束更有效的策略正则化**。

### 3.1 算法框架总览

Adv-GRPO 的整体流程如 Figure 3 所示，核心思想是将 T2I 生成器与奖励模型置于对抗协同训练的框架下：生成器通过 GRPO 损失进行优化，而奖励模型（充当鉴别器）则被训练以区分高质量参考图像（正样本）与生成图像（负样本），从而为生成器提供动态、难以被“黑客攻击”的奖励信号。

整个系统包含四个关键模块：

1.  **Generator (SD3 with LoRA)**：基于 GRPO 目标优化的去噪扩散生成器，接收文本条件 $c$ 并生成图像 $x_g$。生成器参数 $\theta$ 通过最大化裁剪后的重要性加权优势来更新。
2.  **Adversarial Reward Model (Discriminator)**：作为鉴别器的奖励模型 $R_\phi$，以参考图像 $x_r \sim \mathcal{D}_\text{ref}$ 为正样本、生成图像 $x_g$ 为负样本进行对抗训练，提供动态校准的奖励信号。
3.  **Visual Foundation Model (frozen DINO)**：冻结的视觉骨干网络 $F_\psi$（如 DINO），用于提取全局 [CLS] 嵌入 $\mathbf{f}_\text{cls}$ 和 patch 级特征 $\mathbf{F}_\text{patch}$，为奖励模型提供丰富的视觉先验。
4.  **Reward Head (global + local)**：轻量二分类头 $h_\phi$，将 DINO 特征映射为奖励值，分别计算全局奖励和局部奖励，最终加权组合形成密集奖励信号。

---

### 3.2 GRPO 基础目标

Adv-GRPO 以 GRPO（Group Relative Policy Optimization）为基础优化框架。对于每个文本条件 $c$，生成器采样一组 $G$ 张图像 $\{x_0^i\}_{i=1}^G$，奖励模型 $R$ 为每张图像打分后，通过组内归一化计算优势函数：

$$\hat{A}^i = \frac{R(x_0^i, c) - \text{mean}(\{R(x_0^j, c)\}_{j=1}^G)}{\text{std}(\{R(x_0^j, c)\}_{j=1}^G)} \tag{1}$$

其中 $\hat{A}^i$ 表示第 $i$ 个样本在组内的相对优势。GRPO 的优化目标为最大化裁剪后的重要性加权优势，并减去 KL 散度惩罚项以约束策略更新幅度：

$$f(\mathbf{r}, \hat{\mathbf{A}}, \theta, \epsilon, \beta) = \frac{1}{G}\sum_{i=1}^G \frac{1}{T}\sum_{t=0}^{T-1} \min\left(r_t^i(\theta)\hat{A}^i, \tilde{r}_t^i(\theta)\hat{A}^i\right) - \beta D_{KL}(\pi_\theta(\cdot|x_t^i,c) \parallel \pi_{\theta_\text{old}}(\cdot|x_t^i,c)) \tag{2}$$

其中重要性比率为当前策略与旧策略在去噪步骤 $t$ 的概率比，并通过裁剪操作限制在 $[1-\epsilon, 1+\epsilon]$ 区间内：

$$r_t^i(\theta) = \frac{p_\theta(x_{t-1}^i|x_t^i,c)}{p_{\theta_\text{old}}(x_{t-1}^i|x_t^i,c)}, \quad \tilde{r}_t^i(\theta) = \text{clip}(r_t^i(\theta), 1-\epsilon, 1+\epsilon) \tag{3}$$

---

### 3.3 对抗协同训练机制

Adv-GRPO 将标准 GAN 的极小极大博弈引入奖励模型的训练中。生成器 $G_\theta$ 与鉴别器 $D_\phi$ 的对抗目标为：

$$\min_\theta \max_\phi \mathbb{E}_{x\sim p_{data}}[\log D_\phi(x)] + \mathbb{E}_{z\sim p_z}[\log(1-D_\phi(G_\theta(z)))] \tag{4}$$

在此框架下，生成器的 GRPO 目标被重新表述为：

$$J_\text{gen}(\theta) = \mathbb{E}_{c\sim\mathcal{C},\{x_g^i\}_{i=1}^G\sim G_{\theta_\text{old}}}\left[f(r, \hat{A}, \theta, \epsilon, \beta)\right] \tag{5}$$

奖励模型（鉴别器）的对抗损失以参考图像为正样本、生成图像为负样本：

$$J_\text{reward}(\phi) = -\mathbb{E}_{x_r\sim\mathcal{D}_\text{ref}}[\log R_\phi(x_r)] - \mathbb{E}_{x_g\sim G_\theta(c)}[\log(1-R_\phi(x_g))] \tag{6}$$

**对抗触发机制**：方法通过监测生成图像的平均奖励 $\bar{r}_\text{gen}$ 与参考图像的平均奖励 $\bar{r}_\text{ref}$ 来控制对抗训练的时机：

$$\bar{r}_\text{gen} = \mathbb{E}_{x_g\sim G}[R(x_g)], \quad \bar{r}_\text{ref} = \mathbb{E}_{x_r\sim D_\text{ref}}[R(x_r)] \tag{7}$$

仅当 $\bar{r}_\text{gen}$ 超过 $\bar{r}_\text{ref}$ 时触发奖励模型的对抗微调，这一设计避免了在生成质量尚未接近参考水平时进行无效对抗。

**规则型奖励的组合策略**：对于基于规则的奖励模型（如 OCR 精度），方法引入 CLIP 相似度作为辅助信号，以平衡任务特定性与视觉真实性：

$$R_\text{combined}(x_g, c) = \lambda R_\text{rule}(x_g, c) + (1-\lambda) \text{sim}_\text{CLIP}(x_g, x_r) \tag{8}$$

---

### 3.4 视觉基础模型奖励

为获得更全面、更可靠的奖励信号，Adv-GRPO 探索了以冻结的视觉基础模型作为奖励骨干的方案。给定预训练的视觉基础模型 $F_\psi$（如 DINO），提取全局与局部特征：

$$\mathbf{f}_\text{cls}, \mathbf{F}_\text{patch} = F_\psi(x) \tag{9}$$

其中 $\mathbf{f}_\text{cls}$ 为全局 [CLS] 嵌入，$\mathbf{F}_\text{patch}$ 为 patch 级特征图。轻量分类头 $h_\phi$ 分别计算全局奖励和局部奖励：

$$R_\text{global}(x) = h_\phi(\mathbf{f}_\text{cls}), \quad R_\text{local}(x) = \frac{1}{n}\sum_{j\in\mathcal{S}} h_\phi(\mathbf{f}_j) \tag{10}$$

其中 $\mathcal{S}$ 为采样的 patch 索引集合，$n = |\mathcal{S}|$。最终奖励由全局与局部分数加权组合：

$$R_\phi(x) = \lambda_\text{g} R_\text{global}(x) + \lambda_\text{l} R_\text{local}(x) \tag{11}$$

这一全局-局部设计的关键优势在于：全局 [CLS] 特征强调高层语义和结构一致性，而局部 patch 特征捕捉细粒度纹理和细节质量，两者互补，为生成器提供密集的视觉引导。

奖励模型的训练采用 hinge 损失。全局特征的 hinge 损失为：

$$\mathcal{L}_\text{global}(\phi) = \mathbb{E}_{x_r}[\max(0,1-h_\phi(\mathbf{f}_\text{cls}^r))] + \mathbb{E}_{x_g}[\max(0,1+h_\phi(\mathbf{f}_\text{cls}^g))] \tag{12}$$

局部 patch 特征的 hinge 损失为：

$$\mathcal{L}_\text{local}(\phi) = \mathbb{E}_{x_r}\left[\frac{1}{|\mathcal{S}|}\sum_{j\in\mathcal{S}} \max(0,1-h_\phi(\mathbf{f}_j^r))\right] + \mathbb{E}_{x_g}\left[\frac{1}{|\mathcal{S}|}\sum_{j\in\mathcal{S}} \max(0,1+h_\phi(\mathbf{f}_j^g))\right] \tag{13}$$

最终对抗奖励损失为全局与局部损失的加权求和：

$$\mathcal{L}_\text{reward}(\phi) = \lambda_\text{g} \mathcal{L}_\text{global}(\phi) + \lambda_\text{l} \mathcal{L}_\text{local}(\phi) \tag{14}$$

消融实验（Table 4）表明，Adv-GRPO 在该对抗框架下**不需要 KL 散度正则化**即可获得比 SFT 和 KL 正则化变体更好的稳定性与性能，因为学习到的高质量奖励信号本身就能有效引导生成器的更新方向。

## 实验与关键发现

### 核心发现：对抗奖励缓解奖励黑客并提升感知质量

本方法的核心实验结论是：Adv-GRPO 通过对抗训练动态更新奖励模型，在保持基准指标竞争力的同时，显著缓解了现有奖励模型易被“黑客攻击”的缺陷，并在人工评估中获得压倒性优势。

**定量基准对比：对抗训练不损害指标表现。** 如表1所示，在 PickScore 和 OCR 两个代表性奖励模型下，Adv-GRPO 与 Flow-GRPO 的基准分数几乎持平（PickScore: 22.78 vs 22.82；OCR Accuracy: 0.91 vs 0.91）。这表明引入对抗训练机制并未以牺牲定量指标为代价，生成器在维持任务相关能力的同时，其优化方向得到了有效校准。

**人工评估：感知质量与美学的显著提升。** 基准分数的持平掩盖了感知质量的巨大差异。在 PickScore 奖励下，Adv-GRPO 相对 Flow-GRPO 的图像质量胜率达到 70.0%；在 OCR 奖励下，美学胜率更攀升至 85.3%（见 Figure 4）。这组数据揭示了关键洞察：固定的预训练奖励模型给出的标量分数与人类感知偏好之间存在系统性偏差，Flow-GRPO 在单纯最大化这些分数时陷入了奖励黑客陷阱（例如，PickScore 优化导致画质下降，OCR 优化损害美学），而 Adv-GRPO 通过引入参考图像作为鉴别器正样本，迫使奖励模型学习更鲁棒的“真实 vs 生成”判别边界，从而为生成器提供了更贴近人类偏好的梯度信号。

**视觉基础模型作为奖励：跨维度全面改进。** 当采用冻结的 DINO 作为奖励模型骨干时，Adv-GRPO 展现出更强的泛化能力。Table 2 显示，相比 SD3 基线，DINO 奖励下的 Adv-GRPO 在 PickScore（21.90 vs 21.70）、OCR Accuracy（0.69 vs 0.59）和 GenEval（0.69 vs 0.61）三项指标上全面领先。更关键的是，人工评估中该方法相对 SD3 的美学胜率达到 72.4%（Figure 6）。这表明视觉基础模型提取的全局-局部密集特征（[CLS] 嵌入 + patch 特征）比单一标量奖励包含更丰富的视觉先验，能够同时引导生成器改善画质、美学和图文对齐，避免了传统奖励模型顾此失彼的困境。

### 消融实验：关键设计选择验证

**参考图像数据效率。** Table 3 的消融实验表明，即使仅使用 200 张参考图像，Adv-GRPO 仍能维持稳定的 DINO 相似度（0.621），验证了该方法对参考数据规模的低敏感性。这一特性降低了实际应用中对大规模高质量参考数据集的依赖。

**对抗训练 vs SFT 与 KL 正则化。** Table 4 系统对比了 Adv-GRPO 与监督微调（SFT）及 KL 正则化变体。在 PickScore 和 OCR 精度上，Adv-GRPO 均显著优于 SFT（PickScore: 21.60；OCR: 0.68）。值得注意的是，Adv-GRPO 无需 KL 散度惩罚即可获得更好的训练稳定性——这是因为对抗训练学到的奖励模型本身提供了高质量、自校准的反馈信号，替代了 KL 正则化防止策略崩溃的作用。Figure 10 的人工评估进一步印证：Adv-GRPO（DINO 奖励）在美学和画质上的胜率均超过 70%，远超 SFT。

**多奖励组合的有效性。** 对于基于规则的奖励模型（如 OCR），Adv-GRPO 采用加权组合任务奖励与 CLIP 相似度的策略（Eq.8），消融实验证实该设计有效平衡了任务特定精度与视觉真实感，避免了单一规则奖励导致的生成质量退化。

### 失败模式与局限性

尽管 Adv-GRPO 在多数场景下表现优异，分析揭示了若干边界条件：

1. **触发条件依赖。** 对抗训练仅在生成图像的平均奖励超过参考图像时触发（Eq.7）。对于奖励始终低于参考的场景，鉴别器无法提供有效的对抗梯度，方法退化为普通 GRPO。这一机制假设参考集质量足够高，若参考图像质量参差不齐，可能引入噪声监督。

2. **参考分布偏差。** 方法依赖高质量参考图像数据集，参考图像的分布直接塑造奖励模型的判别偏好。当目标生成域与参考分布存在显著偏移时，对抗奖励可能引导生成器过度拟合参考风格，损害多样性（尽管风格迁移应用（Figure 11）利用了此特性，但在通用生成场景下需谨慎控制）。

3. **视觉基础模型覆盖范围有限。** 当前仅验证了 DINO 和 SigLIP（Figure 15）两种视觉骨干，未探索 CLIP、MAE 等其他模型。不同预训练模型的归纳偏置可能导致奖励信号的侧重点差异，该泛化性需进一步验证。

![[assets/figures/papers/paper_list_l2292_https_arxiv_org_abs_2511_20256/figures/020_Figure_15.jpg]]
*Figure 15: Visualizations with the SigLIP reward. Compared with SD3, using other visual foundation models such as SigLIP as the reward function can also lead to overall improvements in image quality*

4. **规则奖励的辅助开销。** 在 OCR 等规则奖励上采用的 CLIP 相似度辅助机制（Eq.8）引入了额外的前向计算，增加了训练开销。如何更优雅地融合规则奖励与视觉真实感信号仍是开放问题。

### 图表结论摘要

- **Figure 4/5：** 直观展示了 Adv-GRPO 缓解奖励黑客的效果——PickScore 下不再出现纹理过平滑，OCR 下不再牺牲美学换取文字精度。
- **Figure 6/7：** DINO 奖励下的生成结果在细节丰富度、光影自然度和语义一致性上均优于 SD3 基线。
- **Figure 9/Table 3/4：** 消融实验可视化与定量结果一致表明，对抗训练机制、全局-局部奖励组合、以及数据效率是方法有效性的三大支柱。
- **Figure 11：** 风格迁移应用验证了对抗 DINO 奖励在分布定制任务中的潜力，通过替换参考域即可将 SD3 迁移至动漫、科幻等目标风格。

![[assets/figures/papers/paper_list_l2292_https_arxiv_org_abs_2511_20256/figures/012_Figure_9.jpg]]
*Figure 9: Ablation results. (a) Visualizations with different numbers of reference images, showing effectiveness even with 200 samples. (b) Visualizations of ablation studies on SFT, KL regularization, multi-reward optimization, and our method Adv-GRPO*

![[assets/figures/papers/paper_list_l2292_https_arxiv_org_abs_2511_20256/figures/013_Table_3.jpg]]
*Table 3: Ablation on the number of reference samples used during inference. Our method maintains stable DINO similarity even with few reference images, demonstrating strong data efficiency*

![[assets/figures/papers/paper_list_l2292_https_arxiv_org_abs_2511_20256/figures/009_Table_1.jpg]]
*Table 1: Comparison under different reward models. Each row corresponds to an independent optimization using the specific reward and its associated evaluation metric*

![[assets/figures/papers/paper_list_l2292_https_arxiv_org_abs_2511_20256/figures/014_Table_4.jpg]]
*Table 4: Ablation on SFT, KL regularization, and multi-reward optimization under PickScore and OCR metrics*

## 定位与知识库关联

### 1. 与基线方法的关系

Adv-GRPO 的核心贡献在于将对抗训练范式引入基于强化学习的文生图微调流程，其方法定位可从与以下基线的对比中清晰界定：

**与 Flow-GRPO 的关系：从固定奖励到对抗协同。** Flow-GRPO 是本文最直接的 RL 基线，它使用固定的预训练奖励模型（如 PickScore、OCR 准确率）通过 GRPO 损失优化生成器。Adv-GRPO 在此基础上引入了两个关键改造：（1）将奖励模型从固定评估器转变为与生成器协同训练的鉴别器，以参考图像为正样本、生成图像为负样本进行对抗训练；（2）在视觉基础模型奖励方案中，用冻结的 DINO 骨干网络加可训练分类头替代单一标量奖励模型，提供全局-局部密集视觉信号。实验表明，Adv-GRPO 在 PickScore（22.78 vs 22.82）和 OCR 准确率（0.91 vs 0.91）上保持了与 Flow-GRPO 相当的水平（Table 1），同时在人工评估中画质胜率达 70.0%，美学胜率达 85.3%（Figure 4），这揭示了 Flow-GRPO 的固定奖励模型存在“奖励黑客”问题——优化后的生成器学会了欺骗奖励模型而非真正提升视觉质量。

**与 SD3 的关系：从基础生成到对抗增强。** SD3 作为基础生成模型，未经任何 RL 微调。Adv-GRPO 在 DINO 奖励方案下，将 SD3 的 OCR 准确率从 0.59 提升至 0.69，GenEval 从 0.61 提升至 0.69（Table 2），并在人工评估中取得 72.4% 的美学胜率（Figure 6）。这验证了视觉基础模型奖励能够提供比原始 SD3 更全面的生成引导。

**与 SFT 的关系：RL 优于监督微调。** 消融实验（Table 4）对比了 SFT 与 Adv-GRPO，SFT 在 PickScore（21.60）和 OCR 精度（0.68）上均低于 Adv-GRPO。人工评估（Figure 10）进一步确认 Adv-GRPO 在美学和画质上均显著优于 SFT。这表明简单的监督微调无法有效利用参考图像的分布信息，而对抗 RL 框架能够通过动态奖励信号实现更精细的分布对齐。

### 2. 方法适用的边界与条件

**对抗训练触发条件。** Adv-GRPO 的对抗微调仅在生成图像的平均奖励 $\bar{r}_\text{gen}$ 超过参考图像的平均奖励 $\bar{r}_\text{ref}$ 时触发（Eq. 7）。这意味着当生成器尚未达到足以“欺骗”奖励模型的水平时，对抗训练不会启动，奖励模型保持冻结。这一设计保证了训练稳定性，但也意味着在奖励始终低于参考的场景（如生成质量极差的早期训练阶段）该方法退化为普通 GRPO。

**参考图像依赖。** 方法需要一组高质量参考图像作为对抗训练的正样本。消融实验（Table 3）表明即使仅使用 200 张参考图像，Adv-GRPO 仍能维持稳定的 DINO 相似度（0.621），显示出较强的数据效率。但参考图像的质量和分布直接影响生成效果——若参考图像存在偏差或质量不均，奖励模型的鉴别能力将受到限制。

**奖励模型类型适配。** 方法被验证可适配三类奖励模型：（1）人类偏好模型（如 PickScore），采用对抗微调；（2）基于规则的奖励（如 OCR），采用任务奖励与 CLIP 相似度的加权组合 $R_\text{combined} = \lambda R_\text{rule} + (1-\lambda)\text{sim}_\text{CLIP}(x_g, x_r)$；（3）视觉基础模型奖励（如 DINO），采用全局-局部 hinge 损失训练。对于规则性奖励，CLIP 相似度的引入增加了计算开销，且 $\lambda$ 超参数需人工调节。

**视觉基础模型的局限性。** 本文仅验证了 DINO 和 SigLIP（Figure 15）两种视觉基础模型作为奖励骨干。其他广泛使用的模型如 CLIP、MAE 等未被探索，其作为奖励信号的有效性尚待验证。此外，视觉基础模型本身可能存在预训练偏差，这些偏差会通过奖励信号传递给生成器。

### 3. 局限与开放问题

**已确认的局限：**

1. **触发机制的单向性。** 对抗训练仅在生成奖励超过参考奖励时触发，对于奖励始终低于参考的场景，方法退化为普通 GRPO，无法从对抗训练中获益。
2. **参考图像质量依赖。** 方法假设参考图像代表高质量分布，但实际中参考图像的选择可能引入噪声或偏差，影响奖励模型的判别能力。
3. **视觉基础模型覆盖有限。** 仅验证了 DINO 和 SigLIP，未探索其他预训练范式（如对比学习 CLIP、掩码建模 MAE）的视觉骨干作为奖励信号的潜力。
4. **规则奖励的计算开销。** 在 OCR 等规则奖励上采用 CLIP 相似度辅助，增加了额外的推理计算。

**开放问题：**

1. **跨模态与跨任务的泛化。** 对抗奖励训练框架能否推广到视频生成、3D 生成等其他生成任务？其核心机制——用参考样本校准奖励模型——在理论上具有通用性，但需验证。
2. **参考图像的自适应选择。** 当前方法依赖固定的参考图像集。能否设计自适应机制，根据生成进度或文本条件动态选择最合适的参考样本？这涉及在线难例挖掘与课程学习策略的结合。
3. **对抗训练收敛性与多样性的平衡。** GAN 训练中固有的模式坍塌风险在文生图 RL 场景下如何表现？本文未报告多样性指标（如 FID 的 recall 分量），对抗训练对生成多样性的影响需进一步量化。
4. **多模态奖励的整合。** 视觉基础模型奖励仅利用图像信号，未结合文本条件。能否设计跨模态奖励模型，同时利用图文对齐信号（如 CLIP 分数）和视觉质量信号，实现更全面的奖励引导？
5. **奖励模型的持续演化。** 当前对抗训练中奖励模型随生成器同步更新，但两者更新频率和幅度如何最优协调？奖励模型是否可能过拟合到生成器的特定缺陷模式，从而丧失泛化判别能力？

## 原文 PDF

![[paperPDFs/CVPR_2026/The_Image_as_Its_Own_Reward_Reinforcement_Learning_with_Adversarial_Reward_for_Image_Generation.pdf]]
