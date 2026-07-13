---
title: "WaveAR: Wavelet-Aware Continuous Autoregressive Diffusion for Accurate Human Motion Prediction"
type: paper
paper_level: A
venue: NEURIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/WaveAR_Wavelet-Aware_Continuous_Autoregressive_Diffusion_for_Accurate_Human_Motion_Prediction.pdf
project_link: null
code_link: null
aliases:
- WaveAR
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用连续潜变量替代离散化，通过离散小波变换（DWT）提取多尺度高频子带，并利用交叉注意力融合到 masked autoregressive diffusion 中，从而恢复精细运动细节并提升预测准确性。
primary_logic: 连续自回归生成与小波多频率引导相结合，既避免了量化误差，又能捕获运动序列的高低频动态，实现高保真度、高准确度的随机人体运动预测。
claims:
- WaveAR 在 Human3.6M 和 HumanEva-I 上均取得最优 ADE 和 FDE 指标，超过 SOTA 方法。
- HumanEva-I 上 ADE / FDE = 0.199 / 0.201
- Human3.6M 上 ADE / FDE = 0.347 / 0.452
- Human3.6M (推理时间) 上 Inference Time (s) / Params (M) = 0.65s / 86.5M
---

# WaveAR: Wavelet-Aware Continuous Autoregressive Diffusion for Accurate Human Motion Prediction

> [!tip] 核心洞察
> 连续自回归生成与小波多频率引导相结合，既避免了量化误差，又能捕获运动序列的高低频动态，实现高保真度、高准确度的随机人体运动预测。

