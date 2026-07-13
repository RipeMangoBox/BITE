---
title: A Unified Diffusion Framework for Scene aware Human Motion Estimation from Sparse Signals
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/A_Unified_Diffusion_Framework_for_Scene_aware_Human_Motion_Estimation_from_Sparse_Signals.pdf
project_link: null
code_link: https://github.com/jn-tang/S2Fusion
aliases:
- UDFSAHMEFSS
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入3D场景几何信息作为附加模态，结合周期性运动对齐特征与基于物理的损失引导，能够显著缩小可能运动空间，并约束下半身运动。
primary_logic: 通过预训练运动先验初始化扩散采样、利用周期自动编码器提取稀疏信号的时间对齐特征，并在采样过程中施加场景穿透和相位匹配损失，能够有效生成场景感知且上下半身协调的真实全身运动。
claims:
- 引入场景模态可以极大地减少稀疏到密集的一对多模糊性，显著提高运动估计质量。
- 使用预训练运动先验进行初始化显著提高了运动平滑度和估计精度。
- 周期性自编码器提取的空间-时间对齐特征提升了运动估计质量。
- 相位匹配损失比场景穿透损失在产生准确运动方面更有效。
---

# A Unified Diffusion Framework for Scene aware Human Motion Estimation from Sparse Signals

