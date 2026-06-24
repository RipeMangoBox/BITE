---
title: "TCFG: Tangential Damping Classifier-free Guidance"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/TCFG_Tangential_Damping_Classifier_free_Guidance.pdf
aliases:
- TDCFGT
- TCFG
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过奇异值分解（SVD）将无条件评分中与条件评分不对齐的切向分量移除，仅保留法向分量。
primary_logic: 扩散模型的评分函数位于数据流形的法向空间；无条件与条件评分的法向分量高度对齐，而切向分量不对齐。利用 SVD 分离并丢弃切向分量可有效改善条件生成质量与流形对齐。
claims:
- 所有时间步长下，评分函数的奇异值均存在显著下降，表明法向分量主导且存在中间流形。
- 无条件与条件评分的奇异向量在高奇异值处余弦相似度高，低奇异值处相似度低，证明切向分量不对齐。
- 在 MS-COCO 30k 和 ImageNet 50k 上，TCFG 在多种扩散模型上一致改善 FID，同时保持 CLIPScore 近乎不变。
- MS-COCO 30k zero-shot (SD v1.5) 上 FID = 13.12
---

# TCFG: Tangential Damping Classifier-free Guidance

> [!tip] 核心洞察
> 扩散模型的评分函数位于数据流形的法向空间；无条件与条件评分的法向分量高度对齐，而切向分量不对齐。利用 SVD 分离并丢弃切向分量可有效改善条件生成质量与流形对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | TCFG：切向阻尼无分类器引导 |
| 英文题名 | TCFG: Tangential Damping Classifier-free Guidance |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2025/html/Kwon_TCFG_Tangential_Damping_Classifier-free_Guidance_CVPR_2025_paper.html) · [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Tangential Damping Classifier-free Guidance (TCFG) |
| Dataset | MS-COCO 30k zero-shot, ImageNet 50k |

> [!tip] 效果简介
> - MS-COCO 30k zero-shot (SD v1.5) 上，FID 13.12 vs 13.26 (-0.14)。
> - MS-COCO 30k zero-shot (SDXL) 上，FID 12.65 vs 13.36 (-0.71)。
> - MS-COCO 30k zero-shot (SD v3) 上，FID 13.74 vs 16.66 (-2.92)。

## 概述

扩散模型中的标准无分类器引导（CFG）通过线性组合无条件评分与条件评分来增强条件生成，但其核心瓶颈在于：无条件评分中存在的**切向分量与条件评分不对齐**，导致生成轨迹偏离条件指定的目标流形（Figure 1）。

本文提出**切向阻尼无分类器引导（TCFG）**，核心思想源于一个关键发现——扩散模型的评分函数位于数据流形的法向空间，无条件与条件评分的法向分量高度对齐，而切向分量存在显著不对齐（Figure 2, Figure 3）。TCFG 通过奇异值分解（SVD）将拼接后的评分矩阵分解，仅保留无条件评分在最大奇异值对应右奇异向量上的投影，从而**丢弃切向分量、保留法向分量**，实现对 CFG 的即插即用式改进。

实验表明，TCFG 在 MS-COCO 30k 零样本生成上使 SD v1.5、SDXL、SD v3 的 FID 分别降低 0.14、0.71、2.92，在 ImageNet 50k 上使 DiT 的 FID 降低 3.17，同时保持 CLIPScore 近乎不变（Table 1, Table 2）。方法增加的计算成本可忽略不计，且可与 SAG、PAG、CFG++ 等现有 CFG 增强方法组合使用，进一步改善生成质量（Table 3）。

TCFG 为扩散模型的引导机制提供了新的几何视角，但仍存在中间流形假设缺乏严格理论证明、对严重异常区域修复能力有限等局限性（Fig. 10）。

## 背景与动机

### 扩散模型与无分类器引导

扩散模型通过逐步向数据添加噪声并学习逆向去噪过程来生成样本。给定真实数据 $x_0$，前向加噪过程定义为 $z_t = x_0 + \sigma(t) \epsilon$，其中 $\sigma(t)$ 为噪声调度。逆向生成过程可通过随机微分方程（SDE）描述：

$$\mathrm{d} z = - \dot{\sigma}(t) \sigma(t) \nabla_{z_t} \log p_t(z_t) \mathrm{d} t - \beta(t) \sigma(t)^2 \nabla_{z_t} \log p_t(z_t) \mathrm{d} t + \sqrt{2 \beta(t)} \sigma(t) \mathrm{d} \omega_t$$

其中评分函数 $\nabla_{z_t} \log p_t(z_t)$ 是驱动采样的核心，通常通过神经网络 $s_\theta(z_t, t)$ 近似，关系为 $\nabla_{z_t} \log p_t(z_t) \approx \frac{s_{\theta}(z_t, t) - z_t}{\sigma(t)^2}$。

为实现条件生成，**无分类器引导（Classifier-free Guidance, CFG）**（Ho & Salimans, arXiv 2022）通过混合条件评分与无条件评分来放大条件信号：

$$\tilde{s}_{\theta} = s_{\theta}^{\mathrm{uncond}} + \omega_{\mathrm{scale}} (s_{\theta}^{\mathrm{cond}} - s_{\theta}^{\mathrm{uncond}})$$

其中 $\omega_{\mathrm{scale}}$ 为引导尺度。CFG 因其简洁有效而被广泛采用，但其工作机制——特别是无条件评分在引导过程中扮演的角色——尚未被充分剖析。

### 核心瓶颈：切向分量不对齐

本文揭示了一个关键现象：**无条件评分与条件评分在法向分量上高度对齐，而在切向分量上存在显著不对齐**。具体而言，评分函数位于数据流形的法向空间，无条件评分负责估计相邻时间步流形之间的过渡。当无条件评分包含与条件评分不对齐的切向分量时，CFG 的引导结果会偏离条件指定的目标流形，导致生成质量下降。

这一观察得到了系统性的实验支持。作者在 Stable Diffusion v1.5 上使用 17,000 个样本计算了所有时间步下评分函数的奇异值（Figure 2），发现在索引接近 0 处存在显著的奇异值下降，表明**法向分量主导且存在中间流形**。进一步，对无条件与条件评分的奇异向量进行余弦相似度分析（Figure 3），发现高奇异值对应的奇异向量余弦相似度高，而低奇异值处相似度低，这直接证明了**切向分量的不对齐**。该关系可形式化为：

$$[ S_{\mathrm{cos}}(\mathbf{v}_1, \hat{\mathbf{v}}_1) > S_{\mathrm{cos}}(\mathbf{v}_j, \hat{\mathbf{v}}_j) ] \approx [ S_{\mathrm{cos}}(\mathbf{N}_p \nabla_{z_t} \log p_t(z_t, y), \mathbf{N}_p \nabla_{z_t} \log p_t(z_t)) > S_{\mathrm{cos}}(\mathbf{T}_p \nabla_{z_t} \log p_t(z_t, y), \mathbf{T}_p \nabla_{z_t} \log p_t(z_t)) ]$$

### 现有方法的局限

已有的 CFG 增强方法如 **Self-Attention Guidance (SAG)**（Hong et al., ICCV 2023）、**Perturbed-Attention Guidance (PAG)**（Ahn et al., arXiv 2024）和 **CFG++**（Chung et al., arXiv 2024）分别从注意力扰动或流形约束角度改进引导过程，但均未从评分函数的几何结构——特别是法向/切向分量对齐性——入手解决问题。因此，这些方法虽然有效，却未触及不对齐这一根本矛盾。

### 本文动机

基于上述分析，本文提出**切向阻尼无分类器引导（Tangential Damping Classifier-free Guidance, TCFG）**，核心思路是：通过奇异值分解（SVD）识别并丢弃无条件评分中与条件评分不对齐的切向分量，仅保留法向分量，从而减少引导过程中的流形偏离。如 Figure 1 的概念插图所示，标准 CFG 在无条件与条件评分不对齐时容易偏离目标流形，而 TCFG 通过减少这种不对齐，使采样轨迹更准确地收敛到条件指定的目标分布。

## 核心创新

TCFG 的核心创新在于揭示了标准 CFG 中无条件评分与条件评分之间存在的**切向分量不对齐**问题，并提出了一种基于**奇异值分解（SVD）的切向阻尼机制**来解决该问题。该方法仅修改无条件评分的处理方式，不改变模型权重或采样器结构，可作为即插即用的模块嵌入任意 CFG 流程。

### 问题诊断：切向分量不对齐

标准 CFG 的引导评分公式为：

$$\tilde{s}_{\theta} = s_{\theta}^{\mathrm{uncond}} + \omega_{\mathrm{scale}} (s_{\theta}^{\mathrm{cond}} - s_{\theta}^{\mathrm{uncond}})$$

该公式隐含假设无条件评分与条件评分在方向上高度一致。然而，TCFG 通过大规模实证分析发现这一假设并不成立：

- **法向分量对齐**：评分函数位于数据流形的法向空间，无条件与条件评分在高奇异值对应的奇异向量上余弦相似度较高（Figure 3）。
- **切向分量不对齐**：在低奇异值对应的奇异向量上，两者余弦相似度显著降低，表明无条件评分包含指向非目标流形的切向分量（Figure 2, Figure 3）。

当无条件评分携带与条件方向不一致的切向分量时，CFG 组合后的引导方向会偏离目标流形，导致生成质量下降。Figure 1 概念性地展示了这一机制：CFG 的采样轨迹因切向干扰而偏离目标流形，而 TCFG 通过移除切向分量使轨迹保持在目标流形上。

### 核心机制：基于 SVD 的切向阻尼

TCFG 对标准 CFG 的改动集中在**无条件评分的预处理**上，涉及两个 changed slot：

**Slot 1 — 无条件评分的处理方式**：
- **Baseline**：直接使用原始无条件评分 $s_{\theta}(z_t)$。
- **TCFG**：将无条件评分 $s_{\theta}(z_t)$ 与条件评分 $s_{\theta}(z_t, y)$ 拼接为矩阵 $\mathbf{A}$，执行 SVD 分解，然后将无条件评分投影到第一个右奇异向量 $\mathbf{v}_1$ 上，丢弃其余分量：

$$\hat{\mathbf{s}}_{\theta}(z_t) = \mathbf{s}_{\theta}(z_t) \cdot \mathbf{V}^T \cdot [\mathbf{v}_1, \mathbf{0}]$$

这一操作等价于保留无条件评分中与条件评分最对齐的法向分量，同时抑制不对齐的切向分量。

**Slot 2 — 引导评分组合公式**：
- **Baseline**：$\nabla \log \tilde{p} = s_{\theta}^{\mathrm{uncond}} + \omega (s_{\theta}^{\mathrm{cond}} - s_{\theta}^{\mathrm{uncond}})$
- **TCFG**：使用投影后的无条件评分替代原始无条件评分：

$$\nabla_{z_t} \log \hat{p}_t(z_t | y) = \hat{\mathbf{s}}_{\theta}(z_t) + w (\mathbf{s}_{\theta}(z_t, y) - \hat{\mathbf{s}}_{\theta}(z_t))$$

### 与现有方法的本质区别

TCFG 的改进思路与现有 CFG 增强方法存在根本差异：

- **SAG**（Hong et al., ICCV 2023）和 **PAG**（Ahn et al., arXiv 2024）通过注意力机制扰动或自注意力引导来改善生成质量，不涉及评分函数的几何结构分析。
- **CFG++**（Chung et al., arXiv 2024）通过流形约束修正 CFG 更新方向，但未显式建模切向/法向分量的不对齐问题。
- TCFG 首次从**评分函数奇异值谱**的角度揭示了 CFG 失效的几何根源，并利用 SVD 实现了对切向分量的精确阻尼。

### 计算开销

TCFG 仅需对每个采样步的评分向量执行一次小规模 SVD 分解，论文明确指出额外计算成本可忽略不计（negligible additional computation），无需修改模型架构或重新训练。

## 整体框架

TCFG 的核心流程可概括为四个串联模块：**评分预测网络** → **基于 SVD 的切向阻尼模块** → **CFG 组合模块** → **ODE/SDE 采样器**。整体 pipeline 在保持标准 CFG 采样框架不变的前提下，仅在无条件评分的处理环节插入一次轻量级的奇异值分解（SVD）操作。

### 模块关系与输入输出流

1. **评分预测网络**  
   给定当前时间步 $t$ 的噪声潜在变量 $z_t$ 和条件信号 $y$（如文本嵌入或类别标签），预训练的扩散模型同时输出两个评分向量：无条件评分 $\mathbf{s}_{\theta}(z_t)$ 和条件评分 $\mathbf{s}_{\theta}(z_t, y)$。该模块与标准 CFG 完全一致，无需额外训练或微调。

2. **基于 SVD 的切向阻尼模块**  
   这是 TCFG 的核心创新。将无条件评分与条件评分拼接为矩阵 $\mathbf{A} = [\mathbf{s}_{\theta}(z_t), \mathbf{s}_{\theta}(z_t, y)]$，对其进行奇异值分解。依据第 3 节揭示的规律——评分函数的法向分量（对应高奇异值）高度对齐，切向分量（对应低奇异值）不对齐——该模块将无条件评分投影到第一个右奇异向量 $\mathbf{v}_1$ 上，丢弃其余切向分量，得到修正后的无条件评分：

   $$\hat{\mathbf{s}}_{\theta}(z_t) = \mathbf{s}_{\theta}(z_t) \cdot \mathbf{V}^T \cdot [\mathbf{v}_1, \mathbf{0}]$$

   这一操作仅在每个采样步增加可忽略不计的计算开销，且支持单样本 SVD 近似（见 Figure 4 消融实验）。

3. **CFG 组合模块**  
   使用修正后的无条件评分替代原始无条件评分，按引导尺度 $w$ 进行标准无分类器引导组合：

   $$\nabla_{z_t} \log \hat{p}_t(z_t | y) = \hat{\mathbf{s}}_{\theta}(z_t) + w (\mathbf{s}_{\theta}(z_t, y) - \hat{\mathbf{s}}_{\theta}(z_t))$$

   与原始 CFG 公式 $\tilde{s}_{\theta} = s_{\theta}^{\mathrm{uncond}} + \omega_{\mathrm{scale}} (s_{\theta}^{\mathrm{cond}} - s_{\theta}^{\mathrm{uncond}})$ 相比，唯一差异在于无条件评分被替换为切向阻尼后的版本。

4. **ODE/SDE 采样器**  
   将组合后的引导评分代入反向扩散过程，通过 ODE 或 SDE 求解器逐步去噪，最终生成图像 $z_0$。整个采样流程的伪代码见 Algorithm 1。

### 与基线方法的差异定位

| 方法 | 无条件评分处理 | 组合公式 |
|------|---------------|---------|
| **Standard CFG** (Ho & Salimans, arXiv 2022) | 直接使用原始预测 | $\tilde{s}_{\theta} = s_{\theta}^{\mathrm{uncond}} + \omega (s_{\theta}^{\mathrm{cond}} - s_{\theta}^{\mathrm{uncond}})$ |
| **TCFG (本文)** | SVD 投影至 $\mathbf{v}_1$，丢弃切向分量 | $\nabla \log \hat{p} = \hat{\mathbf{s}}_{\theta}^{\mathrm{uncond}} + w (\mathbf{s}_{\theta}^{\mathrm{cond}} - \hat{\mathbf{s}}_{\theta}^{\mathrm{uncond}})$ |

TCFG 的设计使其天然兼容现有的 CFG 增强方法。实验表明，与 **SAG** (Hong et al., ICCV 2023)、**PAG** (Ahn et al., arXiv 2024)、**CFG++** (Chung et al., arXiv 2024) 等方法组合使用时，可进一步降低 FID（Table 3），验证了切向阻尼作为即插即用模块的通用性。

### 关键设计决策

- **仅保留第一个奇异向量**：实验观察到评分函数存在显著的奇异值下降（Figure 2），表明法向分量由少数高奇异值方向主导。保留 $\mathbf{v}_1$ 足以捕获法向信息，同时最大化地消除切向不对齐。如何最优确定保留的奇异向量数量仍是一个开放问题。
- **单样本 SVD 近似**：在玩具示例（Figure 4）中，使用单对评分进行 SVD 与使用多样本 SVD 的生成效果几乎一致，这为实际部署中的计算效率提供了支撑。但在更复杂的条件分布下，该近似的鲁棒性仍需进一步验证（开放问题）。
- **中间流形假设**：整个框架建立在“每个时间步存在中间流形 $\mathcal{M}_t$，且评分函数位于其法向空间”的假设之上（Assumption 1）。Figure 2 和 Figure 3 提供了有力的经验证据，但严格的理论证明尚未给出（局限性）。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/001_Figure_1.jpg]]
*Figure 1: (a) Classifier-free guidance. When the unconditional score*

