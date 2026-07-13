---
title: "PureProof: Diffusion-Resistant Black-box Targeted Attack on Large Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PureProof_Diffusion_Resistant_Black_box_Targeted_Attack_on_Large_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- PureProof
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在攻击优化中显式模拟扩散净化过程：利用扩散替代模型进行单步逆向去噪预测，并与目标语义对齐；同时通过自适应再噪声增强正则化来应对扩散随机性，并通过自一致性约束稳定优化。这三部分的协同使得生成的对抗样本能够在经过扩散净化后仍保持恶意意图。
primary_logic: PureProof 证明，仅需随机时间步的单步逆向预测（SRA）即可有效指导对抗优化，避免全轨迹反向传播的巨额计算开销和梯度消失/爆炸问题；自适应再噪声增强（ARA）利用扩散模型的时间步相关噪声特性，作为曲率感知正则化器平滑损失地貌，稳定优化；自一致性正则化（SCR）通过强制两次去噪预测的一致性，增强了对净化后图像的预测稳健性。
claims:
- 在 DiffPure 净化防御下，PureProof 在多个开源 VLM 上取得显著优于基线攻击的定点攻击成功率（例如 LLaVA-1.5 上 ASR (Target) 达 12.3%，而基线攻击均接近 0%）。
- 消融实验显示，自适应再噪声增强（ARA）在所有模块中贡献最大，移除后攻击性能大幅下降，证实了处理扩散随机性对于成功规避 DBP 至关重要。
- 纯随机逆向对齐（SRA）使得每步优化时间从 DiffAttack 的 44.7 秒降至 1.76 秒，同时保持了优越的攻击效果。
- 在无防御设置下，PureProof 也取得了具有竞争力的 CLIP 分数，证明该方法不会牺牲基本攻击能力。
---

# PureProof: Diffusion-Resistant Black-box Targeted Attack on Large Vision-Language Models

> [!tip] 核心洞察
> PureProof 证明，仅需随机时间步的单步逆向预测（SRA）即可有效指导对抗优化，避免全轨迹反向传播的巨额计算开销和梯度消失/爆炸问题；自适应再噪声增强（ARA）利用扩散模型的时间步相关噪声特性，作为曲率感知正则化器平滑损失地貌，稳定优化；自一致性正则化（SCR）通过强制两次去噪预测的一致性，增强了对净化后图像的预测稳健性。

| 字段 | 内容 |
|------|------|
| 中文题名 | PureProof：一种面向大视觉语言模型的抗扩散黑盒定向攻击 |
| 英文题名 | PureProof: Diffusion-Resistant Black-box Targeted Attack on Large Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Cao_PureProof_Diffusion-Resistant_Black-box_Targeted_Attack_on_Large_Vision-Language_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PureProof |
| Dataset | LLaVA-1.5 (Open-source VLM) 对抗 DiffPure 净化, MiniGPT-4 对抗 DiffPure 净化, LLaVA-1.6 对抗 DiffPure 净化, Qwen3-VL (商业级VLM) 对抗 DiffPure 净化 |

> [!tip] 效果简介
> - LLaVA-1.5 (Open-source VLM) 对抗 DiffPure 净化 上，定向攻击成功率 ASR (Target) 12.3% vs ≈0.0% (best existing attack) (+12.3%)；诱导有害行为成功率 ASR (Fool) 76.8% vs ≈19.3% (best baseline) (提升逾50%)。
> - MiniGPT-4 对抗 DiffPure 净化 上，ASR (Fool) 77.1% vs 低（≤20%） (大幅提升)。
> - LLaVA-1.6 对抗 DiffPure 净化 上，ASR (Target) 17.8% vs ≈0% (+17.8%)。

## 概要

**问题瓶颈**：现有针对大视觉语言模型（VLM）的定向攻击在基于扩散的净化（Diffusion-Based Purification, DBP）防御下普遍失效。扩散模型的前向加噪与逆向去噪过程能够有效移除对抗扰动，使对抗样本被“净化”为良性图像，从而无法诱导模型输出目标文本。此前针对扩散净化的规避攻击（如 **DiffAttack**，Kang et al., NeurIPS 2023；**DiffHammer**，Wang et al., NeurIPS 2024）虽在分类任务上有所尝试，但依赖全扩散轨迹的反向传播，计算开销巨大且存在梯度消失/爆炸问题，难以高效迁移至 VLM 的定向攻击场景。

**核心方法与洞察**：本文提出 **PureProof**，一种抗扩散净化的黑盒定向攻击框架。其核心洞察在于：仅需随机时间步的单步逆向预测即可有效指导对抗优化，无需穿越完整扩散链。方法由三个协同模块构成——**随机逆向对齐（SRA）** 利用扩散替代模型在随机采样的时间步上进行单步去噪预测，并将预测的干净图像与目标图像语义对齐；**自适应再噪声增强（ARA）** 对预测的干净图像重新注入与时间步匹配的高斯噪声，利用扩散模型的噪声特性实现曲率感知的损失地貌平滑，以稳定梯度优化；**自一致性正则化（SCR）** 通过强制两次独立去噪预测的一致性，增强对净化后图像预测的稳健性。三者的协同使得对抗样本在经过扩散净化后仍能保持恶意意图。

