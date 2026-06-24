---
title: Learning Physics-Based Full-Body Human Reaching and Grasping from Brief Walking References
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Grasping_from_Brief_Walking_References.pdf
aliases:
- PRG
- LPBFBHRGFBWR
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用行走数据中可迁移的浅层局部运动特征（如肢体协调、动态平衡等）作为正则化约束：通过主动数据生成策略定向扩展困难任务的动作空间，同时在低层策略微调中加入浅层特征对齐奖励（基于马氏距离），将行走的自然运动模式传递至抓取动作，从而在极少量真实数据下实现高成功率和自然度。
primary_logic: 行走运动的浅层网络特征具有跨任务可迁移性：尽管整体语义差异巨大，浅层特征依然能在真实动作中形成聚类，其分布（如部分身体部位的运动模式）可作为强先验来正则化生成动作，有效减少人工痕迹、提升运动稳定性。
claims:
- 先导研究表明，浅层特征在真实运动数据（行走和伸手）之间FID较低且t-SNE呈现聚类，而深层特征这一现象消失，说明浅层捕捉了跨任务可迁移的真实运动特性。
- 特征对齐消融：在20%生成数据比例下，对齐浅层特征f0和f1使目标成功率从无对齐的69.1%提升至88.8%，同时用户偏好和判别器评分显著提高。
- 主动数据增强消融：结合成功率和判别器得分的主动策略（Active-Both）在20%数据比下实现69.1%目标成功率，显著优于随机策略（51.0%）及单一指标策略。
- 主实验对比：在简单场景中，所提方法达到99.8%抓取成功率和88.8%目标成功率，而简单全链路PPO基线（Fullbody PPO）的目标成功率仅为0.01%，说明仅靠强化学习无法完成任务，必须借助行走先验。
---

# Learning Physics-Based Full-Body Human Reaching and Grasping from Brief Walking References

> [!tip] 核心洞察
> 行走运动的浅层网络特征具有跨任务可迁移性：尽管整体语义差异巨大，浅层特征依然能在真实动作中形成聚类，其分布（如部分身体部位的运动模式）可作为强先验来正则化生成动作，有效减少人工痕迹、提升运动稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于物理的全身人类伸手抓取学习：从简短行走参考中学习 |
| 英文题名 | Learning Physics-Based Full-Body Human Reaching and Grasping from Brief Walking References |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://liyitang22.github.io/phys-reach-grasp/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Phys Reach Grasp |
| Dataset |  |

> [!tip] 效果简介
> - 简单场景 (Simple Scenes) 上，抓取成功率 SR(Grasp) 99.8% vs 96.6% (Fullbody PPO) (+3.2%)；目标成功率 SR(Goal) 88.8% vs 0.01% (Fullbody PPO) (+88.79%)。
> - 复杂场景 (Complex Scenes) 上，抓取成功率 SR(Grasp) 69.7% vs — (—)；目标成功率 SR(Goal) 55.8% vs — (—)。

## 概述

**问题瓶颈**：高质量全身交互运动捕捉数据的收集成本高昂、耗时长，导致可用数据稀缺且分布偏差大，严重限制了数据驱动方法在多样化场景和未知物体下的伸手抓取动作生成。同时，仅依赖运动学插值生成的抓取动作缺乏物理真实性和人类自然运动模式，无法满足物理仿真要求。

**核心洞察**：行走运动的浅层网络特征具有跨任务可迁移性。先导实验表明，尽管行走与伸手抓取的整体语义差异巨大，浅层特征依然能在真实运动数据中形成聚类（Table 1, Figure 3），其分布可作为强先验来正则化生成动作，有效减少人工痕迹、提升运动稳定性。

**方法定位**：本文提出 **Phys Reach Grasp**，一种仅需简短行走动作捕捉数据即可生成多样化、物理可行的全身伸手抓取运动的框架。该方法在对抗技能嵌入框架（**ASE**, Peng et al., TOG 2022）基础上，引入两个关键机制：（1）主动数据生成策略，定向扩展困难任务的动作空间；（2）浅层特征对齐奖励，将行走的自然运动模式传递至抓取动作。

**主要结果**：在简单场景下，Phys Reach Grasp 达到 99.8% 的抓取成功率和 88.8% 的目标成功率；相比之下，全链路 PPO 基线（Fullbody PPO）的目标成功率仅为 0.01%（Table 2）。在复杂场景下，抓取成功率和目标成功率分别达到 69.7% 和 55.8%。消融实验证实，特征对齐模块使目标成功率从 69.1% 提升至 88.8%，主动数据增强策略中结合成功率和判别器得分的方案显著优于随机策略（69.1% vs. 51.0%）。

## 背景与动机

