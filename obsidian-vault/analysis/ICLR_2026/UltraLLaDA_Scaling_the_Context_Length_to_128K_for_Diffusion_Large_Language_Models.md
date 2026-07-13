---
title: "UltraLLaDA: Scaling the Context Length to 128K for Diffusion Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/UltraLLaDA_Scaling_the_Context_Length_to_128K_for_Diffusion_Large_Language_Models.pdf
project_link: null
code_link: null
openreview_forum_id: 68DGlhlvD9
aliases:
- UltraLLaDA
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "扩散感知的 NTK 缩放（Diffusion-aware NTK）：将预训练期间学习的有效相对位置范围从自回归模型的 [0, T] 修改为扩散模型实际的 [-(T-1), T-1]，即 T_cap ≈ 2T_train，并据此重新估计 RoPE 的关键维度 d'_crit 和缩放因子 λ′，从而正确放慢旋转频率以覆盖扩展后的双向相对位置。"
primary_logic: "扩散LLM的双向注意力使其在预训练时学习了对称的相对位置范围，因此上下文扩展时应将有效长度加倍至约 2T，而非自回归模型的 T。这一洞察直接体现在扩散感知 NTK 的公式中，并指导了长上下文后训练策略。"
claims:
- "UltraLLaDA 在 NIAH 128K 上下文下实现 100% 检索准确率，而训练自由基线 LongLLaDA 在 32K 时已退化至约 20%，且无法超过 32K。"
- "UltraLLaDA 在 128K 困惑度评估中保持低且稳定的 PPL（10.45），而基础模型 LLaDA-8B-Base 则暴涨至 343.88，LongLLaDA 无法超过 32K。"
- "扩散感知 NTK 在训练自由和训练后场景下均优于基线 NTK（例如 RULER 32K 平均分 70.78 vs 65.85），表明考虑双向注意力是扩展扩散 LLM 上下文的关键。"
- "在相同后训练设置下，采用自适应注意力掩码处理跨文档干扰，相比直接拼接在 RULER 32K 上平均分从 63.04 提升至 73.63，验证了掩码策略的必要性。"
---

# UltraLLaDA: Scaling the Context Length to 128K for Diffusion Large Language Models

> [!tip] 核心洞察
> 扩散LLM的双向注意力使其在预训练时学习了对称的相对位置范围，因此上下文扩展时应将有效长度加倍至约 2T，而非自回归模型的 T。这一洞察直接体现在扩散感知 NTK 的公式中，并指导了长上下文后训练策略。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | UltraLLaDA: 将扩散大语言模型的上下文长度扩展至128K |
| 英文题名 | UltraLLaDA: Scaling the Context Length to 128K for Diffusion Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=68DGlhlvD9) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | UltraLLaDA |
| Dataset | PPL-128K (PG19), NIAH-128K (检索准确率), LongBench-16K, RULER-32K |

> [!tip] 效果简介
> - PPL-128K (PG19) 上，Perplexity (越低越好) 为 10.45 (at 128K)，对比 343.88 (LLaDA-8B-Base)，变化 -333.43。
> - NIAH-128K (检索准确率) 上，Accuracy (%) 为 100.0，对比 0.0 (LongLLaDA, >32K 失败)，变化 +100。
> - LongBench-16K 上，加权平均分 (AVG) 为 39.98，对比 31.56 (LLaDA-8B-Base)，变化 +8.42。

## 概要

### 问题与瓶颈

将大语言模型的上下文窗口从数千令牌扩展到数万乃至十万令牌级别，是当前基础模型研究的重要方向。然而，现有长上下文扩展方法几乎全部基于**自回归（Auto-regressive）注意力模式**设计，天然假设每个令牌只能关注其左侧的上下文。这一假设在**扩散大语言模型（Diffusion LLM）**中不再成立——扩散模型采用**双向注意力**，每个令牌在去噪过程中可以同时关注序列中的所有位置。

这一差异导致了一个根本性瓶颈：将自回归模型的位置编码扩展方法直接迁移到扩散LLM时，对**有效相对位置范围**的估计出现系统性错误。具体而言，自回归模型在预训练期间学习的相对位置范围是 $[0, T_{\text{train}}-1]$，而扩散模型由于双向注意力，实际学习的范围是 $[-(T_{\text{train}}-1), T_{\text{train}}-1]$，约为前者的两倍。忽略这一对称性会导致位置编码在长上下文下过度压缩高频旋转维度，使模型退化为仅利用最近邻信息的**局部感知偏差**，无法有效利用长程依赖。

### 核心方法：扩散感知NTK与上下文后训练

UltraLLaDA 的核心贡献在于识别并修正了上述瓶颈，提出了**扩散感知的NTK（Neural Tangent Kernel）缩放方法**。其关键洞察是：在计算RoPE位置编码的关键维度 $d_{\text{crit}}$ 和缩放因子 $\lambda$ 时，应将预训练有效覆盖长度从 $T_{\text{train}}$ 修正为 $T_{\text{cap}} \approx 2T_{\text{train}}$，目标覆盖长度相应修正为 $T_{\text{Ecap}} \approx 2T_{\text{target}}$。这一修正直接体现在公式中：

$$\lambda' = b^{-1} \cdot \left(\frac{T_{\text{Ecap}}}{2\pi}\right)^{\frac{d}{d'_{\text{crit}}}}, \quad d'_{\text{crit}} = 2\left\lceil \frac{d}{2} \log_b \frac{T_{\text{cap}}}{2\pi} \right\rceil$$

