---
title: "ShaderTransformer: Predicting Shader Quality via One-shot Embedding for Fast Simplification"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/ShaderTransformer_Predicting_Shader_Quality_via_One_shot_Embedding_for_Fast_Simplification.pdf
project_link: "https://jingsenzhu.github.io/i2-sdf"
code_link: null
aliases:
- IS
- ShaderTransformer
tags:
- SIGGRAPH_2022
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 引入气泡损失（bubble loss）和误差引导的自适应采样：利用深度图在缺失表面点插入“气泡”，为SDF网络恢复梯度信号；同时根据重建误差构造采样分布，将计算资源集中到缺失的高频区域。
primary_logic: 通过从深度图注入气泡点来激活SDF网络对细小结构的梯度，结合误差引导的自适应采样以聚焦于缺失物体区域，可以在不依赖额外数据的情况下显著改善对复杂室内场景中细薄物体的重建，进而实现高质量的基于物理的场景内在分解和真实感编辑。
claims:
- 在合成数据集上的几何重建结果（F-Score 0.83）显著优于VolSDF-D（0.68）、NeuRIS（0.66）和MonoSDF（0.77），尤其是细小物体的重建完整性明显改善。
- 误差引导的自适应采样策略在重建精度上明显优于均匀采样，即便在使用带噪声深度的情况下仍优于基于地面真值的均匀采样方案。
- Synthetic Dataset (ours, 8 scenes) 上 PSNR (novel view synthesis) = 29.70
- Real Scenes (4 scenes) 上 PSNR (novel view synthesis) = 25.15
---

# ShaderTransformer: Predicting Shader Quality via One-shot Embedding for Fast Simplification

