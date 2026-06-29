---
title: Neural Slicer for Multi-axis 3D Printing
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Neural_Slicer_for_Multi_axis_3D_Printing.pdf
project_link: null
code_link: null
aliases:
- NS
- NSMA3P
tags:
- SIGGRAPH_2024
- topic/graphics_fabrication_design
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用神经网络将映射参数化为连续的四元数场 q(x) 和缩放场 s(x)，并通过中间笼网格的可微变形直接在模型空间中基于局部打印方向（LPD）梯度定义损失函数，从而实现对支撑自由和强度增强目标的直接且鲁棒的优化。
primary_logic: 将曲线切片任务转化为在中间笼网格上通过神经网络优化标量场 G(x) 及其梯度 ∇G(x) 的可微问题，使制造目标能够通过直接损失函数定义，从而摆脱对高品质网格和良好初始姿态的依赖，同时保持表示无关性。
claims:
- 在Bridge模型上，Neural Slicer 相比 S3-Slicer 将最大应变降低40.5%，物理断裂力提高101.9%
- 在Shelf模型上，Neural Slicer 相比平面层切片将最大应变降低43.3%
- 在Tubes模型上，Neural Slicer 将剩余悬垂区域减少95%
- 在Bunny Head模型上，引入强度增强（SF+SR）使断裂力相比仅支撑自由（SF）提升30.6%
---

# Neural Slicer for Multi-axis 3D Printing

> [!tip] 核心洞察
> 将曲线切片任务转化为在中间笼网格上通过神经网络优化标量场 G(x) 及其梯度 ∇G(x) 的可微问题，使制造目标能够通过直接损失函数定义，从而摆脱对高品质网格和良好初始姿态的依赖，同时保持表示无关性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向多轴3D打印的神经切片器 |
| 英文题名 | Neural Slicer for Multi-axis 3D Printing |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://ryantaoliu.github.io/NeuralSlicer/) |
| Topic | #topic/graphics_fabrication_design #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Neural Slicer |
| Dataset | Shelf, Bridge, Bunny Head（实物测试）, Tubes |

> [!tip] 效果简介
> - Shelf 上，最大应变降低（与平面层对比） Neural Slicer (SF+SR) vs Planar layers (-43.3%)。
> - Bridge 上，最大应变降低（与 S3-Slicer 对比） Neural Slicer (SR) vs S3-Slicer (SR) (-40.5%)。
> - Bridge（实物测试） 上，断裂力 Neural Slicer (SR) vs S3-Slicer (SR) (+101.9%)。

## 概要

多轴3D打印中的曲线切片技术旨在通过优化逐层堆积方向，同时满足支撑自由和强度增强等制造目标。现有最优方法**S³-Slicer**（Zhang et al., 2022）依赖高质量四面体网格，并在变形空间中通过间接优化旋转来满足制造约束，导致模型空间中产生失真，且优化结果对初始姿态敏感。本文提出**Neural Slicer**，一种基于神经网络的表示无关型曲线切片器。其核心思路是将映射参数化为两个SIREN网络预测的连续四元数场$\mathbf{q}(\mathbf{x})$和缩放场$\mathbf{s}(\mathbf{x})$，通过中间笼网格的可微ARAP变形定义标量场$G(\mathbf{x})$，并以$G(\mathbf{x})$的梯度作为局部打印方向，在模型空间中直接定义支撑自由、强度增强等损失函数进行端到端优化。实验表明，Neural Slicer在支撑自由任务上将悬垂区域缩减高达95%，在强度增强任务上相比S³-Slicer最大应变降低40.5%、物理断裂力提升101.9%，且优化过程对初始猜测鲁棒、不依赖高品质四面体网格。

## 核心方法与创新机理

### 问题瓶颈：间接优化的失真陷阱

现有最先进的曲线切片方法 **S³-Slicer**（Zhang et al., 2022）的核心思路，是对包围模型的四面体网格施加非线性变形，将制造目标（如支撑自由、强度增强）转化为变形空间中的角度约束进行间接优化。然而，这一范式存在两个根本性瓶颈：

