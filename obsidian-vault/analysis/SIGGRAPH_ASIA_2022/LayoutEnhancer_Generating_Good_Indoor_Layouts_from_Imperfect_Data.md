---
title: "LayoutEnhancer: Generating Good Indoor Layouts from Imperfect Data"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/LayoutEnhancer_Generating_Good_Indoor_Layouts_from_Imperfect_Data.pdf
project_link: null
code_link: "https://github.com/kleimerTU/HumanCentricLayouts"
aliases:
- LayoutEnhancer
tags:
- SIGGRAPH_ASIA_2022
- topic/benchmarks_datasets_evaluation
core_operator: 在基于Transformer的布局生成器训练中，引入根据人体工学专家知识设计的可微损失函数（包括可达性、可见性、照明、眩光、可访问性），将其与交叉熵损失结合，从而将人体工学约束直接编码到模型优化目标中。
primary_logic: 将人体工学规则形式化为一组连续可微的标量成本函数，并通过评估房间内的活动（如看电视、阅读、工作）来累积这些成本，使得生成模型能够在数据缺陷的情况下，通过损失函数偏向生成符合人体工学的布局。
claims:
- 包含人体工学损失项的训练显著降低了生成布局的人体工学损失。
- 在用户研究中，完整模型生成的布局比真实布局更受青睐，且明显优于基线方法ATISS。
- Bedrooms validation set (3DFRONT) 上 Mean ergonomic loss = LayoutEnhancer (full model)
- User study on perceived realism 上 Realism score (compared to ground truth) = LayoutEnhancer (full model)
---

# LayoutEnhancer: Generating Good Indoor Layouts from Imperfect Data

> [!tip] 核心洞察
> 将人体工学规则形式化为一组连续可微的标量成本函数，并通过评估房间内的活动（如看电视、阅读、工作）来累积这些成本，使得生成模型能够在数据缺陷的情况下，通过损失函数偏向生成符合人体工学的布局。

