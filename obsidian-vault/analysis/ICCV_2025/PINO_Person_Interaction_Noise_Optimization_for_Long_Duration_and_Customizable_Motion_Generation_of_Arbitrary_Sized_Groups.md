---
title: PINO Person Interaction Noise Optimization for Long Duration and Customizable Motion Generation of Arbitrary Sized Groups
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/PINO_Person_Interaction_Noise_Optimization_for_Long_Duration_and_Customizable_Motion_Generation_of_Arbitrary_Sized_Groups.pdf
project_link: https://sinc865.github.io/pino/
code_link: null
aliases:
- PINOP
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将群组交互分解为语义相关的成对交互，并通过噪声优化引入物理惩罚（如重叠避免、时空控制），从而支持任意规模和多样化控制生成。
primary_logic: 群组交互由较小的、相互连接的成对交互组成，其中角色通过共享人物作为枢纽连接多个交互。
claims:
- PINO 将复杂群组交互分解为语义相关的成对交互，并增量组合生成任意规模群体运动。
- 通过噪声优化引入物理惩罚，显著减少重叠和穿透，同时保持语义保真度。
- 用户可通过时空惩罚灵活控制角色方向、速度和空间关系，无需重新训练。
- Two-person interaction (InterHuman test set) 上 Overlap = 0.000 (PINO-InterGen)
---

# PINO Person Interaction Noise Optimization for Long Duration and Customizable Motion Generation of Arbitrary Sized Groups

> [!tip] 核心洞察
> 群组交互由较小的、相互连接的成对交互组成，其中角色通过共享人物作为枢纽连接多个交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | PINO：面向任意规模群体的长时程可定制运动生成的人员交互噪声优化 |
| 英文题名 | PINO Person Interaction Noise Optimization for Long Duration and Customizable Motion Generation of Arbitrary Sized Groups |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://sinc865.github.io/pino/) · [paper](https://arxiv.org/abs/2507.19292) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Person-Interaction Noise Optimization (PINO) |
| Dataset | Two-person interaction, Multi-person interaction (incremental pair (1,5)) |

> [!tip] 效果简介
> - Two-person interaction (InterHuman test set) 上，Overlap 0.000 (PINO-InterGen) vs 0.119 (InterGen) (-0.119)；Penetration Volume (cm^3) 275.65 (PINO-InterGen) vs 3112.72 (InterGen) (-2837.07)。
> - Multi-person interaction (incremental pair (1,5)) 上，Overlap 0.069 (PINO-InterGen) vs 0.977 (InterGen) (-0.908)。
> - Multi-person interaction (incremental pair (1,2)) 上，FID 12.920 (PINO-InterGen) vs 13.100 (InterGen) (-0.180)。

## 概要

### 问题瓶颈

随着群体规模扩大，现有多人交互运动生成方法面临两个核心瓶颈。其一，方法通常使用单一共享文本提示描述整个群体，难以刻画复杂、异构的交互语义。其二，生成过程缺乏显式物理约束，导致角色间出现重叠、穿透以及运动不自然等伪影。这些瓶颈使得现有方法在面向任意规模群体的长时程、可定制运动生成任务上表现受限。

### 核心方法

PINO（Person-Interaction Noise Optimization）提出了一种无需额外训练的后处理优化框架。其核心洞察在于：复杂群组交互可分解为若干语义相关的成对交互，角色之间通过共享“枢纽人物”连接多个交互关系。方法以预训练的双人交互扩散模型（InterGen）为运动先验，将群组生成转化为顺序的成对交互组合过程——每步选择一个已生成角色作为条件，生成新角色并赋予独立的语义提示。在此基础上，PINO通过对扩散模型的初始噪声进行可微优化，引入物理惩罚项（如重叠避免、根节点位置约束、朝向约束、运动区域限制），在保持语义保真度的同时强制空间一致性。此外，方法支持运动扩展，通过运动修复实现长时程生成。

### 方法定位

在多人运动生成的方法谱系中，PINO占据独特位置。与需要专门多人数据集进行监督训练的方法（如Shan等人的并发工作）不同，PINO直接复用预训练双人模型，无需额外训练。与基于ControlNet的序列生成方法（如FreeMotion）或单人生成方法（如InterControl）相比，PINO通过噪声优化引入了可微的物理约束，避免了生成过程中的误差累积和运动不自然问题。Table 1系统对比了近期多人交互生成方法在群体规模、提示类型、物理约束和用户控制等维度的差异，PINO是唯一同时支持任意规模群体、成对语义提示、显式物理约束和多样化用户控制的方法。

