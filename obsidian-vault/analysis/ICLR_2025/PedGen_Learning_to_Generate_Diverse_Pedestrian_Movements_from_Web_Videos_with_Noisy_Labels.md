---
title: "PedGen: Learning to Generate Diverse Pedestrian Movements from Web Videos with Noisy Labels"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos_with_Noisy_Labels.pdf
project_link: null
code_link: null
aliases:
- PedGen
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: PedGen 通过两个关键机制突破瓶颈：1) 重建误差驱动的自动迭代标签过滤与可学习的运动掩码嵌入，使模型能够从含噪声且部分缺失的伪标签中有效学习；2) 新颖的上下文编码器将2D场景深度和语义提升至3D局部体素表示，并结合行人身体形状与目标位置，为扩散去噪网络提供丰富的3D场景理解，从而生成上下文一致的运动。
primary_logic: 将2D像素通过单目深度估计和语义分割反投影为3D局部点云并离散化为体素，既能编码场景的几何与语义信息，又能解耦行人自身与背景，避免模型依赖前景而非场景。再融合目标点和个体特征，即使训练标签含有噪声与缺失，条件扩散模型仍能生成逼真、多样化且贴合3D环境的行人运动。
claims:
- PedGen在CityWalkers验证集上显著超越MDM、HumanMac等基线，并且在Waymo和CARLA数据集上实现零样本泛化
- 自动异常标签过滤带来aADE改善2.9%，而将部分标签作为额外训练数据进一步改善5.8%
- 目标点是最重要的上下文因素，单独提供即可使aADE降低72.9%；同时使用场景、人体形状和目标点三种上下文因素达到最低生成误差
- 分离速度与旋转令牌、加入轨迹损失和几何损失均对最终性能有正向贡献
---

# PedGen: Learning to Generate Diverse Pedestrian Movements from Web Videos with Noisy Labels

> [!tip] 核心洞察
> 将2D像素通过单目深度估计和语义分割反投影为3D局部点云并离散化为体素，既能编码场景的几何与语义信息，又能解耦行人自身与背景，避免模型依赖前景而非场景。再融合目标点和个体特征，即使训练标签含有噪声与缺失，条件扩散模型仍能生成逼真、多样化且贴合3D环境的行人运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | PedGen：从含噪网络视频中学习生成多样化行人运动 |
| 英文题名 | PedGen: Learning to Generate Diverse Pedestrian Movements from Web Videos with Noisy Labels |
| 会议/期刊 | ICLR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PedGen |
| Dataset | CityWalkers, Waymo, CARLA |

> [!tip] 效果简介
> - CityWalkers (无目标) 上，mADE 1.13 vs 1.31 (HumanMAC) (-0.18)；aADE 4.08 vs 4.55 (MDM) (-0.47)。
> - CityWalkers (有目标) 上，aADE 1.08 vs 1.26 (TRUMANS) (-0.18)。
> - Waymo (无目标) 上，mADE 2.90 vs 3.19 (HumanMAC) (-0.29)。

## 概要

从网络视频中学习上下文感知的行人运动生成面临两个核心瓶颈。其一，预训练预测器给出的伪标签不可避免地含有异常和不完整噪声，直接使用会严重损害模型训练。其二，现有人体运动生成方法往往忽略周围3D场景、行人身体形状和目标位置等关键上下文因素，导致生成的运动缺乏环境一致性与物理合理性。**PedGen** 通过两个机制突破上述瓶颈：（1）基于重建误差的迭代式自动标签过滤与可学习的运动掩码嵌入，使模型能从含噪且部分缺失的伪标签中有效学习；（2）一个新颖的上下文编码器，将2D深度和语义信息提升为3D局部体素表示，并融合身体形状与目标点，为条件扩散模型提供丰富的3D场景理解。

核心洞察在于：将2D像素通过单目深度估计和语义分割反投影为3D局部点云并离散化为体素，既能编码场景的几何与语义信息，又能解耦行人与背景，避免模型依赖前景而非场景。即使训练标签含有噪声与缺失，融合目标点和个体特征的条件扩散模型仍能生成逼真、多样化且贴合3D环境的行人运动。

实验表明，PedGen在CityWalkers验证集上显著超越 **MDM**（Tevet et al., 2022）、**HumanMac**（Chen et al., 2023a）、**TRUMANS**（Jiang et al., 2024）等基线方法，并在Waymo和CARLA数据集上实现零样本泛化（Table 1）。消融研究揭示：自动异常标签过滤带来aADE改善2.9%，将部分标签作为额外训练数据进一步改善5.8%；目标点是最重要的上下文因素，单独提供即可使aADE降低72.9%，同时使用场景、人体形状和目标点三种上下文因素达到最低生成误差（Table 2）。分离速度与旋转令牌、加入轨迹损失和几何损失均对最终性能有正向贡献（Table 3）。



### 问题背景：从网络视频中学习行人运动生成

生成逼真且多样化的人体运动是计算机视觉与图形学中长期存在的核心挑战。近年来，数据驱动的方法在受控实验室或固定场景下取得了显著进展，但这些方法普遍依赖高质量的运动捕捉数据，获取成本高昂且场景覆盖有限。与此同时，互联网上存在海量的行人视频，其中蕴含着丰富的运动模式、多样的身体形态和真实的城市场景——若能有效利用这些数据，将极大地推动上下文感知的行人运动生成技术的发展。

然而，从网络视频中学习行人运动生成面临两个关键瓶颈：

