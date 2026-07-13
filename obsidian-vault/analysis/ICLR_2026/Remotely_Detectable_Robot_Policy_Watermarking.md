---
title: "Remotely Detectable Robot Policy Watermarking"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Remotely_Detectable_Robot_Policy_Watermarking.pdf
project_link: https://sites.google.com/view/robotpolicywatermarking/
code_link: null
openreview_forum_id: 8s5jBVybhQ
aliases:
- CNCC
- RDRPW
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "将策略探索噪声从白高斯噪声（WGN）替换为有色高斯噪声（CGN），并在频域用频谱相干性检测，该检测量对线性时不变（LTI）系统动力学具有不变性。"
primary_logic: "利用策略固有的随机性，在频域嵌入对边际分布无影响的水印信号，并通过频谱相干性（LTI 不变性）抵抗物理系统滤波，从而实现仅依赖远程观察的策略溯源。"
claims:
- "CoNoCo 通过在频域嵌入有色噪声并利用频谱相干性检测，实现远程水印。"
- "频谱相干性对未知 LTI 动力学具有不变性。"
- "水印保持动作的边际分布不变。"
- "在多种任务和远程观测条件下，CoNoCo 达到近乎完美的检测性能。"
---

# Remotely Detectable Robot Policy Watermarking

> [!tip] 核心洞察
> 利用策略固有的随机性，在频域嵌入对边际分布无影响的水印信号，并通过频谱相干性（LTI 不变性）抵抗物理系统滤波，从而实现仅依赖远程观察的策略溯源。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 可远程检测的机器人策略水印 |
| 英文题名 | Remotely Detectable Robot Policy Watermarking |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8s5jBVybhQ) · [Project](https://sites.google.com/view/robotpolicywatermarking/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Colored Noise Coherency (CoNoCo) |
| Dataset | RoboMaster Navigation (Real Robot), Velocity-Controlled VMAS Navigation (Sim), Mujoco Inverted Pendulum, Mujoco HalfCheetah |

> [!tip] 效果简介
> - RoboMaster Navigation (Real Robot) 上，Detection (ROC AUC) 为 ≈1.0，对比 varies, generally lower，变化 Best or near-best。
> - Velocity-Controlled VMAS Navigation (Sim) 上，Detection (ROC AUC) 为 high，对比 lower (some baselines fail on real robot)，变化 significant。
> - Mujoco Inverted Pendulum 上，Detection (ROC AUC) 为 near-perfect，对比 lower (Multi-Sine high but fails anonymity)，变化 superior when combined with anonymity。

## 概要

### 问题背景

在机器人策略部署中，策略所有者需要一种机制来验证部署在第三方机器人上的策略是否为其所有——即**策略溯源**。传统水印方法要求审计者能够访问机器人的内部状态或动作日志（白盒审计），但在现实场景中，审计者往往只能通过摄像头等外部传感器进行**远程观察**。这种远程观察面临三个核心挑战（C1–C3）：同步不确定性、未知系统动力学、以及干扰与测量噪声。这些挑战构成了“物理观察鸿沟”，使得传统水印方法在仅依赖远程观察时失效。

### 核心方法

本文提出 **CoNoCo（Colored Noise Coherency）**，一种在频域工作的策略水印方法。其核心思路是：

- **嵌入**：将策略原有的白高斯探索噪声替换为经带通滤波的有色高斯噪声（CGN），将水印信号集中在秘密频带 $\mathcal{B}$ 内，同时保持动作的边际分布不变（Theorem 5.1）。
- **检测**：利用**频谱相干性**（Spectral Coherency）作为检测统计量。频谱相干性对线性时不变（LTI）系统动力学具有不变性（Theorem 5.2），因此即使远程观测信号经历了未知的机器人动力学和传感器滤波，水印在频域的特征仍可被可靠检测。

### 方法定位

CoNoCo 属于**远程黑盒策略水印**方法，与现有工作的关键区别在于：

| 维度 | 传统方法 | CoNoCo |
|------|---------|--------|
| 水印载体 | 白高斯噪声（WGN） | 有色高斯噪声（CGN） |
| 检测域 | 时域（相关、能量检测等） | 频域（频谱相干性） |
| 同步需求 | 精确时间戳依赖 | 候选频率网格搜索 + 重采样 |
| 审计访问 | 内部状态/动作日志 | 仅需外部远程观察 |

对比的基线方法包括：**Multi-Sine Wave**（Ghamarilangroudi et al., 2025，嵌入秘密正弦波并通过 DFT 能量检测）、**Correlation-Based**（用秘密伪随机序列替换探索噪声，通过归一化互相关检测）、以及 **Tournament-Based**（基于 SynthID 改进，Dathathri et al., 2024）。

### 主要结果

- 在 **RoboMaster 真实机器人导航**任务中，CoNoCo 达到近乎完美的检测性能（ROC AUC ≈ 1.0），显著优于各基线方法。
- 在 **MuJoCo Inverted Pendulum** 和 **HalfCheetah** 等力/力矩控制任务中，CoNoCo 在保持匿名性和策略回报的同时，实现了近乎完美的可检测性。
- 消融实验表明：检测性能在约 1000 个时间步后饱和；CoNoCo 对时间偏移、抖动、丢帧和视角偏差均表现出强鲁棒性。
- 对抗性分析显示，加性噪声攻击和带阻滤波攻击在削弱水印的同时会导致策略行为严重失真，攻击代价高昂。

### 局限与开放问题

CoNoCo 依赖策略的随机性来嵌入水印，**目前不能直接应用于确定性策略**。理论分析假设 LTI 系统动力学，在强非线性或快速时变场景下性能可能下降。此外，远程速度估计依赖计算机视觉方法，对遮挡和光照变化的鲁棒性有限。开放问题包括：如何扩展到确定性控制策略、如何在多运动对象场景下鲁棒提取运动 glimpse、以及对抗性带宽感知攻击的理论上限等。



### 机器人策略溯源的黑箱困境

现代机器人系统日益依赖深度强化学习（RL）训练的连续控制策略。这些策略的开发往往需要大量计算资源、专家知识和真实环境交互，构成了高价值知识产权。然而，策略一旦部署到用户自有的机器人上，其内部参数和动作日志对策略所有者即不可见。此时，如何仅通过**外部远程观察**（如摄像头视频）来验证机器人上运行的策略是否为自己的知识产权，成为一个尚未解决的问题。

这一需求催生了**可远程检测的策略水印**问题：策略所有者希望在不干扰策略正常行为的前提下，嵌入一个可识别的签名；审计者仅需通过远程传感器获取的“glimpse”（不完整的状态/运动片段），就能可靠地判定该策略是否含水印。

### 物理观察鸿沟：三个核心挑战

传统数字水印技术（如图像、音频水印）依赖对嵌入信号的精确同步和对传输信道的已知假设。但在机器人策略水印场景中，审计者面对的是**物理世界观察鸿沟**，具体表现为三个递进挑战（Table 1）：

1. **同步不确定性（C1）**：远程传感器与策略执行时钟之间不存在精确同步，glimpse 序列存在未知的时间偏移和采样率失配。
2. **未知系统动力学（C2）**：策略输出的动作需经过机器人自身的控制器、执行器和物理本体，形成未知的线性/非线性动力学变换，再被远程传感器捕捉。审计者无法获知这一完整映射。
3. **干扰与噪声（C3）**：远程观测中混入传感器噪声、环境扰动及其他无关运动信号。

这三个挑战使得传统水印方法失效：时域相关检测无法应对未知动力学滤波；能量检测对同步偏移高度敏感；而直接替换探索噪声的方法虽能保持动作分布，却无法在远程观测中可靠提取。

### 现有方法的局限

已有工作尝试在策略中嵌入水印，但均未解决远程检测问题：

- **Multi-Sine Wave 方法**（Ghamarilangroudi et al., 2025）受重放攻击检测启发，在动作中注入秘密正弦波，通过 DFT 能量峰值检测。该方法在直接访问动作信号时有效，但经过未知系统动力学滤波后，正弦波的幅度和相位被严重扭曲，远程检测性能急剧下降。
- **Correlation-Based 方法**用秘密伪随机序列替换探索噪声，通过归一化互相关检测。该方法同样依赖时域对齐，对同步误差和动力学变换缺乏鲁棒性。
- **Tournament-Based 方法**（基于 SynthID，Dathathri et al., 2024）扩展至连续动作空间，但其检测机制未针对远程物理观察场景设计。

这些方法的共同缺陷在于：**检测机制与物理信道特性不匹配**——它们假设审计者可以获取“干净”的动作信号，而忽略了机器人本体和远程传感器构成的未知滤波链路。

### 核心动机：频域不变性与策略随机性

本文的核心洞察是：**利用策略固有的探索随机性，在频域嵌入水印信号，并通过一种对线性时不变（LTI）系统具有不变性的检测量——频谱相干性（Spectral Coherency）——来抵抗物理系统滤波**。

具体而言，标准连续控制策略的动作输出通常为高斯分布：

$$a_k = \mu_{\theta}(\mathbf{o}_k) + \Sigma_{\theta}(\mathbf{o}_k) \epsilon_k$$

其中 $\epsilon_k \sim \mathcal{N}(0, I)$ 为白高斯探索噪声（WGN）。该噪声仅影响动作的随机性，不改变策略的确定性行为。本文提出将 WGN 替换为**有色高斯噪声（CGN）**，将水印信号编码在特定频带内。由于 CGN 与 WGN 具有相同的边际分布 $\mathcal{N}(0, I)$（Theorem 5.1），水印嵌入**不改变动作的边际分布**，从而保持策略的行为特性。

在检测端，频谱相干性定义为：

$$C_{XY}(f) = \frac{S_{XY}(f)}{\sqrt{S_{XX}(f) S_{YY}(f)}}$$

其模长 $|C_{XY}(f)| \in [0, 1]$ 衡量两个信号在频率 $f$ 处的线性关系强度。关键性质在于：**相干性幅度对 LTI 滤波具有不变性**（Theorem 5.2）——无论信号经过何种未知的 LTI 系统，只要输入与输出之间存在线性关系，相干性幅度保持不变。这恰好解决了 C2（未知系统动力学）问题。

由此，本文提出 **CoNoCo（Colored Noise Coherency）**：在频域嵌入有色噪声水印，通过频谱相干性进行检测，辅以频率网格搜索和重采样机制处理同步不确定性（C1），从而首次实现仅依赖远程观察的策略所有权验证。



## 核心方法与创新机理

CoNoCo 的核心创新在于将策略溯源问题从传统的“白盒审计”范式迁移至“远程黑盒检测”范式。其关键洞察是：**利用连续控制策略固有的随机性作为水印载体，在频域嵌入信号，并通过频谱相干性对线性时不变（LTI）系统动力学的不变性来抵抗物理世界的滤波效应**。这一设计直接破解了远程策略水印的核心瓶颈——物理观察鸿沟（同步不确定性、未知系统动力学、干扰与噪声）。

### 关键创新点（Changed Slots）

相较于现有基线方法，CoNoCo 在以下四个维度上实现了根本性的改变：

**1. 探索噪声类型：从白高斯噪声（WGN）到有色高斯噪声（CGN）**

现有策略（如 PPO 等标准连续控制算法）在动作采样时添加的是白高斯噪声，其功率在频谱上均匀分布。CoNoCo 将探索噪声替换为经过带通滤波并归一化的有色高斯噪声（CGN），将水印能量集中在预设的秘密频带 $\mathcal{B}$ 内。这一改变是水印可检测性的基础：它使得水印信号在特定频率上具有了可辨识的“频谱特征”，同时保持了动作的边际分布不变（Theorem 5.1 证明 $W_k$ 的边际分布仍为 $\mathcal{N}(0, I)$），从而满足匿名性要求。

**2. 检测方法：从时域检测到频域频谱相干性检测**

基线方法依赖时域相关或能量检测，这些方法在信号经过未知物理系统滤波后，其时域波形会发生严重畸变，导致检测失效。CoNoCo 转而使用频谱相干性（Spectral Coherency）作为检测度量：

$$C_{XY}(f) = \frac{S_{XY}(f)}{\sqrt{S_{XX}(f) S_{YY}(f)}}$$

其核心优势在于 **LTI 不变性**（Theorem 5.2）：当水印信号 $W$ 和远程观测 $G$ 分别经过相同的 LTI 系统时，二者之间的频谱相干性幅值保持不变。这意味着，无论机器人的底层动力学如何对动作进行“滤波”，只要系统可近似为 LTI，水印在频域的线性关系就得以保留。检测分数 $D(G)$ 在所有候选频率和观测维度上对秘密频带内的平均相干性取最大值，从而实现了对未知动力学的鲁棒性。

**3. 同步机制：从精确时间戳依赖到候选频率网格搜索与重采样**

远程观测无法获取策略的精确执行时间戳，这引入了严重的时间同步不确定性（C1 挑战）。CoNoCo 通过在候选频率集合 $\mathcal{F}_{\text{search}}$ 上进行网格搜索，并利用多项式重采样（ResamplePoly）将水印序列对齐到观测的时间尺度，从而在无需精确同步信息的条件下恢复频域对齐。此外，CoNoCo 结合 GCC-PHAT 技术处理时间偏移，进一步增强了检测的鲁棒性。

**4. 审计访问要求：从内部状态/动作日志到仅需外部远程观察**

传统水印检测需要访问策略的内部状态或动作日志（白盒假设），这在实际部署中极不现实。CoNoCo 将审计的输入要求降低为仅需外部远程观察（如摄像头视频或运动捕捉数据），即所谓的“glimpse”。这一改变使得策略溯源从实验室场景走向真实世界部署成为可能——审计者无需与被审计的机器人有任何物理接触或软件接口。

### 理论保证与设计机理

CoNoCo 的检测性能由信号干扰噪声比（SINR）直接决定：

$$|C_{WG}(f)|^2 = \frac{\mathrm{SINR}(f)}{\mathrm{SINR}(f) + 1}$$

其中 $\mathrm{SINR}(f) = P_S(f) / P_N(f)$。当水印功率 $P_S(f)$ 显著高于干扰加噪声功率 $P_N(f)$ 时，相干性趋近于 1，检测近乎确定。水印功率由策略的探索尺度 $\Sigma$ 直接控制，因此策略的随机性越强，可检测性越高——这恰好与连续控制策略的典型特性相吻合。当系统呈现非线性或时变特性时，CoNoCo 通过短时分析（Welch 方法分窗处理）和多维度平均（利用空间分集）来缓解频谱扩散效应，保持检测鲁棒性。



![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_8s5jBVybhQ/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the pipeline for robot policy watermarking. In Step 1, the policy owner trains a policy, adds a watermark to it and produces a detection function to identify it. In Step 2, the watermarked policy is used by a policy user who deploys it on their own robot. In Step 3, a policy auditor aims to identify the policy used on the robot. To do so, they can only access glimpses of the policy behaviour through remote sensing, such as a camera feed; these glimpses are passed through the detection function to identify the policy*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_8s5jBVybhQ/figures/003_Table_1.jpg]]
*Table 1: Overview of the glimpse modalities considered in our experiments and the challenges they induce*