高质量全身人-物交互动作捕捉数据的获取成本极高、制作周期漫长，导致可用数据不仅稀缺，还存在严重的分布偏差。这一瓶颈直接限制了数据驱动方法在多样化场景和未知物体条件下生成伸手抓取动作的能力。与此同时，单纯依赖运动学插值生成的抓取动作缺乏物理真实性，无法反映人类自然的运动模式，难以满足物理仿真对动态平衡、肢体协调等底层运动特性的要求。

现有工作大多沿两条路径展开：一类是基于对抗模仿学习的运动合成方法，如 **AMP**（Peng et al., TOG 2021）和 **ASE**（Peng et al., TOG 2022），它们能从运动捕捉数据中学习逼真的运动策略，但运动空间受限于训练数据的分布，难以泛化到未见过的任务；另一类方法如 **CALM**（Tessler et al., SIGGRAPH 2023）通过条件隐变量指导角色运动，但仍需要与目标任务相关的参考数据。当目标任务是全身伸手抓取、而可用的真实数据仅包含简短行走动作时，上述方法均面临运动空间覆盖不足与任务成功率低下的双重困境——实验表明，直接使用标准PPO训练的全链路策略（Fullbody PPO）在简单场景中的目标成功率仅为0.01%，几乎完全无法完成任务。

本文的核心动机在于回答一个根本性问题：**能否仅利用极易获取的简短行走动作捕捉数据，生成多样化、物理可行的全身伸手抓取运动？** 这一设想的可行性源自一个关键的先导发现：在对抗模仿学习框架中，运动批评家网络的浅层特征对真实运动数据（行走与伸手）表现出较低的FID值，且t-SNE投影呈现明显的聚类现象，而深层特征中这一跨任务的相似性消失。这表明，浅层网络捕捉了可迁移的局部运动特性——如肢体协调模式、动态平衡策略等——它们在不同任务间共享，可作为正则化生成动作的强先验。

基于这一洞察，本文提出 **Phys Reach Grasp** 框架，通过“主动数据生成”与“浅层特征对齐”两大机制，将行走数据中的自然运动模式迁移至伸手抓取任务，在极少量真实数据的条件下实现高成功率和运动自然度。

## 核心创新

**Phys Reach Grasp** 的核心创新在于打破高质量全身交互数据稀缺的瓶颈，仅利用*简短行走动作捕捉数据*即可生成多样化、物理可行的全身伸手抓取运动。其关键突破可从以下两个 changed slots 理解：

### 1. 训练数据与运动空间扩充：主动数据生成策略

传统低层策略训练仅依赖行走 MoCap 数据（M0），导致运动空间局限于行走动作，难以覆盖复杂的伸手抓取任务。Phys Reach Grasp 引入**主动数据生成策略**（Active Data Generation），针对性地扩展运动空间：

- **困难任务识别**：综合各任务的成功率 $sr_j$ 与判别器平均预测分数 $\overline{p_j}$，计算加权得分 $W_j$（见 Eq. 4），得分越低表示任务越困难——即策略既无法完成任务，生成的运动也不被判别器认可为“真实”。

$$W_j = s_0 + w_{succ} \frac{\max_i sr_i - sr_j}{\max_i sr_i - \min_i sr_i} + w_{disc} \frac{\max_i \overline{p_i} - \overline{p_j}}{\max_i \overline{p_i} - \min_i \overline{p_i}}$$

- **定向数据扩充**：针对困难任务，利用运动学姿势先验生成插值抓取动作数据，迭代扩充训练集，使低层策略的运动空间逐步覆盖多样化抓取场景。

消融实验（Table 4）证实了该策略的有效性：在 20% 生成数据比例下，结合成功率和判别器得分的 **Active-Both** 策略使目标成功率 SR(Goal) 达到 69.1%，显著优于随机策略（51.0%）及仅基于单一指标的策略。同时，增加生成数据比例（从 5% 到 20%）持续提升成功率，说明适量注入任务导向的生成数据对扩展运动空间是有效的。

### 2. 运动自然度约束与先验迁移：局部特征对齐

仅依赖运动学插值生成的抓取动作容易出现僵硬、不平衡等人工痕迹，缺乏人类运动的自然模式。Phys Reach Grasp 的核心洞察是：**行走运动的浅层网络特征具有跨任务可迁移性**。

先导实验（Table 1, Figure 3）为这一洞察提供了决定性证据：
- 浅层特征在真实运动数据（行走和伸手）之间的 FID 较低（如 f0 层 MoCap-Reach 与 MoCap-Walk 间 FID 仅为 2.3531），而深层特征这一现象消失。
- t-SNE 可视化显示，浅层特征在真实 MoCap 数据中形成明显聚类，深层则不再区分真实与生成数据。

