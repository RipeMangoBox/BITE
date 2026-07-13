---
title: "R2-Seg: Training-Free OOD Medical Tumor Segmentation via Anatomical Reasoning and Statistical Rejection"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/R2_Seg_Training_Free_OOD_Medical_Tumor_Segmentation_via_Anatomical_Reasoning_and_Statistical_Rejection.pdf
project_link: null
code_link: null
aliases:
- RS
- R2-Seg
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过LLM引导的解剖推理定位感兴趣区域并利用双样本统计检验过滤假阳性候选区域。
primary_logic: 将搜索空间限制在由解剖锚点定义的局部ROI内，并保留统计上与正常组织显著不同的候选区域，无需模型参数更新即可有效抑制假阳性。
claims:
- R2-Seg 通过 Reason-and-Reject 两阶段框架有效抑制假阳性
- 移除双样本统计检验导致假阳性显著增加，引入MMD检验和Benjamini–Hochberg校正可恢复清晰边界
- R2-Seg 无需参数更新，避免了微调导致的灾难性遗忘
- 五种OOD肿瘤类型（膀胱、子宫、前列腺、乳腺、宫颈） 上 Dice, Sensitivity, Specificity, Accuracy, CA = R2-Seg
---

# R2-Seg: Training-Free OOD Medical Tumor Segmentation via Anatomical Reasoning and Statistical Rejection

> [!tip] 核心洞察
> 将搜索空间限制在由解剖锚点定义的局部ROI内，并保留统计上与正常组织显著不同的候选区域，无需模型参数更新即可有效抑制假阳性。

| 字段 | 内容 |
|------|------|
| 中文题名 | R2-Seg：基于解剖推理与统计拒绝的训练无关OOD医学肿瘤分割 |
| 英文题名 | R2-Seg: Training-Free OOD Medical Tumor Segmentation via Anatomical Reasoning and Statistical Rejection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Shen_R2-Seg_Training-Free_OOD_Medical_Tumor_Segmentation_via_Anatomical_Reasoning_and_CVPR_2026_paper.html) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | R2-Seg |
| Dataset | 五种OOD肿瘤类型（膀胱、子宫、前列腺、乳腺、宫颈）, 肝、胰腺肿瘤（分布内CT） |

> [!tip] 效果简介
> - 五种OOD肿瘤类型（膀胱、子宫、前列腺、乳腺、宫颈） 上，Dice, Sensitivity, Specificity, Accuracy, CA R2-Seg vs BiomedParse / BiomedParse-LoRA (所有指标一致提升；膀胱 Dice 0.297，CA 0.762)。
> - 肝、胰腺肿瘤（分布内CT） 上，Dice, CA R2-Seg vs BiomedParse (10–30% 相对增益)。

## 概要

医学图像分割的基础模型在分布内（In-Distribution）数据上表现优异，但当部署到分布外（Out-of-Distribution, OOD）肿瘤类型时，普遍产生大量碎片化假阳性，导致过度诊断风险。这一瓶颈的根本原因在于，OOD偏移下视觉嵌入分布的可分离性下降，模型的决策边界不再适用（图1）。

针对上述问题，本文提出 **R2-Seg**，一种训练无关（training‑free）的OOD肿瘤分割框架。其核心思路是将问题分解为“推理（Reason）—拒绝（Reject）”两个阶段：首先通过大语言模型（LLM）引导的解剖推理，将搜索空间限制在由解剖锚点定义的局部感兴趣区域（ROI）内；随后利用双样本统计检验，保留在特征分布上与正常组织显著不同的候选区域，从而在不更新模型参数的前提下有效抑制假阳性。

该方法在五种OOD肿瘤类型（膀胱、子宫、前列腺、乳腺、宫颈）上，相较于冻结的 **BiomedParse**（Zhao et al., Nature Methods 2025）和经LoRA微调的 **BiomedParse‑LoRA** 基线，所有评估指标均一致提升。其中膀胱肿瘤Dice系数达到0.297，类别平均准确率（CA）达到0.762。消融实验进一步表明，移除双样本统计检验会导致特异性急剧下降（膀胱特异性降至0.089），而重新引入MMD检验与Benjamini–Hochberg校正可恢复清晰边界。此外，R2‑Seg无需参数更新，避免了微调带来的灾难性遗忘，在分布内CT器官分割上保持原始性能不退化。

