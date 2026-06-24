---
title: "PAMotion: Physics-Aware Motion Generation for Full-Body Interaction with Multiple Objects"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PAMotion_Physics_Aware_Motion_Generation_for_Full_Body_Interaction_with_Multiple_Objects.pdf
aliases:
- PAMotion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过物体加速度揭示接触状态（自由运动或接触运动），并设计物理感知交互损失(L_phy)软约束物体加速与手/物距离的一致性。
primary_logic: 在日常生活慢动作交互中，物体加速度与重力对齐则无接触，偏离重力则必有直接或间接接触；将此观测形式化为一个动态激活的软约束损失，可在生成过程中自动纠正穿透和漂浮，提升物理合理性。
claims:
- 引入物理感知交互损失L_phy后，在两物体和三物体设置上FID和R-Precision均显著提升，并可视化了漂浮/穿透的减少。
- PAMotion在HIMO和ParaHome数据集上全面超越HIMO-Gen，特别是三物体场景FID从4.7712降至1.3763，大幅改善了物理一致性。
- HIMO (两物体) 上 FID = 0.8285
- HIMO (两物体) 上 R-Precision = 0.6914
---

# PAMotion: Physics-Aware Motion Generation for Full-Body Interaction with Multiple Objects

> [!tip] 核心洞察
> 在日常生活慢动作交互中，物体加速度与重力对齐则无接触，偏离重力则必有直接或间接接触；将此观测形式化为一个动态激活的软约束损失，可在生成过程中自动纠正穿透和漂浮，提升物理合理性。

| 字段 | 内容 |
|------|------|
| 中文题名 | PAMotion: 面向多物体全身交互的物理感知运动生成 |
| 英文题名 | PAMotion: Physics-Aware Motion Generation for Full-Body Interaction with Multiple Objects |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Di_PAMotion_Physics-Aware_Motion_Generation_for_Full-Body_Interaction_with_Multiple_Objects_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PAMotion |
| Dataset | HIMO, ParaHome |

> [!tip] 效果简介
> - HIMO (两物体) 上，FID 0.8285 vs 1.4811 (HIMO-Gen) (-0.6526)；R-Precision 0.6914 vs 0.6369 (HIMO-Gen) (+5.45%)。
> - HIMO (三物体) 上，FID 1.3763 vs 4.7712 (HIMO-Gen) (-3.3949)；R-Precision 0.6750 vs 0.5350 (HIMO-Gen) (+14.0%)；MM-Dist 3.7707 vs 5.0866 (HIMO-Gen) (-1.3159)。
> - ParaHome 上，FID 0.7962 vs 3.2398 (HIMO-Gen) (-2.4436)。

## 概述

**问题瓶颈**：现有扩散方法在生成多物体全身交互运动时，难以捕获复杂的物理约束，尤其是手与物体之间的接触关系，导致生成结果普遍存在物体漂浮、手部穿透等物理不一致问题。

**核心洞察**：在日常生活慢动作交互中，物体的加速度方向天然编码了接触状态——若物体加速度与重力对齐，则物体处于自由运动状态，无需手部接触；若加速度偏离重力，则必然存在直接或间接的手-物接触。将这一观测形式化为一个动态激活的软约束损失，可在扩散生成过程中自动纠正穿透与漂浮，显著提升物理合理性。

**方法定位**：**PAMotion** 是一个面向多物体全身交互的物理感知运动生成框架（CVPR 2026）。它采用粗到细的两阶段条件扩散架构：第一阶段生成身体躯干运动与物体平移，第二阶段精细化手部关节与物体旋转，并引入**物理感知交互损失**（Physics-Aware Interaction Loss）动态约束物体加速度与手-物距离的一致性。相比于基线方法 **HIMO-Gen**，PAMotion 的核心创新在于将物理先验显式嵌入扩散损失，而非仅依赖运动学监督。

**主要结果**：在 HIMO 数据集上，PAMotion 在两物体和三物体设置下均全面超越现有方法。三物体场景的 FID 从 4.7712 降至 1.3763，R-Precision 提升 14.0%；在 ParaHome 数据集上，FID 从 3.2398 降至 0.7962。消融实验证实，移除物理感知交互损失后所有指标一致下降，验证了该模块对生成质量与物理一致性的关键作用。

