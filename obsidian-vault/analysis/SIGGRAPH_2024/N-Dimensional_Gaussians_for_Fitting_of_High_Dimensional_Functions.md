---
title: N-Dimensional Gaussians for Fitting of High Dimensional Functions
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/N_Dimensional_Gaussians_for_Fitting_of_High_Dimensional_Functions.pdf
project_link: null
code_link: null
aliases:
- NDGMLCOCR
- NDGFHDF
tags:
- SIGGRAPH_2024
- topic/other_unclear
core_operator: 通过局部敏感哈希启发的高维剔除（随机投影+瓦片级3σ测试）大幅减少无关高斯计算，同时引入优化器控制的父子依赖高斯平滑细化机制，实现无分裂扰动的高质量自适应容量增长。
primary_logic: 将高维高斯组件投影到随机向量上，利用投影区间快速安全地剔除远距离组件，从而在训练与推理中保持高效；并通过在父高斯参考系中定义子高斯并仅当子高斯贡献超过阈值才将其物化为独立组件的策略，让优化器自主决定新容量的引入位置与时机，避免领域强相关启发式，实现通用的自适应拟合。
claims:
- 基于LSH的高维剔除使训练迭代时间减半，推理速度提升约3倍（Bathroom场景）
- 在合成场景上，本方法MAPE均低于Hash Grid和Pixel Generator基线
- 在真实高光场景上，PSNR显著优于3DGS和Instant NGP，且使用更少高斯、更低推理时间
- LSH剔除阈值3σ在速度与质量间取得最优平衡，更低阈值导致块状伪影
---

# N-Dimensional Gaussians for Fitting of High Dimensional Functions

> [!tip] 核心洞察
> 将高维高斯组件投影到随机向量上，利用投影区间快速安全地剔除远距离组件，从而在训练与推理中保持高效；并通过在父高斯参考系中定义子高斯并仅当子高斯贡献超过阈值才将其物化为独立组件的策略，让优化器自主决定新容量的引入位置与时机，避免领域强相关启发式，实现通用的自适应拟合。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向高维函数拟合的N维高斯方法 |
| 英文题名 | N-Dimensional Gaussians for Fitting of High Dimensional Functions |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://www.sdiolatz.info/ndg-fitting/) |
| Topic | #topic/other_unclear |
| Method | N-Dimensional Gaussian Mixture with LSH Culling and Optimization-Controlled Refinement |
| Dataset | Synthetic Scenes, Real Specular Scenes, CD Scene, Bathroom Scene |

> [!tip] 效果简介
> - Synthetic Scenes (Bathroom / Aquarium / Living Room) 上，MAPE 0.127 / 0.153 / 0.126 vs Hash Grid: 0.161/0.180/0.128; Pixel Generator: 0.415/0.168/0.178 (Ours lowest across all)。
> - Real Specular Scenes (CD / Tools) 上，PSNR 28.39 / 27.58 vs 3DGS: 25.76/26.32; INGP: 27.23/25.70 (+2.63/+1.26 over 3DGS)。
> - CD Scene 上，Inference Time (ms) / #Gaussians 24.5 ms / 3.2×10^5 vs 3DGS 62.92 ms / 10.1×10^5 (-38.4 ms / -68% Gaussians)。

## 概要

传统显式高斯混合模型在向高维扩展时面临两大瓶颈：训练与推理需对所有高斯组件求值导致计算代价高昂，且缺乏通用的自适应细化策略，难以在稀疏高维数据下同时保证模型紧凑性与重建质量。本文提出**N维自适应高斯混合表示**，核心包含三项创新：1）基于局部敏感哈希启发的高维剔除机制，通过随机投影与瓦片级3σ测试安全丢弃远距离组件，大幅减少无关计算；2）优化器控制的渐进细化策略，在父高斯参考系中定义子高斯，仅当子组件贡献超过阈值时才将其物化为独立组件，让优化器自主决定容量增长的位置与时机，避免显式分裂带来的损失尖峰；3）通过Cholesky分解参数化全协方差矩阵，保证高维各向异性分布的正定性。

在合成场景（10维表面辐射场）上，本方法MAPE全面低于Hash Grid与Pixel Generator基线；在真实高光场景（CD/Tools）上，PSNR比3DGS分别提升2.63/1.26 dB，同时高斯数量减少68%、推理时间降低约61%。LSH剔除消融实验表明，训练迭代时间减半、推理速度提升约3倍，且3σ阈值在速度与质量间取得最优平衡。该方法定位为**面向高维函数拟合的通用显式混合模型**，以无分裂扰动的自适应容量增长替代领域启发式细化，为高维稀疏数据下的紧凑表示提供了新范式。