R2‑Seg 的定位介于冻结基础模型与全参数微调之间：它利用LLM的语义先验和统计检验的分布校准能力，在不改变模型权重的前提下，将OOD肿瘤分割的假阳性问题转化为可解释的ROI约束与显著性筛选问题。

### 医学影像分割中的分布外挑战

基础分割模型（如 **BiomedParse**，Zhao et al., *Nature Methods* 2025）在分布内（In-Distribution, ID）医学影像上展现了强大的通用分割能力。然而，当这些模型被部署到分布外（Out-of-Distribution, OOD）场景——例如在训练阶段未见过的新肿瘤类型、新成像模态或新解剖部位——时，其性能会急剧恶化。核心瓶颈在于：OOD偏移会导致模型产生大量碎片化的假阳性预测，这些假阳性区域在视觉嵌入空间中与真实肿瘤的分布高度重叠，使得基础模型的决策边界失效（参见 Figure 1）。

具体而言，OOD场景下基础分割模型面临两个关键困境：
1. **假阳性泛滥**：模型在全图范围内过度激活，产生大量非肿瘤区域的误分割，导致过度诊断风险。
2. **灾难性遗忘**：若通过微调（如 LoRA）适配OOD数据，模型会遗忘其在分布内任务上的原有能力，损害多任务通用性（见 Figure 5 和 Section 4.5.3）。

### 现有方法的缺口

当前应对OOD分割的策略主要分为两类，但各有局限：

- **参数更新类方法**（如 **BiomedParse-LoRA**）：通过对目标OOD数据进行微调来适配模型。然而，这种方法不仅需要标注数据，还会引发灾难性遗忘——微调后的模型在分布内正常器官分割上的性能显著下降（Figure 5），丧失了基础模型的通用性优势。

- **传统测试时增强（TTA）与后处理**：虽然TTA可以在一定程度上提升预测的鲁棒性，但仅靠多视角融合无法从根本上抑制假阳性，因为OOD偏移导致的视觉嵌入混淆并未被解决。

### 本文动机

本文的核心洞察是：**OOD假阳性问题的根源不在于模型参数的不足，而在于搜索空间过大和决策边界失准**。若能通过解剖先验将分割搜索限制在合理的感兴趣区域（ROI）内，并利用统计检验校准决策边界，就有可能在完全不更新模型参数的前提下有效抑制假阳性。

基于这一洞察，本文提出 **R2-Seg**——一个训练无关的OOD肿瘤分割框架，通过“推理-拒绝”（Reason-and-Reject）两阶段流程解决上述问题。该框架无需任何参数更新或目标域标注数据，从而从根源上避免了灾难性遗忘，同时显著提升了OOD场景下的分割特异性与整体精度。

## 核心方法与创新机理

R2‑Seg 的核心创新在于**将 OOD 医学肿瘤分割问题解耦为“可分离性增强 + 决策边界校准”两个阶段**，在不更新基础模型参数的前提下，通过**LLM 引导的解剖推理**与**双样本统计检验**协同抑制假阳性。其相对于冻结基线的关键改变可归纳为四个 changed slot。

### 输入区域：从全图到解剖约束的局部 ROI

基线 **BiomedParse** (Zhao et al., Nature Methods 2025) 在全图影像上直接执行分割；当测试分布发生 OOD 偏移时，视觉嵌入的分布重叠加剧（Figure 1），导致模型在非肿瘤区域产生大量碎片化假阳性。R2‑Seg 通过 LLM 解剖规划器 $\Phi(c)$ 将肿瘤类型 $c$ 翻译为锚点器官集 $A$、ROI 指令 $\mathcal{T}_{\mathrm{ROI}}$ 和推理轨迹 $r$，然后基于锚点器官联合掩码 $B_0$ 生成多尺度膨胀‑方形裁剪 ROI：

$$B_{\gamma} = \mathsf{Square}\big(\mathsf{Dilate}(B_0, \lceil \delta / s \rceil \cdot \gamma)\big), \quad \gamma \in \Gamma$$

这一操作将搜索空间从全图压缩至解剖学合理的局部区域，**从源头降低假阳性候选的生成概率**。

### 假阳性过滤：从无到双样本 MMD 检验 + FDR 控制

