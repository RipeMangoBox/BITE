---
title: "UniHM: Unified Dexterous Hand Manipulation with Vision Language Model"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/UniHM_Unified_Dexterous_Hand_Manipulation_with_Vision_Language_Model.pdf
project_link: https://unihm.github.io/
code_link: null
openreview_forum_id: cVX3VqO8BO
aliases:
- UniHM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "引入形态无关的共享码本（Unified Hand-Dexterous Tokenizer），将异构手部运动映射到统一离散空间，并耦合视觉语言模型（VLM）与物理引导动态优化，从而支持跨手部形态的开放指令操作生成与精细化。"
primary_logic: "利用VQ-VAE交叉手部蒸馏训练，使不同灵巧手的运动可互相翻译，同时通过VLM融合语言、视觉与点云信息自回归生成操作token序列，再以接触与时间先验进行后优化，无需遥操作数据即可实现强泛化。"
claims:
- "UniHM 在 DexYCB 与 OakInk 数据集上多项指标（MPJPE, FPL, FOL, FID）全面超越现有基线（TM2T, MDM, FlowMDM, MotionGPT3），尤其在Final Position Location Error上优势显著（DexYCB 12.15 vs 19.32; OakInk 19.86 vs 23.98）。"
- "消融实验表明深度输入（Depth Input）、渐进掩码训练（Masked Training）和物理细化（Physical Refinement）三个组件各个均对性能至关重要，移除任一部均导致MPJPE等指标明显上升。"
- "真实世界跨具身实验中，UniHM在抓取、放置、推拉、开合等任务上的成功率（最高65%）显著优于MDM+Dex-Retargeting和MotionGPT3+Dex-Retargeting，且未见对象上的泛化能力保持良好。"
- "物理引导优化采用非对称平滑接触核 f(d)，相比欧氏距离对点云噪声更加鲁棒，可视化结果（Figure B2）显示核函数方法即使在噪声输入下也能收敛到正确解。"
---

# UniHM: Unified Dexterous Hand Manipulation with Vision Language Model

