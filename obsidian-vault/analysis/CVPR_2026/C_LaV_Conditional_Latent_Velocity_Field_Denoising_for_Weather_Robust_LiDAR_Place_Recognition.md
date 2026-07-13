---
title: "C-LaV: Conditional Latent Velocity Field Denoising for Weather-Robust LiDAR Place Recognition"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/C_LaV_Conditional_Latent_Velocity_Field_Denoising_for_Weather_Robust_LiDAR_Place_Recognition.pdf
project_link: null
code_link: null
aliases:
- CL
- C-LaV
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在DINOv2编码的语义潜在空间中，通过条件流匹配学习一个从噪声潜在表示到清晰潜在表示的速度场；利用概率流ODE对随机初始化的高斯样本进行确定性传输，将噪声潜在去噪至接近晴朗天气的分布，从而恢复天气鲁棒的检索结构。
primary_logic: 对基于检索的LiDAR地点识别，在语义稳定的潜在空间直接进行条件去噪比在输入空间处理更能保留地点判别性；结合流匹配的确定性传输和SALAD软聚类描述子，进一步提升跨天气的一致性和鉴别力。
claims:
- 在统一基准下，C-LaV在NCLT雪天和Boreas真实数据上分别将Recall@1绝对提升17.5%和21.5%，显著超越现有方法。
- 在KITTI上，C-LaV平均Recall@1达到62.4%，优于MinkLoc3D v2（60.8%）和ImLPR（58.4%）。
- 消融实验表明：用流匹配速度场代替DDPM，KITTI R@1从30.45%提升至50.15%，NCLT从16.80%提升至27.35%；进一步替换为SALAD描述子，KITTI达62.83%，NCLT达34.52%。
- t-SNE可视化显示，去噪后的查询嵌入与晴朗数据库嵌入分布更接近，PR曲线提升明显。
---

# C-LaV: Conditional Latent Velocity Field Denoising for Weather-Robust LiDAR Place Recognition

> [!tip] 核心洞察
> 对基于检索的LiDAR地点识别，在语义稳定的潜在空间直接进行条件去噪比在输入空间处理更能保留地点判别性；结合流匹配的确定性传输和SALAD软聚类描述子，进一步提升跨天气的一致性和鉴别力。

| 字段 | 内容 |
|------|------|
| 中文题名 | C-LaV：面向天气鲁棒LiDAR地点识别的条件潜在速度场去噪 |
| 英文题名 | C-LaV: Conditional Latent Velocity Field Denoising for Weather-Robust LiDAR Place Recognition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Cao_C-LaV_Conditional_Latent_Velocity_Field_Denoising_for_Weather-Robust_LiDAR_Place_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | C-LaV |
| Dataset | KITTI, NCLT, Boreas |

> [!tip] 效果简介
> - KITTI (平均 rain/fog/snow) 上，Recall@1 62.4% vs MinkLoc3D v2: 60.8% (+1.6%)。
> - NCLT (snow) 上，Recall@1 46.41% vs previous best (e.g., MinkLoc3D v2) ~28.91% (approx) (+17.5% absolute)。
> - Boreas (overall adverse, rain+snow) 上，Recall@1 75.82% (average rain/snow) vs previous best (est. ~54.32%) (+21.5% absolute)。

## 概要

LiDAR地点识别是自动驾驶和移动机器人长期定位的关键技术，其目标是根据单帧点云在预先构建的晴天地图数据库中检索最相似的位置。然而，雨、雾、雪等恶劣天气会造成点云的几何畸变和强度衰减，使得传统方法在输入空间（点云或BEV）直接去噪难以保留检索所需的结构信息；若直接在腐蚀的特征空间中学习描述子，嵌入空间又会随天气条件显著偏移，导致跨天气检索性能急剧下降。

针对这一瓶颈，**C-LaV**（Conditional Latent Velocity Field Denoising）提出了一种新的解决范式：**在语义稳定的潜在空间中进行条件去噪，而非在原始输入空间处理**。其核心因果机制可概括为三步——首先将单帧LiDAR点云投影为三通道鸟瞰图（BEV）并由冻结的DINOv2编码器映射到语义潜在空间；随后，通过条件流匹配（Conditional Flow Matching）学习一个从噪声潜在表示到清晰潜在表示的速度场，利用概率流ODE对随机初始化的高斯样本进行确定性传输，将恶劣天气下的噪声潜在逐步“拉回”至接近晴朗天气的分布；最后，由SALAD软聚类描述子头对去噪后的潜在token进行聚合，生成具有强跨天气一致性和地点鉴别力的全局描述子。