## 核心方法与创新机理

### 问题瓶颈与核心思路

传统显式高斯混合模型在向高维扩展时面临两个根本瓶颈。第一，**计算代价随维度与组件数爆炸**：训练与推理时需对所有高斯组件逐一求值，当输入空间升至6维（位置+方向）或10维（表面点+光照/视角参数）时，暴力求值导致训练迭代与推理时间不可接受。第二，**缺乏通用的自适应容量增长策略**：3DGS依赖基于梯度统计的显式分裂/合并启发式，该过程产生损失尖峰，且其阈值选择与领域强相关，难以直接迁移至任意高维函数拟合任务。

本方法的核心洞察在于：**将高维高斯组件投影到随机向量上，利用投影区间快速安全地剔除远距离组件**，从而在训练与推理中保持高效；同时，**让优化器自主决定新容量的引入位置与时机**——通过在父高斯参考系中定义子高斯，并仅当子高斯贡献超过阈值才将其物化为独立组件，实现无分裂扰动的平滑容量增长。

### 核心模块与因果链路

方法由三个紧密耦合的模块构成，其因果链路为：N维高斯参数化（模块1）提供可优化的各向异性分布表达；基于LSH的高维剔除（模块2）在每次前向求值前大幅缩减有效组件数，使模块1的求值在计算上可行；优化器控制的渐进细化（模块3）利用模块1的Cholesky参数化定义父子依赖，在训练过程中自主增加容量，而模块2确保新增组件不会导致求值代价失控。

#### 模块1：N维高斯参数化与Cholesky分解

每个N维高斯组件由均值 $\mathbf{m} \in \mathbb{R}^N$ 和全协方差矩阵 $\mathbf{V} \in \mathbb{R}^{N \times N}$ 参数化，其响应函数为：

$$G_{\mathbf{V}}(\mathbf{x}-\mathbf{m}) = e^{-\frac{1}{2}(\mathbf{x}-\mathbf{m})^T \mathbf{V}^{-1} (\mathbf{x}-\mathbf{m})}$$

为保证协方差矩阵的正定性且便于优化，采用Cholesky分解 $\mathbf{V} = \mathbf{L} \mathbf{L}^T$，其中 $\mathbf{L}$ 为下三角矩阵。对角元素经指数激活函数约束为正，确保 $\mathbf{V}$ 始终正定。这一参数化选择是后续父子依赖细化（模块3）的基础——子高斯协方差可通过父高斯的 $\mathbf{L}$ 因子与局部参数组合表达，避免对子协方差独立进行Cholesky分解的数值不稳定。

与3DGS的三维尺度-旋转四元数参数化相比，本方法的全协方差表达具有两个优势：(1) 可刻画任意N维各向异性分布，无需将参数化适配到特定维度；(2) Cholesky分解为优化器提供了平滑的无约束参数空间，利于梯度下降。

#### 模块2：基于LSH的高维剔除

该模块是训练与推理加速的核心。其机制受局部敏感哈希（LSH）启发，通过随机投影将高维剔除问题转化为一维区间判选：

**投影计算**：对每个查询点 $\mathbf{q}$ 和高斯均值 $\mathbf{m}$，在随机单位向量 $\mathbf{r}$ 上计算投影：
$$q_{\mathbf{r}} = \mathbf{q}^T \mathbf{r}, \quad m_{\mathbf{r}} = \mathbf{m}^T \mathbf{r}$$

同时计算该高斯在方向 $\mathbf{r}$ 上的投影方差：
$$\sigma_{\mathbf{r}}^2 = \mathbf{r}^T \mathbf{V} \mathbf{r}$$

**剔除判据**：若查询点投影落于高斯投影的3σ区间外，即 $|q_{\mathbf{r}} - m_{\mathbf{r}}| \geq 3\sigma_{\mathbf{r}}$，则安全剔除该高斯。3σ阈值在速度与质量间取得最优平衡——更低阈值虽进一步加速，但会导致块状伪影（见实验部分Figure 5）。

**瓦片级批量处理**：剔除以16×16像素的瓦片为单位执行。对每个瓦片，先以所有查询点的空间范围作为边界，仅对投影落入该边界3σ邻域内的高斯保留求值。这一批量策略将剔除开销分摊到整个瓦片，相比逐像素判选大幅降低常数因子。