**主要结果**：在 DiffPure 净化防御下，PureProof 在多个开源 VLM 上取得显著优于基线的定向攻击成功率——LLaVA-1.5 上 ASR (Target) 达 12.3%，而所有基线攻击均接近 0%；在商业级 VLM（如 Qwen3-VL）上 ASR (Fool) 达 87.7%。消融实验证实，自适应再噪声增强（ARA）对性能贡献最大，移除后攻击效果大幅下降；同时，SRA 使每步优化时间从 DiffAttack 的 44.7 秒降至 1.76 秒，兼顾了效率与效果。在无防御设置下，PureProof 亦保持具有竞争力的攻击能力，未牺牲基本攻击性能。

大视觉语言模型（Large Vision-Language Models, VLMs）通过融合视觉编码器与大语言模型，在图像描述、视觉问答等任务上展现出卓越能力。然而，其多模态输入特性引入了新的攻击面：对抗样本可通过微小的视觉扰动，诱导模型产生攻击者指定的恶意输出，构成**定向黑盒攻击**（targeted black-box attack）的严重威胁。

### 扩散净化防御及其对现有攻击的瓦解

为应对此类威胁，基于扩散的净化（Diffusion-Based Purification, DBP）防御被提出并展现出显著效果。其核心思想是利用扩散模型的去噪能力，在保留图像语义内容的同时消除对抗扰动。以代表性方法 **DiffPure**（Nie et al., ICML 2022）为例，其流程为：对输入图像执行短步前向扩散以破坏对抗噪声，随后通过逆向去噪重建干净图像。**GDMP**（Wang et al., arXiv 2022）则进一步利用原始输入的距离信息引导逆向过程，以平衡噪声去除与语义保真度；**LM**（Likelihood Maximization, Chen et al., ICML 2024）通过最大化似然来优化净化效果。

DBP的防御机制对现有VLM定向攻击构成了根本性挑战。现有攻击方法——如 **AttackVLM**（Zhao et al., NeurIPS 2023）、**Chain-of-Attack (CoA)**（Xie et al., CVPR 2025）、**AnyAttack**（Zhang et al., CVPR 2025）和 **FOA-Attack**（Jia et al., NeurIPS 2025）——在优化对抗扰动时并未考虑扩散净化的存在。其生成的对抗扰动属于高频、低幅噪声，在扩散模型的去噪过程中会被有效移除，导致攻击完全失效。如图1所示，经过DBP处理后，现有攻击生成的对抗样本被还原为良性图像，模型输出回归正常，定向攻击成功率（ASR）骤降至接近0%。

### 现有规避攻击的局限

针对扩散净化的规避攻击已在图像分类领域有所探索。**DiffAttack**（Kang et al., NeurIPS 2023）和 **DiffHammer**（Wang et al., NeurIPS 2024）通过模拟扩散净化的全轨迹梯度来优化对抗样本。然而，这些方法存在两个根本性瓶颈：

1. **计算开销巨大**：全轨迹反向传播需要对扩散模型的每一个时间步进行梯度计算，单步优化耗时高达数十秒（DiffAttack 约44.7秒/步），在实际攻击场景中难以承受。
2. **梯度消失与爆炸**：长链式反向传播面临梯度不稳定问题，限制了优化的有效性。

更重要的是，这些方法针对的是分类任务的非定向攻击，将其直接迁移至VLM的定向攻击场景时，面临语义对齐与扩散随机性的双重挑战。

### 核心瓶颈与本文动机

综上，现有VLM定向攻击在DBP防御下失效的根本瓶颈在于：**对抗扰动会被扩散模型的去噪过程有效移除，使攻击无法定向引导模型输出**。解决这一瓶颈需要回答一个关键问题：**如何生成在扩散净化后仍能保持恶意意图的对抗样本？**

这要求攻击优化过程必须显式地考虑扩散净化的影响，但同时需要避免全轨迹梯度计算带来的高昂代价。PureProof正是在这一动机下提出的：通过随机时间步的单步逆向预测、自适应再噪声增强和自一致性正则化三者的协同，以极低的计算代价实现抗扩散的定向攻击能力。

## 核心方法与创新机理

PureProof 的核心创新在于首次系统性地解决了大视觉语言模型（VLM）定向攻击在扩散净化（DBP）防御下全面失效的问题。现有攻击方法（如 **AttackVLM** (Zhao et al., NeurIPS 2023)、**CoA** (Xie et al., CVPR 2025)、**AnyAttack** (Zhang et al., CVPR 2025)）生成的对抗扰动会被扩散模型的去噪过程有效移除，导致攻击意图完全丧失。PureProof 通过三个协同模块，在攻击优化中显式模拟并利用扩散净化过程，实现了抗净化的定向攻击。

### 关键创新一：随机逆向对齐（SRA）—— 低成本模拟扩散净化

现有针对扩散净化的规避攻击（如 **DiffAttack** (Kang et al., NeurIPS 2023)）依赖全扩散轨迹的梯度反向传播，计算开销巨大（每步 44.7 秒）且面临梯度消失/爆炸问题。SRA 的核心突破在于：仅需在随机采样的扩散时间步 $t$ 上执行单步逆向去噪预测，即可有效指导对抗优化。