该方法在统一基准下取得了显著的性能突破：在NCLT雪天数据上，Recall@1绝对提升**17.5%**；在Boreas真实雨雪数据上，Recall@1绝对提升**21.5%**；即使在相对成熟的KITTI基准上，C-LaV也以**62.4%**的平均Recall@1超越了MinkLoc3D v2（60.8%）和ImLPR（58.4%）等先前最优方法。消融实验进一步验证了设计选择的有效性：将DDPM去噪器替换为流匹配速度场，KITTI平均R@1从30.45%跃升至50.15%；在此基础上将NetVLAD描述子替换为SALAD，R@1进一步提高至62.83%，充分说明流匹配的确定性传输与软聚类聚合之间存在正向协同。

在方法谱系上，C-LaV位于LiDAR地点识别与生成式潜在空间建模的交叉点：它继承了**MinkLoc3D**（Komorowski, WACV 2021）和**BEVPlace**（Luo et al., ICCV 2023）将点云转换为结构化表示进行检索的思路，但通过引入冻结的DINOv2视觉基础模型编码器（与**ImLPR**（Jung et al., CoRL 2025）共享类似动机）获得了语义稳定的潜在空间；其去噪模块以条件流匹配DiT替代传统扩散模型，实现了更高效的确定性传输；描述子层面则用SALAD的Sinkhorn软聚类机制取代了**NetVLAD**（Arandjelovic et al., CVPR 2016）的硬分配，进一步提升了描述子的细粒度鉴别力。



### 问题背景：恶劣天气下的LiDAR地点识别

地点识别是自动驾驶与移动机器人系统的核心能力，其目标是根据当前传感器观测，在预先构建的参考地图中检索最匹配的位置。LiDAR因其对光照变化不敏感的特性，成为地点识别任务的主流传感器。然而，雨、雾、雪等恶劣天气会严重扰乱LiDAR点云的几何结构和强度分布——雨滴和雪花引入虚假反射点，雾气衰减信号导致远距离点缺失，积雪覆盖改变地面几何形态。这些失真使得在晴朗天气下构建的数据库与恶劣天气下的查询之间出现显著的**域差异**，直接导致检索性能崩溃。

### 现有方法的缺口

现有应对恶劣天气的地点识别方法大致可分为两类，但均存在结构性不足：

**输入空间去噪或增强**：部分工作在原始点云或鸟瞰图（BEV）层面进行去噪或天气增强，试图恢复干净的几何输入。然而，输入空间的去噪难以精确保持对检索至关重要的结构信息——过度去噪可能抹除地标细节，不足去噪则残留天气噪声。这种“在输入端修复”的策略缺乏对检索任务本身的针对性优化。

**特征空间学习**：另一类方法直接在腐蚀的特征空间中学习描述子，期望网络能够隐式地学习天气不变性。但恶劣天气会导致嵌入空间产生系统性偏移：同一地点在晴朗与雨雪条件下的特征向量在嵌入空间中形成分离的流形，使得基于距离的检索失效。传统方法缺乏显式机制将噪声嵌入“拉回”到晴朗分布附近。

### 核心动机：在潜在空间进行条件化修复

C-LaV的核心动机源于一个关键洞察：**对基于检索的地点识别而言，在语义稳定的潜在空间直接进行条件化去噪，比在原始输入空间处理更能保留地点判别性**。具体来说：

1. **语义潜在空间天然稳定**：冻结的视觉基础模型（如DINOv2）编码的BEV潜在表示已经具备一定的语义鲁棒性，天气噪声在此空间中表现为可控的扰动，而非毁灭性的结构破坏。
2. **条件流匹配提供确定性传输**：与扩散模型的随机采样不同，条件流匹配学习一个从噪声潜在到干净潜在的速度场，通过概率流ODE实现**确定性传输**。这意味着给定相同的噪声输入，去噪结果是确定的，这对地点识别的一致性至关重要。
3. **检索导向的优化**：将去噪模块与SALAD软聚类描述子联合优化，使得整个流水线以检索性能为最终目标，而非单纯追求重建质量。

### 目标与贡献

基于上述动机，C-LaV的目标是构建一个统一的框架，将BEV投影、冻结的语义编码器、条件流匹配去噪器和可学习的描述子聚合头串联起来，实现跨天气的鲁棒LiDAR地点识别。该方法在NCLT雪天场景上将Recall@1绝对提升17.5%，在Boreas真实数据上提升21.5%（见**Figure 1**雷达图），验证了“潜在空间条件化修复”策略的有效性。



## 核心方法与创新机理

C-LaV 的核心创新在于将恶劣天气下的 LiDAR 地点识别问题重新定义为**语义稳定潜在空间中的条件传输问题**，而非传统的输入空间去噪或特征空间直接适配。其关键 changed slots 体现在三个层面：