**因果效应**：在Bathroom场景上，LSH剔除使训练迭代时间减半，推理时间从317ms降至131ms（约3倍加速），平均每查询点求值次数从7856降至1985（减少75%）。该加速直接使高维（6-10维）高斯混合模型的训练在数分钟内可行。

#### 模块3：优化器控制的渐进细化

该模块替代了传统显式分裂/合并启发式，实现无损失尖峰的平滑容量增长。其核心机制为**父子高斯依赖**：

**父子参数化**：每个父高斯内部维护若干子高斯，子高斯的参数在父参考系中定义。给定父高斯的Cholesky因子 $\mathbf{L}$（满足 $\mathbf{V}_p = \mathbf{L}\mathbf{L}^T$），子高斯的协方差和均值通过局部参数 $(\mathbf{U}, \mathbf{m}_u)$ 表达：
$$\mathbf{V}_c = \mathbf{L} \mathbf{U} (\mathbf{L} \mathbf{U})^T, \quad \mathbf{m}_c = \mathbf{L} \mathbf{m}_u + \mathbf{m}_p$$

这一设计使子高斯天然继承父高斯的形状先验，同时允许优化器通过调整局部参数探索新的分布模式。

**物化机制**：训练以约300次迭代为一个阶段。每阶段末尾，检查各子高斯的不透明度或亮度（取决于应用场景）：若超过阈值（不透明度0.1，亮度0.01），则将该子高斯物化为独立的父高斯，并为其初始化新的子高斯；低于阈值的子高斯被丢弃。这一机制让优化器自主决定新容量的引入位置与时机——只有优化器实际“使用”的子高斯才会被保留并扩展。

**与3DGS细化的本质区别**：3DGS的显式分裂需监控梯度累积，分裂操作本身产生损失尖峰，且分裂阈值为领域相关超参数。本方法中，子高斯始终参与优化（通过父高斯的求值路径），物化过程仅改变参数的组织方式，不改变函数值，因此**损失曲线保持平滑**。此外，物化阈值（不透明度/亮度）具有明确的物理含义，跨场景泛化性好。

### 训练与推理路径

**训练路径**：
1. 初始化：在输入空间均匀采样初始父高斯，丢弃不透明度低于0.1的组件。
2. 每阶段（约300迭代）循环：
   - 对训练查询点，执行模块2的LSH剔除，筛选可见高斯。
   - 对保留的高斯求值混合模型，计算损失。
   - 反向传播更新所有参数（父高斯与子高斯的均值、协方差、颜色、不透明度/亮度）。
   - 阶段结束时，执行模块3的物化检查：将超过阈值的子高斯提升为父高斯，初始化新子高斯。
3. 方向正则化：对视角依赖应用，在训练方向间随机扰动以覆盖全空间，强制学习平滑的方向变化。

**推理路径**：
1. 对输入查询点，执行模块2的瓦片级LSH剔除。
2. 对保留的高斯求值并输出。对于体积辐射场应用，先将N维高斯投影至3D空间再计算颜色贡献；对于表面辐射场，直接在N维空间求值。

### 关键公式与应用适配

对于全局光照应用，空间点 $\mathbf{x}$ 的颜色由各高斯组件加权求和：
$$c(\mathbf{x}) = G_{\mathbf{V}_1}(\mathbf{x}-\mathbf{m}_1)\alpha_1 c_1 + \dots + G_{\mathbf{V}_k}(\mathbf{x}-\mathbf{m}_k)\alpha_k c_k$$
其中 $\alpha$ 为亮度（brightness），$c$ 为可学习颜色。该公式揭示了方法的本质：**用高斯混合模型直接拟合高维辐射函数**，而非学习3D场景几何。这使得方法天然适合表达各向异性高光、视角依赖反射等复杂效果，无需显式建模表面法线或BRDF参数。

### 方法边界与未解决问题

当前细化机制深度依赖Cholesky参数化——若直接迁移至3DGS的尺度-旋转参数化，父子依赖的表达需额外转换，可能降低性能。全协方差矩阵的存储代价随维度平方增长（$O(N^2)$ 每组件），在高维场景下组件数增加时存储压力显著，论文未探索稀疏协方差表达（如限制主成分轴数）的可能性。此外，方法对不连续边界的表现力受限于高斯混合模型的平滑本质，不如基于ReLU的隐式模型自然锐利。