基线 BiomedParse 缺乏任何后处理过滤机制，OOD 条件下假阳性泛滥。R2‑Seg 引入**基于特征分布的双样本统计拒绝**：对每个连通分量候选区域 $C_k$，提取其视觉特征与同切片正常组织特征，计算无偏平方 MMD 统计量：

$$\widehat{\mathrm{MMD}}^2 = \frac{1}{m(m-1)} \sum_{i \neq i'} k_{\sigma}(x_i, x_{i'}) + \frac{1}{n(n-1)} \sum_{j \neq j'} k_{\sigma}(y_j, y_{j'}) - \frac{2}{mn} \sum_{i,j} k_{\sigma}(x_i, y_j)$$

通过 $B$ 次置换估计平滑 p 值：

$$p_k = \frac{|\{b \mid \widehat{\mathrm{MMD}}_{\mathrm{perm},b}^2 \geq \widehat{\mathrm{MMD}}_{\mathrm{obs}}^2\}| + 1}{B + 1}$$

并采用 Benjamini–Hochberg 程序控制错误发现率（FDR），仅保留统计上显著异于正常组织的候选区域。消融实验（Table 3）证实：**移除该检验后膀胱肿瘤敏感性虽达 0.923，但特异性骤降至 0.089；重新引入 MMD 检验与 FDR 控制后，特异性显著恢复，Dice 回升至 0.297 ± 0.45**。

### 假阳性门控：三级自适应抑制

在统计检验之外，R2‑Seg 增设**存在性门控（L1）、候选级门控（L2）和案例级门控（L3）**。L2 通过面积下限 $A_{\min}$、平均概率阈值 $\tau_{\mathrm{mean}}$ 和锚点重叠比 $\tau_{\cap}$ 过滤低质量候选；L3 以评分 $S_k = \overline{P}_k \sqrt{|C_k|}$ 选择最优候选，并在空掩码场景下自动抑制输出。该层级策略在维持高特异性的同时，提供了可控的灵敏度‑假阳性权衡（Figure 4）。

### 测试时增强：多视角 TTA + max 融合

R2‑Seg 在 ROI 内引入多视角测试时增强（TTA），对几何变换群 $\mathcal{G}$ 下的增强视图分别推理后取 max 融合：

$$\bar{P} = \max_{g \in \mathcal{G}} \left[ \mathsf{Inv}(g) \circ f_{\theta}\left(g(I|_{B_{\gamma}}); c_{\mathrm{tumor}}, \tau_{\mathrm{tumor}}\right) \right]$$

该设计在不增加训练成本的前提下提升了分割的边界一致性和鲁棒性。

### 模型参数策略：训练无关，避免灾难性遗忘

R2‑Seg 全程**冻结 BiomedParse 权重，不执行任何梯度更新**。对比实验（Figure 5）表明，使用 LoRA 微调的 BiomedParse‑LoRA 在分布内 CT 正常器官分割上性能显著下降，出现灾难性遗忘；R2‑Seg 则完全保持原始模型在分布内任务上的性能。这一特性使 R2‑Seg 更适合临床部署中“零破坏”适配的需求。

综上，R2‑Seg 的创新本质在于**将 OOD 适应的负担从模型参数更新转移至解剖先验注入与统计决策校准**，形成“Reason‑and‑Reject”的训练无关范式。

R2‑Seg 是一种**训练无关**（training‑free）的 OOD 医学肿瘤分割框架，其核心思路是将一个冻结的基础分割模型置于由解剖推理引导的局部搜索空间内，再通过统计假设检验剔除不可靠的候选区域。该框架不更新基础模型的任何参数，因此从根本上避免了微调带来的灾难性遗忘。

### Pipeline 总览

整个管道由两个阶段、七个功能模块串接而成，信息流向为：

1. **LLM 解剖推理规划器**  
   输入一个自由文本的肿瘤概念 $c$（如 “bladder tumor”），LLM 规划器 $\Phi(c)$ 输出结构化的解剖计划，包含锚点器官集 $A$、ROI 构建指令 $\mathcal{T}_{\mathrm{ROI}}$ 以及推理轨迹 $r$。