### 主要结果

在双人交互基准上，PINO-InterGen将重叠指标从InterGen的0.119降至0.000，穿透体积从3112.72 cm³降至275.65 cm³，同时保持竞争性的FID和语义指标（Table 2）。在多人交互场景中，PINO在增量生成和整体群组评估中均显著优于InterGen inpainting等基线，三人群体重叠从0.766降至0.000（Table 3）。消融实验证实，全部四种惩罚项的组合达到最低违规率（Table 5），且基于优化的方法相比inpainting方法产生更自然的运动加速度（Table B）。用户研究进一步表明，PINO在文本忠实度和交互质量上均获得一致更高的评分和偏好投票（Figure B）。

### 局限与开放问题

当前方法的主要局限在于推理效率——每生成一个角色约需1分钟（仅重叠惩罚）至10分钟（全惩罚），难以满足实时应用需求。此外，手部关节数据的缺失导致手部穿透问题尚未完全解决，双人模型基座可能无法捕捉超过两人的高阶交互依赖。开放问题包括：如何加速噪声优化过程、能否扩展基础模型直接支持三人以上交互、如何自动生成合理的成对交互图以减少用户手动设计负担，以及现有评估指标是否充分反映群组交互的自然性和语义一致性。

### 多人交互运动生成的核心瓶颈

生成逼真的多人交互运动是计算机视觉与图形学中的基础难题。随着群体规模扩大，现有方法面临两个相互交织的瓶颈：**语义描述能力不足**与**物理约束缺失**。

在语义层面，当前多人交互生成方法通常使用单一共享文本提示来描述整个群体的行为。这种方式在两人场景下尚可工作，但当群体扩展至三人或以上时，单一提示难以刻画复杂的交互结构——例如“两个人握手，第三个人在一旁拍照”这样的场景，需要同时描述握手和拍照两个语义不同的子交互。**InterGen**等预训练双人扩散模型虽然在两人交互生成上表现出色，但缺乏直接扩展到任意规模群体的机制。

在物理层面，现有方法在生成过程中没有显式的物理约束，导致生成的角色之间频繁出现**重叠**（角色占据同一空间）和**穿透**（身体部位相互穿插）。定量评估显示，InterGen在两人交互测试集上的重叠指标高达0.119，穿透体积达到3112.72 cm³（Table 2(a)），这些伪影严重破坏了运动的物理可信度。

### 现有方法的局限

表1（Table 1）系统比较了近期多人交互生成方法的能力边界。**FreeMotion**采用基于ControlNet的序列化生成策略，但缺乏对角色间空间关系的显式建模。**InterControl**将单人ControlNet扩展至多人场景，同样面临物理一致性不足的问题。**Shan et al.**尝试通过监督训练实现并发多人生成，但依赖专门的多人数据集，泛化能力受限。这些方法的共同缺陷在于：要么将群体交互视为不可分解的整体，要么简单地进行序列化拼接，都未能有效利用双人交互先验来构建群体运动。

### 核心洞察与方法动机

PINO的核心洞察在于：**复杂的群组交互本质上由较小的、语义相关的成对交互组成，其中角色通过共享人物作为枢纽连接多个交互**。例如，三人合影场景可以分解为“两人摆姿势”和“第三人拍照”两个成对交互，其中被拍摄的两人之一作为枢纽角色连接两个交互。

基于这一洞察，PINO提出了一种无需额外训练的范式：将预训练双人扩散模型作为运动先验，通过**交互分解**将群体生成转化为序列化成对生成问题，并通过**噪声优化**引入物理惩罚来强制执行空间一致性和用户指定的控制约束。这种设计使得方法能够（1）支持任意规模群体的生成，（2）为每对交互提供独立的语义提示，（3）通过可微损失函数实现灵活的用户控制，而无需重新训练基础模型。

## 核心方法与创新机理

PINO 的核心创新在于将复杂的多人交互生成问题**重新定义为一系列语义相关的成对交互的组合优化问题**，而非试图用单一模型直接生成整个群体的运动。这一思路源于一个关键的因果洞察：现实中的群组交互本质上由较小的、相互连接的成对交互构成，其中角色通过共享的“枢纽人物”连接多个交互关系。

