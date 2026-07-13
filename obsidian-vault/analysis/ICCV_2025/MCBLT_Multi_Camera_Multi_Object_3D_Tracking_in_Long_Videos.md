---
title: "MCBLT: Multi-Camera Multi-Object 3D Tracking in Long Videos"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/MCBLT_Multi_Camera_Multi_Object_3D_Tracking_in_Long_Videos.pdf
project_link: null
code_link: null
aliases:
- MCBLT
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在BEV空间中进行早期多视图特征融合实现可泛化的3D检测，并通过层级图神经网络在3D空间中完成长时关联，特别是引入无需训练的全局合并块替代启发式匹配。"
primary_logic: "通过BEVFormer将多视图2D特征统一到鸟瞰图空间进行3D检测，消除了对固定相机布局的依赖；结合2D-3D检测关联优化ReID特征质量；再以层级GNN在3D世界坐标下直接建模跟踪，并利用全局层实现跨数千帧的稳定关联，从而大幅提升MTMC的泛化性和长时跟踪能力。"
claims:
- "MCBLT在AICity'24数据集上取得SOTA（HOTA 81.22），在WildTrack数据集上同样取得SOTA（IDF1 95.6）。"
- "所提出的全局合并块相比启发式匹配将HOTA提升了4.42。"
- "2D-3D检测关联算法大幅提升了ReID特征质量，使得WildTrack上的IDF1从63.2跃升至93.4。"
- "MCBLT在长视频序列上展示出卓越的鲁棒性，从1000帧到23994帧HOTA仅下降4.58，而Kalman滤波基线下降43.35。"
---

# MCBLT: Multi-Camera Multi-Object 3D Tracking in Long Videos

> [!tip] 核心洞察
> 通过BEVFormer将多视图2D特征统一到鸟瞰图空间进行3D检测，消除了对固定相机布局的依赖；结合2D-3D检测关联优化ReID特征质量；再以层级GNN在3D世界坐标下直接建模跟踪，并利用全局层实现跨数千帧的稳定关联，从而大幅提升MTMC的泛化性和长时跟踪能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MCBLT：长视频中的多相机多目标三维跟踪 |
| 英文题名 | MCBLT: Multi-Camera Multi-Object 3D Tracking in Long Videos |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2412.00692) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MCBLT |
| Dataset | AICity'24, WildTrack, WildTrack (共享检测输入), AICity'24 仓库场景 (23,994帧长视频) |

> [!tip] 效果简介
> - AICity'24 上，HOTA 为 81.22，对比 N/A (SOTA)，变化 N/A。
> - WildTrack 上，IDF1 为 93.4，对比 92.3 (EarlyBird)，变化 +1.1。
> - WildTrack (共享检测输入) 上，IDF1 为 95.6，对比 92.3 (EarlyBird)，变化 +3.3。

## 概要

多相机多目标（MTMC）三维跟踪的核心挑战在于，如何在相机布局多变的大规模场景中，实现鲁棒的跨视图信息融合与长时关联。现有方法主要分为两类：一是**后期多视图聚合**，在各相机独立完成2D检测后，仅依赖外观ReID特征进行跨视图匹配，缺乏几何约束，易受遮挡和视角变化影响；二是**带几何投影的后期聚合**，虽引入相机标定信息进行空间关联，但融合仍发生在检测之后，难以充分利用多视图的互补信息。近年来出现的**早期多视图融合**方法（如EarlyBird）尝试在BEV空间统一检测，但其依赖固定场景的相机配置，且采用Kalman滤波与启发式匹配进行跟踪，在长视频中易发生漂移和身份断裂。

MCBLT针对上述瓶颈，提出了一条**可泛化的早期多视图融合MTMC管线**，其核心洞察在于：**将多视图2D特征在BEV空间进行早期融合以消除对固定相机布局的依赖，并在3D世界坐标下以层级图神经网络直接建模跟踪关联，从而大幅提升泛化性与长时跟踪的鲁棒性。** 具体而言，MCBLT通过BEVFormer的空间-时序注意力机制，将任意相机配置下的多视图特征聚合为统一的鸟瞰图表示并直接预测3D边界框；随后，通过2D-3D检测关联算法将3D框反投影至各视图，与2D检测结果匹配以获取精确的2D框，从而提取更纯净的ReID外观特征；最后，以层级图神经网络（SUSHI-3D）在3D世界坐标下执行跟踪，并引入无需额外训练的全局合并块，替代传统滑动窗口重叠与启发式匹配，实现跨数千帧的稳定关联。