具体而言，SRA 利用公开的扩散替代模型（Guided Diffusion），从对抗图像的前向加噪结果 $\mathbf{x}_t$ 出发，通过 DDPM 闭式解预测干净图像：

$$\hat{\mathbf{x}}_0(\mathbf{x}_t, t) = \frac{\mathbf{x}_t - \sqrt{1 - \bar{\alpha}_t} \epsilon_\theta(\mathbf{x}_t, t)}{\sqrt{\bar{\alpha}_t}}$$

随后将预测的干净图像与目标图像 $\mathbf{x}_{\mathrm{tar}}$ 进行语义对齐：

$$\mathcal{L}_{\mathrm{SRA}} = - \mathbb{E}_t \big[ sim( \hat{\mathbf{x}}_0(\mathbf{x}_t, t), \mathbf{x}_{\mathrm{tar}} ) \big]$$

这一设计将每步优化时间从 DiffAttack 的 44.7 秒骤降至 1.76 秒（Fig. 3c），同时避免了全轨迹反向传播的不稳定性。

### 关键创新二：自适应再噪声增强（ARA）—— 对抗扩散随机性

扩散净化的随机性是导致攻击失效的另一核心原因。ARA 通过时间步自适应的再噪声机制，将扩散随机性转化为优化地貌的平滑正则化器。在获得 SRA 的干净图像预测 $\hat{\mathbf{x}}_0(\mathbf{x}_t, t)$ 后，ARA 重新注入与当前时间步匹配的高斯噪声，生成 $K$ 个变体：

$$\tilde{\mathbf{x}}_t^{(k)} = \sqrt{\bar{\alpha}_t} \hat{\mathbf{x}}_0(\mathbf{x}_t, t) + \sqrt{1 - \bar{\alpha}_t} \epsilon^{(k)}$$

并对这些变体与目标图像的语义相似度取平均：

$$\mathcal{L}_{\mathrm{ARA}} = - \mathbb{E}_t \left[ \frac{1}{K} \sum_{k=1}^{K} sim\Bigl( \tilde{\mathbf{x}}_t^{(k)}, \mathbf{x}_{\mathrm{tar}} \Bigr) \right]$$

从理论层面，ARA 损失的二阶泰勒展开揭示了其本质：

$$\mathbb{E}_{\epsilon}[\ell(\tilde{\mathbf{x}}_t)] = \ell(\mathbb{E}[\tilde{\mathbf{x}}_t]) + \frac{1}{2}\sigma_t^2 \mathrm{tr}(H_\ell(\mathbb{E}[\tilde{\mathbf{x}}_t])) + R_t$$

这表明 ARA 通过引入与噪声方差 $\sigma_t^2$ 成比例的曲率惩罚项，自适应地平整损失地貌，从而稳定梯度优化。消融实验（Fig. 3a）证实，移除 ARA 导致攻击性能下降最为显著，验证了处理扩散随机性对规避 DBP 的核心作用。

### 关键创新三：自一致性正则化（SCR）—— 增强跨时间步预测鲁棒性

SRA 和 ARA 均依赖于单步逆向预测的准确性，但扩散模型的随机性可能导致不同噪声实现下的预测不一致。SCR 通过强制两次独立去噪预测的一致性来解决这一问题：对同一干净图像估计 $\hat{\mathbf{x}}_0(\mathbf{x}_t, t)$ 重新注入不同噪声 $\epsilon'$，获得二次预测 $\hat{\mathbf{x}}_0'$，并惩罚两者的差异：

