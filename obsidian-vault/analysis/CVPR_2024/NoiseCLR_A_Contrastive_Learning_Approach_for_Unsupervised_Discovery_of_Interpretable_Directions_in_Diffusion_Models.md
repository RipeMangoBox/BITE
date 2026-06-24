---
title: "NoiseCLR: A Contrastive Learning Approach for Unsupervised Discovery of Interpretable Directions in Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/NoiseCLR_A_Contrastive_Learning_Approach_for_Unsupervised_Discovery_of_Interpretable_Directions_in_Diffusion_Models.pdf
project_link: https://noiseclr.github.io
aliases:
- NoiseCLR
tags:
- CVPR_2024
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "在多个时间步的噪声预测差异（特征分歧）上应用对比学习目标，鼓励相同方向编辑相似、不同方向编辑相异，从而在无任何标注的情况下发现解耦的方向。"
primary_logic: "以学习方向为条件与无条件噪声预测之差编码了语义编辑信息；对比同一方向在不同图像上的这些差异可以分离出细粒度语义，而推开不同方向的差异则强制解耦。"
claims:
- "NoiseCLR 在没有任何文本提示的情况下，从无标签图像中发现了人脸、猫、车、艺术品等领域的细粒度语义方向。"
- "该方法实现了高度解耦的编辑，支持同域内和跨域多方向同时应用，且不干扰其他区域。"
- "NoiseCLR 在保真度和解耦能力上均优于扩散模型编辑方法（Cycle-Diffusion, SEGA, Composable Diffusion）和无监督概念发现方法（Unsup. Concept Discovery）。"
- "在噪声空间上使用对比学习能够发现比之前工作（如 Diffusion-Pullback）多得多的方向。"
---

# NoiseCLR: A Contrastive Learning Approach for Unsupervised Discovery of Interpretable Directions in Diffusion Models

> [!tip] 核心洞察
> 以学习方向为条件与无条件噪声预测之差编码了语义编辑信息；对比同一方向在不同图像上的这些差异可以分离出细粒度语义，而推开不同方向的差异则强制解耦。

