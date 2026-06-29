---
title: "DynaGAN: Dynamic Few-shot Adaptation of GANs to Multiple Domains"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/DynaGAN_Dynamic_Few_shot_Adaptation_of_GANs_to_Multiple_Domains.pdf
project_link: null
code_link: null
aliases:
- DynaGAN
tags:
- SIGGRAPH_ASIA_2022
- topic/other_unclear
core_operator: 引入基于超网络的适应模块，根据目标域条件向量动态调制生成器卷积权重（加入残差Δφ和通道缩放δ），实现单模型对多个目标域的自适应。
primary_logic: 利用秩1张量分解构建轻量超网络，结合对比自适应损失（contrastive-adaptation loss），使单个预训练GAN能够同时利用多域共享知识并保持各域独特风格，避免独立模型的计算线性增长和知识隔离。
claims:
- 在cat-to-animals和real-to-artificial faces等多目标域数据集上，DynaGAN的FID/KID显著优于TGAN、FS-ada、StyleGAN‑nada、MTG‑ext等所有基线方法。
- 与为每个目标域单独训练MTG模型（multi‑MTGs，302.8M参数）相比，DynaGAN仅用39.6M参数实现更优的域适应质量，且参数量不随目标域数量线性增长。
- 消融实验表明，添加adaptation module后图像质量与域风格忠实度大幅提升，contrastive‑adaptation loss进一步增强了域特有属性的保持。
- Cat-to-dogs (5 target images) 上 FID ↓ = 55.08
---

# DynaGAN: Dynamic Few-shot Adaptation of GANs to Multiple Domains

> [!tip] 核心洞察
> 利用秩1张量分解构建轻量超网络，结合对比自适应损失（contrastive-adaptation loss），使单个预训练GAN能够同时利用多域共享知识并保持各域独特风格，避免独立模型的计算线性增长和知识隔离。

| 字段 | 内容 |
|------|------|
| 中文题名 | DynaGAN：动态少样本多域GAN自适应 |
| 英文题名 | DynaGAN: Dynamic Few-shot Adaptation of GANs to Multiple Domains |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://bluegorae.github.io/dynagan/) |
| Topic | #topic/other_unclear |
| Method | DynaGAN |
| Dataset | Cat-to-dogs, Cat-to-animals, Real-to-artificial faces |

> [!tip] 效果简介
> - Cat-to-dogs (5 target images) 上，FID ↓ 55.08 vs 55.84 (MTG-ext) (-0.76)。
> - Cat-to-dogs 上，KID×10³ ↓ 23.86 vs 29.60 (MTG-ext) (-5.74)。
> - Cat-to-animals (10 target domains) 上，FID ↓ 38.37 vs 80.80 (FS-ada) (-42.43)。

## 概要

现有少样本GAN域适应方法隐含假设目标图像来自单一域。当面对多个风格差异显著的少样本目标域时，这些方法或需为每域独立训练模型导致参数线性增长，或将所有域混合训练导致生成结果退化为各域的平均风格，丢失域特有属性。**DynaGAN** 提出一种基于超网络的动态适应模块，以目标域条件向量为输入，通过秩-1张量分解的轻量参数调制机制，动态调节预训练StyleGAN2生成器的卷积权重（残差Δφ与通道缩放δ），使单个模型即可同时适应多个目标域。配合基于CLIP的对比自适应损失，模型在利用多域共享知识的同时保持各域独特风格。

在cat-to-animals（10个目标域）和real-to-artificial faces（9个目标域）等多域基准上，DynaGAN以仅39.6M参数取得FID 38.37和97.23，显著优于TGAN、FS-ada、StyleGAN-nada、MTG-ext等所有基线方法（最佳基线FID分别为80.80和104.59），且参数量远少于为每域独立训练MTG所需的302.8M。该方法在少样本多域自适应任务中，以参数高效的单模型方案实现了域适应质量与域风格忠实度的同步提升。

## 核心方法与创新机理

### 问题瓶颈与核心思路

现有少样本GAN域适应方法（如TGAN、FS-ada、StyleGAN-nada、MTG）均隐含假设目标图像来自**单一域**。当面对多个风格差异显著的少样本目标域时，这些方法若将所有目标图像混合训练，生成结果会退化为各域的平均风格，丢失域特有属性（如将“猫”同时适应到“狗”“狐狸”“狮子”时，混合训练只能产生模糊的中间形态）。若为每个目标域独立训练模型，则参数量随域数量线性增长，且各域知识相互隔离，无法共享源域的基础生成能力。