| 字段 | 内容 |
|------|------|
| 中文题名 | WaveAR：小波感知的连续自回归扩散用于精确人体运动预测 |
| 英文题名 | WaveAR: Wavelet-Aware Continuous Autoregressive Diffusion for Accurate Human Motion Prediction |
| 会议/期刊 | NEURIPS 2025 |
| Links | [paper](https://neurips.cc/virtual/2025/loc/san-diego/poster/116377) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | WaveAR |
| Dataset | HumanEva-I, Human3.6M, AMASS |

> [!tip] 效果简介
> - HumanEva-I 上，ADE / FDE 0.199 / 0.201 vs HumanMAC (0.209 / 0.223) (-0.01 / -0.022)。
> - Human3.6M 上，ADE / FDE 0.347 / 0.452 vs CoMusion (0.350 / 0.458) (-0.003 / -0.006)。
> - Human3.6M (推理时间) 上，Inference Time (s) / Params (M) 0.65s / 86.5M vs HumanMAC 1.25s / 28.4M (-0.6s (faster))。

## 概要

### 问题瓶颈

现有随机人体运动预测（SHMP）方法普遍依赖向量量化（VQ）将连续运动压缩为离散 token，再以自回归方式逐 token 生成。这一范式存在两个根本性瓶颈：

1. **量化误差导致运动细节丢失**：VQ-VAE 的离散化过程不可避免地引入信息损失，使得生成的运动缺乏精细关节动态，尤其在手指、脚踝等高频部位表现明显。
2. **频率建模局限于低频**：主流方法采用离散余弦变换（DCT）提取运动频率特征，但 DCT 仅保留低频分量，丢弃了高频信息，限制了预测精度。

这两个瓶颈共同导致现有方法的预测准确度与运动保真度之间存在难以调和的矛盾。

### 核心方法定位

WaveAR 提出了一种**连续空间中的小波感知自回归扩散框架**，从根本上规避上述瓶颈。其核心创新在于三个“替换”：

| 设计维度 | 现有范式 | WaveAR |
|---------|---------|--------|
| 隐空间表征 | VQ-VAE 离散 token | 轻量级时空 VAE 产生的**连续潜 token** |
| 频率建模 | DCT 仅保留低频 | 离散小波变换（DWT）提取 **LL/LH/HL/HH 四个子带** |
| 生成范式 | 离散 token 上的自回归 | 连续空间中的 **Masked Autoregressive Diffusion** |

方法流程为两阶段：第一阶段，时空 VAE（ST-VAE）将原始 3D 关节序列压缩为时间下采样的连续潜 token 流；第二阶段，小波特征提取器对输入序列施加 2D DWT 生成四个频率子带，经线性投影后，通过交替交叉注意力与自注意力层融合到 masked autoregressive diffusion 中，由小型 MLP 扩散头预测逐 token 噪声残差，最终由 ST-VAE 解码器恢复未来运动轨迹。

### 方法谱系与知识库定位

WaveAR 处于**随机人体运动预测**的连续生成建模分支，其直接参照系包括：

- **离散自回归方法**：HumanMAC、CoMusion 等将运动预测建模为离散 token 的自回归生成，WaveAR 继承了其自回归分解的思路，但将操作空间从离散转为连续。
- **扩散方法**：MotionDiff、BeLFusion 等将扩散模型引入运动生成，WaveAR 借鉴了扩散损失与去噪采样的机制，但将其嵌入自回归框架而非独立使用。
- **频率引导方法**：基于 DCT 的频率编码在 SHMP 中广泛使用，WaveAR 用 DWT 替代 DCT，在保留低频的同时显式建模高频子带。

从更宏观的视角看，WaveAR 将**连续潜变量学习**、**多尺度频率分解**与**自回归扩散**三者统一，为高保真序列生成提供了一种新的组合范式。

### 核心结论

WaveAR 在两个标准基准上均取得最优性能：

- **Human3.6M**：ADE 0.347，FDE 0.452，优于 CoMusion（0.350 / 0.458）
- **HumanEva-I**：ADE 0.199，FDE 0.201，优于 HumanMAC（0.209 / 0.223）

消融实验系统验证了各组件的必要性：移除 ST-VAE 导致 ADE 从 0.347 升至 0.492；移除 DWT 分支使 ADE 升至 0.381；用 DCT 替代 DWT 使 ADE 升至 0.362；用 L2 损失替代扩散损失使 ADE 升至 0.422。所有证据一致表明，连续潜变量编码与小波多频率引导的协同作用是性能提升的关键。

在推理效率方面，WaveAR 基础模型推理时间仅 0.65s，比 HumanMAC（1.25s）快约 48%，同时参数量为 86.5M，实现了精度与速度的双重优势。

**局限性与开放问题**：连续自回归范式在生成多样性（APD 指标）上相对较低；模型仅基于 3D 关节坐标，难以捕捉手指或面部等精细动作；跨数据集泛化性尚未验证。如何在高准确度下提升多样性、扩展至更细粒度运动捕捉，是该方向值得探索的问题。



### 问题定义

人体运动预测（Stochastic Human Motion Prediction, SHMP）旨在根据观测到的历史姿态序列，生成未来可能的多条合理运动轨迹。给定 $P$ 帧历史 3D 关节坐标 $\mathbf{X} \in \mathbb{R}^{P \times J \times 3}$（$J$ 为关节数），模型需预测 $F$ 帧未来姿态 $\mathbf{Y} \in \mathbb{R}^{F \times J \times 3}$。由于人体运动的固有随机性——同一历史动作可对应多种合理未来——该任务本质上是一个一对多的条件生成问题。

### 现有方法的两大瓶颈

当前主流 SHMP 方法普遍面临两个相互关联的技术瓶颈：

**瓶颈一：向量量化（VQ）导致细节丢失与训练不稳定。** 多数现有方法沿用“先压缩后生成”的两阶段范式：首先通过 VQ-VAE 将连续运动序列离散化为有限码本中的 token，再在离散空间中进行自回归生成。然而，向量量化过程不可避免地引入信息损失，导致手指微动、关节震颤等精细运动细节被抹除；同时，码本坍塌（codebook collapse）等问题使得训练过程不稳定，限制了生成质量的上限。

**瓶颈二：基于 DCT 的频率表示忽略高频信息。** 为引入时序结构先验，部分方法采用离散余弦变换（DCT）将运动序列投影到频域。但 DCT 仅保留低频分量，丢弃了表征快速运动切换、瞬时加速等动态的高频子带。这种“低通滤波”式的频率建模从根本上制约了模型对复杂运动模式的捕捉能力，尤其在需要精确时序对齐的长时程预测场景中，误差累积问题更为突出。

### 核心动机：连续自回归与小波多频率引导

针对上述瓶颈，WaveAR 提出两条核心改进思路：

1. **从离散到连续的范式迁移**：以轻量级时空 VAE（ST-VAE）替代 VQ-VAE，直接在连续潜空间中保留运动信息的完整分布，从根本上消除量化误差。在连续潜 token 流上执行 masked autoregressive diffusion，既继承了自回归模型的逐帧因果归纳偏置，又通过扩散损失增强了生成质量。

2. **从 DCT 到 DWT 的频率建模升级**：引入离散小波变换（DWT）替代 DCT，将运动序列分解为四个子带——低频近似分量（LL）与三个高频细节分量（LH, HL, HH）。通过交叉注意力机制将这些多尺度频率信息注入生成过程，使模型同时感知运动的全局趋势与局部细节，从而在保持预测准确性的同时恢复高频运动特征。

这两种设计的协同效应在于：连续潜空间保留了 DWT 提取的完整频谱信息，而小波引导的交叉注意力则为扩散去噪过程提供了结构化的频率先验，使得逐 token 自回归生成既能保持时序一致性，又能捕捉精细的运动动态。



## 核心方法与创新机理

WaveAR 的核心创新在于用**连续潜变量**替代现有 SHMP 方法中普遍采用的向量量化（VQ）离散 token，并通过**离散小波变换（DWT）** 提取多尺度高频子带，将其融合到 masked autoregressive diffusion 框架中，从而同时解决“量化误差导致运动细节丢失”和“频率表示忽略高频信息”两个瓶颈问题。

### 创新点一：连续潜空间替代向量量化

现有方法（如 HumanMAC、CoMusion 等）依赖 VQ-VAE 将运动序列压缩为离散 token，再在离散空间中进行自回归生成。这一范式存在两个固有问题：（1）量化操作不可避免地丢弃精细运动细节；（2）训练不稳定，码本坍塌风险高。

WaveAR 提出**轻量级时空 VAE（ST-VAE）**，将原始 3D 关节序列压缩为时间下采样的**连续潜 token 流**，完全避免量化步骤。ST-VAE 编码器由 1D 卷积、若干 ResNet1D 块和步长卷积组成，通过重参数化技巧采样潜变量：

$$\mathbf{z} = \mu(\mathbf{X}) + \sigma(\mathbf{X}) \odot \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

训练损失结合 L1 重建误差与 KL 正则项：

$$\mathcal{L}_{\mathrm{VAE}} = \| \hat{\mathbf{X}} - \mathbf{X} \|_1 + \beta \operatorname{KL} \big( \mathbf{q}(\mathbf{Z} \mid \mathbf{X}) \| \mathcal{N}(0, I) \big)$$

消融实验直接验证了这一设计的必要性：**移除 ST-VAE 后，ADE 从 0.347 骤升至 0.492，FDE 从 0.452 升至 0.641**（Table 3），证明连续潜变量编码是方法有效性的基础。

### 创新点二：小波多频率引导替代 DCT 低频表示

现有频率域方法（如基于 DCT 的工作）仅保留低频分量，丢弃高频信息，导致预测运动缺乏细节和锐度。WaveAR 改用**离散小波变换（DWT）**，对输入序列应用 2D Haar 小波，生成四个子带（LL、LH、HL、HH），同时保留低频全局结构和三个方向的高频细节：

$$Y_{a,b}[k_1,k_2] = \sum_{i=1}^{H+F} \sum_{j=1}^{3J} f_a(i-2k_1) f_b(j-2k_2) x[i,j]$$

四个子带经拼接和线性投影后，得到与潜 token 同维度的小波特征：

$$F_{\mathrm{wave}}[b] = \mathrm{LN}(W Y + b) \in \mathbb{R}^{K \times D}$$

消融实验中，**用 DCT 替代 DWT 导致 ADE 从 0.347 升至 0.362，FDE 从 0.451 升至 0.478**（Table 5），直接证明 DWT 的多尺度高频信息优于 DCT 的纯低频表示。完全移除频率分支则使 ADE 升至 0.381，FDE 升至 0.503（Table 3），进一步确认频率引导的关键作用。

### 创新点三：小波引导的 Masked Autoregressive Diffusion

WaveAR 将上述两个创新整合到一个统一的生成范式中。在连续潜空间中，采用**masked 自回归扩散**进行逐 token 预测：每个未来 token 被初始化为掩码状态，条件于历史 token 和小波频率特征，通过扩散去噪过程逐步恢复。

核心组件是**小波引导的掩码融合模块**（Wavelet-guided Masked Fusion Module），其 Transformer 栈分为两个阶段：（1）局部融合层使用交叉注意力将潜查询与小波频率键值融合；（2）全局自注意力层建模 token 间长程依赖：

$$X' = \mathrm{CrossAttn}(Q, K, V) = \mathrm{softmax}\left(\frac{(Q W_Q) \cdot (K W_K)^T}{\sqrt{d_k}}\right)(V W_V)$$

扩散头为一个小型 MLP，预测每个噪声 token 的噪声残差，训练目标为标准扩散损失：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{i,t,\epsilon} \left[ \| \epsilon - \epsilon_{\theta}(x_i^{(t)} | t, z_i) \|_2^2 \right]$$

消融实验中，**将扩散损失替换为 L2 损失导致 ADE 升至 0.422，FDE 升至 0.548**（Table 4），证明扩散建模对预测精度的贡献显著。

### 创新总结：Changed Slots 对照

| 设计维度 | 基线方法 | WaveAR 创新 |
|---------|---------|------------|
| 隐空间表征 | VQ-VAE 离散 token | ST-VAE 连续潜 token（无量化） |
| 频率建模 | DCT 仅保留低频 | DWT 提取 LL/LH/HL/HH 四子带 |
| 生成范式 | 离散 token 自回归 | 连续空间 masked 自回归扩散 |

三个 changed slots 形成因果链路：连续潜空间保留细节 → DWT 提供多尺度频率引导 → 扩散损失稳定训练与精细去噪。这一设计使 WaveAR 在 Human3.6M（ADE 0.347, FDE 0.452）和 HumanEva-I（ADE 0.199, FDE 0.201）上均取得最优结果，同时推理速度（0.65s）快于代表性基线 HumanMAC（1.25s），实现了精度与效率的双重提升。



WaveAR 提出了一种完全在连续空间中运行的自回归人体运动预测框架，其核心设计动机在于解决现有方法因向量量化（VQ）导致的运动细节丢失与训练不稳定问题，同时克服基于离散余弦变换（DCT）的频率表示忽略高频信息的局限。整个 pipeline 分为两个阶段，形成“编码—频率引导—自回归扩散生成—解码”的端到端流程。

**第一阶段：连续潜空间编码。** 给定一段包含 $H$ 帧历史观测和 $F$ 帧未来目标的原始 3D 关节序列 $\mathbf{X} \in \mathbb{R}^{(H+F) \times J \times 3}$，一个轻量级的时空 VAE（ST-VAE）将其压缩为时间下采样的连续潜 token 流。ST-VAE 编码器由 1D 卷积、若干 ResNet1D 块和步长卷积堆叠而成，通过重参数化技巧从编码器输出的均值与方差中采样得到潜变量：

$$\mathbf{z} = \mu(\mathbf{X}) + \sigma(\mathbf{X}) \odot \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

训练 ST-VAE 的损失函数结合了 L1 重建误差与 KL 正则项：

$$\mathcal{L}_{\mathrm{VAE}} = \| \hat{\mathbf{X}} - \mathbf{X} \|_1 + \beta \operatorname{KL} \big( \mathbf{q}(\mathbf{Z} \mid \mathbf{X}) \| \mathcal{N}(0, I) \big)$$

这一阶段完全避免了 VQ-VAE 的离散化操作，保留了运动的细粒度信息。

**第二阶段：小波引导的掩码自回归扩散生成。** 该阶段包含三个紧密协作的模块：

1. **小波特征提取器**：对原始 3D 关节历史序列应用 2D 离散小波变换（DWT），使用低通和高通滤波器生成四个频率子带（LL, LH, HL, HH），随后通过线性投影将拼接的子带映射到与潜 token 相同的维度空间。相比 DCT 仅保留低频成分的做法，DWT 同时捕获了高低频细节。

2. **小波引导的掩码融合模块**：这是框架的核心交互单元。Transformer 堆栈被划分为两个阶段——前 $N_{\text{local}}$ 层为局部融合层，每层先执行交叉注意力（以掩码潜 token 为查询、小波频率特征为键值），再执行自注意力；后续层则为纯自注意力层，进行全局时序建模。这种设计使得时间域的运动 token 能够自适应地吸收频率域的多尺度谱信息。

3. **掩码自回归扩散器**：在连续潜空间中，未来 token 被初始化为掩码状态。训练时，真实未来 token 按 DDPM 调度逐步加噪，扩散头（一个小型 MLP）以融合模块输出的条件特征 $z_i$ 和扩散时间步 $t$ 为条件，预测所加的噪声残差，损失函数为：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{i,t,\epsilon} \left[ \| \epsilon - \epsilon_{\theta}(x_i^{(t)} | t, z_i) \|_2^2 \right]$$

推理时，未来 token 以自回归方式逐批解掩码：每一步根据余弦调度确定解掩码比例，已解掩码的 token 经过 $K$ 轮 DDPM 去噪迭代更新，未解掩码的 token 保持噪声状态，直至全部未来帧生成完毕。

**第三阶段：解码。** 去噪后的连续潜 token 流通过 ST-VAE 解码器恢复为 3D 关节轨迹，得到最终预测的运动序列。

整个框架的输入输出流可概括为：**原始 3D 关节序列 → ST-VAE 编码器 → 连续潜 token + DWT 频率子带 → 小波引导融合模块 → 掩码自回归扩散生成 → ST-VAE 解码器 → 未来 3D 运动预测**。图 1 展示了这一完整架构，图 4 则给出了小波引导融合模块的详细结构。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/001_Figure_1.jpg]]
*Figure 1: Overall architecture of our proposed WaveAR. (a) During training, a lightweight Spatio-Temporal VAE encodes the raw 3D-joint sequence (past H + future F frames) into a compact latent token stream via temporal downsampling. (b) shows the process of the wavelet-guided autoregressive masked generation model. First, the VAE latents are randomly masked, while the original input sequence’s history undergoes a 2D discrete wavelet transform for wavelet frequency-domain feature extraction, and linear projection into the same embedding space. Next, the masked latents and projected wavelet features are fused through a fusion module consisting of alternating cross-attention and self-attention layers. F...*