实验验证了MCBLT的有效性：在AICity'24数据集上取得SOTA结果（HOTA 81.22），在WildTrack数据集上同样取得SOTA（IDF1 95.6）。消融实验表明，全局合并块相比启发式匹配将HOTA提升4.42；2D-3D检测关联模块使WildTrack的IDF1从63.2跃升至93.4。在长达23,994帧的仓库场景中，MCBLT的HOTA仅从90.51下降4.58，而基于Kalman滤波的基线则骤降43.35，充分展示了其在长时跟踪中的卓越鲁棒性。

多相机多目标（MTMC）三维跟踪旨在从多个同步且重叠的相机视图中，在三维世界坐标系下持续定位和识别所有感兴趣的目标。该任务在智能交通、安防监控、体育分析等领域具有广泛应用，其核心挑战在于如何有效融合多视图信息，并在长时间跨度内保持目标的身份一致性。

现有MTMC方法可根据多视图信息融合的时机分为三类范式（Figure 1）。第一类为**后期多视图聚合**：在各相机上独立进行2D检测，随后仅依赖外观ReID特征进行跨视图关联。此类方法完全忽视了场景的几何约束，当相机视角差异大或目标外观相似时，关联可靠性急剧下降。第二类为**带几何投影的后期聚合**：在2D检测后引入相机标定信息，通过几何投影约束辅助跨视图匹配。尽管这在一定程度上利用了空间信息，但多视图融合仍发生在检测之后，未能充分利用原始多视图特征之间的互补性。第三类为**早期多视图聚合**：在特征层面直接融合多视图信息，统一推理三维目标。这类方法理论上更具优势，但现有工作（如**EarlyBird**）通常依赖特定场景的固定相机布局进行BEV检测，并结合Kalman滤波与启发式匹配完成跟踪，导致两个关键瓶颈：

**瓶颈一：场景泛化性受限。** 现有早期融合方法针对特定场景设计和训练，当相机数量、视角或场景布局发生变化时，检测性能显著退化，难以快速部署到新环境。

**瓶颈二：长时跟踪的关联鲁棒性不足。** 传统Kalman滤波依赖线性运动假设，在目标频繁遮挡、急停急转等非线性运动场景中容易发生漂移。同时，基于滑动窗口重叠的启发式轨迹匹配策略在处理跨越数千帧的长视频时，窗口间的身份断裂问题突出。实验表明，基于Kalman滤波的基线方法（BEV-KF）在AICity'24仓库场景中，当视频长度从1,000帧扩展到23,994帧时，HOTA指标从63.50骤降至20.15（下降43.35），充分暴露了传统方法在长时关联上的脆弱性（Table 6）。

针对上述瓶颈，本文提出**MCBLT**（Multi-Camera Multi-Object 3D Tracking in Long Videos），一种基于早期多视图聚合的MTMC跟踪框架。其核心动机在于：通过在BEV空间中进行早期多视图特征融合，消除对固定相机布局的依赖，实现可泛化的三维检测；同时，以层级图神经网络在三维世界坐标下直接建模跟踪关联，并引入无需训练的全局合并块替代启发式匹配，从根本上提升长时跟踪的精度与鲁棒性。

## 核心方法与创新机理

MCBLT的核心创新在于将“早期多视图融合—3D空间关联—长时全局跟踪”整合为统一的MTMC框架，系统性地解决了现有方法在相机布局泛化性和长时跟踪鲁棒性上的双重瓶颈。其创新点可凝练为四个相互协同的**changed slots**：

### 1. 检测空间：从各相机独立2D检测到BEV空间的早期多视图融合

传统MTMC方法（如**LMGP**和**ReST**）采用后期多视图聚合策略，即先在各相机视图独立进行2D检测，再通过几何投影或外观特征进行跨视图关联。这种方式对相机布局变化高度敏感，且跨视图关联环节易成为性能瓶颈。MCBLT将检测空间直接迁移至BEV（鸟瞰图）空间，通过**BEVFormer**实现早期多视图特征融合，从根本上消除了对固定相机布局的依赖。

具体而言，多视图图像特征通过**空间交叉注意力编码器（SCA）**聚合到BEV表示：

$$\mathrm{SCA}(Q_p, F_t) = \frac{1}{|\mathcal{V}_{\mathrm{hit}}|} \sum_{i \in \mathcal{V}_{\mathrm{hit}}} \sum_{j=1}^{N_{\mathrm{ref}}} \mathrm{Attn}(Q_p, \mathcal{P}(p,i,j), F_t^i)$$

