---
title: "AbdCTBench: Learning Clinical Biomarker Representations from Abdominal Surface Geometry"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AbdCTBench_Learning_Clinical_Biomarker_Representations_from_Abdominal_Surface_Geometry.pdf
aliases:
- AB2
- AbdCTBench
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/health
core_operator: "利用腹部外部表面几何形状（2D深度图投影）作为间接观测变量，推断内部体成分生物标志物。"
primary_logic: "外部体表几何与内部组织成分具有可学习的预测关联，计算机视觉模型可从2D表面网格中提取表征，实现非侵入式生物标志物预测。"
claims:
- "仅用外部表面几何，年龄预测MAE可达6.22岁（R²=0.757），远优于随机基线MAE 13.16。"
- "ResNet-18在死亡率预测中达到AUROC 0.839。"
- "Swin Transformer-Base在糖尿病伴慢性并发症（HCC-18）检测中达到AUROC 0.801。"
- "所有深度学习架构在各任务上均显著优于naive baseline（AUROC≈0.5，Age MAE 13.16）。"
---

# AbdCTBench: Learning Clinical Biomarker Representations from Abdominal Surface Geometry

> [!tip] 核心洞察
> 外部体表几何与内部组织成分具有可学习的预测关联，计算机视觉模型可从2D表面网格中提取表征，实现非侵入式生物标志物预测。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AbdCTBench：从腹部表面几何学习临床生物标志物表示 |
| 英文题名 | AbdCTBench: Learning Clinical Biomarker Representations from Abdominal Surface Geometry |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=dKRAo0a9Gm); [Project](https://stair-lab.github.io/AbdCTBench/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/health |
| Method | AbdCTBench Benchmark (基于2D腹部表面网格的单目标生物标志物预测基准) |
| Dataset | Age prediction (regression), Calcium Scoring Abdominal Agatston (binary), Mortality prediction (binary), Type-2 Diabetes (binary) |

> [!tip] 效果简介
> - Age prediction (regression) 上，MAE (years) 为 6.223 (EfficientNet-B0)，对比 13.16 (Naive Baseline)，变化 -6.937。
> - Calcium Scoring Abdominal Agatston (binary) 上，AUROC 为 0.848 (ResNet-34)，对比 0.5 (Naive Baseline)，变化 +0.348。
> - Mortality prediction (binary) 上，AUROC 为 0.839 (ResNet-18)，对比 0.5 (Naive Baseline)，变化 +0.339。

## 概述

传统基于CT和MRI的影像学生物标志物获取方法存在辐射暴露、高成本和设备可及性障碍，难以应用于大规模常规筛查。本文提出利用腹部外部表面几何形状（二维深度图投影）作为间接观测变量，通过计算机视觉模型学习外部体表几何与内部体成分生物标志物之间的预测关联，从而实现非侵入式的关键生物标志物推断。

为此，构建了**AbdCTBench**基准，以统一的单目标学习框架系统评估多种深度学习架构在该任务上的表现。该基准使用从CT衍生并可在消费级设备上生成的2D腹部表面网格图像作为输入，预测年龄、骨密度、代谢疾病风险等16个临床生物标志物。

核心实验结果表明，仅依靠外部表面几何，模型即可获得远超随机基线的预测性能：
- 年龄回归任务的最佳平均绝对误差（MAE）低至**6.22岁**（决定系数$R^2=0.757$），而随机基线MAE为13.16岁；
- 死亡率预测最优AUROC达到**0.839**；
- 糖尿病伴慢性并发症检测最优AUROC达到**0.801**；
- 在所有分类任务上，各深度模型AUROC均显著优于naive baseline的≈0.5。

这些结果验证了从表面几何推断内部生物标志物的可行性，为利用消费级深度传感器进行大规模、低风险的健康筛查提供了概念验证和实验基准。

## 背景与动机

医学影像学中，体成分生物标志物（如骨密度、脂肪分布、肌肉质量等）的评估对疾病风险分层和健康管理至关重要。传统上，这些指标依赖计算机断层扫描（CT）或磁共振成像（MRI）等高级模态进行量化。然而，CT 检查存在电离辐射暴露风险，MRI 则成本高昂且设备可及性有限，二者均无法支撑大规模常规人群筛查的需求。这一可及性鸿沟构成了影像学生物标志物从精密临床工具走向全民健康监测的核心瓶颈。

在此背景下，一个关键观察是：人体外部体表几何与内部组织成分之间存在可建模的关联。AbdCTBench 工作提出了一种全新的通路——利用腹部外部表面三维形状的二维投影（即深度图风格的表面网格图像）作为间接观测变量，通过计算机视觉模型推断内部体成分生物标志物。论文构建了一个系统的基准测试，将 CT DICOM 序列转化为 2D 表面网格图像（384×384 的 PNG 图像），并以 CT 衍生的 16 项生物标志物（通过 OSCAR 系统计算）作为训练目标，要求模型仅从外部几何中学习这些内部指标。该研究进一步设计了单目标学习框架，对每一项生物标志物独立训练分类或回归模型，并引入逆频率加权、均衡批次采样和阈值优化等类别不平衡处理策略。

初步实验结果表明，这一"由表及里"的预测通路具有实质性可行性：即便仅使用不含任何内部密度信息的表面几何，年龄预测的平均绝对误差（MAE）即可达到 6.22 岁（$R^2=0.757$），远优于随机基线的 MAE 13.16 岁；死亡率预测的 AUROC 可达 0.839（ResNet-18）；糖尿病伴慢性并发症（HCC-18）检测的 AUROC 达到 0.801（Swin Transformer-Base）。所有被评估的深度学习架构（ResNet、EfficientNet、ViT-Small、Swin Transformer 等）在各任务上均显著优于随机猜测基线（AUROC≈0.5），从而证实外部体表几何确实携带了足以支持临床推理的信号。该基准的建立为后续探索在消费级深度传感器（如智能手机 LiDAR）上重建腹部表面、实现零辐射体成分筛查奠定了评估框架与模型基础。

## 核心创新

本工作的核心创新在于将**输入数据模态**从传统临床影像（CT/MRI）替换为**从CT衍生、并可被消费级设备生成的2D腹部表面网格图像**（深度图投影），使模型绕开辐射暴露与设备可及性障碍，直接从外部体表几何推断内部体成分生物标志物。这一"changed slot"是整个方法的逻辑枢纽：表面几何作为间接观测变量，替代了传统成像所需的昂贵原始数据，打开了大规模常规筛查的可能性（Abstract: bridging the gap between high-precision clinical imaging and widely accessible consumer technology）。

围绕该模态转换，工作从三个方面验证了创新的有效性：

1. **预测关联的存在性**：所有深度学习架构在各任务上均显著优于随机基线（Naive Baseline AUROC≈0.5，Age MAE 13.16），确认了外部体表几何与内部组织成分之间的可学习映射关系。定性上，Grad-CAM可视化（Figure 7）进一步显示ResNet-18在预测糖尿病慢性并发症（HCC-18）时，能稳定聚焦于腹部表面几何的关键区域，为表征的可解释性提供了初步证据。

2. **预测能力的量化上限**：表1与表2的系统基准测试给出了当前可行区间。Age预测中EfficientNet-B0达到MAE 6.22年、$R^2=0.757$；Mortality预测中ResNet-18达到AUROC 0.839；HCC-18检测中Swin Transformer-Base达到AUROC 0.801。这些数值构成了"表面→内部"预测的证据锚点，同时表明该模态转换保留了足够的临床相关信息。

3. **技术路径的可行性**：整条流水线——从DICOM到3D STL网格（表面提取）、再渲染为384×384的2D PNG图像——已标准化为可复现的计算流程（Section 3.1）。在此基础上，构建了单目标学习框架（Single-Target Learning Framework），通过逆频率加权、均衡批次采样与阈值优化处理类别不平衡，使得标准CV架构无需特定架构定制即可直接用于该新模态，极大地降低了方法采纳成本。

在方法学层面，创新不体现在提出新模型架构，而在于**问题重定义本身**：将临床生物标志物预测刻画为一个可从表面几何单模态求解的视觉任务，并通过系统基准证实了其成立条件。消融实验的附加发现（多任务联合训练导致Age MAE从6.22升至14.53，其他AUROC普遍低于0.63）也从另一侧面印证了该问题的几何约束形态——表面特征对不同生物标志物的预测信号具有特异性，简单共享表征会引发强烈负迁移（需手动核验该结论是否完全成立）。

当前创新仍受限于数据集来源（单一医疗机构CT扫描）以及表面网格的实际生成方式（衍生自CT而非消费级深度传感器）。在真实LiDAR或结构光重建的腹部网格上验证，将直接决定该模态替换能否从概念验证走向部署闭环。

## 整体框架

![[assets/figures/papers/iclr26_0005_dKRAo0a9Gm_AbdCTBench_Learning_Clinical_Biomarker_Represent/figures/005_Figure_2.jpg]]
*Figure 2: AbdCTBench dataset overview showing the pipeline from CT scans to surface mesh extraction and biomarker prediction*

AbdCTBench 的设计目标是为"从腹部体表几何推断内部体成分生物标志物"这一任务建立一个可复现的基准。整体流程将 CT 影像转化为标准化输入-标签对，再通过单目标学习框架统一评估多种视觉架构的预测能力。框架由三个核心模块串联而成：

1. **表面网格提取与渲染**  
   输入为腹部 CT 的 DICOM 序列。首先对体积数据进行各向异性平滑（CurvatureAnisotropicDiffusion）与可选收缩，随后利用 VTK/Marching-Cubes 提取 3D 三角面片网格，最后将 3D 表面渲染为 384×384 的 2D 深度图投影（PNG）。该步骤将原始 CT 转化为不含辐射信息的纯几何表示，是连接临床影像与消费级深度传感器预期输入的桥梁（Section 3.1，Figure 2）。

2. **CT 衍生生物标志物计算**  
   同一批 CT 数据经 **OSCAR**（Pickhardt et al., 2020）自动化处理，输出 16 个体成分生物标志物，包括内脏/皮下脂肪面积、肌肉指数、骨密度、主动脉钙化积分等。这些生物标志物随后被二值化（用于分类）或直接保留连续值（用于回归），作为单目标学习的监督信号（Section 3.1，Table 5）。

3. **单目标学习框架**  
   对每一个生物标志物分别训练独立的分类或回归模型。输入为步骤 1 生成的 2D 表面网格图像，标签为步骤 2 计算得到的对应生物标志物。框架统一采用 AdamW（weight decay $1\times10^{-4}$）、余弦退火学习率调度、batch size 16、训练 100 epoch 并配合 early stopping（patience 10）与 dropout 0.2。为缓解严重的类别不平衡，引入三项策略：**逆频率加权**损失、**均衡批次采样**、以及基于验证集的 **F1-最优阈值** 选择（Section 4.2 & 4.3）。所有模型按此协议训练，以保证不同架构间的可比性。

上述模块使得整个基准从"原始 CT → 表面图像 + 临床金标准"的管线完全固定，之后即可插拔式替换 CNN（ResNet、EfficientNet、DenseNet 等）或 Vision Transformer（ViT-DINOv2、Swin）等 backbone，衡量其从外部几何捕获内部病理信息的能力。多目标联合训练的初步尝试则揭示出显著的负迁移（Age MAE 从单任务 6.2 升至 14.5 年，AUROC 普遍低于 0.63），因此当前版本仍以单目标设置作为标准基准（Appendix A.6）。

## 核心模块与公式推导

本文未引入新的数学公式推导，研究工作聚焦于构建基准实验和学习框架，因此本节重点介绍构成AbdCTBench的三个核心流程模块及其组合方式。

---

### 模块一：表面网格提取与渲染（DICOM → 2D 图像）

原始 CT 检查产生的 DICOM 序列首先通过标准化体数据处理（可选收缩、各向异性平滑等预处理）生成腹腔区域的三角网格。网格以 STL 格式保存后，再被渲染为固定分辨率为 384×384 的 2D 深度图投影，即"表面网格图像"。该模块的输出是计算机视觉模型可读取的 PNG 图像，其像素值编码了外部腹部几何信息，从而替代直接的 CT 体素数据，规避了辐射暴露和高端设备依赖。

### 模块二：CT 衍生的生物标志物计算（OSCAR）

同一批 CT 数据经 Pickhardt 等人开发的 OSCAR 系统处理，自动计算出包含骨密度、肌肉组成、皮下脂肪/内脏脂肪分布等 16 项内部体成分生物标志物。这些量化值作为训练的监督信号（ground truth）。其计算逻辑独立于表面网格生成，保证每个样本的外部表面几何与内部组分之间的关联可以通过后续学习被捕捉，且两者之间不存在简单的公式映射。

### 模块三：单目标学习框架与非平衡处理

AbdCTBench 为每个生物标志物独立训练一个分类或回归模型（单目标学习），不共享参数。所有模型采用统一的训练协议，主要技术栈为：

- **优化器**：AdamW，权重衰减 1e-4，配合余弦退火学习率调度。
- **损失函数**：二分类任务使用带 logits 的二元交叉熵损失；年龄预测回归任务使用均方误差（MSE）。
- **类别不平衡缓解**：组合使用逆频率加权损失、均衡批次采样和基于验证集 F1-最优阈值的决策阈值优化。
- **正则化**：Dropout（rate=0.2），早停（patience=10 epochs），训练上限 100 epochs。

该框架本身没有引入新的理论推导，其核心在于实验性地探明"从表面几何到内部生物标志物"这一映射是否可被现有视觉架构学习，并提供了标准化的比较环境。辅助消融显示，改成多任务共享主干网络后性能显著退化（年龄 MAE 升至 14.53，分类 AUROC 普遍低于 0.63），提示当前模板下的负迁移效应，关于多目标学习还需进一步方法探索。

## 实验与分析

### 主要结果：单目标生物标志物预测

**年龄预测（回归）**：所有架构均显著优于随机基线（MAE 13.16），其中EfficientNet-B0获得最低MAE 6.223（95% CI 6.012–6.389），对应$R^2=0.757$（Table 1）。该结果表明，仅从腹部表面几何便能提取与生理年龄高度相关的表征，预测误差约6年，远低于盲猜的13年。ResNet-18和ResNet-34的MAE分别为6.47和6.53，接近最优。RadImageNet预训练的ResNet-50（MAE 6.57）未取得明显优势，提示领域预训练在小规模表面图像任务上的增益有限。

![[assets/figures/papers/iclr26_0005_dKRAo0a9Gm_AbdCTBench_Learning_Clinical_Biomarker_Represent/figures/006_Table_1.jpg]]
*Table 1: Results for non-HCC biomarkers by architecture on the test set. AUROC is reported for the binary classification tasks and MAE is reported for Age prediction (regression task). Bootstrapped 95% CIs are reported in parentheses*

**二分类任务**：在主要的临床标志物上，ResNet系列和EfficientNet-B0交替取得最优AUROC（Table 1）。钙化积分（Calcium Score）预测上，ResNet-34以AUROC 0.848（0.832–0.862）最优；死亡率（Mortality）预测上，ResNet-18达到0.839（0.816–0.861）；2型糖尿病（T2D）上，ResNet-34达到0.742（0.722–0.761）。心肌梗死（MI）预测中Swin-Transformer-Base以0.742（0.709–0.773）最优，但相比CNN优势不大。所有模型在这些任务上均比随机基线（≈0.5）有大幅提升，证实体表几何与内部病变存在可学习的关联。

**HCC合并症编码**：模型在Hierarchical Condition Categories（HCC）编码预测上也表现出显著判别力（Table 2）。对于糖尿病伴慢性并发症（HCC-18），Swin-Transformer-Base取得AUROC 0.801（0.780–0.822）；对于血管疾病（HCC-108）和房颤（HCC-96），Swin分别获得0.768和0.770。ResNet-18在心肌梗死相关HCC（HCC-111）上更优（0.758），而HCC-12（较少见的神经精神合并症）上所有模型AUROC均未超过0.661，说明低流行率和特征关联弱限制了表面几何的表征能力。总体来看，视觉Transformer在处理全局、多区域特征上有一定优势，但与CNN的差距并不显著。

![[assets/figures/papers/iclr26_0005_dKRAo0a9Gm_AbdCTBench_Learning_Clinical_Biomarker_Represent/figures/007_Table_2.jpg]]
*Table 2: Results for HCC code biomarkers by architecture on the test set. All biomarkers report AUROC. Bootstrapped 95% CIs are reported in parentheses*

**性别分层公平性**：性别分层测试（Table 3）显示，年龄预测上女性MAE高出男性约0.87岁（6.63 vs 5.76），可能是由于女性体脂分布差异引入的系统偏差。其他任务上性别间的AUROC差异较小（绝对值差异多<0.03），模型整体未表现出严重的性别偏见，但仍需进一步校准以弥补年龄任务上的缺口。

![[assets/figures/papers/iclr26_0005_dKRAo0a9Gm_AbdCTBench_Learning_Clinical_Biomarker_Represent/figures/008_Table_3.jpg]]
*Table 3: Gender-stratified performance metrics on the test set. Bootstrapped 95% CIs are shown in parentheses*

### 消融与稳健性分析

**多任务学习 vs. 单任务**：为探索多目标联合训练能否共享几何表征，对ResNet-18/34/50（RadImageNet）实施了覆盖所有10个生物标志物的多任务学习框架（使用GradNorm平衡梯度，以中位AUROC选择模型）。结果显示，多任务学习在所有任务上均大幅劣于单任务学习（附录 A.6）。以ResNet-18为例，年龄预测MAE从单任务的6.47恶化为14.53，钙化积分AUROC从0.843降至0.615，死亡率AUROC从0.839降至0.590（Table 17–18）。说明不同生物标志物所依赖的表面几何线索存在显著冲突，共享骨干导致了严重的负迁移。当前多任务设置无法直接提升性能，需要更精细的任务分组或解耦策略。

![[assets/figures/papers/iclr26_0005_dKRAo0a9Gm_AbdCTBench_Learning_Clinical_Biomarker_Represent/figures/052_Table_17.jpg]]
*Table 17: Multi-task learning results for non-HCC biomarkers by architecture on the test set. AU-ROC is reported for the binary classification tasks. MAE is reported for Age prediction (regression task). Bootstrapped 95% CIs are shown in parentheses*

**随机种子敏感性**：使用三个随机种子（42, 43, 44）重复所有关键实验，性能波动均在自助法（bootstrap）95%置信区间内（附录 A.5），表明训练过程和结论是稳定的，不依赖于特定初始化。

**模型选择趋势**：轻量级架构（ResNet-18、EfficientNet-B0）在多数任务上接近甚至优于更深的ResNet-34/50，暗示任务难度并未完全受益于模型容量增加，过拟合风险小但特征表示已饱和。RadImageNet预训练的医学影像模型未带来一致提升，说明自然图像预训练的CNN从表面几何中提取纹理与轮廓特征已足够，领域预训练的优势在此类合成图像上不明显。

### 失败模式与局限

1. **多任务联合训练的负迁移**：已如前述，直接联合所有任务导致性能崩溃，是当前最主要的方法失败。原因可能在于各生物标志物关联的表面区域差异大（例如年龄可能依赖整体体型，而钙化积分可能依赖特定断面轮廓），强行共享导致梯度冲突。
2. **低流行率疾病表现差**：HCC-12等罕见合并症AUROC整体偏低（<0.66），样本量不足和特征信号弱限制了模型的泛化。在极端类别不平衡条件下，尽管采用了逆频率加权和均衡批次采样，部分任务仍存在高召回、低精度问题，需要更系统的校准策略。
3. **跨机构泛化未知**：数据集仅来自单一医疗机构的CT扫描，扫描协议和设备的一致性可能高估实际表现。不同种族、体型、扫描参数下的泛化能力尚未验证。
4. **消费级设备验证缺失**：所有实验均基于从CT衍生的表面网格，而目标是利用消费级深度传感器（如iPhone LiDAR）获取网格。真实环境下噪声、遮挡、分辨率下降可能显著退化模型性能，目前缺乏这一闭环验证。

### 重要图表结论

- **Figure 1**：展示了数据集中腹部表面网格的视觉多样性，说明输入包含个体体型、轮廓及局部起伏信息，为预测内部标志物提供了物理基础。
- **Figure 2**：勾画了从CT到表面网格再到预测的完整流水线，是理解该方法间接观测性质的关键。
- **Table 1 & 2**：汇总了所有单目标测试结果，表明外部几何能可靠预测内部标志物，且CNN与视觉Transformer均可作为有效的主干网络。
- **Table 3**：提供了性别分层的证据，指出年龄预测中女性MAE偏大的偏差，提示未来需探究体成分性别差异的影响。
- **Figure 7**（附录）：Grad-CAM热力图显示ResNet-18对HCC-18的预测主要关注腹部轮廓和腰臀部区域，初步解释模型利用了体脂分布相关的几何特征，但需要更多病例验证其临床合理性。

![[assets/figures/papers/iclr26_0005_dKRAo0a9Gm_AbdCTBench_Learning_Clinical_Biomarker_Represent/figures/054_Figure_7.jpg]]
*Figure 7: Grad-CAM visualizations showing learned representations from abdominal surface geometry. The heatmaps highlight regions of interest that the ResNet-18 model focuses on for HCC-18 (Diabetes with Chronic Complications) prediction*

## 方法谱系与知识库定位

AbdCTBench的核心贡献并非提出一种全新的网络架构，而是构建了一个**从外部体表几何到内部体成分生物标志物的预测框架**，并将其形式化为可复现的基准任务。该工作在方法谱系中定位为非侵入式代谢风险评估的**代理变量学习管道**，其边界条件、与现有工作的关系以及未解决问题如下。

### 与Baseline及Follow-up的关系

该基准所采用的架构覆盖了CNN与视觉Transformer两个世代的核心设计。表1和表2的系统性对比揭示了一个关键现象：**在单一任务上，轻量级CNN（ResNet-18、ResNet-34）与更复杂的ViT变体（Swin Transformer-Base）之间并不存在绝对优势**。例如，死亡率预测的AUROC最佳值为ResNet-18的0.839（95% CI 0.816–0.861），糖尿病伴慢性并发症（HCC-18）的AUROC最佳值则为Swin Transformer-Base的0.801。这一结果暗示，对于表面几何到内部生物标志物的映射，残差连接的局部特征聚合能力与Transformer的全局注意力机制在**现有数据规模下处于相近的帕累托前沿**。

RadImageNet预训练的ResNet-50作为医学影像领域的迁移学习baseline，在死亡率预测（AUROC 0.810）上反而不及从头训练的ResNet-18（0.839）。这表明医学影像预训练所捕获的纹理和灰度特征，与表面网格渲染图的深度图几何表征之间存在**显著的模态缺口**，直接迁移未必带来增益。相比之下，DINOv2自监督预训练的ViT-Small在多项HCC编码分类上表现稳健，提示自监督学习可能更适合表面几何的特征解耦。

各架构相对于Naive Baseline（AUROC ≈ 0.5，Age MAE 13.16）的大幅提升（年龄MAE降至6.22，钙化评分AUROC升至0.848）证明了外部腹部几何与内部组织成分之间的**可学习预测关联**是真实存在的，而非统计偶然。

### 适用边界

本工作的适用边界由三个关键约束划定。

**输入模态的代理性约束。** 表面网格从CT DICOM序列衍生而来，其信息量受限于原始扫描的精度和患者体位。表面深度图投影本质上是内部解剖结构的一个**间接观测变量**，它所提供的信息是内部组织体积和分布在体表的投影效应，而非内部结构的完整表征。因此，该方法对骨骼密度、内脏脂肪分布等与体表形态有直接因果关联的生物标志物预测能力较强，而对于仅与内部微循环或细胞代谢相关的指标，预测上限受限于投影过程的信息损失。

**数据来源的分布约束。** 数据集来自单一医疗机构的CT扫描，性别分层分析（表3）显示年龄预测中存在女性MAE略高于男性的差异（EfficientNet-B0整体6.22，性别间差约0.87年）。该偏差的归因尚未明确，可能源于体型分布的性别差异，也可能与CT扫描参数相关。跨机构、跨种族、跨CT协议的泛化性目前无法保证。

**类别不平衡的决策边界约束。** 部分HCC编码的患病率极低（如HCC-12），尽管采用了逆频率加权、均衡批次采样和F1最优阈值选择，异常检测任务仍面临高召回与低精度的经典权衡。模型输出的原始logits在极端不平衡场景下需要额外的校准手段才能转化为临床可用的决策阈值。

### 局限与开放问题

**单中心数据偏差与跨机构泛化。** 训练数据仅覆盖一家医院的患者群体，设备型号、成像协议、人群特征均为固定变量。模型对外部机构的CT扫描、或在消费级深度传感器（如iPhone LiDAR）生成的真实表面网格上的性能，目前**完全没有实证支撑**。这一从"CT衍生网格"到"消费级传感器网格"的跨越，构成了该方法从学术基准走向实际部署的核心瓶颈。

**多任务学习负迁移的本质原因未明。** 多任务联合训练（表17、18）将年龄MAE从6.22急剧恶化至14.53，多个AUROC低于0.63，表明多个生物标志物共享单一backbone时存在显著的负迁移。这是否源于不同任务所需表面几何特征的**空间分布冲突**（例如，内脏脂肪厚度预测关注下腹部，骨密度预测关注整体轮廓），还是损失函数梯度幅值的不匹配（GradNorm未能充分缓解），需要进一步分析。

**极端BMI亚群的预测可靠性待验证。** 腹部表面几何与内部成分的映射关系在肥胖和极度消瘦等极端体型人群中可能发生系统性偏移。当前数据集未对此类亚群做专门的分层报告，模型在这些人群中的适用性仍属未知。

**文本层次之外的开源问题。** 论文展示了从DICOM到表面网格的全管道，但消费级设备上如何实现同精度的表面重建、如何校准深度传感器噪声，均未涉及。这一工程化缺口决定了该方法从概念验证到大规模人群筛查的实际距离。

**开放研究方向**包括：① 在真实消费级深度传感器上完成端到端验证，建立设备间校准协议；② 探索更大规模的医学影像基础模型或2D-3D混合表征能否突破表面几何的信息上限；③ 设计针对多任务学习的解耦策略（如任务特定的注意力路径或渐进式微调）；④ 将校准方法（温度缩放、焦点损失调参）与类别不平衡处理相结合，优化罕见疾病检测的精度-召回平衡。

整体而言，AbdCTBench确立了"外部体表几何→内部生物标志物"这一预测范式的可行性下限，但将其推向临床筛查或消费级应用，仍需要在跨设备泛化、多目标协同和极端亚群鲁棒性上完成实质性突破。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/AbdCTBench_Learning_Clinical_Biomarker_Representations_from_Abdominal_Surface_Geometry.pdf

![[paperPDFs/ICLR_2026/AbdCTBench_Learning_Clinical_Biomarker_Representations_from_Abdominal_Surface_Geometry.pdf]]