> [!tip] 核心洞察
> 通过从深度图注入气泡点来激活SDF网络对细小结构的梯度，结合误差引导的自适应采样以聚焦于缺失物体区域，可以在不依赖额外数据的情况下显著改善对复杂室内场景中细薄物体的重建，进而实现高质量的基于物理的场景内在分解和真实感编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | I2-SDF：基于神经SDF光线追踪的室内场景内在重建与编辑 |
| 英文题名 | ShaderTransformer: Predicting Shader Quality via One-shot Embedding for Fast Simplification |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [Project](https://jingsenzhu.github.io/i2-sdf) |
| Topic | #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | I2-SDF |
| Dataset | Synthetic Dataset, Real Scenes |

> [!tip] 效果简介
> - Synthetic Dataset (ours, 8 scenes) 上，PSNR (novel view synthesis) 29.70 vs 27.09 (NeRF) (+2.61 dB)。
> - Real Scenes (4 scenes) 上，PSNR (novel view synthesis) 25.15 vs 24.66 (NeRF) (+0.49 dB)。
> - Synthetic Dataset (with GT meshes) 上，F-Score (geometry reconstruction) 0.83 vs 0.68 (VolSDF-D) (+0.15)。

## 概要

现有基于神经隐式表面表示的方法（如 VolSDF、NeuRIS、MonoSDF）在重建室内场景中的细小与薄结构物体（如灯具、吊灯、灯杆）时面临严重困难，导致几何质量差且无法支撑后续的材质编辑与重光照。I2‑SDF 提出了一种整体式神经符号距离场框架，核心创新包括：引入**气泡损失**（bubble loss），从深度图中注入缺失表面点以恢复 SDF 网络的梯度信号；结合**误差引导的自适应采样**策略，将计算资源集中于缺失的高频区域。在此基础上，方法进一步利用可微蒙特卡洛光线追踪实现场景的内在分解，输出材质场与发光场，支持真实感场景编辑与重光照。在合成数据集上，I2‑SDF 的几何重建 F‑Score 达到 0.83，显著优于 VolSDF‑D（0.68）、NeuRIS（0.66）和 MonoSDF（0.77）；在新视角合成任务中，PSNR 达到 29.70 dB，较 NeRF 基线提升 2.61 dB。消融实验表明，误差引导的自适应采样在重建精度上明显优于均匀采样，且方法对深度噪声具有良好的鲁棒性。该方法定位于结合几何先验与基于物理的渲染，为室内场景的内在重建与编辑提供了新的基准。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有基于神经隐式表面表示的方法（如 **VolSDF**、**NeuRIS**、**MonoSDF**）在重建室内场景时，对细小物体与薄结构（如吊灯、灯杆、灯具支撑线）的重建能力严重不足。这类结构在深度图中占据极少像素，导致 SDF 网络在该区域的梯度信号几乎消失——网络无法感知到这些表面点的存在，从而产生塌陷或缺失的几何。这一问题直接阻碍了后续的材质分解与真实感编辑，因为不完整的几何无法支撑基于物理的光线追踪渲染。

I2-SDF 的核心洞察是：**通过从深度图注入“气泡点”来激活 SDF 网络对缺失细小结构的梯度，并结合误差引导的自适应采样将计算资源集中到这些高频区域，可以在不依赖额外数据的情况下显著改善薄结构重建，进而实现高质量的场景内在分解与编辑。**

### 方法框架与模块顺序

I2-SDF 采用两阶段训练框架，整体流程如图 2 所示：

**第一阶段：几何与辐射场联合学习。** 从多视图 RGB 图像和深度/法线先验出发，同时训练神经 SDF 场 $F_d$ 和神经辐射场 $F_c$，并引入气泡损失与自适应采样策略来改善细小物体的几何重建。同时训练发光语义场 $F_e$ 以识别场景中的光源区域。

**第二阶段：材质场学习与内在分解。** 固定第一阶段的几何和发光场，训练神经材质场（漫反射率场 $F_a$ 和粗糙度场 $F_\rho$），通过可微蒙特卡洛光线追踪层进行基于物理的内在渲染，最小化重渲染与输入图像之间的误差。

各模块的因果链接为：$F_d$ 提供场景几何表面 → $F_c$ 提供视角相关的辐射场用于第一阶段渲染监督 → 气泡损失与自适应采样直接优化 $F_d$ 对薄结构的表达能力 → $F_e$ 识别光源为第二阶段提供发光先验 → $F_a$ 和 $F_\rho$ 在固定几何上建模空间变化的材质 → 蒙特卡洛光线追踪层将几何、材质、发光统一为物理正确的重渲染结果。

### 关键创新模块一：气泡损失（Bubble Loss）

气泡损失是解决细小物体重建瓶颈的核心机制。其工作原理如下：

对于深度图中的每个像素 $\mathbf{p}$，利用相机内外参将其反投影到三维空间，得到表面点：

$$\mathbf{x}(\mathbf{p}, D) = \mathbf{t} + D(u,v) \left( \mathbf{R} \mathbf{K}^{-1} \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} \right)$$

当 SDF 网络尚未学习到某个细小结构时，该表面点处的 SDF 绝对值 $|d(\mathbf{x}(\mathbf{p}, D))|$ 会很大（网络认为该点远离表面）。气泡损失显式惩罚这一绝对值：

$$\mathcal{L}_{\mathrm{bubble}} = \sum_{\mathbf{p} \in \mathcal{P}} | d(\mathbf{x}(\mathbf{p}, D)) |$$

其因果机制如图 3 所示：当薄结构未被学习时，SDF 在该区域的梯度消失（左图）；插入气泡点后，损失函数为网络提供了指向零水平集的梯度信号（中图）；随着训练进行，气泡点“生长”为完整的表面（右图）。这一机制本质上是在缺失表面处注入人工的符号距离约束，迫使网络将零水平集扩展到这些区域。

### 关键创新模块二：误差引导的自适应采样（Error-Guided Adaptive Sampling）

均匀采样策略将计算资源平均分配到所有像素，导致细小物体所在的高频区域采样不足。I2-SDF 提出基于重建误差的概率密度函数（PDF）进行重要性采样。

具体而言，维护一个重建误差图 $E(\mathbf{p})$，记录每个像素在最近训练迭代中的渲染误差。采样时，像素 $\mathbf{p}$ 被选中的概率正比于 $E(\mathbf{p})$：

$$P(\mathbf{p}) \propto E(\mathbf{p})$$