| 字段 | 内容 |
|------|------|
| 中文题名 | LayoutEnhancer: 从缺陷数据生成优质室内布局 |
| 英文题名 | LayoutEnhancer: Generating Good Indoor Layouts from Imperfect Data |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2202.00185) · [Code](https://github.com/kleimerTU/HumanCentricLayouts) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | LayoutEnhancer |
| Dataset | Bedrooms validation set, User study on perceived realism |

> [!tip] 效果简介
> - Bedrooms validation set (3DFRONT) 上，Mean ergonomic loss LayoutEnhancer (full model) vs Ground truth data (30.8% reduction)。
> - User study on perceived realism 上，Realism score (compared to ground truth) LayoutEnhancer (full model) vs Ground truth (score 0), ATISS (negative) (Preferred over ground truth and significantly more realistic than ATISS)。

## 概要

现有公开室内布局数据集存在大量人体工学缺陷（如眩光、照明不足、物体交叉、遮挡门口），导致纯数据驱动的生成模型难以学习到合理布局。本文提出 **LayoutEnhancer**，将人体工学专家知识形式化为一组连续可微的标量成本函数（可达性、可见性、照明、眩光、可访问性），并在房间活动（如看电视、阅读、工作）上下文中评估累积成本。该方法将这些可微损失与交叉熵损失结合，直接编码到基于 GPT-2 Transformer 的自回归布局生成器训练中，同时通过样本加权使模型更关注低质量布局。在 3DFRONT 卧室数据集上，完整模型生成的布局相比真实数据人体工学损失降低 30.8%，用户研究中亦比真实布局更受青睐，且显著优于基线方法 ATISS。该方法定位为数据驱动生成与专家知识约束的融合范式，适用于从缺陷数据中学习符合人体工学的室内场景布局。

## 核心方法与创新机理

### 问题背景与核心瓶颈

现有公开室内布局数据集（如3DFRONT）包含大量非专家设计的样本，存在两类典型缺陷：人体工学缺陷（如窗户位于电视正后方导致眩光、阅读位置缺乏照明）和几何缺陷（家具交叉、衣柜遮挡门口）。纯数据驱动的生成模型（如ATISS）直接拟合此类数据，无法习得符合人体工学的布局。LayoutEnhancer的核心瓶颈即在于：**如何在数据质量缺陷的条件下，使生成模型偏向输出符合人体工学规则的布局**。

### 核心创新机制

LayoutEnhancer的创新机理是将**人体工学专家知识形式化为一组连续可微的标量成本函数**，并通过**评估房间内的活动**来累积这些成本，最终将其作为**可微损失项**集成到Transformer序列生成器的训练目标中。这一机制包含三个相互耦合的环节：

1. **人体工学规则→可微成本函数**：将可达性、可见性、照明、眩光、可访问性五类规则转化为连续可微函数。
2. **活动上下文评估**：在"观看电视""阅读""工作"等活动场景下，采样虚拟人物位置和朝向，计算各规则成本的加权组合。
3. **损失驱动生成**：将人体工学损失与交叉熵损失加权求和，在训练时通过Gaussian核将损失梯度传播至离散token概率分布。

### 方法框架与模块顺序

整个pipeline由四个核心模块构成，按训练和推理两条路径组织：

**训练路径**：
1. **序列化映射**：将房间布局（家具类别、位置、尺寸、朝向等）映射为离散token序列。
2. **GPT-2 Transformer生成器**：以自回归方式预测下一token的类别分布。
3. **人体工学成本函数**：在活动上下文中评估当前布局的人体工学损失。
4. **混合损失反向传播**：将交叉熵损失与人体工学损失的加权和反向传播，更新Transformer参数。

**推理路径**：
1. **条件编码**：将房间边界、门窗等条件编码为token（矩形房间直接编码，非矩形房间通过AlexNet编码平面图特征）。
2. **自回归生成**：GPT-2逐token采样生成家具序列。
3. **场景重建**：将2D边界框恢复为3D场景，匹配3D模型并调整垂直位置。

### 关键Changed Slots

#### Slot 1：训练损失函数（核心变更）

**基线（ATISS）**：仅使用交叉熵损失 $\mathcal{L}_T$ 训练序列生成器。

**LayoutEnhancer**：总损失函数定义为交叉熵损失与人体工学损失的加权和：
$$\mathcal{L}(S^k) = \beta_T \mathcal{L}_T(S^k) + \beta_E \mathcal{L}_E(S^k)$$

其中 $\beta_T, \beta_E$ 为权重系数。这一变更将人体工学约束直接编码到优化目标中，使模型在数据缺陷条件下仍能偏向生成符合规则的布局。

**可微性实现**：由于布局token是离散的，直接计算人体工学损失对token概率的梯度不可行。LayoutEnhancer采用Gaussian核平滑策略：对于每个预测token，选取概率最大的离散值作为中心，在其邻域内用Gaussian核卷积，计算期望值：
$$\bar{v} = \sum_j N(v_j | \hat{v}, \sigma) \cdot P(s_i = v_j | s_{<i}, \theta)$$

然后基于期望值 $\bar{v}$ 计算人体工学损失，使梯度可传播回token概率分布。

#### Slot 2：样本权重策略

**基线**：所有训练样本权重相同。

**LayoutEnhancer**：根据每个训练样本的人体工学损失 $E(S^k)$ 进行加权，使模型更关注质量较差的布局。权重定义为 $w^k = 1 - E(S^k)$，人体工学损失越高的样本获得越低权重，迫使模型优先学习纠正缺陷。消融实验（Fig. 7）表明，单独的权重策略（Weight-only）可降低人体工学损失，但与损失项结合效果最佳。

#### Slot 3：数据增强

**基线**：使用原始数据集。

**LayoutEnhancer**：以50%概率向布局中添加缺失的关键家具对象（如室内灯、电脑、电视）。这是因为人体工学成本函数依赖这些对象的存在（如照明成本需要灯、观看电视成本需要电视），而原始数据中常缺失这些元素。该增强策略确保人体工学损失可计算，但依赖于启发式规则，可能引入偏差。

### 人体工学成本函数体系

五类成本函数构成人体工学评估的基础，均在活动上下文中计算：

**可达性成本（Reach）**：衡量从位置 $p$ 到目标 $q$ 的交互容易程度，采用sigmoid函数平滑建模：
$$E_R = \frac{1.0}{1.0 + \exp(-\beta_R(|q - p| - d_R))}$$
其中 $d_R$ 为最大舒适交互距离，$\beta_R$ 控制过渡陡峭度。

**可见性成本（Visibility）**：衡量从视点 $p_j$、方向 $u_j$ 观察目标 $q_k$ 的可见度：
$$E_V = 1 - \left( \frac{1 + \langle u_j, v \rangle}{2} \right)$$
其中 $v$ 为视点到目标的方向向量。

**照明成本（Lighting）**：评估目标位置的光照充足程度，基于光源位置和强度计算。

**眩光成本（Glare）**：考虑视野内强光源带来的视觉性能下降，采用softmax加权：
$$E_G = \langle e^g, \text{softmax}(\beta \cdot e^g) \rangle$$

**可访问性成本（Accessibility）**：衡量目标前方自由空间的大小：
$$E_A = \sum_{k=0}^{N} \frac{|I_j \cap A_k|}{|I_j|}$$

### 活动上下文评估机制

人体工学成本不是孤立计算的，而是在具体活动上下文中评估。以"观看电视"活动为例：

1. 对所有可能的座位位置采样虚拟人物（avatar），确定视点 $p_j$ 和朝向 $u_j$。
2. 对每个座位-电视组合，计算配对损失：
   $$e_{j,k}^{tv} = \frac{E_V(p_j, u_j, q_k) + E_G(p_j, B, q_k)}{2}$$
   其中 $B$ 为窗户等强光源位置。
3. 总观看电视损失采用软最小加权和，使系统关注最佳观看位置：
   $$E_{tv} = \langle e^{tv}, \text{softmin}(\beta \cdot e^{tv}) \rangle$$

类似地，"阅读"活动结合照明和可达性，"工作"活动结合可见性、照明和可达性：
$$e_{j,k}^{work} = \frac{\bar{E}_V(p_j, u_j, q_k) + \bar{E}_L(p_j, B, q_k) + \bar{E}_R(p_j, q_k)}{3}$$

总人体工学损失为所有可能活动成本的加权平均：
$$E = \frac{\sum_a \delta_a E_a}{\sum_a \delta_a}$$
其中 $\delta_a$ 指示活动 $a$ 是否可执行（依赖必要对象是否存在）。

### 成本重缩放

为增强高成本区域的梯度信号，LayoutEnhancer对原始成本进行对数重缩放（以可达性为例）：
$$\bar{E}_R = -\ln(1.0 + \epsilon - E_R)$$
该变换拉伸了高成本区域，使优化过程对严重违反人体工学规则的情况更敏感。

### 生成模型架构

序列生成器采用GPT-2 Transformer，输入为布局token序列 $S = (s_1, \ldots, s_n)$。每个家具对象表示为6元组：
$$F_i := (c_i, o_i, x_i, y_i, w_i, d_i)$$
分别对应类别、朝向、位置坐标、宽度、深度。序列概率分解为条件概率乘积：
$$\mathcal{P}(S | \theta) = \prod_i p(s_i | s_{<i}, \theta)$$

模型预测下一token分布：
$$\dot{p}(s_i | s_{<i}, \theta) = f_\theta(s_{<i}, \bar{s}_{<i}^P, s_{<i}^I)$$
其中 $\bar{s}_{<i}^P$ 为位置编码序列，$s_{<i}^I$ 为索引序列。

对于非矩形房间，使用AlexNet将二值平面图编码为特征嵌入，替代基于token的房间表示，增强对复杂房间形状的适应能力。

### 训练策略

训练时采用teacher forcing，但人体工学损失的计算需要完整布局。为解决这一矛盾，LayoutEnhancer在计算人体工学损失时，将当前生成token $s_i$ 与ground truth的 $s_{<i}$ 和 $s_{>i}$ 拼接，形成完整布局进行评估。这种"单token替换"策略使人体工学损失能够针对每个生成步骤提供反馈，同时保持训练稳定性。

迁移学习策略进一步提升了小样本房间类型的生成质量：先在包含所有房间类型的通用数据集上预训练，再针对特定房间类型（如客厅、餐厅）微调，显著降低验证损失（Fig. A.12）。

### 推理阶段

推理时，模型以自回归方式逐token采样，从预测的类别分布中随机采样实际token值。生成完成后，通过场景重建模块将2D边界框恢复为3D场景：选择匹配的3D模型，根据家具类别调整垂直位置，最终输出可渲染的3D室内布局。

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2202_00185/figures/003_Figure_3.jpg]]
*Figure 3: Ergonomic rules implemented in our system. We chose these guide-v u u lines as they are essential in most indoor scenarios, like reading a book, watching TV, or working at the desk or the computer. We convert the rules to scalar cost functions and evaluate them using activities (cf. Section 3)*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2202_00185/figures/012_Figure.jpg]]
*Figure: Fig. A.11. Overview of our model. A room layout consisting of individual furniture objects is mapped to a sequence of tokens which serves as the input to the transformer model. Given this sequence, the network predicts a categorical distribution for the next token from which we randomly sample the actual token value. During training, the order of objects other than the room, doors and windows is shuffled in the sequence. Furthermore, the attributes of the room can be either mapped to tokens directly (for rectangular rooms only), or by using an additional encoder network given a binary image of the floor plan as input*

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2202_00185/figures/007_Figure_7.jpg]]
*Figure 7: Cross-entropy loss and ergonomic loss for our model and its ablations, evaluated on the Bedrooms dataset. The training loss and validation loss refer to the cross-entropy loss on the training and validation sets, respectively. By including our proposed ergonomic loss term during training we can significantly decrease the ergonomic loss of synthesized layouts*

