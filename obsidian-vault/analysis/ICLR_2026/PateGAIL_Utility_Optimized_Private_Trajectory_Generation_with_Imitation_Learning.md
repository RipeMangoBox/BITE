---
title: "PateGAIL++: Utility Optimized Private Trajectory Generation with Imitation Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PateGAIL_Utility_Optimized_Private_Trajectory_Generation_with_Imitation_Learning.pdf
project_link: null
code_link: null
openreview_forum_id: Oyfz6G0hmc
aliases:
- PUOPTGIL
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "引入基于本地判别器置信度的样本级敏感度估计，自适应分配每样本的隐私预算，使高敏感样本获得更强保护（更小隐私预算），低敏感样本减少噪声注入，从而在固定总隐私预算下优化隐私-效用权衡。"
primary_logic: "利用生成对抗模仿学习框架中，本地判别器对生成状态-动作对的评分（接近1表示高度相似于真实用户行为）作为隐私敏感度的代理信号，实现细粒度的、可解释的隐私预算控制，并结合WGAN-GP稳定训练，显著提升轨迹合成保真度与抗攻击能力。"
claims:
- "PateGAIL++ 引入敏感度感知的噪声注入模块，动态调整噪声水平。"
- "在Geolife数据集上，中等噪声（0.10）下PateGAIL++将DailyLoc误差降低约29%，且排名误差大幅下降。"
- "白盒成员推断攻击下，PateGAIL++的AUC接近随机猜测（0.4962），远低于PATEGAIL的0.7208。"
- "Geolife (no noise) 上 G-Rank = 0.0256"
---

# PateGAIL++: Utility Optimized Private Trajectory Generation with Imitation Learning

> [!tip] 核心洞察
> 利用生成对抗模仿学习框架中，本地判别器对生成状态-动作对的评分（接近1表示高度相似于真实用户行为）作为隐私敏感度的代理信号，实现细粒度的、可解释的隐私预算控制，并结合WGAN-GP稳定训练，显著提升轨迹合成保真度与抗攻击能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PateGAIL++：基于模仿学习的效用优化隐私轨迹生成 |
| 英文题名 | PateGAIL++: Utility Optimized Private Trajectory Generation with Imitation Learning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Oyfz6G0hmc) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | PateGAIL++ |
| Dataset | Geolife (no noise), Geolife (noise=0.10), Geolife MIA (noise=0.01), Geolife LDP (noise=0.01) |

> [!tip] 效果简介
> - Geolife (no noise) 上，G-Rank 为 0.0256，对比 0.0387 (MoveSim)，变化 -0.0131。
> - Geolife (noise=0.10) 上，DailyLoc 为 0.4914，对比 0.6915 (PATEGAIL)，变化 -0.2001。
> - Geolife MIA (noise=0.01) 上，White-box AUC 为 0.4962，对比 0.7208 (PATEGAIL)，变化 -0.2246。

## 概要

现有差分隐私轨迹生成方法普遍对所有训练样本施加均匀的隐私保护强度，忽视了轨迹片段因行为独特性而呈现的差异化隐私风险。这一设计造成双重困境：低敏感样本承受了不必要的效用损失，而高敏感样本却未能获得与其风险匹配的充分保护。PateGAIL++ 针对上述瓶颈，提出在生成对抗模仿学习框架内引入**样本级敏感度感知的隐私预算分配机制**，实现细粒度的隐私-效用优化。

核心思路是：利用部署在用户端的本地判别器对生成状态-动作对的置信度评分，作为隐私敏感度的代理信号——判别器评分越接近1，表明该样本与真实用户行为高度相似，隐私风险越高，应分配更小的隐私预算以施加更强的噪声保护。在此基础上，PateGAIL++ 采用 Wasserstein GAN with Gradient Penalty（WGAN-GP）替代标准交叉熵损失以稳定训练，并将框架扩展至本地差分隐私（LDP）场景，消除对可信中心服务器的依赖。

实验表明，在 Geolife 数据集上，当噪声水平为 0.10 时，PateGAIL++ 的 DailyLoc 误差较 PateGAIL 降低约 29%（0.4914 vs. 0.6915），排名指标 G-Rank 和 I-Rank 同样大幅改善。抗攻击能力方面，白盒成员推断攻击下 PateGAIL++ 的 AUC 接近随机猜测水平（0.4962），远低于 PateGAIL 的 0.7208，验证了敏感度感知噪声分配在隐私保护上的实质增益。在用户参与比例降至 40% 的受限条件下，PateGAIL++ 仍保持优于 PateGAIL 的性能弹性。