这一策略的因果链条为：细小物体区域的重建误差天然较高 → 自适应采样自动增加这些区域的采样密度 → 气泡损失和深度损失在这些区域获得更多梯度更新 → 薄结构重建质量持续改善。图 11 可视化了训练过程中误差 PDF 图的演化，可以观察到采样分布逐渐聚焦到高频细节区域。

### 关键创新模块三：可微蒙特卡洛光线追踪与内在分解

与现有方法仅建模视角相关的辐射场不同，I2-SDF 将场景外观显式分解为几何、材质和发光三个内在分量，并通过可微蒙特卡洛光线追踪实现物理正确的重渲染。

**光线追踪求交。** 对于每条光线 $\mathbf{r}$，通过体积渲染累积透射率来估计与神经 SDF 表面的交点 $\mathbf{s}$：

$$\mathbf{s} = \mathrm{trace}(\mathbf{r}) = \mathbf{o} + \left( \sum_{i=1}^{M} T_{\mathbf{r}}^i \alpha_{\mathbf{r}}^i t_{\mathbf{r}}^i \right) \mathbf{d}$$

**基于物理的表面着色。** 在交点 $\mathbf{s}$ 处，使用 GGX 微面元 BRDF 模型，通过蒙特卡洛重要性采样渲染表面颜色：

$$\hat{\mathbf{R}}(\mathbf{s}) = \frac{1}{N} \sum_{k=1}^{N} \frac{f_r(\mathbf{v_s}, \mathbf{d_s}^k; \hat{N}, \hat{K}_d, \hat{K}_s, \hat{\rho}) (\mathbf{d_s}^k \cdot \hat{N}) L_i(\mathbf{s}, \mathbf{d_s}^k)}{p(\mathbf{d_s}^k)}$$

其中 $\hat{N}$ 为 SDF 梯度法线，$\hat{K}_d$ 和 $\hat{K}_s$ 为漫反射率和镜面反射率（由 $F_a$ 输出），$\hat{\rho}$ 为粗糙度（由 $F_\rho$ 输出），$L_i$ 为入射辐射（由 $F_e$ 提供）。

**发光语义场。** $F_e$ 不仅输出辐射值，还输出一个发射语义 logit，通过语义损失 $\mathcal{L}_{\mathrm{emi}}$ 监督，使网络自动识别光源区域（如灯泡、窗户），为第二阶段的光线追踪提供发光先验。

### 训练路径与损失函数

**第一阶段总损失：**

$$\mathcal{L}_{1} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{geo}} \mathcal{L}_{\mathrm{geo}} + \lambda_{\mathrm{emi}} \mathcal{L}_{\mathrm{emi}}$$

其中 $\mathcal{L}_{\mathrm{rgb}}$ 为体积渲染颜色与输入 RGB 的 L1 误差，几何损失 $\mathcal{L}_{\mathrm{geo}}$ 展开为：

$$\mathcal{L}_{\mathrm{geo}} = \lambda_{1} \mathcal{L}_{\mathrm{eikonal}} + \lambda_{2} \mathcal{L}_{\mathrm{depth}} + \lambda_{3} \mathcal{L}_{\mathrm{normal}} + \lambda_{4} \mathcal{L}_{\mathrm{smooth}} + \lambda_{5} \mathcal{L}_{\mathrm{bubble}}$$

- $\mathcal{L}_{\mathrm{eikonal}} = \sum_{\mathbf{x} \in \mathcal{X}} ( \| \nabla d(\mathbf{x}) \|_2 - 1 )^2$：约束 SDF 梯度范数为 1，保证符号距离函数的数学性质。
- $\mathcal{L}_{\mathrm{depth}} = \sum_{\mathbf{r} \in \mathcal{R}} \| \hat{D}(\mathbf{r}) - D(\mathbf{r}) \|_1$：体积渲染深度与真实深度的 L1 误差。
- $\mathcal{L}_{\mathrm{normal}}$ 和 $\mathcal{L}_{\mathrm{smooth}}$：法线一致性约束和平滑正则。
- $\mathcal{L}_{\mathrm{bubble}}$：气泡损失，激活细小结构的梯度信号。

**第二阶段总损失：**