## 背景与动机

### 多物体全身交互生成的物理瓶颈

生成逼真的全身人体与多个物体的交互运动，是计算机视觉与图形学中长期存在的挑战。这项任务要求模型同时推理人体运动学、物体动力学以及二者之间精细的接触关系。近年来，扩散模型在人体运动生成领域取得了显著进展，但当场景从单人自由运动扩展到**多物体全身交互**时，现有方法暴露出根本性的物理一致性问题。

核心瓶颈在于：扩散模型本质上学习的是运动数据的统计分布，缺乏对物理规律的显式建模。当人体与多个物体发生接触时——例如一只手握住苹果、另一只手用刀切割——物体运动受到人手施加的接触力驱动，其加速度必然偏离重力方向。然而，现有方法无法捕获这种**接触状态与物体加速度之间的因果关联**，导致生成的运动中出现两类典型伪影：

- **漂浮（Floating）**：物体在无接触支撑的情况下悬停在空中，违背重力约束。
- **穿透（Penetration）**：手部穿入物体内部，违背刚体不可穿透性。

这些伪影在**HIMO-Gen**（HIMO ）等基线方法中普遍存在（Figure 1），严重损害了生成运动的物理可信度。

### 现有方法的缺口

当前面向人体-物体交互的运动生成方法大致可分为两类：基于运动合成的方法（如**IMoS** ）和基于扩散模型的方法（如**priorMDM** 、**HIMO-Gen**）。前者依赖显式的运动图或规则，难以泛化到复杂的多物体场景；后者虽然具备更强的生成能力，但其损失函数通常仅包含运动学层面的监督（如关节位置、速度、旋转的 L2 损失），完全忽视了物理一致性。

具体而言，**HIMO-Gen** 采用双分支扩散架构，同时预测人体和物体运动，但其训练目标仅最小化预测运动与真值之间的运动学误差。这种纯数据驱动的方式无法保证生成结果满足基本的物理约束——模型可以输出统计上“合理”但物理上不可能的运动序列。随着交互物体数量增加，物理不一致问题急剧恶化：在三物体设置中，HIMO-Gen 的 FID 高达 4.7712，生成质量显著退化。

### 核心洞察与动机

本工作的动机源于一个关键的物理观察：**在日常生活慢动作交互中，物体加速度可以作为接触状态的可靠代理信号**。具体而言：

- 若物体仅受重力作用（如自由落体的苹果），其加速度 $\hat{a} = g$，表明无接触发生；
- 若物体加速度偏离重力（$\hat{a} \neq g$），则必然存在人手施加的直接或间接接触力——例如手持苹果保持静止时 $\hat{a} = 0$，或刀切割苹果时加速度方向复杂多变。

这一观察揭示了将**物理先验**注入扩散生成过程的可行路径：通过监测生成过程中物体的加速度，动态判断接触状态，并对违背物理合理性的手-物距离施加惩罚。基于此，我们提出 **PAMotion**，一个物理感知的粗到细扩散框架，其核心创新在于将上述观察形式化为一个**动态激活的物理感知交互损失** $\mathcal{L}_{\mathrm{phy}}$，在生成过程中自动纠正漂浮和穿透，从而系统性地提升多物体交互运动的物理合理性。

## 核心创新

PAMotion 的核心创新在于将**物理感知交互建模**引入条件扩散框架，以解决现有多物体全身交互生成中普遍存在的漂浮、穿透等物理不一致问题。相较于以 **HIMO-Gen**（HIMO ）为代表的单阶段联合生成方法，PAMotion 在两个关键维度上进行了系统性改进。

### 1. 粗到细两阶段扩散生成框架

现有方法（如 HIMO-Gen）通常采用单阶段扩散联合预测所有运动变量，难以同时兼顾全局运动轨迹的语义对齐与局部手-物交互的物理合理性。PAMotion 将生成过程解耦为两个条件扩散阶段（Figure 2）：