WaveAR 的核心由四个紧密耦合的模块构成：**ST-VAE 编码器**、**小波特征提取器**、**小波引导的掩码融合模块**和**掩码自回归扩散器**。以下逐一展开其设计逻辑与关键公式。

### 1. 时空 VAE（ST-VAE）编码器

现有方法依赖向量量化（VQ-VAE）将运动序列离散化为 token，但量化操作不可避免地丢失精细运动细节，并带来训练不稳定。WaveAR 用轻量级时空 VAE 替代，直接在**连续潜空间**中生成 token，从根源上消除量化误差。

- **编码**：输入为 $P$ 帧历史姿态与 $F$ 帧未来姿态拼接的完整序列 $\mathbf{X} \in \mathbb{R}^{(P+F) \times J \times 3}$。编码器由 1D 卷积、若干 ResNet1D 块和步长卷积组成，以因子 $r$ 进行时间下采样，输出均值 $\mu(\mathbf{X})$ 和对数方差 $\sigma(\mathbf{X})$。
- **重参数化采样**：从编码器输出中采样连续潜 token：
  $$\mathbf{z} = \mu(\mathbf{X}) + \sigma(\mathbf{X}) \odot \epsilon, \quad \epsilon \sim \mathcal{N}(0, I) \tag{1}$$