基于此，方法在低层策略微调时加入**局部特征对齐奖励** $r^{feats}$：
- 提取批评家网络浅层特征 $f_i(s,z)$，计算其与行走特征分布的马氏距离 $d_{f_i}^{ma}$（Eq. 5）。
- 对超出阈值 $\mathrm{thres}_{f_i}$ 的特征距离进行加权惩罚（Eq. 6），强制生成动作的浅层特征分布与行走数据对齐。

$$d_{f_i}^{ma} = \sqrt{(f_i(s,z) - \mu_i)(\sigma_i + \epsilon \mathbb{I})^{-1}(f_i(s,z) - \mu_i)}$$

$$r^{feats} = -\sum_{f_i} w_{f_i} d_{f_i}^{ma} \mathbb{1}(d_{f_i}^{ma} > \mathrm{thres}_{f_i})$$

该机制将行走的局部运动模式（如肢体协调、动态平衡）作为强先验，正则化生成动作的自然度。消融实验（Table 5）表明：在 20% 生成数据比例下，对齐浅层特征 f0 和 f1 使 SR(Goal) 从无对齐的 69.1% 跃升至 **88.8%**，同时用户偏好和判别器评分显著提高。值得注意的是，仅对齐深层特征或对齐全部层特征会导致性能崩溃（如“f0,f1&f”行 SR(Goal) 降至 47.5%），证明正确的约束应局限在浅层。

### 创新总结

两个 changed slots 形成协同效应：主动数据生成策略扩展了低层策略可处理的任务空间，而局部特征对齐机制则确保扩展后的运动空间仍保持人类运动的自然模式。这一组合使得 Phys Reach Grasp 在简单场景中实现了 **99.8% 抓取成功率**和 **88.8% 目标成功率**，而简单全链路 PPO 基线（Fullbody PPO）的目标成功率仅为 0.01%（Table 2），凸显了仅靠强化学习无法完成任务，必须借助行走先验的关键结论。

## 整体框架

### 核心瓶颈与设计动机

高质量全身交互运动捕捉数据的收集成本高、耗时长，导致可用数据稀缺且分布偏差大，严重限制了数据驱动方法在多样场景和未知物体下的伸手抓取动作生成。同时，仅依赖运动学插值或纯强化学习（如 **Fullbody PPO**，目标成功率仅 0.01%）生成的抓取动作缺乏物理真实性和人类自然运动模式，无法满足物理仿真要求。本工作提出 **Phys Reach Grasp** 框架，核心洞察在于：**行走运动的浅层网络特征具有跨任务可迁移性**——尽管整体语义差异巨大，浅层特征依然能在真实动作中形成聚类（Table 1, Figure 3），其分布可作为强先验来正则化生成动作，有效减少人工痕迹、提升运动稳定性。

### 多轮迭代训练管线

框架采用多轮迭代训练流程（Figure 4），每轮迭代包含四个核心模块，逐步扩展运动空间并提升抓取动作的自然度：

![[assets/figures/papers/paper_list_l1744_Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Gra/figures/005_Figure_4.jpg]]
*Figure 4: Overview of our framework: We propose a pipeline that generates diverse reaching and grasping motions using brief walk MoCap data through the multi-iteration training. In each iteration, with the imitation and discovery objective specified respectively by the discriminator and encoder, we first train a low-level policy*

1. **低层策略训练（Low-level Policy Training）**  
   使用对抗模仿和技能发现目标训练策略 $\pi(a|s,z)$，将隐变量 $z$ 映射为物理仿真动作。训练奖励为：
   $$r_t = -\log(1 - D(s_t, s_{t+1})) + \beta \log q(z | s_t, s_{t+1})$$
   其中判别器 $D$ 提供对抗模仿目标，编码器 $q$ 提供技能发现目标，$\beta$ 为平衡系数。该模块构建了从行走数据中学习的技能空间。

