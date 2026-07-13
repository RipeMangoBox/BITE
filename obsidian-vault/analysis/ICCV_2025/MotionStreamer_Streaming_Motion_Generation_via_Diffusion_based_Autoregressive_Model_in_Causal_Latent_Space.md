---
title: "MotionStreamer: Streaming Motion Generation via Diffusion-based Autoregressive Model in Causal Latent Space"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space.pdf
project_link: https://zju3dv.github.io/MotionStreamer/
code_link: null
aliases:
- MotionStreamer
tags:
- ICCV_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "将运动压缩器替换为因果时域自编码器（Causal TAE），在连续潜空间中进行运动表示，建立时间因果依赖关系以支持在线解码；将生成模型设计为集成扩散头的自回归Transformer，直接预测连续运动潜变量；同时引入Two-Forward训练和混合训练策略，减轻自回归曝光偏差并支持多轮文本输入。"
primary_logic: "通过采用连续因果潜空间，避免了离散量化瓶颈，使运动潜变量能够即时解码，实现真正流式生成；扩散头在自回归框架中生成高质量潜变量，既利用了扩散模型的优异生成能力，又保持了自回归的流式特性，从根本上解决了流式运动生成中的延迟、误差累积和信息损失问题。"
claims:
- "在HumanML3D测试集上，MotionStreamer在FID、R-Precision、MM-Dist等指标上全面超越现有方法，FID达到11.790，显著优于MoMask的12.232。"
- "在BABEL长期运动生成任务上，我们的方法在子序列和过渡段的FID均优于FlowMDM，过渡FID 32.888 vs 34.721，且动作更平滑。"
- "消融实验中，使用Causal TAE连续潜变量的生成FID（11.790）远优于VQ-VAE离散标记的FID（13.226），证明了连续表示的信息保留优势。"
- "Causal TAE实现了最低的首帧延迟，而传统非因果VAE必须等待整个序列生成完毕才能解码，导致延迟随帧数增加。"
---

# MotionStreamer: Streaming Motion Generation via Diffusion-based Autoregressive Model in Causal Latent Space

