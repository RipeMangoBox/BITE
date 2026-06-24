---
title: "EARS: Efficiency-aware Russian Roulette and Splitting"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/EARS_Efficiency_aware_Russian_Roulette_and_Splitting.pdf
project_link: "https://graphics.cg.uni-saarland.de/publications/rath-sig2022.html"
code_link: "https://github.com/iRath96/ears"
aliases:
- EEARRS
- EARS
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 通过一个可证明收敛的固定点迭代，利用局部和全局的方差与成本估计，直接计算出最大化渲染效率的RRS因子（每个前缀路径的生存概率或分裂数量）。
primary_logic: 渲染效率定义为方差与成本乘积的倒数；通过将RRS决策视为一个连续优化问题并推导固定点迭代公式，可以在渲染过程中在线学习最优的RRS因子，将计算量集中在造成图像噪声的路径区域（如焦散），从而实现比现有启发式方法更优的时间-质量权衡。
claims:
- 所提方法在五个测试场景上平均比ADRRS加速1.6倍，在厨房场景加速达4.3倍。
- 固定点迭代在给定真实方差与成本的条件下，被证明收敛到全局最优RRS因子。
- 使用相对均方误差（relMSE）代替绝对MSE作为优化目标，显著改善高动态范围场景的采样分布和收敛效果。
- Pool scene (Fig. 1) 上 qualitative relMSE after 10min = EARS (RRS) 显著降低误差，焦散处更清晰
---

# EARS: Efficiency-aware Russian Roulette and Splitting

> [!tip] 核心洞察
> 渲染效率定义为方差与成本乘积的倒数；通过将RRS决策视为一个连续优化问题并推导固定点迭代公式，可以在渲染过程中在线学习最优的RRS因子，将计算量集中在造成图像噪声的路径区域（如焦散），从而实现比现有启发式方法更优的时间-质量权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | EARS: 效率感知的俄罗斯轮盘赌与分裂 |
| 英文题名 | EARS: Efficiency-aware Russian Roulette and Splitting |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://graphics.cg.uni-saarland.de/publications/rath-sig2022.html) · [Code](https://github.com/iRath96/ears) · [Project](https://prime-itn.eu/) |
| Topic | #topic/other_unclear |
| Method | EARS (Efficiency-Aware Russian Roulette and Splitting) |
| Dataset | Pool scene, Kitchen scene, All five test scenes, Modern Living Room |

> [!tip] 效果简介
> - Pool scene (Fig. 1) 上，qualitative relMSE after 10min EARS (RRS) 显著降低误差，焦散处更清晰 vs ADRRS (视觉上更优)。
> - Kitchen scene 上，speed-up (equal-time relMSE) 4.3× over ADRRS vs ADRRS (+4.3×)。
> - All five test scenes 上，average speed-up vs ADRRS 1.6× vs ADRRS (+1.6×)。

## 概要

**问题瓶颈**：现有俄罗斯轮盘赌与分裂（RRS）方法（如 ADRRS）仅依据路径的期望贡献做终止/分裂决策，完全忽略了局部方差和计算成本，导致计算资源无法精准投向真正造成图像噪声的路径区域，渲染效率受限。

**核心方法**：本文提出 **EARS（Efficiency-Aware Russian Roulette and Splitting）**，将 RRS 决策形式化为一个连续优化问题——直接最小化图像平均相对方差与平均每像素成本的乘积（即最大化渲染效率）。通过推导一个可证明收敛的固定点迭代公式，EARS 在渲染过程中在线学习每个前缀路径的最优生存概率或分裂数量，将计算量自动集中到焦散等高方差路径上。

**主要结果**：在五个测试场景上，EARS 平均比 ADRRS 加速 **1.6 倍**，在 Kitchen 场景加速达 **4.3 倍**。使用相对均方误差（relMSE）替代绝对 MSE 作为优化目标，显著改善了高动态范围场景的采样分布和收敛质量。

**方法定位**：EARS 首次将 RRS 决策从启发式规则提升为有收敛保证的效率最优框架，填补了基于方差-成本联合优化的 RRS 方法空白，为蒙特卡洛路径追踪的自适应采样提供了新的理论基础。

## 核心方法与创新机理

### 问题瓶颈与优化目标的重新定义