- **粗阶段（Coarse Stage）**：生成人体躯干运动、全局平移以及物体的平移状态，建立文本对齐的全局交互骨架。
- **细阶段（Fine Stage）**：以粗阶段输出为条件，精细化生成手部关节运动和物体旋转状态，并在此阶段引入物理感知交互损失进行约束。

这种“先全局后局部”的生成策略，使得模型能够在保持整体运动质量的前提下，对手-物接触区域进行有针对性的物理优化。

### 2. 物理感知交互损失 L_phy

这是 PAMotion 最核心的算法创新。其关键洞察在于：**在日常生活慢动作交互中，物体加速度与重力的关系可以揭示接触状态——加速度与重力对齐时物体处于自由运动状态，偏离重力时则必然存在直接或间接的手-物接触**（Figure 3）。

基于此，PAMotion 将物体加速度作为接触状态的代理信号，设计了一个动态激活的软约束损失：

$$
\mathcal { L } _ { \mathrm { p h y } } = \mathbb { E } _ { t } \left[ \left| \log \left( \frac { d _ { t } } { \beta } \right) \right| \cdot \left| ( a _ { t } - g ) \cdot t \right| \right]
$$

该损失的因果机制如下：
- 当物体加速度 $a_t$ 接近重力 $g$ 时，$(a_t - g) \approx 0$，损失项自动“休眠”，不施加约束；
- 当物体加速度偏离重力时，损失被激活，惩罚手-物距离 $d_t$ 偏离合理接触阈值 $\beta$ 的程度，从而**同时抑制漂浮（距离过大）和穿透（距离过小）**。

与 HIMO-Gen 仅依赖运动学损失不同，$L_{phy}$ 首次在扩散生成过程中引入了对物理一致性的显式软约束，且无需额外的物理模拟器或后处理步骤。

### 3. 创新消融验证

消融实验直接验证了上述创新的有效性（Table 2, Table 3, Figure 6）。移除 $L_{phy}$ 后：
- 两物体设置中，FID 从 0.8285 升至 0.9046，R-Precision 从 0.6914 降至 0.6758；
- 三物体设置中，FID 从 1.3763 升至 1.5736，R-Precision 从 0.6750 降至 0.6312。

可视化结果进一步证实，$L_{phy}$ 的移除导致生成结果中漂浮和穿透伪影的明显回归，从而确立了物理感知损失作为 PAMotion 性能增益的核心因果杠杆。

## 整体框架

PAMotion 采用 **粗到细两阶段条件扩散框架**，将多物体全身交互生成分解为全局运动合成与局部物理细化两个级联阶段。该设计的核心动机在于：单阶段联合生成所有变量（如 **HIMO‑Gen** 的范式）难以同时捕获躯干‑物体的大范围位移与手‑物接触的精细物理约束，容易导致漂浮、穿透等物理不一致。

### 输入与条件编码

框架接受三类条件输入：
- **文本描述**：通过冻结的 **CLIP‑ViT‑B/32** 编码为潜在向量 $L$。
- **初始状态** $x_0$：包含首帧的人体姿态与物体位姿。
- **物体几何** $G$：使用 **BPS（Basis Point Set）** 表示编码物体形状，作为扩散模型的条件信号。

### 阶段 I：粗粒度全局交互合成

第一阶段以 $x_0$、$G$、$L$ 为条件，通过扩散模型生成 **文本对齐的粗粒度全局运动**，具体输出包括：
- 人体躯干运动：全局平移 $g_i$、身体关节位置 $J_{b,i}$ 与四元数 $Q_{b,i}$。
- 物体平移状态 $T_i^n$。

该阶段的监督信号由 **粗阶段总损失** $\mathcal{L}_{\mathrm{coarse}}$ 提供，综合了人体位置/速度损失 $\mathcal{L}_{\mathrm{pv}}$、四元数损失 $\mathcal{L}_{\mathrm{qv}}$、平移损失 $\mathcal{L}_{\mathrm{tv}}$、全局平移损失 $\mathcal{L}_{\mathrm{gv}}$ 以及物体间相对距离损失 $\mathcal{L}_{\mathrm{dist}}$（Eq. 4）。其中 $\mathcal{L}_{\mathrm{dist}}$ 显式维护多物体间的空间关系稳定性，防止物体漂移。