- **训练损失**：ST-VAE 以 L1 重建误差和 KL 正则项联合优化：
  $$\mathcal{L}_{\mathrm{VAE}} = \| \hat{\mathbf{X}} - \mathbf{X} \|_1 + \beta \operatorname{KL} \big( \mathbf{q}(\mathbf{Z} \mid \mathbf{X}) \| \mathcal{N}(0, I) \big) \tag{2}$$

消融实验证实，移除 ST-VAE 直接在原始空间建模会导致 ADE 从 0.347 恶化至 0.492、FDE 从 0.452 恶化至 0.641（Table 3），验证了连续潜变量编码的必要性。

### 2. 小波特征提取器

现有方法采用离散余弦变换（DCT）仅保留低频分量，高频信息被丢弃。WaveAR 改用**二维离散小波变换（2D DWT）**，将原始运动序列分解为四个频率子带：LL（低频近似）、LH（水平高频）、HL（垂直高频）、HH（对角线高频）。

给定输入序列 $x[i,j]$，使用低通滤波器 $f_a$ 和高通滤波器 $f_b$ 计算各子带：
$$Y_{a,b}[k_1,k_2] = \sum_{i=1}^{P+F} \sum_{j=1}^{3J} f_a(i-2k_1) f_b(j-2k_2) x[i,j] \tag{3}$$

