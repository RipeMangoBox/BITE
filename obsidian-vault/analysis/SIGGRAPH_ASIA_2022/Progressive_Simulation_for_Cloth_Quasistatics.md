---
title: Progressive Simulation for Cloth Quasistatics
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Progressive_Simulation_for_Cloth_Quasistatics.pdf
project_link: null
code_link: null
aliases:
- PCSP
- PSCQ
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_physical_simulation
core_operator: 对粗级模拟的优化目标进行“富集”：在粗网格节点上构造混合能量，将细级别膜与弯曲力通过网格延拓和梯度投影的方式融入粗级目标函数，使得粗级平衡态能够预测细级的褶皱模式。
primary_logic: 通过构造包含细物理支持的代理能量并逐级最小化，PCS 在每一分辨率保证无穿透可行解的前提下，消除了传统级联方法中粗级锁死伪影的传递，实现了从粗到细的可预测、自一致的渐进仿真。
claims:
- PCS 能消除 Sensitive Couture 等级联方法中出现的尖锐褶皱和锁定伪影，并在多分辨率下保持一致的折叠行为。
- PCS 的粗级预览与收敛的高分辨率 C-IPC 解之间的互相关一致性距离比直接重模拟或 SC 方法小一个数量级。
- PCS 在龙形布料悬垂测试中获得 10 倍加速（122 秒 vs 1248 秒），同时不牺牲解的质量。
- Dragon drop test (布料垂落龙模型) 上 总耗时（秒） = 122 (PCS)
---

# Progressive Simulation for Cloth Quasistatics

> [!tip] 核心洞察
> 通过构造包含细物理支持的代理能量并逐级最小化，PCS 在每一分辨率保证无穿透可行解的前提下，消除了传统级联方法中粗级锁死伪影的传递，实现了从粗到细的可预测、自一致的渐进仿真。

| 字段 | 内容 |
|------|------|
| 中文题名 | 布料准静态的渐进模拟 |
| 英文题名 | Progressive Simulation for Cloth Quasistatics |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://pcs-sim.github.io/) |
| Topic | #topic/graphics_physical_simulation |
| Method | Progressive Cloth Simulation (PCS) |
| Dataset | Dragon drop test |

> [!tip] 效果简介
> - Dragon drop test (布料垂落龙模型) 上，总耗时（秒） 122 (PCS) vs 1248 (C-IPC direct) (10× 加速)。
> - 多场景布料悬垂一致性评估 上，平均曲率一致性距离（越小越好） PCS 值（close-to or greater-than an order of magnitude smaller） vs SC 或直接仿真值 (降低约一个数量级)。

## 概要

布料设计者面临一个根本性矛盾：粗粒度模拟速度快、可交互，但无法预测最终高分辨率解下的褶皱形态与折叠方式；直接进行高分辨率 C-IPC 仿真虽能保证物理准确性，却极其缓慢（例如龙形悬垂需 1248 秒），丧失交互探索的可能性。传统级联式渐进方法（如 Sensitive Couture）试图通过逐级细化来加速，但粗级产生的尖锐褶皱和锁定伪影会不可逆地传递到细级，导致跨分辨率行为不一致。

本文提出 **渐进布料仿真（Progressive Cloth Simulation, PCS）**，核心思想是对粗级模拟的优化目标进行“富集”：在粗网格节点上构造一个代理能量，将细级别的膜与弯曲力通过网格延拓和梯度投影融入粗级目标函数，使得粗级平衡态能够预测细级的褶皱模式。方法分为两个阶段——**预览模拟**在极粗网格（如 1.5K 三角形）上交互式编辑并实时求解富集后的代理能量；**渐进细化**则逐级求解代理能量最小化，通过安全延拓初始化保证无穿透可行解，最终收敛到与 C-IPC 一致的高分辨率平衡态。

实验表明，PCS 消除了 Sensitive Couture 等级联方法中的锁定伪影，粗级预览与收敛细解之间的曲率一致性距离比直接重模拟或 SC 方法小约一个数量级。在龙形布料垂落测试中，PCS 获得 **10 倍加速**（122 秒 vs 1248 秒）且不牺牲解的质量。方法定位为一种单向非线性多分辨率求解器，在每一分辨率层级均保证无穿透、满足应变限制，实现了从粗到细可预测、自一致的渐进仿真。

## 核心方法与创新机理

