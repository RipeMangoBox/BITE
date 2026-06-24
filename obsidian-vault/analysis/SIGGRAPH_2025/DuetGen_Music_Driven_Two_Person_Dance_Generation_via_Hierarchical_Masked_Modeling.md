---
title: "DuetGen: Music Driven Two-Person Dance Generation via Hierarchical Masked Modeling"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked_Modeling.pdf
aliases:
- DuetGen
tags:
- SIGGRAPH_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 统一双人表示（将两人运动作为整体建模）与层次化标记化（将运动分为语义层和细节层，利用两层离散标记分别捕获全局语义和局部细节）使得模型能够以粗-细方式从音乐生成舞蹈，同时简化了人际交互的建模难度。
primary_logic: 通过将双人舞蹈运动视为一个整体并采用层次化离散表示，掩码Transformer能够从音乐逐步生成语义明确的舞蹈标记，既保证了单人运动的逼真度，又维持了双人之间的同步与交互。
claims:
- 移除关系全局定位（A1）使FID从1.31升至5.03，PFID从2.54升至14.97，表明该设计对生成质量至关重要。
- 层次化VQ-VAE将双人相对距离误差（RDE）从7.12 mm降至0.17 mm，且单人重建误差降低30%以上。
- 用户研究中DuetGen在运动质量、音乐对齐与搭档协调三个维度均获最高评分（>4/5），显著优于所有基线。
- 消融实验证实，统一表示、关系定位、层次标记化与解码器音乐条件对最终舞蹈质量均有显著提升。
---

# DuetGen: Music Driven Two-Person Dance Generation via Hierarchical Masked Modeling