### 1. 编码器：从 3D 稀疏卷积到冻结的 DINOv2 语义潜在空间

传统方法如 **MinkLoc3D**（Komorowski, WACV 2021）和 **MinkLoc3D v2**（Komorowski, ICPR 2022）直接在 3D 点云上使用稀疏卷积提取几何特征，**BEVPlace**（Luo et al., ICCV 2023）则将点云投影为 BEV 后用 2D CNN 编码。这些编码器在恶劣天气下易受点云几何和强度失真的影响，导致嵌入空间偏移。

C-LaV 将单帧点云投影为三通道 BEV 图像（高度、强度、密度），并采用**冻结的 DINOv2-B ViT/14** 作为编码器：

$$
Z_0 = E(\mathbf{I}) \in \mathbb{R}^{C \times H_\ell \times W_\ell}
$$

冻结的 DINOv2 提供了语义稳定、对局部几何扰动不敏感的潜在表示，这是后续去噪能够保持地点判别性的前提。消融实验（Table 3）表明，仅替换编码器即可带来显著增益。

### 2. 潜在去噪：从 DDPM 随机扩散到条件流匹配确定性传输

这是 C-LaV 最关键的创新 slot。传统去噪思路（如消融中的 DDPM baseline）在潜在空间进行随机扩散-去噪，缺乏对“向晴朗天气分布传输”的显式建模。

C-LaV 引入**条件流匹配（Conditional Flow Matching）**，学习一个条件速度场 $\mathcal{F}_\theta(z_t, t, Z_{\text{noisy}})$，其训练损失为：

$$
\mathcal{L}_{\text{CFM}} = \mathbb{E}_{z_0,z_1,t}\left[\Vert \mathcal{F}_\theta(z_t,t,Z_{\text{noisy}}) - v_t(z_t|z_1) \Vert_2^2\right]
$$

推理时通过**概率流 ODE** 进行确定性传输：

$$
\frac{dz_t}{dt} = \mathcal{F}_\theta(z_t, t, Z_{\text{noisy}}), \quad t\in[0,1]
$$

采用 Euler 积分（约 50 步）将随机高斯噪声 $z_{t_0}$ 逐步传输至去噪潜在 $Z_d$：

$$
z_{t_{k+1}} = z_{t_k} + \Delta t \, \mathcal{F}_\theta(z_{t_k}, t_k, Z_{\text{noisy}})
$$

**因果机制**：流匹配学习的是从噪声潜在到干净潜在的最优传输方向，ODE 的确定性保证了去噪过程的稳定性和可复现性。消融实验（Table 3）验证了这一创新的决定性作用：将 DDPM 替换为流匹配速度场后，KITTI 平均 R@1 从 30.45% 跃升至 50.15%（+19.7%），NCLT 从 16.80% 提升至 27.35%（+10.55%）。

### 3. 描述子聚合：从 NetVLAD 硬聚类到 SALAD 软聚类

传统 **NetVLAD**（Arandjelovic et al., CVPR 2016）使用硬分配的聚类方式聚合局部特征。C-LaV 采用 **SALAD** 描述子头，通过 Sinkhorn 软聚类实现更精细的特征聚合：

$$
a_{ik} = \frac{\exp(f_i^\top w_k / \tau_a)}{\sum_{k'}\exp(f_i^\top w_{k'} / \tau_a)}
$$

$$
u_k = \sum_i a_{ik} f_i \in \mathbb{R}^{d_c}
$$

最终描述子由全局注意力 token 与 64 个簇描述子拼接而成，维度为 $256 + 64 \times 128 = 8448$。在流匹配去噪基础上，用 SALAD 替换 NetVLAD 使 KITTI R@1 进一步提高至 62.83%（+12.68%），NCLT 提高至 34.52%（+7.17%）。

### 创新总结

三个 changed slots 的协同效应构成了 C-LaV 的核心优势：DINOv2 提供语义稳定的潜在空间，流匹配 ODE 在该空间中执行确定性的天气去噪传输，SALAD 软聚类则最大化去噪后特征的鉴别力。t-SNE 可视化（Figure 6）直观展示了去噪后查询嵌入与晴朗数据库嵌入分布的显著接近，PR 曲线亦大幅提升。



C-LaV 的完整流水线将单帧 LiDAR 点云映射为一个紧凑的全局描述子，用于跨天气地点检索。整个映射过程由四个顺序模块组成：

$$
\mathbf{D} = \Omega(\mathcal{P}), \quad \Omega = h \circ \psi \circ E \circ \phi
$$