### 问题瓶颈与核心机制

布料设计的核心矛盾在于：粗粒度模拟速度快、支持交互编辑，但无法预测最终高分辨率解会呈现怎样的褶皱模式与折叠行为；而直接高分辨率模拟虽然能给出精确的收敛解，却极其缓慢（如 C-IPC 直接仿真一个悬垂场景需 1248 秒），完全丧失了交互性。更关键的是，传统级联式渐进方法（如 Sensitive Couture, Umetani et al., 2011）虽然尝试通过逐级细化来加速，但粗级解中因缺乏细物理信息而产生的“锁定伪影”——尖锐的非自然折痕与屈曲错误——会通过延拓传递到细级解，导致最终结果不可预测且与粗级预览不一致（Fig. 4, Fig. 6）。

![[assets/figures/papers/paper_list_l77_https_pcs_sim_github_io/figures/006_Figure_6.jpg]]
*Figure 6: Avoiding refinement inconsistencies. (Left) Cascadic methods like Sensitive Couture (SC) can suffer from inconsistent folds across levels. For example, the crumpled corner on levels 0 and 1 bifurcates into a different fold on levels 2 and 3. (Right) In contrast, PCS provides multi-level consistency so that the original coarse-scale folds are progressively refined predictively*

PCS 的核心机制是**对粗级模拟的优化目标进行“富集”（enrichment）**：在粗网格节点上构造一个混合代理能量，将细级别的膜力与弯曲力通过网格延拓和梯度投影的方式融入粗级目标函数。这使得粗级平衡态能够“感知”到细级物理的约束，从而预测出与最终高分辨率收敛解自洽的褶皱模式。这一机制的本质是将传统多分辨率方法中“粗级近似→细级修正”的单向信息流，转变为“细级物理反馈→粗级目标重塑”的双向耦合。

### 关键 Changed Slots

相较于传统级联方法和直接粗模拟，PCS 在三个关键设计槽位上做出了根本性改变：

**Slot 1: 粗级模拟目标能量。** 传统方法在粗网格上直接使用粗网格自身的膜与弯曲能量 $E_l$，这导致粗级解缺乏对细级褶皱行为的预测能力。PCS 将粗级目标替换为代理能量 $F_l(x_l) = C_l(x_l) + G(P^l x_l)$，其中 $C_l$ 是粗级接触势能（包含障碍、摩擦和应变限制），$G(P^l x_l)$ 则是通过延拓算子 $P^l$ 将粗级节点位置映射到细级网格后评估的细级壳势能。这一混合构造使得粗级优化在每一步都能“看到”细级物理对当前构型的响应，从而从根本上消除了粗级锁定伪影的生成源头（Fig. 10 展示了粗级力与 PCS 富集力在弯曲和膜力分布上的显著差异）。

**Slot 2: 层间传递方式。** 传统级联方法直接将粗级收敛解通过延拓上采样作为下一级的初始值，但这一过程可能引入穿透或远离可行域的初始猜测。PCS 采用“安全延拓”（Safe Prolongation）策略：首先通过重心上采样（barycentric upsampling）$x_l^{up} = U_l^{l-1} x_{l-1}^{t+1}$ 保证无穿透的拓扑更新，随后在该安全起点与延拓目标 $x_l^p$ 之间进行线搜索优化，最小化能量 $K_l(x, x_l^p) + B_l(x) + S_l|_{\mathcal{F}}(x) + A_l|_{\mathcal{F}^c}(x)$，其中 $K_l$ 度量与延拓目标的接近度，$B_l$ 为障碍势能，$S_l|_{\mathcal{F}}$ 为应变限制，$A_l|_{\mathcal{F}^c}$ 为受限 ARAP 能量（通过惩罚主拉伸超出限制来拉回可行域）。这一过程为下一级的牛顿求解提供了既可行又充分接近的初始猜测（Fig. 14 对比了不同延拓策略的效果）。

**Slot 3: 约束处理。** 传统粗级模拟往往忽略高分辨率细节的物理约束或缺乏应变限制，导致粗级解本身就不满足细级物理的基本要求。PCS 在所有层级（包括最粗的预览级）均保证无穿透、满足应变限制，并利用细尺度力避免伪影。这一全层级可行性保证是 PCS 实现跨分辨率一致性的基础条件。

### 模块架构与工作流

PCS 的完整工作流包含五个核心模块，按执行顺序构成两条路径：