传统俄罗斯轮盘赌与分裂（RRS）方法——尤其是作为主要对比基线的**ADRRS**（Vorba and Křivánek, ACM Trans. Graph. 2016）——仅依据路径前缀的期望贡献（即入射辐射度估计）来决定终止或分裂。这一策略的根本缺陷在于：它忽略了局部估计的**方差**和**计算成本**，导致大量计算资源被浪费在低方差区域，而真正造成图像噪声的高方差区域（如焦散路径）反而采样不足。

EARS 的核心洞察在于将 RRS 决策重新表述为一个**效率最大化问题**。渲染的逆效率定义为平均像素方差与平均像素成本的乘积：

$$\epsilon^{-1} = \left(\frac{1}{N_{\mathrm{px}}}\sum_{\mathrm{px}}\mathbb{V}[\langle I_{\mathrm{px}}\rangle]\right) \left(\frac{1}{N_{\mathrm{px}}}\sum_{\mathrm{px}}\mathbb{E}[c(\langle I_{\mathrm{px}}\rangle)]\right)$$

优化目标是最小化该乘积，即最大化效率。在实际渲染中，由于绝对 MSE 会导致对高亮度像素的过度采样（见 Fig. 4），EARS 改用**相对均方误差（relMSE）**作为优化目标：

![[assets/figures/papers/paper_list_l31_https_graphics_cg_uni_saarland_de_publications_rath_sig2022_html/figures/003_Figure_4.jpg]]
*Figure 4: Minimizing the mean-squared error (MSE) or relative MSE (relMSE) in EARS. Using the relMSE performs significantly better in scenes with high contrast. By decreasing the exposure (EV -6) of a crop we can see that using the MSE oversamples very bright regions. Using the relMSE, on the other hand, yields better convergence across the entire dynamic range of the image, as we can see when looking at the average per-pixel cost, shown in false-color. With the MSE, most computation time is invested in the bright pixels. With the relMSE, computation time is spread more evenly*

$$\bar{V}(n)\bar{C}(n) = \left(\frac{1}{N_{\mathrm{px}}}\sum_{\mathrm{px}}\frac{\mathbb{V}[\langle I_{\mathrm{px}};n\rangle]}{I_{\mathrm{px}}^2}\right) \left(\frac{1}{N_{\mathrm{px}}}\sum_{\mathrm{px}}\mathbb{E}[c(\langle I_{\mathrm{px}};n\rangle)]\right)$$

这一改变使得计算资源在图像动态范围内分布更均匀，显著改善了高对比度场景的收敛质量。

### 核心机制：可证明收敛的固定点迭代

EARS 的方法论核心是一个**固定点迭代公式**，它直接计算每个前缀路径的最优 RRS 因子。该公式将 RRS 决策分解为三个可解释的组成部分：

$$n_i(\bar{\mathbf{x}}_k) = \underbrace{\frac{T(\bar{\mathbf{x}}_k)}{I_{\mathrm{px}}(\bar{\mathbf{x}}_k)}}_{\mathrm{prefix}} \underbrace{\sqrt{\frac{R(\langle L_{\mathrm{r}}(\mathbf{x}_k,\mathbf{x}_{k-1});n_i\rangle)}{\mathbb{E}[c(\langle L_{\mathrm{r}}(\mathbf{x}_k,\mathbf{x}_{k-1});n_i\rangle)]}}}_{\mathrm{local}} \underbrace{\sqrt{\frac{\bar{C}(n_i)}{\bar{V}(n_i)}}}_{\mathrm{global}}$$

其中：
- **前缀项**：路径前缀的累积吞吐量 $T(\bar{\mathbf{x}}_k)$ 与像素真值 $I_{\mathrm{px}}$ 的比值，反映该路径对最终像素的相对重要性；
- **局部项**：当前顶点处后缀估计的二阶矩 $R$（近似方差）与期望成本的比值，反映局部效率；
- **全局项**：全局平均成本 $\bar{C}$ 与全局平均相对方差 $\bar{V}$ 的比值，确保所有路径的 RRS 因子在全局尺度上协调一致。

该公式的推导基于嵌套估计器的方差分解（全方差定律），并利用了分裂方差近似为 $O(1/n)$ 的假设来保持优化问题的凸性。对于联合分裂与俄罗斯轮盘赌，EARS 采用分段固定点函数：

$$\gamma_{\mathrm{RRS}}(s(x)) = \begin{cases} \gamma_{\mathrm{S}}(s(x)) & \text{if } \gamma_{\mathrm{S}}(s(x)) > 1 \\ \min\{\gamma_{\mathrm{RR}}(s(x)),1\} & \text{otherwise} \end{cases}$$