CoNoCo 将机器人策略水印定义为一个三阶段管道（Figure 1），其核心设计目标是使审计者仅凭远程观察（如摄像头视频）即可判定机器人是否运行了特定策略。

**阶段一：策略训练与水印注入。** 策略所有者首先使用标准强化学习算法（如 PPO）预训练一个连续控制策略，该策略输出高斯分布的均值 $\mu_{\theta}(\mathbf{o}_k)$ 和探索尺度 $\Sigma_k$。水印的注入发生在推理时，而非训练过程中——这一设计保证了所有水印方法可在同一预训练策略上公平比较，且不干扰训练收敛。注入方式为：将策略原有的白高斯探索噪声（WGN）替换为基于秘密种子生成的有色高斯噪声（CGN），使水印动作 $\tilde{a}_k = \mu_{\theta}(\mathbf{o}_k) + \Sigma_k \cdot W_k$ 在频域携带可识别信号，同时保持动作的边际分布不变（Theorem 5.1）。

**阶段二：策略部署。** 策略使用者将已注入水印的策略部署到自己的机器人上。机器人在执行过程中通过观测-动作循环与环境交互，其运动轨迹自然地携带了水印信号。

**阶段三：远程审计与检测。** 审计者仅能通过外部传感器获取机器人的运动片段（glimpse），例如远程摄像头视频或运动捕捉数据。检测管道包含五个关键模块：