**瓶颈一：伪标签噪声不可避免。** 要从网络视频中获取运动标签，通常需要依赖预训练的4D人体运动预测器（如WHAM）进行自动标注。这些伪标签不可避免地包含两类噪声：（1）**异常标签**——由于预测器在复杂场景下的失效，部分样本的运动估计完全错误；（2）**不完整标签**——因遮挡或跟踪失败，部分时间步的运动参数缺失。直接使用这些含噪标签训练生成模型，会严重损害模型的学习效果和生成质量。

**瓶颈二：上下文因素被长期忽略。** 现有的人体运动生成方法——无论是基于文本/动作条件的扩散模型（如**MDM**, Tevet et al., 2022），还是基于历史序列的运动预测方法（如**HumanMAC**, Chen et al., 2023a）——大多将人体视为孤立于环境的运动体，忽略了行人运动天然受到周围场景几何、个体身体特征和行进目标点等多重上下文因素的约束。即便少数工作（如**TRUMANS**, Jiang et al., 2024）尝试引入场景条件，也仅限于室内受控环境，且仅使用2D图像特征，缺乏对3D场景几何与语义的深层理解。因此，现有方法难以生成在真实城市场景中既符合物理约束又贴合环境语义的行人运动。

### 方法缺口：缺乏噪声鲁棒且上下文感知的生成框架

上述瓶颈揭示了当前研究中的一个显著缺口：**缺乏一种既能从含噪伪标签中鲁棒学习，又能有效编码3D场景、人体特征和目标点等多种上下文因素的统一生成框架。** 具体而言：

- **标签质量处理方面**，现有方法要么直接使用所有伪标签（完全忽略噪声），要么仅依赖简单的规则过滤（缺乏自适应能力），没有针对异常标签和不完整标签分别设计的有效处理机制。
- **场景上下文编码方面**，现有方法或完全不编码场景信息，或将场景图像通过2D视觉骨干（如DINO-v2）提取特征后简单注入，未能将2D观测提升至3D空间以编码几何结构，也无法有效解耦行人自身前景与背景场景，导致模型可能依赖前景线索而非真实场景信息。
- **多因素融合方面**，现有工作未系统研究场景、人体形状、目标点等不同上下文因素对运动生成的独立与联合贡献，缺乏对因素间因果关系的定量理解。

### 本文动机：PedGen的设计目标

基于上述分析，本文提出**PedGen**——首个面向上下文感知行人运动生成的条件扩散模型，其设计目标直指两大瓶颈：

1. **噪声标签鲁棒学习**：通过迭代式重建误差驱动的自动异常标签过滤，以及可学习运动掩码嵌入以利用不完整标签，使模型能够从大规模网络视频的含噪伪标签中有效提取训练信号。
2. **3D场景感知的上下文编码**：将2D深度图与语义分割图通过单目几何反投影提升为3D局部体素表示，融合行人身体形状与目标位置，为扩散去噪网络提供丰富的3D场景理解，从而生成与真实环境几何和语义一致的多样化行人运动。

通过在自建的大规模网络视频数据集**CityWalkers**（含104,192个训练样本，覆盖多样化的真实城市场景与行人运动）上的系统验证，以及在Waymo真实场景和CARLA仿真环境上的零样本泛化测试，PedGen旨在证明：即使训练标签含有显著噪声与缺失，条件扩散模型仍能生成逼真、多样化且贴合3D环境的行人运动。



## 核心方法与创新机理

PedGen 的核心创新在于针对“从含噪网络视频学习上下文感知行人运动生成”这一任务，系统性地重构了标签利用策略和场景上下文编码方式，形成了四个关键的 changed slots。

### 1. 从被动接受噪声到主动迭代过滤的标签质量处理

现有运动生成方法通常假设训练标签是完整且准确的。PedGen 面对 CityWalkers 数据集中由预训练预测器产生的伪标签，首次引入了**重建误差驱动的自动迭代标签过滤**机制。其逻辑是：模型在训练初期对低质量异常标签的重建误差会显著偏高，因此可以基于无监督异常检测原理自动识别并移除这些样本。更重要的是，该过程并非一次性完成——PedGen 采用数据迭代策略，在每轮过滤后重新训练模型，利用逐步提升的模型能力发现更隐蔽的异常标签。实验表明，仅需两个迭代即可达到最佳性能（Table 6），且自动过滤带来 aADE 改善 2.9%（Table 2a）。

针对过滤后仍保留的**部分标签**（即某些时间步缺失的样本），PedGen 没有简单丢弃这些宝贵数据，而是设计了一个**可学习的运动掩码嵌入**（motion mask embedding），替换缺失时间步的输入令牌。这使得模型能够将部分标签作为额外训练数据加以利用，进一步带来 5.8% 的 aADE 改善（Table 2a）。这一“过滤+利用”的双重策略，使 PedGen 在标签质量远低于学术数据集的条件下仍能稳定训练。

### 2. 从 2D 图像特征到 3D 局部体素的场景上下文编码

现有场景条件运动生成方法（如 **TRUMANS**，Jiang et al., 2024）多使用 2D 图像特征编码场景，或仅适用于室内受控环境。PedGen 的**上下文编码器**（Context Encoder）则实现了从 2D 到 3D 的质的飞跃：首先将单目深度估计和语义分割结果反投影为 3D 点云，然后以行人初始位置为中心提取局部邻域点云：