轨迹数据——即个体在时空中的移动序列——已成为智能交通、城市规划与个性化推荐等应用的核心驱动力。然而，原始轨迹天然携带高度个人化的行为模式，直接将其用于模型训练或数据共享会引发严峻的隐私泄露风险。差分隐私（Differential Privacy, DP）为这一困境提供了理论完备的解决方案，其核心思想是通过向数据或模型梯度注入经校准的随机噪声，使得攻击者无法从输出中可靠推断任意单个样本是否存在于训练集。形式化地，一个随机化算法 $\mathcal{M}$ 满足 $(\varepsilon, \delta)$-差分隐私，当且仅当对于任意相邻数据集 $\mathcal{D}$ 与 $\mathcal{D}'$ 以及任意输出子集 $\mathcal{E}$，有：

$$\mathbb{P}[\mathcal{M}(\mathcal{D}) \in \mathcal{E}] \leq e^{\varepsilon} \cdot \mathbb{P}[\mathcal{M}(\mathcal{D}') \in \mathcal{E}] + \delta$$

其中隐私预算 $\varepsilon$ 越小，保护强度越高，但通常以效用损失为代价。Laplace机制是实现该定义的经典工具，其噪声分布为 $\mathrm{Lap}(x \mid \lambda) = \frac{1}{2\lambda} \exp\left(-\frac{|x|}{\lambda}\right)$，尺度参数 $\lambda$ 由全局敏感度 $\Delta f$ 与隐私预算 $\varepsilon$ 共同决定。

在轨迹生成领域，生成对抗模仿学习（Generative Adversarial Imitation Learning, GAIL）提供了一条从专家轨迹中学习策略的有效路径。GAIL通过一个极小极大博弈联合学习判别器与策略：

$$\min_{\pi_\theta} \max_{D_\phi} \mathbb{E}_{(s,a) \sim \pi_E}[\log D_\phi(s,a)] + \mathbb{E}_{(s,a) \sim \pi_\theta}[\log(1 - D_\phi(s,a))]$$

其中判别器 $D_\phi$ 为策略提供奖励信号，引导生成轨迹逼近专家分布。将差分隐私引入GAIL框架以保护训练数据隐私，催生了**PATEGAIL**（Wang et al., AAAI 2023）等方法。然而，现有差分隐私轨迹生成方法存在一个关键的结构性缺陷：**它们对所有训练样本施加均匀的隐私噪声等级**，完全忽略了不同轨迹片段在行为独特性上的本质差异。

这一缺陷导致了一个双重困境。如Figure 1所示，高度反映用户特异行为的轨迹片段（例如，一条仅由某用户频繁访问的罕见路径）承载着远高于常规路段的隐私风险，却仅获得与低敏感样本同等的噪声保护，使得攻击者仍可能通过成员推断攻击（Membership Inference Attack, MIA）识别其训练集归属。相反，大量行为模式与群体高度重叠的低敏感样本被注入了不必要的过量噪声，导致合成轨迹在空间分布、日常移动模式等关键维度上的保真度严重退化。这种“一刀切”的隐私预算分配策略，在固定总隐私预算的约束下，无法实现隐私与效用之间的最优权衡。

PateGAIL++正是针对上述瓶颈而提出。其核心动机在于：**利用生成对抗框架中本地判别器对生成样本的置信度评分，作为轨迹片段隐私敏感度的可解释代理信号**——当判别器对某个生成状态-动作对的评分接近1时，意味着该样本高度相似于某用户的真实行为，因而具有更高的隐私敏感度。基于这一洞察，PateGAIL++设计了一个敏感度感知的噪声注入模块，能够动态地、自适应地为每个样本分配差异化的隐私预算：高敏感样本获得更小的 $\varepsilon$（更强噪声保护），低敏感样本则减少噪声注入以保留效用。这一机制在理论上维持了总隐私预算不变，却在实践中显著拓展了隐私-效用的帕累托前沿。



## 核心方法与创新机理

PateGAIL++ 的核心创新在于**打破均匀隐私预算分配的范式**，通过三个相互耦合的机制协同解决隐私-效用失衡问题：**敏感度感知的隐私预算分配**、**基于 WGAN-GP 的稳定训练**，以及**向本地差分隐私的自然扩展**。

### 瓶颈诊断：均匀噪声的双重困境

现有差分隐私轨迹生成方法（如 **PATEGAIL**，Wang et al., AAAI 2023）对所有训练样本施加相同的隐私噪声等级。这一均匀策略忽视了不同轨迹样本因行为独特性导致的隐私敏感度差异——用户高度特异化的移动模式（如深夜前往偏僻地点）比常见通勤路线面临更高的成员推断风险。其后果是双重的：低风险样本因过度噪声注入而效用损失严重，高风险样本却因保护不足而易受攻击。PateGAIL++ 正是围绕这一瓶颈展开设计。

### 关键控制变量：判别器置信度作为敏感度代理信号

PateGAIL++ 的核心洞察在于：在生成对抗模仿学习框架中，本地判别器对生成状态-动作对的评分天然携带了隐私敏感度信息。若某轨迹片段的判别器输出接近 1（高度相似于真实用户行为），意味着该模式具有强个人标识性，应被赋予更小的隐私预算（更强的噪声保护）；反之，接近 0.5 的模糊评分表示该行为接近群体共性，可容忍更大预算（更弱噪声）。这一设计将隐私预算分配从一个外部超参数转变为一个**数据驱动、可解释的自适应过程**。

具体而言，每样本的敏感度权重定义为：

$$w(s,a) = 1 - \hat{R}_p(s,a) + \delta'$$

其中 $\hat{R}_p(s,a)$ 为本地判别器的置信度估计。总隐私预算 $\varepsilon$ 按权重比例分配：

$$\varepsilon(s,a) = \frac{\varepsilon \cdot w(s,a)}{\sum_{(s',a') \in \mathcal{D}} w(s',a')}$$

高敏感样本获得更小的 $\varepsilon(s,a)$，在后续奖励聚合中注入更大尺度的 Laplace 噪声，实现细粒度保护。

### 改进槽位一：从均匀分配到敏感度感知的隐私预算分配

| 维度 | PATEGAIL 基线 | PateGAIL++ 改进 |
|------|-------------|----------------|
| 分配策略 | 全体样本均匀分配总隐私预算 | 基于判别器置信度的样本级敏感度自适应分配 |
| 噪声粒度 | 全局统一噪声尺度 | 每样本独立噪声尺度，与敏感度成反比 |
| 保护效果 | 低敏感样本效用损失严重，高敏感样本保护不足 | 高敏感样本获更强保护，低敏感样本减少噪声注入 |

在敏感度感知的奖励聚合阶段，全局奖励的噪声注入遵循：

$$R(s,a) = \frac{1}{N} \sum_{u=1}^{N} R^{(u)}(s,a) + \text{Lap}\left(\frac{\Delta f}{\varepsilon(s,a)}\right)$$

噪声尺度 $\Delta f / \varepsilon(s,a)$ 与每样本预算成反比，确保在固定总隐私预算下实现效用最优的噪声分布。实验证据表明，在 Geolife 数据集中等噪声水平（0.10）下，PateGAIL++ 将 DailyLoc 误差降低约 29%（0.4914 vs. 0.6915），且排名误差大幅下降（G-Rank 0.0278 vs. 0.0512，I-Rank 0.0607 vs. 0.2698）。

### 改进槽位二：从标准 GAN 损失到 WGAN-GP 稳定训练

| 维度 | PATEGAIL 基线 | PateGAIL++ 改进 |
|------|-------------|----------------|
| 训练目标 | 标准 GAN 交叉熵损失 | Wasserstein GAN with Gradient Penalty (WGAN-GP) |
| 训练稳定性 | 易受模式崩溃和梯度消失影响 | 梯度惩罚约束 Lipschitz 连续性，显著提升稳定性 |
| 优化目标 | $\min_\pi \max_D \mathbb{E}[\log D] + \mathbb{E}[\log(1-D)]$ | $\min_\pi \max_D \mathbb{E}[D] - \mathbb{E}[D] - \lambda_{GP} \mathbb{E}[(\|\nabla_{\hat{x}} D\|_2 - 1)^2]$ |

敏感度感知的噪声注入虽然优化了隐私-效用权衡，但引入了奖励信号的异方差性，加剧了策略优化的不稳定性。PateGAIL++ 引入 WGAN-GP 作为对抗训练目标，通过梯度惩罚项强制判别器满足 1-Lipschitz 约束，有效抑制了噪声环境下的训练震荡。消融实验（Table 6, Figure 3）显示，梯度惩罚系数 $\lambda_{GP}=20$ 在各噪声水平下取得最佳轨迹保真度，验证了该改进对噪声环境的适配性。

### 改进槽位三：从中心差分隐私到本地差分隐私的自然扩展

| 维度 | PATEGAIL 基线 | PateGAIL++ 改进 |
|------|-------------|----------------|
| 部署模式 | 仅中心差分隐私（依赖可信服务器） | 扩展至本地差分隐私（LDP），用户端加噪 |
| 信任假设 | 服务器可信，原始数据集中处理 | 无需可信服务器，用户本地保护原始数据 |
| 敏感度机制 | 不适用 | 敏感度感知聚合在 LDP 下仍有效（PateGAIL++⁺） |

PateGAIL++ 将敏感度感知框架自然扩展至本地差分隐私设置。在 LDP 下，每个用户在本地对判别器输出加噪后上传，服务器仅接触扰动后的奖励信号。实验表明，带敏感度感知的 LDP 变体（PateGAIL++⁺）在大多数指标上优于无敏感度感知版本（PateGAIL++⁻），例如在噪声 0.01 下 I-Rank 从 0.1419 降至 0.1158（Table 7）。这一扩展使得 PateGAIL++ 在中心与本地两种隐私模型下均能推动隐私-效用前沿超越 PATEGAIL。

### 隐私保护效果的因果链条

三个改进槽位形成了一条清晰的因果链条：**敏感度感知分配**（改进一）提供了差异化的隐私保护强度，使白盒成员推断攻击的 AUC 从 PATEGAIL 的 0.7208 降至接近随机猜测的 0.4962（Table 4，噪声 0.01）；**WGAN-GP 稳定训练**（改进二）确保了噪声环境下的收敛质量，消融实验证实 $\lambda_{GP}=20$ 为最优配置；**LDP 扩展**（改进三）将保护边界从服务器端前移至用户端，在用户子集减少至 40% 时仍表现出强于 PATEGAIL 的弹性（Table 10）。三者共同实现了固定总隐私预算下的细粒度效用优化与抗攻击能力提升。



![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/002_Figure_2.jpg]]
*Figure 2: PATEGAIL++ framework*

PateGAIL++ 的总体流程围绕**联邦式本地判别器训练 → 敏感度感知的奖励聚合 → 中心策略优化**这一闭环构建，其核心设计目标是在固定总隐私预算下，将噪声从“均匀分配”转变为“按样本敏感度自适应分配”，从而在保护高敏感行为的同时减少低敏感样本的效用损失。

### 框架总览

图 2 展示了 PateGAIL++ 的整体架构。系统由三类角色组成：多个持有私有轨迹数据的用户端、一个负责全局策略更新的中心服务器，以及一个连接两者的安全聚合通道。

**Figure 2: PATEGAIL++ framework.**

### 模块分解与数据流

**① 本地判别器（Local Discriminator）**
每个用户 $u \in \mathcal{U}$ 在本地设备上独立训练一个判别器 $D_{\phi_u}$，其任务是区分真实轨迹与生成器产生的合成轨迹。判别器的输出 $D_{\phi_u}(s,a)$ 即为该用户对状态-动作对 $(s,a)$ 的**本地奖励信号**——值越接近 1，表示该样本越像该用户的真实行为，隐私风险也越高。

**② 敏感度估计模块（Sensitivity Module）**
这是 PateGAIL++ 区别于 PateGail 的核心创新。模块利用本地判别器的置信度作为隐私敏感度的代理信号：样本越被判别器判定为真实（即 $D_{\phi_u}(s,a)$ 接近 1），其行为独特性越强，敏感度越高。敏感度权重定义为：
$$w(s,a) = 1 - \hat{R}_p(s,a) + \delta'$$
其中 $\hat{R}_p(s,a)$ 为经动态补偿后的聚合奖励估计，$\delta'$ 为平滑常数。该权重随后用于分配每样本的隐私预算：
$$\varepsilon(s,a) = \frac{\varepsilon \cdot w(s,a)}{\sum_{(s',a') \in \mathcal{D}} w(s',a')}$$
高敏感样本获得更小的 $\varepsilon(s,a)$（更强的噪声保护），低敏感样本获得更大的预算（更弱的噪声干扰）。

**③ 敏感度感知奖励聚合（Sensitivity-Aware Reward Aggregation）**
服务器收集各用户本地判别器对同一 $(s,a)$ 的奖励值 $R^{(u)}(s,a)$，计算均值后注入与样本敏感度成反比的 Laplace 噪声：
$$R(s,a) = \frac{1}{N}\sum_{u=1}^{N} R^{(u)}(s,a) + \text{Lap}\left(\frac{\Delta f}{\varepsilon(s,a)}\right)$$
噪声尺度 $\Delta f / \varepsilon(s,a)$ 随敏感度升高而增大，实现了细粒度的隐私预算消耗。为进一步稳定训练，框架引入**动态补偿项**，减去奖励方差估计的缩放值：
$$\hat{R}(s,a) = R(s,a) - \beta \cdot \xi(s,a), \quad \xi(s,a) = \sqrt{\text{Var}(R^{(u)}(s,a)) + \text{Lap}(0, \Delta f/\varepsilon(s,a))}$$

**④ PPO 策略优化与 WGAN-GP 训练**
最终经差分隐私扰动的奖励 $\hat{R}(s,a)$ 被送入 PPO（Proximal Policy Optimization）算法，更新全局策略 $\pi_\theta(a|s)$。为缓解标准 GAN 训练的不稳定性，PateGAIL++ 将判别器-生成器的对抗目标替换为 **Wasserstein GAN with Gradient Penalty (WGAN-GP)**：
$$\min_{\pi_\theta} \max_{D_\phi} \mathbb{E}_{(s,a)\sim\pi_E}[D_\phi(s,a)] - \mathbb{E}_{(s,a)\sim\pi_\theta}[D_\phi(s,a)] - \lambda_{GP}\mathbb{E}_{\hat{x}}[(\|\nabla_{\hat{x}}D_\phi(\hat{x})\|_2 - 1)^2]$$
梯度惩罚项强制判别器满足 1-Lipschitz 约束，使训练在噪声环境下仍能保持稳定收敛。

### 隐私保护模式扩展

PateGAIL++ 同时支持两种差分隐私部署模式：
- **中心差分隐私（CDP）**：上述流程的默认模式，用户上传本地奖励至可信服务器进行噪声聚合。
- **本地差分隐私（LDP）**：用户端在发送奖励前自行注入 Laplace 噪声，无需依赖可信服务器。其敏感度感知变体记为 **PateGAIL++⁺**，在 LDP 设置下仍能保持对非敏感度感知版本（PateGAIL++⁻）的性能优势。



### 3.1 本地判别器与敏感度感知机制

PateGAIL++ 的核心创新在于引入**样本级敏感度估计**，打破传统差分隐私方法对所有训练样本均匀分配隐私预算的刚性约束。其因果机制如下：

每个用户 $u \in \mathcal{U}$ 在本地维护一个判别器 $D_{\phi_u}$，该判别器在设备端独立训练，用于区分真实轨迹与生成轨迹。判别器对状态-动作对 $(s,a)$ 的输出评分 $D_{\phi_u}(s,a)$ 反映了该样本与真实用户行为的相似程度——评分越接近 1，表明该样本越能体现用户特有的行为模式，因而具有更高的隐私敏感度。

基于此，敏感度权重定义为判别器置信度的反函数：

$$
w(s,a) = 1 - \hat{R}_p(s,a) + \delta'
$$

其中 $\hat{R}_p(s,a)$ 为本地判别器经动态补偿后的奖励信号，$\delta'$ 为小常数防止权重归零。该权重直接驱动**每样本隐私预算分配**：

$$
\varepsilon(s,a) = \frac{\varepsilon \cdot w(s,a)}{\sum_{(s',a') \in \mathcal{D}} w(s',a')}
$$

**公式变量含义**：$\varepsilon$ 为总隐私预算，$\mathcal{D}$ 为当前批次的状态-动作对集合。高敏感样本（$w(s,a)$ 大）获得更小的 $\varepsilon(s,a)$ 值，意味着注入更强的 Laplace 噪声；低敏感样本则保留更多信号，从而在固定总预算下优化隐私-效用权衡。

---

### 3.2 敏感度感知奖励聚合

全局奖励的聚合过程直接利用上述每样本隐私预算。服务器收集各用户的本地奖励 $R^{(u)}(s,a)$ 后，执行敏感度感知的噪声注入：

$$
R(s,a) = \frac{1}{N} \sum_{u=1}^{N} R^{(u)}(s,a) + \mathbf{Lap}\left(\frac{\Delta f}{\varepsilon(s,a)}\right)
$$

**公式变量含义**：$N$ 为用户总数，$\Delta f$ 为全局敏感度（奖励函数的输出范围），$\mathbf{Lap}(\cdot)$ 为 Laplace 噪声，其尺度参数与 $\varepsilon(s,a)$ 成反比——敏感度越高的样本，噪声尺度越大。

为进一步稳定训练，引入**动态补偿项**以抑制本地判别器输出的高方差：

$$
\hat{R}(s,a) = R(s,a) - \beta \cdot \xi(s,a)
$$

其中：

$$
\xi(s,a) = \sqrt{\mathrm{Var}(R^{(u)}(s,a)) + \mathbf{Lap}\left(0, \frac{\Delta f}{\varepsilon(s,a)}\right)}
$$

$\beta$ 为补偿系数，$\mathrm{Var}(\cdot)$ 为本地奖励的方差。该补偿项对判别器输出波动大的样本施加惩罚，防止策略被噪声误导。

---

### 3.3 WGAN-GP 稳定训练

PateGAIL++ 将标准 GAIL 的交叉熵对抗损失替换为 **Wasserstein GAN with Gradient Penalty (WGAN-GP)**，以缓解差分隐私噪声环境下的训练不稳定问题。优化目标为：

$$
\operatorname*{min}_{\pi_\theta} \operatorname*{max}_{D_\phi} \mathbb{E}_{(s,a) \sim \pi_E} [D_\phi(s,a)] - \mathbb{E}_{(s,a) \sim \pi_\theta} [D_\phi(s,a)] - \lambda_{GP} \mathbb{E}_{\hat{x}} [(\|\nabla_{\hat{x}} D_\phi(\hat{x})\|_2 - 1)^2]
$$

**公式变量含义**：$\pi_E$ 为专家（真实）策略，$\pi_\theta$ 为生成策略，$\hat{x}$ 为真实样本与生成样本之间的随机插值点，$\lambda_{GP}$ 为梯度惩罚系数。梯度惩罚项强制判别器满足 1-Lipschitz 约束，确保 Wasserstein 距离的有效估计。消融实验表明，$\lambda_{GP}=20$ 在噪声环境中取得最佳轨迹保真度。

---

### 3.4 隐私保护部署模式

PateGAIL++ 支持两种部署模式：

- **中心差分隐私（CDP）**：依赖可信服务器聚合本地奖励并注入噪声，上述模块均在此设定下运行。
- **本地差分隐私（LDP）**：将噪声注入下沉至用户端，无需可信服务器。LDP 变体记为 $\mathrm{PATEGAIL++}^+$，其在用户端执行敏感度感知的噪声注入后再上传加噪奖励，服务器仅执行简单聚合。

两种模式均通过敏感度感知分配机制优化隐私-效用前沿，LDP 扩展使框架在去中心化场景下仍能保持竞争力。



## 实验与关键发现

### 实验设置

实验在两个真实轨迹数据集上进行：**Geolife**（个体级GPS轨迹）和**Telecom Shanghai**（基站级移动记录）。评估指标覆盖空间保真度（DailyLoc、Distance、Radius）和序列排序质量（G-Rank、I-Rank）。隐私保护有效性通过白盒成员推断攻击（White-box MIA）和黑盒LiRA攻击评估，攻击者利用判别器奖励信号构建特征向量训练随机森林分类器。基线方法包括 **GAN**（Goodfellow et al., 2020）、**SeqGAN**（Yu et al., 2017）、**TimeGeo**（Jiang et al., 2016）、**MoveSim**（Feng et al., 2020）、**DiffTraj**（Zhu et al., 2023）以及直接对比对象 **PATEGAIL**（Wang et al., AAAI 2023）。

### 主实验结果

**无噪声条件下**，PateGAIL++ 展现出与当前最优方法相当的轨迹合成能力。如表1所示，G-Rank 达到 0.0256，优于 MoveSim 的 0.0387；I-Rank 为 0.0176，与 MoveSim 的 0.0173 持平。这表明在纯效用维度上，该方法并未因引入隐私机制而牺牲生成质量。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/003_Table_1.jpg]]
*Table 1: Comparison results with baselines. Approaches were implemented without noise on the training data, and the results of PATEGAIL and PATEGAIL++ are identical when the noise level is 0*