1. **失真映射问题**：在变形空间中满足的角度约束，经逆映射回到模型空间后会发生严重失真。如图2所示，变形空间中满足自支撑角条件的层，映射回模型空间后可能产生更大的悬垂区域——优化器在“错误的空间”中完成了“正确”的优化。
2. **初始姿态敏感性**：非线性优化的结果强烈依赖于四面体网格的初始姿态选择，且高质量四面体网格的生成在复杂拓扑下本身就是一个困难问题。

这些瓶颈的因果根源在于：**制造目标本质上是模型空间中局部打印方向（LPD）的几何约束，但 S³-Slicer 却通过变形空间的旋转变量来间接表达这些约束**，造成了优化目标与约束定义空间之间的错位。

### 核心洞察：连续场参数化与直接损失定义

Neural Slicer 的核心洞察是将曲线切片任务重新表述为一个在中间笼网格上的可微优化问题。具体而言：

- 将变形映射参数化为两个全域连续函数：**四元数场 `q(x)`** 和 **缩放场 `s(x)`**，两者均由 SIREN 神经网络表示；
- 利用这些连续场驱动中间笼网格的可微 ARAP 变形，得到离散映射 `λ`；
- 将映射结果的 z 分量定义为标量场 `G(x) := proj_z λ_θ(x)`，其梯度 `∇G(x)` 即为局部打印方向 `d_p`；
- 在**模型空间**中直接基于 `d_p` 定义制造目标的损失函数，实现端到端的可微优化。

这一设计彻底绕开了 S³-Slicer 的间接优化陷阱：优化器始终在模型空间中直接评估约束满足程度，不再依赖变形空间到模型空间的保真映射。

### 三个关键 Changed Slots

相对于 S³-Slicer 基线，Neural Slicer 在以下三个维度上做出了根本性改变：

**Slot 1: 映射参数化方式**  
基线在四面体网格上逐元素定义旋转与缩放，是离散的、局部的参数化；Neural Slicer 使用两个 SIREN 神经网络（10层，每层512神经元）分别预测全域连续的 `q(x)` 和 `s(x)`。连续场参数化带来了两个关键优势：(1) 自然保证变形在空间上的平滑性；(2) 神经网络作为隐式先验，对初始猜测具有极强的鲁棒性——实验表明，使用平面场、热方法场、甚至 S³-Slicer 的结果作为初始猜测，均能收敛到相近的最终损失（Fig.12）。

**Slot 2: 优化目标定义空间**  
基线在变形空间中通过旋转定义间接目标；Neural Slicer 在模型空间中基于 `d_p = ∇G(x)` 直接定义损失函数。这一改变是解决失真问题的关键：`d_p` 是标量场在模型空间中的梯度，其几何意义（打印方向）不依赖任何映射逆变换，因此优化目标与物理约束在同一个空间中保持一致。

**Slot 3: 几何表示依赖性**  
基线必须生成高质量四面体网格，在复杂拓扑（如 Tubes 模型的卷积曲面骨架表示）下困难且不可靠；Neural Slicer 仅依赖一个与输入表示无关的中间笼网格 `C`——该笼网格通过隐式表面膨胀生成，无论输入是三角网格、四面体网格还是隐式曲面，均可统一处理（Fig.4）。这使得方法天然具有表示无关性。

![[assets/figures/papers/paper_list_l25_https_ryantaoliu_github_io_NeuralSlicer/figures/009_Figure_4.jpg]]
*Figure 4: The illustration of cage generation: (a) the implicit surface*

### 流水线模块与因果链路

Neural Slicer 的完整流水线包含9个模块，其间的因果关系构成了从输入到曲线层的完整计算图：

**模块1: 隐式固体构建**  
为输入模型 `M` 构建隐式函数 `H(x)`，用于后续的采样点判别和等值面裁剪。`H(x)` 是表示无关性的基础——无论输入格式如何，均转化为统一的隐式表示。

**模块2: 应力场计算**  
通过体素有限元分析（FEA）获得主应力场 `τ_max`，作为强度增强损失的指导信号。当前实现采用各向同性 FEA，这是方法的一个已知局限（各向异性 FEA 尚未集成到可微优化回路中）。

**模块3: 笼网格生成**  
生成包围模型的四面体网格 `C` 作为中间计算域。笼网格的角色是提供一个离散域，使连续场 `q(x)` 和 `s(x)` 的预测值可以被“采样”并转化为离散变形。

