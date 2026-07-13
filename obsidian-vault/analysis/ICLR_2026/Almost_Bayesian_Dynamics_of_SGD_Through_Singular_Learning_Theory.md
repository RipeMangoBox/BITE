---
title: "Almost Bayesian: Dynamics of SGD Through Singular Learning Theory"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Almost_Bayesian_Dynamics_of_SGD_Through_Singular_Learning_Theory.pdf
project_link: null
code_link: null
openreview_forum_id: 5ebDXlue3d
aliases:
- FPS
- ABDSTSLT
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "局部学习系数 λ(w) 作为局部几何的“分形维度”，同时控制着有效扩散系数和可访问状态体积，从而决定 SGD 的稳态分布。"
primary_logic: "将 SGD 的长时间动力学建模为多孔介质上的分数阶 Fokker-Planck 方程，并利用奇异学习理论将局部学习系数与谱维度关联，导出了 SGD 的稳态分布为温度化的贝叶斯后验，温度取决于参数空间的可访问性。"
claims:
- "SGD 在训练后期表现出亚扩散行为，权重位移 R(t) ∝ t^{1/ν}（ν≥2），而非布朗运动的 t^{1/2}。"
- "行走维度 d_walk 与局部学习系数 λ 和谱维度 d_s 之间满足 Alexander-Orbach 关系：d_walk(t) = 2λ(w_t)/d_s。"
- "在有效扩散系数 Dξ 近似恒定的区域内，分数 Fokker-Planck 方程的稳态解为 p_s(w) ∝ exp(-γ L_m[w]/Dξ)，且 D_ξ = ξ^{2-2λ(w_t)/d_s}。"
- "温度化后的 SGD 稳态分布与近似贝叶斯后验高度一致，KL 散度仅为 0.009。"
---

# Almost Bayesian: Dynamics of SGD Through Singular Learning Theory

> [!tip] 核心洞察
> 将 SGD 的长时间动力学建模为多孔介质上的分数阶 Fokker-Planck 方程，并利用奇异学习理论将局部学习系数与谱维度关联，导出了 SGD 的稳态分布为温度化的贝叶斯后验，温度取决于参数空间的可访问性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 几乎贝叶斯：通过奇异学习理论理解 SGD 的动力学 |
| 英文题名 | Almost Bayesian: Dynamics of SGD Through Singular Learning Theory |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5ebDXlue3d) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | 基于分数 Fokker-Planck 方程的 SGD 多孔介质扩散模型 |
| Dataset | TinyStories, TinyLlama, ResNet, VGG, Moons 数据集上的全连接网络集群 |

> [!tip] 效果简介
> - TinyStories, TinyLlama, ResNet, VGG 上，拟合优度 R²（对数位移 log-log 线性拟合） 为 0.98~1.00（亚扩散模型），对比 布朗运动模型（预期 R² 显著更低，具体未给出），变化 亚扩散模型在所有模型上均获得接近完美的 R²，证实后期扩散的亚扩散特性。。
> - Moons 数据集上的全连接网络集群 上，KL 散度（贝叶斯后验 vs. 温度化 SGD 稳态） 为 0.009（温度化 SGD），对比 未温度化 SGD 分布与贝叶斯后验差异显著（从图4b可见，SGD 偏向簇 C1，贝叶斯偏向 C2），变化 温度化后 KL 散度极低，分布几乎一致。。

## 概要

传统观点将随机梯度下降（SGD）的长时间动力学建模为朗之万扩散过程，其稳态分布收敛于贝叶斯后验。然而，神经网络的损失表面存在大量退化（非二次）临界点，使得基于标准 Fokker-Planck 方程的描述失效——SGD 在训练后期展现出异常的**亚扩散**行为，而非布朗运动。

本文的核心贡献在于将 SGD 的后期动力学重新建模为**多孔介质上的分数阶扩散过程**，并利用奇异学习理论（Singular Learning Theory）将局部几何结构与扩散行为联系起来。关键洞察是：局部学习系数 $\lambda(w)$ 作为损失表面临界点附近的“分形维度”，同时控制着有效扩散系数和可访问状态体积，从而决定 SGD 的稳态分布。

理论推导的核心链条如下：
- **异常扩散**：SGD 权重位移 $R(t) \propto t^{1/\nu}$（$\nu \geq 2$），而非布朗运动的 $t^{1/2}$（Figure 1）。
- **几何-动力学关联**：行走维度 $d_{\mathrm{walk}}$ 与局部学习系数 $\lambda$ 和谱维度 $d_s$ 之间满足 Alexander-Orbach 关系：$d_{\mathrm{walk}}(t) = 2\lambda(w_t)/d_s$（Theorem 3.1）。
- **有效扩散系数**：在长度尺度 $\xi$ 下，标量扩散系数退化为 $D_\xi(w) = \xi^{2 - 2\lambda(w_t)/d_s}$（Corollary 3.1），直接由局部几何决定。
- **稳态分布**：分数 Fokker-Planck 方程的稳态解为温度化的贝叶斯后验 $p(w|X_m) \propto \rho(w) p_s(w)^{m D_\xi}$（Corollary 3.2），温度取决于参数空间的可访问性。