这使得旋转频率的放慢程度更适配扩散模型的双向特性，从而在扩展上下文时保留长程位置分辨能力。

在此基础上，UltraLLaDA 进一步探索了**长上下文后训练策略**，包括自适应注意力掩码（仅允许文档内双向注意力，阻断跨文档噪声）和文档结束符拼接等方法，以轻量级微调（仅600步，4M tokens/batch）将上下文窗口稳定扩展至128K。

### 方法谱系与知识库定位

UltraLLaDA 建立在以下工作基础之上：

- **LLaDA-8B-Base**（Nie et al., 2025）：8B参数的掩码扩散语言模型，作为基础初始化模型，未经长上下文微调。
- **LongLLaDA**（Liu et al., 2025b）：训练自由的上下文扩展基线，直接应用原始NTK感知RoPE缩放，未考虑扩散模型的双向性。
- **Baseline NTK**（Peng & Quesnelle, 2023）：原始NTK感知RoPE缩放方法，基于自回归假设设计，作为消融对比的参照系。
- **Dream**（Ye et al., 2025）：由自回归LLM转换而来的扩散语言模型，用于验证所提策略的跨模型泛化性。

UltraLLaDA 的方法定位在于：**首次系统性地揭示了扩散LLM与自回归LLM在位置编码扩展上的本质差异**，并据此设计了专用的NTK缩放方案与数据打包策略。与训练自由基线LongLLaDA相比，UltraLLaDA通过轻量级后训练将有效上下文从不足32K扩展至128K，在NIAH检索任务上实现了100%准确率，而LongLLaDA在32K时已退化至约20%且无法超越该长度。

### 主要结果

在128K上下文的困惑度评估中，UltraLLaDA 保持低且稳定的PPL（10.45），而基础模型LLaDA-8B-Base则暴涨至343.88。在Needle-in-a-Haystack（NIAH）检索任务上，UltraLLaDA在128K上下文内实现100%检索准确率，可处理的上下文窗口是LongLLaDA的8–32倍。在LongBench-16K和RULER-32K等综合长上下文基准上，UltraLLaDA分别取得39.98和73.63的加权平均分，显著优于所有训练自由基线。

消融实验进一步证实：扩散感知NTK在训练自由和训练后场景下均优于基线NTK（RULER 32K平均分70.78 vs 65.85），而自适应注意力掩码策略相比直接拼接将RULER 32K平均分从63.04提升至73.63，验证了跨文档干扰对扩散LLM的显著影响以及掩码策略的必要性。

### 局限与开放问题

尽管在检索和追踪任务上表现卓越，UltraLLaDA在需要聚合多个信息片段的复杂任务（如RULER AGG，48K时仅25.12分）上仍显不足。此外，在传统短上下文基准（Winogrande, ARC-c）上，扩展上下文后的模型性能有所下降，提示长上下文能力与短上下文推理之间可能存在权衡。方法的泛化性目前仅在LLaDA和Dream两种扩散模型上验证，向更大规模模型和更长上下文（如512K或1M）的扩展仍需进一步研究。

### 扩散语言模型的长上下文困境

扩散语言模型（Diffusion LLM）作为一种新兴的生成范式，通过迭代去噪过程生成文本，其核心训练目标为掩码扩散的负对数似然上界：

$$- \mathbb{E}_{t \sim U[0,1], \pmb{x}_0 \sim p_{\mathrm{data}}, \pmb{x}_t \sim q(\pmb{x}_t|\pmb{x}_0)} \left[ \sum_{\lbrace i | \pmb{x}_t^i = m \rbrace} \log p_{\pmb{\theta}}(\pmb{x}_0^i | \pmb{x}_t) \right]$$

其中 $m$ 为掩码令牌，$p_{\pmb{\theta}}$ 由双向 Transformer 参数化。与自回归模型不同，扩散 LLM 采用**双向注意力**机制，允许每个位置同时关注上下文中的所有令牌。这一架构差异在长上下文扩展时暴露出根本性问题：现有方法假定自回归注意力模式，忽略了扩散 LLM 的双向特性。

### 现有方法的根本缺陷

当前主流的长上下文扩展方法（如 NTK 感知 RoPE 缩放）均针对自回归模型设计。以 **LongLLaDA**（Liu et al., 2025b）为代表的训练自由基线直接沿用原始 NTK 缩放公式：

$$\lambda_{\mathrm{baseline}} = b^{-1} \cdot \left( \frac{T_{\mathrm{target}}}{2\pi} \right)^{\frac{d}{d_{\mathrm{crit}}}}, \quad d_{\mathrm{crit}} = 2\left\lceil \frac{d}{2} \log_b \frac{T_{\mathrm{train}}}{2\pi} \right\rceil$$

该方法基于自回归假设，使用预训练长度 $T_{\mathrm{train}}$ 计算 RoPE 的关键维度 $d_{\mathrm{crit}}$。然而，扩散 LLM 的双向注意力使其在预训练期间实际学习的**有效相对位置范围**为 $[-(T-1), T-1]$，而非自回归模型的 $[0, T]$。这一差异导致基线方法对有效相对位置范围的估计出现系统性偏差——它错误地将双向覆盖范围压缩至单向区间，使得模型在长上下文下仅能利用最近的部分信息（局部感知偏差），无法充分利用长程依赖。

### 实证证据揭示的性能断层