其中 $\phi$ 为 BEV 投影，$E$ 为冻结的 DINOv2 编码器，$\psi$ 为条件流匹配去噪器，$h$ 为 SALAD 描述子聚合头。该流水线的核心设计理念是：**在语义稳定的潜在空间中进行条件去噪**，而非直接在输入点云或 BEV 图像上处理天气失真。

### 模块间数据流

1. **BEV 投影**（$\phi$）：将原始点云 $\mathcal{P} = \{ (x_n, y_n, z_n, i_n) \}_{n=1}^N$ 栅格化为三通道 BEV 图像 $\mathbf{I} \in \mathbb{R}^{H \times W \times 3}$，三个通道分别编码高度、反射强度和点密度。该步骤将稀疏无序的点云转化为规整的 2D 表示，为后续视觉基础模型编码奠定基础。

2. **DINOv2 编码器**（$E$）：冻结的 DINOv2-Base (ViT/14) 将 BEV 图像编码为语义稳定的潜在特征网格 $Z_0 \in \mathbb{R}^{C \times H_\ell \times W_\ell}$（$C=768$, $H_\ell=W_\ell=32$）。编码器参数完全冻结，确保语义空间的稳定性不受天气影响。

3. **条件流匹配去噪器**（$\psi$）：以含天气噪声的潜在表示 $Z_{\text{noisy}}$ 为条件，通过训练好的速度场 $\mathcal{F}_\theta$ 和概率流 ODE 求解器，将随机高斯噪声 $z_{t_0} \sim \mathcal{N}(0, I)$ 确定性传输为去噪后的潜在 $Z_d$。该模块是 C-LaV 的核心创新——**用流匹配替代传统 DDPM**，实现更高效、更稳定的潜在空间去噪。

4. **SALAD 描述子头**（$h$）：对去噪后的空间 token 进行 Sinkhorn 软聚类，结合全局上下文 token，输出 8448 维最终描述子 $\mathbf{D}$：
   $$
   \mathrm{dim}(\mathbf{D}) = d_g + K d_c = 256 + 64 \times 128 = 8448
   $$

### 训练与推理流程

训练阶段（Figure 3 左支）需要成对的晴朗天气和恶劣天气 BEV 图像。从晴朗 BEV 编码得到的真实潜在分布 $q(z_1)$ 中采样目标 $z_1$，利用最优传输路径构造训练信号，通过条件流匹配损失 $\mathcal{L}_{\text{CFM}}$ 学习速度场 $\mathcal{F}_\theta$。联合优化目标包含去噪损失、截断 Smooth-AP 检索损失以及可选的潜在一致性正则项。

推理阶段（Figure 3 右支）仅需单帧恶劣天气点云。从高斯噪声 $z_{t_0}$ 出发，通过 Euler 积分（约 50 步）沿学习到的速度场逐步生成去噪潜在 $z_{t_n}$：

$$
z_{t_{k+1}} = z_{t_k} + \Delta t \, \mathcal{F}_\theta(z_{t_k}, t_k, Z_{\text{noisy}}), \quad \Delta t = \frac{1}{T}
$$

去噪后的潜在经 SALAD 头聚合为描述子，与晴朗天气数据库描述子进行最近邻检索，完成地点识别。Figure 2 完整展示了这一三阶段架构：编码→潜在去噪→描述子聚合。

![[assets/figures/papers/paper_list_l843_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_C_LaV_Conditional/figures/002_Figure_2.jpg]]
*Figure 2: Notes: OT CVF: Optimal Transport Conditional Velocity Field, only for training; ODE: Ordinary Differential Equation Solver. Figure 2. Overview of the proposed C-LaV architecture. The framework consists of three sequential stages: (1) a frozen DINOv2 encoder that transforms BEV images into semantic latent tokens; (2) a conditional diffusion transformer (ConditionalDiT) trained via flow-matching to denoise latent features under adverse weather; and (3) a SALAD descriptor head that aggregates denoised latent tokens into a global descriptor using Sinkhorn-based soft clustering. This unified pipeline enables robust cross-weather place recognition from BEV LiDAR representations*

> **注意**：Figure 3 为训练/推理流程示意图，Figure 2 为整体架构总览，两图互补说明流水线的模块关系与数据流向。



C-LaV 将单帧 LiDAR 点云到地点描述子的映射分解为四个顺序模块：BEV 投影、DINOv2 编码器、条件流匹配去噪器、SALAD 描述子头。整体流水线形式化为：

$$\mathbf{D} = \Omega(\mathcal{P}), \quad \Omega = h \circ \psi \circ E \circ \phi \tag{1}$$