> [!tip] 核心洞察
> 利用VQ-VAE交叉手部蒸馏训练，使不同灵巧手的运动可互相翻译，同时通过VLM融合语言、视觉与点云信息自回归生成操作token序列，再以接触与时间先验进行后优化，无需遥操作数据即可实现强泛化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | UniHM：基于视觉语言模型的统一灵巧手操作 |
| 英文题名 | UniHM: Unified Dexterous Hand Manipulation with Vision Language Model |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=cVX3VqO8BO) · [Project](https://unihm.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | UniHM |
| Dataset | DexYCB (Seen), OakInk (Seen) |

> [!tip] 效果简介
> - DexYCB (Seen) 上，MPJPE↓ 为 61.40，对比 MotionGPT3: 74.80，变化 -13.40。
> - DexYCB (Seen) 上，FPL↓ 为 12.15，对比 MotionGPT3: 19.32，变化 -7.17。
> - OakInk (Seen) 上，FPL↓ 为 19.86，对比 MotionGPT3: 23.98，变化 -4.12。

## 概要

灵巧手操作是具身智能走向真实世界应用的关键瓶颈。现有方法大多局限于静态抓取姿态生成，或依赖预定义的交互序列，难以理解开放词汇的语言指令，更无法生成跨手部形态、长时域的物理可行操作轨迹。**UniHM** 作为首个以自由语言指令为条件的统一灵巧手操作框架，直接回应了这一核心矛盾。

其核心思路可概括为“统一表示—语言驱动生成—物理后优化”三阶段范式：

1. **形态无关的统一动作空间**：提出 Unified Hand-Dexterous Tokenizer，利用共享 VQ-VAE 码本将异构灵巧手（Shadow、Allegro、SVH、Leap、Panda）的运动映射到同一离散空间。新形态手部通过知识蒸馏对齐隐空间后即可无缝接入，无需重新训练码本。这一设计使不同灵巧手的姿态可互相翻译，从根本上解决了跨具身泛化的表示瓶颈。
2. **视觉语言模型驱动的序列生成**：以 Qwen3-0.6B 为基座，融合 RGB-D 图像、开放词汇语言指令、目标轨迹与物体点云信息，自回归生成操作 token 序列。渐进掩码训练策略使模型学会在部分 token 缺失的条件下补全序列，增强了长序列生成的鲁棒性。
3. **物理引导的动态细化**：对 VLM 生成的粗糙轨迹逐帧执行高斯-牛顿优化，引入非对称平滑接触核 $f(d)$（穿透时指数惩罚、分离时二次惩罚）替代传统欧氏距离，使指尖在噪声点云下仍能收敛到正确接触位置。同时融合生成先验与时间先验，确保输出序列平滑且物理可行。

在实验验证层面，UniHM 在 DexYCB 与 OakInk 两个标准数据集上全面超越现有基线（TM2T、MDM、FlowMDM、MotionGPT3），尤其在 Final Position Location Error 上优势显著（DexYCB: 12.15 vs 19.32; OakInk: 19.86 vs 23.98）。消融实验证实深度输入、渐进掩码训练与物理细化三个组件各自均对性能至关重要。更重要的是，在真实世界跨具身实验中，UniHM 在抓取、放置、推拉、开合等任务上的成功率（最高 65%）大幅领先 MDM+Dex-Retargeting 与 MotionGPT3+Dex-Retargeting 组合，且在未见对象上保持了良好的泛化能力。

值得注意的是，整个框架仅依赖人类-物体交互（HOI）视频数据与 GPT-4o 自动语言标注，无需昂贵的遥操作数据，显著降低了灵巧手操作学习的数据门槛。这一数据效率优势，结合统一的形态无关表示，使 UniHM 成为向通用灵巧操作迈出的重要一步。



灵巧手操作是机器人学中长期存在的核心挑战。与简单夹爪的抓取不同，灵巧手拥有多指、多自由度的结构，能够执行抓取、放置、推拉、开合等丰富操作，但这也使得运动规划与控制变得极为复杂。近年来，基于学习的方法在灵巧手操作上取得了显著进展，然而现有工作普遍面临两个关键瓶颈：

**瓶颈一：缺乏对开放词汇语言指令的理解。** 当前主流方法大多局限于静态抓取姿态生成，或依赖预定义的交互序列与目标物体类别。它们无法理解自由形式的语言指令（如“小心地拿起桌上的苹果”或“拉开抽屉并放入杯子”），因而难以在真实世界中灵活泛化。

**瓶颈二：异构手部形态之间的迁移困难。** 不同灵巧手在自由度数量、关节结构、指节长度等形态参数上差异巨大——从 Shadow Hand（五指仿人手）到 Allegro Hand（四指），再到 SVH Hand 与 LEAP Hand 等。现有方法通常为每种手部形态独立设计编码器/解码器，缺乏统一的动作表示空间，导致跨形态迁移需要大量额外数据与工程适配。

**核心洞察：** UniHM 的关键思路在于——利用 VQ-VAE 交叉手部蒸馏训练，使不同灵巧手的运动可互相翻译，同时通过视觉语言模型（VLM）融合语言、视觉与点云信息，自回归生成操作 token 序列，再以接触与时间先验进行后优化。这一设计使得模型无需遥操作数据即可实现强泛化。

**数据瓶颈的突破。** 大规模灵巧手遥操作数据获取成本极高，严重制约了可扩展性。UniHM 另辟蹊径：仅使用人类-物体交互（HOI）视频数据，通过 GPT-4o 自动生成开放词汇语言标注，并利用 Dex-Retargeting 将 MANO 手部姿态映射到多种机器人灵巧手。这一数据策略大幅降低了训练成本，同时为模型提供了丰富的语义-动作对应关系。

**物理可行性的保障。** 单纯从数据中学习的运动生成模型容易产生穿透物体、关节抖动等物理上不可行的结果。UniHM 引入物理引导动态细化模块，采用非对称平滑接触核函数 $f(d)$（见 Eq 12），在穿透时呈指数增长惩罚，相比欧氏距离对点云噪声更加鲁棒（Figure B2 展示了噪声输入下核函数方法仍能收敛到正确解），确保生成轨迹满足接触约束与时间平滑性。

综上所述，UniHM 试图回答一个核心问题：**能否构建一个统一的框架，使得单一模型在仅依赖 HOI 视频数据训练后，即可理解开放词汇语言指令，并为多种异构灵巧手生成物理可行的操作序列？** 这一问题的解决将显著推动灵巧手操作从实验室走向真实世界应用。



## 核心方法与创新机理

UniHM 的核心创新在于将灵巧手操作从“特定形态、预设轨迹”推进到“跨形态、开放指令、物理可行”的统一框架。其关键设计围绕三个 **changed slots** 展开：

### 1. 动作表示：形态无关的统一离散空间

现有方法（如 **MDM**、**MotionGPT3**）为不同灵巧手设计独立的编码/解码器，无法实现跨手部迁移。UniHM 提出 **Unified Hand-Dexterous Tokenizer**——一个基于 VQ-VAE 的共享码本，将所有异构手部姿态映射到同一离散空间：

$$c = Q\left(E_h\left(\mathbf{x}^{(h)}\right)\right) = \arg\min_{k\in[K]}\left\|\mathbf{z}_e^{(h)} - \mathbf{e}_k\right\|_2^2$$

其关键机制是**交叉手部蒸馏**：当集成新形态手部时，先通过知识蒸馏对齐新编码器与参考编码器的隐空间（$\mathcal{L}_{\mathrm{distill}} = \|E_{\mathrm{new}}(\mathbf{x}_{\mathrm{new}}) - E_{\mathrm{ref}}(\mathbf{x}_{\mathrm{ref}})\|_2^2$），再微调 VQ-VAE。这使得不同手部姿态可以互相翻译——编码源手部姿态，用量化码本索引查找共享码字，再由目标手部解码器重建：

$$\hat{\mathbf{x}}^{(j)} = D_j\left(\mathbf{e}_{Q\left(E_i\left(\mathbf{x}^{(i)}\right)\right)}\right)$$

**效果**：无需为新形态重新训练生成模型，码本天然支持跨手部泛化。消融中 1D-Conv 骨干在全部灵巧手上的 MAE（0.0256）显著优于 MLP（0.0350）（Table B1）。

### 2. 条件模态：从类别标签到开放词汇多模态理解

基线方法仅依赖物体类别或预设轨迹，缺乏对自然语言指令的理解。UniHM 将条件信号扩展为 **RGB-D 图像 + 开放词汇语言指令 + 目标轨迹 + 物体点云** 的联合输入。DexHand VLM（以 Qwen3-0.6B 为基座）融合这些信息，自回归生成操作 token 序列：

$$\hat{Q}_{pos} = D_h\big(\mathbf{VLM}(E_j(Qpos_0), \mathcal{T}_{\mathrm{tar}}, \mathcal{P}_{\mathrm{obj}}, \mathcal{T})\big)$$

其中 $\mathcal{T}_{\mathrm{tar}}$ 由 CLIPort 从 RGB-D 和指令中推断，$\mathcal{P}_{\mathrm{obj}}$ 由 Point-SAM 分割。训练采用**渐进掩码课程**——从 teacher forcing 逐步过渡到自回归生成，使模型学会利用语言和感知信息补全序列。消融显示，移除深度输入后 MPJPE 从 61.40 升至 78.12，移除掩码训练后 FID 从 31.24 升至 38.56（Table 4），验证了多模态感知与掩码策略的关键作用。

### 3. 物理可行性：后验接触-时间联合优化

多数基线方法不包含物理细化步骤，生成结果可能穿透物体或违反物理约束。UniHM 引入 **Physical-Guided Dynamic Refinement**，对 VLM 生成的轨迹逐帧进行高斯-牛顿优化，目标函数融合三项：

$$\mathcal{E}_t(q_t, q_t^{\mathrm{gen}}, q_{t-1}^{\mathrm{opt}}, q_{t-2}^{\mathrm{opt}}) = \mathcal{E}_{\mathrm{contact}}(q_t) + \mathcal{E}_{\mathrm{gen}}(q_t, q_t^{\mathrm{gen}}) + \mathcal{E}_{\mathrm{time}}(q_t, q_{t-1}^{\mathrm{opt}}, q_{t-2}^{\mathrm{opt}})$$

其中接触能量采用**非对称平滑核函数** $f(d)$——在穿透时呈指数增长，在非穿透时二次增长，相比欧氏距离对点云噪声更加鲁棒（Figure B2 可视化证实）。优化通过 Levenberg-Marquardt 阻尼求解正规方程：

$$(J_t^{\mathrm{T}} J_t + \mathbf{W}_{\mathrm{gen}} + \mathbf{W}_{\mathrm{vel}} + \mathbf{W}_{\mathrm{acc}} + \lambda I) \Delta q_t = -J_t^{\mathrm{T}} r_{\mathrm{contact}}(q_t) - \tilde{\mathbf{W}}$$

**效果**：移除物理细化后，FPL 从 12.15 升至 16.22，FID 也明显上升（Table 4），证明该模块对消除穿透和保持分布真实性的贡献。

### 训练数据范式转变

与依赖遥操作数据的基线不同，UniHM 仅使用**人类-物体交互（HOI）视频数据**，通过 GPT-4o 自动标注语言指令，以 Dex-Retargeting 将 MANO 姿态映射到多种机器人手，配合能量优化提高物理一致性。这一范式大幅降低了数据获取成本，同时使模型天然具备跨具身泛化能力——真实世界实验中，UniHM 在未见对象上的 Pick & Place 成功率达 35%，优于 MotionGPT3+Dex-Retargeting 的 25%（Table 3）。



![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_cVX3VqO8BO/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline. UniHM converts open-vocabulary instructions and RGB-D inputs into executable dexterous-hand trajectories via three stages: (1) morphology-agnostic motion tokenization; (2) language-guided generation that fuses text, perception, and token history to produce manipulation token sequences; and (3) physics-aware decoding with smoothness/contact priors for feasible, stable execution*

UniHM 的整体设计遵循“统一表示—语言驱动生成—物理后优化”三阶段流水线，将开放词汇语言指令与 RGB-D 感知输入转化为可执行的灵巧手操作轨迹（Figure 2）。

**核心瓶颈与设计动机**：现有方法要么局限于静态抓取姿态生成，要么依赖预定义交互序列，缺乏对自由形式语言指令的理解，无法在跨手部形态下生成动态、长时域的物理可行操作。UniHM 通过引入形态无关的共享离散动作空间，使异构灵巧手的运动可互相翻译，同时耦合 VLM 与物理引导优化，在不依赖遥操作数据的前提下实现强泛化。

**流水线三阶段**：

1. **自动数据标注与重定向**（Section 3.1）：以 HOI 视频为唯一数据源，利用 GPT-4o 为操作序列生成开放词汇语言标注；通过 Dex-Retargeting 将 MANO 姿态映射到五种机器人灵巧手（Shadow、Allegro、SVH、Leap、Panda），并经能量优化提升物理一致性。

2. **形态无关的统一动作分词**（Section 3.2）：构建共享 VQ-VAE 码本，为每种灵巧手配备独立编码器/解码器，但共享同一离散码本。新形态灵巧手通过知识蒸馏对齐隐空间后接入，无需重新训练整个码本，实现跨手部姿态翻译。

3. **语言驱动的 VLM 序列生成**（Section 3.3）：以 Qwen3-0.6B 为基座，融合 RGB-D 图像、文本指令、目标轨迹（由 CLIPort 推断）和物体点云（由 Point-SAM 分割）信息，自回归生成操作 token 序列，采用渐进掩码课程训练增强序列建模能力。

4. **物理引导动态细化**（Section 3.4）：对 VLM 生成轨迹逐帧进行高斯-牛顿优化，目标函数融合接触能量（基于非对称平滑核 $f(d)$ 的 signed point-to-plane 距离）、生成先验和时间平滑先验，确保最终轨迹的物理可行性、接触一致性与时序平滑性。

**推理时适配**：保持 HOI 生成器冻结，仅微调 CLIPort 感知模块以适应场景分布变化，兼顾数据效率与鲁棒性。

**输入输出流**：输入为自由形式语言指令 + 单帧 RGB-D 图像；输出为完整灵巧手关节轨迹序列，可直接部署到多种真实灵巧手平台（Figure 1）。



UniHM 的核心架构由三个级联模块构成：**统一灵巧手分词器**（Unified Hand-Dexterous Tokenizer）负责将异构手部姿态映射到共享离散空间；**DexHand VLM** 融合多模态条件自回归生成操作 token 序列；**物理引导动态细化**（Physical-Guided Dynamic Refinement）对生成轨迹进行逐帧后优化，确保物理可行性。以下逐模块展开关键公式与变量含义。

### 3.1 统一灵巧手分词器：形态无关的共享码本

该模块的核心目标是构建一个跨手部形态的离散动作空间。对于手部 $h$ 的输入姿态 $\mathbf{x}^{(h)}$，其编码器 $E_h$ 输出连续隐变量 $\mathbf{z}_e^{(h)}$，随后通过向量量化映射到共享码本 $\{\mathbf{e}_k\}_{k=1}^K$ 中最近的条目：

$$
c = Q\left(E_h\left(\mathbf{x}^{(h)}\right)\right) = \arg\min_{k\in[K]}\left\|\mathbf{z}_e^{(h)} - \mathbf{e}_k\right\|_2^2 \tag{1}
$$

其中 $c$ 为离散 token 索引，$\mathbf{e}_k$ 为码本中第 $k$ 个条目。解码器 $D_h$ 从量化表示 $\mathbf{z}_q^{(h)} = \mathbf{e}_c$ 重建该手部的姿态：

$$
\hat{\mathbf{x}}^{(h)} = D_h\left(\mathbf{z}_q^{(h)}\right) = D_h\left(\mathbf{e}_c\right) \tag{2}
$$

**新手部形态的集成**不依赖直接的非可微 token 对齐，而是通过知识蒸馏将新编码器 $E_{\mathrm{new}}$ 的隐空间与参考编码器 $E_{\mathrm{ref}}$ 对齐：

$$
\mathcal{L}_{\mathrm{distill}} = \|E_{\mathrm{new}}(\mathbf{x}_{\mathrm{new}}) - E_{\mathrm{ref}}(\mathbf{x}_{\mathrm{ref}})\|_2^2 \tag{3}
$$

蒸馏完成后，再对 VQ-VAE 进行微调，使新手部编码器可直接使用共享码本。

**跨手部姿态翻译**则直接利用共享码本的可交换性：给定源手部 $i$ 的姿态 $\mathbf{x}^{(i)}$，将其编码后用量化 token 驱动目标手部 $j$ 的解码器，即实现姿态迁移：

$$
\hat{\mathbf{x}}^{(j)} = D_j\left(\mathbf{e}_{Q\left(E_i\left(\mathbf{x}^{(i)}\right)\right)}\right) \tag{6}
$$

这一设计使得不同自由度、不同构型的灵巧手之间可以互相翻译运动语义，无需成对数据。

### 3.2 DexHand VLM：多模态条件序列生成

VLM 模块以 Qwen3-0.6B 为基座，采用解耦架构将场景感知与 HOI 序列生成分离。感知端通过 CLIPort 风格的视觉模块从 RGB-D 图像和语言指令中推断目标轨迹 $\mathcal{T}_{\mathrm{tar}}$，并通过 Point-SAM 分割物体点云 $\mathcal{P}_{\mathrm{obj}}$。生成端则融合文本指令 $\mathcal{T}$、目标轨迹编码、物体点云编码及历史 token 序列，自回归预测下一帧的操作 token。最终，目标手部解码器 $D_h$ 将生成的 token 序列映射为关节位置：

$$
\hat{Q}_{pos} = D_h\big(\mathbf{VLM}(E_j(Qpos_0), \mathcal{T}_{\mathrm{tar}}, \mathcal{P}_{\mathrm{obj}}, \mathcal{T})\big) \tag{9}
$$

训练采用**渐进掩码课程策略**：初期使用 teacher forcing 同时输入语言和真值序列，随后逐步以概率 $p_t$ 将真值 token 替换为掩码 token，迫使模型学习从语言条件和部分历史中补全序列，增强自回归生成能力。

### 3.3 物理引导动态细化：接触感知的逐帧优化

VLM 生成的粗糙轨迹可能存在指尖穿透物体或运动不平滑的问题。该模块将其视为逐帧的后验优化问题，每帧 $t$ 的关节状态 $q_t$ 通过高斯-牛顿法求解，目标函数由三项组成：

**接触能量**：定义指尖 $i$ 到物体表面沿法线方向的带符号点面距离：

$$
d_i(q_t) = \mathbf{n}_i^{\mathrm{T}} \left( \mathcal{T}_{\mathrm{tar}}(t)^{-1} s_i(q_t) - \mathbf{p}_i \right) \tag{11}
$$

其中 $s_i(q_t)$ 为指尖在世界坐标系的位置，$\mathbf{p}_i$ 和 $\mathbf{n}_i$ 分别为物体表面点的位置和法线，$\mathcal{T}_{\mathrm{tar}}(t)^{-1}$ 将指尖变换到物体坐标系。为在穿透时施加指数级惩罚而在非穿透区保持二次平滑，采用非对称平滑核函数：

$$
f(d) = \begin{cases} \frac{\alpha}{2} d^2, & d \geq 0 \\ \frac{\alpha}{k^2} (e^{-kd} + kd - 1), & d < 0 \end{cases} \tag{12}
$$

其中 $\alpha$ 控制非穿透区惩罚强度，$k$ 控制穿透区指数增长速率。接触残差定义为 $r_{\mathrm{contact},i}(q_t) = \sqrt{2\lambda_c f(d_i(q_t))}$，接触能量为残差的平方和。

**逐帧总能量**融合接触项、生成先验项和时间平滑项：

$$
\mathcal{E}_t(q_t, q_t^{\mathrm{gen}}, q_{t-1}^{\mathrm{opt}}, q_{t-2}^{\mathrm{opt}}) = \mathcal{E}_{\mathrm{contact}}(q_t) + \mathcal{E}_{\mathrm{gen}}(q_t, q_t^{\mathrm{gen}}) + \mathcal{E}_{\mathrm{time}}(q_t, q_{t-1}^{\mathrm{opt}}, q_{t-2}^{\mathrm{opt}}) \tag{16}
$$

其中 $\mathcal{E}_{\mathrm{gen}}$ 惩罚当前解偏离 VLM 生成值 $q_t^{\mathrm{gen}}$ 的程度，$\mathcal{E}_{\mathrm{time}}$ 包含速度和加速度平滑项，依赖前两帧优化结果 $q_{t-1}^{\mathrm{opt}}, q_{t-2}^{\mathrm{opt}}$。

**求解**：线性化接触残差后，带 Levenberg-Marquardt 阻尼 $\lambda$ 的正规方程为：

$$
(J_t^{\mathrm{T}} J_t + \mathbf{W}_{\mathrm{gen}} + \mathbf{W}_{\mathrm{vel}} + \mathbf{W}_{\mathrm{acc}} + \lambda I) \Delta q_t = -J_t^{\mathrm{T}} r_{\mathrm{contact}}(q_t) - \tilde{\mathbf{W}} \tag{17}
$$

其中 $J_t$ 为接触残差关于 $q_t$ 的雅可比矩阵，$\mathbf{W}_{\mathrm{gen}}, \mathbf{W}_{\mathrm{vel}}, \mathbf{W}_{\mathrm{acc}}$ 分别为生成先验、速度先验和加速度先验的权重矩阵，$\tilde{\mathbf{W}}$ 为这些先验项的线性梯度：

$$
\tilde{\mathbf{W}} \triangleq \mathbf{W}_{\mathrm{gen}}(q_t - q_t^{\mathrm{gen}}) + \mathbf{W}_{\mathrm{vel}}(q_t - q_{t-1}^{\mathrm{opt}}) + \mathbf{W}_{\mathrm{acc}}((q_t - q_{t-1}^{\mathrm{opt}}) - (q_{t-1}^{\mathrm{opt}} - q_{t-2}^{\mathrm{opt}})) \tag{18}
$$

求解得到增量 $\Delta q_t$ 后更新 $q_t \leftarrow q_t + \Delta q_t$，迭代至收敛。该优化为后处理步骤，不参与 VLM 训练，但消融实验（Table 4）表明移除该模块会导致 FPL 从 12.15 升至 16.22，FID 从 31.24 升至 38.56，验证了其对穿透抑制和分布保真的双重作用。



## 实验与关键发现

### 实验设置

**数据集与划分。** UniHM 在两个主流灵巧手-物体交互数据集上进行评估：DexYCB 和 OakInk。DexYCB 提供以人手为中心的抓取姿态序列，OakInk 则包含更丰富的交互类型与物体类别。两个数据集均按 80/20 的比例划分为 Seen 和 Unseen 子集，其中 Unseen 子集包含训练阶段未见过的物体与轨迹，用于检验模型的泛化能力。

**基线方法。** 选取四类代表性运动生成方法作为对比基线：**TM2T**（文本-动作生成）、**MDM**（Tevet et al., 2023，扩散模型人体运动生成）、**FlowMDM**（Barquero et al., 2024，流模型运动生成）和 **MotionGPT3**（Zhu et al., 2025，将运动视为语言进行序列生成）。所有基线方法采用相同的 80/20 数据划分，并在统一的特征编码器下评估 FID 等分布指标，保证比较的公平性。

**评估指标。** 采用五项指标从重建精度与分布质量两个维度评估生成的运动序列：
- **MPJPE**（Mean Per Joint Position Error，mm）：关节位置平均误差，衡量逐帧重建精度；
- **FOL**（Final Object Location Error，mm）：最终物体位置误差，衡量操作终态的准确性；
- **FPL**（Final Position Location Error，mm）：最终手部位置误差，衡量末端定位精度；
- **FID**（Fréchet Inception Distance）：衡量生成运动分布与真实分布的距离；
- **Diversity**：衡量生成运动的多样性，越接近真实数据值越好。

**真实世界实验设置。** 硬件平台采用 Franka 机械臂配合多种灵巧手（Shadow Hand、Allegro Hand、SVH Hand、Leap Hand 和 Panda Hand）。任务指令标准化，成功率由人工判定，以减少评估偏差。实验涵盖 Seen 和 Unseen 两类对象上的四个典型任务：Grab（抓取）、Pick & Place（拾取放置）、Pull & Push（推拉）和 Open & Close（开合）。

---

### 主实验结果

#### DexYCB 数据集（Table 1）

UniHM 在 DexYCB 数据集的 Seen 和 Unseen 子集上均取得最优性能，全面超越所有基线方法。


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_cVX3VqO8BO/figures/003_Table_1.jpg]]
*Table 1: Main Result on DexYCB. The arrow pointing to the right means closer to the GT*