2. **多尺度 ROI 裁剪**  
   利用锚点器官的分割掩码，计算联合边界框 $B_0$，并通过膨胀与方形裁剪生成一组多尺度 ROI $\{B_\gamma\}_{\gamma\in\Gamma}$：
   $$B_{\gamma} = \mathsf{Square}\big(\mathsf{Dilate}(B_0, \lceil \delta / s \rceil \cdot \gamma)\big), \quad \gamma \in \Gamma$$
   这一步将全图影像压缩为解剖学上合理的局部区域，极大降低了假阳性搜索空间。

3. **肿瘤分割与 TTA 融合**  
   在每个 ROI 内，冻结的基础模型 $f_\theta$ 以肿瘤概念 $c_{\mathrm{tumor}}$ 和阈值 $\tau_{\mathrm{tumor}}$ 为提示进行分割，同时施加多视角测试时增强（TTA），并通过 max 融合得到概率图：
   $$\bar{P} = \max_{g \in \mathcal{G}} \left[ \mathsf{Inv}(g) \circ f_{\theta}\left(g(I|_{B_{\gamma}}); c_{\mathrm{tumor}}, \tau_{\mathrm{tumor}}\right) \right]$$

4. **候选区域提取**  
   对二值化后的肿瘤掩码 $\mathcal{M}_{\mathrm{tumor}}$ 进行连通分量分解，获得空间上不相交的候选区域集：
   $$\{C_k\}_{k \in \mathcal{K}} = \mathsf{Conn}(\mathcal{M}_{\mathrm{tumor}})$$

5. **双样本 MMD 检验**  
   对每个候选区域 $C_k$，抽取其视觉嵌入作为样本集，与正常组织嵌入构成双样本，计算无偏平方 MMD 统计量：
   $$\widehat{\mathrm{MMD}}^2 = \frac{1}{m(m-1)}\sum_{i \neq i'} k_{\sigma}(x_i, x_{i'}) + \frac{1}{n(n-1)}\sum_{j \neq j'} k_{\sigma}(y_j, y_{j'}) - \frac{2}{mn}\sum_{i,j} k_{\sigma}(x_i, y_j)$$
   并通过 $B$ 次置换估计平滑 p 值：
   $$p_k = \frac{|\{b \mid \widehat{\mathrm{MMD}}_{\mathrm{perm},b}^2 \geq \widehat{\mathrm{MMD}}_{\mathrm{obs}}^2\}| + 1}{B + 1}$$

6. **FDR 控制**  
   对全部候选区域的 p 值施加 Benjamini–Hochberg 校正，保留在给定水平 $\alpha$ 下显著异常的候选区域，从而控制假阳性发现率。

7. **假阳性门控（三级）**  
   - **存在性门控**：若肿瘤掩码为空则直接判定无肿瘤。  
   - **候选级门控**：按面积、平均概率和与锚点掩码的重叠比过滤低质量候选。  
   - **案例级门控**：计算候选评分 $S_k = \overline{P}_k \sqrt{|C_k|}$，取最大值 $S^*$，若低于阈值则抑制整例输出，有效应对空掩码场景下的假阳性。

### 设计逻辑与因果机制

该框架的因果杠杆在于将 OOD 偏移下的分割问题分解为两个正交环节：  
- **Reason 阶段**通过 LLM 解剖知识将搜索空间压缩到由锚点器官定义的局部 ROI，提升视觉嵌入的可分离性；  
- **Reject 阶段**利用双样本 MMD 检验与 FDR 控制，仅保留在统计上与正常组织嵌入分布显著不同的候选区域，实现无需标签的决策边界校准。

消融实验直接验证了这一逻辑：移除统计检验后，膀胱肿瘤敏感性虽高达 0.923，但特异性骤降至 0.089，假阳性大量涌现；重新引入 MMD 检验与 Benjamini–Hochberg 校正后，特异性显著恢复，Dice 回升至 0.297 ± 0.45。关闭假阳性门控机制同样导致各肿瘤类别特异性大幅下降，而层级门控策略能够自适应地抑制低置信度区域，维持高特异性。

![[assets/figures/papers/paper_list_l2109_https_openaccess_thecvf_com_content_CVPR2026_html_Shen_R2_Seg_Training_F/figures/002_Figure_2.jpg]]
*Figure 2: Overview of R2-Seg pipeline. Top row: LLM-based segmentation planning and ROI construction; middle row: BioMedParsebased tumor segmentation and candidate extraction; bottom row: Statistical two-sample test and false discovery rate control*