基于此，PINO 在三个关键维度上对现有范式进行了根本性改造：

**1. 交互分解与语义提示切换（Interaction decomposition）**

现有方法（如 InterGen）为整个群体使用单一共享文本提示，难以描述复杂的差异化交互。PINO 将群组交互分解为语义相关的成对交互，每对交互由专属的文本提示引导。当增量添加新角色时，系统自动切换提示词以描述新加入的交互关系，使每个角色都能获得与其行为匹配的语义指导。

**2. 物理约束的后验注入（Physical constraint enforcement）**

现有方法在生成过程中缺乏显式物理约束，导致角色重叠、穿透和运动不自然。PINO 通过**噪声优化（noise optimization）**机制，在扩散模型的初始噪声空间引入可微分的物理惩罚函数（如重叠避免损失、时空控制损失），通过反向传播优化噪声向量，从而在保持语义保真度的前提下显著减少物理违规。关键的是，这一过程无需重新训练基础模型。

**3. 免训练的灵活用户控制（User control mechanism）**

现有方法对单个角色的空间属性（位置、朝向、速度）控制能力有限。PINO 在噪声优化框架下引入一系列可微分的控制损失函数，包括根节点位置惩罚、运动区域约束、朝向惩罚和相对位置惩罚，使用户能够在生成后灵活指定角色的空间行为，而无需任何额外训练。

这三个创新点形成了协同效应：交互分解使语义控制成为可能，噪声优化为物理约束和用户控制提供了统一的注入接口，而免训练的特性使方法可即插即用地应用于不同的预训练双人扩散模型。

PINO 的整体框架围绕一个核心思想展开：**将复杂群组交互分解为一系列语义相关的成对交互**，并利用预训练的双人交互扩散模型作为运动先验，通过**噪声优化**逐步组合生成任意规模群体的运动。整个 pipeline 由四个关键模块串联而成，形成“生成—优化—组合—扩展”的闭环。

### Pipeline 总览

**输入**：用户指定群体规模 $M$、成对交互图（每对包含一个枢纽人物 $k_p$ 和一个新加入人物 $p$）、每对交互的文本提示 $c_{k_p,p}$，以及可选的控制约束（如目标位置、朝向、移动区域等）。

**输出**：$M$ 个角色的长时程运动序列 $\hat{\mathbf{x}}_0^1, \hat{\mathbf{x}}_0^2, \ldots, \hat{\mathbf{x}}_0^M$，满足物理合理性（低重叠、低穿透）和用户控制要求。

**核心流程**（对应 Algorithm 1 与 Figure 2）：

1. **初始双人交互生成**：使用预训练的 InterGen 双人扩散模型 $G_{\boldsymbol{\theta}}$，从随机噪声 $\mathbf{x}_T^1, \mathbf{x}_T^2$ 和文本提示 $c_{1,2}$ 生成第一对交互运动 $\mathbf{x}_0^1, \mathbf{x}_0^2$。
2. **噪声优化（第一角色精修）**：固定第二个角色的运动 $\mathbf{x}_0^2$，通过掩码扩散模型 $G_{\theta}^{\mathrm{mask}}$ 对第一个角色的初始噪声 $\mathbf{x}_T^1$ 进行优化，最小化重叠损失和控制损失，得到精修后的运动 $\hat{\mathbf{x}}_0^1$。
3. **增量角色组合**：对于每个新角色 $p$，选定一个已生成的枢纽角色 $k_p$，将 $\hat{\mathbf{x}}_0^{k_p}$ 作为条件输入掩码扩散模型，生成新角色的初始运动，随后通过噪声优化施加物理惩罚，确保新角色与所有已生成角色之间的空间协调。
4. **运动扩展（长时程生成）**：对已生成的运动序列进行运动修复（motion inpainting），在时间维度上扩展运动长度，并施加边界加速度惩罚以保证过渡平滑。