## 核心模块与公式推导

### 问题形式化：CFG 中的切向不对齐

标准无分类器引导（CFG）的评分组合公式为：

$$
\tilde{s}_{\theta} = s_{\theta}^{\mathrm{uncond}} + \omega_{\mathrm{scale}} (s_{\theta}^{\mathrm{cond}} - s_{\theta}^{\mathrm{uncond}})
$$

其核心假设是：无条件评分与条件评分的差异方向能够引导生成轨迹向条件分布靠拢。然而，本文通过实验揭示了这一假设的脆弱性——**无条件评分中存在与条件评分不对齐的切向分量**，这些分量在 CFG 组合中被放大，导致生成结果偏离目标流形。

### 核心洞察：法向对齐与切向不对齐

本文提出两个关键假设（Section 3）：

1. **中间流形假设**：在每个时间步 $t$，评分函数 $\nabla_{z_t} \log p_t(z_t)$ 位于某个中间流形 $\mathcal{M}_{t'}$ 的法向空间 $\mathcal{N}_{\pi_{t'}(z_t)} \mathcal{M}_{t'}$ 中。Figure 2 的实验证据支持这一点：在 Stable Diffusion v1.5 上对 17,000 个样本计算评分函数的奇异值，所有时间步下均观察到奇异值在低索引处出现显著下降，表明评分函数由少数法向分量主导。

2. **切向不对齐假设**：无条件评分与条件评分的法向分量（高奇异值对应的奇异向量）高度对齐，而切向分量（低奇异值对应的奇异向量）对齐度低。Figure 3 的余弦相似度分析证实：高奇异值对应的奇异向量余弦相似度接近 1，低奇异值对应的奇异向量余弦相似度显著下降。这一关系可形式化为：

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/003_Figure_3.jpg]]
*Figure 3: Cosine similarity between singular vectors of unconditional and conditional scores. We computed the singular vectors*

