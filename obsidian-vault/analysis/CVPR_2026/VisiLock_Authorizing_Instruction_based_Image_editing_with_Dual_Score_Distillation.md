---
title: "VisiLock: Authorizing Instruction-based Image editing with Dual Score Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VisiLock_Authorizing_Instruction_based_Image_editing_with_Dual_Score_Distillation.pdf
project_link: null
code_link: "https://github.com/Luvata/VisiLock"
aliases:
- VisiLock
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过双教师蒸馏将授权与未授权行为的学习解耦，并从退化教师初始化学生模型，使模型默认处于锁定状态
primary_logic: 利用原始教师和退化教师分别提供授权和未授权样本的噪声预测目标，避免单模型多目标梯度冲突；同时从退化教师初始化确保发布模型默认锁定，仅对正确钥匙恢复编辑能力
claims:
- 双教师蒸馏有效解耦授权与未授权行为，避免训练崩溃
- 授权编辑保持基线质量，未授权尝试严重退化（CLIP-I 0.821 vs 0.481，DINO 0.726 vs 0.072）
- 从退化教师初始化提供抗对抗微调能力，恢复受限
- MagicBrush 上 CLIP-I ↑ = 0.821 (Authorized)
---

# VisiLock: Authorizing Instruction-based Image editing with Dual Score Distillation

> [!tip] 核心洞察
> 利用原始教师和退化教师分别提供授权和未授权样本的噪声预测目标，避免单模型多目标梯度冲突；同时从退化教师初始化确保发布模型默认锁定，仅对正确钥匙恢复编辑能力

