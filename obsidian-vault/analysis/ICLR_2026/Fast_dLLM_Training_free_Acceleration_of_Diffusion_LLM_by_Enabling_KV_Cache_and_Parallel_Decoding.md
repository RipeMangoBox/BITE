---
title: "Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Fast_dLLM_Training_free_Acceleration_of_Diffusion_LLM_by_Enabling_KV_Cache_and_Parallel_Decoding.pdf
project_link: https://nvlabs.github.io/Fast-dLLM
code_link: null
openreview_forum_id: 3Z3Is6hnOT
aliases:
- FD
- Fast-dLLM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "引入面向双向注意力的块状近似KV缓存机制（PrefixCache/DualCache）以复用高相似性的注意力激活；并设计基于置信度阈值/因子的自适应并行解码策略，在保持质量的同时大幅减少冗余计算。"
primary_logic: "相邻解码步之间的KV激活具有极高余弦相似度（≈1），使得近似缓存重用可行且精度损失微小；高置信度token的独立边际分布可有效近似联合分布，理论保证当 (n+1)ε ≤ 1 时贪婪并行解码与贪婪顺序解码等价。"
claims:
- "缓存与并行解码结合，在GSM8K 5-shot 256 tokens上实现8.1×吞吐提升（6.7→54.4 tokens/s），精度仅下降0.8个百分点（79.3→78.5）。"
- "DualCache在8-shot、生成长度1024的条件下达到27.6×端到端加速（LLaDA基线0.7→19.3 tokens/s）。"
- "置信度感知并行解码在GSM8K上以更少NFE生成更多token，且准确率始终优于固定top‑K基线。"
- "KV激活相似度热力图显示块内相邻步相似度接近1，为近似缓存提供直接的实验支撑。"
---

# Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding

> [!tip] 核心洞察
> 相邻解码步之间的KV激活具有极高余弦相似度（≈1），使得近似缓存重用可行且精度损失微小；高置信度token的独立边际分布可有效近似联合分布，理论保证当 (n+1)ε ≤ 1 时贪婪并行解码与贪婪顺序解码等价。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Fast-dLLM：通过启用KV缓存与并行解码实现扩散大语言模型的免训练加速 |
| 英文题名 | Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3Z3Is6hnOT) · [Project](https://nvlabs.github.io/Fast-dLLM) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Fast-dLLM |
| Dataset | GSM8K (5-shot, 256 tokens), 512 tokens), MATH (4-shot, MBPP (3-shot |

> [!tip] 效果简介
> - GSM8K (5-shot, 256 tokens) 上，Throughput (tokens/s) 为 54.4，对比 6.7，变化 +8.1×。
> - GSM8K (5-shot, 512 tokens) 上，Throughput (tokens/s) 为 35.3，对比 3.2，变化 +11.0×。
> - MATH (4-shot, 256 tokens) 上，Throughput (tokens/s) 为 51.7，对比 9.1，变化 +5.7×。

## 概要

扩散大语言模型（dLLM）在文本生成中展现出独特优势，但其推理效率严重受制于两个结构性瓶颈：**（1）缺乏KV缓存机制**，导致每步解码都需对全序列重新计算注意力，计算冗余极高；**（2）并行解码中的条件独立性假设**破坏了token间的依赖关系，使得同时解码多个token时生成质量显著下降。这些瓶颈使得dLLM的端到端吞吐量远低于同等规模的自回归模型。

Fast-dLLM针对上述问题提出了两项核心创新。第一，引入**面向双向注意力的块状近似KV缓存机制**（PrefixCache/DualCache），利用相邻解码步之间KV激活的高度余弦相似性（≈1）实现缓存复用，大幅削减冗余的注意力计算。第二，设计**基于置信度感知的自适应并行解码策略**，通过置信度阈值或因子动态选择高置信度token进行并行解码，并从理论上证明当 $(n+1)\epsilon \le 1$ 时，贪婪并行解码与贪婪顺序解码等价，从而在保持输出质量的同时显著减少解码步数。

在LLaDA-Instruct骨干上，Fast-dLLM在GSM8K 5-shot、生成长度256的设置下实现**8.1倍吞吐提升**（6.7→54.4 tokens/s），精度仅下降0.8个百分点（79.3→78.5）；在长prefill（8-shot）与长生成（1024 tokens）条件下，DualCache方案实现**27.6倍端到端加速**（0.7→19.3 tokens/s）。该方法同时泛化至Dream-Base文本模型、LLaDA-V多模态模型以及蒸馏少步模型dParallel，展现出良好的骨干无关性。

**方法定位**：Fast-dLLM属于扩散大语言模型的免训练推理加速方法，通过近似KV缓存与置信度感知并行解码的组合，在不修改模型权重的前提下实现数量级的吞吐提升，为dLLM的实际部署提供了可行路径。

### 扩散大语言模型的推理困境

掩码扩散模型（Masked Diffusion Models, MDMs）近年来作为自回归（AR）大语言模型的替代范式受到关注。其核心思想是通过迭代去噪过程生成文本：从全 `[MASK]` 序列出发，逐步将掩码token替换为真实token。形式上，给定序列 $\mathbf{x}_0$，前向扩散过程以时间 $t$ 的概率独立地将每个token掩码化：

$$q_{t|0}(\mathbf{x}_t|\mathbf{x}_0) = \prod_{i=1}^{n} \mathrm{Cat}\big(\mathbf{x}_t^i; (1-t)\delta_{\mathbf{x}_0^i} + t\delta_{[\mathrm{MASK}]}\big)$$

模型 $p_\theta$ 通过最小化ELBO进行训练：

$$-\log p_{\theta}(x) \leq \int_0^1 \frac{1}{t} \mathbb{E}_{q_{t\mid 0}}\Big[\sum_{i:x_0^i=\mathrm{[MASK]}} -\log p_{\theta}(x_0^i|x_t)\Big] dt := \mathcal{L}_{\mathrm{MDM}}$$

代表性的扩散LLM包括 **LLaDA**（Nie et al., 2025b）、**Dream**（Ye et al., 2025），以及多模态扩散模型 **LLaDA-V**（You et al., 2025）。这些模型在数学推理、代码生成等任务上展现了竞争力，但其推理效率存在根本性制约。

### 瓶颈一：KV缓存的缺失

自回归模型推理的核心优化是KV缓存——每生成一个token，其Key-Value激活被存储，后续解码仅需计算新token的注意力，避免重复计算。然而，扩散LLM的生成范式本质不同：每一步解码需对**整个序列**执行全注意力计算，包括已确定token和剩余掩码token。这意味着：

- **无缓存复用**：每步解码均需从头计算全序列注意力，计算量随序列长度平方增长。
- **逐token顺序解码效率极低**：以LLaDA为例，在NVIDIA A100上生成256 tokens的吞吐仅约6.7 tokens/s（Table 1），远低于同等规模的自回归模型。

这一瓶颈的根源在于扩散模型的双向注意力机制：已解码token的表示会因后续去噪步骤中上下文变化而更新，使得简单的“存储并复用”策略难以直接适用。

### 瓶颈二：并行解码的质量退化

为加速生成，扩散模型可采用$\tau$-leaping策略一次恢复多个掩码token：

$$q_{s\mid t}(x_s^i|x_t) = \begin{cases}1, & x_t^i \neq [\mathrm{MASK}], x_s^i = x_t^i \\ \frac{s}{t}, & x_t^i = [\mathrm{MASK}], x_s^i = [\mathrm{MASK}] \\ \frac{t-s}{t} q_{0\mid t}(x_s^i|x_t), & x_t^i = [\mathrm{MASK}], x_s^i \neq [\mathrm{MASK}] \end{cases}$$

然而，并行解码引入了一个关键假设：**条件独立性**——同时解码的多个token被视为彼此独立，联合分布被近似为边缘分布的乘积 $q(\mathbf{X}|E) = \prod_{j=1}^{n} p_j(X_{i_j}|E)$。这一假设破坏了token间的真实依赖关系，导致生成质量显著下降。固定top-K并行解码虽能提升吞吐，但精度随并行度增加而快速衰减。

### 核心洞察与动机

Fast-dLLM的提出基于两个关键观察：

1. **相邻解码步的KV激活高度相似**：实验热力图（Figure 3）显示，块内相邻步骤的KV激活余弦相似度接近1，这为近似缓存复用提供了直接支撑——用前一步的KV近似当前步，精度损失微小。

2. **高置信度token的独立解码可理论保证**：当解码置信度足够高时，并行贪婪解码与顺序贪婪解码等价。Theorem 1给出了精确条件：当 $(n+1)\epsilon \le 1$ 时（其中$\epsilon$为置信度误差界），$\operatorname{argmax}_z p(z|E) = \operatorname{argmax}_z q(z|E) = \mathbf{x}^*$，且真实联合分布与边缘乘积分布之间的总变差距离有界：$D_{\mathrm{TV}}(p,q) < \frac{3n-1}{2}\epsilon$。

基于这两个洞察，Fast-dLLM旨在**免训练**地同时解决KV缓存缺失与并行解码质量退化两大瓶颈，在保持生成精度的前提下实现扩散LLM推理的实质性加速。

## 核心方法与创新机理

Fast-dLLM 针对扩散大语言模型的两大结构性瓶颈——**缺乏 KV 缓存导致逐 token 全注意力重计算**，以及**并行解码中条件独立性假设破坏 token 间依赖关系**——提出了两个相互协同的核心创新。

### 创新一：面向双向注意力的块状近似 KV 缓存

自回归模型天然支持因果掩码下的 KV 缓存复用，但扩散模型的**双向注意力**使得每次解码步的激活随序列整体变化，传统缓存方案直接失效。Fast-dLLM 的关键洞察是：**相邻解码步之间的 KV 激活具有极高的余弦相似度（≈1）**（Figure 3 红色方框区域），使得近似缓存重用可行且精度损失微小。

基于此，Fast-dLLM 设计了两种块状缓存机制：

- **PrefixCache**：将提示（prompt）部分的 KV 缓存预先计算一次，在块内多个解码步中直接复用，块完成后联合解码步骤更新全序列缓存，**零额外计算开销**（Algorithm 1 Line 19）。
- **DualCache**：进一步缓存由全掩码 token 组成的后缀块 KV 激活，实现双向注意力下的前缀与后缀双重复用，在长生成场景下加速效果更为显著。

这一设计将扩散模型的“每次重计算全注意力”变为“块内复用 + 块间更新”，从根源上削减了冗余计算。Table 14 显示，在 256+256 的输入-生成长度下，DualCache 将计算量从 7.68T FLOPs 降至 0.48T（**16× 以上缩减**），而显存仅从 15.07G 微增至 15.36G。

### 创新二：置信度感知的自适应并行解码

并行解码（τ-leaping）一次性恢复多个掩码 token，虽能减少解码步数，但其**条件独立性假设**（将联合分布近似为边缘乘积）会破坏 token 间依赖，导致生成质量下降。Fast-dLLM 的解决思路是：**仅对高置信度 token 并行解码，低置信度 token 保留掩码状态等待后续步处理**，从而在加速的同时约束近似误差。

具体策略包括两种可切换模式：

- **阈值解码**：对每个掩码位置计算最大 softmax 概率作为置信度，并行解码所有置信度 ≥ τ 的 token，并始终解码最高置信度 token 以保证每步都有进展（Algorithm 1 Lines 7-13）。
- **因子解码**：寻找满足 $(n+1)(1-c^{(n)}) < f$ 的最大 $n$，其中 $c^{(n)}$ 为第 $n$ 高置信度，$f$ 为可控因子。该策略具有理论保证：**当 $(n+1)\epsilon \le 1$ 时，贪婪并行解码与贪婪顺序解码结果等价**（Theorem 1）。

Theorem 1 进一步给出了真实联合分布 $p$ 与边缘乘积分布 $q$ 之间的总变差距离上界 $D_{\mathrm{TV}}(p,q) < \frac{3n-1}{2}\epsilon$ 和前向 KL 散度上界 $D_{\mathrm{KL}}(p \| q) < (n-1)[H_b(\epsilon) + \epsilon \ln(|\mathcal{V}|-1)]$，为置信度感知策略提供了形式化支撑。

### 协同效应

两项创新并非简单叠加，而是**架构级协同**：块状生成使缓存复用成为可能，缓存复用又释放了计算资源，使并行解码的额外开销被有效吸收。在 GSM8K 5-shot 256 tokens 设置下，+Cache+Parallel（即 Fast-dLLM）组合实现 **8.1× 吞吐提升**（6.7→54.4 tokens/s），精度仅下降 0.8 个百分点（79.3→78.5）；在 8-shot、生成长度 1024 的极端场景下，DualCache 达到 **27.6× 端到端加速**（0.7→19.3 tokens/s）。

### 与基线方法的关键差异

| 维度 | 基线扩散 LLM（LLaDA/Dream） | Fast-dLLM |
|------|---------------------------|-----------|
| KV 缓存 | 无，每次解码重计算全注意力 | 块状近似缓存（PrefixCache/DualCache），利用相邻步高相似性复用 |
| 解码策略 | τ-leaping 同时解码所有掩码 token，或固定 top-K 并行 | 置信度感知自适应并行，理论保证下的安全多 token 生成 |
| 生成粒度 | 整个序列同时迭代去噪 | 块内步骤复用缓存，块间更新全序列缓存 |

Fast-dLLM 的上述设计是**免训练**的，可直接应用于任何预训练扩散大语言模型（已验证 LLaDA、Dream、LLaDA-V、dParallel 等），无需额外微调或蒸馏。

Fast-dLLM 的整体推理流程围绕两个核心机制展开：**块状近似 KV 缓存**（Block-wise Approximate KV Cache）与**置信度感知并行解码**（Confidence-Aware Parallel Decoding）。两者协同工作，在扩散大语言模型（如 LLaDA、Dream）的迭代去噪过程中消除冗余计算，同时通过理论保证维持生成质量。

### Pipeline 总览

完整流程由 Algorithm 1 给出，可分解为五个模块：

1.  **KV Cache Init**：根据缓存策略（PrefixCache 或 DualCache）初始化前缀或双向 KV 缓存。PrefixCache 仅缓存 prompt 的注意力激活；DualCache 额外缓存当前块之后的掩码 suffix token 的激活。
2.  **Cache Reuse**：在块内每一步解码中，直接复用预计算的 KV 缓存，避免对全序列重复执行注意力计算。
3.  **Confidence Scoring**：对每个掩码位置计算最大 softmax 概率作为置信度 $c_i$，用于指导并行解码的 token 选择。
4.  **Parallel Unmasking (Threshold / Factor)**：根据阈值策略（$c_i \ge \tau$）或因子策略（$(n+1)(1-c^{(n)}) < f$）自适应选择高置信度 token 并行解码。两种策略均强制解码当前置信度最高的 token 以保证每步都有进展。
5.  **Cache Update**：块解码完成后，与解码步骤联合更新全序列 KV 缓存，**零额外计算开销**。

### 输入输出流

-   **输入**：一个完全掩码的序列 $x_t$（或仅包含 prompt 的部分掩码序列）及可选的多模态上下文。
-   **块状生成循环**：将生成过程划分为多个块。每个块内，步骤 2–4 循环执行，复用同一份 KV 缓存；块完成后触发步骤 5 更新缓存，再进入下一块。
-   **输出**：逐步去噪的完整文本序列，直至命中 `<eos>` 或达到最大生成长度。

### 模块关系与关键设计决策

块状生成是 KV 缓存得以实现的前提。扩散模型的双向注意力使得自回归模型中“逐 token 追加缓存”的策略失效；Fast-dLLM 转而采用**块状近似**：假设相邻解码步之间的 KV 激活具有极高余弦相似度（Figure 3 热力图显示块内相邻步相似度接近 1），因此可在整个块内安全复用缓存，仅在块边界更新。

置信度感知并行解码解决了 $\tau$-leaping 中条件独立性假设对 token 依赖关系的破坏。Theorem 1 提供了理论保证：当 $(n+1)\epsilon \le 1$ 时，基于边缘乘积的贪婪并行解码与顺序贪婪解码等价。阈值策略和因子策略分别从绝对置信度和相对置信度两个角度实现这一条件，确保并行解码的精度损失可控。

两个机制的组合效应是乘法级的：缓存减少单步计算量，并行解码减少所需步数。在 GSM8K 5-shot 256 tokens 设定下，两者叠加带来 **8.1×** 吞吐提升（6.7 → 54.4 tokens/s），精度仅下降 0.8 个百分点（Table 1）。

### 3.1 方法总览

Fast-dLLM 由两个核心模块构成：**块状近似KV缓存机制**（Block-Wise Approximate KV Cache）与**置信度感知并行解码策略**（Confidence-Aware Parallel Decoding）。两者的协同逻辑是：先将生成过程划分为若干块，块内复用预计算的KV缓存以消除冗余注意力计算；再在每个块内，根据token置信度自适应地选择多个高置信度token并行解码，在保持生成质量的前提下大幅减少解码步数。整体流程见 Algorithm 1。

### 3.2 块状近似KV缓存

扩散大语言模型采用双向注意力，每次解码步需对完整序列重新计算注意力，这是其推理效率低下的根本瓶颈。Fast-dLLM 观察到：相邻解码步之间的KV激活具有极高余弦相似度（Figure 3 中红色方框区域，相似度接近1），这为近似缓存重用提供了实验基础。

基于此，方法将生成过程组织为**块状解码**（Block-Wise Decoding）。具体而言：

- **PrefixCache**：在生成每个块之前，仅对前缀（prompt）计算一次KV缓存并存储；块内的每一步解码直接复用该缓存，无需重复计算前缀注意力。块解码完成后，与解码步骤联合更新全序列KV缓存，更新开销几乎为零（因为更新操作可与解码计算融合）。
- **DualCache**：进一步将缓存范围从纯前缀扩展至前缀与后缀（mask token区域）。由于块状解码中后缀token全为[MASK]，其KV激活同样具备跨步高相似性，可一并缓存复用，从而获得更大的计算节省。

缓存块尺寸（cache block size）是该方法的关键超参数：较小的块尺寸精度更高但缓存更新更频繁，较大的块尺寸吞吐更高但近似误差累积风险增大。消融实验表明块尺寸32在吞吐与精度间取得最佳权衡（Figure 4）。

### 3.3 置信度感知并行解码

扩散模型的并行解码（如τ-leaping）通过条件独立性假设同时解码多个mask token，但这破坏了token间的依赖关系，导致生成质量下降。Fast-dLLM 的核心洞察是：当某个token的预测置信度足够高时，其边际分布可有效近似其真实条件分布，此时并行解码该token引入的误差可控。

**置信度定义**：对每个mask位置 $i$，取模型预测概率的最大值作为置信度 $c_i = \max_{v \in \mathcal{V}} p_\theta(x_0^i = v | x_t)$。

**两种并行策略**：

1. **阈值解码（Threshold）**：设定置信度阈值 $\tau$，每步解码所有满足 $c_i \ge \tau$ 的token。为保证每步至少有一个token被解码，始终选择置信度最高的token。
2. **因子解码（Factor）**：寻找最大的 $n$ 使得 $(n+1)(1 - c^{(n)}) < f$，其中 $c^{(n)}$ 为第 $n$ 高置信度，$f$ 为控制并行度的因子超参数。该策略从理论上更精细地控制并行度与精度损失之间的权衡。

**理论保证**（Theorem 1）：令 $p$ 为真实联合分布，$q$ 为边缘乘积分布（即并行解码所依据的分布），$\epsilon$ 为每个token置信度下界（即 $1 - c_i \le \epsilon$）。当 $(n+1)\epsilon \le 1$ 时，贪婪并行解码与贪婪顺序解码结果一致：
$$\underset{z}{\operatorname{argmax}}\ p(z|E) = \underset{z}{\operatorname{argmax}}\ q(z|E) = \mathbf{x}^*$$

同时，$p$ 与 $q$ 之间的总变差距离存在上界：
$$D_{\mathrm{TV}}(p, q) < \frac{3n-1}{2}\epsilon$$

前向KL散度上界为：
$$D_{\mathrm{KL}}(p \| q) < (n-1)[H_b(\epsilon) + \epsilon \ln(|\mathcal{V}|-1)]$$

这些界表明：当置信度足够高（$\epsilon$ 小）且并行token数 $n$ 受控时，并行解码引入的分布偏差是有限的，为方法提供了理论支撑。

### 3.4 扩散模型基础公式

Fast-dLLM 建立在掩码扩散模型（Masked Diffusion Model, MDM）之上。其前向过程以时间 $t$ 为概率将token替换为[MASK]：

$$q_{t|0}(\mathbf{x}_t|\mathbf{x}_0) = \prod_{i=1}^{n} \mathrm{Cat}\big(\mathbf{x}_t^i; (1-t)\delta_{\mathbf{x}_0^i} + t\delta_{[\mathrm{MASK}]}\big)$$

训练目标为连续时间ELBO：

$$-\log p_{\theta}(x) \leq \int_0^1 \frac{1}{t} \mathbb{E}_{q_{t\mid 0}}\Big[\sum_{i:x_0^i=[\mathrm{MASK}]} -\log p_{\theta}(x_0^i|x_t)\Big] dt := \mathcal{L}_{\mathrm{MDM}}$$

推理时，τ-leaping策略一次恢复多个mask token，其转移动态为：

$$q_{s\mid t}(x_s^i|x_t) = \begin{cases}1, & x_t^i \neq [\mathrm{MASK}], x_s^i = x_t^i \\ \frac{s}{t}, & x_t^i = [\mathrm{MASK}], x_s^i = [\mathrm{MASK}] \\ \frac{t-s}{t} q_{0\mid t}(x_s^i|x_t), & x_t^i = [\mathrm{MASK}], x_s^i \neq [\mathrm{MASK}] \end{cases}$$

Fast-dLLM 的并行解码正是在τ-leaping框架下，将条件独立假设下的联合分布替换为边缘乘积形式：

$$q(\mathbf{X}|E) = \prod_{j=1}^{n} p_j(X_{i_j}|E)$$

并通过置信度感知机制筛选参与并行解码的token，从而在加速与质量间取得可控平衡。

## 实验与关键发现

### 核心性能：吞吐与精度的权衡

Fast-dLLM 在多种扩散大语言模型骨干上实现了数量级的解码吞吐提升，同时将精度损失控制在极窄范围内。Table 1 汇总了 LLaDA-Instruct 在五个基准上的主结果：在 GSM8K（5-shot，生成长度 256）上，+Cache+Parallel 组合将吞吐从 6.7 tokens/s 推至 54.4 tokens/s（**8.1× 加速**），精度仅从 79.3% 微降至 78.5%（−0.8 个百分点）。生成长度增至 512 时，加速比进一步扩大至 **11.0×**（3.2 → 35.3 tokens/s）。在 MATH、MBPP 等任务上，加速比稳定在 5.7×–7.5× 区间，HumanEval 甚至出现精度正增益（41.5% → 43.3%，+1.8 个百分点）。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_3Z3Is6hnOT/figures/007_Table_1.jpg]]
*Table 1: Comprehensive benchmark results on the LLaDA-Instruct suite. Each cell presents the accuracy and the decoding throughput in tokens per second with relative speedup to the LLaDA baseline (bottom row, blue: tokens per second/orange: relative speedup). The highest throughput and speedup for each configuration are highlighted*

