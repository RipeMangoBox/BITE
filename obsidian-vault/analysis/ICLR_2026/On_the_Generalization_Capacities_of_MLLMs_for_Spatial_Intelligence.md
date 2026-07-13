---
title: "On the Generalization Capacities of MLLMs for Spatial Intelligence"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/On_the_Generalization_Capacities_of_MLLMs_for_Spatial_Intelligence.pdf
project_link: null
code_link: https://github.com/Vegetebird/CA-MLLM
openreview_forum_id: DE5ZJtR4bg
aliases:
- CAMF
- GCMSI
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过为每个视觉token注入由相机内参导出的射线方向嵌入，显式提供相机几何信息，解除焦距-深度和尺度-深度的歧义。"
primary_logic: "相机内参是空间推理的必要信息通道；缺乏相机内参，MLLM只能学到与特定相机耦合的捷径，而非通用的三维几何原理。相机感知是实现鲁棒空间智能的前提。"
claims:
- "投影高度公式 h = fH/Z 表明，对于任意λ>0，(f, H, Z)、(λf, H, λZ)和(f, λH, λZ)在投影上是等价的，导致焦距-深度和尺度-深度的内在歧义。"
- "在ScanNet上训练的相机无关模型，当测试图像缩放0.8或1.2倍时，3D物体检测F1@0.25从45.7%骤降至24.3%或31.6%（Qwen2.5-VL），且定位发生系统性偏移，证明模型过拟合于特定分辨率。"
- "相机感知模型在跨相机泛化测试中保持高度一致的精度，而相机无关基线（Qwen2.5-VL、VG-LLM）在改变相机内参时性能急剧下降。"
- "消融实验表明，相机射线嵌入、几何增强与先验蒸馏三个组件均对跨相机泛化有贡献，完整模型在ScanNet-val x1.2上达到52.1% F1@0.25。"
---

# On the Generalization Capacities of MLLMs for Spatial Intelligence