| 字段 | 内容 |
|------|------|
| 中文题名 | VisiLock: 基于双分数蒸馏的指令图像编辑授权 |
| 英文题名 | VisiLock: Authorizing Instruction-based Image editing with Dual Score Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Le_VisiLock_Authorizing_Instruction-based_Image_editing_with_Dual_Score_Distillation_CVPR_2026_paper.html) · [Code](https://github.com/Luvata/VisiLock) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VisiLock |
| Dataset | MagicBrush |

> [!tip] 效果简介
> - MagicBrush 上，CLIP-I ↑ 0.821 (Authorized) vs 0.481 (Unauthorized) (-41%)；DINO ↑ 0.726 (Authorized) vs 0.072 (Unauthorized) (-90%)。

## 概要

指令驱动的图像编辑模型（如 **InstructPix2Pix**，Brooks et al., CVPR 2022）允许用户通过自然语言描述对图像进行修改，但模型一旦公开发布，其编辑能力便完全不受控制。**VisiLock** 针对这一访问控制缺失问题，提出了一种基于可见空间视觉触发器的条件授权机制：当输入图像包含正确的可见钥匙时，模型输出高质量编辑结果；否则输出预定义的退化结果（如固定提示图、模糊或噪声图像），从而在发布公开检查点的同时保留对高级编辑能力的控制。

核心挑战在于，直接对扩散模型进行多目标微调会导致**授权与未授权行为的梯度冲突**——授权梯度将权重拉向编辑流形，而未授权梯度将其推向退化方向，二者相互抵消，最终使模型去噪流形崩溃。现有方案 **FMLock**（Liu et al., ICLR 2024 Withdrawn Submission）尝试通过对比损失推开两种行为的噪声预测，但训练不稳定，约 200 步后即崩溃（Figure 4）。

VisiLock 的核心洞察是**通过双教师蒸馏解耦两种行为的学习**：引入一个经微调的“退化教师”定义失败模式，由原始预训练模型作为“原始教师”保留编辑能力，学生模型同时从两个教师蒸馏噪声预测。关键设计在于**从退化教师初始化学生模型**，使其默认处于锁定状态，仅对正确钥匙恢复编辑能力。这一初始化策略天然提供了对抗微调解锁的鲁棒性——即使攻击者尝试通过自蒸馏将授权行为迁移到未授权模式，恢复程度也因初始遗忘而受限。

主要实验结果（Table 1，MagicBrush 基准）：授权编辑保持基线质量（CLIP-I: 0.821, DINO: 0.726），而未授权尝试严重退化（CLIP-I: 0.481, DINO: 0.072），分别下降 41% 和 90%。消融实验验证了退化教师初始化对训练稳定性的关键作用（随机初始化无法收敛，从原始模型初始化产生弱锁），以及边距排斥损失对行为分离的增强效果。

方法层面，VisiLock 属于**模型级访问控制**范式，与基于水印的被动追溯方法互补。其双教师蒸馏框架不改变模型架构，不引入额外模块，可推广至其他条件扩散模型。当前局限包括：授权编辑质量略低于未锁定基线，可见钥匙遮挡小区域，以及对抗复杂自适应攻击的鲁棒性有待提升。未来方向涵盖扩展至 Flux Kontext、Qwen Image 等现代架构，以及多钥匙分层锁定以支持细粒度访问控制。



### 指令图像编辑的普及与访问控制缺失

指令驱动的图像编辑（instruction-guided image editing）允许用户通过自然语言描述对图像进行语义级修改，以 **InstructPix2Pix**（Brooks et al., CVPR 2022）为代表的扩散模型已展现出令人瞩目的编辑能力。模型提供商通常以公共检查点（public checkpoint）形式发布预训练权重，用户下载后即可无限制地使用全部编辑功能。这一开放范式带来了直接的商业化困境：提供商无法对高级编辑能力实施访问控制，任何用户均可免费调用全部功能。

现有模型保护方案主要依赖水印（watermarking）技术进行事后追溯，但无法在推理阶段主动阻止未授权使用。真正需要的是一种**模型锁定**（model locking）机制——发布一个默认处于退化状态的模型检查点，仅当用户提供正确密钥（key）时才恢复完整编辑能力。

### 现有锁定方案的训练困境

当前模型锁定的代表性工作是 **FMLock**（Liu et al., ICLR 2024 Withdrawn Submission），其核心思路是通过对比学习（contrastive learning）训练模型区分秘密触发词：正确触发词产生正常输出，错误触发词产生退化结果。然而，FMLock 面临根本性的训练稳定性问题。

**核心瓶颈在于多目标梯度冲突**。当单一扩散模型同时学习授权编辑和未授权退化两种行为时，两个目标的噪声预测方向相互矛盾——授权分支要求模型向高质量编辑方向去噪，未授权分支则要求模型向退化方向去噪。这种冲突导致扩散模型的去噪流形（denoising manifold）崩溃，训练过程中两类输出均变得不可用（Figure 4 展示了 FMLock 在训练约 200 步后两类模式输出同时崩溃的现象）。

朴素微调方案——简单地对授权和未授权样本分别施加标准扩散损失——同样无法解决这一问题，因为两类样本的噪声预测目标在参数空间中指向相反方向，联合优化导致模型无法收敛到任一行为的有效解。

### VisiLock 的核心动机

本文的核心洞察是：**授权与未授权行为的学习必须解耦**。与其让单一模型内部同时容纳两种相互冲突的行为，不如通过独立的教师模型分别提供两类行为的噪声预测目标，让学生模型从两个教师处分别蒸馏（distill）对应的行为。

这一思路引出三个关键设计决策：

1. **双教师蒸馏**：使用原始教师（预训练的 InstructPix2Pix）提供授权样本的高质量编辑目标，使用退化教师（经微调以抑制编辑能力的模型）提供未授权样本的退化目标。学生模型无需在内部调和冲突，只需分别模仿两个教师的行为。

2. **从退化状态初始化**：学生模型从退化教师权重初始化，而非随机初始化或从原始 InstructPix2Pix 初始化。这确保了发布模型默认处于锁定状态，且训练初期即具备稳定的退化行为，避免训练崩溃。

3. **可见空间触发器**：与 FMLock 的文本秘密触发词不同，VisiLock 采用嵌入输入图像的可见视觉钥匙（visible spatial trigger），使授权机制对用户透明且易于验证。

通过这一双分数蒸馏（Dual Score Distillation）框架，VisiLock 旨在实现：授权编辑质量接近未锁定基线（CLIP-I 0.821, DINO 0.726），而未授权尝试的图像相似度大幅退化（CLIP-I 下降 41% 至 0.481，DINO 下降 90% 至 0.072），无需修改模型架构或引入额外模块。



## 核心方法与创新机理

VisiLock 的核心创新在于用**双教师蒸馏（Dual Score Distillation）**解耦了授权与未授权编辑行为的学习，从根本上解决了此前方法中单模型多目标训练导致的梯度冲突与训练崩溃问题。

### 问题根因：多目标梯度冲突

指令图像编辑模型的访问控制面临一个本质性矛盾：模型需要同时学习两种截然不同的行为——在正确钥匙下输出高质量编辑，在无钥匙或错误钥匙下输出退化结果。直接对混合批次进行微调会导致梯度“拔河”：

$$
\mathcal{L}_{\mathrm{naive}} = \mathbb{E}[\|\epsilon - \hat{\epsilon}_{\theta}^{\mathrm{auth}}\|_2^2] + \mathbb{E}[\|\epsilon' - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2^2]
$$

授权梯度将权重拉向编辑流形，而未授权梯度将其推向恒等映射或退化方向，两者相互抵消，导致去噪流形崩溃（Section 3.2）。**FMLock**（Liu et al., ICLR 2024 Withdrawn Submission）尝试通过对比损失推开两种噪声预测来缓解冲突：

$$
\mathcal{L}_{\mathrm{FMLock}} = \mathcal{L}_{\mathrm{naive}} - \lambda \mathbb{E}[\|\hat{\epsilon}_{\theta}^{\mathrm{auth}} - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2]
$$

但该方法在训练约200步后即出现不稳定，两种模式的输出均不可用（Figure 4）。

### 核心机制：双教师蒸馏 + 退化初始化

VisiLock 通过三个关键设计彻底绕过了梯度冲突：

**1. 双教师解耦学习。** 引入两个独立教师模型分别负责两种行为的噪声预测目标：**原始教师 $\mathbf{M}_o$**（预训练的 InstructPix2Pix）提供授权样本的高质量编辑目标；**退化教师 $\mathbf{M}_d$**（经微调抑制编辑能力的模型）定义未授权时的失败模式。学生模型 $\mathbf{M}_{lock}$ 通过蒸馏分别从两个教师学习：

$$
\mathcal{L}_{\mathrm{auth}} = \mathbb{E}_{t, \mathbf{z}_0, \epsilon}[\|\mathbf{M}_o([\mathbf{z}_t, \mathbf{z}_x], t, c) - \hat{\epsilon}_{\theta}^{\mathrm{auth}}\|_2^2]
$$

$$
\mathcal{L}_{\mathrm{unauth}} = \mathbb{E}_{t, \mathbf{z}_0, \epsilon}[\|\mathbf{M}_d([\mathbf{z}_t, \mathbf{z}_x], t, c) - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2^2]
$$

由于两个教师各自独立运行，授权与未授权梯度不再在学生模型内部直接对抗，训练稳定性得到根本保证。

**2. 退化教师初始化。** 学生模型不从随机权重或预训练 InstructPix2Pix 初始化，而是**从退化教师 $\mathbf{M}_d$ 初始化**。这一设计的深层逻辑是：初始训练阶段学生遗忘几乎所有编辑能力，随后双分数蒸馏框架在有限数据上有选择地重新学习授权能力，而未授权分支仅能恢复到退化教师的上限。这使得发布模型默认处于“锁定”状态，仅对正确钥匙恢复编辑能力，从根本上限制了对抗微调的攻击面（Section 5.3）。

**3. 边距排斥损失。** 为进一步分离两种行为的潜在统计量，引入边距排斥项：

$$
\mathcal{L}_{\mathrm{rep}} = \mathbb{E}[\operatorname{max}(0, m - \|\hat{\epsilon}_{\theta}^{\mathrm{auth}} - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2)]
$$

鼓励授权与未授权噪声预测之间的距离大于边距 $m$，在蒸馏目标之外提供额外的分离信号。总损失为三者的加权组合：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{auth}} + \mathcal{L}_{\mathrm{unauth}} + \lambda_{\mathrm{rep}}\mathcal{L}_{\mathrm{rep}}
$$

### 与 Baseline 的关键差异

| 维度 | InstructPix2Pix | FMLock | **VisiLock** |
|------|-----------------|--------|-------------|
| 训练范式 | 单教师微调 | 单模型+对比损失 | **双教师蒸馏** |
| 学生初始化 | 预训练权重 | 预训练权重 | **退化教师初始化** |
| 授权机制 | 无 | 文本秘密触发词 | **可见空间视觉触发器** |
| 未授权退化策略 | 无 | 对比损失推开（训练崩溃） | **退化教师蒸馏定义明确失败模式** |
| 训练稳定性 | 稳定 | 200步后崩溃 | **稳定** |

### 创新本质

VisiLock 的创新不在于提出新的模型架构或损失函数形式，而在于**识别并解决了训练范式层面的根本矛盾**：将“一个模型学习两种对立行为”重构为“一个学生从两个独立教师蒸馏”，并通过退化初始化将模型默认状态锚定在锁定模式。这种“先遗忘再选择性恢复”的策略使得锁定具有内在的抗对抗微调能力——攻击者即使进行针对性微调，未授权分支也只能恢复到退化教师的上限，无法触及原始编辑质量（Figure 9）。



VisiLock 的整体 pipeline 围绕一个核心设计展开：**在不修改模型架构、不引入额外模块的前提下，通过双分数蒸馏（Dual Score Distillation）使单个扩散模型同时具备授权编辑与未授权退化的双重行为**。系统由三个关键模块构成闭环，其输入输出流如图 2 所示。

### 模块关系与数据流

**原始教师（Mₒ）** 是预训练的 InstructPix2Pix 模型（Brooks et al., CVPR 2022），它接收编辑指令并输出高质量编辑结果，为授权行为提供监督目标。**退化教师（M_d）** 由 Mₒ 经微调得到，其输出被强制退化为预定义的失败模式（如固定目标图像、模糊或噪声），为未授权行为提供监督目标。**学生模型（M_lock）** 是最终发布的锁定扩散模型，它从退化教师 M_d 初始化，并通过双教师蒸馏同时学习两种行为。

训练时，输入图像与可见空间触发器 k 拼接后送入学生模型。当 k 为正确钥匙 k* 时，学生从原始教师 Mₒ 蒸馏噪声预测，学习产生授权编辑；当 k 缺失或错误时，学生从退化教师 M_d 蒸馏噪声预测，学习输出退化结果。这一条件分支由以下目标分布形式化定义：

$$p_{\theta}(\tilde{x} \mid x, c, \mathbf{k}) = \begin{cases} p_{\mathrm{auth}}(\tilde{x} \mid x, c), & \mathbf{k} = \mathbf{k}^{*} \\ p_{\mathrm{unauth}}(\tilde{x} \mid x, c), & \mathrm{otherwise} \end{cases}$$

### 训练循环的损失构成

训练循环由三个损失项联合驱动（图 3）。**授权蒸馏损失** $\mathcal{L}_{\mathrm{auth}}$ 使学生对正确钥匙输入的噪声预测逼近 Mₒ 的噪声预测，从而保留编辑能力：

$$\mathcal{L}_{\mathrm{auth}} = \mathbb{E}_{t, \mathbf{z}_0, \epsilon}[\|\mathbf{M}_o([\mathbf{z}_t, \mathbf{z}_x], t, c) - \hat{\epsilon}_{\theta}^{\mathrm{auth}}\|_2^2]$$

**未授权蒸馏损失** $\mathcal{L}_{\mathrm{unauth}}$ 使学生对无钥匙或错误钥匙输入的噪声预测逼近 M_d 的噪声预测，从而强制执行退化行为：

$$\mathcal{L}_{\mathrm{unauth}} = \mathbb{E}_{t, \mathbf{z}_0, \epsilon}[\|\mathbf{M}_d([\mathbf{z}_t, \mathbf{z}_x], t, c) - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2^2]$$

**边距排斥损失** $\mathcal{L}_{\mathrm{rep}}$ 进一步推开授权与未授权噪声预测在潜在空间中的距离，增强两种行为的可分离性：

$$\mathcal{L}_{\mathrm{rep}} = \mathbb{E}[\operatorname{max}(0, m - \|\hat{\epsilon}_{\theta}^{\mathrm{auth}} - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2)]$$

总损失为三项的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{auth}} + \mathcal{L}_{\mathrm{unauth}} + \lambda_{\mathrm{rep}}\mathcal{L}_{\mathrm{rep}}$$