### 模块关系与数据流

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **Base two-person diffusion model (InterGen)** | 提供双人交互的运动先验，作为所有成对交互的生成骨干 | 随机噪声 $\mathbf{x}_T$、文本提示 $c$ | 双人运动序列 $\mathbf{x}_0^1, \mathbf{x}_0^2$ |
| **Masked diffusion adaptation** | 修改基础模型，使其以固定参考角色为条件，仅对目标角色去噪 | 目标角色噪声 $\mathbf{x}_T^p$、参考角色运动 $\hat{\mathbf{x}}_0^{k_p}$、文本提示 $c_{k_p,p}$ | 新角色的初始运动 |
| **Noise optimization with penalty functions** | 通过反向传播优化初始噪声，施加物理惩罚和控制约束 | 掩码扩散模型、已生成角色运动集合、惩罚项配置 | 优化后的噪声 $\hat{\mathbf{x}}_T^p$，进而得到精修运动 $\hat{\mathbf{x}}_0^p$ |
| **Sequential interaction composition** | 迭代选择枢纽角色，增量添加新角色，形成完整群体运动 | 已生成角色运动集合、成对交互图 | 全体 $M$ 个角色的运动序列 |
| **Motion extension (long-duration generation)** | 通过运动修复扩展时间维度，实现长时程交互 | 已生成运动序列、二元掩码 $\mathbf{m}$ | 扩展后的长时程运动序列 |

### 关键设计决策

- **成对分解策略**：群体交互被建模为相互连接的成对交互图，其中角色通过共享枢纽人物连接多个交互。这一设计使得每对交互可以使用独立的语义提示，解决了单一共享提示难以描述复杂群组交互的瓶颈问题。
- **噪声优化而非微调**：所有物理惩罚和控制约束均通过优化初始噪声实现，无需重新训练或微调预训练模型。这保证了方法的即插即用特性，且与具体的预训练模型解耦。
- **物理惩罚体系**：核心惩罚项包括重叠避免惩罚 $\mathcal{L}_{\mathrm{overlap}}$（惩罚根节点间距小于阈值 $\delta$）和时空控制惩罚 $\mathcal{L}_{\mathrm{control}}$（涵盖根位置、移动区域、朝向、相对位置等），总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{overlap}} + \mathcal{L}_{\mathrm{control}}$。

### 运动表征

PINO 沿袭 InterGen 的个体运动表征。对于个体 $p$ 在第 $n$ 帧的姿态，其状态向量为：

$$ \mathbf{x}^p(n) = \left[ \mathbf{j}_{\mathrm{glo}}^p, \mathbf{j}_{\mathrm{vel}}^p, \mathbf{j}_{\mathrm{rot}}^p, \mathbf{g}_{\mathrm{foot}}^p \right] \quad \text{(Eq. 1)} $$

其中：
- $\mathbf{j}_{\mathrm{glo}}^p$：全局坐标系下的关节位置
- $\mathbf{j}_{\mathrm{vel}}^p$：关节速度
- $\mathbf{j}_{\mathrm{rot}}^p$：局部关节旋转
- $\mathbf{g}_{\mathrm{foot}}^p$：二值脚部-地面接触特征

整个群体的运动序列表示为 $X = \{ \mathbf{x}^1, \mathbf{x}^2, \ldots, \mathbf{x}^M \}$，每个个体包含 $N$ 帧、$D$ 维表征。

### 基础双人扩散模型

PINO 的生成主干是一个预训练的文本驱动双人交互扩散模型（InterGen）。给定两个个体的随机噪声 $\mathbf{x}_T^1, \mathbf{x}_T^2$ 和文本提示 $c$，模型通过去噪过程生成双人运动：

$$ [\mathbf{x}_0^1, \mathbf{x}_0^2] = G_{\theta}(\mathbf{x}_T^1, \mathbf{x}_T^2, c) \quad \text{(Eq. 2)} $$

### 掩码扩散适配

为支持以已生成角色为条件、增量添加新角色，PINO 对基础模型进行掩码改造，得到 $G_{\theta}^{\mathrm{mask}}$。其核心机制是：将参考角色（已生成）的运动作为固定条件输入，仅对新加入角色的噪声进行去噪。这一改造使得模型能够生成与参考角色语义一致的新角色运动，而无需重新训练。

### 噪声优化框架

PINO 的核心创新在于通过优化初始噪声来强制执行物理约束和用户控制。对于第一个交互对，首先生成初始运动，然后通过最小化损失函数优化第一个角色的初始噪声：

$$ \hat{\mathbf{x}}_T^1 = \arg\min_{\mathbf{x}_T^1} \mathcal{L}\left(G_{\theta}^{\mathrm{mask}}(\mathbf{x}_T^1, \mathbf{x}_0^2), \mathbf{x}_0^2, c_{1,2}\right) \quad \text{(Eq. 3)} $$