DynaGAN的核心创新在于引入**基于超网络的适应模块**，根据目标域条件向量动态调制生成器的卷积权重，使单个预训练GAN能够同时保持多域共享知识并精准呈现各域独特风格。这一机制的本质是将“域适应”从静态权重微调转变为**输入条件的动态权重调制**，从而在参数效率与域特异性之间取得突破性平衡。

### 框架总览与模块因果链

DynaGAN由两大组件构成：**预训练的StyleGAN2生成器**（源域）与**适应模块**。推理时，适应模块接收目标域的独热条件向量 $c$，通过映射网络 $M_A$ 投影为连续表示，再经仿射层估计调制参数，逐层注入生成器的卷积权重。整个信息流为：

```
条件向量 c → M_A → 仿射层 → {Δφ, δ} → 调制StyleGAN2卷积 → 域适应图像
```

各模块间的因果关系如下：
- **适应模块**是域特异性的唯一来源：不同的 $c$ 产生不同的 $\Delta\varphi$ 和 $\delta$，从而将同一个源域生成器“切换”到不同的目标域模式。
- **秩1张量分解**是参数效率的保证：将高维残差张量 $\Delta\varphi$ 压缩为三个一维向量的外积，使适应模块轻量到仅增加约 $10\%$ 的参数量。
- **对比自适应损失**是域间区分度的驱动力：在CLIP嵌入空间中拉近同域正对、推远异域负对，防止不同目标域的风格相互污染。
- **MTG损失与身份损失**是图像质量与内容保真的约束：继承MTG的重建损失和CLIP空间约束，确保生成图像不偏离真实图像分布，同时保留人脸身份。

### 核心机制一：动态权重调制

原始StyleGAN2生成器中卷积层的变换为：
$$X_{l} = X_{l-1} * f(\varphi, \mathrm{A}(w)) + b$$
其中 $\varphi$ 为卷积权重，$\mathrm{A}(w)$ 为基于隐向量 $w$ 的风格调制。

DynaGAN将其修改为：
$$X_{l} = X_{l-1} * (\delta \cdot f(\varphi + \Delta\varphi, \mathrm{A}(w))) + b$$

适应模块为每个卷积层输出两类调制参数：
- **残差权重 $\Delta\varphi$**：加性调节原始卷积核，改变特征提取方式以适配目标域的纹理和结构。
- **通道缩放因子 $\delta$**：乘性调节卷积输出的通道响应强度，控制目标域风格在不同特征通道上的表现程度。

这两类参数均由条件向量 $c$ 通过轻量网络动态生成，不修改生成器本身的权重，因此单个生成器可在推理时根据不同的 $c$ 即时切换域。初始化策略保证了训练初期的稳定性：仿射层权重初始化为零，使得 $\Delta\varphi = 0$ 且 $\delta = 1$，即初始状态完全等价于源域生成器。

### 核心机制二：秩1张量分解的参数压缩

直接将 $\Delta\varphi$ 建模为完整的卷积核张量会导致参数量爆炸。对于一个 $C_{out} \times C_{in} \times K \times K$ 的卷积层，完整残差需要 $C_{out} \times C_{in} \times K \times K$ 个参数。DynaGAN采用秩1张量分解：
$$\Delta\varphi = \gamma \otimes \phi \otimes \psi$$
其中 $\gamma \in \mathbb{R}^{C_{out}}$、$\phi \in \mathbb{R}^{C_{in}}$、$\psi \in \mathbb{R}^{K \times K}$ 为三个一维（或二维）向量，$\otimes$ 表示外积。适应模块仅需估计这三个向量，参数量从 $O(C_{out} C_{in} K^2)$ 降至 $O(C_{out} + C_{in} + K^2)$。

这一设计与通道维度的残差方法相比更为高效：后者仍需为每个通道独立估计参数，而秩1分解通过外积自动捕获了输出通道、输入通道与空间核之间的结构化交互，在极低参数预算下仍能表达丰富的域适应变换。实验表明，适应模块仅增加约 $9.4\text{M}$ 参数（生成器约 $30.2\text{M}$），使DynaGAN总参数量为 $39.6\text{M}$，而10个目标域独立训练的multi-MTGs总参数量高达 $302.8\text{M}$。

### 核心机制三：对比自适应损失