$$
[ S_{\mathrm{cos}}(\mathbf{v}_1, \hat{\mathbf{v}}_1) > S_{\mathrm{cos}}(\mathbf{v}_j, \hat{\mathbf{v}}_j) ] \approx [ S_{\mathrm{cos}}(\mathbf{N}_p \nabla_{z_t} \log p_t(z_t, y), \mathbf{N}_p \nabla_{z_t} \log p_t(z_t)) > S_{\mathrm{cos}}(\mathbf{T}_p \nabla_{z_t} \log p_t(z_t, y), \mathbf{T}_p \nabla_{z_t} \log p_t(z_t)) ]
$$

### 关键模块：基于 SVD 的切向阻尼

TCFG 的核心操作是在每个采样步对无条件评分进行**切向阻尼**——保留法向分量，丢弃切向分量。具体流程如下（Algorithm 1）：

**步骤 1：评分拼接与 SVD**

给定当前时刻 $t$ 的噪声隐变量 $z_t$，评分预测网络同时输出无条件评分 $\mathbf{s}_{\theta}(z_t)$ 和条件评分 $\mathbf{s}_{\theta}(z_t, y)$。将两者拼接为矩阵 $\mathbf{A} = [\mathbf{s}_{\theta}(z_t), \mathbf{s}_{\theta}(z_t, y)]$，执行奇异值分解：