| 字段 | 内容 |
|------|------|
| 中文题名 | NoiseCLR：一种用于扩散模型中可解释方向无监督发现的对比学习方法 |
| 英文题名 | NoiseCLR: A Contrastive Learning Approach for Unsupervised Discovery of Interpretable Directions in Diffusion Models |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.05390); [Project](https://noiseclr.github.io) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | NoiseCLR |
| Dataset | Race Edit, Mustache Edit, Age Edit, Gender Edit |

> [!tip] 效果简介
> - Race Edit 上，LPIPS 为 0.15，对比 0.24 (Prompt2Prompt)，变化 -0.09。
> - Mustache Edit 上，LPIPS 为 0.12，对比 0.22 (Prompt2Prompt)，变化 -0.10。
> - Age Edit 上，LPIPS 为 0.18，对比 0.28 (Prompt2Prompt)，变化 -0.10。

## 概述

扩散模型在图像生成领域取得了显著成功，但对其进行细粒度、解耦的语义编辑仍高度依赖文本提示或成对标注数据。这严重限制了在难以构想精确提示词的领域（如艺术风格、时尚设计、医学影像）中的应用。核心瓶颈在于：**缺少一种无需文本提示或标注数据即可无监督发现可解释编辑方向的方法**。

针对这一瓶颈，**NoiseCLR** 提出了一种基于对比学习的无监督框架。其核心思想是：以学习到的方向为条件与无条件噪声预测之差（特征分歧）编码了语义编辑信息；通过对比学习目标，鼓励同一方向在不同图像上的编辑相似、不同方向的编辑相异，从而在没有任何标注的情况下分离出细粒度语义并强制解耦。该方法无需微调扩散模型，仅需少量无标签领域图像即可学习丰富的编辑方向。

**主要贡献与结果：**
- **无监督方向发现**：在无文本提示的条件下，从无标签图像中发现了人脸（口红、眼镜、年龄等）、猫、车、艺术品等多个领域的细粒度语义方向（Fig. 4, Fig. 5）。
- **解耦编辑能力**：支持同域内和跨域多方向同时编辑，且不干扰其他区域（Fig. 1, Fig. 6）；用户调研中解耦度评分 3.05/5，显著优于基线（Table 2）。
- **保真度优势**：在 LPIPS 指标上优于 Cycle-Diffusion、SEGA、Composable Diffusion 等编辑方法，以及 Unsup. Concept Discovery 等概念发现方法（Table 3，如 Age: 0.17, Mustache: 0.17）；与 Prompt2Prompt 和 Concept Sliders 相比同样取得更低 LPIPS（Table S.4）。
- **高效性**：单领域训练约需 7 小时，零样本编辑仅需约 5 秒；消融实验证实 100 张无标签图像、K=100 个方向即可产生细粒度编辑（Fig. S.12）。

**方法定位：** NoiseCLR 属于扩散模型可解释方向发现方法，与基于 GAN 的 LatentCLR、GANspace、SeFa 等方法形成跨范式对比，同时与 Diffusion-Pullback、Concept Sliders 等扩散模型方向发现/编辑方法直接竞争。相较于依赖文本引导的 Prompt2Prompt 和基于语义掩码的 SEGA，NoiseCLR 在无监督设定下实现了更解耦、更高保真度的编辑。

## 背景与动机

扩散模型，特别是以 Stable Diffusion 为代表的文本到图像生成模型，在图像合成领域已展现出卓越的能力。然而，如何对这些模型进行精确的语义编辑仍然是一个开放挑战。核心瓶颈在于：**扩散模型缺少一种无需文本提示或标注数据即可无监督发现可解释编辑方向的方法**。这一缺口在难以构想提示词的领域（如艺术风格、时尚设计、医学影像）尤为突出。

现有编辑方法主要依赖文本提示来指定编辑意图。例如，基于语义的编辑方法 **SEGA** 和 **Composable Diffusion** 需要用户提供精确的文本描述来引导编辑过程；**Prompt2Prompt** 和 **Cycle-Diffusion** 等方法则通过修改交叉注意力图或反演过程来实现编辑，但仍需文本条件作为语义锚点。这些方法的共同局限在于：当用户无法用语言准确描述期望的编辑效果时（如某种特定的艺术笔触、微妙的年龄变化），系统的可用性急剧下降。

另一类工作尝试在生成模型的潜空间中自动发现可解释方向。在 GAN 时代，**GANspace**、**SeFa** 和 **LatentCLR** 等方法通过主成分分析或对比学习在潜空间中发现了丰富的语义方向。然而，这些方法依赖于 GAN 的架构特性，无法直接迁移到扩散模型。在扩散模型领域，**Diffusion-Pullback** 尝试进行无监督方向发现，但仅能发现极为有限的方向（如仅“超重”和“性别”两个方向），远未达到实用所需的细粒度和多样性。

这种“要么需要文本提示，要么发现方向稀少”的困境，实质上源于一个更深层的机制性问题：扩散模型的去噪过程在高维噪声空间中运行，而语义信息如何在该空间中编码和分离，此前并未被充分理解和利用。

NoiseCLR 正是在这一背景下提出的。其核心动机是回答一个根本性问题：**能否在不依赖任何文本提示或标注的条件下，从少量无标签图像中自动发现丰富、解耦、可解释的编辑方向？** 这一目标的实现将使得扩散模型编辑能力拓展到那些难以用语言描述的语义维度，从而在艺术创作、设计迭代、医学图像分析等场景中释放新的可能性。

## 核心创新

NoiseCLR 的核心创新在于**将扩散模型的可解释方向发现从有监督/文本依赖范式转变为完全无监督的对比学习范式**。这一转变解决了此前方法在难以构想文本提示的领域（如艺术、时尚、医学）中无法发现编辑方向的瓶颈。

### 关键创新点

**1. 无监督方向发现机制（监督方式变更）**

此前的方法——无论是基于文本提示的编辑方法（如 Prompt2Prompt、SEGA）还是无监督概念发现方法——要么依赖成对标注数据，要么需要用户提供文本描述来引导编辑。NoiseCLR 仅使用目标领域的少量无标签图像（如 100 张人脸），通过对比学习目标自动发现 K 个可解释的潜在方向向量 $d_k$，无需任何文本提示或标注（见 Abstract 及 Section 3.2）。

**2. 噪声空间特征分歧上的对比学习（编辑机制变更）**

核心洞见在于：以学习方向为条件与无条件噪声预测之差 $\Delta \epsilon_k^n = \epsilon_\theta(x_t^n, d_k) - \epsilon_\theta(x_t^n, \phi)$ 编码了语义编辑信息。NoiseCLR 在此“特征分歧”上施加对比损失（Equation 5）：

$$\mathcal{L} = -\log \frac{\sum_{a=1}^{|X'|} \sum_{b=1}^{|X'|} \mathbf{1}_{[a \neq b]} \exp(\text{sim}(\Delta \epsilon_j^a, \Delta \epsilon_j^b) / \tau)}{\sum_{a=1}^{|X'|} \sum_{i=1}^{|D'|} \mathbf{1}_{[i \neq j]} \exp(\text{sim}(\Delta \epsilon_j^a, \Delta \epsilon_i^a) / \tau)}$$

该损失鼓励同一方向在不同图像上产生的编辑效果相似（正样本对），而不同方向产生的编辑效果相异（负样本对），从而在无监督条件下分离出细粒度语义并强制解耦。这与标准基于文本条件的无分类器引导（Equation 3）形成根本差异——NoiseCLR 的编辑项直接作用于噪声预测空间，而非依赖文本嵌入的差异。

**3. 多方向解耦编辑的求和机制（多方向编辑变更）**

传统方法在同时应用多个编辑时往往需要分离生成或语义掩码，容易引起属性纠缠。NoiseCLR 将多方向编辑形式化为噪声预测差异的简单求和（Equation 8）：

$$\bar{\epsilon}_\theta(x_t, L) = \sum_{i=1}^{|L|} \lambda_i (\epsilon_\theta(x_t, d_i) - \epsilon_\theta(x_t, \phi))$$

这一线性叠加机制天然支持同域内和跨域多方向同时编辑，且无需任何掩码或用户引导即可保持解耦（见 Figure 1 和 Figure 6）。用户调研（Table 2）的解耦度评分达到 3.05/5，显著优于基线方法。

**4. 真实图像编辑的免优化方案（真实图像条件化变更）**

与依赖逐图像优化或固定反演的现有方法不同，NoiseCLR 采用 DDIM 反演将真实图像映射到噪声变量 $x_T$，随后直接应用已学习的方向进行编辑（Equation 9），无需任何逐图像微调。这使得零样本编辑仅需约 5 秒（单张 NVIDIA L40 GPU），而方向训练阶段约需 7 小时。

### 与最相关工作的本质区别

- **vs. Diffusion-Pullback**：该方法在噪声空间上使用对比学习，发现了比 Diffusion-Pullback 多得多的细粒度方向（见 Supplementary Section S.1.3 及 Fig. S.10），后者仅能发现极少数粗粒度方向。
- **vs. GAN 潜空间发现方法（LatentCLR、GANspace、SeFa）**：NoiseCLR 将对比学习从 GAN 的潜空间迁移到扩散模型的噪声预测空间，利用扩散模型更强的生成能力和多时间步特性，实现了跨域泛化编辑（见 Figure 5 和 Fig. S.9）。
- **vs. 文本驱动编辑方法（Prompt2Prompt、Cycle-Diffusion、SEGA）**：NoiseCLR 完全不依赖文本提示，在 LPIPS 保真度指标上全面优于 Prompt2Prompt（Age: 0.18 vs. 0.28, Mustache: 0.12 vs. 0.22, Race: 0.15 vs. 0.24, Gender: 0.21 vs. 0.25，见 Table S.4）。

## 整体框架

NoiseCLR 的整体 pipeline 围绕一个核心洞察构建：**以学习方向为条件与无条件噪声预测之差（特征分歧）编码了语义编辑信息**。基于此，方法通过对比学习目标在多个时间步的噪声预测差异上鼓励同一方向编辑相似、不同方向编辑相异，从而在无任何标注的情况下发现解耦的语义方向。

### 框架总览

如图 2 所示，NoiseCLR 的输入仅为：
- 一个预训练的文本到图像扩散模型（如 Stable Diffusion）
- 来自特定领域（人脸、猫、车、艺术品等）的一小组无标签图像

输出是 $K$ 个可解释的潜方向向量 $D = \{d_1, \dots, d_K\}$，每个方向对应一个细粒度语义编辑操作（如添加口红、眼镜、改变年龄等）。整个过程无需文本提示、无需标注数据、无需微调扩散模型。

### 模块构成与数据流

框架由四个核心模块串联而成，数据流贯穿扩散模型的前向与逆向过程：

**1. 扩散前向过程（Diffusion Forward Process）**
给定 $N$ 张无标签图像 $X = \{x_1, \dots, x_N\}$，对每张图像施加 $t$ 步前向扩散加噪，获得噪声潜变量 $x_t^n$。这一步骤将图像映射到扩散模型的共享噪声空间，为后续方向学习提供统一的表示基础。

**2. 方向学习模块（Direction Learning Module）**
这是 NoiseCLR 的核心。模块维护 $K$ 个可学习的潜方向向量 $d_k$，以这些方向作为条件输入预训练去噪网络 $\epsilon_\theta$，计算每个方向在每张图像上引起的**特征分歧**：

$$\Delta \epsilon_k^n = \epsilon_\theta(x_t^n, d_k) - \epsilon_\theta(x_t^n, \phi)$$

其中 $\phi$ 表示无条件（空文本）条件。随后，在特征分歧上施加对比学习目标（式 5）：正样本对为同一方向在不同图像上的特征分歧，负样本对为同一图像上不同方向的特征分歧。通过最大化正样本对余弦相似度、最小化负样本对相似度，迫使同一方向学到一致的语义编辑模式，同时推开不同方向以实现解耦。

**3. DDIM 反演模块（DDIM Inversion Module）**
针对真实图像编辑场景，模块使用 DDIM 反演将真实图像逆向映射为噪声变量 $x_T$，从而在无需逐图像优化的条件下将真实图像接入编辑流程。

**4. 编辑集成模块（Editing Integration Module）**
在逆向扩散采样过程中，将方向条件化的噪声差异叠加到标准无分类器引导预测中。对于单一方向 $d_e$ 的生成图像编辑：

$$\bar{\epsilon}_\theta(x_t, c, d_e) = \tilde{\epsilon}_\theta(x_t, c) + \lambda_e (\epsilon_\theta(x_t, d_e) - \epsilon_\theta(x_t, \phi))$$

其中 $\tilde{\epsilon}_\theta(x_t, c)$ 为标准无分类器引导预测，$\lambda_e$ 为编辑强度标量。对于多方向同时编辑，将多个方向的噪声差异求和叠加（式 8），实现无需语义掩码的解耦多属性编辑。真实图像编辑则使用 DDIM 反演轨迹替代文本条件引导（式 9）。

### 关键设计选择

- **方向学习发生在噪声空间而非潜变量空间**：与 GAN 潜空间方向发现方法（如 LatentCLR、GANspace、SeFa）不同，NoiseCLR 直接在扩散模型的噪声预测层面操作，利用去噪网络在不同时间步对语义信息的编码能力。
- **编辑时间步控制编辑粒度**：消融实验证实，从 $t=0.5T$ 开始应用编辑可实现解耦编辑；粗结构编辑（如年龄、种族）需要更早的时间步区间 $[0.9T, 0.8T]$；精细结构编辑（如眼镜）则需要手动选择合适的时间步区间。
- **训练效率**：单领域（人脸）训练约需 7 小时学习 100 个方向；零样本编辑仅需约 5 秒（单张 NVIDIA L40 GPU）。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2312_05390/figures/005_Figure_5.jpg]]
*Figure 5: Editing results on various domains. To demonstrate the generalizability of our method across different domains, we provide editing results on artistic paintings, cats and cars. As demonstrated from in the editing results, our method is able to learn and apply latent directions from various domains using a single diffusion model*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2312_05390/figures/001_Figure_1.jpg]]
*Figure 1: NoiseCLR. We propose an unsupervised approach to identify interpretable directions in text-to-image diffusion models, such as Stable Diffusion [31]. Our method finds semantically meaningful directions across various domains like faces, cats, and art. NoiseCLR can apply multiple directions either within a single domain (a) or across different domains in the same image (b, c) in a disentangled manner. Since the directions learned by our model are highly disentangled, there is no need for semantic masks or user-provided guidance to prevent edits in different domains from influencing each other. Additionally, our method does not require fine-tuning or retraining of the diffusion model, nor does...*