| 指标 | UniHM (Ours) | MotionGPT3 | 提升幅度 |
|------|-------------|------------|----------|
| MPJPE↓ | **61.40** | 74.80 | -13.40 |
| FOL↓ | **23.14** | 26.20 | -3.06 |
| FPL↓ | **12.15** | 19.32 | -7.17 |
| FID↓ | **31.24** | 37.12 | -5.88 |
| Diversity | **39.62** | 41.50 | 更接近GT |

在 Unseen 子集上，UniHM 同样保持领先，尤其在 FPL 指标上的优势最为显著（12.15 vs MotionGPT3 的 19.32），表明模型对未见物体的末端定位能力具有明显优势。

#### OakInk 数据集（Table 2）

在任务类型更丰富的 OakInk 数据集上，UniHM 同样表现出一致的优越性：


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_cVX3VqO8BO/figures/004_Table_2.jpg]]
*Table 2: Main Result on OakInk. The arrow pointing to the right means closer to the GT*

| 指标 | UniHM (Ours) | MotionGPT3 | 提升幅度 |
|------|-------------|------------|----------|
| FPL↓ | **19.86** | 23.98 | -4.12 |
| FID↓ | **204.91** | 221.10 | -16.19 |

跨数据集的稳定优势表明，UniHM 的统一码本表示和物理引导优化机制对不同交互类型具有良好的适应性。