### 阶段 II：细粒度物理交互细化

第二阶段以粗阶段输出、$x_0$、$G$、$L$ 为条件，进一步生成 **手部精细关节运动** 与 **物体旋转状态**：
- 手部关节：$J_{h,i}$、$Q_{h,i}$。
- 物体旋转状态 $R_i^n$。

该阶段的核心创新在于引入 **物理感知交互损失** $\mathcal{L}_{\mathrm{phy}}$（Eq. 1），其与位置、四元数、旋转速度损失共同构成 **细阶段总损失** $\mathcal{L}_{\mathrm{fue}}$（Eq. 5）。$\mathcal{L}_{\mathrm{phy}}$ 通过物体加速度 $a_t$ 与重力 $g$ 的偏差动态激活：当 $a_t \neq g$ 时，物体必然处于直接或间接接触状态，此时损失函数惩罚手‑物距离 $d_t$ 违背合理接触范围的行为，从而 **联合抑制手部穿透与物体漂浮**（Fig. 3）。

### 数据流与模块关系

整体数据流可概括为：

```
文本 → CLIP编码 → L
物体几何 → BPS编码 → G
初始状态 x₀ ─────────────────┐
                              ▼
              ┌─────────────────────────────┐
              │  阶段 I：粗粒度全局交互合成    │
              │  输出：gᵢ, J_{b,i}, Q_{b,i}, T_iⁿ │
              │  监督：L_coarse               │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │  阶段 II：细粒度物理交互细化   │
              │  输出：J_{h,i}, Q_{h,i}, R_iⁿ  │
              │  监督：L_fine（含 L_phy）      │
              └─────────────────────────────┘
```

两阶段的级联设计使模型能够先建立全局运动的大致结构，再在局部细节层面注入物理约束，从而在 **HIMO** 和 **ParaHome** 数据集上均取得显著优于单阶段基线 **HIMO‑Gen** 的生成质量与物理一致性（Table 1, Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Di_PAMotion_Physics_Aw/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of PAMotion. PAMotion is a two-stage coarse-to-fine conditional diffusion framework. In the Coarse Motion Generation stage, the model predicts coarse, text-aligned global motion by generating global human body translation*

## 核心模块与公式推导

PAMotion 的核心设计围绕一个关键因果机制展开：**物体加速度是手-物接触状态的天然探针**。在日常生活慢动作交互中，若物体仅受重力作用（加速度与重力对齐），则手与物体无接触；一旦加速度偏离重力方向，必然存在直接或间接的手-物接触。PAMotion 将这一物理先验形式化为**物理感知交互损失（Physics-Aware Interaction Loss）**，并将其嵌入到**粗到细两阶段条件扩散框架**中，在生成过程中动态纠正漂浮和穿透伪影。

### 物理感知交互损失（L_phy）

物理感知交互损失是 PAMotion 的核心创新模块，其数学形式为：

$$
\mathcal { L } _ { \mathrm { p h y } } = \mathbb { E } _ { t } \left[ \left| \log \left( \frac { d _ { t } } { \beta } \right) \right| \cdot \left| ( a _ { t } - g ) \cdot t \right| \right]
$$

各变量含义如下：
- **$a_t$**：物体在时刻 $t$ 的加速度，由生成的运动序列计算得到。
- **$g$**：重力加速度向量。
- **$d_t$**：手部关键点与物体表面之间的最短距离。
- **$\beta$**：接触距离阈值，当 $d_t \leq \beta$ 时视为接触状态。
- **$t$**：时间变量，用于对加速度偏差进行时间加权。

该损失的设计逻辑与三个典型交互场景（见 Figure 3）对应：
1. **自由运动状态**：物体仅受重力影响，$a_t \approx g$，此时 $|(a_t - g) \cdot t| \approx 0$，损失项被自动抑制，模型不施加接触约束。
2. **手持静止状态**：物体被手稳定握持，加速度趋近于零（$a_t \approx 0$），$|(a_t - g) \cdot t|$ 显著激活，此时若手-物距离 $d_t$ 偏离阈值 $\beta$，$|\log(d_t/\beta)|$ 项将施加惩罚，迫使手与物体保持合理接触，抑制**漂浮**。
3. **交互运动状态**：物体受手部施力，加速度偏离重力（$a_t \neq g$），损失同样被激活，通过手-物距离约束确保接触一致性，抑制**穿透**。

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Di_PAMotion_Physics_Aw/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of Physics-Aware Motion Modeling. Object acceleration aˆ as an indicator of human-object contact state. Free-Motion State: (a) the apple is influenced only by gravity*