**路径一：预览模拟（Preview Simulation）**
1. **网格层次结构构建**（§3.1 Hierarchy）：生成嵌套三角形网格序列 $l=0,1,\dots,L$，其中 $l=0$ 为最粗级。同时构建延拓算子 $P_{l+1}^l \in \mathbb{R}^{3n_{l+1} \times 3n_l}$（将粗级节点线性插值到细级）和投影算子 $\Pi_{l-1}^l = \big((P_l^{l-1})^T (P_l^{l-1})\big)^{-1} (P_l^{l-1})^T$（通过最小二乘将细级变形投影回粗级）。
2. **粗级预览模拟**（§4.5 Preview simulation）：在 $l=0$ 粗网格上，用户进行交互式编辑（手柄操控、材质切换、碰撞体变换等）。每次编辑后，求解器通过不精确牛顿法最小化代理能量 $F_0 + K_0$，其中 $K_0(x_0, y_0) = \frac{1}{2h^2} \|x_0 - y_0\|_{M_0}^2$ 为惯性项，保持时间步间的连续性。代理步的隐式欧拉更新公式为：
   $$\boldsymbol{x}_l = y_l - h^2 M_l^{-1} \nabla C(\boldsymbol{x}_l) - h^2 M_l^{-1} \boldsymbol{P}^{l^T} \nabla G(\boldsymbol{P}^l \boldsymbol{x}_l)$$
   该公式显式展示了代理能量的梯度结构：第一项为粗级接触力的贡献，第二项为细级壳力通过延拓的雅可比 $\boldsymbol{P}^{l^T}$ 投影回粗级空间的贡献。预览模拟平均比直接粗模拟慢 56%，但收敛速度更快（平均 14%），交互性仍可维持。

**路径二：渐进细化模拟（Refinement Simulation）**
3. **安全延拓初始化**（§4.3 Safe prolongation）：当用户对粗级预览满意后，PCS 自动启动渐进细化。对于每一级 $l=1,\dots,L$，首先通过重心上采样获得安全起点，再通过线搜索优化找到最接近延拓目标 $x_l^p$ 的可行初始猜测。
4. **代理能量最小化**（§4.4 Proxy energy minimization）：在当前级 $l$ 上，通过不精确牛顿法结合投影 Hessian 预条件器求解代理能量 $F_l + K_l$ 的最小化问题。预条件器利用未修改的粗模型增量势能 $E_l + K_l$ 的 Hessian 投影，加速线性系统的求解。每一级求解至收敛（使用 C-IPC 默认容差 0.01），确保该级解是代理能量的稳定平衡态。
5. **层级传递**：将当前级的收敛解作为下一级安全延拓的输入，重复步骤 3-4，直至达到最高分辨率 $L$。最终级解即为完全收敛的高保真 C-IPC 仿真结果。

### 关键公式与因果关系

**代理能量的构造逻辑：**
$$F_l(x_l) = C_l(x_l) + G(P^l x_l)$$
这一公式是 PCS 全部创新性的数学凝练。$C_l$ 包含粗级接触障碍势能、摩擦势能和应变限制势能，保证粗级解满足基本物理可行性。$G(P^l x_l)$ 通过延拓算子 $P^l$ 将粗级节点位置映射到细级网格，然后在细级网格上评估完整的壳势能（膜能量 + 弯曲能量），使得粗级优化能感知到细级几何对当前粗构型的物理响应。这种“粗级变量、细级评估”的混合策略，使得粗级平衡态自动趋向于细级物理所偏好的褶皱模式，从而消除了传统方法中粗级解与细级解之间的系统性偏差。

**安全延拓的优化目标：**
$$K_l(x, x_l^p) + B_l(x) + S_l|_{\mathcal{F}}(x) + A_l|_{\mathcal{F}^c}(x)$$
四项能量各自承担明确的因果角色：$K_l$ 驱动解向延拓目标靠近（保持跨层级几何一致性）；$B_l$ 保证无穿透（可行性约束）；$S_l|_{\mathcal{F}}$ 对已满足应变限制的三角形施加零惩罚，对违反者施加障碍势能；$A_l|_{\mathcal{F}^c}(x) = \kappa_a \sum_{f \in \mathcal{F}^c} \sum_{i \in [1,2]} (\sigma_{f_i} - 1)^2$ 对尚未满足应变限制的三角形施加二次惩罚，将其主拉伸拉回允许范围。这四项的协同作用确保了初始猜测既可行又充分接近目标，为后续牛顿求解提供了良好的收敛起点。