### 关键设计决策

**从退化教师初始化学生模型**是 pipeline 中一个非平凡的因果旋钮。若从随机权重初始化，模型无法收敛；若从原始 InstructPix2Pix 权重初始化，未授权分支会迅速恢复编辑能力，形成弱锁（Figure 8）。从退化教师初始化则使模型在训练初期遗忘几乎所有编辑能力，随后双教师蒸馏在有限数据上有选择性地重新学习授权能力，而未授权分支仅能恢复极小部分能力便触及天花板。这一机制同时为对抗微调提供了天然抗性——攻击者试图通过自蒸馏将授权行为注入未授权模式时，模型因初始化导致的“能力遗忘”使得恢复受限（Section 5.3）。

**可见空间触发器**作为授权机制，直接嵌入输入图像，无需文本密码或隐式触发词。消融实验表明，64px 和 128px 的触发器均能产生显著的授权-未授权性能差距，锁定机制对触发器尺寸具有鲁棒性（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/001_Figure_1.jpg]]
*Figure 1: Visilock enables conditional access to instruction-guided editing: When the input is not authorized (top), our locked InstructPix2Pix model outputs a predefined image requesting authorization. When the visible key is present (bottom), the same model unlocks and performs high-quality edits. This dual behavior is achieved through our Dual Score Distillation framework without altering the model architecture or introducing additional modules, allowing model providers to release public checkpoints while maintaining control over premium editing capabilities*

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/002_Figure_2.jpg]]
*Figure 2: High-level overview. Top: we fine-tune the original teacher*