实验结果清晰地展示了这一瓶颈的严重性。在 NIAH（Needle-in-a-Haystack）128K 上下文检索任务中（Figure 1），训练自由基线 LongLLaDA 在 32K 时检索准确率已退化至约 20%，且完全无法处理超过 32K 的上下文。在困惑度评估中（Table 1），基础模型 **LLaDA-8B-Base**（Nie et al., 2025）在 128K 上下文下 PPL 暴涨至 343.88，而 LongLLaDA 同样无法超过 32K 限制。这些结果表明，简单迁移自回归模型的扩展策略对扩散 LLM 完全失效。

### 本文的核心动机与解决路径

针对上述瓶颈，本文提出 **UltraLLaDA**，核心洞察在于：扩散 LLM 的双向注意力使其预训练时学习了对称的相对位置范围，因此上下文扩展时应将有效长度加倍至约 $2T$，而非自回归模型的 $T$。这一洞察直接体现在**扩散感知 NTK（Diffusion-aware NTK）**方法中：

$$\lambda' = b^{-1} \cdot \left( \frac{T_{\mathrm{Ecap}}}{2\pi} \right)^{\frac{d}{d_{\mathrm{crit}}'}}, \quad d_{\mathrm{crit}}' = 2\left\lceil \frac{d}{2} \log_b \frac{T_{\mathrm{cap}}}{2\pi} \right\rceil$$

其中 $T_{\mathrm{cap}} \approx 2T_{\mathrm{train}}$（双向覆盖），$T_{\mathrm{Ecap}} \approx 2T_{\mathrm{target}}$。该公式显式修正了有效相对位置范围的估计，从而正确放慢旋转频率以覆盖扩展后的双向相对位置。

此外，本文还探索了长上下文后训练中的**自适应注意力掩码**策略，以隔离跨文档干扰——这一问题在扩散 LLM 的全双向注意力下尤为突出。通过扩散感知 NTK 与掩码策略的协同，UltraLLaDA 在 128K 上下文下实现了 100% 的 NIAH 检索准确率和 10.45 的低困惑度，将扩散 LLM 的可处理上下文窗口扩展至训练自由基线的 8–32 倍。

## 核心方法与创新机理

UltraLLaDA 的核心创新根植于一个被现有长上下文扩展方法系统性忽视的瓶颈：**扩散语言模型的双向注意力特性**。所有为自回归模型设计的 RoPE 扩展方法（如 NTK 感知缩放）均假定模型在预训练期间仅学习单向的、长度为 $T_{\mathrm{train}}$ 的相对位置范围。然而，扩散 LLM 的双向注意力使每个令牌在训练时实际暴露于 $[-(T_{\mathrm{train}}-1), T_{\mathrm{train}}-1]$ 的对称相对位置区间，其有效相对位置跨度约为 $2T_{\mathrm{train}}$。直接沿用自回归假设会导致位置编码扩展时对有效相对位置范围的估计严重不足，迫使模型在长上下文下退化为仅利用最近部分信息的局部感知模式，无法建立长程依赖。

### 扩散感知 NTK 缩放（Diffusion-aware NTK）

针对上述瓶颈，UltraLLaDA 提出**扩散感知 NTK 缩放**作为因果调控旋钮。该方法对 RoPE 关键维度 $d_{\mathrm{crit}}$ 和缩放因子 $\lambda$ 的估计进行了根本性修正：

**基线 NTK**（LongLLaDA 采用，Peng & Quesnelle, 2023）基于自回归假设，使用预训练长度 $T_{\mathrm{train}}$ 和目标长度 $T_{\mathrm{target}}$ 计算关键维度：

$$\lambda_{\mathrm{baseline}} = b^{-1} \cdot \left(\frac{T_{\mathrm{target}}}{2\pi}\right)^{\frac{d}{d_{\mathrm{crit}}}}, \quad d_{\mathrm{crit}} = 2\left\lceil \frac{d}{2} \log_{b} \frac{T_{\mathrm{train}}}{2\pi} \right\rceil$$

**扩散感知 NTK** 则显式引入双向覆盖长度 $T_{\mathrm{cap}} \approx 2T_{\mathrm{train}}$ 和 $T_{\mathrm{Ecap}} \approx 2T_{\mathrm{target}}$，重新推导关键维度与缩放因子：

$$\lambda' = b^{-1} \cdot \left(\frac{T_{\mathrm{Ecap}}}{2\pi}\right)^{\frac{d}{d_{\mathrm{crit}}'}}, \quad d_{\mathrm{crit}}' = 2\left\lceil \frac{d}{2} \log_{b} \frac{T_{\mathrm{cap}}}{2\pi} \right\rceil$$

这一修正产生了两个关键效应：$d_{\mathrm{crit}}'$ 相比基线更大（因为 $T_{\mathrm{cap}} > T_{\mathrm{train}}$），而 $\lambda'$ 相比基线更小。更小的缩放因子意味着旋转频率放慢的幅度更温和，从而更好地保留了预训练期间学习到的双向长程相对位置信息。

**证据强度**：训练自由场景下，扩散感知 NTK 在 NIAH 32K 上达到 79.36% 准确率，显著优于基线 NTK 的 75.28%（Figure 2c）。在后训练场景下，这一优势随上下文增长而扩大——RULER 32K 平均分从 65.85 提升至 70.78，48K 下从 53.75 提升至 56.94（Table 5, Table 9）。关键维度扫描实验进一步验证了分析估计的可靠性：$d_{\mathrm{crit}}'=73$ 实现最佳综合性能，与分析估计的 70 接近，微小偏差归因于训练期间非均匀的相对位置观察频率（Table 8）。