**模块4: 采样点生成**  
在模型表面生成采样点 `B`（用于支撑自由损失 `L_SF` 和点悬垂损失 `L_PO`），在应力上区生成采样点 `T`（用于强度增强损失 `L_SR`）。采样点的选择直接影响损失函数的聚焦区域。

**模块5: 神经网络前向映射**  
两个 SIREN 网络分别预测 `q(x)` 和 `s(x)`。这是整个流水线的核心参数化模块——网络的权重 `θ_q` 和 `θ_s` 是优化变量，而 `q(x)` 和 `s(x)` 的连续性保证了变形场的全局平滑性。

**模块6: 可微 ARAP 变形**  
利用 `q(x)` 和 `s(x)` 驱动笼网格 `C` 的尺度控制 ARAP（As-Rigid-As-Possible）变形，生成变形后的笼网格 `C^d`，并得到离散映射 `λ`。ARAP 的目标函数为：

$$\arg\min_{C^d} \sum_{e\in C} \| (\mathbf{N} \mathbf{V}_e^d)^{\mathrm{T}} - \mathbf{R}_e \mathbf{S}_e (\mathbf{N} \mathbf{V}_e)^{\mathrm{T}} \|_F^2 + \gamma \sum_{\mathbf{v}\in C} \| \mathbf{v}^d - \mathbf{v} \|^2$$

其中 `R_e` 和 `S_e` 分别由 `q(x)` 和 `s(x)` 在元素中心的值确定，正则化项 `γ` 控制变形幅度。这一模块是整个流水线的可微性关键——它建立了从网络输出到离散映射的可微桥梁。

**模块7: 标量场与梯度提取**  
将 `λ` 的 z 分量定义为标量场 `G(x)`，其梯度 `∇G(x)` 即为局部打印方向 `d_p`。这是连接变形与制造目标的语义接口：`G(x)` 的等值面将成为曲线层，而 `∇G(x)` 的方向决定了每一层的打印方向。

**模块8: 损失函数评估**  
在模型空间直接计算各项损失并进行可微误差反向传播。总损失函数为：

$$L = w_1 \mathcal{L}_{SF} + w_2 \mathcal{L}_{SR} + w_3 \mathcal{L}_{OP} + \mathcal{L}_{HS} + \mathcal{L}_{HQ}$$

其中各损失项的因果角色如下：

- **强度增强损失 `L_SR`**：鼓励 `d_p` 垂直于最大主应力方向 `τ_max`，以提高层间结合强度。通过 sigmoid 函数 `σ` 将角度偏差转化为可微损失：

$$\mathcal{L}_{SR} := \sum_{\mathbf{p}\in\mathcal{T}} |V_e| \sigma\big(k_{SR} (|\mathbf{d}_p \cdot \boldsymbol{\tau}_{\max}|) \big)$$

- **支撑自由损失 `L_SF`**：要求 `d_p` 与表面法线的夹角满足自支撑角 `α`：

$$\mathcal{L}_{SF} := \sum_{\mathbf{p}\in\mathcal{B}} |A_{\mathbf{p}}| \sigma\big(k_{SF} (-\mathbf{n}(\mathbf{p}) \cdot \mathbf{d}_p - \sin\alpha) \big)$$

- **点悬垂损失 `L_PO`**：防止表面点成为沿打印方向的局部极小值，确保逐层累积可行：

$$\mathcal{L}_{PO} := \sum_{\mathbf{p}\in\mathcal{B}} |A_{\mathbf{p}}| \max\big(0, \min_{\mathbf{p}_j\in N_{\mathbf{p}}} ( (\mathbf{p}_j - \mathbf{p}) \cdot \mathbf{d}_p ) \big)$$

- **缩放正则化损失 `L_HS`** 与 **四元数正则化损失 `L_HQ`**：分别强制相邻四面体元素的缩放比和四元数方向平滑变化，保证变形场的几何质量。

**模块9: 等值面提取与裁剪**  
收敛后从 `C` 上提取 `G(x)` 的等值面，并用隐式固体 `H(x)` 裁剪以生成最终的曲面层（Fig.5）。

### 训练/推理路径

整个流水线的训练路径是一个闭环的可微优化过程：前向传播从模块1到模块8计算总损失 `L`，反向传播通过模块8→7→6→5更新网络参数 `θ_q` 和 `θ_s`。ARAP 变形（模块6）的可微性通过隐函数定理保证——每个优化步内求解一个线性系统得到 `C^d`，其梯度可通过求解伴随线性系统高效计算。