其中 $\mathcal{P}$ 为输入点云，$\mathbf{D}$ 为输出描述子，$\phi, E, \psi, h$ 分别对应四个模块。

### BEV 投影

将 $N$ 个点的 LiDAR 扫描 $\mathcal{P} = \{(\mathbf{p}_n)\}_{n=1}^{N}$（每点含坐标 $x_n, y_n, z_n$ 与强度 $i_n$）栅格化为固定尺寸的鸟瞰图：

$$\mathbf{I} = \phi(\mathcal{P}) \in \mathbb{R}^{H \times W \times 3} \tag{2}$$

三个通道分别编码高度（最大 $z$）、反射强度（平均强度）、点密度（归一化点数）。该 BEV 图像作为后续冻结编码器的输入。

### DINOv2 编码器

采用冻结的 DINOv2-Base (ViT/14) 将 BEV 图像编码为语义稳定的潜在特征网格：

$$Z_0 = E(\mathbf{I}) \in \mathbb{R}^{C \times H_\ell \times W_\ell} \tag{3}$$

输出维度为 $768 \times 32 \times 32$，所有编码器参数在训练中保持冻结，确保潜在空间不受天气退化影响而发生分布偏移。

### 条件流匹配去噪器

去噪阶段的核心是学习一个条件速度场 $\mathcal{F}_\theta$，该速度场以噪声潜在 $Z_{\text{noisy}}$ 为条件，预测从当前噪声状态 $z_t$ 向干净潜在 $z_1$ 的传输方向。训练时，从干净潜在分布 $q(z_1)$ 采样目标，沿最优传输路径构造训练信号：

$$\mathcal{L}_{\text{CFM}} = \mathbb{E}_{z_0, z_1, t}\left[\left\| \mathcal{F}_\theta(z_t, t, Z_{\text{noisy}}) - v_t(z_t \mid z_1) \right\|_2^2\right] \tag{11}$$

其中 $v_t(z_t \mid z_1)$ 为条件真值速度。推理时，利用概率流 ODE 从随机高斯噪声 $z_{t_0}$ 出发，通过 Euler 积分迭代生成去噪潜在 $z_{t_n}$：

$$\frac{dz_t}{dt} = \mathcal{F}_\theta(z_t, t, Z_{\text{noisy}}), \quad t \in [0, 1] \tag{12}$$

$$z_{t_{k+1}} = z_{t_k} + \Delta t \, \mathcal{F}_\theta(z_{t_k}, t_k, Z_{\text{noisy}}), \quad \Delta t = \frac{1}{T} \tag{14}$$

其中 $T \approx 50$ 步。速度场由 ConditionalDiT（条件扩散 Transformer）参数化，训练时以噪声 BEV 的潜在 $Z_{\text{noisy}}$ 作为条件输入，引导去噪方向指向晴朗天气下的潜在分布。

### SALAD 描述子聚合

去噪后的潜在 token $\{f_i\}$ 通过 Sinkhorn 软聚类聚合为紧凑的全局描述子。维护 $K = 64$ 个可学习簇原型 $\{w_k\}$ 和一个全局上下文 token $g \in \mathbb{R}^{256}$。空间 token $i$ 对原型 $k$ 的软分配为：

$$a_{ik} = \frac{\exp(f_i^\top w_k / \tau_a)}{\sum_{k'} \exp(f_i^\top w_{k'} / \tau_a)} \tag{15}$$

簇 $k$ 的聚合特征为 token 的加权平均：

$$u_k = \sum_i a_{ik} f_i \in \mathbb{R}^{d_c} \tag{16}$$

最终描述子由全局注意力 token 与所有簇描述子拼接得到：

$$\mathbf{D} = [g_{\text{att}}; u_1; \dots; u_K] \in \mathbb{R}^{8448} \tag{18}$$

其中 $d_g = 256$，$d_c = 128$，总维度 $256 + 64 \times 128 = 8448$。

### 联合训练损失

总损失联合优化去噪质量与检索性能：

$$\mathcal{L} = \mathcal{L}_{\text{denoise}} + \lambda_{\text{desc}} \mathcal{L}_{\text{TSAP}} + \lambda_{\text{lat}} \|Z_{\text{noisy}} - Z_{\text{clean}}\|_2^2$$

其中 $\mathcal{L}_{\text{denoise}}$ 为流匹配损失（式 11），$\mathcal{L}_{\text{TSAP}}$ 为截断 Smooth-AP 检索损失，第三项为可选的潜在一致性正则项（约束去噪潜在与干净潜在的距离）。