### 自适应注意力掩码策略

第二个关键创新是针对长上下文数据打包的**自适应注意力掩码**。扩散模型的全双向注意力在直接拼接多文档时会产生跨文档噪声——不同文档的令牌相互关注，引入虚假的语义关联，干扰长程依赖的学习。

UltraLLaDA 对比了三种策略（Figure 3）：
- **直接拼接**：无边界处理，全双向注意力跨越文档边界
- **文档结束符（EOD）拼接**：在文档间插入特殊分隔符
- **自适应注意力掩码**：构建文档感知的注意力掩码，仅允许文档内注意力，显式阻断跨文档交互

**证据强度**：消融实验表明，自适应掩码策略在 RULER 32K 上达到 73.63 平均分，显著优于 EOD 拼接的 70.78 和直接拼接的 63.04（Table 5）。在 LongBench 16K 上，自适应掩码同样以 39.98 的平均分领先（Table 4）。这一差距验证了跨文档干扰对扩散 LLM 长上下文学习的实质性影响，以及显式隔离策略的必要性。

### 创新总结

UltraLLaDA 的两个 changed slots 形成协同效应：扩散感知 NTK 从位置编码层面保留了双向注意力习得的长程相对位置信息，自适应掩码从数据层面消除了跨文档噪声对长程依赖学习的干扰。二者共同支撑了轻量级后训练（仅 600 步）即可将上下文窗口从 4K 扩展至 128K，并在 NIAH 上实现 100% 检索准确率（Figure 1），同时将 128K 困惑度从基础模型的 343.88 压缩至 10.45（Table 1）。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_68DGlhlvD9/figures/005_Figure_2.jpg]]
*Figure 2: RoPE critical dimension and training-free case study under different NTK scaling*

UltraLLaDA 的长上下文扩展 pipeline 由三个核心模块串联构成：**扩散感知 NTK 位置编码扩展**、**长上下文数据打包与自适应掩码生成**，以及**轻量级后训练**。整个流程以预训练的 8B 参数扩散语言模型 **LLaDA-8B-Base**（Nie et al., 2025）为起点，目标是将上下文窗口从原始的 4K tokens 扩展至 128K tokens。

### 模块关系与数据流

```
LLaDA-8B-Base (4K 预训练)
        │
        ▼
┌─────────────────────────────┐
│ 模块1: Diffusion-aware NTK  │
│ 位置编码扩展               │
│ • 计算 T_cap ≈ 2T_train    │
│ • 计算 d'_crit 和 λ′       │
│ • 重缩放 RoPE 频率         │
└─────────────┬───────────────┘
              │ 扩展后的位置嵌入
              ▼
┌─────────────────────────────┐
│ 模块2: 长上下文数据打包     │
│ 与自适应掩码生成           │
│ • PG19 → 64K 序列打包      │
│ • 生成文档感知注意力掩码   │
└─────────────┬───────────────┘
              │ 长序列 + 掩码
              ▼
┌─────────────────────────────┐
│ 模块3: 轻量级后训练         │
│ • AdamW, 600 步            │
│ • 4M tokens/batch          │
│ • 128-GPU 集群             │
└─────────────┬───────────────┘
              │
              ▼
        UltraLLaDA (128K 上下文)
```

**模块1** 是整个 pipeline 的理论核心。它解决了扩散 LLM 上下文扩展的根本瓶颈：现有方法（如 LongLLaDA 使用的基线 NTK）假定自回归注意力模式，在计算 RoPE 关键维度 $d_{\text{crit}}$ 时仅使用预训练长度 $T_{\text{train}}$，忽略了扩散模型双向注意力所学习的对称相对位置范围 $[-(T-1), T-1]$。扩散感知 NTK 显式地将有效覆盖长度设为 $T_{\text{cap}} \approx 2T_{\text{train}}$，目标扩展长度设为 $T_{\text{Ecap}} \approx 2T_{\text{target}}$，据此重新估计关键维度 $d'_{\text{crit}}$ 和缩放因子 $\lambda'$：

$$\lambda' = b^{-1} \cdot \left( \frac{T_{\text{Ecap}}}{2\pi} \right)^{\frac{d}{d'_{\text{crit}}}}, \quad d'_{\text{crit}} = 2\left\lceil \frac{d}{2} \log_{b} \frac{T_{\text{cap}}}{2\pi} \right\rceil$$

这一修正使得高频旋转维度的频率放慢幅度更小，从而在长上下文下更好地保留预训练期间学到的相对位置信息。

**模块2** 负责构造后训练所需的长序列数据。从 PG19 语料库中按打包策略将短文档拼接至每条序列 64K tokens，并生成文档感知的注意力掩码。论文比较了三种掩码策略：自适应注意力掩码（仅允许文档内双向注意力）、文档结束符拼接（以 EOD token 分隔文档但保持全注意力），以及直接拼接（无任何边界处理）。最终采用自适应掩码作为主方案，因其能有效隔离跨文档噪声。

**模块3** 执行轻量级后训练，仅需 600 步、4M tokens/batch 的配置在 128-GPU 集群上完成。消融实验证实，使用 4K 短数据在相同步数下进行后训练并不能提升 RULER-4K 性能（Table 10），表明增益主要源于上下文长度的扩展而非额外的训练数据量。

### 训练自由与训练后两条路径