当计算出的分裂因子大于 1 时执行分裂，否则执行 RR 且因子不超过 1。该联合目标被证明是**凸的**（见 Fig. 3），且固定点迭代在给定真实方差与成本的条件下**可证明收敛到全局最优**（附录 C 提供了完整证明）。

![[assets/figures/papers/paper_list_l31_https_graphics_cg_uni_saarland_de_publications_rath_sig2022_html/figures/004_Figure_3.jpg]]
*Figure 3: Examples visualizing the shape of our objective function, here in 1D for a single point ?? with corresponding ?? (??). The splitting (blue) and RR (orange) objectives are both convex and have a unique local minimum (vertical lines). There are three possible cases, shown from left to right: RR is optimal, doing neither is optimal, and splitting is optimal. By definition, the RR objective and the splitting objective intersect at*

### 三个关键 Changed Slots

相较于基线方法，EARS 在以下三个关键决策槽位上进行了根本性改变：

**1. RRS 决策输入**（从期望贡献到方差-成本联合）
ADRRS 仅使用路径前缀的入射辐射度估计作为决策依据。EARS 将输入扩展为局部二阶矩、局部成本、全局平均方差和成本的组合，通过固定点迭代公式综合计算。这使得决策能够识别“高方差但低贡献”的关键路径（如焦散），并在此处集中分裂资源。

**2. 优化目标函数**（从启发式到效率最大化）
传统方法间接地最大化路径未终止概率或依赖手工参数。EARS 直接最小化图像平均相对方差与平均每像素成本的乘积，将 RRS 决策纳入一个严格的数学优化框架。

**3. 分裂因子优化**（从手工规则到迭代固定点更新）
ADRRS 的分裂决策基于局部成本/方差的简单启发式。EARS 通过固定点迭代自动平衡局部与全局效率，无需手工调参即可适应不同场景特性。

### 管线模块与因果链路

EARS 的完整渲染管线由五个模块构成，形成闭环在线学习系统：

**模块 1：relMSE 目标计算**
在每次迭代中，系统计算全局平均相对方差 $\tilde{V}$ 和平均成本 $\tilde{C}$，作为效率优化的全局协调信号。该模块输出的比值 $\sqrt{\bar{C}/\bar{V}}$ 直接进入固定点更新公式的全局项。

**模块 2：5D 空间-方向缓存（八叉树 + 方向直方图）**
场景被八叉树空间分割，每个叶节点存储方向离散化的直方图（见 Fig. 6）。每个空间-方向 bin 维护局部方差、二阶矩和成本估计。该缓存是局部项 $\sqrt{R/\mathbb{E}[c]}$ 的数据来源，其精度直接影响固定点迭代的收敛质量。在低样本数时，离散化估计不足会导致视觉伪影（Fig. 11）。

![[assets/figures/papers/paper_list_l31_https_graphics_cg_uni_saarland_de_publications_rath_sig2022_html/figures/006_Figure_6.jpg]]
*Figure 6: The data structure used by our implementation. The scene is divided by an octree (left). Each cell of which stores variance estimates for the reflected radiance estimator. The directional dependency on*

**模块 3：固定点迭代更新**
在每个前缀路径处，系统从缓存中查询局部统计量，结合全局效率比例，通过公式 (29) 计算该路径的最优 RRS 因子。该模块是方法的核心——它将全局效率目标与局部路径特性耦合，因果链为：**缓存统计量 → 局部效率比 → 全局效率比 → 最优 RRS 因子**。

**模块 4：随机舍入与 RRS 估计器**
实数 RRS 因子通过随机舍入转换为整数分裂数：

$$r(s(\bar{\mathbf{x}}_k)) = \begin{cases} \lfloor s(\bar{\mathbf{x}}_k)\rfloor + 1 & \text{with prob. } s(\bar{\mathbf{x}}_k)-\lfloor s(\bar{\mathbf{x}}_k)\rfloor \\ \lfloor s(\bar{\mathbf{x}}_k)\rfloor & \text{otherwise} \end{cases}$$

这保证了嵌套 RRS 估计器的无偏性。分裂后的路径通过权重 $1/s(\bar{\mathbf{x}}_k)$ 归一化，形成递归的路径追踪估计器。

**模块 5：迭代渲染循环**
整个系统交替进行路径追踪采样、缓存统计更新和 RRS 因子应用。初始迭代使用均匀 RRS 因子进行训练，随后每次迭代利用上一轮积累的方差/成本估计更新因子，逐步收敛到最优采样分布。Fig. 5 展示了焦散路径上三个嵌套估计器在初始训练、第一次和第二次固定点迭代中的采样行为演变——分裂逐渐集中在高方差的后缀区域。