## 实验与关键发现

### 合成场景：高维明暗处理函数的拟合精度

在三个合成场景（Bathroom / Aquarium / Living Room）上，本文方法以MAPE（Mean Absolute Percentage Error）为指标，与隐式生成网络**Pixel Generator**（Diolatzis et al., 2022）和混合哈希网格表示**Hash Grid**（Müller et al., 2022）进行了对比。如表1所示，本方法在所有三个场景上均取得最低误差：Bathroom场景0.127（Hash Grid 0.161，Pixel Generator 0.415），Aquarium场景0.153（Hash Grid 0.180，Pixel Generator 0.168），Living Room场景0.126（Hash Grid 0.128，Pixel Generator 0.178）。值得注意的是，Pixel Generator在Bathroom场景上MAPE高达0.415，暴露出隐式网络在捕捉高维各向异性变化时的系统性不足；而Hash Grid虽在Living Room场景上与本方法接近（0.128 vs 0.126），但在Aquarium场景上差距拉大（0.180 vs 0.153），说明混合表示对复杂反射变化的适应性仍弱于显式高斯混合。本方法在仅数分钟训练内即达到上述精度，且支持快速渲染与交互。

### 真实高光场景：视角依赖效果的PSNR对比

在真实拍摄的高光场景（CD / Tools）上，本方法与**3DGS**（Kerbl et al., 2023）、**Instant NGP**（Müller et al., 2022）及**NeX**进行了PSNR对比（表2）。在CD场景上，本方法PSNR达28.39 dB，显著高于3DGS的25.76 dB（+2.63 dB）和INGP的27.23 dB（+1.16 dB）；在Tools场景上，本方法27.58 dB，高于3DGS的26.32 dB（+1.26 dB）和INGP的25.70 dB（+1.88 dB）。定性结果（Figure 6）进一步证实，本方法对各向异性反射随视角移动的复现更为准确，而3DGS和INGP在镜面高光区域的保真度明显不足。