值得注意的是，扩散感知 NTK 本身即可作为训练自由的上下文扩展方法使用（无需模块2和模块3）。在训练自由场景下，它已在 32K NIAH 上达到 79.36% 的准确率，显著优于基线 NTK 的 75.28%（Figure 2c）。模块2和模块3的叠加则进一步将性能推向极致——UltraLLaDA 在 128K NIAH 上实现 100% 检索准确率，而训练自由基线 LongLLaDA 在 32K 时已退化至约 20% 且无法超越 32K（Figure 1）。

### 3.1 问题定位：自回归 NTK 缩放为何在扩散 LLM 上失效

扩散 LLM 与自回归 LLM 的根本差异在于注意力模式：自回归模型使用因果注意力，每个令牌仅关注其左侧的 $T_{\text{train}}-1$ 个令牌；而扩散 LLM 使用双向注意力，每个令牌在预训练期间同时关注其左侧和右侧的所有令牌，实际学习的有效相对位置范围为 $[-(T_{\text{train}}-1), T_{\text{train}}-1]$，覆盖长度约为 $2T_{\text{train}}$。

现有长上下文扩展方法（如 LongLLaDA 采用的基线 NTK 缩放）直接沿用自回归假设，在计算 RoPE 关键维度时仅使用 $T_{\text{train}}$：
$$
d_{\mathrm{crit}} = 2\lceil \frac{d}{2} \log_{b} \frac{T_{\mathrm{train}}}{2\pi} \rceil
$$
$$
\lambda_{\mathrm{baseline}} = b^{-1} \cdot (\frac{T_{\mathrm{target}}}{2\pi})^{\frac{d}{d_{\mathrm{crit}}}}
$$

这一错误估计导致旋转频率放慢不足，模型在长上下文下仅能利用最近部分的信息（局部感知偏差），无法充分利用长程依赖。**Figure 1** 直观展示了这一瓶颈：LongLLaDA 在 32K 上下文时 NIAH 检索准确率已退化至约 20%，且无法超过 32K。

### 3.2 核心模块：扩散感知 NTK 缩放

UltraLLaDA 的核心创新在于将扩散模型的双向注意力特性显式编码进 RoPE 缩放公式中。具体而言，将预训练期间实际学习的有效相对位置范围 $T_{\mathrm{cap}} \approx 2T_{\mathrm{train}}$ 和扩展目标的有效范围 $T_{\mathrm{Ecap}} \approx 2T_{\mathrm{target}}$ 代入 NTK 框架，重新计算关键维度与缩放因子：

$$
d_{\mathrm{crit}}' = 2\lceil \frac{d}{2} \log_{b} \frac{T_{\mathrm{cap}}}{2\pi} \rceil
$$
$$
\lambda' = b^{-1} \cdot (\frac{T_{\mathrm{Ecap}}}{2\pi})^{\frac{d}{d_{\mathrm{crit}}'}}
$$

**公式变量含义**：
- $b$：RoPE 的基础频率（LLaDA-8B 中通常为 10000）
- $d$：注意力头维度
- $T_{\mathrm{cap}} \approx 2T_{\mathrm{train}}$：扩散模型预训练期间实际覆盖的有效相对位置范围
- $T_{\mathrm{Ecap}} \approx 2T_{\mathrm{target}}$：扩展后目标上下文长度的有效双向覆盖范围
- $d_{\mathrm{crit}}'$：扩散感知的关键维度——当旋转频率在该维度上完成一个完整周期时，对应的波长恰好覆盖 $T_{\mathrm{cap}}$
- $\lambda'$：扩散感知的缩放因子，用于对 RoPE 的位置嵌入进行变换

**因果机制**：由于 $T_{\mathrm{cap}} > T_{\mathrm{train}}$，扩散感知 NTK 计算出的 $d_{\mathrm{crit}}'$ 略大于基线 NTK 的 $d_{\mathrm{crit}}$，进而产生更小的缩放因子 $\lambda' < \lambda_{\mathrm{baseline}}$。这意味着高频维度的旋转频率放慢更温和，保留了更多局部位置分辨能力，同时低频维度获得足够的扩展空间来覆盖双向长程依赖。

**Figure 2** 展示了关键维度的几何意义：当相对位置 $(j-i)$ 的绝对值超过关键维度对应的半波长时，RoPE 的注意力分数将无法可靠区分该位置。扩散感知 NTK 通过正确估计 $T_{\mathrm{cap}}$ 来确保关键维度能够覆盖实际需要的双向范围。

### 3.3 长上下文数据打包与自适应掩码

为在轻量级后训练中有效利用扩展的上下文窗口，UltraLLaDA 从 PG19 语料库生成 64K 长度的序列，并引入自适应注意力掩码策略以隔离跨文档干扰。

**Figure 3** 对比了三种注意力模式：
- **全注意力（扩散）**：令牌可关注序列内所有其他令牌，跨文档边界无限制——这导致不同文档间的噪声信号相互干扰
- **自适应注意力（扩散）**：仅允许文档内注意力，跨文档注意力权重被掩码置零，每个文档形成独立的注意力子图
- **自回归注意力**：仅允许左侧单向注意力，作为参考对比

自适应掩码在训练时通过文档边界信息动态构建块对角注意力矩阵，使每个令牌的上下文窗口严格限定在其所属文档内。这一设计消除了跨文档的虚假关联，使模型能够专注于学习长文档内部的依赖关系，而非被无关文档片段的噪声分散注意力。

### 3.4 轻量级后训练流程