R2-Seg 的核心由两个阶段、六个功能模块构成：**LLM解剖推理规划器** → **多尺度ROI裁剪** → **肿瘤分割与TTA融合** → **候选区域提取** → **双样本MMD检验** → **FDR控制**，并辅以三级假阳性门控机制。以下按管道顺序推导关键公式并解释变量含义。

### LLM解剖推理规划器

给定自由形式的肿瘤类型描述 $c$（如“bladder tumor”），LLM规划器 $\Phi$ 将其映射为结构化解剖计划：

$$\Phi(c) \longrightarrow (A, \mathcal{T}_{\mathrm{ROI}}, r)$$

其中：
- $A$：锚点器官集合（如膀胱肿瘤对应的锚点为膀胱本身）；
- $\mathcal{T}_{\mathrm{ROI}}$：ROI构建指令集；
- $r$：推理轨迹，记录LLM从肿瘤类型到解剖约束的因果链路。

该模块将临床先验注入管道，无需任何参数训练。

### 多尺度ROI裁剪

基于锚点器官的联合二值掩码 $B_0$，通过膨胀与方形裁剪生成多尺度ROI：

$$B_{\gamma} = \mathsf{Square}\big(\mathsf{Dilate}(B_0, \lceil \delta / s \rceil \cdot \gamma)\big), \quad \gamma \in \Gamma$$

变量定义：
- $B_0$：所有锚点器官掩码的并集；
- $\delta$：基础膨胀半径（物理距离）；
- $s$：像素间距；
- $\gamma$：尺度因子，取自预定义集合 $\Gamma$；
- $\mathsf{Dilate}(\cdot, r)$：以半径 $r$ 膨胀掩码；
- $\mathsf{Square}(\cdot)$：将膨胀后的边界框扩展为正方形裁剪区域。

多尺度设计确保不同大小的肿瘤均能被ROI覆盖，同时将搜索空间从全图限制在解剖相关区域，从根本上降低假阳性基数。

### 肿瘤分割与TTA融合

在每个ROI $B_{\gamma}$ 内，冻结的基础分割模型 $f_{\theta}$ 接受几何增强后的图像与肿瘤提示 $(c_{\mathrm{tumor}}, \tau_{\mathrm{tumor}})$，经多视角测试时增强（TTA）后取最大值融合：

$$\bar{P} = \max_{g \in \mathcal{G}} \left[ \mathsf{Inv}(g) \circ f_{\theta}\big(g(I|_{B_{\gamma}}); c_{\mathrm{tumor}}, \tau_{\mathrm{tumor}}\big) \right]$$

其中：
- $\mathcal{G}$：几何变换集合（旋转、翻转等）；
- $g(I|_{B_{\gamma}})$：对ROI图像施加变换 $g$；
- $f_{\theta}(\cdot)$：冻结的分割模型（BiomedParse，Zhao et al., Nature Methods 2025）；
- $\mathsf{Inv}(g)$：逆变换，将预测概率图映射回原始坐标；
- $\bar{P}$：融合后的肿瘤概率图。

$\max$ 融合策略倾向于保留高置信度激活，对碎片化假阳性具有天然抑制作用。

### 候选区域提取

对融合概率图 $\bar{P}$ 二值化得到肿瘤掩码 $\mathcal{M}_{\mathrm{tumor}}$，通过连通分量分解提取空间不相交的候选区域：

$$\{C_k\}_{k \in \mathcal{K}} = \mathsf{Conn}(\mathcal{M}_{\mathrm{tumor}})$$

其中 $C_k$ 为第 $k$ 个连通分量，$\mathcal{K}$ 为候选区域索引集。每个 $C_k$ 将作为后续统计检验的基本单元。

### 双样本MMD检验

对每个候选区域 $C_k$，提取其内部像素的视觉嵌入 $\{x_i\}_{i=1}^m$，并从正常组织区域采样嵌入 $\{y_j\}_{j=1}^n$ 作为对照。使用无偏平方MMD统计量量化两组分布差异：

$$\widehat{\mathrm{MMD}}^2 = \frac{1}{m(m-1)} \sum_{i \neq i'} k_{\sigma}(x_i, x_{i'}) + \frac{1}{n(n-1)} \sum_{j \neq j'} k_{\sigma}(y_j, y_{j'}) - \frac{2}{mn} \sum_{i,j} k_{\sigma}(x_i, y_j)$$