推理路径则是一次性的前向传播：给定收敛后的网络参数，在笼网格上采样 `q(x)` 和 `s(x)`，执行 ARAP 变形，提取等值面并裁剪。整个优化过程在 ≤15 分钟内完成（Table 1），且对初始猜测鲁棒（Fig.12）。

### 关键公式的变量含义总结

| 符号 | 含义 | 来源 |
|------|------|------|
| `q(x)` | 四元数场，定义局部旋转 | SIREN 网络预测 |
| `s(x)` | 缩放场，定义局部缩放比 | SIREN 网络预测 |
| `λ_θ(x)` | 变形映射，将点 x 映射到 y | ARAP 变形计算 |
| `G(x)` | 标量场，λ 的 z 分量 | Eq.(1) |
| `d_p = ∇G(x)` | 局部打印方向（LPD） | 标量场梯度 |
| `τ_max` | 最大主应力方向 | 体素 FEA |
| `α` | 自支撑角 | 材料/工艺参数 |
| `B` | 表面采样点集 | 模块4 |
| `T` | 应力上区采样点集 | 模块4 |
| `C` | 中间笼网格 | 模块3 |

### 方法边界条件与未解决问题

尽管 Neural Slicer 在多个维度上优于 S³-Slicer，其方法设计仍存在以下边界条件：

1. **笼网格依赖性**：映射计算依赖中间笼网格，不同分辨率会影响收敛速度和最终损失值（Fig.18），但缺乏自动选择笼网格分辨率的指南。
2. **各向异性应力场的缺失**：当前应力场来自各向同性 FEA，未考虑打印过程中因各向异性材料属性变化导致的应力重新分布。各向异性 FEA 虽已进行离线验证（Fig.17），但尚未集成到可微优化回路中。
3. **碰撞处理的简并风险**：全局碰撞处理简化为增加谐波项权重，极端情况下强制生成平面层，可能削弱其他制造目标的满足程度。
4. **参数化效率的理论缺口**：四元数-缩放场参数化相比标量场或向量场更高效（Fig.19），但这一优势仅通过数值实验验证，缺乏形式化的理论证明。

![[assets/figures/papers/paper_list_l25_https_ryantaoliu_github_io_NeuralSlicer/figures/002_Figure_2.jpg]]
*Figure 2: An illustration of the distortion caused by indirect optimization in ??3-Slicer: (a) the layers generated in the deformed space, and (b) curved layers in the model space obtained by the mapping. In the deformed space, the support-free requirement has been fulfilled – i.e., the angle between the printing direction and surface normal is less than 135◦. However, the angle expands when mapped back to the model space, resulting in a larger overhang area (see also the 3D printing result shown in Fig.7)*

![[assets/figures/papers/paper_list_l25_https_ryantaoliu_github_io_NeuralSlicer/figures/003_Figure_3.jpg]]
*Figure 3: An overview of our neural slicer to generate curved layers for multi-axis 3D printing. (a) The input Yoga model M with its implicit solid ?? (x) and the distribution of principal stresses obtained from voxel-based FEA. (b) A volumetric mesh C caging the input model M is constructed, serving as the intermediate representation in numerical computation. (c) Two continuous functions q(x) and s(x) specify the quaternion and the scaling ratios of local deformation for all x ∈ R3, which are represented as neural networks (NN) to be optimized. (d) The function values of q(x) and s(x) are sampled to drive a differential deformation to obtain a deformed caging mesh*

## 实验与关键发现

### 一、主实验结果

Neural Slicer 在支撑自由、强度增强及物理力学性能等多个维度上均展现出对现有方法的显著优势。

**Shelf 模型**（Fig.6）是展示强度增强效果的典型案例。在给定的外力载荷下，Neural Slicer（SF+SR 模式）生成的曲面层使最大应变相比传统平面层切片降低了 **43.3%**。可视化结果显示，曲面层在应力集中区域自动调整了局部打印方向（LPD），使其趋近于与最大主应力方向垂直，从而有效提升了层间结合强度。