**关键设计决策**：将去噪操作置于冻结 DINOv2 的语义潜在空间而非原始点云或 BEV 输入空间，是 C-LaV 与现有去噪方法的本质区别。消融实验（Table 3）表明，仅将 DDPM 替换为流匹配速度场，KITTI 平均 R@1 即从 30.45% 跃升至 50.15%，NCLT 从 16.80% 提升至 27.35%；进一步替换 SALAD 描述子后，KITTI 达 62.83%，NCLT 达 34.52%，验证了各模块的独立贡献。

### 补充图表

![[assets/figures/papers/paper_list_l843_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_C_LaV_Conditional/figures/003_Figure_3.jpg]]
*Figure 3: Training and inference pipeline of conditional Flow Matching (CFM). Training: Sample*

![[assets/figures/papers/paper_list_l843_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_C_LaV_Conditional/figures/005_Figure_5.jpg]]
*Figure 5: Three-channel BEV construction and pairing. From a clear-weather point cloud (top-left) and an adverse-weather BEV (bottom-left, fog), we derive three channels—Height, Intensity, and Density—and form a three-channel BEV for each condition*



## 实验与关键发现

### 数据集与评估协议

C-LaV 在三个公开 LiDAR 地点识别数据集上进行评估：**KITTI**、**NCLT** 和 **Boreas**。所有数据集均采用统一的预处理与评估协议：原始轨迹以 3 m 间距重采样，正样本定义为地理距离小于 10 m 的帧对，负样本为距离大于 50 m 的帧对。训练与测试轨迹按地理区域严格划分（见原文 Figure 4），避免信息泄露。Table 1 汇总了各数据集在不同天气条件下的 BEV 帧数及地点识别（PR）与去噪配对（DN）的样本量。Boreas 数据集缺少雾天数据，仅在雨和雪条件下评估。

![[assets/figures/papers/paper_list_l843_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_C_LaV_Conditional/figures/006_Table_1.jpg]]
*Table 1: Dataset summary with weather-wise counts and split policy. All sets use 3 m spacing; positives are below 10 m, and negatives are above 50 m. PR = place recognition tuples; DN = denoising pairs*

![[assets/figures/papers/paper_list_l843_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_C_LaV_Conditional/figures/004_Figure_4.jpg]]
*Figure 4: Train/test splits on (a) KITTI, (b) NCLT, and (c) Boreas. Red trajectories indicate the test set, and the remaining trajectories are used for training*

### 主要结果：跨天气地点识别性能

Table 2 报告了 C-LaV 与现有方法在 Recall@1 / Recall@5 指标上的全面比较。C-LaV 在所有三个数据集的绝大多数天气条件下均取得最优或接近最优的结果：

![[assets/figures/papers/paper_list_l843_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_C_LaV_Conditional/figures/007_Table_2.jpg]]
*Table 2: Recall@1 / Recall@5 (%) performance across three datasets. Note that there are no foggy-weather runs in the Boreas dataset*

- **KITTI 数据集**：C-LaV 在雨、雾、雪三种天气下的平均 Recall@1 达到 **62.4%**，超越 **MinkLoc3D v2**（Komorowski, ICPR 2022）的 60.8% 和 **ImLPR**（Jung et al., CoRL 2025）的 58.4%。其中，雨天场景 Recall@1 为 46.97%，较 BEVPlace 的约 37.08% 提升超过 9.9 个百分点；雪天场景达到 77.60%，体现了对强几何失真场景的优异鲁棒性。
- **NCLT 数据集**：在真实雪天条件下，C-LaV 的 Recall@1 达到 **46.41%**，相比此前最优方法（约 28.91%）**绝对提升 17.5 个百分点**。雨天和雾天场景同样全面领先，Recall@1 分别达到 29.49% 和 28.87%。
- **Boreas 数据集**：在真实雨雪条件下，C-LaV 的平均 Recall@1 达到 **75.82%**，平均 Recall@5 达到 96.57%，**绝对提升 21.5 个百分点**（原文 Abstract 及 Section 4.2）。雨天场景 Recall@1 高达 79.66%，雪天为 71.98%，展现出对真实恶劣天气的强泛化能力。

值得注意的是，C-LaV 在晴天基准上同样具有竞争力，表明潜在空间去噪并未损害正常天气下的检索性能。

### 消融实验：关键设计选择的影响

Table 3 系统拆解了编码器、潜在去噪模块和描述子聚合三个核心组件的贡献（以 KITTI 和 NCLT 的平均 Recall@1 为指标）：

![[assets/figures/papers/paper_list_l843_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_C_LaV_Conditional/figures/009_Table_3.jpg]]
*Table 3: Ablation (B): Encoder, latent denoising, and descriptor choices vs. dataset averages (KITTI / NCLT)*