其中 $k_{\sigma}(\cdot, \cdot)$ 为带宽 $\sigma$ 的高斯核。该统计量度量候选区域特征分布与正常组织分布的偏离程度。

通过 $B$ 次置换检验估计平滑p值：

$$p_k = \frac{|\{b \mid \widehat{\mathrm{MMD}}_{\mathrm{perm},b}^2 \geq \widehat{\mathrm{MMD}}_{\mathrm{obs}}^2\}| + 1}{B + 1}$$

分子中 $+1$ 避免p值为零，$B$ 为置换次数。该p值量化了观察到的分布差异由随机因素解释的概率。

### FDR控制

对全部候选区域的p值 $\{p_k\}_{k \in \mathcal{K}}$ 排序为 $p_{(1)} \leq p_{(2)} \leq \cdots \leq p_{(|\mathcal{K}|)}$，采用Benjamini–Hochberg程序控制错误发现率：

$$i^* = \max\left\{i : p_{(i)} \leq \frac{\alpha \cdot i}{|\mathcal{K}|}\right\}$$

保留 $p_{(i)} \leq p_{(i^*)}$ 的所有候选区域，其余作为假阳性拒绝。$\alpha$ 为预设的FDR水平。该步骤无需标注数据即可自适应校准决策边界。

### 三级假阳性门控

为进一步抑制空掩码场景的假阳性，引入层级门控机制：

- **存在性门控（L1）**：若 $\mathcal{M}_{\mathrm{tumor}}$ 为空，直接判定无肿瘤；
- **候选区门控（L2）**：过滤面积过小、平均概率过低或与锚点器官重叠不足的候选区域；
- **案例级门控（L3）**：定义候选区域评分 $S_k = \overline{P}_k \sqrt{|C_k|}$，其中 $\overline{P}_k$ 为候选区域平均概率，$|C_k|$ 为像素面积。取最大评分 $S^* = \max_k S_k$，若低于阈值则判定为阴性案例。

该评分将概率置信度与空间规模耦合，有效区分真实肿瘤激活与碎片化噪声。

---

**关键设计总结**：整个管道以冻结的分割模型为核心，通过LLM推理约束搜索空间（Reason），再以非参数统计检验过滤假阳性（Reject），全程无需梯度更新，从根本上规避了微调引起的灾难性遗忘。消融实验证实，移除MMD检验后膀胱肿瘤敏感性虽达0.923，但特异性骤降至0.089；重新引入检验与FDR控制后，Dice恢复至0.297±0.45，特异性显著回升（Table 3）。