$$\mathcal{P}_{\mathrm{local}} = \left\{ \mathbf{p} \in \mathcal{P} \ \vert \ \Vert p_x - x_1 \Vert < \Delta_x, \Vert p_y - y_1 \Vert < \Delta_y, \Vert p_z - z_1 \Vert < \Delta z \right\}$$

随后将局部点云体素化为 3D 网格，通过交叉注意力层编码几何与语义信息。这一设计的关键洞察在于：**将 2D 像素提升为 3D 体素表示，既能编码场景的几何结构与语义类别，又能自然解耦行人自身与背景**，避免模型依赖前景而非场景。消融实验证实，仅添加场景上下文即可使 aADE 降低 15.7%（Table 2b, setting 1→5）。

### 3. 速度与旋转分离的令牌化设计

传统 Transformer 运动生成模型（如 **MDM**，Tevet et al., 2022）将每帧的所有运动参数编码为单一令牌。PedGen 发现将**速度与旋转作为独立的 Transformer 令牌**处理效果更好，原因在于两者具有不同的表示空间和数值尺度——速度是平动向量，旋转是角度参数，分开编码使注意力机制能够更精细地建模各自的时序依赖。消融实验表明，这一设计对最终性能有正向贡献（Table 3b）。

### 4. 多目标联合优化的训练损失

PedGen 将标准扩散重构损失扩展为三项联合优化目标：

$$\mathcal{L}(\pmb{x}, \hat{\pmb{x}}) = \mathbb{E}_{k \in [1, K], (\pmb{x}, \pmb{c}) \in \mathcal{D}} \big[ w_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}} + w_{\mathrm{traj}} \mathcal{L}_{\mathrm{traj}} + w_{\mathrm{geo}} \mathcal{L}_{\mathrm{geo}} \big]$$

其中 $\mathcal{L}_{\mathrm{traj}}$ 是轨迹损失，约束生成运动的全局路径与真值一致；$\mathcal{L}_{\mathrm{geo}}$ 是基于前向运动学的几何损失，惩罚脚部滑动、关节异常等物理不一致。消融显示，两项额外损失均有独立正向贡献，全部组件组合达到最优（Table 3b）。



PedGen 的整体设计围绕一个核心矛盾展开：如何从大规模网络视频中学习上下文感知的行人运动生成，同时应对伪标签不可避免的噪声与缺失。为此，PedGen 构建了一条从含噪标签清洗到条件扩散生成的完整流水线，其架构与数据流可概括为四个耦合阶段（参见 Figure 3）。

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/004_Figure_3.jpg]]
*Figure 3: Our method. We discard the anomaly labels with an iterative automatic label filtering procedure and add the partial labels to training data. We then train PedGen with a Context Encoder to represent crucial context factors. The scene context is obtained by lifting the 2D depth and semantic labels to the 3D space and converting them into a local voxel representation. The encoded scene context is combined with other context factors, including the body shape and the goal to get the context embedding c. The context embedding c and the timestep embedding k are then used to guide the Denoising Transformer to predict the clean motion from the noised one. We use a learnable motion mask embedding m t...*

**阶段一：自动标签过滤与部分标签利用。** 原始 CityWalkers 数据集的伪标签由预训练预测器生成，包含两类噪声——异常标签（严重偏离物理真实的运动）和部分标签（因遮挡或跟踪失败导致的时间步缺失）。PedGen 采用迭代式重建误差驱动的无监督异常检测策略：先用当前干净子集训练模型，再对全量数据计算重建误差，将误差显著偏高的样本标记为异常并移除，随后用更新后的子集重新训练，如此迭代两轮即可达到最优性能（Table 6）。对于部分标签，PedGen 引入可学习的运动掩码嵌入 $m$，替换缺失时间步的输入令牌，使模型能从这些不完整样本中提取有效运动模式。消融实验表明，仅移除异常标签即可使 aADE 改善 2.9%，而将部分标签作为额外训练数据进一步带来 5.8% 的增益（Table 2a）。

**阶段二：上下文编码器。** 这是 PedGen 实现场景感知的关键模块。输入包含场景图像 $\mathcal{I}$、深度图 $\mathcal{I}^d$、语义分割图 $\mathcal{I}^s$、行人形状估计 $\tilde{\beta}$ 以及起止位置 $t_1, t_T$。场景上下文通过“2D→3D 提升”获得：首先利用单目深度估计将 2D 像素反投影为 3D 点云 $\mathcal{P}$，然后以行人起始位置为中心提取局部邻域点云 $\mathcal{P}_{\text{local}}$（公式见 Section 4.4），再将其体素化为离散 3D 网格，最后通过单层交叉注意力编码为场景嵌入。人体形状 $\tilde{\beta}$ 和目标点 $t_T$ 分别经独立编码后与场景嵌入融合，得到统一的条件嵌入 $c$。这种设计将几何与语义信息从 2D 像素解耦至 3D 空间，避免了模型过度依赖前景行人特征而忽略真实场景结构。

**阶段三：去噪 Transformer 与运动令牌化。** PedGen 遵循条件扩散框架，去噪网络采用 Transformer 架构。与传统运动生成方法不同，PedGen 将运动参数分离为速度令牌和旋转令牌分别处理，以适应两者在表示空间和数值尺度上的差异。训练时，条件嵌入 $c$ 与时间步嵌入 $k$ 共同引导去噪 Transformer 从噪声运动样本 $\hat{x}$ 中预测干净运动 $x$。