四个子带沿空间维度拼接后，通过线性投影映射到与潜 token 相同的维度 $D$：
$$F_{\mathrm{wave}}[b] = \mathrm{LN}(W Y + b) \in \mathbb{R}^{K \times D} \tag{4}$$

消融表明，用 DCT 替代 DWT 会使 ADE 从 0.347 升至 0.362、FDE 从 0.451 升至 0.478（Table 5），验证了 DWT 多尺度高频信息的增益。

### 3. 小波引导的掩码融合模块

该模块是连接频率域信息与时域运动 token 的关键桥梁，采用**两阶段 Transformer 架构**：

- **局部融合层**（前 $N_{\mathrm{local}}$ 层）：每层先执行**交叉注意力**，以潜 token 为 Query、小波特征为 Key 和 Value，将频率线索注入时域表示：
  $$X' = \mathrm{CrossAttn}(Q, K, V) = \mathrm{softmax}\left(\frac{(Q W_Q) \cdot (K W_K)^T}{\sqrt{d_k}}\right)(V W_V) \tag{5}$$
  随后对融合特征施加**自注意力**，让 token 在获得频率信息后进行全局交互。

- **全局自注意力层**（剩余层）：仅包含标准自注意力，进一步建模长程时序依赖。

消融显示，在 12 层总架构中配置 6 个局部融合层取得最优性能（Table 7），说明频率与时域的充分交互至关重要。

### 4. 掩码自回归扩散器

与传统离散 token 自回归不同，WaveAR 在连续潜空间中进行**掩码自回归扩散**，逐 token 预测未来帧。