损失函数中的对数距离项 $|\log(d_t/\beta)|$ 具有对称惩罚特性：当 $d_t \ll \beta$（穿透）或 $d_t \gg \beta$（漂浮）时均产生较大梯度，实现对两类物理不一致问题的联合抑制。时间加权因子 $t$ 则确保加速度偏差在运动序列中的累积效应得到合理考虑。

### 两阶段条件扩散框架

PAMotion 采用粗到细的两阶段生成策略（见 Figure 2），将复杂的全身多物体交互生成分解为两个可控子任务。

**粗阶段（Coarse Global Interaction Synthesis）** 负责生成文本对齐的全局运动骨架，包括人体躯干运动（身体关节位置 $J_{b,i}$、四元数 $Q_{b,i}$）、全局平移 $g_i$ 以及所有物体的平移状态 $T_i^n$。该阶段以初始状态 $x_0$、物体几何编码 $G$ 和文本嵌入 $L$ 为条件，采用条件扩散模型进行生成。粗阶段的总损失函数为：

$$
\mathcal { L } _ { \mathrm { c o a r s e } } = \mathcal { L } _ { \mathrm { p v } } + \mathcal { L } _ { \mathrm { q v } } + \mathcal { L } _ { \mathrm { t v } } + \mathcal { L } _ { \mathrm { g v } } + \lambda _ { 0 } \mathcal { L } _ { \mathrm { d i s t } }
$$

其中：
- **$\mathcal{L}_{\mathrm{pv}}$**（身体关节位置与速度损失）：

$$
\mathcal { L } _ { \mathrm { p v } } = \sum _ { i = 1 } ^ { T } { \Vert \boldsymbol { J } _ { b , i } - \hat { J _ { b , i } } \Vert _ { 2 } ^ { 2 } } + \sum _ { i = 1 } ^ { T } { \Vert \dot { J _ { b , i } } - \hat { J _ { b , i } } \Vert _ { 2 } ^ { 2 } }
$$

该项同时监督身体关节位置及其一阶导数，确保空间对齐与时间平滑性。

- **$\mathcal{L}_{\mathrm{dist}}$**（物体间相对距离损失）：

$$
\mathcal { L } _ { \mathrm { d i s t } } = \sum _ { i = 1 } ^ { T } \| d _ { m n , i } - \hat { d } _ { m n , i } \| _ { 2 } ^ { 2 }
$$

该项维护多个物体之间的空间关系稳定性，防止物体间出现不合理的相对位移。

- **$\mathcal{L}_{\mathrm{qv}}$、$\mathcal{L}_{\mathrm{tv}}$、$\mathcal{L}_{\mathrm{gv}}$**：分别为四元数旋转损失、物体平移损失和全局平移损失，共同构成粗阶段的运动学监督。

**细阶段（Fine-Grained Physical Interaction Generation）** 以粗阶段输出为条件，精细化生成手部关节运动（$J_{h,i}$、$Q_{h,i}$）和物体旋转状态 $R_i^n$。该阶段的核心特征是引入了物理感知交互损失，总损失为：

$$
\mathcal { L } _ { \mathrm { f u e } } = \mathcal { L } _ { \mathrm { p v } } ^ { r } + \mathcal { L } _ { \mathrm { q v } } ^ { r } + \mathcal { L } _ { \mathrm { r v } } ^ { r } + \lambda _ { 1 } \mathcal { L } _ { \mathrm { p h y } }
$$