这一性能增益并非 LLaDA 独有。Table 2 显示，在 Dream-Base 骨干上，Fast-dLLM 在 GSM8K（256 tokens）和 MBPP（512 tokens）分别实现 5.3× 和 7.8× 加速。多模态场景下（LLaDA-V，Table 3），MathVista 和 MathVerse 的吞吐分别提升 **9.9×** 和 8.5×，精度损失仅 2.6 和 −0.1 个百分点。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_3Z3Is6hnOT/figures/008_Table_2.jpg]]
*Table 2: Comprehensive benchmark results on Dream-Base variants over four tasks with different generation lengths (256 and 512). Each cell shows accuracy (top row) and decoding throughput in tokens per second with relative speedup to Dream-Base baseline (bottom row, blue: tokens per second/orange: relative speedup). Numbers in yellow indicate the highest throughput and speedup per configuration*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_3Z3Is6hnOT/figures/013_Table_3.jpg]]
*Table 3: Performance and Speedup Comparison of LLaDA-V on MathVista and MathVerse. Each benchmark includes results from Full Steps, Half Steps, and Fast-dLLM. Fast-dLLM significantly improves throughput (highlighted), with minimal accuracy loss*

**瓶颈-机制-证据链**：扩散大语言模型缺乏 KV 缓存，每次解码步需对全序列重新计算注意力，这是吞吐低下的根源。Fast-dLLM 通过块状近似 KV 缓存（PrefixCache/DualCache）复用相邻步的高相似性注意力激活（Figure 3 热力图显示块内相邻步余弦相似度接近 1），将冗余计算压缩至块更新时刻；置信度感知并行解码则在高置信度区间以边缘乘积近似联合分布，理论保证当 (n+1)ε ≤ 1 时贪婪解码等价（Theorem 1）。两者叠加，在 GSM8K 256-token 设定下实现 8.1× 吞吐跃升，精度仅降 0.8 个百分点，构成全文最坚实的因果证据。