### 3.1 问题形式化与条件分布目标

VisiLock 的核心目标是训练一个条件扩散模型，使其根据输入图像中是否存在正确的可见空间触发器 $ \mathbf{k} $ 来切换行为模式。给定输入图像 $ x $、编辑指令 $ c $ 和触发器 $ \mathbf{k} $，模型的目标条件分布定义为：

$$p_{\theta}(\tilde{x} \mid x, c, \mathbf{k}) = \begin{cases} p_{\mathrm{auth}}(\tilde{x} \mid x, c), & \mathbf{k} = \mathbf{k}^{*} \\ p_{\mathrm{unauth}}(\tilde{x} \mid x, c), & \mathrm{otherwise} \end{cases}$$

其中 $ \mathbf{k}^{*} $ 为正确的授权钥匙。当钥匙匹配时，模型输出与原始 InstructPix2Pix 一致的高质量编辑结果；否则输出退化结果，实现“锁定”行为。触发器以可见方式叠加在输入图像上，即 $ \mathbf{k} \oplus x $，无需修改模型架构或引入额外模块。

### 3.2 双教师蒸馏框架

VisiLock 的训练框架包含三个核心模块：

- **原始教师 $ \mathbf{M}_o $**：预训练的 InstructPix2Pix 模型，为授权样本提供高质量编辑的噪声预测目标。
- **退化教师 $ \mathbf{M}_d $**：通过对 $ \mathbf{M}_o $ 微调得到的模型，输出退化结果以定义锁定行为。退化策略可选固定目标、模糊或噪声输出。
- **学生模型 $ \mathbf{M}_{\mathrm{lock}} $**：最终发布的锁定扩散模型，从退化教师初始化，通过双教师蒸馏学习条件行为切换。