随后，**时序自注意力编码器（TSA）**融合历史BEV特征以利用时序信息，最终由DETR检测头直接从BEV特征预测3D边界框。这一设计使检测器天然具备跨视图一致性，无需后处理式的跨相机匹配。

### 2. ReID特征提取：2D-3D检测关联算法

直接将3D检测框投影到2D图像提取ReID特征会引入显著的背景噪声，因为投影框往往大于实际目标的2D边界（见Figure 3）。MCBLT提出**2D-3D检测关联模块**，将3D检测框投影至各相机视图后，与独立的2D检测器结果进行匹配，从而获取精确的2D框用于ReID特征提取。

关联的核心是基于下底中心点距离和IoU门控的代价函数：

$$c_{ij} = \begin{cases} \lambda \| \mathbf{bc}_i^{\mathrm{3D}} - \mathbf{bc}_j^{\mathrm{2D}} \|_2, & \mathrm{if } IoU(\mathbf{b}_i^{\mathrm{3D}}, \mathbf{b}_j^{\mathrm{2D}}) \geq 0.1, \\ +\infty, & \mathrm{otherwise} \end{cases}$$

并引入鲁棒性因子$\lambda = \mathbb{1}(v_i^{\mathrm{3D}} \geq v_j^{\mathrm{2D}}) + \alpha \mathbb{1}(v_i^{\mathrm{3D}} < v_j^{\mathrm{2D}})$（$\alpha>1$），以处理遮挡场景下2D框底部低于投影3D框底部的情况。该模块在WildTrack数据集上将IDF1从63.2跃升至93.4（Table 9），证明外观特征质量的提升是跟踪性能的关键杠杆。

### 3. 跟踪方法：从Kalman滤波到层级图神经网络（SUSHI-3D）

基线方法**BEV-KF**和**EarlyBird**采用Kalman滤波器进行运动预测和启发式匹配，在长序列中易发生漂移和身份断裂。MCBLT将跟踪建模为3D世界坐标系下的图神经网络消息传递问题，设计了**SUSHI-3D层级GNN**。

GNN的边特征更新规则为：

$$h_{(i,j)}^{(l)} = \mathcal{N}_e([h_i^{(l-1)}, h_j^{(l-1)}, h_{(i,j)}^{(l-1)}])$$

节点消息计算与聚合分别为：

$$m_{(i,j)}^{(l)} = \mathcal{N}_v([h_i^{(l-1)}, h_{(i,j)}^{(l)}])$$

$$h_i^{(l)} = \Phi(\{m_{(i,j)}^{(l)}\}_{j \in N_i})$$

边特征中显式编码了3D几何距离$(x_i - x_j, y_i - y_j, z_i - z_j)$，不受投影畸变和相机距离缩放影响。这一设计使跟踪器直接在物理世界坐标下推理目标间的时空关系，相较于2D图像空间或投影空间的关联具有天然的几何一致性。

### 4. 长时关联：无需训练的全局合并块

传统方法（如EarlyBird）依赖滑动窗口重叠和启发式轨迹匹配实现长时关联，窗口重叠率的选择对性能影响敏感且缺乏泛化性。MCBLT提出**全局合并块（Global Merging Block）**，在无窗口重叠的情况下，将过去轨迹与新帧预测关联。该模块与层级GNN共享权重，**无需额外训练**，以近在线方式处理长序列。

消融实验（Table 5）表明，全局合并块相比启发式窗口匹配将AICity'24上的HOTA从76.80提升至81.22（+4.42）。在23,994帧的极限长视频测试中（Table 6），MCBLT的HOTA仅从90.51下降至86.03（-4.58），而BEV-KF基线从20.15骤降至-23.20（-43.35），充分验证了全局合并块在长时关联上的鲁棒性优势。

### 5. 辅助创新：场景重新定位

BEV坐标原点的选择对检测器泛化性有显著影响。MCBLT将原点从传统的场景角落改为场景平面中心（重新定位），使WildTrack检测mAP从66.03提升至88.36（Table 8），提升幅度达22.33。结合AICity'24预训练后进一步达到92.03，表明坐标原点选择是跨场景迁移的关键工程细节。

---