> [!tip] 核心洞察
> 通过采用连续因果潜空间，避免了离散量化瓶颈，使运动潜变量能够即时解码，实现真正流式生成；扩散头在自回归框架中生成高质量潜变量，既利用了扩散模型的优异生成能力，又保持了自回归的流式特性，从根本上解决了流式运动生成中的延迟、误差累积和信息损失问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionStreamer：基于因果潜空间扩散自回归模型的流式运动生成 |
| 英文题名 | MotionStreamer: Streaming Motion Generation via Diffusion-based Autoregressive Model in Causal Latent Space |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2411.18247) · [Project](https://zju3dv.github.io/MotionStreamer/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | MotionStreamer |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，FID ↓ 为 11.790，对比 12.232 (MoMask)，变化 -0.442。
> - HumanML3D 上，R@3 ↑ 为 0.859，对比 0.846 (MoMask)，变化 +0.013。
> - HumanML3D 上，MM-Dist ↓ 为 16.081，对比 16.138 (MoMask)，变化 -0.057。

## 概要

**核心问题**：现有运动生成方法无法同时实现流式生成与在线响应。基于扩散模型的方法受限于固定长度和非增量生成，无法处理动态变化的文本输入；基于GPT的自回归方法则依赖非因果VQ-VAE离散tokenization，导致解码延迟、误差累积以及离散化带来的运动细节信息损失，严重影响长序列生成质量。

**核心方案**：MotionStreamer 提出两大关键创新来解决上述瓶颈。其一，将运动压缩器替换为**因果时域自编码器（Causal TAE）**，在连续潜空间中进行运动表示，建立时间因果依赖关系以支持在线解码，从根本上避免了离散量化瓶颈。其二，将生成模型设计为**集成扩散头的自回归Transformer**，直接预测连续运动潜变量，既利用扩散模型的优异生成能力，又保持自回归的流式特性。此外，引入Two-Forward训练策略减轻自回归曝光偏差，并通过混合训练策略统一原子文本-运动对与上下文三元组，支持多轮文本输入。

**方法定位**：MotionStreamer 在方法谱系中处于扩散模型与自回归模型的交叉地带。与纯扩散模型（如MDM、MLD）相比，它具备流式增量生成能力；与基于VQ-VAE + GPT的自回归方法（如T2M-GPT、MotionGPT、MoMask）相比，它用连续因果潜空间替代离散tokenization，消除了量化信息损失和解码延迟。其运动压缩器从非因果VQ-VAE变为因果TAE，生成模型从预测离散token变为扩散头预测连续潜变量，训练策略从单一teacher forcing升级为Two-Forward，运动表示也从263维（需IK后处理）升级为272维6D旋转（直接驱动SMPL）。

**主要结果**：在HumanML3D测试集上，MotionStreamer在FID（11.790 vs 12.232）、R-Precision（R@3: 0.859 vs 0.846）、MM-Dist（16.081 vs 16.138）等指标上全面超越MoMask（Table 1）。在BABEL长期运动生成任务上，子序列FID（15.743 vs 18.736）和过渡段FID（32.888 vs 34.721）均显著优于FlowMDM（Table 2）。消融实验证实，Causal TAE连续潜变量的生成FID（11.790）远优于VQ-VAE离散标记（13.226），证明了连续表示的信息保留优势（Table 3）。此外，Causal TAE实现了最低的首帧延迟，而传统非因果VAE必须等待整个序列生成完毕才能解码（Figure 4）。

### 流式运动生成的核心瓶颈

人体运动生成在数字人、游戏和影视领域有广泛需求。然而，现有方法在**流式生成**与**在线响应**两个关键能力上存在根本性矛盾：扩散模型受限于固定长度和非增量生成，无法处理动态变化的文本输入；基于GPT的自回归方法则依赖非因果VQ-VAE进行离散tokenization，导致解码延迟和误差累积，且离散化造成运动细节信息损失，严重影响长序列生成质量。

这一瓶颈的本质在于两个技术路线的结构性缺陷。**扩散模型**（如MDM、MLD）虽然生成质量优异，但需要完整噪声序列的迭代去噪，天然不支持逐帧流式输出。**自回归方法**（如T2M-GPT、MotionGPT、MoMask）虽然具备序列生成能力，却普遍采用基于VQ-VAE的离散运动表示——编码器使用非因果卷积，必须等待完整序列才能编码；解码器同样非因果，无法在潜变量生成后立即解码对应帧。更关键的是，离散量化过程引入的信息损失在长序列中持续累积，导致动作跳跃、脚下打滑等典型错误。

### 现有方法的缺口

从运动表示和生成范式两个维度审视，现有方法存在以下缺口：

1. **运动压缩的非因果性**：VQ-VAE及其变体（RVQ-VAE）使用标准卷积，缺乏时间因果约束。即使生成模型能逐token预测，解码器仍需等待完整潜变量序列，首帧延迟随帧数线性增长，无法实现真正的在线输出。

2. **离散量化的信息损失**：将连续运动映射到有限码本，不可避免地丢失关节旋转、速度等精细信息。消融实验证实，使用VQ-VAE离散标记的生成FID为13.226，而连续潜变量可将FID降至11.790（Table 3），差距显著。

3. **生成范式的割裂**：扩散模型擅长高质量生成但不支持流式，自回归模型支持流式但受限于离散表示的质量瓶颈。两种范式的优势未能统一。

### MotionStreamer的动机与核心思路

针对上述缺口，MotionStreamer提出了一条新路径：**在连续因果潜空间中，用扩散头增强的自回归Transformer实现流式运动生成**。其核心逻辑包含三个层面：

- **因果时域自编码器（Causal TAE）** 替代VQ-VAE，在连续潜空间中进行运动压缩，通过1D时间因果卷积建立潜变量间的时间依赖关系，使每个潜变量仅依赖历史帧。这从根本上消除了离散量化瓶颈，并支持在线解码——每个潜变量生成后即可解码为对应运动帧。

- **扩散头集成自回归Transformer** 直接预测连续运动潜变量，而非离散token。扩散头在自回归框架中逐段去噪生成高质量潜变量，既保留了扩散模型的优异生成能力，又继承了自回归的流式特性。

- **Two-Forward训练与混合训练策略** 分别解决自回归曝光偏差和多轮文本输入问题。Two-Forward策略在训练中逐步引入模型自身预测的潜变量替代真实值，混合训练则统一原子文本-运动对和上下文三元组，使模型同时具备单轮生成和在线续写能力。

通过上述设计，MotionStreamer首次实现了真正意义上的流式运动生成：文本增量输入，运动帧即时输出，且生成质量在HumanML3D和BABEL基准上全面超越现有方法。

## 核心方法与创新机理

MotionStreamer 的核心创新在于将**连续因果潜空间**与**扩散自回归模型**深度耦合，从根本上重构了流式运动生成的范式。这一设计通过三个关键“changed slots”实现了对现有方法的突破。

### 从离散量化到连续因果潜空间

现有基于自回归的运动生成方法（如 T2M-GPT、MotionGPT、MoMask）普遍采用 VQ-VAE 将运动序列离散化为 token，再交由 GPT 类模型逐 token 预测。这一范式存在两个结构性缺陷：**离散量化造成运动细节信息损失**，尤其在长序列生成中误差会逐步累积；**非因果的编码方式要求完整序列才能解码**，无法支持流式输出。

MotionStreamer 用 **Causal TAE（因果时域自编码器）** 替换了 VQ-VAE。Causal TAE 在编码器和解码器中均采用 1D 因果卷积，在序列起始端进行时间填充（pad $(k_t - 1) \times d_t + (1 - s_t)$ 帧），确保每个潜变量 $z_i$ 仅依赖于当前及过去的运动帧，建立起严格的时间因果依赖关系。潜变量从连续高斯分布中采样，完全避免了离散量化的信息瓶颈。

这一替换的直接效果体现在两个层面：
- **信息保留**：消融实验（Table 3）显示，Causal TAE 连续潜变量的生成 FID 为 **11.790**，而 VQ-VAE 离散 token 的 FID 高达 **13.226**，差距显著。定性可视化（Figure 5）进一步印证，VQ 方法生成的动作出现跳跃、脚下打滑等伪影，而连续潜空间方法生成的动作更加准确，细节保留更好。
- **流式解码**：因果结构使得每生成一个潜变量即可立即解码为对应的人体运动帧。Figure 4 的首帧延迟对比表明，Causal TAE 实现了最低的首帧延迟，且延迟不随生成帧数增加而增长；而非因果 VAE 必须等待整个序列生成完毕才能解码，延迟随帧数线性上升。

### 从离散 token 预测到扩散头生成连续潜变量

传统自回归方法用 GPT 预测离散 token，本质上是分类问题，难以捕捉运动潜空间的连续性和多模态分布。MotionStreamer 将生成模型设计为**集成扩散头的自回归 Transformer**：AR Transformer 接收文本嵌入和历史运动潜变量，通过因果掩码自注意力处理序列上下文，扩散头则在高斯噪声空间中执行去噪过程，直接预测下一段连续运动潜变量序列。

扩散头的训练目标为标准噪声预测损失：

$$\mathcal{L} = \mathbb{E}_{\epsilon, t} [ || \epsilon - \epsilon_\theta ( Z_t | t, C_i, T_i ) ||^2 ]$$

其中 $Z_t$ 为加噪后的目标潜变量，$C_i$ 为历史潜变量条件，$T_i$ 为文本嵌入条件。推理时，扩散头从纯噪声出发，经过多步去噪生成高质量潜变量，再通过无分类器引导增强文本跟随：

$$\epsilon_g = \epsilon_u + s ( \epsilon_c - \epsilon_u )$$

消融实验（Table 4）表明，移除扩散头改用 MSE 损失直接回归潜变量，生成质量显著下降，证明扩散去噪过程对于捕捉运动分布的多模态性和生成高质量样本至关重要。最优引导尺度 $s=4.0$（Figure 7）。

### 从 Teacher Forcing 到 Two-Forward 训练

自回归模型的标准训练方式——Teacher Forcing——在推理时面临严重的曝光偏差（exposure bias）：训练时使用真实历史 token，推理时却使用模型自身预测的历史 token，误差随序列增长而累积。

MotionStreamer 提出 **Two-Forward 训练策略**来缓解这一问题。第一轮前向传播使用真实运动潜变量作为历史条件；第二轮前向传播则将部分真实潜变量替换为第一轮预测的潜变量，替换比例由余弦调度器控制：

$$\gamma_t = \frac{1}{2} (1 - \cos(\frac{\pi t}{T}))$$

这种混合历史条件的训练方式使模型逐步适应自身预测误差，有效弥合了训练与推理之间的分布偏移。Table 4 的消融结果证实，Two-Forward 策略配合 QK 归一化（稳定自回归训练）对整体指标有显著提升。

### 从固定长度生成到连续停止机制

流式生成需要模型自主判断何时停止。MotionStreamer 摒弃了二元分类器或固定长度的方案，转而编码一个“不可能姿态”（all-zero impossible pose）作为参考结束潜变量。当生成潜变量与该参考潜变量的距离低于预设阈值时，生成过程终止。这一连续停止条件与 Causal TAE 的连续潜空间天然兼容，实现简洁。实验表明二元分类器方法无法正确训练，而连续参考结束潜变量方案可行且稳定。

### 从单一文本-运动对到混合训练

为支持流式场景中动态变化的文本输入，MotionStreamer 采用**混合训练策略**，将原子文本-运动对 $(T_i, Z_i)$ 和上下文三元组 $(T_i, C_i, Z_i)$ 统一到同一训练框架中。这使得模型既能从零开始生成运动（仅依赖文本），也能基于已有运动历史和新的文本指令继续生成，为动态运动组合（Figure 6）等应用奠定了基础。

### 运动表示的改进

MotionStreamer 对运动表示做了细微但关键的调整：将传统的 263 维表示（需要逆运动学 IK 后处理）替换为 **272 维 6D 旋转表示**，直接使用 SMPL 关节旋转，包含根速度、角速度、局部关节位置、速度和 6D 旋转：

$$x = \{ \dot{r}^x, \dot{r}^z, \dot{r}^a, \dot{\jmath}^p, \dot{\jmath}^v, \dot{\jmath}^r \}$$

这一表示可直接驱动 SMPL 模型，避免了 IK 后处理引入的误差和不自然姿态（Figure 8 展示了 IK 导致的抖动问题）。

MotionStreamer 的 pipeline 围绕**流式因果潜变量生成**这一核心思想构建，由四个关键模块串联形成端到端的在线推理流程（Figure 2）。

![[assets/figures/papers/paper_list_l26_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregre/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MotionStreamer. During inference, the AR model streamingly predicts next motion latents conditioned on the current text and previous motion latents. Each latent can be decoded into motion frames online as soon as it is generated*

**输入层**：用户以增量方式提供文本描述，每个时间步的文本 $T_i$ 通过预训练语言模型（默认 T5-XXL）编码为固定维度的文本嵌入。运动姿态采用 272 维表示 $x = \{ \dot{r}^x, \dot{r}^z, \dot{r}^a, \dot{\jmath}^p, \dot{\jmath}^v, \dot{\jmath}^r \}$，包含根关节的线速度和角速度、局部关节位置、速度及 6D 旋转，可直接驱动 SMPL 模型，避免了传统 263 维表示所需的逆运动学后处理。

**压缩模块 — Causal TAE**：因果时域自编码器将原始运动序列压缩到连续潜空间。编码器和解码器均采用一维时序因果卷积，通过在序列起始端填充 $(k_t - 1) \times d_t + (1 - s_t)$ 帧来严格保证时间因果性——即每个潜变量 $z_i$ 仅依赖于当前及过去的运动帧，无法窥视未来。这种因果约束是实现在线解码的架构基础：解码器每收到一个潜变量即可立即输出对应的人体姿态帧，无需等待完整序列生成完毕。

**生成模块 — 扩散头自回归 Transformer**：这是框架的核心创新。自回归 Transformer 接收当前文本嵌入 $T_i$ 和历史运动潜变量 $C_i$ 作为条件，通过因果掩码自注意力处理时序依赖，随后由扩散头对目标潜变量 $Z_i$ 执行去噪生成。具体而言，扩散头在噪声潜变量 $Z_t$ 上预测噪声 $\epsilon_\theta(Z_t | t, C_i, T_i)$，通过多步去噪逐步精炼出高质量的运动潜变量。这种设计将扩散模型的优异生成能力嵌入自回归框架，既保持了逐段生成的流式特性，又避免了离散 tokenization 的信息损失。

**输出层 — 在线解码**：生成的运动潜变量被送入 Causal TAE 解码器，即时转化为人体运动帧。由于因果结构的存在，每预测出一个潜变量序列即可解码对应帧，形成真正的流式输出。推理过程循环执行：历史潜变量窗口随生成推进而滑动，新文本到达时更新条件嵌入，直至遇到停止条件（连续参考结束潜变量）终止生成。

**训练策略的协同设计**：为支撑上述推理流程，训练阶段引入了两项关键策略。**Two-Forward 训练**在第一轮前向中使用真实潜变量进行 teacher forcing，第二轮前向中按余弦调度器 $\gamma_t = \frac{1}{2}(1 - \cos(\frac{\pi t}{T}))$ 逐步替换部分真实潜变量为第一轮的预测值，有效缓解自回归模型的曝光偏差。**混合训练**统一处理原子文本-运动对和上下文三元组（文本，历史运动，当前运动），使模型同时学会从零开始生成和基于历史继续生成，为流式场景中的多轮文本输入提供支持。

### 运动表示与问题形式化

MotionStreamer 将人体运动表示为 272 维姿态向量，直接驱动 SMPL 模型，避免传统 263 维表示所需的逆运动学（IK）后处理。每帧姿态由以下分量构成：

$$x = \{ \dot{r}^x, \dot{r}^z, \dot{r}^a, \dot{\jmath}^p, \dot{\jmath}^v, \dot{\jmath}^r \}$$

其中 $\dot{r}^x, \dot{r}^z$ 为根节点在 XZ 平面上的线速度（2 维），$\dot{r}^a$ 为根节点绕 Y 轴的角速度（6 维 6D 旋转表示），$\dot{\jmath}^p, \dot{\jmath}^v, \dot{\jmath}^r$ 分别为 22 个局部关节相对于根节点的位置（3×22 维）、速度（3×22 维）和 6D 旋转（6×22 维），合计 272 维。6D 旋转表示的引入使得旋转量的学习更加连续和平滑，且可直接映射到 SMPL 关节旋转。

### 因果时域自编码器（Causal TAE）

Causal TAE 是 MotionStreamer 流式能力的核心使能模块。其设计目标是将原始运动序列压缩为连续潜变量表示，同时严格保持时间因果性——即每一时刻的潜变量仅依赖于当前及过去的运动帧，不得访问未来信息。

**因果卷积架构**：编码器 $E$ 和解码器 $D$ 均采用一维时域因果卷积构建。对于卷积核大小 $k_t$、膨胀系数 $d_t$ 和步长 $s_t$，在序列起始处填充 $(k_t - 1) \times d_t + (1 - s_t)$ 帧，确保卷积操作不跨越未来时间步。这一设计使得编码器可在线处理流式输入，解码器可在每个潜变量生成后立即输出对应运动帧，无需等待完整序列。

**训练损失函数**：Causal TAE 采用 $\sigma$-VAE 风格的完整训练目标：

$$\mathcal{L} = \mathcal{L}_{recon} + D_{KL}(q(z|x)||p(z)) + \lambda \mathcal{L}_{root}$$

**重建损失** $\mathcal{L}_{recon}$ 使用解析标准差进行自适应加权：

$$\mathcal{L}_{recon} = \sum_{d=1}^{D} \sum_{i=1}^{N} \left( \frac{(x_{di} - \hat{x}_{di})^2}{2{\sigma^*}^2} + \ln \sigma^* \right)$$

其中 $D$ 为运动表示维度（272），$N$ 为序列帧数，$\sigma^*$ 为可学习的解析标准差参数，使模型自动平衡各维度的重建精度。

**根关节损失** $\mathcal{L}_{root}$ 专门针对根关节分量施加额外约束，增强根轨迹的稳定性：

$$\mathcal{L}_{root} = \sum_{d=1}^{D_{root}} \sum_{i=1}^{N} \left( \frac{(x_{di} - \hat{x}_{di})^2}{2{\sigma^*}^2} + \ln \sigma^* \right)$$

**KL 散度** 约束潜变量分布 $q(z|x)$ 接近标准正态先验 $p(z) = \mathcal{N}(0, I)$：

$$D_{KL}(q(z|x)||p(z)) = \frac{1}{2} \sum_{d=1}^{d_c} \sum_{i'=1}^{N/l} \left( \mu_{di'}^2 + \sigma_{di'}^2 - \ln(\sigma_{di'}^2) - 1 \right)$$

其中 $d_c$ 为潜变量维度，$l$ 为时间下采样率，$\mu_{di'}$ 和 $\sigma_{di'}$ 为编码器输出的分布参数。

消融实验（Table 3）证实，Causal TAE 的重建 FID（0.661）和 MPJPE（22.9mm）均优于 VQ-VAE 和非因果 VAE，且其连续潜空间使下游生成 FID 从 VQ-VAE 的 13.226 降至 11.790，验证了连续表示对信息保留的关键作用。

### 扩散自回归 Transformer

MotionStreamer 的生成模型将扩散头集成到自回归 Transformer 框架中，直接预测连续运动潜变量。每个训练样本 $S_i = (T_i, C_i, Z_i)$ 包含三个组件：文本嵌入 $T_i$（由预训练 T5-XXL 提取）、历史运动潜变量 $C_i$（先前已生成的潜变量序列）、以及当前目标运动潜变量 $Z_i$。

**扩散损失**：对目标潜变量 $Z_i$ 施加前向扩散过程，在第 $t$ 步得到加噪潜变量 $Z_t$，模型学习预测所加噪声 $\epsilon$：

$$\mathcal{L} = \mathbb{E}_{\epsilon, t} [ || \epsilon - \epsilon_\theta ( Z_t | t, C_i, T_i ) ||^2 ]$$

其中 $\epsilon_\theta$ 为以时间步 $t$、历史潜变量 $C_i$ 和文本嵌入 $T_i$ 为条件的噪声预测网络。推理时，模型从随机噪声出发，通过多步去噪生成下一组运动潜变量。

**无分类器引导**（Classifier-Free Guidance）在推理时增强文本条件控制：

$$\epsilon_g = \epsilon_u + s ( \epsilon_c - \epsilon_u )$$

其中 $\epsilon_u$ 为无条件噪声预测，$\epsilon_c$ 为文本条件噪声预测，$s$ 为引导尺度。消融实验（Figure 7）表明 $s=4.0$ 在所有实验中取得最佳生成质量。

**停止条件**：模型额外编码一个“不可能姿态”（all-zero impossible pose）作为连续参考结束潜变量。生成过程中，当预测潜变量与该参考潜变量的距离低于手动设定阈值时，自动终止生成。消融表明该方案可行，而二元分类器方法无法正确训练。

### Two-Forward 训练策略

为缓解自回归模型固有的曝光偏差（exposure bias），MotionStreamer 引入 Two-Forward 训练策略。第一次前向使用全部真实潜变量作为历史条件生成预测潜变量；第二次前向则按余弦调度器 $\gamma_t = \frac{1}{2} (1 - \cos(\frac{\pi t}{T}))$ 的比例，将部分真实历史潜变量替换为第一次前向的预测值，形成混合历史条件再次前向。这一策略使模型逐步适应自身预测误差，消融实验（Table 4）证实其有效提升整体指标，配合 QK 归一化进一步稳定训练。

### 混合训练策略

训练数据统一为两种模式：原子对 $(T_i, \emptyset, Z_i)$ 模拟文本到运动的冷启动生成；上下文三元组 $(T_i, C_i, Z_i)$ 模拟流式生成中的延续预测。混合训练使单一模型同时掌握从零开始生成和基于历史继续生成的能力，支持动态文本输入下的在线响应。

## 实验与关键发现

### 核心实验设置

MotionStreamer 的实验评估围绕两个核心基准展开：**HumanML3D** 用于标准文本到运动生成，**BABEL** 用于长期运动生成。所有基线方法均从零开始按照原始实现训练，并统一使用 272 维 SMPL 运动表示数据，评估器采用 TMR 训练以获得公平的跨方法比较。运动表示从传统的 263 维扩展为 272 维，直接包含局部关节的 6D 旋转，消除了对逆运动学后处理的需求，可直接驱动 SMPL 模型。

### 主实验结果

#### 文本到运动生成

在 HumanML3D 测试集上（Table 1），MotionStreamer 在多个关键指标上全面超越现有方法。与当前最佳方法 **MoMask** 相比，FID 从 12.232 降至 **11.790**，R@3 从 0.846 提升至 **0.859**，MM-Dist 从 16.138 降至 **16.081**。这一性能优势源于连续因果潜空间对运动细节的完整保留，以及扩散头在自回归框架中提供的高质量潜变量生成能力。相比之下，基于 VQ-VAE 离散 tokenization 的方法（如 T2M-GPT、MotionGPT、MoMask）因量化误差累积而损失信息，基于标准扩散模型的方法（如 MDM、MLD）则受限于固定长度生成范式。

![[assets/figures/papers/paper_list_l26_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregre/figures/005_Table_1.jpg]]
*Table 1: Comparison with baseline text-to-motion generation methods on HumanML3D [20] test set. MM-D and Div denote Multimodal Distance and Diversity respectively*

#### 长期运动生成

在 BABEL 长期运动生成任务上（Table 2），MotionStreamer 在子序列和过渡段两个维度均显著优于 **FlowMDM**（基于流的扩散方法）。子序列 FID 从 18.736 降至 **15.743**，过渡段 FID 从 34.721 降至 **32.888**，子序列 R@3 从 0.492 提升至 **0.568**。这表明因果潜空间中的自回归生成能够更好地维持长序列中的运动连贯性，避免离散方法在长序列生成中出现的误差累积和动作跳跃问题。

![[assets/figures/papers/paper_list_l26_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregre/figures/006_Table_2.jpg]]
*Table 2: Comparison with long-term motion generation methods on BABEL [54] dataset*

### 流式生成延迟分析

Figure 4 展示了不同方法的**首帧延迟**对比。Causal TAE 实现了最低的首帧延迟，且延迟不随生成帧数增加而增长，因为每个运动潜变量在生成后即可立即解码为运动帧。相比之下，非因果 VAE 必须等待整个序列生成完毕才能解码，导致延迟随帧数线性增长；VQ-VAE 方法虽然支持逐 token 解码，但离散化过程引入了额外的解码开销。这一结果直接验证了因果时域自编码器在流式生成场景中的核心优势。

### 消融实验

#### 运动压缩器对比

Table 3 对比了不同运动压缩器的重建与生成质量。使用 Causal TAE 连续潜变量的生成 FID 为 **11.790**，远优于 VQ-VAE 离散标记的 **13.226**，证明了连续表示对运动细节的信息保留优势。同时，Causal TAE 的重建 FID 为 0.661，MPJPE 为 22.9mm，优于非因果 VAE 和标准自编码器，表明因果约束并未损害压缩质量。

![[assets/figures/papers/paper_list_l26_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregre/figures/009_Table_3.jpg]]
*Table 3: Ablation Study of different motion compressors on HumanML3D [20] test set. MPJPE is measured in millimeters*

#### AR 模型设计选择

Table 4 分析了自回归模型的关键设计选择。移除扩散头改用 MSE 损失直接预测潜变量，生成质量显著下降，验证了扩散去噪过程对于高质量生成至关重要。Two-Forward 训练策略配合 QK 归一化有效减轻了自回归模型的曝光偏差问题，提升了整体指标。使用 T5-XXL 作为文本编码器优于 CLIP，表明更强的语言理解能力有助于运动-文本对齐。

#### 架构超参数

Table 6 显示 Causal TAE 在潜变量维度 16、隐藏大小 1024 时达到最佳重建-生成权衡。Table 7 表明 AR 模型采用 12 层 Transformer、12 注意力头、768 隐藏维、9 层扩散头时性能最优。无分类器引导尺度 s=4.0 在所有实验中取得最佳生成质量（Figure 7）。

![[assets/figures/papers/paper_list_l26_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregre/figures/012_Table_6.jpg]]
*Table 6: Ablation Study of different Causal TAE architecture designs on HumanML3D [20] test set. Each generation model remains the same. MPJPE is measured in millimeters. (16, 1024) indicates the latent dimension and hidden size of the Causal TAE*

![[assets/figures/papers/paper_list_l26_MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregre/figures/014_Table_7.jpg]]
*Table 7: Ablation study of AR Model architecture on HumanML3D [20] test set. For each architecture, we use the same Causal TAE*

### 定性分析

Figure 5 的定性可视化显示，VQ 方法生成的动作出现跳跃、脚下打滑等典型错误，而 MotionStreamer 的连续潜空间方法生成的动作更加准确，细节保留更好。在长期生成场景中，我们的方法在过渡段保持动作平滑，避免了 FlowMDM 等基线方法中出现的突变和抖动。

### 失败模式与局限

Figure 8 展示了一个典型失败案例：当使用逆运动学从相对关节位置直接求解关节旋转时，会产生不自然的身体抖动。MotionStreamer 通过直接使用 6D 旋转表示规避了这一问题，但在需要 IK 后处理的传统表示中，该问题仍然存在。

流式生成的单向因果架构限制了运动插值和局部编辑的能力，无法在任意中间点插入或修改动作，这影响了需要精细调整的交互式场景。此外，连续参考结束潜变量（基于“不可能姿态”的 all-zero 潜变量）虽然简化了停止机制，但其性能可能依赖于手动设定的距离阈值，在边界情况下可能出现提前停止或延迟停止的问题。

## 定位与知识库关联

### 1. 问题定位：流式生成与在线响应的双重缺失

现有文本驱动人体运动生成方法可归为两大范式，但均无法同时满足“流式生成”与“在线响应”的需求：

**扩散模型范式**（如 **MDM**、**MLD**、**FlowMDM**）虽然生成质量优异，但受限于固定长度的非增量生成机制。这类方法需预定义运动时长，在推理时一次性去噪生成完整序列，无法处理动态变化的增量文本输入。当文本指令逐句到达时，扩散模型必须重新生成整个序列，导致计算冗余和响应延迟。

**自回归范式**（如 **T2M-GPT**、**MotionGPT**、**MoMask**）通过 GPT 类模型逐 token 预测运动序列，天然支持变长生成。然而，这些方法依赖 VQ-VAE 或 RVQ-VAE 将连续运动量化为离散 token，引入了双重瓶颈：（1）离散量化造成运动细节信息损失，影响长序列生成的保真度；（2）解码器通常采用非因果架构，必须等待整个潜变量序列生成完毕后才能解码，无法实现逐帧即时输出。此外，离散 token 的自回归预测存在误差累积问题，在长序列生成中尤为突出。

**核心瓶颈**：现有方法在“流式生成范式”和“连续表示质量”之间面临根本性权衡——扩散模型提供高质量连续生成但缺乏流式能力，VQ-GPT 提供自回归流式框架但受限于离散量化的信息损失和非因果解码的延迟。

### 2. MotionStreamer 的方法学突破

MotionStreamer 通过两个关键设计打破了上述权衡，建立起“连续因果潜空间 + 扩散自回归”的新范式：

**因果时域自编码器（Causal TAE）**：将传统 VQ-VAE 的离散 tokenization 替换为连续潜变量压缩，同时强制时间因果依赖关系。编码器和解码器均采用 1D 因果卷积，保证每个潜变量仅依赖当前及过去的运动帧，从根本上支持在线解码——每生成一个潜变量即可即时解码为对应的人体姿态帧，无需等待完整序列。这消除了 VQ-VAE 的量化误差和非因果 VAE 的解码延迟。

**扩散头集成自回归 Transformer**：在自回归框架中引入扩散模型作为生成头，直接预测下一组连续运动潜变量。自回归 Transformer 负责建模文本条件与历史潜变量的时序依赖，扩散头则在潜空间中进行迭代去噪生成，兼顾了自回归的流式特性和扩散模型的高质量生成能力。这与 **T2M-GPT** 等预测离散 token 的方法形成本质区别：连续潜空间避免了离散化导致的信息损失，扩散去噪过程提供了比交叉熵损失更精细的分布建模。

**配套训练策略**：
- **Two-Forward 策略**：首轮前向使用真实潜变量作为历史条件，次轮前向将部分真实潜变量替换为首轮预测值，逐步引入自生成上下文，有效减轻自回归模型的曝光偏差（exposure bias）。
- **混合训练**：统一处理原子（文本，运动）对和上下文（文本，历史运动，当前运动）三元组，使单一模型同时支持从头生成和条件续写，无需额外的 fine-tuning 阶段。
- **连续停止条件**：引入“不可能姿态”（all-zero pose）编码为参考结束潜变量，通过潜空间距离判断生成终止，替代了 VQ 方法中常用的二元分类器。

### 3. 与基线方法的系统性对比

| 方法 | 运动表示 | 生成范式 | 流式支持 | 关键局限 |
|------|----------|----------|----------|----------|
| **MDM** | 原始运动帧 | 扩散模型 | ✗ | 固定长度，无法增量生成 |
| **MLD** | VAE 连续潜变量 | 潜扩散 | ✗ | 非因果 VAE，需完整序列解码 |
| **T2M-GPT** | VQ-VAE 离散 token | 自回归 GPT | 部分 | 离散量化损失，非因果解码 |
| **MoMask** | RVQ-VAE 多层离散 token | 掩码 Transformer | ✗ | 多层量化误差累积，非流式 |
| **MotionGPT** | VQ-VAE 离散 token | 自回归 GPT | 部分 | 同 T2M-GPT |
| **FlowMDM** | 原始运动帧 | 流匹配扩散 | ✗ | 固定长度生成 |
| **MotionStreamer** | **Causal TAE 连续潜变量** | **扩散头 + 自回归 Transformer** | **✓ 完全流式** | 单向因果限制插值编辑 |

在 **HumanML3D** 基准上，MotionStreamer 以 FID **11.790** 超越 MoMask 的 12.232，同时在 R-Precision（R@3: 0.859 vs 0.846）和 MM-Dist（16.081 vs 16.138）上全面领先（Table 1）。在 **BABEL** 长期运动生成任务上，子序列 FID（15.743 vs FlowMDM 18.736）和过渡段 FID（32.888 vs 34.721）均显著更优（Table 2），证明连续潜空间在长序列建模中的信息保留优势。

消融实验（Table 3）提供了决定性证据：使用 Causal TAE 连续潜变量的生成 FID 为 11.790，而相同架构下使用 VQ-VAE 离散 token 的 FID 恶化至 13.226，直接验证了连续表示对生成质量的关键作用。移除扩散头改用 MSE 损失后，生成质量显著下降（Table 4），证明扩散去噪过程对高质量潜变量预测不可或缺。

### 4. 适用边界与局限

**适用场景**：
- 增量文本驱动的流式运动生成，如实时人机交互、游戏角色控制
- 长序列运动生成与动态运动组合（Figure 6），支持多段文本依次输入且保持历史运动不变
- 需要低首帧延迟的在线应用（Figure 4 显示 Causal TAE 的首帧延迟恒定且最低）

**已知局限**：
1. **单向因果架构限制交互式编辑**：流式生成的因果约束意味着模型只能前向预测，无法在已生成序列的任意中间点插入或修改动作。这限制了需要精细调整的交互式运动编辑场景（如动画后期修正）。论文明确将此列为方法的内在限制。
2. **停止条件的阈值敏感性**：连续参考结束潜变量虽然简化了停止机制，但其性能可能依赖于手动设定的距离阈值，在分布外文本输入下可能出现提前终止或延迟终止。
3. **逆运动学（IK）后处理的固有问题**：论文在 Figure 8 中展示了 IK 求解导致的失败案例——直接从相对关节位置求解关节旋转可能产生不自然的身体抖动。尽管采用了 6D 旋转表示改善学习，IK 后处理仍是潜在的质量瓶颈。

### 5. 开放问题

1. **双向精炼与流式生成的兼容性**：能否在保持因果流式推理的前提下，通过预测多个未来潜变量实现局部双向精炼？这需要在不破坏因果掩码的条件下引入有限的未来信息。

2. **中间帧插入与局部编辑**：如何在流式生成范式中支持“在已生成序列的第 k 帧后插入新动作”这类操作？可能的思路包括条件掩码生成或可逆潜空间操作，但需解决因果依赖链的断裂问题。

3. **多模态条件扩展**：当前方法仅支持文本条件，能否将因果潜空间框架扩展至音频、场景上下文等多模态条件，同时保持流式生成的实时性？

4. **更长序列的误差累积**：虽然连续潜空间缓解了离散量化的误差累积，但自回归生成在超长序列（数千帧）上的漂移问题仍需进一步研究，可能需要引入全局规划或周期性重锚定机制。

## 原文 PDF

![[paperPDFs/ICCV_2025/MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space.pdf]]