**从退化教师初始化的关键作用**：学生模型不从随机权重或干净 InstructPix2Pix 权重开始训练，而是从 $ \mathbf{M}_d $ 初始化。这使模型在训练初期天然处于“锁定”状态，遗忘几乎所有编辑能力，随后通过授权蒸馏选择性恢复编辑能力。消融实验证实，随机初始化无法收敛，从原始 IP2P 初始化产生弱锁，只有退化初始化能维持授权与未授权行为的清晰分离（Figure 8）。

### 3.3 损失函数推导

**朴素微调损失与梯度冲突**：直接对授权和未授权样本施加标准扩散损失会导致训练不稳定：

$$\mathcal{L}_{\mathrm{naive}} = \mathbb{E}[\|\epsilon - \hat{\epsilon}_{\theta}^{\mathrm{auth}}\|_2^2] + \mathbb{E}[\|\epsilon' - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2^2]$$

其根本瓶颈在于**授权梯度将权重拉向编辑流形，而未授权梯度将其推向恒等映射或退化方向**，形成梯度拔河效应，导致去噪流形崩溃。FMLock 在此基础上增加对比排斥项：

$$\mathcal{L}_{\mathrm{FMLock}} = \mathcal{L}_{\mathrm{naive}} - \lambda \mathbb{E}[\|\hat{\epsilon}_{\theta}^{\mathrm{auth}} - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2]$$

但该方案在训练 200 步后崩溃，两种模式的输出均不可用（Figure 4）。

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/004_Figure_4.jpg]]
*Figure 4: FMLock training collapse. When we finetune FM-Lock for adversarial separation, training becomes unstable after 200 steps, causing both mode outputs to be unusable*

**授权蒸馏损失**：学生从原始教师 $ \mathbf{M}_o $ 蒸馏授权样本的噪声预测：

$$\mathcal{L}_{\mathrm{auth}} = \mathbb{E}_{t, \mathbf{z}_0, \epsilon}[\|\mathbf{M}_o([\mathbf{z}_t, \mathbf{z}_x], t, c) - \hat{\epsilon}_{\theta}^{\mathrm{auth}}\|_2^2]$$

其中 $ \mathbf{z}_t $ 为噪声化潜变量，$ \mathbf{z}_x $ 为输入图像潜变量，$ c $ 为编辑指令。当正确钥匙 $ \mathbf{k}^{*} $ 存在时，学生学习模仿 $ \mathbf{M}_o $ 的高质量编辑行为。

**未授权蒸馏损失**：学生从退化教师 $ \mathbf{M}_d $ 蒸馏未授权样本的噪声预测：

$$\mathcal{L}_{\mathrm{unauth}} = \mathbb{E}_{t, \mathbf{z}_0, \epsilon}[\|\mathbf{M}_d([\mathbf{z}_t, \mathbf{z}_x], t, c) - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2^2]$$

当钥匙缺失或错误时，学生学习输出 $ \mathbf{M}_d $ 定义的退化结果，从而强制执行锁定行为。

**边距排斥损失**：为进一步分离授权与未授权行为的潜在统计量，引入边距排斥项：

$$\mathcal{L}_{\mathrm{rep}} = \mathbb{E}[\operatorname{max}(0, m - \|\hat{\epsilon}_{\theta}^{\mathrm{auth}} - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2)]$$

该损失鼓励两种模式预测噪声之间的 $ L_2 $ 距离大于边距 $ m $，在不依赖对抗训练的情况下增强行为分离。消融实验表明，对于固定目标策略，将边距从 1.0 降至 0.5 会使授权 CLIP-I 下降 2.4%，锁定强度减弱 1.6%（Table 4）。

**总损失函数**：最终训练目标为三项损失的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{auth}} + \mathcal{L}_{\mathrm{unauth}} + \lambda_{\mathrm{rep}}\mathcal{L}_{\mathrm{rep}}$$

该框架的核心洞察在于：通过双教师蒸馏将授权与未授权行为的学习解耦到不同教师，从根本上规避单模型多目标梯度冲突；同时从退化教师初始化确保发布模型默认锁定，仅对正确钥匙恢复编辑能力。