**模块间的因果链：**
网格层次结构为延拓/投影算子提供了几何基础；延拓算子使得细级物理信息能反馈到粗级代理能量中；代理能量改变了粗级优化的目标景观，使得粗级平衡态具有细级褶皱的预测性；安全延拓保证了层级间传递的可行性与接近性；投影 Hessian 预条件器加速了代理能量最小化的收敛。整个链条形成闭环：细级物理 → 代理能量 → 粗级预览 → 安全延拓 → 细级收敛，每一步都依赖于前一步的输出质量。

## 实验与关键发现

### 核心性能与加速效果

PCS 最直接的性能优势体现在“一次性”高分辨率仿真任务的加速上。在龙形布料悬垂测试（Dragon drop test）中，五级渐进仿真将一块布料悬垂至龙模型上，最终收敛到 370K 三角形的解，总耗时仅 **122 秒**，而直接对高分辨率模型进行 C-IPC 仿真则需要 **1248 秒**，PCS 实现了约 **10 倍加速**（Fig. 13）。这一加速并非以牺牲解的质量为代价——PCS 的最终解是完全收敛的 C-IPC 平衡态，具备高保真褶皱和精确的无穿透摩擦接触行为。

![[assets/figures/papers/paper_list_l77_https_pcs_sim_github_io/figures/013_Figure_13.jpg]]
*Figure 13: Dragon drop test. PCS progression also significantly speeds up direct “one-shot” simulation tasks when scene parameters are already known. (Blue) a five-level PCS simulation of a cloth drape on a dragon converges to 370K triangle drape solution with a 10X speed-up over a direct simulation solve (Orange) of the high-resolution model*

### 一致性验证：消除级联伪影与跨分辨率可预测性

PCS 的核心价值在于实现从粗到细的**可预测渐进仿真**，而非简单的加速。传统级联方法（如 Sensitive Couture, SC）在逐级细化时会将粗级产生的尖锐褶皱和锁定伪影传递至精细解，导致最终结果不可预测（Fig. 4）。PCS 通过富集代理能量，在粗级求解时即融入细级膜与弯曲力的信息，从根源上避免了这些伪影的产生。

定量评估采用**平均曲率一致性距离**作为度量：PCS 粗级预览与收敛的高分辨率 C-IPC 解之间的互相关一致性距离，比直接重模拟或 SC 方法**小约一个数量级**（§6.2 Consistency Analysis）。在多级渐进过程中，SC 方法会出现褶皱分叉现象——例如揉皱的角落在 0 级和 1 级呈现一种折叠模式，而在 2 级和 3 级却分叉为完全不同的折叠形态；相比之下，PCS 在所有分辨率级别上保持一致的折叠行为，粗级褶皱被可预测地渐进细化（Fig. 6）。

### 与商业软件的对比

与 Marvelous Designer 和 Vellum（Houdini）的对比进一步揭示了 PCS 的独特优势（Fig. 2）。在低分辨率粗网格上，Marvelous Designer 和 Vellum 均产生大量不期望的折痕伪影，而这些伪影在 PCS 的粗级解中完全不存在——因为 PCS 的粗级能量富集了细尺度的布料力和能量评估。更关键的是，当尝试对粗设计进行“升分辨率”重模拟时，两个商业软件在不同分辨率下展现出截然不同的折叠模式，Vellum 还出现穿透和不一致的材料拉伸，Marvelous Designer 则出现爆炸性不稳定。PCS 则始终生成与交互式粗网格预览一致的高保真、无伪影的细尺度布料仿真。

![[assets/figures/papers/paper_list_l77_https_pcs_sim_github_io/figures/002_Figure_2.jpg]]
*Figure 2: Consistent and stable cloth up-resing. Designing with interactive coarse cloth models and then re-running at a higher resolution can lead to undesirable and unpredictable outcomes in traditional cloth solvers. For example, (Left) both Marvelous Designer (MD, in green) and Vellum (in purple) produce numerous undesirable creasing artifacts at low mesh resolutions, which are notably absent in (Right) the coarse level-0 PCS solution due to its enrichment with fine-scale cloth forces and energy evaluations. Furthermore, trying to “up-res” coarse cloth designs by then re-running them at higher resolutions leads to unpredictable results: (Left) both MD and Vellum exhibit dramatically different fol...*