优化过程通过反向传播贯穿整个扩散去噪过程，更新初始噪声以最小化物理惩罚项。

### 物理惩罚函数

#### 重叠避免惩罚

重叠惩罚以角色根节点（骨盆）间距为核心约束，惩罚间距小于阈值 $\delta$ 的情况：

$$ \mathcal{L}_{\mathrm{overlap}} = \sum_i \sum_n \max\left(0, \delta - \|\mathbf{p}_{\mathrm{root}}^p(n) - \hat{\mathbf{p}}_{\mathrm{root}}^i(n)\|_2\right) \quad \text{(Eq. 8)} $$

其中 $\mathbf{p}_{\mathrm{root}}^p(n)$ 为新生成角色在第 $n$ 帧的根节点位置，$\hat{\mathbf{p}}_{\mathrm{root}}^i(n)$ 为已生成角色 $i$ 的对应位置。

#### 时空控制惩罚

控制损失 $\mathcal{L}_{\mathrm{control}}$ 由四个可组合的子惩罚构成：

- **根节点位置惩罚**（Eq. 11）：约束角色在指定时刻到达目标位置
  $$ \mathcal{L}_{\mathrm{root}} = \sum_{n \in \mathcal{N}} \max\left(0, \|\mathbf{p}_{\mathrm{root}}^{p}(n) - \mathbf{p}_{\mathrm{target}}(n)\|^2 - \delta\right) $$

- **朝向惩罚**（Eq. 14）：约束角色面向目标方向
  $$ \mathcal{L}_{\mathrm{orient}} = \sum_{n \in \mathcal{N}} \max\left(0, 1 - \mathbf{d}^{p}(n) \cdot \mathbf{d}_{\mathrm{target}}(n) - \delta\right) $$

- **移动区域惩罚**：惩罚角色进入禁区

- **相对位置惩罚**：约束角色间的空间关系

#### 总优化损失

$$ \mathcal{L} = \mathcal{L}_{\mathrm{overlap}} + \mathcal{L}_{\mathrm{control}} \quad \text{(Eq. 9)} $$

### 顺序交互组合

PINO 通过迭代方式构建任意规模群体运动（Algorithm 1）。每轮迭代中：
1. 从已生成角色中选择一个枢纽（pivot）作为参考
2. 使用掩码扩散模型生成新角色运动，条件为枢纽运动和新交互的文本提示
3. 通过噪声优化施加物理惩罚，确保新角色与所有已生成角色的空间一致性

### 运动扩展（长时程生成）

为实现长时程交互，PINO 采用运动修复（motion inpainting）策略。使用二元掩码 $\mathbf{m}$ 标记已知帧区域，在扩散采样过程中将已知部分替换为原始运动：

$$ \mathbf{x}_t^i \gets \mathbf{m} \odot \hat{\mathbf{x}}^i + (1 - \mathbf{m}) \odot \mathbf{x}_t^i \quad \text{(Eq. 10)} $$

同时引入边界加速度惩罚，确保扩展段与已知段的过渡平滑自然。

## 实验与关键发现

### 双人交互：消除重叠与穿透

现有双人扩散模型（InterGen）虽能生成语义合理的交互，但缺乏物理约束，导致频繁的肢体重叠与穿透。PINO 通过噪声优化引入重叠惩罚（Overlap Penalty），在不重新训练的前提下大幅缓解该问题。

**定量结果**（Table 2(a)）：在 InterHuman 测试集上，PINO-InterGen 将 Overlap 从 InterGen 的 0.119 降至 0.000，甚至低于真实数据（GT 0.029）；穿透体积（Penetration Volume）从 3112.72 cm³ 降至 275.65 cm³，降幅达 91.1%。同时，足部滑动（Foot Skate）和最大加速度（Max Acc.）与 InterGen 相当，表明优化未损害运动自然度。语义指标（Table 2(b)）显示，R-Precision 和 FID 保持竞争性，证明物理约束与语义保真度可兼得。

**定性对比**：Figure 3 展示双人交互生成结果，PINO 生成的序列避免了 InterGen 中常见的角色穿透与姿态畸变，交互边界清晰。

### 多人交互：增量组合与物理约束