> [!tip] 核心洞察
> 相机内参是空间推理的必要信息通道；缺乏相机内参，MLLM只能学到与特定相机耦合的捷径，而非通用的三维几何原理。相机感知是实现鲁棒空间智能的前提。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 多模态大语言模型在空间智能中的泛化能力研究 |
| 英文题名 | On the Generalization Capacities of MLLMs for Spatial Intelligence |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=DE5ZJtR4bg) · [GitHub](https://github.com/Vegetebird/CA-MLLM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Camera-Aware MLLM Framework |
| Dataset | ScanNet-val (cross-camera generalization, resized images), SPAR-Bench, VSI-Bench, Spatially-grounded tasks (cross-camera) |

> [!tip] 效果简介
> - ScanNet-val (cross-camera generalization, resized images) 上，3D object detection F1@0.25 为 52.1 (Camera-Aware MLLM with all components)，对比 基线在缩放图像上性能大幅下降（例如Qwen2.5-VL从45.7降至24.3），变化 在严重分布偏移下仍保持高性能。
> - SPAR-Bench 上，Overall spatial reasoning accuracy 为 最高 (state-of-the-art)，对比 其他MLLMs (GPT-4o, Gemini-2.5, Qwen2.5-VL, VG-LLM等) 性能较低，变化 显著领先。
> - VSI-Bench 上，Average accuracy across tasks 为 46.8 (Ours-4B)，对比 其他MLLMs (如VG-LLM 4B等) 低于该值，变化 性能领先。

## 概要

### 问题：RGB-only MLLM 空间推理的几何歧义

多模态大语言模型（MLLM）在空间推理任务中存在一个根本性瓶颈：仅依赖 RGB 图像进行三维定位时，相机内参的缺失导致焦距-深度和尺度-深度的内在歧义。对于前平行物体，其投影图像高度由公式 $h_{\mathrm{proj}} = \frac{f_y H}{Z}$ 决定——垂直焦距 $f_y$、物理高度 $H$ 和深度 $Z$ 三者中任意两者的等比例缩放（如 $(\lambda f_y, H, \lambda Z)$ 或 $(f_y, \lambda H, \lambda Z)$）均产生完全相同的二维观测。这意味着，缺乏相机内参的 MLLM 无法区分“近处小物体”与“远处大物体”，也无法区分“长焦拍摄”与“近距离拍摄”，只能学到与训练相机分布耦合的捷径，而非通用的三维几何原理。

这一理论缺陷在实验中得到直接验证：在 ScanNet 上训练的相机无关模型，当测试图像仅被缩放 0.8 或 1.2 倍时，3D 物体检测 F1@0.25 从 45.7% 骤降至 24.3% 或 31.6%（Qwen2.5-VL），且预测的物体位置发生系统性偏移——缩放因子为 $s$ 时，深度预测近似为 $Z_{\mathrm{pred}} \approx Z_{\mathrm{physical}} / s$。此外，在多源混合数据集上训练时，由于各数据源相机内参分布不一致，模型性能反而低于单源训练，进一步暴露了其过拟合于特定相机配置的本质。

### 核心结论：相机感知是实现鲁棒空间智能的前提

本工作提出 **Camera-Aware MLLM 框架**，通过三个关键机制显式注入相机几何信息以解除歧义：

- **密集相机射线嵌入**：基于相机内参为每个视觉 token 计算归一化射线方向 $R_x[i,j] = \frac{u_{ij} - c_x}{f_x}$、$R_y[i,j] = \frac{v_{ij} - c_y}{f_y}$，使模型感知每个像素对应的视线方向。
- **相机感知几何增强**：训练时通过缩放和主点平移合成变化的内参，迫使模型解耦相机属性与场景内容。
- **几何先验蒸馏**：从预训练单目深度估计模型（UniDepth v2）蒸馏密集三维几何先验，在缺乏真实内参时提供补偿。

实验表明，相机感知模型在跨相机泛化测试中保持高度一致的精度，而相机无关基线（Qwen2.5-VL、VG-LLM）在改变相机内参时性能急剧下降。消融实验确认三个组件均对跨相机泛化有正向贡献，完整模型在 ScanNet-val ×1.2 上达到 52.1% F1@0.25。

### 方法定位

该方法属于 **相机条件化的多模态空间推理** 范式，其核心改变在于将相机内参作为显式条件信号注入 MLLM 的视觉编码流程，而非依赖模型从数据中隐式学习相机属性。相较于现有空间推理 MLLM（如 SPAR）和通用 MLLM（如 GPT-4o、Gemini-2.5、Qwen2.5-VL），本框架首次系统性地解决了由相机内参缺失导致的几何歧义问题，在 SPAR-Bench 和 VSI-Bench 上均取得领先性能。

### 主要结果概览

| 基准 | 指标 | 关键结果 |
|------|------|----------|
| ScanNet-val（跨相机泛化） | 3D 检测 F1@0.25 | 完整模型 52.1%，相机无关基线在缩放图像上大幅下降（Qwen2.5-VL 45.7→24.3） |
| SPAR-Bench | 空间推理准确率 | 达到 state-of-the-art，显著领先 GPT-4o、Gemini-2.5 等 |
| VSI-Bench | 平均任务准确率 | Ours-4B 达 46.8%，领先同类模型 |
| 跨相机定位鲁棒性 | 定位一致性 | 相机感知模型保持高度鲁棒，相机无关基线灾难性失效 |

### 局限与开放问题

当前方法依赖预训练单目深度估计模型进行内参估计，估计误差可能影响性能；几何增强主要模拟缩放和主点平移，未能涵盖镜头畸变等现实相机变化；训练和评估集中于室内场景，在室外及自动驾驶领域的泛化性尚待验证。未来方向包括：扩展至鱼眼、多摄像头等非针孔模型；探索在完全无内参场景下的隐式补偿机制；以及评估在实时机器人应用中的计算可行性。



多模态大语言模型（MLLM）在二维视觉理解上取得了长足进步，但当任务涉及三维空间推理——如物体定位、深度估计、相机姿态感知——时，现有模型的泛化能力暴露出根本性缺陷。这一缺陷的根源在于一个被长期忽视的几何事实：**单张RGB图像本身携带固有的三维歧义**。

### 核心问题：RGB-Only空间推理的几何歧义

考虑一个前平行物体在针孔相机下的投影。其图像高度由物理高度 $H$、深度 $Z$ 和垂直焦距 $f_y$ 共同决定：

$$h_{\mathrm{proj}} = \frac{f_y H}{Z}$$

这一简洁的公式揭示了一个关键问题：对于任意缩放因子 $\lambda > 0$，以下三组参数在投影上是完全等价的：

$$(f_y, H, Z) \sim (\lambda f_y, H, \lambda Z) \sim (f_y, \lambda H, \lambda Z)$$

这意味着，仅凭一张RGB图像，模型无法区分“近距离小物体用短焦镜头拍摄”与“远距离大物体用长焦镜头拍摄”这两种截然不同的三维场景（Figure 1）。这种**焦距-深度歧义**与**尺度-深度歧义**构成了空间推理的根本障碍。当相机内参未知时，从二维图像恢复三维几何本质上是一个不适定问题。

### 现有方法的泛化失败

当前主流的MLLM（如**Qwen2.5-VL**、**VG-LLM**、**GPT-4o**、**Gemini-2.5**等）均未显式利用相机内参信息。它们试图仅从视觉特征中隐式学习三维理解，却不可避免地过拟合于训练数据中的特定相机分布。这一缺陷在两个关键实验中得到了清晰验证（Table 1）：

- **跨数据源训练退化**：当将多个室内数据集混合训练时，基线模型在ScanNet验证集上的3D物体检测F1@0.25从45.7%骤降至35.4%（Qwen2.5-VL 3B）。混合数据集中多模态的相机内参分布（Figure 3）产生了冲突的几何信号，模型无法从中提取统一的物理规律。
- **图像缩放测试崩溃**：更令人警醒的是，即使仅在ScanNet上训练，仅将测试图像缩放0.8或1.2倍，Qwen2.5-VL的检测性能便从45.7%分别暴跌至24.3%和31.6%。定位结果发生系统性偏移（Figure 2），预测深度与物理深度呈反比关系：$Z_{\mathrm{pred}} \approx Z_{\mathrm{physical}} / s$。这表明模型学到的并非通用的三维几何原理，而是与训练图像分辨率强耦合的“捷径”。

### 动机与研究目标

上述现象指向一个清晰的瓶颈：**RGB-only MLLM因缺失相机内参这一关键信息通道，无法解耦焦距、尺度与深度之间的几何纠缠，从而丧失跨相机泛化能力。** 相机内参并非可有可无的辅助信息，而是实现鲁棒空间推理的必要条件。

基于这一洞察，本文的核心动机是：**通过为MLLM显式注入相机几何信息，使其学习相机无关的三维物理规律，而非相机特定的视觉模式。** 研究目标包括：（1）设计一种相机感知架构，将内参信息有效融入视觉token；（2）开发相机感知的数据增强策略，迫使模型解耦相机属性与场景内容；（3）在缺乏真值内参的场景中，通过蒸馏预训练三维模型的几何先验来弥补信息缺口。



## 核心方法与创新机理

本研究的核心创新在于首次系统性地诊断并解决了多模态大语言模型（MLLM）在空间推理中因缺乏相机内参而产生的几何歧义问题。其关键洞察是：**相机内参是空间推理的必要信息通道**；缺乏相机内参，模型只能学到与特定相机耦合的捷径，而非通用的三维几何原理。基于此，提出了 **Camera-Aware MLLM框架**，通过以下三个相互协同的 **changed slots** 实现相机感知：

### 1. 相机内参条件注入：密集相机射线嵌入

**基线缺陷**：现有MLLM（如 **Qwen2.5-VL** (Bai et al., 2025)、**VG-LLM** (Zheng et al., 2025)）仅以RGB图像作为视觉输入，完全缺失相机内参信息。这导致模型无法区分焦距变化与深度变化、物体物理尺度与距离——从投影公式 $h_{\mathrm{proj}} = \frac{f_y H}{Z}$ 可知，对任意 $\lambda > 0$，$(f_y, H, Z) \sim (\lambda f_y, H, \lambda Z) \sim (f_y, \lambda H, \lambda Z)$ 在二维投影上完全等价（Eq.1, Eq.2），形成焦距-深度和尺度-深度的内在歧义。

**创新方案**：为每个视觉token注入由相机内参导出的**密集相机射线嵌入（Dense Camera Ray Embedding）**。具体而言，对于每个视觉token对应的网格位置 $(i,j)$，利用内参矩阵 $\mathbf{K}$ 中的焦距 $(f_x, f_y)$ 和主点 $(c_x, c_y)$，计算其归一化射线方向分量（Section 4.2）：

$$R_x[i,j] = \frac{u_{ij} - c_x}{f_x}, \quad R_y[i,j] = \frac{v_{ij} - c_y}{f_y}$$

该嵌入显式编码了每个像素在三维空间中的视线方向，使模型能够将二维观测与三维几何关联起来，从根本上解除了焦距-深度和尺度-深度的歧义。

### 2. 数据增强策略：相机感知几何增强

**基线缺陷**：标准的数据增强策略（如随机裁剪、翻转）不涉及相机内参的相应调整，导致训练数据中的图像变换与相机参数脱节。模型由此学到的是与特定训练分辨率耦合的伪特征，而非对相机属性不变的几何理解。

**创新方案**：提出**相机感知几何增强（Camera-Aware Geometric Augmentation）**策略（Section 4.3, Figure 5），在训练过程中通过两种操作合成变化的内参：
- **缩放（Scaling）**：将图像缩放 $s$ 倍，同时更新内参为 $(f_x, f_y, c_x, c_y) \mapsto (s f_x, s f_y, s c_x, s c_y)$；
- **主点平移（Shifting）**：平移主点位置，模拟非中心裁切效果。

该策略迫使模型解耦相机属性与场景内容，从而习得对相机内参不变的几何表征。

### 3. 先验知识来源：三维几何先验蒸馏

**基线缺陷**：现有MLLM仅依赖视觉编码器（ViT）提取的语义特征，缺乏显式的三维几何信息。即使注入相机射线嵌入，模型仍需从零开始学习将视线方向与深度、三维结构关联。

**创新方案**：从预训练的单目深度估计基础模型 **UniDepth v2** 中蒸馏密集三维几何先验（Section 4.4）。具体而言，利用冻结的UniDepth v2预测场景的密集点云，将其编码为**几何先验嵌入 $E_\text{geo}$**，与视觉特征和相机射线嵌入一并输入**几何感知视觉编码器（Geometry-Aware Visual Encoder, GAVE）**进行融合（Figure 4）。这一设计为模型提供了丰富的三维结构线索，降低了从二维图像和射线方向中隐式推断几何的难度。当真实相机内参不可用时，UniDepth v2还可用于在线估计内参，使模型在无真值内参的场景下仍能超越相机无关基线（Figure 6c）。

### 创新协同与证据强度

三个changed slots并非孤立设计，而是形成闭环：**相机射线嵌入**提供几何推理的必要输入，**几何增强**确保模型不依赖特定相机参数，**先验蒸馏**补充三维结构知识。消融实验（Table 5）证实，移除任一组件均导致跨相机泛化性能下降，完整模型在ScanNet-val ×1.2缩放测试上达到52.1% F1@0.25，而相机无关基线在相同条件下性能骤降（如Qwen2.5-VL从45.7%降至24.3%），证据强度高（confidence ≥ 0.9）。



![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_DE5ZJtR4bg/figures/007_Figure_6.jpg]]
*Figure 6: Cross-camera generalization on spatially-grounded tasks. While camera-agnostic MLLMs (Qwen2.5-VL, VG-LLM) fail catastrophically on altered camera geometries by rescaling, our method maintains robust performance, proving its ability to generalize across cameras*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_DE5ZJtR4bg/figures/005_Figure_4.jpg]]
*Figure 4: The proposed Camera-Aware MLLM Framework. (a) The overview of the architecture, where (b) Geometry-Aware Visual Encoder (GAVE) injects camera-awareness and 3D geometric priors into the MLLM*