**阶段四：多损失联合优化。** 训练目标由三项损失加权组合构成：
$$\mathcal{L}(\pmb{x}, \hat{\pmb{x}}) = \mathbb{E}_{k \in [1, K], (\pmb{x}, \pmb{c}) \in \mathcal{D}} \big[ w_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}} + w_{\mathrm{traj}} \mathcal{L}_{\mathrm{traj}} + w_{\mathrm{geo}} \mathcal{L}_{\mathrm{geo}} \big]$$
其中 $\mathcal{L}_{\text{rec}}$ 为标准扩散重构损失，$\mathcal{L}_{\text{traj}}$ 为轨迹损失（约束根节点平移的全局路径），$\mathcal{L}_{\text{geo}}$ 为基于前向运动学的几何损失（约束关节点位置的物理一致性）。消融实验证实，三项损失和速度/旋转分离令牌均对最终性能有正向贡献，全部组件组合达到最优（Table 3b）。

**推理流程。** 给定场景上下文和（可选的）目标点，PedGen 从随机噪声出发，通过迭代去噪生成 SMPL 运动参数序列 $\{t_t, \phi_t, \pmb{\theta}_t, \beta\}$。当给定目标点 $t_T$ 时，模型额外计算速度缩放因子 $\lambda = (t_T - t_1) / \hat{t}_T$，以确保生成轨迹精确收敛至目标位置。

整个流水线的核心洞察在于：通过将 2D 场景提升至 3D 体素表示并融合多源上下文，再辅以迭代标签清洗和部分标签掩码机制，条件扩散模型即使在大规模含噪数据上也能学习到逼真、多样化且与 3D 环境一致的行人运动。



PedGen 的整体架构围绕条件扩散框架构建，其核心设计目标是从含噪网络视频标签中学习上下文感知的行人运动生成。方法由四个紧密协作的模块构成，并在运动表示、损失函数和上下文编码层面引入了若干关键公式。

### 运动表示与令牌化

行人运动采用 SMPL 模型参数表示，每一时刻 $t$ 的运动状态由根节点平移 $t_t$、根节点旋转 $\phi_t$、身体姿态参数 $\pmb{\theta}_t$ 以及全局共享的形状参数 $\beta$ 组成：

$$\{ t_t, \phi_t, \pmb{\theta}_t, \beta \}$$

上下文标签 $\pmb{y}$ 则整合了场景图像 $\mathcal{I}$、深度图 $\mathcal{I}^d$、语义分割图 $\mathcal{I}^s$、人体形状估计 $\tilde{\beta}$ 以及起始位置 $t_1$ 和终点位置 $t_T$：

$$\pmb{y} = [ \mathcal{I}, \mathcal{I}^d, \mathcal{I}^s, \tilde{\beta}, t_1, t_T ]$$

在去噪 Transformer 内部，PedGen 将速度与旋转分离为独立的 Transformer 令牌，以应对两者在表示形式和数值尺度上的差异，这一设计在消融实验中被验证对最终性能有正向贡献（Table 3b）。

### 训练损失函数

PedGen 的总体训练目标由三个加权损失项联合优化，其完整形式为：

$$\mathcal{L}(\pmb{x}, \hat{\pmb{x}}) = \mathbb{E}_{k \in [1, K], (\pmb{x}, \pmb{c}) \in \mathcal{D}} \big[ w_{\mathrm{rec}} \mathcal{L}_{\mathrm{rec}} + w_{\mathrm{traj}} \mathcal{L}_{\mathrm{traj}} + w_{\mathrm{geo}} \mathcal{L}_{\mathrm{geo}} \big]$$

其中各项含义如下：
- $\mathcal{L}_{\mathrm{rec}}$：标准扩散重构损失，驱动去噪网络从噪声运动样本 $\pmb{x}$ 中预测干净运动 $\hat{\pmb{x}}$；
- $\mathcal{L}_{\mathrm{traj}}$：轨迹损失，约束生成运动的根节点轨迹与真实轨迹的一致性；
- $\mathcal{L}_{\mathrm{geo}}$：基于前向运动学的几何损失，惩罚生成运动中的脚部滑动、地面穿透等物理不一致现象；
- $w_{\mathrm{rec}}$、$w_{\mathrm{traj}}$、$w_{\mathrm{geo}}$ 为各损失项的权重系数。

消融实验表明，同时使用三项损失（而非仅用重构损失）可取得最优性能（Table 3b）。

### 自动标签过滤模块

该模块通过重建误差驱动的无监督异常检测技术，迭代识别并移除数据集中的低质量伪标签。具体流程为：先训练一个初始 PedGen 模型，计算每个训练样本的重建误差；将误差显著偏高的样本标记为异常标签并移除；随后用清洗后的数据重新训练模型，重复上述过程。实验表明，两个迭代周期即可达到最佳性能（Table 6），移除异常标签使 aADE 改善 2.9%（Table 2a）。

### 部分标签处理模块

对于仅包含部分时间步标注的不完整标签，PedGen 引入可学习的运动掩码嵌入 $\mathbf{m}$，在训练时替换缺失时间步的令牌输入去噪 Transformer。这使得模型能够将 53,405 个部分标签样本作为额外训练数据加以利用，进一步带来 aADE 改善 5.8%（Table 2a）。

### 上下文编码器

上下文编码器负责将多种上下文因素融合为统一的条件嵌入 $\mathbf{c}$，其核心创新在于场景上下文的 3D 提升与体素化编码。具体步骤如下：