$$\mathcal{L}_{\mathrm{SCR}} = \mathbb{E}_t \left[ \lambda_t \cdot \| \hat{\mathbf{x}}_0' - \hat{\mathbf{x}}_0(\mathbf{x}_t, t) \|_2^2 \right]$$

该约束增强了攻击对净化后图像预测的相干性，使对抗样本在经过完整扩散净化后仍能保持恶意语义。

### 关键创新四：三模块协同的总损失设计

PureProof 将上述三个模块整合为统一的优化目标：

$$\mathcal{L}_{\mathrm{PureProof}} = \alpha \cdot \mathcal{L}_{\mathrm{SRA}} + (1 - \alpha) \cdot \mathcal{L}_{\mathrm{ARA}} + \mathcal{L}_{\mathrm{SCR}}$$

这一损失函数在 changed slots 层面实现了对基线方法的根本性超越：将仅最小化 CLIP 嵌入余弦距离的简单目标，替换为显式建模扩散净化过程、对抗扩散随机性、并增强预测一致性的复合损失。三者的协同使得 PureProof 在 DiffPure 净化防御下，在 LLaVA-1.5 上取得 12.3% 的定向攻击成功率（基线攻击均接近 0%，Table 1），同时将有害行为诱导成功率从最优基线的 19.3% 提升至 76.8%。

PureProof 是一个在现实黑盒条件下，针对大视觉语言模型（VLM）且能抵御扩散净化（DBP）防御的定向对抗攻击框架。其核心设计动机源于一个关键瓶颈：现有 VLM 定向攻击所注入的对抗扰动，在通过扩散模型的加噪-去噪过程后会被有效移除，导致攻击意图完全丧失。PureProof 通过在攻击优化中显式模拟扩散净化过程，使生成的对抗样本在经过净化后仍能保持恶意语义指向。

### 框架总览

PureProof 的整体 pipeline 由三个协同工作的核心模块构成：**随机逆向对齐（SRA）**、**自适应再噪声增强（ARA）** 和 **自一致性正则化（SCR）**。如图 Figure 2 所示，每次迭代中，对抗图像首先被前向加噪至一个随机采样的扩散时间步 $t$，随后经由替代扩散模型执行**单步逆向去噪预测**，得到对原始干净图像的估计 $\hat{\mathbf{x}}_0(\mathbf{x}_t, t)$。三个模块围绕这一预测结果展开优化：

![[assets/figures/papers/paper_list_l2223_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_PureProof_Diffusio/figures/002_Figure_2.jpg]]
*Figure 2: The framework of our proposed PureProof. PureProof consists of three components: SRA, ARA, and SCR. At each iteration, the adversarial image is forward-noised to a randomly sampled diffusion timestep and processed with a single reverse-denoising step. SRA aligns the predicted clean image with the target, ARA introduces controlled noise to stabilize gradients and adaptively smooth the optimization landscape, and SCR enforces consistency between paired clean-image estimates to improve coherence*

1. **SRA** 将单步预测的干净图像与目标图像在语义空间对齐，提供基础的定向引导信号。
2. **ARA** 在预测的干净图像上重新注入与时间步匹配的高斯噪声，生成 $K$ 个再噪声变体，并将它们与目标图像对齐，以平滑损失地貌、稳定梯度。
3. **SCR** 对同一噪声水平下的预测结果执行二次去噪，并约束两次预测之间的一致性，增强净化后预测的鲁棒性。

三者的损失函数以加权方式组合为 PureProof 的总优化目标：

$$\mathcal{L}_{\mathrm{PureProof}} = \alpha \cdot \mathcal{L}_{\mathrm{SRA}} + (1 - \alpha) \cdot \mathcal{L}_{\mathrm{ARA}} + \mathcal{L}_{\mathrm{SCR}}$$

### 模块间的输入输出关系

框架的数据流遵循一条清晰的“加噪→预测→增强→约束”链路：

- **输入**：原始干净图像 $\mathbf{x}_0$（或当前迭代的对抗样本）与目标图像 $\mathbf{x}_{\mathrm{tar}}$。
- **前向加噪**：按扩散前向过程 $\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$ 将对抗图像加噪至随机时间步 $t$。
- **单步逆向预测（SRA 核心）**：利用替代扩散模型（Guided Diffusion）的闭式解 $\hat{\mathbf{x}}_0(\mathbf{x}_t, t) = \frac{\mathbf{x}_t - \sqrt{1 - \bar{\alpha}_t} \epsilon_\theta(\mathbf{x}_t, t)}{\sqrt{\bar{\alpha}_t}}$ 直接估计干净图像，避免沿完整去噪轨迹反向传播的巨额计算开销和梯度消失/爆炸问题。
- **再噪声增强（ARA）**：对 $\hat{\mathbf{x}}_0(\mathbf{x}_t, t)$ 按 $\tilde{\mathbf{x}}_t^{(k)} = \sqrt{\bar{\alpha}_t} \hat{\mathbf{x}}_0(\mathbf{x}_t, t) + \sqrt{1 - \bar{\alpha}_t} \epsilon^{(k)}$ 生成 $K$ 个再噪声变体，利用扩散模型时间步相关的噪声特性实现曲率感知的正则化。
- **自一致性约束（SCR）**：通过二次重注入噪声 $\widetilde{\mathbf{x}}_t^{\prime}$ 并再次去噪得到 $\hat{\mathbf{x}}_0^{\prime}$，以 $\mathcal{L}_{\mathrm{SCR}} = \mathbb{E}_t [ \lambda_t \cdot \| \hat{\mathbf{x}}_0^{\prime} - \hat{\mathbf{x}}_0(\mathbf{x}_t, t) \|_2^2 ]$ 惩罚两次预测的差异。
- **语义对齐**：所有模块均通过 CLIP 编码器集成（ViT-B/16, ViT-B/32, ViTg-14）计算与目标图像的语义相似度，作为黑盒条件下的代理监督信号。

### 关键设计选择

- **替代模型选择**：攻击者使用公开的 Guided Diffusion 作为扩散替代模型，CLIP 集成作为语义监督，均不依赖对目标 VLM 内部参数的访问，维持黑盒设定。
- **时间步采样**：SRA 在每个迭代步随机采样扩散时间步 $t$，而非遍历完整轨迹，使得每步优化时间从 DiffAttack 的 44.7 秒降至 1.76 秒（Fig. 3c），同时保持优越的攻击效果。
- **超参数配置**：扩散时间步上限 $T_p = 150$，再噪声变体数 $K = 3$，SRA 与 ARA 的平衡系数 $\varepsilon = 0.3$（即 $\alpha$ 由 $\varepsilon$ 控制）。消融实验表明 $K=2$ 时性能已趋于饱和（Fig. 3b），进一步增加无显著收益。

这一框架的核心洞察在于：仅需随机时间步的单步逆向预测即可有效指导对抗优化，而自适应再噪声增强与自一致性正则化分别从损失地貌平滑和预测稳健性两个维度，解决了扩散随机性对攻击优化的根本挑战。

PureProof 的攻击优化围绕三个协同模块展开：**随机逆向对齐（SRA）**、**自适应再噪声增强（ARA）** 和 **自一致性正则化（SCR）**。三者共同构成一个可端到端优化的损失函数，使对抗样本在经过扩散净化后仍能保持恶意语义。

### 2.1 随机逆向对齐（SRA）

SRA 的核心思想是避免通过完整的扩散去噪轨迹进行反向传播。给定对抗图像 $\mathbf{x}_{\mathrm{adv}}$，先将其前向扩散至随机采样的时间步 $t$：

$$
\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_{\mathrm{adv}} + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}) \tag{1}
$$