### 问题定位：相机无关MLLM的几何歧义瓶颈

现有MLLM在空间推理任务中面临一个根本性瓶颈：RGB-only的视觉编码器缺乏相机内参信息，导致模型无法区分物体尺度与深度、焦距与物体距离等几何属性。从针孔相机模型出发，前平行物体在图像中的投影高度由公式 $h_{\mathrm{proj}} = \frac{f_y H}{Z}$ 决定，其中 $f_y$ 为垂直焦距、$H$ 为物理高度、$Z$ 为深度。对于任意缩放因子 $\lambda > 0$，以下等价类在投影上完全不可区分：

$$(f_y, H, Z) \sim (\lambda f_y, H, \lambda Z) \sim (f_y, \lambda H, \lambda Z)$$

这种焦距-深度歧义和尺度-深度歧义意味着，相同的2D图像可以由不同的3D场景产生——近距离物体配合广角镜头与远距离物体配合长焦镜头在图像上完全一致。缺乏相机内参的MLLM因此只能学到与特定相机分布耦合的捷径，而非通用的三维几何原理。

实证证据充分支持了这一诊断：在ScanNet上训练的相机无关模型，当测试图像仅缩放0.8或1.2倍时，3D物体检测F1@0.25从45.7%骤降至24.3%或31.6%（Qwen2.5-VL），且预测的3D定位发生系统性偏移——缩放因子为 $s$ 时，预测深度近似缩放为 $Z_{\mathrm{pred}} \approx Z_{\mathrm{physical}} / s$。这证明模型过拟合于训练时的特定分辨率，而非学习到真正的几何推理能力。