**公平性说明**：Marvelous Designer 和 Vellum 利用了 GPU 加速，而 PCS 为 CPU 实现；作者已尽可能匹配材质参数，但商业软件参数不透明，可能影响对比公正性。所有方法均使用 C-IPC 默认收敛容差 0.01 终止，保证了对比基准一致。

### 消融实验与关键设计验证

**延拓算子的选择**（Fig. 14）：单纯使用面内中点上升（in-plane midpoint upsampling）作为延拓算子虽然从可行性角度是安全的，但会导致粗折痕伪影传播至精细解。改用平滑的 Loop 细分作为延拓算子后，这一问题得到有效缓解，证明了延拓算子的光滑性对消除伪影传递至关重要。

**收敛容差的后置调整**（Fig. 15）：PCS 允许用户在较低的“草稿”容差设置下设计和预览高保真细尺度结果，然后在最终阶段降低容差以获得更多褶皱细节。这一特性使得用户无需重新模拟粗级即可在最终解上增加细节丰富度，进一步提升了工作流的灵活性。

**粗级预览的开销与收敛**（§6.2）：粗级预览模拟平均比直接粗模拟慢 56%，但其收敛速度更快（平均快 14%），且交互性仍可维持。当精细网格从 23K 三角形增加到 1.4M 三角形时，每步预览时间仅从 0.1 秒增加到 0.3 秒（§6.2 Scaling），表明预览开销对最终分辨率的增长具有良好的可扩展性。

**材质鲁棒性**（Fig. 16）：针对丝绸、牛仔布、羊毛等七种不同真实世界材质参数，PCS 均能保持多级褶皱一致性，展现出对不同材料刚度行为的广泛适用性。

**网格拓扑独立性**（Fig. 11）：在不同基础三角剖分下，SC 方法始终产生折痕伪影，而 PCS 的粗仿真保持无伪影，且与收敛的精细解一致，证明 PCS 对网格拓扑变化具有鲁棒性。

### 失败模式与适用边界

尽管 PCS 在多个维度上展现出显著优势，其方法仍存在明确的局限：

1. **缺乏理论保证**：PCS 目前仅提供经验一致性，对于严重扭曲或揉皱的布料配置，缺乏预测一致性的形式化理论保证。在极端变形场景下，代理能量能否始终准确预测细级行为仍需进一步验证。

2. **几何域限制**：方法针对二维平面布料设计，扩展到曲面壳体或体弹性体需要在非欧几里德域上重新设计层次结构和延拓算子，当前框架无法直接适用。

3. **服装复杂度不足**：未处理带有精细边界和复杂缝纫约束的服装（如衣领、袖口），限制了在完整服装设计工作流中的应用。

4. **材料模型限制**：仅针对纯弹性布料，未考虑塑性或永久变形，无法模拟布料的历史依赖行为。

5. **预览步时的适度增长**：尽管粗级交互速度很快，预览步时随最终级网格规模增加而适度增长（从 0.1s 到 0.3s），在极端高分辨率场景下可能影响交互流畅性。作者指出未来可探索 GPU 加速来解决此问题。

![[assets/figures/papers/paper_list_l77_https_pcs_sim_github_io/figures/010_Figure_10.jpg]]
*Figure 10: Coarse v.s. PCS cloth forces. Visualization of coarse-level bending and membrane forces using (Top) the coarse-mesh force evaluation versus (Bottom) PCS forces obtained by evaluating fine-scale cloth forces on prolongated geometry followed by subsequent projection back to the coarse scale. The latter avoids ill-scaled values, which can generate locking and numerical artifacts*

![[assets/figures/papers/paper_list_l77_https_pcs_sim_github_io/figures/012_Figure_11.jpg]]
*Figure 11: Changing base triangulation. Each column presents a different base-mesh triangulation. SC suffers from creasing artifacts regardless of mesh, while, PCS coarse simulations remain artifact free, and consistent with their converged fine counterparts across different tesselations*

![[assets/figures/papers/paper_list_l77_https_pcs_sim_github_io/figures/003_Figure_3.jpg]]
*Figure 3: Previsualization results, using coarse (Left) simulation, give “previews” that are generally far from final (Right) simulation results that are then produced by slow, high-resolution simulations using the same selected settings*