$$
\mathbf{A} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T
$$

其中 $\mathbf{V}$ 的列向量为右奇异向量，按对应奇异值从大到小排列。第一右奇异向量 $\mathbf{v}_1$ 对应最大奇异值，代表法向分量的主方向。

**步骤 2：无条件评分的投影**

将原始无条件评分投影到 $\mathbf{v}_1$ 方向上，其余分量置零：

$$
\hat{\mathbf{s}}_{\theta}(z_t) = \mathbf{s}_{\theta}(z_t) \cdot \mathbf{V}^T \cdot [\mathbf{v}_1, \mathbf{0}]
$$

这一操作等价于仅保留无条件评分中与条件评分法向分量对齐的部分，丢弃切向分量。在玩具示例（Figure 4）中，使用单样本 SVD 近似（c）与多样本 SVD（d）均能生成与目标分布更一致的样本，验证了该投影策略的有效性。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/005_Figure_4.jpg]]
*Figure 4: Sampling results on different methods with diffusion model trained on two moons dataset. Our proposed methods*

**步骤 3：CFG 组合**

使用投影后的无条件评分进行标准无分类器引导：

$$
\nabla_{z_t} \log \hat{p}_t(z_t | y) = \hat{\mathbf{s}}_{\theta}(z_t) + w (\mathbf{s}_{\theta}(z_t, y) - \hat{\mathbf{s}}_{\theta}(z_t))
$$