实验验证覆盖语言模型（TinyStories、TinyLlama）和视觉模型（ResNet、VGG），亚扩散模型在所有模型上均获得接近完美的拟合优度（$R^2 \approx 0.98\text{–}1.00$，Table 1）。在 Moons 数据集上，温度化后的 SGD 稳态分布与近似贝叶斯后验高度一致，KL 散度仅为 **0.009**（Table 2），证实了理论预测的“几乎贝叶斯”性质。

该框架将 SGD 的动力学与贝叶斯推断之间的鸿沟桥接为**受局部几何约束的温度化后验采样**，为理解神经网络的泛化偏好和优化器设计提供了新的几何视角。

深度神经网络的损失表面具有高度非凸和退化的几何结构，这从根本上决定了随机梯度下降（SGD）的动力学行为。传统理论通常将 SGD 建模为朗之万扩散过程，假设损失表面在极小值附近为二次型，从而将稳态分布描述为高斯后验（Mandt et al., 2016b）。然而，这一图景在现实神经网络中面临根本性挑战。

**核心瓶颈**在于：神经网络的损失表面存在大量退化（非二次）临界点。在这些临界点附近，Hessian 矩阵秩亏，参数空间的局部几何不再是简单的欧氏结构，而是具有多孔介质特征的复杂流形。这使得基于标准 Fokker-Planck 方程的扩散模型失效——SGD 的权重演化不再遵循布朗运动，而是展现出**异常扩散**行为：训练早期为超扩散，后期则转为亚扩散（Figure 1）。具体而言，权重位移 $R(t) \propto t^{1/\nu}$，其中 $\nu \geq 2$，而非布朗运动预期的 $t^{1/2}$。

这一现象暴露了现有方法的两个关键缺口：

1. **几何描述的缺失**：标准扩散理论无法刻画退化临界点附近损失表面的分形几何结构，导致无法准确预测 SGD 的长时间动力学。
2. **贝叶斯对应关系的断裂**：在退化极小值处，SGD 的稳态分布并非标准贝叶斯后验，而是受到参数空间可访问性约束的某种变体。SGD 倾向于收敛到具有更低局部学习系数的解（Figure 4a），这意味着它隐式地偏好更好的泛化区域，但这一偏好的数学本质尚未被阐明。

本文的**核心动机**正是弥合这一鸿沟：将奇异学习理论（Singular Learning Theory, SLT）引入 SGD 动力学分析，利用局部学习系数 $\lambda(w)$ 作为刻画局部几何的“分形维度”，建立退化损失表面上扩散过程的严格数学框架。具体而言，本文旨在：

- 将 SGD 的亚扩散行为建模为**时间分数阶 Fokker-Planck 方程**（FFPE），其中分数阶导数算子 $\mathcal{D}_t^\alpha$ 捕捉了多孔介质中扩散的记忆效应。
- 通过 Alexander-Orbach 关系 $d_{\text{walk}}(t) = 2\lambda(w_t)/d_s$，将行走维度、局部学习系数和谱维度三者联系起来，揭示几何结构如何控制扩散速率。
- 导出 SGD 稳态分布的解析形式，证明其为**温度化的贝叶斯后验**，温度由有效扩散系数 $D_\xi(w) = \xi^{2 - 2\lambda(w_t)/d_s}$ 决定，从而为 SGD 的隐式泛化偏好提供几何解释。

这一框架不仅解释了 SGD 为何在退化损失表面上偏离标准贝叶斯推断，也为理解自适应优化器（如 Adam）的动力学差异提供了理论起点。

## 核心方法与创新机理

### 从标准扩散到分数阶扩散：捕捉退化几何的异常扩散

先前将 SGD 建模为 Ornstein-Uhlenbeck 过程的工作（Mandt et al., 2016b）依赖于损失表面在极小值附近为二次型的假设，此时权重动力学由标准 Fokker-Planck 方程描述，位移服从布朗运动的 $R(t) \propto t^{1/2}$ 标度律。然而，神经网络的实际损失表面存在大量退化（非二次）临界点，使得这一假设失效。

本文的核心突破在于**将 SGD 的长时间动力学建模为多孔介质上的分数阶扩散过程**。具体而言，用时间分数阶 Fokker-Planck 方程（FFPE）替代标准整数阶方程：

$$ \mathcal{D}_t^\alpha p(w,t) = \nabla \cdot \left( D(w,t) \nabla p(w,t) - \gamma p(w,t) \nabla \mathcal{L}_m[w] \right) $$