#### 真实世界实验（Table 3）

真实世界跨具身实验中，UniHM 在所有任务和对象划分上均取得最高成功率：


![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_cVX3VqO8BO/figures/005_Table_3.jpg]]
*Table 3: Real-World Experiments*

| 任务 | 对象划分 | UniHM | MotionGPT3 + Dex-Retargeting | MDM + Dex-Retargeting |
|------|---------|-------|---------------------------|---------------------|
| Grab | Seen | **65%** | 30% | 25% |
| Pick & Place | Seen | **50%** | 30% | 25% |
| Pull & Push | Seen | **60%** | 35% | 30% |
| Open & Close | Seen | **55%** | 30% | 25% |
| Grab | Unseen | **45%** | 25% | 20% |
| Pick & Place | Unseen | **35%** | 25% | 20% |

UniHM 在 Seen 对象上的抓取成功率达到 65%，相比 MotionGPT3+Dex-Retargeting（30%）提升超过一倍。在 Unseen 对象上，UniHM 的 Pick & Place 成功率为 35%，仍优于基线（25%），证明模型具备良好的开放世界泛化能力。

---

### 消融实验（Table 4）

为量化各组件的贡献，在 DexYCB 数据集上进行了系统的消融实验，逐一移除深度输入、渐进掩码训练和物理细化三个关键组件。