**Bridge 模型**（Fig.9）是验证强度增强性能的核心基准。该模型在水平悬臂梁区域承受弯曲载荷时，层间界面恰好处于拉应力最大的位置，对切片策略极为敏感。Neural Slicer（SR 模式）给出的解接近于理想的平面层方向，而 **S³-Slicer**（Zhang et al., 2022）因在变形空间中间接优化旋转，映射回模型空间后产生了显著的层间错位。定量对比显示，Neural Slicer 将最大应变降低了 **40.5%**。更重要的是，在实物三点弯曲试验中（Fig.15），Neural Slicer 制造的样件断裂力达到约 120 N，相比 S³-Slicer 的约 60 N，**提升了 101.9%**。此外，Neural Slicer 仅需 350 层即可完成打印，而 S³-Slicer 需要 600 层，且前者重量更轻（Table 2），说明 Neural Slicer 在层数效率与材料用量上也更具优势。

**Tubes 模型**（Fig.8）是支撑自由需求的代表性测试。该模型包含多个悬垂分支，对自支撑角度约束极为敏感。Neural Slicer（SF 模式）将残余悬垂区域从 S³-Slicer 的结果中**减少了 95%**。从 LPD 与表面法线夹角的直方图可以看出，Neural Slicer 的分布更集中地落在自支撑角 α 的容许范围内，而 S³-Slicer 的分布则明显向大角度偏移——这正是 Fig.2 所揭示的变形空间间接优化导致模型空间失真的直接后果。

**Spiral Fish** 模型（Fig.12）进一步验证了支撑自由能力：Neural Slicer 将悬垂区域相比 S³-Slicer 缩减了 **94.2%**，且该结果在多种不同初始猜测下均能稳定复现。

在实物制造层面，**Bunny Head** 模型（Fig.16）的压缩试验提供了消融证据。仅使用支撑自由损失（SF only）时，模型在耳根处发生断裂；当同时加入强度增强损失（SF+SR）后，断裂部位转移至耳孔区域，且断裂力**提升了 30.6%**。这直接证明了强度增强损失项在实际力学性能上的贡献，而非仅在仿真层面有效。

### 二、关键消融实验

**点悬垂损失 L_PO 的必要性**（Fig.11）。在 Bunny Head 模型上移除 L_PO 后，右耳尖部出现了明显的点悬垂——即表面点在沿 LPD 方向上成为局部极小值，导致该区域无法被后续层覆盖。这种情况下，必须引入外部支撑结构才能完成打印，直接违背了无支撑制造的目标。该消融实验确证了 L_PO 在防止局部不可打印区域方面的关键作用。

**各向异性 FEA 的影响**（Fig.17）。当前方法使用各向同性有限元分析计算主应力场，但实际 FFF 打印件具有显著的各向异性力学属性。实验统计了 Bunny Head 模型上 LPD 与最大应力方向夹角在各向同性与各向异性 FEA 下的分布差异，结果显示角度分布有一定偏移，但**影响并不显著**——SF+SR 模式下的最大应变降低幅度在各向异性 FEA 中仍达到 36.8%（Fig.10）。这表明各向同性 FEA 在当前框架下是一个可接受的近似，但将各向异性 FEA 集成到可微优化回路中是进一步提升精度的重要方向。

**笼网格分辨率的影响**（Fig.18）。在 Spiral Fish 模型上使用不同分辨率的笼网格进行优化，所有配置均能收敛，但收敛速度和最终损失值存在差异。这说明方法对笼分辨率具有较好的鲁棒性，但缺乏自动选择最优分辨率的机制。

**场参数化方式的对比**（Fig.19）。将四元数-缩放场参数化与标量场参数化、向量场参数化进行收敛速度对比，结果显示四元数-缩放场的收敛速度最快。这从数值实验角度支持了该参数化选择的有效性，但论文明确指出尚未从理论上证明其优势。

**神经网络与直接优化的对比**（Fig.20）。使用 10 层 SIREN 网络优化四元数与缩放场的收敛速度显著快于直接使用 SGD 或 Adam 优化四面体元素中心参数的方法。这验证了神经网络作为连续场隐式参数化在优化效率上的优势。

### 三、计算效率与物理制造统计

Table 1 汇总了各模型的计算统计。所有模型的优化时间均控制在 **15 分钟以内**，其中 Bunny Head 模型（笼元素数约 8000）的优化时间约为 12 分钟。工具路径生成时间与模型规模正相关，但总体保持在可接受的离线计算范围内。