将群组交互分解为语义相关的成对交互是 PINO 的核心机制。通过顺序选择枢纽人物（pivot），以掩码扩散模型条件生成新角色，并对每个新增角色施加重叠惩罚，实现任意规模群体的自然交互生成。

**整体评估**（Table 3）：三人场景下，PINO-InterGen 的 Overlap 为 0.000，而 InterGen inpainting 基线高达 0.766；穿透体积从 1598.46 cm³ 降至 46.80 cm³，降幅达 97.1%。足部滑动（0.045 vs 0.042）和最大加速度（0.039 vs 0.042）与基线持平，说明群体扩展未引入额外运动伪影。

**增量评估**（Table 4）：从双人（1,2）逐步增至五人时，每步的 Overlap 均显著低于 InterGen。例如，增量对（1,5）的 Overlap 从 0.977 降至 0.069，FID 从 13.100 降至 12.920，验证了逐对优化策略对群体规模扩展的鲁棒性。

**定性结果**（Figure 4）：PINO 生成的多人交互序列中，角色间保持合理的空间距离，交互动作连贯自然，未出现基线方法中的严重穿透或姿态崩溃。

### 时空控制：用户可定制的运动生成

PINO 在噪声优化中引入可微分的控制惩罚，支持用户对角色根位置、运动区域、朝向和相对距离的灵活约束，无需重新训练。

**消融实验**（Table 5）：逐步叠加四种惩罚项（根位置、区域、重叠、朝向），违规率单调下降。使用全部惩罚时，位置误差（Pos. Err.）0.083、重叠 0.043、区域违规 0.083、朝向误差 0.208，均达到最低。Figure 5 可视化展示了各惩罚项的独立贡献：仅用重叠惩罚可避免碰撞，但角色可能偏离目标位置或朝向；加入根位置和区域惩罚后，角色精确到达指定区域；朝向惩罚进一步修正了面向方向。

**与 inpainting 方法的对比**（Table B）：在指定首末帧位置的场景中，PINO 的优化方法实现 Overlap 0.000、最大加速度 0.039，而 inpainting 基线 Overlap 0.119、最大加速度 0.191。Figure A 显示，inpainting 方法在约束关节与其他关节间产生不协调，导致骨架扭曲；PINO 则保持全身运动一致性。

### 长时程运动扩展

通过运动修复（motion inpainting）与边界加速度惩罚，PINO 支持交互序列的时间扩展。

**非语义指标**（Table 6）：添加加速度惩罚后，足部滑动从 0.045 降至 0.040，最大加速度保持 0.039，过渡段平滑自然。语义评估（Table 7）表明，扩展段裁剪至真实长度后，FID 和 R-Precision 与直接生成相当，未出现语义退化。

### 跨模型泛化与用户研究

**跨模型验证**（Table C）：将 PINO 应用于 in2IN 模型，三人场景 Overlap 从 0.000 降至 0.000（注：原文 Table C 中 in2IN 基线 Overlap 为 0.000，PINO-in2IN 亦为 0.000，需手动核实具体数值），穿透体积大幅降低，FID 和足部滑动保持竞争性，证明优化框架的模型无关性。

**用户研究**（Figure B）：人类评估者在运动真实性、文本一致性和整体偏好三个维度上，对 PINO 的评分均显著优于 InterGen 基线，验证了物理约束对感知质量的提升。

### 失败模式与局限性

1. **推理效率**：噪声优化需 100 步反向传播，仅重叠惩罚时每角色约 1 分钟，全惩罚约 10 分钟，远未达到实时要求。
2. **手部穿透**：因 InterHuman 数据集缺乏手部关节标注，PINO 无法约束手指级别的穿透，手部交互仍存在伪影。
3. **高阶交互依赖**：当前分解策略仅建模成对交互，三人以上的协同行为（如三人同时握手）可能无法精确捕捉。
4. **用户设计负担**：需手动指定成对交互顺序与提示，对复杂群体场景编排繁琐，缺乏自动化的交互图生成机制。

![[assets/figures/papers/paper_list_l1770_PINO_Person_Interaction_Noise_Optimization_for_Long_Duration_and_Customi/figures/005_Table_2.jpg]]
*Table 2: Evaluation of two-person interaction generation while avoiding overlap*