1. **2D→3D 反投影**：利用深度标签 $\mathcal{I}^d$ 和相机参数，将 2D 图像像素反投影为 3D 点云 $\mathcal{P}$，同时将语义分割标签 $\mathcal{I}^s$ 附着到对应 3D 点上，赋予每个点语义类别信息。

2. **局部邻域提取**：以行人起始位置 $(x_1, y_1, z_1)$ 为中心，从全局点云中裁切局部邻域点云：

$$\mathcal{P}_{\mathrm{local}} = \left\{ \mathbf{p} \in \mathcal{P} \ \vert \ \Vert p_x - x_1 \Vert < \Delta_x, \Vert p_y - y_1 \Vert < \Delta_y, \Vert p_z - z_1 \Vert < \Delta z \right\}$$

3. **体素化与编码**：将局部点云离散化为 3D 体素网格，每个体素编码其内部点的几何占据与语义分布信息，随后通过单层交叉注意力层将体素特征聚合为场景上下文表示。

4. **多因素融合**：将编码后的场景上下文与人体形状 $\tilde{\beta}$、目标位置 $t_T$ 等信息融合，生成最终的条件嵌入 $\mathbf{c}$，用于引导去噪 Transformer 的生成过程。

### 目标条件速度缩放

当给定目标点条件时，PedGen 在推理阶段引入速度缩放因子 $\lambda$，以确保生成运动的终点精确到达目标位置：

$$\lambda = (t_T - t_1) / \hat{t_T}$$

其中 $\hat{t_T}$ 为模型预测的终点位置，通过缩放预测速度使累积位移与目标位移一致（Appendix C）。



## 实验与关键发现

### 主结果：PedGen 在真实与仿真环境中的生成性能

为验证 PedGen 在上下文感知行人运动生成任务上的有效性，作者在 CityWalkers 验证集、Waymo 真实世界测试集和 CARLA 仿真测试集上，分别在有目标点（goal）和无目标点两种设定下，与三类代表性基线方法进行了全面比较（Table 1）：

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/006_Table_1.jpg]]
*Table 1: Comparison to baselines. We consider two cases where the model is given the goal condition or not. We evaluate on the validation set of CityWalkers, the real-world Waymo test set, and the simulated CARLA test set. We evaluate our model (PedGen) compared with the other baselines*

- **MDM**（Tevet et al., 2022）：以文本或动作标签为条件的运动生成方法；
- **HumanMac**（Chen et al., 2023a）：以历史运动序列为条件的运动预测方法；
- **TRUMANS**（Jiang et al., 2024）：以室内场景上下文为条件的运动生成方法。

所有基线方法均根据新任务定义做出最小必要调整，以适配上下文条件输入。

#### CityWalkers 验证集结果

在 CityWalkers 验证集上，PedGen 在所有指标上均显著超越基线：

- **无目标点设定**：PedGen 的 mADE 为 1.13，相比最优基线 HumanMAC（1.31）降低 **13.7%**；aADE 为 4.08，相比最优基线 MDM（4.55）降低 **10.3%**；mFDE 和 aFDE 同样取得最低值（1.61 和 7.56），表明生成的运动在平均误差和多样性方面均具优势。
- **有目标点设定**：PedGen 的 mADE 进一步降至 0.59，aADE 降至 1.08，mFDE 和 aFDE 分别为 0.46 和 0.99，在所有指标上均优于 TRUMANS 等基线，证明目标点条件对运动精度的巨大提升作用。

#### 零样本泛化：Waymo 与 CARLA

PedGen 展现出优异的零样本泛化能力：

- **Waymo 真实场景**：无目标点设定下，PedGen 的 mADE 为 2.90，优于 HumanMAC 的 3.19；有目标点设定下，mADE 进一步降至 1.44，显著低于 TRUMANS 的 2.08。
- **CARLA 仿真场景**：PedGen 在物理合理性指标上表现突出——无目标点设定下碰撞率（CR）仅为 1.6%，低于 MDM 的 2.1%；有目标点设定下脚部浮空率（FFR）为 0.0%，而 TRUMANS 高达 60.6%，表明 PedGen 生成的 3D 运动与场景几何高度吻合，避免了穿透和浮空等常见伪影。

这些结果表明，PedGen 不仅能在训练域内生成高质量运动，还能在未见过的真实和仿真环境中保持鲁棒性，这得益于其 3D 场景上下文编码器对几何与语义信息的有效建模。

### 消融实验：噪声标签处理与上下文因素贡献

#### 噪声标签处理策略的有效性（Table 2a）

为验证自动标签过滤和部分标签利用策略的效果，作者在无上下文条件下进行了消融实验：

- **仅移除异常标签**：相比直接使用全部伪标签，自动过滤异常标签使 aADE 改善 **2.9%**，证明基于重建误差的迭代过滤能有效识别并剔除低质量样本。
- **进一步加入部分标签**：在异常标签过滤基础上，将部分标签（至少 30 帧）作为额外训练数据，并使用可学习运动掩码嵌入处理缺失时间步，使 aADE 进一步改善 **5.8%**。这表明部分标签虽不完整，但仍蕴含有用运动信息，掩码嵌入机制能有效利用这些信息提升模型性能。

#### 上下文因素的贡献分解（Table 2b）

作者系统消融了三种上下文因素——场景（scene）、人体形状（human）和目标点（goal）——对生成性能的影响：