### 组件拆解：缓存与并行解码的独立贡献

Figure 1(a) 和 Table 1 的行结构允许逐组件归因。单独启用 KV Cache（+Cache）在 GSM8K 256-token 上带来约 2.2× 加速（6.7 → 14.5 tokens/s），单独启用并行解码（+Parallel）贡献约 4.3× 加速（6.7 → 28.7 tokens/s）。两者组合（+Cache+Parallel）产生 8.1× 的总加速，超过各自贡献之和，说明缓存减少的每步计算量与并行解码减少的总步数之间存在乘法效应。

Figure 1(b) 进一步按“每步生成 token 数”和“总吞吐”两个维度分解贡献：并行解码大幅提升单步 token 产出（折线），缓存则降低每步的计算开销（柱状图），二者协同使总吞吐达到最高。

### 缓存机制消融

**块尺寸选择**：Figure 4 展示了缓存块大小对吞吐与精度的权衡。块尺寸过小（如 4）虽能最大化精度，但频繁的缓存更新引入额外开销；块尺寸过大（如 64）则因近似误差累积导致精度下降。块尺寸 **32** 在吞吐与精度之间取得最佳平衡，被选为主实验的默认配置。

**PrefixCache vs. DualCache**：Table 4 在 8-shot、生成长度 1024 的设定下对比了两种缓存策略。PrefixCache 实现 18.6× 加速，而 DualCache 进一步推至 **27.6×**（LLaDA 基线 0.7 → 19.3 tokens/s）。DualCache 同时缓存前缀和掩码后缀的 KV 激活，在长序列场景下复用率更高。Table 5 的生成长度扫描（256/512/1024）确认了这一趋势：生成长度越长，DualCache 的相对优势越显著。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_3Z3Is6hnOT/figures/015_Table_5.jpg]]
*Table 5: Impact of Generation Length on Accuracy and Speedup Under 8-Shot for LLaDA. This table illustrates the effect of varying generation lengths (256, 512, and 1024) on decoding performance and efficiency for different caching strategies under the 8- shot setting. Longer generation lengths lead to higher throughput gains, especially for DualCache, validating the scalability of our approach. We perform extensive ablations to assess the contribution of different components in Fast-dLLM, focusing on prefill length, generation length, cache variants, block size, and confidence thresholds*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_3Z3Is6hnOT/figures/014_Table_4.jpg]]