![[assets/figures/papers/paper_list_l31_https_graphics_cg_uni_saarland_de_publications_rath_sig2022_html/figures/005_Figure_5.jpg]]
*Figure 5: Illustration of the fixed-point update behavior for a set of nested estimators (blue, green, and orange) along a caustic path. (a) shows the scene setup, which is similar to the Pool scene (Fig. 1). The yellow region marks the subset of paths that constitute the caustic. (b), (c), and (d) show the sampling behavior (top) and the estimated variances and costs (bottom) of the nested estimators at different stages: the initial training iteration (b) as well as the first (c), and second (d) fixed-point iteration*

### 训练与推理路径

EARS 的“训练”与“推理”并非分离阶段，而是**交织在同一渲染过程中**。初始阶段使用默认 RRS 因子进行采样以收集统计量（训练），随后每次固定点迭代更新因子并继续采样（推理），形成在线学习闭环。这种设计使得方法无需预计算或场景特定的参数调整，即可自适应地优化采样分布。收敛性保证（附录 C）确保了迭代过程稳定趋向最优效率配置。

![[assets/figures/papers/paper_list_l31_https_graphics_cg_uni_saarland_de_publications_rath_sig2022_html/figures/001_Figure_1.jpg]]
*Figure 1: We derive a fixed-point iteration to compute the Russian roulette and splitting (RRS) factors that maximize the rendering efficiency. Here, we compare the rendered images in equal-time (10 min) of our method and the state of the art, adjoint-driven Russian roulette and splitting (ADRRS) [Vorba and Křivánek 2016]. The false-color images on the right visualize the average RRS factors in each pixel at the second and third bounce. Red indicates that mostly roulette is played; blue indicates that mostly splitting is done. By directly optimizing variance and cost, our method produces more efficient RRS decisions: splitting is mostly performed at the bottom of the pool and on the diffuse surface b...*

## 实验与关键发现

### 整体性能：与 ADRRS 的等时对比

EARS 在五个测试场景上以 10 分钟等时渲染为基准，与当前最优方法 ADRRS（Vorba and Křivánek, 2016）进行全面对比。**核心结论是：EARS 平均加速 1.6 倍，在个别场景加速高达 4.3 倍**。

具体而言，在 Kitchen 场景上 EARS RRS 达到 ADRRS 的 4.3 倍加速；在 Bookshelf 场景上，仅使用俄罗斯轮盘赌的 EARS RR 比 ADRR（无分裂版本）快 30%，而完整的 EARS RRS 比 ADRRS 快约 2 倍。这些加速来自于 EARS 将计算资源集中到真正造成图像噪声的路径区域——例如 Pool 场景中的池底焦散和窗后漫反射表面（Fig. 1, Fig. 7）。

![[assets/figures/papers/paper_list_l31_https_graphics_cg_uni_saarland_de_publications_rath_sig2022_html/figures/007_Figure_7.jpg]]
*Figure 7: We render five scenes with different Russian roulette and splitting strategies for 10 minutes each. The numbers below the crops are the relative mean-squared error (relMSE, lower is better), with the speed-up compared to classic RR in parentheses (higher is better)*

Table 1 提供了关键的定量统计。以 Modern Living Room 场景为例，在相同 10 分钟渲染时间内，EARS RRS 仅需 274 SPP（samples per pixel），而 ADRRS 需要 1147 SPP——**EARS 用 4.2 倍更少的样本达到了相当或更优的误差水平**。这直接体现了效率提升：EARS 的每条路径成本更高（因为分裂增加了计算量），但通过将分裂集中在高方差区域、在低方差区域积极执行轮盘赌终止，整体渲染效率显著提升。

### 效率收敛行为

Fig. 9 展示了 Veach Door 场景中成本、方差和效率随迭代的收敛曲线。EARS 的成本和方差均收敛到一个固定点，效率（方差与成本乘积的倒数）随之稳定。这验证了固定点迭代在实践中的收敛性，与理论证明一致。相比之下，ADRRS 和经典 RR 的效率曲线在相同时间内未达到同等水平。

### 关键消融：relMSE vs. MSE 目标函数