其中 $w$ 为引导尺度。与原始 CFG 相比，唯一的区别是将无条件评分 $\mathbf{s}_{\theta}(z_t)$ 替换为切向阻尼后的 $\hat{\mathbf{s}}_{\theta}(z_t)$。

### 模块间的因果链路

整个 TCFG 流水线由四个模块串联：

1. **评分预测网络**：输入 $z_t$ 和时间步 $t$，输出无条件评分和条件评分（Section 2）。
2. **基于 SVD 的切向阻尼模块**：对拼接评分矩阵执行 SVD，将无条件评分投影至第一右奇异向量（Equation 3）。
3. **CFG 组合模块**：按引导尺度 $w$ 组合投影后的无条件评分与原始条件评分（Equation 4）。
4. **ODE/SDE 采样器**：利用修改后的引导评分执行反向扩散过程，生成最终图像。

### 与基线方法的关键差异

| 方法 | 无条件评分处理 | 引导组合公式 |
|------|---------------|-------------|
| **Standard CFG** (Ho & Salimans, arXiv 2022) | 直接使用原始 $\mathbf{s}_{\theta}(z_t)$ | $\tilde{s}_{\theta} = s_{\theta}^{\mathrm{uncond}} + \omega (s_{\theta}^{\mathrm{cond}} - s_{\theta}^{\mathrm{uncond}})$ |
| **TCFG** (本文) | SVD 投影至 $\mathbf{v}_1$，丢弃切向分量 | $\nabla_{z_t} \log \hat{p}_t = \hat{\mathbf{s}}_{\theta}(z_t) + w (\mathbf{s}_{\theta}(z_t, y) - \hat{\mathbf{s}}_{\theta}(z_t))$ |