| 配置 | MPJPE↓ | FOL↓ | FPL↓ | FID↓ | Diversity |
|------|--------|------|------|------|-----------|
| **Ours (完整)** | **61.40** | **23.14** | **12.15** | **31.24** | **39.62** |
| w/o Depth Input | 78.12 | 27.89 | 16.48 | 35.10 | 40.15 |
| w/o Masked Training | 63.50 | 24.67 | 13.02 | 38.56 | 42.30 |
| w/o Physical Refinement | 62.18 | 24.01 | 16.22 | 36.47 | 40.88 |

**深度输入（Depth Input）** 的移除导致 MPJPE 从 61.40 急剧上升至 78.12，增幅达 27%。这一结果表明，深度信息对于精确的空间交互定位至关重要，RGB 信息不足以恢复精细的三维手-物关系。

**渐进掩码训练（Masked Training）** 的移除（仅使用 teacher forcing）导致 FID 从 31.24 升至 38.56，Diversity 从 39.62 偏离至 42.30。这表明掩码策略通过逐步增加模型的自回归生成能力，有效提升了序列生成的分布质量和多样性。

**物理细化（Physical Refinement）** 的移除使得 FPL 从 12.15 升至 16.22，增幅约 33%。这验证了后优化步骤对改善末端定位精度和减少物体穿透的关键作用。物理细化作为后处理步骤，将语义上合理但物理上不可行的规划转化为可执行的轨迹。