$$\mathcal{L}_{2} = \mathcal{L}_{\mathrm{render}} + \lambda_{\mathrm{mat}} \mathcal{L}_{\mathrm{mat}}$$

其中 $\mathcal{L}_{\mathrm{render}} = \sum_{\mathbf{r} \in \mathcal{R}} \| \hat{\mathbf{R}}(\mathbf{s}(\mathbf{r})) - \mathbf{C}(\mathbf{r}) \|_1$ 为蒙特卡洛重渲染结果与输入图像之间的 L1 误差，$\mathcal{L}_{\mathrm{mat}}$ 为材质平滑正则项。

### 与基线方法的关键差异

| 维度 | VolSDF-D / NeuRIS / MonoSDF | I2-SDF |
|------|---------------------------|--------|
| 细小物体重建 | 依赖标准损失，梯度消失 | 气泡损失注入梯度信号 |
| 采样策略 | 均匀随机采样 | 误差引导的自适应重要性采样 |
| 场景表示 | 仅视角相关辐射场 | 几何-材质-发光内在分解 |
| 渲染方式 | 体积渲染 | 可微蒙特卡洛光线追踪 |
| 编辑能力 | 不支持 | 支持材质编辑与重光照 |

I2-SDF 以 **VolSDF** 作为神经隐式表示的骨干网络，保留其 SDF 参数化 $F_d$ 和辐射场 $F_c$ 的基本架构，但在三个关键槽位上进行了替换：几何损失中增加气泡项、采样策略从均匀改为误差引导、渲染模型从纯辐射场升级为基于物理的内在分解与光线追踪。这三个改变形成因果闭环——气泡损失改善几何完整性 → 完整几何支撑准确的光线追踪求交 → 准确的求交使材质分解更可靠 → 最终实现照片级真实的场景编辑与重光照。