### 核心洞察：相机内参是空间推理的必要信息通道

论文的核心洞察在于：相机内参不是可选的辅助信息，而是实现鲁棒空间推理的必要条件。只有显式地将相机几何信息注入模型，才能解除焦距-深度和尺度-深度的内在歧义，使模型学到与相机解耦的通用三维理解能力。这一洞察驱动了整个框架的设计。

### 整体Pipeline架构

所提出的Camera-Aware MLLM框架由以下核心模块构成，数据流如图4所示：

1. **Text Encoder（文本编码器）**：采用标准文本编码器处理文本指令，生成文本token序列。

2. **Visual Encoder (ViT)（视觉编码器）**：从输入图像中提取视觉特征 $F_{\mathrm{vis}}$，作为后续几何感知融合的基础表示。

3. **Camera Ray Embedding（相机射线嵌入）**：这是框架的核心创新之一。基于相机内参矩阵 $\mathbf{K} = \left[ \begin{array}{ccc} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{array} \right]$，为每个视觉token计算其对应的归一化射线方向：
   $$R_x[i,j] = \frac{u_{ij} - c_x}{f_x}, \quad R_y[i,j] = \frac{v_{ij} - c_y}{f_y}$$
   这些方向分量被编码为密集嵌入 $E_{\mathrm{cam}}$，为每个视觉token显式提供其视线方向的几何信息。