**噪声环境下的效用增益**构成核心证据。在 Geolife 数据集上，当噪声水平为 0.10 时，PateGAIL++ 的 DailyLoc 误差为 0.4914，相比 PATEGAIL 的 0.6915 降低约 29%；G-Rank 从 0.0512 降至 0.0278，I-Rank 从 0.2698 大幅降至 0.0607（表2）。这一改进源于敏感度感知的隐私预算分配——低敏感样本获得更少的噪声注入，保留了更多有用信号。Telecom Shanghai 数据集上的趋势一致（表3），验证了方法的跨场景泛化性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/004_Table_2.jpg]]
*Table 2: Comparison of PATEGAIL vs. PATEGAIL++ at various noise levels under Geolife dataset. PATEGAIL++ consistently outperforms PATEGAIL in DailyLoc, G-Rank and I-Rank*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/005_Table_3.jpg]]
*Table 3: Comparison of PATEGAIL and PATEGAIL++ at various noise levels under the Telecom Shanghai dataset*

**抗成员推断攻击能力**是隐私保护的核心检验。白盒MIA下，PateGAIL++ 在噪声 0.01 时 AUC 为 0.4962，接近随机猜测的 0.5，而 PATEGAIL 的 AUC 高达 0.7208（表4）。LiRA 黑盒攻击下，攻击准确率从 PATEGAIL 的 0.7000 降至 0.6088（噪声 0.01，表5）。关键机制在于：敏感度感知分配使高敏感样本获得更小的隐私预算（更强噪声），攻击者难以从这些样本的奖励信号中提取成员信息。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/006_Table_4.jpg]]
*Table 4: Comparison of white-box MIA performance against PATEGAIL and PATEGAIL++ under different noise levels (70% members, 30% non-members) using Geolife dataset*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/007_Table_5.jpg]]
*Table 5: Comparison of LiRA performance against PATEGAIL and PATEGAIL++ under different noise levels using Geolife dataset*