随后利用公开的扩散替代模型（Guided Diffusion）进行**单步**逆向预测，得到干净图像的闭式估计：

$$
\hat{\mathbf{x}}_0(\mathbf{x}_t, t) = \frac{\mathbf{x}_t - \sqrt{1 - \bar{\alpha}_t} \epsilon_\theta(\mathbf{x}_t, t)}{\sqrt{\bar{\alpha}_t}} \tag{2}
$$

SRA 损失即最大化该预测干净图像与目标图像 $\mathbf{x}_{\mathrm{tar}}$ 之间的语义相似度：

$$
\mathcal{L}_{\mathrm{SRA}} = - \mathbb{E}_t \big[ \mathrm{sim}( \hat{\mathbf{x}}_0(\mathbf{x}_t, t), \mathbf{x}_{\mathrm{tar}} ) \big] \tag{3}
$$

其中 $\mathrm{sim}(\cdot, \cdot)$ 为 CLIP 替代模型集合（ViT-B/16, ViT-B/32, ViTg-14）提供的余弦相似度。随机时间步采样的设计使得优化过程无需展开完整去噪链，每步优化时间从 DiffAttack 的 44.7 秒降至 1.76 秒（Fig. 3c），同时避免了全轨迹反向传播中的梯度消失/爆炸问题。

### 2.2 自适应再噪声增强（ARA）

扩散模型的随机性源于前向加噪和逆向去噪过程中的高斯噪声注入。为应对这一不确定性，ARA 在 SRA 预测的干净图像上重新注入与当前时间步匹配的高斯噪声，生成 $K$ 个变体：

$$
\tilde{\mathbf{x}}_t^{(k)} = \sqrt{\bar{\alpha}_t} \hat{\mathbf{x}}_0(\mathbf{x}_t, t) + \sqrt{1 - \bar{\alpha}_t} \epsilon^{(k)}, \quad k = 1, \dots, K \tag{4}
$$

ARA 损失定义为这些再噪声变体与目标图像的平均语义相似度：

$$
\mathcal{L}_{\mathrm{ARA}} = - \mathbb{E}_t \left[ \frac{1}{K} \sum_{k=1}^{K} \mathrm{sim}\Bigl( \tilde{\mathbf{x}}_t^{(k)}, \mathbf{x}_{\mathrm{tar}} \Bigr) \right] \tag{5}
$$

ARA 的理论依据可通过二阶泰勒展开揭示。设 $\ell(\cdot)$ 为某损失函数，$\sigma_t^2 = 1 - \bar{\alpha}_t$ 为时间步 $t$ 的噪声方差，则 ARA 损失的期望满足：

$$
\mathbb{E}_{\epsilon}[\ell(\tilde{\mathbf{x}}_t)] = \ell(\mathbb{E}[\tilde{\mathbf{x}}_t]) + \frac{1}{2}\sigma_t^2 \mathrm{tr}(H_\ell(\mathbb{E}[\tilde{\mathbf{x}}_t])) + R_t \tag{6}
$$

其中 $H_\ell$ 为 Hessian 矩阵，$R_t$ 为高阶余项。式 (6) 表明，ARA 等价于在原始损失上施加一项**曲率感知的正则化**：噪声方差 $\sigma_t^2$ 越大（对应高噪声时间步），对损失地貌的平滑作用越强。这使得优化过程在不同扩散时间步下均能保持稳定的梯度信号，有效缓解扩散随机性对攻击优化的干扰。消融实验（Fig. 3a）证实，移除 ARA 后攻击性能下降最为显著，验证了处理扩散随机性是规避 DBP 的关键瓶颈。

### 2.3 自一致性正则化（SCR）

为进一步增强去噪预测的稳健性，SCR 对同一噪声水平下的两次独立去噪预测施加一致性约束。具体而言，在 ARA 再噪声的基础上，使用另一独立噪声 $\epsilon'$ 生成第二个变体：

$$
\widetilde{\mathbf{x}}_t^{\prime} = \sqrt{\bar{\alpha}_t} \hat{\mathbf{x}}_0(\mathbf{x}_t, t) + \sqrt{1 - \bar{\alpha}_t} \epsilon^{\prime} \tag{7}
$$

对该变体再次进行单步逆向预测，得到第二次干净图像估计 $\hat{\mathbf{x}}_0^{\prime}$。SCR 损失惩罚两次预测的差异：

$$
\mathcal{L}_{\mathrm{SCR}} = \mathbb{E}_t \left[ \lambda_t \cdot \| \hat{\mathbf{x}}_0^{\prime} - \hat{\mathbf{x}}_0(\mathbf{x}_t, t) \|_2^2 \right] \tag{8}
$$