## 实验与关键发现

### 核心实验设置

LayoutEnhancer 的训练基于 3DFRONT 数据集的卧室（Bedrooms）子集，该数据集包含非专家设计的布局，存在大量人体工学缺陷（如眩光、照明不足、物体交叉、遮挡门口）。模型以 GPT-2 Transformer 为基础，将布局表示为离散标记序列，训练时结合交叉熵损失 $`\mathcal{L}_T`$ 与人体工学损失 $`\mathcal{L}_E`$，总损失为 $`\mathcal{L}(S^k) = \beta_T \mathcal{L}_T(S^k) + \beta_E \mathcal{L}_E(S^k)`$。人体工学损失由五项可微成本函数（可达性、可见性、照明、眩光、可访问性）在活动上下文中累积计算得出，涵盖看电视、阅读、工作等典型室内活动（Table 1 给出了规则与活动的关联映射）。

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2202_00185/figures/011_Table_1.jpg]]
*Table 1: Associations of rules to activities that can be performed in an environment. Not all activities require all rules to be fulfilled*

### 主结果：人体工学损失与用户感知

**人体工学损失降低**。在卧室验证集上，对每个平面图生成 20 个布局变体，LayoutEnhancer 完整模型（同时使用样本权重和人体工学损失项）生成的布局，其平均人体工学损失相比真实数据（Ground Truth）降低了 **30.8%**（Fig. 8 左图）。这一结果表明，尽管训练数据本身存在缺陷，模型通过损失函数中嵌入的专家知识，成功偏向生成更符合人体工学的布局。