- **自回归分解**：将未来潜 token 的条件概率建模为：
  $$p(x_1, \ldots, x_N) = \prod_{i=1}^N p(x_i \mid x_{1:i-1}) \tag{7}$$

- **扩散前向加噪**：对每个真实 token $x_i$ 按 DDPM 调度加噪：
  $$x_i^{(t)} = \sqrt{\bar{\alpha}_t} x_i + (1 - \bar{\alpha}_t) \epsilon, \quad \epsilon \sim \mathcal{N}(0, I), \quad t = 1, \dots, T \tag{8}$$

- **扩散损失**：训练一个小型 MLP 噪声预测器 $\epsilon_\theta$，以加噪 token、时间步 $t$ 和融合模块输出的条件特征 $z_i$ 为输入：
  $$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{i,t,\epsilon} \left[ \| \epsilon - \epsilon_{\theta}(x_i^{(t)} | t, z_i) \|_2^2 \right] \tag{9}$$

- **推理去噪**：在自回归生成每一步，对未掩码 token 执行 $K$ 步 DDPM 去噪更新：
  $$u_i^{(k)} = \frac{1}{\sqrt{\alpha_t}} \Big( u_i^{(k-1)} - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_{\theta}(u_i^{(k-1)} | t, z_i) \Big) + \sigma_t \epsilon, \quad \epsilon \sim \mathcal{N}(0, I) \tag{10}$$

消融证实，将扩散损失替换为 L2 损失会导致 ADE 升至 0.422、FDE 升至 0.548（Table 4），说明扩散建模对高保真预测不可或缺。

### 5. 解码与最终预测

去噪后的潜 token 通过 ST-VAE 解码器上采样并重建为 3D 关节轨迹 $\hat{\mathbf{Y}}$，完成从连续潜空间到运动序列的端到端映射。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/009_Figure_4.jpg]]
*Figure 4: The detailed architecture of the Wavelet guided masked fusion module*



## 实验与关键发现

### 主要结果

WaveAR 在标准人体运动预测基准上取得了最优性能。Table 1 汇总了与 11 个基线方法的定量比较：

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/002_Table_1.jpg]]
*Table 1: Quantitative comparison on HumanEva-I and Human3.6M*

**Human3.6M 数据集**：WaveAR 取得 ADE 0.347、FDE 0.452，优于此前最优的 CoMusion（ADE 0.350, FDE 0.458）。在 APD 多样性指标上，WaveAR 为 6.088，处于中等水平——这一结果与其设计取向一致：连续自回归范式天然倾向于高保真预测，但可能牺牲部分样本多样性。

**HumanEva-I 数据集**：WaveAR 取得 ADE 0.199、FDE 0.201，显著优于 HumanMAC（ADE 0.209, FDE 0.223），在所有对比方法中排名第一。

**推理效率**：Table 2 显示 WaveAR（base）推理时间为 0.65s，参数量 86.5M，比 HumanMAC（1.25s, 28.4M）快约 48%，同时精度更高。这表明连续潜空间设计避免了离散 token 的逐 token 采样开销，以可接受的参数量增加换取了显著的推理加速。

**AMASS 数据集**：Table 9 中 WaveAR 取得 ADE 0.485、FDE 0.538，同样优于 HumanMAC 等基线，验证了方法在更大规模、更多样化运动数据上的泛化能力。

### 消融实验

Table 3–5 系统验证了各核心组件的贡献：

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/006_Table_3.jpg]]
*Table 3: Ablation studies on proposed components, conducted on the Human3.6M dataset. Here, “w/o ST-VAE” indicates applying the downstream model directly on the raw input space; “w/ ST-VAE (γ = 1)” denotes an ST-VAE with a single downsampling (our implementation uses two downsamplings); “w/o DWT” removes the DWT branch*

**ST-VAE 连续编码的必要性**：移除 ST-VAE、直接在原始关节空间进行扩散预测（Table 3, “w/o ST-VAE”），性能急剧下降至 ADE 0.492、FDE 0.641。这证明连续潜变量编码不仅压缩了时空冗余，更为后续扩散过程提供了更平滑的优化景观。进一步地，将下采样率从 2 降为 1（即不做时间压缩）也会导致性能退化，表明适度的时序抽象有利于建模长程依赖。

**小波频率引导的有效性**：完全移除 DWT 分支（Table 3, “w/o DWT”）使 ADE 升至 0.381、FDE 升至 0.503。Table 5 进一步对比了三种频率设计：无频率模块（ADE 0.381）、DCT 替代（ADE 0.362）、DWT（ADE 0.347）。DCT 仅保留低频成分，丢失了高频运动细节（如急停、转向的瞬时加速度变化）；DWT 通过四个子带（LL, LH, HL, HH）同时保留高低频信息，使模型能够显式感知不同时间尺度的运动模式。