### 消融研究

**WGAN-GP 梯度惩罚系数 λGP** 对性能有显著影响。消融实验（表6）显示，λGP=20 在噪声环境中取得最佳轨迹保真度，验证了 Wasserstein 距离配合梯度惩罚对稳定差分隐私训练的贡献。图3进一步表明，最优配置的 PateGAIL++ 在不同噪声水平下均一致优于 PATEGAIL。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/008_Table_6.jpg]]
*Table 6: Ablation study of different λGP levels across noise levels*

**用户参与比例**的鲁棒性测试（表10）揭示：当用户子集减少至 40% 时，PateGAIL++ 的性能下降幅度通常小于 PATEGAIL。这归因于敏感度感知机制使有限用户的高质量样本得到更充分的利用，表现出更强的弹性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/013_Table_10.jpg]]
*Table 10: Performance comparison across different user percentages (40%, 80%, 100%) under varying noise levels. ues compared to PATEGAIL. This highlights PATEGAIL++’s stronger resilience under limited user availability*

### 本地差分隐私扩展

PateGAIL++ 进一步扩展至本地差分隐私（LDP）场景。表7显示，敏感度感知聚合变体 PateGAIL++⁺ 在噪声 0.01 时 I-Rank 为 0.1158，优于无敏感度感知的 PateGAIL++⁻（0.1419）。在中心和本地两种设置下，PateGAIL++ 均将隐私-效用前沿推至 PATEGAIL 之上。