1. **去噪模块：DDPM → 流匹配速度场**  
   将 DDPM 去噪器替换为条件流匹配（Conditional Flow Matching）学习的潜在速度场后，KITTI 平均 Recall@1 从 30.45% **跃升至 50.15%**（+19.70%），NCLT 从 16.80% 提升至 27.35%（+10.55%）。这一巨大增益表明，基于概率流 ODE 的确定性传输比 DDPM 的随机采样更有效地恢复了天气鲁棒的检索结构，其核心机制在于速度场直接建模最优传输方向，避免了随机扩散带来的信息损失。

2. **描述子聚合：NetVLAD → SALAD**  
   在流匹配去噪的基础上，将 NetVLAD 替换为 SALAD（Sinkhorn 软聚类 + 全局上下文 token）后，KITTI 平均 Recall@1 进一步提高至 **62.83%**（+12.68%），NCLT 提高至 34.52%（+7.17%）。SALAD 通过 64 个可学习簇原型对去噪后的潜在 token 进行软分配，保留了更丰富的空间结构信息，最终输出 8448 维描述子（256 维全局 token + 64×128 维簇描述子），显著增强了跨天气的描述子鉴别力。

3. **编码器选择**：冻结的 DINOv2-B ViT/14 编码器提供了语义稳定的潜在表示基础。消融显示，仅使用该编码器配合基础聚合（无去噪），KITTI 平均 Recall@1 约为 30.45%，说明语义潜在空间本身已具备一定鲁棒性，但缺少去噪模块时性能严重不足。

### 可视化分析：潜在去噪的定性证据

原文 Figure 6 提供了精度-召回曲线和 t-SNE 联合嵌入可视化。t-SNE 图（经 PCA 预降维）将噪声查询嵌入、去噪后查询嵌入与晴朗天气数据库嵌入共同投影：去噪前，噪声查询嵌入与数据库嵌入分布明显分离；去噪后，查询嵌入的分布显著向数据库嵌入靠拢，印证了条件流匹配去噪有效恢复了语义一致的潜在表示。精度-召回曲线进一步量化了这一改善——去噪后的 PR 曲线在所有召回率水平上均高于去噪前，尤其在低假阳性区域提升显著。

![[assets/figures/papers/paper_list_l843_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_C_LaV_Conditional/figures/008_Figure_6.jpg]]
*Figure 6: Precision–Recall curves (left) and joint t-SNE visualizations (right) of C-LaV before and after latent denoising. All t-SNE plots use a single joint embedding of noisy queries, denoised queries, and database descriptors with PCA pre-reduction*

### 失败模式与局限性

尽管 C-LaV 取得了显著的性能提升，仍存在以下局限：

1. **训练数据依赖**：条件流匹配的训练需要成对的“无噪-有噪”BEV 数据，在真实场景中获取严格配对的跨天气数据成本较高。当前实验依赖模拟天气增强（KITTI、NCLT）或自然跨天气配对（Boreas），对完全无配对数据的场景泛化能力未经验证。
2. **推理效率**：ODE 求解器需要约 50 步 Euler 积分才能完成去噪，单帧推理耗时较高，难以满足自动驾驶等实时应用需求。能否通过蒸馏或更高效的 ODE 求解器将步数压缩至 10 步以内，是实际部署的关键挑战。
3. **极端天气泛化**：当前评估仅限于雨、雾、雪三种天气，对暴雪、强降雨、沙尘暴等更极端的点云退化场景的鲁棒性尚未测试。
4. **BEV 分辨率限制**：BEV 投影固定为 448×448 分辨率，对远距离或小尺寸物体的表示能力可能不足，潜在影响长距离地点识别的精度。

### 补充图表

![[assets/figures/papers/paper_list_l843_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_C_LaV_Conditional/figures/001_Figure_1.jpg]]
*Figure 1: (Left) Given LiDAR point clouds in adverse weather, our C-LaV encodes them into a weather-stable latent space to retrieve the nearest position from geo-tagged LiDAR sequences in sunny weather. (Right) The radar plot reports Recall@1 on KITTI, NCLT, and Boreas datasets under rain, fog, and snow weather, where C-LaV outperforms prior LiDAR place recognition methods*



## 定位与知识库关联

### 1. 与现有基线的关系

C-LaV 处于**基于检索的LiDAR地点识别**这一主线，其核心改进针对的是该领域长期存在的瓶颈——恶劣天气（雨/雾/雪）导致的点云几何与强度失真。传统方法可大致归为三类，C-LaV 对每一类都做出了关键性的路径切换。

**（1）相对于基于稀疏卷积的方法**