## 核心模块与公式推导

### 扩散模型基础

NoiseCLR 构建在预训练的文本条件扩散模型（Stable Diffusion）之上，不进行微调或重新训练。扩散模型的核心训练目标为：

$$\mathcal{L}_{DM} = \mathbb{E}_{x_0, \epsilon^t \sim \mathcal{N}(0,1), t} \Big[ || \epsilon^t - \epsilon_\theta(x_t, t) ||_2^2 \Big]$$

其中 $\epsilon_\theta$ 为去噪网络，$x_t$ 为加噪后的潜变量，$\epsilon^t$ 为真实噪声。逆向扩散过程通过迭代去噪实现图像生成：

$$x_{t-1} = x_t - \gamma \epsilon_\theta(x_t, t) + \xi, \quad \xi \sim \mathcal{N}(0, \sigma_t^2 I)$$

条件采样采用无分类器引导（Classifier-Free Guidance），将条件 $c$ 与无条件 $\phi$ 的噪声预测进行线性组合：

$$\tilde{\epsilon_\theta}(x_t, c) = \epsilon_\theta(x_t, \phi) + \lambda_g (\epsilon_\theta(x_t, c) - \epsilon_\theta(x_t, \phi))$$

### 方向学习模块：噪声特征分歧与对比损失