---

### 架构选择的验证（Table B1）

在统一分词器的骨干网络选择上，对比了 MLP 和 1D-Conv 在六种灵巧手上的验证集性能：

| 骨干 | Allegro | Shadow | Schunk | LEAP | Ability | Panda | 整体 MAE |
|------|---------|--------|--------|------|---------|-------|----------|
| MLP | 0.0382 | 0.0361 | 0.0348 | 0.0335 | 0.0349 | 0.0325 | 0.0350 |
| **1D-Conv** | **0.0284** | **0.0261** | **0.0253** | **0.0248** | **0.0251** | **0.0239** | **0.0256** |

1D-Conv 在所有灵巧手上均优于 MLP，整体 MAE 从 0.0350 降至 0.0256，RMSE 同样显著降低。这表明时序卷积结构能更好地捕捉手部关节运动的时间依赖性，为后续的 VLM 生成提供更高质量的离散表示。

---

### 接触核函数的鲁棒性验证（Figure B2）

物理优化中采用的非对称平滑接触核 $f(d)$ 相比欧氏距离对点云噪声更加鲁棒。Figure B2 的可视化对比显示：
- 在含噪声点云上，$f(d)$ 核的优化结果（A）使指尖准确收敛到物体表面附近；
- 欧氏距离的优化结果（B）则出现明显偏移，指尖位置分散且偏离表面；
- 将优化结果投影到无噪声点云后（C vs D），$f(d)$ 核的指尖位置依然紧贴物体表面，而欧氏距离的指尖位置出现穿透或悬空。

这种鲁棒性源于 $f(d)$ 的非对称设计：在 $d \ge 0$（指尖在物体外部）时采用二次惩罚，在 $d < 0$（穿透）时采用指数增长惩罚（$\frac{\alpha}{k^2} (e^{-kd} + kd - 1)$），使得优化过程即使在噪声干扰下也能有效避免穿透并收敛到正确接触解。

---

### 失败模式分析

尽管 UniHM 在多数指标上取得领先，实验中也暴露出若干典型失败模式：

1. **精细操作中的力控不足**：UniHM 依赖 RGB-D 感知，未集成触觉或力反馈。在需要精确力控的任务（如抓取易碎物体、拧瓶盖）中，物理优化中的接触能量仅为简化模型，未显式建模摩擦与物体变形，可能导致抓取失败或物体滑落。