**扩散损失的必要性**：Table 4 对比了三种训练目标——VQ-VAE 损失、L2 回归损失、扩散损失。L2 损失（ADE 0.422, FDE 0.548）远差于扩散损失，说明确定性回归难以捕捉未来运动的随机多模态分布；扩散损失通过噪声预测范式，使模型学会在连续空间中逐步细化预测，从而更准确地拟合真实运动分布。

**架构配置**：Table 7 显示在总 12 层 Transformer 中，使用 6 个局部融合层（交叉注意力+自注意力）取得最优性能，过多或过少的融合层均会降低精度。Table 8 表明扩散步骤数在 10 步时达到精度-效率的最佳平衡。

### 定性分析

Figure 2 展示了 WaveAR 与 HumanMAC 在多个动作类别上的预测可视化。WaveAR 的十条预测轨迹更紧凑地分布在 ground truth 周围，尤其在“行走”“坐下”等包含精细关节协调的动作上，HumanMAC 的预测出现了明显的末端抖动，而 WaveAR 保持了平滑的关节轨迹。这归因于 DWT 高频子带提供的局部细节引导。

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/003_Figure_2.jpg]]
*Figure 2: Qualitative comparisons: The first line is input history and ground truth motion, both methods predict ten predictions based on the same input history*

Figure 3 展示了运动中间帧生成（motion in-betweening）能力：给定起始动作和结束动作，WaveAR 能生成物理合理、风格一致的平滑过渡序列，进一步验证了模型对运动动力学的理解。

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/005_Figure_3.jpg]]
*Figure 3: Motion in-betweening results of our proposed WaveAR model on the Human3.6M dataset. The first two columns represent the given initial motion, and the last two columns represent the target motion to be transitioned to. The visualization demonstrates that our model smoothly transitions from one motion to another. Both the initial and target motions consist of 20 frames*

### 失败模式与局限

尽管 WaveAR 在精度指标上表现优异，但分析揭示了以下局限：

1. **多样性不足**：APD 指标在多个设置下低于部分基线（如 DLow、DivSamp），这是连续自回归范式固有的 trade-off——模型倾向于生成“最可能”的运动，而非探索分布尾部。实际应用中可能需要额外的多样性促进机制。

2. **高频动作退化**：Table 6 的分类结果显示，在“跳舞”“运动”等高频动态类别上，WaveAR 的优势缩小。DWT 虽能捕获高频信息，但 Haar 小波的频率分辨率有限，可能不足以表征极端快速的关节运动。

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/010_Table_6.jpg]]
*Table 6: Comparison of different methods on various classes and metrics*

3. **数据依赖**：模型仅基于 3D 关节坐标训练，无法捕捉手指运动、面部表情等细粒度动作；训练数据受试者数量有限（Human3.6M 仅 7 名专业演员），可能限制对非典型运动风格的泛化。

4. **缺少跨域验证**：未进行跨数据集或少样本泛化实验，模型在分布外场景下的鲁棒性尚待验证。

> **需人工核实**：论文未提供 APD 指标的完整数值对比表（Table 1 中部分方法的 APD 值缺失），建议查阅原文确认多样性指标的具体排名。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/004_Table_2.jpg]]
*Table 2: Comparison of inference time of different model sizes*

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/007_Table_4.jpg]]
*Table 4: Performance comparison of different loss functions*

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/008_Table_5.jpg]]
*Table 5: Ablation study on different frequency-domain designs*

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/011_Table_7.jpg]]
*Table 7: Performance comparison with different configurations of local fusion layers and total layers*

![[assets/figures/papers/paper_list_l3_https_neurips_cc_virtual_2025_loc_san_diego_poster_116377/figures/012_Table_8.jpg]]
*Table 8: Experiment results of the ablation study on diffusion steps*



## 定位与知识库关联

### 瓶颈与核心洞察

现有随机人体运动预测（SHMP）方法长期受困于两大瓶颈：**向量量化（VQ）导致的细节丢失**与**频率建模的局限性**。以 HumanMAC、CoMusion、MotionDiff 等为代表的基线方法普遍采用 VQ-VAE 将连续运动序列离散化为有限码本 token，再在离散空间中进行自回归生成。这一范式虽简化了建模，却不可避免地引入量化误差，导致手指抖动、脚步滑动等精细运动细节的丢失，同时码本坍塌问题使训练不稳定。在频率维度上，基于离散余弦变换（DCT）的表示仅保留低频分量，系统性忽略高频子带中承载的瞬时姿态变化信息，从根本上限制了预测精度。