NoiseCLR 的核心创新在于：将可学习的方向向量 $d_k$ 作为扩散模型的条件输入，通过对比学习目标在噪声预测空间中无监督地发现语义方向。其关键洞察是：**同一方向在不同图像上引起的噪声预测差异应彼此相似，而不同方向引起的差异应相互远离**。

给定 $N$ 张无标签图像 $X = \{x_1, ..., x_N\}$ 和 $K$ 个待学习的方向向量 $D = \{d_1, ..., d_K\}$，首先对图像施加 $t$ 步前向扩散过程获得噪声潜变量 $x_t^n$。方向 $d_k$ 在样本 $x_n$ 上引起的**特征分歧**（Feature Divergence）定义为：

$$\Delta \epsilon_k^n = \epsilon_\theta(x_t^n, d_k) - \epsilon_\theta(x_t^n, \phi)$$

该分歧向量编码了以 $d_k$ 为条件与无条件之间的噪声预测差异，本质上是方向 $d_k$ 所承载的语义编辑信息在噪声空间中的投影。

对比学习目标鼓励来自同一方向的特征分歧彼此吸引、来自不同方向的特征分歧彼此排斥。损失函数为：

$$\mathcal{L} = -\log \frac{\sum_{a=1}^{|X'|} \sum_{b=1}^{|X'|} \mathbf{1}_{[a \neq b]} \exp(\sin(\Delta \epsilon_j^a, \Delta \epsilon_j^b) / \tau)}{\sum_{a=1}^{|X'|} \sum_{i=1}^{|D'|} \mathbf{1}_{[i \neq j]} \exp(\sin(\Delta \epsilon_j^a, \Delta \epsilon_i^a) / \tau)}$$