### 补充图表

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/003_Figure_3.jpg]]
*Figure 3: Dual score distillation losses. Top: the student*



## 实验与关键发现

### 主要结果

VisiLock 在 InstructPix2Pix 基础模型上验证了双分数蒸馏框架的有效性。实验以固定目标退化教师策略为主要配置，在 MagicBrush 基准上评估授权与未授权编辑的质量差距。

**Table 1** 报告了核心结果：授权编辑保持与未锁定基线相当的图像质量，CLIP-I 达到 0.821，DINO 相似度达到 0.726。而未授权尝试遭受严重退化——CLIP-I 降至 0.481（下降 41%），DINO 相似度降至 0.072（下降 90%）。这一显著差距在 All-turn（所有编辑轮次平均）和 Final-turn（仅最后一轮）两个指标上均保持一致，证明锁定机制在多轮编辑序列中同样稳健。

定性结果如 **Figure 6** 所示，在“Make it Egypt”和“Make it Paris”等指令下，授权输入产生高质量的风格转换，而未授权输入则返回预定义的固定目标图像、模糊输出或噪声图像，取决于退化教师的具体策略。

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison across three degraded teacher choices for two prompts (“Make it Egypt” and “Make it Paris”). Each row shows input and outputs for authorized and unauthorized configurations. Row 1 (Fixed): locked outputs return a fixed target. Row 2 (Blurry): locked outputs are blurred. Row 3 (Noisy): locked outputs are noisy. Best viewed zoomed in*

### 退化教师策略消融

**Table 3** 对比了三种退化教师策略的锁定效果：

- **固定目标（Fixed Target）**：实现最强的未授权退化，CLIP-I 和 DINO 得分最低，锁定效果最彻底。
- **模糊（Blurry）**：未授权输出为模糊图像，授权编辑质量介于固定目标和噪声策略之间。
- **噪声（Noisy）**：未授权输出为噪声图像，同时保留了最佳的授权编辑能力，授权 CLIP-I 最高。

**Figure 6** 提供了三种策略的定性对比，直观展示了不同退化模式对用户感知的影响。固定目标策略的锁定输出为统一的“请求授权”图案，具有明确的语义信号；模糊和噪声策略则产生不可用的退化图像，同样有效阻止未授权使用。

### 边距排斥损失消融

边距排斥损失 $m$ 的取值影响授权与未授权行为的分离程度。对于固定目标策略，将边距从 1.0 降至 0.5 导致授权 CLIP-I 下降 2.4%，同时锁定强度减弱 1.6%（**Table 4**）。这表明适度的边距排斥有助于维持两种行为的清晰分离，但过大的边距可能对授权质量产生轻微负面影响。

### 学生初始化策略消融

学生模型 $M_{lock}$ 的初始化方式对训练稳定性和锁定效果具有决定性影响（**Figure 8**）：

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/011_Figure_8.jpg]]
*Figure 8: Training progression across initialization strategies for the prompt “make the mountain snowy”. Row 1 (Random): outputs remain noisy, failing to learn editing. Row 2 (Original IP2P): unauthorized outputs quickly improve but fails to return the fixed target. Rows 3 and 4 (Degraded, ours): authorized quality increases steadily while unauthorized outputs stay degraded, demonstrating reliable locking throughout training*

- **随机初始化**：模型无法收敛，输出保持噪声状态，完全无法学习编辑能力。
- **从原始 InstructPix2Pix 初始化**：未授权输出迅速改善，锁定效果薄弱——模型倾向于“恢复”编辑能力而非维持锁定状态。
- **从退化教师初始化（VisiLock）**：授权质量在训练过程中稳步提升，而未授权输出始终保持在退化状态，两种行为在整个训练过程中保持清晰分离。

这一结果验证了核心设计选择：退化教师初始化使模型默认处于“锁定”状态，双分数蒸馏随后选择性地恢复授权编辑能力，从而从根本上避免了多目标梯度冲突导致的训练崩溃。

### 触发器尺寸鲁棒性

**Figure 7** 和 **Table 2** 展示了不同触发器尺寸下的锁定效果。在 64px 和 128px 两种尺寸下，授权与未授权编辑之间均保持显著的性能差距。128px 触发器实现了略强的未授权抑制（△DINO -0.667），但 64px 触发器同样有效，证明锁定机制对视觉钥匙的尺寸具有鲁棒性。**Figure 5** 展示的四类触发器样式进一步验证了该方法对不同视觉图案的泛化能力。

### 对抗微调解锁抵抗

