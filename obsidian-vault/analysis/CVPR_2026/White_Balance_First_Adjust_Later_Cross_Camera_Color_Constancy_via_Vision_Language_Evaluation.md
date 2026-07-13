---
title: "White-Balance First, Adjust Later: Cross-Camera Color Constancy via Vision-Language Evaluation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/White_Balance_First_Adjust_Later_Cross_Camera_Color_Constancy_via_Vision_Language_Evaluation.pdf
project_link: null
code_link: "https://github.com/NothingIknow/VLM-CC"
aliases:
- VC
- WBFALCCCCVLE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将颜色恒常性重新定义为迭代语义反馈过程：先用当前估计白平衡并转换到伪sRGB，再通过VLM评估残差颜色偏向（红/绿/蓝），并触发光照方向更新，从而绕过直接RGB回归的相机依赖。
primary_logic: 通过在白平衡后的伪sRGB图像上利用VLM的语义先验进行定性颜色评估（而非数值回归），使迭代校正能够利用对象内在颜色知识，实现稳健的跨相机泛化。
claims:
- VLM-CC在多个跨相机数据集上取得最优性能，尤其最差25%误差显著降低。
- 迭代离散推理策略优于一步或迭代数值方法，验证了分类反馈优于连续回归。
- 语义线索和微调对稳定估计至关重要：随机先验导致性能下降，未微调的VLM几乎失效。
- "Gehler-Shi (leave-one-out, 训练: Cube+, NUS-8, Intel-TAU) 上 Mean angular error (°) = 1.52"
---

# White-Balance First, Adjust Later: Cross-Camera Color Constancy via Vision-Language Evaluation