其中 $X'$ 和 $D'$ 分别为训练批次中的样本子集和方向子集，$\tau$ 为温度参数。余弦相似度定义为：

$$\sin(\Delta \epsilon_j^a, \Delta \epsilon_j^b) = \frac{\Delta \epsilon_j^a \cdot \Delta \epsilon_j^b}{||\Delta \epsilon_j^a|| \ ||\Delta \epsilon_j^b||}$$

分子鼓励同一方向 $d_j$ 在不同图像 $a$ 和 $b$ 上的编辑效果相似，分母则推开方向 $d_j$ 与其他方向 $d_i$ 在同一图像上的编辑效果。这种设计强制了方向之间的解耦，使得每个方向独立地控制一个语义属性。

### 编辑集成模块：单方向与多方向编辑

学习到的方向向量可直接嵌入扩散模型的逆向采样过程，无需额外训练。对于单一方向 $d_e$ 的生成图像编辑，噪声预测为：

$$\bar{\epsilon_\theta}(x_t, c, d_e) = \tilde{\epsilon_\theta}(x_t, c) + \lambda_e (\epsilon_\theta(x_t, d_e) - \epsilon_\theta(x_t, \phi))$$

其中 $\lambda_e$ 为编辑尺度参数，控制编辑强度（正值增强、负值减弱或反向编辑）。该公式在标准无分类器引导的基础上叠加方向条件化的噪声差异项。

对于多方向同时编辑，NoiseCLR 将一组方向 $L = \{d_1, ..., d_L\}$ 的噪声预测差异直接求和：

$$\bar{\epsilon_\theta}(x_t, L) = \sum_{i=1}^{|L|} \lambda_i (\epsilon_\theta(x_t, d_i) - \epsilon_\theta(x_t, \phi))$$

该求和机制允许在单次扩散过程中同时施加多个解耦的编辑，无需语义掩码或分离生成。

### DDIM 反演模块：真实图像编辑

对于真实图像编辑，NoiseCLR 采用 DDIM 反演将真实图像 $x_0$ 映射为噪声变量 $x_T$，然后在逆向过程中施加方向编辑。真实图像的单方向编辑噪声预测为：

$$\bar{\epsilon_\theta}(x_t, d_e) = \epsilon_\theta(x_t, \phi) + \lambda_e (\epsilon_\theta(x_t, d_e) - \epsilon_\theta(x_t, \phi))$$