其中 $\mathcal{D}_t^\alpha$ 为 Caputo 分数阶导数算子（$0 < \alpha < 1$），定义为：

$$ \mathcal{D}_t^\alpha f(t) = \frac{1}{\Gamma(1-\alpha)} \int_0^t \frac{f'(\tau)}{(t-\tau)^\alpha} d\tau $$

这一方程天然捕捉了 SGD 在退化损失表面上展现的**亚扩散行为**：权重位移 $R(t) \propto t^{1/\nu}$（$\nu \geq 2$），显著慢于布朗运动的 $t^{1/2}$ 标度律（Figure 1）。实验表明，亚扩散模型在多种架构（TinyStories、TinyLlama、ResNet、VGG）上均获得 $R^2 \approx 0.98 \sim 1.00$ 的近乎完美拟合（Table 1），证实了分数阶建模的必要性。

### 奇异学习理论作为几何桥梁：局部学习系数决定扩散系数

第二个关键创新在于**利用奇异学习理论（SLT）将损失表面的退化几何与扩散动力学定量连接**。传统方法缺乏描述退化极小值附近几何结构的工具，而本文引入局部学习系数（LLC）$\lambda(w)$ 作为核心几何量：

$$ \lambda(w^*) = \lim_{\epsilon \to 0} \frac{ \log \frac{V(a\epsilon)}{V(\epsilon)} }{ \log(a) } $$

$\lambda(w)$ 度量了临界点附近低损失区域体积的缩放指数，本质上是一个“分形维度”，同时控制着两个关键动力学量：

1. **行走维度** $d_{\mathrm{walk}}$：通过 Alexander-Orbach 关系与 $\lambda$ 和谱维度 $d_s$ 关联：
   $$ d_{\mathrm{walk}}(t) = \frac{2\lambda(w_t)}{d_s} $$
   这一定理（Theorem 3.1）将权重位移的标度律直接与局部几何绑定。

2. **有效扩散系数** $D_\xi$：在长度尺度 $\xi$ 下，标量扩散系数由 $\lambda$ 和 $d_s$ 决定：
   $$ D_\xi(w) = \xi^{2 - \frac{2\lambda(w_t)}{d_s}} $$
   当 $\lambda > 0$（退化情形）时，$D_\xi$ 随 $\xi$ 减小而衰减，导致亚扩散；仅当 $\lambda = 0$（非退化二次极小值）时，$D_\xi$ 退化为常数，恢复标准布朗运动。

### 稳态分布的温度化贝叶斯解释

基于上述扩散模型，第三个核心创新是**导出了 SGD 稳态分布的显式形式，并揭示了其与贝叶斯后验的温度化关系**。在有效扩散系数 $D_\xi$ 近似恒定的区域内，FFPE 的稳态解为：

$$ p_s(w) \propto \exp\left( -\gamma \mathcal{L}_m[w] / D_\xi \right) $$

进一步，SGD 的稳态分布可表达为温度化的贝叶斯后验（Corollary 3.2）：

$$ p(w|X_m) = \frac{ \rho(w) p_s(w)^{m D_\xi} }{ Z_{m D_\xi} } $$

其中温度由有效扩散系数 $D_\xi$ 决定，而 $D_\xi$ 又依赖于局部学习系数 $\lambda$。这意味着 **SGD 并非均匀地探索所有解，而是偏好可访问性更高（即 $\lambda$ 更小）的区域**。实验验证了这一预测：SGD 找到的解集中在较低 LLC 值附近（Figure 4a），且温度化后的 SGD 分布与近似贝叶斯后验高度一致，KL 散度仅为 0.009（Table 2）。

这一框架将 SGD 的隐式偏好从经验观察提升为可计算的几何量，为理解泛化提供了动力学基础：SGD 天然倾向于收敛到 $\lambda$ 较小的“宽”极小值，这些极小值对应更好的泛化性能。

![[assets/figures/papers/iclr26_0010_5ebDXlue3d_Almost_Bayesian_Dynamics_of_SGD_Through_Singular/figures/001_Figure_1.jpg]]
*Figure 1: Mean weight displacement of a collection of fully connected neural networks trained using SGD on a randomly generated Moons dataset (Pedregosa et al., 2011), compared with expected displacement in the case of Brownian motion. It can be seen that this displays anomalous diffusion corresponding to early super-diffusion followed by late stage sub-diffusion*

本文提出了一套完整的分析管线，将 SGD 的长时间动力学建模为多孔介质上的分数阶扩散过程，并最终导出其稳态分布与温度化贝叶斯后验的对应关系。整体框架由四个核心模块串联而成，形成从经验观测到理论验证的闭环。

### 模块一：局部学习系数估计

该模块负责量化损失表面临界点附近的局部几何退化程度。对于每个检查点 $w^*$，采用 SGLD 采样与参数扰动相结合的方法估计局部学习系数（LLC）$\lambda(w^*)$：

$$
\hat{\lambda}(w^{*}) = \frac{n}{\log n} \left[ \mathbb{E}_{w|B_{r}(w^{*})}(L_{n}(w)) - L_{n}(w^{*}) \right]
$$

其几何含义是低损失区域体积的缩放指数，等价于参数空间在该点附近的分形维度。$\lambda$ 越大，意味着该临界点周围可访问的低损失体积越小，即解的“宽度”越窄。此模块的输出是沿 SGD 轨迹各检查点的 $\lambda(w_t)$ 序列，为后续扩散系数计算提供局部几何信息。

### 模块二：谱维度估计

谱维度 $d_s$ 刻画了扩散过程在参数空间中可访问状态体积随时间的增长律 $V_s(t) \sim t^{d_s/2}$。该模块利用 SGD 训练过程中记录的总权重位移 $R(t)$ 进行估计：

$$
\log(R(t)) = \frac{d_s}{2\lambda(w)} \log(t) + c
$$

具体操作上，对 $\log(R(t))$ 与 $\log(t)$ 进行线性回归，结合已获得的 $\lambda(w)$ 反解出 $d_s$。论文发现对于普通 SGD，谱维度在训练过程中可被单一常数良好刻画。该模块的输出是一个标量 $d_s$，表征了整个扩散过程的全局几何约束。

### 模块三：有效扩散系数计算

此模块是连接局部几何与全局动力学的枢纽。基于定理 3.1 建立的 Alexander-Orbach 关系 $d_{\mathrm{walk}}(t) = 2\lambda(w_t)/d_s$，将行走维度与局部学习系数、谱维度关联起来。进一步，在长度尺度 $\xi$ 下，有效标量扩散系数由推论 3.1 给出：

$$
D_\xi(w) = \xi^{2 - \frac{2\lambda(w_t)}{d_s}}
$$

该公式揭示了核心因果机制：局部学习系数 $\lambda$ 同时控制着有效扩散系数和可访问状态体积。当 $\lambda$ 较大时，指数 $2 - 2\lambda/d_s$ 可能小于 1，导致 $D_\xi$ 随尺度 $\xi$ 减小而减小——这正是亚扩散的数学表征。模块输出为各检查点处的有效扩散系数 $D_\xi(w_t)$，直接输入稳态分布推导。

### 模块四：稳态分布验证

该模块将理论预测与经验观测进行对比，完成闭环验证。在有效扩散系数近似恒定的区域内，分数 Fokker-Planck 方程的稳态解为温度化的 Gibbs 形式 $p_s(w) \propto e^{-\gamma \mathcal{L}_m[w]/D_\xi}$。进一步由推论 3.2，SGD 的稳态分布与贝叶斯后验的关系为：

$$
p(w|X_m) = \frac{\rho(w) p_s(w)^{m D_\xi}}{Z_{m D_\xi}}
$$

其中温度 $m D_\xi$ 取决于有效扩散系数，解释了 SGD 对参数空间可访问性的偏好——SGD 倾向于收敛到 $\lambda$ 较低（即更“宽”）的解区域。验证手段包括：计算 SGD 经验分布与温度化贝叶斯后验之间的 KL 散度、Wasserstein 距离和 Jensen-Shannon 散度；通过不同尺度 $\xi$ 下的理论分布与经验分布的 KL 散度曲线确定最优尺度。

### 数据流总览

整个管线的输入是 SGD 训练轨迹（权重快照序列与损失值），输出是经过验证的稳态分布与贝叶斯后验的对应关系。数据流依次经过：轨迹 → LLC 估计（模块一）→ 谱维度回归（模块二）→ 扩散系数合成（模块三）→ 稳态分布验证（模块四）。四个模块之间存在严格的依赖关系：模块二依赖模块一的 $\lambda$ 输出；模块三依赖模块一和模块二的联合输出；模块四依赖模块三的 $D_\xi$ 以及模块一的 $\lambda$ 分布。

### 适用范围与边界

该框架的有效性建立在两个关键假设之上：(1) SGD 在训练后期进入近似稳态，权重位移呈现亚扩散 $R(t) \propto t^{1/\nu}$（$\nu \geq 2$）；(2) 谱维度 $d_s$ 在训练过程中近似恒定。这两个假设在普通 SGD 训练的视觉模型（ResNet、VGG）和语言模型（TinyStories、TinyLlama）上均得到实验支持（Table 1 中 $R^2$ 达 0.98~1.00）。然而，对于 Adam 等自适应优化器，其可能改变黎曼度量结构并产生多个谱维度，该框架的直接适用性受限，需要进一步扩展。

本文的核心理论框架由四个相互关联的模块构成，它们共同将 SGD 的长时间动力学与奇异学习理论的局部几何描述联系起来。

### 模块一：从 Langevin 方程到分数阶 Fokker-Planck 方程

SGD 的权重更新可分解为梯度下降项与各向异性高斯噪声项，对应的 Langevin 随机微分方程为：

$$ \frac{dw}{dt} = -\gamma \nabla \mathcal{L}(w_{t-1}) + \Sigma_{w_{t-1}} $$

其中 $\gamma$ 为学习率，$\Sigma_{w_{t-1}}$ 为噪声协方差矩阵。该过程的概率密度演化由标准 Fokker-Planck 方程描述：

$$ \frac{\partial p(w,t)}{\partial t} = \nabla \cdot ( D(w,t) \nabla p(w,t) - \gamma p(w,t) \nabla \mathcal{L}(w) ) $$

然而，标准 Fokker-Planck 方程隐含假设扩散过程为布朗运动（位移 $R(t) \propto t^{1/2}$）。实验证据（Figure 1）显示 SGD 在训练后期呈现亚扩散行为（$R(t) \propto t^{1/\nu}$，$\nu \ge 2$），迫使理论框架引入分数阶导数。为此，采用 Caputo 分数阶导数算子：

$$ \mathcal{D}_t^\alpha f(t) = \frac{1}{\Gamma(1-\alpha)} \int_0^t \frac{f'(\tau)}{(t-\tau)^\alpha} d\tau $$

其中 $0 < \alpha < 1$ 控制亚扩散程度（$\alpha=1$ 退化为标准扩散）。将标准时间导数替换为 Caputo 分数阶导数，得到**时间分数阶 Fokker-Planck 方程**（FFPE）：

$$ \mathcal{D}_t^\alpha p(w,t) = \nabla \cdot ( D(w,t) \nabla p(w,t) - \gamma p(w,t) \nabla \mathcal{L}_m[w] ) \tag{4} $$

这是整个理论框架的动力学基础。分数阶导数的引入使得方程能够捕捉 SGD 在退化损失表面上的记忆效应和异常扩散特征。

### 模块二：局部学习系数——损失表面几何的量化

奇异学习理论的核心概念是**局部学习系数**（Local Learning Coefficient, LLC），它度量了临界点 $w^*$ 附近低损失区域的体积缩放行为：

$$ \lambda(w^*) = \lim_{\epsilon \to 0} \frac{ \log \frac{V(a\epsilon)}{V(\epsilon)} }{ \log(a) } \tag{6} $$

其中 $V(\epsilon) = \int_{\{w \in W \mid \mathcal{L}(w) < \epsilon\}} \rho(w) dw$ 是损失低于 $\epsilon$ 的参数空间体积。$\lambda(w^*)$ 本质上是损失表面在该临界点附近的“分形维度”：$\lambda$ 越小，意味着低损失区域体积增长越慢，即该解越“尖锐”；$\lambda$ 越大，低损失区域越“平坦”。

在实际计算中，LLC 通过 SGLD 采样和参数扰动方法估计（van Wingerden et al., 2024），其估计器为：

$$ \hat{\lambda}(w^{*}) = \frac{n}{\log n} [\mathbb{E}_{w|B_{r}(w^{*})}(\mathcal{L}_{n}(w)) - \mathcal{L}_{n}(w^{*})] $$

该估计器通过比较临界点附近球域内的期望损失与临界点损失来推断局部几何的缩放指数。

### 模块三：谱维度与 Alexander-Orbach 关系

为了连接局部几何与全局扩散行为，引入**谱维度** $d_s$，它描述了扩散过程在时间 $t$ 内可访问的状态体积：

$$ V_s(t) \sim t^{d_s/2} $$

谱维度可以通过权重位移 $R(t)$ 的对数-对数线性回归估计：

$$ \log(R(t)) = \frac{d_s}{2\lambda(w)} \log(t) + c \tag{17} $$

此处 $\lambda(w)$ 为沿轨迹的时间平均学习系数。实验表明（Table 1），对于标准 SGD，谱维度在训练过程中可被单一常数良好近似。

关键的桥梁是 **Alexander-Orbach 关系**，它将行走维度 $d_{\mathrm{walk}}$（由 $R(t) \sim t^{1/d_{\mathrm{walk}}}$ 定义）与局部学习系数和谱维度联系起来：

$$ d_{\mathrm{walk}}(t) = \frac{2\lambda(w_t)}{d_s} \tag{Theorem 3.1} $$

该定理表明：SGD 在损失表面上的扩散速度由局部几何（$\lambda$）和全局连通性（$d_s$）共同决定。$\lambda$ 越大或 $d_s$ 越小，行走维度越高，扩散越慢（亚扩散越强）。

### 模块四：有效扩散系数与稳态分布

在标量扩散近似下（假设有效扩散系数 $D_\xi$ 在局部近似恒定），FFPE 的稳态解可显式求出。**有效扩散系数**由局部学习系数和谱维度决定：

$$ D_\xi(w) = \xi^{2 - \frac{2\lambda(w_t)}{d_s}} \tag{Corollary 3.1} $$

其中 $\xi$ 为长度尺度。当 $\lambda(w_t) = d_s$ 时，$D_\xi = 1$，恢复标准扩散；当 $\lambda(w_t) > d_s$ 时，$D_\xi < 1$，扩散被抑制。

在此条件下，FFPE 的稳态分布为 Gibbs 形式：

$$ p_s(w) \propto \exp\left(-\gamma \frac{\mathcal{L}_m[w]}{D_\xi}\right) $$

进一步，SGD 的稳态分布与贝叶斯后验之间满足**温度化关系**：

$$ p(w|X_m) = \frac{ \rho(w) \, p_s(w)^{m D_\xi} }{ Z_{m D_\xi} } \tag{Corollary 3.2} $$

其中 $m$ 为训练样本数，$Z_{m D_\xi}$ 为归一化常数。该公式揭示了 SGD 并非采样标准贝叶斯后验，而是采样一个**温度化的贝叶斯后验**，温度 $T = 1/(m D_\xi)$ 由参数空间的可访问性（通过 $D_\xi$）决定。当损失表面存在严重退化（$\lambda$ 大，$D_\xi$ 小）时，有效温度升高，SGD 倾向于集中在更容易访问的解区域——这解释了 SGD 对平坦极小值的内在偏好。

### 模块间的因果链条

四个模块形成闭合的逻辑链：损失表面的退化几何（模块二）通过 Alexander-Orbach 关系（模块三）决定了扩散的异常程度，进而通过有效扩散系数（模块四）影响 FFPE（模块一）的稳态分布，最终导出 SGD 稳态分布与温度化贝叶斯后验的对应关系。这一链条将 SGD 的动力学行为从纯经验观察提升到了可定量预测的理论层面。

## 实验与关键发现

### 异常扩散现象的实证确认

论文首先在 Moons 数据集上训练全连接网络集群，追踪 SGD 下的平均权重位移 $R(t)$。如 Figure 1 所示，权重位移展现出典型的异常扩散行为：训练早期表现为超扩散（位移快于布朗运动的 $t^{1/2}$），而后期则进入亚扩散阶段，$R(t) \propto t^{1/\nu}$（$\nu \geq 2$）。这与传统基于二次极小值的 Ornstein-Uhlenbeck 过程所预测的布朗运动行为形成鲜明对比，直接证实了损失表面退化临界点对扩散动力学的根本性影响。

### 亚扩散模型拟合优度

为量化亚扩散假设的解释力，论文在多个模型上进行了对数位移-对数时间的线性回归，以估计谱维度 $d_s$ 和分数阶指数 $\alpha$。Table 1 汇总了关键结果：

- **视觉模型**（ResNet18、ResNet34、VGG16）：拟合优度 $R^2 \approx 1.00$，亚扩散模型几乎完美捕捉权重位移的标度律。
- **语言模型**（TinyStories-1M、TinyLlama-15M、TinyStories-33M）：$R^2 \approx 0.98$，虽略低于视觉模型，但仍高度支持亚扩散图景。

所有模型均获得接近 1 的 $R^2$，这一致性强烈表明：SGD 训练后期的权重动力学并非各向同性布朗运动，而是受损失表面退化几何约束的亚扩散过程。**需要手动验证**：论文未直接给出布朗运动基线模型的 $R^2$ 数值，仅通过对比暗示其解释力显著更弱，建议查看原文确认基线对比的定量细节。

### 稳态分布与贝叶斯后验的对应

理论部分的核心预测是：SGD 的稳态分布可表示为温度化的贝叶斯后验，温度由有效扩散系数 $D_\xi$ 决定。论文在 Moons 数据集上对这一预测进行了严格验证：

- **SGD 解的局部学习系数分布**（Figure 4a）：SGD 倾向于收敛到较低 LLC 值的区域，表明优化过程偏好几何上更“可访问”的解。
- **分布对比**（Figure 4b）：未温度化的 SGD 经验分布与近似贝叶斯后验存在系统性偏差——SGD 偏向簇 C1，而贝叶斯后验偏向簇 C2。经温度化处理后，两者高度一致。
- **统计距离**（Table 2）：温度化 SGD 分布与贝叶斯后验之间的 KL 散度仅为 **0.009**，Wasserstein 距离为 0.002，Jensen-Shannon 散度为 0.003。这些极低的距离度量提供了强有力的定量证据，支持“SGD 稳态分布等效于温度化贝叶斯后验”这一核心论断。

![[assets/figures/papers/iclr26_0010_5ebDXlue3d_Almost_Bayesian_Dynamics_of_SGD_Through_Singular/figures/007_Figure_4.jpg]]
*Figure 4: a) Shows the histogram of local learning coefficients of solutions found by SGD. Notice that as predicted by the theoretical results, they tend to concentrate near lower LLC values (better generalizing solutions). b) The probability concentrations of solutions found by SGD (blue), the approximate Bayesian posterior (orange), and the tempered SGD distribution (green) for each cluster. Notice that despite SGD itself preferring the cluster C1, after tempering ( $\xi$ = 0 . 5 ) , the tempered SGD steady state distribution almost entirely agrees with the Bayesian posterior. Statistical measures can be seen in table 2*