**Prefill 长度的影响**：Table 4 还揭示了 prefill 长度对加速比的调制作用。在 5-shot 设定下，DualCache 的加速比为 19.6×；增至 8-shot 后提升至 27.6×。更长的 prefill 意味着前缀 KV 缓存可复用的计算量更大，缓存命中率更高，这与 Figure 3(a) 中前缀区域的高相似性热力模式一致。

### 并行解码策略消融

**置信度阈值 vs. 固定 top-K**：Figure 5(a) 的红线展示了 GSM8K 精度随置信度阈值 τ 的变化，线上数字标注了每步平均解码 token 数。三条虚线分别代表固定每步解码 top-2/4/8 token 的基线精度。在任意每步平均 token 数下，置信度感知策略的精度均优于固定 top-K 基线（Figure 5(c)）。Figure 5(b) 进一步表明，置信度感知策略所需的总推理步数（NFE）更少——以更少的计算量生成更多有效 token。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_3Z3Is6hnOT/figures/012_Figure_5.jpg]]
*Figure 5: (a) The red line shows the GSM8K (5-shot) accuracy across different confidence thresholds. Numbers along the red line indicate the average number of tokens decoded at each step. The three dashed lines represent the accuracy of the baseline method when selecting the top 2, 4, or 8 tokens per step. (b) The number of inference steps required under varying confidence thresholds. (c) A comparison between our method and the baseline on GSM8K (5-shot) accuracy, plotted against the average number of tokens per step. Our method consistently outperforms the baseline*