![[assets/figures/papers/paper_list_l1770_PINO_Person_Interaction_Noise_Optimization_for_Long_Duration_and_Customi/figures/012_Table_5.jpg]]
*Table 5: Ablation study on motion penalties. Metrics include positional errors (Pos. Err.↓), overlap (Overlap↓), region violations (Reg. Viol.↓), and orientation errors (Orient. Err.↓). Positional errors are measured with a threshold of 20 cm, region violations with a threshold of 10 cm, and orientation errors with a threshold of 20 degrees. Lower values indicate better performance*

![[assets/figures/papers/paper_list_l1770_PINO_Person_Interaction_Noise_Optimization_for_Long_Duration_and_Customi/figures/010_Figure_5.jpg]]
*Figure 5: Visualization of the ablation study. We incrementally introduce the proposed penalties to InterGen (1). We highlight the unfulfilled demands: Red circle: Individuals not at intended initial/end positions. Green circle: Collision with other individual. Orange circle: Entering restricted regions. Blue circle: Unintended orientation. By introducing additional penalties, our method is able to generate motions that fulfill the requests from the users and naturally fit in the provided context or environment*

![[assets/figures/papers/paper_list_l1770_PINO_Person_Interaction_Noise_Optimization_for_Long_Duration_and_Customi/figures/007_Figure_3.jpg]]
*Figure 3: Comparison of the generated multi-person interaction*