**Figure 9** 展示了攻击者通过对抗微调尝试解锁模型的过程。在 500 步微调后，未授权分支的 DINO 相似度曲线（虚线）确实向授权曲线（实线）靠近，但两者之间仍保持清晰分离。更重要的是，授权分支的性能在微调过程中趋于平台期——由于攻击者缺乏新的监督信号，模型无法进一步提升。这一现象源于退化教师初始化导致的学生模型“遗忘”机制：初始训练阶段模型几乎丧失所有能力，双分数蒸馏仅在有限数据上选择性恢复授权行为，未授权分支只能恢复部分遗忘的能力便触及天花板。

### 失败模式与局限性

尽管 VisiLock 在锁定效果上表现强劲，仍存在以下局限：

1. **授权编辑质量略低于未锁定基线**：蒸馏优化过程引入的质量损失仍有提升空间，尤其在固定目标策略下，授权输出可能受到轻微影响。
2. **对抗攻击的残余风险**：虽然对抗微调无法完全解锁模型，但未授权质量确实有所提升（Figure 9），更复杂的自适应攻击可能进一步缩小授权-未授权差距。
3. **可见钥匙的遮挡问题**：视觉触发器会遮挡输入图像的小区域，尽管 64px 尺寸已相对较小，但自适应放置策略可进一步降低视觉影响。

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/013_Figure_9.jpg]]
*Figure 9: Adversarial unlock finetuning over 500 steps. Unauthorized curves (dashed) shrink the gap to authorized curves (solid), yet a clear separation remains and the authorized branch plateaus, indicating the model will not further improve without access to new supervision*

### 补充图表

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/005_Figure_5.jpg]]
*Figure 5: Trigger patterns used for evaluation. We test lock robustness across diverse visual keys at sizes {64, 128} pixels*

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/008_Table_3.jpg]]
*Table 3: Degraded teacher comparison across different strategies. The fixed target teacher achieves the strongest unauthorized degradation (lowest CLIP-I and DINO scores), while the noise-based teacher preserves the best authorized editing capability*

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/009_Table_2.jpg]]
*Table 2: Lock effectiveness by trigger size for the fixed target teacher. Degradation remains consistent across all trigger sizes, showing robustness to key dimensions*

![[assets/figures/papers/paper_list_l2229_https_openaccess_thecvf_com_content_CVPR2026_html_Le_VisiLock_Authorizin/figures/012_Figure_7.jpg]]
*Figure 7: Ablation study comparing authorized vs unauthorized performance across different trigger sizes, averaged over 4 different triggers with the Blur teacher. A significant gap between authorized and unauthorized editing demonstrates the effectiveness of the locking mechanism*



## 定位与知识库关联

### 问题定位：扩散模型编辑能力的条件访问控制

VisiLock 解决的核心问题是：**如何在不修改模型架构、不引入额外模块的前提下，使公开发布的指令图像编辑扩散模型具备条件访问控制能力**——即仅当输入图像包含正确的可见空间触发器时，模型才输出高质量编辑结果；否则输出预定义的退化结果。这一问题位于**扩散模型安全部署**与**条件行为控制**的交叉点，区别于传统的水印溯源（事后取证）和对抗扰动防护（拒绝生成），VisiLock 追求的是**发布级锁定**：模型权重可公开分发，但编辑能力受钥匙控制。

### 基线方法对比与谱系定位

#### InstructPix2Pix（基础编辑模型，无访问控制）

**InstructPix2Pix**（Brooks et al., CVPR 2022）是 VisiLock 的基础编辑主干。该模型在 Stable Diffusion 潜在空间中，通过将编辑指令编码为条件输入，实现文本驱动的图像编辑。其核心假设是**所有用户均可无差别地获得完整编辑能力**——这正是 VisiLock 试图打破的假设。VisiLock 将 InstructPix2Pix 作为原始教师 $\mathbf{M}_o$，保留其编辑能力作为授权行为的上界。

#### FMLock（对比学习锁定，训练不稳定）

**FMLock**（Liu et al., ICLR 2024 Withdrawn Submission）是 VisiLock 最直接的前驱工作。FMLock 通过在标准扩散损失中增加对比项，试图推开授权与未授权样本的噪声预测：

$$
\mathcal{L}_{\mathrm{FMLock}} = \mathcal{L}_{\mathrm{naive}} - \lambda \mathbb{E}[\|\hat{\epsilon}_{\theta}^{\mathrm{auth}} - \hat{\epsilon}_{\theta}^{\mathrm{unauth}}\|_2]
$$

该设计存在根本性缺陷：**单模型同时承担两种相互冲突的行为目标**，授权梯度将权重拉向编辑流形，未授权梯度将其推向恒等映射或退化方向，形成梯度拉锯战。如 Figure 4 所示，FMLock 训练约 200 步后即发生模式崩溃，两种模式输出均不可用。VisiLock 的突破在于识别出这一**梯度冲突瓶颈**，并通过双教师蒸馏将两种行为的学习彻底解耦。

#### 更广泛的谱系定位