**阈值解码 vs. 因子解码**：Table 11 对比了两种置信度感知策略。因子解码（基于 (n+1)(1−c⁽ⁿ⁾) < f 动态选择并行度 n）在同等精度水平下可获得比阈值解码更高的吞吐（如 GSM8K 512-token 上 14.7× vs. 11.0×）。Figure 8 的消融曲线确认了这一优势，并标注了主实验中选用的因子设定（红色 “Selected” 点）。因子解码的理论优势在于其直接控制了并行度与置信度衰减之间的权衡，而非依赖绝对阈值。

### 失败模式与局限性

**大批次场景的瓶颈转移**：Figure 9 的吞吐对比显示，当批大小增至 32 时，PrefixCache 虽仍显著优于 LLaDA 基线（211 vs. 43 tokens/s，近 5× 提升），但与同规模自回归模型 LLaMA 相比仍有差距。扩散模型在解码阶段的全注意力计算开销随批大小线性增长，缓存仅压缩了单序列内的冗余，无法消除跨序列注意力的计算负担。这是扩散解码的结构性局限，而非 Fast-dLLM 的方法缺陷。

**近似缓存的精度边界**：Figure 10（附录）展示了不同层间 KV 相似性的非均匀性——部分层的相似性随步间隔衰减更快。当前统一块尺寸和统一更新策略未利用这种层间差异，可能留下精度优化空间。当解码步间隔增大时，近似误差累积可能影响生成长序列的尾部质量，这在 1024-token 设定下已有微弱体现（Table 5 中 DualCache 的精度略低于 PrefixCache）。