4. **Geometric Prior Distillator（几何先验蒸馏器）**：利用冻结的预训练单目深度估计模型（UniDepth v2）预测密集点云，并将其编码为几何先验嵌入 $E_{\mathrm{geo}}$。这一模块在相机内参不可用时尤为重要——UniDepth v2可在推理时动态估计内参，使模型在缺少真值内参的场景中仍能获得几何信息。

5. **Geometry-Aware Visual Encoder (GAVE)（几何感知视觉编码器）**：这是信息融合的核心模块。GAVE接收三个输入流——视觉特征 $F_{\mathrm{vis}}$、相机射线嵌入 $E_{\mathrm{cam}}$ 和几何先验嵌入 $E_{\mathrm{geo}}$——并将它们融合为几何感知的视觉token序列。这一融合过程使LLM后续处理时能够同时利用表观信息和显式几何信息。

6. **LLM（大语言模型）**：接收GAVE输出的几何感知视觉token和文本编码器输出的文本token，进行多模态联合推理，完成空间定位、3D物体检测等任务。

### 训练策略中的关键设计

除架构层面的相机内参注入外，框架还引入了**相机感知几何增强**（Camera-Aware Geometric Augmentation）策略。在训练过程中，通过缩放图像（因子 $s$，同步更新内参为 $(s f_x, s f_y, s c_x, s c_y)$）和主点平移来合成变化的内参。这一策略迫使模型解耦相机属性与场景内容，是其跨相机泛化能力的关键来源。

训练时，视觉编码器（ViT）、3D几何编码器（VGGT）和UniDepth v2均被冻结，仅MLLM主体、相机射线嵌入模块和几何先验蒸馏器可训练，确保消融比较的公平性。



### 几何歧义的形式化根源

RGB-only MLLM在空间推理中面临根本性的几何歧义，其根源在于标准针孔相机投影模型。对于前平行物体，其投影图像高度由以下公式决定：

$$h_{\mathrm{proj}} = \frac{f_y H}{Z}$$

其中 $f_y$ 为垂直焦距，$H$ 为物体物理高度，$Z$ 为物体深度。该公式揭示了两类内在歧义：

**焦距-深度歧义**：对于任意缩放因子 $\lambda > 0$，参数组 $(f_y, H, Z)$ 与 $(\lambda f_y, H, \lambda Z)$ 产生完全相同的投影高度。这意味着焦距变化在观测上与深度变化等价。

**尺度-深度歧义**：参数组 $(f_y, H, Z)$ 与 $(f_y, \lambda H, \lambda Z)$ 同样产生相同的投影高度，导致物体物理尺寸与深度相互混淆。

这两类歧义可统一表示为等价类关系：

$$(f_y, H, Z) \sim (\lambda f_y, H, \lambda Z) \sim (f_y, \lambda H, \lambda Z)$$

当图像被缩放因子 $s$ 处理时，相机无关模型的深度预测会产生系统性偏差：

$$Z_{\text{pred}} \approx \frac{Z_{\text{physical}}}{s}$$

该偏差解释了为何在ScanNet上训练的模型，当测试图像缩放0.8或1.2倍时，3D物体检测F1@0.25从45.7%骤降至24.3%或31.6%（Qwen2.5-VL），且定位发生系统性偏移。

### 核心模块设计

为解决上述歧义，Camera-Aware MLLM框架引入三个关键模块：