与生成图像编辑不同，此处省略了文本条件 $c$ 的无分类器引导项，直接以无条件预测为基底叠加方向差异，避免了反演过程中文本条件与方向条件的冲突。

### 模块间数据流

整个流程可概括为：**扩散前向过程**对无标签图像加噪获得 $x_t$ → **方向学习模块**通过对比损失优化 $K$ 个方向向量 $d_k$，使特征分歧 $\Delta \epsilon_k^n$ 在方向内相似、方向间相异 → 对于新图像，**DDIM 反演模块**将真实图像映射为 $x_T$（仅真实图像编辑需要）→ **编辑集成模块**将方向条件化的噪声差异叠加到逆向扩散的噪声预测中，实现单方向或多方向的解耦编辑。

## 实验与分析

### 核心定量结果

NoiseCLR 在编辑保真度上显著优于现有方法。Table 3 报告了 LPIPS（越低越好）对比：在 Age、Mustache、Gender、Race 四个属性上，NoiseCLR 的 LPIPS 分别为 0.17、0.17、0.20、0.13，均低于 Cycle-Diffusion、SEGA、Composable Diffusion 和 Unsupervised Concept Discovery。与基于文本提示的方法对比（Table S.4），NoiseCLR 同样优于 Prompt2Prompt：Race 编辑 LPIPS 为 0.15 vs. 0.24，Mustache 为 0.12 vs. 0.22，Age 为 0.18 vs. 0.28，Gender 为 0.21 vs. 0.25。这表明 NoiseCLR 在实现语义编辑的同时更好地保持了与原图的视觉一致性。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2312_05390/figures/011_Table_3.jpg]]
*Table 3: LPIPS [47] scores (lower is the better). Our method is able to achieve lower LPIPS than the other methods, indicating greater coherence while performing the edits*

### 解耦能力验证

Table 1 的 CLIP 分类器重评分分析量化了解耦效果。以 Indian 属性为例，NoiseCLR 将其分类概率提升 29.8%，而其他属性（Asian、Mustache、Child、Lipstick）的变化极小。类似地，Asian 属性提升 27.5%，Mustache 提升 48.9%，Child 提升 32.8%，Lipstick 提升 11.0%，且均未显著干扰非目标属性。这证实了对比学习目标强制不同方向的特征分歧（feature divergence）相互排斥，从而实现了属性级解耦。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2312_05390/figures/009_Table_1.jpg]]
*Table 1: Re-scoring Analysis. The change in classification probability of the CLIP classifier for various attributes. Bold numbers indicate that NoiseCLR consistently enhances the target semantics across all attributes. Additionally, our approach achieves disentangled editing by minimizing its influence on other attribute scores when modifying a single attribute*

用户调研（Table 2）进一步支持了这一结论：在 1-5 分制下，NoiseCLR 的解耦度评分达到 3.05/5，编辑质量评分为 2.65/5，均显著高于基线方法。Fig. 6 直观展示了同域内（人脸同时加眼镜和口红）和跨域（猫+人脸同时编辑）的多方向同时应用，编辑效果互不干扰，无需语义掩码。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2312_05390/figures/010_Table_2.jpg]]
*Table 2: User Study Results. The average response score of the participants are provided in the table. The scoring is performed within the scale of 1-to-5*

### 消融实验关键发现

消融实验揭示了方法的关键依赖关系：

- **训练数据量（N）**：使用 N=100 张无标签人脸图像即可学习丰富的细粒度方向；N=10 时编辑效果变粗（Fig. S.12）。这表明方法对数据量的需求较低，但仍需一定数量的样本以捕获语义多样性。
- **方向数量（K）**：设定 K=100 个方向能产生细粒度编辑（如口红、眼镜、年龄等）；K=10 仅能获得粗粒度编辑（Fig. S.12）。这说明对比学习目标在较大方向空间中能自然分离出更多细粒度语义。
- **数据来源**：从合成图像学习到的方向范围显著窄于真实图像（Fig. S.12）。原因在于扩散模型生成的合成图像存在伪影，干扰了噪声预测差异的学习，这是一个值得注意的失败模式。
- **编辑时间步**：从 t=0.5T 开始应用编辑可实现解耦；粗结构编辑（如年龄、种族）需要更早的时间步（[0.9T, 0.8T]）（Fig. S.13）。精细结构编辑（如眼镜）需要手动选择合适的时间步区间，这是当前方法的操作限制。
- **计算开销**：在单域（人脸）上训练约需 7 小时，零样本编辑仅需约 5 秒（单张 NVIDIA L40 GPU）。