**因子解码的超参数敏感性**：因子 f 需手动调节，缺乏任务自适应的自动选择机制。Table 11 中不同 f 值对应的吞吐与精度差异显著，说明该超参数对最终性能有实质性影响。

### 计算效率与显存开销

Table 14 的 FLOPs 与显存分析量化了缓存机制的计算收益。在输入+生成长度均为 256 的设定下，DualCache 将计算量从 LLaDA 基线的 7.68T FLOPs 压缩至 0.48T FLOPs（**16× 削减**），而峰值显存仅从 15.07G 微增至 15.36G。这一近乎零显存代价的计算压缩，源于块状缓存更新与解码步骤的联合计算——缓存更新不引入额外前向传播。

## 定位与知识库关联

### 核心瓶颈与设计动机

扩散大语言模型（Diffusion LLMs）在推理时面临双重效率瓶颈：**（1）缺乏KV缓存机制**，导致每个解码步需重新计算全序列注意力，计算冗余极高；**（2）并行解码中的条件独立性假设**破坏了token间的真实依赖关系，造成生成质量显著下降。Fast-dLLM正是围绕这两个瓶颈展开设计：一方面引入面向双向注意力的块状近似KV缓存（PrefixCache/DualCache），利用相邻解码步KV激活的高余弦相似度（≈1，见Figure 3）实现缓存复用；另一方面设计基于置信度阈值/因子的自适应并行解码策略，在理论保证（Theorem 1）下大幅减少冗余计算。

### 方法谱系

#### 扩散语言模型骨干

Fast-dLLM作为**免训练加速框架**，可适配多种扩散语言模型骨干：

- **LLaDA**（Nie et al., 2025b）：文本扩散大语言模型，采用掩码扩散（Masked Diffusion）前向过程与τ-leaping解码策略，是本文的主要验证平台。
- **Dream**（Ye et al., 2025）：另一文本扩散语言模型，同样基于掩码扩散范式，Fast-dLLM在其上的加速效果见Table 2。
- **LLaDA-V**（You et al., 2025）：多模态扩散模型（视觉-语言），Fast-dLLM首次将KV缓存与并行解码推广至多模态场景（Table 3）。
- **dParallel**（Chen et al., 2025b）：蒸馏少步扩散模型，Fast-dLLM的PrefixCache与之结合可实现13.7×吞吐提升（Table 13），但该组合在极端蒸馏（如单步扩散）上的下游任务表现尚未充分验证。