#### 密集相机射线嵌入（Dense Camera Ray Embedding）

该模块为每个视觉token注入由其对应像素的相机射线方向导出的几何信息。给定相机内参矩阵：

$$\mathbf{K} = \left[ \begin{array}{ccc} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{array} \right]$$

对于位于网格位置 $(i,j)$ 的视觉token，其归一化射线方向分量计算如下：

$$R_x[i,j] = \frac{u_{ij} - c_x}{f_x}, \quad R_y[i,j] = \frac{v_{ij} - c_y}{f_y}$$

其中 $(u_{ij}, v_{ij})$ 为像素坐标，$(c_x, c_y)$ 为主点，$(f_x, f_y)$ 为焦距。这些归一化方向分量构成密集嵌入 $\mathbf{E}_{\text{cam}}$，显式地为每个token提供其视线方向信息，从而解除焦距-深度和尺度-深度的歧义。

#### 几何先验蒸馏器（Geometric Prior Distillator）

该模块利用冻结的预训练单目深度估计模型（UniDepth v2）预测密集点云，并将其编码为几何先验嵌入 $\mathbf{E}_{\text{geo}}$。当真实相机内参不可用时，UniDepth v2可在线估计内参，使模型在缺乏真值标注的场景下仍能获得几何信息。

#### 几何感知视觉编码器（Geometry-Aware Visual Encoder, GAVE）

GAVE负责融合三类信息：视觉编码器（ViT）提取的视觉特征 $\mathbf{F}_{\text{vis}}$、相机射线嵌入 $\mathbf{E}_{\text{cam}}$ 以及几何先验嵌入 $\mathbf{E}_{\text{geo}}$。融合后的几何感知视觉token被送入LLM进行多模态推理和空间定位。训练过程中，视觉编码器、3D几何编码器和UniDepth v2均被冻结，仅MLLM、相机射线嵌入和几何先验蒸馏器可训练。

### 相机感知几何增强

训练阶段，通过合成扰动相机内参来增强数据多样性：
- **缩放**：将图像缩放 $s$ 倍，同步更新内参为 $(s f_x, s f_y, s c_x, s c_y)$
- **主点平移**：随机平移主点位置

该策略迫使模型解耦相机属性与场景内容，显著提升对未见相机内参的鲁棒性。



## 实验与关键发现

### 核心瓶颈的实证验证

论文首先通过一组受控实验，系统性地揭示了相机无关MLLM在空间推理中的泛化失败。**Table 1** 给出了定量证据：当Qwen2.5-VL仅在ScanNet上训练时，3D物体检测F1@0.25达到45.7%；然而，当训练数据混合了多个室内场景数据集后，同一验证集上的性能骤降至35.4%。这一退化源于不同数据源之间相机内参的多模态分布（**Figure 3**），模型在相互冲突的内参信号中无法学到统一的几何映射。


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_DE5ZJtR4bg/figures/004_Figure_3.jpg]]
*Figure 3: Multi-modal distribution of camera intrinsics in mixed datasets*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_DE5ZJtR4bg/figures/002_Table_1.jpg]]
*Table 1: Generalization failure of camera-agnostic MLLMs. 3D object detection performance drops when trained on mixed data sources or evaluated on resized images, exposing a fundamental lack of robustness and generalization*

更直接的证据来自图像缩放实验。将ScanNet测试图像缩放至0.8倍或1.2倍后，Qwen2.5-VL的F1@0.25从45.7%分别暴跌至24.3%和31.6%。**Figure 2** 可视化了这一失效模式：缩放后的图像导致预测的3D定位发生系统性偏移，模型并非输出随机噪声，而是产生了与缩放因子耦合的定向偏差。

这一现象的因果机制可由投影几何严格解释。对于前平行物体，其投影高度遵循：

$$h_{\mathrm{proj}} = \frac{f_y H}{Z}$$

由此导出等价类关系：对于任意 $\lambda > 0$，

$$(f_y, H, Z) \sim (\lambda f_y, H, \lambda Z) \sim (f_y, \lambda H, \lambda Z)$$

这意味着，仅凭RGB图像，焦距变化与深度变化在观测上不可区分（焦距-深度歧义），物体物理尺寸与深度同样不可区分（尺度-深度歧义）。当图像被缩放因子 $s$ 时，相机无关模型的深度预测近似为 $Z_{\mathrm{pred}} \approx Z_{\mathrm{physical}} / s$，这正是**Figure 2**中系统性偏移的数学根源。

### 跨相机泛化能力