Table 2 对比了曲面层与平面层的物理制造统计。以 Bunny Head 为例，Neural Slicer 的曲面层方案使用了 200 层，而平面层方案需要 250 层，且前者在压缩试验中表现出更高的断裂力。Bridge 模型的对比更为突出：Neural Slicer 仅需 350 层，S³-Slicer 则需 600 层。

### 四、失败模式与适用边界

尽管 Neural Slicer 在多个基准上表现优异，但仍存在明确的适用边界：

1. **全局碰撞处理的退化风险**。当模型几何导致严重的全局碰撞时，当前策略是增加谐波正则化项的权重以强制生成平面层。这虽然保证了可打印性，但会削弱支撑自由和强度增强目标的满足程度。论文未提供在复杂碰撞场景下自动平衡各目标权重的机制。

2. **应力场的各向异性近似**。各向异性 FEA 尚未集成到可微优化回路中，当前使用的各向同性应力场在材料各向异性显著的场景下可能低估或误估应力分布，导致优化出的 LPD 方向并非真正的最优解。

3. **笼网格选择的经验性**。笼网格分辨率影响收敛质量，但选择过程缺乏自动化指南。对于复杂拓扑模型，笼网格的生成质量本身可能成为瓶颈。

4. **初始猜测的鲁棒性边界**。虽然 Fig.12 展示了三种不同初始猜测下均能收敛，但所有测试的初始猜测均为“合理”的场（平面场、热方法场、S³-Slicer 结果）。当初始猜测远离可行域时，基于梯度的优化是否仍能收敛，论文未给出实验证据。

![[assets/figures/papers/paper_list_l25_https_ryantaoliu_github_io_NeuralSlicer/figures/016_Figure_12.jpg]]
*Figure 12: Study conducted on a Spiral-Fish model by using different initial guesses for our Neural Slicer: (a) planar layers as a height field, (b) curved layers from a field generated by the heat method [Crane et al. 2017] and (c) curved layers as the result of*

![[assets/figures/papers/paper_list_l25_https_ryantaoliu_github_io_NeuralSlicer/figures/011_Figure_6.jpg]]
*Figure 6: The result generated by our Neural Slicer vs. the result by a planar slicer on the Shelf model: (a) the stress field under the given forces (shown as the arrows) and the model’s cage used in the computation, (b) the curved layers (bottom) generated from the mapping determined by a deformed cage (top), (c) the histograms for evaluating the quality of results in terms of (top) the angles between LPDs and surface normals for the SF requirement and (bottom) the angles between LPDs and the maximal stresses for the SR requirement, (d) the results of FEA simulation by using anisotropic material orientations defined according to the LPDs for planar layers (top) and our curved layers (bottom)*

![[assets/figures/papers/paper_list_l25_https_ryantaoliu_github_io_NeuralSlicer/figures/014_Figure_9.jpg]]
*Figure 9: Comparing our results with the result of*

## 定位与知识库关联

Neural Slicer 在曲线切片这一技术路线上，相对于最先进的方法 **S³-Slicer** (Zhang et al., 2022) 和基于向量场的强度增强方法 (Fang et al., 2020)，改变了四个关键 slot，从而突破了现有方法的瓶颈。

**1. 映射参数化方式：从离散元素到场函数**

S³-Slicer 将变形映射定义为四面体网格上逐元素的旋转与缩放，本质上是一个离散优化问题。Neural Slicer 将这一 slot 替换为两个 SIREN 神经网络分别预测全域连续四元数场 $q(x)$ 和缩放场 $s(x)$。这一改变使得优化从局部离散空间跃迁到全局连续函数空间，不仅摆脱了对高质量四面体网格的依赖，还使优化过程对初始猜测鲁棒——实验表明，使用平面场、热方法场甚至 S³-Slicer 的输出作为初始猜测，均能收敛到相近的最终损失（Fig. 12）。

**2. 优化目标定义空间：从变形空间到模型空间**