1. **水印生成模块**：基于秘密种子生成伪随机白高斯噪声，通过 Butterworth 带通滤波器将能量集中在目标频带 $\mathcal{B}$ 内，再归一化得到有色高斯噪声序列 $W_k$。
2. **频率对齐与重采样模块**：估计策略执行频率 $f_\pi$，将基准水印重采样到与远程观测时间尺度一致的频率上，以应对同步不确定性（C1）。
3. **相干性计算模块**：使用 Welch 方法计算水印与远程观测信号各维度的频谱相干性 $C_{W_d' G_d}(f; s)$，该指标对线性时不变（LTI）系统动力学具有不变性（Theorem 5.2），从而抵抗未知系统动力学（C2）的影响。
4. **分数聚合模块**：在秘密频带 $\mathcal{B}$ 内取平均相干性幅值，并跨多个物理维度 $D$ 取均值，以利用空间分集提升鲁棒性。
5. **检测判定模块**：在所有候选频率假设 $\mathcal{F}_{\text{search}}$ 上取最大值作为最终检测分数 $D(G)$，通过阈值判定策略归属。

**物理观察鸿沟。** Table 1 系统刻画了四种观测模态面临的三个核心挑战：C1 同步不确定性（远程传感器采样时刻与策略执行时刻不匹配）、C2 未知系统动力学（机器人自身动力学和控制器对动作信号进行滤波）、C3 干扰与噪声（环境扰动和测量噪声）。Ground Truth Action 不受任何挑战影响，但要求白盒访问；Onboard Sensors 仅受 C2 和 C3 影响；而 Remote Motion Capture 和 Remote Camera Feed 则面临全部三个挑战，是 CoNoCo 设计的核心目标场景。CoNoCo 通过频域嵌入与频谱相干性检测的组合，在仅依赖远程观察的条件下跨越了这一物理观察鸿沟。



CoNoCo 的核心机制由水印生成、水印注入、同步对齐、相干性计算和分数聚合五个模块构成。以下逐一阐述其关键公式与变量含义。

### 水印生成

水印生成模块的目标是基于秘密种子 $S$ 产生一个有色高斯噪声（CGN）序列 $W_k \in \mathbb{R}^D$，将其能量集中在预设的秘密频带 $\mathcal{B} = [f_{\text{low}}, f_{\text{high}}]$ 内。具体流程为：

1. 以 $S$ 为种子生成伪随机白高斯噪声（WGN）序列 $X$。
2. 设计一个数字带通滤波器 $H_{\mathcal{B}}$（论文中采用 Butterworth 带通滤波器），对 $X$ 进行滤波，得到原始有色噪声 $W_{\text{raw}} = H_{\mathcal{B}}(X)$。
3. 对每个动作维度 $d$，将 $W_{\text{raw}}$ 归一化为单位方差：$W_{[:,d]} = W_{\text{raw}} / \operatorname{Std}(W_{\text{raw}})$。

这一过程确保了 $W_k$ 的边际分布仍为标准正态分布 $\mathcal{N}(0, I)$，这是后续保持动作分布不变性的基础。

### 水印注入

水印注入发生在策略推理阶段。标准随机策略的动作采样形式为：

$$a_k = \mu_\theta(\mathbf{o}_k) + \Sigma_k \cdot \epsilon_k$$

其中 $\mu_\theta(\mathbf{o}_k)$ 为策略网络输出的均值动作，$\Sigma_k$ 为探索尺度，$\epsilon_k \sim \mathcal{N}(0, I)$ 为白高斯噪声。CoNoCo 将 $\epsilon_k$ 替换为水印噪声 $W_k$，得到水印动作：

$$\tilde{a}_k = \mu_\theta(\mathbf{o}_k) + \Sigma_k \cdot W_k$$

由于 $W_k$ 与 $\epsilon_k$ 具有相同的边际分布 $\mathcal{N}(0, I)$，水印注入不改变动作的概率分布，从而满足匿名性要求（W1）。

### 同步对齐与重采样

远程观测信号 $G$ 的采样频率 $f_g$ 与策略执行频率 $f_\pi$ 通常不同且未知。检测时，需要在候选频率集合 $\mathcal{F}_{\text{search}}$ 中搜索最佳对齐频率 $s$。对于每个候选 $s$，将基础水印 $W_{\text{base}}$ 通过多项式重采样（`ResamplePoly`）调整到与观测信号一致的时间尺度：

$$W_s' = \text{ResamplePoly}(W_{\text{base}}, f_g / s)$$

这一重采样步骤是处理同步不确定性（C1）的关键。

### 频谱相干性计算

对对齐后的水印 $W'$ 和观测信号 $G$ 的每个维度 $d$，采用 Welch 方法估计其频谱相干性。复相干性定义为归一化交叉谱密度：

$$C_{XY}(f) = \frac{S_{XY}(f)}{\sqrt{S_{XX}(f) S_{YY}(f)}}$$

其中 $S_{XY}(f)$ 为信号 $X$ 与 $Y$ 在频率 $f$ 处的交叉谱密度，$S_{XX}(f)$ 和 $S_{YY}(f)$ 分别为各自的功率谱密度。相干性模长 $|C_{XY}(f)| \in [0, 1]$ 衡量两信号在频率 $f$ 处的线性关系强度。

### 分数聚合

最终检测分数 $D(G)$ 定义为所有候选频率 $s$ 和所有维度 $d$ 上，秘密频带 $\mathcal{B}$ 内平均相干性模长的最大值：

$$D(G) = \max_{s \in \mathcal{F}_{\text{search}}} \left( \frac{1}{D} \sum_{d=1}^{D} \operatorname{mean}_{f \in \mathcal{B}} |C_{W_d' G_d}(f; s)| \right)$$

这一聚合策略利用了多维度空间分集和候选频率搜索，增强了对非线性时变系统效应的鲁棒性。

### 理论支撑：相干性与 SINR 的关系

CoNoCo 的检测性能由信号干扰噪声比（SINR）决定。在频率 $f$ 处，SINR 定义为水印信号功率 $P_S(f)$ 与干扰加噪声功率 $P_N(f)$ 之比：

$$\mathrm{SINR}(f) = \frac{P_S(f)}{P_N(f)}$$

论文证明了水印 $W$ 与观测信号 $G$ 之间的模平方相干性仅由 SINR 决定：

$$|C_{WG}(f)|^2 = \frac{\mathrm{SINR}(f)}{\mathrm{SINR}(f) + 1}$$

该关系揭示了两个核心性质：
- 当 $\mathrm{SINR}(f) \gg 1$ 时，$|C_{WG}(f)|^2 \to 1$，检测可靠。
- 探索尺度 $\Sigma_k$ 直接控制 $P_S(f)$ 的强度，因此策略的随机性越强，水印可检测性越高（满足 W2）。

此外，论文证明了相干性模长在线性时不变（LTI）系统滤波下具有不变性（Theorem 5.2），这是 CoNoCo 能够抵抗未知系统动力学（C2）的理论基石。对于实际中常见的线性时变（LTV）系统，CoNoCo 通过 Welch 方法的短时分析和多维度平均加以缓解。



## 实验与关键发现

### 实验设置与评估维度

实验覆盖四类观测模态（Table 1），分别对应审计者不同的物理访问级别：**Ground Truth Action**（无物理鸿沟）、**Onboard Sensors**（面临 C2 系统动力学与 C3 干扰噪声）、**Remote Motion Capture** 与 **Remote Camera Feed**（同时面临 C1 同步不确定性、C2 系统动力学、C3 干扰噪声）。其中 Remote Camera Feed 通过模板匹配（LuNežič et al., 2018）将视频转换为速度估计，是最贴近现实审计场景的模态。

测试平台包含四类任务：RoboMaster 真实机器人导航（速度控制）、VMAS 导航（速度控制与力控制两种变体）、MuJoCo 倒立摆（力矩控制）、MuJoCo HalfCheetah（力矩控制）。所有水印策略均在推理时应用于相同的预训练 PPO 策略，不干扰训练过程；每种水印方法均保留动作的边际高斯分布，确保策略行为的直接影响可比。

### 主实验结果

**CoNoCo 在所有任务和观测模态下均达到近乎完美的可检测性。** 在真实机器人 RoboMaster 导航任务上，CoNoCo 的 ROC AUC 约为 1.0（Figure 3），同时在匿名性（使用不同种子检测时 AUC 接近 0.5）和回报保持（水印与非水印策略的奖励分布几乎重合）两个维度上均表现优异。相比之下，Multi-Sine Wave 虽然检测性能同样很高，但匿名性极差——攻击者用不同种子即可轻易检测到水印的存在，暴露了策略来源。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_8s5jBVybhQ/figures/007_Figure_3.jpg]]
*Figure 3: Results on the RoboMaster Navigation tasks. (A) Example trajectories of the watermarked and nonwatermarked policies on the robot. (B) Detectability: ROC curve for 40 replications of the watermarked and non-watermarked policy for each baseline, lines indicate median and dashed areas quartiles. (C) Anonymity: computed as 1− area under the ROC curve, for detection with a different seed. (D) Reward Preservation: reward distribution of the watermarked and non-watermarked policies*

在力矩/力控制任务（倒立摆、HalfCheetah、力控 VMAS 导航）上，CoNoCo 继续保持近乎完美的检测性能（Figure 4），而 Tournament-Based 和 Correlation-Based 方法在部分任务上出现明显退化。Multi-Sine Wave 在检测维度上表现强劲，但其匿名性在所有任务中均显著低于 CoNoCo，这构成了关键的实用缺陷：高检测率若不能与匿名性解耦，策略所有者将无法在不暴露身份的前提下进行审计。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_8s5jBVybhQ/figures/008_Figure_4.jpg]]
*Figure 4: Results on a variety of Force and Torque Control tasks with increasing difficulty. (A) Detectability: ROC curve over 100 replications of the watermarked and non-watermarked policy for each baseline, lines indicate median and dashed areas quartiles. (B) Anonymity: computed as the complement to 1 of the ROC area under the curve for detection with a different owner seed, for Onboard Sensors glimpses. (C) Reward Preservation: reward distribution of the watermarked and non-watermarked policies*