其中 $\mathcal{L}_{\mathrm{pv}}^{r}$、$\mathcal{L}_{\mathrm{qv}}^{r}$、$\mathcal{L}_{\mathrm{rv}}^{r}$ 分别为细阶段的位置、四元数和旋转速度细化损失，$\lambda_1$ 为物理损失的权重系数。$\mathcal{L}_{\mathrm{phy}}$ 在此阶段动态激活，根据物体加速度与重力的偏差自动调整手-物接触约束强度，从物理层面保证生成交互的合理性。

### 条件编码模块

PAMotion 使用两个编码器将多模态条件映射到扩散模型的潜在空间：
- **文本编码器**：采用冻结的 CLIP-ViT-B/32 模型将条件文本映射为潜在向量 $L$。
- **物体几何编码器**：采用基点集（Basis Point Set, BPS）表示对物体几何 $G$ 进行编码，捕获物体的空间形状信息。

这两个编码器的输出与初始状态 $x_0$ 共同构成扩散模型的条件输入，贯穿粗阶段和细阶段的全过程。

## 实验与分析

### 主实验结果

PAMotion在HIMO和ParaHome两个数据集上均进行了系统评估，并与当前主流方法进行了全面对比。在HIMO数据集的两物体设置中，PAMotion在FID指标上达到**0.8285**，相较基线方法**HIMO-Gen**（FID=1.4811）降低了0.6526，降幅达44%；在R-Precision上达到**0.6914**，较HIMO-Gen（0.6369）提升了5.45个百分点。这表明PAMotion生成的交互运动不仅分布更接近真实数据，且与文本描述的语义对齐程度也更强（见 Table 1）。

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Di_PAMotion_Physics_Aw/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison under two-object and three-object settings on the HIMO dataset. PAMotion outperforms all state-of-theart methods on nearly all metrics—except MM-Dist in the two-object case—and achieves a clear performance margin in the three-object case. These results demonstrate PAMotion’s strong ability to model complex human–object interactions. ’↑’: higher is better, ’↓’: lower is better, ’→’: closer to ground truth is better*

在三物体场景中，PAMotion的优势更为显著。FID从HIMO-Gen的**4.7712**大幅降至**1.3763**，降幅超过70%；R-Precision从0.5350提升至**0.6750**，提升幅度达14.0个百分点；MM-Dist也从5.0866降至**3.7707**，缩小了与真实分布的距离。三物体场景涉及更复杂的多物体协调与接触切换，PAMotion在该场景下的显著提升直接验证了物理感知交互损失对复杂物理约束的建模能力（见 Table 1）。

在ParaHome数据集上，PAMotion同样保持了明显优势。FID从HIMO-Gen的3.2398降至**0.7962**，R-Precision从0.5909提升至**0.6364**，在所有指标上均实现了对基线的超越（见 Table 4）。ParaHome数据集包含更丰富的日常交互动作，该结果进一步证明了PAMotion在不同数据分布下的泛化能力。

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Di_PAMotion_Physics_Aw/figures/010_Table_4.jpg]]
*Table 4: Quantitative comparison on the ParaHome dataset. PAMotion consistently outperforms the baseline method HIMO-Gen across all metrics. In particular, PAMotion achieves a significantly lower FID score (0.7962 vs. 3.2398), demonstrating its superior generation quality*

需要注意的是，在两物体设置的MM-Dist指标上，PAMotion略逊于HIMO-Gen。该指标衡量生成运动与真实运动在特征空间中的多模态距离，PAMotion在该指标上的微弱劣势可能源于物理约束的引入对运动多样性的轻微抑制，但考虑到FID和R-Precision的大幅领先，这一权衡是可接受的。

### 消融实验

为验证物理感知交互损失 $\mathcal{L}_{\mathrm{phy}}$ 的核心作用，作者进行了消融实验。移除 $\mathcal{L}_{\mathrm{phy}}$ 后，在两物体设置中FID从**0.8285**恶化至0.9046，R-Precision从**0.6914**降至0.6758；在三物体设置中FID从**1.3763**升至1.5736，R-Precision从**0.6750**降至0.6312。两个设置下所有指标的一致性退化表明，$\mathcal{L}_{\mathrm{phy}}$ 对生成质量和语义对齐均有实质贡献（见 Table 2 和 Table 3）。

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Di_PAMotion_Physics_Aw/figures/008_Table_2.jpg]]
*Table 2: Ablation study of*

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Di_PAMotion_Physics_Aw/figures/009_Table_3.jpg]]
*Table 3: Ablation study of*