**创新协同逻辑**：上述四个核心changed slots形成因果链条——BEV早期融合使检测器泛化且输出3D框→2D-3D关联获取高质量外观特征→3D空间GNN跟踪消除投影畸变→全局合并块实现超长时稳定关联。每个环节解决一个具体瓶颈，组合后产生超越各模块简单叠加的系统性增益。

MCBLT 的整体 pipeline 采用 **早期多视图聚合（early multi-view aggregation）** 范式，将多相机输入统一到鸟瞰图（BEV）空间中进行 3D 检测与跟踪，从而消除对固定相机布局的依赖。如图 2 所示，框架由四个核心阶段串联构成：**BEV 空间 3D 检测**、**2D-3D 检测关联**、**ReID 特征提取** 以及 **层级 GNN 3D 跟踪**。

### 数据流与模块关系

1. **图像主干网络**  
   对于第 $t$ 帧的多视图图像，首先通过共享的图像主干网络（如 ResNet-101）提取各视图的 2D 特征图 $F_t^i$。

2. **BEV 特征构建（空间 & 时序编码器）**  
   - **空间交叉注意力编码器（SCA）** 将多视图 2D 特征聚合到 BEV 空间：对每个 BEV 查询 $Q_p$，利用相机投影矩阵 $\mathcal{P}(p,i,j)$ 在命中视图 $\mathcal{V}_{\text{hit}}$ 上执行可变形注意力，生成当前帧 BEV 特征 $B_t$。  
   - **时序自注意力编码器（TSA）** 进一步融合历史 BEV 特征 $B_{t-1}$ 与当前查询 $Q$，赋予模型时序上下文感知能力。

3. **DETR 检测头**  
   从融合后的 BEV 特征中直接解码出 3D 边界框，输出格式为世界坐标系下的 $(x, y, z, l, w, h, \theta)$。

4. **2D-3D 检测关联模块**  
   将 3D 检测框通过相机投影矩阵 $\mathbf{P}^i$ 反投影到各 2D 视图，与独立的 2D 检测器结果进行匈牙利匹配。关联代价函数结合了下底中心点距离和 IoU 门控，并引入鲁棒性因子 $\lambda$ 处理遮挡场景（当 2D 框底部低于投影 3D 框底部时施加惩罚 $\alpha > 1$）。匹配失败的 3D 检测将被滤除，从而获得精确的 2D 框用于后续 ReID 特征提取。

5. **ReID 特征提取器**  
   基于关联后的 2D 框裁剪图像区域，提取外观特征嵌入。相比直接使用投影 3D 框，该方法能获取更纯净、无背景干扰的 ReID 特征。

6. **SUSHI-3D 层级图神经网络**  
   在 3D 世界坐标下直接建模多目标跟踪。图节点为各帧检测，边特征编码了 3D 几何距离 $(x_i - x_j, y_i - y_j, z_i - z_j)$ 和外观相似度，通过多层消息传递（边更新 → 消息计算 → 节点聚合）学习关联决策。

7. **全局合并块**  
   为处理长视频序列，MCBLT 以步长 $s$ 的近在线方式处理非重叠窗口。全局合并块将过去已确认的轨迹与当前窗口的新检测进行关联，**无需窗口重叠和启发式匹配**，且与层级 GNN 共享权重，无需额外训练。这一设计是长时跟踪鲁棒性的关键支撑——在 AICity'24 上，全局合并块相比启发式窗口匹配将 HOTA 从 76.80 提升至 81.22（Table 5）。

### 关键设计决策

框架的核心洞察在于将 **多视图融合前置到检测阶段**：通过 BEVFormer 式的空间-时序注意力机制，在早期就将多相机特征统一到场景级表示中。这不仅使检测器对相机布局变化具有天然泛化性，还为后续的 3D 跟踪提供了统一的坐标基准，避免了传统后期聚合方法中跨视图关联的级联误差。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2412_00692/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of MCBLT. First, multi-view images at frame t are passed through the image backbone to obtain multiview image features. A spatial encoder is then introduced to aggregate multi-view image features to BEV features B _ { t } , followed by a temporal encoder to aggregate BEV features within a temporal window. A DETR-based decoder is utilized to obtain object detection results, which are in the format of 3D bounding boxes. To get reliable ReID features for the detected objects, a ReID feature extraction module is proposed, including a 2D ReID feature extractor and a 2D-3D detection association algorithm. Finally, SUSHI-3D is designed to achieve multi-object tracking in BEV...*

### 3.1 坐标系统与投影