**用户感知真实性**。采用双盲对比的用户研究显示，完整模型生成的布局在感知真实性上**优于真实数据**（得分 >0），而纯数据驱动的基线方法 ATISS（Paschalidou et al., 2021）得分显著为负，表明其生成的布局不如真实数据真实（Fig. 8 右图）。用户研究排除了应答不一致或平均比较时间少于 10 秒的参与者以保证数据质量。

### 消融实验：权重与损失项的贡献

为解耦样本加权与人体工学损失项各自的作用，论文定义了三组消融变体：

- **Baseline**：$`\beta_T = 1, \beta_E = 0`$，仅使用标准交叉熵损失训练，不使用任何人体工学信息。
- **Weight-only**：$`\beta_T = 1 - E(S^k), \beta_E = 0`$，以人体工学损失 $`E(S^k)`$ 作为样本权重，使模型更关注质量较差的布局，但不将损失项直接加入优化目标。
- **Loss-only**：$`\beta_T = 1, \beta_E = 1`$，将人体工学损失作为附加损失项，但不进行样本加权。

Fig. 7 展示了各变体在训练和验证集上的交叉熵损失与人体工学损失曲线。核心发现如下：

1. **完整模型在降低人体工学损失方面最优**。同时使用权重与损失项的完整模型，其生成布局的人体工学损失显著低于仅使用权重或仅使用损失项的变体。
2. **Loss-only 优于 Weight-only**。将人体工学损失直接编码到优化目标中，比仅通过样本权重间接引导模型更有效。
3. **所有变体均优于 ATISS**。在用户研究（Fig. 8）中，所有 LayoutEnhancer 变体的感知真实性得分均高于 ATISS，表明即使是不完整的人体工学知识注入也能带来显著提升。
4. **交叉熵损失的权衡**。引入人体工学损失项后，训练交叉熵损失略有上升，但验证交叉熵损失保持稳定，说明模型并未因过度拟合人体工学规则而丧失生成多样性。

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2202_00185/figures/008_Figure_8.jpg]]
*Figure 8: Room-conditioned layout synthesis. We synthesize 20 layout variations for each floor plan in the Bedrooms validation set and evaluate the ergonomic loss. The left chart shows the mean ergonomic loss of the synthesized layouts, with the 80% confidence interval of the mean shown in black. The realism of the synthesized layouts is evaluated in a user study. The right chart shows how the layouts synthesized using each method are perceived compared to the ground truth, with a negative value meaning that the ground truth is seen as more realistic. Our proposed approach improves the ergonomic loss of the scenes, while also being perceived as more realistic than the ground truth*