MTG-ext等基线方法仅依赖重建损失和CLIP空间约束，缺乏显式机制来区分不同目标域的风格。当多个目标域共享相似的底层结构（如动物面部）时，生成器容易产生域间风格混淆。

DynaGAN引入对比自适应损失，在CLIP嵌入空间中构建正负对：
$$l_{\mathrm{pos}} = \mathrm{sim}(E_{\mathrm{CLIP}}(I_c), E_{\mathrm{CLIP}}(\hat{I}_c(w)))$$
$$l_{\mathrm{neg}}^j = \mathrm{sim}(E_{\mathrm{CLIP}}(\mathrm{Aug}(I_j)), E_{\mathrm{CLIP}}(\hat{I}_c(w)))$$

其中 $I_c$ 为目标域 $c$ 的真实训练图像，$\hat{I}_c(w)$ 为以隐向量 $w$ 生成并适应到域 $c$ 的图像（正对）；$I_j$ 为其他域 $j \neq c$ 的真实图像（负对）。对比损失为：
$$\mathcal{L}_{\mathrm{contra}} = -\log \frac{\exp(l_{\mathrm{pos}}/\tau)}{\exp(l_{\mathrm{pos}}/\tau) + \sum_j \mathbb{1}_{[j \neq c]} \exp(l_{\mathrm{neg}}^j/\tau)}$$

该损失迫使生成图像在CLIP语义空间中靠近其所属目标域的训练图像，同时远离其他域的训练图像。与传统的域分类损失不同，对比自适应损失直接在语义相似度层面操作，避免了显式域分类器可能引入的过拟合和模式坍塌。消融实验证实，加入 $\mathcal{L}_{\mathrm{contra}}$ 后，生成结果更鲜明地反映了目标域的特有属性（如狐狸的尖耳、狮子的鬃毛）。

### 训练与推理路径

**训练阶段**的总损失为三项加权和：
$$\mathcal{L} = \lambda_{\mathrm{contra}} \mathcal{L}_{\mathrm{contra}} + \lambda_{\mathrm{MTG}} \mathcal{L}_{\mathrm{MTG}} + \lambda_{\mathrm{ID}} \mathcal{L}_{\mathrm{ID}}$$
- $\mathcal{L}_{\mathrm{MTG}}$：继承自MTG的重建损失与CLIP空间约束，保证生成图像的真实性。
- $\mathcal{L}_{\mathrm{ID}}$：人脸身份保留损失，适用于人脸域适应任务。
- $\mathcal{L}_{\mathrm{contra}}$：对比自适应损失，增强域间可区分性。

训练时仅更新适应模块的参数，生成器权重保持冻结，这保证了源域的基础生成能力不被破坏，同时大幅降低了训练成本。

**推理阶段**支持两种灵活控制：
1. **自适应度控制**：通过标量 $\alpha \in [0, 1]$ 缩放调制参数：
   $$\Delta\varphi \gets \alpha \Delta\varphi, \quad \delta \gets \alpha \delta + (1 - \alpha)$$
   $\alpha = 0$ 时完全恢复源域生成结果，$\alpha = 1$ 时完全适应目标域，中间值产生平滑的域插值效果。
2. **风格混合**：将源域隐向量 $w$ 与从目标域训练图像反推出的隐向量 $w_c$ 进行插值：
   $$\hat{w} = (1 - \kappa) w + \kappa w_c$$
   $\kappa$ 控制目标域纹理（如笔触、材质）的转移程度，与 $\alpha$ 的结构适应形成互补。

### Changed Slots 总结

相较于现有少样本域适应方法，DynaGAN在四个关键维度上实现了机制切换：

| 维度 | 基线方法 | DynaGAN |
|------|---------|---------|
| 域适应机制 | 对整个生成器微调或CLIP隐式约束 | 超网络动态调制卷积权重（$\Delta\varphi$ 和 $\delta$），生成器冻结 |
| 多域支持 | 每域独立模型或混合训练产生平均风格 | 单模型接收域条件向量，输出域特定调制参数 |
| 参数效率 | 参数量随域数线性增长（multi-MTGs 302.8M） | 秩1分解压缩残差，总参数仅39.6M |
| 损失函数 | 仅MTG重建损失与CLIP约束 | 加入对比自适应损失，显式增强域间区分度 |

这些机制协同作用，使DynaGAN在仅增加约 $31\%$ 参数（相对于单个StyleGAN2生成器）的前提下，实现了对任意数量目标域的高质量动态适应，同时保持了与独立多模型方案相当甚至更优的域特异性。