![[assets/figures/papers/iclr26_0010_5ebDXlue3d_Almost_Bayesian_Dynamics_of_SGD_Through_Singular/figures/008_Table_2.jpg]]
*Table 2: The KL divergence, the Wasserstein distance, and the Jensen-Shannon divergence for the approximated Bayesian posterior and the tempered SGD distribution*

### 有效扩散系数的尺度依赖性

理论分析指出，有效扩散系数 $D_\xi(w) = \xi^{2 - 2\lambda(w_t)/d_s}$ 依赖于所考察的长度尺度 $\xi$。Figure 3 展示了不同 $\xi$ 取值下，理论分布与经验分布之间的 KL 散度变化。结果表明存在一个最优的中间尺度使理论预测与实证分布最为吻合，这验证了多尺度分析的必要性——过小的 $\xi$ 会放大局部噪声，过大的 $\xi$ 则会掩盖退化几何的细节结构。

![[assets/figures/papers/iclr26_0010_5ebDXlue3d_Almost_Bayesian_Dynamics_of_SGD_Through_Singular/figures/005_Figure_3.jpg]]
*Figure 3: KL-divergences between the empirical vs. theoretical distribution for different choices of ξ*

### 消融分析：优化器与超参数的影响

论文通过一系列消融实验揭示了不同优化器下几何特征的差异：