WaveAR 的核心洞察在于：**连续潜变量与多尺度小波频率引导的结合，可同时规避量化误差并捕获运动序列的全频带动态**。具体而言，该方法用轻量级时空 VAE 替换 VQ-VAE，产生完全连续的潜 token 流；用离散小波变换（DWT）替代 DCT，将输入序列分解为 LL、LH、HL、HH 四个子带，显式保留高频细节；在生成范式中，采用连续空间中的 Masked Autoregressive Diffusion，通过交叉注意力将小波频率特征逐层注入自回归去噪过程。这一设计在 Human3.6M 上取得 ADE 0.347、FDE 0.452，在 HumanEva-I 上取得 ADE 0.199、FDE 0.201，均超越所有对比方法。

### 与基线方法的关系定位

**离散潜空间方法的对比。** HumanMAC（未提供具体引用，需手动核实会议/年份）是离散自回归范式的代表，其 APD 指标较高（Human3.6M 上 6.769 vs. WaveAR 的 5.884），表明生成多样性更好，但 ADE/FDE 均劣于 WaveAR。这一对比揭示了连续与离散范式之间准确度-多样性的经典权衡：VQ-VAE 的码本离散化天然引入了随机性，有利于多样性，但牺牲了细节保真度。CoMusion、MotionDiff 等扩散方法同样受限于离散潜空间或频率建模不足，ADE/FDE 均被 WaveAR 超越。

**频率建模范式的对比。** 消融实验（Table 5）直接对比了三种频率设计：无频率模块（ADE 0.381, FDE 0.503）、DCT 引导（ADE 0.362, FDE 0.478）、DWT 引导（WaveAR，ADE 0.347, FDE 0.451）。DCT 仅保留低频，其性能显著弱于 DWT，证明高频子带（LH、HL、HH）对恢复瞬时运动细节至关重要。这一结果将 WaveAR 定位为频率感知 SHMP 的新基准。

**推理效率的定位。** Table 2 显示，WaveAR（base）推理时间 0.65s，参数量 86.5M，相比 HumanMAC（1.25s, 28.4M）速度提升近一倍，但参数量更大。这表明连续扩散范式的计算开销主要来自参数规模而非迭代步数，在精度优先的场景下具有实用价值。

### 适用边界

WaveAR 的有效性在以下条件下得到验证：
- **数据集**：Human3.6M（室内受控环境，7 名受试者，15 个动作类）、HumanEva-I（3 名受试者，6 个动作类）、AMASS（多源运动捕捉融合数据集）。
- **预测时长**：标准短时预测（400ms-1000ms），未验证极端长时程（>2s）场景。
- **运动表示**：仅基于 3D 关节坐标，不涉及手指、面部等细粒度部位。
- **任务类型**：给定历史序列预测未来序列（标准 SHMP）及运动插值（motion in-betweening），未涉及文本/音频驱动的条件生成。

### 局限与开放问题

**多样性不足。** WaveAR 的 APD 指标（Human3.6M 上 5.884）低于 HumanMAC（6.769）和部分扩散基线，表明连续自回归范式倾向于产生“平均化”的预测，生成运动的多样性受限。如何在保持高准确度的同时提升多样性，是该范式的核心开放问题。

**细粒度运动缺失。** 模型仅建模 3D 关节坐标，无法捕捉手指运动、面部表情等精细动作。将框架扩展到包含手部关键点或参数化身体模型（如 SMPL-X）是自然的延伸方向。

**泛化性未验证。** 训练数据受试者数量有限（Human3.6M 仅 7 人），模型可能对差异显著的运动风格（如舞蹈、体育动作）泛化不足。跨数据集零样本或少样本迁移实验尚未开展。

**长时程与高频动作。** 论文未报告极端长时程预测（>2s）的性能，且高频动作（如快速转身、跳跃）上的预测质量缺乏专项分析。DWT 虽提供高频子带，但扩散模型在长序列上的误差累积效应仍需研究。

**部署效率。** 86.5M 的参数量限制了在移动端或嵌入式设备上的部署。模型量化、知识蒸馏等压缩方案尚未探索。

**范式迁移潜力。** 连续自回归扩散范式是否可推广到更通用的运动生成任务（如文本驱动运动合成、运动风格迁移），以及小波频率引导是否适用于其他时序生成领域（如视频预测、音频合成），是值得关注的开放方向。



## 原文 PDF

![[paperPDFs/NEURIPS_2025/WaveAR_Wavelet-Aware_Continuous_Autoregressive_Diffusion_for_Accurate_Human_Motion_Prediction.pdf]]