其中 $\lambda_t$ 为时间步相关的权重系数。SCR 强制模型在随机噪声扰动下保持预测的相干性，从而提升对抗样本在经过扩散净化后的语义稳定性。

### 2.4 总损失函数

PureProof 的最终优化目标为上述三部分的加权组合：

$$
\mathcal{L}_{\mathrm{PureProof}} = \alpha \cdot \mathcal{L}_{\mathrm{SRA}} + (1 - \alpha) \cdot \mathcal{L}_{\mathrm{ARA}} + \mathcal{L}_{\mathrm{SCR}} \tag{9}
$$

其中 $\alpha$ 平衡 SRA 与 ARA 的贡献。三个模块的协同机制可概括为：SRA 提供高效的单步语义对齐信号；ARA 通过曲率感知正则化平滑损失地貌，应对扩散随机性；SCR 增强跨时间步的预测一致性，提升净化后图像的语义保真度。三者共同实现了对扩散净化防御的有效规避。

## 实验与关键发现

### 核心瓶颈验证：扩散净化下的定向攻击失效与PureProof的突破

现有针对大视觉语言模型（VLM）的定向攻击在基于扩散的净化（Diffusion-Based Purification, DBP）防御下普遍失效。其根本原因在于，对抗扰动会被扩散模型的去噪过程有效移除，使攻击无法定向引导模型输出。表1（Table 1）在开源VLM上的主实验结果直接验证了这一瓶颈：在DiffPure（Nie et al., ICML 2022）净化防御下，所有基线攻击方法——包括AttackVLM（Zhao et al., NeurIPS 2023）、Chain-of-Attack（Xie et al., CVPR 2025）、AnyAttack（Zhang et al., CVPR 2025）、FOA-Attack（Jia et al., NeurIPS 2025）以及针对扩散净化的规避攻击DiffAttack（Kang et al., NeurIPS 2023）和DiffHammer（Wang et al., NeurIPS 2024）——的定向攻击成功率（ASR Target）均接近0%。这构成了本文的核心研究瓶颈：**如何在扩散净化的“去噪”效应下，保持对抗样本的恶意语义指向？**

![[assets/figures/papers/paper_list_l2223_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_PureProof_Diffusio/figures/003_Table_1.jpg]]
*Table 1: Attack performance comparison on open-source VLMs against different diffusion-based purification (DBP) defenses. We report Ensemble CLIP score and ASR (%). The gray shading highlights our proposed method, while bold numbers indicate the best results*

PureProof通过三项协同设计突破了这一瓶颈。在LLaVA-1.5上，PureProof的ASR (Target)达到12.3%，而最佳基线方法仅约0.0%；诱导有害行为成功率ASR (Fool)达76.8%，较最佳基线（约19.3%）提升逾50个百分点。在MiniGPT-4上，ASR (Fool)达77.1%，同样大幅领先基线（≤20%）。在更新一代的LLaVA-1.6上，ASR (Target)进一步升至17.8%。这些结果表明，PureProof成功建立了从对抗图像到目标语义的“净化-鲁棒”映射通道。

### 跨防御泛化与商业级VLM上的有效性

PureProof的攻击能力不仅限于单一防御。如表1所示，在GDMP（Wang et al., arXiv 2022）和LM（Chen et al., ICML 2024）两种替代扩散净化防御下，PureProof同样保持显著优势。例如，在LLaVA-1.5对抗GDMP的设置中，PureProof的ASR (Target)为8.1%，而最佳基线仅为0.3%。这表明PureProof对扩散净化的不同实现方式具有较好的泛化性。

在商业级VLM上（表2, Table 2），PureProof展现出更强的攻击效能：在Qwen3-VL上ASR (Fool)达87.7%，Gemma 3上达85.4%，GPT-5上达78.1%，Gemini-2.5上达67.8%。这些模型代表当前工业界的前沿水平，高攻击成功率意味着PureProof所揭示的安全威胁具有现实紧迫性。

![[assets/figures/papers/paper_list_l2223_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_PureProof_Diffusio/figures/005_Table_2.jpg]]
*Table 2: Attack performance comparison on commercial VLMs against DiffPure. We report Ensemble CLIP score and ASR (%). The gray shading highlights our proposed method, while bold numbers indicate the best results*

### 消融实验：因果机制的实证分解

图3（Figure 3）的消融实验系统解构了PureProof各模块的贡献，验证了分析中识别的因果机制。

![[assets/figures/papers/paper_list_l2223_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_PureProof_Diffusio/figures/006_Figure_3.jpg]]
*Figure 3: Left: Attack efficacy of each loss components in*

**自适应再噪声增强（ARA）的核心作用**。在三个模块中，移除ARA导致攻击性能最显著的下降（Fig. 3a）。这一结果直接证实了分析中的核心判断：**扩散过程的随机性是阻碍对抗样本通过净化的主要障碍，而ARA通过时间步自适应的噪声注入，有效平滑了优化地貌**。从理论层面看，ARA损失的二阶泰勒展开（Eq. 8）揭示了其作为曲率感知正则化器的本质——通过最小化损失函数在噪声扰动下的期望值，ARA隐式地惩罚了损失地貌的曲率，使优化更稳定。