在速度控制 VMAS 导航任务（Figure 14）中，CoNoCo 在仿真和真实机器人对比中均保持显著优势，部分基线方法在真实机器人上完全失效，凸显了 CoNoCo 对物理系统动力学不确定性的鲁棒性。

### 检测灵敏度与鲁棒性分析

**序列长度依赖性（Figure 5）：** 检测性能在约 1000 个时间步后趋于饱和，表明 CoNoCo 在相对较短的观测窗口内即可达到可靠检测。这一特性对实际部署至关重要——审计者无需长时间监控即可做出判断。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_8s5jBVybhQ/figures/009_Figure_5.jpg]]
*Figure 5: Relationship between glimpse sequence length and the watermark detectability of CoNoCo. Detectability is reported as the ROC AUC averaged over 10 repetitions. We use the Onboard Sensors glimpse modality, except for “RoboMaster Navigation,” where we instead use real-world data from our robot experiments with Motion Capture glimpses. Shaded regions indicate quartiles*

**时间偏移处理（Figure 6）：** 标准 CoNoCo 对 glimpse 序列的时间偏移较为敏感，但 CoNoCo-Offset-Handling（结合 GCC-PHAT 的增强版本）在即使存在较大时间偏移时仍能保持 AUC ≈ 1.0，证明同步机制设计的有效性。