2. **高层策略训练（High-level Policy Training）**  
   在低层策略基础上选择隐变量 $z$，完成分阶段伸手抓取任务（方向行走、预抓取、抓取、后抓取四个阶段）。结合任务奖励和两个运动先验奖励引导技能选择：
   $$r_{p_1} = -\log(1 - D(s_t, s_{t+1}))$$
   $$r_{p_2} = -\log(1 - D'(s_t, s_{t+1}))$$
   $r_{p_1}$ 防止技能切换过于频繁，$r_{p_2}$ 通过额外训练的判别器 $D'$ 引导采样偏向连续行走区域。

3. **主动数据生成（Active Data Generation）**  
   首轮迭代后，运动空间仅包含有限的行走动作，限制了困难抓取任务的表现。本模块根据各任务的成功率 $sr_j$ 和平均判别器预测分数 $\bar{p}_j$，计算综合难度得分：
   $$W_j = s_0 + w_{succ} \frac{\max_i sr_i - sr_j}{\max_i sr_i - \min_i sr_i} + w_{disc} \frac{\max_i \overline{p_i} - \overline{p_j}}{\max_i \overline{p_i} - \min_i \overline{p_i}}$$
   识别困难任务后，利用运动学姿势先验生成插值抓取动作数据，有针对性地扩充训练集，定向扩展运动空间。

4. **局部特征对齐（Local Feature Alignment）**  
   在后续迭代的低层策略微调中，提取浅层特征 $f_i(s,z)$，计算其与行走特征分布的马氏距离：
   $$d_{f_i}^{ma} = \sqrt{(f_i(s,z) - \mu_i)(\sigma_i + \epsilon \mathbb{I})^{-1}(f_i(s,z) - \mu_i)}$$
   对超出阈值 $\mathrm{thres}_{f_i}$ 的特征距离进行加权惩罚，形成特征对齐奖励：
   $$r^{feats} = -\sum_{f_i} w_{f_i} d_{f_i}^{ma} \mathbb{1}(d_{f_i}^{ma} > \mathrm{thres}_{f_i})$$
   该机制将行走的局部运动模式（如肢体协调、动态平衡）迁移至抓取动作，同时保留特征变化多样性。

### 输入输出流与模块关系

- **输入**：简短行走动作捕捉数据（MoCap）作为唯一真实运动先验。
- **数据流**：行走数据 → 低层策略训练（构建初始技能空间）→ 高层策略训练（执行抓取任务）→ 主动数据生成（识别困难任务并扩充数据集）→ 低层策略微调 + 局部特征对齐（扩展运动空间并正则化自然度）→ 下一轮高层策略训练。此迭代过程持续至性能收敛。
- **输出**：多样化、物理可行的全身伸手抓取运动，在简单场景中达到 99.8% 抓取成功率和 88.8% 目标成功率，在复杂场景中达到 69.7% 抓取成功率和 55.8% 目标成功率（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l1744_Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Gra/figures/001_Figure_1.jpg]]
*Figure 1: In this work, we design a framework that generates diverse, physically feasible full-body human reaching and grasping motions using only brief walking MoCap data*

## 核心模块与公式推导

Phys Reach Grasp 框架围绕四个核心模块构建，形成一个多轮迭代的训练流水线（Figure 4）。以下逐一展开各模块的关键设计与公式。

### 低层策略训练：技能空间构建

低层策略 $\pi(\mathbf{a}|\mathbf{s},\mathbf{z})$ 的目标是将隐变量 $\mathbf{z}$ 映射为物理仿真中的具体动作，同时构建一个结构化的技能空间。训练采用两个互补的目标函数：

- **对抗模仿目标**：由判别器 $D(\mathbf{s}_t, \mathbf{s}_{t+1})$ 提供，迫使策略生成的动作序列在分布上逼近真实运动捕捉数据。
- **技能发现目标**：由编码器 $q(\mathbf{z}|\mathbf{s}_t, \mathbf{s}_{t+1})$ 提供，鼓励不同隐变量 $\mathbf{z}$ 产生可区分的运动模式，从而形成多样化的技能空间。

两个目标统一为以下奖励函数：

$$r_t = -\log(1 - D(\mathbf{s}_t, \mathbf{s}_{t+1})) + \beta \log q(\mathbf{z} | \mathbf{s}_t, \mathbf{s}_{t+1})$$

其中 $\beta$ 为平衡系数，控制技能发现目标相对于对抗模仿目标的权重。该奖励函数是低层策略训练的核心驱动力，使策略既能模仿真实运动，又能探索结构化的技能表示。

### 高层策略训练：分阶段任务引导

在低层策略构建的技能空间之上，高层策略 $\pi_H(\mathbf{z}|\mathbf{s})$ 负责选择适当的隐变量 $\mathbf{z}$，以完成伸手抓取任务。任务被划分为四个阶段：方向与行走、预抓取、抓取、后抓取，每个阶段有特定的任务奖励 $r_G$。

为防止高层策略频繁切换技能导致运动不连贯，引入两个运动先验奖励：

$$r_{p_1} = -\log(1 - D(\mathbf{s}_t, \mathbf{s}_{t+1}))$$