### 迁移学习与小样本泛化

针对卧室以外的房间类型（如客厅、餐厅），训练数据量显著减少。论文采用迁移学习策略：先在包含所有房间类型的通用数据集上预训练，再在特定房间类型上微调。Fig. A.12 显示，该策略**显著降低了小样本房间类型的验证交叉熵损失**，验证了人体工学损失的引入并未损害模型的泛化能力，反而通过迁移学习实现了有效的知识复用。

### 失败模式与适用边界

**推理效率瓶颈**。人体工学损失的引入使训练时间从每 epoch 13 秒增至 123 秒（约 9.5 倍）。推理阶段，物体交叉检测是主要瓶颈，每个布局平均耗时 1.653 秒，限制了实时交互式应用场景。

**规则覆盖的局限性**。当前人体工学规则为手工设计，仅覆盖可达性、可见性、照明、眩光、可访问性五个维度，且要求规则可微。这意味着：
- 某些优质布局的隐性标准（如风格协调、动线流畅性）无法被当前规则捕捉。
- 规则的可微性要求限制了知识表示形式，难以直接纳入离散或基于逻辑的约束。

**数据增强的启发式偏差**。为使人体验工学损失可计算，训练时以 50% 概率向布局中添加缺失的家具对象（如室内灯、电脑、电视）。这一启发式策略可能引入偏差：添加的家具位置和类型基于简单规则，不一定符合真实分布，可能在某些边缘情况下导致不合理的布局生成。

**评估范围有限**。当前实验主要基于卧室数据集，且仅评估了静态布局的人体工学指标和用户感知真实性。扩展到包含多人交互、动态活动的全 3D 场景，以及更复杂的房间类型（如开放式厨房-客厅组合），仍需进一步验证。

### 关键数值汇总

| 指标 | 对比对象 | 结果 |
|------|----------|------|
| 平均人体工学损失 | LayoutEnhancer vs. Ground Truth | 降低 30.8% |
| 用户感知真实性 | LayoutEnhancer vs. Ground Truth | 优于真实数据（得分 >0） |
| 用户感知真实性 | LayoutEnhancer vs. ATISS | 显著优于 ATISS（得分负值） |
| 训练时间 | 含人体工学损失 vs. 仅交叉熵 | 13s → 123s / epoch |
| 推理时间（物体交叉检测） | 每布局 | 1.653s |
| 小样本验证损失 | 迁移学习 vs. 直接训练 | 显著降低（Fig. A.12） |

![[assets/figures/papers/paper_list_l61_https_arxiv_org_abs_2202_00185/figures/014_Figure.jpg]]
*Figure: Fig. A.13. The interface of the user study. Participants were asked which of the 2 displayed scenes is more realistic*

## 定位与知识库关联

LayoutEnhancer 的核心定位是**在数据驱动布局生成中引入可微的人体工学先验**，以弥补训练数据本身的质量缺陷。与纯数据驱动的基线方法 **ATISS**（Paschalidou et al., 2021）相比，LayoutEnhancer 改变的 slot 并非生成器架构本身（两者均采用基于 Transformer 的自回归序列生成范式），而是**训练损失函数的构成**和**样本利用策略**：