### 失败模式与局限性

当前敏感度模型主要依赖判别器置信度作为代理信号，尚未整合位置特定的长期风险信号（如医院等高风险位置）。这可能导致对某些语义敏感但行为常见的轨迹片段保护不足。此外，每用户训练一个本地判别器的设计在用户数量极大时的计算开销需要进一步评估。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/009_Table.jpg]]
*Table: \mathrm { P A T E G A I L + + } ^ { + } achieves comparable or superior performance to \mathrm { P A T E G A I L ^ { + + } } ^ { - } across most settings. Moreover, PATEGAIL++ consistently pushes the privacy–utility frontier beyond PATEGAIL in both central and local settings*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/010_Table_8.jpg]]
*Table 8: Comparison of white-box MIA performance against PATEGAIL and PATEGAIL++ under different noise levels (70% members, 30% non-members) using Telecom Shanghai dataset*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_Oyfz6G0hmc/figures/011_Table_9.jpg]]
*Table 9: Comparison of LiRA performance against PATEGAIL and PATEGAIL++ under different noise levels using Telecom Shanghai dataset*



## 定位与知识库关联

PateGAIL++ 建立在差分隐私轨迹生成与生成对抗模仿学习两条技术路线的交叉点上。其直接前身 **PATEGAIL**（Wang et al., AAAI 2023）首次将 PATE（Private Aggregation of Teacher Ensembles）框架引入模仿学习，通过多个本地判别器提供隐私保护下的奖励信号。然而，PATEGAIL 对所有训练样本施加均匀的隐私预算，忽视了轨迹片段之间天然的敏感度差异——某些高度个性化的行为模式（如深夜前往特定地点）比常见通勤路线承载更高的隐私风险。这一瓶颈构成了 PateGAIL++ 的核心改进动机。