- **学习率与 batch size 的相关性**（Figure 10、11）：在 SGD 下，局部学习系数 $\lambda$ 和谱维度 $d_s$ 与 batch size 的相关性强于与学习率的相关性。这意味着批量大小是调控扩散几何结构的关键超参数。
- **SGD vs. Adam**（Table 4）：SGD 展现出更高的谱维度（7.82 vs. 0.41）和更高的最终 LLC（12.53 vs. 3.10），同时测试准确率也更优（94.06% vs. 90.43%）。Adam 的谱维度显著更低，表明其动力学受限于更狭窄的参数子空间。
- **几何量与泛化的关联**（Figure 12、13）：使用 Adam 时，谱维度与测试准确率的相关性高于 LLC；而使用 SGD 时，LLC 的相关性更高。这一差异暗示两种优化器在损失表面上感知的“有效几何”存在本质不同。
- **LLC 与位移的相关性**（Figure 17）：LLC 与 SGD 权重位移的相关性强，但与 Adam 位移的相关性弱。论文推测这是因为 Adam 改变了参数空间的黎曼度量结构，使得基于欧氏度量的 LLC 不再能准确刻画其扩散行为。

![[assets/figures/papers/iclr26_0010_5ebDXlue3d_Almost_Bayesian_Dynamics_of_SGD_Through_Singular/figures/013_Table_4.jpg]]