TCFG 的额外计算成本可忽略不计，因为 SVD 仅在 $2 \times d$ 的小矩阵上进行（$d$ 为评分向量维度），且可与现有 CFG 增强方法（**SAG** (Hong et al., ICCV 2023)、**PAG** (Ahn et al., arXiv 2024)、**CFG++** (Chung et al., arXiv 2024)）直接组合使用（Table 3）。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/004_Figure_5.jpg]]
*Figure 5: Visualization of the sampling trajectory. In CFG (orange path), the unconditional scores (red arrows) include components that point towards directions other than the target distribution, making the final destination deviate from the target distribution. Whereas, our method (green path) removes the inconsistent tangent components in unconditional scores and eventually reaches the target distribution*

## 实验与分析

### 核心发现：TCFG 一致改善生成质量且不牺牲语义对齐

TCFG 的核心效果体现在 **FID 的一致下降** 与 **CLIPScore 的近乎不变** 的同步达成。这一模式在多个模型架构和数据集上得到验证：

**文本到图像生成（MS-COCO 30k 零样本）**：在 Stable Diffusion v1.5、SDXL 和 SD v3 三个不同规模的模型上，TCFG 均实现了 FID 的改善，且 CLIPScore 保持稳定（Table 1）。其中 SD v3 上 FID 从 16.66 降至 13.74（降幅 2.92），效果最为显著；SDXL 上 FID 从 13.36 降至 12.65（降幅 0.71）；SD v1.5 上 FID 从 13.26 降至 13.12（降幅 0.14）。

**类条件图像生成（ImageNet 50k）**：在 DiT 模型上，TCFG 在 FID、sFID、Precision 和 Recall 四个指标上均取得改善，FID 从 32.67 降至 29.5（降幅 3.17），同时 Inception Score 出现轻微下降（Table 2）。这一 IS 的下降值得注意：可能暗示 TCFG 在提升样本真实性的同时略微降低了类条件多样性，但 FID 与 Recall 的同步改善表明整体质量是正向的。

**因果机制验证**：这些改善的根源在于 TCFG 通过 SVD 移除了无条件评分中与条件评分不对齐的切向分量。Figure 2 的实验证据表明，评分函数在所有时间步上的奇异值均存在显著下降，这支持了“中间流形”假设——评分函数主要位于数据流形的法向空间。Figure 3 进一步揭示，无条件与条件评分在高奇异值对应的奇异向量上余弦相似度高，低奇异值处相似度低，直接证明了切向分量的不对齐是标准 CFG 生成偏离目标流形的关键原因。

### 与现有 CFG 增强方法的组合与比较

TCFG 不仅独立有效，还能与现有的 CFG 增强方法协同工作。Table 3 显示，将 TCFG 与 **SAG**（Hong et al., ICCV 2023）、**PAG**（Ahn et al., arXiv 2024）或 **CFG++**（Chung et al., arXiv 2024）组合使用时，FID 均能进一步降低。这表明 TCFG 的切向阻尼机制与这些方法（分别关注自注意力引导、扰动注意力或流形约束）是正交的改进方向。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/010_Table_3.jpg]]
*Table 3: Quantitative comparison with existing baselines. The evaluation was conducted on 30k images from the MS-COCO dataset using the official code; SD v1.4 for SAG, SD v1.5 for PAG and SDXL for CFG++*

### 引导尺度的鲁棒性

TCFG 在不同引导尺度 $w$ 下均表现出稳定的改善效果。Figure 6 的 FID-CLIP 曲线表明，在 SDXL 上使用 50 步采样时，TCFG 在整个引导尺度范围内均能降低 FID，且不牺牲 CLIPScore。这一特性降低了实际使用中的调参负担——用户无需为 TCFG 重新搜索最优引导尺度。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/007_Figure_6.jpg]]
*Figure 6: FID-CLIP curves on SDXL with 50 sampling steps*

### 定性改善：减少过曝光与增强结构