### 定性对比

Fig. 8 展示了与 Cycle-Diffusion、SEGA、Composable Diffusion 和 Unsupervised Concept Discovery 的定性对比。NoiseCLR 在语义忠实度和解耦能力上均表现更优，尤其在真实图像编辑任务中，基线方法往往出现属性纠缠或过度修改原图的问题。与 Diffusion-Pullback 的对比（Fig. S.10）显示，NoiseCLR 不仅编辑更忠实，而且发现了数量多得多的方向（Diffusion-Pullback 仅能发现 overweight 和 gender 两个方向，而 NoiseCLR 发现了口红、眼镜、年龄、种族等十余个方向）。

### 失败模式与局限

1. **合成图像伪影干扰**：使用扩散模型生成的合成图像训练时，生成图像中的伪影会污染噪声预测差异的学习，导致发现的方向范围变窄。这是对比学习目标对数据质量敏感的体现。
2. **精细编辑的时间步依赖**：眼镜等精细结构编辑需要手动选择合适的时间步区间，缺乏自动化机制。
3. **预训练模型偏差继承**：方法依赖 Stable Diffusion 和 CLIP，可能继承并放大其中的人口统计学偏差。例如，种族编辑方向可能被滥用于生成偏见内容或深度伪造。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2312_05390/figures/016_Figure.jpg]]
*Figure: Input*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2312_05390/figures/017_Figure.jpg]]

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2312_05390/figures/013_Table.jpg]]
*Table: S.4. LPIPS metric which measures how well the similarity to the original image distribution is maintained (lower is the better). Our method is able to achieve lower LPIPS than the other methods, indicating greater coherence while performing the edits*

## 方法谱系与知识库定位

### 问题定位：扩散模型中的无监督语义方向发现

NoiseCLR 针对的核心瓶颈是：**扩散模型缺少一种无需文本提示或标注数据即可无监督发现可解释编辑方向的方法**，这限制了在难以构想提示词的领域（如艺术、时尚、医学）中的应用。现有扩散模型编辑方法（如 Prompt2Prompt、SEGA、Cycle-Diffusion）依赖文本条件或成对标注数据进行语义编辑；基于 GAN 的潜空间方向发现方法（如 LatentCLR、GANspace、SeFa）虽然无需文本提示，但受限于 GAN 的生成质量和领域覆盖。NoiseCLR 在扩散模型框架内首次实现了完全无监督、无需任何标注的方向发现，填补了这一空白。

### 与已有工作的关系

#### 扩散模型编辑方法

NoiseCLR 与现有扩散模型编辑方法的核心差异在于**监督方式**和**编辑机制**：

- **监督方式**：Prompt2Prompt 需要源-目标文本提示对；SEGA 和 Composable Diffusion 依赖用户提供的语义方向描述；Cycle-Diffusion 需要成对文本条件。NoiseCLR 仅需 100 张无标签域内图像，通过对比学习目标自动发现方向。
- **编辑机制**：标准方法使用基于文本条件的无分类器引导（Classifier-Free Guidance），而 NoiseCLR 在噪声预测中叠加方向项 $\lambda_e(\epsilon_\theta(x_t, d_e) - \epsilon_\theta(x_t, \phi))$（Equation 7），将编辑操作从文本空间转移到学习的潜方向空间。
- **多方向编辑**：现有方法需要分离生成或语义掩码来避免纠缠；NoiseCLR 通过对多个方向对应的噪声预测差异求和（Equation 8）实现同时的解耦编辑，无需额外掩码（Fig. 6 验证了跨域编辑的无干扰效果）。

定量对比（Table S.4）显示，NoiseCLR 在 Age、Mustache、Gender、Race 编辑上的 LPIPS 均显著低于 Prompt2Prompt（如 Age: 0.18 vs 0.28，Mustache: 0.12 vs 0.22），表明更高的保真度。与 Concept Sliders（同期工作）的定性对比（Fig. S.11）表明，Concept Sliders 在 Race 编辑中会改变面部形状、在 Mustache 编辑中混合年龄属性，而 NoiseCLR 保持了更好的解耦性。

#### 无监督概念发现方法

与 Unsupervised Concept Discovery 相比，NoiseCLR 在**方向粒度**和**可编辑性**上具有优势。Fig. 8 的定性对比显示，NoiseCLR 发现的细粒度方向（如口红、眼镜、年龄）在语义保真度上优于 Unsupervised Concept Discovery 的表示。