### 失败模式与局限性

尽管理论框架在 SGD 上取得了令人信服的实证支持，但存在以下明确的失败模式：

1. **Adam 的谱维度多值性**：Adam 可能展现出多个谱维度（Table 4 中 Adam 的 $d_s$ 标准差异常大），使得单一常数谱维度的假设失效。这表明分数 Fokker-Planck 方程框架对自适应优化器的直接推广面临根本性障碍。
2. **训练初期的超扩散**：当前理论主要关注后期亚扩散阶段，但 Figure 1 明确显示训练早期存在超扩散行为。论文未对该阶段提供定量模型，这是理论覆盖范围的已知缺口。
3. **非平衡稳态的可能性**：理论假设 SGD 达到近似稳态，但若训练过程中存在标注噪声或持续的数据分布漂移，SGD 可能维持在非平衡稳态，此时稳态分布与贝叶斯后验的对应关系需要重新审视。

![[assets/figures/papers/iclr26_0010_5ebDXlue3d_Almost_Bayesian_Dynamics_of_SGD_Through_Singular/figures/004_Figure_2.jpg]]
*Figure 2: In a) we check that the result of lemma 3.4 holds. In b) we check that independent of our choice of diffusion model, the total displacement and average learning rate are strongly correlated in the large batch, low learning rate regime. Table 1: Results for different models*