定性可视化进一步揭示了 $\mathcal{L}_{\mathrm{phy}}$ 的物理纠正效果。如 Figure 6 所示，移除物理损失后生成的运动中出现了明显的手部穿透物体和物体漂浮现象，而完整模型则能生成手-物接触紧密、物体运动符合物理直觉的交互序列。这验证了 $\mathcal{L}_{\mathrm{phy}}$ 通过动态激活机制——当物体加速度偏离重力时惩罚不合理的手-物距离——有效抑制了漂浮和穿透这两类典型的物理不一致问题。

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Di_PAMotion_Physics_Aw/figures/011_Figure_6.jpg]]
*Figure 6: Ablation Study of*

### 失败模式与局限性

尽管PAMotion在整体指标上表现优异，论文也坦诚地展示了失败案例。如 Figure 7 所示，在“抓取灯泡”的场景中，虽然手部与灯泡发生了交互，但抓取姿势在物理上并不合理。这一失败模式揭示了当前方法的根本局限：$\mathcal{L}_{\mathrm{phy}}$ 仅从物体加速度与手-物距离的一致性角度约束接触状态，缺乏对抓取姿势本身的显式建模。模型不知道“抓取灯泡”应该用指尖捏住而非手掌包裹，这种语义-物理的双重缺失需要引入更结构化的抓取先验才能解决。

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Di_PAMotion_Physics_Aw/figures/007_Figure_7.jpg]]
*Figure 7: Failure Case on HIMO dataset. Although the hand interacts with the bulb, the grasp pose is physically implausible*

此外，论文指出的其他局限包括：物理感知损失的核心假设——通过物体加速度偏离重力来判定接触状态——适用于日常慢动作交互，但在高动态或涉及复杂外力的场景（如投掷、击打）中可能失效；当前仅考虑手部与物体的接触，忽略了身体其他部位（如躯干倚靠、脚部踢动）的接触建模；方法依赖大量运动捕捉数据，向多人-多物交互场景的扩展尚未探索。

### 关键图表总结

- **Table 1**：HIMO数据集主结果，PAMotion在两物体和三物体设置上全面超越HIMO-Gen等基线，三物体场景FID降幅超70%。
- **Table 2 & Table 3**：$\mathcal{L}_{\mathrm{phy}}$ 消融实验，移除后FID和R-Precision在两个设置下均一致退化，证实物理损失的关键作用。
- **Table 4**：ParaHome数据集对比，PAMotion在所有指标上优于HIMO-Gen，FID从3.2398降至0.7962。
- **Figure 6**：消融可视化，移除 $\mathcal{L}_{\mathrm{phy}}$ 后出现穿透和漂浮，完整模型生成物理合理的交互。
- **Figure 7**：失败案例，灯泡抓取姿势物理不合理，暴露缺乏显式抓取约束的局限。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openaccess_thecvf_com_content_CVPR2026_html_Di_PAMotion_Physics_Aw/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative Comparison on HIMO dataset [53]. Our method PAMotion produces physically plausible human–object interactions, while the baseline method HIMO-Gen [53] often exhibits floating or penetration artifacts*

## 方法谱系与知识库定位

### 与基线方法的关系

PAMotion 的生成架构直接继承自 **HIMO-Gen**（，HIMO 数据集原生基线）的双分支扩散范式，即同时预测人体运动与物体运动。但 HIMO-Gen 采用单阶段联合生成所有变量，缺乏对物理一致性的显式建模，导致生成结果中频繁出现手部穿透物体或物体漂浮等伪影（Figure 1 定性对比）。PAMotion 在此基础上引入两个关键改造：

1. **粗到细两阶段扩散**：将生成过程解耦为“全局躯干/物体平移”与“精细手部/物体旋转”两个阶段，使模型先建立整体空间布局，再在局部细化中施加物理约束，从而降低高维联合生成的优化难度。
2. **物理感知交互损失**：这是 PAMotion 区别于所有现有方法的核心创新。此前的方法（包括 HIMO-Gen、**priorMDM** 、**IMoS** ）仅依赖运动学损失（如关节位置、速度、四元数损失）监督生成，完全忽略了物体运动应遵循的基本物理规律。PAMotion 首次将物体加速度与手-物接触状态的因果关系形式化为可微损失，在生成过程中动态纠正物理不一致。