以 **MinkLoc3D**（Komorowski, WACV 2021）及其改进版 **MinkLoc3D v2**（Komorowski, ICPR 2022）为代表，这类方法直接在3D稀疏体素上学习描述子，对晴朗天气表现优异，但对点云密度和强度分布的变化高度敏感。在KITTI跨天气基准上，MinkLoc3D v2 的平均 Recall@1 为 60.8%，而 C-LaV 达到 62.4%（Table 2）。差距虽看似不大，但在NCLT雪天场景中，C-LaV 将 Recall@1 从约 28.9% 提升至 46.41%，绝对提升达 17.5%——这表明稀疏卷积对雪天造成的点缺失和强度漂移缺乏内在鲁棒性，而C-LaV通过语义潜在空间的去噪从根本上绕过了这一问题。

**（2）相对于基于BEV投影的方法**

**BEVPlace**（Luo et al., ICCV 2023）将点云投影为BEV图像后使用2D CNN编码，在KITTI雨天场景下 Recall@1 约为 37.08%，而 C-LaV 达到 46.97%（Table 2）。BEVPlace 的瓶颈在于其在输入空间（BEV像素）直接处理天气退化，缺乏对语义结构的显式保护。C-LaV 同样使用BEV作为输入表示，但将其通过冻结的 DINOv2-B 编码器映射到语义稳定的潜在空间后再进行去噪，这使得去噪操作不会破坏地点判别所需的结构信息。

**（3）相对于基于视觉基础模型的方法**

**ImLPR**（Jung et al., CoRL 2025）同样利用 DINOv2 进行图像到LiDAR的地点识别，在KITTI上 Recall@1 为 58.4%（Table 2）。C-LaV 在此基础上增加了条件流匹配去噪和SALAD软聚类描述子两个模块，使 Recall@1 提升至 62.4%。消融实验（Table 3）揭示了这两个模块各自的贡献：在DINOv2编码器 + NetVLAD描述子的基础上，仅将DDPM去噪替换为流匹配速度场，KITTI平均R@1即从30.45%跃升至50.15%（+19.7%）；进一步将NetVLAD替换为SALAD，R@1再提升至62.83%（+12.68%）。这表明**流匹配的确定性传输是性能提升的主要因果杠杆**，而SALAD的软聚类机制进一步增强了描述子的鉴别力。

### 2. 适用边界与局限

**（1）数据依赖**

C-LaV 的训练依赖成对的晴朗天气BEV与恶劣天气BEV作为去噪监督信号。在真实场景中，精确配对的跨天气数据获取困难，这限制了该方法向新环境的快速迁移。论文未探索无监督或自监督的替代方案。

**（2）推理效率**

推理阶段，ODE求解器需要约 $T \approx 50$ 步Euler积分来完成从随机噪声到去噪潜在的传输。这使单帧推理时间显著长于纯前馈方法（如MinkLoc3D），限制了在实时SLAM系统中的应用。论文未讨论蒸馏或更高效的ODE求解策略。

**（3）天气覆盖范围**

实验覆盖了雨、雾、雪三种天气，但Boreas数据集缺少雾天数据（Table 2注释）。对于更极端的天气现象（如暴雪导致的全遮挡、强降雨导致的严重衰减、沙尘暴、烟雾），C-LaV的泛化能力未经验证。BEV投影的固定分辨率（$448 \times 448$）在远距离物体或极端稀疏点云下可能存在信息瓶颈。

**（4）模态限制**

C-LaV 仅在LiDAR单一模态下测试。在LiDAR完全失效的场景（如浓雾中激光被完全吸收），该方法缺乏来自相机或雷达的补充信息。

### 3. 开放问题

1. **推理加速**：能否通过蒸馏或更高效的ODE求解器（如DPM-Solver）将推理步数压缩至10步以内，使C-LaV满足实时部署需求？
2. **无配对训练**：能否利用无监督域适应或自监督预训练摆脱对配对晴朗/恶劣天气BEV数据的依赖？
3. **极端天气泛化**：当前的条件流匹配去噪框架能否直接扩展到烟雾、沙尘暴等更复杂的散射介质，还是需要重新设计条件信号？
4. **多模态融合**：在LiDAR严重退化的场景下，融合相机语义信息或雷达回波强度是否能为潜在去噪提供更强的条件引导？
5. **动态物体处理**：BEV投影将动态物体（车辆、行人）的痕迹固化为静态栅格，这些“幽灵痕迹”在跨天气检索中是否被DINOv2的语义先验自动抑制，还是需要显式的动态掩膜？



## 原文 PDF

![[paperPDFs/CVPR_2026/C_LaV_Conditional_Latent_Velocity_Field_Denoising_for_Weather_Robust_LiDAR_Place_Recognition.pdf]]