#### 与自回归模型的对比定位

扩散语言模型在推理效率上长期落后于自回归模型（如LLaMA），根本原因在于自回归模型天然支持因果KV缓存，而扩散模型的双向注意力使标准缓存不可用。Fast-dLLM通过块状生成策略绕开了这一限制，使得扩散模型首次获得可复用的KV缓存。然而，在较大批次（>8）下，扩散模型仍因全注意力计算开销落后于LLaMA（Figure 9），缓存带来的加速未能完全弥合这一结构性差距。

#### 并行解码策略的演进

扩散模型的并行解码源于τ-leaping策略（Eq.3），其核心思想是一次性恢复多个掩码token。早期方法（如LLaDA的固定top-K并行解码）对所有mask位置同等对待，忽略了token间的依赖关系。Fast-dLLM的置信度感知并行解码在此基础上引入了**选择性机制**：仅对高置信度token执行并行解码，并通过Theorem 1给出理论保证——当$(n+1)\varepsilon \le 1$时（其中$n$为并行解码token数，$\varepsilon$为置信度误差上界），贪婪并行解码与贪婪顺序解码等价。这一理论结果将并行解码从启发式策略提升为有界近似。

### 适用边界与局限

#### 缓存机制的适用条件

近似KV缓存的有效性依赖于**相邻解码步激活的高相似性假设**。Figure 3的热力图验证了这一假设在块内相邻步成立，但当解码步间隔增大时相似性下降（Figure 10），可能影响精度。这意味着：
- **块尺寸需要谨慎选择**：过小则缓存更新开销增大，过大则近似误差累积。消融实验（Figure 4）表明块大小32在吞吐与精度间取得最佳权衡。
- **长生成场景下DualCache优势更显著**：DualCache同时缓存前缀和掩码后缀token，在生成长度1024时达到27.6×加速（vs PrefixCache的18.6×，Table 4），因为后缀token的KV激活在块内多步解码中同样高度可复用。

#### 并行解码的适用范围

置信度感知策略在数学推理（GSM8K、MATH）和代码生成（HumanEval、MBPP）等任务上表现稳定，但其有效性依赖于模型对正确token的置信度集中程度。当模型不确定性较高（如开放域对话）时，高置信度token比例降低，并行度自然收缩，加速效果可能减弱。

#### 已知局限

1. **批次扩展性受限**：在较大批次（>8）下，扩散模型的全注意力计算开销仍使其落后于自回归模型LLaMA（Figure 9），缓存加速未能完全消除这一差距。
2. **超参数手动调节**：因子解码策略需手动设置超参数$f$，缺乏任务自适应的自动选择机制。阈值策略同样需要针对任务调整$\tau$。
3. **极端蒸馏场景未充分验证**：现有评估在蒸馏模型上仅涉及perplexity指标，下游任务表现未知（见limitations）。
4. **层间相似性非均匀性未利用**：Figure 10显示不同层KV相似性存在差异，当前统一缓存策略未对此进行层感知优化。

### 开放问题

1. **向少步扩散的泛化**：能否将Fast-dLLM的缓存与并行解码策略推广到一步或少数步扩散模型（如OneFlowSeq），实现更大推理加速？这需要重新审视缓存复用的相似性假设在极短解码链上的成立条件。

2. **层感知缓存策略**：Figure 10揭示了不同层KV相似性的非均匀性——某些层的激活变化更剧烈。是否可设计层感知或自适应缓存更新策略，对高相似层延长复用周期、对低相似层缩短更新间隔，从而在不增加显存开销的前提下提升近似精度？

3. **多模态注意力模式差异**：LLaDA-V的初步实验（Table 3）表明Fast-dLLM在多模态场景同样有效，但视觉token与语言token的注意力模式存在结构性差异，这种差异是否影响缓存重用的有效性？视觉token的空间冗余是否可被进一步利用？

4. **在线自适应决策**：能否通过轻量预测器（如小型MLP或统计检验）在线决策最优阈值$\tau$或因子$f$，从而避免手动调节并实现动态自适应？这需要设计无额外标注的在线信号（如置信度分布熵、解码步间token变化率）。

5. **大规模模型的边际效益**：当前实验基于~7B参数规模。在更大规模（>30B）扩散模型上，显存与计算减少的边际效益如何？KV缓存的显存开销（Table 14显示DualCache在256+256配置下仅增加0.29G）是否随模型规模线性扩展？

## 原文 PDF

![[paperPDFs/ICLR_2026/Fast_dLLM_Training_free_Acceleration_of_Diffusion_LLM_by_Enabling_KV_Cache_and_Parallel_Decoding.pdf]]