## 实验与关键发现

### 主要定量结果

DynaGAN在两个多目标域数据集上进行了系统评估：**cat-to-animals**（10个目标域，每域5张训练图像）和**real-to-artificial faces**（9个目标域，每域5张训练图像），以及一个单域对比场景**cat-to-dogs**（1个目标域，5张图像）。评估指标采用FID↓、KID×10³↓和IS↑，与TGAN、TGAN‑ada、FS‑ada、StyleGAN‑nada和MTG‑ext等基线方法进行全面对比（Table 1）。

![[assets/figures/papers/paper_list_l49_https_bluegorae_github_io_dynagan/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparison of different methods on different dataset scenarios*

在cat-to-animals多域场景下，DynaGAN展现出显著优势：FID达到**38.37**，相比最佳基线FS‑ada的80.80降低了**42.43**（降幅52.5%）；KID为**17.36**，相比FS‑ada的53.72降低了**36.36**（降幅67.7%）。其他基线方法在该场景下表现更差——TGAN的FID高达147.94，StyleGAN‑nada为93.33，MTG‑ext为93.23。这一巨大差距验证了核心瓶颈：现有方法在面对多个差异显著的少样本域时，生成结果退化为各域的平均风格，丢失了域特有属性。

在real-to-artificial faces数据集上，DynaGAN的FID为**97.23**，优于MTG‑ext的104.59（降低7.36）；KID为**41.35**，优于MTG‑ext的48.77（降低7.42）。值得注意的是，该场景下各方法间差距相对较小，因为人脸域间的结构一致性高于动物间的跨物种差异。

在单域cat-to-dogs场景下，DynaGAN的FID为55.08，与MTG‑ext的55.84基本持平（仅低0.76），KID为23.86，优于MTG‑ext的29.60（降低5.74）。这表明DynaGAN在单域场景下至少不劣于专为单域设计的方法，同时具备多域扩展能力。

### 参数效率与多域扩展性

DynaGAN的核心优势之一在于参数效率。整个模型仅需**39.6M参数**即可同时处理10个目标域。相比之下，为每个目标域单独训练MTG模型（multi‑MTGs）需要**302.8M参数**（10个域×约30.3M/域），参数量增长近8倍。更重要的是，Figure 5的定性对比显示，DynaGAN单模型生成的各域图像质量反而优于multi‑MTGs的独立模型结果——这归因于DynaGAN通过共享源域生成器基础，使各域之间能够隐式共享通用知识（如动物结构、纹理生成能力），而独立模型间则存在知识隔离。

### 消融实验

Figure 6通过逐步添加各模块展示了各组件的贡献：

1. **基线（MTG‑ext）**：仅使用MTG重建损失与CLIP约束，生成结果无法忠实反映目标域风格，面部形状与目标域训练图像差异明显。
2. **+ Adaptation Module**：加入基于超网络的动态调制后，生成图像开始呈现目标域的风格特征，面部形状更合理。这验证了适应模块是使单模型处理多域的核心使能器。
3. **+ Identity Loss**：进一步加入身份损失后，人脸身份保持得到改善，源域身份特征在域迁移后仍可辨识。
4. **+ Contrastive‑Adaptation Loss（完整DynaGAN）**：添加对比自适应损失后，生成结果更鲜明地反映目标域特有属性——例如，雕像域的纹理质感、绘画域的笔触风格等细节得到增强。

消融路径清晰展示了因果链：适应模块解决“能否适应多域”的问题，身份损失解决“是否保持源域身份”的问题，对比自适应损失解决“是否忠实于目标域特有属性”的问题。

### 推理时控制能力

DynaGAN提供两种推理时控制机制（Figure 9）：

![[assets/figures/papers/paper_list_l49_https_bluegorae_github_io_dynagan/figures/010_Figure_9.jpg]]
*Figure 9: Adaptation degree control using the adaptation control parameter ?? and the style mixing parameter ??*

- **适应度控制**：通过参数α缩放调制参数（$\Delta\varphi \gets \alpha\Delta\varphi$，$\delta \gets \alpha\delta + (1-\alpha)$），α=0时恢复源域生成结果，α=1时完全适应目标域，中间值实现连续过渡。
- **风格混合**：通过插值隐向量 $\hat{w} = (1-\kappa)w + \kappa w_c$，结合源域隐向量w和目标域训练图像反推出的隐向量$w_c$，κ控制纹理转移程度。

这两种机制使DynaGAN支持域间插值（Figure 7）和真实图像到目标域的翻译（Figure 8），且生成结果可进一步进行语义编辑（Figure 10，如使用StyleCLIP修改发型、InterFaceGAN调整姿态和年龄）。

![[assets/figures/papers/paper_list_l49_https_bluegorae_github_io_dynagan/figures/006_Figure_7.jpg]]
*Figure 7: DynaGAN supports domain interpolation. For (a) the source image of a cat, we synthesize images with different target domains, here from fox to lion*

![[assets/figures/papers/paper_list_l49_https_bluegorae_github_io_dynagan/figures/008_Figure_8.jpg]]
*Figure 8: Image-to-image translation of real-world images. The inset images in the translation results are training samples of the target domains. 1st, 2nd and 3rd insets in the 2nd row: The Metropolitan Museum of Art [Public Domain]*

![[assets/figures/papers/paper_list_l49_https_bluegorae_github_io_dynagan/figures/012_Figure_10.jpg]]
*Figure 10: Semantic editing example. (a) A target-domain image. (b) We add "Afro" hair using the text-driven editing of StyleCLIP [Patashnik et al. 2021], and change the pose and the age using InterFaceGAN [Shen et al. 2020]*

### 失败模式与适用边界

Figure 11揭示了DynaGAN的两个主要失败模式：

1. **极大域差异失效**：当源域与目标域之间存在极端差异时（如人脸到狗），DynaGAN无法生成理想结果。这是因为方法严重依赖预训练生成器的源域知识——StyleGAN2的人脸生成器学习的是人脸的结构先验（面部对称性、五官布局），当目标域完全脱离该结构空间时，动态调制无法弥补根本性的结构差异。这是基于预训练生成器进行域适应方法的共性瓶颈。

2. **极端少样本过拟合**：当每域仅有一张训练图像时，生成结果可能出现目标域训练图像的不当细节泄露（如眼镜等特定元素被复制到生成图像中）。这源于对比自适应损失在正样本极度稀缺时，可能过度强调与唯一正样本的相似性，导致生成多样性下降和训练图像特征的不当迁移。

适用边界可总结为：DynaGAN在目标域与源域共享一定结构先验（如猫到其他动物、人脸到艺术风格人脸）且每域有少量（≥5张）训练图像的场景下表现优异；当域间结构差异过大或样本极度稀缺时，性能显著退化。

![[assets/figures/papers/paper_list_l49_https_bluegorae_github_io_dynagan/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison with multi-MTGs on the cat-to-animals dataset. Multi-MTGs consists of multiple MTG [Zhu et al. 2022] models separately trained on each target domain. Despite using a single model, our method represents each domain more effectively. Insets from left to right: Pixabay (Pexels, vinzling, WikiImages, Gregorius_o) [Pixabay License]*

## 定位与知识库关联

DynaGAN 的核心定位是**少样本多域 GAN 自适应**——在单模型内同时适应多个目标域，而非为每个域独立训练模型。相比现有工作，它改变的关键 slot 是**域适应机制的参数化方式**：从“对整个生成器微调”或“通过 CLIP 空间隐式约束”转变为“基于超网络的动态卷积权重调制”。这一转变使模型能够以条件驱动的方式为不同目标域生成域特定的调制参数（残差 Δφ 和通道缩放 δ），从而在保持源域生成能力的同时，实现多域差异化适应。

### 与基线方法的本质差异

现有少样本域适应方法可大致分为三类，DynaGAN 在每一类上都有明确的差异化改进：

1. **基于微调的方法**，如 **TGAN**（Wang et al., 2018）和 **TGAN‑ada**（Karras et al., 2020a）：这些方法通过直接微调生成器参数来适应目标域，但每个目标域需要独立的微调过程或模型副本，无法在单模型中支持多域。DynaGAN 改变了这一 slot：生成器权重本身保持不变，适应由外挂的超网络通过调制参数实现，单模型即可覆盖多域。

2. **基于跨域一致性的方法**，如 **FS‑ada**（Ojha et al., 2021）：通过在源域和目标域之间施加一致性约束来进行适应，但当面对多个差异显著的目标域时，模型倾向于产生“平均风格”，丢失各域的独特属性。DynaGAN 通过域条件向量 $c$ 显式解耦不同目标域的适应路径，从机制上避免了域间信息混淆。

3. **基于 CLIP 引导的方法**，如 **StyleGAN‑nada**（Gal et al., 2022）和 **MTG‑ext**（Zhu et al., 2022）：前者利用 CLIP 空间的文本引导进行域适应，后者在 MTG 重建损失基础上加入 CLIP 约束。但这些方法同样未针对多域场景设计。DynaGAN 在继承 MTG 损失的同时，引入了**对比自适应损失**（contrastive-adaptation loss），利用 CLIP 编码器构建同域正对和异域负对，显式推动生成图像靠近所属目标域、远离其他域——这是此前方法中缺失的显式多域区分机制。

与 **multi‑MTGs**（Zhu et al., 2022）——即每域独立训练一个 MTG 模型——相比，DynaGAN 在参数效率上实现了质变：10 个目标域下 multi‑MTGs 需要 302.8M 参数，而 DynaGAN 仅需 39.6M，且生成质量更优（Fig.5）。这得益于秩-1 张量分解将高维残差张量 $\Delta\varphi$ 压缩为三个一维向量的外积，使适应模块的参数量不随目标域数量线性增长。

### 知识库挂载点

DynaGAN 的方法链条可挂载到以下知识节点：

- **超网络与动态权重调制**：这是 DynaGAN 的核心技术手段，挂载于“超网络用于参数生成”这一知识线。与一般超网络直接生成完整权重不同，DynaGAN 仅生成残差调制量（Δφ 和 δ），且通过秩-1 分解实现轻量化。这一设计可视为“低秩适应”（LoRA）思想在 GAN 域适应中的早期实践，后续可与 LoRA 系列方法（如 LoRA、AdaLoRA）建立关联。

- **对比学习与域解耦**：对比自适应损失（Eq.5）将对比学习框架引入 GAN 域适应，利用 CLIP 语义空间的正负对区分不同目标域。这与自监督对比学习（SimCLR、MoCo）及 CLIP 引导的图像生成工作（如 StyleCLIP）形成知识交叉，挂载点在于“对比学习用于生成任务的域/风格解耦”。

- **少样本域适应与多域泛化**：DynaGAN 填补了“单模型多域少样本适应”这一空白。在它之前，少样本适应（TGAN、FS‑ada、StyleGAN‑nada）和多域生成（如 StarGAN、GANimation）是两条相对独立的线，DynaGAN 将两者桥接。知识库中可将其定位为“基于预训练 GAN 的多域少样本适应”这一子类的开创性工作。

### 适用边界

DynaGAN 的适用性受以下条件约束：

1. **依赖预训练生成器的源域知识**：适应模块仅调制卷积权重，不改变生成器的底层结构。当源域与目标域差距极大时（如人脸到狗），生成器缺乏目标域的基础先验，调制参数难以弥补这一鸿沟（Fig.11 失败案例）。

2. **极端少样本下的过拟合风险**：当每域仅有一张训练图像时，模型可能将训练图像中的非域特有细节（如眼镜）错误地编码为域属性，导致生成结果中出现不当的源域-目标域混合。

3. **域数量的上限未探索**：论文在 10 个目标域（cat-to-animals）和 9 个目标域（faces）上验证，但未测试当目标域数量大幅增加（如 50+）时，条件向量的表达能力是否饱和，以及对比自适应损失在大量负对下的计算效率问题。

### 后续工作启发

DynaGAN 为以下方向提供了明确的研究起点：

1. **跨大域差距的适应增强**：当前方法在源域-目标域差异过大时失效，后续可探索引入目标域的额外结构先验（如语义分割图、边缘图）或分阶段适应策略，逐步桥接域差距。

2. **过拟合正则化**：针对极端少样本场景，可研究数据增强策略（如域内增广）或正则化项（如调制参数的稀疏约束），防止模型将单张训练图像的特异细节泛化为域属性。

3. **动态适应模块的迁移**：将基于超网络的动态调制思想推广到其他生成框架（如扩散模型、文本到图像模型）或其他任务（如视频风格迁移、3D 生成），探索“单模型多风格/多条件控制”的通用范式。

4. **域插值与连续域空间**：DynaGAN 已展示域插值能力（Fig.7），后续可进一步探索构建连续的域空间，实现域间平滑过渡和新域的零样本组合。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/DynaGAN_Dynamic_Few_shot_Adaptation_of_GANs_to_Multiple_Domains.pdf]]