![[assets/figures/papers/sig_p2_36k_l8_http_www_cad_zju_edu_cn_home_rwang/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our pipeline. Multi-view images are used to learn the underlying neural SDF field*

## 实验与关键发现

### 新视角合成与几何重建的主结果

I2-SDF在合成数据集与真实场景上均进行了系统评估，涵盖新视角合成质量和几何重建精度两个核心维度。

**新视角合成。** 在自建的8个合成室内场景上，I2-SDF取得了29.70 dB的PSNR，相比NeRF基线（27.09 dB）提升+2.61 dB（Table 4）。在4个真实场景上，PSNR为25.15 dB，略高于NeRF的24.66 dB（+0.49 dB）。值得注意的是，NeRF和Instant-NGP未使用深度或法线等几何监督，因此虽然其视图合成指标不低，但几何一致性显著弱于隐式表面方法。与同样使用深度监督的VolSDF-D相比，I2-SDF在合成数据上的PSNR优势更为明显，这主要归因于气泡损失和自适应采样策略对细小物体区域的几何改善，进而提升了该区域的渲染质量。

**几何重建。** 在合成数据集的几何重建评估中（Table 2），I2-SDF的F-Score达到0.83，显著优于VolSDF-D（0.68）、NeuRIS（0.66）和MonoSDF（0.77）。F-Score的提升主要来自对灯具、吊灯、灯杆等细小薄结构的重建完整性改善——这正是现有方法普遍失败的瓶颈区域（Figure 1左半部分）。定性结果（Figure 5、Figure 13）显示，I2-SDF恢复的深度图和法线图在这些高频区域具有明显更清晰的结构边界，而基线方法则倾向于将这些细小物体“抹平”或完全丢失。

### 关键消融实验

消融实验围绕两个核心设计选择展开：气泡损失与深度噪声鲁棒性，以及误差引导的自适应采样策略。

**深度噪声鲁棒性。** Table 3报告了深度噪声对重建质量的影响。使用标准噪声模型（σ noise）时，几何重建指标和PSNR的下降幅度极小，表明方法对深度传感器的常见噪声水平具有良好的鲁棒性。即使将噪声幅度放大至3倍（3σ noise），重建质量虽有所下降，但仍然优于使用地面真值深度但采用均匀采样的方案。这一结果表明，气泡损失并非简单依赖精确深度，而是通过从深度图注入梯度信号来激活SDF网络对缺失区域的感知能力，其效果在深度不完美时依然成立。

**自适应采样 vs. 均匀采样。** 采样策略的消融结果（Table 3、Figure 8）是最具决定性的证据之一。在相同深度质量条件下，误差引导的自适应采样在PSNR和几何指标上均显著优于均匀采样。更关键的是：即使使用带噪声的深度（σ noise），自适应采样的PSNR仍然高于使用地面真值深度但采用均匀采样的方案。这一因果链表明，自适应采样通过将计算资源集中到重建误差大的高频区域（即细小物体所在位置），直接解决了瓶颈问题的资源分配维度——不是缺乏信息，而是信息没有被有效利用。Figure 11可视化了训练过程中误差PDF图的演化，直观展示了采样分布如何逐步聚焦到缺失物体区域。

### 方法边界与失败模式

**高频纹理的渲染局限。** 当前方法采用基于MLP的网络骨干来建模材质场和辐射场，其表示能力有限，难以有效捕捉精细的高频纹理细节。这在材质分解结果（Figure 12、Figure 16）中表现为：漫反射率预测能捕捉到整体颜色分布，但表面纹理的锐利度不足。这一局限与NeRF类方法的MLP容量瓶颈一致，并非本方法特有，但在追求照片级编辑的应用场景中构成实际约束。

**计算开销与可扩展性。** 可微蒙特卡洛光线追踪是方法实现内在分解和重光照的关键，但也带来了极大的计算开销。材质阶段（第二阶段）的训练需要2-3天，这显著限制了方法的实用性和对更大场景的可扩展性。该开销主要来自每次迭代中需要在三维体空间中进行大量光线追踪采样以估计入射辐射度，这是当前基于物理的神经渲染方法的共性难题。

**对几何先验的依赖。** 气泡损失和自适应采样策略均依赖于深度图和法线图作为几何先验。虽然消融实验证明了方法对深度噪声的鲁棒性，但在完全没有深度先验的场景中（例如仅凭稀疏视角或纹理贫乏区域），细小物体的重建质量将无法得到保证。方法本质上是对现有几何监督的“更有效利用”，而非完全摆脱对几何先验的需求。

**场景类型边界。** 所有实验均在室内场景上进行，场景特点为漫反射为主、光照相对可控。方法能否推广到室外大场景（几何尺度更大、光照条件更复杂）、动态光照环境或强镜面反射场景，尚缺乏实验证据支持。

![[assets/figures/papers/sig_p2_36k_l8_http_www_cad_zju_edu_cn_home_rwang/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparisons of geometric reconstruction results on synthetic data*

![[assets/figures/papers/sig_p2_36k_l8_http_www_cad_zju_edu_cn_home_rwang/figures/010_Table_3.jpg]]
*Table 3: Ablation studies on noisy depth and sampling strategy. “σ noise” and “3σ noise” means using the standard noise model and 3 times noise model. “σ noise” induces negligible negative effects, while “3σ noise” still outperforms “Uniform”*

![[assets/figures/papers/sig_p2_36k_l8_http_www_cad_zju_edu_cn_home_rwang/figures/008_Figure_8.jpg]]
*Figure 8: Sampling strategy*

![[assets/figures/papers/sig_p2_36k_l8_http_www_cad_zju_edu_cn_home_rwang/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative comparisons of reconstructed depth map and normal map (real data). Zoom in for details*

![[assets/figures/papers/sig_p2_36k_l8_http_www_cad_zju_edu_cn_home_rwang/figures/015_Table_4.jpg]]
*Table 4: Comparisons of per-scene novel view PSNR*

## 定位与知识库关联

I2-SDF 的核心贡献在于**改变了室内场景神经隐式重建中“几何监督信号注入方式”这一关键 slot**，并在此基础上将重建结果接入可微物理渲染管线，从而打通从多视图图像到可编辑内在场景表示的完整链路。

### 改变的 slot：从被动表面正则到主动缺失区域梯度注入

现有神经隐式表面重建方法——例如 **VolSDF** (Yariv et al., NeurIPS 2021)、**NeuRIS** (Wang et al., CVPR 2023) 和 **MonoSDF** (Yu et al., CVPR 2022)——在几何优化中主要依赖 Eikonal 损失、深度损失和法线损失等**表面正则项**。这些损失作用于已存在（或被深度观测覆盖）的表面区域，但对于细小物体和薄结构（如灯具、吊灯灯杆），SDF 网络在训练早期便无法感知这些区域的存在，导致梯度消失，形成不可恢复的几何缺失。这是一种**被动式的几何约束策略**：损失函数只能“加固”网络已经学到的表面，却无法主动引导网络去发现被忽略的结构。

I2-SDF 将这一 slot 替换为**主动缺失区域梯度注入机制**，具体包含两个耦合组件：

1. **气泡损失（Bubble Loss）**：利用深度图在缺失表面点处显式插入“气泡”，惩罚这些位置上的 SDF 绝对值 $|d(\mathbf{x})|$，从而为 SDF 网络恢复梯度信号。这相当于在几何场的零水平集附近“播种”梯度源，引导网络生长出原本被忽略的细小几何。

2. **误差引导的自适应采样**：根据重建误差构造采样概率分布，将计算资源集中到缺失的高频区域，确保气泡损失作用在真正需要的位置，而非均匀浪费在已重建良好的区域。

这一改变的因果机制是：**梯度信号源头从“表面正则”转变为“缺失区域主动注入”**，使得方法能够在不依赖额外数据或更强先验的情况下，显著提升对细薄物体的重建完整性。

### 知识库挂载点

I2-SDF 可挂载到以下知识节点：

- **神经隐式表面重建**（VolSDF 系列）：作为几何表示的骨干网络，I2-SDF 直接继承 VolSDF 的 SDF 参数化与体积渲染框架，但在损失函数和采样策略层面进行了针对性改造。气泡损失可视为对 Eikonal 损失体系的一种**补充性梯度注入机制**，而非替代。

- **基于物理的内在分解与重光照**：在几何重建完成后，I2-SDF 引入可微蒙特卡洛光线追踪层，将场景分解为材质场（漫反射率、粗糙度）和发光场。这一设计与 **NVDiffRec** (Munkberg et al., SIGGRAPH 2022) 等基于网格的内在分解方法形成对比：I2-SDF 在隐式 SDF 空间中进行光线追踪，避免了显式网格提取带来的拓扑约束，但代价是极高的计算开销。

- **深度图引导的神经重建**：方法依赖多视图深度图作为监督信号，与 **NeuRIS** 等利用多视角先验的思路不同，I2-SDF 将深度图从单纯的监督信号升级为**梯度激活源**（通过气泡损失），这是对深度先验利用方式的根本性拓展。

### 适用边界

1. **场景类型**：方法专为室内场景设计，依赖相对可控的光照条件和丰富的可见表面。对于室外大场景、动态光照或强镜面反射环境，当前框架未经验证，且 MC 光线追踪的计算负担可能进一步加剧。

2. **数据依赖**：气泡损失和自适应采样强依赖深度图的可用性。尽管消融实验表明方法对深度噪声具有良好的鲁棒性（Table 3），但在完全无深度先验的条件下，气泡损失无法发挥作用，细小物体的重建质量将回退到基线水平。

3. **计算成本**：可微 MC 光线追踪使材质阶段训练需要 2–3 天，这限制了方法在交互式应用场景中的实用性。MLP 骨干对高频纹理的表示能力也存在上限。

### 后续启发

I2-SDF 的“气泡”思想——从观测数据中识别缺失区域并主动注入梯度——具有跨任务迁移的潜力。例如，在稀疏视角重建或遮挡区域补全中，可借鉴类似的“缺失感知梯度注入”策略。此外，误差引导的自适应采样为神经渲染中的计算资源分配提供了新的视角：将采样密度与重建不确定性绑定，而非仅依赖视角或几何先验。未来工作若能将气泡机制与更高效的采样或轻量级神经渲染技术结合，有望在保持细薄物体重建质量的同时，大幅降低计算开销，推动该方法向实时编辑场景演进。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/ShaderTransformer_Predicting_Shader_Quality_via_One_shot_Embedding_for_Fast_Simplification.pdf]]