**时间抖动（Figure 7）：** 在远超真实 RoboMaster 平台测量到的抖动水平下，CoNoCo 仍保持鲁棒。红色竖线标记了实际系统中的抖动量级，远低于导致性能退化的阈值。

**观测丢帧（Figure 8）：** 在最多丢失 200 帧 glimpse 的极端条件下，CoNoCo 依然保持高检测率，表明其对断续观测的容忍度。

**视角偏移（Figure 9）：** 当运动捕捉注视角度偏差超过 60° 时，检测性能才开始显著下降，说明 CoNoCo 对视角变化具有较宽的容限。

### 对抗性鲁棒性

**加性噪声攻击（Figure 10）：** 在 HalfCheetah 任务上，即使对抗性噪声强度达到 σ=2，CoNoCo 的检测分数仍保持在较高水平，攻击者未能完全消除水印。而在倒立摆任务上，σ=0.25 即已严重降低检测分数，但同时也导致策略回报大幅下降——攻击者需要付出破坏策略性能的代价才能削弱水印。这种“检测-性能”权衡是 CoNoCo 对抗性鲁棒性的核心机制。

**带阻滤波攻击（Figure 11）：** 攻击者通过增加滤波器阶数来削弱水印频带内的信号，但随之而来的是策略行为的严重失真（MSE 增加 257%）。这意味着带阻滤波攻击在实际中代价高昂，攻击者必须在隐蔽性和策略可用性之间做出权衡。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_8s5jBVybhQ/figures/021_Figure_11.jpg]]
*Figure 11: Adversarial Trade-off for Band-Stop Filtering Attack. As the adversary increases the filter strength (Order), the watermark detection score (Blue) decreases, but the distortion (MSE) to the original policy behavior (Red) increases dramatically (by 257% in this simulation), demonstrating the degradation of policy utility*