在上述两个核心模块的基础上，UltraLLaDA 采用极轻量级的后训练：使用 AdamW 优化器，仅 600 步训练，每批 4M tokens，在 128-GPU 集群上完成。训练目标沿用掩码扩散语言模型的标准上限负对数似然（**Eq. 1**）：

$$
-\mathbb{E}_{t \sim U[0,1], \pmb{x}_0 \sim p_{\mathrm{data}}, \pmb{x}_t \sim q(\pmb{x}_t|\pmb{x}_0)} \left[ \sum_{\lbrace i | \pmb{x}_t^i = m \rbrace} \log p_{\pmb{\theta}}(\pmb{x}_0^i | \pmb{x}_t) \right]
$$

其中 $m$ 为掩码令牌，$p_{\pmb{\theta}}$ 由双向 Transformer 参数化，$t$ 为扩散时间步。该目标与预训练完全一致，仅上下文长度和位置编码发生了改变，确保后训练不会引入分布偏移。

## 实验与关键发现

### 核心瓶颈与因果机制

现有长上下文扩展方法（如 NTK 感知 RoPE 缩放）均基于自回归语言模型设计，其位置编码的关键维度计算依赖于单向注意力的有效相对位置范围 $[0, T_{\text{train}}]$。然而，扩散大语言模型（Diffusion LLM）采用双向注意力，预训练期间每个令牌学习到的相对位置范围实际为 $[-(T_{\text{train}}-1), T_{\text{train}}-1]$，即有效跨度约为 $2T_{\text{train}}$。直接套用自回归假设会导致对有效相对位置范围的严重低估，使得模型在长上下文下仅能利用最近的部分信息（局部感知偏差），无法有效利用长程依赖。这一瓶颈是 **LongLLaDA**（Liu et al., 2025b）在 32K 上下文时性能急剧退化（RULER 平均分仅 5.69，NIAH 准确率约 20%）的根本原因。

**UltraLLaDA** 的核心调控旋钮是**扩散感知的 NTK 缩放**（Diffusion-aware NTK）：将 RoPE 关键维度计算中的有效训练长度从 $T_{\text{train}}$ 修正为 $T_{\text{cap}} \approx 2T_{\text{train}}$，目标长度对应地修正为 $T_{\text{Ecap}} \approx 2T_{\text{target}}$，从而重新估计关键维度 $d'_{\text{crit}}$ 和缩放因子 $\lambda'$：

$$d'_{\text{crit}} = 2\left\lceil \frac{d}{2} \log_b \frac{T_{\text{cap}}}{2\pi} \right\rceil, \quad \lambda' = b^{-1} \cdot \left( \frac{T_{\text{Ecap}}}{2\pi} \right)^{\frac{d}{d'_{\text{crit}}}}$$

这一修正使得高频旋转维度的频率放慢程度更加合理，覆盖了扩散模型实际需要的对称相对位置范围，是后续所有长上下文能力提升的基础。

### 主要实验结果

**长上下文困惑度（PPL-128K）**：在 PG19 测试集上，**UltraLLaDA** 在 128K 上下文长度下保持 10.45 的低困惑度，而基础模型 **LLaDA-8B-Base**（Nie et al., 2025）则暴涨至 343.88（Table 1）。训练自由基线 **LongLLaDA** 无法处理超过 32K 的序列长度，在 32K 时 PPL 已升至 35.02。这表明仅靠训练自由的 RoPE 外推无法解决扩散 LLM 的长上下文退化问题，必须结合扩散感知的位置编码修正与后训练。

**Needle-in-a-Haystack（NIAH-128K）**：**UltraLLaDA** 在 4K 至 128K 的所有上下文长度上均实现了 100% 的检索准确率（Figure 1a），而 **LongLLaDA** 在 32K 时准确率已降至约 20%，且无法扩展到 32K 以上（Figure 1b）。这一对比直观地展示了扩散感知 NTK 与轻量级后训练的组合效果——UltraLLaDA 的有效上下文窗口是 LongLLaDA 的 8–32 倍。

**LongBench-16K**：在 16K 上下文的标准长文本基准上，**UltraLLaDA** 的加权平均分达到 39.98，较 **LLaDA-8B-Base**（31.56）提升 8.42 分，较 **LongLLaDA**（34.50）提升 5.48 分（Table 2）。UltraLLaDA 在所有六个子任务（单文档 QA、多文档 QA、摘要、上下文学习、合成任务、代码补全）上均取得最优，其中合成任务（Syn）的增益最为显著（从 20.00 提升至 33.00）。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_68DGlhlvD9/figures/010_Table_2.jpg]]
*Table 2: LongBench cut at 16K Evaluation. Sub tasks: single-document QA (SD), multi-document QA (MD), summarization (Sum), in-context learning (ICL), synthetic tasks (Syn), and code completion (Code). AVG is an aggregated question-count–weighted average score*

**RULER（4K–32K）**：在更具挑战性的 RULER 基准上，**UltraLLaDA** 在 32K 上下文下的加权平均分达到 73.63，而 **LongLLaDA** 仅为 5.69，**LLaDA-8B-Base** 则完全失败（Table 3）。值得注意的是，UltraLLaDA 在检索（NIAH）和变量追踪（VT）任务上表现尤为突出（32K 时 NIAH 达 99.21，VT 达 97.20），但在聚合任务（AGG）上得分仍然较低（32K 时仅 29.80），这揭示了扩散 LLM 在需要跨多个位置整合信息的复杂任务上的固有困难。