### 与基线的差异化定位

PateGAIL++ 在方法谱系中的位置可通过三个关键改进槽位来界定：

**1. 隐私预算分配：从均匀到敏感度自适应**

PATEGAIL 及此前的差分隐私轨迹生成方法（如基于 DP-SGD 的 GAN 变体）均采用全局统一的隐私预算。PateGAIL++ 引入基于本地判别器置信度的样本级敏感度估计：当判别器对生成的状态-动作对给出接近 1 的评分时，表明该样本高度模仿了真实用户行为，因此具有更高的隐私敏感度，应分配更小的隐私预算（即注入更强噪声）。具体而言，每样本隐私预算分配遵循：

$$\varepsilon(s, a) = \frac{\varepsilon \cdot w(s, a)}{\sum_{(s', a') \in \mathcal{D}} w(s', a')}, \quad \text{where } w(s, a) = 1 - \hat{R}_p(s, a) + \delta'$$

这一机制将总隐私预算从均匀分配转变为与敏感度成反比的加权分配，在固定总预算下实现了更精细的隐私-效用权衡。

**2. 训练稳定性：从标准 GAN 到 WGAN-GP**

PATEGAIL 采用标准 GAN 的交叉熵损失，在噪声环境下易出现训练不稳定和模式坍塌。PateGAIL++ 将训练目标替换为 Wasserstein GAN with Gradient Penalty（WGAN-GP），最小化 Wasserstein-1 距离：