## 定位与知识库关联

PCS 的核心定位是**交互式布料设计的跨分辨率一致性预览与渐进细化框架**，其根本改变在于对粗级模拟目标函数的重新定义。传统级联式方法（如 **Sensitive Couture** (Umetani et al., 2011)）和商业软件（如 Marvelous Designer、Vellum/Houdini）均采用“粗网格独立模拟→上采样作为细级初值”的策略：粗级仅使用自身低分辨率网格的膜与弯曲能量 $E_l$，完全无视细尺度物理，导致粗预览与最终高分辨率解之间出现不可预测的褶皱分歧（Fig. 3, Fig. 2）。PCS 将这一粗级目标能量槽位替换为富集的代理能量 $F_l(x_l) = C_l(x_l) + G(P^l x_l)$，其中 $C_l$ 为粗级接触势能，$G(P^l x_l)$ 通过延拓算子 $P^l$ 评估细级壳体力并投影回粗网格。这一改变使得粗级平衡态能够“感知”细级膜与弯曲力的分布，从而在交互速率下预测最终褶皱模式。

第二个关键槽位是**层间传递方式**。Sensitive Couture 直接将粗级解延拓作为下一级初始值，但粗级锁定的尖锐折痕会不可逆地传递到细级（Fig. 4）。PCS 引入安全延拓机制：先通过重心上采样保证无穿透可行起点，再沿可行方向搜索最接近延拓目标的配置（§4.3），从根本上切断伪影的跨层级传播。

在知识库中的挂载点，PCS 位于**多分辨率物理仿真**与**增量势能接触力学**的交汇处。其直接继承的基础设施是 **C-IPC**（Li et al., 2021）的无穿透摩擦接触模型与应变限制框架，PCS 的所有层级均在此约束下求解，保证了可行性。在层次结构构建上，PCS 采用标准的嵌套三角形网格与线性延拓/投影算子对 $(P_{l+1}^l, \Pi_{l-1}^l)$，这与经典几何多重网格方法共享数学骨架，但 PCS 并非线性系统的多重网格求解器，而是**非线性代理能量的逐级最小化**：每一级都求解一个修改后的隐式欧拉增量势能最小化问题，直至收敛。

与知识库中已有工作的本质差异体现在三个维度：

1. **与级联仿真（cascadic simulation）的区别**：Sensitive Couture 等方法的粗级解仅作为细级初始猜测，粗级自身不包含细级信息，导致“所见非所得”。PCS 的粗级本身就是细级平衡态的预测，粗预览与收敛解之间的曲率一致性距离比 SC 小约一个数量级（§6.2）。

2. **与直接高分辨率仿真的区别**：C-IPC 直接仿真虽然精度最高，但无法提供交互式预览——粗网格模拟的预览结果与最终解差异巨大（Fig. 3）。PCS 在龙形悬垂测试中实现了 10 倍加速（122 秒 vs 1248 秒），同时保持与 C-IPC 收敛解一致的褶皱结构（Fig. 13）。

3. **与商业布料软件的区别**：Marvelous Designer 和 Vellum 在低分辨率下产生大量非物理的折痕伪影，且跨分辨率上采样后褶皱行为发生剧烈变化（Fig. 2）。PCS 通过代理能量富集消除了粗级伪影，并在多分辨率下保持自洽的折叠模式。

PCS 的适用边界明确：当前框架针对**二维平面布料的准静态悬垂**设计，依赖纯弹性材料假设，不处理塑性变形、复杂缝纫约束（衣领、袖口）或动态连续运动。方法仅在经验层面验证了一致性，缺乏对严重扭曲/揉皱配置下预测一致性的理论保证。扩展到曲面壳体或体弹性体需要在非欧几里德域上重新设计层次结构与延拓算子。

从后续启发角度看，PCS 开辟了若干值得关注的方向：代理能量富集的思想可推广至其他“粗预览需预测细结果”的场景（如体弹性断裂预览）；安全延拓机制为需要保证无穿透的层次化求解器提供了通用初始化策略；PCS 生成的多分辨率自洽数据对为训练学习型粗仿真提升器提供了天然监督信号。此外，PCS 的投影 Hessian 预条件器与不精确牛顿法的结合，为接触密集型层次仿真的高效线性求解指出了与多重网格预处理进一步整合的可能性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Progressive_Simulation_for_Cloth_Quasistatics.pdf]]