2. **高动态任务的物理约束松弛**：物理优化采用逐帧高斯-牛顿方法，缺乏对整条轨迹的全局约束。在快速推拉或抛接等高动态任务中，生成轨迹可能出现瞬时加速度不连续或动量不守恒的问题。

3. **新形态灵巧手的重定向误差**：人体视频数据通过 Dex-Retargeting 映射到机器手时，当机器手自由度远少于人手（如 Panda Hand），语义保真度与物理可行性的权衡可能导致部分手势无法准确复现。

4. **未见动词-名词组合的泛化边界**：UniHM 在 Unseen 对象上成功率有所下降（如 Pick & Place 从 50% 降至 35%），表明模型对训练分布外的新交互类型仍存在泛化瓶颈。

---

### 关键图表结论汇总

- **Table 1 & Table 2**：UniHM 在两个数据集上全面超越基线，FPL 优势尤为显著（DexYCB 12.15 vs 19.32，OakInk 19.86 vs 23.98），验证了统一码本表示与物理优化的有效性。
- **Table 3**：真实世界实验中，UniHM 在四个任务上的成功率均最高（最高 65%），且对未见对象保持良好泛化能力。
- **Table 4**：深度输入、渐进掩码训练和物理细化三个组件各自对性能有显著贡献，移除任一部均导致关键指标明显恶化。
- **Figure B2**：非对称平滑接触核 $f(d)$ 在噪声点云下比欧氏距离更鲁棒，是物理优化成功的关键设计。
- **Table B1**：1D-Conv 骨干在所有灵巧手上一致优于 MLP，验证了时序建模对运动表示的重要性。

### 补充图表

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_cVX3VqO8BO/figures/014_Figure_3.jpg]]
*Figure 3: Real-World Results. UniHM achieves higher success rates than prior methods on both seen and unseen objects, producing physically consistent and executable real-world manipulations. Table 4: Ablation Result on DexYCB. The arrow pointing to the right means closer to the GT*

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_cVX3VqO8BO/figures/017_Figure_12.jpg]]
*Figure 12: Figure B2: Optimization results when the point cloud includes noise. Here, the black points represent the object point cloud, and the red/green points denote the positions of the dexterous hand’s fingertips. (A) Optimization using the f ( d ) kernel, visualized on the noisy input. (B) Optimization using the Euclidean distance, visualized on the noisy input. (C) The f(d) kernel optimization result projected onto the clean noise-free point cloud. (D) The Euclidean distance optimization result projected onto the noise-free point cloud*




## 定位与知识库关联

### 1. 核心瓶颈与因果机制

现有灵巧手操作方法普遍受限于两个结构性问题。其一，动作表示层面：各灵巧手形态（Shadow、Allegro、SVH、LEAP、Panda等）使用独立编码/解码器，缺乏统一的跨手部动作空间，导致方法难以泛化至新形态末端执行器。其二，条件生成层面：多数工作仅依赖目标物体类别或预设轨迹，不具备对开放词汇语言指令的理解能力，无法生成动态、长时域的物理可行操作序列。

UniHM 通过引入**形态无关的共享码本（Unified Hand-Dexterous Tokenizer）** 作为因果旋钮，将异构手部运动映射到统一离散空间。该码本基于 VQ-VAE 架构，并通过知识蒸馏对齐不同手部编码器的隐空间，使新形态手部可快速集成而不需重新训练整个系统。在此统一表示之上，耦合视觉语言模型（VLM）与物理引导动态优化，实现“开放指令→token序列→物理可行轨迹”的端到端生成与精细化。

核心洞察在于：利用 VQ-VAE 的交叉手部蒸馏训练，使不同灵巧手的运动可互相翻译（跨手部姿态迁移）；同时通过 VLM 融合语言、RGB-D 视觉与物体点云信息，自回归生成操作 token 序列；再以非对称平滑接触核 $f(d)$ 与时空先验进行后优化，确保生成的指尖轨迹既不穿透物体又保持时序平滑。该范式仅需人类-物体交互（HOI）视频数据配合 GPT-4o 语言标注，无需昂贵的大规模遥操作数据。

### 2. 与基线方法的关系

UniHM 在以下关键维度上与现有工作形成对比：

**动作表示的统一性。** 基线方法如 **TM2T**、**MDM**（Tevet et al., 2023）、**FlowMDM**（Barquero et al., 2024）和 **MotionGPT3**（Zhu et al., 2025）均针对特定手部形态设计编码/解码器，或依赖 MANO 等参数化手模型，缺乏跨形态泛化能力。UniHM 的共享 VQ-VAE 码本通过蒸馏机制实现了形态无关的离散动作空间，支持 5 种机器人手的统一表示与跨手部姿态翻译（Eq 6）。

**条件模态的丰富度。** 多数基线仅以目标物体类别或预设轨迹为条件，而 UniHM 引入 RGB-D 图像 + 开放词汇语言指令 + 目标轨迹 + 物体点云的多模态条件（Eq 7-9），使生成过程能理解自然语言中的动词-名词组合与空间关系。

**物理可行性的保障。** 除 UniHM 外，现有方法普遍不包含物理细化步骤，生成结果可能存在指尖穿透物体或不满足运动学约束的问题。UniHM 的物理引导动态细化模块（Section 3.4）以逐帧高斯-牛顿优化形式，融合接触能量 $E_{\text{contact}}$、生成先验 $E_{\text{gen}}$ 和时间先验 $E_{\text{time}}$（Eq 16），通过 Levenberg-Marquardt 阻尼求解关节增量（Eq 17），在保持语义意图的同时确保物理可行性。