**结构化干扰信号（Figure 12）：** 攻击者无法在不拥有秘密密钥的情况下生成抵消水印的干扰信号。功率谱密度分析表明，水印与干扰信号的组合功率等于各自功率之和，证实了抵消的不可能性——这是频域水印基于密钥随机性的根本安全保障。

### 失败模式与局限性

1. **确定性策略不适用：** CoNoCo 依赖策略的随机性来嵌入水印，目前无法直接应用于确定性控制策略，需要额外的变异源。
2. **非线性/时变动力学：** 理论分析假设 LTI 系统动力学。当系统呈现强非线性或快速时变特性时，检测性能可能下降。文中通过 Welch 方法的短时分析、多维度平均和频带选择加以缓解，但在极端非线性场景下仍需验证。
3. **远程速度估计的脆弱性：** 基于模板匹配的计算机视觉方法对严重遮挡、不利光照或视角变化鲁棒性有限，这直接限制了 Remote Camera Feed 模态在实际部署中的可靠性。
4. **频率先验依赖：** 水印检测需预先标定策略执行频率的上下界。当这些先验信息不可靠时，搜索范围扩大将影响检测可靠性。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Figure 3 | CoNoCo 在真实机器人上达到近乎完美检测，同时保持匿名性和回报 |
| Figure 4 | 在多种力矩/力控任务上，CoNoCo 检测性能优于或持平所有基线，且匿名性显著优于 Multi-Sine Wave |
| Figure 5 | 检测性能在约 1000 时间步后饱和，审计效率高 |
| Figure 6 | 增强版 CoNoCo-Offset-Handling 对时间偏移几乎免疫 |
| Figure 10 | 对抗性噪声攻击需要付出策略性能代价才能削弱水印 |
| Figure 11 | 带阻滤波攻击导致策略行为严重失真（MSE +257%） |