**使用相对均方误差（relMSE）替代绝对 MSE 是 EARS 在实践中的关键设计选择**。Fig. 4 的消融实验清晰展示了差异：在 EV -6 的曝光下，使用 MSE 优化的 EARS 在极亮区域（如窗边高光）投入了过多的计算资源，导致其他区域噪声严重；而使用 relMSE 的版本将计算时间更均匀地分布在整个动态范围内。false-color 的每像素成本图直观显示：MSE 版本的计算集中在明亮像素，relMSE 版本则更均衡。

这一消融的重要性在于：渲染效率的优化目标定义直接影响资源分配策略。MSE 天然偏向高辐射度像素（因为这些像素的绝对方差更大），而 relMSE 通过除以像素真值的平方，将优化目标归一化到相对误差上，从而避免了对高动态范围场景中亮区的过度采样。

### 方法间的噪声分布特性

Fig. 8 揭示了 EARS 与经典 RR + 自适应采样之间有趣的权衡。在测试场景中，EARS 和 ADRRS 达到了相近的平均 relMSE，但 **EARS 的噪声在图像空间分布更均匀**。经典 RR 结合自适应采样虽然实现了更均匀的噪声分布，但平均误差更高。这说明 EARS 在"降低整体误差"和"均匀化噪声分布"之间取得了更好的平衡——它通过路径空间的 RRS 决策直接针对方差源头，而非依赖图像空间的后验样本分配。

### 失败模式与适用边界

**1. 局部方差过度近似导致的性能退化**

在 Glossy Bathroom 场景中，EARS 的性能比 ADRRS 低 9%。原因是该场景的光泽表面导致局部方差估计的离散化近似不够精确，引发了过度分裂——将过多的路径分裂在并非真正高方差的区域，反而浪费了计算资源。这暴露了 EARS 对缓存估计质量的敏感性：当空间-方向缓存的离散化无法准确捕捉局部方差结构时，固定点迭代可能收敛到次优的 RRS 因子。

**2. 低样本数下的离散化伪影**

Fig. 11 展示了渲染初期因缓存样本不足而产生的视觉伪影。空间缓存（八叉树 + 方向直方图）在未积累足够样本时，方差估计不准确，导致分裂因子计算出现偏差，在图像中形成块状或方向性的不自然噪声模式。这些伪影会随迭代进行逐渐消失，但在极短渲染时间下可能影响视觉质量。

**3. 主射线的激进轮盘赌与局部噪声增大**

Fig. 12 的 Pool 场景放大图揭示了 EARS 的一个重要行为特征：在焦散路径上大量分裂的同时，EARS 对相机出发的主射线执行了激进的轮盘赌终止。这意味着许多从相机出发的路径在首次击中后就可能被终止，导致图像某些区域（如非焦散的漫反射表面）噪声反而增大。这是 EARS 优化策略的直接结果——它将有限的计算预算集中到对整体 relMSE 贡献最大的路径上，代价是牺牲"容易渲染"区域的质量。自适应采样可以通过图像空间的样本重分配缓解这一问题，但 EARS 的路径空间决策无法直接做到这一点。

**4. 双向方法的扩展障碍**

EARS 目前仅在前向路径追踪中实现。扩展到双向路径追踪时面临两个核心挑战：一是 MIS（多重重要性采样）权重中分裂引入的协方差使目标函数失去凸性；二是双向路径的连接策略使得"前缀路径"的定义变得模糊，固定点迭代的嵌套结构不再直接适用。论文明确指出这是一个开放问题，目前无法直接应用。

**5. QMC 采样下的方差假设偏差**

EARS 的优化推导依赖于分裂方差按 O(1/n) 缩放的假设，这在独立随机采样下成立。但在使用 QMC（拟蒙特卡洛）采样时，样本间的相关性会改变方差的缩放行为，可能导致优化目标偏离真实的效率函数。论文承认这一局限性，但实验表明在实际渲染中影响有限。

**6. 像素真值代理引入的偏差**

relMSE 优化需要使用去噪图像作为像素真值的代理来计算相对方差。去噪图像本身可能引入偏差，尤其是在尖锐特征（如焦散边缘、几何边界）处。这种偏差会影响 RRS 因子的计算，可能导致在这些区域的分裂决策不够精确。

## 定位与知识库关联

### 改变的 Slot：RRS 决策从“仅看期望”到“效率感知”