- **损失函数 slot**：ATISS 仅使用交叉熵损失 $\mathcal{L}_T$ 训练序列生成器；LayoutEnhancer 将总损失扩展为 $\mathcal{L}(S^k) = \beta_T \mathcal{L}_T(S^k) + \beta_E \mathcal{L}_E(S^k)$，其中 $\mathcal{L}_E$ 是一组连续可微的人体工学成本函数（可达性、可见性、照明、眩光、可访问性）在活动上下文中的加权聚合。这一改变使得梯度信号不仅来自序列似然，还来自布局的物理合理性反馈。
- **样本权重 slot**：ATISS 对所有训练样本等权处理；LayoutEnhancer 可根据样本的人体工学损失进行加权，使模型在训练中更关注质量较差的布局，强化纠偏能力。
- **数据增强 slot**：ATISS 使用原始数据集；LayoutEnhancer 以 50% 概率向布局中补充缺失的功能性家具（如灯、电视、电脑），以确保人体工学损失可计算，避免因数据不完整导致损失项失效。

从知识库挂载的角度看，LayoutEnhancer 提供了一个清晰的**“可微专家知识注入”模板**：将领域知识形式化为连续可微的标量成本函数，通过活动上下文（如看电视、阅读、工作）将多个规则聚合为单一损失项，再以加权方式嵌入到生成模型的训练目标中。这一模板可挂载到知识库的以下节点：

1. **“神经符号推理与约束满足”节点**：LayoutEnhancer 的做法本质上是一种软约束注入——不要求生成结果严格满足规则，而是通过损失函数偏置模型分布。这与硬约束满足方法（如基于优化的后处理）形成互补，适合规则不可精确满足或存在冲突的场景。
2. **“数据增强与弱监督学习”节点**：通过启发式数据增强补全缺失家具，使得原本不可计算的人体工学损失可被评估，这是一种面向弱标注数据的实用策略，可推广到其他需要特定评估条件但数据不完整的任务。
3. **“生成模型的可控性”节点**：LayoutEnhancer 展示了在不改变模型架构的情况下，仅通过损失函数设计即可显著改变生成分布的特性，为可控生成提供了轻量级范式。

**适用边界**：

- **规则依赖**：方法要求人体工学规则必须可微，这限制了知识的表示形式。离散规则或需要复杂模拟评估的约束（如碰撞检测的精确物理仿真）难以直接纳入当前框架。论文中物体交叉检测在推理时仍需后处理（每布局 1.653 秒），说明可微损失并未完全解决几何约束问题。
- **训练开销**：添加人体工学损失使每 epoch 训练时间从 13 秒增至 123 秒（约 9.5 倍），这限制了在更大规模数据集或更复杂规则集上的扩展性。
- **评估范围**：主要实验基于 3DFRONT 的卧室数据集，人体工学规则集为手工设计的五类规则。扩展到起居室、厨房等更多房间类型，以及包含动态人物交互的全 3D 场景，需要定义新的活动上下文和对应规则，其有效性和泛化性仍需验证。
- **数据增强偏差**：随机添加灯、电视等家具的启发式策略可能引入分布偏差——如果增强策略本身不符合真实布局统计，模型可能学到错误的先验。论文未对此偏差进行消融分析。

**后续启发**：

- **自动规则学习**：当前人体工学规则完全手工设计，后续工作可探索从专家标注的布局对比数据中自动学习可微成本函数，或通过交互式反馈（如用户偏好点击）在线更新规则参数，减少手工设计负担。
- **多阶段与混合约束**：将可微软约束与不可微硬约束（如碰撞检测）分层处理——训练时用软约束引导分布，推理时用硬约束后处理修正——可能兼顾生成质量与物理可行性，同时降低训练开销。
- **跨领域迁移**：该范式可迁移到其他“数据有缺陷但存在可微领域知识”的布局生成任务，如城市道路规划（交通流规则）、电路布局（电磁约束）、UI 设计（可用性准则）等。关键在于能否将领域知识表达为连续可微的标量函数。
- **效率优化**：训练和推理的瓶颈提示需要更高效的架构设计（如非自回归生成、损失近似计算）来降低实际部署门槛，这是该方法进入交互式设计工具的重要前提。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/LayoutEnhancer_Generating_Good_Indoor_Layouts_from_Imperfect_Data.pdf]]