**数据效率。** 基线方法通常依赖大规模遥操作或仿真数据。UniHM 仅利用 HOI 视频数据，通过 Dex-Retargeting 将 MANO 姿态映射至多种机器人手，并辅以能量优化提高物理一致性，显著降低了数据获取成本。

### 3. 关键证据强度评估

以下证据链支撑 UniHM 的方法论优势：

**主实验（Table 1, Table 2）。** 在 DexYCB 和 OakInk 两个数据集上，UniHM 在 MPJPE、FOL、FPL、FID 四项指标上全面超越 TM2T、MDM、FlowMDM 和 MotionGPT3。其中 Final Position Location Error（FPL）优势最为显著：DexYCB 上 12.15 vs MotionGPT3 的 19.32（降幅 37.1%），OakInk 上 19.86 vs 23.98（降幅 17.2%）。该指标直接反映末端位置的物理准确性，与物理优化模块的设计目标高度一致。置信度 0.98。

**消融实验（Table 4）。** 三个关键组件各自对性能贡献明确：去除深度输入后 MPJPE 从 61.40 升至 78.12（+27.2%），验证深度信息对精确空间交互的必要性；去除渐进掩码训练后 FID 从 31.24 升至 38.56，说明掩码策略对序列生成分布质量的影响；去除物理细化后 FPL 从 12.15 升至 16.22（+33.5%），证实后优化对减少穿透的关键作用。置信度 0.95。

**真实世界验证（Table 3）。** 跨具身实验中，UniHM 在抓取、放置、推拉、开合四项任务上的成功率（最高 65%）显著优于 MDM+Dex-Retargeting 和 MotionGPT3+Dex-Retargeting 组合。未见对象上的泛化能力保持良好（Pick & Place 35% vs 基线 25%），验证了统一码本的跨形态迁移能力。置信度 0.95。

**物理优化的鲁棒性（Figure B2）。** 非对称平滑接触核 $f(d)$ 相比欧氏距离对点云噪声更加鲁棒：即使在噪声输入下，$f(d)$ 核也能收敛到正确接触位置，而欧氏距离优化结果偏离真实表面。该可视化证据直接支撑了接触能量设计的合理性。置信度 0.9。

### 4. 适用边界与局限性

UniHM 在以下场景中存在已知局限：

1. **感知模态限制。** 框架依赖 RGB-D 视觉感知，未集成触觉或力反馈传感器。这意味着在需要精细接触力控制的任务（如捏取易碎物体、旋拧旋钮）中，系统无法感知或调节接触力，可能限制操作精度和安全性。

2. **物理模型的简化。** 物理优化中的接触能量为简化模型——采用点对面距离与非对称惩罚函数，未显式建模摩擦力、物体变形、或动态碰撞响应。因此不适用于高动态任务（如抛接、拍打）或强约束场景（如紧密配合装配）。

3. **单手操作范式。** 当前框架主要针对单手操作设计，尚未涵盖双手协同（如拧瓶盖、掰开物体）或工具使用（如使用螺丝刀、剪刀）等复杂操作场景。统一码本虽可扩展至多手，但训练与优化框架需重新设计。

4. **人体数据重定向误差。** 训练数据源自人体 HOI 视频，通过 Dex-Retargeting 映射至机器人手。该过程可能引入运动学误差，尤其当机器手自由度远少于人手时（如 Panda 手仅 1 自由度），语义保真度与物理可行性的平衡尚未充分验证。

5. **语言泛化的边界。** 虽然 UniHM 展示了开放指令泛化能力，但训练数据由 GPT-4o 从封闭集 HOI 数据集标注生成，语言多样性受限于原始动作分布。对未见的动词-名词组合或多步推理任务（如“把杯子放到左边，然后拉抽屉”）的泛化能力尚需进一步验证。

### 5. 开放问题

基于上述分析，以下研究方向值得关注：

1. **多模态感知融合。** 如何将触觉、力矩、温度等多模态感知信息融入 VLM 的序列生成过程，使系统能在真实世界中实现稳定的力控操作？一个可能路径是将触觉信号也量化为离散 token，与动作 token 在统一序列中联合建模。

2. **通用具身操作空间。** 统一的 VQ-VAE 码本是否可进一步扩展至其他末端执行器（如吸盘、平行夹爪、多指手）甚至移动基座，形成覆盖更广泛末端执行器形态的通用具身操作空间？这需要解决不同执行器在自由度、运动学约束和工作空间上的本质差异。

3. **全局轨迹优化。** 当前的物理优化采用单帧高斯-牛顿方法，逐帧独立求解，未考虑帧间耦合。能否设计更高效的全局规划方法（如微分规划、模型预测控制或整条轨迹的联合优化），以同时优化接触序列、时序分配和运动平滑性？

4. **语义保真度与物理可行性的权衡。** 基于人体视频的学习范式在存在显著形态差异时，如何保证生成动作既保持原始语义意图（如“捏”与“抓”的区分），又满足目标手部的物理约束？知识蒸馏过程中的语义信息保留机制值得深入研究。

5. **组合泛化与多步推理。** UniHM 展示的开放指令泛化能力是否可迁移到更复杂的语言组合（未见动词-名词对）和多步推理任务？这可能需要引入层次化任务规划器，将复杂指令分解为子任务序列，再由 HOI 生成器逐段执行。



## 原文 PDF

![[paperPDFs/ICLR_2026/UniHM_Unified_Dexterous_Hand_Manipulation_with_Vision_Language_Model.pdf]]