MCBLT 的统一跟踪框架建立在三个坐标系的精确转换之上：世界坐标系 $\mathbf{W}$、相机坐标系 $\mathbf{C}^i$ 和像素坐标系 $\mathbf{I}^i$。给定第 $i$ 个相机的内参矩阵 $\mathbf{K}^i$、旋转矩阵 $\mathbf{R}^i$ 和平移向量 $\mathbf{t}^i$，世界坐标系中的 3D 点 $\mathbf{x}$ 到像素坐标 $\mathbf{u}$ 的投影为：

$$s \left( \mathbf{u} \right) = \mathbf{P}^{i} \left( \mathbf{x} \right) = \mathbf{K}^{i} \left[ \mathbf{R}^{i} | \mathbf{t}^{i} \right]_{3 \times 4} \left( \mathbf{x} \right)$$

其中 $s$ 为尺度因子。这一投影关系是整个框架中多视图融合、检测关联和 3D 推理的基础。

### 3.2 基于 BEVFormer 的多视图 3D 检测

MCBLT 的检测模块采用 BEVFormer 架构，在鸟瞰图（BEV）空间中进行早期多视图特征融合。其核心由两个编码器构成：

**空间交叉注意力编码器 (SCA)** 将多视图图像特征聚合到 BEV 查询 $Q_p$ 上。对每个 BEV 查询，通过投影矩阵 $\mathcal{P}$ 在命中视图集 $\mathcal{V}_{\text{hit}}$ 上采样 $N_{\text{ref}}$ 个参考点，利用可变形注意力聚合图像特征 $F_t^i$：

$$\mathrm{SCA}(Q_p, F_t) = \frac{1}{|\mathcal{V}_{\mathrm{hit}}|} \sum_{i \in \mathcal{V}_{\mathrm{hit}}} \sum_{j=1}^{N_{\mathrm{ref}}} \mathrm{Attn}(Q_p, \mathcal{P}(p,i,j), F_t^i)$$

**时序自注意力编码器 (TSA)** 则融合历史 BEV 特征 $B_{t-1}$ 与当前查询 $Q$，以利用时序信息增强检测稳定性：

$$\mathrm{TSA}(Q_p, Q, B_{t-1}) = \sum_{S \in \{Q, B_{t-1}\}} \mathrm{Attn}(Q_p, p, S)$$

经上述编码器处理后，DETR 检测头从 BEV 特征中直接预测 3D 边界框。这种早期融合策略消除了对固定相机布局的依赖，使检测器能够泛化到不同相机数量和视角的场景。

### 3.3 2D-3D 检测关联与 ReID 特征提取

由于 3D 检测框投影到 2D 图像时往往无法精确贴合目标边界（Figure 3），直接使用投影框提取外观特征会引入背景噪声。MCBLT 提出 2D-3D 检测关联算法来解决这一问题。

关联代价函数基于下底中心点距离和 IoU 门控：

$$c_{ij} = \begin{cases} \lambda \| \mathbf{bc}_i^{\mathrm{3D}} - \mathbf{bc}_j^{\mathrm{2D}} \|_2, & \mathrm{if } IoU(\mathbf{b}_i^{\mathrm{3D}}, \mathbf{b}_j^{\mathrm{2D}}) \geq 0.1, \\ +\infty, & \mathrm{otherwise} \end{cases}$$

其中 $\mathbf{bc}_i^{\mathrm{3D}}$ 和 $\mathbf{bc}_j^{\mathrm{2D}}$ 分别为 3D 投影框和 2D 检测框的下底中心点坐标。为处理遮挡场景，引入鲁棒性因子：

$$\lambda = \mathbb{1}(v_i^{\mathrm{3D}} \geq v_j^{\mathrm{2D}}) + \alpha \mathbb{1}(v_i^{\mathrm{3D}} < v_j^{\mathrm{2D}})$$

其中 $v$ 表示框底部的垂直像素坐标，$\alpha > 1$。当 2D 框底部低于 3D 投影框底部时（通常意味着遮挡），施加额外惩罚。最终通过匈牙利算法求解最优匹配，并移除无法与任何 2D 检测匹配的 3D 检测，从而获得精确的 2D 框用于 ReID 特征提取。

### 3.4 SUSHI-3D：层级图神经网络跟踪

MCBLT 在 3D 世界坐标下直接进行多目标跟踪，采用层级图神经网络 SUSHI-3D。图结构以检测目标为节点，以帧间关联为边。