**自一致性正则化（SCR）的辅助贡献**。SCR的移除同样导致性能适度下降（Fig. 3a），证明强制两次独立去噪预测的一致性有助于增强对净化后图像的预测稳健性。这验证了分析中的判断：SCR通过约束跨时间步的预测相干性，提升了攻击的可靠性。

**再噪声变体数量K的饱和效应**。Fig. 3b显示，当K=2时ARA的性能已趋于饱和，进一步增加K无显著收益。这表明少量噪声变体即可有效捕捉扩散时间步相关的不确定性，验证了ARA设计的高效性。

**单步逆向预测的效率优势**。Fig. 3c对比了不同方法的每步优化时间。PureProof每步仅需1.76秒，而依赖全扩散轨迹梯度的DiffAttack需44.72秒——效率提升逾25倍，同时攻击效果更优。这直接验证了分析中的核心洞察：**仅需随机时间步的单步逆向预测（SRA）即可有效指导对抗优化，避免全轨迹反向传播的巨额计算开销和梯度消失/爆炸问题**。

### 鲁棒性边界与无防御场景下的竞争力

在高斯噪声干扰下（σ=8/255），PureProof在MiniGPT-4上取得0.6342的Ensemble CLIP Score（表3, Table 3），略优于CoA的0.6274，表明该方法对常见输入扰动具有一定鲁棒性。

![[assets/figures/papers/paper_list_l2223_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_PureProof_Diffusio/figures/007_Table_3.jpg]]
*Table 3: Attack performance comparison against Gaussian noise. We report Ensemble CLIP score (↑). The gray shading highlights our method, while the bold numbers indicate the best results*

在无防御场景下（表4, Table 4），PureProof同样取得具有竞争力的CLIP分数，证明该方法并未以牺牲基本攻击能力为代价来换取对DBP的规避能力。这一结果排除了“PureProof仅通过降低扰动幅度来绕过净化”的简单解释，进一步支持了其设计机制的有效性。

### 可视化验证

图4（Figure 4）展示了PureProof生成的对抗样本在经DiffPure净化后，成功诱导LLaVA-1.5输出目标描述的可视化案例。顶部为原始干净图像和对应的目标文本，底部为净化后对抗图像所触发的模型输出。这些定性结果与定量指标相互印证，直观展示了PureProof使对抗意图“穿透”扩散净化过程的能力。