**Figure 6** 是验证方法有效性的核心实验。在空间定位任务上，当测试图像的相机内参被合成扰动（缩放、主点平移）时，相机无关基线（Qwen2.5-VL、VG-LLM）的性能发生灾难性崩溃，而所提出的Camera-Aware MLLM保持了高度一致的精度。这一对比直接证明了相机内参条件注入是实现跨相机泛化的关键。

值得注意的是，**Figure 6(c)** 展示了当真实相机内参不可用时的场景。此时方法依赖几何先验蒸馏模块（基于冻结的UniDepth v2）在线估计内参，即便如此，其性能仍持续且显著地超越相机无关基线。这表明蒸馏的3D几何先验在缺失真值内参时可作为有效的替代信息通道。

### 空间推理基准性能

在提供精确相机参数的**SPAR-Bench**上（**Table 2**），Camera-Aware MLLM取得了最高的综合空间推理精度，超越了包括GPT-4o、Gemini-2.5、Qwen2.5-VL、VG-LLM和SPAR在内的所有对比方法。


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_DE5ZJtR4bg/figures/008_Table_2.jpg]]
*Table 2: Comparison of MLLMs’ spatial reasoning performance on SPAR-Bench*

在面向RGB-only方法设计的通用空间推理基准**VSI-Bench**上（**Table 3**），尽管该基准不提供相机内参，方法仍达到46.8%的平均准确率（Ours-4B），领先于同规模的VG-LLM 4B等基线。**Table 4** 进一步展示了在多个空间理解数据集上的综合对比，方法在多数指标上取得了最优或领先的性能。这些结果表明，相机感知不仅有利于跨相机泛化，也能提升通用空间推理能力。


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_DE5ZJtR4bg/figures/009_Table_3.jpg]]
*Table 3: Comparison of MLLMs’ spatial reasoning performance on VSI-Bench*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_DE5ZJtR4bg/figures/010_Table_4.jpg]]
*Table 4: Comparison of model performance on various spatial understanding datasets. rated collection of spatially-grounded tasks to train a generalist model on spatial reasoning*

### 消融实验

**Table 5** 在ScanNet-val x1.2（跨相机泛化测试）上对框架的三个核心组件进行了消融：


![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_DE5ZJtR4bg/figures/011_Table_5.jpg]]
*Table 5: Ablation study on the components of our Camera-Aware MLLM framework. Performance measured on ScanNet-val x1.2 to test cross-camera generalization*

- **相机射线嵌入（Camera Ray Embedding）**：移除后性能显著下降，验证了为每个视觉token注入归一化射线方向 $R_x[i,j] = (u_{ij} - c_x)/f_x, R_y[i,j] = (v_{ij} - c_y)/f_y$ 是解除几何歧义的必要条件。
- **相机感知几何增强（Geometric Augmentation）**：通过合成缩放和主点平移迫使模型解耦相机属性与场景内容，移除该组件导致对未见内参的鲁棒性明显降低。
- **几何先验蒸馏（Prior Distillation）**：从UniDepth v2蒸馏的密集3D几何先验嵌入为模型提供了额外的深度与结构信息，移除后跨相机泛化能力受损。

完整模型在ScanNet-val x1.2上达到52.1%的F1@0.25，三个组件均对最终性能有正向贡献。

### 失败模式与局限

尽管方法在跨相机泛化上表现鲁棒，仍存在若干已知局限：

1. **内参估计依赖**：当真实内参缺失时，方法依赖UniDepth v2进行在线估计。估计误差会通过相机射线嵌入传播，影响最终定位精度。在极端失真的场景下，这一误差可能不可忽略。
2. **增强覆盖不足**：相机感知几何增强目前主要模拟缩放和主点平移，未能覆盖镜头畸变、非中心裁切等现实世界中的复杂相机变化，在这些场景下的泛化性未经充分验证。
3. **领域限制**：训练和评估主要集中于室内场景数据集，在室外、自动驾驶等领域的迁移能力有待进一步检验。
4. **单帧假设**：模型仅在单帧上训练，对于视频序列中动态变化的相机参数处理能力未深入探究。



## 定位与知识库关联

### 核心瓶颈与理论洞见

RGB-only MLLM 在空间推理任务中面临一个根本性的几何歧义问题：从单张二维图像反推三维结构是一个病态问题。其数学根源在于针孔投影公式 $h_{\mathrm{proj}} = \frac{f_y H}{Z}$ 所揭示的等价类变换 $(f_y, H, Z) \sim (\lambda f_y, H, \lambda Z) \sim (f_y, \lambda H, \lambda Z)$——对于任意缩放因子 $\lambda > 0$，焦距、深度与物体尺度的组合可以产生完全相同的二维投影。这意味着，缺乏相机内参的 MLLM 无法区分“近处物体用广角镜头拍摄”与“远处物体用长焦镜头拍摄”这两种截然不同的三维场景。模型学到的不是通用的三维几何原理，而是与训练相机分布耦合的统计捷径，导致在相机参数变化时发生灾难性遗忘。