Figure 7 的定性对比显示，TCFG 生成的图像在物体形状和细节上有所增强，同时有效抑制了标准 CFG 中常见的过曝光（overexposure）问题。Figure 9 进一步揭示了这一改善的机制：从相同随机噪声出发，TCFG 修改后的无条件评分（即投影到条件评分主导方向后的评分）已经能生成与目标文本提示部分匹配的图像，而原始无条件评分则生成完全随机的图像。这种“预处理”使得最终的条件生成质量得到改善——例如羽毛基部结构更自然、人体手臂更真实、棒球手套左侧多余的线条被移除。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative evaluation of text-to-image models. Our method prevents overexposure, enhancing the shapes and details of objects*

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/011_Figure_9.jpg]]
*Figure 9: TCFG reduces misalignments between unconditional and conditional generation. Starting from the same random noise z1, when SDXL samples images with only the unconditional score, it produces random images such as trees, snowy mountain landscapes, and women. In contrast, our modified unconditional score, projected on dominant (conditional), generates images that somewhat match the desired text prompts. This is because our method reduces misalignment with the conditional score by dropping the tangential components of the unconditional score. Once the misalignment decreases, the quality of the final images (unconditional + conditional score) improves: The base of the feather has a more natural s...*

### 计算开销与实用性

TCFG 增加的额外计算成本被作者描述为“可忽略不计”（negligible additional computation）。考虑到 SVD 仅在每个采样步对 2×d 维的拼接评分矩阵执行（其中 d 为评分向量维度），且实际实现中可能采用单样本 SVD 近似（Figure 4 显示单样本近似与多样本 SVD 效果几乎一致），这一声称是合理的。

### 失效模式与局限性

TCFG 并非万能。Figure 10 展示了其局限性：当基线样本中存在严重异常区域时，TCFG 有时难以完全修复这些错误。这一失效模式与方法的机制一致——TCFG 通过移除切向分量来改善流形对齐，但如果条件评分本身在异常区域也缺乏正确的法向引导，则切向阻尼无法弥补这一根本性缺陷。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/012_Figure_10.jpg]]
*Figure 10: Limitations Our method occasionally struggles to fix severely wrong regions in the baseline samples*

此外，以下问题仍需进一步验证：
- **中间流形 $\mathcal{M}_t$ 的存在性**目前仅依赖奇异值下降的经验观察，缺乏严格的理论证明。
- **分类器引导场景**下的切向不对齐假设是否成立尚未检验。
- **扩散蒸馏**（如将 CFG 尺度作为输入的一致性模型）中 TCFG 的适用性未探索。
- **最优奇异向量保留数量**：目前仅保留第一个右奇异向量 $\mathbf{v}_1$，是否存在更优的截断策略是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/006_Table_1.jpg]]
*Table 1: Zero-shot FID and CLIPScore measured on MSCOCO 30k. Our method consistently improves FID across all models—Stable Diffusion v1.5, SDXL, and SD v3—while maintaining a nearly identical CLIPScore*

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/008_Table_2.jpg]]
*Table 2: Evaluation metrics measured on ImageNet 50k using DiT. Our method achieves better performance in FID, sFID, Precision, and Recall while showing a slight decrease in Inception Score*

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2025_html_Kwon_TCFG_Tangential_D/figures/002_Figure_2.jpg]]
*Figure 2: Singular values of the score function across all timesteps. We computed the singular values for all timesteps using a total of 17,000 samples from Stable Diffusion v1.5. For both the unconditional and the conditional scores, a significant drop in singular values was observed at indices close to 0 across all timesteps. This suggests the existence of an intermediate manifold*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

TCFG 的核心改进对象是标准无分类器引导（**CFG**，Ho & Salimans, arXiv 2022）。原始 CFG 在每一步无条件评分与条件评分之间做线性外推：

$$
\tilde{s}_{\theta} = s_{\theta}^{\mathrm{uncond}} + \omega_{\mathrm{scale}} (s_{\theta}^{\mathrm{cond}} - s_{\theta}^{\mathrm{uncond}})
$$

TCFG 的切入点在于：无条件评分中与条件评分不对齐的切向分量会干扰生成轨迹向目标流形收敛。因此，TCFG 在 CFG 组合之前，先对无条件评分执行基于 SVD 的切向阻尼：

$$
\hat{\mathbf{s}}_{\theta}(z_t) = \mathbf{s}_{\theta}(z_t) \cdot \mathbf{V}^T \cdot [\mathbf{v}_1, \mathbf{0}]
$$

随后进行引导组合：

$$
\nabla_{z_t} \log \hat{p}_t(z_t | y) = \hat{\mathbf{s}}_{\theta}(z_t) + w (\mathbf{s}_{\theta}(z_t, y) - \hat{\mathbf{s}}_{\theta}(z_t))
$$