在对比实验方面，Table 1 显示 PAMotion 在两物体和三物体设置上全面超越 HIMO-Gen：三物体场景下 FID 从 4.7712 降至 1.3763（降幅 71.2%），R-Precision 从 0.5350 提升至 0.6750（提升 14.0%），MM-Dist 从 5.0866 降至 3.7707。ParaHome 数据集上的跨域泛化实验（Table 4）进一步验证了方法的鲁棒性，FID 从 3.2398 降至 0.7962。

### 适用边界与关键假设

PAMotion 的物理感知损失建立在以下核心假设之上，这些假设定义了方法的有效边界：

- **慢动作交互假设**：$L_{phy}$ 通过判断物体加速度是否偏离重力（$a_t \neq g$）来推断接触状态。这一逻辑在日常生活慢动作场景（如拿起杯子、切水果）中成立，但在高动态场景（如投掷、击打）中，物体即使无接触也可能因惯性而偏离重力加速度，导致损失函数误判接触状态。论文明确承认这一局限。
- **手-物接触主导假设**：当前物理损失仅考虑手部与物体的接触关系，忽略身体其他部位（如躯干、腿部）可能与物体发生的接触。对于“用身体推门”或“用脚踢球”等场景，模型缺乏相应的物理约束。
- **刚体运动假设**：物体运动以平移和旋转参数化，不涉及形变或流体动力学，因此不适用于衣物折叠、液体倾倒等需要模拟柔性体或流体的交互。

### 局限与开放问题

**已知局限**：

1. **抓取姿势物理合理性不足**：如 Figure 7 所示，模型生成的抓取姿势可能在几何上接触物体但生物力学上不合理（如灯泡案例中手部关节角度违反人体自然约束）。这是因为 $L_{phy}$ 仅约束手-物距离与物体加速度的一致性，不包含抓取稳定性或手部关节限位等显式约束。
2. **数据依赖**：方法依赖大规模运动捕捉数据（HIMO、ParaHome），对数据集中未覆盖的物体形状和交互类型的泛化能力未经充分验证。
3. **多人-多物扩展未探索**：当前框架仅考虑单人与多物体的交互，向多人协作或竞争场景的扩展需要解决人体间物理约束和社交协调等新挑战。

**开放问题**：

- **整合预训练抓取模型**：论文提出可将 **GraspNet** 等预训练抓取模型作为先验，在精细阶段规约抓取姿势的合理性，同时确保双手协调和手间一致性。这需要设计一种机制，使抓取先验与扩散生成过程兼容，而非简单的后处理修正。
- **扩展到多人-多物场景**：多人交互涉及人体间相对运动、力传递和社会意图建模，当前基于加速度的物理损失框架能否直接推广尚待研究。
- **高动态场景的物理建模**：对于投掷、击打等涉及大加速度和瞬时接触力的场景，需要更复杂的物理模型（如引入接触力估计或脉冲动力学）来替代当前的准静态假设。

### 知识库定位

PAMotion 处于**物理感知人体运动生成**与**多物体交互建模**的交叉点。相较于纯运动学驱动的扩散生成方法（如 MDM、priorMDM），它首次将牛顿力学层面的物体加速度约束引入生成过程；相较于基于强化学习或轨迹优化的物理仿真方法，它保留了扩散模型的表达力和数据驱动优势，同时以软约束形式嵌入物理知识，避免了刚性物理引擎的收敛困难。这一“物理软约束 + 扩散生成”的范式为后续研究提供了一个可扩展的框架：物理知识不再需要作为硬性仿真步骤，而是可以通过可微损失灵活注入生成过程。

## 原文 PDF

![[paperPDFs/CVPR_2026/PAMotion_Physics_Aware_Motion_Generation_for_Full_Body_Interaction_with_Multiple_Objects.pdf]]