$$\min_{\pi_\theta} \max_{D_\phi} \mathbb{E}_{(s,a) \sim \pi_E} [D_\phi(s,a)] - \mathbb{E}_{(s,a) \sim \pi_\theta} [D_\phi(s,a)] - \lambda_{GP} \mathbb{E}_{\hat{x}} [(\|\nabla_{\hat{x}} D_\phi(\hat{x})\|_2 - 1)^2]$$

消融实验表明，梯度惩罚系数 $\lambda_{GP} = 20$ 在噪声环境中取得最佳轨迹保真度（Table 6），且 WGAN-GP 的引入使 PateGAIL++ 在用户参与比例降至 40% 时仍表现出比 PATEGAIL 更强的弹性（Table 10）。

**3. 部署模式：从中心差分隐私到本地差分隐私**

PATEGAIL 仅支持中心差分隐私（CDP）模式，依赖可信服务器聚合用户数据。PateGAIL++ 将框架扩展至本地差分隐私（LDP）设置，用户在本地端完成噪声注入后再上传，消除了对可信第三方的依赖。LDP 变体（记为 PateGAIL++⁺）在大多数指标上达到或超越无敏感度感知的 LDP 基线（PateGAIL++⁻），例如在噪声水平 0.01 时 I-Rank 从 0.1419 降至 0.1158（Table 7）。