## 定位与知识库关联

### 与先前工作的关系

本研究直接回应的核心瓶颈是：传统基于 Ornstein-Uhlenbeck 过程的 SGD 动力学模型（Mandt et al., 2016b）假设损失表面在极小值附近为二次型，从而将稳态分布刻画为高斯后验。然而，神经网络的损失表面存在大量退化（非二次）临界点，使得这一假设在实际训练后期失效。本文的工作正是填补了这一理论空白。

**对 SGLD 基准的超越**：SGLD（Welling & Teh, 2011）通过注入显式高斯噪声来近似贝叶斯后验，但未考虑参数空间的可访问性约束。本文证明，即使在无显式噪声注入的 vanilla SGD 中，其稳态分布天然地是一个温度化的贝叶斯后验 $p(w|X_m) = \rho(w) p_s(w)^{m D_\xi} / Z_{m D_\xi}$（推论 3.2），温度由有效扩散系数 $D_\xi$ 决定。这一对应关系在 Moons 数据集的全连接网络集群上得到验证：温度化 SGD 分布与贝叶斯后验的 KL 散度仅为 0.009（表 2），Wasserstein 距离为 0.002，Jensen-Shannon 散度为 0.003。

**关键理论跃迁**：从标准 Fokker-Planck 方程到时间分数阶 Fokker-Planck 方程 $\mathcal{D}_t^\alpha p(w,t) = \nabla \cdot ( D(w,t) \nabla p(w,t) - \gamma p(w,t) \nabla \mathcal{L}_m[w] )$（方程 4）的转变，是捕捉亚扩散行为的核心。这一跃迁的物理动机来自多孔介质中的异常扩散理论，而本文的贡献在于利用奇异学习理论将分数阶指数 $\alpha$ 与局部学习系数 $\lambda(w)$ 和谱维度 $d_s$ 建立了定量联系。