![[assets/figures/papers/paper_list_l2223_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_PureProof_Diffusio/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of our proposed PureProof performance against DBP on LLaVA-1.5. Top: clean and target text. Bottom: model outputs on adversarial images purified by DiffPure*

### 实验公平性说明

所有攻击方法均在同一扰动预算（ℓ∞ bound = 16/255）和相同优化步数（PGD 100步）下评估。所有攻击均采用相同的CLIP替代模型集合（ViT-B/16, ViT-B/32, ViTg-14）以及相同的公开扩散替代模型（Guided Diffusion），排除了替代模型差异对比较结果的影响。这些控制条件确保了实验结论的可靠性。

## 定位与知识库关联

### 1. 攻击方法谱系

PureProof 处于**大视觉语言模型（VLM）黑盒定向攻击**与**扩散净化防御规避**的交叉点。其方法谱系可从两个维度梳理。

#### 1.1 VLM 定向攻击基线

在 PureProof 之前，VLM 定向攻击方法普遍未考虑扩散净化防御的存在。典型基线包括：

- **AttackVLM**（Zhao et al., NeurIPS 2023）：早期 VLM 黑盒定向攻击，通过 CLIP 嵌入空间中的余弦相似度优化生成对抗扰动。该方法在无防御场景下有效，但面对扩散净化时，扰动被去噪过程完全移除。
- **Chain-of-Attack (CoA)**（Xie et al., CVPR 2025）：引入链式语义引导的定向攻击策略，增强了攻击的语义一致性，但同样未建模扩散净化过程。
- **AnyAttack**（Zhang et al., CVPR 2025）与 **FOA-Attack**（Jia et al., NeurIPS 2025）：更近期的定向攻击方法，在无防御设置下取得更强性能，但在扩散净化防御下均接近完全失效（ASR (Target) ≈ 0%）。

这些方法的核心瓶颈在于：它们仅最小化对抗图像与目标图像的 CLIP 嵌入余弦距离，未考虑防御方可能执行的扩散去噪操作。PureProof 在此瓶颈上做出根本性改变——将扩散净化过程显式纳入攻击优化循环。

#### 1.2 扩散净化规避攻击基线

针对扩散净化防御的规避攻击此前仅存在于图像分类任务中，代表性工作包括：

- **DiffAttack**（Kang et al., NeurIPS 2023）：通过计算扩散模型全轨迹的梯度来生成抗净化对抗样本。该方法首次证明了规避扩散净化的可行性，但存在两个严重缺陷：（1）需反向传播通过完整扩散链，计算开销极大（每步约 44.7 秒）；（2）全轨迹梯度存在消失/爆炸问题，导致优化不稳定。
- **DiffHammer**（Wang et al., NeurIPS 2024）：在 DiffAttack 基础上改进，通过更精细的梯度估计策略提升攻击效果，但同样依赖全轨迹反向传播，计算效率问题未解决。

PureProof 与上述方法的本质区别在于**对扩散净化过程的建模方式**：它仅利用随机时间步的单步逆向预测（SRA）来指导优化，完全避免了全轨迹梯度回传。这一设计使每步优化时间从 DiffAttack 的 44.72 秒降至 1.76 秒，同时攻击效果更优（见 Figure 3c）。

#### 1.3 扩散净化防御基线

PureProof 评估中涉及的扩散净化防御包括：

- **DiffPure**（Nie et al., ICML 2022）：通过短时前向扩散加逆向去噪来移除对抗噪声，同时保留语义内容。这是当前最主流的扩散净化防御。
- **GDMP**（Wang et al., arXiv 2022）：在逆向过程中引入与原始输入的距离引导，平衡噪声移除与语义保真度。
- **LM (Likelihood Maximization)**（Chen et al., ICML 2024）：基于似然最大化的净化策略，进一步约束去噪过程。

PureProof 在所有三种防御下均展现出显著优于基线的攻击成功率（Table 1），表明其规避能力具有跨防御策略的泛化性。

### 2. 核心方法定位

PureProof 的方法论贡献可定位于以下三个技术槽位的变化：

| 技术槽位 | 基线方案 | PureProof 方案 | 证据锚点 |
|---------|---------|---------------|---------|
| 对扩散净化过程的建模 | 未考虑（VLM攻击）或全轨迹梯度（DiffAttack/DiffHammer） | 随机时间步单步逆向预测（SRA），避免全轨迹回传 | Sec. 3.2, Eq. 4–5 |
| 对抗扩散随机性的机制 | 无专用机制（或简单 EOT 平均） | 自适应再噪声增强（ARA）：时间步相关噪声注入实现曲率感知的损失平整化 | Sec. 3.2, Eq. 6–8 |
| 时序一致性约束 | 未使用 | 自一致性正则化（SCR）：对同一噪声水平下的两次去噪预测施加一致性损失 | Sec. 3.2, Eq. 9–10 |

这三个槽位的变化形成了 PureProof 的核心因果链路：SRA 提供高效的净化过程模拟，ARA 处理扩散随机性导致的优化不稳定，SCR 增强跨时间步预测的鲁棒性。消融实验（Figure 3a）证实，ARA 的贡献最为显著，移除后攻击性能大幅下降，验证了处理扩散随机性是规避 DBP 的关键瓶颈。

### 3. 适用边界与局限

尽管 PureProof 在实验中展现出显著优势，其适用边界需明确界定：

**已验证的适用范围**：
- 攻击范式：黑盒定向攻击（仅需 VLM 文本输出，无需梯度访问）
- 目标模型：开源 VLM（LLaVA-1.5/1.6, MiniGPT-4, InstructBLIP）与商业 VLM（GPT-5, Gemma 3, Qwen3-VL, Gemini-2.5）
- 防御类型：基于扩散的净化防御（DiffPure, GDMP, LM）
- 扰动预算：ℓ∞ 约束 ≤ 16/255
- 替代模型：CLIP 集成（ViT-B/16, ViT-B/32, ViTg-14）+ Guided Diffusion

**已知局限与待验证边界**：
1. **扩散模型迁移性**：当前实验使用 Guided Diffusion 作为替代模型。若防御方使用不同架构的扩散模型（如 Stable Diffusion 系列）或更复杂的净化策略，PureProof 的迁移攻击效果尚未验证。
2. **模态限制**：方法仅针对图像模态设计，未涉及视频或多模态融合攻击场景。
3. **对抗训练防御**：对抗性训练对 PureProof 的防御效果未被探讨，这可能是未来的潜在防御方向。
4. **物理世界鲁棒性**：在光照变化、视角变换等物理世界条件下的攻击鲁棒性仍待验证。

### 4. 开放问题

基于方法设计与实验分析，以下开放问题值得后续研究关注：

1. **自适应时间步采样**：当前 SRA 从均匀分布中随机采样扩散时间步。是否可以通过自适应策略（如根据损失地貌动态调整采样分布）进一步提升攻击效率与成功率？
2. **跨架构迁移性**：在实际部署中，攻击者通常无法获知防御方使用的具体扩散模型。PureProof 对不同扩散架构的迁移能力需要系统评估。
3. **多模态扩展**：该方法的核心思想——在优化中模拟净化过程——是否可扩展至视频对抗攻击或其他多模态场景？
4. **防御方的反制策略**：若防御方采用对抗训练或差异化扩散模型，PureProof 的鲁棒性如何？这构成了攻击-防御博弈的下一轮迭代。
5. **更强的自适应攻击**：ARA 的再噪声变体数量 K=2 时性能已趋于饱和（Figure 3b），这是否意味着当前噪声增强策略已触及信息瓶颈？更精细的噪声建模（如条件扩散模型）是否可进一步突破？

*注：以上开放问题均来自论文讨论部分的明确陈述，部分问题（如物理世界鲁棒性、对抗训练防御）的实验证据尚缺，需后续工作验证。*

## 原文 PDF

![[paperPDFs/CVPR_2026/PureProof_Diffusion_Resistant_Black_box_Targeted_Attack_on_Large_Vision_Language_Models.pdf]]