> [!tip] 核心洞察
> 通过预训练运动先验初始化扩散采样、利用周期自动编码器提取稀疏信号的时间对齐特征，并在采样过程中施加场景穿透和相位匹配损失，能够有效生成场景感知且上下半身协调的真实全身运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于场景感知的统一扩散框架用于稀疏信号的人体运动估计 |
| 英文题名 | A Unified Diffusion Framework for Scene aware Human Motion Estimation from Sparse Signals |
| 会议/期刊 | CVPR 2024 |
| Links | [Code](https://github.com/jn-tang/S2Fusion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | S2Fusion |
| Dataset | CIRCLE, GIMO |

> [!tip] 效果简介
> - CIRCLE 上，MPJPE (mm) 19.2 vs 24.6 (AvatarJLM) (-5.4 (22.0%↓))。
> - GIMO 上，MPJPE (mm) 57.8 vs 70.7 (AvatarJLM) (-12.9 (18.2%↓))；Lower PE (mm) 107.9 vs 132.6 (AvatarJLM) (-24.7 (18.6%↓))。

## 概要

从稀疏的上半身追踪信号（如头、手）估计全身运动，存在固有的一对多映射模糊性：由于完全缺乏下半身观测，生成的运动往往腿部不真实且与上半身动作不协调。S2Fusion 针对该瓶颈，提出一个统一的场景感知条件扩散框架，核心思路是将**3D场景几何信息**作为额外模态，结合**周期性运动对齐特征**与**基于物理的损失引导**，显著缩小可行运动空间并约束下半身。

方法的关键因果调节机制有三点：
1. **非高斯运动先验初始化**：用预训练的VAE运动先验代替标准高斯噪声启动反向扩散过程，加速推理并提高运动平滑度与精度。
2. **多模态条件融合**：将原始稀疏信号、周期性自编码器（PAE）提取的时间对齐特征、场景点云编码特征共同作为去噪网络的条件输入。
3. **损失引导采样**：在采样过程中施加场景穿透损失和相位匹配损失的梯度，迫使下半身运动既避免穿模又与上半身相位一致。

实验表明，S2Fusion在CIRCLE和GIMO两个基准上均显著优于现有方法：在CIRCLE上，MPJPE降至**19.2 mm**（相对AvatarJLM降低22.0%）；在GIMO上，MPJPE降至**57.8 mm**（降低18.2%），下半身位置误差降低18.6%。消融研究验证了场景模态、运动先验和PAE各自对性能的独立贡献，其中场景信息的引入将CIRCLE MPJPE从26.2 mm降至19.2 mm。在引导损失中，相位匹配损失比场景穿透损失更为关键。

方法的主要局限在于精细手-物交互（如捡衣服、擦黑板）仍表现不佳，因其侧重腿部运动约束，尚未纳入全身物理约束。

从稀疏的上半身追踪信号（如头戴式显示器与手柄的6-DoF位姿）中估计全身人体运动，是VR/AR应用中的核心需求。然而，该任务存在一个根本性的**一对多映射模糊性**：仅凭头部和双手的稀疏观测，下半身运动存在无穷多种可能解。现有方法主要分为两类：基于回归的方法（如**AvatarPoser**）直接映射稀疏信号到全身姿态，但往往产生不真实、不平滑的腿部运动；基于概率生成模型的方法（如**AGRoL**采用normalizing flow，**AvatarJLM**（Zheng et al., ICCV 2023）采用关节级建模）试图建模运动分布，但由于缺乏下半身观测，生成的腿部运动仍常与上半身不协调，且易与3D场景几何发生穿透。

一个关键的观察是：**人体上下半身运动存在内在的周期性协调关系**。如Figure 3所示，从AMASS数据集中随机采样的运动序列，其上、下半身的运动特征在频率、相位和幅值上呈现出显著的对齐模式——相位偏移反映了时间对齐关系，而幅值则对应运动动量。这一观察揭示了从上半身信号推断下半身运动的可行路径：若能有效提取并利用这种周期性对齐特征，就能为稀疏到密集的映射提供强有力的先验约束。

此外，**3D场景几何信息**是另一个尚未被充分挖掘的关键模态。在真实交互场景中，人体运动受场景约束——脚不能穿透地面，身体不能穿越墙壁。引入场景几何作为附加条件，可以极大地缩小可能运动空间，约束下半身运动使其与场景相容。

基于以上动机，本文提出**S2Fusion**——一个统一的场景感知稀疏信号融合框架。其核心思路是：将稀疏到密集的运动估计建模为一个**条件扩散模型的生成过程**，并通过三个关键设计解决固有模糊性：
1. **利用预训练运动先验初始化扩散采样**，使生成从符合真实运动分布的非高斯空间开始，而非标准高斯噪声；
2. **引入场景几何特征与周期性对齐特征**作为条件输入，从空间约束和运动协调两个维度缩小解空间；
3. **在采样过程中施加场景穿透损失与相位匹配损失**的梯度引导，进一步正则化下半身运动，确保生成结果既场景相容又上下半身协调。

## 核心方法与创新机理

S2Fusion 的核心创新在于针对“稀疏上半身信号 → 全身运动”这一病态映射，引入了三个相互协同的关键机制，共同构成了一个场景感知的统一扩散框架。

**1. 非高斯扩散初始化：从运动先验中采样**

标准的扩散模型从纯高斯噪声开始反向去噪，这在高维且高度结构化的运动空间中效率低下，且容易产生不自然的姿态。S2Fusion 改变了这一初始化方式：它首先在 AMASS 大规模运动数据集上预训练一个基于 VAE 的运动先验模型，然后在推理时从该先验分布中采样，生成初始噪声运动 $\tilde{\mathbf{x}}^{1:N} = f_{\phi}(z, \mathbf{p}^{1:N})$。这一改变的本质是将扩散过程的起点从“无意义的噪声”拉近到“合理的运动流形”附近，从而显著降低了采样难度，并提升了生成运动的平滑性和真实性（消融实验显示，移除运动先验后 CIRCLE 上的 MPJPE 从 19.2 升至 21.2）。

**2. 多模态条件融合：场景几何与周期性对齐特征**

传统方法仅以稀疏追踪信号 $\mathbf{p}^{1:N}$ 作为输入，信息瓶颈严重。S2Fusion 将条件信号扩展为 $\mathbf{c} = (\mathbf{p}^{1:N}, \mathbf{f}^{1:N}, \mathbf{E}_S)$，引入了两个新的信息源：
- **场景几何特征 $\mathbf{E}_S$**：通过场景编码器从裁剪的点云中提取，为模型提供物理空间约束，使生成的运动能够主动避让障碍物。这是解决“一对多”模糊性的关键因果杠杆——场景信息极大地缩小了可能运动的搜索空间。
- **周期性对齐特征 $\mathbf{f}^{1:N}$**：由周期性自编码器（PAE）从稀疏信号中提取。PAE 通过 1D 卷积和 FFT 计算运动的幅值、频率和相位偏移，并在时域重建出平滑的正弦特征。这一设计的核心洞察在于：上下半身运动存在内在的周期性耦合关系（如行走时手臂与腿部的相位差），PAE 显式地捕捉了这种时空对齐，为下半身生成提供了强先验。

**3. 损失引导的采样过程：物理约束注入**

在扩散采样的每一步，S2Fusion 不仅依赖去噪网络的预测 $\hat{\mathbf{x}}_0^{1:N}$，还通过损失函数的梯度对生成结果进行显式正则化。具体而言，采样损失由两部分组成：
$$\ell_{\mathrm{sample}} = \alpha \cdot \ell_{\mathrm{penetration}} + \beta \cdot \ell_{\mathrm{phase}}$$
- **场景穿透损失 $\ell_{\mathrm{penetration}}$**：惩罚关节与场景点云之间的穿透距离，强制运动满足几何可行性。
- **相位匹配损失 $\ell_{\mathrm{phase}}$**：计算上半身（手腕）与下半身（骨盆、脚踝）运动相位之间的差异，强制上下半身运动保持协调。消融研究表明，相位匹配损失的有效性高于穿透损失（CIRCLE 上单独使用相位损失 MPJPE 为 19.8，穿透损失为 20.1），这验证了周期性耦合假设的正确性。

通过梯度更新 $\bar{\mathbf{x}}_0^{1:N} \gets \hat{\mathbf{x}}_0^{1:N} - \eta \nabla \ell_{\mathrm{sample}}$，这些物理约束被直接注入到采样轨迹中，使得最终生成的运动既符合场景几何，又保持了上下半身的运动一致性。

S2Fusion 是一个统一的条件扩散框架，目标是从极稀疏的上半身追踪信号（仅头部与双手的 6-DoF 位姿）和 3D 场景几何中估计全身运动。其核心设计围绕三个瓶颈展开：**稀疏到密集的一对多映射模糊性**、**下半身观测缺失导致的运动不协调**，以及**人-场景交互的物理合理性**。

### 管线总览

整体管线如 Figure 2 所示，由四个主要模块串联构成：

![[assets/figures/papers/paper_list_l1709_A_Unified_Diffusion_Framework_for_Scene_aware_Human_Motion_Estimation_fr/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of*

1. **运动先验初始化**：从预训练的 VAE 运动先验中采样初始噪声运动 $\tilde{\mathbf{x}}^{1:N}$，替代标准扩散过程中的高斯噪声，使逆扩散过程从非高斯的自然运动分布出发。
2. **多模态条件编码**：将稀疏追踪信号 $\mathbf{p}^{1:N}$、周期性对齐特征 $\mathbf{f}^{1:N}$ 和场景几何特征 $\mathbf{E}_S$ 融合为统一的条件向量 $\mathbf{c} = (\mathbf{p}^{1:N}, \mathbf{f}^{1:N}, \mathbf{E}_S)$。
3. **条件去噪网络**：基于条件 $\mathbf{c}$ 和时间步 $t$，去噪网络 $G$ 预测干净运动 $\hat{\mathbf{x}}_0^{1:N}$，训练目标为简单损失 $\mathcal{L}_{\mathrm{simple}}$ 与几何损失 $\mathcal{L}_{\mathrm{geometric}}$ 的组合。
4. **损失引导采样**：在逆扩散的每一步，利用场景穿透损失 $\ell_{\mathrm{penetration}}$ 和相位匹配损失 $\ell_{\mathrm{phase}}$ 的梯度对预测运动的下半身部分进行正则化更新，生成最终全身运动。

### 模块间因果机制

框架的关键因果链路可概括为：**场景信息缩小解空间 → 周期性特征对齐上下半身 → 运动先验保证平滑性 → 损失引导强制物理约束**。

- **场景模态的模糊性消减**：仅依赖稀疏上半身信号时，下半身运动存在大量可能解。引入场景几何特征 $\mathbf{E}_S$ 后，模型能够利用场景约束（如地面高度、障碍物位置）显著缩小可行运动空间。消融实验（Table 3/4）证实，移除场景输入后 CIRCLE 数据集上的 MPJPE 从 19.2 mm 退化至 26.2 mm，降幅达 26.7%。
- **周期性自编码器 (PAE) 的时空对齐**：PAE 通过 1D 卷积和 FFT 从稀疏信号中提取幅值 $\mathbf{A}$、偏移 $\mathbf{B}$、频率 $\mathbf{F}$ 和相位偏移 $\mathbf{S}$，在时域重建平滑的周期性对齐特征 $\mathbf{f}_t = \mathbf{A} \cdot \sin(2\pi \cdot (\mathbf{F} \cdot t - \mathbf{S})) + \mathbf{B}$。这一设计利用了上下半身运动的天然周期性关联（Figure 3 可视化了这种相关性），为下半身运动提供了隐式的时间对齐先验。
- **运动先验的初始化增益**：预训练 VAE 运动先验在 AMASS 大规模运动数据集上训练，使初始采样即具备合理的运动模式。去除运动先验后，CIRCLE MPJPE 从 19.2 mm 升至 21.2 mm（Table 3），表明先验对运动平滑性和估计精度均有显著贡献。
- **损失引导的物理约束**：采样过程中的混合损失 $\ell_{\mathrm{sample}} = \alpha \cdot \ell_{\mathrm{penetration}} + \beta \cdot \ell_{\mathrm{phase}}$ 通过梯度更新 $\bar{\mathbf{x}}_0^{1:N} \gets \hat{\mathbf{x}}_0^{1:N} - \eta \nabla \ell_{\mathrm{sample}}$ 直接作用于下半身关节。其中相位匹配损失 $\ell_{\mathrm{phase}}$ 强制上下半身运动相位一致，消融实验（Table 5/6）表明其效果优于场景穿透损失，两者联合使用可取得最佳性能。

### 输入输出规范

- **输入**：长度为 $N$ 的稀疏追踪序列 $\mathbf{p}^{1:N}$（头部和双手的 6-DoF 位姿）及对应场景点云 $S$。
- **输出**：全身运动序列 $\mathbf{x}^{1:N}$，包含所有身体关节的 3D 位置，具有场景感知能力和上下半身协调性。

### 与基线方法的差异

相较于现有方法，S2Fusion 在三个关键维度上进行了改进：**AvatarPoser** 等回归方法直接映射稀疏信号到全身姿态，缺乏对一对多模糊性的建模；**AGRoL** 等概率生成模型虽能产生多样输出，但未利用场景信息约束解空间；**AvatarJLM** (Zheng et al., ICCV 2023) 等关节级建模方法在下半身估计上仍有较大误差（GIMO Lower PE 132.6 mm vs. S2Fusion 107.9 mm，Table 2）。S2Fusion 通过融合场景、运动先验和周期对齐特征，并在采样过程中施加物理损失引导，系统性地解决了上述局限。

S2Fusion 的核心设计围绕三个关键改造展开：**非高斯运动先验初始化**、**多模态条件融合**以及**损失引导的扩散采样**。以下逐一拆解各模块的机理与关键公式。

### 3.1 基于 VAE 的运动先验初始化

标准扩散模型从各向同性高斯噪声 $\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 开始反向去噪，但这忽略了人体运动的强结构性先验。在稀疏信号条件下，从无信息噪声出发容易产生不合理的姿态，尤其在下半身缺乏观测时更为严重。

S2Fusion 的解决方案是：**用预训练运动先验生成的样本替代标准高斯噪声作为扩散起点**。具体而言，在 AMASS 大规模运动数据集上预训练一个 VAE 生成模型，其编码器 $\mathcal{E}$ 将运动序列压缩为隐变量 $z$，解码器 $\mathcal{D}$ 则从 $z$ 和条件信号 $\mathbf{p}^{1:N}$ 重建运动。推理时，从该先验中采样初始噪声运动：

$$\tilde{\mathbf{x}}^{1:N} = f_{\phi}(z, \mathbf{p}^{1:N}), \quad z \sim \mathcal{N}(\mathbf{0}, \mathbf{I}) \tag{1}$$

其中 $f_{\phi}$ 为预训练 VAE 的解码器。这一初始化将搜索空间从全空间压缩到“合理运动流形”附近，既加速了推理收敛（约 20 步即可），又缓解了小数据集上的过拟合风险（证据锚点：Table 3/4 中 MP 消融行）。

### 3.2 多模态条件编码

扩散去噪网络 $G$ 的条件输入 $\mathbf{c}$ 融合了三类互补信息：

$$\mathbf{c} = (\mathbf{p}^{1:N}, \mathbf{f}^{1:N}, \mathbf{E}_S) \tag{2}$$

- **$\mathbf{p}^{1:N}$**：原始稀疏追踪信号（头部与双手的 6DoF 位姿序列）。
- **$\mathbf{E}_S$**：场景编码器从裁剪的场景点云中提取的几何特征，提供坐、站、靠等 affordance 约束。
- **$\mathbf{f}^{1:N}$**：周期性自编码器（PAE）从 $\mathbf{p}^{1:N}$ 中提取的空间-时间对齐特征，是该框架的独特设计。

**PAE 的机理**源于一个关键观察：上下半身运动在相位上高度耦合（见 Figure 3）。PAE 首先通过 1D 卷积和 FFT 从追踪信号中提取幅值 $\mathbf{A}$、偏移 $\mathbf{B}$ 和频率 $\mathbf{F}$：

$$[\mathbf{A}, \mathbf{B}, \mathbf{F}] = \mathrm{FFT}(\mathrm{Conv}(\mathbf{p}^{1:N})) \tag{3}$$

同时通过全连接网络计算相位偏移：

$$(s_x, s_y) = \mathrm{FC}(\mathrm{Conv}(\mathbf{p}^{1:N})), \quad \mathbf{S} = \arctan(s_y, s_x) \tag{4}$$

最后在时域重建平滑的周期性对齐特征：

$$\mathbf{f}_t = \mathbf{A} \cdot \sin(2\pi \cdot (\mathbf{F} \cdot t - \mathbf{S})) + \mathbf{B} \tag{5}$$

这些特征显式编码了上半身运动的周期性模式，为下半身预测提供了强时间对齐先验。

### 3.3 条件扩散训练

前向扩散过程按标准 DDPM 定义，逐步向真实运动 $\mathbf{x}_0$ 注入高斯噪声：

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1 - \beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I}) \tag{6}$$

去噪网络 $G$ 接收噪声运动 $\mathbf{x}_t^{1:N}$、时间步 $t$ 和条件 $\mathbf{c}$，直接预测干净运动 $\hat{\mathbf{x}}_0$。训练损失由简单重建损失和几何损失组成：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{t \sim [1, T]} \lVert G(\mathbf{x}_t^{1:N}, t, \mathbf{c}) - \mathbf{x}_0 \rVert \tag{8}$$

$$\mathcal{L}_{\mathrm{geometric}} = \| \mathrm{FK}(\hat{\mathbf{x}}) - \mathrm{FK}(\mathbf{x}_0) \| \tag{11}$$

几何损失通过正向运动学（FK）约束生成的运动位于骨骼流形上，防止出现骨长畸变。反向采样时，利用 $G$ 的预测进行单步去噪：

$$\mathbf{x}_{t-1}^{1:N} = \sqrt{\bar{\alpha}_{t-1}} G(\mathbf{x}_t^{1:N}, t, \mathbf{c}) + \sqrt{1 - \bar{\alpha}_{t-1}} \epsilon \tag{9}$$

### 3.4 损失引导的扩散采样

即使条件信号提供了强先验，初始预测仍可能出现场景穿透或上下半身相位失配。S2Fusion 在采样过程中注入两类物理引导损失的梯度，仅对下半身关节进行正则化更新。

**场景穿透损失**惩罚关节侵入场景点云：

$$\ell_{\mathrm{penetration}}(\mathbf{x}_0) = \sum_{i \in \mathcal{C}} \sum_{b \in \mathrm{KNN}(\mathbf{x}_{0,i}, k)} \max(r - \| \mathbf{x}_{0,i} - b \|, 0) \tag{12}$$

其中 $\mathcal{C}$ 为下半身关节集合，$b$ 为场景点云中关节 $\mathbf{x}_{0,i}$ 的 $k$ 近邻点，$r$ 为碰撞检测半径。

**相位匹配损失**迫使下半身运动与上半身保持相位一致。从骨盆和左右脚踝提取下半身相位特征 $P_{\mathrm{lower}}$，与上半身相位 $P_{\mathrm{upper}}$ 计算偏差：

$$\ell_{\mathrm{phase}}(\mathbf{x}_0) = \| P_{\mathrm{upper}} - P_{\mathrm{lower}} \| \tag{13-14}$$

总采样引导损失为两者的加权组合：

$$\ell_{\mathrm{sample}} = \alpha \cdot \ell_{\mathrm{penetration}} + \beta \cdot \ell_{\mathrm{phase}} \tag{15}$$

在每个去噪步后，对预测的干净运动 $\hat{\mathbf{x}}_0^{1:N}$ 施加梯度更新以正则化下半身：

$$\bar{\mathbf{x}}_0^{1:N} \gets \hat{\mathbf{x}}_0^{1:N} - \eta \nabla_{\hat{\mathbf{x}}_0^{1:N}} \ell_{\mathrm{sample}}(\hat{\mathbf{x}}_0^{1:N}) \tag{16}$$

消融实验（Table 5/6）表明，相位匹配损失对运动质量的提升大于穿透损失：在 CIRCLE 上，仅用相位损失时 MPJPE 为 19.8 mm，仅用穿透损失时为 20.1 mm，两者联合使用达到最优的 19.2 mm。这验证了“上下半身相位协调”是比“避免穿透”更根本的约束——穿透往往是不合理运动的症状，而非根因。

## 实验与关键发现

### 主实验结果

S2Fusion 在两个基准数据集 **GIMO** 和 **CIRCLE** 上均取得了最优的全身运动估计性能。与现有方法相比，S2Fusion 在位置误差和运动平滑性指标上均表现出显著优势。

在全局位置误差（MPJPE）上，S2Fusion 在 CIRCLE 数据集上达到 **19.2 mm**，相比最强基线 **AvatarJLM**（Zheng et al., ICCV 2023）的 24.6 mm 降低了 **22.0%**；在 GIMO 数据集上达到 **57.8 mm**，相比 AvatarJLM 的 70.7 mm 降低了 **18.2%**（见 Table 1）。

![[assets/figures/papers/paper_list_l1709_A_Unified_Diffusion_Framework_for_Scene_aware_Human_Motion_Estimation_fr/figures/004_Table_1.jpg]]
*Table 1: Full-body motion estimation results evaluated on GIMO [77] and CIRCLE [3]*

在运动平滑性方面，S2Fusion 同样大幅领先。以 GIMO 数据集为例，其 MPJVE 为 235.7、Jitter 为 10.1，显著优于 AvatarJLM 的 354.1 和 15.3，表明生成的全身运动在时序上更加连贯和自然。

细分身体部位的误差分析（Table 2）进一步揭示了 S2Fusion 的核心优势。在下半身位置误差（Lower PE）上，S2Fusion 在 GIMO 数据集上达到 **107.9 mm**，相比 AvatarJLM 的 132.6 mm 降低了 **18.6%**。这一结果表明，引入场景信息与相位匹配损失能够有效约束缺乏直接观测的下半身运动，生成与上半身协调且场景合理的腿部姿态。

![[assets/figures/papers/paper_list_l1709_A_Unified_Diffusion_Framework_for_Scene_aware_Human_Motion_Estimation_fr/figures/006_Table_2.jpg]]
*Table 2: More metrics comparison with AvatarPoser [28], AGRoL [17], and AvatarJLM [76] on GIMO [77] and CIRCLE [3]. We show the results of comparing the hand, upper body, and lower body reconstruction quality*

定性结果（Figure 4）显示，基线方法在复杂场景中容易产生穿透物体或不自然的腿部姿态，而 S2Fusion 能够生成贴合场景几何且上下半身协调的全身运动。

![[assets/figures/papers/paper_list_l1709_A_Unified_Diffusion_Framework_for_Scene_aware_Human_Motion_Estimation_fr/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results on the CIRCLE [3] dataset. We show the results of two motion sequences in different scenes and highlight the implausible motions in the red box. It can be shown that our method generates more correlated leg motions and avoids scene penetration as much as possible*

![[assets/figures/papers/paper_list_l1709_A_Unified_Diffusion_Framework_for_Scene_aware_Human_Motion_Estimation_fr/figures/018_Figure_4.jpg]]
*Figure 4: Human perceptual study results on the GIMO dataset*

### 消融研究

为验证各模块的独立贡献，作者在 CIRCLE 和 GIMO 数据集上进行了系统的部件消融实验（Table 3 和 Table 4）。完整模型 S2Fusion 在 CIRCLE 上取得 19.2 mm MPJPE，消融结果如下：

- **场景模态（Scene）**：移除场景输入后，MPJPE 从 19.2 上升至 26.2，性能下降约 **36.5%**。这验证了核心洞察：3D 场景几何信息能够极大缩小稀疏信号到全身运动的一对多映射模糊性，是实现场景感知运动估计的关键。
- **预训练运动先验（MP）**：将扩散采样的初始分布从预训练 VAE 先验替换为标准高斯噪声后，MPJPE 上升至 21.2。这表明从大规模运动数据集（AMASS）学习的运动先验能够有效规避有限训练数据的问题，提升运动平滑度和估计精度。
- **周期性自编码器（PAE）**：移除 PAE 提取的时空对齐特征后，MPJPE 上升至 20.8。PAE 通过 FFT 从稀疏追踪信号中提取幅值、频率和相位偏移，并在时域重建平滑的周期性特征，为扩散模型提供了有效的时序先验。

损失函数消融（Table 5 和 Table 6）进一步分析了采样引导损失中各部分的作用。在 CIRCLE 数据集上：

![[assets/figures/papers/paper_list_l1709_A_Unified_Diffusion_Framework_for_Scene_aware_Human_Motion_Estimation_fr/figures/008_Table_5.jpg]]
*Table 5: Ablation on the effect of our designed loss function during loss-guided sampling on CIRCLE*

- 仅使用**场景穿透损失**时，MPJPE 为 20.1 mm。
- 仅使用**相位匹配损失**时，MPJPE 为 19.8 mm。
- 完整损失（穿透 + 相位匹配）达到最优的 19.2 mm。

相位匹配损失的单独效果优于穿透损失，这与其设计动机一致：上下半身运动在行走、转身等日常行为中存在固有的相位协调关系（Figure 3 展示了从 AMASS 中提取的上下半身周期性运动特征），强制这种协调性能有效正则化下半身运动。场景穿透损失则进一步消除了人体与场景几何之间的不合理穿透。

### 局限性分析

S2Fusion 在精细的手-物交互场景中表现不佳。典型失败案例（Figure 9）显示，对于捡衣服、擦黑板等需要精确手部操作的任务，生成的运动缺乏足够的细节和物理合理性。这一局限源于方法设计侧重于利用场景和相位约束改善腿部运动，未纳入全身物理约束（如接触力、摩擦力等）。作者指出，系统整合更全面的物理合理性约束是未来工作方向。

## 定位与知识库关联

### 1. 问题定位与基线方法

S2Fusion 解决的是**从稀疏上半身追踪信号（头部与双手的6DoF位姿）估计全身运动**的跨模态生成问题。该任务的核心瓶颈在于：仅凭上半身稀疏观测推断下半身运动存在固有的一对多映射模糊性，且缺乏下半身观测导致腿部运动不真实、与上半身不协调。现有方法可归纳为三类：

- **回归式方法**：如 **AvatarPoser**，基于Transformer直接回归全身姿态。此类方法输出确定性估计，难以捕捉运动的多模态分布，在稀疏观测下容易产生平均化的模糊姿态。
- **概率生成模型**：如 **AGRoL**，采用归一化流（normalizing flow）建模条件分布。相比回归方法具有更好的多样性，但流模型的表达能力受限于可逆结构设计，且未显式利用场景几何约束。
- **关节级建模方法**：如 **AvatarJLM**（Zheng et al., ICCV 2023），在关节层面进行条件建模。该方法在GIMO和CIRCLE基准上代表了先前最优水平（GIMO MPJPE 70.7mm，CIRCLE MPJPE 24.6mm），但仍存在下半身运动不协调和场景穿透问题。

### 2. S2Fusion 的核心改进维度

S2Fusion 在扩散模型框架下，从三个维度对上述基线进行了系统性改进：

| 改进维度 | 基线做法 | S2Fusion 做法 | 机制与收益 |
|---------|---------|--------------|-----------|
| **扩散初始化** | 标准高斯噪声 | 预训练VAE运动先验采样 | 将初始分布从无信息高斯拉向合理运动流形，加速推理并提升运动平滑性（CIRCLE MPJPE从21.2降至19.2，Table 3） |
| **条件模态** | 仅稀疏追踪信号 | 稀疏信号 + 场景几何特征 + 周期性对齐特征 | 场景信息显著缩小解空间（无场景MPJPE 26.2 vs 完整模型19.2，Table 3）；PAE提取的时间对齐特征进一步降低模糊性 |
| **采样引导** | 无条件采样 | 场景穿透损失 + 相位匹配损失联合引导 | 在采样过程中注入物理约束梯度，显式惩罚穿透并强制上下半身相位协调 |

### 3. 知识库定位与适用边界

**方法类型**：S2Fusion 属于**条件扩散模型 + 物理引导采样**的混合框架。其生成过程可分解为三个阶段：
1. **先验初始化**：VAE运动先验（预训练于AMASS）提供非高斯初始分布
2. **条件去噪**：以场景编码特征 $E_S$、原始信号 $p^{1:N}$、周期对齐特征 $f^{1:N}$ 为条件，通过去噪网络 $G$ 预测干净运动
3. **损失引导精炼**：在采样过程中对下半身关节施加梯度更新 $\bar{\mathbf{x}}_0^{1:N} \gets \hat{\mathbf{x}}_0^{1:N} - \eta \nabla_{\hat{\mathbf{x}}_0^{1:N}} \ell_{\mathrm{sample}}$，其中 $\ell_{\mathrm{sample}} = \alpha \cdot \ell_{\mathrm{penetration}} + \beta \cdot \ell_{\mathrm{phase}}$

**适用场景**：
- 输入为头部+双手6DoF追踪信号的VR/AR全身运动估计
- 需要场景感知（避免穿透）和上下半身协调的运动生成
- 对运动平滑性（MPJVE、Jitter）有较高要求的应用

**不适用/表现受限场景**：
- **精细手-物交互**：如捡衣服、擦黑板等动作。S2Fusion 侧重于腿部运动生成，未纳入全身物理约束，手部交互质量不足（Figure 9 失败案例）
- **仅头部运动输入**：虽在Table 7中验证了场景模态的增益，但整体精度仍显著低于头部+双手输入场景

### 4. 消融发现的关键因果机制

消融实验揭示了各组件的相对重要性排序：

1. **场景信息 > 运动先验 > 周期对齐特征**（Table 3/4）：移除场景导致CIRCLE MPJPE从19.2升至26.2（+36.5%），是影响最大的单因素；移除MP升至21.2（+10.4%）；移除PAE升至20.8（+8.3%）
2. **相位匹配损失 > 场景穿透损失**（Table 5/6）：单独使用相位损失（CIRCLE MPJPE 19.8）优于单独使用穿透损失（20.1），二者联合达到最优（19.2）。这表明上下半身运动协调性约束比场景物理约束对精度贡献更大
3. **下半身改善显著**：在GIMO上，下半身位置误差从AvatarJLM的132.6mm降至107.9mm（-18.6%，Table 2），验证了损失引导对不可观测区域的强约束效果

### 5. 局限与开放问题

**已知局限**（来自Figure 9与论文讨论）：
- 方法在精细手-物交互场景下表现不佳，原因在于损失引导仅作用于下半身关节，未对上半身手部运动施加物理约束
- 场景穿透损失依赖于场景点云的KNN查询，对点云密度和噪声敏感

**开放问题**：
- 如何系统整合更全面的全身物理约束（如接触力、动力学约束），在保持实时性的前提下提升复杂交互场景的生成质量？
- 周期对齐特征的提取依赖于运动具有明显周期性，对于非周期性动作（如突然转向、下蹲）的泛化性如何？
- 损失引导的权重 $\alpha, \beta$ 和步长 $\eta$ 目前为固定超参数，是否可设计自适应调节机制以应对不同场景复杂度？

**注意**：上述局限与开放问题均来自论文自身的讨论和失败案例分析，部分细节（如非周期性动作的泛化性）论文未提供定量实验，需后续工作验证。

## 原文 PDF

![[paperPDFs/CVPR_2024/A_Unified_Diffusion_Framework_for_Scene_aware_Human_Motion_Estimation_from_Sparse_Signals.pdf]]