## 定位与知识库关联

### 问题定位：物理观察鸿沟下的策略溯源

CoNoCo 瞄准的核心瓶颈是**物理观察鸿沟**（Physical Observation Gap）：当审计者仅能通过外部传感器（如摄像头）远程观察机器人的运动轨迹时，三个相互交织的挑战使得传统水印方法失效——**C1 同步不确定性**（策略执行与远程观测之间的时间偏移未知）、**C2 未知系统动力学**（机器人的物理动态将动作信号滤波为观测信号）、**C3 干扰与噪声**（环境扰动和传感器噪声叠加在观测上）。Table 1 系统刻画了这一鸿沟：Ground Truth Action 不受任何挑战影响，而 Remote Camera Feed 则同时面临全部三项挑战。

现有机器人策略水印方法均未有效跨越这一鸿沟。**Multi-Sine Wave**（Ghamarilangroudi et al., 2025）受重放攻击检测启发，在动作中嵌入秘密正弦波，通过 DFT 能量检测——但该方法在远程观测下因系统动力学对正弦信号的滤波和相位偏移而严重退化，且匿名性极低（Figure 4 显示其在不同种子下的检测 AUC 接近 1.0，意味着水印极易被非所有者识别）。**Correlation-Based** 方法用秘密伪随机序列替换探索噪声，通过归一化互相关检测，但其时域相关性在动力学滤波后迅速衰减。**Tournament-Based** 方法（基于 SynthID，Dathathri et al., 2024）将文本水印的锦标赛检测扩展到连续动作空间，但同样缺乏对物理系统滤波的理论不变性保证。

### 核心创新：频域不变性与有色噪声注入

CoNoCo 的方法论突破在于两个相互耦合的设计选择：

**（1）将水印载体从白高斯噪声（WGN）替换为有色高斯噪声（CGN）**。标准连续控制策略的动作采样为 $\tilde{a}_k = \mu_{\theta}(\mathbf{o}_k) + \Sigma_k \cdot W_k$，其中 $W_k$ 是探索噪声。CoNoCo 将 $W_k$ 从 WGN 改为经 Butterworth 带通滤波器处理并归一化的 CGN，将信号能量集中在秘密频带 $\mathcal{B}$ 内。Theorem 5.1 证明这一替换保持了动作的边际分布 $N(0, I)$ 不变，从而满足水印的匿名性要求（W1）。

**（2）在频域使用频谱相干性（Spectral Coherency）作为检测统计量**。复相干性定义为 $C_{XY}(f) = \frac{S_{XY}(f)}{\sqrt{S_{XX}(f) S_{YY}(f)}}$，其模长 $\in [0,1]$ 衡量两个信号在频率 $f$ 处的线性关系强度。Theorem 5.2 揭示了这一选择的关键性质：**相干性模长对线性时不变（LTI）系统动力学具有不变性**。这意味着无论机器人的物理动态如何对动作信号进行线性滤波，水印信号与远程观测之间的相干性在理论上保持不变。检测分数 $D(G)$ 在所有候选频率 $\mathcal{F}_{\text{search}}$ 上最大化秘密频带内的平均相干性模长，从而同时解决了 C1（频率搜索）和 C2（LTI 不变性）的挑战。