![[assets/figures/papers/paper_list_l24_https_www_sdiolatz_info_ndg_fitting/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative results of our method compared 3DGS and Instant-NGP for two different scenes with complex view dependent effects*

需注意公平性边界：NeX的PSNR直接取自其论文，且其训练分辨率受限，与本方法在不同分辨率下比较，可对比性有限（表2脚注）。此外，3DGS的C++渲染器性能显著优于其Python版本，而本文仅使用Python版本比较推理时间——若集成至同一C++框架，本方法亦能获益。

### 推理效率与模型紧凑性

表3报告了CD场景训练结束时的高斯数量与推理时间。本方法仅需约3.2×10⁵个高斯组件，推理时间24.5 ms；而3DGS需要10.1×10⁵个高斯（多出约68%），推理时间62.92 ms（慢约2.6倍）。这意味着本方法在取得更高PSNR的同时，使用了更少的组件和更低的推理开销，直接证明了高维各向异性高斯混合在表达效率上的优势——用更少的组件即可捕捉更丰富的视角依赖细节。

### LSH剔除消融：速度与质量的权衡

Bathroom场景上的LSH剔除消融实验（表4）是支撑核心加速机制的关键证据。启用LSH剔除后，推理时间从317 ms降至131 ms（加速约2.4倍），平均每像素高斯求值次数从7856.0骤降至1984.89（减少约75%）；训练迭代时间亦减半。这验证了随机投影+瓦片级3σ剔除策略在高维空间中确实能安全丢弃大量不相关组件，且未引入额外伪影。

阈值参数消融（Figure 5）揭示了安全边界：本文选择的3σ阈值在速度与质量间取得最优平衡。当阈值降至2σ或1.5σ时，推理速度虽进一步提升，但图像开始出现块状伪影（图中红色箭头指示），原因是过于激进的剔除丢弃了本应对像素有贡献的高斯组件。这一现象揭示了LSH启发式剔除的本质局限：单次随机投影的区间判定是一种概率性安全剔除，过低的σ乘数会突破“安全”边界，导致不可逆的信息丢失。

![[assets/figures/papers/paper_list_l24_https_www_sdiolatz_info_ndg_fitting/figures/009_Figure_5.jpg]]
*Figure 5: Demonstration of the impact to image quality and inference time for different values of LSH threshold. With red arrows we point out the artifacts that appear when the threshold is set to lower values than our choice of 3??*

### 公平性说明与性能边界

在解读上述效率数据时，需注意以下公平性约束：
- Hash Grid基线使用C++绑定调用，而本方法为纯Python实现，因此表4中的迭代时间比较存在不公平因素。
- 3DGS的推理时间比较同样基于Python版泼溅渲染器，若双方均迁移至C++框架，绝对时间差距可能缩小，但相对加速趋势应保持。
- 本方法的高斯组件存储成本随维度平方增长（全协方差矩阵），虽然当前实验维度（6D/10D）下尚可接受，但论文明确指出这一二次存储开销是向更高维度扩展的潜在瓶颈，稀疏化协方差表达（如限制主成分轴数）尚未探索。

### 失败模式与适用边界

1. **过拟合与混叠风险**：论文明确指出的核心局限是，随着输入维度增加，对参考数据的过拟合与混叠风险加剧，需要更大的训练样本量。在真实360°稀疏视点场景下，仅靠方向正则化（随机扰动训练方向以覆盖全空间）可能不足，可能需要额外的专门调优。

2. **不连续边界的表现力**：由于表示基于高斯混合模型，对锐利不连续边界的表现力不如基于ReLU的隐式模型自然。这是显式分布基元表示的内在特性，而非本方法特有缺陷。

3. **细化机制的参数化依赖**：当前优化器控制的父子高斯细化策略深度依赖Cholesky分解参数化。若直接迁移至3DGS的尺度-旋转参数化，会因额外转换而复杂化，且可能降低性能。这意味着该细化机制目前并非“即插即用”的通用模块。

4. **动态场景的局限**：本方法仅提供高维混合模型的静态切片求值，未内在解决物体运动一致性与时序对应问题——这是显式表示在动态场景中的共性挑战。

![[assets/figures/papers/paper_list_l24_https_www_sdiolatz_info_ndg_fitting/figures/005_Table_1.jpg]]
*Table 1: In this table we report Mean Absolute Percentage Error (MAPE) for each method in our synthetic scenes dataset*

![[assets/figures/papers/paper_list_l24_https_www_sdiolatz_info_ndg_fitting/figures/006_Table_4.jpg]]
*Table 4: Iteration time (during training and inference) of our method (with and without LSH culling), the Pixel Generator and the Hash Grid baselines for the Bathroom scene*

![[assets/figures/papers/paper_list_l24_https_www_sdiolatz_info_ndg_fitting/figures/007_Table_2.jpg]]
*Table 2: Quantitative evaluation of our method against 3DGS, Instant NGP and NeX for our two scenes. We show training resolution, training times and PSNR for all methods. Nex metrics are provided from their paper*

![[assets/figures/papers/paper_list_l24_https_www_sdiolatz_info_ndg_fitting/figures/010_Table_3.jpg]]
*Table 3: We report the number of Gaussians at the end of training for our method and 3DGS as well as the inference time for both methods using the Python splatting renderer of [Kerbl et al. 2023]*

## 定位与知识库关联

本工作在“高维函数拟合表示”这一知识库节点上做出了关键推进：**将显式高斯混合模型从低维（3D/4D）推广至任意N维，并通过两个协同机制解决了此前显式模型在高维下的根本性瓶颈**——训练与推理时对所有组件的全量求值，以及缺乏通用自适应容量增长策略。

### 相对于已有方法的本质差异

本方法改变的**核心slot**是**高维高斯组件的可见性判定与容量增长方式**，这使其与以下基线形成本质区别：

- **相对于3DGS (Kerbl et al., 2023)**：3DGS在3维空间内工作，其剔除策略依赖图像平面投影的空间判选，细化策略采用基于梯度统计的显式分裂/克隆启发式，分裂过程会产生损失尖峰。本方法将参数化slot从3维均值与尺度-旋转协方差推广至N维均值与全协方差（Cholesky分解），将剔除slot从图像空间剔除替换为基于局部敏感哈希（LSH）启发的高维随机投影剔除，将细化slot从显式分裂替换为优化器控制的父子依赖渐进物化机制。在真实高光场景（CD/Tools）上，本方法用**少68%的高斯数量**（3.2×10⁵ vs 10.1×10⁵）取得了**+2.63/+1.26 dB PSNR**的提升，且推理时间从62.92 ms降至24.5 ms（Table 2, Table 3）。

- **相对于Instant NGP (Müller et al., 2022)**：Instant NGP采用混合隐式-显式方案（哈希网格+小MLP），其表示能力受限于网格分辨率与MLP容量的权衡。本方法完全显式，无需MLP解码，在高光场景上PSNR优于INGP（CD: 28.39 vs 27.23; Tools: 27.58 vs 25.70），且训练时间相当（Table 2）。关键差异在于：显式高斯混合提供了**直接可解释的空间局部性**，而哈希网格的隐式特征需要MLP解耦。

- **相对于NeX与Pixel Generator**：NeX是面向高光效应的隐式神经渲染方法，但训练时间长且分辨率受限；Pixel Generator (Diolatzis et al., 2022) 是隐式生成网络。本方法在合成场景的MAPE上全面优于Pixel Generator（Bathroom: 0.127 vs 0.415; Aquarium: 0.153 vs 0.168; Living Room: 0.126 vs 0.178），且训练仅需数分钟（Table 1）。

### 知识库挂载点

本方法可挂载至以下知识库分支：

1. **显式神经表示 (Explicit Neural Representations)**：作为3DGS向高维的推广，本方法证明了显式高斯混合在6维（位置+方向）乃至10维（表面辐射场）空间中的可行性。挂载关键词：`N-Dimensional Gaussian Mixture`、`Cholesky Covariance Parameterization`。

2. **高维近邻搜索与剔除 (High-Dimensional Culling)**：LSH启发的高维剔除策略（随机投影+瓦片级3σ测试）是一个通用加速模块，可独立应用于任何需要在高维空间中快速排除远距离高斯组件的场景。该模块将Bathroom场景的平均求值次数从7856降至1985（-75%），推理时间从317 ms降至131 ms（Table 4）。

3. **自适应容量增长 (Adaptive Capacity Growth)**：优化器控制的父子依赖细化机制提供了一种**无分裂扰动**的容量增长范式。子高斯在父高斯的Cholesky参考系中定义（$\mathbf{V_c} = \mathbf{L} \mathbf{U} (\mathbf{L} \mathbf{U})^T$，$\mathbf{m}_c = \mathbf{L} \mathbf{m}_u + \mathbf{m}_p$），仅当其不透明度/亮度超过阈值（0.1/0.01）时才物化为独立组件。这避免了3DGS分裂启发式中梯度统计阈值的手动调节和损失尖峰问题。

### 适用边界

- **维度上限**：全协方差矩阵的存储与计算开销随维度平方增长（$O(N^2)$），论文未探索稀疏化策略。对于极高维（N>20）的输入空间，存储可能成为瓶颈。
- **不连续边界**：高斯混合模型本质上是平滑基函数的组合，对锐利不连续边界的表现力不如基于ReLU的隐式模型自然。
- **动态场景**：本方法仅提供高维混合模型的静态切片求值，未内在解决物体运动一致性与时序对应问题。
- **稀疏视点**：在真实360°稀疏视点场景下，仅靠方向正则化（随机扰动训练方向）可能不足以防止过拟合，需额外调优。

### 后续启发与开放问题

1. **协方差参数化的泛化**：当前细化机制深度依赖Cholesky分解，直接迁移至3DGS的尺度-旋转参数化会因额外转换而复杂化。探索如何将优化器控制的自适应细化适配至其他协方差表达（如限制主成分轴数的稀疏表达），可降低高维存储开销并减少超参数。

2. **替代分布基元**：论文提出了开放问题——是否可探索非高斯分布基元（如Student-t分布、混合指数分布）以实现更好的控制、收敛性与紧凑性。这直接关联到知识库中“表示基元选择”节点。

3. **LSH剔除的通用性**：瓦片级高维剔除策略本身不限于高斯混合模型，可推广至任何需要在高维查询中快速筛选候选组件的显式表示，例如高维粒子系统、高维点云渲染等。

4. **与C++渲染管线的集成**：论文坦诚指出，3DGS的C++渲染器性能显著优于Python版本，而本方法的Python实现与Hash Grid的C++绑定比较存在不公平因素（Table 4备注）。将本方法的剔除与求值集成到同一C++框架中，预期可获得进一步的推理加速。

5. **动态场景扩展**：如何在保持显式表示局部性优势的同时，捕捉可见物体的连贯运动与一致性对应，是将本方法推向4D/5D动态辐射场的关键挑战。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/N_Dimensional_Gaussians_for_Fitting_of_High_Dimensional_Functions.pdf]]