这是本工作最根本的 slot 改变。S³-Slicer 在变形空间中通过优化旋转来间接满足制造目标，然后将结果映射回模型空间。这种间接优化存在映射失真风险：变形空间中满足的角度约束，映射回模型空间后可能被破坏（Fig. 2）。Neural Slicer 改为在模型空间中基于局部打印方向（LPD）梯度 $\nabla G(x)$ 直接定义损失函数。因果链条是：神经网络输出 $q(x)$ 和 $s(x)$ → 驱动笼网格可微 ARAP 变形 → 提取标量场 $G(x)$ 的梯度作为 LPD → 在模型空间直接评估支撑自由、强度增强等损失 → 梯度反向传播至网络参数。这一设计消除了变形空间与模型空间之间的映射失真，使优化目标与制造结果直接对齐。

**3. 对几何表示的依赖：从四面体网格到表示无关**

S³-Slicer 必须基于输入模型的高质量四面体网格进行变形，这在复杂拓扑（如 Bunny Head 模型同时包含实体、开放曲面和曲线骨架）下极为困难。Neural Slicer 将计算域转移到独立生成的中间笼网格，仅需输入模型的隐式固体函数 $H(x)$ 用于最终裁剪（Fig. 4, Fig. 5）。这一 slot 改变使得方法天然支持任意表示（四面体网格、三角面片、点云等）和任意拓扑，实现了“表示无关”的曲线切片。

**4. 优化求解器：从非线性优化到神经网络随机求解器**

S³-Slicer 的非线性优化结果强烈依赖初始姿态选择。Neural Slicer 采用随机初始化的 SIREN 网络（10层，每层512神经元）作为隐式求解器，配合 Adam 优化器进行训练。消融实验证实，这种参数化方式比直接对四面体元素中心优化四元数与缩放收敛更快（Fig. 20），且四元数-缩放场参数化比标量场或向量场参数化收敛更快（Fig. 19）。

**知识库挂载点**

本工作可挂载到增材制造知识库中“计算切片”节点的“曲线层生成”子节点下，与以下工作形成关联：
- **上游依赖**：基于标量场等值面定义曲线层的思想（scalar field-based curved layer definition）；Fang et al. (2020) 利用向量场对齐应力方向进行强度增强的 pipeline。
- **平行对比**：S³-Slicer (Zhang et al., 2022) 的变形空间间接优化范式。
- **下游扩展**：本方法的核心贡献——连续场参数化 + 模型空间直接损失——为后续工作提供了可微框架，可集成各向异性有限元分析（当前方法使用各向同性 FEA，且各向异性 FEA 尚未可微分化）、动态碰撞处理等模块。

**适用边界**

- **输入要求**：需要输入模型的隐式固体表示 $H(x)$ 和主应力场 $\tau_{\max}$（通过体素 FEA 获得），以及一个包围模型的中间笼网格。笼网格分辨率影响收敛速度和最终损失值（Fig. 18），但方法缺乏对笼网格选择的自动化指南。
- **制造目标**：当前支持支撑自由（SF）、强度增强（SR）、碰撞避免（CA）三个目标，通过加权总损失 $L = w_1 \mathcal{L}_{SF} + w_2 \mathcal{L}_{SR} + w_3 \mathcal{L}_{OP} + \mathcal{L}_{HS} + \mathcal{L}_{HQ}$ 统一优化。全局碰撞处理简化为增加谐波项权重，极端情况下会强制回归平面层，削弱其他制造目标的满足。
- **计算开销**：优化时间 ≤ 15 分钟（Table 1），适用于交互式设计迭代，但尚未达到实时性能。
- **材料假设**：应力场来自各向同性 FEA，未考虑打印过程中因各向异性材料属性变化导致的应力重新分布。

**后续工作启发**

1. **可微 FEA 集成**：当前各向异性 FEA 仅用于后验分析（Fig. 17 显示其影响不显著），若将其可微分化并嵌入优化回路，有望更准确地估计打印过程中的应力演化。
2. **无笼网格方法**：中间笼网格是当前 pipeline 的必要组件，设计直接基于采样点或隐式表示计算映射的方法可进一步降低计算复杂度和人工干预。
3. **理论收敛性分析**：四元数-缩放场参数化在数值实验中被证明高效，但缺乏形式化证明，理论分析可为此类神经隐式参数化在几何处理中的应用提供基础。
4. **工艺泛化**：该框架可推广至树脂基打印、非均匀材料分布等多轴增材制造场景，只需替换相应的制造目标损失函数。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Neural_Slicer_for_Multi_axis_3D_Printing.pdf]]