### 与其他轨迹生成方法的边界

在无噪声条件下，PateGAIL++ 与 **MoveSim**（Feng et al., 2020）、**DiffTraj**（Zhu et al., 2023）等非隐私方法进行了对比（Table 1）。其 G-Rank 达到 0.0256，优于 MoveSim 的 0.0387，表明即使在未注入隐私噪声时，GAIL 框架本身已具备较强的轨迹分布建模能力。然而，这些非隐私基线（包括 **GAN**、**SeqGAN**、**TimeGeo**）不提供任何隐私保证，与 PateGAIL++ 的目标场景存在根本性差异——PateGAIL++ 的核心价值恰在于隐私约束下的效用保持。

### 适用边界与开放问题

PateGAIL++ 的敏感度估计依赖于本地判别器的置信度信号，这意味着其有效性受限于判别器的校准质量。在用户数据极度稀疏或行为模式高度同质化的场景中，判别器可能无法提供有区分度的敏感度信号，导致自适应分配退化为近似均匀分配。此外，当前敏感度模型仅考虑行为模式的独特性，未纳入位置本身的语义风险（如医院、军事区域等敏感场所）。

论文明确指出的开放问题是：“如何开发更细致的敏感度模型，结合位置特定和长期风险信号以进一步提升隐私-效用平衡”。这一方向指向将静态位置语义与动态行为模式融合的多维敏感度建模，可能涉及知识图谱或预训练位置嵌入的引入，但论文未提供具体方案，需后续工作探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/PateGAIL_Utility_Optimized_Private_Trajectory_Generation_with_Imitation_Learning.pdf]]