**边特征更新**：第 $l$ 层的边嵌入 $h_{(i,j)}^{(l)}$ 由两个节点和上一层边嵌入拼接后经神经网络 $\mathcal{N}_e$ 更新：

$$h_{(i,j)}^{(l)} = \mathcal{N}_e([h_i^{(l-1)}, h_j^{(l-1)}, h_{(i,j)}^{(l-1)}])$$

**消息计算**：从边到节点的消息由节点和更新后的边嵌入计算：

$$m_{(i,j)}^{(l)} = \mathcal{N}_v([h_i^{(l-1)}, h_{(i,j)}^{(l)}])$$

**节点更新**：通过聚合邻居边的消息更新节点嵌入，$\Phi$ 可以是求和、最大值或平均：

$$h_i^{(l)} = \Phi(\{m_{(i,j)}^{(l)}\}_{j \in N_i})$$

**3D 几何距离编码**：边特征中包含 3D 中心点距离 $(x_i - x_j, y_i - y_j, z_i - z_j)$，这不受投影畸变和相机距离缩放的影响，为关联提供了稳定的几何线索。

**全局合并块**：为实现长时跟踪，MCBLT 以近在线方式处理长序列（步长 $s$），但不使用滑动窗口重叠和启发式匹配。取而代之的是全局合并块，它将过去轨迹与新帧的预测直接关联，与层级 GNN 共享权重且无需额外训练，从根本上解决了长视频中身份断裂的问题。

## 实验与关键发现

### 核心性能与SOTA对比

MCBLT在两个主流MTMC基准上均取得领先结果。在**AICity'24测试集**上，MCBLT以HOTA 81.22达到SOTA（Table 1），显著超越其他方法。该数据集覆盖仓库、零售店和医院三种场景，相机数量和视角差异大，验证了方法的泛化性。在**WildTrack测试集**上，MCBLT以IDF1 93.4超越此前最优的**EarlyBird**（IDF1 92.3），提升+1.1；当使用与EarlyBird完全相同的检测输入（MCBLT†）进行公平对比时，IDF1进一步达到95.6，提升+3.3（Table 3）。这一公平性设计确保性能增益来自跟踪方法本身而非检测器差异。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2412_00692/figures/006_Figure_5.jpg]]
*Figure 5: Visualization of MTMC detection and tracking results for three different scenes in AICity’24 test set. The tracked objects are shown as colored dots in the BEV floor plans, and object 3D bounding boxes are projected and drawn in each camera view. Table 1. Results on AICity’24 test set. The first place is in bold, and the second place is underlined*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2412_00692/figures/007_Table_3.jpg]]
*Table 3: Results on WildTrack test set. The first place is in bold, and the second place is underlined. † uses the same detections as EarlyBird [30]*

### 长时跟踪鲁棒性

MCBLT在长视频场景中展现出显著优势。在AICity'24仓库场景的23994帧长序列上，MCBLT的HOTA为90.51，而基于BEVFormer检测+Kalman滤波器的基线**BEV-KF**仅20.15，差距高达+70.36（Table 6）。更关键的是，当视频从1000帧增长至23994帧时，MCBLT的HOTA仅下降4.58，而BEV-KF下降43.35，表明层级GNN与全局合并块在长时关联中的鲁棒性远超传统Kalman滤波方法。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2412_00692/figures/011_Table_5.jpg]]
*Table 5: SUSHI inference ablation on the AICity’24 test set. Rows 1 to 4 rely on heuristic matching to track overlapping sliding windows inferred by the SUSHI GNN hierarchy. Our final tracking solution (the last row) applies a global merging block to associate without graph overlaps. Table 6. Tracking comparisons with increasing video lengths from a warehouse scene in AICity’24 dataset. The baseline BEV-KF is based on the detection results from BEVFormer processed by a Kalman filter based tracker [33] used in EarlyBird [30]*

### 关键模块消融

**全局合并块**是长时关联的核心设计。在AICity'24测试集上，将启发式窗口匹配替换为无需额外训练的全局合并块后，HOTA从76.80提升至81.22，提升幅度达4.42（Table 5）。该模块无需滑动窗口重叠，直接关联历史轨迹与新帧预测，且与层级GNN共享学习权重。

**2D-3D检测关联算法**对ReID特征质量的影响极为显著。在WildTrack上，引入该模块后IDF1从63.2跃升至93.4（提升+30.2），MOTA从73.4升至87.5（Table 9）。该模块通过将3D检测投影回2D并与2D检测匹配，获取更精确的2D框以提取纯净外观特征，有效避免了投影框不精确导致的特征污染。