与 Diffusion-Pullback 的直接对比（Fig. S.10）尤为关键：Diffusion-Pullback 仅能发现少数粗粒度方向（如超重、性别），而 NoiseCLR 在相同设置下发现了显著更多的细粒度方向（Fig. 4 展示了数十个方向），且编辑效果更忠实于原图。

#### GAN 潜空间方向发现方法

NoiseCLR 与 GAN 方法（LatentCLR、GANspace、SeFa）的对比（Fig. S.9）表明，在扩散模型框架内学习到的方向在细粒度人脸编辑上具有竞争力。但关键差异在于：GAN 方法受限于 GAN 的生成质量和领域覆盖，而 NoiseCLR 利用了 Stable Diffusion 的共享潜空间，使得从不同领域（人脸、猫、车、艺术品）学习的方向可以在同一模型中协同工作（Fig. 5, Fig. 6）。

### 核心机制创新

NoiseCLR 的核心洞察是：**以学习方向为条件与无条件噪声预测之差编码了语义编辑信息**（Equation 4: $\Delta \epsilon_k^n = \epsilon_\theta(x_t^n, d_k) - \epsilon_\theta(x_t^n, \phi)$）。对比学习目标（Equation 5）鼓励同一方向在不同图像上的这些差异相似、不同方向的差异相异，从而在无任何标注的情况下分离出细粒度语义并强制解耦。

这一机制与 LatentCLR（在 GAN 潜空间上使用对比学习）在思路上相似，但 NoiseCLR 将对比学习应用于**扩散模型的噪声预测空间**，而非 GAN 的潜空间。关键差异在于：
1. 噪声空间的多时间步特性允许通过编辑时间步控制编辑粒度（Fig. S.13 消融证实：粗结构编辑需要 $[0.9T, 0.8T]$，细粒度编辑从 $0.5T$ 开始即可解耦）。
2. 扩散模型的共享潜空间使得跨域编辑成为可能。

### 适用边界与局限

#### 已知局限

1. **预训练模型偏差继承**：方法依赖预训练的 Stable Diffusion，因此继承了其中的偏差；CLIP 评估也包含偏差。这在局限性部分已明确提及。
2. **数据依赖性**：需要少量目标领域图像（消融证实 N=100 足够，N=10 时编辑变粗），性能取决于图像质量和多样性。使用合成图像学习到的方向范围显著窄于真实图像（Fig. S.12），因为扩散模型产生的伪影会干扰学习。
3. **时间步敏感性**：精细结构编辑（如眼镜）需要手动选择合适的时间步区间。
4. **计算成本**：训练单个领域（人脸）约需 7 小时（100 个方向），但零样本编辑仅需 5 秒。
5. **滥用风险**：发现的方向可能被用于未经同意的非道德编辑（如修改种族、年龄生成深度伪造）。

#### 开放问题

1. **偏差缓解**：如何缓解从 Stable Diffusion 和 CLIP 继承的偏差？具体的恶意应用场景及相应的缓解策略是什么？
2. **零样本扩展**：对比学习目标能否以完全零样本的方式（无需任何域内图像）应用于方向学习？
3. **模态扩展**：该方法能否扩展到其他模态或无条件的扩散模型？
4. **合成数据改进**：为什么 Stable Diffusion 在使用合成图像时会产生阻碍方向发现的缺陷图像，以及如何改进？
5. **训练动力学**：训练步数和批次大小如何影响发现方向的多样性？

### 知识库定位

NoiseCLR 定位于**扩散模型可解释性与可控编辑**的交叉领域，属于无监督表示学习在生成模型中的应用。其技术谱系可追溯至：
- **对比学习**（SimCLR 等）→ LatentCLR（GAN 潜空间）→ NoiseCLR（扩散噪声空间）
- **无分类器引导**（Classifier-Free Guidance）→ 方向条件化编辑
- **GAN 潜空间解耦**（GANspace, SeFa）→ 扩散模型潜空间解耦

该方法在以下维度推进了领域边界：
- **监督范式**：从文本监督/标注依赖 → 完全无监督
- **编辑粒度**：从粗粒度属性 → 细粒度语义（口红、眼镜等）
- **跨域能力**：从单域 GAN → 共享潜空间的多域扩散模型

## 原文 PDF

![[paperPDFs/CVPR_2024/NoiseCLR_A_Contrastive_Learning_Approach_for_Unsupervised_Discovery_of_Interpretable_Directions_in_Diffusion_Models.pdf]]