### 消融实验

**扩散感知 NTK vs. 基线 NTK**：在控制其他变量的条件下，扩散感知 NTK 在 RULER 32K 上的平均分从基线 NTK（**Peng & Quesnelle, 2023**）的 65.85 提升至 70.78（Table 5），且随上下文长度增加优势扩大（8K 时差距 1.00，16K 时 3.45，32K 时 4.93）。在 LongBench-16K 上，扩散感知 NTK 也带来小幅但一致的提升（39.80 vs. 39.44，Table 4）。训练自由场景下的对比同样验证了这一优势：扩散感知 NTK 在 NIAH-32K 上达到 79.36，基线 NTK 为 75.28（Figure 2c）。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_68DGlhlvD9/figures/013_Table_5.jpg]]
*Table 5: RULER results: Diffusion-aware NTK and mitigating cross-document interference*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_68DGlhlvD9/figures/012_Table_4.jpg]]
*Table 4: LongBench results: Diffusion-aware NTK and mitigating cross-document interference*

**自适应掩码策略**：在相同后训练设置下，三种跨文档干扰缓解策略的效果排序为：自适应注意力掩码 > 文档结束符（EOD）拼接 > 直接拼接。在 RULER 32K 上，自适应掩码达到 73.63 的平均分，显著优于 EOD 拼接（70.78）和直接拼接（63.04）（Table 5）。这表明扩散 LLM 的双向注意力对跨文档噪声极为敏感——直接拼接会导致无关文档间的注意力干扰，严重损害长上下文理解能力。

**关键维度扫描**：对 $d'_{\text{crit}}$ 的细粒度扫描实验显示，$d'_{\text{crit}}=73$ 时在 LongBench-v2-Short 和 NIAH 上取得最佳综合性能（Table 8），与分析估计的 70 接近。3 个维度的微小偏差主要归因于预训练期间非均匀的相对位置观察频率。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_68DGlhlvD9/figures/016_Table_8.jpg]]
*Table 8: Finer-grained sweep over nearby critical dimensions*

**短数据后训练的对照实验**：在 4K 短数据上使用相同步数（600 步）进行后训练并未提高 RULER-4K 的性能（Table 10），这证实了长上下文能力的增益主要源于位置编码的重新缩放和长序列训练，而非额外的训练数据量。

### 泛化验证

为验证训练策略的通用性，将相同的扩散感知 NTK 与后训练流程应用于 **Dream**（Ye et al., 2025）——一个由自回归模型转换而来的扩散 LLM。将 Dream 从 2K 扩展至 32K 后，**Dream-Finetune** 在 NIAH-32K 的所有长度上均达到 100% 检索准确率，LongBench-v2-Short 得分 31.11，显著优于训练自由的 Dream-NTK（NIAH-32K 仅 4.1）（Table 6）。这证明扩散感知 NTK 框架对不同扩散架构具有良好的泛化性。

### 失败模式与局限

1. **复杂聚合任务困难**：在 RULER 48K 上，**UltraLLaDA** 的 AGG 得分仅 25.12，QA 得分 24.50（Table 12），远低于检索（68.22）和追踪（95.20）任务。扩散 LLM 在需要跨多个信息片段进行聚合推理的场景下存在系统性弱点，这可能与掩码扩散训练的生成式目标有关。

2. **短上下文性能退化**：在传统短上下文基准（Winogrande、ARC-c）上，扩展上下文后的模型性能有所下降（Table 14），表明长上下文能力与短上下文推理能力之间存在权衡。短数据后训练未能缓解这一问题，暗示位置编码的重新缩放可能对短序列的注意力模式产生了副作用。

3. **后训练配置的未优化性**：当前仅使用 600 步后训练（Table 7），更长的训练或不同的优化策略可能进一步提升性能，尤其是在聚合类任务上。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_68DGlhlvD9/figures/015_Table_7.jpg]]
*Table 7: Model training settings for all main results*

## 定位与知识库关联

### 核心问题定位

现有长上下文扩展方法（如 NTK-aware RoPE 缩放、YaRN 等）均建立在自回归语言模型的注意力模式之上，其位置编码扩展策略隐含假定模型在预训练期间仅学习单向的相对位置范围 $[0, T_{\text{train}}-1]$。然而，扩散大语言模型（Diffusion LLM）采用**双向注意力**机制，每个令牌在预训练时同时关注前后两个方向的所有令牌，实际学习的有效相对位置范围为 $[-(T_{\text{train}}-1), T_{\text{train}}-1]$，即跨度约为 $2T_{\text{train}}$。直接将自回归模型的扩展方法迁移至扩散 LLM 会导致对有效相对位置范围的系统性低估，使模型在长上下文下仅能利用最近的部分信息（局部感知偏差），无法充分发挥长程依赖能力——这正是 **LongLLaDA**（Liu et al., 2025b）在 32K 上下文时性能急剧退化至约 20% 检索准确率、且无法超过 32K 的根本瓶颈。

### 方法谱系与关键改进

UltraLLaDA 的核心贡献在于针对扩散 LLM 的双向注意力特性，提出了**扩散感知的 NTK 缩放**（Diffusion-aware NTK），其方法论定位如下：

**上游基线：LongLLaDA 的 NTK 感知 RoPE 缩放。** LongLLaDA 采用原始 NTK 感知缩放公式（Peng & Quesnelle, 2023），基于自回归假设使用 $T_{\text{train}}$ 计算关键维度 $d_{\text{crit}}$：