**场景重新定位**大幅提升检测性能。将BEV坐标原点从场景角落移至平面中心后，WildTrack检测mAP从66.03提升至88.36（+22.33）；结合AICity'24预训练后进一步达到92.03（Table 8）。这一改进通过优化坐标数值范围提升了模型训练的数值稳定性。

**检测器配置**方面，在AICity'24验证集上，ResNet-101骨干的BEVFormer检测mAP达88.64，优于其他配置（Table 7）。

### 检测关联准确率

2D-3D检测关联算法在不同场景下表现稳健：仓库99.4%、零售店95.2%、医院91.2%，总体96.9%（Table 2）。医院场景准确率相对较低，可能与遮挡和光照条件更复杂有关。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2412_00692/figures/008_Table_2.jpg]]
*Table 2: Detection association accuracy among different scene types on AICity’24 dataset*

### 效率与局限性

MCBLT在NVIDIA A100上的端到端推理速度约为1.5 FPS（Table 11），暂不适合实时应用。在大规模场景中使用更大图像骨干（如V2-99）时受GPU显存限制。ReID特征在真实数据集WildTrack上的质量明显低于合成数据集AICity'24（Table 10），表明对真实噪声和光照变化的鲁棒性仍有提升空间。层级GNN跟踪流程为近在线方式，并非严格在线跟踪。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2412_00692/figures/010_Table_4.jpg]]
*Table 4: Ablation studies on the configurations of our multi-view object detector. The evaluation is done on the customized validation set of the AICity’24 dataset*

## 定位与知识库关联

### 1. 方法范式定位

MCBLT 属于**早期多视图聚合（Early Multi-View Aggregation）范式**的 MTMC 三维跟踪方法。现有 MTMC 方法可按多视图信息融合的时机分为三类（Figure 1）：

- **后期多视图聚合（Late Aggregation）**：各相机独立进行 2D 检测，再通过外观 ReID 进行跨视图关联。此类方法完全依赖外观特征质量，在遮挡和密集场景下鲁棒性不足。
- **带几何投影的后期聚合（Late Aggregation with Geometric Projection）**：在后期聚合基础上引入相机几何约束辅助跨视图匹配，如 **LMGP** 和 **ReST**。这类方法部分缓解了纯外观关联的脆弱性，但检测本身仍局限于 2D 空间，未从根本上利用多视图几何一致性。
- **早期多视图聚合（Early Aggregation）**：在特征层面融合多视图信息，直接在统一的三维空间中进行检测和跟踪。**EarlyBird** 是该范式的代表性工作，但存在两个关键局限：（1）其 BEV 检测依赖固定场景的相机布局，泛化性受限；（2）跟踪采用 Kalman 滤波 + 启发式匹配，在长视频中易发生漂移和身份断裂。

MCBLT 在早期聚合范式的基础上实现了两个根本性突破：**场景可泛化的 BEV 检测**和**层级 GNN 驱动的长时三维跟踪**，从而大幅提升了 MTMC 系统的泛化性和长时关联鲁棒性。

### 2. 与关键基线的方法论对比

#### 2.1 与 EarlyBird 的对比

**EarlyBird** 是早期多视图融合 MTMC 的代表性工作，也是 MCBLT 最直接的对比基线。二者在以下维度存在根本差异：

| 维度 | EarlyBird | MCBLT |
|------|-----------|-------|
| **检测空间** | 固定场景 BEV 检测 | 场景可泛化的 BEVFormer 检测 |
| **ReID 特征提取** | 直接投影 3D 框提取特征 | 2D-3D 检测关联获取精确 2D 框后提取 |
| **跟踪方法** | Kalman 滤波 + 启发式匹配 | 层级 GNN（SUSHI-3D）在 3D 空间跟踪 |
| **长时关联** | 滑动窗口重叠 + 启发式轨迹匹配 | 无需重叠的全局合并块 |
| **BEV 坐标原点** | 场景角落 | 场景平面中心（重新定位） |

在 WildTrack 数据集上，当使用与 EarlyBird 完全相同的 3D 检测结果时（MCBLT†），MCBLT 的 IDF1 达到 95.6，比 EarlyBird 的 92.3 高出 **+3.3**（Table 3），证明跟踪性能的提升完全来自关联方法而非检测器。在 AICity'24 仓库场景的 23,994 帧长视频上，MCBLT 的 HOTA 为 90.51，而基于 Kalman 滤波的 BEV-KF 基线仅为 20.15，差距达 **+70.36**（Table 6），凸显了 GNN 跟踪在长时场景下的压倒性优势。