![[assets/figures/papers/paper_list_l2109_https_openaccess_thecvf_com_content_CVPR2026_html_Shen_R2_Seg_Training_F/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of visual embedding distributions. Left: In-Distribution, Right: Out-of-Distribution*

## 实验与关键发现

### 主实验结果

R2‑Seg 在五种 OOD 肿瘤类型（膀胱、子宫、前列腺、乳腺、宫颈）上均一致优于冻结的 **BiomedParse** 基线与经过 LoRA 微调的 **BiomedParse‑LoRA**。表 2 汇总了各方法的 Dice、敏感性、特异性、准确率和类别平均准确率。以膀胱肿瘤为例，R2‑Seg 的 Dice 达到 0.297，类别平均准确率 0.762，在保持高特异性（0.536）的同时将敏感性从基线的近零水平提升至 0.335。这一结果表明，解剖推理与统计拒绝的组合在无需更新模型参数的前提下，有效抑制了基础模型在 OOD 分布下的碎片化假阳性，同时避免了对阳性区域的过度抑制。

在分布内 CT 场景（肝、胰腺肿瘤）中，R2‑Seg 同样带来 10–30% 的相对 Dice 和类别平均准确率增益，说明该框架对分布内数据也具有正向迁移能力，并非以牺牲分布内性能为代价。

### 消融实验

消融实验围绕两个核心组件展开：双样本统计检验与假阳性门控机制。表 3 给出了系统性的定量拆解。

移除统计检验后，膀胱肿瘤的敏感性上升至 0.923，但特异性骤降至 0.089，表明模型在 OOD 条件下产生了大量假阳性激活，几乎无法区分肿瘤与正常组织。重新引入基于无偏平方 MMD 统计量的置换检验，并配合 Benjamini–Hochberg 多重检验校正，膀胱 Dice 恢复至 0.297±0.45，特异性显著回升。这一现象在所有 OOD 肿瘤类型中一致出现，证实统计拒绝是该框架抑制假阳性的关键因果环节。

关闭假阳性门控机制（包括存在性门控、候选区门控和案例级评分）同样导致各肿瘤类别的特异性明显下降。层级门控策略通过面积阈值、平均概率阈值、重叠比约束以及案例级评分 $S_k = \overline{P}_k \sqrt{|C_k|}$，在保留真实阳性区域的同时自适应地过滤低置信度候选，维持了高特异性水平。图 4 的 FROC 曲线进一步展示了不同拒绝设置下扫描级敏感性与每扫描假阳性数之间的权衡关系。

### 灾难性遗忘分析

微调基线 BiomedParse‑LoRA 在 OOD 肿瘤分割上有所提升，但在分布内 CT 正常器官分割任务上出现显著的性能退化（图 5）。统计检验表明，微调模型在所有器官上的分割性能均显著下降，揭示了参数更新带来的灾难性遗忘。相比之下，R2‑Seg 完全冻结 BiomedParse 的权重，仅通过推理阶段的解剖规划与统计过滤实现 OOD 适应，因此天然避免了知识遗忘问题。这一特性使 R2‑Seg 在实际部署中更具安全性——它不会以牺牲原有分布内能力为代价来换取 OOD 泛化。

### 失败模式与局限性

尽管 R2‑Seg 在特异性上取得了显著提升，但敏感性仍处于中等水平（如膀胱 0.335，子宫 0.394）。同时提升敏感性与特异性仍然是开放挑战。部分低对比度或微小肿瘤可能因候选区域在统计检验中与正常组织分布差异不显著而被误拒，导致假阴性。此外，LLM 解剖规划器对肿瘤类型的语义理解和锚点器官定位的准确性高度依赖预训练语言模型的知识覆盖范围，对于罕见肿瘤或解剖变异较大的病例，其鲁棒性有待进一步验证。

![[assets/figures/papers/paper_list_l2109_https_openaccess_thecvf_com_content_CVPR2026_html_Shen_R2_Seg_Training_F/figures/004_Table_2.jpg]]
*Table 2: Representative results across five OOD tumor types. Mean values of Dice, sensitivity (Sens.), specificity (Spec.), accuracy (Acc.), and class-average accuracy (CA) are reported*

![[assets/figures/papers/paper_list_l2109_https_openaccess_thecvf_com_content_CVPR2026_html_Shen_R2_Seg_Training_F/figures/007_Table_3.jpg]]
*Table 3: Ablation results on OOD tumor types*

![[assets/figures/papers/paper_list_l2109_https_openaccess_thecvf_com_content_CVPR2026_html_Shen_R2_Seg_Training_F/figures/005_Figure_3.jpg]]
*Figure 3: Visualization of segmentation results for both in-distribution and out-of-distribution tumor types*

![[assets/figures/papers/paper_list_l2109_https_openaccess_thecvf_com_content_CVPR2026_html_Shen_R2_Seg_Training_F/figures/003_Table_1.jpg]]
*Table 1: A summary of datasets for tumor segmentation. Ax and Sag refer to Axial and Sagittal planes respectively*

## 定位与知识库关联

### 基础模型适配策略的谱系位置

R2-Seg 处于**训练无关（training-free）OOD 适配**与**基础模型即插即用**两条技术路线的交汇点。与当前主流的微调范式形成鲜明对比：

- **BiomedParse‑LoRA**（本文复现基线）：在 OOD 肿瘤数据上使用 LoRA 进行参数更新，虽然提升了目标肿瘤的分割性能，但导致分布内正常器官分割的灾难性遗忘（Figure 5），所有器官的分割性能均显著下降。这暴露了微调路线在多任务基础模型上的根本脆弱性——参数更新不可避免地破坏模型原有的泛化能力。

- **R2‑Seg**：完全冻结 BiomedParse（Zhao et al., Nature Methods 2025）的权重，将适配压力从参数空间转移到**输入空间约束**和**输出空间统计筛选**两个可解释的轻量级模块。这一设计使其天然规避了灾难性遗忘问题，在提升 OOD 肿瘤分割的同时，保持了基础模型在分布内任务上的原始性能。

从更广的谱系看，R2‑Seg 的方法论渊源可追溯至两条线索：

1. **测试时增强（TTA）与推理时优化**：R2‑Seg 的多视角 TTA 与 max 融合属于推理时增强的经典范式，但其创新在于将 TTA 限定在解剖约束的 ROI 内执行，而非全图盲目增强，从而在提升鲁棒性的同时避免了背景区域的假阳性放大。

2. **基于统计假设检验的异常检测**：双样本 MMD 检验 + Benjamini–Hochberg FDR 控制的设计，将分割后处理重新框定为分布差异的统计推断问题。这与基于深度生成模型的重构误差或密度估计的异常检测方法有本质区别——R2‑Seg 直接操作预训练模型的视觉嵌入，无需训练额外的异常检测器。

### 适用边界与条件约束

R2‑Seg 的有效性建立在一系列前提条件之上，这些条件界定了其适用边界：

**必要条件**：
- **可用的解剖锚点**：LLM 规划器需要肿瘤类型具有明确的解剖学邻接关系（如膀胱肿瘤→膀胱锚点、前列腺肿瘤→前列腺锚点）。对于缺乏清晰解剖锚点的弥漫性病变或转移性肿瘤，ROI 构建的有效性将显著降低。
- **正常组织参考分布**：双样本 MMD 检验需要从同病例的非肿瘤切片中采样正常组织特征。这要求输入扫描包含足够的正常区域，对于肿瘤占据绝大部分视野的晚期病例可能失效。
- **基础模型的嵌入质量**：统计检验的判别力依赖于预训练视觉编码器在 OOD 数据上的嵌入是否仍保留足够的分布差异信息（Figure 1 所示的条件成立）。

**性能边界**：
- 在五种 OOD 肿瘤类型上，R2‑Seg 的 Dice 提升幅度存在显著差异（膀胱 0.297、前列腺 0.465），表明解剖约束的有效性受器官形态规则性和锚点分割精度的影响。
- 敏感性与特异性的权衡仍是开放挑战：消融实验显示，关闭统计检验后膀胱敏感性可达 0.923，但特异性骤降至 0.089；重新引入检验后特异性恢复，但敏感性回落至 0.335。这一内在张力表明，基于固定显著性阈值的统计拒绝难以同时最大化两个指标。

### 局限与开放问题

**已识别的局限**：
1. **敏感性与特异性的零和困境**：如原文讨论所述，同时提升敏感性与特异性仍为开放挑战。统计检验的拒绝阈值在过滤假阳性的同时不可避免地牺牲部分真阳性区域，这在低对比度肿瘤边界处尤为突出。
2. **公平性评估缺失**：测试覆盖了多中心、多模态扫描，但未讨论跨人群、种族或扫描设备的公平性表现。数据仅限 CT 和 MR 的特定解剖部位，向其他成像模态（如超声、PET）的泛化性未经验证。

**开放问题**：
- **阈值自适应机制**：能否设计数据驱动的自适应阈值策略，使统计检验的拒绝强度根据输入扫描的噪声水平和肿瘤显著性动态调整，从而在不牺牲特异性的前提下提高敏感性？
- **框架的可迁移性**：统计拒绝框架能否拓展至其他非肿瘤病变（如炎症、纤维化）的分割，或适配至其他类型的基础分割模型（如 SAM、MedSAM）？这需要验证解剖推理的通用性和 MMD 检验在不同嵌入空间中的有效性。
- **LLM 推理的鲁棒性**：LLM 解剖规划器的推理质量在不同临床中心、不同报告习惯下的鲁棒性尚未深入探讨。解剖锚点的错误指定将导致 ROI 构建失败，进而级联影响后续所有模块。这一依赖关系使 R2‑Seg 的端到端可靠性受限于 LLM 的医学知识覆盖度和推理一致性。
- **计算开销的临床可接受性**：多尺度 ROI 的多次前向传播、多视角 TTA、以及置换检验的 B 次重采样，共同构成了显著的推理时计算开销。在临床实时场景中的部署可行性需要量化评估和优化。

## 原文 PDF

![[paperPDFs/CVPR_2026/R2_Seg_Training_Free_OOD_Medical_Tumor_Segmentation_via_Anatomical_Reasoning_and_Statistical_Rejection.pdf]]