- **目标点是最关键的上下文因素**（setting 6 vs. 无上下文 baseline）：单独提供目标点条件即可使 aADE 从 4.08 骤降至 1.11，降幅达 **72.9%**，mADE 从 1.13 降至 0.63。这揭示了目标位置对行人运动生成的强约束作用。
- **场景上下文的独立贡献**（setting 2）：仅提供场景上下文（不含目标点和人体形状），aADE 为 3.82，mADE 为 1.09，相比无上下文 baseline 仅有微弱改善。这表明 3D 场景编码本身对运动生成的约束力有限，其价值更多体现在与目标点等其他因素的协同作用中。
- **人体形状的独立贡献**（setting 3）：仅提供人体形状信息，aADE 为 4.01，mADE 为 1.12，改善幅度极小，说明个体身体特征对运动轨迹的约束较弱。
- **场景与目标点的协同**（setting 7 vs. setting 6）：在目标点基础上加入场景上下文，mADE 从 0.63 进一步降至 0.56，aADE 从 1.11 降至 0.98，证明 3D 场景信息能帮助模型生成更贴合环境的运动路径。
- **三种因素全部使用**（setting 8）：同时提供场景、人体形状和目标点，达到最低生成误差（mADE 0.54，aADE 0.96），验证了多上下文因素融合的有效性。

定性结果（Figure 5）进一步佐证了上述发现：缺少场景上下文时，生成的运动可能穿越建筑物或障碍物；缺少目标点时，运动方向和终点位置不可控；三者结合则能生成自然且符合场景约束的行人运动。

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of training with context factors. We compare the generated movements of PedGen trained with or without context factors in real-world environments (a) and in simulation (b)*

#### 模型组件消融（Table 3b）

对 PedGen 关键设计选择的消融分析表明：

- **分离速度与旋转令牌**：将速度和旋转合并为单一令牌会导致 mADE 从 1.13 升至 1.21，aADE 从 4.08 升至 4.29，验证了分离令牌处理不同表示和尺度的必要性。
- **轨迹损失**：移除轨迹损失使 mADE 升至 1.18，aADE 升至 4.22，表明直接监督根节点轨迹有助于提升运动精度。
- **几何损失**：移除基于前向运动学的几何损失使 mADE 升至 1.17，aADE 升至 4.18，说明显式约束关节运动学有助于减少物理不合理性。
- **所有组件组合**达到最优性能，证明各设计选择具有互补效应。

#### 训练数据规模与过滤迭代次数（Table 3a, Table 6）

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/024_Table_6.jpg]]
*Table 6: Ablation on the number of filtering iterations. We evaluate PedGen with no context on the CityWalkers validation set*

- **仅用 SLOPER4D 小数据集训练**（Table 3a）：mADE 高达 3.82，远高于使用 CityWalkers 大数据的 1.13，说明小规模精确标注数据不足以支撑上下文感知运动生成任务，大规模数据（即使含噪）至关重要。
- **自动标签过滤迭代次数**（Table 6）：仅进行两轮迭代即可达到最佳性能（mADE 1.13，aADE 4.32），继续增加迭代轮次未见进一步改善，表明两轮过滤已能有效剔除大部分异常样本。

### 失败模式与局限性分析

尽管 PedGen 在定量和定性评估中表现优异，但分析揭示了若干失败模式和局限性：

1. **长时间运动衔接问题**：生成的运动在长时间范围内可能出现微小的脚下滑动或与场景轮廓的轻微穿透，物理一致性有待进一步提高。这源于扩散模型对长序列的误差累积以及 3D 体素表示的有限分辨率。

2. **动态智能体交互缺失**：当前方法仅考虑静态场景和单个行人的运动生成，未建模行人与其他动态智能体（车辆、其他行人）之间的交互，导致在拥挤场景中生成的运动可能缺乏社交合理性。

3. **自动标签过滤的误删风险**：基于重建误差的异常检测可能误删除具有新颖但正确运动模式的样本，尤其在运动类型高度多样化的数据集中。Figure 15 可视化了被过滤的标签样本，部分样本确实呈现异常姿态，但少数被过滤样本的运动模式可能具有合理性。

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/023_Figure_15.jpg]]
*Figure 15: Visualizations of anomaly labels in CityWalkers. We visualize the filtered labels in the first and the second iterations of automatic anomaly label filtering*

4. **数据集地域偏差**：CityWalkers 数据集的地域覆盖偏重于欧洲和部分亚洲城市，可能使模型在完全不同文化背景的路权规则或建筑风格下泛化能力受限。

5. **部分标签掩码嵌入的不稳定性**：可学习运动掩码嵌入在处理极端缺失（如仅保留极少帧）的部分标签时，可能引入额外的学习不稳定，表现为生成运动在缺失段落的突然跳变。

### 重要图表结论

- **Table 1**：PedGen 在 CityWalkers、Waymo 和 CARLA 三个测试场景上全面超越基线，在有目标点条件下优势尤为显著（mADE 低至 0.59），并展现出优异的零样本泛化能力。
- **Table 2a**：自动异常标签过滤和部分标签利用分别带来 2.9% 和 5.8% 的 aADE 改善，验证了噪声标签处理策略的有效性。
- **Table 2b**：目标点是最重要的上下文因素，单独提供即可使 aADE 降低 72.9%；三种上下文因素联合使用达到最低生成误差。
- **Table 3b**：分离速度/旋转令牌、轨迹损失和几何损失均对性能有正向贡献，所有组件组合达到最优。
- **Figure 5**：定性展示了上下文因素的消融效果——缺少场景上下文导致穿墙，缺少目标点导致方向不可控，三者结合生成自然且场景一致的运动。