### 方法谱系定位

本研究提出的 **Camera-Aware MLLM Framework** 明确针对上述几何歧义，在现有 MLLM 谱系中引入了“相机感知”这一新的设计维度。与之形成对比的基线方法可分为两类：

- **通用 MLLM**：如 **Qwen2.5-VL**（Bai et al., 2025）、**GPT-4o**（Hurst et al., 2024）、**Gemini-2.5**（Comanici et al., 2025），这些模型在通用视觉语言任务上表现强大，但完全不建模相机几何，因此在空间推理任务中缺乏跨相机泛化能力。
- **空间推理专用 MLLM**：如 **VG-LLM**（Zheng et al., 2025）和 **SPAR**（Zhang et al., 2025），前者引入了三维特征提取，后者专为空间推理设计，但它们均未显式条件化于相机内参，本质上仍属于相机无关范式。

本方法的独特贡献在于将相机内参提升为一等公民，通过三个互补机制构建相机感知能力：

1. **密集相机射线嵌入**：基于归一化射线方向 $R_x[i,j] = \frac{u_{ij} - c_x}{f_x}, R_y[i,j] = \frac{v_{ij} - c_y}{f_y}$ 为每个视觉 token 注入几何信息，显式解除焦距-深度和尺度-深度的歧义。
2. **相机感知几何增强**：在训练时通过缩放和主点平移合成变化的内参，迫使模型解耦相机属性与场景内容。
3. **几何先验蒸馏**：从冻结的单目深度估计模型（UniDepth v2）蒸馏密集三维几何先验，在相机内参不可用时提供替代性几何信息。

### 关键证据支撑

实验证据从多个维度验证了相机感知的必要性与有效性：

- **泛化失败的可视化与量化**（Table 1, Figure 2）：在 ScanNet 上训练的相机无关模型（Qwen2.5-VL），当测试图像缩放 0.8 或 1.2 倍时，3D 物体检测 F1@0.25 从 45.7% 骤降至 24.3% 或 31.6%，且定位发生系统性偏移。这直接证实了模型过拟合于特定分辨率，而非学习到真正的三维推理。
- **跨相机鲁棒性**（Figure 6）：相机感知模型在改变相机内参时保持高度一致的精度，而相机无关基线性能急剧下降。即使相机内参未知，几何先验蒸馏仍使模型显著超越基线。
- **消融实验**（Table 5）：三个组件均对跨相机泛化有正向贡献，完整模型在 ScanNet-val ×1.2 上达到 52.1% F1@0.25。
- **通用空间推理基准**：在 SPAR-Bench 和 VSI-Bench 上均达到最优性能，证明相机感知不仅解决跨相机泛化，也提升了通用空间推理能力。

### 适用边界与局限

本方法的适用性受以下因素制约：

1. **内参获取依赖**：在缺乏真实相机内参时，方法依赖 UniDepth v2 进行估计，估计误差会传播到下游推理。在完全无法可靠估计的场景中，性能增益可能衰减。
2. **增强策略的覆盖范围**：相机感知几何增强主要模拟缩放和主点平移，未能涵盖镜头畸变、非中心裁切等现实世界中的复杂相机变化。
3. **场景泛化未验证**：训练和评估集中在室内场景数据集，在室外、自动驾驶等领域的泛化性有待实证检验。
4. **动态相机处理缺失**：模型仅在单帧上训练，对于视频序列中动态变化的相机参数，其处理能力未深入探究。

### 开放问题

- 如何将相机感知框架从针孔模型扩展到鱼眼、多摄像头等非标准投影模型？
- 在完全无内参且无法可靠估计的场景中，模型能否通过学习内部表征来隐式补偿几何信息的缺失？
- 相机感知方法引入的额外计算开销（射线嵌入计算、几何先验蒸馏）是否满足实时机器人应用的需求？
- 能否通过自监督或弱监督方式，从大规模无内参标注的图像中学习相机感知能力，从而突破数据规模的瓶颈？



## 原文 PDF

![[paperPDFs/ICLR_2026/On_the_Generalization_Capacities_of_MLLMs_for_Spatial_Intelligence.pdf]]