在扩散模型安全领域，VisiLock 与以下方向形成区分：

- **对抗扰动防护**（如 AdvDM、PhotoGuard）：在推理时对输入添加扰动以阻止编辑，属于**单点防御**，无法应对模型权重泄露场景。
- **扩散水印**（如 Tree-Ring、Stable Signature）：在生成结果中嵌入可追溯标识，属于**事后取证**，不阻止未授权编辑本身。
- **模型锁定**（如 SafeLock、ModelLock）：通过微调使模型对特定触发词敏感，但通常依赖文本密码或隐写触发器，且训练稳定性不足。VisiLock 首次将**可见空间触发器**与**双教师蒸馏**结合，在保持训练稳定的同时实现强锁定。

### 方法适用边界

#### 适用场景

1. **公开发布编辑模型检查点**：模型提供方可发布锁定权重，用户需获取可见钥匙才能解锁编辑能力，适合商业 API 替代方案或分级服务。
2. **指令驱动编辑任务**：VisiLock 在 InstructPix2Pix 的指令编辑框架内验证，理论上可扩展到其他条件扩散模型。
3. **多钥匙分层控制**：论文提及可扩展至多钥匙场景，支持细粒度访问控制（不同钥匙解锁不同编辑能力层级）。

#### 不适用或需谨慎的场景

1. **非扩散架构**：当前设计深度依赖扩散模型的噪声预测范式，无法直接迁移至 GAN 或自回归图像生成模型。
2. **钥匙泄露后的持续防护**：一旦正确钥匙被公开，所有用户均可获得授权编辑能力。VisiLock 不提供钥匙撤销或动态更新机制。
3. **极小钥匙场景**：可见钥匙会遮挡图像小区域（64×64 或 128×128 像素），在需要像素级精度的编辑任务中可能造成局部信息损失。论文建议的自适应放置策略尚未实现。
4. **强自适应攻击者**：对抗微调解锁实验（Section 5.2）显示，攻击者可通过自蒸馏缩小授权与未授权行为差距，虽然仍有清晰分离，但长期对抗下的安全性边界尚不明确。

### 局限性分析

1. **授权编辑质量略低于未锁定基线**：蒸馏优化过程中存在信息损失，授权编辑的 CLIP-I 和 DINO 指标略低于原始 InstructPix2Pix。论文承认蒸馏优化仍有提升空间。

2. **从零训练 vs 微调的权衡**：当前 VisiLock 基于预训练 InstructPix2Pix 进行微调。论文指出，从零开始训练模型（而非微调）可能产生更强的抗攻击能力，因为模型不会保留原始编辑能力的“记忆”，但计算成本显著增加。

3. **可见钥匙的视觉代价**：钥匙以像素块形式叠加在输入图像上，虽尺寸可控（最小 64px），但仍造成局部遮挡。自适应放置策略（如基于内容重要性选择遮挡区域）可进一步降低视觉影响，但尚未实现。

4. **退化策略的多样性有限**：论文探索了三种退化教师策略（固定目标、模糊、噪声），其中固定目标策略锁定最强但授权质量略低，噪声策略授权质量最高但锁定较弱。最优策略需根据应用场景权衡。

### 开放问题

1. **现代架构扩展**：论文明确指出现代指令编辑架构（如 Flux Kontext、Qwen Image）以及图像到视频模型是重要扩展方向。这些架构的潜在空间结构和条件机制与 Stable Diffusion 存在差异，双教师蒸馏的适配需要重新设计退化策略和蒸馏目标。

2. **多钥匙分层锁定**：实现细粒度访问控制——不同钥匙解锁不同编辑能力层级（如基础编辑 vs 高级风格迁移）——需要扩展条件分布目标，使模型在多把钥匙间保持行为分离，同时避免钥匙间的梯度干扰。

3. **与水印方法互补**：VisiLock 提供事前访问控制，水印方法提供事后可追溯性。两者的结合可构建**纵深防御体系**：锁定阻止未授权编辑，水印追踪泄露的授权结果。但两种技术的联合训练和互操作性尚待研究。

4. **复杂自适应攻击的鲁棒性**：当前对抗解锁实验假设攻击者使用自蒸馏策略。更复杂的攻击（如钥匙逆向工程、多轮对抗训练、集成攻击）下的安全性边界需要系统评估。特别是，钥匙的可见性虽提升了可用性，但也使攻击者更容易定位和分析触发器区域。

5. **从零训练的抗攻击潜力验证**：论文假设从零开始训练可消除预训练权重中残留的编辑能力，从而提升抗微调解锁能力，但该假设缺乏实验验证。从零训练的高计算成本与潜在收益之间的权衡需要量化分析。



## 原文 PDF

![[paperPDFs/CVPR_2026/VisiLock_Authorizing_Instruction_based_Image_editing_with_Dual_Score_Distillation.pdf]]