### 补充图表

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/008_Table.jpg]]
*Table: (a) Evaluation of training with noisy labels. We evaluate PedGen with no context trained with or without anomaly and partial labels*

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/009_Table.jpg]]
*Table: (b) Evaluation of the context factors. We evaluate PedGen conditioned on each context factor, including the surrounding environment (scene), the pedestrian’s own characteristics (human), and the goal points (goal)*

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/010_Table_3.jpg]]
*Table 3: Ablation experiment results. We ablate on the training data of PedGen (a) and the PedGen model’s key components (b) on the CityWalkers validation set*

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/005_Figure_4.jpg]]
*Figure 4: Visualizations of the generated pedestrian movements. The top row shows results in real scenes from the CityWalkers dataset, the middle row shows results in the real-world Waymo test set, and the bottom row shows results in simulated scenes from the CARLA test set*

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/001_Figure_1.jpg]]
*Figure 1: Pedestrian Movement Generation. Our method can generate diverse pedestrian movements in real-world (top row) and simulated (bottom row) urban environments*

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/011_Figure_6.jpg]]
*Figure 6: Pedestrian movement prediction in Waymo. We predict long-term pedestrian movements using PedGen*

![[assets/figures/papers/paper_list_l1904_PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos/figures/019_Figure_12.jpg]]
*Figure 12: Samples of 4D pedestrian movement labels in CityWalkers. The text descriptions of the movements from top left to bottom right are: walking down stairs (pink), turning and lifting baggage up steps (light green), walking up stairs (dark purple), turning around with phone in hand (sky blue), moving hands to hip (dark green), wiping seats and tables (red), jumping and skipping around (yellow), taking photo and standing up (light purple)*



## 定位与知识库关联

### 任务定位与基线谱系

PedGen 提出了一个新任务——**上下文感知的行人运动生成**（context-aware pedestrian movement generation），其核心区别于现有工作的三个维度是：（1）从真实世界网络视频而非受控实验室数据学习；（2）同时编码场景几何/语义、行人身体形状和目标点三类上下文因素；（3）在伪标签含噪声且部分缺失的条件下完成训练。

在基线谱系上，PedGen 与三类方法形成对照：

- **无条件/动作条件运动生成**：以 **MDM**（Tevet et al., 2022）为代表，使用文本或动作标签作为条件，通过扩散模型生成人体运动。MDM 不编码场景上下文，因此在 CityWalkers 无目标设置下 aADE 达 4.55，而 PedGen 为 4.08（Table 1）。MDM 的核心局限在于生成的运动与 3D 环境无关，脚部浮空率（FFR）在 CARLA 有目标条件下高达 60.6%（PedGen 为 0.0%）。

- **历史条件运动预测**：以 **HumanMAC**（Chen et al., 2023a）为代表，基于历史运动序列预测未来运动。HumanMAC 同样不编码场景上下文，在 CityWalkers 无目标设置下 mADE 为 1.31（PedGen 为 1.13），Waymo 零样本泛化时 mADE 为 3.19（PedGen 为 2.90）。其瓶颈在于缺乏对周围障碍物和目标点的理解，导致长期预测出现场景穿透。

- **场景条件运动生成**：以 **TRUMANS**（Jiang et al., 2024）为代表，使用室内场景图像作为条件生成人体运动。TRUMANS 的上下文编码依赖 2D 图像特征，无法显式建模 3D 几何约束。在 CityWalkers 有目标设置下，TRUMANS 的 aADE 为 1.26，PedGen 为 1.08；在 CARLA 仿真环境中，TRUMANS 因缺乏对 3D 场景的正确理解而出现严重脚部浮空（FFR 60.6%）。

PedGen 相对于上述基线的关键差异化在于：将 2D 深度和语义标签反投影为 3D 局部点云并体素化，通过交叉注意力编码 3D 几何与语义信息，使生成的运动在物理上贴合场景表面。

### 方法谱系中的技术继承与创新

PedGen 的技术架构沿袭了条件扩散模型的通用框架（Ho et al., 2020; Ho & Salimans, 2022），其去噪 Transformer 遵循了当前主流的人体运动生成架构设计。在此基础上，PedGen 引入了四项关键创新：

1. **噪声标签处理策略**：不同于基线方法直接使用所有伪标签或仅做规则过滤，PedGen 采用**重建误差驱动的迭代自动过滤**（Section 4.3）——利用模型在异常标签上重建误差更大的特性，自动识别并移除低质量样本。该策略与异常检测领域基于重建的无监督方法原理一致，但被首次系统应用于人体运动生成的伪标签清洗。消融实验表明，移除异常标签后 aADE 改善 2.9%，而将部分标签作为额外训练数据进一步改善 5.8%（Table 2a）。

2. **部分标签的可学习掩码嵌入**：针对网络视频中因遮挡或跟踪失败导致的标签不完整问题，PedGen 使用可学习的运动掩码嵌入 $m$ 替换缺失时间步（Section 4.3）。这一设计借鉴了掩码自编码器（MAE）的思想，但被适配到序列运动数据的条件扩散训练中，使模型能从 53,405 个部分标注样本中学习（占总训练集的 51.2%）。