#### 2.2 与后期聚合方法的对比

**LMGP** 和 **ReST** 等后期聚合方法虽然在跨视图关联中引入了几何约束，但其检测阶段仍独立于多视图一致性。MCBLT 通过 BEVFormer 的空间交叉注意力机制（Equation 2）在特征层面实现多视图融合，使得检测本身即受益于多视角信息的互补，从根本上避免了后期匹配中的歧义性。在 AICity'24 测试集上，MCBLT 的 HOTA 达到 81.22（SOTA），远超所有后期聚合方法（Table 1）。

#### 2.3 与 BEV-KF 基线的对比

**BEV-KF** 是 MCBLT 自行构建的消融基线，采用 BEVFormer 检测 + Kalman 滤波跟踪的组合。该基线用于隔离跟踪方法的影响。实验表明，随着视频长度从 1,000 帧增长到 23,994 帧，BEV-KF 的 HOTA 从 63.50 骤降至 20.15（下降 43.35），而 MCBLT 仅从 95.09 降至 90.51（下降 4.58）（Table 6）。这直接证明了 Kalman 滤波在长时跟踪中的根本性缺陷——其线性运动假设和启发式关联策略无法应对长序列中的累积误差和复杂遮挡。

### 3. 适用边界与局限性

#### 3.1 场景泛化边界

MCBLT 在 AICity'24 的仓库、零售店、医院三种场景和 WildTrack 的户外场景上均取得了 SOTA 性能，证明了其对不同相机布局和场景类型的泛化能力。场景重新定位策略（将 BEV 坐标原点移至场景平面中心）是泛化性的关键使能因素：在 WildTrack 上，重新定位使检测 mAP 从 66.03 提升至 88.36（+22.33）（Table 8）。然而，该方法在完全不同的室内建筑结构（如多层建筑、非平面地面）下的泛化能力尚未验证，可能需要额外的场景自适应机制。

#### 3.2 计算效率边界

MCBLT 的端到端推理速度约为 **1.5 FPS**（NVIDIA A100 GPU）（Table 11），暂不适合实时性要求高的应用场景。当使用更大规模的图像骨干（如 V2-99）时，受 GPU 显存限制，难以同时处理大量相机视图。这是早期多视图融合范式的固有代价——BEV 空间的特征聚合需要同时加载所有视图的特征图。

#### 3.3 ReID 特征质量边界

2D-3D 检测关联算法大幅提升了 ReID 特征质量，使 WildTrack 上的 IDF1 从 63.2 跃升至 93.4（Table 9）。但 ReID 特征在真实世界数据集（WildTrack）上的质量仍明显低于合成数据集（AICity'24），表明模型对真实噪声、光照变化和遮挡的鲁棒性仍有提升空间（Table 10）。

#### 3.4 在线性边界

MCBLT 的层级 GNN 跟踪流程为**近在线（near-online）**方式，以步长 s 处理非重叠帧窗口，并非严格的逐帧在线跟踪。全局合并块虽然无需窗口重叠，但仍需等待一个窗口内的帧全部处理完毕才能进行关联。

### 4. 开放问题

1. **运动模型深化**：当前 SUSHI-3D 的边特征仅包含 3D 中心点距离编码（Equation 9），如何设计更复杂的运动模型（如速度、加速度、运动方向）以进一步提升 3D GNN 跟踪的鲁棒性，是明确的改进方向。

2. **推理速度优化**：能否通过模型压缩、BEV 特征选择或轻量化骨干网络，在保持跟踪精度的同时大幅提升推理速度，是走向实际部署的关键问题。

3. **跨域 ReID 鲁棒性**：如何进一步改进 ReID 特征提取（如引入域自适应或数据增强策略），以缩小合成数据与真实数据之间的性能差距，是提升真实场景性能的重要方向。

4. **极端场景泛化**：在完全不同的室内环境（如多层建筑、非平面地面、极端光照条件）下，MCBLT 的泛化能力是否需要额外的场景自适应机制或在线标定策略，仍需进一步研究。

## 原文 PDF

![[paperPDFs/ICCV_2025/MCBLT_Multi_Camera_Multi_Object_3D_Tracking_in_Long_Videos.pdf]]