> [!tip] 核心洞察
> 通过在白平衡后的伪sRGB图像上利用VLM的语义先验进行定性颜色评估（而非数值回归），使迭代校正能够利用对象内在颜色知识，实现稳健的跨相机泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 先白平衡后调整：基于视觉-语言评价的跨相机颜色恒常性 |
| 英文题名 | White-Balance First, Adjust Later: Cross-Camera Color Constancy via Vision-Language Evaluation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.19613) · [Code](https://github.com/NothingIknow/VLM-CC) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VLM-CC |
| Dataset | Gehler-Shi, NUS-8, Cube+ |

> [!tip] 效果简介
> - Gehler-Shi (leave-one-out, 训练: Cube+, NUS-8, Intel-TAU) 上，Mean angular error (°) 1.52 vs 2.23 (CCMNet) (-0.71)。
> - NUS-8 (leave-one-out, 训练: Gehler-Shi, Cube+, Intel-TAU) 上，Mean angular error (°) 1.83 vs 2.32 (CCMNet) (-0.49)。
> - Cube+ (leave-one-out, 训练: Gehler-Shi, NUS-8, Intel-TAU) 上，Mean angular error (°) 1.51 vs 1.68 (CCMNet) (-0.17)。

## 概要

**问题瓶颈**：现有学习型颜色恒常性方法大多直接回归光照，在跨相机场景中因传感器光谱响应的差异导致相机特定过拟合，且缺乏语义理解来评估校正质量。统计方法（如 Gray-World）虽具备相机无关性，但精度有限；深度学习方法（如 CCMNet）在已知相机上表现优异，跨相机泛化时性能显著退化。

**核心思路**：VLM-CC 将颜色恒常性重新定义为**迭代语义反馈过程**——先用当前估计对 RAW 图像白平衡并转换到伪 sRGB 空间，再通过视觉-语言模型（VLM）评估残差颜色偏向（红/绿/蓝），并据此触发光照方向的离散更新。这一范式绕过了直接 RGB 回归对相机特性的依赖，转而利用 VLM 对物体内在颜色的语义先验来指导校正。

**方法定位**：VLM-CC 属于**基于语义反馈的迭代白平衡框架**，区别于传统的统计假设方法（Gray-World, Buchsbaum 1980）和端到端回归方法（FFCC, Barron & Tsai CVPR 2017; C5, Afifi et al. ICCV 2021; CCMNet, Kim et al. ICCV 2025）。其关键创新在于：(1) 在白平衡后的伪 sRGB 图像上进行定性颜色评估而非数值回归；(2) 输出离散色偏类别触发方向性更新，而非连续光照值；(3) 通过 LoRA 微调使 VLM 获得稳定的色偏判断能力。

**主要结果**：VLM-CC 在多个跨相机数据集上取得最优性能——Gehler-Shi 上平均角度误差 1.52°（CCMNet 为 2.23°），NUS-8 上 1.83°（CCMNet 为 2.32°），Cube+ 上 1.51°（CCMNet 为 1.68°）。消融实验证实，迭代离散推理策略优于一步或迭代数值方法，语义先验和 VLM 微调对稳定估计至关重要。代码已开源（https://github.com/NothingIknow/VLM-CC）。

颜色恒常性（Color Constancy）是计算摄影中的基础任务，旨在从相机记录的原始RAW图像中消除全局光源颜色偏差，恢复场景在标准白光下的真实色彩。该问题可形式化为单一全局光照模型：原始图像 $I$ 的每个像素可表示为该像素在白光下的真实颜色 $W$ 与全局光照颜色 $\ell$ 的逐通道乘积，即 $I = W \odot \ell$。颜色恒常性的目标是从观测到的 $I$ 中估计光照 $\hat{\ell}$，进而通过逐通道除法恢复白平衡图像 $W = I \oslash \hat{\ell}$。

### 现有方法的瓶颈

传统颜色恒常性方法可分为两类。统计方法，如 **Gray-World**（Buchsbaum, J. Franklin Inst., 1980），基于低级颜色统计假设（如场景平均反射率为灰色）进行光照估计，计算简单但精度有限。学习方法则直接从RAW图像回归连续光照向量，代表工作包括 **FFCC**（Barron and Tsai, CVPR 2017）、**SIIE**（Afifi and Brown, BMVC 2019）、**C5**（Afifi et al., ICCV 2021）以及最新的 **CCMNet**（Kim et al., ICCV 2025）等。

然而，现有学习方法存在一个核心瓶颈：**直接回归光照向量的范式导致模型对训练相机的传感器特性产生过拟合**。不同相机的光谱敏感度曲线各异，同一场景在不同相机上的RAW图像呈现不同的颜色分布。当模型在特定相机数据上学习从RAW到光照的端到端映射时，其习得的特征高度依赖于该相机的传感器反应模式。在跨相机场景中——即训练和测试使用不同相机拍摄的图像时——这种相机特定的过拟合导致性能显著下降。此外，这些方法缺乏对场景内容的语义理解，无法利用“草地应为绿色、天空应为蓝色”等对象内在颜色知识来评估白平衡校正的质量。

### 本文动机与核心思路

针对上述瓶颈，本文提出 **VLM-CC**，将颜色恒常性从根本上重新定义为**迭代语义反馈过程**，而非单步数值回归。其核心调控旋钮（causal knob）在于：**先白平衡，后评估，再调整**——在每次迭代中，先用当前的光照估计对RAW图像进行白平衡，并通过相机颜色矩阵转换到伪sRGB空间；然后利用视觉-语言模型（VLM）对白平衡后的图像进行定性的残差颜色偏向评估（预测主导色偏为红、绿或蓝），而非直接回归连续光照值；最后根据评估结果在色度空间中沿相应方向更新光照估计，形成闭环迭代直至收敛。

这一范式的关键洞察在于：**通过在白平衡后的伪sRGB图像上利用VLM的语义先验进行定性颜色评估，使迭代校正能够利用对象内在颜色知识，从而绕过直接RAW回归带来的相机依赖，实现稳健的跨相机泛化**。VLM在预训练过程中习得了丰富的对象颜色先验（如香蕉是黄色的、雪是白色的），这些语义线索为判断当前白平衡结果是否存在残余色偏提供了强有力的依据，而这种依据不依赖于特定相机的传感器特性。

## 核心方法与创新机理

### 问题瓶颈的重定义

传统学习型颜色恒常性方法（如 **CCMNet** (Kim et al., ICCV 2025)、**C5** (Afifi et al., ICCV 2021)）遵循“从原始图像直接回归连续光照向量”的范式。这一范式在跨相机场景中暴露了根本性缺陷：不同相机的传感器光谱响应差异导致相同的场景光照在 RAW 域呈现不同的数值分布，直接回归模型因此过拟合到训练相机的特定响应特性，缺乏对场景语义的理解来评估校正质量。

VLM-CC 重新诊断了这一瓶颈：问题不在于回归模型的容量不足，而在于**回归发生在错误的表征空间**。RAW 域的像素值与相机硬件强耦合，使得模型难以习得跨相机的光照不变表征。

### 核心调控变量：评估-更新的语义反馈闭环

VLM-CC 的核心创新在于将颜色恒常性从“单步数值回归”重构为“迭代语义反馈过程”。这一重构引入了四个关键的 **changed slots**：

**1. 光照估计范式：从单步回归到迭代语义反馈**

基线方法（CCMNet、C5、**SIIE** (Afifi and Brown, BMVC 2019)、**FFCC** (Barron and Tsai, CVPR 2017)）均采用单次前向推理直接输出光照向量。VLM-CC 将其替换为最多 20 步的迭代循环：每一步用当前估计白平衡图像，交由 VLM 评估残差色偏，再根据反馈更新光照方向。这一范式转变使得校正过程能够利用语义信息逐步逼近真值，而非依赖一次性的数值预测。

**2. 输入表示：从 RAW 域到伪 sRGB 语义空间**

基线方法直接处理原始相机 RAW 图像。VLM-CC 在每次迭代中先将 RAW 图像用当前光照估计进行白平衡（$W^{(t)} = I \oslash \hat{\ell}^{(t)}$），再通过相机颜色矩阵映射到伪 sRGB 空间（$I_{\mathrm{srgb}}^{(t)} = M_{\mathrm{x \to s}} M_{\mathrm{c \to x}} W^{(t)}$）。这一转换的关键在于：sRGB 空间是 VLM 预训练所使用的色彩空间，语义先验（如“天空是蓝色的”“草地是绿色的”）在该空间内才具有稳定的参照意义。同时，相机颜色矩阵 $M_{\mathrm{c \to x}}$ 承担了传感器响应差异的归一化角色，使后续的语义评估与相机硬件解耦。

**3. 语义信息利用：从无显式语义到 VLM 对象颜色先验**

基线方法仅依赖低级颜色统计或深度特征，缺乏对场景内容的显式理解。VLM-CC 引入经 LoRA 微调的 VLM，在每次迭代中执行双重语义任务：
- **颜色先验提取**：从初始白平衡图像中识别可靠对象（如草坪、天空、白色墙壁），提取其内在颜色作为粗粒度先验；
- **残差色偏预测**：结合当前伪 sRGB 图像和上述颜色先验，判断主导残余光色。

消融实验证实了这一 slot 的关键性：使用随机颜色先验替代语义先验时，平均角度误差从 1.52° 升至 1.93°；打乱图像空间结构后，最差 25% 误差从 3.29° 大幅增至 5.27°，表明空间连贯的语义线索对困难样本尤为关键。

**4. 输出粒度：从连续 RGB 值到离散三色分类**

基线方法输出连续 RGB 光照值，在跨相机场景中易受数值不稳定性影响。VLM-CC 将输出空间离散化为 {red, green, blue} 三类，每次迭代仅预测主导残余光色的方向类别（$\boldsymbol{c}^{(t)} \in \{\mathrm{red}, \mathrm{green}, \mathrm{blue}\}$），并据此在色度空间中执行方向性旋转更新（$\hat{\ell}^{(t+1)} = \mathrm{Normalize}(\cos A_t u^{(t)} + \sin A_t v^{(t)})$）。消融实验直接验证了这一选择的优势：迭代离散推理（Mean 1.52°）显著优于一步数值回归（Mean 2.75°）和迭代数值回归（Mean 2.54°），证明分类反馈比连续回归更匹配 VLM 的语义判断能力，同时避免了跨相机场景中的数值漂移。

### 创新路径的因果逻辑

上述四个 slot 形成了完整的因果闭环：**sRGB 转换**将问题从相机相关的 RAW 域迁移到语义可理解的色彩空间 → **VLM 语义先验**提供对象内在颜色的稳定参照 → **离散分类输出**匹配 VLM 的定性判断优势，避免数值不稳定性 → **迭代反馈**使每次更新都能利用前一步的校正结果逐步收敛。这一闭环的核心洞察在于：**通过在白平衡后的伪 sRGB 图像上利用 VLM 的语义先验进行定性颜色评估（而非数值回归），使校正过程能够利用对象内在颜色知识，实现稳健的跨相机泛化。**

### 问题设定与核心思路

传统学习型颜色恒常性方法直接从原始相机图像回归连续光照向量，在跨相机场景中因不同传感器的光谱响应差异导致相机特定过拟合，且缺乏语义理解来评估校正质量。**VLM-CC** 将颜色恒常性重新定义为**迭代语义反馈过程**：先用当前估计光照对原始图像进行白平衡并转换到伪sRGB空间，再通过视觉-语言模型（VLM）评估残差颜色偏向，触发光照方向的更新，从而绕过直接RGB回归的相机依赖。

该方法基于单一全局光源假设，将原始图像 $I$ 建模为白平衡后图像 $W$ 与全局光照 $\ell$ 的逐通道乘积：

$$I = W \odot \ell$$

光照估计的目标是从观测图像 $I$ 中恢复 $\hat{\ell} = f(I)$。VLM-CC 的核心创新在于不直接回归数值，而是利用VLM的语义先验进行**定性颜色评估**——每次迭代仅预测主导残差色偏的离散类别（红/绿/蓝），并据此在色度空间中执行方向性光照更新。

### 整体Pipeline

VLM-CC 的推理流程（Figure 2）由五个核心模块串联成闭环，以迭代方式逐步精化光照估计：

![[assets/figures/papers/paper_list_l2217_https_arxiv_org_abs_2605_19613/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed framework. Given a raw input image, we first apply white balance using the current illuminant estimate and convert the result to sRGB for VLM processing. A pretrained VLM extracts semantic color priors from the pseudo-sRGB image, identifying objects whose inherent colors are reliable under neutral light. A LoRA-finetuned VLM then predicts the dominant residual light color label (red, green, or blue) based on these priors. The illuminant estimate is updated accordingly in chromaticity space and fed back into the next iteration. This iterative semantic feedback loop gradually refines the illumination direction until convergence*

1. **初始化模块（Gray-World）**  
   利用 Gray-World 假设（Buchsbaum, J. Franklin Inst., 1980）提供初始光照估计，加速收敛：
   $$\hat{\ell}^{(1)} = \mathrm{Normalize}\big(\frac{1}{|\Omega|} \sum_{x \in \Omega} I(x)\big)$$

2. **白平衡与sRGB转换**  
   在第 $t$ 次迭代，用当前估计 $\hat{\ell}^{(t)}$ 对原始图像 $I$ 进行逐通道除法得到白平衡图像：
   $$W^{(t)} = I \oslash \hat{\ell}^{(t)}$$
   随后通过相机颜色矩阵 $M_{c \to x}$（相机空间→XYZ）和标准转换矩阵 $M_{x \to s}$（XYZ→线性sRGB）映射到伪sRGB空间：
   $$I_{\mathrm{srgb}}^{(t)} = M_{\mathrm{x \to s}} M_{\mathrm{c \to x}} W^{(t)}$$
   这一转换将不同相机的RAW数据统一到语义模型可理解的色彩空间，是跨相机泛化的关键。

3. **颜色先验提取（预训练VLM）**  
   从初始白平衡后的伪sRGB图像中，利用预训练VLM识别场景中的可靠对象及其内在颜色（如“草地是绿色的”、“天空是蓝色的”），形成结构化的颜色先验列表。该先验在后续所有迭代中共享，为残差色偏判断提供稳定的语义锚点。

4. **残差光色估计（LoRA微调VLM）**  
   结合当前伪sRGB图像 $I_{\mathrm{srgb}}^{(t)}$ 和颜色先验，LoRA微调的VLM预测主导残余光色的离散标签：
   $$\boldsymbol{c}^{(t)} = \mathrm{VLM}(\boldsymbol{I}_{\mathrm{srgb}}^{(t)}, \mathrm{prompt}), \quad \boldsymbol{c}^{(t)} \in \{\mathrm{red}, \mathrm{green}, \mathrm{blue}\}$$
   选择离散分类而非连续回归，是因为VLM在类别判断上更稳定，避免了数值回归的不稳定性（消融实验证实：迭代离散推理 Mean 1.52° vs. 迭代数值 Mean 2.54°）。

5. **光照更新与收敛控制**  
   根据预测的色偏方向 $\boldsymbol{c}^{(t)}$，在RGB空间中将当前归一化光照方向 $u^{(t)}$ 旋转步角 $A_t$，向预测色偏的垂直分量方向 $v^{(t)}$ 移动：
   $$\hat{\ell}^{(t+1)} = \mathrm{Normalize}\big(\cos A_t u^{(t)} + \sin A_t v^{(t)}\big)$$
   当首次出现三种不同色偏标签时，判定为粗收敛信号，将所有剩余步角减半进入精化阶段。推理最多执行20步。最终取最后三次估计的归一化几何平均以抑制收敛后的小幅振荡：
   $$\hat{\ell}^{*} = \operatorname{Normalize}\big((\hat{\ell}^{(t)} \odot \hat{\ell}^{(t-1)} \odot \hat{\ell}^{(t-2)})^{1/3}\big)$$

### 训练流程

训练阶段（Figure 3）与推理共享相同的颜色先验提示策略。给定原始图像，首先在相机色彩空间中进行光色增强，转换到sRGB后由LoRA微调的VLM预测主导残差光色标签。监督信号来自真实光照方向，损失函数为标准因果语言建模损失，仅作用于预测的色偏token（red/green/blue）：

$$\mathcal{L}_{\mathrm{LM}} = -\sum_{t} \log p_{\theta}(y_{t} \mid y_{<t}, I_{\mathrm{srgb}}, \mathrm{prompt})$$

所有训练在一张NVIDIA H200 GPU上进行，仅训练LoRA参数（参数量极小），使用AdamW优化器，有效batch size 512，学习率 $4 \times 10^{-4}$，共800次迭代。

### 输入输出流总结

- **输入**：单张相机RAW图像、相机颜色校正矩阵 $M_{c \to x}$
- **中间表示**：每次迭代的伪sRGB图像、VLM提取的颜色先验列表、离散色偏预测标签
- **输出**：归一化光照方向向量 $\hat{\ell}^{*} \in \mathbb{R}^3$
- **反馈回路**：光照估计 → 白平衡 → sRGB转换 → VLM评估 → 方向更新 → 下一轮迭代

### 3.1 光照模型与问题重定义

VLM-CC 假设场景受单一全局光源照射，每个像素的 RAW 值 $I$ 是其白平衡后颜色 $W$ 与全局光照颜色 $\ell$ 的逐通道乘积：

$$I = W \odot \ell$$

传统方法直接学习映射 $\hat{\ell} = f(I)$，从 RAW 图像一步回归连续光照向量。VLM-CC 将其重构为迭代语义反馈过程：每次迭代先用当前估计白平衡并转换到伪 sRGB 空间，再由 VLM 评估残差色偏，触发光照方向更新。

### 3.2 白平衡与伪 sRGB 转换

在第 $t$ 次迭代，给定 RAW 图像 $I$ 和当前光照估计 $\hat{\ell}^{(t)}$，白平衡操作定义为逐通道除法：

$$W^{(t)} = I \oslash \hat{\ell}^{(t)}$$

随后通过相机颜色矩阵 $M_{\mathrm{c \to x}}$（相机空间到 XYZ）和标准转换矩阵 $M_{\mathrm{x \to s}}$（XYZ 到线性 sRGB），将白平衡图像映射到伪 sRGB 空间：

$$I_{\mathrm{srgb}}^{(t)} = M_{\mathrm{x \to s}} \, M_{\mathrm{c \to x}} \, W^{(t)}$$

这一步的关键在于：通过相机专属的颜色校正矩阵，将不同传感器的 RAW 数据统一到近似 sRGB 的色彩空间，降低跨相机域偏移，使 VLM 的语义先验能够稳定发挥作用。

### 3.3 颜色先验提取

初始白平衡图像（$t=1$）被送入预训练 VLM，提取场景中可靠对象及其内在颜色，形成结构化的颜色先验列表。该先验在后续所有迭代中共享，为残差光色判断提供语义锚点——例如“草地应为绿色”“天空应为蓝色”，从而避免将物体固有色误判为光照色偏。

### 3.4 残差光色估计

LoRA 微调后的 VLM 接收当前伪 sRGB 图像 $I_{\mathrm{srgb}}^{(t)}$ 和颜色先验提示，预测主导残余光色类别：

$$\boldsymbol{c}^{(t)} = \mathrm{VLM}(\boldsymbol{I}_{\mathrm{srgb}}^{(t)}, \mathrm{prompt}), \quad \boldsymbol{c}^{(t)} \in \{\mathrm{red}, \mathrm{green}, \mathrm{blue}\}$$

输出为离散三分类而非连续 RGB 值，这是方法的核心设计选择：分类任务更匹配 VLM 的语义判断能力，避免了数值回归的不稳定性（消融实验证实，一步数值回归 Mean 2.75°，迭代数值 2.54°，而分类反馈仅 1.52°）。

### 3.5 光照更新与收敛控制

#### 初始化
采用 Gray-World 假设提供初始估计，避免从随机方向开始：

$$\hat{\ell}^{(1)} = \mathrm{Normalize}\Big(\frac{1}{|\Omega|} \sum_{x \in \Omega} I(x)\Big)$$

#### 方向旋转更新
在 RGB 空间中，将当前归一化光照方向 $u^{(t)}$ 向预测色偏的垂直分量方向 $v^{(t)}$ 旋转步角 $A_t$：

$$\hat{\ell}^{(t+1)} = \mathrm{Normalize}\big(\cos A_t \, u^{(t)} + \sin A_t \, v^{(t)}\big)$$

其中 $v^{(t)}$ 由色偏类别 $\boldsymbol{c}^{(t)}$ 确定：例如预测“偏红”时，$v^{(t)}$ 指向红轴在色度平面上的垂直方向。

#### 收敛与终止
当首次出现三种不同色偏标签时，判定进入粗收敛阶段，所有剩余步角 $A_t$ 减半，进入精细调整阶段。迭代上限设为 20 步。

#### 最终估计
为抑制收敛后的小幅振荡，取最后三次迭代估计的归一化几何平均作为最终输出：

$$\hat{\ell}^{*} = \mathrm{Normalize}\big((\hat{\ell}^{(t)} \odot \hat{\ell}^{(t-1)} \odot \hat{\ell}^{(t-2)})^{1/3}\big)$$

### 3.6 训练损失

VLM 微调阶段，对目标色偏 token（red/green/blue）施加标准因果语言建模损失：

$$\mathcal{L}_{\mathrm{LM}} = -\sum_{t} \log p_{\theta}(y_{t} \mid y_{<t}, I_{\mathrm{srgb}}, \mathrm{prompt})$$

训练仅更新 LoRA 参数，使用 AdamW 优化器，学习率 $4 \times 10^{-4}$，有效批次大小 512，共 800 步迭代，在单张 NVIDIA H200 GPU 上完成。

![[assets/figures/papers/paper_list_l2217_https_arxiv_org_abs_2605_19613/figures/003_Figure_3.jpg]]
*Figure 3: Finetuning pipeline of VLM. Given a raw image, we first apply light-color augmentation in camera color space and convert the results to sRGB. These images are processed by a LoRAfinetuned [36] VLM, using the same color-prior prompting strategy as in the inference pipeline. The model predicts the dominant residual light color (red, green, or blue), supervised by the ground-truth illuminant direction. A standard language modeling loss*

## 实验与关键发现

### 核心实验设置

实验采用四组公开数据集——**Gehler‑Shi**、**NUS‑8**、**Intel‑TAU** 和 **Cube+**——并排除缺少相机颜色校正矩阵（CCM）的 Sony IMX135 子集，以保证伪 sRGB 转换的可行性。所有对比均遵循标准 leave‑one‑out 跨数据集协议或跨传感器（cross‑sensor）协议，与近年工作保持一致。训练仅在一张 NVIDIA H200 GPU 上进行，使用 AdamW 优化器训练 800 步，有效批大小为 512，学习率 $4 \times 10^{-4}$，仅更新 LoRA 参数。

### 跨数据集泛化性能

在三个 leave‑one‑out 跨数据集设置中，**VLM‑CC 在所有评估指标上均取得最优性能**，尤其在最差 25% 误差（Worst‑25%）上表现出显著优势。

- **Gehler‑Shi**（训练集：Cube+、NUS‑8、Intel‑TAU）：VLM‑CC 平均角度误差 **1.52°**，较最强直接回归方法 **CCMNet**（Kim et al., ICCV 2025）的 2.23° 降低 0.71°（表 1）。
- **NUS‑8**（训练集：Gehler‑Shi、Cube+、Intel‑TAU）：VLM‑CC 平均误差 **1.83°**，优于 CCMNet 的 2.32°（表 2）。
- **Cube+**（训练集：Gehler‑Shi、NUS‑8、Intel‑TAU）：VLM‑CC 平均误差 **1.51°**，优于 CCMNet 的 1.68°（表 3）。

上述结果验证了核心论断：**语义驱动的迭代反馈框架在跨相机场景中能有效绕过直接 RGB 回归的相机特定过拟合**。

### 跨传感器泛化性能

在 NUS‑8 的跨传感器设置中（7 个相机训练，剩余 1 个测试），VLM‑CC 平均误差 **1.49°**，优于 CCMNet 的 1.71°（表 4）。这表明方法对不同传感器光谱响应的鲁棒性不仅来自 sRGB 转换的域对齐，更来自 VLM 对场景语义颜色先验的利用。

### 同数据集三折交叉验证

在 Gehler‑Shi 的三折交叉验证中（表 5），VLM‑CC 平均误差 **1.34°**，与专为该数据集优化的 **C4‑SqueezeNet‑FC4**（1.35°）持平。该结果说明，即使在相机一致的设定下，VLM‑CC 的迭代语义反馈策略也能达到与专用深度回归方法相当的性能，同时保持跨相机泛化优势。

### 消融实验：推理策略与输出粒度

表 7(a) 对比了三种推理策略：
- **一步数值回归**：直接预测连续 RGB 光照，平均误差 2.75°；
- **迭代数值回归**：每步预测连续值并更新，平均误差 2.54°；
- **VLM‑CC 迭代离散分类**：每步仅预测离散色偏标签（红/绿/蓝），平均误差 **1.52°**。

**离散分类策略显著优于连续回归**，验证了核心设计选择：VLM 在类别颜色判断上的优势远大于不稳定的数值回归，将输出空间离散化是匹配 VLM 能力的关键。

### 消融实验：语义先验与空间结构

表 7(d) 揭示了语义信息的决定性作用：
- 使用**随机颜色先验**替代语义先验，平均误差从 1.52° 升至 1.93°，表明 VLM 提取的对象内在颜色知识是准确评估残差色偏的基础。
- **打乱图像空间结构**（随机排列图像块），平均误差小幅上升，但最差 25% 误差从 3.29° 大幅增至 5.27°。这说明空间连贯性对困难样本（如大面积单色区域）尤为关键——失去空间上下文后，VLM 难以可靠识别对象及其固有颜色。

### 消融实验：微调策略与模型选择

表 7(e) 显示微调至关重要：
- **不微调**：预训练 VLM 几乎失效，平均误差高达 14.33°；
- **仅微调语言模型**：平均误差降至 1.76°；
- **全微调**（LoRA 同时作用于视觉和语言部分）：平均误差 **1.52°**，为最优。

表 7(c) 进一步表明，方法对不同 VLM 骨干（Qwen2.5‑VL、InternVL2）和不同规模（2B、7B）均稳健，更大模型带来微小但一致的提升，说明框架不依赖特定 VLM 架构。

### 收敛行为与定性分析

图 4 展示了一个典型的大面积木地板场景：**CCMNet** 受木材本身偏红色影响，估计光照过红，导致白平衡结果偏蓝；VLM‑CC 从同样受木材偏差影响的 Gray‑World 初始化出发，通过迭代语义反馈逐步校正，最终收敛到 0.57° 误差。色度空间轨迹显示，光照方向在迭代中稳定向真值移动，最后三次估计的归一化几何平均有效抑制了收敛后的小幅振荡。

### 失败模式与局限

1. **相机矩阵依赖**：方法依赖 $M_{c \to x}$ 矩阵实现 sRGB 转换，对于无法提供该矩阵的相机（如 Intel‑TAU 的 Sony IMX135 子集）无法直接适用。
2. **语义先验缺失场景**：当场景缺乏可识别对象或对象颜色先验不可靠时（如随机先验消融所示），VLM 的语义反馈精度下降，最差样本误差增大。
3. **推理延迟**：迭代过程最多 20 步，每步需 VLM 前向推理，相比单次前向方法延迟较高，可能限制实时应用。
4. **离散粒度**：三类色偏分类（红/绿/蓝）虽稳定，但对于需要极精细色彩校正的任务可能粒度不足。
5. **单一光源假设**：当前方法假设全局单一光源，不适用于多光源或复杂混合光照场景。

### 与基线方法的对比总结

| 基准方法 | 范式 | 跨相机泛化 | 语义利用 |
|----------|------|-----------|---------|
| **Gray‑World** (Buchsbaum, 1980) | 统计假设 | 弱 | 无 |
| **FFCC** (Barron & Tsai, CVPR 2017) | 快速傅里叶回归 | 有限 | 无 |
| **SIIE** (Afifi & Brown, BMVC 2019) | 传感器无关估计 | 中等 | 无 |
| **C5** (Afifi et al., ICCV 2021) | 单步超网络 | 较好 | 无 |
| **CCMNet** (Kim et al., ICCV 2025) | 直接回归 + CCM | 最优（此前） | 无 |
| **VLM‑CC**（本方法） | 迭代语义反馈 | **最优** | **显式对象颜色先验** |

VLM‑CC 的核心优势在于将颜色恒常性从“数值回归问题”转化为“语义评估问题”，通过 VLM 的对象颜色先验和离散反馈机制，实现了对相机差异的鲁棒泛化。

![[assets/figures/papers/paper_list_l2217_https_arxiv_org_abs_2605_19613/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative example of our iterative correction process. The scene contains large wooden surfaces, which leads CCMNet [41] toward an over-red illuminant estimate. As a result, its white-balanced result appears blue. Our method starts from Gray-World [15] initialization that is also biased by the wood, but iteratively refines the estimate through feedback and converges to*

![[assets/figures/papers/paper_list_l2217_https_arxiv_org_abs_2605_19613/figures/005_Table_1.jpg]]
*Table 1: Leave-one-out evaluation on the Gehler-Shi dataset*

![[assets/figures/papers/paper_list_l2217_https_arxiv_org_abs_2605_19613/figures/006_Table_4.jpg]]
*Table 4: Cross-sensor evaluation on the NUS-8 dataset. Trained on 7 cameras and tested on the last one*

![[assets/figures/papers/paper_list_l2217_https_arxiv_org_abs_2605_19613/figures/011_Table_7.jpg]]
*Table 7: Comprehensive ablation study in leave-one-out evaluation on Gehler-Shi dataset*

## 定位与知识库关联

### 5.1 颜色恒常性研究脉络中的位置

VLM-CC 的核心贡献在于将颜色恒常性从“直接回归光照”的范式转向“迭代语义反馈”范式。在现有方法谱系中，它可以被定位为**语义驱动、跨相机泛化的迭代校正方法**，其设计逻辑与以下几类工作形成对比或互补。

**统计先验方法**：以 **Gray-World**（Buchsbaum, J. Franklin Inst., 1980）为代表的经典方法假设场景平均颜色为灰色，计算简单且无需训练，但对大面积单色场景（如草地、木地板）极易产生系统性偏差。本文将其仅用作迭代初始化的起点，而非最终估计手段。

**单步学习型回归方法**：这类方法直接从原始图像回归连续光照向量，是近年主流。**FFCC**（Barron and Tsai, CVPR 2017）通过频域卷积实现快速推理；**C5**（Afifi et al., ICCV 2021）引入超网络以适应不同相机传感器；**SIIE**（Afifi and Brown, BMVC 2019）试图学习传感器无关表示。然而，这些方法的核心瓶颈在于：它们隐式地学习了相机特定的 RAW 到光照的映射，在训练数据未覆盖的相机上泛化能力受限。**CCMNet**（Kim et al., ICCV 2025）是当前最先进的跨相机方法，通过直接回归取得了此前最优结果，但 VLM-CC 在多个跨数据集协议下均一致超越 CCMNet（Gehler-Shi 上 Mean 1.52° vs. 2.23°，NUS-8 上 1.83° vs. 2.32°），表明绕过 RAW 域回归、转而利用语义反馈的策略在跨相机场景中具有本质优势。

**迭代优化方法**：部分工作尝试通过迭代精化光照估计，但通常依赖数值优化或物理模型。VLM-CC 的关键区别在于，每次迭代不输出连续数值，而是让 VLM 预测一个离散的残差色偏类别（红/绿/蓝），触发色度空间中的方向性旋转更新。消融实验直接验证了这一设计选择：一步数值回归（Mean 2.75°）和迭代数值回归（Mean 2.54°）均显著劣于迭代离散推理（Mean 1.52°），说明**将连续回归问题转化为分类问题，更匹配 VLM 在类别判断上的优势，避免了不稳定的数值预测**。

### 5.2 适用边界与前提条件

VLM-CC 的有效性依赖于以下前提条件，这些条件划定了其适用边界：

1. **相机颜色矩阵（CCM）的可用性**：方法需要相机专用的 $M_{c \to x}$ 矩阵将白平衡后的图像映射到伪 sRGB 空间，以降低 VLM 面临的域偏移。对于无法提供该矩阵的相机（如论文中排除了 Intel-TAU 数据集中 Sony IMX135 传感器的子集），方法无法直接适用。这是当前框架最硬性的约束。

2. **场景中存在可识别的语义对象**：VLM 的颜色先验提取依赖于识别场景中具有可靠内在颜色的物体（如“草地是绿色的”、“天空是蓝色的”）。当场景缺乏可识别物体，或物体颜色先验不可靠时（如人工染色物体），语义反馈的精度会下降。消融实验用随机颜色先验替换语义先验后，Mean 误差从 1.52° 升至 1.93°，且打乱图像空间结构后 Worst-25% 误差从 3.29° 大幅增至 5.27°，证实了语义和空间连贯性的重要性。

3. **单一全局光源假设**：模型假设 $I = W \odot \ell$，即整幅图像受同一全局光照。在多光源、混合光照或强阴影场景中，这一假设不成立，方法无法处理空间变化的光照。

4. **VLM 微调的必要性**：未微调的预训练 VLM 几乎完全失效（Mean 14.33°），说明通用 VLM 的零样本颜色评估能力不足以支撑该任务，必须通过 LoRA 微调注入特定领域知识。这要求训练数据中包含带有真实光照标注的 RAW 图像。

### 5.3 局限性与开放问题

**推理效率**：迭代推理最多需要 20 步，每步涉及一次 VLM 前向传播，相比单次前向方法（如 FFCC、CCMNet）具有显著更长的推理延迟。论文未报告具体推理时间，但这可能限制其在实时视频处理或低算力边缘设备上的部署。

**离散色偏粒度的上限**：当前仅预测三类残差色偏（红/绿/蓝），虽然稳定但粒度较粗。对于需要极精细色彩校正的专业摄影或印刷场景，三色分类可能不足以捕捉微妙的色温偏差。是否可以在保持稳定性的前提下引入更细粒度的颜色类别（如六类或连续角度离散化），是一个值得探索的方向。

**收敛性的理论保证**：论文采用启发式收敛控制策略（当观察到三种不同色偏标签时减半步角并进入精化阶段），但未给出收敛性的理论分析。在极端初始偏差（如严重偏色的光照）下，迭代过程是否能稳定收敛到真值附近，缺乏形式化保证。

**无 CCM 场景的扩展**：是否可以通过 VLM 的语义先验直接完成白平衡，完全绕过相机颜色矩阵，从而实现真正的“零标定”跨相机应用？这需要 VLM 在 RAW 域或仅经过简单归一化的图像上具备稳健的颜色理解能力，对模型能力提出了更高要求。

**与物理先验的融合**：当前方法纯粹依赖语义反馈，未利用高光检测、色域映射等物理线索。将语义反馈与物理先验结合，有望处理多光源场景或进一步提升困难样本的校正精度。

**视频与多帧扩展**：该框架的迭代特性天然适合利用时间序列信息——前一帧的收敛估计可作为下一帧的初始化，且多帧语义一致性可提供更强的先验约束。但论文未涉及视频场景的实验验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/White_Balance_First_Adjust_Later_Cross_Camera_Color_Constancy_via_Vision_Language_Evaluation.pdf]]