3. **3D 局部体素场景编码**：PedGen 的上下文编码器将 2D 深度图 $\mathcal{I}^d$ 和语义分割图 $\mathcal{I}^s$ 反投影为 3D 点云 $\mathcal{P}$，提取以起始位置为中心的局部邻域点云 $\mathcal{P}_{\mathrm{local}}$，体素化为 3D 网格后通过交叉注意力编码（Section 4.4）。这一设计的核心洞察在于：通过局部裁切解耦行人自身前景与背景场景，避免模型依赖前景特征而非场景结构。该编码方式与 3D 视觉中的点云体素化方法原理相通，但被创新性地应用于为运动扩散模型提供空间条件。

4. **速度-旋转分离令牌与多目标损失**：PedGen 将运动的速度和旋转作为独立的 Transformer 令牌处理（Section 4.2），以应对两者在表示空间和数值尺度上的差异。训练损失函数联合优化重构损失 $\mathcal{L}_{\mathrm{rec}}$、轨迹损失 $\mathcal{L}_{\mathrm{traj}}$ 和基于前向运动学的几何损失 $\mathcal{L}_{\mathrm{geo}}$（Equation 1）。消融实验证实，分离令牌、轨迹损失和几何损失均对最终性能有正向贡献，所有组件组合达到最优（Table 3b）。

### 上下文因素的贡献分解

PedGen 对三类上下文因素的消融揭示了它们在运动生成中的相对重要性（Table 2b）：

- **目标点**是最关键的上下文因素：单独提供目标点即可使 aADE 从无上下文时的 3.53 降至 0.96（降低 72.9%，setting 6 vs setting 1），这解释了为何有目标条件下所有方法的表现均显著优于无目标条件（Table 1）。
- **场景上下文**单独使用时改善有限（aADE 3.28 vs 3.53），但与目标点结合后产生协同效应（aADE 0.90, setting 7），表明场景信息主要在目标导向的运动中约束路径选择。
- **人体形状**的独立贡献较小，但与场景和目标点三者结合时达到最低生成误差（mADE 0.54, aADE 0.96, setting 8），说明个体特征在精细化运动生成中起补充作用。

### 适用边界与局限

PedGen 的适用范围和局限可从以下四个维度界定：

1. **静态场景假设**：当前方法仅考虑静态场景，未建模行人与其他动态智能体（车辆、其他行人）之间的交互，也不涉及群体行为。在 Waymo 等真实交通场景中，行人运动往往受到周围车辆和行人的影响，PedGen 目前无法捕捉这些社交交互信号。

2. **伪标签噪声的固有限制**：尽管自动标签过滤和掩码嵌入有效缓解了噪声问题，但伪标签噪声仍不可避免。自动过滤可能误删除具有新颖但正确运动模式的样本（例如罕见动作），而部分标签掩码嵌入可能引入额外的学习不稳定。Table 3a 显示，仅用 SLOPER4D 小数据集训练会导致严重过拟合（mADE 高达 3.82），说明大规模数据对模型泛化至关重要，但也使模型对数据质量更加敏感。

3. **地域与场景多样性**：CityWalkers 数据集虽然规模大（104,192 个训练样本），但地域覆盖偏重于欧洲和部分亚洲城市。模型在完全不同文化背景的路权规则、建筑风格或行人行为规范下，泛化能力可能受限。Waymo 和 CARLA 的零样本测试虽展示了跨域泛化潜力，但测试场景与训练数据仍存在一定分布重叠。

4. **物理一致性的微观缺陷**：生成的运动在长时间范围内衔接可能仍会出现微小的脚下滑动或与场景轮廓的轻微穿透。尽管几何损失 $\mathcal{L}_{\mathrm{geo}}$ 和轨迹损失 $\mathcal{L}_{\mathrm{traj}}$ 已显著缓解了这一问题（FFR 降至 0.0%），但在极端场景（如狭窄通道、陡峭台阶）下，物理一致性有待进一步提高。

### 开放问题与后续方向

基于 PedGen 的方法定位和局限分析，以下开放问题值得后续工作关注：

1. **多智能体交互扩展**：如何将行人运动生成扩展到多智能体交互场景，联合建模行人之间的社交互动（如避让、跟随、结伴）与场景共享？这需要引入交互编码器，并可能借助图神经网络或注意力机制建模智能体间的关系。

2. **弱监督与自监督学习**：能否利用自监督或半监督方法在无伪标签或少标签条件下学习上下文感知的运动生成，进一步降低对标注质量的依赖？例如，利用场景几何一致性作为自监督信号，或通过对抗学习缩小合成数据与真实数据的域差异。

3. **动态场景适应**：如何将 2D-3D 提升的上下文编码器推广到包含移动障碍物的动态场景，并实时捕捉场景变化对运动的影响？这需要编码器具备时序建模能力，可能融合视频帧序列或 4D 场景表示。

4. **多活动类型统一建模**：当前方法是否适用于更剧烈的非步行行为（如跑步、跳跃、上下楼梯），以及如何统一建模多种活动类型的上下文条件生成？CityWalkers 数据集中已包含部分非步行行为（Figure 12），但模型在这些类别上的表现尚未被系统评估。

5. **物理仿真集成**：是否可以将 PedGen 与物理仿真器（如 CARLA）形成闭环，利用仿真反馈进一步优化生成运动的物理合理性？这类似于强化学习中 sim-to-real 的思路，但需要解决生成模型与仿真器之间的可微分接口问题。



## 原文 PDF

![[paperPDFs/ICLR_2025/PedGen_Learning_to_Generate_Diverse_Pedestrian_Movements_from_Web_Videos_with_Noisy_Labels.pdf]]