这一设计将水印检测从“在时域匹配信号形状”转变为“在频域检测线性关系强度”，后者对未知动力学具有天然的鲁棒性。Theorem 5.3 进一步建立了相干性与信号干扰噪声比（SINR）的单调关系 $|C_{WG}(f)|^2 = \frac{\mathrm{SINR}(f)}{\mathrm{SINR}(f) + 1}$，为检测性能提供了可分析的理论基础：当水印功率 $P_S(f)$ 显著高于噪声功率 $P_N(f)$ 时，相干性趋近于 1。

### 与基线的系统性差异

| 维度 | Multi-Sine Wave | Correlation-Based | Tournament-Based | **CoNoCo** |
|------|-----------------|-------------------|------------------|------------|
| 水印载体 | 确定性正弦波叠加 | 伪随机序列替换噪声 | 锦标赛评分函数 | 有色高斯噪声替换探索噪声 |
| 检测域 | 频域（DFT 能量） | 时域（互相关） | 统计假设检验 | 频域（频谱相干性） |
| LTI 不变性 | 无（正弦波被滤波变形） | 无（时域相关性被破坏） | 无 | 有（Theorem 5.2） |
| 同步机制 | 无 | 无 | 无 | 候选频率网格搜索 + GCC-PHAT 时间偏移处理 |
| 审计访问要求 | 动作日志（白盒） | 动作日志（白盒） | 动作日志（白盒） | 仅需远程观察（黑盒） |
| 匿名性 | 极低 | 中等 | 中等 | 高（边际分布不变） |

### 适用边界与局限

CoNoCo 的有效性依赖于若干前提条件，这些条件定义了其适用边界：

**（1）策略随机性依赖**。CoNoCo 通过替换探索噪声来嵌入水印，因此**无法直接应用于确定性策略**。对于输出确定性动作的策略（如 DDPG 在推理时），需要额外的变异源来承载水印信号。

**（2）LTI 假设的松弛**。理论分析基于 LTI 系统动力学假设。当机器人系统呈现强非线性或快速时变（LTV）特性时，相干性不变性不再严格成立。CoNoCo 通过两种机制缓解这一问题：Welch 方法的短时分析将信号分割为短窗口，在窗口内近似 LTI；多维度平均利用空间分集，聚合来自不同物理维度（如 $x, y$ 位置）的相干性，其中某些维度可能更接近 LTI 行为。但这一缓解是经验性的，缺乏对非线性程度的理论上限保证。

**（3）远程速度估计的脆弱性**。Remote Camera Feed 模态依赖基于模板匹配的计算机视觉方法（LuNežič et al., 2018）将视频转换为速度估计。在严重遮挡、不利光照或大视角变化（Figure 9 显示角度偏差超过 60° 时检测性能开始显著下降）的情况下，速度估计的质量成为瓶颈。

**（4）频率先验依赖**。水印检测需要预先标定策略执行频率 $f_\pi$ 的上下界，以确定频率搜索范围 $\mathcal{F}_{\text{search}}$。当这些先验信息不可靠时，搜索范围扩大将增加虚警概率并降低检测可靠性。

### 对抗鲁棒性的经验边界

CoNoCo 在面对主动攻击时展现出不对称的鲁棒性。**加性噪声攻击**在 HalfCheetah 上即使 $\sigma_{\text{adv}} = 2$ 也未能完全消除检测，但在 Inverted Pendulum 上 $\sigma_{\text{adv}} = 0.25$ 就已同时严重降低检测和策略回报（Figure 10）——这说明攻击代价与任务动力学密切相关，高自由度系统中的噪声被自然分散。**带阻滤波攻击**在减弱水印的同时导致策略行为失真（MSE 增加 257%，Figure 11），攻击者面临检测规避与策略效用之间的尖锐权衡。**结构化干扰信号**无法在不依赖密钥的情况下抵消水印，因为不同种子生成的信号功率相加而非相消（Figure 12）。这些结果表明 CoNoCo 在当前攻击模型下具有实用层面的鲁棒性，但对通过强化学习精确学习的对抗性带宽感知攻击的鲁棒性上限仍是开放问题。

### 开放问题

1. **确定性策略扩展**：如何将 CoNoCo 的频域水印思路扩展到确定性控制策略？可能的路径包括引入受控的伪随机抖动或利用环境交互中的自然变异。
2. **遮挡与多对象场景**：在机器人部分被遮挡或存在多个运动对象时，如何鲁棒地提取有效的运动 glimpse？这需要超越当前模板匹配方法的计算机视觉技术。
3. **蒸馏攻击的可行性**：能否在不依赖训练数据分布的情况下，通过行为克隆或蒸馏反向推导并去除水印？这涉及水印信号是否与策略的“有用”行为在频域上可分离。
4. **对抗性带宽感知攻击的理论上限**：如果攻击者能够通过强化学习精确学习在秘密频带内注入抵消信号，CoNoCo 的检测性能是否存在理论上的下界？当前的结构化干扰分析仅覆盖了无密钥场景。



## 原文 PDF

![[paperPDFs/ICLR_2026/Remotely_Detectable_Robot_Policy_Watermarking.pdf]]