$$r_{p_2} = -\log(1 - D'(\mathbf{s}_t, \mathbf{s}_{t+1}))$$

$r_{p_1}$ 直接复用低层训练的判别器 $D$，惩罚与真实运动分布偏离过大的状态转移。$r_{p_2}$ 则使用一个额外训练的判别器 $D'$，专门引导高层策略在连续行走区域内采样技能，确保从行走到抓取的运动过渡自然流畅。

### 主动数据生成：定向扩展运动空间

首轮训练后，低层策略的运动空间仅覆盖行走动作，难以处理复杂的伸手抓取任务。主动数据生成模块针对这一瓶颈，通过评估各任务难度来定向扩充训练集。

任务 $j$ 的难度综合得分定义为：

$$W_j = s_0 + w_{succ} \frac{\max_i sr_i - sr_j}{\max_i sr_i - \min_i sr_i} + w_{disc} \frac{\max_i \overline{p_i} - \overline{p_j}}{\max_i \overline{p_i} - \min_i \overline{p_i}}$$

其中 $sr_j$ 为任务 $j$ 的成功率，$\overline{p_j}$ 为判别器对该任务生成动作的平均预测分数，$w_{succ}$ 和 $w_{disc}$ 为权重系数，$s_0$ 为基础分数。得分越高的任务被视为越困难——成功率低且判别器评分低意味着该任务既难以完成，生成动作又与真实运动分布偏差大。针对这些困难任务，模块利用运动学姿势先验生成插值抓取动作数据，迭代地扩充训练集，使运动空间逐步覆盖多样化的抓取场景。

### 局部特征对齐：行走先验迁移

先导实验（Table 1, Figure 3）揭示了一个关键洞察：运动批评家网络的浅层特征在真实运动数据（行走与伸手）之间呈现低FID值和t-SNE聚类，而深层特征这一现象消失。这表明浅层特征捕捉了跨任务可迁移的真实运动特性（如肢体协调、动态平衡等局部运动模式）。

![[assets/figures/papers/paper_list_l1744_Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Gra/figures/004_Figure_3.jpg]]
*Figure 3: t-SNE plots of features extracted at different levels of the critic network: There is clear clustering within the MoCap data in shallow layers and this phenomenon is less evident in deeper layers*

基于此，局部特征对齐模块在低层策略微调时，强制生成动作的浅层特征分布与行走数据的特征分布对齐。对于第 $i$ 个浅层特征 $f_i(\mathbf{s},\mathbf{z})$，计算其相对于行走特征分布的马氏距离：

$$d_{f_i}^{ma} = \sqrt{(f_i(\mathbf{s},\mathbf{z}) - \mu_i)(\sigma_i + \epsilon \mathbb{I})^{-1}(f_i(\mathbf{s},\mathbf{z}) - \mu_i)}$$

其中 $\mu_i$ 和 $\sigma_i$ 分别为行走数据特征的均值和协方差矩阵，$\epsilon$ 为防止零特征值的小常数。为避免过度约束导致运动多样性丧失，仅对超出阈值 $\mathrm{thres}_{f_i}$ 的特征距离施加惩罚：

$$r^{feats} = -\sum_{f_i} w_{f_i} d_{f_i}^{ma} \mathbb{1}(d_{f_i}^{ma} > \mathrm{thres}_{f_i})$$

该奖励函数的设计兼顾了两方面需求：一方面通过马氏距离惩罚将异常运动拉回自然分布，另一方面通过阈值机制保留特征变化的合理空间，避免生成动作千篇一律。特征提取器同时接收运动状态和隐变量 $\mathbf{z}$ 作为输入，确保对齐约束与技能选择相关联。

### 补充图表

![[assets/figures/papers/paper_list_l1744_Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Gra/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of our modified critic architecture*

## 实验与分析

### 核心瓶颈与因果机制

本研究试图解决的核心瓶颈在于：高质量全身交互运动捕捉数据获取成本极高，而仅依赖运动学插值生成的抓取动作缺乏物理真实性与人类自然运动模式。论文提出的因果机制是，利用行走数据中可迁移的浅层局部运动特征（如肢体协调、动态平衡）作为正则化约束，通过主动数据生成策略扩展动作空间，并在低层策略微调中施加浅层特征对齐奖励，将行走的自然运动模式传递至抓取动作。

先导实验为此提供了关键证据。Table 1 显示，在浅层（f0），真实行走与真实伸手数据之间的 FID（2.3531）远低于真实伸手与生成伸手之间的 FID（2.4671），且接近真实伸手训练集与测试集之间的参考 FID（0.1750）。随着网络加深，这一差距急剧扩大，表明深层特征已丧失跨任务的通用性。Figure 3 的 t-SNE 可视化进一步印证：浅层特征在真实运动捕捉数据中形成明显聚类，而深层特征中该现象消失。这确立了浅层特征作为可迁移运动先验的理论基础。

![[assets/figures/papers/paper_list_l1744_Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Gra/figures/003_Table_1.jpg]]
*Table 1: Quantitative Results of Pilot Study: In the shallower layers, the FID difference between the MoCap data is relatively small, compared to that between the MoCap and generated datasets. As feature extraction moves to deeper layers, the FID value increases significantly compared to the reference FID between training and test datasets*

### 主实验结果

Table 2 汇总了各方法在简单场景与复杂场景下的性能对比。所提方法 Phys Reach Grasp（f0 & f1 对齐，数据比例 20%）在简单场景中达到 99.8% 的抓取成功率 SR(Grasp) 和 88.8% 的目标成功率 SR(Goal)。相比之下，全链路 PPO 基线（Fullbody PPO）的 SR(Goal) 仅为 0.01%，说明仅靠强化学习无法完成该任务，必须借助行走先验。在复杂场景中，所提方法的 SR(Grasp) 为 69.7%，SR(Goal) 为 55.8%，虽有所下降，但仍显著优于各基线方法。

![[assets/figures/papers/paper_list_l1744_Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Gra/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of overall task performance: We compare success rate and user preference. Our method(with f0&f1 aligned, data ratio 20%) achieves the highest success rate while remaining significantly more naturalness among all baselines*

用户研究（100 名志愿者随机盲评）和自动评估（GPT-4o/Kimi 统一提示词评分）进一步验证了运动自然度。Table 2 中，所提方法的用户偏好得分 FS(±1%) 为 12.0%，GPT-4o/Kimi 评分分别为 7.38/7.25，在所有方法中表现最优。Figure 5 的可视化对比显示，基线方法（如 Fullbody PPO、AMP*）在抓取过程中出现显著的非自然运动，而所提方法能生成流畅自然的全身协调动作。

![[assets/figures/papers/paper_list_l1744_Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Gra/figures/008_Figure_5.jpg]]
*Figure 5: Visualization of the overall task compared to baselines: We visualized our method and baselines. Our methods can yield nature reaching and grasping in various scenes and tasks while baselines show significant unnatural movements*

### 消融实验

#### 主动数据增强策略

Table 4 对比了四种数据增强策略在不同生成数据比例下的表现。结合成功率和判别器得分的 Active-Both 策略在 20% 数据比例下达到 69.1% 的 SR(Goal)，显著优于随机策略 Random（51.0%）、仅基于成功率的 Active-S（57.5%）和仅基于判别器得分的 Active-D（59.3%）。增加生成数据比例（从 5% 到 20%）持续提高成功率，验证了适量注入任务导向生成数据对扩展运动空间的有效性。该策略通过公式 $W_j = s_0 + w_{succ} \frac{\max_i sr_i - sr_j}{\max_i sr_i - \min_i sr_i} + w_{disc} \frac{\max_i \overline{p_i} - \overline{p_j}}{\max_i \overline{p_i} - \min_i \overline{p_i}}$ 综合评估各任务难度，定向扩充困难任务的动作空间。

![[assets/figures/papers/paper_list_l1744_Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Gra/figures/010_Table_4.jpg]]
*Table 4: We found that*

#### 浅层特征对齐

Table 5 的消融结果揭示了特征对齐的关键作用。在 20% 生成数据比例下，对齐 f0 和 f1 浅层特征使 SR(Goal) 从无对齐的 69.1% 跃升至 88.8%，同时用户偏好和判别器评分明显提高。然而，对齐深层特征或对齐全部层特征会导致性能崩溃——“fo, fi & f”行 SR(Goal) 骤降至 47.5%。这证实了正确的约束应严格局限在浅层，深层特征包含过多任务特定信息，强行对齐反而破坏策略学习。

![[assets/figures/papers/paper_list_l1744_Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Gra/figures/011_Table_5.jpg]]
*Table 5: Quantitative results of the feature alignment ablation: The mechanism improves success rate and reduces artifacts*

特征对齐通过马氏距离奖励实现：$d_{f_i}^{ma} = \sqrt{(f_i(s,z) - \mu_i)(\sigma_i + \epsilon \mathbb{I})^{-1}(f_i(s,z) - \mu_i)}$，仅对超出阈值 $\mathrm{thres}_{f_i}$ 的距离施加惩罚 $r^{feats} = -\sum_{f_i} w_{f_i} d_{f_i}^{ma} \mathbb{1}(d_{f_i}^{ma} > \mathrm{thres}_{f_i})$，在正则化运动自然度的同时保留特征变化多样性。Figure 6 的可视化展示了对齐躯干和左上肢特征对抓取姿态的改善效果。

### 与 SOTA 对比

Table 3 展示了与同期工作的自然度对比结果。所提方法在运动自然度指标上表现优异，进一步验证了浅层特征对齐机制在减少人工痕迹、提升运动稳定性方面的有效性。与 **ASE**（Peng et al., TOG 2022）、**AMP**（Peng et al., TOG 2021）、**CALM**（Tessler et al., SIGGRAPH 2023）等基于对抗模仿学习的框架相比，所提方法的创新在于主动数据生成与跨任务浅层特征迁移的协同设计。

![[assets/figures/papers/paper_list_l1744_Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Gra/figures/007_Table_3.jpg]]
*Table 3: Results of comparison with concurrent SOTAs*

### 失败模式与局限

尽管实验结果整体积极，但仍存在若干失败模式与局限：

1. **复杂场景性能下降**：从简单场景到复杂场景，SR(Goal) 从 88.8% 下降至 55.8%，表明当前方法在更复杂的多步骤交互任务中性能受限。仅使用行走数据作为真实先验，未融合更丰富的全身交互数据，可能是性能瓶颈之一。

2. **动作多样性受限**：浅层特征对齐依赖预先提取的行走特征分布，可能限制生成动作的多样性，难以覆盖与行走差异极大的动作风格。Table 5 中仅对齐深层特征导致的性能崩溃也暗示，当前特征提取网络结构较为简单，可能无法充分捕捉复杂的时空运动模式。

3. **仿真到现实的迁移未知**：目前所有实验仅在仿真环境中验证，未在真实人形机器人上进行测试。sim-to-real 迁移能力、特征实时对齐的可行性等关键问题尚待探索。

4. **公平性说明**：所有方法均在同一物理仿真环境、相同人形模型和 PPO 训练框架下评估。消融实验中控制训练轮次和其他超参数保持一致，仅改变所研究的模块。用户研究采用随机化盲评方式，自动评估指标使用统一的提示词和评分标准。

## 方法谱系与知识库定位

### 1. 方法谱系：从运动模仿到跨任务先验迁移

Phys Reach Grasp 的核心技术路径建立在物理角色动画与技能发现两大研究脉络的交汇点上，其演进逻辑可归纳为“模仿→发现→迁移”的三阶段范式。

**第一阶段：对抗运动模仿。** 本工作的底层策略训练直接继承了 **AMP**（Adversarial Motion Priors, Peng et al., TOG 2021）的对抗模仿框架——通过判别器 $D(s_t, s_{t+1})$ 区分策略生成的运动与参考运动捕捉数据，以 $- \log(1 - D(s_t, s_{t+1}))$ 作为模仿奖励。这一机制使物理仿真角色能够复现给定数据集中的运动模式，但 AMP 本身不具备跨任务迁移能力：当参考数据仅包含行走动作时，策略的运动空间被严格限制在行走分布内，无法自主生成伸手抓取等目标导向行为。本工作中的 **AMP\*** 基线即在此框架下注入与所提方法等量的生成数据，以验证单纯增加数据量无法替代结构化先验迁移。

**第二阶段：技能发现与条件控制。** 为赋予策略在单一数据集中挖掘多样化运动模式的能力，**ASE**（Adversarial Skill Embeddings, Peng et al., TOG 2022）在 AMP 基础上引入隐变量 $z$ 和编码器 $q(z|s_t, s_{t+1})$，通过互信息最大化目标 $\beta \log q(z | s_t, s_{t+1})$ 构建结构化的技能空间。Phys Reach Grasp 的低层策略训练（Section 4.1）完整沿用了 ASE 的双目标框架（Eq. 1），并在此基础上训练高层策略 $\pi_H(z|s)$ 在技能空间中采样以完成分阶段抓取任务。**PSE** 基线则进一步在 ASE 中引入部位判别器（Part-wise Skill Embedding），试图通过分部位建模提升运动质量。**CALM**（Tessler et al., SIGGRAPH 2023）作为同期条件运动生成方法，采用条件对抗隐模型指导角色运动，但在本文的对比中（Table 3），其生成动作的自然度显著低于所提方法，说明条件生成机制本身不足以弥合行走与抓取之间的运动分布鸿沟。

**第三阶段：跨任务浅层特征迁移（本工作核心贡献）。** 上述方法均未解决一个根本瓶颈：当真实运动捕捉数据仅覆盖行走动作时，如何生成物理可行且自然的全身抓取运动？Phys Reach Grasp 的关键突破在于通过先导实验（Table 1, Figure 3）发现：运动批评家网络的浅层特征在真实行走和真实伸手数据之间呈现低 FID 和 t-SNE 聚类，而深层特征则丧失这一跨任务一致性。这一洞察催生了两个互补机制：（1）**主动数据生成**（Section 4.3）——利用插值姿态先验定向扩充困难任务的动作空间；（2）**浅层特征对齐**（Section 4.4）——以马氏距离度量生成动作与行走特征分布的偏差，并通过 $r^{\text{feats}}$ 惩罚超出阈值的特征维度。消融实验（Table 5）表明，仅对齐浅层特征 $f_0$ 和 $f_1$ 即可将目标成功率从 69.1% 提升至 88.8%，而对齐深层或全部层特征则导致性能崩溃（47.5%），验证了“浅层正则化”这一设计选择的正确性。

### 2. 与基线方法的系统性对比

| 方法 | 运动先验来源 | 技能发现 | 跨任务迁移 | 抓取成功率 (简单场景) | 目标成功率 (简单场景) |
|------|-------------|---------|-----------|---------------------|---------------------|
| **Fullbody PPO** | 无 | 无 | 无 | 96.6% | 0.01% |
| **AMP\*** | 行走+生成数据 | 无 | 隐式 | — | — |
| **ASE** | 行走 | 有 | 无 | — | — |
| **PSE** | 行走 | 有（部位级） | 无 | — | — |
| **CALM** | 条件对抗 | 隐式 | 条件控制 | — | — |
| **Oracle Grasp Policy** | 抓取专家数据 (UnidexGrasp, Xu et al., CVPR 2023) | 无 | 无 | — | — |
| **Phys Reach Grasp** | 行走+主动生成数据 | 有 | 浅层特征对齐 | **99.8%** | **88.8%** |

**Fullbody PPO** 的极端失败（目标成功率 0.01%）揭示了纯强化学习在稀疏奖励全身抓取任务中的根本困境：没有运动先验的端到端探索几乎不可能发现从行走到精准抓取的协调运动序列。**Oracle Grasp Policy** 依赖 UnidexGrasp 提供的非目标条件抓取专家策略，虽能完成抓取动作本身，但缺乏全身协调和任务导向的目标达成能力。Phys Reach Grasp 在仅使用行走数据的前提下，超越了所有需要额外抓取数据或仅依赖运动学插值的基线，证明了“行走先验+主动扩展+浅层对齐”这一技术路线的有效性。

### 3. 适用边界与局限

**数据依赖性边界。** 本方法的核心假设是行走数据中蕴含的局部运动模式（如肢体协调、动态平衡、步态节奏）具有跨任务可迁移性。这一假设在伸手抓取场景中得到验证，但其适用性受限于目标动作与行走在运动学结构上的重叠程度。当目标动作与行走差异极大（如匍匐前进、倒立、翻滚）时，浅层特征分布可能不再重叠，对齐机制将失效。论文明确指出“仅使用了行走动作数据作为真实先验，未融合更丰富的全身交互数据”，这构成了当前方法的能力上限。

**运动多样性约束。** 浅层特征对齐以马氏距离阈值 $\text{thres}_{f_i}$ 作为正则化边界（Eq. 6），其设计初衷是“在惩罚异常偏差的同时保留特征变化多样性”。然而，这种基于固定行走分布的对齐本质上是一种收缩正则化，可能抑制策略探索出与行走模式差异显著但物理可行的抓取策略。消融实验虽未直接量化多样性损失，但“对齐全部层特征导致性能崩溃”的现象暗示，过强的正则化会扼杀任务所需的运动可变性。

**仿真到现实的鸿沟。** 所有实验均在物理仿真环境中完成，未在真实人形机器人平台上验证。仿真中的动力学参数、接触建模和传感器延迟均与真实世界存在偏差，浅层特征对齐所依赖的马氏距离分布能否在真实机器人传感器数据中保持有效性，仍是一个开放问题。

### 4. 未解决的问题与未来方向

1. **可迁移运动模式的选择机制。** 当前方法将浅层特征 $f_0$ 和 $f_1$ 的对齐作为固定设计，但不同任务可能受益于不同层次或不同身体部位的特征对齐。先导实验的 t-SNE 可视化（Figure 3）揭示了部位级别的聚类模式差异，但尚未发展出自动选择最具可迁移性特征子集的机制。一个潜在方向是引入注意力机制或元学习策略，使策略根据目标任务动态调整对齐权重。

2. **时空特征提取的增强。** 当前特征提取网络结构较为简单，可能无法充分捕捉复杂的时空运动模式。论文在开放问题中明确提及“采用图神经网络（如 ST-GCN）提取时空特征能否获得更鲁棒的运动先验”。基于骨骼图的时空建模有望更精确地表征肢体间的协调关系，从而提升浅层特征对齐的精度和泛化能力。

3. **跨任务泛化能力验证。** 本方法在伸手抓取任务上得到验证，但其技术路线——从行走数据中提取可迁移运动先验——理论上可泛化至其他需要全身协调的人-物交互任务，如搬运、开门、坐下等。这些任务与行走的运动学重叠程度各异，系统性验证将有助于刻画该方法的真实适用边界。

4. **Sim-to-Real 迁移与实时对齐。** 在真实人形机器人上部署时，需要解决仿真动力学偏差、传感器噪声和实时性约束。浅层特征对齐的马氏距离计算（Eq. 5）需要预先提取行走特征的均值 $\mu_i$ 和协方差 $\sigma_i$，真实场景中这些统计量可能因机器人硬件差异而偏移，需要发展在线自适应或域随机化策略来弥合这一差距。

## 原文 PDF

![[paperPDFs/CVPR_2025/Phys_Reach_Grasp_Learning_Physics_Based_Full_Body_Human_Reaching_and_Grasping_from_Brief_Walking_References.pdf]]