### 适用边界与局限

**优化器的适用范围**：本文的理论推导和实验验证主要针对 vanilla SGD。对于自适应优化器（如 Adam），理论适用性存在显著限制。实验证据表明，Adam 可能产生多个谱维度（表 4 中 Adam 的 $d_s$ 均值为 0.41，而 SGD 为 7.82），且学习系数 $\lambda$ 与 Adam 的相关性弱（图 17）。这暗示 Adam 改变了参数空间的黎曼度量结构，导致奇点结构不同，理论需要显式扩展才能适用。

**稳态假设的限制**：理论框架假设 SGD 在训练后期达到近似稳态，但实际中 SGD 可能只趋近临界点而不达到精确稳态。当存在标注噪声时，可能出现非平衡稳态，此时稳态分布的形式可能偏离推论 3.2 给出的温度化贝叶斯后验。论文未给出达到近似稳态所需时间（平衡时间）的定量估计，这是理论应用的一个实际限制。

**扩散阶段的覆盖范围**：理论主要关注训练后期的亚扩散阶段（$R(t) \propto t^{1/\nu}, \nu \geq 2$），而对于训练初期的超扩散行为未给出完整的动力学描述。大模型在训练初期可能展现更强的超扩散行为（图 1），这一阶段不在当前理论框架的核心覆盖范围内。

**标量扩散近似的局限**：推论 3.1 将各向异性扩散张量近似为有效标量扩散系数 $D_\xi(w) = \xi^{2 - 2\lambda(w_t)/d_s}$，这一近似在扩散张量高度非均匀的区域可能失效。附录 D.2 讨论了弱各向异性和弱梯度条件下的一阶通过时间结果是否成立，但未给出严格证明，该点需要进一步的理论工作。

### 开放问题

1. **自适应优化器的显式扩展**：如何将分数 Fokker-Planck 框架显式扩展到 Adam 等自适应优化器？Adam 改变了黎曼度量结构，可能导致不同的奇点结构和多个谱维度，需要重新推导行走维度与局部几何的关系。

2. **平衡时间的量化**：能否给出 SGD 达到近似稳态所需时间的定量估计？这对于判断理论在实际训练中的适用窗口至关重要。

3. **非平衡稳态的刻画**：如果 SGD 不趋于平衡，能否刻画其非平衡稳态及概率流？这对应标注噪声存在或学习率不衰减的场景。

4. **扩散阶段转换的动力学**：训练从超扩散到亚扩散的转换机制是什么？这一转换与损失表面的几何结构变化（如从一个吸引域进入另一个）有何关系？

5. **与涌现和相变的联系**：论文提出该框架为研究训练过程中的涌现和相变提供了工具，但未给出具体的研究路径。如何利用 $\lambda(w)$ 和 $d_s$ 的时间演化来检测和预测模型行为相变，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Almost_Bayesian_Dynamics_of_SGD_Through_Singular_Learning_Theory.pdf]]