> [!tip] 核心洞察
> 通过将双人舞蹈运动视为一个整体并采用层次化离散表示，掩码Transformer能够从音乐逐步生成语义明确的舞蹈标记，既保证了单人运动的逼真度，又维持了双人之间的同步与交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | DuetGen：基于层次掩码建模的音乐驱动双人舞蹈生成 |
| 英文题名 | DuetGen: Music Driven Two-Person Dance Generation via Hierarchical Masked Modeling |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [Code](https://github.com/anindita127/DuetGen) · [arXiv](https://arxiv.org/abs/2207.01685) · [paper](https://doi.org/10.1145/3721238.3730741) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DuetGen |
| Dataset | DD100 |

> [!tip] 效果简介
> - DD100 上，FID↓ 1.31 (显著优于所有基线（具体数值见表2）)；PFID↓ 2.54 (显著优于所有基线)；BAS↑ 0.215 (最佳)。

## 概述

双人舞蹈生成面临一个核心瓶颈：系统必须同时处理两位舞者之间的空间协调、引导-跟随动态与紧密的身体互动，而现有方法或仅关注群舞的节奏同步（忽略人际交互），或只能生成跟随者动作，无法从音乐直接合成两位舞者的协调舞蹈。

DuetGen 提出了一条因果清晰的解决路径。其关键洞察在于，将双人舞蹈运动视为一个统一的整体，并采用层次化离散表示——粗粒度的顶层标记捕获全局语义，细粒度的底层标记保留局部细节——从而让掩码 Transformer 能够以“从粗到细”的方式从音乐逐步生成语义明确的舞蹈标记。这一设计既保证了单人运动的逼真度，又维持了双人之间的同步与交互。

在方法定位上，DuetGen 属于**音乐驱动的双人舞蹈生成**，其技术谱系融合了离散运动标记化、掩码建模与层次化运动表示。相比于 Duolando（Siyao et al., ICLR 2024）等只生成跟随者动作的方法，或 GCD（Le et al., TOG 2023）等基于扩散的群舞方法，DuetGen 首次在统一的离散标记空间中同时建模两位舞者的协调运动，并引入关系全局定位来显式编码人际空间关系。

实验证据支撑了这一设计的有效性。在 DD100 双人舞蹈数据集上，DuetGen 取得了 FID 1.31、配对 FID 2.54 和 BAS 0.215 的最佳结果。消融实验进一步揭示了各模块的因果贡献：移除关系全局定位使 FID 从 1.31 升至 5.03，配对 FID 从 2.54 升至 14.97；层次化 VQ-VAE 将双人相对距离误差从 7.12 mm 降至 0.17 mm，且单人重建误差降低超过 30%。用户研究同样表明，DuetGen 在运动质量、音乐对齐与搭档协调三个维度上均显著优于所有基线（评分 > 4/5）。

当前方法的主要局限在于：未对精细的手指交互建模（受限于 DD100 数据集的指部噪声），训练数据仅约 1.9 小时，且解码阶段未考虑身体形状变化。这些方面指向了未来工作的可能方向，包括结合动捕与在线视频缓解数据稀缺、在低质量数据下有效建模手指交互，以及将层次标记化框架推广到其他多人交互场景。

## 背景与动机

音乐驱动的舞蹈生成是计算机视觉与图形学交叉领域的前沿课题，其目标是从输入音乐中合成自然、富有表现力的人体动作序列。近年来，单人舞蹈生成取得了显著进展，但双人舞蹈生成仍然是一个极具挑战性的开放问题。

双人舞蹈的核心难点在于，它不仅要求每位舞者的动作与音乐节拍和风格高度契合，还要求两位舞者之间保持紧密的空间协调与动态交互。这种交互体现在多个层面：引导者与跟随者之间的角色配合、肢体接触时的相对距离控制、以及整体编舞中同步与呼应的时序一致性。现有方法或仅关注群舞的宏观同步而忽略个体间的精细互动，或只能生成跟随者动作而无法从音乐同时生成两位舞者的协调舞蹈，使得双人舞蹈生成成为一个亟待填补的空白。

从技术路径来看，双人舞蹈生成面临的瓶颈可以归结为两个相互交织的问题：**表征困难**与**生成困难**。表征困难在于，如何有效地编码两位舞者的运动信息，使得模型能够同时捕获单人运动的逼真度和双人交互的协调性。生成困难在于，如何从音乐信号中推断出既符合音乐语义又满足交互约束的双人动作序列。这两个问题互为前提：没有好的表征，生成模型难以学习有意义的映射；没有强大的生成能力，再好的表征也无法转化为高质量的输出。

本文提出的 DuetGen 方法正是围绕这两个核心问题展开。其核心动机可以概括为：**将双人舞蹈视为一个不可分割的整体，而非两个独立个体的简单拼接**。基于这一理念，DuetGen 采用统一双人表示将两位舞者的运动编码为单一序列，并通过层次化标记化将运动分解为语义层和细节层两个粒度的离散标记，最终利用掩码 Transformer 以粗-细方式从音乐逐步生成舞蹈。这一设计既简化了人际交互的建模难度，又保证了单人运动的逼真度。

## 核心创新

DuetGen 的核心创新在于通过**统一双人表示**与**层次化标记化**，将双人舞蹈生成问题转化为从音乐到离散标记的粗-细掩码预测任务，从而同时解决单人运动逼真度与双人空间协调两大难题。

### 1. 统一双人运动表示与关系全局定位

传统方法通常将两位舞者的全局位置独立编码，这迫使模型额外学习复杂的空间耦合关系。DuetGen 提出**关系全局定位**（relational global positioning）：将舞者 A 的全局位置表示为速度，而舞者 B 的全局位置则相对于 A 的坐标进行表达（见 Eq. (1)，Section 3.1）。这一设计将双人运动视为一个**统一整体**，使模型天然地捕获引导-跟随动态与相对空间关系，大幅降低了人际交互的建模难度。

消融实验证实了这一设计的决定性作用：移除关系全局定位（A1）后，生成质量急剧恶化，FID 从 1.31 升至 5.03，PFID 从 2.54 升至 14.97（Table 2）；在 VQ 重建阶段，双人相对距离误差（RDE）从 0.17 mm 飙升至 7.12 mm（Table 1）。

### 2. 层次化 VQ-VAE：语义-细节解耦的离散标记化

与单层 VQ-VAE 或全分辨率残差量化不同，DuetGen 采用**两层离散标记化**：

- **顶层标记**（top-level tokens）：由顶层编码器 $E_T$ 在粗时间分辨率（下采样因子 $\eta_{top}$）下量化得到，捕获高层次的舞蹈语义与双人协调模式；
- **底层标记**（bottom-level tokens）：由底层编码器 $E_B$ 在更细时间分辨率（$\eta_{bot}$，且 $\eta_{top} > \eta_{bot} > 1$）下，结合顶层解码特征后量化得到，负责补充精细的运动细节。

这一层次化设计使单人重建误差降低超过 30%，同时将 RDE 从 7.12 mm 压缩至 0.17 mm（Table 1）。移除层次化标记（A2）后，VQ-VAE 退化为普通单层量化，MPJPE 升至 65.09 mm，重建质量显著下降。

### 3. 两阶段掩码 Transformer：从音乐到标记的粗-细生成

生成架构由两个双向掩码 Transformer 级联组成：

- **第一阶段 Transformer** $\theta_t$：以音乐特征为条件，通过迭代掩码预测生成顶层标记序列，确立舞蹈的全局语义框架；
- **第二阶段 Transformer** $\theta_b$：同时以音乐特征和已生成的顶层标记为条件，生成底层标记序列，填充精细运动细节。

训练中采用 10% 概率丢弃音乐条件的无分类器引导策略。推理时，顶层标记在 $L_{top}$ 轮迭代中逐步填充，底层标记再据此一次性生成。这种粗-细分离策略使得模型能够先确定“跳什么”，再决定“怎么跳”，避免了单阶段模型在语义与细节间的冲突。

### 4. 轻量级轨迹精炼模块

为解决生成运动中常见的滑步伪影，DuetGen 在解码后附加一个轻量卷积回归器，从局部运动特征（根关节朝向与局部姿态）预测根轨迹速度，并替换原始生成的根轨迹。该模块作为后处理步骤，不参与 VQ-VAE 或 Transformer 的训练，但有效提升了足部接触的物理合理性。

### 创新点总结

| 创新维度 | 现有方法不足 | DuetGen 方案 | 关键证据 |
|---------|------------|-------------|---------|
| 双人空间表示 | 独立编码全局位置，需额外学习耦合 | 统一表示 + 关系全局定位 | 移除后 FID↑5.03, PFID↑14.97 |
| 运动离散化 | 单层量化，语义与细节混杂 | 层次化 VQ-VAE，语义-细节解耦 | RDE 从 7.12→0.17 mm，MPJPE↓30%+ |
| 生成策略 | 单阶段生成或扩散模型 | 两阶段掩码 Transformer，粗-细渐进 | 用户研究三项指标均 >4/5 |
| 轨迹质量 | 依赖生成轨迹，存在滑步 | 轻量卷积回归器精炼根轨迹 | 定性结果中滑步减少 |

这些创新并非孤立存在，而是形成了从表示、量化到生成的完整链条：统一表示降低了双人交互的建模难度，层次化标记化为粗-细生成提供了天然接口，掩码 Transformer 则充分利用了离散标记的可预测性。消融实验（A1-A6）系统性地验证了每个设计模块对最终舞蹈质量的显著贡献。

## 整体框架

DuetGen 采用**两阶段训练**与**层次化生成**的流水线，将音乐驱动的双人舞蹈生成解耦为“运动离散化”与“音乐到标记映射”两个核心步骤。

### 训练阶段：从连续运动到离散标记

训练流程（图 2）包含两个串行训练的组件：

1. **层次化双人运动 VQ-VAE**  
   首先将统一表示的双人运动序列 $x_{1:N}$ 压缩为两层离散标记：
   - **顶层标记**（$z_{top}$）：以粗时间分辨率 $\eta_{top}$ 捕获高层运动语义（如舞蹈风格、交互模式）
   - **底层标记**（$z_{bot}$）：以较细时间分辨率 $\eta_{bot}$ 保留局部运动细节（如关节速度、足部轨迹）
   
   解码器 $D$ 同时接收两层标记与音乐特征 $z_m$，通过五项损失函数（重建损失、速度损失、承诺损失、前向运动学损失、相对距离损失）联合优化，确保重建运动既保持单人逼真度，又维持双人间精确的空间关系。

2. **两阶段掩码 Transformer**  
   在 VQ-VAE 训练收敛后，固定码本，训练两个双向 Transformer：
   - **第一阶段 Transformer $\theta_t$**：以音乐特征 $m$ 为条件，通过掩码建模从全掩码序列迭代预测顶层标记 $t_{top}$
   - **第二阶段 Transformer $\theta_b$**：以音乐特征 $m$ 和已生成的顶层标记 $t_{top}$ 为条件，预测底层标记 $t_{bot}$

   两个 Transformer 均采用分类器自由引导策略，在 10% 的训练步中丢弃音乐条件，以增强推理时的可控性。

### 推理阶段：从音乐到双人舞蹈的粗-细生成

推理过程（图 3）遵循“先语义后细节”的层次化策略：

1. **顶层生成**：$\theta_t$ 从全掩码序列出发，在 $L_{top}$ 次迭代中逐步填充顶层标记，每次迭代保留置信度最高的预测并重新掩码其余位置。
2. **底层生成**：$\theta_b$ 以生成的顶层标记和音乐为条件，在 $L_{bot}$ 次迭代中生成底层标记序列。
3. **运动解码**：层次化 VQ-VAE 解码器 $D$ 将两层标记与音乐特征解码为连续运动序列。
4. **轨迹精修**：轻量级卷积回归器从局部运动特征预测根关节速度，替换原始根轨迹以减少滑步伪影。

### 模块关系与数据流

整个流水线的输入输出流可概括为：

```
音乐音频 → 音乐编码器 E_M → 音乐特征 z_m
                                ↓
双人运动 x_{1:N} → 层次化 VQ-VAE → 顶层标记 z_top + 底层标记 z_bot
                                ↓
训练：z_m + z_top → θ_t（掩码预测）；z_m + z_top + z_bot → θ_b（掩码预测）
推理：z_m → θ_t → t_top → θ_b → t_bot → 解码器 D → 运动序列 → 轨迹精修 → 最终舞蹈
```

关键设计在于**统一双人表示**（将舞者 B 的全局位置表示为相对 A 的偏移，A 的全局位置表示为速度）与**层次化标记化**的协同：前者使 VQ-VAE 能够将双人交互内化为单一运动表征，后者则让 Transformer 以粗-细方式逐步生成，既降低了人际协调的建模难度，又保证了单人运动的自然度。消融实验证实，移除关系全局定位（A1）会使 FID 从 1.31 升至 5.03、PFID 从 2.54 升至 14.97；移除层次标记化（A2）则使 VQ 重建的相对距离误差从 0.17 mm 飙升至 7.12 mm（表 1、表 2）。

### 补充图表

![[assets/figures/papers/paper_list_l1803_DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked/figures/002_Figure_2.jpg]]
*Figure 2: DuetGen Training Framework. Left: Our hierarchical two-person motion VQ-VAE encodes a unified two-person motion sequence ?? of length ?? into two-scale discrete token sequences. Top-level tokens at a coarse temporal resolution*

![[assets/figures/papers/paper_list_l1803_DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked/figures/003_Figure_3.jpg]]
*Figure 3: Inference Process. Our first-stage transformer*

![[assets/figures/papers/paper_list_l1803_DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked/figures/001_Figure_1.jpg]]
*Figure 1: DuetGen generates synchronized two-person dance choreography from input music, featuring natural and close interactions between dancers*

## 核心模块与公式推导

DuetGen 的核心架构由三个紧密协作的模块构成：统一双人运动表示、层次化向量量化变分自编码器（Hierarchical VQ-VAE）以及两阶段掩码Transformer生成器。以下逐一推导其关键公式与设计机理。

### 统一双人运动表示

传统方法通常独立处理两位舞者的全局位置，这导致模型难以捕捉人际间的空间协调关系。DuetGen 提出**关系全局定位（Relational Global Positioning）**：将舞者 A 的全局位置表示为速度，而舞者 B 的全局位置表示为相对于 A 的偏移。第 i 帧的统一运动特征向量定义为：

$$
\boldsymbol{x}_i = \left[ t_{\mathcal{A}}^{\delta}, r_{\mathcal{A}}^{g}, j_{\mathcal{A}}^{p}, j_{\mathcal{A}}^{r}, j_{\mathcal{A}}^{v}, c_{\mathcal{A}}^{f}, t_{\mathcal{B}}^{\epsilon}, r_{\mathcal{B}}^{g}, j_{\mathcal{B}}^{p}, j_{\mathcal{B}}^{r}, j_{\mathcal{B}}^{v}, c_{\mathcal{B}}^{f} \right]_i
$$

其中 $t_{\mathcal{A}}^{\delta}$ 为 A 的根节点速度，$t_{\mathcal{B}}^{\epsilon}$ 为 B 相对于 A 的根节点位置偏移；$r^{g}$ 为全局根朝向，$j^{p}$、$j^{r}$、$j^{v}$ 分别为局部关节位置、旋转和速度，$c^{f}$ 为脚部接触标签。该表示将双人运动视为一个整体，迫使模型在统一的坐标框架下学习交互模式。消融实验证实，移除该设计（A3）会导致重建和生成中出现互穿与不同步现象（Figure 6）。

### 层次化双人运动量化

为将连续运动转换为离散标记序列，DuetGen 设计了层次化 VQ-VAE，包含底编码器 $\mathbf{E_B}$ 和顶编码器 $\mathbf{E_T}$，分别以因子 $\eta_{bot}$ 和 $\eta_{top}$（$\eta_{top} > \eta_{bot} > 1$）对输入运动进行时序下采样。顶层标记在粗粒度上捕获高层语义，底层标记在细粒度上保留局部细节。

顶层隐变量由底编码器输出经顶编码器进一步压缩后量化：

$$
z_{top} = \mathbf{Q_T}(\tilde{z}_{top}); \quad \tilde{z}_{top} = \mathbf{E_T}(\mathbf{E_B}(x_{1:N}))
$$

底层隐变量则融合底编码器输出与顶解码器 $\mathbf{D_T}$ 的上采样特征后量化：

$$
\tilde{z}_{bot} = (\mathbf{E_B}(x_{1:N}), \mathbf{D_T}(z_{top})); \quad z_{bot} = \mathbf{Q_B}(\tilde{z}_{bot})
$$

最终重构由解码器 $\mathbf{D}$ 同时接收两层标记和音乐特征完成：

$$
\hat{x}_{1:N} = \mathbf{D}(z_{top}, z_{bot}, z_m)
$$

### 损失函数设计

VQ-VAE 的训练目标由五项损失加权求和构成：

$$
\mathcal{L}_{vq} = \lambda_r \mathcal{L}_r + \lambda_v \mathcal{L}_v + \lambda_{com} \mathcal{L}_{com} + \lambda_{fk} \mathcal{L}_{fk} + \lambda_{rel} \mathcal{L}_{rel}
$$

其中 $\mathcal{L}_r$ 和 $\mathcal{L}_v$ 分别为局部姿态的重建损失和速度损失；$\mathcal{L}_{com}$ 为两层量化的承诺损失：

$$
\mathcal{L}_{com} = \beta_1 \|\tilde{z}_{top} - sg[z_{top}]\|_2 + \beta_2 \|\tilde{z}_{bot} - sg[z_{bot}]\|_2
$$

$\mathcal{L}_{fk}$ 为前向运动学重建损失，直接在全局坐标系下约束双人关节位置：

$$
\mathcal{L}_{fk} = \|p_{\mathcal{A}} - \hat{p}_{\mathcal{A}}\|_2 + \|p_{\mathcal{B}} - \hat{p}_{\mathcal{B}}\|_2
$$

$\mathcal{L}_{rel}$ 为相对距离损失，是保障双人空间协调的关键设计：

$$
\mathcal{L}_{rel} = \frac{1}{J}\sum_{j \in J} \lambda_j \sum_{k \in J} e^{-d(p_{\mathcal{A}_j}, \hat{p}_{\mathcal{B}_k})} \left| d(\hat{p}_{\mathcal{A}_j}, \hat{p}_{\mathcal{B}_k}) - d(\hat{p}_{\mathcal{A}_j}, \hat{p}_{\mathcal{B}_k}) \right|
$$

该损失对舞者 A 的第 $j$ 个关节与舞者 B 的第 $k$ 个关节之间的欧氏距离进行约束，$\lambda_j$ 为关节重要性权重（手脚等关键部位权重更高），指数衰减项 $e^{-d(\cdot)}$ 使损失聚焦于距离较近的交互关节对。实验表明，引入 $\mathcal{L}_{rel}$ 后，双人相对距离误差（RDE）从 7.12 mm 降至 0.17 mm（Table 1）。

### 两阶段掩码生成

生成阶段采用两个双向Transformer，以掩码建模方式从音乐逐步恢复运动标记。第一阶段Transformer $\theta_t$ 预测顶层掩码标记：

$$
\mathcal{L}_{tmask} = \sum_{t_{top_k}^M=[MASK]} -\log \theta_t(t_{top_k} \mid t_{top}^{\bar{M}}, m)
$$

第二阶段Transformer $\theta_b$ 在给定顶层完整序列和音乐条件下预测底层掩码标记：

$$
\mathcal{L}_{bmask} = \sum_{t_{bot_k}^M=[MASK]} -\log \theta_b(t_{bot_k} \mid t_{bot}^{\bar{M}}, m, t_{top})
$$

训练时采用无分类器引导（CFG）策略，以 10% 概率丢弃音乐条件，使推理时可通过引导系数调控音乐对齐强度。推理过程（Figure 3）中，第一阶段以 $L_{top}$ 轮迭代填充顶层标记序列，第二阶段据此生成底层细节标记，最终经轨迹精修模块（Trajectory Refinement Module）预测根节点速度以消除滑步伪影。

## 实验与分析

### 实验设置与评估基准

DuetGen在DD100双人舞蹈数据集上进行训练和评估。该数据集包含约1.9小时的动作捕捉数据，按8:2比例划分为168,176帧训练集和42,496帧测试集。通过滑动窗口增强后，获得4,556个训练样本和1,144个测试样本。音乐特征采用MFCC、MFCC差分和Chroma特征，帧率为30 fps。

评估指标涵盖三个维度：**单人运动质量**使用FID（Fréchet Inception Distance）衡量生成运动与真实运动分布的距离；**双人协调性**通过PFID（Paired FID）评估两位舞者运动的联合分布质量；**音乐对齐度**采用BAS（Beat Alignment Score）衡量舞蹈节拍与音乐节拍的一致性。此外，VQ-VAE重建质量使用MPJPE（Mean Per Joint Position Error）和RDE（Relative Distance Error）评估。

基线方法包括：**Duolando**（Siyao et al., ICLR 2024）——原为跟随者舞蹈生成方法，通过额外训练领舞者Transformer适配双人场景；**GCD**（Le et al., TOG 2023）——基于对比扩散的群舞编排方法，在DD100上重训练；**InterGen**（Liang et al., IJCV 2024）——基于扩散的文本驱动双人运动生成，替换CLIP编码为音乐特征；**MoFusion**（Dabral et al., CVPR 2023）——基于扩散的音乐到运动方法，通过拼接两人关节位置适配。所有基线均在DD100上重新训练，但需注意GCD、InterGen和MoFusion原本并非针对双人音乐驱动设计，直接比较的公平性存在一定局限。

### 主实验结果

**Table 2**展示了DD100数据集上的生成质量定量对比。DuetGen在所有指标上均显著优于基线方法：

- **FID**：DuetGen取得1.31的最佳分数，表明单人运动质量最接近真实数据分布。
- **PFID**：DuetGen的配对FID为2.54，大幅领先基线，验证了统一双人表示对协调性建模的有效性。
- **BAS**：节拍对齐分数0.215，表明生成的舞蹈与音乐节奏高度同步。

**用户研究**（**Figure 4**）进一步从感知层面验证了优势。在运动质量、音乐-运动对齐和搭档协调三个维度上，DuetGen均获得超过4分（满分5分）的平均评分，显著优于所有基线方法。这证实了层次掩码建模框架不仅提升了客观指标，也带来了可感知的舞蹈质量提升。

**Figure 5**的定性对比直观展示了差异：基线方法常出现舞者间动作不同步、互穿（interpenetration）或协调性差的问题（图中红色标记），而DuetGen生成的舞蹈保持了自然的双人互动和空间协调。

### VQ-VAE重建质量消融

**Table 1**展示了VQ-VAE模块的消融实验，揭示各设计选择对运动重建精度的影响：

- **完整模型（Ours）**：单人MPJPE最低，双人相对距离误差RDE仅0.17 mm，表明层次标记化与关系全局定位的组合实现了近乎完美的重建。
- **移除关系全局定位（A3）**：RDE飙升至7.12 mm，MPJPE显著升高，证实将B的全局位置表示为相对A的偏移对于精确捕捉双人空间关系至关重要。
- **移除层次标记化（A2）**：采用普通VQ-VAE（单层标记）时，MPJPE升至65.09 mm，RDE达7.12 mm，单人重建误差增加超过30%。这验证了层次化离散表示——顶层捕获语义、底层保留细节——能更有效地压缩和重建双人运动。
- **移除统一表示（A3）**和**移除解码器音乐条件（A6）**：均导致重建质量下降，**Figure 6**的定性结果显示这些消融版本出现互穿和不协调运动。

![[assets/figures/papers/paper_list_l1803_DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative Comparison on VQ-VAE reconstruction. Reconstruction quality of the hierarchical two-person VQ-VAE module of DuetGen compared to its ablations. Notice that the ablations exhibit uncoordinated movements and interpenetration (red circles), while DuetGen achieves interactions and synchronization between the two persons*

### 生成质量消融

**Table 2**的A1-A6消融实验量化了各模块对最终生成质量的贡献：

- **移除关系全局定位（A1）**：FID从1.31升至5.03，PFID从2.54升至14.97，性能退化最为严重。这是最具决定性的证据，表明关系全局定位是双人舞蹈生成的核心设计。
- **移除层次标记化（A2）**和**移除统一表示（A3）**：均导致FID和PFID显著恶化，BAS下降，证实了层次化离散表示和整体建模双人运动的必要性。
- **移除解码器音乐条件（A6）**：生成质量下降，说明音乐信号需要贯穿整个解码过程以维持运动与音频的对齐。

**Figure 5**和**Figure 6**的定性消融对比进一步印证：移除关键模块后，生成的舞蹈出现动作不协调、空间关系混乱等问题。

### 失败模式与局限性

尽管DuetGen在整体指标上表现优异，仍存在以下局限：

1. **手指交互噪声**：**Figure 7**展示了DD100数据集中手指运动存在严重扭曲和互穿伪影。由于数据质量问题，DuetGen未对手指交互进行精细建模，生成的手指动作可能不够自然。这需要手动验证实际生成效果。

![[assets/figures/papers/paper_list_l1803_DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked/figures/009_Figure_7.jpg]]
*Figure 7: Noisy Finger Motions in the DD100 dataset. Common artifacts in the DD100 dataset include twisted or inter-penetrated finger motions (red circles)*

2. **数据规模限制**：训练数据仅约1.9小时，样本多样性有限，可能影响模型对复杂舞蹈风格和长序列的泛化能力。

3. **身体形状固定**：解码阶段依赖数据集中的固定SMPL-X体型，未考虑舞者身体形状变化对交互的影响。

4. **推理效率**：迭代生成需要多轮掩码预测，实时性可能受限。论文未明确讨论推理速度，该点需要手动验证。

5. **数据集局限**：DD100仅包含特定风格的双人舞蹈，模型在更广泛舞蹈类型上的表现有待进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l1803_DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked/figures/005_Table_2.jpg]]
*Table 2: Quantitative Evaluation of Dance Generation. Comparison of motion generation quality between baselines, ablated versions, and our method on the DD100 dataset. Bold indicates best*

![[assets/figures/papers/paper_list_l1803_DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked/figures/004_Table_1.jpg]]
*Table 1: Quantitative Evaluation of VQ Reconstruction. Comparison of motion reconstruction quality after tokenization across ablated versions. Bold indicates the best performance*

![[assets/figures/papers/paper_list_l1803_DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked/figures/006_Figure_4.jpg]]
*Figure 4: User Study Results. Each column indicates the average user rating on a 1-5 scale. DuetGen consistently outperforms all baselines*

![[assets/figures/papers/paper_list_l1803_DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative Comparisons. Dance motions generated by DuetGen, the baselines, and relevant ablations, from the same music input. Notice that the baseline methods and the ablations exhibit uncoordinated movements (red dots), interpenetration (red circles), and drift in root joint positions (red arrows). In contrast, DuetGen maintains natural interactions and well-synchronized two-person dance movements*

## 方法谱系与知识库定位

### 1. 与基线工作的关系

DuetGen 针对**音乐驱动的双人舞蹈生成**这一特定问题，相较于现有方法在问题设定和技术路径上均有显著差异。

**与单人音乐-舞蹈生成方法的差异。** 传统的音乐驱动舞蹈合成方法（如 **MoFusion** (Dabral et al., CVPR 2023)）仅面向单人场景。若将其直接适配至双人任务——例如通过拼接两人关节位置进行训练——则无法显式建模舞伴间的空间协调与交互关系。DuetGen 通过统一双人表示与层次化标记化，将双人运动作为整体进行建模，从根本上区别于简单的拼接策略。

**与群舞/跟随舞蹈生成方法的差异。** 群舞编排方法 **GCD** (Le et al., TOG 2023) 采用对比扩散模型生成多人舞蹈，但其核心目标是群体同步而非紧密的双人交互。跟随舞蹈生成方法 **Duolando** (Siyao et al., ICLR 2024) 则仅生成跟随者动作，需预先给定领导者动作序列，无法从音乐同时生成两位舞者的协调舞蹈。DuetGen 首次实现了从音乐直接生成包含引导-跟随动态与紧密互动的双人舞蹈。

**与文本驱动双人运动生成方法的差异。** **InterGen** (Liang et al., IJCV 2024) 是基于扩散模型的文本到双人运动生成方法。将其适配至音乐驱动任务需替换文本编码为音乐编码，但扩散模型在长序列舞蹈生成中的时序一致性和音乐对齐能力未经充分验证。DuetGen 采用掩码 Transformer 架构，在音乐对齐指标（BAS）上取得了 0.215 的最佳分数 (Table 2)。

### 2. 适用边界

DuetGen 的设计依赖于以下核心假设，这些假设同时界定了其适用范围：

- **双人舞蹈的封闭场景。** 模型仅面向双人舞蹈生成，未涉及三人及以上群舞编排。其统一表示中的关系全局定位（A 的全局速度 + B 相对 A 的位置）天然适配双人配对，但直接推广至多人场景时需重新设计空间关系编码。
- **固定体型的依赖。** 模型在 VQ-VAE 训练与生成阶段均使用 DD100 数据集中的固定 SMPL-X 体型参数，未考虑身体形状变化。这意味着生成的舞蹈运动绑定于特定体型，无法直接迁移至不同体型的角色。
- **数据规模与风格的局限。** DD100 数据集仅包含约 1.9 小时的双人舞蹈动作（4,556 个训练样本），覆盖的舞蹈风格和交互类型有限。模型在训练分布之外的舞蹈风格或复杂交互上的泛化能力尚未验证。
- **手指交互的缺失。** DD100 数据集中手指运动存在严重噪声（Figure 7），导致模型未对手指交互进行精细建模。对于需要手部接触的双人舞蹈（如拉丁舞中的手拉手动作），生成质量可能受限。

### 3. 局限与开放问题

**已识别的局限。**

1. **数据稀缺与质量问题。** 双人舞蹈动作捕捉数据获取成本高，DD100 仅约 1.9 小时，且手指运动噪声严重（Figure 7）。数据瓶颈直接限制了模型对精细交互的建模能力和泛化范围。
2. **推理效率未明确。** 推理过程中的迭代生成需多轮预测（顶层标记 $L_{top}$ 轮迭代 + 底层标记生成），论文未报告推理速度指标，其实时性存疑。
3. **身体形状未纳入生成。** 模型依赖数据集中固定体型，无法根据角色需求调整身体形状，限制了在虚拟人动画等应用中的灵活性。

**开放问题。**

- **如何缓解双人舞蹈数据的稀缺性？** 一个潜在方向是结合专业动作捕捉数据与在线舞蹈视频，通过半监督或弱监督学习扩充训练数据。
- **如何在低质量数据下有效建模手指交互？** 可能需引入手指运动的物理约束或专门的手指重建模块，以在噪声标签下保持重建精度。
- **能否将身体形状变化纳入生成过程？** 将体型参数作为条件输入，或设计体型无关的运动表示，可使模型适配不同角色。
- **层次标记化与掩码建模框架能否推广至其他多人交互场景？** 如体育合作（双人网球）、格斗对抗等，这些场景同样需要空间协调与交互建模，但交互模式与舞蹈存在本质差异，需验证框架的迁移能力。

### 4. 知识库定位

DuetGen 在方法谱系中占据以下位置：

- **问题层级：** 音乐驱动的人体运动生成 → 多人舞蹈生成 → 双人交互舞蹈生成。DuetGen 是首个面向音乐驱动双人舞蹈生成的专门方法。
- **技术路径：** 离散标记化（VQ-VAE）+ 掩码生成式 Transformer。该路径继承自单人运动生成中的 **M2D** 等工作，DuetGen 将其扩展至双人场景，核心创新在于**统一双人表示**与**层次化标记化**的协同设计。
- **关键贡献：** 证明了“将双人运动视为整体 + 粗-细层次化标记”这一组合策略能够有效解决双人舞蹈中的空间协调与交互建模难题，为后续多人交互运动生成提供了可参考的范式。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/DuetGen_Music_Driven_Two_Person_Dance_Generation_via_Hierarchical_Masked_Modeling.pdf]]