从方法谱系上看，TCFG 属于 **CFG 的流形约束增强** 方向。与以下现有增强方法的关系如下：

- **Self-Attention Guidance (SAG)**（Hong et al., ICCV 2023）：通过模糊注意力图来抑制生成过程中的对抗性高频噪声，作用于注意力层的中间特征，而非评分函数本身。
- **Perturbed-Attention Guidance (PAG)**（Ahn et al., arXiv 2024）：通过对自注意力图施加扰动来增强引导信号，同样在特征空间操作。
- **CFG++**（Chung et al., arXiv 2024）：引入流形约束，在评分更新中显式加入对数据流形的投影，与 TCFG 共享“流形对齐”的直觉，但实现路径不同——CFG++ 使用正则化项约束，而 TCFG 通过 SVD 在评分空间直接分离法向/切向分量。

关键区别在于：SAG 和 PAG 在注意力层操作，CFG++ 在损失或更新规则层面施加约束，而 **TCFG 在评分函数的几何结构层面直接干预**——利用 SVD 揭示的法向-切向不对齐现象来修正无条件评分。Table 3 的消融实验表明，TCFG 可与 SAG、PAG、CFG++ 叠加使用，进一步降低 FID，说明其改进机制与上述方法是正交的。

在类条件生成任务上，TCFG 与 **DiT**（Peebles & Xie, ICCV 2023）结合时，将 DiT 上的 FID 从 32.67 降至 29.5（Table 2），表明该方法对基于 Transformer 的扩散骨干同样有效。

### 2. 适用边界

**已验证的有效范围：**

- **模型架构**：Stable Diffusion v1.5、SDXL、SD v3（UNet 骨干）以及 DiT（Transformer 骨干）。
- **任务类型**：文本到图像生成（MS-COCO 零样本）和类条件图像生成（ImageNet）。
- **引导尺度**：在 SDXL 上，不同 ω 取值下 TCFG 均能改善 FID 且不牺牲 CLIPScore（Figure 6），表明对超参数鲁棒。
- **SVD 近似**：在玩具示例中，单样本 SVD 近似与多样本 SVD 产生几乎一致的生成效果（Figure 4），为实际部署提供了计算可行性。

**已知局限（来自论文明确讨论）：**

- **严重异常修复失败**：当基线样本存在严重异常区域时，TCFG 偶尔无法完全修复（Figure 10）。这表明切向阻尼只能修正评分方向的不对齐，无法弥补评分网络本身的根本性预测错误。
- **中间流形缺乏严格理论证明**：TCFG 的核心假设——评分函数位于中间流形 M_t 的法向空间——仅通过奇异值下降的实验观察（Figure 2）得到经验支持，尚未从理论上严格证明。
- **分类器引导场景未验证**：所有分析和实验均在无分类器引导框架下完成，切向不对齐假设在分类器引导（classifier guidance）背景下是否成立，论文未做验证。

### 3. 开放问题

1. **奇异向量保留数量的最优选择**：当前 TCFG 仅保留第一个右奇异向量 v₁ 对应的分量，丢弃所有其他分量。是否存在一个自适应机制，根据奇异值衰减曲线动态确定保留数量，以在法向对齐与信息保留之间取得更优平衡？论文未对此进行消融。

2. **中间流形假设的理论证明**：Assumption 1 断言评分函数位于中间流形的法向空间，但该流形 M_t 的显式构造和严格存在性证明仍是开放问题。若能得到理论保证，将为 SVD 分离法向/切向分量的操作提供更坚实的数学基础。

3. **单样本 SVD 近似的鲁棒性**：玩具示例中单样本 SVD 表现良好，但在高维复杂条件分布（如 MS-COCO 的多样化文本提示）下，单样本近似是否始终可靠？论文未在真实数据上对此进行系统消融。

4. **扩散蒸馏场景的适用性**：当前扩散蒸馏方法（如一致性模型）通常将 CFG 尺度作为输入条件蒸馏到学生模型中。TCFG 的切向阻尼思想能否推广到此类蒸馏框架，减少蒸馏过程中由切向不对齐引入的误差，尚未探索。

5. **分类器引导场景的迁移**：论文的几何分析围绕无条件评分与条件评分的奇异向量对齐展开。在分类器引导设置下，评分函数来自外部分类器的梯度，其法向-切向结构与无分类器引导可能存在本质差异，TCFG 的适用性需要独立验证。

## 原文 PDF

![[paperPDFs/CVPR_2025/TCFG_Tangential_Damping_Classifier_free_Guidance.pdf]]