$$
\lambda_{\text{baseline}} = b^{-1} \cdot \left(\frac{T_{\text{target}}}{2\pi}\right)^{\frac{d}{d_{\text{crit}}}}, \quad d_{\text{crit}} = 2\lceil \frac{d}{2} \log_{b} \frac{T_{\text{train}}}{2\pi} \rceil
$$

该方法未考虑扩散模型的双向性，导致关键维度估计偏小、缩放因子偏大，在长上下文下位置编码的高频分量被过度压缩。

**UltraLLaDA 的改进：扩散感知 NTK。** 核心洞察是将有效覆盖长度从 $T_{\text{train}}$ 修正为 $T_{\text{cap}} \approx 2T_{\text{train}}$（双向覆盖），目标覆盖长度同步修正为 $T_{\text{Ecap}} \approx 2T_{\text{target}}$，重新计算关键维度 $d'_{\text{crit}}$ 和缩放因子 $\lambda'$：

$$
\lambda' = b^{-1} \cdot \left(\frac{T_{\text{Ecap}}}{2\pi}\right)^{\frac{d}{d'_{\text{crit}}}}, \quad d'_{\text{crit}} = 2\lceil \frac{d}{2} \log_{b} \frac{T_{\text{cap}}}{2\pi} \rceil
$$

这一修正使得关键维度略大于基线值、缩放因子略小，从而更正确地放慢旋转频率以覆盖扩展后的双向相对位置范围。在训练自由场景下，扩散感知 NTK 在 NIAH-32K 上达到 79.36%（基线 NTK 为 75.28%）；在后训练场景下，优势随上下文增长而扩大——RULER-32K 平均分从 65.85 提升至 70.78，RULER-48K 从 53.75 提升至 56.94。

**长上下文数据打包与掩码策略。** 扩散 LLM 的双向注意力在直接拼接多文档时会产生跨文档干扰（cross-document interference），这是自回归模型因因果掩码而天然规避的问题。UltraLLaDA 系统比较了三种策略：
1. **直接拼接**（Direct concatenation）：全双向注意力，跨文档噪声最大；
2. **文档结束符拼接**（EOD concatenation）：在文档边界插入特殊令牌，但未强制掩码；
3. **自适应注意力掩码**（Adaptive attention masking）：仅允许文档内注意力，隔离跨文档交互。

消融实验表明，自适应掩码在 RULER-32K 上达到 73.63 平均分，显著优于 EOD 拼接（70.78）和直接拼接（63.04），验证了跨文档干扰对扩散 LLM 的显著影响及掩码策略的必要性。

### 泛化性与适用边界

**跨架构泛化。** 该方法在 **Dream**（Ye et al., 2025）——一种从自回归模型转换而来的扩散 LLM——上得到验证。将 Dream 从 2K 扩展至 32K 后，经相同后训练管线处理的 Dream-Finetune 在 NIAH-32K 所有长度下均达到 100% 检索准确率，LongBench-v2-Short 得分 31.11；而直接 NTK 缩放无后训练的 Dream-NTK 在 NIAH-32K 上仅 4.1%，甚至低于原始 2K 基线的 19.3%。这表明扩散感知 NTK 框架对不同类型的扩散 LLM 具有泛化能力。

**适用边界与已知局限：**
- **短上下文性能退化**：在传统短上下文基准（Winogrande、ARC-c）上，扩展上下文后的模型性能有所下降，表明存在长上下文能力与短上下文推理能力之间的权衡。在 4K 短数据上进行相同步数的后训练并未提高 RULER-4K 性能，进一步暗示增益主要源于位置编码的重新缩放而非额外训练数据。
- **复杂聚合任务的困难**：长上下文下，聚合多个信息片段的复杂任务（如 RULER AGG）得分仍然偏低——48K 时仅 25.12，扩散 LLM 在这些任务上的表现尚不及检索（NIAH）和变量追踪（VT）。
- **验证范围有限**：方法仅在 LLaDA-8B 和 Dream 两种扩散模型上验证，尚未在更大规模（如 70B 级别）或更长上下文（如 512K/1M）上测试。

### 开放问题

1. **能力差异的根源**：为何扩散 LLM 在检索（NIAH）和变量追踪（VT）任务上特别优越，但在聚合（AGG）和复杂 QA 任务上依然困难？这种能力差异是否与双向注意力的归纳偏置或掩码扩散训练目标的特性根本相关？

2. **短上下文性能保留**：短上下文后训练未能带来 RULER-4K 的提升，是否意味着位置编码的重新缩放是长上下文增益的唯一来源？进一步增加后训练数据量或调整训练设置能否同时保留短上下文性能？

3. **关键维度估计的精度**：关键维度 $d'_{\text{crit}}$ 的分析估计值（70）与实验最优值（73）之间存在微小偏差，是否可以通过建模预训练期间非均匀的相对位置观察频率来消除？

4. **极限扩展的可行性**：扩散感知 NTK 框架是否能够扩展到更大的模型（如 70B 级别）以及更长的上下文（如 512K 或 1M）？在这些极限设置下，仅 600 步的轻量级后训练是否仍然足够？

5. **掩码策略的泛化**：如何将自适应掩码策略泛化到多模态扩散模型或需要跨文档推理的任务中，而不引入额外的计算开销？

## 原文 PDF

![[paperPDFs/ICLR_2026/UltraLLaDA_Scaling_the_Context_Length_to_128K_for_Diffusion_Large_Language_Models.pdf]]