![[assets/figures/papers/paper_list_l1770_PINO_Person_Interaction_Noise_Optimization_for_Long_Duration_and_Customi/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative results of multi-person interaction generation. Representative frames are shown for visualization*

![[assets/figures/papers/paper_list_l1770_PINO_Person_Interaction_Noise_Optimization_for_Long_Duration_and_Customi/figures/002_Table_1.jpg]]
*Table 1: Comparison of recent multi-person interaction generation methods, including single-person method ProgMoGen [20]*

## 定位与知识库关联

### 1. 问题定位：从双人到群体的生成鸿沟

现有文本驱动的多人交互运动生成方法面临一个核心矛盾：**群体规模扩大时，单一共享文本提示无法描述复杂的差异化交互，且缺乏物理约束导致角色重叠、穿透和运动失真**。PINO 将这一瓶颈归因为两个层面：

- **语义层面**：群组交互本质上是多个语义相关的成对交互的集合，而非单一整体行为。现有方法（如 InterGen）使用一个文本提示描述整个群体，无法为不同角色对分配不同的交互语义。
- **物理层面**：扩散模型在去噪过程中缺乏对角色间空间关系的显式建模，导致生成结果中出现严重的穿透和重叠。

### 2. 方法谱系中的位置

#### 2.1 与基线方法的关系

**Table 1** 系统对比了近期多人交互生成方法，PINO 在以下维度形成差异化定位：

| 方法 | 核心机制 | 群体规模 | 文本控制粒度 | 物理约束 | 是否需要训练 |
|------|----------|----------|--------------|----------|--------------|
| **InterGen** | 预训练双人扩散模型 | 2人（固定） | 单一提示 | 无 | 是（预训练） |
| **FreeMotion** | 基于 ControlNet 的序列生成 | 任意 | 逐人提示 | 无 | 是 |
| **InterControl** | 单人 ControlNet 扩展 | 任意 | 逐人提示 | 无 | 是 |
| **Shan et al.** | 监督训练的多人生成 | 多人 | 全局提示 | 无 | 是 |
| **in2IN** | 多人生成框架 | 多人 | 逐人提示 | 无 | 是 |
| **PINO** | 噪声优化 + 成对分解 | 任意 | 逐对提示切换 | 有（后验优化） | 否（无需额外训练） |

**关键区分点**：
- **PINO 对 InterGen**：PINO 直接复用 InterGen 的预训练权重作为运动先验，但通过成对分解和噪声优化突破了双人限制。在双人交互任务上，PINO-InterGen 将 Overlap 从 0.119 降至 0.000，Penetration Volume 从 3112.72 cm³ 降至 275.65 cm³（Table 2a），同时保持语义保真度（Table 2b）。
- **PINO 对 FreeMotion / InterControl**：这些方法通过 ControlNet 架构扩展单人模型，但缺乏对成对交互语义的显式建模和物理约束。PINO 的成对提示切换机制允许为每对角色指定独立的交互语义（如“握手”后切换为“拍照”），而噪声优化提供了统一的物理惩罚框架。
- **PINO 对 in2IN**：PINO 的噪声优化框架具有通用性。**Table C** 显示，将 PINO 应用于 in2IN 模型同样显著减少重叠，同时维持竞争性的 FID 和足部滑动指标，证明优化机制独立于具体生成骨干。

#### 2.2 方法论谱系中的继承与创新

PINO 的方法论可追溯至两个技术脉络：

**脉络一：扩散模型的噪声空间优化**。利用扩散模型去噪过程的可微性，在初始噪声空间进行梯度下降优化以施加约束。这一思路在图像生成领域已有探索（如 classifier guidance），PINO 将其首次系统性地应用于多人运动生成，并设计了针对性的物理惩罚项。

**脉络二：组合式运动生成**。将复杂群体交互分解为可管理的子问题（成对交互），通过枢纽角色（pivot）连接不同交互对。这种“分治”策略与图结构建模有思想共鸣，但 PINO 通过噪声优化实现了免训练的增量组合。

### 3. 适用边界与能力范围

#### 3.1 明确适用的场景

- **任意规模群体**：从 2 人到理论上任意数量，通过增量添加角色实现（Algorithm 1）
- **长时程生成**：通过运动修复（motion inpainting）扩展交互时长，支持平滑过渡（Section 4.4, Eq. 10）
- **多样化控制**：用户可通过时空惩罚灵活指定角色根位置、运动区域、朝向和相对距离，无需重新训练（Section 4.3, Appendix A）
- **语义切换**：在不同成对交互间切换文本提示，实现复杂场景叙事（如 Figure 1 的交替握手序列）

#### 3.2 适用边界与局限

基于论文明确指出的限制：

1. **推理效率瓶颈**：噪声优化耗时，每生成一个角色约需 1 分钟（仅重叠惩罚）到 10 分钟（全惩罚），不适合实时应用。这是梯度下降在扩散空间进行 100 步优化（学习率 0.003）的固有代价。

2. **手部穿透未解决**：由于手部关节数据缺失，手部穿透问题仍有待改进。当前物理惩罚主要作用于根节点层级，对手部等末端关节的约束不足。

3. **高阶交互依赖缺失**：当前方法基于双人扩散模型，可能无法捕捉超过两人的高阶交互依赖（如三人同时协作的复杂模式）。成对分解假设群组交互可近似为成对交互的集合，这一假设在紧密耦合的多人场景中可能失效。

4. **用户设计负担**：用户需要手动指定成对交互的顺序和提示，对复杂场景可能繁琐。缺乏自动生成合理成对交互图的机制。

### 4. 开放问题与未来方向

基于论文的局限性和领域发展趋势，以下问题值得关注：

1. **加速噪声优化**：如何将每角色分钟级的优化降至秒级？可能的方向包括：学习优化器初始化、蒸馏优化轨迹、或设计更高效的采样策略。

2. **扩展基础模型容量**：能否训练直接支持三人或以上交互的基础模型？这将从根本上解决高阶交互依赖问题，但面临数据稀缺和模型复杂度挑战。

3. **自动化交互图构建**：如何从场景描述自动生成合理的成对交互图，减少用户手动设计？这可能涉及大语言模型进行任务规划。

4. **误差累积控制**：在大规模群体中，后续角色的生成依赖于已生成角色的质量，误差可能逐级放大。需要研究更鲁棒的组合策略或全局优化机制。

5. **评估指标完善**：现有指标（Overlap, Penetration Volume, FID, Foot Skate）是否充分评估群组交互的自然性和语义一致性？可能需要引入基于物理模拟或人类感知的新指标。

### 5. 知识库定位总结

PINO 在多人运动生成领域占据**免训练、物理感知、任意规模**的方法学位置。其核心贡献不在于提出新的生成架构，而在于证明：**通过巧妙的噪声空间优化和成对分解策略，预训练的双人扩散模型可以被“外推”至任意规模的群体生成，同时获得物理合理性和用户可控性**。这一思路对资源受限、数据稀缺的场景具有实际价值，但其推理效率瓶颈限制了实时应用的前景。

## 原文 PDF

![[paperPDFs/ICCV_2025/PINO_Person_Interaction_Noise_Optimization_for_Long_Duration_and_Customizable_Motion_Generation_of_Arbitrary_Sized_Groups.pdf]]