现有路径追踪中的俄罗斯轮盘赌与分裂（RRS）方法，其决策输入可归纳为一个核心 slot：**用什么信息决定一条前缀路径应该被终止还是分裂**。经典方法（如基于反照率或吞吐量的 RR，Pharr et al., 2016；Arvo and Kirk, SIGGRAPH 1990）仅使用路径的局部权重；**ADRRS**（Vorba and Křivánek, *ACM Trans. Graph.* 2016）将这一 slot 扩展为基于伴随输运的期望贡献估计——即“这条路径对最终像素可能有多重要”。但 ADRRS 仍然遗漏了一个关键维度：它不区分“贡献大但方差小”和“贡献小但方差大”的路径，因此无法将算力精准投放到真正制造噪声的区域。

EARS 改变了这个 slot 的输入语义：**决策不再仅依赖期望贡献，而是直接以最大化渲染效率为目标**。效率定义为平均像素方差与平均像素成本的乘积的倒数（Eq. 2）。通过推导固定点迭代公式（Eq. 29），每个前缀路径的 RRS 因子由三部分乘积决定：前缀重要性、局部效率比（方差/成本）和全局效率比。这一改变使得 RRS 决策从“启发式地保留重要路径”升级为“在全局效率最优的意义上分配算力”。

### 知识库挂载点：效率驱动的采样资源分配

EARS 在知识库中的核心挂载点是 **效率感知的采样资源分配**。这个方向连接着两条研究脉络：

**上游脉络——RRS 的理论与启发式方法**。俄罗斯轮盘赌自 Arvo and Kirk（SIGGRAPH 1990）引入渲染以来，一直作为控制路径深度的启发式工具。ADRRS 将伴随输运引入 RRS，使得终止/分裂决策有了理论依据，但其优化目标是隐式的——通过保留高贡献路径间接提升效率。EARS 首次将 RRS 决策形式化为一个显式的连续优化问题，并给出了可证明收敛的迭代求解器。这一理论贡献（固定点迭代的收敛性证明，见 Appendix C）将 RRS 从工程技巧提升为有最优性保证的数学框架。

**下游脉络——在线学习与自适应采样**。EARS 的在线学习方案（Section 5）与图像空间自适应采样形成了互补关系：自适应采样在像素层面分配样本数，而 EARS 在路径前缀层面分配分裂/终止决策。论文明确指出，两者可以结合——在容易渲染的像素上减少主射线数量，同时用 EARS 处理路径内部的方差（Fig. 8, Fig. 12 的讨论）。这为后续工作提供了一个明确的组合方向。

### 适用边界与限制

EARS 的适用边界由以下条件划定：

1. **仅适用于前向路径追踪**。论文明确承认，将效率感知 RRS 扩展到双向路径追踪面临根本性困难：MIS 权重中会出现分裂协方差项，且目标函数的凸性不再成立。这是一个开放问题，而非工程挑战。

2. **依赖局部方差与成本的在线估计**。当空间缓存（5D 八叉树 + 方向直方图，Fig. 6）样本不足时，离散化估计会产生视觉伪影（Fig. 11）。在 Glossy Bathroom 场景中，局部方差的过度近似导致过度分裂，性能反比 ADRRS 低 9%——说明当缓存统计量不可靠时，效率优化的理论优势无法兑现。

3. **分裂方差的 O(1/n) 假设**。固定点迭代的推导假设分裂方差随分裂数 n 以 O(1/n) 衰减。在 QMC 采样下，这一假设不完全成立，可能影响最优性保证的严格性。

4. **相对方差优化依赖像素真值代理**。实际实现中使用去噪图像作为像素真值的近似（Section 4.3.1），这可能引入偏差，尤其在去噪器对特定材质或光照失效时。

### 后续启发与可迁移价值

EARS 的核心方法论——**将采样决策形式化为效率优化问题，并用固定点迭代在线求解**——具有跨问题迁移的潜力：

- **路径引导**：Fig. 10 展示了 EARS 与路径引导结合的初步结果，说明效率感知的采样决策可以与方向采样分布联合优化。
- **参与介质与体渲染**：论文将体渲染列为扩展方向，其挑战在于自由路径上的 RRS 决策空间更大，但效率优化的框架本身是可迁移的。
- **动态场景**：如何在时域上决定固定点迭代的重训练频率，以及哪些缓存数据需要丢弃，是一个兼具理论和工程价值的问题。

对于后续研究，EARS 最重要的启示是：**采样决策不应仅基于“重要性”，而应基于“单位成本能减少多少方差”**。这一原则在渲染以外的蒙特卡洛积分应用中同样成立。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/EARS_Efficiency_aware_Russian_Roulette_and_Splitting.pdf]]